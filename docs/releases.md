# 下载与发版 / Downloads and releases

## 下载 / Download

打开 [Releases](https://github.com/admax1259/SKILLS/releases)，选择最新 Pre-release，在 Assets 下载 ZIP 与 SHA256SUMS。无需 GitHub 登录即可下载公开 Release 资产。Actions artifacts 是限期保存的 CI 构建；Source code ZIP 是源码，不能替代安装包。

Open the latest Pre-release under Releases and download ZIP assets and SHA256SUMS. Public Release assets do not require signing in. Actions artifacts expire; GitHub Source code ZIPs require building.

| Asset | 安装 / Installation |
|---|---|
| admax-skills-codex-<version>.zip | 全部 19 项 / All 19 skills. Extract, run `codex plugin marketplace add .` there, restart the app and install Admax Skills from Plugins Directory. CLI alternative: `codex plugin add admax-skills@admax-skills`. |
| skills-<version>.zip | Codex / Claude Code bundle marketplace. Extract, enter skills-<version>, run `python3 scripts/install.py --engine claude --bundle engineering-kit`, then repeat with `--bundle show-me`. Use `--engine codex` for Codex. Requires Python 3.10+ and the engine CLI. |
| engineering-kit-claude-<version>.zip | 18 项工程技能 / 18 engineering skills. Native Claude plugin for compatible import surfaces; Claude Code users should use the marketplace ZIP above. |
| engineering-kit-codex-<version>.zip | Native Codex engineering plugin; marketplace registration uses the complete marketplace ZIP above. |
| show-me / compiler-checks / code-cleanup ZIPs | Individual native plugins with both engine manifests. |
| SHA256SUMS | ZIP checksums. |

下载所有 ZIP 后，macOS 执行 `shasum -a 256 -c SHA256SUMS`；Linux 执行 `sha256sum -c SHA256SUMS`。只下载部分包时，检查对应校验行；其他文件缺失不代表已下载文件损坏。

After downloading all ZIPs, verify with those checksum commands. If downloading a subset, verify the matching entries only. Keep the extracted marketplace at a permanent path while registered. 解压目录注册后请保留。

## 自动发版 / Automated releases

1. 在版本 PR 同步更新 VERSION、根 .codex-plugin/plugin.json、CHANGELOG.md。支持 X.Y.Z 与 X.Y.Z-beta.N，数字不允许多余前导零。
2. 校验、索引、测试、打包通过后合并到 main。VERSION 的 main 更新会自动启动 Release；也支持手动运行和 v<VERSION> tag。
3. 工作流检查 main ancestry、tag/version（tag 触发时）、包校验和，再将 tag 指向本次构建的精确提交，创建 Release。Beta 标为 Pre-release，且不覆盖稳定版 Latest。
4. 同版本已存在时拒绝覆盖。失败构建可在不存在 Release 时重跑；已发布版本需要新版本 PR。下载发布资产并验证，不能把本地构建当作下载验证。

Update VERSION, the root plugin version, and CHANGELOG in a version PR. Merging VERSION into main builds and publishes a Release at that exact commit. Manual dispatch and matching version tags are also supported. Validation precedes publication; beta releases are marked prerelease and do not replace the stable Latest release. Existing releases are never overwritten: publish a new version for corrections.

## 注册来源迁移 / Marketplace identity migration

根全量来源仍为 admax-skills。0.6.0-beta.1 起，集合来源改为 admax-skills-bundles，防止安装集合时覆盖全量来源。旧集合用户先使用引擎原生命令卸载旧集合（如 engineering-kit@admax-skills），再注册新包并安装 engineering-kit@admax-skills-bundles。不要移除其他来源；检查 marketplace list 确认注册路径。

The all-skills source remains admax-skills. Generated bundles now use admax-skills-bundles. Uninstall old bundle identifiers such as engineering-kit@admax-skills through the engine before installing engineering-kit@admax-skills-bundles. Inspect registered paths and preserve unrelated sources.

## UI 支持边界 / UI support boundary

[OpenAI testing instructions](https://developers.openai.com/plugins/deploy/connect-chatgpt) distinguish local marketplace installation from optional MCP connections. This is a skills-only collection. No MCP URL is provided; generic ChatGPT ZIP upload and public catalog approval are not established. Desktop UI clicking and Claude runtime activation must be verified separately from archive/manifest checks.
