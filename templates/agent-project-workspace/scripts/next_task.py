#!/usr/bin/env python3
"""Claim and inspect machine-readable Agent Project Workspace tasks."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

TASKS_PATH = Path(".hermes/tasks.yaml")
HANDOFF_DIR = Path(".hermes/runs")
GUARDED_STATUSES = {"claimed", "active", "review"}
READY_STATUSES = {"ready", "todo"}
TERMINAL_STATUSES = {"done", "cancelled"}


def run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(result.stdout.strip() or f"{' '.join(args)} failed")
    return result


def git_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    return Path(result.stdout.strip()).resolve()


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError("PyYAML is required for .hermes/tasks.yaml") from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise RuntimeError("PyYAML is required for .hermes/tasks.yaml") from exc
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def task_by_id(tasks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(task.get("id")): task for task in tasks if isinstance(task, dict) and task.get("id")}


def dependencies_done(task: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> bool:
    for dep in task.get("depends_on") or []:
        if by_id.get(str(dep), {}).get("status") != "done":
            return False
    return True


def claim_expired(task: dict[str, Any], now: datetime) -> bool:
    claim = task.get("claim") if isinstance(task.get("claim"), dict) else {}
    lease_until = parse_dt(claim.get("lease_until"))
    return bool(lease_until and lease_until < now)


def normalize_paths(values: Any) -> set[str]:
    if not isinstance(values, list):
        return set()
    return {str(value).rstrip("/") for value in values if str(value).strip()}


def paths_overlap(a: str, b: str) -> bool:
    a = a.rstrip("/")
    b = b.rstrip("/")
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def blocked_by_concurrency(candidate: dict[str, Any], tasks: list[dict[str, Any]]) -> list[str]:
    candidate_paths = normalize_paths((candidate.get("scope") or {}).get("modify"))
    if not candidate_paths:
        return []
    blockers: list[str] = []
    candidate_id = str(candidate.get("id"))
    candidate_deps = set(str(dep) for dep in candidate.get("depends_on") or [])
    for other in tasks:
        other_id = str(other.get("id"))
        if other_id == candidate_id or other.get("status") not in GUARDED_STATUSES:
            continue
        if other_id in candidate_deps:
            continue
        other_paths = normalize_paths((other.get("scope") or {}).get("modify"))
        for path in candidate_paths:
            if any(paths_overlap(path, other_path) for other_path in other_paths):
                blockers.append(other_id)
                break
    return blockers


def runnable_tasks(data: dict[str, Any], now: datetime) -> list[dict[str, Any]]:
    tasks = [task for task in data.get("tasks", []) if isinstance(task, dict)]
    by_id = task_by_id(tasks)
    result = []
    for task in tasks:
        status = task.get("status")
        if status in TERMINAL_STATUSES or status == "waiting" or status == "review":
            continue
        if status == "claimed" and not claim_expired(task, now):
            continue
        if status not in READY_STATUSES and not (status == "claimed" and claim_expired(task, now)):
            continue
        if not dependencies_done(task, by_id):
            continue
        if blocked_by_concurrency(task, tasks):
            continue
        result.append(task)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(result, key=lambda t: (priority_order.get(str(t.get("priority", "medium")), 1), str(t.get("id"))))


def generate_handoff(root: Path, task: dict[str, Any]) -> Path:
    now = datetime.now().astimezone()
    task_id = str(task.get("id"))
    slug = task_id.lower()
    path = root / HANDOFF_DIR / f"{now.strftime('%Y-%m-%d-%H%M')}-{slug}-handoff.md"
    scope = task.get("scope") or {}
    verification = task.get("verification") or {}
    docs = task.get("docs") or {}
    lines = [
        f"# Task Handoff: {task_id}",
        "",
        f"- Generated: {now.isoformat(timespec='seconds')}",
        f"- Goal: {task.get('goal')}",
        f"- Title: {task.get('title')}",
        f"- Status: {task.get('status')}",
        f"- Priority: {task.get('priority')}",
        "",
        "## Dependencies",
        "",
        *(f"- {dep}" for dep in task.get("depends_on") or ["none"]),
        "",
        "## Scope: read first",
        "",
        *(f"- `{item}`" for item in scope.get("read") or ["none"]),
        "",
        "## Scope: modify only",
        "",
        *(f"- `{item}`" for item in scope.get("modify") or ["none"]),
        "",
        "## Do not touch",
        "",
        *(f"- `{item}`" for item in scope.get("do_not_touch") or ["none"]),
        "",
        "## Acceptance criteria",
        "",
        *(f"- [ ] {item}" for item in task.get("acceptance") or ["No explicit criteria"]),
        "",
        "## Verification commands",
        "",
        *(f"- `{cmd}`" for cmd in verification.get("commands") or ["No command specified"]),
        "",
        "## Documentation",
        "",
        "Check:",
        *(f"- `{item}`" for item in docs.get("check") or []),
        "",
        "Update:",
        *(f"- `{item}`" for item in docs.get("update") or []),
        "",
        "## Commit",
        "",
        f"- Mode: {(task.get('commit') or {}).get('mode')}",
        f"- Message: `{(task.get('commit') or {}).get('message')}`",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or claim the next repo task.")
    parser.add_argument("--claim", action="store_true", help="Claim the next runnable task and write a handoff file.")
    parser.add_argument("--agent", default=os.environ.get("HERMES_PROFILE", "hermes-agent"), help="Agent/profile name for claims.")
    parser.add_argument("--session", default=os.environ.get("HERMES_SESSION_ID", ""), help="Optional session id to record in the claim.")
    parser.add_argument("--task", help="Show one task by id.")
    parser.add_argument("--list", action="store_true", help="List tasks and runnable status.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()

    try:
        root = git_root()
        path = root / TASKS_PATH
        if not path.exists():
            raise RuntimeError(f"missing task queue: {TASKS_PATH}")
        data = load_yaml(path)
        tasks = [task for task in data.get("tasks", []) if isinstance(task, dict)]
        by_id = task_by_id(tasks)
        now = datetime.now(timezone.utc)

        if args.task:
            task = by_id.get(args.task)
            if not task:
                raise RuntimeError(f"task not found: {args.task}")
            print(json.dumps(task, indent=2, ensure_ascii=False) if args.json else task_to_text(task))
            return 0

        runnable = runnable_tasks(data, now)
        if args.list or not args.claim:
            rows = []
            for task in tasks:
                rows.append({
                    "id": task.get("id"),
                    "status": task.get("status"),
                    "priority": task.get("priority"),
                    "runnable": task in runnable,
                    "title": task.get("title"),
                })
            print(json.dumps(rows, indent=2, ensure_ascii=False) if args.json else "\n".join(f"{row['id']} [{row['status']}] runnable={row['runnable']} — {row['title']}" for row in rows))
            return 0

        if not runnable:
            print(json.dumps({"claimed": None, "reason": "no runnable tasks"}) if args.json else "No runnable tasks.")
            return 0

        task = runnable[0]
        lease_minutes = int((data.get("queue_policy") or {}).get("lease_minutes") or 60)
        task["status"] = "claimed"
        task["claim"] = {
            "by": args.agent,
            "at": now.isoformat(timespec="seconds"),
            "lease_until": (now + timedelta(minutes=lease_minutes)).isoformat(timespec="seconds"),
        }
        if args.session:
            task["claim"]["session"] = args.session
        dump_yaml(path, data)
        handoff = generate_handoff(root, task)
        payload = {"claimed": task.get("id"), "title": task.get("title"), "handoff": str(handoff.relative_to(root))}
        print(json.dumps(payload, indent=2, ensure_ascii=False) if args.json else f"Claimed {payload['claimed']}: {payload['handoff']}")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


def task_to_text(task: dict[str, Any]) -> str:
    return json.dumps(task, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sys.exit(main())
