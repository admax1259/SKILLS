---
name: weekly-review
description: Produce an evidence-backed weekly recap of repository work grouped into fixes, maintenance, and new capabilities.
---

# Weekly review

Resolve the calendar week and timezone the user means. If they do not specify, use the previous completed calendar week in their timezone and state the dates; do not silently stretch it to 7–10 days.

Use the supplied author identity, git config/.mailmap, or authorized provider identity without rewriting configuration. Review the requested/default branch and available commits, diffs, and PR/MR merge evidence. Flag missing history and ambiguous authorship; a squash commit or connector author may differ from the contributor.

Group meaningful work into fixes, maintenance/technical debt, and new capabilities when evidence supports those categories. Mark inference when classification is uncertain. Avoid double-counting merge/cherry-pick equivalents and avoid treating a branch commit as a shipped feature.

Produce a short weekly narrative with concrete date range, scope, supporting links/commits, and notable unfinished work only when requested. Report merged and deployed work separately. Use what-did-i-get-done if available for the collection principles; this skill remains usable with ordinary git/provider tools alone.

Do not publish the recap to chat/email or change tracking data merely because a summary was requested.
