#!/usr/bin/env python3
"""Inspect maintenance commands and checkout state without running writers.

Use ``plan --json`` for the executable generation contract, ``plan --step ID``
for one step, and ``status --json`` for local prerequisites. This interface is
offline and never stages, generates, fetches, commits, pushes, or attests.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools.generation_plan import (  # noqa: E402
    EXCLUDED_OPERATIONS,
    LOCAL_GENERATION_STEPS,
    coverage_errors,
    effective_step_inputs,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "1.0"


class UsageError(ValueError):
    """An invalid inspection request; distinct from a failed observation."""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def plan_payload(step_id: str | None = None) -> dict:
    steps = [step for step in LOCAL_GENERATION_STEPS if step_id in (None, step.identifier)]
    if not steps:
        raise UsageError(f"unknown generation step: {step_id}")
    errors = coverage_errors()
    return {
        "ok": not errors,
        "errors": errors,
        "authority": "code/src/generation_plan.py",
        "execution": "preview_only",
        "steps": [
            {
                "id": step.identifier,
                "description": step.description,
                "write_argv": ["uv", "run", "python3", f"code/orchestrators/{step.script}", *step.write_args],
                "check_argv": ["uv", "run", "python3", f"code/orchestrators/{step.script}", *step.check_args],
                "cache_inputs": list(effective_step_inputs(step)),
                "cache_exclusions": list(step.inputs_exclude),
                "git_index_inputs": list(step.index_inputs),
                "always_run": not bool(step.inputs),
            }
            for step in steps
        ],
        "excluded_operations": [asdict(operation) for operation in EXCLUDED_OPERATIONS],
        "workflow": {
            "regenerate_argv": ["uv", "run", "python3", "code/orchestrators/regenerate_all.py", "--validate"],
            "validate_argv": ["uv", "run", "python3", "code/orchestrators/validate_repo.py"],
            "landing_guide": "docs/operations/settle.md",
            "source_intake_guide": "docs/operations/publication-sync.md",
            "required_gates": ["generated-data", "pytest", "ruff", "artifact-budget", "browser-acceptance"],
        },
    }


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False, timeout=15,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )


def status_payload(root: Path) -> dict:
    """Report observations, without equating a clean tree with validation."""
    errors = coverage_errors(orchestrators_dir=root / "code/orchestrators")
    git = {"available": False}
    try:
        head = _git(root, "rev-parse", "--verify", "HEAD")
        branch = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
        status = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
        if head.returncode == 0 and status.returncode == 0:
            git = {
                "available": True,
                "head": head.stdout.decode("ascii").strip(),
                "branch": branch.stdout.decode("utf-8", errors="replace").strip() or None,
                "clean": not bool(status.stdout),
                "commit_requires_work_branch": branch.stdout.strip() == b"main",
                "remote_verified": False,
            }
        else:
            errors.append("Git checkout state is unavailable")
    except (OSError, subprocess.TimeoutExpired):
        errors.append("Git checkout inspection failed or timed out")
    versions = {}
    for package in ("pytest", "ruff", "playwright", "pypdf", "reportlab"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return {
        "ok": not errors,
        "errors": errors,
        "git": git,
        "runtime": {
            "python": ".".join(map(str, sys.version_info[:3])),
            "python_pin": (root / ".python-version").read_text().strip() if (root / ".python-version").is_file() else None,
            "uv_available": shutil.which("uv") is not None,
            "packages": versions,
            "browser_executable_checked": False,
        },
        "validation": "not_run",
        "network_freshness": "not_checked",
        "deployment": "not_checked",
        "human_visual_review": "not_attested",
        "next_step": "Inspect plan, edit authoritative sources on a work branch, regenerate, then follow the landing guide.",
    }


def main(argv: list[str] | None = None, *, repo_root: Path = REPO_ROOT) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = Parser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
    status = subparsers.add_parser("status", help="Inspect local prerequisites; does not run validation")
    status.add_argument("--json", action="store_true")
    plan = subparsers.add_parser("plan", help="Preview authoritative ordered commands and excluded operations")
    plan.add_argument("--json", action="store_true")
    plan.add_argument("--step", help="Select one stable generation-step ID")
    try:
        args = parser.parse_args(argv)
        payload = plan_payload(args.step) if args.command == "plan" else status_payload(repo_root)
        payload = {"schema_version": SCHEMA_VERSION, "command": args.command, "ok": True, **payload}
        code = 0 if payload["ok"] else 1
    except UsageError as exc:
        payload = {"schema_version": SCHEMA_VERSION, "ok": False, "errors": [str(exc)]}
        code = 2
    except (OSError, ValueError) as exc:
        payload = {"schema_version": SCHEMA_VERSION, "ok": False, "errors": [str(exc)]}
        code = 1
    if "--json" in argv:
        print(json.dumps(payload, ensure_ascii=False))
    elif "steps" in payload:
        for step in payload["steps"]:
            print(f"{step['id']}: {step['description']}")
            print("  write:", " ".join(step["write_argv"]))
            print("  check:", " ".join(step["check_argv"]))
        print("Preview only; source intake, generation and publication retain their existing gates.")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
