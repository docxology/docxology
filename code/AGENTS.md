# AGENTS.md — `code/`

Thin Python utilities and orchestrators for site-adjacent data, generated exports, validation, and public-source snapshots. GitHub Pages serves static files, but these scripts keep the source data and rendered pages synchronized.

## Layout

| Path | Role |
| --- | --- |
| `src/youtube_fetcher.py` | `yt-dlp` wrapper: fetch tabs, normalize records, save JSON |
| `src/count_consistency.py` | Parse BIBLIOGRAPHY / papers index counts; detect drift in llms.txt, README, publications title, `data/works.json`, `data/publications-ld.json` |
| `src/publication_pairing.py` | Normalize GitHub release and Zenodo record metadata; classify paired publication evidence |
| `src/resume_data.py` | Load, clean, validate, merge, and render structured resume/CV data |
| `src/site_nav.py` | `render_nav()` for work pages; `render_nav_domain()` for domain landing pages |
| `src/sitemap_policy.py` | Index-priority URL lists for `sitemap.xml` and IndexNow (open crawl; sitemap is not a crawl gate) |
| `orchestrators/fetch_youtube_data.py` | CLI entry: personal + institute channels → `data/*.json` |
| `orchestrators/export_bibliography.py` | Generate BibTeX, CSL JSON, RIS, and `data/works.json` from `pages/BIBLIOGRAPHY.md` |
| `orchestrators/export_agent_data.py` | Generate `data/software.json`, `data/people.json`, `data/organizations.json`, and `data/claims.json` |
| `orchestrators/build_resume.py` | Generate `data/resume.json`, plaintext resume variants, and `resume/resume.pdf` |
| `orchestrators/sync_paired_publications.py` | Dry-run/apply checker for paired GitHub release + Zenodo DOI publications |
| `orchestrators/build_domain_pages.py` | Generate `domains.html`, `domain-*.html`, and `pages/DOMAINS.md` |
| `orchestrators/build_work_pages.py` | Generate `works/index.html` and one HTML landing page per bibliography row |
| `orchestrators/build_evidence_page.py` | Generate `evidence.html` and `pages/EVIDENCE.md` from `data/claims.json` |
| `orchestrators/build_catalog.py` | Generate `catalog.html` and `data/catalog.json` with Schema.org DataCatalog metadata |
| `orchestrators/build_updates_page.py` | Generate `updates.html` from `CHANGELOG.md` |
| `orchestrators/build_search_index.py` | Generate `search-index.json` for site and agent discovery |
| `orchestrators/build_exports_page.py` | Generate `exports.html` HTML hub for citation/JSON exports |
| `orchestrators/build_sitemap.py` | Generate index-priority `sitemap.xml` (hubs + works + citation exports) |
| `orchestrators/indexnow_urls.py` | Emit filtered IndexNow URL list from sitemap policy |
| `orchestrators/validate_repo.py` | Validate generated files, JSON-LD, metadata, sitemap targets, local links, and count consistency |
| `orchestrators/sync_scholar_metrics.py` | Propagate `data/scholar-snapshot.json` to hand-maintained surfaces |
| `data/youtube_personal.json` | Cached export (personal channel) |
| `data/youtube_institute.json` | Cached export (institute channel) |
| `tests/test_youtube_fetcher.py` | Unit tests for fetcher parsing and normalization |
| `tests/test_count_consistency.py` | Unit tests for volatile-count drift detection |

Other orchestrators (external links, sitemap, visual QA, GitHub inventory, etc.) are listed in [GENERATED.md](../GENERATED.md) and [`data/generated-manifest.json`](../data/generated-manifest.json).

## Public API (`youtube_fetcher`)

- `run_yt_dlp(url: str, mode: str = "full", timeout: int = 600) -> list[str]` — JSONL lines from `yt-dlp`.
- `parse_jsonl(lines: list[str]) -> list[dict]` — skip bad lines.
- `normalize_video(raw: dict, channel_id: str) -> dict | None` — canonical video dict or `None` if no `upload_date`.
- `fetch_tab(channel_url: str, tab: str, channel_id: str, mode: str) -> list[dict]` — one tab (`videos` / `streams` / `shorts`).
- `fetch_channel(channel_url: str, channel_id: str) -> list[dict]` — all tabs, deduped, sorted by `upload_date`.
- `save_json(videos: list[dict], channel_url: str, channel_id: str, output_path: Path) -> None` — write envelope with `meta` + `videos`.
- `load_json(path: Path) -> dict | None` — read existing export.

## Generated discovery layer

Use [GENERATED.md](../GENERATED.md) as the exhaustive rebuild matrix. Dependency order:

1. Bibliography edits — `papers/sync_publications_html.py --apply`, `export_bibliography.py`, then work/domain/search/feed/sitemap exports.
2. Software catalog edits — `papers/sync_software_html.py --apply`, `export_agent_data.py`, then domain/search/catalog exports.
3. Claims-only edits — `export_agent_data.py`, then evidence/catalog/search exports.
4. Resume/CV exports — `build_resume.py --all` after changing `resume/source.json`, bibliography/software data, Scholar snapshot, or claim data.
5. Paired GitHub + Zenodo publication checks — `sync_paired_publications.py` writes a dry-run report by default; use `--apply` only for strong pairs.
6. Changelog or manifest changes — `build_updates_page.py` / `build_generated_manifest.py`.
7. Freshness and QA — reports under [`reports/`](../reports/); triage bot-protection before copy changes.
8. Health gate — `validate_repo.py` (includes count-consistency check).

## Tests

From repo root:

```bash
cd code/tests && uv run pytest -q
uv run python3 code/orchestrators/validate_repo.py
```

## Maintenance

Requires `yt-dlp` on `PATH` for live fetches. Static site copy lives at the repo root and under `pages/`; keep counts aligned with `pages/BIBLIOGRAPHY.md` and `papers/README.md` per root [AGENTS.md](../AGENTS.md) learned facts.
