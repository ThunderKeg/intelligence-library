const shelf = Array.isArray(books) ? books : [];
const params = new URLSearchParams(location.search);
const activeBook = shelf.find((book) => book.id === params.get("book"));
const progressPrefix = "intelligence-library:progress:v2:";
const themeKey = "intelligence-library:theme:v1";
if (activeBook?.id === "mackay-information-theory-2003" && "scrollRestoration" in history) {
  history.scrollRestoration = "manual";
}

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

function saveProgress(book, chapterId, blockId, sourcePdfPage) {
  const page = Number(blockId.match(/^read-p(\d+)-/)?.[1] ?? sourcePdfPage);
  try {
    localStorage.setItem(progressPrefix + book.id, JSON.stringify({ chapter: chapterId, page, block: blockId, updatedAt: Date.now() }));
  } catch { /* Reading remains available when storage is disabled. */ }
}

function bookUrl(book, chapterId) {
  const url = new URL("./", location.href);
  url.searchParams.set("book", book.id);
  if (chapterId) url.searchParams.set("chapter", chapterId);
  return url.href;
}

function setupTheme() {
  const button = document.querySelector("#theme-toggle");
  const system = matchMedia("(prefers-color-scheme: dark)");
  let preference;
  try { preference = localStorage.getItem(themeKey); } catch { /* Use system theme. */ }
  if (!["light", "dark"].includes(preference)) preference = null;

  function apply(theme, save) {
    document.documentElement.dataset.theme = theme;
    button.textContent = theme === "dark" ? "浅色模式" : "深色模式";
    button.setAttribute("aria-label", theme === "dark" ? "切换浅色模式" : "切换深色模式");
    button.setAttribute("aria-pressed", String(theme === "dark"));
    document.querySelector('meta[name="theme-color"]').content = theme === "dark" ? "#171e1a" : "#f7f6f2";
    if (save) {
      preference = theme;
      try { localStorage.setItem(themeKey, theme); } catch { /* Keep the current session theme. */ }
    }
  }

  apply(preference || (system.matches ? "dark" : "light"), false);
  button.addEventListener("click", () => apply(document.documentElement.dataset.theme === "dark" ? "light" : "dark", true));
  system.addEventListener("change", () => {
    if (!preference) apply(system.matches ? "dark" : "light", false);
  });
}

function renderReadingInfo(progress, chapter) {
  const info = element("dl", "book-reading-info");
  const lastRead = element("dd", "book-last-read", progress ? "时间未记录" : "尚未阅读");
  const date = new Date(typeof progress?.updatedAt === "number" && progress.updatedAt > 0 ? progress.updatedAt : NaN);
  if (Number.isFinite(date.getTime())) {
    const time = element("time", "", date.toLocaleString("zh-CN", {
      year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
    }));
    time.dateTime = date.toISOString();
    lastRead.replaceChildren(time);
  }
  const number = chapter && /^\d+$/.test(chapter.number) ? `第 ${chapter.number} 章` : chapter?.number || "";
  const lastChapter = element("dd", "book-last-chapter", !progress ? "尚未阅读" :
    chapter ? `${number} ${chapter.title}`.trim() : "章节已不可用");
  info.append(element("dt", "", "最近阅读时间"), lastRead, element("dt", "", "最近阅读章节"), lastChapter);
  return info;
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
      const progress = readProgress(book);
      const chapters = Array.isArray(book.chapters) ? book.chapters : [];
      const chapter = progress && (chapters.find((item) => item.id === (progress.chapter || book.legacyPageChapter)) ||
        (!progress.chapter ? chapters[0] : null));
      const read = element("a", "read-link", progress ? "继续阅读 →" : "开始阅读 →");
      read.href = bookUrl(book, chapter?.id);
      card.append(title, original, author, description, renderReadingInfo(progress, chapter), read);
      return card;
    }));
    document.querySelector("#empty-state").hidden = matches.length > 0;
  }

  search.addEventListener("input", draw);
  window.addEventListener("pageshow", draw);
  window.addEventListener("storage", (event) => {
    if (event.key === null || event.key.startsWith(progressPrefix)) draw();
  });
  draw();
}

function renderTable(block) {
  const wrapper = element("div", "table-scroll");
  const table = element("table", "book-table");
  if (block.notation === true) table.classList.add("notation-table");
  if (block.codeTable === true) table.classList.add("code-table");
  if (block.caption) {
    const caption = element("caption");
    caption.append(renderSegments(block.captionSegments, block.caption));
    table.append(caption);
  }
  if (Array.isArray(block.rows)) {
    function makeRow(cells, header) {
      const row = element("tr");
      for (const cell of cells) {
        const value = cell && typeof cell === "object" ? cell : { text: String(cell ?? "") };
        const td = element(header || value.header ? "th" : "td");
        td.append(renderSegments(value.segments, value.text || ""));
        if (Number.isSafeInteger(value.colspan) && value.colspan > 1) td.colSpan = value.colspan;
        if (Number.isSafeInteger(value.rowspan) && value.rowspan > 1) td.rowSpan = value.rowspan;
        row.append(td);
      }
      return row;
    }
    if (Array.isArray(block.headers)) {
      const head = element("thead");
      head.append(makeRow(block.headers, true));
      table.append(head);
    }
    const body = element("tbody");
    for (const cells of block.rows) if (Array.isArray(cells)) body.append(makeRow(cells, false));
    table.append(body);
  } else {
    (block.text || "").split("\n").filter((line) => line.startsWith("|")).forEach((line, index) => {
      if (index === 1) return;
      const row = element("tr");
      line.slice(1, -1).split("|").forEach((cell) => row.append(element(index === 0 ? "th" : "td", "", cell.trim())));
      table.append(row);
    });
  }
  wrapper.append(table);
  return wrapper;
}

const mathNamespace = "http://www.w3.org/1998/Math/MathML";
const mathTags = new Set([
  "math", "mrow", "mi", "mn", "mo", "mtext", "mspace", "mfrac", "msqrt", "mroot",
  "msup", "msub", "msubsup", "munder", "mover", "munderover", "mmultiscripts",
  "mprescripts", "none", "mfenced", "menclose", "mtable", "mtr", "mtd", "mstyle",
  "mpadded", "mphantom",
]);
const mathAttributes = new Set([
  "mathvariant", "stretchy", "fence", "separator", "accent", "accentunder", "largeop",
  "movablelimits", "linethickness", "lspace", "rspace", "minsize", "maxsize",
  "columnalign", "rowalign", "columnspacing", "rowspacing", "columnlines", "rowlines", "columnspan", "rowspan",
  "notation", "scriptlevel", "displaystyle",
]);

// Chromium retains mathvariant in MathML but can paint script and bold Latin
// identifiers with the same face as ordinary variables. Use their Unicode
// mathematical letters so a codebook 𝒞 and a capacity C remain distinct.
const scriptCapitals = [..."𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"];

function visibleMathVariant(variant, value) {
  if (typeof value !== "string" || value.length !== 1) return null;
  const point = value.charCodeAt(0);
  if (variant === "script" && point >= 65 && point <= 90) return scriptCapitals[point - 65];
  if (variant === "bold") {
    if (point >= 65 && point <= 90) return String.fromCodePoint(0x1d400 + point - 65);
    if (point >= 97 && point <= 122) return String.fromCodePoint(0x1d41a + point - 97);
  }
  return null;
}

function renderMathml(source, display) {
  if (typeof source !== "string" || !source.trim()) return null;
  const parsed = new DOMParser().parseFromString(source, "application/xml");
  const root = parsed.documentElement;
  if (root.localName !== "math" || parsed.querySelector("parsererror")) return null;

  function copy(node) {
    if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent);
    if (node.nodeType !== Node.ELEMENT_NODE || !mathTags.has(node.localName)) return null;
    const result = document.createElementNS(mathNamespace, node.localName);
    const variantGlyph = node.localName === "mi"
      ? visibleMathVariant(node.getAttribute("mathvariant"), node.textContent) : null;
    if (variantGlyph) {
      result.textContent = variantGlyph;
      return result;
    }
    for (const attribute of node.attributes) {
      if (mathAttributes.has(attribute.localName) && !attribute.name.includes(":")) {
        result.setAttribute(attribute.localName, attribute.value);
      }
      if (node.localName === "mspace" && attribute.name === "width" &&
          /^-?(?:\d+(?:\.\d*)?|\.\d+)(?:em|ex|px|pt|pc|cm|mm|in|%)$/.test(attribute.value)) {
        result.setAttribute("width", attribute.value);
      }
    }
    for (const child of node.childNodes) {
      const safe = copy(child);
      if (!safe) return null;
      result.append(safe);
    }
    return result;
  }

  const math = copy(root);
  if (math) math.setAttribute("display", display ? "block" : "inline");
  return math;
}

function renderSegments(segments, fallback) {
  const content = document.createDocumentFragment();
  if (!Array.isArray(segments)) {
    content.append(document.createTextNode(fallback || ""));
    return content;
  }
  for (const segment of segments) {
    if (typeof segment === "string") {
      content.append(document.createTextNode(segment));
    } else if (segment && typeof segment === "object") {
      if (segment.mathml) {
        const math = renderMathml(segment.mathml, false);
        if (math) {
          const wrapper = element("span", "inline-math");
          wrapper.append(math);
          content.append(wrapper);
        } else {
          content.append(document.createTextNode(segment.text || segment.tex || ""));
        }
      } else if (typeof segment.ref === "string" && /^[\w-]+$/.test(segment.ref)) {
        const link = element("a", "reading-reference", segment.text || segment.ref);
        link.href = `#read-${segment.ref}`;
        content.append(link);
      } else if (segment.code === true) {
        content.append(element("code", "book-inline-code", segment.text || ""));
      } else if (segment.nowrap === true) {
        content.append(element("span", "book-inline-nowrap", segment.text || ""));
      } else if (segment.break === true) {
        content.append(document.createElement("wbr"));
      } else if (segment.footnote === true && typeof segment.href === "string" &&
                 /^#read-fn-\d+-\d+$/.test(segment.href)) {
        const superscript = element("sup", "book-footnote-ref");
        const link = element("a", "reading-reference", segment.text || "");
        link.href = segment.href;
        superscript.append(link);
        content.append(superscript);
      } else if (typeof segment.href === "string" && /^https?:\/\//i.test(segment.href)) {
        const link = element("a", "reading-reference", segment.text || segment.href);
        link.href = segment.href;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        content.append(link);
      } else if (segment.em === true || segment.strong === true) {
        const emphasis = element(segment.strong === true ? "strong" : "em");
        if (Array.isArray(segment.segments)) emphasis.append(renderSegments(segment.segments, segment.text));
        else emphasis.textContent = segment.text || "";
        content.append(emphasis);
      } else {
        content.append(document.createTextNode(segment.text || ""));
      }
    }
  }
  return content;
}

function readerContentsHref(value) {
  return typeof value === "string" &&
    (/^#read-[\w-]+$/.test(value) || /^\?book=[\w-]+&chapter=[\w-]+(?:#read-[\w-]+)?$/.test(value))
    ? value : null;
}

function renderList(block) {
  if (block.originalContents === true) {
    const list = element("ul", "book-list original-contents");
    for (const item of Array.isArray(block.items) ? block.items : []) {
      const depth = Math.max(0, Math.min(2, Number(item.depth) || 0));
      const row = element("li", `contents-depth-${depth}`);
      const title = element(item.strong ? "strong" : "span", "contents-title");
      const href = readerContentsHref(item.href);
      if (href) {
        const link = element("a", "contents-reader-link", item.title || "");
        link.href = href;
        title.append(link);
      } else title.textContent = item.title || "";
      row.append(title, element("span", "contents-page", item.pageLabel || ""));
      list.append(row);
    }
    return list;
  }
  function makeList(items, ordered, start) {
    const list = element(ordered ? "ol" : "ul", "book-list");
    if (ordered && Number.isSafeInteger(start) && start > 0) list.start = start;
    for (const item of items) {
      const li = element("li");
      if (typeof item === "string") li.append(document.createTextNode(item));
      else if (item && typeof item === "object") {
        const href = readerContentsHref(item.href);
        const paragraph = element(href ? "a" : "span", href ? "contents-reader-link" : "");
        if (href) paragraph.href = href;
        paragraph.append(renderSegments(item.segments, item.text));
        li.append(paragraph);
        if (Array.isArray(item.children) && item.children.length) {
          li.append(makeList(item.children, item.ordered === true, item.start));
        }
      }
      list.append(li);
    }
    return list;
  }
  return makeList(Array.isArray(block.items) ? block.items : [], block.ordered === true, block.start);
}

function figureUrl(book, source) {
  if (typeof source !== "string" || !/^assets\/[\w./-]+\.(?:png|jpe?g|webp|gif|svg)$/i.test(source)) return null;
  if (source.split("/").includes("..")) return null;
  const root = new URL(`books/${book.id}/`, document.baseURI);
  const url = new URL(source, root);
  return url.origin === root.origin && url.pathname.startsWith(`${root.pathname}assets/`) ? url.href : null;
}

function renderFigure(block, book) {
  const figure = element("figure", "book-figure");
  if (block.wide) figure.classList.add("wide-figure");
  const source = figureUrl(book, block.src);
  if (source) {
    const image = element("img");
    image.src = source;
    image.alt = block.alt || "";
    image.loading = "lazy";
    image.decoding = "async";
    if (Number.isSafeInteger(block.width) && block.width > 0) image.width = block.width;
    if (Number.isSafeInteger(block.height) && block.height > 0) image.height = block.height;
    if (image.width > 0 && image.height > 0) {
      image.classList.add("has-image-size");
      image.style.setProperty("--figure-width", `${image.width}px`);
      image.style.setProperty("--figure-ratio", `${image.width} / ${image.height}`);
    }
    image.addEventListener("error", () => figure.append(element("p", "figure-error", "图片无法加载")), { once: true });
    const media = element("div", "figure-media");
    if (block.wide) {
      media.setAttribute("role", "region");
      media.setAttribute("aria-label", `可横向滚动的图：${block.alt || block.caption || "原书插图"}`);
      media.tabIndex = 0;
    }
    const link = element("a", "figure-image-link");
    link.href = source;
    link.target = "_blank";
    link.rel = "noopener";
    link.setAttribute("aria-label", `打开原图：${block.alt || block.caption || "原书插图"}`);
    link.append(image);
    media.append(link);
    figure.append(media);
    if (block.wide) figure.append(element("p", "figure-view-hint", "左右滑动查看图 · 点击图片查看原图"));
  } else {
    figure.append(element("p", "figure-error", "图片路径无效"));
  }
  if (block.caption || (Array.isArray(block.annotations) && block.annotations.length)) {
    const caption = element("figcaption", "figure-caption");
    if (block.caption) {
      const paragraph = element("p");
      paragraph.append(renderSegments(block.captionSegments, block.caption));
      caption.append(paragraph);
    }
    if (Array.isArray(block.annotations) && block.annotations.length) {
      const notes = element("div", "figure-annotations");
      notes.append(element("p", "figure-annotations-title", "图内文字译注"));
      const list = element("ul");
      block.annotations.forEach((annotation, index) => {
        const item = element("li");
        item.append(renderSegments(block.annotationSegments?.[index], annotation));
        list.append(item);
      });
      notes.append(list);
      caption.append(notes);
    }
    figure.append(caption);
  }
  return figure;
}

function renderLabeledParagraph(block, className, book) {
  const paragraph = element("p", className);
  const iconSource = figureUrl(book, block.recommendedIcon);
  if (iconSource) {
    const icon = element("img", `${className}-icon`);
    icon.src = iconSource;
    icon.alt = "原书推荐习题图标";
    icon.width = 42;
    icon.height = 46;
    paragraph.append(icon);
  }
  if (block.label) paragraph.append(element("strong", `${className}-label`, block.label));
  const body = element("span", `${className}-body`);
  body.append(renderSegments(block.segments, block.text));
  paragraph.append(body);
  return paragraph;
}

function renderBlock(block, book) {
  if (block.kind === "box" && Array.isArray(block.blocks)) {
    const aside = element("aside", "book-box");
    if (block.outlined === true) aside.classList.add("outlined-box");
    if (block.algorithm === true) aside.classList.add("algorithm-box");
    aside.id = `read-${block.id}`;
    for (const child of block.blocks) aside.append(renderBlock(child, book));
    if (block.algorithm === true) aside.append(element("p", "algorithm-view-hint", "左右滑动查看完整算法"));
    return aside;
  }
  const node = element("div", `reading-block reading-${block.kind}`);
  node.id = `read-${block.id}`;
  if (Number.isFinite(block.pdfPage)) node.dataset.pdfPage = block.pdfPage;
  if (block.kind === "table") {
    node.append(renderTable(block));
  } else if (block.kind === "heading") {
    if (typeof block.html === "string") {
      const fragment = document.createElement("template");
      fragment.innerHTML = block.html;
      node.append(fragment.content);
    } else {
      const number = block.text.match(/^(\d+(?:\.\d+)*)(?:\s|$)/)?.[1];
      const depth = Number.isInteger(block.level) ? block.level :
        (number ? number.split(".").length : (/^第\s*\d+\s*章/.test(block.text) ? 1 : 3));
      const heading = element(`h${Math.max(1, Math.min(depth, 3))}`);
      const href = readerContentsHref(block.href);
      if (href) {
        const link = element("a", "contents-reader-link");
        link.href = href;
        link.append(renderSegments(block.segments, block.text));
        heading.append(link);
      } else {
        heading.append(renderSegments(block.segments, block.text));
      }
      node.append(heading);
    }
  } else if (block.kind === "figure" || block.kind === "image") {
    node.append(renderFigure(block, book));
  } else if (block.kind === "formula") {
    const formula = element("div", "book-formula");
    const scroller = element("div", "formula-scroll");
    const math = block.mathml ? renderMathml(block.mathml, true) : null;
    scroller.append(math || element("span", "formula-fallback", block.text || block.tex || "公式无法显示"));
    formula.append(scroller);
    if (block.number) formula.append(element("span", "formula-number", block.number));
    if (block.text) formula.setAttribute("aria-label", block.text);
    node.append(formula);
  } else if (block.kind === "code") {
    const pre = element("pre", "book-code");
    const code = element("code", "", block.text || "");
    if (block.language) code.dataset.language = block.language;
    pre.append(code);
    node.append(pre);
  } else if (block.kind === "list") {
    node.append(renderList(block));
  } else if (block.kind === "footnote") {
    const note = element("p", "book-footnote");
    if (block.label) note.append(element("span", "footnote-label", block.label));
    note.append(renderSegments(block.segments, block.text));
    node.append(note);
  } else if (block.kind === "quote") {
    const quote = element("blockquote", "book-quote");
    const paragraph = element("p");
    paragraph.append(renderSegments(block.segments, block.text));
    quote.append(paragraph);
    node.append(quote);
  } else if (block.kind === "exercise") {
    node.append(renderLabeledParagraph(block, "book-exercise", book));
  } else if (block.kind === "bibliographical-note") {
    node.append(renderLabeledParagraph(block, "book-bibliographical-note", book));
  } else if (block.kind === "rich" && typeof block.html === "string") {
    const fragment = document.createElement("template");
    fragment.innerHTML = block.html;
    node.append(fragment.content);
  } else {
    const paragraph = element("p");
    paragraph.append(renderSegments(block.segments, block.text));
    node.append(paragraph);
  }
  return node;
}

async function loadReferenceIndex(book) {
  if (!book.referenceIndex) return null;
  try {
    const response = await fetch(new URL(book.referenceIndex, document.baseURI));
    if (!response.ok) return null;
    const index = await response.json();
    return index.bookId === book.id && index.targets ? index.targets : null;
  } catch { return null; }
}

function referenceMatches(text, targets, book, currentChapter, selfBlock) {
  const matches = [];
  const chapters = new Set(book.chapters.map((chapter) => chapter.id));
  const number = "(?:[A-E]|\\d+)\\.\\d+(?:\\.\\d+)?";
  const joined = `(?:\\s*(?:、|,|，|和|及|与|-|–|—|至|到)\\s*${number})+`;

  function add(kind, key, start, end) {
    const target = targets[kind]?.[key];
    if (!target || !chapters.has(target.chapter) || !/^[\w-]+$/.test(target.block) ||
        (target.element && !/^[\w-]+$/.test(target.element))) return;
    if (target.chapter === currentChapter && target.block === selfBlock) return;
    const fragment = target.element || `read-${target.block}`;
    const href = target.chapter === currentChapter ? `#${fragment}` :
      `${bookUrl(book, target.chapter)}#${fragment}`;
    matches.push({ start, end, href, kind, number: key, chapter: target.chapter, block: target.block,
      element: target.element, blockKind: target.blockKind, previewable: target.preview !== false });
  }

  function singles(kind, pattern) {
    for (const match of text.matchAll(pattern)) add(kind, match[1], match.index, match.index + match[0].length);
  }

  function groups(kind, pattern, numberPattern) {
    for (const match of text.matchAll(pattern)) {
      const offset = match.index + match[0].indexOf(match[1]);
      for (const value of match[1].matchAll(numberPattern)) {
        add(kind, value[0], offset + value.index, offset + value.index + value[0].length);
      }
    }
  }

  singles("chapter", /第\s*(\d+)\s*章/g);
  singles("part", /第\s*([一二三四五六七])\s*部分/g);
  singles("chapter", /附录\s*([A-E])(?![A-Za-z0-9])/g);
  singles("section", /(?:第\s*)?((?:[A-E]|\d+)(?:\.\d+){1,2})\s*(?:小)?节/g);
  singles("section", /附录\s*([A-E]\.\d+(?:\.\d+)?)\s*节?/g);
  if (book.richReferenceAuto === true) singles("section", /第\s*(\d+)\s*节(?![\d.])/g);
  singles("figure", /图\s*((?:[A-E]|\d+)\.\d+)(?![\d.])/g);
  if (book.richReferenceAuto === true) singles("figure", /图\s*(\d+)(?![\d.])/g);
  singles("table", /表\s*((?:[A-E]|\d+)\.\d+)(?![\d.])/g);
  if (book.richReferenceAuto === true) singles("table", /表\s*([IVX]+)(?![A-Za-z])/g);
  singles("algorithm", /算法\s*((?:[A-E]|\d+)\.\d+)(?![\d.])/g);
  singles("exercise", /习题\s*((?:[A-E]|\d+)\.\d+)(?![\d.])/g);
  singles("example", /(?:示例|例)\s*((?:[A-E]|\d+)\.\d+)(?![\d.])/g);
  singles("formula", /(?:公式|式)\s*[（(]\s*((?:[A-E]|\d+)\.\d+)\s*[）)]/g);
  singles("formula", /[（(]\s*((?:[A-E]|\d+)\.\d+)\s*[）)]/g);
  groups("chapter", /第\s*(\d+(?:\s*(?:、|,|，|和|及|与|-|–|—|至|到)\s*\d+)+)\s*章/g, /\d+/g);
  groups("section", new RegExp(`(?:第\\s*)?(${number}${joined})\\s*(?:小)?节`, "g"), new RegExp(number, "g"));
  groups("figure", new RegExp(`图\\s*(${number}${joined})`, "g"), new RegExp(number, "g"));
  groups("table", new RegExp(`表\\s*(${number}${joined})`, "g"), new RegExp(number, "g"));
  matches.sort((left, right) => left.start - right.start || right.end - left.end);
  const selected = [];
  for (const match of matches) {
    if (!selected.length || match.start >= selected[selected.length - 1].end) selected.push(match);
  }
  return selected;
}

function linkReferences(article, book, currentChapter, targets) {
  let linked = 0;
  const selector = ".reading-paragraph, .reading-list, .reading-footnote, .reading-quote, .reading-exercise, .reading-bibliographical-note, .reading-figure .figure-caption, .reading-table .book-table, .reading-heading" +
    (book.richReferenceAuto === true ? ", .reading-rich" : "");
  const containers = article.querySelectorAll(selector);
  for (const container of containers) {
    const selfBlock = container.closest(".reading-block")?.id.slice(5);
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      if (node.parentElement?.closest("a, code, pre, math, .reading-intro") ||
          (container.classList.contains("reading-rich") && node.parentElement?.closest("figure, .book-formula, .footnote"))) continue;
      const matches = referenceMatches(node.textContent, targets, book, currentChapter, selfBlock);
      if (!matches.length) continue;
      const fragment = document.createDocumentFragment();
      let offset = 0;
      for (const match of matches) {
        if (match.start < offset) continue;
        fragment.append(document.createTextNode(node.textContent.slice(offset, match.start)));
        const link = element("a", "reading-reference", node.textContent.slice(match.start, match.end));
        link.href = match.href;
        if (book.referencePreview === true && match.previewable &&
            ["figure", "formula", "table", "chapter", "section"].includes(match.kind)) {
          link.dataset.previewKind = match.kind;
          link.dataset.previewNumber = match.number;
          link.dataset.previewChapter = match.chapter;
          link.dataset.previewBlock = match.block;
          if (match.element) link.dataset.previewElement = match.element;
          if (match.blockKind) link.dataset.previewBlockKind = match.blockKind;
          link.setAttribute("aria-haspopup", "dialog");
        }
        fragment.append(link);
        linked += 1;
        offset = match.end;
      }
      fragment.append(document.createTextNode(node.textContent.slice(offset)));
      node.replaceWith(fragment);
    }
  }
  if (book.referencePreview === true) {
    for (const link of article.querySelectorAll("a.reading-reference[data-convex-reference]")) {
      const kind = link.dataset.convexReference;
      if (!["figure", "formula", "table", "chapter", "section"].includes(kind)) continue;
      const value = link.textContent;
      const number = kind === "chapter" ?
        (value.match(/第\s*(\d+)\s*章/)?.[1] || value.match(/附录\s*([A-C])/)?.[1] ||
         value.match(/^\s*([A-C]|\d+)(?=\s)/)?.[1]) :
        value.match(/(?:[A-C]|\d+)\.\d+(?:\.\d+)?/)?.[0];
      const target = targets[kind]?.[number];
      if (!target || target.preview === false || (target.element && !/^[\w-]+$/.test(target.element)) ||
          !/^[\w-]+$/.test(target.block) ||
          !book.chapters.some((chapter) => chapter.id === target.chapter)) continue;
      const fragment = target.element || `read-${target.block}`;
      link.href = target.chapter === currentChapter ? `#${fragment}` :
        `${bookUrl(book, target.chapter)}#${fragment}`;
      link.dataset.previewKind = kind;
      link.dataset.previewNumber = number;
      link.dataset.previewChapter = target.chapter;
      link.dataset.previewBlock = target.block;
      if (target.element) link.dataset.previewElement = target.element;
      if (target.blockKind) link.dataset.previewBlockKind = target.blockKind;
      link.setAttribute("aria-haspopup", "dialog");
      linked += 1;
    }
  }
  article.dataset.referenceLinks = String(linked);
}

function setupOfflineImages(book) {
  if (!book.offlineImages || !("serviceWorker" in navigator)) return;
  const panel = document.querySelector("#offline-panel");
  const status = document.querySelector("#offline-status");
  const retry = document.querySelector("#offline-retry");
  panel.hidden = false;
  let runId = 0;
  let activePort = null;
  let timer = null;

  async function prepare() {
    const currentRun = ++runId;
    if (activePort) activePort.close();
    activePort = null;
    clearTimeout(timer);
    panel.hidden = false;
    panel.dataset.state = "checking";
    status.textContent = "正在检查离线图片…";
    retry.hidden = true;
    try {
      let registration = await navigator.serviceWorker.getRegistration();
      if (!registration) registration = await navigator.serviceWorker.register("./sw.js", { updateViaCache: "none" });
      if (!registration.active) status.textContent = "正在下载离线阅读内容，请保持联网…";
      const ready = registration.active ? registration : await Promise.race([
        navigator.serviceWorker.ready,
        new Promise((_, reject) => setTimeout(() => reject(new Error("Service Worker timeout")), 300000)),
      ]);
      if (currentRun !== runId) return;
      const worker = ready.active || navigator.serviceWorker.controller;
      if (!worker) throw new Error("Service Worker unavailable");
      const channel = new MessageChannel();
      activePort = channel.port1;
      const timeOut = () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
          if (currentRun !== runId) return;
          panel.dataset.state = "error";
          status.textContent = "离线图片准备未响应，请重试。";
          retry.hidden = false;
          channel.port1.close();
          activePort = null;
        }, 30000);
      };
      channel.port1.onmessage = ({ data }) => {
        if (currentRun !== runId || data?.type !== "offline-images-status") return;
        clearTimeout(timer);
        panel.dataset.state = data.state;
        const size = data.totalBytes ? `，约 ${Math.ceil(data.totalBytes / 1048576)} MB` : "";
        if (data.state === "complete") {
          status.textContent = "";
          panel.hidden = true;
          channel.port1.close();
          activePort = null;
        } else if (data.state === "error") {
          status.textContent = `离线图片已准备 ${data.done}/${data.total} 张；联网后可重试。`;
          retry.hidden = false;
          channel.port1.close();
          activePort = null;
        } else {
          status.textContent = `正在准备离线图片 ${data.done}/${data.total}${size}`;
          timeOut();
        }
      };
      worker.postMessage({ type: "prepare-offline-images", path: book.offlineImages }, [channel.port2]);
      timeOut();
    } catch {
      if (currentRun !== runId) return;
      panel.dataset.state = "error";
      status.textContent = "离线图片准备失败，请重试。";
      retry.hidden = false;
    }
  }

  retry.addEventListener("click", prepare);
  window.addEventListener("online", prepare);
  navigator.serviceWorker.addEventListener("controllerchange", prepare);
  void prepare();
}

async function renderReader(book) {
  document.querySelector("#landing-view").hidden = true;
  document.querySelector("#reader-view").hidden = false;
  document.querySelector("#reader-book-title").textContent = book.title;
  document.title = `${book.title} · 算经阁`;

  const chapters = Array.isArray(book.chapters) ? book.chapters : [];
  const saved = readProgress(book);
  const explicit = chapters.find((item) => item.id === params.get("chapter"));
  const legacyChapter = chapters.find((item) => item.id === book.legacyPageChapter) || chapters[0];
  const chapterInfo = explicit || (params.has("page") ? legacyChapter : chapters.find((item) => item.id === saved?.chapter)) || chapters[0];
  const referenceIndexPromise = loadReferenceIndex(book);
  let chapter;
  try {
    if (!chapterInfo) throw new Error("No chapters");
    const response = await fetch(new URL(chapterInfo.content, document.baseURI));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    chapter = await response.json();
    if (!Array.isArray(chapter.blocks) || !chapter.blocks.length || !Array.isArray(chapter.toc) || !chapter.toc.length) throw new Error("Empty chapter");
  } catch {
    const status = document.querySelector("#reader-status");
    status.textContent = "内容暂时无法加载，请检查网络后刷新。";
    status.hidden = false;
    return;
  }

  const blocks = chapter.blocks;
  const article = document.querySelector("#reader-article");
  article.dataset.bookId = book.id;
  article.replaceChildren(...blocks.map((block) => renderBlock(block, book)));
  const referenceIndex = await referenceIndexPromise;
  if (referenceIndex) linkReferences(article, book, chapterInfo.id, referenceIndex);
  function rememberReferenceReturn(link) {
    const destination = new URL(link.href, location.href);
    const source = link.closest(".reading-block");
    if (!source || destination.origin !== location.origin || destination.pathname !== location.pathname ||
        destination.searchParams.get("book") !== book.id ||
        destination.searchParams.get("chapter") === chapterInfo.id) return;
    try {
      history.replaceState({ ...history.state, readerReturn: {
        book: book.id, chapter: chapterInfo.id, block: source.id, url: location.href,
      } }, "");
    } catch { /* Navigation remains available if history state is unavailable. */ }
  }
  if (book.referencePreview === true && referenceIndex) {
    createReferencePreview({ article, book, chapterInfo, chapter, renderBlock, rememberReferenceReturn });
  }
  setupOfflineImages(book);
  const nodes = [...article.querySelectorAll(".reading-block")];
  const updateFormulaHints = () => {
    for (const formula of article.querySelectorAll(".book-formula")) {
      const scroller = formula.querySelector(".formula-scroll") || formula;
      const overflows = scroller.scrollWidth > scroller.clientWidth + 2;
      let hint = formula.nextElementSibling;
      if (overflows && !hint?.classList.contains("formula-view-hint")) {
        hint = element("p", "formula-view-hint", "左右滑动查看完整公式");
        formula.after(hint);
      }
      if (hint?.classList.contains("formula-view-hint")) hint.hidden = !overflows;
      if (overflows) {
        scroller.tabIndex = 0;
        scroller.title = "左右滑动查看完整公式";
      }
    }
    for (const inlineMath of article.querySelectorAll(".inline-math")) {
      const overflows = inlineMath.scrollWidth > inlineMath.clientWidth + 2;
      let hint = inlineMath.nextElementSibling;
      if (overflows && !hint?.classList.contains("inline-math-view-hint")) {
        hint = element("span", "inline-math-view-hint", "（左右滑动查看完整公式）");
        inlineMath.after(hint);
      }
      if (hint?.classList.contains("inline-math-view-hint")) hint.hidden = !overflows;
      if (overflows) {
        inlineMath.tabIndex = 0;
        inlineMath.title = "左右滑动查看完整公式";
      }
    }
    for (const code of article.querySelectorAll(".book-code")) {
      const overflows = code.scrollWidth > code.clientWidth + 2;
      let hint = code.nextElementSibling;
      if (overflows && !hint?.classList.contains("code-view-hint")) {
        hint = element("p", "code-view-hint", "左右滑动查看完整代码或算法");
        code.after(hint);
      }
      if (hint?.classList.contains("code-view-hint")) hint.hidden = !overflows;
      if (overflows) {
        code.tabIndex = 0;
        code.title = "左右滑动查看完整代码或算法";
      }
    }
  };
  const indexById = new Map(nodes.map((node, index) => [node.id, index]));
  const toc = document.querySelector("#reader-toc");
  const mobileToc = document.querySelector("#reader-toc-mobile");
  const menu = document.querySelector("#reader-menu");
  const dialog = document.querySelector("#toc-dialog");
  const tocToggle = document.querySelector("#toc-toggle");
  const desktop = matchMedia("(min-width: 800px)");
  const setMenuForWidth = () => { menu.open = desktop.matches; };
  setMenuForWidth();
  desktop.addEventListener("change", setMenuForWidth);

  function drawToc(container, closeOnSelect) {
    const links = [];
    for (const item of chapters) {
      const currentChapter = item.id === chapterInfo.id;
      const chapterLink = element("a", `toc-link toc-chapter-link${currentChapter ? " chapter-current" : ""}`, `${item.number} ${item.title}`);
      chapterLink.href = currentChapter ? `#read-${chapter.toc[0].block}` : bookUrl(book, item.id);
      if (currentChapter) chapterLink.setAttribute("aria-current", "page");
      if (closeOnSelect) chapterLink.addEventListener("click", () => dialog.close());
      links.push(chapterLink);
      if (currentChapter) {
        for (const entry of chapter.toc.slice(1)) {
          const level = Number.isInteger(entry.level) ? entry.level : Math.min(entry.number.split(".").length, 3);
          const link = element("a", `toc-link toc-section-link toc-level-${level}`, `${entry.number} ${entry.title}`.trim());
          if (entry.segments) link.replaceChildren(renderSegments(entry.segments, `${entry.number} ${entry.title}`.trim()));
          link.href = `#read-${entry.block}`;
          if (closeOnSelect) link.addEventListener("click", () => dialog.close());
          links.push(link);
        }
      }
    }
    container.replaceChildren(...links);
  }
  drawToc(toc, false);
  drawToc(mobileToc, true);
  tocToggle.addEventListener("click", () => { dialog.showModal(); tocToggle.setAttribute("aria-expanded", "true"); });
  document.querySelector("#toc-close").addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => tocToggle.setAttribute("aria-expanded", "false"));
  dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });

  const chapterNavigation = document.querySelector("#chapter-navigation");
  const chapterIndex = chapters.indexOf(chapterInfo);
  const adjacent = [chapters[chapterIndex - 1], chapters[chapterIndex + 1]];
  chapterNavigation.replaceChildren(...adjacent.filter(Boolean).map((item) => {
    const link = element("a", "chapter-navigation-link", `${item === adjacent[0] ? "← 上一章" : "下一章 →"} · ${item.number} ${item.title}`);
    link.href = bookUrl(book, item.id);
    return link;
  }));
  chapterNavigation.hidden = !chapterNavigation.childElementCount;

  let lastSaved = "";
  let historyReturnScrollY = null;
  let restoreScrollY = null;
  function updatePosition() {
    let current = 0;
    const threshold = (Number.parseFloat(getComputedStyle(nodes[0]).scrollMarginTop) || 0) + 1;
    for (let index = 0; index < nodes.length; index += 1) {
      if (nodes[index].getBoundingClientRect().top <= threshold) current = index;
      else break;
    }
    const restoredNode = restoreId && document.getElementById(restoreId);
    const stillAtRestoredBlock = restoredNode && indexById.has(restoreId) &&
      restoreId !== nodes[nodes.length - 1].id &&
      restoreScrollY !== null && Math.abs(window.scrollY - restoreScrollY) <= 2 &&
      Math.abs(restoredNode.getBoundingClientRect().top - threshold) <= 24;
    if (stillAtRestoredBlock) current = indexById.get(restoreId);
    const bottomGap = document.documentElement.scrollHeight - window.scrollY - window.innerHeight;
    const lastBlockVisible = nodes[nodes.length - 1].getBoundingClientRect().top < window.innerHeight;
    if (!stillAtRestoredBlock && bottomGap <= 64 && lastBlockVisible) {
      current = nodes.length - 1;
    }
    const blockId = nodes[current].id;
    if (blockId !== lastSaved) {
      saveProgress(book, chapterInfo.id, blockId, nodes[current].dataset.pdfPage);
      const entry = history.state;
      if (entry?.readerReturn?.url === location.href) {
        if (historyReturnScrollY !== null && Math.abs(window.scrollY - historyReturnScrollY) > 2) {
          try {
            history.replaceState({ ...entry, readerReturn: { ...entry.readerReturn, block: blockId } }, "");
          } catch { /* Keep reading when history state is unavailable. */ }
        }
        historyReturnScrollY = window.scrollY;
      }
      lastSaved = blockId;
    }
    document.querySelector("#reading-progress").style.width = `${((current + 1) / nodes.length) * 100}%`;
    const currentToc = [...chapter.toc].reverse().find((entry) => (indexById.get(`read-${entry.block}`) ?? 0) <= current);
    for (const link of document.querySelectorAll(".toc-section-link")) {
      const selected = link.hash === `#read-${currentToc?.block}`;
      link.classList.toggle("active", selected);
      if (selected) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }

  // Keep the source paragraph in this history entry: another chapter can
  // replace the book-wide reading progress before the reader presses Back.
  article.addEventListener("click", (event) => {
    const link = event.target.closest?.("a.reading-reference");
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey ||
        event.ctrlKey || event.shiftKey || event.altKey || link.target === "_blank") return;
    rememberReferenceReturn(link);
  });
  const navigationType = performance.getEntriesByType("navigation")[0]?.type;
  const historyReturn = history.state?.readerReturn;
  const returnId = (navigationType === "back_forward" || navigationType === "reload") &&
    historyReturn?.url === location.href && historyReturn.book === book.id && historyReturn.chapter === chapterInfo.id &&
    indexById.has(historyReturn.block) ? historyReturn.block : null;

  const legacyPage = Number(params.get("page"));
  const legacyBlock = blocks.find((block) => block.page === legacyPage)?.id;
  const requested = decodeURIComponent(location.hash.slice(1));
  const requestedNode = requested && document.getElementById(requested);
  const canRestore = saved && (!params.has("chapter") || saved.chapter === chapterInfo.id || (!saved.chapter && chapterInfo.id === legacyChapter?.id));
  const restoreId = returnId || (requestedNode && article.contains(requestedNode) ? requested :
    legacyBlock ? `read-${legacyBlock}` :
    canRestore && indexById.has(saved.block) ? saved.block :
    canRestore && saved.page ? `read-${blocks.find((block) => block.page === saved.page)?.id}` : null);
  const initialScrollY = window.scrollY;
  let movedBeforeTracking = false;
  const observePreTrackingScroll = () => {
    if (Math.abs(window.scrollY - initialScrollY) > 2) movedBeforeTracking = true;
  };
  window.addEventListener("scroll", observePreTrackingScroll, { passive: true });
  const startTracking = () => {
    const preserveEarlyScroll = movedBeforeTracking || Math.abs(window.scrollY - initialScrollY) > 2;
    window.removeEventListener("scroll", observePreTrackingScroll);
    updateFormulaHints();
    const bottomGap = document.documentElement.scrollHeight - window.scrollY - window.innerHeight;
    const restoreLastAtBottom = restoreId === nodes[nodes.length - 1].id && bottomGap <= 64;
    if (!preserveEarlyScroll || restoreLastAtBottom) {
      if (restoreId === nodes[nodes.length - 1].id) {
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "instant" });
      } else if (restoreId) {
        document.getElementById(restoreId)?.scrollIntoView({ block: "start", behavior: "instant" });
      } else {
        window.scrollTo({ top: 0, behavior: "instant" });
      }
    }
    restoreScrollY = (!preserveEarlyScroll || restoreLastAtBottom) && restoreId ? window.scrollY : null;
    updatePosition();
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { ticking = false; updatePosition(); });
    }, { passive: true });
    window.addEventListener("resize", () => requestAnimationFrame(updateFormulaHints), { passive: true });
  };
  document.fonts.ready.then(() => requestAnimationFrame(startTracking));
}

async function setupPwa() {
  if (!("serviceWorker" in navigator)) return;
  let previousController = navigator.serviceWorker.controller;
  let refreshing = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    const hadController = Boolean(previousController);
    previousController = navigator.serviceWorker.controller;
    if (hadController && !refreshing) {
      refreshing = true;
      location.reload();
    }
  });
  try {
    const registration = await navigator.serviceWorker.register("./sw.js", { updateViaCache: "none" });
    let checking = false;
    let lastCheck = 0;
    async function checkForUpdate() {
      if (checking || document.hidden || !navigator.onLine || Date.now() - lastCheck < 15 * 1000) return;
      checking = true;
      lastCheck = Date.now();
      try { await registration.update(); }
      catch { /* Try again when the reader returns to the foreground. */ }
      finally { checking = false; }
    }
    void checkForUpdate();
    setInterval(checkForUpdate, 5 * 60 * 1000);
    document.addEventListener("visibilitychange", checkForUpdate);
    window.addEventListener("pageshow", checkForUpdate);
    window.addEventListener("focus", checkForUpdate);
    window.addEventListener("online", checkForUpdate);
  } catch { /* Reading remains available without offline support. */ }
}

setupTheme();
if (activeBook) renderReader(activeBook);
else renderShelf();
setupPwa();
