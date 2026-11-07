#!/usr/bin/env python3
"""Point operators from the retired Zenodo-only writer to reviewed intake."""

from __future__ import annotations

import argparse

GUIDE = "docs/operations/publication-sync.md#zenodo-only-publications"
CHECK_COMMAND = "uv run python3 code/orchestrators/check_zenodo_uncatalogued.py"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="The automatic Zenodo-only publication writer has been retired.",
        epilog=f"Discover candidates with {CHECK_COMMAND}. Review and curate them using {GUIDE}.",
        allow_abbrev=False,
    )
    parser.parse_known_args(argv)
    parser.error(
        f"automatic Zenodo-only publication writes have been retired. "
        f"Run {CHECK_COMMAND}, then follow {GUIDE}."
    )


if __name__ == "__main__":
    raise SystemExit(main())
