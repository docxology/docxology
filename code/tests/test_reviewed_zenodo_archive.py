"""A manual source-archive review grants only its exact frozen record."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools.publication_pairing import ZenodoRecord  # noqa: E402
from check_zenodo_uncatalogued import build_report, check_report  # noqa: E402


def _json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


@pytest.fixture
def archive_review(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "SOFTWARE.md").write_text(
        "## 🧬 docxology\n\n"
        "| Repository | Description | Language | Stars | Updated |\n"
        "|---|---|---|---|---|\n"
        "| [demo](https://github.com/docxology/demo) | Demo source archive · "
        "[Archive](https://doi.org/10.5281/zenodo.500) · [📄](../papers/2026_Demo/) | Python | 0 | 2026 |\n",
        encoding="utf-8",
    )
    (pages / "BIBLIOGRAPHY.md").write_text(
        "| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| 1 | 2026 | 💻 | Paper | Demo manuscript | Zenodo | "
        "[10.5281/zenodo.900](https://doi.org/10.5281/zenodo.900) | [📁](../papers/2026_Demo/) |\n",
        encoding="utf-8",
    )
    record = ZenodoRecord(
        record_id="501", doi="10.5281/zenodo.500", title="Demo manuscript",
        publication_date="2026-11-03", version="0.5.0",
        resource_type={"type": "publication", "subtype": "workingpaper", "title": "Working paper"},
        creators=[{"name": "Friedman, Daniel Ari"}], description="A reviewed source archive.",
        keywords=["source"], related_identifiers=[],
        files=[{"key": "docxology/demo-v1.0.0.zip", "size": 123456,
                "checksum": "md5:" + "a" * 32,
                "links": {"self": "https://zenodo.org/api/records/501/files/docxology/demo-v1.0.0.zip/content"}}],
        html_url="https://zenodo.org/records/501",
    )
    identity = {
        "doi": record.doi, "github_repo": "docxology/demo",
        "github_release_url": "https://github.com/docxology/demo/releases/tag/v1.0.0",
        "zenodo_record_url": "https://zenodo.org/records/500",
        "record_title": record.title, "release_tag": "v1.0.0",
    }
    relative = "reports/publication_intake_2026-11-05.json"
    source = tmp_path / relative
    _json(source, {
        "source": "GitHub Releases API + Zenodo Records API", "warnings": [],
        "zenodo_records": [record.to_dict()],
        "pairs": [{**{key: value for key, value in identity.items() if key not in {"record_title", "release_tag"}},
                   "record": record.to_dict(), "release": {"tag": "v1.0.0"}}],
    })
    raw = {**identity, "zenodo_version_record_id": "501", "source_report": relative,
           "source_report_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
    group = {
        "id": "source-archive-review", "decision": "accept", "decided_by": "Named source reviewer",
        "decided_at": "2026-11-05T01:21:43+00:00", "doi": record.doi, "title": record.title,
        "candidate_github_repo": "docxology/demo", "folder": "2026_Demo",
        "representation": "software-catalog", "rationale": "Reviewed as supplemental source archive, preserving upstream working-paper type.",
        "raw_candidate_count": 1, "raw_candidates": [raw],
    }
    ledger = {"groups": [group]}
    _json(tmp_path / "data/paired-publication-decisions.json", ledger)
    return tmp_path, record, source, ledger


def _build(fixture, record=None):
    root, original, _, _ = fixture
    return build_report(root, records=[record or original], records_source="cached")


def _assert_not_exempt(report):
    assert report["uncatalogued_count"] == 1
    assert report.get("reviewed_source_archive_count", 0) == 0


def test_exact_reviewed_workingpaper_archive_is_separate_from_software_type(archive_review):
    report = _build(archive_review)
    assert report["uncatalogued_count"] == 0
    assert report["software_catalogued_count"] == 0
    assert report["reviewed_source_archive_count"] == 1
    approved = report["reviewed_source_archives"][0]
    assert approved["record_id"] == "501"
    assert approved["decision_group"] == "source-archive-review"
    assert approved["resource_type"]["subtype"] == "workingpaper"
    assert approved["software_row"] == "demo"
    assert approved["paper_folder"] == "2026_Demo"
    assert approved["source_report_sha256"] == hashlib.sha256(archive_review[2].read_bytes()).hexdigest()


def test_zip_only_is_not_itself_a_software_classification(archive_review):
    root, _, _, _ = archive_review
    (root / "data/paired-publication-decisions.json").unlink()
    _assert_not_exempt(_build(archive_review))


def test_later_workingpaper_record_under_same_concept_requires_its_own_review(archive_review):
    later = replace(archive_review[1], record_id="502", html_url="https://zenodo.org/records/502")
    _assert_not_exempt(_build(archive_review, later))


@pytest.mark.parametrize("change", [
    {"title": "A changed title"}, {"version": "0.6.0"},
    {"resource_type": {"type": "publication", "subtype": "article"}},
    {"doi": "10.5281/zenodo.700"},
])
def test_changed_record_identity_or_type_revokes_review(archive_review, change):
    _assert_not_exempt(_build(archive_review, replace(archive_review[1], **change)))


@pytest.mark.parametrize("field,value", [
    ("key", "different.zip"), ("size", 654321), ("checksum", "md5:" + "b" * 32),
    ("links", {"self": "https://zenodo.org/api/records/501/files/different.zip/content"}),
])
def test_changed_archive_manifest_revokes_review(archive_review, field, value):
    record = archive_review[1]
    changed = replace(record, files=[{**record.files[0], field: value}])
    _assert_not_exempt(_build(archive_review, changed))


def test_added_pdf_is_not_hidden_by_the_source_archive_review(archive_review):
    record = archive_review[1]
    changed = replace(record, files=[*record.files, {"key": "new.pdf", "size": 999}])
    _assert_not_exempt(_build(archive_review, changed))


@pytest.mark.parametrize("decision", ("reject", "superseded", "acknowledged"))
def test_only_an_accepted_software_catalog_decision_grants_the_exception(archive_review, decision):
    root, _, _, ledger = archive_review
    ledger["groups"][0]["decision"] = decision
    _json(root / "data/paired-publication-decisions.json", ledger)
    _assert_not_exempt(_build(archive_review))


def test_duplicate_conflicting_decisions_fail_closed(archive_review):
    root, _, _, ledger = archive_review
    conflicting = {**ledger["groups"][0], "id": "conflicting-review", "decision": "reject"}
    ledger["groups"].append(conflicting)
    _json(root / "data/paired-publication-decisions.json", ledger)
    report = _build(archive_review)
    _assert_not_exempt(report)
    assert report["reviewed_source_archive_drift_count"] > 0


@pytest.mark.parametrize("failure", ("missing", "tampered", "unsafe-path", "duplicate-record"))
def test_source_report_must_be_exact_safe_and_unambiguous(archive_review, failure):
    root, record, source, ledger = archive_review
    raw = ledger["groups"][0]["raw_candidates"][0]
    if failure == "missing":
        source.unlink()
    elif failure == "tampered":
        source.write_text(source.read_text() + " ", encoding="utf-8")
    elif failure == "unsafe-path":
        raw["source_report"] = "../outside.json"
        _json(root / "data/paired-publication-decisions.json", ledger)
    else:
        payload = json.loads(source.read_text())
        payload["zenodo_records"].append(record.to_dict())
        _json(source, payload)
        raw["source_report_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        _json(root / "data/paired-publication-decisions.json", ledger)
    _assert_not_exempt(_build(archive_review))


@pytest.mark.parametrize("target", ("software-doi", "paper-folder", "repository", "review-folder"))
def test_current_catalog_identity_is_required(archive_review, target):
    root, _, _, ledger = archive_review
    if target == "review-folder":
        ledger["groups"][0]["folder"] = "2026_Other"
        _json(root / "data/paired-publication-decisions.json", ledger)
    else:
        path = root / "pages" / ("BIBLIOGRAPHY.md" if target == "paper-folder" else "SOFTWARE.md")
        text = path.read_text()
        if target == "software-doi":
            text = text.replace("zenodo.500", "zenodo.600")
        elif target == "paper-folder":
            text = text.replace("2026_Demo", "2026_Other")
        else:
            text = text.replace("github.com/docxology/demo", "github.com/other/demo")
        path.write_text(text, encoding="utf-8")
    _assert_not_exempt(_build(archive_review))


@pytest.mark.parametrize("drift", ("source", "decision", "catalog", "saved-manifest", "saved-empty", "missing-context", "missing-receipts", "saved-observation"))
def test_persisted_check_revalidates_manual_exception(archive_review, drift):
    root, _, source, ledger = archive_review
    report = _build(archive_review)
    report["version_specific_doi_exception_drift_count"] = 0
    report["version_specific_doi_exception_drift"] = []
    saved = root / "reports/zenodo_uncatalogued_2026-11-05.json"
    _json(saved, report)
    assert check_report(saved, repo_root=root) == []
    if drift == "source":
        source.write_text(source.read_text() + " ", encoding="utf-8")
    elif drift == "decision":
        ledger["groups"][0]["decision"] = "reject"
        _json(root / "data/paired-publication-decisions.json", ledger)
    elif drift == "catalog":
        path = root / "pages/SOFTWARE.md"
        path.write_text(path.read_text().replace("zenodo.500", "zenodo.600"), encoding="utf-8")
    elif drift == "saved-manifest":
        report["reviewed_source_archives"][0]["record"]["files"][0]["size"] += 1
        _json(saved, report)
    elif drift == "saved-empty":
        report["reviewed_source_archives"] = []
        report["reviewed_source_archive_count"] = 0
        _json(saved, report)
    elif drift == "missing-context":
        report.pop("reviewed_source_archive_context")
        _json(saved, report)
    elif drift == "missing-receipts":
        report.pop("reviewed_source_archives")
        report.pop("reviewed_source_archive_count")
        _json(saved, report)
    else:
        report["reviewed_source_archive_context"]["records"][0]["files"][0]["size"] += 1
        _json(saved, report)
    assert any("reviewed source archive" in issue.lower() for issue in check_report(saved, repo_root=root))


def _pair(record, repository, tag):
    return {
        "doi": record.doi, "github_repo": repository,
        "github_release_url": f"https://github.com/{repository}/releases/tag/{tag}",
        "zenodo_record_url": record.record_url,
        "record": record.to_dict(), "release": {"tag": tag},
    }


def _next_review(group, record, repository, tag, source, digest, group_id, folder):
    result = json.loads(json.dumps(group))
    result.update(id=group_id, folder=folder, doi=record.doi, title=record.title,
                  candidate_github_repo=repository)
    result["raw_candidates"] = [{
        "doi": record.doi, "github_repo": repository,
        "github_release_url": f"https://github.com/{repository}/releases/tag/{tag}",
        "zenodo_record_url": record.record_url, "record_title": record.title,
        "release_tag": tag, "zenodo_version_record_id": record.record_id,
        "source_report": source, "source_report_sha256": digest,
    }]
    return result


def _assert_saved_report_passes(root, report):
    report["version_specific_doi_exception_drift_count"] = 0
    report["version_specific_doi_exception_drift"] = []
    saved = root / "reports/zenodo_uncatalogued_2026-11-05.json"
    _json(saved, report)
    assert check_report(saved, repo_root=root) == []


def test_represented_template_review_does_not_invalidate_active_archive_context(archive_review):
    root, original, source, ledger = archive_review
    template = replace(original, record_id="701", doi="10.5281/zenodo.700",
                       title="Template manuscript", html_url="https://zenodo.org/records/701",
                       files=[{"key": "docxology/template-v1.0.0.zip", "size": 3456,
                               "checksum": "md5:" + "b" * 32,
                               "links": {"self": "https://zenodo.org/api/records/701/files/docxology/template-v1.0.0.zip/content"}}])
    payload = json.loads(source.read_text())
    payload["zenodo_records"].append(template.to_dict())
    payload["pairs"].append(_pair(template, "docxology/template", "v1.0.0"))
    _json(source, payload)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    ledger["groups"][0]["raw_candidates"][0]["source_report_sha256"] = digest
    ledger["groups"].append(_next_review(
        ledger["groups"][0], template, "docxology/template", "v1.0.0",
        source.relative_to(root).as_posix(), digest, "template-review", "2026_Template",
    ))
    _json(root / "data/paired-publication-decisions.json", ledger)
    bibliography = root / "pages/BIBLIOGRAPHY.md"
    bibliography.write_text(bibliography.read_text() +
        "| 2 | 2026 | 💻 | Paper | Template manuscript | Zenodo | "
        "[10.5281/zenodo.700](https://doi.org/10.5281/zenodo.700) | [📁](../papers/2026_Template/) |\n", encoding="utf-8")
    software = root / "pages/SOFTWARE.md"
    software.write_text(software.read_text() +
        "| [template](https://github.com/docxology/template) | Template · "
        "[DOI](https://doi.org/10.5281/zenodo.700) · [📄](../papers/2026_Template/) | Python | 0 | 2026 |\n", encoding="utf-8")
    report = build_report(root, records=[original, template], records_source="cached")
    assert report["uncatalogued_count"] == 0
    assert report["reviewed_source_archive_count"] == 1
    assert report["reviewed_source_archive_drift_count"] == 0
    assert [row["record_id"] for row in report["reviewed_source_archive_context"]["records"]] == ["501"]
    _assert_saved_report_passes(root, report)


def test_later_review_preserves_nonobserved_historical_decision_without_false_drift(archive_review):
    root, original, historical_source, ledger = archive_review
    current = replace(original, record_id="502", version="0.6.0",
                      html_url="https://zenodo.org/records/502",
                      files=[{"key": "docxology/demo-v2.0.0.zip", "size": 34567,
                              "checksum": "md5:" + "c" * 32,
                              "links": {"self": "https://zenodo.org/api/records/502/files/docxology/demo-v2.0.0.zip/content"}}])
    relative = "reports/publication_intake_2026-11-06.json"
    source = root / relative
    _json(source, {"source": "GitHub Releases API + Zenodo Records API", "warnings": [],
                   "zenodo_records": [current.to_dict()],
                   "pairs": [_pair(current, "docxology/demo", "v2.0.0")]})
    ledger["groups"].append(_next_review(
        ledger["groups"][0], current, "docxology/demo", "v2.0.0", relative,
        hashlib.sha256(source.read_bytes()).hexdigest(), "later-archive-review", "2026_Demo",
    ))
    _json(root / "data/paired-publication-decisions.json", ledger)
    historical_source.unlink()  # An unrelated historical dependency is not consulted.
    report = _build(archive_review, current)
    assert report["uncatalogued_count"] == 0
    assert report["reviewed_source_archive_count"] == 1
    assert report["reviewed_source_archives"][0]["record_id"] == "502"
    assert report["reviewed_source_archive_drift_count"] == 0
    _assert_saved_report_passes(root, report)


def test_current_ordinary_software_coverage_does_not_require_a_manual_exception(archive_review):
    root, original, _, _ = archive_review
    software_record = replace(original, resource_type={"type": "software", "title": "Software"})
    report = _build(archive_review, software_record)
    assert report["uncatalogued_count"] == 0
    assert report["software_catalogued_count"] == 1
    assert report["reviewed_source_archive_count"] == 0
    assert report["reviewed_source_archive_drift_count"] == 0
    assert report["reviewed_source_archive_context"]["records"] == []
    _assert_saved_report_passes(root, report)
