"""Tests for the search index builder (code/orchestrators/build_search_index.py)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH_DIR))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_search_index  # noqa: E402


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
