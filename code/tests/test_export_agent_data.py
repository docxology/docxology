"""Tests for lazy IO in export_agent_data."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"


def test_import_does_not_read_current_counts():
    """A fresh interpreter must not open the lazy current-counts input."""
    script = f"""
import importlib
import sys
from pathlib import Path

def reject_current_counts(event, args):
    if event != "open" or not args:
        return
    candidate = args[0]
    if isinstance(candidate, bytes):
        candidate = candidate.decode("utf-8", errors="surrogateescape")
    if isinstance(candidate, (str, Path)) and Path(candidate).name == "current-counts.json":
        raise AssertionError("current-counts.json must not be read at import")

sys.addaudithook(reject_current_counts)
sys.path.insert(0, {str(ORCH_DIR)!r})
sys.path.insert(0, {str(REPO_ROOT / "code" / "src")!r})
module = importlib.import_module("export_agent_data")
assert not hasattr(module, "_WORK_COUNT")
assert not hasattr(module, "CLAIMS")
assert callable(module._claims)
assert callable(module._current_counts_payload)
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"{result.stdout}\n{result.stderr}"
