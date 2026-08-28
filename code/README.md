# Source Layer Map

The `code/` tree is the entire build system for the static site. Two layers,
thin-orchestrator pattern: **`code/src/`** holds shared, importable logic;
**`code/orchestrators/`** holds runnable scripts that read sources, call `src`
helpers, and write the generated artifacts checked into the repo root.

- Agent roles and maintenance log for this tree: [`AGENTS.md`](AGENTS.md)
- Artifact-by-artifact rebuild matrix (generated): [`../GENERATED.md`](../GENERATED.md)
- Dependency-ordered full rebuild: `uv run python3 code/orchestrators/regenerate_all.py --validate`
- Gate before declaring work done: `uv run python3 code/orchestrators/validate_repo.py`
- Tests: `uv run python3 -m pytest code/tests -q`

## `code/src/` — shared modules

| Module | Purpose |
| --- | --- |
| `biblio_table.py` | Shared iteration over the 8-column unified bibliography table in `pages/BIBLIOGRAPHY.md` |
| `count_consistency.py` | Cross-checks volatile counts across agent-facing surfaces |
| `domain_inference.py` | Canonical whole-word domain inference shared by pairing, Zenodo-only add, metadata enrich, and doc regen |
| `paper_metadata_schema.py` | Dataclass schema for paper `metadata.json` validation |
| `public_integrity.py` | Privacy and URL-safety checks for public source and generated manifests |
| `publication_pairing.py` | Pairs public GitHub releases with Zenodo records |
| `report_paths.py` | Helpers for date-stamped report artifacts (latest-report resolution) |
| `resume_data.py` | Resume/CV data loading, validation, variant filtering, text rendering |
| `seo_invariants.py` | SEO invariant checks: canonicals, sitemap policy, redirect stubs, security head |
| `site_facts.py` | Read-only helpers for generated site facts |
| `site_nav.py` | Shared site navigation HTML (incl. Agent Map) for generated pages |
| `sitemap_policy.py` | Index-priority URL policy for `sitemap.xml` + IndexNow (source of truth for the URL set) |
| `software_table.py` | Shared iteration over `pages/SOFTWARE.md` repository tables |
| `youtube_fetcher.py` | YouTube channel metadata fetcher using yt-dlp |

## `code/orchestrators/` — runnable scripts

Grouped by role; per-script outputs, sources, and rebuild commands live in
[`../GENERATED.md`](../GENERATED.md) (artifact matrix + utilities table).

| Role | Scripts |
| --- | --- |
| **Driver / gate** | `regenerate_all.py` (ordered rebuild), `validate_repo.py` (runs every `--check` + invariants), `build_generated_manifest.py` (writes `GENERATED.md` itself) |
| **Bibliography & works** | `export_bibliography.py`, `sync_publications_html.py`, `build_work_pages.py`, `build_paper_pages.py`, `batch_enrich_metadata.py`, `improve_metadata_quality.py`, `regenerate_docs.py`, `generate_citation_cff.py`, `extract_paper_texts.py` |
| **Software & repos** | `sync_software_html.py`, `build_github_inventory.py`, `classify_repositories.py` |
| **Site pages** | `build_domain_pages.py`, `generate_pillar_pages.py`, `build_video_pages.py`, `build_catalog.py`, `build_exports_page.py`, `build_updates_page.py`, `build_evidence_page.py`, `build_search_index.py`, `sync_site_facts.py`, `ensure_agent_navigation.py`, `ensure_social_meta.py` |
| **Media & art** | `fetch_youtube_data.py`, `fetch_video_transcripts.py`, `build_artwork_index.py`, `generate_og_images.py` |
| **Resume** | `build_resume.py` |
| **Counts & integrity** | `build_current_counts.py`, `build_coverage_exceptions.py`, `build_agent_index.py`, `build_pages_artifact.py`, `build_release_integrity.py`, `build_reconciliation_report.py`, `audit_publication_skills.py` |
| **Publication sync (network)** | `refresh_public_sources.py`, `refresh_public_source_inventory.py`, `sync_paired_publications.py`, `sync_scholar_metrics.py`, `add_zenodo_only.py`, `check_zenodo_uncatalogued.py` |
| **SEO & indexing** | `build_sitemap.py`, `build_image_sitemap.py`, `generate_feed.py`, `indexnow_urls.py`, `submit_indexnow.py`, `gsc_followup_preflight.py` |
| **QA & audits** | `audit_assets.py`, `accessibility_audit.py`, `check_external_links.py`, `build_external_link_triage.py`, `browser_smoke.py`, `browser_qa.py`, `visual_qa.py`, `verify_live_site.py` |
| **Maintenance / one-shot** | `prune_old_reports.py`, `deploy_seo_security.py`, `migrate_inline_handlers.py`, `optimize_font_loading.py` |

## Deploy topology

The live site (`https://danielarifriedman.com/`) is served by GitHub Pages from
the **public** `docxology/docxology` repository (`pages.yml`, branch `main`).
The working checkout's default remote is `docxology-private`. Deploying means
pushing the same `main` history to **both** remotes:

```bash
git push docxology-private main
git push https://github.com/docxology/docxology.git main:main
```

The private repo's own `pages.yml` run always fails (Pages is not enabled
there) — that failure is noise, not a deploy signal. Watch
`gh run list --repo docxology/docxology --workflow pages.yml` for the real
deploy conclusion.

## Conventions

- Edit *sources*, run the matching orchestrator; never hand-edit a generated
  artifact (see `../CLAUDE.md` → "Source → generated").
- New tracked files ripple through the check onion (asset report → agent index
  → site facts → Pages manifest → release integrity): run `regenerate_all.py
  --validate`, then after committing regenerate `build_sitemap.py` (lastmod
  derives from git commit dates) and the integrity tail
  (`build_pages_artifact.py --write-manifest` → `build_agent_index.py` →
  `build_generated_manifest.py` → `build_release_integrity.py` → final
  `build_generated_manifest.py`).
- Every orchestrator carries a module docstring stating outputs and sources;
  `code/tests/` is the pytest suite gating CI.
