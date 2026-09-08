# SKILLS

[中文](README.md) · [Skill catalog](docs/CATALOG.md) · [Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md)

A personal Agent Skills collector: collect consistently, preserve provenance, review each workflow, then package for different engines.

**[Download the complete beta package](https://github.com/admax1259/SKILLS/releases): one ZIP, all 19 skills, supporting both Codex and Claude Code.** Download `skills-<version>.zip` and `SHA256SUMS` from the latest Pre-release Assets. No individual skill packages to choose.

**19 skills, 6 categories, 2 sources. All 19 adapted and eligible for packaging; see [bootstrap evidence](docs/bootstrap.md) for tested scope.**

## Layout

```text
SKILLS/
├── .agents/plugins/marketplace.json # Marketplace for the single root plugin
├── .codex-plugin/plugin.json     # Root plugin referencing skills/ directly
├── skills/                       # Canonical sources; one stable path per skill
│   ├── show-me/
│   │   ├── SKILL.md
│   │   └── LICENSE
│   ├── check-compiler-errors/
│   ├── control-cli/
│   ├── control-ui/
│   ├── pr-review-canvas/          # Includes renderer.js, styles.css, template.html
│   └── …                         # All 19 entries are in the catalog
├── catalog.json                  # Categories, origins, review status, bundle membership
├── sources/                      # Upstream URLs, immutable commits, licenses, import records
│   ├── cursor-team-kit.json
│   └── humanlayer.json
├── scripts/                      # Validation, index, build, installation
├── tests/
├── docs/
└── dist/                         # Generated plugins and ZIPs; untracked, never hand-edited
```

Browse by category through the [index](docs/CATALOG.md), without moving skills through nested folders. Maintain one source per skill; all reviewed skills enter the complete plugin. Adding an author, category, or engine does not change existing skill paths.

## Collected content

- [show-me](skills/show-me/SKILL.md): ready for packaging; from HumanLayer, with portable preview behavior.
- [check-compiler-errors](skills/check-compiler-errors/SKILL.md): adapted to check/report by default and repair when requested; included in the complete plugin.
- [deslop](skills/deslop/SKILL.md): focused diff cleanup preserving behavior, necessary comments, and error handling; included in the complete plugin.
- **All 18 cursor-team-kit skills are physically imported**, including PR canvas resources. They are categorized by verification, review, code quality, delivery, and knowledge. All 18 engineering skills are adapted and included in the complete plugin; see the [migration review](docs/migration-review.zh-CN.md).

Ready means eligible for packaging, not behaviorally verified on every engine. Bundles containing unreviewed members are withheld entirely rather than silently published with missing skills. Generic third-party installers may ignore this repository's status metadata; the installer below enforces it.

## Install all skills

**Fill Add plugin marketplace in the app:**

| Field | GitHub source | Extracted Release source |
|---|---|---|
| Source | `admax1259/SKILLS` | Absolute path to the extracted `skills-0.6.0-beta.3` folder |
| Git ref | `v0.6.0-beta.3` | Leave empty |
| Sparse paths | Leave empty | Leave empty |

Click Add marketplace, select Admax Skills, open the plugin card and click Install. Source is not a ZIP path; `plugins/codex` is only a UI example. See [INSTALL](docs/INSTALL.md) for the exact fields and [package audit](docs/package-audit.md) for required/optional files and verification limits.


Download the complete ZIP from [GitHub Releases](https://github.com/admax1259/SKILLS/releases), extract it to a permanent location, and enter `skills-<version>/`. Requires Python 3.10+ and the engine CLI. Choose your engine:

```sh
# Codex
python3 scripts/install.py --engine codex

# Claude Code
python3 scripts/install.py --engine claude
```

Both commands install one complete `admax-skills` plugin containing show-me and all 18 engineering skills. Start a fresh session and retain the extracted directory. Add `--dry-run` to preview commands.

**Codex UI**: run `codex plugin marketplace add .` in the extracted directory, restart the app, select Admax Skills in Plugins Directory, and click Install. **Claude Code UI**: run `/plugin marketplace add <absolute-extracted-directory>`, then install Admax Skills from Discover.

If the same marketplace name is already registered, inspect `codex plugin marketplace list` or the Claude equivalent. Before changing paths, remove only this repository's old admax-skills source using the engine's native command, then register the new directory. Preserve unrelated sources. Uninstall old individual plugins such as show-me and engineering-kit to avoid duplicate activation.

### Install from source

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex
# Use --engine claude for Claude Code
```

The source installer validates the catalog, includes only ready skills, builds at stable `dist/marketplace/`, and installs the complete plugin. Categories and historical bundles are collection metadata, no longer installation choices.

### Download assets

| File | Purpose |
|---|---|
| `skills-<version>.zip` | The single complete installer package for both Codex and Claude Code |
| `SHA256SUMS` | SHA-256 checksum for the complete package |

macOS: `LC_ALL=C shasum -a 256 -c SHA256SUMS`; Linux: `sha256sum -c SHA256SUMS`. GitHub's automatic Source code ZIP requires building. Merging a new VERSION to main automatically publishes packages; `-beta.N` versions are prereleases. See [release instructions](docs/releases.md).

### ChatGPT and runtime support

[OpenAI's testing documentation](https://developers.openai.com/plugins/deploy/connect-chatgpt) distinguishes skills-only local marketplaces from optional MCP connections. This collection has no MCP server. Do not enter a ZIP or repository URL as an MCP URL. Generic ChatGPT ZIP upload, public listing, and desktop UI clicking remain unverified.

Codex manifests, archive contents, and reproducible builds are validated. Claude Code native format and explicit invocation policies have structural tests; this development machine has no Claude CLI, so runtime activation remains unverified. Skills need host-provided terminal, repository, and GitHub/GitLab tools.

Codex examples: `$show-me`, `$verify-this`. Claude Code: `/admax-skills:show-me`, `/admax-skills:verify-this`. PR canvas and comprehensive quality review retain explicit invocation; the builder handles engine-specific policy without separate downloads.

## Collection workflow

Add skills/<id>/ → preserve LICENSE → register source and catalog entry → review and test → mark ready → include in the complete plugin. See [Contributing](CONTRIBUTING.md).

```sh
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Full development tests also require Node.js 22+ for Canvas rendering regressions; installing a prebuilt plugin does not require Node.js.

CI checks missing entries, duplicate names, invalid bundles, exclusion of unreviewed skills, import integrity, and reproducible archives. Deliver changes through PRs.

## Licenses

Repository-owned tools use [Apache-2.0](LICENSE). Collected skills retain their licenses: this batch from Cursor and HumanLayer is MIT, with full notices in each skill directory. See [sources/](sources/) for provenance and adaptations. This is not an official project of the upstream authors or engine vendors.
