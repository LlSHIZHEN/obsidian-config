#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export.py —— 从一个正在使用的 Obsidian vault 扫描社区插件，生成插件清单。

为什么需要它：插件自己的 manifest.json 里【没有】源码仓库地址，
只有 author / authorUrl（而且这些信息会过时）。所以必须拿插件 id 去查
Obsidian 官方的 community-plugins.json（7700+ 个插件）来解析出真实仓库。

产出：
  plugins.json  机器可读清单（id → 仓库 → 锁定版本 → commit → 许可证）
  PLUGINS.md    人类可读表格（含作者与来源，便于公开仓库标注出处）
  config/       核心插件开关、外观等配置快照

用法：
  python3 scripts/export.py <源 vault 路径> [--out <输出根目录>]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

OFFICIAL_LIST = (
    "https://raw.githubusercontent.com/obsidianmd/"
    "obsidian-releases/master/community-plugins.json"
)

# GitHub CLI 在本机可能不在 PATH 里（例如装在 ~/.local/bin）
GH_CANDIDATES = ["gh", os.path.expanduser("~/.local/bin/gh")]


def find_gh():
    for c in GH_CANDIDATES:
        try:
            subprocess.run([c, "--version"], capture_output=True, check=True)
            return c
        except Exception:
            continue
    return None


class Api:
    """优先用已认证的 gh（5000 次/小时），退化到匿名 API（60 次/小时）。"""

    def __init__(self):
        self.gh = find_gh()
        if not self.gh:
            print("⚠️  未找到 gh CLI，将使用匿名 GitHub API（限额 60 次/小时，"
                  "插件多时可能失败）。建议先安装并登录 gh。", file=sys.stderr)

    def get(self, path, ref=None):
        if self.gh:
            url = path if ref is None else "%s?ref=%s" % (path, ref)
            p = subprocess.run([self.gh, "api", url],
                               capture_output=True, text=True)
            if p.returncode != 0:
                raise RuntimeError(p.stderr.strip()[:200])
            return json.loads(p.stdout)
        url = "https://api.github.com/" + path.lstrip("/")
        if ref:
            url += "?ref=" + ref
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "obsidian-plugin-kit",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)


def load_json(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scan_vault(vault):
    """"正在使用"的定义 = community-plugins.json 里列出（即已启用）的插件。"""
    cfg = os.path.join(vault, ".obsidian")
    enabled = load_json(os.path.join(cfg, "community-plugins.json"), []) or []
    plugins = []
    for pid in enabled:
        mf = os.path.join(cfg, "plugins", pid, "manifest.json")
        man = load_json(mf)
        if not man:
            print("⚠️  插件 %s 在 community-plugins.json 中已启用，"
                  "但 manifest.json 缺失，已跳过" % pid, file=sys.stderr)
            continue
        plugins.append(man)
    return plugins, cfg


def resolve_repos(ids):
    print("→ 拉取 Obsidian 官方插件索引以解析源码仓库…")
    with urllib.request.urlopen(OFFICIAL_LIST, timeout=60) as r:
        official = json.load(r)
    m = {p["id"]: p.get("repo") for p in official}
    print("  官方索引共 %d 个插件" % len(official))
    return {i: m.get(i) for i in ids}


def license_info(api, repo, ref):
    try:
        d = api.get("repos/%s/license" % repo, ref=ref)
        lic = d.get("license") or {}
        return {
            "spdx": lic.get("spdx_id") or "NOASSERTION",
            "name": lic.get("name") or "Unknown",
            "path": d.get("path"),
            "text": base64.b64decode(d["content"]).decode("utf-8", "replace")
            if d.get("content") else None,
        }
    except Exception as e:
        return {"spdx": "UNKNOWN", "name": "查询失败: %s" % e,
                "path": None, "text": None}


def build(vault, outdir):
    plugins, cfg = scan_vault(vault)
    if not plugins:
        print("没有扫描到任何已启用的社区插件。", file=sys.stderr)
        return 1

    api = Api()
    repos = resolve_repos([p["id"] for p in plugins])

    entries = []
    for man in plugins:
        pid = man["id"]
        repo = repos.get(pid)
        # 官方索引里的仓库名可能已过时（作者改名/迁移组织）。查一次规范名，
        # 否则清单里的链接与下载地址都会指向旧地址。
        if repo:
            try:
                canonical = api.get("repos/%s" % repo).get("full_name")
                if canonical:
                    repo = canonical
            except Exception:
                pass
        ver = man.get("version", "")
        entry = {
            "id": pid,
            "name": man.get("name", pid),
            "version": ver,
            "minAppVersion": man.get("minAppVersion"),
            "isDesktopOnly": bool(man.get("isDesktopOnly")),
            "author": man.get("author", ""),
            "authorUrl": man.get("authorUrl", ""),
            "repo": repo,
            "tag": ver if repo else None,
            "commit": None,
            "license": None,
            "licenseFile": None,
            "bundle": "bundles/%s/%s" % (pid, ver) if ver else None,
            "sourceArchive": None,
        }
        if repo and ver:
            try:
                ref = api.get("repos/%s/git/ref/tags/%s" % (repo, ver))
                entry["commit"] = ref["object"]["sha"]
            except Exception as e:
                print("  ⚠️  %s 解析 tag %s 失败: %s" % (repo, ver, str(e)[:70]),
                      file=sys.stderr)
            lic = license_info(api, repo, ver)
            lic.pop("text", None)  # 全文单独存 LICENSE 文件，不塞进 json
            entry["license"] = lic
            entry["licenseFile"] = "bundles/%s/%s/LICENSE" % (pid, ver)
            # GPL 系列是强 copyleft：分发二进制必须同时提供对应源码
            if str(lic["spdx"]).startswith("GPL"):
                entry["sourceArchive"] = "bundles/%s/%s/source.tar.gz" % (pid, ver)
        else:
            print("  ⚠️  %s 未能解析源码仓库，清单中留空" % pid, file=sys.stderr)
        entries.append(entry)
        print("  ✓ %-26s %-8s %s" % (pid, ver, repo or "❌ 未知仓库"))

    data = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # 只记 vault 名称，不记绝对路径：本仓库是 public 的，
        # 绝对路径会暴露本机用户名等环境信息
        "generatedFromVault": os.path.basename(vault.rstrip("/")),
        "pluginCount": len(entries),
        "plugins": entries,
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "plugins.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 配置快照：核心插件开关 + 外观，新电脑靠它复刻主题与核心插件状态
    cfgdir = os.path.join(outdir, "config")
    os.makedirs(cfgdir, exist_ok=True)
    for fn in ("core-plugins.json", "appearance.json", "app.json"):
        src = os.path.join(cfg, fn)
        if os.path.isfile(src):
            with open(src, encoding="utf-8") as a, \
                 open(os.path.join(cfgdir, fn), "w", encoding="utf-8") as b:
                b.write(a.read())

    write_plugins_md(data, outdir)
    write_notice_md(data, outdir)
    print("\n✅ 已生成 plugins.json（%d 个插件）、PLUGINS.md、NOTICE.md 与 config/"
          % len(entries))
    return 0


def write_notice_md(data, outdir):
    """第三方归属声明。自动生成，避免手工维护导致声明与实物不符。
    仓库是 public 的，这份文件是合规的关键：谁的作品、来自哪里、什么许可证。"""
    strong = [p for p in data["plugins"]
              if str((p.get("license") or {}).get("spdx", "")).startswith("GPL")]
    L = [
        "# 第三方插件归属声明 / Third-Party Notices",
        "",
        "> 本文件由 `scripts/export.py` 自动生成，请勿手工编辑。",
        "",
        "## 性质说明",
        "",
        "本仓库是**个人 Obsidian 配置的迁移备份**，与下列任何插件作者、",
        "以及 Obsidian 官方（Dynalist Inc.）**均无隶属或 endorsement 关系**。",
        "所有插件的著作权归其各自作者所有，此处按各插件原有许可证原样分发。",
        "`Obsidian` 是 Dynalist Inc. 的商标，仅用于说明用途。",
        "",
        "## 插件出处与许可证",
        "",
        "| 插件 ID | 名称 | 版本 | 作者 | 来源仓库 | 许可证 | 锁定 commit |",
        "|---|---|---|---|---|---|---|",
    ]
    for p in data["plugins"]:
        repo = p["repo"] or "❌ 未知"
        repo_md = "[%s](https://github.com/%s)" % (repo, repo) if p["repo"] else repo
        lic = p["license"] or {}
        spdx = lic.get("spdx", "—")
        licfile = p.get("licenseFile") or "—"
        L.append("| `%s` | %s | `%s` | %s | %s | [`%s`](%s) | `%s` |" % (
            p["id"], p["name"], p["version"], p["author"] or "—", repo_md,
            spdx, licfile if licfile != "—" else "#",
            (p["commit"] or "—")[:12]))
    L += [
        "",
        "对照关系：上表每一行对应 `bundles/<插件 ID>/<版本>/`，该目录内包含",
        "",
        "- `main.js` / `manifest.json` / `styles.css` —— 插件作者发布的原始产物",
        "- `LICENSE` —— 该作者仓库中该版本 tag 下的许可证**全文**",
        "- `checksums.txt` —— 上述文件的 sha256，用于校验完整性",
        "",
        "## 各许可证对应的分发义务",
        "",
        "| 许可证 | 义务 | 本仓库如何履行 |",
        "|---|---|---|",
        "| MIT | 保留版权声明与许可证全文 | 每个 bundle 内附 `LICENSE` 全文 |",
        "| MPL-2.0 | 保留许可证、说明源码可得 | `LICENSE` 全文 + 来源仓库链接 |",
        "| GPL-3.0 | 强 copyleft：分发二进制**必须同时提供对应源码** | 额外附 `source.tar.gz` 源码归档 |",
        "",
    ]
    if strong:
        L += [
            "### 强 copyleft 插件的额外说明",
            "",
            "以下插件使用 GPL 系列许可证，仅提供二进制而不提供源码**不合规**，",
            "因此本仓库为它们一并保存了对应 tag 的完整源码归档：",
            "",
        ]
        for p in strong:
            L.append("- **%s** `%s` —— %s；源码归档：`%s`" % (
                p["name"], p["version"],
                (p.get("license") or {}).get("spdx", "GPL"),
                p.get("sourceArchive") or "（缺失，请勿分发）"))
        L.append("")
    L += [
        "## 如果你要拿走这里的插件",
        "",
        "请不要直接用本仓库的副本，而是回到**上游来源仓库**下载最新版，",
        "这样才能拿到作者的安全修复。本仓库锁定旧版本，只为迁移还原之用。",
        "",
        "## 权利人的移除请求",
        "",
        "若你是某插件的作者，不希望自己的产物出现在本仓库，",
        "请提 Issue，我会立即移除对应目录。",
        "",
    ]
    with open(os.path.join(outdir, "NOTICE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def write_plugins_md(data, outdir):
    L = [
        "# 插件清单",
        "",
        "> 本文件由 `scripts/export.py` 自动生成，请勿手工编辑。",
        "",
        "生成时间：`%s`　|　来源 vault：`%s`　|　插件数：**%d**"
        % (data["generatedAt"], data.get("generatedFromVault", "—"),
           data["pluginCount"]),
        "",
        "## 社区插件",
        "",
        "| 插件 ID | 名称 | 版本 | 作者 | 源码仓库 | 许可证 |",
        "|---|---|---|---|---|---|",
    ]
    for p in data["plugins"]:
        repo = "❌ 未解析"
        if p["repo"]:
            repo = "[%s](https://github.com/%s)" % (p["repo"], p["repo"])
        lic = (p["license"] or {}).get("spdx", "—")
        author = p["author"] or "—"
        if p.get("authorUrl"):
            author = "[%s](%s)" % (author, p["authorUrl"])
        L.append("| `%s` | %s | `%s` | %s | %s | `%s` |"
                 % (p["id"], p["name"], p["version"], author, repo, lic))
    L += [
        "",
        "## 版本锁定与溯源",
        "",
        "每个插件都锁定到**本机正在使用的确切版本**，并记录了该 tag 对应的 commit。",
        "因此即使上游发新版、迁移仓库、甚至删库，仍可还原到完全相同的状态。",
        "",
        "| 插件 ID | 锁定 tag | commit SHA |",
        "|---|---|---|",
    ]
    for p in data["plugins"]:
        L.append("| `%s` | `%s` | `%s` |"
                 % (p["id"], p["tag"] or "—", (p["commit"] or "—")[:12]))
    L += [
        "",
        "## 版权与出处",
        "",
        "所有插件的著作权归其各自作者所有。本仓库仅作为个人配置的迁移备份，",
        "按各插件原有许可证分发。完整归属声明见 [NOTICE.md](NOTICE.md)，",
        "许可证全文见 `bundles/<插件>/<版本>/LICENSE`。",
        "",
        "GPL 系列为强 copyleft 协议，分发二进制时必须同时提供对应源码，",
        "因此这些插件的源码归档一并存放在同目录的 `source.tar.gz`。",
        "",
    ]
    with open(os.path.join(outdir, "PLUGINS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault", help="源 Obsidian vault 路径")
    ap.add_argument("--out", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    if not os.path.isdir(os.path.join(a.vault, ".obsidian")):
        print("错误：%s 看起来不是 Obsidian vault（缺 .obsidian）" % a.vault,
              file=sys.stderr)
        return 2
    return build(os.path.abspath(a.vault), os.path.abspath(a.out))


if __name__ == "__main__":
    sys.exit(main())
