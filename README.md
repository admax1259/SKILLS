# SKILLS

[English](README.en.md) · [Catalog](docs/CATALOG.md) · [Install](docs/INSTALL.md) · [Contributing](CONTRIBUTING.md)

个人 Agent Skills 收集器：保留作者与来源，适配工作流，统一分发。**44 个技能、8 个分类、3 个上游来源，一个完整插件。**

**[Download v0.7.0-beta.1](https://github.com/admax1259/SKILLS/releases/tag/v0.7.0-beta.1)** — `skills-0.7.0-beta.1.zip` + `SHA256SUMS`.

同一个 ZIP 包含 Codex 和 Claude Code 两种原生插件布局；全部技能一起安装，无需挑选小包。

## 安装

**Codex 应用内**：Plugins → Add plugin marketplace：

| Field | GitHub | Release 解压目录 |
|---|---|---|
| Source | `admax1259/SKILLS` | 解压后 `skills-0.7.0-beta.1` 的绝对路径 |
| Git ref | `v0.7.0-beta.1` | 留空 |
| Sparse paths | 留空 | 留空 |

添加来源后，打开 **Admax Skills** 卡片并点击 **Install**。Source 不能填 ZIP 或 Release 网页地址。

**Claude Code**：解压后执行 `/plugin marketplace add <解压目录绝对路径>`，再到 Discover 安装 Admax Skills。

也可在解压目录一键安装（Python 3.10+ 和对应 CLI）：

```sh
python3 scripts/install.py --engine codex
# or
python3 scripts/install.py --engine claude
```

[详细步骤、校验、旧版本升级与常见问题](docs/INSTALL.md)。安装后新建会话，Codex 可用 `$show-me`，Claude Code 可用 `/admax-skills:show-me`。

## 本次新增：Matt Pocock 的 25 个技能

### engineering

| Skill | 用途 |
|---|---|
| [ask-matt](skills/ask-matt/SKILL.md) | 流程导航与阶段衔接 |
| [code-review](skills/code-review/SKILL.md) | 按正确性和设计审查变更 |
| [codebase-design](skills/codebase-design/SKILL.md) | 设计深模块与清晰接口 |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | 复现并定位缺陷 |
| [domain-modeling](skills/domain-modeling/SKILL.md) | 领域术语、上下文与 ADR |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | 带文档记录的需求访谈 |
| [implement](skills/implement/SKILL.md) | 从规格或工单实施变更 |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | 发现架构改进机会 |
| [prototype](skills/prototype/SKILL.md) | 用原型验证设计问题 |
| [research](skills/research/SKILL.md) | 基于一手资料的研究 |
| [resolving-merge-conflicts](skills/resolving-merge-conflicts/SKILL.md) | 按双方意图解决冲突 |
| [setup-matt-pocock-skills](skills/setup-matt-pocock-skills/SKILL.md) | 配置跟踪器、标签与文档布局 |
| [tdd](skills/tdd/SKILL.md) | 围绕稳定接口进行 TDD |
| [to-spec](skills/to-spec/SKILL.md) | 将讨论整理为规格 |
| [to-tickets](skills/to-tickets/SKILL.md) | 将规格拆分为工单 |
| [triage](skills/triage/SKILL.md) | 分类工单并生成执行说明 |
| [wayfinder](skills/wayfinder/SKILL.md) | 绘制问题与决策地图 |
| [wizard](skills/wizard/SKILL.md) | 生成需要人工参与的配置向导 |

### productivity

| Skill | 用途 |
|---|---|
| [grill-me](skills/grill-me/SKILL.md) | 无状态的深入访谈 |
| [grilling](skills/grilling/SKILL.md) | 逐步澄清问题与决策 |
| [handoff](skills/handoff/SKILL.md) | 生成可移交的上下文文档 |
| [teach](skills/teach/SKILL.md) | 持续学习与学习记录 |
| [to-questionnaire](skills/to-questionnaire/SKILL.md) | 为他人准备问题清单 |
| [wait-what](skills/wait-what/SKILL.md) | 用易懂语言重新解释 |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | 编写供 Agent 使用的文档 |

建议从 `ask-matt` 了解流程；需求澄清用 `grill-with-docs`，然后按需要进入 `to-spec` → `to-tickets` → `implement`。这些是可组合工具，不要求每次走完全部步骤。

`fix-merge-conflicts` 保留原有交付流程，`resolving-merge-conflicts` 提供基于双方意图的简洁方法；按任务选择一个，不重复执行。

## 原有 19 个技能

| Category | Skills |
|---|---|
| visualization | [show-me](skills/show-me/SKILL.md) |
| verification | [check-compiler-errors](skills/check-compiler-errors/SKILL.md), [control-cli](skills/control-cli/SKILL.md), [control-ui](skills/control-ui/SKILL.md), [run-smoke-tests](skills/run-smoke-tests/SKILL.md), [verify-this](skills/verify-this/SKILL.md) |
| code-review | [get-pr-comments](skills/get-pr-comments/SKILL.md), [make-pr-easy-to-review](skills/make-pr-easy-to-review/SKILL.md), [pr-review-canvas](skills/pr-review-canvas/SKILL.md), [thermo-nuclear-code-quality-review](skills/thermo-nuclear-code-quality-review/SKILL.md) |
| code-quality | [deslop](skills/deslop/SKILL.md) |
| delivery | [fix-ci](skills/fix-ci/SKILL.md), [fix-merge-conflicts](skills/fix-merge-conflicts/SKILL.md), [loop-on-ci](skills/loop-on-ci/SKILL.md), [new-branch-and-pr](skills/new-branch-and-pr/SKILL.md), [review-and-ship](skills/review-and-ship/SKILL.md) |
| knowledge | [weekly-review](skills/weekly-review/SKILL.md), [what-did-i-get-done](skills/what-did-i-get-done/SKILL.md), [workflow-from-chats](skills/workflow-from-chats/SKILL.md) |

## 来源与适配

| Upstream | Count | License | Provenance |
|---|---:|---|---|
| [Cursor](https://github.com/cursor/plugins) | 18 | MIT | [cursor-team-kit](sources/cursor-team-kit.json) |
| [HumanLayer](https://github.com/humanlayer/skills) | 1 | MIT | [humanlayer](sources/humanlayer.json) |
| [Matt Pocock](https://github.com/mattpocock/skills) | 25 | MIT | [matt-pocock](sources/matt-pocock.json) |

保留每个技能的许可证、资源、固定上游 commit 和文件校验值。新增适配说明见[导入评审](docs/matt-pocock-import.md)。`ready` 表示可打包，不代表所有工作流和引擎均经过行为实测。GitHub/GitLab 操作需要可用且有权限的连接器或 CLI；向导模板内置的 CI secret helper 目前是 GitHub 专用。

## 仓库组织与维护

```text
skills/<id>/SKILL.md       # canonical source and adjacent resources
catalog.json              # categories, readiness, invocation policy
sources/*.json            # upstream revisions, licenses, adaptations
.agents/plugins/          # Codex source marketplace
.codex-plugin/            # Codex source manifest
scripts/                  # validation, packaging, installation
docs/                     # generated catalog and guides
dist/                     # generated releases; not committed
```

分类和作者放在元数据中，技能路径保持扁平稳定。新增技能经过审阅、适配、校验后进入唯一完整插件。Release 包另行生成 Codex 与 Claude Code 目录，避免两种清单混入同一插件。

```sh
python3 scripts/catalog.py
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

[Changelog](CHANGELOG.md) · [Architecture](docs/architecture.md) · [Validation history](docs/bootstrap.md)
