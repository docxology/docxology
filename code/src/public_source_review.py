"""Review-gated rendering for dated public-source evidence reports.

The refresh scripts intentionally collect observations without editing curated
surfaces.  This module makes that boundary explicit: it turns the current
snapshot, pairing output, classification queue, DOI-role receipt, and claims
ledger into a stable human-and-machine review queue.  It never writes a
bibliography row, claim, Scholar snapshot, or repository classification.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
VALID_STATUSES = ("applied", "deferred", "rejected")
STATUS_ORDER = {status: index for index, status in enumerate(VALID_STATUSES)}
REQUIRED_CATEGORIES = (
    "zenodo_candidate",
    "ambiguous_doi_change",
    "repository_classification",
    "scholar_metric_change",
    "biographical_claim_change",
)
BIOGRAPHICAL_CLAIM_STATUSES = {
    "public-grant-record",
    "public-identifier",
    "public-institutional-record",
    "public-profile",
    "public-site",
    "curated-profile",
    "curated-program-copy",
}
SCHOLAR_METRIC_FIELDS = ("citations", "h_index", "i10_index")


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing review input: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON review input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"review input must be a JSON object: {path}")
    return value


def _provenance(path: Path | None, repo_root: Path) -> dict[str, Any] | None:
    if path is None:
        return None
    content = path.read_bytes()
    payload = _load_object(path)
    return {
        "path": _display_path(path, repo_root),
        "sha256": hashlib.sha256(content).hexdigest(),
        "generated_at": payload.get("generated_at"),
        "source_commit": payload.get("source_commit"),
    }


def _item(
    identifier: str,
    category: str,
    status: str,
    reason: str,
    *,
    sources: list[str],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid review status {status!r} for {identifier}")
    return {
        "id": identifier,
        "category": category,
        "status": status,
        "reason": reason,
        "sources": sorted(dict.fromkeys(source for source in sources if source)),
        "candidate": candidate,
    }


def _pair_key(doi: object, release_url: object) -> tuple[str, str]:
    return str(doi or "").strip().casefold(), str(release_url or "").strip()


def _decision_status(value: object) -> str:
    decision = str(value or "").strip().casefold()
    if decision in {"reject", "rejected"}:
        return "rejected"
    if decision in {"accept", "accepted", "acknowledged", "applied", "supersede", "superseded"}:
        return "applied"
    return "deferred"


def _pair_decisions(payload: dict[str, Any]) -> dict[tuple[str, str], str]:
    """Map an exact DOI/release candidate to its durable review outcome."""
    indexed: dict[tuple[str, str], str] = {}
    for group in payload.get("groups", []):
        if not isinstance(group, dict):
            continue
        group_doi = group.get("doi")
        status = _decision_status(group.get("decision"))
        for raw in group.get("raw_candidates", []):
            if isinstance(raw, dict):
                key = _pair_key(raw.get("doi") or group_doi, raw.get("github_release_url"))
            elif isinstance(raw, str):
                key = _pair_key(group_doi, raw)
            else:
                continue
            if key[0] and key[1]:
                indexed[key] = status
    return indexed


def _report_date(payload: dict[str, Any] | None) -> str:
    """Return a report's UTC date when it declares one, otherwise an empty string."""
    if not isinstance(payload, dict):
        return ""
    value = str(payload.get("date") or payload.get("generated_at") or "")
    return value[:10] if len(value) >= 10 else ""


def _report_timestamp(payload: dict[str, Any] | None) -> datetime | None:
    """Parse a report's zoned generation timestamp without guessing a time."""
    if not isinstance(payload, dict):
        return None
    value = payload.get("generated_at")
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def paired_publication_items(
    report: dict[str, Any] | None,
    decisions: dict[str, Any] | None,
    *,
    report_source: str,
    decision_source: str | None,
    snapshot_generated_at: datetime | None,
    refresh_status: str = "auto",
    refresh_note: str = "",
) -> list[dict[str, Any]]:
    """Return every paired-publication observation as an explicit review item."""
    if report is None:
        return [
            _item(
                "zenodo-report-unavailable",
                "zenodo_candidate",
                "deferred",
                "No GitHub–Zenodo pairing report was supplied; refresh and review candidates before changing curated publication data.",
                sources=[],
                candidate={"action_type": "unavailable"},
            )
        ]

    pairing_date = _report_date(report)
    pairing_generated_at = _report_timestamp(report)
    warnings = report.get("warnings", [])
    failed_or_stale = (
        refresh_status == "failed"
        or bool(warnings)
        or pairing_generated_at is None
        or bool(snapshot_generated_at and pairing_generated_at < snapshot_generated_at)
    )
    if failed_or_stale:
        if refresh_status == "failed":
            state = "failed"
            reason = "The current GitHub–Zenodo refresh was explicitly recorded as failed; retain the prior pairing report only as historical evidence."
        elif warnings:
            state = "failed"
            reason = "The supplied GitHub–Zenodo pairing report contains API warnings and cannot certify a current candidate set."
        else:
            state = "stale"
            reason = "The latest successful GitHub–Zenodo pairing report predates the public-source snapshot and cannot be treated as current release evidence."
        return [
            _item(
                "zenodo-refresh-incomplete",
                "zenodo_candidate",
                "deferred",
                reason,
                sources=[report_source],
                candidate={
                    "refresh_state": state,
                    "pairing_report_date": pairing_date,
                    "pairing_report_generated_at": pairing_generated_at.isoformat().replace("+00:00", "Z") if pairing_generated_at else "",
                    "public_source_snapshot_generated_at": snapshot_generated_at.isoformat().replace("+00:00", "Z") if snapshot_generated_at else "",
                    "warnings": [str(warning) for warning in warnings] if isinstance(warnings, list) else [],
                    "refresh_note": refresh_note,
                },
            )
        ]

    reviewed = _pair_decisions(decisions or {})
    items: list[dict[str, Any]] = []
    actions = report.get("actions", [])
    if not isinstance(actions, list):
        actions = []
    for ordinal, action in enumerate(actions, start=1):
        if not isinstance(action, dict):
            continue
        action_type = str(action.get("action_type") or "unknown")
        doi = str(action.get("doi") or "")
        release_url = str(action.get("github_release_url") or "")
        identifier = f"paired-publication:{doi or ordinal}:{release_url or ordinal}"
        if action_type == "already_reviewed":
            status = reviewed.get(_pair_key(doi, release_url), "deferred")
            category = "zenodo_candidate"
            reason = (
                "A durable pairing decision was found; retain its recorded outcome and do not create a duplicate curated row."
                if status != "deferred"
                else "The pairing report says this candidate was reviewed, but no exact durable decision was found; re-review it."
            )
        elif action_type == "needs_review":
            status = "deferred"
            category = "ambiguous_doi_change"
            reason = "The GitHub–Zenodo relation lacks sufficient DOI/release evidence for an automatic curated change."
        else:
            status = "deferred"
            category = "zenodo_candidate"
            reason = "Public release/Zenodo evidence is a candidate only; explicit review is required before changing curated source data."
        candidate = {
            "action_type": action_type,
            "doi": doi,
            "title": str(action.get("title") or ""),
            "confidence": str(action.get("confidence") or ""),
            "folder": str(action.get("folder") or ""),
            "github_repo": str(action.get("github_repo") or ""),
            "github_release_url": release_url,
            "zenodo_record_url": str(action.get("zenodo_record_url") or ""),
            "pairing_reason": str(action.get("reason") or ""),
        }
        items.append(
            _item(
                identifier,
                category,
                status,
                reason,
                sources=[report_source, decision_source or ""],
                candidate=candidate,
            )
        )
    if not items:
        items.append(
            _item(
                "zenodo-report-empty",
                "zenodo_candidate",
                "applied",
                "The supplied pairing report contains no candidate actions; no curated publication change is pending from that report.",
                sources=[report_source],
                candidate={"action_count": 0},
            )
        )
    return items


def _doi_actions_sha256(actions: list[dict[str, Any]]) -> str:
    return hashlib.sha256(_canonical_json(actions).encode("utf-8")).hexdigest()


def _verified_doi_approval(
    report: dict[str, Any], *, repo_root: Path | None
) -> bool:
    """Bind an applied DOI receipt to its exact separate approved proposal."""
    approval = report.get("approval")
    actions = report.get("actions")
    if not isinstance(approval, dict) or not isinstance(actions, list) or not all(isinstance(item, dict) for item in actions):
        return False
    required = ("proposal_sha256", "source_sha256", "actions_sha256", "reviewed_by", "reviewed_at")
    if any(not isinstance(approval.get(field), str) or not approval[field].strip() for field in required):
        return False
    if approval.get("decision") != "approved":
        return False
    try:
        reviewed_at = datetime.fromisoformat(str(approval["reviewed_at"]).replace("Z", "+00:00"))
    except ValueError:
        return False
    if reviewed_at.tzinfo is None:
        return False
    if approval.get("source_sha256") != report.get("source_sha256"):
        return False
    if approval.get("actions_sha256") != _doi_actions_sha256(actions):
        return False
    proposal_sha = str(approval.get("proposal_sha256"))
    if not re_full_sha256(proposal_sha) or repo_root is None:
        return False
    for proposal_path in sorted((repo_root / "reports").glob("doi_role_reconciliation_*.proposed.json")):
        try:
            content = proposal_path.read_bytes()
            proposal = json.loads(content)
        except (OSError, json.JSONDecodeError):
            continue
        if hashlib.sha256(content).hexdigest() != proposal_sha or not isinstance(proposal, dict):
            continue
        if proposal.get("status") != "proposed":
            continue
        if proposal.get("source_sha256") != report.get("source_sha256"):
            continue
        if proposal.get("actions") != actions or _doi_actions_sha256(proposal["actions"]) != approval.get("actions_sha256"):
            continue
        return True
    return False


def re_full_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def doi_review_items(
    report: dict[str, Any] | None, *, source: str | None, repo_root: Path | None = None
) -> list[dict[str, Any]]:
    """Expose DOI-role proposals and conflicts without applying metadata edits."""
    if report is None:
        return [
            _item(
                "doi-role-audit-unavailable",
                "ambiguous_doi_change",
                "deferred",
                "No DOI-role reconciliation or audit receipt was supplied; canonical/artifact DOI drift must be reviewed before document drift becomes a release blocker.",
                sources=[],
                candidate={"state": "unavailable"},
            )
        ]
    raw_status = str(report.get("status") or "proposed").casefold()
    approved = _verified_doi_approval(report, repo_root=repo_root)
    receipt_status = _decision_status(raw_status)
    if raw_status not in {"applied", "rejected"} or (raw_status == "applied" and not approved):
        receipt_status = "deferred"
    items: list[dict[str, Any]] = []
    actions = report.get("actions", [])
    if isinstance(actions, list):
        for ordinal, action in enumerate(actions, start=1):
            if not isinstance(action, dict):
                continue
            folder = str(action.get("folder") or ordinal)
            items.append(
                _item(
                    f"doi-role:{folder}",
                    "ambiguous_doi_change",
                    receipt_status,
                    (
                        "The exact DOI-role proposal was applied after a separately recorded review approval."
                        if receipt_status == "applied"
                        else "Canonical/artifact DOI roles require an explicit reviewed reconciliation before metadata is changed."
                    ),
                    sources=[source or ""],
                    candidate={
                        "folder": str(action.get("folder") or ""),
                        "prior_canonical_doi": str(action.get("prior_canonical_doi") or ""),
                        "canonical_doi": str(action.get("canonical_doi") or ""),
                        "artifact_doi": str(action.get("artifact_doi") or ""),
                        "action": str(action.get("action") or ""),
                    },
                )
            )
    conflicts = report.get("conflicts", [])
    if isinstance(conflicts, list):
        for ordinal, conflict in enumerate(conflicts, start=1):
            if not isinstance(conflict, dict):
                continue
            folder = str(conflict.get("folder") or ordinal)
            items.append(
                _item(
                    f"doi-conflict:{folder}:{conflict.get('code', ordinal)}",
                    "ambiguous_doi_change",
                    "deferred",
                    "The DOI audit found a conflict that cannot be converted into a metadata change without review.",
                    sources=[source or ""],
                    candidate={key: conflict.get(key) for key in sorted(conflict)},
                )
            )
    if not items:
        items.append(
            _item(
                "doi-role-audit-clean",
                "ambiguous_doi_change",
                "applied",
                "The supplied DOI-role report has no actions or conflicts; no DOI-role change is pending.",
                sources=[source or ""],
                candidate={"state": raw_status},
            )
        )
    return items


def repository_classification_items(
    payload: dict[str, Any] | None, *, source: str | None
) -> list[dict[str, Any]]:
    """Represent every repository-classification state without changing catalog data."""
    if payload is None:
        return [
            _item(
                "repository-classification-unavailable",
                "repository_classification",
                "deferred",
                "No repository classification queue was supplied; do not promote or exclude repositories automatically.",
                sources=[],
                candidate={"state": "unavailable"},
            )
        ]
    items: list[dict[str, Any]] = []
    rows = payload.get("repositories", [])
    if not isinstance(rows, list):
        rows = []
    for ordinal, row in enumerate(sorted((row for row in rows if isinstance(row, dict)), key=lambda row: str(row.get("full_name") or "")), start=1):
        review_status = str(row.get("review_status") or "defer").casefold()
        status = _decision_status(review_status)
        name = str(row.get("full_name") or ordinal)
        if review_status in {"defer", "pending", "unknown"}:
            reason = "The repository remains outside the curated catalog pending a human classification decision."
        elif status == "rejected":
            reason = "A recorded rejection keeps this repository out of the curated catalog."
        else:
            reason = "A recorded classification or acknowledged exclusion is retained; this report does not alter catalog membership."
        candidate = {
            "full_name": str(row.get("full_name") or ""),
            "html_url": str(row.get("html_url") or ""),
            "fork": bool(row.get("fork")),
            "archived": bool(row.get("archived")),
            "catalog_role": str(row.get("catalog_role") or ""),
            "review_status": review_status,
            "exclusion_reason": str(row.get("exclusion_reason") or ""),
            "acknowledged_reason": str(row.get("acknowledged_reason") or ""),
        }
        items.append(
            _item(
                f"repository:{name}",
                "repository_classification",
                status,
                reason,
                sources=[source or ""],
                candidate=candidate,
            )
        )
    if not items:
        items.append(
            _item(
                "repository-classification-empty",
                "repository_classification",
                "applied",
                "The supplied repository-classification queue contains no rows requiring a catalog decision.",
                sources=[source or ""],
                candidate={"row_count": 0},
            )
        )
    return items


def _direct_authenticated_scholar_metrics(
    receipt: dict[str, Any] | None, scholar_snapshot: dict[str, Any]
) -> tuple[dict[str, int] | None, str]:
    """Validate the deliberately narrow receipt contract for Scholar changes."""
    if receipt is None:
        return None, "No direct authenticated Scholar verification receipt was supplied."
    profile_id = str(receipt.get("profile_id") or "")
    if profile_id != str(scholar_snapshot.get("profile_id") or ""):
        return None, "Scholar verification receipt profile_id does not match the canonical snapshot."
    if receipt.get("direct") is not True or receipt.get("authenticated") is not True:
        return None, "Scholar verification receipt must explicitly state direct=true and authenticated=true."
    if not str(receipt.get("verified_at") or "").strip():
        return None, "Scholar verification receipt is missing verified_at."
    metrics = receipt.get("metrics")
    if not isinstance(metrics, dict):
        return None, "Scholar verification receipt is missing a metrics object."
    normalized: dict[str, int] = {}
    for field in SCHOLAR_METRIC_FIELDS:
        value = metrics.get(field)
        if not isinstance(value, int) or value < 0:
            return None, f"Scholar verification receipt field {field!r} must be a non-negative integer."
        normalized[field] = value
    return normalized, ""


def scholar_metric_item(
    scholar_snapshot: dict[str, Any],
    receipt: dict[str, Any] | None,
    *,
    snapshot_source: str,
    receipt_source: str | None,
) -> dict[str, Any]:
    observed, error = _direct_authenticated_scholar_metrics(receipt, scholar_snapshot)
    current = {field: scholar_snapshot.get(field) for field in SCHOLAR_METRIC_FIELDS}
    receipt_valid = observed is not None
    if observed is None:
        status = "deferred"
        reason = f"{error} Preserve the dated Scholar snapshot; do not infer a metric update from anonymous or cached views."
    elif observed == current:
        status = "applied"
        reason = "The direct authenticated Scholar receipt matches the dated snapshot, so no metric change is required."
    else:
        status = "deferred"
        reason = "A direct authenticated Scholar receipt found a metric difference, but explicit review is still required before changing the curated snapshot."
    return _item(
        "scholar-metrics",
        "scholar_metric_change",
        status,
        reason,
        sources=[snapshot_source, receipt_source or ""],
        candidate={
            "profile_id": str(scholar_snapshot.get("profile_id") or ""),
            "current": current,
            "observed": observed,
            "receipt_valid": receipt_valid,
            "receipt_verified_at": str((receipt or {}).get("verified_at") or ""),
        },
    )


def _checked_urls(snapshot: dict[str, Any] | None, inventory: dict[str, Any] | None) -> set[str]:
    urls: set[str] = set()
    for payload, key in ((snapshot, "checks"), (inventory, "sections")):
        if not isinstance(payload, dict):
            continue
        rows = payload.get(key, [])
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("ok") is True and isinstance(row.get("url"), str):
                urls.add(row["url"])
    return urls


def biographical_claim_items(
    claims_payload: dict[str, Any],
    *,
    claims_source: str,
    snapshot: dict[str, Any] | None,
    inventory: dict[str, Any] | None,
    snapshot_source: str | None,
    inventory_source: str | None,
) -> list[dict[str, Any]]:
    """Queue every time-sensitive biographical claim for deliberate content review.

    Public refreshes establish endpoint availability and discovery evidence; they
    do not establish that a narrative claim should be rewritten.  Listing each
    claim makes that conservative boundary auditable rather than implicit.
    """
    checked_urls = _checked_urls(snapshot, inventory)
    claims = claims_payload.get("claims", [])
    if not isinstance(claims, list):
        claims = []
    items: list[dict[str, Any]] = []
    for claim in sorted((claim for claim in claims if isinstance(claim, dict)), key=lambda claim: str(claim.get("id") or "")):
        identifier = str(claim.get("id") or "")
        if not identifier or "scholar" in identifier.casefold():
            continue
        claim_status = str(claim.get("status") or "")
        if claim_status not in BIOGRAPHICAL_CLAIM_STATUSES:
            continue
        sources = [str(value) for value in claim.get("sources", []) if isinstance(value, str)]
        checked = sorted(source for source in sources if source in checked_urls)
        if checked:
            reason = "A refreshed public endpoint is relevant to this biographical claim, but its content still requires explicit human comparison before any curated edit."
        else:
            reason = "No direct claim-change receipt was supplied; preserve this biographical claim until a human records an applied, deferred, or rejected review decision."
        items.append(
            _item(
                f"biographical-claim:{identifier}",
                "biographical_claim_change",
                "deferred",
                reason,
                sources=[claims_source, snapshot_source or "", inventory_source or "", *checked],
                candidate={
                    "claim_id": identifier,
                    "claim": str(claim.get("claim") or ""),
                    "claim_status": claim_status,
                    "checked_at": str(claim.get("checked_at") or ""),
                    "refreshed_sources": checked,
                },
            )
        )
    if not items:
        items.append(
            _item(
                "biographical-claims-none",
                "biographical_claim_change",
                "applied",
                "No biographical claims were present in the supplied claim ledger.",
                sources=[claims_source],
                candidate={"claim_count": 0},
            )
        )
    return items


def public_source_observation_items(
    snapshot: dict[str, Any] | None,
    previous_snapshot: dict[str, Any] | None,
    *,
    snapshot_source: str | None,
    previous_source: str | None,
) -> list[dict[str, Any]]:
    """Surface changes between two snapshots without treating them as claims."""
    if not isinstance(snapshot, dict) or not isinstance(previous_snapshot, dict):
        return []
    current_facts = snapshot.get("facts", {})
    prior_facts = previous_snapshot.get("facts", {})
    if not isinstance(current_facts, dict) or not isinstance(prior_facts, dict):
        return []
    items: list[dict[str, Any]] = []
    for label in sorted(set(current_facts) | set(prior_facts)):
        prior = prior_facts.get(label)
        current = current_facts.get(label)
        if _canonical_json(prior) == _canonical_json(current):
            continue
        items.append(
            _item(
                f"public-source-observation:{label}",
                "public_source_observation",
                "deferred",
                "A public-source observation changed since the prior snapshot. Review its meaning before changing any curated claim or derivative.",
                sources=[snapshot_source or "", previous_source or ""],
                candidate={"label": label, "previous": prior, "current": current},
            )
        )
    return items


def _category_summary(items: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for item in items:
        summary[item["category"]][item["status"]] += 1
    result: dict[str, dict[str, int]] = {}
    for category in sorted(set(REQUIRED_CATEGORIES) | set(summary)):
        counts = summary[category]
        result[category] = {status: counts[status] for status in VALID_STATUSES}
    return result


def build_review_report(
    *,
    repo_root: Path,
    report_date: str,
    source_commit: str,
    snapshot_path: Path,
    inventory_path: Path | None,
    paired_publications_path: Path | None,
    pair_decisions_path: Path | None,
    doi_review_path: Path | None,
    repository_classification_path: Path | None,
    claims_path: Path,
    scholar_snapshot_path: Path,
    scholar_receipt_path: Path | None = None,
    previous_snapshot_path: Path | None = None,
    pairing_refresh_status: str = "auto",
    pairing_refresh_note: str = "",
    source_provenance: dict[str, object] | None = None,
) -> dict[str, Any]:
    """Build a deterministic review report from immutable input snapshots."""
    snapshot = _load_object(snapshot_path)
    inventory = _load_object(inventory_path) if inventory_path else None
    paired = _load_object(paired_publications_path) if paired_publications_path else None
    decisions = _load_object(pair_decisions_path) if pair_decisions_path else None
    doi_review = _load_object(doi_review_path) if doi_review_path else None
    repository_classification = _load_object(repository_classification_path) if repository_classification_path else None
    claims = _load_object(claims_path)
    scholar_snapshot = _load_object(scholar_snapshot_path)
    scholar_receipt = _load_object(scholar_receipt_path) if scholar_receipt_path else None
    previous_snapshot = _load_object(previous_snapshot_path) if previous_snapshot_path else None

    paths = {
        "public_source_snapshot": snapshot_path,
        "public_source_inventory": inventory_path,
        "paired_publications": paired_publications_path,
        "paired_publication_decisions": pair_decisions_path,
        "doi_role_review": doi_review_path,
        "repository_classification": repository_classification_path,
        "claims_ledger": claims_path,
        "scholar_snapshot": scholar_snapshot_path,
        "scholar_verification_receipt": scholar_receipt_path,
        "previous_public_source_snapshot": previous_snapshot_path,
    }
    source_names = {name: _display_path(path, repo_root) if path else None for name, path in paths.items()}
    items = [
        *paired_publication_items(
            paired,
            decisions,
            report_source=source_names["paired_publications"] or "",
            decision_source=source_names["paired_publication_decisions"],
            snapshot_generated_at=_report_timestamp(snapshot),
            refresh_status=pairing_refresh_status,
            refresh_note=pairing_refresh_note,
        ),
        *doi_review_items(doi_review, source=source_names["doi_role_review"], repo_root=repo_root),
        *repository_classification_items(repository_classification, source=source_names["repository_classification"]),
        scholar_metric_item(
            scholar_snapshot,
            scholar_receipt,
            snapshot_source=source_names["scholar_snapshot"] or "",
            receipt_source=source_names["scholar_verification_receipt"],
        ),
        *biographical_claim_items(
            claims,
            claims_source=source_names["claims_ledger"] or "",
            snapshot=snapshot,
            inventory=inventory,
            snapshot_source=source_names["public_source_snapshot"],
            inventory_source=source_names["public_source_inventory"],
        ),
        *public_source_observation_items(
            snapshot,
            previous_snapshot,
            snapshot_source=source_names["public_source_snapshot"],
            previous_source=source_names["previous_public_source_snapshot"],
        ),
    ]
    items.sort(key=lambda item: (item["category"], STATUS_ORDER[item["status"]], item["id"]))
    status_counts = Counter(item["status"] for item in items)
    report = {
        "schema_version": SCHEMA_VERSION,
        "date": report_date,
        # The report is a deterministic dated review queue.  Its release-age
        # receipt therefore uses the declared UTC review date rather than a
        # wall-clock render time that would make --check perpetually stale.
        "generated_at": f"{report_date}T00:00:00Z",
        "source_commit": source_commit,
        **(source_provenance or {}),
        "refresh_context": {
            "pairing_refresh_status": pairing_refresh_status,
            "pairing_refresh_note": pairing_refresh_note,
        },
        "policy": (
            "Review-only evidence report. It never modifies curated bibliography rows, paper metadata, claims, Scholar metrics, "
            "repository classifications, or generated site data. Public observations become curated changes only through an explicit review."
        ),
        "inputs": {name: _provenance(path, repo_root) for name, path in paths.items()},
        "summary": {
            "items": len(items),
            "applied": status_counts["applied"],
            "deferred": status_counts["deferred"],
            "rejected": status_counts["rejected"],
            "review_required": status_counts["deferred"] > 0,
            "categories": _category_summary(items),
        },
        "items": items,
    }
    errors = validate_review_report(report)
    if errors:
        raise ValueError("invalid rendered public-source review report: " + "; ".join(errors))
    return report


def render_markdown(report: dict[str, Any]) -> str:
    """Render the JSON report into a concise deterministic human review surface."""
    summary = report["summary"]
    lines = [
        f"# Public-source review — {report['date']}",
        "",
        "> Review-only evidence. This report does not change curated bibliography data, claims, Scholar metrics, or repository classifications.",
        "",
        f"Source commit: `{report['source_commit']}`",
        "",
        "## Disposition summary",
        "",
        "| Status | Items |",
        "|---|---:|",
        f"| Applied | {summary['applied']} |",
        f"| Deferred | {summary['deferred']} |",
        f"| Rejected | {summary['rejected']} |",
        "",
        "| Category | Applied | Deferred | Rejected |",
        "|---|---:|---:|---:|",
    ]
    for category, counts in summary["categories"].items():
        lines.append(f"| `{category}` | {counts['applied']} | {counts['deferred']} | {counts['rejected']} |")

    inputs = report["inputs"]
    lines.extend(["", "## Evidence inputs", ""])
    for name in sorted(inputs):
        provenance = inputs[name]
        if provenance is None:
            lines.append(f"- `{name}`: not supplied")
        else:
            lines.append(f"- `{name}`: `{provenance['path']}` (`{provenance['sha256']}`)")

    for heading, statuses in (("Deferred review", {"deferred"}), ("Applied decisions", {"applied"}), ("Rejected decisions", {"rejected"})):
        selected = [item for item in report["items"] if item["status"] in statuses]
        lines.extend(["", f"## {heading}", ""])
        if not selected:
            lines.append("None.")
            continue
        for item in selected:
            lines.append(f"- **`{item['category']}` — {item['id']}**: {item['reason']}")
    lines.extend(
        [
            "",
            "## Required handling",
            "",
            "- Review every deferred item before changing its curated target.",
            "- A Scholar metric change remains deferred unless this report includes a valid direct authenticated verification receipt; a valid receipt still requires an explicit source update review.",
            "- Keep ambiguous DOI, Zenodo, repository-classification, and biographical decisions in their dedicated reviewed source records before regenerating derivatives.",
            "",
        ]
    )
    return "\n".join(lines)


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def validate_review_report(report: dict[str, Any]) -> list[str]:
    """Return structural errors rather than quietly accepting a false-green review."""
    errors: list[str] = []
    if report.get("schema_version") != SCHEMA_VERSION:
        errors.append("unexpected schema_version")
    if not isinstance(report.get("date"), str) or not report.get("date"):
        errors.append("missing date")
    elif report.get("generated_at") != f"{report['date']}T00:00:00Z":
        errors.append("generated_at must be the deterministic UTC review-date timestamp")
    if not isinstance(report.get("source_commit"), str) or not report.get("source_commit"):
        errors.append("missing source_commit")
    refresh_context = report.get("refresh_context")
    if not isinstance(refresh_context, dict):
        errors.append("missing refresh_context")
    elif refresh_context.get("pairing_refresh_status") not in {"auto", "failed"}:
        errors.append("invalid pairing_refresh_status")
    elif not isinstance(refresh_context.get("pairing_refresh_note"), str):
        errors.append("invalid pairing_refresh_note")
    items = report.get("items")
    if not isinstance(items, list):
        return [*errors, "items must be a list"]
    identifiers: set[str] = set()
    counts: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    scholar_items = []
    for item in items:
        if not isinstance(item, dict):
            errors.append("item must be an object")
            continue
        identifier = item.get("id")
        status = item.get("status")
        category = item.get("category")
        if not isinstance(identifier, str) or not identifier:
            errors.append("item missing id")
        elif identifier in identifiers:
            errors.append(f"duplicate item id: {identifier}")
        else:
            identifiers.add(identifier)
        if status not in VALID_STATUSES:
            errors.append(f"invalid item status: {identifier}")
        else:
            counts[status] += 1
        if not isinstance(category, str) or not category:
            errors.append(f"item missing category: {identifier}")
        else:
            categories[category] += 1
        if category == "scholar_metric_change":
            scholar_items.append(item)
    if len(scholar_items) != 1:
        errors.append("exactly one scholar_metric_change item is required")
    elif scholar_items[0].get("status") != "deferred":
        candidate = scholar_items[0].get("candidate")
        if not isinstance(candidate, dict) or candidate.get("receipt_valid") is not True:
            errors.append("Scholar metrics may be non-deferred only with a valid direct authenticated receipt")
    summary = report.get("summary")
    if not isinstance(summary, dict):
        return [*errors, "summary must be an object"]
    for status in VALID_STATUSES:
        if summary.get(status) != counts[status]:
            errors.append(f"summary count mismatch for {status}")
    category_summary = summary.get("categories")
    if not isinstance(category_summary, dict):
        errors.append("summary categories missing")
    else:
        for category in REQUIRED_CATEGORIES:
            if category not in category_summary:
                errors.append(f"required category absent: {category}")
        for category, status_counts in category_summary.items():
            if not isinstance(status_counts, dict):
                errors.append(f"invalid category summary: {category}")
                continue
            expected = Counter(item["status"] for item in items if isinstance(item, dict) and item.get("category") == category)
            for status in VALID_STATUSES:
                if status_counts.get(status) != expected[status]:
                    errors.append(f"category count mismatch for {category}/{status}")
    if summary.get("items") != len(items):
        errors.append("summary item count mismatch")
    if summary.get("review_required") != (counts["deferred"] > 0):
        errors.append("summary review_required mismatch")
    return errors
