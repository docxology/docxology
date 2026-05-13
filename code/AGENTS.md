# AGENTS.md — `code/`

Thin Python utilities and orchestrators for site-adjacent data, generated exports, validation, and public-source snapshots. GitHub Pages serves static files, but these scripts keep the source data and rendered pages synchronized.

## Layout

| Path | Role |
| --- | --- |
| `src/youtube_fetcher.py` | `yt-dlp` wrapper: fetch tabs, normalize records, save JSON |
| `orchestrators/fetch_youtube_data.py` | CLI entry: personal + institute channels → `data/*.json` |
| `orchestrators/export_bibliography.py` | Generate BibTeX, CSL JSON, RIS, and `data/works.json` from `pages/BIBLIOGRAPHY.md` |
| `orchestrators/export_agent_data.py` | Generate `data/software.json`, `data/people.json`, `data/organizations.json`, and `data/claims.json` |
| `orchestrators/build_domain_pages.py` | Generate `domains.html`, `domain-*.html`, and `pages/DOMAINS.md` |
| `orchestrators/build_work_pages.py` | Generate `works/index.html` and one HTML landing page per bibliography row |
| `orchestrators/build_evidence_page.py` | Generate `evidence.html` and `pages/EVIDENCE.md` from `data/claims.json` |
| `orchestrators/build_catalog.py` | Generate `catalog.html` and `data/catalog.json` with Schema.org DataCatalog metadata |
| `orchestrators/build_search_index.py` | Generate `search-index.json` for site and agent discovery |
| `orchestrators/check_external_links.py` | Generate scoped outbound-link freshness reports for site-critical files |
| `orchestrators/build_generated_manifest.py` | Generate `GENERATED.md` and `data/generated-manifest.json` |
| `orchestrators/generate_feed.py` | Generate `feed.xml` from recent works and site updates |
| `orchestrators/build_reconciliation_report.py` | Generate curated-vs-public source comparison outputs |
| `orchestrators/accessibility_audit.py` | Generate a static accessibility/metadata report |
| `orchestrators/build_sitemap.py` | Generate `sitemap.xml` from public pages, exports, reports, and work pages |
| `orchestrators/visual_qa.py` | Capture Playwright screenshots for key desktop/mobile pages |
| `orchestrators/refresh_public_sources.py` | Write timestamped public API freshness reports under `reports/` |
| `orchestrators/generate_og_images.py` | Generate tailored Open Graph preview images |
| `orchestrators/validate_repo.py` | Validate generated files, JSON-LD, metadata, sitemap targets, and local links |
| `data/youtube_personal.json` | Cached export (personal channel) |
| `data/youtube_institute.json` | Cached export (institute channel) |
| `tests/test_youtube_fetcher.py` | Unit tests for fetcher parsing and normalization |

## Public API (`youtube_fetcher`)

- `run_yt_dlp(url: str, mode: str = "full", timeout: int = 600) -> list[str]` — JSONL lines from `yt-dlp`.
- `parse_jsonl(lines: list[str]) -> list[dict]` — skip bad lines.
- `normalize_video(raw: dict, channel_id: str) -> dict | None` — canonical video dict or `None` if no `upload_date`.
- `fetch_tab(channel_url: str, tab: str, channel_id: str, mode: str) -> list[dict]` — one tab (`videos` / `streams` / `shorts`).
- `fetch_channel(channel_url: str, channel_id: str) -> list[dict]` — all tabs, deduped, sorted by `upload_date`.
- `save_json(videos: list[dict], channel_url: str, channel_id: str, output_path: Path) -> None` — write envelope with `meta` + `videos`.
- `load_json(path: Path) -> dict | None` — read existing export.

## Tests

From repo root:

```bash
cd code/tests && uv run pytest -q
python3 code/orchestrators/validate_repo.py
```

## Maintenance

Requires `yt-dlp` on `PATH` for live fetches. Orchestrator defaults write under `code/data/`. Static site and profile copy (including teaching lines) live at the repo root and under `pages/`; keep them consistent with [README.md](../README.md) and [AGENTS.md](../AGENTS.md) when you change YouTube or course data that surface on the site.

Generated public-site artifacts should be refreshed in dependency order: bibliography/software exports, domain/work/evidence/catalog/search/feed/reconciliation outputs, generated manifest, external-link report, sitemap, accessibility report, visual QA screenshots, then `validate_repo.py`.
