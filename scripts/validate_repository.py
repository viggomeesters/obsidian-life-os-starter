#!/usr/bin/env python3
"""Validate the vault-schema repository completeness and public-safety guardrails."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "life-os-schema.yaml",
    "life-os-schema.md",
    "versions.json",
    "Makefile",
    "AGENTS.md",
    ".editorconfig",
    "assets/vault-schema-hero.svg",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
    "docs/REPO_COMPLETE.md",
    "docs/MAINTAINER_CHECKLIST.md",
    "docs/PACKAGE.md",
    "docs/HERO_GUIDELINES.md",
    "CONTRIBUTORS.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "SECURITY.md",
    "NOTICE.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/config.yml",
]
BLOCKED_PATHS = [".go-workflow", "go_workflow", "tasks.md"]
BLOCKED_CONTENT = [
    "This repo has been consolidated into",
    "Archived",
    "agent-brain/context/schema",
]
PRIVATE_ARTIFACT_SUFFIXES = {".sqlite", ".db", ".duckdb", ".parquet", ".mbox"}
PRIVATE_ARTIFACT_NAMES = {"telegram-export", "gmail-export", "imap-cache", "vault-index"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    for blocked in BLOCKED_PATHS:
        if (ROOT / blocked).exists():
            fail(f"blocked repo-local workflow artifact present: {blocked}")

    schema = yaml.safe_load((ROOT / "life-os-schema.yaml").read_text(encoding="utf-8"))
    versions = json.loads((ROOT / "versions.json").read_text(encoding="utf-8"))
    if str(schema.get("version")) != versions.get("version"):
        fail("versions.json version does not match life-os-schema.yaml")
    if len(schema.get("types", {}) or {}) != versions.get("types"):
        fail("versions.json type count does not match schema types")
    if len(schema.get("types", {}) or {}) < 10:
        fail("schema unexpectedly has fewer than 10 note types")
    if "note_intake" not in schema:
        fail("schema missing note_intake contract")
    if "anchor_contract" not in schema:
        fail("schema missing anchor_contract")
    if "project_slug" not in (schema.get("context_fields") or {}):
        fail("schema missing project_slug provenance/context field")

    template_files = [p for p in (ROOT / "templates").rglob("*") if p.is_file()]
    if len(template_files) != versions.get("templates"):
        fail(f"template count mismatch: found {len(template_files)}, expected {versions.get('templates')}")
    if len(template_files) < 15:
        fail("too few templates copied")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in BLOCKED_CONTENT:
        if needle in readme:
            fail(f"README still contains old archive/consolidation wording: {needle}")
    if "https://github.com/viggomeesters/vault-schema" not in readme:
        fail("README does not point to canonical vault-schema repo")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in PRIVATE_ARTIFACT_SUFFIXES:
            fail(f"private/runtime artifact should not be tracked: {path.relative_to(ROOT)}")
        lowered = str(path.relative_to(ROOT)).lower()
        if any(name in lowered for name in PRIVATE_ARTIFACT_NAMES):
            fail(f"private export/index-like artifact path present: {path.relative_to(ROOT)}")

    print(
        "OK: vault-schema repository validated "
        f"(schema v{schema.get('version')}, {len(schema.get('types', {}) or {})} types, {len(template_files)} templates)"
    )


if __name__ == "__main__":
    main()
