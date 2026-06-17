"""Tests for software.html sync orchestrator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from count_consistency import parse_software_catalog_counts  # noqa: E402
from sync_software_html import (  # noqa: E402
    SOFTWARE_HTML,
    SOFTWARE_LD_JSON,
    build_collection_page,
    load_rows,
    validate_rows,
)


def test_dry_run_cli():
    expected_docx, expected_aii = parse_software_catalog_counts()
    result = subprocess.run(
        ["python3", "code/orchestrators/sync_software_html.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert (
        f"OK dry-run: {expected_docx} docxology + {expected_aii} AII rows"
        in result.stdout
    )


def test_collection_page_entity_count():
    expected_docx, expected_aii = parse_software_catalog_counts()
    rows = load_rows()
    validate_rows(rows)
    collection = build_collection_page(rows)
    assert len(collection["mainEntity"]) == expected_docx + expected_aii
    assert f"{expected_docx} original repositories" in collection["description"]


def test_generated_software_surfaces():
    expected_docx, expected_aii = parse_software_catalog_counts()
    html = SOFTWARE_HTML.read_text(encoding="utf-8")
    assert "biology_textbook" in html
    assert f"{expected_docx} original repositories" in html
    assert f"{expected_aii} catalogued" in html
    assert 'src="/data/software-ld.json"' in html
    og_match = re.search(r'<meta property="og:description" content="([^"]*)">', html)
    twitter_match = re.search(r'<meta name="twitter:description" content="([^"]*)">', html)
    assert og_match and twitter_match
    assert og_match.group(1) == twitter_match.group(1)
    assert f"{expected_docx} owned" in og_match.group(1)
    assert f"{expected_aii} AII" in og_match.group(1)
    ld = json.loads(SOFTWARE_LD_JSON.read_text(encoding="utf-8"))
    assert ld["@type"] == "CollectionPage"
    assert len(ld["mainEntity"]) == expected_docx + expected_aii
    names = {item["name"] for item in ld["mainEntity"]}
    assert "biology_textbook" in names
    assert "itrace" in names
    assert "template_autoscientists" in names
