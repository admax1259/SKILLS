"""Read GitHub/GitLab review diffs through an existing authenticated CLI."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote


def cli_get(provider, host, endpoint):
    command = ["gh" if provider == "github" else "glab", "api", "--hostname", host, endpoint]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=60)
    return json.loads(result.stdout)


def collect(provider, host, repo, number, get=None):
    if provider not in {"github", "gitlab"}:
        raise ValueError("Unsupported provider")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*(?::[0-9]+)?", host):
        raise ValueError("Specify a hostname, not a URL")
    if not repo or any(part in {"", ".", ".."} for part in repo.split("/")):
        raise ValueError("Invalid project path")
    if number < 1:
        raise ValueError("PR/MR number must be positive")
    get = get or (lambda endpoint: cli_get(provider, host, endpoint))

    def pages(endpoint):
        items = []
        for page in range(1, 101):
            batch = get(endpoint + "?per_page=100&page=" + str(page))
            if not isinstance(batch, list):
                raise ValueError("Expected a paginated list")
            items.extend(batch)
            if len(batch) < 100:
                return items
        raise ValueError("Pagination limit reached; refusing an incomplete snapshot")

    if provider == "github":
        if len(repo.split("/")) != 2:
            raise ValueError("GitHub repository must be owner/repo")
        endpoint = "repos/" + "/".join(quote(part, safe="") for part in repo.split("/")) + "/pulls/" + str(number)
        meta = get(endpoint)
        raw = pages(endpoint + "/files")
        head = meta["head"]["sha"]
        files = [{"path": item["filename"], "old_path": item.get("previous_filename"),
                  "patch": item.get("patch"), "status": item["status"]}
                 for item in raw]
        limits = ["Provider patches may omit binary or truncated content; file coverage is not full-content verification."]
        if len(files) != meta["changed_files"]:
            limits.append("Returned file count differs from PR changed_files.")
        latest_head = get(endpoint)["head"]["sha"]
        url = meta["html_url"]
    else:
        endpoint = "projects/" + quote(repo, safe="") + "/merge_requests/" + str(number)
        meta = get(endpoint)
        raw = pages(endpoint + "/diffs")
        head = meta["sha"]
        files = [{"path": item["new_path"], "old_path": item["old_path"],
                  "patch": item.get("diff"),
                  "incomplete": bool(item.get("collapsed") or item.get("too_large")),
                  "status": "renamed" if item.get("renamed_file") else
                            "added" if item.get("new_file") else
                            "deleted" if item.get("deleted_file") else "modified"}
                 for item in raw]
        limits = ["GitLab diff limits may omit files or content; inspect collapsed/too_large and source diffs."]
        count = str(meta.get("changes_count", ""))
        if count.isdigit() and int(count) != len(files):
            limits.append("Returned file count differs from MR changes_count.")
        latest_head = get(endpoint)["sha"]
        url = meta["web_url"]
    if head != latest_head:
        raise ValueError("Head changed during collection; recollect the snapshot")
    return {"provider": provider, "host": host, "repo": repo, "number": number,
            "title": meta["title"], "url": url, "head_sha": head,
            "files": files, "limitations": limits}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["github", "gitlab"], required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        snapshot = collect(args.provider, args.host, args.repo, args.number)
    except subprocess.CalledProcessError as error:
        # CLI stderr can contain private request details; leave it out of shared artifacts.
        raise SystemExit(f"Provider CLI failed (exit {error.returncode}); check host, login and access.") from None
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error)) from None
    args.output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
