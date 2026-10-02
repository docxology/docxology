"""Regression tests for the ordered local regeneration pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


import regenerate_all  # noqa: E402


def test_integrity_tail_resolves_generated_manifest_before_agent_index():
    names = [name for name, _args in regenerate_all.CHAIN]
    generated_manifest_indices = [i for i, name in enumerate(names) if name == "build_generated_manifest.py"]

    assert names.count("build_agent_index.py") == 1
    assert len(generated_manifest_indices) == 2
    # build_image_sitemap.py removed (NEW-2, 2026-08-28): artwork index remains.
    assert "build_image_sitemap.py" not in names
    docs_index = names.index("regenerate_docs.py")
    assert docs_index < names.index("export_bibliography.py", docs_index + 1) < names.index("sync_publications_html.py", docs_index + 1) < names.index("build_work_pages.py")
    assert names.index("generate_redirect_stubs.py") < names.index("deploy_seo_security.py")
    assert names.index("build_pages_artifact.py") < names.index("build_agent_index.py")
    assert names.index("build_pages_artifact.py") < generated_manifest_indices[0] < names.index("build_agent_index.py")
    assert names.index("build_agent_index.py") < names.index("build_release_integrity.py") < generated_manifest_indices[1]
    assert names[-1] == "build_generated_manifest.py"
    site_facts_indices = [i for i, name in enumerate(names) if name == "sync_site_facts.py"]
    accessibility_indices = [i for i, name in enumerate(names) if name == "accessibility_audit.py"]
    assert len(site_facts_indices) >= 2
    assert site_facts_indices[-1] > accessibility_indices[-1]


def test_default_two_passes_refresh_an_early_consumer_after_a_late_producer(tmp_path):
    """Exercise the known cross-pass boundary without touching site outputs."""
    from docxology_tools.generation_plan import GenerationStep

    data = tmp_path / "data"
    data.mkdir()
    source = data / "source.json"
    projection = data / "projection.json"
    consumer = data / "consumer.json"
    source.write_text("new\n")
    projection.write_text("old\n")
    for relative in (
        "code/orchestrators/consumer.py", "code/orchestrators/producer.py", "code/src/site_nav.py",
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fixture source\n")
    steps = (
        GenerationStep("consumer", "consumer.py", (), ("--check",), "early consumer",
                       ("data/projection.json",)),
        GenerationStep("producer", "producer.py", (), ("--check",), "late producer",
                       ("data/source.json",)),
    )

    def runner(script, _args):
        if script == "consumer.py":
            consumer.write_text(projection.read_text())
        else:
            projection.write_text(source.read_text())

    ran, skipped = regenerate_all.run_regeneration_passes(
        steps=steps, repo_root=tmp_path, runner=runner, emit=lambda _message: None,
    )

    assert consumer.read_text() == "new\n"
    assert (ran, skipped) == (3, 1)
    assert regenerate_all.run_regeneration_passes(
        steps=steps, repo_root=tmp_path, runner=runner, emit=lambda _message: None,
    ) == (0, 4)


def test_regeneration_failure_stops_before_another_pass(tmp_path):
    from docxology_tools.generation_plan import GenerationStep

    steps = (GenerationStep("fixture", "fixture.py", (), ("--check",), "fixture"),)
    calls = []

    def runner(script, _args):
        calls.append(script)
        raise RuntimeError("writer failed")

    with pytest.raises(RuntimeError, match="writer failed"):
        regenerate_all.run_regeneration_passes(
            steps=steps, repo_root=tmp_path, runner=runner, emit=lambda _message: None,
        )
    assert calls == ["fixture.py"]


@pytest.mark.parametrize("passes", [0, 5])
def test_regeneration_pass_bound_is_enforced(passes):
    with pytest.raises(ValueError, match="between 1 and 4"):
        regenerate_all.run_regeneration_passes(passes=passes, steps=())
