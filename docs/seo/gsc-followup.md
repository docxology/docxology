# Google Search Console — manual follow-up runbook

Site-side SEO fixes are live on [danielarifriedman.com](https://danielarifriedman.com/) (sitemap includes priority hubs, canonical `works/` pages, per-video `videos/<id>.html` pages, open crawl, and the `exports.html` hub). **IndexNow does not notify Google.** These steps require a signed-in browser with owner or full-user access to the GSC property.

**Property:** [https://danielarifriedman.com/](https://danielarifriedman.com/) (apex, not `www`)

**Preflight (automated):** `uv run python3 code/orchestrators/gsc_followup_preflight.py`

**Time:** ~10–15 minutes once; recheck weekly for 2–4 weeks.

---

## Before you start

1. Sign in at [Google Search Console](https://search.google.com/search-console).
2. Select the **URL prefix** property `https://danielarifriedman.com/` (or domain property for `danielarifriedman.com`).
3. Run preflight locally and fix any failures before opening GSC:
   ```bash
   uv run python3 code/orchestrators/gsc_followup_preflight.py
   ```
4. Sanity checks (also covered by preflight):
   - [sitemap.xml](https://danielarifriedman.com/sitemap.xml) — generated URL count from preflight, no `/papers/` paths
   - [robots.txt](https://danielarifriedman.com/robots.txt) — `Allow: /` only, and lists exactly one `Sitemap:` (`sitemap.xml`)
   - Retired sitemap URLs (Step 1b) return 404 — preflight checks both the local sitemap files and the live status

---

## Step 1 — Resubmit the sitemap

**Why:** Google should discover the slimmed sitemap (`papers/` removed; high-value hubs and work pages retained).

1. Open [Sitemaps](https://search.google.com/search-console/sitemaps?resource_id=https://danielarifriedman.com/).
2. Under **Add a new sitemap**, enter `sitemap.xml` and click **Submit**.
3. If already listed, confirm **Last read** updates over the next few days (resubmit is fine).

**Success:** Status **Success**; discovered URLs trend toward the current sitemap URL count.

---

## Step 1b — Remove the retired image sitemap

**Why:** Search Console may still list `/sitemap-images.xml` as **Couldn't fetch**. That file was deliberately removed on 2026-08-28 (decision recorded in [asset-strategy-adr.md](../operations/asset-strategy-adr.md); its generator is absent from the regeneration chain, pinned by [test_regenerate_all.py](../../code/tests/test_regenerate_all.py)) and the URL correctly returns 404. **Do not recreate or resubmit it.**

1. In [Sitemaps](https://search.google.com/search-console/sitemaps?resource_id=https://danielarifriedman.com/), open the `sitemap-images.xml` row under **Submitted sitemaps**.
2. Remove the sitemap (use the remove action in the row's menu; confirm the exact wording in the signed-in UI).

**Success:** Only `sitemap.xml` remains, with status **Success**.

---

## Step 2 — Request indexing (priority URLs)

Use [URL Inspection](https://search.google.com/search-console/inspect?resource_id=https://danielarifriedman.com/) for each URL:

| URL |
|-----|
| https://danielarifriedman.com/ |
| https://danielarifriedman.com/repositories.html |
| https://danielarifriedman.com/videos.html |
| https://danielarifriedman.com/software.html |
| https://danielarifriedman.com/exports.html |
| https://danielarifriedman.com/catalog.html |
| https://danielarifriedman.com/cite-verify.html |
| https://danielarifriedman.com/discovery.html |
| https://danielarifriedman.com/publications.html |
| https://danielarifriedman.com/works/ |

Per URL: paste URL → Enter → **Request indexing** (daily quota applies; spread across days if needed).

**Do not request indexing** for `noindex` pages (the `videos/` index) or for the redirect stubs listed in Step 3; they are excluded on purpose. For video and work detail pages, request indexing selectively on indexable pages that are in the sitemap (`videos/<id>.html`, `works/<key>.html`), spread across days for the quota.

---

## Step 3 — Review exclusions; validate only real fixes

Open [Page indexing](https://search.google.com/search-console/index?resource_id=https://danielarifriedman.com/) → **Why pages aren’t indexed**.

**Validate fix** is only for a bucket where the site changed **and** the fix is live across **all** affected URLs. Never use it to dismiss an expected exclusion — those pages are excluded by design, so there is nothing to fix.

### Legitimate exclusions (no action)

- **Alternate page with proper canonical** — every `papers/{folder}/` page is `noindex, follow` with a canonical to `works/{citation_key}.html`, and JSON-LD is removed from paper pages. This is intended.
- **Page with redirect** / **Excluded by ‘noindex’ tag** — the legacy redirect stubs (`noindex, follow` plus a canonical pointing away; defined in [redirect_stubs.py](../../code/src/redirect_stubs.py)):
  - `about.html`, `blog/` (index), `meditations.html`, `research.html` canonicalize to the homepage (`https://danielarifriedman.com/`); their meta-refresh targets are the `#about`, `#media`, `#media` and `#research` sections
  - `nft.html` and `blog/winged-snowflake-2021/` canonicalize to `art.html`
  - `agent-verify.html` canonicalizes to `cite-verify.html`
  - `reports.html` canonicalizes to `evidence.html`
- **Excluded by ‘noindex’ tag** — the `videos/` index is `noindex, follow` and not in the sitemap; `videos.html` and the per-video `videos/<id>.html` pages are the indexed surfaces.

### Not found (404)

A **Not found (404)** row is a real problem only if the URL is one the site publishes or links. Fix the page or add a stub, deploy, confirm the sample URLs now return 200 live, and only then click **Validate fix**. 404s for URLs the site never published (external typos, retired sitemap files) need no action.

---

## Step 4 — Large buckets (monitor only)

### Discovered – currently not indexed

Ops JSON/MD URLs removed from sitemap but still crawlable — **not indexed is acceptable**. No bulk **Validate fix**. Count should fall over weeks.

### Crawled – currently not indexed

Spot-check samples; request indexing on high-value `works/*.html` URLs if needed.

---

## Step 5 — Weekly monitoring (weeks 1–4)

| When | Action |
|------|--------|
| Day 1 | Sitemap submitted; retired sitemap removed; hub URLs requested |
| Days 3–7 | Review exclusion buckets against the legitimate-exclusion list; check **Validate fix** status only for fixes actually submitted |
| Weekly | [Page indexing](https://search.google.com/search-console/index?resource_id=https://danielarifriedman.com/) totals; record the Page-indexing filter used (all known pages vs all submitted pages) so weeks compare like with like |
| ~2 weeks | Re-inspect homepage + `publications.html` if not indexed |

Meaningful count changes often take **1–4 weeks**.

---

## Checklist

```text
[ ] Signed into GSC for https://danielarifriedman.com/
[ ] Preflight passed: uv run python3 code/orchestrators/gsc_followup_preflight.py
[ ] Submitted sitemap.xml
[ ] Removed the retired sitemap from GSC Sitemaps: sitemap-images.xml
[ ] Requested indexing: /, repositories.html, videos.html, software.html, exports.html, catalog.html, cite-verify.html, discovery.html, publications.html, works/
[ ] Reviewed exclusions against the legitimate-exclusion list (Validate fix only after a real, live, site-wide fix)
[ ] Calendar reminder: recheck Page indexing in 7 days
```

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| A validation run fails | Inspect a failing sample URL; confirm 200 + `noindex` or a valid canonical target, and that the fix is live for **all** affected URLs, before re-validating. If the URL is a legitimate exclusion, stop — it needs no validation |
| Alternate canonical persists | Expected for `papers/` pages — not an error. For any other page, re-request indexing on the canonical `works/` page and wait for recrawl |
| Request indexing greyed out | Daily quota — retry tomorrow; prioritize `/` and `publications.html` |
| Sitemap couldn't fetch | If it is `sitemap.xml`, confirm [sitemap.xml](https://danielarifriedman.com/sitemap.xml) loads and retry. If it is a retired sitemap (Step 1b), remove it in GSC — do not recreate the file |
| Unfamiliar referring page such as `github.global.ssl.fastly.net/...` | GitHub Pages’ legacy CDN host. Direct requests to it return 404 and the page self-canonicalizes to the apex. No action |

---

## Observation log

Dated Search Console observations (what was read, what was requested, the next recheck) live in `reports/gsc_observations_<date>.md`, not in this runbook. Latest: [gsc_observations_2026-10-05.md](../../reports/gsc_observations_2026-10-05.md).

---

## Related automation (not Google)

```bash
uv run python3 code/orchestrators/submit_indexnow.py   # Bing, Yandex, Naver
uv run python3 code/orchestrators/validate_repo.py      # includes seo_invariants
```

See also [canonical-policy.md](canonical-policy.md) and [code/src/seo_invariants.py](../../code/src/seo_invariants.py).
