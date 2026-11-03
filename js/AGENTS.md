# AGENTS.md — `js/`

The site's front-end JavaScript modules: the shared interactive layer
(`interactive.js`, `menu-esc.js`, `nav-toggle.js`), text-to-speech
(`tts-controls.js`), and the page runtimes (`publications.js`, `art-gallery.js`,
`collections.js`, and the rest). Hand-maintained; there is no bundler or build step.

- CSP is `script-src 'self'`: no inline event handlers and no inline script blocks.
  Behaviour belongs in these modules, wired through `data-*` attributes.
- These files are loaded by generated pages, so a breaking change reaches many pages at
  once; check the page that loads a module before changing its contract.
- No test executes the browser behaviour here — the Playwright suites record against
  the built site, and nothing in CI runs a browser, so JavaScript regressions are found
  by reading or by a recorded run, not by the gate.

Repository rules: [root guide](../AGENTS.md).
