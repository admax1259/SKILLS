# SKILLS

[中文](README.md) · [Skill catalog](docs/CATALOG.md) · [Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md)

A personal Agent Skills collector: collect consistently, preserve provenance, review each workflow, then package for different engines.

**19 skills, 6 categories, 2 sources. Currently 3 ready and 16 awaiting adaptation.**

## Layout

```text
SKILLS/
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
- **All 18 cursor-team-kit skills are physically imported**, including PR canvas resources. They are categorized by verification, review, code quality, delivery, and knowledge. Except for the adapted check-compiler-errors and deslop skills, the other 16 retain upstream behavior and remain review-needed pending [individual discussion](docs/migration-review.zh-CN.md).

Ready means eligible for packaging, not behaviorally verified on every engine. Bundles containing unreviewed members are withheld entirely rather than silently published with missing skills. Generic third-party installers may ignore this repository's status metadata; the installer below enforces it.

## Install

Requires Python 3.10+ and the Codex or Claude Code CLI. Clone, then build and install with one command:

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --bundle show-me
# Compiler checking skill:
python3 scripts/install.py --engine codex --bundle compiler-checks
# Focused code cleanup:
python3 scripts/install.py --engine codex --bundle code-cleanup
# Claude Code:
python3 scripts/install.py --engine claude --bundle show-me
```

Use --dry-run for a preview with no file writes or installation. The installer builds reviewed bundles into dist/marketplace/, registers that directory, and invokes the native engine installer. Keep the generated directory. Until the new layout is merged, use the PR branch or its CI artifact.

**The source repository is no longer a directly registrable native marketplace.** Sources do not contain generated plugin copies; the native marketplace lives in build output or an extracted installation ZIP. Do not run codex plugin marketplace add . or /plugin marketplace add admax1259/SKILLS against source. Inside Claude Code, register the generated absolute directory path and install show-me@admax-skills.

Invoke $show-me in Codex or /show-me:show-me in Claude Code. For a standalone skill, take the complete skills/show-me/ directory including its license.

## Packages and support

```sh
python3 scripts/package.py
```

Outputs in dist/packages/:

| File | Purpose |
|---|---|
| skills-<version>.zip | Complete native marketplace; extract and run the same installer without Git or build dependencies |
| <bundle>-<version>.zip | Standalone plugin (show-me, compiler-checks, or code-cleanup) with both engine manifests |
| SHA256SUMS | ZIP checksums |

Download from [Actions artifacts](https://github.com/admax1259/SKILLS/actions); formal versions follow the [release process](docs/releases.md). Verify with shasum -a 256 -c SHA256SUMS on macOS or sha256sum -c SHA256SUMS on Linux.

- Codex: native format and installation flow have been validated; new versions are rechecked.
- Claude Code: native format generated; CLI installation remains untested on the development machine.
- ChatGPT / other Claude surfaces: plugin ZIPs provided; UI import and public listing are separate verification steps, with no listing claimed.
- GitHub / GitLab: source on any Git host can be cloned and built. Engineering PR/MR workflow adaptation remains pending.

## Collection workflow

Add skills/<id>/ → preserve LICENSE → register source and catalog entry → review and test → mark ready → include in a bundle. See [Contributing](CONTRIBUTING.md).

```sh
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

CI checks missing entries, duplicate names, invalid bundles, exclusion of unreviewed skills, import integrity, and reproducible archives. Deliver changes through PRs.

## Licenses

Repository-owned tools use [Apache-2.0](LICENSE). Collected skills retain their licenses: this batch from Cursor and HumanLayer is MIT, with full notices in each skill directory. See [sources/](sources/) for provenance and adaptations. This is not an official project of the upstream authors or engine vendors.
