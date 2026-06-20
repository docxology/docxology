from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from fetch_youtube_data import merge_videos  # noqa: E402


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
