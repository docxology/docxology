"""Work-page URLs are a permanent public contract.

`works/{citation_key}.html` is the canonical, indexed, externally-cited URL for each
work (it is also the BibTeX key in bibliography.bib). Permanent production reservations
live in data/work-identifiers.json, independently of editable titles and years.

This historical fixture independently catches accidental rewriting of established keys.
New works require an explicit registry allocation; removed works retain retired
reservations. Do not regenerate this fixture to authorize metadata-induced URL churn.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FROZEN = REPO_ROOT / "code" / "tests" / "fixtures" / "frozen-work-keys.json"
WORKS = REPO_ROOT / "data" / "works.json"


def _current_keys_by_num() -> dict[str, str]:
    data = json.loads(WORKS.read_text(encoding="utf-8"))
    works = data.get("works") or data.get("items") or []
    return {str(w["num"]): w["citation_key"] for w in works}


def test_existing_work_urls_are_stable():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    current = _current_keys_by_num()
    drift = {
        num: f"{key} -> {current[num]}"
        for num, key in frozen.items()
        if num in current and current[num] != key
    }
    assert not drift, (
        f"Existing work URLs changed despite permanent identity reservations: {drift}"
    )


def test_work_citation_keys_are_unique():
    current = _current_keys_by_num()
    keys = list(current.values())
    dupes = {k for k in keys if keys.count(k) > 1}
    assert not dupes, f"Duplicate citation_key(s) would overwrite a work page: {dupes}"
