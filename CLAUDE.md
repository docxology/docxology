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
| `TODO.md` | active unfinished backlog only; completed work stays in `CHANGELOG.md` and dated reports |

Never hard-code volatile totals (work counts, repo counts, citation counts, domain
breakdowns) in hand-authored docs. Link to `reports/current_counts.md` /
`data/current-counts.json` instead. `code/src/count_consistency.py` +
`build_current_counts.py --check` guard drift and run inside `validate_repo.py`.

## Commands

Python tooling is `uv`-only (never bare `pip`). Everything runs from the repo root.

```bash
# Environment (the .venv interpreter path goes stale if the repo is moved — recreate it):
uv sync --python 3.12

# Tests (CI gate):
uv run python3 -m pytest code/tests -q
uv run python3 -m pytest code/tests/test_seo_invariants.py::test_collect_seo_errors_empty_on_repo -q   # single test

# Lint (CI gate):
uv run --group lint ruff check code

# Validate the generated layer (CI gate — run before declaring work done):
uv run python3 code/orchestrators/validate_repo.py

# One-command landing flow (tiered battery + commit split; see docs/operations/settle.md):
uv run --no-sync python3 code/orchestrators/settle.py --tier full --dry-run
```

The release envelope is checked as part of validation: `data/release-integrity.json`
connects source/generator hashes, the bounded Pages manifest, deployment metadata,
and the latest live verification. `data/pages-artifact-manifest.json` documents the
hosted projection and GitHub tree/raw fallbacks for omitted extracted paper images.

## Interactive Layer (added 2026-07-05)

Every indexable page includes the shared interactive modules; page-specific runtimes are declared by the corresponding source page or generator:

| Module | File | Features |
|--------|------|----------|
| **TTS Controls** | `js/tts-controls.js` | Web Speech API read-aloud, floating panel (T key), speed/voice selection, paragraph highlighting, auto-scroll |
| **Interactive** | `js/interactive.js` | Reading progress bar, scroll-to-top button, keyboard shortcuts overlay (? key), section anchor copy-links, search autocomplete (search-index-core.json), image lazy loading, external link safety |
| **Menu Escape** | `js/menu-esc.js` | Closes the mobile navigation with Escape |

`js/nav-toggle.js` is loaded synchronously in pages that include the mobile
toggle. Navigation stays expanded if that small head asset is blocked or
JavaScript is disabled. Search autocomplete uses `search-index-core.json`;
the dedicated search page initially browses the small bootstrap export and
loads deeper segments on demand. See [`docs/operations/site-runtime.md`](docs/operations/site-runtime.md)
for the exact gallery, publications, search, video, and worker contracts.

To verify:
- Press `T` → TTS panel opens
- Press `?` → keyboard shortcuts overlay
- Scroll down → red-gold progress bar fills, `↑` button appears
- Type in search input → autocomplete suggestions from search-index-core.json
- Hover section `h2` heading → `#` anchor link appears (click to copy URL)

Shared styling lives in `style.css`, with homepage overrides in `css/home.css`.
Use the design-system tokens, preserve reduced-motion behavior, and check the
specific component's print/mobile contract rather than assuming every widget
is hidden in every context.

`.github/workflows/validate.yml` runs `validate_repo.py` + `pytest` on every push/PR.
Other workflows: `pages.yml` (Pages deploy on main), `indexnow-on-push.yml`, `freshness.yml`, `live-verify.yml`.

### Rebuild ordering

Outputs depend on upstream outputs, so regenerate in dependency order. The single
dependency-ordered driver for this is `regenerate_all.py` — run it after any
`pages/BIBLIOGRAPHY.md` / `pages/SOFTWARE.md` edit (or any other source change)
instead of invoking individual orchestrators by hand:

```bash
uv run python3 code/orchestrators/regenerate_all.py --validate
```

It is local-only and idempotent (no network freshness steps — those are a deliberate
separate step; see `docs/operations/publication-sync.md`), and ends with the Pages
artifact manifest, then `build_generated_manifest.py` → `build_agent_index.py` →
`build_release_integrity.py` → the final `build_generated_manifest.py` and
`validate_repo.py`.
Inspect the current order directly from the authoritative plan instead of
maintaining a second script list in these instructions:

```bash
uv run python3 code/orchestrators/regenerate_all.py --list
```

The driver and no-write checks share
[`LOCAL_GENERATION_STEPS`](code/src/generation_plan.py).
[`test_generation_plan_docs.py`](code/tests/test_generation_plan_docs.py) checks
the actual read-only plan command and this documented entry point. Use
[`GENERATED.md`](GENERATED.md) for the output matrix and the
[regeneration runbook](docs/operations/regeneration.md) for cache and locking
contracts.

`prune_old_reports.py --apply` is deliberately NOT in the chain: it deletes report
artifacts, and a destructive step has no place in an idempotent rebuild. Run it on its own
when the retention runbook calls for it.

Software path: `pages/SOFTWARE.md` → `sync_software_html.py --apply` → `export_agent_data.py`.
After editing any HTML head template that changes file size, refresh the size report with
`audit_assets.py` (otherwise `validate_repo` fails on a stale report). `build_sitemap.py`
derives each URL's `<lastmod>` from **git commit dates**, so regenerate `sitemap.xml` *after*
committing page changes (a fresh commit bumps every touched file's date) and keep CI on a
full-history checkout (`fetch-depth: 0`) or `build_sitemap.py --check` reports a stale sitemap. Network-dependent
generators (`build_github_inventory.py`, `refresh_public_sources.py`) hit live APIs; their
outputs are committed. Render cached inventory data with `render_github_inventory.py`
when changing its template or presentation. If fresh API data is unavailable,
retain the dated snapshot and its caveat; do not silently replace generated
records with hand-written substitutes.

For interactive-layer changes, run the cached Playwright behavior suite in
`code/orchestrators/browser_qa.py` in addition to `browser_smoke.py`; it covers
no-JavaScript fallbacks, state announcements, focus restoration, responsive
overflow, reduced motion, forced colors, CSP-adjacent console output, and the
YouTube iframe policy.

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
  hand-maintained pages get them from `ensure_social_meta.py` (idempotent).
- Work-page meta descriptions are ≤160 rendered chars, word-boundary clipped
  (`site_nav.clip_description`).

After major SEO/sitemap changes, run `gsc_followup_preflight.py` then follow
`docs/seo/gsc-followup.md` in a signed-in browser (no GSC API in the repo).

## Identity invariants

- Wikidata **Q138781444** must be first in the `index.html` Person `sameAs` (not the merged
  duplicate Q85887463). Scholar profile `DXjPFtYAAAAJ`; ORCID `0000-0001-6232-9096`.
- `ActiveInferenceInstitute` on GitHub is an **Organization** (API `type: Organization`, observed
  2026-10-06; `/users/...` calls remain valid for organizations and `/orgs/...` now resolves too).
  The profile's `updated_at` of 2026-09-22 is consistent with a conversion around then; do not
  state a conversion date as fact.
- Scholar metrics: only publish a count from a direct (non-cached) fetch; record it with
  `code/orchestrators/record_scholar_observation.py` (writes `data/scholar-snapshot.json`
  and its SHA-256-bound receipt together), run `sync_scholar_metrics.py`, then regenerate
  claims/resume. Never publish above the latest direct-fetch value.

## Where to look

- `AGENTS.md` — agent roles and "Learned User Preferences / Workspace Facts" (the
  operating bible; read it for any non-trivial content change). The full maintenance
  log lives at `docs/operations/maintenance-log.md` (which `AGENTS.md` delegates to).
- `GENERATED.md` — the exhaustive rebuild matrix. `AGENT_START.md` — task recipes.
- `docs/README.md` — human docs index; `docs/seo/`, `docs/design/`, `docs/operations/`,
  `docs/security/` hold the topic runbooks.
- `docs/operations/development.md` — architecture, configuration ownership, source
  boundaries, and proportionate validation. `docs/manuscript/README.md` documents
  the repository-methods draft and local `validate_manuscript.py` gate; structural
  acceptance is separate from rendering and external publication readiness.
