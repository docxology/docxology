# docxology_tools

The canonical import surface for the shared modules that live flat in `../` —
`report_paths`, `site_nav`, `publication_pairing` and the rest. Historically every
orchestrator and test inserted `code/src` (sometimes also `code/orchestrators`) onto
`sys.path` by hand and imported those modules by bare name; this package is the single
bootstrap for that layout, so a caller writes one import instead of repeating the path
setup.

`__init__.py` is the whole package. Importers include the orchestrators in
`../../orchestrators/` and the tests.
