# 参考文献 a 作者自检记录

范围：PDF 物理页 731–738。仅初译与作者自检，不代表独立审查或整章验收。

## 任务清单

- [x] 检查当前工作区状态及文件所有权；不修改其他作者或共享文件。
- [x] 阅读原页预读基线并与 b 确认 738/739 为完整条目边界。
- [x] 实际查看 731–732；核对双栏顺序、条目字段及中文题名。
- [x] 实际查看 733–734；核对双栏顺序、条目字段及中文题名。
- [x] 实际查看 735–736；核对双栏顺序、条目字段及中文题名。
- [x] 实际查看 737–738；核对双栏顺序、条目字段及中文题名。
- [x] 逐条复核作者、原题、年份、卷期页码、出版信息及特殊字形。
- [x] 检查页标、跨页接续、条目计数与最终 SHA-256，交接独立审查。

## 边界与格式

- 页 731 首条为 Abramowitz / Stegun (1965)，页 738 末条为 Ito (1991)。
- 原书每页先读左栏再读右栏；跨栏续条仍为同一条。
- Attias (1999b) 跨 731/732，使用同类 reference-entry 段落与 join-previous-paragraph-with-space。
- 738/739 不跨条、不使用 join；b 页 739 从 Jaakkola / Jordan (2000) 开始。
- 仅一个“参考文献”标题，不增导读或小节；保留原题并在其后给出中文题名。

## 计数及原页核对

- 实际查看 PDF 731–738 的全部双栏内容，逐条读完后直接翻译题名；本分片确认 183 个完整条目，与原页基线候选数一致。原页 2 倍渲染图保存在 `tmp/prml-refa/page-731.png` 至 `page-738.png`。
- Bishop / Nabney (2008) 的 In preparation 按原书历史状态保留。

| PDF 物理页 | 左栏起点 | 右栏起点 | 新条目数 | 首／末新条目 |
| --- | ---: | ---: | ---: | --- |
| 731 | 8 | 8 | 16 | Abramowitz / Stegun (1965)／Attias (1999b) |
| 732 | 11 | 12 | 23 | Bach / Jordan (2002)／Besag 等 (1995) |
| 733 | 12 | 8 | 20 | Bishop (1991)／Bishop / Tipping (1998) |
| 734 | 12 | 14 | 26 | Bishop / Winn (2000)／Chen 等 (1991) |
| 735 | 12 | 15 | 27 | Choudrey / Roberts (2003)／Duda / Hart (1973) |
| 736 | 12 | 13 | 25 | Duda 等 (2001)／Gallager (1963) |
| 737 | 11 | 12 | 23 | Gamerman (1997)／Gull (1989) |
| 738 | 12 | 11 | 23 | Hassibi / Stork (1993)／Ito (1991) |

- 732 顶部另有 Attias (1999b) 续条，不重复计数。733 的 VIBES 条目、738 的 Hinton 等 (2001) 条目跨左右栏，均连成完整同一条。
- 每条逐项核对作者及顺序、年份与字母后缀、原题、中文题名、编辑者、书刊及会议录名、卷／期／页码、版次、出版社、地点、报告或学位信息、转载及历史状态；没有新增原书未印的字段。

## 已核原印疑点

- 732：Attias (1999b) 续条的会议名称确为 Fifth Conference；Besag (1995) 的两位作者原印确为 D. Hidgon、K. Megersen。均按原印保留。
- 733：Bishop / Nabney (2008) 的 In preparation 完整保留；Bishop 等 (1997a) 编辑者原印 T. Petche，不改作其他条目的 Petsche。
- 734：Blei 等 (2003) 编辑字段原印 J. M. B. et al. (Ed.)；Box / Tao (1973) 原印 Tao；Cardoso (1998) 原印卷期 9(10)。均不按外部书目信息更正。
- 735：Csiszàr / Tusnàdy 两处 à 的原印均为重音符（grave accent），已实际查看 4 倍局部；不换成通常见到的 á。该页 Dawid (1979) 原印卷号 4、Cover / Hart (1967) 原印 IT-11，均保留。
- 736：Feynman 等 (1964) 题名原印 The Feynman Lectures of Physics；Frey / MacKay (1998) 编辑者原印 M. J. Kearns，且未印页码，均保留。
- 737：Ghahramani / Jordan (1994) 题名原印 appproach（三个 p）；Golub / Van Loan (1996) 出版社原印 John Hopkins University Press；Gibbs (1997) 原印 Phd thesis。均按源保留。
- 738：Hastie / Stuetzle (1989) 卷期原印 84(106)；Hodgson (1998) 期刊名原印 Remote Sensing of Environments（复数）；Hojen-Sorensen 姓名按源不加额外变音符号。

## 原书强调格式

- 依集成者纠正的格式要求，论文题名一般正体，书名/期刊名/会议录名按源使用斜体；卷号逐项按源保留粗体，不将所有题名一律斜体。
- 每页原图已实际查看，另以 PDF 字体字典辅助逐字符检查 Times-Italic / Times-Bold；此辅助不替代对源页的阅读。
- 731–738 英文字段与 PDF 文本的逐字符比对仅有原页断词、连字和变音符号重组差异；不以提取差异自行更改原印内容。736 的 Elkan 题名中 k 为 CMMI 数学斜体，正文保留其斜体。

## 作者结构自检与最终交接

- 仅通过构建器的 `render_chapter` 解析本分片到临时目录，未写共享文件、章节 JSON 或全书清单。
- 8 个连续页标；源码 184 个 reference-entry 段落，跨页合并后为 183 条；183 个中文题名；仅 1 个 H1，无额外导读、小节、图片或公式。
- 182 个 em 强调段与 88 个 strong 强调段在解析前后数量相同；183 条的全部文本与渲染结果逐条完全一致。
- Attias (1999b) 合并为一条，`pdfPage=731`、`continuedPdfPages=[732]`，编辑者之后与会议录名称之间保留空格。
- 作者核对清单：`tmp/prml-refa/entry-checklist.json`；结构结果：`tmp/prml-refa/qa-summary.json`；临时解析结果：`tmp/prml-refa/rendered-part.json`；字体／字符对照辅助：`tmp/prml-refa/source-emphasis-alignment.json`。
- 最终源码 raw SHA-256 与 LF SHA-256 相同：`541c4ef760046754b4a5f1903b69829afa57bb1a90252085be807addf9b9f18e`。
- 根 Agent 已反馈对全部 183 条原页、字段、译题及强调的独立复核无待修项；此记录只交付稳定分片及作者自检，整体合并与网页验收由集成者另行登记。

## RA-01 术语修复交接

- 独立审查要求将 PDF 731 Adler (1981) 译题中的“用超松弛方法”统一为第 11 章及 Neal (1999) 条目使用的“用过松弛方法”。已按要求完成，仅替换该词，其他源码字节及格式均未改动；修复前后文件长度均为 44290 字节。
- 修复前 SHA-256：`541c4ef760046754b4a5f1903b69829afa57bb1a90252085be807addf9b9f18e`。
- 修复后当前 raw / LF SHA-256：`e4d0f1bdfacb09c855edbd8bcc4d981d665ca784005dca4fa8eea6ced0b1120e`。
- 临时作者 QA 保存的是修复前结构快照；本次术语替换不改变条目、页码或任何标记，独立修复复核及两模式网页检查由集成者登记。
