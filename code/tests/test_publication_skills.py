from __future__ import annotations

import json
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


REPO_ROOT = Path(__file__).resolve().parents[2]

from audit_publication_skills import collect_skill_errors  # noqa: E402


def test_current_publication_skills_are_agent_operable():
    assert collect_skill_errors(REPO_ROOT) == []


def test_publication_skill_audit_reports_contract_errors(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (tmp_path / "papers" / "2026_Good").mkdir(parents=True)
    (tmp_path / "papers" / "2026_Orphan").mkdir(parents=True)
    (data_dir / "works.json").write_text(
        json.dumps(
            {
                "works": [
                    {"docs_path": "papers/2026_Good"},
                    {"docs_path": "papers/2026_Missing"},
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "papers" / "2026_Good" / "SKILL.md").write_text(
        "---\nname: Good\ndescription: bad legacy host\ntags: not-json\n---\n\n# Good\n\nNo instructions.\n"
        "https://docxology.github.io/docxology/\n",
        encoding="utf-8",
    )
    (tmp_path / "papers" / "2026_Orphan" / "SKILL.md").write_text(
        '---\nname: Orphan\ndescription: Orphan\ntags: ["orphan"]\n---\n\n## Instructions\n',
        encoding="utf-8",
    )

    errors = collect_skill_errors(tmp_path)

    assert (
        "papers/2026_Missing/SKILL.md missing for data/works.json docs_path" in errors
    )
    assert (
        "papers/2026_Orphan/SKILL.md is not referenced by data/works.json docs_path"
        in errors
    )
    assert any("legacy GitHub Pages host" in error for error in errors)
    assert any("tags must be a JSON list" in error for error in errors)
    assert any("missing ## Instructions section" in error for error in errors)


def test_publication_skill_audit_checks_only_explicit_citation_dois(tmp_path):
    folder = "papers/2026_Example"
    canonical = "10.5281/zenodo.5678"
    artifact = "10.5281/zenodo.1234"
    (tmp_path / "data").mkdir()
    (tmp_path / folder).mkdir(parents=True)
    (tmp_path / "data/works.json").write_text(
        json.dumps({"works": [{"docs_path": folder + "/", "doi": canonical}]}),
        encoding="utf-8",
    )
    skill = tmp_path / folder / "SKILL.md"
    content = (
        f'---\nname: example\ndescription: Example paper\ntags: ["example"]\n'
        f'doi: "https://doi.org/{canonical.upper()}"\n'
        f'artifact_doi: "{artifact}"\n---\n\n'
        f"## Instructions\n\n1. Ground citations in DOI `{canonical}`.\n\n"
        f"## Historical source\n\nEarlier edition: https://doi.org/{artifact}.\n"
    )
    skill.write_text(content, encoding="utf-8")
    assert collect_skill_errors(tmp_path) == []

    skill.write_text(
        content.replace(f"`{canonical}`", f"`{artifact}`"),
        encoding="utf-8",
    )
    assert collect_skill_errors(tmp_path) == [
        f"{folder}/SKILL.md: citation DOI {artifact!r} differs from data/works.json "
        f"({canonical})"
    ]

    skill.write_text(
        content.replace(canonical.upper(), artifact),
        encoding="utf-8",
    )
    assert collect_skill_errors(tmp_path) == [
        f"{folder}/SKILL.md: citation DOI {artifact!r} differs from data/works.json "
        f"({canonical})"
    ]
