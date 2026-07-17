"""Tests for the bounded GitHub Pages publication projection."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_pages_artifact as bpa  # noqa: E402


def test_paper_extracted_binary_images_are_omitted_from_pages():
    assert not bpa.is_published_path(Path("papers/2026_Example/images/page1_img1.png"))
    assert not bpa.is_published_path(Path("papers/2026_Example/images/page1_img1.jpeg"))


def test_artwork_and_public_site_images_are_retained():
    assert bpa.is_published_path(Path("art/42_drawing.jpg"))
    assert bpa.is_published_path(Path("og-image.jpg"))
    assert bpa.is_published_path(Path("papers/2026_Example/figure.jpg"))


def test_source_and_local_only_tooling_are_separated():
    assert bpa.is_published_path(Path("code/orchestrators/build_pages_artifact.py"))
    assert not bpa.is_published_path(Path(".github/workflows/pages.yml"))
    assert bpa.is_published_path(Path("data/agent-index.json"))
    assert bpa.is_published_path(Path("resume/resume.pdf"))
