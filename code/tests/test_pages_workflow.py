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
    assert "uv run python3 code/orchestrators/validate_repo.py" in validate_job
    assert "uv run python3 -m pytest code/tests -q" in validate_job
    assert "uv run --group lint ruff check --select W605 code" in validate_job
    assert "needs: validate" in deploy_job
    assert "if: github.ref == 'refs/heads/main'" in deploy_job
    assert "fetch-depth: 0" in deploy_job
    assert "uv run python3 code/orchestrators/build_pages_artifact.py --output _site --check-size --check-manifest" in deploy_job
