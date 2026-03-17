# Life OS Schema

The data model for Life OS — a structured Obsidian vault system.

This repo contains the **schema specification** and **frontmatter templates** for all 11 note types. It is the single source of truth for how notes are structured, categorized, and linked.

## What's Here

```
life-os-schema/
├── life-os-schema.md   # Full schema specification (v8.5)
├── CHANGELOG.md        # Version history
└── templates/          # Frontmatter templates for all note types
    ├── task.md
    ├── entity.md
    ├── project.md
    ├── interaction.md
    ├── note.md
    ├── daily.md
    ├── weekly.md
    ├── bookmark.md
    ├── resource.md
    ├── media.md
    ├── purchase.md
    ├── anniversary.md
    ├── migraine.md
    ├── decision.md
    └── chore.md
```

## 11 Note Types

| Type | Purpose | Categories |
|------|---------|------------|
| `entity` | People, companies, products, places | person, pet, company, product, place |
| `interaction` | Logged contacts with entities | call, irl, chat, mail, letter |
| `purchase` | Items bought with amount tracking | electronics, appliances, furniture, ... |
| `anniversary` | Recurring dates | verjaardag, verkering, getrouwd, ... |
| `health` | Health tracking | migraine, weight, bloodpressure, nutrition, ... |
| `entry` | Journals, notes, reflections | daily, weekly, yearly, note, reflection |
| `task` | Actions to complete | people, money, screen, hands |
| `project` | Task containers | personal, client, internal |
| `reference` | Bookmarks, books, media | bookmark, article, book, movie, video, ... |
| `chore` | Recurring household tasks | schoonmaken, onderhoud, administratie, ... |
| `context` | Personal background docs | (freeform) |

## Quick Reference

**Core fields** (all types): `type`, `category`, `created`, `slug`, `timestamp`

**Context fields** (recommended): `area`, `project`, `entity`, `topics`

**Areas**: `work`, `home`, `self`, `social`

**Statuses** (tasks/projects only): `to-do`, `in progress`, `waiting`, `done`, `backlog`, `cancelled`

## Related

- **[life-os-starter](https://github.com/viggomeesters/life-os-starter)** — Plug & play Obsidian vault with AI agent support (simplified 5-type version)

## License

MIT
