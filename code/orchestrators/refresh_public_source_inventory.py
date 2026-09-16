#!/usr/bin/env python3
"""Write a paginated public-source inventory report for discovery auditing."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCID = "0000-0001-6232-9096"
USER_AGENT = "docxology-public-source-inventory/1.0 (+https://danielarifriedman.com/)"

from docxology_tools.report_paths import latest_report, source_commit  # noqa: E402


def latest_output_path(date: str | None = None) -> Path:
    report_date = date or dt.datetime.now(dt.timezone.utc).date().isoformat()
    return REPO_ROOT / "reports" / f"public_source_inventory_{report_date}.json"


def fetch_json(url: str, timeout: int = 30, accept: str = "application/json") -> dict[str, Any]:
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def safe(label: str, url: str, extractor) -> dict[str, Any]:
    try:
        data = fetch_json(url)
        return {"label": label, "url": url, "ok": True, "items": extractor(data)}
    except Exception as exc:  # pragma: no cover - network failures are report data
        return {"label": label, "url": url, "ok": False, "error": f"{type(exc).__name__}: {exc}", "items": []}


def orcid_works() -> dict[str, Any]:
    url = f"https://pub.orcid.org/v3.0/{ORCID}/works"

    def extract(data: dict[str, Any]) -> list[dict[str, Any]]:
        rows = []
        for group in data.get("group", []):
            summary = (group.get("work-summary") or [{}])[0]
            rows.append(
                {
                    "title": (((summary.get("title") or {}).get("title") or {}).get("value")),
                    "year": (((summary.get("publication-date") or {}).get("year") or {}).get("value")),
                    "type": summary.get("type"),
                    "source": ((summary.get("source") or {}).get("source-name") or {}).get("value"),
                    "path": summary.get("path"),
                }
            )
        return rows

    return safe("ORCID work groups", url, extract)


def crossref_orcid() -> dict[str, Any]:
    url = f"https://api.crossref.org/works?filter=orcid:{ORCID}&rows=100"

    def extract(data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "title": (item.get("title") or [""])[0],
                "doi": item.get("DOI", ""),
                "published": item.get("published-print") or item.get("published-online") or item.get("issued"),
                "container": (item.get("container-title") or [""])[0],
                "type": item.get("type", ""),
            }
            for item in data.get("message", {}).get("items", [])
        ]

    return safe("Crossref ORCID DOI records", url, extract)


def pubmed_exact_author() -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {"db": "pubmed", "term": "Daniel Ari Friedman[Author]", "retmode": "json", "retmax": 100}
    )
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{query}"
    return safe("PubMed exact author records", url, lambda data: data.get("esearchresult", {}).get("idlist", []))


def europe_pmc_exact_author() -> dict[str, Any]:
    query = urllib.parse.urlencode({"query": 'AUTH:"Daniel Ari Friedman"', "format": "json", "pageSize": 100})
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{query}"

    def extract(data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "title": item.get("title", ""),
                "journal": item.get("journalTitle", ""),
                "year": item.get("pubYear", ""),
                "doi": item.get("doi", ""),
                "pmid": item.get("pmid", ""),
                "source": item.get("source", ""),
            }
            for item in data.get("resultList", {}).get("result", [])
        ]

    return safe("Europe PMC exact author records", url, extract)


def zenodo_records(label: str, q: str) -> dict[str, Any]:
    base_params = {"q": q, "size": 25, "sort": "mostrecent"}
    first_url = "https://zenodo.org/api/records?" + urllib.parse.urlencode(base_params)
    rows: list[dict[str, Any]] = []
    total = None
    try:
        for page in range(1, 11):
            params = {**base_params, "page": page}
            url = "https://zenodo.org/api/records?" + urllib.parse.urlencode(params)
            data = fetch_json(url)
            hits = data.get("hits", {})
            total_value = hits.get("total")
            if isinstance(total_value, dict):
                total = total_value.get("value")
            elif total_value is not None:
                total = total_value
            batch = hits.get("hits", [])
            if not batch:
                break
            for hit in batch:
                meta = hit.get("metadata", {})
                rows.append(
                    {
                        "title": meta.get("title", ""),
                        "doi": hit.get("doi", ""),
                        "publication_date": meta.get("publication_date", ""),
                        "resource_type": (meta.get("resource_type") or {}).get("type", ""),
                        "version": meta.get("version", ""),
                    }
                )
            if total is not None and len(rows) >= int(total):
                break
        return {"label": label, "url": first_url, "ok": True, "items": rows, "total": total}
    except Exception as exc:  # pragma: no cover - network failures are report data
        return {"label": label, "url": first_url, "ok": False, "error": f"{type(exc).__name__}: {exc}", "items": []}


def wikidata_person() -> dict[str, Any]:
    url = "https://www.wikidata.org/wiki/Special:EntityData/Q138781444.json"

    def extract(data: dict[str, Any]) -> list[dict[str, Any]]:
        entity = data.get("entities", {}).get("Q138781444", {})
        claims = entity.get("claims", {})
        return [
            {
                "id": "Q138781444",
                "label": (entity.get("labels", {}).get("en") or {}).get("value", ""),
                "description": (entity.get("descriptions", {}).get("en") or {}).get("value", ""),
                "orcid": (((claims.get("P496") or [{}])[0].get("mainsnak") or {}).get("datavalue") or {}).get("value"),
                "website": (((claims.get("P856") or [{}])[0].get("mainsnak") or {}).get("datavalue") or {}).get("value"),
            }
        ]

    return safe("Wikidata person entity", url, extract)


def semantic_scholar_author_search() -> dict[str, Any]:
    return public_page(
        "https://www.semanticscholar.org/search?q=%22Daniel%20Ari%20Friedman%22&sort=relevance",
        "Semantic Scholar exact-name search",
    )


def dblp_author_profile() -> dict[str, Any]:
    return public_page("https://dblp.org/pid/346/2173.html", "DBLP author profile")


def researchgate_profile() -> dict[str, Any]:
    return public_page("https://www.researchgate.net/profile/Daniel-Friedman-2", "ResearchGate profile")


def sciprofiles_profile() -> dict[str, Any]:
    return public_page("https://sciprofiles.com/profile/447575", "SciProfiles profile")


def philpeople_profile() -> dict[str, Any]:
    return public_page("https://philpeople.org/profiles/daniel-ari-friedman", "PhilPeople profile")


def openalex_author_advisory() -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "search": "Daniel Ari Friedman",
            "per-page": 20,
        }
    )
    url = f"https://api.openalex.org/authors?{query}"

    def extract(data: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "id": item.get("id"),
                "name": item.get("display_name"),
                "works_count": item.get("works_count"),
                "h_index": item.get("summary_stats", {}).get("h_index"),
            }
            for item in data.get("results", [])
        ]

    return safe("OpenAlex author advisory search (low-confidence)", url, extract)


def github_profile(owner: str) -> dict[str, Any]:
    url = f"https://api.github.com/users/{owner}"
    return safe(
        f"GitHub profile {owner}",
        url,
        lambda data: [
            {
                "login": data.get("login", owner),
                "public_repos": data.get("public_repos", 0),
                "html_url": data.get("html_url", ""),
                "updated_at": data.get("updated_at", ""),
            }
        ],
    )


def public_page(url: str, label: str) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            text = response.read(200_000).decode("utf-8", errors="replace")
        title = ""
        start = text.lower().find("<title>")
        end = text.lower().find("</title>")
        if start >= 0 and end > start:
            title = text[start + 7 : end].strip()
        return {"label": label, "url": url, "ok": True, "items": [{"status": response.status, "title": title}]}
    except Exception as exc:  # pragma: no cover
        return {"label": label, "url": url, "ok": False, "error": f"{type(exc).__name__}: {exc}", "items": []}




def load_cached_sections(today: str, *, force: bool = False) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Reuse a same-day inventory report's section payloads instead of re-fetching.

    Reuse requires a same-day ``public_source_inventory_*.json`` (keyed on its
    ``generated_at`` date) whose sections carry no warnings (every section ok).
    When the optional same-day ``public_source_snapshot_*.json`` exists, its
    ``generated_at`` must also be same-day. ANY violation falls back to a live
    fetch; with ``force``, a stale or warned cache is reused as-is (an explicit
    "accept the cache anyway" escape), and a missing/unreadable cache simply
    falls back to a live fetch.
    """
    inventory_path = latest_report("public_source_inventory_*.json", required=False)
    if inventory_path is None:
        return [], None
    try:
        payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], None
    generated_at = payload.get("generated_at", "")
    sections = payload.get("sections")
    if not isinstance(sections, list) or not generated_at:
        return [], None
    same_day = generated_at[:10] == today
    warnings = [section.get("label") for section in sections if isinstance(section, dict) and not section.get("ok")]
    if not same_day or warnings:
        if force:
            return sections, {
                "mode": "forced-reuse",
                "source_report": str(inventory_path.relative_to(REPO_ROOT)),
                "source_generated_at": generated_at,
                "warnings_accepted": warnings,
            }
        return [], None
    anchor = {
        "mode": "cache-reuse",
        "source_report": str(inventory_path.relative_to(REPO_ROOT)),
        "source_generated_at": generated_at,
        "cached_section_labels": [s["label"] for s in sections if isinstance(s, dict)],
        "live_section_labels": [],
    }
    snapshot_path = latest_report("public_source_snapshot_*.json", required=False)
    if snapshot_path is not None:
        try:
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            snapshot_at = snapshot.get("generated_at", "")
            if snapshot_at[:10] != today:
                return [], None
            anchor["source_snapshot"] = str(snapshot_path.relative_to(REPO_ROOT))
            anchor["source_snapshot_generated_at"] = snapshot_at
        except (OSError, json.JSONDecodeError):
            return [], None
    return sections, anchor


def build_report(*, cache_reports: bool = False, force: bool = False) -> dict[str, Any]:
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    cached_sections, anchor = (
        load_cached_sections(today, force=force) if cache_reports else ([], None)
    )
    if cached_sections:
        sections = cached_sections
    else:
        sections = [
            orcid_works(),
            crossref_orcid(),
            pubmed_exact_author(),
            europe_pmc_exact_author(),
            zenodo_records("Zenodo exact-name creator records", 'metadata.creators.person_or_org.name:"Friedman, Daniel Ari"'),
            zenodo_records(
                "Zenodo ORCID-linked records",
                f'metadata.creators.person_or_org.identifiers.identifier:"{ORCID}"',
            ),
            wikidata_person(),
            dblp_author_profile(),
            researchgate_profile(),
            sciprofiles_profile(),
            philpeople_profile(),
            semantic_scholar_author_search(),
            openalex_author_advisory(),
            github_profile("docxology"),
            github_profile("ActiveInferenceInstitute"),
            public_page("https://activeinference.org/", "AII public landing page"),
            public_page("https://activeinference.institute/structure/officers/", "AII officers page"),
            public_page("https://activeinference.institute/structure/board-of-directors/", "AII board page"),
            public_page("https://activeinference.institute/structure/scientific-advisory-board/", "AII SAB page"),
            public_page("https://activeinference.institute/projects/textbook-group/", "AII textbook-group page"),
        ]
    report = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_commit": source_commit(),
        "date": today,
        "note": "Paginated public-source inventory for review. Use as discovery evidence, not automatic claim replacement.",
        "sections": sections,
        "counts": {section["label"]: len(section.get("items", [])) for section in sections},
    }
    if anchor:
        report["anchors"] = anchor
    return report

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Optional output path. Defaults to reports/public_source_inventory_DATE.json")
    parser.add_argument("--check", action="store_true", help="Validate cached inventory report")
    parser.add_argument("--cache-reports", action="store_true", help="Reuse a same-day cached inventory report instead of refetching")
    parser.add_argument("--force", action="store_true", help="With --cache-reports: reuse the cached report even if stale or warned")
    args = parser.parse_args()
    if args.output:
        out = Path(args.output)
    elif args.check:
        out = latest_report("public_source_inventory_*.json")
    else:
        out = latest_output_path()
    if not out.is_absolute():
        out = REPO_ROOT / out
    if args.check:
        if not out.exists():
            raise SystemExit("Missing public-source inventory report")
        payload = json.loads(out.read_text(encoding="utf-8"))
        if not payload.get("sections"):
            raise SystemExit("Public-source inventory report has no sections")
        print(f"checked public-source inventory report ({len(payload['sections'])} sections)")
        return
    payload = build_report(cache_reports=args.cache_reports, force=args.force)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = [section["label"] for section in payload["sections"] if not section.get("ok")]
    print(f"wrote {out.relative_to(REPO_ROOT)} with {len(payload['sections'])} sections")
    if failures:
        print("warnings:", ", ".join(failures))


if __name__ == "__main__":
    main()
