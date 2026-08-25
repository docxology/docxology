"""Tests for the per-work reproducibility ledger.

The staleness gate is the load-bearing part: if ``--check`` cannot detect a
hand-edit, the published ledger silently stops reflecting the computation it
claims to report. ``test_check_detects_drift_in_every_output`` is a regression
test for exactly that failure — an earlier revision compared freshly generated
content against itself and therefore always passed.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

_SPEC = importlib.util.spec_from_file_location(
    "build_reproducibility_ledger",
    REPO_ROOT / "code" / "orchestrators" / "build_reproducibility_ledger.py",
)
ledger_mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(ledger_mod)


@pytest.fixture(scope="module")
def ledger() -> dict:
    return ledger_mod.build_ledger()


def test_every_catalogued_work_is_scored(ledger: dict) -> None:
    works = json.loads((REPO_ROOT / "data" / "works.json").read_text(encoding="utf-8"))["works"]
    assert ledger["work_count"] == len(works)
    assert {entry["num"] for entry in ledger["works"]} == {work["num"] for work in works}


def test_scores_are_bounded_and_match_their_signals(ledger: dict) -> None:
    for entry in ledger["works"]:
        assert 0 <= entry["score"] <= ledger_mod.MAX_SCORE
        assert entry["score"] == sum(1 for key in ledger_mod.SIGNAL_KEYS if entry["signals"][key])
        assert set(entry["signals"]) == set(ledger_mod.SIGNAL_KEYS)


def test_bands_follow_the_declared_thresholds(ledger: dict) -> None:
    for entry in ledger["works"]:
        expected = next(name for name, floor, _ in ledger_mod.BANDS if entry["score"] >= floor)
        assert entry["band"] == expected


def test_aggregates_agree_with_per_work_rows(ledger: dict) -> None:
    for key in ledger_mod.SIGNAL_KEYS:
        assert ledger["signal_totals"][key] == sum(1 for e in ledger["works"] if e["signals"][key])
    assert sum(ledger["band_counts"].values()) == ledger["work_count"]
    assert sum(ledger["score_histogram"].values()) == ledger["work_count"]


def test_executable_code_signal_implies_a_named_repository(ledger: dict) -> None:
    for entry in ledger["works"]:
        assert bool(entry["repositories"]) == entry["signals"]["executable_code"]


def test_weakest_section_is_published_worst_first(ledger: dict) -> None:
    rows = ledger_mod.weakest(ledger)
    assert rows, "the ledger must publish its weakest entries, not only its strongest"
    assert [r["score"] for r in rows] == sorted(r["score"] for r in rows)


def test_page_is_promoted_for_indexing() -> None:
    from sitemap_policy import INDEX_PRIORITY_STATIC  # noqa: PLC0415

    assert any(path == "reproducibility.html" for path, _, _ in INDEX_PRIORITY_STATIC)


def test_generated_outputs_on_disk_are_current() -> None:
    for path, content in ledger_mod.outputs().items():
        assert path.exists(), f"{path} has never been generated"
        on_disk, fresh = ledger_mod._comparable(path, content)
        assert on_disk == fresh, f"{path.name} is stale — rerun build_reproducibility_ledger.py"


@pytest.mark.parametrize("target", ["HTML_OUT", "MD_OUT", "JSON_OUT"])
def test_check_detects_drift_in_every_output(target: str, tmp_path: Path) -> None:
    """A hand-edit to any output must be visible to --check.

    Regression guard: comparing generated content against itself made this gate
    vacuously green, so a drifted page shipped without complaint.
    """
    path: Path = getattr(ledger_mod, target)
    content = ledger_mod.outputs()[path]
    original = path.read_text(encoding="utf-8")
    try:
        if target == "JSON_OUT":
            tampered = json.loads(original)
            tampered["work_count"] = tampered["work_count"] + 1
            path.write_text(json.dumps(tampered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            path.write_text(original + "\n<!-- drift -->\n", encoding="utf-8")
        on_disk, fresh = ledger_mod._comparable(path, content)
        assert on_disk != fresh, f"--check is blind to drift in {path.name}"
    finally:
        path.write_text(original, encoding="utf-8")


def test_timestamp_alone_does_not_count_as_drift() -> None:
    """Clock movement must not make the JSON perpetually 'stale'."""
    content = ledger_mod.outputs()[ledger_mod.JSON_OUT]
    bumped = json.loads(content)
    bumped["generated_at"] = "1999-12-31T23:59:59Z"
    on_disk, fresh = ledger_mod._comparable(
        ledger_mod.JSON_OUT, json.dumps(bumped, indent=2, ensure_ascii=False) + "\n"
    )
    assert on_disk == fresh


def test_write_render_preserves_timestamp_when_ledger_body_is_unchanged(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A repeat apply must not dirty Pages control manifests through a clock tick."""
    json_out = tmp_path / "reproducibility.json"
    existing = ledger_mod.build_ledger()
    existing["generated_at"] = "2026-08-25T00:00:00Z"
    json_out.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    monkeypatch.setattr(ledger_mod, "JSON_OUT", json_out)

    rendered = json.loads(ledger_mod.outputs()[json_out])

    assert rendered["generated_at"] == "2026-08-25T00:00:00Z"
