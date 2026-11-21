# Agent Start Guide

This repository is the public research, software, citation, evidence, and website index for Daniel Ari Friedman.

## Inspect maintenance commands

After [setting up the locked environment](docs/operations/development.md#configuration-ownership),
`uv run --no-sync python3 code/orchestrators/agent.py status --json` observes local
prerequisites. `uv run --no-sync python3 code/orchestrators/agent.py plan --json`
previews the authoritative ordered write/check
commands and manual/network exclusions. Neither executes those commands nor
certifies validation or deployment. Use `plan --step <id> --json` to inspect one
step. See the [interface contract](docs/operations/agent-interface.md).

## First Reads

1. Start with [`llms.txt`](llms.txt) for canonical pages, machine-readable files, and source-of-truth rules.
2. Use [`discovery.html`](discovery.html) or [`pages/DISCOVERY.md`](pages/DISCOVERY.md) for public identifiers, API endpoints, and refresh queries.
3. Use [`data/agent-index.json`](data/agent-index.json) for the stable route, dataset-schema, count, freshness, and query manifest.
   Its `schemas` registry documents the fields and caveats for works, software, repositories, artworks, videos, people, organizations, CV, claims, search items, coverage exceptions, repository classifications, and generated reports; every `datasets` entry resolves to a documented schema.
4. Use [`GENERATED.md`](GENERATED.md) before editing generated artifacts.
5. Use [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md) as the curated bibliography source of truth.
6. Use [`pages/SOFTWARE.md`](pages/SOFTWARE.md) as the curated software source of truth.
7. Use [`docs/operations/publication-sync.md`](docs/operations/publication-sync.md) for GitHub + Zenodo publication intake and DOI/version refreshes.
   For 1-3 new pairs with data-only changes and a same-day warning-free scan,
   use the **fast intake path** in that runbook
   ([docs/operations/publication-sync.md](docs/operations/publication-sync.md)
   → "Fast Intake Path (Small, Data-Only Changes)") — cached reports and
   fingerprint-gated regeneration instead of full re-fetching.
8. Use [`docs/operations/repository-classification.md`](docs/operations/repository-classification.md) for complete-inventory versus curated-software review.
9. Use [`docs/operations/evidence-refresh.md`](docs/operations/evidence-refresh.md) for dated public-source and claim refreshes.
10. Browse [`docs/README.md`](docs/README.md) for the full repository-documentation index; [`docs/operations/development.md`](docs/operations/development.md) maps architecture, configuration ownership, and verification boundaries. [`docs/AGENTS.md`](docs/AGENTS.md) holds agent operational guidance.
11. For hosting boundaries, read [`docs/operations/github-pages-artifact.md`](docs/operations/github-pages-artifact.md); GitHub Pages receives a bounded web projection. Existing local originals remain preserved; new primary PDFs may use reviewed versioned Zenodo files.
12. Read [`TODO.md`](TODO.md) for the unfinished public-release backlog; completed work belongs in `CHANGELOG.md` and dated reports.

## Task Recipes

| Task | Start Here | Verify With |
| --- | --- | --- |
| Cite the repository | [`CITATION.cff`](CITATION.cff), [`cite-verify.html`](cite-verify.html) | [`bibliography.bib`](bibliography.bib), [`bibliography.csl.json`](bibliography.csl.json) |
| Find a publication | [`search.html`](search.html), [`works/`](works/) | [`pages/BIBLIOGRAPHY.md`](pages/BIBLIOGRAPHY.md), DOI links |
| Allocate a new work identity | [`data/work-identifiers.json`](data/work-identifiers.json), [`docs/seo/canonical-policy.md`](docs/seo/canonical-policy.md) | Reviewed intake allocates once; manual rows require `uv run python3 code/orchestrators/export_bibliography.py --register-new-identifiers` |
| Verify a public claim | [`evidence.html`](evidence.html), [`data/claims.json`](data/claims.json) | Primary URLs listed in the claim ledger |
| Find software | [`software.html`](software.html), [`repositories.html`](repositories.html), [`data/software.json`](data/software.json), [`data/github-repositories.json`](data/github-repositories.json) | Curated and full GitHub repository inventories |
| Generate resume/CV artifacts | [`resume/`](resume/), [`data/resume.json`](data/resume.json) | `uv run python3 code/orchestrators/build_resume.py --all`, then `--check` |
| Check GitHub + Zenodo publication intake | [`docs/operations/publication-sync.md`](docs/operations/publication-sync.md), latest `reports/paired_publications_*.json` | `GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii` (dry-run), then `--apply` for strong pairs only; review unpaired records using `check_zenodo_uncatalogued.py` and the [Zenodo-only workflow](docs/operations/publication-sync.md#zenodo-only-publications) |
| Audit publication skills | [`papers/`](papers/), [`data/works.json`](data/works.json) | `uv run python3 code/orchestrators/audit_publication_skills.py --check` |
| Refresh generated files | [`GENERATED.md`](GENERATED.md) | `uv run python3 code/orchestrators/regenerate_all.py --validate`; rerun as a byte-stability assurance |
| Google Search Console follow-up | [`docs/seo/gsc-followup.md`](docs/seo/gsc-followup.md), [`data/gsc-followup-checklist.json`](data/gsc-followup-checklist.json) | `uv run python3 code/orchestrators/gsc_followup_preflight.py` |
| Refresh the live-site observation | [Live verification](docs/operations/live-verification.md) | `uv run --no-sync python3 code/orchestrators/verify_live_site.py` writes a dated maintenance report. |
| Verify a specific Pages deployment | [Live verification](docs/operations/live-verification.md) | From the clean deployed checkout, use `verify_live_site.py` with `--expected-commit`, the Pages `--deployment-run-id`, and `--output` for a fresh receipt. |
| Verify a deployed candidate's bytes | [`docs/operations/github-pages-artifact.md`](docs/operations/github-pages-artifact.md) | `uv run python3 code/orchestrators/verify_deployed_artifact.py --expected-commit <full-HEAD-SHA> --output /tmp/deployment-acceptance.json`; receipt is targeted technical acceptance, separate from full release attestation |
| Classify repository inventory | [`docs/operations/repository-classification.md`](docs/operations/repository-classification.md) | `uv run python3 code/orchestrators/classify_repositories.py --check` |
| Refresh evidence and coverage | [`docs/operations/evidence-refresh.md`](docs/operations/evidence-refresh.md) | latest `reports/public_source_*.json`, `reports/source_coverage_*.json` |
| Run accessibility and visual QA | [`docs/operations/accessibility-qa.md`](docs/operations/accessibility-qa.md) | `uv run python3 code/orchestrators/accessibility_audit.py --check`; use the `browser-qa` extra for dynamic commands |
| Check Pages artifact size | [`docs/operations/github-pages-artifact.md`](docs/operations/github-pages-artifact.md) | `uv run python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size` |
| Run browser behavior QA | [Browser and Lighthouse checks](docs/operations/site-runtime.md#declared-browser-and-lighthouse-checks) | Follow the locked setup and run the rendered checks. Browser reports are under `reports/browser-qa/`. |
| Check release integrity | [`data/release-integrity.json`](data/release-integrity.json), [`data/pages-artifact-manifest.json`](data/pages-artifact-manifest.json) | `uv run python3 code/orchestrators/build_release_integrity.py --check`; require a deployed release with `--require-deployed` |
| Refresh public-source inventory | latest `reports/public_source_inventory_*.json` | `uv run python3 code/orchestrators/refresh_public_source_inventory.py` |
| Triage external links | latest dated report under `reports/` via the [GENERATED.md](GENERATED.md) triage row | `uv run python3 code/orchestrators/check_external_links.py`, then `uv run python3 code/orchestrators/build_external_link_triage.py` |
| Extract paper full text + images | [`papers/AGENTS.md`](papers/AGENTS.md), [`code/orchestrators/extract_paper_texts.py`](code/orchestrators/extract_paper_texts.py) | `uv sync --locked --extra pdf-extraction`, then `uv run --no-sync python3 code/orchestrators/extract_paper_texts.py --only <folder>`; add `--force` only for an intended source-bound re-extraction (base `pypdf` remains the text fallback) |
| Synchronize paper CITATION.cff | [`papers/`](papers/), [`code/orchestrators/generate_citation_cff.py`](code/orchestrators/generate_citation_cff.py) | `uv run python3 code/orchestrators/generate_citation_cff.py --apply`, then `--check`; curated citation identity owns DOI roles and registry-verified title/authors, while other fields are preserved |
| Validate the repository manuscript | [`docs/manuscript/README.md`](docs/manuscript/README.md), [`MANUSCRIPT_STATUS.md`](docs/manuscript/MANUSCRIPT_STATUS.md) | `uv run python3 code/orchestrators/validate_manuscript.py`; `--json` records structural findings, not rendering or publication readiness |
| Deploy SEO + security tags | [`*.html`](.), [`code/orchestrators/deploy_seo_security.py`](code/orchestrators/deploy_seo_security.py) | `uv run python3 code/orchestrators/deploy_seo_security.py` (idempotent — only adds missing CSP, rel-me, hreflang) |

Settle a finished change in one command — see
[`docs/operations/settle.md`](docs/operations/settle.md): it classifies dirty paths, runs the tiered
check battery, then lands the payload and control-tail commits (`--push`/`--pr` optional). Preview
the plan without executing anything with `uv run python3 code/orchestrators/settle.py --tier fast --dry-run`.

Landing rule worth knowing before your first lap: a commit that creates new
dated reports (snapshots, pairing receipts, reconciliation reports) flips the
`latest_source_report()` index-tracked resolution. Staging those receipts
before rendering lets the ordinary plan consume them immediately; report-aware
cache entries now include index membership. If adoption happens in a later
commit, run the ordinary plan again before its binder tail —
see the do-not-skip list in
[`docs/operations/publication-sync.md`](docs/operations/publication-sync.md).

## Source-Of-Truth Rules

- Curated local counts intentionally differ from public index counts when public sources include forks, duplicates, software archives, preprints, or name variants.
- Public APIs are freshness checks, not automatic replacements for curated bibliography and software rows.
- Permanent citation keys and numeric reservations live in `data/work-identifiers.json`. Editing a title or year does not rename a published work URL; removing a row requires an explicit retired reservation with a reason.
- Treat Wikidata as an entity anchor, not sole evidence for lightly referenced claims.
- Google Scholar citation counts use [`data/scholar-snapshot.json`](data/scholar-snapshot.json) as the single source of truth; propagate with [`code/orchestrators/sync_scholar_metrics.py`](code/orchestrators/sync_scholar_metrics.py) (`--check` exits 1 on drift). Update only after a direct (non-cached) Scholar verify—anonymous or cached UI views can disagree with the snapshot. Record the observation with [`code/orchestrators/record_scholar_observation.py`](code/orchestrators/record_scholar_observation.py), which writes the snapshot and its matching direct-authenticated [`data/scholar-verification-receipt.json`](data/scholar-verification-receipt.json) together, bound to the exact snapshot SHA-256, then run `sync_scholar_metrics.py`.
- Do not edit generated outputs directly unless the generator itself is also updated.
- Prefer existing versioned Zenodo archives for new primary PDF editions, keeping metadata, pages, available extracted text, and previews here. Record `remote_primary_pdf` and independent `source_evidence` per the [hosting policy](docs/operations/github-pages-artifact.md#primary-pdf-hosting-and-source-custody); preserve all existing local PDFs and URLs. A declaration does not verify remote bytes or authorize migration, deletion, a new repository, or a budget change.
- Preserve archived PDFs and literal `full_text.md` source extractions during directory/link maintenance. A replacement extraction requires the identified source document, its hash, and checks of affected quotations; PDF presence or a matching hash alone does not establish correct extraction or scientific replication. When the selected primary is remote, keep older local extraction provenance explicit.
- Repository-methods prose in `docs/manuscript/` describes this index system. It is separate from the publications archived in `papers/`; local manuscript validation does not grant publication status to either.
- Follow the [landing workflow](docs/operations/settle.md) for integration.
  Confirm the active work branch after merging or switching checkouts and before
  staging or committing.

## Validation commands

```bash
uv run --no-sync python3 code/orchestrators/validate_repo.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-sync python3 -m pytest code/tests -q -m "not browser and not manuscript_render" -n auto --dist loadfile
uv run --no-sync --group lint ruff check code
uv run --no-sync python3 code/src/artifact_budget.py
```

These commands reproduce the core validation checks. Install the locked
environment and lint group first. Follow [Site runtime](docs/operations/site-runtime.md)
for the separate browser and Lighthouse jobs. The default pytest selection
includes browser and native manuscript tests and fails when any selected test
skips. See [Development](docs/operations/development.md#verification-sequence)
for full-suite prerequisites and [Settle](docs/operations/settle.md) for landing.

## Backend performance

Use the [Python 3.15 profiling guide](docs/operations/backend-profiling.md) for fixed read-only timing/tracing workloads, external JSON diagnostics and comparison boundaries.
