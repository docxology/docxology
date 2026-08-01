"""Regression tests for SEC-001: path-traversal-safe Zenodo PDF download targets.

Both add_zenodo_only.py and sync_paired_publications.py join a Zenodo file key
onto the paper folder when downloading a PDF. A hostile or compromised record
could set ``key`` to ``../../outside.pdf`` or an absolute path; the downloader
must neutralize it to a plain basename that stays inside the folder.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH))

from add_zenodo_only import _pdf_target as add_target  # noqa: E402
from sync_paired_publications import _pdf_target as sync_target  # noqa: E402

TARGETS = (add_target, sync_target)


def _folder(tmp_path: Path) -> Path:
    folder = tmp_path / "2026_Example"
    folder.mkdir()
    return folder


def test_plain_pdf_key_resolves_inside_folder(tmp_path):
    folder = _folder(tmp_path)
    for target in TARGETS:
        t = target(folder, "paper.pdf")
        assert t is not None
        assert t.parent == folder.resolve()
        assert t.name == "paper.pdf"


def test_traversal_key_neutralized_to_basename(tmp_path):
    folder = _folder(tmp_path)
    for target in TARGETS:
        t = target(folder, "../../../../tmp/outside.pdf")
        assert t is not None
        assert t.parent == folder.resolve()  # does NOT escape the folder
        assert t.name == "outside.pdf"


def test_absolute_key_sanitized_to_basename(tmp_path):
    folder = _folder(tmp_path)
    for target in TARGETS:
        t = target(folder, "/etc/passwd.pdf")
        assert t is not None
        assert t.parent == folder.resolve()
        assert t.name == "passwd.pdf"


def test_non_pdf_or_empty_key_rejected(tmp_path):
    folder = _folder(tmp_path)
    for target in TARGETS:
        assert target(folder, "notes.txt") is None
        assert target(folder, "dir/paper.txt") is None
        assert target(folder, "") is None
