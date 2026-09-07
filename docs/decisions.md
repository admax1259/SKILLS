# Decisions / 决策记录

## 2026-09-03 — Repository management

The owner requests a personal skills collector at SKILLS, bilingual documentation, Codex and Claude plugin distribution, downloadable local-install artifacts, and pushing changes through PRs. Remote: https://github.com/admax1259/SKILLS . PRs are the default delivery boundary; publication in a platform directory is a separate process.

Canonical content lives under plugins/<collection>/skills/<skill>. Engine manifests and catalogs wrap the same files. Repository-owned infrastructure retains Apache-2.0; HumanLayer show-me retains MIT.

Release 0.1.0 is the initial package version, not a claim that a release has already been published. CI packages every push/PR and publishes immutable versioned release assets on matching v* tags. No automatic merge.

## Migration discussion 1 — check-compiler-errors (pending)

Original behavior: run compile/type checks, group failures, automatically fix high-confidence issues, repeat until clean or blocked.

Proposed choice: default to checking/reporting; repair only when the user's request includes fixing. Alternative: preserve automatic repair. Await the owner's choice before migrating. GitHub/GitLab are not required for local compiler checks; discover project commands rather than hardcoding npm or TypeScript.
