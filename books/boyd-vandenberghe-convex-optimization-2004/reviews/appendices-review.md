# 附录分隔页独立审查

审查者：`convex_build`，未承担本单元初译。审查范围：原 PDF 645–646、`translation/appendices.md`、`chapter-appendices.json` 和实际阅读器；不含附录 A/B/C 正文。

**结论：本单元内容与网页排版审查通过，无待修问题。** 此结论仅适用于下列冻结快照，不表示附录正文或全书导航已经验收。

| 对象 | 独立核对结果 |
| --- | --- |
| PDF 645 | 完整原页只有标题 `Appendices`，译文“附录”准确；没有遗漏的正文、图、表、公式、脚注或页下注。 |
| PDF 646 | 已直接查看完整原页，确为空白；源稿保留 646 页标，没有编造阅读内容或嵌入整页图片。 |
| Markdown | 页标为 645、646，中间仅一个一级标题“附录”，与原页内容相符。 |
| JSON | schemaVersion 3，sourcePdfPages 为 `[645,646]`；仅 1 个 heading block，来源页为 645，images 为空；没有生成空白页正文。 |
| 实际 reader | 独立运行现有 `tools/qa_reader.py`，只在隔离测试浏览器中注入本单元目录。1440 浅色、390 浅色、390 深色、320 深色共 4 视图通过；已逐张查看本轮截图，标题完整、字形和对比正常、无正文横向溢出，页标没有外露。移动目录开关断言通过。 |

独立复测只读使用原稿和正式 JSON；前后 SHA 相同。没有重建或修改 JSON，没有改共享配置，也没有重跑旧单元。

证据目录：`tmp/convex/review-appendixA/appendices-reader/`。`results.json` 记录自动检查，`independent-check.json` 记录快照与独立目视状态，四张 `appendices-*-opening.png` 为实际网页截图。复现脚本：`tmp/convex/review-appendixA/check_appendices_reader.py`。原页目视为 `tmp/convex/pages/page-645.png`、`page-646.png`。

| 冻结文件 | SHA-256 |
| --- | --- |
| `translation/appendices.md` | `9fc923d4de3fd96aaebc997e217a58c7f1f0f78fff552710d6e8a1549af65f30` |
| `chapter-appendices.json` | `34708c62cd4b3c870d66471aaca38f05a9758ed7507414d6a11c38e9c40d281b` |

原 PDF SHA-256 为 `40d976c83c18cce1900eff8c41bd5ad408c102b813af39d05ff85678ccf8d76e`。后续 A/B/C 内容与整书导航由各自的独立审查和全书整体验收处理。
