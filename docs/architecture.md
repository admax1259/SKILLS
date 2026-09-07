# 目录设计 / Repository architecture

## 决策

采用平铺技能源码 + 分类索引 + 来源记录 + 生成式插件分发。技能身份由稳定 id 决定，不由作者、分类或引擎决定。

- skills/<id>/ 只放该技能的 SKILL.md、LICENSE 和运行所需资源。
- catalog.json 是分类、审核状态和 bundle 成员的唯一维护入口；docs/CATALOG.md 自动生成并由 CI 检查。
- sources/<source>.json 保存仓库 URL、固定 commit、授权和初始导入校验和；后续适配记录具体变更。来源不是技能分类。
- scripts/ 是仓库工具；技能专用脚本留在该技能内部。
- dist/ 是可删除、可重建的分发产物；插件宿主要求的 plugins/<bundle>/skills/<id>/ 只在这里出现。
- 所有 19 项源码可直接浏览；只有全体成员 ready 的 bundle 可以生成。收录不等于适配完成。

## 参考仓库与选择理由

实际读取仓库树与 marketplace 配置，未按 README 印象猜测：

| 仓库 | 观察到的组织方式 | 本仓库借鉴 |
|---|---|---|
| [Anthropic skills](https://github.com/anthropics/skills) | 顶层 skills/<name>；marketplace 用 skills 列表组织集合 | 平铺源码、集合与物理路径解耦 |
| [Vercel agent-skills](https://github.com/vercel-labs/agent-skills) | 顶层 skills/<name>，另有 scripts/packages | 技能源码和维护工具分开 |
| [HumanLayer skills](https://github.com/humanlayer/skills) | plugins/<plugin>/skills/<skill>，独立插件市场 | 保留其技能内容与来源；不照搬其作者目录作为收集主结构 |
| [OpenAI plugins](https://github.com/openai/plugins) | plugins/<plugin> 下组合 skills、工具、服务资源 | 学习目标插件打包契约，不让产物布局主导源码布局 |

旧 openai/skills 仓库已声明 deprecated 并指向 openai/plugins，不能把旧仓库当成最新安装契约。

## 取舍

生成式方案不在 Git 源码内维护原生 marketplace。用户需要运行一次构建安装命令，或下载已经构建的 ZIP；直接将 GitHub 源码 URL 注册为原生 marketplace 不再成立。README 和安装器明确支持这一流程。

这样避免三种问题：手工维护引擎副本造成漂移；用符号链接让插件缓存访问包外资源；为每个技能重复维护一套插件目录。dist 中存在的复制是可验证的构建结果，不是第二份源码。

## 扩展规则

- 不按上游作者加多层 skills 子目录；用 source 字段归档作者。
- 分类可变化，技能路径不随之变化。新分类先在 catalog 中声明。
- 名称冲突时，判断是否同一能力；不同能力用有含义的前缀，不盲目加 -2。
- 改分类只改 catalog；加引擎只改构建适配；加 bundle 只改成员列表。
- 废弃先标 deprecated，保留迁移说明；不在无说明的情况下让用户旧路径失效。
- 新资源类型按实际用途加入技能目录，避免空 references/scripts/assets 模板泛滥。

## 引擎策略适配

源码仍是单份 skills/<id>。普通 bundle 生成双 manifest；包含显式调用技能的 bundle 自动生成 plugins/<bundle>（Codex）与 claude-plugins/<bundle>（Claude），各 marketplace 指向对应产物。Codex 使用 agents/openai.yaml 调用策略，Claude 保留 disable-model-invocation 前言。复制只发生在 dist，无手工维护副本。

打包目录固定为 dist/packages/current，仅重建带所有权标记的输出；CI 与 Release 只上传这里的 ZIP 和校验和，避免旧产物混入。

## 当前结构验证

19 项已登记；21 个 Cursor 原始文件已记录导入 SHA-256（get-pr-comments 的结尾换行规范化单独说明），18 份 MIT 声明跟随技能。Cursor agents/rules 未作为跨引擎配置启用。测试覆盖：额外未登记技能、非法集合引用、待适配成员隔离、打包可重现、解压安装、新技能扩展和 dry-run 无副作用。
