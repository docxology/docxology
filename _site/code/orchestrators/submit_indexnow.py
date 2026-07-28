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
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from build_sitemap import sitemap_locs  # noqa: E402
from sitemap_policy import SITE_ORIGIN, indexnow_urls_from_locs  # noqa: E402

DEFAULT_KEY_FILE = REPO_ROOT / "a3f7c1b8d4e9426b8f2c5a7d9e3f1b6c.txt"
INDEXNOW_API = "https://api.indexnow.org/indexnow"


def indexnow_urls() -> list[str]:
    return indexnow_urls_from_locs(sitemap_locs())


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit index-priority URLs to IndexNow.")
    parser.add_argument("--key-file", type=Path, default=DEFAULT_KEY_FILE)
    parser.add_argument("--list-urls", action="store_true", help="Print IndexNow URL list and exit.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    urls = indexnow_urls()
    if args.list_urls:
        for url in urls:
            print(url)
        return 0

    key = load_key(args.key_file)
    return submit_bulk(urls, key, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
