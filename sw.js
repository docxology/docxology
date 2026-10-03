// Small offline shell; visited content is cached on demand, never bulk-downloaded.
const CACHE_NAME = 'daf-portfolio-v26';
const CACHE_PREFIX = 'daf-portfolio-';
const SHELL_CACHE = `${CACHE_NAME}-shell`;
// Keep successful visited content across shell updates for returning visitors.
const RUNTIME_CACHE = `${CACHE_PREFIX}runtime-v1`;
const MAX_RUNTIME_ENTRIES = 48;
const MAX_CACHEABLE_BYTES = 2 * 1024 * 1024;
// Bound buffering while completing a response before it can enter the cache.
const MAX_NETWORK_BODY_BYTES = 16 * 1024 * 1024;
const NETWORK_HEADER_TIMEOUT_MS = 5000;
const NETWORK_BODY_TIMEOUT_MS = 25000;
const STATIC_ASSETS = [
  '/', '/index.html', '/style.css', '/css/home.css', '/favicon.ico', '/manifest.json',
  '/js/index-page.js', '/js/interactive.js', '/js/menu-esc.js',
  '/js/tts-controls.js', '/js/search-utils.js', '/js/nav-toggle.js'
];

let cacheWriteQueue = Promise.resolve();

async function storeResponse(request, response) {
  if (!response.ok || response.type !== 'basic' || response.headers.has('Content-Range') ||
      /\bno-store\b/i.test(response.headers.get('Cache-Control') || '')) return;
  const declaredLength = response.headers.get('Content-Length');
  if (declaredLength !== null && Number(declaredLength) > MAX_CACHEABLE_BYTES) return;
  // Content-Length can be absent or compressed: enforce the limit on decoded bytes.
  const reader = response.clone().body?.getReader();
  if (reader) {
    let bytes = 0;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > MAX_CACHEABLE_BYTES) {
        // Do not await cancellation of a tee branch: its sibling may still be consumed.
        reader.cancel().catch(() => {});
        return;
      }
    }
  }
  cacheWriteQueue = cacheWriteQueue.catch(() => {}).then(async () => {
    const cache = await caches.open(RUNTIME_CACHE);
    // Cache.put replaces atomically; a quota error must preserve the prior copy.
    await cache.put(request, response);
    const keys = await cache.keys();
    await Promise.all(keys.slice(0, Math.max(0, keys.length - MAX_RUNTIME_ENTRIES))
      .map(key => cache.delete(key)));
  });
  await cacheWriteQueue;
}

async function cachedResponse(request, { offline = false } = {}) {
  try {
    const runtime = await caches.open(RUNTIME_CACHE);
    const shell = await caches.open(SHELL_CACHE);
    const exact = await runtime.match(request) || await shell.match(request);
    if (exact) return exact;
    // Only offline may reuse the same document or shell path with another query.
    // An online new asset version must reach the network.
    if (offline) {
      if (request.mode === 'navigate') return await runtime.match(request, { ignoreSearch: true });
      return await shell.match(request, { ignoreSearch: true });
    }
  } catch { /* Storage may be unavailable; the network response remains usable. */ }
  return undefined;
}

function unavailableResponse(request) {
  if (request.mode === 'navigate') {
    return new Response('<!doctype html><html lang="en"><head><meta charset="utf-8">' +
      '<meta name="viewport" content="width=device-width, initial-scale=1">' +
      '<title>Page unavailable offline — Daniel Ari Friedman</title></head><body><main>' +
      '<h1>This page is unavailable offline</h1><p>Reconnect to load this page. ' +
      'Previously visited pages remain available while cached.</p>' +
      '<p><a href="/">Open the saved homepage</a></p></main></body></html>', {
      status: 503, headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Security-Policy': "default-src 'none'; base-uri 'none'"
      }
    });
  }
  const isJSON = new URL(request.url).pathname.endsWith('.json');
  return new Response(isJSON ? JSON.stringify({ error: 'offline', message: 'This data is not cached.' }) :
    'This resource is unavailable offline.', {
    status: 503, headers: { 'Content-Type': isJSON ? 'application/json; charset=utf-8' : 'text/plain; charset=utf-8' }
  });
}

async function fetchWithDeadline(request) {
  const controller = new AbortController();
  let timer = setTimeout(() => controller.abort(), NETWORK_HEADER_TIMEOUT_MS);
  try {
    const response = await fetch(request, { signal: controller.signal });
    clearTimeout(timer);
    timer = setTimeout(() => controller.abort(), NETWORK_BODY_TIMEOUT_MS);
    const declaredLength = response.headers.get('Content-Length');
    if (declaredLength !== null && Number(declaredLength) > MAX_NETWORK_BODY_BYTES) {
      controller.abort();
      throw new Error('Response exceeds the service-worker transfer limit');
    }
    // Headers do not complete a fetch. Allow slower mobile body transfers a
    // separate finite window, bounded to 30 seconds including the header wait.
    // A stalled/dripping stream cannot hold navigation or waitUntil forever.
    // Reading the clone leaves the original response consumable.
    const reader = response.clone().body?.getReader();
    if (reader) {
      let bytes = 0;
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          bytes += value.byteLength;
          if (bytes > MAX_NETWORK_BODY_BYTES) {
            controller.abort();
            throw new Error('Response exceeds the service-worker transfer limit');
          }
        }
      } finally {
        reader.releaseLock();
      }
    }
    return response;
  } finally {
    clearTimeout(timer);
  }
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const requests = STATIC_ASSETS.map(url => new Request(url, { cache: 'reload' }));
    const responses = await Promise.all(requests.map(request => fetchWithDeadline(request)));
    if (responses.some(response => !response.ok || response.type !== 'basic')) {
      throw new Error('Offline shell contains an unsuccessful or cross-origin response');
    }
    // Validate every complete bounded response before writing any shell file.
    // Failed downloads preserve the prior worker; activation follows all puts.
    const cache = await caches.open(SHELL_CACHE);
    await Promise.all(requests.map((request, index) => cache.put(request, responses[index])));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith(CACHE_PREFIX) &&
      key !== SHELL_CACHE && key !== RUNTIME_CACHE).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || request.headers.has('Range')) return;
  // Source documents and large archives stay direct downloads, outside browser caches.
  if (/\.(?:pdf|docx?|zip|gz|tar|mp4|mp3|wav)$/i.test(url.pathname)) return;

  const network = fetchWithDeadline(request);
  // Cache writes and revalidation belong to this fetch event's lifetime.
  // Storage/quota failures never invalidate a successful network response.
  event.waitUntil(network.then(response => storeResponse(request, response.clone())).catch(() => {}));
  const isStatic = request.mode !== 'navigate' && /\.(?:css|js|png|jpe?g|webp|avif|gif|svg|ico|woff2?|ttf)$/i.test(url.pathname);
  if (isStatic) {
    event.respondWith((async () => {
      const cached = await cachedResponse(request);
      if (cached) return cached;
      try { return await network; }
      catch { return await cachedResponse(request, { offline: true }) || unavailableResponse(request); }
    })());
    return;
  }
  event.respondWith((async () => {
    try {
      const response = await network;
      if (response.ok) return response;
      // 404/500 responses must not poison a successful offline copy.
      return await cachedResponse(request) || response;
    } catch {
      return await cachedResponse(request, { offline: true }) || unavailableResponse(request);
    }
  })());
});
