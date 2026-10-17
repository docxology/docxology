from __future__ import annotations

import json
import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import refresh_public_source_inventory as inventory  # noqa: E402


def test_external_output_finishes_and_reports_source_warnings(tmp_path, monkeypatch, capsys):
    output = tmp_path / "inventory.json"
    payload = {"sections": [{"label": "restricted source", "ok": False}]}
    monkeypatch.setattr(inventory, "build_report", lambda **kwargs: payload)
    monkeypatch.setattr(sys, "argv", ["inventory", "--output", str(output)])

    inventory.main()

    assert json.loads(output.read_text()) == payload
    printed = capsys.readouterr().out
    assert f"wrote {output} with 1 sections" in printed
    assert "warnings: restricted source" in printed
