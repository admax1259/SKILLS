# 安装完整插件 / Install the complete plugin

一个 ZIP、一个插件、全部已审核技能。Codex 与 Claude Code 共用同一个下载包。
One ZIP, one plugin, all reviewed skills; the download supports both engines.

## Codex：你截图中的 Add plugin marketplace 窗口

打开 Plugins → 添加 marketplace。在下面两种来源中选择一种填写。
Open Plugins → Add plugin marketplace. Choose one source below.

| 字段 / Field | GitHub 安装 / GitHub | Release 离线包 / Extracted Release |
|---|---|---|
| Source | `admax1259/SKILLS` | 解压后 `skills-<version>` 文件夹的绝对路径 / Absolute path to the extracted `skills-<version>` folder |
| Git ref | `distribution`（跟随已发布版本 / follow published versions） | 留空 / Leave empty |
| Sparse paths | 留空 / Leave empty | 留空 / Leave empty |

点击 **Add marketplace**，选择 **Admax Skills** 来源，打开同名插件卡片，再点击 **Install**。注册来源和安装插件是两个步骤。界面未刷新时，退出并重启应用，然后新建会话。

Click **Add marketplace**, select the **Admax Skills** source, open its plugin card, then click **Install**. Registering the source and installing the plugin are separate steps. Restart the app if the directory has not refreshed; test in a new conversation.

Source 不接受 ZIP 文件路径、Release 网页地址或 ZIP 下载地址。离线包必须先解压，选含 `.agents/plugins/marketplace.json` 的外层目录，不是 `plugins/admax-skills` 子目录。Finder 默认隐藏点开头的目录，按 ⌘⇧. 可显示。

Source is a repository or local marketplace directory, not a ZIP or Release URL. Extract first and select the outer folder containing `.agents/plugins/marketplace.json`, not the inner plugin directory. Finder hides dot-directories; press Command-Shift-period to reveal them.

Sparse paths 的 `plugins/codex` 是窗口示例占位文字，不是本仓库路径；不要填入。GitHub 的 distribution 分支与 Release ZIP 使用同一份构建结果，两者都提供一个完整插件。main 是维护源码的分支；建议安装 distribution。

The `plugins/codex` placeholder is not a path in this repository. Leave Sparse paths blank. The distribution branch and Release ZIP use the same generated payload. Both expose one complete plugin. main is the source branch; use distribution for installation.

## 命令行 / Command line

在解压目录执行以下之一，需要 Python 3.10+ 与对应引擎 CLI：
From the extracted directory, choose one command (Python 3.10+ and the engine CLI required):

```sh
python3 scripts/install.py --engine codex
python3 scripts/install.py --engine claude
```

仅注册 Codex 来源、保留界面点击安装：`codex plugin marketplace add .`。
To register only and finish installation in the UI: `codex plugin marketplace add .`.

Claude Code 界面：`/plugin marketplace add <解压目录绝对路径>`，然后 Discover → Admax Skills → Install。
Claude Code UI: `/plugin marketplace add <absolute-extracted-directory>`, then Discover → Admax Skills → Install.

## 在线安装与升级 / Online installation and updates

在源码仓库或新版 ZIP 解压目录执行；二选一：
Run from the source checkout or a current extracted ZIP; choose your engine:

```sh
python3 scripts/install.py --engine codex --source github
python3 scripts/install.py --engine claude --source github
```

它们注册 GitHub 的 `distribution` 分支并安装完整插件。该分支只在 Release 成功后更新，包含独立的 Codex 和 Claude 布局。以后升级：
These commands register the GitHub distribution branch and install the complete plugin. The branch advances after successful Releases and includes isolated native layouts. To update later:

```sh
python3 scripts/install.py --engine codex --source github --update
python3 scripts/install.py --engine claude --source github --update
```

升级前确认 admax-skills 已注册为 distribution 来源；`--update` 刷新当前注册来源，不会自动把本地目录或固定 tag 切换成在线分支。加 `--dry-run` 可预览命令。
Before updating, confirm admax-skills is registered from distribution. --update refreshes the existing source; it does not replace a local folder or fixed tag with an online branch. Add --dry-run to preview commands.

不使用 Python 也可安装：
Native installation without Python:

```sh
codex plugin marketplace add https://github.com/admax1259/SKILLS.git --ref distribution
codex plugin add admax-skills@admax-skills
# Claude Code
claude plugin marketplace add 'https://github.com/admax1259/SKILLS.git#distribution'
claude plugin install admax-skills@admax-skills
```

**自动更新的边界 / Auto-update behavior**

- Claude Code：`/plugin` → Marketplaces → admax-skills → Enable auto-update。第三方来源需要主动开启。手动刷新用 `claude plugin marketplace update admax-skills`，然后 `claude plugin update admax-skills@admax-skills`。
- Codex：已验证 Git marketplace 刷新及插件重新安装入口；个人桌面端是否后台自动更新取决于宿主，不能仅凭仓库配置承诺。可运行 `codex plugin marketplace upgrade admax-skills`，再运行 `codex plugin add admax-skills@admax-skills`。
- ChatGPT 管理员导入的工作区 marketplace 有每日同步功能；它与个人桌面注册是不同入口。

Claude Code supports opt-in marketplace auto-updates. Personal Codex background behavior is host-dependent; the commands above explicitly refresh and install the current snapshot. Admin-managed ChatGPT workspaces have a separate daily-sync feature. Restart/start a new conversation after updating if the host requests it.

## 离线升级和回退 / Offline upgrade and rollback

下载指定 Release 的 ZIP 与 SHA256SUMS，校验、解压到固定保存的位置，然后从该目录运行原来的 `--source local` 安装（也是默认值）。切换旧来源按下一节操作。回退同理，选旧 Release 并重新注册、安装。ZIP 不会自动下载新版本；不要将 Git 自动更新开启在需要固定版本的安装上。

Download a chosen Release ZIP and SHA256SUMS, verify, extract to a permanent location, and run the installer with --source local (the default). Switch sources as described below. Roll back by selecting an older Release and registering/installing that snapshot. Offline ZIPs do not fetch updates.

两种分发方式同时维护，但同一引擎的同名 marketplace 一次注册一个来源。不会重复安装两套同名技能。
Both delivery methods are maintained; each engine registers one source for the same marketplace identity at a time.

## 已注册旧来源 / Existing source

若提示同名来源已从其他路径添加，先检查 `codex plugin marketplace list`。确认旧 `admax-skills` 属于本仓库后，用 `codex plugin marketplace remove admax-skills` 移除旧注册，再添加新来源。不要删除其他来源。Claude Code 可先用 `claude plugin marketplace list` 查看，再用 `claude plugin marketplace remove admax-skills` 移除本集合旧来源。移除旧来源可能影响其已安装插件，因此随后重新安装完整插件。

If the same name is registered from another path, inspect `codex plugin marketplace list`. Remove only this collection's old registration using `codex plugin marketplace remove admax-skills`, add the new source, and reinstall. Preserve unrelated sources.

## 校验 / Verify

下载 ZIP 和 SHA256SUMS 后，macOS 执行 `LC_ALL=C shasum -a 256 -c SHA256SUMS`。
On Linux use `sha256sum -c SHA256SUMS`. Retain the extracted directory while registered.

```sh
python3 scripts/check_package.py .
# Optional: real CLI install in a temporary Codex home, without changing personal plugins
python3 scripts/check_package.py . --codex-install
```

安装后 `codex plugin list` 应列出 admax-skills 与对应版本。新会话尝试 `$show-me`；Claude Code 尝试 `/admax-skills:show-me`。CLI 安装验证不代表已验证桌面点击或技能实际完成任务。

After installation, `codex plugin list` should show admax-skills and its version. Try `$show-me` in a new Codex conversation or `/admax-skills:show-me` in Claude Code. CLI installation does not prove desktop UI or workflow execution.

官方规范 / Official specification: https://developers.openai.com/plugins/build/plugins

Update references: [OpenAI workspace sync](https://learn.chatgpt.com/docs/enterprise/plugin-management) · [Claude Code updates](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates).
