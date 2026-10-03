// The Pages workflow replaces this token with the commit SHA on every deployment.
const CACHE_NAME = "intelligence-library-__BUILD_VERSION__";
const IMAGE_CACHE_NAME = "intelligence-library-images-v1";
const CACHE_PREFIX = "intelligence-library-";

function isBookImage(url) {
  return /\/books\/[^/]+\/assets\/.+\.(?:png|jpe?g|webp|gif|svg)$/i.test(url.pathname);
}
const CORE_ASSETS = [
  "./", "./index.html", "./styles.css", "./app.js", "./books.js",
  "./books/bishop-deep-learning-2024/frontmatter.json",
  "./books/bishop-deep-learning-2024/chapter-00.json",
  "./books/bishop-deep-learning-2024/contents.json",
  "./books/bishop-deep-learning-2024/chapter-01.json", "./manifest.webmanifest",
  "./books/bishop-deep-learning-2024/chapter-02.json",
  "./books/bishop-deep-learning-2024/chapter-03.json",
  "./books/bishop-deep-learning-2024/chapter-04.json",
  "./books/bishop-deep-learning-2024/chapter-05.json",
  "./books/bishop-deep-learning-2024/chapter-06.json",
  "./books/bishop-deep-learning-2024/chapter-07.json",
  "./books/bishop-deep-learning-2024/chapter-08.json",
  "./books/bishop-deep-learning-2024/chapter-09.json",
  "./books/bishop-deep-learning-2024/chapter-10.json",
  "./books/bishop-deep-learning-2024/chapter-11.json",
  "./books/bishop-deep-learning-2024/chapter-12.json",
  "./books/bishop-deep-learning-2024/chapter-13.json",
  "./books/bishop-deep-learning-2024/chapter-14.json",
  "./books/bishop-deep-learning-2024/chapter-15.json",
  "./books/bishop-deep-learning-2024/chapter-16.json",
  "./books/bishop-deep-learning-2024/chapter-17.json",
  "./books/bishop-deep-learning-2024/chapter-18.json",
  "./books/bishop-deep-learning-2024/chapter-19.json",
  "./books/bishop-deep-learning-2024/chapter-20.json",
  "./books/bishop-deep-learning-2024/appendix-a.json",
  "./books/bishop-deep-learning-2024/appendix-b.json",
  "./books/bishop-deep-learning-2024/appendix-c.json",
  "./books/bishop-deep-learning-2024/bibliography.json",
  "./books/bishop-deep-learning-2024/index.json",
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
  event.waitUntil((async () => {
    const oldVersions = (await caches.keys()).filter((key) =>
      key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME && key !== IMAGE_CACHE_NAME);
    const imageCache = await caches.open(IMAGE_CACHE_NAME);
    for (const name of oldVersions) {
      const oldCache = await caches.open(name);
      for (const request of await oldCache.keys()) {
        if (!isBookImage(new URL(request.url)) || await imageCache.match(request)) continue;
        const response = await oldCache.match(request);
        if (response) await imageCache.put(request, response);
      }
      await caches.delete(name);
    }
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
  event.respondWith(fetch(event.request, { cache: "no-cache" }).then((response) => {
    if (response.ok) {
      const copy = response.clone();
      const cacheName = isBookImage(url) ? IMAGE_CACHE_NAME : CACHE_NAME;
      event.waitUntil(caches.open(cacheName).then((cache) => cache.put(event.request, copy)));
    }
    return response;
  }).catch(async () => {
    const cached = await caches.match(event.request);
    if (cached) return cached;
    if (event.request.mode === "navigate") return caches.match("./index.html");
    return Response.error();
  }));
});
