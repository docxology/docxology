#!/usr/bin/env python3
"""Build a public-source reconciliation report from local indexes and freshness snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
JSON_OUT = REPO_ROOT / "data" / "reconciliation.json"

try:
    from report_paths import latest_report, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, rel


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def snapshot_value(snapshot: dict, label: str, key: str) -> int | str | None:
    for check in snapshot["checks"]:
        if check["label"] == label:
            result = check.get("result", {})
            return result.get(key)
    return None


def snapshot_path() -> Path:
    return latest_report("public_source_snapshot_*.json")


def snapshot_date(path: Path) -> str:
    return path.stem.removeprefix("public_source_snapshot_")


def build_payload() -> dict:
    works = load_json(REPO_ROOT / "data" / "works.json")
    software = load_json(REPO_ROOT / "data" / "software.json")
    claims = load_json(REPO_ROOT / "data" / "claims.json")
    source_snapshot = snapshot_path()
    snapshot = load_json(source_snapshot)
    owned = [r for r in software["repositories"] if r["owner"] == "docxology"]
    aii = [r for r in software["repositories"] if r["owner"] == "ActiveInferenceInstitute"]
    comparisons = [
        {
            "name": "Curated bibliography vs ORCID work groups",
            "local_value": works["count"],
            "public_value": snapshot_value(snapshot, "ORCID work groups", "group_count"),
            "relationship": "not expected to match",
            "interpretation": "The local bibliography intentionally includes presentations, courses, books, software-linked works, and local documentation. ORCID groups external works by identifier/version.",
        },
        {
            "name": "Curated bibliography vs PubMed exact author records",
            "local_value": works["count"],
            "public_value": snapshot_value(snapshot, "PubMed exact author records", "count"),
            "relationship": "subset",
            "interpretation": "PubMed only covers biomedical/indexed literature and is a strict subset of the curated bibliography.",
        },
        {
            "name": "Curated bibliography vs Crossref ORCID DOI records",
            "local_value": works["count"],
            "public_value": snapshot_value(snapshot, "Crossref ORCID DOI records", "total_results"),
            "relationship": "subset",
            "interpretation": "Crossref captures DOI records attached to the ORCID; Zenodo, books, courses, and non-DOI works may be absent or represented elsewhere.",
        },
        {
            "name": "Curated bibliography vs Zenodo ORCID-linked records",
            "local_value": works["count"],
            "public_value": snapshot_value(snapshot, "Zenodo ORCID-linked records", "total"),
            "relationship": "overlapping sets",
            "interpretation": "Zenodo includes versioned records and software archives; the local bibliography normalizes selected works into one curated table.",
        },
        {
            "name": "Catalogued docxology software vs GitHub public repository count",
            "local_value": len(owned),
            "public_value": snapshot_value(snapshot, "GitHub user docxology", "public_repos"),
            "relationship": "curated subset",
            "interpretation": "SOFTWARE.md intentionally catalogs selected owned repositories; GitHub counts all public repositories including forks and uncatalogued experiments.",
        },
        {
            "name": "Catalogued AII contributions vs AII GitHub public repository count",
            "local_value": len(aii),
            "public_value": snapshot_value(snapshot, "GitHub user ActiveInferenceInstitute", "public_repos"),
            "relationship": "curated subset",
            "interpretation": "SOFTWARE.md lists AII repositories with docxology contributions, not every public AII repository.",
        },
    ]
    return {
        "generated_at": snapshot.get("generated_at", snapshot_date(source_snapshot)),
        "snapshot": rel(source_snapshot),
        "claims_count": len(claims["claims"]),
        "comparisons": comparisons,
    }


def render_md(payload: dict) -> str:
    lines = [
        "# Public-Source Reconciliation Report",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"Snapshot: [`{payload['snapshot']}`]({Path(payload['snapshot']).name})",
        "",
        "This report compares curated local counts against public authority/source indexes. Differences are expected unless the relationship says otherwise.",
        "",
        "| Comparison | Local | Public | Relationship | Interpretation |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in payload["comparisons"]:
        lines.append(
            f"| {row['name']} | {row['local_value']} | {row['public_value']} | {row['relationship']} | {row['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Maintenance Use",
            "",
            "- Use this report to decide whether a public-source change requires curated copy updates.",
            "- Do not automatically overwrite curated counts when public indexes have different scope.",
            "- Re-run `code/orchestrators/refresh_public_sources.py` before updating this report.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    payload = build_payload()
    md_out = REPO_ROOT / "reports" / f"reconciliation_{snapshot_date(REPO_ROOT / payload['snapshot'])}.md"
    return {
        JSON_OUT: json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        md_out: render_md(payload),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if reconciliation outputs are stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale reconciliation outputs: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " reconciliation report")


if __name__ == "__main__":
    main()
