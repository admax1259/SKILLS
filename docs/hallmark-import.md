# Hallmark import / 收录记录

Imported [Nutlope/Hallmark](https://github.com/Nutlope/hallmark/tree/13ac0ec7e148655948100b6396439e481361d690) at immutable revision `13ac0ec7e148655948100b6396439e481361d690`. Upstream skill version: 1.1.0. MIT copyright: 2026 Hallmark contributors.

## Contents / 内容

One canonical skill at `skills/hallmark/`, including the upstream entrypoint and all 106 reference documents. The additional `assets/catalog-tokens.css` is an unchanged copy of upstream `site/css/tokens.css`, needed by the theme guidance. Every upstream file has a recorded SHA-256 in [sources/hallmark.json](../sources/hallmark.json); adapted files retain both baseline and current hashes. The upstream root LICENSE accompanies the skill.

保留一个技能、四种模式：新建界面、只读 audit、指定范围 redesign、参考 study。归入 design 分类，随唯一完整插件发布，总数 45。没有收录上游演示网站、构建依赖或第三方安装器。

## Adaptations / 适配

- Move upstream version into portable frontmatter metadata. Limit discovery to design requests rather than generic audit/research keywords.
- Map invocation and WebFetch references to available host tools. Keep study's source restrictions; report unavailable HTML/CSS evidence instead of inventing it.
- Reuse supplied audience, purpose, tone and authorization; remove the unconditional repeated questionnaire. User requirements and existing design systems take precedence over aesthetic defaults.
- Audit remains read-only, including no cache/log writes. Design cache invalidation includes CSS and design.md. Preserve existing token files and restrict project history to design choices.
- Before building, preview checks are pending. Actual viewport/interaction checks must be performed before reporting success; subjective scores remain self-assessment.
- Bundle the token library locally. Repair 13 upstream-relative links: token links resolve within the installed skill, optional site/docs examples point to the immutable upstream revision.
- An attached screenshot does not establish ownership; abstract reference analysis retains attribution and excludes copied assets/text.

## Verification / 验证范围

The entrypoint and routing, audit/redesign/study, output-contract and external dependency instructions were reviewed; reference-library content is preserved with integrity checks, not individually certified design advice. Tests verify local Markdown dependencies remain inside the packaged skill and exist in both Codex and Claude layouts. Existing provenance tests cover every imported resource. No upstream scripts were executed and no infrastructure or personal plugin configuration was changed.

Package/CLI checks establish installability, not end-to-end quality of generated designs. External fonts, imagery and linked examples may require network access. Upstream vendor/pricing examples are snapshots, not current recommendations. Claude runtime and desktop-click behavior require separate verification.
