# {{PROJECT_NAME}}

Agent project workspace voor {{PROJECT_NAME}}.

## Start Hier

1. Lees `context.md`.
2. Lees `work/{{GLOSSARY_FILE}}`.
3. Kijk in `tasks.md`.
4. Zet nieuwe input in `sources/`.
5. Werk analyses uit in `work/`.
6. Zet opleveringen in `output/`.

## Structuur

- `schema.yaml` - machine-readable contract voor deze map.
- `AGENTS.md` - werkwijze voor agents.
- `config.yaml` - paden naar deze dev-map, vaultnotes en centrale template-tooling.
- `context.md` - korte projectwaarheid.
- `tasks.md` - actieve werkvoorraad.
- `changelog.md` - betekenisvolle wijzigingen, beslissingen en verwerkte input.
- `work/{{GLOSSARY_FILE}}` - projectbrede begrippenlijst.
- `scripts/finish_task.py` - valideert en commit een afgeronde taak.
- `scripts/next_task.py` - toont/claimt de volgende uitvoerbare taak uit `.hermes/tasks.yaml`.
- `.hermes/` - repo-local projectcontract, machine-readable task queue, handoff prompts en run ledgers.
- `.githooks/` - repo-lokale git hooks voor validatie en taak-id commitberichten.
- `sources/` - externe bronnen zoals notulen, mails, documenten en data.
- `work/` - onderzoek, analyse, beslissingen, mapping en scratch notes.
- `output/` - deliverables, exports, rapporten en mailconcepten.

## Simpele Regel

`sources` is wat binnenkomt, `work` is wat ermee gebeurt, `output` is wat eruit gaat.

## Glossary

De glossary is standaard onderdeel van elke agent project workspace en staat in `config.yaml` onder `paths.glossary`.

Gebruik hem voor terugkerende termen, afkortingen, systemen, dataobjecten, stakeholders en domeinbegrippen. Werk hem bij zodra een begrip projectbreed relevant wordt.

## Goals En Taken

Gebruik goals in `tasks.md` als primaire structuur voor grotere uitkomsten of epics. Een goal is geen losse actie, maar het resultaat waar meerdere taken samen naartoe werken.

Taken blijven hun hele lifecycle onder hetzelfde goal staan. De status staat op de taakregel:

```text
## {{PROJECT_CODE}}-G01: Projectstart en context

outcome: context helder | owner: project owner | target: YYYY-MM-DD
deliverables: context snapshot; processed source inventory; project glossary; first actionable task set

- [ ] {{PROJECT_CODE}}-T###: Beschrijving | status: todo | start: YYYY-MM-DD | deadline: YYYY-MM-DD | source: `work/bron.md`
- [x] {{PROJECT_CODE}}-T###: Beschrijving | status: done | done: YYYY-MM-DD | evidence: `commit-or-file`
```

Als een nieuwe taak niet onder een bestaand goal past, maak of herformuleer eerst het goal.


## Machine-readable Task Orchestration

`tasks.md` blijft de menselijke cockpit. Voor agents is `.hermes/tasks.yaml` de primaire queue met dependencies, scope, acceptance criteria, verificatie, docs-impact, commit policy en claim-state.

Gebruik:

```bash
python3 scripts/next_task.py --list
python3 scripts/next_task.py --claim --agent hermes-default
python3 scripts/next_task.py --task {{PROJECT_CODE}}-T###
```

Een claim schrijft een handoff in `.hermes/runs/`. Parallel werk mag alleen zonder overlappende `scope.modify` paden en zonder parent dependency; `claimed`, `active` en `review` taken blokkeren conflicterende claims.

De finish gate is:

1. acceptance criteria afgevinkt of bewijsbaar voldaan;
2. verificatiecommands groen of expliciet verklaard;
3. docs checked/updated;
4. `tasks.md` done-regel bijgewerkt;
5. `.hermes/tasks.yaml` task op `status: done` met evidence;
6. validator groen;
7. taakcommit gemaakt met task-id.

## Taken Afronden

Afgeronde taken blijven onder hun goal staan en moeten altijd `status: done`, een datum en bewijs hebben:

```text
- [x] {{PROJECT_CODE}}-T###: Beschrijving | status: done | done: YYYY-MM-DD | evidence: `path-or-command-or-commit`
```

Bewijs is concreet: bijvoorbeeld een commit hash, validator-output, command, bestandspad of bronnote.

Rond een taak af met:

```bash
python3 scripts/finish_task.py {{PROJECT_CODE}}-T### "korte beschrijving" --all
```

Het script controleert dat de taak is afgevinkt en `status: done`, `done:` en `evidence:` heeft, draait de validator, zet repo-lokale hooks aan en maakt een commit met het taak-id in het bericht. Zonder `--all` commit het alleen bestanden die al gestaged zijn.

## Taken Uit Documenten

Na elk substantieel document in `work/` of `output/` volgt een task-extractiepass: lees het document alsof het nieuwe acties, blokkades, besluiten, vragen, owners of afhankelijkheden kan bevatten.

Nieuwe follow-up taken komen in `tasks.md` met de herkomst expliciet op de taakregel:

```text
- [ ] {{PROJECT_CODE}}-T###: Beschrijving | start: YYYY-MM-DD | deadline: YYYY-MM-DD | source: `work/{{DATE}}-voorbeeld.md`
```

Gebruik echte datums wanneer die uit planning of document volgen. Als timing ontbreekt, gebruik `status: waiting` met de ontbrekende planninginput.

## Validatie

```bash
python3 "{{VAULT_PATH}}/system/scripts/agent_project_workspace/validate_agent_project_workspace.py" "{{DEV_FOLDER}}"
```

## Nieuwe Projectmap

Gebruik voor nieuwe projecten de vault-standaard via Raycast `Agent Project Workspace Init` of:

```bash
python3 "{{VAULT_PATH}}/system/scripts/agent_project_workspace/init_agent_project_workspace.py" "{{PROJECT_ID}}" "{{PROJECT_NAME}}" --entity "{{ENTITY_SLUG}}" --git-initial-commit
```
