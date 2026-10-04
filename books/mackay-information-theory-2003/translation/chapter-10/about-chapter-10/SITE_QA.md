# 第 10 章导页草稿站点独立验收

审查日期：2026-10-03。审查者未参与本页初译或构建。以 `chapter-10-intro.draft.json` 的临时路由检查 PDF 物理页 173；原页内容独立审查见 `REVIEW.md`。当前仅评价草稿页面，正式目录接入后还需回归。

**结论：草稿网站验收通过，S10-01 已修复并独立复测。** `python books/mackay-information-theory-2003/tools/preview_about_chapter_10.py` 通过结构基线；1440 × 844 浅色、390 × 844 浅色和深色页面均无脚本错误、MathML 回退或整页横溢，表格 13 行（导航表头 + 原书 12 行）、18 处表内 MathML 均存在。窄屏表格宽度为 342／342px，无截列；技术译注在原书提示后独立显示。上一章链接进入第 9 章；在表格处保存 `chapter=10-intro, block=read-p173-b005`，刷新后回到表格。

| 编号 | 定位及可复核证据 | 影响及状态 |
| --- | --- | --- |
| S10-01 | 初审时，表格 `#read-p173-b005` 的 `$C$` 与 `$\mathcal C$`、`$s$` 与 `$\mathbf{s}$` 在 Edge 390px 页面上几乎相同。原始 MathML 的 `mathvariant="script"/"bold"` 在此浏览器未可靠显形。 | 集成 Agent 修复后再次运行三个视口：相应 `mi` 的可见文本分别为 `C`／`𝒞`、`s`／`𝐬`，截图中的笔形也能区分。修复后截图在系统临时目录 `mackay-a10-fixed-1440-light.png`、`mackay-a10-fixed-390-light.png`、`mackay-a10-fixed-390-dark.png`；无缺字和横溢。**已关闭。** |

表格的 `$R=K/N$` 行在 DOM 和截图中均保留 `$R'$` 的上标 prime；`$\mathbf{x}^{(s)}$` 的 `(s)` 保留上标；`$\hat{s}$` 的帽标可见。正式目录路径仍待接入后复核。

## 正式路径独立回归（2026-10-03）

不注入临时 `books.js` 或章节 JSON，从第 9 章的下一章链接进入 `?book=mackay-information-theory-2003&chapter=10-intro`。Edge 1440 × 844 浅色、390 × 844 浅色／深色均有 5 个阅读块、13 行表格（表头加原书 12 行）及表内 18 个 MathML，无错误、失败资源请求或整页横溢。表格宽度在桌面为 740／740px、手机为 342／342px；三个视口的实际 `mi` 文本均分别为 `C`／`𝒞`、`s`／`𝐬`，截图显示字形可区分，$R'$ 的 prime 亦可见。

正式目录中本导页有当前章标识；上一章链接返回第 9 章正文并加载 240 块。在表格处保存 `chapter=10-intro, page=173, block=read-p173-b005`，刷新后表格顶部位于视口约 y=85px。三视口截图存于系统临时目录的 `mackay-real-a10-table-1440-0.png`、`mackay-real-a10-table-390-0.png`、`mackay-real-a10-table-390-1.png`。**正式路径独立回归通过。**
