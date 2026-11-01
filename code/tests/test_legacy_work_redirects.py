"""Preserve work URLs reproduced as 404s in Search Console follow-up."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.redirect_stubs import (  # noqa: E402
    RedirectStub,
    collect_redirect_errors,
    declared_stubs,
    render_stub,
)
from docxology_tools.seo_invariants import check_work_pages  # noqa: E402
from build_sitemap import render, sitemap_locs  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_WORKS = {
    "Friedman2026CogSecSkillsMultiharnessCognitiveSecurity174": 174,
    "Friedman2025CEREBRUMCaseEnabledReasoning118": 10,
    "Friedman2026LiteratureReviewArchitectureActive110": 110,
}


def catalog_keys() -> dict[int, str]:
    works = json.loads((REPO_ROOT / "data/works.json").read_text())["works"]
    return {work["num"]: work["citation_key"] for work in works}


@pytest.mark.parametrize("legacy,num", LEGACY_WORKS.items())
def test_old_work_url_reaches_its_catalogued_identity(legacy: str, num: int):
    key = catalog_keys()[num]
    target = f"https://danielarifriedman.com/works/{key}.html"
    stub = declared_stubs()[f"works/{legacy}.html"]
    assert stub.target_url == stub.canonical_url == target
    assert (REPO_ROOT / "works" / f"{key}.html").is_file()
    if legacy.endswith("118"):
        registry = json.loads((REPO_ROOT / "data/work-identifiers.json").read_text())
        assert registry["identifiers"]["118"]["status"] == "retired"


def test_known_work_redirects_are_excluded_from_both_sitemap_interfaces(tmp_path):
    works = tmp_path / "works"
    works.mkdir()
    keys = catalog_keys()
    old_urls, canonical_urls = set(), set()
    for legacy, num in LEGACY_WORKS.items():
        key = keys[num]
        old_url = f"https://danielarifriedman.com/works/{legacy}.html"
        target = f"https://danielarifriedman.com/works/{key}.html"
        stub = RedirectStub(
            f"works/{legacy}.html", "Legacy work", target, target, "Work"
        )
        (works / f"{legacy}.html").write_text(render_stub(stub))
        (works / f"{key}.html").write_text(
            '<html><head><meta name="robots" content="index, follow">'
            f'<link rel="canonical" href="{target}"></head><body></body></html>'
        )
        old_urls.add(old_url)
        canonical_urls.add(target)
    assert check_work_pages(tmp_path) == []
    listed = set(sitemap_locs(repo_root=tmp_path))
    xml = render("2026-11-01", repo_root=tmp_path)
    assert canonical_urls <= listed
    assert not old_urls & listed
    assert all(f"<loc>{url}</loc>" in xml for url in canonical_urls)
    assert all(f"<loc>{url}</loc>" not in xml for url in old_urls)


def test_unregistered_noindex_work_still_fails(tmp_path):
    works = tmp_path / "works"
    works.mkdir()
    (works / "unregistered.html").write_text(
        '<html><head><meta name="robots" content="noindex, follow">'
        '<link rel="canonical" href="https://danielarifriedman.com/works/unregistered.html">'
        "</head><body></body></html>"
    )
    assert any(
        "unregistered.html: expected robots index, follow" in error
        for error in check_work_pages(tmp_path)
    )


def test_wrong_destination_on_a_known_work_redirect_fails(tmp_path):
    (tmp_path / "works").mkdir()
    legacy = next(iter(LEGACY_WORKS))
    relative = f"works/{legacy}.html"
    stub = RedirectStub(
        relative,
        "Legacy work",
        "https://example.test/wrong",
        "https://example.test/wrong",
        "Wrong",
    )
    (tmp_path / relative).write_text(render_stub(stub))
    assert f"stale redirect stub: {relative}" in collect_redirect_errors(tmp_path)
