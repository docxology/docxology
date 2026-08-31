# Agent Start Guide

This repository is the public research, software, citation, evidence, and website index for Daniel Ari Friedman.

## First Reads

1. Start with [`llms.txt`](llms.txt) for canonical pages, machine-readable files, and source-of-truth rules.
2. Use [`discovery.html`](discovery.html) or [`pages/DISCOVERY.md`](pages/DISCOVERY.md) for public identifiers, API endpoints, and refresh queries.
3. Use [`data/agent-index.json`](data/agent-index.json) for the stable route, dataset-schema, count, freshness, and query manifest.
   Its `schemas` registry documents the fields and caveats for works, software, repositories, artworks, videos, people, organizations, CV, claims, search items, coverage exceptions, repository classifications, and generated reports; every `datasets` entry resolves to a documented schema.
4. Use [`GENERATED.md`](GENERATED.md) before editing generated artifacts.
5. Use [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md) as the curated bibliography source of truth.
6. Use [`pages/SOFTWARE.md`](pages/SOFTWARE.md) as the curated software source of truth.
7. Use [`docs/operations/publication-sync.md`](docs/operations/publication-sync.md) for GitHub + Zenodo publication intake and DOI/version refreshes.
8. Use [`docs/operations/repository-classification.md`](docs/operations/repository-classification.md) for complete-inventory versus curated-software review.
9. Use [`docs/operations/evidence-refresh.md`](docs/operations/evidence-refresh.md) for dated public-source and claim refreshes.
10. Browse [`docs/README.md`](docs/README.md) for the full repository-documentation index (architecture, operations, SEO, design, security, releases); [`docs/AGENTS.md`](docs/AGENTS.md) holds agent operational guidance.
11. For hosting boundaries, read [`docs/operations/github-pages-artifact.md`](docs/operations/github-pages-artifact.md); GitHub Pages receives a bounded web projection, while the repository remains the complete archive.
12. Read [`TODO.md`](TODO.md) for the unfinished public-release backlog; completed work belongs in `CHANGELOG.md` and dated reports.

## Task Recipes

| Task | Start Here | Verify With |
| --- | --- | --- |
| Cite the repository | [`CITATION.cff`](CITATION.cff), [`cite-verify.html`](cite-verify.html) | [`bibliography.bib`](bibliography.bib), [`bibliography.csl.json`](bibliography.csl.json) |
| Find a publication | [`search.html`](search.html), [`works/`](works/) | [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md), DOI links |
| Verify a public claim | [`evidence.html`](evidence.html), [`data/claims.json`](data/claims.json) | Primary URLs listed in the claim ledger |
| Find software | [`software.html`](software.html), [`repositories.html`](repositories.html), [`data/software.json`](data/software.json), [`data/github-repositories.json`](data/github-repositories.json) | Curated and full GitHub repository inventories |
| Generate resume/CV artifacts | [`resume/`](resume/), [`data/resume.json`](data/resume.json) | `uv run python3 code/orchestrators/build_resume.py --all`, then `--check` |
| Check GitHub + Zenodo publication intake | [`docs/operations/publication-sync.md`](docs/operations/publication-sync.md), latest `reports/paired_publications_*.json` | `GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii` (dry-run), then `--apply` for strong pairs only; use `add_zenodo_only.py <record_id>` for Zenodo records with no paired GitHub release |
| Audit publication skills | [`papers/`](papers/), [`data/works.json`](data/works.json) | `uv run python3 code/orchestrators/audit_publication_skills.py --check` |
| Refresh generated files | [`GENERATED.md`](GENERATED.md) | `uv run python3 code/orchestrators/regenerate_all.py --validate`; rerun as a byte-stability assurance |
| Google Search Console follow-up | [`docs/seo/gsc-followup.md`](docs/seo/gsc-followup.md), [`data/gsc-followup-checklist.json`](data/gsc-followup-checklist.json) | `uv run python3 code/orchestrators/gsc_followup_preflight.py` |
| Check deployed site health | latest `reports/live_site_verification_*.json` | `uv run python3 code/orchestrators/verify_live_site.py` |
| Classify repository inventory | [`docs/operations/repository-classification.md`](docs/operations/repository-classification.md) | `uv run python3 code/orchestrators/classify_repositories.py --check` |
| Refresh evidence and coverage | [`docs/operations/evidence-refresh.md`](docs/operations/evidence-refresh.md) | latest `reports/public_source_*.json`, `reports/source_coverage_*.json` |
| Run accessibility and visual QA | [`docs/operations/accessibility-qa.md`](docs/operations/accessibility-qa.md) | `uv run python3 code/orchestrators/accessibility_audit.py --check`; use the `browser-qa` extra for dynamic commands |
| Check Pages artifact size | [`docs/operations/github-pages-artifact.md`](docs/operations/github-pages-artifact.md) | `uv run python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size` |
| Run browser behavior QA | [`code/orchestrators/browser_qa.py`](code/orchestrators/browser_qa.py), latest `reports/browser-qa/` | `uv sync --extra browser-qa`, `uv run --extra browser-qa playwright install chromium`, then `uv run --extra browser-qa python3 code/orchestrators/browser_qa.py` and `--check` |
| Check release integrity | [`data/release-integrity.json`](data/release-integrity.json), [`data/pages-artifact-manifest.json`](data/pages-artifact-manifest.json) | `uv run python3 code/orchestrators/build_release_integrity.py --check`; require a deployed release with `--require-deployed` |
| Refresh public-source inventory | latest `reports/public_source_inventory_*.json` | `uv run python3 code/orchestrators/refresh_public_source_inventory.py` |
| Triage external links | latest dated report under `reports/` via the [GENERATED.md](GENERATED.md) triage row (e.g. `reports/external_links_triage_2026-08-29.md`) | `uv run python3 code/orchestrators/check_external_links.py`, then `python3 code/orchestrators/build_external_link_triage.py` |
| Extract paper full text + images | [`papers/`](papers/), [`code/orchestrators/extract_paper_texts.py`](code/orchestrators/extract_paper_texts.py) | `uv sync --extra pdf-extraction`, then `uv run --extra pdf-extraction python3 code/orchestrators/extract_paper_texts.py --force` (PyMuPDF is optional; base `pypdf` remains the text fallback) |
| Generate CITATION.cff | [`papers/*/CITATION.cff`](papers/), [`code/orchestrators/generate_citation_cff.py`](code/orchestrators/generate_citation_cff.py) | `uv run python3 code/orchestrators/generate_citation_cff.py --force` |
| Deploy SEO + security tags | [`*.html`](.), [`code/orchestrators/deploy_seo_security.py`](code/orchestrators/deploy_seo_security.py) | `uv run python3 code/orchestrators/deploy_seo_security.py` (idempotent — only adds missing CSP, rel-me, hreflang) |
| Migrate inline handlers | [`*.html`](.), [`code/orchestrators/migrate_inline_handlers.py`](code/orchestrators/migrate_inline_handlers.py) | `uv run python3 code/orchestrators/migrate_inline_handlers.py` |
| Optimize font loading | [`*.html`](.), [`code/orchestrators/optimize_font_loading.py`](code/orchestrators/optimize_font_loading.py) | `uv run python3 code/orchestrators/optimize_font_loading.py` |

## Source-Of-Truth Rules

- Curated local counts intentionally differ from public index counts when public sources include forks, duplicates, software archives, preprints, or name variants.
- Public APIs are freshness checks, not automatic replacements for curated bibliography and software rows.
- Treat Wikidata as an entity anchor, not sole evidence for lightly referenced claims.
- Google Scholar citation counts use [`data/scholar-snapshot.json`](data/scholar-snapshot.json) as the single source of truth; propagate with [`code/orchestrators/sync_scholar_metrics.py`](code/orchestrators/sync_scholar_metrics.py) (`--check` exits 1 on drift). Update only after a direct (non-cached) Scholar verify—anonymous or cached UI views can disagree with the snapshot. Every snapshot revision also needs a matching direct-authenticated [`data/scholar-verification-receipt.json`](data/scholar-verification-receipt.json), bound to the exact snapshot SHA-256.
- Do not edit generated outputs directly unless the generator itself is also updated.

## Validation Command

```bash
uv run python3 code/orchestrators/validate_repo.py
PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q
```
