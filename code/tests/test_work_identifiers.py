"""Public work identity survives corrections; intake cannot reuse reservations."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.biblio_table import BiblioRow, iter_bibliography_rows  # noqa: E402
from docxology_tools.work_identifiers import (  # noqa: E402
    SCHEMA_VERSION, WorkIdentifierError, key_for_num, load_registry,
    next_catalog_num, register_new_rows, validate_catalog, write_catalog_with_identifiers,
)
from docxology_tools.generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402
from docxology_tools import work_identifiers  # noqa: E402
from export_bibliography import citation_key, row_to_work  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]


def _row(num: int = 1, title: str = "Original title", year: str = "2026") -> BiblioRow:
    return BiblioRow(num, year, "🧠", "Paper", title, "Venue", "https://example.test", "")


def _registry_file(tmp_path: Path, reservations: dict | None = None) -> Path:
    path = tmp_path / "work-identifiers.json"
    payload = {"schema_version": SCHEMA_VERSION, "identifiers": reservations if reservations is not None else {
        "1": {"citation_key": "Friedman2026OriginalTitle001", "status": "active"},
        "2": {"citation_key": "Friedman2026RetiredTitle002", "status": "retired", "reason": "Duplicate"},
    }}
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    return path


def test_all_current_public_keys_and_retired_gaps_are_reserved():
    registry = load_registry()
    rows = list(iter_bibliography_rows())
    validate_catalog(rows, registry)
    works = json.loads((REPO_ROOT / "data/works.json").read_text(encoding="utf-8"))["works"]
    assert {work["num"]: work["citation_key"] for work in works} == {
        row.num: key_for_num(row.num, registry) for row in rows
    }
    retired = {int(num) for num, record in registry["identifiers"].items() if record["status"] == "retired"}
    assert {30, 49, 118, 193}.issubset(retired)


def test_title_year_and_external_identifier_corrections_preserve_every_public_key():
    registry = load_registry()
    for row in iter_bibliography_rows():
        corrected = row._replace(year="2023", title="Corrected complete publication title", link_cell="https://doi.org/10.1234/corrected")
        assert citation_key(corrected, registry=registry) == citation_key(row, registry=registry)
        work = row_to_work(corrected, registry=registry, visible_source_paths=frozenset())
        assert work.citation_key == key_for_num(row.num, registry)
        assert work.title == corrected.title
        assert work.year == 2023
        assert work.doi == "10.1234/corrected"


def test_registration_is_explicit_idempotent_and_ignores_later_metadata_edits(tmp_path):
    path = _registry_file(tmp_path)
    rows = [_row(), _row(3, "New Work Title")]
    with pytest.raises(WorkIdentifierError, match="no permanent identifier"):
        validate_catalog(rows, load_registry(path, repo_root=tmp_path))
    assert register_new_rows(rows, path, repo_root=tmp_path) == [3]
    registered = path.read_bytes()
    assert key_for_num(3, load_registry(path, repo_root=tmp_path)) == "Friedman2026NewWorkTitle003"
    assert register_new_rows([rows[0], rows[1]._replace(year="2024", title="Expanded title")], path, repo_root=tmp_path) == []
    assert path.read_bytes() == registered


def test_intake_allocates_after_a_retired_final_numeric_id(tmp_path):
    path = _registry_file(tmp_path)
    assert next_catalog_num([_row()], path, repo_root=tmp_path) == 3


@pytest.mark.parametrize("rows, message", [
    ([_row(), _row()], "duplicate numeric"),
    ([_row(2)], "retired work"),
    ([], "no bibliography row"),
    ([_row(), _row(3)], "no permanent identifier"),
])
def test_catalog_binding_fails_closed(tmp_path, rows, message):
    path = _registry_file(tmp_path)
    with pytest.raises(WorkIdentifierError, match=message):
        validate_catalog(rows, load_registry(path, repo_root=tmp_path))


def test_failed_registration_does_not_write_or_infer_retirement(tmp_path):
    path = _registry_file(tmp_path)
    before = path.read_bytes()
    with pytest.raises(WorkIdentifierError, match="no bibliography row"):
        register_new_rows([_row(3)], path, repo_root=tmp_path)
    assert path.read_bytes() == before


def test_missing_earlier_numeric_gap_cannot_be_reallocated(tmp_path):
    path = _registry_file(tmp_path, {"3": {"citation_key": "Reserved003", "status": "active"}})
    with pytest.raises(WorkIdentifierError, match="earlier catalog ID"):
        register_new_rows([_row(3), _row(2)], path, repo_root=tmp_path)


@pytest.mark.parametrize("record", [
    {"citation_key": "../outside", "status": "active"},
    {"citation_key": "ValidKey", "status": "unknown"},
    {"citation_key": "ValidKey", "status": []},
    {"citation_key": "ValidKey", "status": "retired"},
    {"citation_key": "ValidKey", "status": "retired", "reason": []},
])
def test_unsafe_or_incomplete_reservations_are_rejected(tmp_path, record):
    path = _registry_file(tmp_path, {"1": record})
    with pytest.raises(WorkIdentifierError):
        load_registry(path, repo_root=tmp_path)


def test_active_key_cannot_collide_with_retired_key_on_case_insensitive_hosts(tmp_path):
    path = _registry_file(tmp_path, {
        "1": {"citation_key": "PermanentKey", "status": "active"},
        "2": {"citation_key": "permanentkey", "status": "retired", "reason": "Duplicate"},
    })
    with pytest.raises(WorkIdentifierError, match="collision"):
        load_registry(path, repo_root=tmp_path)


def test_duplicate_json_properties_cannot_hide_a_reservation(tmp_path):
    path = tmp_path / "work-identifiers.json"
    path.write_text('{"schema_version":"WorkIdentifierRegistry.v1","identifiers":{},"identifiers":{}}', encoding="utf-8")
    with pytest.raises(WorkIdentifierError, match="duplicate identity registry property"):
        load_registry(path, repo_root=tmp_path)


def test_new_allocation_cannot_reclaim_a_reserved_retired_key(tmp_path):
    path = _registry_file(tmp_path, {
        "1": {"citation_key": "Original001", "status": "active"},
        "2": {"citation_key": "Friedman2026NewTitle003", "status": "retired", "reason": "Reserved historic URL"},
    })
    before = path.read_bytes()
    with pytest.raises(WorkIdentifierError, match="collision"):
        register_new_rows([_row(), _row(3, "New Title")], path, repo_root=tmp_path)
    assert path.read_bytes() == before


def test_missing_registry_does_not_rederive_public_identifiers(tmp_path):
    with pytest.raises(WorkIdentifierError, match="cannot read"):
        load_registry(tmp_path / "missing.json", repo_root=tmp_path)


@pytest.mark.parametrize("alias", ["symlink", "hardlink", "ancestor"])
def test_registry_alias_cannot_read_or_mutate_external_inode(tmp_path, alias):
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    external = _registry_file(outside)
    before = external.read_bytes()
    target = root / "data/work-identifiers.json"
    if alias == "ancestor":
        external.rename(outside / target.name)
        external = outside / target.name
        (root / "data").symlink_to(outside, target_is_directory=True)
    else:
        target.parent.mkdir()
        if alias == "symlink":
            target.symlink_to(external)
        else:
            os.link(external, target)
    with pytest.raises(UnsafeGeneratedOutputPathError):
        load_registry(target, repo_root=root)
    with pytest.raises(UnsafeGeneratedOutputPathError):
        register_new_rows([_row(), _row(3)], target, repo_root=root)
    assert external.read_bytes() == before


def _catalog_pair(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    registry = _registry_file(data)
    registry.rename(data / "work-identifiers.json")
    registry = data / "work-identifiers.json"
    bibliography = tmp_path / "BIBLIOGRAPHY.md"
    text = "| 1 | 2026 | 🧠 | Paper | Original title | Venue | — | — |\n"
    bibliography.write_text(text, encoding="utf-8")
    return bibliography, registry, text


def test_rejected_intake_candidate_leaves_both_sources_unchanged(tmp_path):
    bibliography, registry, before = _catalog_pair(tmp_path)
    registry_before = registry.read_bytes()
    candidate = before + f"| 3 | 2026 | 🧠 | Paper | {'A' * 220} | Venue | — | — |\n"
    with pytest.raises(WorkIdentifierError, match="unsafe citation key"):
        write_catalog_with_identifiers(bibliography, candidate, repo_root=tmp_path)
    assert bibliography.read_text(encoding="utf-8") == before
    assert registry.read_bytes() == registry_before


def test_registry_write_failure_rolls_back_bibliography_and_preserves_pair(tmp_path, monkeypatch):
    bibliography, registry, before = _catalog_pair(tmp_path)
    registry_before = registry.read_bytes()
    writer = work_identifiers.write_generated_output_text
    def fail_registry(repo_root, target, content):
        if target == registry:
            raise OSError("simulated registry disk failure")
        return writer(repo_root, target, content)
    monkeypatch.setattr(work_identifiers, "write_generated_output_text", fail_registry)
    candidate = before + "| 3 | 2026 | 🧠 | Paper | New title | Venue | — | — |\n"
    with pytest.raises(OSError, match="registry disk failure"):
        write_catalog_with_identifiers(bibliography, candidate, repo_root=tmp_path)
    assert bibliography.read_text(encoding="utf-8") == before
    assert registry.read_bytes() == registry_before


def test_concurrent_bibliography_edit_is_preserved_and_rejected(tmp_path):
    bibliography, registry, before = _catalog_pair(tmp_path)
    registry_before = registry.read_bytes()
    concurrent = before + "\nConcurrent documentation change\n"
    bibliography.write_text(concurrent, encoding="utf-8")
    with pytest.raises(WorkIdentifierError, match="changed concurrently"):
        write_catalog_with_identifiers(bibliography, before, repo_root=tmp_path, expected_previous=before)
    assert bibliography.read_text(encoding="utf-8") == concurrent
    assert registry.read_bytes() == registry_before


def test_bibliography_edit_during_preparation_is_preserved(tmp_path, monkeypatch):
    bibliography, registry, before = _catalog_pair(tmp_path)
    registry_before = registry.read_bytes()
    concurrent = before + "\nConcurrent documentation change\n"
    prepare = work_identifiers.prepare_new_rows

    def interleaved_prepare(*args, **kwargs):
        result = prepare(*args, **kwargs)
        bibliography.write_text(concurrent, encoding="utf-8")
        return result

    monkeypatch.setattr(work_identifiers, "prepare_new_rows", interleaved_prepare)
    candidate = before + "| 3 | 2026 | 🧠 | Paper | New title | Venue | — | — |\n"
    with pytest.raises(WorkIdentifierError, match="bibliography changed concurrently"):
        write_catalog_with_identifiers(bibliography, candidate, repo_root=tmp_path, expected_previous=before)
    assert bibliography.read_text(encoding="utf-8") == concurrent
    assert registry.read_bytes() == registry_before
