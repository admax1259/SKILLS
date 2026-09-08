# 下载与发版 / Downloads and releases

## 下载 / Download

[应用内字段说明 / GUI fields](INSTALL.md) · [包结构核对 / Package audit](package-audit.md)

打开 [Releases](https://github.com/admax1259/SKILLS/releases)，选择最新 Pre-release，在 Assets 下载 ZIP 与 SHA256SUMS。无需 GitHub 登录即可下载公开 Release 资产。Actions artifacts 是限期保存的 CI 构建；Source code ZIP 是源码，不能替代安装包。

Open the latest Pre-release under Releases and download ZIP assets and SHA256SUMS. Public Release assets do not require signing in. Actions artifacts expire; GitHub Source code ZIPs require building.

| Asset | 安装 / Installation |
|---|---|
| skills-<version>.zip | 唯一完整包，包含全部已审核技能 / One complete package with all reviewed skills. Extract, enter skills-<version>, run `python3 scripts/install.py --engine codex` or `--engine claude`. |
| SHA256SUMS | 完整包校验和 / Checksum for the complete package. |

macOS：`LC_ALL=C shasum -a 256 -c SHA256SUMS`；Linux：`sha256sum -c SHA256SUMS`。解压目录注册后请保留。Keep the extracted marketplace at a permanent path while registered.

从 beta.2 起不再发布单独的 show-me、code-cleanup 或工程集合包。一个插件包含全部 19 个技能；同一个 ZIP 自动提供两个引擎各自的元数据。Since beta.2, individual skill/bundle downloads are retired. One plugin contains all 19 skills; the same ZIP provides both engine layouts.

## 自动发版 / Automated releases

1. 在版本 PR 同步更新 VERSION、根 .codex-plugin/plugin.json、CHANGELOG.md。支持 X.Y.Z 与 X.Y.Z-beta.N，数字不允许多余前导零。
2. 校验、索引、测试、打包通过后合并到 main。VERSION 的 main 更新会自动启动 Release；也支持手动运行和 v<VERSION> tag。
3. 工作流检查 main ancestry、tag/version（tag 触发时）、包校验和，再将 tag 指向本次构建的精确提交，创建 Release。Beta 标为 Pre-release，且不覆盖稳定版 Latest。
4. 同版本已存在时拒绝覆盖。失败构建可在不存在 Release 时重跑；已发布版本需要新版本 PR。下载发布资产并验证，不能把本地构建当作下载验证。

Update VERSION, the root plugin version, and CHANGELOG in a version PR. Merging VERSION into main builds and publishes a Release at that exact commit. Manual dispatch and matching version tags are also supported. Validation precedes publication; beta releases are marked prerelease and do not replace the stable Latest release. Existing releases are never overwritten: publish a new version for corrections.

## 注册来源迁移 / Marketplace source migration

完整插件与来源均名为 admax-skills。旧 show-me、engineering-kit、compiler-checks、code-cleanup 插件需要先通过引擎原生命令卸载，避免技能重复。旧 admax-skills-bundles 来源可以在确认属于本仓库后移除。

The complete plugin and marketplace are both admax-skills. Uninstall old individual plugins through the engine to prevent duplicate skills; remove the old admax-skills-bundles registration only after verifying its origin.

更换同名来源的注册路径时，先运行 marketplace list 确认来源，然后移除旧 admax-skills 注册，再注册新解压目录。Codex 命令示例：

```sh
codex plugin marketplace list
codex plugin marketplace remove admax-skills
codex plugin marketplace add /absolute/path/to/skills-version
```

When changing a source path, inspect the registered source and remove the old admax-skills registration before adding the new extracted directory. Preserve unrelated sources. 本仓库安装脚本不会自动删除已有来源。

## UI 支持边界 / UI support boundary

[OpenAI testing instructions](https://developers.openai.com/plugins/deploy/connect-chatgpt) distinguish local marketplace installation from optional MCP connections. This is a skills-only collection. No MCP URL is provided; generic ChatGPT ZIP upload and public catalog approval are not established. Desktop UI clicking and Claude runtime activation must be verified separately from archive/manifest checks.
