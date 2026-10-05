// A book opts in with referencePreview: true and a reference index. The reader
// supplies its existing block renderer so previews use the same content as the page.
function createReferencePreview({ article, book, chapterInfo, chapter, renderBlock, rememberReferenceReturn }) {
  const chapters = new Map(book.chapters.map((item) => [item.id, item]));
  const chapterCache = new Map([[chapterInfo.id, Promise.resolve(chapter)]]);
  const tooltip = document.createElement("div");
  tooltip.className = "reference-preview-tooltip";
  tooltip.id = "reference-preview-tooltip";
  tooltip.setAttribute("role", "tooltip");
  tooltip.hidden = true;
  const tooltipTitle = document.createElement("strong");
  tooltipTitle.className = "reference-preview-title";
  const tooltipBody = document.createElement("div");
  tooltipBody.className = "reference-preview-tooltip-body";
  const tooltipHint = document.createElement("p");
  tooltipHint.className = "reference-preview-hint";
  tooltipHint.textContent = "点击引用查看完整内容";
  tooltip.append(tooltipTitle, tooltipBody, tooltipHint);

  const dialog = document.createElement("dialog");
  dialog.className = "reference-preview-dialog";
  dialog.setAttribute("aria-labelledby", "reference-preview-dialog-title");
  const header = document.createElement("div");
  header.className = "reference-preview-header";
  const heading = document.createElement("h2");
  heading.id = "reference-preview-dialog-title";
  const close = document.createElement("button");
  close.type = "button";
  close.className = "text-button";
  close.textContent = "关闭";
  header.append(heading, close);
  const body = document.createElement("div");
  body.className = "reference-preview-body";
  const footer = document.createElement("div");
  footer.className = "reference-preview-footer";
  const jump = document.createElement("a");
  jump.className = "reference-preview-jump";
  jump.textContent = "跳转到原文 →";
  footer.append(jump);
  dialog.append(header, body, footer);
  article.append(tooltip, dialog);

  function referenceLink(target) {
    const link = target instanceof Element ? target.closest("a.reading-reference[data-preview-kind]") : null;
    return link && article.contains(link) && !dialog.contains(link) ? link : null;
  }

  function label(link) {
    const number = link.dataset.previewNumber;
    return link.dataset.previewKind === "figure" ? `图 ${number}` : `式 (${number})`;
  }

  function loadChapter(id) {
    let pending = chapterCache.get(id);
    if (pending) return pending;
    const entry = chapters.get(id);
    if (!entry) return Promise.reject(new Error("Unknown chapter"));
    pending = fetch(new URL(entry.content, document.baseURI)).then(async (response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (data.bookId !== book.id || !Array.isArray(data.blocks)) throw new Error("Invalid chapter");
      return data;
    });
    chapterCache.set(id, pending);
    void pending.catch(() => {
      if (chapterCache.get(id) === pending) chapterCache.delete(id);
    });
    return pending;
  }

  async function loadTarget(link) {
    const { previewChapter: chapterId, previewBlock: blockId, previewKind: kind } = link.dataset;
    if (!chapters.has(chapterId) || !/^[\w-]+$/.test(blockId || "") || !["figure", "formula"].includes(kind)) {
      throw new Error("Invalid reference");
    }
    const data = await loadChapter(chapterId);
    const block = data.blocks.find((item) => item.id === blockId);
    if (!block || block.kind !== kind) throw new Error("Reference target unavailable");
    return block;
  }

  function fill(container, block) {
    const rendered = renderBlock(block, book);
    rendered.removeAttribute("id");
    rendered.removeAttribute("data-pdf-page");
    rendered.classList.add("reference-preview-content");
    for (const image of rendered.querySelectorAll("img")) image.loading = "eager";
    container.replaceChildren(rendered);
  }

  function positionTooltip(link) {
    if (tooltip.hidden) return;
    const anchor = link.getBoundingClientRect();
    const box = tooltip.getBoundingClientRect();
    const gap = 10;
    const left = Math.max(12, Math.min(anchor.left, innerWidth - box.width - 12));
    const below = anchor.bottom + gap;
    const above = anchor.top - box.height - gap;
    const top = below + box.height <= innerHeight - 12 || above < 12 ?
      Math.min(below, innerHeight - box.height - 12) : above;
    tooltip.style.left = `${left}px`;
    tooltip.style.top = `${Math.max(12, top)}px`;
  }

  let hoverTimer = null;
  let hoverLink = null;
  let hoverVersion = 0;
  function hideTooltip() {
    clearTimeout(hoverTimer);
    hoverTimer = null;
    hoverLink = null;
    hoverVersion += 1;
    tooltip.hidden = true;
  }

  article.addEventListener("pointerover", (event) => {
    if (event.pointerType !== "mouse" || !matchMedia("(hover: hover)").matches || dialog.open) return;
    const link = referenceLink(event.target);
    if (!link || (event.relatedTarget instanceof Node && link.contains(event.relatedTarget)) || hoverLink === link) return;
    hideTooltip();
    hoverLink = link;
    const version = hoverVersion;
    hoverTimer = setTimeout(async () => {
      tooltipTitle.textContent = label(link);
      tooltipBody.textContent = "正在加载预览…";
      tooltip.hidden = false;
      positionTooltip(link);
      try {
        const block = await loadTarget(link);
        if (version !== hoverVersion || dialog.open) return;
        fill(tooltipBody, block);
      } catch {
        if (version !== hoverVersion || dialog.open) return;
        tooltipBody.textContent = "预览暂时无法加载，可点击引用后跳转原文。";
      }
      positionTooltip(link);
      tooltipBody.querySelector("img")?.addEventListener("load", () => positionTooltip(link), { once: true });
    }, 250);
  });
  article.addEventListener("pointerout", (event) => {
    const link = referenceLink(event.target);
    if (!link || link !== hoverLink ||
        (event.relatedTarget instanceof Node && link.contains(event.relatedTarget))) return;
    hideTooltip();
  });
  window.addEventListener("scroll", () => {
    if (!hoverLink) return;
    const bounds = hoverLink.getBoundingClientRect();
    if (bounds.bottom < 0 || bounds.top > innerHeight) hideTooltip();
    else positionTooltip(hoverLink);
  }, { passive: true });
  window.addEventListener("resize", hideTooltip, { passive: true });

  let trigger = null;
  let dialogVersion = 0;
  let openingScrollY = 0;
  let jumping = false;
  article.addEventListener("click", async (event) => {
    const link = referenceLink(event.target);
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey ||
        event.ctrlKey || event.shiftKey || event.altKey || link.target === "_blank") return;
    event.preventDefault();
    hideTooltip();
    trigger = link;
    jumping = false;
    openingScrollY = window.scrollY;
    heading.textContent = label(link);
    jump.href = link.href;
    body.textContent = "正在加载预览…";
    dialog.showModal();
    document.documentElement.classList.add("reference-preview-open");
    const version = ++dialogVersion;
    try {
      const block = await loadTarget(link);
      if (version === dialogVersion && dialog.open) fill(body, block);
    } catch {
      if (version === dialogVersion && dialog.open) {
        body.textContent = "预览暂时无法加载，可跳转到原文查看。";
      }
    }
  });
  close.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener("close", () => {
    dialogVersion += 1;
    document.documentElement.classList.remove("reference-preview-open");
    if (trigger?.isConnected) trigger.focus({ preventScroll: true });
    if (!jumping && Math.abs(window.scrollY - openingScrollY) > 2) {
      window.scrollTo({ top: openingScrollY, behavior: "instant" });
    }
    trigger = null;
  });
  jump.addEventListener("click", (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (trigger) rememberReferenceReturn(trigger);
    jumping = true;
    dialog.close();
  });
}
