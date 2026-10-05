/** Publications table: loads catalog from data/works.json (canonical export of BIBLIOGRAPHY.md). */
// This input owns the publication results and filters. Site-wide autocomplete
// would fetch an unrelated index and cover this local search surface.
document.getElementById('pub-search')?.setAttribute('data-local-search', '');
let PUBS = [];
let catalogLoaded = false;
let enrichmentState = 'idle';
let enrichmentPromise = null;
const SCRIPT_QUERY = (() => {
    const script = document.currentScript || document.querySelector('script[src*="publications.js"]');
    if (!script) return '';
    try {
        return new URL(script.src, window.location.href).search;
    } catch {
        return '';
    }
})();

const DOMAIN_KW = {
    '🐜': 'entomology ants insect',
    '🧠': 'active inference brain fep free energy',
    '🛡️': 'cognitive security',
    '💻': 'computational software',
    '🌍': 'aii active inference institute ecosystem',
    '🎥': 'media video course presentation livestream',
    '🧬': 'genetics genomics biomedical',
    '🎨': 'art synergetics blake buckminster',
};

const DOMAIN_LABELS = {
    '🐜': 'ENT',
    '🧠': 'FEP',
    '🛡️': 'SEC',
    '🛡': 'SEC',
    '💻': 'COM',
    '🌍': 'AII',
    '🎥': 'MED',
    '🧬': 'BIO',
    '🎨': 'ART',
};

let currentTypeFilter = 'all';
let currentDomainFilter = 'all';
let currentYearFilter = 'all';
let currentVenueFilter = 'all';
let currentSort = { col: 'num', dir: 1 };

// Client-side pagination. The first SSR_FLOOR_ROWS rows are already
// server-rendered into the page for crawlers; everything beyond that renders
// on demand ("Load more"), so the table DOM (and per-filter layout work) stays
// bounded while every row remains reachable client-side. Filtering, search,
// and sorting always operate over the full catalog and reset to page 1.
const PAGE_SIZE = 50;
let currentLimit = PAGE_SIZE;

function workToPub(work) {
    const url = work.url || '';
    const citationKey = work.citation_key || '';
    const workPage = citationKey ? `/works/${citationKey}.html` : '';
    const docsPath = work.docs_path ? String(work.docs_path).replace(/\/$/, '') : '';
    const docs =
        work.has_paper_folder && docsPath
            ? `https://github.com/docxology/docxology/tree/main/${docsPath}`
            : '';
    const fullTextUrl = work.has_full_text && docsPath ? `/${docsPath}/full_text.md` : '';
    return {
        num: work.num,
        year: work.year,
        domain: work.domain,
        domainName: work.domain_name || '',
        citationKey,
        authors: work.authors || [],
        type: work.type,
        title: work.title,
        venue: work.venue,
        doi: url,
        docs,
        workPage,
        hasDoi: url.startsWith('https://doi.org/'),
        hasDocs: Boolean(work.has_paper_folder && work.docs_path),
        hasFullText: Boolean(work.has_full_text),
        hasImages: Boolean(work.has_images),
        fullTextUrl,
    };
}

function buildSearchIndex(pub, enrichment) {
    const lab = pub.domain;
    const extra = enrichment || {};
    // Beyond the visible columns, index the spelled-out domain name, the
    // citation key, and the abstract/keywords from work-enrichment.json. Without
    // these, searching a phrase straight out of a paper's own abstract — or the
    // domain label shown in the filter pills — returned nothing.
    pub._search = [
        pub.title,
        pub.venue,
        pub.type,
        pub.doi,
        pub.year,
        pub.domain,
        pub.domainName,
        pub.citationKey,
        pub.authors.join(' '),
        DOMAIN_KW[lab] || '',
        extra.abstract || '',
        (extra.keywords || []).join(' '),
    ]
        .join(' ')
        .toLowerCase();
}

function typeClass(t) {
    const m = {
        Paper: 'type-paper',
        Presentation: 'type-presentation',
        Book: 'type-book',
        Course: 'type-course',
        Series: 'type-series',
        Playbook: 'type-playbook',
    };
    return m[t] || 'type-paper';
}

function domainMatches(pDomain, filterKey) {
    if (filterKey === 'all') return true;
    if (!pDomain || !filterKey) return false;
    return pDomain.indexOf(filterKey) === 0;
}

function populateFilterSelects() {
    const years = Array.from(new Set(PUBS.map((p) => p.year))).sort((a, b) => b - a);
    const venues = Array.from(new Set(PUBS.map((p) => p.venue).filter(Boolean))).sort((a, b) =>
        a.localeCompare(b, undefined, { sensitivity: 'base' }),
    );
    const yearSelect = document.getElementById('year-filter');
    const venueSelect = document.getElementById('venue-filter');
    yearSelect.innerHTML =
        '<option value="all">All years</option>' +
        years.map((y) => `<option value="${y}">${y}</option>`).join('');
    venueSelect.innerHTML =
        '<option value="all">All venues</option>' +
        venues.map((v) => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
}

function cmpSort(a, b, col, dir) {
    let va;
    let vb;
    if (col === 'num' || col === 'year') {
        va = a[col];
        vb = b[col];
        if (va < vb) return -1 * dir;
        if (va > vb) return 1 * dir;
        return 0;
    }
    va = a[col] == null ? '' : String(a[col]);
    vb = b[col] == null ? '' : String(b[col]);
    let r = va.localeCompare(vb, undefined, { sensitivity: 'base' });
    if (r === 0) r = a.num - b.num;
    return r * dir;
}

function updateSortUI() {
    document.querySelectorAll('thead th[data-sortable]').forEach((th) => {
        th.classList.remove('sorted');
        const b = th.querySelector('.th-sort-btn');
        const icon = th.querySelector('.sort-icon');
        if (!b || !icon) return;
        th.removeAttribute('aria-sort');
        b.setAttribute('aria-label', `Sort by ${th.textContent.replace(/[↕↑↓]/g, '').trim()}`);
        const col = th.getAttribute('data-sortable');
        if (col === currentSort.col) {
            th.classList.add('sorted');
            th.setAttribute('aria-sort', currentSort.dir < 0 ? 'descending' : 'ascending');
            b.setAttribute('aria-label', `Sorted by ${th.textContent.replace(/[↕↑↓]/g, '').trim()} ${currentSort.dir < 0 ? 'descending' : 'ascending'}`);
            icon.textContent = currentSort.dir < 0 ? '\u2193' : '\u2191';
        } else {
            icon.textContent = '\u2195';
        }
    });
}

function renderTable() {
    // Preserve the server-rendered native links while the catalog is loading
    // or unavailable; early filter interactions must not erase that fallback.
    if (!catalogLoaded) return;
    const table = document.getElementById('pub-table');
    if (table) table.setAttribute('aria-busy', 'true');
    const q = (document.getElementById('pub-search').value || '').toLowerCase().trim();
    const terms = q ? q.split(/\s+/).filter((t) => t.length > 0) : [];
    const doiOnly = document.getElementById('doi-filter').checked;
    const docsOnly = document.getElementById('docs-filter').checked;
    let data = PUBS.filter((p) => {
        if (!domainMatches(p.domain, currentDomainFilter)) return false;
        if (currentTypeFilter !== 'all' && p.type !== currentTypeFilter) return false;
        if (currentYearFilter !== 'all' && String(p.year) !== currentYearFilter) return false;
        if (currentVenueFilter !== 'all' && p.venue !== currentVenueFilter) return false;
        if (doiOnly && !p.hasDoi) return false;
        if (docsOnly && !p.hasDocs) return false;
        if (terms.length === 0) return true;
        const s = p._search;
        for (let i = 0; i < terms.length; i++) {
            if (s.indexOf(terms[i]) === -1) return false;
        }
        return true;
    });
    data = data.slice().sort((a, b) => cmpSort(a, b, currentSort.col, currentSort.dir));
    const tbody = document.getElementById('pub-tbody');
    const empty = document.getElementById('no-results');
    const shown = data.slice(0, currentLimit);
    const loadMore = ensureLoadMoreButton(tbody);
    if (loadMore) {
        loadMore.hidden = data.length <= currentLimit;
        // The shared .btn display rule overrides the browser's hidden style.
        loadMore.classList.toggle('d-none', loadMore.hidden);
        loadMore.textContent = `Load more (${data.length - shown.length} of ${data.length} remaining)`;
    }
    if (data.length === 0) {
        tbody.innerHTML = '';
        const incomplete = q && enrichmentState !== 'ready';
        empty.hidden = Boolean(incomplete);
        empty.classList.toggle('d-none', Boolean(incomplete));
    } else {
        empty.hidden = true;
        empty.classList.add('d-none');
        tbody.innerHTML = shown
            .map((p) => {
                const title = esc(p.title);
                const titleCell = p.workPage
                    ? `<a href="${esc(p.workPage)}">${title}</a>`
                    : `<a href="${esc(p.doi || p.docs || '#')}" target="_blank" rel="noopener">${title}</a>`;
                const primary = p.doi
                    ? `<a href="${esc(p.doi)}" target="_blank" rel="noopener">→ Link</a>`
                    : '<span aria-label="No primary link">—</span>';
                const docs = p.docs
                    ? ` <a href="${esc(p.docs)}" target="_blank" rel="noopener">Docs</a>`
                    : '';
                const ft = p.hasFullText
                    ? ` <a href="${esc(p.fullTextUrl)}" title="Full text extraction">FT</a>`
                    : '';
                const img = p.hasImages ? ' <span class="badge-img" title="Has extracted images">🖼</span>' : '';
                return (
                    '<tr>' +
                    `<td class="td-num">${p.num}</td>` +
                    `<td class="td-year">${p.year}</td>` +
                    `<td class="td-domain">${esc(DOMAIN_LABELS[p.domain] || p.domain)}</td>` +
                    `<td class="td-type"><span class="type-badge ${typeClass(p.type)}">${esc(p.type)}</span></td>` +
                    `<td class="td-title">${titleCell}</td>` +
                    `<td class="td-venue">${esc(p.venue)}</td>` +
                    `<td class="td-doi">${primary}${docs}${ft}${img}</td>` +
                    '</tr>'
                );
            })
            .join('');
    }
    const n = PUBS.length;
    const msg = data.length === n
        ? `${Math.min(shown.length, data.length)} of ${n} shown`
        : `${shown.length} of ${data.length} shown (filtered from ${n})`;
    document.getElementById('result-count').textContent = msg;
    document.querySelectorAll('[data-type-filter], [data-domain-filter]').forEach((button) => {
        const active = button.classList.contains('active');
        button.setAttribute('aria-pressed', String(active));
    });
    if (table) table.setAttribute('aria-busy', String(Boolean(q && enrichmentState === 'loading')));
    renderSearchStatus(q);
    updateSortUI();
}

function renderSearchStatus(query) {
    let status = document.getElementById('pub-search-status');
    if (!status) {
        const count = document.getElementById('result-count');
        if (!count) return;
        status = document.createElement('div');
        status.id = 'pub-search-status';
        status.className = 'text-muted';
        status.setAttribute('role', 'status');
        count.insertAdjacentElement('afterend', status);
    }
    status.hidden = !query || enrichmentState === 'ready';
    if (status.hidden) { status.textContent = ''; return; }
    if (enrichmentState === 'error') {
        status.textContent = 'Abstract and keyword search is temporarily unavailable. Showing available catalog matches. ';
        const retry = document.createElement('button');
        retry.type = 'button';
        retry.className = 'filter-btn';
        retry.textContent = 'Retry abstract search';
        retry.addEventListener('click', () => {
            ensureEnrichment(true);
            renderTable();
        });
        status.appendChild(retry);
    } else {
        status.textContent = 'Searching publication abstracts and keywords…';
    }
}

function ensureEnrichment(retry = false) {
    const query = (document.getElementById('pub-search').value || '').trim();
    if (!catalogLoaded || !query || enrichmentState === 'ready' || enrichmentState === 'error' && !retry) return;
    if (enrichmentPromise) return enrichmentPromise;
    enrichmentState = 'loading';
    enrichmentPromise = fetchEnrichment().then(byKey => {
        PUBS.forEach(pub => buildSearchIndex(pub, byKey[pub.citationKey]));
        enrichmentState = 'ready';
        // Read current controls here. A completed older request must not
        // reinstate a cleared query, previous scope, or obsolete sort order.
        renderTable();
    }).catch(error => {
        enrichmentState = 'error';
        console.warn('publication search: abstract/keyword index unavailable', error);
        renderTable();
    }).finally(() => { enrichmentPromise = null; });
    return enrichmentPromise;
}

function ensureLoadMoreButton(tbody) {
    // Created lazily in DOM order right after the table: no template change
    // needed, and it exists only when JS runs (crawlers/noscript never see it).
    let btn = document.getElementById('pub-load-more');
    if (btn) return btn;
    const table = document.getElementById('pub-table');
    if (!table || !table.parentNode) return null;
    btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'pub-load-more';
    btn.className = 'btn btn-outline';
    btn.style.margin = '0.75rem 0 0';
    btn.addEventListener('click', loadMorePubs);
    table.parentNode.insertBefore(btn, table.nextSibling);
    return btn;
}

function filterPubs() {
    currentLimit = PAGE_SIZE;
    ensureEnrichment();
    renderTable();
}

function loadMorePubs() {
    const firstNew = currentLimit;
    currentLimit += PAGE_SIZE;
    renderTable();
    document.querySelectorAll('#pub-tbody .td-title a')[firstNew]?.focus();
}

function setTypeFilter(t, btn) {
    currentTypeFilter = t;
    currentLimit = PAGE_SIZE;
    document.querySelectorAll('[data-type-filter]').forEach((b) => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderTable();
}

function setDomainFilter(d, pill) {
    currentDomainFilter = d;
    currentLimit = PAGE_SIZE;
    document.querySelectorAll('.domain-pill').forEach((p) => p.classList.remove('active'));
    if (pill) pill.classList.add('active');
    renderTable();
}

function setYearFilter(y) {
    currentYearFilter = y;
    currentLimit = PAGE_SIZE;
    renderTable();
}

function setVenueFilter(v) {
    currentVenueFilter = v;
    currentLimit = PAGE_SIZE;
    renderTable();
}

function resetFilters() {
    currentLimit = PAGE_SIZE;
    document.getElementById('pub-search').value = '';
    currentTypeFilter = 'all';
    currentDomainFilter = 'all';
    currentYearFilter = 'all';
    currentVenueFilter = 'all';
    document.getElementById('year-filter').value = 'all';
    document.getElementById('venue-filter').value = 'all';
    document.getElementById('doi-filter').checked = false;
    document.getElementById('docs-filter').checked = false;
    document.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
    document.getElementById('filter-all').classList.add('active');
    document.querySelectorAll('.domain-pill').forEach((p) => p.classList.remove('active'));
    document.querySelector('.domain-pill').classList.add('active');
    renderTable();
}

function defaultDirForCol(col) {
    if (col === 'year') return -1;
    if (col === 'num') return 1;
    return 1;
}

function sortBy(col) {
    currentLimit = PAGE_SIZE;
    if (currentSort.col === col) {
        currentSort.dir = -currentSort.dir;
    } else {
        currentSort.col = col;
        currentSort.dir = defaultDirForCol(col);
    }
    renderTable();
}

function initPublications(works, enrichmentByKey) {
    PUBS = works.map(workToPub);
    for (let i = 0; i < PUBS.length; i++) {
        buildSearchIndex(PUBS[i], enrichmentByKey[PUBS[i].citationKey]);
    }
    catalogLoaded = true;
    populateFilterSelects();
    ensureEnrichment();
    renderTable();
}

function fetchEnrichment() {
    // Abstracts and keywords are needed only after a nonempty query. Keep a
    // failure explicit and retryable instead of claiming an empty search index.
    const url = new URL(`data/work-enrichment.json${SCRIPT_QUERY}`, window.location.href);
    return fetch(url, { cache: 'no-store' })
        .then((response) => {
            if (!response.ok) throw new Error(`work-enrichment.json HTTP ${response.status}`);
            return response.json();
        })
        .then((data) => {
            const byKey = Object.create(null);
            const works = data && data.works;
            if (!works || typeof works !== 'object' || Array.isArray(works)) {
                throw new Error('Invalid publication enrichment');
            }
            Object.keys(works).forEach((key) => {
                const work = works[key];
                if (!work || typeof work !== 'object' ||
                        work.abstract !== undefined && typeof work.abstract !== 'string' ||
                        work.keywords !== undefined && (!Array.isArray(work.keywords) || work.keywords.some(word => typeof word !== 'string'))) {
                    throw new Error('Invalid publication enrichment entry');
                }
                byKey[works[key].citation_key || key] = works[key];
            });
            if (PUBS.some(pub => !Object.prototype.hasOwnProperty.call(byKey, pub.citationKey))) {
                throw new Error('Incomplete publication enrichment for the loaded catalog');
            }
            return byKey;
        });
}

function loadPublications() {
    const catalogUrl = new URL(`data/works.json${SCRIPT_QUERY}`, window.location.href);
    fetch(catalogUrl, { cache: 'no-store' }).then((response) => {
            if (!response.ok) throw new Error(`works.json HTTP ${response.status}`);
            return response.json();
        })
        .then((data) => {
            if (!data || !Array.isArray(data.works)) throw new Error('Invalid publication catalog');
            initPublications(data.works, {});
        })
        .catch((err) => {
            const empty = document.getElementById('no-results');
            if (empty) {
                empty.hidden = false;
                empty.classList.remove('d-none');
                empty.textContent = 'Interactive publication catalog could not be loaded. The publication links above remain available. Try again later.';
                empty.setAttribute('role', 'alert');
            }
            document.getElementById('pub-table')?.setAttribute('aria-busy', 'false');
            document.getElementById('result-count').textContent = 'Interactive catalog unavailable';
            console.error('publications catalog load failed', err);
        });
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
}

document.addEventListener('DOMContentLoaded', function () {
    loadPublications();
    // CSP (script-src 'self') forbids inline oninput handlers — wire here instead.
    var pubSearch = document.getElementById('pub-search');
    if (pubSearch) pubSearch.addEventListener('input', filterPubs);
});

window.filterPubs = filterPubs;
window.setTypeFilter = setTypeFilter;
window.setDomainFilter = setDomainFilter;
window.setYearFilter = setYearFilter;
window.setVenueFilter = setVenueFilter;
window.resetFilters = resetFilters;
window.sortBy = sortBy;
window.loadMorePubs = loadMorePubs;
window.esc = esc;
