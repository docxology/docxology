"""Tests for parallel public-source refresh and --cache-reports reuse."""

from __future__ import annotations

import json
import sys
import unittest.mock as mock
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

import refresh_public_source_inventory as inv  # noqa: E402
import refresh_public_sources as rps  # noqa: E402

def _today() -> str:
    """Runtime date — a module-level date goes stale across a midnight pytest run."""
    return __import__("datetime").datetime.now(__import__("datetime").timezone.utc).date().isoformat()


def _ok_section(label: str, url: str = "https://example.com") -> dict:
    return {"label": label, "url": url, "ok": True, "items": [{"status": 200, "title": label}]}


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


# --- 1. parallel refresh: output equality with sequential reference ----------


class _SerialPool:
    """ThreadPoolExecutor stand-in that runs tasks inline (sequential reference)."""

    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def map(self, fn, iterable):
        return map(fn, iterable)


def test_parallel_refresh_output_identical_to_sequential(monkeypatch):
    """Threaded build_report output is byte-identical (mod timestamps) to the sequential run."""
    captured_urls = []

    def fake_fetch_json(url, **kwargs):
        captured_urls.append(url)
        return {"login": url, "public_repos": 1, "updated_at": "t", "html_url": url,
                "full_name": url, "stargazers_count": 0, "language": "Python",
                "message": {"total-results": 3},
                "esearchresult": {"count": "2", "idlist": ["1", "2"]},
                "hitCount": 7, "group": [{"g": 1}, {"g": 2}],
                "hits": {"total": {"value": 9}, "hits": [{"metadata": {"title": "T", "doi": "d",
                    "publication_date": "2026", "resource_type": {"title": "article"},
                    "creators": [{"name": "x"}]}}]}}

    monkeypatch.setattr(rps, "fetch_json", fake_fetch_json)

    threaded = rps.build_report()
    assert len(captured_urls) == len(rps.expected_check_labels())

    captured_urls.clear()
    with mock.patch.object(rps, "ThreadPoolExecutor", _SerialPool):
        sequential = rps.build_report()

    assert [c["label"] for c in threaded["checks"]] == list(rps.expected_check_labels())
    assert threaded["checks"] == sequential["checks"]
    assert threaded["facts"] == sequential["facts"]
    assert threaded["date"] == sequential["date"]
    for key in ("source_commit", "note", "facts"):
        assert threaded[key] == sequential[key]
    assert all(c["ok"] for c in threaded["checks"])
    del threaded["generated_at"], sequential["generated_at"]
    assert json.dumps(threaded, sort_keys=False) == json.dumps(sequential, sort_keys=False)


# --- 2. cache reuse ----------------------------------------------------------


def _setup_cache(tmp_path, monkeypatch, *, inventory_at: str, snapshot_at: str | None,
                 warnings: int = 0):
    reports = tmp_path / "reports"
    labels = ["ORCID work groups", "Crossref ORCID DOI records"]
    sections = [_ok_section(label) for label in labels]
    for i in range(warnings):
        sections.append({"label": f"warned-{i}", "url": "https://x", "ok": False,
                         "error": "HTTPError: 500", "items": []})
    _write_json(reports / f"public_source_inventory_{_today()}.json", {
        "generated_at": inventory_at, "sections": sections,
        "counts": {s["label"]: len(s["items"]) for s in sections},
    })
    if snapshot_at is not None:
        _write_json(reports / f"public_source_snapshot_{_today()}.json", {
            "generated_at": snapshot_at, "checks": [],
        })
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(inv, "latest_report", lambda pattern, required=False: _latest(pattern, reports))
    return reports, sections


def _latest(pattern: str, reports: Path):
    matches = sorted(reports.glob(pattern), reverse=True)
    return matches[0] if matches else None


def test_cache_reuse_same_day(tmp_path, monkeypatch):
    """Same-day clean cache is reused verbatim; anchors field records provenance; no fetch."""
    inventory_at = f"{_today()}T12:00:00Z"
    reports, sections = _setup_cache(tmp_path, monkeypatch, inventory_at=inventory_at,
                                     snapshot_at=f"{_today()}T12:30:00Z")

    def boom(*a, **k):
        raise AssertionError("live fetch must not run on cache reuse")

    for name in ("orcid_works", "crossref_orcid", "pubmed_exact_author", "europe_pmc_exact_author",
                 "wikidata_person", "dblp_author_profile", "researchgate_profile", "sciprofiles_profile",
                 "philpeople_profile", "semantic_scholar_author_search", "openalex_author_advisory",
                 "github_profile", "public_page"):
        monkeypatch.setattr(inv, name, boom)

    report = inv.build_report(cache_reports=True)
    assert report["sections"] == sections
    assert report["counts"] == {s["label"]: len(s["items"]) for s in sections}
    anchor = report["anchors"]
    assert anchor["mode"] == "cache-reuse"
    assert anchor["source_report"] == f"reports/public_source_inventory_{_today()}.json"
    assert anchor["source_generated_at"] == inventory_at
    assert anchor["cached_section_labels"] == [s["label"] for s in sections]
    assert anchor["source_snapshot_generated_at"] == f"{_today()}T12:30:00Z"


def test_cache_reuse_without_snapshot(tmp_path, monkeypatch):
    """Missing snapshot report is optional: reuse still fires."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T09:00:00Z", snapshot_at=None)
    report = inv.build_report(cache_reports=True)
    assert report["anchors"]["mode"] == "cache-reuse"


LIVE_FETCHERS = (
    "orcid_works", "crossref_orcid", "pubmed_exact_author", "europe_pmc_exact_author",
    "wikidata_person", "dblp_author_profile", "researchgate_profile", "sciprofiles_profile",
    "philpeople_profile", "semantic_scholar_author_search", "openalex_author_advisory",
)


def _stub_live_fetchers(monkeypatch, marker):
    """Patch every live fetcher with a stub that records it ran."""
    def stub(*a, **k):
        marker.append(a and a[0] or k.get("label", "fetch"))
        return {"label": "stub", "url": "u", "ok": True, "items": []}
    for name in LIVE_FETCHERS:
        monkeypatch.setattr(inv, name, stub)
    monkeypatch.setattr(inv, "zenodo_records", stub)
    monkeypatch.setattr(inv, "github_profile", stub)
    monkeypatch.setattr(inv, "public_page", stub)


def test_cache_reuse_stale_falls_back_live(tmp_path, monkeypatch):
    """A stale cache is ignored: live fetch runs, no anchors field."""
    _setup_cache(tmp_path, monkeypatch, inventory_at="2000-01-01T12:00:00Z", snapshot_at=None)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report(cache_reports=True)
    assert len(marker) == 20, "stale cache must trigger the full live fetch"
    assert "anchors" not in report


def test_cache_reuse_warning_fails_closed(tmp_path, monkeypatch):
    """ANY warning in the cached report forces a live fetch (fail closed)."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z",
                 snapshot_at=None, warnings=1)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report(cache_reports=True)
    assert len(marker) == 20, "warned cache must trigger the full live fetch"
    assert "anchors" not in report


def test_cache_force_accepts_warnings(tmp_path, monkeypatch):
    """--force reuses a warned cache and records forced-reuse provenance."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z",
                 snapshot_at=None, warnings=1)
    report = inv.build_report(cache_reports=True, force=True)
    anchor = report["anchors"]
    assert anchor["mode"] == "forced-reuse"
    assert anchor["warnings_accepted"] == ["warned-0"]


def test_no_flag_never_reads_cache(tmp_path, monkeypatch):
    """Default (no --cache-reports) always live-fetches, even with a clean same-day cache."""
    _setup_cache(tmp_path, monkeypatch, inventory_at=f"{_today()}T12:00:00Z", snapshot_at=None)
    marker: list = []
    _stub_live_fetchers(monkeypatch, marker)
    report = inv.build_report()
    assert len(marker) == 20, "default run live-fetches even with a clean same-day cache"
    assert "anchors" not in report


def test_main_check_offline(tmp_path, monkeypatch, capsys):
    """--check stays offline: validates the cached report without any fetch."""
    reports = tmp_path / "reports"
    _write_json(reports / f"public_source_inventory_{_today()}.json", {
        "generated_at": f"{_today()}T12:00:00Z", "sections": [_ok_section("L")],
    })
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--check"])
    inv.main()
