/* Browser-local reading lists. Shared URLs are previews, never storage writes. */
(() => {
    'use strict';
    const STORAGE_KEY = 'docxology.reading-lists.v1';
    const KEY = /^[A-Za-z][A-Za-z0-9_-]{0,180}$/;
    const MAX_KEYS = 500;
    function title(value) {
        if (typeof value !== 'string' || !value.trim() || value.length > 100 || /[\r\n\u0000-\u001f]/.test(value)) throw new Error('List titles must contain 1–100 printable characters.');
        return value.trim();
    }
    function keys(value) {
        if (!Array.isArray(value) || value.length > MAX_KEYS || value.some(k => typeof k !== 'string' || !KEY.test(k)) || new Set(value).size !== value.length) throw new Error('Invalid, duplicate, or excessive citation keys.');
        return value.slice();
    }
    function validateStore(value) {
        if (!value || value.version !== 1 || !Array.isArray(value.lists) || !value.lists.length || value.lists.length > 20) throw new Error('Invalid reading-list backup (version 1, 1–20 lists required).');
        const lists = value.lists.map(list => {
            if (!list || typeof list.id !== 'string' || !KEY.test(list.id)) throw new Error('Invalid list identifier.');
            return {id: list.id, title: title(list.title), keys: keys(list.keys)};
        });
        if (new Set(lists.map(list => list.id)).size !== lists.length || !lists.some(list => list.id === value.active)) throw new Error('Duplicate or missing active list identifier.');
        return {version: 1, active: value.active, lists};
    }
    function parseStore(raw) {
        if (typeof raw !== 'string' || raw.length > 1000000) throw new Error('Backup exceeds the 1 MB safety limit.');
        return validateStore(JSON.parse(raw));
    }
    function parseShare(hash) {
        if (!hash || hash === '#') return null;
        if (hash.length > 100000) throw new Error('Shared list URL is too long.');
        const p = new URLSearchParams(hash.replace(/^#/, ''));
        if (p.get('v') !== '1' || ['v', 'title', 'works'].some(name => p.getAll(name).length !== 1) || [...p.keys()].some(k => !['v', 'title', 'works'].includes(k))) throw new Error('Invalid shared list URL.');
        return {id: 'shared', title: title(p.get('title')), keys: keys(p.get('works') ? p.get('works').split(',') : [])};
    }
    function shareURL(list, base) {
        const url = new URL('/collections.html', base);
        url.hash = new URLSearchParams({v: '1', title: title(list.title), works: keys(list.keys).join(',')}).toString();
        return url.href;
    }
    const markdown = value => String(value).replace(/([\\`*_{}\[\]()#+.!<>])/g, '\\$1');
    function exportList(list, catalog, format) {
        const records = keys(list.keys).map(key => {
            if (!catalog.has(key)) throw new Error('Resolve unavailable work ' + key + ' before exporting citations.');
            return catalog.get(key);
        });
        if (format === 'bib' || format === 'ris') return records.map(w => w[format].trim()).join('\n\n') + '\n';
        if (format === 'csl') return JSON.stringify(records.map(w => w.csl), null, 2) + '\n';
        if (format === 'md') return '# ' + markdown(title(list.title)) + '\n\n' + records.map((w, i) => `${i + 1}. [${markdown(w.title)}](${new URL(w.url, 'https://danielarifriedman.com').href}) (${w.year})`).join('\n') + '\n';
        throw new Error('Unknown export format.');
    }
    if (typeof module !== 'undefined') module.exports = {STORAGE_KEY, keys, validateStore, parseStore, parseShare, shareURL, exportList};
    if (typeof document === 'undefined' || !document.getElementById('collection-app')) return;

    const $ = id => document.getElementById(id);
    const status = message => { $('collection-status').textContent = message; };
    const make = (tag, text, attrs = {}) => {
        const node = document.createElement(tag);
        if (text !== undefined) node.textContent = text;
        Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
        return node;
    };
    let catalog, state, preview = null, persistent = true, lastRaw = null, rawBackup = null, imported = null, storageWarning = '', deleted = null;
    const current = () => preview || state.lists.find(list => list.id === state.active);
    function report(message = '') {
        const missing = current().keys.filter(key => !catalog.has(key));
        status([message, preview ? 'Shared/imported preview: save explicitly to retain it.' : '', storageWarning, missing.length ? `${missing.length} unavailable work(s) retained in the list. Remove them or restore their catalog records before citation export.` : ''].filter(Boolean).join(' '));
    }
    function download(text, filename, mime) {
        const url = URL.createObjectURL(new Blob([text], {type: mime}));
        const anchor = make('a', '', {href: url, download: filename});
        document.body.appendChild(anchor); anchor.click(); anchor.remove();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }
    function persist() {
        if (preview || !persistent) return;
        try {
            if (localStorage.getItem(STORAGE_KEY) !== lastRaw) throw new Error('Saved lists changed in another tab. Export this draft and reload before editing saved lists.');
            const raw = JSON.stringify(validateStore(state));
            if (raw.length > 1000000) throw new Error('Lists exceed the 1 MB safety limit. Export a backup and shorten the lists.');
            localStorage.setItem(STORAGE_KEY, raw);
            lastRaw = raw;
        } catch (error) {
            persistent = false;
            storageWarning = `${error.message} Changes remain available in this tab; download a backup to retain them.`;
        }
    }
    function renderChoices() {
        const query = $('collection-search').value.toLocaleLowerCase().trim();
        const select = $('collection-candidate'); select.replaceChildren();
        const matches = [...catalog.values()].filter(w => `${w.title} ${w.authors.join(' ')} ${w.year} ${w.key}`.toLocaleLowerCase().includes(query));
        for (const work of matches) select.appendChild(make('option', `${work.year} — ${work.title}`, {value: work.key}));
        $('collection-add').disabled = !matches.length;
        if (!matches.length) select.appendChild(make('option', 'No matching works', {value: ''}));
    }
    function render(message = '') {
        const list = current();
        $('collection-title').value = list.title;
        const select = $('collection-select'); select.replaceChildren();
        for (const item of state.lists) select.appendChild(make('option', item.title, {value: item.id}));
        if (preview) select.appendChild(make('option', 'Preview: ' + preview.title, {value: 'shared'}));
        select.value = preview ? 'shared' : state.active;
        $('collection-save-shared').hidden = !preview;
        $('collection-delete').hidden = Boolean(preview);
        $('collection-items').replaceChildren();
        list.keys.forEach((key, index) => {
            const work = catalog.get(key);
            const row = make('li');
            row.appendChild(work ? make('a', work.title, {href: work.url}) : make('span', 'Unavailable work: ' + key));
            const actions = make('div', undefined, {class: 'tool-toolbar'});
            for (const [action, label, disabled] of [['up', 'Move up', index === 0], ['down', 'Move down', index === list.keys.length - 1], ['remove', 'Remove', false]]) {
                const button = make('button', label, {type: 'button', 'data-list-action': action, 'data-list-key': key, 'aria-label': `${label}: ${work ? work.title : key}`});
                button.disabled = disabled; actions.appendChild(button);
            }
            row.appendChild(actions); $('collection-items').appendChild(row);
        });
        if (!list.keys.length) $('collection-items').appendChild(make('li', 'No papers yet. Add a catalog work above.'));
        $('collection-share-label').hidden = true;
        report(message || `${list.keys.length} work(s) in reading order.`);
    }
    function add(key) {
        if (!catalog.has(key)) throw new Error('That citation key is not in the current catalog.');
        if (current().keys.includes(key)) { report('That work is already in this list.'); return; }
        if (current().keys.length >= MAX_KEYS) throw new Error('A list can contain at most 500 works.');
        current().keys.push(key); persist(); render('Work added.');
    }
    function guard(action) { return (...args) => { try { action(...args); } catch (error) { report(error.message); } }; }
    function newID() { return 'list-' + crypto.randomUUID(); }
    function bind() {
        $('collection-search').addEventListener('input', renderChoices);
        $('collection-add').addEventListener('click', guard(() => add($('collection-candidate').value)));
        $('collection-title').addEventListener('change', guard(() => { current().title = title($('collection-title').value); persist(); render('Title updated.'); }));
        $('collection-select').addEventListener('change', guard(() => { if ($('collection-select').value !== 'shared') { preview = null; state.active = $('collection-select').value; persist(); render(); } }));
        $('collection-new').addEventListener('click', guard(() => {
            if (state.lists.length >= 20) throw new Error('At most 20 saved lists. Export a backup before starting another browser library.');
            const list = {id: newID(), title: 'Reading list ' + (state.lists.length + 1), keys: []};
            state.lists.push(list); state.active = list.id; preview = null; persist(); render('New list created.');
        }));
        $('collection-delete').addEventListener('click', guard(() => {
            if (preview) return;
            deleted = structuredClone(current());
            state.lists = state.lists.filter(list => list.id !== state.active);
            if (!state.lists.length) state.lists.push({id: newID(), title: 'Reading list', keys: []});
            state.active = state.lists[0].id; persist(); render('List deleted. Undo is available until another list is deleted or this page closes.');
            let undo = $('collection-undo');
            if (!undo) { undo = make('button', 'Undo list deletion', {id: 'collection-undo', type: 'button'}); $('collection-delete').after(undo); undo.addEventListener('click', guard(() => { if (!deleted) return; if (state.lists.length >= 20) throw new Error('Make room for the restored list first.'); state.lists.push(deleted); state.active = deleted.id; deleted = null; persist(); render('List restored.'); undo.remove(); })); }
        }));
        $('collection-save-shared').addEventListener('click', guard(() => {
            if (!preview) return;
            if (state.lists.length >= 20) throw new Error('At most 20 saved lists. Download this preview instead.');
            const list = {id: newID(), title: title(preview.title), keys: keys(preview.keys)};
            state.lists.push(list); state.active = list.id; preview = null; persist(); render('Preview saved as a new list.');
        }));
        $('collection-items').addEventListener('click', guard(event => {
            const button = event.target.closest('[data-list-action]'); if (!button) return;
            const list = current(); const index = list.keys.indexOf(button.dataset.listKey); if (index < 0) return;
            const action = button.dataset.listAction;
            if (action === 'remove') list.keys.splice(index, 1);
            else { const next = index + (action === 'up' ? -1 : 1); if (next < 0 || next >= list.keys.length) return; [list.keys[index], list.keys[next]] = [list.keys[next], list.keys[index]]; }
            persist(); render('Reading order updated.');
            const rows = [...$('collection-items').querySelectorAll('li')];
            const destination = action === 'remove' ? Math.min(index, rows.length - 1) : list.keys.indexOf(button.dataset.listKey);
            rows[destination]?.querySelector('a,button')?.focus();
        }));
        document.querySelectorAll('[data-collection-export]').forEach(button => button.addEventListener('click', guard(() => {
            const format = button.dataset.collectionExport;
            download(exportList(current(), catalog, format), 'reading-list.' + (format === 'csl' ? 'csl.json' : format), format === 'csl' ? 'application/json' : 'text/plain;charset=utf-8');
            report('Selected citations exported in reading order.');
        })));
        $('collection-share').addEventListener('click', guard(() => {
            $('collection-share-url').value = shareURL(current(), location.href);
            $('collection-share-label').hidden = false; $('collection-share-url').focus(); $('collection-share-url').select();
            report('Share link ready to copy. It opens a preview and does not synchronize later edits.');
        }));
        $('collection-backup').addEventListener('click', guard(() => {
            const backup = preview ? {version: 1, active: 'list-preview', lists: [{id: 'list-preview', title: preview.title, keys: preview.keys}]} : state;
            download(JSON.stringify(validateStore(backup), null, 2) + '\n', 'reading-lists.json', 'application/json');
        }));
        $('collection-original').hidden = rawBackup === null;
        $('collection-original').addEventListener('click', () => { if (rawBackup !== null) download(rawBackup, 'original-reading-lists.json', 'application/json'); });
        $('collection-import').addEventListener('change', async () => {
            try {
                const file = $('collection-import').files[0]; if (!file) return;
                if (file.size > 1000000) throw new Error('Backup exceeds the 1 MB safety limit.');
                imported = parseStore(await file.text()); $('collection-import-choice').replaceChildren();
                for (const list of imported.lists) $('collection-import-choice').appendChild(make('option', list.title, {value: list.id}));
                report('Backup validated. Choose a list to preview before saving.');
            } catch (error) { imported = null; report('Import refused: ' + error.message); }
        });
        $('collection-preview-import').addEventListener('click', guard(() => {
            if (!imported) throw new Error('Choose a valid JSON backup first.');
            const selected = imported.lists.find(list => list.id === $('collection-import-choice').value);
            preview = {id: 'shared', title: selected.title, keys: selected.keys.slice()}; render('Imported preview opened; existing lists are unchanged.');
        }));
        window.addEventListener('storage', event => { if (event.key === STORAGE_KEY && event.newValue !== lastRaw) { persistent = false; storageWarning = 'Saved lists changed in another tab. Download this draft before reloading.'; report(); } });
        window.addEventListener('hashchange', guard(() => { preview = parseShare(location.hash); render(); }));
    }
    async function start() {
        $('collection-retry').hidden = true;
        try {
            const response = await fetch('/data/collection-catalog.json?v=1', {cache: 'no-store'});
            if (!response.ok) throw new Error('Catalog HTTP ' + response.status);
            const data = await response.json();
            if (data.schema_version !== 1 || !Array.isArray(data.works) || data.works.some(w => !w || !KEY.test(w.key) || typeof w.title !== 'string' || !Array.isArray(w.authors) || !w.authors.every(a => typeof a === 'string') || typeof w.bib !== 'string' || typeof w.ris !== 'string' || !w.csl || w.url !== '/works/' + w.key + '.html') || new Set(data.works.map(w => w.key)).size !== data.works.length) throw new Error('Invalid citation catalog.');
            catalog = new Map(data.works.map(w => [w.key, w]));
            state = {version: 1, active: 'list-initial', lists: [{id: 'list-initial', title: 'Reading list', keys: []}]};
            try { lastRaw = localStorage.getItem(STORAGE_KEY); if (lastRaw !== null) state = parseStore(lastRaw); }
            catch (error) { persistent = false; rawBackup = lastRaw; storageWarning = 'Saved storage is unavailable or unreadable; it has not been overwritten. This tab remains usable. Download a backup before leaving. ' + error.message; }
            try { preview = parseShare(location.hash); } catch (error) { storageWarning += ' ' + error.message; }
            bind(); renderChoices(); render();
            $('collection-app').disabled = false; $('collection-app').setAttribute('aria-busy', 'false');
            const url = new URL(location.href); const key = url.searchParams.get('add');
            if (key !== null) { try { add(key); } catch (error) { report(error.message); } url.searchParams.delete('add'); history.replaceState(null, '', url); }
        } catch (error) { status('Citation catalog unavailable: ' + error.message + ' Browse the bibliography or retry.'); $('collection-retry').hidden = false; }
    }
    $('collection-retry').addEventListener('click', start);
    start();
})();
