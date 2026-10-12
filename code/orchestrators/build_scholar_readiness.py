#!/usr/bin/env python3
"""Generate or check the offline per-work Scholar prerequisite audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.generated_outputs import read_generated_output_text, write_output_texts  # noqa: E402
from docxology_tools.scholar_readiness import build_report, render_markdown  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare outputs without writing")
    args = parser.parse_args()
    report = build_report(REPO_ROOT)
    outputs = {
        REPO_ROOT / "data/scholar-readiness.json": json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        REPO_ROOT / "reports/scholar_readiness.md": render_markdown(report),
    }
    if args.check:
        drift = [path.relative_to(REPO_ROOT).as_posix() for path, text in outputs.items()
                 if read_generated_output_text(REPO_ROOT, path) != text]
        if drift:
            print("Scholar readiness drift: " + ", ".join(drift))
            return 1
    else:
        write_output_texts(outputs, repo_root=REPO_ROOT)
    print(f"Scholar prerequisite audit: {report['summary']['works']} works; indexing remains unverified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
