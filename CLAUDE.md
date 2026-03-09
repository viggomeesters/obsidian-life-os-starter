# Life OS Vault — Agent Instructions

> This vault uses Life OS v8.4 Read the schema before making changes.

## Schema & Rules

@20_structure/01_system/docs/life-os-schema.md
@20_structure/01_system/docs/agent-instructions.md

## Vault Path

`[UPDATE: /path/to/your/vault]`

## Structure

- `10_notes/` → timestamped notes (flat, no subfolders)
- `20_structure/01_system/docs/` → schema, conventions, agent instructions
- `20_structure/01_system/templates/` → note templates
- `20_structure/02_context/` → entities, projects, anniversaries, chores, self
- `90_attachments/` → files (flat, no subfolders)

## Critical Rules

### Filenames

- `10_notes/` format: `YYYYMMDD-HHmm-slug.md` (always with timestamp prefix)
- `02_context/` files: no timestamp, only slug (e.g., `john-doe.md`)
- Chores: `{category}-{frequency}-{slug}.md` (e.g., `cleaning-7-bathroom.md`)
- Anniversaries: `{MM-DD}-{category}-{entity}.md` (e.g., `01-15-birthday-john-doe.md`)
- No type/category in filename (type belongs in frontmatter)
- Slug always kebab-case, never truncate long names

### Slugs

- `10_notes/` slugs: `slug: 20260212-1000-my-note` (with timestamp, matches filename without `.md`)
- `02_context/` slugs: `slug: john-doe` (without timestamp)

### Links

- WikiLinks only: `[[slug]]` or `[[slug|Display text]]`
- No paths and no extensions: use `[[john-doe]]`, not `[[entity/john-doe.md]]`
- No markdown links for internal links
- No placeholders: always use real slugs, with timestamp for `10_notes`

### Frontmatter

- `entity` always as array: `entity: [john-doe]` (even for single value)
- `topics` always as array: `topics: [python, automation]`
- `status` only for `task` and `project` types
- `timestamp` format: `YYYYMMDD-HHmm` (no dashes in date part)

### Content

- Use WikiLinks with display text for readability: `[[slug|Readable title]]`

## 11 Types (Quick Reference)

| Type | Location | Example |
|------|----------|---------|
| `entity` | `02_context/entity/` | `john-doe.md` |
| `interaction` | `10_notes/` | `20260215-1400-call-john.md` |
| `purchase` | `10_notes/` | `20260215-1500-mechanical-keyboard.md` |
| `anniversary` | `02_context/anniversaries/` | `01-15-birthday-john-doe.md` |
| `health` | `10_notes/` | `20260215-0800-headache.md` |
| `entry` | `10_notes/` | `20260215-0600-daily.md` |
| `task` | `10_notes/` | `20260215-1000-fix-login-bug.md` |
| `project` | `02_context/projects/` | `2026-01-personal-website.md` |
| `reference` | `10_notes/` | `20260215-1200-article-rag.md` |
| `chore` | `02_context/chores/` | `cleaning-7-bathroom.md` |
| `context` | `02_context/self/` | `health.md` |

For all categories, fields, and templates: read `life-os-schema.md`.

## Task Status Headers

Tasks use `##` headers for status timeline (newest = last = current status):

```
## to-do - 19 Jan 2026 at 17:31
Created

## in progress - 20 Jan 2026 at 09:15
Started working on it
```

## Chore/Ritual Completion Headers

```
## done 2026-01-29 - person-name (30 min)
Optional note
```

## Context Routing (Self-Context Docs)

| Topic | File | Contains |
|-------|------|----------|
| **Health** | `[[health]]` | Medical history, medications, tracking |
| **Preferences** | `[[preferences]]` | Sizes, dietary, comfort, brands |
| **Navigation** | `[[index]]` | Links to all context docs |

## Git

- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Commit after completing tasks
- No `--force` or `--no-verify`
