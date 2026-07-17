# Security posture — danielarifriedman.com

Static GitHub Pages site for a public research profile. No authentication, no server-side execution, no user-submitted content stored on-site.

## Scope

| Asset | Exposure |
| --- | --- |
| HTML/CSS/JS | Public read-only |
| `data/*.json`, `search-index.json` | Intentional public exports |
| Client-side search / publications filters | Browser-only; no backend |
| Fonts | Same-origin/system fallbacks; no runtime font provider |
| Outbound links | DOI, Scholar, GitHub, social profiles |

## Responsible disclosure

RFC 9116 `security.txt` is published at both [`/.well-known/security.txt`](../../.well-known/security.txt) (canonical) and [`/security.txt`](../../security.txt) (root mirror) — contact `Daniel@ActiveInference.Institute`, policy via GitHub issue chooser. Both carry a `Canary:` pointer to `/canary.txt`; keep `Expires:` aligned to the quarterly canary cadence. An `Encryption:` field is deliberately omitted until a real PGP public key is published at `/.well-known/pgp-key.txt` — add the field back only once that file actually exists, so the RFC 9116 metadata never points to a dead reference.

## Warrant canary

A warrant canary (`canary.txt`, dead-man's-switch, quarterly re-sign) affirms no secret legal process / duress / state compulsion. **It is a personal attestation: only the operator fills the live freshness anchors and PGP-clearsigns it** — it is published only when signed (an unsigned canary is intentionally withheld). The current `canary.txt` has its freshness anchors filled in but is **not yet PGP-signed** (fingerprint and signature block are still placeholders); do not treat it as a valid attestation until the operator clearsigns it. The `Encryption:` field in `security.txt` should be added once `.well-known/pgp-key.txt` lands.

## Client-side XSS

Search and publications UIs build HTML from `search-index.json` / `data/works.json`. All dynamic text passes through `esc()` in [`js/search-utils.js`](../../js/search-utils.js) and [`js/publications.js`](../../js/publications.js). Prefer keeping escape logic centralized; do not add unescaped `innerHTML` from index data.

## Content Security Policy

A CSP meta tag is deployed on all indexable HTML pages:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data: https:; connect-src 'self'; frame-src https://www.youtube-nocookie.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';">
```

`script-src 'self'` blocks all inline event handlers (`onclick=`, `onchange=`, etc.) and executable inline scripts. JSON-LD remains inline because it is data, not executable JavaScript. All event wiring goes through `addEventListener` in the external JS files (`js/interactive.js`, `js/tts-controls.js`, `js/menu-esc.js`, `js/publications.js`, plus the per-page modules `js/art-gallery.js`, `js/videos-page.js`, `js/search-page.js`, `js/repo-inventory.js`, `js/index-page.js`). The `style-src 'unsafe-inline'` exception is needed for per-page `<style>` blocks and inline display rules. `frame-src` permits only privacy-preserving YouTube embeds.

**History (2026-07-15):** the original CSP rollout shipped while art.html, videos.html, search.html, repositories.html, repositories-forks.html, and index.html still carried inline `<script>` blocks, and while nine pages used the inline `onload="this.media='all'"` font trick — the CSP silently disabled all of them (the /art gallery rendered zero artworks). Every inline script is now externalized; font media-swap runs CSP-safely from `js/interactive.js` via `data-media-swap`. Any new page-level JS must ship as an external file under `js/` — an inline `<script>` will be silently blocked in production.

The `code/orchestrators/deploy_seo_security.py` script idempotently adds or normalizes the CSP/referrer meta tags (plus `rel="me"` and `hreflang` links) across public HTML pages. GitHub Pages does not expose a project-level mechanism for custom response headers, so these meta policies are the strongest repository-controlled enforcement layer. The `code/orchestrators/migrate_inline_handlers.py` script converts inline `on*` event handlers to `data-*` attributes that `interactive.js` wires up via `addEventListener`.

## Supply chain

- No npm runtime on the live site today (vanilla JS + static assets).
- If bundling React artifacts under `code/artifacts/`, pin dependencies and run `npm audit` before copying bundles to `js/`.
- The site uses system font fallbacks and carries no runtime Google Fonts dependency.

## External links

Use `rel="noopener"` (and `noreferrer` when appropriate) on `target="_blank"` anchors. Publications and work pages already follow this pattern.

## Secrets

Do not commit API keys, tokens, or private paths. Public JSON exports must not embed credentials.

## Assessment report

See [`reports/web_assessment_2026-05-26.md`](../../reports/web_assessment_2026-05-26.md) for the 2026-05-26 static review summary.
