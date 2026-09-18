"""Tests for release-integrity deployment status semantics."""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


import build_release_integrity as bri  # noqa: E402


def test_matching_built_deployment_is_not_pending():
    assert bri.deployment_pending_reasons(
        "abc123",
        {"commit": "abc123", "pages_status": "built", "verification_overall_ok": True},
        deployed_content_differs=False,
    ) == []


def test_mismatched_deployment_is_explicitly_pending():
    reasons = bri.deployment_pending_reasons(
        "current",
        {"commit": "deployed", "pages_status": "built", "verification_overall_ok": True},
        deployed_content_differs=True,
    )
    assert reasons == ["tracked release content differs from the deployed commit"]


def test_incomplete_live_evidence_is_explicitly_pending():
    reasons = bri.deployment_pending_reasons(
        "current",
        {"commit": "current", "pages_status": "building", "verification_overall_ok": False},
        deployed_content_differs=False,
    )
    assert reasons == ["Pages status is building", "live verification is not passing"]


def test_preserved_local_site_output_does_not_count_as_a_release_change():
    assert not bri.has_release_changes("?? _site/")
    assert not bri.has_release_changes('?? "_site/art/name with spaces.json"')
    assert bri.has_release_changes(" M SKILL.md\n?? reports/live.json")


def test_release_envelope_rejects_a_stale_pages_source_commit() -> None:
    """A stale Pages SHA cannot be reused to mint a fresh integrity envelope."""
    try:
        bri.build_pages_artifact.validate_source_commit_at_generation(
            "old-source-commit",
            expected_source_commit="current-source-commit",
            manifest_path=Path("data/pages-artifact-manifest.json"),
        )
    except SystemExit as exc:
        assert "source_commit_at_generation" in str(exc)
    else:  # pragma: no cover - regression guard
        raise AssertionError("stale source revision was accepted")
