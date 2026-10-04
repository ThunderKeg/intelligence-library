# 算经阁

用于阅读个人学习图书的静态网页，托管在 [GitHub Pages](https://thunderkeg.github.io/intelligence-library/)。目前收录香农的 *A Mathematical Theory of Communication* 全文（引言、五篇正文和七个附录），以及 Bishop 与 Bishop 的 *Deep Learning: Foundations and Concepts* 封面、前言、原书目录、20 章、附录、参考文献和索引的完整中文编撰；Sutton 与 Barto 的 *Reinforcement Learning: An Introduction* 卷首、三部分引言、第 1–17 章及书后材料的中文编撰；MacKay 的 *Information Theory, Inference, and Learning Algorithms* 全书中文译编。

阅读器显示连续正文和章节目录，按书保存当前章节及段落位置。桌面显示侧栏目录，手机可从顶部打开目录；深色模式可跟随系统或手动切换。多章图书在目录中切换章节，并在章末显示上一章、下一章。Sutton 正文的章节、部分、小节、图、表、公式、习题和示例编号可以点击跳转。PWA 预缓存香农全文及图表、Bishop、Sutton 与 MacKay 全部文本；打开 Bishop、Sutton 或 MacKay 图书后，页面会准备全书图片，准备期间显示进度，完成后隐藏提示；尚未访问过的图片也可离线阅读。其他已阅读章节和图片在访问后缓存供离线阅读，并在部署新版本后自动更新。

## 本地预览

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>。

## 编辑内容

书架元数据及章节清单在 `books.js`。香农译稿、任务和审查记录在 `books/shannon-mathematical-theory-1948/`，运行 `python scripts/build_shannon_chapters.py` 更新八个阅读器 JSON。Bishop 完整译稿在 `books/bishop-deep-learning-2024/chapters/`，任务和审查记录在同书目录；运行 `python scripts/build_bishop_chapters.py --chapter 1`（替换章号或使用 `A`、`frontmatter` 等单元名）更新阅读器 JSON。Sutton 与 Barto 的任务、术语、审查记录及逐页译稿在 `books/sutton-barto-reinforcement-learning-2e/`；逐章重建后运行 `python scripts/build_sutton_reader_indexes.py` 更新交叉引用与离线图片清单。网页发布章节 JSON 和图资产，不发布原书 PDF 或正文整页页图。

MacKay 全书译稿、任务清单与逐章独立审查记录在 `books/mackay-information-theory-2003/`。正式阅读内容覆盖原书 PDF 物理页 1–640；`tools/build_reference_index.py` 生成正文编号跳转索引，`tools/build_offline_manifest.py` 生成全书图片离线清单，`tools/verify_book_static.py` 校验结构与资源。首次打开本书并等图片准备完成后，尚未访问的图也可离线阅读。

新增图书或章节时，在 `books.js` 中为图书设置唯一 `id`，在 `chapters` 中按阅读顺序列出章节编号、标题与内容 JSON 路径。Pages 工作流会发布 `books` 下的 `chapter-*.json`、Bishop 前后附属 JSON、Sutton 的引用索引和图片清单，以及 `assets/`；已访问的章节会进入离线缓存。`main` 分支更新会自动部署。
