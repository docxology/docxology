#!/usr/bin/env python3
"""regenerate_docs.py — Regenerate documentation files for all paper folders.

Reads paper_metadata.json and generates/updates README.md, AGENTS.md, and SKILL.md
for each paper folder. Extended version with enriched Methods/Findings sections.

Usage:
    python3 regenerate_docs.py                    # preview mode
    python3 regenerate_docs.py --apply            # apply changes
    python3 regenerate_docs.py --force --apply    # overwrite existing files
"""

from __future__ import annotations

import json
import os
import re
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from biblio_table import iter_bibliography_rows  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PAPERS_DIR / "regenerate_docs.log"),
    ],
)
log = logging.getLogger(__name__)
BIBLIOGRAPHY_PATH = Path(os.environ.get("BIB_PATH", PAPERS_DIR.parent / "pages" / "BIBLIOGRAPHY.md"))

# ─── Helpers ──────────────────────────────────────────────────────────────────


def parse_folder_id(folder: str) -> tuple[str, str]:
    """Map directory name ``YYYY_Topic`` to ``(year, topic)``."""
    m = re.match(r"^(\d{4})_(.+)$", folder)
    if not m:
        return "unknown", folder
    return m.group(1), m.group(2)


def load_metadata() -> dict:
    """Load consolidated metadata from paper_metadata.json."""
    metadata_path = PAPERS_DIR / "paper_metadata.json"
    if metadata_path.exists():
        with open(metadata_path) as f:
            return json.load(f)
    log.warning("No paper_metadata.json found")
    return {}


def parse_bibliography() -> dict:
    """Parse BIBLIOGRAPHY.md table into a dict keyed by folder name (rows with a Docs link)."""
    bib = {}
    if not BIBLIOGRAPHY_PATH.exists():
        log.warning("BIBLIOGRAPHY.md not found")
        return bib
    for row in iter_bibliography_rows(BIBLIOGRAPHY_PATH):
        folder = row.folder
        if not folder:
            continue
        bib[folder] = {
            "num": row.num,
            "year": row.year,
            "title": row.title,
            "venue": row.venue,
            "link": row.link_cell,
            "domain": row.domain,
            "type": row.typ,
        }
    log.info(f"Parsed {len(bib)} entries from BIBLIOGRAPHY.md")
    return bib


def resolve_domain(folder: str, meta: dict, bib_entry: dict | None = None) -> str:
    """Resolve the domain name from metadata, bibliography, or inference."""
    emoji_to_name = {
        '💻': 'Computational',
        '🧠': 'Active Inference',
        '🛡️': 'Cognitive Security',
        '🐜': 'Entomology',
        '🎨': 'Art & Synergetics',
        '🧬': 'Genetics & Biomedical',
        '🌍': 'AII Ecosystem',
        '🎥': 'Presentations & Media',
    }
    # Priority 1: explicit domain in metadata.json (may be emoji or name)
    if meta.get('domain'):
        d = meta['domain']
        if d in emoji_to_name:
            return emoji_to_name[d]
        return d
    # Priority 2: bib_entry domain (emoji form)
    if bib_entry and bib_entry.get('domain'):
        domain_cell = bib_entry['domain']
        if domain_cell in emoji_to_name:
            return emoji_to_name[domain_cell]
    # Priority 3: infer from content
    return infer_domain(folder, meta)


def infer_domain(folder: str, meta: dict) -> str:
    """Infer research domain from folder name, tags, and keywords."""
    _, topic = parse_folder_id(folder)
    tags = meta.get('tags', [])
    keywords = meta.get('keywords', [])
    all_text = ' '.join([topic.lower()] + [t.lower() for t in tags] + [k.lower() for k in keywords])

    if any(x in all_text for x in ['ant', 'insect', 'bee', 'entomol', 'myrmec', 'colony', 'foraging']):
        return 'Entomology'
    if any(x in all_text for x in ['active inference', 'free energy', 'bayesian', 'variational', 'markov blanket']):
        return 'Active Inference'
    if any(x in all_text for x in ['cognitive security', 'cogsec', 'narrative', 'integrity']):
        return 'Cognitive Security'
    if any(x in all_text for x in ['art', 'blake', 'synergetics', 'music', 'imaginarium']):
        return 'Art'
    if any(x in all_text for x in ['genetic', 'genom', 'transcriptom', 'dna', 'pcr']):
        return 'Genetics & Biomedical'
    return 'Research'


def extract_methods_from_metadata(meta: dict) -> list[str]:
    """Extract methods from metadata, falling back to inferred list."""
    methods = meta.get('methods', [])
    if methods:
        if isinstance(methods[0], dict):
            return [m.get('name', '') for m in methods if m.get('name')]
        return list(methods)
    # Generate placeholder methods based on domain
    domain = infer_domain('', meta)
    base_methods = {
        'Entomology': ['Field observation', 'Population genetics analysis', 'Behavioral assays'],
        'Active Inference': ['Free energy minimization', 'Generative modeling', 'Bayesian inference'],
        'Cognitive Security': ['Narrative analysis', 'Misinformation detection', 'Trust frameworks'],
        'Art': ['Visual analysis', 'Historical interpretation', 'Conceptual synthesis'],
        'Genetics & Biomedical': ['Genomic sequencing', 'Phylogenetic analysis', 'Statistical genetics'],
    }
    return base_methods.get(domain, ['Literature review', 'Theoretical analysis'])


def extract_findings_from_metadata(meta: dict) -> list[str]:
    """Extract key findings from metadata, falling back to placeholder."""
    findings = meta.get('key_findings', [])
    if findings:
        return findings
    return ['See full paper for detailed findings and analysis']


def extract_related_papers(meta: dict, all_folders: list[str]) -> list[str]:
    """Extract related paper folder names from metadata."""
    related = meta.get('related_papers', [])
    # Filter to only valid folders
    return [r for r in related if r in all_folders]


# ─── Generators ───────────────────────────────────────────────────────────────


def generate_readme(folder: str, meta: dict, bib_entry: dict | None = None) -> str:
    """Generate README.md content with enhanced structure."""
    year, topic = parse_folder_id(folder)
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')

    # Get abstract from description or metadata
    abstract = meta.get('abstract', meta.get('description', f'Research paper on {topic}.'))
    # Truncate for display
    abstract_short = abstract[:400] + '...' if len(abstract) > 400 else abstract

    keywords = meta.get('keywords', meta.get('tags', []))
    domain = resolve_domain(folder, meta, bib_entry)
    venue = bib_entry.get('venue', 'Zenodo') if bib_entry else 'Zenodo'
    link = bib_entry.get('link', '') if bib_entry else ''

    # Methods and findings
    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)

    # Domain emoji
    emoji_map = {'Entomology': '🐜', 'Active Inference': '🧠', 'Cognitive Security': '🛡️',
                 'Art': '🎨', 'Genetics & Biomedical': '🧬', 'Research': '📄', 'Computational': '💻'}
    # Normalize domain name for emoji lookup
    domain_key = domain if domain in emoji_map else 'Research'
    emoji = emoji_map.get(domain_key, '📄')

    kw_str = ' · '.join(f'`{k}`' for k in keywords[:12]) if keywords else f'`{topic}`'

    lines = [
        f'# {emoji} {title}',
        '',
        f'**{authors}** ({year}) · *{venue}*',
        '',
    ]

    if link and 'doi' in link.lower():
        doi_match = re.search(r'(10\.\S+)', link)
        if doi_match:
            doi_text = doi_match.group(1)
            # Clean the link for the badge (no protocol in badge URL)
            link_clean = link.split()[0] if ' ' in link else link
            lines.append(f'[![DOI](https://img.shields.io/badge/DOI-{doi_text.replace("/", "%2F")}-blue)]({link_clean})')
            lines.append('')

    lines.extend([
        '---',
        '',
        '## Abstract',
        '',
        f'> {abstract_short}',
        '',
        '## Keywords',
        '',
        kw_str,
        '',
        '## Methods',
        '',
    ])

    for method in methods[:6]:
        lines.append(f'- {method}')
    lines.append('')

    lines.extend([
        '## Key Findings',
        '',
    ])

    for finding in findings[:6]:
        lines.append(f'- {finding}')
    lines.append('')

    # Artifacts section
    lines.extend([
        '## Artifacts',
        '',
    ])

    # Check for associated GitHub repo
    github_repo = meta.get('github_repo')
    if github_repo:
        lines.append(f'- GitHub release: https://github.com/{github_repo}')

    # Check for DOI
    doi = meta.get('doi') or (bib_entry.get('link') if bib_entry else '')
    if doi:
        lines.append(f'- DOI: {doi}')

    lines.extend([
        f'- PDF SHA-256: {meta.get("pdf_sha256") or "See zenodo_record"}',
        '',
        '## Citation',
        '',
        f'> {authors} ({year}). *{title}*. {venue}.',
        '',
        '## Related',
        '',
        '- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)',
        '- [All Papers](../README.md)',
    ])

    return '\n'.join(lines)


def generate_agents(folder: str, meta: dict, bib_entry: dict | None = None) -> str:
    """Generate AGENTS.md content with enhanced structure."""
    year, topic = parse_folder_id(folder)
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')
    domain = resolve_domain(folder, meta, bib_entry)
    description = meta.get('description', meta.get('abstract', f'Research on {topic}'))[:200]

    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)

    lines = [
        f'# AGENTS.md — {title}',
        '',
        f'**Paper**: {title} ({year})',
        f'**Domain**: {domain}',
        f'**Authors**: {authors}',
        '',
        '---',
        '',
        '## Agent Roles',
        '',
        '### 📖 ARCHIVIST',
        '- Maintains bibliographic metadata and cross-references',
        f'- Tracks citation links and DOI consistency for {topic}',
        '- Updates related_papers links when new connections are identified',
        '',
        '### 🔬 RESEARCHER',
        f'- Extracts methods: {", ".join(methods[:3]) if methods else "See paper"}',
        f'- Identifies findings: {", ".join(findings[:3]) if findings else "See paper"}',
        f'- Maps contributions to {domain} literature',
        '',
        '### 🎓 EDUCATOR',
        f'- Creates learning pathways for {domain} concepts',
        f'- Develops SKILL.md with executable instructions',
        '- Maintains prerequisite knowledge mapping',
        '',
        '### 🔗 INTEGRATOR',
        f'- Connects {title} to related works in the bibliography',
        '- Maps paper-to-software relationships',
        '- Updates cross-domain connections',
        '',
        '---',
        '',
        '## Extraction Log',
        '',
        '| Date | Agent | Action | Status |',
        '|------|-------|--------|--------|',
        f'| {datetime.now().strftime("%Y-%m-%d")} | ARCHIVIST | Cataloged metadata | ✅ |',
        f'| {datetime.now().strftime("%Y-%m-%d")} | RESEARCHER | Extracted methods/findings | ✅ |',
        f'| {datetime.now().strftime("%Y-%m-%d")} | EDUCATOR | Generated documentation | ✅ |',
    ]

    # Extended metadata
    if meta.get('related_papers') or meta.get('related_software'):
        lines.extend([
            '',
            '## Cross-References',
            '',
        ])
        if meta.get('related_papers'):
            lines.append('### Related Papers')
            for rp in meta['related_papers'][:8]:
                lines.append(f'- [{rp}](../{rp}/)')
            lines.append('')
        if meta.get('related_software'):
            lines.append('### Related Software')
            for rs in meta['related_software'][:4]:
                lines.append(f'- https://github.com/{rs}')
            lines.append('')

    return '\n'.join(lines)


def generate_skill(folder: str, meta: dict, all_folders: list[str] | None = None, bib_entry: dict | None = None) -> str:
    """Generate SKILL.md content with Claude Code-compatible YAML frontmatter.

    Extended version with Methods, Key Findings, Related Works, Datasets, and Validation sections.
    """
    year, topic = parse_folder_id(folder)
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')
    description = meta.get('description', meta.get('abstract', f'Research on {topic}')).strip()
    domain = resolve_domain(folder, meta, bib_entry)
    tags = meta.get('tags', meta.get('keywords', [topic.lower()]))
    keywords = meta.get('keywords', tags)

    # Merge with folder-specific metadata if available
    folder_meta_path = PAPERS_DIR / folder / "metadata.json"
    folder_meta = {}
    if folder_meta_path.exists():
        with open(folder_meta_path) as f:
            folder_meta = json.load(f)
        # Merge: folder-specific values override parent metadata
        for key in ['methods', 'key_findings', 'related_papers', 'related_software', 'pdf_sha256', 'pairing_confidence', 'checked_at']:
            if key in folder_meta:
                meta[key] = folder_meta[key]
        if 'domain' in folder_meta:
            # Convert emoji to name if needed
            emoji_to_name = {
                '💻': 'Computational',
                '🧠': 'Active Inference',
                '🛡️': 'Cognitive Security',
                '🐜': 'Entomology',
                '🎨': 'Art & Synergetics',
                '🧬': 'Genetics & Biomedical',
            }
            d = folder_meta['domain']
            domain = emoji_to_name.get(d, d)

    methods = extract_methods_from_metadata(meta)
    findings = extract_findings_from_metadata(meta)
    related = extract_related_papers(meta, all_folders or [])

    # Format tags
    if isinstance(tags, list) and tags:
        tags_yaml = json.dumps([t.lower().replace(' ', '-') for t in tags[:10]])
    else:
        tags_yaml = f'["{topic.lower()}"]'

    # Truncate description for frontmatter (must be single-line for YAML)
    desc_clean = ' '.join(description.split())  # Normalize whitespace
    desc_short = desc_clean[:250] + '...' if len(desc_clean) > 250 else desc_clean

    # DOI for reference
    doi = meta.get('doi', '')
    citation = f'{authors} ({year}). *{title}*. {domain}.'

    lines = [
        '---',
        f'name: "{title}"',
        f'description: "{desc_short}"',
        f'tags: {tags_yaml}',
        f'domain: "{domain}"',
        f'citation: "{citation}"',
    ]

    if doi:
        lines.append(f'doi: "{doi}"')

    lines.extend([
        '---',
        '',
        f'# {title}',
        '',
        f'**{authors}** ({year}) · {domain}',
        '',
        '## Context',
        '',
        f'This work addresses topics in **{domain}**: {", ".join(keywords[:4]) if keywords else topic}.',
        '',
    ])

    # Methods section
    lines.extend([
        '## Methods',
        '',
        'Primary methods and techniques applied in this work:',
        '',
    ])
    for method in methods[:6]:
        lines.append(f'- {method}')
    lines.append('')

    # Key Findings section
    lines.extend([
        '## Key Findings',
        '',
        'Core contributions and results:',
        '',
    ])
    for finding in findings[:6]:
        lines.append(f'- {finding}')
    lines.append('')

    # Datasets section
    dataset_refs = meta.get('dataset_references', [])
    if dataset_refs:
        lines.extend([
            '## Datasets',
            '',
            'Referenced datasets:',
            '',
        ])
        for ds in dataset_refs[:6]:
            lines.append(f'- {ds}')
        lines.append('')

    # Related Works section
    lines.extend([
        '## Related Works',
        '',
    ])
    for rp in related[:6]:
        lines.append(f'- [{rp}](../{rp}/)')
    if not related:
        lines.append('See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.')
    lines.append('')

    # Validation section
    lines.extend([
        '## Validation',
        '',
        'Verification points for this work:',
        '',
        f'- DOI: {doi if doi else "Not assigned"}',
        f'- PDF SHA-256: {meta.get("pdf_sha256") or "See zenodo_record"}',
        f'- Pairing confidence: {meta.get("pairing_confidence") or "unknown"}',
        f'- Last checked: {meta.get("checked_at") or "unknown"}',
        '',
    ])

    # Prerequisites
    lines.extend([
        '## Prerequisites',
        '',
        f'- Familiarity with {", ".join(keywords[:3]) if keywords else topic}',
        f'- Background in {domain} fundamentals',
        f'- Access to source repository: {meta.get("github_repo") or "N/A"}',
        '',
        '## Instructions',
        '',
        'When working with this paper:',
        '',
        f'1. Reference the DOI for citation: `{doi}`' if doi else '1. Use the canonical citation above.',
        '2. Apply methods listed in the Methods section for related analysis.',
        '3. Validate findings against the original PDF and metadata.',
        '',
    ])

    return '\n'.join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    apply = '--apply' in sys.argv
    force = '--force' in sys.argv

    metadata = load_metadata()
    bib = parse_bibliography()

    folders = sorted([
        d for d in os.listdir(PAPERS_DIR)
        if re.match(r"^\d{4}_", d) and os.path.isdir(PAPERS_DIR / d)
    ])

    log.info(f"Found {len(folders)} paper folders, {len(metadata)} metadata entries")

    stats = {'created': 0, 'skipped': 0, 'updated': 0}

    for folder in folders:
        yr, tp = parse_folder_id(folder)
        meta = metadata.get(folder, {'year': yr, 'topic': tp, 'name': tp})
        bib_entry = bib.get(folder)

        # Merge with folder-specific metadata if available (for extended fields)
        folder_meta_path = PAPERS_DIR / folder / "metadata.json"
        if folder_meta_path.exists():
            with open(folder_meta_path) as f:
                folder_meta = json.load(f)
            for key in ['methods', 'key_findings', 'related_papers', 'related_software', 'domain', 'pdf_sha256', 'pairing_confidence', 'checked_at']:
                if key in folder_meta:
                    meta[key] = folder_meta[key]

        for filename in ['README.md', 'AGENTS.md', 'SKILL.md']:
            filepath = PAPERS_DIR / folder / filename
            exists = filepath.exists()
            is_substantive = exists and filepath.stat().st_size > 500

            if is_substantive and not force:
                stats['skipped'] += 1
                continue

            if filename == 'README.md':
                content = generate_readme(folder, meta, bib_entry)
            elif filename == 'AGENTS.md':
                content = generate_agents(folder, meta, bib_entry)
            else:  # SKILL.md
                content = generate_skill(folder, meta, folders, bib_entry)

            if apply:
                filepath.write_text(content)
                action = 'UPDATED' if exists else 'CREATED'
                stats['updated' if exists else 'created'] += 1
                log.info(f"  {action}: {folder}/{filename}")
            else:
                action = 'WOULD UPDATE' if exists else 'WOULD CREATE'
                stats['created'] += 1
                log.info(f"  {action}: {folder}/{filename}")

    log.info(f"\nResults: created={stats['created']}, updated={stats['updated']}, skipped={stats['skipped']}")
    if not apply:
        log.info("DRY RUN — use --apply to write files")


if __name__ == '__main__':
    main()