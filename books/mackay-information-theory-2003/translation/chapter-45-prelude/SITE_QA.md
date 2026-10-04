# 第 45 章前导页网站独立 QA

## 未注册草稿：PASS（2026-10-04）

- 基线：`chapter-45-prelude.draft.json`，4252 字节，SHA256 `b24825171362126007c16454504d00144b1673fb027b01e556403c8816505407`；独立原页与草稿结构 `REVIEW.md` 已 PASS。未参与初译的 Agent 用 `tools/preview_chapter_45_prelude.py --sha256 <SHA>` 在 Edge 1440／390／320 px 明暗六视口渲染。草稿模式只在浏览器收到的 `books.js` 中临时把导页接在正式第 44 章后，不写正式目录或 JSON。
- 六视口均按原页顺序呈现 7 块：一个上边 3px 横线、居中斜体“关于第 45 章”标题，三段导言、带空心三角及难度 3 的习题 45.1、两个软件网址段。标题 DOM 文字与草稿相同；目录仅一项且在手机可开关。原页没有的图、公式、表、脚注或额外导读均未出现。
- 两条 URL 的可见文字、`href` 和实际点击事件均与原页一致：`http://www.inference.phy.cam.ac.uk/mackay/itprnn/software.html`、`http://www.cs.toronto.edu/~radford/`；句点留在链接外。`octave` 保持等宽代码显示；320px 长链接可换行且保持可点，没有整页横溢。
- 44↔前导页临时相邻导航可点击往返。六视口滚至页底均保存 `chapter=45-prelude`、物理 PDF 页 546、末块 `read-p546-b007`、进度 100%；各连续刷新三次恢复位置稳定。无 JS 报错、失败资源或 HTTP 错误。
- **S45P-SITE-01 已关闭：** 首轮 1440px 明暗第二段 `p546-b003` 末行仅“算。”。浏览器定向对照后，共享 CSS 为该块在桌面 ≥801px 用 `text-wrap: balance`、窄屏保留 `pretty`；最终桌面段落五行均匀，390／320 明暗原有布局可读，六视口短尾扫描为零。草稿 SHA 未变。

## 已注册正式路径：PASS（2026-10-04）

- 正式 `chapter-45-prelude.json` 与审定草稿逐字节一致：4252 字节，SHA256 `b24825171362126007c16454504d00144b1673fb027b01e556403c8816505407`。`tools/preview_chapter_45_prelude.py --formal --sha256 <SHA>` 直接加载原始 `books.js`、正式 JSON 与真实 `?book=mackay-information-theory-2003&chapter=45-prelude`；正式模式没有目录／JSON 路由拦截或 CSS 注入。
- Edge 1440／390／320 px 明暗六视口重新核实 7 块／1 目录、3px 上横线与居中斜体标题、三段和习题 45.1、两条 URL 的显示文字／目标／可点击性及链接外句点。44↔导页真实双向导航可用；窄屏链接正常换行，无短尾、整页横溢、脚本或资源错误。
- 六视口页底均保存 `chapter=45-prelude`、物理 PDF 页 546、末块 `read-p546-b007`、进度 100%；各连续刷新三次恢复位置稳定。
