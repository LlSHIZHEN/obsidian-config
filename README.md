# Obsidian 插件迁移包

这是一个 **Obsidian 插件清单 + 离线快照仓库**。目的只有一个：

> 换电脑时，不用凭记忆一个个去社区插件市场里翻，直接按这份清单把插件
> **还原到完全相同的版本**。

## 它解决什么问题

只写一份"插件名字列表"是不够的，实测下来有三个坑：

1. **插件的 `manifest.json` 里没有源码仓库地址**，只有 `author` / `authorUrl`，
   而且作者信息会过时。比如 `obsidian-style-settings` 的仓库早已从
   `mgmeyers/` 迁到 `community-archive/` 下——光靠 manifest 里的信息，
   新电脑上根本找不到该去哪儿下载。
   → 本仓库改为查 Obsidian 官方插件索引（7700+ 条）来解析真实仓库。

2. **插件会删库、改名、或被新版破坏兼容**。只存清单的话，上游一消失，
   你就永远装不回原来那一版。
   → 本仓库把插件产物**离线快照**进 `bundles/`，并锁定到具体 commit。

3. **社区插件市场只能装"最新版"**，装不回旧版。
   → 快照 + 精确 tag，保证版本一致。

## 目录结构

```
plugins.json          机器可读清单：id → 仓库 → 锁定版本 → commit → 许可证 → sha256
PLUGINS.md            人类可读的插件表格（自动生成）
NOTICE.md             第三方归属声明与许可证义务（自动生成，public 仓库合规关键）
APPEARANCE.md         主题与 CSS 片段的来源、锁定 commit 与校验和（自动生成）
config/               核心插件开关、外观设置等配置快照
bundles/<id>/<ver>/   插件产物快照
    main.js           插件本体
    manifest.json     插件元数据
    styles.css        样式（部分插件没有，属正常）
    LICENSE           该作者该版本下的许可证全文
    checksums.txt     sha256 校验和
    source.tar.gz     仅 GPL 系列：强 copyleft 要求的对应源码
scripts/
    export.py         扫描一个 vault → 重新生成清单
    bundle.py         按清单下载并快照插件产物
    install.py        在新电脑上按清单恢复插件
```

## 迁移到新电脑

```bash
# 1. 装开发工具（提供 git；新电脑若没装过会弹窗引导）
xcode-select --install

# 2. 克隆本仓库
git clone https://github.com/LlSHIZHEN/obsidian-plugin-kit.git
cd obsidian-plugin-kit

# 3. 装 Obsidian，然后随便建一个空 vault，记下它的路径

# 4. 一键恢复插件（优先用仓库内快照，离线也能装）
python3 scripts/install.py --target "/path/to/你的新 vault" --with-config

# 5. 恢复主题与 CSS 片段（这一步需要联网：本仓库不含它们的文件本体）
python3 scripts/install.py --target "/path/to/你的新 vault" --with-appearance
```

参数说明：

| 参数 | 作用 |
|---|---|
| `--target` | 目标 vault 路径（必填） |
| `--offline` | 只用仓库内快照，绝不联网 |
| `--force` | 目标已存在同名插件时覆盖 |
| `--with-config` | 恢复核心插件开关与外观设置（原文件会备份成 `.bak`） |
| `--with-appearance` | 恢复主题与 CSS 片段（回上游下载并校验 sha256） |
| `--only a,b` | 只恢复指定插件 |

安装完成后 **重启 Obsidian**，进入 `设置 → 第三方插件`，关闭「受限模式」，
插件就会按 `community-plugins.json` 自动启用。

### 为什么主题和片段不在仓库里

插件产物我做了离线快照，但**主题和 CSS 片段故意不打包**：它们同样是他人作品，
而且多方使用 **AGPL-3.0 / GPL-3.0** 这类强 copyleft 许可证，在公开仓库里
分发会给你带来分发义务。所以这里只记录来源、锁定 commit 与 sha256，
安装时回上游取——**本仓库不分发它们，也就不产生再分发义务**。

代价是这一步必须联网，而且上游哪天删库就取不到了。详见 [APPEARANCE.md](APPEARANCE.md)。

> ⚠️ **主题的版本号不可信**。实测 `AnuPpuccin` 的 `manifest.json` 声明版本
> `1.5.0`，但它实际的 `theme.css` 来自 **main 分支**，与 `v1.5.0` release
> 的产物**内容不同**。所以 `export.py` 不会直接按版本号下载，而是逐个探测
> main HEAD、`v<版本>`、`<版本>` 哪个的产物与本地**逐字节一致**，锁定匹配的
> commit；都匹配不上就明确报错（说明你本地改过），而不是静默装回一个不一样的东西。

> ⚠️ 如果你要迁移的是**笔记本身**而不是插件，看另一个仓库
> `LlSHIZHEN/MYOBSIDIAN`（那是笔记，这是环境）。

## 更新这份清单

在**当前正在用的电脑**上，把最新插件状态重新导出并快照：

```bash
# 1. 重新扫描现有 vault，刷新清单（换成你实际的 vault 路径）
python3 scripts/export.py "$HOME/Desktop/AIEngineering/AIEngineering"

# 2. 把新插件的产物下载进 bundles/
python3 scripts/bundle.py

# 3. 提交
git add -A && git commit -m "chore: 更新插件清单" && git push
```

装完新插件后记得跑一遍，否则这份备份会逐渐偏离现实。

## 依赖

- `python3`（macOS 装 Command Line Tools 即有）
- `curl`（系统自带）
- `git`
- 可选：`gh`（GitHub CLI）。`export.py` 会优先用它调 GitHub API。
  未登录时走匿名接口，限额 **60 次/小时**，插件一多就会失败；
  已登录 `gh` 则是 5000 次/小时。

## 已知限制

- **仅覆盖桌面端**。iOS 上跑不了 git，Android 支持也很有限；
  手机端同步只能用 Obsidian Sync。
- 本仓库是**迁移备份，不是同步工具**。它不跟随你日常的插件开关变化，
  需要你手动跑 `export.py` 刷新。
- **快照锁定的是旧版本**。要拿安全修复，请回上游仓库重新下载。

## 版权

本仓库不包含任何 Obsidian 官方代码。所有插件的著作权归其各自作者所有，
按各插件原有许可证分发。**完整归属声明、来源与许可证义务见
[NOTICE.md](NOTICE.md)**，每个插件的许可证全文见
`bundles/<插件>/<版本>/LICENSE`。

如果你是某插件的作者且不希望它出现在这里，提 Issue 我会立即移除。
