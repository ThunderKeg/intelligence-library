# 算经阁

用于阅读个人学习图书的静态网页，托管在 [GitHub Pages](https://thunderkeg.github.io/intelligence-library/)。目前收录 Bishop 与 Bishop 的 *Deep Learning: Foundations and Concepts* 第 1 章中文译文。

阅读器显示连续正文和章节目录，按书保存当前章节及段落位置。桌面显示侧栏目录，手机可从顶部打开目录；深色模式可跟随系统或手动切换。多章图书在目录中切换章节，并在章末显示上一章、下一章。PWA 缓存已阅读章节以供离线阅读，并在部署新版本后自动更新。

## 本地预览

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>。

## 编辑内容

书架元数据及章节清单在 `books.js`。Bishop 第 1 章的译文在 `books/bishop-deep-learning-2024/translation/page-XX.md`，运行 `python scripts/bundle_bishop_chapter1.py` 更新阅读器使用的 `chapter-01.json`。网页只发布正文 JSON，不发布原书 PDF 或页图。

新增图书或章节时，在 `books.js` 中为图书设置唯一 `id`，在 `chapters` 中按阅读顺序列出章节编号、标题与内容 JSON 路径。Pages 工作流会自动发布 `books` 下的 `chapter-*.json`；已访问的章节会进入离线缓存。`main` 分支更新会自动部署。
