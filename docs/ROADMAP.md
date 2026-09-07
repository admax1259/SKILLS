# Roadmap / 仓库规划

## 0.1 — Distribution foundation

- [x] 收录并注明 show-me 来源与 MIT 授权。
- [x] Codex / Claude Code manifest 与 marketplace。
- [x] 中英文说明、本地安装入口、可重现 ZIP、校验和与 CI artifact 流程。
- [ ] 验证远程 PR CI artifact 下载与本机 Codex 插件安装。
- [ ] 在装有 Claude Code 的环境完成安装与行为验证。
- [ ] 合并后按版本流程发布第一个正式 Release。

## 0.2 — Engineering collection

逐项讨论 cursor-team-kit 的 18 个 skills，记录保留、修改、合并或暂缓。先从 check-compiler-errors 开始；不提前把未讨论项标成已迁移。

GitHub PR / GitLab MR 支持采用宿主工具选择与平台专用参考资料。覆盖自建 GitLab、嵌套 group、fork、分页、当前提交与 CI 状态，不靠命令名称替换宣称兼容。

## Later — Collection and promotion

- 建立按来源、场景、工具依赖和验证状态检索的目录。
- 增加 upstream 更新检查与差异评审；不自动覆盖本地适配。
- 收集实际案例、截图与演示，准备推广文案。
- 根据平台要求准备 ChatGPT / Claude 目录提交；打包完成不等于已获上架。
- 在有真实需求时扩展 Cursor 等引擎，并增加对应安装验证。
