# 第三方插件归属声明 / Third-Party Notices

> 本文件由 `scripts/export.py` 自动生成，请勿手工编辑。

## 性质说明

本仓库是**个人 Obsidian 配置的迁移备份**，与下列任何插件作者、
以及 Obsidian 官方（Dynalist Inc.）**均无隶属或 endorsement 关系**。
所有插件的著作权归其各自作者所有，此处按各插件原有许可证原样分发。
`Obsidian` 是 Dynalist Inc. 的商标，仅用于说明用途。

## 插件出处与许可证

| 插件 ID | 名称 | 版本 | 作者 | 来源仓库 | 许可证 | 锁定 commit |
|---|---|---|---|---|---|---|
| `obsidian-git` | Git | `2.40.0` | Vinzent | [Vinzent03/obsidian-git](https://github.com/Vinzent03/obsidian-git) | [`MIT`](bundles/obsidian-git/2.40.0/LICENSE) | `a9d1c5925d98` |
| `obsidian-style-settings` | Style Settings | `1.0.9` | mgmeyers | [community-archive/obsidian-style-settings](https://github.com/community-archive/obsidian-style-settings) | [`GPL-3.0`](bundles/obsidian-style-settings/1.0.9/LICENSE) | `4ebec6ae0131` |
| `obsidian-icon-folder` | Iconize | `2.14.7` | Florian Woelki | [FlorianWoelki/obsidian-iconize](https://github.com/FlorianWoelki/obsidian-iconize) | [`MIT`](bundles/obsidian-icon-folder/2.14.7/LICENSE) | `1264d5800a02` |
| `editing-toolbar` | Editing Toolbar | `4.1.4` | Cuman | [PKM-er/obsidian-editing-toolbar](https://github.com/PKM-er/obsidian-editing-toolbar) | [`MPL-2.0`](bundles/editing-toolbar/4.1.4/LICENSE) | `2ce7d3db0d27` |
| `obsidian-banners` | Banners | `1.3.3` | Danny Hernandez | [noatpad/obsidian-banners](https://github.com/noatpad/obsidian-banners) | [`MIT`](bundles/obsidian-banners/1.3.3/LICENSE) | `b4601ca54814` |

对照关系：上表每一行对应 `bundles/<插件 ID>/<版本>/`，该目录内包含

- `main.js` / `manifest.json` / `styles.css` —— 插件作者发布的原始产物
- `LICENSE` —— 该作者仓库中该版本 tag 下的许可证**全文**
- `checksums.txt` —— 上述文件的 sha256，用于校验完整性

## 各许可证对应的分发义务

| 许可证 | 义务 | 本仓库如何履行 |
|---|---|---|
| MIT | 保留版权声明与许可证全文 | 每个 bundle 内附 `LICENSE` 全文 |
| MPL-2.0 | 保留许可证、说明源码可得 | `LICENSE` 全文 + 来源仓库链接 |
| GPL-3.0 | 强 copyleft：分发二进制**必须同时提供对应源码** | 额外附 `source.tar.gz` 源码归档 |

### 强 copyleft 插件的额外说明

以下插件使用 GPL 系列许可证，仅提供二进制而不提供源码**不合规**，
因此本仓库为它们一并保存了对应 tag 的完整源码归档：

- **Style Settings** `1.0.9` —— GPL-3.0；源码归档：`bundles/obsidian-style-settings/1.0.9/source.tar.gz`

## 主题与 CSS 片段：本仓库不包含，仅作指引

`config/appearance.json` 里引用的主题与 CSS 片段**不在本仓库中**。
它们同样是他人的作品（多方使用 GPL / AGPL 系列许可证），
但本仓库**没有分发它们的文件本体**，因此在这一点上不产生再分发义务；
清单里只记录了名称、作者、来源仓库、锁定的 commit 与 sha256 校验和，
由使用者在安装时**自行从上游获取**。

详见 [APPEARANCE.md](APPEARANCE.md)。

## 如果你要拿走这里的插件

请不要直接用本仓库的副本，而是回到**上游来源仓库**下载最新版，
这样才能拿到作者的安全修复。本仓库锁定旧版本，只为迁移还原之用。

## 权利人的移除请求

若你是某插件的作者，不希望自己的产物出现在本仓库，
请提 Issue，我会立即移除对应目录。
