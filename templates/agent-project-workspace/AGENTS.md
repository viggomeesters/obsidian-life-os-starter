# Agent Instructions

This folder is the agent project workspace for `{{PROJECT_ID}}`.

## Startup

1. Read `schema.yaml`.
2. Read `config.yaml`.
3. Read `context.md`.
4. Read the glossary at `work/{{GLOSSARY_FILE}}`.
5. Check `tasks.md` before starting work.
6. Use the vault project, entity, and tool paths from `config.yaml` when vault context is needed.

## Folder Rules

- Root is for project control files only, plus workflow tooling in `scripts/` and `.githooks/`.
- `sources/` contains external source material: meetings, mails, documents, data, and raw notes.
- `work/` contains internal thinking: research, analysis, decisions, mappings, scratch notes.
- `work/{{GLOSSARY_FILE}}` is the project-wide glossary and must stay current.
- `output/` contains outward-facing deliverables, reports, exports, and mail drafts.
- Do not add extra folders unless the existing three-way split clearly breaks down.
- Use `YYYY-MM-DD-kebab-case-title.ext` for project files.

## Processing Rules

- New external input goes to `sources/` with `processed: false`.
- Mark a source as `processed: true` only after its useful content has been reflected in `context.md`, `tasks.md`, `changelog.md`, or a file in `work/`.
- Put AI analysis in `work/`, not in `sources/`.
- Add recurring terms, abbreviations, systems, data objects, stakeholders, and domain concepts to the glossary.
- Put client-ready output in `output/`, not in `work/`.
- For binary source files, create a markdown sidecar when metadata or a summary is needed.
- After creating or substantially updating a `work/` or `output/` document, perform a task-extraction pass before considering the document done: scan for new actions, blockers, decisions needed, owners, dependencies, dates, and questions that require follow-up.
- If the task-extraction pass finds actionable follow-ups, add or update tasks in `tasks.md`. Each new follow-up task must include `source: ` with the originating document path. Add `start: YYYY-MM-DD` and `deadline: YYYY-MM-DD` when the timing can be reasonably determined from the document or project planning.
- If follow-up timing is unknown, do not invent false precision; either omit the date fields or create a task with `status: waiting` that explicitly states what date/planning input is missing.
- If a substantial document creates no new tasks, record that explicitly in the relevant task evidence, changelog entry, or completion note.


## Machine-readable Orchestration

- Treat `.hermes/tasks.yaml` as the primary agent queue and `tasks.md` as the human cockpit.
- Before editing project content, claim one ready task:

```bash
python3 scripts/next_task.py --claim --agent <agent-name>
```

- Read the generated `.hermes/runs/*-handoff.md` and stay within `scope.modify` unless the task itself requires a recorded follow-up.
- Do not run parallel workers on overlapping `scope.modify` paths. Guarded statuses are `claimed`, `active`, and `review`.
- When completing a task, update both `tasks.md` and `.hermes/tasks.yaml` with evidence before running `scripts/finish_task.py`.
- If a task has no machine-readable entry yet, add it to `.hermes/tasks.yaml` before delegating it to another agent.

## Required Updates

- Update `context.md` when project truth changes.
- Update `tasks.md` when new actions are found, started, blocked, or completed.
- Before adding many granular tasks, first bundle them under a goal heading in `tasks.md`. A goal represents a concrete outcome/epic; individual tasks stay under that goal for their full lifecycle.
- If a new task does not fit an existing goal, create or refine the goal before adding the task.
- Use goal-first task structure: `## {{PROJECT_CODE}}-G##: Goal name`, an `outcome:` line, a `deliverables:` line naming concrete artifacts/decisions/trackers, then task lines sorted by `{{PROJECT_CODE}}-T###`. Use `status: todo|active|waiting|done|cancelled` on task lines instead of moving tasks between `Inbox`, `Waiting`, and `Done` sections.
- Update `work/{{GLOSSARY_FILE}}` when terminology changes or new recurring project language appears.
- When completing a task, keep it under its goal, check it, set `status: done`, and include both completion date and evidence on the task line:

```text
- [x] {{PROJECT_CODE}}-T###: Description | status: done | done: YYYY-MM-DD | evidence: `path-or-command-or-commit`
```

- After setting a task to `status: done`, run the validator and commit that completed task as a separate local git commit.
- Prefer the finish script:

```bash
python3 scripts/finish_task.py {{PROJECT_CODE}}-T### "short description" --all
```

- Use the task id in the commit message. Do not wait to batch multiple completed tasks into one commit unless they are inseparable.
- Update `changelog.md` for meaningful additions, decisions, processed sources, and structure changes.
- Follow `schema.yaml` for frontmatter, task format, changelog labels, and allowed types.
- Run the validator before considering workspace changes complete:

```bash
python3 "{{VAULT_PATH}}/system/scripts/agent_project_workspace/validate_agent_project_workspace.py" "{{DEV_FOLDER}}"
```

Use Raycast `Agent Project Workspace Init` or `init_agent_project_workspace.py --git-init` / `--git-initial-commit` for new project folders.

## Frontmatter

Project markdown files in `sources/`, `work/`, and `output/` must include:

```yaml
---
type: meeting
project: {{PROJECT_ID}}
created: {{DATE}}
processed: false
---
```

Use only types allowed by `schema.yaml`.
