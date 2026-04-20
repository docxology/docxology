"""
Orchestrator: fetch YouTube channel metadata for both channels.

Usage:
    python3 fetch_youtube_data.py              # fetch both channels
    python3 fetch_youtube_data.py --personal   # personal channel only
    python3 fetch_youtube_data.py --institute  # institute channel only
    python3 fetch_youtube_data.py --dry-run    # print stats from existing JSON
"""
import argparse
import logging
import sys
import time
from pathlib import Path

# Allow importing from code/src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import youtube_fetcher as yf

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

REPO_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = REPO_ROOT / "code" / "data"

CHANNELS = {
    "personal": {
        "url": "https://www.youtube.com/@danielarifriedman",
        "output": DATA_DIR / "youtube_personal.json",
    },
    "institute": {
        "url": "https://www.youtube.com/@activeinference",
        "output": DATA_DIR / "youtube_institute.json",
    },
}


def fetch_and_save(channel_id: str) -> None:
    cfg = CHANNELS[channel_id]
    print(f"\n--- Fetching {channel_id} channel: {cfg['url']} ---")
    t0 = time.time()
    videos = yf.fetch_channel(cfg["url"], channel_id)
    elapsed = time.time() - t0

    if videos:
        dates = [v["upload_date"] for v in videos]
        print(f"  {len(videos)} videos | {min(dates)[:4]}–{max(dates)[:4]} | {elapsed:.1f}s")
    else:
        print(f"  0 videos fetched ({elapsed:.1f}s)")

    yf.save_json(videos, cfg["url"], channel_id, cfg["output"])
    print(f"  Saved → {cfg['output']}")


def dry_run(channel_id: str) -> None:
    cfg = CHANNELS[channel_id]
    data = yf.load_json(cfg["output"])
    if data is None:
        print(f"  {channel_id}: no data file at {cfg['output']}")
        return
    meta = data["meta"]
    videos = data["videos"]
    dates = [v["upload_date"] for v in videos] if videos else []
    date_range = f"{min(dates)[:4]}–{max(dates)[:4]}" if dates else "no videos"
    print(f"  {channel_id}: {meta['video_count']} videos | {date_range} | fetched {meta['fetched_at'][:10]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch YouTube channel metadata")
    parser.add_argument("--personal", action="store_true", help="Fetch personal channel only")
    parser.add_argument("--institute", action="store_true", help="Fetch institute channel only")
    parser.add_argument("--dry-run", action="store_true", help="Print stats from existing JSON")
    args = parser.parse_args()

    if args.personal and not args.institute:
        targets = ["personal"]
    elif args.institute and not args.personal:
        targets = ["institute"]
    else:
        targets = ["personal", "institute"]

    if args.dry_run:
        print("=== Dry run: existing data ===")
        for ch in targets:
            dry_run(ch)
    else:
        print("=== Fetching YouTube channel metadata ===")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        for ch in targets:
            fetch_and_save(ch)
        print("\nDone. Commit code/data/*.json to update the site.")


if __name__ == "__main__":
    main()
