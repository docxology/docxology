from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_public_entry_navigation_check_passes():
    result = subprocess.run(
        ["python3", "code/orchestrators/ensure_agent_navigation.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_entry_pages_have_visible_agent_map_links():
    for path in REPO_ROOT.glob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "<nav" not in text.lower() or 'name="robots" content="noindex' in text.lower():
            continue
        assert 'href="data/agent-index.json"' in text, path
