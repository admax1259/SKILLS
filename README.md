# SKILLS

[English](README.en.md) · [技能目录](docs/CATALOG.md) · [目录设计](docs/architecture.md) · [收录规范](CONTRIBUTING.md)

个人 Agent Skills 收集器：统一收录、保留来源、逐项适配，再打包给不同引擎。

**[下载完整 Beta 安装包](https://github.com/admax1259/SKILLS/releases)：一个 ZIP，全部 19 个技能，同时支持 Codex 和 Claude Code。** 在最新 Pre-release 的 Assets 下载 `skills-<version>.zip` 与 `SHA256SUMS`。不需要挑选单独的技能包。

**19 个技能，6 个分类，2 个来源。19 个均已适配并可打包；实际验证范围见[自举记录](docs/bootstrap.md)。**

## 目录

```text
SKILLS/
├── .agents/plugins/marketplace.json # 根目录单一插件的 marketplace 清单
├── .codex-plugin/plugin.json     # 直接引用 skills/ 的根插件清单
├── skills/                       # 唯一技能源码；每个技能一个稳定路径
│   ├── show-me/
│   │   ├── SKILL.md
│   │   └── LICENSE
│   ├── check-compiler-errors/
│   ├── control-cli/
│   ├── control-ui/
│   ├── pr-review-canvas/          # 自带 renderer.js、styles.css、template.html
│   └── …                         # 全部 19 项见技能目录
├── catalog.json                  # 分类、来源、审核状态与 bundle 成员
├── sources/                      # 上游 URL、固定 commit、授权、导入记录
│   ├── cursor-team-kit.json
│   └── humanlayer.json
├── scripts/                      # 校验、索引、构建、安装
├── tests/
├── docs/
└── dist/                         # 生成的插件与 ZIP；不提交、不手改
```

分类通过[索引](docs/CATALOG.md)导航，不通过多层目录移动技能。一个技能只维护一份源码，全部已审核技能统一进入完整插件。以后增加作者、分类或引擎，都不需要改变已有 skill 路径。

## 已收录内容

- [show-me](skills/show-me/SKILL.md)：可打包。来自 HumanLayer，已适配跨平台预览。
- [check-compiler-errors](skills/check-compiler-errors/SKILL.md)：已适配，默认检查并报告，明确要求时修复；包含在完整插件中。
- [deslop](skills/deslop/SKILL.md)：已适配，清理当前 diff 的冗余并保持行为；保留必要注释和错误处理，包含在完整插件中。
- **cursor-team-kit 全部 18 个 skills 已实际收录**，包含 PR canvas 的配套资源；按验证、审查、代码质量、交付、知识复盘分类。18 项工程技能已完成批量适配，随完整插件一起安装；逐项决策见[迁移评审](docs/migration-review.zh-CN.md)。

`ready` 表示可以进入包，不代表每个引擎均已行为验证。未适配技能不会进入发布包。通用第三方安装器可能不读取本仓库状态；使用下面的安装器可执行审核过滤。

## 安装全部技能

从 [GitHub Releases](https://github.com/admax1259/SKILLS/releases) 下载完整 ZIP，解压到固定目录并进入 `skills-<version>/`。需要 Python 3.10+ 和对应引擎 CLI。选择你使用的引擎，执行一条命令：

```sh
# Codex
python3 scripts/install.py --engine codex

# Claude Code
python3 scripts/install.py --engine claude
```

两条命令都安装同一个完整插件 `admax-skills`，包含 show-me 与全部 18 个工程技能。安装后开启新会话，保留解压目录。追加 `--dry-run` 可先预览。

**Codex 界面安装**：在解压目录运行 `codex plugin marketplace add .`，重启应用，在 Plugins Directory 的 Admax Skills 中点击 Install。**Claude Code 界面安装**：运行 `/plugin marketplace add <解压目录绝对路径>`，然后从 Discover 安装 Admax Skills。

如果已经注册过同名来源，先用 `codex plugin marketplace list` 或 Claude 对应命令确认它属于本仓库；更换路径前使用引擎原生命令移除旧的 `admax-skills` 来源，再注册新目录。保留其他来源。旧 show-me、engineering-kit 等独立插件应先卸载，避免重复激活。

### 从源码安装

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex
# Claude Code 改为 --engine claude
```

源码安装器校验 catalog，只收录 `ready` 技能，构建到固定 `dist/marketplace/` 再安装。分类与历史 bundle 记录用于管理，不再作为用户安装选项。

### 下载文件

| 文件 | 用途 |
|---|---|
| `skills-<version>.zip` | 唯一完整安装包，Codex 与 Claude Code 共用 |
| `SHA256SUMS` | 完整包的 SHA-256 校验和 |

macOS：`LC_ALL=C shasum -a 256 -c SHA256SUMS`；Linux：`sha256sum -c SHA256SUMS`。GitHub 自动生成的 Source code ZIP 是源码，不能替代安装包。每次新 VERSION 合并到 main 会自动打包发布；`-beta.N` 标为预发布。见[发版流程](docs/releases.md)。

### ChatGPT 与运行时支持

[OpenAI 官方测试文档](https://developers.openai.com/plugins/deploy/connect-chatgpt)将技能插件的本地 marketplace 安装与 MCP 连接分开。本项目没有 MCP 服务器地址，不应把 ZIP 或仓库链接填入 MCP URL。通用 ChatGPT ZIP 上传、公共目录上架和当前桌面 UI 点击安装尚未完成验证。

Codex 清单、包内容、可重现构建已验证；Claude Code 原生格式和显式调用策略有结构测试，当前开发机没有 Claude CLI，实际激活待验证。技能依赖宿主提供终端、仓库及 GitHub/GitLab 工具。

Codex 调用示例：`$show-me`、`$verify-this`；Claude Code：`/admax-skills:show-me`、`/admax-skills:verify-this`。PR canvas 与全面质量审查保持显式调用，构建器自动生成引擎专用策略，不需要用户选择不同包。

## 收录与维护

每个新技能：放入 `skills/<id>/` → 保留 LICENSE → 登记 source 与 catalog → 审阅与测试 → 标为 ready → 自动进入完整插件。见[收录规范](CONTRIBUTING.md)。

```sh
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

运行完整开发测试还需要 Node.js 22+（Canvas 渲染回归）；安装预打包插件不需要 Node.js。

CI 检查索引遗漏、重名、非法 bundle、未审核技能隔离、导入完整性和可重现打包。所有变动通过 PR 交付。

## 授权

仓库自有工具使用 [Apache-2.0](LICENSE)。收录技能保留各自许可证：Cursor 与 HumanLayer 的本批内容均为 MIT，完整声明位于每个技能目录。来源与修改见 [sources/](sources/)。本项目不是上游作者或引擎厂商的官方项目。
