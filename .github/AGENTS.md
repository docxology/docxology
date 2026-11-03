# AGENTS.md — `.github/`

GitHub-side configuration: `workflows/` (Actions), `ISSUE_TEMPLATE/` (the issue forms),
and `dependabot.yml`. `README.md` here is generated from the repository's own
`README.md` by `code/orchestrators/build_github_readme.py` — edit the root README and
regenerate, never this copy.

- The workflows are the repository's automated gate; `validate.yml` runs
  `code/orchestrators/validate_repo.py` and the Python suite. See
  [`workflows/AGENTS.md`](workflows/AGENTS.md) for what each one is for.
- Nothing in this folder runs locally. Copy the commands from the workflow you are
  reproducing instead of inventing a local equivalent.
- Branch protection, required checks, and secrets live in GitHub settings, not in the
  repository; this guide cannot tell you what they are.

Repository rules: [root guide](../AGENTS.md).
