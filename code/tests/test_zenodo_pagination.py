"""Public Zenodo readers must never bless a partial search as complete."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlsplit

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import refresh_public_source_inventory as inventory  # noqa: E402
import sync_paired_publications as pairing  # noqa: E402

ZENODO_LABEL = "Zenodo ORCID-linked records"


def _record(record_id: int) -> dict:
    return {
        "id": record_id,
        "doi": f"10.5281/zenodo.{record_id}",
        "metadata": {
            "title": f"Paper {record_id}",
            "publication_date": "2026-11-01",
            "resource_type": {"type": "publication", "subtype": "article"},
        },
    }


def _page(records: list, total: object) -> dict:
    return {"hits": {"hits": records, "total": total}}


class _Pages:
    def __init__(self, payloads: list):
        self.payloads = payloads
        self.calls: list[str] = []

    def __call__(self, url: str):
        query = parse_qs(urlsplit(url).query)
        assert query["sort"] == ["mostrecent"]
        assert query["size"] == ["25"]
        assert query["q"] == ["test query"]
        assert query["page"] == [str(len(self.calls) + 1)]
        self.calls.append(url)
        if len(self.calls) > len(self.payloads):
            return _page([], 0)
        return self.payloads[len(self.calls) - 1]


@pytest.fixture(params=("pairing", "inventory"))
def reader(request):
    return request.param


def _read(reader: str, monkeypatch, fetch):
    if reader == "pairing":
        monkeypatch.setattr(pairing, "fetch_json", fetch)
        return pairing.fetch_zenodo_query("test query")
    monkeypatch.setattr(inventory, "fetch_json", fetch)
    return inventory.zenodo_records(ZENODO_LABEL, "test query")


def _reject(reader: str, monkeypatch, fetch):
    if reader == "pairing":
        with pytest.raises(ValueError):
            _read(reader, monkeypatch, fetch)
    else:
        result = _read(reader, monkeypatch, fetch)
        assert result["ok"] is False
        assert result["items"] == []
        assert result["error"]


@pytest.mark.parametrize("total_object", (False, True))
def test_complete_paginated_scan_preserves_order_and_exact_total(
    reader, monkeypatch, total_object
):
    total = {"value": 26, "relation": "eq"} if total_object else 26
    fetch = _Pages([_page([_record(i) for i in range(1, 26)], total), _page([_record(26)], total)])
    result = _read(reader, monkeypatch, fetch)
    if reader == "pairing":
        assert [row.record_id for row in result] == [str(i) for i in range(1, 27)]
    else:
        assert result["ok"] is True
        assert result["total"] == 26
        assert [row["title"] for row in result["items"]] == [f"Paper {i}" for i in range(1, 27)]
    assert len(fetch.calls) == 2


def test_complete_full_page_does_not_fetch_an_extra_page(reader, monkeypatch):
    fetch = _Pages([_page([_record(i) for i in range(1, 26)], 25)])
    result = _read(reader, monkeypatch, fetch)
    if reader == "pairing":
        assert len(result) == 25
    else:
        assert result["ok"] is True
        assert result["total"] == len(result["items"]) == 25
    assert len(fetch.calls) == 1


def test_explicit_zero_total_is_a_complete_empty_scan(reader, monkeypatch):
    fetch = _Pages([_page([], 0)])
    result = _read(reader, monkeypatch, fetch)
    if reader == "pairing":
        assert result == []
    else:
        assert result["ok"] is True
        assert result["total"] == 0
        assert result["items"] == []
    assert len(fetch.calls) == 1


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"hits": []},
        {"hits": {"hits": [], "total": None}},
        {"hits": {"hits": []}},
        {"hits": {"hits": {}, "total": 1}},
        _page([None], 1),
        _page([{"metadata": {"title": "Missing identity"}}], 1),
    ],
)
def test_malformed_search_is_unavailable_instead_of_empty(reader, monkeypatch, payload):
    _reject(reader, monkeypatch, _Pages([payload]))


@pytest.mark.parametrize(
    "total",
    [True, -1, "1", {"value": True}, {"value": -1}, {"value": 1, "relation": "gte"}, {"value": 1, "relation": "unknown"}],
)
def test_only_exact_nonnegative_integer_totals_can_certify_a_scan(reader, monkeypatch, total):
    _reject(reader, monkeypatch, _Pages([_page([_record(1)], total)]))


def test_empty_page_before_advertised_total_is_incomplete(reader, monkeypatch):
    fetch = _Pages([_page([_record(i) for i in range(1, 26)], 26), _page([], 26)])
    _reject(reader, monkeypatch, fetch)
    assert len(fetch.calls) == 2


def test_short_page_before_advertised_total_is_incomplete(reader, monkeypatch):
    fetch = _Pages([_page([_record(i) for i in range(1, 11)], 26)])
    _reject(reader, monkeypatch, fetch)
    assert len(fetch.calls) == 1


def test_repeated_records_do_not_satisfy_advertised_total(reader, monkeypatch):
    fetch = _Pages([_page([_record(i) for i in range(1, 26)], 26), _page([_record(25)], 26)])
    _reject(reader, monkeypatch, fetch)


def test_duplicate_identity_inside_one_page_is_incomplete(reader, monkeypatch):
    _reject(reader, monkeypatch, _Pages([_page([_record(1), _record(1)], 2)]))


def test_count_above_total_is_inconsistent(reader, monkeypatch):
    _reject(reader, monkeypatch, _Pages([_page([_record(1), _record(2)], 1)]))


def test_total_changes_during_scan_require_a_fresh_observation(reader, monkeypatch):
    fetch = _Pages([_page([_record(i) for i in range(1, 26)], 26), _page([_record(26)], 27)])
    _reject(reader, monkeypatch, fetch)


def test_search_bound_refuses_partial_success(reader, monkeypatch):
    calls = []

    def fetch(url):
        page = int(parse_qs(urlsplit(url).query)["page"][0])
        calls.append(page)
        assert len(calls) <= 20, "Zenodo search exceeded its request bound"
        return _page([_record(i) for i in range((page - 1) * 25 + 1, page * 25 + 1)], 501)

    _reject(reader, monkeypatch, fetch)
    assert 1 <= len(calls) <= 20


def _summary(record_id: int) -> dict:
    return {
        "title": f"Paper {record_id}",
        "doi": f"10.5281/zenodo.{record_id}",
        "publication_date": "2026-11-01",
        "resource_type": "publication",
        "version": "1.0",
    }


def _cached_inventory(tmp_path, monkeypatch, section):
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    report = tmp_path / "reports" / f"public_source_inventory_{today}.json"
    report.parent.mkdir()
    report.write_text(json.dumps({"generated_at": f"{today}T00:00:00Z", "sections": [section]}), encoding="utf-8")
    monkeypatch.setattr(inventory, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(inventory, "latest_report", lambda pattern, **kwargs: report if pattern.startswith("public_source_inventory_") else None)
    return today, report


@pytest.mark.parametrize("force", (False, True))
@pytest.mark.parametrize("total", (2, True, "1", None))
def test_incomplete_zenodo_inventory_cache_cannot_be_reused(tmp_path, monkeypatch, force, total):
    section = {"label": ZENODO_LABEL, "url": "https://zenodo.org/api/records", "ok": True, "total": total, "items": [_summary(1)]}
    today, _ = _cached_inventory(tmp_path, monkeypatch, section)
    assert inventory.load_cached_sections(today, force=force) == ([], None)


def test_complete_zenodo_inventory_cache_still_reuses_same_day_observation(tmp_path, monkeypatch):
    section = {"label": ZENODO_LABEL, "url": "https://zenodo.org/api/records", "ok": True, "total": 1, "items": [_summary(1)]}
    today, _ = _cached_inventory(tmp_path, monkeypatch, section)
    sections, anchor = inventory.load_cached_sections(today)
    assert sections == [section]
    assert anchor["mode"] == "cache-reuse"


def test_inventory_check_rejects_a_cached_zenodo_count_mismatch(tmp_path, monkeypatch):
    section = {"label": ZENODO_LABEL, "url": "https://zenodo.org/api/records", "ok": True, "total": 2, "items": [_summary(1)]}
    _, report = _cached_inventory(tmp_path, monkeypatch, section)
    monkeypatch.setattr(sys, "argv", ["inventory", "--check", "--output", str(report)])
    with pytest.raises(SystemExit, match="Zenodo"):
        inventory.main()


@pytest.mark.parametrize("force", (False, True))
@pytest.mark.parametrize("items", ([None], [{"title": "Missing DOI"}], [_summary(1), _summary(1)]))
def test_malformed_or_duplicate_cached_zenodo_identity_is_unavailable(tmp_path, monkeypatch, force, items):
    section = {"label": ZENODO_LABEL, "url": "https://zenodo.org/api/records", "ok": True, "total": len(items), "items": items}
    today, _ = _cached_inventory(tmp_path, monkeypatch, section)
    assert inventory.load_cached_sections(today, force=force) == ([], None)
