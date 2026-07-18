/* Externalized from videos.html inline script (CSP: script-src 'self'). */
// ═══════════════════════════════════════════════════════════════
//  DATA LAYER
// ═══════════════════════════════════════════════════════════════

const VIDEO_INDEX_URL = 'data/videos-index.json';

// ═══════════════════════════════════════════════════════════════
//  ZOOM / LAYOUT CONSTANTS
// ═══════════════════════════════════════════════════════════════

const ZOOM = [
  { name: 'overview', pxPerDay: 0.5, thumbW: 56, thumbH: 32 },
  { name: 'month',    pxPerDay: 3,   thumbW: 96, thumbH: 54 },
  { name: 'week',     pxPerDay: 14,  thumbW: 160, thumbH: 90 },
];

// track height = (rows * (thumbH + gap)) + axis zone
const TRACK_ROWS = 4;
const ROW_GAP = 4;
const AXIS_ZONE = 28; // space at axis center for year labels
const CANVAS_PADDING = 80; // px left/right margin

// ═══════════════════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════════════════

let allVideos = [];      // combined + sorted
let positions = {};      // videoId → {left, top} per zoom level
let currentZoom = 0;
let channelFilter = 'both';
let searchQuery = '';
let minDate, maxDate, totalDays;
let yearOffsets = {};    // year → leftPx
let imgObserver = null;

// ═══════════════════════════════════════════════════════════════
//  BOOTSTRAP
// ═══════════════════════════════════════════════════════════════

async function init() {
  let payload;
  try {
    const response = await fetch(VIDEO_INDEX_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    payload = await response.json();
  } catch (error) {
    document.getElementById('loading').innerHTML =
      '<p style="color:var(--text-secondary)">Video index unavailable. Run <code>python3 code/orchestrators/build_video_pages.py</code> to generate data.</p>';
    return;
  }

  const personalVideos  = (payload.videos || []).filter(video => video.channel === 'personal');
  const instituteVideos = (payload.videos || []).filter(video => video.channel === 'institute');
  const personalMeta    = payload.channels?.personal || null;
  const instituteMeta   = payload.channels?.institute || null;

  allVideos = [...personalVideos, ...instituteVideos];
  allVideos.sort((a, b) => a.upload_date.localeCompare(b.upload_date));

  if (allVideos.length === 0) {
    document.getElementById('loading').innerHTML =
      '<p style="color:var(--text-secondary)">No video data found. Run <code>python3 code/orchestrators/fetch_youtube_data.py</code> to generate data.</p>';
    return;
  }

  // Date range
  const dates = allVideos.map(v => parseDate(v.upload_date));
  minDate = new Date(Math.min(...dates));
  maxDate = new Date(Math.max(...dates));
  // Pad by 30 days on each side
  minDate.setDate(minDate.getDate() - 30);
  maxDate.setDate(maxDate.getDate() + 30);
  totalDays = Math.ceil((maxDate - minDate) / 86400000);

  // Hero stats
  const heroStats = document.getElementById('hero-stats');
  const pCount = personalVideos.length;
  const iCount = instituteVideos.length;
  const pRange = pCount ? `${personalVideos[0].year}–${personalVideos[personalVideos.length-1].year}` : '—';
  const iRange = iCount ? `${instituteVideos[0].year}–${instituteVideos[instituteVideos.length-1].year}` : '—';
  const fetchDate = personalMeta ? personalMeta.fetched_at.slice(0,10) : (instituteMeta ? instituteMeta.fetched_at.slice(0,10) : '');
  heroStats.innerHTML = `<span>${pCount}</span> personal videos (${pRange}) · <span>${iCount}</span> institute videos (${iRange}) · <span>${allVideos.length}</span> total · data from ${fetchDate}`;

  // Populate year jump
  buildYearJump();

  // Pre-compute positions for all zoom levels
  computeAllPositions();

  // Render
  document.getElementById('loading').style.display = 'none';
  document.getElementById('timeline-wrap').style.display = 'block';
  document.getElementById('status-bar').style.display = 'flex';

  buildTimeline();
  buildMobileList();
  setupInteractions();
  updateCount();

  // Read URL params (may re-zoom/filter, so do after setup)
  applyUrlParams();

  // Scroll to first video unless URL already specifies a state
  if (!location.search) {
    const firstDate = allVideos[0]?.upload_date;
    if (firstDate) {
      const wrap = document.getElementById('timeline-wrap');
      const x = CANVAS_PADDING + dayOffset(firstDate) * ZOOM[currentZoom].pxPerDay;
      wrap.scrollLeft = Math.max(0, x - wrap.clientWidth * 0.15);
    }
  }
}

// ═══════════════════════════════════════════════════════════════
//  DATE HELPERS
// ═══════════════════════════════════════════════════════════════

function parseDate(yyyymmdd) {
  const y = yyyymmdd.slice(0,4), m = yyyymmdd.slice(4,6), d = yyyymmdd.slice(6,8);
  return new Date(Date.UTC(+y, +m-1, +d));
}

function dayOffset(yyyymmdd) {
  return Math.floor((parseDate(yyyymmdd) - minDate) / 86400000);
}

function fmtDate(yyyymmdd) {
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const m = parseInt(yyyymmdd.slice(4,6), 10) - 1;
  return `${months[m]} ${yyyymmdd.slice(0,4)}`;
}

// ═══════════════════════════════════════════════════════════════
//  POSITION COMPUTATION
// ═══════════════════════════════════════════════════════════════

function computeAllPositions() {
  positions = {};
  for (let z = 0; z < ZOOM.length; z++) {
    const { pxPerDay, thumbW, thumbH } = ZOOM[z];
    const rowH = thumbH + ROW_GAP;
    const trackH = TRACK_ROWS * rowH;
    const canvasH = 2 * trackH + AXIS_ZONE;
    const axisMid = trackH + AXIS_ZONE / 2;

    // Separate by channel, maintain order (already date-sorted)
    const personalVideos  = allVideos.filter(v => v.channel === 'personal');
    const instituteVideos = allVideos.filter(v => v.channel === 'institute');

    [personalVideos, instituteVideos].forEach((group, gi) => {
      group.forEach((v, idx) => {
        const left = CANVAS_PADDING + dayOffset(v.upload_date) * pxPerDay - thumbW / 2;
        const row = idx % TRACK_ROWS;
        let top;
        if (gi === 0) {
          // personal: above axis → positioned from axis upward
          top = axisMid - ROW_GAP - (row + 1) * rowH;
        } else {
          // institute: below axis → positioned from axis downward
          top = axisMid + AXIS_ZONE / 2 + row * rowH + ROW_GAP;
        }
        if (!positions[v.id]) positions[v.id] = {};
        positions[v.id][z] = { left, top, canvasH };
      });
    });
  }
}

function canvasWidth(zoom) {
  return CANVAS_PADDING * 2 + totalDays * ZOOM[zoom].pxPerDay;
}

function canvasHeight(zoom) {
  const { thumbH } = ZOOM[zoom];
  const rowH = thumbH + ROW_GAP;
  return 2 * TRACK_ROWS * rowH + AXIS_ZONE + 20;
}

// ═══════════════════════════════════════════════════════════════
//  TIMELINE BUILD
// ═══════════════════════════════════════════════════════════════

function buildTimeline() {
  const wrap = document.getElementById('timeline-wrap');
  const canvas = document.getElementById('timeline-canvas');
  const z = currentZoom;
  const { pxPerDay, thumbW, thumbH } = ZOOM[z];
  const cw = canvasWidth(z);
  const ch = canvasHeight(z);

  wrap.style.height = (ch + 16) + 'px';
  canvas.style.width = cw + 'px';
  canvas.style.height = ch + 'px';

  const rowH = thumbH + ROW_GAP;
  const trackH = TRACK_ROWS * rowH;
  const axisMid = trackH + AXIS_ZONE / 2;

  canvas.innerHTML = '';

  // Axis line
  const axis = document.createElement('div');
  axis.className = 'axis-line';
  axis.style.top = axisMid + 'px';
  canvas.appendChild(axis);

  // Track labels (sticky)
  const lblP = document.createElement('div');
  lblP.className = 'track-label track-label-personal';
  lblP.style.cssText = `position:absolute;top:${axisMid - trackH + 4}px;left:1rem;`;
  lblP.textContent = '▲ Personal';
  canvas.appendChild(lblP);

  const lblI = document.createElement('div');
  lblI.className = 'track-label track-label-institute';
  lblI.style.cssText = `position:absolute;top:${axisMid + AXIS_ZONE / 2 + 4}px;left:1rem;`;
  lblI.textContent = '▼ Institute';
  canvas.appendChild(lblI);

  // Year markers + month ticks
  yearOffsets = {};
  const startYear = minDate.getUTCFullYear();
  const endYear   = maxDate.getUTCFullYear() + 1;

  for (let yr = startYear; yr <= endYear; yr++) {
    const yearDate = new Date(Date.UTC(yr, 0, 1));
    if (yearDate < minDate) continue;
    const xPx = CANVAS_PADDING + Math.floor((yearDate - minDate) / 86400000) * pxPerDay;
    yearOffsets[yr] = xPx;

    const ym = document.createElement('div');
    ym.className = 'year-marker';
    ym.style.cssText = `left:${xPx}px;top:${axisMid - 10}px;`;
    ym.innerHTML = `<div class="year-tick" style="height:20px"></div><div class="year-label">${yr}</div>`;
    canvas.appendChild(ym);

    // Month ticks (only at zoom >= 1)
    if (z >= 1) {
      for (let mo = 1; mo <= 11; mo++) {
        const moDate = new Date(Date.UTC(yr, mo, 1));
        const mxPx = CANVAS_PADDING + Math.floor((moDate - minDate) / 86400000) * pxPerDay;
        const mt = document.createElement('div');
        mt.className = 'month-tick';
        mt.style.cssText = `left:${mxPx}px;top:${axisMid - 5}px;height:10px;`;
        canvas.appendChild(mt);
      }
    }
  }

  // Video cards
  if (imgObserver) imgObserver.disconnect();
  imgObserver = new IntersectionObserver(onImgIntersect, {
    root: wrap,
    rootMargin: '0px 600px 0px 600px',
    threshold: 0,
  });

  allVideos.forEach((v, i) => {
    const pos = positions[v.id]?.[z];
    if (!pos) return;

    const card = document.createElement('a');
    card.className = `vid-card vid-${v.channel}`;
    card.href = `videos/${v.channel}-${v.id}.html`;
    card.dataset.id = v.id;
    card.dataset.channel = v.channel;
    card.dataset.year = v.year;
    card.dataset.date = v.upload_date;
    card.dataset.title = v.title;
    card.dataset.query = v.title.toLowerCase();
    card.setAttribute('aria-label', `${v.title} (${fmtDate(v.upload_date)})`);
    card.style.cssText = `left:${pos.left}px;top:${pos.top}px;width:${thumbW}px;height:${thumbH}px;`;

    const img = document.createElement('img');
    img.dataset.src = `https://img.youtube.com/vi/${v.id}/mqdefault.jpg`;
    img.alt = v.title;
    img.className = 'placeholder';
    img.width = thumbW;
    img.height = thumbH;
    card.appendChild(img);

    canvas.appendChild(card);
    imgObserver.observe(img);
  });

  applyFilter();
}

function onImgIntersect(entries) {
  entries.forEach(entry => {
    const img = entry.target;
    if (entry.isIntersecting && img.dataset.src) {
      img.src = img.dataset.src;
      img.classList.remove('placeholder');
      imgObserver.unobserve(img);
    }
  });
}

// ═══════════════════════════════════════════════════════════════
//  MOBILE LIST
// ═══════════════════════════════════════════════════════════════

function buildMobileList() {
  const container = document.getElementById('mobile-list');
  const groups = { personal: [], institute: [] };
  allVideos.forEach(v => groups[v.channel].push(v));

  container.innerHTML = '';
  [['personal','▲ Personal Channel'],['institute','▼ Active Inference Institute']].forEach(([ch, label]) => {
    const sec = document.createElement('div');
    sec.className = 'mobile-channel-section';
    const hdr = document.createElement('div');
    hdr.className = `mobile-channel-title ${ch}`;
    hdr.textContent = label;
    sec.appendChild(hdr);

    groups[ch].slice().reverse().forEach(v => {
      const a = document.createElement('a');
      a.className = 'mobile-vid-item';
      a.href = `videos/${v.channel}-${v.id}.html`;
      a.dataset.query = v.title.toLowerCase();

      const img = document.createElement('img');
      img.src = `https://img.youtube.com/vi/${v.id}/mqdefault.jpg`;
      img.alt = v.title;
      img.loading = 'lazy';
      img.width = 80; img.height = 45;

      const meta = document.createElement('div');
      meta.className = 'mobile-vid-meta';

      const title = document.createElement('div');
      title.className = 'mobile-vid-title';
      title.textContent = v.title;

      const date = document.createElement('div');
      date.className = 'mobile-vid-date';
      date.textContent = fmtDate(v.upload_date);

      meta.appendChild(title);
      meta.appendChild(date);
      a.appendChild(img);
      a.appendChild(meta);
      sec.appendChild(a);
    });
    container.appendChild(sec);
  });
}

function filterMobileList() {
  document.querySelectorAll('#mobile-list .mobile-channel-section').forEach(sec => {
    const titleEl = sec.querySelector('.mobile-channel-title');
    const chOk = channelFilter === 'both' || (titleEl && titleEl.classList.contains(channelFilter));
    sec.querySelectorAll('.mobile-vid-item').forEach(item => {
      const qOk = !searchQuery || item.dataset.query.includes(searchQuery);
      item.style.display = (chOk && qOk) ? 'flex' : 'none';
    });
  });
}

// ═══════════════════════════════════════════════════════════════
//  FILTER
// ═══════════════════════════════════════════════════════════════

function applyFilter() {
  const cards = document.querySelectorAll('.vid-card');
  let visible = 0;
  cards.forEach(card => {
    const ch = card.dataset.channel;
    const chOk = channelFilter === 'both' || ch === channelFilter;
    const qOk  = !searchQuery || card.dataset.query.includes(searchQuery);
    const show = chOk && qOk;
    card.style.display = show ? 'block' : 'none';
    if (show) visible++;
  });
  filterMobileList();
  updateCount(visible);
}

function updateCount(visible) {
  const badge = document.getElementById('count-badge');
  const status = document.getElementById('status-text');
  const total = allVideos.length;
  if (visible === undefined) visible = total;
  badge.innerHTML = `<strong>${visible}</strong> / ${total} videos`;
  status.innerHTML = `Showing <strong>${visible}</strong> of <strong>${total}</strong> videos`;
}

// ═══════════════════════════════════════════════════════════════
//  CONTROLS
// ═══════════════════════════════════════════════════════════════

function setZoom(level, btn) {
  const wrap = document.getElementById('timeline-wrap');
  // Preserve center date across zoom
  const centerPx = wrap.scrollLeft + wrap.clientWidth / 2;
  const oldPpd = ZOOM[currentZoom].pxPerDay;
  const centerDay = (centerPx - CANVAS_PADDING) / oldPpd;

  currentZoom = level;
  document.querySelectorAll('[data-zoom]').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  buildTimeline();

  const newPpd = ZOOM[level].pxPerDay;
  const newCenter = CANVAS_PADDING + centerDay * newPpd;
  wrap.scrollLeft = newCenter - wrap.clientWidth / 2;

  pushUrlState();
}

function setChannel(ch, btn) {
  channelFilter = ch;
  document.querySelectorAll('[data-ch]').forEach(b => {
    b.classList.remove('active', 'active-red');
  });
  if (ch === 'institute') {
    btn.classList.add('active-red');
  } else {
    btn.classList.add('active');
  }
  applyFilter();
  pushUrlState();
}

function buildYearJump() {
  const sel = document.getElementById('year-jump');
  const years = [...new Set(allVideos.map(v => v.year))].sort();
  years.forEach(yr => {
    const opt = document.createElement('option');
    opt.value = yr; opt.textContent = yr;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => {
    const yr = parseInt(sel.value);
    if (!yr) return;
    jumpToYear(yr);
    sel.value = '';
  });
}

function jumpToYear(year) {
  const wrap = document.getElementById('timeline-wrap');
  const x = yearOffsets[year];
  if (x !== undefined) {
    wrap.scrollLeft = x - 80;
  }
}

// ═══════════════════════════════════════════════════════════════
//  INTERACTIONS
// ═══════════════════════════════════════════════════════════════

function setupInteractions() {
  // Search
  const searchInput = document.getElementById('search');
  searchInput.addEventListener('input', () => {
    searchQuery = searchInput.value.trim().toLowerCase();
    applyFilter();
    pushUrlState();
  });

  // Mouse wheel: horizontal scroll normally; Ctrl/Cmd+wheel zooms
  const wrap = document.getElementById('timeline-wrap');
  wrap.addEventListener('wheel', e => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      const newZ = e.deltaY < 0
        ? Math.min(currentZoom + 1, ZOOM.length - 1)
        : Math.max(currentZoom - 1, 0);
      if (newZ !== currentZoom) {
        const zBtn = document.querySelector(`[data-zoom="${newZ}"]`);
        setZoom(newZ, zBtn);
      }
    } else if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) {
      // Route vertical scroll to horizontal scroll on the timeline
      e.preventDefault();
      wrap.scrollLeft += e.deltaY;
    }
  }, { passive: false });

  // Keyboard navigation
  wrap.addEventListener('keydown', e => {
    const mth = ZOOM[currentZoom].pxPerDay * 30;
    if (e.key === 'ArrowRight') { e.preventDefault(); wrap.scrollLeft += mth; }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); wrap.scrollLeft -= mth; }
  });

  // Drag-to-scroll
  let isDragging = false, dragStart = 0, scrollStart = 0;
  wrap.addEventListener('mousedown', e => {
    if (e.target.closest('.vid-card')) return;
    isDragging = true; dragStart = e.clientX; scrollStart = wrap.scrollLeft;
  });
  document.addEventListener('mousemove', e => {
    if (!isDragging) return;
    wrap.scrollLeft = scrollStart - (e.clientX - dragStart);
  });
  document.addEventListener('mouseup', () => { isDragging = false; });
}

// ═══════════════════════════════════════════════════════════════
//  URL STATE
// ═══════════════════════════════════════════════════════════════

function pushUrlState() {
  const params = new URLSearchParams();
  if (searchQuery) params.set('q', searchQuery);
  if (channelFilter !== 'both') params.set('ch', channelFilter);
  if (currentZoom !== 0) params.set('z', currentZoom);
  history.replaceState(null, '', params.toString() ? '?' + params : location.pathname);
}

function applyUrlParams() {
  const params = new URLSearchParams(location.search);
  if (params.get('q')) {
    searchQuery = params.get('q');
    document.getElementById('search').value = searchQuery;
  }
  if (params.get('ch') && params.get('ch') !== 'both') {
    const btn = document.querySelector(`[data-ch="${params.get('ch')}"]`);
    if (btn) setChannel(params.get('ch'), btn);
  }
  if (params.get('z')) {
    const z = parseInt(params.get('z'));
    const btn = document.querySelector(`[data-zoom="${z}"]`);
    if (btn) setZoom(z, btn);
  }
  applyFilter();
}

// ── GO ──
init().catch(err => {
  console.error(err);
  document.getElementById('loading').innerHTML =
    `<p style="color:var(--red)">Error loading data: ${err.message}</p>
     <p style="color:var(--text-secondary);font-size:.82rem;margin-top:.5rem">Run <code>python3 code/orchestrators/fetch_youtube_data.py</code> to generate video data, then serve locally with <code>python3 -m http.server 8080</code></p>`;
});
