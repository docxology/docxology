"""The bibliography owns every work's title and authorship.

Regression guard for the 2026-10-01 accuracy pass. Legacy paper folders were
seeded with hand-written metadata — CamelCase placeholder titles
("ForagingGene") and, for several journal papers, co-author lists that do not
match the publication (papers/2016_ForagingGene credited five people who are
not on Ingram et al. 2016). The generated README/SKILL/CITATION.cff files
rendered that seed data instead of the registry-verified bibliography row, so
the public citation for a paper could name the wrong authors.

These tests pin the derived citation surfaces to ``pages/BIBLIOGRAPHY.md`` and
cover the helpers that keep template filler and registry name-packing out of
the published record.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import pytest  # noqa: E402

import docxology_tools  # noqa: E402,F401
import build_start_here  # noqa: E402
import fetch_work_authors  # noqa: E402
import generate_citation_cff as cff  # noqa: E402
import regenerate_docs  # noqa: E402
from docxology_tools.biblio_table import iter_bibliography_rows  # noqa: E402
from docxology_tools.metadata_templates import (  # noqa: E402
    specific_findings,
    specific_methods,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
BIBLIOGRAPHY = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"


def _rows_with_authors():
    return [row for row in iter_bibliography_rows(BIBLIOGRAPHY) if row.folder and row.authors]


def _family(name: str) -> str:
    return name.partition(",")[0].strip() if "," in name else name.strip()


# ── Repository invariants ───────────────────────────────────────────────────


def test_paper_citation_cff_matches_bibliography_title_and_authors():
    drift = []
    for row in _rows_with_authors():
        path = REPO_ROOT / "papers" / row.folder / "CITATION.cff"
        if not path.is_file():
            continue
        identity = cff._cff_citation_identity(path.read_text(encoding="utf-8"))
        expected = cff._bibliography_identity({"title": row.title.strip(), "authors": list(row.authors)})
        if identity != expected:
            drift.append(row.folder)
    assert not drift, f"CITATION.cff title/authors drifted from the bibliography: {drift[:10]}"


def test_paper_readme_byline_and_heading_follow_bibliography():
    drift = []
    for row in _rows_with_authors():
        path = REPO_ROOT / "papers" / row.folder / "README.md"
        text = path.read_text(encoding="utf-8")
        if not regenerate_docs.is_generated_document("README.md", text):
            continue  # hand-authored README: not owned by the generator
        byline = re.search(r"^\*\*(.+?)\*\* \(\d{4}\)", text, re.MULTILINE)
        heading = re.search(r"^# \S+ (.+)$", text, re.MULTILINE)
        expected_authors = ", ".join(regenerate_docs.display_author_name(a) for a in row.authors)
        if not byline or byline.group(1) != expected_authors:
            drift.append(f"{row.folder}: byline")
        if not heading or heading.group(1) != regenerate_docs.clean_markdown_text(row.title):
            drift.append(f"{row.folder}: heading")
    assert not drift, f"paper README drifted from the bibliography: {drift[:10]}"


def test_generated_paper_docs_never_present_template_methods():
    offenders = []
    for path in sorted((REPO_ROOT / "papers").glob("*/README.md")):
        text = path.read_text(encoding="utf-8")
        if not regenerate_docs.is_generated_document("README.md", text):
            continue
        section = text.split("## Methods", 1)[-1].split("## Key Findings", 1)[0]
        bullets = [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]
        if any(not specific_methods([bullet]) for bullet in bullets):
            offenders.append(path.parent.name)
    assert not offenders, f"template methods rendered as paper methods: {offenders[:10]}"


def test_bibliography_authors_are_inverted_person_names_for_the_owner():
    """The owner's name must never ship uninverted (CSL would emit a literal)."""
    bad = []
    for row in iter_bibliography_rows(BIBLIOGRAPHY):
        for name in row.authors:
            if "Friedman" in name and not _family(name) == "Friedman":
                bad.append((row.num, name))
    assert not bad, f"owner name not in 'Friedman, Given' form: {bad[:10]}"


# ── Helper behaviour ────────────────────────────────────────────────────────


def test_specific_methods_drops_domain_templates_and_keeps_curated_methods():
    methods = [
        {"name": "Field observation and behavioral assays", "description": "Applied ..."},
        {"name": "Quantitative PCR of the foraging gene"},
        "Deterministic software pipeline design",
    ]
    assert specific_methods(methods) == ["Quantitative PCR of the foraging gene"]
    assert specific_methods(None) == []


def test_specific_findings_drops_placeholders_and_abstract_echoes():
    abstract = "Elegant laboratory studies have pioneered this effort, but field studies are rare. We find X."
    findings = [
        "See full paper for detailed findings and analysis",
        "Elegant laboratory studies have pioneered this effort, but field stu....",
        "Foraging expression rises with light exposure in brood workers.",
    ]
    assert specific_findings(findings, abstract) == [
        "Foraging expression rises with light exposure in brood workers."
    ]


@pytest.mark.parametrize(
    ("author", "expected"),
    [
        ({"family": "Daniel Ari Friedman", "given": "", "orcid": "0000-0001-6232-9096"}, "Friedman, Daniel Ari"),
        ({"family": "Andrew Pashea", "given": "", "orcid": "0009-0004-4061-6296"}, "Pashea, Andrew"),
        # No ORCID: the string may be a pseudonym or collective — never split.
        ({"family": "Die Schwarze Katze", "given": ""}, "Die Schwarze Katze"),
        ({"family": "John Clippinger", "given": ""}, "John Clippinger"),
        # Multi-word family names with a given name are left intact.
        ({"family": "St. Clere Smithe", "given": "Toby", "orcid": "x"}, "St. Clere Smithe, Toby"),
        ({"literal": "Active Inference Institute"}, "Active Inference Institute"),
        # Explicit owner-name correction for a mis-split Crossref deposit.
        ({"family": "Ari Friedman", "given": "Daniel"}, "Friedman, Daniel Ari"),
    ],
)
def test_format_author_undoes_registry_name_packing_only_when_safe(author, expected):
    assert fetch_work_authors.format_author(author) == expected


def test_display_author_name_inverts_family_given():
    assert regenerate_docs.display_author_name("Ingram, Krista K.") == "Krista K. Ingram"
    assert regenerate_docs.display_author_name("John Clippinger") == "John Clippinger"


def test_cff_reconcile_is_byte_stable_when_identity_matches():
    text = (
        'cff-version: 1.2.0\ntitle: Example Title\nauthors:\n'
        '  - family-names: Friedman\n    given-names: Daniel A.\n    orcid: "x"\nidentifiers:\n  - type: doi\n'
    )
    citation = {"title": "Example Title", "authors": ["Friedman, Daniel A."]}
    assert cff.reconcile_cff_bibliography(text, citation) == text


def test_cff_reconcile_replaces_wrong_title_and_authors():
    text = (
        'cff-version: 1.2.0\ntitle: "ForagingGene"\nauthors:\n'
        '  - family-names: Pilko\n    given-names: Anna\nidentifiers:\n  - type: doi\n'
    )
    citation = {"title": "Context-dependent expression", "authors": ["Ingram, Krista K.", "Friedman, Daniel A.", "Collective"]}
    out = cff.reconcile_cff_bibliography(text, citation)
    assert 'title: "Context-dependent expression"' in out
    assert "Pilko" not in out
    assert '  - family-names: "Ingram"\n    given-names: "Krista K."\n' in out
    assert f'    orcid: "{cff.ORCID}"' in out  # only on the Friedman entry
    assert out.count("orcid:") == 1
    assert '  - name: "Collective"\n' in out
    assert out.endswith("identifiers:\n  - type: doi\n")


def test_start_here_sync_counts_is_idempotent(tmp_path, monkeypatch):
    page = tmp_path / "start-here.html"
    page.write_text((REPO_ROOT / "start-here.html").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(build_start_here, "PAGE", page)
    build_start_here.sync_counts()
    first = page.read_text(encoding="utf-8")
    assert build_start_here.sync_counts() is False
    assert page.read_text(encoding="utf-8") == first
    assert build_start_here.check_counts(first) == []
