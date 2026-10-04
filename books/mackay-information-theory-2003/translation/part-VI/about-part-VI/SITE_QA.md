# 关于第六部分导页网站独立 QA

## 未注册草稿：PASS（2026-10-04）

- 冻结基线：`chapter-VI-intro.draft.json`，3869 字节，SHA256 `8855f5e49eb555da1ce5ee716a8e48aece87418badb4ad69040dc207480ea584`，原书 PDF 物理页 568；独立原页源审 `REVIEW.md` 已 PASS。`tools/preview_about_part_VI.py --expected-sha <SHA> --scan-tail` 在 Edge 1440／390／320 px 明暗六视口渲染。草稿模式仅在浏览器目录响应中临时接入第六部分扉页及本导页。
- 最终六视口通过：标题与四段按顺序显示，一项目录；顶部分隔线、居中斜体标题、五处正文斜体强调及五处行内 MathML 可见，1440 浅与 320 深逐式复制各 5／5。第六部分扉页↔导页双向导航、末块 `read-p568-b005`／PDF568／100% 和各三次刷新稳定；无 JS／资源错误或整页横溢。原页无展示公式、图片、表格或习题。
- **SVI-INTRO-SITE-01 已关闭：** 首轮截图确认 390px `p568-b003`“长。”、`p568-b005`“录。”及 320px `p568-b004`“出。”独占末行。集成 Agent 在共享 CSS 对这三个精确段落加 `text-wrap: pretty`；最终按冻结 SHA 用 `--scan-tail --strict-tail` 复测六视口短尾均为零，截图目视斜体、段落和行内数学可读。原译文未改。

## 已注册正式路径：PASS（2026-10-04）

- 正式 `chapter-VI-intro.json` 与审定草稿逐字节一致：3869 字节，SHA256 `8855f5e49eb555da1ce5ee716a8e48aece87418badb4ad69040dc207480ea584`。`tools/preview_about_part_VI.py --formal --expected-sha <SHA> --scan-tail --strict-tail` 在真实 `?book=mackay-information-theory-2003&chapter=VI-intro` 加载原始 `books.js` 与正式 JSON；正式模式无目录／JSON 拦截或样式注入。
- Edge 1440／390／320 px 明暗六视口再次通过 5 块／1 目录／4 段、标题横线及居中斜体、5 处强调、5 处行内 MathML。1440 浅和 320 深逐个复制各 5／5；六视口短尾零处、无整页横溢。真实第六部分扉页↔导页双向导航可用；页底 `chapter=VI-intro`、PDF568、末块 `read-p568-b005`、100% 及各三次刷新稳定。无 JS／资源／HTTP 错误。
