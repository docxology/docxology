#!/usr/bin/env python3
"""Render manuscript drafts with a pinned offline backend into a new review directory."""
from pathlib import Path
import argparse
import json
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.manuscript_rendering import render_manuscript  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-dir", type=Path, required=True, help="New external review directory; parent must exist")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = render_manuscript(args.root, args.output_dir)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Render failed: {exc}\n")
    print(json.dumps(result, indent=2) if args.json else "Rendered draft formats with a hash-bound receipt; human and editorial reviews remain pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
