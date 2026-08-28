#!/usr/bin/env python3
"""Render or verify all centrally declared legacy redirect stubs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from generated_outputs import (  # noqa: E402
    read_generated_output_text,
    safe_generated_output_path,
    write_generated_output_text,
)
from redirect_stubs import collect_redirect_errors, declared_stubs, render_stub  # noqa: E402


def apply(*, repo_root: Path = REPO_ROOT) -> None:
    """Write each declared redirect stub from the central renderer."""
    declarations = declared_stubs()
    # Preflight all targets before changing any legacy address.  A stale or
    # malicious later path must not leave an earlier redirect partially
    # refreshed.
    for relative in declarations:
        safe_generated_output_path(repo_root, repo_root / relative)
    for relative, stub in declarations.items():
        path = repo_root / relative
        rendered = render_stub(stub)
        actual = read_generated_output_text(repo_root, path, errors="replace")
        if actual != rendered:
            write_generated_output_text(repo_root, path, rendered)
            print(f"wrote {relative}")
        else:
            print(f"unchanged {relative}")


def check() -> None:
    """Fail closed on any missing, undeclared, or non-deterministic redirect."""
    errors = collect_redirect_errors(REPO_ROOT)
    if errors:
        raise SystemExit("Redirect stub validation failed:\n" + "\n".join(f"  - {error}" for error in errors))
    print(f"checked {len(declared_stubs())} redirect stubs")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="Write centrally rendered redirect stubs")
    mode.add_argument("--check", action="store_true", help="Fail if any redirect stub is stale or undeclared")
    args = parser.parse_args()
    if args.apply:
        apply()
    else:
        check()


if __name__ == "__main__":
    main()
