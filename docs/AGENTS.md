# AGENTS.md — `docs/`

Reserved for repository-level documentation beyond the `pages/` hub (architecture notes, runbooks, migration logs). For the human-facing navigation index of this folder, see [`README.md`](README.md); docs are grouped under `operations/`, `seo/`, `design/`, `security/`, and `releases/` (architecture notes live in this file).

See root [AGENTS.md](../AGENTS.md) for site/SEO, teaching-line alignment (`index.html`, `pages/PROFILE.md`, `README` Educator bullet), and maintenance log. Indexed paper folders are listed in [`papers/README.md`](../papers/README.md). Use [`operations/publication-sync.md`](operations/publication-sync.md) for GitHub + Zenodo paired publication intake, Zenodo-only backfill, and software-only GitHub record triage. Add long-form architecture or runbooks under the matching topic directory.

**Volatile counts:** do not repeat current totals in this file or root `README.md`. Link to [`reports/current_counts.md`](../reports/current_counts.md), [`data/current-counts.json`](../data/current-counts.json), and the canonical source tables instead.

## Bibliography vs paper folders

- [pages/BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) is the unified works table; the **Docs** column links to a folder under [papers/](../papers/) only when one exists.
- [papers/](../papers/) has per-work folders (README / AGENTS / SKILL) for rows with in-tree documentation; rows without a folder (e.g. some YouTube series or Udemy courses) have no duplicate in-tree index row beyond BIBLIOGRAPHY.
- After table **adds or reorders**, run [`code/orchestrators/sync_publications_html.py`](../code/orchestrators/sync_publications_html.py) with `--apply` so [publications.html](../publications.html) head meta and [`data/publications-ld.json`](../data/publications-ld.json) **mainEntity** stay in table order and length; run [`export_bibliography.py`](../code/orchestrators/export_bibliography.py) for `data/works.json`.
- [`code/src/biblio_table.py`](../code/src/biblio_table.py) is the shared eight-column parser used by `sync_publications_html` and [`code/orchestrators/regenerate_docs.py`](../code/orchestrators/regenerate_docs.py).

## Generated discovery layer

Use [GENERATED.md](../GENERATED.md) and [`data/generated-manifest.json`](../data/generated-manifest.json) as the exhaustive rebuild matrix (orchestrator → output paths). This file records **ordering principles** only:

1. **Bibliography edits** — `export_bibliography.py`, then `code/orchestrators/sync_publications_html.py --apply`, then downstream HTML/JSON that consume `data/works.json` (work pages, domain pages, search index, feed, sitemap). Use `regenerate_all.py` for the authoritative ordered passes rather than constructing a partial chain from this overview.
2. **Software or claims edits** — `sync_software_html.py --apply` after curated software edits, then `export_agent_data.py` and evidence/catalog/search exports that read `data/claims.json` or `data/software.json`.
3. **YouTube metadata edits** — `build_video_pages.py`, then catalog/search/sitemap exports that read `data/videos.json`; run `fetch_video_transcripts.py` first only when refreshing cached caption text.
4. **Resume/CV edits** — `build_resume.py --all` after `resume/source.json`, bibliography/software exports, Scholar snapshot, or claim data changes.
5. **Changelog or manifest changes** — `build_updates_page.py` / `build_generated_manifest.py` when public changelog or generated-artifact lists change.
6. **Freshness and QA** — public-source snapshots, external-link checks, live-site verification, accessibility/visual QA under [`reports/`](../reports/); triage bot-protection (403/429) before rewriting site copy based on checker output alone.
7. **Health gate** — `code/orchestrators/validate_repo.py` before declaring the repo healthy; it includes publication-skill coverage/frontmatter checks through `code/orchestrators/audit_publication_skills.py --check`.
8. **Interactive layer rebuild** — after updating shared or page-specific JavaScript, change its cache token at the authoritative source (`code/src/site_nav.py`, templates, and hand-authored pages), regenerate all generated pages (`regenerate_all.py`), and update the worker shell/cache version when those assets change. Read current tokens from source rather than copying a dated value from documentation. CSP meta tag (`script-src 'self'`) blocks inline handlers — use `code/orchestrators/deploy_seo_security.py` to add CSP/rel-me/hreflang to new pages, and `code/orchestrators/migrate_inline_handlers.py` to convert any new inline `on*` handlers to `data-*` attributes. Run actual browser behavior checks as described in [`operations/site-runtime.md`](operations/site-runtime.md).
9. **Landing** — `docs/operations/settle.md` (`code/orchestrators/settle.py`) classifies the dirty paths, runs the tiered battery, and splits payload/control-tail commits.

## Architecture and manuscript boundaries

- [`operations/development.md`](operations/development.md) maps the static site, thin command entry points, shared modules, configuration, and source authority. Keep reusable policy in shared code and the ordered plan; documentation should link that authority instead of introducing a second configuration layer.
- [`manuscript/`](manuscript/README.md) documents the repository system itself. It is distinct from archived publication text under `papers/`.
- `uv run python3 code/orchestrators/validate_manuscript.py` checks manuscript structure, config/path binding, citations, tokens, and local references. It does not render a document or attest scientific validity, source extraction completeness, licensing, or publication readiness.
- See [`operations/accessibility-qa.md`](operations/accessibility-qa.md) for capture and explicit visual-review records. Screenshot generation, automated browser assertions, and human visual approval are separate evidence.

## Canonical URLs and reports

- [docs/seo/canonical-policy.md](seo/canonical-policy.md) records canonical URL, redirect-stub, and permanent-work-URL rules for GitHub Pages.
- [docs/seo/gsc-followup.md](seo/gsc-followup.md) — manual Google Search Console runbook after SEO remediation; preflight via `code/orchestrators/gsc_followup_preflight.py`.
- [CHANGELOG.md](../CHANGELOG.md) summarizes public-index and generated-site changes.
- [reports/](../reports/) stores source snapshots, reconciliation outputs, external-link reports, accessibility results, and Playwright visual QA screenshots.
