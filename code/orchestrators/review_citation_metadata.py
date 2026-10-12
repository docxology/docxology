#!/usr/bin/env python3
"""Write bounded Crossref review proposals; never apply or regenerate sources."""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.citation_intake import review_works  # noqa: E402
from docxology_tools.paper_artifacts import source_file  # noqa: E402
from docxology_tools.generated_outputs import safe_generated_output_path, write_generated_output_text  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Explicit report path outside source tree or under reports/")
    parser.add_argument("--citation-key", action="append", default=[], help="Repeat to select eligible Crossref works")
    args = parser.parse_args(argv)
    output = Path(os.path.abspath(args.output))
    if output.is_relative_to(REPO_ROOT) and not output.is_relative_to(REPO_ROOT / "reports"):
        parser.error("output inside repository must be under reports/; source writes are forbidden")
    try:
        output_root = REPO_ROOT if output.is_relative_to(REPO_ROOT) else output.parent
        if output_root != REPO_ROOT:
            # External reports require an explicit existing, unaliased parent.
            # The shared writer then enforces final-file custody atomically.
            for ancestor in (output_root, *output_root.parents):
                if stat.S_ISLNK(ancestor.lstat().st_mode):
                    raise ValueError(f"external report ancestor is a symlink: {ancestor}")
        safe_generated_output_path(output_root, output)
        works_path = source_file(REPO_ROOT, "data/works.json")
        if works_path is None:
            raise ValueError("eligible data/works.json is required")
        works = json.loads(works_path.read_text(encoding="utf-8"))["works"]
        report = review_works(works, REPO_ROOT, citation_keys=args.citation_key)
        write_generated_output_text(output_root, output, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Citation review failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {len(report['records'])} review records to {output}; proposals require source review")
    return 1 if any(record["status"] in {"mismatch", "unavailable"} for record in report["records"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
