/**
 * Art Gallery — externalized from art.html inline script (CSP: script-src 'self').
 * Loads the compact data/artworks-index.json (942 pieces), renders the grid,
 * and lazily fetches data/artworks.json only when a description search or
 * lightbox detail view needs the full resolution/media record.
 * window.filterGallery / window.setSize stay exposed for the data-attribute
 * delegation in js/interactive.js.
 */
(function () {
  'use strict';

  let DATA = [];
  let filtered = [];
  let currentIdx = 0;
  let DETAIL_DATA = null;
  let detailPromise = null;

  const grid = document.getElementById('grid');
  const lb = document.getElementById('lightbox');

  async function loadGalleryData() {
    try {
      const res = await fetch('data/artworks-index.json', { cache: 'default' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const payload = await res.json();
      DATA = payload.artworks || [];
      filtered = [...DATA];
      filterGallery();
    } catch (err) {
      console.error('Unable to load artwork data', err);
      const empty = document.getElementById('emptyState');
      empty.style.display = 'block';
      empty.textContent = 'Artwork data could not be loaded.';
    }
  }

  async function loadDetailData() {
    if (DETAIL_DATA) return DETAIL_DATA;
    if (!detailPromise) {
      detailPromise = fetch('data/artworks.json', { cache: 'default' })
        .then(res => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        })
        .then(payload => {
          DETAIL_DATA = new Map((payload.artworks || []).map(art => [String(art.id), art]));
          return DETAIL_DATA;
        })
        .catch(err => {
          detailPromise = null;
          throw err;
        });
    }
    return detailPromise;
  }

  async function enrich(art) {
    const details = await loadDetailData();
    return details.get(String(art.id)) || art;
  }

  // Lazy-load observer
  const loadImage = (img) => {
    if (!img || !img.dataset.src || img.src) return;
    img.src = img.dataset.src;
    img.onload = () => img.classList.add('loaded');
    img.onerror = () => {
      img.classList.add('loaded', 'load-error');
      img.alt = `${img.alt} (image unavailable)`;
    };
  };

  const imgObs = 'IntersectionObserver' in window
    ? new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        loadImage(e.target);
        imgObs.unobserve(e.target);
      });
    }, { rootMargin: '400px' })
    : null;

  function esc(s) {
    return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function plain(s) {
    const parsed = new DOMParser().parseFromString(String(s || ''), 'text/html');
    return (parsed.body.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function artAlt(art) {
    const parts = [art.title || 'Untitled artwork', 'pen-and-ink drawing by Daniel Ari Friedman'];
    if (art.date) parts.push('created ' + art.date.slice(0, 10));
    const tags = (art.tags || []).filter(t => !['daniel', 'friedman', 'danielarifriedman', 'art', 'drawing', 'draw', 'paper', 'ink', 'pen'].includes(String(t).toLowerCase())).slice(0, 4);
    if (tags.length) parts.push('tags: ' + tags.join(', '));
    const desc = plain(art.desc || '').slice(0, 120);
    if (desc) parts.push(desc);
    return parts.join('. ');
  }

  // ── RENDER ──
  function renderGrid() {
    grid.innerHTML = '';
    document.getElementById('emptyState').style.display = filtered.length ? 'none' : 'block';
    document.getElementById('resultCount').textContent = filtered.length + ' artworks';
    filtered.forEach((art, i) => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'art-card';
      card.setAttribute('aria-haspopup', 'dialog');
      card.setAttribute('aria-label', `Open artwork: ${art.title || 'Untitled artwork'}`);
      card.innerHTML =
        `<img data-src="${esc(art.thumb)}" alt="${esc(artAlt(art))}" class="art-thumb" loading="lazy" decoding="async">` +
        `<div class="art-info">` +
        `<div class="art-title" title="${esc(art.title)}">${esc(art.title)}</div>` +
        `<div class="art-meta">${art.date ? art.date.slice(0, 10) : ''}</div>` +
        (art.views ? `<div class="art-views">${parseInt(art.views).toLocaleString()} views</div>` : '') +
        `</div>`;
      card.addEventListener('click', () => openLightbox(i, card));
      grid.appendChild(card);
      const image = card.querySelector('.art-thumb');
      if (imgObs) imgObs.observe(image);
      else loadImage(image);
    });
  }

  // ── FILTER + SORT ──
  function filterGallery() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    const sort = document.getElementById('sortSelect').value;
    filtered = DATA.filter(a => {
      if (!q) return true;
      return a.title.toLowerCase().includes(q) ||
        (a.desc || '').toLowerCase().includes(q) ||
        (a.tags || []).some(t => t.toLowerCase().includes(q));
    });
    filtered.sort((a, b) => {
      if (sort === 'newest') return (b.date || '') > (a.date || '') ? 1 : -1;
      if (sort === 'oldest') return (a.date || '') > (b.date || '') ? 1 : -1;
      if (sort === 'title') return a.title.localeCompare(b.title);
      if (sort === 'views') return parseInt(b.views || 0) - parseInt(a.views || 0);
      return 0;
    });
    renderGrid();
  }

  // ── GRID SIZE ──
  function setSize(s) {
    grid.className = 'grid grid-' + s;
    ['sm', 'md', 'lg'].forEach(x => {
      const button = document.getElementById('btn-' + x);
      const active = x === s;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }

  // ── LIGHTBOX ──
  const SIZE_ORDER = ['Square', 'Thumbnail', 'Small', 'Small 320', 'Small 400', 'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600', 'Large 2048', 'X-Large 3K', 'X-Large 4K', 'X-Large 5K', 'Original'];

  let previouslyFocused = null;

  async function openLightbox(i, trigger) {
    currentIdx = i;
    previouslyFocused = trigger || document.activeElement;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    document.getElementById('lb-close')?.focus();
    try {
      populate(await enrich(filtered[i]));
    } catch (err) {
      console.error('Unable to load artwork details', err);
      document.getElementById('lb-desc').textContent = 'Artwork details could not be loaded.';
    }
  }

  function populate(art) {
    document.getElementById('lb-title').textContent = art.title || 'Untitled';
    document.getElementById('lb-date').textContent = art.date ? art.date.slice(0, 10) : '';
    document.getElementById('lb-desc').textContent = art.desc || '';

    const sizes = art.sizes || {};
    const mainSrc = sizes['Large 1600'] || sizes['Large'] || sizes['Medium 640'] || sizes['Medium'] || art.thumb;
    const img = document.getElementById('lb-img');
    img.style.opacity = '0';
    img.src = mainSrc;
    img.alt = artAlt(art);
    img.onload = () => { img.style.opacity = '1'; };

    const origUrl = sizes['Original'] || sizes['Large 2048'] || sizes['X-Large 4K'] || mainSrc;
    document.getElementById('lb-download').href = origUrl;

    const flickrBtn = document.getElementById('lb-flickr-link');
    flickrBtn.href = art.flickr_url || 'https://www.flickr.com/photos/43693624@N07/';

    // Resolutions
    const resList = document.getElementById('lb-resolutions');
    resList.innerHTML = '';
    SIZE_ORDER.forEach(name => {
      const url = sizes[name];
      if (!url) return;
      const row = document.createElement('div');
      row.className = 'res-item';
      const fname = (art.title || 'art').replace(/[^a-z0-9]/gi, '_') + '_' + name.replace(/ /g, '_');
      row.innerHTML =
        `<span class="res-label">${esc(name)}</span>` +
        `<div class="res-actions">` +
        `<a class="res-btn" href="${esc(url)}" target="_blank" rel="noopener">View ↗</a>` +
        `<a class="res-btn" href="${esc(url)}" download="${esc(fname)}.jpg">DL</a>` +
        `</div>`;
      resList.appendChild(row);
    });

    // Tags
    const tagsEl = document.getElementById('lb-tags');
    tagsEl.innerHTML = (art.tags || []).slice(0, 20).map(t => `<span class="lb-tag">${esc(t)}</span>`).join('');

    // Details
    document.getElementById('lb-details').innerHTML =
      `Views: ${parseInt(art.views || 0).toLocaleString()}<br>` +
      `Flickr ID: ${esc(art.id || '—')}<br>` +
      `Media: ${esc(art.media || 'photo')}`;
  }

  function closeLightbox() {
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (previouslyFocused && typeof previouslyFocused.focus === 'function') previouslyFocused.focus();
  }

  async function navLightbox(dir) {
    currentIdx = (currentIdx + dir + filtered.length) % filtered.length;
    try {
      populate(await enrich(filtered[currentIdx]));
    } catch (err) {
      console.error('Unable to load artwork details', err);
    }
  }

  // ── EVENT WIRING (CSP-safe, no inline handlers) ──
  // The sort <select> (data-filter-gallery), size buttons (data-set-size), and
  // lightbox nav/close buttons (data-lightbox) are wired by js/interactive.js's
  // generic delegation, which calls the window.* globals exposed below. Do NOT
  // also addEventListener them here — double-binding advances the lightbox two
  // items per click. Only wire what interactive.js does not handle:
  document.getElementById('searchInput').addEventListener('input', async () => {
    const query = document.getElementById('searchInput').value.trim();
    if (query && !DETAIL_DATA) {
      document.getElementById('resultCount').textContent = 'Loading descriptions…';
      try {
        const details = await loadDetailData();
        DATA = DATA.map(art => details.get(String(art.id)) || art);
      } catch (err) {
        console.error('Unable to load searchable artwork details', err);
      }
    }
    filterGallery();
  });

  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') navLightbox(1);
    if (e.key === 'ArrowLeft') navLightbox(-1);
    if (e.key === 'Tab') {
      const focusable = lb.querySelectorAll('button, a[href], [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  lb.addEventListener('click', e => { if (e.target === lb) closeLightbox(); });

  // js/interactive.js delegates [data-set-size]/[data-filter-gallery]/[data-lightbox]
  // to these globals — they are the sole wiring for those controls.
  window.filterGallery = filterGallery;
  window.setSize = setSize;
  window.closeLightbox = closeLightbox;
  window.navLightbox = navLightbox;

  loadGalleryData();
})();
