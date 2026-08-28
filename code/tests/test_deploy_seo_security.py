"""Tests for no-write SEO/security normalization checks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from deploy_seo_security import (  # noqa: E402
    is_indexable_html_path,
    process_file,
    transform_html,
)
from generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402


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
