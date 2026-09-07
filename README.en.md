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

## What these skills help you do

HumanLayer's **show-me** provides visual explanations; **18 Cursor team kit workflows** cover verification, review, code quality, delivery and reflection. All are adapted with original licenses, pinned provenance and recorded modifications.

Use the examples as task prompts. Execution requires the relevant repository, terminal, browser or provider access in the host.

| Skill | Category | Capability and scope | Example prompt |
|---|---|---|---|
| [show-me](skills/show-me/SKILL.md) | Visualization | Explain concepts, trees and flows with Mermaid, pseudocode or interactive HTML and available host previews. | Show how this repository packages and installs skills. |
| [check-compiler-errors](skills/check-compiler-errors/SKILL.md) | Verification | Discover real build/type checks; distinguish code errors from environment blockers. Report by default, repair on request. | Check compiler errors without changing code. |
| [run-smoke-tests](skills/run-smoke-tests/SKILL.md) | Verification | Run existing smoke tests, record results, and diagnose failures; disclose missing harnesses or environments. | Run smoke tests and diagnose failures. |
| [verify-this](skills/verify-this/SKILL.md) | Verification | Turn a claim into measurable criteria and return verified, not verified or inconclusive. | Verify that packages include every skill and license. |
| [control-cli](skills/control-cli/SKILL.md) | Verification | Reproduce CLI/TUI behavior with available terminal tools, exit evidence and owned session cleanup. | Reproduce this CLI interaction hang. |
| [control-ui](skills/control-ui/SKILL.md) | Verification | Use available browser/desktop automation to inspect interactions, state and errors while preserving user sessions. | Check that this page expands and collapses correctly. |
| [get-pr-comments](skills/get-pr-comments/SKILL.md) | Code review | Summarize PR/MR feedback with discussion state, locations and links; read-only by default. | List actionable unresolved feedback on this MR. |
| [make-pr-easy-to-review](skills/make-pr-easy-to-review/SKILL.md) | Code review | Improve descriptions and reviewer reading order; preserve behavior and require explicit history-rewrite authorization. | Make this PR easier to review with context and test results. |
| [pr-review-canvas](skills/pr-review-canvas/SKILL.md) | Code review | Explicitly generate an offline interactive PR/MR walkthrough with faithful imports, whitespace changes and line numbers. | Use $pr-review-canvas for a visual walkthrough of this PR. |
| [thermo-nuclear-code-quality-review](skills/thermo-nuclear-code-quality-review/SKILL.md) | Code review | Explicit strict maintainability audit of abstractions, coupling and complexity; findings do not imply a broad refactor. | Use $thermo-nuclear-code-quality-review on this branch. |
| [deslop](skills/deslop/SKILL.md) | Code quality | Remove justified diff noise while preserving behavior, rationale and safeguards; no changes is a valid result. | Clean this diff without changing behavior. |
| [fix-merge-conflicts](skills/fix-merge-conflicts/SKILL.md) | Delivery | Resolve the active merge/rebase/cherry-pick using both sides' intent, scoped verification and preserved unrelated work. | Resolve the current rebase conflicts and verify. |
| [fix-ci](skills/fix-ci/SKILL.md) | Delivery | Diagnose current-revision checks and logs, then apply bounded focused repairs for PR/MR workflows. | Fix CI failures for this PR's current revision. |
| [loop-on-ci](skills/loop-on-ci/SKILL.md) | Delivery | Watch current PR/MR checks with bounded waits and authorized repairs; stale, empty or manual states are not success. | Watch this MR's CI and repair in-scope failures. |
| [new-branch-and-pr](skills/new-branch-and-pr/SKILL.md) | Delivery | Preserve workspace state, implement, commit and create a PR/MR with existing-branch and fork awareness. | Implement this change and open a PR. |
| [review-and-ship](skills/review-and-ship/SKILL.md) | Delivery | Review, verify and deliver changes through a PR/MR; shipping does not implicitly include merge, release or deployment. | Review and verify this branch, then open a PR. |
| [what-did-i-get-done](skills/what-did-i-get-done/SKILL.md) | Knowledge | Summarize work by identity, timezone and interval, distinguishing commits, merges and deployments. | Summarize my work in this repo over the last two days. |
| [weekly-review](skills/weekly-review/SKILL.md) | Knowledge | Create an evidence-based weekly review of features, fixes and debt without publishing it automatically. | Review my last complete calendar week using repository records. |
| [workflow-from-chats](skills/workflow-from-chats/SKILL.md) | Knowledge | Extract workflows and explicit preferences from authorized chats without making one-off comments permanent rules. | Record the repository workflow agreed in this conversation. |

## Choose a bundle

| Bundle | Contents | Best for |
|---|---|---|
| `show-me` | One visualization skill | Understanding problems visually |
| `engineering-kit` | All 18 engineering skills | Development, PR/MR delivery and reflection; pair with show-me |
| `compiler-checks` | Only check-compiler-errors | Compiler/type checking alone |
| `code-cleanup` | Only deslop | Behavior-preserving diff cleanup alone |

engineering-kit already includes compiler-checks and code-cleanup skills. Canvas and strict quality review retain explicit-only invocation; other skills can be matched by the host or named directly. Installation does not prove automatic selection behavior.

Ready means eligible for packaging. See [bootstrap evidence](docs/bootstrap.md) for tested scope and the [migration review](docs/migration-review.zh-CN.md) for decisions. Future imports enter bundles only after readiness review.

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

Use --dry-run for a preview with no file writes or installation. The installer builds reviewed bundles into dist/marketplace/, registers that directory, and invokes the native engine installer. Keep the generated directory. 0.5.0 is merged into main; start a fresh session after installation.

**The source repository is no longer a directly registrable native marketplace.** Sources do not contain generated plugin copies; the native marketplace lives in build output or an extracted installation ZIP. Do not run codex plugin marketplace add . or /plugin marketplace add admax1259/SKILLS against source. Inside Claude Code, register the generated absolute directory path and install show-me@admax-skills.

Invoke $show-me or $verify-this in Codex; /show-me:show-me or /engineering-kit:verify-this in Claude Code. Canvas and strict quality review retain explicit-only invocation. For a standalone skill, take the complete skills/show-me/ directory including its license.

## Download from GitHub and install locally

Currently distributed as **Actions build artifacts**, with no formal Release published yet. Choose the complete marketplace ZIP so the installer selects the correct engine variant.

1. Sign in to GitHub and open [Actions](https://github.com/admax1259/SKILLS/actions/workflows/ci.yml).
2. Select a successful **Validate and package** run on **main**, then find **Artifacts** at the bottom.
3. Download `skills-packages-<commit>`. This repository retains artifacts for **30 days**; use a newer successful build after expiry.
4. Extract the outer download ZIP to get six installation ZIPs and `SHA256SUMS`. Then extract `skills-0.5.0.zip` (substitute the version for newer builds).
5. Keep `skills-0.5.0/` in a permanent location, enter that directory, and run:

```sh
python3 scripts/install.py --engine codex --bundle engineering-kit
python3 scripts/install.py --engine codex --bundle show-me
# With Claude Code CLI installed, use:
python3 scripts/install.py --engine claude --bundle engineering-kit
python3 scripts/install.py --engine claude --bundle show-me
```

When the marketplace name is already registered, reuse its stable directory during upgrades, or remove the old registration through the engine CLI before registering another path. Keep the extracted directory while registered. Start a fresh session, then try `Use $verify-this to verify this project's packages` or `Use $show-me to explain this project`.

[Post-merge 0.5.0 build](https://github.com/admax1259/SKILLS/actions/runs/34171173838) · [Build artifact](https://github.com/admax1259/SKILLS/actions/runs/34171173838/artifacts/10035744753). All six downloaded ZIPs passed SHA-256 checks; engineering-kit and show-me were installed into Codex from the downloaded package. This fixed artifact link expires with retention; use the Actions entry above afterward. See [GitHub download requirements](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts).

## Packages and support

```sh
python3 scripts/package.py
```

Outputs in dist/packages/current/:

| File | Purpose |
|---|---|
| skills-<version>.zip | Complete native marketplace; extract and run the same installer without Git or build dependencies |
| <bundle>-<version>.zip | Dual-engine show-me, compiler-checks, or code-cleanup plugin |
| engineering-kit-<engine>-<version>.zip | Engine-specific Codex or Claude engineering plugin; differing invocation policies are generated automatically |
| SHA256SUMS | ZIP checksums |

Download from [Actions artifacts](https://github.com/admax1259/SKILLS/actions); formal versions follow the [release process](docs/releases.md). Verify with shasum -a 256 -c SHA256SUMS on macOS or sha256sum -c SHA256SUMS on Linux.

- Codex: native format and installation flow have been validated; new versions are rechecked.
- Claude Code: native format generated; CLI installation remains untested on the development machine.
- ChatGPT / other Claude surfaces: plugin ZIPs provided; UI import and public listing are separate verification steps, with no listing claimed.
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
