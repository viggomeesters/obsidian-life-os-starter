# Worker Handoff Format

Every worker receives one bounded task. Do not broaden scope without updating the task queue.

## Required input

- Task ID
- Goal
- Status and dependencies
- Scope: read, create/update, do-not-touch
- Acceptance criteria
- Verification commands
- Documentation impact
- Commit policy

## Execution rules

1. Read the listed files first.
2. Touch only the listed modify paths unless the task itself discovers a necessary follow-up; record that in `tasks.md` / `.hermes/tasks.yaml` instead of silently expanding scope.
3. Keep project terms and glossary current.
4. Run every verification command or explicitly record why it cannot run.
5. Before finish, update task evidence and run `scripts/finish_task.py`.
