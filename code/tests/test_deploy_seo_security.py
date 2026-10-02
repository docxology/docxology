"""Tests for no-write SEO/security normalization checks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools.generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402
from docxology_tools.site_nav import NAV_TOGGLE_SCRIPT_TAG  # noqa: E402
from deploy_seo_security import (  # noqa: E402
    add_early_navigation_if_needed,
    is_indexable_html_path,
    process_file,
    transform_html,
)


NAV = '<nav><button class="menu-btn">Menu</button><ul class="nav-links"><li><a href="/">Home</a></li></ul></nav>'


def test_early_navigation_is_in_head_before_body_and_idempotent():
    source = f"<html><head></head><body>{NAV}</body></html>"
    normalized = add_early_navigation_if_needed(source)
    assert normalized.count(NAV_TOGGLE_SCRIPT_TAG) == 1
    assert normalized.index(NAV_TOGGLE_SCRIPT_TAG) < normalized.index("</head>")
    assert add_early_navigation_if_needed(normalized) == normalized
    complete, _, skipped = transform_html(source)
    assert not skipped
    assert transform_html(complete) == (complete, [], False)


def test_early_navigation_normalizes_deferred_body_and_duplicate_owners():
    deferred = '<script src="../js/nav-toggle.js?v=old" defer></script>'
    source = f"<html><head>{deferred}</head><body>{NAV}{NAV_TOGGLE_SCRIPT_TAG}</body></html>"
    normalized = add_early_navigation_if_needed(source)
    assert normalized.count("nav-toggle.js") == 1
    assert NAV_TOGGLE_SCRIPT_TAG in normalized.split("</head>")[0]
    assert add_early_navigation_if_needed(normalized) == normalized


@pytest.mark.parametrize("navigation", [
    '<nav class="breadcrumb"><a href="/">Home</a></nav>',
    '<nav><div class="nav-links"><a href="/">Home</a></div></nav>',
    '<nav class><button class>Menu</button><ul class></ul></nav>',
    '<nav><button class="menu-btn">Menu</button></nav><nav><ul class="nav-links"></ul></nav>',
    '<!-- ' + NAV + ' -->',
    '<script type="text/plain">' + NAV + '</script>',
])
def test_pages_without_real_toggle_controls_do_not_load_navigation_asset(navigation):
    source = f"<html><head>{NAV_TOGGLE_SCRIPT_TAG}</head><body>{navigation}</body></html>"
    normalized = add_early_navigation_if_needed(source)
    assert "nav-toggle.js" not in normalized
    assert add_early_navigation_if_needed(normalized) == normalized


def test_navigation_normalization_check_preserves_actual_file_bytes(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    page = repo / "index.html"
    source = f"<html><head></head><body>{NAV}</body></html>"
    page.write_text(source, encoding="utf-8")
    result = process_file(page, redirect_paths=set(), write=False, repo_root=repo)
    assert "early-navigation" in result["changes"]
    assert page.read_text(encoding="utf-8") == source


def test_dependency_html_is_not_a_site_normalization_target():
    assert not is_indexable_html_path(Path(".venv/lib/python3.12/site-packages/playwright/report.html"))
    assert not is_indexable_html_path(Path("code/templates/example.html"))
    assert is_indexable_html_path(Path("works/example.html"))


def test_transform_html_reports_missing_security_tags_without_writing():
    original = "<html><head></head><body></body></html>"
    updated, changes, skipped = transform_html(original)
    assert not skipped
    assert "csp" in changes
    assert "referrer-policy" in changes
    assert "rel-me" in changes
    assert original != updated


def test_transform_html_leaves_redirect_stub_untouched():
    original = '<meta name="robots" content="noindex, follow">'
    updated, changes, skipped = transform_html(original, is_redirect=True)
    assert skipped
    assert changes == []
    assert updated == original


def test_process_file_check_is_no_write_for_a_stale_page(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    page = repo_root / "index.html"
    original = "<html><head></head><body></body></html>"
    page.write_text(original, encoding="utf-8")

    result = process_file(
        page,
        redirect_paths=set(),
        write=False,
        repo_root=repo_root,
    )

    assert result["changes"]
    assert page.read_text(encoding="utf-8") == original


def test_process_file_write_uses_safe_generated_output_boundary(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    page = repo_root / "index.html"
    page.write_text("<html><head></head><body></body></html>", encoding="utf-8")

    result = process_file(
        page,
        redirect_paths=set(),
        write=True,
        repo_root=repo_root,
    )

    assert result["changes"]
    assert "Content-Security-Policy" in page.read_text(encoding="utf-8")


@pytest.mark.parametrize("write", [False, True], ids=["check", "write"])
@pytest.mark.parametrize("unsafe_kind", ["final-symlink", "ancestor-symlink", "hard-link"])
def test_process_file_rejects_unsafe_output_paths_without_touching_external_content(
    tmp_path: Path,
    write: bool,
    unsafe_kind: str,
):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    sentinel = "outside content must remain unchanged\n"
    external = tmp_path / "external.html"
    external.write_text(sentinel, encoding="utf-8")

    if unsafe_kind == "final-symlink":
        page = repo_root / "index.html"
        page.symlink_to(external)
    elif unsafe_kind == "ancestor-symlink":
        external_directory = tmp_path / "external-directory"
        external_directory.mkdir()
        external = external_directory / "index.html"
        external.write_text(sentinel, encoding="utf-8")
        (repo_root / "nested").symlink_to(external_directory, target_is_directory=True)
        page = repo_root / "nested" / "index.html"
    else:
        page = repo_root / "index.html"
        os.link(external, page)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        process_file(
            page,
            redirect_paths=set(),
            write=write,
            repo_root=repo_root,
        )

    assert external.read_text(encoding="utf-8") == sentinel
