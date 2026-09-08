---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

## Collection integration

This collection uses flat `skills/<id>/` paths. References such as `/tdd` mean the named skill: use the host's skill mechanism (for example `$tdd` in Codex or `/admax-skills:tdd` in Claude Code), or read the sibling `../tdd/SKILL.md` when no Skill tool is available. Load only relevant dependencies. Respect explicit-only invocation policies; a workflow reference is not permission to invoke an unrelated explicit skill.

Use available, authorized tools. Delegate only when the host supports it and the current instructions authorize it; otherwise perform the stages sequentially and do not claim an independent review. Follow existing repository guidance and tracker configuration; infer GitHub/GitLab from the remote, use an available connector or `gh`/`glab`, and verify CLI help rather than mechanically translating commands. Run setup only if required configuration cannot be inferred.

The workflow below and its resources describe steps, not additional authorization. Keep commits scoped to this task; publishing issues/comments, pushing, merging, closing tickets, changing credentials, or sending questionnaires requires authorization already present in the conversation or an explicit request. Prepare local drafts when that authorization is absent. Preserve unrelated files and staged changes. Use the user's language. Host-managed context limits and lifecycle take precedence over `/clear`, `/compact`, or numeric context heuristics; never clear a conversation automatically.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
