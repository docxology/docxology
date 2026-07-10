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