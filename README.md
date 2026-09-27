# Intelligence Library · 算经阁

一个无构建依赖的个人学习书架。每本书有独立内容文件；阅读器支持中英双语、逐书进度、离线阅读和自动更新。

## 预览样章

在仓库根目录运行：

```powershell
python -m http.server 8787 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8787/>，点击 Bishop 书卡上的“阅读样章”。PWA 和 JSON 内容都需要 HTTP，直接双击 `index.html` 无法完整预览。关闭网络后，已首次加载的页面和样章可从缓存打开。

目前的样章依据 Christopher M. Bishop 与 Hugh Bishop 的 *Deep Learning: Foundations and Concepts*（2024）第 1 章 1.2 节编写。中英文都是原创学习导读，不是原书逐字内容或正式译本。原书可从[作者网站](https://www.bishopbook.com/)访问。仓库内的 PDF 不作为网站资源上传。

## 添加一本书

1. 在 `books.js` 的 `books` 数组添加书籍元数据，给每本书一个永久且唯一的 `id`。`content` 指向该书的 JSON 文件，例如 `books/my-book.json`。
2. 按 `books/bishop-deep-learning-2024.json` 的结构添加章节、节和段落。每个段落有 `en` 和 `zh`；可用 `type: "formula"` 加 `formula`，或用 `type: "callout"` 加 `label`。
3. 在 `sw.js` 的 `CORE_ASSETS` 中加入新内容文件。Pages 工作流每次部署都会把提交 SHA 写入缓存版本；浏览器会检查新版 service worker 并更新缓存。

阅读进度以 `intelligence-library:progress:v1:<book-id>` 保存在浏览器本地，包括节与段落位置；不同书互不影响。语言偏好在各书之间共用。清除浏览器站点数据会清除进度，目前没有跨设备同步。

## 发布到 GitHub Pages

仓库的 `.github/workflows/pages.yml` 会在 `main` 更新时发布精确列出的网页文件。首次发布前，在 GitHub 仓库 **Settings → Pages → Build and deployment** 中选择 **GitHub Actions**。之后提交并推送到 `main` 即可触发部署。项目站点路径是 `https://thunderkeg.github.io/intelligence-library/`（以仓库实际 Pages 设置为准）。

Workflow 只打包 HTML、CSS、JS、JSON、图标和 manifest；不会上传 PDF 或 `.obsidian`。图标可运行 `python scripts/generate_icons.py` 重新生成。
