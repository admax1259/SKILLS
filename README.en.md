# SKILLS

[中文](README.md) · [Skill catalog](docs/CATALOG.md) · [Architecture](docs/architecture.md) · [Contributing](CONTRIBUTING.md)

A personal Agent Skills collector: collect consistently, preserve provenance, review each workflow, then package for different engines.

**19 skills, 6 categories, 2 sources. All 19 adapted and eligible for packaging; see [bootstrap evidence](docs/bootstrap.md) for tested scope.**

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
- **All 18 cursor-team-kit skills are physically imported**, including PR canvas resources. They are categorized by verification, review, code quality, delivery, and knowledge. All 18 engineering skills are adapted and available in engineering-kit; see the [migration review](docs/migration-review.zh-CN.md).

Ready means eligible for packaging, not behaviorally verified on every engine. Bundles containing unreviewed members are withheld entirely rather than silently published with missing skills. Generic third-party installers may ignore this repository's status metadata; the installer below enforces it.

## Install

Requires Python 3.10+ and the Codex or Claude Code CLI. Clone, then build and install with one command:

```sh
git clone https://github.com/admax1259/SKILLS.git
cd SKILLS
python3 scripts/install.py --engine codex --bundle show-me
# Complete engineering collection (already includes compiler-checks and code-cleanup skills):
python3 scripts/install.py --engine codex --bundle engineering-kit
# Or install only compiler checking:
python3 scripts/install.py --engine codex --bundle compiler-checks
# Focused code cleanup:
python3 scripts/install.py --engine codex --bundle code-cleanup
# Claude Code:
python3 scripts/install.py --engine claude --bundle engineering-kit
```

### ChatGPT

Enter `https://github.com/admax1259/SKILLS` directly in ChatGPT's add-plugin flow. The repository
root now contains both a marketplace manifest and the `admax-skills` plugin manifest, so no build is
required. A local Codex installation can use `codex plugin marketplace add /path/to/SKILLS` followed
by `codex plugin add admax-skills@admax-skills`. If the UI asks for an upload instead, run
`python3 scripts/package.py` and upload `dist/packages/current/admax-skills-chatgpt-<version>.zip`.
Workflows needing a terminal, repository, or another host tool still require that tool in the chat.

If an older checkout reported `marketplace root does not contain a supported manifest`, pull a
revision containing `.agents/plugins/marketplace.json` and retry. Use `codex plugin marketplace list`
and `codex plugin list` to confirm that both the marketplace and plugin are discovered.

Use --dry-run for a preview with no file writes or installation. The installer builds reviewed bundles into dist/marketplace/, registers that directory, and invokes the native engine installer. Keep the generated directory. Until 0.5.0 is merged, use this PR branch or its CI artifact.

**The source repository is directly registrable as an OpenAI marketplace.** Its root manifests reference canonical `skills/` without maintaining plugin copies; generated output remains in ignored `dist/`. Claude Code's multi-bundle marketplace continues to use the generated absolute directory.

Invoke $show-me or $verify-this in Codex; /show-me:show-me or /engineering-kit:verify-this in Claude Code. Canvas and strict quality review retain explicit-only invocation. For a standalone skill, take the complete skills/show-me/ directory including its license.

## Packages and support

```sh
python3 scripts/package.py
```

Outputs in dist/packages/current/:

| File | Purpose |
|---|---|
| skills-<version>.zip | Complete native marketplace; extract and run the same installer without Git or build dependencies |
| admax-skills-chatgpt-<version>.zip | Single root-manifest plugin for direct ChatGPT upload; includes all reviewed skills |
| <bundle>-<version>.zip | Dual-engine show-me, compiler-checks, or code-cleanup plugin |
| engineering-kit-<engine>-<version>.zip | Engine-specific Codex or Claude engineering plugin; differing invocation policies are generated automatically |
| SHA256SUMS | ZIP checksums |

Download from [Actions artifacts](https://github.com/admax1259/SKILLS/actions); formal versions follow the [release process](docs/releases.md). Verify with shasum -a 256 -c SHA256SUMS on macOS or sha256sum -c SHA256SUMS on Linux.

- Codex: native format and installation flow have been validated; new versions are rechecked.
- Claude Code: native format generated; CLI installation remains untested on the development machine.
- ChatGPT: a single root-manifest plugin is generated for direct upload; public listing remains a separate verification step, with no listing claimed.
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
