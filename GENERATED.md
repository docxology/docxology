# Generated Files

This repository keeps public site pages, citation exports, data indexes, and QA reports as checked-in generated artifacts so GitHub Pages can serve them statically.

| Artifact | Outputs | Sources | Rebuild command |
| --- | --- | --- | --- |
| Paper folder doc regeneration | `papers/*/README.md` `papers/*/AGENTS.md` `papers/*/SKILL.md` | `papers/paper_metadata.json` `pages/BIBLIOGRAPHY.md` `papers/*/metadata.json` | `uv run python3 code/orchestrators/regenerate_docs.py --apply --force` |
| Publications HTML sync | `publications.html` `data/publications-ld.json` | `pages/BIBLIOGRAPHY.md` `code/src/biblio_table.py` | `python3 code/orchestrators/sync_publications_html.py --apply` |
| Metadata enrichment | `papers/*/metadata.json` | `papers/paper_metadata.json` `pages/BIBLIOGRAPHY.md` | `uv run python3 code/orchestrators/batch_enrich_metadata.py --apply` |
| Metadata quality improvement | `papers/*/metadata.json` | `papers/*/metadata.json` | `uv run python3 code/orchestrators/improve_metadata_quality.py --apply` |
| Bibliography exports | `bibliography.bib` `bibliography.csl.json` `bibliography.ris` `data/works.json` | `pages/BIBLIOGRAPHY.md` `code/src/biblio_table.py` | `python3 code/orchestrators/export_bibliography.py` |
| Scholar metrics sync | `pages/BIBLIOGRAPHY.md (badge)`<br>`index.html (meta/og/stat/li)`<br>`pages/PROFILE.md (prose + metrics table)`<br>`pages/LINKS.md`<br>`publications.html (header metrics pill)` | `data/scholar-snapshot.json`<br>`code/orchestrators/sync_scholar_metrics.py` | `python3 code/orchestrators/sync_scholar_metrics.py` |
| Current count report | `reports/current_counts.md`<br>`data/current-counts.json` | `pages/BIBLIOGRAPHY.md`<br>`papers/README.md`<br>`pages/SOFTWARE.md`<br>`data/works.json`<br>`data/software.json`<br>`data/github-repositories.json`<br>`reports/public_source_snapshot_*.json`<br>`reports/paired_publications_*.json` | `uv run python3 code/orchestrators/build_current_counts.py` |
| Open Graph preview images | `og-*.jpg`<br>`data/og-image-counts.json` | `data/current-counts.json`<br>`code/orchestrators/generate_og_images.py` | `python3 code/orchestrators/generate_og_images.py` |
| Agent data exports | `data/software.json`<br>`data/people.json`<br>`data/organizations.json`<br>`data/claims.json` | `pages/SOFTWARE.md`<br>`code/src/software_table.py`<br>`data/scholar-snapshot.json`<br>`code/orchestrators/export_agent_data.py` | `python3 code/orchestrators/export_agent_data.py` |
| Resume and CV exports | `data/resume.json`<br>`resume/full.txt`<br>`resume/academic.txt`<br>`resume/software-consulting.txt`<br>`resume/teaching-service.txt`<br>`resume/resume.pdf`<br>`resume/verify.html` | `resume/source.json`<br>`data/works.json`<br>`data/software.json`<br>`data/scholar-snapshot.json`<br>`data/claims.json`<br>`code/src/resume_data.py`<br>`code/orchestrators/build_resume.py` | `uv run python3 code/orchestrators/build_resume.py --all` |
| Software catalog HTML sync | `software.html`<br>`data/software-ld.json` | `pages/SOFTWARE.md`<br>`code/src/software_table.py`<br>`code/orchestrators/sync_software_html.py` | `python3 code/orchestrators/sync_software_html.py --apply` |
| Full GitHub repository inventory | `data/github-repositories.json`<br>`repositories.html` | `GitHub REST API`<br>`data/software.json`<br>`code/orchestrators/build_github_inventory.py` | `python3 code/orchestrators/build_github_inventory.py` |
| Paired publication sync report | `reports/paired_publications_2026-07-01.json` | `GitHub Releases API`<br>`Zenodo Records API`<br>`docs/operations/publication-sync.md`<br>`code/src/publication_pairing.py`<br>`code/orchestrators/sync_paired_publications.py` | `python3 code/orchestrators/sync_paired_publications.py` |
| Paired publication review decisions | `data/paired-publication-decisions.json`<br>`reports/paired_publications_review_queue_2026-06-04.md` | `reports/paired_publications_2026-07-01.json`<br>`manual review decision` | `manual review; update data/paired-publication-decisions.json` |
| Zenodo-only publication backfill | `pages/BIBLIOGRAPHY.md`<br>`papers/<YEAR>_<Slug>/`<br>`papers/paper_metadata.json`<br>`papers/README.md` | `Zenodo Records API`<br>`docs/operations/publication-sync.md`<br>`code/orchestrators/add_zenodo_only.py` | `python3 code/orchestrators/add_zenodo_only.py <record_id>` |
| Domain pages | `domains.html`<br>`domain-*.html`<br>`pages/DOMAINS.md` | `data/works.json`<br>`data/software.json`<br>`code/orchestrators/build_domain_pages.py` | `python3 code/orchestrators/build_domain_pages.py` |
| Work pages | `works/*.html`<br>`data/work-enrichment.json` | `data/works.json`<br>`papers/*/README.md`<br>`papers/*/SKILL.md` | `python3 code/orchestrators/build_work_pages.py` |
| Video pages | `videos/*.html`<br>`data/videos.json` | `code/data/youtube_personal.json`<br>`code/data/youtube_institute.json`<br>`data/video-transcripts/*.txt`<br>`data/works.json`<br>`data/work-enrichment.json` | `python3 code/orchestrators/build_video_pages.py` |
| Video transcript cache | `data/video-transcripts/*.txt` | `YouTube captions`<br>`code/orchestrators/fetch_video_transcripts.py` | `python3 code/orchestrators/fetch_video_transcripts.py --channel all` |
| Paper folder pages | `papers/*/index.html` | `data/works.json`<br>`papers/*/README.md`<br>`papers/*/AGENTS.md`<br>`papers/*/*.pdf` | `python3 code/orchestrators/build_paper_pages.py` |
| Evidence pages | `evidence.html`<br>`pages/EVIDENCE.md` | `data/claims.json`<br>`code/orchestrators/build_evidence_page.py` | `python3 code/orchestrators/build_evidence_page.py` |
| Search index | `search-index.json` | `data/*.json`<br>`data/work-enrichment.json` | `python3 code/orchestrators/build_search_index.py` |
| Data catalog | `catalog.html`<br>`data/catalog.json` | `code/orchestrators/build_catalog.py`<br>`data/*.json` | `python3 code/orchestrators/build_catalog.py` |
| Exports hub | `exports.html` | `code/orchestrators/build_exports_page.py`<br>`data/catalog.json` | `python3 code/orchestrators/build_exports_page.py` |
| Updates page | `updates.html` | `CHANGELOG.md`<br>`code/orchestrators/build_updates_page.py` | `python3 code/orchestrators/build_updates_page.py` |
| External link report | `reports/external_links_2026-05-15.json` | `site-critical HTML, Markdown, and JSON-LD files` | `python3 code/orchestrators/check_external_links.py` |
| Public source snapshot | `reports/public_source_snapshot_2026-06-18.json` | `GitHub, ORCID, PubMed, Europe PMC, Crossref, Zenodo public APIs` | `python3 code/orchestrators/refresh_public_sources.py` |
| Public source inventory | `reports/public_source_inventory_2026-06-18.json` | `ORCID, Crossref, PubMed, Europe PMC, Zenodo, Wikidata, Semantic Scholar, GitHub, AII pages` | `python3 code/orchestrators/refresh_public_source_inventory.py` |
| External link triage | `reports/external_links_triage_2026-05-15.json`<br>`reports/external_links_triage_2026-05-15.md` | `reports/external_links_2026-05-15.json` | `python3 code/orchestrators/build_external_link_triage.py` |
| Asset size audit | `reports/asset_size_2026-07-01.json` | `root HTML pages`<br>`og-*.jpg`<br>`data/*.json`<br>`style.css`<br>`sw.js` | `python3 code/orchestrators/audit_assets.py` |
| Static accessibility report | `reports/accessibility_static_2026-07-01.json` | `root HTML pages`<br>`style.css`<br>`code/orchestrators/accessibility_audit.py` | `python3 code/orchestrators/accessibility_audit.py` |
| Browser smoke checks | `reports/browser-smoke/2026-05-28/*.png`<br>`reports/browser-smoke/2026-05-28/manifest.json` | `root HTML pages`<br>`works/index.html`<br>`search-index.json` | `python3 code/orchestrators/browser_smoke.py` |
| Live site verification | `reports/live_site_verification_2026-07-01.json` | `https://danielarifriedman.com/`<br>`GitHub Pages API` | `python3 code/orchestrators/verify_live_site.py` |
| Feed | `feed.xml` | `data/works.json`<br>`code/orchestrators/generate_feed.py` | `python3 code/orchestrators/generate_feed.py` |
| Sitemap | `sitemap.xml` | `works/*.html`<br>`code/src/sitemap_policy.py`<br>`code/orchestrators/build_sitemap.py` | `python3 code/orchestrators/build_sitemap.py` |
| Image sitemap | `sitemap-images.xml` | `data/artworks.json`<br>`art/*`<br>`code/orchestrators/build_image_sitemap.py` | `python3 code/orchestrators/build_image_sitemap.py` |
| Visual QA | `reports/visual-qa/2026-05-28/*.png`<br>`reports/visual-qa/2026-05-28/manifest.json` | `root HTML pages`<br>`style.css` | `python3 code/orchestrators/visual_qa.py` |

## Validation

Run `python3 code/orchestrators/validate_repo.py` before declaring the generated layer current.
