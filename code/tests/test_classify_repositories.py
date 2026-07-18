from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
import classify_repositories  # noqa: E402


def test_repository_classification_exposes_description_quality_and_review_contract():
    payload = classify_repositories.build_payload()
    rows = payload["repositories"]
    assert rows
    required = {
        "full_name", "name", "owner", "html_url", "fork", "archived", "private",
        "description", "description_quality", "catalog_role", "exclusion_reason", "review_status",
    }
    assert required <= set(rows[0])
    assert {row["review_status"] for row in rows} == {"defer"}
    assert payload["summary"]["uncatalogued"] == len(rows)
    assert payload["summary"]["missing_description"] + payload["summary"]["short_description"] + payload["summary"]["substantive_description"] == len(rows)


def test_repository_classification_projection_is_current():
    actual = json.loads((REPO_ROOT / "data" / "repository-classification.json").read_text(encoding="utf-8"))
    expected = classify_repositories.build_payload()
    expected["generated_at"] = actual["generated_at"]
    assert actual == expected
