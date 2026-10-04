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
  "./books/bishop-deep-learning-2024/reference-index.json",
  "./books/bishop-deep-learning-2024/offline-images.json",
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
  "./books/sutton-barto-reinforcement-learning-2e/chapter-00.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-01.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-I.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-02.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-03.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-04.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-05.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-06.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-07.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-08.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-II.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-09.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-10.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-11.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-12.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-13.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-III.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-14.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-15.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-16.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-17.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-REF.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-IDX.json",
  "./books/sutton-barto-reinforcement-learning-2e/chapter-SERIES.json",
  "./books/sutton-barto-reinforcement-learning-2e/reference-index.json",
  "./books/sutton-barto-reinforcement-learning-2e/offline-images.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-frontmatter.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-contents.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-preface.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-01.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-part-I.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-02.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-03.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-04.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-05.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-part-II.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-06.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-07.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-08.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-part-III.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-09.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-10.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-11.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-appendices.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-A.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-B.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-C.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-references.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/chapter-notation.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/offline-images.json",
  "./books/boyd-vandenberghe-convex-optimization-2004/assets/fonts/STIXTwoMath-Regular.woff2",
];

const MACKAY_CHAPTER_IDS = [
  "00", "01", "02", "03-intro", "03", "I", "04-intro", "04", "05-intro", "05",
  "06-intro", "06", "07", "II", "08", "09-intro", "09", "10-intro", "10", "11-intro",
  "11", "III", "12-intro", "12", "13-intro", "13", "14-intro", "14", "15", "16",
  "17", "18", "19", "IV", "IV-intro", "20", "21", "22", "23", "24",
  "25", "26", "27", "28", "29-intro", "29", "30", "31-intro", "31", "32",
  "33", "34", "35", "36", "37", "V", "38", "39", "40-prelude", "40",
  "41", "41-postscript", "42", "43", "44", "45-prelude", "45", "46", "VI", "VI-intro",
  "47", "48", "49", "50-intro", "50", "VII", "A", "B", "C", "REF", "IDX",
];
CORE_ASSETS.push(
  "./books/mackay-information-theory-2003/reference-index.json",
  "./books/mackay-information-theory-2003/offline-images.json",
  ...MACKAY_CHAPTER_IDS.map((id) => `./books/mackay-information-theory-2003/chapter-${id}.json`),
);

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

const offlineImageJobs = new Map();

function reportOfflineImages(job, state, done, total, totalBytes = 0) {
  job.latest = { type: "offline-images-status", state, done, total, totalBytes };
  for (const port of job.ports) {
    try { port.postMessage(job.latest); } catch { job.ports.delete(port); }
  }
}

async function prepareOfflineImages(path, job) {
  const bookId = path.match(/^books\/([a-z0-9-]+)\/offline-images\.json$/)?.[1];
  if (!bookId) throw new Error("Invalid image manifest path");
  const manifestUrl = new URL(`./${path}`, self.registration.scope);
  let response;
  try { response = await fetch(manifestUrl, { cache: "no-cache" }); }
  catch { response = await caches.match(manifestUrl); }
  if (!response?.ok) throw new Error("Image manifest unavailable");
  const manifest = await response.json();
  if (manifest.bookId !== bookId || !/^[a-f0-9]{20}$/.test(manifest.version) ||
      !Array.isArray(manifest.assets) || manifest.assets.length > 10000 ||
      new Set(manifest.assets).size !== manifest.assets.length ||
      !manifest.assets.every((asset) => typeof asset === "string" &&
        asset.startsWith(`books/${bookId}/assets/`) && !asset.includes("..") &&
        isBookImage(new URL(`./${asset}`, self.registration.scope)))) {
    throw new Error("Invalid image manifest");
  }
  const imageCache = await caches.open(IMAGE_CACHE_NAME);
  const versionUrl = new URL(`./books/${bookId}/offline-images-version`, self.registration.scope);
  const cachedVersion = (await (await imageCache.match(versionUrl))?.text()) || "";
  const urls = manifest.assets.map((asset) => new URL(`./${asset}`, self.registration.scope));
  const total = urls.length;
  const totalBytes = manifest.totalBytes || 0;
  let done = 0;
  let pending = urls;

  if (cachedVersion === manifest.version) {
    pending = [];
    for (const url of urls) {
      if (await imageCache.match(url)) done += 1;
      else pending.push(url);
    }
    if (done === total) {
      reportOfflineImages(job, "complete", done, total, totalBytes);
      return;
    }
  }
  reportOfflineImages(job, "progress", done, total, totalBytes);

  let next = 0;
  let failures = 0;
  async function worker() {
    while (next < pending.length) {
      const url = pending[next++];
      try {
        const fetched = await fetch(url, { cache: "no-cache" });
        if (!fetched.ok) throw new Error(`HTTP ${fetched.status}`);
        await imageCache.put(url, fetched);
        done += 1;
      } catch {
        failures += 1;
      }
      reportOfflineImages(job, "progress", done, total, totalBytes);
    }
  }
  await Promise.all(Array.from({ length: Math.min(4, pending.length) }, worker));
  if (failures) {
    reportOfflineImages(job, "error", done, total, totalBytes);
    return;
  }
  const assetUrls = new Set(urls.map((url) => url.href));
  for (const request of await imageCache.keys()) {
    if (request.url.includes(`/books/${bookId}/assets/`) && !assetUrls.has(request.url)) {
      await imageCache.delete(request);
    }
  }
  await imageCache.put(versionUrl, new Response(manifest.version));
  reportOfflineImages(job, "complete", total, total, totalBytes);
}

self.addEventListener("message", (event) => {
  if (event.data?.type !== "prepare-offline-images" || typeof event.data.path !== "string") return;
  const path = event.data.path;
  const port = event.ports[0];
  if (!port) return;
  let job = offlineImageJobs.get(path);
  if (job) {
    job.ports.add(port);
    if (job.latest) port.postMessage(job.latest);
    event.waitUntil(job.promise);
    return;
  }
  job = { ports: new Set([port]), latest: null, promise: null };
  offlineImageJobs.set(path, job);
  job.promise = prepareOfflineImages(path, job).catch(() => {
    reportOfflineImages(job, "error", job.latest?.done || 0, job.latest?.total || 0);
  }).finally(() => offlineImageJobs.delete(path));
  event.waitUntil(job.promise);
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
