# Maintainer Checklist

Before publishing a schema update:

1. Update `vault-schema.json`; run `make generate` to refresh the legacy YAML export and generated artifacts.
2. Update `life-os-schema.md` and `templates/` when the contract changed.
3. Update `versions.json`.
4. Update `CHANGELOG.md`.
5. Run `make check`.
6. Verify no private vault notes, exports, indexes, databases, caches, or attachments are tracked.
7. Commit and push.
8. Create/update the matching GitHub release if the schema version changed.
