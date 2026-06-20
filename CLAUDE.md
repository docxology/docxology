# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`docxology/docxology` is the public research, software, citation, and CV index for
Daniel Ari Friedman, published as a **static site at `https://danielarifriedman.com/`**
via GitHub Pages (apex domain set in `CNAME`, no `www`). It is a self-versioned project
with its own remote — commit here, not into the parent `projects` monorepo.

The core mental model: **almost every HTML page and JSON file is a generated artifact
checked into git** so GitHub Pages can serve it statically. You edit a *source*, then run
the matching orchestrator to rebuild the *output*. Hand-editing a generated file is a bug —
it will drift and be overwritten on the next rebuild.

## Source → generated (the cardinal rule)

`GENERATED.md` is the authoritative source→output→command matrix. The primary sources of truth:

| Source of truth | Drives |
| --- | --- |
| `pages/BIBLIOGRAPHY.md` (8-col table, parsed by `code/src/biblio_table.py`) | works.json, exports, `publications.html`, `works/*.html`, domains, search, sitemap, feed |
| `pages/SOFTWARE.md` (parsed by `code/src/software_table.py`) | `software.html`, `data/software*.json`, repo grids |
| `data/scholar-snapshot.json` | every citation count on the site |
| `resume/source.json` | `data/resume.json`, plaintext CVs, `resume/resume.pdf` |
| `CHANGELOG.md` | `updates.html` |
| `code/src/sitemap_policy.py` | `sitemap.xml` URL set + IndexNow promotion list |

Never hard-code volatile totals (work counts, repo counts, citation counts, domain
breakdowns) in hand-authored docs. Link to `reports/current_counts.md` /
`data/current-counts.json` instead. `code/src/count_consistency.py` +
`build_current_counts.py --check` guard drift and run inside `validate_repo.py`.

## Commands

Python tooling is `uv`-only (never bare `pip`). Everything runs from the repo root.

```bash
# Environment (the .venv interpreter path goes stale if the repo is moved — recreate it):
uv venv --python 3.12 && uv pip install -e .

# Tests (CI gate):
uv run pytest code/tests -q
uv run pytest code/tests/test_seo_invariants.py::test_collect_seo_errors_empty_on_repo -q   # single test

# Validate the generated layer (CI gate — run before declaring work done):
uv run python3 code/orchestrators/validate_repo.py
```

`.github/workflows/validate.yml` runs `validate_repo.py` + `pytest` on every push/PR.
Other workflows: `indexnow-on-push.yml`, `freshness.yml`, `live-verify.yml`.

### Rebuild ordering

Outputs depend on upstream outputs, so regenerate in dependency order. After a
`pages/BIBLIOGRAPHY.md` edit:

```bash
python3 code/orchestrators/export_bibliography.py          # → data/works.json + bib/csl/ris
python3 code/orchestrators/sync_publications_html.py --apply
python3 code/orchestrators/build_work_pages.py             # → works/*.html
python3 code/orchestrators/build_domain_pages.py
python3 code/orchestrators/build_search_index.py
python3 code/orchestrators/build_sitemap.py
python3 code/orchestrators/generate_feed.py
uv run python3 code/orchestrators/build_current_counts.py
uv run python3 code/orchestrators/validate_repo.py
```

Software path: `pages/SOFTWARE.md` → `sync_software_html.py --apply` → `export_agent_data.py`.
After editing any HTML head template that changes file size, refresh the size report with
`audit_assets.py` (otherwise `validate_repo` fails on a stale report). Network-dependent
generators (`build_github_inventory.py`, `refresh_public_sources.py`) hit live APIs; their
outputs are committed — patch the output by hand if you only need a small head/meta change
and can't reach the API, then keep the template in sync.

## SEO invariants (enforced by `code/src/seo_invariants.py` via `validate_repo`)

- **Apex canonicals only** — `https://danielarifriedman.com/...`, never `www`, in
  `rel=canonical`, `og:url`, sitemap `loc`, and machine-readable exports.
- **`works/{citation_key}.html` is a permanent URL contract.** The `citation_key` is also
  the BibTeX key external academics may cite; this host has no server-side redirects, so a
  changed key is a 404. Never re-slug an existing work on a title/year edit. `num` is the
  immutable id; gaps from removed works are retired, never renumbered.
  (`test_frozen_work_keys.py` freezes every `num→citation_key`.)
- **`papers/{folder}/index.html`** are `noindex, follow`, canonical to the matching work
  page, and **must not emit JSON-LD**. Redirect stubs (`about.html`, `nft.html`, …) are also
  `noindex, follow`.
- **`sitemap.xml` must equal `sitemap_policy.sitemap_locs()` exactly** and never list
  `/papers/`. `robots.txt` is `Allow: /` with no `Disallow` — crawl discipline is done with
  canonicals + sitemap, not robots blocking.
- **Social meta:** every indexable page with `og:image` must also carry `twitter:card`,
  `og:image:alt`, and `twitter:image:alt`. Generated pages get these from
  `code/src/site_nav.py::social_meta_tags()` or each generator's inline head template;
  the 10 hand-maintained pages get them from `ensure_social_meta.py` (idempotent).
- Work-page meta descriptions are ≤160 rendered chars, word-boundary clipped
  (`site_nav.clip_description`).

After major SEO/sitemap changes, run `gsc_followup_preflight.py` then follow
`docs/seo/gsc-followup.md` in a signed-in browser (no GSC API in the repo).

## Identity invariants

- Wikidata **Q138781444** must be first in the `index.html` Person `sameAs` (not the merged
  duplicate Q85887463). Scholar profile `DXjPFtYAAAAJ`; ORCID `0000-0001-6232-9096`.
- `ActiveInferenceInstitute` on GitHub is a **User** account (`/users/...`, not `/orgs/...`).
- Scholar metrics: only publish a count from a direct (non-cached) fetch; update
  `data/scholar-snapshot.json` (`as_of`, `method`, `history`), run `sync_scholar_metrics.py`,
  then regenerate claims/resume. Never publish above the latest direct-fetch value.

## Where to look

- `AGENTS.md` — agent roles, the full maintenance log, and "Learned User Preferences /
  Workspace Facts" (the operating bible; read it for any non-trivial content change).
- `GENERATED.md` — the exhaustive rebuild matrix. `AGENT_START.md` — task recipes.
- `docs/README.md` — human docs index; `docs/seo/`, `docs/design/`, `docs/operations/`,
  `docs/security/` hold the topic runbooks.
