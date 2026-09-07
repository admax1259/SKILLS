# SKILLS · A personal Agent Skills collection

[中文](README.md) · [Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md) · [Releases](https://github.com/admax1259/SKILLS/releases)

Collect reusable skills, preserve attribution and licenses, adapt them deliberately, and validate them in real workflows. One canonical skill body is distributed through Codex and Claude Code plugin manifests.

## Collection

| Plugin | Purpose | Upstream | Status |
|---|---|---|---|
| show-me | Explain a topic with Mermaid, code trees, diffs, or focused HTML | [HumanLayer](plugins/show-me/UPSTREAM.md) · MIT | Packaged; see runtime verification limits below |

The 18 cursor-team-kit skills remain under [individual review](docs/migration-review.zh-CN.md); they are not distributed yet.

## Install

Requires Python 3.10+ and your chosen engine CLI. Until the initial infrastructure PR is merged, use its branch or CI artifact. Installation from main becomes available after merge.

After cloning, install a plugin with one command:

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --plugin show-me
# Or:
python3 scripts/install.py --engine claude --plugin show-me
```

Use `--dry-run` to print commands. The installer registers the local marketplace and calls the engine's native plugin installer; it does not overwrite skill directories directly. The engine handles existing marketplace name conflicts; a failed command stops installation. Keep the cloned/extracted directory for local marketplace updates.

Alternatively, inside Claude Code:

```text
/plugin marketplace add admax1259/SKILLS
/plugin install show-me@admax-skills
/show-me:show-me Explain this code visually
```

Native Codex commands:

```sh
codex plugin marketplace add admax1259/SKILLS
codex plugin add show-me@admax-skills
```

Start a fresh session and use `$show-me` in Codex or `/show-me:show-me` in Claude Code. If you previously installed a standalone skill with the same name, inspect its origin before removing the older copy to avoid duplicate discovery.

## Install from a downloaded ZIP

Download `skills-packages-<commit>` from a successful [Actions](https://github.com/admax1259/SKILLS/actions) run, or versioned assets from [Releases](https://github.com/admax1259/SKILLS/releases).

- `skills-<version>.zip`: complete marketplace. Extract, enter `skills-<version>`, and run the Python install command above. Git is not required.
- `show-me-<version>.zip`: standalone plugin with both manifests at the archive root, for surfaces explicitly supporting plugin ZIP import. It is not a marketplace root.
- `SHA256SUMS`: archive checksums. Run `shasum -a 256 -c SHA256SUMS` on macOS or `sha256sum -c SHA256SUMS` on Linux; compare individual hashes using `Get-FileHash -Algorithm SHA256` on Windows.

CI artifacts expire after 30 days. Versioned release assets use a separate release workflow. The first formal release has not been published yet.

## Compatibility

| Surface/capability | Current scope |
|---|---|
| Codex | Official local validator passed; native CLI registration and installation succeeded; fresh-session behavior remains untested |
| ChatGPT Plugins | OpenAI plugin format provided; capabilities depend on the host. No public directory submission or UI installation test yet |
| Claude Code | Native manifest, marketplace, and installer; Claude CLI is unavailable on the development machine, so runtime validation is pending |
| Other Claude surfaces | Standalone plugin ZIP available; surface-specific import remains unverified |
| GitHub / GitLab hosting | Clone from any Git host and register locally; this repository and its CI currently live on GitHub |
| GitHub PR / GitLab MR workflows | Planned for the engineering collection; show-me does not operate on PRs/MRs |

A model's ability to read a skill does not grant terminal, browser, or repository access. Text/diagram generation and local HTML preview need separate verification.

## Development and releases

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Packages appear in `dist/`. Deliver repository changes through a committed and pushed branch and PR. CI validates and packages changes. Release tags must match VERSION and point into main history before publishing archives and checksums. See the [release process](docs/releases.md).

## Attribution and licenses

Original repository infrastructure uses [Apache-2.0](LICENSE). Third-party content retains its license: show-me uses [MIT](plugins/show-me/skills/show-me/LICENSE), Copyright © 2026 HumanLayer. See [UPSTREAM.md](plugins/show-me/UPSTREAM.md) for the immutable source revision and adaptations. This is a personal collection, not an official project of the upstream authors or engine vendors.

Format references: [OpenAI Plugins](https://developers.openai.com/plugins/build/plugins), [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).
