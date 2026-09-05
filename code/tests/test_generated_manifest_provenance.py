"""Ensure generator manifests disclose inputs that affect rendered output."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_generated_manifest  # noqa: E402


def _artifact(name: str) -> dict:
    return next(item for item in build_generated_manifest.ARTIFACTS if item["name"] == name)


def test_manifest_declares_count_paper_availability_and_repository_inventory_inputs():
    publications = _artifact("Publications HTML sync")
    bibliography = _artifact("Bibliography exports")
    software = _artifact("Software catalog HTML sync")
    routes = _artifact("Agent route manifest")
    counts = _artifact("Current count report")

    assert {
        "data/current-counts.json",
        "papers/*/README.md",
        "papers/*/AGENTS.md",
        "papers/*/SKILL.md",
        "papers/*/full_text.md",
        "papers/*/images/",
    }.issubset(publications["sources"])
    assert {
        "papers/*/README.md",
        "papers/*/AGENTS.md",
        "papers/*/SKILL.md",
        "papers/*/full_text.md",
        "papers/*/images/",
    }.issubset(bibliography["sources"])
    assert "data/github-repositories.json" in software["sources"]
    assert "data/github-repositories.json" in routes["sources"]
    assert {"papers/*/full_text.md", "papers/*/images/*"}.issubset(counts["sources"])


def test_browser_qa_manifest_uses_the_portable_uv_optional_group_command():
    browser_qa = _artifact("Progressive browser QA")
    assert browser_qa["command"] == "uv run --extra browser-qa python3 code/orchestrators/browser_qa.py"


def test_every_declared_generator_script_still_exists():
    """GENERATED.md is the rebuild matrix; a row for a deleted script is a trap.

    `build_image_sitemap.py` was removed on 2026-08-28, but its manifest row
    survived and kept publishing a rebuild command — and an output file — that
    an agent following GENERATED.md would run and never produce.
    """
    referenced: set[str] = set()
    for artifact in build_generated_manifest.ARTIFACTS:
        for source in artifact["sources"]:
            if source.startswith("code/") and source.endswith(".py"):
                referenced.add(source)
        for token in str(artifact["command"]).split():
            if token.startswith("code/") and token.endswith(".py"):
                referenced.add(token)
    assert referenced, "no generator scripts are declared in the manifest"
    missing = sorted(rel for rel in referenced if not (REPO_ROOT / rel).is_file())
    assert missing == [], f"generated manifest names scripts that do not exist: {missing}"
