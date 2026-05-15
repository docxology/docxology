# Agent Start Guide

This repository is the public research, software, citation, evidence, and website index for Daniel Ari Friedman.

## First Reads

1. Start with [`llms.txt`](llms.txt) for canonical pages, machine-readable files, and source-of-truth rules.
2. Use [`discovery.html`](discovery.html) or [`pages/DISCOVERY.md`](pages/DISCOVERY.md) for public identifiers, API endpoints, and refresh queries.
3. Use [`GENERATED.md`](GENERATED.md) before editing generated artifacts.
4. Use [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md) as the curated bibliography source of truth.
5. Use [`pages/SOFTWARE.md`](pages/SOFTWARE.md) as the curated software source of truth.

## Task Recipes

| Task | Start Here | Verify With |
| --- | --- | --- |
| Cite the repository | [`CITATION.cff`](CITATION.cff), [`cite-verify.html`](cite-verify.html) | [`bibliography.bib`](bibliography.bib), [`bibliography.csl.json`](bibliography.csl.json) |
| Find a publication | [`search.html`](search.html), [`works/`](works/) | [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md), DOI links |
| Verify a public claim | [`evidence.html`](evidence.html), [`data/claims.json`](data/claims.json) | Primary URLs listed in the claim ledger |
| Find software | [`software.html`](software.html), [`repositories.html`](repositories.html), [`data/software.json`](data/software.json), [`data/github-repositories.json`](data/github-repositories.json) | Curated and full GitHub repository inventories |
| Refresh generated files | [`GENERATED.md`](GENERATED.md) | `python3 code/orchestrators/validate_repo.py` |
| Check deployed site health | [`reports/live_site_verification_2026-05-13.json`](reports/live_site_verification_2026-05-13.json) | `python3 code/orchestrators/verify_live_site.py` |
| Refresh public-source inventory | [`reports/public_source_inventory_2026-05-15.json`](reports/public_source_inventory_2026-05-15.json) | `python3 code/orchestrators/refresh_public_source_inventory.py` |
| Triage external links | [`reports/external_links_triage_2026-05-13.md`](reports/external_links_triage_2026-05-13.md) | `python3 code/orchestrators/check_external_links.py` |

## Source-Of-Truth Rules

- Curated local counts intentionally differ from public index counts when public sources include forks, duplicates, software archives, preprints, or name variants.
- Public APIs are freshness checks, not automatic replacements for curated bibliography and software rows.
- Treat Wikidata as an entity anchor, not sole evidence for lightly referenced claims.
- Treat Google Scholar citation counts as manually synced metrics because cache and access path can vary.
- Do not edit generated outputs directly unless the generator itself is also updated.

## Validation Command

```bash
python3 code/orchestrators/validate_repo.py
cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q
```
