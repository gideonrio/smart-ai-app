const CACHE_NAME = 'farm-ai-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/dashboard',
    '/chatbot',
    '/weather'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            try {
                return cache.addAll(urlsToCache);
            } catch (e) { }
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        }).catch(() => {
            return new Response('Offline Mode');
        })
    );
});
