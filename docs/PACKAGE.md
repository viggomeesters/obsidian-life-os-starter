# Package / Distribution

This repo is a schema/reference artifact, not an installable application package.

Supported consumption modes:

- Git clone/submodule.
- Download `vault-schema.json` from a release tag; use `life-os-schema.yaml` only as the generated legacy export.
- Download `vault-schema-v9.4.1.zip` from the release assets.
- Fetch raw files from GitHub for automation.
- Use `dist/vault-schema.schema.json` or the Pages copy for note-frontmatter JSON Schema consumers.
- Use `schema/vault-schema.contract.schema.json` for validating the canonical contract itself.
- Use `scripts/validate_note.py` and `scripts/diff_schema_compatibility.py` from a clone or release bundle for local agent workflows.

Local verification:

```bash
make check
```

Generated release artifacts:

- `schema/vault-schema.contract.schema.json`
- `dist/vault-schema.schema.json`
- `scripts/validate_note.py`
- `scripts/diff_schema_compatibility.py`
- `dist/vault-schema-v9.4.1.zip`
- `dist/checksums.txt`
