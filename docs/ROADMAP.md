# Roadmap / 仓库规划

## 0.2 — Collection structure

- [x] 平铺 skills/<id>，收录 show-me 与 cursor-team-kit 共 19 项。
- [x] 分类、来源、状态与 bundle 的统一 catalog；中英文分类目录自动生成。
- [x] 插件目录与 ZIP 从源码生成，未审核 bundle 不发布。
- [x] 单一源码扩展、导入完整性、可重现打包和解压安装测试。
- [x] 结构 PR #2 已合并；CI 通过，artifact 已生成。
- [ ] Claude Code 实机安装与行为验证。
- [ ] 合并后按需发布正式版本。

## Engineering adaptation

18 项工程技能已完成适配，和 show-me 共 19 项可打包。使用本地分批提交、一次汇总 PR；自举证据见 [bootstrap.md](bootstrap.md)。已补 GitHub PR / GitLab MR 指令、分页采集、当前 SHA 检查、调用策略映射和完整 diff 展示。

- [ ] GitLab 真实 MR 写入、pipeline 与 discussions 端到端验证。
- [ ] Claude Code 安装与行为验证。
- [ ] 新会话自动技能选择的独立评估。
- [ ] 根据真实使用反馈继续改进，不把当前 ready 当作永久兼容认证。

## Growth and promotion

- 增加真实使用案例、截图与可核验兼容状态。
- 增加上游更新差异检查，保留本地适配，避免自动覆盖。
- 按用户场景扩充 bundle，不按作者重复存放技能。
- 准备平台目录提交资料与中英文推广文案；上架独立于打包。
