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
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

OFFICIAL_LIST = (
    "https://raw.githubusercontent.com/obsidianmd/"
    "obsidian-releases/master/community-plugins.json"
)

# 主题的官方索引：插件有 community-plugins.json，主题对应 community-css-themes.json
OFFICIAL_THEMES = (
    "https://raw.githubusercontent.com/obsidianmd/"
    "obsidian-releases/master/community-css-themes.json"
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

    print("\n→ 扫描主题与 CSS 片段（只记录来源，不打包）…")
    appearance = scan_appearance(vault, api)

    data = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # 只记 vault 名称，不记绝对路径：本仓库是 public 的，
        # 绝对路径会暴露本机用户名等环境信息
        "generatedFromVault": os.path.basename(vault.rstrip("/")),
        "pluginCount": len(entries),
        "plugins": entries,
        "appearance": appearance,
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
    write_appearance_md(data, outdir)
    print("\n✅ 已生成 plugins.json（%d 个插件）、PLUGINS.md、NOTICE.md、"
          "APPEARANCE.md 与 config/" % len(entries))
    return 0


def write_appearance_md(data, outdir):
    a = data.get("appearance") or {}
    t = a.get("theme")
    L = [
        "# 主题与 CSS 片段",
        "",
        "> 本文件由 `scripts/export.py` 自动生成，请勿手工编辑。",
        "",
        "本仓库**不包含**主题与 CSS 片段的文件本体。它们多为 GPL / AGPL 作品，",
        "在公开仓库里分发会引入 copyleft 分发义务，因此这里只记录**来源、",
        "锁定 commit 与 sha256 校验和**，由 `install.py --with-appearance` ",
        "在安装时回上游下载并逐个校验。",
        "",
    ]
    if t:
        L += [
            "## 主题",
            "",
            "| 名称 | 作者 | manifest 声明版本 | 来源仓库 | 锁定 ref | ref 类型 |",
            "|---|---|---|---|---|---|",
            "| %s | %s | `%s` | %s | `%s` | %s |" % (
                t.get("name", "—"),
                "[%s](%s)" % (t.get("author"), t.get("authorUrl"))
                if t.get("authorUrl") else (t.get("author") or "—"),
                t.get("version") or "—",
                "[%s](https://github.com/%s)" % (t["repo"], t["repo"])
                if t.get("repo") else "❌ 未解析",
                t.get("ref") or "—",
                t.get("refKind") or "—"),
            "",
        ]
        if t.get("refKind") == "main-head":
            L += [
                "> ⚠️ **版本号不可信**：该主题 `manifest.json` 声明版本为 "
                "`%s`，但其实际内容与 `main` 分支一致，与该版本 tag 的发布产物"
                "**内容不同**。因此这里锁定的是 commit 而非版本号 —— 按版本号"
                "下载会装回另一个文件。" % (t.get("version") or "?"),
                "",
            ]
        if not t.get("ref"):
            L += [
                "> ❌ **无法自动还原**：本地主题内容与上游任何 ref 都不匹配，"
                "可能被本地修改过。新电脑上只能手工处理。",
                "",
            ]
    if a.get("snippets"):
        L += [
            "## CSS 片段",
            "",
            "| 文件 | 大小 | 注释中声明的作者 | 注释中声明的许可证 | 来源 |",
            "|---|---|---|---|---|",
        ]
        for s in a["snippets"]:
            L.append("| `%s` | %d B | %s | `%s` | %s |" % (
                s["file"], s["bytes"],
                s.get("declaredAuthor") or "未声明",
                s.get("declaredLicense") or "未声明",
                "[上游](%s)" % s["sourceUrl"] if s.get("sourceUrl") else "❌ 未知"))
        L += [
            "",
            "> 片段通常没有 manifest，许可证与作者信息只写在 CSS 注释里，",
            "上表由脚本从注释中解析得到，可能不完整。",
            "",
            "### 许可证不一致的提示",
            "",
            "这些片段来自 AnuPpuccin 仓库，部分文件的注释声明为 **AGPL-3.0**，",
            "而该仓库自身的 LICENSE 文件是 **GPL-3.0**。两者不一致时，",
            "本清单按文件注释里声明的、更严格的许可证记录。若你要另行使用",
            "这些文件，请自行向上游作者确认。",
            "",
        ]
    L += [
        "## 校验方式",
        "",
        "`plugins.json` 的 `appearance` 段里为每个文件记录了 `sha256`。",
        "安装脚本下载后会比对；不一致就报错退出，避免静默装出一个外观不对的 vault。",
        "",
    ]
    with open(os.path.join(outdir, "APPEARANCE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


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
        "## 主题与 CSS 片段：本仓库不包含，仅作指引",
        "",
        "`config/appearance.json` 里引用的主题与 CSS 片段**不在本仓库中**。",
        "它们同样是他人的作品（多方使用 GPL / AGPL 系列许可证），",
        "但本仓库**没有分发它们的文件本体**，因此在这一点上不产生再分发义务；",
        "清单里只记录了名称、作者、来源仓库、锁定的 commit 与 sha256 校验和，",
        "由使用者在安装时**自行从上游获取**。",
        "",
        "详见 [APPEARANCE.md](APPEARANCE.md)。",
        "",
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


# ---------------------------------------------------------------- 外观资产
# 主题与 CSS 片段按使用者选择【不打包】进仓库：它们多为 GPL/AGPL 作品，
# 在 public 仓库里分发会引入 copyleft 义务。这里只记录来源、锁定 commit
# 与每个文件的 sha256；安装时回上游下载，并逐个校验，保证装回来的一致。

LICENSE_HINTS = [
    ("AGPL", "AGPL-3.0"), ("GPL", "GPL-3.0"), ("MPL", "MPL-2.0"),
    ("Mozilla", "MPL-2.0"), ("MIT", "MIT"),
    ("Apache", "Apache-2.0"), ("BSD", "BSD"),
]

# 识别许可证名必须用 \b 词边界、且把 AGPL 放在 GPL 之前：
#  · "imitation" 里的 mit 不该被判成 MIT（曾真实误判过）
#  · "AGPLv3" 里若先匹配 GPL 会判成 GPL
LICENSE_LINE_RE = re.compile(
    r"\b(AGPL|GPL|Mozilla|MPL|MIT|Apache|BSD)(?:[-\s]?v?\d|[\s,;/.)]|$)",
    re.I)
LICENSE_KW_RE = re.compile(r"licen|copyright|spdx|copyleft", re.I)
# 这些缩写几乎不会出现在普通英文里，可以不要求同一行有 license 关键词；
# MIT / BSD / Apache 则是常见单词（如 "imitation"、"apache"），必须同行有声明
LICENSE_UNAMBIGUOUS = {"AGPL", "GPL", "MPL", "MOZILLA"}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    with open(p, "rb") as f:
        return sha256_bytes(f.read())


def raw_url(repo, ref, path):
    return "https://raw.githubusercontent.com/%s/%s/%s" % (repo, ref, path)


def fetch_raw(repo, ref, path):
    try:
        req = urllib.request.Request(raw_url(repo, ref, path),
                                     headers={"User-Agent": "kit"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read()
    except Exception:
        return None


def sniff_license(text):
    """片段通常没有 manifest，版权信息只写在 CSS 注释里，需要嗅探。

    只在含 license/copyright 等关键词的行里识别许可证名，并强制词边界，
    否则会把普通英文单词误判成许可证（"imitation" → MIT）。
    """
    head = text[:2000]
    lic = None
    for line in head.splitlines():
        m = LICENSE_LINE_RE.search(line)
        if not m:
            continue
        key = m.group(1).upper()
        if key not in LICENSE_UNAMBIGUOUS and not LICENSE_KW_RE.search(line):
            continue
        for needle, spdx in LICENSE_HINTS:
            if needle.upper() == key:
                lic = spdx
                break
        if lic:
            break
    m = re.search(r"@?[Aa]uthor\s*[:：]\s*([^\n*]{1,60})", head)
    if m:
        author = m.group(1).strip()
    else:
        # 片段常写成 "by @Someone" 或 "theme by @Someone"
        m = re.search(r"\bby\s+@([A-Za-z0-9_.\-]{2,40})", head)
        author = m.group(1) if m else None
    m2 = re.search(
        r"(https?://github\.com/[A-Za-z0-9_.\-]+/?[A-Za-z0-9_.\-]*)", head)
    return author, lic, (m2.group(1) if m2 else None)


def theme_index():
    with urllib.request.urlopen(OFFICIAL_THEMES, timeout=60) as r:
        d = json.load(r)
    return {t["name"].lower(): t for t in d if t.get("name")}


def resolve_ref(api, repo, version, local_sha, probe_path="theme.css"):
    """找出哪个 ref 的产物与本地文件逐字节一致。

    这一步是必需的：主题 manifest 里的 version 经常与它实际内容的来源对不上。
    实测 AnuPpuccin 的 manifest 写 1.5.0，但本地文件来自 main 分支，与
    v1.5.0 release 的产物内容不同 —— 直接按 version 下载会静默装回另一个东西。

    返回 (ref, kind)；都不匹配则返回 (None, None)，说明本地被改过，
    这种情况必须如实报出，而不是假装能还原。
    """
    cands = []
    try:
        cands.append((api.get("repos/%s/commits/main" % repo)["sha"], "main-head"))
    except Exception:
        pass
    for tag in ("v%s" % version, version):
        cands.append((tag, "tag"))
    for ref, kind in cands:
        b = fetch_raw(repo, ref, probe_path)
        if b is not None and sha256_bytes(b) == local_sha:
            return ref, kind
    return None, None


def scan_appearance(vault, api):
    cfg = os.path.join(vault, ".obsidian")
    out = {"theme": None, "snippets": []}

    themes_dir = os.path.join(cfg, "themes")
    if os.path.isdir(themes_dir):
        for name in sorted(os.listdir(themes_dir)):
            td = os.path.join(themes_dir, name)
            mf = os.path.join(td, "manifest.json")
            css = os.path.join(td, "theme.css")
            if not (os.path.isfile(mf) and os.path.isfile(css)):
                continue
            man = load_json(mf, {})
            entry = theme_index().get(name.lower())
            repo = entry.get("repo") if entry else None
            ver = man.get("version", "")
            rec = {
                "name": man.get("name", name),
                "version": ver,
                "author": man.get("author", ""),
                "authorUrl": man.get("authorUrl", ""),
                "repo": repo,
                "ref": None,
                "refKind": None,
                "files": {},
            }
            if repo and ver:
                rec["files"]["theme.css"] = sha256_file(css)
                ref, kind = resolve_ref(api, repo, ver, rec["files"]["theme.css"])
                rec["ref"], rec["refKind"] = ref, kind
                if ref:
                    print("  ✓ 主题 %s  仓库=%s  ref=%s (%s)"
                          % (name, repo, ref[:12], kind))
                    if kind == "main-head":
                        print("      ⚠️  manifest 声明版本 %s，但实际内容来自 main 分支；"
                              "按版本号下载会得到不同文件" % ver)
                else:
                    print("      ❌ 主题 %s 的本地内容与上游任何 ref 都不匹配，"
                          "可能被本地改过 —— 无法自动还原" % name, file=sys.stderr)
            out["theme"] = rec
            break

    sn_dir = os.path.join(cfg, "snippets")
    t = out["theme"]
    if os.path.isdir(sn_dir):
        for fn in sorted(os.listdir(sn_dir)):
            if not fn.endswith(".css"):
                continue
            p = os.path.join(sn_dir, fn)
            with open(p, encoding="utf-8", errors="replace") as f:
                text = f.read()
            author, lic, _ = sniff_license(text)
            out["snippets"].append({
                "file": fn,
                "bytes": os.path.getsize(p),
                "sha256": sha256_file(p),
                "declaredAuthor": author,
                "declaredLicense": lic,
                "sourceUrl": raw_url(t["repo"], t["ref"], "snippets/" + fn)
                if t and t.get("ref") else None,
            })
            print("  ✓ 片段 %-32s %-9s %s"
                  % (fn, lic or "未声明", author or ""))
    return out


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
