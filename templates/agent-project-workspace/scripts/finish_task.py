#!/usr/bin/env python3
"""Validate and commit one completed project task."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


TASK_ID_RE = re.compile(r"^[A-Z0-9]+-T\d{3}$")
TASK_LINE_RE = re.compile(r"^-\s+\[(?P<state>[ xX])\]\s+(?P<body>.+)$")
VALIDATOR_RELATIVE_PATH = "system/scripts/agent_project_workspace/validate_agent_project_workspace.py"
VAULT_ROOT_ENV_VARS = ("AGENT_WORKSPACE_VAULT_ROOT", "VIGGO_LIFE_OS_VAULT_ROOT", "LIFE_OS_VAULT_ROOT")
VALIDATOR_ENV_VAR = "AGENT_WORKSPACE_VALIDATOR"
DEFAULT_VAULT_ROOTS = (
    Path("{{VAULT_PATH}}"),
    Path("/mnt/c/Users/Viggo/Syncthing/vault"),
    Path("/Users/viggomeesters/Library/Mobile Documents/iCloud~md~obsidian/Documents/vault"),
)


def run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and result.returncode != 0:
        output = result.stdout.strip()
        raise RuntimeError(f"{' '.join(args)} failed" + (f":\n{output}" if output else ""))
    return result


def git_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    return Path(result.stdout.strip()).resolve()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError(f"PyYAML is required to read {path.name}") from exc
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def get_nested(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def candidate_vault_roots(root: Path, local_config: dict[str, Any]) -> list[Path]:
    candidates: list[Path] = []
    local_vault_root = get_nested(local_config, "machine.vault_root")
    if local_vault_root:
        candidates.append(Path(str(local_vault_root)).expanduser())
    for env_var in VAULT_ROOT_ENV_VARS:
        value = os.environ.get(env_var)
        if value:
            candidates.append(Path(value).expanduser())
    candidates.extend(DEFAULT_VAULT_ROOTS)

    seen: set[Path] = set()
    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else root / candidate
        if resolved not in seen:
            unique.append(resolved)
            seen.add(resolved)
    return unique


def resolve_external_path(path_value: str, root: Path, vault_roots: list[Path]) -> Path | None:
    path = Path(os.path.expandvars(path_value)).expanduser()
    candidates = [path] if path.is_absolute() else [root / path, *(vault_root / path for vault_root in vault_roots)]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return None


def resolve_validator(root: Path, explicit: str | None = None) -> Path:
    config = load_yaml(root / "config.yaml")
    local_config = load_yaml(root / "config.local.yaml")
    vault_roots = candidate_vault_roots(root, local_config)

    candidate_values = [
        explicit,
        os.environ.get(VALIDATOR_ENV_VAR),
        get_nested(local_config, "machine.validator"),
        get_nested(local_config, "tools.validator"),
        get_nested(config, "tools.validator"),
        VALIDATOR_RELATIVE_PATH,
    ]
    for value in candidate_values:
        if not value:
            continue
        validator = resolve_external_path(str(value), root, vault_roots)
        if validator and validator.is_file():
            return validator

    searched = [str(root / VALIDATOR_RELATIVE_PATH), *(str(vault_root / VALIDATOR_RELATIVE_PATH) for vault_root in vault_roots)]
    env_hint = f"export {VALIDATOR_ENV_VAR}=<path-to-{VALIDATOR_RELATIVE_PATH}>"
    local_hint = "or set machine.vault_root / machine.validator in config.local.yaml"
    raise RuntimeError("validator not found; tried:\n- " + "\n- ".join(searched) + f"\nSet {env_hint}, {local_hint}.")



def machine_task_done(root: Path, task_id: str) -> tuple[bool, str]:
    tasks_path = root / ".hermes" / "tasks.yaml"
    if not tasks_path.exists():
        return False, ""
    data = load_yaml(tasks_path)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        raise RuntimeError(".hermes/tasks.yaml tasks must be a list")
    for task in tasks:
        if not isinstance(task, dict) or str(task.get("id")) != task_id:
            continue
        if task.get("status") != "done":
            raise RuntimeError(f"{task_id} exists in .hermes/tasks.yaml but status is not done")
        evidence = task.get("evidence")
        if not isinstance(evidence, dict) or not any(evidence.get(key) for key in ("paths", "commands", "commit")):
            raise RuntimeError(f"{task_id} is done in .hermes/tasks.yaml but missing evidence")
        title = str(task.get("title") or task_id)
        return True, title
    return False, ""

def task_done_line(root: Path, task_id: str) -> tuple[str, str]:
    tasks_path = root / "tasks.md"
    if not tasks_path.exists():
        raise RuntimeError("tasks.md not found")

    current_section: str | None = None
    goal_first = "layout: goal_first" in (root / "schema.yaml").read_text(encoding="utf-8") if (root / "schema.yaml").exists() else False
    for line in tasks_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        match = TASK_LINE_RE.match(line)
        if not match or task_id not in match.group("body"):
            continue
        if match.group("state").lower() != "x":
            raise RuntimeError(f"{task_id} exists but is not checked")
        if goal_first:
            if "status: done" not in line:
                raise RuntimeError(f"{task_id} is checked but missing status: done")
        elif current_section != "Done":
            raise RuntimeError(f"{task_id} exists but is not checked under Done")
        if " done: " not in line and "| done:" not in line:
            raise RuntimeError(f"{task_id} is missing done: YYYY-MM-DD")
        if " evidence: " not in line and "| evidence:" not in line:
            raise RuntimeError(f"{task_id} is missing evidence")
        body = match.group("body")
        description = body.split("|", 1)[0].strip()
        return line, description
    raise RuntimeError(f"{task_id} not found as a completed task in tasks.md")


def install_hooks(root: Path) -> None:
    hooks_dir = root / ".githooks"
    if hooks_dir.is_dir():
        run(["git", "config", "core.hooksPath", ".githooks"], root)


def has_staged_changes(root: Path) -> bool:
    result = run(["git", "diff", "--cached", "--quiet"], root, check=False)
    return result.returncode == 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and commit one completed task.")
    parser.add_argument("task_id", help="Task id, e.g. {{PROJECT_CODE}}-T002")
    parser.add_argument("message", nargs="*", help="Commit message tail. Defaults to the task description.")
    parser.add_argument("--all", action="store_true", dest="stage_all", help="Stage all workspace changes before committing.")
    parser.add_argument("--no-hooks", action="store_true", help="Do not install repo-local git hooks before committing.")
    parser.add_argument("--validator", help=f"Explicit validator path. Overrides {VALIDATOR_ENV_VAR} and config.local.yaml.")
    args = parser.parse_args()

    task_id = args.task_id.strip().upper()
    if not TASK_ID_RE.match(task_id):
        print(f"Invalid task id: {args.task_id}", file=sys.stderr)
        return 2

    try:
        root = git_root()
        machine_done, machine_description = machine_task_done(root, task_id)
        try:
            _line, description = task_done_line(root, task_id)
        except RuntimeError:
            if not machine_done:
                raise
            description = machine_description

        if not args.no_hooks:
            install_hooks(root)

        validator = resolve_validator(root, args.validator)
        run(["python3", str(validator), str(root)], root)

        if args.stage_all:
            run(["git", "add", "-A"], root)

        if not has_staged_changes(root):
            raise RuntimeError("no staged changes; stage files first or rerun with --all")

        tail = " ".join(args.message).strip() or description
        commit_message = tail if task_id in tail else f"{task_id}: {tail}"
        run(["git", "commit", "-m", commit_message], root)
        commit_hash = run(["git", "rev-parse", "--short", "HEAD"], root).stdout.strip()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Committed {task_id}: {commit_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
