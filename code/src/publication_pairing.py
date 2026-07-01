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
from pathlib import Path
from typing import Any, Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


def _contains_term(text: str, term: str) -> bool:
    """Whole-word/whole-phrase match so e.g. "ant" does not hit "dominant" and "art" does not hit "smart"."""
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def infer_domain(pair: PublicationPair) -> str | None:
    text = " ".join(
        [
            pair.record.title,
            pair.record.description,
            " ".join(pair.record.keywords),
            pair.github_repo,
            pair.release.name,
        ]
    ).lower()
    if any(_contains_term(text, term) for term in ["textbook", "reproducible", "computational", "software", "code", "pipeline"]):
        return "💻"
    if any(_contains_term(text, term) for term in ["active inference", "free energy", "bayesian", "markov blanket"]):
        return "🧠"
    if any(_contains_term(text, term) for term in ["cognitive security", "cogsec", "narrative", "trust", "integrity"]):
        return "🛡️"
    if any(_contains_term(text, term) for term in ["ant", "bee", "insect", "ento", "foraging"]):
        return "🐜"
    if any(_contains_term(text, term) for term in ["blake", "synergetics", "art", "fuller", "quadray"]):
        return "🎨"
    if any(_contains_term(text, term) for term in ["genetic", "genomic", "transcriptomic", "biomedical"]):
        return "🧬"
    if "activeinferenceinstitute" in text or "active inference institute" in text:
        return "🌍"
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

{record.description or 'Publication metadata synchronized from Zenodo and GitHub.'}

## Keywords

{keywords}

## Publication Details

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

> Friedman, D. A. ({(record.publication_date or '')[:4] or 'n.d.'}). *{record.title}*. Zenodo. https://doi.org/{record.doi}

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
