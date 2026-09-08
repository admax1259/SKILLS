# Matt Pocock import review / 导入评审

Imported `engineering` (18) and `productivity` (7) from [mattpocock/skills at 3cca18b](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015/skills). Other upstream groups are excluded. All 25 skills and adjacent resources were reviewed as source documents, not executed as instructions during ingestion.

仅导入指定的两个目录，保留配套模板、文档、脚本与 Codex UI 元数据。每个目录附上上游 MIT LICENSE；逐文件上游哈希与适配后哈希见 [provenance](../sources/matt-pocock.json)。

## Adaptation decisions

- Flat canonical paths preserve all relative resource links. Cross-skill names resolve through the host skill mechanism or sibling files; a Claude-specific Skill tool is not required.
- Existing explicit-only policies remain in catalog.json and agents/openai.yaml. The package builder generates Claude's `disable-model-invocation` flag. Argument hints move into portable body text.
- Available connectors or provider CLIs may serve GitHub/GitLab. Existing tracker settings take precedence over setup. Resource CLI examples need current help verification; the wizard's bundled secret helpers remain GitHub-specific.
- Delegation requires host capability and authorization; sequential execution must not be called independent review. Publishing, closing tickets, merging and credential changes remain within the user's authorized scope; local drafts are the fallback.
- Conflict resolution preserves unrelated staged changes and honors a requested abort. TDD reuses already agreed interfaces instead of asking for the same approval again.
- Context limits follow the actual host/model; clearing a conversation is never automatic. Explanations use the user's language.
- Mermaid reports use strict security and escaped input. The supplied CDN template requires network access; provide text fallback offline.

## Scope and overlap

All 25 additions are eligible for the single complete plugin. Categories are metadata, not extra installable bundles. `ask-matt` is a navigation aid, not an obligatory entry point. Existing `fix-merge-conflicts` and new `resolving-merge-conflicts` are alternatives; select the workflow appropriate to the task rather than running both.

## Validation boundaries

Repository tests check provenance integrity, resource preservation and explicit-policy translation for both engine outputs. Shell templates receive syntax checks only: tests must not provision infrastructure or write real secrets. Package checks and isolated Codex CLI installation establish distribution compatibility, not end-to-end behavior of all 44 workflows. Claude runtime and desktop-click verification must be reported separately; neither is implied by generated manifest validation.
