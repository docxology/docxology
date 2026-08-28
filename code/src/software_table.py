"""
Shared iteration over SOFTWARE.md repository tables.

Used by export_agent_data, sync_software_html, and tests.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Iterator, NamedTuple

DEFAULT_SOFTWARE_PATH = Path(__file__).resolve().parents[2] / "pages" / "SOFTWARE.md"

PAPER_LINK_RE = re.compile(r"\[📄\]\(([^)]+)\)")
DOI_INLINE_RE = re.compile(r"(10\.\d{4,}/[^\s\])]+)")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
DOI_RESOLVER_RE = re.compile(r"^https?://(?:dx\.)?doi\.org/(10\.\d{4,9}/[^\s)]+)$", re.I)
ZENODO_RECORD_URL_RE = re.compile(
    r"^https?://(?:www\.)?zenodo\.org/records/(\d+)(?:[/?#].*)?$", re.I
)
CANONICAL_DOI_LABEL_RE = re.compile(r"\b(?:canonical|citation)\b", re.I)
ARTIFACT_DOI_LABEL_RE = re.compile(r"\b(?:artifact|version|download)\b", re.I)


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


def _is_zenodo_url(url: str) -> bool:
    """Whether a catalog URL resolves to a Zenodo record or DOI."""
    normalized = url.rstrip(").,").casefold()
    return "zenodo.org/" in normalized or bool(
        re.match(r"^https?://(?:dx\.)?doi\.org/10\.5281/zenodo\.", normalized)
    )


def zenodo_url(description_raw: str) -> str:
    """Return a catalog's canonical Zenodo citation link when one is labelled.

    A software row can intentionally contain both a citation DOI and a
    version-specific artifact DOI.  The generic exported ``zenodo_url`` and
    JSON-LD ``sameAs`` field represent the citation identity, so an explicit
    ``Citation DOI`` / ``Canonical DOI`` label wins even when the artifact is
    listed first for download convenience.
    """
    links = [
        (label, url.rstrip(").,"))
        for label, url in MARKDOWN_LINK_RE.findall(description_raw)
        if _is_zenodo_url(url)
    ]
    if links:
        canonical = next(
            (url for label, url in links if CANONICAL_DOI_LABEL_RE.search(label)), ""
        )
        return canonical or links[0][1]
    m = DOI_INLINE_RE.search(description_raw)
    if m and "zenodo" in description_raw.lower():
        return f"https://doi.org/{m.group(1).rstrip(').,')}"
    return ""


def _doi_from_resolver_url(url: str) -> str:
    """Extract a bare DOI from a DOI resolver URL used in the source table."""
    match = DOI_RESOLVER_RE.fullmatch(url.rstrip(").,"))
    return match.group(1).rstrip(").,") if match else ""


def _doi_from_zenodo_link(url: str) -> str:
    """Resolve a DOI identity from either a DOI resolver or Zenodo record URL."""
    resolver_doi = _doi_from_resolver_url(url)
    if resolver_doi:
        return resolver_doi
    match = ZENODO_RECORD_URL_RE.fullmatch(url.rstrip(").,"))
    return f"10.5281/zenodo.{match.group(1)}" if match else ""


def _doi_role_label_errors_for_row(row: SoftwareRow, repo_root: Path) -> list[str]:
    """Require explicit labels when a linked paper has citation and artifact DOI roles."""
    paper = paper_path(row.description_raw)
    if not paper:
        return []
    metadata_path = repo_root / paper / "metadata.json"
    if not metadata_path.is_file():
        return [f"{row.name}: linked paper metadata is missing: {paper}metadata.json"]
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{row.name}: linked paper metadata is invalid: {exc}"]
    if not isinstance(metadata, dict):
        return [f"{row.name}: linked paper metadata must be a JSON object"]
    canonical = str(metadata.get("doi") or "").strip()
    artifact = str(metadata.get("artifact_doi") or "").strip()
    if not canonical or not artifact or canonical.casefold() == artifact.casefold():
        return []

    errors: list[str] = []
    zenodo_links = [
        (label, url, _doi_from_zenodo_link(url))
        for label, url in MARKDOWN_LINK_RE.findall(row.description_raw)
        if _is_zenodo_url(url)
    ]
    canonical_links = [
        (label, url)
        for label, url, doi in zenodo_links
        if doi.casefold() == canonical.casefold()
    ]
    for label, _url, doi in zenodo_links:
        if doi.casefold() == canonical.casefold() and not CANONICAL_DOI_LABEL_RE.search(label):
            errors.append(
                f"{row.name}: canonical DOI link {canonical} must be labelled citation or canonical"
            )
        if doi.casefold() == artifact.casefold() and not ARTIFACT_DOI_LABEL_RE.search(label):
            errors.append(
                f"{row.name}: artifact DOI link {artifact} must be labelled artifact, version, or download"
            )
    if zenodo_links and not canonical_links:
        errors.append(
            f"{row.name}: dual-role linked paper has Zenodo link(s) but omits canonical citation DOI {canonical}"
        )
    return errors


def doi_role_label_errors(
    rows: list[SoftwareRow], repo_root: Path | None = None
) -> list[str]:
    """Return source-table ambiguities between paper citation and artifact DOI links.

    A single Zenodo link is not inherently ambiguous. The guard applies only
    when its linked paper declares distinct canonical and artifact DOI roles.
    In that case every matching link needs a role-bearing label and any Zenodo
    link requires the canonical citation DOI to be present, so a version
    artifact can never become the generic exported identity.
    """
    root = repo_root or DEFAULT_SOFTWARE_PATH.parent.parent
    errors: list[str] = []
    for row in rows:
        errors.extend(_doi_role_label_errors_for_row(row, root))
    return errors


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
    # Escape all prose first and reconstruct only the small, explicitly
    # supported link grammar. This keeps future catalog descriptions from
    # injecting tags or event-handler attributes into generated cards.
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    chunks: list[str] = []
    cursor = 0
    for match in link_re.finditer(text):
        chunks.append(html.escape(text[cursor : match.start()]))
        label, href = match.group(1), match.group(2).strip()
        if label == "📄" and (href.startswith("../papers/") or href.startswith("papers/")):
            href = _rewrite_paper_href(href)
            label = "paper"
        elif not href.startswith("https://"):
            chunks.append(html.escape(label))
            cursor = match.end()
            continue
        chunks.append(
            f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
        )
        cursor = match.end()
    chunks.append(html.escape(text[cursor:]))
    return "".join(chunks)


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
