# Repo-complete checklist

- [x] Standalone public identity: `viggomeesters/vault-schema`
- [x] Repo unarchived
- [x] README with hero, quick start, safety boundary, generated artifacts, and agent usage
- [x] Current machine-readable schema: `life-os-schema.yaml` v9.4.1
- [x] Prose companion: `life-os-schema.md`
- [x] Latest templates copied from the vault contract
- [x] Synthetic public-safe examples for every note type
- [x] Generated JSON Schema export in `dist/`
- [x] Generated Markdown reference in `docs/generated-schema-reference.md`
- [x] Release bundle + checksums in `dist/`
- [x] Compatibility report in `docs/compatibility/v9.4.1.md`
- [x] GitHub Pages static docs under `site/`
- [x] `AGENTS.md`
- [x] `Makefile` with `make check`
- [x] Hermetic dependency declaration via `requirements.txt`
- [x] Deterministic repository/schema/example guard
- [x] Pull request template and issue routing
- [x] Security/support/conduct/notice/contributor docs
- [x] Architecture/roadmap/package/maintainer/hero docs
- [x] GitHub Pages static docs served from `main:/docs` without Actions

Validation command:

```bash
make check
```
