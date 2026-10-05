# 算经阁

用于阅读个人学习图书的静态网页，托管在 [GitHub Pages](https://thunderkeg.github.io/intelligence-library/)。目前收录以下六本书的中文译文与编撰内容：

- 《深度学习：基础与概念》（Christopher M. Bishop、Hugh Bishop，2024）
- 《模式识别与机器学习》（Christopher M. Bishop，2006）
- 《通信的数学理论》（Claude E. Shannon，1948）
- 《强化学习：导论》（Richard S. Sutton、Andrew G. Barto，第二版）
- 《信息论、推断与学习算法》（David J. C. MacKay，2003）
- 《凸优化》（Stephen Boyd、Lieven Vandenberghe，2004）

阅读器显示连续正文和章节目录，按书保存当前章节及段落位置。桌面显示侧栏目录，手机可从顶部打开目录；深色模式可跟随系统或手动切换。多章图书在目录中切换章节，并在章末显示上一章、下一章。阅读器支持正文编号、原书目录和索引的链接跳转。

图、公式和有编号的表格引用支持桌面悬停预览、点击查看完整内容，以及手机轻点查看；章引用显示章标题，节引用显示所属章和节标题，预览内可跳转到原文。结构化内容的书复用章节引用索引，《凸优化》按 HTML 元素编号精确定位图与公式，并为章、节引用建立索引。《通信的数学理论》支持原书有编号的图片和表 I 引用；书内没有可唯一核对的公式及章引用。后续书籍可在 `books.js` 中配置 `referenceIndex` 和 `referencePreview` 复用同一组件，并逐书核对引用目标和显示效果。富 HTML 书籍可用 `python scripts/build_rich_reference_indexes.py --check` 校验预览索引。

PWA 预缓存六本书的全部阅读文本，以及香农全文图表。打开其余五本书后，页面会准备对应图书的全部图片，准备期间显示进度，完成后隐藏提示；尚未访问的章节和图片也可离线阅读。部署新版本后，缓存会自动更新。

## 本地预览

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>。

## 编辑内容

书架元数据及章节清单在 `books.js`。各书的译稿、任务与审查记录保存在对应书目目录中。

香农全文的逐篇译稿在 `books/shannon-mathematical-theory-1948/`；运行 `python scripts/build_shannon_chapters.py` 更新八个阅读器 JSON，内容覆盖引言、五篇正文和七个附录。

《深度学习：基础与概念》的完整译稿在 `books/bishop-deep-learning-2024/chapters/`，覆盖卷首、20 章、附录 A–C、参考文献和索引；运行 `python scripts/build_bishop_chapters.py --chapter 1` 更新对应阅读器 JSON，可替换为章号 `0–20`、附录名 `A`、`B`、`C`，或 `frontmatter`、`contents`、`bibliography`、`index` 等单元名。

Sutton 与 Barto 的任务、术语和审查记录在 `books/sutton-barto-reinforcement-learning-2e/`，逐页译稿分别在 `frontmatter/`、`parts/`、`translation/` 和 `backmatter/`，完整页码映射见 `PAGE-AUDIT.csv`。运行 `python scripts/bundle_sutton_frontmatter.py`、`python scripts/bundle_sutton_part1.py`、`python scripts/bundle_sutton_part2.py`、`python scripts/bundle_sutton_part3.py` 更新卷首与三部分引言；第 1、2 章分别使用 `python scripts/bundle_sutton_chapter1.py`、`python scripts/bundle_sutton_chapter2.py`，第 3–17 章使用 `python scripts/bundle_sutton_chapters.py 3`（替换章号），书后材料使用 `python scripts/bundle_sutton_backmatter.py all`。重建后运行 `python scripts/build_sutton_reader_indexes.py` 更新交叉引用与离线图片清单。

MacKay 全书译稿、任务清单与逐章独立审查记录在 `books/mackay-information-theory-2003/`。正式阅读内容覆盖原书 PDF 物理页 1–640，包括卷首、第 1–50 章、各部分扉页与导页、附录 A–C、参考文献、索引及独立后记。该目录下的 `tools/build_reference_index.py` 生成正文编号跳转索引，`tools/build_offline_manifest.py` 生成全书图片离线清单，`tools/verify_registered.py` 和 `tools/verify_book_static.py` 校验正式阅读单元、引用及资源。全书整体审查已通过，记录见 `translation/GLOBAL_REVIEW.md`；首次打开本书并等图片准备完成后，尚未访问的图也可离线阅读。

《模式识别与机器学习》（Christopher M. Bishop，2006）已完成卷首、14 章、附录 A–E、参考文献和索引的中文翻译与编撰，保留原图并附图内文字译注。任务、逐页来源、译稿、术语和独立审查记录在 `books/bishop-pattern-recognition-2006/`；运行 `python books/bishop-pattern-recognition-2006/tools/build.py chapter-01`（替换阅读单元 ID）重建该单元，再运行 `python books/bishop-pattern-recognition-2006/tools/indexes.py` 更新本书引用和离线图片清单，`python books/bishop-pattern-recognition-2006/tools/verify_book.py` 核对验收指纹与全书结构。书架包含 25 个阅读单元，支持正文的章节、小节、图表、公式、习题及附录编号跳转，也支持目录与索引跳转和阅读进度。首次联网打开本书时会预先下载全部 342 张图片；准备完成后，尚未读过的章节图片也可离线加载。

《凸优化》（Stephen Boyd、Lieven Vandenberghe，2004；依据 2009 年第七次印刷）已完成卷首、第 1–11 章、三篇附录、250 条参考文献与 67 行符号表的中文翻译和独立审查。全书按原序提供 23 个阅读单元，保留 180 幅原图并附图内文字译注；每章有独立导读，公式保留可复制 TeX，支持目录、交叉引用、阅读进度及全书离线阅读。首次联网打开本书时会自动准备全书图片，准备完成后，无需逐章访问即可离线阅读；正文编号与文献键可以直接点击跳转。译稿、术语、任务与审查记录位于 `books/boyd-vandenberghe-convex-optimization-2004/`。运行 `python books/boyd-vandenberghe-convex-optimization-2004/tools/build.py` 重建内容，再运行 `python books/boyd-vandenberghe-convex-optimization-2004/tools/link_references.py` 与 `python books/boyd-vandenberghe-convex-optimization-2004/tools/offline_manifest.py` 更新引用及离线清单；使用 `python books/boyd-vandenberghe-convex-optimization-2004/tools/validate.py` 核对结构。

新增图书或章节时，在 `books.js` 中为图书设置唯一 `id`，在 `chapters` 中按阅读顺序列出章节编号、标题与内容 JSON 路径。Pages 工作流会发布各书的正式阅读 JSON、引用索引、图片离线清单及 `assets/`，不发布原书 PDF、逐页译稿或审查记录。`main` 分支更新会自动部署。
