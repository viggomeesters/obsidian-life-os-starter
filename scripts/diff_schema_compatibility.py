#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_schema(ref: str) -> dict:
    path = Path(ref)
    if path.exists():
        text = path.read_text(encoding="utf-8")
    elif ":" in ref:
        git_ref, rel = ref.split(":", 1)
        text = subprocess.check_output(["git", "show", f"{git_ref}:{rel}"], cwd=ROOT, text=True)
    else:
        raise SystemExit(f"schema reference not found: {ref}")
    if ref.endswith((".yaml", ".yml")):
        return yaml.safe_load(text)
    return json.loads(text)


def compare(old: dict, new: dict) -> dict:
    old_types = set((old.get("types") or {}).keys())
    new_types = set((new.get("types") or {}).keys())
    old_fields = set((old.get("core_fields") or {}).keys()) | set((old.get("context_fields") or {}).keys())
    new_fields = set((new.get("core_fields") or {}).keys()) | set((new.get("context_fields") or {}).keys())
    changed_locations = []
    changed_categories = []
    for t in sorted(old_types & new_types):
        if old["types"][t].get("location") != new["types"][t].get("location"):
            changed_locations.append({"type": t, "old": old["types"][t].get("location"), "new": new["types"][t].get("location")})
        old_cats = set((old["types"][t].get("categories") or {}).keys())
        new_cats = set((new["types"][t].get("categories") or {}).keys())
        if old_cats != new_cats:
            changed_categories.append({"type": t, "added": sorted(new_cats-old_cats), "removed": sorted(old_cats-new_cats)})
    breaking = []
    if old_types - new_types:
        breaking.append("removed note types")
    if old_fields - new_fields:
        breaking.append("removed fields")
    if changed_locations:
        breaking.append("changed canonical locations")
    if any(item["removed"] for item in changed_categories):
        breaking.append("removed categories")
    return {
        "old_version": old.get("version"),
        "new_version": new.get("version"),
        "breaking": breaking,
        "type_changes": {"added": sorted(new_types-old_types), "removed": sorted(old_types-new_types)},
        "field_changes": {"added": sorted(new_fields-old_fields), "removed": sorted(old_fields-new_fields)},
        "changed_locations": changed_locations,
        "changed_categories": changed_categories,
    }


def markdown(report: dict) -> str:
    lines = [f"# Compatibility Diff — {report['old_version']} → {report['new_version']}", ""]
    lines.append(f"Breaking: {'yes' if report['breaking'] else 'no'}")
    if report["breaking"]:
        lines += ["", "## Breaking signals"] + [f"- {x}" for x in report["breaking"]]
    for label, data in [("Type changes", report["type_changes"]), ("Field changes", report["field_changes"] )]:
        lines += ["", f"## {label}", f"- Added: {', '.join(data['added']) or 'none'}", f"- Removed: {', '.join(data['removed']) or 'none'}"]
    if report["changed_locations"]:
        lines += ["", "## Changed locations"] + [f"- `{x['type']}`: `{x['old']}` → `{x['new']}`" for x in report["changed_locations"]]
    if report["changed_categories"]:
        lines += ["", "## Changed categories"] + [f"- `{x['type']}`: added {x['added'] or 'none'}, removed {x['removed'] or 'none'}" for x in report["changed_categories"]]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Compare two vault schema contract files or git refs.")
    parser.add_argument("old")
    parser.add_argument("new")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args(argv)
    report = compare(read_schema(args.old), read_schema(args.new))
    if args.format == "markdown":
        print(markdown(report), end="")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
