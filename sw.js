// The Pages workflow replaces this token with the commit SHA on every deployment.
const CACHE_NAME = "intelligence-library-__BUILD_VERSION__";
const CORE_ASSETS = [
  "./", "./index.html", "./styles.css", "./app.js", "./books.js",
  "./books/bishop-deep-learning-2024/chapter-01.json", "./manifest.webmanifest",
  "./favicon.svg", "./icons/icon-180.png", "./icons/icon-192.png", "./icons/icon-512.png",
  "./books/shannon-mathematical-theory-1948/chapter-00.json",
  "./books/shannon-mathematical-theory-1948/chapter-01.json",
  "./books/shannon-mathematical-theory-1948/chapter-02.json",
  "./books/shannon-mathematical-theory-1948/chapter-a1-a4.json",
  "./books/shannon-mathematical-theory-1948/chapter-03.json",
  "./books/shannon-mathematical-theory-1948/chapter-04.json",
  "./books/shannon-mathematical-theory-1948/chapter-05.json",
  "./books/shannon-mathematical-theory-1948/chapter-a5-a7.json",
  "./books/shannon-mathematical-theory-1948/assets/fig-1.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-2.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-3.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-4.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-5.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-6.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-7.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-8.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-9.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-10.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-11.png",
  "./books/shannon-mathematical-theory-1948/assets/fig-12.png",
  "./books/shannon-mathematical-theory-1948/assets/table-i-original.png",
];

self.addEventListener("install", (event) => {
  const freshAssets = CORE_ASSETS.map((path) => new Request(new URL(path, self.registration.scope), { cache: "reload" }));
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(freshAssets)).then(() => self.skipWaiting()));
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
  event.respondWith(fetch(event.request, { cache: "no-cache" }).then((response) => {
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
