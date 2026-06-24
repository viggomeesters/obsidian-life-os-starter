#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TS_RE = re.compile(r"^\d{8}-\d{4}$")


def load_schema() -> dict:
    return json.loads((ROOT / "vault-schema.json").read_text(encoding="utf-8"))


def load_json_schema() -> dict:
    return json.loads((ROOT / "dist" / "vault-schema.schema.json").read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter block")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("malformed YAML frontmatter block")
    return yaml.safe_load(parts[1]) or {}


def validate_frontmatter(fm: dict, contract: dict, json_schema: dict, source: str) -> list[str]:
    errors = []
    validator = Draft202012Validator(json_schema)
    for err in sorted(validator.iter_errors(fm), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{source}: JSON Schema {loc}: {err.message}")
    note_type = fm.get("type")
    category = fm.get("category")
    area = fm.get("area")
    if note_type not in contract.get("types", {}):
        errors.append(f"{source}: unknown type {note_type!r}")
        return errors
    type_spec = contract["types"][note_type]
    if category not in (type_spec.get("categories") or {}):
        errors.append(f"{source}: category {category!r} not allowed for type {note_type!r}")
    allowed_areas = (((contract.get("type_category_area") or {}).get(note_type) or {}).get(category) or {}).get("allowed_areas") or []
    if allowed_areas and area not in allowed_areas:
        errors.append(f"{source}: area {area!r} not allowed for {note_type}/{category}; expected one of {allowed_areas}")
    if "created" in fm and not DATE_RE.match(str(fm["created"])):
        errors.append(f"{source}: created must be YYYY-MM-DD")
    if "timestamp" in fm and not TS_RE.match(str(fm["timestamp"])):
        errors.append(f"{source}: timestamp must be YYYYMMDD-HHmm")
    if "topics" in fm and (not isinstance(fm["topics"], list) or not fm["topics"]):
        errors.append(f"{source}: topics must be a non-empty list")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate Markdown note frontmatter against vault-schema.json and the generated JSON Schema.")
    parser.add_argument("paths", nargs="+", help="Markdown note path(s) to validate")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation result")
    args = parser.parse_args(argv)
    contract = load_schema()
    json_schema = load_json_schema()
    results = []
    all_errors = []
    for raw in args.paths:
        path = Path(raw)
        try:
            fm = frontmatter(path)
            errors = validate_frontmatter(fm, contract, json_schema, str(path))
        except Exception as exc:
            errors = [f"{path}: {exc}"]
        results.append({"path": str(path), "ok": not errors, "errors": errors})
        all_errors.extend(errors)
    if args.json:
        print(json.dumps({"ok": not all_errors, "results": results}, indent=2, ensure_ascii=False))
    else:
        if all_errors:
            for err in all_errors:
                print(f"FAIL: {err}")
        else:
            print(f"OK: validated {len(results)} note(s)")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
