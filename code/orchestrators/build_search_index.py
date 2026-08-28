#!/usr/bin/env python3
"""Build a lightweight site-wide JSON search index."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
OUT = REPO_ROOT / "search-index.json"

# Split-index companions (search-index.json remains the complete, valid,
# backward-compatible surface for every existing consumer).  The core file is
# the full item set minus the heavy ``content`` fields, so a lazy client can
# paint from ~0.5 MB and fetch content segments only for the type being
# searched.  Only the two heavy types (work, video) ship content segments;
# every other type's content is small enough to stay negligible in the core.
CORE_OUT = REPO_ROOT / "search-index-core.json"
CONTENT_SEGMENT_TYPES = ("work", "video")


def content_segment_path(item_type: str) -> Path:
    return REPO_ROOT / f"search-index-content-{item_type}.json"

try:
    from report_paths import generated_timestamp, latest_source_report, latest_source_subdir_file, rel, stable_generated_at
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_source_report, latest_source_subdir_file, rel, stable_generated_at


def _latest_url(pattern: str, _fallback: str) -> str:
    try:
        return "/" + rel(latest_source_report(pattern))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"build_search_index: no report matches {pattern!r}; refusing a stale fallback link"
        ) from None


def _latest_subdir_url(prefix: str, filename: str, _fallback: str) -> str:
    try:
        latest = latest_source_subdir_file(prefix, filename)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"build_search_index: no {prefix} report dir {filename!r}; refusing a stale fallback link"
        ) from None
    return "/" + rel(latest)


def static_pages() -> list[tuple[str, str, str, str, str, list[str]]]:
    reconciliation = _latest_url("reconciliation_*.md", "/reports/reconciliation_2026-05-15.md")
    public_source_inventory = _latest_url(
        "public_source_inventory_*.json", "/reports/public_source_inventory_2026-05-15.json"
    )
    accessibility = _latest_url("accessibility_static_*.json", "/reports/accessibility_static_2026-05-13.json")
    visual_qa = _latest_subdir_url("visual-qa", "manifest.json", "/reports/visual-qa/2026-05-13/manifest.json")
    external_links = _latest_url("external_links_[0-9]*.json", "/reports/external_links_2026-05-13.json")
    external_link_triage = _latest_url(
        "external_links_triage_*.md", "/reports/external_links_triage_2026-05-13.md"
    )
    asset_size = _latest_url("asset_size_*.json", "/reports/asset_size_2026-05-13.json")
    browser_smoke = _latest_subdir_url(
        "browser-smoke", "manifest.json", "/reports/browser-smoke/2026-05-13/manifest.json"
    )
    live_site = _latest_url("live_site_verification_*.json", "/reports/live_site_verification_2026-05-13.json")
    return [
    ("home", "page", "Daniel Ari Friedman", "/", "Homepage and professional profile.", ["homepage", "profile"]),
    ("publications", "page", "Publications", "/publications.html", "Searchable bibliography of Active Inference, biology, cognitive security, art, and computational works.", ["bibliography", "papers", "active inference"]),
    ("works", "page", "Works Index", "/works/", "Generated per-work bibliography pages.", ["works", "citations"]),
    ("domains", "page", "Research Domains", "/domains.html", "Domain landing pages and learning paths.", ["domains"]),
    ("software", "page", "Software", "/software.html", "Owned and AII software repositories.", ["software", "github"]),
    ("repositories", "page", "Primary GitHub Repositories", "/repositories.html", "Search non-fork public docxology and Active Inference Institute repositories by topic, language, owner, and curation status.", ["software", "github", "inventory", "active inference"]),
    ("repositories-forks", "page", "Forked GitHub Repositories", "/repositories-forks.html", "Separated archive of forked public docxology and Active Inference Institute repositories.", ["software", "github", "inventory", "forks"]),
    ("videos", "page", "Videos", "/videos.html", "Timeline of Active Inference talks, research livestreams, courses, interviews, and public video sessions.", ["videos", "active inference", "talks", "youtube"]),
    ("search", "page", "Search", "/search.html", "Human-facing search over works, software, pages, people, organizations, and claims.", ["search"]),
    ("catalog", "page", "Data Catalog", "/catalog.html", "Structured DataCatalog for public JSON exports.", ["catalog", "structured data"]),
    ("exports", "page", "Public Exports", "/exports.html", "HTML index of citation exports and JSON datasets.", ["exports", "citation", "bibtex"]),
    ("updates", "page", "Updates", "/updates.html", "Human-readable changelog for the public research and discovery index.", ["updates", "changelog"]),
    ("discovery", "page", "Discovery Map", "/discovery.html", "Canonical identifiers and public source queries.", ["agents"]),
    ("cognitive-security-pillar", "page", "What Is Cognitive Security?", "/cognitive-security.html", "Foundational guide to cognitive security, threat modeling, narrative ecosystems, and multi-agent defense.", ["cognitive security", "epistemic security", "misinformation", "active inference"]),
    ("computational-entomology-pillar", "page", "Computational Entomology", "/computational-entomology.html", "Computational models of social insects, algorithmic entomology, ant colony simulation, and transcriptomics.", ["computational entomology", "ants", "collective behavior", "simulation"]),
    ("insect-cognition-pillar", "page", "Insect Cognition & Collective Intelligence", "/insect-cognition.html", "Explainer on insect cognition, ant colony intelligence without a central brain, stigmergy, and active inference.", ["insect cognition", "ant intelligence", "stigmergy", "superorganism"]),
    ("active-inference-pillar", "page", "Active Inference & Free Energy Principle Guide", "/active-inference.html", "Comprehensive tutorial and guide to Active Inference, generative models, expected free energy, and belief updating.", ["active inference", "free energy principle", "bayesian mechanics", "generative models"]),
    ("neurosymbolic-ai-pillar", "page", "Neurosymbolic AI & Active Inference", "/neurosymbolic-ai.html", "Guide to neurosymbolic artificial intelligence, formal knowledge representations, and discrete active inference agents.", ["neurosymbolic ai", "symbolic reasoning", "generative ai", "knowledge graphs"]),
    ("cite-verify", "page", "Cite & Verify", "/cite-verify.html", "Citation and source-of-truth rules.", ["citation"]),
    ("evidence", "page", "Evidence Ledger", "/evidence.html", "Claim-level evidence and caveats.", ["claims"]),
    ("reproducibility", "page", "Reproducibility Ledger", "/reproducibility.html", "Per-work artifact availability across the curated bibliography.", ["reproducibility", "open science", "verification"]),
    ("resume", "document", "Resume and CV", "/resume/resume.html", "Accessible, no-JavaScript HTML CV with PDF, plaintext, JSON, and verification links.", ["resume", "cv", "accessibility"]),
    ("resume-verify", "page", "Resume Verification", "/resume/verify.html", "Hashes, source manifest, file sizes, QR target, and artifact links for the generated structured CV.", ["resume", "cv", "verification", "hashes"]),
    ("collaborators", "page", "Collaborators", "/collaborators.html", "Research collaborator network.", ["people"]),
    ("media", "page", "Media", "/media.html", "Talks, podcasts, videos, and press.", ["media"]),
    ("art", "page", "Art", "/art.html", "Visual art and Curio Cards work.", ["art"]),
    ("changelog", "document", "Changelog", "/CHANGELOG.md", "Public-index and generated-site change history.", ["maintenance"]),
    ("redirects", "document", "Redirect And Canonical Policy", "/docs/seo/canonical-policy.md", "Canonical URL and redirect-stub rules.", ["canonical", "seo"]),
    ("reconciliation", "report", "Public-Source Reconciliation Report", reconciliation, "Curated local counts compared with public source indexes.", ["evidence", "reports"]),
    ("public-source-inventory", "report", "Public Source Inventory", public_source_inventory, "Paginated public-source inventory for source discovery and claim auditing.", ["evidence", "public sources", "reports"]),
    ("accessibility", "report", "Static Accessibility Report", accessibility, "Static accessibility and metadata audit output.", ["accessibility", "reports"]),
    ("visual-qa", "report", "Visual QA Manifest", visual_qa, "Desktop and mobile Playwright screenshots for key pages.", ["visual", "qa"]),
    ("external-links", "report", "External Link Report", external_links, "Cached network check over site-critical external links.", ["links", "reports"]),
    ("external-link-triage", "report", "External Link Triage", external_link_triage, "Categorized warning report for scoped external links.", ["links", "triage", "reports"]),
    ("asset-size", "report", "Asset Size Audit", asset_size, "Size report for public HTML, Open Graph images, data exports, and runtime assets.", ["assets", "performance", "reports"]),
    ("browser-smoke", "report", "Browser Smoke Manifest", browser_smoke, "Selector-based browser smoke checks for core local pages.", ["browser", "qa", "reports"]),
    ("live-site", "report", "Live Site Verification", live_site, "Deployed-site status, expected markers, and GitHub Pages build state.", ["deploy", "live", "reports"]),
    ("generated", "document", "Generated Files", "/GENERATED.md", "Generated artifact manifest and rebuild commands.", ["generated", "maintenance"]),
    ("agent-start", "document", "Agent Start Guide", "/AGENT_START.md", "Task recipes for agents using the repository.", ["agents", "start"]),
    ("humans", "document", "Humans.txt", "/humans.txt", "Human-maintained contact and site credits.", ["contact", "humans"]),
    ("release-snapshot", "document", "2026-05 Discovery Layer Release Snapshot", "/docs/releases/2026-05-discovery-layer.md", "Release note and validation gate for the discovery layer.", ["release", "maintenance"]),
    ]


def existing_generated_at() -> str | None:
    if not OUT.exists():
        return None
    try:
        return json.loads(OUT.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def load_json(rel: str) -> dict:
    with open(REPO_ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def work_item(work: dict, enrichments: dict[str, dict]) -> dict:
    enrich = enrichments.get(work["citation_key"], {})
    keywords = enrich.get("keywords", [])
    abstract = enrich.get("abstract", "")
    docs_path = str(work.get("docs_path") or "").rstrip("/")
    full_text_path = REPO_ROOT / docs_path / "full_text.md" if docs_path else None
    full_text_url = f"/{docs_path}/full_text.md" if full_text_path and full_text_path.exists() else ""
    images_dir = REPO_ROOT / docs_path / "images" if docs_path else None
    image_count = 0
    if images_dir and images_dir.is_dir():
        image_count = sum(
            1 for f in images_dir.iterdir()
            if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif")
        )
    result = {
        "id": f"work:{work['citation_key']}",
        "type": "work",
        "title": work["title"],
        "url": f"/works/{work['citation_key']}.html",
        "external_url": work.get("url", ""),
        "full_text_url": full_text_url,
        "summary": abstract[:220] if abstract else f"{work['type']} · {work['venue']} · {work['domain_name']}",
        "year": work["year"],
        "domain": work["domain_name"],
        "tags": [work["type"], work["domain_name"], "bibliography", *keywords[:8]],
        "content": " ".join(
            str(part)
            for part in [
                work["title"],
                # Both orders, so "Smékal" and "Jakub Smékal" both match.
                " ".join(work.get("authors", [])),
                " ".join(
                    name.partition(",")[2].strip() + " " + name.partition(",")[0].strip()
                    for name in work.get("authors", [])
                    if "," in name
                ),
                work.get("venue", ""),
                work.get("doi", ""),
                work.get("citation_key", ""),
                work["domain_name"],
                work["type"],
                abstract,
                " ".join(keywords),
                " ".join(enrich.get("findings", [])),
                " ".join(enrich.get("methods", [])),
            ]
            if part
        ),
    }
    if image_count:
        result["image_count"] = image_count
    return result


def software_item(repo: dict) -> dict:
    return {
        "id": f"software:{repo['owner']}:{repo['name']}",
        "type": "software",
        "title": repo["name"],
        "url": repo["url"],
        "summary": repo["description"],
        "domain": repo["catalog_section"],
        "tags": ["software", repo.get("language", ""), repo["owner"]],
        "content": " ".join([repo["name"], repo["description"], repo.get("language", ""), repo["owner"]]).strip(),
    }


def github_repo_item(repo: dict) -> dict:
    flags = []
    if repo.get("curated"):
        flags.append("curated")
    if repo.get("fork"):
        flags.append("fork")
    if repo.get("archived"):
        flags.append("archived")
    if repo.get("recently_updated"):
        flags.append("recent")
    return {
        "id": f"github-repo:{repo['full_name']}",
        "type": "github_repository",
        "title": repo["full_name"],
        "url": repo["html_url"],
        "summary": repo.get("description", "") or f"{repo['owner']} repository",
        "domain": repo["owner"],
        "tags": ["github", "repository", repo.get("language", ""), repo["owner"], *flags],
        "content": " ".join(
            [
                repo["full_name"],
                repo.get("description", ""),
                repo.get("language", ""),
                repo["owner"],
                " ".join(repo.get("topics", [])),
                " ".join(flags),
            ]
        ).strip(),
    }


def video_item(video: dict) -> dict:
    topics = [topic["label"] for topic in video.get("topics", [])]
    related_works = [work["title"] for work in video.get("related_works", [])]
    return {
        "id": f"video:{video['channel']}:{video['id']}",
        "type": "video",
        "title": video["title"],
        "url": video["page_url"],
        "external_url": video["youtube_url"],
        "summary": (
            f"{video['channel_label']} video from {video['date']}"
            + (f" · {', '.join(topics[:3])}" if topics else "")
        ),
        "year": video["year"],
        "domain": video["channel_label"],
        "tags": ["video", "youtube", video["channel"], *topics],
        "content": " ".join(
            [
                video["title"],
                video["channel_label"],
                video["date"],
                " ".join(topics),
                " ".join(related_works),
                video.get("transcript_excerpt", ""),
            ]
        ).strip(),
    }


def person_item(person: dict) -> dict:
    return {
        "id": f"person:{person['name']}",
        "type": "person",
        "title": person["name"],
        "url": person.get("homepage") or person.get("source") or "",
        "summary": person.get("role", ""),
        "tags": ["person", "collaborator"],
        "content": " ".join(str(v) for v in person.values() if isinstance(v, str)),
    }


def org_item(org: dict) -> dict:
    return {
        "id": f"organization:{org['name']}",
        "type": "organization",
        "title": org["name"],
        "url": org.get("url", ""),
        "summary": org.get("role", ""),
        "tags": ["organization"],
        "content": " ".join(str(v) for v in org.values() if isinstance(v, str)),
    }


def claim_item(claim: dict) -> dict:
    return {
        "id": f"claim:{claim['id']}",
        "type": "claim",
        "title": claim["claim"],
        "url": "/evidence.html",
        "summary": f"{claim['status']} · confidence: {claim['confidence']}",
        "tags": ["claim", claim["status"], claim["confidence"]],
        "content": " ".join([claim["claim"], claim.get("caveat", ""), claim.get("verification_method", "")]),
    }


def resume_item(resume: dict) -> dict:
    profile = resume["profile"]
    contact = resume["contact"]
    metrics = resume["metrics"]
    section_text = " ".join(
        str(part)
        for part in [
            profile.get("summary", ""),
            " ".join(contact.get("email", [])),
            " ".join(item.get("workplace", "") for item in resume.get("experience", [])),
            " ".join(item.get("institution", "") for item in resume.get("education", [])),
            " ".join(item.get("name", "") for item in resume.get("media_outreach", [])),
            " ".join(item.get("description", "") for item in resume.get("service", [])),
        ]
        if part
    )
    return {
        "id": "resume:structured-cv",
        "type": "resume",
        "title": f"{profile['name']} Resume / CV",
        "url": "/resume/resume.html",
        "summary": (
            f"Structured CV export: {metrics['works']} works, "
            f"{metrics['software_catalogued']} software rows, {metrics['github_inventory']['public']} public GitHub repositories, education, experience, service, media, and art-use records."
        ),
        "tags": ["resume", "cv", "profile", "html", "plaintext", "pdf", "accessibility", "verification"],
        "content": " ".join([profile["name"], profile["headline"], section_text]).strip(),
    }


def _compact(value: object) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False) + "\n"


def render_split(generated_at: str | None = None) -> dict[Path, str]:
    """Render the core + per-type content-segment companions of the main index.

    The main ``search-index.json`` keeps every field for existing consumers;
    these files exist so a progressive client can defer the ~1 MB of video and
    work ``content`` text until a query actually needs it.
    """
    content = json.loads(render(generated_at))
    core_items = []
    segments: dict[str, list[dict]] = {typ: [] for typ in CONTENT_SEGMENT_TYPES}
    for item in content["items"]:
        if item["type"] in segments:
            segments[item["type"]].append(item)
        core_items.append({key: value for key, value in item.items() if key != "content"})
    outputs = {
        CORE_OUT: _compact(
            {
                "generated_at": content["generated_at"],
                "source_files": content["source_files"],
                "count": content["count"],
                "note": (
                    "Companion of search-index.json without item content; "
                    "fetch search-index-content-<type>.json segments for full-text fields."
                ),
                "content_segments": list(CONTENT_SEGMENT_TYPES),
                "items": core_items,
            }
        )
    }
    for typ, items in segments.items():
        outputs[content_segment_path(typ)] = _compact(
            {
                "generated_at": content["generated_at"],
                "type": typ,
                "count": len(items),
                "items": items,
            }
        )
    return outputs


def render(generated_at: str | None = None) -> str:
    works = load_json("data/works.json")["works"]
    enrichments = load_json("data/work-enrichment.json").get("works", {})
    software = load_json("data/software.json")["repositories"]
    github_repositories = load_json("data/github-repositories.json")["repositories"]
    videos = load_json("data/videos.json")["videos"]
    people = load_json("data/people.json")["people"]
    orgs = load_json("data/organizations.json")["organizations"]
    claims = load_json("data/claims.json")["claims"]
    resume = load_json("data/resume.json")
    items: list[dict] = []
    for page in static_pages():
        id_, typ, title, url, summary, tags = page
        items.append({"id": f"page:{id_}", "type": typ, "title": title, "url": url, "summary": summary, "tags": tags, "content": " ".join([title, summary, *tags])})
    items.extend(work_item(work, enrichments) for work in works)
    items.extend(software_item(repo) for repo in software)
    items.extend(github_repo_item(repo) for repo in github_repositories if not repo.get("fork"))
    items.extend(video_item(video) for video in videos)
    items.extend(person_item(person) for person in people)
    items.extend(org_item(org) for org in orgs)
    items.extend(claim_item(claim) for claim in claims)
    items.append(resume_item(resume))
    payload = {
        "generated_at": generated_at or generated_timestamp(),
        "source_files": [
            "data/works.json",
            "data/work-enrichment.json",
            "data/software.json",
            "data/github-repositories.json",
            "data/videos.json",
            "data/people.json",
            "data/organizations.json",
            "data/claims.json",
            "data/resume.json",
        ],
        "count": len(items),
        "items": items,
    }
    return _compact(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if search-index.json is stale")
    args = parser.parse_args()
    generated_at = existing_generated_at() if args.check else None
    if not args.check:
        candidate = json.loads(render())
        generated_at = stable_generated_at(OUT, candidate)
    content = render(generated_at)
    outputs = {OUT: content}
    outputs.update(render_split(generated_at))
    if args.check:
        stale = [
            path.relative_to(REPO_ROOT).as_posix()
            for path, expected in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != expected
        ]
        if stale:
            raise SystemExit("Stale generated search index surfaces: " + ", ".join(stale))
    else:
        for path, text in outputs.items():
            path.write_text(text, encoding="utf-8")
    print(("checked" if args.check else "wrote") + f" search-index.json (+{len(outputs) - 1} split surfaces)")


if __name__ == "__main__":
    main()
