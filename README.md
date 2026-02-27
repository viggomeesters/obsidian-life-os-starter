# Life OS — Obsidian Starter Vault

A batteries-included [Obsidian](https://obsidian.md) vault template for organizing your entire life with structured notes, templates, and AI agent support.

Life OS gives you **12 note types**, **16 templates**, and a flat-file architecture that scales from a handful of notes to tens of thousands — all queryable, all linkable, no plugins required for the core workflow.

## Quick Start (5 minutes)

1. **Use this template** — click "Use this template" on GitHub, or clone/download the repo
2. **Open in Obsidian** — Open as vault: File → Open vault → Open folder as vault
3. **Install the Minimal theme** — Settings → Appearance → Themes → Browse → search "Minimal" → Install and Use
4. **Install community plugins** — Settings → Community Plugins → Turn on community plugins → Browse, then install these 10:

   | Plugin | Purpose |
   |--------|---------|
   | Templater | Dynamic templates with date logic |
   | Periodic Notes | Daily/weekly note generation |
   | Obsidian Git | Auto-commit vault to git |
   | Calendar | Calendar sidebar for daily notes |
   | Minimal Theme Settings | Fine-tune the Minimal theme |
   | Style Settings | CSS variable overrides |
   | Hider | Hide UI clutter |
   | Recent Files | Quick access to recent notes |
   | Iconize | Folder/file icons |
   | Settings Search | Search through settings |

5. **Enable all plugins** — Toggle each one on in Settings → Community Plugins
6. **Restart Obsidian** — Close and reopen to apply all configs
7. **Open the welcome note** — Read `20260101-0000-welcome.md` for a guided tour

> Configs for all 10 plugins are pre-set in `.obsidian/plugins/`. Once you install and enable them, everything works automatically.

## Folder Structure

```
vault/
├── 10_notes/              # All timestamped notes (flat)
├── 20_structure/
│   ├── 01_system/
│   │   ├── docs/          # Schema & agent instructions
│   │   └── templates/     # 16 note templates
│   └── 02_context/
│       ├── entity/        # People, companies, products
│       ├── projects/      # Active projects
│       ├── anniversaries/ # Birthdays, weddings
│       ├── chores/        # Recurring household tasks
│       ├── rituals/       # Recurring personal activities
│       └── self/          # Personal context docs
├── 90_attachments/        # Images, PDFs, files (flat)
├── CLAUDE.md              # AI agent instructions
└── README.md
```

**Why this structure?**
- `10_notes/` is flat — every timestamped note in one folder, discoverable by frontmatter
- `02_context/` holds reference documents that don't need timestamps
- No nested subfolders means simpler linking and faster search

## The 12 Note Types

| Type | Purpose | Location | Filename |
|------|---------|----------|----------|
| `entity` | People, companies, products | `02_context/entity/` | `john-doe.md` |
| `interaction` | Calls, meetings, chats | `10_notes/` | `20260102-0900-call-john.md` |
| `purchase` | Items bought with amount | `10_notes/` | `20260102-1400-keyboard.md` |
| `anniversary` | Recurring dates | `02_context/anniversaries/` | `03-15-birthday-john.md` |
| `health` | Migraine, weight, BP logs | `10_notes/` | `20260103-0800-headache.md` |
| `entry` | Daily journals, notes | `10_notes/` | `20260101-0600-daily.md` |
| `task` | Actions to complete | `10_notes/` | `20260101-1000-fix-bug.md` |
| `project` | Task containers | `02_context/projects/` | `2026-01-website.md` |
| `reference` | Bookmarks, books, media | `10_notes/` | `20260103-1200-docs.md` |
| `chore` | Recurring household tasks | `02_context/chores/` | `cleaning-7-bathroom.md` |
| `ritual` | Recurring personal activities | `02_context/rituals/` | `self-7-piano.md` |
| `context` | Personal background docs | `02_context/self/` | `health.md` |

Every note has YAML frontmatter with `type`, `category`, `slug`, and `timestamp`. This makes the vault fully queryable without folder hierarchy.

## Templates

16 templates in `20_structure/01_system/templates/`:

| Template | Type | Syntax |
|----------|------|--------|
| `daily.md` | Entry (daily) | Templater |
| `weekly.md` | Entry (weekly) | Templater |
| `migraine.md` | Health | Templater |
| `task.md` | Task | Placeholder |
| `entity.md` | Entity (person) | Placeholder |
| `project.md` | Project | Placeholder |
| `interaction.md` | Interaction | Placeholder |
| `bookmark.md` | Reference (bookmark) | Placeholder |
| `purchase.md` | Purchase | Placeholder |
| `anniversary.md` | Anniversary | Placeholder |
| `note.md` | Entry (note) | Placeholder |
| `decision.md` | Entry (decision) | Placeholder |
| `media.md` | Reference (book/media) | Placeholder |
| `resource.md` | Reference (guide) | Placeholder |
| `chore.md` | Chore | Placeholder |
| `ritual.md` | Ritual | Placeholder |

**Templater templates** use `<% %>` syntax for dynamic dates and interactive prompts.
**Placeholder templates** use `{{field}}` syntax for manual fill-in (works with any note creation tool).

### Using Templates

- **Alt+N** — Create new note from template
- **Alt+3** — Insert template into current note
- **Calendar sidebar** — Click a date to create a daily note (auto-applies template)

## Hotkeys

| Shortcut | Action |
|----------|--------|
| `Alt+N` | New note from template |
| `Alt+3` | Insert template |
| `Alt+P` | Command palette |
| `Alt+F` | Global search |
| `Alt+L` | Insert WikiLink |
| `Alt+R` | Move/rename file |
| `Alt+6` | Reveal in file explorer |
| `Alt+X` | Close other tabs |
| `Mod+W` | Close tab |
| `Mod+T` | New tab |
| `Mod+F` | Find in file |
| `Mod+Shift+F` | Find and replace |
| `Mod+Shift+C` | Copy Obsidian URL |
| `F2` | Rename file |

## Key Conventions

### Filenames
- Notes in `10_notes/`: `YYYYMMDD-HHmm-slug.md` (e.g., `20260215-1400-call-john.md`)
- Context docs: slug only (e.g., `john-doe.md`, `cleaning-7-bathroom.md`)

### Links
- Always WikiLinks: `[[slug]]` or `[[slug|Display text]]`
- No paths, no extensions: `[[john-doe]]` not `[[entity/john-doe.md]]`

### Frontmatter
- `entity` and `topics` always as arrays: `entity: [john-doe]`
- `status` only on `task` and `project` types
- `timestamp` format: `YYYYMMDD-HHmm` (no dashes in date)

### Task Status

Tasks use `##` headers for a status timeline:

```markdown
## to-do - 01 Jan 2026 at 10:00
Created the task

## in progress - 02 Jan 2026 at 09:30
Started working on it
```

The last `##` header is the current status.

## AI Agent Setup

This vault includes `CLAUDE.md` with instructions for AI coding assistants (Claude Code, GitHub Copilot, Cursor, etc.). The instructions teach agents how to:

- Create notes with correct frontmatter and filenames
- Use WikiLinks properly
- Respect the 12-type schema
- Avoid common mistakes

To use with **Claude Code**: just open the vault directory — Claude reads `CLAUDE.md` automatically.

For full schema documentation, see `20_structure/01_system/docs/life-os-schema.md`.

## Customization

### Adding your own context
1. Create entities in `02_context/entity/` for your contacts
2. Add projects in `02_context/projects/`
3. Fill in `02_context/self/` docs with your personal context
4. Delete example notes when you're comfortable with the structure

### Changing the theme
The vault ships with Minimal theme (dark mode, accent `#31addd`). Change in:
- Settings → Appearance (theme, dark/light mode)
- Settings → Minimal Theme Settings (typography, colors)
- Settings → Style Settings (CSS variables)

### Adding more templates
Create new `.md` files in `20_structure/01_system/templates/`. Use Templater syntax for dynamic content or `{{placeholders}}` for manual fill.

### Extending the schema
The schema in `life-os-schema.md` is a living document. Add new categories to existing types or create new context document types as needed.

## FAQ

**Do I need all 10 plugins?**
Only Templater and Periodic Notes are essential for template-based workflows. The rest enhance the experience but are optional.

**Can I use Dataview?**
Absolutely. The structured frontmatter is designed to be queryable. Dataview, DB Folder, or any metadata-based plugin will work great with this schema.

**What about mobile?**
The vault works on Obsidian Mobile. Install the same plugins and the configs will sync via your preferred method (git, iCloud, Syncthing).

**How do I back up?**
The included Obsidian Git plugin auto-commits every 10 minutes. Push is disabled by default — enable it in plugin settings when you've set up a remote.

**Can I change the folder names?**
Yes, but update the paths in:
- `.obsidian/app.json` (`newFileFolderPath`, `attachmentFolderPath`)
- `.obsidian/plugins/periodic-notes/data.json` (`folder`)
- `.obsidian/plugins/templater-obsidian/data.json` (`templates_folder`)
- `CLAUDE.md` (agent instructions)

## License

MIT — use it however you want.
