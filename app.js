const categories = [
  { value: "all", label: "全部学科" },
  { value: "Machine Learning", label: "机器学习" },
  { value: "Artificial Intelligence", label: "人工智能" },
  { value: "Mathematics", label: "数学" },
  { value: "Information Theory", label: "信息论" },
];

const state = { category: "all", edition: "all", query: "" };
const shelf = Array.isArray(books) ? books : [];
const categoryFilters = document.querySelector("#category-filters");
const bookGrid = document.querySelector("#book-grid");
const emptyState = document.querySelector("#empty-state");

document.querySelector("#collection-count").textContent = `${shelf.length} ${shelf.length === 1 ? "BOOK" : "BOOKS"} & COUNTING`;

function makeElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text) element.textContent = text;
  return element;
}

function renderCategories() {
  categoryFilters.replaceChildren();
  categories.forEach(({ value, label }) => {
    const button = makeElement("button", value === state.category ? "active" : "", label);
    button.type = "button";
    button.setAttribute("aria-pressed", String(value === state.category));
    button.addEventListener("click", () => {
      state.category = value;
      renderCategories();
      renderBooks();
    });
    categoryFilters.append(button);
  });
}

function matches(book) {
  if (state.category !== "all" && book.category !== state.category) return false;
  if (state.edition !== "all" && book.edition !== state.edition) return false;
  const searchable = [book.title, book.originalTitle, book.author, book.description, book.category]
    .filter(Boolean).join(" ").toLocaleLowerCase();
  return searchable.includes(state.query);
}

function makeBookCard(book) {
  const card = makeElement("article", "book-card");
  const top = makeElement("div", "book-card-top");
  top.append(makeElement("span", "book-category", categories.find((item) => item.value === book.category)?.label || book.category || "未分类"));
  top.append(makeElement("span", "book-edition", book.edition === "translation" ? "译本" : "原著"));
  card.append(top);
  card.append(makeElement("h3", "book-title", book.title || "未命名书籍"));
  if (book.originalTitle && book.originalTitle !== book.title) card.append(makeElement("p", "book-original-title", book.originalTitle));
  card.append(makeElement("p", "book-author", [book.author, book.language].filter(Boolean).join(" · ")));
  if (book.description) card.append(makeElement("p", "book-description", book.description));

  const links = makeElement("div", "book-links");
  (book.links || []).forEach((item) => {
    try {
      const url = new URL(item.url);
      if (!["https:", "http:"].includes(url.protocol)) return;
      const link = makeElement("a", "book-link", `${item.label || "查看书籍"} ↗`);
      link.href = url.href;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      links.append(link);
    } catch { /* Ignore an invalid book link. */ }
  });
  card.append(links);
  return card;
}

function renderBooks() {
  const visible = shelf.filter(matches);
  bookGrid.replaceChildren(...visible.map(makeBookCard));
  bookGrid.hidden = visible.length === 0;
  emptyState.hidden = visible.length > 0;

  if (shelf.length === 0) {
    document.querySelector("#empty-title").textContent = "书架已经备好。";
    document.querySelector("#empty-description").textContent = "第一本值得收藏的书，即将在这里上架。";
  } else {
    document.querySelector("#empty-title").textContent = "暂时没有找到这本书。";
    document.querySelector("#empty-description").textContent = "试试其他关键词或筛选条件。";
  }
}

document.querySelector("#search").addEventListener("input", (event) => {
  state.query = event.target.value.trim().toLocaleLowerCase();
  renderBooks();
});

document.querySelectorAll("[data-edition]").forEach((button) => {
  button.addEventListener("click", () => {
    state.edition = button.dataset.edition;
    document.querySelectorAll("[data-edition]").forEach((option) => {
      option.classList.toggle("active", option === button);
      option.setAttribute("aria-pressed", String(option === button));
    });
    renderBooks();
  });
});

renderCategories();
renderBooks();
