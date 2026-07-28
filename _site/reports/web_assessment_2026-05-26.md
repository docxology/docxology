# Web assessment — danielarifriedman.com

Date: 2026-05-26  
Scope: Authorized defensive review of the public static GitHub Pages profile (principal-owned).  
Method: UnderstandApplication + CreateThreatModel (WebAssessment workflow), codebase review, existing CI reports.

## Application summary

| Field | Value |
| --- | --- |
| Purpose | Public research/software bibliography, evidence ledger, discovery exports |
| Users | Anonymous readers, citation agents, search engines |
| Auth | None |
| Data stores | Static JSON under `/data/`, generated HTML |
| Dynamic behavior | Client-side search (`search.html`), publications filter (`publications.html` + `data/works.json`) |
| Hosting | GitHub Pages, apex `danielarifriedman.com` |

## Attack surface

- **Entry points:** All public HTML/JSON routes listed in `sitemap.xml`
- **Inputs:** Search query string, publication filter controls (client-only)
- **Outputs:** Rendered DOM from JSON indexes
- **Third party:** Google Fonts, external DOI/scholar/social URLs
- **Disclosure:** `/.well-known/security.txt` present (expires 2027-05-13)

## Threat model (prioritized)

| ID | Threat | Risk | Status / mitigation |
| --- | --- | --- | --- |
| T1 | DOM XSS via search/publications rendering | Medium | Centralized `esc()` in `js/search-utils.js` + `js/publications.js`; avoid new unescaped templates |
| T2 | Supply chain (CDN fonts, future JS bundles) | Low–Med | Document CSP in `docs/SECURITY.md`; pin npm if React artifacts added |
| T3 | Misleading public metrics (count drift) | Low (integrity) | `code/src/count_consistency.py` + `validate_repo.py` gate |
| T4 | Sensitive data in public JSON | Low | Exports are intentional; no secrets in repo |
| T5 | Clickjacking / missing security headers | Low | GH Pages header limits; document CSP meta option |
| T6 | Broken outbound links / stale claims | Low | `check_external_links.py`, evidence ledger + reconciliation reports |

## Existing automated checks (2026-05-26 baseline)

| Check | Result |
| --- | --- |
| `validate_repo.py` | Pass after count-consistency gate |
| `accessibility_static` report | 20/20 passing (prior snapshot) |
| `browser_smoke` report | 8/8 passing (prior snapshot) |
| `live_site_verification` | 12/12 passing (prior snapshot; may lag deploy) |
| External links | Scoped report under `reports/`; triage 403/429 as bot protection |

## Recommendations implemented this pass

1. Publications catalog loads from canonical `data/works.json` (removes duplicate inline array).
2. Count drift validation across `llms.txt`, README, publications title, `works.json`.
3. `docs/SECURITY.md` documents CSP, XSS, and disclosure paths.
4. Search page uses shared escape helper script.

## Out of scope

Active exploitation, subdomain enumeration, or third-party service pentesting without expanded written authorization.

## Re-test after deploy

```bash
python3 code/orchestrators/validate_repo.py
python3 code/orchestrators/browser_smoke.py --apply   # if Playwright available
python3 code/orchestrators/verify_live_site.py --apply
```
