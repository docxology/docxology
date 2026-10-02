"""Citation exports preserve confirmed author lists and omit unknown authors."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.biblio_table import BiblioRow  # noqa: E402
from export_bibliography import author_names, bibtex_entry, csl_item, ris_record, row_to_work  # noqa: E402


def _work(authors_cell: str, work_type: str = "Paper"):
    row = BiblioRow(
        num=1, year="2026", domain="🧠", typ=work_type,
        title="Source-authority example", venue="Source venue",
        link_cell="https://example.test/work", docs_cell="", authors_cell=authors_cell,
    )
    return row_to_work(row, visible_source_paths=frozenset())


@pytest.mark.parametrize("authors_cell", ["", "—", "-"])
@pytest.mark.parametrize("work_type", ["Paper", "Book Chapter", "Course", "Series"])
def test_unknown_authors_are_omitted_from_every_citation_format(authors_cell, work_type):
    work = _work(authors_cell, work_type)
    assert author_names(work) == []
    assert "  author =" not in bibtex_entry(work)
    assert "author" not in csl_item(work)
    assert not any(line.startswith("AU  -") for line in ris_record(work).splitlines())
    assert work.title in bibtex_entry(work)
    assert csl_item(work)["title"] == work.title
    assert f"TI  - {work.title}" in ris_record(work)


def test_confirmed_people_and_collective_authors_keep_their_source_order():
    authors = ["Smith, Alex", "Active Inference Institute", "Friedman, Daniel Ari"]
    work = _work("; ".join(authors))
    assert author_names(work) == authors
    assert f"  author = {{{' and '.join(authors)}}}" in bibtex_entry(work)
    assert csl_item(work)["author"] == [
        {"family": "Smith", "given": "Alex"},
        {"literal": "Active Inference Institute"},
        {"family": "Friedman", "given": "Daniel Ari"},
    ]
    assert [line.removeprefix("AU  - ") for line in ris_record(work).splitlines() if line.startswith("AU  - ")] == authors


def test_export_author_list_does_not_mutate_the_source_work():
    work = _work("Smith, Alex")
    exported = author_names(work)
    exported.append("Unconfirmed contributor")
    assert work.authors == ["Smith, Alex"]
