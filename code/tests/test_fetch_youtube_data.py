from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from fetch_youtube_data import merge_videos, refresh_channel  # noqa: E402
import youtube_fetcher as yf  # noqa: E402


class _StaticFetcher:
    """Local injected fetcher that returns a pre-built channel result."""

    def __init__(self, result: yf.ChannelFetchResult):
        self.result = result
        self.calls: list[tuple[str, str, object]] = []

    def __call__(self, channel_url: str, channel_id: str, *, tabs: object = None) -> yf.ChannelFetchResult:
        self.calls.append((channel_url, channel_id, tabs))
        return self.result


class _UnexpectedCallback:
    """Fails the test if an incomplete refresh reaches cache I/O."""

    def __init__(self):
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("incomplete refresh must not reach cache I/O")


def _video(video_id: str = "video") -> dict:
    return {
        "id": video_id,
        "title": video_id,
        "upload_date": "20240101",
        "year": 2024,
        "month": 1,
        "day": 1,
        "duration": 10,
        "view_count": 1,
        "channel": "personal",
    }


def _channel_result(*, complete: bool, videos: tuple[dict, ...]) -> yf.ChannelFetchResult:
    if complete:
        tabs = tuple(
            yf.TabFetchResult(tab=tab, mode=mode, videos=videos if tab == "videos" else ())
            for tab, mode in yf.TABS
        )
    else:
        failure = yf.TabFetchFailure(
            tab="streams",
            mode="approximate",
            error_type="RuntimeError",
            message="simulated streams outage",
        )
        tabs = (
            yf.TabFetchResult(tab="videos", mode="full", videos=videos),
            yf.TabFetchResult(tab="streams", mode="approximate", videos=(), failure=failure),
            yf.TabFetchResult(tab="shorts", mode="approximate", videos=()),
        )
    return yf.ChannelFetchResult(
        channel_url="https://example.test/@channel",
        channel_id="personal",
        videos=videos,
        tabs=tabs,
    )


def test_merge_videos_preserves_exact_cached_date_and_nonzero_views():
    existing = [
        {
            "id": "abc",
            "title": "Original",
            "upload_date": "20200716",
            "year": 2020,
            "month": 7,
            "day": 16,
            "duration": 10,
            "view_count": 1092,
            "channel": "institute",
        }
    ]
    fetched = [
        {
            "id": "abc",
            "title": "Updated title",
            "upload_date": "20210620",
            "year": 2021,
            "month": 6,
            "day": 20,
            "duration": 10.0,
            "view_count": 0,
            "channel": "institute",
        },
        {
            "id": "new",
            "title": "New video",
            "upload_date": "20260619",
            "year": 2026,
            "month": 6,
            "day": 19,
            "duration": 20,
            "view_count": 0,
            "channel": "institute",
        },
    ]
    merged = {video["id"]: video for video in merge_videos(existing, fetched)}
    assert merged["abc"]["title"] == "Updated title"
    assert merged["abc"]["upload_date"] == "20200716"
    assert merged["abc"]["year"] == 2020
    assert merged["abc"]["view_count"] == 1092
    assert merged["new"]["upload_date"] == "20260619"


def test_incomplete_tab_refresh_preserves_existing_cache(tmp_path: Path):
    output_path = tmp_path / "youtube_personal.json"
    original = '{"meta":{"video_count":99},"videos":[{"id":"cached"}]}\n'
    output_path.write_text(original, encoding="utf-8")
    fetcher = _StaticFetcher(_channel_result(complete=False, videos=(_video(),)))
    loader = _UnexpectedCallback()
    saver = _UnexpectedCallback()

    result = refresh_channel(
        "personal",
        "https://example.test/@channel",
        output_path,
        fast=True,
        fetcher=fetcher,
        loader=loader,
        saver=saver,
        clock=iter((10.0, 12.5)).__next__,
    )

    assert not result.complete
    assert not result.saved
    assert result.failure is None
    assert result.fetch is not None
    assert result.fetch.failures[0].tab == "streams"
    assert result.as_dict()["fetch"]["complete"] is False
    assert fetcher.calls[0][2] == yf.FAST_TABS
    assert loader.calls == 0
    assert saver.calls == 0
    assert output_path.read_text(encoding="utf-8") == original


def test_complete_refresh_writes_structured_cache_result(tmp_path: Path):
    output_path = tmp_path / "youtube_personal.json"
    fetcher = _StaticFetcher(_channel_result(complete=True, videos=(_video(),)))

    result = refresh_channel(
        "personal",
        "https://example.test/@channel",
        output_path,
        fetcher=fetcher,
        clock=iter((3.0, 3.25)).__next__,
    )

    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert result.complete
    assert result.saved
    assert result.written_video_count == 1
    assert result.as_dict()["written_video_count"] == 1
    assert written["meta"]["video_count"] == 1
    assert written["videos"][0]["id"] == "video"
    assert not list(tmp_path.glob(".youtube_personal.json.*.tmp"))


def test_complete_but_empty_exact_refresh_preserves_existing_cache(tmp_path: Path):
    output_path = tmp_path / "youtube_personal.json"
    original = '{"meta":{"video_count":1},"videos":[{"id":"cached"}]}\n'
    output_path.write_text(original, encoding="utf-8")
    fetcher = _StaticFetcher(_channel_result(complete=True, videos=()))

    result = refresh_channel(
        "personal",
        "https://example.test/@channel",
        output_path,
        fetcher=fetcher,
        clock=iter((10.0, 10.5)).__next__,
    )

    assert not result.complete
    assert not result.saved
    assert result.failure is not None
    assert result.failure.stage == "validate_refresh"
    assert result.failure.error_type == "EmptyRefresh"
    assert output_path.read_text(encoding="utf-8") == original
