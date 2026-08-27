/* Externalized from search.html inline script (CSP: script-src 'self'). */
const state = { items: [], type: 'all', q: '' };
        const params = new URLSearchParams(location.search);
        const input = document.getElementById('q');
        const filters = document.getElementById('filters');
        const results = document.getElementById('results');
        input.value = params.get('q') || '';
        state.q = input.value;

        // Compile each query term to a word-start matcher: "\b" anchors to a word
        // boundary so "ant" matches "ant"/"ants"/"ant-colony" and "info" matches
        // "information" (useful prefix search), but NOT the interior of "important".
        // Symbol/emoji terms (no leading word char) fall back to substring so
        // queries like "🐜" or "c++" still match. Compiled once per render.
        function matchers(terms){
            return terms.map(term => {
                const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                return new RegExp((/^\w/.test(term) ? '\\b' : '') + escaped, 'i');
            });
        }

        function score(item, res){
            const title = item.title || '';
            const content = item.content || '';
            let value = 0;
            for (const re of res){
                const inTitle = re.test(title);
                const inContent = re.test(content);
                // Every term must appear somewhere. Scoring the terms
                // independently made the query an OR: "active inference"
                // returned everything mentioning either word — about two
                // thirds of the index — burying the actual matches.
                if (!inTitle && !inContent) return 0;
                if (inTitle) value += 8;
                if (inContent) value += 2;
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

        function renderStatus(total, filtered, truncated){
            // Result count line: "N results for “query”" when searching, an
            // explicit empty state when a query matches nothing. Plain text
            // interpolated through esc() like every other dynamic string.
            const status = document.getElementById('result-status');
            if (!status) return;
            if (!state.q.trim()){
                status.textContent = '';
                status.hidden = true;
                return;
            }
            if (total === 0){
                status.innerHTML = `<p class="no-results">No results for &ldquo;${esc(state.q)}&rdquo;. Try fewer or different words, or browse the <a href="works/">works index</a>.</p>`;
                status.hidden = false;
                return;
            }
            const suffix = truncated ? ' (showing first 80)' : '';
            status.innerHTML = `<p class="result-count" role="status">${total} result${total === 1 ? '' : 's'} for &ldquo;${esc(state.q)}&rdquo;${suffix}</p>`;
            status.hidden = false;
        }

        function render(){
            const terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
            let matches = state.items;
            if (state.type !== 'all') matches = matches.filter(item => item.type === state.type);
            if (terms.length) { const res = matchers(terms); matches = matches.map(item => ({item, rank: score(item, res)})).filter(x => x.rank > 0).sort((a,b) => b.rank - a.rank).map(x => x.item); }
            else matches = matches.slice(0, 40);
            const totalMatches = matches.length;
            matches = matches.slice(0, 80);
            renderStatus(totalMatches, state.items.length, totalMatches > 80);
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
