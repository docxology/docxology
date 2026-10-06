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
