const shelf = Array.isArray(books) ? books : [];
const params = new URLSearchParams(location.search);
const activeBook = shelf.find((book) => book.id === params.get("book"));
const progressPrefix = "intelligence-library:progress:v2:";
const languageKey = "intelligence-library:language:v1";
const state = { category: "all", query: "", language: readStorage(languageKey) || "both" };

function readStorage(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function writeStorage(key, value) {
  try { localStorage.setItem(key, value); } catch { /* Storage may be disabled. */ }
}
function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}
function bookUrl(book, pageNumber) {
  const url = new URL("./", location.href);
  url.searchParams.set("book", book.id);
  if (pageNumber) url.searchParams.set("page", String(pageNumber));
  return url.href;
}
function getProgress(book) {
  try {
    const value = JSON.parse(readStorage(progressPrefix + book.id));
    return value && Number.isInteger(value.page) ? value : null;
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
      if (progress) info.append(element("p", "book-progress", `● 已读到第 ${progress.page} 页`));
      const links = element("div", "book-links");
      const read = element("a", "read-link", progress ? "继续阅读 ↗" : "阅读第一章 ↗");
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
    if (!Array.isArray(content.pages) || !content.pages.length) throw new Error("No pages");
  } catch {
    const status = document.querySelector("#reader-status");
    status.textContent = "本章暂时无法加载。请检查网络连接，然后刷新页面。";
    status.hidden = false;
    return;
  }

  const pages = content.pages;
  const saved = getProgress(book);
  const requested = Number(params.get("page"));
  let current = pages.find((page) => page.number === requested) || pages.find((page) => page.number === saved?.page) || pages[0];
  const article = document.querySelector("#reader-article");
  const toc = document.querySelector("#reader-toc");
  const languageButtons = [...document.querySelectorAll("[data-language]")];
  if (!["both", "zh", "en"].includes(state.language)) state.language = "both";

  function setLanguage(language) {
    state.language = language;
    writeStorage(languageKey, language);
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
    writeStorage(progressPrefix + book.id, JSON.stringify({ page: current.number, block: blockId, updatedAt: Date.now() }));
  }

  function drawToc() {
    toc.replaceChildren(...content.toc.map((entry, index) => {
      const next = content.toc[index + 1];
      const selected = entry.page <= current.number && (!next || current.number < next.page);
      const link = element("a", selected ? "toc-link active" : "toc-link", `${entry.number} ${entry.title}`);
      link.href = bookUrl(book, entry.page);
      if (selected) link.setAttribute("aria-current", "page");
      link.addEventListener("click", (event) => {
        event.preventDefault();
        selectPage(pages.find((page) => page.number === entry.page), true);
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
      return link;
    }));
  }

  function renderBlock(block) {
    const node = element("div", `translation-block translation-${block.kind || "paragraph"}`);
    node.id = `read-${block.id}`;
    if (block.kind === "table") {
      const wrapper = element("div", "translation-table-scroll");
      const table = element("table", "translation-table");
      block.zh.split("\n").filter((line) => line.startsWith("|")).forEach((line, index) => {
        if (index === 1) return;
        const row = element("tr");
        line.slice(1, -1).split("|").forEach((cell) => row.append(element(index === 0 ? "th" : "td", "", cell.trim())));
        table.append(row);
      });
      wrapper.append(table);
      node.append(wrapper);
    } else {
      node.append(element(block.kind === "heading" ? "h2" : "p", "translation-zh", block.zh));
    }
    return node;
  }

  function selectPage(page, updateUrl, restoreBlock) {
    current = page;
    const index = pages.findIndex((item) => item.number === page.number);
    document.querySelector("#reader-chapter-kicker").textContent = `CHAPTER 01 / PAGE ${String(page.number).padStart(2, "0")} OF ${pages.length}`;
    document.querySelector("#reader-section-title").textContent = content.title;
    document.querySelector("#reader-section-en").textContent = content.originalTitle;
    document.querySelector("#reader-lede").textContent = `原书第 ${page.number} 页 · PDF 第 ${page.pdfPage} 页`;
    document.querySelector("#reader-count").textContent = `${page.number} / ${pages.length}`;
    document.querySelector("#reading-progress").style.width = `${((index + 1) / pages.length) * 100}%`;

    const grid = element("div", "reader-page-grid");
    const original = element("div", "reader-page-original");
    const imageLink = element("a", "facsimile-link");
    imageLink.href = new URL(page.image, document.baseURI).href;
    imageLink.target = "_blank";
    imageLink.rel = "noopener noreferrer";
    imageLink.setAttribute("aria-label", `打开原书第 ${page.number} 页大图`);
    const image = element("img");
    image.src = imageLink.href;
    image.alt = `《Deep Learning: Foundations and Concepts》第 1 章第 ${page.number} 页原版页图`;
    image.loading = "eager";
    imageLink.append(image);
    original.append(element("p", "reader-panel-label", `ORIGINAL · P. ${page.number} / 点击放大`), imageLink);
    const transcript = element("details", "source-transcript");
    transcript.append(element("summary", "", "可选取的英文原文文本（以页图为准）"));
    transcript.append(element("pre", "", page.sourceText));
    original.append(transcript);

    const translation = element("div", "reader-page-translation");
    translation.append(element("p", "reader-panel-label", `中文译文 · 第 ${page.number} 页`));
    translation.append(...page.blocks.map(renderBlock));
    grid.append(original, translation);
    article.replaceChildren(grid);

    const previous = document.querySelector("#previous-section");
    const next = document.querySelector("#next-section");
    previous.disabled = index === 0;
    next.disabled = index === pages.length - 1;
    previous.onclick = () => { selectPage(pages[index - 1], true); window.scrollTo({ top: 0, behavior: "smooth" }); };
    next.onclick = () => { selectPage(pages[index + 1], true); window.scrollTo({ top: 0, behavior: "smooth" }); };
    drawToc();
    if (updateUrl) history.pushState({ page: page.number }, "", bookUrl(book, page.number));
    savePosition(restoreBlock || `read-${page.blocks[0]?.id}`);
    if (restoreBlock && document.getElementById(restoreBlock)) {
      requestAnimationFrame(() => document.getElementById(restoreBlock)?.scrollIntoView({ block: "start" }));
    }
  }

  const restore = (!requested || requested === saved?.page) ? saved?.block : null;
  selectPage(current, false, restore);
  window.addEventListener("popstate", () => {
    const pageNumber = Number(new URLSearchParams(location.search).get("page"));
    selectPage(pages.find((page) => page.number === pageNumber) || pages[0], false);
  });
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const reached = [...article.querySelectorAll(".translation-block")].filter((block) => block.getBoundingClientRect().top < innerHeight * 0.42);
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
