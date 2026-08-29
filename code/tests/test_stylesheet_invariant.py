"""Stylesheet invariant: interactive pages must link style.css.

Extends the invariant family of test_build_video_pages.py (interactive-page
integrity): any page in the lane scope referencing one of the interactive
scripts must also reference style.css, otherwise the unstyled DOM renders
as broken layout (the videos.html overflow class of bug).

Static, no browser. Measured baseline (2026-08-29): 1566 interactive pages,
0 missing style.css.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

INTERACTIVE_SCRIPTS = (
    "interactive.js",
    "tts-controls.js",
    "art-gallery.js",
    "videos-page.js",
)


def lane_pages() -> list[Path]:
    pages = sorted(REPO_ROOT.glob("*.html"))
    pages += sorted((REPO_ROOT / "works").glob("*.html"))
    pages += sorted((REPO_ROOT / "videos").glob("*.html"))
    pages += sorted(REPO_ROOT.glob("papers/*/index.html"))
    return pages


@pytest.fixture(scope="module")
def interactive_pages() -> list[tuple[Path, str]]:
    pairs: list[tuple[Path, str]] = []
    for page in lane_pages():
        text = page.read_text(encoding="utf-8", errors="replace")
        if any(script in text for script in INTERACTIVE_SCRIPTS):
            pairs.append((page, text))
    assert len(pairs) > 1000, f"interactive page scan collapsed: {len(pairs)}"
    return pairs


def test_interactive_pages_link_stylesheet(interactive_pages: list[tuple[Path, str]]) -> None:
    missing = [
        page.relative_to(REPO_ROOT).as_posix()
        for page, text in interactive_pages
        if "style.css" not in text
    ]
    print(f"stylesheet invariant: {len(interactive_pages)} interactive pages; "
          f"{len(missing)} missing style.css")
    assert not missing, (
        f"{len(missing)} interactive pages do not reference style.css:\n"
        + "\n".join(missing[:20])
    )


def test_interactive_pages_use_relative_stylesheet_paths(interactive_pages: list[tuple[Path, str]]) -> None:
    # Root-level absolute paths (/style.css) break under subpath serving,
    # which is how the rendered-nav fixture serves copies; every interactive
    # page must resolve style.css relative to its own location.
    bad: list[str] = []
    for page, text in interactive_pages:
        if "style.css" not in text:
            continue
        for fragment in (
            'href="/style.css"',
            "href='/style.css'",
        ):
            if fragment in text:
                bad.append(f"{page.relative_to(REPO_ROOT).as_posix()}: {fragment}")
    assert not bad, (
        "absolute /style.css references break under subpath serving:\n"
        + "\n".join(bad[:20])
    )
