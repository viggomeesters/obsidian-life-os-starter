# Agent Instructions — vault-schema

This repository is the public schema mirror for the structured Obsidian vault contract.

## Source of truth

- `life-os-schema.yaml` is canonical.
- `life-os-schema.md` is explanatory prose.
- `templates/` contains public-safe reusable templates.
- `examples/` contains synthetic fixtures only; never infer or add private vault data.
- `dist/`, `docs/generated-schema-reference.md`, and `site/` are generated artifacts from the YAML contract.
- The repository must never contain private vault notes, generated indexes, exports, databases, caches, or attachments.

## Required workflow

1. Inspect `git status --short --branch` before edits.
2. Keep edits scoped to schema/docs/templates/examples/guards/generated artifacts.
3. Run `make check` before finishing.
4. If changing schema semantics, update `versions.json`, `CHANGELOG.md`, compatibility docs, and generated artifacts.
5. GitHub Actions are present only for explicitly requested GitHub Pages publishing; local `make check` remains the main repo-complete gate.
