from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from docxology_tools.content_citations import ContentCitations


class ContentPage(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[dict] = []
        self.in_main = False
        self.anchor: dict | None = None
        self.annotations: list[dict] = []
        self.annotation: dict | None = None
        self.annotation_depth = 0
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.annotation is not None and tag == self.annotation["tag"]:
            self.annotation_depth += 1
        for kind, attribute in (("citation", "data-citation-key"), ("reference", "data-reference-key")):
            if attribute in attrs:
                self.annotation = dict(kind=kind, tag=tag, key=attrs[attribute], text="", links=[])
                self.annotation_depth = 1
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "main":
            self.in_main = True
        if tag == "a" and attrs.get("href"):
            self.anchor = dict(href=attrs["href"], text="", line=self.getpos()[0], in_main=self.in_main,
                               cited_author=attrs.get("data-cited-author"))
            self.links.append(self.anchor)
            if self.annotation is not None:
                self.annotation["links"].append(attrs["href"])

    def handle_endtag(self, tag):
        if self.annotation is not None and tag == self.annotation["tag"]:
            self.annotation_depth -= 1
            if self.annotation_depth == 0:
                self.annotation["text"] = " ".join(self.annotation["text"].split())
                self.annotations.append(self.annotation)
                self.annotation = None
        if tag == "a":
            self.anchor = None
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.annotation is not None:
            self.annotation["text"] += data
        if self.anchor is not None:
            self.anchor["text"] += data


def public_html_paths(root: Path) -> list[Path]:
    from build_pages_artifact import is_published_path, tracked_paths

    return sorted(
        root / path for path in tracked_paths()
        if path.suffix == ".html" and is_published_path(path) and (root / path).is_file()
    )


def audit_content(root: Path, paths: list[Path], works: list[dict], *, published_paths: set[Path] | None = None) -> dict:
    catalog = ContentCitations(works)
    parsed = {path: ContentPage(path.read_text(encoding="utf-8")) for path in paths}
    citations = []
    external: dict[str, list[str]] = {}
    errors = []
    inputs = {}
    checked_links = 0
    checked_fragments = 0
    for path, page in parsed.items():
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        inputs[relative] = hashlib.sha256(text.encode()).hexdigest()
        if page.annotation is not None:
            errors.append(f"{relative}: unterminated citation annotation")
        for annotation in page.annotations:
            key = annotation["key"]
            if key not in catalog.works:
                errors.append(f"{relative}: unknown citation key {key}")
            else:
                expected = ContentCitations(works)
                citation = expected.cite(key)
                fragment = citation if annotation["kind"] == "citation" else expected.references()
                if annotation != ContentPage(fragment).annotations[0]:
                    errors.append(f"{relative}: citation text/target differs from catalog for {key}")
        cited = {a["key"] for a in page.annotations if a["kind"] == "citation"}
        referenced = {a["key"] for a in page.annotations if a["kind"] == "reference"}
        if cited != referenced:
            errors.append(f"{relative}: inline citation/reference coverage differs")
        for link in page.links:
            url = urlsplit(urljoin("https://danielarifriedman.com/" + relative, link["href"]))
            if url.scheme not in {"http", "https"}:
                continue
            location = f'{relative}:{link["line"]}'
            if url.hostname not in {"danielarifriedman.com", "www.danielarifriedman.com"}:
                if link["in_main"]:
                    external.setdefault(link["href"], []).append(location)
                continue
            target = (root / unquote(url.path).lstrip("/")).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f'{location}: local target escapes the site root {link["href"]}')
                continue
            if target.is_dir():
                target /= "index.html"
            checked_links += 1
            if not target.is_file():
                errors.append(f'{location}: missing local target {link["href"]}')
                continue
            if published_paths is not None and target.relative_to(root) not in published_paths:
                errors.append(f'{location}: target is absent from the Pages projection {link["href"]}')
                continue
            if url.fragment and target.suffix == ".html":
                fragment = unquote(url.fragment)
                if not fragment.startswith(":~:text="):
                    target_page = parsed.get(target)
                    if target_page is None:
                        target_page = ContentPage(target.read_text(encoding="utf-8"))
                        parsed_target_ids = target_page.ids
                    else:
                        parsed_target_ids = target_page.ids
                    checked_fragments += 1
                    if fragment not in parsed_target_ids:
                        errors.append(f'{location}: missing fragment {link["href"]}')
            key = target.stem if target.parent == root / "works" else None
            if key and key != "index":
                if key not in catalog.works:
                    errors.append(f"{location}: unknown work target {key}")
                elif link["in_main"]:
                    citations.append(dict(page=relative, line=link["line"], key=key, label=" ".join(link["text"].split())))
                    if link.get("cited_author") and link["cited_author"] not in {name.split(",")[0] for name in catalog.works[key]["authors"]}:
                        errors.append(f'{location}: {link["cited_author"]} is absent from the contributors to {key}')
    collaborator_source = root / "pages/COLLABORATORS.md"
    if collaborator_source.is_file():
        source = collaborator_source.read_text(encoding="utf-8")
        inputs["pages/COLLABORATORS.md"] = hashlib.sha256(source.encode()).hexdigest()
        folders = {w.get("docs_path"): w for w in works if w.get("docs_path")}
        family = ""
        for line_number, line in enumerate(source.splitlines(), 1):
            if line.startswith("### "):
                family = line[4:].split(" — ")[0].split()[-1]
            if line.startswith("**Joint publications**"):
                for folder in re.findall(r"\]\(\.\./(papers/[^)]+/)\)", line):
                    work = folders.get(folder)
                    if work is None or family not in {name.split(",")[0] for name in work["authors"]}:
                        errors.append(f"pages/COLLABORATORS.md:{line_number}: {family} joint-publication attribution lacks matching catalog contributors: {folder}")
    return dict(
        scope="Tracked HTML in the Pages publication policy, including paper, work, video, art, and content pages, plus the Markdown collaborator joint-publication list",
        evidence_boundary="Local target/fragment integrity and exact catalog-derived inline citations; semantic support and live external responses require separate source review",
        html_pages=len(paths), local_links_checked=checked_links, fragments_checked=checked_fragments,
        work_links=len(citations), distinct_works=len({c["key"] for c in citations}),
        input_sha256=inputs, catalog_sha256=hashlib.sha256(json.dumps(works, sort_keys=True).encode()).hexdigest(),
        errors=errors, citations=citations, external_links={url: sorted(set(sources)) for url, sources in sorted(external.items())},
    )
