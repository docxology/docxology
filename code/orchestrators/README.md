# orchestrators

Pipeline orchestrator scripts for the site. See `AGENTS.md` here.

Every script that needs `code/src` starts with the same uniform two-line
wrapper bootstrap — `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))`
then `import docxology_tools` — so it self-bootstraps however it is invoked:
as `python3 code/orchestrators/<name>.py` from any cwd, flat-imported by
tests, or copied into a minimal fixture checkout. The package's canonical
bootstrap then puts both `code/src` and `code/orchestrators` on `sys.path`
(idempotent); sibling-orchestrator imports stay flat. See
[`../README.md`](../README.md) → "Import contract (DOC-014)".
