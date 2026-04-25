# AGENTS.md — `code/`

Thin Python utilities and orchestrators for site-adjacent data (YouTube channel exports). Not required to build static HTML on GitHub Pages.

## Layout

| Path | Role |
| --- | --- |
| `src/youtube_fetcher.py` | `yt-dlp` wrapper: fetch tabs, normalize records, save JSON |
| `orchestrators/fetch_youtube_data.py` | CLI entry: personal + institute channels → `data/*.json` |
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
```

## Maintenance

Requires `yt-dlp` on `PATH` for live fetches. Orchestrator defaults write under `code/data/`.
