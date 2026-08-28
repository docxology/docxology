#!/usr/bin/env python3
"""Create a bounded review queue for repositories outside the curated catalog."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IN = REPO_ROOT / "data" / "github-repositories.json"
OUT = REPO_ROOT / "data" / "repository-classification.json"
EXCLUSIONS = REPO_ROOT / "data" / "repository-exclusions.json"
EXCLUSIONS_SCHEMA_VERSION = "1.3"
FORK_EXCLUSION_REASON = "fork_not_curated"


def _is_iso_date(value: object) -> bool:
    """Return whether ``value`` is a complete ISO calendar date."""
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value


def _valid_github_id(value: object) -> bool:
    """Return whether ``value`` is a positive immutable GitHub REST id."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _valid_github_node_id(value: object) -> bool:
    """Return whether ``value`` is a non-empty immutable GitHub node id."""
    return isinstance(value, str) and bool(value.strip())


def validate_acknowledged_exclusions(payload: object) -> dict[str, dict]:
    """Validate the durable exclusion registry before it can clear review work.

    A fork must never become acknowledged merely because a loosely shaped JSON
    row happens to share its full name.  The registry is therefore an explicit
    schema boundary: all reasons must be declared, names must be unique, and
    Every exclusion needs a recorded reviewer, calendar date, and both GitHub
    immutable identities.  Primary and fork exclusions both remove a live
    repository from the review queue, so a provenance-free or path-only
    exclusion is just as capable of creating a false green as a malformed fork
    exclusion.
    """
    if not isinstance(payload, dict):
        raise ValueError("repository exclusions must be a JSON object")
    if payload.get("schema_version") != EXCLUSIONS_SCHEMA_VERSION:
        raise ValueError(
            "repository exclusions have an unexpected schema_version"
        )
    reasons = payload.get("reasons")
    if not isinstance(reasons, dict) or not reasons:
        raise ValueError("repository exclusions must declare a non-empty reasons map")
    if any(
        not isinstance(reason, str)
        or not reason.strip()
        or not isinstance(description, str)
        or not description.strip()
        for reason, description in reasons.items()
    ):
        raise ValueError("repository exclusions reasons map contains an invalid entry")
    exclusions = payload.get("exclusions")
    if not isinstance(exclusions, list):
        raise ValueError("repository exclusions must contain an exclusions list")

    acknowledged: dict[str, dict] = {}
    for ordinal, exclusion in enumerate(exclusions, start=1):
        if not isinstance(exclusion, dict):
            raise ValueError(
                f"repository exclusion {ordinal} must be an object"
            )
        full_name = exclusion.get("full_name")
        reason = exclusion.get("reason")
        note = exclusion.get("note")
        if (
            not isinstance(full_name, str)
            or not full_name.strip()
            or "/" not in full_name
        ):
            raise ValueError(
                f"repository exclusion {ordinal} has an invalid full_name"
            )
        if full_name in acknowledged:
            raise ValueError(f"duplicate repository exclusion: {full_name}")
        if not isinstance(reason, str) or reason not in reasons:
            raise ValueError(
                f"repository exclusion {full_name} has an undeclared reason"
            )
        if not isinstance(note, str) or not note.strip():
            raise ValueError(f"repository exclusion {full_name} is missing note")
        reviewed_by = exclusion.get("reviewed_by")
        reviewed_at = exclusion.get("reviewed_at")
        if not isinstance(reviewed_by, str) or not reviewed_by.strip():
            raise ValueError(
                f"repository exclusion {full_name} is missing reviewed_by"
            )
        if not _is_iso_date(reviewed_at):
            raise ValueError(
                f"repository exclusion {full_name} has an invalid reviewed_at date"
            )
        if not _valid_github_id(exclusion.get("github_id")):
            raise ValueError(
                f"repository exclusion {full_name} has an invalid github_id"
            )
        if not _valid_github_node_id(exclusion.get("github_node_id")):
            raise ValueError(
                f"repository exclusion {full_name} has an invalid github_node_id"
            )
        acknowledged[full_name] = exclusion
    return acknowledged


def load_acknowledged() -> dict[str, dict]:
    """Map full_name -> {reason, note} for deliberate, human-reviewed exclusions."""
    if not EXCLUSIONS.is_file():
        return {}
    try:
        payload = json.loads(EXCLUSIONS.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"could not read repository exclusions: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"repository exclusions are invalid JSON: {exc}") from exc
    return validate_acknowledged_exclusions(payload)


def acknowledged_exclusion(
    acknowledgement: dict | None,
    *,
    fork: bool,
    github_id: object,
    github_node_id: object,
) -> dict | None:
    """Return an acknowledgement only when its reason suits the repo kind.

    A structurally valid primary-repository reason is not evidence that a fork
    was reviewed, and a fork-specific decision cannot clear a primary repo.
    Nor can a full-name match clear a transferred or recreated repository: both
    immutable GitHub identities must match the reviewed exclusion exactly.
    Such mismatches remain deferred instead of inheriting an unrelated row.
    """
    if acknowledgement is None:
        return None
    if (
        acknowledgement.get("github_id") != github_id
        or acknowledgement.get("github_node_id") != github_node_id
    ):
        return None
    reason = acknowledgement.get("reason")
    if fork:
        return acknowledgement if reason == FORK_EXCLUSION_REASON else None
    return acknowledgement if reason != FORK_EXCLUSION_REASON else None


def build_payload() -> dict:
    source = json.loads(IN.read_text(encoding="utf-8"))
    acknowledged = load_acknowledged()
    rows = []
    for repo in source.get("repositories", []):
        if repo.get("curated"):
            continue
        fork = bool(repo.get("fork"))
        archived = bool(repo.get("archived"))
        description = str(repo.get("description") or "").strip()
        if not description:
            description_quality = "missing"
        elif len(description) < 40:
            description_quality = "short"
        else:
            description_quality = "substantive"
        full_name = repo.get("full_name")
        github_id = repo.get("github_id")
        github_node_id = repo.get("github_node_id")
        ack = acknowledged_exclusion(
            acknowledged.get(full_name),
            fork=fork,
            github_id=github_id,
            github_node_id=github_node_id,
        )
        if ack and fork:
            catalog_role, exclusion_reason, review_status = "acknowledged_not_curated", "fork_not_curated", "acknowledged"
        elif fork:
            catalog_role, exclusion_reason, review_status = "not_curated", "fork_not_curated", "defer"
        elif ack:
            catalog_role, exclusion_reason, review_status = "acknowledged_not_curated", "acknowledged_not_catalogued", "acknowledged"
        else:
            catalog_role, exclusion_reason, review_status = "not_curated", "primary_repo_requires_manual_review", "defer"
        row = {
            "full_name": full_name,
            "github_id": github_id,
            "github_node_id": github_node_id,
            "name": repo.get("name"),
            "owner": repo.get("owner"),
            "html_url": repo.get("html_url"),
            "fork": fork,
            "archived": archived,
            "private": bool(repo.get("private")),
            "description": description,
            "description_quality": description_quality,
            "language": repo.get("language") or "",
            "topics": repo.get("topics") or [],
            "recently_updated": bool(repo.get("recently_updated")),
            "relevance": "unknown",
            "catalog_role": catalog_role,
            "exclusion_reason": exclusion_reason,
            "review_status": review_status,
        }
        if ack:
            row["acknowledged_reason"] = ack.get("reason")
            if ack.get("reviewed_by"):
                row["reviewed_by"] = ack["reviewed_by"]
            if ack.get("reviewed_at"):
                row["reviewed_at"] = ack["reviewed_at"]
        rows.append(row)
    return {
        "schema_version": "1.4",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "data/github-repositories.json",
        "acknowledged_exclusions_source": "data/repository-exclusions.json",
        "policy": "Complete GitHub inventory remains distinct from the curated software catalog; unknown primary repositories stay reviewable and are never auto-promoted. Repositories listed in data/repository-exclusions.json are deliberate, human-reviewed not-catalog decisions (profile/website/test/mirror/duplicate or explicitly reviewed forks) and are marked acknowledged only when their full_name and immutable github_id/github_node_id match the reviewed repository.",
        "summary": {
            "total_inventory": len(source.get("repositories", [])),
            "uncatalogued": len(rows),
            "forks": sum(row["fork"] for row in rows),
            "acknowledged_forks": sum(row["fork"] and row["review_status"] == "acknowledged" for row in rows),
            "primary_requires_review": sum(row["exclusion_reason"] == "primary_repo_requires_manual_review" for row in rows),
            "acknowledged_excluded": sum(row["exclusion_reason"] == "acknowledged_not_catalogued" for row in rows),
            "archived": sum(row["archived"] for row in rows),
            "missing_description": sum(row["description_quality"] == "missing" for row in rows),
            "short_description": sum(row["description_quality"] == "short" for row in rows),
            "substantive_description": sum(row["description_quality"] == "substantive" for row in rows),
        },
        "repositories": rows,
    }


def preserve_timestamp_when_unchanged(payload: dict) -> dict:
    """Keep the queue timestamp stable unless the inventory-derived body changed."""
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
    parser.add_argument("--check", action="store_true", help="Fail if the classification queue is stale")
    args = parser.parse_args()
    payload = build_payload()
    payload = preserve_timestamp_when_unchanged(payload)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale repository classification: {OUT.relative_to(REPO_ROOT)}")
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
