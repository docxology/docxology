"""Tests for exact-capture visual QA approval."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import visual_qa as vq  # noqa: E402


def _pending_capture(root: Path) -> Path:
    report_dir = root / "reports" / "visual-qa" / "2026-08-26"
    report_dir.mkdir(parents=True)
    screenshots = []
    for index, (_name, page) in enumerate(vq.PAGES):
        for viewport, size in vq.VIEWPORTS:
            image = report_dir / f"shot-{index}-{viewport}.png"
            image.write_bytes(f"{page}|{viewport}|{size}".encode("utf-8"))
            screenshots.append(
                {
                    "page": page,
                    "viewport": viewport,
                    "size": size,
                    "file": image.relative_to(root).as_posix(),
                    "sha256": vq.sha256_file(image),
                }
            )
    manifest = {
        "generated_at": "2026-08-26T12:00:00Z",
        "source_commit": "a" * 40,
        "source_worktree_clean": True,
        "source_tree_sha": "b" * 40,
        "screenshots": screenshots,
        "review": {"status": "pending", "reviewed_by": None, "reviewed_at": None},
    }
    path = report_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def test_approve_existing_marks_the_exact_pending_capture_reviewed(tmp_path: Path):
    manifest_path = _pending_capture(tmp_path)
    before = json.loads(manifest_path.read_text(encoding="utf-8"))

    approved = vq.approve_existing(
        "Release reviewer",
        manifest_path=manifest_path,
        repo_root=tmp_path,
    )

    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert approved == after
    assert after["generated_at"] == before["generated_at"]
    assert after["screenshots"] == before["screenshots"]
    assert after["review"]["status"] == "reviewed"
    assert after["review"]["reviewed_by"] == "Release reviewer"
    assert isinstance(after["review"]["reviewed_at"], str)


def test_approve_existing_refuses_a_tampered_pending_screenshot(tmp_path: Path):
    manifest_path = _pending_capture(tmp_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    screenshot = tmp_path / payload["screenshots"][0]["file"]
    screenshot.write_bytes(b"changed after capture")

    with pytest.raises(SystemExit, match="digest mismatch"):
        vq.approve_existing("Release reviewer", manifest_path=manifest_path, repo_root=tmp_path)

    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert after["review"]["status"] == "pending"


def test_approve_existing_refuses_a_symlinked_manifest_target(tmp_path: Path):
    manifest_path = _pending_capture(tmp_path)
    outside = tmp_path / "outside-manifest.json"
    original = manifest_path.read_text(encoding="utf-8")
    outside.write_text(original, encoding="utf-8")
    alias = manifest_path.parent / "approval-alias.json"
    alias.symlink_to(outside)

    with pytest.raises(SystemExit, match="symlinked generated output"):
        vq.approve_existing("Release reviewer", manifest_path=alias, repo_root=tmp_path)

    assert outside.read_text(encoding="utf-8") == original


def test_reviewed_by_cannot_stamp_a_new_capture_without_inspection():
    with pytest.raises(SystemExit):
        vq.main(["--reviewed-by", "Release reviewer"])
