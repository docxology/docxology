"""Tests for the art gallery image sitemap."""

from __future__ import annotations

import sys
import xml.dom.minidom as minidom
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_image_sitemap as bis  # noqa: E402


def test_image_sitemap_is_current():
    """Checked-in sitemap-images.xml matches the generator (not stale)."""
    artworks = bis.load_artworks()
    expected = bis.render(artworks, bis.local_files_by_id())
    assert bis.OUT.read_text(encoding="utf-8") == expected


def test_image_sitemap_well_formed_and_namespaced():
    text = bis.OUT.read_text(encoding="utf-8")
    minidom.parseString(text)  # raises on malformed XML
    assert 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"' in text
    assert text.count("<image:image>") > 100  # the gallery has hundreds of works


def test_image_sitemap_uses_deployed_image_sources():
    text = bis.OUT.read_text(encoding="utf-8")
    total = text.count("<image:loc>")
    flickr = text.count("<image:loc>https://live.staticflickr.com/")
    local_art = text.count("<image:loc>https://danielarifriedman.com/art/")
    local_papers = text.count("<image:loc>https://danielarifriedman.com/papers/")
    assert flickr + local_art + local_papers == total
    assert local_art == 0  # gallery images use Flickr URLs
    assert local_papers == 0  # paper figures remain repository-only; Pages links to GitHub


def test_robots_references_image_sitemap():
    robots = (REPO_ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Sitemap: https://danielarifriedman.com/sitemap-images.xml" in robots
