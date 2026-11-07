"""Regression tests for SEC-001: safe Zenodo PDF download targets."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401

from sync_paired_publications import _pdf_target  # noqa: E402


def _folder(tmp_path: Path) -> Path:
    folder = tmp_path / "2026_Example"
    folder.mkdir()
    return folder


def test_plain_pdf_key_resolves_inside_folder(tmp_path):
    folder = _folder(tmp_path)
    assert _pdf_target(folder, "paper.pdf") == folder.resolve() / "paper.pdf"


def test_traversal_key_neutralized_to_basename(tmp_path):
    folder = _folder(tmp_path)
    assert _pdf_target(folder, "../../../../tmp/outside.pdf") == (
        folder.resolve() / "outside.pdf"
    )


def test_absolute_key_sanitized_to_basename(tmp_path):
    folder = _folder(tmp_path)
    assert _pdf_target(folder, "/etc/passwd.pdf") == folder.resolve() / "passwd.pdf"


def test_non_pdf_or_empty_key_rejected(tmp_path):
    folder = _folder(tmp_path)
    for key in ("notes.txt", "dir/paper.txt", ""):
        assert _pdf_target(folder, key) is None


def test_paired_pdf_uses_exact_record_url_and_verified_bytes(monkeypatch):
    import hashlib
    import io
    from types import SimpleNamespace

    import sync_paired_publications as sync

    payload = b"%PDF-1.7\nretained fixture"
    opened = []

    class Response(io.BytesIO):
        status = 200

    def open_response(request, *, timeout):
        opened.append((request.full_url, timeout))
        return Response(payload)

    monkeypatch.setattr(
        sync.urllib.request, "build_opener", lambda *handlers: SimpleNamespace(open=open_response)
    )
    item = {
        "links": {"self": "https://attacker.invalid/other.pdf"},
        "size": len(payload),
        "checksum": "md5:" + hashlib.md5(payload, usedforsecurity=False).hexdigest(),
    }
    assert sync._read_zenodo_pdf("123", "work file.pdf", item) == payload
    assert opened == [("https://zenodo.org/api/records/123/files/work%20file.pdf/content", 15)]
    item["size"] -= 1
    with pytest.raises(ValueError, match="do not match"):
        sync._read_zenodo_pdf("123", "work file.pdf", item)
    item["size"] = sync.MAX_ZENODO_PDF_BYTES + 1
    with pytest.raises(ValueError, match="bounded size"):
        sync._read_zenodo_pdf("123", "work file.pdf", item)
    assert len(opened) == 2


def test_paired_pdf_exclusive_publish_preserves_incumbent(tmp_path):
    from sync_paired_publications import _publish_zenodo_pdf

    output = tmp_path / "paper.pdf"
    output.write_bytes(b"incumbent")
    with pytest.raises(FileExistsError):
        _publish_zenodo_pdf(output, b"candidate")
    assert output.read_bytes() == b"incumbent"
    assert list(tmp_path.iterdir()) == [output]
