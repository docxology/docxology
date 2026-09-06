"""Tests for centrally generated, fail-closed redirect stubs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import redirect_stubs  # noqa: E402
from generate_redirect_stubs import apply  # noqa: E402
from generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402
from redirect_stubs import (  # noqa: E402
    REDIRECT_STUBS,
    RedirectStub,
    collect_redirect_errors,
    discover_redirect_stubs,
    has_meta_refresh,
    render_stub,
)


def test_every_discovered_redirect_is_centrally_declared_and_current():
    assert discover_redirect_stubs(REPO_ROOT) == {stub.path for stub in REDIRECT_STUBS}
    assert collect_redirect_errors(REPO_ROOT) == []


def test_renderer_has_accessible_no_script_fallback():
    rendered = render_stub(
        RedirectStub("legacy.html", "Legacy", "https://example.test/next", "https://example.test/next", "Next page")
    )
    assert '<meta name="robots" content="noindex, follow">' in rendered
    assert '<meta http-equiv="refresh" content="0; url=https://example.test/next">' in rendered
    assert '<link rel="canonical" href="https://example.test/next">' in rendered
    assert '<a href="https://example.test/next">Next page</a>' in rendered
    assert "<script" not in rendered


def test_validation_flags_a_hand_written_redirect_not_in_source(tmp_path):
    (tmp_path / "about.html").write_text(render_stub(REDIRECT_STUBS[0]), encoding="utf-8")
    (tmp_path / "surprise.html").write_text(
        '<meta http-equiv="refresh" content="0; url=https://example.test/">', encoding="utf-8"
    )
    errors = collect_redirect_errors(tmp_path)
    assert "undeclared redirect stub: surprise.html" in errors


def test_meta_refresh_discovery_is_independent_of_quote_style_and_attribute_order(tmp_path):
    (tmp_path / "about.html").write_text(render_stub(REDIRECT_STUBS[0]), encoding="utf-8")
    surprise = tmp_path / "surprise.html"
    surprise.write_text(
        "<meta content='0; url=https://example.test/next' data-legacy='yes' http-equiv='REFRESH'>",
        encoding="utf-8",
    )

    assert has_meta_refresh(surprise.read_text(encoding="utf-8"))
    assert discover_redirect_stubs(tmp_path) == {"about.html", "surprise.html"}
    assert "undeclared redirect stub: surprise.html" in collect_redirect_errors(tmp_path)


def test_redirect_discovery_prunes_venv_and_cache_html_without_reading_them(tmp_path: Path):
    (tmp_path / "about.html").write_text(render_stub(REDIRECT_STUBS[0]), encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text('<meta http-equiv="refresh" content="0; url=https://example.test/">', encoding="utf-8")
    for directory in (".venv", ".pytest_cache", "__pycache__"):
        cache = tmp_path / directory
        cache.mkdir()
        (cache / "vendor.html").symlink_to(outside)

    assert discover_redirect_stubs(tmp_path) == {"about.html"}


def test_redirect_check_and_apply_reject_a_symlinked_declared_stub(tmp_path: Path):
    outside = tmp_path / "outside.html"
    outside.write_text("outside must survive\n", encoding="utf-8")
    (tmp_path / "about.html").symlink_to(outside)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        collect_redirect_errors(tmp_path)
    with pytest.raises(UnsafeGeneratedOutputPathError):
        apply(repo_root=tmp_path)

    assert outside.read_text(encoding="utf-8") == "outside must survive\n"


def test_discovery_cache_is_keyed_by_file_identity_not_path(tmp_path):
    """A rewritten or replaced document must be re-read, never served from cache."""
    redirect_stubs.clear_discovery_cache()
    page = tmp_path / "page.html"
    page.write_text("<html><head></head><body>plain</body></html>", encoding="utf-8")
    assert redirect_stubs.discover_redirect_stubs(tmp_path) == set()

    # Rewritten in place: the same path is now a redirect and must be found.
    page.write_text(render_stub(REDIRECT_STUBS[0]), encoding="utf-8")
    assert redirect_stubs.discover_redirect_stubs(tmp_path) == {"page.html"}

    # Replaced through a new inode (how the generators write): still found.
    replacement = tmp_path / "page.html.new"
    replacement.write_text("<html><head></head><body>plain again</body></html>", encoding="utf-8")
    replacement.replace(page)
    assert redirect_stubs.discover_redirect_stubs(tmp_path) == set()


def test_a_cached_path_that_becomes_a_symlink_still_fails_closed(tmp_path):
    """The cache must not soften the reader's refusal to follow a link.

    The key comes from ``lstat``, so the symlink presents its own inode rather
    than the target's: the lookup misses and the hardened reader runs again.
    """
    redirect_stubs.clear_discovery_cache()
    real = tmp_path / "real.html"
    real.write_text("<html><head></head><body>plain</body></html>", encoding="utf-8")
    assert redirect_stubs.discover_redirect_stubs(tmp_path) == set()

    outside = tmp_path.parent / "outside.html"
    outside.write_text(render_stub(REDIRECT_STUBS[0]), encoding="utf-8")
    real.unlink()
    real.symlink_to(outside)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        redirect_stubs.discover_redirect_stubs(tmp_path)
