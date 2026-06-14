"""Work-page URLs are a permanent public contract.

`works/{citation_key}.html` is the canonical, indexed, externally-cited URL for each
work (it is also the BibTeX key in bibliography.bib). The citation_key is derived from
year + title-slug + num (export_bibliography.py), so an *edit to an existing work's title
or year would silently change its filename* — breaking the live URL, every inbound link,
the sitemap entry, and the JSON-LD @id, with no error on a static host that cannot 301.

This test freezes the citation_key of every existing work, keyed by its immutable `num`.
Adding a work (new num) or removing one (num disappears) is fine. But if a work that is
still in the catalogue changes its citation_key, this fails — catching the churn before it
ships. When you intentionally change an existing work's key, regenerate the fixture:

    python3 -c "import json; d=json.load(open('data/works.json')); \
        w=d.get('works') or d.get('items'); \
        open('code/tests/fixtures/frozen-work-keys.json','w').write( \
        json.dumps({str(x['num']): x['citation_key'] for x in w}, indent=2, \
        ensure_ascii=False, sort_keys=True)+chr(10))"
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
        "Existing work URLs changed (retitle/year edit churns a live works/*.html URL). "
        f"Regenerate the fixture only if this is intentional: {drift}"
    )


def test_work_citation_keys_are_unique():
    current = _current_keys_by_num()
    keys = list(current.values())
    dupes = {k for k in keys if keys.count(k) > 1}
    assert not dupes, f"Duplicate citation_key(s) would overwrite a work page: {dupes}"
