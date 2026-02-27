# Life OS Schema v7.4

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
| `02_context/rituals/` | Quality of life rituals | Recurring personal/relationship activities |

**Why separate folders?**
- **Entity**: Queried for contact management (PRM)
- **Anniversaries**: Special MM-DD filename for calendar sorting
- **Projects**: Linked from tasks, contain roadmaps
- **Chores**: Recurring household tasks, separate from one-time tasks
- **Rituals**: Quality of life activities (dates, family time, self-care) - distinct from chores

---

## Field Definitions

### Core Fields (Mandatory)

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `type` | String | What IS this? | `task`, `entity`, `anniversary` |
| `category` | String | Which variant? | `person`, `call`, `bookmark` |
| `created` | Date | When conceived? | `2026-01-16` |
| `slug` | String | Unique identifier? | `alex-johnson`, `fix-login-bug` |
| `timestamp` | String | Exact creation time? | `20260116-1200` |

### Task-Only Fields

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `status` | String | Current state? | `in progress` |

> **Note**: The `status` field is **only used for tasks and projects**. Other note types (interactions, health, entries, etc.) do not have a status field.

### Context Fields (Recommended)

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `area` | String | Which life domain? | `work`, `home`, `self` |
| `project` | String | Belongs to which project? | `bookmark-manager` |
| `entity` | Array | Linked to whom/what? | `[alex-johnson, acme-corp]` |
| `topics` | Array | Discovery keywords? | `[typescript, caching]` |

### Obsidian Native Fields

| Field | Type | Question | Example |
|-------|------|----------|---------|
| `aliases` | Array | Alternative names for linking? | `[Alex, A. Johnson]` |

> **Note**: `aliases` is an Obsidian-native field for alternative link names. Always keep this field - it enables `alias` linking to notes.

### Type-Specific Fields

Defined per type in the Categories section below.

---

## Types (12 Core Types)

| Type | Purpose | Location |
|------|---------|----------|
| `entity` | People, pets, companies, products | `02_context/entity/` |
| `interaction` | Calls, meetings, chats, visits, mail | `10_notes/` |
| `purchase` | Buying things with amount tracking | `10_notes/` |
| `anniversary` | Recurring dates (birthdays, weddings) | `02_context/anniversaries/` |
| `health` | Health tracking (migraine, weight, blood pressure) | `10_notes/` |
| `entry` | Journals, notes, reflections | `10_notes/` |
| `task` | Actions to complete | `10_notes/` |
| `project` | Container for tasks | `02_context/projects/` |
| `reference` | Bookmarks, articles, books, etc. | `10_notes/` |
| `chore` | Recurring household tasks | `02_context/chores/` |
| `ritual` | Recurring quality of life activities | `02_context/rituals/` |
| `context` | Personal context docs (identity, history, mindset) | `02_context/self/` |

### Type Separation

- **interaction**: Linked to entities, for contact logging
- **purchase**: Has `amount` field, for inventory and spending tracking
- **anniversary**: Recurring dates with special MM-DD filename format
- **health**: Health metrics tracking, automatically sets `area: health`
- **chore**: Recurring household tasks with frequency and effort tracking
- **ritual**: Recurring quality of life activities (dates, family time, self-care) - distinct from chores in purpose
- **context**: Personal context documentation for AI agent interactions and self-reflection

---

## Categories per Type

### `entity`

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `person` | Human contact | See PersonEntity fields below |
| `pet` | Animal | `species`, `birthday` |
| `company` | Organization | See CompanyEntity fields below |
| `product` | Physical item | `brand`, `model`, `purchase_date` |
| `place` | Location | `address`, `coordinates` |

#### PersonEntity Fields

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
| **Sync Meta** | `sync.last_synced` | ISO Date | Last sync timestamp |
| | `sync.sync_status` | String | synced, pending, conflict, orphaned |

#### CompanyEntity Fields

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

#### Contact Field Labels

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
title: Acme Corp
emails:
  - label: work
    value: info@acme-corp.com
  - label: other
    value: support@acme-corp.com
```

### `interaction`

Interactions are logged contacts with entities, used for relationship management.

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `call` | Phone/video call | `entity` (required), `duration` |
| `meeting` | In-person meeting | `entity` (required), `location` |
| `chat` | Text conversation | `entity` (required), `platform` |
| `visit` | Social visit | `entity` (required), `location` |
| `letter` | Physical letter/card | `entity` (required) |
| `mail` | Email message | `entity` (required), `mail_link`, `from`, `to`, `direction` |

### `purchase`

Purchases track bought items with amount tracking.

| Category | Product Type | Specific Fields |
|----------|--------------|-----------------|
| `electronics` | Phones, computers, gadgets | `amount`, `brand`, `model`, `store`, `warranty_until` |
| `appliances` | White goods, kitchen | `amount`, `brand`, `model` |
| `furniture` | Furniture | `amount`, `brand`, `store` |
| `clothing` | Clothing | `amount`, `brand` |
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

Common fields: `amount` (required), `currency` (default USD), `store`, `url`

### `anniversary`

Anniversaries are recurring dates, stored in `02_context/anniversaries/`.

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `birthday` | Date of birth | `entity`, `date`, `recurring: 365` |
| `dating` | Dating anniversary | `entity`, `date`, `recurring: 365` |
| `married` | Wedding anniversary | `entity`, `date`, `recurring: 365` |
| `living-together` | Move-in date | `entity`, `date`, `recurring: 365` |
| `adoption` | Pet/child adoption | `entity`, `date`, `recurring: 365` |
| `passed-away` | Date of passing | `entity`, `date`, `recurring: false` |
| `friendship` | Friendship day | `entity`, `date`, `recurring: 365` |
| `moved` | Moving date | `entity`, `date`, `recurring: 365` |

### `health`

Health tracking records, automatically sets `area: health`.

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `migraine` | Migraine logging | `pain_level`, `triggers[]`, `meds[]`, `preventive` |
| `weight` | Weight tracking | `weight` (kg) |
| `bloodpressure` | Blood pressure | `systolic`, `diastolic`, `pulse` |
| `measurement` | Body measurements | `measurement_type`, `value`, `unit` |
| `symptom` | Medical symptoms | `severity`, `body_part`, `description` |

Common fields: `date` (measurement date), `notes`

#### Pain Level Scale

| Value | Meaning |
|-------|---------|
| `none` | No pain |
| `tension` | Tension headache |
| `mild` | Mild pain |
| `moderate` | Moderate pain |
| `severe` | Severe pain |

#### Migraine Fixed Options

| Field | Type | Options | Default |
|-------|------|---------|---------|
| `triggers` | Array | `smell`, `food`, `sleep`, `light`, `exercise` | - |
| `meds` | Array | `Acetaminophen 1000mg`, `Sumatriptan 50mg` | - |
| `preventive` | String | (your preventive medication) | - |

### `entry`

| Category | Description | Specific Fields |
|----------|-------------|-----------------|
| `daily` | Daily journal | `migraine_*` fields (see below) |
| `weekly` | Weekly review | `week_start`, `week_end` |
| `yearly` | Yearly review | `year` |
| `note` | General note | - |
| `reflection` | Personal reflection | - |
| `log` | Activity log | - |
| `snapshot` | Point-in-time capture | - |

#### Daily Note Migraine Fields

Daily notes use prefixed migraine fields for inline health tracking:

| Field | Type | Options | Default |
|-------|------|---------|---------|
| `migraine_pain` | String | `none`, `tension`, `mild`, `moderate`, `severe` | `none` |
| `migraine_preventive` | String | - | - |
| `migraine_meds` | Array | `Acetaminophen 1000mg`, `Sumatriptan 50mg` | `[]` |
| `migraine_triggers` | Array | `smell`, `food`, `sleep`, `light`, `exercise` | `[]` |
| `migraine_note` | String | Free text | - |

> **Note**: These prefixed fields are for quick daily tracking. For detailed migraine logging, use `type: health`, `category: migraine` notes with non-prefixed fields (`pain_level`, `triggers`, etc.).

### `task`

Task categories are **resource-based** ("What do I need?"), while `area` defines the life domain ("Where does it belong?").

| Category | Resource | Examples |
|----------|----------|----------|
| `people` | Human contact needed | Call dentist, email client, schedule meeting |
| `money` | Spending required | Order monitor, book hotel, pay bill |
| `screen` | Computer/digital work | Fix bug, write report, research laptops |
| `hands` | Physical/manual work | Clean garage, repair bike, hang laundry |

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
## to-do - 19 Jan 2026 at 17:31
Initial creation

## in progress - 20 Jan 2026 at 09:15
Started working on it

## waiting until 23 Jan 2026 - 20 Jan 2026 at 14:30
Waiting for response from client
```

The last H2 status header determines the current status.

> Tasks can be prioritized using focus scoring based on due date, area, and status.

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
| `game` | Video game | `platform`, `genre` |
| `course` | Online course | `url`, `platform`, `progress` |
| `tool` | Software/tool | `url`, `platform` |
| `guide` | Documentation | `url` |

Common fields: `url`, `rating`, `consumed`

#### Rating Scale (all media types)

| Value | Label | Meaning |
|-------|-------|---------|
| `s-tier` | S-tier | All-time favorite, unforgettable |
| `recommended` | Recommended | Strong, definitely worth consuming |
| `decent` | Decent | Okay, entertaining |
| `disappointing` | Disappointing | Fell short of expectations |

> Applies to all `reference` categories: movie, series, book, podcast, course, etc.

### `chore`

Chores are recurring household tasks, stored in `02_context/chores/`.

| Category | Description | Example |
|----------|-------------|---------|
| `cleaning` | Cleaning (incl. laundry) | Bathroom, vacuuming, laundry, bedsheets |
| `maintenance` | Maintenance (incl. garden) | Filters, garden, car, appliances |
| `admin` | Admin & finance | Mail, contracts, budget |
| `pets` | Pet care | Litter box, food, vet |
| `children` | Children care | Diapers, feeding, doctor visits |
| `groceries` | Shopping (incl. cooking) | Groceries, cooking, stock |
| `tidying` | Tidying up | Toys, attic, donation |
| `relationships` | Relationships & social | Birthdays, gifts, babysitting |

#### Chore-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `frequency` | Number | Days between occurrences (7 = weekly, 30 = monthly) |
| `effort` | Number | Default time estimate in minutes |
| `entity` | Array | Who can do this chore (person slugs) |

#### Completion Tracking (H2 Headers)

Chores track completion history in the markdown body using H2 headers:

```markdown
## done 2026-01-29 - alex-johnson (30 min)
Optional note about this completion

## done 2026-01-22 - sam-johnson (45 min)
Did extra deep clean
```

**Format:** `## done YYYY-MM-DD - {entity-slug} ({effort} min)`

These headers are used to calculate:
- Last done date and by whom
- Days since last completion
- Days overdue (when frequency is set)
- Weekly/monthly effort distribution per person

**Filename format:** `{category}-{frequency}-{slug}.md`
Example: `cleaning-7-bathroom.md` (weekly bathroom cleaning)

### `ritual`

Rituals are recurring quality of life activities, stored in `02_context/rituals/`. Unlike chores (household tasks), rituals focus on relationships, self-care, and personal well-being.

| Category | Description | Example |
|----------|-------------|---------|
| `relationship` | Partner/family quality time | Date night, quality time with child |
| `social` | Friends & family connections | Call parents, meet a friend |
| `self` | Personal well-being | Meditation, piano practice, reading |
| `health` | Health-related rituals | Exercise, walking, yoga |

#### Ritual-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `frequency` | Number | Days between occurrences (7 = weekly, 14 = bi-weekly) |
| `entity` | Array | Who is involved (person slugs) |
| `last_completed` | Date | When last done (YYYY-MM-DD) |

#### Completion Tracking (H2 Headers)

Rituals track completion history in the markdown body using H2 headers:

```markdown
## done 2026-02-01
Nice evening, went to the movies

## done 2026-01-18
Cooked at home, quiet evening
```

**Format:** `## done YYYY-MM-DD`

**Filename format:** `{category}-{frequency}-{slug}.md`
Example: `relationship-14-date-night.md` (bi-weekly date night)

---

> **Advanced:** Activity Boxes (time organization) can be added for weekly scheduling. See the project wiki for details.

---

## Areas (Life Domains)

Areas provide context for WHERE something belongs in your life:

| Area | Domain | Covers |
|------|--------|--------|
| `work` | Professional | Career, employer, colleagues, clients |
| `home` | Domestic | House, household, family, chores |
| `self` | Personal | Health, growth, hobbies, learning |
| `social` | Community | Friends, network, events |

### Area vs Category vs Topics

```
area:     WHERE in your life  ->  work, home, self, social
type:     WHAT kind of thing  ->  task, anniversary, entity
category: WHICH variant       ->  people, money, screen, hands (for tasks)
topics:   DISCOVERY keywords  ->  typescript, caching, review
```

**Example:**
```yaml
type: task
category: screen
area: work
project: 2026-01-bookmark-manager
topics: [typescript, caching]
```

This task is:
- A `task` (what) that requires `screen` work (computer/digital)
- For `work` (professional context)
- Part of `bookmark-manager` (which project)
- Related to `typescript, caching` (discovery)

---

## Status Values

| Status | Meaning | Use for |
|--------|---------|---------|
| `to-do` | Not started | Tasks, projects |
| `in progress` | Actively working | Tasks, projects |
| `waiting` | Blocked/external | Tasks |
| `done` | Completed | Everything |
| `backlog` | Future consideration | Tasks, projects |
| `cancelled` | Aborted | Everything |

---

## Linking & Relations

### Field-based Links

```yaml
project: 2026-01-bookmark-manager     # Task belongs to project
entity: [alex-johnson, jane-doe]       # Event involves these people
```

### WikiLinks in Content

```markdown
Related to [[20260202-1555-activate-pet-chip]] and [[alex-johnson]].
```

### Rules

1. Notes in `10_notes/` link by filename: `[[YYYYMMDD-HHmm-slug]]`
2. Context notes link by slug: `[[alex-johnson]]`, `[[2026-01-bookmark-manager]]`
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
- No type/category in filename -- use frontmatter for filtering

### Examples by Type

| Type | Location | Pattern | Example |
|------|----------|---------|---------|
| `entity` | `02_context/entity/` | `{slug}.md` | `alex-johnson.md` |
| `project` | `02_context/projects/` | `YYYY-MM-slug.md` | `2026-01-bookmark-manager.md` |
| `anniversary` | `02_context/anniversaries/` | `{MM-DD}-{category}-{entity}.md` | `01-15-birthday-alex-johnson.md` |
| `chore` | `02_context/chores/` | `{category}-{frequency}-{slug}.md` | `cleaning-7-bathroom.md` |
| `ritual` | `02_context/rituals/` | `{category}-{frequency}-{slug}.md` | `relationship-14-date-night.md` |
| All others | `10_notes/` | `YYYYMMDD-HHmm-slug.md` | `20260202-1555-activate-pet-chip.md` |

**Context files** (in `02_context/`) don't need timestamps -- they're reference documents, not timestamped notes.

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
area: social  # or work, self
title: "First Last"
first_name: "First"
last_name: "Last"
phone: "+1..."
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
area: work
title: "Company Name"
website: "https://..."
industry: "..."
emails:
  - label: other
    value: info@company.com
```

### Interaction Template
```yaml
type: interaction
category: call  # or meeting, chat, visit, letter
created: YYYY-MM-DD
slug: call-firstname-lastname
timestamp: YYYYMMDD-HHmm
area: social  # or work
entity: [firstname-lastname]  # Required
title: "Call with First"
duration: "30m"  # for calls
location: "..."  # for meetings/visits
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
project: project-slug  # Optional
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
# Email Subject

From: [[entity-slug]] (sender@example.com)
To: recipient@example.com
Date: D Mon YYYY at HH:mm
[Open in Mail](message://<messageId>)
Task: [[task-slug|Task title]]

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
area: home  # or work, self
title: "Product Name"
amount: 99.00  # Required
currency: USD
brand: "..."
model: "..."
store: "..."
url: "..."
warranty_until: YYYY-MM-DD
```

### Anniversary Template
```yaml
type: anniversary
category: birthday  # or dating, married, living-together, adoption, passed-away, friendship, moved
created: YYYY-MM-DD
slug: MM-DD-category-entity
timestamp: YYYYMMDD-HHmm
area: social
entity: [firstname-lastname]  # Required
title: "First's Birthday"
date: YYYY-MM-DD  # Original date (year for age calculation)
recurring: 365  # Use false for passed-away
```

### Health Templates

#### Migraine
```yaml
type: health
category: migraine
created: YYYY-MM-DD
slug: migraine-YYYYMMDD
timestamp: YYYYMMDD-HHmm
area: health
title: "Migraine Log"
date: YYYY-MM-DD
pain_level: mild  # none | tension | mild | moderate | severe
triggers: [sleep]  # smell, food, sleep, light, exercise
meds: [Sumatriptan 50mg]  # Acetaminophen 1000mg, Sumatriptan 50mg
preventive: ""  # Your preventive medication, if any
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

### Entry Templates

#### Daily Journal
```yaml
type: entry
category: daily
created: YYYY-MM-DD
slug: YYYYMMDD-HHmm-daily
timestamp: YYYYMMDD-HHmm
area: self
title: "Daily Note"
migraine_pain: none  # Optional migraine tracking
migraine_preventive: ""
```

#### Note
```yaml
type: entry
category: note
created: YYYY-MM-DD
slug: note-title
timestamp: YYYYMMDD-HHmm
area: self  # or work
title: "Note Title"
topics: []
```

### Task Template
```yaml
type: task
category: screen  # or people, money, hands
created: YYYY-MM-DD
slug: action-description
timestamp: YYYYMMDD-HHmm
status: to-do
area: work  # or home, self, social
project: project-slug  # Optional
entity: []  # Optional
title: "Action Description"
due: YYYY-MM-DD
```

### Project Template
```yaml
type: project
category: personal  # or client, internal
created: YYYY-MM-DD
slug: project-name
code: P-NAME  # Optional abbreviation
timestamp: YYYYMMDD-HHmm
status: in progress
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
status: backlog  # or in progress, done
area: self
title: "Title"
author: "..."  # or director, host
url: "..."
rating: recommended  # s-tier, recommended, decent, disappointing
consumed: YYYY-MM-DD  # When finished
```

### Chore Template
```yaml
type: chore
category: cleaning  # or maintenance, admin, pets, children, groceries, tidying, relationships
created: YYYY-MM-DD
slug: category-frequency-description
title: "Chore Description"
area: home
frequency: 7  # days (7=weekly, 14=bi-weekly, 30=monthly)
effort: 30  # default minutes
entity: [person-slug]  # who can do this
topics: [household]
```

**Body with completion history:**
```markdown
# Chore Description

Checklist or description here.

## done 2026-01-29 - alex-johnson (30 min)
Optional completion note
```

### Ritual Template
```yaml
type: ritual
category: relationship  # or social, self, health
created: YYYY-MM-DD
slug: category-frequency-description
title: "Ritual Description"
area: social  # or self, home
frequency: 14  # days (7=weekly, 14=bi-weekly, 30=monthly)
entity: [person-slug]  # who is involved
last_completed: YYYY-MM-DD
```

**Body with completion history:**
```markdown
# Ritual Description

Description or notes about this ritual.

## done 2026-02-01
Optional note about this occurrence

## done 2026-01-18
Previous occurrence note
```
