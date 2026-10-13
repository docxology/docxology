"""Reviewed author identity types without punctuation-based organization guesses."""
import json
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.author_entities import author_entity, verified_author_types  # noqa: E402
import build_work_pages as bwp  # noqa: E402
import sync_publications_html as sph  # noqa: E402
from docxology_tools.biblio_table import BiblioRow  # noqa: E402


def work_and_records():
    work = {"citation_key": "Example", "doi": "10.1234/example", "authors": ["Friedman, Daniel Ari", "Alexandra Mikhailova", "Research Collective"]}
    records = {"Example": {"doi": "10.1234/EXAMPLE", "status": "verified", "authors": [{"family": "Friedman", "given": "Daniel Ari"}, {"family": "Alexandra Mikhailova", "given": ""}, {"literal": "Research Collective"}]}}
    return work, records


def test_verified_structured_person_and_literal_have_source_backed_types():
    work, records = work_and_records()
    assert verified_author_types(work, records) == {"Friedman, Daniel Ari": "Person", "Alexandra Mikhailova": "Person", "Research Collective": "Organization"}


@pytest.mark.parametrize("change", ["doi", "status", "missing-doi", "wrong-name"])
def test_unbound_or_unverified_records_never_establish_type(change):
    work, records = work_and_records()
    record = records["Example"]
    if change == "doi":
        record["doi"] = "10.1234/other"
    elif change == "status":
        record["status"] = "title_mismatch"
    elif change == "missing-doi":
        work["doi"] = ""
    else:
        record["authors"] = [{"family": "Other Person"}]
    types = verified_author_types(work, records)
    assert "Alexandra Mikhailova" not in types
    assert author_entity("Alexandra Mikhailova", {}, types.get("Alexandra Mikhailova")) == {"name": "Alexandra Mikhailova"}


def test_unknown_plain_name_remains_unknown_and_explicit_literal_with_comma_is_organization():
    assert author_entity("Unknown Name", {}) == {"name": "Unknown Name"}
    assert author_entity("Institute, Research", {}, "Organization") == {"@type": "Organization", "name": "Institute, Research"}
    assert author_entity("Mikhailova, Alexandra", {}) == {"@type": "Person", "name": "Alexandra Mikhailova"}


def test_both_renderers_preserve_order_names_and_principal_identity():
    work, records = work_and_records()
    types = verified_author_types(work, records)
    individual = bwp.author_ld({**work, "_author_types": types})
    collection = sph._author_block(work["authors"], types)
    for authors, principal in ((individual, bwp.PRINCIPAL_LD), (collection, sph.PRINCIPAL)):
        assert authors[0] is principal
        assert any("orcid.org" in url for url in principal["sameAs"])
        assert [author["name"] for author in authors] == ["Daniel Ari Friedman", "Alexandra Mikhailova", "Research Collective"]
        assert [author["@type"] for author in authors] == ["Person", "Person", "Organization"]


def test_work_renderer_reads_author_registry_once_per_load(monkeypatch):
    work, records = work_and_records()
    loaded = []
    monkeypatch.setattr(bwp, "load_author_records", lambda root: loaded.append(root) or records)
    monkeypatch.setattr(bwp, "load_publishing_status", lambda: {})
    # Existing source loader is read-only; substitute only its small JSON input.
    from io import StringIO
    import builtins
    original = builtins.open
    monkeypatch.setattr(builtins, "open", lambda path, *a, **kw: StringIO(json.dumps({"works": [work, work]})) if Path(path) == bwp.REPO_ROOT / "data/works.json" else original(path, *a, **kw))
    works = bwp.load_works()
    assert len(loaded) == 1
    assert all(bwp.author_ld(value)[1]["@type"] == "Person" for value in works)


def test_collection_renderer_reads_author_registry_once_and_uses_bound_type(monkeypatch):
    work, records = work_and_records()
    loaded = []
    monkeypatch.setattr(sph, "load_author_records", lambda root: loaded.append(root) or records)
    row = BiblioRow(1, "2026", "Computational", "Paper", "Example", "Zenodo", "https://doi.org/10.1234/example", "", "; ".join(work["authors"]))
    # Supply the authoritative projection directly so this focuses on typing.
    work.update(title="Example", year=2026, type="Paper", domain_name="Computational", url="https://doi.org/10.1234/example")
    result = sph.build_collection_page([row, row._replace(num=2)], {1: work, 2: work})
    assert len(loaded) == 1
    assert all(entity["author"][1]["@type"] == "Person" for entity in result["mainEntity"])


def test_actual_new_coauthor_is_person_in_both_source_renderers():
    work = next(work for work in bwp.load_works() if work["citation_key"] == "Friedman2026ActiveInferenceSyntheticOverview225")
    authors = bwp.author_ld(work)
    assert authors[1] == {"@type": "Person", "name": "Alexandra Mikhailova"}
    row = next(row for row in sph.load_rows() if row.num == work["num"])
    collection = sph.build_collection_page([row], {row.num: work})
    assert collection["mainEntity"][0]["author"][1] == {"@type": "Person", "name": "Alexandra Mikhailova"}


def test_generic_name_only_never_establishes_personhood():
    work, records = work_and_records()
    records["Example"]["authors"] = [{"name": "Research Collective"}]
    types = verified_author_types(work, records)
    assert types == {}
    assert author_entity("Research Collective", {}, types.get("Research Collective")) == {"name": "Research Collective"}


def test_explicit_given_only_person_field_preserves_exact_source_name():
    work, records = work_and_records()
    records["Example"]["authors"] = [{"family": "", "given": "Alexandra Mikhailova"}]
    assert verified_author_types(work, records) == {"Alexandra Mikhailova": "Person"}
