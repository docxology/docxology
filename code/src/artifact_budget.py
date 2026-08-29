"""Artifact budget gate: fail the CI budget check when the Pages artifact
exceeds the documented 850 MiB warning budget (reports/pages_artifact_growth_*.json).
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

BUDGET_MIB = 850.0
REPORT_GLOB = "reports/pages_artifact_growth_*.json"


class ArtifactBudgetError(RuntimeError):
    """Raised when the latest artifact measurement exceeds the budget."""


def latest_growth_report(repo_root: Path) -> Path:
    """Return the newest dated pages_artifact_growth report, or raise."""
    candidates = sorted(glob.glob(str(repo_root / REPORT_GLOB)))
    if not candidates:
        raise ArtifactBudgetError(f"no artifact growth reports found matching {REPORT_GLOB}")
    return Path(candidates[-1])


def artifact_mib_from_report(path: Path) -> float:
    """Extract artifact_mib from a growth report JSON."""
    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    mib = payload.get("artifact_mib")
    if not isinstance(mib, (int, float)):
        raise ArtifactBudgetError(f"{path}: missing numeric 'artifact_mib'")
    return float(mib)


def enforce_budget(repo_root: Path, budget_mib: float = BUDGET_MIB) -> float:
    """Raise :class:`ArtifactBudgetError` when the latest artifact exceeds budget."""
    path = latest_growth_report(repo_root)
    mib = artifact_mib_from_report(path)
    if mib > budget_mib:
        raise ArtifactBudgetError(
            f"ARTIFACT BUDGET EXCEEDED: {path} reports {mib:.2f} MiB "
            f"> budget {budget_mib:.0f} MiB. Trim the Pages artifact before deploy."
        )
    print(f"Artifact budget OK: {mib:.2f} MiB <= {budget_mib:.0f} MiB ({path})")
    return mib


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    try:
        enforce_budget(repo_root)
    except ArtifactBudgetError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
