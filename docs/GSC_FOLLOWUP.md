# Google Search Console — manual follow-up runbook

Site-side SEO fixes are live on [danielarifriedman.com](https://danielarifriedman.com/) (sitemap ~157 URLs, `works/` canonicals, open crawl, `exports.html` hub). **IndexNow does not notify Google.** These steps require a signed-in browser with owner or full-user access to the GSC property.

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
   - [sitemap.xml](https://danielarifriedman.com/sitemap.xml) — ~157 URLs, no `/papers/` paths
   - [robots.txt](https://danielarifriedman.com/robots.txt) — `Allow: /` only

---

## Step 1 — Resubmit the sitemap

**Why:** Google should discover the slimmed sitemap (was ~309 URLs; `papers/` removed).

1. Open [Sitemaps](https://search.google.com/search-console/sitemaps?resource_id=https://danielarifriedman.com/).
2. Under **Add a new sitemap**, enter `sitemap.xml` and click **Submit**.
3. If already listed, confirm **Last read** updates over the next few days (resubmit is fine).

**Success:** Status **Success**; discovered URLs trend toward ~157.

---

## Step 2 — Request indexing (6 priority hubs)

Use [URL Inspection](https://search.google.com/search-console/inspect?resource_id=https://danielarifriedman.com/) for each URL:

| URL |
|-----|
| https://danielarifriedman.com/ |
| https://danielarifriedman.com/exports.html |
| https://danielarifriedman.com/catalog.html |
| https://danielarifriedman.com/cite-verify.html |
| https://danielarifriedman.com/discovery.html |
| https://danielarifriedman.com/publications.html |

Per URL: paste URL → Enter → **Request indexing** (daily quota applies; spread across days if needed).

---

## Step 3 — Validate fixes (3 issue buckets)

Open [Page indexing](https://search.google.com/search-console/index?resource_id=https://danielarifriedman.com/) → **Why pages aren’t indexed**.

### 3a — Page with redirect

Fixed on site: `about.html`, `blog/`, `meditations.html`, `research.html`, `nft.html` → `art.html` use `noindex, follow` + canonical away.

Click **Page with redirect** → **Validate fix**.

### 3b — Alternate page with proper canonical

Fixed: all `papers/{folder}/` are `noindex, follow` with canonical → `works/{citation_key}.html`; JSON-LD removed from paper pages.

Click **Alternate page with proper canonical** → **Validate fix**.

### 3c — Not found (404)

Fixed: `nft.html` and `blog/winged-snowflake-2021/` stubs; art dead links repaired.

Click **Not found (404)** → **Validate fix**.

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
| Day 1 | Sitemap submitted; hub URLs requested |
| Days 3–7 | Check **Validate fix** status on three buckets |
| Weekly | [Page indexing](https://search.google.com/search-console/index?resource_id=https://danielarifriedman.com/) totals |
| ~2 weeks | Re-inspect homepage + `publications.html` if not indexed |

Meaningful count changes often take **1–4 weeks**.

---

## Checklist

```text
[ ] Signed into GSC for https://danielarifriedman.com/
[ ] Preflight passed: uv run python3 code/orchestrators/gsc_followup_preflight.py
[ ] Submitted sitemap.xml
[ ] Requested indexing: /, exports.html, catalog.html, cite-verify.html, discovery.html, publications.html
[ ] Validate fix: Page with redirect
[ ] Validate fix: Alternate page with proper canonical
[ ] Validate fix: Not found (404)
[ ] Calendar reminder: recheck Page indexing in 7 days
```

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Validate fix fails on redirects | Inspect sample URL; confirm 200 + `noindex` or valid redirect target |
| Alternate canonical persists | Re-request indexing on canonical `works/` page; wait for recrawl |
| Request indexing greyed out | Daily quota — retry tomorrow; prioritize `/` and `publications.html` |
| Sitemap couldn't fetch | Confirm [sitemap.xml](https://danielarifriedman.com/sitemap.xml) loads; retry |

---

## Related automation (not Google)

```bash
uv run python3 code/orchestrators/submit_indexnow.py   # Bing, Yandex, Naver
uv run python3 code/orchestrators/validate_repo.py      # includes seo_invariants
```

See also [docs/REDIRECTS.md](REDIRECTS.md) and [code/src/seo_invariants.py](../code/src/seo_invariants.py).
