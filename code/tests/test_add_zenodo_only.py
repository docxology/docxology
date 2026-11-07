"""Regression tests for the retired Zenodo-only publication command."""

from __future__ import annotations

import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401

from add_zenodo_only import main  # noqa: E402


@pytest.mark.parametrize(
    "argv",
    [[], ["23987671"], ["23987671:💻", "--no-regenerate"], ["--apply", "23987671"]],
)
def test_legacy_intake_refuses_before_network_or_writes(argv, monkeypatch, capsys):
    def unexpected_side_effect(*args, **kwargs):
        pytest.fail("Retired intake attempted network, file, or subprocess work")

    monkeypatch.setattr(urllib.request, "urlopen", unexpected_side_effect)
    monkeypatch.setattr(subprocess, "run", unexpected_side_effect)
    monkeypatch.setattr(Path, "mkdir", unexpected_side_effect)
    monkeypatch.setattr(Path, "write_bytes", unexpected_side_effect)
    monkeypatch.setattr(Path, "write_text", unexpected_side_effect)

    with pytest.raises(SystemExit) as stopped:
        main(argv)

    assert stopped.value.code == 2
    message = capsys.readouterr().err
    assert "writes have been retired" in message
    assert "check_zenodo_uncatalogued.py" in message
    assert "docs/operations/publication-sync.md#zenodo-only-publications" in message


def test_help_explains_the_reviewed_intake_route(capsys):
    with pytest.raises(SystemExit) as stopped:
        main(["--help"])

    assert stopped.value.code == 0
    message = capsys.readouterr().out
    assert "check_zenodo_uncatalogued.py" in message
    assert "docs/operations/publication-sync.md#zenodo-only-publications" in message
