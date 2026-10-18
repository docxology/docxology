#!/usr/bin/env python3
"""Measure fixed backend workloads with Python 3.15; JSON diagnostics only.

Reports must be new files outside the repository. Tracing overhead is explicitly
separate from ordinary timing. No network, writers or release attestations run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools import backend_profiling  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workload", choices=backend_profiling.WORKLOADS)
    parser.add_argument("--mode", choices=("timing", "tracing"), default="timing")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180, help="Seconds per sample, including source binding (1–600)")
    parser.add_argument("--output", type=Path, help="New JSON file outside this repository; stdout always emits JSON")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.output is not None:
            if args.worker or args.output.resolve().is_relative_to(REPO_ROOT) or args.output.exists():
                raise ValueError("output must be a new external file for a parent run")
        if args.worker:
            payload = {"schema_version": backend_profiling.SCHEMA_VERSION, "ok": True,
                       "sample": backend_profiling.measure(args.workload, REPO_ROOT, args.mode)}
        else:
            payload = backend_profiling.run_samples(Path(__file__).resolve(), REPO_ROOT, args.workload,
                                                   args.mode, args.repeats, args.timeout)
        if args.output:
            backend_profiling.write_report(args.output, REPO_ROOT, payload)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        # No raw subprocess stderr/argv or absolute source paths in diagnostics.
        payload = {"schema_version": backend_profiling.SCHEMA_VERSION, "ok": False,
                   "error": "sample timed out" if isinstance(exc, subprocess.TimeoutExpired)
                   else str(exc) if isinstance(exc, ValueError) else "profiling I/O failed",
                   "validation": "not_run"}
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
