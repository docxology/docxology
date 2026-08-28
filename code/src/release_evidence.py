"""Freshness and provenance checks for a deployment-ready release receipt.

Normal repository validation is deliberately offline and may inspect cached
evidence.  A release is stricter: each required report must be recent, record
the exact source revision it exercised, and be bound to a post-deploy
attestation for that same revision.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
import fnmatch
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from scholar_verification import validate_scholar_snapshot_receipt


@dataclass(frozen=True)
class EvidenceRequirement:
    """A dated release-evidence artifact and its repository glob."""

    name: str
    pattern: str


RELEASE_EVIDENCE: tuple[EvidenceRequirement, ...] = (
    EvidenceRequirement("public-source snapshot", "reports/public_source_snapshot_*.json"),
    EvidenceRequirement("public-source review", "reports/public_source_review_*.json"),
    EvidenceRequirement("external-link report", "reports/external_links_[0-9]*.json"),
    EvidenceRequirement("browser smoke", "reports/browser-smoke/*/manifest.json"),
    EvidenceRequirement("browser QA", "reports/browser-qa/*/manifest.json"),
    EvidenceRequirement("visual QA", "reports/visual-qa/*/manifest.json"),
    EvidenceRequirement("live-site verification", "reports/live_site_verification_*.json"),
)

# A glob is useful for discovering dated receipts, but it is deliberately not
# sufficient authorization to treat a file as release evidence.  Each required
# report has a fixed public path shape and an ISO calendar date.  Keep this
# contract adjacent to ``RELEASE_EVIDENCE`` so collection and attestation use
# the same boundary rather than accepting any lexically matching filename.
_REQUIREMENT_PATH_PATTERNS: dict[str, re.Pattern[str]] = {
    "public-source snapshot": re.compile(
        r"^reports/public_source_snapshot_(?P<date>\d{4}-\d{2}-\d{2})\.json$"
    ),
    "public-source review": re.compile(
        r"^reports/public_source_review_(?P<date>\d{4}-\d{2}-\d{2})\.json$"
    ),
    "external-link report": re.compile(
        r"^reports/external_links_(?P<date>\d{4}-\d{2}-\d{2})\.json$"
    ),
    "browser smoke": re.compile(
        r"^reports/browser-smoke/(?P<date>\d{4}-\d{2}-\d{2})/manifest\.json$"
    ),
    "browser QA": re.compile(
        r"^reports/browser-qa/(?P<date>\d{4}-\d{2}-\d{2})/manifest\.json$"
    ),
    "visual QA": re.compile(
        r"^reports/visual-qa/(?P<date>\d{4}-\d{2}-\d{2})/manifest\.json$"
    ),
    "live-site verification": re.compile(
        r"^reports/live_site_verification_(?P<date>\d{4}-\d{2}-\d{2})\.json$"
    ),
}

_DATED_REPORT_NAME = re.compile(
    r"^reports/(?:public_source_snapshot|public_source_review|external_links|external_links_triage|live_site_verification)_(\d{4}-\d{2}-\d{2})\.json$"
)
_POSTDEPLOY_MARKDOWN_REPORT_NAME = re.compile(
    r"^reports/(?:public_source_review|external_links_triage)_(\d{4}-\d{2}-\d{2})\.md$"
)
_BROWSER_REPORT_FILE = re.compile(
    r"^reports/(?:browser-smoke|browser-qa|visual-qa)/(\d{4}-\d{2}-\d{2})/(?:manifest\.json|[a-z0-9][a-z0-9-]*\.png)$"
)
_ATTESTATION_FILE = re.compile(r"^reports/deployment-attestations/[0-9a-f]{40}\.json$")
ORCHESTRATORS_DIR = Path(__file__).resolve().parents[1] / "orchestrators"
FUTURE_TIMESTAMP_TOLERANCE_SECONDS = 300


def _is_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_ephemeral_release_evidence_path(path: str) -> bool:
    """Return whether a worktree-relative path is generated release evidence.

    Release verification runs against an already committed SHA.  Its fresh
    browser, link, source, live-site, and attestation receipts are deliberately
    produced *after* that commit and may remain untracked or modify a dated
    report in the checkout.  They are evidence about the candidate, not source
    changes to it.  Keep this exception narrow: hand-authored reports and every
    other tracked source path still make ``validate_repo --release`` fail.
    """
    # Never normalize a backslash into a forward slash: POSIX permits it in a
    # filename, and doing so would let an unrelated changed source file become
    # an evidence exemption.
    if "\\" in path or path.startswith("./"):
        return False
    dated = _DATED_REPORT_NAME.fullmatch(path)
    if dated:
        return _is_iso_date(dated.group(1))
    markdown = _POSTDEPLOY_MARKDOWN_REPORT_NAME.fullmatch(path)
    if markdown:
        return _is_iso_date(markdown.group(1))
    browser = _BROWSER_REPORT_FILE.fullmatch(path)
    if browser:
        return _is_iso_date(browser.group(1))
    return _ATTESTATION_FILE.fullmatch(path) is not None


def deployment_attestation_path(repo_root: Path, commit: str) -> Path:
    """Return the sole permitted storage location for one deployment SHA."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("deployment commit must be a lowercase 40-character SHA")
    return repo_root / "reports" / "deployment-attestations" / f"{commit}.json"


def _orchestrator_module(name: str):
    """Load a local declarative coverage contract without running its CLI."""
    location = str(ORCHESTRATORS_DIR)
    if location not in sys.path:
        sys.path.insert(0, location)
    return importlib.import_module(name)


def expected_public_source_labels() -> set[str]:
    module = _orchestrator_module("refresh_public_sources")
    return set(module.expected_check_labels())


def expected_external_urls() -> set[str]:
    module = _orchestrator_module("check_external_links")
    return set(module.collect_urls())


def expected_browser_smoke_names() -> set[str]:
    module = _orchestrator_module("browser_smoke")
    return {name for name, _path, _selector in module.PAGES}


def expected_browser_qa_names() -> set[str]:
    module = _orchestrator_module("browser_qa")
    return set(module.CHECK_NAMES)


def expected_visual_targets() -> set[tuple[str, str, str]]:
    module = _orchestrator_module("visual_qa")
    return {
        (path, viewport, size)
        for _name, path in module.PAGES
        for viewport, size in module.VIEWPORTS
    }


def expected_live_paths() -> set[str]:
    module = _orchestrator_module("verify_live_site")
    return {check["path"] or "index.html" for check in module.load_dynamic_checks()}


@dataclass(frozen=True)
class EvidenceReceipt:
    """The immutable facts copied into a post-deploy attestation."""

    name: str
    path: str
    generated_at: str
    source_commit: str
    sha256: str


def matches_requirement_path(relative: str, requirement: EvidenceRequirement) -> bool:
    """Match a release receipt against its full repository-relative pattern.

    ``Path.match`` suffix-matches patterns containing directory components;
    that would let a nested source file impersonate ``reports/...`` evidence.
    The fixed requirement patterns are repository-relative, so require the
    same path-component depth as well as a full string glob match.
    """
    candidate = Path(relative)
    pattern = Path(requirement.pattern)
    path_pattern = _REQUIREMENT_PATH_PATTERNS.get(requirement.name)
    if path_pattern is None:
        return False
    dated = path_pattern.fullmatch(relative)
    return bool(
        not candidate.is_absolute()
        and len(candidate.parts) == len(pattern.parts)
        and fnmatch.fnmatchcase(relative, requirement.pattern)
        and dated is not None
        and _is_iso_date(dated.group("date"))
    )


def _latest_path(repo_root: Path, requirement: EvidenceRequirement) -> Path | None:
    """Return the newest validly named receipt for one evidence requirement.

    Invalid date-like filenames are not merely lower-priority candidates: they
    are not evidence at all.  Filtering them before selecting the latest path
    prevents a lexically newer malformed report from masking a valid receipt.
    """
    matches = sorted(
        (
            path
            for path in repo_root.glob(requirement.pattern)
            if matches_requirement_path(path.relative_to(repo_root).as_posix(), requirement)
        ),
        key=lambda path: path.as_posix(),
        reverse=True,
    )
    return matches[0] if matches else None


def _json_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("report root must be a JSON object")
    return payload


def _parse_timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing generated_at")
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("generated_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def sha256_file(path: Path) -> str:
    """Return the SHA-256 of a report exactly as it was attested."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_repo_file(repo_root: Path, path: Path) -> tuple[Path | None, str | None]:
    """Resolve a regular file only when neither it nor an ancestor is a link."""
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return None, f"path escapes repository: {path}"
    current = repo_root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            return None, f"symlinked release evidence is not permitted: {path.relative_to(repo_root)}"
    if not path.is_file():
        return None, f"missing regular file: {path.relative_to(repo_root)}"
    if path.lstat().st_nlink != 1:
        return None, f"hard-linked release evidence is not permitted: {path.relative_to(repo_root)}"
    try:
        resolved_root = repo_root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        return None, f"unresolvable repository evidence path {path.relative_to(repo_root)}: {exc}"
    return resolved_path, None


def _check_rows(
    payload: dict[str, Any],
    *,
    report_name: str,
    require_screenshots: bool,
    repo_root: Path,
    manifest_path: Path,
    expected_names: set[str] | None = None,
) -> list[str]:
    """Validate a completed browser-style report instead of just its age."""
    checks = payload.get("checks")
    if not isinstance(checks, list) or not checks:
        return [f"{report_name} has no checks"]
    count = payload.get("count")
    passing = payload.get("passing")
    if not isinstance(count, int) or count != len(checks):
        return [f"{report_name} count does not match its checks"]
    if not isinstance(passing, int):
        return [f"{report_name} lacks an integer passing count"]
    failures = [
        str(item.get("name") or item.get("page") or index)
        for index, item in enumerate(checks, start=1)
        if not isinstance(item, dict) or item.get("ok") is not True
    ]
    if failures:
        return [f"{report_name} has failing checks: {', '.join(failures[:5])}"]
    if passing != count:
        return [f"{report_name} passing count {passing} != count {count}"]
    if expected_names is not None:
        observed_names = [item.get("name") for item in checks if isinstance(item, dict)]
        if not all(isinstance(name, str) and name for name in observed_names):
            return [f"{report_name} has a check without a stable name"]
        observed_set = set(observed_names)
        if len(observed_set) != len(observed_names):
            return [f"{report_name} repeats a coverage check name"]
        if observed_set != expected_names:
            missing = sorted(expected_names - observed_set)
            unexpected = sorted(observed_set - expected_names)
            pieces = []
            if missing:
                pieces.append("missing " + ", ".join(missing[:5]))
            if unexpected:
                pieces.append("unexpected " + ", ".join(unexpected[:5]))
            return [f"{report_name} coverage does not match the current contract ({'; '.join(pieces)})"]
    if require_screenshots:
        missing: list[str] = []
        for item in checks:
            if not isinstance(item, dict):
                missing.append("unnamed")
                continue
            screenshot = item.get("screenshot")
            artifact, error = _report_artifact_path(repo_root, manifest_path, screenshot)
            if error:
                missing.append(error)
                continue
            digest = item.get("screenshot_sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                missing.append(str(screenshot) + " (missing screenshot_sha256)")
            elif sha256_file(artifact) != digest:
                missing.append(str(screenshot) + " (digest mismatch)")
        if missing:
            return [f"{report_name} has invalid screenshots: {', '.join(missing[:5])}"]
    return []


def _report_artifact_path(
    repo_root: Path, manifest_path: Path, raw_path: object
) -> tuple[Path | None, str | None]:
    """Resolve only a report-local, repository-owned screenshot artifact."""
    if not isinstance(raw_path, str) or not raw_path:
        return None, "missing screenshot path"
    if "\\" in raw_path:
        return None, f"invalid screenshot path {raw_path!r}"
    candidate = Path(raw_path)
    if candidate.is_absolute() or ".." in candidate.parts or raw_path.startswith("./"):
        return None, f"invalid screenshot path {raw_path!r}"
    absolute = repo_root / candidate
    try:
        absolute.relative_to(manifest_path.parent)
    except ValueError:
        return None, f"screenshot is outside its report directory: {raw_path}"
    if absolute.suffix.lower() != ".png":
        return None, f"missing PNG screenshot: {raw_path}"
    resolved, error = _safe_repo_file(repo_root, absolute)
    if error:
        return None, error
    try:
        resolved_parent = manifest_path.parent.resolve(strict=True)
        resolved.relative_to(resolved_parent)
    except (OSError, ValueError):
        return None, f"screenshot is outside its report directory: {raw_path}"
    return resolved, None


def _visual_review_errors(payload: dict[str, Any], repo_root: Path, manifest_path: Path) -> list[str]:
    """Require an explicit human review record in addition to screenshots."""
    screenshots = payload.get("screenshots")
    if not isinstance(screenshots, list) or not screenshots:
        return ["visual QA has no screenshots"]
    missing: list[str] = []
    observed_targets: list[tuple[str, str, str]] = []
    for screenshot in screenshots:
        file_name = screenshot.get("file") if isinstance(screenshot, dict) else None
        artifact, error = _report_artifact_path(repo_root, manifest_path, file_name)
        if error:
            missing.append(error)
            continue
        digest = screenshot.get("sha256") if isinstance(screenshot, dict) else None
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            missing.append(str(file_name) + " (missing sha256)")
        elif sha256_file(artifact) != digest:
            missing.append(str(file_name) + " (digest mismatch)")
        if isinstance(screenshot, dict):
            page = screenshot.get("page")
            viewport = screenshot.get("viewport")
            size = screenshot.get("size")
            if all(isinstance(value, str) and value for value in (page, viewport, size)):
                observed_targets.append((page, viewport, size))
            else:
                missing.append(str(file_name) + " (missing page/viewport/size coverage fields)")
    if missing:
        return [f"visual QA has missing screenshots: {', '.join(missing[:5])}"]
    expected_targets = expected_visual_targets()
    if set(observed_targets) != expected_targets or len(observed_targets) != len(set(observed_targets)):
        missing_targets = sorted(expected_targets - set(observed_targets))
        unexpected_targets = sorted(set(observed_targets) - expected_targets)
        details = []
        if missing_targets:
            details.append("missing " + repr(missing_targets[:3]))
        if unexpected_targets:
            details.append("unexpected " + repr(unexpected_targets[:3]))
        if len(observed_targets) != len(set(observed_targets)):
            details.append("duplicate targets")
        return ["visual QA coverage does not match the current contract (" + "; ".join(details) + ")"]
    review = payload.get("review")
    if not isinstance(review, dict) or review.get("status") != "reviewed":
        return ["visual QA has not recorded an explicit review"]
    reviewer = review.get("reviewed_by")
    if not isinstance(reviewer, str) or not reviewer.strip():
        return ["visual QA lacks reviewed_by"]
    try:
        reviewed_at = _parse_timestamp(review.get("reviewed_at"))
    except ValueError as exc:
        return [f"visual QA has invalid reviewed_at: {exc}"]
    try:
        generated_at = _parse_timestamp(payload.get("generated_at"))
    except ValueError as exc:
        return [f"visual QA has invalid generated_at: {exc}"]
    if reviewed_at < generated_at:
        return ["visual QA review predates its captured manifest"]
    return []


def _report_result_errors(
    requirement: EvidenceRequirement,
    payload: dict[str, Any],
    *,
    repo_root: Path,
    report_path: Path,
) -> list[str]:
    """Return semantic failures for one release evidence report type."""
    if requirement.name == "public-source snapshot":
        checks = payload.get("checks")
        if not isinstance(checks, list) or not checks:
            return ["public-source snapshot has no checks"]
        labels = [item.get("label") for item in checks if isinstance(item, dict)]
        if not all(isinstance(label, str) and label for label in labels):
            return ["public-source snapshot has a check without a stable label"]
        if len(labels) != len(set(labels)):
            return ["public-source snapshot repeats a check label"]
        expected_labels = expected_public_source_labels()
        if set(labels) != expected_labels:
            return ["public-source snapshot coverage does not match the current contract"]
        failures = [
            str(item.get("label") or item.get("url") or index)
            for index, item in enumerate(checks, start=1)
            if not isinstance(item, dict) or item.get("ok") is not True
        ]
        return [f"public-source snapshot has failing checks: {', '.join(failures[:5])}"] if failures else []

    if requirement.name == "public-source review":
        from public_source_review import validate_review_report

        errors = validate_review_report(payload)
        if not payload.get("items"):
            errors.append("public-source review has no disposition items")
        inputs = payload.get("inputs")
        snapshot = inputs.get("public_source_snapshot") if isinstance(inputs, dict) else None
        if not isinstance(snapshot, dict):
            errors.append("public-source review lacks public-source snapshot provenance")
        return errors

    if requirement.name == "external-link report":
        checked = payload.get("checked_urls")
        total = payload.get("total_unique_urls")
        results = payload.get("results")
        if not isinstance(checked, int) or checked <= 0:
            return ["external-link report has no checked URLs"]
        if not isinstance(total, int) or total != checked:
            return ["external-link report is incomplete"]
        if not isinstance(results, list) or len(results) != checked:
            return ["external-link report result count does not match checked URLs"]
        malformed = [
            str(index)
            for index, item in enumerate(results, start=1)
            if not isinstance(item, dict) or not isinstance(item.get("ok"), bool)
        ]
        if malformed:
            return [f"external-link report has malformed results: {', '.join(malformed[:5])}"]
        expected_urls = expected_external_urls()
        observed_urls = [item.get("url") for item in results if isinstance(item, dict)]
        if not all(isinstance(url, str) and url for url in observed_urls):
            return ["external-link report has a result without a URL"]
        if len(observed_urls) != len(set(observed_urls)) or set(observed_urls) != expected_urls:
            return ["external-link report coverage does not match the current URL contract"]
        observed_ok = sum(1 for item in results if item["ok"])
        observed_warnings = len(results) - observed_ok
        if payload.get("ok") != observed_ok or payload.get("warnings") != observed_warnings:
            return ["external-link report summary does not match results"]
        confirmed_404s = [
            str(item.get("url"))
            for item in results
            if str(item.get("status") or "") == "404"
        ]
        if confirmed_404s:
            return [
                "external-link report has confirmed 404s requiring replacement: "
                + ", ".join(confirmed_404s[:5])
            ]
        return []

    if requirement.name == "browser smoke":
        return _check_rows(
            payload,
            report_name="browser smoke",
            require_screenshots=True,
            repo_root=repo_root,
            manifest_path=report_path,
            expected_names=expected_browser_smoke_names(),
        )
    if requirement.name == "browser QA":
        return _check_rows(
            payload,
            report_name="browser QA",
            require_screenshots=False,
            repo_root=repo_root,
            manifest_path=report_path,
            expected_names=expected_browser_qa_names(),
        )
    if requirement.name == "visual QA":
        return _visual_review_errors(payload, repo_root, report_path)
    if requirement.name == "live-site verification":
        if payload.get("overall_ok") is not True:
            return ["live-site verification is not passing"]
        results = payload.get("results")
        if not isinstance(results, list) or not results:
            return ["live-site verification has no results"]
        paths = [item.get("path") for item in results if isinstance(item, dict)]
        if len(paths) != len(results) or not all(isinstance(path, str) and path for path in paths):
            return ["live-site verification has a result without a path"]
        if len(paths) != len(set(paths)) or set(paths) != expected_live_paths():
            return ["live-site verification coverage does not match the current route contract"]
        if any(item.get("ok") is not True for item in results if isinstance(item, dict)):
            return ["live-site verification has a failing route"]
        return []
    return [f"unsupported release evidence requirement: {requirement.name}"]


def _validate_report(
    requirement: EvidenceRequirement,
    path: Path,
    repo_root: Path,
    expected_commit: str,
    *,
    max_age_days: int,
    reference: datetime,
) -> tuple[EvidenceReceipt | None, list[str]]:
    """Validate one exact report path and return its immutable receipt."""
    safe_path, safe_error = _safe_repo_file(repo_root, path)
    if safe_error:
        return None, [f"invalid {requirement.name} {path}: {safe_error}"]
    assert safe_path is not None
    path = safe_path
    try:
        payload = _json_object(path)
        generated = _parse_timestamp(payload.get("generated_at"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, [f"invalid {requirement.name} {path.relative_to(repo_root)}: {exc}"]
    errors: list[str] = []
    age_seconds = (reference - generated).total_seconds()
    if age_seconds < -FUTURE_TIMESTAMP_TOLERANCE_SECONDS:
        errors.append(f"{requirement.name} is dated in the future: {path.relative_to(repo_root)}")
    elif age_seconds > max_age_days * 86400:
        age_days = age_seconds / 86400
        errors.append(
            f"stale {requirement.name}: {path.relative_to(repo_root)} is {age_days:.1f} days old "
            f"(maximum {max_age_days})"
        )
    source_commit = str(payload.get("source_commit") or payload.get("source_commit_at_generation") or "").strip()
    if not source_commit:
        errors.append(f"{requirement.name} lacks source_commit: {path.relative_to(repo_root)}")
    elif source_commit != expected_commit:
        errors.append(
            f"{requirement.name} source_commit {source_commit} != release commit {expected_commit}: "
            f"{path.relative_to(repo_root)}"
        )
    if payload.get("source_worktree_clean") is not True:
        errors.append(f"{requirement.name} was not captured from a clean source worktree: {path.relative_to(repo_root)}")
    tree = _git_tree_for_commit(repo_root, expected_commit)
    if tree is not None and payload.get("source_tree_sha") != tree:
        errors.append(f"{requirement.name} source_tree_sha does not match the release commit: {path.relative_to(repo_root)}")
    for error in _report_result_errors(requirement, payload, repo_root=repo_root, report_path=path):
        errors.append(f"{requirement.name} failed semantic validation: {error}")
    return (
        EvidenceReceipt(
            name=requirement.name,
            path=path.relative_to(repo_root).as_posix(),
            generated_at=str(payload.get("generated_at")),
            source_commit=source_commit,
            sha256=sha256_file(path),
        ),
        errors,
    )


def _git_tree_for_commit(repo_root: Path, commit: str) -> str | None:
    """Return a commit tree hash when the candidate exists in this checkout."""
    import subprocess

    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}^{{tree}}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def collect_release_evidence(
    repo_root: Path,
    expected_commit: str,
    *,
    max_age_days: int,
    now: datetime | None = None,
) -> tuple[list[EvidenceReceipt], list[str]]:
    """Collect recent reports and return validation errors without writing.

    Matching the source commit exactly is intentional.  A report made before a
    content edit is evidence for an earlier revision, not evidence for the
    candidate being released.
    """
    if max_age_days < 0:
        raise ValueError("max_age_days must be non-negative")
    reference = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    receipts: list[EvidenceReceipt] = []
    errors: list[str] = []
    for requirement in RELEASE_EVIDENCE:
        path = _latest_path(repo_root, requirement)
        if path is None:
            errors.append(f"missing {requirement.name} ({requirement.pattern})")
            continue
        receipt, report_errors = _validate_report(
            requirement,
            path,
            repo_root,
            expected_commit,
            max_age_days=max_age_days,
            reference=reference,
        )
        errors.extend(report_errors)
        if receipt is not None:
            receipts.append(receipt)
    errors.extend(scholar_source_receipt_errors(repo_root))
    errors.extend(_review_snapshot_binding_errors(repo_root, receipts, expected_commit))
    return receipts, errors


def scholar_source_receipt_errors(repo_root: Path) -> list[str]:
    """Return release-facing errors for an unbound Scholar metric source.

    This deliberately validates the source sidecar rather than the status of a
    public-source review item.  A review can remain deferred when a fresh
    external scan did not modify curated metrics; the stable receipt only
    becomes invalid when ``data/scholar-snapshot.json`` itself changes.
    """
    return [
        f"Scholar source receipt validation failed: {error}"
        for error in validate_scholar_snapshot_receipt(repo_root)
    ]


def _review_snapshot_binding_errors(
    repo_root: Path, receipts: list[EvidenceReceipt], expected_commit: str
) -> list[str]:
    """Ensure the review queue is about the exact refreshed snapshot attested."""
    by_name = {receipt.name: receipt for receipt in receipts}
    review = by_name.get("public-source review")
    snapshot_receipt = by_name.get("public-source snapshot")
    if review is None or snapshot_receipt is None:
        return []
    try:
        review_payload = _json_object(repo_root / review.path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid public-source review provenance: {exc}"]
    inputs = review_payload.get("inputs")
    provenance = inputs.get("public_source_snapshot") if isinstance(inputs, dict) else None
    if not isinstance(provenance, dict):
        return ["public-source review lacks public-source snapshot provenance"]
    errors: list[str] = []
    if provenance.get("path") != snapshot_receipt.path:
        errors.append("public-source review does not reference the attested public-source snapshot")
    if provenance.get("sha256") != snapshot_receipt.sha256:
        errors.append("public-source review public-source snapshot hash does not match the attested snapshot")
    if provenance.get("source_commit") != expected_commit:
        errors.append("public-source review public-source snapshot provenance is not bound to the release commit")
    return errors


def live_deployment_errors(
    repo_root: Path, expected_commit: str, *, path: Path | None = None
) -> list[str]:
    """Check the live-site receipt specifically proves deployment of the SHA."""
    requirement = next(item for item in RELEASE_EVIDENCE if item.name == "live-site verification")
    path = path or _latest_path(repo_root, requirement)
    if path is None:
        return ["missing live-site verification report"]
    try:
        payload = _json_object(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid live-site verification {path.relative_to(repo_root)}: {exc}"]
    errors: list[str] = []
    if payload.get("overall_ok") is not True:
        errors.append("live-site verification is not passing")
    pages = payload.get("github_pages") if isinstance(payload.get("github_pages"), dict) else {}
    if pages.get("status") != "built":
        errors.append(f"GitHub Pages status is {pages.get('status') or 'unknown'}")
    deployment = payload.get("deployment") if isinstance(payload.get("deployment"), dict) else {}
    deployed_sha = str(deployment.get("head_sha") or deployment.get("commit") or "").strip()
    if deployed_sha != expected_commit:
        errors.append(f"live deployment SHA {deployed_sha or 'missing'} != release commit {expected_commit}")
    return errors


def render_attestation(
    deployment_sha: str,
    receipts: list[EvidenceReceipt],
    *,
    attested_at: str,
) -> dict:
    """Build the content-addressed post-deploy attestation payload."""
    return {
        "schema_version": "1.0",
        "attested_at": attested_at,
        "deployment_sha": deployment_sha,
        "evidence": [
            {
                "name": receipt.name,
                "path": receipt.path,
                "generated_at": receipt.generated_at,
                "source_commit": receipt.source_commit,
                "sha256": receipt.sha256,
            }
            for receipt in receipts
        ],
        "result": "passed",
        "note": "Post-deploy attestation. A release-ready claim requires this receipt to bind every required evidence report to the deployed SHA.",
    }


def validate_attestation(
    repo_root: Path,
    path: Path,
    expected_commit: str,
    *,
    max_age_days: int,
    now: datetime | None = None,
) -> list[str]:
    """Verify a stored attestation and all reports it content-addresses."""
    errors: list[str] = []
    try:
        expected_path = deployment_attestation_path(repo_root, expected_commit)
    except ValueError as exc:
        return [str(exc)]
    candidate_path = path if path.is_absolute() else repo_root / path
    if candidate_path.resolve(strict=False) != expected_path.resolve(strict=False):
        return [
            "deployment attestation must use the canonical path "
            f"{expected_path.relative_to(repo_root)} for its deployment SHA"
        ]
    safe_attestation, safe_error = _safe_repo_file(repo_root, expected_path)
    if safe_error:
        return [f"invalid deployment attestation: {safe_error}"]
    assert safe_attestation is not None
    path = safe_attestation
    try:
        payload = _json_object(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid deployment attestation {path}: {exc}"]
    if payload.get("schema_version") != "1.0":
        errors.append("deployment attestation has unsupported schema_version")
    if payload.get("result") != "passed":
        errors.append("deployment attestation result is not passed")
    if payload.get("deployment_sha") != expected_commit:
        errors.append(
            f"deployment attestation SHA {payload.get('deployment_sha') or 'missing'} != release commit {expected_commit}"
        )
    attested_at: datetime | None = None
    try:
        attested_at = _parse_timestamp(payload.get("attested_at"))
        reference = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        age_seconds = (reference - attested_at).total_seconds()
        if age_seconds < -FUTURE_TIMESTAMP_TOLERANCE_SECONDS:
            errors.append("deployment attestation is dated in the future")
        elif age_seconds > max_age_days * 86400:
            errors.append(f"deployment attestation is older than {max_age_days} days")
    except ValueError as exc:
        errors.append(f"invalid deployment attestation timestamp: {exc}")
    entries = payload.get("evidence")
    if not isinstance(entries, list):
        return [*errors, "deployment attestation lacks evidence list"]
    by_name: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("deployment attestation has a non-object evidence entry")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            errors.append("deployment attestation has an evidence entry without a name")
            continue
        if name in by_name:
            errors.append(f"deployment attestation repeats {name}")
            continue
        by_name[name] = entry
    known_names = {requirement.name for requirement in RELEASE_EVIDENCE}
    unknown = sorted(set(by_name) - known_names)
    if unknown:
        errors.append("deployment attestation has unknown evidence: " + ", ".join(unknown))
    reference = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    attested_receipts: list[EvidenceReceipt] = []
    for requirement in RELEASE_EVIDENCE:
        entry = by_name.get(requirement.name)
        if not entry:
            errors.append(f"deployment attestation lacks {requirement.name}")
            continue
        relative = entry.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append(f"deployment attestation has invalid path for {requirement.name}")
            continue
        if "\\" in relative:
            errors.append(f"deployment attestation path has invalid separators for {requirement.name}")
            continue
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts or relative.startswith("./"):
            errors.append(f"deployment attestation path escapes repository for {requirement.name}")
            continue
        report_path = repo_root / candidate
        safe_report, safe_error = _safe_repo_file(repo_root, report_path)
        if safe_error:
            errors.append(f"attested {requirement.name} is invalid: {safe_error}")
            continue
        assert safe_report is not None
        report_path = safe_report
        if not matches_requirement_path(relative, requirement):
            errors.append(f"deployment attestation path does not match {requirement.name}: {relative}")
            continue
        if entry.get("source_commit") != expected_commit:
            errors.append(f"attested {requirement.name} is not bound to release commit {expected_commit}")
        if entry.get("sha256") != sha256_file(report_path):
            errors.append(f"attested {requirement.name} changed after attestation: {relative}")
        receipt, report_errors = _validate_report(
            requirement,
            report_path,
            repo_root,
            expected_commit,
            max_age_days=max_age_days,
            reference=reference,
        )
        errors.extend(report_errors)
        if receipt is None:
            continue
        if entry.get("generated_at") != receipt.generated_at:
            errors.append(f"attested {requirement.name} generated_at does not match the report")
        if entry.get("source_commit") != receipt.source_commit:
            errors.append(f"attested {requirement.name} source_commit does not match the report")
        if attested_at is not None:
            try:
                generated_at = _parse_timestamp(receipt.generated_at)
            except ValueError as exc:
                errors.append(
                    f"attested {requirement.name} has invalid generated_at: {exc}"
                )
            else:
                if attested_at < generated_at:
                    errors.append(
                        f"deployment attestation predates {requirement.name} evidence"
                    )
        attested_receipts.append(receipt)
    errors.extend(_review_snapshot_binding_errors(repo_root, attested_receipts, expected_commit))
    errors.extend(scholar_source_receipt_errors(repo_root))
    live_receipt = next((item for item in attested_receipts if item.name == "live-site verification"), None)
    if live_receipt is not None:
        errors.extend(live_deployment_errors(repo_root, expected_commit, path=repo_root / live_receipt.path))
    return errors
