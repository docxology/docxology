"""The documented regeneration chain must be the chain that actually runs.

`CLAUDE.md` spells out `regenerate_all.py`'s step order in prose, which is the
first thing an agent reads before touching generated artifacts. That prose had
silently fallen nine steps behind `LOCAL_GENERATION_STEPS` — it still listed a
generator deleted on 2026-08-28 and omitted ten that had been added since — so
an agent following it would have rebuilt the site incorrectly and trusted the
result. The order is machine-checkable, so it is machine-checked.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402

CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
_CHAIN_INTRO = "Internally it runs, in order:\n"
_SCRIPT = re.compile(r"`([a-z0-9_]+\.py)[^`]*`")


def _documented_chain() -> list[str]:
    text = CLAUDE_MD.read_text(encoding="utf-8")
    assert _CHAIN_INTRO in text, "CLAUDE.md no longer documents the regeneration chain"
    block = text.split(_CHAIN_INTRO, 1)[1].split("\n\n", 1)[0]
    return _SCRIPT.findall(block)


def test_claude_md_chain_matches_the_generation_plan():
    assert _documented_chain() == [step.script for step in LOCAL_GENERATION_STEPS]


def test_destructive_pruning_stays_out_of_the_documented_chain():
    """A rebuild that deletes report artifacts is not idempotent."""
    assert "prune_old_reports.py" not in _documented_chain()
    assert "prune_old_reports.py" not in {step.script for step in LOCAL_GENERATION_STEPS}


def test_every_documented_step_is_an_executable_orchestrator():
    orchestrators = REPO_ROOT / "code" / "orchestrators"
    missing = [name for name in _documented_chain() if not (orchestrators / name).is_file()]
    assert missing == [], f"CLAUDE.md names generators that do not exist: {missing}"
