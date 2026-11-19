"""Canonical external-link normalization for bibliography-derived outputs."""

from __future__ import annotations

import re
from html import unescape
from html.entities import html5
from string import punctuation


_ESCAPED_PUNCTUATION = rf"\\([{re.escape(punctuation)}])"
_LABEL_TOKEN = re.compile(rf"{_ESCAPED_PUNCTUATION}|!?\[|\]")
_DESTINATION_TEXT = re.compile(
    rf"{_ESCAPED_PUNCTUATION}|&(?:[A-Za-z][A-Za-z0-9]*|#[0-9]{{1,7}}|#[xX][0-9A-Fa-f]{{1,6}});"
)
_DESTINATION_START = re.compile(r"\(\s*")
_LINK_END = re.compile(
    r"""(?:\s+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^()\\])*\)))?\s*\)"""
)


def _decode_destination_token(match: re.Match[str]) -> str:
    if match[1] is not None:
        return match[1]
    token = match[0]
    return unescape(token) if token.startswith("&#") else html5.get(token[1:], token)


def _destination_at(cell: str, label_end: int) -> tuple[str, int] | None:
    """Read one inline destination and validate its optional title and closer."""
    if not (opening := _DESTINATION_START.match(cell, label_end)):
        return None
    angle = cell.startswith("<", opening.end())
    start = end = opening.end() + angle
    depth = 0
    while end < len(cell):
        char = cell[end]
        if char == "\\" and end + 1 < len(cell) and cell[end + 1] in punctuation:
            end += 2
            continue
        if angle:
            if char == ">":
                break
            if char in "<\r\n":
                return None
        elif char == "(":
            depth += 1
        elif char == ")":
            if not depth:
                break
            depth -= 1
        elif char.isspace():
            break
        end += 1

    if depth or (angle and not cell.startswith(">", end)):
        return None
    if not (closing := _LINK_END.match(cell, end + angle)):
        return None
    return _DESTINATION_TEXT.sub(_decode_destination_token, cell[start:end]), closing.end()


def _explicit_link_url(cell: str) -> str:
    # Brackets close inside-out, but an enclosing link precedes links inside
    # its label (for example a linked image). Keep the earliest opening.
    openings: list[tuple[int, bool]] = []
    last_link = -1
    first = len(cell)
    url = ""
    cursor = 0
    while token := _LABEL_TOKEN.search(cell, cursor):
        cursor = token.end()
        if token[0] in ("[", "!["):
            openings.append((token.start(), token[0] == "!["))
        elif token[0] == "]" and openings:
            start, image = openings.pop()
            if image or start > last_link:
                if parsed := _destination_at(cell, cursor):
                    candidate, cursor = parsed
                    if not image:
                        # An inline link cannot be nested in another link label.
                        last_link = start
                    if start < first and candidate.startswith(("https://", "http://")):
                        first, url = start, candidate
            if url and not openings:
                break
    return url


def canonical_link_url(link_cell: str, venue: str) -> str:
    """Preserve explicit Markdown URLs; trim prose punctuation from bare links."""
    cell = (link_cell or "").strip()
    venue_u = venue.upper()

    if url := _explicit_link_url(cell):
        return url

    m = re.search(r"(https?://[^\s\])>]+)", cell)
    if m:
        return m.group(1).rstrip(").,;:!?")

    doi_m = re.search(r"(10\.\d{4,}/[^\s\])]*)", cell)
    if doi_m:
        slug = doi_m.group(1).rstrip(").,;:!?")
        return f"https://doi.org/{slug}"

    if re.search(r"^978[-\dXx]+$", cell) or cell.startswith("978-"):
        isbn = cell.split()[0]
        if "COGSEC" in venue_u or "COGSEC.ORG" in venue_u:
            return "https://cogsec.org"
        return f"https://www.worldcat.org/isbn/{isbn}"

    if cell in ("—", "-", ""):
        return ""

    if "UDEMY" in cell.upper() or "udemy.com" in cell.lower():
        um = re.search(r"(https?://www\.udemy\.com/[^\s)]+)", cell)
        if um:
            return um.group(1).rstrip(").,;:!?")

    return cell
