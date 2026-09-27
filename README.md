# 算经阁

用于阅读个人学习图书的静态网页，托管在 [GitHub Pages](https://thunderkeg.github.io/intelligence-library/)。目前收录香农的 *A Mathematical Theory of Communication* 全文（引言、五篇正文和七个附录），以及 Bishop 与 Bishop 的 *Deep Learning: Foundations and Concepts* 第 1 章中文译文。

阅读器显示连续正文和章节目录，按书保存当前章节及段落位置。桌面显示侧栏目录，手机可从顶部打开目录；深色模式可跟随系统或手动切换。多章图书在目录中切换章节，并在章末显示上一章、下一章。PWA 预缓存香农全文及图表，也缓存其他已阅读章节供离线阅读，并在部署新版本后自动更新。

## 本地预览

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>。

## 编辑内容

书架元数据及章节清单在 `books.js`。香农译稿、任务和审查记录在 `books/shannon-mathematical-theory-1948/`，运行 `python scripts/build_shannon_chapters.py` 更新八个阅读器 JSON。Bishop 第 1 章的译文在 `books/bishop-deep-learning-2024/translation/page-XX.md`，运行 `python scripts/bundle_bishop_chapter1.py` 更新阅读器使用的 `chapter-01.json`。网页发布章节 JSON 和图资产，不发布原书 PDF 或正文整页页图。

新增图书或章节时，在 `books.js` 中为图书设置唯一 `id`，在 `chapters` 中按阅读顺序列出章节编号、标题与内容 JSON 路径。Pages 工作流会发布 `books` 下的 `chapter-*.json` 和 `assets/`；已访问的章节会进入离线缓存。`main` 分支更新会自动部署。
