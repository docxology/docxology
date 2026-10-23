"""Release-path contracts for the Pages deployment workflow."""

from __future__ import annotations

import re
from pathlib import Path

import yaml
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pages_deploy_waits_for_the_authoritative_validation_job():
    workflow = (REPO_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    jobs = workflow.split("jobs:\n", 1)[1]
    validate_job, deploy_job = jobs.split("\n  deploy:\n", 1)

    assert "  validate:\n" in validate_job
    assert "if: github.ref == 'refs/heads/main'" in validate_job
    assert "fetch-depth: 0" in validate_job
    assert "ref: ${{ github.sha }}" in validate_job
    assert "uv run python3 code/orchestrators/validate_repo.py" in validate_job
    # -n auto parallelises across cores; --dist loadfile keeps every test in a
    # file on one worker, so module-level caches and fixtures behave as written.
    assert 'uv run python3 -m pytest code/tests -q -m "not browser and not manuscript_render" -n auto --dist loadfile' in validate_job
    # The lint gate is configured in pyproject.toml ([tool.ruff.lint]) rather
    # than pinned to one rule on the command line, so CI and a local
    # `ruff check code` enforce exactly the same set.
    assert "uv run --group lint ruff check code" in validate_job
    assert "uv run python3 code/src/artifact_budget.py" in validate_job
    assert "needs: [validate, browser-tests]" in deploy_job
    assert "  browser-tests:\n" in validate_job
    assert "uses: ./.github/workflows/browser-qa.yml" in validate_job
    assert "if: github.ref == 'refs/heads/main'" in deploy_job
    assert "fetch-depth: 0" in deploy_job
    assert "ref: ${{ github.sha }}" in deploy_job
    assert "uv run python3 code/orchestrators/build_pages_artifact.py --output _site --check-size --check-manifest" in deploy_job



def test_pages_deploy_projects_and_verifies_the_exact_candidate():
    """Tripwire for the deploy steps that workflow-only commits can change.

    Workflow files are payload-neutral (``release_controls.is_payload_neutral_path``),
    so no payload-anchored record names a commit that edits them; the deployed
    projection and its exact-HEAD acceptance must therefore stay pinned here.
    Action versions are deliberately not pinned, so Dependabot bumps pass.
    """
    workflow = (REPO_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    deploy_job = workflow.split("\n  deploy:\n", 1)[1]
    upload = deploy_job.split("- name: Upload Pages artifact", 1)[1].split("- name:", 1)[0]
    assert re.search(r"uses: actions/upload-pages-artifact@v\d+", upload)
    assert "path: _site" in upload
    assert "include-hidden-files: true" in upload
    assert re.search(r"uses: actions/deploy-pages@v\d+", deploy_job)
    verify = deploy_job.split("- name: Verify deployed artifact against candidate SHA", 1)[1].split("- name:", 1)[0]
    assert "CANDIDATE_SHA: ${{ github.sha }}" in verify
    assert 'verify_deployed_artifact.py --expected-commit "$CANDIDATE_SHA"' in verify
    receipt = deploy_job.split("- name: Retain deployment acceptance receipt", 1)[1]
    assert "if: always()" in receipt
    assert "path: /tmp/deployment-acceptance.json" in receipt
    assert "if-no-files-found: error" in receipt

def test_publication_and_validation_share_required_browser_acceptance():
    reusable = (REPO_ROOT / ".github/workflows/browser-qa.yml").read_text(encoding="utf-8")
    validation = (REPO_ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    assert "uses: ./.github/workflows/browser-qa.yml" in validation
    assert "ref: ${{ github.event.pull_request.head.sha || github.sha }}" in validation
    assert "ref: ${{ github.event.pull_request.head.sha || github.sha }}" in reusable
    assert "workflow_call:" in reusable
    assert "uv sync --extra browser-qa" in reusable
    assert "playwright install --with-deps chromium" in reusable
    assert "lighthouse@13.4.1" in reusable
    assert '-m "browser and not lighthouse" -n 2 --dist loadfile' in reusable
    assert 'pytest code/tests -q -m lighthouse' in reusable
    assert 'test_rendered_frontend.py' not in reusable
    assert '-m "not browser and not manuscript_render"' in validation


def test_live_verification_binds_triggering_candidate_and_retains_failed_receipt():
    workflow = (REPO_ROOT / ".github/workflows/live-verify.yml").read_text(encoding="utf-8")
    assert "ref: ${{ github.event.workflow_run.head_sha || github.sha }}" in workflow
    assert "CANDIDATE_SHA: ${{ github.event.workflow_run.head_sha || github.sha }}" in workflow
    assert "DEPLOYMENT_RUN_ID: ${{ github.event.workflow_run.id }}" in workflow
    assert "--expected-commit \"$CANDIDATE_SHA\"" in workflow
    assert "--deployment-run-id \"$DEPLOYMENT_RUN_ID\"" in workflow
    assert "github.event.workflow_run.head_branch == 'main'" in workflow
    assert "glob.glob" not in workflow
    upload = workflow.split("- name: Upload live verification report", 1)[1]
    assert "if: always()" in upload
    assert "path: /tmp/live-site-verification.json" in upload
    assert "if-no-files-found: error" in upload
    assert "retention-days: 90" in upload


def test_indexnow_submits_the_deployed_candidate_from_main():
    workflow = (REPO_ROOT / ".github/workflows/indexnow-on-push.yml").read_text(encoding="utf-8")
    assert "ref: ${{ github.event.workflow_run.head_sha || github.sha }}" in workflow
    assert "github.event.workflow_run.head_branch == 'main'" in workflow
    assert "github.ref == 'refs/heads/main'" in workflow


def test_pages_workflow_name_matches_every_follower_trigger():
    """Live verification and IndexNow follow the Pages run by its display name.

    A workflow-only commit needs no control tail, so nothing else would notice
    a rename of ``pages.yml`` that silently stops both followers.
    """
    pages = (REPO_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    name = re.search(r"^name:\s*(.+?)\s*$", pages, re.MULTILINE).group(1)
    for follower in ("live-verify.yml", "indexnow-on-push.yml"):
        text = (REPO_ROOT / ".github/workflows" / follower).read_text(encoding="utf-8")
        triggers = re.search(r"^\s+workflows:\s*\[(.+)\]\s*$", text, re.MULTILINE).group(1)
        assert [t.strip().strip("\"'") for t in triggers.split(",")] == [name], follower
    verifier = (REPO_ROOT / "code/orchestrators/verify_live_site.py").read_text(encoding="utf-8")
    assert verifier.count(f'"{name}"') == 2


def test_every_python_workflow_job_uses_the_declared_runtime():
    """A runner default must not silently bypass the repository Python pin."""
    checked = 0
    for path in (REPO_ROOT / ".github/workflows").glob("*.yml"):
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        for name, job in workflow.get("jobs", {}).items():
            steps = job.get("steps", [])
            python_steps = [i for i, step in enumerate(steps)
                            if re.search(r"\bpython[0-9]*\b", step.get("run", ""))]
            if not python_steps:
                continue
            setup = [(i, step) for i, step in enumerate(steps)
                     if step.get("uses", "").startswith("actions/setup-python@")]
            assert len(setup) == 1, f"{path.name}:{name} must select the repository runtime"
            index, step = setup[0]
            assert index < min(python_steps), f"{path.name}:{name} runs Python before setup"
            assert step.get("with", {}).get("python-version-file") == ".python-version"
            assert "python-version" not in step.get("with", {})
            checked += 1
    assert checked, "no Python workflow jobs were inspected"


def test_uv_workflow_jobs_require_locked_binary_dependencies():
    """Missing native wheels must fail before an incidental source build."""
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    required_wheels = set(project["tool"]["uv"]["no-build-package"])
    assert {"pillow", "greenlet", "pymupdf"} <= required_wheels
    checked = 0
    for path in (REPO_ROOT / ".github/workflows").glob("*.yml"):
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        for name, job in workflow.get("jobs", {}).items():
            if not any(re.search(r"\buv (run|sync)\b", step.get("run", ""))
                       for step in job.get("steps", [])):
                continue
            environment = {**workflow.get("env", {}), **job.get("env", {})}
            assert str(environment.get("UV_LOCKED")) == "1", f"{path.name}:{name} must enforce its lock"
            checked += 1
    assert checked, "no uv workflow jobs were inspected"
