"""Tests for SEO invariant enforcement."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from seo_invariants import (  # noqa: E402
    REDIRECT_STUBS,
    check_paper_pages,
    check_sitemap_policy,
    check_social_meta,
    check_work_descriptions,
    collect_seo_errors,
)


def test_collect_seo_errors_empty_on_repo():
    assert collect_seo_errors(REPO_ROOT) == []


def test_paper_pages_no_json_ld():
    errors = check_paper_pages(REPO_ROOT)
    assert not any("JSON-LD" in err for err in errors)


def test_sitemap_matches_policy():
    assert check_sitemap_policy(REPO_ROOT) == []


def test_redirect_stub_list_covers_known_stubs():
    rels = {rel for rel, _ in REDIRECT_STUBS}
    assert "about.html" in rels
    assert "nft.html" in rels


def test_indexable_pages_have_twitter_and_og_alt():
    assert check_social_meta(REPO_ROOT) == []


def test_work_descriptions_not_truncated_midword():
    assert check_work_descriptions(REPO_ROOT) == []
