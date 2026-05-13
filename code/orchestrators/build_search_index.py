#!/usr/bin/env python3
"""Build a lightweight site-wide JSON search index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "search-index.json"


STATIC_PAGES = [
    ("home", "page", "Daniel Ari Friedman", "/", "Homepage and professional profile.", ["homepage", "profile"]),
    ("publications", "page", "Publications", "/publications.html", "Unified bibliography table.", ["bibliography", "papers"]),
    ("works", "page", "Works Index", "/works/", "Generated per-work bibliography pages.", ["works", "citations"]),
    ("domains", "page", "Research Domains", "/domains.html", "Domain landing pages and learning paths.", ["domains"]),
    ("software", "page", "Software", "/software.html", "Owned and AII software repositories.", ["software", "github"]),
    ("search", "page", "Search", "/search.html", "Human-facing search over works, software, pages, people, organizations, and claims.", ["search"]),
    ("catalog", "page", "Data Catalog", "/catalog.html", "Structured DataCatalog for public JSON exports.", ["catalog", "structured data"]),
    ("discovery", "page", "Discovery Map", "/discovery.html", "Canonical identifiers and public source queries.", ["agents"]),
    ("cite-verify", "page", "Cite & Verify", "/cite-verify.html", "Citation and source-of-truth rules.", ["citation"]),
    ("evidence", "page", "Evidence Ledger", "/evidence.html", "Claim-level evidence and caveats.", ["claims"]),
    ("collaborators", "page", "Collaborators", "/collaborators.html", "Research collaborator network.", ["people"]),
    ("media", "page", "Media", "/media.html", "Talks, podcasts, videos, and press.", ["media"]),
    ("art", "page", "Art", "/art.html", "Visual art and Curio Cards work.", ["art"]),
    ("changelog", "document", "Changelog", "/CHANGELOG.md", "Public-index and generated-site change history.", ["maintenance"]),
    ("redirects", "document", "Redirect And Canonical Policy", "/docs/REDIRECTS.md", "Canonical URL and redirect-stub rules.", ["canonical", "seo"]),
    ("reconciliation", "report", "Public-Source Reconciliation Report", "/reports/reconciliation_2026-05-13.md", "Curated local counts compared with public source indexes.", ["evidence", "reports"]),
    ("accessibility", "report", "Static Accessibility Report", "/reports/accessibility_static_2026-05-13.json", "Static accessibility and metadata audit output.", ["accessibility", "reports"]),
    ("visual-qa", "report", "Visual QA Manifest", "/reports/visual-qa/2026-05-13/manifest.json", "Desktop and mobile Playwright screenshots for key pages.", ["visual", "qa"]),
    ("external-links", "report", "External Link Report", "/reports/external_links_2026-05-13.json", "Cached network check over site-critical external links.", ["links", "reports"]),
    ("generated", "document", "Generated Files", "/GENERATED.md", "Generated artifact manifest and rebuild commands.", ["generated", "maintenance"]),
    ("release-snapshot", "document", "2026-05 Discovery Layer Release Snapshot", "/docs/RELEASE_2026-05_DISCOVERY_LAYER.md", "Release note and validation gate for the discovery layer.", ["release", "maintenance"]),
]


def load_json(rel: str) -> dict:
    with open(REPO_ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def work_item(work: dict, enrichments: dict[str, dict]) -> dict:
    enrich = enrichments.get(work["citation_key"], {})
    keywords = enrich.get("keywords", [])
    abstract = enrich.get("abstract", "")
    return {
        "id": f"work:{work['citation_key']}",
        "type": "work",
        "title": work["title"],
        "url": f"/works/{work['citation_key']}.html",
        "external_url": work.get("url", ""),
        "summary": abstract[:220] if abstract else f"{work['type']} · {work['venue']} · {work['domain_name']}",
        "year": work["year"],
        "domain": work["domain_name"],
        "tags": [work["type"], work["domain_name"], "bibliography", *keywords[:8]],
        "content": " ".join(
            str(part)
            for part in [
                work["title"],
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


def render() -> str:
    works = load_json("data/works.json")["works"]
    enrichments = load_json("data/work-enrichment.json").get("works", {})
    software = load_json("data/software.json")["repositories"]
    people = load_json("data/people.json")["people"]
    orgs = load_json("data/organizations.json")["organizations"]
    claims = load_json("data/claims.json")["claims"]
    items: list[dict] = []
    for page in STATIC_PAGES:
        id_, typ, title, url, summary, tags = page
        items.append({"id": f"page:{id_}", "type": typ, "title": title, "url": url, "summary": summary, "tags": tags, "content": " ".join([title, summary, *tags])})
    items.extend(work_item(work, enrichments) for work in works)
    items.extend(software_item(repo) for repo in software)
    items.extend(person_item(person) for person in people)
    items.extend(org_item(org) for org in orgs)
    items.extend(claim_item(claim) for claim in claims)
    payload = {
        "generated_at": "2026-05-13",
        "source_files": [
            "data/works.json",
            "data/work-enrichment.json",
            "data/software.json",
            "data/people.json",
            "data/organizations.json",
            "data/claims.json",
        ],
        "count": len(items),
        "items": items,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if search-index.json is stale")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated search-index.json")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " search-index.json")


if __name__ == "__main__":
    main()
