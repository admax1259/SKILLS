# SKILLS

[简体中文](README.md) · [Catalog](docs/CATALOG.md) · [Install](docs/INSTALL.md) · [Contributing](CONTRIBUTING.md)

A personal Agent Skills collection: preserve attribution, adapt workflows, and distribute together. **45 skills, 9 categories, 4 upstream sources, one complete plugin.**

**[Download v0.7.0-beta.3](https://github.com/admax1259/SKILLS/releases/tag/v0.7.0-beta.3)** — `skills-0.7.0-beta.3.zip` + `SHA256SUMS`.

One ZIP contains native layouts for Codex and Claude Code. Install the entire collection without selecting separate packs.

## Two installation methods

- **Online updates**: use GitHub source `admax1259/SKILLS` and ref `distribution`, which advances only with validated releases. Claude Code supports opt-in auto-updates; Codex has explicit refresh/install commands.
- **Offline snapshots**: download, verify and extract a Release ZIP; keep older versions for rollback.

Both methods share one plugin identity and payload. Choose one registered source per engine. [Install, update, switch sources and roll back](docs/INSTALL.md#在线安装与升级--online-installation-and-updates).

## Install

**In Codex**: Plugins → Add plugin marketplace:

| Field | GitHub | Extracted Release |
|---|---|---|
| Source | `admax1259/SKILLS` | Absolute path to extracted `skills-0.7.0-beta.3` |
| Git ref | `distribution` | Leave empty |
| Sparse paths | Leave empty | Leave empty |

After adding the source, open **Admax Skills** and click **Install**. Source accepts a repository or directory, not a ZIP or Release page.

**Claude Code**: run `/plugin marketplace add <absolute-extracted-directory>`, then install Admax Skills from Discover.

Alternatively, run one command from the extracted directory (Python 3.10+ and the relevant CLI required):

```sh
python3 scripts/install.py --engine codex
# or
python3 scripts/install.py --engine claude
```

[Detailed setup, checksums, upgrades and troubleshooting](docs/INSTALL.md). Start a new conversation; try `$show-me` in Codex or `/admax-skills:show-me` in Claude Code.

## New: Hallmark interface design

[hallmark](skills/hallmark/SKILL.md) from [Nutlope/Hallmark](https://github.com/Nutlope/hallmark) supports new pages/components, read-only `audit`, scoped `redesign`, and reference `study`. All reference documents and the theme token library are included; existing brand and framework requirements take precedence.

Try `$hallmark audit src/app/page.tsx` or `/admax-skills:hallmark audit src/app/page.tsx` in Claude Code. The design library ships locally; external fonts, assets and online examples may require network access. [Adaptation record](docs/hallmark-import.md).

## 25 skills from Matt Pocock

### engineering

| Skill | Purpose |
|---|---|
| [ask-matt](skills/ask-matt/SKILL.md) | Find the right skill or workflow |
| [code-review](skills/code-review/SKILL.md) | Review a diff on standards and spec |
| [codebase-design](skills/codebase-design/SKILL.md) | Vocabulary for deep-module design |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | Diagnose hard bugs and regressions |
| [domain-modeling](skills/domain-modeling/SKILL.md) | Build and sharpen a domain model |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | Grill a design and write its docs |
| [implement](skills/implement/SKILL.md) | Build work from a spec or tickets |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Find and grill architecture improvements |
| [prototype](skills/prototype/SKILL.md) | Prototype to answer a design question |
| [research](skills/research/SKILL.md) | Research from high-trust sources |
| [resolving-merge-conflicts](skills/resolving-merge-conflicts/SKILL.md) | Resolve merge and rebase conflicts |
| [setup-matt-pocock-skills](skills/setup-matt-pocock-skills/SKILL.md) | Configure a repo for the skills |
| [tdd](skills/tdd/SKILL.md) | Test-driven red-green-refactor |
| [to-spec](skills/to-spec/SKILL.md) | Turn a conversation into a spec |
| [to-tickets](skills/to-tickets/SKILL.md) | Split a plan into tracer-bullet tickets |
| [triage](skills/triage/SKILL.md) | Move issues through triage roles |
| [wayfinder](skills/wayfinder/SKILL.md) | Map a large effort as decision tickets |
| [wizard](skills/wizard/SKILL.md) | Generate an interactive setup wizard |

### productivity

| Skill | Purpose |
|---|---|
| [grill-me](skills/grill-me/SKILL.md) | Sharpen a plan through interview |
| [grilling](skills/grilling/SKILL.md) | Stress-test thinking a round of questions at a time |
| [handoff](skills/handoff/SKILL.md) | Compact a conversation into a handoff |
| [teach](skills/teach/SKILL.md) | Learn a concept in a guided workspace |
| [to-questionnaire](skills/to-questionnaire/SKILL.md) | Front-load questions into a doc for someone to answer |
| [wait-what](skills/wait-what/SKILL.md) | Re-pitch that: simpler, with the context I'm missing |
| [writing-for-agents](skills/writing-for-agents/SKILL.md) | Write documents agents consume |

Start with `ask-matt` for navigation. Use `grill-with-docs` for discovery, then `to-spec` → `to-tickets` → `implement` when useful. These are composable tools, not mandatory stages.

`fix-merge-conflicts` retains the existing delivery workflow; `resolving-merge-conflicts` offers a concise intent-based method. Choose one for a task.

## Existing 19 skills

| Category | Skills |
|---|---|
| visualization | [show-me](skills/show-me/SKILL.md) |
| verification | [check-compiler-errors](skills/check-compiler-errors/SKILL.md), [control-cli](skills/control-cli/SKILL.md), [control-ui](skills/control-ui/SKILL.md), [run-smoke-tests](skills/run-smoke-tests/SKILL.md), [verify-this](skills/verify-this/SKILL.md) |
| code-review | [get-pr-comments](skills/get-pr-comments/SKILL.md), [make-pr-easy-to-review](skills/make-pr-easy-to-review/SKILL.md), [pr-review-canvas](skills/pr-review-canvas/SKILL.md), [thermo-nuclear-code-quality-review](skills/thermo-nuclear-code-quality-review/SKILL.md) |
| code-quality | [deslop](skills/deslop/SKILL.md) |
| delivery | [fix-ci](skills/fix-ci/SKILL.md), [fix-merge-conflicts](skills/fix-merge-conflicts/SKILL.md), [loop-on-ci](skills/loop-on-ci/SKILL.md), [new-branch-and-pr](skills/new-branch-and-pr/SKILL.md), [review-and-ship](skills/review-and-ship/SKILL.md) |
| knowledge | [weekly-review](skills/weekly-review/SKILL.md), [what-did-i-get-done](skills/what-did-i-get-done/SKILL.md), [workflow-from-chats](skills/workflow-from-chats/SKILL.md) |

## Sources and adaptation

| Upstream | Count | License | Provenance |
|---|---:|---|---|
| [Nutlope/Hallmark](https://github.com/Nutlope/hallmark) | 1 | MIT | [hallmark](sources/hallmark.json) |
| [Cursor](https://github.com/cursor/plugins) | 18 | MIT | [cursor-team-kit](sources/cursor-team-kit.json) |
| [HumanLayer](https://github.com/humanlayer/skills) | 1 | MIT | [humanlayer](sources/humanlayer.json) |
| [Matt Pocock](https://github.com/mattpocock/skills) | 25 | MIT | [matt-pocock](sources/matt-pocock.json) |

Each skill retains its license and resources; provenance records immutable upstream commits and file hashes. See the [import review](docs/matt-pocock-import.md). `ready` means eligible for packaging, not behavioral validation of every workflow on every engine. GitHub/GitLab operations require an authorized connector or CLI; bundled wizard CI secret helpers are GitHub-specific.

## Repository organization and maintenance

```text
skills/<id>/SKILL.md       # canonical source and adjacent resources
catalog.json              # categories, readiness, invocation policy
sources/*.json            # upstream revisions, licenses, adaptations
.agents/plugins/          # Codex source marketplace
.codex-plugin/            # Codex source manifest
scripts/                  # validation, packaging, installation
docs/                     # generated catalog and guides
dist/                     # generated releases; not committed
```

Categories and authors live in metadata; skill paths remain flat and stable. Reviewed additions enter the single complete plugin. Releases generate separate Codex and Claude Code directories to keep native manifests isolated.

```sh
python3 scripts/catalog.py
python3 scripts/validate.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

[Changelog](CHANGELOG.md) · [Architecture](docs/architecture.md) · [Validation history](docs/bootstrap.md)
