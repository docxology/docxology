from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import refresh_public_source_inventory as inventory  # noqa: E402


def test_external_output_finishes_and_reports_source_warnings(
    tmp_path, monkeypatch, capsys
):
    output = tmp_path / "inventory.json"
    payload = {"sections": [{"label": "restricted source", "ok": False}]}
    monkeypatch.setattr(inventory, "build_report", lambda **kwargs: payload)
    monkeypatch.setattr(sys, "argv", ["inventory", "--output", str(output)])

    inventory.main()

    assert json.loads(output.read_text()) == payload
    printed = capsys.readouterr().out
    assert f"wrote {output} with 1 sections" in printed
    assert "warnings: restricted source" in printed


class Response:
    def __init__(self, status, body):
        self.status, self.body = status, body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, bound):
        return self.body[:bound]


@pytest.mark.parametrize(
    "status,body",
    [
        (202, b"<title>Making sure you are not a bot</title>"),
        (202, b""),
        (200, b""),
        (200, b"<html><body>unavailable</body></html>"),
        (200, b"<title>   </title>"),
    ],
)
def test_incomplete_advisory_response_is_unavailable(monkeypatch, status, body):
    monkeypatch.setattr(
        inventory.urllib.request,
        "urlopen",
        lambda *args, **kwargs: Response(status, body),
    )
    result = inventory.public_page("https://example.org/author", "author advisory")
    assert result["ok"] is False
    assert result["items"] == []
    assert "error" in result


def test_complete_advisory_page_retains_observed_title(monkeypatch):
    monkeypatch.setattr(
        inventory.urllib.request,
        "urlopen",
        lambda *args, **kwargs: Response(
            200, b"<html><title>Author profile</title></html>"
        ),
    )
    assert inventory.public_page("https://example.org/author", "author advisory") == {
        "label": "author advisory",
        "url": "https://example.org/author",
        "ok": True,
        "items": [{"status": 200, "title": "Author profile"}],
    }
