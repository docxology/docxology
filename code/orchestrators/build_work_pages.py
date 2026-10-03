#!/usr/bin/env python3
"""Generate per-work HTML landing pages from data/works.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS_DIR = REPO_ROOT / "works"
ENRICHMENT_OUT = REPO_ROOT / "data" / "work-enrichment.json"
GENERATED_PAGE_MARKER = "<!-- docxology:generated-work-page; ownership=renderer -->"

from docxology_tools.generated_outputs import (  # noqa: E402
    generated_output_files,
    read_generated_output_text,
    remove_generated_output,
    safe_generated_output_path,
    stale_output_paths,
    stable_generated_output_timestamp,
    write_output_texts,
)
from docxology_tools.build_stamp import footer_build_stamp_html, reuse_on_disk_stamp  # noqa: E402
from docxology_tools.site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    CITE_EXPORT_SCRIPT_TAG,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    breadcrumb_jsonld_script,
    canonical_work_key,
    clip_description,
    domain_page_href,
    render_breadcrumb,
    render_nav,
)

from docxology_tools.report_paths import generated_timestamp  # noqa: E402
from docxology_tools.abstract_text import abstract_display_text  # noqa: E402
from docxology_tools.paper_artifacts import PaperResources, source_file, source_paths  # noqa: E402


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


# Ordered (display label, publishing-status label) for the 8 platforms a work may
# live on. The status label matches the present/missing strings emitted into
# data/publishing-status.json (the generated source of truth); the display label is
# what the work page shows.
PLATFORMS: list[tuple[str, str]] = [
    ("Zenodo", "Zenodo (DOI)"),
    ("GitHub", "GitHub"),
    ("arXiv", "arXiv"),
    ("OSF", "OSF"),
    ("HuggingFace", "HuggingFace"),
    ("Software Heritage", "IPFS/Software-Heritage"),
    ("PyPI", "PyPI"),
    ("Full documentation", "personal-site canonical page"),
]


def load_publishing_status() -> dict[str, dict]:
    """Map canonical_page (== each work's docs_path) -> its publishing-status entry."""
    path = REPO_ROOT / "data" / "publishing-status.json"
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    return {e["canonical_page"]: e for e in entries if e.get("canonical_page")}


def load_works() -> list[dict]:
    with open(REPO_ROOT / "data" / "works.json", encoding="utf-8") as f:
        works = json.load(f)["works"]
    pub = load_publishing_status()
    for work in works:
        work["publishing"] = pub.get(work.get("docs_path", ""), {})
    return works


PRINCIPAL_LD = {
    "@type": "Person",
    "@id": "https://danielarifriedman.com/#person",
    "name": "Daniel Ari Friedman",
    "url": "https://danielarifriedman.com/",
    "sameAs": [
        "https://orcid.org/0000-0001-6232-9096",
        "https://www.wikidata.org/wiki/Q138781444",
        "https://www.flickr.com/photos/daniel_friedman/",
    ],
}


def author_ld(work: dict) -> dict | list[dict] | None:
    """schema.org author(s) for a work.

    The principal keeps his full identity node (@id + ORCID/Wikidata sameAs);
    co-authors from the bibliography's Authors column are emitted as plain
    Person entries, and literal names without a comma as Organization.
    """
    names = work.get("authors") or []
    if not names:
        return None
    entities: list[dict] = []
    for name in names:
        family, _, given = name.partition(",")
        if family.strip() == "Friedman" and given.strip().startswith("Daniel"):
            entities.append(PRINCIPAL_LD)
        elif "," not in name:
            entities.append({"@type": "Organization", "name": name})
        else:
            entities.append({"@type": "Person", "name": f"{given.strip()} {family.strip()}".strip()})
    return entities[0] if len(entities) == 1 else entities


def display_name(name: str) -> str:
    """"Family, Given" as a reader-facing "Given Family"; literals unchanged."""
    if "," not in name:
        return name
    family, _, given = name.partition(",")
    return f"{given.strip()} {family.strip()}".strip()


def byline_html(work: dict) -> str:
    names = work.get("authors") or []
    if not names:
        return ""
    return f'        <p class="byline">{h(", ".join(display_name(n) for n in names))}</p>'


def _github_repo(identifiers: dict) -> str:
    gh = identifiers.get("github")
    if isinstance(gh, list):
        gh = gh[0] if gh else ""
    return str(gh or "")


def platform_link(status_label: str, work: dict) -> str:
    """Absolute URL for a work's presence on the given platform, or '' if not derivable.

    Thin read of the joined publishing-status identifiers (the generated source of truth),
    reusing the same DOI/sameAs URL conventions as json_ld().
    """
    identifiers = work.get("publishing", {}).get("identifiers", {})
    if status_label == "Zenodo (DOI)":
        doi = identifiers.get("zenodo_doi")
        return f"https://doi.org/{doi}" if doi else ""
    if status_label == "GitHub":
        repo = _github_repo(identifiers)
        if not repo:
            return ""
        return repo if repo.startswith("http") else f"https://github.com/{repo}"
    if status_label == "arXiv":
        arxiv = identifiers.get("arxiv")
        if not arxiv:
            return ""
        bare = str(arxiv).split("arXiv.")[-1]
        return f"https://arxiv.org/abs/{bare}"
    if status_label == "OSF":
        osf = identifiers.get("osf")
        return f"https://doi.org/{osf}" if osf else ""
    if status_label == "HuggingFace":
        hf = identifiers.get("huggingface")
        return f"https://huggingface.co/{hf}" if hf else ""
    if status_label == "IPFS/Software-Heritage":
        repo = _github_repo(identifiers)
        if not repo:
            return ""
        origin = repo if repo.startswith("http") else f"https://github.com/{repo}"
        return f"https://archive.softwareheritage.org/browse/origin/directory/?origin_url={origin}"
    if status_label == "PyPI":
        pypi = identifiers.get("pypi")
        return f"https://pypi.org/project/{pypi}/" if pypi else ""
    if status_label == "personal-site canonical page":
        canon = identifiers.get("canonical") or work.get("docs_path", "")
        return f"https://danielarifriedman.com/{canon.rstrip('/')}/" if canon else ""
    return ""


def present_platform_urls(work: dict) -> list[str]:
    """Absolute URLs for the platforms a work is actually present on (deduped, ordered)."""
    present = set(work.get("publishing", {}).get("present_platforms", []))
    urls: list[str] = []
    for _display, status_label in PLATFORMS:
        if status_label in present:
            link = platform_link(status_label, work)
            if link and link not in urls:
                urls.append(link)
    return urls


def platform_availability_card(work: dict) -> str:
    """A meta-card listing all 8 platforms: present ones link out, missing ones are muted."""
    pub = work.get("publishing", {})
    if not pub:
        return ""
    present = set(pub.get("present_platforms", []))
    rows: list[str] = []
    for display, status_label in PLATFORMS:
        if status_label in present:
            link = platform_link(status_label, work)
            label = f'<a href="{h(link)}">{h(display)}</a>' if link else h(display)
            rows.append(f'<li>✅ {label}</li>')
        else:
            rows.append(f'<li class="muted">⬜ {h(display)}</li>')
    return (
        '<div class="meta-card platform-card"><strong>Platform availability</strong>'
        f'<ul class="platform-list">{"".join(rows)}</ul></div>'
    )


def strip_md(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_>#|]+", " ", text)
    text = re.sub(r"[<>]", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##+\s+.*{re.escape(heading)}.*?$", re.I | re.M)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##+\s+", markdown[start:], re.M)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def section_paragraph(markdown: str, heading: str, max_chars: int = 900) -> str:
    raw = section(markdown, heading)
    if not raw:
        return ""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("|") or line.startswith("- ") or line.startswith("* "):
            continue
        lines.append(line)
    text = strip_md(" ".join(lines))
    return text[:max_chars].rstrip()


def bullet_section(markdown: str, heading: str, limit: int = 5) -> list[str]:
    raw = section(markdown, heading)
    items = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            item = strip_md(stripped[2:])
            if item:
                items.append(item)
        if len(items) >= limit:
            break
    return items


def keyword_list(markdown: str, limit: int = 12) -> list[str]:
    raw = section(markdown, "Keywords")
    if not raw:
        return []
    text = strip_md(raw.replace("·", ",").replace(";", ","))
    words = [w.strip(" ,.") for w in re.split(r",|\n", text) if w.strip(" ,.")]
    seen: set[str] = set()
    out: list[str] = []
    for word in words:
        key = word.lower()
        if key not in seen:
            seen.add(key)
            out.append(word)
        if len(out) >= limit:
            break
    return out


def enrichment_for(
    work: dict, *, resources: PaperResources | None = None, curated: dict | None = None,
    visible_paths: frozenset[str] | None = None,
) -> dict:
    """Read complete curated content, retaining a source for each displayed field.

    Explicitly empty curated fields and cleared metadata summaries are decisions,
    so they never fall back to stale generated README/SKILL text. Hand-authored
    documentation remains a fallback when the corresponding authoritative field
    is absent. Concepts and contributions are kept apart from findings.
    """
    from urllib.parse import urlsplit

    from docxology_tools.metadata_templates import (
        is_template_method,
        specific_findings,
        specific_method_details,
    )

    resources = resources or work.get("_resources")
    if resources is None:
        resources = PaperResources.load(REPO_ROOT, work.get("docs_path") or "", visible_paths)
    if curated is None:
        master_path = source_file(REPO_ROOT, "papers/paper_metadata.json", visible_paths)
        curated = json.loads(master_path.read_text(encoding="utf-8")) if master_path else {}
    if not isinstance(curated, dict):
        raise ValueError("Consolidated paper metadata must be an object")
    folder = resources.folder.name if resources.folder else ""
    entry = curated.get(folder, {})
    if not isinstance(entry, dict):
        raise ValueError(f"Curated metadata must be an object for {folder}")
    metadata = resources.metadata or {}
    sources: dict[str, str] = {}
    master_source = "papers/paper_metadata.json"
    metadata_source = f"{resources.docs_path}metadata.json" if folder else ""
    readme_text = resources.readme.read_text(encoding="utf-8", errors="replace") if resources.readme else ""
    skill_text = resources.skill.read_text(encoding="utf-8", errors="replace") if resources.skill else ""
    documents = [
        (readme_text, f"{resources.docs_path}README.md"),
        (skill_text, f"{resources.docs_path}SKILL.md"),
    ]

    def missing_notice(value: str) -> bool:
        return bool(re.match(
            r"^(?:No abstract (?:is recorded|is available|available)|"
            r"Detailed local abstract is not available|"
            r"(?:Abstract|Summary) (?:is )?not available)\b", value, re.I,
        ))

    def provenance(value: object) -> dict:
        if not isinstance(value, dict):
            return {}
        result = {}
        for field in ("source", "date", "work_kind", "kind"):
            text = value.get(field)
            if isinstance(text, str) and text and not text.startswith(("/", "file:", "~/")):
                result[field] = text
        url = value.get("url")
        if isinstance(url, str):
            try:
                parsed = urlsplit(url)
            except ValueError:
                return result
            if parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password:
                result["url"] = url
        return result

    if "abstract" in entry:
        value = entry["abstract"]
        abstract = value.strip() if isinstance(value, str) else ""
        if abstract and not missing_notice(abstract):
            sources["abstract"] = master_source
        else:
            abstract = ""
    else:
        abstract = ""
        for text, origin in documents:
            candidate = strip_md(section(text, "Abstract"))
            if candidate and not missing_notice(candidate):
                abstract = candidate
                sources["abstract"] = origin
                break

    topic = str(entry.get("topic") or folder.partition("_")[2]).casefold()
    if "keywords" in entry or "tags" in entry:
        keywords = entry.get("keywords", entry.get("tags")) or []
        keyword_source = master_source
    elif "keywords" in metadata or "tags" in metadata:
        keywords = metadata.get("keywords", metadata.get("tags")) or []
        keyword_source = metadata_source
    else:
        keywords, keyword_source = [], ""
        for text, origin in documents:
            candidate = keyword_list(text)
            if len(candidate) == 1 and candidate[0].casefold() == topic:
                candidate = []
            if candidate:
                keywords, keyword_source = candidate, origin
                break
    keywords = list(dict.fromkeys(
        word.strip() for word in keywords
        if isinstance(word, str) and word.strip()
    )) if isinstance(keywords, list) else []
    if keywords:
        sources["keywords"] = keyword_source

    methods = []
    if "methods" in metadata:
        methods = [
            f"{name} — {description}" if description else name
            for name, description in specific_method_details(metadata.get("methods"))
        ]
        method_source = metadata_source
    else:
        method_source = ""
        for text, origin in documents:
            candidates = bullet_section(text, "Methods", limit=10000)
            candidates = [item for item in candidates if not is_template_method({"name": item.split(" — ", 1)[0]})]
            if candidates:
                methods, method_source = candidates, origin
                break
    if methods:
        sources["methods"] = method_source

    grounded = (
        isinstance(metadata.get("summary_provenance"), dict)
        and metadata["summary_provenance"].get("source") == "full_text.md"
    )
    findings = []
    if "key_findings" in metadata:
        findings = specific_findings(metadata.get("key_findings"), *([] if grounded else [abstract]))
        finding_source = metadata_source
    else:
        finding_source = ""
        for text, origin in documents:
            candidate = specific_findings(bullet_section(text, "Key Findings", limit=10000), abstract)
            if candidate:
                findings, finding_source = candidate, origin
                break
    if findings:
        sources["findings"] = finding_source

    concepts = []
    if "key_concepts" in metadata or "concepts" in metadata:
        concepts = [str(item).strip() for item in metadata.get("key_concepts", metadata.get("concepts")) or [] if str(item).strip()]
        concept_source = metadata_source
    else:
        concept_source = ""
        for text, origin in documents:
            candidate = bullet_section(text, "Key Concepts", limit=10000) or bullet_section(text, "Key Contributions", limit=10000)
            if candidate:
                concepts, concept_source = candidate, origin
                break
    if concepts:
        sources["concepts"] = concept_source

    return {
        "citation_key": work["citation_key"],
        "abstract": abstract,
        "keywords": keywords,
        "findings": findings,
        "methods": methods,
        "concepts": concepts,
        "sources": sources,
        "source": next((sources[field] for field in ("abstract", "findings", "methods", "concepts", "keywords") if field in sources), ""),
        "abstract_provenance": provenance(metadata.get("abstract_provenance")) if abstract else {},
        "summary_provenance": provenance(metadata.get("summary_provenance")) if methods or findings else {},
    }


def enrichment_map(
    works: list[dict], *, visible_paths: frozenset[str] | None = None,
) -> dict[str, dict]:
    """Load the curated collection and Git-visible source inventory once per batch."""
    visible = source_paths(REPO_ROOT) if visible_paths is None else visible_paths
    master_path = source_file(REPO_ROOT, "papers/paper_metadata.json", visible)
    curated = json.loads(master_path.read_text(encoding="utf-8")) if master_path else {}
    return {
        work["citation_key"]: enrichment_for(
            work,
            resources=work.get("_resources") or PaperResources.load(REPO_ROOT, work.get("docs_path") or "", visible),
            curated=curated,
            visible_paths=visible,
        )
        for work in works
    }


def abstract_source_html(enrichment: dict, prefix: str = "../") -> str:
    """Label the overview's public source without exposing review notes.

    Provenance labels and external hosts are the audited values already used by
    the archive. Unknown free-text provenance falls back to the actual public
    source file, rather than being copied into the page.
    """
    from urllib.parse import urlsplit

    from docxology_tools.paper_artifacts import encoded_path

    if not enrichment.get("abstract"):
        return ""
    provenance = enrichment.get("abstract_provenance") or {}
    if not isinstance(provenance, dict):
        provenance = {}
    labels = {
        "papers/paper_metadata.json": ("Curated paper metadata", ""),
        "abridged publisher synopsis": ("Abridged publisher synopsis", "link.springer.com"),
        "published Summary in NLM JATS full text": ("Published Summary (NLM full text)", "pmc-oa-opendata.s3.amazonaws.com"),
        "Rendered manuscript Abstract in exact Zenodo v3.6.0 archive": ("Archived manuscript abstract", ""),
    }
    label, allowed_host = labels.get(provenance.get("source"), ("", ""))
    target = ""
    url = provenance.get("url")
    if allowed_host and isinstance(url, str):
        try:
            parsed = urlsplit(url)
        except ValueError:
            parsed = None
        if (
            parsed and parsed.scheme == "https" and parsed.netloc == allowed_host
            and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment
        ):
            target = url
    sources = enrichment.get("sources") or {}
    origin = sources.get("abstract", "") if isinstance(sources, dict) else ""
    if isinstance(origin, str):
        if origin == "papers/paper_metadata.json":
            label = label or "Curated paper metadata"
            target = target or prefix + encoded_path(origin)
        elif re.fullmatch(r"papers/\d{4}_[^/\\\x00-\x1f]+/(?:README\.md|SKILL\.md|metadata\.json)", origin):
            name = origin.rsplit("/", 1)[-1]
            label = label or {
                "README.md": "Paper overview (README)",
                "SKILL.md": "Paper documentation (SKILL)",
                "metadata.json": "Paper metadata",
            }[name]
            target = target or prefix + encoded_path(origin)
    if not label:
        return ""
    source = f'<a href="{h(target)}">{h(label)}</a>' if target else h(label)
    return f'<p class="summary-sources abstract-source">Overview source: {source}.</p>'


def resources_for(work: dict) -> PaperResources:
    return work.get("_resources") or PaperResources.load(REPO_ROOT, work.get("docs_path", ""))


def local_docs_link(path: str) -> str:
    return PaperResources.load(REPO_ROOT, path).docs_url


def full_text_link(docs_path: str) -> str:
    resources = PaperResources.load(REPO_ROOT, docs_path)
    return resources.url(resources.full_text) if resources.full_text else ""


def image_gallery_link_work(docs_path: str) -> str:
    resources = PaperResources.load(REPO_ROOT, docs_path)
    return resources.github_url + "/images" if resources.images else ""


def source_repository_url(docs_path: str, resources: PaperResources | None = None) -> str:
    """Associated software repository, distinct from this archive's paper folder."""
    from urllib.parse import urlsplit

    resources = resources or PaperResources.load(REPO_ROOT, docs_path)
    meta = resources.metadata or {}
    candidates = [meta.get("github_repo", "")]
    candidates.extend(item.get("url", "") for item in meta.get("related_resources", []) if item.get("type") == "repository")
    for url in candidates:
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", str(url)):
            url = "https://github.com/" + str(url)
        parsed = urlsplit(str(url))
        if parsed.scheme == "https" and parsed.netloc == "github.com" and not parsed.query and not parsed.fragment:
            parts = parsed.path.strip("/").split("/")
            if len(parts) == 2 and all(re.fullmatch(r"[A-Za-z0-9_.-]+", part) and part not in {".", ".."} for part in parts):
                return "https://github.com/" + "/".join(parts)
    return ""


def load_bibtex_entries() -> dict[str, str]:
    """Read the managed bibliography safely once for a rendering batch."""
    source = read_generated_output_text(REPO_ROOT, REPO_ROOT / "bibliography.bib")
    if source is None:
        return {}
    entries = {}
    for match in re.finditer(r"(?ms)^@\w+\{([^,\n]+),.*?^\}\s*$", source):
        key = match.group(1)
        if key in entries:
            raise ValueError(f"Duplicate BibTeX citation key: {key}")
        entries[key] = match.group(0).strip()
    return entries


def work_bibtex(citation_key: str) -> str:
    """The work's BibTeX entry from bibliography.bib (same per-work citation keys).

    Returns '' when the key is absent so pages for un-bibbed works simply omit
    the Copy-BibTeX affordance instead of embedding a stale/wrong entry.
    """
    return load_bibtex_entries().get(citation_key, "")


def bibtex_button_html(work: dict) -> str:
    """Copy-BibTeX button + embedded entry, wired by js/cite-export.js (CSP-safe)."""
    bib = work["_bibtex"] if "_bibtex" in work else work_bibtex(work["citation_key"])
    if not bib:
        return ""
    # Script contents are raw text: HTML entities would be copied literally.
    # JSON preserves the entry exactly; escaping '<' prevents a citation from
    # closing the inert script element with a literal </script> sequence.
    payload = json.dumps(bib, ensure_ascii=False).replace("<", "\\u003c")
    return (
        '<button type="button" class="btn btn-outline" id="cite-bibtex-btn" '
        'aria-label="Copy BibTeX entry to clipboard">Copy BibTeX</button>\n'
        f'        <script type="application/json" id="work-bibtex">{payload}</script>'
    )


def citation_text(work: dict) -> str:
    venue = f" {work['venue']}." if work.get("venue") else ""
    url = work.get("url") or f"https://danielarifriedman.com/works/{work['citation_key']}.html"
    doi = f" DOI: {work['doi']}." if work.get("doi") else ""
    authors = "; ".join(work.get("authors") or [])
    byline = f"{authors}. " if authors else ""
    return f"{byline}{work['year']}. {work['title']}.{venue}{doi} URL: {url}."


def breadcrumb_trail(work: dict) -> list[tuple[str, str]]:
    """Shared-renderer (label, root-relative path) pairs for one work page."""
    return [
        ("Home", ""),
        ("Works", "works/"),
        (work["title"], f"works/{work['citation_key']}.html"),
    ]


def related_works_html(work: dict) -> str:
    related = work.get("related", [])
    if not related:
        return ""
    items = "".join(
        f'<li><a href="{h(r["citation_key"])}.html">{h(r["title"])}</a>'
        f'<span class="muted"> · {h(r["year"])}</span></li>'
        for r in related
    )
    domain_href = domain_page_href(work.get("domain", ""), depth=1)
    domain_name = h(work["domain_name"])
    header_domain = f'<a href="{domain_href}">{domain_name}</a>' if domain_href else domain_name
    hub_link = (
        f'<p><a class="related-hub-link" href="{domain_href}">View all {domain_name} works, software &amp; media →</a></p>'
        if domain_href
        else ""
    )
    return f"""
        <section class="section">
            <div class="section-header"><h2>Related in {header_domain}</h2><p>Other catalogued works in the same domain.</p><div class="section-divider"></div></div>
            <ul class="related-list">{items}</ul>
            {hub_link}
        </section>"""


def json_ld(work: dict) -> str:
    typ = "ScholarlyArticle" if work["type"] in {"Paper", "Book Chapter", "Poster", "Thesis", "Report", "Preprint", "Review"} else "CreativeWork"
    enrich = work.get("enrichment", {})
    same_as = [work["url"]] if work.get("url") else []
    if work.get("doi"):
        same_as.append(f"https://doi.org/{work['doi']}")
    # Keep structured data in sync with the visible Platform availability card.
    for url in present_platform_urls(work):
        if url not in same_as:
            same_as.append(url)
    data = {
        "@context": "https://schema.org",
        "@type": typ,
        "@id": f"https://danielarifriedman.com/works/{work['citation_key']}.html#work",
        "name": work["title"],
        "headline": work["title"],
        "datePublished": str(work["year"]),
        "url": f"https://danielarifriedman.com/works/{work['citation_key']}.html",
        "mainEntityOfPage": f"https://danielarifriedman.com/works/{work['citation_key']}.html",
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
        "about": [
            {"@type": "DefinedTerm", "name": work["domain_name"]},
            {"@type": "DefinedTerm", "name": work["type"]},
        ],
        "genre": work["type"],
        "inLanguage": "en",
        "sameAs": same_as,
        "image": "https://danielarifriedman.com/og-publications.jpg",
    }
    if author := author_ld(work):
        data["author"] = author
    if work.get("doi"):
        data["identifier"] = [
            {"@type": "PropertyValue", "propertyID": "DOI", "value": work["doi"], "url": f"https://doi.org/{work['doi']}"},
            {"@type": "PropertyValue", "propertyID": "Citation key", "value": work["citation_key"]},
        ]
    else:
        data["identifier"] = {"@type": "PropertyValue", "propertyID": "Citation key", "value": work["citation_key"]}
    if work.get("venue"):
        data["publisher"] = {"@type": "Organization", "name": work["venue"]}
    if enrich.get("abstract"):
        data["abstract"] = abstract_display_text(enrich["abstract"])
    if enrich.get("keywords"):
        data["keywords"] = enrich["keywords"]
        data["about"].extend({"@type": "DefinedTerm", "name": keyword} for keyword in enrich["keywords"][:8])
    if enrich.get("findings") or enrich.get("methods"):
        data["description"] = " ".join([*(enrich.get("findings") or []), *(enrich.get("methods") or [])])[:700]
    cite_str = citation_text(work)
    if cite_str:
        data["citation"] = cite_str

    if work.get("license"):
        data["license"] = work["license"]

    resources = resources_for(work)
    if resources.github_url:
        data["hasPart"] = {
            "@type": "CreativeWork", "name": "Paper documentation and source files",
            "url": resources.github_url,
        }
    encodings = [
        {"@type": "MediaObject", "encodingFormat": "application/pdf",
         "contentUrl": resources.absolute_url(pdf), "url": resources.absolute_url(pdf),
         "name": pdf.name, "contentSize": f"{pdf.stat().st_size} bytes"}
        for pdf in ([resources.primary_pdf] if resources.primary_pdf else [])
    ]
    attachments = [
        {"@type": "MediaObject", "encodingFormat": "application/pdf", "name": pdf.name,
         "contentUrl": resources.absolute_url(pdf), "contentSize": f"{pdf.stat().st_size} bytes"}
        for pdf in resources.pdfs if pdf != resources.primary_pdf
    ]
    if resources.full_text:
        text_encoding = {
            "@type": "TextObject", "encodingFormat": "text/markdown",
            "url": resources.absolute_url(resources.full_text), "name": "Full text (extracted)",
        }
        if resources.primary_pdf and resources.extraction_source and resources.extraction_source != resources.primary_pdf.name:
            attachments.append({**text_encoding, "@type": "MediaObject",
                                "contentUrl": text_encoding["url"],
                                "name": f"Extracted text from {resources.extraction_source}"})
        else:
            encodings.append(text_encoding)
    if encodings:
        data["encoding"] = encodings
    if attachments:
        data["associatedMedia"] = attachments
    return json.dumps(data, indent=4, ensure_ascii=False).replace("<", "\\u003c")


def work_page_title(work: dict, max_len: int = 100) -> str:
    """Full title first; clip on a word boundary only when the ~100-char
    SERP-safe budget forces it (Google wraps/clips visually, so the ellipsis
    budget stays generous instead of hard-truncating at ~60 chars)."""
    title = " ".join(work["title"].split())
    suffix = " — Daniel Ari Friedman"
    if len(h(title)) + len(h(suffix)) <= max_len:
        return f"{title}{suffix}"
    if len(h(title)) <= max_len:
        return title
    cut = title
    while len(h(cut + "…")) > max_len and len(cut) > 0:
        cut = cut.rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
        if " " not in cut and len(h(cut + "…")) > max_len:
            cut = cut[:-1]
    return cut + "…"


def page_head(work: dict) -> str:
    # Prefer the enriched abstract; otherwise build a per-work fallback that
    # includes the title so each page has a unique, descriptive meta description
    # (a bare "{type} in {domain} by ..." template collides across same-type works).
    fallback = (
        f"{work['title']} — {str(work['type']).lower()} in {work['domain_name']} "
        f"({work['year']}). Part of the unified bibliography."
    )
    description = abstract_display_text(work.get("enrichment", {}).get("abstract")) or fallback
    description = clip_description(description)
    canon_url = f"https://danielarifriedman.com/works/{canonical_work_key(work['citation_key'])}.html"
    page_title = work_page_title(work)
    resources = resources_for(work)
    citation_meta = [f'<meta name="citation_title" content="{h(work["title"])}">',
                     f'<meta name="citation_publication_date" content="{h(work["year"])}">']
    citation_meta.extend(f'<meta name="citation_author" content="{h(display_name(name))}">' for name in work.get("authors") or [])
    if work.get("doi"):
        citation_meta.append(f'<meta name="citation_doi" content="{h(work["doi"])}">')
    if resources.primary_pdf:
        citation_meta.append(f'<meta name="citation_pdf_url" content="{h(resources.absolute_url(resources.primary_pdf))}">')
    citation_meta_html = "\n    ".join(citation_meta)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(page_title)}</title>
    <meta name="description" content="{h(description)}">
    <meta name="robots" content="index, follow">
    {citation_meta_html}
    <link rel="canonical" href="{h(canon_url)}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    <link rel="alternate" type="text/x-bibtex" href="/bibliography.bib" title="BibTeX bibliography">
    <link rel="alternate" type="application/vnd.citationstyles.csl+json" href="/bibliography.csl.json" title="CSL JSON bibliography">
{HEAD_EXTRAS}
    <meta property="og:type" content="article">
    <meta property="og:title" content="{h(work['title'])}">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="{h(canon_url)}">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{h(work['title'])} — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{h(work['title'])}">
    <meta name="twitter:description" content="{h(description)}">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta name="twitter:image:alt" content="{h(work['title'])} — Daniel Ari Friedman">
    <link rel="stylesheet" href="../style.css?v=site-20261002b">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        {BREADCRUMB_CSS}
    </style>
    <script type="application/ld+json">
{json_ld(work)}
    </script>
{breadcrumb_jsonld_script(breadcrumb_trail(work))}
</head>
<body class="work-page">
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=1)}
"""


def pdf_downloads_html(resources: PaperResources) -> str:
    if not resources.pdfs:
        return ""
    rows = []
    for pdf in resources.pdfs:
        size = pdf.stat().st_size / (1024 * 1024)
        basis = f" · {resources.primary_basis}" if pdf == resources.primary_pdf else ""
        rows.append(
            f'<li><a href="{h(resources.url(pdf))}" download="{h(pdf.name)}" type="application/pdf">'
            f'{h(pdf.name)}</a><span class="muted"> PDF · {size:.2f} MiB{h(basis)}</span></li>'
        )
    note = resources.selection_issue
    if len(resources.pdfs) > 1:
        note = (note + " " if note else "") + "These files may be different versions or companion documents. The archive does not identify a latest edition."
    note_html = f'<p class="muted">{h(note)}</p>' if note else ""
    return f'''<section class="section" id="downloads" aria-labelledby="downloads-title">
            <div class="section-header"><h2 id="downloads-title">PDF downloads</h2><p>Archived files available directly from this site.</p><div class="section-divider"></div></div>
            <div class="work-detail"><ul class="download-list">{"".join(rows)}</ul>{note_html}</div>
        </section>'''


def render_work_page(work: dict) -> str:
    resources = resources_for(work)
    work = {**work, "_resources": resources}
    footer_stamp = footer_build_stamp_html()
    doi_link = f"https://doi.org/{work['doi']}" if work.get("doi") else ""
    primary = work.get("url") or doi_link
    actions = []
    if resources.primary_pdf:
        pdf = resources.primary_pdf
        actions.append(f'<a class="btn btn-gold" href="{h(resources.url(pdf))}" download="{h(pdf.name)}" type="application/pdf">Download PDF</a>')
    elif resources.pdfs:
        actions.append('<a class="btn btn-gold" href="#downloads">PDF downloads</a>')
    if primary:
        actions.append(f'<a class="btn btn-outline" href="{h(primary)}">Publication source</a>')
    if resources.github_url:
        actions.append(f'<a class="btn btn-outline" href="{h(resources.github_url)}">Paper folder on GitHub</a>')
    if resources.full_text:
        actions.append(f'<a class="btn btn-outline" href="{h(resources.url(resources.full_text))}">Read extracted text</a>')
    actions_html = '<div class="work-actions" role="group" aria-label="Read and download this work">' + "\n".join(actions) + '</div>' if actions else ""

    extras = []
    if resources.docs_url:
        extras.append(f'<a class="btn btn-outline" href="{h(resources.docs_url)}">Paper documentation</a>')
    if resources.images:
        extras.append(f'<a class="btn btn-outline" href="{h(resources.github_url + "/images")}">Figures on GitHub</a>')
    source_repo = source_repository_url(work.get("docs_path", ""), resources)
    if source_repo:
        extras.append(f'<a class="btn btn-outline" href="{h(source_repo)}">Associated software repository</a>')
    extras_html = '<div class="work-actions" role="group" aria-label="Documentation and related resources">' + "\n".join(extras) + '</div>' if extras else ""
    doi_value = f'<a href="{h(doi_link)}">{h(work["doi"])}</a>' if doi_link else "Not listed"
    meta_cards = [
        f'<div class="meta-card"><strong>Catalog row</strong><a href="../publications.html">{h(work["num"])}</a></div>',
        f'<div class="meta-card"><strong>Citation key</strong>{h(work["citation_key"])}</div>',
        f'<div class="meta-card"><strong>DOI</strong>{doi_value}</div>',
    ]
    platform_card = platform_availability_card(work)
    if platform_card:
        meta_cards.append(platform_card)
    meta_cards_html = "\n".join(meta_cards)
    enrich = work.get("enrichment", {})
    abstract = abstract_display_text(enrich.get("abstract", ""))
    keywords = enrich.get("keywords", [])
    findings = enrich.get("findings", [])
    methods = enrich.get("methods", [])
    concepts = enrich.get("concepts", [])
    detail_sections = ""
    if abstract or keywords:
        abstract_html = (
            "".join("<p>" + h(paragraph).replace("\n", "<br>") + "</p>" for paragraph in abstract.split("\n\n"))
            if abstract else "<p>An abstract is not available in this archive.</p>"
        )
        keyword_spans = "".join(f"<span>{h(k)}</span>" for k in keywords)
        keyword_row = f'<div class="keyword-row" aria-label="Keywords">{keyword_spans}</div>' if keywords else ""
        detail_sections += f'''
        <section class="section">
            <div class="section-header"><h2>Overview</h2><div class="section-divider"></div></div>
            <div class="work-detail">{abstract_html}{keyword_row}{abstract_source_html(enrich)}</div>
        </section>'''
    cards = []
    for heading, items in (("Findings and contributions", findings), ("Methods", methods), ("Key concepts", concepts)):
        if items:
            rows = "".join(f"<li>{h(item)}</li>" for item in items)
            cards.append(f'<div class="work-detail"><h3>{heading}</h3><ul>{rows}</ul></div>')
    if cards:
        sources = enrich.get("sources", {})
        source_links = []
        for source in dict.fromkeys(sources.get(field, "") for field in ("findings", "methods", "concepts")):
            if source:
                path = REPO_ROOT / source
                if path in resources.files:
                    label = {"metadata.json": "Paper metadata and evidence", "README.md": "Paper documentation", "SKILL.md": "Learning guide"}.get(path.name, "Summary source")
                    source_links.append(f'<a href="{h(resources.url(path))}">{label}</a>')
        if resources.full_text:
            source_links.append(f'<a href="{h(resources.url(resources.full_text))}">Extracted source text</a>')
        provenance = '<p class="summary-sources">Summary sources: ' + ' · '.join(source_links) + '.</p>' if source_links else ""
        detail_sections += f'''
        <section class="section section-alt">
            <div class="section-header"><h2>Methods and contributions</h2><p>Read the source for the full argument, qualifications, and evidence.</p><div class="section-divider"></div></div>
            <div class="work-summary-grid">{"".join(cards)}</div>{provenance}
        </section>'''
    citation_buttons = bibtex_button_html(work) + '\n<a class="btn btn-outline" href="../bibliography.bib" download>Download bibliography</a>'
    return (
        page_head(work)
        + f'''
{render_breadcrumb(breadcrumb_trail(work), depth=1)}
    <header class="work-hero">
        <p class="eyebrow">{h(work['domain_name'])} · {h(work['type'])} · {h(work['year'])}</p>
        <h1>{h(work['title'])}</h1>
{byline_html(work)}
        <p class="sub">{h(work.get('venue') or 'Curated bibliography entry')}</p>
{actions_html}
    </header>
    <main id="main" class="main">
{detail_sections}
{pdf_downloads_html(resources)}
        <section class="section section-alt">
            <div class="section-header"><h2>Citation</h2><p>Citation metadata follows the unified bibliography.</p><div class="section-divider"></div></div>
            <div class="cite-box">{h(citation_text(work))}</div>
            <div class="work-actions">{citation_buttons}</div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Catalog details and resources</h2><div class="section-divider"></div></div>
            <div class="meta-grid">{meta_cards_html}</div>{extras_html}
        </section>
{related_works_html(work)}
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="../publications.html">Unified bibliography</a> · <a href="../cite-verify.html">Cite &amp; Verify</a></p>
        {footer_stamp}
    </footer>
''' + INTERACTIVE_SCRIPTS + "\n" + CITE_EXPORT_SCRIPT_TAG + "\n" + MENU_ESC_SCRIPT + '''</body>
</html>
'''
    )


def render_index(works: list[dict]) -> str:
    years = sorted({int(str(w.get("year", "")).strip()[:4]) for w in works if str(w.get("year", "")).strip()[:4].isdigit()})
    min_year, max_year = (years[0], years[-1]) if years else ("", "")
    rows = "\n".join(
        f"""                <article class="work-row">
                    <div class="year">{h(w['year'])}</div>
                    <div><a href="{h(w['citation_key'])}.html">{h(w['title'])}</a><div class="venue">{h(w['domain_name'])} · {h(w['venue'])}</div></div>
                    <a href="{h(w.get('url') or '../publications.html')}">Source</a>
                </article>"""
        for w in sorted(works, key=lambda x: (int(x["year"]), -int(x["num"])), reverse=True)
    )
    item_list_elements = json.dumps(
        [
            {
                "@type": "ListItem",
                "position": index + 1,
                "url": f"https://danielarifriedman.com/works/{w['citation_key']}.html",
                "name": w["title"],
            }
            for index, w in enumerate(sorted(works, key=lambda x: (int(x["year"]), -int(x["num"])), reverse=True))
        ],
        ensure_ascii=False,
    ).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Works Index — Daniel Ari Friedman</title>
    <meta name="description" content="Browse {len(works)} per-work pages — the paper trail of a longitudinal thinking practice: papers, books, courses, and presentations across Active Inference, computational biology, cognitive security, entomology, and art, each with DOI, citation tools, and related works.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/works/">
    <link rel="stylesheet" href="../style.css?v=site-20261002b">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
{HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="Works Index — Daniel Ari Friedman">
    <meta property="og:description" content="Browse {len(works)} per-work pages — the paper trail of a longitudinal thinking practice: papers, books, courses, and presentations across Active Inference, computational biology, cognitive security, entomology, and art, each with DOI, citation tools, and related works.">
    <meta property="og:url" content="https://danielarifriedman.com/works/">
    <meta property="og:site_name" content="Daniel Ari Friedman">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Works Index — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Works Index — Daniel Ari Friedman">
    <meta name="twitter:description" content="Browse {len(works)} per-work pages — the paper trail of a longitudinal thinking practice: papers, books, courses, and presentations across Active Inference, computational biology, cognitive security, entomology, and art, each with DOI, citation tools, and related works.">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta name="twitter:image:alt" content="Works Index — Daniel Ari Friedman">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://danielarifriedman.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Works", "item": "https://danielarifriedman.com/works/" }}
      ]
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Daniel Ari Friedman Works Index",
      "numberOfItems": {len(works)},
      "url": "https://danielarifriedman.com/works/",
      "itemListElement": {item_list_elements}
    }}
    </script>
    <style>.work-list{{display:grid;gap:.75rem}}.work-row{{display:grid;grid-template-columns:4.5rem 1fr auto;gap:1rem;align-items:start;padding:.9rem 1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:8px}}.work-row .year{{color:var(--gold);font-weight:700}}.work-row .venue{{color:var(--text-muted);font-size:.8rem}}@media(max-width:760px){{.work-row{{grid-template-columns:1fr}}}}</style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=1)}
    <header class="page-hero"><h1>Works Index</h1><p class="sub">{len(works)} per-work pages — the paper trail of a thinking practice: versioned deposits from {min_year} to {max_year}, preserving beliefs held, positions updated, and wrong turns along the way.</p></header>
    <main id="main" class="main"><section class="section"><div class="work-list">
{rows}
    </div></section></main>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + """</body>
</html>
"""


def existing_generated_at(path: Path) -> str | None:
    content = read_generated_output_text(REPO_ROOT, path)
    if content is None:
        return None
    try:
        return json.loads(content).get("generated_at")
    except json.JSONDecodeError:
        return None


def render_outputs(generated_at: str | None = None) -> dict[Path, str]:
    visible = source_paths(REPO_ROOT)
    citations = load_bibtex_entries()
    works = [{**work, "_resources": PaperResources.load(REPO_ROOT, work.get("docs_path", ""), visible), "_bibtex": citations.get(work["citation_key"], "")} for work in load_works()]
    enrichments = enrichment_map(works, visible_paths=visible)
    works = [{**work, "enrichment": enrichments.get(work["citation_key"], {})} for work in works]
    by_domain: dict[str, list[dict]] = {}
    for w in works:
        by_domain.setdefault(w["domain"], []).append(w)
    for w in works:
        siblings = [s for s in by_domain.get(w["domain"], []) if s["citation_key"] != w["citation_key"]]
        siblings.sort(key=lambda x: (int(x["year"]), int(x["num"])), reverse=True)
        w["related"] = siblings[:6]
    outputs = {WORKS_DIR / "index.html": mark_generated_page(render_index(works))}
    html_outputs: list[Path] = [WORKS_DIR / "index.html"]
    # citation_key is the permanent public URL primitive (works/{key}.html). It must be
    # unique: two works mapping to the same key would silently overwrite one page (and its
    # canonical/JSON-LD @id). Fail loud here rather than ship a clobbered/missing work.
    seen_keys: dict[str, dict] = {}
    for work in works:
        key = work["citation_key"]
        if key in seen_keys:
            raise SystemExit(
                f"Duplicate work citation_key {key!r}: bibliography rows num "
                f"{seen_keys[key]['num']} and {work['num']} collide on works/{key}.html"
            )
        seen_keys[key] = work
        page_path = WORKS_DIR / f"{key}.html"
        outputs[page_path] = mark_generated_page(render_work_page(work))
        html_outputs.append(page_path)
    # Stamp-reuse (generated_at pattern): when a rendered page differs from the
    # on-disk page only by the footer build stamp, keep the on-disk stamp so
    # non-rendering commits do not churn (or stale-flag) every work page.
    for page_path in html_outputs:
        disk = read_generated_output_text(REPO_ROOT, page_path)
        if disk is not None:
            outputs[page_path] = reuse_on_disk_stamp(outputs[page_path], disk)
    outputs[ENRICHMENT_OUT] = json.dumps(
        {
            "generated_at": generated_at or generated_timestamp(),
            "source": "papers/paper_metadata.json, papers/*/metadata.json, README.md and SKILL.md",
            "count": len(enrichments),
            "works": enrichments,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"
    return outputs


def mark_generated_page(content: str) -> str:
    """Embed the ownership marker immediately after the HTML doctype."""
    prefix = "<!DOCTYPE html>\n"
    if not content.startswith(prefix):
        raise ValueError("generated work page must start with an HTML doctype")
    return prefix + GENERATED_PAGE_MARKER + "\n" + content.removeprefix(prefix)


def is_owned_generated_page(path: Path, *, repo_root: Path = REPO_ROOT) -> bool:
    """Return whether a work page explicitly authorizes renderer pruning."""
    content = read_generated_output_text(repo_root, path, errors="replace")
    return bool(content and content.startswith("<!DOCTYPE html>\n" + GENERATED_PAGE_MARKER + "\n"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    parser.add_argument(
        "--prune-owned",
        action="store_true",
        help="Remove only explicitly renderer-owned orphan work pages (destructive; requires an explicit manual invocation)",
    )
    args = parser.parse_args()
    if args.check and args.prune_owned:
        parser.error("--prune-owned cannot be combined with --check")
    generated_at = existing_generated_at(ENRICHMENT_OUT) if args.check else None
    if not args.check:
        candidate_outputs = render_outputs()
        generated_at = stable_generated_output_timestamp(
            REPO_ROOT,
            ENRICHMENT_OUT,
            json.loads(candidate_outputs[ENRICHMENT_OUT]),
        )
    outputs = render_outputs(generated_at)
    stale = [str(path.relative_to(REPO_ROOT)) for path in stale_output_paths(outputs, repo_root=REPO_ROOT)] if args.check else []
    if not args.check:
        write_output_texts(outputs, repo_root=REPO_ROOT)
    if args.check:
        expected = {
            safe_generated_output_path(REPO_ROOT, path)
            for path in outputs
            if path.parent == WORKS_DIR
        }
        extra = (
            {
                path
                for path in generated_output_files(REPO_ROOT, WORKS_DIR, "*.html")
                if is_owned_generated_page(path, repo_root=REPO_ROOT)
            }
            - expected
        )
        stale.extend(str(p.relative_to(REPO_ROOT)) for p in sorted(extra))
    elif args.prune_owned:
        expected = {
            safe_generated_output_path(REPO_ROOT, path)
            for path in outputs
            if path.parent == WORKS_DIR
        }
        owned_orphans = [
            path
            for path in generated_output_files(REPO_ROOT, WORKS_DIR, "*.html")
            if path not in expected and is_owned_generated_page(path, repo_root=REPO_ROOT)
        ]
        for path in owned_orphans:
            remove_generated_output(REPO_ROOT, path)
    if stale:
        raise SystemExit("Stale generated work pages: " + ", ".join(stale[:20]))
    action = "checked" if args.check else "wrote"
    suffix = " (pruned explicitly owned orphans)" if args.prune_owned else ""
    print(f"{action} {len(outputs)} work pages{suffix}")


if __name__ == "__main__":
    main()
