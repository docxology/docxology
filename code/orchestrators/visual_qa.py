#!/usr/bin/env python3
"""Capture Playwright screenshots for key site pages.

Requires the optional ``browser-qa`` dependency plus its Chromium binary
(``uv sync --extra browser-qa && uv run playwright install chromium``). The
script starts a local static server, captures desktop and mobile screenshots,
and writes a manifest under reports/visual-qa/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
import stat
import subprocess
import time
import sys
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from generated_outputs import (
        read_generated_output_text,
        safe_generated_output_path,
        write_generated_output_text,
    )
    from report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state
except ImportError:  # pragma: no cover - package import path
    from .generated_outputs import (
        read_generated_output_text,
        safe_generated_output_path,
        write_generated_output_text,
    )
    from .report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state

OUT_DIR = dated_report_dir("visual-qa")
MANIFEST = OUT_DIR / "manifest.json"

PAGES = [
    ("home", "index.html"),
    ("publications", "publications.html"),
    ("works", "works/index.html"),
    ("domains", "domains.html"),
    ("search", "search.html?q=active%20inference"),
    ("repositories", "repositories.html"),
    ("repository-forks", "repositories-forks.html"),
    ("catalog", "catalog.html"),
    ("updates", "updates.html"),
    ("art", "art.html"),
    ("discovery", "discovery.html"),
    ("cite-verify", "cite-verify.html"),
    ("evidence", "evidence.html"),
]

VIEWPORTS = [
    ("desktop", "1440,1100"),
    ("mobile", "390,900"),
]


def sha256_file(path: Path) -> str:
    """Return the digest of a visual-review screenshot."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(url: str) -> None:
    for _ in range(60):
        try:
            with urlopen(url, timeout=1) as res:
                if res.status == 200:
                    return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Server did not become ready: {url}")


def capture() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        ["python3", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        wait_for_server(base + "/index.html")
        shots = []
        for page_name, rel in PAGES:
            for viewport_name, size in VIEWPORTS:
                out = safe_generated_output_path(
                    REPO_ROOT, OUT_DIR / f"{page_name}-{viewport_name}.png"
                )
                subprocess.run(
                    [
                        "playwright",
                        "screenshot",
                        "--browser=chromium",
                        f"--viewport-size={size}",
                        "--full-page",
                        f"{base}/{rel}",
                        str(out),
                    ],
                    cwd=REPO_ROOT,
                    check=True,
                )
                shots.append(
                    {
                        "page": rel,
                        "viewport": viewport_name,
                        "size": size,
                        "file": str(out.relative_to(REPO_ROOT)),
                        "sha256": sha256_file(out),
                    }
                )
        manifest = {
            "generated_at": generated_timestamp(),
            "source_commit": source_commit(),
            **source_worktree_state(),
            "tool": "playwright screenshot",
            "note": "Human review still required; these snapshots guard against obvious layout regressions.",
            "screenshots": shots,
            "review": {
                "status": "pending",
                "reviewed_by": None,
                "reviewed_at": None,
            },
        }
        write_generated_output_text(REPO_ROOT, MANIFEST, json.dumps(manifest, indent=2) + "\n")
        return manifest
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def _capture_errors(manifest: object, manifest_path: Path, repo_root: Path) -> list[str]:
    """Return integrity and coverage errors before a screenshot set is approved."""
    if not isinstance(manifest, dict):
        return ["visual QA manifest must be a JSON object"]
    screenshots = manifest.get("screenshots")
    if not isinstance(screenshots, list) or not screenshots:
        return ["visual QA manifest has no screenshots"]
    expected = {
        (page, viewport, size)
        for _name, page in PAGES
        for viewport, size in VIEWPORTS
    }
    observed: list[tuple[str, str, str]] = []
    errors: list[str] = []
    for index, screenshot in enumerate(screenshots, start=1):
        if not isinstance(screenshot, dict):
            errors.append(f"screenshot {index} is not an object")
            continue
        page = screenshot.get("page")
        viewport = screenshot.get("viewport")
        size = screenshot.get("size")
        if all(isinstance(value, str) and value for value in (page, viewport, size)):
            observed.append((page, viewport, size))
        else:
            errors.append(f"screenshot {index} lacks page/viewport/size coverage fields")
        file_name = screenshot.get("file")
        if not isinstance(file_name, str) or not file_name:
            errors.append(f"screenshot {index} lacks a file path")
            continue
        candidate = Path(file_name)
        if (
            candidate.is_absolute()
            or ".." in candidate.parts
            or "\\" in file_name
            or file_name.startswith("./")
            or candidate.suffix.lower() != ".png"
        ):
            errors.append(f"screenshot {index} has an invalid PNG path: {file_name!r}")
            continue
        path = repo_root / candidate
        try:
            path.relative_to(manifest_path.parent)
        except ValueError:
            errors.append(f"screenshot {index} is outside its manifest directory: {file_name}")
            continue
        try:
            relative = path.relative_to(repo_root)
            current = repo_root
            for component in relative.parts:
                current = current / component
                entry = current.lstat()
                if current.is_symlink():
                    raise OSError("symlinked screenshot path")
            if not stat.S_ISREG(entry.st_mode) or entry.st_nlink != 1:
                raise OSError("screenshot is not a singly linked regular file")
        except OSError as exc:
            errors.append(f"screenshot {index} is unsafe or missing: {file_name} ({exc})")
            continue
        digest = screenshot.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            errors.append(f"screenshot {index} lacks a valid SHA-256: {file_name}")
        elif sha256_file(path) != digest:
            errors.append(f"screenshot {index} digest mismatch: {file_name}")
    if set(observed) != expected or len(observed) != len(set(observed)):
        errors.append("visual QA screenshot coverage does not match the current page/viewport contract")
    return errors


def _load_manifest(manifest_path: Path, repo_root: Path = REPO_ROOT) -> dict:
    path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    try:
        text = read_generated_output_text(repo_root, path)
        if text is None:
            raise FileNotFoundError(path)
        payload = json.loads(text)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid visual QA manifest: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("Invalid visual QA manifest: expected a JSON object")
    return payload


def _latest_manifest() -> Path:
    try:
        return latest_subdir_file("visual-qa", "manifest.json")
    except FileNotFoundError as exc:
        raise SystemExit("Missing visual QA manifest") from exc


def check() -> None:
    manifest_path = _latest_manifest()
    manifest = _load_manifest(manifest_path, REPO_ROOT)
    errors = _capture_errors(manifest, manifest_path, REPO_ROOT)
    if errors:
        raise SystemExit("Invalid visual QA capture:\n" + "\n".join(f"  - {error}" for error in errors))
    print(f"checked {len(manifest['screenshots'])} visual QA screenshots")


def approve_existing(
    reviewed_by: str,
    *,
    manifest_path: Path | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict:
    """Record review of the exact pending capture after validating its files."""
    reviewer = reviewed_by.strip()
    if not reviewer:
        raise SystemExit("--reviewed-by must name the reviewer approving the existing capture")
    path = manifest_path or _latest_manifest()
    path = path if path.is_absolute() else repo_root / path
    manifest = _load_manifest(path, repo_root)
    errors = _capture_errors(manifest, path, repo_root)
    if errors:
        raise SystemExit("Cannot approve visual QA capture:\n" + "\n".join(f"  - {error}" for error in errors))
    review = manifest.get("review")
    if not isinstance(review, dict) or review.get("status") != "pending":
        raise SystemExit("Visual QA capture is not pending review; capture a new screenshot set before approval")
    manifest["review"] = {
        "status": "reviewed",
        "reviewed_by": reviewer,
        "reviewed_at": generated_timestamp(),
    }
    write_generated_output_text(repo_root, path, json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Verify the existing manifest and screenshot files")
    mode.add_argument(
        "--approve-existing",
        action="store_true",
        help="Record review for the current pending capture without recapturing it.",
    )
    parser.add_argument(
        "--reviewed-by",
        help="Name the reviewer approving --approve-existing; required by the post-deploy release gate.",
    )
    args = parser.parse_args(argv)
    if args.reviewed_by and not args.approve_existing:
        parser.error("--reviewed-by requires --approve-existing after the capture has been inspected")
    if args.approve_existing:
        if not args.reviewed_by:
            parser.error("--approve-existing requires --reviewed-by")
        manifest = approve_existing(args.reviewed_by)
        print(f"approved {len(manifest['screenshots'])} existing visual QA screenshots")
        return
    if args.check:
        check()
        return
    manifest = capture()
    print(f"wrote {len(manifest['screenshots'])} visual QA screenshots")


if __name__ == "__main__":
    main()
