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


def test_generated_revision_date_is_deterministic_and_supports_all_calendar_months(
    tmp_path: Path,
):
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
        (
            json.dumps({"generated_at": "not-a-date", "counts": {}}),
            site_facts.generated_date,
        ),
        (
            json.dumps({"generated_at": "2026-08-25T00:00:00Z", "counts": []}),
            site_facts.counts,
        ),
    ],
)
def test_missing_or_malformed_revision_inputs_fail_closed(
    tmp_path: Path, payload: str, reader
):
    facts = tmp_path / "current-counts.json"
    facts.write_text(payload, encoding="utf-8")

    with pytest.raises(site_facts.SiteFactsError):
        reader(facts)


def test_missing_revision_input_fails_closed(tmp_path: Path):
    with pytest.raises(site_facts.SiteFactsError):
        site_facts.generated_date(tmp_path / "missing.json")


def test_site_fact_renderer_replaces_any_calendar_month_not_a_fixed_allowlist(
    tmp_path: Path,
):
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


def test_public_source_checked_date_comes_from_the_snapshot_report_not_the_build(
    tmp_path: Path,
):
    facts = tmp_path / "current-counts.json"
    facts.write_text(
        json.dumps(
            {
                "generated_at": "2026-10-05T22:00:00+00:00",
                "counts": {},
                "sources": {
                    "public_source_snapshot": "reports/public_source_snapshot_2026-09-30.json"
                },
            }
        ),
        encoding="utf-8",
    )
    assert site_facts.public_source_checked_date(facts) == "2026-09-30"
    assert site_facts.generated_date(facts) == "2026-10-05"


@pytest.mark.parametrize(
    "sources",
    [
        None,
        {},
        {"public_source_snapshot": "reports/public_source_snapshot_latest.json"},
        {"public_source_snapshot": "reports/public_source_snapshot_2026-13-40.json"},
    ],
)
def test_public_source_checked_date_fails_closed(tmp_path: Path, sources):
    facts = tmp_path / "current-counts.json"
    payload = {"generated_at": "2026-10-05T22:00:00+00:00", "counts": {}}
    if sources is not None:
        payload["sources"] = sources
    facts.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(site_facts.SiteFactsError):
        site_facts.public_source_checked_date(facts)


def _stamp_anchor(
    *, sha: str = "aaaaaaa", date: str = "2025-12-31", instant: str = "2025-12-31T23:59:59Z"
) -> str:
    return (
        f'<p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/{sha}">'
        f"build {sha} {date} · generated {instant}</a></p>"
    )


def test_render_migrates_a_legacy_stamp_on_a_hand_authored_page(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setattr(
        sync_site_facts,
        "footer_build_stamp_html",
        lambda repo_root=None: _stamp_anchor(
            sha="abc1234", date="2026-01-02", instant="2026-01-02T03:04:05Z"
        ),
    )
    page = tmp_path / "index.html"
    page.write_text(
        '<p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/8ecdaa07">'
        "build 8ecdaa07 2026-08-29</a></p>\n"
        "Last updated: December 2023\n",
        encoding="utf-8",
    )

    rendered = sync_site_facts.render(page)

    assert "build abc1234 2026-01-02 · generated 2026-01-02T03:04:05Z" in rendered
    assert "build 8ecdaa07 2026-08-29" not in rendered


def test_render_reuses_a_current_stamp_when_only_the_stamp_would_change(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setattr(
        sync_site_facts,
        "footer_build_stamp_html",
        lambda repo_root=None: _stamp_anchor(
            sha="bbbbbbb", instant="2026-02-03T04:05:06Z"
        ),
    )
    original = _stamp_anchor(sha="aaaaaaa", instant="2025-12-31T23:59:59Z") + "\n"
    page = tmp_path / "index.html"
    page.write_text(original, encoding="utf-8")

    assert sync_site_facts.render(page) == original


def test_render_refreshes_a_current_stamp_when_the_page_content_changes(
    tmp_path: Path, monkeypatch
):
    monkeypatch.setattr(
        sync_site_facts,
        "footer_build_stamp_html",
        lambda repo_root=None: _stamp_anchor(
            sha="ccccccc", date="2026-03-04", instant="2026-03-04T05:06:07Z"
        ),
    )
    page = tmp_path / "index.html"
    page.write_text(
        _stamp_anchor(sha="aaaaaaa", instant="2025-12-31T23:59:59Z")
        + "\nLast updated: December 2023\n",
        encoding="utf-8",
    )

    rendered = sync_site_facts.render(page)

    assert "build ccccccc 2026-03-04 · generated 2026-03-04T05:06:07Z" in rendered
