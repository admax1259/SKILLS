# 发版 / Releases

源码仓库与可安装产物分开。源码不提交 plugins 副本或 marketplace 配置。

1. 版本 PR 更新 VERSION、CHANGELOG.md 与必要文档；插件版本由构建器派生，不手改多个 manifest。
2. 运行校验、目录检查、测试与打包。核对生成包仅含就绪 bundle。
3. 合并并收到发布指令后，在该 main 提交上创建 v<VERSION> tag 并推送。
4. CI 检查 tag/version、main ancestry，发布 dist/packages/current/ 中的 ZIP 与 SHA256SUMS；不覆盖旧版本。
5. 下载并核对校验和，解压安装验证。保留作为本地 marketplace 注册的解压目录。

PR artifacts 保留 30 天。正式 Release 资产是长期下载入口。GitHub 自动 Source code ZIP 是源码快照，需要构建，不等于预构建安装包。

- skills-<version>.zip: complete generated marketplace, with standalone Python installer.
- <bundle>-<version>.zip: native plugin at archive root for plugin-ZIP import surfaces.
- SHA256SUMS: checksums for those archives only.

Release versions are derived from VERSION. Publish only after the release change is merged and requested. Never upload the generated staging directory as a release asset.

本地源码安装使用固定 dist/marketplace/，版本写入插件 manifest。已有 0.2 安装如果注册了 dist/marketplace-0.2.0，先确认该来源属于本仓库，再用引擎原生命令移除旧 marketplace 注册并重新运行安装器；不要删除其他来源。下载 ZIP 的用户也应在稳定解压目录管理升级。

Source installs now use a stable dist/marketplace/ directory. For a prior 0.2 registration pointing to dist/marketplace-0.2.0, verify its origin, remove that old marketplace registration using the engine's native command, then rerun the installer. Do not remove unrelated sources. Use a stable extracted directory for ZIP-based upgrades as well.
