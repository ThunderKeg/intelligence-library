const shelf = Array.isArray(books) ? books : [];
const params = new URLSearchParams(location.search);
const activeBook = shelf.find((book) => book.id === params.get("book"));
const progressPrefix = "intelligence-library:progress:v2:";

function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}

function readProgress(book) {
  try {
    const progress = JSON.parse(localStorage.getItem(progressPrefix + book.id));
    return progress && typeof progress.block === "string" ? progress : null;
  } catch { return null; }
}

function saveProgress(book, blockId) {
  const page = Number(blockId.match(/^read-p(\d+)-/)?.[1]);
  try {
    localStorage.setItem(progressPrefix + book.id, JSON.stringify({ page, block: blockId, updatedAt: Date.now() }));
  } catch { /* Reading remains available when storage is disabled. */ }
}

function bookUrl(book) {
  const url = new URL("./", location.href);
  url.searchParams.set("book", book.id);
  return url.href;
}

function renderShelf() {
  const grid = document.querySelector("#book-grid");
  const search = document.querySelector("#search");
  document.querySelector("#book-count").textContent = `${shelf.length} 本书`;

  function draw() {
    const query = search.value.trim().toLocaleLowerCase();
    const matches = shelf.filter((book) =>
      [book.title, book.originalTitle, book.author, book.description].join(" ").toLocaleLowerCase().includes(query));
    grid.replaceChildren(...matches.map((book) => {
      const card = element("article", "book-card");
      const title = element("h2", "book-title", book.title);
      const original = element("p", "book-original-title", book.originalTitle);
      const author = element("p", "book-author", `${book.author} · ${book.year}`);
      const description = element("p", "book-description", book.description);
      const read = element("a", "read-link", readProgress(book) ? "继续阅读 →" : "开始阅读 →");
      read.href = bookUrl(book);
      card.append(title, original, author, description, read);
      return card;
    }));
    document.querySelector("#empty-state").hidden = matches.length > 0;
  }

  search.addEventListener("input", draw);
  draw();
}

function renderTable(text) {
  const wrapper = element("div", "table-scroll");
  const table = element("table", "book-table");
  text.split("\n").filter((line) => line.startsWith("|")).forEach((line, index) => {
    if (index === 1) return;
    const row = element("tr");
    line.slice(1, -1).split("|").forEach((cell) => row.append(element(index === 0 ? "th" : "td", "", cell.trim())));
    table.append(row);
  });
  wrapper.append(table);
  return wrapper;
}

function renderBlock(block) {
  const node = element("div", `reading-block reading-${block.kind}`);
  node.id = `read-${block.id}`;
  if (block.kind === "table") {
    node.append(renderTable(block.text));
  } else if (block.kind === "heading") {
    const number = block.text.match(/^(\d+(?:\.\d+)*)(?:\s|$)/)?.[1];
    const depth = number ? number.split(".").length : (block.text.startsWith("第 1 章") ? 1 : 3);
    node.append(element(`h${Math.min(depth, 3)}`, "", block.text));
  } else {
    node.append(element("p", "", block.text));
  }
  return node;
}

async function renderReader(book) {
  document.querySelector("#landing-view").hidden = true;
  document.querySelector("#reader-view").hidden = false;
  document.querySelector("#reader-book-title").textContent = book.title;
  document.title = `${book.title} · 算经阁`;

  let chapter;
  try {
    const response = await fetch(new URL(book.content, document.baseURI));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    chapter = await response.json();
    if (!Array.isArray(chapter.blocks) || !chapter.blocks.length) throw new Error("Empty chapter");
  } catch {
    const status = document.querySelector("#reader-status");
    status.textContent = "内容暂时无法加载，请检查网络后刷新。";
    status.hidden = false;
    return;
  }

  const blocks = chapter.blocks;
  const article = document.querySelector("#reader-article");
  article.replaceChildren(...blocks.map(renderBlock));
  const nodes = [...article.querySelectorAll(".reading-block")];
  const indexById = new Map(nodes.map((node, index) => [node.id, index]));
  const toc = document.querySelector("#reader-toc");
  const menu = document.querySelector("#reader-menu");
  const desktop = matchMedia("(min-width: 800px)");
  const setMenuForWidth = () => { menu.open = desktop.matches; };
  setMenuForWidth();
  desktop.addEventListener("change", setMenuForWidth);

  toc.replaceChildren(...chapter.toc.map((entry) => {
    const link = element("a", "toc-link", `${entry.number} ${entry.title}`);
    link.href = `#read-${entry.block}`;
    link.addEventListener("click", () => { if (!desktop.matches) menu.open = false; });
    return link;
  }));

  let lastSaved = "";
  function updatePosition() {
    let current = 0;
    const threshold = innerHeight * 0.35;
    for (let index = 0; index < nodes.length; index += 1) {
      if (nodes[index].getBoundingClientRect().top <= threshold) current = index;
      else break;
    }
    const blockId = nodes[current].id;
    if (blockId !== lastSaved) {
      saveProgress(book, blockId);
      lastSaved = blockId;
    }
    document.querySelector("#reading-progress").style.width = `${((current + 1) / nodes.length) * 100}%`;
    const currentToc = [...chapter.toc].reverse().find((entry) => (indexById.get(`read-${entry.block}`) ?? 0) <= current);
    for (const link of toc.querySelectorAll("a")) {
      const selected = link.hash === `#read-${currentToc?.block}`;
      link.classList.toggle("active", selected);
      if (selected) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }

  const saved = readProgress(book);
  const legacyPage = Number(params.get("page"));
  const legacyBlock = blocks.find((block) => block.page === legacyPage)?.id;
  const requested = decodeURIComponent(location.hash.slice(1));
  const restoreId = indexById.has(requested) ? requested :
    legacyBlock ? `read-${legacyBlock}` :
    indexById.has(saved?.block) ? saved.block :
    saved?.page ? `read-${blocks.find((block) => block.page === saved.page)?.id}` : null;
  const startTracking = () => {
    if (restoreId) document.getElementById(restoreId)?.scrollIntoView({ block: "start", behavior: "instant" });
    updatePosition();
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { ticking = false; updatePosition(); });
    }, { passive: true });
  };
  document.fonts.ready.then(() => requestAnimationFrame(startTracking));
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
  } catch { /* Reading remains available without offline support. */ }
}

if (activeBook) renderReader(activeBook);
else renderShelf();
setupPwa();
