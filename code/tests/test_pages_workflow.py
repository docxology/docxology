"""Release-path contracts for the Pages deployment workflow."""

from __future__ import annotations

from pathlib import Path


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
    assert "uv run python3 -m pytest code/tests -q -n auto --dist loadfile" in validate_job
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


def test_publication_and_validation_share_required_browser_acceptance():
    reusable = (REPO_ROOT / ".github/workflows/browser-qa.yml").read_text(encoding="utf-8")
    validation = (REPO_ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    assert "uses: ./.github/workflows/browser-qa.yml" in validation
    assert "ref: ${{ github.event.pull_request.head.sha || github.sha }}" in validation
    assert "ref: ${{ github.event.pull_request.head.sha || github.sha }}" in reusable
    assert "workflow_call:" in reusable
    assert "DOCXOLOGY_REQUIRE_BROWSER_QA: \"1\"" in reusable
    assert "uv sync --extra browser-qa" in reusable
    assert "playwright install --with-deps chromium" in reusable
    assert "lighthouse@13.4.1" in reusable
    for test_file in ("test_lighthouse_budgets.py", "test_service_worker.py",
                      "test_rendered_frontend.py", "test_rendered_progressive_enhancement.py"):
        assert test_file in reusable


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
