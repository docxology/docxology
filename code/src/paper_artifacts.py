"""Resolve public paper artifacts without guessing editions or following symlinks.

Git-visible, non-ignored intake files are eligible for local previews; publication
still commits those files before assembling the tracked-only Pages projection.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, replace
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docxology_tools.scholar_pdf_projection import ProjectedPDF
from urllib.parse import quote

SITE_URL = "https://danielarifriedman.com/"
GITHUB_TREE = "https://github.com/docxology/docxology/tree/main/"


class SourcePaths(frozenset[str]):
    """One Git visibility snapshot, indexed once by canonical paper folder.

    Only names are indexed. Each artifact's current file/link checks still run
    when loading resources, and a new Git snapshot gets a new index.
    """

    def __new__(cls, paths):
        instance = super().__new__(cls, paths)
        grouped = {}
        for name in sorted(instance):
            parts = name.split("/", 2)
            if len(parts) == 3 and parts[0] == "papers":
                grouped.setdefault("/".join(parts[:2]), []).append(name)
        instance._paper_paths = MappingProxyType(
            {k: tuple(v) for k, v in grouped.items()}
        )
        return instance

    def paper_paths(self, folder: str) -> tuple[str, ...]:
        return self._paper_paths.get(folder, ())


def source_paths(repo_root: Path) -> SourcePaths:
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        timeout=15,
        stdin=subprocess.DEVNULL,
    )
    return SourcePaths(
        name for name in result.stdout.decode("utf-8").split("\0") if name
    )


def encoded_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in PurePosixPath(path).parts)


def source_file(
    repo_root: Path, relative_path: str, visible_paths: frozenset[str] | None = None
) -> Path | None:
    """A regular public source file; authoritative reads must reject symlinks."""
    root = repo_root.resolve()
    rel = PurePosixPath(relative_path)
    if (
        rel.is_absolute()
        or not rel.parts
        or any(part in {".", ".."} for part in rel.parts)
        or "\\" in relative_path
    ):
        raise ValueError(f"Invalid public source path: {relative_path!r}")
    if any(
        (root / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)
    ):
        raise ValueError(f"Symlinked public source: {relative_path!r}")
    path = root / Path(*rel.parts)
    if not path.is_file():
        return None
    if path.stat().st_nlink != 1:
        raise ValueError(f"Hardlinked public source: {relative_path!r}")
    visible = source_paths(root) if visible_paths is None else visible_paths
    return path if rel.as_posix() in visible else None


def read_source_text(
    path: Path, *, limit: int, reader: Callable[..., str] | None = None
) -> str:
    """Read eligible source text strictly and within its byte boundary.

    Callers still own current source eligibility checks. A supplied reader may
    reuse a version-aware text observation, but cannot waive the byte/type gate.
    """
    if path.stat().st_size > limit:
        raise ValueError(f"Oversized public source input: {path}")
    if reader is None:
        with path.open("rb") as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ValueError(f"Oversized public source input: {path}")
        text = raw.decode("utf-8")
    else:
        text = reader(path, limit=limit)
    if not isinstance(text, str):
        raise TypeError("Public source reader must return text")
    if len(text.encode("utf-8")) > limit:
        raise ValueError(f"Oversized public source input: {path}")
    return text


@dataclass(frozen=True)
class RemotePrimaryPDF:
    """An explicitly reviewed edition hosted at one exact Zenodo record."""

    name: str
    url: str
    version: str
    record_id: str
    bytes: int
    sha256: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.name, str)
            or not self.name.lower().endswith(".pdf")
            or "/" in self.name
            or "\\" in self.name
            or re.search(r"[\x00-\x1f\x7f]", self.name)
            or not isinstance(self.version, str)
            or not self.version.strip()
            or re.search(r"[\x00-\x1f\x7f]", self.version)
            or not isinstance(self.record_id, str)
            or not re.fullmatch(r"[1-9][0-9]*", self.record_id)
            or isinstance(self.bytes, bool)
            or not isinstance(self.bytes, int)
            or self.bytes <= 0
            or not isinstance(self.sha256, str)
            or not re.fullmatch(r"[0-9a-fA-F]{64}", self.sha256)
        ):
            raise ValueError("Invalid remote primary PDF identity or integrity metadata")
        encoded = quote(self.name, safe="")
        permitted = {
            f"https://zenodo.org/records/{self.record_id}/files/{encoded}",
            f"https://zenodo.org/api/records/{self.record_id}/files/{encoded}/content",
        }
        if not isinstance(self.url, str) or self.url not in permitted:
            raise ValueError("Remote primary PDF requires its exact versioned Zenodo URL")

    @classmethod
    def from_value(cls, value: object) -> RemotePrimaryPDF:
        fields = ("name", "url", "version", "record_id", "bytes", "sha256")
        if not isinstance(value, dict) or not all(key in value for key in fields):
            raise ValueError("Remote primary PDF declaration requires all edition fields")
        return cls(**{key: value[key] for key in fields})


@dataclass(frozen=True)
class PaperResources:
    repo_root: Path
    docs_path: str = ""
    folder: Path | None = None
    metadata: dict | None = None
    files: tuple[Path, ...] = ()
    pdfs: tuple[Path, ...] = ()
    primary_pdf: Path | None = None
    primary_basis: str = ""
    selection_issue: str = ""
    extraction_source: str = ""
    remote_primary_pdf: RemotePrimaryPDF | None = None
    scholar_pdf: ProjectedPDF | None = None

    @classmethod
    def load(
        cls,
        repo_root: Path,
        docs_path: str,
        visible_paths: frozenset[str] | None = None,
        *,
        read_text: Callable[..., str] | None = None,
    ) -> PaperResources:
        resources = cls._load(repo_root, docs_path, visible_paths, read_text=read_text)
        from docxology_tools.scholar_pdf_projection import projection_for_resources

        projection = projection_for_resources(resources, visible_paths, read_text=read_text)
        return replace(resources, scholar_pdf=projection) if projection else resources

    @classmethod
    def _load(
        cls,
        repo_root: Path,
        docs_path: str,
        visible_paths: frozenset[str] | None = None,
        *,
        read_text: Callable[..., str] | None = None,
    ) -> PaperResources:
        root = repo_root.resolve()
        if not docs_path:
            return cls(root)
        # Accept exactly one canonical paper folder, with an optional final slash.
        clean = docs_path.rstrip("/")
        if not re.fullmatch(r"papers/\d{4}_[^/\\]+", clean) or "\0" in clean:
            raise ValueError(f"Invalid paper-folder path: {docs_path!r}")
        folder = root / clean
        if any(p.is_symlink() for p in (root / "papers", folder)):
            raise ValueError(f"Symlinked paper-folder path: {docs_path!r}")
        if not folder.is_dir():
            return cls(root)
        visible = source_paths(root) if visible_paths is None else visible_paths
        files = []
        candidates = (
            visible.paper_paths(clean)
            if isinstance(visible, SourcePaths)
            else sorted(visible)
        )
        for name in candidates:
            if not name.startswith(clean + "/"):
                continue
            rel = PurePosixPath(name)
            if rel.is_absolute() or any(part in {".", ".."} for part in rel.parts):
                continue
            path = root / name
            # Reject every symlink ancestor, including image subdirectories.
            if any(
                (root / Path(*rel.parts[:i])).is_symlink()
                for i in range(1, len(rel.parts) + 1)
            ):
                continue
            if path.is_file():
                if path.stat().st_nlink != 1:
                    raise ValueError(f"Hardlinked paper source: {name!r}")
                files.append(path)
        if not files:
            return cls(root)
        meta_path = folder / "metadata.json"
        meta = (
            json.loads(read_source_text(meta_path, limit=32 * 1024 * 1024, reader=read_text))
            if meta_path in files
            else {}
        )
        if not isinstance(meta, dict):
            raise ValueError(f"Paper metadata must be an object: {meta_path}")
        pdfs = tuple(
            path
            for path in files
            if path.parent == folder and path.suffix.lower() == ".pdf"
        )
        primary = None
        basis = issue = extracted = ""
        full_text = folder / "full_text.md"
        if full_text in files:
            with full_text.open(encoding="utf-8") as stream:
                header = stream.read(4096)
            match = re.search(r"^> Extracted from `([^`\n]+)`\s*$", header, re.M)
            extracted = match.group(1) if match else ""
        if explicit := meta.get("primary_pdf"):
            primary = next((p for p in pdfs if p.name == explicit), None)
            if primary is None:
                raise ValueError(f"Unavailable primary_pdf {explicit!r} in {clean}")
            basis = "declared primary"
            if extracted and extracted != primary.name:
                issue = f"The extracted text comes from {extracted}, while the declared primary PDF is {primary.name}."
        elif extracted:
            primary = next((p for p in pdfs if p.name == extracted), None)
            if primary:
                basis = "extracted-text source"
            elif pdfs:
                issue = (
                    "The extracted text names a PDF that is unavailable in this folder."
                )
        elif len(pdfs) == 1:
            primary, basis = pdfs[0], "only archived PDF"
        remote = None
        if meta.get("remote_primary_pdf") is not None:
            remote = RemotePrimaryPDF.from_value(meta["remote_primary_pdf"])
            primary = None
            basis = "declared remote edition"
            issue = f"Current PDF version {remote.version} is hosted at Zenodo."
            if pdfs:
                issue += " Local PDFs remain preserved historical archives."
            if full_text in files:
                issue += (
                    " Extracted text retains its own source provenance;"
                    " a matching filename does not establish edition identity."
                )
        return cls(
            root,
            clean + "/",
            folder,
            meta,
            tuple(files),
            pdfs,
            primary,
            basis,
            issue,
            extracted,
            remote,
        )

    def file(self, name: str) -> Path | None:
        if self.folder is None:
            return None
        path = self.folder / name
        return path if path in self.files else None

    @property
    def readme(self) -> Path | None:
        return self.file("README.md")

    @property
    def skill(self) -> Path | None:
        return self.file("SKILL.md")

    @property
    def full_text(self) -> Path | None:
        return self.file("full_text.md")

    @property
    def primary_pdf_url(self) -> str:
        if self.remote_primary_pdf:
            return self.remote_primary_pdf.url
        if self.scholar_pdf:
            return self.scholar_pdf.url
        return self.absolute_url(self.primary_pdf) if self.primary_pdf else ""

    @property
    def images(self) -> tuple[Path, ...]:
        return (
            tuple(
                p
                for p in self.files
                if p.parent == self.folder / "images"
                and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}
            )
            if self.folder
            else ()
        )

    @property
    def historical_image_source(self) -> dict[str, str] | None:
        """Resolve only an explicitly bound historical gallery, without guessing."""
        evidence = self.file("source_evidence.json")
        if not self.images or evidence is None:
            return None
        with evidence.open("rb") as stream:
            raw = stream.read(65537)
        if len(raw) > 65536:
            raise ValueError("Historical image evidence exceeds its bounded reader")
        payload = json.loads(raw)
        if not isinstance(payload, dict) or not isinstance(payload.get("historical_sources", []), list):
            raise ValueError("Invalid historical image evidence")
        bindings = [
            entry for entry in payload.get("historical_sources", [])
            if isinstance(entry, dict) and "images" in entry
        ]
        if not bindings:
            return None
        if len(bindings) != 1 or bindings[0]["images"] != "images/":
            raise ValueError("Historical image archive requires one exact images/ binding")
        source = bindings[0]
        for field, suffix in (("file", ".md"), ("source_pdf", ".pdf")):
            name = source.get(field)
            if (
                not isinstance(name, str) or not name.lower().endswith(suffix)
                or "/" in name or "\\" in name or re.search(r"[\x00-\x1f\x7f]", name)
            ):
                raise ValueError("Historical image source requires plain document filenames")
        edition, digest = source.get("edition"), source.get("sha256")
        if (
            not isinstance(edition, str) or not edition.strip()
            or re.search(r"[\x00-\x1f\x7f]", edition)
            or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest)
        ):
            raise ValueError("Historical image source requires an edition and extraction SHA-256")
        extraction = self.file(source["file"])
        if extraction is None:
            raise ValueError("Historical image extraction is unavailable")
        with extraction.open("rb") as stream:
            text = stream.read(32 * 1024 * 1024 + 1)
        if len(text) > 32 * 1024 * 1024 or hashlib.sha256(text).hexdigest() != digest.casefold():
            raise ValueError("Historical image extraction no longer matches its SHA-256")
        return {key: source[key] for key in ("file", "source_pdf", "edition")}

    @property
    def github_url(self) -> str:
        return (
            GITHUB_TREE + encoded_path(self.docs_path.rstrip("/"))
            if self.folder
            else ""
        )

    def url(self, path: Path, prefix: str = "../") -> str:
        if path not in self.files:
            raise ValueError("Only eligible paper files can be linked")
        return prefix + encoded_path(path.relative_to(self.repo_root).as_posix())

    def absolute_url(self, path: Path) -> str:
        return self.url(path, SITE_URL)

    @property
    def docs_url(self) -> str:
        return (
            "../" + encoded_path(self.docs_path.rstrip("/")) + "/"
            if self.folder
            else ""
        )

    @property
    def archive_documents(self) -> tuple[dict, ...]:
        """Reviewed supporting source downloads, separate from hosted PDFs."""
        from docxology_tools.archive_projection import declared_archives

        return tuple(
            item
            for name, item in declared_archives(self.repo_root).items()
            if str(Path(name).parent) + "/" == self.docs_path
        )
