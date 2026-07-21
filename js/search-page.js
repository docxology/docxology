/* Externalized from search.html inline script (CSP: script-src 'self'). */
const state = { items: [], type: 'all', q: '' };
        const params = new URLSearchParams(location.search);
        const input = document.getElementById('q');
        const filters = document.getElementById('filters');
        const results = document.getElementById('results');
        input.value = params.get('q') || '';
        state.q = input.value;

        function score(item, terms){
            const title = (item.title || '').toLowerCase();
            const content = (item.content || '').toLowerCase();
            let value = 0;
            for (const term of terms){
                if (title.includes(term)) value += 8;
                if (content.includes(term)) value += 2;
            }
            // Tie-break boost for works — only when the item already matched a
            // term. Applied unconditionally this leaked a baseline score to every
            // work, so every query (even nonsense) returned all works and a genuine
            // no-match query never showed "No results".
            if (value > 0 && item.type === 'work') value += 1;
            return value;
        }

        function renderFilters(){
            const types = ['all', ...Array.from(new Set(state.items.map(i => i.type))).sort()];
            filters.innerHTML = types.map(type => {
                const count = type === 'all' ? state.items.length : state.items.filter(i => i.type === type).length;
                return `<button type="button" class="${type === state.type ? 'active' : ''}" data-type="${esc(type)}">${esc(type)} (${count})</button>`;
            }).join('');
            filters.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => {
                state.type = btn.dataset.type;
                filters.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
                render();
            }));
            filters.querySelectorAll('button').forEach(btn => btn.setAttribute('aria-pressed', String(btn.dataset.type === state.type)));
        }

        function render(){
            const terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
            let matches = state.items;
            if (state.type !== 'all') matches = matches.filter(item => item.type === state.type);
            if (terms.length) matches = matches.map(item => ({item, rank: score(item, terms)})).filter(x => x.rank > 0).sort((a,b) => b.rank - a.rank).map(x => x.item);
            else matches = matches.slice(0, 40);
            matches = matches.slice(0, 80);
            results.innerHTML = matches.map(item => {
                const tags = (item.tags || []).filter(Boolean).slice(0, 5).map(tag => `<span>${esc(tag)}</span>`).join('');
                const badges = [];
                if (item.full_text_url) badges.push('<span class="badge-ft">Full Text</span>');
                if (item.image_count) badges.push(`<span class="badge-img">${esc(item.image_count)} Images</span>`);
                const badgeHtml = badges.length ? `<div class="result-badges">${badges.join('')}</div>` : '';
                return `<article class="result-card"><h2><a href="${esc(item.url)}">${esc(item.title)}</a></h2><p>${esc(item.summary || '')}</p><div class="result-meta"><span>${esc(item.type)}</span>${item.year ? `<span>${esc(item.year)}</span>` : ''}${tags}</div>${badgeHtml}</article>`;
            }).join('') || '<p class="text-center text-muted mt-2">No results.</p>';
            results.setAttribute('aria-live', 'polite');
            results.setAttribute('aria-busy', 'false');
            results.setAttribute('aria-label', `${matches.length} search results`);
            const url = new URL(location.href);
            if (state.q) url.searchParams.set('q', state.q); else url.searchParams.delete('q');
            history.replaceState(null, '', url);
        }

        input.addEventListener('input', () => {
            state.q = input.value;
            render();
        });

        fetch('search-index.json?v=video-index-20260620', { cache: 'no-store' })
            .then(res => res.json())
            .then(data => {
                state.items = data.items || [];
                renderFilters();
                render();
            })
            .catch(() => {
                results.innerHTML = '<p class="text-center text-muted mt-2">Search index unavailable.</p>';
                results.setAttribute('role', 'alert');
                results.setAttribute('aria-busy', 'false');
            });
