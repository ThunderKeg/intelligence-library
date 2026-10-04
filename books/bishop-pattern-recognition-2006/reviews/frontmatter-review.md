# 卷首独立审查记录

状态：**独立审查通过（2026-10-03）。2 项内容问题均已修复并复核，4 项补充网页证据缺口已关闭；卷首 4 部分可验收。**

审查日期：2026-10-03。审查人未参与本部分初译；本轮只修改本审查记录，不修改译稿、生成 JSON、任务清单或共享站点文件。

## 依据与范围

- 唯一正文依据：仓库根目录 `Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf`，SHA-256 为 `4ee767e0a6b04fa05ba7e599e9dbb4637a94a4407ccedf0b4d316b1fd7c8ec64`。
- 已逐页查看 PDF 物理页 1–20 的渲染图（`tmp/prml-front/page-001.png` 至 `page-020.png`）。PDF 10 是原书空白页，不是译文漏页。
- 已逐段审查 4 份 Markdown 译稿，并检查对应 JSON 的图片、目录层级、数学段落和页码映射。
- 已实际查看 3 个输出图像资产，对照原页检查图像内容完整性。
- 本轮未启动或控制网站浏览器。下述 MathML/目录数据检查不等于实际网页窄屏和深色模式的显示验收。

## 被审版本

| 译稿 | 覆盖 PDF 页 | SHA-256 |
|---|---:|---|
| `translation/frontmatter.md` | 1–6 | `d3f23536ffaf70b4d11b6372be51657b2d12abf7b316979a90dc447e3b34c5a9` |
| `translation/preface.md` | 7–10 | `8ad20fe44d2e1b4bce59751f311a95c8200b1248c337f60072662f7fd65c6816` |
| `translation/notation.md` | 11–12 | `8f143026a4c4fbee272dd4d1bfe37e13eba756a9f08549c94eb4893b25d01d7d` |
| `translation/contents.md` | 13–20 | `4e809908d0440db7435aa5deb6f88c9d4e3a37b94eceba572162a14e54cb382e` |

| 对应生成文件 | SHA-256 |
|---|---|
| `frontmatter.json` | `2184825e0b8a9fb8fa10c03ba112d3fef2f10cc0fea8f4b6e48410c7dc194b3c` |
| `preface.json` | `e5c22ef8838b2dadde0c683d829f2d8bdffcb0f306f90109f68c81a61124a085` |
| `notation.json` | `21a8eba1913c1f1aaa13563b029ed76a94aedf6d7b19f2822f2c6e46bc278b8e` |
| `contents.json` | `8566e3c40a8f06d2917fe151e275971eff997d7508deaace4834a51a8c408640` |

4 个生成文件的 `sourcePdfPages` 分别为 `[1,6]`、`[7,10]`、`[11,12]`、`[13,20]`，初审时均为 `draft-unreviewed`；没有发现提前宣称验收完成的状态。

2026-10-03 修复复核版本：`translation/frontmatter.md` SHA-256 为 `58597ab72d5daba1fb2423499de046158b4a3926d61c968751526c5096f03a67`；重新构建的 `frontmatter.json` 为 `ab1f11cc1ad122a3d5689a65d5f1e6b6392a3422adadb8504a97b48c5decd607`。以下 2 项已同时核对源码与 JSON。

## 问题台账

| ID | 严重度 | 译稿精确位置 | 原书位置 | 发现与影响 | 建议修复 | 修复/复核状态 |
|---|---|---|---|---|---|---|
| FM-01 | P3：阅读内容规范 | `translation/frontmatter.md:8`；`frontmatter.json` 的 `p01-b002` 第二条 annotation | PDF 1，封面作者姓名 | “Christopher M. Bishop → 作者姓名，保留原文”中“保留原文”是编撰说明，原书没有此句，且作者姓名已经在图注和封面出现。这类过程说明不符合本仓库阅读页以书籍内容为主的要求 | 删去第二条说明，保留书名的完整中文译注即可；若保留作者译注，只呈现姓名本身，不写处理过程 | **已关闭**：第二条说明已删除；源码与 JSON 均复核通过 |
| FM-02 | P3：职衔译法准确性 | `translation/frontmatter.md:55` | PDF 5，作者信息第二行 `Assistant Director` | “副主任”没有保留原书 `Assistant` 这一职衔限定，容易与 `Deputy Director` 混淆。仅根据本 PDF，不能确定作者使用“副主任”这一中文职衔 | 改为“助理主任（Assistant Director）”，或直接保留 `Assistant Director`；不需要外部资料替换原书信息 | **已关闭**：已改为“助理主任（Assistant Director）”；源码与 JSON 均复核通过 |

本轮未发现 P1/P2 级正文缺失、数学语义改变或目录条目遗漏。内容问题均已关闭；网页通过结论另以下述实际截图和交互检查为依据。

## 逐页内容核对

| PDF 页 | 原页内容 | 核对结果 |
|---:|---|---|
| 1 | 封面、水纹背景、英文书名与作者 | 原始图像完整，书名中文对应正确；译注见 FM-01 |
| 2 | Information Science and Statistics；3 位 Series Editors | 丛书名和 M. Jordan、J. Kleinberg、B. Schölkopf 均保留 |
| 3 | 丛书书目 | 12 条均保留，作者、书名、Vapnik 第二版信息完整；Wallace 书名疑点见下节 |
| 4 | 作者、扉页书名、Springer 标志 | 作者和书名完整，标志资产完整 |
| 5 | 作者与 3 位主编信息、地址、ISBN、出版/版权/印刷信息 | 邮箱、网站、图书馆控制号、两种 ISBN、地址、无酸纸声明、完整版权段、商标声明、KYO、印次数字和 springer.com 均保留；职衔见 FM-02 |
| 6 | 献辞、Jenna/Mark/Hugh、家庭照片与日全食说明 | 姓名、照片、Antalya/Turkey、2006-03-29 信息完整 |
| 7 | 前言 4 个正文段落及书籍网址 | 研究背景、读者对象/数学前置要求、参考文献范围、配套材料和网址完整，未发现语义偏差 |
| 8 | Exercises；Acknowledgements | 习题作用、1–3 星难度、www 解答规则、课堂实践、配套书/Matlab 信息及 4 段致谢均完整；图 13.1/12.17 和文献年份保留 |
| 9 | 书稿校阅者名单、妻子致谢、署名地点日期 | 名单逐名对照未发现遗漏；Chris Bishop、Cambridge、February 2006 完整 |
| 10 | 空白页 | 已确认原页空白，译稿保留源页标记，不需添加阅读正文 |
| 11 | 数学记号前 6 段与第 7 段前半 | 向量/矩阵、转置、区间、恒等矩阵、泛函、大 O、期望均对应原文；已知源书大 O 定义未被静默修订 |
| 12 | 期望段落续文、数据矩阵/数据向量记号 | 条件期望、方差/协方差、X 与两种 x 字体和 N/D 维数区分完整；跨页段落在生成 JSON 中合并并保留 `continuedPdfPages:[12]` |
| 13–20 | 全书原目录 | 逐页核对全部 285 个条目；章节、各节、习题、5 个附录、参考文献、索引和页码完整；详情见目录表 |

## 图像资产核对

| 输出资产 | 原页 | 已实际检查的内容 | 结果 |
|---|---:|---|---|
| `assets/frontmatter/cover.jpeg` | 1 | 书名、作者、水纹、版面边缘 | 完整；827×1126 |
| `assets/frontmatter/springer.jpeg` | 4 | 马头标志与 Springer 字样 | 完整；241×67 |
| `assets/frontmatter/eclipse-family.jpeg` | 6 | 4 人、海滩和日食观测眼镜等整幅照片内容 | 完整；472×707 |

这些是对应图像内容，未把原书正文页整页嵌入译文。卷首原页没有编号图、编号表、编号公式或程序代码块。

## 数学记号检查

- 译稿中 63 个数学片段均保留 TeX，生成 JSON 中均有可解析 MathML；本轮对全部 MathML 做了 XML 结构检查。
- 小写粗体罗马向量 `\mathbf{x}` 输出为 `mathvariant="bold"`；数据矩阵 `\mathbf{X}` 同样保留粗体罗马大写。
- 一维数据集合 `\boldsymbol{\mathsf{x}}` 输出为 `mathvariant="bold-sans-serif"`，与 D 维向量的粗体罗马 `x` 明确区分。
- 上标转置 T、行/列向量、区间端点、I_M 下标、泛函方括号、条件期望的条件竖线和 cov[x] 简写均已对照 PDF 11–12。
- 静态数据层面未发现数学字体或变量被合并的问题；浏览器是否按这些 MathML 字体变体显示，仍须实际网页验收。

## 目录核对

先逐页查看原目录，再把原页右栏页码序列与生成 JSON 逐项比较；下表所有条目数和页码序列一致。PDF 书签漏有第 7 章习题项，故不能仅以书签数量判定目录完整性；译稿保留了原目录中的该项（印刷页 357）。

| PDF 页 | 条目数 | 内容范围 | 页码序列 | 层级 |
|---:|---:|---|---|---|
| 13 | 23 | 前言、数学记号、目录、第 1 章和全部各节/习题 | 全部一致 | 原书层级已反映为 JSON depth 0/1/2 |
| 14 | 42 | 第 2、3 章及各节/习题 | 全部一致 | 同上 |
| 15 | 44 | 第 4 章、第 5 章至 5.4.3 | 全部一致 | 同上 |
| 16 | 43 | 5.4.4 起、第 6、7 章及习题 | 全部一致 | 同上 |
| 17 | 44 | 第 8、9 章、第 10 章至 10.2 | 全部一致 | 同上 |
| 18 | 44 | 10.2.1 起、第 11 章、第 12 章至 12.1.4 | 全部一致 | 同上 |
| 19 | 41 | 12.2 起、第 13、14 章、附录 A–C | 全部一致 | 同上 |
| 20 | 4 | 附录 D/E、参考文献、索引 | 全部一致 | 顶层加粗 |
| 合计 | **285** | — | **全部一致** | — |

目录翻译未发现改变原题所指概念的情况。后续章节完成后仍须做全书术语/题名一致性复核；例如“生成式模型”“逻辑回归”“维数灾难”等应与相应正文标题统一。

## 原书自身疑点（不记为译稿错误）

1. PDF 3 的 Wallace 书名原页确为 `Statistical and Inductive Inference by Minimum Massage Length`。现译稿保留该英文拼写，中文采用“最小消息长度”；与主 Agent 说明一致。本次没有引入外部版本或静默替换源书英文。
2. PDF 11 大 O 的定义确实把 `|f(x)/g(x)|` 写为有界。译稿忠实保留该式；本轮按唯一 PDF 依据核对，不把常见数学定义替换进正文。

## 网页证据与补充复核

集成负责人已运行 `tools/qa_reader.py`，报告位于 `reviews/reader-qa-frontmatter-preface-notation-contents.json`。reviewer 已读该脚本与报告，并独立查看 `tmp/prml-browser-qa/` 中全部 8 张截图。

| 检查范围 | 当前证据与结果 |
|---|---|
| 屏幕/主题 | 4 部分各测 1440px 桌面浅色、390px 窄屏深色，共 8 组 |
| 内容块 | frontmatter 37、preface 20、notation 9、contents 9；实际 `.reading-block` 数与 JSON 一致 |
| 图片 | 3 张图均成功 decode，未发现 figure-error；reviewer 已另外查看全部图像资产 |
| 数学 | notation 63 个 MathML 节点，未发现 formula-fallback；首屏截图中上下标/数学符号可读 |
| 页面宽度 | 8 组均为 `scrollWidth == pageWidth`，没有文档级横向溢出 |
| 浏览器异常 | 8 组报告的 `pageerror` 列表均为空 |
| 目录首屏 | JSON 的 depth 0/1/2 在桌面和窄屏截图中呈现不同缩进，标题及页码清楚可读 |
| 图色彩和深色模式 | 窄屏深色截图中的封面保持原色，没有反相损毁 |

初次检查仅有首屏截图，后来集成负责人补充了页面末段、图片与交互检查。reviewer 已查看新增的 10 张截图（4 部分末段及 Springer 标志，各两种视口），并复核数学字形修复后的 notation 末段截图。以下原缺口已关闭：

- [x] 数学记号末段的 `X`、无衬线粗体 `x` 与罗马粗体 `x` 在实际网页上同屏可辨。最终截图同时确认双线体期望符号 𝔼；构建器保留原 TeX，使用准确的 Unicode 数学字形避免浏览器忽略 mathvariant。
- [x] frontmatter 下方的 Springer 标志和献辞照片在桌面/窄屏深色中的实际布局。新增 `frontmatter-publisher-*.png`、`frontmatter-end-*.png` 显示完整图像、图注，颜色未反相。
- [x] 章内目录点击后目标进入视口。`qa_reader.py` 现在等待 hash 与目标位置，窄屏目录点击后也确认弹层关闭。
- [x] 阅读进度更新与重新加载后的恢复。脚本滚到末块，核对 localStorage 的章节与块标识，再移除 hash 重载并确认末块进入视口。

新增依据为 `reviews/reader-qa-frontmatter-preface-notation-contents-chapter-01.json`（10 组基础检查）与最终字形版 `reviews/reader-qa-notation-chapter-01.json`（4 组，其中数学记号 2 组）。后者记录数学记号两种视口均恢复到 `read-p02-b002`，各有 63 个 MathML、无文档横向溢出和浏览器异常。最终 `notation.json` 的原始文件 SHA-256 为 `b4fdbddc583b9f31a66568b5b35bade6d114c65adbe23a964d209c192b6f097f`。此处哈希用于记录被审内容快照，不阻止集成负责人随后仅更新审核状态元数据。

## 验收与后续

- [x] 未参与初译的 reviewer 对 PDF 1–20 逐页核对。
- [x] 4 份译稿逐段核对，3 个图像资产实际查看，全部 285 条目录核对。
- [x] 数学字体/上下标及生成 MathML 数据检查。
- [x] FM-01 修复并独立复核。
- [x] FM-02 修复并独立复核。
- [x] 修复后重新构建，核对最新 JSON 与源稿一致。
- [x] 8 组网页首屏、主题、图片加载、MathML 数量与文档级溢出检查；reviewer 独立查看截图。
- [x] 集成负责人补充上节 4 项显示/交互证据，reviewer 复核。
- [x] 全部待办关闭，更新本记录的最终通过结论。

**最终结论：卷首 4 部分独立审查通过。PDF 1–20 的正文、3 张图像、63 个数学片段及全部 285 条目录项已核对；2 项修订与 4 项网页证据缺口均已关闭，没有未解决的卷首审查问题。全书完成后仍须检查目录与后续章题、跨章术语和引用的一致性。**
