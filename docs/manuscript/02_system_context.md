# System Context {#sec:system_context}

## Project Boundary

A master profile repository indexing bibliography, software, generated GitHub inventory, and research documentation across entomology, active inference, cognitive security, and art/synergetics.

## Source Surfaces

- `pages/`
- `papers/`
- `code/`
- `reports/`
- `resume/`
- `works/`
- `data/`

## Template Boundary

The private project lives in the sidecar repository. Rendering and validation run through the sibling public template checkout after `link-projects` mirrors the project into `template/projects/` as a local symlink.
