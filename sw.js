// The Pages workflow replaces this token with the commit SHA on every deployment.
const CACHE_NAME = "intelligence-library-__BUILD_VERSION__";
const CORE_ASSETS = [
  "./", "./index.html", "./styles.css", "./app.js", "./books.js",
  "./books/bishop-deep-learning-2024/chapter-01.json", "./manifest.webmanifest",
  "./favicon.svg", "./icons/icon-192.png", "./icons/icon-512.png",
  ...Array.from({ length: 22 }, (_, index) => `./books/bishop-deep-learning-2024/pages/page-${String(index + 1).padStart(2, "0")}.webp`),
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(Promise.all([
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))),
    self.clients.claim(),
  ]));
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
  event.respondWith(fetch(event.request).then((response) => {
    if (response.ok) {
      const copy = response.clone();
      event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy)));
    }
    return response;
  }).catch(async () => {
    const cached = await caches.match(event.request);
    if (cached) return cached;
    if (event.request.mode === "navigate") return caches.match("./index.html");
    return Response.error();
  }));
});
