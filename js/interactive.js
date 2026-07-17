/**
 * Interactive Enhancements for danielarifriedman.com
 *
 * Features:
 * 1. Reading Progress Bar — thin bar at top of page tracking scroll position
 * 2. Scroll-to-Top Button — appears after 300px scroll
 * 3. Keyboard Shortcuts Hints — press ? to show/hide overlay
 * 4. Section Anchor Copy — click section heading to copy anchor link
 * 5. Search Autocomplete — lightweight suggestions from search-index.json
 * 6. Image Lazy Loading — adds loading="lazy" to images
 * 7. External Link Indicator — adds rel="noopener noreferrer" + icon to external links
 *
 * All features respect prefers-reduced-motion.
 */

(function () {
  'use strict';

  // Non-render-blocking font loading: stylesheets ship with media="print" and
  // data-media-swap="all"; swap here because CSP (script-src 'self') forbids
  // the inline onload="this.media='all'" pattern. This script is deferred, so
  // the DOM is fully parsed by the time this runs.
  document.querySelectorAll('link[rel="stylesheet"][data-media-swap]').forEach(function (l) {
    l.media = l.getAttribute('data-media-swap') || 'all';
  });

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ═══════════════════════════════════════════════
  // 1. READING PROGRESS BAR
  // ═══════════════════════════════════════════════

  function createProgressBar() {
    const bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'Reading progress');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    bar.setAttribute('aria-valuenow', '0');
    document.body.prepend(bar);

    let ticking = false;
    function updateProgress() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0;
      bar.style.width = progress + '%';
      bar.setAttribute('aria-valuenow', Math.round(progress));
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => updateProgress());
        ticking = true;
      }
    }, { passive: true });

    // Also update on resize
    window.addEventListener('resize', updateProgress, { passive: true });
    // Initial position
    updateProgress();
  }

  // ═══════════════════════════════════════════════
  // 2. SCROLL-TO-TOP BUTTON
  // ═══════════════════════════════════════════════

  function createScrollToTop() {
    const btn = document.createElement('button');
    btn.className = 'scroll-top';
    btn.setAttribute('aria-label', 'Scroll to top');
    btn.setAttribute('title', 'Back to top');
    btn.innerHTML = '↑';
    btn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: reduceMotion ? 'instant' : 'smooth',
      });
    });
    document.body.appendChild(btn);

    let visible = false;
    window.addEventListener('scroll', () => {
      const shouldShow = window.scrollY > 300;
      if (shouldShow !== visible) {
        visible = shouldShow;
        btn.classList.toggle('scroll-top-visible', visible);
      }
    }, { passive: true });
  }

  // ═══════════════════════════════════════════════
  // 3. KEYBOARD SHORTCUTS HINT OVERLAY
  // ═══════════════════════════════════════════════

  function createShortcutsOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'shortcuts-overlay';
    overlay.id = 'shortcuts-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Keyboard shortcuts');
    overlay.setAttribute('aria-hidden', 'true');
    overlay.innerHTML = `
      <div class="shortcuts-panel">
        <div class="shortcuts-header">
          <span class="shortcuts-title">Keyboard Shortcuts</span>
          <button class="shortcuts-close" aria-label="Close shortcuts">×</button>
        </div>
        <div class="shortcuts-body">
          <div class="shortcut-row"><kbd>?</kbd> <span>Toggle this panel</span></div>
          <div class="shortcut-row"><kbd>T</kbd> <span>Toggle text-to-speech controls</span></div>
          <div class="shortcut-row"><kbd>Esc</kbd> <span>Close panel / Close menu</span></div>
          <div class="shortcut-row"><kbd>/</kbd> <span>Focus search (on search page)</span></div>
          <div class="shortcut-row"><kbd>↑</kbd> <span>Scroll to top</span></div>
          <div class="shortcut-row"><kbd>Home</kbd> <span>Go to top of page</span></div>
          <div class="shortcut-row"><kbd>End</kbd> <span>Go to bottom of page</span></div>
          <div class="shortcut-row"><kbd>Ctrl+F</kbd> <span>Browser find (text search)</span></div>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    const closeBtn = overlay.querySelector('.shortcuts-close');
    const panel = overlay.querySelector('.shortcuts-panel');

    function show() {
      overlay.classList.add('shortcuts-open');
      overlay.setAttribute('aria-hidden', 'false');
      closeBtn.focus();
    }

    function hide() {
      overlay.classList.remove('shortcuts-open');
      overlay.setAttribute('aria-hidden', 'true');
    }

    closeBtn.addEventListener('click', hide);

    // Click outside panel to close
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) hide();
    });

    // Escape to close
    overlay.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        hide();
      }
    });

    // Global ? key to toggle
    document.addEventListener('keydown', (e) => {
      // Don't fire when typing in input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
      if (e.key === '?' && !e.shiftKey) {
        e.preventDefault();
        if (overlay.getAttribute('aria-hidden') === 'true') {
          show();
        } else {
          hide();
        }
      }
      // / to focus search on search page
      if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        const searchInput = document.querySelector('.search-input, .search-wrap input');
        if (searchInput && document.body.contains(searchInput)) {
          e.preventDefault();
          searchInput.focus();
        }
      }
    });

    return { show, hide };
  }

  // ═══════════════════════════════════════════════
  // 4. SECTION ANCHOR COPY
  // ═══════════════════════════════════════════════

  function addSectionAnchors() {
    document.querySelectorAll('section[id] h2, .section[id] h2, .section-header h2[id]').forEach(heading => {
      const section = heading.closest('section, .section');
      if (!section) return;
      const id = section.id || heading.id || heading.closest('[id]')?.id;
      if (!id) return;

      // Don't add if already has anchor
      if (heading.querySelector('.anchor-link')) return;

      const link = document.createElement('a');
      link.className = 'anchor-link';
      link.href = '#' + id;
      link.setAttribute('aria-label', 'Anchor link for ' + heading.textContent.trim());
      link.setAttribute('title', 'Copy link to this section');
      link.textContent = '#';
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const url = window.location.origin + window.location.pathname + '#' + id;
        navigator.clipboard.writeText(url).catch(() => {});
        link.textContent = '✓';
        setTimeout(() => { link.textContent = '#'; }, 1500);
      });
      heading.appendChild(link);
    });
  }

  // ═══════════════════════════════════════════════
  // 5. SEARCH AUTOCOMPLETE
  // ═══════════════════════════════════════════════

  let searchIndex = null;
  let searchIndexLoading = false;

  function loadSearchIndex(callback) {
    if (searchIndex) { callback(searchIndex); return; }
    if (searchIndexLoading) return;
    searchIndexLoading = true;

    fetch('/search-index.json')
      .then(r => r.json())
      .then(data => {
        // Flatten the index
        if (Array.isArray(data)) {
          searchIndex = data;
        } else if (data.items) {
          searchIndex = data.items;
        } else if (data.results) {
          searchIndex = data.results;
        } else if (data.entries) {
          searchIndex = data.entries;
        } else {
          searchIndex = [];
        }
        callback(searchIndex);
      })
      .catch(() => {
        searchIndex = [];
        callback(searchIndex);
      });
  }

  function addSearchAutocomplete(input) {
    if (!input) return;
    // Pages with their own local dataset search (e.g. the art gallery) opt out
    // of the site-wide search-index.json autocomplete via data-local-search.
    if (input.hasAttribute('data-local-search')) return;
    if (input.dataset.ttsAutocompleteAdded) return;
    input.dataset.ttsAutocompleteAdded = 'true';

    // Create suggestions container
    const container = document.createElement('div');
    container.className = 'search-suggestions';
    container.setAttribute('role', 'listbox');
    container.setAttribute('aria-label', 'Search suggestions');
    input.parentNode.appendChild(container);

    let activeIndex = -1;
    let currentSuggestions = [];

    function showSuggestions(suggestions, query) {
      container.innerHTML = '';
      currentSuggestions = suggestions;
      activeIndex = -1;

      if (suggestions.length === 0) {
        if (query && query.length >= 2) {
          const empty = document.createElement('div');
          empty.className = 'search-suggestion search-suggestion-empty';
          empty.setAttribute('role', 'option');
          empty.setAttribute('aria-disabled', 'true');
          empty.textContent = 'No matches';
          container.appendChild(empty);
          container.classList.add('active');
          return;
        }
        container.classList.remove('active');
        return;
      }

      suggestions.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = 'search-suggestion';
        div.setAttribute('role', 'option');
        div.setAttribute('aria-selected', 'false');
        div.dataset.index = i;

        const title = item.title || item.name || item.text || '';
        const desc = (item.summary || item.content || '').substring(0, 80);
        const url = item.url || item.link || '';

        div.innerHTML = `
          <span class="ss-title">${esc(title)}</span>
          ${desc ? `<span class="ss-desc">${esc(desc)}</span>` : ''}
        `;

        div.addEventListener('mousedown', (e) => {
          e.preventDefault();
          if (url) {
            window.location.href = url;
          } else {
            input.value = title;
            container.classList.remove('active');
            // Trigger search if there's a search button
            const form = input.closest('form');
            if (form) form.submit();
          }
        });

        div.addEventListener('mouseenter', () => {
          container.querySelectorAll('.search-suggestion').forEach(el => {
            el.classList.remove('selected');
            el.setAttribute('aria-selected', 'false');
          });
          div.classList.add('selected');
          div.setAttribute('aria-selected', 'true');
          activeIndex = i;
        });

        container.appendChild(div);
      });

      container.classList.add('active');
    }

    // Simple fuzzy match
    function fuzzyMatch(text, query) {
      if (!query || query.length < 2) return false;
      const lower = text.toLowerCase();
      const q = query.toLowerCase();
      // Direct substring
      if (lower.includes(q)) return true;
      // Character-by-character fuzzy
      let qi = 0;
      for (let i = 0; i < lower.length && qi < q.length; i++) {
        if (lower[i] === q[qi]) qi++;
      }
      return qi === q.length;
    }

    function score(pattern, text) {
      const lower = text.toLowerCase();
      const q = pattern.toLowerCase();
      // Exact match at start = highest
      if (lower.startsWith(q)) return 100 + q.length;
      // Contains match
      if (lower.includes(q)) return 50 + q.length;
      // Fuzzy
      return 10;
    }

    input.addEventListener('input', function () {
      const val = this.value.trim();
      if (val.length < 2) {
        container.classList.remove('active');
        return;
      }

      loadSearchIndex((index) => {
        const scored = [];
        index.forEach(item => {
          const title = item.title || item.name || item.text || '';
          const desc = item.summary || item.content || '';
          const combined = title + ' ' + desc;
          if (fuzzyMatch(combined, val)) {
            scored.push({ item, score: score(val, title) + score(val, desc) / 10 });
          }
        });

        scored.sort((a, b) => b.score - a.score);
        const top = scored.slice(0, 8).map(s => s.item);
        showSuggestions(top, val);
      });
    });

    input.addEventListener('keydown', function (e) {
      const items = container.querySelectorAll('.search-suggestion');
      if (items.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
        updateSelection(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, -1);
        updateSelection(items);
      } else if (e.key === 'Enter' && activeIndex >= 0) {
        e.preventDefault();
        items[activeIndex].querySelector('span')?.click();
        items[activeIndex].dispatchEvent(new MouseEvent('mousedown'));
      } else if (e.key === 'Escape') {
        container.classList.remove('active');
      }
    });

    function updateSelection(items) {
      items.forEach((el, i) => {
        el.classList.toggle('selected', i === activeIndex);
        el.setAttribute('aria-selected', i === activeIndex ? 'true' : 'false');
      });
      if (activeIndex >= 0) {
        items[activeIndex].scrollIntoView({ block: 'nearest' });
      }
    }

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (!container.contains(e.target) && e.target !== input) {
        container.classList.remove('active');
      }
    });
  }

  // ═══════════════════════════════════════════════
  // 6. IMAGE LAZY LOADING
  // ═══════════════════════════════════════════════

  function addLazyLoading() {
    document.querySelectorAll('img:not([loading])').forEach(img => {
      // Skip small icons, logos, and inline images
      if (img.closest('nav, .profile-links, .footer-links, .hero-glitch-canvas')) return;
      if (img.width <= 48 && img.height <= 48) return;
      img.loading = 'lazy';
    });
  }

  // ═══════════════════════════════════════════════
  // 7. EXTERNAL LINK HANDLING
  // ═══════════════════════════════════════════════

  function addExternalLinkAttributes() {
    const host = window.location.hostname;
    document.querySelectorAll('a[href^="http"]').forEach(a => {
      try {
        const url = new URL(a.href);
        if (url.hostname !== host) {
          if (!a.rel) {
            a.rel = 'noopener noreferrer';
          } else if (!a.rel.includes('noopener')) {
            a.rel += ' noopener noreferrer';
          }
          a.target = a.target || '_blank';
        }
      } catch (_) { /* ignore malformed URLs */ }
    });
  }

  // ═══════════════════════════════════════════════
  // 8. NAV TOGGLE (replaces inline onclick handlers)
  // ═══════════════════════════════════════════════

  /**
   * Wires up the .menu-btn button to toggle .nav-links.open.
   * Replaces the inline onclick handler that was on 21+ pages.
   * Also handles keyboard activation (Enter/Space) for a11y.
   */
  function initNavToggle() {
    const btn = document.querySelector('.menu-btn');
    if (!btn) return;
    // Don't double-wire if the button already has a listener
    if (btn.dataset.navToggleWired) return;
    btn.dataset.navToggleWired = 'true';

    function toggle() {
      const navLinks = document.querySelector('.nav-links');
      if (!navLinks) return;
      const isOpen = navLinks.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(isOpen));
    }

    btn.addEventListener('click', toggle);
  }

  /**
   * Wires up tab-switching buttons on the homepage.
   * Replaces inline onclick="showTab(event,'video')" handlers.
   * Looks for buttons with data-tab attribute.
   */
  function initTabSwitcher() {
    const tabButtons = document.querySelectorAll('[data-tab]');
    if (tabButtons.length === 0) return;

    tabButtons.forEach(function (btn) {
      if (btn.dataset.tabWired) return;
      btn.dataset.tabWired = 'true';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const tabName = btn.getAttribute('data-tab');
        if (!tabName) return;
        // Call the existing showTab function if it exists
        if (typeof window.showTab === 'function') {
          window.showTab(e, tabName);
        }
      });
    });
  }

  /**
   * Wires up publication filter buttons.
   * Replaces inline onclick="setTypeFilter('Paper',this)" etc.
   */
  function initPublicationFilters() {
    // Type filter buttons
    const typeButtons = document.querySelectorAll('[data-type-filter]');
    typeButtons.forEach(function (btn) {
      if (btn.dataset.filterWired) return;
      btn.dataset.filterWired = 'true';
      btn.setAttribute('aria-pressed', String(btn.classList.contains('active')));
      btn.addEventListener('click', function () {
        const filter = btn.getAttribute('data-type-filter');
        if (!filter) return;
        if (typeof window.setTypeFilter === 'function') {
          window.setTypeFilter(filter, btn);
        }
      });
    });

    // Year/venue selects
    const yearSelect = document.querySelector('[data-year-filter]');
    if (yearSelect && !yearSelect.dataset.filterWired) {
      yearSelect.dataset.filterWired = 'true';
      yearSelect.addEventListener('change', function () {
        if (typeof window.setYearFilter === 'function') {
          window.setYearFilter(this.value);
        }
      });
    }

    const venueSelect = document.querySelector('[data-venue-filter]');
    if (venueSelect && !venueSelect.dataset.filterWired) {
      venueSelect.dataset.filterWired = 'true';
      venueSelect.addEventListener('change', function () {
        if (typeof window.setVenueFilter === 'function') {
          window.setVenueFilter(this.value);
        }
      });
    }

    // Generic filterPubs selects
    const filterSelects = document.querySelectorAll('[data-filter-pubs]');
    filterSelects.forEach(function (sel) {
      if (sel.dataset.filterWired) return;
      sel.dataset.filterWired = 'true';
      sel.addEventListener('change', function () {
        if (typeof window.filterPubs === 'function') {
          window.filterPubs();
        }
      });
    });
  }

  /**
   * Wires up art gallery controls (size buttons, lightbox).
   * Replaces inline onclick handlers in art.html.
   */
  function initArtGallery() {
    // Size buttons
    const sizeButtons = document.querySelectorAll('[data-set-size]');
    sizeButtons.forEach(function (btn) {
      if (btn.dataset.artWired) return;
      btn.dataset.artWired = 'true';
      btn.addEventListener('click', function () {
        const size = btn.getAttribute('data-set-size');
        if (!size) return;
        if (typeof window.setSize === 'function') {
          window.setSize(size);
        }
      });
    });

    // Gallery filter select
    const galleryFilter = document.querySelector('[data-filter-gallery]');
    if (galleryFilter && !galleryFilter.dataset.artWired) {
      galleryFilter.dataset.artWired = 'true';
      galleryFilter.addEventListener('change', function () {
        if (typeof window.filterGallery === 'function') {
          window.filterGallery();
        }
      });
    }

    // Lightbox controls
    const lightboxActions = document.querySelectorAll('[data-lightbox]');
    lightboxActions.forEach(function (el) {
      if (el.dataset.artWired) return;
      el.dataset.artWired = 'true';
      el.addEventListener('click', function () {
        const action = el.getAttribute('data-lightbox');
        if (action === 'close' && typeof window.closeLightbox === 'function') {
          window.closeLightbox();
        } else if (action === 'prev' && typeof window.navLightbox === 'function') {
          window.navLightbox(-1);
        } else if (action === 'next' && typeof window.navLightbox === 'function') {
          window.navLightbox(1);
        }
      });
    });
  }

  /**
   * Wires up publication domain filters, sort buttons, and reset.
   * Replaces inline onclick handlers in publications.html.
   */
  function initPublicationAdvanced() {
    // Domain filter buttons
    const domainButtons = document.querySelectorAll('[data-domain-filter]');
    domainButtons.forEach(function (btn) {
      if (btn.dataset.filterWired) return;
      btn.dataset.filterWired = 'true';
      btn.setAttribute('aria-pressed', String(btn.classList.contains('active')));
      btn.addEventListener('click', function () {
        const filter = btn.getAttribute('data-domain-filter');
        if (!filter) return;
        if (typeof window.setDomainFilter === 'function') {
          window.setDomainFilter(filter, btn);
        }
      });
    });

    // Sort buttons
    const sortButtons = document.querySelectorAll('[data-sort-by]');
    sortButtons.forEach(function (btn) {
      if (btn.dataset.filterWired) return;
      btn.dataset.filterWired = 'true';
      btn.addEventListener('click', function () {
        const sortKey = btn.getAttribute('data-sort-by');
        if (!sortKey) return;
        if (typeof window.sortBy === 'function') {
          window.sortBy(sortKey);
        }
      });
    });

    // Reset filters button
    const resetBtn = document.querySelector('[data-reset-filters]');
    if (resetBtn && !resetBtn.dataset.filterWired) {
      resetBtn.dataset.filterWired = 'true';
      resetBtn.addEventListener('click', function () {
        if (typeof window.resetFilters === 'function') {
          window.resetFilters();
        }
      });
    }

    // Form no-submit
    const noSubmitForms = document.querySelectorAll('[data-no-submit]');
    noSubmitForms.forEach(function (form) {
      if (form.dataset.filterWired) return;
      form.dataset.filterWired = 'true';
      form.addEventListener('submit', function (e) {
        e.preventDefault();
      });
    });
  }

  /**
   * Wires up video page channel and zoom controls.
   * Replaces inline onclick handlers in videos.html.
   */
  function initVideoControls() {
    // Channel buttons
    const channelButtons = document.querySelectorAll('[data-channel]');
    channelButtons.forEach(function (btn) {
      if (btn.dataset.videoWired) return;
      btn.dataset.videoWired = 'true';
      btn.addEventListener('click', function () {
        const channel = btn.getAttribute('data-channel');
        if (!channel) return;
        if (typeof window.setChannel === 'function') {
          window.setChannel(channel, btn);
        }
      });
    });

    // Zoom buttons
    const zoomButtons = document.querySelectorAll('[data-zoom]');
    zoomButtons.forEach(function (btn) {
      if (btn.dataset.videoWired) return;
      btn.dataset.videoWired = 'true';
      btn.addEventListener('click', function () {
        const zoom = btn.getAttribute('data-zoom');
        if (zoom === null) return;
        if (typeof window.setZoom === 'function') {
          window.setZoom(parseInt(zoom, 10), btn);
        }
      });
    });
  }

  // ═══════════════════════════════════════════════
  // UTILITY
  // ═══════════════════════════════════════════════

  function esc(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ═══════════════════════════════════════════════
  // INIT
  // ═══════════════════════════════════════════════

  function init() {
    createProgressBar();
    createScrollToTop();
    const shortcuts = createShortcutsOverlay();
    addSectionAnchors();
    addLazyLoading();
    addExternalLinkAttributes();

    // Nav toggle (replaces inline onclick on .menu-btn)
    initNavToggle();

    // Tab switcher (homepage media tabs)
    initTabSwitcher();

    // Publication filters
    initPublicationFilters();

    // Art gallery controls
    initArtGallery();

    // Publication advanced filters (domain, sort, reset)
    initPublicationAdvanced();

    // Video page controls (channel, zoom)
    initVideoControls();

    // Search autocomplete — wire up any search input
    const searchInput = document.querySelector('.search-input, .search-wrap input');
    if (searchInput) {
      addSearchAutocomplete(searchInput);
    }

    // Also watch for dynamically added search inputs
    const observer = new MutationObserver(() => {
      const input = document.querySelector('.search-input, .search-wrap input');
      if (input && !input.dataset.ttsAutocompleteAdded) {
        addSearchAutocomplete(input);
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
