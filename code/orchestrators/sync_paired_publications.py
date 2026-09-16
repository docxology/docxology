#!/usr/bin/env python3
"""Detect and optionally apply paired GitHub + Zenodo publications.

Default mode writes a dry-run report only. Pass ``--apply`` to update curated
source files (paper folders, bibliography rows, software links). Regeneration
of the generated surfaces is left to ``regenerate_all.py``, which re-runs every
step this tool's former inline chain covered.

``--cache-reports`` reuses the latest same-day report's GitHub releases and
Zenodo records instead of re-fetching them (``--force`` lifts the same-day
requirement). The already_reviewed classification is persisted in the report
and keyed by bibliography + decision-log content hashes; a hash mismatch falls
back to the full classification scan -- drift is surfaced, never absorbed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.publication_pairing import (  # noqa: E402
    GitHubAsset,
    GitHubRelease,
    PairCandidateFingerprint,
    PublicationPair,
    SyncAction,
    ZenodoRecord,
    canonical_pair_candidate_fingerprint,
    find_publication_pairs,
    generated_timestamp,
    infer_domain,
    infer_type,
    metadata_payload,
    render_agents,
    render_citation,
    render_readme,
    render_skill,
    reviewed_pair_decision_index,
    slug_topic,
)

ORCID = "0000-0001-6232-9096"
DEFAULT_OWNERS = ("docxology",)
AII_OWNER = "ActiveInferenceInstitute"
USER_AGENT = "docxology-paired-publication-sync/1.0 (+https://danielarifriedman.com/)"
BIBLIOGRAPHY = "pages/BIBLIOGRAPHY.md"
SOFTWARE = "pages/SOFTWARE.md"
PAPER_METADATA = "papers/paper_metadata.json"
PAIRED_PUBLICATION_DECISIONS = "data/paired-publication-decisions.json"
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
    action: dict[str, Any] | None = None
    metadata_path: str = ""
    metadata_sha256: str = ""


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


def github_release_from_payload(payload: dict[str, Any]) -> GitHubRelease:
    """Rebuild a GitHubRelease from a report payload's serialized release."""
    try:
        return GitHubRelease(
            owner=str(payload["owner"]),
            repo=str(payload["repo"]),
            tag=str(payload["tag"]),
            name=str(payload["name"]),
            body=str(payload["body"]),
            html_url=str(payload["html_url"]),
            published_at=str(payload["published_at"]),
            assets=[
                GitHubAsset.from_api(item)
                for item in payload.get("assets", [])
                if isinstance(item, dict)
            ],
        )
    except KeyError as exc:
        raise ValueError(f"cached GitHub release is missing field {exc}") from exc


def github_releases_from_payload(payload: dict[str, Any]) -> list[GitHubRelease]:
    raw = payload.get("github_releases")
    if not isinstance(raw, list):
        raise ValueError("report payload has no github_releases list")
    releases: list[GitHubRelease] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("cached GitHub release entry is not an object")
        releases.append(github_release_from_payload(item))
    return releases


def zenodo_record_from_payload(payload: dict[str, Any]) -> ZenodoRecord:
    """Rebuild a ZenodoRecord from a report payload's to_dict() serialization."""
    version = payload.get("version")
    if version is not None and not isinstance(version, str):
        version = str(version)
    try:
        return ZenodoRecord(
            record_id=str(payload["record_id"]),
            doi=str(payload["doi"]),
            title=str(payload["title"]),
            publication_date=str(payload["publication_date"]),
            version=version,
            resource_type=(
                payload["resource_type"] if isinstance(payload.get("resource_type"), dict) else {}
            ),
            creators=payload["creators"] if isinstance(payload.get("creators"), list) else [],
            description=str(payload["description"]),
            keywords=[str(item) for item in (payload.get("keywords") or [])],
            related_identifiers=(
                payload["related_identifiers"]
                if isinstance(payload.get("related_identifiers"), list)
                else []
            ),
            files=payload["files"] if isinstance(payload.get("files"), list) else [],
            html_url=str(payload["html_url"]),
        )
    except KeyError as exc:
        raise ValueError(f"cached Zenodo record is missing field {exc}") from exc


def zenodo_records_from_payload(payload: dict[str, Any]) -> list[ZenodoRecord]:
    raw = payload.get("zenodo_records")
    if not isinstance(raw, list) or not raw:
        raise ValueError("report payload has no zenodo_records list")
    records: list[ZenodoRecord] = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("cached Zenodo record entry is not an object")
        records.append(zenodo_record_from_payload(item))
    return records


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


def _normalized_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def _pair_key(title: str, github_release_url: str) -> tuple[str, str]:
    return _normalized_title(title), github_release_url.strip()


def _repo_title_key(title: str, github_repo: str) -> tuple[str, str]:
    return _normalized_title(title), github_repo.strip().lower()


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


def existing_repo_title_map(repo_root: Path = REPO_ROOT) -> dict[tuple[str, str], str]:
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
        github_repo = str(metadata.get("github_repo") or "")
        if title and github_repo:
            out.setdefault(_repo_title_key(title, github_repo), folder_path.name)
    return out


def reviewed_pair_decisions(
    repo_root: Path = REPO_ROOT,
) -> dict[tuple[str, str, str, str, str, str], dict[str, str]]:
    """Load durable decisions keyed by their full reviewed candidate identity.

    A DOI/release-only key lets a later Zenodo record, title, repository, or
    tag inherit a decision that reviewed different public evidence.  Legacy
    rows are retained only when their group context reconstructs every field
    of the current canonical fingerprint.
    """
    path = repo_root / PAIRED_PUBLICATION_DECISIONS
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return reviewed_pair_decision_index(payload)


def folder_for_pair(pair: PublicationPair, repo_root: Path = REPO_ROOT) -> str:
    existing = existing_doi_map(repo_root).get(pair.doi)
    if existing:
        return existing
    existing_by_release = existing_release_title_map(repo_root).get(_pair_key(pair.record.title, pair.github_release_url))
    if existing_by_release:
        return existing_by_release
    existing_by_repo = existing_repo_title_map(repo_root).get(_repo_title_key(pair.record.title, pair.github_repo))
    if existing_by_repo:
        return existing_by_repo
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


PairFingerprintEntry = tuple[PairCandidateFingerprint, dict[str, str]]


@dataclass(frozen=True)
class ClassificationCache:
    """Cached already_reviewed classification keyed by curated-input hashes."""

    inputs: dict[str, str]
    already_reviewed: dict[PairCandidateFingerprint, dict[str, str]]


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def classification_inputs(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    """Hash the curated inputs the already_reviewed classification depends on.

    The class is fully determined by the durable decision log (fingerprinted
    per candidate), but the bibliography hash joins the key so any curated
    source drift invalidates the cache in the safe (full-rescan) direction.
    """
    return {
        "bibliography_sha256": _file_sha256(repo_root / BIBLIOGRAPHY),
        "decisions_sha256": _file_sha256(repo_root / PAIRED_PUBLICATION_DECISIONS),
    }


def classification_cache_from_payload(payload: object) -> ClassificationCache | None:
    """Parse a report's classification_cache block; ``None`` when unusable.

    Any structural problem makes the cache inert: the caller falls back to the
    full classification rather than absorbing an unreadable fingerprint.
    """
    if not isinstance(payload, dict):
        return None
    block = payload.get("classification_cache")
    if not isinstance(block, dict):
        return None
    inputs = block.get("inputs")
    entries = block.get("already_reviewed")
    if not isinstance(inputs, dict) or not isinstance(entries, list):
        return None
    if not all(isinstance(value, str) for value in inputs.values()):
        return None
    already: dict[PairCandidateFingerprint, dict[str, str]] = {}
    for entry in entries:
        if (
            not isinstance(entry, list)
            or len(entry) != 2
            or not isinstance(entry[0], list)
            or len(entry[0]) != 6
            or not all(isinstance(value, str) for value in entry[0])
            or not isinstance(entry[1], dict)
            or not all(isinstance(entry[1].get(key), str) for key in ("group_id", "representation", "folder"))
        ):
            return None
        already[tuple(entry[0])] = dict(entry[1])
    return ClassificationCache(
        inputs={str(key): str(value) for key, value in inputs.items()},
        already_reviewed=already,
    )


def classification_cache_payload(entries: list[PairFingerprintEntry], *, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    """Serialize this run's already_reviewed classification into the report."""
    return {
        "inputs": classification_inputs(repo_root),
        "already_reviewed": [[list(fingerprint), dict(info)] for fingerprint, info in entries],
    }
def build_sync_actions(
    pairs: list[PublicationPair],
    *,
    repo_root: Path = REPO_ROOT,
    cache: ClassificationCache | None = None,
    already_reviewed_entries: list[PairFingerprintEntry] | None = None,
) -> list[SyncAction]:
    """Classify pairs into sync actions, optionally from a validated cache.

    ``cache`` short-circuits the already_reviewed class only when its input
    hashes still match the on-disk bibliography and decision log; any drift
    falls back to the full classification. ``already_reviewed_entries``
    collects the (fingerprint, decision) pairs that back the report's
    persisted classification cache.
    """
    doi_to_folder = existing_doi_map(repo_root)
    release_title_to_folder: dict[tuple[str, str], str] = {}
    repo_title_to_folder: dict[tuple[str, str], str] = {}
    title_maps_loaded = False

    def title_maps() -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], str]]:
        nonlocal title_maps_loaded, release_title_to_folder, repo_title_to_folder
        if not title_maps_loaded:
            release_title_to_folder = existing_release_title_map(repo_root)
            repo_title_to_folder = existing_repo_title_map(repo_root)
            title_maps_loaded = True
        return release_title_to_folder, repo_title_to_folder

    reviewed_decisions: dict[PairCandidateFingerprint, dict[str, str]] | None = None

    def decisions() -> dict[PairCandidateFingerprint, dict[str, str]]:
        nonlocal reviewed_decisions
        if reviewed_decisions is None:
            reviewed_decisions = reviewed_pair_decisions(repo_root)
        return reviewed_decisions

    def resolved_folder(
        pair: PublicationPair,
    ) -> tuple[str, str | None, str | None]:
        release_map, repo_map = title_maps()
        release_title_folder = release_map.get(_pair_key(pair.record.title, pair.github_release_url))
        repo_title_folder = repo_map.get(_repo_title_key(pair.record.title, pair.github_repo))
        folder = (
            doi_to_folder.get(pair.doi)
            or release_title_folder
            or repo_title_folder
            or folder_for_pair(pair, repo_root)
        )
        return folder, release_title_folder, repo_title_folder

    use_cache = cache is not None and cache.inputs == classification_inputs(repo_root)
    if not use_cache:
        decisions()
        title_maps()
    actions: list[SyncAction] = []
    for pair in pairs:
        candidate_fingerprint = canonical_pair_candidate_fingerprint(
            doi=pair.doi,
            github_release_url=pair.github_release_url,
            zenodo_record_url=pair.zenodo_record_url,
            github_repo=pair.github_repo,
            title=pair.record.title,
            release_tag=pair.release.tag,
        )
        reviewed: dict[str, str] | None = None
        release_title_folder: str | None = None
        repo_title_folder: str | None = None
        if use_cache and candidate_fingerprint is not None:
            reviewed = cache.already_reviewed.get(candidate_fingerprint)
        if reviewed is not None:
            folder = reviewed.get("folder") or resolved_folder(pair)[0]
        else:
            folder, release_title_folder, repo_title_folder = resolved_folder(pair)
            reviewed = (
                decisions().get(candidate_fingerprint)
                if candidate_fingerprint is not None
                else None
            )
        if reviewed:
            action_type = "already_reviewed"
            representation = reviewed.get("representation") or "manual decision"
            group_id = reviewed.get("group_id") or "decision log"
            reason = f"{group_id} records this pair as {representation}; do not create a duplicate bibliography row"
            folder = reviewed.get("folder") or folder
            if already_reviewed_entries is not None and candidate_fingerprint is not None:
                already_reviewed_entries.append(
                    (
                        candidate_fingerprint,
                        {"group_id": group_id, "representation": representation, "folder": folder},
                    )
                )
        elif pair.confidence != "strong":
            action_type = "needs_review"
            reason = "pair lacks DOI/release cross-link evidence required for automatic apply"
        elif pair.doi in doi_to_folder:
            action_type = "update_existing"
            reason = "DOI already exists in bibliography; update folder metadata and software links"
        elif release_title_folder:
            action_type = "update_existing"
            reason = "same title and GitHub release already exist; update Zenodo version metadata"
        elif repo_title_folder:
            action_type = "update_existing"
            reason = "same title and GitHub repository already exist; update Zenodo version metadata"
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
                release_tag=pair.release.tag,
                folder=folder,
            )
        )
    return actions


def ordered_apply_pairs(
    actions: list[SyncAction], pairs: list[PublicationPair]
) -> list[tuple[SyncAction, PublicationPair]]:
    """Return writable pairs in a deterministic, version-safe order.

    GitHub returns releases newest-first, while a single Zenodo concept DOI can
    be paired with several releases in one scan. Applying that API order could
    leave ``metadata.json`` pointing at an older release after a newer one had
    already been applied. Grouping by DOI and sorting by release timestamp/tag
    makes the newest observed release the final metadata writer while retaining
    all release links in the folder.
    """
    candidates = [
        (action, pair)
        for action, pair in zip(actions, pairs)
        if action.action_type in {"create_new", "update_existing"}
    ]
    return sorted(
        candidates,
        key=lambda item: (
            item[1].doi.lower(),
            item[1].release.published_at or "",
            item[1].release.tag or "",
            item[1].github_release_url,
        ),
    )


def _safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _write_if_changed(path: Path, content: str, updated: list[str], repo_root: Path) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    updated.append(str(path.relative_to(repo_root)))


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _action_sha256(action: dict[str, Any]) -> str:
    """Hash the complete action so a report cannot prove only a matching DOI."""
    return hashlib.sha256(_canonical_json(action).encode("utf-8")).hexdigest()


def attest_applied_publication(
    applied: AppliedPublication,
    action: SyncAction,
    *,
    repo_root: Path = REPO_ROOT,
) -> AppliedPublication:
    """Bind an applied publication result to its exact action and metadata target."""
    if Path(applied.folder).name != applied.folder:
        raise ValueError(f"unsafe applied publication folder: {applied.folder!r}")
    metadata_path = repo_root / "papers" / applied.folder / "metadata.json"
    try:
        resolved = metadata_path.resolve()
        resolved.relative_to(repo_root.resolve())
        metadata_bytes = metadata_path.read_bytes()
        metadata = json.loads(metadata_bytes)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"cannot attest applied publication metadata for {applied.folder}: {exc}"
        ) from exc
    if not isinstance(metadata, dict) or str(metadata.get("doi") or "").casefold() != applied.doi.casefold():
        raise RuntimeError(
            f"cannot attest applied publication metadata for {applied.folder}: DOI does not match applied action"
        )
    action_payload = action.to_dict()
    return AppliedPublication(
        doi=applied.doi,
        folder=applied.folder,
        created=applied.created,
        updated_files=applied.updated_files,
        action=action_payload,
        metadata_path=metadata_path.relative_to(repo_root).as_posix(),
        metadata_sha256=hashlib.sha256(metadata_bytes).hexdigest(),
    )


def _verified_applied_update_receipt(
    receipt: object,
    action: SyncAction,
    *,
    repo_root: Path,
    require_current_metadata: bool = True,
) -> bool:
    """Verify an applied-update receipt, optionally against current metadata.

    One scan can apply several observed release versions to the same folder.
    Earlier receipts remain structurally attestable, but their metadata hash is
    intentionally superseded by the final writer.  Cache validation checks the
    durable receipt shape while review rendering separately requires the exact
    action to still match the on-disk metadata before calling it applied.
    """
    if not isinstance(receipt, dict):
        return False
    action_payload = action.to_dict()
    if receipt.get("action") != action_payload:
        return False
    if receipt.get("doi") != action.doi or receipt.get("folder") != action.folder:
        return False
    if not isinstance(receipt.get("created"), bool) or not isinstance(
        receipt.get("updated_files"), list
    ) or not all(
        isinstance(path, str) and path for path in receipt["updated_files"]
    ):
        return False
    provenance = receipt.get("provenance")
    action_sha256 = _action_sha256(action_payload)
    if not isinstance(provenance, dict) or provenance.get(
        "action_sha256"
    ) != action_sha256:
        return False
    expected_metadata_path = f"papers/{action.folder}/metadata.json"
    if provenance.get("metadata_path") != expected_metadata_path:
        return False
    metadata_sha256 = provenance.get("metadata_sha256")
    if not isinstance(metadata_sha256, str) or len(metadata_sha256) != 64:
        return False
    approval = provenance.get("approval")
    if (
        not isinstance(approval, dict)
        or approval.get("decision") != "approved"
        or approval.get("action_sha256") != action_sha256
        or not isinstance(approval.get("approved_by"), str)
        or not approval["approved_by"].strip()
        or not isinstance(approval.get("approved_at"), str)
        or not approval["approved_at"].endswith("Z")
    ):
        return False
    if not require_current_metadata:
        return True
    try:
        metadata_path = repo_root / expected_metadata_path
        metadata_bytes = metadata_path.read_bytes()
        metadata = json.loads(metadata_bytes)
    except (OSError, json.JSONDecodeError):
        return False
    return (
        hashlib.sha256(metadata_bytes).hexdigest() == metadata_sha256
        and isinstance(metadata, dict)
        and str(metadata.get("doi") or "").casefold() == action.doi.casefold()
    )


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


def _pdf_target(folder: Path, key: str) -> Path | None:
    """Return the safe on-disk target for a Zenodo file key, or ``None``.

    Only the basename is used so a hostile/compromised record cannot escape the
    paper folder via ``../`` or absolute paths; only ``.pdf`` keys resolve.
    """
    name = Path(str(key or "")).name
    if not name.lower().endswith(".pdf"):
        return None
    base = folder.resolve()
    target = (base / name).resolve()
    return target if target.parent == base else None


def download_zenodo_pdf(pair: PublicationPair, folder_path: Path, updated: list[str], repo_root: Path) -> None:
    for item in pair.record.files:
        name = str(item.get("key") or item.get("filename") or "")
        target = _pdf_target(folder_path, name)
        if target is None:
            continue
        links = item.get("links") if isinstance(item.get("links"), dict) else {}
        url = links.get("self") or links.get("download")
        if not url:
            continue
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
    # Keep the "**N** indexed paper folders" prose in sync with the table's folder
    # links (count_consistency._folder_links_in_bibliography validates this). Apply
    # used to bump the works total but not this, forcing a manual edit + failed
    # validate_repo on every new-folder publication.
    folder_links = sum(1 for row in rows if len(row) > 7 and "../papers/" in row[7])
    text = re.sub(
        r"\*\*\d+\*\*\s+indexed paper folders",
        f"**{folder_links}** indexed paper folders",
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
    text = re.sub(
        r"for \d+ publications",
        "for bibliography entries with in-tree documentation",
        text,
    )
    text = re.sub(
        r"\(\d+ entries as of [^)]+\)",
        "; current folder/export counts live in [`../reports/current_counts.md`](../reports/current_counts.md)",
        text,
    )
    text = re.sub(
        r"README\.md present \| \d+/\d+ folders[^|]*",
        "README.md present | required per folder; current coverage is generated in [`../reports/current_counts.md`](../reports/current_counts.md) ",
        text,
    )
    text = re.sub(r"AGENTS\.md present \| \d+/\d+", "AGENTS.md present | required per folder", text)
    text = re.sub(r"SKILL\.md present \| \d+/\d+", "SKILL.md present | required per folder", text)
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
    classification_cache: dict[str, Any] | None = None,
) -> None:
    generated_at = generated_timestamp()

    def applied_payload(item: AppliedPublication) -> dict[str, Any]:
        result: dict[str, Any] = {
            "doi": item.doi,
            "folder": item.folder,
            "created": item.created,
            "updated_files": list(item.updated_files),
        }
        if item.action is None:
            return result
        action_sha256 = _action_sha256(item.action)
        result["action"] = item.action
        result["provenance"] = {
            "action_sha256": action_sha256,
            "metadata_path": item.metadata_path,
            "metadata_sha256": item.metadata_sha256,
            "applied_at": generated_at,
            "approval": {
                "decision": "approved",
                "approved_by": "sync_paired_publications --apply",
                "approved_at": generated_at,
                "action_sha256": action_sha256,
            },
        }
        return result

    payload = {
        "generated_at": generated_at,
        "source": "GitHub Releases API + Zenodo Records API",
        "owners": owners,
        "counts": {
            "github_releases": len(releases),
            "zenodo_records": len(records),
            "pairs": len(pairs),
            "strong_pairs": sum(1 for pair in pairs if pair.confidence == "strong"),
            "already_reviewed": sum(1 for action in actions if action.action_type == "already_reviewed"),
            "needs_review": sum(1 for action in actions if action.action_type == "needs_review"),
            "create_new": sum(1 for action in actions if action.action_type == "create_new"),
            "update_existing": sum(1 for action in actions if action.action_type == "update_existing"),
        },
        "warnings": warnings,
        "actions": [action.to_dict() for action in actions],
        "pairs": [pair.to_dict() for pair in pairs],
        "github_releases": [release.to_dict() for release in releases],
        "zenodo_records": [record.to_dict() for record in records],
        "applied": [applied_payload(item) for item in (applied or [])],
    }
    if classification_cache is not None:
        payload["classification_cache"] = classification_cache
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def latest_report(repo_root: Path = REPO_ROOT) -> Path | None:
    reports = sorted((repo_root / "reports").glob("paired_publications_*.json"))
    return reports[-1] if reports else None


def display_report_path(path: Path, repo_root: Path = REPO_ROOT) -> str:
    """Return a compact report path without assuming it lives under the repo."""
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def check_report(repo_root: Path = REPO_ROOT) -> None:
    path = latest_report(repo_root)
    if path is None:
        raise SystemExit("Missing paired publication report")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("source") != "GitHub Releases API + Zenodo Records API":
        raise SystemExit("Paired publication report has unexpected source")
    if "actions" not in payload or "pairs" not in payload or "counts" not in payload:
        raise SystemExit("Paired publication report missing required keys")
    warnings = payload.get("warnings")
    if warnings:
        raise SystemExit(f"Paired publication report has API warnings: {len(warnings)}")
    actions = payload.get("actions")
    if not isinstance(actions, list):
        raise SystemExit("Paired publication report actions must be a list")
    counts = payload.get("counts")
    if not isinstance(counts, dict):
        raise SystemExit("Paired publication report counts must be an object")
    for action_type in ("create_new", "update_existing", "needs_review", "already_reviewed"):
        actual = sum(1 for action in actions if isinstance(action, dict) and action.get("action_type") == action_type)
        expected = counts.get(action_type, 0)
        if expected != actual:
            raise SystemExit(f"Paired publication report count mismatch for {action_type}: {expected} != {actual}")
    cache_block = payload.get("classification_cache")
    if cache_block is not None:
        cache = classification_cache_from_payload(payload)
        if cache is None:
            raise SystemExit("Paired publication report has a malformed classification_cache block")
        if cache.inputs != classification_inputs(repo_root):
            print(
                "note: paired publication report classification_cache inputs have drifted from the "
                "current bibliography/decision-log hashes; the next scan re-derives already_reviewed "
                "from full state",
                file=sys.stderr,
            )
    existing_dois = {row["doi"] for row in parse_bibliography_rows(repo_root) if row.get("doi")}
    applied_created_dois = {
        str(item.get("doi") or "")
        for item in payload.get("applied", [])
        if isinstance(item, dict) and item.get("created") is True
    }
    stale_create = [
        str(action.get("doi"))
        for action in actions
        if isinstance(action, dict)
        and action.get("action_type") == "create_new"
        and str(action.get("doi") or "") in existing_dois
        and str(action.get("doi") or "") not in applied_created_dois
    ]
    if stale_create:
        joined = ", ".join(stale_create)
        raise SystemExit(f"Paired publication report has stale create_new actions for existing DOIs: {joined}")
    applied = payload.get("applied", [])
    if not isinstance(applied, list):
        raise SystemExit("Paired publication report applied receipts must be a list")
    for action in actions:
        if (
            not isinstance(action, dict)
            or action.get("action_type") != "update_existing"
            or str(action.get("confidence") or "").casefold() != "strong"
        ):
            continue
        matching = [
            receipt
            for receipt in applied
            if isinstance(receipt, dict) and receipt.get("action") == action
        ]
        if matching and (
            len(matching) != 1
            or not _verified_applied_update_receipt(
                matching[0],
                SyncAction(
                    action_type=str(action.get("action_type") or ""),
                    doi=str(action.get("doi") or ""),
                    title=str(action.get("title") or ""),
                    confidence=str(action.get("confidence") or ""),
                    reason=str(action.get("reason") or ""),
                    github_repo=str(action.get("github_repo") or ""),
                    github_release_url=str(action.get("github_release_url") or ""),
                    zenodo_record_url=str(action.get("zenodo_record_url") or ""),
                    release_tag=str(action.get("release_tag") or ""),
                    folder=str(action.get("folder") or ""),
                ),
                repo_root=repo_root,
                require_current_metadata=False,
            )
        ):
            raise SystemExit(
                "Paired publication report has an unverifiable applied strong update receipt"
            )
    print(f"checked paired publication report ({path.relative_to(repo_root)})")


def parse_owners(raw: str, include_aii: bool) -> list[str]:
    owners = [item.strip() for item in raw.split(",") if item.strip()]
    if include_aii and AII_OWNER not in owners:
        owners.append(AII_OWNER)
    return owners or list(DEFAULT_OWNERS)


def load_cached_scan_payload(
    path: Path, *, force: bool = False
) -> tuple[list[GitHubRelease], list[ZenodoRecord]]:
    """Reuse a prior pairing scan's fetched releases and records.

    Freshness keys on the source report's ``generated_at`` date, not file
    presence: an older report is refused unless ``force``. A warned scan is
    always refused -- cache validation must not bless a scan that saw API
    errors.
    """
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Cannot reuse cached scan payload from {path}: {exc}") from exc
    if payload.get("source") != "GitHub Releases API + Zenodo Records API":
        raise SystemExit(f"Cannot reuse cached scan payload from {path}: unexpected report source")
    warnings = payload.get("warnings")
    if warnings:
        raise SystemExit(
            f"Refusing cached scan payload from {path}: {len(warnings)} API warning(s); rerun the live scan"
        )
    generated_at = str(payload.get("generated_at") or "")
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    if generated_at[:10] != today and not force:
        raise SystemExit(
            f"Cached scan payload {path} is not same-day (generated_at {generated_at}); "
            "pass --force to reuse it anyway"
        )
    try:
        return github_releases_from_payload(payload), zenodo_records_from_payload(payload)
    except ValueError as exc:
        raise SystemExit(f"Cannot reuse cached scan payload from {path}: {exc}") from exc


def classification_cache_from_report(repo_root: Path = REPO_ROOT) -> ClassificationCache | None:
    """Load the latest report's classification cache when its inputs still match disk.

    A missing, unreadable, or hash-drifted cache returns ``None`` so the caller
    runs the full classification -- drift is surfaced by the fallback, never
    absorbed.
    """
    path = latest_report(repo_root)
    if path is None:
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    cache = classification_cache_from_payload(payload)
    if cache is None or cache.inputs != classification_inputs(repo_root):
        return None
    return cache


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Runbook: docs/operations/publication-sync.md",
    )
    parser.add_argument("--apply", action="store_true", help="Apply strong create/update actions")
    parser.add_argument("--owners", default="docxology", help="Comma-separated GitHub owners to scan")
    parser.add_argument("--include-aii", action="store_true", help="Also scan ActiveInferenceInstitute")
    parser.add_argument("--since", help="Only consider GitHub releases published on/after YYYY-MM-DD")
    parser.add_argument("--report", help="Report path (default: reports/paired_publications_DATE.json)")
    parser.add_argument("--no-download-files", action="store_true", help="Do not download Zenodo PDFs during apply")
    parser.add_argument("--check", action="store_true", help="Validate the latest cached report")
    parser.add_argument(
        "--cache-reports",
        action="store_true",
        help="Reuse the latest same-day report's GitHub releases and Zenodo records instead of re-fetching",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --cache-reports: accept a source report that is not same-day",
    )
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

    if args.cache_reports:
        source = Path(args.report) if args.report else latest_report(REPO_ROOT)
        if source is None or not Path(source).exists():
            raise SystemExit("--cache-reports found no paired publication report to reuse")
        releases, records = load_cached_scan_payload(Path(source), force=args.force)
        github_warnings: list[str] = []
        zenodo_warnings: list[str] = []
        print(f"reusing cached scan payload from {display_report_path(Path(source))}")
    else:
        releases, github_warnings = fetch_github_releases(owners, since=args.since)
        records, zenodo_warnings = fetch_zenodo_records()
    if args.cache_reports and args.since:
        releases = [release for release in releases if _date_at_or_after(release.published_at, args.since)]
    pairs = find_publication_pairs(releases, records)
    already_reviewed_entries: list[PairFingerprintEntry] = []
    actions = build_sync_actions(
        pairs,
        cache=classification_cache_from_report(REPO_ROOT),
        already_reviewed_entries=already_reviewed_entries,
    )
    warnings = [*github_warnings, *zenodo_warnings]
    applied: list[AppliedPublication] = []
    changed = False

    if warnings:
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        raise SystemExit(f"Refusing to write paired publication report with API warnings: {len(warnings)}")

    if args.apply:
        for action, pair in ordered_apply_pairs(actions, pairs):
            item = apply_publication_pair(
                pair,
                download_files=not args.no_download_files,
                folder=action.folder,
                refresh_docs=action.reason.startswith("same title and GitHub"),
            )
            item = attest_applied_publication(item, action)
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
                classification_cache=classification_cache_payload(already_reviewed_entries),
            )

    write_report(
        report,
        owners=owners,
        releases=releases,
        records=records,
        pairs=pairs,
        actions=actions,
        warnings=warnings,
        applied=applied,
        classification_cache=classification_cache_payload(already_reviewed_entries),
    )
    print(
        f"wrote {display_report_path(report)}: "
        f"{len(pairs)} pairs, "
            f"{sum(1 for action in actions if action.action_type == 'create_new')} new, "
            f"{sum(1 for action in actions if action.action_type == 'update_existing')} updates, "
            f"{sum(1 for action in actions if action.action_type == 'needs_review')} needs review, "
            f"{sum(1 for action in actions if action.action_type == 'already_reviewed')} already reviewed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
