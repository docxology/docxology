"""Render recorded abstract text without treating source HTML as active markup.

Metadata remains untouched. Block boundaries and safe anchor destinations are
retained in display text; each HTML/Markdown consumer still escapes its output.
"""
from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit


_BLOCKS = frozenset({
    "p", "div", "section", "article", "blockquote", "pre", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "tr",
})
_INLINE = frozenset({
    "a", "strong", "em", "b", "i", "u", "code", "span", "sup", "sub",
    "s", "del", "ins", "small", "mark", "abbr", "cite", "q", "kbd", "samp",
})
_HIDDEN = frozenset({"script", "style", "template", "iframe", "object"})
_TAGS = _BLOCKS | _INLINE | _HIDDEN | {"br", "hr", "td", "th", "html", "body"}
_HTML_TAG = re.compile(r"</?(?:" + "|".join(sorted(_TAGS)) + r")(?:\s[^<>]*|\s*/?)>", re.I)


def _safe_destination(value: str) -> str:
    """Keep readable web/mail/relative URLs, never executable schemes."""
    value = value.strip()
    if not value or re.search(r"[\x00-\x20\x7f]", value):
        return ""
    try:
        parsed = urlsplit(value)
    except ValueError:
        return ""
    if parsed.scheme.casefold() not in {"", "http", "https", "mailto"}:
        return ""
    if parsed.username or parsed.password:
        return ""
    return value


class _AbstractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.hidden: list[str] = []
        self.anchors: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _HIDDEN:
            self.hidden.append(tag)
        if self.hidden:
            return
        if tag in _BLOCKS or tag == "hr":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in {"td", "th"}:
            self.parts.append(" ")
        elif tag == "a":
            destination = next((value or "" for name, value in attrs if name == "href"), "")
            self.anchors.append((len(self.parts), _safe_destination(destination)))
        elif tag not in _TAGS:
            # Unknown tags may be literal technical notation such as <T>.
            # Keep it as text; the final renderer escapes all angle brackets.
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
            return
        if tag == "a" and self.anchors:
            self._finish_anchor()
        elif tag in _BLOCKS:
            self.parts.append("\n\n")
        elif tag in {"td", "th"}:
            self.parts.append(" ")
        elif tag not in _TAGS:
            self.parts.append("</" + tag + ">")

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            # Newlines in HTML source are layout whitespace. Only actual
            # block tags and <br> create the display's paragraph boundaries.
            self.parts.append(re.sub(r"\s+", " ", data))

    def _finish_anchor(self) -> None:
        start, destination = self.anchors.pop()
        label = "".join(self.parts[start:]).strip()
        if destination and destination != label:
            self.parts.append(" (" + destination + ")")

    def display_text(self) -> str:
        while self.anchors:
            self._finish_anchor()
        return "".join(self.parts)


def abstract_display_text(value: object) -> str:
    """Return complete inert display text, retaining paragraphs and URLs.

    Plain text, comparison signs, and literal encoded tags are preserved.
    Unsupported metadata containers/scalars are not invented into prose.
    """
    if not isinstance(value, str) or not value.strip():
        return ""
    if _HTML_TAG.search(value):
        parser = _AbstractParser()
        parser.feed(value)
        parser.close()
        text = parser.display_text()
    else:
        text = unescape(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()
