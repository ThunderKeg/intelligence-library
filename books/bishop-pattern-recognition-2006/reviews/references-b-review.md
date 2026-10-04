# 参考文献 b 分片独立审查

状态：**独立审查通过，结合 root 的 a/UI 报告，参考文献可登记验收。** 本 reviewer 未参与初译，负责 PDF 739–748 的全部条目、源页字体/格式、中文题名与整合 JSON；root 负责 a 分片 PDF 731–738 和整部分网页审查。只以原 PDF 为正文依据，文本提取和作者/基线记录仅用于定位。本报告明确引用 root 的独立网页检查，不冒称由本人重复实看其全部截图，也不直接更改验收状态。

- [x] 逐页实际查看 739–748，按左栏→右栏核对每条作者、年份、题名、编者、出版信息和原排版。
- [x] 核对全部中文题名及跨章术语，登记问题并完成 RB-01/02 修复复核。
- [x] 核对四组 b 内跨页条目接续及 a/b 边界。
- [x] 接收作者最终稳定版本并复核修改、源稿和格式指纹。
- [x] 对整合 JSON 检查条目顺序、内容和强调样式守恒，形成正式结论。

## 逐页进度

| PDF 物理页 | 实际新条目数（左/右） | 人工核对状态 |
|---|---:|---|
| 739 | 13/12 | 25 条逐项核对完成 |
| 740 | 12/10 | 22 条逐项核对完成，Le Cun (1990) 跨页 |
| 741 | 13/12 | 25 条及上页续文核对完成 |
| 742 | 12/12 | 24 条逐项核对完成 |
| 743 | 12/12 | 24 条逐项核对完成，RB-01 已关闭 |
| 744 | 11/13 | 24 条逐项核对完成，Roth (2000) 跨页 |
| 745 | 10/12 | 22 条及上页续文核对完成，Simard (1993) 跨页 |
| 746 | 10/11 | 21 条及上页续文核对完成，Tino (2001) 跨页，RB-02 已关闭 |
| 747 | 10/13 | 23 条及上页续文核对完成 |
| 748 | 11/4 | 15 条逐项核对完成 |

## 问题台账

| 编号 | 精确位置与发现 | 限定修复建议 | 状态 |
|---|---|---|---|
| RB-01 | PDF 743，`translation/parts/references-b.md:251`，Platt (1999) 中文题名写“序列最小优化”，与第 7 章 7.1.3 的同一 SMO 算法“序贯最小优化”不一致。 | 仅中文题名“序列最小优化”→“序贯最小优化”；英文题名和书目字段不变。 | 已修复，独立检查最终词语及反向字节差异后关闭 |
| RB-02 | PDF 746，Simard et al. (1992) 中文题名写“切线传播”；第 5 章 5.5.4 标题/正文均用“切向传播”，并直接引用此文献。 | 仅“切线传播”→“切向传播”；英文 Tangent prop 与其他字段不变。 | 已修复，独立检查最终词语及反向字节差异后关闭 |
| RA-01（整合中发现，a 负责） | PDF 731，`translation/parts/references-a.md:7`，Adler (1981) 中文题名用“超松弛”，与第 11 章直接引用此文献的“过松弛”和 b 的“有序过松弛”不一致。 | 仅“用超松弛方法”→“用过松弛方法”；交 root/a 复核原分片。 | root 已反向字节复核并更新 a 独审附记；本人核最终源稿与该快照一致，且 JSON 对应词语正确，内容关闭 |

## 已完成的源页核对

本人实际逐张打开 `tmp/prml-root-review/appendix-references/page-739.png` 至 `page-748.png` 十张原页，并查看 738 末尾接口；逐条按左栏到右栏阅读。共 225 条新书目、229 个页内段，额外四段为跨页续文，不算新增条目。全部作者顺序、首字母、年份后缀、英文题名及其中文译名、书刊/会议/编者、卷期、页码、出版社、版次、报告号、学位机构、转载和历史出版状态均已对照原页核查。225 个题名加 Nilsson 的重印书名，中文译题共 226 组。无图片、公式、表格或脚注。

四组跨页书目分别为 Le Cun/Denker/Solla (1990) 740→741、Roth/Steinhage (2000) 744→745、Simard/Le Cun/Denker (1993) 745→746、Tino/Nabney/Sun (2001) 746→747；每条的后续编辑者/会议录/卷页/出版社完整。738 末 Ito (1991) 已结束，739 首 Jaakkola/Jordan (2000) 是新条目，分片接口无需合并。

作为人工核查的补充，独立从 PDF 字体跨度提取原字符，按页左栏→右栏串接，与移除新增中文译题后的 HTML 原文比对。NFKD 归一、去掉空白/标点/组合音调后的 24847 个字母和数字逐页顺序相等；相同字符的正体/斜体/粗体属性逐一相等，没有用整页字符数代替内容比对。该辅证不覆盖标点和音调本身，因此这些仍按原页实际阅读核对。证据为 `tmp/prml-review/references/english-content-comparison.json` 和 `english-font-comparison.json`。

已实际辨明的原印细节保留：739 Jeffries / Pro. Roy. Soc. AA、Russel；740 Kschischnang / probabailities；742 Ppropagation、Moore 的 hierarch；743 Neal (1997) 的 Computer Statistics；745 Seeger 的 Edinburg；746 Stinchecombe / mamograms / Americal；747 Tipping/Bishop (1999b) 的卷号 21。Föglein、Sjölander、Kůrková、Lütkepohl、Rätsch、Møller、Müller、É、Quiñonero-Candela、Svensén、Sankhyā 的字形按页保留；Le Cun/LeCun、Nystrom 不以外部常见写法替换。

历史信息（Jordan 2007 In preparation、Kuss 2006 in press、MacKay 1997 Unpublished manuscript、Teh 2006 to appear）、重印信息和 Shannon 的两个页码区间完整。字体并非机械按文献类别统一：如 Møller 的学位论文题名原为正体，依原页保留；期刊卷号与会议 Volume 字段的字体差异也保留。

## 最终 b 源稿指纹

已实际复核两项修复，反向替换后字节完全恢复先前审过的 `5bcd50d22d46ec925657854aa137ffec8d5627ea67be403cd4146e0bf9c92915`，没有英文、出版字段或格式变更。最终原始字节 SHA-256：`7b0777811a5b4df96bf9d59c1f84def4c2a2d96fdb5d7aeb0cc7bfd628468808`。快照 `tmp/prml-review/references/reviewed-b-final.md`，差异证据 `RB01-RB02-diff.json`，十张整页和一张接口页的实际查看指纹 `source-pages-viewed.json`。

## 整份 JSON 独立核验

已阅读 `references-a-review.md` 的 a 内容结论及 RA-01 附记，当前 a 源稿与 root 最终审过快照逐字节相同。b 源稿与本人最终快照相同。本人独立解析每个页内 HTML 段及跨页 join 指令，得到 183+225=408 条书目；它们与合并源稿的条目数组完全相等。再与最终 JSON 按顺序逐条比对，**408 条正文 HTML（含标点、中文译题、em/strong 标签）及 PDF 页归属全部相等**，不是仅比字符总量。空白做排版归一，不丢弃标点或强调。逐条内容/格式指纹在 `tmp/prml-review/references/all-408-entry-content-and-format.json`。

最终 409 根块为 1 标题加 408 富文本书目；397 个 em、178 个 strong 全部保存，409 组中文题名包含 Nilsson 的重印书名。每条仍是独立 `p.reference-entry`，没有新增图片、公式、脚注或代码。头条 Abramowitz/Stegun (1965)、a/b 边界 Ito→Jaakkola、末条 Zarchan/Musoff (2005) 顺序正确。RA-01/RB-01/RB-02 三处最终词语均已在 JSON 中检查。

五条跨页接续均完整，条目不重复：`p01-b017`→732、`p10-b022`→741、`p14-b024`→745、`p15-b023`→746、`p16-b022`→747。实际阅读生成后的五条完整 HTML，编辑者名字没有粘连，会议录/页码/出版商没有丢失。复查脚本与统计结果在 `tmp/prml-review/references/verify_integration.py` 和 `integration-verification.json`。

| 项目 | SHA-256 |
|---|---|
| a 原始字节 / LF（RA-01 后） | `e4d0f1bdfacb09c855edbd8bcc4d981d665ca784005dca4fa8eea6ced0b1120e` |
| b 原始字节 | `7b0777811a5b4df96bf9d59c1f84def4c2a2d96fdb5d7aeb0cc7bfd628468808` |
| b LF | `6c5356c1ed501f42f8b7c25022f5c91d23eaca2eb1c04fef4a29cd289165ff66` |
| 合并稿原始字节 | `8b0377b11acbdb35283b9365d55d5098e3a11df9ddf55fba761867f8b7fa26d2` |
| 合并稿 LF | `c6a0bc7e658e0d68579b1cedd92ce67201ef44ea255ecae28c57bad9886959fd` |
| 渲染内容 | `e46361ad8d8ede4b6a7dbbfa5ff4a91ff3b546de3807613c37c3537491add4ac` |
| 空图片集合 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

本 reviewer 负责的 b 全部内容和整份生成内容均通过，没有遗留内容问题。整份参考文献由 root 结合 a 独审及其独立网页检查记录登记验收。a/b 译题分别置于英文句点后/前的呈现差异已告知 root，留全书格式评估；它没有改变英文原题或漏译题名，不作本次内容阻塞。

## 网页独审证据与整体验收结论

已完整阅读 root 的 `references-ui-review.md` 与 `reader-qa-referencesfinal.json`。root 未承担参考文献初译，实际逐张看过 54 张初始截图和 RA-01 后 2 张增量，共 56 文件版本，覆盖 18 页首条、5 条跨页书目、末条和基本阅读流程。本人逐项复算 `viewed-ui-history.json` 的 56 个文件 SHA，全部与其查看记录相同；验证记录在 `tmp/prml-review/references/root-ui-proof-verified.json`。这里采用 root 的独立目视结论，没有声称本人也打开了 56 张图。

两种屏幕的 408 条书目、悬挂缩进、原斜体/粗体和变音字形、长条目换行及末尾进度保存/无 hash 恢复均通过。书目本身无公式、图片或章内二级标题，因此公式引用和目录项落点测试不适用，未把 false/null 当作已执行。索引下一章链接等待 25 单元最终集成时检查，不属于本部分译文缺失。

结合 root 的 a 原页独审、本人 b 全部原页独审、408 条精确内容/强调守恒以及 root 的独立网页审查，最终表中所列版本可登记为参考文献已验收。RA-01、RB-01、RB-02 均已修复复核，无遗留内容或布局问题。
