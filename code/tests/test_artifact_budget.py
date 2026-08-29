"""Tests for the artifact budget gate (code/src/artifact_budget.py)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from artifact_budget import (  # noqa: E402
    ArtifactBudgetError,
    artifact_mib_from_report,
    enforce_budget,
    latest_growth_report,
)


def _write_report(tmp_path: Path, mib: float, name: str = "pages_artifact_growth_2026-08-29.json") -> Path:
    path = tmp_path / "reports" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"artifact_mib": mib, "generated_at": "2026-08-29T00:00:00Z"}), encoding="utf-8")
    return path


def test_latest_growth_report_picks_newest(tmp_path: Path) -> None:
    _write_report(tmp_path, 800.0, "pages_artifact_growth_2026-08-28.json")
    newest = _write_report(tmp_path, 810.0, "pages_artifact_growth_2026-08-29.json")
    assert latest_growth_report(tmp_path) == newest


def test_latest_growth_report_missing(tmp_path: Path) -> None:
    with pytest.raises(ArtifactBudgetError, match="no artifact growth reports"):
        latest_growth_report(tmp_path)


def test_artifact_mib_reads_payload(tmp_path: Path) -> None:
    path = _write_report(tmp_path, 821.66)
    assert artifact_mib_from_report(path) == pytest.approx(821.66)


def test_enforce_budget_passes_under_budget(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_report(tmp_path, 821.66)
    assert enforce_budget(tmp_path) == pytest.approx(821.66)
    assert "Artifact budget OK" in capsys.readouterr().out


def test_enforce_budget_fails_over_budget(tmp_path: Path) -> None:
    _write_report(tmp_path, 901.5)
    with pytest.raises(ArtifactBudgetError, match="ARTIFACT BUDGET EXCEEDED"):
        enforce_budget(tmp_path)
