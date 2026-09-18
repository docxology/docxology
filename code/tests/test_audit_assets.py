"""Budget exceptions must stay narrow and explicitly documented."""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


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
