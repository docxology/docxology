"""Privacy and URL-safety checks for public source and generated manifests."""

from __future__ import annotations

import re
from pathlib import Path

LOCAL_PATH_RE = re.compile(
    r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:\\\\Users\\\\[A-Za-z0-9._-]+\\\\)"
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)
UNSAFE_URL_RE = re.compile(
    r"(?:"
    r"\b(?:href|src|action|formaction)\s*=\s*[\"']?\s*|"
    r"\burl\s*[\"']?\s*:\s*[\"']\s*|"
    r"\burl\(\s*[\"']?\s*"
    r")(?:javascript|vbscript|data):",
    re.IGNORECASE,
)

CV_PUBLIC_FILES = (
    "resume/source.json",
    "resume/README.md",
    "data/resume.json",
    "resume/full.txt",
    "resume/academic.txt",
    "resume/software-consulting.txt",
    "resume/teaching-service.txt",
    "resume/resume.html",
    "resume/verify.html",
)


def scan_public_files(repo_root: Path, paths: tuple[str, ...] = CV_PUBLIC_FILES) -> list[str]:
    """Return privacy and unsafe-URL violations in public CV surfaces."""
    errors: list[str] = []
    for relative in paths:
        path = repo_root / relative
        if not path.is_file():
            errors.append(f"missing public integrity input: {relative}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if LOCAL_PATH_RE.search(text):
            errors.append(f"{relative}: local filesystem path detected")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative}: secret-like token detected")
        if UNSAFE_URL_RE.search(text):
            errors.append(f"{relative}: unsafe URL scheme detected")
    return errors


def validate_public_files(repo_root: Path, paths: tuple[str, ...] = CV_PUBLIC_FILES) -> None:
    errors = scan_public_files(repo_root, paths)
    if errors:
        raise SystemExit("Public integrity violations:\n" + "\n".join(f"  - {error}" for error in errors))
