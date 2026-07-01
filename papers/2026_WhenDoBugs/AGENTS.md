# AGENTS.md - When do bugs see (infra)red?

**Paper**: When do bugs see (infra)red? (2026)
**DOI**: [10.5281/zenodo.20450970](https://doi.org/10.5281/zenodo.20450970)
**GitHub release**: https://github.com/docxology/cohereants/releases/tag/v1.0.0

---

## Agent Roles

### Citation Agent
- Use the Zenodo DOI as the canonical citation.
- Track future GitHub release and Zenodo version changes.

### Integration Agent
- Keep README, CITATION.cff, metadata.json, paper_metadata.json, BIBLIOGRAPHY.md, and software links synchronized.
- Preserve the paired GitHub + Zenodo release relationship.

## Extraction Log

- **Zenodo record**: https://zenodo.org/records/20450880
- **GitHub release**: https://github.com/docxology/cohereants/releases/tag/v1.0.0
- **Pairing evidence**: github_release_mentions_doi, github_release_mentions_zenodo_record, zenodo_related_identifier_mentions_release, github_repo_self_linked, title_overlap
