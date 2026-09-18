"""Tests for GSC follow-up preflight orchestrator."""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from gsc_followup_preflight import (  # noqa: E402
    MANUAL_STEPS,
    build_report,
    local_checks,
)
from docxology_tools.sitemap_policy import gsc_priority_urls  # noqa: E402


def test_manual_steps_cover_plan_todos():
    ids = {step["id"] for step in MANUAL_STEPS}
    assert ids == {
        "gsc-sitemap",
        "gsc-index-hubs",
        "gsc-validate-redirect",
        "gsc-validate-canonical",
        "gsc-validate-404",
        "gsc-monitor",
    }


def test_local_checks_pass_on_repo():
    rows = local_checks(REPO_ROOT)
    assert rows
    assert all(row["ok"] for row in rows), rows


def test_build_report_skip_live_preflight_ok():
    report = build_report(REPO_ROOT, skip_live=True)
    assert report["preflight_ok"] is True
    assert report["priority_urls"] == gsc_priority_urls()
    assert "https://danielarifriedman.com/repositories.html" in report["priority_urls"]
    assert "https://danielarifriedman.com/videos.html" in report["priority_urls"]
