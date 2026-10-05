# Supplemental Source Surface {#sec:source_surface}

This supplement maps statements to the source owners that should be inspected when the draft or implementation changes.

| Concern | Source owner | Verification or guidance |
| --- | --- | --- |
| Bibliography parsing and stable identity | [biblio_table.py](../../code/src/biblio_table.py), [work_identifiers.py](../../code/src/work_identifiers.py) | [Canonical policy](../seo/canonical-policy.md), bibliography export checks |
| Local generation and configuration | [generation_plan.py](../../code/src/generation_plan.py), [regenerate_all.py](../../code/orchestrators/regenerate_all.py) | [Regeneration runbook](../operations/regeneration.md), no-write checks in the plan |
| Structured resume and evidence | [resume_data.py](../../code/src/resume_data.py), [claim exports](../../code/orchestrators/export_agent_data.py) | [Development map](../operations/development.md), generated manifest |
| Static navigation and progressive search | [nav-toggle.js](../../js/nav-toggle.js), [search-page.js](../../js/search-page.js) | [Runtime acceptance](../operations/site-runtime.md), rendered frontend tests |
| Gallery and publication batching | [art-gallery.js](../../js/art-gallery.js), [publications.js](../../js/publications.js) | [Progressive gallery tests](../../code/tests/test_art_gallery_progressive.py), [publication tests](../../code/tests/test_publications_startup.py) |
| Video browsing | [videos-page.js](../../js/videos-page.js) | [Accessibility tests](../../code/tests/test_accessibility_refinements.py) |
| Browser caching | [sw.js](../../sw.js) | [Service-worker tests](../../code/tests/test_service_worker.py) |
| Bounded hosting projection | [Artifact policy](../operations/github-pages-artifact.md) | [Artifact builder](../../code/orchestrators/build_pages_artifact.py), manifest checks |
| Deployed source/run binding | [verify_live_site.py](../../code/orchestrators/verify_live_site.py) | [Live verification](../operations/live-verification.md), fresh scoped receipt |
| Human review and release attestation | [visual_qa.py](../../code/orchestrators/visual_qa.py) | [Accessibility QA](../operations/accessibility-qa.md), [release integrity](../operations/release-integrity.md) |
| Manuscript source checks | [manuscript_validation.py](../../code/src/manuscript_validation.py), [config.yaml](config.yaml) | [Validator tests](../../code/tests/test_manuscript_validation.py), read-only JSON diagnostics |

## Expansion checklist

- Identify authored source and generated projections separately.
- Verify the commands and configuration that reproduce a claim.
- Keep volatile totals in generated snapshots until a manuscript value producer exists.
- Check external references and citation metadata before adding literature claims.
- Exclude credentials, personal records, and unpublished sensitive material from public prose.
