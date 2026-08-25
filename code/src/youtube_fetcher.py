"""
YouTube channel metadata fetcher using yt-dlp.
Fetches video metadata across /videos, /streams, and /shorts tabs.
"""
from __future__ import annotations

import json
import logging
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

# Tabs to fetch per channel. 'full' uses exact metadata (slower); 'approximate'
# uses flat-playlist + approximate_date (fast, dates accurate to ~weeks).
TABS = [
    ("videos",  "full"),
    ("streams", "approximate"),
    ("shorts",  "approximate"),
]

FAST_TABS = [
    ("videos", "approximate"),
    ("streams", "approximate"),
    ("shorts", "approximate"),
]


CommandExecutor = Callable[[list[str], int], subprocess.CompletedProcess]
VideoRunner = Callable[[str, str], list[str]]


@dataclass(frozen=True)
class TabFetchFailure:
    """A recoverable failure while retrieving one channel tab."""

    tab: str
    mode: str
    error_type: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "tab": self.tab,
            "mode": self.mode,
            "error_type": self.error_type,
            "message": self.message,
        }


@dataclass(frozen=True)
class TabFetchResult:
    """Outcome for one requested YouTube channel tab."""

    tab: str
    mode: str
    videos: tuple[dict[str, Any], ...]
    failure: TabFetchFailure | None = None

    @property
    def complete(self) -> bool:
        return self.failure is None

    def as_dict(self) -> dict[str, Any]:
        return {
            "tab": self.tab,
            "mode": self.mode,
            "complete": self.complete,
            "video_count": len(self.videos),
            "failure": self.failure.as_dict() if self.failure else None,
        }


@dataclass(frozen=True)
class ChannelFetchResult:
    """Structured result for a whole-channel refresh.

    A result is complete only when every requested tab succeeded.  Callers that
    persist cached data must check :attr:`complete` before writing, so an
    intermittent YouTube or yt-dlp failure cannot replace a complete cache with
    a partial catalog.
    """

    channel_url: str
    channel_id: str
    videos: tuple[dict[str, Any], ...]
    tabs: tuple[TabFetchResult, ...]

    @property
    def failures(self) -> tuple[TabFetchFailure, ...]:
        return tuple(result.failure for result in self.tabs if result.failure is not None)

    @property
    def complete(self) -> bool:
        return not self.failures

    def as_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "channel_url": self.channel_url,
            "complete": self.complete,
            "video_count": len(self.videos),
            "tabs": [result.as_dict() for result in self.tabs],
            "failures": [failure.as_dict() for failure in self.failures],
        }


class IncompleteChannelFetchError(RuntimeError):
    """Raised when a legacy video-list caller requests an incomplete channel."""

    def __init__(self, result: ChannelFetchResult):
        self.result = result
        failed_tabs = ", ".join(failure.tab for failure in result.failures) or "unknown"
        super().__init__(f"Incomplete YouTube channel fetch; failed tabs: {failed_tabs}")


def _run_subprocess(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    """Execute yt-dlp through the real subprocess boundary."""
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)


def run_yt_dlp(
    url: str,
    mode: str = "full",
    timeout: int = 600,
    executor: CommandExecutor = _run_subprocess,
) -> list[str]:
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
    result = executor(cmd, timeout)
    # yt-dlp may emit useful JSONL before reporting an unavailable item with
    # exit status 1.  That output is incomplete, so it must surface as a tab
    # failure rather than silently becoming a partial cache refresh.
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp exited {result.returncode}: {result.stderr[:500]}")
    return result.stdout.splitlines()


def parse_jsonl(lines: list[str]) -> list[dict[str, Any]]:
    """Parse a complete yt-dlp JSONL response without silently discarding data.

    ``yt-dlp --dump-json`` promises one object per line.  A malformed or
    non-object line therefore makes the tab's coverage unknown.  Treat it as
    a failure rather than skipping it: callers must preserve the previous
    cache instead of publishing a smaller, apparently successful catalog.
    """
    records: list[dict[str, Any]] = []
    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"malformed yt-dlp JSONL line {i}: {e.msg}") from e
        if not isinstance(record, dict):
            raise ValueError(f"yt-dlp JSONL line {i} is not an object")
        records.append(record)
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
        # Reject impossible dates (month 13, day 40, 2023-02-29) rather than
        # emitting a year/month/day that is not a real calendar date.
        datetime.strptime(upload_date, "%Y%m%d")
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


def fetch_tab(
    channel_url: str,
    tab: str,
    channel_id: str,
    mode: str,
    runner: VideoRunner = run_yt_dlp,
) -> list[dict]:
    """Fetch one tab (/videos, /streams, or /shorts) for a channel.

    ``runner`` is injectable for testability (defaults to :func:`run_yt_dlp`);
    it maps ``(url, mode)`` -> raw JSONL lines.
    """
    url = f"{channel_url}/{tab}"
    lines = runner(url, mode)
    raw_records = parse_jsonl(lines)
    videos: list[dict] = []
    invalid_records: list[int] = []
    for index, raw in enumerate(raw_records, start=1):
        rec = normalize_video(raw, channel_id)
        if rec is None:
            invalid_records.append(index)
        else:
            videos.append(rec)
    if invalid_records:
        preview = ", ".join(str(index) for index in invalid_records[:5])
        suffix = ", …" if len(invalid_records) > 5 else ""
        raise ValueError(
            f"{tab}: {len(invalid_records)} yt-dlp record(s) failed canonical video validation "
            f"(records {preview}{suffix})"
        )
    logger.info("  %s: %d videos", tab, len(videos))
    return videos


def fetch_channel_result(
    channel_url: str,
    channel_id: str,
    tabs: list[tuple[str, str]] | None = None,
    runner: VideoRunner = run_yt_dlp,
) -> ChannelFetchResult:
    """Fetch all tabs and return videos plus explicit completion state.

    Tab failures are retained in the result for diagnostics.  The returned
    videos are intentionally available for inspection, but :attr:`complete`
    remains false until all requested tabs succeed.
    """
    seen_ids: set[str] = set()
    all_videos: list[dict] = []
    tab_results: list[TabFetchResult] = []

    selected_tabs = TABS if tabs is None else tabs
    for tab, mode in selected_tabs:
        try:
            videos = fetch_tab(channel_url, tab, channel_id, mode, runner=runner)
        except Exception as e:
            logger.warning("Failed to fetch %s/%s: %s", channel_url, tab, e)
            tab_results.append(
                TabFetchResult(
                    tab=tab,
                    mode=mode,
                    videos=(),
                    failure=TabFetchFailure(
                        tab=tab,
                        mode=mode,
                        error_type=type(e).__name__,
                        message=str(e),
                    ),
                )
            )
            continue
        tab_results.append(TabFetchResult(tab=tab, mode=mode, videos=tuple(videos)))
        for v in videos:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                all_videos.append(v)

    all_videos.sort(key=lambda v: v["upload_date"])
    result = ChannelFetchResult(
        channel_url=channel_url,
        channel_id=channel_id,
        videos=tuple(all_videos),
        tabs=tuple(tab_results),
    )
    logger.info("Total unique: %d (complete=%s)", len(all_videos), result.complete)
    return result


def fetch_channel(
    channel_url: str,
    channel_id: str,
    tabs: list[tuple[str, str]] | None = None,
    runner: VideoRunner = run_yt_dlp,
) -> list[dict]:
    """Return channel videos for legacy callers when every tab succeeds.

    Cache-writing callers must use :func:`fetch_channel_result` and reject
    incomplete results.  This compatibility helper retains the historical
    list-returning interface while failing closed for incomplete channels.
    """
    result = fetch_channel_result(channel_url, channel_id, tabs=tabs, runner=runner)
    if not result.complete:
        raise IncompleteChannelFetchError(result)
    return list(result.videos)


def save_json(videos: list[dict], channel_url: str, channel_id: str, output_path: Path) -> None:
    """Atomically write a complete ChannelData envelope to disk as indented JSON."""
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
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(json.dumps(data, indent=2, ensure_ascii=False))
            handle.write("\n")
        temporary_path.replace(output_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    logger.info("Saved %d videos to %s", len(videos), output_path)


def load_json(path: Path) -> dict | None:
    """Load existing channel JSON. Returns None if file doesn't exist."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
