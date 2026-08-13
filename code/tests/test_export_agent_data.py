"""Tests for lazy IO in export_agent_data."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"


def test_import_does_not_read_current_counts(monkeypatch: pytest.MonkeyPatch):
    orig = Path.read_text

    def guarded(self: Path, *args, **kwargs):
        if self.name == "current-counts.json":
            raise AssertionError("current-counts.json must not be read at import")
        return orig(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded)
    sys.path.insert(0, str(ORCH_DIR))
    sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
    sys.modules.pop("export_agent_data", None)
    module = importlib.import_module("export_agent_data")
    assert not hasattr(module, "_WORK_COUNT")
    assert not hasattr(module, "CLAIMS")
    assert callable(module._claims)
    assert callable(module._current_counts_payload)
