#!/usr/bin/env python3
"""Generate a lightweight size audit for public assets and data exports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report

OUT = dated_report_path("asset_size", "json")

PATTERNS = [
    ("html", "*.html", 500_000),
    ("og-image", "og-*.jpg", 220_000),
    ("json-data", "data/*.json", 4_000_000),
    ("resume-export", "resume/*.txt", 1_000_000),
    ("resume-export", "resume/*.pdf", 5_000_000),
    ("citation-export", "bibliography.*", 4_000_000),
    ("site-runtime", "sw.js", 50_000),
    ("site-runtime", "manifest.json", 50_000),
    ("site-runtime", "style.css", 250_000),
    ("hero-art", "assets/hero-art/*.webp", 320_000),
]


def iter_assets() -> list[dict]:
    assets = []
    for kind, pattern, budget in PATTERNS:
        for path in sorted(REPO_ROOT.glob(pattern)):
            if not path.is_file():
                continue
            size = path.stat().st_size
            assets.append(
                {
                    "path": str(path.relative_to(REPO_ROOT)),
                    "kind": kind,
                    "bytes": size,
                    "budget_bytes": budget,
                    "ok": size <= budget,
                }
            )
    return assets


def existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def render(generated_at: str | None = None) -> str:
    assets = iter_assets()
    warnings = [item for item in assets if not item["ok"]]
    payload = {
        "generated_at": generated_at or generated_timestamp(),
        "scope": "Public root HTML, Open Graph images, data exports, citation exports, and site runtime assets. Visual QA screenshots are excluded.",
        "asset_count": len(assets),
        "warnings": len(warnings),
        "total_bytes": sum(item["bytes"] for item in assets),
        "largest": sorted(assets, key=lambda item: item["bytes"], reverse=True)[:20],
        "over_budget": warnings,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the asset-size report is stale")
    args = parser.parse_args()
    out = latest_report("asset_size_*.json") if args.check else OUT
    content = render(existing_generated_at(out) if args.check else None)
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale asset-size report")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
    payload = json.loads(content)
    print(("checked" if args.check else "wrote") + f" asset-size report ({payload['warnings']} warnings)")


if __name__ == "__main__":
    main()
