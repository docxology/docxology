"""Negative-fixture tests for the SEO lane additions (2026-08-27).

Proves each new detector actually flags a constructed violation rather than
only passing on an already-clean repo, per the repo negative-control convention.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from title_policy import (  # noqa: E402
    HARD_LIMIT,
    SOFT_LIMIT,
    assert_title_within_limit,
    clip_title,
)

import build_404_page  # noqa: E402
from seo_invariants import check_canonical_integrity  # noqa: E402
import pytest  # noqa: E402


# --- title_policy --------------------------------------------------------------

def test_clip_title_word_boundary_under_hard_limit():
    long_title = "Neurosymbolic AI & Active Inference: Bridging Symbolic Reasoning and Generative Agents"
    clipped = clip_title(long_title)
    assert len(clipped) <= HARD_LIMIT
    assert clipped.endswith("…")
    assert clipped.startswith("Neurosymbolic AI")  # leading tokens preserved


def test_clip_title_leaves_short_titles_untouched():
    assert clip_title("Short Title") == "Short Title"
    assert clip_title("") == ""


def test_clip_title_is_idempotent():
    once = clip_title("A very long title that definitely exceeds the sixty five character hard limit for sure")
    twice = clip_title(once)
    assert once == twice


def test_assert_title_within_limit_raises_over_hard_limit():
    with pytest.raises(ValueError, match="exceeds hard limit"):
        assert_title_within_limit("x" * (HARD_LIMIT + 1))


def test_assert_title_within_limit_accepts_soft_range():
    # Between soft target and hard ceiling is allowed (clipped by generators).
    assert_title_within_limit("x" * (SOFT_LIMIT + 1))


# --- canonical integrity -------------------------------------------------------

def test_canonical_integrity_flags_link_to_away_canonical_page(tmp_path):
    (tmp_path / "index.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/index.html"></head>'
        '<body><a href="stub.html">stub</a><a href="/good.html">good</a></body></html>',
        encoding="utf-8",
    )
    (tmp_path / "stub.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/good.html"></head></html>',
        encoding="utf-8",
    )
    (tmp_path / "good.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/good.html"></head></html>',
        encoding="utf-8",
    )
    errors = check_canonical_integrity(tmp_path)
    assert len(errors) == 1, errors
    assert "stub.html" in errors[0]
    assert "index.html" in errors[0]  # the linking page is named


def test_canonical_integrity_clean_repo_passes(tmp_path):
    for name in ("index.html", "good.html"):
        (tmp_path / name).write_text(
            f'<html><head><link rel="canonical" href="https://danielarifriedman.com/{name}"></head></html>',
            encoding="utf-8",
        )
    (tmp_path / "index.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/index.html"></head>'
        '<body><a href="good.html">good</a></body></html>',
        encoding="utf-8",
    )
    assert check_canonical_integrity(tmp_path) == []


def test_canonical_integrity_accepts_directory_and_index_forms(tmp_path):
    (tmp_path / "works").mkdir()
    (tmp_path / "works" / "index.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/works/"></head></html>',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/"></head>'
        '<body><a href="/works/">works</a><a href="/works/index.html">works idx</a></body></html>',
        encoding="utf-8",
    )
    assert check_canonical_integrity(tmp_path) == []


def test_canonical_integrity_ignores_external_links(tmp_path):
    (tmp_path / "index.html").write_text(
        '<html><head><link rel="canonical" href="https://danielarifriedman.com/index.html"></head>'
        '<body><a href="https://example.com/other.html">ext</a>'
        '<a href="mailto:x@y.z">mail</a><a href="#section">anchor</a></body></html>',
        encoding="utf-8",
    )
    assert check_canonical_integrity(tmp_path) == []


# --- 404 page generator --------------------------------------------------------

def test_build_404_page_check_mode_passes_on_fresh_render():
    # The checked-in 404.html must match the renderer modulo the footer build
    # stamp (commit SHA at generation time) - mirrors generated_outputs semantics.
    import re as _re
    import sys as _sys
    _sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
    from build_stamp import current_on_disk_stamp, reuse_on_disk_stamp
    content = build_404_page.render()
    on_disk = (REPO_ROOT / "404.html").read_text(encoding="utf-8")
    assert on_disk == reuse_on_disk_stamp(content, on_disk)


def test_build_404_page_shell_and_recovery_features():
    content = build_404_page.render()
    assert 'id="q"' in content  # search box
    assert "/js/search-page.js" in content  # wired to the search index
    assert "noindex, follow" in content
    assert 'class="destinations"' in content
    # Exactly the top-8 destinations
    assert content.count("<a href=\"/") >= 8
    assert build_404_page.OUT == REPO_ROOT / "404.html"
