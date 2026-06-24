# Architecture

`vault-schema` is intentionally small and static.

## Layers

1. **Contract** — `life-os-schema.yaml` defines note types, fields, enums, canonical locations, intake rules, anchors, filename patterns, and database-column hints.
2. **Prose companion** — `life-os-schema.md` explains the same model for humans.
3. **Templates** — `templates/` contains reusable public-safe templates mirrored from the vault contract.
4. **Guard** — `scripts/validate_repository.py` checks identity, version alignment, template coverage, public-safety boundaries, and required repo-complete files.

## Non-goals

- No private vault data.
- No runtime database.
- No generated vector/index artifacts.
- No hosted app.
- No default GitHub Actions; local validation is `make check`.

## Release unit

Schema version `9.4.1` is the contract version. Repository releases should normally use `v9.4.1` when the public mirror is updated.
