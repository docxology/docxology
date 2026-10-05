"""Agent guidance uses the live plan instead of duplicating its script list."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402

CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
PLAN_COMMAND = "uv run python3 code/orchestrators/regenerate_all.py --list"


def test_agent_guidance_points_to_the_single_live_plan():
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert PLAN_COMMAND in text
    assert "code/src/generation_plan.py" in text
    assert "Internally it runs, in order:" not in text


def test_actual_plan_command_matches_declarations_without_writing_cache():
    cache = REPO_ROOT / "reports/regeneration-state.json"
    before = cache.read_bytes() if cache.exists() else None
    result = subprocess.run(
        [sys.executable, "code/orchestrators/regenerate_all.py", "--list"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True, timeout=15,
    )
    scripts = re.findall(r"(?m)^\s*\d+\.\s+([a-z0-9_]+\.py)\b", result.stdout)
    assert scripts == [step.script for step in LOCAL_GENERATION_STEPS]
    assert (cache.read_bytes() if cache.exists() else None) == before


def test_destructive_pruning_stays_out_of_the_live_plan():
    """A rebuild that deletes report artifacts is not idempotent."""
    assert "prune_old_reports.py" not in {step.script for step in LOCAL_GENERATION_STEPS}
