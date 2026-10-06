"""Behavior tests for the drift-comparison step of .github/workflows/freshness.yml.

The workflow decides whether to open a "freshness drift" issue from one shell
step (`id: diff`) that normalizes two facts documents with jq and compares them.
That logic lives in YAML, so a unit test of `refresh_public_sources` cannot see
it. These tests parse the real workflow file, take the step's `run` script
verbatim, and execute it with bash inside a tmp_path that mirrors the repository
layout the script expects (`reports/...`), with `GITHUB_OUTPUT` pointed at a temp
file exactly as the Actions runner does.

Skipped, not failed, when bash or the coreutils/jq the script shells out to are
unavailable (the CI runner and a developer macOS box both have them).
"""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "freshness.yml"

# Every executable the compare step calls; a missing one would fail the script
# for a reason unrelated to the logic under test.
REQUIRED_TOOLS = ("bash", "jq", "cmp", "diff", "sort", "tail", "printf")
_MISSING_TOOLS = [tool for tool in REQUIRED_TOOLS if shutil.which(tool) is None]
pytestmark = pytest.mark.skipif(
    bool(_MISSING_TOOLS),
    reason=f"freshness compare step needs {', '.join(REQUIRED_TOOLS)}; not on PATH: {', '.join(_MISSING_TOOLS)}",
)

LATEST_FACTS = "reports/public_source_snapshot_latest.facts.json"


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _steps() -> list[dict]:
    return _workflow()["jobs"]["freshness"]["steps"]


def _step_by_id(step_id: str) -> dict:
    matches = [step for step in _steps() if step.get("id") == step_id]
    assert len(matches) == 1, f"expected exactly one step with id {step_id!r} in {WORKFLOW.name}"
    return matches[0]


def compare_script() -> str:
    """The `run` body of the compare step, byte-for-byte as the runner would execute it."""
    script = _step_by_id("diff")["run"]
    assert isinstance(script, str) and script.strip()
    # The runner expands ${{ ... }} before bash sees the script; this harness does not,
    # so an expression would run as literal text and silently test something else.
    assert "${{" not in script, "compare step uses a workflow expression; extend this harness to substitute it"
    return script


# --- fixtures -----------------------------------------------------------------

BASE_FACTS: dict = {
    "GitHub user docxology": {
        "login": "docxology",
        "type": "User",
        "public_repos": 231,
        "updated_at": "2026-09-30T04:00:00Z",
        "html_url": "https://github.com/docxology",
    },
    "GitHub user ActiveInferenceInstitute": {
        "login": "ActiveInferenceInstitute",
        "type": "Organization",
        "public_repos": 45,
        "updated_at": "2026-09-22T19:05:32Z",
        "html_url": "https://github.com/ActiveInferenceInstitute",
    },
    "ORCID work groups": {"group_count": 120},
    "Zenodo exact-name creator records": {
        "total": 31,
        "first_title": "Newest deposit",
        "first_doi": "10.5281/zenodo.1000001",
    },
    "Zenodo record 18686966": {
        "title": "Journal-Utilities",
        "doi": "10.5281/zenodo.18686966",
        "publication_date": "2026-02-24",
        "resource_type": "Software",
        "creators": ["Friedman, Daniel Ari"],
    },
    "GitHub repo ActiveInferenceInstitute/fep_lean": {
        "full_name": "ActiveInferenceInstitute/fep_lean",
        "stargazers_count": 3,
        "language": "Lean",
        "updated_at": "2026-09-01T00:00:00Z",
        "html_url": "https://github.com/ActiveInferenceInstitute/fep_lean",
    },
}


@dataclass
class CompareResult:
    returncode: int
    outputs: dict[str, str]
    output_lines: list[str]
    stdout: str
    stderr: str


def _write_json(path: Path, payload: object, *, sort_keys: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=sort_keys, ensure_ascii=False) + "\n", encoding="utf-8")


def write_baseline(root: Path, facts: dict, date: str = "2026-09-30") -> Path:
    """A dated, checked-in snapshot: facts wrapped in the full report envelope."""
    path = root / "reports" / f"public_source_snapshot_{date}.json"
    _write_json(path, {"generated_at": f"{date}T04:00:00+00:00", "facts": facts, "checks": []})
    return path


def write_latest(root: Path, facts: dict) -> Path:
    """The freshly generated facts, bare and key-sorted, as `--facts-output` writes them."""
    path = root / LATEST_FACTS
    _write_json(path, facts, sort_keys=True)
    return path


def _reverse_key_order(value: object) -> object:
    """Rebuild `value` with every object's keys in reverse insertion order (arrays keep their order)."""
    if isinstance(value, dict):
        return {key: _reverse_key_order(value[key]) for key in reversed(list(value))}
    if isinstance(value, list):
        return [_reverse_key_order(item) for item in value]
    return value


def write_latest_unsorted(root: Path, facts: dict) -> Path:
    """The freshly generated facts, bare but genuinely NOT key-sorted.

    `write_latest` mirrors what `--facts-output` writes today (key-sorted), so with it the
    latest side already arrives in canonical order and the compare step's `jq -S` on that
    side is never exercised: delete it and every test still passes. This helper writes the
    same facts with every object's keys in reverse insertion order, which is neither sorted
    order nor the baseline's order, so only a `-S` on BOTH jq calls makes the two normalized
    files byte-equal. The assertions guard the helper itself: they fail if a future edit makes
    the file sorted again, which would silently turn this back into a no-op.
    """
    path = root / LATEST_FACTS
    _write_json(path, _reverse_key_order(facts))
    written = json.loads(path.read_text(encoding="utf-8"))
    assert list(written) != sorted(written), "top-level keys must be unsorted for this helper to mean anything"
    assert any(list(inner) != sorted(inner) for inner in written.values() if isinstance(inner, dict)), (
        "nested keys must be unsorted too"
    )
    return path


def run_compare(root: Path, *, tmp_out: Path | None = None) -> CompareResult:
    """Execute the workflow's compare script in `root` the way the Actions runner does."""
    github_output = tmp_out or (root.parent / f"{root.name}.github_output")
    github_output.write_text("", encoding="utf-8")
    env = {**os.environ, "GITHUB_OUTPUT": str(github_output)}
    # `bash -e` is the runner's default shell for an unspecified `shell:` on Linux.
    proc = subprocess.run(
        ["bash", "-e", "-c", compare_script()],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    lines = [line for line in github_output.read_text(encoding="utf-8").splitlines() if line]
    outputs = dict(line.split("=", 1) for line in lines)
    return CompareResult(proc.returncode, outputs, lines, proc.stdout, proc.stderr)


def compare(root: Path, baseline: dict, latest: dict) -> CompareResult:
    write_baseline(root, baseline)
    write_latest(root, latest)
    return run_compare(root)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "reports").mkdir(parents=True)
    return repo


def _variant(mutate) -> dict:
    facts = copy.deepcopy(BASE_FACTS)
    mutate(facts)
    return facts


# --- the workflow file itself -------------------------------------------------


def test_compare_step_is_wired_to_the_files_the_refresh_step_writes():
    """The refresh step's --facts-output and the compare step's input path must be the same file."""
    refresh = next(step for step in _steps() if step.get("name") == "Refresh public-source snapshot")
    assert f"--facts-output {LATEST_FACTS}" in refresh["run"]
    assert LATEST_FACTS in compare_script()


def test_drift_issue_step_reads_the_compare_steps_changed_output():
    steps = _steps()
    ids = [step.get("id") for step in steps]
    issue = next(step for step in steps if step.get("name") == "Open drift issue")
    assert "steps.diff.outputs.changed == 'true'" in issue["if"]
    assert ids.index("diff") < steps.index(issue)


# --- no-drift cases -----------------------------------------------------------


def test_identical_facts_report_unchanged(root):
    result = compare(root, BASE_FACTS, BASE_FACTS)
    assert result.returncode == 0, result.stderr
    assert result.outputs["changed"] == "false"
    assert result.outputs["baseline"] == "reports/public_source_snapshot_2026-09-30.json"
    assert result.stdout.strip() == "", "no diff is printed when nothing moved"


def test_telemetry_only_changes_report_unchanged(root):
    """updated_at and stargazers_count move with ordinary activity, at any depth, and are not drift."""

    def churn(facts: dict) -> None:
        facts["GitHub user docxology"]["updated_at"] = "2026-10-06T09:30:00Z"
        facts["GitHub user ActiveInferenceInstitute"]["updated_at"] = "2026-10-05T18:00:00Z"
        facts["GitHub repo ActiveInferenceInstitute/fep_lean"]["stargazers_count"] = 9
        facts["GitHub repo ActiveInferenceInstitute/fep_lean"]["updated_at"] = "2026-10-06T00:00:00Z"

    result = compare(root, BASE_FACTS, _variant(churn))
    assert result.returncode == 0, result.stderr
    assert result.outputs["changed"] == "false"


def test_key_order_differences_are_not_drift(root):
    """Baseline in insertion order, latest in reversed (unsorted) order: `jq -S` on BOTH sides makes them equal.

    The latest facts are written unsorted on purpose (see `write_latest_unsorted`); with the usual
    key-sorted writer a missing `-S` on the latest side would go undetected.
    """
    write_baseline(root, BASE_FACTS)
    write_latest_unsorted(root, BASE_FACTS)
    result = run_compare(root)
    assert result.returncode == 0, result.stderr
    assert result.outputs["changed"] == "false"
    assert result.stdout.strip() == "", "no diff is printed when only key order differs"


def test_normalized_files_drop_only_the_telemetry_keys(root):
    compare(root, BASE_FACTS, BASE_FACTS)
    normalized = json.loads((root / "reports" / "public_source_snapshot_latest.facts.norm.json").read_text("utf-8"))
    user = normalized["GitHub user docxology"]
    assert "updated_at" not in user and "stargazers_count" not in user
    assert user["public_repos"] == 231 and user["type"] == "User"
    repo = normalized["GitHub repo ActiveInferenceInstitute/fep_lean"]
    assert "stargazers_count" not in repo and repo["language"] == "Lean"


# --- drift cases --------------------------------------------------------------


def _assert_drift(result: CompareResult, *needles: str) -> None:
    assert result.returncode == 0, f"the step must not fail when drift is found:\n{result.stderr}"
    assert result.outputs["changed"] == "true"
    assert result.outputs["baseline"] == "reports/public_source_snapshot_2026-09-30.json"
    assert result.stdout.startswith("--- reports/public_source_snapshot_baseline.facts.norm.json"), result.stdout
    for needle in needles:
        assert needle in result.stdout, f"{needle!r} missing from the logged diff:\n{result.stdout}"


def test_public_repo_count_change_reports_drift(root):
    result = compare(root, BASE_FACTS, _variant(
        lambda f: f["GitHub user ActiveInferenceInstitute"].__setitem__("public_repos", 46)
    ))
    _assert_drift(result, '-    "public_repos": 45', '+    "public_repos": 46')


def test_zenodo_first_doi_change_reports_drift(root):
    result = compare(root, BASE_FACTS, _variant(
        lambda f: f["Zenodo exact-name creator records"].__setitem__("first_doi", "10.5281/zenodo.1000002")
    ))
    _assert_drift(result, "10.5281/zenodo.1000001", "10.5281/zenodo.1000002")


def test_missing_label_reports_drift(root):
    """A check that failed to fetch drops its label from facts; that must read as drift, not as 'no change'."""
    result = compare(root, BASE_FACTS, _variant(lambda f: f.pop("Zenodo record 18686966")))
    _assert_drift(result, "Zenodo record 18686966")


def test_added_type_key_reports_drift(root):
    """A snapshot that first records the account `type` differs from one that never did."""
    baseline = _variant(lambda f: f["GitHub user ActiveInferenceInstitute"].pop("type"))
    result = compare(root, baseline, BASE_FACTS)
    _assert_drift(result, '+    "type": "Organization"')


def test_account_type_change_reports_drift(root):
    result = compare(root, BASE_FACTS, _variant(
        lambda f: f["GitHub user ActiveInferenceInstitute"].__setitem__("type", "User")
    ))
    _assert_drift(result, '-    "type": "Organization"', '+    "type": "User"')


def test_unsorted_latest_facts_still_report_a_real_change(root):
    """Sorting the unsorted latest side must not hide a genuine fact change."""
    changed = _variant(lambda f: f["GitHub user docxology"].__setitem__("public_repos", 232))
    write_baseline(root, BASE_FACTS)
    write_latest_unsorted(root, changed)
    result = run_compare(root)
    _assert_drift(result, '-    "public_repos": 231', '+    "public_repos": 232')


def test_new_label_reports_drift(root):
    result = compare(root, BASE_FACTS, _variant(lambda f: f.__setitem__("Zenodo record 99999999", {"title": "New"})))
    _assert_drift(result, "Zenodo record 99999999")


def test_telemetry_noise_does_not_mask_a_real_change(root):
    """Drift in one fact still reports when other facts also churned in telemetry-only ways."""

    def both(facts: dict) -> None:
        facts["GitHub repo ActiveInferenceInstitute/fep_lean"]["stargazers_count"] = 12
        facts["GitHub user docxology"]["public_repos"] = 232
        facts["GitHub user docxology"]["updated_at"] = "2026-10-06T00:00:00Z"

    result = compare(root, BASE_FACTS, _variant(both))
    _assert_drift(result, '+    "public_repos": 232')
    assert "stargazers_count" not in result.stdout


# --- baseline selection -------------------------------------------------------


def test_baseline_is_the_newest_dated_snapshot_and_never_the_latest_file(root):
    """The glob matches only YYYY-MM-DD snapshots, so the freshly written *_latest.json cannot be its own baseline."""
    newer = _variant(lambda f: f["GitHub user docxology"].__setitem__("public_repos", 240))
    write_baseline(root, BASE_FACTS, "2026-09-17")
    write_baseline(root, newer, "2026-09-30")
    # A decoy named like the refresh output: were it picked, the comparison below would read as unchanged.
    _write_json(root / "reports" / "public_source_snapshot_latest.json", {"facts": newer, "checks": []})
    write_latest(root, newer)
    result = run_compare(root)
    assert result.returncode == 0, result.stderr
    assert result.outputs["baseline"] == "reports/public_source_snapshot_2026-09-30.json"
    assert result.outputs["changed"] == "false"


def test_a_latest_file_alone_cannot_hide_drift(root):
    """Only the dated baseline differs from the new facts; the equal *_latest.json decoy must be ignored."""
    changed = _variant(lambda f: f["GitHub user docxology"].__setitem__("public_repos", 240))
    write_baseline(root, BASE_FACTS, "2026-09-30")
    _write_json(root / "reports" / "public_source_snapshot_latest.json", {"facts": changed, "checks": []})
    write_latest(root, changed)
    result = run_compare(root)
    assert result.returncode == 0, result.stderr
    assert result.outputs["changed"] == "true"
    assert result.outputs["baseline"] == "reports/public_source_snapshot_2026-09-30.json"


def test_other_report_files_are_not_mistaken_for_baselines(root):
    """Inventory reports and non-snapshot files sharing the directory do not match the baseline glob."""
    write_baseline(root, BASE_FACTS, "2026-09-30")
    _write_json(root / "reports" / "public_source_inventory_2026-10-05.json", {"facts": {"x": 1}})
    _write_json(root / "reports" / "public_source_snapshot_2026-10-05.facts.json", {"x": 1})
    write_latest(root, BASE_FACTS)
    result = run_compare(root)
    assert result.returncode == 0, result.stderr
    assert result.outputs["baseline"] == "reports/public_source_snapshot_2026-09-30.json"
    assert result.outputs["changed"] == "false"


def test_missing_dated_baseline_fails_the_step_instead_of_reporting_a_verdict(root):
    """With no checked-in baseline the script must fail loudly, never write changed=false."""
    write_latest(root, BASE_FACTS)
    result = run_compare(root)
    assert result.returncode != 0
    assert "changed" not in result.outputs
