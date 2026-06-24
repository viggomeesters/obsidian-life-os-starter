#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = yaml.safe_load((ROOT / "life-os-schema.yaml").read_text(encoding="utf-8"))
REQUIRED = set(SCHEMA["anchor_contract"]["new_or_changed_notes"]["required_fields"])
REQUIRED_TYPES = set(SCHEMA["types"].keys())
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TS_RE = re.compile(r"^\d{8}-\d{4}$")

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} missing frontmatter")
    try:
        raw = text.split("---\n", 2)[1]
    except IndexError:
        fail(f"{path.relative_to(ROOT)} malformed frontmatter")
    return yaml.safe_load(raw) or {}

def main() -> None:
    seen = set()
    for path in sorted((ROOT / "examples").glob("*.md")):
        fm = frontmatter(path)
        note_type = fm.get("type")
        seen.add(note_type)
        missing = REQUIRED - set(fm)
        if missing:
            fail(f"{path.name} missing required fields: {sorted(missing)}")
        if note_type not in REQUIRED_TYPES:
            fail(f"{path.name} has unknown type {note_type!r}")
        type_spec = SCHEMA["types"][note_type]
        if fm.get("category") not in (type_spec.get("categories") or {}):
            fail(f"{path.name} category {fm.get('category')!r} not allowed for {note_type}")
        allowed = (SCHEMA.get("type_category_area", {}).get(note_type, {}).get(fm.get("category"), {}).get("allowed_areas") or [])
        if allowed and fm.get("area") not in allowed:
            fail(f"{path.name} area {fm.get('area')!r} not allowed for {note_type}/{fm.get('category')}")
        if not DATE_RE.match(str(fm.get("created"))):
            fail(f"{path.name} created is not YYYY-MM-DD")
        if not TS_RE.match(str(fm.get("timestamp"))):
            fail(f"{path.name} timestamp is not YYYYMMDD-HHmm")
        if not isinstance(fm.get("topics"), list) or not fm["topics"]:
            fail(f"{path.name} topics must be non-empty list")
    missing_types = REQUIRED_TYPES - seen
    if missing_types:
        fail(f"missing examples for types: {sorted(missing_types)}")
    print(f"OK: validated {len(seen)} synthetic examples")

if __name__ == "__main__":
    main()
