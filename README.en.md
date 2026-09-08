# SKILLS

[中文](README.md) · [Skill catalog](docs/CATALOG.md) · [Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md)

A personal Agent Skills collector: collect consistently, preserve provenance, review each workflow, then package for different engines.

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

Browse by category through the [index](docs/CATALOG.md), without moving skills through nested folders. Maintain one source per skill and include it in multiple bundles when useful. Adding an author, category, or engine does not change existing skill paths.

## Collected content

- [show-me](skills/show-me/SKILL.md): ready for packaging; from HumanLayer, with portable preview behavior.
- [check-compiler-errors](skills/check-compiler-errors/SKILL.md): adapted to check/report by default and repair when requested; install the compiler-checks bundle.
- [deslop](skills/deslop/SKILL.md): focused diff cleanup preserving behavior, necessary comments, and error handling; install the code-cleanup bundle.
- **All 18 cursor-team-kit skills are physically imported**, including PR canvas resources. They are categorized by verification, review, code quality, delivery, and knowledge. All 18 engineering skills are adapted and available in engineering-kit; see the [migration review](docs/migration-review.zh-CN.md).

Ready means eligible for packaging, not behaviorally verified on every engine. Bundles containing unreviewed members are withheld entirely rather than silently published with missing skills. Generic third-party installers may ignore this repository's status metadata; the installer below enforces it.

## Install

### Bundle installation (Codex / Claude Code)

Building and installing from source requires Python 3.10+ and the selected engine CLI. Build scripts use only the Python standard library. Clone, then choose the commands you need:

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --bundle show-me
# 18 engineering skills; includes compiler-checks and code-cleanup, not show-me
python3 scripts/install.py --engine codex --bundle engineering-kit
# Alternatively, install individual bundles:
python3 scripts/install.py --engine codex --bundle compiler-checks
python3 scripts/install.py --engine codex --bundle code-cleanup
# Claude Code uses the generated engine-specific marketplace:
python3 scripts/install.py --engine claude --bundle engineering-kit
```

These are alternatives; do not run every command unless intended. `scripts/install.py` defaults to the `show-me` bundle and supports only `codex` and `claude`, not a ChatGPT installer.

Append `--dry-run` to validate and preview without building plugins, invoking engine installation, or requiring an installed engine CLI:

```sh
python3 scripts/install.py --engine codex --bundle engineering-kit --dry-run
```

The source installer validates the catalog, permits only bundles whose members are all `ready`, builds `dist/marketplace/`, registers its absolute path, and invokes the engine CLI. Keep that directory and start a fresh engine session after installation.

### Single root plugin (Codex manifests)

Unlike bundle builds, [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) declares just one plugin, `admax-skills`; [.codex-plugin/plugin.json](.codex-plugin/plugin.json) points directly to `./skills/`. From a checkout containing these manifests, the registration commands for this layout are:

```sh
codex plugin marketplace add .
codex plugin add admax-skills@admax-skills
codex plugin marketplace list
codex plugin list
```

This path does not run the Python builder or filter by catalog review status: it exposes the entire `skills/` directory, currently 19 skills. The root-plugin test requires every catalog entry to be `ready`. Use bundle installation or generated packages when review filtering is needed.

Both root and generated marketplaces are named `admax-skills`, but their plugin lists differ. Choose one layout and check the CLI's registered path; do not confuse `admax-skills@admax-skills` with `engineering-kit@admax-skills`. The source root has no Claude marketplace manifest; use the generated directory for Claude Code.

For `marketplace root does not contain a supported manifest`, first verify that the checked-out branch and directory contain the root manifests. Do not register an older source layout or the wrong directory as a generated marketplace. Manifest presence and actual CLI compatibility are separate checks.

### ChatGPT-targeted ZIP

In `scripts/package.py`, `build_chatgpt_plugin()` selects all `ready` catalog entries and creates a single OpenAI-format plugin ZIP:

```sh
python3 scripts/package.py
```

The output is `dist/packages/current/admax-skills-chatgpt-<version>.zip`, with `<version>` read from `VERSION`. Its root contains `.codex-plugin/plugin.json`, `skills/`, `SOURCES.json`, and a README; per-skill licenses are retained. The plugin manifest is copied from the root manifest and its version must match `VERSION`.

Code and tests establish package structure and contents, not whether the current ChatGPT UI supports repository URLs, ZIP uploads, or a successful import. Use this ZIP only where the UI explicitly accepts that format; do not substitute the complete marketplace ZIP. The host must still expose a terminal, repository, or other tools needed by each workflow; this plugin does not provide those connections.

### Invocation policies

Codex examples are `$show-me` and `$verify-this`; Claude Code bundle examples are `/show-me:show-me` and `/engineering-kit:verify-this`.

The catalog marks `pr-review-canvas` and `thermo-nuclear-code-quality-review` as `invocation: explicit`. Validation requires ready explicit-only skills to set `allow_implicit_invocation: false` in `agents/openai.yaml`; the builder adds `disable-model-invocation: true` to Claude copies. This metadata mapping is not proof of runtime invocation behavior on every host. When copying a standalone skill, preserve its complete directory and LICENSE.

## Packages and support

```sh
python3 scripts/package.py
```

Outputs in `dist/packages/current/`. Rebuilding replaces output bearing this builder's ownership marker; old artifacts are not retained:

| File | Purpose |
|---|---|
| skills-<version>.zip | Complete native marketplace; extract and run the same installer without Git or rebuilding; still requires Python 3.10+ and the engine CLI |
| admax-skills-chatgpt-<version>.zip | ChatGPT-targeted single plugin; all ready skills, UI import unverified |
| <bundle>-<version>.zip | Dual-engine show-me, compiler-checks, or code-cleanup plugin |
| engineering-kit-<engine>-<version>.zip | Engine-specific Codex or Claude engineering plugin; differing invocation policies are generated automatically |
| SHA256SUMS | ZIP checksums |

Download from [Actions artifacts](https://github.com/admax1259/SKILLS/actions); formal versions follow the [release process](docs/releases.md). Verify with shasum -a 256 -c SHA256SUMS on macOS or sha256sum -c SHA256SUMS on Linux.

- Codex: native format and installation flow have been validated; new versions are rechecked.
- Claude Code: native format generated; CLI installation remains untested on the development machine.
- ChatGPT: target ZIP structure and contents are tested; repository URL installation, UI import, runtime behavior, and public listing are not established by repository tests.
- GitHub / GitLab: instructions cover PR/MR, forks, current-revision CI, and discussion state; Canvas includes read-only collection for both. GitHub has live repository evidence; GitLab collection uses fixtures and live MR writes remain unverified.

## Collection workflow

Add skills/<id>/ → preserve LICENSE → register source and catalog entry → review and test → mark ready → include in a bundle. See [Contributing](CONTRIBUTING.md).

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
