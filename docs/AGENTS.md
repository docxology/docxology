# AGENTS.md — `docs/`

Reserved for repository-level documentation beyond the `pages/` hub (architecture notes, runbooks, migration logs).

See root [AGENTS.md](../AGENTS.md) for site/SEO, teaching-line alignment (`index.html`, `pages/PROFILE.md`, `README` Educator bullet), and maintenance log. The [pages/README](../pages/README.md) hub lists **108** paper folders under `papers/`. Add long-form architecture or runbooks here when they outgrow the root index.

## Bibliography vs paper folders

- [pages/BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) is the **115-row** unified table (works); the **Docs** column links to a folder under [papers/](../papers/) only when one exists.
- [papers/](../papers/) has **108** per-work folders (README / AGENTS / SKILL); rows without a folder (e.g. some YouTube series or Udemy courses) have no duplicate in-tree index row beyond BIBLIOGRAPHY.
- After table **adds or reorders**, run [`papers/sync_publications_html.py`](../papers/sync_publications_html.py) with `--apply` so [publications.html](../publications.html) **PUBS** and JSON-LD **mainEntity** stay in table order and length.
- [`papers/biblio_table.py`](../papers/biblio_table.py) is the shared eight-column parser used by `sync_publications_html` and [`papers/regenerate_docs.py`](../papers/regenerate_docs.py).

## Generated discovery layer

- Run [`code/orchestrators/export_bibliography.py`](../code/orchestrators/export_bibliography.py) after bibliography edits to refresh BibTeX, CSL JSON, RIS, and `data/works.json`.
- Run [`code/orchestrators/export_agent_data.py`](../code/orchestrators/export_agent_data.py) after software or claim-ledger edits.
- Run [`code/orchestrators/build_domain_pages.py`](../code/orchestrators/build_domain_pages.py) after bibliography/software exports change.
- Run [`code/orchestrators/build_work_pages.py`](../code/orchestrators/build_work_pages.py) after `data/works.json` changes.
- Run [`code/orchestrators/build_evidence_page.py`](../code/orchestrators/build_evidence_page.py) after `data/claims.json` changes.
- Run [`code/orchestrators/build_catalog.py`](../code/orchestrators/build_catalog.py) after `data/*.json` exports change.
- Run [`code/orchestrators/build_search_index.py`](../code/orchestrators/build_search_index.py), [`code/orchestrators/generate_feed.py`](../code/orchestrators/generate_feed.py), and [`code/orchestrators/build_sitemap.py`](../code/orchestrators/build_sitemap.py) after public-page or export changes.
- Run [`code/orchestrators/build_reconciliation_report.py`](../code/orchestrators/build_reconciliation_report.py) after public-source snapshots or curated counts change.
- Run [`code/orchestrators/build_generated_manifest.py`](../code/orchestrators/build_generated_manifest.py) when generated-artifact lists or commands change.
- Run [`code/orchestrators/check_external_links.py`](../code/orchestrators/check_external_links.py) to refresh the scoped external-link report; 403/429 entries may be bot protection rather than broken sources.
- Run [`code/orchestrators/accessibility_audit.py`](../code/orchestrators/accessibility_audit.py) and [`code/orchestrators/visual_qa.py`](../code/orchestrators/visual_qa.py) after significant frontend changes.
- Run [`code/orchestrators/validate_repo.py`](../code/orchestrators/validate_repo.py) before declaring the repo healthy.

## Canonical URLs and reports

- [docs/REDIRECTS.md](REDIRECTS.md) records canonical URL and redirect-stub rules for GitHub Pages.
- [CHANGELOG.md](../CHANGELOG.md) summarizes public-index and generated-site changes.
- [reports/](../reports/) stores source snapshots, reconciliation outputs, external-link reports, accessibility results, and Playwright visual QA screenshots.
- [GENERATED.md](../GENERATED.md) and [`data/generated-manifest.json`](../data/generated-manifest.json) document generated outputs and rebuild commands.
