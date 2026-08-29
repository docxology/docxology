"""NEW-5 hydrate regression: SSR art tiles must be reused, never downgraded to _m."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ART_HTML = REPO_ROOT / "art.html"
ART_GALLERY_JS = REPO_ROOT / "js" / "art-gallery.js"


def test_gallery_js_has_no_m_template_literal():
    js = ART_GALLERY_JS.read_text(encoding="utf-8")
    # The only permitted _m reference is the promote-away replace() regex.
    for line in js.splitlines():
        if "_m.jpg" in line:
            assert "replace(/_m" in line, f"raw _m.jpg emitted outside the promote regex: {line.strip()}"


def test_injected_tiles_request_z_and_ssr_tiles_are_reused():
    js = ART_GALLERY_JS.read_text(encoding="utf-8")
    # Hydrate presence: the script must reuse existing SSR tiles...
    assert "art-thumb.ssr" in js
    assert "ssrByTitle" in js
    # ...and injected tiles must promote data-src through largeThumb (no raw _m).
    assert 'data-src="${esc(largeThumb(art.thumb))}"' in js


def test_load_image_never_overwrites_an_existing_src():
    js = ART_GALLERY_JS.read_text(encoding="utf-8")
    # Hydrate-first guard: the lazy loader must not reassign src on hydrated tiles.
    assert "if (!img || img.src) return;" in js


def test_ssr_tiles_ship_z_sources_and_no_inline_handlers():
    html = ART_HTML.read_text(encoding="utf-8")
    imgs = re.findall(r'<img[^>]+class="art-thumb ssr"[^>]*>', html)
    assert imgs, "no SSR art tiles found in art.html"
    assert all("_m.jpg" not in img for img in imgs), "SSR tile downgraded to _m"
    assert all("onclick" not in img.lower() for img in imgs)
