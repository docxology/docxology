#!/usr/bin/env python3
"""Emit IndexNow URL list from sitemap index-priority policy."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from submit_indexnow import indexnow_urls  # noqa: E402


def main() -> None:
    for url in indexnow_urls():
        print(url)


if __name__ == "__main__":
    main()
