const CACHE = 'quizzer-v15';
const PRECACHE = ['./', './index.html', './sw.js', './sample-quiz.json'];

self.addEventListener('install', function (event) {
  event.waitUntil((async function () {
    const cache = await caches.open(CACHE);
    await Promise.all(PRECACHE.map(function (url) {
      return cache.add(url).catch(function () {});
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', function (event) {
  event.waitUntil((async function () {
    const keys = await caches.keys();
    await Promise.all(keys.filter(function (key) {
      return key !== CACHE;
    }).map(function (key) {
      return caches.delete(key);
    }));
    await self.clients.claim();
  })());
});

self.addEventListener('message', function (event) {
  const data = event.data || {};
  if (data.type !== 'CACHE_URLS' || !data.urls) return;
  event.waitUntil(caches.open(CACHE).then(function (cache) {
    return Promise.all(data.urls.map(function (url) {
      return cache.add(url).catch(function () {});
    }));
  }));
});

self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;
  event.respondWith((async function () {
    const cache = await caches.open(CACHE);
    try {
      const fresh = await fetch(event.request);
      cache.put(event.request, fresh.clone()).catch(function () {});
      return fresh;
    } catch (err) {
      const cached = await cache.match(event.request, { ignoreSearch: true });
      if (cached) return cached;
      if (event.request.mode === 'navigate') {
        return (await cache.match('./index.html')) || (await cache.match('./')) || Response.error();
      }
      throw err;
    }
  })());
});
