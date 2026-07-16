/**
 * Art Gallery — externalized from art.html inline script (CSP: script-src 'self').
 * Loads data/artworks.json (942 pieces), renders the grid, and drives the
 * page-local search / sort / size / lightbox controls via addEventListener.
 * window.filterGallery / window.setSize stay exposed for the data-attribute
 * delegation in js/interactive.js.
 */
(function () {
  'use strict';

  let DATA = [];
  let filtered = [];
  let currentIdx = 0;

  const grid = document.getElementById('grid');
  const lb = document.getElementById('lightbox');

  async function loadGalleryData() {
    try {
      const res = await fetch('data/artworks.json', { cache: 'default' });
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

  // Lazy-load observer
  const imgObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const img = e.target;
      if (!img.dataset.src) return;
      img.src = img.dataset.src;
      img.onload = () => img.classList.add('loaded');
      img.onerror = () => img.classList.add('loaded');
      imgObs.unobserve(img);
    });
  }, { rootMargin: '250px' });

  function esc(s) {
    return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function plain(s) {
    const div = document.createElement('div');
    div.innerHTML = s || '';
    return (div.textContent || div.innerText || '').replace(/\s+/g, ' ').trim();
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
      const card = document.createElement('div');
      card.className = 'art-card';
      card.innerHTML =
        `<img data-src="${esc(art.thumb)}" alt="${esc(artAlt(art))}" class="art-thumb">` +
        `<div class="art-info">` +
        `<div class="art-title" title="${esc(art.title)}">${esc(art.title)}</div>` +
        `<div class="art-meta">${art.date ? art.date.slice(0, 10) : ''}</div>` +
        (art.views ? `<div class="art-views">${parseInt(art.views).toLocaleString()} views</div>` : '') +
        `</div>`;
      card.addEventListener('click', () => openLightbox(i));
      grid.appendChild(card);
      imgObs.observe(card.querySelector('.art-thumb'));
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
    ['sm', 'md', 'lg'].forEach(x => document.getElementById('btn-' + x).classList.toggle('active', x === s));
  }

  // ── LIGHTBOX ──
  const SIZE_ORDER = ['Square', 'Thumbnail', 'Small', 'Small 320', 'Small 400', 'Medium', 'Medium 640', 'Medium 800', 'Large', 'Large 1600', 'Large 2048', 'X-Large 3K', 'X-Large 4K', 'X-Large 5K', 'Original'];

  function openLightbox(i) {
    currentIdx = i;
    populate(filtered[i]);
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function populate(art) {
    document.getElementById('lb-title').textContent = art.title || 'Untitled';
    document.getElementById('lb-date').textContent = art.date ? art.date.slice(0, 10) : '';
    document.getElementById('lb-desc').textContent = art.desc || '';

    const mainSrc = art.sizes['Large 1600'] || art.sizes['Large'] || art.sizes['Medium 640'] || art.sizes['Medium'] || art.thumb;
    const img = document.getElementById('lb-img');
    img.style.opacity = '0';
    img.src = mainSrc;
    img.alt = artAlt(art);
    img.onload = () => { img.style.opacity = '1'; };

    const origUrl = art.sizes['Original'] || art.sizes['Large 2048'] || art.sizes['X-Large 4K'] || mainSrc;
    document.getElementById('lb-download').href = origUrl;

    const flickrBtn = document.getElementById('lb-flickr-link');
    flickrBtn.href = art.flickr_url || 'https://www.flickr.com/photos/43693624@N07/';

    // Resolutions
    const resList = document.getElementById('lb-resolutions');
    resList.innerHTML = '';
    SIZE_ORDER.forEach(name => {
      const url = art.sizes[name];
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
    document.body.style.overflow = '';
  }

  function navLightbox(dir) {
    currentIdx = (currentIdx + dir + filtered.length) % filtered.length;
    populate(filtered[currentIdx]);
  }

  // ── EVENT WIRING (CSP-safe, no inline handlers) ──
  document.getElementById('searchInput').addEventListener('input', filterGallery);
  document.getElementById('sortSelect').addEventListener('change', filterGallery);
  ['sm', 'md', 'lg'].forEach(s => {
    document.getElementById('btn-' + s).addEventListener('click', () => setSize(s));
  });
  document.querySelector('.lb-close').addEventListener('click', closeLightbox);
  document.querySelector('.lb-prev').addEventListener('click', () => navLightbox(-1));
  document.querySelector('.lb-next').addEventListener('click', () => navLightbox(1));

  document.addEventListener('keydown', e => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') navLightbox(1);
    if (e.key === 'ArrowLeft') navLightbox(-1);
  });
  lb.addEventListener('click', e => { if (e.target === lb) closeLightbox(); });

  // Compat: js/interactive.js delegates [data-set-size]/[data-filter-gallery]/[data-lightbox]
  // clicks to these globals.
  window.filterGallery = filterGallery;
  window.setSize = setSize;
  window.closeLightbox = closeLightbox;
  window.navLightbox = navLightbox;

  loadGalleryData();
})();
