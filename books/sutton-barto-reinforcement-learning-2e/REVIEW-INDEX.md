# 索引独立审查记录

- 审查日期：2026-10-03。
- 审查者：未承担索引初编的独立 Agent。
- 原文依据：仓库中的《Reinforcement Learning: An Introduction》第二版 PDF 物理页 541–546（印刷页 519–524）。逐页查看原页图像，并在符号歧义处放大原页；文本及字体抽取只用于辅助逐项定位。
- 审查对象：`backmatter/index/page-541.md` 至 `page-546.md`、重建的 `chapter-IDX.json` 及阅读页桌面、390px 深色模式。
- 当前结论：**通过。** F01 已修复并独立复核，无待解决问题。

## 逐页核对

| PDF 物理页 | 原页与页稿核对重点 | 结果 |
| --- | --- | --- |
| 541 | 索引标题与斜体、粗体页码说明；左栏 k-armed bandits 起，右栏承接 backup diagram 子项；bootstrapping 跨至下一页 | 已核 |
| 542 | bootstrapping 续项；classical conditioning 的三级子项；左右栏 C–E 的词条与 see/see also | 已核 |
| 543 | importance sampling 从左栏接右栏；Mean Square 五个误差缩写 F01；Monte Carlo methods 跨至下一页 | 已核；F01 已关闭 |
| 544 | Monte Carlo methods 续项；on-policy methods 从左栏接右栏；各算法的粗体页码与策略、规划词条 | 已核 |
| 545 | random walk、return、Sarsa 的多级子项；reward signal 从左栏接右栏；state 及其子项 | 已核 |
| 546 | temporal-difference learning 多级子项、Tree Backup、see/see also、value function 的符号与末条 Witten | 已核 |

## 发现与处理

| 编号 | 等级 | 位置 | 问题、依据与状态 |
| --- | --- | --- | --- |
| F01 | 符号 | `page-543.md`，Mean Square 下 Bellman Error、Projected Bellman Error、Return Error、TD Error、Value Error 五个子项 | 原页的缩写分别是带上横线的 BE、PBE、RE、TDE、VE；初稿写成无上横线纯文本。已对照高分辨率原页确认五条上横线，主 Agent 将其改为 `\overline{\mathrm{...}}` 的行内数学并重建 `chapter-IDX.json`。独立复核确认五处均生成 MathML `<mover>`，桌面与 390px 深色模式均显示上横线。已关闭。 |

## 完整性与编排验收

- 六页共 529 个索引条目：290 个主词条、216 个一级子项、23 个二级子项。页稿按原书先左栏后右栏的阅读顺序排列；跨栏、跨页的子项接回所属主词条，没有因物理分页拆出新主词条。
- 对整段原页与页稿按顺序核对，**1139 个数字令牌完全一致**，包括页码、范围及术语内的数字；**167 个斜体数字令牌、75 个粗体数字令牌**的顺序与内容也完全一致。斜体罗马页码 `xv`、`xix` 已另行目视核对。原页说明“先查斜体页码；粗体页码含框内算法”的中文译文准确，且与索引正文分开。
- 索引中的 26 处 *see*/*see also*（其中 *see also* 6 处）及其指向文字、术语中的 λ、σ、ε、α、价值函数上下标与帽号，已结合原页和页稿核对。原页五个上横线是唯一需要补入的图形符号；其余提取时未识别的希腊字母均以原页可见字形核实。
- 独立浏览器预览确认桌面 1440px 与 390px 深色模式均显示 529 个条目、13 处 MathML 行内数学；五个上横线实际可见，子项缩进可辨，无 JavaScript 异常或整页横向溢出。

## 最终复核

已重新对照 PDF 物理页 543 的五处上横线，核查源稿、构建结果及网页显示。F01 已关闭；PDF 物理页 541–546 的索引独立审查**通过**。
