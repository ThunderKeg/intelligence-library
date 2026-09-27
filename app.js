const shelf = Array.isArray(books) ? books : [];
const params = new URLSearchParams(location.search);
const activeBook = shelf.find((book) => book.id === params.get("book"));
const progressPrefix = "intelligence-library:progress:v1:";
const languageKey = "intelligence-library:language:v1";
const state = { category: "all", query: "", language: readStorage(languageKey) || "both" };

function readStorage(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function writeStorage(key, value) {
  try { localStorage.setItem(key, value); } catch { /* Storage can be disabled. */ }
}
function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}
function bookUrl(book, sectionId) {
  const url = new URL("./", location.href);
  url.searchParams.set("book", book.id);
  if (sectionId) url.searchParams.set("section", sectionId);
  return url.href;
}
function getProgress(book) {
  try {
    const value = JSON.parse(readStorage(progressPrefix + book.id));
    return value && typeof value.section === "string" ? value : null;
  } catch { return null; }
}

function renderShelf() {
  const grid = document.querySelector("#book-grid");
  const filters = document.querySelector("#category-filters");
  const empty = document.querySelector("#empty-state");
  document.querySelector("#collection-count").textContent = `${shelf.length} ${shelf.length === 1 ? "BOOK" : "BOOKS"} & COUNTING`;
  function drawFilters() {
    filters.replaceChildren(...categories.map(({ value, label }) => {
      const button = element("button", value === state.category ? "active" : "", label);
      button.type = "button";
      button.setAttribute("aria-pressed", String(value === state.category));
      button.addEventListener("click", () => { state.category = value; drawFilters(); drawCards(); });
      return button;
    }));
  }
  function drawCards() {
    const visible = shelf.filter((book) =>
      (state.category === "all" || book.category === state.category) &&
      [book.title, book.originalTitle, book.author, book.description].join(" ").toLocaleLowerCase().includes(state.query));
    grid.replaceChildren(...visible.map((book) => {
      const card = element("article", "book-card");
      card.style.setProperty("--book-accent", book.accent || "#3c6856");
      const cover = element("div", "book-cover");
      cover.append(element("span", "book-cover-kicker", "INTELLIGENCE LIBRARY"),
        element("span", "book-cover-symbol", book.coverSymbol || "✳"),
        element("span", "book-cover-title", book.coverTitle || book.originalTitle || book.title),
        element("span", "book-cover-footer", book.coverSeries || book.author));
      const info = element("div", "book-card-info");
      const top = element("div", "book-card-top");
      top.append(element("span", "book-category", categories.find((item) => item.value === book.category)?.label || book.category),
        element("span", "book-edition", book.status || "馆藏"));
      info.append(top, element("h3", "book-title", book.title),
        element("p", "book-original-title", book.originalTitle),
        element("p", "book-author", `${book.author} · ${book.year}`),
        element("p", "book-description", book.description));
      const progress = getProgress(book);
      if (progress) info.append(element("p", "book-progress", `● 已记录阅读位置 · ${progress.label || "继续阅读"}`));
      const links = element("div", "book-links");
      const read = element("a", "read-link", progress ? "继续阅读 ↗" : "阅读样章 ↗");
      read.href = bookUrl(book);
      links.append(read);
      for (const item of book.links || []) {
        try {
          const url = new URL(item.url);
          if (!["https:", "http:"].includes(url.protocol)) continue;
          const link = element("a", "book-link", `${item.label} ↗`);
          link.href = url.href; link.target = "_blank"; link.rel = "noopener noreferrer";
          links.append(link);
        } catch { /* Ignore malformed links. */ }
      }
      info.append(links);
      card.append(cover, info);
      return card;
    }));
    grid.hidden = visible.length === 0;
    empty.hidden = visible.length > 0;
    document.querySelector("#empty-title").textContent = shelf.length ? "暂时没有找到这本书。" : "书架已经备好。";
    document.querySelector("#empty-description").textContent = shelf.length ? "试试其他关键词或筛选条件。" : "第一本值得收藏的书，即将在这里上架。";
  }
  document.querySelector("#search").addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLocaleLowerCase(); drawCards();
  });
  drawFilters(); drawCards();
}

async function renderReader(book) {
  document.querySelector("#landing-view").hidden = true;
  document.querySelector("#reader-view").hidden = false;
  document.querySelector("#header-nav").hidden = true;
  document.querySelector("#reader-book-title").textContent = book.title;
  document.title = `${book.title} · Intelligence Library`;
  let content;
  try {
    const response = await fetch(new URL(book.content, document.baseURI));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    content = await response.json();
    if (!Array.isArray(content.chapters) || !content.chapters.length) throw new Error("No chapters");
  } catch {
    const status = document.querySelector("#reader-status");
    status.textContent = "样章暂时无法加载。请检查网络连接，然后刷新页面。";
    status.hidden = false;
    return;
  }
  const sections = content.chapters.flatMap((chapter) => chapter.sections.map((section) => ({ ...section, chapter })));
  const saved = getProgress(book);
  const requested = params.get("section");
  let current = sections.find((section) => section.id === requested) || sections.find((section) => section.id === saved?.section) || sections[0];
  const article = document.querySelector("#reader-article");
  const toc = document.querySelector("#reader-toc");
  const languageButtons = [...document.querySelectorAll("[data-language]")];
  if (!["both", "zh", "en"].includes(state.language)) state.language = "both";
  function setLanguage(language) {
    state.language = language;
    writeStorage(languageKey, language);
    article.dataset.language = language;
    document.querySelector("#reader-view").dataset.language = language;
    languageButtons.forEach((button) => {
      const selected = button.dataset.language === language;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
  }
  languageButtons.forEach((button) => button.addEventListener("click", () => setLanguage(button.dataset.language)));
  setLanguage(state.language);
  function savePosition(blockId) {
    writeStorage(progressPrefix + book.id, JSON.stringify({ section: current.id, block: blockId, label: current.title, updatedAt: Date.now() }));
  }
  function drawToc() {
    toc.replaceChildren(...content.chapters.map((chapter) => {
      const group = element("div", "toc-group");
      group.append(element("p", "toc-chapter", chapter.title));
      chapter.sections.forEach((section) => {
        const link = element("a", section.id === current.id ? "toc-link active" : "toc-link", section.title);
        link.href = bookUrl(book, section.id);
        if (section.id === current.id) link.setAttribute("aria-current", "page");
        link.addEventListener("click", (event) => {
          event.preventDefault();
          selectSection(sections.find((item) => item.id === section.id), true);
          article.scrollIntoView({ behavior: "smooth", block: "start" });
        });
        group.append(link);
      });
      return group;
    }));
  }
  function drawBlock(block, index) {
    const row = element("div", `reading-block reading-block-${block.type || "text"}`);
    row.id = `${current.id}-block-${index}`;
    if (block.type === "formula") row.append(element("div", "formula", block.formula));
    if (block.type === "callout") row.append(element("span", "callout-label", block.label || "READING NOTE"));
    const copy = element("div", "parallel-copy");
    copy.append(element("p", "copy-en", block.en), element("p", "copy-zh", block.zh));
    row.append(copy);
    return row;
  }
  function selectSection(section, updateUrl, restoreBlock) {
    current = section;
    const index = sections.findIndex((item) => item.id === current.id);
    const chapterNumber = content.chapters.indexOf(current.chapter) + 1;
    document.querySelector("#reader-chapter-kicker").textContent = `CHAPTER ${String(chapterNumber).padStart(2, "0")} / SECTION ${String(index + 1).padStart(2, "0")}`;
    document.querySelector("#reader-section-title").textContent = current.title;
    document.querySelector("#reader-section-en").textContent = current.titleEn;
    document.querySelector("#reader-lede").textContent = current.lede;
    article.replaceChildren(...current.blocks.map(drawBlock));
    document.querySelector("#reader-count").textContent = `${index + 1} / ${sections.length}`;
    document.querySelector("#reading-progress").style.width = `${((index + 1) / sections.length) * 100}%`;
    const previous = document.querySelector("#previous-section");
    const next = document.querySelector("#next-section");
    previous.disabled = index === 0;
    next.disabled = index === sections.length - 1;
    previous.onclick = () => { selectSection(sections[index - 1], true); window.scrollTo({ top: 0, behavior: "smooth" }); };
    next.onclick = () => { selectSection(sections[index + 1], true); window.scrollTo({ top: 0, behavior: "smooth" }); };
    drawToc();
    if (updateUrl) history.pushState({ section: current.id }, "", bookUrl(book, current.id));
    savePosition(restoreBlock || `${current.id}-block-0`);
    if (restoreBlock && document.getElementById(restoreBlock)) {
      requestAnimationFrame(() => document.getElementById(restoreBlock)?.scrollIntoView({ block: "start" }));
    }
  }
  selectSection(current, false, (!requested || requested === saved?.section) ? saved?.block : null);
  window.addEventListener("popstate", () => {
    const id = new URLSearchParams(location.search).get("section");
    selectSection(sections.find((section) => section.id === id) || sections[0], false);
  });
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const reached = [...article.querySelectorAll(".reading-block")].filter((block) => block.getBoundingClientRect().top < innerHeight * 0.42);
      if (reached.length) savePosition(reached[reached.length - 1].id);
    });
  }, { passive: true });
}

async function setupPwa() {
  if (!("serviceWorker" in navigator)) return;
  try {
    const registration = await navigator.serviceWorker.register("./sw.js");
    registration.update();
    setInterval(() => registration.update(), 60 * 60 * 1000);
    let refreshing = false;
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (!refreshing) { refreshing = true; location.reload(); }
    });
  } catch { /* Reading still works without offline support. */ }
}

if (activeBook) renderReader(activeBook);
else renderShelf();
setupPwa();
