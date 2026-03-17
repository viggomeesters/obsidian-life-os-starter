# Life OS Schema v8.5

This document defines the unified data model for the Life OS platform. It serves as the **Single Source of Truth** for how notes are structured, categorized, and linked across the vault.

## Design Principles

1. **Separation of Concerns**: Each field answers a specific question
2. **Type Safety**: Categories are type-specific, not global
3. **Flat Discovery**: All notes queryable without folder hierarchy
4. **Extensible**: New categories can be added without schema changes

---

## Folder Structure

Most notes live in `10_notes/` (flat). Special note types have dedicated folders in `20_structure/02_context/`:

| Folder | Purpose | Contents |
|--------|---------|----------|
| `10_notes/` | All general notes | Entries, tasks, interactions, references |
| `02_context/entity/` | Tracked entities | People, pets, companies, products |
| `02_context/anniversaries/` | Recurring events | Birthdays, weddings, adoptions |
| `02_context/projects/` | Active projects | Code repos, personal projects |
| `02_context/chores/` | Recurring chores | Household tasks with frequency tracking |

**Why separate folders?**
- **Entity**: Queried by PRM for contact management
- **Anniversaries**: Special MM-DD filename for calendar sorting
- **Projects**: Linked from tasks, contain roadmaps
- **Chores**: Recurring household tasks, separate from one-time tasks

---

## Field Definitions

### Core Fields (Mandatory)

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `type` | String | What IS this? | `task`, `entity`, `anniversary` |
| `category` | String | Which variant? | `person`, `call`, `bookmark` |
| `created` | Date | When conceived? | `2026-01-16` |
| `slug` | String | Unique identifier? | `john-doe`, `fix-login-bug` |
| `timestamp` | String | Exact creation time? | `20260116-1200` |

### Task-Only Fields

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `status` | String | Current state? | `🟠 in progress` |

> **Note**: The `status` field is **only used for tasks and projects**. Other note types (interactions, health, entries, etc.) do not have a status field.

### Context Fields (Recommended)

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `area` | String | Which life domain? | `work`, `personal`, `household` |
| `project` | String | Belongs to which project? | `bookmark-manager` |
| `entity` | Array | Linked to whom/what? | `[john-doe, acme-corp]` |
| `topics` | Array | Discovery keywords? | `[raycast, typescript]` |

### Obsidian Native Fields

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `aliases` | Array | Alternative names for linking? | `[Johnny, J. Doe]` |

> **Note**: `aliases` is an Obsidian-native field for alternative link names. Always keep this field - it enables `alias` linking to notes.

### Type-Specific Fields

Defined per type in the Categories section below.

---

## Types (11 Core Types)

| Type | Purpose | Location | Commands |
|------|---------|----------|----------|
| `entity` | People, pets, companies, products | `02_context/entity/` | Contacts, Contact Insights, Life OS Config |
| `interaction` | Calls, IRL, chats, mail | `10_notes/` | Log Interaction, Save (mail/chat), Import Calendar |
| `purchase` | Buying things with amount tracking | `10_notes/` | New Note, Purchases |
| `anniversary` | Recurring dates (birthdays, weddings) | `02_context/anniversaries/` | Anniversaries |
| `health` | Health tracking (migraine, weight, blood pressure, nutrition) | `10_notes/` | Log Health, Health Dashboard |
| `entry` | Journals, notes, reflections | `10_notes/` | New Note, Daily Note |
| `task` | Actions to complete | `10_notes/` | New Task, Task Inbox, Task Overview, Today's Focus |
| `project` | Container for tasks | `02_context/projects/` | Projects, Task Overview |
| `reference` | Bookmarks, articles, books, etc. | `10_notes/` | Save (bookmark), References |
| `chore` | Recurring household tasks | `02_context/chores/` | Chores |
| `context` | Personal context docs (identity, history, mindset) | `02_context/self/` | AI agents |

### Type Separation

- **interaction**: Linked to entities, for PRM contact logging
- **purchase**: Has `amount` field, for Shopping Manager inventory tracking
- **anniversary**: Recurring dates with special MM-DD filename format
- **health**: Health metrics tracking, automatically sets `area: health`
- **chore**: Recurring household tasks with frequency and effort tracking
- **context**: Personal context documentation for AI agent interactions and self-reflection

---

## Categories per Type

### `entity`

| Category  | Description   | Specific Fields                   |
| --------- | ------------- | --------------------------------- |
| `person`  | Human contact | See PersonEntity fields below     |
| `pet`     | Animal        | `species`, `birthday`             |
| `company` | Organization  | See CompanyEntity fields below    |
| `product` | Physical item | `brand`, `model`, `purchase_date` |
| `place`   | Location      | `address`, `coordinates`          |

#### PersonEntity Fields (v6.4 - Apple Contacts Compatible)

| Field Group | Field | Type | Description |
|-------------|-------|------|-------------|
| **Sync** | `apple_contact_id` | String | Apple Contact identifier for sync |
| | `google_contact_id` | String | Google Contact identifier for sync (e.g., `people/c123`) |
| **Name** | `first_name`, `last_name` | String | Split name fields |
| | `middle_name`, `nickname` | String | Additional name parts |
| | `name_prefix`, `name_suffix` | String | Dr., Jr., etc. |
| **Primary** | `phone`, `email` | String | Primary contact (backward compatible) |
| | `address`, `city`, `postal_code` | String | Primary address |
| **Multi-value** | `phones[]` | Array | `{label, value}` - mobile, home, work, iPhone |
| | `emails[]` | Array | `{label, value}` - home, work, iCloud |
| | `addresses[]` | Array | `{label, street, city, state, postal_code, country}` |
| | `urls[]` | Array | `{label, value}` - homepage, work |
| **Social** | `social_profiles[]` | Array | `{service, username, url}` - Twitter, LinkedIn |
| **Work** | `company`, `role`, `department` | String | Employment info |
| **Relations** | `birthday` | Date | YYYY-MM-DD |
| | `met_who`, `known_from` | String | Entity slugs |
| | `relations[]` | Array | `{label, name, entity_slug}` |
| **PRM Only** | `contact_frequency` | Number | Days between contacts |
| | `last_contact`, `contact_note` | String | Contact tracking |
| **Apple Only** | `apple_note` | String | Note from Apple Contacts |
| | `contact_image_path` | String | Path to contact photo |
| **Sync Meta** | `sync.last_synced` | ISO Date | Last sync timestamp |
| | `sync.sync_status` | String | synced, pending, conflict, orphaned |

#### CompanyEntity Fields (v6.6)

| Field Group | Field | Type | Description |
|-------------|-------|------|-------------|
| **Basic** | `website` | String | Company website URL |
| | `industry` | String | Industry/sector |
| **Primary** | `phone`, `email` | String | Primary contact (backward compatible) |
| | `address`, `city`, `postal_code` | String | Primary address |
| **Multi-value** | `phones[]` | Array | `{label, value}` - see Phone Labels |
| | `emails[]` | Array | `{label, value}` - see Email Labels |
| | `addresses[]` | Array | `{label, street, city, state, postal_code, country}` |
| | `urls[]` | Array | `{label, value}` - see URL Labels |

#### Contact Field Labels (Apple Contacts Compatible)

| Field | Labels |
|-------|--------|
| `phones[].label` | `mobile`, `home`, `work`, `iPhone`, `main`, `other` |
| `emails[].label` | `home`, `work`, `iCloud`, `other` |
| `addresses[].label` | `home`, `work`, `other` |
| `urls[].label` | `homepage`, `home`, `work`, `other` |

**Example (CompanyEntity with multiple emails):**
```yaml
type: entity
category: company
title: Independer
emails:
  - label: other
    value: noreply@mails.independer.nl
  - label: other
    value: noreply@mijn.independer.nl
```

### `interaction`

Interactions are logged contacts with entities, used by PRM.

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `call` | Phone/video call | `entity` (required), `duration` |
| `irl` | In-person (meeting, visit, hangout) | `entity` (required), `location` |
| `chat` | Text conversation | `entity` (required), `platform` |
| `letter` | Physical letter/card | `entity` (required) |
| `mail` | Email message | `entity` (required), `mail_link`, `from`, `to`, `direction` |

### `purchase`

Purchases track bought items with amount, browseable via the Purchases command.

| Category | Product Type | Specific Fields |
|----------|--------------|-----------------|
| `electronics` | Phones, computers, gadgets | `amount`, `brand`, `model`, `store`, `warranty_until` |
| `appliances` | Witgoed, kitchen | `amount`, `brand`, `model` |
| `furniture` | Meubels | `amount`, `brand`, `store` |
| `clothing` | Kleding | `amount`, `brand` |
| `baby` | Baby items | `amount` |
| `home` | Home improvement, decor | `amount` |
| `sports` | Sports equipment | `amount` |
| `hobby` | Hobby items | `amount` |
| `vehicle` | Car, bike, etc. | `amount`, `brand`, `model` |
| `pet` | Pet food, toys, care supplies | `amount` |
| `intimate` | Intimate wellness products | `amount` |
| `personal_care` | Hygiene & personal care | `amount` |
| `subscription` | Recurring subscriptions & services | `amount` |
| `other` | Miscellaneous | `amount` |

Common fields: `amount` (required), `currency` (default EUR), `store`, `url`

### `anniversary`

Anniversaries are recurring dates, stored in `02_context/anniversaries/`.

| Category | Dutch | Description | Specific Fields |
|----------|-------|-------------|-----------------|
| `verjaardag` | Birthday | Geboortedag | `entity`, `date`, `recurring: 365` |
| `verkering` | Dating | Verkerings anniversary | `entity`, `date`, `recurring: 365` |
| `getrouwd` | Married | Trouwdag | `entity`, `date`, `recurring: 365` |
| `samenwonen` | Living Together | Samenwoondatum | `entity`, `date`, `recurring: 365` |
| `adoptie` | Adoption | Pet/kind adoptie | `entity`, `date`, `recurring: 365` |
| `overleden` | Passed Away | Overlijdensdatum | `entity`, `date`, `recurring: false` |
| `friendship` | Friendship | Vriendschapsdag | `entity`, `date`, `recurring: 365` |
| `verhuisd` | Moved | Verhuisdatum | `entity`, `date`, `recurring: 365` |

### `health`

Health tracking records, automatically sets `area: health`.

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `migraine` | Migraine logging | `pain_level` (🟢🔵🟡🟠🔴), `triggers[]`, `meds[]`, `preventive` |
| `weight` | Weight tracking | `weight` (kg) |
| `bloodpressure` | Blood pressure | `systolic`, `diastolic`, `pulse` |
| `measurement` | Body measurements | `measurement_type`, `value`, `unit` |
| `symptom` | Medical symptoms | `severity` (🟢🟡🟠🔴), `body_part`, `description` |
| `nutrition` | Daily food/calorie tracking | `kcal`, `protein`, `carbs`, `fats`, `fiber`, `tdee`, `deficit` |

Common fields: `date` (measurement date), `notes`

#### Migraine Fixed Options

| Field | Type | Options | Default |
|-------|------|---------|---------|
| `triggers` | Array | `geur`, `voedsel`, `slaap`, `licht`, `sport` | - |
| `meds` | Array | `Paracetemol 1000mg`, `Rizatriptan 5mg` | - |
| `preventive` | String | `Metoprolol 100mg` | `Metoprolol 100mg` |

### `entry`

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `daily` | Daily journal | - |
| `weekly` | Weekly review | `week_start`, `week_end` |
| `yearly` | Yearly review | `year` |
| `note` | General note | - |
| `reflection` | Personal reflection | - |
| `log` | Activity log | - |
| `snapshot` | Point-in-time capture | - |

### `task`

Task categories are **resource-based** ("What do I need?"), while `area` defines the life domain ("Where does it belong?").

| Category | Resource | Examples |
|----------|----------|----------|
| `people` | Human contact needed | Bel tandarts, mail klant, vergadering |
| `money` | Spending required | Bestel monitor, boek hotel, betaal rekening |
| `screen` | Computer/digital work | Fix bug, schrijf rapport, research laptops |
| `hands` | Physical/manual work | Schuur opruimen, fiets repareren, was ophangen |

Common fields: `due`, `recurring`, `area`, `project`

**Category vs Area:**
```yaml
# "Order monitor for work"
category: money    # WHAT resource needed (spending)
area: work         # WHERE it belongs (professional)
```

#### Task Status Timeline

Tasks can have a status timeline in the body using H2 headers:

```markdown
## 🔴 to-do - 19 Jan 2026 at 17:31
Initial creation

## 🟠 in progress - 20 Jan 2026 at 09:15
Started working on it

## 🔵 waiting until 23 Jan 2026 - 20 Jan 2026 at 14:30
Waiting for response from client
```

The last H2 status header determines the current status. The Taskfeed extension parses these headers to track status changes over time.

#### Taskfeed Focus Scoring

Tasks are scored for prioritization (used by Life OS Taskfeed):

| Factor | Weight | Description |
|--------|--------|-------------|
| Due date | 0-100 | Overdue=100, Today=90, Tomorrow=70, This week=40 |
| Area | 0-30 | work=30, home=20, self=15, social=10 |
| Status | 0-25 | in progress=25, to-do=15 |
| Staleness | 0-15 | Older tasks score higher (max 15 days) |
| Time context | -50/+20 | Bonus/penalty based on time of day (e.g., work tasks during work hours) |

### `project`

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `personal` | Personal projects | `local_path` (if code) |
| `client` | Client projects (work) | `local_path` (if code) |
| `internal` | Internal company projects (work) | `local_path` (if code) |

Common fields: `code` (abbreviation), `start_date`, `end_date`, `local_path` (optional)

### `reference`

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `bookmark` | Web bookmark | `url`, `image`, `favicon` |
| `article` | Article/blog post | `url`, `author` |
| `book` | Book | `author`, `isbn`, `rating` |
| `movie` | Film | `director`, `year`, `rating` |
| `series` | TV series | `seasons`, `rating` |
| `podcast` | Podcast | `url`, `host` |
| `video` | YouTube/video | `url`, `channel` |
| `channel` | YouTube/Twitch channel subscription | `url`, `platform`, `thumbnail`, `subscribed` |
| `game` | Video game | `platform`, `genre` |
| `course` | Online course | `url`, `platform`, `progress` |
| `tool` | Software/tool | `url`, `platform` |
| `guide` | Documentation | `url` |

Common fields: `url`, `rating`, `consumed`

#### Rating Scale (alle mediavormen)

| Waarde | Label | Betekenis |
|--------|-------|-----------|
| `s-tier` | S-tier | All-time favoriet, onvergetelijk |
| `aanrader` | Aanrader | Sterk, zeker kijken/lezen |
| `prima` | Prima | Oké, vermakelijk |
| `tegenvaller` | Tegenvaller | Viel tegen |

> Geldt voor alle `reference` categories: movie, series, anime, book, podcast, course, etc.

### `chore`

Chores are recurring items stored in `02_context/chores/`. Each chore has a `nature` that defines its purpose.

#### Nature

| Nature | Meaning | Example |
|--------|---------|---------|
| `obligation` | Must happen, household/care | Kattenbak, aanrecht, stofzuigen, douchen |
| `routine` | Bundle of obligations/invests | Ochtendroutine, avondroutine, bedtijdroutine |
| `invest` | Deliberate choice, personal growth | Bewegen, lezen, piano, date night |

**Rules:**
- A `routine` can be a parent — it groups other chores via `parent` field on children
- An `obligation` or `invest` can have a `parent` (linking to a routine)
- A `routine` cannot itself have a parent (no nesting)

#### Categories

| Category | Description | Example |
|----------|-------------|---------|
| `schoonmaken` | Cleaning (incl. laundry) | Badkamer, stofzuigen, was, beddengoed |
| `onderhoud` | Maintenance (incl. garden) | Filters, tuin, auto, apparaten |
| `administratie` | Admin & finance | Post, contracten, budget |
| `huisdieren` | Pet care | Kattenbak, voer, dierenarts |
| `kinderen` | Children care | Luiers, voeding, consultatiebureau |
| `boodschappen` | Shopping (incl. cooking) | Boodschappen, koken, voorraad |
| `opruimen` | Tidying up | Speelgoed, zolder, kringloop |
| `relaties` | Relationships & social | Verjaardagen, cadeaus, oppas, vrienden, ouders |
| `self` | Personal care & growth | Douchen, lezen, piano, bewegen |
| `health` | Health-related | Bewegen, wandelen |

#### Chore-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `nature` | String | Yes | `obligation`, `routine`, or `invest` |
| `frequency` | Number | Yes | Days between occurrences (1=daily, 7=weekly, 30=monthly) |
| `duration` | Number | No | Time estimate in minutes |
| `time_hint` | String | No | Computed start time within routine (`"06:00"`, `"17:25"`). **Derived value** — written by dashboard on reorder, not manually edited. |
| `parent` | String | No | Slug of parent routine (for habit stacking) |
| `entity` | Array | No | Who can do / is involved (person slugs) |

#### Parent-Child (Habit Stacking)

Routines group obligations and invests via the `parent` field:

```yaml
# ochtendroutine.md (parent)
nature: routine
frequency: 1
time_hint: "06:00"

# douchen.md (child)
nature: obligation
frequency: 1
duration: 10
time_hint: "06:10"  # computed: routine start (06:00) + previous durations
parent: ochtendroutine
```

Children inherit their schedule context from the parent routine. The `time_hint` on children is **computed** by the dashboard when reordering: each chore's start time = previous chore's start time + previous chore's `duration`. Drag-and-drop in the dashboard recalculates and writes all `time_hint` values in the routine.

#### Streak Calculation

Streaks are **computed** from completion headers (not stored):
- Parse `## ✅ YYYY-MM-DD` headers chronologically
- If gap between consecutive completions ≤ `frequency + 1 day` (grace period), streak continues
- Current streak = consecutive completions from most recent backwards

#### Completion Tracking (H2 Headers)

Chores track completion history in the markdown body using H2 headers:

```markdown
## ✅ 2026-01-29 - viggo-meesters (30 min)
Optional note about this completion

## ✅ 2026-01-22 - anne-meesters (45 min)
Did extra deep clean
```

**Format:** `## ✅ YYYY-MM-DD - {entity-slug} ({duration} min)` or `## ✅ YYYY-MM-DD` (minimal)

The system parses these headers to calculate:
- Last done date and by whom
- Days since last completion
- Days overdue (when frequency is set)
- Current streak (consecutive on-time completions)

**Filename format:** `{category}-{frequency}-{slug}.md`
Example: `schoonmaken-7-badkamer.md` (weekly bathroom cleaning)

---

## Areas (Life Domains)

Areas provide context for WHERE something belongs in your life:

| Area     | Domain       | Covers                                |
| -------- | ------------ | ------------------------------------- |
| `work`   | Professional | Career, employer, colleagues, clients |
| `home`   | Domestic     | House, household, family, chores      |
| `self`   | Personal     | Health, growth, hobbies, learning     |
| `social` | Community    | Friends, network, events              |

### Area vs Category vs Topics

```
area:     WHERE in your life  →  work, home, self, social
type:     WHAT kind of thing  →  task, anniversary, entity
category: WHICH variant       →  people, money, screen, hands, admin (for tasks)
topics:   DISCOVERY keywords  →  raycast, typescript, review
```

**Example:**
```yaml
type: task
category: screen
area: work
project: 2026-01-bookmark-manager
topics: [raycast, typescript, caching]
```

This task is:
- A `task` (what) that requires `screen` work (computer/digital)
- For `work` (professional context)
- Part of `bookmark-manager` (which project)
- Related to `raycast, typescript, caching` (discovery)

---

## Status Values

| Status | Meaning | Use for |
|--------|---------|---------|
| `🔴 to-do` | Not started | Tasks, projects |
| `🟠 in progress` | Actively working | Tasks, projects |
| `🔵 waiting` | Blocked/external | Tasks |
| `🟢 done` | Completed | Everything |
| `🟣 backlog` | Future consideration | Tasks, projects |
| `⚫ cancelled` | Aborted | Everything |

---

## Linking & Relations

### Field-based Links

```yaml
project: 2026-01-bookmark-manager     # Task belongs to project
entity: [john-doe, jane-doe]  # Event involves these people
```

### WikiLinks in Content

```markdown
Related to [[20260202-1555-bella-chip-activeren]] and [[john-doe]].
```

### Rules

1. Notes in `10_notes/` link by filename: `[[YYYYMMDD-HHmm-slug]]`
2. Context notes link by slug: `[[john-doe]]`, `[[2026-01-bookmark-manager]]`
3. No folder paths in links
4. `entity` field always as array for consistency
5. `project` field as string (single project per item)

---

## Filename Conventions

### Standard Format

Most notes use timestamp + slug:
```
YYYYMMDD-HHmm-slug.md
```

**Why this format?**
- **Unique**: Minute-level timestamp prevents duplicates
- **Sortable**: Chronological by default
- **Simple**: No type/category in filename (that's in frontmatter)
- **Short**: More room for descriptive slug

**Rules:**
- Slug in `kebab-case`
- Keep slug concise but descriptive
- No type/category in filename — use frontmatter for filtering

### Examples by Type

| Type | Location | Pattern | Example |
|------|----------|---------|---------|
| `entity` | `02_context/entity/` | `{slug}.md` | `john-doe.md` |
| `project` | `02_context/projects/` | `YYYY-MM-slug.md` | `2026-01-bookmark-manager.md` |
| `anniversary` | `02_context/anniversaries/` | `{MM-DD}-{category}-{entity}.md` | `01-15-verjaardag-john-doe.md` |
| `chore` | `02_context/chores/` | `{category}-{frequency}-{slug}.md` | `schoonmaken-7-badkamer.md` |
| All others | `10_notes/` | `YYYYMMDD-HHmm-slug.md` | `20260202-1555-bella-chip-activeren.md` |

**Context files** (in `02_context/`) don't need timestamps — they're reference documents, not timestamped notes.

---

## Extension Mapping

All functionality lives in a single unified Raycast extension: **Life OS** (`extensions/life-os/`), with 25 commands organized by domain.

### Command → Type Mapping

| Domain | Command | Types Created/Managed |
|--------|---------|----------------------|
| **Capture** | New Note | `entry`, `interaction`, `purchase`, `health`, `task`, `project`, `entity`, `reference` |
| | New Task | `task` |
| | Log Health | `health` |
| | Log Interaction | `interaction` |
| | Daily Note | `entry` (daily) |
| | Health Dashboard | `health` (read-only) |
| | Task from Note | `task` |
| **Save** | Save | `interaction` (mail, chat), `reference` (bookmark) |
| | Copy Mail Link | - (clipboard utility) |
| | Path to Link | - (clipboard utility) |
| **PRM** | Contacts | `entity` (read-only) |
| | Contact Insights | `entity` (decay analysis) |
| | Anniversaries | `anniversary` (read-only) |
| | Life OS Config | `entity` (Apple Contacts sync, repair) |
| | Vault Health | all types (validation) |
| **Search** | Search Vault | all types (read-only) |
| **Tasks** | Task Inbox | `task` (focus scoring) |
| | Task Overview | `task`, `project` (read-only) |
| | Today's Focus | `task` (daily view) |
| | Chores | `chore` (completion tracking, streaks) |
| **Browse** | References | `reference` (read-only) |
| | Projects | `project` (with task stats) |
| | Purchases | `purchase` (read-only) |
| **Calendar** | Import Calendar | `interaction` (irl) |

### Shared Core Package

All commands share `@life-os/core` (located at `~/Dev/raycast-life-os/packages/core`):
- **Types**: All note types, categories, areas
- **VaultService**: File I/O, frontmatter parsing, path traversal protection
- **Services**: Scoring engine, status parser, expiry processor, chore parser, contact mapper
- **Utilities**: Slug generation, date formatting, path helpers

---

## Query Examples

```typescript
// All overdue work tasks
vault.query()
  .type('task')
  .area('work')
  .where(t => t.due < today && t.status === '🔴 to-do')

// Upcoming birthdays
vault.query()
  .type('anniversary')
  .category('verjaardag')
  .where(e => daysUntil(e.date) <= 7)

// All interactions with John
vault.query()
  .type('interaction')
  .entity('john-doe')
  .orderBy('created', 'desc')

// Bookmarks about TypeScript
vault.query()
  .type('reference')
  .category('bookmark')
  .topic('typescript')
```

---

## Templates

Frontmatter templates for each note type. Copy and fill in the relevant fields.

**Note:** Template files in `01_system/templates/` use placeholders like `{{entity}}` and `{{project}}`. These are intentional and excluded from vault health checks.

### Entity Templates

#### Person
```yaml
type: entity
category: person
created: YYYY-MM-DD
slug: firstname-lastname
timestamp: YYYYMMDD-HHmm
area: social  # or work, personal
title: "First Last"
first_name: "First"
last_name: "Last"
phone: "+31..."
email: "..."
birthday: YYYY-MM-DD
company: "..."
role: "..."
contact_frequency: 30  # days
```

#### Company
```yaml
type: entity
category: company
created: YYYY-MM-DD
slug: company-name
timestamp: YYYYMMDD-HHmm
area: work  # or finance
title: "Company Name"
website: "https://..."
industry: "..."
emails:
  - label: other
    value: noreply@company.com
```

### Interaction Template
```yaml
type: interaction
category: call  # or irl, chat, letter
created: YYYY-MM-DD
slug: call-firstname-lastname
timestamp: YYYYMMDD-HHmm
area: social  # or work
entity: [firstname-lastname]  # Required
title: "Call with First"
duration: "30m"  # for calls
location: "..."  # for irl
platform: "..."  # for chats
```

### Mail Interaction Template
```yaml
type: interaction
category: mail
created: YYYY-MM-DD
slug: YYYYMMDD-HHmm-mail-entity-slug
timestamp: YYYYMMDD-HHmm
area: work  # or self, social
project: project-slug  # Optional, auto-detected from entity
entity: [entity-slug]  # Required
title: "Email Subject"
mail_link: message://<messageId>
from: sender@example.com
to: recipient@example.com
direction: received  # or sent
topics: []
```

**Body format:**
```markdown
# 📥 Email Subject

📧 From: [[entity-slug]] (sender@example.com)
📬 To: recipient@example.com
📅 D Mon YYYY at HH:mm
[📩 Open in Mail](message://<messageId>)
📋 Task: [[task-slug|Task title]]

---

{email body}
```

### Purchase Template
```yaml
type: purchase
category: electronics  # or appliances, furniture, clothing, baby, home, sports, hobby, vehicle, other
created: YYYY-MM-DD
slug: product-name
timestamp: YYYYMMDD-HHmm
area: personal  # or household, work
title: "Product Name"
amount: 99.00  # Required
currency: EUR
brand: "..."
model: "..."
store: "..."
url: "..."
warranty_until: YYYY-MM-DD
```

### Anniversary Template
```yaml
type: anniversary
category: verjaardag  # or verkering, getrouwd, samenwonen, adoptie, overleden, friendship, verhuisd
created: YYYY-MM-DD
slug: MM-DD_category_entity
timestamp: YYYYMMDD-HHmm
area: social
entity: [firstname-lastname]  # Required
title: "First's Birthday"
date: YYYY-MM-DD  # Original date (year for age calculation)
recurring: 365  # Use false for overleden
enable_admin_notifications: true
enable_congratulation_notifications: false
```

### Health Templates

#### Migraine

- `created` / `timestamp`: moment of logging (not the migraine day)
- `date`: the migraine day being logged
- `slug`: `YYYYMMDD-HHmm-migraine` where YYYYMMDD is the migraine date

```yaml
type: health
category: migraine
created: YYYY-MM-DD          # when this note was created
slug: YYYYMMDD-1200-migraine  # based on migraine date
timestamp: YYYYMMDD-HHmm     # when this note was created
area: health
title: "Migraine — Matige migraine"
date: YYYY-MM-DD              # the migraine day
pain_level: 🟡 mild  # 🟢 none | 🔵 tension | 🟡 mild | 🟠 moderate | 🔴 severe
triggers: [slaap]  # slaap, stress, weer, eten, griep, scherm, alcohol, geur, voedsel, licht, sport
meds: [Rizatriptan 5mg]  # Paracetamol 1000mg, Rizatriptan 5mg, Ibuprofen 400mg
preventive: Metoprolol 100mg
```

#### Weight
```yaml
type: health
category: weight
created: YYYY-MM-DD
slug: weight-YYYYMMDD
timestamp: YYYYMMDD-HHmm
area: health
title: "Weight Log"
date: YYYY-MM-DD
weight: 80.0  # kg
```

#### Blood Pressure
```yaml
type: health
category: bloodpressure
created: YYYY-MM-DD
slug: bp-YYYYMMDD
timestamp: YYYYMMDD-HHmm
area: health
title: "Blood Pressure"
date: YYYY-MM-DD
systolic: 120
diastolic: 80
pulse: 70
```

#### Nutrition
```yaml
type: health
category: nutrition
created: YYYY-MM-DD
slug: YYYYMMDD-HHmm-nutrition
timestamp: YYYYMMDD-HHmm
area: health
title: "Voeding DD mmm"
date: YYYY-MM-DD
kcal: 0
protein: 0       # grams
carbs: 0         # grams
fats: 0          # grams
fiber: 0         # grams
tdee: 2500       # estimated daily energy expenditure
deficit: 0       # kcal (negative = surplus)
```

### Entry Templates

#### Daily Journal
```yaml
type: entry
category: daily
created: YYYY-MM-DD
slug: YYYYMMDD_daily_note
timestamp: YYYYMMDD-HHmm
area: personal
title: "Daily Note"
```

#### Note
```yaml
type: entry
category: note
created: YYYY-MM-DD
slug: note-title
timestamp: YYYYMMDD-HHmm
area: personal  # or work
title: "Note Title"
topics: []
```

### Task Template
```yaml
type: task
category: screen  # or people, money, hands, admin
created: YYYY-MM-DD
slug: action-description
timestamp: YYYYMMDD-HHmm
status: 🔴 to-do
area: work  # or home, self, social
project: project-slug  # Optional
entity: []  # Optional
title: "Action Description"
due: YYYY-MM-DD
scheduled: "YYYY-MM-DD HH:MM-HH:MM"  # Optional — time block for calendar week view
```

### Project Template
```yaml
type: project
category: personal  # or client, internal
created: YYYY-MM-DD
slug: project-name
code: P-NAME  # Optional abbreviation
timestamp: YYYYMMDD-HHmm
status: 🟠 in progress
area: work  # or home, self, social
title: "Project Name"
start_date: YYYY-MM-DD
local_path: "/path/to/repo"  # Optional, for code projects
```

### Reference Templates

#### Bookmark
```yaml
type: reference
category: bookmark
created: YYYY-MM-DD
slug: page-title
timestamp: YYYYMMDD-HHmm
area: work  # or home, self, social
title: "Page Title"
url: "https://..."
description: "..."
topics: []
```

#### Book/Media
```yaml
type: reference
category: book  # or movie, series, podcast, video, course
created: YYYY-MM-DD
slug: title
timestamp: YYYYMMDD-HHmm
status: 🟣 backlog  # or 🟠 in progress, 🟢 done
area: personal
title: "Title"
author: "..."  # or director, host
url: "..."
rating: 4  # 1-5
consumed: YYYY-MM-DD  # When finished
```

#### Channel
```yaml
type: reference
category: channel
created: YYYY-MM-DD
slug: YYYYMMDD-HHmm-channel-name
timestamp: YYYYMMDD-HHmm
area: self
title: "Channel Name"
url: "https://youtube.com/@handle"
platform: youtube  # or twitch
thumbnail: "https://yt3.ggpht.com/..."
subscribed: true
topics: [tech, gaming]  # genre tags
```

### Chore Template
```yaml
type: chore
nature: obligation  # or routine, invest
category: schoonmaken  # or onderhoud, administratie, huisdieren, kinderen, boodschappen, opruimen, relaties, self, health
created: YYYY-MM-DD
slug: category-frequency-description
title: "Chore Description"
area: home  # or self, social
frequency: 7  # days (1=daily, 7=weekly, 14=bi-weekly, 30=monthly)
duration: 30  # minutes (optional)
time_hint: "17:00"  # computed by dashboard on reorder (do not edit manually)
parent: routine-slug  # habit stacking (optional)
entity: [person-slug]  # who can do this (optional)
topics: [huishouden]
```

**Body with completion history:**
```markdown
# Chore Description

Checklist or description here.

## ✅ 2026-01-29 - viggo-meesters (30 min)
Optional completion note
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v8.5 | 2026-03-09 | Added optional `scheduled` field to tasks. Format: `"YYYY-MM-DD HH:MM-HH:MM"`. Enables time-block scheduling via dashboard calendar week view drag-and-drop. Separate from `due` (deadline) — `scheduled` is when you plan to work on it. |
| v8.4 | 2026-03-09 | Added `channel` category to `reference` type for YouTube/Twitch channel subscriptions. Fields: `platform`, `thumbnail`, `subscribed`. Dashboard tab for channel management. |
| v8.3 | 2026-03-08 | Renamed `effort` → `duration` on chores for consistency between frontmatter and dashboard. `time_hint` is now a derived value — computed by dashboard drag-and-drop reorder based on routine start time + cumulative duration. Migrated 102 chore notes. |
| v8.2 | 2026-03-07 | Merged interaction categories `meeting` and `visit` into single `irl` category. Simplifies to 5 medium-based categories: `irl`, `call`, `chat`, `mail`, `letter`. Migrated 129 existing notes. |
| v8.1 | 2026-03-05 | Clarified migraine template: `created`/`timestamp` = moment of logging, `date` = migraine day. Updated slug format to match actual notes (`YYYYMMDD-1200-migraine`). Expanded trigger and meds options. Added dashboard migraine logging via `/api/migraine`. |
| v8.0 | 2026-03-05 | **Breaking change:** Removed `ritual` type — merged into `chore` with new `nature` field (obligation/routine/invest). Added `time_hint` for ordering, `parent` for habit stacking (Atomic Habits-inspired routines). Removed Activity Box (AB) system — scheduling now lives on chores themselves via `time_hint` and `parent`. Streak calculation from completion headers. 12→11 note types. |
| v7.7 | 2026-02-28 | Added `nutrition` category under `health` type for daily food/calorie tracking. Fields: `kcal`, `protein`, `carbs`, `fats`, `fiber`, `tdee`, `deficit`. Removed `migraine_*` fields from daily notes — migraine tracking is exclusively via `type: health, category: migraine` notes. |
| v7.6 | 2026-02-25 | Added `google_contact_id` to all entity types (person, company, pet, place). Added `apple_contact_id` to company, pet, place entities. Enables hub-and-spoke contact sync: Obsidian → Apple + Google. |
| v7.5 | 2026-02-17 | Added `code` field to projects for short abbreviations (e.g., SDP, UU, GG). |
| v7.4 | 2026-02-15 | Added Activity Box (AB) concept — time-organisation layer linking timeslots, chores, and tasks. 11 ABs covering 168h/week (100%). Defined in `focus-overview.md`, documented in schema. |
| v7.3 | 2026-02-14 | Unified 6 separate Raycast extensions into single `life-os` extension (25 commands). Added commands: Log Interaction, Rituals, References, Projects, Purchases, Contact Insights. Updated extension mapping to command-based table. |
| v7.2 | 2026-02-09 | Removed `priority` field from tasks and projects. Priority (P1/P2/P3) was not meaningful enough. Removed from schema, templates, Taskfeed scoring, and all existing notes. |
| v7.1 | 2026-02-05 | Added `ritual` type for recurring quality of life activities (12 types total). Categories: relationship, social, self, health. Stored in `02_context/rituals/`. Distinct from chores - focuses on relationships and well-being rather than household tasks. |
| v7.0 | 2026-02-02 | **Breaking change:** Simplified task categories (7→4) and areas (7→4). Categories now resource-based: `people`, `money`, `screen`, `hands`. Areas now: `work`, `home`, `self`, `social`. Reduces choice fatigue from 14 to 8 options. See migration mapping in task note. |
| v6.11 | 2026-01-29 | Added `chore` type for recurring household tasks (10 types total). Categories: schoonmaken, koken, was, tuin, onderhoud, administratie, huisdieren, baby, boodschappen, opruimen. Completion tracking via H2 headers in body |
| v6.10 | 2026-01-21 | Added 🔵 tension headache to pain_level options (between none and mild) |
| v6.9 | 2026-01-21 | Status field now only for tasks and projects (removed from other note types). Reference media (books, etc.) may optionally use status for consumption tracking |
| v6.8 | 2026-01-21 | Interaction filenames no longer include "interaction" type - category (call, irl, etc.) is sufficient, giving more space for title |
| v6.7 | 2026-01-21 | Added Templates section, consolidated from template_schema.md |
| v6.6 | 2026-01-21 | Extended CompanyEntity with contact fields (phones, emails, addresses, urls), added Contact Field Labels reference table |
| v6.5 | 2026-01-20 | Added Taskfeed extension with focus scoring, task status timeline (H2 headers), `letter` interaction category, updated extension mapping with Life OS extensions |
| v6.4 | 2026-01-19 | Extended PersonEntity with Apple Contacts compatibility (multi-value fields, sync metadata) |
| v6.3 | 2026-01-17 | Renamed `family` → `household`, smart filename format with max 50 chars |
| v6.2 | 2026-01-17 | Added migraine fixed options: triggers, meds, preventive with defaults |
| v6.1 | 2026-01-16 | Added `health` type for health tracking (9 types total) |
| v6.0 | 2026-01-16 | Introduced `area`, simplified types (10→6), standardized `entity` as array |
| v5.1 | 2026-01-16 | Added chat fallback protocol |
| v5.0 | 2026-01-15 | English-first, concise titles |
