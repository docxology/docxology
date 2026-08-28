"""Tests for software.html sync orchestrator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from count_consistency import parse_software_catalog_counts  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from sync_software_html import (  # noqa: E402
    SOFTWARE_HTML,
    SOFTWARE_LD_JSON,
    SOFTWARE_TEMPLATE,
    build_collection_page,
    load_source_template,
    load_rows,
    render_outputs,
    render_outputs_from_template,
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


def test_check_cli_reports_exact_source_rendered_status_without_writing():
    before = {
        SOFTWARE_HTML: SOFTWARE_HTML.read_bytes(),
        SOFTWARE_LD_JSON: SOFTWARE_LD_JSON.read_bytes(),
    }
    expected_stale = stale_output_paths(render_outputs(), repo_root=REPO_ROOT)
    result = subprocess.run(
        ["python3", "code/orchestrators/sync_software_html.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert {path: path.read_bytes() for path in before} == before
    if expected_stale:
        assert result.returncode != 0
        assert "Stale source-rendered software outputs" in result.stderr
        for path in expected_stale:
            assert str(path.relative_to(REPO_ROOT)) in result.stderr
    else:
        assert result.returncode == 0, result.stderr
        assert "Checked 2 software outputs" in result.stdout


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
    assert f"{expected_docx} original repositories" in html
    assert f"{expected_aii} catalogued" in html
    assert 'src="/data/software-ld.json"' not in html
    assert '<script type="application/ld+json">' in html
    og_match = re.search(r'<meta property="og:description" content="([^"]*)">', html)
    twitter_match = re.search(r'<meta name="twitter:description" content="([^"]*)">', html)
    assert og_match and twitter_match
    assert og_match.group(1) == twitter_match.group(1)
    description = og_match.group(1)
    assert len(description) <= 160
    assert "public repositories" in description
    ld = json.loads(SOFTWARE_LD_JSON.read_text(encoding="utf-8"))
    assert ld["@type"] == "CollectionPage"
    assert len(ld["mainEntity"]) == expected_docx + expected_aii


def _temporary_software_outputs(tmp_path: Path, rendered: dict[Path, str]) -> dict[Path, str]:
    """Map canonical source-rendered text to isolated real output files."""
    return {
        tmp_path / "software.html": rendered[SOFTWARE_HTML],
        tmp_path / "data" / "software-ld.json": rendered[SOFTWARE_LD_JSON],
    }


def test_render_and_check_detect_stale_repo_card_and_json_ld(tmp_path: Path):
    """A no-write check must see stale cards as well as stale JSON-LD."""
    rendered = render_outputs()
    canonical_html = rendered[SOFTWARE_HTML]
    targets = _temporary_software_outputs(tmp_path, rendered)
    write_output_texts(targets, repo_root=tmp_path)

    stale_card = canonical_html.replace(
        '<div class="repo-card">', '<div class="repo-card stale-card">', 1
    )
    assert stale_card != canonical_html
    assert render_outputs_from_template(None, stale_card)[SOFTWARE_HTML] == canonical_html

    stale_json_ld = rendered[SOFTWARE_LD_JSON].replace(
        '"CollectionPage"', '"StaleCollectionPage"', 1
    )
    cases = {
        "stale generated repo card": {
            tmp_path / "software.html": stale_card,
        },
        "stale JSON-LD": {
            tmp_path / "data" / "software-ld.json": stale_json_ld,
        },
    }
    for label, changed in cases.items():
        original = {path: path.read_text(encoding="utf-8") for path in changed}
        try:
            for path, stale in changed.items():
                path.write_text(stale, encoding="utf-8")
            assert stale_output_paths(targets, repo_root=tmp_path) == tuple(changed), label
        finally:
            for path, content in original.items():
                path.write_text(content, encoding="utf-8")


def test_source_owned_template_detects_hand_authored_body_framing_drift(tmp_path: Path):
    """The source template, rather than software.html, defines the page frame."""
    template = load_source_template()
    assert SOFTWARE_TEMPLATE.is_file()
    for token in (
        "{{SOFTWARE_INLINE_LD}}",
        "{{SOFTWARE_DOCX_GRID}}",
        "{{SOFTWARE_AII_GRID}}",
        "{{SOFTWARE_DOCX_FOOTER}}",
    ):
        assert token in template

    rendered = render_outputs()
    canonical_html = rendered[SOFTWARE_HTML]
    assert "{{SOFTWARE_DOCX_GRID}}" not in canonical_html
    targets = _temporary_software_outputs(tmp_path, rendered)
    write_output_texts(targets, repo_root=tmp_path)
    html_target = tmp_path / "software.html"

    stale_frame = canonical_html.replace(
        '<main id="main" class="main">',
        '<main id="main" class="main" data-unowned-frame-drift="true">',
        1,
    )
    assert stale_frame != canonical_html
    html_target.write_text(stale_frame, encoding="utf-8")

    assert stale_output_paths(targets, repo_root=tmp_path) == (html_target,)
    assert render_outputs()[SOFTWARE_HTML] == canonical_html


def test_apply_mapping_normalizes_software_targets(tmp_path: Path):
    """The exact mapping used by ``--apply`` restores every checked target."""
    targets = _temporary_software_outputs(tmp_path, render_outputs())
    write_output_texts(targets, repo_root=tmp_path)
    html_target, json_target = tuple(targets)
    html_target.write_text(targets[html_target] + "\n<!-- stale -->\n", encoding="utf-8")
    json_target.write_text("{}\n", encoding="utf-8")

    assert stale_output_paths(targets, repo_root=tmp_path) == (html_target, json_target)
    write_output_texts(targets, repo_root=tmp_path)
    assert stale_output_paths(targets, repo_root=tmp_path) == ()


def test_render_refuses_a_missing_generated_repo_grid_marker():
    from sync_software_html import DOCX_GRID_BEGIN  # noqa: PLC0415

    canonical_html = render_outputs()[SOFTWARE_HTML]
    missing_marker = canonical_html.replace(DOCX_GRID_BEGIN, "", 1)
    with pytest.raises(ValueError, match=r"SOFTWARE_DOCX_GRID_BEGIN"):
        render_outputs_from_template(None, missing_marker)
