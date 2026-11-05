"""Privacy and URL-safety checks for public source and generated manifests."""

from __future__ import annotations

import re
from pathlib import Path

# This exported regex identifies candidates; public prose checks use the
# URL-aware helpers below so complete HTTP(S) URLs remain unchanged.
LOCAL_PATH_RE = re.compile(
    r"""(?<![\w/])(?:/+(?:Users|home|Volumes)/|[A-Za-z]:[\\/]+Users[\\/]+|~/)[^\s`"'<>()[\]{}]+"""
)
_HTTP_URL_RE = re.compile(
    r"""(https?://[^\s`"'<>\\]+)""", re.IGNORECASE
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
INSECURE_HTTP_URL_RE = re.compile(r"http(?!s):", re.IGNORECASE)

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


def _http_url_end(text: str, start: int, end: int) -> int:
    """Find a surrounding prose delimiter without trimming balanced URL text."""
    previous = start - 1
    while previous >= 0 and text[previous].isspace():
        previous -= 1
    opening = text[previous] if previous >= 0 else ""
    closing = {"(": ")", "[": "]"}.get(opening)
    if closing is None:
        return end
    depth = 0
    for index in range(start, end):
        character = text[index]
        if character == opening:
            depth += 1
        elif character == closing:
            if depth == 0:
                return index
            depth -= 1
    return end


def redact_local_paths(text: str) -> str:
    """Remove local filesystem paths while preserving public HTTP(S) URLs."""
    parts: list[str] = []
    cursor = 0
    while match := _HTTP_URL_RE.search(text, cursor):
        end = _http_url_end(text, match.start(), match.end())
        parts.append(LOCAL_PATH_RE.sub("[local path redacted]", text[cursor:match.start()]))
        parts.append(text[match.start():end])
        cursor = end
    parts.append(LOCAL_PATH_RE.sub("[local path redacted]", text[cursor:]))
    return "".join(parts)


def contains_local_paths(text: str) -> bool:
    """Detect local paths using the same URL boundary as public redaction."""
    return redact_local_paths(text) != text


def scan_public_files(
    repo_root: Path, paths: tuple[str, ...] = CV_PUBLIC_FILES
) -> list[str]:
    """Return privacy and unsafe-URL violations in public CV surfaces."""
    errors: list[str] = []
    for relative in paths:
        path = repo_root / relative
        if not path.is_file():
            errors.append(f"missing public integrity input: {relative}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if contains_local_paths(text):
            errors.append(f"{relative}: local filesystem path detected")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{relative}: secret-like token detected")
        if UNSAFE_URL_RE.search(text):
            errors.append(f"{relative}: unsafe URL scheme detected")
        if INSECURE_HTTP_URL_RE.search(text):
            errors.append(f"{relative}: insecure http:// URL detected (use https)")
    return errors


def validate_public_files(
    repo_root: Path, paths: tuple[str, ...] = CV_PUBLIC_FILES
) -> None:
    errors = scan_public_files(repo_root, paths)
    if errors:
        raise SystemExit(
            "Public integrity violations:\n"
            + "\n".join(f"  - {error}" for error in errors)
        )
