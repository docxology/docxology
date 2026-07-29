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
  const searchIndexWaiting = [];

  function loadSearchIndex(callback) {
    if (searchIndex) { callback(searchIndex); return; }
    // Queue rather than drop: keystrokes arriving while the fetch is in flight
    // used to return early and lose their callback, so the first characters
    // typed on a cold page produced no suggestions at all.
    searchIndexWaiting.push(callback);
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
      })
      .catch(() => {
        searchIndex = [];
      })
      .then(() => {
        searchIndexLoading = false;
        while (searchIndexWaiting.length) {
          searchIndexWaiting.shift()(searchIndex);
        }
      });
  }

  // Cached lowercase haystack per index entry. Rebuilding this for all ~1650
  // entries on every keystroke was the bulk of the autocomplete's cost.
  function autocompleteHaystack(item) {
    if (item._acHay === undefined) {
      item._acHay = (
        (item.title || item.name || item.text || '') + ' ' +
        (item.summary || item.content || '')
      ).toLowerCase();
    }
    return item._acHay;
  }

  // Debounce so a fast typist does not rescan the whole index per keystroke.
  const AUTOCOMPLETE_DEBOUNCE_MS = 120;
  const MAX_SUGGESTIONS = 8;
  let autocompleteSeq = 0;

  function addSearchAutocomplete(input) {
    if (!input) return;
    // Pages with their own local dataset search (e.g. the art gallery) opt out
    // of the site-wide search-index.json autocomplete via data-local-search.
    if (input.hasAttribute('data-local-search')) return;
    if (input.dataset.ttsAutocompleteAdded) return;
    input.dataset.ttsAutocompleteAdded = 'true';

    // The list lives on <body>, not beside the input: on publications.html the
    // field sits inside .filter-row, which the card treatment gives
    // overflow:hidden (clipping the list) and isolation:isolate plus a
    // z-index:1 on every child (painting the filter buttons over it). Escaping
    // to the body sidesteps both without unclipping that row.
    const listId = 'search-suggestions-' + (++autocompleteSeq);
    const container = document.createElement('div');
    container.className = 'search-suggestions';
    container.id = listId;
    container.setAttribute('role', 'listbox');
    container.setAttribute('aria-label', 'Search suggestions');
    document.body.appendChild(container);

    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    input.setAttribute('aria-controls', listId);

    let activeIndex = -1;

    function optionEls() {
      return container.querySelectorAll('.search-suggestion:not(.search-suggestion-empty)');
    }

    // Viewport coordinates, since the container is fixed on <body>. Anchored to
    // the field itself: where the input shares a parent with other controls
    // (search.html), the old `top:100%` dropped the list below the entire panel
    // rather than below the field. Kept in sync while open, because scrolling
    // moves the field out from under it.
    const MIN_LIST_HEIGHT = 120;

    function positionContainer() {
      const r = input.getBoundingClientRect();
      container.style.left = r.left + 'px';
      container.style.width = r.width + 'px';

      const below = window.innerHeight - r.bottom - 8;
      const above = r.top - 8;
      // Drop upward when the field is near the bottom of a short viewport,
      // rather than running the list off-screen.
      if (below < MIN_LIST_HEIGHT && above > below) {
        const height = Math.min(320, above);
        container.style.top = (r.top - height) + 'px';
        container.style.maxHeight = height + 'px';
      } else {
        container.style.top = r.bottom + 'px';
        container.style.maxHeight = Math.max(MIN_LIST_HEIGHT, Math.min(320, below)) + 'px';
      }
    }

    function setOpen(open) {
      container.classList.toggle('active', open);
      input.setAttribute('aria-expanded', String(open));
      if (!open) {
        activeIndex = -1;
        input.removeAttribute('aria-activedescendant');
      }
    }

    function select(i) {
      const items = optionEls();
      activeIndex = i;
      items.forEach((el, n) => {
        const on = n === i;
        el.classList.toggle('selected', on);
        el.setAttribute('aria-selected', String(on));
      });
      if (i >= 0 && items[i]) {
        input.setAttribute('aria-activedescendant', items[i].id);
        items[i].scrollIntoView({ block: 'nearest' });
      } else {
        input.removeAttribute('aria-activedescendant');
      }
    }

    function choose(div) {
      if (div.dataset.url) {
        window.location.href = div.dataset.url;
        return;
      }
      input.value = div.dataset.title || '';
      setOpen(false);
      // Re-run whatever filter the page has bound to this input. The previous
      // form.submit() fought the [data-no-submit] handler and reloaded nothing.
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function showSuggestions(suggestions, query) {
      container.innerHTML = '';
      activeIndex = -1;
      input.removeAttribute('aria-activedescendant');

      if (suggestions.length === 0) {
        if (query && query.length >= 2) {
          const empty = document.createElement('div');
          empty.className = 'search-suggestion search-suggestion-empty';
          empty.setAttribute('role', 'option');
          empty.setAttribute('aria-disabled', 'true');
          empty.textContent = 'No matches';
          container.appendChild(empty);
          positionContainer();
          setOpen(true);
          return;
        }
        setOpen(false);
        return;
      }

      suggestions.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = 'search-suggestion';
        div.id = listId + '-opt-' + i;
        div.setAttribute('role', 'option');
        div.setAttribute('aria-selected', 'false');

        const title = item.title || item.name || item.text || '';
        const desc = (item.summary || item.content || '').substring(0, 80);
        const url = item.url || item.link || '';
        div.dataset.title = title;
        if (url) div.dataset.url = url;

        div.innerHTML = `
          <span class="ss-title">${esc(title)}</span>
          ${desc ? `<span class="ss-desc">${esc(desc)}</span>` : ''}
        `;

        div.addEventListener('mousedown', (e) => {
          e.preventDefault();
          choose(div);
        });
        div.addEventListener('mouseenter', () => select(i));

        container.appendChild(div);
      });

      positionContainer();
      setOpen(true);
    }

    // Every term must appear. The old matcher fell back to a character
    // subsequence spread across title+summary, so any longer query matched
    // most of the index and the list filled with unrelated entries.
    function matchesAll(hay, terms) {
      for (let i = 0; i < terms.length; i++) {
        if (hay.indexOf(terms[i]) === -1) return false;
      }
      return true;
    }

    function scoreItem(hay, title, terms) {
      const t = title.toLowerCase();
      let total = 0;
      for (let i = 0; i < terms.length; i++) {
        const term = terms[i];
        if (t.startsWith(term)) total += 100;
        else if (t.indexOf(term) !== -1) total += 50;
        else if (hay.indexOf(term) !== -1) total += 10;
      }
      return total;
    }

    let debounceTimer = null;
    input.addEventListener('input', function () {
      const val = this.value.trim();
      clearTimeout(debounceTimer);
      if (val.length < 2) {
        setOpen(false);
        return;
      }
      debounceTimer = setTimeout(() => {
        loadSearchIndex((index) => {
          // The box may have moved on while the index loaded.
          if (input.value.trim() !== val) return;
          const terms = val.toLowerCase().split(/\s+/).filter(Boolean);
          const scored = [];
          for (let i = 0; i < index.length; i++) {
            const item = index[i];
            const hay = autocompleteHaystack(item);
            if (!matchesAll(hay, terms)) continue;
            const title = item.title || item.name || item.text || '';
            scored.push({ item, s: scoreItem(hay, title, terms) });
          }
          scored.sort((a, b) => b.s - a.s);
          showSuggestions(scored.slice(0, MAX_SUGGESTIONS).map(x => x.item), val);
        });
      }, AUTOCOMPLETE_DEBOUNCE_MS);
    });

    input.addEventListener('keydown', function (e) {
      if (!container.classList.contains('active')) return;
      const items = optionEls();
      if (items.length === 0) {
        if (e.key === 'Escape') setOpen(false);
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        select(Math.min(activeIndex + 1, items.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        select(Math.max(activeIndex - 1, -1));
      } else if (e.key === 'Enter' && activeIndex >= 0) {
        e.preventDefault();
        choose(items[activeIndex]);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        setOpen(false);
      }
    });

    // Close on blur (deferred so a mousedown on an option still lands) and on
    // any click outside the field.
    input.addEventListener('blur', () => {
      setTimeout(() => setOpen(false), 150);
    });

    document.addEventListener('click', (e) => {
      if (!container.contains(e.target) && e.target !== input) {
        setOpen(false);
      }
    });

    const reposition = () => {
      if (!container.classList.contains('active')) return;
      const r = input.getBoundingClientRect();
      // A fixed list would otherwise keep floating at the coordinates of a
      // field that has been scrolled out of view.
      if (r.bottom < 0 || r.top > window.innerHeight) {
        setOpen(false);
        return;
      }
      positionContainer();
    };
    window.addEventListener('resize', reposition);
    window.addEventListener('scroll', reposition, { passive: true });
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
