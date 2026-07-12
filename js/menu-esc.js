// Menu Escape-to-close handler — external script for CSP compliance.
// Esc closes the mobile nav menu, resets aria-expanded, and refocuses the toggle button.
(function () {
  if (window.__navEsc) return;
  window.__navEsc = 1;
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      var m = document.querySelector(".nav-links.open");
      if (m) {
        m.classList.remove("open");
        var b = document.querySelector(".menu-btn");
        if (b) {
          b.setAttribute("aria-expanded", "false");
          b.focus();
        }
      }
    }
  });
})();
