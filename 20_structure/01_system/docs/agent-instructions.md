# Agent Instructions

Rules and common pitfalls for AI agents working in this vault.

> **Data model (types, categories, fields, templates, filenames):** see `life-os-schema.md`
> This document contains only **behavioral rules** and **pitfalls** -- no schema duplication.

---

## Quick Start

1. Read `CLAUDE.md` (vault root) for structure overview
2. Read `life-os-schema.md` for the complete data model (**Single Source of Truth**)
3. Check the project note in `02_context/projects/` if relevant
4. Execute task, commit with conventional commit message

---

## Vault Workflow

### Working on Vault Tasks
1. Read the relevant project note: `02_context/projects/YYYY-MM-slug.md`
2. Pick the topmost open task
3. Execute following schema conventions (read `life-os-schema.md`)
4. Commit with conventional commit message

---

## Self-Verification (Required for Bulk Edits)

After **every** bulk operation (5 or more files changed), **before** committing:

1. Run your vault verification checks
2. Fix all `[fail]` items
3. Review all `[warn]` items
4. Only then commit

### Manual Checks (not automatable)
- **Semantic correctness**: does the slug refer to what you think? (e.g., `acme-corp` = entity, `acme.com` = URL)
- **Deleted files**: are all wikilinks to deleted files updated?
- **Bulk find-replace**: spot-check 3 changed files and verify visually

---

## Vault Rules

### Do Not
- No subfolders in `10_notes/` or `90_attachments/`
- No absolute paths in links
- No empty notes
- No type/category in filenames (that belongs in frontmatter)
- **NEVER create a filename without YYYYMMDD-HHmm prefix in `10_notes/`!**

### Do
- **Filename format: `YYYYMMDD-HHmm-slug.md`** (CRITICAL - check this ALWAYS!)
- Check schema for valid types/categories
- Use kebab-case for slugs
- Update frontmatter when making changes
- WikiLinks only: `[[slug]]` -- no paths, no extensions
- **Gift ideas on entity notes** (`## Gift ideas`), not on anniversary notes -- ideas belong to the person, not a date

---

## Common Mistakes to Avoid

> This is the most important section -- these mistakes are made most frequently.

### Timestamp Format Errors

**Wrong:**
```yaml
timestamp: 2026-02-06-1327  # Dashes in date portion
timestamp: 20260206_1327    # Underscore
timestamp: 2026-02-06 13:27 # Space
```

**Correct:**
```yaml
timestamp: 20260206-1327    # YYYYMMDD-HHmm (no dashes in date!)
```

### Type in Filename

**Wrong:**
```
20260206-1327-task-fix-bug.md        # "task" in filename
20260206-1327-entry-note.md          # "entry" in filename
20260206-1327-interaction-call.md    # "interaction" in filename
```

**Correct:**
```
20260206-1327-fix-bug.md             # Type only in frontmatter
20260206-1327-note.md
20260206-1327-call-alex.md
```

### Invalid Category for Type

**Wrong:**
```yaml
type: entry
category: technical  # Not valid for entry
```

**Correct:** Check `life-os-schema.md` -> Categories per Type for valid options.

### Entity/Topics Not as Array

**Wrong:**
```yaml
entity: alex-johnson   # String instead of array
topics: security       # String instead of array
```

**Correct:**
```yaml
entity: [alex-johnson]   # Always array, even for single value
topics: [security, privacy]
```

### Filename Truncation on Long Slugs

**Wrong:**
```
# Slug: follow-up-analytics-connector-for-data-license
# File: 20260209-1713-follow-up-analytics-connector.md  <-- TRUNCATED!
```

**Correct:**
```
# Slug: follow-up-analytics-connector-for-data-license
# File: 20260209-1713-follow-up-analytics-connector-for-data-license.md
```

**Rule:** The filename must ALWAYS contain the FULL slug. Never truncate.

### Placeholder in WikiLinks

**Wrong:**
```markdown
[[temp-mail-note]]          # Placeholder not replaced!
Task: [[task-slug]]         # Without timestamp prefix
```

**Correct:**
```markdown
[[20260202-1200-mail-alex|Mail from Alex]]
Task: [[20260209-1025-book-hotel|Hotel booking]]
```

**Rule:** Never use placeholders. WikiLinks in `10_notes/` always WITH timestamp prefix and display text.

### WikiLink with Path or Extension

**Wrong:**
```markdown
[[10_notes/20260206-1327-note.md]]    # With path and extension
[[entity/alex-johnson]]               # With subfolder
```

**Correct:**
```markdown
[[20260206-1327-note]]                # Slug only
[[alex-johnson]]                      # Slug only
```

### Status on Non-Task Types

**Wrong:**
```yaml
type: entry
category: log
status: to-do     # Entry does not have status!
```

**Correct:** Status is only for `task` and `project` types. See schema.
