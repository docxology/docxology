/* Progressive site search (CSP: script-src 'self'). */
(function () {
    'use strict';

    const state = { items: [], type: 'all', q: '', loading: true, contentError: false, revision: null };
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
        const types = ['all', ...Array.from(new Set(state.items.map(item => item.type))).sort()];
        // Preserve the user's selected scope even if a new revision has no
        // entries of that type; silently switching to all would broaden it.
        if (!types.includes(state.type)) types.push(state.type);
        filters.innerHTML = types.map(type => {
            const count = type === 'all' ? state.items.length : state.items.filter(item => item.type === type).length;
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
        const types = contentTypes();
        state.contentError = false;
        state.loading = types.length > 0;
        state.items = window.DocxologySearch.getItems();
        render();
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

    results.setAttribute('aria-busy', 'true');
    Promise.resolve().then(() => window.DocxologySearch.loadCore()).then(items => {
        state.items = items;
        state.revision = window.DocxologySearch.getRevision();
        renderFilters();
        refresh();
    }).catch(error => {
        console.error('Search core index unavailable', error);
        results.innerHTML = '<p class="text-center text-muted mt-2">Search index unavailable. Browse the <a href="works/">works index</a>, or reload to retry.</p>';
        results.setAttribute('role', 'alert');
        results.setAttribute('aria-busy', 'false');
    });
})();
