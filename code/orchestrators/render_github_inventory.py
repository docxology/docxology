#!/usr/bin/env python3
"""Render cached GitHub inventory pages without a network request.

``build_github_inventory.py`` is the explicit GitHub API refresh operation.
This companion is the deterministic derivative step: it renders
``repositories.html`` and ``repositories-forks.html`` from the already
reviewed ``data/github-repositories.json`` cache and validates byte-for-byte
drift in ``--check`` mode.
"""

from __future__ import annotations

import argparse

from build_github_inventory import check_outputs, render_cached_inventory_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if cached inventory pages differ from their deterministic render",
    )
    args = parser.parse_args()
    if args.check:
        check_outputs()
        return
    render_cached_inventory_outputs()
    print("rendered GitHub repository inventory pages from cached data")


if __name__ == "__main__":
    main()
