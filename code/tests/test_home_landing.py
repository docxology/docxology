"""Actual homepage routes and complete Curio Cards remain usable on mobile."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rendered_site_fixture import REPO_ROOT, serve_copy, skip_without_playwright, stop_server  # noqa: E402


CARD_HASHES = {
    "24-complexity.jpg": "b0b832c56edd3c72b842e43039256a6a1f6e2a31eb63c7e26d42d0c7afa6219a",
    "25-passion.jpg": "b601063f76e78c4117c77a185d1cf4af5837543d640d1c96e3d0d5c39b5304ed",
    "26-education.jpg": "164dc0a6f02c84c0bfa79ac786e524fa727264e72adfb11eb2bf4d6c718781eb",
}


@pytest.fixture(scope="module")
def homepage_server(tmp_path_factory):
    skip_without_playwright()
    base_url, server = serve_copy(tmp_path_factory.mktemp("homepage"))
    try:
        yield base_url
    finally:
        stop_server(server)


def test_curio_images_match_verified_official_sources() -> None:
    root = REPO_ROOT / "assets" / "curio-cards"
    provenance = json.loads((root / "provenance.json").read_text(encoding="utf-8"))
    records = {record["filename"]: record for record in provenance["assets"]}
    assert records.keys() == CARD_HASHES.keys()
    for filename, expected in CARD_HASHES.items():
        blob = (root / filename).read_bytes()
        record = records[filename]
        assert hashlib.sha256(blob).hexdigest() == record["sha256"] == expected
        assert len(blob) == record["bytes"]
        assert record["source_page"] == f"https://curio.cards/card/{record['card_number']}/"
        assert (record["width"], record["height"], record["transformation"]) == (900, 1200, "none")


@pytest.mark.parametrize("width", [320, 412, 1280])
@pytest.mark.parametrize("color_scheme", ["dark", "light"])
def test_homepage_paths_and_actual_curio_images(homepage_server: str, width: int, color_scheme: str) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=color_scheme, service_workers="block")
        page = context.new_page()
        page.goto(f"{homepage_server}/index.html", wait_until="load")
        assert page.locator(".hero h1").inner_text() == "Daniel Ari Friedman"
        assert page.locator(".home-pathway").evaluate_all("links => links.map(link => link.getAttribute('href'))") == [
            "publications.html", "software.html", "art.html", "#teaching",
        ]
        assert page.locator(".home-actions a").first.bounding_box()["y"] < 900
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")
        cards = page.locator(".curio-card")
        assert cards.count() == 3
        for index, number in enumerate([24, 25, 26]):
            card = cards.nth(index)
            card.scroll_into_view_if_needed()
            image = card.locator("img")
            image.evaluate("image => image.decode()")
            assert card.get_attribute("href") == f"https://curio.cards/card/{number}/"
            assert image.get_attribute("alt")
            assert image.get_attribute("loading") == "lazy"
            dimensions = image.evaluate("image => ({width: image.naturalWidth, height: image.naturalHeight, fit: getComputedStyle(image).objectFit, rect: image.getBoundingClientRect().toJSON()})")
            assert (dimensions["width"], dimensions["height"], dimensions["fit"]) == (900, 1200, "contain")
            assert abs(dimensions["rect"]["height"] / dimensions["rect"]["width"] - 4 / 3) < .01
            assert card.evaluate("card => getComputedStyle(card, '::before').content") in {"none", "normal"}
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")
        page.locator(".home-profiles summary").scroll_into_view_if_needed()
        page.locator(".home-profiles summary").focus()
        page.keyboard.press("Enter")
        assert page.locator(".home-profiles").get_attribute("open") is not None
        assert page.locator(".home-profiles a", has_text="ORCID").is_visible()
        context.close()
        browser.close()


@pytest.mark.parametrize("width", [320, 412])
def test_homepage_no_javascript_keeps_routes_and_media_reachable(homepage_server: str, width: int) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False, service_workers="block")
        page = context.new_page()
        page.goto(f"{homepage_server}/index.html", wait_until="load")
        assert page.locator("nav a", has_text="Publications").is_visible()
        assert page.locator(".home-pathway").count() == 4
        assert not page.locator(".media-tabs").is_visible()
        for panel in ["video", "podcasts", "talks", "interviews", "press"]:
            assert page.locator(f"#tab-{panel}").is_visible()
        page.locator(".home-profiles summary").click()
        assert page.locator(".home-profiles a", has_text="ORCID").is_visible()
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")
        context.close()
        browser.close()


def test_homepage_reduced_motion_does_not_hide_primary_content(homepage_server: str) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 412, "height": 900}, reduced_motion="reduce", service_workers="block")
        page = context.new_page()
        page.goto(f"{homepage_server}/index.html", wait_until="load")
        assert page.locator(".hero-content").evaluate("element => getComputedStyle(element).animationName") == "none"
        page.locator('.home-pathway[href="#teaching"]').click()
        page.wait_for_function("location.hash === '#teaching'")
        assert page.locator("#teaching").bounding_box()["y"] >= 0
        assert page.locator("#teaching").bounding_box()["y"] < 200
        assert page.locator("#teaching").is_visible()
        context.close()
        browser.close()
