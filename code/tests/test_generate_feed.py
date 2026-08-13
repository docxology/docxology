"""Tests for RSS feed generation."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import generate_feed as gf  # noqa: E402
from generate_feed import _year_key, render  # noqa: E402

STABLE_GUIDS = (
    "site-update-2026-05-15-repositories",
    "site-update-2026-05-13-discovery",
    "site-update-2026-05-13-works",
)

SITE_UPDATES = [
    {
        "title": "Repository inventory and evidence layer refreshed",
        "link": "https://danielarifriedman.com/repositories.html",
        "guid": STABLE_GUIDS[0],
        "description": "Inventory refresh.",
        "pub_date": "2026-05-15",
    },
    {
        "title": "Discovery, citation, evidence, and domain pages expanded",
        "link": "https://danielarifriedman.com/discovery.html",
        "guid": STABLE_GUIDS[1],
        "description": "Discovery pages.",
        "pub_date": "2026-05-13",
    },
    {
        "title": "Per-work landing pages and search index generated",
        "link": "https://danielarifriedman.com/works/",
        "guid": STABLE_GUIDS[2],
        "description": "Work pages.",
        "pub_date": "2026-05-13",
    },
]


def _write_feed_inputs(tmp_path: Path, *, site_updates: list[dict] | None) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "works.json").write_text(
        json.dumps(
            {
                "works": [
                    {
                        "year": 2026,
                        "num": 1,
                        "title": "Alpha",
                        "citation_key": "Alpha2026",
                        "type": "Paper",
                        "venue": "Zenodo",
                        "domain_name": "Test",
                    },
                    {
                        "year": "n.d.",
                        "num": 2,
                        "title": "Undated",
                        "citation_key": "Undated",
                        "type": "Paper",
                        "venue": "Zenodo",
                        "domain_name": "Test",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    if site_updates is not None:
        (data / "site-updates.json").write_text(
            json.dumps(site_updates), encoding="utf-8"
        )


def test_generate_feed_guids_and_year_key_sort(tmp_path: Path, monkeypatch):
    _write_feed_inputs(tmp_path, site_updates=SITE_UPDATES)
    monkeypatch.setattr(gf, "REPO_ROOT", tmp_path)
    xml = render(datetime(2026, 8, 13, tzinfo=timezone.utc))

    for guid in STABLE_GUIDS:
        assert guid in xml
    assert "15 May 2026" in xml
    assert "13 May 2026" in xml
    guids = re.findall(r"<guid[^>]*>([^<]+)</guid>", xml)
    assert len(guids) == len(set(guids))
    assert _year_key("n.d.") == 0
    assert _year_key("n.d.") < _year_key("2026")
    assert xml.index("work-Alpha2026") < xml.index("work-Undated")


def test_missing_site_updates_still_emits_works(tmp_path: Path, monkeypatch):
    _write_feed_inputs(tmp_path, site_updates=None)
    monkeypatch.setattr(gf, "REPO_ROOT", tmp_path)
    xml = render(datetime(2026, 8, 13, tzinfo=timezone.utc))
    assert "work-Alpha2026" in xml
    assert STABLE_GUIDS[0] not in xml
