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
  the checked-in export differs from live (CI drift gate).
- Deterministic: records sort by (date_upload desc, id desc), every payload
  field is content-derived, and ``generated_at`` is reused via
  ``stable_generated_at`` when the body is unchanged (no timestamp churn).

Deliberately NOT synced here: ``width``/``height`` original dimensions. The
NEW-1 contract in ``code/tests/test_art_thumb_dimensions.py`` pins the
art-grid to CSS-pinned tile shape with no HTML dimension attributes; landing
the real per-image dims requires the conscious art.html flip documented on
that test and TODO.md, not a silent manifest field.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import os
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


class FlickrSyncError(RuntimeError):
    """Raised when the live fetch is unusable (missing key, API error, drift guard)."""


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
    raise FlickrSyncError(f"Flickr fetch failed after {attempts} attempts: {url} ({last_error})")


def fetch_license_map(api_key: str) -> dict[str, dict[str, str]]:
    payload = fetch_json(api_url("flickr.photos.licenses.getInfo", api_key))
    return {
        str(entry["id"]): {"name": str(entry["name"]), "url": str(entry["url"])}
        for entry in payload.get("licenses", {}).get("license", [])
    }


def fetch_public_photos(api_key: str) -> tuple[list[dict], int]:
    """Return every public photo record plus Flickr's public total."""
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
        envelope = payload.get("photos", {})
        try:
            total = int(envelope.get("total", len(photos)))
        except (TypeError, ValueError):
            total = len(photos)
        batch = envelope.get("photo", [])
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


def build_record(photo: dict, sizes: dict[str, str], license_map: dict[str, dict[str, str]]) -> dict:
    photo_id = str(photo["id"])
    license_code = str(photo.get("license", "0"))
    license_entry = license_map.get(license_code, {})
    description = html.unescape(str(photo.get("description", {}).get("_content", "")))
    record = {
        "id": photo_id,
        "title": html.unescape(str(photo.get("title", ""))).strip(),
        "desc": html.unescape(description),
        "tags": [tag for tag in str(photo.get("tags", "")).split() if tag],
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


def existing_generated_at() -> str | None:
    if not OUTPUT.exists():
        return None
    try:
        return str(json.loads(OUTPUT.read_text(encoding="utf-8")).get("generated_at", "")) or None
    except json.JSONDecodeError:
        return None


def on_disk_body() -> str | None:
    if not OUTPUT.exists():
        return None
    try:
        payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FlickrSyncError(f"{OUTPUT} is not valid JSON: {exc}") from exc
    payload.pop("generated_at", None)
    return json.dumps(payload, indent=2, ensure_ascii=False)


def sync(api_key: str, *, write: bool, check_drift: bool) -> int:
    photos, total = fetch_public_photos(api_key)
    if not photos:
        raise FlickrSyncError("Flickr returned zero public photos")
    license_map = fetch_license_map(api_key)
    size_maps = fetch_size_maps(api_key, [str(photo["id"]) for photo in photos])
    payload = build_payload(photos, size_maps, license_map)
    if payload["count"] != total:
        print(
            f"warning: fetched {payload['count']} public photos but Flickr reports total {total}",
            file=sys.stderr,
        )
    stamp = existing_generated_at() if payload_body(payload) == on_disk_body() else None
    text = render(payload, existing_generated_at=stamp)

    if check_drift:
        current = on_disk_body()
        if current == payload_body(payload):
            print(f"checked flickr artwork export (up to date, {payload['count']} artworks)")
            return 0
        changed = []
        if current is None:
            changed.append("data/artworks.json missing")
        else:
            changed_ids = {record["id"] for record in json.loads(current)["artworks"]}
            live_ids = {record["id"] for record in payload["artworks"]}
            added = sorted(live_ids - changed_ids)
            removed = sorted(changed_ids - live_ids)
            if added:
                changed.append(f"added {len(added)} (newest: {added[:3]})")
            if removed:
                changed.append(f"removed {len(removed)}")
            if not added and not removed:
                changed.append("record content changed")
        raise FlickrSyncError("artworks.json is stale vs Flickr: " + "; ".join(changed))

    if not write:
        print(f"dry run: {payload['count']} artworks; not writing {OUTPUT.relative_to(REPO_ROOT)}")
        return 0

    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({payload['count']} artworks)")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Fetch and summarize without writing")
    parser.add_argument(
        "--check-drift",
        action="store_true",
        help="Exit nonzero when the checked-in export differs from live (CI gate)",
    )
    args = parser.parse_args()
    api_key = os.environ.get("FLICKR_API_KEY", "")
    if not api_key:
        raise SystemExit(
            "FLICKR_API_KEY is not set. Create a non-commercial Flickr API key at "
            "https://www.flickr.com/services/apps/create/ and export it in the shell; "
            "never commit the key. CI maps it to the FLICKR_API_KEY repository secret."
        )
    try:
        raise SystemExit(sync(api_key, write=not (args.dry_run or args.check_drift), check_drift=args.check_drift))
    except FlickrSyncError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
