"""Budget exceptions must stay narrow and explicitly documented."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import audit_assets  # noqa: E402


def test_publications_ssr_budget_exception_is_explicit_and_bounded():
    exception = audit_assets.ASSET_BUDGET_EXCEPTIONS["publications.html"]
    assert exception["budget_bytes"] == 600_000
    assert "SSR" in str(exception["reason"])
    assert exception["approved_in"] == "docs/operations/github-pages-artifact.md"


def test_asset_inventory_records_baseline_and_exception():
    publications = next(item for item in audit_assets.iter_assets() if item["path"] == "publications.html")
    assert publications["baseline_budget_bytes"] == 500_000
    assert publications["budget_bytes"] == 600_000
    assert publications["budget_exception"] == audit_assets.ASSET_BUDGET_EXCEPTIONS["publications.html"]
