# Supplemental Source Surface {#sec:source_surface}

This supplement maps statements to the source owners that should be inspected when the draft or implementation changes.

- **Bibliography parsing and stable identity.** Source: [biblio_table.py](../../code/src/biblio_table.py), [work_identifiers.py](../../code/src/work_identifiers.py). Verification: [Canonical policy](../seo/canonical-policy.md), bibliography export checks.

- **Local generation and configuration.** Source: [generation_plan.py](../../code/src/generation_plan.py), [regenerate_all.py](../../code/orchestrators/regenerate_all.py). Verification: [Regeneration runbook](../operations/regeneration.md), no-write checks in the plan.

- **Structured resume and evidence.** Source: [resume_data.py](../../code/src/resume_data.py), [claim exports](../../code/orchestrators/export_agent_data.py). Verification: [Development map](../operations/development.md), generated manifest.

- **Static navigation and progressive search.** Source: [nav-toggle.js](../../js/nav-toggle.js), [search-page.js](../../js/search-page.js). Verification: [Runtime acceptance](../operations/site-runtime.md), rendered frontend tests.

- **Gallery and publication batching.** Source: [art-gallery.js](../../js/art-gallery.js), [publications.js](../../js/publications.js). Verification: [Progressive gallery tests](../../code/tests/test_art_gallery_progressive.py), [publication tests](../../code/tests/test_publications_startup.py).

- **Video browsing.** Source: [videos-page.js](../../js/videos-page.js). Verification: [Accessibility tests](../../code/tests/test_accessibility_refinements.py).

- **Browser caching.** Source: [sw.js](../../sw.js). Verification: [Service-worker tests](../../code/tests/test_service_worker.py).

- **Bounded hosting projection.** Source: [Artifact policy](../operations/github-pages-artifact.md). Verification: [Artifact builder](../../code/orchestrators/build_pages_artifact.py), manifest checks.

- **Deployed source/run binding.** Source: [verify_live_site.py](../../code/orchestrators/verify_live_site.py). Verification: [Live verification](../operations/live-verification.md), fresh scoped receipt.

- **Human review and release attestation.** Source: [visual_qa.py](../../code/orchestrators/visual_qa.py). Verification: [Accessibility QA](../operations/accessibility-qa.md), [release integrity](../operations/release-integrity.md).

- **Manuscript source checks.** Source: [manuscript_validation.py](../../code/src/manuscript_validation.py), [config.yaml](config.yaml). Verification: [Validator tests](../../code/tests/test_manuscript_validation.py), read-only JSON diagnostics.


- **Agent inspection and profiling.** Source: [agent entry point](../../code/orchestrators/agent.py), [backend profiler](../../code/src/backend_profiling.py). Verification: [agent interface](../operations/agent-interface.md), [profiling method](../operations/backend-profiling.md).

- **Native manuscript PDF.** Source: [renderer](../../code/src/manuscript_rendering.py), [template adapter](../../code/src/manuscript_template.py). Verification: [rendering guide](README.md), opt-in real integration and page inspection.

## Expansion checklist

- Identify authored source and generated projections separately.
- Verify the commands and configuration that reproduce a claim.
- Keep volatile totals in generated snapshots until a manuscript value producer exists.
- Check external references and citation metadata before adding literature claims.
- Exclude credentials, personal records, and unpublished sensitive material from public prose.
