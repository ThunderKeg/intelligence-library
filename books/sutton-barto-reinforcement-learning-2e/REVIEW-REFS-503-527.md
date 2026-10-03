# 参考文献 PDF 503–527 页独立审查记录

- 审查日期：2026-10-03。
- 审查者：未承担本段初编的独立 Agent。
- 原文依据：仓库中的《Reinforcement Learning: An Introduction》第二版 PDF 物理页 503–527（印刷页 481–505）。逐页查看原页图像；PDF 文本提取仅用于定位和逐字符辅助比对，遇到歧义以原页图像为准。
- 审查对象：`backmatter/references/page-503.md` 至 `page-527.md`，共 25 个页稿、517 条参考文献。
- 当前结论：**通过。** F01 已按原页修复并独立复核。

## 逐页核对

| PDF 物理页 | 条目数 | 范围与重点 | 结果 |
| --- | ---: | --- | --- |
| 503 | 17 | Abbeel–Anderson；题名、卷页、DOI、An 等的 URL | 已核 |
| 504 | 21 | Anderson–Baras；会议、技术报告、ArXiv 编号 | 已核 |
| 505 | 19 | Barnard–Barto；Barto 同姓多条、年份后缀与卷页 | 已核 |
| 506 | 20 | Barto–Bellman；作者、书名、报告号、页码 | 已核 |
| 507 | 24 | Bengio–Blodgett；Bertsekas 多条、卷期页码 | 已核 |
| 508 | 20 | Boakes–Brown；Boakes 题名 F01、时序差分文献与图书信息 | 已核；F01 已关闭 |
| 509 | 20 | Bryson–Ciosek；作者变音符号、TD(λ)、ArXiv 号码 | 已核 |
| 510 | 21 | Claridge-Chang–Dann；跨行题名、期刊卷页 | 已核 |
| 511 | 22 | Daw–Deutsch；三个 λ 符号、年份与卷页 | 已核 |
| 512 | 20 | Deutsch–Duda；会议题名、出版社、ArXiv 编号 | 已核 |
| 513 | 24 | Duff–Geist；期刊题名、年份、卷期与页码 | 已核 |
| 514 | 22 | Gelly–Gordon；Gordon（2001）条目跨至下一页 | 已核 |
| 515 | 19 | Gordon（2001）续接后 Graybiel–Hare；卷页与报告号 | 已核 |
| 516 | 22 | Harth–Hollerman；原书题名拼写异常见下文 | 已核 |
| 517 | 22 | Houk–Kaelbling；作者变音符号、Jaderberg 年份见下文 | 已核 |
| 518 | 22 | Kakade–Klopf；符号、ArXiv 号码、卷页 | 已核 |
| 519 | 20 | Klyubin–Kushner；作者与年份、会议及图书信息 | 已核 |
| 520 | 21 | Kuvayev–Liu；带连字符的题名、卷页 | 已核 |
| 521 | 20 | Ljung–Mahadevan；GQ(λ)、Mahadevan 与 Connell（1992）跨页 | 已核 |
| 522 | 20 | 上页条目续接后 Mahmood–Mendel；卷页与 ArXiv 号码 | 已核 |
| 523 | 19 | Mendel–Monahan；书名、报告、Atari 文献 | 已核 |
| 524 | 20 | Montague–Narendra；作者、年份、卷页 | 已核 |
| 525 | 20 | Narendra–O’Reilly；带重音的姓名、卷页 | 已核 |
| 526 | 21 | Omohundro–Peng；会议、技术报告、DOI、卷页 | 已核 |
| 527 | 21 | Peng–Precup；年份后缀、题名及末条出处 | 已核 |

## 发现与处理

| 编号 | 等级 | 位置 | 问题、依据与状态 |
| --- | --- | --- | --- |
| F01 | 文字忠实度 | `page-508.md`，Boakes, R. A., Costa, D. S. J. (2014) | PDF 原页题名在冒号后印作 **“Iinterference and decay from an historical perspective”**（多一个大写 `I`）；初稿静默改为 **“Interference and decay from an historical perspective”**。高分辨率原页确认这是原书自身的排印错误。主 Agent 已将页稿恢复为 `Iinterference`；再次对照原页和条目全文复核一致，F01 已关闭。 |

## 原书自身的异常

- PDF 物理页 508 的 Boakes 与 Costa（2014）题名多印了一个大写 `I`，对应 F01。这里记录原书错误，不推断该论文的正式发表题名。
- PDF 物理页 516 的 Hollerman 与 Schultz（1998）题名印作 “Dopmine neurons report an error …”（`Dopmine` 少 `a`）。`page-516.md` 如实保留，不属于页稿错误。
- PDF 物理页 517 的 Jaderberg 等 “Reinforcement learning with unsupervised auxiliary tasks” 标注为 **2016**；原书第 17 章书目注释（印刷页 478）却引用 Jaderberg 等 **2017**。参考文献页稿保留原书的 2016；这是原书内部年份不一致，不能为求统一擅改。

## 完整性与格式核对

- 按原页逐条核对作者次序、年份及后缀、英文题名、期刊或会议名、卷期页码、出版社、报告号、ArXiv 编号、DOI 与 URL。517 条的分段数量与 PDF 中的条目起始数逐页一致；页首 `References` 译为“参考文献”，不算文献条目。
- PDF 物理页 514–515 的 Gordon（2001）和 521–522 的 Mahadevan 与 Connell（1992）跨页续段，在前一页页稿中合成完整条目，后一页从下一条开始，无重复或丢失。PDF 物理页 527 的末条 Precup 等（2001）已在本页结束。
- 抽取文本中的 `↵`、`✏` 等连字替代符以及未识别的 `λ`，已回看原页；页稿在 Duff、offline、TD(λ)、SARSA(λ)、GQ(λ) 等位置采用原页可见的正确字形。行末断词产生的连字符歧义，也以原页与条目题名核对。姓名中的变音符号按原页保留。

## 最终复核

已重新核对 PDF 物理页 508 的 Boakes 条目、页稿拼写及上下文。F01 已关闭；PDF 物理页 503–527 的参考文献独立审查**通过**。
