#!/usr/bin/env python3
"""Refresh ``data/artworks.json`` from the Flickr REST API (network freshness step).

The gallery export was frozen from the ``art.html`` embedded gallery data on
2026-05-13; this orchestrator replaces that snapshot with a live fetch of
``flickr.people.getPublicPhotos`` for NSID ``43693624@N07``, so every public
photostream upload (and every description/tag/view refresh on Flickr) reaches
the site through a single documented freshness pass.

Freshness contract (see ``docs/operations/publication-sync.md``):

- Network fetches are deliberate, separate steps: this script is NOT part of
  ``regenerate_all.py`` and is classified in ``generation_plan.EXCLUDED_OPERATIONS``.
- The API key comes from the ``FLICKR_API_KEY`` environment variable and is
  never committed. In CI it maps to the ``FLICKR_API_KEY`` repository secret.
- Modes: default writes ``data/artworks.json``; ``--dry-run`` fetches and prints
  a summary without writing; ``--check-drift`` fetches and exits nonzero when
  the checked-in export differs from live (CI drift gate). The volatile
  ``views`` counter is excluded from drift (``DRIFT_IGNORED_FIELDS``): a
  views-only difference is reported as informational and exits 0, while the
  write path still stores the current views.
- Offline: ``--coverage-local`` runs ``validate_export`` and ``coverage_summary``
  on the checked-in ``data/artworks.json`` with no network and no
  ``FLICKR_API_KEY``; it exits 1 when the structural validator finds errors.
- Completeness: ``--require-complete`` exits nonzero after a live fetch (or with
  ``--coverage-local``, on the checked-in export) when any record is untagged or
  has an empty description. It is opt-in and may be combined with ``--dry-run``;
  when it fails, nothing is written.
- Validation: ``validate_export`` is a pure structural check (key order, unique
  ids, exact record fields, whitespace-free unique tags, URL shapes, upload
  timestamps, sort order). ``sync`` runs it before anything is written and
  refuses to write an invalid export.
- Coverage: ``coverage_summary`` / ``format_coverage`` print tag and description
  coverage (untagged, empty and short descriptions, thin pages, tag counts,
  license and media mixes) plus the delta against the checked-in export (added
  and removed ids, records whose tags or description changed) in the
  ``--dry-run`` and write paths.
- Tags: ``tags`` holds Flickr's clean tag tokens (lowercase, spaces and
  punctuation stripped, so a quoted multiword tag arrives as one token such as
  ``summersolstice``). They are the collection/search matching key and are never
  split further. The export is public-only (``getPublicPhotos``).
- Count guard: Flickr's ``total`` comes from the same ``getPublicPhotos`` query
  as the photos, so a fetched count LOWER than it means a truncated fetch and
  the sync refuses to write (``FlickrSyncError``) unless ``--allow-count-mismatch``
  is passed; a HIGHER fetched count is only a warning.
- Deterministic: records sort by (date_upload desc, id desc), every payload
  field is content-derived, and ``generated_at`` is reused via
  ``stable_generated_at`` when the body is unchanged (no timestamp churn).

Deliberately NOT synced here: ``width``/``height`` original dimensions. The
NEW-1 contract in ``code/tests/test_art_thumb_dimensions.py`` pins the
art-grid to CSS-pinned tile shape with no HTML dimension attributes; landing
the real per-image dims requires a conscious art.html flip, not a silent
manifest field.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "data" / "artworks.json"

from docxology_tools.artwork_pages import THIN_DESCRIPTION_CHARS, is_thin, plain_text  # noqa: E402
from docxology_tools.report_paths import stable_generated_at  # noqa: E402

FLICKR_NSID = "43693624@N07"
FLICKR_REST = "https://api.flickr.com/services/rest/"
PHOTOS_PER_PAGE = 500
EXTRAS = (
    "description,tags,date_taken,date_upload,views,url_m,url_z,url_l,url_o,"
    "license,media,o_dims"
)
SOURCE_LABEL = "flickr.people.getPublicPhotos"

# Full public JSON record set for the chosen account. Each record matches the
# pre-existing art.html embedded-gallery schema; license/date_upload are the
# additive freshness fields this sync introduces.
RECORD_FIELDS = (
    "id",
    "title",
    "desc",
    "tags",
    "date",
    "views",
    "media",
    "thumb",
    "flickr_url",
    "sizes",
    "license",
    "license_name",
    "license_url",
    "date_upload",
)

# Top-level key order of the export (generated_at is None on a fresh payload).
EXPORT_KEYS = ("generated_at", "source", "count", "artworks")
DATE_UPLOAD_FORMAT = "%Y-%m-%d %H:%M:%S"
# Fixed-width, ASCII-digit shape of ``date_upload``. ``strptime`` alone accepts
# non-zero-padded fields and non-ASCII digits, and the sort check compares the
# strings lexicographically, so the shape is enforced first and ``strptime`` is
# kept only for calendar validity (month 13, day 40).
DATE_UPLOAD_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
# Record fields that change on Flickr without any editorial change; they are
# excluded from the --check-drift comparison (the write path still stores them).
DRIFT_IGNORED_FIELDS = ("views",)
# Cap on listed ids/messages in human-readable reports.
REPORT_LIST_LIMIT = 10


class FlickrSyncError(RuntimeError):
    """Raised when the live fetch is unusable (missing key, API error, drift guard)."""


def redact_url(url: str) -> str:
    """The request URL with its ``api_key`` value masked, for messages and logs."""
    parts = urllib.parse.urlsplit(url)
    query = [(key, "REDACTED" if key == "api_key" else value) for key, value in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)]
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))


def api_url(method: str, api_key: str, **params: object) -> str:
    query = {"method": method, "api_key": api_key, "format": "json", "nojsoncallback": "1"}
    query.update(params)
    return f"{FLICKR_REST}?{urllib.parse.urlencode(query)}"


def fetch_json(url: str, *, attempts: int = 3, timeout: float = 30.0) -> dict:
    """GET one Flickr REST response as JSON with bounded retries."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "docxology-art-sync/1.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:  # noqa: RSE102
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
            continue
        if payload.get("stat") == "fail":
            code = payload.get("code")
            message = payload.get("message", "unknown Flickr error")
            raise FlickrSyncError(f"Flickr API error {code}: {message}")
        return payload
    raise FlickrSyncError(f"Flickr fetch failed after {attempts} attempts: {redact_url(url)} ({last_error})")


def fetch_license_map(api_key: str) -> dict[str, dict[str, str]]:
    payload = fetch_json(api_url("flickr.photos.licenses.getInfo", api_key))
    return {
        str(entry["id"]): {"name": str(entry["name"]), "url": str(entry["url"])}
        for entry in payload.get("licenses", {}).get("license", [])
    }


def fetch_public_photos(api_key: str) -> tuple[list[dict], int]:
    """Return every public photo record plus Flickr's public total.

    The total comes from the first page, which must state one: without it the
    short-fetch gate in ``sync()`` could not tell a truncated listing from a
    complete one.  A later page may raise the known total but never lower it.
    """
    photos: list[dict] = []
    page = 1
    total = 0
    while True:
        payload = fetch_json(
            api_url(
                "flickr.people.getPublicPhotos",
                api_key,
                user_id=FLICKR_NSID,
                per_page=PHOTOS_PER_PAGE,
                page=page,
                extras=EXTRAS,
            )
        )
        envelope = payload.get("photos")
        if not isinstance(envelope, dict):
            envelope = {}
        try:
            page_total = int(envelope["total"])
        except (KeyError, TypeError, ValueError):
            if page == 1:
                raise FlickrSyncError("Flickr's first photo page states no usable total; refusing an unverifiable listing")
            page_total = total
        total = max(total, page_total)
        batch = envelope.get("photo", [])
        if not isinstance(batch, list):
            batch = []
        photos.extend(batch)
        try:
            pages = int(envelope.get("pages", 1))
        except (TypeError, ValueError):
            pages = page
        if page >= pages or not batch:
            break
        page += 1
    return photos, total


def fetch_size_maps(api_key: str, photo_ids: list[str]) -> dict[str, dict[str, str]]:
    """Fetch ``flickr.photos.getSizes`` for each photo, preserving input order.

    Size labels are exactly the keys the gallery already consumes ("Medium 640",
    "Large 1600", ...). A photo that returns no sizes contributes an empty map
    rather than aborting the refresh — the gallery falls back to ``thumb``.
    """

    def one(photo_id: str) -> tuple[str, dict[str, str]]:
        payload = fetch_json(api_url("flickr.photos.getSizes", api_key, photo_id=photo_id))
        sizes: dict[str, str] = {}
        for size in payload.get("sizes", {}).get("size", []):
            label = str(size.get("label", "")).strip()
            source = str(size.get("source", "")).strip()
            if label and source.startswith("https://"):
                sizes[label] = source
        return photo_id, sizes

    maps: dict[str, dict[str, str]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for photo_id, sizes in pool.map(one, photo_ids):
            maps[photo_id] = sizes
    return maps


def epoch_to_datetime(epoch: object) -> str:
    """Unix-epoch string (Flickr ``dateupload``) to UTC 'YYYY-MM-DD HH:MM:SS'."""
    try:
        seconds = int(str(epoch))
    except (TypeError, ValueError):
        return ""
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def clean_tags(raw: object) -> list[str]:
    """Flickr's ``tags`` extra (space-delimited clean tokens) -> ordered unique tags.

    The ``tags`` extra is already the clean form (lowercase, spaces and
    punctuation stripped), so a quoted multiword Flickr tag such as
    "summer solstice" arrives as the single token ``summersolstice``; splitting
    on whitespace therefore never fragments a tag. These tokens are the
    matching key for collections, related works and gallery search, which is why
    they are not replaced by raw display forms. If Flickr reports two raw tags
    that clean to the same token, the duplicate is dropped (first wins).
    """
    seen: set[str] = set()
    tags: list[str] = []
    for tag in str(raw or "").split():
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def build_record(photo: dict, sizes: dict[str, str], license_map: dict[str, dict[str, str]]) -> dict:
    photo_id = str(photo["id"])
    license_code = str(photo.get("license", "0"))
    license_entry = license_map.get(license_code, {})
    record = {
        "id": photo_id,
        "title": html.unescape(str(photo.get("title", ""))).strip(),
        # Unescaped exactly once: a description that literally contains an
        # escaped entity ("&amp;amp;") keeps it ("&amp;") rather than being over-decoded.
        "desc": html.unescape(str(photo.get("description", {}).get("_content", ""))),
        "tags": clean_tags(photo.get("tags", "")),
        "date": str(photo.get("datetaken", "")).strip(),
        "views": str(photo.get("views", "0") or "0"),
        "media": str(photo.get("media", "photo")),
        "thumb": str(photo.get("url_m", "")),
        "flickr_url": f"https://www.flickr.com/photos/{FLICKR_NSID}/{photo_id}",
        "sizes": sizes,
        "license": license_code,
        "license_name": license_entry.get("name", ""),
        "license_url": license_entry.get("url", ""),
        "date_upload": epoch_to_datetime(photo.get("dateupload")),
    }
    return {field: record[field] for field in RECORD_FIELDS}


def build_payload(photos: list[dict], size_maps: dict[str, dict[str, str]], license_map: dict[str, dict[str, str]]) -> dict:
    records = [build_record(photo, size_maps.get(str(photo["id"]), {}), license_map) for photo in photos]
    records.sort(key=lambda record: (record["date_upload"], record["id"]), reverse=True)
    return {
        "generated_at": None,  # filled by write/check below via stable_generated_at
        "source": SOURCE_LABEL,
        "count": len(records),
        "artworks": records,
    }


def payload_body(payload: dict) -> str:
    """Serialized body without the volatile ``generated_at`` stamp."""
    body = dict(payload)
    body.pop("generated_at", None)
    return json.dumps(body, indent=2, ensure_ascii=False, sort_keys=False)


def render(payload: dict, *, existing_generated_at: str | None) -> str:
    stamp = existing_generated_at
    if stamp is None:
        body = dict(payload)
        body["generated_at"] = ""
        stamp = stable_generated_at(OUTPUT, body) or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        # stable_generated_at only reuses a timestamp when the body matches the
        # file; a fresh body gets today's date, matching other generated exports.
    final = dict(payload)
    final["generated_at"] = stamp
    return json.dumps(final, indent=2, ensure_ascii=False) + "\n"


def on_disk_payload() -> dict | None:
    """The checked-in export as parsed JSON (``None`` when the file is absent)."""
    if not OUTPUT.exists():
        return None
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FlickrSyncError(f"{OUTPUT} is not valid JSON: {exc}") from exc


def on_disk_body() -> str | None:
    payload = on_disk_payload()
    return payload_body(payload) if isinstance(payload, dict) else None


def export_shape_problem(payload: object) -> str | None:
    """Why ``payload`` cannot serve as the previous export, or ``None`` when its shape is usable.

    A usable previous export is a JSON object whose ``artworks`` is a list.
    This is deliberately weaker than ``validate_export``: the previous file is
    only a comparison baseline (coverage delta, drift), and a file that fails
    full validation but has this shape is still diffed record by record.
    """
    if not isinstance(payload, dict):
        return "export is not a JSON object"
    if not isinstance(payload.get("artworks"), list):
        return "artworks is not a list"
    return None


def drift_body(payload: dict) -> str:
    """``payload_body`` with ``DRIFT_IGNORED_FIELDS`` masked on every record.

    Two payloads with equal drift bodies differ at most in volatile fields
    (today only Flickr's ``views`` counter), which must not fail the drift gate.
    """
    body = dict(payload)
    body.pop("generated_at", None)
    if isinstance(body.get("artworks"), list):
        body["artworks"] = [
            {key: value for key, value in record.items() if key not in DRIFT_IGNORED_FIELDS}
            if isinstance(record, dict)
            else record
            for record in body["artworks"]
        ]
    return json.dumps(body, indent=2, ensure_ascii=False, sort_keys=False)


def _records_by_id(payload: object) -> dict[str, dict]:
    """Records keyed by ``str(id)``; any malformed payload shape yields ``{}``."""
    records = payload.get("artworks") if isinstance(payload, dict) else None
    if not isinstance(records, list):
        return {}
    return {
        str(record["id"]): record
        for record in records
        if isinstance(record, dict) and "id" in record
    }


def _id_order(photo_id: str) -> tuple[int, str]:
    """Numeric-string ordering for ids (shorter first, then lexicographic)."""
    return (len(photo_id), photo_id)


def _newest_first(ids, records: dict[str, dict]) -> list[str]:
    """Order ids newest first: ``date_upload`` descending, then id descending.

    ``records`` maps id -> record for the side the ids belong to. An id without
    a usable ``date_upload`` (record or field missing) sorts as the oldest, so
    when no records are available at all the order is id descending.
    """

    def key(photo_id: str) -> tuple[str, tuple[int, str]]:
        record = records.get(photo_id)
        upload = record.get("date_upload") if isinstance(record, dict) else None
        return (upload if isinstance(upload, str) else "", _id_order(photo_id))

    return sorted(ids, key=key, reverse=True)


def classify_drift(current: object, live: dict) -> tuple[str, list[str]]:
    """Compare the checked-in export with a live payload.

    Returns ``(status, details)``: ``"up-to-date"`` (identical bodies),
    ``"views-only"`` (differs only in ``DRIFT_IGNORED_FIELDS``; informational,
    not drift) or ``"stale"`` (``details`` says what changed).
    """
    if current is None:
        return "stale", ["data/artworks.json missing"]
    problem = export_shape_problem(current)
    if problem:
        return "stale", [f"data/artworks.json is malformed ({problem})"]
    if payload_body(current) == payload_body(live):
        return "up-to-date", []
    current_records = _records_by_id(current)
    live_records = _records_by_id(live)
    if drift_body(current) == drift_body(live):
        changed = sum(
            1
            for photo_id, record in live_records.items()
            if photo_id in current_records and record.get("views") != current_records[photo_id].get("views")
        )
        return "views-only", [f"views changed on {changed} records"]
    added = _newest_first(set(live_records) - set(current_records), live_records)
    removed = _newest_first(set(current_records) - set(live_records), current_records)
    details = []
    if added:
        details.append(f"added {len(added)} (newest: {added[:3]})")
    if removed:
        details.append(f"removed {len(removed)}")
    if not added and not removed:
        details.append("record content changed")
    return "stale", details


def _record_label(record: dict, index: int) -> str:
    photo_id = record.get("id")
    return f"record {photo_id}" if isinstance(photo_id, str) and photo_id else f"artworks[{index}]"


def _record_errors(record: dict, label: str) -> list[str]:
    """Structural errors of one export record (see ``validate_export``)."""
    errors: list[str] = []
    keys = tuple(record)
    if keys != RECORD_FIELDS:
        missing = [field for field in RECORD_FIELDS if field not in record]
        unexpected = [field for field in keys if field not in RECORD_FIELDS]
        if missing or unexpected:
            errors.append(f"{label}: fields differ from RECORD_FIELDS (missing {missing}, unexpected {unexpected})")
        else:
            errors.append(f"{label}: fields are not in RECORD_FIELDS order {list(keys)}")

    photo_id = record.get("id")
    if not isinstance(photo_id, str) or not re.fullmatch(r"[0-9]+", photo_id):
        errors.append(f"{label}: id {photo_id!r} is not a numeric string")

    for field in ("title", "desc", "date", "views", "media", "license", "license_name", "license_url"):
        if field in record and not isinstance(record[field], str):
            errors.append(f"{label}: {field} is not a string")

    tags = record.get("tags")
    if not isinstance(tags, list):
        errors.append(f"{label}: tags is not a list")
    else:
        for tag in tags:
            if not isinstance(tag, str) or not tag:
                errors.append(f"{label}: tag {tag!r} is not a non-empty string")
            elif tag != "".join(tag.split()):
                errors.append(f"{label}: tag {tag!r} contains whitespace")
        duplicates = sorted({tag for tag in tags if isinstance(tag, str) and tags.count(tag) > 1})
        if duplicates:
            errors.append(f"{label}: duplicate tags {duplicates}")

    expected_url = f"https://www.flickr.com/photos/{FLICKR_NSID}/{photo_id}"
    if record.get("flickr_url") != expected_url:
        errors.append(f"{label}: flickr_url {record.get('flickr_url')!r} != {expected_url!r}")

    thumb = record.get("thumb")
    if not isinstance(thumb, str) or not thumb.startswith("https://"):
        errors.append(f"{label}: thumb {thumb!r} is not an https URL")

    sizes = record.get("sizes")
    if not isinstance(sizes, dict):
        errors.append(f"{label}: sizes is not an object")
    else:
        for size_label, source in sizes.items():
            if not isinstance(source, str) or not source.startswith("https://"):
                errors.append(f"{label}: sizes[{size_label!r}] {source!r} is not an https URL")

    date_upload = record.get("date_upload")
    try:
        if not isinstance(date_upload, str) or not DATE_UPLOAD_RE.fullmatch(date_upload):
            raise ValueError("not a fixed-width ASCII timestamp")
        datetime.strptime(date_upload, DATE_UPLOAD_FORMAT)
    except ValueError:
        errors.append(f"{label}: date_upload {date_upload!r} is not YYYY-MM-DD HH:MM:SS")
    return errors


def validate_export(payload: object) -> list[str]:
    """Offline structural validation of an artwork export; ``[]`` when sound.

    Checks the top-level key order (``generated_at``, ``source``, ``count``,
    ``artworks``), ``count == len(artworks)``, unique numeric-string ids, that
    every record's key tuple is exactly ``RECORD_FIELDS``, that tags are
    non-empty, whitespace-free and unique, the canonical ``flickr_url``, https
    ``thumb``/``sizes`` URLs, ``date_upload`` as ``YYYY-MM-DD HH:MM:SS``, and
    that records are sorted by ``(date_upload, id)`` descending. No network and
    no completeness policy: untagged or undescribed records are valid here
    (see ``coverage_summary`` / ``--require-complete`` for that).
    """
    if not isinstance(payload, dict):
        return ["export is not a JSON object"]
    errors: list[str] = []
    if list(payload) != list(EXPORT_KEYS):
        errors.append(f"top-level keys {list(payload)} != {list(EXPORT_KEYS)}")
    if payload.get("source") != SOURCE_LABEL:
        errors.append(f"source {payload.get('source')!r} != {SOURCE_LABEL!r}")
    stamp = payload.get("generated_at")
    if stamp is not None and not isinstance(stamp, str):
        errors.append(f"generated_at {stamp!r} is not a string")
    records = payload.get("artworks")
    if not isinstance(records, list):
        errors.append("artworks is not a list")
        return errors
    if payload.get("count") != len(records):
        errors.append(f"count {payload.get('count')!r} != len(artworks) {len(records)}")

    seen: set[str] = set()
    sortable: list[tuple[str, str]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"artworks[{index}]: not an object")
            continue
        label = _record_label(record, index)
        photo_id = record.get("id")
        if isinstance(photo_id, str):
            if photo_id in seen:
                errors.append(f"{label}: duplicate id")
            seen.add(photo_id)
        errors.extend(_record_errors(record, label))
        if isinstance(photo_id, str) and isinstance(record.get("date_upload"), str):
            sortable.append((record["date_upload"], photo_id))

    for earlier, later in zip(sortable, sortable[1:]):
        if earlier < later:
            errors.append(
                "records are not sorted by (date_upload, id) descending: "
                f"{earlier[1]} ({earlier[0]}) precedes {later[1]} ({later[0]})"
            )
            break
    return errors


def _mix(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _tag_list(record: dict) -> list:
    """The record's ``tags`` when it is a list, else ``[]`` (``validate_export`` reports the defect)."""
    tags = record.get("tags")
    return tags if isinstance(tags, list) else []


def coverage_summary(payload: dict, *, flickr_total: int | None = None, previous: dict | None = None) -> dict:
    """Tag/description coverage of an export, optionally versus Flickr and the last export.

    Pure and JSON-serializable. ``short_desc`` counts plain-text descriptions
    shorter than ``THIN_DESCRIPTION_CHARS`` (empty ones included); ``thin`` is
    the site's ``is_thin`` policy (no tags AND a short description);
    ``tags_with_whitespace`` counts tag tokens containing whitespace and must be
    0. ``vs_previous`` (``None`` without ``previous``) lists ids added/removed
    and ids whose ``tags`` / ``desc`` differ from ``previous``, each newest
    first (``date_upload`` descending, then id descending) so the truncated
    report shows the most recent ids. ``previous`` of any malformed shape
    contributes no records rather than raising.
    """
    artworks = payload.get("artworks") if isinstance(payload, dict) else None
    records = [record for record in artworks if isinstance(record, dict)] if isinstance(artworks, list) else []
    tag_counts = [len(_tag_list(record)) for record in records]
    plain = [plain_text(record.get("desc", "")) for record in records]
    summary: dict = {
        "count": len(records),
        "flickr_total": flickr_total,
        "total_mismatch": flickr_total is not None and flickr_total != len(records),
        "untagged": sum(1 for record in records if not record.get("tags")),
        "untagged_ids": [str(record.get("id")) for record in records if not record.get("tags")],
        "empty_desc": sum(1 for text in plain if not text),
        "empty_desc_ids": [str(record.get("id")) for record, text in zip(records, plain) if not text],
        "short_desc": sum(1 for text in plain if len(text) < THIN_DESCRIPTION_CHARS),
        "thin": sum(1 for record in records if is_thin(record)),
        "tags_with_whitespace": sum(
            1
            for record in records
            for tag in _tag_list(record)
            if not isinstance(tag, str) or tag != "".join(tag.split())
        ),
        "tags_per_record": {
            "min": min(tag_counts, default=0),
            "mean": round(sum(tag_counts) / len(tag_counts), 1) if tag_counts else 0.0,
            "max": max(tag_counts, default=0),
        },
        "licenses": _mix(
            [
                f"{record.get('license', '')} {record.get('license_name', '')}".strip()
                for record in records
            ]
        ),
        "media": _mix([str(record.get("media", "")) for record in records]),
        "vs_previous": None,
    }
    if previous is not None:
        before = _records_by_id(previous)
        now = _records_by_id({"artworks": records})
        shared = _newest_first(set(before) & set(now), now)
        summary["vs_previous"] = {
            "added": _newest_first(set(now) - set(before), now),
            "removed": _newest_first(set(before) - set(now), before),
            "tags_changed": [i for i in shared if before[i].get("tags") != now[i].get("tags")],
            "desc_changed": [i for i in shared if before[i].get("desc") != now[i].get("desc")],
        }
    return summary


def completeness_problems(summary: dict) -> list[str]:
    """Why a coverage summary fails ``--require-complete`` (``[]`` when complete)."""
    problems = []
    if summary["untagged"]:
        problems.append(f"{summary['untagged']} untagged records")
    if summary["empty_desc"]:
        problems.append(f"{summary['empty_desc']} records with an empty description")
    return problems


def _ids_note(ids: list[str]) -> str:
    if not ids:
        return ""
    shown = ", ".join(ids[:REPORT_LIST_LIMIT])
    more = f" (+{len(ids) - REPORT_LIST_LIMIT} more)" if len(ids) > REPORT_LIST_LIMIT else ""
    return f" [{shown}{more}]"


def format_coverage(summary: dict) -> str:
    """Human-readable multi-line rendering of ``coverage_summary``."""
    total = summary["flickr_total"]
    if total is None:
        total_note = ""
    elif summary["total_mismatch"]:
        total_note = f" (Flickr public total {total}: MISMATCH of {summary['count'] - total:+d})"
    else:
        total_note = f" (matches Flickr public total {total})"
    tags = summary["tags_per_record"]
    lines = [
        "flickr artwork coverage:",
        f"  artworks            {summary['count']}{total_note}",
        f"  untagged            {summary['untagged']}{_ids_note(summary['untagged_ids'])}",
        f"  empty description   {summary['empty_desc']}{_ids_note(summary['empty_desc_ids'])}",
        f"  short description   {summary['short_desc']} (< {THIN_DESCRIPTION_CHARS} plain chars, empty included)",
        f"  thin pages          {summary['thin']} (no tags and a short description)",
        f"  tags w/ whitespace  {summary['tags_with_whitespace']} (must be 0)",
        f"  tags per record     min {tags['min']} / mean {tags['mean']} / max {tags['max']}",
        "  licenses            " + ", ".join(f"{label}: {n}" for label, n in summary["licenses"].items()),
        "  media               " + ", ".join(f"{label}: {n}" for label, n in summary["media"].items()),
    ]
    delta = summary["vs_previous"]
    if delta is not None:
        lines.append(
            f"  vs checked-in       +{len(delta['added'])} added, -{len(delta['removed'])} removed, "
            f"{len(delta['tags_changed'])} tags changed, {len(delta['desc_changed'])} descriptions changed"
        )
        for key, label in (
            ("added", "added ids"),
            ("removed", "removed ids"),
            ("tags_changed", "tags changed"),
            ("desc_changed", "desc changed"),
        ):
            if delta[key]:
                lines.append(f"    {label}:{_ids_note(delta[key])}")
    return "\n".join(lines)


def _validation_failure(errors: list[str]) -> FlickrSyncError:
    shown = errors[: REPORT_LIST_LIMIT * 2]
    more = f"\n  ... and {len(errors) - len(shown)} more" if len(errors) > len(shown) else ""
    return FlickrSyncError(
        f"live export failed validation ({len(errors)} errors); nothing written:\n  " + "\n  ".join(shown) + more
    )


def _previous_export() -> tuple[dict | None, str | None]:
    """The checked-in export as a usable comparison baseline: ``(previous, problem)``.

    ``problem`` is set (and ``previous`` is ``None``) when the file exists but
    is not an object with an ``artworks`` list; the caller decides whether that
    is a warning (sync/dry-run) or drift (``--check-drift``). Unparseable JSON
    still raises ``FlickrSyncError`` from ``on_disk_payload``.
    """
    previous = on_disk_payload()
    if previous is None:
        return None, None
    problem = export_shape_problem(previous)
    if problem:
        return None, problem
    return previous, None


def _count_mismatch_gate(count: int, total: int, *, allow: bool) -> None:
    """Refuse a live fetch that returned fewer public photos than Flickr's own total.

    ``total`` comes from the same ``getPublicPhotos`` query, so a shortfall
    means the pagination was cut short (for example an empty page mid-way), not
    that non-public photos are being counted. Writing that export would drop
    real artworks and a later ``--prune-owned`` would delete their pages. A
    higher fetched count (photos added mid-fetch) stays a warning.
    """
    if count > total:
        print(f"warning: fetched {count} public photos but Flickr reports total {total}", file=sys.stderr)
    elif count < total:
        message = f"fetched {count} public photos but Flickr's public total is {total} ({count - total:+d})"
        if not allow:
            raise FlickrSyncError(
                f"{message}; the fetch looks truncated, so nothing is written "
                "(re-run, or pass --allow-count-mismatch to accept this count)"
            )
        print(f"warning: {message}; continuing because --allow-count-mismatch was passed", file=sys.stderr)


def sync(
    api_key: str,
    *,
    write: bool,
    check_drift: bool,
    require_complete: bool = False,
    allow_count_mismatch: bool = False,
) -> int:
    photos, total = fetch_public_photos(api_key)
    if not photos:
        raise FlickrSyncError("Flickr returned zero public photos")
    # Checked before the per-photo getSizes fan-out: a truncated fetch is
    # unusable in every mode, so do not spend one request per photo on it.
    _count_mismatch_gate(len(photos), total, allow=allow_count_mismatch)
    license_map = fetch_license_map(api_key)
    size_maps = fetch_size_maps(api_key, [str(photo["id"]) for photo in photos])
    payload = build_payload(photos, size_maps, license_map)
    errors = validate_export(payload)
    if errors:
        raise _validation_failure(errors)
    previous, previous_problem = _previous_export()
    if previous_problem and not check_drift:
        print(
            f"warning: {OUTPUT.relative_to(REPO_ROOT)} is malformed ({previous_problem}); "
            "comparing against no previous export",
            file=sys.stderr,
        )
    summary = coverage_summary(payload, flickr_total=total, previous=previous)
    incomplete = completeness_problems(summary) if require_complete else []

    if check_drift:
        if previous_problem:
            raise FlickrSyncError(
                f"artworks.json is stale vs Flickr: data/artworks.json is malformed ({previous_problem})"
            )
        if incomplete:
            print(format_coverage(summary), file=sys.stderr)
            raise FlickrSyncError("export is incomplete (--require-complete): " + "; ".join(incomplete))
        status, details = classify_drift(previous, payload)
        if status == "up-to-date":
            print(f"checked flickr artwork export (up to date, {payload['count']} artworks)")
            return 0
        if status == "views-only":
            print(
                f"checked flickr artwork export (up to date, {payload['count']} artworks; "
                f"informational: {'; '.join(details)}, ignored by the drift gate)"
            )
            return 0
        raise FlickrSyncError("artworks.json is stale vs Flickr: " + "; ".join(details))

    print(format_coverage(summary))
    if incomplete:
        raise FlickrSyncError("export is incomplete (--require-complete): " + "; ".join(incomplete) + "; nothing written")
    if not write:
        print(f"dry run: {payload['count']} artworks; not writing {OUTPUT.relative_to(REPO_ROOT)}")
        return 0

    stamp = None
    if previous is not None and payload_body(payload) == payload_body(previous):
        stamp = str(previous.get("generated_at", "")) or None
    OUTPUT.write_text(render(payload, existing_generated_at=stamp), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({payload['count']} artworks)")
    return 0


def coverage_local(*, require_complete: bool = False) -> int:
    """Offline: validate and summarize the checked-in export (no network, no API key)."""
    payload = on_disk_payload()
    if payload is None:
        raise FlickrSyncError(f"{OUTPUT.relative_to(REPO_ROOT)} does not exist")
    errors = validate_export(payload)
    if errors:
        # The coverage summary assumes a structurally sound export, so a broken
        # one reports only the validator's messages.
        print(f"validate_export: {len(errors)} errors in {OUTPUT.relative_to(REPO_ROOT)}", file=sys.stderr)
        for message in errors[: REPORT_LIST_LIMIT * 2]:
            print(f"  {message}", file=sys.stderr)
        if len(errors) > REPORT_LIST_LIMIT * 2:
            print(f"  ... and {len(errors) - REPORT_LIST_LIMIT * 2} more", file=sys.stderr)
        return 1
    print(f"validate_export: ok ({OUTPUT.relative_to(REPO_ROOT)})")
    summary = coverage_summary(payload)
    print(format_coverage(summary))
    incomplete = completeness_problems(summary) if require_complete else []
    if incomplete:
        raise FlickrSyncError("export is incomplete (--require-complete): " + "; ".join(incomplete))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Fetch and summarize without writing")
    parser.add_argument(
        "--check-drift",
        action="store_true",
        help="Exit nonzero when the checked-in export differs from live (CI gate; views are ignored)",
    )
    parser.add_argument(
        "--coverage-local",
        action="store_true",
        help="Offline: validate and summarize the checked-in data/artworks.json (no API key needed)",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Exit nonzero (writing nothing) when any record is untagged or has an empty description",
    )
    parser.add_argument(
        "--allow-count-mismatch",
        action="store_true",
        help=(
            "Proceed when the fetched public photo count is LOWER than Flickr's public total "
            "from the same query (default: refuse, writing nothing; a higher count only warns)"
        ),
    )
    args = parser.parse_args()
    if args.coverage_local and (args.dry_run or args.check_drift or args.allow_count_mismatch):
        parser.error(
            "--coverage-local is offline and cannot be combined with --dry-run, --check-drift "
            "or --allow-count-mismatch"
        )
    try:
        if args.coverage_local:
            raise SystemExit(coverage_local(require_complete=args.require_complete))
        api_key = os.environ.get("FLICKR_API_KEY", "")
        if not api_key:
            raise SystemExit(
                "FLICKR_API_KEY is not set. Create a non-commercial Flickr API key at "
                "https://www.flickr.com/services/apps/create/ and export it in the shell; "
                "never commit the key. CI maps it to the FLICKR_API_KEY repository secret. "
                "Use --coverage-local for the offline report."
            )
        raise SystemExit(
            sync(
                api_key,
                write=not (args.dry_run or args.check_drift),
                check_drift=args.check_drift,
                require_complete=args.require_complete,
                allow_count_mismatch=args.allow_count_mismatch,
            )
        )
    except FlickrSyncError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
