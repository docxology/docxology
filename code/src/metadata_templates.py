"""Registry of generic, non-paper-specific metadata text.

Two manual enrichers (``batch_enrich_metadata.py`` and
``improve_metadata_quality.py``) and an older ``regenerate_docs.py`` fallback
filled empty ``methods`` / ``key_findings`` fields with *domain templates* —
every entomology folder received "Field observation and behavioral assays",
every computational folder "Deterministic software pipeline design", and so on.
``code/src/generation_plan.py`` already excludes those enrichers from the
rebuild because they "can introduce inferred methods/findings"; this module is
the render-side half of that policy. Generated paper documents use it to tell a
recorded, paper-specific method or finding apart from template filler, and
show only the former.
"""

from __future__ import annotations

import re
from html import unescape
from typing import Any, Iterable

# Union of every template list the enrichers and the legacy fallback emitted.
TEMPLATE_METHOD_NAMES: frozenset[str] = frozenset(
    {
        # batch_enrich_metadata.DOMAIN_METHODS
        "Deterministic software pipeline design",
        "Reproducible workflow orchestration",
        "Data-driven analysis and visualization",
        "Infrastructure-as-code methodology",
        "Free energy minimization",
        "Generative modeling and simulation",
        "Bayesian inference and belief updating",
        "Policy selection and expected free energy",
        "Narrative analysis and discourse mapping",
        "Misinformation detection frameworks",
        "Trust and integrity modeling",
        "Cognitive defense pattern analysis",
        "Field observation and behavioral assays",
        "Population genetics analysis",
        "Transcriptomic and gene expression profiling",
        "Collective behavior modeling",
        "Visual analysis and iconographic interpretation",
        "Historical and conceptual synthesis",
        "Cross-domain pattern mapping",
        "Symbolic and metaphorical analysis",
        "Genomic sequencing and bioinformatics",
        "Phylogenetic and evolutionary analysis",
        "Statistical genetics and heritability estimation",
        "Molecular mechanism investigation",
        "Community coordination and governance",
        "Open science infrastructure development",
        "Educational program design",
        "Inter-organizational collaboration",
        "Multimedia content production",
        "Pedagogical framework design",
        "Public communication of science",
        "Cross-platform media distribution",
        "Literature review and meta-analysis",
        "Theoretical analysis and synthesis",
        "Empirical data collection",
        "Cross-disciplinary integration",
        # improve_metadata_quality.generate_methods domain fallback
        "Bayesian modeling and inference",
        "Narrative analysis",
        "Visual and symbolic analysis",
        "Genomic and bioinformatic analysis",
        "Statistical genetics",
        "Software pipeline design",
        "Data-driven analysis",
        "Program coordination",
        "Community governance design",
        "Content production",
        "Pedagogical design",
        "Literature review and analysis",
        "Theoretical synthesis",
        "Analysis",
        "Modeling",
        # legacy regenerate_docs.extract_methods_from_metadata fallback
        "Field observation",
        "Behavioral assays",
        "Generative modeling",
        "Bayesian inference",
        "Misinformation detection",
        "Trust frameworks",
        "Visual analysis",
        "Historical interpretation",
        "Conceptual synthesis",
        "Genomic sequencing",
        "Phylogenetic analysis",
        "Literature review",
        "Theoretical analysis",
    }
)

PLACEHOLDER_FINDINGS: frozenset[str] = frozenset(
    {
        "See full paper for detailed findings and analysis",
        "See paper",
    }
)

_WORDS = re.compile(r"[a-z0-9]+")


def _words(text: Any) -> str:
    plain = re.sub(r"<[^>]+>", " ", unescape(str(text or "")))
    return " ".join(_WORDS.findall(plain.lower()))


def _method_name(method: Any) -> str:
    if isinstance(method, dict):
        return str(method.get("name") or "").strip()
    return str(method or "").strip()


def is_template_method(method: Any) -> bool:
    """Return whether a recorded method is generic domain filler."""
    return _method_name(method) in TEMPLATE_METHOD_NAMES


def specific_methods(methods: Iterable[Any] | None) -> list[str]:
    """Return the paper-specific method names, dropping template filler."""
    names: list[str] = []
    for method in methods or []:
        name = _method_name(method)
        if name and not is_template_method(method) and name not in names:
            names.append(name)
    return names


_AUTO_DESCRIPTION = re.compile(r"^Applied .+ approach\.?$", re.IGNORECASE)


def specific_method_details(methods: Iterable[Any] | None) -> list[tuple[str, str]]:
    """Return ``(name, description)`` for paper-specific methods.

    Descriptions auto-generated by the enrichers ("Applied <name> approach")
    carry no information and are dropped; the name is kept.
    """
    details: list[tuple[str, str]] = []
    seen: set[str] = set()
    for method in methods or []:
        name = _method_name(method)
        if not name or is_template_method(method) or name in seen:
            continue
        seen.add(name)
        description = ""
        if isinstance(method, dict):
            description = " ".join(str(method.get("description") or "").split())
            if _AUTO_DESCRIPTION.match(description):
                description = ""
        details.append((name, description))
    return details


def specific_findings(findings: Iterable[Any] | None, *abstract_sources: Any) -> list[str]:
    """Return recorded findings that are neither placeholders nor abstract echoes.

    Several enrichment passes copied the first sentences of the abstract into
    ``key_findings`` (often cut mid-word and padded with ``....``). Those lines
    restate background, not results, and the abstract is already shown, so a
    finding whose words all occur as a run inside the abstract is dropped.
    """
    abstract_words = " ".join(_words(source) for source in abstract_sources if source)
    kept: list[str] = []
    for finding in findings or []:
        text = str(finding or "").strip()
        if not text or text in PLACEHOLDER_FINDINGS:
            continue
        words = _words(text.rstrip(". "))
        # A truncated fragment ends in a partial word; compare without it.
        probe = words.rsplit(" ", 1)[0] if text.endswith("..") and " " in words else words
        if probe and abstract_words and probe in abstract_words:
            continue
        if text not in kept:
            kept.append(text)
    return kept
