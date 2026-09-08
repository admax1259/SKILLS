# SKILLS

[English](README.en.md) · [技能目录](docs/CATALOG.md) · [目录设计](docs/architecture.md) · [收录规范](CONTRIBUTING.md)

个人 Agent Skills 收集器：统一收录、保留来源、逐项适配，再打包给不同引擎。

**Beta 下载：[GitHub Releases](https://github.com/admax1259/SKILLS/releases)。** 选择标记为 Pre-release 的最新版本，在 Assets 下载安装 ZIP 与 `SHA256SUMS`，不要选择 GitHub 自动生成的 Source code ZIP。

- **Codex 全量安装**：下载 `admax-skills-codex-<version>.zip`，解压到固定目录，在该目录运行 `codex plugin marketplace add .`。重启应用，在 Plugins Directory 选择 Admax Skills 并点击安装。
- **Claude Code**：下载 `skills-<version>.zip`，进入解压目录，运行 `python3 scripts/install.py --engine claude --bundle engineering-kit`；再用 `--bundle show-me` 安装可视化技能。也可用 `/plugin marketplace add <解压目录绝对路径>`，再从 Discover 安装对应集合。
- **ChatGPT 添加要求**：[官方文档](https://developers.openai.com/plugins/deploy/connect-chatgpt)要求技能插件从本地 marketplace 安装。“添加 MCP 连接”需要服务器地址；本仓库没有 MCP 服务。ZIP 不是 MCP 地址，通用 ZIP 上传及公共目录上架尚未验证。

每次将新的 `VERSION` 合并到 main，Release 工作流会检查、打包并发布；`-beta.N` 自动标为预发布。详见[下载与发版](docs/releases.md)。

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

分类通过[索引](docs/CATALOG.md)导航，不通过多层目录移动技能。一个技能只维护一份源码，可以加入多个安装集合（bundle）。以后增加作者、分类或引擎，都不需要改变已有 skill 路径。

## 已收录内容

- [show-me](skills/show-me/SKILL.md)：可打包。来自 HumanLayer，已适配跨平台预览。
- [check-compiler-errors](skills/check-compiler-errors/SKILL.md)：已适配，默认检查并报告，明确要求时修复；独立安装集合为 `compiler-checks`。
- [deslop](skills/deslop/SKILL.md)：已适配，清理当前 diff 的冗余并保持行为；保留必要注释和错误处理，独立集合为 `code-cleanup`。
- **cursor-team-kit 全部 18 个 skills 已实际收录**，包含 PR canvas 的配套资源；按验证、审查、代码质量、交付、知识复盘分类。18 项工程技能已完成批量适配，可安装 `engineering-kit`；逐项决策见[迁移评审](docs/migration-review.zh-CN.md)。

`ready` 表示可以进入包，不代表每个引擎均已行为验证。包含待适配成员的 bundle 整体不生成，避免发布内容不完整的集合。通用第三方安装器可能不读取本仓库状态；使用下面的安装器可执行审核过滤。

## 安装

### 按 bundle 安装（Codex／Claude Code）

源码构建与安装需要 Python 3.10+ 和对应引擎 CLI；构建脚本只使用 Python 标准库。克隆后按需选择安装命令：

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --bundle show-me
# 工程集合：18 个技能，包含 compiler-checks 和 code-cleanup，不包含 show-me
python3 scripts/install.py --engine codex --bundle engineering-kit
# 也可只安装单项集合：
python3 scripts/install.py --engine codex --bundle compiler-checks
python3 scripts/install.py --engine codex --bundle code-cleanup
# Claude Code 使用生成的专用 marketplace：
python3 scripts/install.py --engine claude --bundle engineering-kit
```

上述命令是可选方案，不需要全部执行。`scripts/install.py` 默认 bundle 为 `show-me`，支持的引擎只有 `codex` 和 `claude`，没有 ChatGPT 安装命令。

追加 `--dry-run` 可校验并预览，不构建插件、不调用引擎安装命令，也不要求已安装引擎 CLI：

```sh
python3 scripts/install.py --engine codex --bundle engineering-kit --dry-run
```

源码安装器校验 catalog，只允许所有成员均为 `ready` 的 bundle，构建到 `dist/marketplace/` 后注册该绝对路径并调用引擎 CLI。保留生成目录，安装后开启新的引擎会话。

### 根目录单一插件（Codex 清单）

与上面的按 bundle 构建不同，仓库内的 [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) 仅声明一个插件 `admax-skills`；[.codex-plugin/plugin.json](.codex-plugin/plugin.json) 直接引用 `./skills/`。在包含这些清单的仓库根目录，可按该布局注册：

```sh
codex plugin marketplace add .
codex plugin add admax-skills@admax-skills
codex plugin marketplace list
codex plugin list
```

这条路径不运行 Python 构建器，也不会按 `catalog.json` 的审核状态过滤；它暴露整个 `skills/`，当前为 19 个技能。根插件测试要求 catalog 全部为 `ready`。需要审核过滤时使用按 bundle 安装或下面的生成包。

根 marketplace 名为 `admax-skills`，生成的集合 marketplace 名为 `admax-skills-bundles`，避免注册来源互相覆盖。对应插件分别为 `admax-skills@admax-skills` 和 `engineering-kit@admax-skills-bundles`。根目录没有 Claude marketplace 清单；Claude Code 请使用生成目录。旧集合注册升级请参阅[发版说明](docs/releases.md)。

若报 `marketplace root does not contain a supported manifest`，先确认当前分支与目录确实包含根清单；不要把旧版本源码目录或错误目录当作生成 marketplace。清单存在与 CLI 实际兼容是不同验证项。

### Codex 全量安装包

`scripts/package.py` 的 `build_codex_plugin()` 会从 catalog 选取全部 `ready` 技能，生成单一 OpenAI 格式插件 ZIP：

```sh
python3 scripts/package.py
```

输出为 `dist/packages/current/admax-skills-codex-<version>.zip`，其中 `<version>` 来自 `VERSION`。ZIP 根层包含 `.agents/plugins/marketplace.json`、`.codex-plugin/plugin.json`、`skills/`、`SOURCES.json` 和 README；技能许可证随包保留。插件清单复制自根清单，版本必须与 `VERSION` 一致。

代码和测试能证明打包结构与内容，不能证明当前 ChatGPT 界面支持仓库 URL 添加、ZIP 上传或已成功导入。仅在你的界面明确支持该格式时使用此 ZIP；不要将完整 marketplace ZIP 当作单一插件。宿主仍须提供终端、仓库或其他工作流所需工具，插件本身不提供这些连接能力。

### 调用策略

Codex 示例为 `$show-me`、`$verify-this`；Claude Code 的 bundle 示例为 `/show-me:show-me`、`/engineering-kit:verify-this`。

`pr-review-canvas` 与 `thermo-nuclear-code-quality-review` 在 catalog 中标为 `invocation: explicit`。校验器要求就绪的显式技能配置 `agents/openai.yaml` 的 `allow_implicit_invocation: false`；构建器给 Claude 副本添加 `disable-model-invocation: true`。这是元数据映射，不等于所有宿主的运行时调用行为均已验证。单独复制技能时保留完整目录与 LICENSE。

## 安装包与支持范围

```sh
python3 scripts/package.py
```

生成到 `dist/packages/current/`；重复构建会重建带有本工具所有权标记的输出目录，旧产物不会保留：

| 文件 | 用途 |
|---|---|
| `skills-<version>.zip` | 完整原生 marketplace；解压后执行同样的安装命令，无需 Git 或重新构建；仍需 Python 3.10+ 与对应 CLI |
| `admax-skills-codex-<version>.zip` | Codex 全量插件与本地 marketplace；包含全部 ready 技能，界面导入待验证 |
| `<bundle>-<version>.zip` | show-me、compiler-checks、code-cleanup 的双引擎插件 |
| `engineering-kit-<engine>-<version>.zip` | Codex／Claude 专用工程插件；引擎调用策略不同，构建时自动分开 |
| `SHA256SUMS` | ZIP 校验和 |

可从 [Actions artifacts](https://github.com/admax1259/SKILLS/actions) 下载；正式版本遵循[发版流程](docs/releases.md)。macOS 用 `shasum -a 256 -c SHA256SUMS` 校验，Linux 用 `sha256sum -c SHA256SUMS`。

- Codex：原生格式与安装流程已验证；新版本会重新检查。
- Claude Code：生成原生格式；当前开发机没有 Claude CLI，实际安装待验证。
- ChatGPT：已验证目标 ZIP 的结构与内容；仓库 URL 添加、界面导入、运行时行为和公共目录上架未由本仓库测试证明。
- GitHub／GitLab：工程指令覆盖 PR/MR、fork、当前提交 CI 与讨论状态；Canvas 提供双平台只读采集。GitHub 有本仓库实测；GitLab 采集使用 fixture 验证，真实 MR 写入尚未验证。

## 收录与维护

每个新技能：放入 `skills/<id>/` → 保留 LICENSE → 登记 source 与 catalog → 审阅与测试 → 标为 ready → 加入 bundle。见[收录规范](CONTRIBUTING.md)。

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
