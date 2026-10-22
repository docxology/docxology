from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.author_entities import reviewed_contributor_role  # noqa: E402
from docxology_tools.content_audit import ContentPage, audit_content  # noqa: E402
from docxology_tools.content_citations import ContentCitations  # noqa: E402
from docxology_tools.biblio_table import BiblioRow  # noqa: E402
from export_bibliography import bibtex_entry, csl_item, ris_record, row_to_work  # noqa: E402
import build_work_pages  # noqa: E402
import sync_publications_html  # noqa: E402


def work():
    return dict(num=1, citation_key="StableKey", title="A & B <study>", year=2018,
                authors=["First, A.", "Second, B.", "Third, C."], venue="A & B", doi="10.1234/source", url="https://doi.org/10.1234/source")


def test_catalog_identity_supplies_citation_not_key_prefix():
    value = work()
    refs = ContentCitations([value])
    citation = refs.cite(value["citation_key"])
    page = ContentPage(citation)
    assert page.links[0]["href"] == "works/StableKey.html"
    assert page.links[0]["text"] == value["title"]
    assert "First, Second &amp; Third, 2018" in citation
    refs.cite(value["citation_key"])
    assert refs.used == [value["citation_key"]]
    assert refs.source_urls() == [value["url"]]
    assert all(name in refs.references() for name in value["authors"])


@pytest.mark.parametrize("count", [1, 2, 4])
def test_author_labels_follow_catalog_order(count):
    value = work()
    value["authors"] = [f"Family{i}, Person{i}" for i in range(count)]
    citation = ContentCitations([value]).cite(value["citation_key"])
    if count == 1:
        assert "(Family0, 2018)" in citation
    elif count == 2:
        assert "(Family0 &amp; Family1, 2018)" in citation
    else:
        assert "(Family0 et al., 2018)" in citation


def test_missing_or_duplicate_identity_fails_closed():
    value = work()
    with pytest.raises(ValueError, match="Duplicate"):
        ContentCitations([value, value])
    with pytest.raises(KeyError):
        ContentCitations([value]).cite("Missing")
    value["authors"] = []
    with pytest.raises(ValueError, match="Missing reviewed authors"):
        ContentCitations([value]).cite(value["citation_key"])


def fixture_page(tmp_path, text):
    (tmp_path / "works").mkdir(exist_ok=True)
    target = tmp_path / "works/StableKey.html"
    target.write_text('<main id="valid"></main>')
    path = tmp_path / "index.html"
    path.write_text("<main>" + text + "</main>")
    return [path, target]


def test_audit_catches_real_wrong_author_year_title_and_target(tmp_path):
    value = work()
    citation = ContentCitations([value]).cite(value["citation_key"])
    refs = ContentCitations([value])
    refs.cite(value["citation_key"])
    paths = fixture_page(tmp_path, citation + refs.references())
    assert audit_content(tmp_path, paths, [value])["errors"] == []
    paths[0].write_text("<main>" + citation.replace('"', "'") + refs.references() + "</main>")
    assert audit_content(tmp_path, paths, [value])["errors"] == []
    paths[0].write_text("<main>" + citation.replace('"', "'").replace("First, Second &amp; Third", "Wrong Authors") + refs.references() + "</main>")
    assert any("differs from catalog" in e for e in audit_content(tmp_path, paths, [value])["errors"])
    for old, new in (("First, Second &amp; Third", "Invented &amp; Authors"), ("2018", "2020"),
                     ("A &amp; B &lt;study&gt;", "Unrelated title"), ("StableKey.html", "Absent.html")):
        paths[0].write_text("<main>" + citation.replace(old, new) + "</main>")
        errors = audit_content(tmp_path, paths, [value])["errors"]
        assert any("differs from catalog" in error for error in errors)


def test_audit_checks_same_origin_absolute_urls_fragments_and_does_not_read_comment_links(tmp_path):
    value = work()
    paths = fixture_page(tmp_path, '<a href="https://danielarifriedman.com/works/StableKey.html#valid">valid</a>'
                         '<!-- <a href="missing.html">comment</a> -->'
                         '<a href="https://example.test/source">external</a>')
    report = audit_content(tmp_path, paths, [value])
    assert report["errors"] == []
    assert report["fragments_checked"] == 1
    assert list(report["external_links"]) == ["https://example.test/source"]
    paths[0].write_text('<main><a href="works/StableKey.html#absent">bad</a><a href="missing.html">bad</a></main>')
    errors = audit_content(tmp_path, paths, [value])["errors"]
    assert len(errors) == 2
    assert "missing fragment" in errors[0]
    assert "missing local target" in errors[1]


def test_audit_rejects_existing_files_omitted_from_pages_projection(tmp_path):
    paths = fixture_page(tmp_path, '<a href="works/StableKey.html">work</a>')
    report = audit_content(tmp_path, paths, [work()], published_paths={Path("index.html")})
    assert any("absent from the Pages projection" in error for error in report["errors"])


def test_false_joint_authorship_is_detected_in_html_and_markdown(tmp_path):
    value = work()
    value["docs_path"] = "papers/Example/"
    paths = fixture_page(tmp_path, '<a data-cited-author="Invented" href="works/StableKey.html">work</a>')
    (tmp_path / "pages").mkdir()
    source = tmp_path / "pages/COLLABORATORS.md"
    source.write_text("### An Invented\n**Joint publications**: [Example](../papers/Example/)\n")
    errors = audit_content(tmp_path, paths, [value])["errors"]
    assert len(errors) == 2
    assert "absent from the contributors" in errors[0]
    assert "joint-publication attribution" in errors[1]
    paths[0].write_text(paths[0].read_text().replace("Invented", "First"))
    source.write_text(source.read_text().replace("Invented", "First"))
    assert audit_content(tmp_path, paths, [value])["errors"] == []


def test_editors_require_bound_evidence_and_export_correct_roles():
    value = work()
    record = dict(num=value["num"], title=value["title"], status="document_verified", contributor_role="editor",
                  authors=[dict(family=name.split(", ")[0], given=name.split(", ")[1]) for name in value["authors"]],
                  evidence="EDITED BY First, Second, and Third")
    records = {value["citation_key"]: record}
    assert reviewed_contributor_role(value, records) == "editor"
    for field, invalid in (("num", 2), ("title", "Another book"), ("status", "unverified"), ("authors", []), ("evidence", "AUTHORED BY First")):
        with pytest.raises(ValueError, match="matching document evidence"):
            reviewed_contributor_role(value, {value["citation_key"]: {**record, field: invalid}})
    with pytest.raises(ValueError, match="Unsupported"):
        reviewed_contributor_role(value, {value["citation_key"]: {**record, "contributor_role": "unknown"}})
    row = BiblioRow(1, "2018", "Computational", "Book", "Edited volume", "Publisher", "https://example.test/book", "", "First, A.; Second, B.")
    exported = replace(row_to_work(row, visible_source_paths=frozenset()), citation_key="StableKey")
    assert "editor =" in bibtex_entry(exported, contributor_role="editor")
    assert "author =" not in bibtex_entry(exported, contributor_role="editor")
    assert "editor" in csl_item(exported, contributor_role="editor")
    assert "author" not in csl_item(exported, contributor_role="editor")
    assert "ED  - First, A." in ris_record(exported, contributor_role="editor")
    assert "AU  -" not in ris_record(exported, contributor_role="editor")
    value["contributor_role"] = "editor"
    assert "eds." in ContentCitations([value]).cite("StableKey")
    assert "Edited by" in build_work_pages.byline_html(value)
    collection = sync_publications_html.main_entity_object(row, row.link_cell, value)
    assert "editor" in collection
    assert "author" not in collection


def test_all_guide_inline_citations_and_references_close_over_catalog():
    from docxology_tools.pillar_content import guides

    root = Path(__file__).resolve().parents[2]
    works = json.loads((root / "data/works.json").read_text())["works"]
    catalog = {w["citation_key"]: w for w in works}
    for guide in guides(works):
        page = ContentPage("<main>" + "".join(body for _, body in guide["sections"][:-1]) + "</main>")
        cited = [link for link in page.links if link["href"].startswith("works/")]
        for link in cited:
            key = Path(link["href"]).stem
            assert link["text"] == catalog[key]["title"]
        references = guide["sections"][-1][1]
        referenced_keys = {Path(link["href"]).stem for link in ContentPage(references).links if link["href"].startswith("works/")}
        assert referenced_keys == {Path(link["href"]).stem for link in cited}
        source_urls = {link["href"] for link in ContentPage(references).links if not link["href"].startswith("works/")}
        assert source_urls == set(guide["citation_urls"])


@pytest.mark.parametrize("field,invalid", [("title", "Unrelated work"), ("doi", "10.1234/other"),
                                          ("num", 999), ("authors", []), ("evidence", []),
                                          ("source", "../outside.json")])
def test_website_author_receipt_rejects_changed_identity(field, invalid):
    from fetch_work_authors import document_evidence_errors

    root = Path(__file__).resolve().parents[2]
    records = json.loads((root / "data/work-authors.json").read_text())["works"]
    key = "Friedman2021InnovatorSDigitalPlaybook078"
    payload = {"works": {key: records[key]}}
    assert document_evidence_errors(payload) == []
    payload["works"][key][field] = invalid
    assert document_evidence_errors(payload)
