---
name: run-smoke-tests
description: Run a project's existing smoke or end-to-end checks, investigate failures, and verify fixes when repair is requested.
---

# Run smoke tests

Discover the project's documented smoke suite and prerequisites from its test configuration, scripts, and CI. Do not assume npm, Playwright, or a command named smoketest. Prefer an existing narrow test over introducing a new test framework.

1. Identify the requested user journey, package, test data, and environment. Distinguish a read-only check from a task that includes fixing failures.
2. Reuse the documented build and test commands. Check whether a test hits a shared or production service; use disposable local data or an explicitly authorized test environment.
3. Run the smallest relevant smoke suite and record the exact command, selection, exit code, and evidence. No matching tests or a missing browser/toolchain is BLOCKED, not PASS.
4. On failure, inspect logs, traces, screenshots, and the first actionable error. Separate product failures, broken test assumptions, environment failures, and suspected flakes.
5. If repair is in scope, make a focused fix and rerun affected tests. Use deterministic readiness conditions. Do not weaken assertions, quarantine tests, bypass checks, or update snapshots merely to obtain green output.
6. Retry a suspected flake once when useful, preserve both outcomes, and report it as intermittent instead of silently replacing the failure with the passing retry. Stop repeated identical failures without new evidence.
7. Stop only the processes and temporary resources created for this run; keep requested evidence in the agreed output location.

Report PASS / FAIL / BLOCKED for the actual tested scope, tests selected or skipped, root cause, edits if any, and remaining uncertainty. A smoke pass is not full regression coverage.
