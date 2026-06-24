#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SCHEMA = json.loads((ROOT / "vault-schema.json").read_text(encoding="utf-8"))
VERSION = SCHEMA["version"]
FILES = [
    "README.md", "CHANGELOG.md", "LICENSE", "requirements.txt", "vault-schema.json", "schema/vault-schema.contract.schema.json", "life-os-schema.yaml", "life-os-schema.md", "versions.json",
    "dist/vault-schema.schema.json", "docs/generated-schema-reference.md", "docs/compatibility/v9.4.1.md",
    "scripts/validate_note.py", "scripts/diff_schema_compatibility.py",
]
FIXED_ZIP_DATE = (2026, 1, 1, 0, 0, 0)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_deterministic(zf: zipfile.ZipFile, rel: str) -> None:
    path = ROOT / rel
    info = zipfile.ZipInfo(rel, date_time=FIXED_ZIP_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, path.read_bytes())


def release_file_list() -> list[str]:
    files = list(FILES)
    files.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "templates").rglob("*")) if p.is_file())
    files.extend(p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "examples").rglob("*")) if p.is_file())
    return sorted(dict.fromkeys(files))


def main() -> None:
    DIST.mkdir(exist_ok=True)
    bundle = DIST / f"vault-schema-v{VERSION}.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in release_file_list():
            write_deterministic(zf, rel)
    checksum_targets = FILES + ["dist/vault-schema.schema.json", bundle.relative_to(ROOT).as_posix()]
    checksum_targets = sorted(dict.fromkeys(checksum_targets))
    lines = [f"{sha(ROOT / rel)}  {rel}" for rel in checksum_targets]
    (DIST / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"built {bundle.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
