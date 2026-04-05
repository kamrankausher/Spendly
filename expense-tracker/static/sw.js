const CACHE_NAME = 'spendly-v6';
const ASSETS = [
    '/',
    '/dashboard',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/manifest.json'
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', e => {
    // Network-first for API and form submissions
    if (e.request.method !== 'GET' || e.request.url.includes('/api/')) {
        return;
    }
    e.respondWith(
        fetch(e.request)
            .then(r => {
                const clone = r.clone();
                caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
                return r;
            })
            .catch(() => caches.match(e.request))
    );
});
