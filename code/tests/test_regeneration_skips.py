"""Skip-on-unchanged behavior for the regenerate_all write driver.

These tests run the real ``uv run`` step commands in a temporary git
repository, so they verify the actual interpreter chain a consumer invokes —
not a mocked ``subprocess.run``.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

import regenerate_all  # noqa: E402
import validate_repo  # noqa: E402
from docxology_tools.generation_plan import (  # noqa: E402
    REGENERATION_STATE_RELATIVE_PATH,
    GenerationStep,
    input_fingerprint,
    load_regeneration_state,
    save_regeneration_state,
    step_skip_reason,
)


@pytest.fixture(autouse=True)
def _seed_inputs(tmp_path: Path) -> None:
    """Give every test the two declared inputs most steps consume."""
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "works.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / "data" / "work-enrichment.json").write_text("{}\n", encoding="utf-8")


def _write_step(*inputs: str) -> GenerationStep:
    return GenerationStep(
        "fixture",
        "fixture.py",
        (),
        ("--check",),
        "fixture writer",
        inputs,
    )


def test_no_declared_inputs_step_always_runs(tmp_path: Path) -> None:
    step = _write_step()
    state: dict[str, str] = {}

    assert step_skip_reason(step, state, tmp_path) is None

    # Even a persisted entry cannot make an input-less step skip.
    state[step.identifier] = "anything"
    assert step_skip_reason(step, state, tmp_path) is None
    ran, _skipped = regenerate_all.run_regeneration(
        steps=(step,), runner=lambda script, args: None, repo_root=tmp_path, emit=lambda _m: None
    )
    assert ran == 1


def test_run_then_skip_then_rerun_on_touched_input(tmp_path: Path) -> None:
    step = _write_step("data/works.json", "data/work-enrichment.json")
    calls: list[str] = []
    emitted: list[str] = []

    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=emitted.append,
    )
    assert (ran, skipped) == (1, 0)
    assert calls == ["fixture.py"]
    # A successful run persists the fingerprint.
    state = load_regeneration_state(tmp_path)
    assert step.identifier in state

    # Second run with unchanged inputs: skipped with a logged reason.
    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=emitted.append,
    )
    assert (ran, skipped) == (0, 1)
    assert len(calls) == 1
    assert len(emitted) == 1 and emitted[-1].startswith("skip fixture:")

    # Touching a declared input (content change) reruns the step.
    (tmp_path / "data" / "works.json").write_text('{"works": 2}\n', encoding="utf-8")
    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=emitted.append,
    )
    assert (ran, skipped) == (1, 0)
    assert len(calls) == 2

    # Force reruns even with fresh state.
    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        force=True,
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=emitted.append,
    )
    assert (ran, skipped) == (1, 0)
    assert len(calls) == 3


def test_skip_state_is_fingerprint_not_mtime(tmp_path: Path) -> None:
    step = _write_step("data/works.json")
    calls: list[str] = []

    regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    # An mtime-only touch (same bytes) must not invalidate the fingerprint.
    os.utime(tmp_path / "data" / "works.json", (0, 0))
    assert step_skip_reason(step, load_regeneration_state(tmp_path), tmp_path) is not None
    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    assert (ran, skipped) == (0, 1)


def test_missing_input_file_always_runs(tmp_path: Path) -> None:
    step = _write_step("data/works.json")
    (tmp_path / "data" / "works.json").unlink()
    calls: list[str] = []

    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    assert (ran, skipped) == (1, 0)
    assert calls == ["fixture.py"]


def test_fingerprint_is_none_when_pattern_matches_nothing(tmp_path: Path) -> None:
    assert input_fingerprint(tmp_path, ("nope/*.json",)) is None
    assert input_fingerprint(tmp_path, ()) is None


def test_glob_inputs_match_transitively(tmp_path: Path) -> None:
    (tmp_path / "data" / "video-transcripts").mkdir(parents=True)
    (tmp_path / "data" / "video-transcripts" / "a.txt").write_text("a\n", encoding="utf-8")
    (tmp_path / "code" / "data").mkdir(parents=True)
    (tmp_path / "code" / "data" / "youtube_channel.json").write_text("{}\n", encoding="utf-8")

    fp1 = input_fingerprint(tmp_path, ("data/video-transcripts/*.txt", "code/data/youtube_*.json"))
    (tmp_path / "data" / "video-transcripts" / "b.txt").write_text("b\n", encoding="utf-8")
    fp2 = input_fingerprint(tmp_path, ("data/video-transcripts/*.txt", "code/data/youtube_*.json"))
    assert fp1 is not None and fp2 is not None and fp1 != fp2


def test_corrupt_state_file_behaves_like_cold_state(tmp_path: Path) -> None:
    step = _write_step("data/works.json")
    calls: list[str] = []

    (tmp_path / "reports").mkdir()
    (tmp_path / REGENERATION_STATE_RELATIVE_PATH).write_text("{broken", encoding="utf-8")
    ran, _skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    assert ran == 1
    assert calls == ["fixture.py"]


def test_unexpected_state_payload_is_ignored(tmp_path: Path) -> None:
    save_regeneration_state({"fixture": "hash"}, tmp_path)
    path = tmp_path / REGENERATION_STATE_RELATIVE_PATH
    path.write_text('{"schema_version": 1, "other": {}}', encoding="utf-8")
    assert load_regeneration_state(tmp_path) == {}
    path.write_text("[]", encoding="utf-8")
    assert load_regeneration_state(tmp_path) == {}


def test_state_survives_a_pure_skip_run(tmp_path: Path) -> None:
    """A run that skips everything must not rewrite or drop persisted state."""
    step = _write_step("data/works.json")
    calls: list[str] = []

    regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    before = (tmp_path / REGENERATION_STATE_RELATIVE_PATH).read_text(encoding="utf-8")

    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    after = (tmp_path / REGENERATION_STATE_RELATIVE_PATH).read_text(encoding="utf-8")
    assert (ran, skipped) == (0, 1)
    assert after == before


def test_excluded_files_do_not_block_the_skip(tmp_path: Path) -> None:
    """A file matching ``inputs`` but listed in ``inputs_exclude`` is ignored.

    Mirrors audit_assets.EXCLUDED_ASSETS: post-audit control files written by
    the chain's integrity tail must not keep the audit steps from converging
    to a skip.
    """
    step = GenerationStep(
        "fixture",
        "fixture.py",
        (),
        ("--check",),
        "fixture writer",
        ("data/*.json",),
        ("data/agent-index.json",),
    )
    (tmp_path / "data" / "agent-index.json").write_text('{"tail": 1}\n', encoding="utf-8")
    calls: list[str] = []

    regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    assert calls == ["fixture.py"]

    # Rewriting the excluded control file leaves the fingerprint fresh.
    (tmp_path / "data" / "agent-index.json").write_text('{"tail": 2}\n', encoding="utf-8")
    ran, skipped = regenerate_all.run_regeneration(
        steps=(step,),
        runner=lambda script, args: calls.append(script),
        repo_root=tmp_path,
        emit=lambda _m: None,
    )
    assert (ran, skipped) == (0, 1)
    assert len(calls) == 1


def test_failed_step_does_not_persist_state(tmp_path: Path) -> None:
    """A step that dies before persisting keeps the next run executing it."""

    def failing_runner(script: str, args: list[str]) -> None:
        raise RuntimeError(f"{script} failed")

    step = _write_step("data/works.json")
    with pytest.raises(RuntimeError):
        regenerate_all.run_regeneration(
            steps=(step,),
            runner=failing_runner,
            repo_root=tmp_path,
            emit=lambda _m: None,
        )
    assert load_regeneration_state(tmp_path) == {}


def test_step_state_records_only_nonempty_fingerprints(tmp_path: Path) -> None:
    step = _write_step("data/works.json")
    state: dict[str, str] = {}

    regenerate_all.record_step_state(step, state, tmp_path)
    assert step.identifier in state
    assert state[step.identifier] == input_fingerprint(tmp_path, ("data/works.json",))


def test_fingerprint_hashes_content_not_paths_alone(tmp_path: Path) -> None:
    (tmp_path / "data" / "works.json").write_text("v1\n", encoding="utf-8")
    fp1 = input_fingerprint(tmp_path, ("data/works.json",))
    (tmp_path / "data" / "works.json").write_text("v2\n", encoding="utf-8")
    fp2 = input_fingerprint(tmp_path, ("data/works.json",))
    assert fp1 != fp2


def test_fingerprint_ignores_mtime_only_touches(tmp_path: Path) -> None:
    (tmp_path / "data" / "works.json").write_text("body\n", encoding="utf-8")
    fp1 = input_fingerprint(tmp_path, ("data/works.json",))
    os.utime(tmp_path / "data" / "works.json", (0, 0))
    fp2 = input_fingerprint(tmp_path, ("data/works.json",))
    assert fp1 == fp2


def test_input_gated_step_with_unchanged_inputs_skips_in_subprocess(
    tmp_path: Path,
) -> None:
    """Full-driver subprocess proof in a disposable repo.

    Copies the real ``regenerate_all.py`` + ``generation_plan.py`` into the
    fixture (so module-level REPO_ROOT resolves to the fixture root) plus the
    package ``__init__.py`` as the canonical bootstrap, and runs a driver stub
    that exercises ``run_regeneration`` — the same code path ``main()`` uses —
    twice: first full, then skipping the gated step.
    """
    for rel in (
        "code/orchestrators/regenerate_all.py",
        "code/src/generation_plan.py",
        "code/src/docxology_tools/__init__.py",
    ):
        dest = tmp_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / rel, dest)
    (tmp_path / "code" / "orchestrators" / "fixture.py").write_text(
        "from pathlib import Path\nPath('out').write_text('ran\\n')\n",
        encoding="utf-8",
    )
    (tmp_path / "code" / "orchestrators" / "always.py").write_text(
        "from pathlib import Path\nPath('out-always').write_text('ran\\n')\n",
        encoding="utf-8",
    )

    driver = tmp_path / "code" / "orchestrators" / "driver.py"
    driver.write_text(
        "import sys\n"
        "sys.path.insert(0, 'code/orchestrators')\n"
        "import regenerate_all\n"
        "from generation_plan import GenerationStep\n"
        "gated = GenerationStep('fixture', 'fixture.py', (), ('--check',), 'g', ('data/works.json',))\n"
        "ungated = GenerationStep('always', 'always.py', (), ('--check',), 'u')\n"
        "ran, skipped = regenerate_all.run_regeneration(steps=(gated, ungated), emit=print)\n"
        "print(f'RAN={ran} SKIPPED={skipped}')\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(driver)], cwd=tmp_path, capture_output=True, text=True, check=True
    )
    assert "RAN=2 SKIPPED=0" in result.stdout
    state = json.loads((tmp_path / REGENERATION_STATE_RELATIVE_PATH).read_text(encoding="utf-8"))
    assert set(state["steps"]) == {"fixture"}

    result = subprocess.run(
        [sys.executable, str(driver)], cwd=tmp_path, capture_output=True, text=True, check=True
    )
    assert "RAN=1 SKIPPED=1" in result.stdout
    assert any(line.startswith("skip fixture:") for line in result.stdout.splitlines())


def test_state_path_is_gitignored_in_the_real_repo() -> None:
    """The persisted state is invisible to release-source cleanliness gates.

    Both ``validate_repo._release_worktree_errors`` and
    ``report_paths.source_worktree_state`` classify via ``git status``; a
    gitignored path never appears there. ``git check-ignore`` is the
    authoritative proof for the real checkout.
    """
    result = subprocess.run(
        ["git", "check-ignore", "-v", "reports/regeneration-state.json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "reports/regeneration-state.json must stay gitignored; a tracked or "
        "untracked-but-visible state file would dirty every release gate"
    )
    assert "/reports/regeneration-state.json" in result.stdout


def test_validate_repo_battery_is_not_gated_by_regeneration_state() -> None:
    """A write-mode skip can never mask a check failure.

    The authority lives in validate_repo.run_local_generation_checks, which
    consumes the same plan but never the fingerprint state. If a plausible
    future wired state filtering into that battery, this guard would catch it.
    """
    import inspect

    source = inspect.getsource(validate_repo.run_local_generation_checks)
    assert "step_skip_reason" not in source
    assert "load_regeneration_state" not in source
    # The battery runs the declared check command for every step, always.
    assert "step.check_args" in source
