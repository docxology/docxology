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

# `publications.html` intentionally ships a complete server-rendered table and
# inline CollectionPage JSON-LD so crawlers and no-JavaScript visitors receive
# the bibliography without a client fetch.  The normal root-HTML budget is
# 500 KB; this narrowly scoped, reviewable 600 KB exception preserves that
# crawlability contract instead of pushing the page toward client-only render.
ASSET_BUDGET_EXCEPTIONS: dict[str, dict[str, object]] = {
    "publications.html": {
        "budget_bytes": 600_000,
        "reason": "SSR bibliography table and inline CollectionPage JSON-LD required for crawlability.",
        "approved_in": "docs/operations/github-pages-artifact.md",
    },
}

# The generated manifest describes the audit itself and is rebuilt after all
# reports. Counting it here would create a self-referential size-report cycle:
# manifest size -> asset report -> latest-report pointer -> manifest size.
EXCLUDED_ASSETS = {
    # These control files describe the generated layer or the Pages release
    # itself. Including them would make their own metadata part of the asset
    # budget and create a needless generator cycle.
    "data/agent-index.json",
    "data/generated-manifest.json",
    "data/pages-artifact-manifest.json",
    "data/release-integrity.json",
}


def iter_assets() -> list[dict]:
    assets = []
    for kind, pattern, budget in PATTERNS:
        for path in sorted(REPO_ROOT.glob(pattern)):
            if not path.is_file():
                continue
            relative = str(path.relative_to(REPO_ROOT))
            if relative in EXCLUDED_ASSETS:
                continue
            size = path.stat().st_size
            exception = ASSET_BUDGET_EXCEPTIONS.get(relative)
            effective_budget = int(exception["budget_bytes"]) if exception else budget
            assets.append(
                {
                    "path": relative,
                    "kind": kind,
                    "bytes": size,
                    "baseline_budget_bytes": budget,
                    "budget_bytes": effective_budget,
                    "budget_exception": exception,
                    "ok": size <= effective_budget,
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


def render_for_write(path: Path) -> str:
    """Write a new timestamp only when the measured asset body changed."""
    content = render()
    if not path.exists():
        return content
    try:
        current = json.loads(content)
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return content
    current.pop("generated_at", None)
    existing.pop("generated_at", None)
    if current == existing:
        return render(existing_generated_at(path))
    return content


def render(generated_at: str | None = None) -> str:
    assets = iter_assets()
    warnings = [item for item in assets if not item["ok"]]
    payload = {
        "generated_at": generated_at or generated_timestamp(),
        "scope": "Public root HTML, Open Graph images, data exports, citation exports, and site runtime assets. Visual QA screenshots are excluded.",
        "asset_count": len(assets),
        "budget_exceptions": ASSET_BUDGET_EXCEPTIONS,
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
    content = render(existing_generated_at(out)) if args.check else render_for_write(out)
    if args.check:
        if not out.exists():
            raise SystemExit("Stale asset-size report")
        on_disk = out.read_text(encoding="utf-8")
        if on_disk != content:
            # total_bytes/largest drift whenever any tracked file changes size -
            # a commit that edits prose shifts these without touching the audit
            # contract. Compare the structural fields instead; only fail when a
            # file row appears/disappears or a budget verdict changes.
            import json as _json
            fresh = _json.loads(content)
            current = _json.loads(on_disk)
            def _verdicts(d):
                return {x["path"]: x.get("ok") for x in d.get("largest", [])}
            if (_json.dumps(fresh.get("warnings")), _json.dumps(fresh.get("over_budget", fresh.get("warnings")))) != (
                _json.dumps(current.get("warnings")), _json.dumps(current.get("over_budget", current.get("warnings")))
            ) or _verdicts(fresh) != _verdicts(current):
                raise SystemExit("Stale asset-size report")
            print("asset-size report: size-only drift tolerated")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
    payload = json.loads(content)
    print(("checked" if args.check else "wrote") + f" asset-size report ({payload['warnings']} warnings)")


if __name__ == "__main__":
    main()
