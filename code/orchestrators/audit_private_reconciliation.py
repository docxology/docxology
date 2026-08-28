#!/usr/bin/env python3
"""Audit a private branch against public main without importing either history.

The default references intentionally match this release plan.  The only
permitted output is a review report; this command never merges, cherry-picks,
checks out, resets, or edits source files.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from private_reconciliation import (  # noqa: E402
    ChangedPath,
    bibliography_rows,
    changed_top_level_fields,
    classify_path,
    default_decision,
    manifest_output_patterns,
    parse_name_status_z,
    render_markdown,
    source_backed_metadata_fields,
)

DEFAULT_BASELINE = "b08dc428"
DEFAULT_PRIVATE_REF = "a73d89b"


def git(*args: str, text: bool = False) -> str | bytes:
    """Run a read-only Git query and surface its real failure."""
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        stderr = result.stderr.decode("utf-8", "replace").strip()
        raise ValueError(f"git {' '.join(args)} failed: {stderr}")
    if text:
        return result.stdout.decode("utf-8", "surrogateescape")
    return result.stdout


def resolve_ref(ref: str) -> str:
    return str(git("rev-parse", "--verify", f"{ref}^{{commit}}", text=True)).strip()


def git_text(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        return None
    return result.stdout.decode("utf-8", "surrogateescape")


def git_json(ref: str, path: str) -> Mapping[str, Any] | None:
    content = git_text(ref, path)
    if content is None:
        return None
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def changed_paths(baseline: str, private_ref: str) -> list[ChangedPath]:
    raw = git("diff", "--name-status", "-z", "--find-renames", baseline, private_ref)
    assert isinstance(raw, bytes)
    return parse_name_status_z(raw)


def baseline_manifest(baseline: str) -> tuple[str, ...]:
    payload = git_json(baseline, "data/generated-manifest.json")
    return manifest_output_patterns(payload or {})


def worktree_digest(paths: list[Path]) -> str:
    """Hash checked release-source fields without mutating the worktree."""
    digest = hashlib.sha256()
    for path in sorted(paths):
        relative = path.relative_to(REPO_ROOT).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        if path.is_file():
            content = path.read_bytes()
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
        else:
            digest.update((0).to_bytes(8, "big"))
    return digest.hexdigest()


def audit_payload(baseline_requested: str, private_requested: str, report_date: str) -> dict[str, Any]:
    """Build the complete deterministic audit payload from Git object content."""
    baseline = resolve_ref(baseline_requested)
    private_ref = resolve_ref(private_requested)
    manifest_patterns = baseline_manifest(baseline)
    changes = changed_paths(baseline, private_ref)
    classifications: Counter[str] = Counter()
    path_rows: list[dict[str, Any]] = []
    for change in changes:
        classification = classify_path(change.path, manifest_patterns)
        decision, rationale = default_decision(classification)
        classifications[classification] += 1
        row: dict[str, Any] = {
            "status": change.status,
            "path": change.path,
            "classification": classification,
            "decision": decision,
            "rationale": rationale,
        }
        if change.previous_path:
            row["previous_path"] = change.previous_path
        path_rows.append(row)

    public_bibliography_text = git_text(baseline, "pages/BIBLIOGRAPHY.md")
    private_bibliography_text = git_text(private_ref, "pages/BIBLIOGRAPHY.md")
    if public_bibliography_text is None or private_bibliography_text is None:
        raise ValueError("both references must contain pages/BIBLIOGRAPHY.md")
    public_bibliography = bibliography_rows(public_bibliography_text)
    private_bibliography = bibliography_rows(private_bibliography_text)

    findings: list[dict[str, str]] = []
    metadata_reviews: list[dict[str, Any]] = []
    deferred_metadata_fields = 0
    metadata_paths = [row["path"] for row in path_rows if row["classification"] == "source_metadata" and row["path"].startswith("papers/") and row["path"].endswith("/metadata.json")]
    for path in metadata_paths:
        folder = Path(path).parent.name
        public_metadata = git_json(baseline, path)
        private_metadata = git_json(private_ref, path)
        if public_metadata is None or private_metadata is None:
            metadata_reviews.append(
                {
                    "path": path,
                    "decision": "defer",
                    "reason": "metadata was added, deleted, or invalid JSON in one reference",
                }
            )
            continue
        changed_fields = changed_top_level_fields(public_metadata, private_metadata)
        candidates = source_backed_metadata_fields(folder, public_metadata, private_metadata, private_bibliography)
        candidate_fields = {item["field"] for item in candidates}
        for finding in candidates:
            finding["release_status"] = "deferred pending independent public authority"
            findings.append(finding)
        deferred_fields = changed_fields
        deferred_metadata_fields += len(deferred_fields)
        metadata_reviews.append(
            {
                "path": path,
                "changed_fields": changed_fields,
                "candidate_fields": sorted(candidate_fields),
                "deferred_fields": deferred_fields,
                "decision": "defer",
            }
        )

    # A private bibliography change is an internal candidate, not an external
    # authority. Record it for review without treating it as a public-source
    # correction or an instruction to rewrite the public bibliography.
    for folder in sorted(set(public_bibliography) & set(private_bibliography)):
        public_doi = public_bibliography[folder].get("doi", "")
        private_doi = private_bibliography[folder].get("doi", "")
        if public_doi == private_doi or not private_doi:
            continue
        existing = next((item for item in findings if item["folder"] == folder and item["field"] == "doi"), None)
        if existing:
            continue
        findings.append(
            {
                "folder": folder,
                "field": "bibliography_doi",
                "baseline_value": public_doi,
                "private_value": private_doi,
                "canonical_value": private_doi,
                "decision": "defer",
                "implementation": "Private bibliography change only; verify against the public DOI/venue authority before altering the canonical public citation source.",
                "release_status": "deferred pending independent public authority",
            }
        )

    classifications_payload: dict[str, dict[str, Any]] = {}
    for classification in ("source_metadata", "derived_output", "binary_intake", "other_source"):
        decision, _ = default_decision(classification)
        classifications_payload[classification] = {"count": classifications[classification], "decision": decision}
    worktree_paths = [REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"] + [
        REPO_ROOT / item["path"] for item in metadata_reviews if "path" in item
    ]
    return {
        "schema_version": "1.0",
        "report_date": report_date,
        "baseline": {"requested": baseline_requested, "resolved": baseline},
        "private_ref": {"requested": private_requested, "resolved": private_ref},
        "mode": "read_only_comparison",
        "prohibited_operations": ["merge", "cherry-pick", "checkout", "reset", "source-file write"],
        "worktree_source_sha256": worktree_digest(worktree_paths),
        "summary": {
            "changed_paths": len(path_rows),
            "classifications": classifications_payload,
            "metadata_files_reviewed": len(metadata_reviews),
            "deferred_metadata_fields": deferred_metadata_fields,
        },
        "changes": path_rows,
        "private_identity_candidates": sorted(findings, key=lambda item: (item["folder"], item["field"])),
        "metadata_reviews": metadata_reviews,
    }


def output_paths(report_date: str, json_output: Path | None, markdown_output: Path | None) -> tuple[Path, Path]:
    json_path = json_output or REPO_ROOT / "reports" / f"private_public_reconciliation_{report_date}.json"
    markdown_path = markdown_output or REPO_ROOT / "reports" / f"private_public_reconciliation_{report_date}.md"
    return json_path if json_path.is_absolute() else REPO_ROOT / json_path, markdown_path if markdown_path.is_absolute() else REPO_ROOT / markdown_path


def write_or_check(path: Path, content: str, check: bool) -> bool:
    """Write only requested report outputs, or identify a stale expected report."""
    if check:
        return path.is_file() and path.read_text(encoding="utf-8") == content
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def display_path(path: Path) -> str:
    """Render a report path whether it is inside or outside the repository."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=DEFAULT_BASELINE, help="Public baseline Git ref (default: %(default)s)")
    parser.add_argument("--private-ref", default=DEFAULT_PRIVATE_REF, help="Private comparison Git ref (default: %(default)s)")
    parser.add_argument("--report-date", default=date.today().isoformat(), help="Date embedded in deterministic report names/content")
    parser.add_argument("--json-output", type=Path, help="JSON report destination")
    parser.add_argument("--markdown-output", type=Path, help="Markdown report destination")
    parser.add_argument("--check", action="store_true", help="Fail if expected report outputs differ; never write")
    args = parser.parse_args()
    try:
        payload = audit_payload(args.baseline, args.private_ref, args.report_date)
        json_path, markdown_path = output_paths(args.report_date, args.json_output, args.markdown_output)
        json_content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        markdown_content = render_markdown(payload)
        stale = [
            display_path(path)
            for path, content in ((json_path, json_content), (markdown_path, markdown_content))
            if not write_or_check(path, content, args.check)
        ]
        if stale:
            raise SystemExit("stale private/public reconciliation report: " + ", ".join(stale))
        print(("checked" if args.check else "wrote") + f" private/public reconciliation report for {payload['summary']['changed_paths']} paths")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"private/public reconciliation audit failed: {exc}") from exc


if __name__ == "__main__":
    main()
