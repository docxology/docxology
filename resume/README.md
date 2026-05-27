# Resume / CV Exports

This directory replaces the old Coda resume export with repo-native structured
data and deterministic generated artifacts.

## Source Ownership

- `resume/source.json` is the curated source for resume-specific records:
  contact, education, experience, awards, conferences, media/outreach,
  service, and art-use history.
- Bibliography and software rows are not duplicated here. They are merged from
  `data/works.json` and `data/software.json`.
- Dated metrics and caveats are merged from `data/scholar-snapshot.json` and
  `data/claims.json`.

The original Coda PDF at `/Users/4d/Downloads/Resume.pdf` is an import
checklist only and should not be committed.

## Generated Outputs

Run:

```bash
uv run python3 code/orchestrators/build_resume.py --all
```

Tracked outputs:

- `data/resume.json`
- `resume/full.txt`
- `resume/academic.txt`
- `resume/software-consulting.txt`
- `resume/teaching-service.txt`
- `resume/resume.pdf`
- `resume/verify.html`

`resume/verify.html` is the QR target for the PDF. It records the source
manifest hash, generated JSON hash, final PDF hash, artifact sizes, counts, and
links to `data/resume.json` and `resume/resume.pdf`.

Focused PDFs are available on demand:

```bash
uv run python3 code/orchestrators/build_resume.py --variant academic --format pdf
uv run python3 code/orchestrators/build_resume.py --variant software-consulting --format pdf
uv run python3 code/orchestrators/build_resume.py --variant teaching-service --format pdf
```

## Validation

```bash
uv run python3 code/orchestrators/build_resume.py --check
uv run python3 code/orchestrators/validate_repo.py
cd code/tests && uv run pytest -q
```
