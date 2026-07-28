#!/usr/bin/env python3
"""Write a timestamped public-source freshness report.

This script checks public APIs and official records, then writes a report under
reports/. It does not edit site claims, bibliography counts, or profile copy.
Use the report as evidence before making deliberate site-wide claim updates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCID = "0000-0001-6232-9096"
USER_AGENT = "docxology-public-source-refresh/1.0 (https://github.com/docxology/docxology)"


def fetch_json(url: str, *, accept: str = "application/json", timeout: int = 30, retries: int = 2) -> dict[str, Any]:
    headers = {
        "Accept": accept,
        "User-Agent": USER_AGENT,
    }
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(
        url,
        headers=headers,
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            try:
                delay = min(float(retry_after), 10.0) if retry_after else 2.0 * (attempt + 1)
            except ValueError:
                delay = 2.0 * (attempt + 1)
            time.sleep(delay)
    raise RuntimeError("unreachable retry loop")


def safe_fetch(label: str, url: str, extractor) -> dict[str, Any]:
    try:
        data = fetch_json(url)
        result = extractor(data)
        return {"label": label, "url": url, "ok": True, "result": result}
    except Exception as exc:  # pragma: no cover - network failure details are data, not code behavior
        return {"label": label, "url": url, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def github_user(login: str) -> dict[str, Any]:
    url = f"https://api.github.com/users/{login}"
    return safe_fetch(
        f"GitHub user {login}",
        url,
        lambda data: {
            "login": data.get("login"),
            "public_repos": data.get("public_repos"),
            "updated_at": data.get("updated_at"),
            "html_url": data.get("html_url"),
        },
    )


def github_repo(owner: str, repo: str) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    return safe_fetch(
        f"GitHub repo {owner}/{repo}",
        url,
        lambda data: {
            "full_name": data.get("full_name"),
            "stargazers_count": data.get("stargazers_count"),
            "language": data.get("language"),
            "updated_at": data.get("updated_at"),
            "html_url": data.get("html_url"),
        },
    )


def crossref_orcid() -> dict[str, Any]:
    url = f"https://api.crossref.org/works?filter=orcid:{ORCID}&rows=0"
    return safe_fetch(
        "Crossref ORCID DOI records",
        url,
        lambda data: {"total_results": data.get("message", {}).get("total-results")},
    )


def pubmed_exact_author() -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": "Daniel Ari Friedman[Author]",
            "retmode": "json",
        }
    )
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{query}"
    return safe_fetch(
        "PubMed exact author records",
        url,
        lambda data: {
            "count": int(data.get("esearchresult", {}).get("count", 0)),
            "ids": data.get("esearchresult", {}).get("idlist", []),
        },
    )


def europe_pmc_exact_author() -> dict[str, Any]:
    query = urllib.parse.urlencode(
        {
            "query": 'AUTH:"Daniel Ari Friedman"',
            "format": "json",
            "pageSize": 1,
        }
    )
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{query}"
    return safe_fetch(
        "Europe PMC exact author records",
        url,
        lambda data: {"hit_count": data.get("hitCount")},
    )


def orcid_works() -> dict[str, Any]:
    url = f"https://pub.orcid.org/v3.0/{ORCID}/works"
    return safe_fetch(
        "ORCID work groups",
        url,
        lambda data: {"group_count": len(data.get("group", []))},
    )


def zenodo_query(label: str, q: str) -> dict[str, Any]:
    url = "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": 1})

    def extract(data: dict[str, Any]) -> dict[str, Any]:
        hits = data.get("hits", {})
        total = hits.get("total", {})
        if isinstance(total, dict):
            total_value = total.get("value")
        else:
            total_value = total
        first = (hits.get("hits") or [{}])[0]
        return {
            "total": total_value,
            "first_title": (first.get("metadata") or {}).get("title"),
            "first_doi": first.get("doi"),
        }

    return safe_fetch(label, url, extract)


def zenodo_record(record_id: str) -> dict[str, Any]:
    url = f"https://zenodo.org/api/records/{record_id}"
    return safe_fetch(
        f"Zenodo record {record_id}",
        url,
        lambda data: {
            "title": data.get("metadata", {}).get("title"),
            "doi": data.get("doi"),
            "publication_date": data.get("metadata", {}).get("publication_date"),
            "resource_type": data.get("metadata", {}).get("resource_type", {}).get("title"),
            "creators": [c.get("name") for c in data.get("metadata", {}).get("creators", [])],
        },
    )


def build_report() -> dict[str, Any]:
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    selected_aii_repos = [
        "ActiveInferenceJournal",
        "ActiveBlockference",
        "ActiveInferAnts",
        "GeneralizedNotationNotation",
        "fep_lean",
        "cognitive",
        "CEREBRUM",
        "Journal-Utilities",
    ]
    checks = [
        github_user("docxology"),
        github_user("ActiveInferenceInstitute"),
        orcid_works(),
        pubmed_exact_author(),
        europe_pmc_exact_author(),
        crossref_orcid(),
        zenodo_query("Zenodo exact-name creator records", 'metadata.creators.person_or_org.name:"Friedman, Daniel Ari"'),
        zenodo_query(
            "Zenodo ORCID-linked records",
            f'metadata.creators.person_or_org.identifiers.identifier:"{ORCID}"',
        ),
        zenodo_record("18686966"),
        zenodo_record("19600217"),
        zenodo_record("19897664"),
        zenodo_record("14108992"),
        zenodo_record("17982447"),
    ]
    checks.extend(github_repo("ActiveInferenceInstitute", repo) for repo in selected_aii_repos)
    facts = {
        check["label"]: check.get("result")
        for check in checks
        if check.get("ok") and isinstance(check.get("result"), dict)
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "date": today,
        "note": "Public API freshness report only. Review before updating curated site claims.",
        "facts": facts,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Optional output path. Defaults to reports/public_source_snapshot_DATE.json")
    parser.add_argument("--facts-output", help="Optional path for normalized facts used by CI drift comparisons")
    args = parser.parse_args()

    report = build_report()
    out = Path(args.output) if args.output else REPO_ROOT / "reports" / f"public_source_snapshot_{report['date']}.json"
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.facts_output:
        facts_out = Path(args.facts_output)
        if not facts_out.is_absolute():
            facts_out = REPO_ROOT / facts_out
        facts_out.parent.mkdir(parents=True, exist_ok=True)
        facts_out.write_text(json.dumps(report["facts"], indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = [c["label"] for c in report["checks"] if not c.get("ok")]
    print(f"wrote {out.relative_to(REPO_ROOT)} with {len(report['checks'])} checks")
    if failures:
        print("warnings:", ", ".join(failures))


if __name__ == "__main__":
    main()
