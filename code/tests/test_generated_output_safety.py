"""Regression tests for the release-chain generated-output safety boundary."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from generated_outputs import (  # noqa: E402
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
