/* An accessible, bounded neighborhood of the complete metadata graph. */
(() => {
    'use strict';
    const $ = id => document.getElementById(id);
    if (!$('map-app')) return;
    const status = message => { $('map-status').textContent = message; };
    const make = (tag, text, attrs = {}) => {
        const node = document.createElement(tag); if (text !== undefined) node.textContent = text;
        Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v)); return node;
    };
    const safeURL = value => {
        if (!value) return '';
        const url = new URL(value, location.origin);
        if (url.origin !== location.origin && !(url.protocol === 'https:' && url.hostname === 'github.com' && !url.username && !url.password)) throw new Error('Unsafe graph resource URL.');
        return url.href;
    };
    let nodes, edges, neighbors, selected = '', limit = 40;
    function writeURL(mode = 'push') {
        const url = new URL(location.href); url.search = '';
        if (selected) url.searchParams.set('node', selected);
        if ($('map-search').value) url.searchParams.set('q', $('map-search').value);
        if ($('map-kind').value !== 'all') url.searchParams.set('kind', $('map-kind').value);
        if (url.href !== location.href) history[mode === 'replace' ? 'replaceState' : 'pushState'](null, '', url);
    }
    function diagram(items) {
        const svg = $('research-map-svg'); svg.replaceChildren(); svg.setAttribute('role', 'group');
        const NS = 'http://www.w3.org/2000/svg';
        const element = (name, attrs = {}) => { const node = document.createElementNS(NS, name); Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v)); return node; };
        const points = items.slice(0, 12).map((edge, i, all) => ({edge, x: 400 + 240 * Math.cos(2 * Math.PI * i / all.length), y: 250 + 160 * Math.sin(2 * Math.PI * i / all.length)}));
        for (const p of points) svg.appendChild(element('line', {x1: 400, y1: 250, x2: p.x, y2: p.y, class: 'graph-edge'}));
        const drawNode = (node, x, y, center = false) => {
            const url = new URL('/research-map.html', location.origin); url.searchParams.set('node', node.id);
            const anchor = element('a', {href: url.pathname + url.search, 'aria-label': `Explore ${node.kind}: ${node.label}`});
            anchor.appendChild(element('circle', {cx: x, cy: y, r: center ? 20 : 12, class: 'graph-node ' + node.kind}));
            const text = element('text', {x, y: y + 34, 'text-anchor': 'middle'}); text.textContent = node.label.length > 22 ? node.label.slice(0, 20) + '…' : node.label; anchor.appendChild(text);
            anchor.addEventListener('click', event => { if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return; event.preventDefault(); focusNode(node.id); }); svg.appendChild(anchor);
        };
        for (const p of points) drawNode(nodes.get(p.edge.other), p.x, p.y);
        drawNode(nodes.get(selected), 400, 250, true);
    }
    function show(message = '') {
        $('map-connections').replaceChildren();
        if (!selected) { $('research-map-svg').replaceChildren(); $('map-title').textContent = 'No matching nodes'; $('map-summary').textContent = ''; $('map-more').hidden = true; status('No nodes match these controls.'); return; }
        const node = nodes.get(selected); const connections = neighbors.get(selected);
        $('map-title').textContent = node.label;
        $('map-summary').textContent = `${node.kind} · ${connections.length} recorded connection(s).`;
        diagram(connections);
        for (const edge of connections.slice(0, limit)) {
            const other = nodes.get(edge.other), row = make('li');
            const button = make('button', other.label, {type: 'button', class: 'connection-focus'}); button.addEventListener('click', () => focusNode(other.id)); row.appendChild(button);
            row.appendChild(make('p', `${other.kind} · ${edge.relation}. Source: ${edge.provenance}`));
            if (other.url) row.appendChild(make('a', 'Open ' + other.kind + ' resource', {href: safeURL(other.url)}));
            $('map-connections').appendChild(row);
        }
        $('map-more').hidden = connections.length <= limit;
        status(message || `Showing ${Math.min(limit, connections.length)} of ${connections.length} connections. The diagram shows up to twelve.`);
    }
    function choices(preferred = selected) {
        const q = $('map-search').value.toLocaleLowerCase().trim(), kind = $('map-kind').value;
        const matches = [...nodes.values()].filter(n => (kind === 'all' || n.kind === kind) && n.label.toLocaleLowerCase().includes(q));
        const select = $('map-node'); select.replaceChildren();
        for (const node of matches) select.appendChild(make('option', `${node.kind} — ${node.label}`, {value: node.id}));
        selected = matches.some(n => n.id === preferred) ? preferred : matches[0]?.id || '';
        select.value = selected; limit = 40; show();
    }
    function focusNode(id) {
        $('map-search').value = ''; $('map-kind').value = 'all'; choices(id); writeURL(); $('map-title').tabIndex = -1; $('map-title').focus();
    }
    function restore() {
        const p = new URLSearchParams(location.search), kind = p.get('kind') || 'all';
        $('map-kind').value = ['all', 'work', 'person', 'software', 'domain'].includes(kind) ? kind : 'all';
        $('map-search').value = (p.get('q') || '').slice(0, 300);
        const wanted = p.get('node') || [...nodes.values()].find(n => n.kind === 'domain')?.id;
        choices(wanted);
        if (p.has('node') && !nodes.has(p.get('node'))) status('Unknown map node in URL. Choose a recorded node from the controls.');
    }
    async function start() {
        $('map-retry').hidden = true;
        try {
            const response = await fetch('/data/research-map.json?v=1', {cache: 'no-store'});
            if (!response.ok) throw new Error('Graph HTTP ' + response.status);
            const data = await response.json();
            if (data.schema_version !== 1 || !Array.isArray(data.nodes) || !Array.isArray(data.edges)) throw new Error('Invalid graph schema.');
            if (data.nodes.some(n => !n || typeof n.id !== 'string' || !['work', 'person', 'software', 'domain'].includes(n.kind) || typeof n.label !== 'string' || typeof n.url !== 'string')) throw new Error('Invalid graph node.');
            nodes = new Map(data.nodes.map(n => [n.id, n]));
            if (!nodes.size || nodes.size !== data.nodes.length) throw new Error('Empty or duplicate graph nodes.');
            nodes.forEach(n => safeURL(n.url));
            edges = data.edges;
            if (edges.some(e => !e || !nodes.has(e.source) || !nodes.has(e.target) || typeof e.relation !== 'string' || typeof e.provenance !== 'string')) throw new Error('Dangling or malformed graph edge.');
            neighbors = new Map([...nodes.keys()].map(id => [id, []]));
            edges.forEach(e => { neighbors.get(e.source).push({...e, other: e.target}); neighbors.get(e.target).push({...e, other: e.source}); });
            neighbors.forEach(list => list.sort((a, b) => nodes.get(a.other).label.localeCompare(nodes.get(b.other).label)));
            restore(); $('map-app').disabled = false; $('map-app').setAttribute('aria-busy', 'false');
            $('map-search').addEventListener('input', () => { choices(); writeURL('replace'); });
            $('map-kind').addEventListener('change', () => { choices(); writeURL(); });
            $('map-node').addEventListener('change', () => { selected = $('map-node').value; limit = 40; show(); writeURL(); });
            $('map-more').addEventListener('click', () => { const old = limit; limit += 40; show(); $('map-connections').children[old]?.querySelector('button')?.focus(); });
            window.addEventListener('popstate', restore);
        } catch (error) { status('Research map unavailable: ' + error.message + ' Use the domain links or retry.'); $('map-retry').hidden = false; }
    }
    $('map-retry').addEventListener('click', start); start();
})();
