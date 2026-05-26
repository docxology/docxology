# Security posture — danielarifriedman.com

Static GitHub Pages site for a public research profile. No authentication, no server-side execution, no user-submitted content stored on-site.

## Scope

| Asset | Exposure |
| --- | --- |
| HTML/CSS/JS | Public read-only |
| `data/*.json`, `search-index.json` | Intentional public exports |
| Client-side search / publications filters | Browser-only; no backend |
| Third-party fonts | Google Fonts (Playfair Display on some pages) |
| Outbound links | DOI, Scholar, GitHub, social profiles |

## Responsible disclosure

See [`.well-known/security.txt`](../.well-known/security.txt) — contact `Daniel@ActiveInference.Institute`, policy via GitHub issue chooser.

## Client-side XSS

Search and publications UIs build HTML from `search-index.json` / `data/works.json`. All dynamic text passes through `esc()` in [`js/search-utils.js`](../js/search-utils.js) and [`js/publications.js`](../js/publications.js). Prefer keeping escape logic centralized; do not add unescaped `innerHTML` from index data.

## Content Security Policy

GitHub Pages does not expose custom response headers. Optional hardening via meta CSP (test before deploy):

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';">
```

Adjust `connect-src` if adding analytics. Inline handlers (`onclick=`) on legacy pages may require `'unsafe-inline'` in `script-src` until migrated to `addEventListener`.

## Supply chain

- No npm runtime on the live site today (vanilla JS + static assets).
- If bundling React artifacts under `code/artifacts/`, pin dependencies and run `npm audit` before copying bundles to `js/`.
- Self-hosting font files removes `fonts.googleapis.com` dependency (future improvement).

## External links

Use `rel="noopener"` (and `noreferrer` when appropriate) on `target="_blank"` anchors. Publications and work pages already follow this pattern.

## Secrets

Do not commit API keys, tokens, or private paths. Public JSON exports must not embed credentials.

## Assessment report

See [`reports/web_assessment_2026-05-26.md`](../reports/web_assessment_2026-05-26.md) for the 2026-05-26 static review summary.
