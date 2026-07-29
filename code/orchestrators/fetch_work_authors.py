#!/usr/bin/env python3
"""Fetch authoritative co-author lists for every catalogued DOI.

`pages/BIBLIOGRAPHY.md` records one author per work (Daniel), so every derived
surface — BibTeX, CSL-JSON, RIS, work pages, JSON-LD — understates authorship on
collaborative papers. This orchestrator resolves the real author list from the
DOI's own registration agency and writes `data/work-authors.json`.

Author lists are *never* inferred. Each DOI is resolved to its registration
agency (https://doi.org/doiRA/<doi>), queried at that agency's API, and the
returned record's title is compared against the catalogued title. A record whose
title does not match is recorded as `title_mismatch` and contributes no authors:
a mistyped or recycled DOI resolves to a real but unrelated paper, and silently
adopting its author list would corrupt the bibliography in a way no downstream
check could catch.

Network-dependent, so deliberately NOT part of regenerate_all.py (see the scope
note there). Run it when the bibliography gains works:

    python3 code/orchestrators/fetch_work_authors.py
    python3 code/orchestrators/fetch_work_authors.py --only 10.5281/zenodo.16903351
    python3 code/orchestrators/fetch_work_authors.py --check   # no network; audit
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS = REPO_ROOT / "data" / "works.json"
OUTPUT = REPO_ROOT / "data" / "work-authors.json"
BIBLIOGRAPHY = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"

CONTACT = "danielarifriedman@gmail.com"
USER_AGENT = f"docxology-bibliography/1.0 (https://danielarifriedman.com/; mailto:{CONTACT})"

# A resolved record must look like the catalogued work before its authors are
# trusted. Titles legitimately differ in punctuation, casing, subtitle handling
# and trailing venue text, so compare normalised forms with a similarity floor
# rather than demanding equality.
TITLE_SIMILARITY_FLOOR = 0.80
REQUEST_PAUSE_SECONDS = 0.2
TIMEOUT_SECONDS = 30


def _get(url: str, accept: str = "application/json") -> tuple[int, bytes]:
    request = urllib.request.Request(
        url, headers={"Accept": accept, "User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


# Publisher titles carry markup: Crossref embeds <i>…</i> around gene names and
# DataCite stores HTML entities (&amp;). Left in place they depress similarity on
# genuine matches.
_TAG = re.compile(r"<[^>]+>")

# Ignored when measuring coverage: catalogued titles routinely drop these while
# publisher titles keep them.
_STOPWORDS = frozenset(
    "a an and as at by for from in into of on or the to with is are it its"
    " some at".split()
)


def normalise_title(title: str) -> str:
    text = html.unescape(_TAG.sub(" ", title or ""))
    folded = unicodedata.normalize("NFKD", text).casefold()
    return re.sub(r"[^a-z0-9]+", " ", folded).strip()


def _stem(token: str) -> str:
    """Trim only unambiguous inflectional endings.

    Catalogued and published titles differ by simple morphology ("trust
    systems" vs "trusted system"). Deliberately conservative — anything more
    aggressive starts collapsing distinct technical terms, which would weaken
    the guard this comparator exists to provide.
    """
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def _significant_tokens(normalised: str) -> set[str]:
    return {_stem(token) for token in normalised.split() if token not in _STOPWORDS}


def title_similarity(catalogued: str, resolved: str) -> float:
    """Similarity in [0, 1] between a catalogued and a resolved title.

    Catalogued titles are frequently shortened or reordered versions of the
    published title ("The P3IF: Properties, Processes, and Perspectives
    Inter-Framework" for "The Properties, Processes, and Perspectives
    Inter-Framework (P3IF): Multiplexing…"). Sequence ratio punishes that
    heavily, so also measure how much of the catalogued title the resolved title
    actually covers, and take the stronger signal. An unrelated record still
    scores near zero on both.
    """
    left, right = normalise_title(catalogued), normalise_title(resolved)
    if not left or not right:
        return 0.0
    if left in right or right in left:
        return 1.0
    ratio = SequenceMatcher(None, left, right).ratio()
    catalogued_tokens = _significant_tokens(left)
    if not catalogued_tokens:
        return ratio
    covered = len(catalogued_tokens & _significant_tokens(right)) / len(catalogued_tokens)
    return max(ratio, covered)


def registration_agency(doi: str) -> str | None:
    status, body = _get(f"https://doi.org/doiRA/{doi}")
    if status != 200:
        return None
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, list) and payload:
        return payload[0].get("RA")
    return None


def _split_display_name(name: str) -> tuple[str, str]:
    """Split "Family, Given" or "Given Family" into (family, given)."""
    if "," in name:
        family, _, given = name.partition(",")
        return family.strip(), given.strip()
    parts = name.split()
    if len(parts) < 2:
        return name.strip(), ""
    return parts[-1], " ".join(parts[:-1])


def _orcid(identifiers: list[dict]) -> str | None:
    for identifier in identifiers or []:
        scheme = (identifier.get("nameIdentifierScheme") or "").upper()
        value = identifier.get("nameIdentifier") or ""
        if scheme == "ORCID" or "orcid.org" in value:
            return value.rstrip("/").split("/")[-1] or None
    return None


def fetch_crossref(doi: str) -> dict | None:
    status, body = _get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
    if status != 200:
        return None
    message = json.loads(body).get("message") or {}
    authors = []
    for entry in message.get("author") or []:
        family = (entry.get("family") or "").strip()
        given = (entry.get("given") or "").strip()
        record: dict[str, str]
        if not family and not given:
            # Consortium/organisation authorship carries a literal `name`.
            name = (entry.get("name") or "").strip()
            if not name:
                continue
            record = {"literal": name}
        else:
            record = {"family": family, "given": given}
        if entry.get("ORCID"):
            record["orcid"] = entry["ORCID"].rstrip("/").split("/")[-1]
        authors.append(record)
    titles = message.get("title") or []
    return {"title": titles[0] if titles else "", "authors": authors}


def fetch_datacite(doi: str) -> dict | None:
    status, body = _get(f"https://api.datacite.org/dois/{urllib.parse.quote(doi)}")
    if status != 200:
        return None
    attributes = (json.loads(body).get("data") or {}).get("attributes") or {}
    authors = []
    for entry in attributes.get("creators") or []:
        name = (entry.get("name") or "").strip()
        record: dict[str, str]
        if (entry.get("nameType") or "").lower() == "organizational":
            # "Active Inference Institute" is one literal name, not Given
            # Family; splitting it yields the nonsense "Institute, Active
            # Inference" in every rendered citation.
            if not name:
                continue
            record = {"literal": name}
        else:
            family = (entry.get("familyName") or "").strip()
            given = (entry.get("givenName") or "").strip()
            if not family and not given:
                family, given = _split_display_name(name)
            if not family and not given:
                continue
            record = {"family": family, "given": given}
        orcid = _orcid(entry.get("nameIdentifiers") or [])
        if orcid:
            record["orcid"] = orcid
        authors.append(record)
    titles = attributes.get("titles") or []
    return {"title": (titles[0] or {}).get("title", "") if titles else "", "authors": authors}


def resolve(doi: str, catalogued_title: str) -> dict:
    agency = registration_agency(doi)
    record: dict = {"registration_agency": agency}
    if agency == "Crossref":
        resolved = fetch_crossref(doi)
    elif agency == "DataCite":
        resolved = fetch_datacite(doi)
    elif agency is None:
        record["status"] = "doi_unresolved"
        return record
    else:
        record["status"] = "unsupported_agency"
        return record

    if resolved is None:
        record["status"] = "not_found"
        return record

    similarity = title_similarity(catalogued_title, resolved["title"])
    record["resolved_title"] = resolved["title"]
    record["title_similarity"] = round(similarity, 4)
    if similarity < TITLE_SIMILARITY_FLOOR:
        # The DOI resolves to a real record that is not this work. Authors are
        # withheld deliberately; a human must reconcile the DOI.
        record["status"] = "title_mismatch"
        return record
    if not resolved["authors"]:
        record["status"] = "no_authors_published"
        return record
    record["status"] = "verified"
    record["authors"] = resolved["authors"]
    return record


def load_works() -> list[dict]:
    return json.loads(WORKS.read_text(encoding="utf-8"))["works"]


def format_author(author: dict) -> str:
    if author.get("literal"):
        return author["literal"]
    family = (author.get("family") or "").strip()
    given = (author.get("given") or "").strip()
    return f"{family}, {given}".strip(", ") if given else family


def format_authors(authors: list[dict]) -> str:
    # Semicolons separate authors because "Family, Given" already uses commas;
    # the cell is pipe-free by construction so it cannot break the table.
    return "; ".join(format_author(author) for author in authors)


def apply_to_bibliography() -> int:
    """Write the Authors column into pages/BIBLIOGRAPHY.md from verified data."""
    if not OUTPUT.is_file():
        print(f"missing {OUTPUT.relative_to(REPO_ROOT)}; run without --apply first", file=sys.stderr)
        return 1
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    by_num = {
        entry["num"]: entry
        for entry in payload["works"].values()
        if entry.get("status") == "verified" and entry.get("authors")
    }

    lines = BIBLIOGRAPHY.read_text(encoding="utf-8").splitlines(keepends=True)
    written = 0
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = line.rstrip("\n").strip().strip("|").split("|")
        if len(cells) < 8:
            continue
        header = cells[0].strip()
        if header == "#":
            cells = cells[:8] + [" Authors "]
            lines[index] = "|" + "|".join(cells) + "|\n"
            continue
        if set(header) <= {"-", ":", " "} and "-" in header:
            cells = cells[:8] + ["------- "]
            lines[index] = "|" + "|".join(cells) + "|\n"
            continue
        try:
            num = int(header)
        except ValueError:
            continue
        entry = by_num.get(num)
        if entry is None:
            # Leave unresolved works with an explicit gap rather than implying
            # sole authorship we have not confirmed against a registry.
            authors_cell = " — "
        else:
            authors_cell = " " + format_authors(entry["authors"]) + " "
            written += 1
        cells = cells[:8] + [authors_cell]
        lines[index] = "|" + "|".join(cells) + "|\n"

    BIBLIOGRAPHY.write_text("".join(lines), encoding="utf-8")
    print(f"wrote Authors column for {written} works into {BIBLIOGRAPHY.relative_to(REPO_ROOT)}")
    unresolved = len(payload["works"]) - written
    if unresolved:
        print(f"  {unresolved} works left as '—' (no DOI, unresolved DOI, or no authors published)")
    return 0


def audit(payload: dict) -> int:
    counts: dict[str, int] = {}
    for entry in payload["works"].values():
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1
    print(f"work-authors.json: {len(payload['works'])} resolved records")
    for status, count in sorted(counts.items(), key=lambda item: -item[1]):
        print(f"  {count:4}  {status}")
    multi = [e for e in payload["works"].values() if len(e.get("authors") or []) > 1]
    print(f"  {len(multi):4}  works with co-authors")
    mismatches = [k for k, e in payload["works"].items() if e["status"] == "title_mismatch"]
    if mismatches:
        print("\ntitle mismatches needing a human DOI reconciliation:")
        for key in mismatches:
            entry = payload["works"][key]
            print(f"  {key}\n    doi={entry.get('doi')} similarity={entry.get('title_similarity')}")
            print(f"    resolved: {entry.get('resolved_title', '')[:100]}")
    return 1 if mismatches else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", help="resolve a single DOI (diagnostics)")
    parser.add_argument("--check", action="store_true", help="audit the existing file; no network")
    parser.add_argument("--apply", action="store_true",
                        help="write the Authors column into pages/BIBLIOGRAPHY.md; no network")
    args = parser.parse_args()

    if args.apply:
        return apply_to_bibliography()

    if args.check:
        if not OUTPUT.is_file():
            print(f"missing {OUTPUT.relative_to(REPO_ROOT)}", file=sys.stderr)
            return 1
        return audit(json.loads(OUTPUT.read_text(encoding="utf-8")))

    works = load_works()
    if args.only:
        target = [w for w in works if (w.get("doi") or "") == args.only]
        if not target:
            print(f"no catalogued work with doi {args.only}", file=sys.stderr)
            return 1
        print(json.dumps(resolve(args.only, target[0]["title"]), indent=2, ensure_ascii=False))
        return 0

    resolved: dict[str, dict] = {}
    with_doi = [w for w in works if (w.get("doi") or "").strip()]
    for index, work in enumerate(with_doi, 1):
        doi = work["doi"].strip()
        record = {"num": work["num"], "doi": doi, "title": work["title"]}
        record.update(resolve(doi, work["title"]))
        resolved[work["citation_key"]] = record
        print(f"[{index:3}/{len(with_doi)}] {record['status']:20} {doi}")
        time.sleep(REQUEST_PAUSE_SECONDS)

    for work in works:
        if (work.get("doi") or "").strip():
            continue
        # No DOI means no registry to ask. Recorded explicitly so the gap is
        # visible rather than looking like a work that simply has one author.
        resolved[work["citation_key"]] = {
            "num": work["num"],
            "doi": None,
            "title": work["title"],
            "status": "no_doi",
        }

    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "generator": "code/orchestrators/fetch_work_authors.py",
        "policy": {
            "sources": ["https://api.crossref.org/works/{doi}", "https://api.datacite.org/dois/{doi}"],
            "agency_lookup": "https://doi.org/doiRA/{doi}",
            "title_similarity_floor": TITLE_SIMILARITY_FLOOR,
            "note": "Authors are adopted only from a record whose title matches the catalogued title; never inferred.",
        },
        "works": dict(sorted(resolved.items(), key=lambda item: item[1]["num"])),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {OUTPUT.relative_to(REPO_ROOT)}")
    return audit(payload)


if __name__ == "__main__":
    sys.exit(main())
