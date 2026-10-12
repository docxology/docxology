"""Source-backed citation fields without changing curated work identity."""

from __future__ import annotations

from datetime import date
from html.parser import HTMLParser


def _doi(record: dict) -> str:
    value = record.get("doi", "")
    if not isinstance(value, str):
        raise ValueError("citation DOI must be a string")
    return value.strip().casefold()


def _citation(metadata: dict) -> dict:
    citation = metadata.get("citation_metadata", {})
    if not isinstance(citation, dict):
        raise ValueError("citation_metadata must be an object")
    _doi(citation)
    return citation


def publication_date(work: dict, metadata: dict) -> str:
    """Use a valid source date only when it agrees with the cited year/DOI.

    Deposit dates and later editions must not silently replace the catalog's
    citation year. Crossref's reviewed citation date takes precedence over a
    local archive date; a conflicting citation date keeps year-only precision.
    """
    year = str(work["year"])
    citation = _citation(metadata)
    doi = _doi(work)
    metadata_doi = _doi(metadata)
    if doi and citation and _doi(citation) == doi:
        value = citation.get("publication_date")
    elif doi and metadata_doi == doi:
        value = metadata.get("publication_date")
    else:
        value = None
    if not isinstance(value, str) or len(value) != 10:
        return year
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return year
    return value if str(parsed.year) == year else year


def journal_fields(work: dict, metadata: dict) -> dict[str, str]:
    """Use reviewed journal records only; Zenodo is not a journal venue."""
    citation = _citation(metadata)
    if (
        _doi(citation) != _doi(work)
        or not _doi(work)
        or citation.get("resource_type") != "journal-article"
    ):
        return {}
    fields = {}
    for name in ("journal_title", "volume", "issue", "issn"):
        value = citation.get(name)
        if isinstance(value, str) and value.strip():
            fields[name] = value.strip()
    pages = citation.get("pages")
    if isinstance(pages, str) and pages.strip():
        first, separator, last = pages.strip().replace("–", "-").partition("-")
        fields["firstpage"] = first
        if separator and last:
            fields["lastpage"] = last
    return fields


class CitationHead(HTMLParser):
    """Read real head tags; comments and body lookalikes cannot fill gaps."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.tags: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "head":
            self.in_head = True
        if tag != "meta" or not self.in_head:
            return
        attributes = dict(attrs)
        name = (attributes.get("name") or "").lower()
        if name.startswith("citation_"):
            self.tags.setdefault(name, []).append(attributes.get("content") or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self.in_head = False
