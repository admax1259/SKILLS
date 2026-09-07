# Releases / 发版

PR 和分支 CI 提供临时 Actions artifacts；正式 Release 提供长期可下载资产。首次基础设施 PR 尚未合并前，main 安装方式不会包含新插件。

1. Open a release PR updating VERSION, both manifests, Claude catalog versions, and CHANGELOG.md. Run validation, tests, and package generation.
2. After that PR is merged and a release is requested, tag that exact main commit with v<VERSION> and push the tag. Do not tag an unreviewed development branch.
3. The release workflow checks version/tag agreement and main ancestry, builds ZIPs, and uploads them with SHA256SUMS to GitHub Releases. The workflow uses GitHub's generated release notes.
4. Download the release artifact and verify the checksum before installing. Keep the extracted marketplace directory while registered as a local source.
5. Never overwrite an existing version's assets; fix problems in a new release version.

Artifacts: skills-<version>.zip contains the complete installable marketplace and its installer; show-me-<version>.zip contains the plugin at the archive root for tools accepting plugin ZIPs. The latter is not a marketplace root. GitHub's automatic Source code ZIP is distinct from these tested packages.
