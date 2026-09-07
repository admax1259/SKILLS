# Snapshot contract

Python 3.10+ renders this JSON without additional packages. Collection requires an authenticated GitHub CLI (gh) or GitLab CLI (glab), or equivalent connector reads. Never place credentials in snapshots.

```json
{
  "provider": "gitlab",
  "host": "gitlab.example.com",
  "repo": "group/subgroup/project",
  "number": 12,
  "title": "Explain the changed behavior",
  "url": "https://gitlab.example.com/group/subgroup/project/-/merge_requests/12",
  "head_sha": "observed revision",
  "summary": "Plain text reviewer walkthrough.",
  "limitations": ["CI and comments were not collected."],
  "files": [
    {
      "path": "src/example.py",
      "old_path": null,
      "status": "modified",
      "patch": "@@ -1 +1 @@\n-old\n+new",
      "incomplete": false,
      "note": "Plain text explanation or evidence-backed finding."
    }
  ]
}
```

Required render fields: title, head_sha, files, and each file's path.
Patch may be null for binary/unavailable content. Incomplete must be true when a provider signals collapsed or oversized content. Do not synthesize missing patches. Array order is review order; identity uses numeric keys so similar filenames cannot collide.

Provider references:
- [GitHub PR files](https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files): paginate; at most 3,000 files are returned.
- [GitLab MR diffs](https://docs.gitlab.com/api/merge_requests/#list-merge-request-diffs): encode nested project paths; honor diff limits.
- [GitLab CLI API](https://docs.gitlab.com/cli/api/): select the explicit hostname.

The snapshot is a time-bound read, not a merge-readiness certificate. No comments, review decisions, pipeline results, or full-file contents are implied by this contract.
