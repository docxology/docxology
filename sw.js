// Service Worker for danielarifriedman.com
// Cache-first strategy for static assets, network-first for pages
const CACHE_NAME = 'daf-portfolio-v13';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/js/hero-glitch.js',
  '/js/publications.js',
  '/assets/hero-art/an-ant-is-a-colony.webp',
  '/assets/hero-art/ant-head.webp',
  '/assets/hero-art/army-ants.webp',
  '/assets/hero-art/decentral-antelligence-agency.webp',
  '/assets/hero-art/mesh-network.webp',
  '/art.html',
  '/discovery.html',
  '/domains.html',
  '/domain-entomology.html',
  '/domain-active-inference.html',
  '/domain-cognitive-security.html',
  '/domain-art-synergetics.html',
  '/domain-computational.html',
  '/cite-verify.html',
  '/evidence.html',
  '/search.html',
  '/catalog.html',
  '/updates.html',
  '/works/index.html',
  '/feed.xml',
  '/opensearch.xml',
  '/llms.txt',
  '/humans.txt',
  '/AGENT_START.md',
  '/search-index.json',
  '/codemeta.json',
  '/CITATION.cff',
  '/bibliography.bib',
  '/bibliography.csl.json',
  '/bibliography.ris',
  '/data/works.json',
  '/data/artworks.json',
  '/data/software.json',
  '/data/people.json',
  '/data/organizations.json',
  '/data/claims.json',
  '/data/catalog.json',
  '/data/work-enrichment.json',
  '/data/reconciliation.json',
  '/data/generated-manifest.json',
  '/reports/asset_size_2026-05-13.json',
  '/reports/external_links_2026-05-13.json',
  '/reports/external_links_triage_2026-05-13.json',
  '/reports/live_site_verification_2026-05-13.json',
  '/GENERATED.md',
  '/publications.html',
  '/software.html',
  '/videos.html',
  '/manifest.json'
];

// Install: pre-cache core shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: stale-while-revalidate for HTML, cache-first for fonts/css
self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;

  // For navigation requests: network-first with cache fallback
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // For other resources: cache-first with network fallback
  event.respondWith(
    caches.match(request).then(cached => {
      if (cached) return cached;
      return fetch(request).then(response => {
        if (response.ok && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      });
    })
  );
});
