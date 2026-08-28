#!/usr/bin/env python3
"""Generate an explicit, machine-readable record of legitimate source gaps."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from report_paths import latest_source_report  # noqa: E402

WORKS = REPO_ROOT / "data" / "works.json"
OUT = REPO_ROOT / "data" / "coverage-exceptions.json"
REPORT_JSON = REPO_ROOT / "reports" / f"source_coverage_{datetime.now(timezone.utc).date().isoformat()}.json"
REPORT_MD = REPO_ROOT / "reports" / f"source_coverage_{datetime.now(timezone.utc).date().isoformat()}.md"


# Explicit reviewed overrides: citation_keys recognized as legitimate historical gaps
REVIEWED_LEGITIMATE_GAPS = {
    "Friedman2025TowardsScienceConsciousnessSocial028",
    "Friedman2024WritingCurioCardsNFT044",
    "Friedman2019PhDBehavioralPhysiologicalTranscriptomic093",
    "Friedman2016LessonsFromColony155",
    "Friedman2016FullSpeedAheadCity156",
    "Friedman2021Disinforge157",
    "Friedman2021DefiningEvents2020Hindsight158",
}


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
            key = work.get("citation_key")
            is_legit = ("non_paper_record" in reasons) or (key in REVIEWED_LEGITIMATE_GAPS)
            exceptions.append(
                {
                    "num": work.get("num"),
                    "citation_key": key,
                    "title": work.get("title"),
                    "type": work.get("type"),
                    "reasons": reasons,
                    "review_status": "legitimate_gap" if is_legit else "needs_review",
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


def preserve_timestamp_when_unchanged(payload: dict) -> dict:
    """Avoid report churn when the coverage exception set is unchanged."""
    if not OUT.exists():
        return payload
    try:
        existing = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return payload
    current_body = {key: value for key, value in payload.items() if key != "generated_at"}
    existing_body = {key: value for key, value in existing.items() if key != "generated_at"}
    if current_body == existing_body and existing.get("generated_at"):
        payload["generated_at"] = existing["generated_at"]
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the generated coverage outputs are stale")
    args = parser.parse_args()
    payload = build_payload()
    payload = preserve_timestamp_when_unchanged(payload)
    json_text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    markdown = render_report(payload)
    stale = []
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != json_text:
            stale.append(str(OUT.relative_to(REPO_ROOT)))
        # Dated reports are snapshots, not daily leases.  A validation run just
        # after midnight UTC must check the newest existing snapshot rather than
        # requiring a brand-new file for the new calendar day.  This matters on
        # local west-coast checkouts and in CI jobs whose date boundary differs
        # from the author's working day.
        report_json = latest_source_report("source_coverage_*.json", required=False)
        report_md = latest_source_report("source_coverage_*.md", required=False)
        if not report_json or report_json.read_text(encoding="utf-8") != json_text:
            stale.append(str((report_json or REPORT_JSON).relative_to(REPO_ROOT)))
        if not report_md or report_md.read_text(encoding="utf-8") != markdown:
            stale.append(str((report_md or REPORT_MD).relative_to(REPO_ROOT)))
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
