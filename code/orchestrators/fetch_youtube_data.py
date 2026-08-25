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
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

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


@dataclass(frozen=True)
class RefreshFailure:
    """An operational failure that prevented a cache refresh."""

    stage: str
    error_type: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "stage": self.stage,
            "error_type": self.error_type,
            "message": self.message,
        }


@dataclass(frozen=True)
class ChannelRefreshResult:
    """Result of attempting to refresh one on-disk channel cache.

    ``saved`` is true only after every requested tab completes and the new
    envelope is written successfully.  Failed/incomplete refreshes leave the
    previous cache untouched.
    """

    channel_id: str
    channel_url: str
    output_path: Path
    fast: bool
    elapsed_seconds: float
    fetch: yf.ChannelFetchResult | None
    saved: bool
    failure: RefreshFailure | None = None
    written_video_count: int | None = None

    @property
    def complete(self) -> bool:
        return self.fetch is not None and self.fetch.complete and self.failure is None

    def as_dict(self) -> dict:
        return {
            "channel_id": self.channel_id,
            "channel_url": self.channel_url,
            "output_path": str(self.output_path),
            "mode": "fast" if self.fast else "exact",
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "complete": self.complete,
            "saved": self.saved,
            "written_video_count": self.written_video_count,
            "fetch": self.fetch.as_dict() if self.fetch else None,
            "failure": self.failure.as_dict() if self.failure else None,
        }


def merge_videos(existing: list[dict], fetched: list[dict]) -> list[dict]:
    by_id = {video["id"]: video for video in existing if video.get("id")}
    for video in fetched:
        if video.get("id"):
            prior = by_id.get(video["id"])
            if prior:
                merged = {**prior, **video}
                for key in ("upload_date", "year", "month", "day"):
                    if prior.get(key):
                        merged[key] = prior[key]
                if prior.get("view_count") and not video.get("view_count"):
                    merged["view_count"] = prior["view_count"]
                by_id[video["id"]] = merged
            else:
                by_id[video["id"]] = video
    return sorted(by_id.values(), key=lambda video: (video.get("upload_date", ""), video.get("id", "")))


def refresh_channel(
    channel_id: str,
    channel_url: str,
    output_path: Path,
    *,
    fast: bool = False,
    fetcher: Callable[..., yf.ChannelFetchResult] = yf.fetch_channel_result,
    loader: Callable[[Path], dict | None] = yf.load_json,
    saver: Callable[[list[dict], str, str, Path], None] = yf.save_json,
    clock: Callable[[], float] = time.monotonic,
) -> ChannelRefreshResult:
    """Refresh one channel only when every requested YouTube tab completes.

    The cache is deliberately read and written only after a complete fetch.
    This prevents a transient failure in (for example) ``/streams`` from
    dropping records in the existing JSON export.
    """
    started = clock()
    try:
        fetch = fetcher(channel_url, channel_id, tabs=yf.FAST_TABS if fast else None)
    except Exception as exc:  # pragma: no cover - defensive boundary for custom fetchers
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=clock() - started,
            fetch=None,
            saved=False,
            failure=RefreshFailure("fetch", type(exc).__name__, str(exc)),
        )

    elapsed = clock() - started
    if not fetch.complete:
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=elapsed,
            fetch=fetch,
            saved=False,
        )

    try:
        existing = loader(output_path)
    except Exception as exc:  # pragma: no cover - corrupt-cache boundary
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=elapsed,
            fetch=fetch,
            saved=False,
            failure=RefreshFailure("load_cache", type(exc).__name__, str(exc)),
        )

    videos = list(fetch.videos)
    existing_videos = existing.get("videos", []) if isinstance(existing, dict) else []
    if not isinstance(existing_videos, list):
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=elapsed,
            fetch=fetch,
            saved=False,
            failure=RefreshFailure(
                "load_cache",
                "ValueError",
                "existing cache videos field is not a list",
            ),
        )
    if fast:
        videos = merge_videos(existing_videos, videos)
    elif existing_videos and not videos:
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=elapsed,
            fetch=fetch,
            saved=False,
            failure=RefreshFailure(
                "validate_refresh",
                "EmptyRefresh",
                "complete fetch returned no videos; preserved the non-empty existing cache",
            ),
        )

    try:
        saver(videos, channel_url, channel_id, output_path)
    except Exception as exc:  # pragma: no cover - filesystem boundary
        return ChannelRefreshResult(
            channel_id=channel_id,
            channel_url=channel_url,
            output_path=output_path,
            fast=fast,
            elapsed_seconds=elapsed,
            fetch=fetch,
            saved=False,
            failure=RefreshFailure("save_cache", type(exc).__name__, str(exc)),
        )

    return ChannelRefreshResult(
        channel_id=channel_id,
        channel_url=channel_url,
        output_path=output_path,
        fast=fast,
        elapsed_seconds=elapsed,
        fetch=fetch,
        saved=True,
        written_video_count=len(videos),
    )


def fetch_and_save(
    channel_id: str,
    *,
    fast: bool = False,
    fetcher: Callable[..., yf.ChannelFetchResult] = yf.fetch_channel_result,
    loader: Callable[[Path], dict | None] = yf.load_json,
    saver: Callable[[list[dict], str, str, Path], None] = yf.save_json,
    clock: Callable[[], float] = time.monotonic,
) -> ChannelRefreshResult:
    """Refresh a configured channel and return its structured result."""
    cfg = CHANNELS[channel_id]
    return refresh_channel(
        channel_id,
        cfg["url"],
        cfg["output"],
        fast=fast,
        fetcher=fetcher,
        loader=loader,
        saver=saver,
        clock=clock,
    )


def print_refresh_result(result: ChannelRefreshResult) -> None:
    """Render the structured result while preserving a machine-readable API."""
    print(f"\n--- Fetching {result.channel_id} channel ({'fast' if result.fast else 'exact'}): {result.channel_url} ---")
    if result.fetch is None:
        if result.failure is None:
            print("  Refresh failed before a structured fetch result was available.")
        else:
            print(f"  Refresh failed during {result.failure.stage}: {result.failure.error_type}: {result.failure.message}")
        return

    if not result.fetch.complete:
        print(f"  Incomplete refresh after {result.elapsed_seconds:.1f}s; existing cache preserved.")
        for failure in result.fetch.failures:
            print(f"  {failure.tab}: {failure.error_type}: {failure.message}")
        return

    if result.failure is not None:
        print(f"  Refresh failed during {result.failure.stage}: {result.failure.error_type}: {result.failure.message}")
        return

    print(f"  {result.written_video_count or 0} videos saved ({result.elapsed_seconds:.1f}s)")
    print(f"  Saved → {result.output_path}")


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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch YouTube channel metadata")
    parser.add_argument("--personal", action="store_true", help="Fetch personal channel only")
    parser.add_argument("--institute", action="store_true", help="Fetch institute channel only")
    parser.add_argument("--dry-run", action="store_true", help="Print stats from existing JSON")
    parser.add_argument("--fast", action="store_true", help="Use flat-playlist metadata for all tabs")
    args = parser.parse_args(argv)

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
        return 0
    else:
        print("=== Fetching YouTube channel metadata ===")
        results = [fetch_and_save(ch, fast=args.fast) for ch in targets]
        for result in results:
            print_refresh_result(result)
        failed = [result for result in results if not result.complete or not result.saved]
        if failed:
            print("\nRefresh incomplete; no incomplete channel cache was written.")
            return 1
        print("\nDone. Commit code/data/*.json to update the site.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
