"""Tests for publications.html sync orchestrator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from sync_publications_html import (  # noqa: E402
    PUBLICATIONS_HTML,
    PUBLICATIONS_LD_JSON,
    build_collection_page,
    canonical_link_url,
    load_rows,
    schema_type_for_row,
    validate_rows,
)


def test_dry_run_cli():
    rows = load_rows()
    result = subprocess.run(
        ["python3", "code/orchestrators/sync_publications_html.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert f"OK dry-run: {len(rows)} rows" in result.stdout
    assert f"publications-ld.json would have {len(rows)} mainEntity items" in result.stdout


def test_collection_page_entity_count():
    rows = load_rows()
    validate_rows(rows)
    collection = build_collection_page(rows)
    assert collection["@type"] == "CollectionPage"
    assert len(collection["mainEntity"]) == len(rows)
    assert f"{len(rows)} works" in collection["description"]


def test_generated_publications_surfaces():
    rows = load_rows()
    html = PUBLICATIONS_HTML.read_text(encoding="utf-8")
    assert f"{len(rows)} Research Works" in html
    assert 'src="/data/publications-ld.json"' in html
    og_match = re.search(r'<meta property="og:title" content="([^"]*)">', html)
    twitter_match = re.search(r'<meta name="twitter:title" content="([^"]*)">', html)
    assert og_match and twitter_match
    assert og_match.group(1) == twitter_match.group(1)

    ld = json.loads(PUBLICATIONS_LD_JSON.read_text(encoding="utf-8"))
    assert ld["@type"] == "CollectionPage"
    assert len(ld["mainEntity"]) == len(rows)
    headlines = {item["headline"] for item in ld["mainEntity"]}
    assert "Sortition Upstream of NTQR" in headlines


def test_canonical_link_url_handles_markdown_doi_and_isbn():
    assert canonical_link_url("[10.5281/zenodo.1](https://doi.org/10.5281/zenodo.1)", "Zenodo") == (
        "https://doi.org/10.5281/zenodo.1"
    )
    assert canonical_link_url("10.5281/zenodo.2", "Zenodo") == "https://doi.org/10.5281/zenodo.2"
    assert canonical_link_url("978-0-12-345678-9", "Publisher") == "https://www.worldcat.org/isbn/978-0-12-345678-9"
    assert canonical_link_url("978-0-12-345678-9", "COGSEC.org") == "https://cogsec.org"
    assert canonical_link_url("—", "Zenodo") == ""


def test_schema_type_for_row_maps_known_types():
    assert schema_type_for_row("Paper") == "ScholarlyArticle"
    assert schema_type_for_row("Book") == "Book"
    assert schema_type_for_row("Presentation") == "PresentationDigitalDocument"
    assert schema_type_for_row("Course") == "Course"
    assert schema_type_for_row("Series") == "CreativeWorkSeries"
    assert schema_type_for_row("Unknown Type") == "ScholarlyArticle"
