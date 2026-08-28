"""Canonical external-link normalization for bibliography-derived outputs."""

from __future__ import annotations

import re


def canonical_link_url(link_cell: str, venue: str) -> str:
    """Return the canonical URL encoded by one bibliography link cell."""
    cell = (link_cell or "").strip()
    venue_u = venue.upper()

    m = re.search(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", cell)
    if m:
        return m.group(2).rstrip(").,")

    m = re.search(r"(https?://[^\s\])>]+)", cell)
    if m:
        return m.group(1).rstrip(").,")

    doi_m = re.search(r"(10\.\d{4,}[^\s\])]*)", cell)
    if doi_m:
        slug = doi_m.group(1).rstrip(").,")
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
            return um.group(1).rstrip(").,")

    return cell
