#!/usr/bin/env python3
"""Invariant tests for art.html thumbnail dimensions (NEW-1 regression guard).

Handoff 2026-08-28 NEW-1: SSR art thumbnails must not declare width/height
attributes that contradict the actual image. Real per-image dimensions are not
available in the artwork manifest (Flickr sizes carry no intrinsic dims), and
the grid tile already pins shape via CSS (aspect-ratio + object-fit), so the
correct contract is: NO width/height attributes on .art-thumb images, and the
CSS must keep the 1/1 aspect ratio. If real dimensions ever land in
data/artworks.json, this test must be updated to assert they match instead.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ART_HTML = REPO_ROOT / "art.html"
STYLE_CSS = REPO_ROOT / "style.css"
ARTWORKS = REPO_ROOT / "data" / "artworks.json"


def test_art_thumbs_declare_no_contradicting_dimensions() -> None:
    """Every .art-thumb img must omit width/height (or, if present, they must
    come from real manifest data - which today does not exist)."""
    html = ART_HTML.read_text(encoding="utf-8")
    for match in re.finditer(r"<img[^>]*art-thumb[^>]*>", html):
        tag = match.group(0)
        assert 'width="' not in tag or "data-real-dims" in tag, (
            f"art-thumb declares width without real manifest dims: {tag[:120]}"
        )
        assert 'height="' not in tag or "data-real-dims" in tag, (
            f"art-thumb declares height without real manifest dims: {tag[:120]}"
        )


def test_art_grid_css_keeps_tile_shape_without_html_dims() -> None:
    """With no HTML dimension attrs, the CSS aspect-ratio + object-fit must be
    present so tiles don't collapse before image load."""
    css = STYLE_CSS.read_text(encoding="utf-8")
    art_rule = re.search(r"\.art-thumb\{[^}]*\}", css)
    assert art_rule, ".art-thumb rule missing from style.css"
    assert "aspect-ratio" in art_rule.group(0), ".art-thumb must pin aspect-ratio"
    assert "object-fit" in art_rule.group(0), ".art-thumb must use object-fit"


def test_artwork_manifest_has_no_dimension_fields_to_emit() -> None:
    """Documents the data contract: if dimensions are added to the manifest,
    the generator should emit real ones and the no-dims assertion above flips.
    This test exists to force a conscious update in that case."""
    payload = json.loads(ARTWORKS.read_text(encoding="utf-8"))
    artworks = payload.get("artworks", [])
    assert artworks, "artworks.json unexpectedly empty"
    dimension_keys = {"width", "height", "dimensions", "intrinsic_size"}
    for artwork in artworks[:50]:
        present = dimension_keys & set(artwork)
        assert not present, (
            f"artworks.json now carries {present}; update art.html generator "
            "to emit real per-image dimensions and flip the no-dims invariant"
        )
