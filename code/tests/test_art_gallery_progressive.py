"""Real gallery startup, complete browsing, identity, and late detail responses."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / 'src'
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from rendered_site_fixture import REPO_ROOT, serve_copy, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture(scope='module')
def gallery_server(tmp_path_factory):
    skip_without_playwright()
    base, server = serve_copy(tmp_path_factory.mktemp('progressive-gallery'))
    try:
        yield base
    finally:
        stop_server(server)


def test_gallery_bounds_startup_and_keeps_every_record_reachable(gallery_server):
    from playwright.sync_api import sync_playwright

    records = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks']
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        requests = []
        page.on('request', lambda request: requests.append(urlsplit(request.url).path))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        assert '/data/artworks.json' not in requests
        assert page.locator('#grid .art-card').count() == 48
        first_href = page.locator('#grid .art-card').first.get_attribute('href')
        page.evaluate('() => { window.originalGalleryTile = document.querySelector("#grid .art-card"); }')
        page.locator('#sortSelect').select_option('views')
        assert page.locator('#grid .art-card').count() == 48
        page.locator('#sortSelect').select_option('newest')
        assert page.locator('#grid .art-card').first.get_attribute('href') == first_href
        assert page.evaluate('() => document.querySelector("#grid .art-card") === window.originalGalleryTile')
        page.locator('#gallery-more').click()
        assert page.locator('#grid .art-card').count() == 96
        assert page.evaluate('() => document.activeElement.dataset.index') == '48'
        while page.locator('#gallery-more').is_visible():
            page.locator('#gallery-more').click()
        ids = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.dataset.artworkId)')
        assert len(ids) == len(set(ids)) == len(records)
        assert set(ids) == {str(record['id']) for record in records}
        assert '/data/artworks.json' not in requests
        context.close()
        browser.close()


def test_late_details_cannot_replace_new_selection_or_closed_viewer(gallery_server):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        held = []
        page.route('**/data/artworks.json', lambda route: held.append(route))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        titles = page.locator('#grid .art-title').all_text_contents()
        page.locator('#grid .art-card').first.click()
        page.wait_for_function('() => document.getElementById("lb-title").textContent.length > 0')
        assert page.locator('#lb-title').inner_text() == titles[0]
        page.locator('.lb-next').click()
        assert page.locator('#lb-title').inner_text() == titles[1]
        page.keyboard.press('Escape')
        assert page.locator('#lightbox').get_attribute('aria-hidden') == 'true'
        page.locator('#grid .art-card').nth(2).click()
        assert page.locator('#lb-title').inner_text() == titles[2]
        assert len(held) == 1
        held[0].continue_()
        page.wait_for_function('() => document.getElementById("lightbox").getAttribute("aria-busy") === "false"')
        assert page.locator('#lb-title').inner_text() == titles[2]
        assert page.locator('#lb-desc').inner_text() != 'Loading artwork details…'
        page.keyboard.press('Escape')
        assert page.evaluate('() => document.activeElement.dataset.index') == '2'
        context.close()
        browser.close()


def test_duplicate_titles_keep_distinct_source_page_identity(gallery_server):
    from playwright.sync_api import sync_playwright

    payload = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())
    records = payload['artworks'][:2]
    records[1]['title'] = records[0]['title']
    payload['artworks'] = records
    payload['count'] = 2
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json=payload))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 2')
        assert page.locator('#grid .art-card').count() == 2
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == [record['page'] for record in records]
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.dataset.artworkId)') == [str(record['id']) for record in records]
        context.close()
        browser.close()


def test_failed_index_preserves_native_source_links(gallery_server):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(status=503, body='temporarily unavailable'))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.getElementById("emptyState").textContent.includes("could not be loaded")')
        first = page.locator('#grid .art-card').first
        href = first.get_attribute('href')
        assert first.get_attribute('data-index') is None
        assert page.locator('#gallery-more').is_hidden()
        assert (REPO_ROOT / href).is_file()
        with page.expect_navigation() as navigation:
            first.click()
        assert navigation.value.status == 200
        assert page.url == gallery_server + '/' + href
        context.close()
        browser.close()


def test_compact_artwork_index_preserves_all_fields_and_tags():
    from docxology_tools import artwork_pages  # canonical bootstrap
    import build_artwork_index

    source = json.loads((REPO_ROOT / 'data/artworks.json').read_text())
    actual = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())
    assert len(actual['artworks']) == len(source['artworks'])
    for original, compact in zip(source['artworks'], actual['artworks'], strict=True):
        assert compact == {field: artwork_pages.page_rel_path(original) if field == 'page' else original.get(field) for field in build_artwork_index.INDEX_FIELDS}
    pretty_bytes = len((json.dumps(actual, indent=2, ensure_ascii=False) + '\n').encode())
    assert (REPO_ROOT / 'data/artworks-index.json').stat().st_size < pretty_bytes * 0.65


@pytest.mark.parametrize('lightbox_first', [False, True])
def test_description_search_preserves_pages_after_cached_lightbox(gallery_server, lightbox_first):
    from playwright.sync_api import sync_playwright

    records = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks']
    by_id = {str(record['id']): record['page'] for record in records}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        requests = []
        page.on('request', lambda request: requests.append(urlsplit(request.url).path))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        page.evaluate('() => { window.originalGalleryTile = document.querySelector("#grid .art-card"); }')
        if lightbox_first:
            page.locator('#grid .art-card').first.click()
            page.wait_for_function('() => document.getElementById("lightbox").getAttribute("aria-busy") === "false"')
            page.keyboard.press('Escape')
        page.locator('#searchInput').fill('inflection')
        page.wait_for_function('() => document.querySelector(`#grid [data-artwork-id="55349041831"]`) && document.getElementById("grid").getAttribute("aria-busy") !== "true"')
        cards = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => ({id:card.dataset.artworkId,href:card.getAttribute("href")}))')
        assert cards and all(card['href'] == by_id[card['id']] for card in cards)
        target = page.locator('#grid [data-artwork-id="55349041831"]')
        assert target.get_attribute('href') == 'artworks/55349041831-solstice-turning-point.html'
        response = context.request.get(gallery_server + '/' + target.get_attribute('href'))
        assert response.status == 200
        assert response.body() == (REPO_ROOT / target.get_attribute('href')).read_bytes()
        assert requests.count('/data/artworks.json') == 1
        page.locator('#searchInput').fill('')
        assert page.evaluate('() => document.querySelector("#grid .art-card") === window.originalGalleryTile')
        assert page.locator('#grid .art-card').count() == 48
        context.close()
        browser.close()


def test_description_failure_is_visible_and_retry_restores_matches(gallery_server):
    from playwright.sync_api import sync_playwright

    payload = (REPO_ROOT / 'data/artworks.json').read_text()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnail transport is outside these interaction contracts.
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        attempts = []
        def details(route):
            attempts.append(route.request.url)
            if len(attempts) == 1:
                route.fulfill(status=503, body='temporarily unavailable')
            else:
                route.fulfill(status=200, content_type='application/json', body=payload)
        page.route('**/data/artworks.json', details)
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        page.locator('#searchInput').fill('inflection')
        page.get_by_role('button', name='Retry description search').wait_for(state='visible')
        assert 'titles and tags' in page.locator('#gallery-search-status').inner_text()
        page.get_by_role('button', name='Retry description search').click()
        page.wait_for_function('() => document.querySelector(`#grid [data-artwork-id="55349041831"]`) && document.getElementById("grid").getAttribute("aria-busy") === "false"')
        assert len(attempts) == 2
        assert page.locator('#gallery-search-status').is_hidden()
        assert page.locator('#gallery-search-retry').is_hidden()
        context.close()
        browser.close()
