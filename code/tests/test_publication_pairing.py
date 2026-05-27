"""Tests for GitHub + Zenodo publication pairing helpers."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC_DIR))

from publication_pairing import (  # noqa: E402
    GitHubRelease,
    ZenodoRecord,
    confidence_for_pair,
    extract_dois,
    find_publication_pairs,
    is_ignored_release,
)


def test_extract_dois_normalizes_markdown_links():
    text = "DOI: [10.5281/zenodo.20286478](https://doi.org/10.5281/zenodo.20286478)."
    assert extract_dois(text) == ["10.5281/zenodo.20286478"]


def test_api_normalization_for_github_and_zenodo_records():
    release = GitHubRelease.from_api(
        "docxology",
        "example",
        {
            "tag_name": "v1.0.0",
            "name": "Example Release",
            "body": "DOI: 10.5281/zenodo.1",
            "html_url": "https://github.com/docxology/example/releases/tag/v1.0.0",
            "published_at": "2026-05-27T00:00:00Z",
            "assets": [{"name": "paper.pdf", "browser_download_url": "https://example.test/paper.pdf", "size": 12}],
        },
    )
    record = ZenodoRecord.from_api(
        {
            "id": 1,
            "doi": "10.5281/zenodo.1",
            "links": {"html": "https://zenodo.org/records/1"},
            "metadata": {
                "title": "Example Release",
                "publication_date": "2026-05-27",
                "version": "1.0.0",
                "resource_type": {"type": "publication"},
                "creators": [{"name": "Friedman, Daniel Ari"}],
                "description": "Example.",
                "keywords": ["example"],
                "related_identifiers": [{"identifier": release.html_url}],
            },
            "files": [{"key": "paper.pdf"}],
        }
    )

    assert release.full_name == "docxology/example"
    assert release.assets[0].name == "paper.pdf"
    assert record.record_id == "1"
    assert record.record_url == "https://zenodo.org/records/1"


def test_template_smoke_release_is_ignored():
    release = GitHubRelease(
        owner="docxology",
        repo="template-release-smoke",
        tag="v0.4.0-release-smoke",
        name="Template release smoke v0.4.0 (integration test - do not cite)",
        body="This is a release smoke test. Do not cite.",
        html_url="https://github.com/docxology/template-release-smoke/releases/tag/v0.4.0-release-smoke",
        published_at="2026-05-27T17:08:23Z",
        assets=[],
    )
    assert is_ignored_release(release)


def test_biology_textbook_is_strong_pair_from_shared_doi():
    release = GitHubRelease(
        owner="docxology",
        repo="biology_textbook",
        tag="v1.0.0",
        name="Introduction to Biology v1.0.0 (Instructor Edition)",
        body=(
            "Reserved Zenodo DOI: [10.5281/zenodo.20286478]"
            "(https://doi.org/10.5281/zenodo.20286478)\n"
            "Source: https://github.com/docxology/biology_textbook\n"
            "PDF SHA-256: `79fe889ab05dc92c4580f8b1701fea12716a221045ddf9adc72a711f4f297f7e`"
        ),
        html_url="https://github.com/docxology/biology_textbook/releases/tag/v1.0.0",
        published_at="2026-05-26T14:26:32Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="20286478",
        doi="10.5281/zenodo.20286478",
        title="Introduction to Biology: A Generative Approach",
        publication_date="2026-05-26",
        version="1.0.0",
        resource_type={"type": "publication", "subtype": "book", "title": "Book"},
        creators=[{"name": "Friedman, Daniel Ari", "orcid": "0000-0001-6232-9096"}],
        description="Open biology textbook.",
        keywords=["Biology", "Open textbook"],
        related_identifiers=[],
        files=[],
        html_url="https://zenodo.org/records/20286478",
    )

    pair = confidence_for_pair(release, record)

    assert pair is not None
    assert pair.confidence == "strong"
    assert "github_release_mentions_doi" in pair.evidence
    assert pair.github_repo == "docxology/biology_textbook"


def test_template_cross_linked_release_is_strong_pair():
    release_url = "https://github.com/docxology/template_code_project/releases/tag/v2.2.0"
    release = GitHubRelease(
        owner="docxology",
        repo="template_code_project",
        tag="v2.2.0",
        name="Convergence Analysis of Gradient Descent Optimization (v2.2.0)",
        body=(
            "DOI: https://doi.org/10.5281/zenodo.20416565\n"
            "Zenodo: https://zenodo.org/records/20416565\n"
            f"GitHub release: {release_url}\n"
        ),
        html_url=release_url,
        published_at="2026-05-27T18:08:53Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="20416565",
        doi="10.5281/zenodo.20416565",
        title="Convergence Analysis of Gradient Descent Optimization",
        publication_date="2026",
        version="2.2",
        resource_type={"type": "publication", "title": "Publication"},
        creators=[{"name": "Research Template Author"}],
        description="Convergence study.",
        keywords=["gradient descent"],
        related_identifiers=[
            {"identifier": release_url, "relation": "isSupplementTo", "resource_type": "software"}
        ],
        files=[],
        html_url="https://zenodo.org/records/20416565",
    )

    pairs = find_publication_pairs([release], [record])

    assert len(pairs) == 1
    assert pairs[0].confidence == "strong"
    assert "zenodo_related_identifier_mentions_release" in pairs[0].evidence


def test_unlinked_title_only_match_needs_review():
    release = GitHubRelease(
        owner="docxology",
        repo="crescent-city",
        tag="v0.2.0",
        name="Crescent City in Living Waves",
        body="No DOI here.",
        html_url="https://github.com/docxology/crescent-city/releases/tag/v0.2.0",
        published_at="2026-03-18T17:52:41Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="20286171",
        doi="10.5281/zenodo.20286171",
        title="Crescent City in Living Waves: Space, Time, People, and Minds on the Southern Cascadian Coast",
        publication_date="2026-05-26",
        version="1.0.0",
        resource_type={"type": "publication", "title": "Publication"},
        creators=[{"name": "Friedman, Daniel Ari", "orcid": "0000-0001-6232-9096"}],
        description="Crescent City manuscript.",
        keywords=[],
        related_identifiers=[],
        files=[],
        html_url="https://zenodo.org/records/20286171",
    )

    pair = confidence_for_pair(release, record)

    assert pair is not None
    assert pair.confidence == "needs_review"


def test_release_self_repo_link_alone_does_not_create_pair():
    release = GitHubRelease(
        owner="docxology",
        repo="biology_textbook",
        tag="v1.0.0",
        name="Introduction to Biology v1.0.0",
        body="Source: https://github.com/docxology/biology_textbook",
        html_url="https://github.com/docxology/biology_textbook/releases/tag/v1.0.0",
        published_at="2026-05-26T14:26:32Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="13999298",
        doi="10.5281/zenodo.13999298",
        title="MVEE: A Framework for Evolutionary Studies",
        publication_date="2018",
        version=None,
        resource_type={"type": "publication"},
        creators=[],
        description="Unrelated record.",
        keywords=[],
        related_identifiers=[],
        files=[],
        html_url="https://zenodo.org/records/13999298",
    )

    assert confidence_for_pair(release, record) is None
