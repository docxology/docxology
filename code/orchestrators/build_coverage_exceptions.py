#!/usr/bin/env python3
"""Generate an explicit, machine-readable record of legitimate source gaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS = REPO_ROOT / "data" / "works.json"
OUT = REPO_ROOT / "data" / "coverage-exceptions.json"
REPORT_JSON = REPO_ROOT / "reports" / f"source_coverage_{datetime.now(timezone.utc).date().isoformat()}.json"
REPORT_MD = REPO_ROOT / "reports" / f"source_coverage_{datetime.now(timezone.utc).date().isoformat()}.md"


def build_payload() -> dict:
    works = json.loads(WORKS.read_text(encoding="utf-8")).get("works", [])
    exceptions = []
    for work in works:
        reasons = []
        if not work.get("has_paper_folder"):
            reasons.append("no_paper_folder")
        if not work.get("has_full_text"):
            reasons.append("no_full_text")
        if not work.get("doi"):
            reasons.append("no_doi")
        if not work.get("url"):
            reasons.append("no_canonical_url")
        if work.get("type") != "Paper":
            reasons.append("non_paper_record")
        if reasons:
            exceptions.append(
                {
                    "num": work.get("num"),
                    "citation_key": work.get("citation_key"),
                    "title": work.get("title"),
                    "type": work.get("type"),
                    "reasons": reasons,
                    "review_status": "legitimate_gap" if "non_paper_record" in reasons else "needs_review",
                    "notes": "Coverage exception is retained explicitly; do not infer that the source is missing or invalid.",
                }
            )
    summary = {reason: sum(reason in row["reasons"] for row in exceptions) for reason in (
        "no_paper_folder", "no_full_text", "no_doi", "no_canonical_url", "non_paper_record"
    )}
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "data/works.json",
        "summary": summary,
        "exceptions": exceptions,
    }


def render_report(payload: dict) -> str:
    lines = [
        "# Current Source Coverage",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "This report records legitimate bibliography coverage gaps explicitly. A gap is not evidence that a work is invalid; it identifies what is or is not available in the repository projection.",
        "",
        "## Summary",
        "",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in payload["summary"].items())
    lines.extend(["", "## Exceptions", "", "| Work | Type | Reasons | Review status |", "| --- | --- | --- | --- |"])
    for row in payload["exceptions"]:
        lines.append(f"| {row['citation_key']} | {row['type']} | {', '.join(row['reasons'])} | {row['review_status']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the generated coverage outputs are stale")
    args = parser.parse_args()
    payload = build_payload()
    if OUT.exists():
        try:
            payload["generated_at"] = json.loads(OUT.read_text(encoding="utf-8")).get("generated_at", payload["generated_at"])
        except json.JSONDecodeError:
            pass
    json_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    markdown = render_report(payload)
    stale = []
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != json_text:
            stale.append(str(OUT.relative_to(REPO_ROOT)))
        if not REPORT_JSON.exists() or json.loads(REPORT_JSON.read_text(encoding="utf-8")).get("summary") != payload["summary"]:
            stale.append(str(REPORT_JSON.relative_to(REPO_ROOT)))
        if not REPORT_MD.exists() or REPORT_MD.read_text(encoding="utf-8") != markdown:
            stale.append(str(REPORT_MD.relative_to(REPO_ROOT)))
        if stale:
            raise SystemExit("source coverage is stale: " + ", ".join(stale))
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(json_text, encoding="utf-8")
    REPORT_JSON.write_text(json_text, encoding="utf-8")
    REPORT_MD.write_text(markdown, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}, {REPORT_JSON.relative_to(REPO_ROOT)}, and {REPORT_MD.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
