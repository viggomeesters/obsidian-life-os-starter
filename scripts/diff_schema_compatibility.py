#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json, subprocess
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


def all_fields(schema: dict) -> dict:
    fields = {}
    fields.update(schema.get("core_fields") or {})
    fields.update(schema.get("context_fields") or {})
    return fields


def required_new_fields(fields: dict) -> set[str]:
    return {name for name, spec in fields.items() if isinstance(spec, dict) and (spec.get("required") or spec.get("required_new"))}


def allowed_areas(schema: dict, note_type: str, category: str) -> set[str]:
    return set(((((schema.get("type_category_area") or {}).get(note_type) or {}).get(category) or {}).get("allowed_areas") or []))


def compare(old: dict, new: dict) -> dict:
    old_types = set((old.get("types") or {}).keys())
    new_types = set((new.get("types") or {}).keys())
    old_field_specs = all_fields(old)
    new_field_specs = all_fields(new)
    old_fields = set(old_field_specs)
    new_fields = set(new_field_specs)
    changed_locations = []
    changed_categories = []
    field_type_changes = []
    newly_required_fields = []
    narrowed_allowed_areas = []

    for field in sorted(old_fields & new_fields):
        old_type = old_field_specs[field].get("type") if isinstance(old_field_specs[field], dict) else None
        new_type = new_field_specs[field].get("type") if isinstance(new_field_specs[field], dict) else None
        if old_type != new_type:
            field_type_changes.append({"field": field, "old": old_type, "new": new_type})

    for field in sorted(required_new_fields(new_field_specs) - required_new_fields(old_field_specs)):
        newly_required_fields.append(field)

    for note_type in sorted(old_types & new_types):
        if old["types"][note_type].get("location") != new["types"][note_type].get("location"):
            changed_locations.append({"type": note_type, "old": old["types"][note_type].get("location"), "new": new["types"][note_type].get("location")})
        old_cats = set((old["types"][note_type].get("categories") or {}).keys())
        new_cats = set((new["types"][note_type].get("categories") or {}).keys())
        if old_cats != new_cats:
            changed_categories.append({"type": note_type, "added": sorted(new_cats - old_cats), "removed": sorted(old_cats - new_cats)})
        for category in sorted(old_cats & new_cats):
            old_areas = allowed_areas(old, note_type, category)
            new_areas = allowed_areas(new, note_type, category)
            removed = old_areas - new_areas
            if removed:
                narrowed_allowed_areas.append({
                    "type": note_type,
                    "category": category,
                    "removed": sorted(removed),
                    "old": sorted(old_areas),
                    "new": sorted(new_areas),
                })

    breaking = []
    if old_types - new_types:
        breaking.append("removed note types")
    if old_fields - new_fields:
        breaking.append("removed fields")
    if field_type_changes:
        breaking.append("changed field types")
    if newly_required_fields:
        breaking.append("newly required fields")
    if changed_locations:
        breaking.append("changed canonical locations")
    if any(item["removed"] for item in changed_categories):
        breaking.append("removed categories")
    if narrowed_allowed_areas:
        breaking.append("narrowed allowed areas")

    return {
        "old_version": old.get("version"),
        "new_version": new.get("version"),
        "breaking": breaking,
        "type_changes": {"added": sorted(new_types - old_types), "removed": sorted(old_types - new_types)},
        "field_changes": {"added": sorted(new_fields - old_fields), "removed": sorted(old_fields - new_fields)},
        "field_type_changes": field_type_changes,
        "newly_required_fields": newly_required_fields,
        "changed_locations": changed_locations,
        "changed_categories": changed_categories,
        "narrowed_allowed_areas": narrowed_allowed_areas,
    }


def markdown(report: dict) -> str:
    lines = [f"# Compatibility Diff — {report['old_version']} → {report['new_version']}", ""]
    lines.append(f"Breaking: {'yes' if report['breaking'] else 'no'}")
    if report["breaking"]:
        lines += ["", "## Breaking signals"] + [f"- {x}" for x in report["breaking"]]
    for label, data in [("Type changes", report["type_changes"]), ("Field changes", report["field_changes"] )]:
        lines += ["", f"## {label}", f"- Added: {', '.join(data['added']) or 'none'}", f"- Removed: {', '.join(data['removed']) or 'none'}"]
    if report["field_type_changes"]:
        lines += ["", "## Field type changes"] + [f"- `{x['field']}`: `{x['old']}` → `{x['new']}`" for x in report["field_type_changes"]]
    if report["newly_required_fields"]:
        lines += ["", "## Newly required fields"] + [f"- `{x}`" for x in report["newly_required_fields"]]
    if report["changed_locations"]:
        lines += ["", "## Changed locations"] + [f"- `{x['type']}`: `{x['old']}` → `{x['new']}`" for x in report["changed_locations"]]
    if report["changed_categories"]:
        lines += ["", "## Changed categories"] + [f"- `{x['type']}`: added {x['added'] or 'none'}, removed {x['removed'] or 'none'}" for x in report["changed_categories"]]
    if report["narrowed_allowed_areas"]:
        lines += ["", "## Narrowed allowed areas"] + [f"- `{x['type']}/{x['category']}`: removed {', '.join(x['removed'])}" for x in report["narrowed_allowed_areas"]]
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
