"""Unit tests for the Flickr artwork freshness sync (stubbed transport)."""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)
import sync_flickr_artworks as sync_mod  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = REPO_ROOT / "code" / "orchestrators" / "sync_flickr_artworks.py"


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


def _install_stub(monkeypatch, photos: list[dict], *, total: int | None = None) -> list[str]:
    """Stub the Flickr transport; ``total`` overrides the envelope total (default: len(photos))."""
    calls: list[str] = []

    def fake_fetch(url: str, **_kwargs) -> dict:
        calls.append(url)
        if "flickr.people.getPublicPhotos" in url:
            envelope_total = len(photos) if total is None else total
            return {"stat": "ok", "photos": {"page": 1, "pages": 1, "total": str(envelope_total), "photo": photos}}
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


# --- tag contract, unescape, validation, coverage, drift (pure functions) -------

_LICENSES = {"14": {"name": "CC BY-NC 4.0", "url": "https://creativecommons.org/licenses/by-nc/4.0/"}}


def _payload_for(photos: list[dict]) -> dict:
    """Build a real payload from photo dicts via the pure build_payload path."""
    size_maps = {
        str(photo["id"]): {"Large": f"https://live.staticflickr.com/65535/{photo['id']}_abc_b.jpg"}
        for photo in photos
    }
    payload = sync_mod.build_payload(photos, size_maps, _LICENSES)
    payload["generated_at"] = "2026-10-05"
    return payload


def _good_payload() -> dict:
    return _payload_for(
        [
            _photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink pen", desc="newest"),
            _photo("100", upload="1700000000", taken="2023-09-04 17:12:02", tags="curiocards möbius", desc="older"),
        ]
    )


def test_multiword_flickr_tags_arrive_as_clean_tokens() -> None:
    # Flickr's `tags` extra is the clean form: a quoted multiword tag like
    # "summer solstice" is already the single token `summersolstice`. The record
    # keeps exactly those tokens (the collection/search matching key).
    photo = _photo(
        "55349041831",
        upload="1800000000",
        taken="2026-06-21 07:00:00",
        tags="curiocards danielarifriedman möbius summersolstice",
    )
    record = sync_mod.build_record(photo, {}, {})
    assert record["tags"] == ["curiocards", "danielarifriedman", "möbius", "summersolstice"]
    assert not any(any(ch.isspace() for ch in tag) for tag in record["tags"])
    assert "tags_raw" not in record


def test_clean_tags_drops_repeated_tokens_but_keeps_order() -> None:
    # Two raw Flickr tags ("curio cards" and "curiocards") clean to one token.
    assert sync_mod.clean_tags("zeta curiocards alpha curiocards zeta") == ["zeta", "curiocards", "alpha"]
    assert sync_mod.clean_tags("") == []
    assert sync_mod.clean_tags(None) == []


def test_description_is_unescaped_exactly_once() -> None:
    photo = _photo("1", upload="1700000000", taken="", desc="Tom &amp;amp; Jerry &amp;quot;x&amp;quot; &lt;b&gt;")
    record = sync_mod.build_record(photo, {}, {})
    # One decode: &amp;amp; -> &amp; (not &), &amp;quot; -> &quot; (not ").
    assert record["desc"] == "Tom &amp; Jerry &quot;x&quot; <b>"
    # Titles are likewise decoded once.
    titled = _photo("2", upload="1700000000", taken="")
    titled["title"] = "A &amp;amp; B"
    assert sync_mod.build_record(titled, {}, {})["title"] == "A &amp; B"


def test_validate_export_accepts_a_good_payload() -> None:
    payload = _good_payload()
    assert sync_mod.validate_export(payload) == []
    # A fresh payload has generated_at None until it is stamped.
    payload["generated_at"] = None
    assert sync_mod.validate_export(payload) == []


def _reorder_top_level(payload: dict) -> None:
    payload["generated_at"] = payload.pop("generated_at")


def _bad_count(payload: dict) -> None:
    payload["count"] = 99


def _swap_records(payload: dict) -> None:
    payload["artworks"].reverse()


def _duplicate_id(payload: dict) -> None:
    payload["artworks"][1]["id"] = payload["artworks"][0]["id"]


def _non_numeric_id(payload: dict) -> None:
    payload["artworks"][0]["id"] = "abc1"


def _extra_field(payload: dict) -> None:
    payload["artworks"][0]["tags_raw"] = []


def _missing_field(payload: dict) -> None:
    del payload["artworks"][0]["license_url"]


def _reordered_fields(payload: dict) -> None:
    record = payload["artworks"][0]
    payload["artworks"][0] = {field: record[field] for field in reversed(sync_mod.RECORD_FIELDS)}


def _whitespace_tag(payload: dict) -> None:
    payload["artworks"][0]["tags"] = ["ink", "curio cards"]


def _empty_tag(payload: dict) -> None:
    payload["artworks"][0]["tags"] = ["ink", ""]


def _duplicate_tag(payload: dict) -> None:
    payload["artworks"][0]["tags"] = ["ink", "pen", "ink"]


def _wrong_flickr_url(payload: dict) -> None:
    payload["artworks"][0]["flickr_url"] = "https://www.flickr.com/photos/someone-else/200"


def _http_thumb(payload: dict) -> None:
    payload["artworks"][0]["thumb"] = "http://live.staticflickr.com/65535/200_abc_m.jpg"


def _http_size(payload: dict) -> None:
    payload["artworks"][0]["sizes"]["Large"] = "http://live.staticflickr.com/65535/200_abc_b.jpg"


def _empty_upload(payload: dict) -> None:
    payload["artworks"][0]["date_upload"] = ""


def _impossible_upload(payload: dict) -> None:
    payload["artworks"][0]["date_upload"] = "2026-13-40 00:00:00"


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (_reorder_top_level, "top-level keys"),
        (_bad_count, "count 99 != len(artworks) 2"),
        (_swap_records, "not sorted by (date_upload, id) descending"),
        (_duplicate_id, "duplicate id"),
        (_non_numeric_id, "is not a numeric string"),
        (_extra_field, "unexpected ['tags_raw']"),
        (_missing_field, "missing ['license_url']"),
        (_reordered_fields, "not in RECORD_FIELDS order"),
        (_whitespace_tag, "'curio cards' contains whitespace"),
        (_empty_tag, "is not a non-empty string"),
        (_duplicate_tag, "duplicate tags ['ink']"),
        (_wrong_flickr_url, "flickr_url"),
        (_http_thumb, "thumb"),
        (_http_size, "sizes['Large']"),
        (_empty_upload, "date_upload '' is not YYYY-MM-DD HH:MM:SS"),
        (_impossible_upload, "is not YYYY-MM-DD HH:MM:SS"),
    ],
)
def test_validate_export_reports_specific_defects(mutate, expected: str) -> None:
    payload = copy.deepcopy(_good_payload())
    mutate(payload)
    errors = sync_mod.validate_export(payload)
    assert any(expected in message for message in errors), errors


def test_validate_export_rejects_non_objects_and_non_lists() -> None:
    assert sync_mod.validate_export([]) == ["export is not a JSON object"]
    broken = _good_payload()
    broken["artworks"] = "nope"
    assert "artworks is not a list" in sync_mod.validate_export(broken)


def _coverage_payload() -> dict:
    long_desc = "<p>" + "y" * (sync_mod.THIN_DESCRIPTION_CHARS + 10) + "</p>"
    return _payload_for(
        [
            _photo("105", upload="1700000005", taken="", tags="ink pen", desc=long_desc),
            _photo("104", upload="1700000004", taken="", tags="", desc=""),
            _photo("103", upload="1700000003", taken="", tags="ink", desc="tiny"),
            _photo("102", upload="1700000002", taken="", tags="", desc=long_desc),
            _photo("101", upload="1700000001", taken="", tags="", desc="<br/>"),
        ]
    )


def test_coverage_summary_counts() -> None:
    summary = sync_mod.coverage_summary(_coverage_payload())
    assert summary["count"] == 5
    assert summary["flickr_total"] is None and summary["total_mismatch"] is False
    assert summary["untagged"] == 3 and summary["untagged_ids"] == ["104", "102", "101"]
    # Plain-text emptiness: markup-only descriptions count as empty.
    assert summary["empty_desc"] == 2 and summary["empty_desc_ids"] == ["104", "101"]
    assert summary["short_desc"] == 3  # empty ones included
    assert summary["thin"] == 2  # untagged AND short: 104 and 101
    assert summary["tags_with_whitespace"] == 0
    assert summary["tags_per_record"] == {"min": 0, "mean": 0.6, "max": 2}
    assert summary["licenses"] == {"14 CC BY-NC 4.0": 5}
    assert summary["media"] == {"photo": 5}
    assert summary["vs_previous"] is None


def test_coverage_summary_flags_whitespace_tags_and_total_mismatch() -> None:
    payload = _coverage_payload()
    payload["artworks"][0]["tags"].append("curio cards")
    summary = sync_mod.coverage_summary(payload, flickr_total=7)
    assert summary["tags_with_whitespace"] == 1
    assert summary["flickr_total"] == 7 and summary["total_mismatch"] is True
    assert sync_mod.coverage_summary(payload, flickr_total=5)["total_mismatch"] is False


def test_coverage_summary_delta_against_previous_export() -> None:
    current = _coverage_payload()
    previous = copy.deepcopy(current)
    previous["artworks"] = [r for r in previous["artworks"] if r["id"] != "102"]  # 102 is new
    previous["artworks"].append({**previous["artworks"][0], "id": "999"})  # 999 vanished
    for record in previous["artworks"]:
        if record["id"] == "105":
            record["tags"] = ["ink"]  # tags changed
        if record["id"] == "103":
            record["desc"] = "a different description"  # desc changed
    delta = sync_mod.coverage_summary(current, previous=previous)["vs_previous"]
    assert delta == {
        "added": ["102"],
        "removed": ["999"],
        "tags_changed": ["105"],
        "desc_changed": ["103"],
    }


def test_format_coverage_and_completeness_problems() -> None:
    previous = _good_payload()
    summary = sync_mod.coverage_summary(_coverage_payload(), flickr_total=999, previous=previous)
    text = sync_mod.format_coverage(summary)
    assert "untagged            3 [104, 102, 101]" in text
    assert "empty description   2" in text
    assert "tags w/ whitespace  0 (must be 0)" in text
    assert "MISMATCH" in text and "999" in text
    # The compared total is Flickr's public one: no owner-view excuse in the report.
    assert "owner-view" not in text and "non-public" not in text
    assert "vs checked-in" in text
    assert sync_mod.completeness_problems(summary) == ["3 untagged records", "2 records with an empty description"]
    complete = sync_mod.coverage_summary(_good_payload())
    assert complete["untagged"] == 0
    assert complete["empty_desc"] == 0
    assert sync_mod.completeness_problems(complete) == []


def test_drift_ignores_views_but_not_content() -> None:
    live = _good_payload()
    current = copy.deepcopy(live)
    assert sync_mod.classify_drift(current, live) == ("up-to-date", [])

    # Views move constantly on Flickr; that alone is not drift.
    current["artworks"][0]["views"] = "9999"
    current["generated_at"] = "2020-01-01"
    assert sync_mod.payload_body(current) != sync_mod.payload_body(live)
    assert sync_mod.drift_body(current) == sync_mod.drift_body(live)
    status, details = sync_mod.classify_drift(current, live)
    assert status == "views-only" and details == ["views changed on 1 records"]

    # A real content change alongside a views change is still drift.
    current["artworks"][1]["title"] = "Renamed"
    status, details = sync_mod.classify_drift(current, live)
    assert status == "stale" and details == ["record content changed"]

    # Added / removed ids and a missing export are drift with specific details.
    missing_one = copy.deepcopy(live)
    missing_one["artworks"].pop()
    missing_one["count"] = 1
    assert sync_mod.classify_drift(missing_one, live)[1] == ["added 1 (newest: ['100'])"]
    assert sync_mod.classify_drift(live, missing_one)[1] == ["removed 1"]
    assert sync_mod.classify_drift(None, live) == ("stale", ["data/artworks.json missing"])


def _point_sync_at(monkeypatch, tmp_path: Path) -> Path:
    output = tmp_path / "data" / "artworks.json"
    output.parent.mkdir(parents=True)
    monkeypatch.setattr(sync_mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sync_mod, "OUTPUT", output)
    return output


def test_sync_write_prints_coverage_and_writes_a_valid_export(monkeypatch, tmp_path, capsys) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink", desc="newest")]
    _install_stub(monkeypatch, photos)
    output = _point_sync_at(monkeypatch, tmp_path)
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0
    out = capsys.readouterr().out
    assert "flickr artwork coverage:" in out and "wrote data/artworks.json (1 artworks)" in out
    written = json.loads(output.read_text(encoding="utf-8"))
    assert sync_mod.validate_export(written) == []

    # Dry run prints the coverage delta against the file just written, writes nothing new.
    before = output.read_text(encoding="utf-8")
    assert sync_mod.sync("KEY", write=False, check_drift=False) == 0
    out = capsys.readouterr().out
    assert "vs checked-in       +0 added, -0 removed, 0 tags changed, 0 descriptions changed" in out
    assert "dry run: 1 artworks; not writing data/artworks.json" in out
    assert output.read_text(encoding="utf-8") == before


def test_sync_check_drift_treats_views_as_informational(monkeypatch, tmp_path, capsys) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink", desc="newest")]
    _install_stub(monkeypatch, photos)
    _point_sync_at(monkeypatch, tmp_path)
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0
    capsys.readouterr()

    photos[0]["views"] = "4242"
    assert sync_mod.sync("KEY", write=False, check_drift=True) == 0
    assert "informational: views changed on 1 records" in capsys.readouterr().out

    photos[0]["tags"] = "ink pen"
    with pytest.raises(sync_mod.FlickrSyncError, match="stale vs Flickr: record content changed"):
        sync_mod.sync("KEY", write=False, check_drift=True)


def test_require_complete_refuses_to_write_an_incomplete_export(monkeypatch, tmp_path, capsys) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="", desc="newest")]
    _install_stub(monkeypatch, photos)
    output = _point_sync_at(monkeypatch, tmp_path)
    with pytest.raises(sync_mod.FlickrSyncError, match="1 untagged records"):
        sync_mod.sync("KEY", write=True, check_drift=False, require_complete=True)
    assert not output.exists()
    # --dry-run combines with --require-complete; the coverage still prints first.
    with pytest.raises(sync_mod.FlickrSyncError, match="--require-complete"):
        sync_mod.sync("KEY", write=False, check_drift=False, require_complete=True)
    assert "untagged            1" in capsys.readouterr().out
    # Without the flag the same export writes normally (default behavior unchanged).
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0
    assert output.exists()


def test_sync_refuses_to_write_an_invalid_export(monkeypatch, tmp_path) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink")]
    photos[0].pop("url_m")  # no thumbnail -> record fails validate_export
    _install_stub(monkeypatch, photos)
    output = _point_sync_at(monkeypatch, tmp_path)
    with pytest.raises(sync_mod.FlickrSyncError, match="failed validation"):
        sync_mod.sync("KEY", write=True, check_drift=False)
    assert not output.exists()


# --- decision 1: fetched count below Flickr's public total is refused ------------


def _truncated_photos() -> list[dict]:
    return [
        _photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink", desc="newest"),
        _photo("100", upload="1700000000", taken="2023-09-04 17:12:02", tags="pen", desc="older"),
    ]


def test_sync_refuses_a_fetch_below_the_public_total(monkeypatch, tmp_path, capsys) -> None:
    calls = _install_stub(monkeypatch, _truncated_photos(), total=3)
    output = _point_sync_at(monkeypatch, tmp_path)
    for kwargs in (
        {"write": True, "check_drift": False},
        {"write": False, "check_drift": False},  # --dry-run
        {"write": False, "check_drift": True},  # --check-drift
    ):
        with pytest.raises(sync_mod.FlickrSyncError) as excinfo:
            sync_mod.sync("KEY", **kwargs)
        message = str(excinfo.value)
        assert "fetched 2 public photos but Flickr's public total is 3 (-1)" in message
        assert "--allow-count-mismatch" in message
        assert not output.exists()
    # Refused before the per-photo getSizes fan-out: no wasted requests.
    assert not any("flickr.photos.getSizes" in url for url in calls)
    capsys.readouterr()


def test_allow_count_mismatch_writes_with_a_warning(monkeypatch, tmp_path, capsys) -> None:
    _install_stub(monkeypatch, _truncated_photos(), total=3)
    output = _point_sync_at(monkeypatch, tmp_path)
    assert sync_mod.sync("KEY", write=True, check_drift=False, allow_count_mismatch=True) == 0
    captured = capsys.readouterr()
    assert "continuing because --allow-count-mismatch was passed" in captured.err
    assert "MISMATCH of -1" in captured.out and "owner-view" not in captured.out
    assert sync_mod.validate_export(json.loads(output.read_text(encoding="utf-8"))) == []


def test_a_higher_fetched_count_is_only_a_warning(monkeypatch, tmp_path, capsys) -> None:
    _install_stub(monkeypatch, _truncated_photos(), total=1)
    output = _point_sync_at(monkeypatch, tmp_path)
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0
    captured = capsys.readouterr()
    assert "warning: fetched 2 public photos but Flickr reports total 1" in captured.err
    assert "MISMATCH of +1" in captured.out
    assert output.exists()


def test_main_plumbs_allow_count_mismatch_end_to_end(monkeypatch, tmp_path, capsys) -> None:
    _install_stub(monkeypatch, _truncated_photos(), total=3)
    output = _point_sync_at(monkeypatch, tmp_path)
    monkeypatch.setenv("FLICKR_API_KEY", "KEY")

    monkeypatch.setattr(sys, "argv", ["sync_flickr_artworks.py"])
    with pytest.raises(SystemExit) as refused:
        sync_mod.main()
    assert refused.value.code == 1
    assert "--allow-count-mismatch" in capsys.readouterr().err
    assert not output.exists()

    monkeypatch.setattr(sys, "argv", ["sync_flickr_artworks.py", "--allow-count-mismatch"])
    with pytest.raises(SystemExit) as accepted:
        sync_mod.main()
    assert accepted.value.code == 0
    assert output.exists()


# --- decision 2: malformed on-disk exports never produce a traceback ---------------


def _write_export(output: Path, content: object) -> None:
    text = content if isinstance(content, str) else json.dumps(content)
    output.write_text(text, encoding="utf-8")


def test_coverage_local_reports_validator_errors_for_a_non_object_export(monkeypatch, tmp_path, capsys) -> None:
    output = _point_sync_at(monkeypatch, tmp_path)
    _write_export(output, "[]")
    assert sync_mod.coverage_local() == 1
    captured = capsys.readouterr()
    assert "export is not a JSON object" in captured.err
    assert "flickr artwork coverage" not in captured.out


def test_coverage_local_reports_validator_errors_for_non_list_tags(monkeypatch, tmp_path, capsys) -> None:
    output = _point_sync_at(monkeypatch, tmp_path)
    payload = _good_payload()
    payload["artworks"][0]["tags"] = 5
    _write_export(output, payload)
    assert sync_mod.coverage_local() == 1
    captured = capsys.readouterr()
    assert "tags is not a list" in captured.err
    assert "flickr artwork coverage" not in captured.out


def test_coverage_local_reports_validator_errors_for_a_null_artworks_list(monkeypatch, tmp_path, capsys) -> None:
    output = _point_sync_at(monkeypatch, tmp_path)
    _write_export(output, {"artworks": None})
    assert sync_mod.coverage_local() == 1
    assert "artworks is not a list" in capsys.readouterr().err


def test_coverage_local_still_summarizes_a_sound_export(monkeypatch, tmp_path, capsys) -> None:
    output = _point_sync_at(monkeypatch, tmp_path)
    _write_export(output, _good_payload())
    assert sync_mod.coverage_local() == 0
    captured = capsys.readouterr()
    assert "validate_export: ok" in captured.out and "flickr artwork coverage:" in captured.out


def test_helpers_tolerate_malformed_shapes() -> None:
    for payload in (None, [], "x", 5, {"artworks": None}, {"artworks": "s"}, {"artworks": {"id": "1"}}):
        assert sync_mod._records_by_id(payload) == {}
    mixed = {"artworks": [1, None, "x", {"no_id": 1}, {"id": 3, "tags": 5}]}
    assert sync_mod._records_by_id(mixed) == {"3": {"id": 3, "tags": 5}}

    # coverage_summary: non-list tags / non-list artworks are counted, not raised on.
    summary = sync_mod.coverage_summary({"artworks": [{"id": "1", "tags": 5, "desc": None}]}, previous=[])
    assert summary["count"] == 1 and summary["tags_per_record"] == {"min": 0, "mean": 0.0, "max": 0}
    assert summary["vs_previous"] == {"added": ["1"], "removed": [], "tags_changed": [], "desc_changed": []}
    assert sync_mod.coverage_summary({"artworks": None})["count"] == 0
    assert sync_mod.coverage_summary([])["count"] == 0  # type: ignore[arg-type]

    live = _good_payload()
    for current in ([], {"artworks": None}):
        status, details = sync_mod.classify_drift(current, live)
        assert status == "stale" and "malformed" in details[0]


@pytest.mark.parametrize(
    ("content", "problem"),
    [("[]", "export is not a JSON object"), ('{"artworks": null}', "artworks is not a list")],
)
def test_sync_survives_a_malformed_checked_in_export(monkeypatch, tmp_path, capsys, content: str, problem: str) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink", desc="newest")]
    _install_stub(monkeypatch, photos)
    output = _point_sync_at(monkeypatch, tmp_path)

    _write_export(output, content)
    assert sync_mod.sync("KEY", write=False, check_drift=False) == 0  # dry run
    captured = capsys.readouterr()
    assert f"is malformed ({problem})" in captured.err
    assert "flickr artwork coverage:" in captured.out and "vs checked-in" not in captured.out
    assert output.read_text(encoding="utf-8") == content  # dry run left the file alone

    # Drift gate: a malformed baseline is drift, with a clear message.
    with pytest.raises(sync_mod.FlickrSyncError, match=rf"stale vs Flickr: data/artworks.json is malformed \({problem}\)"):
        sync_mod.sync("KEY", write=False, check_drift=True)

    # A resync repairs the file.
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0
    assert sync_mod.validate_export(json.loads(output.read_text(encoding="utf-8"))) == []


def test_sync_tolerates_junk_records_in_a_well_shaped_checked_in_export(monkeypatch, tmp_path, capsys) -> None:
    photos = [_photo("200", upload="1800000000", taken="2024-01-01 00:00:00", tags="ink", desc="newest")]
    _install_stub(monkeypatch, photos)
    output = _point_sync_at(monkeypatch, tmp_path)
    _write_export(output, {"artworks": [1, "x", {"id": 200, "tags": 5}, {"id": "9", "tags": 5}]})
    assert sync_mod.sync("KEY", write=False, check_drift=False) == 0
    captured = capsys.readouterr()
    assert "malformed" not in captured.err
    assert "vs checked-in       +0 added, -1 removed, 1 tags changed, 1 descriptions changed" in captured.out
    assert sync_mod.sync("KEY", write=True, check_drift=False) == 0


# --- decision 3: date_upload must be fixed-width ASCII ------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        "2026-1-5 1:2:3",  # not zero-padded
        "2026-01-05 1:02:03",  # hour not zero-padded
        "2026-01-05 01:02:03\n",  # trailing newline
        " 2026-01-05 01:02:03",
        "2026-01-05T01:02:03",
        "\uff12\uff10\uff12\uff16-01-05 01:02:03",  # fullwidth digits pass strptime
        "2026-13-40 00:00:00",  # right shape, impossible calendar date
        "2026-02-30 00:00:00",
    ],
)
def test_validate_export_requires_fixed_width_ascii_date_upload(bad: str) -> None:
    payload = copy.deepcopy(_good_payload())
    payload["artworks"][0]["date_upload"] = bad
    errors = sync_mod.validate_export(payload)
    assert any("is not YYYY-MM-DD HH:MM:SS" in message for message in errors), (bad, errors)


def test_validate_export_accepts_a_canonical_date_upload() -> None:
    payload = copy.deepcopy(_good_payload())
    payload["artworks"][0]["date_upload"] = "2027-01-05 01:02:03"
    assert sync_mod.validate_export(payload) == []


# --- decision 4: 'newest' ids are listed newest first -------------------------------


def _drift_photos(uploads: dict[str, str]) -> list[dict]:
    return [_photo(pid, upload=upload, taken="") for pid, upload in uploads.items()]


def test_newest_first_orders_by_upload_then_id_then_id_alone() -> None:
    records = {
        "100": {"date_upload": "2023-01-01 00:00:00"},
        "200": {"date_upload": "2025-01-01 00:00:00"},
        "300": {"date_upload": "2024-01-01 00:00:00"},
        "400": {"date_upload": "2024-01-01 00:00:00"},
    }
    assert sync_mod._newest_first(["100", "200", "300", "400"], records) == ["200", "400", "300", "100"]
    # Without records the order is id descending (numeric: longer ids are larger).
    assert sync_mod._newest_first({"9", "10", "100"}, {}) == ["100", "10", "9"]
    # An id whose record lacks a usable date_upload sorts as the oldest.
    assert sync_mod._newest_first(["1", "2"], {"1": {"date_upload": 5}, "2": {}}) == ["2", "1"]


def test_classify_drift_lists_the_newest_added_ids_first() -> None:
    # id order and upload order agree: 500 is newest.
    live = _payload_for(
        _drift_photos(
            {"100": "1700000000", "200": "1700000100", "300": "1700000200", "400": "1700000300", "500": "1700000400"}
        )
    )
    current = _payload_for(_drift_photos({"100": "1700000000"}))
    status, details = sync_mod.classify_drift(current, live)
    assert status == "stale"
    assert details == ["added 4 (newest: ['500', '400', '300'])"]


def test_upload_order_beats_id_order_for_added_ids() -> None:
    uploads = {"100": "1700000000", "200": "1900000000", "300": "1750000000", "400": "1750000000", "500": "1710000000"}
    live = _payload_for(_drift_photos(uploads))
    current = _payload_for(_drift_photos({"100": "1700000000"}))
    status, details = sync_mod.classify_drift(current, live)
    assert status == "stale"
    # 200 was uploaded last; 400 and 300 tie on upload and fall back to id descending.
    assert details == ["added 4 (newest: ['200', '400', '300'])"]

    delta = sync_mod.coverage_summary(live, previous=current)["vs_previous"]
    assert delta["added"] == ["200", "400", "300", "500"]
    # And in the other direction the removed ids come out newest first too.
    removed = sync_mod.coverage_summary(current, previous=live)["vs_previous"]["removed"]
    assert removed == ["200", "400", "300", "500"]

    text = sync_mod.format_coverage(sync_mod.coverage_summary(live, previous=current))
    assert "added ids: [200, 400, 300, 500]" in text


def test_format_coverage_truncates_added_ids_to_the_newest() -> None:
    count = sync_mod.REPORT_LIST_LIMIT + 3
    uploads = {str(1000 + i): str(1700000000 + i) for i in range(count)}
    live = _payload_for(_drift_photos(uploads))
    current = _payload_for(_drift_photos({"1000": "1700000000"}))
    text = sync_mod.format_coverage(sync_mod.coverage_summary(live, previous=current))
    newest = str(1000 + count - 1)
    line = next(row for row in text.splitlines() if row.strip().startswith("added ids:"))
    assert f"[{newest}, " in line and "(+" in line
    assert str(1001) not in line  # the oldest added ids are the ones truncated away


def _run_script(*args: str, key: str | None = None) -> subprocess.CompletedProcess:
    env = {name: value for name, value in os.environ.items() if name != "FLICKR_API_KEY"}
    if key is not None:
        env["FLICKR_API_KEY"] = key
    return subprocess.run(
        [sys.executable, str(SYNC_SCRIPT), *args],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def test_coverage_local_runs_offline_without_an_api_key() -> None:
    result = _run_script("--coverage-local")
    assert result.returncode == 0, result.stderr
    assert "validate_export: ok" in result.stdout
    exported = json.loads((REPO_ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))
    count = re.search(r"^\s+artworks\s+(\d+)", result.stdout, re.M)
    assert count and int(count.group(1)) == exported["count"]
    for field in ("untagged", "empty description", "short description", "thin pages"):
        assert re.search(rf"^\s+{field}\s+\d+", result.stdout, re.M), (field, result.stdout)
    assert re.search(r"^\s+tags w/ whitespace\s+0 \(must be 0\)", result.stdout, re.M), result.stdout
    assert "tags per record" in result.stdout and "licenses" in result.stdout and "media" in result.stdout


def test_live_modes_still_require_an_api_key() -> None:
    result = _run_script("--dry-run")
    assert result.returncode != 0
    assert "FLICKR_API_KEY is not set" in result.stderr
    combined = _run_script("--coverage-local", "--dry-run")
    assert combined.returncode != 0 and "cannot be combined" in combined.stderr
    allow = _run_script("--coverage-local", "--allow-count-mismatch")
    assert allow.returncode != 0 and "cannot be combined" in allow.stderr


def _paged_stub(monkeypatch, envelopes: list[dict | None]) -> None:
    """Serve one getPublicPhotos envelope per page; ``None`` omits the envelope."""

    def fake_fetch(url: str, **_kwargs) -> dict:
        page = int(re.search(r"[?&]page=(\d+)", url).group(1))
        envelope = envelopes[page - 1]
        return {"stat": "ok"} if envelope is None else {"stat": "ok", "photos": envelope}

    monkeypatch.setattr(sync_mod, "fetch_json", fake_fetch)


def test_a_first_page_without_a_total_is_refused(monkeypatch) -> None:
    _paged_stub(monkeypatch, [{"page": 1, "pages": 1, "photo": [_photo("1", upload="1700000000", taken="2023-09-04 17:12:02")]}])
    with pytest.raises(sync_mod.FlickrSyncError, match="no usable total"):
        sync_mod.fetch_public_photos("key")


@pytest.mark.parametrize(
    "second_page",
    [
        {"page": 2, "pages": 2, "photo": []},
        {"page": 2, "pages": 2, "total": "n/a", "photo": []},
        None,
    ],
    ids=["no-total", "unparseable-total", "no-envelope"],
)
def test_a_truncated_later_page_cannot_lower_the_total(monkeypatch, second_page) -> None:
    first = {"page": 1, "pages": 2, "total": "3", "photo": [_photo("1", upload="1700000000", taken="2023-09-04 17:12:02"), _photo("2", upload="1700000000", taken="2023-09-04 17:12:02")]}
    _paged_stub(monkeypatch, [first, second_page])
    photos, total = sync_mod.fetch_public_photos("key")
    assert (len(photos), total) == (2, 3)
    with pytest.raises(sync_mod.FlickrSyncError):
        sync_mod._count_mismatch_gate(len(photos), total, allow=False)


def test_failure_messages_never_carry_the_api_key() -> None:
    url = sync_mod.api_url("flickr.photos.getSizes", "secret-key-value", photo_id="42")
    redacted = sync_mod.redact_url(url)
    assert "secret-key-value" not in redacted
    assert "api_key=REDACTED" in redacted and "photo_id=42" in redacted
    assert "method=flickr.photos.getSizes" in redacted
