"""Rendered art grid: hydrated srcs (no _m.jpg) and tile dimension hints."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rendered_site_fixture import serve_copy, stop_server  # noqa: E402

CHECK_JS = """
() => {
  const badSrcs = [];
  document.querySelectorAll('img').forEach((img) => {
    const src = img.getAttribute('src') || '';
    if (src.includes('_m.jpg')) {
      badSrcs.push(src);
    }
  });
  const imgs = [...document.querySelectorAll('.art-grid img, #art-grid img, img.art-thumb')];
  const missingDims = imgs
    .filter((img) => {
      if (img.getAttribute('width') && img.getAttribute('height')) return false;
      const style = getComputedStyle(img);
      const tile = img.closest('[style*="aspect-ratio"], .art-tile, .tile');
      const tileStyle = tile ? getComputedStyle(tile) : null;
      return style.aspectRatio === 'auto' && !(tileStyle && tileStyle.aspectRatio !== 'auto');
    })
    .map((img) => img.getAttribute('src'));
  return { badSrcs, missingDims, total: imgs.length };
}
"""


def test_rendered_art_grid_hydrated(tmp_path: Path) -> None:
    from rendered_site_fixture import skip_without_playwright

    skip_without_playwright()
    from playwright.sync_api import sync_playwright  # noqa: E402  (after skip guard)
    base_url, httpd = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
            for path in ("art.html", "index.html"):
                page.goto(f"{base_url}/{path}", wait_until="load")
                page.wait_for_timeout(1500)  # let JS hydration settle
                result = page.evaluate(CHECK_JS)
                assert result["badSrcs"] == [], (
                    f"{path}: {len(result['badSrcs'])} imgs still use _m.jpg srcs "
                    f"after JS settle: {result['badSrcs'][:5]}"
                )
                assert result["missingDims"] == [], (
                    f"{path}: {len(result['missingDims'])} art imgs lack "
                    f"width/height attrs or an aspect-ratio tile: {result['missingDims'][:5]}"
                )
            browser.close()
    finally:
        stop_server(httpd)
