"""The write pipeline and no-write gate must share one complete plan."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from generation_plan import (  # noqa: E402
    EXCLUDED_OPERATIONS,
    LOCAL_GENERATION_STEPS,
    GenerationStep,
    coverage_errors,
)
import regenerate_all  # noqa: E402


def test_every_local_writer_has_a_non_writing_check_and_drives_regenerate_all():
    assert coverage_errors() == []
    assert regenerate_all.CHAIN == [
        (step.script, list(step.write_args)) for step in LOCAL_GENERATION_STEPS
    ]
    assert any(step.script == "regenerate_docs.py" for step in LOCAL_GENERATION_STEPS)
    assert any(step.script == "generate_pillar_pages.py" for step in LOCAL_GENERATION_STEPS)


def test_coverage_check_rejects_a_writer_without_a_check_fixture(tmp_path):
    fixture = tmp_path / "fixture.py"
    fixture.write_text("# fixture\n", encoding="utf-8")
    incomplete = GenerationStep("fixture", "fixture.py", (), (), "negative fixture")
    assert coverage_errors((incomplete,), (), tmp_path) == ["fixture: missing no-write check arguments"]


def test_coverage_check_rejects_an_unclassified_writer(tmp_path):
    (tmp_path / "unclassified.py").write_text(
        'from pathlib import Path\nPath("output.txt").write_text("x")\n',
        encoding="utf-8",
    )

    assert coverage_errors((), (), tmp_path) == [
        "unclassified write-capable orchestrators: unclassified.py"
    ]


def test_coverage_check_detects_an_open_write_bypass(tmp_path):
    (tmp_path / "open_writer.py").write_text(
        'with open("output.txt", "w", encoding="utf-8") as handle:\n    handle.write("x")\n',
        encoding="utf-8",
    )

    assert coverage_errors((), (), tmp_path) == [
        "unclassified write-capable orchestrators: open_writer.py"
    ]


def test_coverage_check_detects_a_path_open_write_bypass(tmp_path):
    (tmp_path / "path_open_writer.py").write_text(
        'Path("output.txt").open("w", encoding="utf-8")\n',
        encoding="utf-8",
    )

    assert coverage_errors((), (), tmp_path) == [
        "unclassified write-capable orchestrators: path_open_writer.py"
    ]


def test_network_manual_and_destructive_operations_are_explicitly_excluded():
    categories = {entry.script: entry.category for entry in EXCLUDED_OPERATIONS}
    assert categories["prune_old_reports.py"] == "destructive/manual-review"
    assert categories["refresh_public_sources.py"] == "network"
    assert categories["verify_live_site.py"] == "network/post-deploy"
    assert categories["fetch_youtube_data.py"] == "network/cache-refresh/manual-review"
    assert categories["batch_enrich_metadata.py"] == "source-authoring/manual-review"
    assert categories["improve_metadata_quality.py"] == "source-authoring/manual-review"
