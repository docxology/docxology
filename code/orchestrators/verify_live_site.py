#!/usr/bin/env python3
"""Verify the deployed GitHub Pages site against expected public artifacts."""

from __future__ import annotations

import argparse
import json
import re
import os
import subprocess
import time
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_COUNTS_JSON = REPO_ROOT / "data" / "current-counts.json"
AGENT_INDEX_JSON = REPO_ROOT / "data" / "agent-index.json"

from docxology_tools.report_paths import dated_report_path, generated_timestamp, latest_report, source_worktree_state  # noqa: E402

OUT = dated_report_path("live_site_verification", "json")
BASE = "https://danielarifriedman.com/"
PAGES_DEPLOYMENT_PENDING_STATUSES = frozenset({"building", "queued"})


MAX_RESPONSE_BYTES = 10_000_000  # search-index.json passed 2 MB in 2026-09; keep a ceiling above any generated route


def is_pages_deployment_pending(status: object) -> bool:
    """Return whether Pages is propagating a build rather than failing."""
    return str(status or "").lower() in PAGES_DEPLOYMENT_PENDING_STATUSES


def _read_current_counts(current_counts_json: Path = CURRENT_COUNTS_JSON) -> dict:
    """Read the canonical volatile-count payload from an explicit path."""
    if not current_counts_json.exists():
        return {}
    try:
        return json.loads(current_counts_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _read_agent_index_schema_version(agent_index_json: Path = AGENT_INDEX_JSON) -> str | None:
    """Read the current generated agent-index contract version.

    Keeping the expected version beside the generated artifact prevents the
    live verifier from becoming the hidden second source of truth when the
    agent manifest evolves.
    """
    if not agent_index_json.exists():
        return None
    try:
        payload = json.loads(agent_index_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    version = payload.get("schema_version")
    return version if isinstance(version, str) else None


def load_dynamic_checks(current_counts_json: Path = CURRENT_COUNTS_JSON) -> list[dict[str, list[str]]]:
    """Build marker checks from canonical volatile-count sources."""
    payload = _read_current_counts(current_counts_json)
    counts = payload.get("counts", {})
    software = counts.get("software", {})
    github_inventory = counts.get("github_inventory", {})

    def as_text(value: int | str | None) -> str | None:
        return str(value) if value is not None else None

    works = as_text(counts.get("bibliography_works"))
    software_docx = as_text(software.get("docxology_owned"))
    software_aii = as_text(software.get("active_inference_institute"))
    public_repos = as_text(github_inventory.get("public"))

    checks = [
        {
            "path": "",
            "markers": ["danielarifriedman.com", "publications", "software.html", "Search"],
        },
        {
            "path": "publications.html",
            "markers": ["Publications", "Research Works"],
            "jsonld_types": ["CollectionPage"],
        },
        {
            "path": "software.html",
            "markers": ["Software", "application/ld+json", "Open-Source Repositories"],
            "jsonld_types": ["CollectionPage"],
        },
        {
            "path": "data/software-ld.json",
            "markers": ['"@type"', '"mainEntity"', '"SoftwareSourceCode"'],
        },
        {
            "path": "search.html",
            "markers": ["Search", "search-index.json", "OpenSearch"],
        },
        {
            "path": "catalog.html",
            "markers": ["Data Catalog", "\"@context\"", "/data/catalog.json", "application/ld+json"],
        },
        {
            "path": "updates.html",
            "markers": ["Updates", "update-card", "changelog"],
        },
        {
            "path": "opensearch.xml",
            "markers": ["OpenSearchDescription", "search.html?q={searchTerms}"],
        },
        {
            "path": "sitemap.xml",
            "markers": ["sitemap", "publications.html", "software.html"],
        },
        {
            "path": "llms.txt",
            "markers": ["Human search page", "Data catalog", "Agent start guide"],
        },
        {
            "path": "search-index.json",
            "markers": ['"count"', '"items"', "items"],
        },
        {
            "path": "data/works.json",
            "markers": ['"works"', '"count"'],
        },
        {
            "path": "data/agent-index.json",
            "markers": ['"schema_version"', '"routes"', '"datasets"'],
        },
        {
            "path": "data/catalog.json",
            "markers": ["DataCatalog", "External Link Triage", "Software"],
        },
        {
            "path": "GENERATED.md",
            "markers": ["# Generated Files", "Rebuild command", "Validation"],
        },
        {
            "path": "humans.txt",
            "markers": ["Daniel Ari Friedman", "docxology"],
        },
        {
            "path": ".well-known/security.txt",
            "markers": ["Contact:", "Policy:"],
        },
    ]

    if works is not None:
        checks[1]["markers"].append(f"{works} Research Works")
    if software_docx is not None:
        checks[2]["markers"].append(f"{software_docx} owned")
    if software_aii is not None:
        checks[2]["markers"].append(f"{software_aii} catalogued")
    if public_repos is not None:
        checks[2]["markers"].append(f"{public_repos} public repositories")

    return checks


def load_current_counts_fingerprint(
    current_counts_json: Path = CURRENT_COUNTS_JSON,
) -> dict[str, int | str | None]:
    """Return stable count fields from an explicit canonical-count source."""
    payload = _read_current_counts(current_counts_json)
    counts = payload.get("counts", {})
    software = counts.get("software", {})
    github_inventory = counts.get("github_inventory", {})
    return {
        "works": counts.get("bibliography_works"),
        "software_docx": software.get("docxology_owned"),
        "software_aii": software.get("active_inference_institute"),
        "software_total": software.get("curated_total"),
        "public_repos": github_inventory.get("public"),
    }


def count_fingerprint_matches(observed: dict, current: dict) -> bool:
    """Compare count fields while ignoring the local report build timestamp.

    The timestamp changes whenever generated artifacts are rebuilt; it is not a
    deployment invariant and made a valid live report look stale before this
    check was introduced. Legacy reports may still contain the timestamp, so
    compare only the stable count keys.
    """
    keys = {"works", "software_docx", "software_aii", "software_total", "public_repos"}
    return all(observed.get(key) == current.get(key) for key in keys)


def jsonld_types_in_html(text: str) -> set[str]:
    """Collect every ``@type`` value from the page's JSON-LD blocks.

    Structural rather than textual: the generator may re-serialize the JSON
    (spacing, key order) without changing meaning, and a raw-substring pin
    false-fails exactly then (2026-09-08: publications.html's compact
    ``"@type":"CollectionPage"`` vs a spaced expectation). Handles both
    top-level dicts and ``@graph`` arrays; ``@type`` may be a string or list.
    """
    types: set[str] = set()
    for match in re.finditer(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    ):
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        nodes = payload.get("@graph", [payload]) if isinstance(payload, dict) else payload
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            value = node.get("@type")
            if isinstance(value, str):
                types.add(value)
            elif isinstance(value, list):
                types.update(v for v in value if isinstance(v, str))
    return types


def parse_json_contract(
    path: str,
    text: str,
    fingerprint: dict,
    *,
    agent_index_json: Path = AGENT_INDEX_JSON,
) -> tuple[dict[str, bool], dict[str, int]]:
    """Parse live JSON routes and compare their counts to local canonical data."""
    if not path.endswith(".json"):
        return {}, {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"valid_json": False}, {}
    checks = {"valid_json": True}
    if not isinstance(payload, dict):
        return {**checks, "json_object": False}, {}
    observed: dict[str, int] = {}
    if path == "data/works.json":
        count = payload.get("count")
        observed["works"] = count if isinstance(count, int) else -1
        checks["works_count_matches"] = count == fingerprint.get("works")
    elif path == "data/software-ld.json":
        count = len(payload.get("mainEntity", [])) if isinstance(payload.get("mainEntity"), list) else -1
        observed["software_total"] = count
        checks["software_count_matches"] = count == fingerprint.get("software_total")
    elif path == "data/agent-index.json":
        expected_schema_version = _read_agent_index_schema_version(agent_index_json)
        checks["versioned_schema"] = (
            expected_schema_version is not None and payload.get("schema_version") == expected_schema_version
        )
        checks["routes_present"] = isinstance(payload.get("routes"), list) and bool(payload.get("routes"))
        checks["datasets_present"] = isinstance(payload.get("datasets"), dict) and bool(payload.get("datasets"))
        checks["dataset_hashes_present"] = isinstance(payload.get("dataset_hashes"), dict) and bool(payload.get("dataset_hashes"))
        raw_datasets = payload.get("datasets")
        datasets = raw_datasets if isinstance(raw_datasets, dict) else {}
        raw_works = datasets.get("works")
        works = raw_works if isinstance(raw_works, dict) else {}
        agent_works = works.get("count")
        observed["agent_works"] = agent_works if isinstance(agent_works, int) else -1
        checks["agent_works_match"] = agent_works == fingerprint.get("works")
    elif path == "search-index.json":
        items = payload.get("items")
        checks["items_present"] = isinstance(items, list)
        checks["count_matches_items"] = (
            isinstance(items, list) and payload.get("count") == len(items)
        )
    elif path == "data/catalog.json":
        # Schema.org DataCatalog uses the singular `dataset` property.
        checks["catalog_datasets_present"] = bool(payload.get("dataset") or payload.get("datasets"))
    return checks, observed


def fetch(url: str, timeout: int, extra_headers: dict[str, str] | None = None) -> dict:
    started = time.time()
    headers = {
        "User-Agent": "docxology-live-verify/1.0 (+https://danielarifriedman.com/)",
        "Cache-Control": "no-cache",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(
        url,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES)
            text = raw.decode("utf-8", errors="replace")
            return {
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "elapsed_ms": int((time.time() - started) * 1000),
                "bytes": len(raw),
                "headers": {k.lower(): v for k, v in response.headers.items()},
                "text": text,
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(200_000).decode("utf-8", errors="replace")
        return {
            "status": exc.code,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "bytes": len(body),
            "headers": dict(exc.headers.items()) if exc.headers else {},
            "text": body,
            "error": str(exc.reason),
        }
    except Exception as exc:
        return {
            "status": 0,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "bytes": 0,
            "headers": {},
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def cache_busted(url: str, attempt: int = 0) -> str:
    """Force each verification attempt through a fresh CDN cache key."""
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append(("__verify", f"{int(time.time())}-{attempt}"))
    return urllib.parse.urlunsplit(parsed._replace(query=urllib.parse.urlencode(query)))


def fetch_with_retries(url: str, timeout: int, attempts: int = 3) -> dict:
    last = None
    for attempt in range(attempts):
        last = fetch(cache_busted(url, attempt), timeout)
        if last["ok"]:
            return last
        if attempt < attempts - 1:
            time.sleep(2**attempt)
    return last or fetch(cache_busted(url), timeout)


def pages_status(timeout: int) -> dict:
    try:
        proc = subprocess.run(
            ["gh", "api", "repos/docxology/docxology/pages"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if proc.returncode == 0:
            payload = json.loads(proc.stdout)
            return {
                "ok": payload.get("status") == "built",
                "status": payload.get("status", ""),
                "deployment_pending": is_pages_deployment_pending(payload.get("status")),
                "cname": payload.get("cname", ""),
                "source": payload.get("source", {}),
                "html_url": payload.get("html_url", ""),
            }
    except Exception:
        pass
    url = "https://api.github.com/repos/docxology/docxology/pages"
    headers = {}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = fetch(url, timeout, headers)
    if not data["ok"]:
        return {"ok": False, "status": data["status"], "error": data["error"]}
    try:
        payload = json.loads(data["text"])
    except json.JSONDecodeError as exc:
        return {"ok": False, "status": data["status"], "error": str(exc)}
    return {
        "ok": payload.get("status") == "built",
        "status": payload.get("status", ""),
        "deployment_pending": is_pages_deployment_pending(payload.get("status")),
        "cname": payload.get("cname", ""),
        "source": payload.get("source", {}),
        "html_url": payload.get("html_url", ""),
    }


def latest_deployment_run(timeout: int, run_id: int | None = None) -> dict:
    """Read an exact triggering Pages run, or the latest successful main run.

    A workflow_run consumer must supply its triggering run ID rather than
    silently selecting a newer deployment while the verification is queued.
    """
    endpoint = (f"repos/docxology/docxology/actions/runs/{run_id}" if run_id is not None
                else "repos/docxology/docxology/actions/runs?branch=main&per_page=20")
    try:
        proc = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        payload = json.loads(proc.stdout) if proc.returncode == 0 else {}
        if not isinstance(payload, dict):
            return {}
        runs = [payload] if run_id is not None else payload.get("workflow_runs", [])
        if not isinstance(runs, list):
            return {}
        for run in runs:
            if not isinstance(run, dict):
                continue
            name = str(run.get("name") or run.get("display_title") or "")
            if run_id is None and (name != "Deploy bounded GitHub Pages artifact"
                                   or run.get("conclusion") != "success"):
                continue
            return {
                "workflow_run_id": run.get("id"),
                "workflow_name": name,
                "workflow_path": run.get("path"),
                "workflow_url": run.get("html_url"),
                "head_sha": run.get("head_sha"),
                "head_branch": run.get("head_branch"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "created_at": run.get("created_at"),
                "updated_at": run.get("updated_at"),
            }
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        pass
    return {}


def deployment_binding(run: dict, *, expected_commit: str | None,
                       source_commit: str, source_dirty: bool,
                       run_id: int | None = None) -> dict:
    """Keep candidate/run identity separate from route marker acceptance."""
    checks = {}
    if expected_commit is not None:
        checks = {
            "checkout_matches": source_commit == expected_commit,
            "source_clean": not source_dirty,
            "deployment_commit_matches": run.get("head_sha") == expected_commit,
            "deployment_completed": run.get("status") == "completed",
            "deployment_succeeded": run.get("conclusion") == "success",
            "main_branch": run.get("head_branch") == "main",
            "pages_workflow": (run.get("workflow_name") == "Deploy bounded GitHub Pages artifact"
                               and run.get("workflow_path") == ".github/workflows/pages.yml"),
        }
        if run_id is not None:
            checks["triggering_run_matches"] = run.get("workflow_run_id") == run_id
    return {
        "required": expected_commit is not None,
        "expected_commit": expected_commit,
        "requested_workflow_run_id": run_id,
        "ok": all(checks.values()),
        "checks": checks,
    }


def hard_failures(payload: dict) -> list[dict]:
    """Reject failures unless supported by explicit propagation evidence.

    A transport failure or upstream server error is never proof of propagation.
    Legacy successful reports may omit an explicit row ``ok`` field; their
    status and recorded contracts still have to pass.
    """
    failures = []
    if not isinstance(payload, dict):
        return [{"path": "report", "error": "Live-site verification report must be an object"}]

    def boolean_flags(record: dict, names: tuple[str, ...], path: str) -> bool:
        invalid = [name for name in names if name in record and not isinstance(record[name], bool)]
        if invalid:
            failures.append({"path": path, "error": "Flags must be booleans", "fields": invalid})
        return not invalid

    boolean_flags(payload, ("overall_ok", "source_dirty", "deployment_sha_mismatch",
                            "source_worktree_clean"), "report")
    pages = payload.get("github_pages", {})
    if not isinstance(pages, dict):
        failures.append({"path": "GitHub Pages API", "error": "Pages metadata must be an object"})
        pages = {}
    boolean_flags(pages, ("ok", "deployment_pending"), "GitHub Pages API")
    propagation = (payload.get("source_dirty") is True
                   or payload.get("deployment_sha_mismatch") is True
                   or is_pages_deployment_pending(pages.get("status")))
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        failures.append({"path": "report", "error": "Live-site verification report has no results"})
        results = []
    for item in results:
        if not isinstance(item, dict):
            failures.append({"path": "report", "error": "Invalid live-site result"})
            continue
        status = item.get("status", 0)
        status_ok = isinstance(status, int) and 200 <= status < 400
        path = item.get("path", item.get("url", "unknown"))
        flags_valid = boolean_flags(item, ("ok", "deployment_pending", "local_exists"), path)
        contracts = [item.get(key, {}) for key in ("markers", "json_checks", "jsonld_types")]
        contracts_valid = all(isinstance(contract, dict)
                              and all(isinstance(value, bool) for value in contract.values())
                              for contract in contracts)
        if not contracts_valid:
            failures.append({"path": path, "error": "Recorded contracts must contain boolean values"})
        contracts_ok = contracts_valid and all(all(value is True for value in contract.values())
                                              for contract in contracts)
        ok = status_ok and contracts_ok and item.get("ok", True) is True
        pending = (flags_valid and contracts_valid and propagation and item.get("deployment_pending") is True
                   and status in {200, 404}
                   and (status != 404 or item.get("local_exists") is True))
        if not ok and not pending:
            failures.append({"path": item.get("path", item.get("url", "unknown")),
                             "status": status, "error": item.get("error", "Live route contract failed")})
    if pages and pages.get("ok") is not True and not is_pages_deployment_pending(pages.get("status")):
        failures.append({"path": "GitHub Pages API", "status": pages.get("status")})
    binding = payload.get("deployment_binding", {})
    if not isinstance(binding, dict):
        failures.append({"path": "deployment binding", "error": "Deployment binding must be an object"})
        binding = {}
    boolean_flags(binding, ("required", "ok"), "deployment binding")
    binding_checks = binding.get("checks", {})
    binding_checks_valid = (isinstance(binding_checks, dict)
                            and all(isinstance(value, bool) for value in binding_checks.values()))
    if not binding_checks_valid:
        failures.append({"path": "deployment binding", "error": "Binding checks must contain boolean values"})
    binding_ok = (binding.get("ok") is True and binding_checks_valid and bool(binding_checks)
                  and all(value is True for value in binding_checks.values()))
    if binding.get("required") is True and not binding_ok:
        failures.append({"path": "deployment binding", "checks": binding.get("checks", {})})
    if payload.get("overall_ok") is not True and not propagation and not failures:
        failures.append({"path": "report", "error": "Report is not passing and has no propagation evidence"})
    return failures


def local_source_commit(repo_root: Path = REPO_ROOT) -> str:
    """Return the checked-out commit used to generate the expected contract."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def local_source_dirty(repo_root: Path = REPO_ROOT) -> bool:
    """Return whether uncommitted source changes can differ from Pages.

    Use the same narrow source-versus-evidence distinction as release
    attestation.  Fresh post-commit browser, link, source, live-site, and
    attestation receipts describe the deployed candidate; they do not make a
    Pages deployment pending.  Unrecognized source changes still do.
    """
    return source_worktree_state(repo_root).get("source_worktree_clean") is not True


def build_report(
    timeout: int,
    *,
    repo_root: Path = REPO_ROOT,
    current_counts_json: Path = CURRENT_COUNTS_JSON,
    agent_index_json: Path = AGENT_INDEX_JSON,
    expected_commit: str | None = None,
    deployment_run_id: int | None = None,
) -> dict:
    """Build a live-site report against explicit local source paths."""
    checks = load_dynamic_checks(current_counts_json)
    fingerprint = load_current_counts_fingerprint(current_counts_json)
    results = []
    observed_counts: dict[str, int] = {}
    for check in checks:
        url = BASE + check["path"]
        response = fetch_with_retries(url, timeout)
        markers = {marker: marker in response["text"] for marker in check["markers"]}
        live_types = jsonld_types_in_html(response["text"]) if check.get("jsonld_types") else set()
        cache = {
            key: response["headers"].get(key, "")
            for key in ("last-modified", "etag", "cache-control", "age", "x-cache", "x-served-by")
        }
        json_checks, observed = parse_json_contract(
            check["path"],
            response["text"],
            fingerprint,
            agent_index_json=agent_index_json,
        )
        observed_counts.update(observed)
        ok = response["ok"] and all(markers.values()) and all(json_checks.values()) and all(
            t in live_types for t in check.get("jsonld_types", ())
        )
        results.append(
            {
                "path": check["path"] or "index.html",
                "url": url,
                "jsonld_types": {t: t in live_types for t in check.get("jsonld_types", ())},
                "ok": ok,
                "status": response["status"],
                "bytes": response["bytes"],
                "elapsed_ms": response["elapsed_ms"],
                "markers": markers,
                "json_checks": json_checks,
                "observed_counts": observed,
                "cache": cache,
                "error": response["error"],
            }
        )

    pages = pages_status(timeout)
    pages["deployment_run"] = (latest_deployment_run(timeout, deployment_run_id)
                               if deployment_run_id is not None else latest_deployment_run(timeout))
    source_commit = local_source_commit(repo_root)
    source_state = source_worktree_state(repo_root)
    source_dirty = source_state.get("source_worktree_clean") is not True
    deployed_commit = pages.get("deployment_run", {}).get("head_sha", "")
    deployment_sha_mismatch = bool(source_commit and deployed_commit and source_commit != deployed_commit)
    deployment_pending = (deployment_sha_mismatch or source_dirty
                          or is_pages_deployment_pending(pages.get("status")))
    binding = deployment_binding(pages["deployment_run"], expected_commit=expected_commit,
                                 source_commit=source_commit, source_dirty=source_dirty,
                                 run_id=deployment_run_id)
    # Same-candidate missing routes after a built deployment are real failures.
    # Only explicit source/deployment lag may defer 200 contract mismatches or
    # locally present 404s; network and server errors remain hard failures.
    pending_paths = []
    for item in results:
        item["local_exists"] = (repo_root / item["path"]).is_file()
        item["deployment_pending"] = bool(
            deployment_pending and not item["ok"] and item["status"] in {200, 404}
            and (item["status"] != 404 or item["local_exists"])
            and (pages.get("ok") or is_pages_deployment_pending(pages.get("status")))
        )
        if item["deployment_pending"]:
            pending_paths.append(item["path"])
    return {
        "generated_at": generated_timestamp(),
        "base_url": BASE,
        "expected_counts": fingerprint,
        "note": "Live verification can fail while GitHub Pages is still building or CDN caches are stale.",
        "github_pages": pages,
        "deployment": pages.get("deployment_run", {}),
        "deployment_binding": binding,
        "source_commit": source_commit,
        "source_dirty": source_dirty,
        **source_state,
        "deployment_sha_mismatch": deployment_sha_mismatch,
        "deployment_pending_reason": (
            "local source is dirty, selected Pages deployment is for a different commit, or Pages is building/queued"
            if deployment_pending
            else ""
        ),
        "observed_counts": observed_counts,
        "deployment_pending_paths": pending_paths,
        "checked_urls": len(results),
        "passing": sum(1 for item in results if item["ok"]),
        "overall_ok": (pages.get("ok", False) and all(item["ok"] for item in results)
                       and not deployment_pending and binding["ok"]),
        "results": results,
    }


def main(
    argv: list[str] | None = None,
    *,
    repo_root: Path = REPO_ROOT,
    current_counts_json: Path = CURRENT_COUNTS_JSON,
    agent_index_json: Path = AGENT_INDEX_JSON,
    report_dir: Path | None = None,
) -> None:
    """Run the CLI with production defaults or explicit local test paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate the cached report exists and is parseable")
    parser.add_argument(
        "--allow-source-count-drift",
        action="store_true",
        help=(
            "Permit a cached pre-deploy report to have different local count inputs; "
            "use only for offline candidate validation."
        ),
    )
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--expected-commit", help="Require an exact clean checkout and successful Pages deployment SHA")
    parser.add_argument("--deployment-run-id", type=int, help="Verify the exact triggering Pages workflow run")
    parser.add_argument("--output", type=Path, help="Write a dedicated receipt instead of a dated source-tree report")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.timeout > 60:
        parser.error("timeout must be 1..60 seconds")
    if args.expected_commit and not re.fullmatch(r"[0-9a-f]{40}", args.expected_commit):
        parser.error("expected commit must be a full lowercase Git SHA")
    if args.deployment_run_id is not None and (args.deployment_run_id <= 0 or not args.expected_commit):
        parser.error("deployment run ID must be positive and requires --expected-commit")
    if args.expected_commit and args.expected_commit != local_source_commit(repo_root):
        parser.error("expected commit must equal checkout HEAD")
    if args.check and (args.expected_commit or args.deployment_run_id is not None):
        parser.error("candidate/run binding requires fresh verification, not --check")
    resolved_report_dir = report_dir or repo_root / "reports"
    current_fingerprint = load_current_counts_fingerprint(current_counts_json)
    if args.check:
        if not current_counts_json.exists():
            raise SystemExit("Current-counts source missing: data/current-counts.json")
        out = latest_report("live_site_verification_*.json", report_dir=resolved_report_dir)
        if out is None or not out.exists():
            raise SystemExit("Missing live-site verification report")
        payload = json.loads(out.read_text(encoding="utf-8"))
        fingerprint_matches = count_fingerprint_matches(payload.get("expected_counts", {}), current_fingerprint)
        if not fingerprint_matches and not args.allow_source_count_drift:
            raise SystemExit(
                f"Live-site verification counts snapshot mismatch: expected={current_fingerprint} got={payload.get('expected_counts')}"
            )
        failures = hard_failures(payload)
        if failures:
            raise SystemExit(f"Live-site verification hard failures: {failures}")
        if not payload.get("overall_ok"):
            print(
                "checked live-site verification report "
                f"({payload.get('passing')}/{payload.get('checked_urls')} passing; "
                f"deployment pending for {len(payload.get('deployment_pending_paths', []))} route(s) or live markers; "
                "live markers pending deploy)"
            )
            return
        if not fingerprint_matches:
            print(
                "checked cached live-site verification report with pre-deploy count drift "
                f"({payload['passing']}/{payload['checked_urls']} passing)"
            )
            return
        print(f"checked live-site verification report ({payload['passing']}/{payload['checked_urls']} passing)")
        return
    payload = build_report(
        args.timeout,
        repo_root=repo_root,
        current_counts_json=current_counts_json,
        agent_index_json=agent_index_json,
        expected_commit=args.expected_commit,
        deployment_run_id=args.deployment_run_id,
    )
    out = args.output or dated_report_path("live_site_verification", "json", report_dir=resolved_report_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote live-site verification report: {payload['passing']}/{payload['checked_urls']} passing; pages={payload['github_pages'].get('status', 'unknown')}")
    if args.expected_commit and (failures := hard_failures(payload)):
        raise SystemExit(f"Live-site verification hard failures: {failures}")


if __name__ == "__main__":
    main()
