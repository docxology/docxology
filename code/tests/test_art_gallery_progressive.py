"""Real gallery startup, complete browsing, identity, and late detail responses."""
from __future__ import annotations

import json
import base64
import copy
import re
import sys
import time
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


@pytest.mark.parametrize('failure', ['http', 'schema', 'thumb', 'date', 'identity', 'views', 'views-overflow', 'views-negative'])
def test_early_filters_preserve_source_tiles_while_index_is_pending_or_invalid(gallery_server, failure):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        held = []
        page.route('**/data/artworks-index.json', lambda route: held.append(route))
        with page.expect_request('**/data/artworks-index.json'):
            page.goto(gallery_server + '/art.html', wait_until='domcontentloaded')
        # The request event can precede delivery to its route handler. Yield to
        # the browser event loop until the deliberately held route is ready.
        page.wait_for_function('() => window.filterGallery !== undefined')
        deadline = time.monotonic() + 10
        while not held and time.monotonic() < deadline:
            page.wait_for_timeout(10)
        assert len(held) == 1
        links = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))')
        page.locator('#searchInput').fill('inflection')
        page.locator('#sortSelect').select_option('oldest')
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == links
        if failure == 'http':
            held[0].fulfill(status=503, body='temporarily unavailable')
        elif failure == 'schema':
            held[0].fulfill(json={'artworks': [{'id': 'public-invalid-fixture', 'title': 'Missing canonical path'}]})
        else:
            records = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks']
            # A retained SSR tile skips view-label construction. Use a record
            # outside that initial source batch to reproduce destructive render
            # failures from malformed view counts rather than masking them.
            record = next(art for art in records if art['page'] not in links) if failure.startswith('views') else records[0]
            field, value = {
                'thumb': ('thumb', 'http://%'),
                'date': ('date', '2026-02-30'),
                'identity': ('page', 'artworks/999-different.html'),
                'views': ('views', {'toString': None, 'valueOf': None}),
                'views-overflow': ('views', '9' * 400),
                'views-negative': ('views', -1),
            }[failure]
            record[field] = value
            held[0].fulfill(json={'artworks': [record]})
        page.wait_for_function('() => document.getElementById("emptyState").textContent.includes("could not be loaded")')
        page.locator('#searchInput').fill('different query')
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == links
        first = page.locator('#grid .art-card').first
        assert first.get_attribute('data-index') is None
        with page.expect_navigation() as navigation:
            first.click()
        assert navigation.value.status == 200
        assert page.url == gallery_server + '/' + links[0]
        context.close()
        browser.close()


# 1x1 transparent PNG served for remote thumbnails when a test asserts a clean console.
PIXEL_PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
# The invalid record sits past the first validation chunk (100 records), so the
# index is rejected after the loader has already yielded to the main thread.
LARGE_INDEX_SIZE = 150
INVALID_AT = 120


def _large_index(invalid=None):
    """A >=150 record index built from the real records, optionally with one bad record at 120."""
    records = copy.deepcopy(json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'][:LARGE_INDEX_SIZE])
    assert len(records) == LARGE_INDEX_SIZE
    if invalid == 'thumb':
        records[INVALID_AT]['thumb'] = 'http://%'
    elif invalid == 'identity':
        records[INVALID_AT]['page'] = 'artworks/999-different.html'
    elif invalid == 'duplicate':
        # Uniqueness is tracked across validation chunks: record 120 repeats a record from the first chunk.
        records[INVALID_AT] = copy.deepcopy(records[5])
    else:
        assert invalid is None
    return {'artworks': records, 'count': len(records)}


@pytest.mark.parametrize('failure', ['thumb', 'identity', 'duplicate'])
def test_invalid_record_deep_in_a_large_index_publishes_nothing(gallery_server, failure):
    from playwright.sync_api import sync_playwright

    payload = _large_index(failure)
    ssr_links = re.findall(r'<a class="art-card" href="([^"]+)"', (REPO_ROOT / 'art.html').read_text())
    assert len(ssr_links) >= 30  # server-rendered tiles are shipped, and fewer than one page of the index
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json=payload))
        page.goto(gallery_server + '/art.html', wait_until='domcontentloaded')
        # Snapshot the server-rendered tiles before the index can be consumed.
        page.evaluate('''() => {
            window.ssrTiles = Array.from(document.querySelectorAll("#grid .art-card"));
            window.ssrHtml = document.getElementById("grid").innerHTML;
            window.ssrCount = document.getElementById("resultCount").textContent;
        }''')
        links = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))')
        assert links == ssr_links
        page.wait_for_function('() => document.getElementById("emptyState").textContent.includes("could not be loaded")')
        # Same contract as the early-filter invalid-index test: the source tiles,
        # their order and their links are exactly what was served, and no record
        # of the rejected index (valid prefix included) was published.
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == links
        assert page.evaluate('() => Array.from(document.querySelectorAll("#grid .art-card")).every((card, i) => card === window.ssrTiles[i])')
        assert page.evaluate('() => document.getElementById("grid").innerHTML === window.ssrHtml')
        assert page.evaluate('() => document.getElementById("resultCount").textContent === window.ssrCount')
        assert page.locator('#grid [data-index], #grid [data-artwork-id]').count() == 0
        assert page.locator('#gallery-more').is_hidden()
        # Controls stay inert: the failed index never became the gallery.
        page.locator('#searchInput').fill('different query')
        page.locator('#sortSelect').select_option('oldest')
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == links
        assert page.evaluate('() => document.getElementById("grid").innerHTML === window.ssrHtml')
        first = page.locator('#grid .art-card').first
        assert first.get_attribute('data-index') is None
        with page.expect_navigation() as navigation:
            first.click()
        assert navigation.value.status == 200
        assert page.url == gallery_server + '/' + links[0]
        context.close()
        browser.close()


def test_large_valid_index_hydrates_after_chunked_validation(gallery_server):
    """Control for the invalid-record test: the same 150 records without the bad one are published."""
    from playwright.sync_api import sync_playwright

    payload = _large_index()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json=payload))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        assert page.locator('#resultCount').inner_text() == f'Showing 48 of {LARGE_INDEX_SIZE} artworks'
        assert page.locator('#emptyState').is_hidden()
        context.close()
        browser.close()


DELETE_SCHEDULER_YIELD = '''(() => {
    // scheduler.yield lives on Scheduler.prototype; remove it there and shadow it
    // on the instance so no lookup can find it, forcing the setTimeout(0) fallback.
    if (window.scheduler) {
        try { delete Scheduler.prototype.yield; } catch (_) {}
        Object.defineProperty(window.scheduler, 'yield', { value: undefined, configurable: true });
    }
})();'''


def _watch_console_errors(page):
    errors = []
    page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
    page.on('pageerror', lambda error: errors.append(str(error)))
    return errors


def test_gallery_hydrates_without_scheduler_yield(gallery_server):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        # Remote thumbnails resolve to a pixel so an aborted load cannot read as a console error.
        context.route('https://**/*', lambda route: route.fulfill(status=200, content_type='image/png', body=PIXEL_PNG))
        page = context.new_page()
        errors = _watch_console_errors(page)
        page.add_init_script(DELETE_SCHEDULER_YIELD)
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        assert page.evaluate('() => typeof (window.scheduler && window.scheduler.yield)') == 'undefined'
        assert page.locator('#grid .art-card').count() == 48
        total = len(json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'])
        assert page.locator('#resultCount').inner_text() == f'Showing 48 of {total} artworks'
        assert page.locator('#emptyState').is_hidden()
        assert errors == []
        context.close()
        browser.close()


def _expected_oldest_first(query, limit=None, descriptions=True):
    """Independent oracle: titles, tags and descriptions search, oldest first."""
    index = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'][:limit]
    details = {str(art['id']): art for art in json.loads((REPO_ROOT / 'data/artworks.json').read_text())['artworks']}
    needle = query.lower()
    matches = [art for art in index
               if needle in str(art['title'] or '').lower()
               or (descriptions and needle in str(details[str(art['id'])].get('desc') or '').lower())
               or any(needle in str(tag).lower() for tag in art['tags'])]
    matches.sort(key=lambda art: str(art.get('date') or ''))  # stable, like Array.prototype.sort
    return [str(art['id']) for art in matches]


def test_controls_changed_while_the_index_is_held_decide_the_final_grid(gallery_server):
    from playwright.sync_api import sync_playwright

    expected = _expected_oldest_first('night')
    published = _expected_oldest_first('night', descriptions=False)  # what the index alone can match
    assert 0 < len(published) < 48 < len(expected) < 200  # the final state needs descriptions and the load-more count text
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        held = []
        details = []
        page.route('**/data/artworks-index.json', lambda route: held.append(route))
        # Holding the descriptions as well exposes the grid the index alone produced.
        page.route('**/data/artworks.json', lambda route: details.append(route))
        with page.expect_request('**/data/artworks-index.json'):
            page.goto(gallery_server + '/art.html', wait_until='domcontentloaded')
        page.wait_for_function('() => window.filterGallery !== undefined')
        deadline = time.monotonic() + 10
        while not held and time.monotonic() < deadline:
            page.wait_for_timeout(10)
        assert len(held) == 1
        links = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))')
        # Type (real key events) and change the sort control repeatedly while the
        # index is in flight. Only the last state may matter.
        search = page.locator('#searchInput')
        search.press_sequentially('spiral')
        page.locator('#sortSelect').select_option('title')
        search.fill('')
        page.locator('#sortSelect').select_option('views')
        search.press_sequentially('night')
        page.locator('#sortSelect').select_option('oldest')
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.getAttribute("href"))') == links
        assert page.locator('#grid [data-index]').count() == 0
        assert details == []  # the loader has not published, so nothing asked for descriptions
        held[0].continue_()
        # Published: the grid follows the final controls using titles and tags only.
        page.wait_for_function(
            '(text) => document.getElementById("resultCount").textContent === text',
            arg=f'{len(published)} artworks')
        assert page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.dataset.artworkId)') == published
        assert page.locator('#grid').get_attribute('aria-busy') == 'true'
        deadline = time.monotonic() + 10
        while not details and time.monotonic() < deadline:
            page.wait_for_timeout(10)
        assert len(details) == 1
        details[0].continue_()
        page.wait_for_function(
            '(text) => document.getElementById("resultCount").textContent === text && document.getElementById("grid").getAttribute("aria-busy") === "false"',
            arg=f'Showing 48 of {len(expected)} artworks')
        assert search.input_value() == 'night'
        assert page.locator('#sortSelect').input_value() == 'oldest'
        ids = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.dataset.artworkId)')
        assert ids == expected[:48]
        assert page.locator('#gallery-more').inner_text() == f'Show {min(48, len(expected) - 48)} more artworks'
        assert page.locator('#emptyState').is_hidden()
        assert len(details) == 1
        context.close()
        browser.close()


HOLD_SCHEDULER_YIELDS = '''(() => {
    // Every scheduler.yield() call parks until the test releases it, so the test
    // decides exactly when the loader resumes.
    window.heldYields = [];
    Object.defineProperty(window.scheduler, 'yield', {
        configurable: true,
        value: () => new Promise(resolve => window.heldYields.push(resolve)),
    });
})();'''


@pytest.mark.parametrize('final_query', ['sun', ''])
def test_controls_changed_while_the_loader_is_parked_after_publishing_decide_the_final_grid(gallery_server, final_query):
    """An index under one validation chunk yields only once, after the data is published and before the first render.

    Typing starts the description search, whose completion re-renders from the live
    controls and can mask a stale loader render. The sort-only case never types, so
    the loader's own render is the only one and must already reflect the final sort.
    """
    from playwright.sync_api import sync_playwright

    subset = 60
    payload = {'artworks': json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'][:subset], 'count': subset}
    expected = _expected_oldest_first(final_query, subset)
    if final_query:
        # Some matches exist only in descriptions, so the final state needs the detail fetch too.
        assert 1 < len(expected) <= 48
        assert len(_expected_oldest_first(final_query, subset, descriptions=False)) < len(expected)
        count_text = f'{len(expected)} artworks'
    else:
        assert len(expected) == subset
        count_text = f'Showing 48 of {subset} artworks'
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        page.add_init_script(HOLD_SCHEDULER_YIELDS)
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json=payload))
        page.goto(gallery_server + '/art.html', wait_until='domcontentloaded')
        page.wait_for_function('() => window.heldYields.length === 1')
        # The loader is parked with the index published but not yet rendered.
        search = page.locator('#searchInput')
        if final_query:
            search.press_sequentially('tree')
        page.locator('#sortSelect').select_option('title')
        if final_query:
            search.fill('')
        page.locator('#sortSelect').select_option('views')
        if final_query:
            search.press_sequentially(final_query)
        page.locator('#sortSelect').select_option('oldest')
        page.evaluate('() => window.heldYields.forEach(resolve => resolve())')
        page.wait_for_function(
            '(text) => document.getElementById("resultCount").textContent === text && document.getElementById("grid").getAttribute("aria-busy") !== "true"',
            arg=count_text)
        assert search.input_value() == final_query
        assert page.locator('#sortSelect').input_value() == 'oldest'
        assert page.evaluate('() => window.heldYields.length') == 1
        ids = page.locator('#grid .art-card').evaluate_all('(cards) => cards.map(card => card.dataset.artworkId)')
        assert ids == expected[:48]
        assert page.locator('#gallery-more').is_hidden() == (len(expected) <= 48)
        assert page.locator('#emptyState').is_hidden()
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


@pytest.mark.parametrize('failure', ['schema', 'missing', 'duplicate', 'url', 'date', 'views', 'views-overflow'])
def test_invalid_detail_payload_is_retryable_without_claiming_complete_search(gallery_server, failure):
    from playwright.sync_api import sync_playwright

    payload = json.loads((REPO_ROOT / 'data/artworks.json').read_text())
    invalid = json.loads(json.dumps(payload))
    if failure == 'schema':
        invalid['artworks'][0]['desc'] = None
    elif failure == 'missing':
        invalid['artworks'].pop(0)
    elif failure == 'duplicate':
        invalid['artworks'].append(invalid['artworks'][0])
    elif failure == 'url':
        invalid['artworks'][0]['sizes']['Large'] = 'http://%'
    elif failure == 'date':
        invalid['artworks'][0]['date'] = 17
    else:
        invalid['artworks'][0]['views'] = {'toString': None, 'valueOf': None} if failure == 'views' else '9' * 400
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.abort())
        page = context.new_page()
        attempts = []
        def details(route):
            attempts.append(route.request.url)
            route.fulfill(json=invalid if len(attempts) == 1 else payload)
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
        context.close()
        browser.close()


@pytest.mark.parametrize('preview_available', [True, False])
@pytest.mark.parametrize('viewport_width', [1280, 412])
def test_lightbox_media_failure_uses_distinct_retained_previews_and_native_links(gallery_server, preview_available, viewport_width):
    from playwright.sync_api import sync_playwright

    compact = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'][0]
    detail = json.loads((REPO_ROOT / 'data/artworks.json').read_text())['artworks'][0]
    media_base = 'https://images.example.test/'
    detail['sizes'] = {'Large 1600': media_base + 'large.jpg', 'Large': media_base + 'large.jpg',
                       'Medium': media_base + 'preview.jpg', 'Original': media_base + 'original.jpg'}
    # A valid synthetic pixel is enough to exercise Chromium image decoding.
    pixel = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': viewport_width, 'height': 900}, service_workers='block')
        context.route('https://**/*', lambda route: route.fulfill(status=429, body='rate limited'))
        page = context.new_page()
        requests = []
        def image(route):
            requests.append(route.request.url)
            if preview_available and route.request.url.endswith('preview.jpg'):
                route.fulfill(status=200, content_type='image/png', body=pixel)
            else:
                route.fulfill(status=429, body='rate limited')
        page.route(media_base + '**', image)
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json={'artworks': [compact]}))
        page.route('**/data/artworks.json', lambda route: route.fulfill(json={'artworks': [detail]}))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 1')
        page.locator('#grid .art-card').click()
        if preview_available:
            page.wait_for_function('() => document.getElementById("lb-img").naturalWidth > 0 && document.getElementById("lb-image-status").textContent.includes("smaller preview")')
            assert page.locator('#lb-img').is_visible()
            assert page.locator('#lb-img').get_attribute('src') == media_base + 'preview.jpg'
        else:
            page.wait_for_function('() => document.getElementById("lb-image-status").textContent.includes("could not be loaded") && document.getElementById("lightbox").getAttribute("aria-busy") === "false"')
            assert page.locator('#lb-img').is_hidden()
        assert requests == [media_base + 'large.jpg', media_base + 'preview.jpg']
        assert page.locator('#lb-image-status').is_visible()
        assert page.locator('#lb-artwork-link').is_visible()
        assert page.locator('#lb-flickr-link').is_visible()
        assert page.locator('#lb-artwork-link').get_attribute('href') == compact['page']
        assert page.locator('#lb-download').get_attribute('href') == media_base + 'original.jpg'
        assert page.locator('#lb-flickr-link').get_attribute('href') == detail['flickr_url']
        if viewport_width == 412 and not preview_available:
            with page.expect_navigation() as navigation:
                page.locator('#lb-artwork-link').click()
            assert navigation.value.status == 200
            assert page.url == gallery_server + '/' + compact['page']
        else:
            page.keyboard.press('Escape')
            assert page.evaluate('() => document.activeElement.dataset.index') == '0'
        context.close()
        browser.close()


def test_ssr_thumbnail_fallback_preserves_decoded_tile_across_sorting(gallery_server):
    from playwright.sync_api import sync_playwright

    compact = json.loads((REPO_ROOT / 'data/artworks-index.json').read_text())['artworks'][0]
    pixel = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(service_workers='block')
        context.route('https://**/*', lambda route: route.fulfill(status=429, body='rate limited'))
        page = context.new_page()
        requests = []
        def preview(route):
            requests.append(route.request.url)
            route.fulfill(status=200, content_type='image/png', body=pixel)
        page.route(compact['thumb'], preview)
        page.route('**/data/artworks-index.json', lambda route: route.fulfill(json={'artworks': [compact]}))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelector("#grid [data-index] img").naturalWidth > 0')
        assert page.locator('#grid img').get_attribute('src') == compact['thumb']
        page.evaluate('() => { window.decodedTile = document.querySelector("#grid .art-card"); }')
        page.locator('#sortSelect').select_option('oldest')
        assert page.evaluate('() => document.querySelector("#grid .art-card") === window.decodedTile')
        assert requests == [compact['thumb']]
        context.close()
        browser.close()


def test_gallery_does_not_request_unrelated_decorative_media(gallery_server):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(service_workers='block')
        page.route('https://**/*', lambda route: route.abort())
        requests = []
        page.on('request', lambda request: requests.append(urlsplit(request.url).path))
        page.goto(gallery_server + '/art.html')
        page.wait_for_function('() => document.querySelectorAll("#grid [data-index]").length === 48')
        assert not any('/assets/hero-art/' in path for path in requests)
        browser.close()
