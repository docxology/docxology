"""Resolve public paper artifacts without guessing editions or following symlinks.

Git-visible, non-ignored intake files are eligible for local previews; publication
still commits those files before assembling the tracked-only Pages projection.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import quote

SITE_URL = "https://danielarifriedman.com/"
GITHUB_TREE = "https://github.com/docxology/docxology/tree/main/"


def source_paths(repo_root: Path) -> frozenset[str]:
    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=repo_root, check=True, capture_output=True,
    )
    return frozenset(result.stdout.decode("utf-8").split("\0")) - {""}


def encoded_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in PurePosixPath(path).parts)


def source_file(repo_root: Path, relative_path: str, visible_paths: frozenset[str] | None = None) -> Path | None:
    """A regular public source file; authoritative reads must reject symlinks."""
    root = repo_root.resolve()
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(part in {".", ".."} for part in rel.parts) or "\\" in relative_path:
        raise ValueError(f"Invalid public source path: {relative_path!r}")
    if any((root / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
        raise ValueError(f"Symlinked public source: {relative_path!r}")
    path = root / Path(*rel.parts)
    if not path.is_file():
        return None
    if path.stat().st_nlink != 1:
        raise ValueError(f"Hardlinked public source: {relative_path!r}")
    visible = source_paths(root) if visible_paths is None else visible_paths
    return path if rel.as_posix() in visible else None


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

    @classmethod
    def load(
        cls, repo_root: Path, docs_path: str,
        visible_paths: frozenset[str] | None = None,
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
        for name in sorted(visible):
            if not name.startswith(clean + "/"):
                continue
            rel = PurePosixPath(name)
            if rel.is_absolute() or any(part in {".", ".."} for part in rel.parts):
                continue
            path = root / name
            # Reject every symlink ancestor, including image subdirectories.
            if any((root / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts) + 1)):
                continue
            if path.is_file():
                if path.stat().st_nlink != 1:
                    raise ValueError(f"Hardlinked paper source: {name!r}")
                files.append(path)
        if not files:
            return cls(root)
        meta_path = folder / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path in files else {}
        if not isinstance(meta, dict):
            raise ValueError(f"Paper metadata must be an object: {meta_path}")
        pdfs = tuple(path for path in files if path.parent == folder and path.suffix.lower() == ".pdf")
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
                issue = "The extracted text names a PDF that is unavailable in this folder."
        elif len(pdfs) == 1:
            primary, basis = pdfs[0], "only archived PDF"
        return cls(root, clean + "/", folder, meta, tuple(files), pdfs, primary, basis, issue, extracted)

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
    def images(self) -> tuple[Path, ...]:
        return tuple(p for p in self.files if p.parent == self.folder / "images" and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}) if self.folder else ()

    @property
    def github_url(self) -> str:
        return GITHUB_TREE + encoded_path(self.docs_path.rstrip("/")) if self.folder else ""

    def url(self, path: Path, prefix: str = "../") -> str:
        if path not in self.files:
            raise ValueError("Only eligible paper files can be linked")
        return prefix + encoded_path(path.relative_to(self.repo_root).as_posix())

    def absolute_url(self, path: Path) -> str:
        return self.url(path, SITE_URL)

    @property
    def docs_url(self) -> str:
        return "../" + encoded_path(self.docs_path.rstrip("/")) + "/" if self.folder else ""
