# Changelog

All notable changes to the Life OS schema are documented here.

This changelog is auto-generated from the schema version history.

## [v8.4] — 2026-03-09

**✨ Added**

- Added `channel` category to `reference` type for YouTube/Twitch channel subscriptions

- Fields: `platform`, `thumbnail`, `subscribed`

- Dashboard tab for channel management


## [v8.3] — 2026-03-08

**♻️ Changed**

- Renamed `effort` → `duration` on chores for consistency between frontmatter and dashboard

- `time_hint` is now a derived value — computed by dashboard drag-and-drop reorder based on routine start time + cumulative duration

- Migrated 102 chore notes


## [v8.2] — 2026-03-07

**♻️ Changed**

- Merged interaction categories `meeting` and `visit` into single `irl` category

- Simplifies to 5 medium-based categories: `irl`, `call`, `chat`, `mail`, `letter`

- Migrated 129 existing notes


## [v8.1] — 2026-03-05

**✨ Added**

- Clarified migraine template: `created`/`timestamp` = moment of logging, `date` = migraine day

- Updated slug format to match actual notes (`YYYYMMDD-1200-migraine`)

- Expanded trigger and meds options

- Added dashboard migraine logging via `/api/migraine`


## [v8.0] — 2026-03-05

**💥 Breaking**

- Breaking change: Removed `ritual` type — merged into `chore` with new `nature` field (obligation/routine/invest)

- Added `time_hint` for ordering, `parent` for habit stacking (Atomic Habits-inspired routines)

- Removed Activity Box (AB) system — scheduling now lives on chores themselves via `time_hint` and `parent`

- Streak calculation from completion headers

- 12→11 note types


## [v7.7] — 2026-02-28

**✨ Added**

- Added `nutrition` category under `health` type for daily food/calorie tracking

- Fields: `kcal`, `protein`, `carbs`, `fats`, `fiber`, `tdee`, `deficit`

- Removed `migraine_*` fields from daily notes — migraine tracking is exclusively via `type: health, category: migraine` notes


## [v7.6] — 2026-02-25

**✨ Added**

- Added `google_contact_id` to all entity types (person, company, pet, place)

- Added `apple_contact_id` to company, pet, place entities

- Enables hub-and-spoke contact sync: Obsidian → Apple + Google


## [v7.5] — 2026-02-17

**✨ Added**

- Added `code` field to projects for short abbreviations (e.g., SDP, UU, GG)


## [v7.4] — 2026-02-15

**✨ Added**

- Added Activity Box (AB) concept — time-organisation layer linking timeslots, chores, and tasks

- 11 ABs covering 168h/week (100%)

- Defined in `focus-overview.md`, documented in schema


## [v7.3] — 2026-02-14

**✨ Added**

- Unified 6 separate Raycast extensions into single `life-os` extension (25 commands)

- Added commands: Log Interaction, Rituals, References, Projects, Purchases, Contact Insights

- Updated extension mapping to command-based table


## [v7.2] — 2026-02-09

**🗑️ Removed**

- Removed `priority` field from tasks and projects

- Priority (P1/P2/P3) was not meaningful enough

- Removed from schema, templates, Taskfeed scoring, and all existing notes


## [v7.1] — 2026-02-05

**✨ Added**

- Added `ritual` type for recurring quality of life activities (12 types total)

- Categories: relationship, social, self, health

- Stored in `02_context/rituals/`

- Distinct from chores - focuses on relationships and well-being rather than household tasks


## [v7.0] — 2026-02-02

**💥 Breaking**

- Breaking change: Simplified task categories (7→4) and areas (7→4)

- Categories now resource-based: `people`, `money`, `screen`, `hands`

- Areas now: `work`, `home`, `self`, `social`

- Reduces choice fatigue from 14 to 8 options

- See migration mapping in task note


## [v6.11] — 2026-01-29

**✨ Added**

- Added `chore` type for recurring household tasks (10 types total)

- Categories: schoonmaken, koken, was, tuin, onderhoud, administratie, huisdieren, baby, boodschappen, opruimen

- Completion tracking via H2 headers in body


## [v6.10] — 2026-01-21

**✨ Added**

- Added 🔵 tension headache to pain_level options (between none and mild)


## [v6.9] — 2026-01-21

**✨ Added**

- Status field now only for tasks and projects (removed from other note types)

- Reference media (books, etc.) may optionally use status for consumption tracking


## [v6.8] — 2026-01-21

**✨ Added**

- Interaction filenames no longer include "interaction" type - category (call, irl, etc.) is sufficient, giving more space for title


## [v6.7] — 2026-01-21

**✨ Added**

- Added Templates section, consolidated from template_schema.md


## [v6.6] — 2026-01-21

**✨ Added**

- Extended CompanyEntity with contact fields (phones, emails, addresses, urls), added Contact Field Labels reference table


## [v6.5] — 2026-01-20

**✨ Added**

- Added Taskfeed extension with focus scoring, task status timeline (H2 headers), `letter` interaction category, updated extension mapping with Life OS extensions


## [v6.4] — 2026-01-19

**✨ Added**

- Extended PersonEntity with Apple Contacts compatibility (multi-value fields, sync metadata)


## [v6.3] — 2026-01-17

**♻️ Changed**

- Renamed `family` → `household`, smart filename format with max 50 chars


## [v6.2] — 2026-01-17

**✨ Added**

- Added migraine fixed options: triggers, meds, preventive with defaults


## [v6.1] — 2026-01-16

**✨ Added**

- Added `health` type for health tracking (9 types total)


## [v6.0] — 2026-01-16

**✨ Added**

- Introduced `area`, simplified types (10→6), standardized `entity` as array


## [v5.1] — 2026-01-16

**✨ Added**

- Added chat fallback protocol


## [v5.0] — 2026-01-15

**✨ Added**

- English-first, concise titles

