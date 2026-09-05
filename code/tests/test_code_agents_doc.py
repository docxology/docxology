"""`code/AGENTS.md` is the agent-facing map of `code/`; it must match the tree.

Two claims in that file have already rotted once each: the ``report_paths``
importer count drifted "~20" → "~26" → 31 while nobody was looking, and a
renamed module leaves a dead row in the layout table that reads as authoritative
to the next agent. Both are cheap to check mechanically, so they are checked
mechanically instead of by review.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CODE_AGENTS = REPO_ROOT / "code" / "AGENTS.md"
_TABLE_PATH = re.compile(r"^\| `([^`]+)` \|")
_IMPORTER_CLAIM = re.compile(r"imported by ~?(\d+) orchestrators")


def _layout_paths() -> list[str]:
    """Every backticked path in the leading column of the layout table."""
    rows: list[str] = []
    for line in CODE_AGENTS.read_text(encoding="utf-8").splitlines():
        match = _TABLE_PATH.match(line)
        if match and "/" in match.group(1):
            rows.append(match.group(1))
    return rows


def test_every_documented_code_path_exists():
    documented = _layout_paths()
    assert documented, "the code/AGENTS.md layout table has no path rows"
    missing = [rel for rel in documented if not (REPO_ROOT / "code" / rel).exists()]
    assert missing == [], f"code/AGENTS.md documents paths that no longer exist: {missing}"


def test_report_paths_importer_count_is_current():
    text = CODE_AGENTS.read_text(encoding="utf-8")
    claim = _IMPORTER_CLAIM.search(text)
    assert claim, "code/AGENTS.md no longer states the report_paths importer count"
    importers = [
        path
        for path in sorted((REPO_ROOT / "code" / "orchestrators").glob("*.py"))
        if re.search(r"^\s*(from report_paths import|import report_paths)",
                     path.read_text(encoding="utf-8"), re.MULTILINE)
    ]
    assert int(claim.group(1)) == len(importers), (
        f"code/AGENTS.md says {claim.group(1)} report_paths importers; the tree has "
        f"{len(importers)}"
    )
