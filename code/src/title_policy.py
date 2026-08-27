"""Shared title-length policy for generated page titles.

SERP titles are truncated by search engines around 60 characters; the site
policy targets <=60 rendered characters with a hard ceiling of 65. Clipping is
word-boundary aware and preserves meaningful leading tokens (series names,
episode markers are handled by the video page generator before this clip runs;
this module never reorders or drops interior tokens — it only trims the tail
on a word boundary and appends an ellipsis).
"""

from __future__ import annotations

SOFT_LIMIT = 60
HARD_LIMIT = 65

_TRAILING = " ,;:.–—-~\"'"


def clip_title(title: str, hard_limit: int = HARD_LIMIT) -> str:
    """Clip a page title to <= hard_limit rendered characters.

    Word-boundary aware; appends ``…`` when truncation occurs. Idempotent:
    clipping an already-clipped title returns it unchanged (the ellipsis is
    treated as part of the text and the result stays within the limit).
    """
    title = " ".join(str(title or "").split()).strip()
    if len(title) <= hard_limit:
        return title
    cut = title[: hard_limit - 1].rsplit(" ", 1)[0].rstrip(_TRAILING)
    if not cut:  # single very long token; hard cut as last resort
        cut = title[: hard_limit - 1].rstrip()
    return cut + "…"


def assert_title_within_limit(title: str, hard_limit: int = HARD_LIMIT) -> None:
    """Raise when a rendered title exceeds the hard ceiling (generator gate)."""
    rendered = " ".join(str(title or "").split()).strip()
    if len(rendered) > hard_limit:
        raise ValueError(
            f"page title {len(rendered)} chars exceeds hard limit {hard_limit}: {rendered!r}"
        )
