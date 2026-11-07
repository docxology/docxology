"""Tests for paired-publication sync apply helpers."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from unittest import mock

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402
from docxology_tools.publication_pairing import (  # noqa: E402
    GitHubRelease,
    PublicationPair,
    ZenodoRecord,
    find_publication_pairs,
    generated_timestamp,
)
import sync_paired_publications  # noqa: E402
from sync_paired_publications import (  # noqa: E402
    attest_applied_publication,
    apply_publication_pair,
    build_sync_actions,
    check_report,
    classification_cache_from_payload,
    classification_cache_payload,
    classification_inputs,
    display_report_path,
    github_releases_from_payload,
    load_cached_scan_payload,
    ordered_apply_pairs,
    refresh_bibliography_counts,
    reviewed_pair_decisions,
    write_report,
    zenodo_records_from_payload,
)


def _write_minimal_repo(root: Path) -> None:
    (root / "pages").mkdir()
    (root / "papers").mkdir()
    (root / "reports").mkdir()
    (root / "data").mkdir()
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
    (root / "data/work-identifiers.json").write_text(
        '{"schema_version": "WorkIdentifierRegistry.v1", "identifiers": {}}\n',
        encoding="utf-8",
    )
    (root / "papers" / "README.md").write_text(
        "# Papers\n\n## Papers (0)\n", encoding="utf-8"
    )
    (root / "papers" / "AGENTS.md").write_text(
        "# Papers\n\nREADME.md present | 0/0 folders\n", encoding="utf-8"
    )


def _write_review_decision(
    root: Path,
    pair: PublicationPair,
    *,
    folder: str = "2026_NewComputationalProject",
    edition_bound: bool = True,
) -> None:
    payload = {
        "generated_at": "2026-06-18T00:00:00Z",
        "source_report": "reports/paired_publications_2026-06-18.json",
        "source_review_queue": "",
        "decision_summary": {
            "decision": "accept",
            "groups": 1,
            "raw_candidates": 1,
            "note": "test decision",
        },
        "groups": [
            {
                "id": "R01",
                "decision": "superseded",
                "decided_at": "2026-06-18T00:00:00Z",
                "decided_by": "codex",
                "doi": pair.doi,
                "title": pair.record.title,
                "candidate_github_repo": pair.github_repo,
                "folder": folder,
                "representation": "version-history",
                "raw_candidate_count": 1,
                "raw_candidates": [
                    {
                        "doi": pair.doi,
                        "record_title": pair.record.title,
                        "zenodo_record_url": pair.zenodo_record_url,
                        "github_repo": pair.github_repo,
                        "github_release_url": pair.github_release_url,
                        "release_tag": pair.release.tag,
                        "release_name": pair.release.name,
                        "resource_type": pair.record.resource_type,
                        "raw_confidence": pair.confidence,
                        "evidence": list(pair.evidence),
                        "review_decision": "superseded",
                        "reviewed_at": "2026-06-18T00:00:00Z",
                        "review_source": "test",
                        "source_report": "reports/paired_publications_2026-06-18.json",
                    }
                ],
            }
        ],
    }
    if edition_bound:
        proof = _inline_edition_evidence(pair)
        payload["groups"][0]["edition_evidence"] = proof
        payload["groups"][0]["raw_candidates"][0]["edition_evidence"] = proof
    (root / "data" / "paired-publication-decisions.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
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
                "links": {
                    "self": "https://zenodo.org/api/records/20990001/files/new_computational_project.pdf/content"
                },
            }
        ],
        html_url="https://zenodo.org/records/20990001",
    )
    return PublicationPair(
        release=release,
        record=record,
        confidence="strong",
        evidence=(
            "github_release_mentions_doi",
            "zenodo_related_identifier_mentions_release",
        ),
    )


def test_build_sync_actions_marks_new_and_existing_pairs(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    actions = build_sync_actions([pair], repo_root=tmp_path)
    assert actions[0].action_type == "create_new"

    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    actions = build_sync_actions([pair], repo_root=tmp_path)
    assert actions[0].action_type == "update_existing"


def test_applied_strong_update_report_binds_exact_action_and_metadata(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    action = build_sync_actions([pair], repo_root=tmp_path)[0]
    applied = apply_publication_pair(
        pair,
        repo_root=tmp_path,
        download_files=False,
        folder=action.folder,
    )
    attested = attest_applied_publication(applied, action, repo_root=tmp_path)
    report_path = tmp_path / "reports" / "paired_publications_2026-08-25.json"

    write_report(
        report_path,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[action],
        warnings=[],
        applied=[attested],
    )

    receipt = json.loads(report_path.read_text(encoding="utf-8"))["applied"][0]
    assert receipt["action"] == action.to_dict()
    assert receipt["provenance"]["metadata_path"] == (
        "papers/2026_NewComputationalProject/metadata.json"
    )
    assert receipt["provenance"]["approval"]["decision"] == "approved"
    assert (
        receipt["provenance"]["approval"]["action_sha256"]
        == receipt["provenance"]["action_sha256"]
    )
    check_report(repo_root=tmp_path)

    receipt["provenance"]["approval"]["action_sha256"] = "0" * 64
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    payload["applied"][0] = receipt
    report_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="unverifiable applied strong update receipt"):
        check_report(repo_root=tmp_path)


def test_ordered_apply_pairs_leaves_latest_release_as_final_metadata_writer(
    tmp_path: Path,
):
    _write_minimal_repo(tmp_path)
    base = _pair()
    apply_publication_pair(base, repo_root=tmp_path, download_files=False)
    older = replace(
        base,
        release=replace(
            base.release,
            tag="v1.0.0",
            published_at="2026-05-27T01:02:03Z",
            html_url="https://github.com/docxology/new_repo/releases/tag/v1.0.0",
        ),
    )
    newer = replace(
        base,
        release=replace(
            base.release,
            tag="v1.1.0",
            published_at="2026-06-01T01:02:03Z",
            html_url="https://github.com/docxology/new_repo/releases/tag/v1.1.0",
        ),
    )
    pairs = [newer, older]
    actions = build_sync_actions(pairs, repo_root=tmp_path)

    ordered = ordered_apply_pairs(actions, pairs)

    assert [pair.release.tag for _, pair in ordered] == ["v1.0.0", "v1.1.0"]


def test_build_sync_actions_honors_reviewed_noncanonical_versions(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)

    actions = build_sync_actions([pair], repo_root=tmp_path)

    assert actions[0].action_type == "already_reviewed"
    assert actions[0].folder == "2026_NewComputationalProject"
    assert "do not create a duplicate bibliography row" in actions[0].reason


def test_reviewed_decision_takes_precedence_over_existing_doi(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    _write_review_decision(tmp_path, pair)

    actions = build_sync_actions([pair], repo_root=tmp_path)

    assert actions[0].action_type == "already_reviewed"


def test_reviewed_decision_accepts_string_raw_candidates(tmp_path: Path):
    """String-form raw_candidates (release-URL strings) must still register.

    Regression: decisions that stored raw_candidates as bare URL strings were
    silently dropped, re-surfacing create_new actions for already-decided pairs
    (e.g. CogSecSkills 10.5281/zenodo.20804585)."""
    _write_minimal_repo(tmp_path)
    pair = _pair()
    payload = {
        "generated_at": "2026-08-10T00:00:00Z",
        "decision_summary": {
            "decision": "rejected",
            "groups": 1,
            "raw_candidates": 1,
            "note": "test",
        },
        "groups": [
            {
                "id": "R25",
                "edition_evidence": _inline_edition_evidence(pair),
                "decision": "rejected",
                "decided_at": "2026-08-10T00:00:00Z",
                "decided_by": "maintainer",
                "doi": pair.doi,
                "title": pair.record.title,
                "representation": "superseded-version false positive",
                "folder": None,
                "raw_candidate_count": 1,
                "raw_candidates": [pair.github_release_url],
            }
        ],
    }
    (tmp_path / "data" / "paired-publication-decisions.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    actions = build_sync_actions([pair], repo_root=tmp_path)

    assert actions[0].action_type == "already_reviewed"
    assert "do not create a duplicate bibliography row" in actions[0].reason


def test_reviewed_decision_does_not_survive_changed_zenodo_or_title(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    decisions_path = tmp_path / "data" / "paired-publication-decisions.json"
    original = json.loads(decisions_path.read_text(encoding="utf-8"))

    for field, changed_value in (
        ("zenodo_record_url", "https://zenodo.org/records/20990002"),
        ("record_title", "New Computational Project: changed evidence"),
    ):
        mutated = json.loads(json.dumps(original))
        mutated["groups"][0]["raw_candidates"][0][field] = changed_value
        decisions_path.write_text(
            json.dumps(mutated, indent=2) + "\n", encoding="utf-8"
        )

        actions = build_sync_actions([pair], repo_root=tmp_path)

        assert actions[0].action_type == "create_new"


def test_malformed_and_conflicting_pair_decisions_cannot_clear_sync_candidates(
    tmp_path: Path,
):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    decisions_path = tmp_path / "data" / "paired-publication-decisions.json"
    malformed = json.loads(decisions_path.read_text(encoding="utf-8"))
    del malformed["groups"][0]["decided_by"]
    decisions_path.write_text(json.dumps(malformed, indent=2) + "\n", encoding="utf-8")

    # Missing human provenance leaves the candidate live; it cannot silently
    # become already reviewed merely because its raw candidate is present.
    assert build_sync_actions([pair], repo_root=tmp_path)[0].action_type == "create_new"

    valid = json.loads(json.dumps(malformed))
    first = valid["groups"][0]
    first["decided_by"] = "codex"
    duplicate = json.loads(json.dumps(valid))
    duplicate_group = json.loads(json.dumps(first))
    duplicate_group.update(
        {
            "id": "R02",
            "decided_by": "second reviewer",
            "decided_at": "2026-06-18T00:30:00Z",
        }
    )
    duplicate["groups"].append(duplicate_group)
    decisions_path.write_text(json.dumps(duplicate, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate paired-publication decisions"):
        build_sync_actions([pair], repo_root=tmp_path)

    conflicting = json.loads(json.dumps(first))
    conflicting.update(
        {
            "id": "R02",
            "decision": "rejected",
            "decided_by": "reviewer",
            "decided_at": "2026-06-18T00:30:00Z",
        }
    )
    valid["groups"].append(conflicting)
    decisions_path.write_text(json.dumps(valid, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate paired-publication decisions"):
        build_sync_actions([pair], repo_root=tmp_path)


def test_authenticated_pair_decision_supersession_is_exact_and_auditable(
    tmp_path: Path,
):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    decisions_path = tmp_path / "data" / "paired-publication-decisions.json"
    payload = json.loads(decisions_path.read_text(encoding="utf-8"))
    first = payload["groups"][0]
    replacement = json.loads(json.dumps(first))
    replacement.update(
        {
            "id": "R02",
            "decision": "rejected",
            "decided_by": "reviewer",
            "decided_at": "2026-06-18T00:30:00Z",
            "supersession": {
                "supersedes_group_id": "R01",
                "authenticated": True,
                "approved_by": "reviewer",
                "approved_at": "2026-06-18T00:30:00Z",
                "rationale": "The newer signed review reverses the original outcome.",
                "superseded_candidate": {
                    "doi": pair.doi,
                    "github_release_url": pair.github_release_url,
                    "zenodo_record_url": pair.zenodo_record_url,
                    "github_repo": pair.github_repo,
                    "title": pair.record.title,
                    "release_tag": pair.release.tag,
                },
            },
        }
    )
    payload["groups"].append(replacement)
    decisions_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    decisions = reviewed_pair_decisions(tmp_path)
    assert len(decisions) == 1
    record = next(iter(decisions.values()))
    assert record["decision"] == "rejected"
    assert record["group_id"] == "R02"
    assert (
        build_sync_actions([pair], repo_root=tmp_path)[0].action_type
        == "already_reviewed"
    )


def test_display_report_path_handles_external_reports(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    assert (
        display_report_path(repo_root / "reports" / "paired.json", repo_root=repo_root)
        == "reports/paired.json"
    )
    assert display_report_path(tmp_path / "outside.json", repo_root=repo_root) == str(
        tmp_path / "outside.json"
    )


def _write_report(root: Path, payload: dict) -> None:
    report = root / "reports" / "paired_publications_2026-06-07.json"
    report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _minimal_report_payload(
    *, warnings: list[str] | None = None, actions: list[dict] | None = None
) -> dict:
    actions = actions or []
    return {
        "source": "GitHub Releases API + Zenodo Records API",
        "counts": {
            "github_releases": 1,
            "zenodo_records": 1,
            "pairs": len(actions),
            "strong_pairs": 0,
            "needs_review": sum(
                1 for action in actions if action.get("action_type") == "needs_review"
            ),
            "create_new": sum(
                1 for action in actions if action.get("action_type") == "create_new"
            ),
            "update_existing": sum(
                1
                for action in actions
                if action.get("action_type") == "update_existing"
            ),
        },
        "warnings": warnings or [],
        "actions": actions,
        "pairs": [],
    }


def test_check_report_rejects_api_warnings(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    _write_report(
        tmp_path,
        _minimal_report_payload(
            warnings=["github:docxology/example: rate limit exceeded"]
        ),
    )

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


def test_check_report_accepts_applied_create_new_existing_doi(tmp_path: Path):
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
        )
        | {
            "applied": [
                {
                    "doi": pair.doi,
                    "folder": "2026_NewComputationalProject",
                    "created": True,
                }
            ]
        },
    )

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
    assert (
        metadata["github_release_url"]
        == "https://github.com/docxology/new_repo/releases/tag/v1.0.0"
    )

    bibliography = (tmp_path / "pages" / "BIBLIOGRAPHY.md").read_text(encoding="utf-8")
    assert bibliography.count("New Computational Project: Reproducible Research") == 1
    assert "[📁](../papers/2026_NewComputationalProject/)" in bibliography
    registry = json.loads(
        (tmp_path / "data/work-identifiers.json").read_text(encoding="utf-8")
    )
    assert registry["identifiers"]["1"] == {
        "citation_key": "Friedman2026NewComputationalProjectReproducible001",
        "status": "active",
    }

    software = (tmp_path / "pages" / "SOFTWARE.md").read_text(encoding="utf-8")
    assert "https://doi.org/10.5281/zenodo.20990001" in software
    assert "[📄](../papers/2026_NewComputationalProject/)" in software


def test_paired_intake_rejects_unsafe_key_before_bibliography_write(tmp_path):
    from docxology_tools.work_identifiers import WorkIdentifierError

    _write_minimal_repo(tmp_path)
    pair = _pair()
    pair = replace(pair, record=replace(pair.record, title="A" * 220))
    bibliography = tmp_path / "pages/BIBLIOGRAPHY.md"
    registry = tmp_path / "data/work-identifiers.json"
    before = (bibliography.read_bytes(), registry.read_bytes())
    with pytest.raises(WorkIdentifierError, match="unsafe citation key"):
        sync_paired_publications.ensure_bibliography_row(
            pair, "2026_Example", [], tmp_path
        )
    assert (bibliography.read_bytes(), registry.read_bytes()) == before


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


def test_refresh_bibliography_counts_updates_indexed_paper_folders():
    # Two rows have ../papers/ folder links, one (a Series) does not.
    text = "\n".join(
        [
            "**1 works** spanning papers",
            "",
            "> **1** works in the table below **·** **1** indexed paper folders in [papers/](../papers/) **·** more",
            "",
            "| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |",
            "|--:|:----:|:------:|:----:|-------|-------|----------|:----:|",
            "| 1 | 2026 | 💻 | Paper | One | *Zenodo* | [10.1/x](https://doi.org/10.1/x) | [📁](../papers/2026_One/) |",
            "| 2 | 2026 | 🧠 | Paper | Two | *Zenodo* | [10.1/y](https://doi.org/10.1/y) | [📁](../papers/2026_Two/) |",
            "| 3 | 2026 | 🎥 | Series | Three | *YouTube* | [link](https://example.com) | — |",
        ]
    )

    refreshed = refresh_bibliography_counts(text)

    # 3 works total, but only 2 carry per-paper folders.
    assert "**3 works**" in refreshed
    assert "**2** indexed paper folders" in refreshed
    assert "**1** indexed paper folders" not in refreshed


def _variant_pair(
    pair: PublicationPair, *, doi: str, record_id: str, tag: str
) -> PublicationPair:
    release = replace(
        pair.release,
        tag=tag,
        html_url=f"https://github.com/{pair.release.owner}/{pair.release.repo}/releases/tag/{tag}",
    )
    record = replace(pair.record, doi=doi, record_id=record_id)
    return PublicationPair(
        release=release,
        record=record,
        confidence="strong",
        evidence=("github_release_mentions_doi",),
    )


def test_apply_mode_no_longer_runs_inline_regeneration():
    """Apply writes curated source only; the former 13-generator chain is regenerate_all's job."""
    assert not hasattr(sync_paired_publications, "run_regeneration")


def test_former_apply_regeneration_chain_is_covered_by_the_generation_plan():
    """Every generator apply used to run inline is a first-class LOCAL_GENERATION_STEPS entry."""
    scripts = {step.script for step in LOCAL_GENERATION_STEPS}
    former_inline_chain = (
        "sync_publications_html.py",
        "export_bibliography.py",
        "sync_software_html.py",
        "export_agent_data.py",
        "build_domain_pages.py",
        "build_work_pages.py",
        "build_paper_pages.py",
        "audit_assets.py",
        "build_catalog.py",
        "build_search_index.py",
        "generate_feed.py",
        "build_sitemap.py",
        "build_generated_manifest.py",
    )
    missing = [script for script in former_inline_chain if script not in scripts]
    assert missing == []


def test_classification_cache_reproduces_full_scan_classification(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    reviewed = _pair()
    _write_review_decision(tmp_path, reviewed)
    fresh = _variant_pair(
        reviewed, doi="10.5281/zenodo.20990002", record_id="20990002", tag="v2.0.0"
    )
    pairs = [reviewed, fresh]
    full = build_sync_actions(pairs, repo_root=tmp_path)
    entries: list = []
    build_sync_actions(pairs, repo_root=tmp_path, already_reviewed_entries=entries)
    cache = classification_cache_from_payload(
        {
            "classification_cache": classification_cache_payload(
                entries, repo_root=tmp_path
            )
        }
    )
    assert cache is not None
    cached = build_sync_actions(pairs, repo_root=tmp_path, cache=cache)
    assert [action.to_dict() for action in cached] == [
        action.to_dict() for action in full
    ]
    assert [action.action_type for action in cached] == [
        "already_reviewed",
        "create_new",
    ]


def test_classification_cache_hit_verifies_ledger_and_skips_title_scans(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache = classification_cache_from_payload(
        {
            "classification_cache": classification_cache_payload(
                entries, repo_root=tmp_path
            )
        }
    )

    def _explode(root):  # pragma: no cover - must never run on a full cache hit
        raise AssertionError("cached inputs must not be re-derived on a cache hit")

    with (
        mock.patch.object(
            sync_paired_publications,
            "reviewed_pair_decisions",
            wraps=reviewed_pair_decisions,
        ) as durable,
        mock.patch.object(
            sync_paired_publications, "existing_release_title_map", _explode
        ),
        mock.patch.object(
            sync_paired_publications, "existing_repo_title_map", _explode
        ),
    ):
        actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type == "already_reviewed"
    assert actions[0].folder == "2026_NewComputationalProject"
    durable.assert_called_once_with(tmp_path)


def test_classification_cache_falls_back_to_full_scan_when_decisions_drift(
    tmp_path: Path,
):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache_block = classification_cache_payload(entries, repo_root=tmp_path)
    # The durable decision is withdrawn after the report was written.
    (tmp_path / "data" / "paired-publication-decisions.json").write_text(
        '{"groups": []}\n', encoding="utf-8"
    )
    cache = classification_cache_from_payload({"classification_cache": cache_block})
    actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert [action.to_dict() for action in actions] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]
    assert actions[0].action_type == "create_new"


def test_classification_cache_falls_back_to_full_scan_when_bibliography_drifts(
    tmp_path: Path,
):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache_block = classification_cache_payload(entries, repo_root=tmp_path)
    bibliography = tmp_path / "pages" / "BIBLIOGRAPHY.md"
    bibliography.write_text(
        bibliography.read_text(encoding="utf-8") + "drift\n", encoding="utf-8"
    )
    cache = classification_cache_from_payload({"classification_cache": cache_block})
    calls = {"count": 0}
    real = sync_paired_publications.reviewed_pair_decisions

    def counting(root):
        calls["count"] += 1
        return real(root)

    with mock.patch.object(
        sync_paired_publications, "reviewed_pair_decisions", counting
    ):
        actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert (
        calls["count"] >= 1
    )  # drift forced the full classification, not the cached one
    assert [action.to_dict() for action in actions] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]


def test_check_report_fails_on_malformed_classification_cache(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = {
        "inputs": {"bibliography_sha256": "short"},
        "already_reviewed": "nope",
    }
    _write_report(tmp_path, payload)
    with pytest.raises(SystemExit, match="malformed classification_cache"):
        check_report(repo_root=tmp_path)


def test_check_report_warns_on_classification_cache_input_drift(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = classification_cache_payload(
        [], repo_root=tmp_path
    )
    bibliography = tmp_path / "pages" / "BIBLIOGRAPHY.md"
    bibliography.write_text(
        bibliography.read_text(encoding="utf-8") + "drift\n", encoding="utf-8"
    )
    _write_report(tmp_path, payload)
    check_report(
        repo_root=tmp_path
    )  # a dated report stays valid; drift is surfaced, not fatal
    assert "classification_cache inputs have drifted" in capsys.readouterr().err


def test_check_report_accepts_current_classification_cache(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = classification_cache_payload(
        [], repo_root=tmp_path
    )
    _write_report(tmp_path, payload)
    check_report(repo_root=tmp_path)
    assert "drifted" not in capsys.readouterr().err


def test_report_payload_roundtrips_releases_records_and_cache(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    entries: list = []
    actions = build_sync_actions(
        [pair], repo_root=tmp_path, already_reviewed_entries=entries
    )
    report = tmp_path / "reports" / "paired_publications_2026-06-07.json"
    write_report(
        report,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=actions,
        warnings=[],
        classification_cache=classification_cache_payload(entries, repo_root=tmp_path),
    )
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert github_releases_from_payload(payload) == [pair.release]
    assert zenodo_records_from_payload(payload) == [pair.record]
    cache = classification_cache_from_payload(payload)
    assert cache is not None
    assert cache.inputs == classification_inputs(tmp_path)


@pytest.mark.parametrize("prefix", ["", "source:", "file:"])
@pytest.mark.parametrize(
    "local_path",
    [
        "/Users/example/private/release",
        "/home/example/private/release",
        "/Volumes/Work/release",
        r"C:\Users\example\release",
    ],
)
def test_public_report_redacts_release_paths_and_rejects_reintroduced_paths(
    tmp_path, local_path, prefix
):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    body = f"Built at `{prefix}{local_path}`. Source: https://example.org/docs:/Users/example/release"
    pair = replace(pair, release=replace(pair.release, body=body))
    report = tmp_path / "reports/paired_publications_2026-06-07.json"
    write_report(
        report,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[],
        warnings=[],
    )
    payload = json.loads(report.read_text())
    for release in (payload["github_releases"][0], payload["pairs"][0]["release"]):
        assert release["body"] == body.replace(local_path, "[local path redacted]")
        assert release["body_redaction"] == {
            "policy": "local-filesystem-paths-v1",
            "source_sha256": hashlib.sha256(body.encode()).hexdigest(),
        }
    assert pair.release.body == body
    rebuilt = github_releases_from_payload(payload)[0]
    assert rebuilt.to_dict() == payload["github_releases"][0]
    check_report(repo_root=tmp_path)
    payload["pairs"][0]["release"]["body"] += " " + prefix + local_path
    report.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(SystemExit, match="local filesystem path"):
        check_report(repo_root=tmp_path)


def test_redaction_cli_preserves_observation_and_apply_receipts_and_is_idempotent(
    tmp_path,
):
    payload = _minimal_report_payload()
    payload["generated_at"] = "2026-01-01T00:00:00Z"
    payload["github_releases"] = [
        {"body": "Built at `source:/Volumes/Example/private/release`."}
    ]
    payload["applied"] = [
        {"doi": "10.5281/zenodo.1234567", "provenance": {"action_sha256": "a" * 64}}
    ]
    report = tmp_path / "paired.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    command = [
        sys.executable,
        str(Path(sync_paired_publications.__file__).resolve()),
        "--redact-local-paths",
        "--report",
        str(report),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    assert result.stdout.startswith("redacted ")
    projected = json.loads(report.read_text())
    assert projected["generated_at"] == payload["generated_at"]
    assert projected["applied"] == payload["applied"]
    assert projected["counts"] == payload["counts"]
    first = report.read_bytes()
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    assert result.stdout.startswith("already safe ")
    assert report.read_bytes() == first
    result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
    assert result.returncode == 2
    assert "cannot combine" in result.stderr
    assert report.read_bytes() == first


def test_cached_body_cleanup_preserves_original_provenance_and_is_idempotent(tmp_path):
    _write_minimal_repo(tmp_path)
    original_body = (
        "First `/Users/example/private.txt`; "
        "second `source:/Volumes/Example/private.txt`. "
        "Public: https://example.org/docs:/Users/example/public.txt"
    )
    cached_body = original_body.replace(
        "/Users/example/private.txt", "[local path redacted]"
    )
    provenance = {
        "policy": "local-filesystem-paths-v1",
        "source_sha256": hashlib.sha256(original_body.encode()).hexdigest(),
    }
    pair = _pair()
    pair = replace(
        pair,
        release=replace(
            pair.release, body=cached_body, body_redaction=dict(provenance)
        ),
    )
    report = tmp_path / "reports/paired_publications_2026-06-07.json"
    write_report(
        report,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[],
        warnings=[],
    )
    payload = json.loads(report.read_text())
    expected_body = cached_body.replace(
        "/Volumes/Example/private.txt", "[local path redacted]"
    )
    for release in (payload["github_releases"][0], payload["pairs"][0]["release"]):
        assert release["body"] == expected_body
        assert release["body_redaction"] == provenance
    assert pair.release.body == cached_body
    assert pair.release.body_redaction == provenance
    rebuilt = github_releases_from_payload(payload)[0]
    assert rebuilt.to_dict() == payload["github_releases"][0]
    assert sync_paired_publications.redact_report_release_bodies(payload) == payload
    first = report.read_bytes()
    assert not sync_paired_publications.redact_report_local_paths(report)
    assert report.read_bytes() == first
    check_report(repo_root=tmp_path)


@pytest.mark.parametrize(
    "provenance",
    [
        {"policy": "unknown", "source_sha256": "a" * 64},
        {"policy": "local-filesystem-paths-v1", "source_sha256": "invalid"},
        {
            "policy": "local-filesystem-paths-v1",
            "source_sha256": "a" * 64,
            "extra": True,
        },
    ],
)
def test_cached_replay_rejects_invalid_existing_redaction_provenance(provenance):
    release = _pair().release.to_dict()
    release["body_redaction"] = provenance
    with pytest.raises(
        ValueError, match="Invalid cached release body redaction provenance"
    ):
        github_releases_from_payload({"github_releases": [release]})


@pytest.mark.parametrize(
    "provenance",
    [
        {"policy": "unknown", "source_sha256": "a" * 64},
        {"policy": "local-filesystem-paths-v1", "source_sha256": "invalid"},
        {
            "policy": "local-filesystem-paths-v1",
            "source_sha256": "a" * 64,
            "extra": True,
        },
    ],
)
def test_direct_cleanup_rejects_invalid_redaction_provenance_without_rewriting(
    tmp_path, provenance
):
    payload = _minimal_report_payload()
    payload["github_releases"] = [
        {
            "body": "source:/Users/example/private.txt",
            "body_redaction": provenance,
        }
    ]
    report = tmp_path / "paired.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    original = report.read_bytes()
    with pytest.raises(
        ValueError, match="Invalid cached release body redaction provenance"
    ):
        sync_paired_publications.redact_report_local_paths(report)
    assert report.read_bytes() == original


def test_load_cached_scan_payload_matches_fresh_classification(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    report = tmp_path / "reports" / "paired_publications_2026-06-07.json"
    write_report(
        report,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[],
        warnings=[],
    )
    releases, records = load_cached_scan_payload(report)
    assert (releases, records) == ([pair.release], [pair.record])
    rebuilt = build_sync_actions(
        find_publication_pairs(releases, records), repo_root=tmp_path
    )
    assert [action.to_dict() for action in rebuilt] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]


def _pairing_payload(
    releases: list[GitHubRelease],
    records: list[ZenodoRecord],
    *,
    generated_at: str | None = None,
    warnings: list[str] | None = None,
) -> dict:
    return {
        "source": "GitHub Releases API + Zenodo Records API",
        "generated_at": generated_at or generated_timestamp(),
        "warnings": warnings or [],
        "github_releases": [release.to_dict() for release in releases],
        "zenodo_records": [record.to_dict() for record in records],
    }


def test_load_cached_scan_payload_refuses_stale_report_unless_forced(tmp_path: Path):
    pair = _pair()
    path = tmp_path / "paired_publications_stale.json"
    path.write_text(
        json.dumps(
            _pairing_payload(
                [pair.release], [pair.record], generated_at="2020-01-01T00:00:00Z"
            )
        ),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="not same-day"):
        load_cached_scan_payload(path)
    releases, records = load_cached_scan_payload(path, force=True)
    assert (releases, records) == ([pair.release], [pair.record])


def test_load_cached_scan_payload_refuses_warned_scan_even_when_forced(tmp_path: Path):
    pair = _pair()
    path = tmp_path / "paired_publications_warned.json"
    path.write_text(
        json.dumps(
            _pairing_payload(
                [pair.release], [pair.record], warnings=["github: rate limited"]
            )
        ),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="API warning"):
        load_cached_scan_payload(path, force=True)


def test_load_cached_scan_payload_refuses_payload_without_records(tmp_path: Path):
    path = tmp_path / "paired_publications_legacy.json"
    path.write_text(
        json.dumps(
            {
                "source": "GitHub Releases API + Zenodo Records API",
                "generated_at": generated_timestamp(),
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="github_releases"):
        load_cached_scan_payload(path)


@pytest.mark.parametrize("resource_type", [{"type": "software"}, {"id": "software"}])
def test_catalogued_software_supplement_is_not_applied_as_new_work(
    tmp_path: Path, resource_type
):
    _write_minimal_repo(tmp_path)
    pair = replace(_pair(), record=replace(_pair().record, resource_type=resource_type))
    bibliography = tmp_path / "pages/BIBLIOGRAPHY.md"
    bibliography.write_text(
        bibliography.read_text()
        + "| 1 | 2026 | 🧠 | Paper | Existing paper | Zenodo | 10.5281/zenodo.100 | [📄](../papers/2026_Existing/) |\n"
    )
    software = tmp_path / "pages/SOFTWARE.md"
    software.write_text(
        software.read_text().replace(
            "Reproducible computational research project",
            f"Software · [Zenodo](https://doi.org/{pair.doi}) · [📄](../papers/2026_Existing/)",
        )
    )
    cache = classification_cache_from_payload(
        {"classification_cache": classification_cache_payload([], repo_root=tmp_path)}
    )
    actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type == "software_catalogued"
    assert actions[0].folder == "2026_Existing"
    assert ordered_apply_pairs(actions, [pair]) == []
    # New versions share the linked concept DOI and remain supplements.
    newer = replace(
        pair, record=replace(pair.record, record_id="20990002", version="2.0")
    )
    assert (
        build_sync_actions([newer], repo_root=tmp_path)[0].action_type
        == "software_catalogued"
    )
    # A paper cannot disappear because its DOI is also linked by a software row.
    publication = replace(
        pair, record=replace(pair.record, resource_type={"type": "publication"})
    )
    assert (
        build_sync_actions([publication], repo_root=tmp_path)[0].action_type
        == "create_new"
    )
    # Re-read current catalog links even when the decision cache remains valid.
    software.write_text(
        software.read_text().replace(
            "../papers/2026_Existing/", "../papers/2026_Uncited/"
        )
    )
    assert (
        build_sync_actions([pair], repo_root=tmp_path, cache=cache)[0].action_type
        == "create_new"
    )


@pytest.mark.parametrize(
    "description",
    [
        "[Zenodo](https://doi.org/10.5281/zenodo.20990001)",
        "[Zenodo](https://doi.org/10.5281/zenodo.999) · [📄](../papers/2026_Existing/)",
        "[Zenodo](https://doi.org/10.5281/zenodo.20990001) · [📄](../papers/2026_Uncited/)",
    ],
)
def test_software_methods_pdf_without_catalogued_supplement_stays_new(
    tmp_path: Path, description
):
    _write_minimal_repo(tmp_path)
    pair = replace(
        _pair(), record=replace(_pair().record, resource_type={"type": "software"})
    )
    bibliography = tmp_path / "pages/BIBLIOGRAPHY.md"
    bibliography.write_text(
        bibliography.read_text()
        + "| 1 | 2026 | 🧠 | Paper | Existing paper | Zenodo | 10.5281/zenodo.100 | [📄](../papers/2026_Existing/) |\n"
    )
    software = tmp_path / "pages/SOFTWARE.md"
    software.write_text(
        software.read_text().replace(
            "Reproducible computational research project", description
        )
    )
    assert pair.record.files[0]["key"].endswith(".pdf")
    assert build_sync_actions([pair], repo_root=tmp_path)[0].action_type == "create_new"


def test_observation_refresh_retains_exact_apply_receipt_without_new_approval(
    tmp_path, monkeypatch
):
    import sync_paired_publications as sync

    _write_minimal_repo(tmp_path)
    pair = _pair()
    apply_publication_pair(pair, repo_root=tmp_path, download_files=False)
    action = build_sync_actions([pair], repo_root=tmp_path)[0]
    applied = apply_publication_pair(
        pair, repo_root=tmp_path, download_files=False, folder=action.folder
    )
    attested = attest_applied_publication(applied, action, repo_root=tmp_path)
    report = tmp_path / "reports/paired_publications_2026-10-12.json"
    kwargs = dict(
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[action],
        warnings=[],
    )
    monkeypatch.setattr(sync, "generated_timestamp", lambda: "2026-10-12T10:00:00Z")
    write_report(report, **kwargs, applied=[attested])
    old = json.loads(report.read_text())["applied"]
    monkeypatch.setattr(sync, "generated_timestamp", lambda: "2026-10-12T11:00:00Z")
    write_report(report, **kwargs)
    refreshed = json.loads(report.read_text())
    assert refreshed["generated_at"] == "2026-10-12T11:00:00Z"
    assert (
        refreshed["applied"] == old
    )  # Original hashes, approval, and apply time survive.
    check_report(repo_root=tmp_path)
    kwargs["actions"] = []
    write_report(report, **kwargs)
    assert (
        json.loads(report.read_text())["applied"] == []
    )  # No receipt transferred to another action.


def test_paired_intake_keeps_all_creators_and_existing_curated_byline(tmp_path):
    _write_minimal_repo(tmp_path)
    bibliography = tmp_path / "pages/BIBLIOGRAPHY.md"
    bibliography.write_text(
        bibliography.read_text().replace("| Docs |", "| Docs | Authors |")
    )
    pair = _pair()
    pair = replace(
        pair,
        record=replace(
            pair.record,
            creators=[
                {"name": "Friedman, Daniel Ari"},
                {"name": "Mikhailova, Alexandra"},
            ],
        ),
    )
    folder = "2026_NewComputationalProject"
    sync_paired_publications.ensure_bibliography_row(pair, folder, [], tmp_path)
    sync_paired_publications.update_paper_metadata_index(pair, folder, [], tmp_path)
    rows = [
        line
        for line in bibliography.read_text().splitlines()
        if line.startswith("| 1 |")
    ]
    assert len(rows) == 1
    assert rows[0].endswith("| Friedman, Daniel Ari; Mikhailova, Alexandra |")
    metadata = json.loads((tmp_path / "papers/paper_metadata.json").read_text())
    assert metadata[folder]["authors"] == "Daniel Ari Friedman, Alexandra Mikhailova"
    bibliography.write_text(
        bibliography.read_text().replace(
            "Friedman, Daniel Ari; Mikhailova, Alexandra |", "Existing curated byline |"
        )
    )
    revised = replace(pair, record=replace(pair.record, doi="10.5281/zenodo.20990002"))
    sync_paired_publications.ensure_bibliography_row(revised, folder, [], tmp_path)
    row = next(
        line
        for line in bibliography.read_text().splitlines()
        if line.startswith("| 1 |")
    )
    assert row.endswith("| Existing curated byline |")
    assert "20990002" in row


# Exact publication editions remain distinct under an unchanged concept DOI.
def _version_bound_review_fixture(root):
    _write_minimal_repo(root)
    base = _pair()
    concept = "10.5281/zenodo.20990000"
    release = replace(
        base.release,
        body=f"DOI: https://doi.org/{concept}\nZenodo: https://zenodo.org/records/20990000\n",
    )
    record = replace(
        base.record,
        doi=concept,
        record_id="20990001",
        html_url="https://zenodo.org/records/20990001",
        version="1.0.0",
        files=[
            {
                "key": "paper.pdf",
                "size": 1234,
                "checksum": "md5:" + "a" * 32,
                "links": {
                    "self": "https://zenodo.org/api/records/20990001/files/paper.pdf/content"
                },
            }
        ],
    )
    pair = replace(base, release=release, record=record)
    apply_publication_pair(pair, repo_root=root, download_files=False)
    _write_review_decision(root, pair, edition_bound=False)
    frozen = {
        "generated_at": "2026-06-18T00:00:00Z",
        "source": "GitHub Releases API + Zenodo Records API",
        "owners": ["docxology"],
        "warnings": [],
        "pairs": [pair.to_dict()],
        "github_releases": [pair.release.to_dict()],
        "zenodo_records": [pair.record.to_dict()],
    }
    frozen_path = root / "reports/publication_intake_2026-06-18.json"
    frozen_bytes = (json.dumps(frozen, indent=2) + "\n").encode()
    frozen_path.write_bytes(frozen_bytes)
    ledger_path = root / "data/paired-publication-decisions.json"
    ledger = json.loads(ledger_path.read_text())
    group = ledger["groups"][0]
    group["decision"] = "accept"
    group["representation"] = "bibliography-folder"
    candidate = group["raw_candidates"][0]
    candidate.update(
        review_decision="accept",
        zenodo_version_record_id=pair.record.record_id,
        source_report="reports/publication_intake_2026-06-18.json",
        source_report_sha256=hashlib.sha256(frozen_bytes).hexdigest(),
    )
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    return pair, ledger


def _changed_reviewed_edition(pair, change):
    if change == "new_record":
        return replace(
            pair,
            record=replace(
                pair.record,
                record_id="20990002",
                version="2.0.0",
                html_url="https://zenodo.org/records/20990002",
            ),
        )
    if change == "version_metadata":
        return replace(pair, record=replace(pair.record, version="1.0.1"))
    assert change == "file_manifest"
    files = json.loads(json.dumps(pair.record.files))
    files[0]["checksum"] = "md5:" + "b" * 32
    return replace(pair, record=replace(pair.record, files=files))


def _review_cache(root, pair):
    entries = []
    actions = build_sync_actions(
        [pair], repo_root=root, already_reviewed_entries=entries
    )
    assert actions[0].action_type == "already_reviewed"
    payload = {
        "classification_cache": classification_cache_payload(entries, repo_root=root)
    }
    cache = classification_cache_from_payload(payload)
    assert cache is not None
    return cache


@pytest.mark.parametrize("cached", [False, True])
def test_exact_bound_edition_keeps_existing_acknowledgement(tmp_path, cached):
    pair, _ = _version_bound_review_fixture(tmp_path)
    cache = _review_cache(tmp_path, pair) if cached else None
    actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type == "already_reviewed"


@pytest.mark.parametrize("cached", [False, True])
@pytest.mark.parametrize("change", ["new_record", "version_metadata", "file_manifest"])
def test_changed_edition_cannot_inherit_concept_acknowledgement(
    tmp_path, cached, change
):
    pair, _ = _version_bound_review_fixture(tmp_path)
    cache = _review_cache(tmp_path, pair) if cached else None
    changed = _changed_reviewed_edition(pair, change)
    # The work-level citation DOI and public URL deliberately stay canonical.
    assert changed.doi == pair.doi
    assert changed.zenodo_record_url == pair.zenodo_record_url
    before = {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    actions = build_sync_actions([changed], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type != "already_reviewed"
    assert actions[0].folder == "2026_NewComputationalProject"
    assert {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    } == before


@pytest.mark.parametrize(
    "change", [None, "new_record", "version_metadata", "file_manifest"]
)
def test_public_review_rechecks_exact_edition_even_if_report_says_reviewed(
    tmp_path, change
):
    from docxology_tools.public_source_review import paired_publication_items

    pair, ledger = _version_bound_review_fixture(tmp_path)
    old_action = build_sync_actions([pair], repo_root=tmp_path)[0]
    observed = _changed_reviewed_edition(pair, change) if change else pair
    # A persisted old action cannot transfer its outcome to changed observed bytes.
    report = {
        "generated_at": "2026-06-18T01:00:00Z",
        "warnings": [],
        "actions": [old_action.to_dict()],
        "pairs": [observed.to_dict()],
        "zenodo_records": [observed.record.to_dict()],
    }
    items = paired_publication_items(
        report,
        ledger,
        report_source="reports/paired_publications_2026-06-18.json",
        decision_source="data/paired-publication-decisions.json",
        snapshot_generated_at=None,
        repo_root=tmp_path,
    )
    assert len(items) == 1
    assert items[0]["status"] == ("deferred" if change else "applied")


@pytest.mark.parametrize("asset_count", [1, 3])
def test_release_asset_normalized_payload_roundtrip_keeps_complete_urls(asset_count):
    from docxology_tools.publication_pairing import GitHubAsset

    release = replace(
        _pair().release,
        assets=[
            GitHubAsset(
                f"artifact-{i}.pdf",
                f"https://github.com/docxology/new_repo/releases/download/v1.0.0/artifact-{i}.pdf",
                100 + i,
            )
            for i in range(asset_count)
        ],
    )
    rebuilt = sync_paired_publications.github_release_from_payload(release.to_dict())
    assert rebuilt.to_dict() == release.to_dict()


def test_release_asset_cached_and_direct_pairing_payloads_are_identical():
    from docxology_tools.publication_pairing import GitHubAsset

    base = _pair()
    release = replace(
        base.release,
        assets=[
            GitHubAsset(
                "paper.pdf",
                "https://github.com/docxology/new_repo/releases/download/v1.0.0/paper.pdf",
                1234,
            )
        ],
    )
    cached = github_releases_from_payload({"github_releases": [release.to_dict()]})
    direct_pairs = find_publication_pairs([release], [base.record])
    cached_pairs = find_publication_pairs(cached, [base.record])
    assert [pair.to_dict() for pair in cached_pairs] == [
        pair.to_dict() for pair in direct_pairs
    ]


def test_release_asset_legacy_api_payload_url_remains_supported():
    payload = _pair().release.to_dict()
    payload["assets"] = [
        {
            "name": "paper.pdf",
            "size": 1234,
            "browser_download_url": "https://github.com/docxology/new_repo/releases/download/v1.0.0/paper.pdf",
        }
    ]
    release = sync_paired_publications.github_release_from_payload(payload)
    assert (
        release.assets[0].download_url == payload["assets"][0]["browser_download_url"]
    )


@pytest.mark.parametrize("cached", [False, True])
@pytest.mark.parametrize("damage", ["missing", "tampered", "ambiguous"])
def test_edition_review_fails_closed_for_unavailable_frozen_evidence(
    tmp_path, cached, damage
):
    pair, ledger = _version_bound_review_fixture(tmp_path)
    cache = _review_cache(tmp_path, pair) if cached else None
    source = tmp_path / "reports/publication_intake_2026-06-18.json"
    if damage == "missing":
        source.unlink()
    elif damage == "tampered":
        source.write_text(source.read_text().replace("paper.pdf", "changed.pdf"))
    else:
        snapshot = json.loads(source.read_text())
        changed = _changed_reviewed_edition(pair, "new_record")
        snapshot["zenodo_records"].append(changed.record.to_dict())
        snapshot["pairs"].append(changed.to_dict())
        raw = (json.dumps(snapshot, indent=2) + "\n").encode()
        source.write_bytes(raw)
        ledger["groups"][0]["raw_candidates"][0]["source_report_sha256"] = (
            hashlib.sha256(raw).hexdigest()
        )
        (tmp_path / "data/paired-publication-decisions.json").write_text(
            json.dumps(ledger) + "\n"
        )
    actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type != "already_reviewed"


def _inline_edition_evidence(pair):
    fields = (
        "record_id",
        "doi",
        "title",
        "publication_date",
        "version",
        "resource_type",
        "creators",
        "description",
        "keywords",
        "related_identifiers",
        "files",
        "html_url",
    )
    record = pair.record.to_dict()
    fingerprint = [
        pair.doi.casefold(),
        pair.github_release_url.rstrip("/"),
        pair.zenodo_record_url.rstrip("/"),
        pair.github_repo.casefold(),
        pair.record.title.casefold(),
        pair.release.tag,
    ]
    frozen = {
        "generated_at": "2026-06-18T00:00:00Z",
        "source": "GitHub Releases API + Zenodo Records API",
        "owners": ["docxology"],
        "warnings": [],
        "pairs": [pair.to_dict()],
        "github_releases": [pair.release.to_dict()],
        "zenodo_records": [pair.record.to_dict()],
    }
    frozen_sha = hashlib.sha256(
        (json.dumps(frozen, indent=2) + "\n").encode()
    ).hexdigest()
    return {
        "schema_version": 1,
        "record_id": pair.record.record_id,
        "record_sha256": hashlib.sha256(
            json.dumps(
                {key: record[key] for key in fields},
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode()
        ).hexdigest(),
        "candidate_sha256": hashlib.sha256(
            json.dumps(fingerprint, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest(),
        "source": {
            "kind": "git_blob",
            "commit": "c" * 40,
            "blob_oid": "d" * 40,
            "path": "reports/publication_intake_2026-06-18.json",
            "sha256": frozen_sha,
        },
    }


@pytest.mark.parametrize("changed", [False, True])
def test_curated_original_blob_edition_evidence_needs_no_old_blob_or_report(
    tmp_path, changed
):
    pair, ledger = _version_bound_review_fixture(tmp_path)
    ledger["groups"][0]["raw_candidates"][0]["edition_evidence"] = (
        _inline_edition_evidence(pair)
    )
    (tmp_path / "data/paired-publication-decisions.json").write_text(
        json.dumps(ledger) + "\n"
    )
    (tmp_path / "reports/publication_intake_2026-06-18.json").unlink()
    observed = _changed_reviewed_edition(pair, "new_record") if changed else pair
    action = build_sync_actions([observed], repo_root=tmp_path)[0]
    assert (action.action_type == "already_reviewed") is (not changed)


def test_new_edition_explicit_supersession_preserves_history_without_old_ack_transfer(
    tmp_path,
):
    pair, ledger = _version_bound_review_fixture(tmp_path)
    original = json.loads(json.dumps(ledger["groups"][0]))
    original["raw_candidates"][0]["edition_evidence"] = _inline_edition_evidence(pair)
    ledger["groups"][0] = original
    newer = _changed_reviewed_edition(pair, "new_record")
    successor = json.loads(json.dumps(original))
    successor.update(
        id="R02", decided_by="Second reviewer", decided_at="2026-06-19T00:00:00Z"
    )
    successor["raw_candidates"][0]["edition_evidence"] = _inline_edition_evidence(newer)
    successor["raw_candidates"][0]["zenodo_version_record_id"] = newer.record.record_id
    successor["raw_candidates"][0]["source_report_sha256"] = successor[
        "raw_candidates"
    ][0]["edition_evidence"]["source"]["sha256"]
    successor["supersession"] = {
        "supersedes_group_id": "R01",
        "authenticated": True,
        "approved_by": "Second reviewer",
        "approved_at": "2026-06-19T00:00:00Z",
        "rationale": "Explicit review acknowledges the replacement deposited edition.",
        "superseded_candidate": {
            "doi": pair.doi,
            "github_release_url": pair.github_release_url,
            "zenodo_record_url": pair.zenodo_record_url,
            "github_repo": pair.github_repo,
            "title": pair.record.title,
            "release_tag": pair.release.tag,
        },
    }
    ledger["groups"].append(successor)
    path = tmp_path / "data/paired-publication-decisions.json"
    path.write_text(json.dumps(ledger) + "\n")
    old_action, new_action = build_sync_actions([pair, newer], repo_root=tmp_path)
    assert old_action.action_type != "already_reviewed"
    assert new_action.action_type == "already_reviewed"
    assert json.loads(path.read_text())["groups"][0] == original


def test_cached_edition_binding_is_never_authority_over_durable_ledger(tmp_path):
    pair, _ = _version_bound_review_fixture(tmp_path)
    cache = _review_cache(tmp_path, pair)
    newer = _changed_reviewed_edition(pair, "new_record")
    cached = next(iter(cache.already_reviewed.values()))
    cached.update(
        edition_record_id=newer.record.record_id,
        edition_record_sha256=_inline_edition_evidence(newer)["record_sha256"],
        edition_binding_state="bound",
    )
    # Genuine current ledger/bibliography hashes do not authenticate a mutable cache row.
    assert cache.inputs == classification_inputs(tmp_path)
    assert (
        build_sync_actions([newer], repo_root=tmp_path, cache=cache)[0].action_type
        != "already_reviewed"
    )


def test_missing_edition_decisions_keep_observation_deferred(tmp_path):
    from docxology_tools.public_source_review import paired_publication_items

    pair, _ = _version_bound_review_fixture(tmp_path)
    action = build_sync_actions([pair], repo_root=tmp_path)[0]
    report = {
        "generated_at": "2026-06-18T01:00:00Z",
        "warnings": [],
        "actions": [action.to_dict()],
        "pairs": [pair.to_dict()],
        "zenodo_records": [pair.record.to_dict()],
    }
    items = paired_publication_items(
        report,
        None,
        report_source="reports/paired_publications_2026-06-18.json",
        decision_source=None,
        snapshot_generated_at=None,
        repo_root=tmp_path,
    )
    assert len(items) == 1 and items[0]["status"] == "deferred"


@pytest.mark.parametrize(
    "change", [None, "new_record", "version_metadata", "file_manifest"]
)
def test_ambiguous_manual_review_rechecks_edition_evidence(tmp_path, change):
    from docxology_tools.public_source_review import paired_publication_items

    pair, ledger = _version_bound_review_fixture(tmp_path)
    action = build_sync_actions([pair], repo_root=tmp_path)[0].to_dict()
    action["action_type"] = "needs_review"
    observed = _changed_reviewed_edition(pair, change) if change else pair
    report = {
        "generated_at": "2026-06-18T01:00:00Z",
        "warnings": [],
        "actions": [action],
        "pairs": [observed.to_dict()],
        "zenodo_records": [observed.record.to_dict()],
    }
    items = paired_publication_items(
        report,
        ledger,
        report_source="reports/paired_publications_2026-06-18.json",
        decision_source="data/paired-publication-decisions.json",
        snapshot_generated_at=None,
        repo_root=tmp_path,
    )
    assert len(items) == 1
    assert items[0]["status"] == ("deferred" if change else "applied")


def _github_api_rows(reader, start, count):
    rows = []
    for number in range(start, start + count):
        row = {
            "id": number,
            "name": f"repo-{number}",
            "full_name": f"example/repo-{number}",
            "node_id": f"R_{number}",
            "owner": {"login": "example"},
            "html_url": f"https://github.com/example/repo-{number}",
            "assets": [],
            "tag_name": f"v{number}",
            "published_at": "2026-11-06T00:00:00Z",
        }
        if reader == "pair-releases":
            row["html_url"] = (
                f"https://github.com/example/project/releases/tag/v{number}"
            )
        rows.append(row)
    return rows


def _github_public_reader(monkeypatch, reader, respond, limit=None):
    import urllib.parse
    import build_github_inventory as inventory

    module = (
        inventory if reader == "inventory-repositories" else sync_paired_publications
    )
    calls = []

    def request(url, **kwargs):
        page = int(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["page"][0])
        calls.append(page)
        return respond(page)

    monkeypatch.setattr(
        module,
        "request_json" if reader == "inventory-repositories" else "fetch_json",
        request,
    )
    if limit is not None:
        monkeypatch.setattr(module, "MAX_GITHUB_PAGES", limit, raising=False)

    def call():
        if reader == "inventory-repositories":
            return inventory.fetch_repositories("example")
        if reader == "pair-releases":
            return sync_paired_publications.fetch_github_releases_for_repo(
                "example", "project"
            )
        return sync_paired_publications.fetch_github_repositories("example")

    return call, calls


@pytest.mark.parametrize(
    "reader", ["pair-repositories", "pair-releases", "inventory-repositories"]
)
@pytest.mark.parametrize(
    "kind",
    [
        "non_object",
        "missing_id",
        "boolean_id",
        "oversized",
        "duplicate_in_page",
        "duplicate_across_pages",
        "missing_identity_name",
    ],
)
def test_github_public_readers_refuse_malformed_or_repeated_rows(
    monkeypatch, reader, kind
):
    first = _github_api_rows(reader, 1, 100 if kind == "duplicate_across_pages" else 1)
    second = []
    if kind == "non_object":
        first = [None]
    elif kind == "missing_id":
        first[0].pop("id")
    elif kind == "boolean_id":
        first[0]["id"] = True
    elif kind == "oversized":
        first = _github_api_rows(reader, 1, 101)
    elif kind == "duplicate_in_page":
        first += json.loads(json.dumps(first))
    elif kind == "duplicate_across_pages":
        second = [first[-1], *_github_api_rows(reader, 101, 99)]
    elif kind == "missing_identity_name":
        first[0].pop("tag_name" if reader == "pair-releases" else "name")
    call, _ = _github_public_reader(
        monkeypatch,
        reader,
        lambda page: first if page == 1 else second if page == 2 else [],
    )
    with pytest.raises(RuntimeError, match="GitHub"):
        call()


@pytest.mark.parametrize(
    "reader", ["pair-repositories", "pair-releases", "inventory-repositories"]
)
def test_github_public_readers_refuse_unproven_completion_at_request_bound(
    monkeypatch, reader
):
    def respond(page):
        assert page <= 2, "reader requested beyond its declared page budget"
        return _github_api_rows(reader, (page - 1) * 100 + 1, 100)

    call, calls = _github_public_reader(monkeypatch, reader, respond, limit=2)
    with pytest.raises(RuntimeError, match="GitHub.*page"):
        call()
    assert calls == [1, 2]


@pytest.mark.parametrize(
    "reader", ["pair-repositories", "pair-releases", "inventory-repositories"]
)
@pytest.mark.parametrize("count", [0, 338])
def test_github_public_readers_preserve_complete_bounded_order(
    monkeypatch, reader, count
):
    rows = _github_api_rows(reader, 1, count)
    call, calls = _github_public_reader(
        monkeypatch, reader, lambda page: rows[(page - 1) * 100 : page * 100]
    )
    fetched = call()
    assert len(fetched) == count
    assert calls == ([1] if count == 0 else [1, 2, 3, 4])
    if reader == "pair-releases":
        assert [r.tag for r in fetched] == [r["tag_name"] for r in rows]
    else:
        assert fetched == rows


@pytest.mark.parametrize(
    "reader", ["pair-repositories", "pair-releases", "inventory-repositories"]
)
def test_github_public_readers_keep_nonlist_response_refusal(monkeypatch, reader):
    call, _ = _github_public_reader(
        monkeypatch, reader, lambda page: {"message": "unavailable"}
    )
    with pytest.raises(RuntimeError, match="GitHub"):
        call()


def _metadata_extension_fixture(root):
    _write_minimal_repo(root)
    pair = _pair()
    applied = apply_publication_pair(pair, repo_root=root, download_files=False)
    return (
        pair,
        applied.folder,
        root / "papers/paper_metadata.json",
        root / "papers" / applied.folder / "metadata.json",
    )


def test_publication_index_preserves_independently_curated_extensions(tmp_path):
    pair, folder, index, _ = _metadata_extension_fixture(tmp_path)
    data = json.loads(index.read_text())
    extras = {
        "tags": ["curated"],
        "methods": ["source-backed method"],
        "key_findings": ["retained finding"],
        "abstract_provenance": {"source": "full_text.md", "sha256": "a" * 64},
        "keywords_provenance": {"source": "metadata.json", "sha256": "b" * 64},
    }
    data[folder].update(extras)
    index.write_text(json.dumps(data) + "\n")
    revised = replace(pair, record=replace(pair.record, title="Updated reviewed title"))
    sync_paired_publications.update_paper_metadata_index(revised, folder, [], tmp_path)
    actual = json.loads(index.read_text())[folder]
    assert {key: actual[key] for key in extras} == extras
    assert actual["name"] == revised.record.title and actual["doi"] == pair.doi


@pytest.mark.parametrize(
    "field,provenance",
    [("description", "abstract_provenance"), ("keywords", "keywords_provenance")],
)
def test_publication_apply_requires_review_before_replacing_provenance_bound_content(
    tmp_path, field, provenance
):
    pair, folder, index, _ = _metadata_extension_fixture(tmp_path)
    data = json.loads(index.read_text())
    data[folder][provenance] = {"source": "full_text.md", "sha256": "a" * 64}
    index.write_text(json.dumps(data) + "\n")
    value = "Different abstract" if field == "description" else ["different keyword"]
    revised = replace(pair, record=replace(pair.record, **{field: value}))
    before = {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    with pytest.raises(ValueError, match="provenance"):
        apply_publication_pair(
            revised, repo_root=tmp_path, download_files=False, folder=folder
        )
    assert {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    } == before


@pytest.mark.parametrize("target", ["index", "folder"])
@pytest.mark.parametrize("malformed", ["{broken", "[]"])
def test_publication_apply_refuses_bad_metadata_before_any_write(
    tmp_path, target, malformed
):
    pair, folder, index, metadata = _metadata_extension_fixture(tmp_path)
    path = index if target == "index" else metadata
    path.write_text(malformed)
    revised = replace(
        pair,
        release=replace(
            pair.release,
            html_url="https://github.com/docxology/new_repo/releases/tag/v2.0.0",
        ),
    )
    before = {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    with pytest.raises(ValueError):
        apply_publication_pair(
            revised,
            repo_root=tmp_path,
            download_files=False,
            folder=folder,
            refresh_docs=True,
        )
    assert {
        p.relative_to(tmp_path): p.read_bytes()
        for p in tmp_path.rglob("*")
        if p.is_file()
    } == before


def test_publication_index_rejects_malformed_existing_folder_entry(tmp_path):
    pair, folder, index, _ = _metadata_extension_fixture(tmp_path)
    data = json.loads(index.read_text())
    data[folder] = ["not an object"]
    index.write_text(json.dumps(data) + "\n")
    before = index.read_bytes()
    with pytest.raises(ValueError):
        sync_paired_publications.update_paper_metadata_index(pair, folder, [], tmp_path)
    assert index.read_bytes() == before


def test_github_inventory_cli_preserves_previous_outputs_on_count_warning(
    tmp_path, monkeypatch
):
    import build_github_inventory as inventory

    cache = tmp_path / "github-repositories.json"
    cache.write_bytes(b"previous complete inventory\n")
    payload = {
        "warnings": ["example profile public_repos=2 but fetched1"],
        "counts": {
            "primary_total": 1,
            "forks": 0,
            "docxology": 1,
            "ActiveInferenceInstitute": 0,
        },
    }
    monkeypatch.setattr(inventory, "build_payload", lambda: payload)
    writes = []

    def write(partial):
        writes.append(partial)
        cache.write_bytes(b"partial inventory\n")

    monkeypatch.setattr(inventory, "write_outputs", write)
    monkeypatch.setattr(sys, "argv", ["build_github_inventory.py"])
    with pytest.raises(SystemExit, match="warning"):
        inventory.main()
    assert writes == []
    assert cache.read_bytes() == b"previous complete inventory\n"


@pytest.mark.parametrize("damage", ["symlink", "ancestor_symlink", "hardlink"])
def test_edition_cache_dependency_never_reads_unsafe_frozen_sources(tmp_path, damage):
    pair, _ledger = _version_bound_review_fixture(tmp_path)
    relative = "reports/publication_intake_2026-06-18.json"
    source = tmp_path / relative
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    outside = tmp_path.parent / (tmp_path.name + "-external.json")
    outside.write_bytes(source.read_bytes())
    if damage == "ancestor_symlink":
        archived_reports = tmp_path.parent / (tmp_path.name + "-external-reports")
        (tmp_path / "reports").rename(archived_reports)
        (tmp_path / "reports").symlink_to(archived_reports, target_is_directory=True)
    else:
        source.unlink()
        if damage == "symlink":
            source.symlink_to(outside)
        else:
            import os

            os.link(outside, source)
    assert classification_inputs(tmp_path)["edition_source:" + relative] != expected
    assert (
        build_sync_actions([pair], repo_root=tmp_path)[0].action_type
        != "already_reviewed"
    )


# Explicit exact-record inclusion remains bounded and independent of author search.
def _explicit_record_payload(record):
    return {
        "id": int(record.record_id),
        "conceptdoi": record.doi,
        "metadata": {
            "title": record.title,
            "publication_date": record.publication_date,
            "version": record.version,
            "resource_type": record.resource_type,
            "creators": record.creators,
            "description": record.description,
            "keywords": record.keywords,
            "related_identifiers": record.related_identifiers,
        },
        "files": record.files,
        "links": {"html": record.html_url},
    }


def _explicit_cli_fixture(root, monkeypatch):
    _write_minimal_repo(root)
    pair = _pair()
    monkeypatch.setattr(sync_paired_publications, "REPO_ROOT", root)
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_github_releases",
        lambda owners, since=None: ([pair.release], []),
    )
    # No optional parameters may be added to the ordinary author-search call.
    monkeypatch.setattr(
        sync_paired_publications, "fetch_zenodo_records", lambda: ([pair.record], [])
    )
    monkeypatch.setattr(
        sync_paired_publications, "build_sync_actions", lambda pairs, **kwargs: []
    )
    monkeypatch.setattr(
        sync_paired_publications, "classification_cache_from_report", lambda root: None
    )
    monkeypatch.setattr(
        sync_paired_publications,
        "classification_cache_payload",
        lambda entries: {"inputs": classification_inputs(root), "already_reviewed": []},
    )
    return pair, root / "reports/paired_publications_2099-01-01.json"


def test_explicit_record_cli_fetches_one_exact_record_and_preserves_full_manifest(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    extra = replace(
        pair.record,
        record_id="201",
        doi="10.5281/zenodo.201",
        html_url="https://zenodo.org/records/201",
        title="Explicit extra source",
    )
    raw = _explicit_record_payload(extra)
    calls = []

    def fetch(url, **kwargs):
        calls.append((url, kwargs))
        return raw

    monkeypatch.setattr(sync_paired_publications, "fetch_json", fetch)
    assert (
        sync_paired_publications.main(
            [
                "--report",
                str(report),
                "--zenodo-record",
                "201",
                "--zenodo-record",
                "201",
            ]
        )
        == 0
    )
    payload = json.loads(report.read_text())
    assert calls == [("https://zenodo.org/api/records/201", {})]
    assert payload["explicit_zenodo_record_ids"] == [201]
    assert payload["zenodo_records"] == [pair.record.to_dict(), extra.to_dict()]
    assert payload["warnings"] == [] and payload["applied"] == []


def test_explicit_record_existing_exact_search_hit_is_not_duplicated(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_json",
        lambda url, **kwargs: _explicit_record_payload(pair.record),
    )
    assert (
        sync_paired_publications.main(
            ["--report", str(report), "--zenodo-record", pair.record.record_id]
        )
        == 0
    )
    payload = json.loads(report.read_text())
    assert payload["zenodo_records"] == [pair.record.to_dict()]
    assert payload["explicit_zenodo_record_ids"] == [int(pair.record.record_id)]


@pytest.mark.parametrize(
    "damage",
    [
        "wrong_id",
        "bool_id",
        "missing_metadata",
        "missing_files",
        "bad_creators",
        "bad_keywords",
        "conflict",
        "get_failure",
    ],
)
def test_explicit_record_failure_warns_and_preserves_previous_report_before_apply(
    tmp_path, monkeypatch, damage
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    report.write_bytes(b"previous complete report\n")
    raw = _explicit_record_payload(pair.record)
    if damage == "wrong_id":
        raw["id"] = 202
    elif damage == "bool_id":
        raw["id"] = True
    elif damage == "missing_metadata":
        raw.pop("metadata")
    elif damage == "missing_files":
        raw.pop("files")
    elif damage == "bad_creators":
        raw["metadata"]["creators"] = ["not an object"]
    elif damage == "bad_keywords":
        raw["metadata"]["keywords"] = "not an array"
    elif damage == "conflict":
        raw["metadata"]["title"] = "Conflicting current response"
    calls = []

    def fetch(url, **kwargs):
        calls.append(url)
        if damage == "get_failure":
            raise OSError("synthetic exact-record unavailable")
        return raw

    monkeypatch.setattr(sync_paired_publications, "fetch_json", fetch)
    monkeypatch.setattr(
        sync_paired_publications,
        "apply_publication_pair",
        lambda *a, **kw: pytest.fail("warning reached apply"),
    )
    with pytest.raises(SystemExit, match="API warnings"):
        sync_paired_publications.main(
            [
                "--apply",
                "--report",
                str(report),
                "--zenodo-record",
                pair.record.record_id,
            ]
        )
    assert calls == ["https://zenodo.org/api/records/" + pair.record.record_id]
    assert report.read_bytes() == b"previous complete report\n"


def test_explicit_record_twenty_unique_limit_refuses_before_any_fetch(
    tmp_path, monkeypatch
):
    _pair_value, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_github_releases",
        lambda *a, **kw: pytest.fail("over-limit reached fetch"),
    )
    args = ["--report", str(report)]
    for record_id in range(1, 22):
        args += ["--zenodo-record", str(record_id)]
    with pytest.raises(SystemExit):
        sync_paired_publications.main(args)
    assert not report.exists()


@pytest.mark.parametrize(
    "record_id",
    ["0", "-1", "+1", "01", "١", "１", "1/2", "https://zenodo.org/records/1"],
)
def test_explicit_record_cli_requires_positive_ascii_identity(
    tmp_path, monkeypatch, record_id
):
    _pair_value, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_github_releases",
        lambda *a, **kw: pytest.fail("invalid ID reached fetch"),
    )
    with pytest.raises(SystemExit):
        sync_paired_publications.main(
            ["--report", str(report), "--zenodo-record", record_id]
        )
    assert not report.exists()


def test_explicit_record_default_cli_keeps_existing_zero_argument_fetch_contract(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_json",
        lambda *a, **kw: pytest.fail("default requested an exact record"),
    )
    assert sync_paired_publications.main(["--report", str(report)]) == 0
    payload = json.loads(report.read_text())
    assert payload["zenodo_records"] == [pair.record.to_dict()]
    assert "explicit_zenodo_record_ids" not in payload


@pytest.mark.parametrize("requested", [False, True])
def test_explicit_record_cached_replay_preserves_inclusion_without_any_get(
    tmp_path, monkeypatch, requested
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    payload = _pairing_payload([pair.release], [pair.record])
    payload["explicit_zenodo_record_ids"] = [int(pair.record.record_id)]
    report.write_text(json.dumps(payload))
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_json",
        lambda *a, **kw: pytest.fail("cached replay performed GET"),
    )
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_github_releases",
        lambda *a, **kw: pytest.fail("cached replay fetched releases"),
    )
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_zenodo_records",
        lambda *a, **kw: pytest.fail("cached replay searched authors"),
    )
    args = ["--cache-reports", "--report", str(report)]
    if requested:
        args += ["--zenodo-record", pair.record.record_id]
    assert sync_paired_publications.main(args) == 0
    saved = json.loads(report.read_text())
    assert saved["explicit_zenodo_record_ids"] == [int(pair.record.record_id)]
    assert saved["zenodo_records"] == [pair.record.to_dict()]


def test_explicit_record_cache_missing_requested_id_refuses_without_get_or_write(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    report.write_text(json.dumps(_pairing_payload([pair.release], [pair.record])))
    original = report.read_bytes()
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_json",
        lambda *a, **kw: pytest.fail("missing cached ID performed GET"),
    )
    with pytest.raises(SystemExit, match="cached.*201|201.*cached"):
        sync_paired_publications.main(
            ["--cache-reports", "--report", str(report), "--zenodo-record", "201"]
        )
    assert report.read_bytes() == original


@pytest.mark.parametrize(
    "declared", [None, [True], ["20990001"], [0], [20990001, 20990001], [201]]
)
def test_explicit_record_cached_declaration_must_bind_unique_present_integer_records(
    tmp_path, declared
):
    pair = _pair()
    path = tmp_path / "cached.json"
    payload = _pairing_payload([pair.release], [pair.record])
    payload["explicit_zenodo_record_ids"] = declared
    path.write_text(json.dumps(payload))
    with pytest.raises(SystemExit, match="explicit"):
        load_cached_scan_payload(path)


@pytest.mark.parametrize(
    "mode", [["--check"], ["--redact-local-paths", "--report", "unused.json"]]
)
def test_explicit_record_option_is_never_silently_ignored_by_non_intake_modes(mode):
    with pytest.raises(SystemExit):
        sync_paired_publications.main([*mode, "--zenodo-record", "201"])


@pytest.mark.parametrize(
    "damage",
    [
        None,
        "commit",
        "foreign_repo",
        "query",
        "fragment",
        "userinfo",
        "http",
        "both_locations",
    ],
)
def test_inline_blob_url_requires_exact_immutable_report_identity(tmp_path, damage):
    pair, ledger = _version_bound_review_fixture(tmp_path)
    evidence = _inline_edition_evidence(pair)
    source = evidence["source"]
    original_path = source.pop("path")
    source["url"] = (
        "https://github.com/docxology/docxology/blob/"
        + source["commit"]
        + "/"
        + original_path
    )
    if damage == "commit":
        source["url"] = source["url"].replace(source["commit"], "b" * 40)
    elif damage == "foreign_repo":
        source["url"] = source["url"].replace("docxology/docxology", "other/docxology")
    elif damage == "query":
        source["url"] += "?raw=1"
    elif damage == "fragment":
        source["url"] += "#report"
    elif damage == "userinfo":
        source["url"] = source["url"].replace("github.com", "user@github.com")
    elif damage == "http":
        source["url"] = source["url"].replace("https:", "http:")
    elif damage == "both_locations":
        source["path"] = original_path
    ledger["groups"][0]["raw_candidates"][0]["edition_evidence"] = evidence
    (tmp_path / "data/paired-publication-decisions.json").write_text(json.dumps(ledger))
    (tmp_path / "reports/publication_intake_2026-06-18.json").unlink()
    action = build_sync_actions([pair], repo_root=tmp_path)[0]
    assert (action.action_type == "already_reviewed") is (damage is None)


@pytest.mark.parametrize("mode", ["same_pool", "filtered_pool", "live_pool"])
def test_explicit_record_capture_context_is_forwarded_only_for_exact_cached_pool(
    tmp_path, monkeypatch, mode
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    payload = _pairing_payload([pair.release], [pair.record])
    context = {
        "captured_at": "2026-01-01T01:00:00Z",
        "source_receipt_sha256": "a" * 64,
        "scope": {"records": 1, "releases": 1},
    }
    payload["source_observations"] = context
    report.write_text(json.dumps(payload))
    args = ["--report", str(report)]
    if mode != "live_pool":
        args += ["--cache-reports"]
        monkeypatch.setattr(
            sync_paired_publications,
            "fetch_json",
            lambda *a, **kw: pytest.fail("cached context performed GET"),
        )
    if mode == "filtered_pool":
        args += ["--since", "2099-01-01"]
    assert sync_paired_publications.main(args) == 0
    saved = json.loads(report.read_text())
    if mode == "same_pool":
        assert saved["source_observations"] == context
        assert json.dumps(saved["source_observations"]) == json.dumps(context)
    else:
        assert "source_observations" not in saved


def test_explicit_record_twenty_unique_ids_are_accepted_with_twenty_exact_gets(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    calls = []

    def fetch(url, **kwargs):
        record_id = url.rsplit("/", 1)[1]
        calls.append(record_id)
        return _explicit_record_payload(
            replace(
                pair.record,
                record_id=record_id,
                doi="10.5281/zenodo." + record_id,
                html_url="https://zenodo.org/records/" + record_id,
            )
        )

    monkeypatch.setattr(sync_paired_publications, "fetch_json", fetch)
    args = ["--report", str(report)]
    for record_id in range(1, 21):
        args += ["--zenodo-record", str(record_id)]
    assert sync_paired_publications.main(args) == 0
    saved = json.loads(report.read_text())
    assert calls == [str(i) for i in range(1, 21)]
    assert saved["explicit_zenodo_record_ids"] == list(range(1, 21))
    assert len(saved["zenodo_records"]) == 21
    assert len({record["doi"] for record in saved["zenodo_records"]}) == 21


def test_explicit_record_cache_can_declare_an_already_present_record_without_get(
    tmp_path, monkeypatch
):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    report.write_text(json.dumps(_pairing_payload([pair.release], [pair.record])))
    monkeypatch.setattr(
        sync_paired_publications,
        "fetch_json",
        lambda *a, **kw: pytest.fail("present cached ID performed GET"),
    )
    assert (
        sync_paired_publications.main(
            [
                "--cache-reports",
                "--report",
                str(report),
                "--zenodo-record",
                pair.record.record_id,
            ]
        )
        == 0
    )
    assert json.loads(report.read_text())["explicit_zenodo_record_ids"] == [
        int(pair.record.record_id)
    ]


def test_explicit_record_persisted_check_refuses_a_declared_missing_record(tmp_path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    path = tmp_path / "reports/paired_publications_2099-01-01.json"
    write_report(
        path,
        owners=["docxology"],
        releases=[pair.release],
        records=[pair.record],
        pairs=[pair],
        actions=[],
        warnings=[],
    )
    payload = json.loads(path.read_text())
    payload["explicit_zenodo_record_ids"] = [201]
    path.write_text(json.dumps(payload))
    with pytest.raises(SystemExit, match="explicit"):
        check_report(repo_root=tmp_path)


@pytest.mark.parametrize(
    "field,value",
    [
        ("creators", ["malformed creator"]),
        ("resource_type", {}),
        ("publication_date", "not a date"),
        ("files", [{"key": "paper.pdf"}]),
    ],
)
def test_explicit_record_cached_declaration_requires_complete_selected_record(
    tmp_path, field, value
):
    pair = _pair()
    payload = _pairing_payload([pair.release], [pair.record])
    payload["explicit_zenodo_record_ids"] = [int(pair.record.record_id)]
    payload["zenodo_records"][0][field] = value
    path = tmp_path / "cached.json"
    path.write_text(json.dumps(payload))
    with pytest.raises(SystemExit, match="explicit"):
        load_cached_scan_payload(path)


def test_explicit_record_preserves_real_year_only_publication_date(tmp_path, monkeypatch):
    _pair_value, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    fixture_path = Path(__file__).parent / "fixtures/zenodo-year-only-20804586.json"
    fixture_bytes = fixture_path.read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == "2eba0c3c9c3b624d158c081f76865a0bd38cbf6f3891d885ae834f8d674d996f"
    record = json.loads(fixture_bytes)["record"]
    assert record["id"] == 20804586
    assert record["metadata"]["publication_date"] == "2026"
    calls = []

    def fetch(url, **kwargs):
        calls.append(url)
        return record

    monkeypatch.setattr(sync_paired_publications, "fetch_json", fetch)
    assert sync_paired_publications.main(
        ["--report", str(report), "--zenodo-record", "20804586"]
    ) == 0
    saved = json.loads(report.read_text())
    observed = next(
        row for row in saved["zenodo_records"] if row["record_id"] == "20804586"
    )
    assert observed["publication_date"] == "2026"
    assert observed == ZenodoRecord.from_api(record).to_dict()
    assert saved["explicit_zenodo_record_ids"] == [20804586]
    assert calls == ["https://zenodo.org/api/records/20804586"]


@pytest.mark.parametrize("change", ["record_id", "file_manifest", "title"])
@pytest.mark.parametrize("reverse", [False, True])
def test_pairing_refuses_differing_observed_editions_for_same_release_and_concept(change, reverse):
    pair = _pair()
    if change == "record_id":
        conflicting = replace(
            pair.record,
            record_id="20990002",
            html_url="https://zenodo.org/records/20990002",
        )
    elif change == "file_manifest":
        files = [dict(row) for row in pair.record.files]
        files[0] = {**files[0], "size": files[0]["size"] + 1}
        conflicting = replace(pair.record, files=files)
    else:
        conflicting = replace(pair.record, title=pair.record.title + " — revised")
    records = [pair.record, conflicting]
    if reverse:
        records.reverse()
    with pytest.raises(ValueError, match="(?i)ambiguous|conflicting"):
        find_publication_pairs([pair.release], records)


def test_pairing_deduplicates_only_identical_record_payloads():
    pair = _pair()
    duplicate = replace(pair.record, files=[dict(row) for row in pair.record.files])
    pairs = find_publication_pairs([pair.release], [pair.record, duplicate])
    assert len(pairs) == 1
    assert pairs[0].record.to_dict() == pair.record.to_dict()


def test_explicit_record_ambiguous_concept_refuses_before_report_or_apply(tmp_path, monkeypatch):
    pair, report = _explicit_cli_fixture(tmp_path, monkeypatch)
    report.write_text(json.dumps(_pairing_payload([pair.release], [pair.record])))
    previous = report.read_bytes()
    newer = replace(
        pair.record,
        record_id="20990002",
        html_url="https://zenodo.org/records/20990002",
        version="2.0.0",
    )
    calls = []

    def fetch(url, **kwargs):
        calls.append(url)
        return _explicit_record_payload(newer)

    monkeypatch.setattr(sync_paired_publications, "fetch_json", fetch)
    monkeypatch.setattr(
        sync_paired_publications,
        "apply_publication_pair",
        lambda *args, **kwargs: pytest.fail("ambiguous editions reached apply"),
    )
    with pytest.raises(ValueError, match="(?i)ambiguous|conflicting"):
        sync_paired_publications.main(
            ["--apply", "--report", str(report), "--zenodo-record", "20990002"]
        )
    assert report.read_bytes() == previous
    assert calls == ["https://zenodo.org/api/records/20990002"]


def test_invalid_paired_pdf_metadata_fails_before_catalog_writes(tmp_path):
    _write_minimal_repo(tmp_path)
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    with pytest.raises(ValueError, match="bounded size, and MD5"):
        apply_publication_pair(_pair(), repo_root=tmp_path)
    assert {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()} == before
