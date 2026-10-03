"""Tests for live-site verification payload checks."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

import verify_live_site as vl  # noqa: E402


def _write_current_counts(path: Path) -> dict:
    payload = {
        "generated_at": "2026-06-16T03:36:11+00:00",
        "counts": {
            "bibliography_works": 168,
            "software": {
                "docxology_owned": 58,
                "active_inference_institute": 33,
            },
            "github_inventory": {
                "public": 360,
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _write_report(path: Path, payload: dict, *, overall_ok: bool = True, expected_counts: dict) -> None:
    report_payload = {
        "generated_at": "2026-06-16T03:36:11Z",
        "expected_counts": expected_counts,
        "results": [
            {"status": 200},
            {"status": 200},
            {"status": 200},
        ],
        "overall_ok": overall_ok,
        "passing": 3,
        "checked_urls": 3,
    }
    report_payload.update(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_payload, indent=2), encoding="utf-8")


def test_load_dynamic_checks_uses_current_counts(tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    payload = _write_current_counts(counts_path)

    checks = vl.load_dynamic_checks(counts_path)

    pubs = next(check for check in checks if check["path"] == "publications.html")
    software = next(check for check in checks if check["path"] == "software.html")
    software_export = next(check for check in checks if check["path"] == "data/software-ld.json")

    assert any("168 Research Works" in marker for marker in pubs["markers"])
    assert any("58 owned" in marker for marker in software["markers"])
    assert any("33 catalogued" in marker for marker in software["markers"])
    assert any(f"{payload['counts']['github_inventory']['public']} public repositories" in marker for marker in software["markers"])
    assert pubs["jsonld_types"] == ["CollectionPage"]
    assert software["jsonld_types"] == ["CollectionPage"]
    assert '"@type"' not in json.dumps(pubs["markers"])
    assert '"SoftwareSourceCode"' in software_export["markers"]


def test_cache_busted_url_preserves_path_and_adds_unique_query():
    url = vl.cache_busted("https://example.test/data/works.json?v=1", attempt=2)
    assert url.startswith("https://example.test/data/works.json?")
    assert "v=1" in url
    assert "__verify=" in url
def test_json_contract_survives_large_index_fetch(monkeypatch):
    """search-index.json outgrew the old 2 MB read cap in verify_live_site.fetch,
    which truncated the fetch and failed valid_json on the live route. The cap
    (MAX_RESPONSE_BYTES) must exceed the deployed index size and be used by fetch."""
    old_cap = 2_000_000
    assert vl.MAX_RESPONSE_BYTES > old_cap
    # Pad the item list so the payload is larger than the old cap: a fetch still
    # capped at 2 MB would truncate mid-JSON and fail to parse.
    filler = "x" * 512
    items = [{"title": filler} for _ in range((old_cap + 500_000) // 532)]
    payload = json.dumps({"generated_at": "x", "count": len(items), "items": items}).encode()
    assert len(payload) > old_cap

    class FakeResponse:
        status = 200
        headers = {}

        def read(self, amount=-1):
            return payload if amount >= len(payload) else payload[:amount]

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        return FakeResponse()

    monkeypatch.setattr(vl.urllib.request, "urlopen", fake_urlopen)
    result = vl.fetch("https://example.test/search-index.json", timeout=10)
    assert result["bytes"] == len(payload)
    checks, observed = vl.parse_json_contract("search-index.json", result["text"], {})
    assert checks == {"valid_json": True, "items_present": True, "count_matches_items": True}


def test_jsonld_types_in_html_parses_graph_and_list_types():
    html = """
    <script type="application/ld+json">
    {"@context": "https://schema.org", "@graph": [
      {"@type": ["CollectionPage", "WebPage"], "name": "Publications"},
      {"@type": "Person", "name": "D"}
    ]}
    </script>
    <script type="application/ld+json">{"@type": "BreadcrumbList", "itemListElement": []}</script>
    <script type="application/ld+json">this is not json</script>
    <script>console.log("not ld+json")</script>
    """
    assert vl.jsonld_types_in_html(html) == {"CollectionPage", "WebPage", "Person", "BreadcrumbList"}


def test_jsonld_types_in_html_empty_and_no_blocks():
    assert vl.jsonld_types_in_html("") == set()
    assert vl.jsonld_types_in_html("<html><body>no ld+json here</body></html>") == set()


def test_jsonld_specs_match_committed_publications_page():
    """The structural pin must hold against the real generated artifact."""
    html = (vl.REPO_ROOT / "publications.html").read_text(encoding="utf-8")
    assert "CollectionPage" in vl.jsonld_types_in_html(html)


def test_catalog_json_contract_accepts_schema_org_dataset_property():
    checks, observed = vl.parse_json_contract(
        "data/catalog.json",
        json.dumps({"@type": "DataCatalog", "dataset": [{"name": "works"}]}),
        {},
    )
    assert checks["valid_json"]
    assert checks["catalog_datasets_present"]
    assert observed == {}


def test_agent_index_contract_uses_current_generated_schema_version(tmp_path):
    agent_index_path = tmp_path / "data" / "agent-index.json"
    agent_index_path.parent.mkdir(parents=True, exist_ok=True)
    agent_index_path.write_text(json.dumps({"schema_version": "1.3"}), encoding="utf-8")
    checks, observed = vl.parse_json_contract(
        "data/agent-index.json",
        json.dumps(
            {
                "schema_version": "1.3",
                "routes": [{"id": "agent-index"}],
                "datasets": {"works": {"count": 196}},
                "dataset_hashes": {"works": "sha256:example"},
            }
        ),
        {"works": 196},
        agent_index_json=agent_index_path,
    )

    assert checks["versioned_schema"]
    assert checks["routes_present"]
    assert checks["datasets_present"]
    assert checks["dataset_hashes_present"]
    assert checks["agent_works_match"]
    assert observed == {"agent_works": 196}


@pytest.mark.parametrize("status", ["building", "queued", "BUILDING"])
def test_pages_build_states_are_deployment_pending(status):
    assert vl.is_pages_deployment_pending(status)


def test_pages_built_is_not_deployment_pending():
    assert not vl.is_pages_deployment_pending("built")


@pytest.mark.parametrize(
    ("untracked_paths", "expected"),
    [
        (["_site"], False),
        (["_site/index.html"], False),
        (["_site/art/name with spaces.json"], False),
        (["reports/external_links_2026-08-25.json"], False),
        (["reports/browser-smoke/2026-08-25/manifest.json"], False),
        (["README.md"], True),
        (["reports/external_links_triage_2026-08-25.json"], False),
        (["reports/external_links_triage_2026-08-25.md"], False),
        (["reports/external_links_triage_2026-08-25.txt"], True),
        (["_site/index.html", "README.md"], True),
    ],
)
def test_local_source_dirty_uses_the_release_evidence_allowlist(tmp_path, untracked_paths, expected):
    initialized = subprocess.run(
        ["git", "init", "--quiet"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert initialized.returncode == 0, initialized.stderr
    for relative in untracked_paths:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")

    assert vl.local_source_dirty(tmp_path) is expected


def test_count_fingerprint_ignores_generated_timestamp():
    current = {
        "works": 194,
        "software_docx": 61,
        "software_aii": 34,
        "software_total": 95,
        "public_repos": 379,
    }
    observed = {**current, "generated_at": "2026-07-16T04:35:51+00:00"}
    assert vl.count_fingerprint_matches(observed, current)


def test_verify_live_site_check_command_validates_fingerprint(tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(report_path, {}, expected_counts=vl.load_current_counts_fingerprint(counts_path))

    vl.main(["--check"], current_counts_json=counts_path, report_dir=report_path.parent)
    output = capsys.readouterr().out
    assert "checked live-site verification report" in output


def test_verify_live_site_check_allows_marker_only_deploy_lag(tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(
        report_path,
        {
            "deployment_sha_mismatch": True,
            "deployment_pending_paths": ["index.html"],
            "results": [{"path": "index.html", "status": 200, "ok": False,
                         "markers": {"new candidate marker": False}, "deployment_pending": True}],
        },
        overall_ok=False,
        expected_counts=vl.load_current_counts_fingerprint(counts_path),
    )

    vl.main(["--check"], current_counts_json=counts_path, report_dir=report_path.parent)
    output = capsys.readouterr().out
    assert "live markers pending deploy" in output


def test_verify_live_site_check_fails_on_http_error(tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(
        report_path,
        {"results": [{"status": 200}, {"status": 500, "url": "https://example.test/bad"}]},
        overall_ok=False,
        expected_counts=vl.load_current_counts_fingerprint(counts_path),
    )

    with pytest.raises(SystemExit, match="hard failures"):
        vl.main(["--check"], current_counts_json=counts_path, report_dir=report_path.parent)


def test_verify_live_site_check_allows_local_404_during_built_pages_deploy(tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(
        report_path,
        {
            "github_pages": {"ok": True, "status": "built"},
            "deployment_sha_mismatch": True,
            "deployment_pending_paths": ["data/agent-index.json"],
            "results": [
                {
                    "status": 404,
                    "url": "https://example.test/data/agent-index.json",
                    "path": "data/agent-index.json",
                    "local_exists": True,
                    "deployment_pending": True,
                }
            ],
        },
        overall_ok=False,
        expected_counts=vl.load_current_counts_fingerprint(counts_path),
    )

    vl.main(["--check"], current_counts_json=counts_path, report_dir=report_path.parent)
    output = capsys.readouterr().out
    assert "deployment pending" in output


def test_verify_live_site_check_fails_when_fingerprint_drifted(tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    drifted = vl.load_current_counts_fingerprint(counts_path).copy()
    drifted["works"] = 999
    _write_report(report_path, {"expected_counts": drifted}, expected_counts=drifted)

    with pytest.raises(SystemExit):
        vl.main(["--check"], current_counts_json=counts_path, report_dir=report_path.parent)


def test_verify_live_site_check_allows_stale_fingerprint_for_offline_candidate(tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    drifted = vl.load_current_counts_fingerprint(counts_path).copy()
    drifted["software_total"] = 999
    _write_report(report_path, {"expected_counts": drifted}, expected_counts=drifted)

    vl.main(
        ["--check", "--allow-source-count-drift"],
        current_counts_json=counts_path,
        report_dir=report_path.parent,
    )

    assert "pre-deploy count drift" in capsys.readouterr().out


@pytest.mark.parametrize("status", [0, 500, 503])
def test_transport_and_server_failures_never_become_propagation(status):
    payload = {
        "overall_ok": False,
        "source_dirty": True,
        "deployment_sha_mismatch": True,
        "github_pages": {"ok": True, "status": "built"},
        "results": [{"path": "index.html", "status": status, "ok": False,
                     "deployment_pending": True}],
    }
    assert vl.hard_failures(payload)[0]["path"] == "index.html"


@pytest.mark.parametrize("row", [
    {"status": 0, "ok": False, "error": "network timeout"},
    {"status": 200, "ok": False, "markers": {"expected heading": False}},
    {"status": 200, "jsonld_types": {"CollectionPage": False}},
])
def test_cached_unclassified_failure_is_rejected(tmp_path, row):
    counts = tmp_path / "data/current-counts.json"
    _write_current_counts(counts)
    report = tmp_path / "reports/live_site_verification_2026-06-16.json"
    _write_report(report, {"results": [{"path": "index.html", **row}]}, overall_ok=False,
                  expected_counts=vl.load_current_counts_fingerprint(counts))
    with pytest.raises(SystemExit, match="hard failures"):
        vl.main(["--check"], current_counts_json=counts, report_dir=report.parent)


def test_pending_flag_alone_cannot_defer_same_candidate_404():
    payload = {"overall_ok": False, "github_pages": {"ok": True, "status": "built"},
               "results": [{"path": "index.html", "status": 404, "ok": False,
                            "local_exists": True, "deployment_pending": True}]}
    assert vl.hard_failures(payload)[0]["path"] == "index.html"


@pytest.fixture
def live_candidate(tmp_path, monkeypatch):
    counts = tmp_path / "data/current-counts.json"
    _write_current_counts(counts)
    (tmp_path / "index.html").write_text("candidate heading", encoding="utf-8")
    run = {"workflow_run_id": 101, "workflow_name": "Deploy bounded GitHub Pages artifact",
           "workflow_path": ".github/workflows/pages.yml", "head_sha": "a" * 40,
           "head_branch": "main", "status": "completed", "conclusion": "success"}
    response = {"status": 200, "ok": True, "text": "candidate heading", "headers": {},
                "bytes": 17, "elapsed_ms": 1, "error": ""}
    monkeypatch.setattr(vl, "load_dynamic_checks", lambda _: [{"path": "", "markers": ["candidate heading"]}])
    monkeypatch.setattr(vl, "fetch_with_retries", lambda *_: response)
    monkeypatch.setattr(vl, "pages_status", lambda _: {"ok": True, "status": "built"})
    monkeypatch.setattr(vl, "latest_deployment_run", lambda *_: run)
    monkeypatch.setattr(vl, "local_source_commit", lambda *_: "a" * 40)
    monkeypatch.setattr(vl, "source_worktree_state", lambda *_: {"source_worktree_clean": True})
    return tmp_path, counts, run, response


def test_same_candidate_built_deployment_missing_route_is_hard_failure(live_candidate):
    root, counts, _, response = live_candidate
    response.update(status=404, ok=False, text="not found")
    report = vl.build_report(1, repo_root=root, current_counts_json=counts,
                             expected_commit="a" * 40, deployment_run_id=101)
    assert report["deployment_binding"]["ok"]
    assert not report["deployment_sha_mismatch"]
    assert not report["results"][0]["deployment_pending"]
    assert vl.hard_failures(report)[0]["path"] == "index.html"


def test_actual_predeploy_missing_route_remains_explicitly_pending(live_candidate):
    root, counts, run, response = live_candidate
    run["head_sha"] = "b" * 40
    response.update(status=404, ok=False, text="not found")
    report = vl.build_report(1, repo_root=root, current_counts_json=counts)
    assert report["deployment_sha_mismatch"]
    assert report["results"][0]["deployment_pending"]
    assert not report["overall_ok"]
    assert vl.hard_failures(report) == []


@pytest.mark.parametrize("status", [0, 500])
def test_build_report_keeps_transport_errors_hard_during_predeploy(live_candidate, status):
    root, counts, run, response = live_candidate
    run["head_sha"] = "b" * 40
    response.update(status=status, ok=False, text="failure")
    report = vl.build_report(1, repo_root=root, current_counts_json=counts)
    assert not report["results"][0]["deployment_pending"]
    assert vl.hard_failures(report)


def test_triggering_candidate_and_run_binding_passes(live_candidate, monkeypatch):
    root, counts, run, _ = live_candidate
    requested = []
    monkeypatch.setattr(vl, "latest_deployment_run", lambda timeout, run_id: requested.append(run_id) or run)
    report = vl.build_report(1, repo_root=root, current_counts_json=counts,
                             expected_commit="a" * 40, deployment_run_id=101)
    assert requested == [101]
    assert report["deployment_binding"]["ok"]
    assert report["overall_ok"]
    assert vl.hard_failures(report) == []


@pytest.mark.parametrize("field,value", [
    ("head_sha", "b" * 40), ("workflow_run_id", 102), ("head_branch", "feature"),
    ("status", "in_progress"), ("conclusion", "failure"),
    ("workflow_path", ".github/workflows/other.yml"), ("workflow_name", "Other workflow"),
])
def test_mismatched_deployment_identity_fails_even_when_routes_pass(live_candidate, field, value):
    root, counts, run, _ = live_candidate
    run[field] = value
    report = vl.build_report(1, repo_root=root, current_counts_json=counts,
                             expected_commit="a" * 40, deployment_run_id=101)
    assert report["results"][0]["ok"]
    assert not report["deployment_binding"]["ok"]
    assert not report["overall_ok"]
    assert any(item["path"] == "deployment binding" for item in vl.hard_failures(report))


def test_exact_run_lookup_does_not_select_floating_latest(monkeypatch):
    commands = []
    run = {"id": 101, "name": "Deploy bounded GitHub Pages artifact", "head_sha": "a" * 40,
           "path": ".github/workflows/pages.yml", "head_branch": "main", "status": "completed",
           "conclusion": "success"}
    def run_api(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(run), stderr="")
    monkeypatch.setattr(vl.subprocess, "run", run_api)
    observed = vl.latest_deployment_run(1, run_id=101)
    assert commands == [["gh", "api", "repos/docxology/docxology/actions/runs/101"]]
    assert observed["workflow_run_id"] == 101
    assert observed["head_sha"] == "a" * 40


def test_failed_candidate_verification_retains_dedicated_receipt(live_candidate):
    root, counts, _, response = live_candidate
    response.update(status=404, ok=False, text="not found")
    output = root / "private-evidence/live.json"
    with pytest.raises(SystemExit, match="hard failures"):
        vl.main(["--expected-commit", "a" * 40, "--deployment-run-id", "101", "--output", str(output)],
                repo_root=root, current_counts_json=counts)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["source_commit"] == "a" * 40
    assert not payload["overall_ok"]
    assert not (root / "reports").exists()


def test_non_object_live_json_records_failed_contract_instead_of_raising():
    checks, observed = vl.parse_json_contract("data/works.json", '[]', {"works": 1})
    assert checks == {"valid_json": True, "json_object": False}
    assert observed == {}


def _successful_typed_report() -> dict:
    return {
        "overall_ok": True, "source_dirty": False, "deployment_sha_mismatch": False,
        "source_worktree_clean": True,
        "github_pages": {"ok": True, "status": "built", "deployment_pending": False},
        "deployment_binding": {"required": False, "ok": True, "checks": {}},
        "results": [{"path": "index.html", "status": 200, "ok": True,
                     "deployment_pending": False, "local_exists": True,
                     "markers": {"required heading": True},
                     "json_checks": {"valid_json": True},
                     "jsonld_types": {"WebPage": True}}],
    }


@pytest.mark.parametrize("path,value", [
    (("overall_ok",), "false"), (("overall_ok",), "true"), (("overall_ok",), 1),
    (("overall_ok",), 0), (("overall_ok",), None),
    (("source_dirty",), "false"), (("deployment_sha_mismatch",), 1),
    (("source_worktree_clean",), "true"),
    (("github_pages", "ok"), "true"), (("github_pages", "deployment_pending"), "false"),
    (("results", 0, "ok"), 1), (("results", 0, "deployment_pending"), 0),
    (("results", 0, "local_exists"), "true"),
    (("results", 0, "markers", "required heading"), "false"),
    (("results", 0, "markers", "required heading"), 1),
    (("results", 0, "json_checks", "valid_json"), "true"),
    (("results", 0, "jsonld_types", "WebPage"), "false"),
    (("results", 0, "markers"), None),
    (("deployment_binding", "required"), "false"), (("deployment_binding", "ok"), 1),
    (("deployment_binding", "checks"), {"checkout_matches": "false"}),
    (("github_pages",), []), (("deployment_binding",), None),
])
def test_cached_malformed_boolean_fields_are_rejected_by_check(tmp_path, path, value):
    counts = tmp_path / "data/current-counts.json"
    _write_current_counts(counts)
    payload = _successful_typed_report()
    record = payload
    for part in path[:-1]:
        record = record[part]
    record[path[-1]] = value
    report = tmp_path / "reports/live_site_verification_2026-06-16.json"
    _write_report(report, payload, expected_counts=vl.load_current_counts_fingerprint(counts))
    with pytest.raises(SystemExit, match="hard failures"):
        vl.main(["--check"], current_counts_json=counts, report_dir=report.parent)


def test_malformed_contract_cannot_hide_behind_valid_propagation_flags(tmp_path):
    counts = tmp_path / "data/current-counts.json"
    _write_current_counts(counts)
    payload = _successful_typed_report()
    payload.update(overall_ok=False, source_dirty=True)
    payload["results"][0].update(ok=False, deployment_pending=True,
                                 markers={"required heading": "false"})
    report = tmp_path / "reports/live_site_verification_2026-06-16.json"
    _write_report(report, payload, expected_counts=vl.load_current_counts_fingerprint(counts))
    with pytest.raises(SystemExit, match="boolean values"):
        vl.main(["--check"], current_counts_json=counts, report_dir=report.parent)


@pytest.mark.parametrize("checks", [{"checkout_matches": False}, {}])
def test_required_binding_cannot_claim_success_with_failed_or_missing_checks(tmp_path, checks):
    counts = tmp_path / "data/current-counts.json"
    _write_current_counts(counts)
    payload = _successful_typed_report()
    payload["deployment_binding"] = {"required": True, "ok": True, "checks": checks}
    report = tmp_path / "reports/live_site_verification_2026-06-16.json"
    _write_report(report, payload, expected_counts=vl.load_current_counts_fingerprint(counts))
    with pytest.raises(SystemExit, match="deployment binding"):
        vl.main(["--check"], current_counts_json=counts, report_dir=report.parent)


def test_legacy_successful_row_without_ok_remains_accepted():
    payload = _successful_typed_report()
    del payload["results"][0]["ok"]
    assert vl.hard_failures(payload) == []
