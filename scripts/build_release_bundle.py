#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SCHEMA = yaml.safe_load((ROOT / "life-os-schema.yaml").read_text(encoding="utf-8"))
VERSION = SCHEMA["version"]
FILES = [
    "README.md", "LICENSE", "life-os-schema.yaml", "life-os-schema.md", "versions.json",
    "dist/vault-schema.schema.json", "docs/generated-schema-reference.md", "docs/compatibility/v9.4.1.md",
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    DIST.mkdir(exist_ok=True)
    bundle = DIST / f"vault-schema-v{VERSION}.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in FILES:
            zf.write(ROOT / rel, rel)
        for path in sorted((ROOT / "templates").rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(ROOT).as_posix())
        for path in sorted((ROOT / "examples").rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(ROOT).as_posix())
    checksum_targets = FILES + [bundle.relative_to(ROOT).as_posix()]
    lines = [f"{sha(ROOT / rel)}  {rel}" for rel in checksum_targets]
    (DIST / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"built {bundle.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
