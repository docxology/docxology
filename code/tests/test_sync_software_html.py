"""Tests for software.html sync orchestrator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(PAPERS_DIR))

from sync_software_html import (  # noqa: E402
    SOFTWARE_HTML,
    SOFTWARE_LD_JSON,
    build_collection_page,
    load_rows,
    validate_rows,
)


def test_dry_run_cli():
    result = subprocess.run(
        ["python3", "papers/sync_software_html.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "OK dry-run: 56 docxology + 32 AII rows" in result.stdout


def test_collection_page_entity_count():
    rows = load_rows()
    validate_rows(rows)
    collection = build_collection_page(rows)
    assert len(collection["mainEntity"]) == 88
    assert "56 original repositories" in collection["description"]


def test_generated_software_surfaces():
    html = SOFTWARE_HTML.read_text(encoding="utf-8")
    assert "biology_textbook" in html
    assert "49 original" not in html.lower()
    assert 'src="/data/software-ld.json"' in html
    ld = json.loads(SOFTWARE_LD_JSON.read_text(encoding="utf-8"))
    assert ld["@type"] == "CollectionPage"
    assert len(ld["mainEntity"]) == 88
    names = {item["name"] for item in ld["mainEntity"]}
    assert "biology_textbook" in names
    assert "template_autoscientists" in names
