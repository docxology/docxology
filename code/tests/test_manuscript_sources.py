"""A render binds conservative production dependencies without Git or private paths."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import manuscript_sources as sources  # noqa: E402
from docxology_tools.generated_outputs import read_generated_output_text  # noqa: E402


def fixture(root):
    for name in ("code/src/policy.py", "code/orchestrators/render.py"):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"# Public source\r\n")
    return root


def test_snapshot_is_stable_byte_exact_and_conservative(tmp_path):
    root = fixture(tmp_path)
    source = root / "code/src/policy.py"
    before = sources.production_source_snapshot(root)
    assert (
        before["files_sha256"]["code/src/policy.py"]
        == hashlib.sha256(source.read_bytes()).hexdigest()
    )
    assert before == sources.production_source_snapshot(root)
    assert str(root) not in json.dumps(before)
    (root / "code/src/unrelated.json").write_text("{}")
    assert before == sources.production_source_snapshot(root)
    source.write_bytes(b"# Other source!\r\n")
    assert before != sources.production_source_snapshot(root)
    (root / "code/src/added.py").write_text("# Newly declared dependency")
    assert (
        "code/src/added.py" in sources.production_source_snapshot(root)["files_sha256"]
    )


@pytest.mark.parametrize(
    "kind", ["symlink", "hardlink", "directory", "missing", "encoding"]
)
def test_source_snapshot_rejects_incomplete_or_unsafe_inputs(tmp_path, kind):
    root = fixture(tmp_path / "repo")
    source = root / "code/src/policy.py"
    if kind == "missing":
        source.unlink()
        source.parent.rmdir()
    elif kind == "directory":
        (source.parent / "hidden").symlink_to(
            root / "code/orchestrators", target_is_directory=True
        )
    elif kind == "encoding":
        source.write_bytes(b"\xff")
    else:
        original = tmp_path / "outside.py"
        source.rename(original)
        if kind == "symlink":
            source.symlink_to(original)
        else:
            os.link(original, source)
    with pytest.raises((ValueError, UnicodeError)):
        sources.production_source_snapshot(root)


@pytest.mark.parametrize(
    "bound",
    ["MAX_SOURCE_FILES", "MAX_SOURCE_BYTES", "MAX_TOTAL_BYTES", "MAX_SOURCE_ENTRIES"],
)
def test_source_snapshot_fails_closed_at_bounds(tmp_path, monkeypatch, bound):
    root = fixture(tmp_path)
    monkeypatch.setattr(sources, bound, 1)
    with pytest.raises(ValueError, match="bound"):
        sources.production_source_snapshot(root)


def test_safe_reader_byte_bound_preserves_newlines_and_utf8(tmp_path):
    source = tmp_path / "source.py"
    raw = "# café\r\n".encode()
    source.write_bytes(raw)
    assert (
        read_generated_output_text(
            tmp_path, source, newline="", max_bytes=len(raw)
        ).encode()
        == raw
    )
    assert (
        read_generated_output_text(tmp_path, source, max_bytes=len(raw)) == "# café\n"
    )
    with pytest.raises(ValueError, match="bound"):
        read_generated_output_text(tmp_path, source, max_bytes=len(raw) - 1)
    for invalid in (True, 0, -1, 1.5):
        with pytest.raises(ValueError):
            read_generated_output_text(tmp_path, source, max_bytes=invalid)


def test_source_inventory_permission_error_is_not_a_partial_snapshot(
    tmp_path, monkeypatch
):
    root = fixture(tmp_path)
    real_scandir = sources.os.scandir

    def unavailable(path):
        if str(path).endswith("blocked"):
            raise PermissionError("unavailable directory")
        return real_scandir(path)

    (root / "code/src/blocked").mkdir()
    monkeypatch.setattr(sources.os, "scandir", unavailable)
    with pytest.raises(ValueError, match="unavailable"):
        sources.production_source_snapshot(root)


class ControlledScan:
    def __init__(self, scan, transform):
        self.scan = scan
        self.transform = transform

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.scan.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.transform(next(self.scan))


def test_source_entry_bound_stops_before_exhausting_scanner(tmp_path, monkeypatch):
    root = fixture(tmp_path)
    for index in range(3):
        (root / f"code/src/extra{index}.py").write_text("# Additional source")
    real_scandir = sources.os.scandir
    seen = []

    def bounded_scan(path):
        def observe(entry):
            seen.append(entry.name)
            if len(seen) > 2:
                raise AssertionError("Scanner exhausted beyond declared bound")
            return entry

        return ControlledScan(real_scandir(path), observe)

    monkeypatch.setattr(sources, "MAX_SOURCE_ENTRIES", 1)
    monkeypatch.setattr(sources.os, "scandir", bounded_scan)
    with pytest.raises(ValueError, match="bound"):
        sources.production_source_snapshot(root)
    assert len(seen) == 2


def test_unavailable_entry_classification_cannot_silently_omit_a_directory(
    tmp_path, monkeypatch
):
    root = fixture(tmp_path)
    (root / "code/src/blocked").mkdir()
    real_scandir = sources.os.scandir

    class UnknownEntry:
        def __init__(self, entry):
            self.name = entry.name
            self.path = entry.path

        def is_dir(self, *args, **kwargs):
            raise PermissionError("Unknown entry kind")

        def stat(self, *args, **kwargs):
            raise PermissionError("Unknown entry kind")

    def scan(path):
        return ControlledScan(
            real_scandir(path),
            lambda entry: UnknownEntry(entry) if entry.name == "blocked" else entry,
        )

    monkeypatch.setattr(sources.os, "scandir", scan)
    with pytest.raises(ValueError, match="unavailable"):
        sources.production_source_snapshot(root)


def test_declared_recursive_scope_includes_python_under_bytecode_directory(tmp_path):
    root = fixture(tmp_path)
    cache = root / "code/src/__pycache__"
    cache.mkdir()
    source = cache / "policy.py"
    source.write_text("# Python source is included regardless of directory name")
    before = sources.production_source_snapshot(root)
    assert "code/src/__pycache__/policy.py" in before["files_sha256"]
    (cache / "policy.cpython.pyc").write_bytes(b"Not Python source")
    assert before == sources.production_source_snapshot(root)
    source.write_text("# Changed source")
    assert before != sources.production_source_snapshot(root)
