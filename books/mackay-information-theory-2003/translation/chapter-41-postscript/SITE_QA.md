# PDF516 独立附记网站 QA

## 未注册草稿：PASS（2026-10-04）

- 基线：`chapter-41-postscript.draft.json`，1823 字节，SHA256 `31ec052c08626e22ef3cfb04cffbf618c38c630bc25f85f7ef699fba002c3999`；独立原页和结构审查见本目录 `REVIEW.md`，结论 PASS。`tools/preview_chapter_41_postscript.py --sha256 <SHA>` 在 Edge 1440／390／320 px 浅色、深色六视口实际渲染；草稿模式仅在浏览器请求时临时插入第 41 章和本附记，不写正式目录。
- 六视口均显示 PDF516 原顺序的 5 块、1 项目录：标题、作者段、第一段缩进引文、作者段、第二段缩进引文。引语正文与 JSON 完全一致；左边线 3px、内缩 20px，在 320px 仍完整可读且不横溢。标题上方原页横线、两段间距和深浅色对比已目视截图复核。没有多余图、表、公式、习题、代码或脚注。
- 目录可在移动端打开、关闭；第 41 章↔独立附记的草稿临时相邻导航双向可达。六视口末块均保存 `chapter=41-postscript`、物理页 516、`read-p516-b005`、进度 100%；各连续刷新三次，末块位置稳定。无 JS 报错、HTTP／资源失败或整页横溢。

## 已注册正式路径：PASS（2026-10-04）

- 正式 `chapter-41-postscript.json` 与上列审定草稿逐字节一致，SHA256 同上。用 `tools/preview_chapter_41_postscript.py --formal --sha256 <SHA>` 从原始 `books.js` 和正式 JSON 加载真实 `?book=mackay-information-theory-2003&chapter=41-postscript`；正式模式不拦截或注入目录、JSON。
- 1440／390／320 px 明暗六视口复核 5 阅读块、1 目录、两段缩进引文及标题上方横线；移动端引文左边线、20px 内缩和深浅色正文均清晰，无额外图、式或习题。正式第 41 章↔独立附记的双向相邻导航逐视口点击可达。
- 六视口页底均为 `chapter=41-postscript`、物理页 516、末块 `read-p516-b005`、进度 100%；各连续刷新三次，末块位置稳定。无资源失败、JS 报错或整页横溢。
