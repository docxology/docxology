# CV release

`resume/source.json` is the sole curated CV source. Generated JSON, plaintext,
semantic HTML, verification metadata, and PDF outputs must be rebuilt together.

```bash
uv run python3 code/orchestrators/build_resume.py --all
uv run python3 code/orchestrators/build_resume.py --check
uv run python3 code/orchestrators/regenerate_all.py --validate
```

The repository validator runs the public-integrity checks as part of the full
gate. Public CV artifacts must not contain local filesystem paths, secrets, or
unsafe URL schemes. Source notes should describe public provenance without
exposing the operator's checkout or download directories.

Retain explicit uncertainty: dated affiliations, ongoing work, stealth records,
and snapshot metrics must not be rewritten as current verified claims without a
fresh primary source. Use `data/claims.json` and `data/scholar-snapshot.json` for
the evidence boundary.
