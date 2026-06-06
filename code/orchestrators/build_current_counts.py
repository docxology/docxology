#!/usr/bin/env python3
"""Build the generated volatile-count report used by hand-authored docs."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "current_counts.md"
JSON_PATH = REPO_ROOT / "data" / "current-counts.json"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from count_consistency import (  # noqa: E402
    DOMAIN_COUNTS,
    TYPE_LABELS,
    parse_bibliography_rows,
    parse_paper_folder_count,
    parse_software_catalog_counts,
)


def _json(path: str) -> dict:
    return json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))


def _latest_report(pattern: str) -> Path | None:
    matches = sorted((REPO_ROOT / "reports").glob(pattern))
    return matches[-1] if matches else None


def _public_source_snapshot_counts(payload: dict) -> dict:
    facts = payload.get("facts", {})
    values: dict[str, int] = {}
    for label, fact in facts.items():
        if not isinstance(fact, dict):
            continue
        for key in ("public_repos", "group_count", "count"):
            value = fact.get(key)
            if isinstance(value, int):
                values[label] = value
                break
    return values


def collect_counts() -> dict:
    rows = parse_bibliography_rows()
    type_counts = Counter(row["type"] for row in rows)
    domain_counts = Counter(row["domain"] for row in rows)
    software_docx, software_aii = parse_software_catalog_counts()
    works_json = _json("data/works.json")
    software_json = _json("data/software.json")
    github_json = _json("data/github-repositories.json")
    public_source_report = _latest_report("public_source_snapshot_*.json")
    paired_report = _latest_report("paired_publications_*.json")
    decision_path = REPO_ROOT / "data" / "paired-publication-decisions.json"

    public_source_payload = _json(str(public_source_report.relative_to(REPO_ROOT))) if public_source_report else {}
    paired_payload = _json(str(paired_report.relative_to(REPO_ROOT))) if paired_report else {}
    decision_payload = json.loads(decision_path.read_text(encoding="utf-8")) if decision_path.is_file() else {}

    return {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "command": "uv run python3 code/orchestrators/build_current_counts.py",
        "check_command": "uv run python3 code/orchestrators/build_current_counts.py --check",
        "sources": {
            "bibliography": "pages/BIBLIOGRAPHY.md",
            "paper_folders": "papers/README.md",
            "software_catalog": "pages/SOFTWARE.md",
            "works_export": "data/works.json",
            "software_export": "data/software.json",
            "github_inventory": "data/github-repositories.json",
            "public_source_snapshot": str(public_source_report.relative_to(REPO_ROOT)) if public_source_report else None,
            "paired_publications": str(paired_report.relative_to(REPO_ROOT)) if paired_report else None,
            "paired_publication_decisions": str(decision_path.relative_to(REPO_ROOT)) if decision_path.is_file() else None,
        },
        "counts": {
            "bibliography_works": len(rows),
            "paper_folder_docs": parse_paper_folder_count(),
            "bibliography_docs_links": sum(1 for row in rows if "../papers/" in row["docs"]),
            "types": {TYPE_LABELS.get(k, k): type_counts[k] for k in sorted(type_counts)},
            "domains": {
                label: domain_counts[symbol]
                for label, symbol in DOMAIN_COUNTS.items()
            },
            "software": {
                "docxology_owned": software_docx,
                "active_inference_institute": software_aii,
                "curated_total": software_docx + software_aii,
            },
            "generated_exports": {
                "data_works_json": works_json.get("count"),
                "data_software_json": software_json.get("count"),
                "data_publications_ld_main_entity": len(_json("data/publications-ld.json").get("mainEntity", [])),
                "data_software_ld_main_entity": len(_json("data/software-ld.json").get("mainEntity", [])),
            },
            "github_inventory": github_json.get("counts", {}),
            "public_source_snapshot": _public_source_snapshot_counts(public_source_payload),
            "paired_publications": paired_payload.get("counts", {}),
            "paired_publication_decisions": decision_payload.get("decision_summary", {}),
        },
        "validation": [
            "uv run python3 code/orchestrators/validate_repo.py",
            "cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q",
        ],
    }


def render_markdown(payload: dict) -> str:
    counts = payload["counts"]
    sources = payload["sources"]
    lines = [
        "# Current Counts Report",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "This generated report is the repo-local plaintext target for volatile totals. Hand-authored docs should link here, to the canonical source tables, or to generated JSON rather than repeating these values.",
        "",
        "Regenerate:",
        "",
        f"```bash\n{payload['command']}\n```",
        "",
        "Check without writing:",
        "",
        f"```bash\n{payload['check_command']}\n```",
        "",
        "## Canonical Sources",
        "",
    ]
    for label, path in sources.items():
        if path:
            lines.append(f"- {label}: `{path}`")
    lines.extend(
        [
            "",
            "## Counts",
            "",
            f"- Bibliography works: `{counts['bibliography_works']}`",
            f"- Paper-folder docs: `{counts['paper_folder_docs']}`",
            f"- Bibliography docs links: `{counts['bibliography_docs_links']}`",
            "",
            "### Types",
            "",
        ]
    )
    for label, value in counts["types"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### Domains", ""])
    for label, value in counts["domains"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### Software", ""])
    for label, value in counts["software"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### Generated Exports", ""])
    for label, value in counts["generated_exports"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### GitHub Inventory", ""])
    for label, value in counts["github_inventory"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### Public Source Snapshot", ""])
    for label, value in counts["public_source_snapshot"].items():
        lines.append(f"- {label}: `{value}`")
    lines.extend(["", "### Paired Publications", ""])
    for label, value in counts["paired_publications"].items():
        lines.append(f"- {label}: `{value}`")
    if counts.get("paired_publication_decisions"):
        lines.extend(["", "### Paired Publication Decisions", ""])
        for label, value in counts["paired_publication_decisions"].items():
            lines.append(f"- {label}: `{value}`")
    lines.extend(["", "## Validation", ""])
    for command in payload["validation"]:
        lines.append(f"- `{command}`")
    lines.append("")
    return "\n".join(lines)


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated outputs are stale")
    args = parser.parse_args()

    payload = collect_counts()
    # Preserve the checked file timestamp so --check is deterministic.
    if args.check and JSON_PATH.exists():
        existing = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        payload["generated_at"] = existing.get("generated_at", payload["generated_at"])

    json_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    markdown = render_markdown(payload)

    if args.check:
        stale = []
        if not JSON_PATH.exists() or JSON_PATH.read_text(encoding="utf-8") != json_text:
            stale.append(str(JSON_PATH.relative_to(REPO_ROOT)))
        if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != markdown:
            stale.append(str(REPORT_PATH.relative_to(REPO_ROOT)))
        if stale:
            raise SystemExit("current count report is stale: " + ", ".join(stale))
        print(f"checked {REPORT_PATH.relative_to(REPO_ROOT)}")
        return

    write_if_changed(JSON_PATH, json_text)
    write_if_changed(REPORT_PATH, markdown)
    print(f"wrote {REPORT_PATH.relative_to(REPO_ROOT)} and {JSON_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
