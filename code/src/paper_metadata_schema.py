"""Dataclass schema for paper metadata validation.

Extends the current metadata.json structure with enriched fields for methods,
findings, related papers, and structured cross-referencing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


@dataclass
class PaperMetadata:
    """Extended metadata schema for paper folders.

    This schema validates and documents the structure of per-paper metadata.json
    files, extending the Zenodo-derived fields with additional indexing and
    cross-reference information.
    """

    # Core identification
    title: str = ""
    version: str | None = None
    doi: str = ""
    doi_url: str | None = None
    zenodo_record: str | None = None
    record_id: str | None = None
    publication_date: str | None = None

    # Classification
    resource_type: dict[str, Any] = field(default_factory=dict)
    domain: str | None = None  # 🐜/🧠/🛡️/🎨/💻/🌍/🎥/🧬
    type: str | None = None  # Paper, Book, Course, Presentation, Playbook, Series

    # Authors
    creators: list[dict[str, Any]] = field(default_factory=list)

    # Content
    description: str = ""
    abstract: str | None = None  # Extended abstract field
    keywords: list[str] = field(default_factory=list)

    # Technical
    files: list[dict[str, Any]] = field(default_factory=list)
    related_resources: list[dict[str, Any]] = field(default_factory=list)

    # Publication source
    venue: str | None = None
    github_repo: str | None = None
    github_release_url: str | None = None
    release_tag: str | None = None
    release_name: str | None = None

    # Validation
    pdf_sha256: str = ""
    pairing_confidence: str = "needs_review"  # strong or needs_review
    pairing_evidence: list[str] = field(default_factory=list)
    checked_at: str | None = None

    # Extended indexing fields
    methods: list[dict[str, str]] = field(default_factory=list)
    key_findings: list[str] = field(default_factory=list)
    related_papers: list[str] = field(default_factory=list)  # Folder names
    related_software: list[str] = field(default_factory=list)  # GitHub repo names
    citation_bibtex: str | None = None
    citation_apa: str | None = None
    license_spdx: str | None = None
    reproducibility_artifacts: list[str] = field(default_factory=list)
    dataset_references: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, path: Path | str) -> "PaperMetadata":
        """Load metadata from a JSON file."""
        p = Path(path)
        if p.exists():
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaperMetadata":
        """Create PaperMetadata from a dictionary, accepting any keys."""
        known_fields = {
            "title", "version", "doi", "doi_url", "zenodo_record", "record_id",
            "publication_date", "resource_type", "domain", "type", "creators",
            "description", "abstract", "keywords", "files", "related_resources",
            "venue", "github_repo", "github_release_url", "release_tag", "release_name",
            "pdf_sha256", "pairing_confidence", "pairing_evidence", "checked_at",
            "methods", "key_findings", "related_papers", "related_software",
            "citation_bibtex", "citation_apa", "license_spdx",
            "reproducibility_artifacts", "dataset_references",
        }
        init_kwargs = {}
        for key in known_fields:
            if key in data:
                init_kwargs[key] = data[key]
        return cls(**init_kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary, omitting None/empty values."""
        result = asdict(self)
        # Remove None values and empty collections
        result = {k: v for k, v in result.items() if v is not None and v != [] and v != {}}
        return result

    def validate(self) -> list[str]:
        """Validate metadata fields, returning list of issues."""
        issues = []
        if not self.title:
            issues.append("Missing title")
        if not self.doi and not self.venue:
            issues.append("Missing both DOI and venue")
        if self.doi and not self.doi.startswith("10."):
            issues.append(f"DOI does not look valid: {self.doi}")
        if self.pairing_confidence not in ("strong", "needs_review"):
            issues.append(f"Invalid pairing_confidence: {self.pairing_confidence}")
        return issues


def merge_metadata(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Merge overlay into base metadata, preserving existing values."""
    result = dict(base)
    for key, value in overlay.items():
        if key not in result or not result[key]:
            result[key] = value
    return result