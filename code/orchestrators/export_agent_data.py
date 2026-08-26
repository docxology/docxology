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
from functools import cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from count_consistency import parse_software_catalog_counts  # noqa: E402
from software_table import iter_software_rows, software_rows_to_dict  # noqa: E402
from report_paths import stable_generated_at  # noqa: E402

SOFTWARE_MD = REPO_ROOT / "pages" / "SOFTWARE.md"
SCHOLAR_SNAPSHOT = REPO_ROOT / "data" / "scholar-snapshot.json"
WORKS_JSON = REPO_ROOT / "data" / "works.json"
CURRENT_COUNTS_JSON = REPO_ROOT / "data" / "current-counts.json"


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
    from report_paths import generated_timestamp, latest_source_report, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_source_report, rel


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
        path = latest_source_report("public_source_snapshot_*.json")
    except FileNotFoundError:
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _current_counts_payload() -> dict:
    if not CURRENT_COUNTS_JSON.exists():
        return {}
    try:
        return json.loads(CURRENT_COUNTS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _date_prefix(value: str | None) -> str | None:
    if not value:
        return None
    return value[:10]


def _require_static_counts_in_fragment(
    claim_id: str,
    claim: str,
    *,
    work_count: int | None,
    folder_count: int | None,
    docxology_public_repos: int | None,
    aii_public_repos: int | None,
) -> list[str]:
    errors: list[str] = []
    if claim_id == "curated-work-count":
        if not claim or f"{int(work_count or 0)} works" not in claim:
            errors.append("curated-work-count claim missing authoritative work count")
    elif claim_id == "paper-folder-count":
        if not claim or f"{int(folder_count or 0)} per-paper documentation folders" not in claim:
            errors.append("paper-folder-count claim missing authoritative paper-folder count")
    elif claim_id == "docxology-github-public-repos":
        if docxology_public_repos is None or not claim or f"has {docxology_public_repos} public repositories" not in claim:
            errors.append("docxology-github-public-repos claim missing authoritative repository count")
    elif claim_id == "aii-github-public-repos":
        if aii_public_repos is None or not claim or f"has {aii_public_repos} public repositories" not in claim:
            errors.append("aii-github-public-repos claim missing authoritative repository count")
    return errors


def _stale_claim_fragment_errors(
    claim: dict,
    work_count: int | None,
    folder_count: int | None,
    docxology_public_repos: int | None,
    aii_public_repos: int | None,
    *,
    source_counts_timestamp: str | None = None,
    source_public_source_timestamp: str | None = None,
) -> list[str]:
    claim_id = claim.get("id")
    claim_text = claim.get("claim", "")
    checked_at = claim.get("checked_at")
    errors = _require_static_counts_in_fragment(
        claim_id,
        claim_text,
        work_count=work_count,
        folder_count=folder_count,
        docxology_public_repos=docxology_public_repos,
        aii_public_repos=aii_public_repos,
    )
    if checked_at and source_counts_timestamp and claim_id in {"curated-work-count", "paper-folder-count"}:
        if _date_prefix(checked_at) and _date_prefix(checked_at) != _date_prefix(source_counts_timestamp):
            errors.append(
                f"{claim_id} checked_at {checked_at} does not match source timestamp {source_counts_timestamp}"
            )
    if checked_at and source_public_source_timestamp and claim_id in {
        "docxology-github-public-repos",
        "aii-github-public-repos",
    }:
        if _date_prefix(checked_at) and _date_prefix(checked_at) != _date_prefix(source_public_source_timestamp):
            errors.append(
                f"{claim_id} checked_at {checked_at} does not match public-source timestamp {source_public_source_timestamp}"
            )
    return errors

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
        "source": "pages/COLLABORATORS.md#maxwell-ramstead",
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


@cache
def _claims() -> list[dict]:
    payload = _current_counts_payload()
    counts = payload.get("counts", {})
    counts_ts = payload.get("generated_at")
    snapshot = _latest_snapshot_payload()
    snapshot_ts = snapshot.get("generated_at")
    github_inventory = counts.get("github_inventory", {})
    docx_public_repos = _snapshot_value(snapshot, "GitHub user docxology", "public_repos")
    if docx_public_repos is None:
        docx_public_repos = github_inventory.get("docxology")
    aii_public_repos = _snapshot_value(snapshot, "GitHub user ActiveInferenceInstitute", "public_repos")
    if aii_public_repos is None:
        aii_public_repos = github_inventory.get("ActiveInferenceInstitute")
    work_count = int(counts.get("bibliography_works", _current_work_count()))
    folder_count = int(counts.get("paper_folder_docs", _current_paper_folder_count()))
    try:
        snapshot_source = rel(latest_source_report("public_source_snapshot_*.json"))
    except FileNotFoundError:
        snapshot_source = ""
    return [
        {
            "id": "curated-work-count",
            "claim": f"The curated bibliography contains {work_count} works.",
            "status": "curated-local",
            "sources": ["pages/BIBLIOGRAPHY.md", "publications.html", "data/works.json"],
            "checked_at": counts_ts or "2026-06-16T03:36:11+00:00",
            "confidence": "high",
            "verification_method": "Generated from the 8-column bibliography table and cross-checked against publications.html.",
            "maintenance_owner": "ARCHIVIST",
            "caveat": "Curated count includes papers, books, presentations, courses, playbooks, and series.",
        },
        {
            "id": "paper-folder-count",
            "claim": f"The repository contains {folder_count} per-paper documentation folders.",
            "status": "curated-local",
            "sources": ["papers/", "papers/README.md", "papers/paper_metadata.json"],
            "checked_at": counts_ts or "2026-06-16T03:36:11+00:00",
            "confidence": "high",
            "verification_method": "Folder inventory and paper metadata count.",
            "maintenance_owner": "MAINTAINER",
            "caveat": "Not every bibliography row has a paper folder; media/course rows may not.",
        },
        {
            "id": "docxology-github-public-repos",
            "claim": f"The docxology GitHub profile has {docx_public_repos} public repositories.",
            "status": "public-api",
            "sources": ["https://api.github.com/users/docxology", snapshot_source],
            "checked_at": snapshot_ts or counts_ts or "2026-06-09T03:41:15.072709+00:00",
            "confidence": "high",
            "verification_method": "GitHub REST API user profile response.",
            "maintenance_owner": "INTEGRATOR",
            "caveat": "GitHub profile count includes forks and repositories not catalogued in SOFTWARE.md.",
        },
        {
            "id": "aii-github-public-repos",
            "claim": (
                "The ActiveInferenceInstitute GitHub account (a User account, not an Organization) "
                f"has {aii_public_repos} public repositories."
            ),
            "status": "public-api",
            "sources": [
                "https://api.github.com/users/ActiveInferenceInstitute",
                snapshot_source
            ],
            "checked_at": snapshot_ts or counts_ts or "2026-06-09T03:41:15.072709+00:00",
            "confidence": "high",
            "verification_method": "GitHub REST API user profile response (type: User). The /orgs/ActiveInferenceInstitute endpoint returns 404 because the account is a User, not an Organization.",
            "maintenance_owner": "INTEGRATOR",
            "caveat": "Use /users/ActiveInferenceInstitute, not /orgs/. Local software catalog tracks AII repositories with docxology contributions (see pages/SOFTWARE.md and reports/current_counts.md).",
        },
        {
            "id": "orcid-canonical-identifier",
            "claim": "ORCID 0000-0001-6232-9096 identifies Daniel Ari Friedman. It publicly links the secondary Google Scholar profile Y2bMf3MAAAAJ; DXjPFtYAAAAJ is the canonical metrics profile under this repository's direct-authenticated Scholar policy.",
            "status": "public-identifier",
            "sources": [
                "https://orcid.org/0000-0001-6232-9096",
                "https://pub.orcid.org/v3.0/0000-0001-6232-9096/person",
                "data/scholar-snapshot.json",
                "data/scholar-verification-receipt.json",
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "ORCID's public person record confirms the identifier and secondary Scholar link. The canonical metrics-profile decision is bounded by the direct authenticated Scholar receipt, not inferred from ORCID.",
            "maintenance_owner": "ARCHIVIST",
            "caveat": "ORCID does not itself designate a canonical Scholar profile. Keep all public metrics tied to DXjPFtYAAAAJ only when the direct authenticated receipt remains valid.",
        },
        {
            "id": "curio-cards-early-ethereum-art",
            "claim": "Daniel Friedman created Curio Cards 24, 25, and 26, part of a collection that debuted on Ethereum on May 9, 2017; all original cards were minted in 2017. A full set of 30 cards plus 17b, representing seven artists, sold at Christie's New York in September 2021 for 393 ETH ($1,202,108).",
            "status": "public-profile",
            "sources": [
                "https://curio.cards/artist/danielfriedman/",
                "https://docs.curio.cards/the-artists/daniel-friedman",
                "https://docs.curio.cards/",
                "https://docs.curio.cards/faqs",
                "https://www.christies.com/en/lot/lot-6337619",
                "https://www.christies.com/en/stories/a-to-z-nft-collecting-guide-b9f875b864c7488eb094595ced7d60cd",
                "papers/2024_CurioCards/README.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "Curio's official artist and project documentation confirms the card attribution, collection debut, and 2017 minting window. Christie's first-party material confirms the New York sale amount, artist count, and September 2021 date; the lot page identifies the specific Curio set.",
            "maintenance_owner": "RESEARCHER",
            "caveat": "Do not claim that cards 24-26 were individually minted on May 9: the collection debuted then and its cards were released in groups during 2017. Avoid unqualified first/earliest-NFT superlatives and treat the exact Christie's lot number as first-party metadata.",
        },
        _scholar_claim(),
        {
            "id": "stanford-phd",
            "claim": "Daniel Ari Friedman earned a PhD at Stanford University with dissertation record pb813wm1484.",
            "status": "public-institutional-record",
            "sources": [
                "https://purl.stanford.edu/pb813wm1484",
                "https://purl.stanford.edu/pb813wm1484.mods",
                "papers/2019_PhDDissertation/README.md",
                "pages/PROFILE.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "Stanford's MODS dissertation record names Daniel Ari Friedman, Stanford Biology, a 2019 PhD thesis, and Deborah M. Gordon as degree supervisor.",
            "maintenance_owner": "RESEARCHER",
            "caveat": "Use the Stanford PURL as the public institutional source.",
        },
        {
            "id": "nsf-postdoc-affiliation",
            "claim": "Daniel Ari Friedman held NSF Postdoctoral Fellowship in Biology award DBI-2010290 from 2020-10-01 through 2023-09-30, conducted at UC Davis and co-trained by Brian Johnson and Tim Linksvayer.",
            "status": "public-grant-record",
            "sources": [
                "https://api.nsf.gov/services/v1/awards/2010290.json",
                "https://grantome.com/grant/NSF/DBI-2010290",
                "pages/PROFILE.md",
                "README.md",
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "NSF's award API names PI Daniel A. Friedman, UC Davis performance location, the named co-training arrangement, and the 2020-10-01 to 2023-09-30 award dates.",
            "maintenance_owner": "RESEARCHER",
            "caveat": "Cite the NSF award ID and its official start/expiration dates. Do not infer a separate 2020-2022 budget period or a no-cost extension from this record.",
        },
        {
            "id": "aii-officer-roles",
            "claim": "Active Inference Institute officers: Daniel Friedman is President and Treasurer, and Alexandra Mikhailova is Vice President and Secretary. Virginia Bleu Knight is a current Board member. The Institute is a 501(c)(3) public charity, EIN 88-2985125, with an IRS ruling in March 2024.",
            "status": "public-profile",
            "sources": [
                "https://activeinference.institute/structure/officers/",
                "https://activeinference.institute/structure/board-of-directors/",
                "https://projects.propublica.org/nonprofits/organizations/882985125",
                "pages/DISCOVERY.md",
                "pages/PROFILE.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "Current AII officer and board pages establish the roles and board membership; ProPublica's IRS-derived record corroborates the 501(c)(3) status, EIN, and ruling month.",
            "maintenance_owner": "INTEGRATOR",
            "caveat": "Officer and board roles are time-sensitive. The refreshed sources do not re-establish historical office dates for Knight; keep any such history separately dated.",
        },
        {
            "id": "aii-board-count",
            "claim": "The Active Inference Institute board page lists 11 current members.",
            "status": "public-profile",
            "sources": [
                "https://activeinference.institute/structure/board-of-directors/",
                "pages/LINKS.md",
                "pages/WIKIPEDIA.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "high",
            "verification_method": "Current AII board page.",
            "maintenance_owner": "INTEGRATOR",
            "caveat": "Board membership is time-sensitive; retain access dates in narrative pages.",
        },
        {
            "id": "aii-scientific-advisory-board-count",
            "claim": "The Active Inference Institute site lists 32 current Scientific Advisory Board members.",
            "status": "public-profile",
            "sources": [
                "https://activeinference.institute/structure/scientific-advisory-board/",
                "pages/LINKS.md",
                "pages/DISCOVERY.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "medium",
            "verification_method": "Current AII Scientific Advisory Board page lists 32 current members, of whom 31 link to a public page.",
            "maintenance_owner": "INTEGRATOR",
            "caveat": "State this as the current public membership count, not a cohort announcement or a claim about any specific announcement month.",
        },
        {
            "id": "aii-textbook-cohorts",
            "claim": "AII's Textbook Group reports nine completed 2022-textbook cohorts and a first 2026 Fundamentals cohort currently live.",
            "status": "curated-program-copy",
            "sources": [
                "https://activeinference.institute/projects/textbook-group/",
                "README.md",
                "pages/VIDEOS.md"
            ],
            "checked_at": "2026-08-26",
            "confidence": "medium",
            "verification_method": "Current AII Textbook Group page states nine cohorts on the 2022 textbook and a live first 2026 Fundamentals cohort.",
            "maintenance_owner": "EDUCATOR",
            "caveat": "The total is ten cohorts only when the current live 2026 cohort is included; do not describe all ten as completed.",
        },
        {
            "id": "college-of-the-redwoods-teaching",
            "claim": "Profile teaching copy lists BIOL-1 at Pelican Bay for Spring and Fall 2026 and BIOL-8 Human Biology for Spring 2026.",
            "status": "principal-confirmed",
            "sources": ["README.md", "index.html", "pages/PROFILE.md", "pages/VERIFICATION_LOG.md"],
            "checked_at": "2026-08-26",
            "confidence": "medium",
            "verification_method": "Principal-confirmed instructor-of-record update supplied 2026-08-26 and synchronized across profile source surfaces.",
            "maintenance_owner": "EDUCATOR",
            "caveat": "Fall 2026 BIOL-1 is principal-confirmed, not represented as a public-schedule verification. The update makes no claim about BIOL-8 after Spring 2026.",
        },
        {
            "id": "cogsec-role",
            "claim": "COGSEC.org is the cognitive security publication and research context linked from the profile.",
            "status": "public-site",
            "sources": [
                "https://www.cogsec.org/r-d-initiatives-3",
                "https://www.cogsec.org/2021-research-initiative-brief-nim-8",
                "https://pubmed.ncbi.nlm.nih.gov/38735269/",
                "README.md",
                "pages/PROFILE.md",
            ],
            "checked_at": "2026-08-26",
            "confidence": "medium",
            "verification_method": "COGSEC's public R&D initiative pages describe research-output activity; PubMed record PMID 38735269 identifies the Cognitive Security & Education Forum affiliation.",
            "maintenance_owner": "RESEARCHER",
            "caveat": "Prefer COGSEC pages for COGSEC-specific publication claims.",
        },
    ]


def _latest_source(pattern: str, _fallback: str) -> str:
    try:
        latest = latest_source_report(pattern)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"export_agent_data: no report matches {pattern!r}; refusing a stale fallback link"
        ) from None
    return rel(latest)


def _existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def _hydrate_claim_checks(*, enforce_stale_checks: bool = True) -> list[dict]:
    claims = []
    latest_snapshot = _latest_source("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json")
    latest_inventory = _latest_source("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json")
    snapshot = _latest_snapshot_payload()
    payload_json = _current_counts_payload()
    payload_counts = payload_json.get("counts", {})
    work_count = payload_counts.get("bibliography_works", _current_work_count())
    folder_count = payload_counts.get("paper_folder_docs", _current_paper_folder_count())
    _, catalogued_aii = parse_software_catalog_counts()
    counts_payload = _current_counts_payload().get("counts", {}).get("github_inventory", {})
    docxology_public_repos = _snapshot_value(snapshot, "GitHub user docxology", "public_repos")
    if docxology_public_repos is None:
        docxology_public_repos = counts_payload.get("docxology")
    aii_public_repos = _snapshot_value(snapshot, "GitHub user ActiveInferenceInstitute", "public_repos")
    if aii_public_repos is None:
        aii_public_repos = counts_payload.get("ActiveInferenceInstitute")
    source_counts_timestamp = payload_json.get("generated_at")
    source_public_source_timestamp = snapshot.get("generated_at")
    stale: list[str] = []
    stale_claims = {claim.get("id"): claim for claim in _claims()}
    if enforce_stale_checks:
        for claim_id in (
            "curated-work-count",
            "paper-folder-count",
            "docxology-github-public-repos",
            "aii-github-public-repos",
        ):
            claim = stale_claims.get(claim_id)
            if claim:
                stale.extend(
                    _stale_claim_fragment_errors(
                        claim,
                        work_count,
                        folder_count,
                        docxology_public_repos,
                        aii_public_repos,
                        source_counts_timestamp=source_counts_timestamp,
                        source_public_source_timestamp=source_public_source_timestamp,
                    )
                )
    if stale:
        raise SystemExit("Volatile claim fragments are stale: " + "; ".join(stale))
    for claim in _claims():
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
            claim_copy["caveat"] = (
                "Use /users/ActiveInferenceInstitute, not /orgs/. "
                f"Local software catalog tracks {catalogued_aii} AII repositories with docxology contributions."
            )
        # Do not stamp claim_copy["checked_at"] with the export run's timestamp here:
        # every claim in _claims() already carries its own checked_at, set from when it
        # was actually verified (a Scholar fetch date, a live-count snapshot date, or a
        # manual review date). Overwriting it with "now" on every regen falsely implied
        # every claim had just been re-verified.
        claim_copy["sources"] = [
            latest_snapshot if source.startswith("reports/public_source_snapshot_") else
            latest_inventory if source.startswith("reports/public_source_inventory_") else source
            for source in claim_copy.get("sources", [])
        ]
        claims.append(claim_copy)
    return claims


def render_outputs(generated_at: str | None = None, *, enforce_stale_checks: bool = True) -> dict[Path, str]:
    software = parse_software()
    generated_at = generated_at or generated_timestamp()
    claims = _hydrate_claim_checks(enforce_stale_checks=enforce_stale_checks)
    return {
        REPO_ROOT / "data" / "software.json": json.dumps(
            {
                "generated_at": generated_at,
                "source": "pages/SOFTWARE.md",
                "schema_ref": "/data/agent-index.json#schemas/SoftwareRepository",
                "count": len(software),
                "repositories": software,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        REPO_ROOT / "data" / "people.json": json.dumps(
            {"generated_at": generated_at, "schema_ref": "/data/agent-index.json#schemas/Person", "people": PEOPLE},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        REPO_ROOT / "data" / "organizations.json": json.dumps(
            {
                "generated_at": generated_at,
                "schema_ref": "/data/agent-index.json#schemas/Organization",
                "organizations": ORGANIZATIONS,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        REPO_ROOT / "data" / "claims.json": json.dumps(
            {"generated_at": generated_at, "schema_ref": "/data/agent-index.json#schemas/ClaimWithEvidence", "claims": claims},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    generated_at = _existing_generated_at(REPO_ROOT / "data" / "claims.json") if args.check else None
    if not args.check:
        candidate_outputs = render_outputs(enforce_stale_checks=False)
        stable_values = [
            stable_generated_at(path, json.loads(content))
            for path, content in candidate_outputs.items()
        ]
        if stable_values and all(value and value == stable_values[0] for value in stable_values):
            generated_at = stable_values[0]
    outputs = render_outputs(generated_at, enforce_stale_checks=args.check)
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
