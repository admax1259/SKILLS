# 发版 / Releases

源码仓库与可安装产物分开。源码不提交 plugins 副本或 marketplace 配置。

1. 版本 PR 更新 VERSION、CHANGELOG.md 与必要文档；插件版本由构建器派生，不手改多个 manifest。
2. 运行校验、目录检查、测试与打包。核对生成包仅含就绪 bundle。
3. 合并并收到发布指令后，在该 main 提交上创建 v<VERSION> tag 并推送。
4. CI 检查 tag/version、main ancestry，发布 dist/packages/ 中的 ZIP 与 SHA256SUMS；不覆盖旧版本。
5. 下载并核对校验和，解压安装验证。保留作为本地 marketplace 注册的解压目录。

PR artifacts 保留 30 天。正式 Release 资产是长期下载入口。GitHub 自动 Source code ZIP 是源码快照，需要构建，不等于预构建安装包。

- skills-<version>.zip: complete generated marketplace, with standalone Python installer.
- <bundle>-<version>.zip: native plugin at archive root for plugin-ZIP import surfaces.
- SHA256SUMS: checksums for those archives only.

Release versions are derived from VERSION. Publish only after the release change is merged and requested. Never upload the generated staging directory as a release asset.
