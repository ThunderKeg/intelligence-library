# 算经阁

用于阅读个人学习图书的静态网页，托管在 [GitHub Pages](https://thunderkeg.github.io/intelligence-library/)。目前收录 Bishop 与 Bishop 的 *Deep Learning: Foundations and Concepts* 第 1 章中文译文。

阅读器显示连续正文和章节目录，按书保存段落位置。PWA 缓存正文以供离线阅读，并在部署新版本后自动更新。

## 本地预览

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>。

## 编辑内容

书架元数据在 `books.js`。Bishop 第 1 章的译文在 `books/bishop-deep-learning-2024/translation/page-XX.md`，运行 `python scripts/bundle_bishop_chapter1.py` 更新阅读器使用的 `chapter-01.json`。网页只发布正文 JSON，不发布原书 PDF 或页图。

新增图书时，在 `books.js` 中设置唯一的 `id` 和内容 JSON 路径，并将 JSON 加入 `.github/workflows/pages.yml` 和 `sw.js`。`main` 分支更新会自动部署。
