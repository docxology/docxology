#!/usr/bin/env python3
"""Review-gated reconciliation of paper-folder DOI roles.

``pages/BIBLIOGRAPHY.md`` owns the citation DOI.  Folder metadata may retain a
different version/download identifier only as ``artifact_doi``.  This command
first writes a deterministic proposed-reconciliation report; an apply run must
be explicitly bound to that unchanged proposal, preventing a broad metadata
rewrite from being silently accepted after its review surface has changed.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from biblio_table import iter_bibliography_rows  # noqa: E402
from regenerate_docs import DOI_TRAILING, DOI_RE  # noqa: E402

BIBLIOGRAPHY = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"
PAPERS = REPO_ROOT / "papers"
SCHEMA_VERSION = "1.0"
APPROVAL_SCHEMA_VERSION = "1.0"


def extract_doi(value: object) -> str:
    """Normalize the DOI portion of a bibliography or metadata field."""
    match = DOI_RE.search(str(value or ""))
    return match.group(0).rstrip(DOI_TRAILING) if match else ""


def resolver(doi: str) -> str:
    return f"https://doi.org/{doi}" if doi else ""


def canonical_dois() -> dict[str, str]:
    """Map bibliography folder IDs to their canonical citation DOI."""
    result: dict[str, str] = {}
    for row in iter_bibliography_rows(BIBLIOGRAPHY):
        if row.folder:
            doi = extract_doi(row.link_cell)
            if doi:
                result[row.folder] = doi
    return result


def metadata_paths() -> dict[str, Path]:
    """Return existing per-folder source metadata paths, sorted by folder."""
    return {
        directory.name: directory / "metadata.json"
        for directory in sorted(PAPERS.glob("????_*"))
        if (directory / "metadata.json").is_file()
    }


def source_digest(paths: dict[str, Path]) -> str:
    """Hash the exact sources a reviewer approved, including the bibliography."""
    digest = hashlib.sha256()
    for path in [BIBLIOGRAPHY, *[paths[key] for key in sorted(paths)]]:
        relative = path.relative_to(REPO_ROOT).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    """Return a digest of an exact review artifact without normalizing it."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def actions_sha256(actions: list[dict[str, str]]) -> str:
    """Bind an approval to the exact, ordered DOI-role actions."""
    rendered = json.dumps(actions, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def proposed_actions(
    canonical: dict[str, str], paths: dict[str, Path], *, repo_root: Path = REPO_ROOT
) -> list[dict[str, str]]:
    """Create conservative DOI role changes without writing source files."""
    actions: list[dict[str, str]] = []
    for folder in sorted(set(canonical) & set(paths)):
        path = paths[folder]
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.relative_to(repo_root)} must contain a JSON object")
        canonical_doi = canonical[folder]
        raw_doi = str(data.get("doi") or "").strip()
        raw_artifact = str(data.get("artifact_doi") or "").strip()
        existing_doi = extract_doi(raw_doi)
        existing_artifact = extract_doi(raw_artifact)
        if raw_doi and not existing_doi:
            raise ValueError(f"{folder}: metadata doi is nonempty but malformed; requires manual DOI-role review")
        if raw_artifact and not existing_artifact:
            raise ValueError(f"{folder}: artifact_doi is nonempty but malformed; requires manual DOI-role review")
        if existing_doi.casefold() == canonical_doi.casefold():
            continue
        if existing_artifact and existing_doi and existing_artifact.casefold() != existing_doi.casefold():
            raise ValueError(
                f"{folder}: existing artifact_doi differs from metadata doi; requires manual DOI-role review"
            )
        actions.append(
            {
                "folder": folder,
                "metadata_path": path.relative_to(repo_root).as_posix(),
                "prior_canonical_doi": existing_doi,
                "canonical_doi": canonical_doi,
                "artifact_doi": existing_doi if existing_doi else "",
                "action": "set_canonical_and_preserve_prior_as_artifact" if existing_doi else "set_canonical_doi",
            }
        )
    return actions


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def render_report(
    actions: list[dict[str, str]], digest: str, *, status: str, approval: dict[str, str] | None = None
) -> dict[str, Any]:
    """Render a reviewable proposal/receipt with no accidental source mutation."""
    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": timestamp(),
        "status": status,
        "canonical_source": "pages/BIBLIOGRAPHY.md",
        "canonical_field": "doi",
        "artifact_field": "artifact_doi",
        "source_sha256": digest,
        "summary": {
            "actions": len(actions),
            "canonical_doi_corrections": sum(1 for action in actions if action["prior_canonical_doi"]),
            "backfills": sum(1 for action in actions if not action["prior_canonical_doi"]),
        },
        "actions": actions,
        "review_note": "Review this proposed record before applying. The apply command rejects any source or action drift.",
    }
    if approval is not None:
        report["approval"] = approval
    return report


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    """Write a small JSON receipt atomically after all validation has passed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def validate_approval(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    """Require an unchanged proposal before consulting its separate approval."""
    try:
        approved = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing approved DOI reconciliation report: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid approved DOI reconciliation report {path}: {exc}") from exc
    if not isinstance(approved, dict) or approved.get("status") != "proposed":
        raise ValueError("approved DOI reconciliation report must have status 'proposed'")
    for field in ("schema_version", "canonical_source", "canonical_field", "artifact_field", "source_sha256", "actions"):
        if approved.get(field) != expected.get(field):
            raise ValueError(f"approved DOI reconciliation report drifted in {field}")
    return approved


def validate_review_approval(
    path: Path, proposal_path: Path, proposal: dict[str, Any]
) -> dict[str, str]:
    """Validate a separately authored approval bound to one exact proposal."""
    if path.resolve() == proposal_path.resolve():
        raise ValueError("DOI approval must be a separate record, not the generated proposal")
    try:
        approval = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing DOI reconciliation approval record: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid DOI reconciliation approval record {path}: {exc}") from exc
    if not isinstance(approval, dict):
        raise ValueError("DOI reconciliation approval record must be a JSON object")
    if approval.get("schema_version") != APPROVAL_SCHEMA_VERSION:
        raise ValueError("DOI reconciliation approval record has an unsupported schema_version")
    if approval.get("decision") != "approved":
        raise ValueError("DOI reconciliation approval decision must be 'approved'")
    if approval.get("proposal_sha256") != file_sha256(proposal_path):
        raise ValueError("DOI reconciliation approval does not bind the supplied proposal")
    if approval.get("source_sha256") != proposal.get("source_sha256"):
        raise ValueError("DOI reconciliation approval source digest does not match the proposal")
    if approval.get("actions_sha256") != actions_sha256(proposal["actions"]):
        raise ValueError("DOI reconciliation approval actions digest does not match the proposal")
    reviewer = approval.get("reviewed_by")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError("DOI reconciliation approval requires reviewed_by")
    reviewed_at = approval.get("reviewed_at")
    if not isinstance(reviewed_at, str) or not reviewed_at.strip():
        raise ValueError("DOI reconciliation approval requires reviewed_at")
    try:
        parsed = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("DOI reconciliation approval reviewed_at must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError("DOI reconciliation approval reviewed_at must include a timezone")
    return {
        "schema_version": APPROVAL_SCHEMA_VERSION,
        "decision": "approved",
        "proposal_sha256": str(approval["proposal_sha256"]),
        "source_sha256": str(approval["source_sha256"]),
        "actions_sha256": str(approval["actions_sha256"]),
        "reviewed_by": reviewer.strip(),
        "reviewed_at": reviewed_at,
    }


def apply_actions(actions: list[dict[str, str]]) -> None:
    """Apply only reviewed canonical DOI role updates, atomically per file."""
    rendered: list[tuple[Path, dict[str, Any]]] = []
    for action in actions:
        path = REPO_ROOT / action["metadata_path"]
        data = json.loads(path.read_text(encoding="utf-8"))
        if extract_doi(data.get("doi")).casefold() != action["prior_canonical_doi"].casefold():
            raise ValueError(f"{action['folder']}: metadata DOI changed after review")
        data["doi"] = action["canonical_doi"]
        data["doi_url"] = resolver(action["canonical_doi"])
        prior = action["artifact_doi"]
        if prior:
            data["artifact_doi"] = prior
            data["artifact_doi_url"] = resolver(prior)
        rendered.append((path, data))
    for path, data in rendered:
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temporary, path)


def default_report_path() -> Path:
    date = datetime.now(timezone.utc).date().isoformat()
    return REPO_ROOT / "reports" / f"doi_role_reconciliation_{date}.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Where to write a proposed or applied report")
    parser.add_argument("--apply", action="store_true", help="Apply only the unchanged, reviewed proposal")
    parser.add_argument(
        "--approved-report",
        type=Path,
        help="Unchanged proposed report that a separate approval record binds; required with --apply",
    )
    parser.add_argument(
        "--approval",
        type=Path,
        help="Separately authored approval JSON bound to --approved-report; required with --apply",
    )
    args = parser.parse_args()
    if args.apply and not args.approved_report:
        parser.error("--apply requires --approved-report")
    if args.apply and not args.approval:
        parser.error("--apply requires --approval")
    if args.apply and not args.report:
        parser.error("--apply requires --report for the applied receipt")

    try:
        paths = metadata_paths()
        actions = proposed_actions(canonical_dois(), paths)
        proposal = render_report(actions, source_digest(paths), status="proposed")
        if args.apply:
            approved = args.approved_report
            if not approved.is_absolute():
                approved = REPO_ROOT / approved
            approved_proposal = validate_approval(approved, proposal)
            approval_path = args.approval
            if not approval_path.is_absolute():
                approval_path = REPO_ROOT / approval_path
            approval = validate_review_approval(approval_path, approved, approved_proposal)
            apply_actions(actions)
            receipt = render_report(actions, proposal["source_sha256"], status="applied", approval=approval)
            receipt["review_note"] = "Applied only after the exact proposed source/action record was supplied. Re-run the DOI audit to verify closure."
            report = args.report
            if not report.is_absolute():
                report = REPO_ROOT / report
            write_json_atomic(report, receipt)
            print(f"applied {len(actions)} DOI-role corrections; wrote {report.relative_to(REPO_ROOT)}")
            return
        if args.report:
            report = args.report
            if not report.is_absolute():
                report = REPO_ROOT / report
            write_json_atomic(report, proposal)
            print(f"wrote proposed DOI-role reconciliation {report.relative_to(REPO_ROOT)} ({len(actions)} actions)")
        else:
            print(json.dumps(proposal, indent=2, ensure_ascii=False))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"DOI reconciliation failed: {exc}") from exc


if __name__ == "__main__":
    main()
