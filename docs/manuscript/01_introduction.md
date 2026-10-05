# Introduction {#sec:introduction}

## Motivation

A scholarly profile can combine papers, software, teaching, art, video, and public identifiers without making their sources and update rules easy to inspect. In docxology, those surfaces share a repository and a static website [@docxologyIndex]. Maintaining their consistency requires explicit authority: a curated bibliography row, an external API observation, an extracted PDF, and a generated page carry different information and different uncertainty.

## Repository-system contribution

The repository connects authored source, machine-readable discovery exports, stable work pages, and deployment controls. The implementation uses shared parsers and policies, runnable command entry points, a declared generation plan, and proportionate checks. Browser catalogs build on native HTML links and fetch larger data when an interaction needs it.

This draft explains those mechanisms using local source references. It is an account of the implemented design with verification boundaries; it does not report a comparison with other scholarly-profile systems.

## Reader orientation

System boundaries are defined in @sec:system_context. Methods and reproducibility commands follow in @sec:methods and @sec:reproducibility. The evidence map in @sec:artifacts_evidence identifies what each check can establish. The supplement links source owners so future changes can update the narrative alongside the implementation.
