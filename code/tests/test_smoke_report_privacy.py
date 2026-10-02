"""Public smoke receipts retain diagnostics without private workspace paths."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401
import browser_smoke  # noqa: E402


def test_smoke_writer_redacts_workspace_before_bounding_diagnostics(tmp_path, monkeypatch):
    root = tmp_path / "private-person-records" / "checkout"
    out_dir = root / "reports" / "browser-smoke" / "fixture"
    monkeypatch.setattr(browser_smoke, "REPO_ROOT", root)
    monkeypatch.setattr(browser_smoke, "OUT_DIR", out_dir)
    monkeypatch.setattr(browser_smoke, "MANIFEST", out_dir / "manifest.json")
    monkeypatch.setattr(browser_smoke, "wait_for_server", lambda _url: None)
    monkeypatch.setattr(browser_smoke, "source_commit", lambda: "a" * 40)
    monkeypatch.setattr(browser_smoke, "source_worktree_state", lambda: {"source_worktree_clean": False})

    class Server:
        def terminate(self):
            pass

        def wait(self, timeout):
            return 0

    monkeypatch.setattr(browser_smoke.subprocess, "Popen", lambda *args, **kwargs: Server())

    def capture(args, **kwargs):
        assert kwargs["cwd"] == root
        image = Path(args[-1])
        image.write_bytes(b"disposable screenshot fixture")
        stdout = f"Waiting for selector {args[args.index('--wait-for-selector') + 1]}...\nCapturing screenshot into {image}"
        # Before redaction, truncating this leaves the tail of a private path.
        stderr = "x" * 900 + str(root) + "/" + "y" * 480
        return subprocess.CompletedProcess(args, 0, stdout, stderr)

    monkeypatch.setattr(browser_smoke.subprocess, "run", capture)
    report = browser_smoke.run_smoke()
    saved = json.loads((out_dir / "manifest.json").read_text())
    assert saved == report
    assert report["passing"] == report["count"] == len(browser_smoke.PAGES)
    for check in report["checks"]:
        assert str(root) not in check["stdout"]
        assert f"Waiting for selector {check['selector']}..." in check["stdout"]
        assert f"Capturing screenshot into {check['screenshot']}" in check["stdout"]
        assert check["stderr"] == "x" * 20 + "y" * 480
        assert check["screenshot_sha256"] == browser_smoke.sha256_file(root / check["screenshot"])
