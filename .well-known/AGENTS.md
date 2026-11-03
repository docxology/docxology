# AGENTS.md — `.well-known/`

`security.txt`, the responsible-disclosure record served at
`https://danielarifriedman.com/.well-known/security.txt`. It is plain text with no
generator behind it: edit it directly.

- Keep the contact and the `Expires` field truthful. An expired record is a dead end
  for whoever finds a vulnerability.
- Nothing validates it: `validate_repo.py` covers the generated site layer, not
  well-known metadata, and there is no CI check for this file.

Repository rules: [root guide](../AGENTS.md).
