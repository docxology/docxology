"""Read-only helpers for generated site facts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_COUNTS_PATH = REPO_ROOT / "data" / "current-counts.json"


def load_facts(path: Path | None = None) -> dict:
    target = path or CURRENT_COUNTS_PATH
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def counts(path: Path | None = None) -> dict:
    return load_facts(path).get("counts", {})


def generated_date(path: Path | None = None) -> str:
    value = load_facts(path).get("generated_at", "")
    if isinstance(value, str) and len(value) >= 10:
        return value[:10]
    return datetime.now(timezone.utc).date().isoformat()


def generated_month_year(path: Path | None = None) -> str:
    try:
        return datetime.strptime(generated_date(path), "%Y-%m-%d").strftime("%B %Y")
    except ValueError:
        return generated_date(path)


def software_counts(path: Path | None = None) -> dict:
    return counts(path).get("software", {})


def github_counts(path: Path | None = None) -> dict:
    return counts(path).get("github_inventory", {})
