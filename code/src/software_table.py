"""
Shared iteration over SOFTWARE.md repository tables.

Used by export_agent_data, sync_software_html, and tests.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Iterator, NamedTuple

DEFAULT_SOFTWARE_PATH = Path(__file__).resolve().parents[2] / "pages" / "SOFTWARE.md"

PAPER_LINK_RE = re.compile(r"\[📄\]\(([^)]+)\)")
ZENODO_LINK_RE = re.compile(
    r"\[(?:Zenodo|DOI|zenodo)[^\]]*\]\((https?://(?:doi\.org/10\.\d+/[^\s)]+|zenodo\.org/[^\s)]+))\)",
    re.I,
)
DOI_INLINE_RE = re.compile(r"(10\.\d{4,}/[^\s\])]+)")


class SoftwareRow(NamedTuple):
    name: str
    url: str
    owner: str
    catalog_section: str
    description_raw: str
    language: str
    stars: int
    updated_or_year: str

    @property
    def is_docxology(self) -> bool:
        return self.catalog_section == "docxology"


def parse_link_cell(cell: str) -> tuple[str, str]:
    m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", cell)
    if not m:
        return strip_md(cell), ""
    return m.group(1), m.group(2)


def strip_md(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("📄", "").strip()
    return re.sub(r"\s*[·;,-]\s*$", "", value).strip()


def description_plain(description_raw: str) -> str:
    return strip_md(description_raw)


def paper_path(description_raw: str) -> str:
    m = PAPER_LINK_RE.search(description_raw)
    if not m:
        return ""
    path = m.group(1).strip()
    path = path.replace("../", "")
    return path if path.endswith("/") else f"{path}/"


def zenodo_url(description_raw: str) -> str:
    m = ZENODO_LINK_RE.search(description_raw)
    if m:
        return m.group(1).rstrip(").,")
    m = DOI_INLINE_RE.search(description_raw)
    if m and "zenodo" in description_raw.lower():
        return f"https://doi.org/{m.group(1).rstrip(').,')}"
    return ""


def _rewrite_paper_href(href: str) -> str:
    href = href.strip()
    if href.startswith("../papers/"):
        return href.replace("../", "", 1)
    if href.startswith("papers/"):
        return href
    return href


def description_html(description_raw: str) -> str:
    """Convert SOFTWARE.md description cell markdown to card-safe HTML."""
    text = description_raw.strip()

    def paper_sub(m: re.Match[str]) -> str:
        href = _rewrite_paper_href(m.group(1))
        return f'<a href="{html.escape(href, quote=True)}">paper</a>'

    text = PAPER_LINK_RE.sub(paper_sub, text)

    def md_link_sub(m: re.Match[str]) -> str:
        label, href = m.group(1), m.group(2)
        return (
            f'<a href="{html.escape(href, quote=True)}">'
            f"{html.escape(label)}</a>"
        )

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", md_link_sub, text)
    return text


def lang_css_class(language: str) -> str:
    if not language or language == "—":
        return "Unknown"
    mapping = {
        "Rich Text Format": "RichTextFormat",
        "Jupyter Notebook": "Jupyter",
    }
    if language in mapping:
        return mapping[language]
    return re.sub(r"[^A-Za-z0-9]+", "", language) or "Unknown"


def iter_software_rows(software_path: Path | None = None) -> Iterator[SoftwareRow]:
    path = software_path or DEFAULT_SOFTWARE_PATH
    section = ""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## 🧬"):
                section = "docxology"
            elif line.startswith("### 🏛️"):
                section = "active-inference-institute"
            if not section or not line.startswith("| ["):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 5:
                continue
            name, url = parse_link_cell(cells[0])
            try:
                stars = int(re.sub(r"[^0-9]", "", cells[3]) or "0")
            except ValueError:
                stars = 0
            owner = "docxology" if section == "docxology" else "ActiveInferenceInstitute"
            yield SoftwareRow(
                name=name,
                url=url,
                owner=owner,
                catalog_section=section,
                description_raw=cells[1],
                language=cells[2] if cells[2] != "—" else "",
                stars=stars,
                updated_or_year=cells[4],
            )


def software_rows_to_dict(row: SoftwareRow) -> dict:
    return {
        "name": row.name,
        "url": row.url,
        "owner": row.owner,
        "catalog_section": row.catalog_section,
        "description": description_plain(row.description_raw),
        "language": row.language,
        "stars": row.stars,
        "updated_or_year": row.updated_or_year,
        "paper_path": paper_path(row.description_raw),
        "zenodo_url": zenodo_url(row.description_raw),
    }
