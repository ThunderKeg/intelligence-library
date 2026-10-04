# MathML 公式列对齐独立回归审查

状态：**通过。** 本记录作为第 1–13 章已有内容验收的显示层附记，不替代原文审查，也不表示后续未验收单元已经完成。reviewer 未编写本次 CSS 修复，独立阅读了规则、检查脚本与完整结果，并实际逐张打开全部 42 张回归截图。

## 问题与修复范围

Chromium 原生 MathML 没有按 `mtable columnalign` 完成预期列对齐；第 14 章式 14.49 的两行等号因此出现明显水平错位。集成 Agent 在 `styles.css:217` 起添加四行规则，将 `right left` 的奇数/偶数列分别设为右/左对齐，单 `right` 设为右对齐，`left left` 的各列设为左对齐。全部选择器都限定 `#reader-article[data-book-id="bishop-pattern-recognition-2006"]`，不影响其他图书。

修复没有改写原书公式、TeX、编号、源稿和图片。本 reviewer 重新计算第 1–13 章的源稿归一化 SHA、去验收元数据的 JSON 内容 SHA 和全部图片集合 SHA，39 项全部仍与 `source-inventory.json` 的已验收值一致，证据为 `tmp/prml-review/math-alignment/accepted-contents-unchanged.json`。

## 自动证据的独立核查

已阅读 `tools/qa_math_alignment.py` 和 `reviews/math-alignment-qa.json`。19 个已生成单元各检查 1440 浅色、390 深色两模式，共 38 个页面结果、350 个对齐表实例：332 个 `right left`、16 个 `left left`、2 个 `right`。全部单元格的计算样式符合指定列方向；其中 222 个含多个可比较等号的表实例，其等号横坐标最大差值均为 0 px。其余实例检查的是列方向，不能把没有多个等号的实例说成做了多等号测量。检查脚本另有页面宽度断言，全部通过。

## 实际查看的 42 张截图

已逐张打开 `tmp/prml-math-alignment/` 下报告列出的全部 42 张 PNG，含两种模式，覆盖第 1–14 章。具体目标：1.9；2.41/2.47；3.11；4.53/4.57；5.73；6.12/6.95；7.42/7.51；8.16；9.2/9.13；10.6/10.64；11.12/11.51；12.25；13.17；14.11。

等号或续行运算符的起点一致，分支中的值与条件按列左对齐，单列两行推导按右边缘对齐。公式编号、分式、可伸缩括号及相邻正文没有出现此次修复引入的碰撞或遮盖。窄屏长式继续使用局部水平滚动并显示提示；本次 42 图是默认滚动位置的列对齐回归，不代替各章已完成的实际横滑审查。

完整截图路径、实际查看标记、逐图 SHA、脚本/报告 SHA 和这四行 CSS 的独立指纹记录在 `tmp/prml-review/math-alignment/viewed-ui.json`。第 13 章额外 13 张长式/横滑修复复核已另记 `chapter-13-review.md`；第 14 章完整网页由 root 在 `chapter-14-ui-review.md` 独立验收。未发现需要继续修复的问题。
