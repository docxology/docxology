"""Regression tests for the release-chain generated-output safety boundary."""

from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools import generated_outputs  # noqa: E402
from docxology_tools.generated_outputs import (  # noqa: E402
    UnsafeGeneratedOutputPathError,
    read_generated_output_text,
    stale_output_paths,
    write_generated_output_text,
    write_output_texts,
)


def _assert_check_and_write_reject(
    root: Path,
    target: Path,
    outside: Path,
) -> None:
    """Prove both no-write drift reads and write mode reject one unsafe target."""
    expected = {target: "generated\n"}
    before = outside.read_text(encoding="utf-8")

    with pytest.raises(UnsafeGeneratedOutputPathError):
        stale_output_paths(expected, repo_root=root)
    assert outside.read_text(encoding="utf-8") == before

    with pytest.raises(UnsafeGeneratedOutputPathError):
        write_output_texts(expected, repo_root=root)
    assert outside.read_text(encoding="utf-8") == before


def test_final_symlink_target_is_rejected_before_check_or_write(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside must survive\n", encoding="utf-8")
    target = root / "publications.html"
    target.symlink_to(outside)

    _assert_check_and_write_reject(root, target, outside)


def test_ancestor_symlink_target_is_rejected_before_check_or_write(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside_dir = tmp_path / "outside"
    outside_dir.mkdir()
    outside = outside_dir / "software.html"
    outside.write_text("outside must survive\n", encoding="utf-8")
    (root / "data").symlink_to(outside_dir, target_is_directory=True)

    _assert_check_and_write_reject(root, root / "data" / "software.html", outside)


def test_symlinked_repository_root_is_rejected_before_check_or_write(tmp_path: Path) -> None:
    real_root = tmp_path / "real-repo"
    real_root.mkdir()
    root = tmp_path / "repo"
    root.symlink_to(real_root, target_is_directory=True)
    outside = tmp_path / "outside.txt"
    outside.write_text("outside must survive\n", encoding="utf-8")

    _assert_check_and_write_reject(root, root / "publications.html", outside)


def test_hard_link_target_is_rejected_before_check_or_write(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside must survive\n", encoding="utf-8")
    target = root / "catalog.html"
    os.link(outside, target)
    assert target.stat().st_nlink == 2

    _assert_check_and_write_reject(root, target, outside)


def test_hard_link_added_during_staged_write_fails_without_mutating_alias(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    target = root / "catalog.html"
    target.write_text("old generated content\n", encoding="utf-8")
    alias = tmp_path / "outside-alias.html"

    def add_hard_link_after_stage() -> None:
        os.link(target, alias)

    with pytest.raises(UnsafeGeneratedOutputPathError, match="hard-linked"):
        write_generated_output_text(
            root,
            target,
            "new generated content\n",
            _before_replace=add_hard_link_after_stage,
        )

    assert target.read_text(encoding="utf-8") == "old generated content\n"
    assert alias.read_text(encoding="utf-8") == "old generated content\n"


def test_atomic_replacement_preserves_alias_added_after_final_target_check(tmp_path: Path) -> None:
    """A link added in the final TOCTOU window keeps the old inode and bytes."""
    root = tmp_path / "repo"
    root.mkdir()
    target = root / "catalog.html"
    target.write_text("old generated content\n", encoding="utf-8")
    alias = tmp_path / "outside-alias.html"

    def add_hard_link_before_atomic_replace() -> None:
        os.link(target, alias)

    write_generated_output_text(
        root,
        target,
        "new generated content\n",
        _before_atomic_replace=add_hard_link_before_atomic_replace,
    )

    assert target.read_text(encoding="utf-8") == "new generated content\n"
    assert alias.read_text(encoding="utf-8") == "old generated content\n"
    assert target.stat().st_ino != alias.stat().st_ino
    assert target.stat().st_nlink == 1
    assert alias.stat().st_nlink == 1


def test_outside_root_target_is_rejected_before_check_or_write(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside must survive\n", encoding="utf-8")

    _assert_check_and_write_reject(root, outside, outside)


def test_safe_generated_output_round_trip_creates_real_parent_directories(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    target = root / "data" / "catalog.json"

    write_generated_output_text(root, target, '{"ok": true}\n')

    assert read_generated_output_text(root, target) == '{"ok": true}\n'
    assert stale_output_paths({target: '{"ok": true}\n'}, repo_root=root) == ()


def test_mapping_write_preflights_every_target_before_changing_any_file(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    safe_target = root / "safe.html"
    outside = tmp_path / "outside.html"
    outside.write_text("outside must survive\n", encoding="utf-8")
    unsafe_target = root / "unsafe.html"
    unsafe_target.symlink_to(outside)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        write_output_texts(
            {safe_target: "would be generated\n", unsafe_target: "unsafe\n"},
            repo_root=root,
        )

    assert not safe_target.exists()
    assert outside.read_text(encoding="utf-8") == "outside must survive\n"


@pytest.mark.parametrize("operation", [stale_output_paths, write_output_texts])
@pytest.mark.parametrize("alias", ["symlink", "hardlink", "ancestor", "outside"])
def test_mapping_preflights_every_target_before_any_stamp_read(tmp_path, monkeypatch, operation, alias):
    root = tmp_path / "repo"
    root.mkdir()
    safe_target = root / "safe.html"
    safe_target.write_text("unchanged safe bytes\n", encoding="utf-8")
    outside = tmp_path / "private" / "private.html"
    outside.parent.mkdir()
    outside.write_text("private bytes must not be read\n", encoding="utf-8")
    unsafe_target = root / "unsafe.html"
    if alias == "symlink":
        unsafe_target.symlink_to(outside)
    elif alias == "hardlink":
        os.link(outside, unsafe_target)
    elif alias == "ancestor":
        (root / "unsafe").symlink_to(outside.parent, target_is_directory=True)
        unsafe_target = root / "unsafe" / outside.name
    else:
        unsafe_target = outside
    reads = []

    def unexpected_read(*args, **kwargs):
        reads.append(args)
        pytest.fail("no stamp or observation read may precede complete-map validation")

    monkeypatch.setattr(generated_outputs, "read_generated_output_text", unexpected_read)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        operation({safe_target: "new safe bytes\n", unsafe_target: "unsafe\n"}, repo_root=root)

    assert reads == []
    assert safe_target.read_text(encoding="utf-8") == "unchanged safe bytes\n"
    assert outside.read_text(encoding="utf-8") == "private bytes must not be read\n"


@pytest.mark.parametrize("operation", [stale_output_paths, write_output_texts])
def test_late_unsafe_stamp_read_fails_before_any_mapping_write(tmp_path, monkeypatch, operation):
    root = tmp_path / "repo"
    root.mkdir()
    first, later = root / "first.html", root / "later.html"
    first.write_text("original first bytes\n", encoding="utf-8")
    later.write_text("original later bytes\n", encoding="utf-8")
    outside = tmp_path / "private.html"
    outside.write_text("private bytes must not be read\n", encoding="utf-8")
    original_read = generated_outputs.read_generated_output_text

    def swap_later_target_before_reuse(repo_root, target, **kwargs):
        if target == first:
            later.unlink()
            later.symlink_to(outside)
        return original_read(repo_root, target, **kwargs)

    monkeypatch.setattr(generated_outputs, "read_generated_output_text", swap_later_target_before_reuse)

    with pytest.raises(UnsafeGeneratedOutputPathError, match="symlinked"):
        operation({first: "new first bytes\n", later: "new later bytes\n"}, repo_root=root)

    assert first.read_text(encoding="utf-8") == "original first bytes\n"
    assert outside.read_text(encoding="utf-8") == "private bytes must not be read\n"


@pytest.mark.parametrize("operation", [stale_output_paths, write_output_texts])
@pytest.mark.parametrize("alias", ["symlink", "hardlink"])
def test_stamp_reuse_rejects_final_alias_race_before_reading_content(tmp_path, monkeypatch, operation, alias):
    root = tmp_path / "repo"
    root.mkdir()
    target = root / "output.html"
    target.write_text("original output\n", encoding="utf-8")
    outside = tmp_path / "private.html"
    outside.write_text("private bytes must not be read\n", encoding="utf-8")
    original_parent = generated_outputs._parent_directory_fd

    @contextmanager
    def swap_before_final_open(repo_root, output, *, create):
        with original_parent(repo_root, output, create=create) as pair:
            target.unlink()
            if alias == "symlink":
                target.symlink_to(outside)
            else:
                os.link(outside, target)
            yield pair

    def unexpected_content_open(*args, **kwargs):
        pytest.fail("unsafe alias must be rejected before opening a text reader")

    monkeypatch.setattr(generated_outputs, "_parent_directory_fd", swap_before_final_open)
    monkeypatch.setattr(generated_outputs.os, "fdopen", unexpected_content_open)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        operation({target: "would be generated\n"}, repo_root=root)

    assert outside.read_text(encoding="utf-8") == "private bytes must not be read\n"
