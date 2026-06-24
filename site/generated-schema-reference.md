# Generated Schema Reference

Generated from canonical `vault-schema.json`. Do not edit by hand; run `make generate`.

Schema version: `9.4.1`  
Updated: `2026-06-08`

## Folders

| Folder | Structure | Purpose |
| --- | --- | --- |
| `00_inbox/` | `flat` | Legacy quarantine buffer for markdown notes that cannot yet be classified safely |
| `10_notes/` | `YYYY-MM` | The Brain (Chronological Timeline for events) |
| `20_files/` | `YYYY-MM` | The Records (Data & Assets in Timeline) |
| `30_media/` | `YYYY-MM` | The Memories (Excluded Binary Data) |
| `system/` | `` | The Engine (Static rules & Structure) |

## Types

| Type | Location | Filename | Categories |
| --- | --- | --- | --- |
| `entity` | `system/entities/` | `{slug}.md` | person, pet, company, product, place |
| `interaction` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | call, irl, chat, letter, mail, meeting |
| `purchase` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | electronics, appliances, furniture, clothing, baby, home, sports, hobby, vehicle, pet, intimate, personal_care, subscription, other |
| `anniversary` | `system/anniversaries/` | `MM-DD-category-entity.md` | verjaardag, getrouwd, adoptie, verkering, friendship, overleden, samenwonen, verhuisd |
| `health` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | migraine, weight, bloodpressure, measurement, symptom, nutrition |
| `entry` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | daily, eod, journal, weekly, yearly, note, reflection, log, snapshot |
| `task` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | inbox, screen, money, hands, ledger, home, work, validation |
| `project` | `system/projects/` | `YYYY-MM-slug.md` | personal, client, internal, project, social |
| `reference` | `10_notes/{YYYY-MM}/` | `YYYYMMDD-HHmm-slug.md` | bookmark, article, attachment, book, movie, series, podcast, video, channel, game, course, tool, guide |
| `chore` | `system/chores/` | `category-frequency-slug.md` | schoonmaken, onderhoud, opruimen, kinderen, huisdieren, boodschappen, self, administratie, relaties, health, Hygiene |
| `context` | `system/context/` | `slug.md` | self, project, work |

## Context fields

| Field | Type | Required new | Description |
| --- | --- | --- | --- |
| `area` | `enum` | `False` | Which life domain? |
| `project` | `string` | `False` | Short project code for retrieval and human queries, normally an abbreviation of the project name, e.g. bam. Must not duplicate project_slug when a separate project code exists. |
| `project_slug` | `string` | `False` | Canonical project note slug/filename stem for the project note, e.g. 2026-05-bam. |
| `entity` | `array` | `False` | Linked to whom/what? |
| `topics` | `array` | `True` | Discovery keywords |
| `aliases` | `array` | `False` | Alternative names for Obsidian linking |
| `source` | `string` | `True` | Origin system (manual, codex-chat, telegram, apple-mail, imessage, browser) |
| `source_id` | `string` | `False` | Stable source identifier for automated captures |
| `thread_id` | `string` | `False` | Conversation/session/thread identifier for chat-like sources |
| `reply_to` | `string` | `False` | Slug or source_id this note replies to |
| `agent` | `string` | `False` | Agent that produced the captured answer when applicable |
| `url` | `string` | `False` | External URL for web/reference captures |
| `generated_from` | `string_or_array` | `False` | Source contract, note, or export that generated this artifact |
| `sources` | `array` | `False` | Source paths, URLs, or source_ids used for compiled synthesis |
| `source_hash` | `string` | `False` | Hash of raw/source content when drift detection is useful |
| `source_hash_algorithm` | `string` | `False` | Hash algorithm for source_hash, usually sha256 |
| `source_checked_at` | `string` | `False` | Timestamp/date when the raw/source hash or URL was last checked |
| `confidence` | `string_or_number` | `False` | Evidence confidence for generated/evidence notes; use high/medium/low or a numeric model confidence |
| `contested` | `boolean` | `False` | True when the note contains unresolved contradiction or competing claims |
| `contradictions` | `array` | `False` | Related slugs/paths/source_ids that conflict with this note |
| `supersedes` | `string_or_array` | `False` | Older slugs/paths/source_ids this note replaces or materially updates |
