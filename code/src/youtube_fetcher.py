"""
YouTube channel metadata fetcher using yt-dlp.
Fetches video metadata across /videos, /streams, and /shorts tabs.
"""
import json
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# Tabs to fetch per channel. 'full' uses exact metadata (slower); 'approximate'
# uses flat-playlist + approximate_date (fast, dates accurate to ~weeks).
TABS = [
    ("videos",  "full"),
    ("streams", "approximate"),
    ("shorts",  "approximate"),
]


def run_yt_dlp(url: str, mode: str = "full", timeout: int = 600) -> list[str]:
    """Run yt-dlp on a URL, return JSONL lines.

    mode='full'        → --dump-json --no-download (exact upload_date, slower)
    mode='approximate' → --flat-playlist + approximate_date extractor arg (fast)
    """
    if mode == "approximate":
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-json",
            "--no-warnings",
            "--extractor-args", "youtubetab:approximate_date",
            url,
        ]
    else:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-warnings",
            "--no-download",
            url,
        ]
    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode not in (0, 1):
        raise RuntimeError(f"yt-dlp exited {result.returncode}: {result.stderr[:500]}")
    return result.stdout.splitlines()


def parse_jsonl(lines: list[str]) -> list[dict]:
    """Parse JSONL lines, skipping malformed lines."""
    records = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            logger.warning("Skipping malformed JSONL line %d: %s", i, e)
    return records


def normalize_video(raw: dict, channel_id: str) -> dict | None:
    """Normalize a raw yt-dlp record to canonical VideoRecord schema.

    Returns None if upload_date is missing.
    """
    upload_date = raw.get("upload_date")
    if not upload_date:
        return None

    if not (isinstance(upload_date, str) and len(upload_date) == 8):
        return None
    try:
        year  = int(upload_date[:4])
        month = int(upload_date[4:6])
        day   = int(upload_date[6:8])
    except ValueError:
        return None

    video_id = raw.get("id")
    if not video_id:
        return None

    return {
        "id":          video_id,
        "title":       raw.get("title") or raw.get("fulltitle") or "",
        "upload_date": upload_date,
        "year":        year,
        "month":       month,
        "day":         day,
        "duration":    raw.get("duration"),
        "view_count":  raw.get("view_count") or 0,
        "channel":     channel_id,
    }


def fetch_tab(channel_url: str, tab: str, channel_id: str, mode: str) -> list[dict]:
    """Fetch one tab (/videos, /streams, or /shorts) for a channel."""
    url = f"{channel_url}/{tab}"
    lines = run_yt_dlp(url, mode=mode)
    raw_records = parse_jsonl(lines)
    videos, skipped = [], 0
    for raw in raw_records:
        rec = normalize_video(raw, channel_id)
        if rec is None:
            skipped += 1
        else:
            videos.append(rec)
    if skipped:
        logger.info("  %s: skipped %d records (no upload_date)", tab, skipped)
    logger.info("  %s: %d videos", tab, len(videos))
    return videos


def fetch_channel(channel_url: str, channel_id: str) -> list[dict]:
    """Fetch all tabs for a channel, deduplicate, return date-sorted VideoRecords."""
    seen_ids: set[str] = set()
    all_videos: list[dict] = []

    for tab, mode in TABS:
        try:
            videos = fetch_tab(channel_url, tab, channel_id, mode)
        except Exception as e:
            logger.warning("Failed to fetch %s/%s: %s", channel_url, tab, e)
            continue
        for v in videos:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                all_videos.append(v)

    all_videos.sort(key=lambda v: v["upload_date"])
    logger.info("Total unique: %d", len(all_videos))
    return all_videos


def save_json(videos: list[dict], channel_url: str, channel_id: str, output_path: Path) -> None:
    """Write ChannelData envelope to disk as indented JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "meta": {
            "channel_id":     channel_id,
            "channel_url":    channel_url,
            "fetched_at":     datetime.now(timezone.utc).isoformat(),
            "video_count":    len(videos),
            "schema_version": "1.0",
        },
        "videos": videos,
    }
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Saved %d videos to %s", len(videos), output_path)


def load_json(path: Path) -> dict | None:
    """Load existing channel JSON. Returns None if file doesn't exist."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
