"""Reviewed virtual PDF routes must be complete, exact and actually assembled."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SOURCE = Path(__file__).resolve().parents[1] / "src"
if str(_SOURCE) not in sys.path:
    sys.path.append(str(_SOURCE))

from docxology_tools.paper_artifacts import PaperResources, source_paths  # noqa: E402
from docxology_tools.citation_metadata import CitationHead  # noqa: E402
from docxology_tools.scholar_readiness import build_report  # noqa: E402
import build_pages_artifact as bpa  # noqa: E402
import build_work_pages as bwp  # noqa: E402
import validate_repo as validator  # noqa: E402

REGISTRY = "data/scholar-pdf-projections.json"
ABSTRACT = "A complete author-written abstract in a disposable public fixture. It describes the documented question, approach and limits without asserting any real study result."


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdin=subprocess.DEVNULL,
        check=True,
        capture_output=True,
    )


@pytest.fixture
def pilot(tmp_path, monkeypatch):
    git(tmp_path, "init", "-q")
    folder = tmp_path / "papers/2026_Example"
    folder.mkdir(parents=True)
    (tmp_path / "works").mkdir()
    (tmp_path / "llms.txt").write_text("Public test fixture.\n")
    payload = b"%PDF-1.4\nDisposable fixture bytes, not a published study.\n"
    pdf = folder / "paper.pdf"
    pdf.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    work = dict(
        num=1,
        citation_key="Example",
        title="Example article",
        type="Paper",
        year=2026,
        doi="10.1234/example",
        docs_path="papers/2026_Example/",
        authors=["Example, Ada"],
        venue="Fixture Journal",
        domain="🧠",
        domain_name="Active Inference",
        url="https://doi.org/10.1234/example",
    )
    metadata = dict(
        title=work["title"],
        doi=work["doi"],
        abstract=ABSTRACT,
        primary_pdf="paper.pdf",
        citation_metadata=dict(
            doi=work["doi"],
            resource_type="journal-article",
            publication_date="2026-11-01",
            journal_title="Fixture Journal",
        ),
    )
    write_json(folder / "metadata.json", metadata)
    write_json(
        tmp_path / "papers/paper_metadata.json", {folder.name: {"abstract": ABSTRACT}}
    )
    write_json(tmp_path / "data/works.json", {"works": [work]})
    write_json(
        tmp_path / "data/work-identifiers.json",
        {
            "schema_version": "WorkIdentifierRegistry.v1",
            "identifiers": {"1": {"citation_key": "Example", "status": "active"}},
        },
    )
    bib = tmp_path / "pages/BIBLIOGRAPHY.md"
    bib.parent.mkdir()
    bib.write_text(
        "| 1 | 2026 | 🧠 | Paper | Example article | Fixture Journal | [DOI](https://doi.org/10.1234/example) | [Docs](../papers/2026_Example/) | Example, Ada |\n"
    )
    review = dict(
        reviewed_at="2026-11-05",
        reviewed_by="Public fixture review",
        rights=dict(
            license="CC BY 4.0",
            license_url="https://creativecommons.org/licenses/by/4.0/",
            evidence_page=1,
            evidence="Fixture redistribution license statement.",
            conditions="Retain author and source attribution and any credit-line conditions.",
        ),
        searchability=dict(
            method="First two pages text-extracted",
            first_page_text_sha256=hashlib.sha256(b"public text fixture").hexdigest(),
            nonblank_first_two_pages=True,
        ),
        scholarly_content=dict(
            kind="journal-article", basis="Publisher PDF and DOI identity reviewed"
        ),
        abstract=dict(
            source="papers/paper_metadata.json",
            sha256=hashlib.sha256(ABSTRACT.encode()).hexdigest(),
            complete_author_written=True,
            method="Complete PDF author abstract passage reviewed",
        ),
    )
    record = dict(
        num=1,
        citation_key="Example",
        doi=work["doi"],
        title=work["title"],
        docs_path=work["docs_path"],
        authors=work["authors"],
        publication_date="2026-11-01",
        source_pdf="papers/2026_Example/paper.pdf",
        bytes=len(payload),
        sha256=digest,
        alias=f"works/{digest}.pdf",
        review=review,
    )
    registry = dict(
        schema_version="ScholarPDFProjectionRegistry.v1",
        reservations=[record],
        selections={"Example": digest},
    )
    write_json(tmp_path / REGISTRY, registry)
    page = tmp_path / "works/Example.html"
    url = "https://danielarifriedman.com/" + record["alias"]
    page.write_text(
        '<html><head><meta name="citation_title" content="Example article"><meta name="citation_author" content="Ada Example"><meta name="citation_publication_date" content="2026/11/01"><meta name="citation_doi" content="10.1234/example"><meta name="citation_pdf_url" content="'
        + url
        + '"></head><body><main><p>'
        + ABSTRACT
        + "</p></main></body></html>"
    )
    git(tmp_path, "add", ".")
    git(
        tmp_path,
        "-c",
        "user.name=Public fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        "Reviewed source fixture",
    )
    monkeypatch.setattr(bpa, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        bpa, "ARTIFACT_MANIFEST", tmp_path / "data/pages-artifact-manifest.json"
    )
    monkeypatch.setattr(
        bpa, "GROWTH_REPORT", tmp_path / "reports/pages_artifact_growth_2026-11-05.json"
    )
    original_source = bpa.source_path
    monkeypatch.setattr(
        bpa,
        "source_path",
        lambda relative: original_source(relative, repo_root=tmp_path),
    )
    monkeypatch.setattr(bpa, "_superseded_report_paths", lambda: set())
    monkeypatch.setattr(bwp, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)
    return dict(
        root=tmp_path,
        folder=folder,
        pdf=pdf,
        payload=payload,
        work=work,
        metadata=metadata,
        record=record,
        registry=registry,
        url=url,
    )


def resources(pilot):
    return PaperResources.load(
        pilot["root"], pilot["work"]["docs_path"], source_paths(pilot["root"])
    )


def test_primary_web_route_preserves_the_original_source(pilot):
    found = resources(pilot)
    assert found.primary_pdf == pilot["pdf"]
    assert found.primary_pdf_url == pilot["url"]
    assert found.absolute_url(found.primary_pdf).endswith(
        "papers/2026_Example/paper.pdf"
    )
    assert not (pilot["root"] / pilot["record"]["alias"]).exists()


def test_citation_and_media_use_the_same_reviewed_route(pilot):
    work = {
        **pilot["work"],
        "_resources": resources(pilot),
        "enrichment": {"abstract": ABSTRACT},
    }
    page = bwp.render_work_page(work)
    assert CitationHead.parse(page).tags["citation_pdf_url"] == [pilot["url"]]
    assert pilot["url"] in bwp.json_ld(work)
    assert ABSTRACT in page and page.index(ABSTRACT, page.index("<main")) < page.index(
        'id="downloads"'
    )
    assert "CC BY 4.0" in page
    assert "papers/2026_Example/paper.pdf" in page


def test_alias_is_budgeted_manifested_and_actually_copied(pilot):
    baseline = sum(
        path.stat().st_size
        for path in pilot["root"].rglob("*")
        if path.is_file() and ".git" not in path.relative_to(pilot["root"]).parts
    )
    _, size = bpa.projected_size()
    assert size == baseline + len(pilot["payload"])
    manifest = bpa._manifest_payload()
    row = next(
        item
        for item in manifest["included_files"]
        if item["path"] == pilot["record"]["alias"]
    )
    assert (
        row["bytes"] == len(pilot["payload"])
        and row["sha256"] == pilot["record"]["sha256"]
    )
    destination = pilot["root"].parent / (pilot["root"].name + "-site")
    bpa.assemble(destination)
    assert (destination / pilot["record"]["alias"]).is_file()
    assert (destination / pilot["record"]["alias"]).read_bytes() == pilot["payload"]
    assert (destination / pilot["record"]["source_pdf"]).read_bytes() == pilot[
        "payload"
    ]
    assert pilot["pdf"].read_bytes() == pilot["payload"]


def test_reviewed_prerequisites_do_not_attest_indexing(pilot):
    report = build_report(pilot["root"])
    row = report["works"][0]
    assert "pdf_directory_differs_from_abstract" not in row["blockers"]
    assert row["primary_pdf"]["url"] == pilot["url"]
    assert (
        row["reviewed_prerequisites"]["complete_author_written_abstract"]["sha256"]
        == pilot["record"]["review"]["abstract"]["sha256"]
    )
    assert "actual_scholar_indexing" in row["unverified_requirements"]
    assert report["indexing_verified"] is False and report["network_checked"] is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("sha256", "f" * 64),
        ("bytes", True),
        ("source_pdf", "../outside.pdf"),
        ("alias", "works/../outside.pdf"),
        ("doi", "10.1234/other"),
        ("num", True),
        ("citation_key", "Another"),
        ("title", "Wrong article"),
    ],
)
def test_unbound_reservations_fail_closed(pilot, field, value):
    pilot["registry"]["reservations"][0][field] = value
    write_json(pilot["root"] / REGISTRY, pilot["registry"])
    with pytest.raises(ValueError):
        resources(pilot)


@pytest.mark.parametrize(
    "change", ["abstract", "reviewer", "rights", "searchability", "duplicate"]
)
def test_review_drift_is_not_a_crawler_approval(pilot, change):
    record = pilot["registry"]["reservations"][0]
    if change == "abstract":
        record["review"]["abstract"]["sha256"] = "0" * 64
    elif change == "reviewer":
        record["review"]["reviewed_by"] = ""
    elif change == "rights":
        record["review"]["rights"]["license"] = ""
    elif change == "searchability":
        record["review"]["searchability"]["nonblank_first_two_pages"] = False
    else:
        pilot["registry"]["reservations"].append(copy.deepcopy(record))
    write_json(pilot["root"] / REGISTRY, pilot["registry"])
    with pytest.raises(ValueError):
        resources(pilot)


@pytest.mark.parametrize("link_kind", ["symlink", "hardlink"])
def test_source_links_cannot_supply_alias_bytes(pilot, link_kind):
    original = pilot["pdf"]
    saved = original.with_name("retained.pdf")
    original.rename(saved)
    if link_kind == "symlink":
        original.symlink_to(saved)
    else:
        original.hardlink_to(saved)
    with pytest.raises(ValueError):
        resources(pilot)


def test_alias_collision_is_not_an_authorized_copy(pilot):
    (pilot["root"] / pilot["record"]["alias"]).write_bytes(b"unreviewed collision")
    with pytest.raises(ValueError):
        bpa.projected_size()


def test_retiring_an_association_does_not_drop_the_public_alias(pilot):
    pilot["registry"]["selections"].clear()
    write_json(pilot["root"] / REGISTRY, pilot["registry"])
    assert resources(pilot).primary_pdf_url.endswith("papers/2026_Example/paper.pdf")
    destination = pilot["root"].parent / (pilot["root"].name + "-retired-site")
    bpa.assemble(destination)
    assert (destination / pilot["record"]["alias"]).read_bytes() == pilot["payload"]


def test_only_verified_virtual_targets_can_satisfy_local_links(pilot):
    page = pilot["root"] / "works/Example.html"
    page.write_text('<a href="' + Path(pilot["record"]["alias"]).name + '">PDF</a>')
    validator.validate_local_links()
    page.write_text('<a href="' + "e" * 64 + '.pdf">Unregistered</a>')
    with pytest.raises(SystemExit, match="Missing local links"):
        validator.validate_local_links()


@pytest.mark.parametrize("hidden", ["short", "details", "script", "hidden"])
def test_complete_abstract_must_be_visible_in_the_actual_source_page(pilot, hidden):
    page = pilot["root"] / "works/Example.html"
    replacement = {
        "short": "A shortened summary.",
        "details": "<details><summary>Abstract</summary>" + ABSTRACT + "</details>",
        "script": '<script type="application/ld+json">' + ABSTRACT + "</script>",
        "hidden": "<span hidden>" + ABSTRACT + "</span>",
    }[hidden]
    page.write_text(page.read_text().replace(ABSTRACT, replacement))
    assert (
        "complete_author_abstract_not_visible"
        in build_report(pilot["root"])["works"][0]["blockers"]
    )


def test_aggregate_cap_counts_preserved_noncurrent_aliases(pilot):
    large = b"%PDF-1.4\n" + b"x" * (3 * 1024 * 1024)
    pilot["pdf"].write_bytes(large)
    record = pilot["registry"]["reservations"][0]
    record.update(bytes=len(large), sha256=hashlib.sha256(large).hexdigest())
    record["alias"] = "works/" + record["sha256"] + ".pdf"
    pilot["registry"]["selections"] = {"Example": record["sha256"]}
    other = copy.deepcopy(record)
    other_path = pilot["folder"] / "previous.pdf"
    other_path.write_bytes(large + b"older")
    other.update(
        source_pdf="papers/2026_Example/previous.pdf",
        bytes=other_path.stat().st_size,
        sha256=hashlib.sha256(other_path.read_bytes()).hexdigest(),
    )
    other["alias"] = "works/" + other["sha256"] + ".pdf"
    pilot["registry"]["reservations"].append(other)
    write_json(pilot["root"] / REGISTRY, pilot["registry"])
    with pytest.raises(ValueError, match="5 MiB"):
        bpa.projected_size()


def test_remote_edition_can_retire_current_route_without_dropping_old_alias(pilot):
    pilot["metadata"]["remote_primary_pdf"] = dict(
        name="remote.pdf",
        url="https://zenodo.org/records/1234/files/remote.pdf",
        version="2.0",
        record_id="1234",
        bytes=30,
        sha256="c" * 64,
    )
    write_json(pilot["folder"] / "metadata.json", pilot["metadata"])
    pilot["registry"]["selections"].clear()
    write_json(pilot["root"] / REGISTRY, pilot["registry"])
    assert (
        resources(pilot).primary_pdf_url
        == pilot["metadata"]["remote_primary_pdf"]["url"]
    )
    destination = pilot["root"].parent / (pilot["root"].name + "-remote-site")
    bpa.assemble(destination)
    assert (destination / pilot["record"]["alias"]).read_bytes() == pilot["payload"]


def test_equal_size_source_changes_revoke_the_review(pilot):
    pilot["pdf"].write_bytes(b"y" * len(pilot["payload"]))
    with pytest.raises(ValueError, match="reviewed bytes"):
        resources(pilot)


@pytest.mark.parametrize("link_kind", ["symlink", "hardlink"])
def test_review_registry_itself_cannot_be_a_filesystem_alias(pilot, link_kind):
    registry = pilot["root"] / REGISTRY
    saved = registry.with_name("retained-review.json")
    registry.rename(saved)
    if link_kind == "symlink":
        registry.symlink_to(saved)
    else:
        registry.hardlink_to(saved)
    with pytest.raises(ValueError):
        resources(pilot)


def test_duplicate_review_json_properties_are_not_last_writer_wins(pilot):
    registry = pilot["root"] / REGISTRY
    registry.write_text(
        registry.read_text().replace(
            '"selections":', '"selections": {}, "selections":', 1
        )
    )
    with pytest.raises(ValueError, match="Duplicate"):
        resources(pilot)


def test_initial_published_alias_reservations_are_immutable_and_byte_bound():
    from docxology_tools.scholar_pdf_projection import (
        PILOT_BYTE_LIMIT,
        verified_projections,
    )

    root = Path(__file__).resolve().parents[2]
    frozen = json.loads(
        (Path(__file__).parent / "fixtures/scholar-pdf-reservations.json").read_text()
    )
    registry = json.loads((root / REGISTRY).read_text())
    records = {item["alias"]: item for item in registry["reservations"]}
    actual = verified_projections(root)
    assert frozen.keys() <= records.keys() and frozen.keys() <= actual.keys()
    for alias, fields in frozen.items():
        assert {key: records[alias][key] for key in fields} == fields
        assert (
            hashlib.sha256(actual[alias].read_bytes()).hexdigest() == fields["sha256"]
        )
    assert sum(item.bytes for item in actual.values()) <= PILOT_BYTE_LIMIT


def test_source_sensitive_steps_own_the_projection_inputs():
    from docxology_tools.generation_plan import (
        LOCAL_GENERATION_STEPS,
        effective_step_inputs,
    )

    required = {
        REGISTRY,
        "data/work-identifiers.json",
        "pages/BIBLIOGRAPHY.md",
        "papers/paper_metadata.json",
        "code/src/scholar_pdf_projection.py",
    }
    steps = {step.identifier: step for step in LOCAL_GENERATION_STEPS}
    for name in ("work-pages", "paper-pages", "scholar-readiness"):
        assert required <= set(effective_step_inputs(steps[name]))
    assert not steps[
        "pages-artifact"
    ].inputs  # Every artifact operation revalidates its full source set.


def test_seo_gate_rejects_a_hidden_complete_abstract_even_with_correct_head(pilot):
    from docxology_tools.seo_invariants import check_work_citations

    page = pilot["root"] / "works/Example.html"
    page.write_text(
        page.read_text().replace(
            "</head>",
            '<meta name="citation_journal_title" content="Fixture Journal"></head>',
        )
    )
    assert check_work_citations(pilot["root"]) == []
    page.write_text(
        page.read_text().replace(ABSTRACT, "<details>" + ABSTRACT + "</details>")
    )
    assert any(
        "complete author abstract is not publicly visible" in error
        for error in check_work_citations(pilot["root"])
    )


def test_content_audit_treats_reviewed_pdf_alias_as_attachment(pilot):
    from docxology_tools.content_audit import audit_content

    page = pilot["root"] / "index.html"
    page.write_text(
        '<main><a href="' + pilot["record"]["alias"] + '">Read PDF</a></main>'
    )
    report = audit_content(
        pilot["root"],
        [page],
        [pilot["work"]],
        published_paths={Path(pilot["record"]["alias"])},
    )
    assert report["errors"] == []
    assert report["citations"] == []
    page.write_text('<main><a href="works/' + "a" * 64 + '.pdf">Unreviewed</a></main>')
    assert any(
        "missing local target" in error
        for error in audit_content(pilot["root"], [page], [pilot["work"]])["errors"]
    )


def test_replaced_pdf_is_refused_without_unbounded_read(pilot, monkeypatch):
    projection = resources(pilot).scholar_pdf
    pilot["pdf"].write_bytes(pilot["payload"] + b"x" * 100000)
    real_open = Path.open
    reads = []

    class BoundedSource:
        def __enter__(self):
            self.stream = real_open(pilot["pdf"], "rb")
            return self

        def __exit__(self, *args):
            self.stream.close()

        def read(self, size=-1):
            assert 0 <= size <= projection.bytes + 1, "unbounded PDF allocation"
            data = self.stream.read(size)
            reads.append(len(data))
            return data

    def opening(path, *args, **kwargs):
        if path == pilot["pdf"]:
            return BoundedSource()
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", opening)
    with pytest.raises(ValueError, match="reviewed bytes"):
        projection.read_bytes()
    assert sum(reads) <= projection.bytes + 1
