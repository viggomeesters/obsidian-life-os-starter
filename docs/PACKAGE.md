# Package / Distribution

This repo is a schema/reference artifact, not an installable application package.

Supported consumption modes:

- Git clone/submodule.
- Download `vault-schema.json` from a release tag; use `life-os-schema.yaml` only as the generated legacy export.
- Download `vault-schema-v9.4.1.zip` from the release assets.
- Fetch raw files from GitHub for automation.
- Use `dist/vault-schema.schema.json` or the Pages copy for JSON Schema consumers.

Local verification:

```bash
make check
```

Generated release artifacts:

- `dist/vault-schema.schema.json`
- `dist/vault-schema-v9.4.1.zip`
- `dist/checksums.txt`
