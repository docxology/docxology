from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH_DIR))

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
        "---\nname: Orphan\ndescription: Orphan\ntags: [\"orphan\"]\n---\n\n## Instructions\n",
        encoding="utf-8",
    )

    errors = collect_skill_errors(tmp_path)

    assert "papers/2026_Missing/SKILL.md missing for data/works.json docs_path" in errors
    assert "papers/2026_Orphan/SKILL.md is not referenced by data/works.json docs_path" in errors
    assert any("legacy GitHub Pages host" in error for error in errors)
    assert any("tags must be a JSON list" in error for error in errors)
    assert any("missing ## Instructions section" in error for error in errors)

