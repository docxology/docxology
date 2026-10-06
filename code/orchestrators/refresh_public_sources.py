#!/usr/bin/env python3
"""Write a timestamped public-source freshness report.

This script checks public APIs and official records, then writes a report under
reports/. It does not edit site claims, bibliography counts, or profile copy.
Use the report as evidence before making deliberate site-wide claim updates.
"""

import argparse
import datetime as dt
import http.client
import json
import math
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.report_paths import source_commit, source_worktree_state  # noqa: E402

ORCID = "0000-0001-6232-9096"
USER_AGENT = "docxology-public-source-refresh/1.0 (https://github.com/docxology/docxology)"
# Connection-level failures worth a bounded retry. ConnectionError covers resets,
# aborts, refusals and broken pipes (ConnectionResetError, ConnectionAbortedError,
# http.client.RemoteDisconnected, ...); TimeoutError covers a socket timeout raised
# while reading the body, which urllib does not wrap in URLError. ssl.SSLError covers
# TLS failures raised while reading the body (SSLEOFError: the peer closed the TLS
# stream mid-response), which urllib likewise leaves unwrapped; it subclasses OSError,
# not ConnectionError. HTTPError subclasses URLError, so fetch_json handles it first and
# only retries the statuses below.
TRANSIENT_ERRORS = (
    urllib.error.URLError,
    TimeoutError,
    ConnectionError,
    http.client.IncompleteRead,
    ssl.SSLError,
)
# Gateway-level HTTP statuses that signal a momentary upstream hiccup, not a verdict.
# 429 is handled alongside them; every other 4xx/5xx status is raised on the first call.
RETRYABLE_HTTP_STATUS = frozenset({429, 502, 503, 504})
SELECTED_AII_REPOS = (
    "ActiveInferenceJournal",
    "ActiveBlockference",
    "ActiveInferAnts",
    "GeneralizedNotationNotation",
    "fep_lean",
    "cognitive",
    "CEREBRUM",
    "Journal-Utilities",
)


def expected_check_labels() -> tuple[str, ...]:
    """Return the versioned public-source coverage contract without fetching."""
    return (
        "GitHub user docxology",
        "GitHub user ActiveInferenceInstitute",
        "ORCID work groups",
        "PubMed exact author records",
        "Europe PMC exact author records",
        "Crossref ORCID DOI records",
        "Zenodo exact-name creator records",
        "Zenodo ORCID-linked records",
        "Zenodo record 18686966",
        "Zenodo record 19600217",
        "Zenodo record 19897664",
        "Zenodo record 14108992",
        "Zenodo record 17982447",
        *(f"GitHub repo ActiveInferenceInstitute/{repo}" for repo in SELECTED_AII_REPOS),
    )


def _backoff_delay(attempt: int, retry_after: str | None = None) -> float:
    """Bounded backoff: honor a numeric Retry-After (capped at 10s), else 2s, 4s, ...

    A Retry-After that is not a finite, non-negative number (an HTTP-date, "-5",
    "nan", "inf") falls back to the default delay: time.sleep rejects negative and
    NaN values, and an infinite one would be clamped to the cap rather than meant.
    """
    if retry_after:
        try:
            seconds = float(retry_after)
        except ValueError:
            pass
        else:
            if math.isfinite(seconds) and seconds >= 0:
                return min(seconds, 10.0)
    return 2.0 * (attempt + 1)


def fetch_json(url: str, *, accept: str = "application/json", timeout: int = 30, retries: int = 2) -> dict[str, Any]:
    """GET `url` as JSON with a bounded retry budget (`retries` extra attempts).

    Retried, with the `_backoff_delay` schedule (2s, 4s, ...; a finite numeric
    Retry-After header is honored up to 10s):
      * connection-level failures in `TRANSIENT_ERRORS` (URLError, TimeoutError,
        ConnectionError and its subclasses, IncompleteRead, ssl.SSLError and its
        subclasses such as SSLEOFError), including mid-read;
      * HTTP 429, 502, 503 and 504 (`RETRYABLE_HTTP_STATUS`): rate limiting and
        gateway/proxy hiccups.
    Never retried: any other HTTP status (a 403 or 404 is a verdict, not a flaky
    link). The last error is re-raised once the budget is spent.
    """
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
            # Listed before TRANSIENT_ERRORS on purpose: a 403/404 is a verdict, not a flaky connection.
            if exc.code not in RETRYABLE_HTTP_STATUS or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After") if exc.headers is not None else None
            time.sleep(_backoff_delay(attempt, retry_after))
        except TRANSIENT_ERRORS:
            # Proxies and CDNs reset or truncate connections intermittently; a missed
            # check would otherwise vanish from `facts` and read as false drift.
            if attempt >= retries:
                raise
            time.sleep(_backoff_delay(attempt))
    raise RuntimeError("unreachable retry loop")


def safe_fetch(label: str, url: str, extractor) -> dict[str, Any]:
    try:
        data = fetch_json(url)
        result = extractor(data)
        return {"label": label, "url": url, "ok": True, "result": result}
    except Exception as exc:  # pragma: no cover - network failure details are data, not code behavior
        return {"label": label, "url": url, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def github_user_facts(data: dict[str, Any]) -> dict[str, Any]:
    """Facts kept from GET /users/<login>; `type` is "User" or "Organization"."""
    return {
        "login": data.get("login"),
        "type": data.get("type"),
        "public_repos": data.get("public_repos"),
        "updated_at": data.get("updated_at"),
        "html_url": data.get("html_url"),
    }


def github_user(login: str) -> dict[str, Any]:
    url = f"https://api.github.com/users/{login}"
    return safe_fetch(f"GitHub user {login}", url, github_user_facts)


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


def zenodo_query_url(q: str) -> str:
    """Search URL whose single hit is the newest deposit, so first_title/first_doi are deterministic."""
    return "https://zenodo.org/api/records?" + urllib.parse.urlencode({"q": q, "size": 1, "sort": "mostrecent"})


def zenodo_query(label: str, q: str) -> dict[str, Any]:
    url = zenodo_query_url(q)

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
    tasks = [
        lambda: github_user("docxology"),
        lambda: github_user("ActiveInferenceInstitute"),
        lambda: orcid_works(),
        lambda: pubmed_exact_author(),
        lambda: europe_pmc_exact_author(),
        lambda: crossref_orcid(),
        lambda: zenodo_query("Zenodo exact-name creator records", 'metadata.creators.person_or_org.name:"Friedman, Daniel Ari"'),
        lambda: zenodo_query(
            "Zenodo ORCID-linked records",
            f'metadata.creators.person_or_org.identifiers.identifier:"{ORCID}"',
        ),
        lambda: zenodo_record("18686966"),
        lambda: zenodo_record("19600217"),
        lambda: zenodo_record("19897664"),
        lambda: zenodo_record("14108992"),
        lambda: zenodo_record("17982447"),
        *(lambda repo=repo: github_repo("ActiveInferenceInstitute", repo) for repo in SELECTED_AII_REPOS),
    ]
    with ThreadPoolExecutor(max_workers=8) as pool:
        checks = list(pool.map(lambda fn: fn(), tasks))
    facts = {
        check["label"]: check.get("result")
        for check in checks
        if check.get("ok") and isinstance(check.get("result"), dict)
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_commit": source_commit(),
        **source_worktree_state(),
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
    try:
        shown = out.relative_to(REPO_ROOT)
    except ValueError:  # --output pointed outside the repo (a scratch rehearsal); the files are already written
        shown = out
    print(f"wrote {shown} with {len(report['checks'])} checks")
    if failures:
        print("warnings:", ", ".join(failures))


if __name__ == "__main__":
    main()
