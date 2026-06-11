# SEO & Discoverability Audit — danielarifriedman.com

**Date:** 2026-06-10 · **Scope:** full static site (26 root pages, 166 work pages, generators in `code/`) · **Method:** working-tree inspection + live-site verification.

## Verdict

The site is already in the top few percent for an academic portfolio: canonical tags everywhere, a 197-URL sitemap that matches a generator-enforced policy, rich JSON-LD (`Person`, `Organization`, `WebSite` + `SearchAction`, `ProfessionalService`, per-work `ScholarlyArticle` + `BreadcrumbList`), `sameAs` identity graph (ORCID, Scholar, Wikidata, GitHub, ResearchGate), `llms.txt`, RSS, OpenSearch, BibTeX/CSL/RIS exports, IndexNow submission, and SEO invariant tests. There is no structural problem. The findings below are refinements, ordered by impact-to-effort. Almost all are one-line generator fixes, not 166 hand-edits.

---

## High impact

### 1. Work-page meta descriptions are hard-cut mid-word (145 of 166 pages)

`code/orchestrators/build_work_pages.py:269` does `description = description[:155].rstrip()`. This slices at a fixed character count regardless of word boundaries, producing snippets like *"…highlighting methodological weak"*, *"…including leuke"*, *"…evo-de"*. The truncated string then propagates verbatim into `meta description`, `og:description`, and `twitter:description` (lines 276, 288, 295), so Google SERP snippets, Slack/Discord unfurls, and X cards all show a cut-off word.

**Fix:** truncate on a word boundary and add an ellipsis. Replace line 269 with something like:

```python
def _clip(text, limit=155):
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.—-")
    return cut + "…"
description = _clip(description)
```

The full abstract already lives in `works.json` / the JSON-LD `abstract` field, so no data is lost — only the snippet is regenerated. Re-run the work-page builder and the 145 pages fix themselves. Consider adding an invariant to `code/src/seo_invariants.py` asserting no work-page description ends in a partial word (e.g. ends with `…` or sentence punctuation).

### 2. No Twitter/X Card tags on any of the 26 root/section pages

Only the 166 generated work pages emit `twitter:card`. The homepage, `publications.html`, `domains.html`, the five `domain-*.html` pages, `art.html`, `software.html`, `catalog.html`, `videos.html`, `collaborators.html`, etc. — i.e. the **most-shared** pages — have Open Graph tags but **no** `twitter:card`, `twitter:title`, `twitter:description`, or `twitter:image`. X, and several other scrapers, need `twitter:card = summary_large_image` to render the large-image preview; without it they fall back to a small/no-image card.

**Fix:** add the four `twitter:*` tags (mirroring the existing `og:*` values) to the head template(s) for the root pages. Mirror exactly what `build_work_pages.py:293–296` already does. If index/section heads are partly hand-maintained, this is a small per-template edit; add a `seo_invariants` check that every indexable page with `og:image` also has `twitter:card`.

---

## Medium impact

### 3. The 6th research domain has no indexable HTML page

The homepage lists six domains, but only five have `domain-*.html` pages (entomology, active-inference, cognitive-security, art-synergetics, computational). The sixth — **"Genetics & Biomedicine"** — links to `https://danielarifriedman.com/pages/BIBLIOGRAPHY.md#-genetics--biomedical`, i.e. a **raw Markdown file** served by GitHub Pages. Raw `.md` is poor for SEO (served as `text/plain` or downloaded, no `<title>`/meta/JSON-LD, not in the sitemap, no internal-link equity). It's also inconsistent with the other five domain cards.

**Fix:** generate a `domain-biomedicine.html` (or `domain-genetics.html`) via `build_domain_pages.py` matching the other five, add it to the sitemap policy, and point the homepage card at it.

### 4. `og:image:alt` missing site-wide (0 pages)

No page provides alt text for its social-share image. This is a small accessibility + social-preview quality gain (some platforms surface it; it also helps screen readers parsing shared cards).

**Fix:** add one `<meta property="og:image:alt" content="…">` per template (e.g. *"Daniel Ari Friedman — academic portfolio"* on root pages; the work title on work pages).

### 5. `software.html` meta description is 184 characters — will be truncated in SERPs

Over the ~155–160 char ideal, so Google clips it. Tighten to ≤160. (Spot-check the rest: `index.html` is 165 — slightly long; `publications.html` 142 and `domains.html` 109 are fine.)

---

## Low impact / polish

### 6. Duplicate, inconsistent `theme-color`

`index.html` emits `<meta name="theme-color" content="#000000">` **twice** (identical). It's also inconsistent across the site: `manifest.json` and the work pages use `#0c0c0e`. Harmless, but sloppy for a "diligent" codebase. Remove the duplicate and standardize on one value (`#0c0c0e` to match the manifest, or update the manifest to match — pick one).

### 7. Run-on text in extracted content layer

In the text/DOM layer, the homepage concatenates fields without separators — e.g. *"Federated inference and belief sharingNeurosci. & Biobehav. Rev., 202445 cites"* (title+venue+`2024`+`45 cites` run together). CSS separates them visually, but text-extraction crawlers, LLM scrapers, and screen readers see the mashup, and `202445` is ambiguous. Add a separator (space/`·`/punctuation or visually-hidden text) between title, venue, year, and citation count in the publication-card template.

### 8. `meta keywords` is dead weight (optional)

`index.html` carries a `meta keywords` tag. No major engine has used it since ~2009 and it can occasionally signal "over-optimization." Harmless to keep; trivially removable.

### 9. Worth confirming (not verified here)

- **Image `alt` coverage** across the large `art/` gallery (942 drawings) and OG images — strong alt text is meaningful image-search discoverability for an artist. Run `accessibility_audit.py` / `audit_assets.py` and confirm alt coverage.
- **Google Search Console / Bing Webmaster** coverage and "Indexed" counts vs. the 197 sitemap URLs — confirm the work pages are actually being indexed, not just submitted (`gsc_followup_preflight.py` exists for this).

---

## Suggested order of work

1. Fix the truncation in `build_work_pages.py` (one function) → regenerate → 145 pages improve. *(biggest snippet-quality win)*
2. Add `twitter:*` + `og:image:alt` to root-page head templates. *(biggest social-share win)*
3. Generate the missing Genetics/Biomedicine domain page; add to sitemap; relink homepage card.
4. Tighten `software.html`/`index.html` descriptions; de-dupe `theme-color`.
5. Add publication-card field separators; (optional) drop `meta keywords`.
6. Add `seo_invariants` checks for: no mid-word description, `twitter:card` parity with `og:image`, no raw-`.md` links from indexable pages.

All changes flow through the existing generators + test suite, consistent with the repo's build-and-verify model.

---

## Addendum — deep scan + Google Search Console (2026-06-10, round 2)

### Static deep scan (all 196 served HTML files)

Verified clean: **373 JSON-LD blocks, 0 invalid**; full `<img>` alt coverage (the 942-piece art gallery renders alt from `artAlt()` — title + medium + date + tags); no broken internal links (the only `.md` links are the repo's intentional agent-readable source exposure); every indexable page has a unique title except one (see below); `lang`/`viewport`/canonical present on all indexable pages.

Issues found and fixed (via generators):

- **Non-unique fallback meta descriptions.** 17 work pages without an enriched abstract shared a templated `"{type} in {domain} by …"` description (4 Cognitive Security papers identical, etc.). `build_work_pages.py` now builds a per-work fallback that includes the title → 162/165 work descriptions unique.
- **ScholarlyArticle author was a bare cross-document `@id`.** Google can't reliably resolve `{"@id": ".../#person"}` across documents for authorship rich results. Now emits inline `@type`/`name`/`url` alongside the `@id` on all 166 work pages.
- **Paper-folder pages truncated descriptions mid-word** (same bug class, 148 noindex pages affecting social unfurls). `build_paper_pages.py` now uses `clip_description()`.

Flagged for your verification (not auto-changed — accuracy-sensitive):

- **3 work pairs share an identical abstract** because the source `papers/*/README.md` Abstract is the *wrong paper's* text: `2023_ToComment` carries the Digital-Rhetorical/image-memes abstract; `2023_AII_v1` carries the TrustFinder abstract; `2023_HoneyBeeGeneExpression` overlaps the 2015 honey-bee-evolution abstract. These need correct abstracts sourced from the actual papers (DOIs available).
- **Duplicate title:** two CEREBRUM records (`…010`, `…118`) with different Zenodo DOIs share an identical title — a bibliography-curation call (dedupe, or differentiate/version the titles).

### Google Search Console (URL-prefix property `https://danielarifriedman.com/`, last 3 months)

Totals: **74 clicks · 3.25K impressions · 2.3% CTR · avg position 9.**

- **Top queries:** `daniel ari friedman` (16 clicks, pos 3.1), `daniel friedman active inference` (10 clicks, pos 4.2) — brand queries convert well (~34% CTR). The site sits at position ~3 for the author's own name (Scholar/ORCID/AII outrank — normal).
- **High-impression, zero-click queries (the opportunity):** `pppip` (84 impressions, likely P3IF), `"interoception as modeling, allostasis as control"` (50 imp, pos 9.6), `mdkv` (17 imp, pos 6.8 — his software), `art friedman phd stanford` (20 imp). These product/paper terms rank but on the page-1 fringe or page 2.
- **Top pages by impressions:** `repositories.html` **907 imp / 0.2% CTR / pos 11.3**, `videos.html` **620 / 0.5% / 10.7**, `publications.html` **325 / 1.2% / 8.0**. These are impression giants stuck at positions 8–11, where CTR is structurally low — the lever is **position** (depth, internal links, backlinks), not snippet wording.
- **Indexing coverage: 118 indexed, 111 not.** Breakdown: 12 noindex (correct), 3 redirects (correct), 2 alternate-canonical (correct), **43 "Crawled – currently not indexed"** and **50 "Discovered – currently not indexed"** (thin/templated work pages — exactly what the unique-description + enriched-author fixes target), and **1 "Not found (404)"** = `papers/2024_PopulationSearch/`, which is **stale** (crawled 2026-05-24, page published 2026-05-30; now returns 200, noindex, correctly canonicalized) and will clear on re-crawl.

### Recommended next steps (position & indexing — beyond meta tags)

1. **After pushing,** request indexing in GSC for the new `domain-biomedicine.html` and re-submit `sitemap.xml`; this nudges the 50 "discovered, not indexed" pages.
2. **Capture the product-term demand** (`mdkv`, `P3IF`/`pppip`, `ai discovery engine`): give each flagship tool a dedicated, indexable, well-linked landing section rather than only a row inside `repositories.html`/`software.html`.
3. **Correct the 3 mis-attributed abstracts** above — fixes both duplicate content and accuracy.
4. **Earn links** to deepen indexing of the work-page corpus (the 43+50 unindexed are a domain-authority/crawl-priority signal, not a markup defect).
