#!/usr/bin/env python3
"""Detect and optionally apply paired GitHub + Zenodo publications.

Default mode writes a dry-run report only. Pass ``--apply`` to update curated
source files and run the generated-surface refresh chain.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC_DIR))

from publication_pairing import (  # noqa: E402
    GitHubRelease,
    PublicationPair,
    SyncAction,
    ZenodoRecord,
    extract_pdf_sha256,
    find_publication_pairs,
)

ORCID = "0000-0001-6232-9096"
DEFAULT_OWNERS = ("docxology",)
AII_OWNER = "ActiveInferenceInstitute"
USER_AGENT = "docxology-paired-publication-sync/1.0 (+https://danielarifriedman.com/)"
BIBLIOGRAPHY = "pages/BIBLIOGRAPHY.md"
SOFTWARE = "pages/SOFTWARE.md"
PAPER_METADATA = "papers/paper_metadata.json"
TYPE_COUNTS_ORDER = ("Paper", "Presentation", "Book", "Course", "Playbook", "Series")
TYPE_LABELS = {
    "Paper": "Papers",
    "Presentation": "Presentations",
    "Book": "Books",
    "Course": "Courses",
    "Playbook": "Playbooks",
    "Series": "Series",
}


@dataclass(frozen=True)
class AppliedPublication:
    doi: str
    folder: str
    created: bool
    updated_files: tuple[str, ...]


def generated_timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def report_path_for_today(repo_root: Path = REPO_ROOT) -> Path:
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    return repo_root / "reports" / f"paired_publications_{today}.json"


def fetch_json(url: str, *, timeout: int = 30, github: bool = False) -> Any:
    headers = {"Accept": "application/vnd.github+json" if github else "application/json", "User-Agent": USER_AGENT}
    if github and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _paged_github(url_template: str) -> list[Any]:
    rows: list[Any] = []
    page = 1
    while True:
        batch = fetch_json(url_template.format(page=page), github=True)
        if not isinstance(batch, list):
            raise RuntimeError(f"Unexpected GitHub response from {url_template}: {batch!r}")
        rows.extend(batch)
        if len(batch) < 100:
            return rows
        page += 1


def fetch_github_repositories(owner: str) -> list[dict[str, Any]]:
    url = f"https://api.github.com/users/{owner}/repos?per_page=100&page={{page}}&sort=updated&direction=desc"
    return [repo for repo in _paged_github(url) if isinstance(repo, dict)]


def fetch_github_releases_for_repo(owner: str, repo: str) -> list[GitHubRelease]:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100&page={{page}}"
    return [GitHubRelease.from_api(owner, repo, item) for item in _paged_github(url) if isinstance(item, dict)]


def _date_at_or_after(value: str, since: str | None) -> bool:
    if not since:
        return True
    return (value or "")[:10] >= since


def fetch_github_releases(owners: list[str], *, since: str | None = None) -> tuple[list[GitHubRelease], list[str]]:
    releases: list[GitHubRelease] = []
    warnings: list[str] = []
    for owner in owners:
        try:
            repos = fetch_github_repositories(owner)
        except Exception as exc:  # pragma: no cover - network failures are report data
            warnings.append(f"github:{owner}: repositories: {type(exc).__name__}: {exc}")
            continue
        for repo in repos:
            name = str(repo.get("name") or "")
            if not name:
                continue
            repo_freshness = str(repo.get("pushed_at") or repo.get("updated_at") or "")
            if since and not _date_at_or_after(repo_freshness, since):
                continue
            try:
                repo_releases = fetch_github_releases_for_repo(owner, name)
            except Exception as exc:  # pragma: no cover - network failures are report data
                warnings.append(f"github:{owner}/{name}: releases: {type(exc).__name__}: {exc}")
                continue
            releases.extend(release for release in repo_releases if _date_at_or_after(release.published_at, since))
    return releases, warnings


def _zenodo_total(value: Any) -> int | None:
    if isinstance(value, dict):
        total = value.get("value")
    else:
        total = value
    return int(total) if isinstance(total, int) else None


def fetch_zenodo_query(query: str, *, size: int = 25) -> list[ZenodoRecord]:
    records: list[ZenodoRecord] = []
    total: int | None = None
    for page in range(1, 20):
        params = {"q": query, "size": size, "page": page, "sort": "mostrecent"}
        url = "https://zenodo.org/api/records?" + urllib.parse.urlencode(params)
        payload = fetch_json(url)
        hits = payload.get("hits", {}) if isinstance(payload, dict) else {}
        total = total if total is not None else _zenodo_total(hits.get("total"))
        batch = hits.get("hits", [])
        if not isinstance(batch, list) or not batch:
            break
        records.extend(ZenodoRecord.from_api(item) for item in batch if isinstance(item, dict))
        if total is not None and len(records) >= total:
            break
    return records


def fetch_zenodo_records() -> tuple[list[ZenodoRecord], list[str]]:
    queries = [
        f"metadata.creators.person_or_org.identifiers.identifier:{ORCID}",
        'creators.name:"Friedman, Daniel Ari"',
    ]
    records: list[ZenodoRecord] = []
    warnings: list[str] = []
    seen: set[str] = set()
    for query in queries:
        try:
            batch = fetch_zenodo_query(query)
        except Exception as exc:  # pragma: no cover - network failures are report data
            warnings.append(f"zenodo:{query}: {type(exc).__name__}: {exc}")
            continue
        for record in batch:
            key = record.record_id or record.doi
            if key in seen:
                continue
            seen.add(key)
            records.append(record)
    return records, warnings


def clean_markdown(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.replace("*", "").strip()


def parse_bibliography_rows(repo_root: Path = REPO_ROOT) -> list[dict[str, str]]:
    path = repo_root / BIBLIOGRAPHY
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        if not cells[0].isdigit():
            continue
        doi_match = re.search(r"(10\.\d{4,}/[^\s\])]+)", cells[6])
        folder_match = re.search(r"\.\./papers/(\d{4}_[^)/]+)/?", cells[7])
        rows.append(
            {
                "num": cells[0],
                "year": cells[1],
                "domain": cells[2],
                "type": cells[3],
                "title": clean_markdown(cells[4]),
                "venue": clean_markdown(cells[5]),
                "link": cells[6],
                "docs": cells[7],
                "doi": doi_match.group(1).rstrip(".,)") if doi_match else "",
                "folder": folder_match.group(1) if folder_match else "",
            }
        )
    return rows


def existing_doi_map(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    return {row["doi"]: row["folder"] for row in parse_bibliography_rows(repo_root) if row["doi"] and row["folder"]}


def _pair_key(title: str, github_release_url: str) -> tuple[str, str]:
    normalized_title = re.sub(r"\s+", " ", title.strip().lower())
    return normalized_title, github_release_url.strip()


def existing_release_title_map(repo_root: Path = REPO_ROOT) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    papers_dir = repo_root / "papers"
    if not papers_dir.exists():
        return out
    for folder_path in sorted(path for path in papers_dir.iterdir() if path.is_dir() and re.match(r"\d{4}_", path.name)):
        metadata_path = folder_path / "metadata.json"
        if not metadata_path.exists():
            continue
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        title = str(metadata.get("title") or "")
        release_url = str(metadata.get("github_release_url") or "")
        if title and release_url:
            out.setdefault(_pair_key(title, release_url), folder_path.name)
    return out


def slug_topic(title: str) -> str:
    head = title.split(":", 1)[0]
    words = re.findall(r"[A-Za-z0-9]+", head)
    if not words:
        words = re.findall(r"[A-Za-z0-9]+", title)
    words = [word for word in words if word.lower() not in {"a", "an", "and", "for", "in", "of", "on", "the", "to"}]
    words = words[:3] or ["Work"]
    return "".join(word[:1].upper() + word[1:] for word in words)


def folder_for_pair(pair: PublicationPair, repo_root: Path = REPO_ROOT) -> str:
    existing = existing_doi_map(repo_root).get(pair.doi)
    if existing:
        return existing
    existing_by_release = existing_release_title_map(repo_root).get(_pair_key(pair.record.title, pair.github_release_url))
    if existing_by_release:
        return existing_by_release
    year_match = re.search(r"\d{4}", pair.record.publication_date or pair.release.published_at)
    year = year_match.group(0) if year_match else str(dt.datetime.now().year)
    base = f"{year}_{slug_topic(pair.record.title)}"
    candidate = base
    i = 2
    while (repo_root / "papers" / candidate).exists():
        if (repo_root / "papers" / candidate / "metadata.json").exists():
            try:
                meta = json.loads((repo_root / "papers" / candidate / "metadata.json").read_text(encoding="utf-8"))
                if meta.get("doi") == pair.doi:
                    return candidate
            except json.JSONDecodeError:
                pass
        candidate = f"{base}{i}"
        i += 1
    return candidate


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
    if any(term in text for term in ["textbook", "reproducible", "computational", "software", "code", "pipeline"]):
        return "💻"
    if any(term in text for term in ["active inference", "free energy", "bayesian", "markov blanket"]):
        return "🧠"
    if any(term in text for term in ["cognitive security", "cogsec", "narrative", "trust", "integrity"]):
        return "🛡️"
    if any(term in text for term in ["ant", "bee", "insect", "ento", "foraging"]):
        return "🐜"
    if any(term in text for term in ["blake", "synergetics", "art", "fuller", "quadray"]):
        return "🎨"
    if any(term in text for term in ["genetic", "genomic", "transcriptomic", "biomedical"]):
        return "🧬"
    if "activeinferenceinstitute" in text or "active inference institute" in text:
        return "🌍"
    return None


def build_sync_actions(pairs: list[PublicationPair], *, repo_root: Path = REPO_ROOT) -> list[SyncAction]:
    doi_to_folder = existing_doi_map(repo_root)
    release_title_to_folder = existing_release_title_map(repo_root)
    actions: list[SyncAction] = []
    for pair in pairs:
        release_title_folder = release_title_to_folder.get(_pair_key(pair.record.title, pair.github_release_url))
        folder = doi_to_folder.get(pair.doi) or release_title_folder or folder_for_pair(pair, repo_root)
        if pair.confidence != "strong":
            action_type = "needs_review"
            reason = "pair lacks DOI/release cross-link evidence required for automatic apply"
        elif pair.doi in doi_to_folder:
            action_type = "update_existing"
            reason = "DOI already exists in bibliography; update folder metadata and software links"
        elif release_title_folder:
            action_type = "update_existing"
            reason = "same title and GitHub release already exist; update Zenodo version metadata"
        elif not infer_type(pair.record) or not infer_domain(pair):
            action_type = "needs_review"
            reason = "new pair is strong, but type or domain cannot be inferred safely"
        else:
            action_type = "create_new"
            reason = "strong new DOI/release pair"
        actions.append(
            SyncAction(
                action_type=action_type,
                doi=pair.doi,
                title=pair.record.title,
                confidence=pair.confidence,
                reason=reason,
                github_repo=pair.github_repo,
                github_release_url=pair.github_release_url,
                zenodo_record_url=pair.zenodo_record_url,
                folder=folder,
            )
        )
    return actions


def _safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _write_if_changed(path: Path, content: str, updated: list[str], repo_root: Path) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    updated.append(str(path.relative_to(repo_root)))


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
    return f"""---
name: "{slug_topic(pair.record.title)}"
description: "Use for {pair.record.title}, a paired GitHub and Zenodo publication with DOI {pair.doi}."
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
    return f"""cff-version: 1.2.0
message: "If you use this work, please cite it as below."
type: article
title: "{pair.record.title}"{version}
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


def update_existing_readme(path: Path, pair: PublicationPair, updated: list[str], repo_root: Path) -> None:
    text = _safe_read(path)
    if not text:
        return
    additions = []
    if pair.github_release_url not in text:
        additions.append(f"- GitHub release: {pair.github_release_url}")
    if pair.zenodo_record_url not in text:
        additions.append(f"- Zenodo record: {pair.zenodo_record_url}")
    if not additions:
        return
    if "## Related" in text:
        text = text.replace("## Related", "## Related\n\n" + "\n".join(additions), 1)
    else:
        text = text.rstrip() + "\n\n## Related\n\n" + "\n".join(additions) + "\n"
    _write_if_changed(path, text, updated, repo_root)


def update_existing_citation(path: Path, pair: PublicationPair, updated: list[str], repo_root: Path) -> None:
    text = _safe_read(path)
    if not text:
        return
    if pair.github_release_url in text:
        return
    block = (
        f'  - type: url\n'
        f'    value: "{pair.github_release_url}"\n'
        f'    description: "GitHub release"\n'
    )
    if "identifiers:" in text:
        text = text.rstrip() + "\n" + block
    else:
        text = text.rstrip() + "\nidentifiers:\n" + block
    _write_if_changed(path, text, updated, repo_root)


def update_metadata_json(path: Path, pair: PublicationPair, updated: list[str], repo_root: Path) -> None:
    existing: dict[str, Any] = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    merged = {**existing, **metadata_payload(pair)}
    _write_if_changed(path, json.dumps(merged, indent=2, ensure_ascii=False) + "\n", updated, repo_root)


def download_zenodo_pdf(pair: PublicationPair, folder_path: Path, updated: list[str], repo_root: Path) -> None:
    for item in pair.record.files:
        name = str(item.get("key") or item.get("filename") or "")
        if not name.lower().endswith(".pdf"):
            continue
        links = item.get("links") if isinstance(item.get("links"), dict) else {}
        url = links.get("self") or links.get("download")
        if not url:
            continue
        target = folder_path / name
        if target.exists():
            return
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as response:
            target.write_bytes(response.read())
        updated.append(str(target.relative_to(repo_root)))
        return


def ensure_bibliography_row(pair: PublicationPair, folder: str, updated: list[str], repo_root: Path) -> None:
    path = repo_root / BIBLIOGRAPHY
    text = _safe_read(path)
    if pair.doi in text:
        return
    folder_link = f"../papers/{folder}/"
    out_lines: list[str] = []
    replaced = False
    for line in text.splitlines():
        if line.startswith("|") and folder_link in line:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 8 and cells[0].isdigit():
                cells[4] = pair.record.title
                cells[5] = "*Zenodo*"
                cells[6] = f"[{pair.doi}](https://doi.org/{pair.doi})"
                cells[7] = f"[📁](../papers/{folder}/)"
                line = "| " + " | ".join(cells[:8]) + " |"
                replaced = True
        out_lines.append(line)
    if replaced:
        out = "\n".join(out_lines).rstrip() + "\n"
        out = refresh_bibliography_counts(out)
        _write_if_changed(path, out, updated, repo_root)
        return
    rows = parse_bibliography_rows(repo_root)
    next_num = max([int(row["num"]) for row in rows], default=0) + 1
    year = (pair.record.publication_date or "")[:4] or (pair.release.published_at or "")[:4] or "n.d."
    typ = infer_type(pair.record) or "Paper"
    domain = infer_domain(pair) or "💻"
    row = (
        f"| {next_num} | {year} | {domain} | {typ} | {pair.record.title} | *Zenodo* | "
        f"[{pair.doi}](https://doi.org/{pair.doi}) | [📁](../papers/{folder}/) |"
    )
    lines = text.splitlines()
    insert_at = len(lines)
    in_table = False
    for idx, line in enumerate(lines):
        if line.startswith("| # | Year | Domain | Type |"):
            in_table = True
            continue
        if in_table and line.startswith("|"):
            continue
        if in_table:
            insert_at = idx
            break
    lines.insert(insert_at, row)
    out = "\n".join(lines).rstrip() + "\n"
    out = refresh_bibliography_counts(out)
    _write_if_changed(path, out, updated, repo_root)


def refresh_bibliography_counts(text: str) -> str:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            rows.append(cells)
    if not rows:
        return text
    count = len(rows)
    text = re.sub(r"\*\*\d+\s+works\*\*", f"**{count} works**", text, count=1)
    text = re.sub(r">\s+\*\*\d+\*\*\s+works", f"> **{count}** works", text, count=1)
    type_counts = {typ: 0 for typ in TYPE_COUNTS_ORDER}
    for row in rows:
        type_counts[row[3]] = type_counts.get(row[3], 0) + 1
    summary = " · ".join(
        f"**{type_counts.get(typ, 0)}** {TYPE_LABELS.get(typ, typ)}"
        for typ in TYPE_COUNTS_ORDER
        if type_counts.get(typ, 0)
    )
    text = re.sub(
        r"\*\*\d+\*\* Papers · \*\*\d+\*\* Presentations · \*\*\d+\*\* Books · \*\*\d+\*\* Courses · \*\*\d+\*\* Playbooks · \*\*\d+\*\* Series\w*",
        summary,
        text,
        count=1,
    )
    return text


def update_paper_metadata_index(pair: PublicationPair, folder: str, updated: list[str], repo_root: Path) -> None:
    path = repo_root / PAPER_METADATA
    try:
        data = json.loads(_safe_read(path) or "{}")
    except json.JSONDecodeError:
        data = {}
    year, topic = folder.split("_", 1)
    data[folder] = {
        "year": year,
        "topic": topic,
        "name": pair.record.title,
        "description": pair.record.description,
        "authors": "Daniel Ari Friedman",
        "abstract": pair.record.description,
        "keywords": pair.record.keywords,
        "doi": pair.doi,
        "github_release_url": pair.github_release_url,
    }
    _write_if_changed(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", updated, repo_root)


def update_papers_readme(folder: str, pair: PublicationPair, updated: list[str], repo_root: Path) -> None:
    path = repo_root / "papers" / "README.md"
    text = _safe_read(path)
    if not text:
        return
    if f"]({folder}/)" not in text:
        rows = [line for line in text.splitlines() if re.match(r"\| \d+ \|", line)]
        next_num = len(rows) + 1
        year, topic = folder.split("_", 1)
        row = f"| {next_num} | [{folder}]({folder}/) | ✅ | {year} | {topic} |"
        lines = text.splitlines()
        insert_at = len(lines)
        for idx, line in enumerate(lines):
            if line.startswith("## Scripts"):
                insert_at = idx
                break
        lines.insert(insert_at, row)
        text = "\n".join(lines).rstrip() + "\n"
    count = len([line for line in text.splitlines() if re.match(r"\| \d+ \|", line)])
    text = re.sub(r"## Papers \(\d+\)", f"## Papers ({count})", text)
    _write_if_changed(path, text, updated, repo_root)


def update_papers_agents(updated: list[str], repo_root: Path) -> None:
    path = repo_root / "papers" / "AGENTS.md"
    text = _safe_read(path)
    if not text:
        return
    folder_count = len([path for path in (repo_root / "papers").iterdir() if path.is_dir() and re.match(r"\d{4}_", path.name)])
    text = re.sub(r"for \d+ publications", f"for {folder_count} publications", text)
    text = re.sub(r"\(\d+ entries as of [^)]+\)", f"({folder_count} entries as of {dt.date.today().isoformat()})", text)
    text = re.sub(r"README\.md present \| \d+/\d+ folders", f"README.md present | {folder_count}/{folder_count} folders", text)
    text = re.sub(r"AGENTS\.md present \| \d+/\d+", f"AGENTS.md present | {folder_count}/{folder_count}", text)
    text = re.sub(r"SKILL\.md present \| \d+/\d+", f"SKILL.md present | {folder_count}/{folder_count}", text)
    _write_if_changed(path, text, updated, repo_root)


def update_software_row(pair: PublicationPair, folder: str, updated: list[str], repo_root: Path) -> None:
    path = repo_root / SOFTWARE
    text = _safe_read(path)
    if not text:
        return
    repo_url = f"https://github.com/{pair.github_repo}"
    out_lines = []
    changed = False
    for line in text.splitlines():
        if line.startswith("| [") and f"]({repo_url})" in line:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 5:
                desc = cells[1]
                additions = []
                if pair.record.doi_url not in desc:
                    additions.append(f"[Zenodo]({pair.record.doi_url})")
                paper_link = f"[📄](../papers/{folder}/)"
                if paper_link not in desc:
                    additions.append(paper_link)
                if additions:
                    desc = desc.rstrip()
                    desc += " · " + " · ".join(additions)
                    cells[1] = desc
                    line = "| " + " | ".join(cells) + " |"
                    changed = True
        out_lines.append(line)
    if changed:
        _write_if_changed(path, "\n".join(out_lines).rstrip() + "\n", updated, repo_root)


def apply_publication_pair(
    pair: PublicationPair,
    *,
    repo_root: Path = REPO_ROOT,
    download_files: bool = True,
    folder: str | None = None,
    refresh_docs: bool = False,
) -> AppliedPublication:
    folder = folder or folder_for_pair(pair, repo_root)
    folder_path = repo_root / "papers" / folder
    created = not folder_path.exists()
    updated: list[str] = []
    folder_path.mkdir(parents=True, exist_ok=True)

    if created:
        _write_if_changed(folder_path / "README.md", render_readme(pair, folder), updated, repo_root)
        _write_if_changed(folder_path / "AGENTS.md", render_agents(pair), updated, repo_root)
        _write_if_changed(folder_path / "SKILL.md", render_skill(pair, folder), updated, repo_root)
        _write_if_changed(folder_path / "CITATION.cff", render_citation(pair), updated, repo_root)
    elif refresh_docs:
        _write_if_changed(folder_path / "README.md", render_readme(pair, folder), updated, repo_root)
        _write_if_changed(folder_path / "AGENTS.md", render_agents(pair), updated, repo_root)
        _write_if_changed(folder_path / "SKILL.md", render_skill(pair, folder), updated, repo_root)
        _write_if_changed(folder_path / "CITATION.cff", render_citation(pair), updated, repo_root)
    else:
        update_existing_readme(folder_path / "README.md", pair, updated, repo_root)
        update_existing_citation(folder_path / "CITATION.cff", pair, updated, repo_root)

    update_metadata_json(folder_path / "metadata.json", pair, updated, repo_root)
    if download_files:
        download_zenodo_pdf(pair, folder_path, updated, repo_root)
    ensure_bibliography_row(pair, folder, updated, repo_root)
    update_paper_metadata_index(pair, folder, updated, repo_root)
    update_papers_readme(folder, pair, updated, repo_root)
    update_papers_agents(updated, repo_root)
    update_software_row(pair, folder, updated, repo_root)
    return AppliedPublication(doi=pair.doi, folder=folder, created=created, updated_files=tuple(updated))


def write_report(
    path: Path,
    *,
    owners: list[str],
    releases: list[GitHubRelease],
    records: list[ZenodoRecord],
    pairs: list[PublicationPair],
    actions: list[SyncAction],
    warnings: list[str],
    applied: list[AppliedPublication] | None = None,
) -> None:
    payload = {
        "generated_at": generated_timestamp(),
        "source": "GitHub Releases API + Zenodo Records API",
        "owners": owners,
        "counts": {
            "github_releases": len(releases),
            "zenodo_records": len(records),
            "pairs": len(pairs),
            "strong_pairs": sum(1 for pair in pairs if pair.confidence == "strong"),
            "needs_review": sum(1 for action in actions if action.action_type == "needs_review"),
            "create_new": sum(1 for action in actions if action.action_type == "create_new"),
            "update_existing": sum(1 for action in actions if action.action_type == "update_existing"),
        },
        "warnings": warnings,
        "actions": [action.to_dict() for action in actions],
        "pairs": [pair.to_dict() for pair in pairs],
        "applied": [
            {"doi": item.doi, "folder": item.folder, "created": item.created, "updated_files": list(item.updated_files)}
            for item in (applied or [])
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_regeneration(repo_root: Path = REPO_ROOT) -> None:
    commands = [
        ["python3", "papers/sync_publications_html.py", "--apply"],
        ["python3", "code/orchestrators/export_bibliography.py"],
        ["python3", "papers/sync_software_html.py", "--apply"],
        ["python3", "code/orchestrators/export_agent_data.py"],
        ["python3", "code/orchestrators/build_domain_pages.py"],
        ["python3", "code/orchestrators/build_work_pages.py"],
        ["python3", "code/orchestrators/build_paper_pages.py"],
        ["python3", "code/orchestrators/audit_assets.py"],
        ["python3", "code/orchestrators/build_catalog.py"],
        ["python3", "code/orchestrators/build_search_index.py"],
        ["python3", "code/orchestrators/generate_feed.py"],
        ["python3", "code/orchestrators/build_sitemap.py"],
        ["python3", "code/orchestrators/build_generated_manifest.py"],
    ]
    for command in commands:
        subprocess.run(command, cwd=repo_root, check=True)


def latest_report(repo_root: Path = REPO_ROOT) -> Path | None:
    reports = sorted((repo_root / "reports").glob("paired_publications_*.json"))
    return reports[-1] if reports else None


def check_report(repo_root: Path = REPO_ROOT) -> None:
    path = latest_report(repo_root)
    if path is None:
        raise SystemExit("Missing paired publication report")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("source") != "GitHub Releases API + Zenodo Records API":
        raise SystemExit("Paired publication report has unexpected source")
    if "actions" not in payload or "pairs" not in payload or "counts" not in payload:
        raise SystemExit("Paired publication report missing required keys")
    print(f"checked paired publication report ({path.relative_to(repo_root)})")


def parse_owners(raw: str, include_aii: bool) -> list[str]:
    owners = [item.strip() for item in raw.split(",") if item.strip()]
    if include_aii and AII_OWNER not in owners:
        owners.append(AII_OWNER)
    return owners or list(DEFAULT_OWNERS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply strong create/update actions")
    parser.add_argument("--owners", default="docxology", help="Comma-separated GitHub owners to scan")
    parser.add_argument("--include-aii", action="store_true", help="Also scan ActiveInferenceInstitute")
    parser.add_argument("--since", help="Only consider GitHub releases published on/after YYYY-MM-DD")
    parser.add_argument("--report", help="Report path (default: reports/paired_publications_DATE.json)")
    parser.add_argument("--no-download-files", action="store_true", help="Do not download Zenodo PDFs during apply")
    parser.add_argument("--check", action="store_true", help="Validate the latest cached report")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.check:
        check_report()
        return 0
    owners = parse_owners(args.owners, args.include_aii)
    report = Path(args.report) if args.report else report_path_for_today()
    if not report.is_absolute():
        report = REPO_ROOT / report

    releases, github_warnings = fetch_github_releases(owners, since=args.since)
    records, zenodo_warnings = fetch_zenodo_records()
    pairs = find_publication_pairs(releases, records)
    actions = build_sync_actions(pairs)
    warnings = [*github_warnings, *zenodo_warnings]
    applied: list[AppliedPublication] = []
    changed = False

    if args.apply:
        for action, pair in zip(actions, pairs):
            if action.action_type not in {"create_new", "update_existing"}:
                continue
            item = apply_publication_pair(
                pair,
                download_files=not args.no_download_files,
                folder=action.folder,
                refresh_docs=action.reason.startswith("same title and GitHub release"),
            )
            applied.append(item)
            changed = changed or bool(item.updated_files)
        if changed:
            write_report(
                report,
                owners=owners,
                releases=releases,
                records=records,
                pairs=pairs,
                actions=actions,
                warnings=warnings,
                applied=applied,
            )
            run_regeneration()

    write_report(
        report,
        owners=owners,
        releases=releases,
        records=records,
        pairs=pairs,
        actions=actions,
        warnings=warnings,
        applied=applied,
    )
    print(
        f"wrote {report.relative_to(REPO_ROOT)}: "
        f"{len(pairs)} pairs, "
        f"{sum(1 for action in actions if action.action_type == 'create_new')} new, "
        f"{sum(1 for action in actions if action.action_type == 'update_existing')} updates, "
        f"{sum(1 for action in actions if action.action_type == 'needs_review')} needs review"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
