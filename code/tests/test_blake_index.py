"""Keep topical search distinct from bibliography identity and source verification."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "orchestrators"))
import build_blake_index as index  # noqa: E402


@pytest.fixture
def corpus(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "reports").mkdir()
    works = []
    reviews = {}
    records = []
    for number, (folder, title, text, relation) in enumerate([
        ("2026_Vision", "William Blake study", "William Blake\n", "title"),
        ("2026_Case", "Case study", "Barry J. Blake\n", "other_person"),
        ("2026_Priors", "Prior art", "An account of priors\n", "no_match"),
    ], 1):
        path = tmp_path / "papers" / folder
        path.mkdir(parents=True)
        (path / "full_text.md").write_text(text)
        (path / "metadata.json").write_text(json.dumps({"record_id": str(number)}))
        works.append({"citation_key": f"Work{number}", "docs_path": f"papers/{folder}/", "title": title, "year": 2026, "doi": f"10.5281/zenodo.{number + 100}", "url": f"https://doi.org/10.5281/zenodo.{number + 100}"})
        reviews[folder] = {"relation": relation, "note": relation, "full_text_sha256": hashlib.sha256(text.encode()).hexdigest()}
        records.append({"record_id": str(number), "doi": f"10.5281/zenodo.{number + 100}", "title": title, "version": "v1"})
    (tmp_path / "data/works.json").write_text(json.dumps({"works": works}))
    (tmp_path / "data/blake-review.json").write_text(json.dumps({"metadata_source": "reports/discovery.json", "reviews": reviews}))
    (tmp_path / "reports/discovery.json").write_text(json.dumps({"generated_at": "2026-10-22T00:00:00Z", "warnings": [], "zenodo_records": records}))
    return tmp_path


def test_excludes_namesakes_and_reports_negative_search_without_claiming_citation_validation(corpus):
    payload = index.build_payload(corpus)
    assert [x["citation_key"] for x in payload["works"]] == ["Work1"]
    assert {x["relation"] for x in payload["exclusions"]} == {"other_person", "no_match"}
    row = payload["works"][0]
    assert row["citation_doi"] == "10.5281/zenodo.101"
    assert row["version_doi"] == "10.5281/zenodo.1"
    assert row["primary_metadata_matched"] is True
    assert row["citation_sources_independently_checked"] is False
    assert row["matching_lines"] == [1]


def test_changed_text_invalidates_passage_review(corpus):
    (corpus / "papers/2026_Vision/full_text.md").write_text("A changed William Blake passage\n")
    with pytest.raises(ValueError, match="Stale passage review"):
        index.build_payload(corpus)


def test_new_match_stays_pending_until_classified(corpus):
    path = corpus / "data/blake-review.json"
    data = json.loads(path.read_text())
    del data["reviews"]["2026_Case"]
    path.write_text(json.dumps(data))
    assert index.build_payload(corpus)["needs_review"] == ["Work2"]


def test_missing_reviewed_text_fails_instead_of_shrinking_coverage(corpus):
    (corpus / "papers/2026_Vision/full_text.md").unlink()
    with pytest.raises(ValueError, match="Reviewed text missing"):
        index.build_payload(corpus)


def test_primary_title_disagreement_rejects_metadata_match(corpus):
    path = corpus / "reports/discovery.json"
    data = json.loads(path.read_text())
    data["zenodo_records"][0]["title"] = "Different work"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="Primary title mismatch"):
        index.build_payload(corpus)


def test_substrings_are_not_blake_matches():
    assert index.WORD.search("Blakemore") is None
    assert index.WORD.search("Blake2b") is None
    assert index.WORD.search("William Blake’s")


def test_rendered_prose_uses_current_counts_and_source_line_links(corpus):
    path = corpus / "data/blake-review.json"
    data = json.loads(path.read_text())
    data["reviews"]["2026_Case"]["relation"] = "quotation"
    path.write_text(json.dumps(data))
    markdown = index.render_markdown(index.build_payload(corpus))
    assert "**1 core treatments** and **1 related or peripheral works**" in markdown
    assert "full_text.md?plain=1#L1" in markdown
    assert "nine core" not in markdown


def test_evidence_line_must_identify_an_actual_text_match(corpus):
    path = corpus / "data/blake-review.json"
    data = json.loads(path.read_text())
    data["reviews"]["2026_Vision"]["evidence_lines"] = [100]
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="evidence line lacks Blake match"):
        index.build_payload(corpus)
