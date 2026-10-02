// HTML escape helper for client-side search surfaces (plain script, no module).

function esc(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/* Shared progressive index loader. Autocomplete needs only the core; the
 * search page requests work/video text when a query is present. Concurrent
 * consumers share in-flight requests, and a failed request remains retryable.
 */
(function (global) {
    'use strict';

    const segmentTypes = ['work', 'video'];
    let core = null;
    let corePromise = null;
    let reloadNeeded = false;
    let revisionEpoch = 0;
    const segments = new Map();
    const pendingSegments = new Map();

    async function readIndex(path) {
        const response = await fetch(path, { cache: 'no-cache' });
        if (!response.ok) throw new Error('Search index request failed: ' + response.status);
        const data = await response.json();
        if (!data || !Array.isArray(data.items) || typeof data.generated_at !== 'string') {
            throw new Error('Invalid search index: ' + path);
        }
        return data;
    }

    function loadCore() {
        // A deploy may change the segment files after this tab loaded core.
        // The next explicit retry gets one fresh core and coherent segments;
        // do not recurse within a failed attempt during an unstable deploy.
        if (reloadNeeded) {
            reloadNeeded = false;
            revisionEpoch++;
            corePromise = null;
            segments.clear();
            pendingSegments.clear();
        }
        if (!corePromise) {
            corePromise = readIndex('/search-index-core.json').then(data => {
                const seen = new Set();
                data.items.forEach(item => {
                    if (!item || typeof item.id !== 'string' || typeof item.type !== 'string' ||
                            typeof item.title !== 'string' || typeof item.url !== 'string' || seen.has(item.id)) {
                        throw new Error('Invalid or duplicate core search entry');
                    }
                    seen.add(item.id);
                });
                if (!Array.isArray(data.content_segments) ||
                        data.content_segments.some(type => !segmentTypes.includes(type))) {
                    throw new Error('Unsupported search content segment');
                }
                core = data;
                return data.items;
            }).catch(error => {
                corePromise = null;
                throw error;
            });
        }
        return corePromise;
    }

    function getItems() {
        if (!core) return [];
        return core.items.map(item => {
            const segment = segments.get(item.type);
            return segment && segment.has(item.id)
                ? Object.assign({}, item, { content: segment.get(item.id) })
                : item;
        });
    }

    function loadSegment(type) {
        if (segments.has(type)) return Promise.resolve();
        if (!pendingSegments.has(type)) {
            const requestedCore = core;
            const requestedEpoch = revisionEpoch;
            const request = readIndex('/search-index-content-' + type + '.json').then(data => {
                if (requestedEpoch !== revisionEpoch) {
                    throw new Error('Search request was superseded by a newer index revision');
                }
                if (data.generated_at !== requestedCore.generated_at) {
                    reloadNeeded = true;
                    throw new Error('Search content belongs to a different index revision');
                }
                if (data.type !== type) throw new Error('Invalid search content segment type');
                const expected = new Set(requestedCore.items.filter(item => item.type === type).map(item => item.id));
                const text = new Map();
                data.items.forEach(item => {
                    if (!item || item.type !== type || !expected.has(item.id) ||
                            typeof item.content !== 'string' || text.has(item.id)) {
                        throw new Error('Invalid or duplicate search content entry');
                    }
                    text.set(item.id, item.content);
                });
                if (text.size !== expected.size) throw new Error('Incomplete search content segment');
                segments.set(type, text);
            }).finally(() => {
                // An old request can finish after a retry starts a new one.
                if (pendingSegments.get(type) === request) pendingSegments.delete(type);
            });
            pendingSegments.set(type, request);
        }
        return pendingSegments.get(type);
    }

    async function loadContent(types) {
        await loadCore();
        const requested = types === undefined ? core.content_segments : types;
        if (!Array.isArray(requested) || requested.some(type => !segmentTypes.includes(type))) {
            throw new Error('Unsupported search content segment');
        }
        await Promise.all(Array.from(new Set(requested)).map(loadSegment));
        return getItems();
    }

    function getRevision() {
        return core ? core.generated_at : null;
    }

    global.DocxologySearch = Object.freeze({ loadCore, loadContent, getItems, getRevision });
})(typeof window !== 'undefined' ? window : globalThis);
