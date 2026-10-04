# 第七部分扉页独立原页与结构审查

状态：**源页与冻结草稿结构 PASS**。本记录核原书 PDF 物理页 609、译稿、图资产及未注册冻结草稿；整页网站视觉验收另行进行。

## 核对基线

- 原书：根目录 `Information Theory, Inference, and Learning Algorithms.pdf`，物理页 609。逐项目视核对。
- 译稿：`pdf-609.md`。
- 冻结草稿：`chapter-VII.draft.json`，572 字节，SHA-256 `b63bf02e97586398bab47d3c954e619304265b90ab6e9ca05faa9ebb03453a43`。
- 独立只读重编译：由 `pdf-609.md` 和图资产重新生成两个块，逐字段与冻结 JSON 的 `blocks` 相同，冻结 SHA 再算一致。

## 原页与资产

| 项目 | 结论 |
| --- | --- |
| 标题 | 原页居中两行 `Part VII`、`Appendices`；译为“第七部分”“附录”准确，H1 与 1 项目录没有额外章正文。 |
| 图案 | `assets/part-VII-emblem.png` 为 2590×2620 RGB PNG，可解码；目视原页与裁图，空心圆、黑色扇形及细小递归分支完整，无图内文字。非白像素包围框为 `(33, 34, 2557, 2586)`，四边仍有留白。 |
| 其他内容 | 原页无正文、图注、公式、表格、脚注或习题；草稿恰为 `p609-b001` H1 和 `p609-b002` 图两个块，`sourcePdfPages=[609,609]`，与附录 A 分离。 |

## 已关闭问题

- **S-VII-01，双行标题。** 初始草稿 H1 用 `segments:["第七部分\n附录"]`，共享 CSS 原先未对本页保留换行。根 Agent 已给本书 `#read-p609-b001 h1` 加 `white-space: pre-line`，草稿内容及 SHA 未变。独立通过真实浏览器草稿路径检查 1440、390、320 px 浅色：字符位置分别落在“第七部分”与“附录”两行；2590×2620 图均成功解码，无脚本错误。移动端截图可复查 `C:\Users\Admin\AppData\Local\Temp\mackay-part-vii-390.png`。本项关闭。
