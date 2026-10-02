from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402,F401
import build_work_pages as bwp  # noqa: E402
import regenerate_docs as rd  # noqa: E402
from docxology_tools.paper_artifacts import PaperResources  # noqa: E402


def _fixture(monkeypatch, tmp_path, *, readme="", skill="", metadata=None):
    folder = tmp_path / "papers" / "2026_Example"
    folder.mkdir(parents=True)
    files = {"README.md": readme, "SKILL.md": skill}
    if metadata is not None:
        files["metadata.json"] = json.dumps(metadata)
    for name, text in files.items():
        (folder / name).write_text(text, encoding="utf-8")
    monkeypatch.setattr(bwp, "REPO_ROOT", tmp_path)
    visible = frozenset((folder / name).relative_to(tmp_path).as_posix() for name in files)
    resources = PaperResources.load(tmp_path, "papers/2026_Example/", visible)
    work = {"citation_key": "Example2026", "docs_path": "papers/2026_Example/"}
    return work, resources, visible


def test_curated_abstract_preserves_complete_result_and_scope(monkeypatch, tmp_path):
    abstract = "Historical context. " * 90 + "The geometric result is exact; no historical influence is claimed."
    work, resources, _ = _fixture(monkeypatch, tmp_path, readme="## Abstract\n\nHistorical context...\n")
    enriched = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"abstract": abstract}})
    assert enriched["abstract"] == abstract
    assert enriched["sources"]["abstract"] == "papers/paper_metadata.json"


@pytest.mark.parametrize("abstract", [None, "", "No abstract is recorded for this work yet; see the DOI."])
def test_explicit_missing_abstract_does_not_resurrect_stale_document(monkeypatch, tmp_path, abstract):
    work, resources, _ = _fixture(monkeypatch, tmp_path, readme="## Abstract\n\nUnsupported old synopsis.\n")
    enriched = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"abstract": abstract}})
    assert enriched["abstract"] == ""
    assert "abstract" not in enriched["sources"]


def test_document_fallback_is_complete_and_missing_notice_is_not_an_abstract(monkeypatch, tmp_path):
    abstract = "A complete hand-authored statement. " * 45 + "The final qualification remains visible."
    work, resources, _ = _fixture(
        monkeypatch, tmp_path,
        readme="## Abstract\n\n> No abstract is recorded for this work yet; see the DOI.\n",
        skill="## Abstract\n\n" + abstract,
    )
    enriched = bwp.enrichment_for(work, resources=resources, curated={})
    assert enriched["abstract"] == abstract
    assert enriched["sources"]["abstract"] == "papers/2026_Example/SKILL.md"


def test_folder_topic_is_not_a_keyword_and_explicit_curated_empty_wins(monkeypatch, tmp_path):
    work, resources, _ = _fixture(
        monkeypatch, tmp_path,
        readme="## Keywords\n\n`Example`\n",
        skill="## Keywords\n\n`real subject`\n",
    )
    enriched = bwp.enrichment_for(work, resources=resources, curated={})
    assert enriched["keywords"] == ["real subject"]
    assert enriched["sources"]["keywords"] == "papers/2026_Example/SKILL.md"
    empty = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"keywords": []}})
    assert empty["keywords"] == []
    assert "keywords" not in empty["sources"]


def test_an_explicit_curated_keyword_can_name_the_work(monkeypatch, tmp_path):
    work, resources, _ = _fixture(monkeypatch, tmp_path)
    enriched = bwp.enrichment_for(work, resources=resources, curated={
        "2026_Example": {"keywords": ["Example", "geometric model"]},
    })
    assert enriched["keywords"] == ["Example", "geometric model"]


def test_each_field_records_its_actual_source_and_concepts_are_separate(monkeypatch, tmp_path):
    work, resources, _ = _fixture(
        monkeypatch, tmp_path,
        readme="## Key Findings\n\n- A measured association was observed in six colonies.\n",
        skill="## Keywords\n\n`colony variation`\n\n## Key Concepts\n\n- A proposed coordination mechanism.\n",
        metadata={"methods": [{"name": "RNA sequencing", "description": "Three pooled libraries per colony."}]},
    )
    enriched = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"abstract": "Curated background."}})
    assert enriched["sources"] == {
        "abstract": "papers/paper_metadata.json",
        "keywords": "papers/2026_Example/SKILL.md",
        "methods": "papers/2026_Example/metadata.json",
        "findings": "papers/2026_Example/README.md",
        "concepts": "papers/2026_Example/SKILL.md",
    }
    assert enriched["findings"] == ["A measured association was observed in six colonies."]
    assert enriched["concepts"] == ["A proposed coordination mechanism."]
    assert enriched["methods"] == ["RNA sequencing — Three pooled libraries per colony."]


def test_grounded_metadata_preserves_result_echo_and_all_qualifications(monkeypatch, tmp_path):
    findings = ["The author reports one measured run; independent execution was not performed."]
    findings += [f"Qualified observation {index} within this source snapshot." for index in range(6)]
    methods = [{"name": f"Specific source method {index}", "description": "Simulated agents only."} for index in range(7)]
    work, resources, _ = _fixture(
        monkeypatch, tmp_path,
        readme="## Key Findings\n\n- Stale claim.\n",
        metadata={"methods": methods, "key_findings": findings, "summary_provenance": {"source": "full_text.md", "date": "2026-10-01"}},
    )
    enriched = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"abstract": findings[0]}})
    assert enriched["findings"] == findings
    assert len(enriched["methods"]) == 7
    assert all(method.endswith("Simulated agents only.") for method in enriched["methods"])
    assert enriched["sources"]["findings"] == "papers/2026_Example/metadata.json"


def test_cleared_summaries_do_not_fall_back_to_stale_readme_or_skill(monkeypatch, tmp_path):
    stale = "## Methods\n\n- Unsupported old procedure.\n\n## Key Findings\n\n- Unsupported old result.\n"
    work, resources, _ = _fixture(monkeypatch, tmp_path, readme=stale, skill=stale, metadata={"methods": [], "key_findings": []})
    enriched = bwp.enrichment_for(work, resources=resources, curated={})
    assert enriched["methods"] == enriched["findings"] == []
    assert "methods" not in enriched["sources"]
    assert "findings" not in enriched["sources"]


def test_generic_templates_and_noninformative_descriptions_are_suppressed(monkeypatch, tmp_path):
    work, resources, _ = _fixture(monkeypatch, tmp_path, metadata={
        "methods": [{"name": "Field observation and behavioral assays"}, {"name": "Specific assay", "description": "Applied Specific assay approach."}],
        "key_findings": ["See full paper for detailed findings and analysis"],
    })
    enriched = bwp.enrichment_for(work, resources=resources, curated={})
    assert enriched["methods"] == ["Specific assay"]
    assert enriched["findings"] == []


def test_public_provenance_does_not_copy_internal_notes_or_private_paths(monkeypatch, tmp_path):
    work, resources, _ = _fixture(monkeypatch, tmp_path, metadata={
        "abstract_provenance": {"source": "/Users/private/source.md", "date": "2026-10-01", "notes": "Internal review rationale", "url": "https://user:password@example.test/source"},
        "methods": [{"name": "Specific source method"}],
        "summary_provenance": {"source": "full_text.md", "work_kind": "theoretical", "reviewed": "Agent notes", "notes": "Internal review rationale"},
    })
    enriched = bwp.enrichment_for(work, resources=resources, curated={"2026_Example": {"abstract": "Curated abstract."}})
    assert enriched["abstract_provenance"] == {"date": "2026-10-01"}
    assert enriched["summary_provenance"] == {"source": "full_text.md", "work_kind": "theoretical"}


def test_batch_loads_inventory_once_and_reuses_attached_resources(monkeypatch, tmp_path):
    work, resources, visible = _fixture(monkeypatch, tmp_path, readme="## Abstract\n\nHand-authored abstract.\n")
    master = {"2026_Example": {"abstract": "Full curated abstract."}}
    (tmp_path / "papers" / "paper_metadata.json").write_text(json.dumps(master), encoding="utf-8")
    visible = visible | {"papers/paper_metadata.json"}
    calls = []

    def inventory(root):
        calls.append(root)
        return visible

    monkeypatch.setattr(bwp, "source_paths", inventory)
    result = bwp.enrichment_map([work, dict(work, citation_key="Another2026")])
    assert len(calls) == 1
    assert result["Example2026"]["abstract"] == "Full curated abstract."
    calls.clear()
    bwp.enrichment_map([dict(work, _resources=resources)], visible_paths=visible)
    assert calls == []


def test_invalid_curated_collection_fails_instead_of_using_generated_fallback(monkeypatch, tmp_path):
    work, resources, _ = _fixture(monkeypatch, tmp_path, readme="## Abstract\n\nOld synopsis.\n")
    with pytest.raises(ValueError, match="Consolidated paper metadata"):
        bwp.enrichment_for(work, resources=resources, curated=[])


@pytest.mark.parametrize("keywords", [None, []])
def test_readme_keeps_the_full_abstract_and_omits_synthetic_topic_keywords(monkeypatch, tmp_path, keywords):
    _fixture(monkeypatch, tmp_path)
    abstract = "Historical context and source qualifications. " * 30
    abstract += "Only exterior cameras are covered, and no historical influence is claimed."
    readme = rd.generate_readme("2026_Example", {
        "name": "Example work",
        "authors": "Daniel Ari Friedman",
        "abstract": abstract,
        "keywords": keywords,
    }, paths=rd.DocumentPaths(tmp_path / "papers", tmp_path / "pages" / "BIBLIOGRAPHY.md"))
    assert f"> {abstract}" in readme
    assert "## Keywords" not in readme
    assert "`Example`" not in readme


@pytest.mark.parametrize("batch", [False, True])
def test_symlinked_master_is_rejected_without_reading_the_sentinel(monkeypatch, tmp_path, batch):
    work, resources, visible = _fixture(monkeypatch, tmp_path, readme="## Abstract\n\nOld synopsis.\n")
    sentinel = tmp_path / "private-sentinel.json"
    sentinel.write_text(json.dumps({"2026_Example": {"abstract": "Private sentinel"}}), encoding="utf-8")
    (tmp_path / "papers" / "paper_metadata.json").symlink_to(sentinel)
    visible = visible | {"papers/paper_metadata.json"}
    with pytest.raises(ValueError, match="Symlink"):
        if batch:
            bwp.enrichment_map([dict(work, _resources=resources)], visible_paths=visible)
        else:
            bwp.enrichment_for(work, resources=resources, visible_paths=visible)


def test_abridged_publisher_synopsis_is_labeled_and_links_to_its_public_source():
    publisher_url = "https://link.springer.com/chapter/10.1007/978-3-032-16955-6_11"
    rendered = bwp.abstract_source_html({
        "abstract": "Publisher synopsis.",
        "sources": {"abstract": "papers/paper_metadata.json"},
        "abstract_provenance": {
            "source": "abridged publisher synopsis", "url": publisher_url,
            "notes": "Private internal rationale", "date": "2026-10-01",
        },
    })
    assert f'href="{publisher_url}"' in rendered
    assert ">Abridged publisher synopsis</a>" in rendered
    assert "Private internal rationale" not in rendered
    assert "2026-10-01" not in rendered


def test_overview_source_uses_the_actual_file_and_encodes_a_paper_folder_prefix():
    rendered = bwp.abstract_source_html({
        "abstract": "A hand-authored abstract.",
        "sources": {"abstract": "papers/2026_Example & Result/README.md"},
        "abstract_provenance": {"source": "Internal extraction notes"},
    }, prefix="../../")
    assert 'href="../../papers/2026_Example%20%26%20Result/README.md"' in rendered
    assert ">Paper overview (README)</a>" in rendered
    assert "Internal extraction notes" not in rendered


@pytest.mark.parametrize("url", [
    "https://user:password@link.springer.com/chapter/record",
    "https://example.test/chapter/record",
    "https://link.springer.com/chapter/record?private=token",
    "http://link.springer.com/chapter/record",
    "https://[invalid",
])
def test_publisher_provenance_rejects_untrusted_links_and_falls_back_to_metadata(url):
    rendered = bwp.abstract_source_html({
        "abstract": "Publisher synopsis.",
        "sources": {"abstract": "papers/paper_metadata.json"},
        "abstract_provenance": {"source": "abridged publisher synopsis", "url": url},
    })
    assert 'href="../papers/paper_metadata.json"' in rendered
    assert ">Abridged publisher synopsis</a>" in rendered
    assert url not in rendered


def test_unknown_or_missing_abstract_source_does_not_expose_arbitrary_provenance():
    assert bwp.abstract_source_html({"abstract": "", "abstract_provenance": {"source": "abridged publisher synopsis"}}) == ""
    assert bwp.abstract_source_html({
        "abstract": "Summary.", "sources": {"abstract": "/Users/private/source.md"},
        "abstract_provenance": {"source": "Private internal rationale", "url": "file:///Users/private/source.md"},
    }) == ""
