# AGENTS.md — `docs/`

Reserved for repository-level documentation beyond the `pages/` hub (architecture notes, runbooks, migration logs).

See root [AGENTS.md](../AGENTS.md) for site/SEO, teaching-line alignment (`index.html`, `pages/PROFILE.md`, `README` Educator bullet), and maintenance log. Indexed paper folders are listed in [`papers/README.md`](../papers/README.md). Add long-form architecture or runbooks here when they outgrow the root index.

**Volatile counts:** before editing totals in this file or root `README.md`, verify [`pages/BIBLIOGRAPHY.md`](../pages/BIBLIOGRAPHY.md) (header/summary/table) and [`papers/README.md`](../papers/README.md) / [`papers/AGENTS.md`](../papers/AGENTS.md)—those surfaces drift easily when only one file is updated.

## Bibliography vs paper folders

- [pages/BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) is the **116-row** unified table (works); the **Docs** column links to a folder under [papers/](../papers/) only when one exists.
- [papers/](../papers/) has **109** per-work folders (README / AGENTS / SKILL); rows without a folder (e.g. some YouTube series or Udemy courses) have no duplicate in-tree index row beyond BIBLIOGRAPHY.
- After table **adds or reorders**, run [`papers/sync_publications_html.py`](../papers/sync_publications_html.py) with `--apply` so [publications.html](../publications.html) head meta and [`data/publications-ld.json`](../data/publications-ld.json) **mainEntity** stay in table order and length; run [`export_bibliography.py`](../code/orchestrators/export_bibliography.py) for `data/works.json`.
- [`papers/biblio_table.py`](../papers/biblio_table.py) is the shared eight-column parser used by `sync_publications_html` and [`papers/regenerate_docs.py`](../papers/regenerate_docs.py).

## Generated discovery layer

Use [GENERATED.md](../GENERATED.md) and [`data/generated-manifest.json`](../data/generated-manifest.json) as the exhaustive rebuild matrix (orchestrator → output paths). This file records **ordering principles** only:

1. **Bibliography edits** — `papers/sync_publications_html.py --apply`, then `export_bibliography.py`, then downstream HTML/JSON that consume `data/works.json` (work pages, domain pages, search index, feed, sitemap).
2. **Software or claims edits** — `export_agent_data.py`, then evidence/catalog/search exports that read `data/claims.json` or `data/software.json`.
3. **Changelog or manifest changes** — `build_updates_page.py` / `build_generated_manifest.py` when public changelog or generated-artifact lists change.
4. **Freshness and QA** — public-source snapshots, external-link checks, live-site verification, accessibility/visual QA under [`reports/`](../reports/); triage bot-protection (403/429) before rewriting copy.
5. **Health gate** — `code/orchestrators/validate_repo.py` before declaring the repo healthy.

## Canonical URLs and reports

- [docs/REDIRECTS.md](REDIRECTS.md) records canonical URL and redirect-stub rules for GitHub Pages.
- [CHANGELOG.md](../CHANGELOG.md) summarizes public-index and generated-site changes.
- [reports/](../reports/) stores source snapshots, reconciliation outputs, external-link reports, accessibility results, and Playwright visual QA screenshots.
