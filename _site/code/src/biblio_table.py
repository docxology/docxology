"""
Shared iteration over the 8-column unified bibliography table in pages/BIBLIOGRAPHY.md.

Used by regenerate_docs (folder-linked rows) and sync_publications_html (all rows).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator, NamedTuple

DEFAULT_BIB_PATH = Path(__file__).resolve().parents[2] / "pages" / "BIBLIOGRAPHY.md"


class BiblioRow(NamedTuple):
    num: int
    year: str
    domain: str
    typ: str
    title: str
    venue: str
    link_cell: str
    docs_cell: str

    @property
    def folder(self) -> str | None:
        m = re.search(r"\.\./papers/(\d{4}_[^)/]+)/?", self.docs_cell)
        if not m:
            return None
        return m.group(1).rstrip("/")


def _strip_md_cell(s: str) -> str:
    return s.replace("*", "").strip()


def iter_bibliography_rows(bib_path: Path | None = None) -> Iterator[BiblioRow]:
    """Yield one BiblioRow per data row (numeric #); skips header and non-table lines."""
    path = bib_path or DEFAULT_BIB_PATH
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 8:
                continue
            try:
                num = int(cells[0])
            except ValueError:
                continue
            yield BiblioRow(
                num=num,
                year=cells[1],
                domain=cells[2],
                typ=cells[3],
                title=_strip_md_cell(cells[4]),
                venue=_strip_md_cell(cells[5]),
                link_cell=cells[6],
                docs_cell=cells[7],
            )
