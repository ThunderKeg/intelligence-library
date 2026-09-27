# 本文源稿约定

原文只依据仓库根目录 `A Mathematical Theory of Communication.pdf`。`pdftotext` 或 PyMuPDF 仅用于定位，所有段落、公式、符号、图和脚注必须在 PDF 原页核对。请勿调用本机模型或以概要代替翻译。

## 文件与分工

按原文顺序使用 `chapter-00.md`（引言）、`chapter-01.md`（Part I）、`chapter-02.md`（Part II）、`appendix-1-4.md`、`chapter-03.md`（Part III）、`chapter-04.md`（Part IV）、`chapter-05.md`（Part V）、`appendix-5-7.md`。每个文件只能由一名初译 Agent 编辑；审查另行分配。跨书共享的 `books.js`、`app.js`、`styles.css`、`sw.js` 和编译脚本由集成 Agent 修改。

## Markdown 约定

- `# 第一篇 ……` 表示原文 Part 标题；`## 1. ……` 表示原文编号节标题。附录用 `# 附录 1—4`，内部用 `## 附录 1`。引言保留论文题名为一级标题、`## 引言` 为原文小标题，并保留原刊重印说明、作者和脚注。
- 每篇标题后用 `<aside class="chapter-guide"><strong>本篇导读</strong><p>……</p></aside>` 添加简短中文导读。导读与译文分离，不宣称是原文。
- 在每个新的 PDF 物理页起点插入 `<!-- pdf-page: N -->`。跨页段落保持为同一段，页标可紧邻段落之前或之后，并在审查记录中说明。
- 原文每一段对应一段译文；保留原顺序与列表层级。原文有脚注时用 `[^标号]` 引用与定义。正文不得出现“略”“待补”等占位文字。
- 行内公式用 `$...$`，独立公式用 `$$` 单独成行的块；原文有编号时用 `\tag{编号}`。保留原始符号、变量大小写、上下标及公式前后的标点。译文中不要用纯文本近似替代公式。
- 原文如有表格，用 Markdown 表格逐格翻译；如有代码，使用标注语言的围栏并保留缩进。
- 图像只截取单幅原图，放在 `assets/`；用下列结构，图注与图内文字都翻译。不要使用整页 PDF 图片。

```html
<figure id="fig-1">
  <img src="books/shannon-mathematical-theory-1948/assets/fig-1.png" alt="原图内容的准确描述">
  <figcaption>图 1：原书图注的译文。</figcaption>
  <p class="figure-translation">图内文字：INFORMATION SOURCE＝信源；……</p>
</figure>
```

- 译名建议：information source＝信源；channel＝信道；capacity＝容量；entropy＝熵；equivocation＝疑义度（首次标注 equivocation）；ensemble＝系综（首次标注 ensemble）；fidelity＝保真度。先以原文语境为准，审查时统一。
- 初译者另写与源稿同名的 `*.review.md` 核对记录，列出覆盖 PDF 页、图、公式/编号、脚注和仍有疑点。审查 Agent 在同一记录中追加独立审查结论；不能仅凭自动统计判定完成。

## 编译与检查

源稿经 `python scripts/build_shannon_chapters.py` 生成八个 `chapter-*.json`。编译器使用 Python 的 `markdown`、`beautifulsoup4` 和 Node.js 中仓库自带的 KaTeX，将公式转换为原生 MathML，并检查页标、图像路径和意外代码块。本地启动 `python -m http.server 8787 --bind 127.0.0.1` 后，可运行 `python scripts/qa_shannon.py` 检查整书结构、图像、公式、窄屏、深色模式、链接、进度与离线缓存；该检查使用 Playwright。
