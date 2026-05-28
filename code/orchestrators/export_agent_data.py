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
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(PAPERS_DIR))

from software_table import iter_software_rows, software_rows_to_dict  # noqa: E402

SOFTWARE_MD = REPO_ROOT / "pages" / "SOFTWARE.md"
SCHOLAR_SNAPSHOT = REPO_ROOT / "data" / "scholar-snapshot.json"
WORKS_JSON = REPO_ROOT / "data" / "works.json"


def _scholar_claim() -> dict:
    """Build the Google Scholar claim from the dated snapshot (single source
    of truth). Replaces a hardcoded, manually-frozen 812 figure: the snapshot
    carries the as-of date and fetch method, so the claim is provenance-stamped
    rather than frozen behind a no-overwrite caveat."""
    s = json.loads(SCHOLAR_SNAPSHOT.read_text(encoding="utf-8"))
    return {
        "id": "google-scholar-citations",
        "claim": (
            f"Google Scholar metrics are recorded as a dated snapshot: "
            f"{s['citations']} citations, h-index {s['h_index']}, "
            f"i10-index {s['i10_index']} (as of {s['as_of']})."
        ),
        "status": "dated-snapshot",
        "sources": [
            s["profile_url"],
            "data/scholar-snapshot.json",
            "pages/VERIFICATION_LOG.md",
        ],
        "checked_at": s["as_of"],
        "confidence": "high",
        "verification_method": s["method"],
        "maintenance_owner": "ARCHIVIST",
        "caveat": (
            "Single source of truth: data/scholar-snapshot.json. Update only "
            "from a direct (non-cached) Scholar fetch, recording the new value, "
            "as_of date, and method there; regenerate surfaces via "
            "code/orchestrators/sync_scholar_metrics.py. Never publish a "
            "citation number above the most recent direct-fetch value."
        ),
    }

try:
    from report_paths import generated_timestamp, latest_report, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_report, rel


def parse_software() -> list[dict]:
    return [software_rows_to_dict(row) for row in iter_software_rows(SOFTWARE_MD)]


def _current_work_count() -> int:
    if WORKS_JSON.exists():
        payload = json.loads(WORKS_JSON.read_text(encoding="utf-8"))
        return int(payload.get("count") or len(payload.get("works", [])))
    rows = [
        line
        for line in (REPO_ROOT / "pages" / "BIBLIOGRAPHY.md").read_text(encoding="utf-8").splitlines()
        if re.match(r"\| \d+ \|", line)
    ]
    return len(rows)


def _current_paper_folder_count() -> int:
    return sum(1 for path in (REPO_ROOT / "papers").iterdir() if path.is_dir() and re.match(r"\d{4}_", path.name))


def _latest_snapshot_payload() -> dict:
    try:
        path = latest_report("public_source_snapshot_*.json")
    except FileNotFoundError:
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _snapshot_value(snapshot: dict, label: str, key: str) -> int | str | None:
    for check in snapshot.get("checks", []):
        if check.get("label") == label:
            result = check.get("result") if isinstance(check.get("result"), dict) else {}
            return result.get(key)
    return None


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
        "github_account_type": "user",
        "github_note": "The ActiveInferenceInstitute GitHub account is a User account, not an Organization; requests to /orgs/ActiveInferenceInstitute return 404. Use /users/ActiveInferenceInstitute.",
        "ein": "88-2985125",
        "irs_status": "501(c)(3) public charity; IRS ruling March 2024",
        "irs_record": "https://projects.propublica.org/nonprofits/organizations/882985125",
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
        "claim": "The curated bibliography contains 130 works.",
        "status": "curated-local",
        "sources": ["pages/BIBLIOGRAPHY.md", "publications.html", "data/works.json"],
        "checked_at": "2026-05-28",
        "confidence": "high",
        "verification_method": "Generated from the 8-column bibliography table and cross-checked against publications.html.",
        "maintenance_owner": "ARCHIVIST",
        "caveat": "Curated count includes papers, books, presentations, courses, playbooks, and series.",
    },
    {
        "id": "paper-folder-count",
        "claim": "The repository contains 123 per-paper documentation folders.",
        "status": "curated-local",
        "sources": ["papers/", "papers/README.md", "papers/paper_metadata.json"],
        "checked_at": "2026-05-28",
        "confidence": "high",
        "verification_method": "Folder inventory and paper metadata count.",
        "maintenance_owner": "MAINTAINER",
        "caveat": "Not every bibliography row has a paper folder; media/course rows may not.",
    },
    {
        "id": "docxology-github-public-repos",
        "claim": "The docxology GitHub profile has 299 public repositories.",
        "status": "public-api",
        "sources": ["https://api.github.com/users/docxology", "reports/public_source_snapshot_2026-05-28.json"],
        "checked_at": "2026-05-28",
        "confidence": "high",
        "verification_method": "GitHub REST API user profile response.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "GitHub profile count includes forks and repositories not catalogued in SOFTWARE.md.",
    },
    {
        "id": "aii-github-public-repos",
        "claim": "The ActiveInferenceInstitute GitHub account (a User account, not an Organization) has 51 public repositories.",
        "status": "public-api",
        "sources": [
            "https://api.github.com/users/ActiveInferenceInstitute",
            "reports/public_source_snapshot_2026-05-28.json"
        ],
        "checked_at": "2026-05-28",
        "confidence": "high",
        "verification_method": "GitHub REST API user profile response (type: User). The /orgs/ActiveInferenceInstitute endpoint returns 404 because the account is a User, not an Organization.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Use /users/ActiveInferenceInstitute, not /orgs/. Local software catalog tracks 32 AII repositories with docxology contributions.",
    },
    {
        "id": "orcid-canonical-identifier",
        "claim": "ORCID 0000-0001-6232-9096 is the canonical researcher identifier. The canonical Google Scholar profile is DXjPFtYAAAAJ; a secondary Scholar profile (Y2bMf3MAAAAJ) is linked from ORCID and should be consolidated/disambiguated.",
        "status": "public-identifier",
        "sources": ["https://orcid.org/0000-0001-6232-9096", "https://pub.orcid.org/v3.0/0000-0001-6232-9096/works"],
        "checked_at": "2026-05-16",
        "confidence": "high",
        "verification_method": "ORCID profile and public works endpoint. ORCID also exposes a secondary Google Scholar ID (Y2bMf3MAAAAJ) distinct from the canonical DXjPFtYAAAAJ used for all public metrics.",
        "maintenance_owner": "ARCHIVIST",
        "caveat": "Use DXjPFtYAAAAJ as the single canonical Scholar profile for metrics. ORCID public work groups may lag new deposits and may group versions differently.",
    },
    {
        "id": "curio-cards-early-ethereum-art",
        "claim": "Curio Cards 24, 25, and 26 are early Ethereum art NFTs minted on May 9, 2017; a complete Curio Cards set later sold at Christie's 'Post-War to Present' (New York, Oct 1, 2021) for 393 ETH (~$1.2M), seven artists.",
        "status": "public-profile",
        "sources": [
            "https://curio.cards/artist/danielfriedman/",
            "https://docs.curio.cards/the-artists/daniel-friedman",
            "https://en.wikipedia.org/wiki/Curio_Cards",
            "https://www.christies.com/en/lot/lot-6337619",
            "papers/2024_CurioCards/README.md"
        ],
        "checked_at": "2026-05-16",
        "confidence": "high",
        "verification_method": "Artist attribution and mint date confirmed via Curio Cards official docs and Wikipedia; the Christie's sale (date, 393 ETH/~$1.2M, seven artists) is independently corroborated. The specific Christie's lot URL (6337619) resolves and its first-party page matches the exact Curio set, but the lot number itself is not corroborated by any source independent of Christie's.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Present the sale facts as independently verified; present the specific Christie's lot number as a first-party (Christie's) reference only, not independently corroborated. Avoid unqualified 'first/earliest NFT' superlatives.",
    },
    _scholar_claim(),
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
        "claim": "Daniel Ari Friedman held an NSF Postdoctoral Research Fellowship in Biology (award DBI-2010290) co-trained at UC Davis; NSF budget period 2020-2022 with a no-cost extension to 2023.",
        "status": "public-grant-record",
        "sources": [
            "https://grantome.com/grant/NSF/DBI-2010290",
            "pages/PROFILE.md",
            "README.md",
        ],
        "checked_at": "2026-05-16",
        "confidence": "high",
        "verification_method": "NSF award DBI-2010290 confirmed via Grantome (NSF PRFB, FY2020, $138,000, Davis CA). The 2020-2022 budget period is on the NSF record; the extension to 2023 aligns with the ORCID UC Davis employment span but is not itself on the funding record.",
        "maintenance_owner": "RESEARCHER",
        "caveat": "Cite the NSF award ID (DBI-2010290) as the authoritative public record. The funding record shows 2020-2022; present 2023 as a no-cost-extension affiliation, not a funded period.",
    },
    {
        "id": "aii-officer-roles",
        "claim": "Active Inference Institute officers: Daniel Friedman is President and Treasurer; Alexandra Mikhailova is Vice-President and Secretary (2025-ongoing). V. Bleu Knight was Secretary 2022-2024 and is a current member of the Board of Directors. The Institute is a 501(c)(3) public charity, EIN 88-2985125, IRS ruling March 2024.",
        "status": "public-profile",
        "sources": [
            "https://www.activeinference.institute/officers",
            "https://projects.propublica.org/nonprofits/organizations/882985125",
            "pages/DISCOVERY.md",
            "pages/PROFILE.md"
        ],
        "checked_at": "2026-05-16",
        "confidence": "high",
        "verification_method": "AII officers page; 501(c)(3) status and EIN independently confirmed via ProPublica Nonprofit Explorer (IRS data, ruling March 2024).",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "Officer roles are time-sensitive. Do not conflate Mikhailova (current VP+Secretary) with Knight (former Secretary 2022-2024, current Board member).",
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
        "claim": "The Active Inference Institute site lists a 33-member Scientific Advisory Board cohort for 2026.",
        "status": "public-profile",
        "sources": [
            "https://www.activeinference.institute/scientific-advisory-board",
            "pages/LINKS.md",
            "pages/DISCOVERY.md"
        ],
        "checked_at": "2026-05-16",
        "confidence": "medium",
        "verification_method": "AII SAB page lists the 2026 cohort (33 members). The member count is corroborated; no specific announcement date (e.g. a January 2026 announcement) is independently verified.",
        "maintenance_owner": "INTEGRATOR",
        "caveat": "State the cohort as 'listed for 2026' (33 members). Do not assert a specific announcement month unless the source page states one.",
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
    snapshot = _latest_snapshot_payload()
    work_count = _current_work_count()
    folder_count = _current_paper_folder_count()
    docxology_public_repos = _snapshot_value(snapshot, "GitHub user docxology", "public_repos")
    aii_public_repos = _snapshot_value(snapshot, "GitHub user ActiveInferenceInstitute", "public_repos")
    for claim in CLAIMS:
        claim_copy = dict(claim)
        if claim_copy["id"] == "curated-work-count":
            claim_copy["claim"] = f"The curated bibliography contains {work_count} works."
        elif claim_copy["id"] == "paper-folder-count":
            claim_copy["claim"] = f"The repository contains {folder_count} per-paper documentation folders."
        elif claim_copy["id"] == "docxology-github-public-repos" and docxology_public_repos is not None:
            claim_copy["claim"] = f"The docxology GitHub profile has {docxology_public_repos} public repositories."
        elif claim_copy["id"] == "aii-github-public-repos" and aii_public_repos is not None:
            claim_copy["claim"] = (
                "The ActiveInferenceInstitute GitHub account (a User account, not an Organization) "
                f"has {aii_public_repos} public repositories."
            )
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
