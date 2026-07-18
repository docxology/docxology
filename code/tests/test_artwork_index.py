from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
import build_artwork_index  # noqa: E402


def test_artwork_index_is_compact_and_complete() -> None:
    source = json.loads((REPO_ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))
    payload = build_artwork_index.build_payload(source)

    assert payload["schema"] == "ArtworkIndex.v1"
    assert payload["count"] == source["count"]
    assert payload["fields"] == list(build_artwork_index.INDEX_FIELDS)
    assert "desc" not in payload["fields"]
    assert "sizes" not in payload["fields"]
    assert all(set(art) == set(build_artwork_index.INDEX_FIELDS) for art in payload["artworks"])


def test_artwork_index_matches_checked_in_projection() -> None:
    build_artwork_index.check()
