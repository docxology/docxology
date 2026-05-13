# Generated Files

This repository keeps public site pages, citation exports, data indexes, and QA reports as checked-in generated artifacts so GitHub Pages can serve them statically.

| Artifact | Outputs | Sources | Rebuild command |
| --- | --- | --- | --- |
| Bibliography exports | `bibliography.bib`<br>`bibliography.csl.json`<br>`bibliography.ris`<br>`data/works.json` | `pages/BIBLIOGRAPHY.md`<br>`papers/biblio_table.py` | `python3 code/orchestrators/export_bibliography.py` |
| Agent data exports | `data/software.json`<br>`data/people.json`<br>`data/organizations.json`<br>`data/claims.json` | `pages/SOFTWARE.md`<br>`code/orchestrators/export_agent_data.py` | `python3 code/orchestrators/export_agent_data.py` |
| Domain pages | `domains.html`<br>`domain-*.html`<br>`pages/DOMAINS.md` | `data/works.json`<br>`data/software.json`<br>`code/orchestrators/build_domain_pages.py` | `python3 code/orchestrators/build_domain_pages.py` |
| Work pages | `works/*.html`<br>`data/work-enrichment.json` | `data/works.json`<br>`papers/*/README.md`<br>`papers/*/SKILL.md` | `python3 code/orchestrators/build_work_pages.py` |
| Evidence pages | `evidence.html`<br>`pages/EVIDENCE.md` | `data/claims.json`<br>`code/orchestrators/build_evidence_page.py` | `python3 code/orchestrators/build_evidence_page.py` |
| Search index | `search-index.json` | `data/*.json`<br>`data/work-enrichment.json` | `python3 code/orchestrators/build_search_index.py` |
| Data catalog | `catalog.html`<br>`data/catalog.json` | `code/orchestrators/build_catalog.py`<br>`data/*.json` | `python3 code/orchestrators/build_catalog.py` |
| External link report | `reports/external_links_2026-05-13.json` | `site-critical HTML, Markdown, and JSON-LD files` | `python3 code/orchestrators/check_external_links.py` |
| Feed | `feed.xml` | `data/works.json`<br>`code/orchestrators/generate_feed.py` | `python3 code/orchestrators/generate_feed.py` |
| Sitemap | `sitemap.xml` | `works/*.html`<br>`code/orchestrators/build_sitemap.py` | `python3 code/orchestrators/build_sitemap.py` |
| Visual QA | `reports/visual-qa/2026-05-13/*.png`<br>`reports/visual-qa/2026-05-13/manifest.json` | `root HTML pages`<br>`style.css` | `python3 code/orchestrators/visual_qa.py` |

## Validation

Run `python3 code/orchestrators/validate_repo.py` before declaring the generated layer current.
