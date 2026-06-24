# Agent Instructions — vault-schema

This repository is the public schema mirror for the structured Obsidian vault contract.

## Source of truth

- `life-os-schema.yaml` is canonical.
- `life-os-schema.md` is explanatory prose.
- `templates/` contains public-safe reusable templates.
- The repository must never contain private vault notes, generated indexes, exports, databases, caches, or attachments.

## Required workflow

1. Inspect `git status --short --branch` before edits.
2. Keep edits scoped to schema/docs/templates/guards.
3. Run `make check` before finishing.
4. If changing schema semantics, update `versions.json`, `CHANGELOG.md`, and docs.
5. Do not add GitHub Actions unless explicitly requested; local `make check` is the gate.
