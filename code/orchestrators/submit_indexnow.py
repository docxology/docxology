#!/usr/bin/env python3
"""Submit index-priority URLs to IndexNow (Bing, Yandex, Naver).

Uses the same URL list as `.github/workflows/indexnow-on-push.yml`.
Google Search Console sitemap / URL inspection still requires manual GSC login.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from build_sitemap import sitemap_locs  # noqa: E402
from sitemap_policy import SITE_ORIGIN, indexnow_urls_from_locs  # noqa: E402

DEFAULT_KEY_FILE = REPO_ROOT / "a3f7c1b8d4e9426b8f2c5a7d9e3f1b6c.txt"
INDEXNOW_API = "https://api.indexnow.org/indexnow"

# GSC manual follow-up priority set (also bulk-submitted here).
GSC_PRIORITY_URLS: list[str] = [
    SITE_ORIGIN,
    f"{SITE_ORIGIN}exports.html",
    f"{SITE_ORIGIN}catalog.html",
    f"{SITE_ORIGIN}cite-verify.html",
    f"{SITE_ORIGIN}discovery.html",
    f"{SITE_ORIGIN}publications.html",
]


def load_key(path: Path) -> str:
    key = path.read_text(encoding="utf-8").strip()
    if not key:
        raise SystemExit(f"empty IndexNow key file: {path}")
    return key


def key_location(key: str) -> str:
    return f"{SITE_ORIGIN}{key}.txt" if len(key) == 32 else f"{SITE_ORIGIN}a3f7c1b8d4e9426b8f2c5a7d9e3f1b6c.txt"


def submit_bulk(urls: list[str], key: str, dry_run: bool) -> int:
    if not urls:
        return 0
    body = json.dumps(
        {
            "host": "danielarifriedman.com",
            "key": key,
            "keyLocation": key_location(key),
            "urlList": urls,
        }
    ).encode()
    if dry_run:
        print(f"dry-run bulk POST {len(urls)} urls")
        return 0
    req = urllib.request.Request(
        INDEXNOW_API,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            print(f"bulk {response.status} ({len(urls)} urls)")
            return 0 if response.status in (200, 202) else 1
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        print(f"bulk error {exc.code}: {detail}", file=sys.stderr)
        return 1


def submit_per_url(urls: list[str], key: str, dry_run: bool) -> tuple[int, int]:
    ok = fail = 0
    for url in urls:
        if dry_run:
            ok += 1
            continue
        query = urllib.parse.urlencode({"url": url, "key": key})
        req = urllib.request.Request(f"{INDEXNOW_API}?{query}")
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status in (200, 202):
                    ok += 1
                else:
                    fail += 1
                    print(f"per-url {response.status} {url}", file=sys.stderr)
        except urllib.error.HTTPError as exc:
            fail += 1
            print(f"per-url {exc.code} {url}", file=sys.stderr)
        except urllib.error.URLError as exc:
            fail += 1
            print(f"per-url error {url}: {exc.reason}", file=sys.stderr)
    return ok, fail


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit index-priority URLs to IndexNow.")
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY_FILE)
    parser.add_argument(
        "--priority-only",
        action="store_true",
        help="Bulk-submit GSC priority URLs only (skip per-URL pass).",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    key = load_key(args.key_file)
    all_urls = indexnow_urls_from_locs(sitemap_locs())

    bulk_rc = submit_bulk(GSC_PRIORITY_URLS, key, args.dry_run)
    if args.priority_only:
        return bulk_rc

    ok, fail = submit_per_url(all_urls, key, args.dry_run)
    print(f"per-url ok={ok} fail={fail} total={ok + fail}")
    return bulk_rc or (1 if fail else 0)


if __name__ == "__main__":
    raise SystemExit(main())
