#!/usr/bin/env python3
"""regenerate_docs.py — Regenerate documentation files for all paper folders.

Reads paper_metadata.json and generates/updates README.md, AGENTS.md, and SKILL.md
for each paper folder. The generated-document manifest is the explicit ownership
boundary: unlisted existing documents are treated as hand-authored and are never
overwritten by this command.

Usage:
    python3 regenerate_docs.py                          # preview mode
    python3 regenerate_docs.py --apply                  # apply managed changes
    python3 regenerate_docs.py --check                  # no-write drift check
    python3 regenerate_docs.py --doi-audit              # JSON DOI-role audit
    python3 regenerate_docs.py --adopt-existing --apply # opt-in legacy adoption
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import stat
import sys
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import quote, urlsplit, urlunsplit

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from biblio_table import iter_bibliography_rows  # noqa: E402
from domain_inference import DOMAIN_TO_EMOJI, infer_domain_name  # noqa: E402

log = logging.getLogger(__name__)
BIBLIOGRAPHY_PATH = Path(os.environ.get("BIB_PATH", PAPERS_DIR.parent / "pages" / "BIBLIOGRAPHY.md"))
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
DOI_TRAILING = ".,;:)]}`'\""
DOCUMENT_FILENAMES = ("README.md", "AGENTS.md", "SKILL.md")
MANIFEST_FILENAME = "generated-documents.json"
MANIFEST_VERSION = 1
GENERATED_DOCUMENT_MARKER = "<!-- docxology:generated-document {filename}; ownership=explicit-manifest -->"


@dataclass(frozen=True)
class DocumentPaths:
    """Filesystem inputs for one paper-document generation run.

    The production CLI uses :data:`DEFAULT_DOCUMENT_PATHS`; callers that need
    an isolated corpus can pass an explicit instance without mutating module
    globals or changing the process environment.
    """

    papers_dir: Path
    bibliography_path: Path


DEFAULT_DOCUMENT_PATHS = DocumentPaths(
    papers_dir=PAPERS_DIR,
    bibliography_path=BIBLIOGRAPHY_PATH,
)

# ─── Helpers ──────────────────────────────────────────────────────────────────


def _lexical_absolute(path: Path) -> Path:
    """Return ``path`` as an absolute, normalized path without dereferencing links."""
    return Path(os.path.abspath(os.fspath(path)))


def _reject_symlink(path: Path, *, label: str) -> None:
    """Fail closed when a renderer input or output path is a symbolic link."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return
    except OSError as exc:
        raise ValueError(f"unable to inspect {label}: {path}: {exc}") from exc
    if stat.S_ISLNK(mode):
        raise ValueError(f"symlinked {label} is not permitted: {path}")


def _safe_papers_path(
    path: Path,
    *,
    label: str,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
    require_directory: bool = False,
    require_regular_if_present: bool = False,
) -> Path:
    """Return a safe paper-document path without following any symlink.

    The paper-document renderer has a narrow, explicit ownership boundary:
    its manifest and managed documents must remain beneath ``PAPERS_DIR``.  A
    symlink in the papers root, a paper folder, or a final managed path could
    otherwise make a no-write check read outside the checkout or make
    ``--apply`` overwrite an unrelated file.  Inspect each lexical component
    with ``lstat`` before reading or writing it, then verify resolved
    containment for an existing papers root.
    """
    papers_root = _lexical_absolute(paths.papers_dir)
    candidate = _lexical_absolute(path)
    try:
        relative = candidate.relative_to(papers_root)
    except ValueError as exc:
        raise ValueError(f"{label} must be contained in {papers_root}: {candidate}") from exc

    _reject_symlink(papers_root, label="papers root")
    current = papers_root
    for component in relative.parts:
        current = current / component
        _reject_symlink(current, label=label)

    # A missing papers directory remains compatible with the existing safe
    # no-op behavior for an absent local paper corpus.  When it exists, prove
    # that ordinary resolution still remains inside that real root.
    if papers_root.exists():
        try:
            resolved_root = papers_root.resolve(strict=True)
            candidate.resolve(strict=False).relative_to(resolved_root)
        except (OSError, ValueError) as exc:
            raise ValueError(f"{label} escapes the papers directory: {candidate}") from exc

    if require_directory and not candidate.is_dir():
        raise ValueError(f"{label} must be an existing directory: {candidate}")
    if require_regular_if_present and candidate.exists() and not candidate.is_file():
        raise ValueError(f"{label} must be a regular file when present: {candidate}")
    return candidate


def _safe_paper_folder(
    folder: str,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> Path:
    """Return one actual, non-symlink paper folder in the renderer boundary."""
    if not re.fullmatch(r"\d{4}_.+", folder) or Path(folder).name != folder:
        raise ValueError(f"invalid paper folder: {folder!r}")
    return _safe_papers_path(
        paths.papers_dir / folder,
        label=f"paper folder {folder}",
        paths=paths,
        require_directory=True,
    )


def _safe_managed_document_path(
    folder: str,
    filename: str,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> Path:
    """Return a managed document target after symlink and containment checks."""
    if filename not in DOCUMENT_FILENAMES:
        raise ValueError(f"unsupported generated document: {filename}")
    folder_path = _safe_paper_folder(folder, paths=paths)
    return _safe_papers_path(
        folder_path / filename,
        label=f"managed document {folder}/{filename}",
        paths=paths,
        require_regular_if_present=True,
    )


def _safe_manifest_path(
    path: Path,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> Path:
    """Return the manifest path only when it is a safe papers-local regular file."""
    return _safe_papers_path(
        path,
        label="generated-document manifest",
        paths=paths,
        require_regular_if_present=True,
    )


def _require_secure_relative_open() -> None:
    """Require the descriptor APIs needed to prevent symlink-swap writes.

    Falling back to ``Path.write_text`` would reintroduce a check-then-use
    race.  The renderer therefore declines to run on a platform without
    descriptor-relative opens and ``O_NOFOLLOW`` rather than weakening this
    ownership boundary.
    """
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY") or os.open not in os.supports_dir_fd:
        raise ValueError("secure no-follow paper-document I/O is unavailable on this platform")


def _open_papers_parent(
    path: Path,
    *,
    label: str,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> tuple[int, str]:
    """Open ``path``'s parent through no-follow directory descriptors."""
    _require_secure_relative_open()
    candidate = _safe_papers_path(path, label=label, paths=paths)
    papers_root = _lexical_absolute(paths.papers_dir)
    relative = candidate.relative_to(papers_root)
    if not relative.parts:
        raise ValueError(f"{label} must name a file beneath the papers root: {candidate}")

    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        parent_fd = os.open(papers_root, directory_flags)
    except OSError as exc:
        raise ValueError(f"unable to securely open papers root for {label}: {exc}") from exc
    try:
        for component in relative.parts[:-1]:
            try:
                next_fd = os.open(component, directory_flags, dir_fd=parent_fd)
            except OSError as exc:
                raise ValueError(f"unable to securely open {label} parent {component!r}: {exc}") from exc
            os.close(parent_fd)
            parent_fd = next_fd
        return parent_fd, relative.parts[-1]
    except Exception:
        os.close(parent_fd)
        raise


def _verify_regular_file_descriptor(
    file_descriptor: int,
    *,
    label: str,
    require_unique_link: bool,
) -> None:
    """Require a regular, non-aliased file descriptor before document I/O."""
    try:
        file_stat = os.fstat(file_descriptor)
    except OSError as exc:
        raise ValueError(f"unable to inspect opened {label}: {exc}") from exc
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError(f"{label} must be a regular file")
    if require_unique_link and file_stat.st_nlink != 1:
        raise ValueError(f"hard-linked {label} is not permitted")


def _read_papers_text(
    path: Path,
    *,
    label: str,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
    require_unique_link: bool = False,
) -> str | None:
    """Read a papers-local text file without following link swaps.

    ``None`` represents a missing file.  Any other unsafe or inaccessible
    state is a blocking error rather than an implicit missing document.
    """
    try:
        parent_fd, filename = _open_papers_parent(path, label=label, paths=paths)
    except ValueError as exc:
        if isinstance(exc.__cause__, FileNotFoundError):
            return None
        raise
    file_descriptor = -1
    try:
        try:
            file_descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise ValueError(f"unable to securely read {label}: {exc}") from exc
        _verify_regular_file_descriptor(
            file_descriptor,
            label=label,
            require_unique_link=require_unique_link,
        )
        with os.fdopen(file_descriptor, "r", encoding="utf-8") as handle:
            file_descriptor = -1
            return handle.read()
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        os.close(parent_fd)


def _write_papers_text(
    path: Path,
    content: str,
    *,
    label: str,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
    require_unique_link: bool,
) -> None:
    """Write a papers-local file through no-follow descriptors.

    The file is opened without ``O_TRUNC`` so a hard-link check can run before
    any bytes of an external alias are modified.  Directory descriptors keep
    a post-check symlink swap from redirecting the write.
    """
    parent_fd, filename = _open_papers_parent(path, label=label, paths=paths)
    file_descriptor = -1
    try:
        try:
            file_descriptor = os.open(
                filename,
                os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW,
                0o666,
                dir_fd=parent_fd,
            )
        except OSError as exc:
            raise ValueError(f"unable to securely open {label} for writing: {exc}") from exc
        _verify_regular_file_descriptor(
            file_descriptor,
            label=label,
            require_unique_link=require_unique_link,
        )
        os.ftruncate(file_descriptor, 0)
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            file_descriptor = -1
            handle.write(content)
    finally:
        if file_descriptor >= 0:
            os.close(file_descriptor)
        os.close(parent_fd)


def parse_folder_id(folder: str) -> tuple[str, str]:
    """Map directory name ``YYYY_Topic`` to ``(year, topic)``."""
    m = re.match(r"^(\d{4})_(.+)$", folder)
    if not m:
        return "unknown", folder
    return m.group(1), m.group(2)


def configure_logging() -> None:
    """Configure console-only logging.

    A validation command must be observational: in particular, importing or
    running this module cannot refresh a timestamped log file under ``papers/``.
    """
    if log.handlers:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


def generated_documents_manifest_path(
    *, paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS
) -> Path:
    """Return the explicit ownership manifest for generated paper documents."""
    return paths.papers_dir / MANIFEST_FILENAME


def generated_document_key(folder: str, filename: str) -> str:
    """Return the stable manifest key for one supported paper document."""
    return f"{folder}/{filename}"


def generated_document_marker(filename: str) -> str:
    """Return the stable ownership marker embedded in generated documents."""
    if filename == "SKILL.md":
        # SKILL.md begins with YAML frontmatter. Keep its ownership declaration
        # inside that frontmatter as a YAML comment so consumers requiring the
        # opening `---` delimiter remain compatible.
        return f"# docxology:generated-document {filename}; ownership=explicit-manifest"
    return GENERATED_DOCUMENT_MARKER.format(filename=filename)


def wrap_generated_document(filename: str, content: str) -> str:
    """Add the ownership marker and one canonical final newline to ``content``."""
    if filename == "SKILL.md":
        if not content.startswith("---\n"):
            raise ValueError("generated SKILL.md content must begin with YAML frontmatter")
        return f"---\n{generated_document_marker(filename)}\n{content.removeprefix('---\n').rstrip()}\n"
    return f"{generated_document_marker(filename)}\n\n{content.rstrip()}\n"


def is_generated_document(filename: str, content: str) -> bool:
    """Return whether ``content`` declares ownership by this generator."""
    if filename == "SKILL.md":
        return content.startswith("---\n" + generated_document_marker(filename) + "\n")
    return content.startswith(generated_document_marker(filename) + "\n")


@dataclass(frozen=True)
class ManifestEntry:
    """One explicit generated-document ownership record."""

    path: str
    adopt: bool = False


@dataclass(frozen=True)
class DocumentChange:
    """A safe, already-rendered document action."""

    path: Path
    key: str
    content: str
    action: str


def _validate_manifest_path(value: str) -> str:
    """Validate and normalize a manifest path without permitting traversal."""
    if not isinstance(value, str):
        raise ValueError("manifest document paths must be strings")
    if "\\" in value:
        raise ValueError(f"manifest path must use '/' separators: {value!r}")
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError(f"manifest path must be '<folder>/<document>': {value!r}")
    folder, filename = parts
    if not re.fullmatch(r"\d{4}_.+", folder):
        raise ValueError(f"manifest folder is not a paper folder: {folder!r}")
    if filename not in DOCUMENT_FILENAMES:
        raise ValueError(f"manifest document is unsupported: {filename!r}")
    return value


def load_generated_documents_manifest(
    path: Path | None = None,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> dict[str, ManifestEntry]:
    """Load the explicit generated-document ownership manifest.

    Existing documentation is deliberately *not* inferred from size, age, or
    resemblance to a renderer. A document becomes generator-owned only when it
    appears here (or is created by this command).
    """
    manifest_path = _safe_manifest_path(
        path or generated_documents_manifest_path(paths=paths),
        paths=paths,
    )
    raw_text = _read_papers_text(
        manifest_path,
        label="generated-document manifest",
        paths=paths,
        require_unique_link=True,
    )
    if raw_text is None:
        return {}
    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid generated-document manifest {manifest_path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"generated-document manifest {manifest_path} must be an object")
    if raw.get("version") != MANIFEST_VERSION:
        raise ValueError(
            f"generated-document manifest {manifest_path} must declare version {MANIFEST_VERSION}"
        )
    documents = raw.get("documents")
    if not isinstance(documents, list):
        raise ValueError(f"generated-document manifest {manifest_path} must contain a documents list")

    entries: dict[str, ManifestEntry] = {}
    for raw_entry in documents:
        if isinstance(raw_entry, str):
            entry = ManifestEntry(path=_validate_manifest_path(raw_entry))
        elif isinstance(raw_entry, dict):
            if set(raw_entry) - {"path", "adopt"}:
                unknown = ", ".join(sorted(set(raw_entry) - {"path", "adopt"}))
                raise ValueError(f"manifest entry has unsupported fields: {unknown}")
            entry = ManifestEntry(
                path=_validate_manifest_path(raw_entry.get("path")),
                adopt=raw_entry.get("adopt", False),
            )
            if not isinstance(entry.adopt, bool):
                raise ValueError(f"manifest adopt flag must be boolean: {entry.path}")
        else:
            raise ValueError("manifest document entries must be paths or objects")
        if entry.path in entries:
            raise ValueError(f"duplicate generated-document manifest entry: {entry.path}")
        entries[entry.path] = entry
    return entries


def render_generated_documents_manifest(entries: Iterable[ManifestEntry]) -> str:
    """Render the manifest deterministically with no clock-derived fields."""
    documents: list[dict[str, Any]] = []
    for entry in sorted(entries, key=lambda item: item.path):
        item: dict[str, Any] = {"path": entry.path}
        if entry.adopt:
            item["adopt"] = True
        documents.append(item)
    payload = {"version": MANIFEST_VERSION, "documents": documents}
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def write_generated_documents_manifest(
    path: Path,
    entries: Iterable[ManifestEntry],
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> None:
    """Write the ownership manifest only as part of an explicit ``--apply`` run."""
    manifest_path = _safe_manifest_path(path, paths=paths)
    _write_papers_text(
        manifest_path,
        render_generated_documents_manifest(entries),
        label="generated-document manifest",
        paths=paths,
        require_unique_link=True,
    )


def load_metadata(
    *, paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS
) -> dict[str, dict[str, Any]]:
    """Load consolidated metadata from paper_metadata.json."""
    _reject_symlink(paths.papers_dir, label="papers root")
    metadata_path = paths.papers_dir / "paper_metadata.json"
    metadata_text = _read_papers_text(
        metadata_path,
        label="consolidated paper metadata",
        paths=paths,
    )
    if metadata_text is not None:
        data = json.loads(metadata_text)
        if not isinstance(data, dict):
            raise ValueError(f"{metadata_path} must contain a metadata object")
        invalid_folders = [folder for folder, meta in data.items() if not isinstance(meta, dict)]
        if invalid_folders:
            raise ValueError(
                f"{metadata_path} contains non-object metadata for: {', '.join(sorted(invalid_folders)[:5])}"
            )
        return data
    log.warning("No paper_metadata.json found")
    return {}


def parse_bibliography(
    *, paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS
) -> dict[str, dict[str, Any]]:
    """Parse BIBLIOGRAPHY.md table into a dict keyed by folder name (rows with a Docs link)."""
    bib = {}
    if not paths.bibliography_path.exists():
        log.warning("BIBLIOGRAPHY.md not found")
        return bib
    for row in iter_bibliography_rows(paths.bibliography_path):
        folder = row.folder
        if not folder:
            continue
        bib[folder] = {
            "num": row.num,
            "year": row.year,
            "title": row.title,
            "venue": row.venue,
            "link": row.link_cell,
            # pages/BIBLIOGRAPHY.md is the canonical citation surface. Keep
            # this field distinct from a per-folder artifact/version DOI.
            "canonical_doi": extract_doi(row.link_cell),
            "domain": row.domain,
            "type": row.typ,
        }
    log.info(f"Parsed {len(bib)} entries from BIBLIOGRAPHY.md")
    return bib


def extract_doi(value: Any) -> str:
    if not value:
        return ""
    match = DOI_RE.search(str(value))
    if not match:
        return ""
    return match.group(0).rstrip(DOI_TRAILING)


def doi_matches(left: str, right: str) -> bool:
    """Compare DOI identifiers case-insensitively after extraction."""
    return bool(left and right and left.casefold() == right.casefold())


def canonical_doi(meta: dict[str, Any], bib_entry: dict[str, Any] | None = None) -> str:
    """Resolve the citation DOI without ever substituting an artifact DOI.

    The unified bibliography owns the public citation identifier when it has a
    DOI. Folder ``artifact_doi`` values may point to a version-specific record
    or downloadable artifact, but must never become the citation DOI merely by
    being present.
    """
    bibliography_doi = extract_doi((bib_entry or {}).get("canonical_doi") or (bib_entry or {}).get("link"))
    return bibliography_doi or extract_doi(meta.get("doi"))


def artifact_doi(meta: dict[str, Any]) -> str:
    """Return the optional per-folder artifact/version DOI only."""
    return extract_doi(meta.get("artifact_doi"))


def clean_markdown_text(value: Any) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_abstract_text(value: Any) -> str:
    text = clean_markdown_text(value)
    return re.split(r"\s---\s+Associated artifacts\b", text, maxsplit=1)[0].strip()


def truncate_display_text(text: str, limit: int = 400) -> str:
    if len(text) <= limit:
        return text
    head = text[:limit].rsplit(" ", 1)[0].rstrip(".,;:(")
    return (head or text[:limit].rstrip()) + "..."


def doi_url(doi: str, fallback_url: str | None = None) -> str:
    """Build a resolver URL, accepting a fallback only for the same DOI."""
    if not doi:
        return ""
    if fallback_url and fallback_url.startswith("http") and doi_matches(extract_doi(fallback_url), doi):
        return fallback_url
    return "https://doi.org/" + quote(doi, safe="/:")


def doi_badge(doi: str, target_url: str) -> str:
    badge_value = quote(doi, safe="")
    return f"[![DOI](https://img.shields.io/badge/DOI-{badge_value}-blue)]({target_url})"


def markdown_target(url: str) -> str:
    if url.startswith(("http://", "https://")):
        parsed = urlsplit(url)
        return urlunsplit((
            parsed.scheme,
            parsed.netloc,
            quote(parsed.path, safe="/%"),
            quote(parsed.query, safe="=&%/:?+"),
            quote(parsed.fragment, safe="=&%/:?+"),
        ))
    return quote(url, safe="/#%")


def markdown_link(label: str, url: str) -> str:
    return f"[{label}]({markdown_target(url)})" if url else label


def resolve_domain(folder: str, meta: dict, bib_entry: dict | None = None) -> str:
    """Resolve the domain name from metadata, bibliography, or inference."""
    return infer_domain_name(folder=folder, meta=meta, bib_entry=bib_entry)


def infer_domain(folder: str, meta: dict) -> str:
    """Infer research domain from folder name, tags, and keywords."""
    return infer_domain_name(folder=folder, meta=meta)


def extract_methods_from_metadata(meta: dict) -> list[str]:
    """Extract methods from metadata, falling back to inferred list."""
    methods = meta.get('methods', [])
    if methods:
        if isinstance(methods[0], dict):
            return [m.get('name', '') for m in methods if m.get('name')]
        return list(methods)
    # Generate placeholder methods based on domain
    domain = infer_domain('', meta)
    base_methods = {
        'Entomology': ['Field observation', 'Population genetics analysis', 'Behavioral assays'],
        'Active Inference': ['Free energy minimization', 'Generative modeling', 'Bayesian inference'],
        'Cognitive Security': ['Narrative analysis', 'Misinformation detection', 'Trust frameworks'],
        'Art & Synergetics': ['Visual analysis', 'Historical interpretation', 'Conceptual synthesis'],
        'Genetics & Biomedical': ['Genomic sequencing', 'Phylogenetic analysis', 'Statistical genetics'],
    }
    return base_methods.get(domain, ['Literature review', 'Theoretical analysis'])


def extract_findings_from_metadata(meta: dict) -> list[str]:
    """Extract key findings from metadata, falling back to placeholder."""
    findings = meta.get('key_findings', [])
    if findings:
        return findings
    return ['See full paper for detailed findings and analysis']


def extract_related_papers(meta: dict, all_folders: list[str]) -> list[str]:
    """Extract related paper folder names from metadata."""
    related = meta.get('related_papers', [])
    # Filter to only valid folders
    return [r for r in related if r in all_folders]


FOLDER_METADATA_FIELDS = (
    "title",
    "version",
    "doi",
    "doi_url",
    "artifact_doi",
    "artifact_doi_url",
    "zenodo_record",
    "record_id",
    "github_repo",
    "github_release_url",
    "release_tag",
    "release_name",
    "files",
    "methods",
    "key_findings",
    "related_papers",
    "related_software",
    "domain",
    "pdf_sha256",
    "pairing_confidence",
    "checked_at",
)


def paper_folders(
    *, paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS
) -> list[str]:
    """Return paper directories in a deterministic order."""
    _reject_symlink(paths.papers_dir, label="papers root")
    if not paths.papers_dir.exists():
        return []
    papers_root = _safe_papers_path(
        paths.papers_dir,
        label="papers root",
        paths=paths,
        require_directory=True,
    )
    folders: list[str] = []
    for item in papers_root.iterdir():
        if not re.fullmatch(r"\d{4}_.+", item.name):
            continue
        # Check ``is_symlink`` before ``is_dir`` because the latter follows a
        # link and would otherwise admit a folder outside the ownership root.
        _reject_symlink(item, label=f"paper folder {item.name}")
        if item.is_dir():
            _safe_paper_folder(item.name, paths=paths)
            folders.append(item.name)
    return sorted(folders)


def resolved_metadata(
    folder: str,
    metadata: dict[str, dict[str, Any]],
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> dict[str, Any]:
    """Merge consolidated and folder metadata without mutating source objects."""
    year, topic = parse_folder_id(folder)
    merged: dict[str, Any] = {"year": year, "topic": topic, "name": topic}
    merged.update(metadata.get(folder, {}))
    folder_metadata_path = _safe_paper_folder(folder, paths=paths) / "metadata.json"
    folder_metadata_text = _read_papers_text(
        folder_metadata_path,
        label=f"folder metadata {folder}/metadata.json",
        paths=paths,
    )
    if folder_metadata_text is None:
        return merged
    folder_metadata = json.loads(folder_metadata_text)
    if not isinstance(folder_metadata, dict):
        raise ValueError(f"{folder_metadata_path} must contain a metadata object")
    for field in FOLDER_METADATA_FIELDS:
        if field in folder_metadata:
            merged[field] = folder_metadata[field]
    return merged


def _invalid_doi_value(value: Any) -> bool:
    """Return whether a non-empty DOI field fails the DOI syntax extractor."""
    return bool(str(value or "").strip() and not extract_doi(value))


def build_doi_audit(
    folders: Iterable[str],
    metadata_by_folder: dict[str, dict[str, Any]],
    bibliography: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a deterministic, machine-readable canonical-versus-artifact DOI audit.

    ``doi`` is always compared to the bibliography's canonical citation DOI.
    ``artifact_doi`` is recorded for context but is intentionally excluded from
    that comparison so an artifact/version identifier cannot mask a citation
    conflict.
    """
    conflicts: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    bibliography_doi_count = 0
    metadata_doi_count = 0
    folder_list = sorted(set(folders))

    for folder in folder_list:
        meta = metadata_by_folder.get(folder, {})
        bib_entry = bibliography.get(folder)
        bibliography_doi = extract_doi((bib_entry or {}).get("canonical_doi") or (bib_entry or {}).get("link"))
        metadata_doi = extract_doi(meta.get("doi"))
        folder_artifact_doi = artifact_doi(meta)
        if bibliography_doi:
            bibliography_doi_count += 1
        if metadata_doi:
            metadata_doi_count += 1

        context = {
            "folder": folder,
            "bibliography_doi": bibliography_doi or None,
            "metadata_doi": metadata_doi or None,
            "artifact_doi": folder_artifact_doi or None,
        }
        if _invalid_doi_value(meta.get("doi")):
            conflicts.append({"code": "invalid_canonical_doi", **context})
        if _invalid_doi_value(meta.get("artifact_doi")):
            conflicts.append({"code": "invalid_artifact_doi", **context})

        metadata_doi_url = str(meta.get("doi_url") or "")
        url_doi = extract_doi(metadata_doi_url)
        if metadata_doi and url_doi and not doi_matches(metadata_doi, url_doi):
            conflicts.append({"code": "canonical_doi_url_mismatch", **context, "doi_url": metadata_doi_url})

        artifact_doi_url = str(meta.get("artifact_doi_url") or "")
        artifact_url_doi = extract_doi(artifact_doi_url)
        if artifact_doi_url and not folder_artifact_doi:
            conflicts.append({"code": "artifact_doi_url_without_artifact_doi", **context})
        elif folder_artifact_doi and artifact_url_doi and not doi_matches(folder_artifact_doi, artifact_url_doi):
            conflicts.append({"code": "artifact_doi_url_mismatch", **context, "artifact_doi_url": artifact_doi_url})

        if bibliography_doi and metadata_doi and not doi_matches(bibliography_doi, metadata_doi):
            conflicts.append({"code": "canonical_doi_mismatch", **context})
        if bibliography_doi and not metadata_doi and folder_artifact_doi:
            warnings.append({"code": "artifact_doi_not_used_as_canonical", **context})
        elif metadata_doi and folder_artifact_doi and doi_matches(metadata_doi, folder_artifact_doi):
            warnings.append({"code": "artifact_doi_duplicates_canonical", **context})

    conflicts.sort(key=lambda item: (item["folder"], item["code"]))
    warnings.sort(key=lambda item: (item["folder"], item["code"]))
    return {
        "version": 1,
        "canonical_source": "pages/BIBLIOGRAPHY.md",
        "canonical_field": "doi",
        "artifact_field": "artifact_doi",
        "summary": {
            "folders_checked": len(folder_list),
            "bibliography_dois": bibliography_doi_count,
            "metadata_dois": metadata_doi_count,
            "conflicts": len(conflicts),
            "warnings": len(warnings),
        },
        "conflicts": conflicts,
        "warnings": warnings,
    }


# ─── Generators ───────────────────────────────────────────────────────────────


def generate_readme(
    folder: str,
    meta: dict,
    bib_entry: dict | None = None,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> str:
    """Generate README.md content with enhanced structure."""
    year, topic = parse_folder_id(folder)
    title = clean_markdown_text(meta.get('name') or meta.get('title') or topic)
    authors = clean_markdown_text(meta.get('authors', 'Daniel Ari Friedman'))

    # Get abstract from description or metadata
    abstract = clean_abstract_text(meta.get('abstract', meta.get('description', f'Research paper on {topic}.')))
    # Truncate for display
    abstract_short = truncate_display_text(abstract)

    keywords = meta.get('keywords', meta.get('tags', []))
    domain = resolve_domain(folder, meta, bib_entry)
    venue = clean_markdown_text(bib_entry.get('venue', 'Zenodo') if bib_entry else 'Zenodo')

    # Methods and findings
    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)

    emoji = DOMAIN_TO_EMOJI.get(domain, '📄')

    kw_str = ' · '.join(f'`{k}`' for k in keywords[:12]) if keywords else f'`{topic}`'

    lines = [
        f'# {emoji} {title}',
        '',
        f'**{authors}** ({year}) · *{venue}*',
        '',
    ]

    doi = canonical_doi(meta, bib_entry)
    doi_target = doi_url(doi, meta.get('doi_url'))
    version_doi = artifact_doi(meta)
    version_doi_target = doi_url(version_doi, meta.get('artifact_doi_url'))
    if doi and doi_target:
        lines.append(doi_badge(doi, doi_target))
        lines.append('')

    lines.extend([
        '---',
        '',
        '## Abstract',
        '',
        f'> {abstract_short}',
        '',
        '## Keywords',
        '',
        kw_str,
        '',
        '## Methods',
        '',
    ])

    for method in methods[:6]:
        lines.append(f'- {clean_markdown_text(method)}')
    lines.append('')

    lines.extend([
        '## Key Findings',
        '',
    ])

    for finding in findings[:6]:
        lines.append(f'- {clean_markdown_text(finding)}')
    lines.append('')

    # Artifacts section
    lines.extend([
        '## Artifacts',
        '',
    ])

    # Check for associated GitHub repo
    github_repo = meta.get('github_repo')
    github_release_url = meta.get('github_release_url')
    if github_repo:
        lines.append(f'- GitHub repository: {markdown_link(github_repo, f"https://github.com/{github_repo}")}')
    if github_release_url:
        release_label = meta.get('release_tag') or meta.get('release_name') or 'Release'
        lines.append(f'- GitHub release: {markdown_link(release_label, github_release_url)}')

    # Check for DOI
    if doi and doi_target:
        lines.append(f'- DOI: {markdown_link(doi, doi_target)}')
    if version_doi and not doi_matches(version_doi, doi) and version_doi_target:
        lines.append(f'- Artifact DOI: {markdown_link(version_doi, version_doi_target)}')

    zenodo_record = meta.get('zenodo_record')
    if zenodo_record:
        lines.append(f'- Zenodo record: {markdown_link(zenodo_record, zenodo_record)}')

    local_pdfs = sorted((paths.papers_dir / folder).glob('*.pdf'))
    for pdf in local_pdfs[:3]:
        lines.append(f'- PDF: {markdown_link(pdf.name, pdf.name)}')

    for file_info in meta.get('files', [])[:3]:
        name = file_info.get('name', '')
        download_url = file_info.get('download_url', '')
        if name and download_url and name.lower().endswith('.pdf') and not any(pdf.name == name for pdf in local_pdfs):
            lines.append(f'- PDF download: {markdown_link(name, download_url)}')

    lines.extend([
        f'- PDF SHA-256: {meta.get("pdf_sha256") or (markdown_link("See Zenodo record", zenodo_record) if zenodo_record else "Not recorded")}',
        '',
        '## Citation',
        '',
        f'> {authors} ({year}). *{title}*. {venue}.'
        + (f' DOI: {doi}. URL: {doi_target}.' if doi and doi_target else ''),
        '',
        '## Related',
        '',
        '- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)',
        '- [All Papers](../README.md)',
    ])

    return '\n'.join(lines)


def generate_agents(folder: str, meta: dict, bib_entry: dict | None = None) -> str:
    """Generate AGENTS.md content with enhanced structure."""
    year, topic = parse_folder_id(folder)
    title = meta.get('name') or meta.get('title') or topic
    authors = meta.get('authors', 'Daniel Ari Friedman')
    domain = resolve_domain(folder, meta, bib_entry)
    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)

    lines = [
        f'# AGENTS.md — {title}',
        '',
        f'**Paper**: {title} ({year})',
        f'**Domain**: {domain}',
        f'**Authors**: {authors}',
        '',
        '---',
        '',
        '## Agent Roles',
        '',
        '### 📖 ARCHIVIST',
        '- Maintains bibliographic metadata and cross-references',
        f'- Tracks citation links and DOI consistency for {topic}',
        '- Updates related_papers links when new connections are identified',
        '',
        '### 🔬 RESEARCHER',
        f'- Extracts methods: {", ".join(methods[:3]) if methods else "See paper"}',
        f'- Identifies findings: {", ".join(findings[:3]) if findings else "See paper"}',
        f'- Maps contributions to {domain} literature',
        '',
        '### 🎓 EDUCATOR',
        f'- Creates learning pathways for {domain} concepts',
        '- Develops SKILL.md with executable instructions',
        '- Maintains prerequisite knowledge mapping',
        '',
        '### 🔗 INTEGRATOR',
        f'- Connects {title} to related works in the bibliography',
        '- Maps paper-to-software relationships',
        '- Updates cross-domain connections',
        '',
        '---',
        '',
        '## Extraction Log',
        '',
        '| Source | Agent | Action | Status |',
        '|--------|-------|--------|--------|',
        '| Metadata | ARCHIVIST | Cataloged metadata | ✅ |',
        '| Metadata | RESEARCHER | Extracted methods/findings | ✅ |',
        '| Metadata | EDUCATOR | Generated documentation | ✅ |',
    ]

    # Extended metadata
    if meta.get('related_papers') or meta.get('related_software'):
        lines.extend([
            '',
            '## Cross-References',
            '',
        ])
        if meta.get('related_papers'):
            lines.append('### Related Papers')
            for rp in meta['related_papers'][:8]:
                lines.append(f'- [{rp}](../{rp}/)')
            lines.append('')
        if meta.get('related_software'):
            lines.append('### Related Software')
            for rs in meta['related_software'][:4]:
                lines.append(f'- https://github.com/{rs}')
            lines.append('')

    return '\n'.join(lines)


def generate_skill(folder: str, meta: dict, all_folders: list[str] | None = None, bib_entry: dict | None = None) -> str:
    """Generate SKILL.md content with Claude Code-compatible YAML frontmatter.

    Extended version with Methods, Key Findings, Related Works, Datasets, and Validation sections.
    """
    year, topic = parse_folder_id(folder)
    title = meta.get('name') or meta.get('title') or topic
    authors = meta.get('authors', 'Daniel Ari Friedman')
    description = meta.get('description', meta.get('abstract', f'Research on {topic}')).strip()
    domain = resolve_domain(folder, meta, bib_entry)
    tags = meta.get('tags', meta.get('keywords', [topic.lower()]))
    keywords = meta.get('keywords', tags)

    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)
    related = extract_related_papers(meta, all_folders or [])

    # Format tags
    if isinstance(tags, list) and tags:
        tags_yaml = json.dumps([t.lower().replace(' ', '-') for t in tags[:10]])
    else:
        tags_yaml = f'["{topic.lower()}"]'

    # Truncate description for frontmatter (must be single-line for YAML)
    desc_clean = ' '.join(description.split())  # Normalize whitespace
    desc_short = desc_clean[:250] + '...' if len(desc_clean) > 250 else desc_clean

    # The bibliography owns the citation DOI; a version/download DOI remains
    # explicitly labeled as an artifact and is never used for citation text.
    doi = canonical_doi(meta, bib_entry)
    version_doi = artifact_doi(meta)
    citation = f'{authors} ({year}). *{title}*. {domain}.'

    lines = [
        '---',
        f'name: "{title}"',
        f'description: "{desc_short}"',
        f'tags: {tags_yaml}',
        f'domain: "{domain}"',
        f'citation: "{citation}"',
    ]

    if doi:
        lines.append(f'doi: "{doi}"')
    if version_doi and not doi_matches(version_doi, doi):
        lines.append(f'artifact_doi: "{version_doi}"')

    lines.extend([
        '---',
        '',
        f'# {title}',
        '',
        f'**{authors}** ({year}) · {domain}',
        '',
        '## Context',
        '',
        f'This work addresses topics in **{domain}**: {", ".join(keywords[:4]) if keywords else topic}.',
        '',
    ])

    # Methods section
    lines.extend([
        '## Methods',
        '',
        'Primary methods and techniques applied in this work:',
        '',
    ])
    for method in methods[:6]:
        lines.append(f'- {method}')
    lines.append('')

    # Key Findings section
    lines.extend([
        '## Key Findings',
        '',
        'Core contributions and results:',
        '',
    ])
    for finding in findings[:6]:
        lines.append(f'- {finding}')
    lines.append('')

    # Datasets section
    dataset_refs = meta.get('dataset_references', [])
    if dataset_refs:
        lines.extend([
            '## Datasets',
            '',
            'Referenced datasets:',
            '',
        ])
        for ds in dataset_refs[:6]:
            lines.append(f'- {ds}')
        lines.append('')

    # Related Works section
    lines.extend([
        '## Related Works',
        '',
    ])
    for rp in related[:6]:
        lines.append(f'- [{rp}](../{rp}/)')
    if not related:
        lines.append('See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.')
    lines.append('')

    # Validation section
    lines.extend([
        '## Validation',
        '',
        'Verification points for this work:',
        '',
        f'- Canonical DOI: {doi if doi else "Not assigned"}',
        f'- PDF SHA-256: {meta.get("pdf_sha256") or "See zenodo_record"}',
        f'- Pairing confidence: {meta.get("pairing_confidence") or "unknown"}',
        f'- Last checked: {meta.get("checked_at") or "unknown"}',
        '',
    ])

    if version_doi and not doi_matches(version_doi, doi):
        lines.insert(-1, f'- Artifact DOI: {version_doi}')

    # Prerequisites
    lines.extend([
        '## Prerequisites',
        '',
        f'- Familiarity with {", ".join(keywords[:3]) if keywords else topic}',
        f'- Background in {domain} fundamentals',
        f'- Access to source repository: {meta.get("github_repo") or "N/A"}',
        '',
        '## Instructions',
        '',
        'When working with this paper:',
        '',
        f'1. Reference the DOI for citation: `{doi}`' if doi else '1. Use the canonical citation above.',
        '2. Apply methods listed in the Methods section for related analysis.',
        '3. Validate findings against the original PDF and metadata.',
        '',
    ])

    return '\n'.join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────


def render_document(
    folder: str,
    filename: str,
    meta: dict[str, Any],
    all_folders: list[str],
    bib_entry: dict[str, Any] | None,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> str:
    """Render one managed document, including its stable ownership marker."""
    _safe_paper_folder(folder, paths=paths)
    if filename == "README.md":
        content = generate_readme(folder, meta, bib_entry, paths=paths)
    elif filename == "AGENTS.md":
        content = generate_agents(folder, meta, bib_entry)
    elif filename == "SKILL.md":
        content = generate_skill(folder, meta, all_folders, bib_entry)
    else:
        raise ValueError(f"unsupported generated document: {filename}")
    return wrap_generated_document(filename, content)


def plan_document_changes(
    folders: list[str],
    metadata_by_folder: dict[str, dict[str, Any]],
    bibliography: dict[str, dict[str, Any]],
    manifest_entries: dict[str, ManifestEntry],
    *,
    adopt_existing: bool,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> tuple[list[DocumentChange], list[str], int]:
    """Plan changes without writing, respecting explicit ownership boundaries."""
    changes: list[DocumentChange] = []
    errors: list[str] = []
    skipped = 0
    seen_manifest_paths: set[str] = set()

    for folder in folders:
        # Validate the folder before metadata-derived rendering reads local PDFs
        # and validate every supported target before inspecting its ownership.
        # This keeps both --check and --apply inside the explicit papers root.
        _safe_paper_folder(folder, paths=paths)
        meta = metadata_by_folder[folder]
        bib_entry = bibliography.get(folder)
        for filename in DOCUMENT_FILENAMES:
            key = generated_document_key(folder, filename)
            path = _safe_managed_document_path(folder, filename, paths=paths)
            entry = manifest_entries.get(key)
            expected = render_document(folder, filename, meta, folders, bib_entry, paths=paths)
            current = _read_papers_text(
                path,
                label=f"managed document {key}",
                paths=paths,
                require_unique_link=True,
            )

            if entry:
                seen_manifest_paths.add(key)
                if entry.adopt:
                    if not adopt_existing:
                        errors.append(
                            f"{key}: manifest entry awaits explicit --adopt-existing --apply"
                        )
                    elif current is None:
                        errors.append(f"{key}: cannot adopt a missing document")
                    else:
                        changes.append(DocumentChange(path, key, expected, "adopt"))
                    continue
                if current is None:
                    changes.append(DocumentChange(path, key, expected, "create"))
                elif current != expected:
                    changes.append(DocumentChange(path, key, expected, "update"))
                continue

            if current is None:
                # A new folder has no hand-authored content to preserve; record
                # ownership at creation so future checks can detect drift.
                changes.append(DocumentChange(path, key, expected, "create"))
                continue

            if is_generated_document(filename, current):
                errors.append(
                    f"{key}: generated marker is present but the document is not in {MANIFEST_FILENAME}"
                )
            else:
                # Existing unlisted material is intentionally considered human
                # authored, regardless of size or resemblance to a template.
                skipped += 1

    for key in sorted(set(manifest_entries) - seen_manifest_paths):
        errors.append(f"{key}: manifest entry does not map to a current paper folder")

    if adopt_existing and not any(entry.adopt for entry in manifest_entries.values()):
        errors.append("--adopt-existing requires at least one manifest entry with adopt: true")
    return changes, errors, skipped


def final_manifest_entries(
    entries: dict[str, ManifestEntry], changes: Iterable[DocumentChange]
) -> dict[str, ManifestEntry]:
    """Return the manifest state after successfully applying planned changes."""
    final_entries = dict(entries)
    for change in changes:
        final_entries[change.key] = ManifestEntry(path=change.key)
    return final_entries


def _log_doi_audit(audit: dict[str, Any]) -> None:
    """Log human-readable DOI failures while keeping --doi-audit stdout as JSON."""
    for conflict in audit["conflicts"]:
        log.error(
            "DOI audit %s for %s (bibliography=%s, metadata=%s, artifact=%s)",
            conflict["code"],
            conflict["folder"],
            conflict.get("bibliography_doi") or "—",
            conflict.get("metadata_doi") or "—",
            conflict.get("artifact_doi") or "—",
        )
    for warning in audit["warnings"]:
        log.warning(
            "DOI audit %s for %s (bibliography=%s, metadata=%s, artifact=%s)",
            warning["code"],
            warning["folder"],
            warning.get("bibliography_doi") or "—",
            warning.get("metadata_doi") or "—",
            warning.get("artifact_doi") or "—",
        )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the CLI parser without performing filesystem writes."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write only owned or newly created documents")
    mode.add_argument("--check", action="store_true", help="fail when managed documents or DOI roles drift")
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help="adopt only explicit manifest entries marked adopt: true (requires --apply)",
    )
    parser.add_argument(
        "--doi-audit",
        action="store_true",
        help="emit the deterministic canonical-versus-artifact DOI audit as JSON on stdout",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help=f"generated-document ownership manifest (default: papers/{MANIFEST_FILENAME})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="deprecated compatibility flag; it never overrides explicit document ownership",
    )
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    paths: DocumentPaths = DEFAULT_DOCUMENT_PATHS,
) -> int:
    """Run the generator and return a process-compatible status code."""
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    if args.adopt_existing and not args.apply:
        parser.error("--adopt-existing requires --apply")

    configure_logging()
    if args.force:
        log.warning("--force is deprecated and does not override the generated-document ownership manifest")

    try:
        metadata = load_metadata(paths=paths)
        bibliography = parse_bibliography(paths=paths)
        folders = paper_folders(paths=paths)
        metadata_by_folder = {
            folder: resolved_metadata(folder, metadata, paths=paths)
            for folder in folders
        }
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        log.error("unable to load paper-document sources: %s", exc)
        return 2

    log.info("Found %s paper folders, %s metadata entries", len(folders), len(metadata))
    audit = build_doi_audit(folders, metadata_by_folder, bibliography)
    if args.doi_audit:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
    _log_doi_audit(audit)

    # A standalone audit is intentionally no-write and does not require a
    # document manifest; it remains useful while an audited migration is being
    # prepared.
    if args.doi_audit and not args.apply and not args.check:
        return 1 if audit["conflicts"] else 0

    try:
        manifest_path = _safe_manifest_path(
            args.manifest or generated_documents_manifest_path(paths=paths),
            paths=paths,
        )
        manifest_entries = load_generated_documents_manifest(manifest_path, paths=paths)
        changes, document_errors, skipped = plan_document_changes(
            folders,
            metadata_by_folder,
            bibliography,
            manifest_entries,
            adopt_existing=args.adopt_existing,
            paths=paths,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        log.error("unable to plan paper-document generation: %s", exc)
        return 2

    if audit["conflicts"]:
        document_errors.append("canonical DOI audit has conflicts; reconcile source metadata before rendering documents")

    # Ownership is a source-controlled contract, not merely parsed JSON.  A
    # semantically equivalent but differently serialized manifest can conceal
    # an out-of-band edit from a structural-only check, so compare the exact
    # deterministic bytes that --apply would write.  A missing manifest remains
    # acceptable only when no documents are generator-owned; this preserves the
    # safe no-op behavior for entirely hand-authored paper folders.
    final_entries = final_manifest_entries(manifest_entries, changes)
    rendered_manifest = render_generated_documents_manifest(final_entries.values())
    try:
        current_manifest = _read_papers_text(
            _safe_manifest_path(manifest_path, paths=paths),
            label="generated-document manifest",
            paths=paths,
            require_unique_link=True,
        )
    except (OSError, ValueError) as exc:
        log.error("unable to validate generated-document manifest before rendering: %s", exc)
        return 2
    manifest_is_required = current_manifest is not None or bool(final_entries)
    manifest_is_stale = manifest_is_required and current_manifest != rendered_manifest

    if args.check:
        for change in changes:
            state = "missing" if change.action == "create" else "stale"
            document_errors.append(f"{change.key}: {state} generated document")
        if manifest_is_stale:
            document_errors.append(f"{manifest_path}: stale generated-document manifest")
        for error in document_errors:
            log.error("%s", error)
        if document_errors:
            log.error("paper-document check failed: %s issue(s)", len(document_errors))
            return 1
        log.info("paper-document check passed: managed documents are current; unmanaged existing documents=%s", skipped)
        return 0

    if document_errors:
        for error in document_errors:
            log.error("%s", error)
        log.error("refusing to write paper documents with %s blocking issue(s)", len(document_errors))
        return 1

    created = sum(change.action == "create" for change in changes)
    updated = sum(change.action == "update" for change in changes)
    adopted = sum(change.action == "adopt" for change in changes)
    if not args.apply:
        for change in changes:
            log.info("WOULD %s: %s", change.action.upper(), change.key)
        log.info(
            "dry run: create=%s update=%s adopt=%s unmanaged-existing=%s",
            created,
            updated,
            adopted,
            skipped,
        )
        return 0

    try:
        # Revalidate the target set immediately before the write phase.  This
        # also prevents a link introduced after planning from redirecting a
        # managed write outside the papers root.
        validated_changes = [
            (
                change,
                _safe_managed_document_path(
                    *change.key.split("/", maxsplit=1),
                    paths=paths,
                ),
            )
            for change in changes
        ]
        for change, path in validated_changes:
            if path != change.path:
                raise ValueError(f"managed document path changed while planning: {change.key}")
            _write_papers_text(
                path,
                change.content,
                label=f"managed document {change.key}",
                paths=paths,
                require_unique_link=True,
            )
            log.info("%s: %s", change.action.upper(), change.key)

        if manifest_is_stale:
            write_generated_documents_manifest(
                manifest_path,
                final_entries.values(),
                paths=paths,
            )
            log.info("UPDATED: %s", manifest_path)
    except (OSError, ValueError) as exc:
        log.error("refusing unsafe paper-document write: %s", exc)
        return 2
    log.info(
        "applied: create=%s update=%s adopt=%s unmanaged-existing=%s",
        created,
        updated,
        adopted,
        skipped,
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
