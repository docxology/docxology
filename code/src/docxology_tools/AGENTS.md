# AGENTS.md — `code/src/docxology_tools/`

A bootstrap package, not a library: `__init__.py` makes the flat modules in `../`
importable as one package so callers stop editing `sys.path`.

- Put new shared code in the flat modules beside this package and expose it here; do not
  add another `sys.path.insert` to a caller.
- The package re-exports what it bootstraps, so a name that works as `docxology_tools.x`
  is also importable flat. Changing what it exports can break orchestrators that still
  import the flat form.
- Repository rules are in [`../../AGENTS.md`](../../AGENTS.md).
