"""Bounded Crossref proposals; never adopt metadata or alter curated identity."""
from __future__ import annotations

import json
import hashlib
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from html.parser import HTMLParser

from docxology_tools.paper_artifacts import PaperResources, source_paths
from typing import Callable

API_ORIGIN = "https://api.crossref.org"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_REQUESTS = 100
TIMEOUT_SECONDS = 15
Fetch = Callable[[str], tuple[int, bytes]]


def plain_text(value: str) -> str:
    """Decode publisher entities, remove markup, and normalize whitespace."""
    class TextParser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []

        def handle_data(self, data):
            self.parts.append(data)

    parser = TextParser()
    parser.feed(value)
    parser.close()
    return " ".join(" ".join(parser.parts).split())


def normalized_title(value: str) -> str:
    # Equality is conservative across scripts: preserve Greek/non-Latin
    # identity while ignoring accents, punctuation and publisher markup.
    folded = unicodedata.normalize("NFKD", plain_text(value)).casefold()
    characters = (
        character if character.isalnum() or unicodedata.category(character).startswith("S") else " "
        for character in folded
        if not unicodedata.category(character).startswith("M")
    )
    return " ".join("".join(characters).split())


def normalized_doi(value: str) -> str:
    return value.strip().casefold()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_crossref(url: str) -> tuple[int, bytes]:
    """One request, fixed origin, no redirects/retries, capped response."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "api.crossref.org" or not parsed.path.startswith("/works/") or parsed.query or parsed.fragment:
        raise ValueError("only fixed-origin Crossref work URLs are permitted")
    request = urllib.request.Request(url, headers={
        "Accept": "application/json", "User-Agent": "docxology-citation-review/1.0",
    })
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        response = opener.open(request, timeout=TIMEOUT_SECONDS)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("Crossref response exceeds byte limit")
        return response.code, body


def _string(record: dict, name: str, *, required: bool = False) -> str:
    value = record.get(name, "")
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{name} must be {'a nonempty' if required else 'a'} string")
    return plain_text(value)


def _strings(record: dict, name: str, *, required: bool = False) -> list[str]:
    values = record.get(name, [])
    if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values) or (required and not values):
        raise ValueError(f"{name} must be a list of nonempty strings")
    return [plain_text(value) for value in values]


def candidate_metadata(message: dict, source_url: str, checked_at: str) -> dict:
    """Validate source shapes before producing a review candidate."""
    candidate = {
        "doi": normalized_doi(_string(message, "DOI", required=True)),
        "title": _strings(message, "title", required=True)[0],
        "source_url": source_url,
        "checked_at": checked_at,
        "resource_type": _string(message, "type", required=True),
    }
    journals = _strings(message, "container-title")
    if journals:
        candidate["journal_title"] = journals[0]
    for source, target in (("volume", "volume"), ("issue", "issue"), ("page", "pages")):
        value = _string(message, source)
        if value:
            candidate[target] = value
    issns = _strings(message, "ISSN")
    if issns:
        if any(not re.fullmatch(r"\d{4}-\d{3}[\dXx]", value) for value in issns):
            raise ValueError("ISSN must have canonical XXXX-XXXX form")
        candidate["issn"] = issns[0].upper()
    for field in ("published", "published-print", "published-online", "issued"):
        if field not in message:
            continue
        value = message[field]
        if not isinstance(value, dict):
            raise ValueError(f"{field} must be an object")
        parts = value.get("date-parts")
        if not isinstance(parts, list) or len(parts) != 1 or not isinstance(parts[0], list) or not 1 <= len(parts[0]) <= 3 or any(type(part) is not int for part in parts[0]):
            raise ValueError(f"{field} has invalid date-parts")
        components = parts[0]
        # Validate partial precision too, but never manufacture month/day.
        parsed = date(components[0], components[1] if len(components) >= 2 else 1, components[2] if len(components) == 3 else 1)
        if len(components) == 3 and "publication_date" not in candidate:
            candidate["publication_date"] = parsed.isoformat()
    return candidate


def review_works(works: list[dict], root: Path, *, citation_keys: list[str] | None = None, fetch: Fetch = fetch_crossref, checked_at: str | None = None) -> dict:
    """Return sequential, bounded proposals without changing any source file."""
    timestamp = checked_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    requested = set(citation_keys or [])
    known = {work.get("citation_key") for work in works}
    if requested - known:
        raise ValueError("unknown citation keys: " + ", ".join(sorted(requested - known)))
    selected = []
    visible = source_paths(root)
    for work in works:
        if requested and work.get("citation_key") not in requested:
            continue
        doi = work.get("doi", "")
        if not isinstance(doi, str):
            raise ValueError("curated DOI must be a string")
        doi = normalized_doi(doi)
        if not doi or doi.startswith("10.5281/") or not work.get("has_paper_folder"):
            if requested:
                raise ValueError(f"ineligible citation key: {work['citation_key']}")
            continue
        if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
            raise ValueError("invalid curated DOI")
        resources = PaperResources.load(root, work["docs_path"], visible)
        if resources.file("metadata.json") is None or resources.metadata is None:
            raise ValueError(f"eligible paper metadata is required: {work['docs_path']}")
        previous = resources.metadata.get("citation_metadata", {})
        if not isinstance(previous, dict):
            raise ValueError("citation_metadata must be an object")
        selected.append((work, doi, previous))
    if len(selected) > MAX_REQUESTS:
        raise ValueError(f"request limit {MAX_REQUESTS} exceeded; use citation-key filters")
    records = []
    for work, doi, previous in selected:
        url = f"{API_ORIGIN}/works/{urllib.parse.quote(doi, safe='')}"
        record = {"citation_key": work["citation_key"], "doi": doi, "title": work["title"], "source_url": url, "checked_at": timestamp, "previous_citation_metadata": previous, "status": "unavailable", "candidate_citation_metadata": None}
        try:
            status, body = fetch(url)
            if len(body) > MAX_RESPONSE_BYTES:
                raise ValueError("Crossref response exceeds byte limit")
            record["response_sha256"] = hashlib.sha256(body).hexdigest()
            if status != 200:
                record["error"] = f"Crossref HTTP {status}; no retry or adoption"
            else:
                envelope = json.loads(body)
                if not isinstance(envelope, dict) or not isinstance(envelope.get("message"), dict):
                    raise ValueError("Crossref message must be an object")
                candidate = candidate_metadata(envelope["message"], url, timestamp)
                if candidate["doi"] != doi or not normalized_title(work["title"]) or normalized_title(candidate["title"]) != normalized_title(work["title"]):
                    record.update(status="mismatch", error="DOI or normalized title does not match curated identity")
                elif {key: value for key, value in previous.items() if key not in {"checked_at", "source_url"}} == {key: value for key, value in candidate.items() if key not in {"checked_at", "source_url"}}:
                    record.update(status="unchanged", candidate_citation_metadata=previous)
                else:
                    record.update(status="proposed", candidate_citation_metadata=candidate)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            record["error"] = str(exc)
        records.append(record)
    return {"schema_version": 1, "mode": "review-proposals-only", "requires_review": True, "identity_policy": "Preserve curated title, authors, year and DOI; no automatic adoption", "checked_at": timestamp, "request_count": len(records), "limits": {"max_requests": MAX_REQUESTS, "timeout_seconds": TIMEOUT_SECONDS, "max_response_bytes": MAX_RESPONSE_BYTES, "retries": 0}, "records": records}
