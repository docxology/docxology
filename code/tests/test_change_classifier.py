"""Tests for the settle-driver change classifier (code/src/change_classifier.py)."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from change_classifier import Classification, classify_paths  # noqa: E402
from release_controls import CONTROL_FILES  # noqa: E402

_FAST_TIERS = frozenset({"fast"})
_FULL_TIERS = frozenset({"fast", "full"})


def _expected(
    payload: tuple[str, ...] = (),
    control: tuple[str, ...] = (),
    surfaces: Iterable[str] = frozenset(),
    tiers: Iterable[str] = _FAST_TIERS,
) -> Classification:
    return Classification(
        payload_paths=payload,
        control_paths=control,
        tiers=frozenset(tiers),
        surfaces=frozenset(surfaces),
    )


_CASES: list[tuple[str, tuple[str, ...], Classification]] = [
    ("empty-input", (), _expected()),
    (
        "reports-datestamped-receipt",
        ("reports/asset_size_2026-09-01.json",),
        _expected(
            control=("reports/asset_size_2026-09-01.json",),
            surfaces={"reports"},
        ),
    ),
    (
        "reports-prefix-beats-papers",
        ("reports/papers/2026-01-01.json",),
        _expected(
            payload=("reports/papers/2026-01-01.json",),
            surfaces={"reports"},
        ),
    ),
    (
        "docs-directory",
        ("docs/seo/gsc-followup.md",),
        _expected(payload=("docs/seo/gsc-followup.md",), surfaces={"docs"}),
    ),
    (
        "root-readme",
        ("README.md",),
        _expected(payload=("README.md",), surfaces={"docs"}),
    ),
    (
        "reports-and-docs-only",
        ("reports/asset_size_2026-09-01.json", "docs/seo/gsc-followup.md", "README.md"),
        _expected(
            payload=("docs/seo/gsc-followup.md", "README.md"),
            control=("reports/asset_size_2026-09-01.json",),
            surfaces={"reports", "docs"},
        ),
    ),
    (
        "dated-receipt-md-variant",
        ("reports/public_source_review_2026-09-09.md",),
        _expected(
            control=("reports/public_source_review_2026-09-09.md",),
            surfaces={"reports"},
        ),
    ),
    (
        "reports-non-receipts-stay-payload",
        (
            "reports/asset_size_2026-13-45.json",
            "reports/asset_size_2026-09-01.yml",
            "reports/release_integrity_2026-09-01.json",
            "reports/notes.md",
        ),
        _expected(
            payload=(
                "reports/asset_size_2026-13-45.json",
                "reports/asset_size_2026-09-01.yml",
                "reports/release_integrity_2026-09-01.json",
                "reports/notes.md",
            ),
            surfaces={"reports"},
        ),
    ),
    (
        "nested-reports-cannot-impersonate",
        ("untrusted/reports/asset_size_2026-09-11.json",),
        _expected(
            payload=("untrusted/reports/asset_size_2026-09-11.json",),
            surfaces={"other"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "site-data-prefix",
        ("data/works.json",),
        _expected(payload=("data/works.json",), surfaces={"site"}, tiers=_FULL_TIERS),
    ),
    (
        "site-prefixes",
        (
            "data/works.json",
            "works/2026/essay.md",
            "papers/10.1234/paper.pdf",
            "pages/index.html",
            "feeds/updates.xml",
        ),
        _expected(
            payload=(
                "data/works.json",
                "works/2026/essay.md",
                "papers/10.1234/paper.pdf",
                "pages/index.html",
                "feeds/updates.xml",
            ),
            surfaces={"site"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "site-root-files",
        (
            "publications.html",
            "publications.html.js",
            "search-index.json",
            "sitemap.xml",
            "llms.txt",
            "agent-index.json",
        ),
        _expected(
            payload=(
                "publications.html",
                "publications.html.js",
                "search-index.json",
                "sitemap.xml",
                "llms.txt",
                "agent-index.json",
            ),
            surfaces={"site"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "code-src",
        ("code/src/report_paths.py",),
        _expected(
            payload=("code/src/report_paths.py",),
            surfaces={"code"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "code-orchestrators",
        ("code/orchestrators/regenerate_all.py",),
        _expected(
            payload=("code/orchestrators/regenerate_all.py",),
            surfaces={"code"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "tests-directory",
        ("code/tests/test_report_paths.py",),
        _expected(
            payload=("code/tests/test_report_paths.py",),
            surfaces={"tests"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "ci-workflow",
        (".github/workflows/deploy-pages.yml",),
        _expected(
            payload=(".github/workflows/deploy-pages.yml",),
            surfaces={"ci"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "unknown-extensions",
        ("assets/og-image.jpg", "LICENSE", "style.css", "codemeta.json"),
        _expected(
            payload=("assets/og-image.jpg", "LICENSE", "style.css", "codemeta.json"),
            surfaces={"other"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "nested-root-lookalikes",
        ("sub/search-index.json", "subdir/README.md", "notes/publications.html"),
        _expected(
            payload=(
                "sub/search-index.json",
                "subdir/README.md",
                "notes/publications.html",
            ),
            surfaces={"other"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "control-generated-md",
        ("GENERATED.md",),
        _expected(control=("GENERATED.md",), surfaces={"docs"}),
    ),
    (
        "control-agent-index",
        ("data/agent-index.json",),
        _expected(
            control=("data/agent-index.json",),
            surfaces={"site"},
            tiers=_FULL_TIERS,
        ),
    ),
    (
        "mixed-payload-and-control",
        (
            "data/works.json",
            "data/agent-index.json",
            "code/src/app.py",
            "GENERATED.md",
        ),
        _expected(
            payload=("data/works.json", "code/src/app.py"),
            control=("data/agent-index.json", "GENERATED.md"),
            surfaces={"site", "code", "docs"},
            tiers=_FULL_TIERS,
        ),
    ),
]


_TABLE = [(paths, expected) for _, paths, expected in _CASES]
_LABELS = [label for label, _, _ in _CASES]


@pytest.mark.parametrize(("paths", "expected"), _TABLE, ids=_LABELS)
def test_classify_paths_table(
    paths: tuple[str, ...], expected: Classification
) -> None:
    result = classify_paths(paths)
    assert result == expected
    assert "release" not in result.tiers


def test_classify_paths_accepts_any_iterable() -> None:
    result = classify_paths(iter(("reports/a.json", "data/b.json")))
    assert result.payload_paths == ("reports/a.json", "data/b.json")
    assert result.surfaces == frozenset({"reports", "site"})


def test_every_control_file_classifies_as_control() -> None:
    control_names = {path.as_posix() for path in CONTROL_FILES}
    result = classify_paths(sorted(control_names))
    assert result.payload_paths == ()
    assert set(result.control_paths) == control_names
    # GENERATED.md maps to docs; the data/* receipts map to site.
    assert result.surfaces == frozenset({"docs", "site"})
    assert result.tiers == _FULL_TIERS


def test_root_lookalikes_of_control_files_stay_payload() -> None:
    result = classify_paths(("agent-index.json", "generated-manifest.json"))
    assert result.payload_paths == ("agent-index.json", "generated-manifest.json")
    assert result.control_paths == ()


def test_dated_control_receipts_classify_as_control() -> None:
    dated = (
        "reports/asset_size_2026-09-01.json",
        "reports/pages_artifact_growth_2026-09-01.json",
        "reports/public_source_review_2026-09-01.json",
        "reports/public_source_review_2026-09-01.md",
    )
    result = classify_paths(dated)
    assert result.payload_paths == ()
    assert result.control_paths == dated
    assert result.surfaces == frozenset({"reports"})
    assert result.tiers == _FAST_TIERS
