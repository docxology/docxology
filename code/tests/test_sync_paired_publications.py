"""Tests for paired-publication sync apply helpers."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH_DIR))

from generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402
from publication_pairing import (  # noqa: E402
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
    (root / "papers" / "README.md").write_text("# Papers\n\n## Papers (0)\n", encoding="utf-8")
    (root / "papers" / "AGENTS.md").write_text(
        "# Papers\n\nREADME.md present | 0/0 folders\n", encoding="utf-8"
    )


def _write_review_decision(root: Path, pair: PublicationPair, *, folder: str = "2026_NewComputationalProject") -> None:
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
    assert receipt["provenance"]["approval"]["action_sha256"] == receipt[
        "provenance"
    ]["action_sha256"]
    check_report(repo_root=tmp_path)

    receipt["provenance"]["approval"]["action_sha256"] = "0" * 64
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    payload["applied"][0] = receipt
    report_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="unverifiable applied strong update receipt"):
        check_report(repo_root=tmp_path)


def test_ordered_apply_pairs_leaves_latest_release_as_final_metadata_writer(tmp_path: Path):
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
        "decision_summary": {"decision": "rejected", "groups": 1, "raw_candidates": 1, "note": "test"},
        "groups": [
            {
                "id": "R25",
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
    decisions_path.write_text(
        json.dumps(malformed, indent=2) + "\n", encoding="utf-8"
    )

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
    decisions_path.write_text(
        json.dumps(duplicate, indent=2) + "\n", encoding="utf-8"
    )
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
    assert build_sync_actions([pair], repo_root=tmp_path)[0].action_type == "already_reviewed"


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
        | {"applied": [{"doi": pair.doi, "folder": "2026_NewComputationalProject", "created": True}]},
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


def _variant_pair(pair: PublicationPair, *, doi: str, record_id: str, tag: str) -> PublicationPair:
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
    fresh = _variant_pair(reviewed, doi="10.5281/zenodo.20990002", record_id="20990002", tag="v2.0.0")
    pairs = [reviewed, fresh]
    full = build_sync_actions(pairs, repo_root=tmp_path)
    entries: list = []
    build_sync_actions(pairs, repo_root=tmp_path, already_reviewed_entries=entries)
    cache = classification_cache_from_payload(
        {"classification_cache": classification_cache_payload(entries, repo_root=tmp_path)}
    )
    assert cache is not None
    cached = build_sync_actions(pairs, repo_root=tmp_path, cache=cache)
    assert [action.to_dict() for action in cached] == [action.to_dict() for action in full]
    assert [action.action_type for action in cached] == ["already_reviewed", "create_new"]


def test_classification_cache_hit_skips_decision_log_and_title_scans(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache = classification_cache_from_payload(
        {"classification_cache": classification_cache_payload(entries, repo_root=tmp_path)}
    )

    def _explode(root):  # pragma: no cover - must never run on a full cache hit
        raise AssertionError("cached inputs must not be re-derived on a cache hit")

    with (
        mock.patch.object(sync_paired_publications, "reviewed_pair_decisions", _explode),
        mock.patch.object(sync_paired_publications, "existing_release_title_map", _explode),
        mock.patch.object(sync_paired_publications, "existing_repo_title_map", _explode),
    ):
        actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert actions[0].action_type == "already_reviewed"
    assert actions[0].folder == "2026_NewComputationalProject"


def test_classification_cache_falls_back_to_full_scan_when_decisions_drift(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache_block = classification_cache_payload(entries, repo_root=tmp_path)
    # The durable decision is withdrawn after the report was written.
    (tmp_path / "data" / "paired-publication-decisions.json").write_text('{"groups": []}\n', encoding="utf-8")
    cache = classification_cache_from_payload({"classification_cache": cache_block})
    actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert [action.to_dict() for action in actions] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]
    assert actions[0].action_type == "create_new"


def test_classification_cache_falls_back_to_full_scan_when_bibliography_drifts(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    _write_review_decision(tmp_path, pair)
    entries: list = []
    build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
    cache_block = classification_cache_payload(entries, repo_root=tmp_path)
    bibliography = tmp_path / "pages" / "BIBLIOGRAPHY.md"
    bibliography.write_text(bibliography.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
    cache = classification_cache_from_payload({"classification_cache": cache_block})
    calls = {"count": 0}
    real = sync_paired_publications.reviewed_pair_decisions

    def counting(root):
        calls["count"] += 1
        return real(root)

    with mock.patch.object(sync_paired_publications, "reviewed_pair_decisions", counting):
        actions = build_sync_actions([pair], repo_root=tmp_path, cache=cache)
    assert calls["count"] >= 1  # drift forced the full classification, not the cached one
    assert [action.to_dict() for action in actions] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]


def test_check_report_fails_on_malformed_classification_cache(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = {"inputs": {"bibliography_sha256": "short"}, "already_reviewed": "nope"}
    _write_report(tmp_path, payload)
    with pytest.raises(SystemExit, match="malformed classification_cache"):
        check_report(repo_root=tmp_path)


def test_check_report_warns_on_classification_cache_input_drift(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = classification_cache_payload([], repo_root=tmp_path)
    bibliography = tmp_path / "pages" / "BIBLIOGRAPHY.md"
    bibliography.write_text(bibliography.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
    _write_report(tmp_path, payload)
    check_report(repo_root=tmp_path)  # a dated report stays valid; drift is surfaced, not fatal
    assert "classification_cache inputs have drifted" in capsys.readouterr().err


def test_check_report_accepts_current_classification_cache(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    _write_minimal_repo(tmp_path)
    payload = _minimal_report_payload()
    payload["classification_cache"] = classification_cache_payload([], repo_root=tmp_path)
    _write_report(tmp_path, payload)
    check_report(repo_root=tmp_path)
    assert "drifted" not in capsys.readouterr().err


def test_report_payload_roundtrips_releases_records_and_cache(tmp_path: Path):
    _write_minimal_repo(tmp_path)
    pair = _pair()
    entries: list = []
    actions = build_sync_actions([pair], repo_root=tmp_path, already_reviewed_entries=entries)
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
    rebuilt = build_sync_actions(find_publication_pairs(releases, records), repo_root=tmp_path)
    assert [action.to_dict() for action in rebuilt] == [
        action.to_dict() for action in build_sync_actions([pair], repo_root=tmp_path)
    ]


def _pairing_payload(releases: list[GitHubRelease], records: list[ZenodoRecord], *, generated_at: str | None = None, warnings: list[str] | None = None) -> dict:
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
        json.dumps(_pairing_payload([pair.release], [pair.record], generated_at="2020-01-01T00:00:00Z")),
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
        json.dumps(_pairing_payload([pair.release], [pair.record], warnings=["github: rate limited"])),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="API warning"):
        load_cached_scan_payload(path, force=True)


def test_load_cached_scan_payload_refuses_payload_without_records(tmp_path: Path):
    path = tmp_path / "paired_publications_legacy.json"
    path.write_text(
        json.dumps({"source": "GitHub Releases API + Zenodo Records API", "generated_at": generated_timestamp(), "warnings": []}),
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="github_releases"):
        load_cached_scan_payload(path)
