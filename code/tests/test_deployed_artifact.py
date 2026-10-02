"""Real HTTP checks for deployment hashes, HEAD contracts and failure scope."""
from __future__ import annotations

from functools import partial
import hashlib
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import subprocess
import threading
import time

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import verify_deployed_artifact as verifier  # noqa: E402


@pytest.fixture
def deployed(tmp_path):
    files = []
    for path in sorted(verifier.CRITICAL_PATHS | {"works/example.html", "papers/example/source.pdf"}):
        body = b"%PDF-1.4\nsource" if path.endswith(".pdf") else path.encode()
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        files.append({"path": path, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
    manifest = {"source_commit_at_generation": "a" * 40, "included_files": files}
    manifest_path = tmp_path / verifier.MANIFEST_PATH
    manifest_path.write_text(json.dumps(manifest))
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *_):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(tmp_path)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield tmp_path, manifest_path, f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_actual_deployment_hashes_and_pdf_head_pass(deployed):
    _, manifest_path, origin = deployed
    receipt = verifier.check_deployment(manifest_path, commit="b" * 40, attempts=1, origin=origin)
    assert receipt["overall_ok"]
    assert receipt["source_commit"] == "b" * 40
    assert receipt["source_payload_commit"] == "a" * 40
    assert receipt["scope"]["paper_pdf_heads"] == 1
    assert receipt["scope"]["full_release_attestation"] is False
    assert receipt["passing"] == receipt["checked"]


def test_changed_live_work_is_a_failure(deployed):
    root, manifest_path, origin = deployed
    (root / "works/example.html").write_text("stale content")
    receipt = verifier.check_deployment(manifest_path, commit="b" * 40, attempts=1, origin=origin)
    assert not receipt["overall_ok"]
    failed = [row["path"] for row in receipt["results"] if not row["ok"]]
    assert failed == ["works/example.html"]


def test_missing_pdf_is_a_failure(deployed):
    root, manifest_path, origin = deployed
    (root / "papers/example/source.pdf").unlink()
    receipt = verifier.check_deployment(manifest_path, commit="b" * 40, attempts=1, origin=origin)
    assert not receipt["overall_ok"]
    assert any(row["method"] == "HEAD" and row["status"] == 404 for row in receipt["results"])


def test_stale_manifest_retry_receipt_counts_every_actual_request(deployed, monkeypatch):
    _, manifest_path, origin = deployed
    original = manifest_path.read_bytes()
    real_fetch = verifier.fetch
    request_count = 0

    def serve_stale(path, **kwargs):
        nonlocal request_count
        request_count += 1
        # Expected bytes have already been read; simulate a stale CDN using a
        # real HTTP response whose JSON differs only in insignificant whitespace.
        manifest_path.write_bytes(original + b"\n")
        return real_fetch(path, **kwargs)

    monkeypatch.setattr(verifier, "fetch", serve_stale)
    try:
        receipt = verifier.check_deployment(manifest_path, commit="b" * 40,
                                           attempts=3, interval=0, origin=origin)
        assert not receipt["overall_ok"]
        assert receipt["attempts"] == receipt["requests_attempted"] == request_count == 3
        assert receipt["checked"] == 1
        assert receipt["results"][0]["status"] == 200
        assert not receipt["results"][0]["hash_matches"]
    finally:
        manifest_path.write_bytes(original)


def test_missing_critical_assets_and_duplicate_paths_fail_closed():
    with pytest.raises(ValueError, match="missing critical"):
        verifier.acceptance_plan({"included_files": []})
    with pytest.raises(ValueError, match="duplicate"):
        verifier.acceptance_plan({"included_files": [{"path": "index.html"}, {"path": "index.html"}]})


@pytest.mark.parametrize("path", ["../private", "/private", "https://other.invalid/file", "a\\b", "a?token=x", "a#b", "a//b"])
def test_external_or_escaping_artifact_paths_rejected(path):
    with pytest.raises(ValueError):
        verifier.public_url(path)


def test_dirty_manifest_cannot_claim_committed_candidate(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    path = tmp_path / verifier.MANIFEST_PATH
    path.parent.mkdir(parents=True)
    path.write_text('{"source_commit_at_generation":"' + "a" * 40 + '"}')
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "-c", "core.fsmonitor=false", "commit", "-qm", "candidate"], cwd=tmp_path, check=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    verifier.require_committed_manifest(tmp_path, commit)
    path.write_text(path.read_text() + "\n")
    with pytest.raises(ValueError, match="bytes differ"):
        verifier.require_committed_manifest(tmp_path, commit)


def test_actual_slow_drip_body_has_total_request_deadline():
    class SlowBody(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Length", "20")
            self.end_headers()
            try:
                for _ in range(20):
                    self.wfile.write(b"x")
                    self.wfile.flush()
                    time.sleep(0.05)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), SlowBody)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        started = time.monotonic()
        result = verifier.fetch("slow.txt", origin=f"http://127.0.0.1:{server.server_port}/", timeout=0.2)
        assert not result["ok"]
        assert "timed out" in result["error"].lower()
        assert time.monotonic() - started < 2
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_whole_acceptance_deadline_stops_queued_requests_and_retries(deployed):
    _, manifest_path, _ = deployed
    manifest_bytes = manifest_path.read_bytes()
    requests = []

    class StalledSite(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_GET(self):
            requests.append(self.path.split("?", 1)[0])
            manifest_request = requests[-1] == "/" + verifier.MANIFEST_PATH
            body = manifest_bytes if manifest_request else b"x" * 100
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                if manifest_request:
                    self.wfile.write(body)
                else:
                    for byte in body:
                        self.wfile.write(bytes([byte]))
                        self.wfile.flush()
                        time.sleep(0.05)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), StalledSite)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        started = time.monotonic()
        receipt = verifier.check_deployment(
            manifest_path, commit="b" * 40, attempts=6, interval=60,
            timeout=20, workers=1, max_duration=0.25,
            origin=f"http://127.0.0.1:{server.server_port}/",
        )
        assert time.monotonic() - started < 2
        assert not receipt["overall_ok"]
        assert receipt["deadline_exhausted"]
        assert receipt["attempts"] == 1
        assert receipt["requests_attempted"] == len(requests) == 2
        assert any(not result["attempted"] and "deadline" in result["error"].lower()
                   for result in receipt["results"])
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
