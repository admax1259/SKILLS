# Skills 收集器：迁移评审与逐项讨论

日期：2026-09-03。状态：评审与讨论中；不是已完成的跨引擎兼容认证。

## 目标与来源

目标仓库：https://github.com/admax1259/SKILLS 。保留现有 Apache-2.0 LICENSE；收录的第三方内容分别保留其原许可证、作者和来源，不能统一改署为原创。

当前可见源是 `../plugins/cursor-team-kit`，18 个 skills、2 个 Cursor agents、2 个 rules。源仓库 HEAD：`93b00b89ef425a9c1bac0d0b317dfc49c930ac99`，插件版本 1.2.0，MIT，Copyright (c) 2026 Cursor。来源声明为 https://github.com/cursor/plugins ，本地 remote 为作者的 fork https://github.com/admax1259/plugins 。本次结构调整时源工作树干净；导入文件及校验和登记在 sources/cursor-team-kit.json。

迁移基线需比较现有工作副本与历史备份后确定，并记录本地修改，避免遗漏先前适配。

额外收录：HumanLayer [show-me](https://github.com/humanlayer/skills/tree/main/plugins/show-me/skills/show-me)，上游快照 `3c2629142c5d437428269b1b722b08c0b87f574d`，MIT，Copyright (c) 2026 HumanLayer。

## 兼容性判断方法

以下是内容审阅结论，不是运行验证结论。GPT 可以理解所有这些工作流；实际执行由宿主工具决定。分别记录：能被发现、能执行主要流程、已通过真实任务验证。不要仅凭 `SKILL.md` 存在就标为全兼容。

OpenAI 当前支持 skills-only 插件，ChatGPT 与 Codex 共享插件目录，但能力可以因宿主而异。普通无仓库访问的对话无法执行本地 git、编译器、PTY 或浏览器测试。

## 逐项评审

| # | Skill | 作用与 GPT 适配判断 | 迁移时要讨论或修改的地方 |
|---|---|---|---|
| 1 | check-compiler-errors | 高可移植；运行编译与类型检查，按文件归类错误 | 原版会自动修复，与“check”名称不完全一致；默认只检查还是直接修复？发现项目命令，不预设语言。 |
| 2 | deslop | 高可移植；清理当前 diff 中多余注释、类型逃逸及不一致风格 | 自动发现基线分支；不能把必要的容错或说明当成垃圾删除。 |
| 3 | fix-merge-conflicts | 高可移植；解决冲突、重建 lockfile、验证 | 区分 merge/rebase/cherry-pick；编译通过不等于冲突语义正确；保留原版不推送、不打 tag 的边界。 |
| 4 | run-smoke-tests | 需要本地测试环境；运行并排查冒烟测试 | `smoketest` 与 `smoketest-no-compile` 是示例而非通用命令；先发现项目实际套件。区分环境失败与产品失败。 |
| 5 | verify-this | 高可移植，但需要测量工具；用 baseline/treatment 验证声明 | 保留 VERIFIED / NOT VERIFIED / INCONCLUSIVE；没有有效基线不能假装已证明。关联的 control skills 缺失时使用已有工具。 |
| 6 | control-cli | 需要终端、PTY 或 tmux；CLI/TUI 复现与性能采集 | POSIX 示例不等于 Windows 支持；补异常退出清理、确定性等待、证据保存位置。 |
| 7 | control-ui | 需要浏览器或 Electron 自动化工具 | 使用宿主已有浏览器工具；无工具时说明限制。区分新建与附着浏览器的生命周期，避免关闭用户会话。 |
| 8 | get-pr-comments | 可适配；收集评论并排序行动项 | GitHub 需区分 discussion、inline comments 与 review 状态；GitLab 需读取 notes/discussions、分页及 resolved 状态。只读取不自动发评论。 |
| 9 | fix-ci | 可适配；定位 CI 根因并修复 | 原版绑定 `gh pr checks` 且默认 push；补 GitLab MR pipeline/jobs、当前提交校验、重试上限及外部 CI 处理。 |
| 10 | loop-on-ci | 可适配；持续观察并修复 CI | 与 fix-ci 分工：一个修根因，一个管理观察循环；不能把空 checks、旧 SHA 或 skipped 当成 green。跨回合监控依赖宿主调度能力。 |
| 11 | new-branch-and-pr | 可适配；建分支、完成工作、提交 PR/MR | 不能写死 main；处理 fork、remote、已有脏工作树及目标分支。保留用户已指定的起点。 |
| 12 | review-and-ship | 可适配；审查、验证、提交、推送、开 PR/MR | 明确 ship 默认到创建/更新 PR/MR，原版没有自动 merge/deploy；子代理可用时再委派，缺失时串行审查。 |
| 13 | make-pr-easy-to-review | 可适配；整理描述与审阅路径，按需整理历史 | GitHub/GitLab 元数据适配；重写历史仅在用户要求范围内；保留 tree identity 验证，避免覆盖他人的远端更新。 |
| 14 | pr-review-canvas | 可适配；生成可交互的 diff 导览 | 保留 renderer.js、styles.css、template.html；GitLab diff 需转换为统一结构；处理分页、截断与二进制，保留防 `</script>` 注入逻辑；替换固定预览端口与宿主假设。 |
| 15 | thermo-nuclear-code-quality-review | 可适配；严格审查抽象、边界、分支复杂度 | 原版很长、规则重复，且把 1000 行门槛视为强阻断；要讨论是否保留这一主观门槛。默认审查不应隐含全面重构；映射显式调用元数据。 |
| 16 | what-did-i-get-done | 高可移植；按时间范围汇总本人提交 | 明确时区、分支与作者别名；提交不等于合并/部署，不把所有 commit 都称为 shipped。 |
| 17 | weekly-review | 高可移植；周度汇总与 bugfix/tech-debt/net-new 分类 | 与上一项重叠；可保留周报入口共享采集规则。缺 git email 时可使用用户提供的作者身份，不强迫更改 git config。 |
| 18 | workflow-from-chats | 工作流可移植，数据源需适配 | 原版指定 Cursor chats；使用用户提供或宿主授权可读的会话；一次性意见不变永久规则；不能直接把私聊写进公开收集仓库。 |
| 19 | show-me | 高可移植；按需选择伪代码、树、Mermaid、diff、HTML | 将 `Bash(open ...)` 替换为宿主预览与跨平台回退；保留“小而清晰”的原则，不强制所有解释都生成网页。 |

## 已采用的收集与分发结构

以 skills/<id>/ 为唯一源码，19 项均已收录。catalog.json 管理分类、来源、状态和集合；sources/ 保留固定上游版本、许可证与修改记录。插件清单与缓存所需层级在 dist/ 中生成。show-me 可打包；18 个工程技能保留原始行为、待逐项适配，默认安装包不包含它们。参见 [目录设计](architecture.md) 与 [全部技能索引](CATALOG.md)。

GitHub 与 GitLab 是两层支持：一是收集仓库可从任意 Git URL 安装；二是工作流能操作 GitHub PR 与 GitLab MR。自建 GitLab、嵌套 group、fork、分页、当前 SHA 与外部 CI 都需要覆盖，不能只把 `gh` 替换成 `glab`。

## 讨论进度

- 已收录 show-me，保留完整 MIT 声明、固定来源版本与修改说明。Codex manifest 通过官方本地校验器，已通过原生 CLI 安装到版本化插件缓存；新会话行为验证尚未完成。
- 已确定：提供 Codex / ChatGPT 格式与 Claude Code 格式；其他界面的导入和公开目录上架独立验证。
- 当前第 1 项：check-compiler-errors 默认仅检查，还是自动修复。
- 已提供中英文 README、安装器及 CI 打包流程；后续逐项确认工程 skills 行为后迁移。正式 Release 尚未发布。

## 核实资料

- [OpenAI 插件架构](https://developers.openai.com/plugins/concepts/plugins)
- [OpenAI Skills & Plugins](https://developers.openai.com/codex/skills-and-plugins)
- [Claude Code 插件](https://code.claude.com/docs/en/plugins)
- [HumanLayer show-me 源码快照](https://github.com/humanlayer/skills/blob/3c2629142c5d437428269b1b722b08c0b87f574d/plugins/show-me/skills/show-me/SKILL.md)

以上资料于 2026-09-03 读取。运行和目录上架状态以 README 与 PR 验证记录为准。
