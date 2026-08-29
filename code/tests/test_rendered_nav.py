"""Rendered nav reachability: no nav link extends past the viewport.

Serves a COPY of the built site (never the live checkout) and probes nav
anchors at 900/1024/1152/1280/1440/1920. Skips cleanly when playwright or
chromium is unavailable locally; CI installs them.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rendered_site_fixture import LANE_PAGES, NAV_VIEWPORTS, serve_copy, skip_without_playwright, stop_server  # noqa: E402

PROBE_JS = """
() => {
  const width = document.documentElement.clientWidth;
  const offenders = [];
  document.querySelectorAll('nav a, header nav a').forEach((a) => {
    const rect = a.getBoundingClientRect();
    if (rect.right > width + 1 || rect.left < -1) {
      offenders.push({
        text: (a.textContent || '').trim().slice(0, 40),
        href: a.getAttribute('href'),
        right: Math.round(rect.right),
        left: Math.round(rect.left),
        viewport: width,
      });
    }
  });
  return { width, offenders };
}
"""


def test_rendered_nav_no_horizontal_overflow(tmp_path: Path) -> None:
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base_url, httpd = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for width in NAV_VIEWPORTS:
                context = browser.new_context(viewport={"width": width, "height": 900})
                page = context.new_page()
                for path in LANE_PAGES:
                    page.goto(f"{base_url}/{path}", wait_until="load")
                    page.wait_for_timeout(150)
                    result = page.evaluate(PROBE_JS)
                    key = (path, width)
                    allowed = NAV_BASELINE.get(key, set())
                    new_offenders = [
                        item
                        for item in result["offenders"]
                        if item["href"] not in allowed
                    ]
                    assert new_offenders == [], (
                        f"{path} @ {width}px: nav links overflow viewport "
                        f"(clientWidth={result['width']}): {new_offenders[:5]}"
                    )
                context.close()
            browser.close()
    finally:
        stop_server(httpd)


# Baseline: empty since 2026-08-29 - videos.html shipped no inline .nav-more
# dropdown rules, so when style.css was absent (fixture copy / subpath serving)
# the More panel rendered inline and its links overflowed at every width.
# Inline nav-more rules landed in videos.html; any NEW overflow fails the test.
NAV_BASELINE: dict[tuple[str, int], set[str]] = {}
