#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bundle.py —— 按 plugins.json，把每个插件的发布产物下载并快照进 bundles/。

为什么要把二进制也存进来：只存清单的话，新电脑仍必须联网去 GitHub Releases
拉取；一旦某个插件删库、改仓库、下架或被新版破坏兼容，你就再也装不回
原来那一版。把产物连同许可证一起快照下来，这份备份才真正抗时间。

顺带记录 sha256 校验和，恢复时可验证文件没被篡改或损坏。

同时处理许可证合规：
  · 每个插件都存一份 LICENSE 全文（MIT/MPL/GPL 都要求随分发保留）
  · GPL 系列额外存 source.tar.gz —— 强 copyleft 要求分发二进制时
    必须同时提供对应源码，只给链接是不够的

用法：
  python3 scripts/bundle.py [--root <仓库根目录>] [--only id1,id2]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

ASSETS = ["main.js", "manifest.json", "styles.css"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def curl(url, dest):
    """下载到 dest，返回 sha256。用 curl 以便正确处理重定向。"""
    p = subprocess.run(["curl", "-sSL", "--fail", "-m", "180", "-o", dest, url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("下载失败 %s : %s" % (url, p.stderr.strip()[:120]))
    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_license_text(repo, ref):
    """从 raw.githubusercontent 取许可证全文，拼出常见文件名。"""
    names = ["LICENSE", "LICENSE.md", "LICENSE.txt", "license", "COPYING",
             "COPYING.txt", "LICENSE-MIT"]
    for n in names:
        url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, ref, n)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kit"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return n, r.read().decode("utf-8", "replace")
        except Exception:
            continue
    return None, None


def bundle(root, only=None):
    pj = os.path.join(root, "plugins.json")
    data = load(pj)
    total, skipped = 0, 0

    for p in data["plugins"]:
        pid, ver, repo, tag = p["id"], p["version"], p["repo"], p["tag"]
        if only and pid not in only:
            continue
        if not (repo and tag):
            print("⏭  %s 无仓库/版本信息，跳过" % pid)
            skipped += 1
            continue

        d = os.path.join(root, "bundles", pid, ver)
        os.makedirs(d, exist_ok=True)
        print("→ %s %s  (%s)" % (pid, ver, repo))
        sums = {}

        for a in ASSETS:
            url = "https://github.com/%s/releases/download/%s/%s" % (repo, tag, a)
            try:
                sums[a] = curl(url, os.path.join(d, a))
                print("    ✓ %-14s %s" % (a, sums[a][:16]))
            except Exception as e:
                # styles.css 并非所有插件都提供，属正常情况
                if a == "styles.css":
                    print("    – styles.css 不存在（可接受）")
                else:
                    print("    ❌ %s 下载失败: %s" % (a, str(e)[:100]))
                    sums.pop(a, None)

        # 许可证全文
        name, text = fetch_license_text(repo, tag)
        if text:
            with open(os.path.join(d, "LICENSE"), "w", encoding="utf-8") as f:
                f.write(text)
            sums["LICENSE"] = hashlib.sha256(text.encode()).hexdigest()
            print("    ✓ LICENSE      (源文件: %s)" % name)
        else:
            print("    ⚠️  未能取到许可证全文，请手工核对！")

        # GPL 强 copyleft：必须提供对应源码
        if str((p.get("license") or {}).get("spdx", "")).startswith("GPL"):
            url = "https://github.com/%s/archive/refs/tags/%s.tar.gz" % (repo, tag)
            try:
                sums["source.tar.gz"] = curl(
                    url, os.path.join(d, "source.tar.gz"))
                print("    ✓ source.tar.gz（GPL 合规要求）")
            except Exception as e:
                print("    ❌ GPL 源码下载失败，该插件不应分发: %s" % str(e)[:90])

        with open(os.path.join(d, "checksums.txt"), "w", encoding="utf-8") as f:
            for k in sorted(sums):
                f.write("%s  %s\n" % (sums[k], k))
        total += 1

    print("\n✅ 已快照 %d 个插件到 bundles/%s"
          % (total, "" if not skipped else "（跳过 %d 个）" % skipped))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--only", default=None, help="逗号分隔的插件 id，只处理这些")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    return bundle(os.path.abspath(a.root), only)


if __name__ == "__main__":
    sys.exit(main())
