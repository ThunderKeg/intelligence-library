# Intelligence Library · 算经阁

个人学习书架，使用静态文件托管于 GitHub Pages。阅读器提供原书页图与中文译文对照、逐书保存阅读位置、PWA 离线缓存和自动更新。

## 本地预览

在仓库根目录运行：

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>，点击 Bishop 书卡上的“阅读第一章”。阅读器通过 HTTP 加载 JSON，直接双击 `index.html` 无法完整预览。

目前收录 Christopher M. Bishop 与 Hugh Bishop 的 *Deep Learning: Foundations and Concepts*（Springer，2024）第 1 章《The Deep Learning Revolution》，对应原书正文第 1–22 页。每页可查看原版页图、可选取的英文文本与直接翻译的中文正文，包含图注、公式和表格。原始 PDF 不随网站上传；网页发布经压缩的章节页图。

## 维护与添加图书

书架元数据在 `books.js`。为每本书指定不变的 `id` 和内容 JSON 路径；每本书的阅读进度以 `intelligence-library:progress:v2:<book-id>` 分别保存在浏览器本地。语言选择跨书共用。清除站点数据会清除阅读进度，目前没有跨设备同步。

Bishop 第 1 章的中文译文按原书页码存放在 `books/bishop-deep-learning-2024/translation/page-XX.md`。修改译文后，运行 `python scripts/bundle_bishop_chapter1.py` 生成供网页使用的 `chapter-01.json`。首次生成或更换 PDF 时，可运行 `python scripts/render_bishop_chapter1.py` 生成页图。脚本从本地原书 PDF 提取可选取的英文文本；原版页图是英文核对基准。新增图书可沿用按书分目录、按章节生成 JSON 和页图的方式。

新增内容文件后，要将发布资源列入 `.github/workflows/pages.yml`，并将需要离线阅读的资源列入 `sw.js` 的 `CORE_ASSETS`。

## 发布到 GitHub Pages

`main` 更新会触发 `.github/workflows/pages.yml` 发布。站点地址：<https://thunderkeg.github.io/intelligence-library/>。

工作流只上传列出的网页、章节 JSON、页图、图标与 manifest，不上传源 PDF 或编辑用 Markdown。每次部署都会用提交 SHA 更新 service worker 缓存版本；浏览器检测到新版后会重新加载站点。
