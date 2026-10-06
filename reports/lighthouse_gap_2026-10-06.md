# Lighthouse performance gap — art and publications (2026-10-06)

Scope: the two pages below the aspirational performance 85 in the CI Lighthouse
ratchet (`code/tests/test_lighthouse_budgets.py`). Thresholds were not changed.
All runs use Lighthouse 13.4.1 with the test's flags (default mobile emulation
and simulated throttling, `--headless=new`).

## Measurements

| Source | `art.html` | `publications.html` |
|--------|-----------:|--------------------:|
| CI artifact `lighthouse-a08e455d…` (Actions run 37344225777, 2026-10-05) | 75 (FCP 1.7 s, LCP 4.5 s, TBT 360 ms) | 82 (FCP 3.0 s, LCP 3.6 s, TBT 160 ms) |
| Operator-reported, 2026-10-05 | 76 | 83 |
| This machine, uncompressed `http.server` copy (the CI fixture's server type), two runs | 80, 84 | 76, 79 |
| This machine, production `https://danielarifriedman.com/`, two runs | 100, 99 | 99, 99 |

Both columns on this machine use the same Lighthouse binary and flags, so the
difference between the last two rows isolates the serving conditions. Its CPU is
faster than a CI runner, which is why total blocking time is 0–20 ms locally and
160–360 ms in CI.

## Cause

- The CI fixture (`code/tools/rendered_site_fixture.py`) serves files with
  `http.server.SimpleHTTPRequestHandler`, which never compresses. GitHub Pages
  serves gzip. Measured on 2026-10-06:

  | File | Raw bytes (CI fixture) | gzip bytes (production) |
  |------|-----------------------:|------------------------:|
  | `publications.html` | 348,745 | 41,793 |
  | `data/artworks-index.json` | 472,657 | 78,191 |
  | `style.css` | 75,190 | 16,522 |
  | `art.html` | 46,911 | 12,200 |
  | `js/art-gallery.js` | 21,135 | 6,500 |

- Both pages' LCP element is text (`art.html`: the gallery introduction
  paragraph; `publications.html`: a section heading or introduction), which
  paints with the first frame. Lighthouse's simulated throttling still charges
  LCP for bandwidth shared with requests that start before it: the render-blocking
  stylesheet and scripts, the four Flickr thumbnails visible in the first
  viewport (lazy-loaded, but in view; about 370 KB) and the data fetch (`data/artworks-index.json` or `data/works.json`).
  Uncompressed, those bytes cost seconds on the simulated slow-4G link.
- CI's blocking time is real on slower processors: `js/art-gallery.js` runs a
  411 ms task when it renders the gallery from the index, and `js/publications.js`
  a 214 ms task.

## Rejected experiment

Deferring the two data fetches until after `load` and an idle callback, at low
fetch priority, measured 98, 80 and 84 (`art.html`) and 76, 84 and 85
(`publications.html`) on the uncompressed copy, no clear change. On a local
server `load` fires before the observed LCP (49 ms against 70 ms in one trace),
so the simulation still counts the fetch, while a longer delay would only
postpone search and filtering for visitors. The change was not adopted.

## Options

1. Serve the Lighthouse fixture with gzip, as GitHub Pages does, so the ratchet
   measures what visitors receive. Thresholds stay unchanged; the measured score
   rises without any site change, so this is a measurement-policy decision.
2. Reduce the bytes and main-thread work the uncompressed fixture counts: split
   page-specific rules out of `style.css` (thumbnails are already lazy-loaded),
   and render the gallery and publication table in yielded chunks to remove the
   long tasks. This also helps slow devices in production, where only the long
   tasks still matter.

## Outcome (2026-10-06)

Option 1 and the yielded-chunk half of Option 2 were taken; splitting
page-specific rules out of `style.css` was not done (after compression
`style.css` is about 16 KB, so it no longer moves the score). The rendered
fixture now serves the site copy gzip-compressed like GitHub Pages (text types,
SVG and ICO at zlib level 5, `Vary: Accept-Encoding` on every response;
`serve_site(..., compress=False)` restores the identity transport), and the
startup work in `js/art-gallery.js` and `js/publications.js` runs as several
short tasks. Thresholds, floors and `BASELINE` are unchanged.
`test_lighthouse_budgets.py` now checks one asset of each type the pages load
(an HTML page, `style.css`, a `js/*.js` file and a `data/*.json` file): each
must come back with `Content-Encoding: gzip` and `Accept-Encoding` among the
`Vary` tokens, and a shortfall fails with a parity message naming the asset. The
check itself is tested without a socket against both the compressing and the
identity handler, so the measurement cannot drift from production unnoticed.

Local Lighthouse 13.4.1 with the test's flags (`--headless=new --no-sandbox`,
default mobile emulation and simulated throttling), served by the new fixture.
Three runs per cell, median shown with the individual scores; "12x CPU" adds
`--throttling.cpuSlowdownMultiplier=12` to approximate a slower runner. Machine:
macOS 27.0.1 on arm64, HeadlessChrome 154. Accessibility and SEO were 100 in all
36 runs.

| Page | CPU | Fixture | Performance | TBT (median) |
|------|-----|---------|------------:|-------------:|
| `art.html` | default | gzip, new scripts | 99 (99, 100, 99) | 0 ms |
| `art.html` | default | identity (`compress=False`) | 83 (84, 83, 80) | 0 ms |
| `art.html` | default | gzip, previous scripts | 100 (98, 100, 100) | 8 ms |
| `art.html` | 12x | gzip, new scripts | 99 (99, 99, 99) | 0 ms |
| `art.html` | 12x | identity (`compress=False`) | 83 (83, 99, 83) | 0 ms |
| `art.html` | 12x | gzip, previous scripts | 100 (100, 100, 100) | 67 ms |
| `publications.html` | default | gzip, new scripts | 100 (100, 100, 100) | 0 ms |
| `publications.html` | default | identity (`compress=False`) | 79 (79, 79, 79) | 0 ms |
| `publications.html` | default | gzip, previous scripts | 100 (100, 100, 100) | 0 ms |
| `publications.html` | 12x | gzip, new scripts | 100 (100, 100, 100) | 0 ms |
| `publications.html` | 12x | identity (`compress=False`) | 85 (79, 85, 85) | 8 ms |
| `publications.html` | 12x | gzip, previous scripts | 100 (100, 100, 100) | 0 ms |

Reading the table:

- Compression accounts for the score change: the identity fixture reproduces the
  pre-change local numbers (medians of 83 for art and 79 to 85 for publications;
  the Measurements table above recorded 80 and 84 for art and 76 and 79 for
  publications), the gzip fixture reproduces the production numbers (98–100).
  Transfer weight falls from 1.14 MB to 0.59 MB for `art.html` and from 0.77 MB
  to 0.20 MB for `publications.html`.
- The identity rows are the noisy ones, and their outliers belong in the
  reading. Across the six identity runs per page, `art.html` scored 80, 83, 83,
  83, 84 and 99, and `publications.html` scored 79, 79, 79, 79, 85 and 85. The
  12x CPU identity runs were 83, 99, 83 for art and 79, 85, 85 for publications,
  so the median hides one run that landed at 99 on art and two at 85 on
  publications. Run-to-run spread on this machine reaches about 20 points (art
  identity, 80 to 99). The gzip rows stayed within 98–100 in every run.
- The script change removes the only measurable blocking time. On `art.html` the
  previous scripts blocked for 7–8 ms (default CPU) and 66–68 ms (12x CPU) in the
  matrix, and 253 ms in one extra 12x run; every run with the new scripts
  reported 0 ms. `publications.html` showed no blocking time before or after.
- Score differences of one point between the new and previous scripts on
  `art.html` are noise: with TBT at 0 the remaining spread comes from LCP, which
  moved between about 1.2 s and 2.3 s from run to run on both script versions
  (it depends on the remote Flickr thumbnails).
- These are one machine's results with simulated CPU slowdown, not CI numbers;
  no CI numbers are claimed. The CI artifact above (75 and 82, TBT 360 and
  160 ms) predates this change; the first hosted run after it is the acceptance
  measurement, and its `lighthouse-<sha>` artifact should be read next to the
  unchanged floors.

Verification before measuring: the browser QA list from
`.github/workflows/browser-qa.yml` (without `test_lighthouse_budgets.py`, plus
`test_rendered_fixture_compression.py`, `test_rendered_fixture_contract.py`,
`test_art_gallery_hydrate.py` and `test_lighthouse_gate_contract.py`) passed 189
tests, none skipped, on Python 3.12.13 with Playwright 1.62.0 and
`DOCXOLOGY_REQUIRE_BROWSER_QA=1`. The new startup paths are covered by committed
tests: `art.html` rejects an index of 150 records with one invalid record at
position 120 without publishing any of it (three failure kinds, plus a valid
control), controls changed while the index fetch is held, or while the loader is
parked after publishing, decide the final grid, and both `art.html` and
`publications.html` hydrate with `scheduler.yield` deleted (the `setTimeout(0)`
fallback) and a clean console.

## CI confirmation (2026-10-06)

The first CI run with the gzip fixture and the yielding startups
(`lighthouse-8d4c7c17…` artifact, one run per page) scored performance 95 on
`art.html` (LCP 1.2 s, TBT 240 ms) and 99 on `publications.html` (LCP 1.4 s,
TBT 130 ms), against 75 and 82 on `a08e455d`. Every ratchet page scored 95–100
for performance, 96–100 for accessibility and 100 for SEO. Thresholds are
unchanged.
