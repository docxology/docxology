"""Pair public GitHub releases with Zenodo records.

The module is intentionally API-shape oriented: callers can feed normalized
responses from the GitHub Releases API and Zenodo Records API without relying
on local release receipts.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any, Iterable, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parent))
from domain_inference import contains_term, infer_domain_emoji_for_pair as infer_domain  # noqa: E402, F401
from report_paths import generated_timestamp  # noqa: E402

ORCID = "0000-0001-6232-9096"

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
GITHUB_RELEASE_RE = re.compile(
    r"https://github\.com/([^/\s)]+)/([^/\s)]+)/releases/tag/([^\s)]+)",
    re.I,
)
ZENODO_RECORD_RE = re.compile(r"https://zenodo\.org/records/(\d+)", re.I)
PDF_SHA_RE = re.compile(r"(?:PDF\s+SHA-?256|sha256)\s*[:=]\s*`?([a-f0-9]{16,64})`?", re.I)

_DOI_TRAILING = ".,;:)]}`'\""
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
    "from",
    "through",
}


@dataclass(frozen=True)
class GitHubAsset:
    """Release asset normalized from the GitHub API."""

    name: str
    download_url: str
    size: int | None = None

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "GitHubAsset":
        return cls(
            name=str(payload.get("name") or ""),
            download_url=str(payload.get("browser_download_url") or ""),
            size=payload.get("size") if isinstance(payload.get("size"), int) else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GitHubRelease:
    """GitHub release candidate for publication pairing."""

    owner: str
    repo: str
    tag: str
    name: str
    body: str
    html_url: str
    published_at: str
    assets: list[GitHubAsset | dict[str, Any]]

    @classmethod
    def from_api(cls, owner: str, repo: str, payload: dict[str, Any]) -> "GitHubRelease":
        assets = [GitHubAsset.from_api(item) for item in payload.get("assets", []) if isinstance(item, dict)]
        return cls(
            owner=owner,
            repo=repo,
            tag=str(payload.get("tag_name") or ""),
            name=str(payload.get("name") or ""),
            body=str(payload.get("body") or ""),
            html_url=str(payload.get("html_url") or ""),
            published_at=str(payload.get("published_at") or payload.get("created_at") or ""),
            assets=assets,
        )

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repo}"

    @property
    def text(self) -> str:
        asset_names = " ".join(asset_name(asset) for asset in self.assets)
        return " ".join([self.name, self.body, self.html_url, self.tag, asset_names]).strip()

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["assets"] = [asset_to_dict(asset) for asset in self.assets]
        payload["full_name"] = self.full_name
        return payload


@dataclass(frozen=True)
class ZenodoRecord:
    """Zenodo record candidate for publication pairing."""

    record_id: str
    doi: str
    title: str
    publication_date: str
    version: str | None
    resource_type: dict[str, Any]
    creators: list[dict[str, Any]]
    description: str
    keywords: list[str]
    related_identifiers: list[dict[str, Any]]
    files: list[dict[str, Any]]
    html_url: str

    @classmethod
    def from_api(cls, payload: dict[str, Any]) -> "ZenodoRecord":
        meta = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        links = payload.get("links") if isinstance(payload.get("links"), dict) else {}
        record_id = str(payload.get("id") or payload.get("record_id") or "")
        return cls(
            record_id=record_id,
            doi=str(payload.get("conceptdoi") or meta.get("conceptdoi") or payload.get("doi") or meta.get("doi") or ""),
            title=str(meta.get("title") or ""),
            publication_date=str(meta.get("publication_date") or ""),
            version=str(meta.get("version")) if meta.get("version") is not None else None,
            resource_type=meta.get("resource_type") if isinstance(meta.get("resource_type"), dict) else {},
            creators=meta.get("creators") if isinstance(meta.get("creators"), list) else [],
            description=str(meta.get("description") or ""),
            keywords=[str(item) for item in (meta.get("keywords") or [])],
            related_identifiers=(
                meta.get("related_identifiers") if isinstance(meta.get("related_identifiers"), list) else []
            ),
            files=payload.get("files") if isinstance(payload.get("files"), list) else [],
            html_url=str(links.get("html") or (f"https://zenodo.org/records/{record_id}" if record_id else "")),
        )

    @property
    def doi_url(self) -> str:
        return f"https://doi.org/{self.doi}" if self.doi else ""

    @property
    def record_url(self) -> str:
        # doi is the Zenodo *concept* DOI (see from_api); derive the record URL from it so the
        # record link always agrees with the canonical DOI shown alongside it. record_id is the
        # version-specific Zenodo record id, which can differ from the concept id and would make
        # the same document cite two different Zenodo URLs for one work.
        derived = zenodo_record_url_from_doi(self.doi)
        if derived:
            return derived
        if self.record_id:
            return f"https://zenodo.org/records/{self.record_id}"
        return ""

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["doi_url"] = self.doi_url
        payload["record_url"] = self.record_url
        return payload


@dataclass(frozen=True)
class PublicationPair:
    """A GitHub release and Zenodo record pairing candidate."""

    release: GitHubRelease
    record: ZenodoRecord
    confidence: str
    evidence: tuple[str, ...]

    @property
    def doi(self) -> str:
        return self.record.doi

    @property
    def github_repo(self) -> str:
        return self.release.full_name

    @property
    def github_release_url(self) -> str:
        return self.release.html_url

    @property
    def zenodo_record_url(self) -> str:
        return self.record.record_url

    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "doi": self.doi,
            "github_repo": self.github_repo,
            "github_release_url": self.github_release_url,
            "zenodo_record_url": self.zenodo_record_url,
            "release": self.release.to_dict(),
            "record": self.record.to_dict(),
        }


@dataclass(frozen=True)
class SyncAction:
    """Action that the sync CLI should take for a pair."""

    action_type: str
    doi: str
    title: str
    confidence: str
    reason: str
    github_repo: str
    github_release_url: str
    zenodo_record_url: str
    release_tag: str
    folder: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def asset_name(asset: GitHubAsset | dict[str, Any]) -> str:
    if isinstance(asset, GitHubAsset):
        return asset.name
    return str(asset.get("name") or "")


def asset_to_dict(asset: GitHubAsset | dict[str, Any]) -> dict[str, Any]:
    if isinstance(asset, GitHubAsset):
        return asset.to_dict()
    return dict(asset)


def clean_markdown_text(value: Any) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_abstract_text(value: Any) -> str:
    text = clean_markdown_text(value)
    return re.split(r"\s---\s+Associated artifacts\b", text, maxsplit=1)[0].strip()


def _normalize_doi(value: str) -> str:
    return value.strip().rstrip(_DOI_TRAILING)


def extract_dois(text: str) -> list[str]:
    """Extract unique DOI strings, preserving first-seen order."""
    seen: set[str] = set()
    out: list[str] = []
    for raw in DOI_RE.findall(text or ""):
        doi = _normalize_doi(raw)
        key = doi.lower()
        if key not in seen:
            seen.add(key)
            out.append(doi)
    return out


def extract_github_release_urls(text: str) -> list[str]:
    seen: set[str] = set()
    urls: list[str] = []
    for match in GITHUB_RELEASE_RE.finditer(text or ""):
        url = match.group(0).rstrip(_DOI_TRAILING)
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def extract_pdf_sha256(text: str) -> str:
    match = PDF_SHA_RE.search(text or "")
    return match.group(1).lower() if match else ""


def yaml_double_quoted(value: str) -> str:
    """Escape a string for safe embedding inside a YAML double-quoted scalar
    (e.g. CITATION.cff `title: "..."`). Titles containing a literal `"` (common
    in transcript/commentary titles that quote another work) would otherwise
    terminate the scalar early and break YAML parsing."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def zenodo_record_url_from_doi(doi: str) -> str:
    match = re.fullmatch(r"10\.5281/zenodo\.(\d+)", doi.strip())
    if match:
        return f"https://zenodo.org/records/{match.group(1)}"
    return f"https://doi.org/{doi}" if doi else ""


# A durable pairing decision is valid only for the complete public candidate
# that was reviewed.  DOI + GitHub release URL alone is too weak: a later
# Zenodo record, changed title, repository correction, or retag can otherwise
# inherit an unrelated decision.  Keep this representation in the shared
# pairing module so the writer and the review renderer make the same decision.
PairCandidateFingerprint = tuple[str, str, str, str, str, str]
_PAIR_DECISION_VALUES = {
    "accept",
    "accepted",
    "acknowledged",
    "applied",
    "reject",
    "rejected",
    "supersede",
    "superseded",
}


def _candidate_text(value: object, *, casefold: bool = False) -> str:
    """Return a stable scalar for a candidate identity field.

    Whitespace and DOI/repository/title case are presentation details, while
    URLs and tags retain their meaningful spelling.  Non-string values are not
    silently coerced into an identity field.
    """
    if not isinstance(value, str):
        return ""
    normalized = re.sub(r"\s+", " ", value).strip()
    return normalized.casefold() if casefold else normalized


def _candidate_url(value: object) -> str:
    """Normalize the harmless trailing slash variance in a candidate URL."""
    return _candidate_text(value).rstrip("/")


def _first_nonempty_string(*values: object) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value
    return ""


def canonical_pair_candidate_fingerprint(
    *,
    doi: object,
    github_release_url: object,
    zenodo_record_url: object,
    github_repo: object,
    title: object,
    release_tag: object,
) -> PairCandidateFingerprint | None:
    """Return the full canonical identity of one reviewed pairing candidate.

    Every component is required.  Callers must defer a candidate when a legacy
    decision cannot supply the full identity from its own fields or its group
    context, rather than falling back to a lossy DOI/release key.
    """
    fingerprint: PairCandidateFingerprint = (
        _candidate_text(doi, casefold=True),
        _candidate_url(github_release_url),
        _candidate_url(zenodo_record_url),
        _candidate_text(github_repo, casefold=True),
        _candidate_text(title, casefold=True),
        _candidate_text(release_tag),
    )
    return fingerprint if all(fingerprint) else None


def release_identity_from_url(github_release_url: object) -> tuple[str, str]:
    """Derive a repository and tag from a canonical GitHub release URL."""
    release_url = _candidate_url(github_release_url)
    match = GITHUB_RELEASE_RE.fullmatch(release_url)
    if not match:
        return "", ""
    return f"{match.group(1)}/{match.group(2)}", match.group(3)


def decision_pair_candidate_fingerprint(
    raw_candidate: object, group: Mapping[str, Any]
) -> PairCandidateFingerprint | None:
    """Resolve a decision-log candidate to the full reviewed identity.

    Older decision logs occasionally stored a bare release URL.  They remain
    usable only when the DOI, title, repository, tag, and canonical Zenodo URL
    can all be derived from the surrounding decision group; otherwise the
    decision is intentionally inert and the live candidate is re-queued.
    """
    if isinstance(raw_candidate, str):
        candidate: Mapping[str, Any] = {"github_release_url": raw_candidate}
    elif isinstance(raw_candidate, Mapping):
        candidate = raw_candidate
    else:
        return None

    doi = _first_nonempty_string(candidate.get("doi"), group.get("doi"))
    release_url = _first_nonempty_string(
        candidate.get("github_release_url"), group.get("github_release_url")
    )
    derived_repo, derived_tag = release_identity_from_url(release_url)
    zenodo_record_url = _first_nonempty_string(
        candidate.get("zenodo_record_url"),
        group.get("zenodo_record_url"),
        zenodo_record_url_from_doi(doi),
    )
    github_repo = _first_nonempty_string(
        candidate.get("github_repo"),
        group.get("candidate_github_repo"),
        group.get("github_repo"),
        derived_repo,
    )
    title = _first_nonempty_string(
        candidate.get("record_title"), candidate.get("title"), group.get("title")
    )
    release_tag = _first_nonempty_string(
        candidate.get("release_tag"), group.get("release_tag"), derived_tag
    )
    return canonical_pair_candidate_fingerprint(
        doi=doi,
        github_release_url=release_url,
        zenodo_record_url=zenodo_record_url,
        github_repo=github_repo,
        title=title,
        release_tag=release_tag,
    )


def _zoned_timestamp(value: object) -> datetime | None:
    """Parse a decision timestamp only when it carries an explicit timezone."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _decision_note(payload: Mapping[str, Any], group: Mapping[str, Any]) -> str:
    """Return a group rationale or the audited global decision note."""
    rationale = group.get("rationale")
    if isinstance(rationale, str) and rationale.strip():
        return rationale.strip()
    summary = payload.get("decision_summary")
    if isinstance(summary, Mapping):
        note = summary.get("note")
        if isinstance(note, str) and note.strip():
            return note.strip()
    return ""


def _authenticated_supersession(
    group: Mapping[str, Any],
    *,
    previous: Mapping[str, str],
    fingerprint: PairCandidateFingerprint,
) -> bool:
    """Return whether a conflicting decision explicitly supersedes another.

    A plain later row is not authority to overwrite a decision for the same
    public candidate.  The successor must name the prior group and exact
    candidate, retain an authenticated approval receipt, and be temporally
    later than the decision it replaces.
    """
    supersession = group.get("supersession")
    if not isinstance(supersession, Mapping):
        return False
    if supersession.get("supersedes_group_id") != previous.get("group_id"):
        return False
    if supersession.get("authenticated") is not True:
        return False
    if not isinstance(supersession.get("approved_by"), str) or not str(
        supersession["approved_by"]
    ).strip():
        return False
    approved_at = _zoned_timestamp(supersession.get("approved_at"))
    if approved_at is None:
        return False
    rationale = supersession.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        return False
    superseded_candidate = supersession.get("superseded_candidate")
    if not isinstance(superseded_candidate, Mapping):
        return False
    superseded_fingerprint = decision_pair_candidate_fingerprint(
        superseded_candidate, {}
    )
    if superseded_fingerprint != fingerprint:
        return False
    previous_decided_at = _zoned_timestamp(previous.get("decided_at"))
    return previous_decided_at is not None and approved_at >= previous_decided_at


def reviewed_pair_decision_index(
    payload: object,
) -> dict[PairCandidateFingerprint, dict[str, str]]:
    """Return only complete, provenance-bearing durable pair decisions.

    Malformed groups and raw candidates are deliberately inert: neither sync
    nor review rendering may let them clear a live candidate.  In contrast,
    any duplicate decision for the exact same full fingerprint is a
    data-integrity error unless the later row carries an explicit,
    authenticated, exact supersession receipt.
    """
    if not isinstance(payload, Mapping):
        raise ValueError("paired-publication decisions must be a JSON object")
    groups = payload.get("groups")
    if not isinstance(groups, list):
        raise ValueError("paired-publication decisions must contain a groups list")

    indexed: dict[PairCandidateFingerprint, dict[str, str]] = {}
    group_ids: set[str] = set()
    for group in groups:
        if not isinstance(group, Mapping):
            continue
        group_id = group.get("id")
        decision = _candidate_text(group.get("decision"), casefold=True)
        decided_by = group.get("decided_by")
        decided_at = _zoned_timestamp(group.get("decided_at"))
        raw_candidates = group.get("raw_candidates")
        raw_candidate_count = group.get("raw_candidate_count")
        if (
            not isinstance(group_id, str)
            or not group_id.strip()
            or group_id in group_ids
            or decision not in _PAIR_DECISION_VALUES
            or not isinstance(decided_by, str)
            or not decided_by.strip()
            or decided_at is None
            or not _decision_note(payload, group)
            or not isinstance(raw_candidates, list)
            or (
                raw_candidate_count is not None
                and (
                    not isinstance(raw_candidate_count, int)
                    or isinstance(raw_candidate_count, bool)
                    or raw_candidate_count != len(raw_candidates)
                )
            )
        ):
            # A decision lacking identity, human provenance, or a usable
            # rationale remains inert rather than clearing a future candidate.
            continue
        group_ids.add(group_id)
        record = {
            "decision": decision,
            "group_id": group_id,
            "folder": _candidate_text(group.get("folder")),
            "representation": _candidate_text(group.get("representation")),
            "decided_by": decided_by.strip(),
            "decided_at": group["decided_at"].strip(),
        }
        for raw_candidate in raw_candidates:
            fingerprint = decision_pair_candidate_fingerprint(raw_candidate, group)
            if fingerprint is None:
                continue
            existing = indexed.get(fingerprint)
            if existing is None:
                indexed[fingerprint] = record
                continue
            if _authenticated_supersession(
                group, previous=existing, fingerprint=fingerprint
            ):
                indexed[fingerprint] = record
                continue
            raise ValueError(
                "duplicate paired-publication decisions for exact candidate "
                f"{fingerprint!r}: {existing['group_id']} vs {group_id}"
            )
    return indexed


def is_ignored_release(release: GitHubRelease) -> bool:
    """Return True for integration-test releases that should never be catalogued."""
    text = " ".join([release.repo, release.tag, release.name, release.body]).lower()
    ignore_markers = (
        "do not cite",
        "don't cite",
        "release smoke",
        "smoke test",
        "integration test",
        "-release-smoke",
        "template-release-smoke",
    )
    return any(marker in text for marker in ignore_markers)


def _identifier_text(record: ZenodoRecord) -> str:
    values: list[str] = []
    for item in record.related_identifiers:
        if isinstance(item, dict):
            values.extend(str(value) for value in item.values() if value)
    return " ".join(values)


def _word_tokens(value: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9]+", value or "") if token.lower() not in _STOP_WORDS}


def title_overlap(left: str, right: str) -> float:
    left_tokens = _word_tokens(left)
    right_tokens = _word_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens))


def confidence_for_pair(release: GitHubRelease, record: ZenodoRecord) -> PublicationPair | None:
    """Classify a GitHub release / Zenodo record pair."""
    if is_ignored_release(release):
        return None
    evidence: list[str] = []
    release_text = release.text
    release_text_lower = release_text.lower()
    identifier_text = _identifier_text(record)
    identifier_text_lower = identifier_text.lower()

    release_dois = {doi.lower() for doi in extract_dois(release_text)}
    if record.doi and record.doi.lower() in release_dois:
        evidence.append("github_release_mentions_doi")

    if record.record_url and record.record_url.lower() in release_text_lower:
        evidence.append("github_release_mentions_zenodo_record")

    if release.html_url and release.html_url.lower() in identifier_text_lower:
        evidence.append("zenodo_related_identifier_mentions_release")

    repo_url = f"https://github.com/{release.full_name}".lower()
    if repo_url in identifier_text_lower:
        evidence.append("github_repo_self_linked")

    overlap = title_overlap(release.name, record.title)
    if overlap >= 0.65:
        evidence.append("title_overlap")

    if not evidence:
        return None

    strong_markers = {
        "github_release_mentions_doi",
        "github_release_mentions_zenodo_record",
        "zenodo_related_identifier_mentions_release",
    }
    strong = "github_release_mentions_doi" in evidence or (
        bool(strong_markers & set(evidence))
        and (
            "title_overlap" in evidence
            or "github_repo_self_linked" in evidence
            or "zenodo_related_identifier_mentions_release" in evidence
            or "github_release_mentions_zenodo_record" in evidence
        )
    )
    confidence = "strong" if strong else "needs_review"
    return PublicationPair(
        release=release,
        record=record,
        confidence=confidence,
        evidence=tuple(evidence),
    )


def find_publication_pairs(
    releases: Iterable[GitHubRelease],
    records: Iterable[ZenodoRecord],
) -> list[PublicationPair]:
    """Return best release/record pair candidates sorted by confidence and DOI."""
    pairs: list[PublicationPair] = []
    seen: set[tuple[str, str]] = set()
    records_list = list(records)
    for release in releases:
        for record in records_list:
            pair = confidence_for_pair(release, record)
            if pair is None:
                continue
            key = (pair.github_release_url, pair.doi)
            if key in seen:
                continue
            seen.add(key)
            pairs.append(pair)
    rank = {"strong": 0, "needs_review": 1}
    return sorted(
        pairs,
        key=lambda pair: (
            rank.get(pair.confidence, 9),
            pair.record.publication_date or "",
            pair.github_repo,
            pair.doi,
        ),
        reverse=False,
    )


def slug_topic(title: str) -> str:
    head = title.split(":", 1)[0]
    words = re.findall(r"[A-Za-z0-9]+", head)
    if not words:
        words = re.findall(r"[A-Za-z0-9]+", title)
    words = [word for word in words if word.lower() not in {"a", "an", "and", "for", "in", "of", "on", "the", "to"}]
    words = words[:3] or ["Work"]
    return "".join(word[:1].upper() + word[1:] for word in words)


def infer_type(record: ZenodoRecord) -> str | None:
    values = " ".join(str(value) for value in record.resource_type.values()).lower()
    if "book" in values:
        return "Book"
    if "presentation" in values:
        return "Presentation"
    if "course" in values:
        return "Course"
    if "publication" in values or "article" in values or record.doi:
        return "Paper"
    return None


def metadata_payload(pair: PublicationPair) -> dict[str, Any]:
    release = pair.release
    record = pair.record
    files = []
    for item in record.files:
        if isinstance(item, dict):
            files.append(
                {
                    "name": item.get("key") or item.get("filename") or "",
                    "size_bytes": item.get("size"),
                    "checksum": item.get("checksum", ""),
                    "download_url": (item.get("links") or {}).get("self") if isinstance(item.get("links"), dict) else "",
                }
            )
    payload = {
        "title": record.title,
        "version": record.version,
        "doi": record.doi,
        "doi_url": record.doi_url,
        "zenodo_record": record.record_url,
        "record_id": record.record_id,
        "publication_date": record.publication_date,
        "resource_type": record.resource_type,
        "creators": record.creators,
        "description": record.description,
        "keywords": record.keywords,
        "files": files,
        "related_resources": [{"type": "repository", "url": f"https://github.com/{release.full_name}"}],
        "github_repo": release.full_name,
        "github_release_url": release.html_url,
        "release_tag": release.tag,
        "release_name": release.name,
        "pdf_sha256": extract_pdf_sha256(release.body),
        "pairing_confidence": pair.confidence,
        "pairing_evidence": list(pair.evidence),
        "checked_at": generated_timestamp(),
    }
    return payload


def render_readme(pair: PublicationPair, folder: str) -> str:
    record = pair.record
    keywords = " · ".join(record.keywords) if record.keywords else "paired GitHub and Zenodo publication"
    description = clean_abstract_text(record.description) or "Publication metadata synchronized from Zenodo and GitHub."
    pdf_lines = []
    for item in record.files:
        name = str(item.get("key") or item.get("filename") or "")
        if name.lower().endswith(".pdf"):
            pdf_lines.append(f"- `{name}` - Zenodo PDF")
    if not pdf_lines:
        pdf_lines.append("- Zenodo PDF: not downloaded")
    return f"""# {record.title}

**Daniel Ari Friedman** ({(record.publication_date or '')[:4] or 'n.d.'}) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/{record.doi}.svg)](https://doi.org/{record.doi})

---

## Abstract

{description}

## Keywords

{keywords}

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [{record.doi}](https://doi.org/{record.doi}) |
| **Published** | {record.publication_date or 'Unknown'} |
| **Version** | {record.version or 'Unknown'} |
| **Zenodo record** | {record.record_url} |
| **GitHub release** | {pair.github_release_url} |
| **Source repository** | https://github.com/{pair.github_repo} |

## Files

{chr(10).join(pdf_lines)}

## Citation

> Friedman, D. A. ({(record.publication_date or '')[:4] or 'n.d.'}). *{record.title}*. Zenodo. DOI: {record.doi}. URL: https://doi.org/{record.doi}.

## Related

- Zenodo record: {record.record_url}
- GitHub release: {pair.github_release_url}
- Source repository: https://github.com/{pair.github_repo}
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
"""


def render_agents(pair: PublicationPair) -> str:
    year = (pair.record.publication_date or "")[:4] or "n.d."
    return f"""# AGENTS.md - {pair.record.title}

**Paper**: {pair.record.title} ({year})
**DOI**: [{pair.doi}](https://doi.org/{pair.doi})
**GitHub release**: {pair.github_release_url}

---

## Agent Roles

### Citation Agent
- Use the Zenodo DOI as the canonical citation.
- Track future GitHub release and Zenodo version changes.

### Integration Agent
- Keep README, CITATION.cff, metadata.json, paper_metadata.json, BIBLIOGRAPHY.md, and software links synchronized.
- Preserve the paired GitHub + Zenodo release relationship.

## Extraction Log

- **Zenodo record**: {pair.zenodo_record_url}
- **GitHub release**: {pair.github_release_url}
- **Pairing evidence**: {", ".join(pair.evidence)}
"""


def render_skill(pair: PublicationPair, folder: str) -> str:
    tags = [tag.lower().replace(" ", "-") for tag in (pair.record.keywords or ["paired-publication"])[:8]]
    title = yaml_double_quoted(pair.record.title)
    return f"""---
name: "{slug_topic(pair.record.title)}"
description: "Use for {title}, a paired GitHub and Zenodo publication with DOI {pair.doi}."
tags: {json.dumps(tags)}
---

# {pair.record.title}

## Instructions

Use this skill when working with the publication **{pair.record.title}** or its paired release artifacts.

1. Ground citations in DOI `{pair.doi}`.
2. Treat the Zenodo record as the archival source and the GitHub release as the executable/source release.
3. Keep release tag `{pair.release.tag}` and repository `{pair.github_repo}` linked when updating catalog surfaces.

## Key Concepts

{chr(10).join(f'- **{keyword}**' for keyword in (pair.record.keywords or ['paired publication']))}

## Prerequisites

- Familiarity with the source repository and Zenodo record.
- Awareness that new versions may update both GitHub and Zenodo surfaces.

## Related

- [README.md](README.md)
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
"""


def render_citation(pair: PublicationPair) -> str:
    year = (pair.record.publication_date or "")[:4] or "n.d."
    version = f'\nversion: "{pair.record.version}"' if pair.record.version else ""
    title = yaml_double_quoted(pair.record.title)
    return f"""cff-version: 1.2.0
message: "If you use this work, please cite it as below."
type: article
title: "{title}"{version}
date-released: {pair.record.publication_date or year}
doi: {pair.doi}
url: "https://doi.org/{pair.doi}"
repository-code: "https://github.com/{pair.github_repo}"
authors:
  - family-names: Friedman
    given-names: Daniel Ari
    orcid: "https://orcid.org/{ORCID}"
identifiers:
  - type: doi
    value: {pair.doi}
    description: "Zenodo DOI"
  - type: url
    value: "{pair.zenodo_record_url}"
    description: "Zenodo landing page"
  - type: url
    value: "{pair.github_release_url}"
    description: "GitHub release"
"""
