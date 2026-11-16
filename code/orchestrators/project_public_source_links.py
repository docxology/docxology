#!/usr/bin/env python3
"""Project newly imported repository links against the public GitHub inventory."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401
from docxology_tools.public_repository_links import source_link_outputs  # noqa: E402
from docxology_tools.generated_outputs import write_output_texts  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = source_link_outputs(ROOT)
    if args.check and outputs:
        raise SystemExit("Non-public repository links in current source projections: " + ", ".join(str(p.relative_to(ROOT)) for p in outputs))
    if not args.check:
        write_output_texts(outputs, repo_root=ROOT)
    print("checked public source links" if args.check else f"projected public source links ({len(outputs)} changed files)")


if __name__ == "__main__":
    main()
