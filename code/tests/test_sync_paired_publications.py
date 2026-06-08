"""Tests for paired-publication sync apply helpers."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH_DIR))

from publication_pairing import GitHubRelease, PublicationPair, ZenodoRecord  # noqa: E402
from sync_paired_publications import (  # noqa: E402
    apply_publication_pair,
    build_sync_actions,
    check_report,
    display_report_path,
    refresh_bibliography_counts,
)


def _write_minimal_repo(root: Path) -> None:
    (root / "pages").mkdir()
    (root / "papers").mkdir()
    (root / "reports").mkdir()
    (root / "pages" / "BIBLIOGRAPHY.md").write_text(
        "\n".join(
            [
                "# Bibliography",
                "",
                "**0** Papers · **0** Books",
                "",
                "| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |",
                "|--:|:----:|:------:|:----:|-------|-------|----------|:----:|",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "pages" / "SOFTWARE.md").write_text(
        "\n".join(
            [
                "# Software",
                "",
                "## 🧬 Repositories Owned by docxology",
                "",
                "| Repository | Description | Language | ⭐ | Updated |",
                "|---|---|---|:---:|---|",
                "| [new_repo](https://github.com/docxology/new_repo) | Reproducible computational research project | Python | 0 | 2026-05 |",
                "",
                "### 🏛️ Active Inference Institute",
                "",
                "| Repository | Description | Language | ⭐ | Year |",
                "|---|---|---|:---:|---|",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "papers" / "paper_metadata.json").write_text("{}\n", encoding="utf-8")
    (root / "papers" / "README.md").write_text("# Papers\n\n## Papers (0)\n", encoding="utf-8")
    (root / "papers" / "AGENTS.md").write_text(
        "# Papers\n\nREADME.md present | 0/0 folders\n", encoding="utf-8"
    )


def _pair() -> PublicationPair:
    release = GitHubRelease(
        owner="docxology",
        repo="new_repo",
        tag="v1.0.0",
        name="New Computational Project v1.0.0",
        body=(
            "DOI: https://doi.org/10.5281/zenodo.20990001\n"
            "Zenodo: https://zenodo.org/records/20990001\n"
            "PDF SHA-256: `abc123`"
        ),
        html_url="https://github.com/docxology/new_repo/releases/tag/v1.0.0",
        published_at="2026-05-27T01:02:03Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="20990001",
        doi="10.5281/zenodo.20990001",
        title="New Computational Project: Reproducible Research",
        publication_date="2026-05-27",
        version="1.0.0",
        resource_type={"type": "publication", "title": "Publication"},
        creators=[{"name": "Friedman, Daniel Ari", "orcid": "0000-0001-6232-9096"}],
        description="A reproducible computational research project with paired GitHub and Zenodo release.",
        keywords=["reproducible research", "computational"],
        related_identifiers=[
            {
                "identifier": "https://github.com/docxology/new_repo/releases/tag/v1.0.0",
                "relation": "isSupplementTo",
                "resource_type": "software",
            }
        ],
        files=[
            {
                "key": "new_computational_project.pdf",
                "size": 1234,
                "checksum": "md5:abc",
                "links": {"self": "https://zenodo.org/api/records/20990001/files/new_computational_project.pdf/content"},
            }
        ],
        html_url="https://zenodo.org/records/20990001",
    )
    return PublicationPair(
        release=release,
        record=record,
        confidence="strong",
        evidence=("github_release_mentions_doi", "zenodo_related_identifier_mentions_release"),
    )


def test_build_sync_actions_marks_new_and_existing_pairs(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    actions = build_sync_actions([pair], repo_root=tmp_path)
    assert actions[0].action_type == "create_new"

    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    actions = build_sync_actions([pair], repo_root=tmp_path)
    assert actions[0].action_type == "update_existing"


def test_display_report_path_handles_external_reports(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    assert display_report_path(repo_root / "reports" / "paired.json", repo_root=repo_root) == "reports/paired.json"
    assert display_report_path(tmp_path / "outside.json", repo_root=repo_root) == str(tmp_path / "outside.json")


def _write_report(root: Path, payload: dict) -> None:
    report = root / "reports" / "paired_publications_2026-06-07.json"
    report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _minimal_report_payload(*, warnings: list[str] | None = None, actions: list[dict] | None = None) -> dict:
    actions = actions or []
    return {
        "source": "GitHub Releases API + Zenodo Records API",
        "counts": {
            "github_releases": 1,
            "zenodo_records": 1,
            "pairs": len(actions),
            "strong_pairs": 0,
            "needs_review": sum(1 for action in actions if action.get("action_type") == "needs_review"),
            "create_new": sum(1 for action in actions if action.get("action_type") == "create_new"),
            "update_existing": sum(1 for action in actions if action.get("action_type") == "update_existing"),
        },
        "warnings": warnings or [],
        "actions": actions,
        "pairs": [],
    }


def test_check_report_rejects_api_warnings(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    _write_report(tmp_path, _minimal_report_payload(warnings=["github:docxology/example: rate limit exceeded"]))

    with pytest.raises(SystemExit, match="API warnings"):
        check_report(repo_root=tmp_path)


def test_check_report_rejects_stale_create_new_existing_doi(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    _write_report(
        tmp_path,
        _minimal_report_payload(
            actions=[
                {
                    "action_type": "create_new",
                    "doi": pair.doi,
                    "title": pair.record.title,
                }
            ]
        ),
    )

    with pytest.raises(SystemExit, match="stale create_new"):
        check_report(repo_root=tmp_path)


def test_apply_creates_new_publication_and_is_idempotent(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()

    first = apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    second = apply_publication_pair(pair, repo_root=tmp_path, download_files=False)

    folder = tmp_path / "papers" / "2026_NewComputationalProject"
    assert first.folder == "2026_NewComputationalProject"
    assert second.folder == "2026_NewComputationalProject"
    assert (folder / "README.md").is_file()
    assert (folder / "AGENTS.md").is_file()
    assert (folder / "SKILL.md").is_file()
    assert (folder / "CITATION.cff").is_file()
    assert (folder / "metadata.json").is_file()
    metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["doi"] == "10.5281/zenodo.20990001"
    assert metadata["github_release_url"] == "https://github.com/docxology/new_repo/releases/tag/v1.0.0"

    bibliography = (tmp_path / "pages" / "BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    assert bibliography.count("New Computational Project: Reproducible Research") == 1
    assert "[📁](../papers/2026_NewComputationalProject/)" in bibliography

    software = (tmp_path / "pages" / "SOFTWARE.md").read_text(encoding="utf-8")
    assert "https://doi.org/10.5281/zenodo.20990001" in software
    assert "[📄](../papers/2026_NewComputationalProject/)" in software


def test_same_title_and_release_new_doi_updates_existing_folder(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)

    updated_record = replace(
        pair.record,
        record_id="20990002",
        doi="10.5281/zenodo.20990002",
        files=[],
        html_url="https://zenodo.org/records/20990002",
    )
    updated_pair = replace(pair, record=updated_record)
    actions = build_sync_actions([updated_pair], repo_root=tmp_path)

    assert actions[0].action_type == "update_existing"
    assert actions[0].folder == "2026_NewComputationalProject"

    applied = apply_publication_pair(
        updated_pair,
        repo_root=tmp_path,
        download_files=False,
        folder=actions[0].folder,
        refresh_docs=True,
    )
    assert applied.created is False

    bibliography = (tmp_path / "pages" / "BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    assert bibliography.count("New Computational Project: Reproducible Research") == 1
    assert "10.5281/zenodo.20990002" in bibliography
    assert "10.5281/zenodo.20990001" not in bibliography


def test_same_title_and_repo_new_release_updates_existing_folder(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)

    updated_release = replace(
        pair.release,
        tag="v1.1.0",
        name="New Computational Project v1.1.0",
        html_url="https://github.com/docxology/new_repo/releases/tag/v1.1.0",
    )
    updated_record = replace(
        pair.record,
        record_id="20990003",
        doi="10.5281/zenodo.20990003",
        files=[],
        html_url="https://zenodo.org/records/20990003",
    )
    updated_pair = replace(pair, release=updated_release, record=updated_record)
    actions = build_sync_actions([updated_pair], repo_root=tmp_path)

    assert actions[0].action_type == "update_existing"
    assert actions[0].folder == "2026_NewComputationalProject"
    assert "GitHub repository" in actions[0].reason

    applied = apply_publication_pair(
        updated_pair,
        repo_root=tmp_path,
        download_files=False,
        folder=actions[0].folder,
        refresh_docs=True,
    )
    assert applied.created is False

    bibliography = (tmp_path / "pages" / "BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    assert bibliography.count("New Computational Project: Reproducible Research") == 1
    assert "10.5281/zenodo.20990003" in bibliography
    assert "10.5281/zenodo.20990001" not in bibliography


def test_refresh_bibliography_counts_keeps_series_unpluralized():
    text = "\n".join(
        [
            "**124 works** spanning peer-reviewed papers",
            "",
            "**105** Papers · **8** Presentations · **4** Books · **3** Courses · **2** Playbooks · **2** Seriesssssssss",
            "",
            "> **124** works in the table below",
            "",
            "| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |",
            "|--:|:----:|:------:|:----:|-------|-------|----------|:----:|",
            "| 1 | 2026 | 💻 | Paper | One | *Zenodo* | [10.1/x](https://doi.org/10.1/x) | — |",
            "| 2 | 2026 | 🎥 | Series | Two | *YouTube* | [link](https://example.com) | — |",
        ]
    )

    refreshed = refresh_bibliography_counts(text)

    assert "**2 works**" in refreshed
    assert "**1** Papers · **1** Series" in refreshed
    assert "Seriess" not in refreshed
