"""Tests for the search index builder (code/orchestrators/build_search_index.py)."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


import build_search_index  # noqa: E402
from docxology_tools.abstract_text import abstract_display_text  # noqa: E402


def test_real_work_abstract_is_readable_search_prose_without_mutating_source():
    root = Path(__file__).resolve().parents[2]
    source_paths = [root / "data/works.json", root / "data/work-enrichment.json"]
    source_bytes = {path: path.read_bytes() for path in source_paths}
    works = json.loads(source_bytes[source_paths[0]])["works"]
    enrichments = json.loads(source_bytes[source_paths[1]])["works"]
    key = "Friedman2026TowardsLean4Formalization113"
    work = next(item for item in works if item["citation_key"] == key)
    original_work, original_enrichment = copy.deepcopy(work), copy.deepcopy(enrichments[key])
    raw = enrichments[key]["abstract"]
    assert raw.startswith("<p><strong>FEP_Lean")

    item = build_search_index.work_item(work, enrichments)

    assert item["summary"].startswith("FEP_Lean v1.1.0 is a source-bound, machine-checked catalogue")
    assert "155 topics" in item["summary"]
    assert item["summary"] == abstract_display_text(raw)[:220]
    assert abstract_display_text(raw) in item["content"]
    for field in ("summary", "content"):
        assert not re.search(r"</?(?:p|strong|code|em|ul|li|br)\b", item[field], re.I)
    assert work == original_work
    assert enrichments[key] == original_enrichment
    assert all(path.read_bytes() == before for path, before in source_bytes.items())


@pytest.mark.parametrize("raw,expected", [
    (
        "A < B and C > D. Use type <T> &amp; literal &lt;code&gt; notation.",
        "A < B and C > D. Use type <T> & literal <code> notation.",
    ),
    (
        "<p><strong>Comparison</strong>: A &lt; B and type <T>.</p><p>Final qualification.</p>",
        "Comparison: A < B and type <T>.\n\nFinal qualification.",
    ),
])
def test_work_search_prose_preserves_literal_math_and_source(raw, expected):
    work = {
        "citation_key": "Example2026", "title": "Public math fixture", "type": "Paper",
        "venue": "Fixture", "domain_name": "Mathematics", "year": 2026,
    }
    enrichments = {work["citation_key"]: {"abstract": raw}}
    original = copy.deepcopy(enrichments)

    item = build_search_index.work_item(work, enrichments)

    assert item["summary"] == expected
    assert expected in item["content"]
    assert enrichments == original


@pytest.fixture
def isolated_outputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    """Redirect every index surface into tmp_path and make the clock countable."""

    paths = {
        "main": tmp_path / "search-index.json",
        "core": tmp_path / "search-index-core.json",
        "work": tmp_path / "search-index-content-work.json",
        "video": tmp_path / "search-index-content-video.json",
    }
    monkeypatch.setattr(build_search_index, "OUT", paths["main"])
    monkeypatch.setattr(build_search_index, "CORE_OUT", paths["core"])
    monkeypatch.setattr(
        build_search_index,
        "content_segment_path",
        lambda item_type: paths[str(item_type)],
    )

    stamps = iter(
        f"2026-09-07T00:00:{second:02d}Z" for second in range(60)
    )
    monkeypatch.setattr(
        build_search_index, "generated_timestamp", lambda: next(stamps)
    )
    return paths


def _read_generated_at(path: Path) -> str:
    return json.loads(path.read_text(encoding="utf-8"))["generated_at"]


def _write_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["build_search_index.py"])
    build_search_index.main()


def test_changed_content_stamps_all_surfaces_with_one_timestamp(
    isolated_outputs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
):
    """A content-changing run must not skew main vs split generated_at values.

    Regression: when the rendered body differed from the on-disk index,
    main() fell back to None and render()/render_split() each called the clock
    again, committing a tree whose companions carried different timestamps —
    validate_repo.py --check then failed until a second idempotent run.
    """

    # Pre-seed a different body so stable_generated_at returns None.
    isolated_outputs["main"].write_text(
        json.dumps({"generated_at": "2000-01-01T00:00:00Z", "count": 0, "items": []}),
        encoding="utf-8",
    )

    _write_run(monkeypatch)

    stamps = {name: _read_generated_at(path) for name, path in isolated_outputs.items()}
    assert len(set(stamps.values())) == 1, stamps


def test_unchanged_content_reuses_the_existing_timestamp(
    isolated_outputs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
):
    """An idempotent re-run must reuse the on-disk timestamp on every surface."""

    _write_run(monkeypatch)
    first = {name: _read_generated_at(path) for name, path in isolated_outputs.items()}

    _write_run(monkeypatch)
    second = {name: _read_generated_at(path) for name, path in isolated_outputs.items()}

    assert second == first
    assert len(set(first.values())) == 1


def test_progressive_split_preserves_every_full_text_field(monkeypatch):
    """Deferred work/video text and retained site text reconstruct the full index."""
    source = {
        "generated_at": "2026-10-02T00:00:00Z",
        "source_files": [],
        "count": 4,
        "items": [
            {"id": "work:1", "type": "work", "title": "Paper", "content": "work text"},
            {"id": "video:1", "type": "video", "title": "Talk", "content": "transcript"},
            {"id": "page:1", "type": "page", "title": "Page", "content": "body-only phrase"},
            {"id": "software:1", "type": "software", "title": "Code", "content": "repository details"},
        ],
    }
    monkeypatch.setattr(build_search_index, "render", lambda stamp=None: json.dumps(source))
    outputs = build_search_index.render_split(source["generated_at"])
    core = json.loads(outputs[build_search_index.CORE_OUT])["items"]
    assert "content" not in core[0]
    assert "content" not in core[1]
    assert core[2]["content"] == "body-only phrase"
    assert core[3]["content"] == "repository details"
    content_by_id = {
        item["id"]: item["content"]
        for item_type in ("work", "video")
        for item in json.loads(outputs[build_search_index.content_segment_path(item_type)])["items"]
    }
    restored = [dict(item, content=content_by_id[item["id"]]) if item["id"] in content_by_id else item for item in core]
    assert restored == source["items"]
