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

[`search-utils.js`](../../js/search-utils.js) shares one cached core-index
request across consumers. Header autocomplete uses
[`search-index-core.json`](../../search-index-core.json). The dedicated search
page loads work/video detail segments on a nonempty query; a work-only filter
loads only the work segment. Deep text matches retain the same AND, word-boundary,
and symbol-search rules. Failed or malformed segments expose an incomplete-search
status and a retry, rather than silently claiming a complete search.

[`search-index.json`](../../search-index.json) remains the complete export for
agents and offline tooling. Generate all projections together with
`code/orchestrators/build_search_index.py`; do not hand-edit them.

The search page reserves the type-filter row before the core arrives. Its
horizontal strip keeps the result area in place at narrow widths, and keyboard
focus scrolls later options into view. Keep the search panel's grid column
bounded with `minmax(0, 1fr)` so long labels cannot widen the document.

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
  code/tests/test_home_landing.py -q
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py
uv run --extra browser-qa python3 code/orchestrators/browser_qa.py --check
```

The worker checks use Chromium and real HTTP responses for install, offline,
returning visits, successful updates, failed/stalled updates, 404/500 fallback,
delayed headers, dripping bodies, oversized streams, and cache eviction.
Interaction checks cover mobile navigation without JavaScript, native More
disclosures, shortcut focus containment/restoration, progressive full-text
search, and clipboard success/failure behavior.

The hosted browser job sets `DOCXOLOGY_REQUIRE_BROWSER_QA=1`; missing Chromium,
Playwright, loopback capability, or Lighthouse fails that mandatory job. Local
optional-tool absence produces an explicit skip. A present tool that fails, or
a Lighthouse report missing a required finite score, fails in both contexts.
The npx fallback uses the hosted Lighthouse version, **13.4.1**.

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
