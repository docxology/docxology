# AGENTS.md - Editorial Quality at Scale: A Reproducible Prose-Review Pipeline

**Paper**: Editorial Quality at Scale: A Reproducible Prose-Review Pipeline (2026)
**DOI**: [10.5281/zenodo.20417105](https://doi.org/10.5281/zenodo.20417105)
**GitHub release**: https://github.com/docxology/template_prose_project/releases/tag/v0.3.0

---

## Agent Roles

### Citation Agent
- Use the Zenodo DOI as the canonical citation.
- Track future GitHub release and Zenodo version changes.

### Integration Agent
- Keep README, CITATION.cff, metadata.json, paper_metadata.json, BIBLIOGRAPHY.md, and software links synchronized.
- Preserve the paired GitHub + Zenodo release relationship.

## Extraction Log

- **Zenodo record**: https://zenodo.org/records/20417105
- **GitHub release**: https://github.com/docxology/template_prose_project/releases/tag/v0.3.0
- **Pairing evidence**: github_release_mentions_doi, github_release_mentions_zenodo_record, zenodo_related_identifier_mentions_release, github_repo_self_linked, title_overlap
