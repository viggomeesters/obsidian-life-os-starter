---
type: task
category: screen
created: {{date:YYYY-MM-DD}}
slug: {{date:YYYYMMDD-HHmm}}-{{slug}}
timestamp: {{date:YYYYMMDD-HHmm}}
status: "🔴 to-do"
area: self
title: "{{title}}"
topics: [codex, agent, planning]
source: manual
project:
project_slug:
entity: []
due:
---

# {{title}}

## Doel

Beschrijf de gewenste eindstaat concreet. Het doel is pas behaald als alle taken, requirements, acceptatiecriteria, validaties, commits, pushes, releases en expliciete deliverables uit dit plan bewezen klaar zijn.

## Scope

### In scope

- 

### Out of scope

- 

## Context

- Relevante repo's:
- Relevante vaultbestanden:
- Relevante externe links:
- Relevante screenshots/assets:
- Belangrijke beperkingen:

## Requirements

- [ ] 

## Taken

- [ ] Inventariseer huidige staat, bestaande go-workflow taken en risico's.
- [ ] Werk een korte uitvoeringsstrategie uit.
- [ ] Implementeer de gevraagde wijzigingen binnen scope.
- [ ] Werk documentatie, templates, release-assets of configuratie bij waar nodig.
- [ ] Draai alle validaties en tests hieronder.
- [ ] Commit scoped wijzigingen.
- [ ] Push/publiceer/release waar expliciet gevraagd.
- [ ] Rapporteer bewijs, links, checks en restpunten.

## Go-workflow

Als de target repo `.go-workflow/config.yaml` bevat:

- [ ] Lees `AGENTS.md`.
- [ ] Lees `.go-workflow/config.yaml`, `.go-workflow/goals.yaml`, `.go-workflow/tasks.yaml` en `.go-workflow/gates.yaml`.
- [ ] Run `python3 scripts/next_task.py --validate`.
- [ ] Run `python3 scripts/next_task.py --list --limit 5`.
- [ ] Dispatch met `python3 -m go_workflow dispatch --text "<doeltekst>"`.
- [ ] Gebruik bestaande runnable taken wanneer ze op dit doel slaan.
- [ ] Maak alleen nieuwe taken als het werk nog niet bestaat.

Als er geen go-workflow context is, voer dit plan zelfstandig end-to-end uit.

## Testing En Validatie

Vul projectspecifiek aan.

```bash
git status --short
```

- [ ] Build:
- [ ] Typecheck/lint:
- [ ] Unit/integration tests:
- [ ] Manual QA:
- [ ] Vault validators, indien vaultfiles wijzigen:

```bash
python3 system/scripts/vault/validate_vault.py --changed
python3 system/scripts/vault/validate_vault_workflow.py --changed
```

## Acceptatiecriteria

- [ ] Alle requirements zijn aantoonbaar voldaan.
- [ ] Alle taken zijn klaar of expliciet als out of scope/restpunt verantwoord.
- [ ] Alle relevante tests en validaties zijn geslaagd.
- [ ] Git state is schoon of resterende dirty changes zijn expliciet unrelated.
- [ ] Externe status is gecontroleerd waar relevant, zoals GitHub release, CI, Community Store review of deployed artifact.
- [ ] Eindrapport bevat bewijs: gewijzigde bestanden, commits, release-/PR-links, testresultaten en bekende beperkingen.

## Risico's En Beslissingen

| Onderwerp | Risico/beslissing | Mitigatie |
|---|---|---|
| | | |

## Deliverables

- [ ] 

## Bronnen

- [[codex-goal-plan-workflow]]

## Status

## 🔴 to-do - {{date:DD MMM YYYY [at] HH:mm}}

Plan aangemaakt.
