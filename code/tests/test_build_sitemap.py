"""Tests for sitemap index-priority policy."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(ORCH_DIR))

from build_sitemap import render, sitemap_locs  # noqa: E402
from sitemap_policy import INDEX_PRIORITY_STATIC, indexnow_urls_from_locs  # noqa: E402


def test_sitemap_excludes_ops_and_paper_paths():
    xml = render()
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    assert "https://danielarifriedman.com/cite-verify.html" in locs
    assert "https://danielarifriedman.com/catalog.html" in locs
    assert "https://danielarifriedman.com/exports.html" in locs
    assert not any("/reports/" in loc for loc in locs)
    assert not any("/papers/" in loc for loc in locs)
    assert "https://danielarifriedman.com/data/works.json" not in locs
    assert "https://danielarifriedman.com/AGENT_START.md" not in locs


def test_sitemap_includes_work_pages():
    locs = re.findall(r"<loc>([^<]+)</loc>", render())
    assert any(loc.endswith("works/Friedman2026PolicyEntanglementActiveInference119.html") for loc in locs)


def test_indexnow_subset_of_sitemap():
    locs = sitemap_locs()
    indexnow = indexnow_urls_from_locs(locs)
    assert indexnow
    assert "https://danielarifriedman.com/" in indexnow
    assert all(url in locs for url in indexnow)
    assert "https://danielarifriedman.com/bibliography.bib" in indexnow
    assert all("/reports/" not in url for url in indexnow)


def test_static_policy_lists_exports_hub():
    paths = {row[0] for row in INDEX_PRIORITY_STATIC}
    assert "exports.html" in paths
    assert "cite-verify.html" in paths
