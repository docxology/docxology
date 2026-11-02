# AGENTS.md — `docs/seo/`

SEO runbooks for the public site: canonical URL and redirect rules
([canonical-policy.md](canonical-policy.md)), the manual Google Search Console
follow-up ([gsc-followup.md](gsc-followup.md)), and Scholar discovery and citation
metadata ([scholar-inclusion.md](scholar-inclusion.md)). The documents state
policy; enforcement lives in `code/src/seo_invariants.py`, which
`code/orchestrators/validate_repo.py` runs as part of the repository health gate.

- Change the policy here and the checker together. A rule that exists only in
  prose is a rule nothing enforces, and `validate_repo.py` is the only automated
  check this folder has: there are no tests, fixtures, or CI jobs scoped to
  `docs/seo/`.
- `gsc-followup.md` covers work that needs a signed-in browser with property
  access; the repository has no Search Console API, so that runbook is written for
  a human operator and cannot be automated here.
- Read [canonical-policy.md](canonical-policy.md) before changing canonical URLs,
  sitemap membership, or the permanent `works/{citation_key}.html` URL contract.
  After changing generated pages or their metadata, run
  `uv run python3 code/orchestrators/validate_repo.py`.

The docs-tree contract and the ordered regeneration pipeline are in
[`../AGENTS.md`](../AGENTS.md); repository-wide operating rules are in the
[root instructions](../../AGENTS.md).
