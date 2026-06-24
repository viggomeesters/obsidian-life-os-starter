# Roadmap

## Now

- Keep the public repository aligned with the latest vault schema contract.
- Keep `make check` deterministic via repo-local `.venv` + `requirements.txt`.
- Preserve the public/private boundary.
- Keep generated JSON Schema, examples, checksums, and docs site in sync.

## Next

- Expand JSON Schema with type/category-specific conditional requirements.
- Add a semantic note validator CLI for downstream agents and Obsidian tooling.
- Add a compatibility diff generator between two tagged schema versions.

## Later

- Add a public-safe migration guide for older vault layouts.
- Publish a tiny package only if downstream projects need versioned dependency consumption.
