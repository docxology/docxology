// Attach the mobile control while the header is parsed, before its first paint.
// The parser-blocking head tag owns the complete enhancement; no later script
// is required. A blocked script leaves the normal-flow navigation accessible.
(function () {
  if (window.__docxologyEarlyNav) return;
  window.__docxologyEarlyNav = true;

  let observer;
  function enhanceNavigation() {
    let enhanced = false;
    document.querySelectorAll('nav').forEach(nav => {
      const button = nav.querySelector('.menu-btn');
      const links = nav.querySelector('.nav-links');
      if (!button || !links) return;
      if (!button.dataset.navToggleWired) {
        button.addEventListener('click', () => {
          const isOpen = links.classList.toggle('open');
          button.setAttribute('aria-expanded', String(isOpen));
        });
        button.dataset.navToggleWired = 'true';
      }
      button.setAttribute('aria-expanded', String(links.classList.contains('open')));
      nav.classList.add('nav-enhanced');
      enhanced = true;
    });
    if (enhanced && observer) observer.disconnect();
    return enhanced;
  }

  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('nav.nav-enhanced .nav-links.open').forEach(links => {
      links.classList.remove('open');
      const button = links.closest('nav').querySelector('.menu-btn');
      button.setAttribute('aria-expanded', 'false');
      button.focus();
      event.preventDefault();
    });
    document.querySelectorAll('details.nav-more[open]').forEach(details => {
      details.removeAttribute('open');
    });
  });

  if (!enhanceNavigation()) {
    observer = new MutationObserver(enhanceNavigation);
    observer.observe(document.documentElement, { childList: true, subtree: true });
    document.addEventListener('DOMContentLoaded', () => {
      enhanceNavigation();
      observer.disconnect();
    }, { once: true });
  }
})();
