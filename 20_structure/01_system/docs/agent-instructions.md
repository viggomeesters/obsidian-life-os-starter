# Agent Instructions

Regels en veelgemaakte fouten voor AI agents werkend in deze vault.

> **Data model (types, categories, fields, templates, filenames):** zie `life-os-schema.md`
> Dit document bevat alleen **gedragsregels** en **pitfalls** — geen schema-duplicatie.

---

## Quick Start

1. Lees `CLAUDE.md` (vault root) voor structuur overzicht
2. Lees `life-os-schema.md` voor het volledige data model (**Single Source of Truth**)
3. Check project note in `02_context/projects/` als relevant
4. Voer taak uit, log resultaat, commit

---

## Vault Workflow

### Bij Vault Taken
1. Lees relevante project note: `02_context/projects/YYYY-MM-slug.md`
2. Pak topmost open task
3. Voer uit volgens schema conventies (lees `life-os-schema.md`)
4. Log resultaat in session logs
5. Commit met conventional commit message

---

## Self-Verification (Verplicht bij Bulk Edits)

Na **elke** bulk-operatie (≥5 bestanden gewijzigd), **voor** commit:

1. Draai `[YOUR_SCRIPTS_PATH]`
2. Fix alle `[fail]` items
3. Review alle `[warn]` items
4. Pas dan committen

### Handmatige checks (niet scriptbaar)
- **Semantische correctheid**: verwijst de slug naar wat je denkt? (bv. `bol-com` = entity, `bol.com` = URL)
- **Verwijderde bestanden**: zijn alle wikilinks naar verwijderde bestanden bijgewerkt?
- **Bulk find-replace**: zoek een steekproef van 3 gewijzigde files en controleer visueel

---

## Root Cleanup (Periodiek)

De vault root mag **alleen** bevatten:
- Mappen: `10_notes/`, `20_structure/`, `90_attachments/`, `.obsidian/`, `.git/`, `.claude/`, `.playwright-mcp/`
- Agent config: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`

Alles anders is rommel en moet opgeruimd worden.

### Procedure

1. **Check root:** `ls -1 "$VAULT/" | grep -v -E '^(10_notes|20_structure|90_attachments|\.obsidian|\.git|\.claude|\.playwright|CLAUDE\.md|AGENTS\.md|GEMINI\.md)$'`
2. **Per bestand beoordelen:**

| Type | Actie |
|------|-------|
| `.png`, `.jpg`, `.pdf`, media | Verplaats naar `90_attachments/` met `YYYYMMDD-HHmm-` prefix (gebruik file mtime) |
| `.md` notes | Verplaats naar `10_notes/` met `YYYYMMDD-HHmm-` prefix |
| Scripts, temp files, logs | Verwijderen (hoort niet in vault) |
| Onbekend | Vraag user |

3. **Wikilinks repareren:** zoek naar `[[oude-naam]]` in alle `.md` bestanden en update naar nieuwe slug
4. **Verify:** draai stap 1 opnieuw — output moet leeg zijn

### Wanneer uitvoeren
- **Proactief:** aan begin van sessie als root rommel bevat
- **Op verzoek:** als user vraagt om opruimen

---

## Vault Regels

### ❌ Niet Doen
- Geen subfolders in `10_notes/` of `90_attachments/`
- Geen absolute paden in links
- Geen lege notes aanmaken
- Geen type/category in filenames (zit in frontmatter)
- **NOOIT filename zonder YYYYMMDD-HHmm prefix in `10_notes/`!**

### ✅ Wel Doen
- **Filename format: `YYYYMMDD-HHmm-slug.md`** (CRITICAL - check dit ALTIJD!)
- Check schema voor geldige types/categories
- Respecteer kebab-case voor slugs
- Update frontmatter bij wijzigingen
- WikiLinks only: `[[slug]]` — geen paden, geen extensies
- **Cadeau-ideeën op entity notes** (`## Cadeau-ideeën`), niet op anniversary notes — ideeën horen bij de persoon, niet bij een datum

---

## Common Mistakes to Avoid

> Dit is de belangrijkste sectie — deze fouten worden het vaakst gemaakt.

### ❌ Timestamp Format Errors

**Wrong:**
```yaml
timestamp: 2026-02-06-1327  # Streepjes in datum
timestamp: 20260206_1327    # Underscore
timestamp: 2026-02-06 13:27 # Spatie
```

**Correct:**
```yaml
timestamp: 20260206-1327    # YYYYMMDD-HHmm (geen streepjes in datum!)
```

### ❌ Type in Filename

**Wrong:**
```
20260206-1327-task-fix-bug.md        # "task" in filename
20260206-1327-entry-note.md          # "entry" in filename
20260206-1327-interaction-call.md    # "interaction" in filename
```

**Correct:**
```
20260206-1327-fix-bug.md             # Type alleen in frontmatter
20260206-1327-note.md
20260206-1327-call-john.md
```

### ❌ Invalid Category for Type

**Wrong:**
```yaml
type: entry
category: technical  # Niet valide voor entry
```

**Correct:** Check `life-os-schema.md` → Categories per Type voor geldige opties.

### ❌ Entity/Topics Niet als Array

**Wrong:**
```yaml
entity: john-doe     # String ipv array
topics: security     # String ipv array
```

**Correct:**
```yaml
entity: [john-doe]   # Altijd array, ook voor single value
topics: [security, privacy]
```

### ❌ Filename Truncatie bij Lange Slugs

**Wrong:**
```
# Slug: follow-up-dvw-analytics-alteryx-connector-for-sap-license
# Bestand: 20260209-1713-follow-up-dvw-analytics-alteryx.md  ← AFGEKAPT!
```

**Correct:**
```
# Slug: follow-up-dvw-analytics-alteryx-connector-for-sap-license
# Bestand: 20260209-1713-follow-up-dvw-analytics-alteryx-connector-for-sap-license.md
```

**Regel:** Bestandsnaam moet ALTIJD de VOLLEDIGE slug bevatten. Nooit afkappen.

### ❌ Placeholder in WikiLinks

**Wrong:**
```markdown
📧 [[temp-mail-note]]       # Placeholder niet vervangen!
📋 Task: [[task-slug]]       # Zonder timestamp prefix
```

**Correct:**
```markdown
📧 [[20260202-1200-mail-ryan|Mail van Ryan]]
📋 Task: [[20260209-1025-book-tsh|Hotelboeking TSH]]
```

**Regel:** Nooit placeholders gebruiken. WikiLinks in `10_notes/` altijd MET timestamp prefix en display text.

### ❌ WikiLink met Pad of Extension

**Wrong:**
```markdown
[[10_notes/20260206-1327-note.md]]    # Met pad en extensie
[[entity/john-doe]]                   # Met submap
[[20260206-1327-note|Note]]         # Markdown link
```

**Correct:**
```markdown
[[20260206-1327-note]]                # Alleen slug
[[john-doe]]                          # Alleen slug
```

### ❌ Status op Niet-Task Types

**Wrong:**
```yaml
type: entry
category: log
status: 🔴 to-do     # Entry heeft geen status!
```

**Correct:** Status is alleen voor `task` en `project` types. Zie schema.

---

---

## Coding Standards

### Algemeen
- **UTF-8 only** — Fix replacement characters direct
- **Geen emoji's in code** tenzij expliciet gevraagd
- **Beknopt** — Korte, directe antwoorden
- **Commit na taken** — Altijd committen na voltooiing

### TypeScript/JavaScript
```typescript
// Strict typing - geen any
interface MyType {
  field: string;
  count: number;
}

// Error handling
try {
  await operation();
} catch (error) {
  console.error(error instanceof Error ? error.message : "Unknown error");
}
```

### Python
```python
# Type hints
def process(data: list[str]) -> dict[str, int]:
    return {item: len(item) for item in data}

# Pathlib voor paden
from pathlib import Path
vault_path = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/viggo_vault_v4"
```

### Git
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Co-author tag: `Co-Authored-By: AI Assistant <noreply@example.com>`
- Geen `--force` of `--no-verify`
