"""Assemble an offline review page from a provider-neutral JSON snapshot."""
import argparse
import html
import json
import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


def render(snapshot):
    def escape(value):
        return html.escape(str(value), quote=True)

    body = ['<header class="header"><h1>' + escape(snapshot["title"]) + "</h1>",
            "<p>" + escape(snapshot.get("url", "")) + "</p>",
            "<p>Head: " + escape(snapshot["head_sha"]) + "</p></header>",
            '<main class="content"><div class="summary">' +
            escape(snapshot.get("summary", "Read the complete available diff below.")) + "</div>"]
    limitations = snapshot.get("limitations", [])
    if limitations:
        body.append('<section class="summary"><strong>Coverage limits</strong><ul>' +
                    "".join("<li>" + escape(item) + "</li>" for item in limitations) + "</ul></section>")
    patches = {}
    for index, file in enumerate(snapshot["files"]):
        key = str(index)
        patch = file.get("patch")
        patches[key] = patch
        body.append('<details class="file-card" open><summary class="file-hdr">' +
                    escape(file["path"]) + '</summary><div class="file-note">' +
                    escape(file.get("note", "")) + "</div>")
        if patch is None or patch == "" or file.get("incomplete"):
            body.append('<p class="file-note">Patch unavailable or incomplete; inspect the source diff.</p>')
        body.append('<div data-diff="' + key + '"></div></details>')
    body.append("</main>")
    payload = json.dumps(patches, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    substitutions = {
        "/* INJECT_CSS */": (SKILL / "styles.css").read_text(encoding="utf-8"),
        "/* INJECT_JS */": (SKILL / "renderer.js").read_text(encoding="utf-8"),
        "<!-- INJECT_BODY -->": "\n".join(body),
        '{"__PR_DIFFS_PLACEHOLDER__":true}': payload,
    }
    # Single substitution pass: untrusted text resembling a template marker stays literal.
    pattern = "|".join(re.escape(key) for key in substitutions)
    return re.sub(pattern, lambda match: substitutions[match.group()], (SKILL / "template.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = render(json.loads(args.snapshot.read_text(encoding="utf-8")))
    args.output.write_text(result, encoding="utf-8")
    print(args.output)
