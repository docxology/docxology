// Menu Escape-to-close handler — external script for CSP compliance.
// Esc closes the mobile nav menu, resets aria-expanded, and refocuses the toggle button.
// NEW-6: the More dropdown (details.nav-more) also closes on outside click and
// on scroll; the hamburger (.nav-links.open) flow is unchanged.
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
      closeOpenMore();
    }
  });

  function closeOpenMore() {
    document.querySelectorAll("details.nav-more[open]").forEach(function (d) {
      d.removeAttribute("open");
    });
  }

  // Outside click: close any open nav-more whose click target is outside it.
  document.addEventListener("click", function (e) {
    document.querySelectorAll("details.nav-more[open]").forEach(function (d) {
      if (!d.contains(e.target)) d.removeAttribute("open");
    });
  });

  // Scroll: passive listener; the dropdown must not survive scrolling away.
  window.addEventListener("scroll", closeOpenMore, { passive: true });
})();
