# Hermes Project Contract

## Purpose

{{PROJECT_NAME}} workspace. The repository is the durable source of truth for project context, task state, evidence, and handoff context.

## Repo Type

client-project / knowledge-workspace

## Startup

Read in order:

1. `AGENTS.md`
2. `.hermes/project.md`
3. `schema.yaml`
4. `config.yaml`
5. `context.md`
6. `work/{{GLOSSARY_FILE}}`
7. `.hermes/tasks.yaml`
8. `tasks.md`

## Task Source

- Primary machine-readable queue: `.hermes/tasks.yaml`
- Human cockpit: `tasks.md`
- Run evidence: `.hermes/runs/`

Agents should claim exactly one ready task before editing project content.

## Commands

- Claim next task: `python3 scripts/next_task.py --claim --agent <agent-name>`
- Inspect task: `python3 scripts/next_task.py --task {{PROJECT_CODE}}-T###`
- Validate workspace: `python3 "$AGENT_WORKSPACE_VALIDATOR" .`
- Finish task: `python3 scripts/finish_task.py {{PROJECT_CODE}}-T### "short description" --all`

## Git Policy

- Default branch: `main`
- Commit granularity: one commit per task unless tasks are inseparable
- Push policy: push only when explicitly shipping or after local verification is complete
- Dirty-state policy: never mix unrelated changes silently; report and isolate pre-existing dirt

## Documentation Policy

Check `README.md`, `AGENTS.md`, `schema.yaml`, `config.yaml`, `context.md`, `tasks.md`, `changelog.md`, and the relevant `work/`/`output/` files when behavior, workflow, task model, or project truth changes.

## Version / Evidence

This is a project workspace, not a runtime service. Evidence is the validator output, task ledger status, changed file paths, and git commit hash.
