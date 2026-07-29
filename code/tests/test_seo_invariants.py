"""Tests for SEO invariant enforcement."""

from __future__ import annotations

import re
import subprocess
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
    check_public_html_security,
    collect_seo_errors,
)
from site_nav import CSP_META_TAG, META_INVALID_CSP_DIRECTIVES  # noqa: E402


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


def test_public_html_security_metadata():
    assert check_public_html_security(REPO_ROOT) == []


def test_meta_csp_carries_no_header_only_directives():
    """A <meta> CSP must not declare directives the spec makes it ignore.

    `frame-ancestors`, `report-uri` and `sandbox` only take effect in an HTTP
    response header. Shipped in a meta policy they protect nothing and make
    Chromium log a console error on every page, which is what previously forced
    browser_qa.py to filter console errors.
    """
    for directive in META_INVALID_CSP_DIRECTIVES:
        assert directive not in CSP_META_TAG


def test_no_tracked_html_ships_a_header_only_csp_directive():
    """Every tracked page, not just the ones deploy_seo_security.py rewrites.

    docs/design/components/*.html are hand-authored and outside that script's
    scope, yet they are published in the Pages artifact — they kept the ignored
    directive for months after the generated pages would have dropped it.
    """
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    offenders = []
    for relative in tracked:
        path = REPO_ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for policy in re.findall(
            r'http-equiv="Content-Security-Policy"\s+content="([^"]*)"', text
        ):
            for directive in META_INVALID_CSP_DIRECTIVES:
                if directive in policy:
                    offenders.append(f"{relative}: {directive}")
    assert offenders == []
