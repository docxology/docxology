/* Progressive site search (CSP: script-src 'self'). */
(function () {
    'use strict';

    const state = { items: [], type: 'all', q: '', loading: true, contentError: false, revision: null, coreLoaded: false, bootstrapReady: false, typeCounts: null };
    const input = document.getElementById('q');
    const filters = document.getElementById('filters');
    const results = document.getElementById('results');
    if (!input || !filters || !results) return;
    // This input already owns the complete results surface. A core-only
    // autocomplete would obscure its filters and disagree on full-text hits.
    input.setAttribute('data-local-search', '');
    input.value = new URLSearchParams(location.search).get('q') || '';
    state.q = input.value;
    let requestSequence = 0;
    let debounceTimer = null;

    // Word-start prefix matches avoid finding "ant" inside "important".
    // Every term must match; title matches outrank text matches.
    function matchers(terms) {
        return terms.map(term => {
            const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            return new RegExp((/^\w/.test(term) ? '\\b' : '') + escaped, 'i');
        });
    }

    function score(item, expressions) {
        const title = item.title || '';
        const content = [item.content || '', item.summary || '', (item.tags || []).join(' ')].join(' ');
        let value = 0;
        for (const expression of expressions) {
            const inTitle = expression.test(title);
            const inContent = expression.test(content);
            if (!inTitle && !inContent) return 0;
            if (inTitle) value += 8;
            if (inContent) value += 2;
        }
        return value > 0 && item.type === 'work' ? value + 1 : value;
    }

    function renderFilters() {
        const counts = state.typeCounts || state.items.reduce((totals, item) => {
            totals[item.type] = (totals[item.type] || 0) + 1;
            return totals;
        }, Object.create(null));
        const types = ['all', ...Object.keys(counts).sort()];
        // Preserve the user's selected scope even if a new revision has no
        // entries of that type; silently switching to all would broaden it.
        if (!types.includes(state.type)) types.push(state.type);
        filters.innerHTML = types.map(type => {
            const count = type === 'all' ? Object.values(counts).reduce((sum, count) => sum + count, 0) : counts[type] || 0;
            return `<button type="button" class="${type === state.type ? 'active' : ''}" aria-pressed="${type === state.type}" data-type="${esc(type)}">${esc(type)} (${count})</button>`;
        }).join('');
        filters.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
            state.type = button.dataset.type;
            filters.querySelectorAll('button').forEach(other => {
                other.setAttribute('aria-pressed', String(other === button));
                other.classList.toggle('active', other === button);
            });
            refresh();
        }));
    }

    function renderStatus(total) {
        const status = document.getElementById('result-status');
        if (!status) return;
        const pending = state.loading ? '<p class="text-muted" role="status">Searching publication and video text…</p>' : '';
        const incomplete = state.contentError
            ? '<p class="text-muted" role="status">Full-text search is temporarily unavailable. Showing available title, summary, and site-text matches. <button type="button" class="filter-btn" data-search-retry>Retry full-text search</button></p>'
            : '';
        let count = '';
        if (state.q.trim()) {
            if (total === 0 && !state.loading && !state.contentError) {
                count = `<p class="no-results">No results for &ldquo;${esc(state.q)}&rdquo;. Try fewer or different words, or browse the <a href="works/">works index</a>.</p>`;
            } else if (total > 0) {
                count = `<p class="result-count" role="status">${total} result${total === 1 ? '' : 's'} for &ldquo;${esc(state.q)}&rdquo;${total > 80 ? ' (showing first 80)' : ''}</p>`;
            }
        }
        status.innerHTML = count + pending + incomplete;
        status.hidden = !status.innerHTML;
        const retry = status.querySelector('[data-search-retry]');
        if (retry) retry.addEventListener('click', refresh);
    }

    function render() {
        const terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
        let matches = state.items;
        if (state.type !== 'all') matches = matches.filter(item => item.type === state.type);
        if (terms.length) {
            const expressions = matchers(terms);
            matches = matches.map(item => ({ item, rank: score(item, expressions) }))
                .filter(match => match.rank > 0).sort((a, b) => b.rank - a.rank).map(match => match.item);
        } else matches = matches.slice(0, 40);
        const total = matches.length;
        matches = matches.slice(0, 80);
        renderStatus(total);
        results.innerHTML = matches.map(item => {
            const tags = (item.tags || []).filter(Boolean).slice(0, 5).map(tag => `<span>${esc(tag)}</span>`).join('');
            const badges = [];
            if (item.full_text_url) badges.push('<span class="badge-ft">Full Text</span>');
            if (item.image_count) badges.push(`<span class="badge-img">${esc(item.image_count)} Images</span>`);
            const badgeHtml = badges.length ? `<div class="result-badges">${badges.join('')}</div>` : '';
            return `<article class="result-card"><h2><a href="${esc(item.url)}">${esc(item.title)}</a></h2><p>${esc(item.summary || '')}</p><div class="result-meta"><span>${esc(item.type)}</span>${item.year ? `<span>${esc(item.year)}</span>` : ''}${tags}</div>${badgeHtml}</article>`;
        }).join('') || (state.loading || state.contentError ? '' : '<p class="text-center text-muted mt-2">No results.</p>');
        results.setAttribute('aria-busy', String(state.loading));
        results.setAttribute('aria-label', `${matches.length} search results`);
        const url = new URL(location.href);
        if (state.q) url.searchParams.set('q', state.q); else url.searchParams.delete('q');
        history.replaceState(null, '', url);
    }

    function contentTypes() {
        if (!state.q.trim()) return [];
        if (state.type === 'all') return ['work', 'video'];
        return state.type === 'work' || state.type === 'video' ? [state.type] : [];
    }

    async function refresh() {
        const sequence = ++requestSequence;
        results.removeAttribute('role');
        const types = contentTypes();
        state.contentError = false;
        const needsCore = state.coreLoaded || !state.bootstrapReady || state.q.trim() || state.type !== 'all';
        state.loading = Boolean(types.length || needsCore && !state.coreLoaded);
        if (state.coreLoaded) state.items = window.DocxologySearch.getItems();
        render();
        if (needsCore) {
            try {
                await window.DocxologySearch.loadCore();
                if (sequence !== requestSequence) return;
                state.coreLoaded = true;
                state.typeCounts = null;
                state.items = window.DocxologySearch.getItems();
                state.revision = window.DocxologySearch.getRevision();
                state.loading = types.length > 0;
                renderFilters();
                render();
            } catch (error) {
                if (sequence !== requestSequence) return;
                coreUnavailable(error);
                return;
            }
        }
        if (!types.length) return;
        try {
            const items = await window.DocxologySearch.loadContent(types);
            if (sequence !== requestSequence) return;
            state.items = items;
        } catch (error) {
            if (sequence !== requestSequence) return;
            state.items = window.DocxologySearch.getItems();
            state.contentError = true;
            console.warn('Full-text search unavailable', error);
        }
        if (state.revision !== window.DocxologySearch.getRevision()) {
            state.revision = window.DocxologySearch.getRevision();
            renderFilters();
        }
        state.loading = false;
        render();
    }

    input.addEventListener('input', () => {
        state.q = input.value;
        // Immediately invalidate any older asynchronous query before debounce.
        requestSequence++;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(refresh, 120);
    });

    function coreUnavailable(error) {
        console.error('Search core index unavailable', error);
        state.loading = false;
        state.bootstrapReady = false;
        const status = document.getElementById('result-status');
        if (status) { status.innerHTML = ''; status.hidden = true; }
        results.innerHTML = '<p class="text-center text-muted mt-2">Search index unavailable. Browse the <a href="works/">works index</a>, or <button type="button" class="filter-btn" data-search-core-retry>retry search</button>.</p>';
        results.setAttribute('role', 'alert');
        results.setAttribute('aria-busy', 'false');
        results.querySelector('[data-search-core-retry]').addEventListener('click', () => {
            results.removeAttribute('role');
            refresh();
        });
    }

    async function browseBootstrap() {
        const sequence = requestSequence;
        try {
            const response = await fetch('/search-index-bootstrap.json', { cache: 'no-cache' });
            if (!response.ok) throw new Error('Search bootstrap request failed: ' + response.status);
            const data = await response.json();
            const counts = data && data.type_counts;
            if (!data || typeof data.generated_at !== 'string' || !Number.isSafeInteger(data.count) || data.count < 0 ||
                    !Array.isArray(data.items) || data.items.length !== Math.min(data.count, 40) ||
                    !counts || typeof counts !== 'object' || Array.isArray(counts) ||
                    Object.values(counts).some(count => !Number.isSafeInteger(count) || count <= 0) ||
                    Object.values(counts).reduce((sum, count) => sum + count, 0) !== data.count) {
                throw new Error('Invalid search bootstrap');
            }
            const seen = new Set();
            const sampleCounts = Object.create(null);
            data.items.forEach(item => {
                if (!item || typeof item.id !== 'string' || typeof item.type !== 'string' ||
                        typeof item.title !== 'string' || typeof item.url !== 'string' || seen.has(item.id) ||
                        !Object.prototype.hasOwnProperty.call(counts, item.type)) {
                    throw new Error('Invalid or duplicate bootstrap search entry');
                }
                seen.add(item.id);
                sampleCounts[item.type] = (sampleCounts[item.type] || 0) + 1;
            });
            if (Object.entries(sampleCounts).some(([type, count]) => count > counts[type])) {
                throw new Error('Invalid search bootstrap counts');
            }
            // Typing or choosing a scope already started the full search. A
            // late bootstrap must never replace those results or filter counts.
            if (sequence !== requestSequence || state.q.trim() || state.type !== 'all' || state.coreLoaded) return;
            state.items = data.items;
            state.typeCounts = counts;
            state.revision = data.generated_at;
            state.bootstrapReady = true;
            state.loading = false;
            renderFilters();
            render();
        } catch (error) {
            if (sequence !== requestSequence || state.coreLoaded) return;
            // The additive browsing companion is optional: existing exports
            // remain the complete search authority and provide the fallback.
            console.warn('Search browsing preview unavailable', error);
            refresh();
        }
    }

    results.setAttribute('aria-busy', 'true');
    if (state.q.trim()) refresh();
    else browseBootstrap();
})();
