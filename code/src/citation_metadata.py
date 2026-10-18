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

    # Use HTMLParser's existing raw-text tokenizer for head text elements.
    # Title is RCDATA in HTML; entity decoding cannot create active tags, and
    # we never collect title text. Treating its contents as raw text therefore
    # preserves the relevant boundary, including embedded script/comment text.
    CDATA_CONTENT_ELEMENTS = ("script", "style", "title", "noscript", "noframes")
    HEAD_ELEMENTS = frozenset({"html", "head", "base", "basefont", "bgsound",
                               "link", "meta", "title", "noscript", "noframes",
                               "style", "script", "template"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.head_finished = False
        self.template_depth = 0
        self.head_text_element: str | None = None
        self.tags: dict[str, list[str]] = {}

    @classmethod
    def parse(cls, text: str):
        """Parse a complete document, stopping after the real head boundary.

        Feed bounded chunks through HTMLParser's tokenizer rather than cutting
        at a textual </head>, which can occur inside comments or raw text.
        Normal incremental ``feed`` remains available to existing callers.
        """
        parser = cls()
        for offset in range(0, len(text), 1024):
            parser.feed(text[offset:offset + 1024])
            if parser.head_finished:
                break
        parser.close()
        return parser

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "template":
            self.template_depth += 1
            return
        if self.template_depth:
            return
        if tag == "body":
            self.in_head = False
            self.head_finished = True
        if tag == "head" and not self.head_finished:
            self.in_head = True
        if self.in_head and tag not in self.HEAD_ELEMENTS:
            self.in_head = False
            self.head_finished = True
        if self.in_head and tag in self.CDATA_CONTENT_ELEMENTS:
            self.head_text_element = tag
        if tag != "meta" or not self.in_head:
            return
        # HTML keeps the first value of a duplicated attribute. A later
        # lookalike must not replace the value a browser actually sees.
        attributes = {}
        for name, value in attrs:
            attributes.setdefault(name, value)
        name = (attributes.get("name") or "").lower()
        if name.startswith("citation_"):
            self.tags.setdefault(name, []).append(attributes.get("content") or "")

    def handle_data(self, data: str) -> None:
        # Non-whitespace outside head text/template content implicitly starts
        # the body in HTML. A later literal </head> must not reopen evidence.
        if (self.in_head and not self.template_depth and not self.head_text_element
                and data.strip(" \t\n\r\f")):
            self.in_head = False
            self.head_finished = True

    def handle_endtag(self, tag: str) -> None:
        if self.head_text_element:
            if tag == self.head_text_element:
                self.head_text_element = None
            return
        if tag == "template" and self.template_depth:
            self.template_depth -= 1
            return
        if self.template_depth:
            return
        if tag == "head":
            self.in_head = False
            self.head_finished = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # HTML ignores the slash on nonvoid elements. Rather than pretend
        # malformed template/script/style markup has closed, stop collecting
        # evidence; this lightweight parser does not perform HTML5 repair.
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.in_head = False
            self.head_finished = True
            return
        self.handle_starttag(tag, attrs)


class MetadataHead(CitationHead):
    """Read real crawler-facing head metadata using the citation boundaries.

    Keep duplicate elements visible for validators. Attribute order, quoting,
    case, and entity encoding do not change the extracted metadata.
    """

    def __init__(self) -> None:
        super().__init__()
        self.names: dict[str, list[str]] = {}
        self.properties: dict[str, list[str]] = {}
        self.canonicals: list[str] = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if not self.in_head or self.template_depth or self.head_text_element:
            return
        attributes = {}
        for key, value in attrs:
            attributes.setdefault(key, value)
        if tag == "meta":
            for attribute, target in (("name", self.names), ("property", self.properties)):
                key = (attributes.get(attribute) or "").casefold()
                if key:
                    target.setdefault(key, []).append(attributes.get("content") or "")
        elif tag == "link" and "canonical" in (attributes.get("rel") or "").casefold().split():
            self.canonicals.append(attributes.get("href") or "")
