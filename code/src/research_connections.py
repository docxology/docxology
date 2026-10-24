"""Deterministic, explainable catalog relationships; never inferred citations."""

from __future__ import annotations

from collections import Counter
import re
import unicodedata

from docxology_tools.site_nav import canonical_work_key


def normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def terms(enrichment: dict, field: str) -> dict[str, str]:
    """Preserve display labels while matching whole recorded phrases."""
    values = enrichment.get(field, [])
    if not isinstance(values, list):
        return {}
    return {
        normalized(v): v.strip()
        for v in values
        if isinstance(v, str) and 2 < len(v.strip()) < 100
    }


def related_catalog(
    works: list[dict], enrichments: dict[str, dict], repositories: dict[str, str]
) -> dict[str, list[dict]]:
    """Rank metadata overlap, with a labelled domain-only fallback.

    Very common authors do not distinguish recommendations. Exact recorded
    phrases are used instead of fuzzy semantic or scientific inference.
    """
    authors = {
        w["citation_key"]: {normalized(a): a for a in w.get("authors", [])}
        for w in works
    }
    frequencies = Counter(a for values in authors.values() for a in values)
    distinctive = {
        a for a, count in frequencies.items() if count <= max(2, len(works) // 2)
    }
    features = {
        w["citation_key"]: {
            f: terms(enrichments.get(w["citation_key"], {}), f)
            for f in ("keywords", "methods")
        }
        for w in works
    }
    result = {}
    for work in works:
        key = work["citation_key"]
        candidates = []
        for other in works:
            target = other["citation_key"]
            # Duplicate deposits must not recommend themselves through aliases.
            if canonical_work_key(key) == canonical_work_key(target) or (
                work.get("doi") and work.get("doi") == other.get("doi")
            ):
                continue
            score, reasons = 0, []
            if (
                repositories.get(key)
                and repositories.get(key, "").casefold()
                == repositories.get(target, "").casefold()
            ):
                score += 10
                reasons.append(
                    "Associated software: "
                    + repositories[key].removeprefix("https://github.com/")
                )
            for field, weight, label in (
                ("methods", 5, "Recorded method"),
                ("keywords", 3, "Recorded topic"),
            ):
                overlap = sorted(
                    features[key][field].keys() & features[target][field].keys()
                )
                if overlap:
                    score += weight * min(len(overlap), 3)
                    reasons.append(
                        label
                        + ": "
                        + "; ".join(features[key][field][term] for term in overlap[:2])
                    )
            shared = sorted(authors[key].keys() & authors[target].keys() & distinctive)
            if shared:
                score += 2 * min(len(shared), 2)
                names = "; ".join(authors[key][author] for author in shared[:2])
                role = (
                    "editor" if work.get("contributor_role") == "editor" else "author"
                )
                other_role = (
                    "editor" if other.get("contributor_role") == "editor" else "author"
                )
                if role == other_role:
                    reasons.append(
                        ("Shared editor: " if role == "editor" else "Coauthor: ")
                        + names
                    )
                else:
                    reasons.append(
                        f"Shared contributor: {names} ({role} of this work; {other_role} of related work)"
                    )
            if work.get("domain") and work.get("domain") == other.get("domain"):
                score += 1
                if not reasons:
                    reasons.append(
                        "Same catalog domain; no more specific metadata overlap recorded"
                    )
            if score:
                candidates.append(
                    {
                        "citation_key": target,
                        "title": other["title"],
                        "year": other["year"],
                        "score": score,
                        "reasons": reasons,
                    }
                )
        result[key] = sorted(
            candidates,
            key=lambda item: (-item["score"], -int(item["year"]), item["citation_key"]),
        )[:6]
    return result


def graph_catalog(works: list[dict], repositories: dict[str, str]) -> dict:
    """Publish literal work/domain/byline/repository edges with source labels."""
    nodes, edges = {}, []
    for work in works:
        key = work["citation_key"]
        wid = "work:" + key
        nodes[wid] = {
            "id": wid,
            "kind": "work",
            "label": work["title"],
            "url": "/works/" + key + ".html",
            "year": work["year"],
        }
        domain = "domain:" + normalized(work["domain_name"])
        nodes[domain] = {
            "id": domain,
            "kind": "domain",
            "label": work["domain_name"],
            "url": "/publications.html?domain=" + work["domain"],
        }
        edges.append(
            {
                "source": wid,
                "target": domain,
                "relation": "Catalog domain",
                "provenance": "pages/BIBLIOGRAPHY.md",
            }
        )
        for author in work.get("authors", []):
            aid = "person:" + normalized(author)
            nodes[aid] = {"id": aid, "kind": "person", "label": author, "url": ""}
            role = (
                "Recorded editor"
                if work.get("contributor_role") == "editor"
                else "Recorded author"
            )
            edges.append(
                {
                    "source": wid,
                    "target": aid,
                    "relation": role,
                    "provenance": "data/work-authors.json",
                }
            )
        repo = repositories.get(key)
        if repo:
            rid = "software:" + repo.casefold()
            nodes[rid] = {
                "id": rid,
                "kind": "software",
                "label": repo.removeprefix("https://github.com/"),
                "url": repo,
            }
            edges.append(
                {
                    "source": wid,
                    "target": rid,
                    "relation": "Associated software",
                    "provenance": work.get("docs_path", "") + "metadata.json",
                }
            )
    return {
        "schema_version": 1,
        "description": "Catalog relationships, not a citation network or identity registry. Author nodes group exact normalized recorded names; homonyms may be grouped and name variants remain separate.",
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "edges": edges,
    }


def valid_key(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,180}", value))
