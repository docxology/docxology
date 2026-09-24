"""Shared helpers for the generated artwork pages (single source of truth).

Consumed by ``build_artwork_pages.py`` (writer), ``build_sitemap.py`` (URL set),
``build_search_index.py`` (indexable set), and the artwork-page tests. Derived
artwork URLs are a permanent contract: ``artworks/<id>-<slug>.html`` keys on the
immutable Flickr photo id, so a re-titled artwork keeps its URL (slug renames
are not allowed to break links — the id prefix is the identity).
"""

from __future__ import annotations

import html
import re
import unicodedata

SITE_ORIGIN = "https://danielarifriedman.com/"
ARTWORKS_DIR = "artworks"
COLLECTIONS_DIR = "art-collections"
ARTWORK_PAGE_MARKER = "<!-- docxology:generated-artwork-page; ownership=artwork-pages-manifest -->"
ARTWORK_PAGES_MANIFEST_VERSION = "ArtworkPages.v1"
ARTWORKS_INDEX_PATH = f"{ARTWORKS_DIR}/index.html"

TITLE_MAX_LEN = 65
DESCRIPTION_MAX_LEN = 155
TITLE_SUFFIX = " — pen and ink drawing by Daniel Ari Friedman"

# A page is thin (generated but noindex,follow, excluded from the sitemap) when
# the artwork carries no Flickr tags AND its plain-text description is shorter
# than this many characters. DAF enriches such records on Flickr; the next
# sync + rebuild promotes them to indexable.
THIN_DESCRIPTION_CHARS = 40

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(title: str, *, max_len: int = 60) -> str:
    """ASCII, lowercase, hyphen-delimited filename slug ('' for untitled)."""
    text = unicodedata.normalize("NFKD", str(title or ""))
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    slug = _SLUG_STRIP.sub("-", text).strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("-")
    return slug


def page_filename(record: dict) -> str:
    slug = slugify(record.get("title", ""))
    return f"{record['id']}-{slug}.html" if slug else f"{record['id']}.html"


def page_rel_path(record: dict) -> str:
    """Repository-root-relative URL path of one artwork page."""
    return f"{ARTWORKS_DIR}/{page_filename(record)}"


def page_url(record: dict) -> str:
    return SITE_ORIGIN + page_rel_path(record)


def plain_text(markup: str) -> str:
    """Flickr HTML description -> single-line plain text (tags stripped)."""
    text = re.sub(r"<[^>]+>", " ", str(markup or ""))
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def is_thin(record: dict) -> bool:
    """No tags and a too-short plain description -> generated but noindex."""
    return not record.get("tags") and len(plain_text(record.get("desc", ""))) < THIN_DESCRIPTION_CHARS


def created_date(record: dict) -> str:
    """Creation date (YYYY-MM-DD): Flickr date-taken, falling back to upload."""
    for field in ("date", "date_upload"):
        value = str(record.get(field, "")).strip()
        if len(value) >= 10 and value[:4].isdigit():
            return value[:10]
    return ""


def og_image_url(record: dict) -> str:
    """Largest dependable social-card image: Large > Medium 800 > Medium 640 > thumb."""
    sizes = record.get("sizes") or {}
    for label in ("Large", "Medium 800", "Medium 640", "Medium"):
        if sizes.get(label):
            return sizes[label]
    return str(record.get("thumb", ""))


def image_alt_text(record: dict) -> str:
    """Meaningful, never-empty alt: title + medium + short plain description."""
    title = plain_text(record.get("title", "")) or "Untitled artwork"
    parts = [f"{title} — pen and ink drawing by Daniel Ari Friedman"]
    description = plain_text(record.get("desc", ""))
    if description:
        parts.append(description[:120].rstrip())
    return ". ".join(part for part in parts if part)


def page_title(record: dict) -> str:
    """Title + medium suffix clipped to the 65-char SERP budget on word boundaries."""
    title = " ".join(plain_text(record.get("title", "")).split()) or "Untitled artwork"
    if len(html.escape(title, quote=True)) + len(html.escape(TITLE_SUFFIX, quote=True)) <= TITLE_MAX_LEN:
        return f"{title}{TITLE_SUFFIX}"
    if len(html.escape(title, quote=True)) <= TITLE_MAX_LEN:
        return title
    cut = title
    while len(html.escape(cut + "…", quote=True)) > TITLE_MAX_LEN and len(cut) > 0:
        cut = cut.rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
        if " " not in cut and len(html.escape(cut + "…", quote=True)) > TITLE_MAX_LEN:
            cut = cut[:-1]
    return cut + "…"


def meta_description(record: dict) -> str:
    """Plain-text meta description, word-boundary clipped to the SERP budget.

    Empty or very short Flickr descriptions get a unique, title-bearing
    fallback so every page keeps a distinct SERP snippet.
    """
    description = plain_text(record.get("desc", ""))
    if len(description) < THIN_DESCRIPTION_CHARS:
        title = plain_text(record.get("title", "")) or "Untitled artwork"
        year = created_date(record)[:4]
        description = (
            f"{title} — pen and ink drawing by Daniel Ari Friedman{f' ({year})' if year else ''}. "
            "Ink on paper from the visual art archive at danielarifriedman.com/art.html."
        )
    if len(description) <= DESCRIPTION_MAX_LEN:
        return description
    cut = description[: DESCRIPTION_MAX_LEN - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
    if not cut:
        cut = description[: DESCRIPTION_MAX_LEN - 1].rstrip()
    return cut + "…"


def artwork_page_paths(payload: dict) -> list[str]:
    """Every generated artwork page path, in canonical (payload) order."""
    return [page_rel_path(record) for record in payload.get("artworks", [])]


def sitemap_paths(payload: dict) -> list[str]:
    """Artwork page paths promoted to the sitemap (thin noindex pages excluded)."""
    records = payload.get("artworks", [])
    return [
        page_rel_path(record)
        for record in records
        if not is_thin(record)
    ]
