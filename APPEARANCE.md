# 主题与 CSS 片段

> 本文件由 `scripts/export.py` 自动生成，请勿手工编辑。

本仓库**不包含**主题与 CSS 片段的文件本体。它们多为 GPL / AGPL 作品，
在公开仓库里分发会引入 copyleft 分发义务，因此这里只记录**来源、
锁定 commit 与 sha256 校验和**，由 `install.py --with-appearance` 
在安装时回上游下载并逐个校验。

## 主题

| 名称 | 作者 | manifest 声明版本 | 来源仓库 | 锁定 ref | ref 类型 |
|---|---|---|---|---|---|
| AnuPpuccin | [Anubis](https://github.com/AnubisNekhet) | `1.5.0` | [anubisnekhet/AnuPpuccin](https://github.com/anubisnekhet/AnuPpuccin) | `82d207c646904e7af371ced499f682fbdfad1012` | main-head |

> ⚠️ **版本号不可信**：该主题 `manifest.json` 声明版本为 `1.5.0`，但其实际内容与 `main` 分支一致，与该版本 tag 的发布产物**内容不同**。因此这里锁定的是 commit 而非版本号 —— 按版本号下载会装回另一个文件。

## CSS 片段

| 文件 | 大小 | 来源类型 | 注释中声明的作者 | 注释中声明的许可证 | 获取方式 |
|---|---|---|---|---|---|
| `custom-background.css` | 5588 B | 上游主题仓库 | AnubisNekhet | `AGPL-3.0` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/custom-background.css) |
| `custom-rainbow-colors.css` | 322227 B | 上游主题仓库 | AnubisNekhet | `AGPL-3.0` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/custom-rainbow-colors.css) |
| `extended-colorschemes.css` | 42015 B | 上游主题仓库 | 未声明 | `未声明` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/extended-colorschemes.css) |
| `floating-search-bar.css` | 1770 B | 上游主题仓库 | AnubisNekhet | `AGPL-3.0` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/floating-search-bar.css) |
| `floating-status-bar.css` | 743 B | 上游主题仓库 | AnubisNekhet | `AGPL-3.0` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/floating-status-bar.css) |
| `its-frontmatter.css` | 2554 B | 上游主题仓库 | SlRvb | `未声明` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/its-frontmatter.css) |
| `minimal-cards.css` | 9169 B | 上游主题仓库 | @kepano | `MIT` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/minimal-cards.css) |
| `notion-cards.css` | 9341 B | 上游主题仓库 | AnubisNekhet | `AGPL-3.0` | [上游](https://raw.githubusercontent.com/anubisnekhet/AnuPpuccin/82d207c646904e7af371ced499f682fbdfad1012/snippets/notion-cards.css) |
| `text-contrast-fix.css` | 506 B | **本地原创** | 未声明 | `未声明` | 本仓库内 `local/snippets/text-contrast-fix.css` |

来源类型由脚本逐个回上游比对 sha256 判定，**不是按文件名猜的**：
与上游主题仓库同路径文件逐字节一致 → 上游；否则 → 本地原创。

### 本地原创的片段

以下片段在你本地编写、上游并不存在，因此**无法从上游下载**，
已随本仓库打包（它们是**你自己的作品**，不涉及第三方许可）：

- `text-contrast-fix.css` —— 存放于 `local/snippets/text-contrast-fix.css`

> ⚠️ 若脚本错误的把这类片段当作上游文件，结果会是：公开仓库里把你的
原创作品错标成他人作品，且新电脑恢复时 404、**你的自定义静默丢失**。
这正是加入逐文件 sha256 比对的原因。

### 上游片段

其余片段与上游主题仓库逐字节一致，因此**不随本仓库分发**
（多为 GPL/AGPL 作品，公开仓库分发会引入 copyleft 义务），
由安装脚本按锁定 commit 回上游下载并校验。

### 许可证不一致的提示

上游片段里有部分文件的注释声明为 **AGPL-3.0**，而该仓库自身的
LICENSE 文件是 **GPL-3.0**。两者不一致时，本清单按文件注释里
声明的、更严格的许可证记录。若你要另行使用这些文件，
请自行向上游作者确认。

## 校验方式

`plugins.json` 的 `appearance` 段里为每个文件记录了 `sha256`。
安装脚本下载后会比对；不一致就报错退出，避免静默装出一个外观不对的 vault。
