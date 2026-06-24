#!/usr/bin/env python3
"""Validate the vault-schema repository completeness, schema semantics, and public-safety guardrails."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md", "LICENSE", "vault-schema.json", "schema/vault-schema.contract.schema.json", "life-os-schema.yaml", "life-os-schema.md", "versions.json", "Makefile",
    "requirements.txt", "AGENTS.md", ".editorconfig", "assets/vault-schema-hero.svg",
    "docs/ARCHITECTURE.md", "docs/ROADMAP.md", "docs/REPO_COMPLETE.md", "docs/MAINTAINER_CHECKLIST.md",
    "docs/PACKAGE.md", "docs/HERO_GUIDELINES.md", "docs/generated-schema-reference.md",
    "docs/compatibility/v9.4.1.md", "CONTRIBUTORS.md", "CODE_OF_CONDUCT.md", "SUPPORT.md", "SECURITY.md", "NOTICE.md",
    ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/config.yml",
    "dist/vault-schema.schema.json", "dist/checksums.txt", "site/index.html", "site/vault-schema.schema.json", "docs/index.html", "docs/vault-schema.schema.json",
    "scripts/validate_note.py", "scripts/diff_schema_compatibility.py",
]
BLOCKED_PATHS = [".go-workflow", "go_workflow", "tasks.md"]
BLOCKED_CONTENT = ["This repo has been consolidated into", "Archived", "agent-brain/context/schema"]
PRIVATE_ARTIFACT_SUFFIXES = {".sqlite", ".db", ".duckdb", ".parquet", ".mbox"}
PRIVATE_ARTIFACT_NAMES = {"telegram-export", "gmail-export", "imap-cache", "vault-index"}
PRIVATE_PATH_PATTERNS = ["/Users/viggomeesters", "/mnt/c/Users/Viggo", "iCloud~md~obsidian", "Syncthing/vault"]
PRIVATE_PATH_ALLOWLIST = {"scripts/validate_repository.py"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def is_under_declared_folder(location: str, folders: dict, subfolders: dict) -> bool:
    normalized = location.replace("{YYYY-MM}", "2026-06")
    candidates = list(folders.keys()) + list(subfolders.values())
    return any(normalized.startswith(candidate) for candidate in candidates)


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")
    for blocked in BLOCKED_PATHS:
        if (ROOT / blocked).exists():
            fail(f"blocked repo-local workflow artifact present: {blocked}")

    schema = read_json(ROOT / "vault-schema.json")
    contract_meta_schema = read_json(ROOT / "schema" / "vault-schema.contract.schema.json")
    meta_errors = sorted(Draft202012Validator(contract_meta_schema).iter_errors(schema), key=lambda e: list(e.path))
    if meta_errors:
        first = meta_errors[0]
        loc = ".".join(str(p) for p in first.path) or "<root>"
        fail(f"vault-schema.json fails contract meta-schema at {loc}: {first.message}")
    versions = json.loads((ROOT / "versions.json").read_text(encoding="utf-8"))
    if str(schema.get("version")) != versions.get("version"):
        fail("versions.json version does not match vault-schema.json")
    if len(schema.get("types", {}) or {}) != versions.get("types"):
        fail("versions.json type count does not match schema types")
    prose_first_line = (ROOT / "life-os-schema.md").read_text(encoding="utf-8").splitlines()[0]
    if f"v{schema.get('version')}" not in prose_first_line:
        fail("life-os-schema.md title version does not match vault-schema.json")
    schema_hash = hashlib.sha256((ROOT / "vault-schema.json").read_bytes()).hexdigest()
    if versions.get("schema_sha256") != schema_hash:
        fail("versions.json schema_sha256 does not match vault-schema.json")
    legacy_yaml = read_yaml(ROOT / "life-os-schema.yaml")
    if legacy_yaml != schema:
        fail("legacy life-os-schema.yaml drifted from canonical vault-schema.json; run make generate")
    legacy_hash = hashlib.sha256((ROOT / "life-os-schema.yaml").read_bytes()).hexdigest()
    if versions.get("legacy_yaml_sha256") != legacy_hash:
        fail("versions.json legacy_yaml_sha256 does not match generated life-os-schema.yaml")

    folders = schema.get("folders") or {}
    subfolders = folders.get("system/", {}).get("subfolders") or {}
    if "00_inbox/" not in folders or folders["00_inbox/"].get("lifecycle") != "legacy_quarantine":
        fail("00_inbox must be declared as legacy_quarantine")
    if "note_intake" not in schema or schema["note_intake"].get("default_creation_location") != "canonical":
        fail("schema missing canonical note_intake contract")
    if "anchor_contract" not in schema:
        fail("schema missing anchor_contract")
    for field in ("source", "source_id", "thread_id", "project_slug", "topics"):
        if field not in (schema.get("context_fields") or {}):
            fail(f"schema missing provenance/context field: {field}")

    type_names = set((schema.get("types") or {}).keys())
    matrix_names = set((schema.get("type_category_area") or {}).keys())
    if type_names != matrix_names:
        fail(f"type_category_area keys differ from types: {sorted(type_names ^ matrix_names)}")
    for note_type, spec in schema["types"].items():
        location = spec.get("location", "")
        filename = spec.get("filename", "")
        categories = set((spec.get("categories") or {}).keys())
        matrix_categories = set((schema["type_category_area"].get(note_type) or {}).keys())
        if not location.endswith("/") or not is_under_declared_folder(location, folders, subfolders):
            fail(f"type {note_type} location is outside declared folders: {location}")
        if not filename or filename.endswith("/") or " " in filename:
            fail(f"type {note_type} has invalid filename pattern: {filename}")
        if not categories:
            fail(f"type {note_type} has no categories")
        if categories != matrix_categories:
            fail(f"category matrix mismatch for {note_type}: {sorted(categories ^ matrix_categories)}")

    template_files = [p for p in (ROOT / "templates").rglob("*") if p.is_file()]
    if len(template_files) != versions.get("templates"):
        fail(f"template count mismatch: found {len(template_files)}, expected {versions.get('templates')}")
    if len(template_files) < 15:
        fail("too few templates copied")

    dist_schema = json.loads((ROOT / "dist" / "vault-schema.schema.json").read_text(encoding="utf-8"))
    if sorted(dist_schema.get("properties", {}).get("type", {}).get("enum", [])) != sorted(type_names):
        fail("JSON Schema type enum does not match canonical JSON types")
    if not dist_schema.get("allOf"):
        fail("JSON Schema export missing type/category conditional validation")
    # Prove conditional schema catches an impossible category for a known type.
    sample_type = sorted(type_names)[0]
    bad_note = {"type": sample_type, "category": "__invalid__"}
    if not list(Draft202012Validator(dist_schema).iter_errors(bad_note)):
        fail("JSON Schema conditional validation did not reject invalid type/category pair")

    checksums = (ROOT / "dist" / "checksums.txt").read_text(encoding="utf-8")
    for rel in ["vault-schema.json", "schema/vault-schema.contract.schema.json", "life-os-schema.yaml", "life-os-schema.md", "versions.json", "dist/vault-schema.schema.json", "dist/vault-schema-v9.4.1.zip"]:
        digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if f"{digest}  {rel}" not in checksums:
            fail(f"checksums.txt missing current digest for {rel}")

    sync_pairs = [
        ("site/index.html", "docs/index.html"),
        ("site/vault-schema.schema.json", "docs/vault-schema.schema.json"),
        ("site/generated-schema-reference.md", "docs/generated-schema-reference.md"),
    ]
    for left, right in sync_pairs:
        if (ROOT / left).read_bytes() != (ROOT / right).read_bytes():
            fail(f"generated Pages artifact drift: {left} != {right}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in BLOCKED_CONTENT:
        if needle in readme:
            fail(f"README still contains old archive/consolidation wording: {needle}")
    if "https://github.com/viggomeesters/vault-schema" not in readme:
        fail("README does not point to canonical vault-schema repo")
    if "https://viggomeesters.github.io/vault-schema/" not in readme:
        fail("README does not link GitHub Pages docs site")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or ".venv" in path.parts or "__pycache__" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in {".pyc", ".pyo"}:
            continue
        if path.suffix.lower() in PRIVATE_ARTIFACT_SUFFIXES:
            fail(f"private/runtime artifact should not be tracked: {path.relative_to(ROOT)}")
        rel = path.relative_to(ROOT).as_posix()
        lowered = rel.lower()
        if any(name in lowered for name in PRIVATE_ARTIFACT_NAMES):
            fail(f"private export/index-like artifact path present: {rel}")
        if rel not in PRIVATE_PATH_ALLOWLIST:
            file_text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in PRIVATE_PATH_PATTERNS:
                if pattern in file_text:
                    fail(f"private/local path pattern {pattern!r} present in {rel}")

    print(
        "OK: vault-schema repository validated "
        f"(schema v{schema.get('version')}, {len(type_names)} types, {len(template_files)} templates)"
    )


if __name__ == "__main__":
    main()
