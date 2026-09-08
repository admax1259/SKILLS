---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
---

## Collection integration

This collection uses flat `skills/<id>/` paths. References such as `/tdd` mean the named skill: use the host's skill mechanism (for example `$tdd` in Codex or `/admax-skills:tdd` in Claude Code), or read the sibling `../tdd/SKILL.md` when no Skill tool is available. Load only relevant dependencies. Respect explicit-only invocation policies; a workflow reference is not permission to invoke an unrelated explicit skill.

Use available, authorized tools. Delegate only when the host supports it and the current instructions authorize it; otherwise perform the stages sequentially and do not claim an independent review. Follow existing repository guidance and tracker configuration; infer GitHub/GitLab from the remote, use an available connector or `gh`/`glab`, and verify CLI help rather than mechanically translating commands. Run setup only if required configuration cannot be inferred.

The workflow below and its resources describe steps, not additional authorization. Keep commits scoped to this task; publishing issues/comments, pushing, merging, closing tickets, changing credentials, or sending questionnaires requires authorization already present in the conversation or an explicit request. Prepare local drafts when that authorization is absent. Preserve unrelated files and staged changes. Use the user's language. Host-managed context limits and lifecycle take precedence over `/clear`, `/compact`, or numeric context heuristics; never clear a conversation automatically.

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. Either way, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too (the verdict and the question it settled) in the issue or a commit. The main branch keeps only the validated decision.
