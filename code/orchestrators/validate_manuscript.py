#!/usr/bin/env python3
"""Check repository manuscript sources without rendering or writing artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401

from docxology_tools.manuscript_validation import validate_manuscript  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2], help="Repository root to inspect")
    parser.add_argument("--json", action="store_true", help="Emit structural results as JSON to stdout")
    args = parser.parse_args()
    result = validate_manuscript(args.root.absolute())
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["source_valid"]:
        print(f"Manuscript source checks passed ({len(result['sections'])} sections); rendering and publication readiness remain separate")
    else:
        print("Manuscript source checks failed:\n" + "\n".join(f"  - {error}" for error in result["errors"]))
    return 0 if result["source_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
