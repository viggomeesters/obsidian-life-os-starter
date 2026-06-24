# Roadmap

## Now

- Keep the public repository aligned with the latest vault schema contract.
- Keep `make check` deterministic via repo-local `.venv` + `requirements.txt`.
- Preserve the public/private boundary.
- Keep generated JSON Schema, examples, checksums, and docs site in sync.

## Done in v9.4.1 hardening

- Added contract meta-schema for canonical `vault-schema.json`.
- Expanded generated JSON Schema with type/category/area conditional requirements.
- Added semantic note validator CLI for downstream agents and Obsidian tooling.
- Added compatibility diff generator for schema files and `git-ref:path` inputs.

## Next

- Add real downstream consumer fixtures once a non-public vault or agent repo starts consuming this package directly.

## Later

- Add a public-safe migration guide for older vault layouts.
