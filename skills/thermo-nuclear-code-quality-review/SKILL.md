---
name: thermo-nuclear-code-quality-review
description: Perform an explicitly requested strict maintainability audit of abstractions, coupling, branching, and structural simplification.
disable-model-invocation: true
---

# Strict code quality review

Use for a requested deep maintainability audit. This is a review, not permission to refactor. Preserve the original explicit-only invocation policy through Claude frontmatter and Codex agents/openai.yaml.

Resolve the requested diff/base or repository scope, user intent, and local architecture. Inspect meaningful callers, invariants, and tests before judging a local abstraction.

Look for removable concepts, repeated policy, tangled state, ownership leaks, unnecessary casts/optionality, brittle partial updates, and wrappers that hide rather than clarify behavior. Prefer simplifications that remove complexity over distributing it across more files. Explain a concrete alternative and its migration cost when recommending structural change.

File size and conditional counts are investigation signals, not automatic blockers. A file crossing 1000 lines alone is not a defect. Check cohesion and actual reasoning burden; generated files and cohesive data tables need different treatment. Do not prescribe parallelism when operations depend on each other or require ordering.

Rank actionable findings by impact. Each needs a code location, evidence, consequence, and a feasible remedy. Separate proven bugs, maintainability risks, and optional design alternatives. Do not manufacture findings or treat an untested elegant alternative as proven behavior-preserving.

Use independent review only when available and authorized; otherwise report a single-agent assessment. Static reading is not execution evidence. Run focused checks when they answer an actual uncertainty; state what remains untested.

Return high-confidence findings first and residual risks afterward. No findings is a valid result. Change code only when requested; preserve behavior and run relevant verification for any approved refactor. Do not submit reviews, approve, or merge without corresponding authorization.
