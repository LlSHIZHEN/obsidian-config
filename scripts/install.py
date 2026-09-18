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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="目标 vault 路径")
    ap.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--with-config", action="store_true")
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

    print("\n" + "=" * 58)
    print("完成：%d 个已安装（本地快照 %d / 联网下载 %d），"
          "跳过 %d，失败 %d"
          % (len(installed), len(served_local), len(served_net),
             len(skipped), len(failed)))
    if skipped:
        print("跳过的：%s" % ", ".join(skipped))
    if failed:
        print("失败的：%s" % ", ".join(failed))
    if installed:
        print("\n下一步：重启 Obsidian，进入 设置 → 第三方插件，"
              "关闭「受限模式」，插件即会按清单启用。")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
