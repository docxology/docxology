# Site runtime and browser acceptance

The static site progressively enhances readable HTML with navigation, search,
clipboard actions, and an optional offline worker. The declared behavior lives
in [`js/`](../../js/), [`style.css`](../../style.css), and
[`sw.js`](../../sw.js). Source changes require shared-script cache-tag updates,
generated-page rebuilding, and browser acceptance before publication.

The synchronous head asset [`nav-toggle.js`](../../js/nav-toggle.js) attaches
the working mobile control as the header is parsed, then collapses its links
before first paint. It owns the toggle independently of the larger interactive
script. Delayed or failed interactive loading cannot move the page by replacing
an expanded header. If the head asset is blocked or JavaScript is disabled,
navigation stays expanded in normal flow and every route remains reachable.
Pages without a mobile toggle omit this asset. Keep the head tag synchronous;
deferring it would restore the first-paint layout shift.

## Search loading

The dedicated search page initially browses
[`search-index-bootstrap.json`](../../search-index-bootstrap.json): up to 40
entries plus complete catalog type counts. This preview supplies the first
unfiltered result page without fetching the full core or text segments. Typing
a query or selecting a scoped type loads the full core before searching that
scope; a query in the URL starts that complete search immediately. A missing or
malformed preview falls back to the core. Late preview responses cannot replace
a newer query or filter selection.

[`search-utils.js`](../../js/search-utils.js) shares one cached core-index
request across consumers. Header autocomplete uses
[`search-index-core.json`](../../search-index-core.json). The dedicated search
page adds work/video detail segments only for a nonempty query; a work-only
filter loads only the work segment, and a video-only filter only the video
segment. Deep text matches retain the same AND, word-boundary, and symbol-search
rules. Failed core requests and failed or malformed segments expose retryable
errors; available matches remain distinct from a complete full-text search.

[`search-index.json`](../../search-index.json) remains the complete export for
agents and offline tooling. Generate all projections together with
`code/orchestrators/build_search_index.py`; do not hand-edit them.

The search page reserves the type-filter row before the core arrives. Its
horizontal strip keeps the result area in place at narrow widths, and keyboard
focus scrolls later options into view. Keep the search panel's grid column
bounded with `minmax(0, 1fr)` so long labels cannot widen the document.

## Gallery and publication loading

The artwork gallery filters and sorts the complete compact
[`data/artworks-index.json`](../../data/artworks-index.json), then renders up to
48 matching tiles. “Show more” adds the next batch and focuses its first new
tile. Filtering resets the rendered batch, without limiting the searchable
catalog to the previously visible tiles. Server-rendered cards retain their
images and native generated artwork-page links; identity follows the canonical
page URL so duplicate titles remain separate works. Modified or middle clicks
keep native navigation, while an ordinary click opens the detail lightbox.
Compact-catalog validation happens before replacing the server-rendered cards;
malformed or failed data cannot erase that native fallback.

[`data/artworks.json`](../../data/artworks.json) loads when a description query
or detail view needs it. Description-load failure preserves title/tag matches
and exposes a retry. Failed detail requests can be retried by reopening or
navigating the lightbox; older responses cannot overwrite a newer selection or
reopen a closed view. The complete export remains available independently of
the initial batch and compact index.
Full-detail records must have unique identities, valid retained fields/media
URLs, and coverage of the loaded compact catalog before they are cached as
complete. Malformed or incomplete responses leave description search explicitly
partial and retryable. Thumbnail and lightbox images try only the distinct
retained source URLs once each; exhaustion marks the image unavailable and
preserves the native artwork-page link. Changing selection retires previous
image callbacks so late failures cannot overwrite the current view.

The publications page renders its catalog from
[`data/works.json`](../../data/works.json) without waiting for
[`data/work-enrichment.json`](../../data/work-enrichment.json). Abstract and
keyword enrichment begins only after a nonempty publication query. While that
request is pending or failed, catalog matches remain usable with an explicit
status and retry. Completion applies the current query, scope, and sort instead
of restoring the state that initiated the request. Catalog-load failure keeps
the server-rendered publication links available.
The page sorts the complete matching catalog before rendering its first 50
rows. “Load more” adds another batch and focuses the first newly added title
link. Filtering or changing sort resets the batch; the button is hidden when
all matches are shown, including empty results. Row counts describe the current
matching catalog rather than treating the rendered batch as the full index.

## Accessible video browsing

The video timeline keeps four rows per channel and groups records when nearby
upload dates would otherwise overlap their click targets. Single-video tiles
remain native links. Numbered groups show their actual count and date range,
then open a native dialog containing every original title, upload date, and
generated video-page link. No records are discarded to reduce the timeline.
The dialog owns Escape and focus restoration, and does not open the site's
separate shortcut or speech overlays from its keyboard events.

Mobile widths use the searchable list rather than an inline-style override of
the hidden timeline. The year menu scrolls to a visible matching-channel item;
an absent year leaves the viewport in place. Reduced-motion preferences disable
that scroll animation. Zoom and channel controls expose their pressed state,
date calculations use UTC across daylight-saving boundaries, and the video
hero and shared reading-progress widget live within appropriate landmarks.
Without JavaScript, native links still reach the static video index.

Homepage decorative background suppression is scoped to
[`css/home.css`](../../css/home.css); it avoids generic hero/card imagery
competing with the actual Curio images. The publications page also disables
decorative artwork tokens within `.publications-page` in its authoritative
[`template`](../../code/templates/publications.html.tmpl), preserving the shared
gradients, borders, and catalog content. Other pages retain the shared artwork
tokens.

The optional [`hero-glitch.js`](../../js/hero-glitch.js) runs only on pages that
include its canvas and module. The current homepage includes neither. Opted-in
pages draw a single static source under reduced motion, pause ongoing frames
offscreen or in a hidden document, and handle motion-preference changes; see
[`animations.md`](../design/animations.md). These behavior checks do not imply a
measured homepage performance change.

## Offline and cache contracts

The service worker installs only the small homepage shell, shared scripts, CSS,
homepage stylesheet, favicon, and manifest. It downloads complete shell responses in parallel under
the same bounded transfer helper used at runtime. Every response must succeed
and stay on the same origin before shell writes begin. The new worker activates
only after every shell write succeeds; a failed or stalled installation leaves
the prior worker active.

| Budget | Contract |
| --- | --- |
| Shell payload | Less than 320 KiB of raw source bytes, enforced by the focused test |
| Network headers | At most 5 seconds |
| Complete decoded body | A separate 25 seconds after headers; at most 30 seconds combined |
| Transfer buffering | At most 16 MiB of decoded bytes, including streams without Content-Length |
| Runtime storage | At most 48 entries, each at most 2 MiB of decoded bytes |

Documents and public data use network-first retrieval with a successful cached
copy as fallback. Static assets use a cached copy immediately while refreshing
in background. Fetch-event `waitUntil` owns that refresh and its cache writes.
HTTP error responses, partial responses, and `Cache-Control: no-store` responses
never enter the runtime cache. Failed reads/writes do not invalidate a successful
network response. An uncached offline document receives explanatory HTML with
status 503; an uncached JSON request receives JSON with status 503.

PDFs, document archives, audio/video downloads, cross-origin requests, and Range
requests bypass the worker cache. Full catalogs, source PDFs, and gallery detail
data are not installation downloads. Successful visited content survives shell
updates until entry eviction or browser storage reclamation; offline availability
is therefore a convenience, not a durable archive guarantee.

Bump `CACHE_NAME` when changing shell assets or worker behavior. Activation
removes old caches owned by this worker while preserving its bounded runtime
cache and unrelated applications' caches. Keep advertised source downloads
independent of browser caching and the Pages projection policy.

## Declared browser and Lighthouse checks

Run the focused acceptance checks with the optional browser runtime installed:

```bash
uv sync --extra browser-qa
uv run playwright install chromium
uv run --extra browser-qa python3 -m pytest \
  code/tests/test_service_worker.py \
  code/tests/test_rendered_frontend.py \
  code/tests/test_rendered_progressive_enhancement.py \
  code/tests/test_home_landing.py \
  code/tests/test_homepage_performance.py \
  code/tests/test_search_bootstrap.py \
  code/tests/test_art_gallery_progressive.py \
  code/tests/test_publications_startup.py \
  code/tests/test_accessibility_refinements.py -q
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py --check
```

The worker checks use Chromium and real HTTP responses for install, offline,
returning visits, successful updates, failed/stalled updates, 404/500 fallback,
delayed headers, dripping bodies, oversized streams, and cache eviction.
Interaction checks cover mobile navigation without JavaScript, native More
disclosures, shortcut focus containment/restoration, progressive full-text
search, and clipboard success/failure behavior. Startup checks observe actual
requests and delayed responses for preview/core/segment transitions, artwork
batches and details, and publication enrichment. Video checks cover every
catalog ID across zoom levels, dense same-day groups, actual target geometry,
contrast, dialog focus, mobile year jumps, UTC date boundaries, forced colors,
reduced motion, and static index access.

The hosted browser job sets `DOCXOLOGY_REQUIRE_BROWSER_QA=1`; missing Chromium,
Playwright, loopback capability, or Lighthouse fails that mandatory job. Local
optional-tool absence produces an explicit skip. A present tool that fails, or
a Lighthouse report missing a required finite score, fails in both contexts.
The npx fallback uses the hosted Lighthouse version, **13.4.1**.

Rendered tests and the Lighthouse ratchet serve the site copy gzip-compressed,
like GitHub Pages (`serve_site(..., compress=False)` gives the identity
transport), and the Lighthouse test asserts that the served copy negotiates gzip
so its scores stay comparable with the published site. Running them locally needs
loopback bind permission and a launchable Chromium.

Lighthouse aspirational scores remain performance 85, accessibility 95, and SEO
95. The gate retains the recorded per-page floors and shared-runner noise policy:
only a below-floor first run triggers two more runs and a median decision. Green
CI establishes the enforced floors, not achievement of all aspirational scores.
`DOCXOLOGY_LIGHTHOUSE_REPORT_DIR` retains each JSON run; JUnit properties record
the per-page scores and aggregation. Keep these diagnostics with the hosted QA
artifacts, and use measured results before ratcheting budgets.

Local tests do not establish live deployment acceptance. Follow
[`live-verification.md`](live-verification.md) and
[`release-integrity.md`](release-integrity.md) to bind published routes,
artifacts, and hosted checks to the deployed commit.

The 2026-10-02 accessibility pass obtained 13 passing focused browser checks
with no skips and one local Lighthouse 13.4.1 video-page observation of
87 performance / 100 accessibility / 100 SEO. These describe the tested local
source and machine; they do not establish hosted performance stability, a
published candidate, or human visual sign-off. Preserve earlier dated receipts
and record subsequent hosted/live acceptance separately.
