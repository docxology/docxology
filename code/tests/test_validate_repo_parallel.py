"""The no-write checks may run concurrently, but must report deterministically.

`validate_repo` ran all 47 generation checks strictly one at a time. The plan's
ordering exists to constrain *writes*: `coverage_errors` rejects any check
command carrying a write flag, so verification has no ordering requirement at
all and the serialization was pure wall-clock cost.

Concurrency introduces one hazard worth pinning: results arrive in completion
order, so a naive implementation would blame whichever failing generator
happened to finish first, and the same broken tree would name a different
culprit on every run.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import validate_repo as vr  # noqa: E402
from generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402


class _Step:
    def __init__(self, script: str) -> None:
        self.script = script
        self.check_args = ("--check",)


def test_failure_is_reported_in_plan_order_not_completion_order():
    results = [
        (_Step("early.py"), 0, ""),
        (_Step("middle.py"), 1, "middle failed"),
        (_Step("late.py"), 1, "late failed"),
    ]
    assert vr.first_check_failure(results)[0].script == "middle.py"
    # Completion order is not plan order; the answer must not move.
    assert vr.first_check_failure(list(reversed(results)))[0].script == "late.py"


def test_a_clean_sweep_reports_no_failure():
    assert vr.first_check_failure([(_Step("a.py"), 0, "checked a")]) is None


def test_worker_count_is_overridable_and_one_restores_serial_execution(monkeypatch):
    monkeypatch.setenv("DOCXOLOGY_CHECK_WORKERS", "1")
    assert vr.check_worker_count() == 1
    monkeypatch.setenv("DOCXOLOGY_CHECK_WORKERS", "4")
    assert vr.check_worker_count() == 4
    # Garbage never silently becomes a pool size.
    monkeypatch.setenv("DOCXOLOGY_CHECK_WORKERS", "banana")
    assert vr.check_worker_count() >= 1
    monkeypatch.delenv("DOCXOLOGY_CHECK_WORKERS")
    assert 1 <= vr.check_worker_count() <= 8


def test_every_plan_step_has_a_read_only_check_command():
    """The premise of running these concurrently: none of them writes."""
    write_flags = {"--apply", "--write-manifest", "--force", "--all"}
    for step in LOCAL_GENERATION_STEPS:
        command = vr.generation_check_command(step)
        assert "--check" in command or "--check-manifest" in command, command
        assert not write_flags.intersection(command), command


def test_the_resume_check_keeps_its_locked_uv_environment():
    step = next(s for s in LOCAL_GENERATION_STEPS if s.script == "build_resume.py")
    assert vr.generation_check_command(step)[:3] == ["uv", "run", "python3"]


def test_other_steps_run_under_the_current_interpreter():
    step = next(s for s in LOCAL_GENERATION_STEPS if s.script == "build_catalog.py")
    assert vr.generation_check_command(step)[0] == sys.executable
    assert os.path.isabs(vr.generation_check_command(step)[0])
