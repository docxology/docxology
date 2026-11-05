"""Reviewed, immutable PDF web routes; never a Scholar indexing attestation.

Reservations retain original custody and rights evidence. Current associations
may retire without removing an already published, byte-identical web alias.
No PDF bytes are written into the repository by this policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit

from docxology_tools.biblio_table import iter_bibliography_rows
from docxology_tools.bibliography_links import canonical_link_url
from docxology_tools.citation_metadata import publication_date
from docxology_tools.paper_artifacts import SITE_URL, read_source_text, source_file, source_paths
from docxology_tools.work_identifiers import validate_catalog, validate_registry

REGISTRY = "data/scholar-pdf-projections.json"
SCHEMA_VERSION = "ScholarPDFProjectionRegistry.v1"
PILOT_BYTE_LIMIT = 5 * 1024 * 1024
PDF_BYTE_LIMIT = 5_000_000
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_KEY = re.compile(r"[A-Za-z][A-Za-z0-9]{0,199}\Z")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate Scholar projection property: {key}")
        result[key] = value
    return result


def _json(root: Path, name: str, visible, *, limit=32 * 1024 * 1024, read_text=None):
    path = source_file(root, name, visible)
    if path is None:
        raise ValueError(f"Missing public Scholar projection input: {name}")
    return json.loads(
        read_source_text(path, limit=limit, reader=read_text), object_pairs_hook=_object
    )


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or "\0" in value:
        raise ValueError(f"Scholar projection requires {label}")
    return value


def _digest(value):
    if not isinstance(value, str) or not _DIGEST.fullmatch(value):
        raise ValueError("Scholar projection requires an exact lowercase SHA-256")
    return value


def _path(value):
    if (
        not isinstance(value, str)
        or "\\" in value
        or re.search(r"[\x00-\x1f\x7f]", value)
        or value != PurePosixPath(value).as_posix()
    ):
        raise ValueError("Noncanonical Scholar projection path")
    parsed = PurePosixPath(value)
    if (
        parsed.is_absolute()
        or not parsed.parts
        or any(p in {".", ".."} for p in parsed.parts)
    ):
        raise ValueError("Unsafe Scholar projection path")
    return value


def declared_projections(root: Path, visible=None, *, read_text=None) -> dict:
    root = root.resolve()
    visible = source_paths(root) if visible is None else visible
    path = source_file(root, REGISTRY, visible)
    if path is None:
        if (root / REGISTRY).exists() or source_file(
            root, "data/work-identifiers.json", visible
        ):
            raise ValueError(
                "Managed site is missing its Scholar PDF reservation registry"
            )
        return {"schema_version": SCHEMA_VERSION, "reservations": [], "selections": {}}
    payload = _json(root, REGISTRY, visible, limit=256 * 1024, read_text=read_text)
    if (
        not isinstance(payload, dict)
        or set(payload) != {"schema_version", "reservations", "selections"}
        or payload["schema_version"] != SCHEMA_VERSION
        or not isinstance(payload["reservations"], list)
        or len(payload["reservations"]) > 64
        or not isinstance(payload["selections"], dict)
    ):
        raise ValueError("Invalid reviewed Scholar PDF projection registry")
    seen, owners, total = {}, {}, 0
    for record in payload["reservations"]:
        if not isinstance(record, dict):
            raise ValueError("Scholar reservation must be an object")
        digest = _digest(record.get("sha256"))
        key = record.get("citation_key")
        if (
            not isinstance(key, str)
            or not _KEY.fullmatch(key)
            or type(record.get("num")) is not int
            or record["num"] <= 0
        ):
            raise ValueError("Invalid Scholar work identity")
        if key in owners and owners[key] != record["num"]:
            raise ValueError("Scholar work identity changed between reservations")
        owners[key] = record["num"]
        folder = record.get("docs_path")
        if not isinstance(folder, str) or not re.fullmatch(
            r"papers/[0-9]{4}_[^/\\\x00-\x1f]+/", folder
        ):
            raise ValueError("Invalid Scholar paper folder")
        source = _path(record.get("source_pdf"))
        if (
            str(PurePosixPath(source).parent) + "/" != folder
            or PurePosixPath(source).suffix.lower() != ".pdf"
        ):
            raise ValueError(
                "Scholar PDF must be a direct source in its reviewed paper folder"
            )
        if record.get("alias") != f"works/{digest}.pdf" or digest in seen:
            raise ValueError("Duplicate or changed Scholar PDF alias reservation")
        seen[digest] = record
        if (
            type(record.get("bytes")) is not int
            or not 0 < record["bytes"] <= PDF_BYTE_LIMIT
        ):
            raise ValueError("Scholar PDF exceeds its exact individual byte limit")
        total += record["bytes"]
        _text(record.get("doi"), "DOI")
        _text(record.get("title"), "title")
        if (
            not isinstance(record.get("authors"), list)
            or not record["authors"]
            or not all(isinstance(a, str) and a.strip() for a in record["authors"])
        ):
            raise ValueError("Scholar projection requires the reviewed ordered byline")
        date.fromisoformat(_text(record.get("publication_date"), "publication date"))
        review = record.get("review")
        if not isinstance(review, dict):
            raise ValueError(
                "Scholar projection requires independent content and rights review"
            )
        date.fromisoformat(_text(review.get("reviewed_at"), "review date"))
        _text(review.get("reviewed_by"), "attributed review")
        rights = review.get("rights", {})
        if not isinstance(rights, dict):
            raise ValueError("Scholar rights review must be an object")
        allowed = {
            "CC BY": "https://creativecommons.org/licenses/by/",
            "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
        }
        if (
            rights.get("license") not in allowed
            or rights.get("license_url") != allowed[rights["license"]]
        ):
            raise ValueError(
                "Scholar projection lacks reviewed CC BY redistribution rights"
            )
        if type(rights.get("evidence_page")) is not int or rights["evidence_page"] < 1:
            raise ValueError("Scholar rights evidence requires an exact PDF page")
        _text(rights.get("evidence"), "PDF license evidence")
        _text(rights.get("conditions"), "attribution and credit-line conditions")
        searchable = review.get("searchability", {})
        if not isinstance(searchable, dict):
            raise ValueError("Scholar searchability review must be an object")
        if searchable.get("nonblank_first_two_pages") is not True:
            raise ValueError("Scholar PDF searchability was not reviewed")
        _text(searchable.get("method"), "searchability review method")
        _digest(searchable.get("first_page_text_sha256"))
        scholarly = review.get("scholarly_content", {})
        if not isinstance(scholarly, dict):
            raise ValueError("Scholar content review must be an object")
        if scholarly.get("kind") != "journal-article":
            raise ValueError("Scholar pilot is restricted to reviewed journal articles")
        _text(scholarly.get("basis"), "scholarly-content evidence")
        abstract = review.get("abstract", {})
        if not isinstance(abstract, dict):
            raise ValueError("Scholar abstract review must be an object")
        if (
            abstract.get("source") != "papers/paper_metadata.json"
            or abstract.get("complete_author_written") is not True
        ):
            raise ValueError(
                "Scholar pilot requires a reviewed complete author-written abstract"
            )
        _digest(abstract.get("sha256"))
        _text(abstract.get("method"), "complete-abstract review method")
    if total > PILOT_BYTE_LIMIT:
        raise ValueError(
            "Scholar PDF reservations exceed the unchanged 5 MiB pilot cap"
        )
    selected = set()
    for key, digest in payload["selections"].items():
        _digest(digest)
        if (
            not isinstance(key, str)
            or not _KEY.fullmatch(key)
            or digest not in seen
            or seen[digest]["citation_key"] != key
            or key.casefold() in selected
        ):
            raise ValueError(
                "Scholar current association has no matching reserved source"
            )
        selected.add(key.casefold())
    aliases = {item["alias"].casefold() for item in seen.values()}
    if any(name.casefold() in aliases for name in visible):
        raise ValueError("Scholar web alias collides with a repository source path")
    if (root / "works").is_symlink():
        raise ValueError("Symlinked Scholar web directory")
    for record in seen.values():
        try:
            (root / record["alias"]).lstat()
        except FileNotFoundError:
            pass
        else:
            raise ValueError("Scholar web alias already exists in the repository")
    return payload


@dataclass(frozen=True)
class ProjectedPDF:
    repo_root: Path
    source_pdf: str
    alias: str
    bytes: int
    sha256: str
    citation_key: str
    num: int
    review_json: str

    @property
    def url(self):
        return SITE_URL + self.alias

    @property
    def source(self):
        return self.repo_root / self.source_pdf

    @property
    def source_url(self):
        from docxology_tools.paper_artifacts import encoded_path

        return SITE_URL + encoded_path(self.source_pdf)

    @property
    def review(self):
        return json.loads(self.review_json)

    def read_bytes(self):
        path = source_file(self.repo_root, self.source_pdf)
        if path is None:
            raise ValueError("Scholar PDF source is no longer public")
        with path.open("rb") as stream:
            data = stream.read(self.bytes + 1)
        if len(data) != self.bytes or hashlib.sha256(data).hexdigest() != self.sha256:
            raise ValueError("Scholar PDF source no longer matches its reviewed bytes")
        return data

    def manifest_record(self):
        return {
            "path": self.alias,
            "source_path": self.source_pdf,
            "bytes": self.bytes,
            "sha256": self.sha256,
            "citation_key": self.citation_key,
            "num": self.num,
            "reviewed_at": self.review["reviewed_at"],
            "reviewed_by": self.review["reviewed_by"],
            "license": self.review["rights"]["license"],
        }


def verified_projections(
    root: Path, visible=None, *, declared=None, read_text=None
) -> dict[str, ProjectedPDF]:
    root = root.resolve()
    visible = source_paths(root) if visible is None else visible
    payload = declared_projections(root, visible, read_text=read_text) if declared is None else declared
    if not payload["reservations"]:
        return {}
    identities = _json(root, "data/work-identifiers.json", visible, read_text=read_text)
    validate_registry(identities)
    works = _json(root, "data/works.json", visible, read_text=read_text)["works"]
    if not isinstance(works, list):
        raise ValueError("Current Scholar works must be a list")
    by_key, by_num = {}, {}
    for work in works:
        if (
            not isinstance(work, dict)
            or not isinstance(work.get("citation_key"), str)
            or type(work.get("num")) is not int
            or work["num"] <= 0
            or work["citation_key"] in by_key
            or work["num"] in by_num
        ):
            raise ValueError(
                "Duplicate or invalid current Scholar work dataset identity"
            )
        by_key[work["citation_key"]] = work
        by_num[work["num"]] = work
    bibliography = source_file(root, "pages/BIBLIOGRAPHY.md", visible)
    if bibliography is None:
        raise ValueError("Missing canonical Scholar bibliography")
    rows = list(iter_bibliography_rows(bibliography))
    validate_catalog(rows, identities)
    rows_by_num = {row.num: row for row in rows}
    master = _json(root, "papers/paper_metadata.json", visible, read_text=read_text)
    result = {}
    from docxology_tools.paper_artifacts import PaperResources

    for record in payload["reservations"]:
        reservation = identities["identifiers"].get(str(record["num"]))
        if reservation is None or reservation["citation_key"] != record["citation_key"]:
            raise ValueError("Scholar alias owner lost its permanent work reservation")
        artifact = ProjectedPDF(
            root,
            record["source_pdf"],
            record["alias"],
            record["bytes"],
            record["sha256"],
            record["citation_key"],
            record["num"],
            json.dumps(record["review"], sort_keys=True),
        )
        artifact.read_bytes()
        if payload["selections"].get(record["citation_key"]) == record["sha256"]:
            work = by_key.get(record["citation_key"], {})
            row = rows_by_num.get(record["num"])
            if (
                reservation["status"] != "active"
                or row is None
                or type(work.get("num")) is not int
                or work["num"] != record["num"]
                or work.get("type") != "Paper"
                or row.typ != "Paper"
                or work.get("title") != record["title"]
                or row.title != record["title"]
                or work.get("docs_path", "").rstrip("/") + "/" != record["docs_path"]
                or row.folder != PurePosixPath(record["docs_path"]).name
                or work.get("doi", "").casefold() != record["doi"].casefold()
                or work.get("authors") != record["authors"]
                or row.authors != record["authors"]
            ):
                raise ValueError(
                    "Scholar source review no longer matches the exact current work"
                )
            link = urlsplit(canonical_link_url(row.link_cell, row.venue))
            if (
                link.scheme != "https"
                or link.netloc != "doi.org"
                or unquote(link.path[1:]).casefold() != record["doi"].casefold()
            ):
                raise ValueError(
                    "Scholar review DOI differs from the canonical bibliography"
                )
            resources = PaperResources._load(root, record["docs_path"], visible, read_text=read_text)
            metadata = _json(root, record["docs_path"] + "metadata.json", visible, read_text=read_text)
            if (
                resources.remote_primary_pdf
                or resources.primary_pdf != artifact.source
                or metadata.get("doi", "").casefold() != record["doi"].casefold()
                or metadata.get("citation_metadata", {}).get("resource_type")
                != "journal-article"
                or metadata.get("citation_metadata", {}).get("doi", "").casefold()
                != record["doi"].casefold()
                or publication_date(work, metadata) != record["publication_date"]
            ):
                raise ValueError(
                    "Scholar association differs from the selected journal PDF edition"
                )
            abstract = master.get(PurePosixPath(record["docs_path"]).name, {}).get(
                "abstract"
            )
            if (
                not isinstance(abstract, str)
                or not abstract.strip()
                or metadata.get("abstract") != abstract
                or hashlib.sha256(abstract.encode()).hexdigest()
                != record["review"]["abstract"]["sha256"]
            ):
                raise ValueError(
                    "Complete author-written abstract no longer matches reviewed source"
                )
            provenance = metadata.get("abstract_provenance") or {}
            if (
                provenance.get("source_pdf_sha256")
                and provenance["source_pdf_sha256"] != record["sha256"]
            ):
                raise ValueError("Author abstract provenance names another PDF edition")
        result[record["alias"]] = artifact
    return result


def projection_for_resources(resources, visible=None, *, read_text=None):
    if resources.remote_primary_pdf or resources.folder is None:
        return None
    visible = source_paths(resources.repo_root) if visible is None else visible
    if source_file(resources.repo_root, REGISTRY, visible) is None:
        if (resources.repo_root / REGISTRY).exists():
            raise ValueError("Scholar registry is not an eligible public source")
        return None
    payload = declared_projections(resources.repo_root, visible, read_text=read_text)
    candidates = [
        item
        for item in payload["reservations"]
        if item["docs_path"] == resources.docs_path
        and payload["selections"].get(item["citation_key"]) == item["sha256"]
    ]
    if not candidates:
        return None
    if len(candidates) != 1:
        raise ValueError("Ambiguous current Scholar association for one paper folder")
    return verified_projections(resources.repo_root, visible, declared=payload, read_text=read_text)[
        candidates[0]["alias"]
    ]


def resolve_alias(root: Path, relative: str, visible=None):
    if not re.fullmatch(r"works/[0-9a-f]{64}\.pdf", relative):
        return None
    return verified_projections(root, visible).get(relative)


class _VisibleMainText(HTMLParser):
    """Conservative static source visibility, separate from browser rendering."""

    VOID = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
    INERT = {"script", "style", "template", "details", "noscript", "iframe", "object"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.frames = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        hidden = tag in self.INERT or any(
            name in {"hidden", "inert"}
            or (name == "aria-hidden" and (value or "").casefold() == "true")
            or (
                name == "style"
                and re.search(
                    r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)",
                    value or "",
                    re.I,
                )
            )
            for name, value in attrs
        )
        if tag not in self.VOID:
            self.frames.append((tag, hidden))
        elif tag in {"br", "hr"}:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        for index in range(len(self.frames) - 1, -1, -1):
            if self.frames[index][0] == tag:
                del self.frames[index:]
                break

    def handle_data(self, data):
        if any(tag == "main" for tag, _ in self.frames) and not any(
            hidden for _, hidden in self.frames
        ):
            self.parts.append(data)


def abstract_visible(page: str, abstract: str) -> bool:
    """Require the entire recorded display text in non-gated static main text.

    This does not attest CSS/browser rendering, crawling or Scholar indexing.
    """
    from docxology_tools.abstract_text import abstract_display_text

    expected = re.sub(r"\s+", " ", abstract_display_text(abstract)).strip()
    if not expected:
        return False
    parser = _VisibleMainText()
    parser.feed(page)
    parser.close()
    return expected in re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
