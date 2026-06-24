#!/usr/bin/env python3
from pathlib import Path
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
