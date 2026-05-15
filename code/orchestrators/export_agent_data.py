#!/usr/bin/env python3
"""Export compact JSON indexes for agentic discovery.

Outputs:
  - data/software.json
  - data/people.json
  - data/organizations.json
  - data/claims.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOFTWARE_MD = REPO_ROOT / "pages" / "SOFTWARE.md"

try:
    from report_paths import generated_timestamp, latest_report, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_report, rel


def strip_md(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("📄", "").strip()
    return re.sub(r"\s*[·;,-]\s*$", "", value).strip()


def parse_link_cell(cell: str) -> tuple[str, str]:
    m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", cell)
    if not m:
        return strip_md(cell), ""
    return m.group(1), m.group(2)


def parse_software() -> list[dict]:
    text = SOFTWARE_MD.read_text(encoding="utf-8")
    rows: list[dict] = []
    section = ""
    for line in text.splitlines():
        if line.startswith("## 🧬"):
            section = "docxology"
        elif line.startswith("### 🏛️"):
            section = "active-inference-institute"
        if not section or not line.startswith("| ["):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        name, url = parse_link_cell(cells[0])
        description = strip_md(cells[1])
        try:
            stars = int(re.sub(r"[^0-9]", "", cells[3]) or "0")
        except ValueError:
            stars = 0
        rows.append(
            {
                "name": name,
                "url": url,
                "owner": "docxology" if section == "docxology" else "ActiveInferenceInstitute",
                "catalog_section": section,
                "description": description,
                "language": cells[2] if cells[2] != "—" else "",
                "stars": stars,
                "updated_or_year": cells[4],
            }
        )
    return rows


PEOPLE = [
    {
        "name": "Daniel Ari Friedman",
        "role": "Computational biologist; cognitive scientist; President and Treasurer of the Active Inference Institute",
        "orcid": "https://orcid.org/0000-0001-6232-9096",
        "wikidata": "https://www.wikidata.org/wiki/Q138781444",
        "homepage": "https://danielarifriedman.com/",
        "github": "https://github.com/docxology",
    },
    {
        "name": "Karl Friston",
        "role": "Active Inference and Free Energy Principle collaborator",
        "source": "pages/COLLABORATORS.md#karl-friston--ucl-london",
    },
    {
        "name": "Deborah Gordon",
        "role": "Stanford PhD advisor and ant collective behavior collaborator",
        "source": "pages/COLLABORATORS.md#deborah-gordon--stanford-university",
    },
    {
        "name": "Thomas Parr",
        "role": "Active Inference collaborator and textbook co-author",
        "source": "pages/COLLABORATORS.md#thomas-parr--ucl-london",
    },
    {
        "name": "MJ Ramstead",
        "role": "Active Inference and cognitive science collaborator",
        "source": "pages/COLLABORATORS.md#maxwell-j-d-ramstead--mila--mcgill",
    },
]


ORGANIZATIONS = [
    {
        "name": "Active Inference Institute",
        "alternate_names": ["AII", "Active Inference Lab"],
        "url": "https://www.activeinference.institute/",
        "public_landing_page": "https://activeinference.org/",
        "wikidata": "https://www.wikidata.org/wiki/Q139600792",
        "github": "https://github.com/ActiveInferenceInstitute",
        "role": "Research and education nonprofit focused on Active Inference and the Free Energy Principle",
    },
    {
        "name": "COGSEC.org",
        "url": "https://cogsec.org",
        "role": "Cognitive security publication and research context",
    },
    {
        "name": "Stanford University",
        "url": "https://www.stanford.edu/",
        "role": "PhD institution",
    },
    {
        "name": "College of the Redwoods",
        "url": "https://www.redwoods.edu/",
        "role": "Teaching affiliation",
    },
]


CLAIMS = [
    {
        "id": "curated-work-count",
        "claim": "The curated bibliography contains 115 works.",
        "status": "curated-local",
        "sources": ["pages/BIBLIOGRAPHY.md", "publications.html", "data/works.json"],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "Generated from the 8-column bibliography table and cross-checked against publications.html.",
        "maintenance_owner": "ARCHIVIST",
        "caveat": "Curated count includes papers, books, presentations, courses, playbooks, and series.",
    },
    {
        "id": "paper-folder-count",
        "claim": "The repository contains 108 per-paper documentation folders.",
        "status": "curated-local",
        "sources": ["papers/", "papers/README.md", "papers/paper_metadata.json"],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "Folder inventory and paper metadata count.",
        "maintenance_owner": "MAINTAINER",
        "caveat": "Not every bibliography row has a paper folder; media/course rows may not.",
    },
    {
        "id": "docxology-github-public-repos",
        "claim": "The docxology GitHub profile has 286 public repositories.",
        "status": "public-api",
        "sources": ["https://api.github.com/users/docxology", "reports/public_source_snapshot_2026-05-15.json"],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "GitHub REST API user profile response.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "GitHub profile count includes forks and repositories not catalogued in SOFTWARE.md.",
    },
    {
        "id": "aii-github-public-repos",
        "claim": "The Active Inference Institute GitHub organization has 50 public repositories.",
        "status": "public-api",
        "sources": [
            "https://api.github.com/users/ActiveInferenceInstitute",
            "reports/public_source_snapshot_2026-05-15.json"
        ],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "GitHub REST API organization profile response.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Local software catalog tracks 32 AII repositories with docxology contributions.",
    },
    {
        "id": "orcid-canonical-identifier",
        "claim": "ORCID 0000-0001-6232-9096 is the canonical researcher identifier.",
        "status": "public-identifier",
        "sources": ["https://orcid.org/0000-0001-6232-9096", "https://pub.orcid.org/v3.0/0000-0001-6232-9096/works"],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "ORCID profile and public works endpoint.",
        "maintenance_owner": "ARCHIVIST",
        "caveat": "ORCID public work groups may lag new deposits and may group versions differently.",
    },
    {
        "id": "curio-cards-early-ethereum-art",
        "claim": "Curio Cards 24, 25, and 26 are early Ethereum art NFTs minted on May 9, 2017.",
        "status": "public-profile",
        "sources": [
            "https://curio.cards/artist/danielfriedman/",
            "https://www.christies.com/en/lot/lot-6337619",
            "papers/2024_CurioCards/README.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Curio Cards artist profile, Christie's lot page, and local paper notes.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Use conservative phrasing; broader first/earliest claims vary by source and definition.",
    },
    {
        "id": "google-scholar-citations",
        "claim": "Google Scholar citation count is manually synced as 812 citations with h-index 15.",
        "status": "manual-public-profile",
        "sources": [
            "https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en",
            "README.md",
            "pages/BIBLIOGRAPHY.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Manual Google Scholar profile sync; public cache and access path can vary.",
        "maintenance_owner": "ARCHIVIST",
        "caveat": "Do not overwrite automatically from cached or anonymous Scholar views.",
    },
    {
        "id": "stanford-phd",
        "claim": "Daniel Ari Friedman earned a PhD at Stanford University with dissertation record pb813wm1484.",
        "status": "public-institutional-record",
        "sources": [
            "http://purl.stanford.edu/pb813wm1484",
            "papers/2019_PhDDissertation/README.md",
            "pages/PROFILE.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "Stanford PURL dissertation record and local paper folder.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Use the Stanford PURL as the public institutional source.",
    },
    {
        "id": "nsf-postdoc-affiliation",
        "claim": "Daniel Ari Friedman was an NSF Postdoctoral Fellow at UC Davis from 2020 to 2023.",
        "status": "curated-profile",
        "sources": ["pages/PROFILE.md", "README.md"],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Curated profile and homepage copy.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Add a grant or institutional source if a public authoritative record is located.",
    },
    {
        "id": "aii-officer-roles",
        "claim": "Active Inference Institute officers list Daniel Friedman as President and Treasurer.",
        "status": "public-profile",
        "sources": [
            "https://www.activeinference.institute/officers",
            "pages/DISCOVERY.md",
            "pages/PROFILE.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "AII officers page and local discovery map.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Officer roles are time-sensitive and should be rechecked before formal bios.",
    },
    {
        "id": "aii-board-count",
        "claim": "The Active Inference Institute board page lists 10 current directors.",
        "status": "public-profile",
        "sources": [
            "https://www.activeinference.institute/board-of-directors",
            "pages/LINKS.md",
            "pages/WIKIPEDIA.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "high",
        "verification_method": "AII board page and local governance notes.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Board membership is time-sensitive; retain access dates in narrative pages.",
    },
    {
        "id": "aii-scientific-advisory-board-count",
        "claim": "The Active Inference Institute announced a 33-member Scientific Advisory Board cohort in 2026.",
        "status": "public-profile",
        "sources": [
            "https://www.activeinference.institute/scientific-advisory-board",
            "pages/LINKS.md",
            "pages/DISCOVERY.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "AII SAB page and local discovery notes.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Use cautious wording unless the source page explicitly states the cohort count.",
    },
    {
        "id": "aii-textbook-cohorts",
        "claim": "AII Textbook Group copy references 10 cohorts through 2026.",
        "status": "curated-program-copy",
        "sources": [
            "https://www.activeinference.institute/textbook-group",
            "README.md",
            "pages/VIDEOS.md"
        ],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Curated site copy and AII program page.",
        "maintenance_owner": "EDUCATOR",
        "caveat": "Program pages may use different public summary counts; keep local copy aligned with preferred site wording.",
    },
    {
        "id": "college-of-the-redwoods-teaching",
        "claim": "Homepage teaching copy lists BIOL-1 at Pelican Bay and BIOL-8 Human Biology for Spring 2026.",
        "status": "curated-profile",
        "sources": ["README.md", "index.html", "pages/PROFILE.md"],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Curated homepage and profile synchronization.",
        "maintenance_owner": "EDUCATOR",
        "caveat": "Term-specific teaching claims should be updated after each semester.",
    },
    {
        "id": "cogsec-role",
        "claim": "COGSEC.org is the cognitive security publication and research context linked from the profile.",
        "status": "public-site",
        "sources": ["https://cogsec.org", "README.md", "pages/PROFILE.md"],
        "checked_at": "2026-05-15",
        "confidence": "medium",
        "verification_method": "Public site link and curated profile copy.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Prefer COGSEC pages for COGSEC-specific publication claims.",
    },
]


def _latest_source(pattern: str, fallback: str) -> str:
    try:
        latest = latest_report(pattern)
    except FileNotFoundError:
        return fallback
    return rel(latest)


def _existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def _hydrate_claim_checks(checked_at: str) -> list[dict]:
    claims = []
    latest_snapshot = _latest_source("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json")
    latest_inventory = _latest_source("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json")
    for claim in CLAIMS:
        claim_copy = dict(claim)
        claim_copy["checked_at"] = checked_at
        claim_copy["sources"] = [
            latest_snapshot if source.startswith("reports/public_source_snapshot_") else
            latest_inventory if source.startswith("reports/public_source_inventory_") else source
            for source in claim_copy.get("sources", [])
        ]
        claims.append(claim_copy)
    return claims


def render_outputs(generated_at: str | None = None) -> dict[Path, str]:
    software = parse_software()
    generated_at = generated_at or generated_timestamp()
    claims = _hydrate_claim_checks(generated_at)
    return {
        REPO_ROOT / "data" / "software.json": json.dumps(
            {
                "generated_at": generated_at,
                "source": "pages/SOFTWARE.md",
                "count": len(software),
                "repositories": software,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        REPO_ROOT / "data" / "people.json": json.dumps(
            {"generated_at": generated_at, "people": PEOPLE}, indent=2, ensure_ascii=False
        )
        + "\n",
        REPO_ROOT / "data" / "organizations.json": json.dumps(
            {"generated_at": generated_at, "organizations": ORGANIZATIONS}, indent=2, ensure_ascii=False
        )
        + "\n",
        REPO_ROOT / "data" / "claims.json": json.dumps(
            {"generated_at": generated_at, "claims": claims}, indent=2, ensure_ascii=False
        )
        + "\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    generated_at = _existing_generated_at(REPO_ROOT / "data" / "claims.json") if args.check else None
    outputs = render_outputs(generated_at)
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated agent data files: " + ", ".join(stale))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} agent data files")


if __name__ == "__main__":
    main()
