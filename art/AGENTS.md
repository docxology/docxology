# AGENTS.md — `art/`

Local copies of the gallery's artwork files and their per-work metadata JSON (about a
thousand files). The public gallery renders from `data/artworks.json`, which stores the
Flickr-hosted image URLs and per-work metadata; this folder holds the in-repository
copies and their metadata.

- Mirror content, read by tooling that resolves artwork metadata. Do not rename or
  reorganise files: check `data/artworks.json` before assuming a file is still
  referenced.
- Nothing in CI verifies an image or its metadata. `validate_repo.py` checks the
  generated layer and its links, not artwork content, so a wrong or missing image is a
  visual defect rather than a build failure.
- Not an inventory: the listing and `data/artworks.json` are the truth about what is
  here.

Repository rules: [root guide](../AGENTS.md).
