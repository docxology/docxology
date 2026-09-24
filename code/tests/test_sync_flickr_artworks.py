"""Unit tests for the Flickr artwork freshness sync (stubbed transport)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)
import sync_flickr_artworks as sync_mod  # noqa: E402


def _photo(pid: str, *, upload: str, taken: str, desc: str = "", tags: str = "") -> dict:
    return {
        "id": pid,
        "title": "Title &amp; Coda",
        "description": {"_content": desc},
        "tags": tags,
        "datetaken": taken,
        "dateupload": upload,
        "views": "12",
        "media": "photo",
        "url_m": f"https://live.staticflickr.com/65535/{pid}_abc_m.jpg",
        "license": "14",
        "o_width": "3000",
        "o_height": "4000",
    }


def _sizes_payload(pid: str) -> dict:
    return {
        "sizes": {
            "size": [
                {"label": "Medium 640", "source": f"https://live.staticflickr.com/65535/{pid}_abc_z.jpg"},
                {"label": "Large", "source": f"https://live.staticflickr.com/65535/{pid}_abc_b.jpg"},
                {"label": "insecure", "source": "http://live.staticflickr.com/65535/x.jpg"},
            ]
        }
    }


def _install_stub(monkeypatch, photos: list[dict]) -> list[str]:
    calls: list[str] = []

    def fake_fetch(url: str, **_kwargs) -> dict:
        calls.append(url)
        if "flickr.people.getPublicPhotos" in url:
            return {"stat": "ok", "photos": {"page": 1, "pages": 1, "total": str(len(photos)), "photo": photos}}
        if "flickr.photos.licenses.getInfo" in url:
            return {"stat": "ok", "licenses": {"license": [{"id": "14", "name": "CC BY-NC 4.0", "url": "https://creativecommons.org/licenses/by-nc/4.0/"}]}}
        if "flickr.photos.getSizes" in url:
            pid = url.split("photo_id=")[1]
            return {"stat": "ok", **_sizes_payload(pid)}
        raise AssertionError(f"unexpected API method: {url}")

    monkeypatch.setattr(sync_mod, "fetch_json", fake_fetch)
    return calls


def test_build_payload_schema_sort_and_unescape(monkeypatch) -> None:
    photos = [
        _photo("100", upload="1700000000", taken="2023-09-04 17:12:02", desc="A &amp; B &quot;quoted&quot;"),
        _photo("300", upload="1700000000", taken="2023-09-04 17:12:02"),
        _photo("200", upload="1800000000", taken="2024-01-01 00:00:00", desc="newest"),
    ]
    _install_stub(monkeypatch, photos)
    fetched, total = sync_mod.fetch_public_photos("KEY")
    assert total == 3
    size_maps = sync_mod.fetch_size_maps("KEY", [str(p["id"]) for p in fetched])
    license_map = sync_mod.fetch_license_map("KEY")
    payload = sync_mod.build_payload(fetched, size_maps, license_map)

    # Upload-desc order; equal upload timestamps fall back to id-desc so the
    # ordering is deterministic regardless of page fetch order.
    assert [record["id"] for record in payload["artworks"]] == ["200", "300", "100"]
    record = payload["artworks"][2]
    assert set(record) == set(sync_mod.RECORD_FIELDS)
    # Descriptions are HTML-unescaped exactly once: double-encoded entities and
    # title entities resolve to real characters.
    assert record["desc"] == 'A & B "quoted"'
    assert record["title"] == "Title & Coda"
    assert record["flickr_url"] == "https://www.flickr.com/photos/43693624@N07/100"
    assert record["date_upload"] == "2023-11-14 22:13:20"
    assert record["license"] == "14"
    assert record["license_name"] == "CC BY-NC 4.0"
    assert record["license_url"] == "https://creativecommons.org/licenses/by-nc/4.0/"
    # Sizes come from getSizes labels; insecure sources are dropped.
    assert record["sizes"] == {
        "Medium 640": "https://live.staticflickr.com/65535/100_abc_z.jpg",
        "Large": "https://live.staticflickr.com/65535/100_abc_b.jpg",
    }
    assert payload["count"] == 3


def test_payload_is_deterministic(monkeypatch) -> None:
    photos = [
        _photo("100", upload="1700000000", taken="2023-09-04 17:12:02", tags="pen ink"),
        _photo("200", upload="1800000000", taken="2024-01-01 00:00:00"),
    ]
    _install_stub(monkeypatch, photos)
    runs = []
    for _ in range(2):
        fetched, _total = sync_mod.fetch_public_photos("KEY")
        size_maps = sync_mod.fetch_size_maps("KEY", [str(p["id"]) for p in fetched])
        license_map = sync_mod.fetch_license_map("KEY")
        runs.append(sync_mod.payload_body(sync_mod.build_payload(fetched, size_maps, license_map)))
    assert runs[0] == runs[1]
    payload = json.loads(runs[0].replace("{", "{", 1))
    assert payload["source"] == sync_mod.SOURCE_LABEL


def test_check_drift_flags_new_photo(monkeypatch, tmp_path) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00")]
    _install_stub(monkeypatch, photos)
    output = tmp_path / "artworks.json"
    output.write_text(
        json.dumps({"generated_at": "2026-01-01", "source": sync_mod.SOURCE_LABEL, "count": 1,
                    "artworks": [{"id": "100", "title": "Old", "desc": "", "tags": [], "date": "",
                                  "views": "0", "media": "photo", "thumb": "", "flickr_url": "",
                                  "sizes": {}, "license": "0", "license_name": "", "license_url": "",
                                  "date_upload": "2023-11-14 22:13:20"}]}, indent=2) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sync_mod, "OUTPUT", output)
    fetched, _total = sync_mod.fetch_public_photos("KEY")
    size_maps = sync_mod.fetch_size_maps("KEY", [str(p["id"]) for p in fetched])
    license_map = sync_mod.fetch_license_map("KEY")
    live = sync_mod.build_payload(fetched, size_maps, license_map)
    assert sync_mod.on_disk_body() != sync_mod.payload_body(live)
