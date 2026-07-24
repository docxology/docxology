"""Tests for live-site verification payload checks."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

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


def _write_report(path: Path, payload: dict, *, overall_ok: bool = True, expected_counts: dict | None = None) -> None:
    report_payload = {
        "generated_at": "2026-06-16T03:36:11Z",
        "expected_counts": expected_counts if expected_counts is not None else vl.load_current_counts_fingerprint(),
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


def test_load_dynamic_checks_uses_current_counts(monkeypatch, tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    payload = _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)

    checks = vl.load_dynamic_checks()

    pubs = next(check for check in checks if check["path"] == "publications.html")
    software = next(check for check in checks if check["path"] == "software.html")
    software_export = next(check for check in checks if check["path"] == "data/software-ld.json")

    assert any("168 Research Works" in marker for marker in pubs["markers"])
    assert any("58 owned" in marker for marker in software["markers"])
    assert any("33 catalogued" in marker for marker in software["markers"])
    assert any(f"{payload['counts']['github_inventory']['public']} public repositories" in marker for marker in software["markers"])
    assert '"@type":"CollectionPage"' in software["markers"]
    assert '"SoftwareSourceCode"' in software_export["markers"]


def test_cache_busted_url_preserves_path_and_adds_unique_query():
    url = vl.cache_busted("https://example.test/data/works.json?v=1", attempt=2)
    assert url.startswith("https://example.test/data/works.json?")
    assert "v=1" in url
    assert "__verify=" in url


def test_catalog_json_contract_accepts_schema_org_dataset_property():
    checks, observed = vl.parse_json_contract(
        "data/catalog.json",
        json.dumps({"@type": "DataCatalog", "dataset": [{"name": "works"}]}),
        {},
    )
    assert checks["valid_json"]
    assert checks["catalog_datasets_present"]
    assert observed == {}


def test_agent_index_contract_uses_current_generated_schema_version(monkeypatch, tmp_path):
    agent_index_path = tmp_path / "data" / "agent-index.json"
    agent_index_path.parent.mkdir(parents=True, exist_ok=True)
    agent_index_path.write_text(json.dumps({"schema_version": "1.3"}), encoding="utf-8")
    monkeypatch.setattr(vl, "AGENT_INDEX_JSON", agent_index_path)

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
    ("status_output", "expected"),
    [
        ("?? _site/\n", False),
        ("?? _site/index.html\n", False),
        (" M README.md\n", True),
        ("?? _site/index.html\n M README.md\n", True),
    ],
)
def test_local_source_dirty_ignores_preserved_site_output(monkeypatch, status_output, expected):
    monkeypatch.setattr(
        vl.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=status_output),
    )

    assert vl.local_source_dirty() is expected


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


def test_verify_live_site_check_command_validates_fingerprint(monkeypatch, tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(report_path, {}, expected_counts=vl.load_current_counts_fingerprint())

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    vl.main()
    output = capsys.readouterr().out
    assert "checked live-site verification report" in output


def test_verify_live_site_check_allows_marker_only_deploy_lag(monkeypatch, tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(report_path, {}, overall_ok=False, expected_counts=vl.load_current_counts_fingerprint())

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    vl.main()
    output = capsys.readouterr().out
    assert "live markers pending deploy" in output


def test_verify_live_site_check_fails_on_http_error(monkeypatch, tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(
        report_path,
        {"results": [{"status": 200}, {"status": 500, "url": "https://example.test/bad"}]},
        overall_ok=False,
        expected_counts=vl.load_current_counts_fingerprint(),
    )

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    with pytest.raises(SystemExit, match="Live-site page failure"):
        vl.main()


def test_verify_live_site_check_allows_local_404_during_built_pages_deploy(monkeypatch, tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    local_route = tmp_path / "data" / "agent-index.json"
    local_route.parent.mkdir(parents=True, exist_ok=True)
    local_route.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    monkeypatch.setattr(vl, "REPO_ROOT", tmp_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(
        report_path,
        {
            "github_pages": {"ok": True, "status": "built"},
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
        expected_counts=vl.load_current_counts_fingerprint(),
    )

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    vl.main()
    output = capsys.readouterr().out
    assert "deployment pending" in output


def test_verify_live_site_check_fails_when_fingerprint_drifted(monkeypatch, tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    drifted = vl.load_current_counts_fingerprint().copy()
    drifted["works"] = 999
    _write_report(report_path, {"expected_counts": drifted}, expected_counts=drifted)

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    with pytest.raises(SystemExit):
        vl.main()
