"""Render the bilingual skill index from catalog.json; --check detects drift."""
import argparse
from validate import ROOT, validate

LABELS = {"design": "界面设计 / Interface design", "engineering": "工程设计 / Engineering", "productivity": "生产力 / Productivity", "visualization": "可视化 / Visualization", "verification": "验证 / Verification",
          "code-review": "代码审查 / Code review", "code-quality": "代码质量 / Code quality",
          "delivery": "交付与 CI / Delivery & CI", "knowledge": "知识与复盘 / Knowledge"}
STATUS = {"ready": "可打包 / Ready", "review-needed": "待适配 / Review needed", "deprecated": "已弃用 / Deprecated"}


def render(root=ROOT):
    _, catalog = validate(root)
    lines = ["# 技能目录 / Skill catalog", "",
             "由 catalog.json 生成；编辑索引数据后运行 python3 scripts/catalog.py。",
             "Generated from catalog.json; edit catalog data, then regenerate.", "",
             "Ready means eligible for packaging, not verified on every engine. / 可打包不代表所有引擎均已实测。", ""]
    for category in catalog["categories"]:
        lines += ["## " + LABELS[category], "",
                  "| Skill | 来源 / Source | 状态 / Status |", "|---|---|---|"]
        for entry in sorted(catalog["skills"], key=lambda e: e["id"]):
            if entry["category"] != category:
                continue
            name, source = entry["id"], entry["source"]
            lines.append(f"| [{name}](../skills/{name}/SKILL.md) | [{source}](../sources/{source}.json) | {STATUS[entry['status']]} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    destination = ROOT / "docs/CATALOG.md"
    if args.check:
        if not destination.exists() or destination.read_text(encoding="utf-8") != expected:
            raise SystemExit("Catalog index is stale; run python3 scripts/catalog.py")
        print("Catalog index is current")
    else:
        destination.write_text(expected, encoding="utf-8")
        print(destination)
