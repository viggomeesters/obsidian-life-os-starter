# Architecture

`vault-schema` is intentionally small and static.

## Layers

1. **Contract** — `vault-schema.json` defines note types, fields, enums, canonical locations, intake rules, anchors, filename patterns, and database-column hints.
2. **Legacy/prose surfaces** — `life-os-schema.yaml` is generated for compatibility; `life-os-schema.md` explains the same model for humans.
3. **Templates** — `templates/` contains reusable public-safe templates mirrored from the vault contract.
4. **Examples** — `examples/` contains synthetic public-safe note fixtures, one per type.
5. **Generated artifacts** — `dist/vault-schema.schema.json`, `docs/generated-schema-reference.md`, and `site/` are generated from the canonical JSON source.
6. **Guard** — `scripts/validate_repository.py` and `scripts/validate_examples.py` check identity, version alignment, schema semantics, template coverage, examples, public-safety boundaries, checksums, and required repo-complete files.

## Non-goals

- No private vault data.
- No runtime database.
- No generated vector/index artifacts.
- No dynamic hosted app; GitHub Pages serves static generated docs from `main:/docs` only.

## Release unit

Schema version `9.4.1` is the contract version. Repository releases should normally use `v9.4.1` when the public mirror is updated.
