#!/usr/bin/env python3
"""Diff every live Zenodo record under the profile's ORCID against the curated bibliography.

sync_paired_publications.py only emits a report row for a Zenodo record that has
some GitHub-release evidence -- a record with no matching release is silently
absent from its pairs/actions/needs_review output, not flagged. This script
closes that blind spot: it diffs every Zenodo record for the profile against
pages/BIBLIOGRAPHY.md directly. By default it re-fetches the same live Zenodo
query the pairing tool uses; pass
``--records-from <paired_publications_report.json>`` to reuse the same-day
pairing scan's records instead (``--force`` lifts the same-day requirement).

Two independent findings, not one:

- ``uncatalogued``: neither the record's concept DOI nor its version-specific
  DOI (``10.5281/zenodo.<record_id>``) appears anywhere in the bibliography --
  a genuine gap. Belongs in the bibliography via
  ``add_zenodo_only.py <record_id>`` (see docs/operations/publication-sync.md).
  A software-type record (a GitHub-release archive) whose concept DOI is
  linked from the ``pages/SOFTWARE.md`` row of a repository whose ``[📄]``
  paper folder the bibliography already cites is that work's software
  supplement: it is listed under ``software_catalogued`` and later releases
  under the same concept need no new entry. Any other record, including a
  software-typed one from a row without a catalogued paper, stays uncatalogued.
  An exact accepted ``software-catalog`` review may instead classify one
  version as a supplemental source archive. Its upstream type is retained;
  frozen report bytes, the complete record and current catalog links must match.
- ``non_canonical_doi``: the record IS represented, but only under its
  version-specific DOI, not the documented canonical concept DOI
  ("Canonical DOI = Zenodo concept DOI", docs/operations/publication-sync.md).
  The yearly AII-Ecosystem snapshots are a documented, deliberate exception to
  this rule. Approved exceptions remain visible in the report and are checked
  against their exact record identity; every other row is actionable drift.

Matching uses every bibliography row with a DOI, not just rows with a local
``papers/`` folder (existing_doi_map() in sync_paired_publications.py requires
a folder, which produces false positives for cited-but-folderless rows such as
playbooks/video transcripts that were never given a paper folder).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.report_paths import (  # noqa: E402
    dated_report_path,
    generated_timestamp,
    latest_report,
    report_date_string,
)

from docxology_tools.publication_pairing import (  # noqa: E402
    ZenodoRecord,
    canonical_pair_candidate_fingerprint,
    decision_pair_candidate_fingerprint,
    is_software_record,
    release_identity_from_url,
    reviewed_pair_decision_index,
)
from docxology_tools.software_table import (  # noqa: E402
    iter_software_rows,
    paper_path,
    software_catalog_dois,
    zenodo_link_dois,
)
from docxology_tools.public_integrity import redact_local_paths  # noqa: E402
from sync_paired_publications import (  # noqa: E402
    fetch_zenodo_records,
    parse_bibliography_rows,
    zenodo_record_from_payload,
    zenodo_records_from_payload,
)

OUT = dated_report_path("zenodo_uncatalogued", "json")

# Superseded Zenodo versions retained by the source registry but deliberately
# not catalogued as new works. The current bibliography cites the replacement
# concept/version for each; software-only and software-supplement records are
# instead curated on pages/SOFTWARE.md (catalog row citing the concept DOI)
# with no bibliography row. Keep this explicit so the freshness gate measures
# actionable drift rather than known release-history records.
KNOWN_STALE_RECORD_IDS = {
    "21418901",  # SynthOBS v1.618.0; current row cites concept 21418782
    "20804586",  # CogSecSkills v1; current row cites concept 21513316
    "19139090",  # Template/Reproducible duplicate of kept row #1
    "22666981",  # Software-only supplement to the CCD paper; paper row cites concept 10.5281/zenodo.19695259
    "22817425",  # daf-jev software release archive; catalogued in SOFTWARE.md citing concept 10.5281/zenodo.22816187; no bibliography row (software-only record)
    "22667290",  # EvoJump v0.5.2 canonical curated deposit per R80 (software-catalog acceptance); work represented by the software row and paper row #12 (concept 10.5281/zenodo.17229924)
    "22667291",  # EvoJump v0.5.2 GitHub-Zenodo automated integration archive per R81 (superseded); kept record is 22667290
    "22760881",  # CCD software revision archive v2.6.0 (supplement to paper row #112, concept 10.5281/zenodo.19695259); code catalogued as cognitive_case_diagrams — same class as 22666981
}

# These records are intentionally cited by their version DOI because each is
# a separately curated bibliographic snapshot, not merely a software release
# superseded by its Zenodo concept record. Keep the exact identity here rather
# than a bare record-ID allowlist: a changed title, concept DOI, bibliography
# DOI role, or missing record must become a visible, failing review item.
VERSION_SPECIFIC_CITATION_EXCEPTIONS = {
    "17982447": {
        "title": "The Active Inference Institute & Active Inference Ecosystem",
        "concept_doi": "10.5281/zenodo.14108991",
        "version_doi": "10.5281/zenodo.17982447",
        "reason": (
            "AII Ecosystem v3 is a separately curated 2025 bibliographic "
            "snapshot, distinct from the earlier v2 concept record."
        ),
    },
    "15168382": {
        "title": "On Time",
        "concept_doi": "10.5281/zenodo.15168381",
        "version_doi": "10.5281/zenodo.15168382",
        "reason": (
            "On Time is a separately curated 2025 paper snapshot; all "
            "references were deliberately pointed at version record "
            "15168382 in commit d086e7a3 (2026-08-22)."
        ),
    },
}


def version_doi(record: ZenodoRecord) -> str:
    """The record's own per-version DOI, independent of ZenodoRecord.doi's concept-DOI preference."""
    return f"10.5281/zenodo.{record.record_id}" if record.record_id else ""


def bibliography_doi_set(repo_root: Path = REPO_ROOT) -> set[str]:
    """Every DOI cited in the bibliography, regardless of whether the row has a papers/ folder."""
    return {row["doi"] for row in parse_bibliography_rows(repo_root) if row["doi"]}


def _in_bibliography(record: ZenodoRecord, catalogued_dois: set[str]) -> bool:
    return record.doi in catalogued_dois or version_doi(record) in catalogued_dois


def software_catalogued_records(
    records: list[ZenodoRecord],
    catalogued_dois: set[str],
    software_dois: dict[str, dict[str, str]],
) -> list[ZenodoRecord]:
    """Software records outside the bibliography that supplement a catalogued work's software row."""
    return [
        record
        for record in records
        if record.record_id not in KNOWN_STALE_RECORD_IDS
        and not _in_bibliography(record, catalogued_dois)
        and is_software_record(record)
        and record.doi.casefold() in software_dois
    ]


def uncatalogued_records(
    records: list[ZenodoRecord],
    catalogued_dois: set[str],
    software_dois: dict[str, dict[str, str]] | None = None,
    *,
    reviewed_archive_ids: set[str] | None = None,
) -> list[ZenodoRecord]:
    """Records cited nowhere: not in the bibliography and not a software-catalogued archive."""
    software_ids = {
        record.record_id
        for record in software_catalogued_records(
            records, catalogued_dois, software_dois or {}
        )
    }
    return [
        record
        for record in records
        if record.record_id not in KNOWN_STALE_RECORD_IDS
        and not _in_bibliography(record, catalogued_dois)
        and record.record_id not in software_ids
        and record.record_id not in (reviewed_archive_ids or set())
    ]


def _review_json(repo_root: Path, relative: str, limit: int) -> tuple[str, dict]:
    """Read bounded, independent local evidence without following links."""
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts or "\\" in relative:
        raise ValueError("invalid review evidence path")
    root = repo_root.resolve()
    if any((root / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
        raise ValueError("symlinked review evidence is unavailable")
    path = root / relative
    if not path.is_file() or path.stat().st_nlink != 1:
        raise ValueError("review evidence must be an independent regular file")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("review evidence exceeds its bounded reader")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("review evidence must be a JSON object")
    return hashlib.sha256(raw).hexdigest(), payload


def reviewed_source_archives(
    repo_root: Path,
    records: list[ZenodoRecord],
    software_dois: dict[str, dict[str, str]],
    *,
    catalogued_dois: set[str] | None = None,
) -> tuple[list[dict], list[dict]]:
    """Resolve only exact accepted source-archive reviews, preserving API types.

    A concept link, title, ZIP extension or historical pairing is insufficient.
    Each grant binds a version record, full frozen record, candidate identity,
    source-report bytes and the current software/bibliography relationship.
    Historical decisions outside this observation, and records already covered
    by ordinary catalog rules, do not require an exception or create drift.
    """
    catalogued = bibliography_doi_set(repo_root) if catalogued_dois is None else catalogued_dois
    active = uncatalogued_records(records, catalogued, software_dois)
    if not active:
        return [], []
    ledger_path = repo_root / "data/paired-publication-decisions.json"
    if not ledger_path.exists() and not ledger_path.is_symlink():
        return [], []
    try:
        _, ledger = _review_json(repo_root, "data/paired-publication-decisions.json", 4 * 1024 * 1024)
        decisions = reviewed_pair_decision_index(ledger)
        by_id = {record.record_id: record for record in active}
        if len(by_id) != len(active):
            raise ValueError("duplicate observed Zenodo record identities")
        rows = list(iter_software_rows(repo_root / "pages/SOFTWARE.md"))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return [], [{"record_id": "decision-ledger", "reason": redact_local_paths(str(exc))}]

    approved: dict[str, dict] = {}
    blocked: set[str] = set()
    drift: list[dict] = []
    sources: dict[str, tuple[str, dict]] = {}
    for group in ledger["groups"]:
        if not isinstance(group, dict) or group.get("representation") != "software-catalog":
            continue
        candidates = group.get("raw_candidates")
        if not isinstance(candidates, list):
            continue
        for raw in candidates:
            if not isinstance(raw, dict) or not raw.get("zenodo_version_record_id"):
                continue
            record_id = raw["zenodo_version_record_id"]
            if not isinstance(record_id, str) or record_id not in by_id:
                # A durable decision is not an assertion that its historical
                # record must appear in every later observation or query.
                continue
            fingerprint = decision_pair_candidate_fingerprint(raw, group)
            decision = decisions.get(fingerprint)
            if (
                decision is None
                or decision["group_id"] != group.get("id")
                or decision["decision"] not in {"accept", "accepted"}
            ):
                continue
            try:
                if not isinstance(record_id, str) or not re.fullmatch(r"[1-9][0-9]*", record_id):
                    raise ValueError("review must name an exact numeric version record")
                record = by_id[record_id]
                catalog = software_dois.get(record.doi.casefold())
                if not catalog or group.get("folder") != catalog["paper_folder"]:
                    raise ValueError("review no longer matches a catalogued paper/software link")
                repository, tag = release_identity_from_url(fingerprint[1])
                if repository.casefold() != fingerprint[3] or tag != fingerprint[5]:
                    raise ValueError("reviewed repository/tag differs from its release URL")
                if not any(
                    f"{row.owner}/{row.name}".casefold() == fingerprint[3]
                    and row.url.rstrip("/").casefold() == f"https://github.com/{fingerprint[3]}"
                    and row.name == catalog["software_row"]
                    and Path(paper_path(row.description_raw)).name == catalog["paper_folder"]
                    and record.doi.casefold() in {doi.casefold() for doi in zenodo_link_dois(row.description_raw)}
                    for row in rows
                ):
                    raise ValueError("reviewed repository does not own the current catalog row")
                source = raw.get("source_report")
                digest = raw.get("source_report_sha256")
                if (
                    not isinstance(source, str)
                    or not re.fullmatch(r"reports/(?:publication_intake|paired_publications)_\d{4}-\d{2}-\d{2}\.json", source)
                    or not isinstance(digest, str)
                    or not re.fullmatch(r"[0-9a-f]{64}", digest)
                ):
                    raise ValueError("review requires an exact local source report and SHA-256")
                if source not in sources:
                    sources[source] = _review_json(repo_root, source, 32 * 1024 * 1024)
                source_digest, payload = sources[source]
                if source_digest != digest:
                    raise ValueError("frozen source report SHA-256 changed")
                if payload.get("source") != "GitHub Releases API + Zenodo Records API" or payload.get("warnings") != []:
                    raise ValueError("frozen source report has unavailable scan evidence")
                frozen = zenodo_records_from_payload(payload)
                frozen_by_id = {item.record_id: item for item in frozen}
                if len(frozen_by_id) != len(frozen):
                    raise ValueError("frozen source report repeats a version record identity")
                if record_id not in frozen_by_id or record.to_dict() != frozen_by_id[record_id].to_dict():
                    raise ValueError("observed record or complete file manifest differs from the reviewed source")
                pairs = payload.get("pairs")
                matched = False
                for pair in (pairs if isinstance(pairs, list) else []):
                    if not isinstance(pair, dict):
                        continue
                    item, release = pair.get("record"), pair.get("release")
                    if not isinstance(item, dict) or not isinstance(release, dict):
                        continue
                    candidate = canonical_pair_candidate_fingerprint(
                        doi=pair.get("doi"), github_release_url=pair.get("github_release_url"),
                        zenodo_record_url=pair.get("zenodo_record_url"), github_repo=pair.get("github_repo"),
                        title=item.get("title"), release_tag=release.get("tag"),
                    )
                    if candidate == fingerprint and item == record.to_dict():
                        matched = True
                if not matched:
                    raise ValueError("exact reviewed pairing candidate is absent from the frozen report")
                if record_id in approved or record_id in blocked:
                    raise ValueError("multiple accepted archive reviews name the same version record")
                approved[record_id] = {
                    "record_id": record_id, "concept_doi": record.doi, "title": record.title,
                    "resource_type": record.resource_type, **catalog,
                    "decision_group": decision["group_id"],
                    "decision_sha256": hashlib.sha256(
                        json.dumps(group, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                    ).hexdigest(),
                    "source_report": source, "source_report_sha256": digest,
                    "record": record.to_dict(),
                }
            except (OSError, ValueError, TypeError, KeyError) as exc:
                blocked.add(str(record_id))
                approved.pop(str(record_id), None)
                drift.append({"record_id": str(record_id), "decision_group": decision["group_id"], "reason": redact_local_paths(str(exc))})
    return [approved[key] for key in sorted(approved)], drift


def non_canonical_doi_records(
    records: list[ZenodoRecord], catalogued_dois: set[str]
) -> list[ZenodoRecord]:
    """All records cited only by their version DOI, not their concept DOI.

    This deliberately includes approved exceptions. ``build_report`` divides
    the result into reviewed exceptions and unresolved drift so that a broad
    record-ID allowlist can never make a future DOI-role change invisible.
    """
    return [
        record
        for record in records
        if record.doi
        and version_doi(record)
        and record.doi != version_doi(record)
        and record.doi not in catalogued_dois
        and version_doi(record) in catalogued_dois
    ]


def approved_version_specific_doi_exceptions(
    records: list[ZenodoRecord], catalogued_dois: set[str]
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """Return explicitly approved exception rows and any identity drift.

    The exception registry is intentionally a complete assertion, not a
    suppression rule. A configured record must be returned by Zenodo and must
    still have the expected title, concept DOI, version DOI, and version-only
    bibliography role. Anything else is a review failure.
    """
    records_by_id = {record.record_id: record for record in records}
    approved: list[dict[str, str]] = []
    drift: list[dict[str, object]] = []

    for record_id, expected in VERSION_SPECIFIC_CITATION_EXCEPTIONS.items():
        record = records_by_id.get(record_id)
        if record is None:
            drift.append(
                {
                    "record_id": record_id,
                    "expected": {"record_id": record_id, **expected},
                    "observed": None,
                    "mismatches": ["record_not_returned_by_zenodo"],
                }
            )
            continue

        observed_version_doi = version_doi(record)
        version_only = record in non_canonical_doi_records([record], catalogued_dois)
        observed = {
            "record_id": record.record_id,
            "title": record.title,
            "concept_doi": record.doi,
            "version_doi": observed_version_doi,
            "version_only_bibliography_citation": version_only,
        }
        mismatches = [
            field
            for field in ("title", "concept_doi", "version_doi")
            if observed[field] != expected[field]
        ]
        if not version_only:
            mismatches.append("version_only_bibliography_citation")
        if mismatches:
            drift.append(
                {
                    "record_id": record_id,
                    "expected": {"record_id": record_id, **expected},
                    "observed": observed,
                    "mismatches": mismatches,
                }
            )
            continue

        approved.append(
            {
                "record_id": record_id,
                "title": record.title,
                "concept_doi": record.doi,
                "version_doi_in_bibliography": observed_version_doi,
                "reason": expected["reason"],
            }
        )

    return approved, drift


def build_report(
    repo_root: Path = REPO_ROOT,
    *,
    records: list[ZenodoRecord] | None = None,
    records_source: str = "live",
    records_source_report: str | None = None,
) -> dict[str, object]:
    """Diff records against the bibliography; ``records`` injects cached records."""
    if records is None:
        records, warnings = fetch_zenodo_records()
    else:
        warnings = []
    catalogued = bibliography_doi_set(repo_root)
    software_dois = software_catalog_dois(repo_root)
    software_catalogued = software_catalogued_records(
        records, catalogued, software_dois
    )
    archive_observations = uncatalogued_records(records, catalogued, software_dois)
    reviewed_archives, archive_drift = reviewed_source_archives(
        repo_root, archive_observations, software_dois, catalogued_dois=catalogued
    )
    missing = uncatalogued_records(
        records, catalogued, software_dois,
        reviewed_archive_ids={item["record_id"] for item in reviewed_archives},
    )
    version_only = non_canonical_doi_records(records, catalogued)
    approved_exceptions, exception_drift = approved_version_specific_doi_exceptions(
        records, catalogued
    )
    approved_record_ids = {item["record_id"] for item in approved_exceptions}
    non_canonical = [
        record for record in version_only if record.record_id not in approved_record_ids
    ]
    return {
        "generated_at": generated_timestamp(),
        "zenodo_records_fetched": len(records),
        "zenodo_records_source": {
            "mode": records_source,
            "source_report": records_source_report,
        },
        "bibliography_dois": len(catalogued),
        "uncatalogued_count": len(missing),
        "software_catalogued_count": len(software_catalogued),
        "reviewed_source_archive_count": len(reviewed_archives),
        "reviewed_source_archive_context": {
            "schema_version": 1,
            "records": [record.to_dict() for record in archive_observations],
        },
        "reviewed_source_archives": reviewed_archives,
        "reviewed_source_archive_drift_count": len(archive_drift),
        "reviewed_source_archive_drift": archive_drift,
        "non_canonical_doi_count": len(non_canonical),
        "approved_version_specific_doi_exception_count": len(approved_exceptions),
        "version_specific_doi_exception_drift_count": len(exception_drift),
        "warnings": warnings,
        "uncatalogued": [
            {
                "record_id": record.record_id,
                "doi": record.doi,
                "title": record.title,
                "publication_date": record.publication_date,
                "html_url": record.html_url,
            }
            for record in missing
        ],
        "software_catalogued": [
            {
                "record_id": record.record_id,
                "concept_doi": record.doi,
                "title": record.title,
                **software_dois[record.doi.casefold()],
            }
            for record in software_catalogued
        ],
        "non_canonical_doi": [
            {
                "record_id": record.record_id,
                "concept_doi": record.doi,
                "version_doi_in_bibliography": version_doi(record),
                "title": record.title,
            }
            for record in non_canonical
        ],
        "approved_version_specific_doi_exceptions": approved_exceptions,
        "version_specific_doi_exception_drift": exception_drift,
    }


def write_report(
    repo_root: Path = REPO_ROOT,
    *,
    records: list[ZenodoRecord] | None = None,
    records_source: str = "live",
    records_source_report: str | None = None,
) -> Path:
    report = build_report(
        repo_root,
        records=records,
        records_source=records_source,
        records_source_report=records_source_report,
    )
    out = repo_root / "reports" / OUT.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return out


def check_report(
    report_path: Path | None = None, *, repo_root: Path = REPO_ROOT
) -> list[str]:
    """Check reports; new manual grants re-resolve their saved observation context."""
    path = report_path or latest_report("zenodo_uncatalogued_*.json", required=False)
    if path is None:
        return [
            "no zenodo_uncatalogued report found -- run this script without --check first"
        ]
    payload = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    if payload.get("warnings"):
        problems.append(f"API warnings present: {payload['warnings']}")
    count = payload.get("uncatalogued_count", 0)
    if count:
        titles = ", ".join(
            item["title"] for item in payload.get("uncatalogued", [])[:5]
        )
        problems.append(f"{count} Zenodo record(s) not in the bibliography: {titles}")
    non_canonical_count = payload.get("non_canonical_doi_count", 0)
    if non_canonical_count:
        titles = ", ".join(
            item["title"] for item in payload.get("non_canonical_doi", [])[:5]
        )
        problems.append(
            f"{non_canonical_count} Zenodo record(s) use a version DOI without an approved exception: {titles}"
        )
    exception_drift_count = payload.get("version_specific_doi_exception_drift_count", 0)
    if exception_drift_count:
        record_ids = ", ".join(
            item["record_id"]
            for item in payload.get("version_specific_doi_exception_drift", [])[:5]
        )
        problems.append(
            f"{exception_drift_count} approved version-DOI exception(s) drifted: {record_ids}"
        )
    archive_fields = {
        "reviewed_source_archive_count", "reviewed_source_archives",
        "reviewed_source_archive_context", "reviewed_source_archive_drift_count",
        "reviewed_source_archive_drift",
    }
    if not archive_fields.intersection(payload):
        return problems  # Historical reports retain the original contract.
    if not archive_fields.issubset(payload):
        problems.append("Reviewed source archive report is missing required context/receipt fields")
        return problems
    archive_drift = payload["reviewed_source_archive_drift_count"]
    saved_drift = payload["reviewed_source_archive_drift"]
    if (
        isinstance(archive_drift, bool)
        or not isinstance(archive_drift, int)
        or archive_drift < 0
        or not isinstance(saved_drift, list)
        or archive_drift != len(saved_drift)
    ):
        problems.append("Reviewed source archive drift count/list is malformed")
    if archive_drift:
        problems.append(f"{archive_drift} reviewed source archive approval(s) drifted")
    archived = payload["reviewed_source_archives"]
    archive_count = payload["reviewed_source_archive_count"]
    context = payload["reviewed_source_archive_context"]
    if (
        not isinstance(archived, list)
        or isinstance(archive_count, bool)
        or not isinstance(archive_count, int)
        or archive_count != len(archived)
    ):
        problems.append("Reviewed source archive count/list is malformed")
    elif (
        not isinstance(context, dict)
        or isinstance(context.get("schema_version"), bool)
        or context.get("schema_version") != 1
        or not isinstance(context.get("records"), list)
    ):
        problems.append("Reviewed source archive observation context is malformed")
    else:
        try:
            records = []
            for item in context["records"]:
                if not isinstance(item, dict):
                    raise ValueError("malformed saved archive observation")
                records.append(zenodo_record_from_payload(item))
            catalogued = bibliography_doi_set(repo_root)
            software_dois = software_catalog_dois(repo_root)
            current, drift = reviewed_source_archives(
                repo_root, records, software_dois, catalogued_dois=catalogued
            )
            if drift or current != archived:
                problems.append("Reviewed source archive evidence no longer matches its approval/source/catalog")
            if uncatalogued_records(
                records, catalogued, software_dois,
                reviewed_archive_ids={item["record_id"] for item in current},
            ):
                problems.append("Reviewed source archive observation context contains unrepresented records")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            problems.append(f"Reviewed source archive evidence is unavailable: {redact_local_paths(str(exc))}")
    return problems


def load_cached_records(path: Path, *, force: bool = False) -> list[ZenodoRecord]:
    """Reuse the pairing scan's Zenodo records instead of re-fetching the query.

    Fails closed: a non-pairing report, a warned scan, or a non-same-day
    ``generated_at`` is refused (``--force`` lifts only the freshness
    requirement). A cached-but-warned scan must never validate.
    """
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"Cannot read cached Zenodo records from {path}: {exc}"
        ) from exc
    if payload.get("source") != "GitHub Releases API + Zenodo Records API":
        raise SystemExit(
            f"Cannot reuse cached records from {path}: unexpected report source"
        )
    warnings = payload.get("warnings")
    if warnings:
        raise SystemExit(
            f"Refusing cached Zenodo records from {path}: {len(warnings)} API warning(s); "
            "rerun the live scan"
        )
    generated_at = str(payload.get("generated_at") or "")
    if generated_at[:10] != report_date_string() and not force:
        raise SystemExit(
            f"Cached Zenodo records from {path} are not same-day (generated_at {generated_at}); "
            "rerun the pairing scan or pass --force"
        )
    try:
        return zenodo_records_from_payload(payload)
    except ValueError as exc:
        raise SystemExit(
            f"Cannot reuse cached Zenodo records from {path}: {exc}"
        ) from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diff live Zenodo records for this profile against the curated bibliography."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Validate the latest report only (no network call); exit 1 for API warnings, "
            "uncatalogued records, unresolved DOI-role drift, or changed approved exceptions"
        ),
    )
    parser.add_argument(
        "--records-from",
        metavar="PATH",
        help=(
            "Reuse the Zenodo records from a paired_publications report instead of "
            "re-fetching the live query"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --records-from: accept a source report that is not same-day",
    )
    args = parser.parse_args()

    if args.check:
        problems = check_report()
        if problems:
            for problem in problems:
                print(problem)
            return 1
        print("checked zenodo_uncatalogued report: 0 uncatalogued records")
        return 0

    if args.records_from:
        cached_from = Path(args.records_from)
        records = load_cached_records(cached_from, force=args.force)
        print(f"reusing {len(records)} cached Zenodo records from {cached_from}")
        out = write_report(
            records=records,
            records_source="cached",
            records_source_report=str(cached_from),
        )
    else:
        out = write_report()
    report = json.loads(out.read_text(encoding="utf-8"))
    count = report["uncatalogued_count"]
    non_canonical_count = report["non_canonical_doi_count"]
    approved_exception_count = report["approved_version_specific_doi_exception_count"]
    exception_drift_count = report["version_specific_doi_exception_drift_count"]
    if count:
        print(
            f"wrote {out.relative_to(REPO_ROOT)}: {count} record(s) not yet in the bibliography"
        )
        for item in report["uncatalogued"]:
            print(f"  {item['record_id']}  {item['doi']}  {item['title']}")
        print(
            "Add real publications with: uv run python3 code/orchestrators/add_zenodo_only.py <record_id>"
        )
    elif report["reviewed_source_archive_drift_count"]:
        print(
            f"wrote {out.relative_to(REPO_ROOT)}: 0 uncatalogued records; "
            "reviewed source archive evidence requires attention"
        )
    else:
        print(
            f"wrote {out.relative_to(REPO_ROOT)}: 0 uncatalogued records (bibliography is caught up)"
        )
    for item in report["software_catalogued"]:
        print(
            f"  software-catalogued: {item['record_id']}  {item['concept_doi']}  via the {item['software_row']} row (supplements {item['paper_folder']})  {item['title']}"
        )
    for item in report["reviewed_source_archives"]:
        print(
            f"  manually reviewed supplemental source archive: {item['record_id']}  "
            f"{item['concept_doi']} via {item['software_row']} (decision {item['decision_group']})"
        )
    for item in report["reviewed_source_archive_drift"]:
        print(f"  reviewed source archive drift: {item['record_id']}  {item['reason']}")
    if non_canonical_count:
        print(
            f"{non_canonical_count} record(s) cited only by version DOI, not the canonical concept DOI:"
        )
        for item in report["non_canonical_doi"]:
            print(
                f"  {item['record_id']}  bibliography has {item['version_doi_in_bibliography']}, concept is {item['concept_doi']}  {item['title']}"
            )
    if approved_exception_count:
        print(f"{approved_exception_count} approved version-specific DOI exception(s):")
        for item in report["approved_version_specific_doi_exceptions"]:
            print(
                f"  {item['record_id']}  bibliography has {item['version_doi_in_bibliography']}, "
                f"concept is {item['concept_doi']}  {item['title']}"
            )
    if exception_drift_count:
        print(
            f"{exception_drift_count} approved version-specific DOI exception(s) drifted:"
        )
        for item in report["version_specific_doi_exception_drift"]:
            print(f"  {item['record_id']}  {', '.join(item['mismatches'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
