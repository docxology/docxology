#!/usr/bin/env python3
"""Emit IndexNow URL list from sitemap index-priority policy."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from build_sitemap import sitemap_locs  # noqa: E402
from sitemap_policy import indexnow_urls_from_locs  # noqa: E402


def main() -> None:
    for url in indexnow_urls_from_locs(sitemap_locs()):
        print(url)


if __name__ == "__main__":
    main()
