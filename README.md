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

## 这些技能能帮你做什么

来自 HumanLayer 的 **show-me** 负责可视化解释；来自 Cursor team kit 的 **18 项工程技能**覆盖验证、审查、代码质量、交付与复盘。它们均已适配，本仓库保留原始许可证、固定来源版本和修改记录。

下面的例句可以直接作为任务描述；实际执行需要宿主具备相应仓库、终端、浏览器或平台访问权限。

| 技能 | 分类 | 能力与边界 | 任务示例 |
|---|---|---|---|
| [show-me](skills/show-me/SKILL.md) | 可视化 | 把概念、目录和流程解释成 Mermaid、伪代码或交互 HTML；使用宿主可用的预览方式。 | 用图解释这个项目的技能如何打包安装。 |
| [check-compiler-errors](skills/check-compiler-errors/SKILL.md) | 验证 | 发现项目实际编译／类型检查命令，区分代码错误与环境阻塞；默认报告，要求时修复。 | 检查编译错误，先不要修改代码。 |
| [run-smoke-tests](skills/run-smoke-tests/SKILL.md) | 验证 | 运行项目已有冒烟测试，记录结果；按授权修复，缺少测试或环境时明确说明。 | 运行这个项目的冒烟测试并定位失败原因。 |
| [verify-this](skills/verify-this/SKILL.md) | 验证 | 把声明转成可测条件，用实际证据判断已验证、未验证或无法确定。 | 验证安装包是否包含全部技能与许可证。 |
| [control-cli](skills/control-cli/SKILL.md) | 验证 | 用可用终端工具复现 CLI/TUI 行为，记录退出状态并管理自己创建的会话。 | 复现这个 CLI 的交互卡住问题。 |
| [control-ui](skills/control-ui/SKILL.md) | 验证 | 使用已有浏览器／桌面自动化检查交互、页面状态和错误，保留用户会话。 | 检查这个页面的展开和收起是否正常。 |
| [get-pr-comments](skills/get-pr-comments/SKILL.md) | 代码审查 | 汇总 GitHub PR／GitLab MR 评论，保留讨论状态、位置和来源；默认只读。 | 整理这个 MR 还需要处理的审查意见。 |
| [make-pr-easy-to-review](skills/make-pr-easy-to-review/SKILL.md) | 代码审查 | 完善 PR/MR 描述与阅读顺序；保持行为，重写历史需要明确授权。 | 让这个 PR 更容易审阅，补充说明和验证结果。 |
| [pr-review-canvas](skills/pr-review-canvas/SKILL.md) | 代码审查 | 显式调用后生成本地交互 diff 导览；支持 GitHub/GitLab 采集，完整保留 import、空白变更及行号。 | 用 $pr-review-canvas 为这个 PR 生成可视化导览。 |
| [thermo-nuclear-code-quality-review](skills/thermo-nuclear-code-quality-review/SKILL.md) | 代码审查 | 显式调用的严格可维护性审查：关注抽象、耦合与复杂度；默认给建议，不自动全面重构。 | 用 $thermo-nuclear-code-quality-review 深入审查这个分支。 |
| [deslop](skills/deslop/SKILL.md) | 代码质量 | 清理当前 diff 的冗余，保持行为、必要注释和容错；没有合理改动时允许不修改。 | 清理这个 diff 的冗余，保持行为不变。 |
| [fix-merge-conflicts](skills/fix-merge-conflicts/SKILL.md) | 交付 | 按当前 merge/rebase/cherry-pick 处理冲突，结合双方意图与验证，保护无关修改。 | 解决当前 rebase 冲突，并运行相关检查。 |
| [fix-ci](skills/fix-ci/SKILL.md) | 交付 | 定位当前提交的失败检查和日志，做有限次数的针对性修复；支持 PR/MR 流程。 | 修复这个 PR 当前提交的 CI 失败。 |
| [loop-on-ci](skills/loop-on-ci/SKILL.md) | 交付 | 在限定时间内观察当前 PR/MR 检查；按授权修复，不把旧结果、空检查或手动步骤当成功。 | 观察这个 MR 的 CI，失败时按当前任务范围修复。 |
| [new-branch-and-pr](skills/new-branch-and-pr/SKILL.md) | 交付 | 保留工作区状态，完成任务、分批提交并创建 GitHub PR／GitLab MR；处理已有分支与 fork。 | 实现这个改动，并提交一个 PR。 |
| [review-and-ship](skills/review-and-ship/SKILL.md) | 交付 | 审查、验证并通过 PR/MR 交付当前改动；ship 默认不包含合并、发版或部署。 | 审查并验证这个分支，然后创建 PR。 |
| [what-did-i-get-done](skills/what-did-i-get-done/SKILL.md) | 知识复盘 | 按身份、时区和时间范围整理工作，区分提交、合并与部署，保留证据。 | 总结我这两天在这个仓库完成的工作。 |
| [weekly-review](skills/weekly-review/SKILL.md) | 知识复盘 | 按明确的一周整理成果、修复与技术债；基于可访问记录，不自动发布周报。 | 根据仓库记录整理我上一个完整自然周的周报。 |
| [workflow-from-chats](skills/workflow-from-chats/SKILL.md) | 知识复盘 | 从当前或授权可读的会话提炼流程和明确偏好；避免把一次意见变成永久规则。 | 把这次确认的仓库管理流程整理到项目约定里。 |

## 选择安装集合

| 集合 | 包含内容 | 适合谁 |
|---|---|---|
| `show-me` | 1 项可视化技能 | 希望用图理解问题 |
| `engineering-kit` | 全部 18 项工程技能 | 日常开发、PR/MR 交付与复盘；推荐与 show-me 一起安装 |
| `compiler-checks` | 仅 check-compiler-errors | 只需要编译／类型检查 |
| `code-cleanup` | 仅 deslop | 只需要保持行为的 diff 清理 |

安装 engineering-kit 后无需重复安装 compiler-checks、code-cleanup。Canvas 和严格质量审查保留显式调用策略；其余技能由宿主按任务匹配，也可明确点名使用。安装完成不等于已验证自动选择行为。

`ready` 表示可以进入安装包；跨引擎实测范围见[自举记录](docs/bootstrap.md)，逐项决策见[迁移评审](docs/migration-review.zh-CN.md)。以后收录的新技能只有审核就绪后才进入对应集合。

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

`--dry-run` 只预览，不写文件、不安装。安装器从就绪技能构建 `dist/marketplace/`，注册该目录后调用引擎原生安装命令。保留这个目录供后续使用。0.5.0 已合并到 main；安装后开启新会话加载技能。

**源码仓库不再直接作为原生 marketplace 注册。** 这是明确的分离：源码不保存生成的插件副本；原生 marketplace 位于生成目录或解压后的安装包。不要对源码根目录运行 `codex plugin marketplace add .` 或 `/plugin marketplace add admax1259/SKILLS`。Claude Code 可在对话中注册构建后的绝对路径，再安装 `show-me@admax-skills`。

Codex 用 `$show-me` 或 `$verify-this`；Claude Code 用 `/show-me:show-me` 或 `/engineering-kit:verify-this`。Canvas 与严格质量审查保留显式调用限制。只需要单个 skill 的用户也可以从 `skills/show-me/` 获取包含许可证的完整目录。

## 如何从 GitHub 下载并本地安装

当前提供 **Actions 构建包**，尚未发布正式 Release。推荐下载完整 marketplace 包，安装器会选择正确的引擎版本。

1. 登录 GitHub，打开仓库的 [Actions](https://github.com/admax1259/SKILLS/actions/workflows/ci.yml)。
2. 选择分支为 **main**、绿色成功的 **Validate and package** 运行；展开页面下方 **Artifacts**。
3. 下载 `skills-packages-<commit>`。本仓库 artifact 保留 **30 天**，过期后选择更新的成功构建。
4. 解压下载的外层 ZIP，可见 6 个安装 ZIP 和 `SHA256SUMS`。再解压其中的 `skills-0.5.0.zip`（新版本替换版本号）。
5. 将 `skills-0.5.0/` 放到长期保留的目录，进入该目录，运行：

```sh
python3 scripts/install.py --engine codex --bundle engineering-kit
python3 scripts/install.py --engine codex --bundle show-me
# 已装 Claude Code CLI 的用户改用：
python3 scripts/install.py --engine claude --bundle engineering-kit
python3 scripts/install.py --engine claude --bundle show-me
```

不要在已有同名 marketplace 时直接改用另一个目录；升级时复用已注册的稳定目录，或先通过引擎原生命令移除旧注册再注册新路径。不要删除仍被注册的解压目录。重开会话后，可试：`用 $verify-this 验证这个项目的安装包` 或 `用 $show-me 解释这个项目结构`。

[0.5.0 合并后构建](https://github.com/admax1259/SKILLS/actions/runs/34171173838) · [对应 artifact](https://github.com/admax1259/SKILLS/actions/runs/34171173838/artifacts/10035744753)。这份构建已下载核验：6 个 ZIP 的 SHA-256 全部匹配，Codex 的 engineering-kit 与 show-me 从下载包安装成功。固定 artifact 链接会随保留期过期，请届时使用上面的 Actions 入口。下载条件见 [GitHub 官方说明](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts)。

## 安装包与支持范围

```sh
python3 scripts/package.py
```

生成到 `dist/packages/current/`：

| 文件 | 用途 |
|---|---|
| `skills-<version>.zip` | 完整原生 marketplace；解压后执行同样的安装命令，无需 Git 或构建依赖 |
| `<bundle>-<version>.zip` | show-me、compiler-checks、code-cleanup 的双引擎插件 |
| `engineering-kit-<engine>-<version>.zip` | Codex／Claude 专用工程插件；引擎调用策略不同，构建时自动分开 |
| `SHA256SUMS` | ZIP 校验和 |

可从 [Actions artifacts](https://github.com/admax1259/SKILLS/actions) 下载；正式版本遵循[发版流程](docs/releases.md)。macOS 用 `shasum -a 256 -c SHA256SUMS` 校验，Linux 用 `sha256sum -c SHA256SUMS`。

- Codex：原生格式与安装流程已验证；新版本会重新检查。
- Claude Code：生成原生格式；当前开发机没有 Claude CLI，实际安装待验证。
- ChatGPT／其他 Claude 界面：提供插件 ZIP；界面导入能力、公共目录上架独立验证，未宣称已上架。
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
