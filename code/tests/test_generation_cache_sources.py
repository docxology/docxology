"""Cached generation must observe implementation changes as well as data."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402,F401 (canonical orchestrator bootstrap)
import regenerate_all  # noqa: E402
from docxology_tools.generation_plan import (  # noqa: E402
    LOCAL_GENERATION_STEPS,
    GenerationStep,
    effective_step_inputs,
    load_regeneration_state,
    step_input_fingerprint,
    step_skip_reason,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHED_STEPS = tuple(step for step in LOCAL_GENERATION_STEPS if step.inputs)
IMPORTED_RENDERERS = (
    ("sync-publications", "export_bibliography.py"),
    ("sync-publications", "build_work_pages.py"),
    ("sync-publications-final", "export_bibliography.py"),
    ("sync-publications-final", "build_work_pages.py"),
    ("github-inventory-pages", "build_github_inventory.py"),
    ("paper-pages", "build_work_pages.py"),
    ("accessibility-first", "deploy_seo_security.py"),
    ("accessibility-final", "deploy_seo_security.py"),
    ("domain-feeds", "build_domain_pages.py"),
)


def _seed_sources(repo: Path, step: GenerationStep) -> None:
    """Give each declared pattern a real file in a disposable source tree."""
    for pattern in effective_step_inputs(step):
        if pattern == "code/src/**/*.py":
            relative = "code/src/site_nav.py"
        else:
            relative = pattern.replace("[0-9]*", "2026-01-01")
            relative = re.sub(r"\[([A-Za-z]+)\]", lambda m: m.group(1)[0], relative)
            relative = relative.replace("**", "fixture").replace("*", "fixture")
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# original fixture source\n", encoding="utf-8")


def _run(step: GenerationStep, repo: Path, calls: list[str]) -> tuple[int, int]:
    return regenerate_all.run_regeneration(
        steps=(step,), runner=lambda script, _args: calls.append(script),
        repo_root=repo, emit=lambda _message: None,
    )


@pytest.mark.parametrize("step", CACHED_STEPS, ids=lambda step: step.identifier)
def test_every_cached_writer_reruns_after_own_or_shared_source_change(tmp_path, step):
    _seed_sources(tmp_path, step)
    calls: list[str] = []
    assert _run(step, tmp_path, calls) == (1, 0)
    assert _run(step, tmp_path, calls) == (0, 1)

    # Data and templates stay fixed throughout: the driver must notice code.
    for relative in (f"code/orchestrators/{step.script}", "code/src/site_nav.py"):
        source = tmp_path / relative
        os.utime(source, (0, 0))
        assert _run(step, tmp_path, calls) == (0, 1)
        source.write_text(source.read_text() + "# changed implementation\n", encoding="utf-8")
        assert _run(step, tmp_path, calls) == (1, 0)
        assert _run(step, tmp_path, calls) == (0, 1)
    assert calls == [step.script] * 3


@pytest.mark.parametrize("identifier,script", IMPORTED_RENDERERS)
def test_imported_orchestrator_changes_rerun_the_actual_plan_stage(tmp_path, identifier, script):
    step = next(step for step in LOCAL_GENERATION_STEPS if step.identifier == identifier)
    _seed_sources(tmp_path, step)
    calls: list[str] = []
    assert _run(step, tmp_path, calls) == (1, 0)
    assert _run(step, tmp_path, calls) == (0, 1)
    source = tmp_path / "code/orchestrators" / script
    assert source.is_file(), "the imported implementation must be an explicit cache input"
    source.write_text(source.read_text() + "# changed imported renderer\n", encoding="utf-8")
    assert _run(step, tmp_path, calls) == (1, 0)
    assert _run(step, tmp_path, calls) == (0, 1)
    assert calls == [step.script, step.script]


@pytest.mark.parametrize("removed", ["code/orchestrators/build_updates_page.py", "code/src"])
def test_missing_implementation_source_fails_closed(tmp_path, removed):
    step = next(step for step in LOCAL_GENERATION_STEPS if step.identifier == "updates-page")
    _seed_sources(tmp_path, step)
    calls: list[str] = []
    assert _run(step, tmp_path, calls) == (1, 0)
    state = load_regeneration_state(tmp_path)
    source = tmp_path / removed
    if source.is_dir():
        shutil.rmtree(source)
    else:
        source.unlink()
    assert step_input_fingerprint(step, tmp_path) is None
    assert step_skip_reason(step, state, tmp_path) is None
    assert _run(step, tmp_path, calls) == (1, 0)
    assert _run(step, tmp_path, calls) == (1, 0)


@pytest.mark.parametrize("changed", ["writer", "navigation", "thinking"])
def test_real_updates_renderer_rebuilds_from_changed_source_in_subprocess(tmp_path, changed):
    """Run the real generator/driver and inspect its changed HTML bytes."""
    shutil.copytree(
        REPO_ROOT / "code/src", tmp_path / "code/src", ignore=shutil.ignore_patterns("__pycache__"),
    )
    for name in ("regenerate_all.py", "build_updates_page.py"):
        target = tmp_path / "code/orchestrators" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / "code/orchestrators" / name, target)
    (tmp_path / "CHANGELOG.md").write_text("## 2026-10-02\n- Public fixture update.\n")
    (tmp_path / "pages").mkdir()
    (tmp_path / "pages/THINKING_LOG.md").write_text(
        "- 2026-10-02: Original public fixture thought.\n", encoding="utf-8",
    )
    driver = tmp_path / "code/orchestrators/driver.py"
    driver.write_text(
        "import regenerate_all\n"
        "from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS\n"
        "step = next(s for s in LOCAL_GENERATION_STEPS if s.identifier == 'updates-page')\n"
        "print(regenerate_all.run_regeneration(steps=(step,)))\n",
        encoding="utf-8",
    )
    # The stamp is a public fixture value; parent-shell source overrides must
    # not make this test observe the working checkout or changing commit data.
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(BUILD_SHA="abcdef0", BUILD_DATE="2026-10-02", PYTHONDONTWRITEBYTECODE="1")

    def run_driver() -> str:
        return subprocess.run(
            [sys.executable, str(driver)], cwd=tmp_path, env=env,
            capture_output=True, text=True, check=True, timeout=30,
        ).stdout

    assert "(1, 0)" in run_driver()
    before = (tmp_path / "updates.html").read_bytes()
    assert "(0, 1)" in run_driver()
    assert (tmp_path / "updates.html").read_bytes() == before
    if changed == "writer":
        source = tmp_path / "code/orchestrators/build_updates_page.py"
        old, new = "<h1>Updates</h1>", "<h1>Fixture refreshed updates</h1>"
    elif changed == "navigation":
        source = tmp_path / "code/src/site_nav.py"
        old, new = "nav-20261002", "nav-fixture-20261002"
    else:
        source = tmp_path / "pages/THINKING_LOG.md"
        old, new = "Original public fixture thought.", "Refreshed public fixture thought."
    content = source.read_text(encoding="utf-8")
    assert old in content
    source.write_text(content.replace(old, new), encoding="utf-8")
    assert "(1, 0)" in run_driver()
    after = (tmp_path / "updates.html").read_bytes()
    assert after != before and new.encode() in after
    assert "(0, 1)" in run_driver()
    assert (tmp_path / "updates.html").read_bytes() == after
