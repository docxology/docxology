"""Regression tests for deterministic revision-derived public site facts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools import site_facts  # noqa: E402
import sync_site_facts  # noqa: E402


def test_generated_revision_date_is_deterministic_and_supports_all_calendar_months(tmp_path: Path):
    facts = tmp_path / "current-counts.json"
    facts.write_text(
        json.dumps({"generated_at": "2026-12-03T12:34:56+00:00", "counts": {}}),
        encoding="utf-8",
    )

    assert site_facts.generated_date(facts) == "2026-12-03"
    assert site_facts.generated_month_year(facts) == "December 2026"


@pytest.mark.parametrize(
    ("payload", "reader"),
    [
        ("{not json}", site_facts.generated_date),
        (json.dumps({"counts": {}}), site_facts.generated_date),
        (json.dumps({"generated_at": "not-a-date", "counts": {}}), site_facts.generated_date),
        (json.dumps({"generated_at": "2026-08-25T00:00:00Z", "counts": []}), site_facts.counts),
    ],
)
def test_missing_or_malformed_revision_inputs_fail_closed(tmp_path: Path, payload: str, reader):
    facts = tmp_path / "current-counts.json"
    facts.write_text(payload, encoding="utf-8")

    with pytest.raises(site_facts.SiteFactsError):
        reader(facts)


def test_missing_revision_input_fails_closed(tmp_path: Path):
    with pytest.raises(site_facts.SiteFactsError):
        site_facts.generated_date(tmp_path / "missing.json")


def test_site_fact_renderer_replaces_any_calendar_month_not_a_fixed_allowlist(tmp_path: Path):
    page = tmp_path / "index.html"
    page.write_text(
        "Data refreshed January 2024\nLast updated: December 2023\n",
        encoding="utf-8",
    )

    rendered = sync_site_facts.render(page)
    expected_month = site_facts.generated_month_year()
    assert rendered.count(f"Data refreshed {expected_month}") == 2
    assert "January 2024" not in rendered
    assert "December 2023" not in rendered
