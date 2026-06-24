---
type: task
category: screen
created: {{date:YYYY-MM-DD}}
slug: {{date:YYYYMMDD-HHmm}}-{{plugin-id}}-plugin-plan
timestamp: {{date:YYYYMMDD-HHmm}}
status: "🔴 to-do"
area: self
title: "{{plugin-name}} plugin plan"
topics: [codex, agent, planning, obsidian, plugin]
source: manual
project:
project_slug:
entity: []
due:
---

# {{plugin-name}} plugin plan

## Doel

Bouw en publiceer `{{plugin-id}}` als Obsidian community plugin volgens [[publish-obsidian-plugins-knowledge-base|Publish Obsidian Plugins knowledge base]].

Het doel is pas behaald als repo, build, tests, test vault, screenshot/hero, GitHub public repo, release assets, Obsidian checker/submission eisen, commit, push, release en projectnote/registry update bewezen klaar zijn.

## Scope

### In scope

- Repo: `{{PLUGIN_REPO_PATH}}`
- GitHub: `https://github.com/viggomeesters/obsidian-{{plugin-id}}`
- Plugin id: `{{plugin-id}}`
- Plugin name: `{{plugin-name}}`
- Supported files/extensions:
  - 
- Read-only viewer gedrag:
  - 
- Test vault: `{{OBSIDIAN_TEST_VAULT}}`
- Test data: `{{OBSIDIAN_TEST_VAULT}}/fixtures/{{plugin-id}}/`

### Out of scope

- Geen write-back of editor tenzij expliciet besloten.
- Geen externe app launch.
- Geen cloudconversie.
- Geen netwerkcalls tenzij expliciet in scope.
- Geen unsupported extensies in v0.1.
- Geen destructive actions.

## Context

- Knowledge base: [[publish-obsidian-plugins-knowledge-base|Publish Obsidian Plugins knowledge base]]
- Registry: `system/contracts/obsidian-plugins.yaml`
- Audit script: `python3 system/scripts/obsidian_plugins/audit_obsidian_plugins.py`
- Vergelijkbare repos:
  - `{{PLUGIN_REPO_PARENT}}/obsidian-...`

## Requirements

- [ ] Repo volgt de bestaande viewer-structuur.
- [ ] Manifest id bevat geen `obsidian` en eindigt niet op `plugin`.
- [ ] `manifest.json.description` noemt de productnaam niet onnodig.
- [ ] Release tag matcht exact met `manifest.json.version`, zonder `v`.
- [ ] Release assets bevatten `main.js`, `manifest.json`, `styles.css`.
- [ ] README, SECURITY, CONTRIBUTING, CHANGELOG, LICENSE en docs aanwezig.
- [ ] `assets/hero.svg`, `assets/social-preview.svg` en `assets/screenshot.svg` aanwezig en renderbaar.
- [ ] Test fixtures aanwezig voor normaal, leeg, malformed, groot en unsupported input.
- [ ] Plugin is in test vault geinstalleerd onder `.obsidian/plugins/{{plugin-id}}/`.
- [ ] Test data staat in de test vault.
- [ ] Screenshot of SVG/renderbewijs van werkende plugin staat in de repo.
- [ ] Registry en projectnote zijn bijgewerkt.

## Taken

- [ ] Inspecteer registry, KB en meest vergelijkbare pluginrepos.
- [ ] Controleer of target repo al bestaat.
- [ ] Gebruik repo-local go-workflow als aanwezig.
- [ ] Scaffold of update de repo.
- [ ] Implementeer read-only viewer en parser.
- [ ] Voeg fixtures en tests toe.
- [ ] Voeg docs en visual assets toe.
- [ ] Bouw en test lokaal.
- [ ] Installeer in test vault met testdata.
- [ ] Maak screenshot/renderbewijs.
- [ ] Run Obsidian/static/release checks.
- [ ] Commit repo clean.
- [ ] Maak of update public GitHub repo.
- [ ] Push `main`.
- [ ] Maak release met exacte tag en assets.
- [ ] Run registry audit.
- [ ] Update projectnote, registry en knowledge base waar nodig.

## Go-workflow

Als de target repo `.go-workflow/config.yaml` bevat:

```bash
cd {{PLUGIN_REPO_PATH}}
cat AGENTS.md
cat .go-workflow/config.yaml
cat .go-workflow/goals.yaml
cat .go-workflow/tasks.yaml
cat .go-workflow/gates.yaml
python3 scripts/next_task.py --validate
python3 scripts/next_task.py --list --limit 5
python3 -m go_workflow dispatch --text "bouw en publiceer {{plugin-id}} volgens {{pad-naar-dit-plan}}"
```

Gebruik bestaande runnable taken als die passen. Maak geen parallelle tasklijst tenzij het plan of de repo-local workflow daarom vraagt.

## Testing En Validatie

```bash
cd {{PLUGIN_REPO_PATH}}
npm install
npm run build
npx tsc --noEmit
npm test
node -e "const m=require('./manifest.json'); if (m.id !== '{{plugin-id}}') throw new Error(m.id); if (/obsidian/i.test(m.description)) throw new Error(m.description)"
node -e "const fs=require('fs'); for (const f of ['main.js','manifest.json','styles.css']) if (!fs.existsSync(f)) throw new Error('missing '+f)"
node -e "const m=require('./manifest.json'); const v=require('./versions.json'); if (!v[m.version]) throw new Error('versions.json mist '+m.version)"
rg -n "fetch\\(|XMLHttpRequest|WebSocket|navigator\\.clipboard|child_process|spawn\\(|exec\\(|write\\(|modify\\(|eval\\(|new Function|process\\.|!important" src styles.css
python3 - <<'PY'
from xml.etree import ElementTree as ET
for f in ['assets/hero.svg', 'assets/social-preview.svg', 'assets/screenshot.svg']:
    ET.parse(f)
PY
gh repo view viggomeesters/obsidian-{{plugin-id}} --json nameWithOwner,url,visibility,repositoryTopics
gh release view "$(node -p "require('./manifest.json').version")" --repo viggomeesters/obsidian-{{plugin-id}} --json tagName,isDraft,isPrerelease,assets,url
```

Vault/registry:

```bash
cd {{VAULT_PATH}}
python3 system/scripts/obsidian_plugins/audit_obsidian_plugins.py --json
python3 system/scripts/vault/validate_vault.py --changed
python3 system/scripts/vault/validate_vault_workflow.py --changed
```

Test vault:

```bash
TEST_VAULT={{OBSIDIAN_TEST_VAULT}}
mkdir -p "$TEST_VAULT/.obsidian/plugins/{{plugin-id}}" "$TEST_VAULT/fixtures/{{plugin-id}}"
cp main.js manifest.json styles.css "$TEST_VAULT/.obsidian/plugins/{{plugin-id}}/"
cp -R fixtures/* "$TEST_VAULT/fixtures/{{plugin-id}}/" 2>/dev/null || true
```

## Acceptatiecriteria

- [ ] Alle requirements zijn aantoonbaar voldaan.
- [ ] Repo is clean, gecommit en gepusht.
- [ ] GitHub repo is public.
- [ ] Release bestaat met exacte manifestversie en juiste assets.
- [ ] Obsidian checker/submission UI is gecontroleerd.
- [ ] Test vault bevat plugin en testdata.
- [ ] Screenshot/renderbewijs staat in de repo.
- [ ] Registry audit is uitgevoerd en verklaard.
- [ ] Projectnote en registry zijn bijgewerkt.
- [ ] Eindrapport bevat bewijslinks, checks, commit hash, release URL en restpunten.

## Risico's En Beslissingen

| Onderwerp | Risico/beslissing | Mitigatie |
|---|---|---|
| Release checker | Manifestversie zonder release blokkeert distributie | Exacte tag en assets checken |
| Security | Viewer mag geen uitvoer-/writepad worden | Static scans en non-goals |
| UI asset | Crooked/cropped repo hero | Rendercheck en screenshot |
| Test vault | Plugin lijkt klaar maar opent extern/niet native | Verplicht testvault bewijs |

## Deliverables

- [ ] Lokale repo
- [ ] Public GitHub repo
- [ ] Release met assets
- [ ] Test vault installatie
- [ ] Test data
- [ ] Screenshot/renderbewijs
- [ ] Projectnote
- [ ] Registry update
- [ ] Eindrapport met bewijs

## Bronnen

- [[publish-obsidian-plugins-knowledge-base]]
- `system/contracts/obsidian-plugins.yaml`
- `system/scripts/obsidian_plugins/audit_obsidian_plugins.py`

## Status

## 🔴 to-do - {{date:DD MMM YYYY [at] HH:mm}}

Plan aangemaakt.
