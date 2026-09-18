#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install.py —— 在一台新电脑（或新 vault）上，按 plugins.json 一键恢复插件。

优先用仓库里 bundles/ 的快照（离线、且版本一定与原来一致）；
快照缺失时才回退到从 GitHub Releases 下载。若快照自带 checksums.txt，
安装后会逐个校验 sha256，确保文件完整。

用法：
  python3 scripts/install.py --target <目标 vault 路径> [选项]

选项：
  --offline        只用本地 bundles/，绝不联网
  --force          目标已存在同名插件时也覆盖
  --with-config    一并恢复核心插件开关与外观设置（会先备份原有配置）
  --only a,b       只恢复指定插件
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

ASSETS = ["main.js", "manifest.json", "styles.css"]


def load(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def verify(bundle_dir):
    """返回 (ok, [问题描述])"""
    cs = os.path.join(bundle_dir, "checksums.txt")
    if not os.path.isfile(cs):
        return True, []
    bad = []
    with open(cs, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            want, name = line.split(None, 1)
            fp = os.path.join(bundle_dir, name)
            if not os.path.isfile(fp):
                bad.append("%s 缺失" % name)
            elif sha256(fp) != want:
                bad.append("%s 校验和不符" % name)
    return not bad, bad


def copy_from_bundle(bundle_dir, dest):
    got = []
    for a in ASSETS:
        src = os.path.join(bundle_dir, a)
        if os.path.isfile(src):
            os.makedirs(dest, exist_ok=True)
            shutil.copy2(src, os.path.join(dest, a))
            got.append(a)
    return got


def download(repo, tag, dest, offline):
    if offline:
        return []
    got = []
    os.makedirs(dest, exist_ok=True)
    for a in ASSETS:
        url = "https://github.com/%s/releases/download/%s/%s" % (repo, tag, a)
        p = subprocess.run(["curl", "-sSL", "--fail", "-m", "180",
                            "-o", os.path.join(dest, a), url],
                           capture_output=True, text=True)
        if p.returncode == 0:
            got.append(a)
        elif a != "styles.css":
            raise RuntimeError("%s 下载失败" % a)
    return got


def restore_appearance(cfg, data, offline):
    """恢复主题与 CSS 片段。

    这些资产【不在本仓库里】—— 它们是他人作品，公开仓库分发会引入
    copyleft 义务。所以这里按 plugins.json 记录的 commit 回上游下载，
    并用记录的 sha256 逐个校验：不校验就等于没还原，因为可能拿到别的版本。
    """
    a = data.get("appearance") or {}
    t = a.get("theme")
    problems = []

    if offline:
        print("\n→ 外观资产：--offline 下跳过（本仓库不含这些文件）")
        return ["主题/片段未恢复（离线模式无法从上游获取）"] if (
            t or a.get("snippets")) else []

    if t and t.get("ref"):
        dest = os.path.join(cfg, "themes", t["name"])
        os.makedirs(dest, exist_ok=True)
        print("\n→ 恢复主题 %s @ %s" % (t["name"], str(t["ref"])[:12]))
        for fn in ("theme.css", "manifest.json", "preview.png"):
            url = "https://raw.githubusercontent.com/%s/%s/%s" % (
                t["repo"], t["ref"], fn)
            tmp = os.path.join(dest, fn)
            p = subprocess.run(["curl", "-sSL", "--fail", "-m", "120",
                                "-o", tmp, url], capture_output=True, text=True)
            if p.returncode != 0:
                if fn == "preview.png":
                    continue
                problems.append("主题 %s 下载失败" % fn)
                print("   ❌ %s 下载失败" % fn)
                continue
            want = (t.get("files") or {}).get(fn)
            if want and sha256(tmp) != want:
                problems.append("主题 %s 校验和不符" % fn)
                print("   ⚠️  %s 校验和不符（上游可能已改动该 commit）" % fn)
            else:
                print("   ✓ %s%s" % (fn, "（已校验）" if want else ""))
    elif t:
        problems.append("主题 %s 在清单里没有可用 ref，无法恢复" % t.get("name"))

    sn = a.get("snippets") or []
    if sn:
        sdir = os.path.join(cfg, "snippets")
        os.makedirs(sdir, exist_ok=True)
        print("→ 恢复 %d 个 CSS 片段" % len(sn))
        for s in sn:
            if not s.get("sourceUrl"):
                problems.append("片段 %s 无来源" % s["file"])
                print("   ❌ %s 无来源，无法恢复" % s["file"])
                continue
            tmp = os.path.join(sdir, s["file"])
            p = subprocess.run(["curl", "-sSL", "--fail", "-m", "120",
                                "-o", tmp, s["sourceUrl"]],
                               capture_output=True, text=True)
            if p.returncode != 0:
                problems.append("片段 %s 下载失败" % s["file"])
                print("   ❌ %s 下载失败" % s["file"])
            elif sha256(tmp) != s["sha256"]:
                problems.append("片段 %s 校验和不符" % s["file"])
                print("   ⚠️  %s 校验和不符" % s["file"])
            else:
                print("   ✓ %s（已校验）" % s["file"])
    return problems


def check_dangling(cfg):
    """检查 appearance.json 引用的主题/片段是否真的存在。

    否则 Obsidian 只会静默回落到默认外观 —— 看起来"迁移成功"，
    实际外观全丢，这种失败最容易被忽略。
    """
    app = load(os.path.join(cfg, "appearance.json"), {}) or {}
    missing = []
    theme = app.get("cssTheme")
    if theme and not os.path.isdir(os.path.join(cfg, "themes", theme)):
        missing.append("主题 %s 不存在" % theme)
    for s in app.get("enabledCssSnippets") or []:
        if not os.path.isfile(os.path.join(cfg, "snippets", s + ".css")):
            missing.append("片段 %s.css 不存在" % s)
    if missing:
        print("\n⚠️  appearance.json 引用了不存在的资产，"
              "Obsidian 会静默回落默认外观：")
        for m in missing:
            print("   · %s" % m)
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="目标 vault 路径")
    ap.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--with-config", action="store_true")
    ap.add_argument("--with-appearance", action="store_true",
                    help="恢复主题与 CSS 片段（回上游下载并校验 sha256）")
    ap.add_argument("--only", default=None)
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    target = os.path.abspath(a.target)
    only = set(a.only.split(",")) if a.only else None

    data = load(os.path.join(root, "plugins.json"))
    if not data:
        print("错误：找不到 plugins.json", file=sys.stderr)
        return 2

    cfg = os.path.join(target, ".obsidian")
    if not os.path.isdir(cfg):
        print("错误：%s 不是 Obsidian vault（缺 .obsidian）" % target,
              file=sys.stderr)
        return 2

    print("目标 vault: %s\n清单: %d 个插件（生成于 %s）\n"
          % (target, data["pluginCount"], data["generatedAt"]))

    installed, served_local, served_net, skipped, failed = [], [], [], [], []

    for p in data["plugins"]:
        pid = p["id"]
        if only and pid not in only:
            continue
        dest = os.path.join(cfg, "plugins", pid)
        bundle_dir = os.path.join(root, p["bundle"]) if p.get("bundle") else None
        has_bundle = bool(bundle_dir and os.path.isdir(bundle_dir))

        if os.path.isdir(dest) and not a.force:
            print("⏭  %-26s 已存在，跳过（用 --force 覆盖）" % pid)
            skipped.append(pid)
            continue

        try:
            if has_bundle:
                ok, bad = verify(bundle_dir)
                if not ok:
                    print("❌ %-26s 快照校验失败: %s" % (pid, "; ".join(bad)))
                    failed.append(pid)
                    continue
                got = copy_from_bundle(bundle_dir, dest)
                served_local.append(pid)
            else:
                got = download(p["repo"], p["tag"], dest, a.offline)
                served_net.append(pid)
            print("✓  %-26s %-8s ← %s"
                  % (pid, p["version"],
                     "本地快照" if has_bundle else "GitHub Releases"))
            installed.append(pid)
        except Exception as e:
            print("❌ %-26s %s" % (pid, str(e)[:110]))
            failed.append(pid)

    # 写入 community-plugins.json（与目标 vault 原有清单合并，避免误删）
    cp = os.path.join(cfg, "community-plugins.json")
    existing = load(cp, []) or []
    merged = list(existing)
    for pid in installed:
        if pid not in merged:
            merged.append(pid)
    with open(cp, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    if a.with_config:
        print("\n→ 恢复配置快照")
        for fn in ("core-plugins.json", "appearance.json", "app.json"):
            src = os.path.join(root, "config", fn)
            if not os.path.isfile(src):
                continue
            dst = os.path.join(cfg, fn)
            if os.path.isfile(dst):
                shutil.copy2(dst, dst + ".bak")
            shutil.copy2(src, dst)
            print("   ✓ %s%s" % (fn, "（原文件已备份为 .bak）"
                                 if os.path.isfile(dst + ".bak") else ""))

    appearance_problems = []
    if a.with_appearance:
        appearance_problems = restore_appearance(cfg, data, a.offline)

    # 无论是否恢复外观，都检查一次引用是否悬空 —— 静默回落默认外观
    # 是最容易被忽略的迁移失败
    dangling = check_dangling(cfg)

    print("\n" + "=" * 58)
    print("完成：%d 个已安装（本地快照 %d / 联网下载 %d），"
          "跳过 %d，失败 %d"
          % (len(installed), len(served_local), len(served_net),
             len(skipped), len(failed)))
    if skipped:
        print("跳过的：%s" % ", ".join(skipped))
    if failed:
        print("失败的：%s" % ", ".join(failed))
    if appearance_problems:
        print("外观资产问题：")
        for m in appearance_problems:
            print("   · %s" % m)
    if dangling and not a.with_appearance:
        print("\n提示：加上 --with-appearance 可从上游恢复主题与 CSS 片段。")
    if installed:
        print("\n下一步：重启 Obsidian，进入 设置 → 第三方插件，"
              "关闭「受限模式」，插件即会按清单启用。")
    return 1 if (failed or appearance_problems) else 0


if __name__ == "__main__":
    sys.exit(main())
