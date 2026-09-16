"""Skip-on-unchanged gating for the plan-wide input-declared steps.

Beyond the original audit/paper gates, every render step in the plan now
declares its curated source inputs, so the write driver can skip it when
those inputs hash unchanged. These tests pin that behavior for the newly
gated steps: unchanged inputs skip, a changed input reruns, and steps
without declared inputs — or with unmatched/empty input sets — always run
(the conservative failsafe). ``validate_repo`` never consults this state and
stays the ungated authority; the skip mechanics themselves are pinned by
``test_regeneration_skips.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: F401,E402  (canonical bootstrap: code/src + code/orchestrators onto sys.path)
import regenerate_all  # noqa: E402
from docxology_tools.generation_plan import (  # noqa: E402
    LOCAL_GENERATION_STEPS,
    GenerationStep,
    load_regeneration_state,
    step_skip_reason,
)
from docxology_tools.release_controls import is_control_path  # noqa: E402

STEPS: dict[str, GenerationStep] = {step.identifier: step for step in LOCAL_GENERATION_STEPS}

# Steps classified DERIVED in the plan: always-run, no declared inputs, each
# with a one-line reason in the plan comment. Keep this set in sync — a new
# unclassified always-run step must either declare inputs or join this list.
DERIVED_STEPS = {
    # Cross-pass cycle: reads the data/software.json projection that agent-data
    # rewrites later in the same pass while agent-data reads its own output.
    "current-counts",
    "repository-classification",
    # Reads data/work-enrichment.json, rewritten later in the same pass by
    # work-pages (documented fixed-point two-pass design).
    "domain-pages",
    # In-place patchers: read scope equals write scope, several surfaces
    # hand-authored.
    "scholar-metrics",
    "citation-cff",
    "site-facts-first",
    "site-facts-final",
    "seo-security",
    "agent-navigation",
    # Git-derived state no content fingerprint captures.
    "sitemap",
    "release-integrity",
    # Renderers with no repository-file inputs (in-script tables/templates).
    "pillar-pages",
    "redirect-stubs",
    "404-page",
    "pages-artifact",
    "generated-manifest-first",
    "generated-manifest-final",
}


def _seed_pattern(repo_root: Path, pattern: str) -> Path:
    """Create one file matched by ``pattern`` in a disposable repo."""
    literal = pattern.replace("[0-9]*", "2026-01-01")
    parts = []
    for segment in Path(literal).parts:
        if segment in ("*", "**"):
            segment = "fixture"
        elif "*" in segment:
            segment = segment.replace("*", "fixture")
        parts.append(segment)
    path = repo_root.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"seed: {pattern}\n", encoding="utf-8")
    assert any(candidate.is_file() for candidate in repo_root.glob(pattern)), (
        f"seeded {path.relative_to(repo_root)} does not match pattern {pattern!r}"
    )
    return path


def _seed_inputs(repo_root: Path, step: GenerationStep) -> list[Path]:
    return [_seed_pattern(repo_root, pattern) for pattern in step.inputs]


def _run(step: GenerationStep, repo_root: Path, calls: list[str]) -> tuple[int, int]:
    def runner(script: str, args: list[str]) -> None:
        calls.append(script)

    return regenerate_all.run_regeneration(
        steps=(step,),
        runner=runner,
        repo_root=repo_root,
        emit=lambda _message: None,
    )


def test_newly_gated_step_skips_then_reruns_on_changed_input(tmp_path: Path) -> None:
    step = STEPS["updates-page"]
    changelog = _seed_pattern(tmp_path, "CHANGELOG.md")
    calls: list[str] = []

    assert _run(step, tmp_path, calls) == (1, 0)
    assert load_regeneration_state(tmp_path).get("updates-page")

    # Unchanged curated input: the second lap skips the step.
    assert _run(step, tmp_path, calls) == (0, 1)

    # A content change to the declared input flips the step back to run.
    changelog.write_text("## 2026-09-16\n- intake\n", encoding="utf-8")
    assert _run(step, tmp_path, calls) == (1, 0)
    assert len(calls) == 2


def test_steps_without_declared_inputs_always_run(tmp_path: Path) -> None:
    for identifier in ("current-counts", "redirect-stubs", "pages-artifact"):
        step = STEPS[identifier]
        assert step.inputs == ()
        calls: list[str] = []
        # Even a persisted entry cannot make an input-less step skip.
        assert step_skip_reason(step, {identifier: "stale"}, tmp_path) is None
        assert _run(step, tmp_path, calls) == (1, 0)
        assert calls == [step.script]


def test_unmatched_declared_inputs_never_skip(tmp_path: Path) -> None:
    """Empty tree under a declared pattern: fingerprint is None, step runs."""
    step = STEPS["og-images"]
    calls: list[str] = []
    # No data/current-counts.json exists in this repo: the failsafe keeps the
    # step running on every lap instead of trusting a vacuous fingerprint.
    assert _run(step, tmp_path, calls) == (1, 0)
    assert _run(step, tmp_path, calls) == (1, 0)
    assert calls == ["generate_og_images.py", "generate_og_images.py"]


def test_every_declared_input_pattern_is_real_and_skip_eligible(tmp_path: Path) -> None:
    """Each gated step skips on unchanged inputs in a minimal fixture repo.

    Seeding one file per declared pattern proves the globs are not typos (a
    pattern that can never match would silently disable skipping forever via
    the fingerprint-None failsafe) and that every gated step participates in
    the skip machinery end to end.
    """
    for step in LOCAL_GENERATION_STEPS:
        if not step.inputs:
            continue
        repo = tmp_path / step.identifier
        repo.mkdir()
        seeded = _seed_inputs(repo, step)
        calls: list[str] = []
        assert _run(step, repo, calls) == (1, 0), step.identifier
        assert _run(step, repo, calls) == (0, 1), step.identifier
        seeded[0].write_text("changed\n", encoding="utf-8")
        assert _run(step, repo, calls) == (1, 0), step.identifier


def test_derived_steps_are_exactly_the_documented_always_run_set() -> None:
    ungated = sorted(step.identifier for step in LOCAL_GENERATION_STEPS if not step.inputs)
    assert ungated == sorted(DERIVED_STEPS)


def test_catalog_and_search_index_outputs_classify_as_payload() -> None:
    """The folded-in catalog/search-index steps write payload, not control.

    Grounds the is_control_path note recorded on the two plan steps: their
    outputs are served artifacts, unlike GENERATED.md, the four tail
    manifests, and the dated control receipts.
    """
    payload_paths = (
        "data/catalog.json",
        "catalog.html",
        "search-index.json",
        "search-index-core.json",
        "search-index-content-work.json",
        "search-index-content-video.json",
    )
    assert not any(is_control_path(Path(relative)) for relative in payload_paths)
    # The contrast that makes the classification meaningful:
    assert is_control_path(Path("data/agent-index.json"))
    assert is_control_path(Path("reports/asset_size_2026-01-01.json"))


def test_catalog_and_search_index_are_input_gated_plan_steps() -> None:
    catalog = STEPS["catalog"]
    search_index = STEPS["search-index"]
    assert catalog.identifier == "catalog" and catalog.script == "build_catalog.py"
    assert search_index.identifier == "search-index" and search_index.script == "build_search_index.py"
    assert catalog.inputs, "catalog must declare source inputs to be skippable"
    assert search_index.inputs, "search-index must declare source inputs to be skippable"
    # Catalog consumes the dataset exports (works/software/videos) and the
    # search index the works export, so a data intake refreshes both without
    # a manual invocation.
    assert "data/works.json" in catalog.inputs
    assert "data/works.json" in search_index.inputs
