# Contributing / 收录规范

每个贡献通过 PR 交付。请先说明来源、用途、授权和与已有 skill 的区别，再修改技能。

For every collected skill, record the upstream URL and immutable commit, preserve the original license, describe local adaptations, and provide one realistic usage scenario. Do not import unlicensed material or private conversations.

Keep one canonical body under plugins/<collection>/skills/<skill>/SKILL.md. Keep all runtime resources inside the plugin directory. Update both READMEs, both engine catalogs, provenance, and compatibility notes when adding a plugin.

Run:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests
python3 scripts/package.py
```

Tests validate the repository contract and archive contents. Engine discovery and actual skill behavior need separate evidence. Record untested engines honestly.
