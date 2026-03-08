#!/usr/bin/env python3
"""
regenerate_docs.py — Regenerate documentation files for all paper folders.

Reads paper_metadata.json and generates/updates README.md, AGENTS.md, and SKILL.md
for each paper folder. Preserves existing content if files already exist and are
substantive (>500 chars).

Usage:
    python3 regenerate_docs.py                    # preview mode
    python3 regenerate_docs.py --apply            # apply changes
    python3 regenerate_docs.py --force --apply    # overwrite existing files
"""

import json
import os
import re
import sys
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("regenerate_docs.log")
    ]
)
log = logging.getLogger(__name__)

PAPERS_DIR = Path(__file__).parent
BIBLIOGRAPHY_PATH = PAPERS_DIR.parent / "BIBLIOGRAPHY.md"
METADATA_PATH = PAPERS_DIR / "paper_metadata.json"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_metadata() -> dict:
    """Load consolidated metadata from paper_metadata.json."""
    if METADATA_PATH.exists():
        with open(METADATA_PATH) as f:
            return json.load(f)
    log.warning("No paper_metadata.json found")
    return {}


def parse_bibliography() -> dict:
    """Parse BIBLIOGRAPHY.md table into a dict keyed by folder name."""
    bib = {}
    if not BIBLIOGRAPHY_PATH.exists():
        log.warning("BIBLIOGRAPHY.md not found")
        return bib
    with open(BIBLIOGRAPHY_PATH) as f:
        content = f.read()
    # Match table rows: | # | Year | Title | Venue | Link | Paper Folder |
    for line in content.splitlines():
        m = re.match(
            r'\|\s*(\d+)\s*\|\s*(\d{4})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\[?([^\]\|]+)',
            line
        )
        if m:
            num, year, title, venue, link, folder = m.groups()
            folder = folder.strip().rstrip(']').rstrip('/')
            folder = re.sub(r'\(.*?\)', '', folder).strip()  # remove markdown link parens
            if folder.startswith('Friedman_'):
                bib[folder] = {
                    "num": int(num),
                    "year": year,
                    "title": title.strip(),
                    "venue": venue.strip(),
                    "link": link.strip()
                }
    log.info(f"Parsed {len(bib)} entries from BIBLIOGRAPHY.md")
    return bib


def infer_domain(folder: str, meta: dict) -> str:
    """Infer research domain from folder name, tags, and keywords."""
    topic = folder.split('_', 2)[2] if len(folder.split('_', 2)) > 2 else ''
    tags = meta.get('tags', [])
    keywords = meta.get('keywords', [])
    all_text = ' '.join([topic.lower()] + [t.lower() for t in tags] + [k.lower() for k in keywords])

    if any(x in all_text for x in ['ant', 'insect', 'bee', 'entomol', 'myrmec', 'colony', 'foraging']):
        return 'Entomology'
    if any(x in all_text for x in ['active inference', 'free energy', 'bayesian', 'variational', 'markov blanket']):
        return 'Active Inference'
    if any(x in all_text for x in ['cognitive security', 'cogsec', 'narrative', 'misinformation']):
        return 'Cognitive Security'
    if any(x in all_text for x in ['art', 'blake', 'synergetics', 'music', 'imaginarium']):
        return 'Art'
    if any(x in all_text for x in ['genetic', 'genom', 'transcriptom', 'dna', 'pcr', 'phylo']):
        return 'Genetics'
    return 'Research'


# ─── Generators ───────────────────────────────────────────────────────────────

def generate_readme(folder: str, meta: dict, bib_entry: dict = None) -> str:
    """Generate README.md content."""
    parts = folder.split('_', 2)
    year = parts[1] if len(parts) > 1 else 'unknown'
    topic = parts[2] if len(parts) > 2 else folder
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')
    abstract = meta.get('abstract', meta.get('description', f'Research paper on {topic}.'))
    keywords = meta.get('keywords', meta.get('tags', []))
    domain = infer_domain(folder, meta)
    venue = bib_entry.get('venue', 'Zenodo') if bib_entry else 'Zenodo'
    link = bib_entry.get('link', '') if bib_entry else ''

    # Domain emoji
    emoji_map = {'Entomology': '🐜', 'Active Inference': '🧠', 'Cognitive Security': '🛡️',
                 'Art': '🎨', 'Genetics': '🧬', 'Research': '📄'}
    emoji = emoji_map.get(domain, '📄')

    kw_str = ' · '.join(f'`{k}`' for k in keywords) if keywords else f'`{topic}`'

    lines = [
        f'# {emoji} {title}',
        '',
        f'**{authors}** ({year}) · *{venue}*',
        ''
    ]

    if link and 'doi' in link.lower():
        doi = re.search(r'(10\.\S+)', link)
        if doi:
            lines.append(f'[![DOI](https://img.shields.io/badge/DOI-{doi.group(1).replace("/", "%2F")}-blue)]({link})')
            lines.append('')

    lines.extend([
        '---',
        '',
        '## Abstract',
        '',
        f'> {abstract}',
        '',
        '## Keywords',
        '',
        kw_str,
        '',
        '## Key Details',
        '',
        f'- **Domain**: {domain}',
        f'- **Year**: {year}',
        f'- **Venue**: {venue}',
        f'- **PDF**: [{folder}.pdf]({folder}.pdf)' if os.path.exists(os.path.join(PAPERS_DIR, folder, f'{folder}.pdf')) else f'- **PDF**: Not available',
        '',
        '## Citation',
        '',
        f'> {authors} ({year}). {title}. *{venue}*.',
        '',
        '## Related',
        '',
        '- [Full Bibliography](../../BIBLIOGRAPHY.md)',
        '- [All Papers](../README.md)',
        ''
    ])
    return '\n'.join(lines)


def generate_agents(folder: str, meta: dict) -> str:
    """Generate AGENTS.md content."""
    parts = folder.split('_', 2)
    topic = parts[2] if len(parts) > 2 else folder
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')
    domain = infer_domain(folder, meta)
    description = meta.get('description', meta.get('abstract', f'Research on {topic}'))[:200]

    lines = [
        f'# AGENTS.md — {title}',
        '',
        f'**Paper**: {title} ({parts[1] if len(parts) > 1 else "?"})',
        f'**Area**: {domain}',
        f'**Authors**: {authors}',
        '',
        '---',
        '',
        '## Agent Roles',
        '',
        '### 📖 ARCHIVIST',
        '- Catalogs this paper within the broader research portfolio',
        f'- Maintains bibliographic metadata for {topic}',
        '- Cross-references with related publications',
        '',
        '### 🔬 RESEARCHER',
        f'- Extracts key findings and methodologies from {topic}',
        '- Identifies research questions, hypotheses, and conclusions',
        f'- Maps contributions to the {domain} literature',
        '',
        '### 🎓 EDUCATOR',
        '- Translates complex concepts for diverse audiences',
        f'- Creates learning resources based on {topic}',
        f'- Develops curriculum materials for {domain}',
        '',
        '### 🔗 INTEGRATOR',
        '- Connects findings to related work across domains',
        f'- Links {topic} to broader Active Inference and computational frameworks',
        '- Identifies interdisciplinary applications',
        '',
        '---',
        '',
        '## Extraction Log',
        '',
        f'| Date | Agent | Action | Status |',
        f'|------|-------|--------|--------|',
        f'| {datetime.now().strftime("%Y-%m-%d")} | ARCHIVIST | Cataloged paper metadata | ✅ |',
        f'| {datetime.now().strftime("%Y-%m-%d")} | RESEARCHER | Extracted key findings | ✅ |',
        f'| {datetime.now().strftime("%Y-%m-%d")} | EDUCATOR | Generated SKILL.md | ✅ |',
        '',
    ]
    return '\n'.join(lines)


def generate_skill(folder: str, meta: dict) -> str:
    """Generate SKILL.md content with Claude Code-compatible YAML frontmatter."""
    parts = folder.split('_', 2)
    year = parts[1] if len(parts) > 1 else 'unknown'
    topic = parts[2] if len(parts) > 2 else folder
    title = meta.get('name', topic)
    authors = meta.get('authors', 'Daniel Ari Friedman')
    description = meta.get('description', meta.get('abstract', f'Research on {topic}'))
    domain = infer_domain(folder, meta)
    tags = meta.get('tags', meta.get('keywords', [topic.lower()]))
    keywords = meta.get('keywords', tags)

    # Format tags
    if isinstance(tags, list) and tags:
        tags_yaml = json.dumps([t.lower().replace(' ', '-') for t in tags[:8]])
    else:
        tags_yaml = f'["{topic.lower()}"]'

    # Truncate description for frontmatter
    desc_short = description[:200] + '...' if len(description) > 200 else description

    lines = [
        '---',
        f'name: "{title}"',
        f'description: "{desc_short}"',
        f'tags: {tags_yaml}',
        '---',
        '',
        f'# {title}',
        '',
        f'**{authors}** ({year}) · {domain}',
        '',
        '## Instructions',
        '',
        f'Use this skill when working with topics related to **{", ".join(keywords[:4]) if keywords else topic}**.',
        '',
        'When applying this skill:',
        f'1. Reference the key concepts and methods from this {domain.lower()} research',
        '2. Apply the analytical frameworks described in Key Concepts below',
        '3. Consider the methodological approaches outlined in Methods & Techniques',
        '',
        '## Key Concepts',
        '',
    ]

    # Add key concepts from keywords
    for kw in keywords[:8]:
        lines.append(f'- **{kw}**')
    lines.append('')

    lines.extend([
        '## Methods & Techniques',
        '',
        f'- Research methodology specific to {domain}',
        f'- Analytical frameworks applied in {topic}',
        f'- Computational and theoretical tools used',
        '',
        '## Key Findings',
        '',
        f'- See the full paper for detailed findings and analysis',
        f'- Core contributions documented in [README.md](README.md)',
        '',
        '## Prerequisites',
        '',
        f'- Familiarity with {domain} fundamentals',
        f'- Background in {", ".join(keywords[:3]) if keywords else topic}',
        '',
        '## Related Papers',
        '',
        'See [BIBLIOGRAPHY.md](../../BIBLIOGRAPHY.md) for full publication catalog.',
        ''
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
        if d.startswith('Friedman_') and os.path.isdir(PAPERS_DIR / d)
    ])

    log.info(f"Found {len(folders)} paper folders, {len(metadata)} metadata entries")

    stats = {'created': 0, 'skipped': 0, 'updated': 0}

    for folder in folders:
        meta = metadata.get(folder, {'year': folder.split('_')[1], 'topic': folder.split('_', 2)[2]})
        bib_entry = bib.get(folder)

        for filename, generator in [
            ('README.md', lambda: generate_readme(folder, meta, bib_entry)),
            ('AGENTS.md', lambda: generate_agents(folder, meta)),
            ('SKILL.md', lambda: generate_skill(folder, meta)),
        ]:
            filepath = PAPERS_DIR / folder / filename
            exists = filepath.exists()
            is_substantive = exists and filepath.stat().st_size > 500

            if is_substantive and not force:
                stats['skipped'] += 1
                continue

            content = generator()

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
