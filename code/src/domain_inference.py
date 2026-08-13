"""Canonical research-domain inference for publications.

Whole-word matching (so ``ant`` does not hit ``dominant`` and ``art`` does not
hit ``smart``). Keyword order is computational before entomology; that order is
pinned by tests.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

EMOJI_TO_DOMAIN: dict[str, str] = {
    "💻": "Computational",
    "🧠": "Active Inference",
    "🛡️": "Cognitive Security",
    "🐜": "Entomology",
    "🎨": "Art & Synergetics",
    "🧬": "Genetics & Biomedical",
    "🌍": "AII Ecosystem",
    "🎥": "Presentations & Media",
}

DOMAIN_TO_EMOJI: dict[str, str] = {name: emoji for emoji, name in EMOJI_TO_DOMAIN.items()}

_ART_ALIAS = "Art"

_KEYWORD_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("💻", ("textbook", "reproducible", "computational", "software", "code", "pipeline")),
    ("🧠", ("active inference", "free energy", "bayesian", "markov blanket")),
    ("🛡️", ("cognitive security", "cogsec", "narrative", "trust", "integrity")),
    ("🐜", ("ant", "bee", "insect", "ento", "foraging")),
    ("🎨", ("blake", "synergetics", "art", "fuller", "quadray")),
    ("🧬", ("genetic", "genomic", "transcriptomic", "biomedical")),
]

# Optional extras used only by add_zenodo_only (second pass after canonical rules).
ZENODO_EXTRA_TERMS: dict[str, tuple[str, ...]] = {
    "💻": ("benchmark", "harness", "agent"),
    "🧠": ("markov", "friston", "allostasis", "interoception"),
    "🛡️": ("sensemaking", "rhetoric", "memetic"),
    "🐜": ("olfact", "semiochem"),
    "🧬": ("hippocampus", "cortex", "neuro"),
    "🌍": ("ecosystem",),
}


def contains_term(text: str, term: str) -> bool:
    """Whole-word/whole-phrase match via ``\\b``."""
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def canonical_domain_name(value: str) -> str:
    """Map an emoji or alias to the canonical domain name; pass other strings through."""
    if value in EMOJI_TO_DOMAIN:
        return EMOJI_TO_DOMAIN[value]
    if value == _ART_ALIAS:
        return EMOJI_TO_DOMAIN["🎨"]
    return value


def infer_domain_emoji(
    text: str,
    extra_terms: Mapping[str, Sequence[str]] | None = None,
) -> str | None:
    """Return a domain emoji from keyword rules, or None if unknown.

    ``extra_terms`` appends optional per-emoji phrases after the canonical
    terms for that emoji, still in canonical order.
    """
    t = text.lower()
    extras = extra_terms or {}
    for emoji, terms in _KEYWORD_RULES:
        combined = terms + tuple(extras.get(emoji, ()))
        if any(contains_term(t, term) for term in combined):
            return emoji
    extra_aii = tuple(extras.get("🌍", ()))
    if (
        "activeinferenceinstitute" in t
        or contains_term(t, "active inference institute")
        or any(contains_term(t, term) for term in extra_aii)
    ):
        return "🌍"
    return None


def infer_domain_emoji_zenodo(text: str) -> str:
    """Canonical rules first; add_zenodo_only extra terms only if unknown. Default 🧠."""
    hit = infer_domain_emoji(text)
    if hit:
        return hit
    return infer_domain_emoji(text, extra_terms=ZENODO_EXTRA_TERMS) or "🧠"


def infer_domain_emoji_for_pair(pair: Any) -> str | None:
    """Build the publication-pairing text blob and infer a domain emoji."""
    text = " ".join(
        [
            pair.record.title,
            pair.record.description,
            " ".join(pair.record.keywords),
            pair.github_repo,
            pair.release.name,
        ]
    )
    return infer_domain_emoji(text)


def infer_domain_name(
    text: str = "",
    *,
    folder: str = "",
    meta: dict | None = None,
    bib_entry: dict | None = None,
) -> str:
    """Resolve a canonical domain name.

    Priority: ``bib_entry.domain`` → ``meta.domain`` → keyword inference on
    joined folder/meta/keywords/title/description text → ``Research``.
    """
    if bib_entry and bib_entry.get("domain"):
        return canonical_domain_name(str(bib_entry["domain"]))
    if meta and meta.get("domain"):
        return canonical_domain_name(str(meta["domain"]))
    blob = _join_inference_text(text, folder, meta)
    emoji = infer_domain_emoji(blob)
    if emoji:
        return EMOJI_TO_DOMAIN[emoji]
    return "Research"


def _join_inference_text(text: str, folder: str, meta: dict | None) -> str:
    parts: list[str] = [text, folder]
    if meta:
        for key in ("title", "name", "description", "abstract"):
            parts.append(str(meta.get(key) or ""))
        for key in ("keywords", "tags"):
            vals = meta.get(key) or []
            if isinstance(vals, str):
                parts.append(vals)
            else:
                parts.extend(str(v) for v in vals)
    return " ".join(parts)
