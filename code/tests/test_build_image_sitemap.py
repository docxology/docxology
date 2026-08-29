"""Tests for the art gallery image sitemap decision (NEW-2, 2026-08-28).

The generated image sitemap was 942/942 cross-domain (live.staticflickr.com)
entries. Google does not index image-sitemap URLs on a domain the site does
not own, so the file was inert for its purpose. Decision: do not ship an
image sitemap until art thumbnails are self-hosted on an origin we control.
These tests pin that decision and the conditions for reversing it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_image_sitemap_is_not_shipped() -> None:
    assert not (REPO_ROOT / "sitemap-images.xml").exists(), (
        "sitemap-images.xml reintroduced: only valid if every <image:loc> "
        "points at an origin this site owns"
    )


def test_robots_does_not_reference_image_sitemap() -> None:
    robots = (REPO_ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "sitemap-images.xml" not in robots


def test_art_gallery_images_are_still_third_party_hosted() -> None:
    """Documents the precondition: while thumbnails live on Flickr, an image
    sitemap has no same-origin URLs to list. If this test starts failing
    because local copies exist under art/, revisit the decision."""
    import json

    payload = json.loads((REPO_ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))
    local_images = [
        p for p in (REPO_ROOT / "art").iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".webp"}
        or (p.suffix.lower() == ".png" and not p.name.startswith("favicon"))
    ]
    assert not local_images, (
        "art/ now contains real image files; consider self-hosted thumbnails "
        "and restoring a same-origin image sitemap"
    )
