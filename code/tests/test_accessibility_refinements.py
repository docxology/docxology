"""Real reading landmarks and crowded video dates remain accessible."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rendered_site_fixture import AXE_JS, REPO_ROOT, serve_copy, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture(scope="module")
def accessibility_server(tmp_path_factory):
    skip_without_playwright()
    base_url, server = serve_copy(tmp_path_factory.mktemp("accessibility"))
    shutil.copy2(AXE_JS, Path(server._directory) / "axe.min.js")
    try:
        yield base_url
    finally:
        stop_server(server)


@pytest.fixture
def browser_page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900}, service_workers="block", timezone_id="America/Los_Angeles")
        page = context.new_page()
        # This gate exercises the served application. Remote thumbnail/font
        # availability is separately checked by live/external-link acceptance.
        page.route("**/*", lambda route: route.continue_() if route.request.url.startswith("http://127.0.0.1:") else route.abort())
        try:
            yield page
        finally:
            context.close()
            browser.close()


def load_videos(page, base_url: str, query: str = "") -> None:
    page.goto(f"{base_url}/videos.html{query}", wait_until="load")
    page.wait_for_function("() => document.querySelector('#loading').style.display === 'none' && document.querySelector('#count-badge').textContent.includes('videos')")


def timeline_ids_and_rectangles(page):
    return page.locator("#timeline-canvas .vid-card").evaluate_all("""cards => cards.map(card => ({
        ids: JSON.parse(card.dataset.videoIds), channel: card.dataset.channel,
        left: card.offsetLeft, top: card.offsetTop, width: card.offsetWidth, height: card.offsetHeight,
        label: card.getAttribute('aria-label'), tag: card.tagName,
    }))""")


def assert_complete_safe_timeline(page, expected_ids: list[str]) -> None:
    cards = timeline_ids_and_rectangles(page)
    actual = [video_id for card in cards for video_id in card["ids"]]
    assert sorted(actual) == sorted(expected_ids)
    assert len(actual) == len(set(actual)), "grouping duplicated video IDs"
    for card in cards:
        assert card["width"] >= 24 and card["height"] >= 24
        assert card["label"]
    for index, left in enumerate(cards):
        for right in cards[index + 1:]:
            overlap_x = min(left["left"] + left["width"], right["left"] + right["width"]) - max(left["left"], right["left"])
            overlap_y = min(left["top"] + left["height"], right["top"] + right["height"]) - max(left["top"], right["top"])
            assert overlap_x <= 0 or overlap_y <= 0, (left, right)


def relevant_axe_violations(page, base_url: str):
    page.add_script_tag(url=f"{base_url}/axe.min.js")
    return page.evaluate("""async () => (await axe.run(document, {
        runOnly: {type: 'rule', values: ['region', 'color-contrast', 'target-size', 'aria-valid-attr-value', 'aria-dialog-name']},
        resultTypes: ['violations'],
    })).violations.map(v => ({id: v.id, nodes: v.nodes.map(n => ({target: n.target, summary: n.failureSummary}))}))""")


@pytest.mark.parametrize("route", ["index.html", "videos.html"])
def test_reading_progress_is_in_main_and_reports_scroll(accessibility_server, browser_page, route):
    page = browser_page
    page.goto(f"{accessibility_server}/{route}", wait_until="load")
    progress = page.get_by_role("progressbar", name="Reading progress")
    assert progress.count() == 1
    assert progress.evaluate("bar => Boolean(bar.closest('main, [role=main]'))")
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_function("() => document.querySelector('.reading-progress').getAttribute('aria-valuenow') === '100'")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_function("() => document.querySelector('.reading-progress').getAttribute('aria-valuenow') === '0'")
    assert progress.get_attribute("aria-valuemin") == "0"
    assert progress.get_attribute("aria-valuemax") == "100"


@pytest.mark.parametrize("zoom", [0, 1, 2])
def test_real_catalog_is_complete_without_obscured_targets(accessibility_server, browser_page, zoom):
    page = browser_page
    load_videos(page, accessibility_server, f"?z={zoom}")
    records = json.loads((REPO_ROOT / "data/videos-index.json").read_text())["videos"]
    assert_complete_safe_timeline(page, [record["id"] for record in records])
    assert page.locator(f'[data-zoom="{zoom}"]').get_attribute("aria-pressed") == "true"
    assert relevant_axe_violations(page, accessibility_server) == []


def test_cluster_dialog_keeps_native_routes_and_keyboard_focus(accessibility_server, browser_page):
    page = browser_page
    load_videos(page, accessibility_server)
    cluster = page.locator("button.vid-card").first
    ids = json.loads(cluster.get_attribute("data-video-ids"))
    assert len(ids) > 1
    cluster.focus()
    page.keyboard.press("Enter")
    dialog = page.get_by_role("dialog")
    assert dialog.is_visible()
    assert page.get_by_role("button", name="Close", exact=True).evaluate("button => button === document.activeElement")
    links = dialog.locator("li a")
    assert links.count() == len(ids)
    channel = cluster.get_attribute("data-channel")
    assert links.evaluate_all("links => links.map(link => link.getAttribute('href'))") == [f"videos/{channel}-{video_id}.html" for video_id in ids]
    assert relevant_axe_violations(page, accessibility_server) == []
    page.keyboard.press("?")
    assert page.locator("#shortcuts-overlay").get_attribute("aria-hidden") == "true"
    page.keyboard.press("Escape")
    assert not dialog.is_visible()
    assert cluster.evaluate("button => button === document.activeElement")
    page.keyboard.press("Enter")
    href = links.first.get_attribute("href")
    links.first.focus()
    page.keyboard.press("Enter")
    page.wait_for_url(f"{accessibility_server}/{href}")
    page.get_by_role("heading", level=1).wait_for(state="visible")


def test_dense_same_day_groups_and_literal_long_titles(accessibility_server, browser_page):
    page = browser_page
    records = []
    for channel in ["personal", "institute"]:
        for index in range(130):
            records.append({"id": f"{channel}-{index:03}", "title": f"Dense {channel} {index:03} " + "Long title <script>literal</script> " * 25, "channel": channel, "upload_date": "20240331", "year": 2024})
    payload = {"videos": records, "channels": {"personal": {"fetched_at": "2026-10-02"}}}
    page.route("**/data/videos-index.json", lambda route: route.fulfill(json=payload))
    load_videos(page, accessibility_server)
    # Upload dates and padding use UTC: crossing Pacific daylight saving time
    # must not move this video's date-based timeline position back one day.
    assert page.evaluate("dayOffset('20240331')") == 30
    assert_complete_safe_timeline(page, [record["id"] for record in records])
    assert page.locator("button.vid-card").count() == 8
    assert page.locator("#count-badge strong").inner_text() == "260"
    page.locator("button.vid-card").first.click()
    dialog = page.get_by_role("dialog")
    assert "Mar 31, 2024" in dialog.inner_text()
    assert "<script>literal</script>" in dialog.locator("li a").first.inner_text()
    assert dialog.locator("script").count() == 0
    assert dialog.evaluate("dialog => dialog.scrollWidth <= dialog.clientWidth + 1")
    page.keyboard.press("Escape")
    page.locator("#search").fill("DENSE PERSONAL 129")
    assert_complete_safe_timeline(page, ["personal-129"])
    assert page.locator("a.vid-card").get_attribute("href") == "videos/personal-personal-129.html"
    assert page.locator("#count-badge strong").inner_text() == "1"


@pytest.mark.parametrize("width,scheme", [(320, "dark"), (412, "light")])
def test_mobile_uses_filtered_list_and_passes_contrast(accessibility_server, browser_page, width, scheme):
    page = browser_page
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(color_scheme=scheme, reduced_motion="reduce")
    load_videos(page, accessibility_server, "?ch=institute")
    assert not page.locator("#timeline-wrap").is_visible()
    assert page.locator("#mobile-list").is_visible()
    assert not page.locator(".mobile-channel-title.personal").is_visible()
    assert page.locator(".mobile-channel-title.institute").is_visible()
    assert page.locator('[data-ch="institute"]').get_attribute("aria-pressed") == "true"
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")
    assert relevant_axe_violations(page, accessibility_server) == []


@pytest.mark.parametrize("width", [320, 412])
def test_mobile_year_jump_respects_visible_channel_and_no_matches(accessibility_server, browser_page, width):
    page = browser_page
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(reduced_motion="reduce")
    load_videos(page, accessibility_server, "?ch=institute")
    records = json.loads((REPO_ROOT / "data/videos-index.json").read_text())["videos"]
    institute_years = {record["year"] for record in records if record["channel"] == "institute"}
    selected_year = min(institute_years)
    target = page.locator(f'.mobile-channel-section:has(.institute) .mobile-vid-item[data-year="{selected_year}"]').first
    assert target.bounding_box()["y"] > 900
    page.locator("#year-jump").select_option(str(selected_year))
    page.wait_for_function("""year => {
        const item = document.querySelector(`.mobile-channel-section:has(.institute) .mobile-vid-item[data-year="${year}"]`);
        const rect = item.getBoundingClientRect();
        return rect.top >= 0 && rect.bottom <= window.innerHeight;
    }""", arg=selected_year)
    assert page.locator("#year-jump").input_value() == ""
    assert not page.locator("#timeline-wrap").is_visible()
    # A year absent from the selected channel must leave the viewport in
    # place; it must not jump to a hidden personal video or hidden timeline.
    absent_years = {record["year"] for record in records} - institute_years
    assert absent_years
    before = page.evaluate("window.scrollY")
    page.evaluate("year => jumpToYear(year)", min(absent_years))
    assert page.evaluate("window.scrollY") == before


def test_dialog_in_forced_colors_and_reduced_motion(accessibility_server, browser_page):
    page = browser_page
    page.emulate_media(forced_colors="active", reduced_motion="reduce")
    load_videos(page, accessibility_server)
    cluster = page.locator("button.vid-card").first
    cluster.focus()
    page.keyboard.press("Enter")
    assert page.get_by_role("dialog").is_visible()
    assert page.get_by_role("button", name="Close", exact=True).evaluate("button => getComputedStyle(button).color !== getComputedStyle(button).backgroundColor")
    page.keyboard.press("Escape")
    assert cluster.evaluate("button => button === document.activeElement")


def test_video_no_javascript_keeps_static_index(accessibility_server, browser_page):
    # A fresh context proves the native fallback without an enhanced-page cache.
    context = browser_page.context.browser.new_context(java_script_enabled=False, service_workers="block", viewport={"width": 320, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{accessibility_server}/videos.html", wait_until="load")
        link = page.locator("noscript a", has_text="static video index")
        assert link.is_visible()
        assert link.get_attribute("href") == "videos/"
        link.click()
        page.wait_for_url(f"{accessibility_server}/videos/")
        page.get_by_role("heading", level=1).wait_for(state="visible")
    finally:
        context.close()
