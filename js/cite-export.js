(() => {
    // Copy-BibTeX: copies the work's embedded BibTeX entry to the clipboard.
    // Wired by build_work_pages.py (button id=cite-bibtex-btn; data in
    // script#work-bibtex). CSP-safe: external file, no inline handlers.
    "use strict";

    const FALLBACK_MS = 2000;

    function readBibtex() {
        const node = document.getElementById("work-bibtex");
        if (!node) return "";
        return (node.textContent || "").trim();
    }

    function flash(button) {
        const original = button.dataset.originalLabel || button.textContent;
        button.dataset.originalLabel = original;
        button.textContent = "Copied";
        button.disabled = true;
        setTimeout(() => {
            button.textContent = original;
            button.disabled = false;
        }, FALLBACK_MS);
    }

    function legacyCopy(text) {
        const scratch = document.createElement("textarea");
        scratch.value = text;
        scratch.setAttribute("readonly", "");
        scratch.style.position = "fixed";
        scratch.style.left = "-9999px";
        document.body.appendChild(scratch);
        scratch.select();
        let ok = false;
        try {
            ok = document.execCommand("copy");
        } catch (err) {
            ok = false;
        }
        document.body.removeChild(scratch);
        return ok;
    }

    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => true, () => legacyCopy(text));
        }
        return Promise.resolve(legacyCopy(text));
    }

    function init() {
        const button = document.getElementById("cite-bibtex-btn");
        if (!button) return;
        button.addEventListener("click", () => {
            const text = readBibtex();
            if (!text) return;
            copyText(text).then((ok) => {
                if (ok) flash(button);
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
