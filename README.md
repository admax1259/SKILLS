# SKILLS

[English](README.en.md) · [技能目录](docs/CATALOG.md) · [目录设计](docs/architecture.md) · [收录规范](CONTRIBUTING.md)

个人 Agent Skills 收集器：统一收录、保留来源、逐项适配，再打包给不同引擎。

**19 个技能，6 个分类，2 个来源。19 个均已适配并可打包；实际验证范围见[自举记录](docs/bootstrap.md)。**

## 目录

```text
SKILLS/
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

需要 Python 3.10+ 与 Codex 或 Claude Code CLI。克隆后一条命令构建并安装：

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --bundle show-me
# 完整工程技能集合（已含 compiler-checks 和 code-cleanup 的技能，无需重复安装）：
python3 scripts/install.py --engine codex --bundle engineering-kit
# 也可以仅安装编译检查技能：
python3 scripts/install.py --engine codex --bundle compiler-checks
# 安装代码清理技能：
python3 scripts/install.py --engine codex --bundle code-cleanup
# Claude Code：
python3 scripts/install.py --engine claude --bundle engineering-kit
```

### ChatGPT

在 ChatGPT 的插件添加界面直接填写 `https://github.com/admax1259/SKILLS`。仓库根目录现在同时
提供 marketplace 清单与 `admax-skills` 插件清单，不需要先生成 ZIP。本地 Codex 也可以直接运行：

```sh
codex plugin marketplace add /Users/max/workspace/SKILLS
codex plugin add admax-skills@admax-skills
```

若曾看到 `marketplace root does not contain a supported manifest`，先 `git pull` 到包含根目录
`.agents/plugins/marketplace.json` 的版本，再重试以上命令。可用
`codex plugin marketplace list` 与 `codex plugin list` 确认 marketplace 和插件均已被发现。

若界面要求上传文件，也可以运行 `python3 scripts/package.py` 后上传
`dist/packages/current/admax-skills-chatgpt-<version>.zip`。ChatGPT 可以载入技能说明，但需要终端、
代码仓库或其他宿主工具的工作流，仍然只有在当前对话提供对应工具时才能运行。

`--dry-run` 只预览，不写文件、不安装。安装器从就绪技能构建 `dist/marketplace/`，注册该目录后调用引擎原生安装命令。保留这个目录供后续使用。0.5.0 合并前请使用本次 PR 分支或对应 CI artifact。

**源码仓库可以直接作为 OpenAI marketplace 注册。** 根清单直接引用规范的 `skills/`，没有维护插件副本；构建输出仍位于忽略的 `dist/`。Claude Code 的多 bundle marketplace 继续使用构建后的绝对路径。

Codex 用 `$show-me` 或 `$verify-this`；Claude Code 用 `/show-me:show-me` 或 `/engineering-kit:verify-this`。Canvas 与严格质量审查保留显式调用限制。只需要单个 skill 的用户也可以从 `skills/show-me/` 获取包含许可证的完整目录。

## 安装包与支持范围

```sh
python3 scripts/package.py
```

生成到 `dist/packages/current/`：

| 文件 | 用途 |
|---|---|
| `skills-<version>.zip` | 完整原生 marketplace；解压后执行同样的安装命令，无需 Git 或构建依赖 |
| `admax-skills-chatgpt-<version>.zip` | 可直接上传 ChatGPT 的根清单单一插件；包含全部已审核技能 |
| `<bundle>-<version>.zip` | show-me、compiler-checks、code-cleanup 的双引擎插件 |
| `engineering-kit-<engine>-<version>.zip` | Codex／Claude 专用工程插件；引擎调用策略不同，构建时自动分开 |
| `SHA256SUMS` | ZIP 校验和 |

可从 [Actions artifacts](https://github.com/admax1259/SKILLS/actions) 下载；正式版本遵循[发版流程](docs/releases.md)。macOS 用 `shasum -a 256 -c SHA256SUMS` 校验，Linux 用 `sha256sum -c SHA256SUMS`。

- Codex：原生格式与安装流程已验证；新版本会重新检查。
- Claude Code：生成原生格式；当前开发机没有 Claude CLI，实际安装待验证。
- ChatGPT：生成根清单单一插件供直接上传；公共目录上架仍需独立验证，未宣称已上架。
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
