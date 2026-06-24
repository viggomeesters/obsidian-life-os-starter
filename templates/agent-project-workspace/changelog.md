# Changelog

## {{DATE}}

- Changed: template includes `.gitignore` so `.hermes/runs/*` and `.hermes/state/*` runtime files stay out of git while `.gitkeep` placeholders remain tracked.

- Added: Finish-task workflow available through `scripts/finish_task.py` and repo-local git hooks.
- Added: Agent project workspace initialized from `system/templates/agent-project-workspace`.
- Decided: Use the flat three-folder model: `sources` for external input, `work` for internal analysis, `output` for deliverables.
