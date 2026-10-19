"""Pinned corrected-source notices beside preserved historical publications."""

from __future__ import annotations

from datetime import date
from html import escape
import re


def revision_notice(metadata: dict) -> dict | None:
    item = metadata.get("source_revision_review")
    if item is None:
        return None
    if not isinstance(item, dict):
        raise ValueError("Invalid corrected-source review")
    repository = item.get("repository", "")
    commit = item.get("commit", "")
    document = item.get("document", "")
    summary = item.get("summary", "")
    reviewed_at = item.get("reviewed_at", "")
    if (
        not isinstance(repository, str)
        or not re.fullmatch(r"docxology/[A-Za-z0-9_-]+", repository)
        or not isinstance(commit, str)
        or not re.fullmatch(r"[0-9a-f]{40}", commit)
        or not isinstance(document, str)
        or not re.fullmatch(r"[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*\.md", document)
        or not isinstance(summary, str)
        or not summary.strip()
        or len(summary) > 1500
        or not isinstance(reviewed_at, str)
    ):
        raise ValueError(
            "Corrected-source reviews require a pinned public source and summary"
        )
    try:
        if date.fromisoformat(reviewed_at).isoformat() != reviewed_at:
            raise ValueError("Noncanonical review date")
    except ValueError as exc:
        raise ValueError("Invalid corrected-source review date") from exc
    return {**item, "url": f"https://github.com/{repository}/blob/{commit}/{document}"}


def revision_notice_html(metadata: dict) -> str:
    item = revision_notice(metadata)
    if item is None:
        return ""
    return (
        '<section class="section" aria-label="Corrected source review">'
        '<div class="work-detail"><h2>Corrected source review</h2>'
        f"<p>{escape(item['summary'])}</p>"
        "<p>The abstract, findings, extracted text and downloadable publication below "
        "describe the historical archive. Consult the corrected source before reusing "
        "its empirical claims. This review does not issue a new publication or DOI.</p>"
        f'<p><a href="{escape(item["url"], quote=True)}">Read the pinned source correction</a> '
        f"(reviewed {escape(item['reviewed_at'])}).</p></div></section>"
    )


def revision_notice_markdown(metadata: dict) -> str:
    item = revision_notice(metadata)
    if item is None:
        return ""
    return (
        "## Corrected source review\n\n" + escape(item["summary"]) + "\n\n"
        "The abstract, findings and downloadable publication describe the historical archive. "
        "Consult the corrected source before reusing its empirical claims. "
        "This review does not issue a new publication or DOI.\n\n"
        f"[Read the pinned source correction]({item['url']}) "
        f"(reviewed {item['reviewed_at']}).\n\n"
    )
