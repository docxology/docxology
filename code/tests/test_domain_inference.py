"""Tests for canonical whole-word domain inference."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC_DIR))

from domain_inference import (  # noqa: E402
    contains_term,
    infer_domain_emoji,
    infer_domain_emoji_zenodo,
    infer_domain_name,
)
from publication_pairing import (  # noqa: E402
    GitHubRelease,
    PublicationPair,
    ZenodoRecord,
    infer_domain,
)


def test_substring_false_positives_dominant_and_smart():
    # "dominant" contains "ant" and "smart" contains "art"; neither should trigger
    # entomology/art domain tags without a genuine whole-word match.
    blob = (
        "The dominant lever is which rule forms the panel, not its size; "
        "a smart selection rule recovers best under a fully deterministic instrument."
    )
    assert not contains_term(blob.lower(), "ant")
    assert not contains_term(blob.lower(), "art")
    assert infer_domain_emoji(blob) is None


def test_whole_word_entomology_ant_colony():
    assert infer_domain_emoji("A study of ant colony foraging behavior.") == "🐜"


def test_computational_beats_entomology_when_both_present():
    blob = "A computational pipeline for ant colony foraging."
    assert infer_domain_emoji(blob) == "💻"


def test_infer_domain_name_maps_emoji_bib_domain():
    assert infer_domain_name(bib_entry={"domain": "🐜"}) == "Entomology"
    assert infer_domain_name(bib_entry={"domain": "🎨"}) == "Art & Synergetics"
    assert infer_domain_name(meta={"domain": "Art"}) == "Art & Synergetics"


def test_infer_domain_name_default_research():
    assert infer_domain_name("unrelated waffle about panels") == "Research"


def test_publication_pairing_reexports_infer_domain():
    release = GitHubRelease(
        owner="docxology",
        repo="probe",
        tag="v0.1.0",
        name="probe v0.1.0",
        body="DOI: https://doi.org/10.5281/zenodo.1",
        html_url="https://github.com/docxology/probe/releases/tag/v0.1.0",
        published_at="2026-06-25T00:00:00Z",
        assets=[],
    )
    record = ZenodoRecord(
        record_id="1",
        doi="10.5281/zenodo.1",
        title="Ant Foraging Behavior",
        publication_date="2026-06-25",
        version="0.1.0",
        resource_type={"type": "publication", "title": "Publication"},
        creators=[{"name": "Friedman, Daniel Ari"}],
        description="A study of ant colony foraging behavior.",
        keywords=["entomology"],
        related_identifiers=[],
        files=[],
        html_url="https://zenodo.org/records/1",
    )
    pair = PublicationPair(release=release, record=record, confidence="strong", evidence=())
    assert infer_domain(pair) == "🐜"


def test_zenodo_unknown_defaults_to_active_inference():
    assert infer_domain_emoji_zenodo("no matching keywords here") == "🧠"
