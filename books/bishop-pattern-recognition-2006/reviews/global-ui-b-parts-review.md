# 全书统一改动：b 初译部分的独立增量排版审查

审查人：root（未承担这些段落的初译）。本次仅审查全书统一术语和语句修正后的页面显示；原章的逐页内容审查仍见各章原审查记录，增量原文语义由 prml_reviewer 另行审查。

审查版本：`reviews/global-delta-before-taylor-qa.json` 所列 chapter-05、chapter-12、chapter-13 的 sourceLF/render/image 指纹（原 global-delta-qa.json 的原样保留版本）。目标块来自 `reviews/global-ui-change-plan.json` 中 originalAuthor=b 的全部 9 块。后来新增的三处泰勒术语统一，由独立的后续增量报告覆盖，不计入本次 21 张截图。

| 单元 | 目标块 | 模式检查 | 实际查看截图 |
| --- | --- | ---: | ---: |
| chapter-05 | p40-b005、p40-b011、p62-b005 | 6 | 6 |
| chapter-12 | p33-b008、p35-b003 | 4 | 4 |
| chapter-13 | p25-b004、p26-b001、p27-b001、p27-b004 | 8 | 11 |

每块均在 1440px 浅色和 390px 深色模式检查。21 张截图已逐张使用 view_image 实际查看，含第 13 章长段落的续屏以及图 13.16 横向滑动后的右半部分；路径与逐文件 SHA-256 记录在 `tmp/prml-global-review/viewed-b-ui.json`。自动几何检查记录为 `reader-qa-chapter-05-targets-global-b.json`、`reader-qa-chapter-12-targets-global-b.json`、`reader-qa-chapter-13-targets-global-b.json`。

结果：通过。雅可比、生成式、判别式、格图及自联想映射的改动显示完整；中文段落、斜体、交叉引用、公式、编号、图注和图内文字译注均清晰。图 13.16 的三个状态、四个时刻与路径在桌面完整显示，在窄屏可左右滑动查看；滑动不会推动整个页面。第 5 章较长公式保留局部横向滚动提示。未发现本次文字改动带来的截断、重叠、缺图或深色模式对比问题。

待修问题：无。该记录不将未检查的其他块或其他模式计作本次人工审查。
