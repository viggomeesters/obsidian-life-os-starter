#!/usr/bin/env python3
from pathlib import Path
import copy
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, str(ROOT / "scripts" / "validate_repository.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_examples.py")],
    [sys.executable, str(ROOT / "scripts" / "validate_note.py"), str(ROOT / "examples" / "entry.md")],
    [sys.executable, str(ROOT / "scripts" / "diff_schema_compatibility.py"), str(ROOT / "vault-schema.json"), str(ROOT / "vault-schema.json")],
]
for command in commands:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    print(result.stdout, end="")
    print(result.stderr, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
print("OK: repository test harness passed")


sys.path.insert(0, str(ROOT))
from scripts.diff_schema_compatibility import compare

schema = json.loads((ROOT / "vault-schema.json").read_text(encoding="utf-8"))
new = copy.deepcopy(schema)
new["core_fields"]["created"]["type"] = "number"
assert "changed field types" in compare(schema, new)["breaking"]

new = copy.deepcopy(schema)
new["context_fields"]["area"]["required_new"] = True
assert "newly required fields" in compare(schema, new)["breaking"]

new = copy.deepcopy(schema)
entry_daily = new["type_category_area"]["entry"]["daily"]
if len(entry_daily["allowed_areas"]) > 1:
    entry_daily["allowed_areas"] = entry_daily["allowed_areas"][:1]
else:
    entry_daily["allowed_areas"] = []
assert "narrowed allowed areas" in compare(schema, new)["breaking"]

print("OK: compatibility diff breaking-change regression passed")
