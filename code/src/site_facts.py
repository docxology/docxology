"""Read-only helpers for generated site facts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_COUNTS_PATH = REPO_ROOT / "data" / "current-counts.json"


class SiteFactsError(ValueError):
    """Raised when the revision-bearing count snapshot is not trustworthy."""


def load_facts(path: Path | None = None) -> dict:
    target = path or CURRENT_COUNTS_PATH
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SiteFactsError(f"missing required site-facts input: {target}") from exc
    except json.JSONDecodeError as exc:
        raise SiteFactsError(f"malformed site-facts input: {target}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SiteFactsError(f"site-facts input must be a JSON object: {target}")
    return payload


def counts(path: Path | None = None) -> dict:
    value = load_facts(path).get("counts")
    if not isinstance(value, dict):
        raise SiteFactsError("site-facts input must contain an object-valued 'counts'")
    return value


def generated_date(path: Path | None = None) -> str:
    value = load_facts(path).get("generated_at", "")
    if not isinstance(value, str) or not value.strip():
        raise SiteFactsError("site-facts input must contain a non-empty 'generated_at' revision timestamp")
    try:
        # ``fromisoformat`` accepts the repository's +00:00 timestamps; map
        # the conventional trailing Z as well so checked-in reports remain
        # portable between Python versions.
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SiteFactsError(f"malformed site-facts generated_at revision: {value!r}") from exc
    return parsed.date().isoformat()


def generated_month_year(path: Path | None = None) -> str:
    return datetime.strptime(generated_date(path), "%Y-%m-%d").strftime("%B %Y")


def software_counts(path: Path | None = None) -> dict:
    return counts(path).get("software", {})


def github_counts(path: Path | None = None) -> dict:
    return counts(path).get("github_inventory", {})
