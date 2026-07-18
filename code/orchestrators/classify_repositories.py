#!/usr/bin/env python3
"""Create a bounded review queue for repositories outside the curated catalog."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IN = REPO_ROOT / "data" / "github-repositories.json"
OUT = REPO_ROOT / "data" / "repository-classification.json"


def build_payload() -> dict:
    source = json.loads(IN.read_text(encoding="utf-8"))
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
        rows.append(
            {
                "full_name": repo.get("full_name"),
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
                "catalog_role": "not_curated",
                "exclusion_reason": "fork_not_curated" if fork else "primary_repo_requires_manual_review",
                "review_status": "defer",
            }
        )
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "data/github-repositories.json",
        "policy": "Complete GitHub inventory remains distinct from the curated software catalog; unknown primary repositories stay reviewable and are never auto-promoted.",
        "summary": {
            "total_inventory": len(source.get("repositories", [])),
            "uncatalogued": len(rows),
            "forks": sum(row["fork"] for row in rows),
            "primary_requires_review": sum(not row["fork"] for row in rows),
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
