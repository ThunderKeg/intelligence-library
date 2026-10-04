# 《Information Theory, Inference, and Learning Algorithms》翻译编撰任务

唯一正文依据：仓库根目录同名 PDF；David J. C. MacKay，Version 7.2（fourth printing，2005-03-28）。PDF 共 640 物理页。本清单页码均为 PDF 物理页；印刷正文页码 +12。PDF 第 3–4 页目录已目视核对。

勾选只表示对应事项已完成并有可检查的译稿或审查记录；未勾选事项仍未完成。前置内容、第 1–50 章、相关导页、前七部分扉页、附录 A–C、参考文献、索引及 PDF516 独立后记已通过独立原页与站点审查，并完成本地正式路径验收（至 PDF640）。第 4 章 PDF86 脚注修复后的独立回归见 `translation/FORMAT_REGRESSION_QA.md`。本地正式构建的全书一致性、站点与离线总审均已通过，见 `translation/GLOBAL_REVIEW.md` 与 `INTEGRATION_QA.md`。

## 全书任务

- [x] 逐页核对前置内容、50 章、分部页、附录 A–C、参考文献和索引；各单元 `REVIEW.md` 与全书 `translation/GLOBAL_REVIEW.md` 留存原页核验。
- [x] 建立每章小节、图表、公式、代码、习题、答案与交叉引用台账；逐章清单和 `tools/verify_book_static.py` 可复查。
- [x] 由不同于初译者的 Agent 逐章独立审查、记录并修复问题；索引全书术语增量修订另由非初译 Agent 复核。
- [x] 全书跨章术语、符号、编号、链接、目录、阅读进度、窄屏、深色模式和离线阅读复审通过；原书两处内部疑点按印本保留，见 `translation/GLOBAL_REVIEW.md`。

## 全书一致性总审进展

- [x] 81 个正式阅读单元按原书顺序唯一覆盖 PDF1–640；目录、静态链接、图片清单和断网阅读均经独立核验，见 `translation/OFFLINE_QA.md`、`INTEGRATION_QA.md`。
- [x] 第 9、17 章题名与导航一致；中段进度连续刷新及 320px 技术词断行问题已修复并由独立 Agent 在六视口复测，见 `translation/GLOBAL_TITLE_SITE_QA.md`。
- [x] 建立 2747 个可点击编号目标；正文与附录的 1528 处图、表、算法、习题和公式编号提及，仅原书悬空的式 (16.5) 留为普通文字。印本“表 4.10／图 30.1”别名已指向真实原图／算法；独立 Agent 抽验正式跳转，见 `translation/GLOBAL_REVIEW.md`。
- [x] 第 16、25、31、43、47 章的和积算法、信念传播与 Gibbs 采样术语已定点修订；不同 Agent 对可视原页、新旧 JSON 差异和正式站点复核通过，见 `translation/GLOBAL_REVIEW.md`。
- [x] 前置目录 22 个中文章名和第 11 章路线图术语已与正文统一；50/50 章名与印刷页码经不同 Agent 对 PDF3–10 和正式站点复核通过。
- [x] PDF6–10 路线图第 25 章六处“格形图”及另外 17 个同英文章名的 106 处中文标签已与正文统一；50/50 章框已程序比对，仅原书有意缩写的 12、17、19、34 章保留短名。不同 Agent 对原图和正式站点六视口增量复核通过；320px 章名与术语不拆词，短尾和整页横溢为零，见 `translation/GLOBAL_REVIEW.md`。
- [x] 索引七处和积算法／Gibbs 采样术语已重建；非初译 Agent 对原页、旧版差异及正式六视口复核通过，1599 词项和全部页码／参见链接保留，见 `translation/index/REVIEW_TERMS_2026-10-04.md`。
- [x] 完成上述修订的最终静态、站点、离线回归与全书总审签结；结论限本地正式构建，见 `INTEGRATION_QA.md`、`translation/GLOBAL_REVIEW.md`。

## 小节定位说明

下方小节名称和起始页最初由原 PDF 文字层提取，仅用于定位；各章已按可视原页核对标题、无编号小节、图、表和公式。缺号不等于原书没有，文字层检测也不能代替逐页图像盘点。逐页条目保留初译阶段的工作记录；当前完成状态以勾选、章末验收条目及对应审查记录为准。

## 前置内容

- [x] 封面、题名与版本页（PDF 1–2）；见 `front-matter/page-01.md`–`page-02.md`、`front-matter/REVIEW.md`。
- [x] Contents（PDF 3–4）：建立中文目录并核对层级。
- [x] Preface（PDF 5–12）：全文、About the exercises、Acknowledgments；F1、F2 已修复并复核。
- [x] About Chapter 1（PDF 13–14）：全文、Figure 1.1–1.3、式 (1.1)–(1.17) 和例题。
- [x] 前置内容站点验收：F3 已由独立 Agent 在手机深色模式复核；17 式、10 图、路线图平移、目录及正式路径见 `front-matter/REVIEW.md` 与 `INTEGRATION_QA.md`。

## 第 1 章：Introduction to Information Theory（PDF 15–33）

- [x] PDF15–17：章导读、1.1 全节和 1.2 开头、四种信道示意、图 1.4–1.6／1.8 与表 1.7 已完成独立原页及站点审查。
- [x] PDF26–27：图 1.18–1.19、习题 1.9–1.11、1.3 全节和 1.4 开头已完成独立原页及站点审查。
- [x] 初译页 PDF 18–25、28–33，合并后逐页核对跨页段落、图表、公式与编号；见 `translation/chapter-01/REVIEW.md`。
- [x] 编写本章简短中文导读，与原书正文区分；站点已将香农题辞置于导读框外。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、答案与参考文献；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；逐节翻译并核对段落和无编号小标题，见 `translation/chapter-01/REVIEW.md`。
  - [x] 1.1 How can we achieve perfect communication over an imperfect, noisy communication channel?（PDF 15 起）
  - [x] 1.2 Error-correcting codes for the binary symmetric channel（PDF 17 起）
  - [x] 1.3 What performance can the best codes achieve?（PDF 26 起）
  - [x] 1.4 Summary（PDF 27 起）
  - [x] 1.5 Further exercises（PDF 28 起）
  - [x] 1.6 Solutions（PDF 28 起）
- [x] 逐项核对图片、图内英文、图注、表格每个单元格并登记编号与页码；图 1.17 已重裁，表 1.14 的 16 个码字复算无误。
- [x] 原页核对图 1.4–1.22、表 1.7／1.14 及未编号对象的实际出现、图内文字、表格单元格与编号，见 `translation/chapter-01/REVIEW.md`。
- [x] 对照 PDF 核对式 (1.18)–(1.60) 共 43 个编号、变量、上下标、算法和代码；网站 MathML 可读可复制，经独立验收。
- [x] 原页核对式 (1.18)–(1.60) 的连续编号、无编号式及算法代码，见 `translation/chapter-01/REVIEW.md`。
- [x] 核对本章术语、原书交叉引用、目录、窄屏和深色模式排版；站点 S1–S4 已独立复测通过。
- [x] 不同于初译者的 Agent 独立审查并记录问题；C1 初审误判已纠正，C2、C3 修复后复核通过。
- [x] 修复审查问题并复核，完成本章原页内容、草稿站点与正式本地路径验收；见 `translation/chapter-01/REVIEW.md`、`translation/chapter-01/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 2 章：Probability, Entropy, and Inference（PDF 34–58）

- [x] 初译 PDF 34–46；逐页译稿、图 2.1–2.8 的已出现图号、表 2.9、框 2.4、式 (2.1)–(2.46) 和代码串已核对。
- [x] 初译 PDF 47–49；2.7、2.8 前半及图 2.10–2.11、页边重心图、式 (2.47)–(2.54) 已按原页核对。
- [x] 初译 PDF 50–58；2.8 后半、2.9、2.10 及余下图表、式 (2.55)–(2.113)、习题和解答已按原页核对。
- [x] 编写本章简短中文导读，与原书正文区分；整章排版已独立审查。
- [x] 逐节逐段翻译并由独立 Agent 对照 PDF 34–58 核对正文、列表、脚注、习题、答案与参考文献；见 `translation/chapter-02/REVIEW.md`。
- [x] 核实以下小节标题、起始页及层级；逐节译文和无编号小标题已核对。
  - [x] 2.1 Probabilities and ensembles（PDF 34 起）
  - [x] 2.2 The meaning of probability（PDF 37 起）
  - [x] 2.3 Forward probabilities and inverse probabilities（PDF 39 起）
  - [x] 2.4 Definition of entropy and related functions（PDF 44 起）
  - [x] 2.5 Decomposability of the entropy（PDF 45 起）
  - [x] 2.6 Gibbs’ inequality（PDF 46 起）
  - [x] 2.7 Jensen’s inequality for convex functions（PDF 47 起）
  - [x] 2.8 Exercises（PDF 48 起）
  - [x] 2.9 Further exercises（PDF 50 起）
  - [x] 2.10 Solutions（PDF 52 起）
- [x] 逐项核对图片、图内英文、图注、表 2.9 的 27 行全部单元格；13 张图像资产均有引用。
- [x] 原页核对图 2.1–2.13、表 2.9 和未编号对象的实际出现、图内文字、全部 27 行单元格与编号，见 `translation/chapter-02/REVIEW.md`。
- [x] 对照 PDF 核对式 (2.1)–(2.113) 连续编号、变量与上下标，300 位代码串逐位一致；网站 MathML 可读可复制，经独立验收。
- [x] 原页核对式 (2.1)–(2.113) 的连续编号、无编号式和代码，见 `translation/chapter-02/REVIEW.md`。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版；见 `translation/chapter-02/REVIEW.md`、`SITE_QA.md`。
- [x] 不同于初译者的 Agent 独立审查并记录问题；式 (2.56) 的近似号已修正、复核通过。
- [x] 修复框 2.4 和习题 2.28 图注的站点问题，独立复测后完成本章正式路径验收；见 `translation/chapter-02/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 3 章导页（PDF 59）

- [x] PDF 59 独立导页已完成初译：`translation/chapter-03/about-chapter-03/pdf-059.md`，衰变窗口图见 `assets/chapter-03/`；初译不代表验收完成。
- [x] 由未参与初译的 Agent 对照原 PDF 独立审查 “About Chapter 3” 全文、习题 3.1–3.4、表格、衰变示意图、公式与译注；源内容通过，见 `translation/chapter-03/about-chapter-03/REVIEW.md`。
- [x] 导页草稿站点独立审查通过，正式注册后与第 2、3 章之间的真实路径、图像及进度复核通过；见 `translation/chapter-03/about-chapter-03/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 3 章：More about Inference（PDF 60–76）

- [x] 编写本章简短中文导读，与原书正文区分；见 `translation/chapter-03/pdf-060.md` 与独立 `REVIEW.md`。
- [x] PDF 60–76 的逐页译稿已由不同 Agent 对照原页检查正文、列表、脚注、习题和原书解答；R3-01／R3-02 修复后复核通过。
- [x] 核实以下小节标题及起始页；逐节译文与无编号小标题已由独立 Agent 核对。
  - [x] 3.1 A first inference problem（PDF 60 起）
  - [x] 3.2 The bent coin（PDF 63 起）
  - [x] 3.3 The bent coin and model comparison（PDF 64 起）
  - [x] 3.4 An example of legal evidence（PDF 67 起）
  - [x] 3.5 Exercises（PDF 69 起）
  - [x] 3.6 Solutions（PDF 71 起）
- [x] 图 3.1–3.4、3.6–3.12、表 3.5 与图内译注由独立 Agent 对照原页复核；图 3.5 在原书中不存在。
- [x] 核对本章图表编号：图 3.1–3.4、3.6–3.12 共 11 幅，表 3.5 一张；未把表误作图。
- [x] 对照 PDF 核对式 (3.1)–(3.47) 的编号、变量与上下标；独立草稿站点排版审查及正式路径验证通过。
- [x] 式 (3.1)–(3.47) 共 47 个编号各出现一次；无编号式与正文数学表达式已逐页核对。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版；见 `translation/chapter-03/REVIEW.md`、`SITE_QA.md`。
- [x] 不同于初译者的 Agent 独立审查并记录问题；源内容 R3-01／R3-02 已修复、复核通过，见 `translation/chapter-03/REVIEW.md`。
- [x] 修复 R3-01／R3-02 并复核，完成原页、草稿站点和本地正式路径验收；见 `translation/chapter-03/REVIEW.md`、`SITE_QA.md`、`INTEGRATION_QA.md`。

## Part I: Data Compression（PDF 77）

- [x] 翻译 PDF 77 扉页标题，并从原页裁取完整中央图形；独立原页审查通过，见 `translation/part-I/REVIEW.md`。
- [x] 分部页草稿站点独立验收通过，已按原书顺序接入正式目录；真实路径与图像解码见 `INTEGRATION_QA.md`。

## 第 4 章导页（PDF 78）

- [x] 对照原 PDF 翻译 “About Chapter 4” 全文、习题 4.1 的 (a)–(e) 与六行记号表；不同 Agent 独立原页审查通过，见 `translation/chapter-04/about-chapter-04/REVIEW.md`。
- [x] 导页草稿站点独立验收通过，推荐习题图标已修复；正式注册后的导航与记号表见 `INTEGRATION_QA.md`，独立真实路径复核仍待补充。

## 第 4 章：The Source Coding Theorem（PDF 79–101）

- [x] 编写与原书正文区分的简短中文导读；`translation/chapter-04/pdf-079.md` 已由独立 Agent 对照原页审查。
- [x] PDF 79–101 的逐页译稿与正文、列表、脚注、习题、原书解答、图像资产由未参与初译的 Agent 对照 PDF 原页审查通过；见 `translation/chapter-04/REVIEW.md`。
- [x] 核实下列小节标题和起始页；逐节译文、段落及无编号小标题已由独立 Agent 对照 PDF 检查。
  - [x] 4.1 How to measure the information content of a random variable?（PDF 79 起）
  - [x] 4.2 Data compression（PDF 85 起）
  - [x] 4.3 Information content defined in terms of lossy compression（PDF 86 起）
  - [x] 4.4 Typicality（PDF 90 起）
  - [x] 4.5 Proofs（PDF 93 起）
  - [x] 4.6 Comments（PDF 95 起）
  - [x] 4.7 Exercises（PDF 96 起）
  - [x] 4.8 Solutions（PDF 98 起）
- [x] 15 处图像引用、图内译注、图注及表格逐格内容经独立原页复核；见 `translation/chapter-04/REVIEW.md`。
- [x] 核对图 4.1–4.4、4.6–4.15 及表 4.5；原书同一图／表称谓矛盾见审查记录。
- [x] 式 (4.1)–(4.55) 的连续编号、变量、上下标及正文数学表达式经原页审查；草稿站点为 300 块、9 节，独立页面审查仍在进行。
- [x] 式 (4.1)–(4.55) 共 55 个编号各出现一次；无编号式及代码已逐页检查。
- [x] 第 4 章原页交叉引用、目录、窄屏和深色模式排版已由独立 Agent 核对；见 `translation/chapter-04/REVIEW.md` 与 `SITE_QA.md`。
- [x] 不同于初译者的 Agent 完成 PDF 原页与译稿的独立审查；未发现待修复的源内容问题，见 `translation/chapter-04/REVIEW.md`。
- [x] 第 4 章原页、草稿站点和正式路径独立审查通过；PDF86 脚注上标、注释块、外链及跳转补入正式 JSON（301 块）后，独立 Agent 再次在桌面/手机复测通过，见 `translation/chapter-04/SITE_QA.md`。

## 第 5 章导页（PDF 102）

- [x] 对照 PDF 原页翻译 “About Chapter 5” 全文和两条区间记号；独立原页审查发现 A5-01 后已修正、复核通过，见 `translation/chapter-05/about-chapter-05/REVIEW.md`。
- [x] 第 5 章导页的五段正文、两行区间记号、13 个行内 MathML、交叉引用与桌面／手机排版已由不同 Agent 独立审查通过；见 `translation/chapter-05/about-chapter-05/REVIEW.md`、`SITE_QA.md`。正式目录接入与真实路径验收待第 5 章正文页面审查后进行。

## 第 5 章：Symbol Codes（PDF 103–120）

- [x] 本章简短中文导读与原书正文分开，独立原页审查通过；见 `translation/chapter-05/REVIEW.md`。
- [x] PDF 103–120 的逐页译稿、段落、跨页续文、习题和原书解答由未参与初译的 Agent 对照原页审查通过。
- [x] 下列小节标题、起始页、译文及无编号小标题已由独立 Agent 对照原 PDF 检查。
  - [x] 5.1 Symbol codes（PDF 104 起）
  - [x] 5.2 What limit is imposed by unique decodeability?（PDF 106 起）
  - [x] 5.3 What’s the most compression that we can hope for?（PDF 109 起）
  - [x] 5.4 How much can we compress?（PDF 110 起）
  - [x] 5.5 Optimal source coding with symbol codes: Huffman coding（PDF 110 起）
  - [x] 5.6 Disadvantages of the Huffman code（PDF 112 起）
  - [x] 5.7 Summary（PDF 114 起）
  - [x] 5.8 Exercises（PDF 114 起）
  - [x] 5.9 Solutions（PDF 116 起）
- [x] 逐项核对 14 处图像引用、全部图内英文译注与图注；图 5.6 中 27 行×5 列及表 5.7、5.10 各格经独立原页审查。
- [x] 核对本章图 5.1–5.3、5.6、5.8–5.9，表 5.5、5.7、5.10，算法 5.4；其余数字是不同对象，不存在相应缺图。
- [x] 式 (5.1)–(5.43) 的变量、上下标、算法、代码及无编号式已逐页核对；网页可读可复制仍待独立验收。
- [x] 式 (5.1)–(5.43) 共 43 个编号各出现一次；原书页 120 的 Kraft 推导由独立 Agent 对照检查。
- [x] 第 5 章术语、交叉引用、目录、窄屏和深色模式排版已由独立 Agent 审查；S5-01/S5-02 已修复并复测通过，见 `translation/chapter-05/SITE_QA.md`。
- [x] 不同于初译者的 Agent 完成 PDF103–120 与译稿的独立逐页审查；无待修源内容问题，见 `translation/chapter-05/REVIEW.md`。
- [x] 第 5 章原页与草稿站点独立审查通过，S5-01/S5-02 已修复；正式 JSON 路径、图片、算法框、公式、表格、导航与进度也经独立 Agent 回归通过，见 `translation/chapter-05/SITE_QA.md`。

## 第 6 章导页（PDF 121）

- [x] 对照原 PDF 物理页 121 翻译 “About Chapter 6” 两段全文，包括上一章习题和习题 2.8 附近的贝叶斯建模提示；独立原页审查通过，见 `translation/chapter-06/about-chapter-06/REVIEW.md`。
- [x] 第 6 章导页原书两段、交叉引用及桌面／手机排版经不同 Agent 独立审查通过；正式路径亦已复测，见 `translation/chapter-06/about-chapter-06/REVIEW.md`、`SITE_QA.md`。

## 第 6 章：Stream Codes（PDF 122–143）

- [x] 不同 Agent 已对 PDF122–143 原页完成只读图、表、算法、公式、码串、习题与解答的逐页盘点；见 `translation/chapter-06/SOURCE_INVENTORY.md`。该盘点不代表正文译稿或网页通过审查。
- [x] 第 6 章简短中文导读与原书正文分开，独立原页审查通过；见 `translation/chapter-06/REVIEW.md`。
- [x] PDF122–143 逐页译稿、段落、脚注、习题 6.1–6.22 与本章 8 道解答经未参与初译的 Agent 对照原页审查。
- [x] 下列小节标题、起始页、译文和无编号小标题已独立对照 PDF 检查。
  - [x] 6.1 The guessing game（PDF 122 起）
  - [x] 6.2 Arithmetic codes（PDF 123 起）
  - [x] 6.3 Further applications of arithmetic coding（PDF 130 起）
  - [x] 6.4 Lempel–Ziv coding（PDF 131 起）
  - [x] 6.5 Demonstration（PDF 133 起）
  - [x] 6.6 Summary（PDF 134 起）
  - [x] 6.7 Exercises on stream codes（PDF 135 起）
  - [x] 6.8 Further exercises on data compression（PDF 136 起）
  - [x] 6.9 Solutions（PDF 139 起）
- [x] 图 6.1、6.2、6.4、6.5、6.8–6.14 的图内文字与图注、8 个习题图标、4 张表逐格经独立原页核对。
- [x] 核对 11 幅编号图、算法 6.3、表 6.6/6.7 与 PDF126/131 两张无编号表；编号空档不代表缺图。
- [x] 式 (6.1)–(6.28)、变量上下标、算法、代码和关键二进制串经独立原页检查；网页公式与代码经独立验收。
- [x] 式 (6.1)–(6.28) 共 28 个编号各出现一次；无编号式亦逐页核对。
- [x] 术语、交叉引用、目录、窄屏和深色模式经独立审查；四张码表、算法框、脚注与图片在正式路径复测通过。
- [x] 不同于初译者的 Agent 依 `SOURCE_INVENTORY.md` 完成 PDF122–143 与译稿逐页独立审查；无待修源内容问题，见 `translation/chapter-06/REVIEW.md`。
- [x] S6-01–03 已修复，草稿与正式路径均由独立 Agent 复测通过；本章验收完成，见 `translation/chapter-06/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 7 章：Codes for Integers（PDF 144–148）

- [x] 本章简短中文导读与原书正文分开，独立原页审查通过；见 `translation/chapter-07/REVIEW.md`。
- [x] PDF144–148 逐页译稿、段落、习题 7.1–7.3、习题 7.1 与跨章 6.22 解答经不同 Agent 对照原页审查。
- [x] 本章没有编号小节；六个无编号标题的层级与先后顺序经独立原页检查。
- [x] 独立 Agent 逐页确认本章无编号小节，保留原书的无编号标题结构。
- [x] 本章原书无图；表 7.1、7.2、7.3、7.5 与一张无编号一元码表逐格核对。
- [x] 核对表 7.1、7.2、7.3、7.5、算法 7.4 与无编号一元码表；表 7.5 的 32 个码字经原页与算法复算。
- [x] 式 (7.1)–(7.6)、上下标、算法 7.4、代码及未编号表达式已逐页核对；网页可读可复制性经独立草稿与正式路径验收。
- [x] 式 (7.1)–(7.6) 共 6 个编号各出现一次；无编号公式、码串、45 的一元码及 98 位 ASCII 例子均对照 PDF 核查。
- [x] 术语、交叉引用、目录、窄屏和深色模式排版经独立草稿与正式路径审查；S7-01 的 98 位代码块已修复并复测通过。
- [x] 不同于初译者的 Agent 对照 PDF144–148 完成独立原页审查；R7-01 译注已修复并复核通过，见 `translation/chapter-07/REVIEW.md`。
- [x] R7-01/S7-01 修复后均通过独立复核；正式路径、公式、码表、算法框、导航及进度恢复通过，本章验收完成，见 `translation/chapter-07/REVIEW.md`、`SITE_QA.md`。

## Part II: Noisy-Channel Coding（PDF 149）

- [x] 已对照 PDF149 翻译分部标题并保留原图；独立原页审查通过，见 `translation/part-II/REVIEW.md`。
- [x] 扉页在草稿与正式路径经独立站点验收；手机标题按原页分两行，原图、目录位置及导航正常，见 `translation/part-II/SITE_QA.md`。

## 第 8 章：Dependent Random Variables（PDF 150–156）

- [x] 本章简短中文导读与原书正文分开，独立原页审查通过。
- [x] PDF150–156 逐节逐段译稿、习题 8.1–8.11 和原书六道解答经不同 Agent 逐页审查；R8-01/02 技术译注已复核。
- [x] 小节标题、起始页、译文与无编号标题经原页目视核对。
  - [x] 8.1 More about entropy（PDF 150 起）
  - [x] 8.2 Exercises（PDF 152 起）
  - [x] 8.3 Further exercises（PDF 153 起）
  - [x] 8.4 Solutions（PDF 154 起）
- [x] 图 8.1–8.3、习题 8.6 的无编号方块图、五个习题图标及 16 格概率表经独立原页核对。
- [x] 图 8.1–8.3 的图内标签、图注和习题 8.6 方块图均保留；见 `translation/chapter-08/REVIEW.md`。
- [x] 式 (8.1)–(8.35)、变量、上下标、习题与解答已独立原页核对；网页公式在草稿与正式路径经独立验收。
- [x] 式 (8.1)–(8.35) 共 35 个编号连续无重号；见 `translation/chapter-08/REVIEW.md`。
- [x] 术语、交叉引用、目录、窄屏和深色模式由独立 Agent 在草稿与正式路径审查；图像、5×5 表与两处技术译注显示正常。
- [x] 不同于初译者的 Agent 已完成原页审查；两处技术译注复核通过，见 `translation/chapter-08/REVIEW.md`。
- [x] R8-01/R8-02 技术译注通过独立原页复核；草稿与正式路径均通过站点审查，本章验收完成，见 `translation/chapter-08/REVIEW.md`、`SITE_QA.md`。

## 第 9 章导页（PDF 157）

- [x] 已对照原 PDF157 翻译并独立核对 “About Chapter 9” 全文与先修习题引用，见 `translation/chapter-09/about-chapter-09/REVIEW.md`；未并入正文。
- [x] 本导页无图表和公式，先修习题引用、两块内容、目录、导航及手机深色经独立 Agent 在原页、草稿与正式路径审查，见 `translation/chapter-09/about-chapter-09/REVIEW.md`、`SITE_QA.md`。

## 第 9 章：Communication over a Noisy Channel（PDF 158–172）

- [x] 不同 Agent 完成 PDF158–172 的图表、公式、例题、习题与解答只读原页盘点，见 `translation/chapter-09/SOURCE_INVENTORY.md`；本项不代表译稿或网页通过审查。
- [x] 初译 Agent 已完成 PDF158–172 的 15 份逐页译稿；R9-01/R9-02 修复后草稿为 240 块、10 个目录项、57 个编号式。
- [x] 本章简短中文导读与原书正文分开，独立原页审查通过。
- [x] PDF158–172 的节次、段落、例题、15 道习题和原书 11 道解答经未参与初译的 Agent 逐页核对。
- [x] 下列小节标题、起始页、译文和无编号小标题经独立 PDF 原页审查。
  - [x] 9.1 The big picture（PDF 158 起）
  - [x] 9.2 Review of probability and information（PDF 159 起）
  - [x] 9.3 Noisy channels（PDF 159 起）
  - [x] 9.4 Inferring the input given the output（PDF 160 起）
  - [x] 9.5 Information conveyed by a channel（PDF 161 起）
  - [x] 9.6 The noisy-channel coding theorem（PDF 163 起）
  - [x] 9.7 Intuitive preview of proof（PDF 165 起）
  - [x] 9.8 Further exercises（PDF 167 起）
  - [x] 9.9 Solutions（PDF 169 起）
- [x] 图 9.1–9.11、无编号流程/信道/手写图、图内文字、图注和三张表逐格经独立原页核对。
- [x] 11 幅编号图及其余无编号插图均有原页对账；34 处图片引用指向 23 个有效资产，见 `translation/chapter-09/REVIEW.md`。
- [x] 式 (9.1)–(9.57)、六个无编号展示式、变量和上下标经独立原页审查；草稿网站数学字形独立复测通过。
- [x] 编号式 (9.1)–(9.57) 连续无重号；式 (9.23)/(9.53) 的特殊变量写法确与原书一致，见 `translation/chapter-09/REVIEW.md`。
- [x] 术语、交叉引用经独立原页审查；草稿与正式站点目录、窄屏、深色模式及 MathML 字形经另一 Agent 独立验收，见 `translation/chapter-09/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已逐页独立审查；R9-01 问号重复和 R9-02 原书端点译注均修复并复核，见 `translation/chapter-09/REVIEW.md`。
- [x] R9-01/R9-02 与 S9-01 修复并独立复核；正式 JSON、相邻导航、34 个图像引用解码和 PDF171 阅读进度在真实路径通过，本章验收完成，见 `translation/chapter-09/REVIEW.md`、`SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 10 章导页（PDF 173）

- [x] 对照 PDF173 翻译 “About Chapter 10” 的先修要求与 Cast of characters 十二行符号表；A10-01 页码技术译注已独立复核。
- [x] 不同 Agent 已逐行核对符号、含义、交叉引用和草稿 JSON，见 `translation/chapter-10/about-chapter-10/REVIEW.md`；未并入上一章或分部扉页。
- [x] 本导页无图片、习题或编号公式；12 行符号表及交叉引用通过原页逐项审查，13 行网页表（含表头）和 18 个 MathML 经独立草稿及正式路径站点审查，见 `translation/chapter-10/about-chapter-10/REVIEW.md`、`SITE_QA.md`。导页验收完成。

## 第 10 章：The Noisy-Channel Coding Theorem（PDF 174–187）

- [x] 不同 Agent 完成 PDF174–187 的只读原页盘点，见 `translation/chapter-10/SOURCE_INVENTORY.md`；涵盖节次、式 (10.1)–(10.33)、图、习题与解答，仅供后续译稿对账，不代表本章完成。
- [x] 初译 Agent 完成 PDF174–187 的 14 份逐页译稿、15 处图像与图内文字译注、12 道习题及 4 道原书解答，生成 216 块草稿；独立原页和站点审查正在进行。
- [x] 编写本章简短中文导读，与原书正文区分；是否准确仍待独立原页审查。
- [x] 独立 Agent 对照 PDF174–187 核对正文、跨页段落、习题 10.1–10.8 与 10.10–10.13、四道原书解答和引用；10.9 是例题，见 `translation/chapter-10/REVIEW.md`。
- [x] 原页核实 10.1–10.10 小节标题、起始页、译文和无编号小标题。
  - [x] 10.1 The theorem（PDF 174 起）
  - [x] 10.2 Jointly-typical sequences（PDF 174 起）
  - [x] 10.3 Proof of the noisy-channel coding theorem（PDF 176 起）
  - [x] 10.4 Communication (with errors) above capacity（PDF 179 起）
  - [x] 10.5 The non-achievable region (part 3 of the theorem)（PDF 180 起）
  - [x] 10.6 Computing capacity（PDF 181 起）
  - [x] 10.7 Other coding theorems（PDF 183 起）
  - [x] 10.8 Noisy-channel coding theorems and coding practice（PDF 184 起）
  - [x] 10.9 Further exercises（PDF 184 起）
  - [x] 10.10 Solutions（PDF 185 起）
- [x] 图 10.1–10.10、五张无编号正文图及页边箭头、图内英文和图注经独立原页审查；三张裁图问题修复后原页及草稿网页复测通过。本章无原书编号表格。
- [x] 图 10.1–10.10 共十幅编号图和五张无编号图片，16 个图片引用（含习题 10.12 图标）均有有效资产；见 `translation/chapter-10/REVIEW.md`。
- [x] 式 (10.1)–(10.33)、八个无编号展示式、变量、上下标与 PDF175 两条 100 位代码串经独立原页核对；草稿网页 41 式可读，长式局部滚动。
- [x] 式 (10.1)–(10.33) 连续无重号；式 (10.24) 三条分组横线、式 (10.26) 近似下界均经原页和草稿网站复核。
- [x] 术语、交叉引用经独立原页审查；草稿及正式站点目录、窄屏、深色模式和阅读进度经不同 Agent 审查。
- [x] 不同于初译者的 Agent 已逐页独立审查；R10-01–04 修复后复核关闭，见 `translation/chapter-10/REVIEW.md`。
- [x] R10-01–04 与 S10-01–04 修复后独立复核；正式 JSON、式 (10.24) 三线、全部图像、相邻导航与 PDF187 阅读位置在真实路径验收通过，本章完成，见 `translation/chapter-10/REVIEW.md`、`SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 11 章导页（PDF 188）

- [x] 已目视 PDF188 初译 “About Chapter 11” 的先修要求、高斯分布预备知识及式 (11.1)–(11.4)，构建 16 块草稿。
- [x] 不同于初译者的 Agent 已对照原 PDF188 逐段核对全部文字、四个公式、符号与交叉引用，无待修复内容；见 `translation/chapter-11/about-chapter-11/REVIEW.md`。本页未并入上一章或分部扉页。
- [x] 本导页无图、表、代码、习题或脚注；式 (11.1)–(11.4) 和正文经独立原页审查，16 块草稿及正式路径的三个视口 MathML、粗体、下标、转置及长公式滚动均通过不同 Agent 独立站点审查。阅读进度漂移修复后连续刷新三次保持原锚点，导页验收完成；见 `translation/chapter-11/about-chapter-11/REVIEW.md`、`SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 11 章：Error-Correcting Codes and Real Channels（PDF 189–202）

- [x] 不同 Agent 完成 PDF189–202 的只读原页盘点，见 `translation/chapter-11/SOURCE_INVENTORY.md`；逐页列出式 (11.5)–(11.47)、图 11.1–11.9、习题与解答、原书疑点。本项不代表译稿或网站审查完成。
- [x] 初译 PDF189–194 六页，保留式 (11.5)–(11.34)、图 11.1–11.5 原始信息和图内中文译注；103 块部分草稿通过构建。
- [x] 初译 PDF195–202 八页，保留式 (11.35)–(11.47)、图 11.6–11.9、无编号生成矩阵/串接流程及题解；整章为 225 块、11 项目录、43 个编号式、11 个图块、10 道习题，已通过独立原页与网站审查。
- [x] PDF189–194 已由未参与初译的 Agent 逐页独立审查，30 个编号式、五张图、两道习题和 103 块部分草稿无待修问题；见 `translation/chapter-11/REVIEW_PARTIAL.md`。这不代表整章验收。
- [x] 编写本章简短中文导读，与原书正文区分；已通过独立原页审查。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、答案与参考文献；核对页段对应关系。
- [x] 对照原 PDF 核实 11.1–11.10 的标题、起始页、段落与无编号小标题，见本章独立 `REVIEW.md`。
  - [x] 11.1 The Gaussian channel（PDF 189 起）
  - [x] 11.2 Inferring the input to a real channel（PDF 191 起）
  - [x] 11.3 Capacity of Gaussian channel（PDF 191 起）
  - [x] 11.4 What are the capabilities of practical error-correcting codes?（PDF 195 起）
  - [x] 11.5 The state of the art（PDF 198 起）
  - [x] 11.6 Summary（PDF 199 起）
  - [x] 11.7 Nonlinear codes（PDF 199 起）
  - [x] 11.8 Errors other than noise（PDF 199 起）
  - [x] 11.9 Exercises（PDF 200 起）
  - [x] 11.10 Solutions（PDF 201 起）
- [x] 逐项核对原页图片、图内英文、图注及页边说明；本章没有表格或程序代码。
- [x] 对照原页确认图 11.1–11.9 及两幅无编号图；图 11.8 对比度问题已修复并复核。
- [x] 逐项核对公式、变量、上下标及编号；44 个展示式在草稿网站可读、可复制。
- [x] 对照原页确认编号式 (11.5)–(11.47) 连续且有 1 个无编号式。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式；正式路径五视口及共享进度修复后的刷新回归均通过。
- [x] 不同于初译者的 Agent 已完成原页和网站独立审查，问题均修复复核，见 `REVIEW.md`、`SITE_QA.md`。
- [x] 图 11.8 对比度、图 11.6 替代文字两项问题均修复复核；正式 JSON 与已审草稿逐字节相同，真实路径验收通过，本章完成。

## Part III: Further Topics in Information Theory（PDF 203）

- [x] 第三部分扉页标题与完整递归图形对照 PDF203 独立审查通过；2 块正式 JSON 与已审草稿相同。
- [x] 扉页目录位置、前后导航、原图及 1440px／390px 浅深色排版通过独立正式路径审查；短页页底进度 100% 与三次刷新恢复已复核。

## 第 12 章导页（PDF 204）

- [x] 对照 PDF204 原页译出 “About Chapter 12” 四段正文；独立原页审查指出的斜体强调和措辞两项已修复复核，正式 JSON 共 5 块且与已审草稿相同。
- [x] 独立核对导页的源编码／信道编码回顾和正文顺序；未并入上一章或分部扉页。
- [x] 确认原页没有图片、公式或习题；斜体、交叉引用、1440px／390px 浅深色排版和正式前后导航均通过独立审查，页底 100% 进度与三次刷新恢复通过。

## 第 12 章：Hash Codes: Codes for Efficient Information Retrieval（PDF 205–216）

- [x] 本章中文导读已明确标为非原书正文；PDF205–216 的 12 页逐页译稿均对照原页完成，正文、列表、页边说明、脚注、8 道习题及解答均经独立 Agent 核对。
- [x] 七节标题、层级、顺序与逐页段落已核实：
  - [x] 12.1 The information-retrieval problem（PDF 205 起）。
  - [x] 12.2 Hash codes（PDF 207 起）。
  - [x] 12.3 Collision resolution（PDF 209 起）。
  - [x] 12.4 Planning for collisions: a birthday problem（PDF 210 起）。
  - [x] 12.5 Other roles for hash codes（PDF 210 起）。
  - [x] 12.6 Further exercises（PDF 213 起）。
  - [x] 12.7 Solutions（PDF 214 起）。
- [x] 图 12.1、12.2、12.4 和算法 12.3 的图形、图注及图内英文译注逐一核对；算法代码和另一代码块可复制。算法 12.3 原书 C 注释续行缺 `//`，网站采用可复制写法并以非正文译注说明，已复核。
- [x] 式 (12.1)–(12.11)、无编号数学表达式、变量、上下标、算法及代码与原页逐一核对；式 (12.4) 两段下划线的浏览器显示问题已修复并经五视口复测。
- [x] 未参与初译的 Agent 完成全 12 页原页审查、草稿与正式路径网站审查；五视口图、公式、代码、脚注、目录、前后导航、进度刷新及整页宽度通过，见 `translation/chapter-12/REVIEW_PARTIAL.md`、`REVIEW.md`、`SITE_QA.md`。
- [x] 审查问题已修复复核；136 块、8 项目录和 11 个编号式的正式 JSON 与已审草稿逐字节相同，本章验收完成。

## 第 13 章导页（PDF 217）

- [x] 对照 PDF217 原页译出标题和两段正文，保留斜体强调与 $N$；3 块正式 JSON 与已审草稿逐字节相同，独立原页审查通过。
- [x] 独立对照原 PDF 核对 “About Chapter 13” 全文，包括二元输入信道与编码理论导入；未并入上一章或分部扉页。
- [x] 确认原页没有图片、展示公式或习题；390px 段尾孤行已修复。正式路径 1440px 浅色、390px 浅／深色、导航及页底 100% 进度三次刷新均经独立审查通过。

## 第 13 章：Binary Codes（PDF 218–239）

- [x] 对照 PDF218–219 原页初译导读、开篇、13.1 与 13.2、图 13.1–13.3 及图内表格；未参与初译的 Agent 已完成两页独立原页审查，例 13.1 的保证纠错界修复复核，见 `translation/chapter-13/REVIEW_PARTIAL.md`。
- [x] PDF220–228 已逐页初译，涵盖 13.3–13.10 起始、图 13.4–13.15、式 (13.1)–(13.27)、习题 13.4–13.6；正在接受独立原页审查，不代表这些页已验收。
- [x] PDF229–231 已逐页初译并通过独立原页审查，涵盖表 13.16、式 (13.28)–(13.38) 与 13.11 起始；几处原书斜体、MDS 名称和擦除界译法已修复复核，见 `translation/chapter-13/REVIEW_229_231.md`。
- [x] PDF232–233 已逐页初译并通过独立原页审查，含图 13.17、式 (13.39)–(13.41) 和习题 13.13–13.19；两处原书强调／变量遗漏已修复复核，见 `translation/chapter-13/REVIEW_232_233.md`。
- [x] PDF234–239 已逐页初译并通过独立原页审查，含习题 13.20–13.26、13.14 节解答、式 (13.42)–(13.56) 及 64 格码字表；原书粗斜体遗漏已修复复核，见 `translation/chapter-13/REVIEW_234_239.md`。全章 334 块草稿、15 项目录、56 个连续编号式可构建。
- [x] 本章简短中文导读已明确标为非原书正文；PDF218 原页导读位置和正文分隔经独立核对。
- [x] 全 22 页逐节逐段译出并经不同于初译者的 Agent 核对正文、列表、页边文字、22 道原书习题、答案、参考文献及跨页衔接；原书本章无脚注。
- [x] 以下小节标题与起始页已对照原 PDF 逐项核对，正文、段落和无编号小标题的源文审查通过。
  - [x] 13.1 Distance properties of a code（PDF 218 起；原页审查通过）。
  - [x] 13.2 Obsession with distance（PDF 218 起；原页审查通过）。
  - [x] 13.3 Perfect codes（PDF 220 起；原页审查通过）。
  - [x] 13.4 Perfectness is unattainable – first proof（PDF 222 起；原页审查通过）。
  - [x] 13.5 Weight enumerator function of random linear codes（PDF 223 起；原页审查通过）。
  - [x] 13.6 Berlekamp’s bats（PDF 225 起；原页审查通过）。
  - [x] 13.7 Concatenation of Hamming codes（PDF 226 起；原页审查通过）。
  - [x] 13.8 Distance isn’t everything（PDF 227 起；原页审查通过）。
  - [x] 13.9 The union bound（PDF 228 起；原页审查通过）。
  - [x] 13.10 Dual codes（PDF 228 起；PDF228–231 原页审查通过）。
  - [x] 13.11 Generalizing perfectness to other channels（PDF 231 起；原页审查通过）。
  - [x] 13.12 Summary（PDF 232 起；原页审查通过）。
  - [x] 13.13 Further exercises（PDF 232 起；原页审查通过）。
  - [x] 13.14 Solutions（PDF 235 起；原页审查通过）。
- [x] 逐项核对图片、图内英文、图注及 5 张表的每个单元格；图 13.1–13.15、13.17 共 16 幅，其中 13.16 是表号而非图号。表 13.16 八个码字和 GF(8) 码字表 64 格均经独立 Agent 逐格核对。
- [x] 编号式 (13.1)–(13.56) 连续各一次，另有 2 条无编号展示式；全部变量、上下标、矩阵逐项对照原页。式 (13.40) 的 5×15 与 (13.41) 的 10×15 共 225 格已独立逐格复核。
- [x] 全章草稿及正式路径的 1440px 浅色、390px 浅／深色、350px 浅／深色独立网站审查通过；58 个展示式、16 图、5 表、22 题的可读性与局部横滑、GF(8) 表复制、进度刷新均已复核，见 `translation/chapter-13/SITE_QA_PARTIAL.md`、`SITE_QA.md`。
- [x] 术语、交叉引用、15 项目录、窄屏和深色模式排版经独立审查；三处矩阵分隔线、表 13.16 线型及 GF(8) 表折行问题均已修复复测。
- [x] 不同于各页初译者的 Agent 分段独立完成全 22 页原文内容审查并记录修复复核，全章结论见 `translation/chapter-13/REVIEW.md`，逐页记录见其索引。
- [x] 全部审查问题已修复复核；334 块正式 JSON 与已审草稿逐字节一致，第 13 章验收完成。

## 第 14 章导页（PDF 240）

- [x] “About Chapter 14” 三段正文与交叉引用已对照 PDF240 原页通过独立审查；4 块草稿可构建，见 `translation/chapter-14/about-chapter-14/REVIEW.md`。
- [x] 独立原页确认本导页没有图、表、公式或习题，也没有漏掉图内文字。
- [x] 草稿与正式网站五视口排版、前后导航和阅读进度经独立审查通过；见 `translation/chapter-14/about-chapter-14/SITE_QA.md`。

## 第 14 章：Very Good Linear Codes Exist（PDF 241–244）

- [x] PDF241–244 四页初译及独立原页审查通过，56 块、3 项目录、式 (14.1)–(14.19) 的草稿可构建，见 `translation/chapter-14/REVIEW.md`。
- [x] 本章简短中文导读已标为非原书正文，位置与原书正文分隔经独立复核。
- [x] 逐节逐段核对正文、列表、三条页边说明、习题 14.1、无编号定理、末尾 Notes 与交叉引用；原书本章无脚注、图、表或代码。
- [x] 两节标题、起始页和正文顺序已对照原页核实：
  - [x] 14.1 A simultaneous proof of the source coding and noisy-channel coding theorems（PDF 241 起）。
  - [x] 14.2 Data compression by linear hash codes（PDF 243 起）。
- [x] 原页确认本章没有图片、图内英文、图注或表格。
- [x] 式 (14.1)–(14.19) 编号连续、变量和上下标经独立原页核对；无漏掉的无编号展示式。
- [x] 19 个编号公式在正式页面可读可复制，五视口桌面／窄屏／深色排版经独立核对。
- [x] 术语、交叉引用、目录、相邻导航、窄屏和深色模式排版经独立复核通过。
- [x] 不同于初译者的 Agent 已完成 PDF241–244 逐页原书内容审查并记录结论，见 `translation/chapter-14/REVIEW.md`。
- [x] PDF244 末句精简经原页复核不改变原意；草稿与正式 JSON 字节一致，五视口真实路径、进度与三次刷新复核通过，完成本章验收；见 `translation/chapter-14/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 15 章：Further Exercises on Information Theory（PDF 245–252）

- [x] PDF245–252 八页初译及独立原页审查通过：21 道习题、式 (15.1)–(15.4)、另 7 条无编号展示式、表 15.1、图 15.2–15.9 及两幅无编号信道图、习题 15.12 解答均在；102 块草稿可构建，见 `translation/chapter-15/REVIEW.md`。
- [x] 本章简短中文导读已标为非原书正文，并经独立原页审查复核。
- [x] 逐页核对正文、21 道习题与子问、列表、唯一解答及跨页接续；原书本章没有脚注。
- [x] 原页确认本章没有编号小节；两个无编号习题分组标题及解答标题的层级和顺序已核对。
- [x] 十幅图的裁切、箭头、曲线、原书图内英文中文译注和图内表格均已核对；图 15.4 在 PDF249 先于 PDF250 的图 15.3，按原书顺序保留。表 15.1 两个 ISBN 单元格逐格一致。
- [x] 式 (15.1)–(15.4) 连续，另 7 条无编号展示式；变量和上下标经原页核对，本章无算法代码块。
- [x] 草稿网站五视口复测 11 个展示式可读可复制、10 图解码、表 15.1、窄屏／深色排版与末页阅读进度；式 (15.3) 分隔线已修复复测，见 `translation/chapter-15/SITE_QA.md`。
- [x] 草稿与正式路径的术语、交叉引用、无编号小标题、目录约定、窄屏和深色模式排版经独立审查通过。
- [x] 不同于初译者的 Agent 已完成 PDF245–252 全八页独立原页审查，结果见 `translation/chapter-15/REVIEW.md`。
- [x] S15-01 式 (15.3) 分隔线已修复复核；正式 JSON 与已审草稿逐字节相同，五视口真实路径、邻接导航、末页 100% 进度与三次刷新通过，本章验收完成；见 `translation/chapter-15/SITE_QA.md`、`INTEGRATION_QA.md`。

## 第 16 章：Message Passing（PDF 253–259）

- [x] PDF253–259 七份逐页初译、12 张图像资产及非原书正文导读已写齐；算法 16.5 的分支层级修复后，71 块草稿经独立审查与正式路径验收。
- [x] 编写本章简短中文导读，与原书正文区分；独立语义与站点审查通过。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、答案与参考文献；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；逐节译文与无编号小标题已核对。
  - [x] 16.1 Counting（PDF 253 起）
  - [x] 16.2 Path-counting（PDF 256 起）
  - [x] 16.3 Finding the lowest-cost path（PDF 257 起）
  - [x] 16.4 Summary and related ideas（PDF 258 起）
  - [x] 16.5 Further exercises（PDF 258 起）
  - [x] 16.6 Solutions（PDF 259 起）
- [x] 逐项核对 11 幅编号图、1 幅无编号图、图内文字与图注，以及 PDF254 的 3×3 加法表全部单元格。
- [x] 图表编号定位：Figure 16.2–16.13 中编号的 11 幅均已核对，另有 1 幅无编号习题图；原书无编号表格 1 张。
- [x] 逐项核对式 (16.1)、变量、上下标、算法 16.1 和 16.5；网站五视口可读可复制。
- [x] 公式编号定位：(16.1) 为本章唯一编号展示式；无 `merror`。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版，见 `translation/chapter-16/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已对照 PDF253–259 独立审查 12 图、两项算法、式 (16.1)、4 道习题及 2 道解答；算法 16.5 的分支层级修复后原页复核通过，见 `translation/chapter-16/REVIEW.md`。
- [x] 修复算法 16.5 层级与网站缩进并独立复核；正式 JSON 与已审草稿逐字节相同，五视口正式路径、导航、末页进度和刷新回归通过，本章验收完成。

## 第 17 章：Communication over Constrained Noiseless Channels（PDF 260–271）

- [x] PDF260–271 十二份逐页译稿、9 幅图、6 张表、式 (17.1)–(17.35) 及 12 道习题已核对；矩阵行数、跨页句和斜体标题均修复复核。式 (17.33) 的原书两行代数差异忠实保留。
- [x] 编写本章简短中文导读，与原书正文区分；独立语义与网站审查通过。
- [x] 逐节逐段翻译和核对正文、列表、习题、六项解答与交叉引用；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；七节与六个斜体小标题已核对。
  - [x] 17.1 Three examples of constrained binary channels（PDF 260 起）
  - [x] 17.2 The capacity of a constrained noiseless channel（PDF 262 起）
  - [x] 17.3 Counting the number of possible messages（PDF 263 起）
  - [x] 17.4 Back to our model channels（PDF 266 起）
  - [x] 17.5 Practical communication over constrained channels（PDF 266 起）
  - [x] 17.6 Variable symbol durations（PDF 268 起）
  - [x] 17.7 Solutions（PDF 269 起）
- [x] 逐项核对 9 幅图、图内英文与图注，以及 6 张表各行列和非空单元格。
- [x] 图表编号定位：Figure 17.1–17.7、17.9–17.10 共 9 幅；17.8 是表，另有 5 张无编号表。
- [x] 对照 PDF 核对 35 个编号式和 1 个无编号矩阵式；网站 MathML 可读可复制。
- [x] 公式编号定位：(17.1)–(17.35) 连续；PDF269 另有无编号矩阵式。
- [x] 术语、交叉引用、目录、窄屏与深色模式排版已独立检查，见 `translation/chapter-17/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已对照 PDF260–271 独立审查并复核全部三项修复，见 `translation/chapter-17/REVIEW.md`。
- [x] 三项原页审查问题均已复核；正式 JSON 与已审草稿逐字节相同，五视口草稿及两视口正式路径、导航和末页进度通过，本章验收完成。

## 第 18 章：Crosswords and Codebreaking（PDF 272–280）

- [x] PDF272–280 九份逐页译稿、6 张图、5 张表、式 (18.1)–(18.25)、习题 18.1–18.3 与脚注经独立审查；118 块正式 JSON 与已审草稿逐字节相同，无 `merror`。
- [x] 编写本章简短中文导读，与原书正文区分；独立语义与网站审查通过。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题与交叉引用；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；逐节译文和斜体已核对。
  - [x] 18.1 Crosswords（PDF 272 起）
  - [x] 18.2 Simple language models（PDF 274 起）
  - [x] 18.3 Units of information content（PDF 276 起）
  - [x] 18.4 A taste of Banburismus（PDF 277 起）
  - [x] 18.5 Exercises（PDF 280 起）
- [x] 逐项核对图 18.1、18.3–18.7 和图内中文译注，表 18.2、18.8、18.9 及两张无编号表的单元格。
- [x] 图表编号定位：原书图 18.2 为表非图，共 6 幅图、5 张表；表 18.9 三行各 72 可见字符与原书题注 $T=74$ 的矛盾忠实保留。
- [x] 对照 PDF 核对式 (18.1)–(18.25) 的变量、上下标与编号；网站可读可复制。
- [x] 公式编号定位：(18.1)–(18.25) 连续，无 `merror`。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版；表 18.9 逐位对齐、局部横滑经六视口复测。
- [x] 不同于初译者的 Agent 已对照 PDF272–280 独立审查，式 (18.15)、原书斜体与概率措辞修复后复核通过；表 18.9 原书字符数与题注数值不一致处按原页保留，见 `translation/chapter-18/REVIEW.md`。
- [x] 式 (18.15)、斜体与概率措辞及表 18.9 换行问题均修复复核；正式 JSON 与草稿逐字节相同，六视口真实路径与末页进度通过，本章验收完成。

## 第 19 章：Why have Sex? Information Acquisition and Evolution（PDF 281–292）

- [x] PDF281–292 十二份逐页译稿、7 节、21 个编号式、6 个无编号展示式、4 图、6 道习题和原书解答 19.1 已对原页核对；131 个递归阅读块中框 19.2 为 14 个子块，顶层 JSON 共 118 项。
- [x] 编写本章简短中文导读，与原书正文区分；独立语义和网站审查通过。
- [x] 逐节逐段翻译和核对正文、列表、习题、唯一解答和参考文献；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；逐节译文和斜体小标题已核对。
  - [x] 19.1 The model（PDF 282 起）
  - [x] 19.2 Rate of increase of fitness（PDF 283 起）
  - [x] 19.3 The maximal tolerable mutation rate（PDF 287 起）
  - [x] 19.4 Fitness increase and information acquisition（PDF 288 起）
  - [x] 19.5 Discussion（PDF 289 起）
  - [x] 19.6 Further exercises（PDF 291 起）
  - [x] 19.7 Solutions（PDF 292 起）
- [x] 逐项核对图 19.1、19.3–19.5、图内英文译注与图注；原书无表格。
- [x] 图表编号定位：19.2 是框号而非缺图；共 4 幅编号图、1 个带框的推导块。
- [x] 对照 PDF 核对式 (19.1)–(19.21) 与框 19.2 内六条无编号式；网站 MathML 可读可复制。
- [x] 公式编号定位：(19.1)–(19.21) 连续，框内六式无编号。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版；框 19.2 的连续外边线修复后五视口复测通过。
- [x] 不同于初译者的 Agent 已对照 PDF281–292 独立审查并复核式 (19.2)；框 19.2 的式号误引及式 (19.14) 的积分常数疑点为原书问题，译稿忠实保留，见 `translation/chapter-19/REVIEW.md`。
- [x] 式 (19.2) 左侧符号及框 19.2 网站结构均修复复核；正式 JSON 与已审草稿逐字节相同，五视口真实路径、导航和末页进度通过，本章验收完成。

## Part IV: Probabilities and Inference（PDF 293）

- [x] 扉页标题与无编号原图已对照 PDF293 核对，2 块正式 JSON 与审定草稿逐字节相同。
- [x] 分部页的目录位置、第 19 章前后导航、六视口正式路径与页末进度均通过独立验收，见 `translation/part-IV/REVIEW.md`、`SITE_QA.md`。

## Part IV 导页（PDF 294–295）

- [x] 已逐页初译两页正文，保留精确／近似方法、两项编号列表、章节路线、两个斜体小标题和推荐阅读；18 块草稿已构建。
- [x] 不同于初译者的 Agent 对照 PDF294–295 独立核对全文、章节路线、斜体和交叉引用；三处译义细节修复后复核通过，见 `translation/part-IV/REVIEW.md`。
- [x] 六视口草稿网站排版由不同 Agent 独立审查通过；三个 PDF295 译义细节和四处短孤行修复复核，图像、列表、强调、目录及进度正常，见 `translation/part-IV/SITE_QA.md`。
- [x] 正式路径第 19 章→第四部分扉页→导页及返回导航、六视口图文和阅读进度均由独立 Agent 复核通过；正式 JSON 与审定草稿逐字节相同。

## 第 20 章：An Example Inference Task: Clustering（PDF 296–304）

- [x] PDF296–304 九页已逐页初译并独立原页审查：9 幅编号图与习题 20.4 附图、算法 20.2/20.7、式 (20.1)–(20.23)、习题 20.1–20.5 和原书解答 20.1/20.3/20.5 齐全。83 项顶层块、6 项目录的正式 JSON 与审定草稿逐字节相同，MathML 无 `merror`；PDF303 两个初始均值均印 $m^{(1)}$，译稿忠实照录。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页及网站审查通过。
- [x] 逐节逐段翻译和核对正文、列表、习题、三条解答与参考文献；核对页段对应关系。
- [x] 核实以下小节标题、起始页及层级；五节译文与无编号斜体标题已核对。
  - [x] 20.1 K-means clustering（PDF 297 起）
  - [x] 20.2 Soft K-means clustering（PDF 301 起）
  - [x] 20.3 Conclusion（PDF 301 起）
  - [x] 20.4 Exercises（PDF 302 起）
  - [x] 20.5 Solutions（PDF 303 起）
- [x] 逐项核对图 20.1、20.3–20.6、20.8–20.11 与习题 20.4 无编号附图的全部小面板、图内英文译注和图注；原书无表格。
- [x] 图表编号定位：20.2 和 20.7 为算法而非缺图，共 9 幅编号图、1 幅无编号习题图。
- [x] 对照 PDF 核对式 (20.1)–(20.23)、变量和上下标；算法框内公式保持编号，网站 MathML 可读可复制。
- [x] 公式编号定位：(20.1)–(20.23) 连续，原书无其他编号式。
- [x] 术语、交叉引用、目录、窄屏与深色模式排版已独立检查，见 `translation/chapter-20/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已对照 PDF296–304 独立审查；斜体、习题提示换行与图 20.8 右裁边三项问题均修复复核，见 `translation/chapter-20/REVIEW.md`。
- [x] 斜体、习题提示换行和图 20.8 右裁边三项修复均经独立复核；正式路径五视口、相邻导航和末页进度通过，本章验收完成。

## 第 21 章：Exact Inference by Complete Enumeration（PDF 305–311）

- [x] 初译 PDF305–311 七页正文已写齐：章题、独立导读、21.1/21.2 与例 21.1、图 21.1–21.7 及图内文字译注、式 (21.1)–(21.9) 和无编号混合式、条件概率与分子枚举、解释消除、习题 21.2/21.3、五维枚举与指数代价均已逐页对照原图。
- [x] 初译者逐页自核并构建草稿 `chapter-21.draft.json`（62 块、3 项目录、7 图、2 道习题；MathML 无错误）；原页与网站独立审查通过。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页审查通过。
- [x] 对照 PDF305–311 逐节逐段核对正文、概率列表、例 21.1、习题 21.2/21.3、跨页顺序；独立原页审查通过，见 `translation/chapter-21/REVIEW.md`。
- [x] 原页确认 21.1 The burglar alarm（PDF305 起）、21.2 Exact inference for continuous hypothesis spaces（PDF307 起）两节及标题层级。
- [x] 逐项核对图 21.1–21.7 的原始内容、图内英文、图注及相邻译注；本章无独立表格。
- [x] 原页确认图 21.1–21.7 连续编号及其所在页；七幅图均已接入草稿。
- [x] 对照原页核对变量、上下标、9 个连续编号式 (21.1)–(21.9) 与 4 个无编号展示式；13 式的 MathML、可读与复制性经六视口网站 QA 通过。
- [x] 原页确认公式范围与无编号展示式；本章没有需另行保留的代码或算法框。
- [x] 网站草稿 QA 的 PDF306 两列条件概率式在桌面阅读栏需横滑；共享 CSS 在溢出时显示提示，经独立 Agent 六视口复测，S21-SITE-01 已关闭。
- [x] 独立 Agent 已核对术语、交叉引用、目录及 1440/390/320px 浅深六视口的图、式、习题、导航和末页进度；草稿与正式路径网站 QA 均通过。
- [x] 不同于初译者的 Agent 已逐页对照原 PDF 独立审查，未发现待修源文问题，见 `translation/chapter-21/REVIEW.md`。
- [x] PDF306 双列式的桌面横滑提示已修复并复核；正式 JSON 与审定草稿逐字节相同（73,338 字节，SHA-256 `915aaf2e0084415803cf9567b7c0abb5814155e2cb2925e8d6b103841feeb5d0`），正式路径六视口及 `verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 22 章：Maximum Likelihood and Clustering（PDF 312–322）

- [x] 初译 PDF312：章题、独立导读、章首三段、22.1、式 (22.1)–(22.6)、充分统计量、例 22.1 与解答；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF313：图 22.1 四面板与图内英文译注、例 22.2/22.3 及解答、式 (22.7)–(22.9)、误差棒说明和跨页括注；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF314：例 22.3 后续式 (22.10)–(22.14) 与解答方框、习题 22.4、22.2 节、习题 22.5 开头、式 (22.15)–(22.17) 及跨页要求；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF315：习题 22.5 续题、式 (22.18)–(22.21)、牛顿—拉夫森括注、原书小数据图和 22.3 节开头；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF316：算法 22.2 与 22.4、式 (22.22)–(22.28)、图 22.3 两行面板及算法图注；初译者已对照原页，待全章独立审查。式 (22.22) 分母的原书下标疑点按原页保留，待独立复核。
- [x] 初译 PDF317：图 22.5–22.7 与时间标记、22.3 续文、33.7 节页边说明、22.4 节及习题 22.6；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF318：22.4 续文中的“砰！”与最大后验方法、式 (22.29)、Hanson 延伸阅读、22.5 节与习题 22.7；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF319：习题 22.8–22.12、式 (22.30)/(22.31)、无编号矩形窗图和图 22.8 三方位图；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF320：习题 22.12 续题、式 (22.32)/(22.33)、习题 22.13、式 (22.34)–(22.36)、强调文字及缩进的作者评论；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF321：习题 22.14–22.16 前半、高维高斯无编号式、图 22.9、七位科学家数据表及跨页解答；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF322：习题 22.16 续题与答案、22.6 解答、图 22.10、习题 22.5/22.12 解答及式 (22.37)–(22.41)；初译者已对照原页。式 (22.38)/(22.40) 上标疑点照印本保留，待独立复核。
- [x] 独立源审发现 S22-01：图 22.10 右侧纵轴 0–5 数字裁断；初译 Agent 已扩大裁边，源审 Agent 已对照原页复核全部数字，问题关闭。
- [x] 初译者完成 PDF312–322 全章逐页自核并构建 `chapter-22.draft.json`：151 顶层块、7 项目录、41 个编号式加 1 个无编号式、11 张源图、13 道习题及七位科学家数据表；MathML 无错误。
- [x] 不同于初译者的 Agent 已对照 PDF312–322 独立原页审查全章并通过；原书式 (22.22)、(22.38)/(22.40) 的记号疑点照原页保留，见 `translation/chapter-22/REVIEW.md`。
- [x] 独立 Agent 完成 1440/390/320px 浅深六视口草稿及正式路径网站 QA：42 式可读可复制、11 图完整、七行数据表和 13 题正常、末页 100% 三次刷新稳定，见 `translation/chapter-22/SITE_QA.md`。
- [x] 编写本章简短中文导读，与原书正文区分，独立原页审查通过。
- [x] 对照 PDF312–322 逐节逐段核对正文、列表、习题、解答、页边说明和跨页接续；原书无单列参考文献或脚注遗漏。
- [x] 原页确认六节标题、层级及起始页：
  - [x] 22.1 Maximum likelihood for one Gaussian（PDF312 起）
  - [x] 22.2 Maximum likelihood for a mixture of Gaussians（PDF314 起）
  - [x] 22.3 Enhancements to soft K-means（PDF315 起）
  - [x] 22.4 A fatal flaw of maximum likelihood（PDF317 起）
  - [x] 22.5 Further exercises（PDF318 起）
  - [x] 22.6 Solutions（PDF322 起）
- [x] 对照原页逐张核对图 22.1、22.3、22.5–22.10 与两张习题插图，保留全部图内文字和图注；图 22.9 的七位科学家数据另列为可复制表格并逐格核对。
- [x] 对照原页核对连续式 (22.1)–(22.41)、1 个无编号展示式、算法 22.2/22.4 的步骤和边框；网站 MathML 可读可复制、窄屏局部横滑正常。
- [x] 核对术语、交叉引用、目录及 1440/390/320px 浅深六视口排版；无整页横溢、资源或脚本错误。
- [x] 不同于初译者的 Agent 独立审查并记录 S22-01；图 22.10 裁边修复后原页与正式网站均复核通过。
- [x] 正式 JSON 与审定草稿逐字节相同（149,221 字节，SHA-256 `91d521e36c3e9a45f507a95db59f7119a14e075c2b16b72108e80350df542992`）；`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，本章验收完成。

## 第 23 章：Useful Probability Distributions（PDF 323–330）

- [x] 不同于初译者的 Agent 已完成 PDF323–330 独立原页内容审查；九图、35 个编号式、2 个无编号式、4 题及四处原书疑点记录见 `translation/chapter-23/REVIEW.md`。草稿与正式网站六视口 QA 均通过。
- [x] 初译 PDF323：章题、独立导读、23.1 与无编号小标题、全部段落、式 (23.1)–(23.4)、图 23.1/23.2 及图内文字译注；已由不同 Agent 对照原页复核。
- [x] 初译 PDF324：23.2 与无编号小标题、式 (23.5)–(23.9)、双高斯无编号式、习题 23.1、图 23.3 及双面板译注；已由不同 Agent 对照原页复核。
- [x] 初译 PDF325：Student-t 与双指数、反双曲余弦分布、式 (23.10)–(23.16)、23.3 节开头及等待时间例子；已由不同 Agent 对照原页复核。
- [x] 初译 PDF326：图 23.4 四面板及译注、式 (23.17)–(23.21)、$1/x$ 先验、习题 23.2 与逆伽马分布；已由不同 Agent 对照原页复核。原书尺度重参数化同符号写法照录并记录。
- [x] 初译 PDF327：图 23.5/23.6 及图注、泊松过程到达时间式 (23.22)、对数正态式 (23.23)–(23.25)、23.4 节 von Mises 式 (23.26)；已由不同 Agent 对照原页复核。图 23.5 图注与坐标轴变量不一致的原书疑点并列保留。
- [x] 初译 PDF328：缠绕高斯式 (23.27)、23.5 节的贝塔和狄利克雷分布、式 (23.28)–(23.33)、图 23.7 上下图及 logit 式、softmax 变换；已由不同 Agent 对照原页复核。
- [x] 初译 PDF329：式 (23.34)、图 23.8/23.9 及图内译注、狄利克雷参数说明和习题 23.3；已由不同 Agent 对照原页复核。
- [x] 初译 PDF330：习题 23.3 续题、熵分布式 (23.35)、KL 定义、延伸阅读、23.6 节与习题 23.4；已由不同 Agent 对照原页复核。
- [x] 编写本章简短中文导读，与原书正文区分，并经独立审查。
- [x] 逐节逐段翻译和核对正文、列表、习题及延伸阅读；PDF323–330 页段对应见 `translation/chapter-23/REVIEW.md`。
- [x] 对照原页核实 23.1–23.6 六节的标题、起始页和无编号小标题。
  - [x] 23.1 Distributions over integers（PDF323）
  - [x] 23.2 Distributions over unbounded real numbers（PDF324）
  - [x] 23.3 Distributions over positive real numbers（PDF325）
  - [x] 23.4 Distributions over periodic variables（PDF327）
  - [x] 23.5 Distributions over probabilities（PDF328）
  - [x] 23.6 Further exercises（PDF330）
- [x] 图 23.1–23.9 的全部面板、坐标、图内英文及图注逐张对照原页；本章无原书数据表。
- [x] 式 (23.1)–(23.35) 及两条无编号式逐式核对；四处原书疑点照印本保留并记录，网站 MathML 可读可复制。
- [x] 核对术语、交叉引用、目录及 1440/390/320px 浅深六视口排版；习题 23.3 长积分的横滑提示修复并复测通过。
- [x] 不同于初译者的 Agent 完成原页内容审查，另有独立草稿与正式网站 QA；见 `translation/chapter-23/REVIEW.md`、`SITE_QA.md`。
- [x] 正式 JSON 与审定草稿逐字节相同（119,936 字节，SHA-256 `51c0f39ea92dc8e5083d98a5d69a992f38865509f9641168d1fe3441cff2eb2b`）；`verify_registered.py`、全站 smoke、JS 语法及差异检查通过，本章验收完成。

## 第 24 章：Exact Marginalization（PDF 331–335）

- [x] 不同于初译者的 Agent 已完成 PDF331–335 独立原页审查，并复核 S24-01/S24-02 两处小标题层级修复；草稿与正式路径六视口网站 QA 均通过，见 `translation/chapter-24/REVIEW.md`、`SITE_QA.md`。
- [x] 初译 PDF331：章题、独立导读、两段章首正文、24.1、式 (24.1)、先验与共轭先验说明；已由不同 Agent 对照原页复核。式 (24.1) 根号横线经放大核对仅覆盖 $2\pi$。
- [x] 初译 PDF332：式 (24.2)–(24.4)、$1/\sigma$ 先验、页边变量变换提示与两无编号式、抽样理论和贝叶斯推断比较；已由不同 Agent 对照原页复核。
- [x] 初译 PDF333：图 24.1 四面板与图内英文译注、习题 24.1、式 (24.5)–(24.8) 与充分统计量；已由不同 Agent 对照原页复核。
- [x] 初译 PDF334：联合/条件/边缘后验、式 (24.9)–(24.14)、奥卡姆因子及跨页 $\chi^2$ 说明；已由不同 Agent 对照原页复核。
- [x] 初译 PDF335：习题 24.2/24.3、式 (24.15)、习题小图、延伸阅读、24.2/24.3 节及习题 24.1 解答；已由不同 Agent 对照原页复核。
- [x] 初译者已构建 `chapter-24.draft.json`：64 块、15 个编号式与 2 个无编号式、2 图、3 题，MathML 无错误；S24-01/S24-02 标题层级修复后独立源审和正式站点 QA 均通过。
- [x] 编写本章简短中文导读，与原书正文区分，并经独立审查。
- [x] PDF331–335 的正文、习题、答案、延伸阅读和跨页段落均经独立 Agent 逐页核对。
- [x] 原页核实 24.1–24.3 的标题、起始页及三个无编号小标题层级。
  - [x] 24.1 Inferring the mean and variance of a Gaussian distribution（PDF331）
  - [x] 24.2 Exercises（PDF335）
  - [x] 24.3 Solutions（PDF335）
- [x] 图 24.1 四面板与习题 24.3 无编号小图的坐标、曲线、图内英文和相邻译注逐一核对；本章无数据表。
- [x] 式 (24.1)–(24.15) 及两条无编号页边式逐式核对，根号覆盖范围经放大原页复核；网站 MathML 可读可复制。
- [x] 核对术语、交叉引用、目录及 1440/390/320px 浅深六视口排版；两图手机端左右端均目视复核。
- [x] 不同于初译者的 Agent 记录并复核 S24-01/S24-02 两处小标题层级修复；草稿及正式路径独立网站 QA 均通过。
- [x] 正式 JSON 与审定草稿逐字节相同（SHA-256 `cc72ad568f48ba858d2b9351de730afd377523161217d6195c2f2a8f4d40754`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 25 章：Exact Marginalization in Trellises（PDF 336–345）

- [x] 不同于初译者的 Agent 已完成 PDF336–345 独立原页内容审查，含 4 张数据表逐格复核；草稿与正式路径六视口网站 QA 均通过，见 `translation/chapter-25/REVIEW.md`、`SITE_QA.md`。
- [x] 初译 PDF336：章题、独立导读、25.1 两类译码问题、式 (25.1)/(25.2) 及跨页高斯信道引句；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF337：式 (25.3)–(25.6)、习题 25.1、最可能码字/MAP 与最小和段落；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF338：图 25.1、式 (25.7)–(25.11)、25.2 节与格形图定义；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF339：线性格形图定义与性质、习题 25.2、25.3 节开头及跨页例 25.3；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF340：图 25.2 的 16 行概率条、式 (25.12)、例 25.3 两种译码结果和跨页过渡；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF341：图 25.3 七行概率、习题 25.4、最小和／和积算法及无编号初始化式；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF342：式 (25.13)–(25.16)、习题 25.5–25.9 与表 25.4 的六个似然值；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF343：25.4 节、表 25.5 码字与跨度、式 (25.17)–(25.19) 的矩阵；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF344：图 25.6/25.7、式 (25.20) 的 $3\times7$ 矩阵及校验矩阵构图跨页句；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF345：表 25.8 的 16 行、无编号后验边缘表及习题 25.4/25.9 解答；初译者已对照原页，待全章独立审查。原书解答 25.9 三个逐位概率均标 $t_1$ 的疑点照印本保留。
- [x] 初译者完成 PDF336–345 十页自核并构建 `chapter-25.draft.json`：134 块、6 项目录、20 个编号式加 2 个无编号式、6 图、8 题、4 表；独立原页及正式网站 QA 均通过。
- [x] 编写本章简短中文导读，与原书正文区分，并经独立审查。
- [x] PDF336–345 正文、例 25.3、习题、解答、列表和参考均逐页原图核对。
- [x] 原页核实 25.1–25.5 五节标题、起始页与无编号小标题。
  - [x] 25.1 Decoding problems（PDF336）
  - [x] 25.2 Codes and trellises（PDF338）
  - [x] 25.3 Solving the decoding problems on a trellis（PDF339）
  - [x] 25.4 More on trellises（PDF343）
  - [x] 25.5 Solutions（PDF345）
- [x] 图 25.1–25.3、25.6/25.7 和表 25.8 原图完整；表 25.4、25.5、25.8 与无编号边缘概率表共四张数据表逐格核对，七位码字手机端单行横滑。
- [x] 式 (25.1)–(25.20)、两条无编号初始化式与矩阵逐式核对；原书习题 25.9 解答三处 $t_1$ 下标照录并记录，网站 MathML 可读可复制。
- [x] 核对术语、交叉引用、目录及 1440/390/320px 浅深六视口排版，24↔25 章导航、末页 100% 与三次刷新通过。
- [x] 不同于初译者的 Agent 完成原页内容审查；另有独立草稿与正式路径网站 QA；表 25.5 的码字断行已修复并复测。
- [x] 正式 JSON 与审定草稿逐字节相同（120,843 字节，SHA-256 `b38c0f3e24beece23b710aa683e81088b413d52badccdc0ea4340cf253492b4f`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 26 章：Exact Marginalization in Graphs（PDF 346–352）

- [x] 不同于初译者的 Agent 已逐页完成 PDF346–352 原页内容审查，并在修复段落、强调、语义及图裁边后复核通过；草稿与正式路径六视口网站 QA 均通过，见 `translation/chapter-26/REVIEW.md`、`SITE_QA.md`。
- [x] 初译 PDF346：章题、独立导读、26.1、式 (26.1)–(26.4) 中五个分段因子与归一化函数及变量子集说明；已对照原页并构建部分草稿，待独立审查。
- [x] 初译 PDF347：图 26.1 及标签译注、归一化与边缘化问题、式 (26.5)–(26.9)、习题 26.1 和树状图限定；已对照原页并构建部分草稿，待独立审查。
- [x] 初译 PDF348：26.2、记号与消息定义、规则框内式 (26.11)/(26.12)、叶节点说明与图 26.2/26.3；已对照原页，整章构建时仍须保留原书规则框。
- [x] 初译 PDF349：式 (26.13)–(26.17)、图 26.4、边缘分布与习题 26.2–26.5；已对照原页并构建部分草稿，待独立审查。
- [x] 初译 PDF350：归一化消息式 (26.18)/(26.19)、因子分解式 (26.20)–(26.23)、习题 26.6/26.7 与两处斜体小标题；已对照原页。原书式 (26.22) 分子印作 $f(\mathbf x_m)$，译稿照录待独立复核。
- [x] 初译 PDF351：计算技巧、式 (26.24)/(26.25)、26.3 最小和算法开头、最大化问题与式 (26.26)；已对照原页。
- [x] 初译 PDF352：26.3 收尾、26.4 联结树算法、延伸阅读、26.5 习题及 26.8；已对照原页。
- [x] 初译者已构建并修订 `chapter-26.draft.json`：111 顶层块（含规则框内 4 子块）、26 个编号式、4 图、8 题；MathML 无错误，独立原页及草稿网站 QA 均通过。
- [x] 编写本章简短中文导读，与原书正文区分，并经独立审查。
- [x] PDF346–352 正文、八题、延伸阅读、跨页句及原书斜体强调逐页原页核对。
- [x] 原页核实 26.1–26.5 五节和九处斜体无编号小标题的层级。
  - [x] 26.1 The general problem（PDF346）
  - [x] 26.2 The sum–product algorithm（PDF348）
  - [x] 26.3 The min–sum algorithm（PDF351）
  - [x] 26.4 The junction tree algorithm（PDF352）
  - [x] 26.5 Exercises（PDF352）
- [x] 图 26.1–26.4 的节点、连线、箭头、标签及相邻译注逐张核对；图 26.1 底边图注残片已裁净。本章无数据表。
- [x] 式 (26.1)–(26.26) 连续、规则 (26.11)/(26.12) 保持原书同一边框；式 (26.22) 原书分子 $f(\mathbf x_m)$ 照录并经独立复核，网站 MathML 可读可复制。
- [x] 核对术语、交叉引用、目录及 1440/390/320px 浅深六视口排版；公式与图手机端局部横滑正常。
- [x] 不同于初译者的 Agent 记录并复核原页问题，另由独立 Agent 完成草稿与正式路径网站 QA。
- [x] 正式 JSON 与审定草稿逐字节相同（97,253 字节，SHA-256 `4d797836ff0bd5fb61d75225a0fa0de6aa5b845ef927577aa5c8d7c078aee725`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 27 章：Laplace’s Method（PDF 353–354）

- [x] 初译 PDF353–354 及简短中文导读，形成未注册 `chapter-27.draft.json`：41 块、式 (27.1)–(27.14)、原书无编号示意图、习题 27.1–27.3；初译者和独立 Agent 均已对照原页。
- [x] 不同于初译者的 Agent 逐页完成 PDF353–354 原页源审；草稿和正式路径六视口网站 QA 均通过，见 `translation/chapter-27/REVIEW.md`、`SITE_QA.md`。
- [x] 编写本章简短中文导读，与原书正文区分，并经独立审查。
- [x] 两页正文、图内译注、习题 27.1–27.3 及交叉引用逐项对照原页。
- [x] 原页核实本章唯一编号小节 27.1 Exercises（PDF354）及其标题层级。
- [x] 原书无编号四层示意图完整保留，$P^*(x)$、$\ln P^*(x)$、$\ln Q^*(x)$、$Q^*(x)$ 的图内标记紧邻译注；本章无数据表。
- [x] 式 (27.1)–(27.14) 的变量、转置、行列式、上下标逐式核对，网站 MathML 可读可复制。
- [x] 核对术语、引用、目录及 1440/390/320px 浅深六视口排版；26↔27 章导航和末页进度刷新通过。
- [x] 不同于初译者的 Agent 完成源文内容审查；另有独立草稿与正式路径网站 QA，无待修问题。
- [x] 正式 JSON 与审定草稿逐字节相同（31,974 字节，SHA-256 `525eec37ced6daa272d96ecc516f0e692086833e4f2d36056074b9a901ccc51d`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 28 章：Model Comparison and Occam’s Razor（PDF 355–367）

- [x] 初译 PDF355：章题、明确区分的简短导读、28.1 节开头、图 28.1/28.2 的原页裁图及图内英文译注；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF356：图 28.3 原页裁图、长图注与图内译注，式 (28.1)、无编号数列及奥卡姆剃刀的贝叶斯解释；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF357：两模型的先验设定、式 (28.2)/(28.3) 的四个因子、$2.5\times10^{-12}$ 与四千万比一比较，以及跨页奥卡姆因子说明；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF358：图 28.4 全部流程框和底部 “Choose future actions” 原图/中文译注、贝叶斯方法的两层推断与跨页决策理论段落；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF359：两层推断中的模型拟合、式 (28.4)/(28.5)、无编号“后验＝似然×先验／证据”及跨页方括号说明；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF360：图 28.5 与单参数奥卡姆因子图注、列表第 2 项、式 (28.6)/(28.7) 及证据评估开头；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF361：式 (28.8)/(28.9)、原书下括号“最佳拟合似然×奥卡姆因子”、后验/先验体积解释与图 28.6 前置说明；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF362：图 28.6 点云、曲线与长图注，式 (28.10) 的行列式和下括号、Hessian 与多参数奥卡姆因子；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF363：图 28.7 与图内英文译注、树后盒子的一/二模型设定、式 (28.11)–(28.14) 的分数因子及约 $1000:1$ 结论；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF364：图 28.8 三模型编码条与长图注、三段符号说明，28.3 节 MDL 及式 (28.15)–(28.17)；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF365：式 (28.18)/(28.19)、在线学习与留一交叉验证、比特回收编码、延伸阅读及跨页正规先验结论；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF366：习题 28.1–28.4 起始、式 (28.20)–(28.22)、326 案件的四行列联表和两幅无编号习题原图；初译者已对照原页，习题 28.4 跨页承接待全章自核。
- [x] 初译 PDF367：习题 28.4 跨页结论、辛普森悖论、模型比较限制、四模型参数/先验问题和图 28.9 四幅 DAG；初译者已对照原页，整章草稿与自核正在进行。
- [x] 初译者完成 PDF355–367 十三页自核：133 块、式 (28.1)–(28.22) 加 2 条无编号式、11 图、4 题、1 表；独立原页及六视口草稿网站审查通过，正式 JSON 与审定草稿逐字节相同。
- [x] 编写本章简短中文导读，与原书正文区分；独立审查通过。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、答案与参考文献；核对页段对应关系，见 `translation/chapter-28/REVIEW.md`。
- [x] 逐页原图核实并翻译以下小节、段落和无编号小标题。
  - [x] 28.1 Occam’s razor（PDF355 起）
  - [x] 28.2 Example（PDF363 起）
  - [x] 28.3 Minimum description length (MDL)（PDF364 起）
  - [x] 28.4 Exercises（PDF366 起）
- [x] 逐项核对图 28.1–28.9、两张无编号习题图、图内英文、图注与列联表每个单元格；见独立审查记录。
- [x] 逐项核对式 (28.1)–(28.22) 与两条无编号式的变量、上下标、编号和页码；正式网站 24 式 MathML 显示及复制通过。
- [x] 核对术语、交叉引用、目录、窄屏和深色模式排版；六视口正式路径通过。
- [x] 不同于初译者的 Agent 完成 PDF355–367 原页审查及草稿／正式网站审查，见 `translation/chapter-28/REVIEW.md`、`SITE_QA.md`。
- [x] 修复并独立复核原书斜体、图 28.1 窄屏布局和 PDF356 两处短尾行；正式 JSON 为 176,305 字节，SHA-256 `fbf6baadc9716c887a91c3ea6528f3f0fd8c7bc557a0bf296ece5d67ebb12515`。真实路径、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 29 章导页（PDF 368）

- [x] 初译者已对照原 PDF368 完成七段正文、式 (29.1)/(29.2)、独立导页层级和未注册 `chapter-29-intro.draft.json`；原页无图表。
- [x] 不同于初译者的 Agent 已对照原 PDF368 独立核对七段、采样方法、式 (29.1)/(29.2) 与下标/乘法方向；草稿及正式六视口网站 QA 通过，见 `translation/chapter-29-intro/REVIEW.md`、`SITE_QA.md`。
- [x] 对照原 PDF 独立翻译并核对 “About Chapter 29” 全文，包括蒙特卡罗方法导引及式 (29.1)–(29.2)；作为独立导页编排。
- [x] 原页无图表和习题；两式及下标、交叉引用经不同 Agent 独立审查，草稿六视口排版通过。
- [x] 第 28 章验收后注册本导页；正式 JSON 与审定草稿逐字节相同（8,831 字节，SHA-256 `352c87f220c19a60bfb52bcf6e39c48c7b94058d17c95a162b1becfdfdd9a637`）。独立正式六视口复核真实 28↔导页导航、10 块、2 式、14 行内 MathML、末页 100% 与三次刷新通过；`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，导页验收完成。导页→第 29 章正文导航待正文审查后验证。

## 第 29 章：Monte Carlo Methods（PDF 369–398）

- [x] 初译 PDF369–370：29.1 开头、两个问题、式 (29.3)–(29.10)、图 29.1 双面板、原书方框强调和跨页接续；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF371–372：式 (29.11)–(29.17)、伊辛模型与原书货币脚注、图 29.2/29.3、湖泊/峡谷类比、均匀采样及典型集；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF373–374：29.1 典型集样本数结论、29.2 重要性采样、式 (29.18)–(29.22)、习题 29.1、图 29.4–29.6 的原页裁图及两种采样密度；初译者已对照原页并合并跨页段落，待全章独立审查。
- [x] 初译 PDF375–376：重要性采样的重尾条件、推荐习题 29.2、高维球面与高斯分布的式 (29.23)–(29.28)、29.3 节拒绝采样开头、式 (29.29)、图 29.7/29.8 及跨页证明句；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF377–378：高维拒绝采样接受率、式 (29.30)、29.4 节及接受率式 (29.31)、接受／拒绝四步、MCMC 收敛与样本依赖性、图 29.9/29.10 及跨页接续；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF379–380：推荐习题 29.3、随机游走方框与式 (29.32)、图 29.11/29.12 及轨迹和六幅直方图的图内译注；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF381–382：玩具随机游走式 (29.33)/(29.34)、图 29.12 的 178/540 次迭代解读、高维 Metropolis 尺度分析、29.5 Gibbs 采样开头、条件分布及图 29.13 四面板；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF383–384：Gibbs 单变量更新式 (29.35)–(29.37)、习题 29.4/29.5、伴随式后验 (29.38)、BUGS 脚注、29.6 术语、式 (29.39)–(29.41)、例 29.6 的 21×21 无编号转移矩阵及图 29.14；初译者已对照原页，待全章独立审查。原书正文时间列与图内八幅标记不同，分别按原文/原图保留，待独立复核。
- [x] 初译 PDF385–386：遍历性第 2 项、式 (29.42)–(29.46)、可约性与周期性、基转移混合／串接、详细平衡、习题 29.7–29.9、29.7 节切片采样开头和图 29.15；初译者已对照原页，待全章独立审查。原书习题编号由 29.5 跳至 29.7，译稿未补造 29.6。
- [x] 初译 PDF387–388：切片采样框架、三组独立算法框、图 29.16 七幅步骤示意及完整图注；PDF387 页末跨整页图至 PDF389 才续完的性质段已合为完整段落并置于原书起始位置，网站顺序保留标题→段落→图。初译者已对照原页，待全章独立审查与算法框网站核验。
- [x] 初译 PDF389–390：跨图接续的切片采样性质段、图 29.17/29.18、习题 29.10/29.11、整数运算表、两段独立描边伪代码及图内端点译注；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF391–392：29.8／29.9 节、归一化常数的三种计算路线、作者判断、习题 29.12、式 (29.47)/(29.48) 和十二样本例子；初译者已对照原页，待全章独立审查。
- [x] 初译 PDF393–394：图 29.19 的三种资源分配策略、29.10 节五条总结与式 (29.49)、29.11 节开头、推荐习题 29.13/29.14 和式 (29.50)/(29.51)；习题 29.14 跨 PDF395 的两问并入完整题干，初译者已对照原页，待全章独立审查。
- [x] 初译 PDF395–396：习题 29.15–29.21、Octave 网址脚注、29.12 节解答开头及式 (29.52)/(29.53)；原书四处习题强调已补，式中 $x$ 的普通斜体字形按放大原页保留，待全章独立审查。
- [x] 初译 PDF397–398：习题 29.1/29.2/29.5/29.12/29.13 解答、式 (29.54)–(29.62)、图 29.20 三面板及图注；初译者已对照原页并保留两处原书内部叙述／式子的疑点，待独立逐页复核。
- [x] PDF369–398 三十页初译及图 29.1–29.20 源图已落盘；逐页初核完成，后续草稿、算法框和网页审查结果见本节章末验收记录。
- [x] 未承担初译的 Agent 已逐页初审 PDF369–398 全 30 页，覆盖 60 条编号式、20 图、20 道习题和 5 道原书解答；S29-01、03–11 的源文问题已修并独立复核，两处印本疑点另记。最终草稿的框体、页面对应和网站 QA 已在后续验收通过，见 `translation/chapter-29/REVIEW_PARTIAL.md`、`REVIEW.md`、`SITE_QA.md`。
- [x] 初译者构建 `chapter-29.draft.json` 并自核 13 项目录、60 条编号式加一条无编号矩阵、20 图、20 题、7 个描边框、3 脚注、5×2 运算表、840 个行内 MathML；PDF389 表格解析问题和 PDF370/379 框内多余引文竖线已修。草稿 SHA-256 `b0dda7c7b61a9d58d60261e0acd5a87a7f77a512359fbdd3da900de0894cb35c`，独立全章原页与网站审查通过。
- [x] 独立分段源审发现 PDF369 式 (29.4) 的花体期望算子和 PDF380 图 29.12 左侧“(a)”裁断；初译者修复后由审查 Agent 对照原页复核通过。
- [x] 独立原页审查发现的 PDF373、375、377、378、384、385、391、392、395、396、397、398 强调样式差异已修并复核，见 `translation/chapter-29/REVIEW.md`。
- [x] PDF370/379 原书两个论述框分别保留完整外框；PDF379 标题、说明、式 (29.32) 与结尾同框，五个算法框独立，框内公式与代码已由独立 Agent 核对；网站视觉验收通过。
- [x] 编写本章简短中文导读，与原书正文区分，独立源审通过。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、解答与参考文献；三十页逐页原页审查通过，见 `translation/chapter-29/REVIEW.md`。
- [x] 逐页原图核实并翻译以下小节、段落和无编号小标题。
  - [x] 29.1 The problems to be solved（PDF369 起）
  - [x] 29.2 Importance sampling（PDF373 起）
  - [x] 29.3 Rejection sampling（PDF376 起）
  - [x] 29.4 The Metropolis–Hastings method（PDF377 起）
  - [x] 29.5 Gibbs sampling（PDF382 起）
  - [x] 29.6 Terminology for Markov chain Monte Carlo methods（PDF384 起）
  - [x] 29.7 Slice sampling（PDF386 起）
  - [x] 29.8 Practicalities（PDF391 起）
  - [x] 29.9 Further practical issues（PDF391 起）
  - [x] 29.10 Summary（PDF393 起）
  - [x] 29.11 Exercises（PDF394 起）
  - [x] 29.12 Solutions（PDF396 起）
- [x] 图 29.1–29.20 的原图、图内英文译注、图注和 PDF389 运算表每格均由独立 Agent 对照原页；图 29.12/29.20 重裁后复核。
- [x] 式 (29.3)–(29.62) 与无编号 21×21 矩阵的变量、粗体、上下标和编号、五段算法代码均由独立 Agent 对照原页；正式网站 61 式和五段代码复制、局部横滑与排版通过。
- [x] 核对术语、交叉引用、13 项目录、窄屏和深色模式排版；独立草稿及正式六视口 QA 通过。
- [x] 不同于初译者的 Agent 完成全章三十页及最终草稿独立源审，另一 Agent 完成草稿与正式六视口网站 QA，所有审查问题关闭，见 `translation/chapter-29/REVIEW.md`、`SITE_QA.md`。
- [x] 修复并独立复核花体／粗体公式、图 29.12/29.20 裁边、斜体、指示因子、表格错列及框内多余竖线。正式 JSON 与审定草稿逐字节相同（450,204 字节，SHA-256 `b0dda7c7b61a9d58d60261e0acd5a87a7f77a512359fbdd3da900de0894cb35c`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。源审及六视口正式回归见 `translation/chapter-29/REVIEW.md`、`SITE_QA.md`。

## 第 30 章：Efficient Monte Carlo Methods（PDF 399–410）

- [x] 初译 PDF399–400：章题、明确区分的简短导读、30.1 节、式 (30.1)–(30.3)、斜体小标题、算法 30.1 完整 Octave 代码与中文注释、图 30.2 四面板及图内译注；初译者已目视原页，待全章独立审查。原书代码中 `findE(xnew)` 的注释提及 $H$，照印本保留并记录。
- [x] 初译 PDF401–402：哈密顿蒙特卡罗细节、式 (30.4)–(30.7)、图 30.2(a)–(d) 说明、图 30.3 三面板与完整图注、30.2 节过松弛方法开头及跨页接续；初译者已目视原页，待全章独立审查。原书 p401 将 p400 的 Algorithm 30.1 称作 “figure 30.1”，按印本保留并记录。
- [x] 初译 PDF403–404：高斯条件分布的过松弛与有序过松弛、式 (30.8)、习题 30.1/30.2、30.3 模拟退火全节与式 (30.9)–(30.12)、30.4 节开头及跨页接续；初译者已对照原页，图 30.3 裁边重新核实，待全章独立审查。
- [x] 初译 PDF405–406：式 (30.13)、无编号蛙跳几何图及图内三点/箭头、斜体子题、习题 30.3、30.5 节的信息论视角、例 30.4、式 (30.14)、习题 30.5 和跨 PDF407 的题末接续；初译者已目视原页，待全章独立审查。
- [x] 初译 PDF407–408：习题 30.6–30.10、30.6 节多状态方法与“遗传方法”小节、式 (30.15)、交叉／选择机制、“粒子滤波器”小节及原书参考文献；初译者已目视原页，待全章独立审查。
- [x] 初译 PDF409–410：30.7／30.8／30.9 节、两行无编号联合密度式、延伸阅读、习题 30.11/30.12、无编号切片方向图及图内译注、解答与式 (30.16)–(30.18)；初译者已目视原页，待全章独立审查。
- [x] PDF399–410 十二页正文、编号图与无编号图初译及逐页自核完成；草稿、正式路径独立网站验收均通过。
- [x] 第 30 章分段独立源审发现 S30-01/02 的 PDF402–408 原书斜体范围差异，初译者修复后已独立复核；算法注释及“figure 30.1”两处原书疑点照印本保留。
- [x] 未承担初译的 Agent 已逐页核对 PDF399–410 全 12 页和稳定草稿；S30-01/02/03 均已修复并复核，源文与结构审查 PASS，见 `translation/chapter-30/REVIEW.md`。草稿与正式六视口网站 QA 均 PASS，见 `SITE_QA.md`。
- [x] 初译者完成十二页逐页自核并构建 `chapter-30.draft.json`：126 顶层／127 递归块、10 项目录、18 条编号式加一条无编号式、4 图、11 题和一个完整 Octave 算法框。四幅图、跨页句、MathML 与代码围栏自核通过，草稿 SHA-256 `d5bf197fcea6ea1d77093b42e4cdfcf3a8e6cc31eb9257e7eaf8b428b6fb42d8`；独立源文与草稿／正式网站审查 PASS。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页审查通过。
- [x] 逐节逐段翻译和核对正文、列表、脚注、习题、解答与参考文献；十二页原页审查通过。
- [x] 独立原页核实并翻译以下小节、段落和无编号小标题。
  - [x] 30.1 Hamiltonian Monte Carlo（PDF399 起）
  - [x] 30.2 Overrelaxation（PDF402 起）
  - [x] 30.3 Simulated annealing（PDF404 起）
  - [x] 30.4 Skilling’s multi-state leapfrog method（PDF404 起）
  - [x] 30.5 Monte Carlo algorithms as communication channels（PDF406 起）
  - [x] 30.6 Multi-state methods（PDF407 起）
  - [x] 30.7 Methods that do not necessarily help（PDF409 起）
  - [x] 30.8 Further exercises（PDF409 起）
  - [x] 30.9 Solutions（PDF410 起）
- [x] 核对图 30.2／30.3、两幅无编号图、图内英文译注与图注；原页无数据表，均见独立源审记录。
- [x] 核对式 (30.1)–(30.18) 与 PDF409 无编号式的变量、上下标、编号和算法 30.1 全部 Octave 代码行；正式网页 MathML 与代码复制、窄屏局部横滑通过。
- [x] 核对术语、交叉引用、10 项目录、窄屏和深色模式排版；独立六视口草稿及正式路径 QA 通过。
- [x] 不同于初译者的 Agent 完成全十二页原页与稳定草稿结构审查，另一 Agent 完成草稿和正式路径网站审查；S30-01/02/03 均关闭，见 `translation/chapter-30/REVIEW.md`、`SITE_QA.md`。
- [x] 正式 JSON 与审定草稿逐字节相同（142,007 字节，SHA-256 `d5bf197fcea6ea1d77093b42e4cdfcf3a8e6cc31eb9257e7eaf8b428b6fb42d8`）；`verify_registered.py`、全站 smoke、JS 语法和差异检查通过，本章验收完成。

## 第 31 章导页（PDF 411）

- [x] 初译者目视 PDF411 完成独立导页三段正文与 Ising 模型／神经网络关系；原页无式、图，已与第 30 章及第 31 章正文分离。
- [x] 独立 `chapter-31-intro.draft.json` 为 4 块、1 项目录、原书 3 段、无图式题；正式 JSON 与审定草稿逐字节相同（2,373 字节，SHA-256 `0e4ef0eb4e58e8e6ab1128fab51f8d6c2feff90622d6d26e71132738fce85ee1`）。
- [x] 不同于初译者的 Agent 已逐段目视核对 PDF411 “About Chapter 31” 全文、引用及原页无图式题的判断，源文与草稿结构审查 PASS，见 `translation/chapter-31-intro/REVIEW.md`。
- [x] 独立草稿与正式六视口网站 QA 均通过：30↔导页导航、4 块、页底 100% 与三次刷新稳定，无整页横溢或加载异常；`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-31-intro/SITE_QA.md`。导页↔第 31 章正文导航也在正文正式路径 QA 通过。

## 第 31 章：Ising Models（PDF 412–424）

- [x] 初译 PDF412：章题、非原书简短导读、式 (31.1)–(31.4)、原书斜体小标题以及跨 PDF413 的自旋玻璃／Hopfield 网络段；初译者已对照可视原页，待全章独立审查。
- [x] 初译 PDF413–414：接续自旋玻璃／Hopfield 网络段、斜体小标题、式 (31.5)–(31.20)、习题 31.1(a)/(b) 和 31.1 节开头；初译者已对照可视原页，待全章独立审查。PDF414 式 (31.12) 与前页推导符号不一致，按印本保留并记录。
- [x] PDF414 式 (31.12) 的印本正号与式 (31.8)/(31.9) 推导矛盾，译稿照印本保留；疑点已记 `translation/chapter-31/SOURCE_NOTES.md` 并经独立原页复核。
- [x] 初译 PDF415–416：式 (31.21)–(31.24)、斜体小标题、Schottky 异常、涨落与热容、图 31.1–31.4 的高分辨率源图及图内译注、跨整页图 PDF417 的反铁磁段落；初译者已目视原页，四图裁边与图内译注已由独立 Agent 对原页复核。全章仍待后续页与网站审查。
- [x] 初译 PDF417–418：原书纯图页 417 的图 31.5 八面板、图 31.6，以及 PDF418 图 31.7–31.10、奇数周期边界阻挫与三角网格模型段；六图按原 PDF 260dpi 裁取并配图内译注，PDF416→418 跨图页句只合并一次。初译者已目视核图，待独立复核。
- [x] 初译 PDF419–420：31.2 节转移矩阵法、式 (31.25)、图 31.11 六面板和原书纯图页 420 的图 31.12 九幅状态及温度标签；跨 PDF421 的段落在起始页合并一次。图 31.11/31.12 与段落已由独立 Agent 对原页复核。
- [x] 初译 PDF421 正文与式 (31.26)–(31.34)、图 31.13 长图注中的二进制状态与能量示例；正文和图资产均由独立 Agent 对原页复核，图的三行五列、节点/连线及边界完整。
- [x] 独立源审发现图 31.12 右下角混入半截原书英文图注；初译者留白该残片并保留左右九幅状态及 5+4 个温度标签，未承担初译的 Agent 对原页复核通过（S31-02）。
- [x] 图 31.13 原书裁图已落盘并独立核对；式 (31.28) 正号与式 (31.1) 能量符号不一致的印本疑点已记入 `translation/chapter-31/SOURCE_NOTES.md`，译稿仍照印本保留，注释经独立对页复核。
- [x] 初译 PDF422–423：图 31.14–31.19 六幅高分辨率裁图、英文图题／图例／轴名／温度刻度译注和基态简并段；PDF422→423 仅合为一个自然段，两页无新增编号式或习题。未承担初译的 Agent 已逐图逐段对页复核，未见待修项。
- [x] 初译 PDF424：与蒙特卡罗结果比较、31.3 节以及习题 31.2／31.3 的三角与鼠图标、两问和斜体强调；原页特征值改记 `λ`，译稿照印本保留。未承担初译的 Agent 已逐段对页复核；待稳定草稿结构与网页审查。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页与网站审查通过。
- [x] 逐节逐段核对 PDF412–424 共 13 页的正文、习题、跨页接续及页段关系；原页无表格、代码、脚注或本章习题解答。
- [x] 逐节对原页核实标题、起始页、段落和无编号小标题。
  - [x] 31.1 Ising models – Monte Carlo simulation（PDF414 起）
  - [x] 31.2 Direct computation of partition function of Ising models（PDF419 起）
  - [x] 31.3 Exercises（PDF424 起）
- [x] 对 PDF 原页逐项核对 19 幅原图、图内英文译注与图注，检查全部裁边与解码；原页无表格。
- [x] 图 31.1–31.19 连续，均已登记页码与译注；图 31.12 残留的半截英文图注已修复并独立复核。
- [x] 对原页逐项核对公式、变量、上下标、编号与术语；正式网页 MathML 可读可复制，窄屏公式局部横滑通过。
- [x] 编号式 (31.1)–(31.34) 连续，原页无无编号展示式或算法代码；式 (31.12)/(31.28) 印本疑点已准确记录并照原文保留。
- [x] 核对术语、交叉引用、4 项目录、窄屏和深色模式排版；草稿与正式路径 1440/390/320px 明暗六视口均通过。
- [x] 未承担初译的 Agent 完成全 13 页独立原页、稳定草稿结构与图资产审查，S31-01/02/03 均关闭，见 `translation/chapter-31/REVIEW.md`。
- [x] 修复并复核审查问题；原审定正式 JSON 与草稿逐字节相同（135,568 字节，SHA-256 `210e574184023956fcbbc43aff57652be64ad041a46cfe44ad863d731d0955b3`）；G-09 全书术语修订后当前正式 JSON 与新草稿逐字节相同（135,550 字节，SHA-256 `ad08db52a1fd0622b0a6b5a4830325c61e7d149d4210f40423a5647ea71aeb60`），独立复核见 `translation/GLOBAL_REVIEW.md`。独立草稿及正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查均通过，见 `translation/chapter-31/SITE_QA.md`。本章验收完成。

## 第 32 章：Exact Monte Carlo Sampling（PDF 425–433）

- [x] 初译 PDF425：章题、与原书正文区分的简短中文导读、32.1／32.2 节及斜体小标题；未承担初译的 Agent 已逐段对原页复核通过。
- [x] 初译 PDF426：图 32.1 四面板、坐标及完整图注；源图已裁取并由未承担初译的 Agent 对原页复核通过。
- [x] 初译 PDF427：过去耦合、单调性及相关数值示例；跨 PDF428–430 图页的同一段仅在此页合并一次，未承担初译的 Agent 已对原页复核通过。
- [x] 独立源审 S32-01：PDF427 `two trajectories never cross` 的译法改为“不会彼此穿越”，避免读作轨迹不能汇合；初译者已修 PDF427／430，PDF427 已独立对原页复核通过。
- [x] 初译 PDF428–429：两页图 32.2／32.3 已保留全部面板、坐标、`T₀` 标记及箭头，图注完整翻译，未承担初译的 Agent 已逐图对原页复核通过。
- [x] 初译 PDF430：32.3 节、算法 32.4 的原框图与逐步中文译文、图 32.5 及跨 PDF431 的末段已落稿；未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF431：六自旋状态的四种展开、两条脚注网址、延伸阅读、耦合的其他用途与式 (32.1)；式后跨 PDF432 的段落仅在本页合并一次，未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF432–433：图 32.6、32.4 节六道习题及空心三角标记、32.5 节习题 32.1 的完整解答；习题 32.4 的跨页段落只合一次。未承担初译的 Agent 已逐页对原书及稳定草稿结构复核通过。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页与网站审查通过。
- [x] 逐节逐段核对 PDF425–433 共九页正文、两脚注、六道习题、唯一解答、跨页段落与页段对应关系；原页无数据表。
- [x] 逐节对原页核实标题与起始页，保留无编号斜体小标题。
  - [x] 32.1 The problem with Monte Carlo methods（PDF425 起）
  - [x] 32.2 Exact sampling concepts（PDF425 起）
  - [x] 32.3 Exact sampling from interesting distributions（PDF430 起）
  - [x] 32.4 Exercises（PDF432 起）
  - [x] 32.5 Solutions（PDF433 起）
- [x] 对原页逐项核对五幅图、算法框、图内英文与图注；原页无数据表。
- [x] 图 32.1–32.3、算法 32.4、图 32.5–32.6 共六个原书图像资源均已核对编号、边界、译注与解码。
- [x] 对原页逐项核对编号式、无编号式、变量、上下标、算法内容；正式网页 MathML 可读可复制且无 `merror`，窄屏局部横滑通过。
- [x] 式 (32.1) 为本章唯一编号式；另有 PDF431 六自旋状态的一条无编号展示式，已独立对原页核实。
- [x] 核对术语、交叉引用、6 项目录、窄屏和深色模式排版；草稿与正式路径 1440/390/320px 明暗六视口均通过。
- [x] 未承担初译的 Agent 已完成全九页原页与稳定草稿结构审查，S32-01 关闭，见 `translation/chapter-32/REVIEW.md`。
- [x] 修复并复核 S32-01；正式 JSON 与审定草稿逐字节相同（58,899 字节，SHA-256 `75c062af6f29b372fa9521e8876f6647008a1a5c2ed711b999802a2dfc6ead82`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-32/SITE_QA.md`。本章验收完成。

## 第 33 章：Variational Methods（PDF 434–448）

- [x] 初译 PDF434：章题、与原书正文区分的简短中文导读、33.1 节、式 (33.1)–(33.4)、Gibbs 不等式页边提示及斜体小标题；跨 PDF435 的末段仅合并一次，未承担初译的 Agent 已逐页复核通过。
- [x] 初译 PDF435：式 (33.5)–(33.11)、变分自由能与可计算性两处斜体小标题、自由能上界和配分函数下界关系；式 (33.7) 原书恒等号 `≡` 已照录，未承担初译的 Agent 已逐式对原页复核通过。
- [x] 初译 PDF436：33.2 节、独立自旋可分离近似、熵与平均自旋的关系及式 (33.12)–(33.20)；未承担初译的 Agent 已逐式对原页复核通过。
- [x] 初译 PDF437：式 (33.21)–(33.27)、图 33.1 的曲面与等高线及图注、平均场异步更新；跨 PDF438 的两点编号列表仅合并一次，未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF438：图 33.2 的三组 `h` 标记、坐标与图注，33.3 节、式 (33.28)–(33.31)；叉形分岔段跨 PDF439 仅合并一次，未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF439：式 (33.32)–(33.33)、推荐习题 33.1、33.4 节开头与跨纯图页 PDF440 至 441 的后验分布段；未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF440：原书整页图 33.3 五面板的原始高分辨率图、图注及图内英文标题／图例中文译注；未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF441：式 (33.34)–(33.37)、33.5 节高斯后验开头、五条原书文献引用及 ensemble learning／variational Bayes 术语；式 (33.36) 的两个先验因子已由未承担初译的 Agent 对原页复核通过。
- [x] 初译 PDF442：图 33.4 六面板及坐标箭头、完整图注、式 (33.38)–(33.43)、两段优化小标题与 `P(σ)→P(β)` 页边提示；未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF443：式 (33.44)–(33.46)、联合最优解、原书描边结论框、VIBES／BUGS 引文及 33.6 节开头；未承担初译的 Agent 已对原页内容复核通过，原书 `σ`／`β` 记号疑点照印本保留并记录。
- [x] 独立审查 S33-01：PDF443 原书完整描边结论框已在草稿中编为单个 outlined 框，学生提问仍为框外普通引文；源审及草稿／正式六视口视觉复核均通过。
- [x] 初译 PDF444：插曲收束、33.7 节 K 均值／EM 的变分推导、式 (33.47)–(33.51)，保留潜变量、`θ` 维度积分及分配／更新步骤；未承担初译的 Agent 已逐式对原页复核通过。
- [x] 初译 PDF445：图 33.5 原图、图内上下界不等式与 `λ(ν)` 定义的中文译注、习题 33.2–33.4、33.8 节、式 (33.52)–(33.53)；跨 PDF446 的预测分布与文献段仅合并一次，未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF446：Bethe／Kikuchi 延伸阅读、六条引文、33.9 节、推荐习题 33.5–33.7 与式 (33.54)；习题 33.7 跨 PDF447 的两条无编号 KL 目标式及 `P(x,y)` 4×4 表已合并，16 格由未承担初译的 Agent 对原页逐格复核通过。
- [x] 初译 PDF447：33.10 节习题 33.5 解答、一条无编号高斯 KL 展示式、式 (33.55)–(33.59) 和逆方差平均值示例；PDF447 页首跨页题／表只在 PDF446 放置一次，未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF448：图 33.6 两幅高斯等高线原图与完整图注、式 (33.60)–(33.62) 及习题 33.6 解答；未承担初译的 Agent 已对原页复核通过。
- [x] 初译者已构建并自核 `chapter-33.draft.json`（216 顶层块、11 项目录、62 个连续编号式与 3 条无编号式、6 图、7 题、1 张概率表）；稳定 SHA-256 `db1388fc5146e1cee08b4c551d0d02cdfacc2b43416e1db2d14a57d653d5eeb5`，独立原页、草稿结构与网站审查均通过。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页与网站审查通过。
- [x] 逐节逐段核对 PDF434–448 共 15 页正文、列表、七题、两解答、参考文献、页边提示及跨页段落；原页内容与稳定草稿结构独立审查通过。
- [x] 逐节对原页核实标题、起始页及斜体小标题。
  - [x] 33.1 Variational free energy minimization（PDF434 起）
  - [x] 33.2 Variational free energy minimization for spin systems（PDF436 起）
  - [x] 33.3 Example: mean field theory for the ferromagnetic Ising model（PDF438 起）
  - [x] 33.4 Variational methods in inference and data modelling（PDF439 起）
  - [x] 33.5 The case of an unknown Gaussian: approximating the posterior（PDF441 起）
  - [x] 33.6 Interlude（PDF443 起）
  - [x] 33.7 K-means clustering and the expectation–maximization algorithm as a variational method（PDF444 起）
  - [x] 33.8 Variational methods other than free energy minimization（PDF445 起）
  - [x] 33.9 Further exercises（PDF446 起）
  - [x] 33.10 Solutions（PDF447 起）
- [x] 对原页逐项核对六幅图、图内英文译注及图注；`P(x,y)` 概率表 5×5 含表头逐格核对。
- [x] 图 33.1–33.6 连续，均已登记页码、图注与图内译注；图像可解码且尺寸匹配。
- [x] 对原页逐项核对公式、变量、上下标、编号及原书框与表；正式网页 65 式可复制，窄屏局部横滑通过。
- [x] 式 (33.1)–(33.62) 连续，另有三条无编号展示式；原书 PDF443／444 的两处记号或排印歧义已记录在 `SOURCE_NOTES.md`。
- [x] 核对术语、交叉引用、11 项目录、窄屏和深色模式排版；草稿与正式路径 1440/390/320px 明暗六视口均通过，320px 标题孤字问题已修复。
- [x] 未承担初译的 Agent 已完成全 15 页原页及稳定草稿结构审查，S33-01 已关闭，见 `translation/chapter-33/REVIEW.md`。
- [x] 修复并复核 S33-01 与窄屏标题断行问题；正式 JSON 与审定草稿逐字节相同（218,394 字节，SHA-256 `db1388fc5146e1cee08b4c551d0d02cdfacc2b43416e1db2d14a57d653d5eeb5`）。独立草稿及正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查均通过，见 `translation/chapter-33/SITE_QA.md`。本章验收完成。

## 第 34 章：Independent Component Analysis and Latent Variable Modelling（PDF 449–456）

- [x] 初译 PDF449：章题、与原书正文区分的简短中文导读、34.1／34.2 节、图 34.1 原图与图内标记中文译注、式 (34.1) 及跨 PDF450 引句；未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF450：式 (34.2)–(34.13)、无噪声假设、似然函数斜体小标题、`δ` 边缘化及求和约定；未承担初译的 Agent 已逐式对原页复核通过。
- [x] 初译 PDF451：算法 34.2 原书完整框图及三步骤中文译注、式 (34.14)–(34.18)、在线梯度上升规则与 `φ` 的选择；未承担初译的 Agent 已对原页复核通过。
- [x] 独立源审 S34-01：算法 34.2 框内第 2 步已按印本恢复 `φ=-tanh(a_i)`，与后文式 (34.17) 的带下标写法分别保留；未承担初译的 Agent 已独立复核修复。
- [x] 初译 PDF452：图 34.3 四面板原图与逐项中文图注、带 `β` 的 tanh 先验、34.3 节及协变优化小标题；未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF453：式 (34.19)–(34.20)、协变原则、量纲分析、度量与曲率／牛顿方法及页边迭代次数说明；式 (34.20) 的 `i`／`i′` 下标照印本保留，未承担初译的 Agent 已对原页复核并要求记录印本疑点。
- [x] 初译 PDF454：式 (34.21)–(34.28)、二阶导数、`Σ/D` 近似、协变更新式与反向传递量；未承担初译的 Agent 已逐式对原页复核通过。
- [x] 初译 PDF455：算法 34.4 原框图与四步骤中文译注、式 (34.29)、自然梯度、延伸阅读引文和“无限模型”开头；跨 PDF456 的簇层级段落仅合并一次，未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF456：无限混合模型正文及引文、34.4 节五道习题、因子分析定义与式 (34.30)；未承担初译的 Agent 已对原页复核通过。
- [x] 独立源审 S34-02：习题 34.5 难度已恢复印本的 `$4^C$` 上标，未承担初译的 Agent 已独立复核修复。
- [x] 初译者已构建并自核 `chapter-34.draft.json`（109 块、5 项目录、式 (34.1)–(34.30) 连续、四个原书图像资源含两个算法框、五道习题）；标题三段呈现调整后的稳定 SHA-256 `9741fecad1e6957ec28b5b4a13c2202154e8a385e175224c4476f53ecc03e2d4`，原 `text` 与目录不变，已通过新草稿独立源审和网站审查。
- [x] 独立网站审查 S34-SITE-01：320px 章题把“独立”拆行的问题已以三段呈现修复；独立 Agent 在浅／深两模式截图核为完整三行，草稿与正式六视口回归均通过。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页与网站审查通过。
- [x] 逐节逐段核对 PDF449–456 共八页正文、算法、五题、引文及跨页接续；独立原页与稳定草稿结构审查通过。
- [x] 逐节对原页核实标题、起始页及斜体小标题。
  - [x] 34.1 Latent variable models（PDF449 起）
  - [x] 34.2 The generative model for independent component analysis（PDF449 起）
  - [x] 34.3 A covariant, simpler, and faster learning algorithm（PDF452 起）
  - [x] 34.4 Exercises（PDF456 起）
- [x] 对原页逐项核对图 34.1／34.3 及算法 34.2／34.4 原框、图内英文与中文译注；原页无数据表。
- [x] 四个图像资源的编号、裁边、解码及算法 3／4 步译注已独立核对。
- [x] 对原页逐项核对式、变量、上下标、两算法内容；正式网页 30 式可复制，窄屏局部横滑通过。
- [x] 式 (34.1)–(34.30) 连续；式 (34.20) 印本 `i`／`i′` 下标疑点照原文保留并记录。
- [x] 核对术语、交叉引用、5 项目录、窄屏和深色模式排版；草稿与正式路径 1440/390/320px 明暗六视口均通过。
- [x] 未承担初译的 Agent 已完成全八页原页与稳定草稿结构审查，S34-01/02 关闭，见 `translation/chapter-34/REVIEW.md`。
- [x] 修复并复核 S34-01/02 与窄屏标题断词问题；正式 JSON 与审定草稿逐字节相同（104,748 字节，SHA-256 `9741fecad1e6957ec28b5b4a13c2202154e8a385e175224c4476f53ecc03e2d4`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-34/SITE_QA.md`。本章验收完成。

## 第 35 章：Random Inference Topics（PDF 457–462）

- [x] 初译 PDF457：章题、与原书正文区分的简短中文导读、35.1 节、例 35.1 的三个无编号常量式、图 35.1 米／英尺／英寸图内译注、式 (35.1) 及解答起段；未承担初译的 Agent 已对原页及图资产复核通过。
- [x] 初译 PDF458：式 (35.2)–(35.3)、本福特定律、原书无编号页边对数区间示意图及译注、习题 35.2／35.3、35.2 节与跨 PDF459 的习题 35.4；跨页末问与二十个观测数已由未承担初译的 Agent 对原页复核通过。
- [x] 初译 PDF459：35.3 节、推荐习题 35.5 鼠图标、似然等价／先验等价论述、二元变量模型及跨 PDF460 的式 (35.4) 列联计数与提示式 (35.5)，连成一道完整习题；未承担初译的 Agent 已对原页及跨页数据复核通过。
- [x] 独立源审 S35-01：式 (35.4) 列联计数表的横线已由跨四列改为嵌套 MathML 表中仅跨两计数列的局部线；源审对原页与 `rowlines` 结构、网站审查对实际线型均复核通过。
- [x] 初译 PDF460：35.3 节末、35.4 节、式 (35.6)、习题 35.6–35.8；习题 35.7 原书无表头 8×6 布局及 43 个非空字符串已由未承担初译的 Agent 对原页逐格复核，跨 PDF461 无编号式已保留。
- [x] 初译 PDF461：习题 35.8 跨页末问与无编号四点数轴图、图 35.2、35.5 解答节及式 (35.7)–(35.11)；解答末段跨 PDF462 仅合并一次，Octave 脚注正文和网址已由独立 Agent 对终页复核通过。
- [x] 初译 PDF462：式 (35.12)–(35.15)、图 35.3 双纵轴曲线与图内译注、习题 35.4／35.5 解答末段及 Octave 脚注网址；未承担初译的 Agent 已对终页和稳定草稿结构复核通过。
- [x] 初译者已构建并自核 `chapter-35.draft.json`（84 块、6 项目录、15 个连续编号式与 5 条无编号式、5 图含两幅无编号图、7 道习题、8×6 无表头数据表、1 脚注）；最终 SHA-256 `09b4071b6c517bd62d3f57c9624da76fa52b4ced0d127efc1a7e49793947bdc8`。三处宽图标志及章题 HTML 两次差异均经独立逐字节核验，正文与目录未变；正式 JSON 同 SHA。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页与网站审查通过。
- [x] 逐节逐段核对 PDF457–462 共六页正文、图、题、解答、脚注及跨页关系，独立原页与稳定草稿结构审查通过。
- [x] 逐节对原页核实标题、起始页及斜体小标题。
  - [x] 35.1 What do you know if you are ignorant?（PDF457 起）
  - [x] 35.2 The Luria–Delbrück distribution（PDF458 起）
  - [x] 35.3 Inferring causation（PDF459 起）
  - [x] 35.4 Further exercises（PDF460 起）
  - [x] 35.5 Solutions（PDF461 起）
- [x] 对原页逐项核对五幅图（含两幅无编号图）、图内英文与图注；习题 35.7 的 8×6 无表头字符串表逐格核对。
- [x] 图 35.1–35.3 加两幅无编号图均已登记页码、译注并可解码。
- [x] 独立网站审查 S35-SITE-02：三幅宽图已改为手机局部横滑，320px 深色复测刻度可读；习题 35.7 的 8×6 表格逐格与局部横滑通过。
- [x] 独立网站审查 S35-SITE-01／03：式 (35.4) 的局部横、竖线已按原页在六视口复测；末脚注的物理页进度保存为 PDF462，六视口各三次刷新稳定。
- [x] 独立网站审查 S35-SITE-04：390／320px 章题拆开“若干”及 390px 的 35.1 节标题孤行均已修复，六视口复测通过。
- [x] 对原页逐项核对编号式、无编号式、变量、上下标和式 (35.4) 局部表线；草稿与正式网站的 20 式可复制、可见线型均通过。
- [x] 式 (35.1)–(35.15) 连续，另有五条无编号展示式；习题 35.6 的印本自身矛盾照原文保留并记录。
- [x] 核对术语、交叉引用、6 项目录、窄屏和深色模式排版；草稿与正式网站六视口审查通过。
- [x] 未承担初译的 Agent 已完成全六页原页与稳定草稿结构审查，S35-01 源文结构已关闭，见 `translation/chapter-35/REVIEW.md`。
- [x] S35-01 与 S35-SITE-01–04 均修复并独立复核；正式 JSON 与审定草稿逐字节相同（78,330 字节，SHA-256 `09b4071b6c517bd62d3f57c9624da76fa52b4ced0d127efc1a7e49793947bdc8`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-35/REVIEW.md`、`SITE_QA.md`。本章验收完成。

## 第 36 章：Decision Theory（PDF 463–468）

- [x] 初译 PDF463：章题、与原书正文区分的简短中文导读、式 (36.1)、36.1 节理性勘探开头及跨 PDF464 的页末括注；未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF464：页边 Gaussian 记号、式 (36.2)–(36.10)、习题 36.1／36.2 及鼠图标；未承担初译的 Agent 已对原页复核通过。
- [x] 初译 PDF465：式 (36.11)–(36.14)、习题 36.3、图 36.1 及 36.2 节延伸阅读；未承担初译的 Agent 已对原页、图资产及式 (36.13) 的印本负号复核通过。
- [x] 初译 PDF466：36.3 节、习题 36.4–36.6 的已出现部分，四门问题、阿莱悖论和最优停止题；未承担初译的 Agent 已对原页复核，S36-01 修复后关闭。
- [x] 独立源审 S36-01：PDF466 习题 36.5 的原书斜体及习题 36.4／36.6 的直立题名强调样式已由初译者修复、独立 Agent 对原页复核关闭。
- [x] 初译 PDF467：习题 36.7、表 36.2／36.3 的数值与双层表头、习题 36.8 跨页首句；未承担初译的 Agent 已对原页逐段、逐格复核通过。
- [x] 初译 PDF468：习题 36.8 的式 (36.15)／(36.16)、`W` 定义与追问、习题 36.9 两轮赌局；未承担初译的 Agent 已对原页复核通过。式 (36.16) 印本 `n` 与前文 `T` 的记号差异照原页保留并在 SOURCE_NOTES 登记。
- [x] 初译者已构建并自核 `chapter-36.draft.json`（93 块、4 项目录、式 (36.1)–(36.16)、图 36.1、9 道习题、双层表头的表 36.2／36.3）；SHA-256 `0250c2ebfe3ffedf88b4487e0dbc20f0498e9df149092da847834b58db19c2c8`，独立整章源审、草稿及正式网站审查通过，正式 JSON 同 SHA。
- [x] 原书式 (36.13) 双负号和式 (36.16) 的 `n`／`T` 差异照印本保留；独立 Agent 已对原页核实并在 `translation/chapter-36/SOURCE_NOTES.md` 记录。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页审查通过。
- [x] 逐节逐段核对 PDF463–468 正文、页边注、习题和跨页关系；原书无解答、脚注和程序代码，独立原页与稳定草稿结构审查通过。
- [x] 原页核实下列三节标题、起始页与译文。
  - [x] 36.1 Rational prospecting（PDF463 起）
  - [x] 36.2 Further reading（PDF465 起）
  - [x] 36.3 Further exercises（PDF466 起）
- [x] 图 36.1 的全部等高线、坐标刻度与图注及表 36.2／36.3 的双层表头和各自四格数值已由独立 Agent 对原页核对。
- [x] 图 36.1 与表 36.2／36.3 的编号、页码和资源已登记；本章无其他图表。
- [x] 对原页逐项核对式 (36.1)–(36.16)、变量、上下标；网站的可读、可复制与窄屏局部横滑已在草稿及正式路径验收。
- [x] 式 (36.1)–(36.16) 编号连续，无无编号展示式；132 处 MathML 可解析，印本两处疑点照原文保留并记录。
- [x] 核对术语、交叉引用、4 项目录、窄屏和深色模式排版；草稿与正式网站六视口审查通过。
- [x] 不同于初译者的 Agent 已完成六页原页与稳定草稿结构审查，S36-01 修复关闭，见 `translation/chapter-36/REVIEW.md`。
- [x] S36-01 修复并独立复核；正式 JSON 与审定草稿逐字节相同（71,738 字节，SHA-256 `0250c2ebfe3ffedf88b4487e0dbc20f0498e9df149092da847834b58db19c2c8`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-36/REVIEW.md`、`SITE_QA.md`。本章验收完成。

## 第 37 章：Bayesian Inference and Sampling Theory（PDF 469–478）

- [x] 初译 PDF469：章题、与原书正文区分的简短中文导读、贝叶斯与抽样理论两派定义、p 值与零假设后验的区分、习题 3.15／第 64 页交叉引用和原书强调；未承担初译的 Agent 已对原页复核通过。本页无图和编号公式。
- [x] 初译 PDF470：37.1 医学例子开头、两条无编号假设陈述、式 (37.1)–(37.3) 与 Yates 校正页边注；未承担初译的 Agent 已对原页和变量下标复核通过，本页无图。
- [x] 初译 PDF471：自由度与抽样分布、两派显著性程序、页边注、式 (37.4)–(37.10) 和本例 Yates 校正结论；未承担初译的 Agent 已对原页、数值与变量下标复核通过。本页无图。
- [x] 初译 PDF472：两派对 p 值的解释、贝叶斯分析开端、式 (37.11)–(37.16) 和图 37.1／37.2 交叉引用；未承担初译的 Agent 已对原页、数字及变量下标复核通过。本页无图。
- [x] 初译 PDF473：图 37.1–37.4 原页裁图、四段图注、后验结论、模型比较开端与无编号 2×2 数据表；未承担初译的 Agent 已对原页、图内曲线与刻度、表格各格复核通过。正文与图 37.4 图注的 `p_{A+}<10p_{B+}` 印本疑点照原文保留并在 SOURCE_NOTES 登记。
- [x] 初译 PDF474：模型比较式 (37.17)–(37.26)、60:40 结论方框符号、方括号旁论及 37.2 节开端的 12 次硬币结果串 `aaabaaaabaab`；未承担初译的 Agent 已对原页、公式数值及 9a/3b 计数复核通过。本页无图。
- [x] 初译 PDF475：单／双侧 p 值、停止规则对比、式 (37.27)–(37.29)、推荐习题 37.1 与鼠图标；未承担初译的 Agent 已对原页复核，S37-01 修复后关闭。末段跨 PDF476 合写；印本 `log p_b` 误差随 `sqrt(r)` 变化的疑点照原页保留并在 SOURCE_NOTES 登记。
- [x] 独立源审 S37-01：PDF475 末段 `boot ... out of the door` 已按印本改为“赶出门”，未承担初译的 Agent 独立复核关闭。
- [x] 初译 PDF476：完整承接上一页跨页段、37.2 节停止规则论证及清洁工对话、37.3 节置信区间定义与例子、式 (37.30)；未承担初译的 Agent 已对原页、三支分布与跨页接续复核通过。本页无图。
- [x] 初译 PDF477：式 (37.31) 的四种结果、式 (37.32) 印本两个 `min`、75% 置信区间反例、两项编号结论、习题 35.4 与 Kepler／Oprea 引文及 37.4 节标题；未承担初译的 Agent 已对原页、四组数据和端点逐项复核通过。37.4 首段跨 PDF478 合写，本页无图。
- [x] 初译 PDF478：37.4 节跨页首段、模型批评、延伸阅读全部引文、37.5 节两道习题及其 (a)／(b)／(c) 问；未承担初译的 Agent 已对原页、题目难度与三项程序输出复核通过。本页无图或编号式，习题 37.3 的两处 `10` 印本疑点照原页保留并在 SOURCE_NOTES 登记。
- [x] 初译者已构建并自核 `chapter-37.draft.json`（137 块、6 项目录、式 (37.1)–(37.32) 及 3 条无编号式、4 图、3 道习题、4×3 无编号表与两项列表）；SHA-256 `1f2c5883aeda504037401a97258153e5c6c4e2e7dc195eea69c43e3ebea965ca`，独立整章源审、草稿与正式网站审查通过，正式 JSON 同 SHA。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页审查通过。
- [x] 逐节逐段核对 PDF469–478 正文、列表、习题、引文及跨页接续；独立原页与稳定草稿结构审查通过。
- [x] 原页核实下列五节标题、起始页与译文。
  - [x] 37.1 A medical example（PDF470 起）
  - [x] 37.2 Dependence of p-values on irrelevant information（PDF474 起）
  - [x] 37.3 Confidence intervals（PDF476 起）
  - [x] 37.4 Some compromise positions（PDF477 起）
  - [x] 37.5 Further exercises（PDF478 起）
- [x] 图 37.1–37.4 的原图、图内符号、刻度和四段图注及 PDF473 无编号 4×3 表每格已由独立 Agent 对原页核对。
- [x] 四幅编号图与一张无编号数据表均已登记页码、译注并可解码；原页无其他图表。
- [x] 对原页逐项核对式 (37.1)–(37.32)、三条无编号展示式、变量和上下标；草稿与正式网站的 35 式可复制、窄屏局部横滑通过。
- [x] 编号式 (37.1)–(37.32) 连续；292 处 MathML 可解析，图 37.4、`√r`、双 `min` 和习题 37.3 两处 `10` 的印本疑点照原文保留并记录。
- [x] 独立网站审查 S37-SITE-01：390px 章题把“贝叶斯推断”拆在两行，三个 span 的窄屏不拆行样式修复后在草稿与正式六视口复测通过。
- [x] 核对术语、交叉引用、6 项目录、窄屏和深色模式排版；草稿与正式网站六视口审查通过。
- [x] 不同于初译者的 Agent 已完成十页原页与稳定草稿结构审查，S37-01 修复关闭，见 `translation/chapter-37/REVIEW.md`。
- [x] S37-01 与 S37-SITE-01 均修复并独立复核；正式 JSON 与审定草稿逐字节相同（130,992 字节，SHA-256 `1f2c5883aeda504037401a97258153e5c6c4e2e7dc195eea69c43e3ebea965ca`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-37/REVIEW.md`、`SITE_QA.md`。本章验收完成。

## Part V: Neural networks（PDF 479）

- [x] 初译者已对照 PDF479 原页核对第五部分的 `Part V / Neural networks` 双行标题与递归圆形／黑色扇形图案，裁得 847×930 原图并生成 2 块草稿；稳定 SHA-256 `3a856d5f3ecce83ef89f3745b6168381d9d6d1f5470792fea97885549b031dbf`，正式 JSON 同 SHA。
- [x] 未承担初译的 Agent 已对 PDF479 可视原页、847×930 图资产、2 块／1 目录的稳定草稿独立审查通过，见 `translation/part-V/REVIEW.md`。
- [x] 独立 Agent 在草稿及正式原始路径六视口复核图、目录、第 37↔V 部分导航、窄屏／深色模式和 PDF479 末块 100% 进度，各三次刷新稳定，见 `translation/part-V/SITE_QA.md`。
- [x] 正式注册 `chapter-V.json`，与审定草稿逐字节相同（547 字节，SHA-256 `3a856d5f3ecce83ef89f3745b6168381d9d6d1f5470792fea97885549b031dbf`）；`verify_registered.py`、全站 smoke、JS 语法与差异检查通过。本扉页验收完成；第 V→38 章导航待第 38 章审定接入后验证。

## 第 38 章：Introduction to Neural Networks（PDF 480–482）

- [x] 初译 PDF480：章题与独立导读、三项粗体研究动机、三项开篇项目和 38.1 节数字记忆引入；未承担初译的 Agent 已对原页及 5000 比特地址例子复核通过。本页无图表公式；页末跨 PDF481 的编号项随完整三项列表在下一页编排。
- [x] 初译 PDF481：基于地址的记忆三项缺点、生物记忆三项性质及第二项的两条嵌套子项、方括号补充说明；未承担初译的 Agent 已对原页和跨页列表复核通过。本页无图表公式，PDF480–481 首个跨页编号列表已合并，页末跨 PDF482 的段落随下页编排。
- [x] 初译 PDF482：跨页人工神经网络定义、38.2 节三项术语、目标函数推导、监督／无监督神经网络及样本集合 `\{\mathbf x\}` 记号；未承担初译的 Agent 已对原页、强调与跨页接续复核通过。本章至此结束，原书三页无图、表、编号展示式或习题。
- [x] 独立网站审查 S38-SITE-01：PDF480 工程学段末孤行“器。”经忠于原句的中文微调在草稿与正式六视口复测关闭。
- [x] 独立网站审查 S38-SITE-02：390px 章题拆开“神经网络导论”；保留原文字的两段 HTML 与窄屏整行样式经草稿、正式六视口复测关闭。
- [x] 独立网站审查 S38-SITE-03：390px PDF480 段末“质：”、320px PDF482 段末“应。”及 PDF481 列表四处短尾经原义中文微调与本章定向 `text-wrap: pretty` 修复，草稿与正式六视口复测关闭。
- [x] 初译者已构建并自核 `chapter-38.draft.json`（25 块、3 项目录、三份列表，含两条嵌套子项）；最终 SHA-256 `72f74147c52ec9220f07373610c25ee79578c07c4925c3e900eeaab142c66f03`，每次源文差异均经独立原页复核，正式 JSON 同 SHA。
- [x] 编写本章简短中文导读，与原书正文区分；独立原页审查通过。
- [x] 逐节逐段核对 PDF480–482 正文、三份列表、强调与两处跨页接续；原书无脚注、习题、答案或参考文献，独立原页与稳定草稿结构审查通过。
- [x] 原页核实两节标题、起始页与译文。
  - [x] 38.1 Memories（PDF480 起）
  - [x] 38.2 Terminology（PDF482 起）
- [x] 独立原页审查确认本章无图或表。
- [x] 本章无图表编号或图片资源。
- [x] 独立原页审查确认本章无展示公式、算法或代码；两处行内 MathML 在草稿及正式网站可解析、可复制，窄屏排版通过。
- [x] 本章无编号展示式。
- [x] 核对术语、交叉引用、3 项目录、窄屏和深色模式排版；草稿与正式网站六视口审查通过。
- [x] 不同于初译者的 Agent 已完成三页原页与稳定草稿结构审查，见 `translation/chapter-38/REVIEW.md`。
- [x] S38-SITE-01–03 全部修复并独立复核；正式 JSON 与审定草稿逐字节相同（16,560 字节，SHA-256 `72f74147c52ec9220f07373610c25ee79578c07c4925c3e900eeaab142c66f03`）。独立草稿与正式六视口网站 QA、`verify_registered.py`、全站 smoke、JS 语法与差异检查通过，见 `translation/chapter-38/REVIEW.md`、`SITE_QA.md`。本章验收完成。

## 第 39 章：The Single Neuron as a Classifier（PDF 483–493）

- [x] 初译 PDF483：章题与独立导读、39.1 节开头、图 39.1 与无编号逻辑函数曲线的原页裁图、式 (39.1)–(39.3)；未承担初译的 Agent 已对原页、图内标签、斜体小标题及活动规则复核通过。
- [x] 初译 PDF484：39.1 节的 tanh、阈值、热浴和 Metropolis 规则、两幅无编号曲线、式 (39.4)–(39.6)，以及 39.2 节开端式 (39.7)–(39.9) 与推荐习题 39.1；未承担初译的 Agent 已对原页、三行规则、图与交叉引用复核通过。
- [x] 初译 PDF485：图 39.2 三维曲面的原页裁图与轴／权重标签、式 (39.10)、输入与权重空间小标题、监督学习目标、梯度和反向传播段落；未承担初译的 Agent 已对原页与图资产复核通过。
- [x] 初译 PDF486：原页仅有图 39.3 及图注；十处权重曲面、`w_1/w_2` 坐标轴和各小图刻度已原页裁图并提供图内译注。未承担初译的 Agent 已对原页逐项复核通过；本页无正文或公式。
- [x] 初译 PDF487：39.3 节、式 (39.11)–(39.15)、推荐习题 39.2、误差函数／梯度及在线梯度下降算法前半；未承担初译的 Agent 已对原页复核通过，算法学习规则续 PDF488 待核。
- [x] 初译 PDF488：式 (39.16)–(39.21)、在线／批量学习说明和原书描边的批量学习框内全部文字与四步关系；未承担初译的 Agent 已对原页复核通过，稳定 JSON 仍须核含式 (39.18)–(39.20) 的单个描边框结构。
- [x] 初译 PDF489：整页图 39.4 原页裁图保留 (a)–(k) 十一个子图、全部坐标轴与线例；译注逐项对应学习率 `η=0.01`、六个迭代阶段、`a=0,±1` 等值线、输出与权重向量。未承担初译的 Agent 已对原页及十一面板独立复核通过。
- [x] 初译 PDF490：算法 39.5 完整 Octave 语句（仅注释译为中文）、长说明、图 39.6 的 3×4 十二子图与 `α` 列标签、曲线图例、坐标及长图注；未承担初译的 Agent 已对原页逐项复核通过，稳定 JSON 仍须核代码单描边框与可复制结构。
- [x] 初译 PDF491：39.4 节正则化全文、式 (39.22)–(39.23)、推荐习题 39.3、末尾斜体“说明”及动量法／共轭梯度的括注；未承担初译的 Agent 已对原页与符号复核通过。
- [x] 独立源审 S39-01：PDF492 表 39.7 缺数字 `14`／底线、LED 图混入相邻文字残片；初译者重裁后，未承担初译的 Agent 已对原页复核两资产完整、无残字并关闭。
- [x] 独立源审 S39-02：PDF492 习题 39.5 原书粗体题名已恢复，未承担初译的 Agent 对原页复核关闭。
- [x] 初译 PDF492：39.5 节、习题 39.4／39.5、式 (39.24)–(39.27)、七段 LED 图与表 39.7 的 `0–14` 全部图形；未承担初译的 Agent 已对原页逐项复核，S39-01/02 均关闭。跨页习题 39.6 随完整题目放 PDF493。
- [x] 初译 PDF493：跨页习题 39.6 完整码字、先验、BSC、无编号后验 sigmoid 式及神经元解码器绘图要求；未承担初译的 Agent 已对原页及跨页关系复核通过。第39章正文至此结束。
- [x] 本章简短中文导读标为“编者导读（非原书正文）”，已与原书正文区分并经独立源审。
- [x] PDF483–493 已逐节逐段翻译，并由未承担初译的 Agent 对照原页核对正文、列表、习题、跨页接续与页段对应；原书本章无脚注、答案或参考文献节，见 `translation/chapter-39/REVIEW.md`。
- [x] 以下小节标题、起始页、段落及无编号斜体小标题均经原页核对。
  - [x] 39.1 The single neuron（PDF483 起）
  - [x] 39.2 Basic neural network concepts（PDF484 起）
  - [x] 39.3 Training the single neuron as a binary classifier（PDF487 起）
  - [x] 39.4 Beyond descent on the error function: regularization（PDF491 起）
  - [x] 39.5 Further exercises（PDF492 起）
- [x] 原页逐项核对图 39.1–39.4、图 39.6、三幅无编号激活曲线、习题 39.5 七段 LED 图及表 39.7 的 0–14 共 15 行；图 39.5 是算法框编号，不存在同号图片。
- [x] 原页核对式 (39.1)–(39.27)、PDF493 一条无编号后验式、Metropolis 规则、算法 39.5 的 Octave 源码及 PDF488 批量学习描边框；网页展示和复制经独立六视口验收。
- [x] 术语、交叉引用和目录经独立源审；正式 JSON 与已审草稿逐字节相同（SHA-256 `011af8998e95282376c73d7a8cd898d84d4717561ced696f65a9733c9275ad3b`），草稿与正式六视口网站 QA 均通过，见 `translation/chapter-39/REVIEW.md`、`SITE_QA.md`。
- [x] 不同于初译者的 Agent 完成 PDF483–493 原页和稳定草稿结构审查；S39-01/02 已修复并复核，见 `translation/chapter-39/REVIEW.md`。
- [x] S39-01/02、S39-SITE-01/02 均修复复核；第 39 章 PDF483–493 独立原页、草稿与本地正式路径验收完成。

## 第 40 章预习题导页：Problems to look at before Chapter 40（PDF494）

- [x] 初译 PDF494：导页标题、习题 40.1–40.3、组合数括注和来源说明已对原页初核并生成独立稳定草稿；原书本页无图表或编号展示式。
- [x] 未承担初译的 Agent 对 PDF494 原页与稳定草稿结构独立审查通过：三道习题、组合数括注、页末来源说明、6 块／1 目录和 5 处行内 MathML 均核对，见 `translation/chapter-40-prelude/REVIEW.md`；无待修问题。
- [x] 未注册草稿已由独立 Agent 在 1440／390／320px 浅深六视口验收：三题、数学复制、目录、临时相邻导航、PDF494 末块 100% 进度和三次刷新均通过，见 `translation/chapter-40-prelude/SITE_QA.md`。
- [x] 独立 Agent 对草稿和已注册正式路径均完成六视口网站验收：三题、数学复制、目录、39↔导页导航、窄屏、深色模式及 PDF494 进度／三次刷新通过；早期滚动竞争经共享修复与无等待复测关闭，见 `translation/chapter-40-prelude/SITE_QA.md`。
- [x] 审定导页已注册正式 JSON（SHA-256 `1ce589fd6a42ff09e6077c36f6679732d11da35788c69a734bf7f2caf74bf6fc`），第 39→40 章前导页及返回导航经真实路径复核。
- [x] 第 40 章正文已审定注册，导页→第 40 章相邻导航及第 39→导页→正文顺序经真实路径六视口复核。

## 第 40 章：Capacity of a Single Neuron（PDF 495–503）

- [x] 初译 PDF495：章题与独立导读、40.1／40.2 节开端、图 40.1 原页裁图和图内 Learning algorithm 译注已由未承担初译的 Agent 对原页核对；跨 PDF496 的段落亦已续核，见 `translation/chapter-40/REVIEW_PARTIAL.md`。
- [x] 初译 PDF496：PDF495 跨页段落接续、容量与一般位置的定义 40.1、式 (40.1)–(40.2) 和偏置说明已按原页译出并通过独立逐页源审，见 `translation/chapter-40/REVIEW_PARTIAL.md`。
- [x] 初译 PDF497：40.3 节开端、图 40.2 双面板原页裁图及译注、`K=1`／`N=1`／`K=2` 计数和异或例子已独立对原页核对；跨 PDF498 接续亦已续核，见 `translation/chapter-40/REVIEW_PARTIAL.md`。
- [x] 初译 PDF498：PDF497 权重空间段落接续、图 40.3／40.4 原页裁图和区域标记译注、式 (40.3)、`T(3,2)=6`／`T(4,3)=14` 与三维推理已独立对原页核对；跨整页图版 PDF499 到 PDF500 的续句亦已核，见 `translation/chapter-40/REVIEW_PARTIAL.md`。
- [x] 初译 PDF499：原书整页图 40.5 双面板、图 40.7 三面板及图注已对原页核对；表 40.6 数值和空白格逐格正确。S40-01 双层 `K`／`N` 表头已在源稿恢复并独立复核；稳定 JSON 结构待核。
- [x] 初译 PDF500：接续 PDF498／499，式 (40.4)–(40.7)、递推关系推导及表 40.8 的 0–5 行／0–7 列已独立对原页核对。S40-01 同样涉及的双层 `K`／`N` 表头已在源稿恢复并独立复核；稳定 JSON 结构待核。
- [x] 初译 PDF501：图 40.9 四面板原页裁图与图内坐标译注、式 (40.8)–(40.9)、帕斯卡三角形构造及 VC 维讨论已独立对原页核对。S40-02 图注 (c) 的 `K=100` 已改为原书 `K=1000` 并复核；式 (40.9) 放大原页可见 `K≥N`／`K<N`，译稿本来正确，审查初报误读已纠正，见 `translation/chapter-40/REVIEW_PARTIAL.md`。
- [x] 初译 PDF502：式 (40.10) 与原书 `Φ` 定义、结论、40.4 节习题 40.4–40.8、图 40.10 和三处推荐习题小鼠图标已独立对原页核对；印本求和下标仅印 `0`、积分未印微分项，译稿照印本保留并记 `SOURCE_NOTES.md`，稳定 JSON 已独立核对。
- [x] 初译 PDF503：章末习题 40.9、40.5 节对习题 40.5 的解答与式 (40.11) 已独立对原页及稳定 JSON 核对通过。
- [x] PDF495 本章简短中文导读已标“编者导读（非原书正文）”，并经独立原页审查确认位置与内容分隔。
- [x] PDF495–503 全九页的正文、列表、习题 40.4–40.9、习题 40.5 解答与跨页接续已由未承担初译的 Agent 独立对原页核对；本章无脚注或参考文献节，见 `translation/chapter-40/REVIEW.md`。
- [x] 以下五节标题、起始页、段落与无编号小标题均经原页核对。
  - [x] 40.1 Neural network learning as communication（PDF495 起，标题与完整本节已独立对原页核对）
  - [x] 40.2 The capacity of a single neuron（PDF495 起）
  - [x] 40.3 Counting threshold functions（PDF497 起）
  - [x] 40.4 Further exercises（PDF502 起）
  - [x] 40.5 Solutions（PDF503 起）
- [x] 原页逐项核对图 40.1–40.5、40.7、40.9、40.10 共八张及图内英文、图注；表 40.6／40.8 双层 `K/N` 表头、数值与空格逐格核对，图号 40.6／40.8 对应表而非缺图。
- [x] 原页核对式 (40.1)–(40.11)、符号、上下标、习题标记及 257 处草稿 MathML；式 (40.9) 条件与式 (40.10) 印本疑点均有记录，网页展示与复制已通过独立六视口验收。
- [x] 术语、交叉引用和目录经独立源审；正式 JSON 与审定草稿逐字节相同（SHA-256 `b3c9ae628c76ec48aa3bd3688153cc577dfb8421455d4c55e3153d99e575d444`），草稿及正式六视口网站 QA 的窄屏、深色模式与阅读进度均通过。
- [x] 未承担初译的 Agent 完成 PDF495–503 九页原页与稳定草稿结构审查，S40-01/02 已修复复核，见 `translation/chapter-40/REVIEW.md`。
- [x] S40-SITE-01/02：表 40.6／40.8 跨列表头 `K` 与 320px 章题拆词经共享 scoped CSS 修复；独立 Agent 在草稿和正式六视口复核表头居中、局部横滑可达右端、标题两行完整。
- [x] S40-01/02 与 S40-SITE-01/02 均修复复核；第 40 章 PDF495–503 独立原页、草稿和本地正式路径验收完成，见 `translation/chapter-40/REVIEW.md`、`SITE_QA.md`。

## 第 41 章：Learning as Inference（PDF 504–515）

- [x] 初译 PDF504：章题与独立导读、41.1 节、式 (41.1)–(41.7) 和似然／先验解释已由未承担初译的 Agent 对原页核对；本页无图表习题，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF505：41.1 后验式 (41.8)–(41.10)、41.2 两权重示例及图 41.1 跨页引用与式 (41.11)、41.3 开端及式 (41.12) 已独立对原页核对；S41-01 最大后验估计句歧义已修复复核，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF506：原书整页图 41.1 的 `N=0/2/4/6` 四行四列似然／后验面板及图 41.2 三面板预测均已由独立 Agent 对原页裁图、图内文字与译注复核通过，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF507：41.3 节式 (41.13)–(41.18)、边缘化积分／后验平均、图 41.2 A/B 预测、过度自信讨论与 Copas（1983）均由独立 Agent 对原页核对通过，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF508：图 41.3 三面板原页裁图与图内文字译注、41.3 节“实现”、41.4 节开端、式 (41.19)、Langevin/Hamiltonian 方法及跨 PDF509 句子已独立对原页核对通过，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF509：原书整页算法 41.4 的 Octave 代码已由未承担初译的 Agent 放大原页逐行核对，运算符、中文行内注释、四行星号、完整图注及算法 41.8 引用均保留；稳定 JSON 单个描边框结构已核，网页复制待 QA。
- [x] 初译 PDF510：图 41.5 四联图原页裁图与刻度／图例译注、式 (41.20)、Langevin 演示及贝叶斯预测段落已独立对原页核对；图注 (d) 原书印 `M(x)`、正文印 `M(w)`，译稿分别照印本保留并待 `SOURCE_NOTES.md` 登记。
- [x] 初译 PDF511：原书整页图 41.6 六行五列三十幅样本小图与图 41.7 双面板高清裁图、两条完整图注及 `η/α/ε/a/y` 数值译注均经独立原页审查通过，见 `translation/chapter-41/REVIEW_PARTIAL.md`；本页无额外正文或公式。
- [x] 初译 PDF512：算法 41.8 Octave 代码及图注、图 41.9 Langevin/HMC 双曲线原页裁图与译注、“优化与典型性”／“减少随机游走”两小节及斜体结论已独立对原页核对；稳定 JSON 独立描边框结构和跨 PDF513 句子均核，网页复制待 QA。
- [x] 初译 PDF513：41.4 节跨页结尾、41.5 节开端、式 (41.21)–(41.27) 及习题 41.1 的小鼠推荐图标、难度 2 和三式已独立对原页核对；PDF512→513 句子在稳定 JSON 中语义完整，网站呈现待 QA。
- [x] 初译 PDF514：图 41.10／41.11 双面板原页裁图及图注、边缘化推断、习题 41.2、式 (41.28)–(41.30) 已独立对原页核对；末段跨 PDF515 的接续也已复核，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] 初译 PDF515：章末习题 41.3、“为什么要边缘化？”与三项决策情形已独立对原页核对；第 41 章止于本页，PDF516 为独立后记，见 `translation/chapter-41/REVIEW_PARTIAL.md`。
- [x] PDF504 本章简短中文导读明确标为非原书正文，独立源审确认位置与正文分隔。
- [x] PDF504–515 全十二页的正文、列表、习题 41.1–41.3、跨页接续和章末结束位置已由未承担初译的 Agent 独立对原页核对；本章无脚注、答案或参考文献节，见 `translation/chapter-41/REVIEW.md`。
- [x] 以下五节标题、起始页、段落及无编号斜体小标题均已对原页核对。
  - [x] 41.1 Neural network learning as inference（PDF504 起）
  - [x] 41.2 Illustration for a neuron with two weights（PDF505 起）
  - [x] 41.3 Beyond optimization: making predictions（PDF505 起）
  - [x] 41.4 Monte Carlo implementation of a single neuron（PDF508 起）
  - [x] 41.5 Implementing inference with Gaussian approximations（PDF513 起）
- [x] 原页逐项核对图 41.1–41.3、41.5–41.7、41.9–41.11 共九张和图内英文／图注；41.4 与 41.8 为算法编号而非缺图，本章原书无表格。
- [x] 原页核对式 (41.1)–(41.30)、符号、上下标及两个描边 Octave 算法；稳定草稿 252 处 MathML 可解析且无 `merror`，网页显示与复制已通过网站 QA。
- [x] 术语、交叉引用、六项目录、窄屏和深色模式已由独立 Agent 在草稿与正式路径六视口复核通过，见 `translation/chapter-41/SITE_QA.md`。
- [x] 未承担初译的 Agent 完成 PDF504–515 原页与冻结草稿结构审查，S41-01 与三组跨页句均修复复核，见 `translation/chapter-41/REVIEW.md`。
- [x] S41-SITE-01/02：五处节标题及四处短尾在 scoped CSS 下修复；独立 Agent 全六视口目视、复制、局部横滑和阅读进度复测通过，见 `translation/chapter-41/SITE_QA.md`。
- [x] 审定草稿与正式 JSON 逐字节一致（134,501 字节；SHA-256 `3984c49d135ee60024befaa6dcc2ff828d57b7f1bd388692e9f2521a4c70853f`）；独立原页与正式站点验收完成，本章通过。

## 监督式神经网络后记：Postscript on Supervised Neural Networks（PDF516）

- [x] 初译 PDF516：独立原页标题、两段 Robert 引语及间隔正文已由未承担初译的 Agent 对原页核对；与第 41 章正文分开，原页无图表、公式或习题，已生成 5 块冻结草稿 SHA-256 `31ec052c08626e22ef3cfb04cffbf618c38c630bc25f85f7ef699fba002c3999`，稳定结构在后续独立审查中通过。
- [x] 未承担初译的 Agent 对 PDF516 原页与 5 块稳定草稿独立审查通过：H1 顶线、两段叙述和两段引语层级正确，见 `translation/chapter-41-postscript/REVIEW.md`。
- [x] 独立 Agent 完成草稿和正式路径的网站六视口验收，核 40↔41↔后记↔42 的目录与相邻导航、窄屏、深色模式和阅读进度；后记→42 已在第 42 章正式注册后复核。
- [x] 审定后注册正式 JSON，与冻结草稿逐字节一致（1,823 字节；SHA-256 `31ec052c08626e22ef3cfb04cffbf618c38c630bc25f85f7ef699fba002c3999`）；前后顺序为 41→后记→42，见 `translation/chapter-41-postscript/SITE_QA.md`。

## 第 42 章：Hopfield Networks（PDF 517–533）

- [x] 初译 PDF517：第 42 章章题与独立导读、图 42.1 前馈／反馈双图及译注、42.1 节开端和式 (42.1) 已由独立 Agent 对原页核对；跨 PDF518 刺激例起句亦确认，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF518：赫布联想与模式补全续段、42.2 节权重方向／结构／活动规则／同步及异步更新／学习规则、式 (42.2)–(42.4) 和原书强调均已独立对原页核对，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF519：图 42.2 九条城市—国家记忆及四个补全／纠错例、式 (42.5)–(42.8)、推荐习题 42.1／42.2、42.3 节全节与 42.4 节开端已独立对原页核对；尾句跨 PDF520 接续亦已复核。
- [x] 初译 PDF520：42.4 节变分／平均场对应的式 (42.9)–(42.15)、Lyapunov 函数与异步／对称收敛条件、推荐习题 42.3／42.4 及解答页码均已独立对原页核对，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF521：原书整页图 42.3 四张高分辨率原页裁图经独立审查，25×25 权重矩阵首尾行列、(a)–(m) 十三组状态图／箭头、顺序与完整译注均对原页核对通过，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF522：42.5 节四记忆异步恢复、两斜体小标题、习题 42.5、五／六模式失效论述，42.6 节开端及式 (42.16)–(42.17) 已独立对原页核对；式后解释续于 PDF524，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF523：原书整页图 42.4／42.5 的高清裁图经独立审查；25×25 权重矩阵、删边标记、(a)–(f) 状态箭头、六条演化路径、图内文字译注与完整图注均对原页核对通过，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF524：§42.6 收尾、习题 42.6、§42.7 开端与四类失效说明及图 42.6 九词对／错字／伪态高清裁图已独立对原页核对。原书最速下降式的正号与“同号”说法经 300 dpi 放大确认照印本保留，疑点见 `translation/chapter-42/SOURCE_NOTES.md` 与 `REVIEW_PARTIAL.md`。
- [x] 初译 PDF525：§42.7 两种容量定义、式 (42.18)–(42.22) 的下标／求和／负号，以及图 42.7 左尾阴影和 $a_i$、$I$、$\sqrt{IN}$ 标注已独立对原页核对；式 (42.22) 后的 $\Phi$ 定义接 PDF526，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF526：PDF525→526 的 $\Phi$ 定义、式 (42.23)–(42.26)、习题 42.7、0.18$I$／1% 与 0.138$I$ 容量论述、图 42.8 双曲线及坐标／虚线／端点均已独立对原页核对，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF527：§42.7 自旋玻璃、0.138 临界点、六条加粗区间结论、式 (42.27) 及页边注，§42.8 开端与单神经元目标规则已独立对原页核对；S42-01 对 likely 的概率判断已修复并复核，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF528：原书算法 42.9 Octave 代码及注释逐行、式 (42.28)–(42.30)、习题 42.8 与 §42.9 开端已独立对原页核对；式 (42.28) 整体括号缺失经高清原页确认照印本保留并登记，单个描边框待稳定草稿 QA。
- [x] 初译 PDF529：原书图 42.10 的 (a1/a2/b/c) 4×4 节点、两路线、负连接与箭头，以及 §42.9 旅行商定义、$I=K^2$、置换矩阵和两种权重作用已独立对原页核对；跨 PDF530 句只译一次，后页已核无重复。
- [x] 初译 PDF530：原书图 42.11 八帧状态演化、剑桥路线地图、完整图注及 §42.9 收束已独立对原页核对。S42-02 已补 `The Backs` 译注，下缘只标原图可辨残字 `Sheeps`；原嵌图仅 435×535px，其余小字不猜写，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF531：§42.10 习题 42.9／42.10 全文与标记层级、式 (42.31)–(42.35) 的分段条件、严格不等号、$x'$／$w'$ 及 $2I$ 上界均已独立对原页核对，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF532：两斜体小标题、习题 42.11／42.12 的全部条件、图 42.12 三状态、图 42.13 五面板／十空格、东南移动三规则及 §42.11 首则解答均已独立对原页核对；末页解答亦经 PDF533 复核，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] 初译 PDF533：§42.11 习题 42.4／42.12 解答、Kraft 等式、守恒权重、$\sum_{l=4}^{\infty}(l+1)2^{-l}=3/4$ 及图 42.14 均已独立对原页核对；S42-03 已改为普通中文并列印本等宽 `southeast`，复核关闭。
- [x] PDF517 本章简短中文导读已明确标为非原书正文，并由独立 Agent 核对位置与分隔，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
- [x] PDF517–533 全十七页正文、列表、习题与答案均已由未承担初译的 Agent 对原页逐页核对；跨页句和 S42-01/02/03 均修复复核，整章草稿结构待核。
- [x] 以下十一节标题、起始页、正文段落与无编号斜体小标题均已由独立 Agent 对原页核对，见 `translation/chapter-42/REVIEW_PARTIAL.md`。
  - [x] 42.1 Hebbian learning（PDF517–518；标题、正文与跨页接续已独立核对）
  - [x] 42.2 Definition of the binary Hopfield network（PDF518–519；标题、定义、式与图引用已独立核对）
  - [x] 42.3 Definition of the continuous Hopfield network（PDF519；标题、定义和式已独立核对）
  - [x] 42.4 Convergence of the Hopfield network（PDF519–520；标题、证明与习题已独立核对）
  - [x] 42.5 The associative memory in action（PDF522–523；标题、斜体小标题、示例、习题与图引用已独立核对）
  - [x] 42.6 The continuous-time continuous Hopfield network（PDF522／524；标题、式 (42.16)–(42.17)、连续时间收尾和习题 42.6 已独立核对）
  - [x] 42.7 The capacity of the Hopfield network（PDF524–527；两种容量、图 42.7／42.8、式 (42.18)–(42.27) 和习题 42.7 已独立原页核对）
  - [x] 42.8 Improving on the capacity of the Hebb rule（PDF527–528；标题、单神经元目标、算法 42.9、式 (42.28)–(42.30) 与习题 42.8 已独立原页核对；代码框待稳定草稿 QA）
  - [x] 42.9 Hopfield networks for optimization problems（PDF528–530；旅行商定义、图 42.10／42.11、权重作用与跨页句已独立核对，地图原始分辨率限制已登记）
  - [x] 42.10 Further exercises（PDF531–532；习题 42.9–42.12、式 (42.31)–(42.35)、两斜体小标题及图 42.12／42.13 已独立原页核对）
  - [x] 42.11 Solutions（PDF532–533；习题 42.3／42.4／42.12 解答及图 42.14 已独立原页核对）
- [x] 原书 13 幅独立编号图的画面、图内可辨英文、图注与页码已独立对原页核对；分裁为 18 资产，图 42.11(b) 原嵌低分辨率地图的不可辨范围见 `translation/chapter-42/REVIEW.md`；本章无独立表格。
- [x] 图编号实核为 42.1–42.8、42.10–42.14；42.9 为描边算法而非缺图，18 个资产均通过独立解码和原页裁边核对。
- [x] 式 (42.1)–(42.35)、符号、上下标、算法 42.9 代码已独立对原页核对；稳定草稿 252 处 MathML 可解析，正式网页 35 条展示式和完整代码可复制，手机局部横滑通过。
- [x] 编号式实核为连续 (42.1)–(42.35)，无额外无编号展示式；算法 42.9 为单个描边代码框，稳定草稿结构已独立核对。
- [x] 冻结草稿 `chapter-42.draft.json`（157,702 字节；SHA-256 `930a42864cefbd0a7da16a0fc188a1619e177e5bf8466dce3742703e454efe82`；207 块、12 目录、18 图资产、35 编号式、12 题、算法 42.9 单描边框）已通过独立结构与网站 QA，并逐字节注册为正式 JSON。
- [x] S42-SITE-01/02：320px 三处节标题断行、手机十一处短尾及桌面另三处短尾以精确块 ID 的 CSS 修复；独立 Agent 草稿与正式路径六视口复测短尾为零，见 `translation/chapter-42/SITE_QA.md`。
- [x] 术语、交叉引用、12 项目录、窄屏和深色模式排版已在草稿和正式路径由独立 Agent 复核通过。
- [x] 未承担初译的 Agent 完成 PDF517–533 原页及冻结草稿结构审查，S42-01/02/03 均修复复核；见 `translation/chapter-42/REVIEW.md`。
- [x] S42-01/02/03 和 S42-SITE-01/02 均修复复核；正式 JSON 与审定草稿逐字节相同（157,702 字节；SHA-256 `930a42864cefbd0a7da16a0fc188a1619e177e5bf8466dce3742703e454efe82`），第 42 章独立原页及正式网站验收完成。

## 第 43 章：Boltzmann Machines（PDF 534–538）

- [x] 初译 PDF534：章题、独立导读、§43.1、式 (43.1)–(43.5) 与原书描边活动规则 (43.3) 已独立对原页核对；单个描边框待稳定草稿 QA。
- [x] 初译 PDF535：式 (43.6)–(43.12)、推荐习题 43.1、经验／模型相关量与“清醒／睡眠”解释开端已独立对原页核对；印本 gradient descent 疑点照录并登记，见 `translation/chapter-43/REVIEW_PARTIAL.md`。
- [x] 初译 PDF536：清醒／睡眠解释、二阶统计局限、椅子／平移样本例、图 43.1 双联与式 (43.13) 已独立对原页核对；高阶求和下标 `ij` 照印本保留，S43-01 图注三格顺序误断言已修复复核。
- [x] 初译 PDF537：习题 43.2、隐变量动机、§43.2 带隐单元学习、式 (43.14)–(43.18)、可见／隐状态和两个配分函数均已独立对原页核对；S43-02 已补回原书 *not* 的斜体强调并复核。
- [x] 初译 PDF538：式 (43.18) 两项期望解释、带标签平移样本、蒙特卡罗成本、原书五组文献、§43.3／习题 43.3 和图 43.2 四个 5×5 样本已独立对原页核对；五页正文源审通过，稳定草稿待核。
- [x] PDF534 本章简短中文导读已明确标为非原书正文，独立 Agent 已核对位置与分隔，见 `translation/chapter-43/REVIEW_PARTIAL.md`。
- [x] PDF534–538 五页正文、习题、图、式和跨页接续已由未承担初译的 Agent 逐页对原页核对；S43-01/02 已修复复核，稳定草稿结构待核。
- [x] 以下三节标题、原页位置、正文段落及章末习题均已独立核对，见 `translation/chapter-43/REVIEW_PARTIAL.md`。
  - [x] 43.1 From Hopfield networks to Boltzmann machines（PDF534–537；活动规则、学习式及清醒／睡眠解释已独立核对）
  - [x] 43.2 Boltzmann machine with hidden units（PDF537–538；隐单元模型、两个配分函数与梯度已独立核对）
  - [x] 43.3 Exercise（PDF538；习题 43.3 与上下文已独立核对）
- [x] 图 43.1／43.2 的画面、图内文字、完整图注、裁边和页码均经独立原页核对；本章原书无独立表格。
- [x] 图编号实核为 43.1／43.2，两张 PNG 均独立解码、核尺寸和图内所有可见内容。
- [x] 式 (43.1)–(43.18)、符号、上下标、描边活动规则及其框内顺序已独立对原页核对；正式网页 18 式可复制、手机局部横滑通过。
- [x] 编号式实核为连续 (43.1)–(43.18)，(43.3) 在原书单个描边活动规则框内；稳定草稿 18 式 MathML 均可解析。
- [x] 冻结草稿 `chapter-43.draft.json` 两处 H2 等文字标记后为 60,827 字节、SHA-256 `5ca6cd684590b08b0d3e497a4398d76ea31b4b0adb32493f4f80f028112ae81f`（67 块、4 目录、18 编号式、2 图、3 题、1 描边活动规则框）；独立 Agent 删除新增 `heading.html` 字段后精确还原旧审定 SHA，正式 JSON 与新草稿逐字节相同，源审和网站 QA 均通过。
- [x] S43-SITE-01/02：两处节标题的技术词拆行用等文字 nowrap span 修复，三处正文／图注短尾用精确块 CSS 修复；独立 Agent 草稿与正式路径六视口复测通过，见 `translation/chapter-43/SITE_QA.md`。
- [x] 术语、交叉引用、4 项目录、窄屏和深色模式排版已在草稿与正式路径由独立 Agent 复核通过。
- [x] 未承担初译的 Agent 完成 PDF534–538 原页与冻结草稿结构审查，S43-01/02 修复复核；见 `translation/chapter-43/REVIEW.md`。
- [x] S43-01/02 和 S43-SITE-01/02 均修复复核；第 43 章独立原页和正式网站验收完成，正式 JSON SHA-256 `5ca6cd684590b08b0d3e497a4398d76ea31b4b0adb32493f4f80f028112ae81f`。

## 第 44 章：Supervised Learning in Multilayer Networks（PDF 539–545）

- [x] 初译 PDF539：章题、独立导读、§44.1、图 44.1 的 6／7／3 节点和英文译注、图 44.2 的 11 个参数值、式 (44.1)／(44.2) 及跨 PDF540 句已独立对原页核对；两图裁边完整，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] 初译 PDF540：PDF539→540 跨页句、图 44.3 的三个尺度和 400／4／8／0.5 参数、图 44.4 曲面及参数、§44.2 式 (44.3) 与反向传播段均已独立对原页核对；两图边界完整，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] 初译 PDF541：§44.2 正则化与历史应用、§44.3 概率解释、式 (44.4)–(44.8) 的 $Z_D/Z_W/Z_M$、方差 $1/\beta$／$1/\alpha$、贝叶斯正负号与 $w_{\mathrm{MP}}$ 均已独立对原页核对，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] 初译 PDF542：§44.3 二分类／多分类网络、式 (44.9)–(44.11)、§44.4 起段与斜体强调已独立对原页核对；式 (44.9) 印本 $\sum_n$ 只在第一项前，译稿照录并登记，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] 初译 PDF543：图 44.5 五联图和图 44.6 误差棒图、§44.4 四点优势、边缘化与贝叶斯实现段落已独立对原页核对；S44-01 两图注额外加粗及标签方向误称已修复复核，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] 初译 PDF544：§44.4 末段、§44.5 习题 44.1 前半及分类器 A／B／C 三张 2×2 频数表已独立逐格核原页：`[[90,0],[10,0]]`、`[[80,10],[0,10]]`、`[[78,12],[0,10]]`；真值／输出轴、排序与首条跨页问题均齐，第二条已于 PDF545 复核。
- [x] 初译 PDF545：习题 44.1 第二条、D／E 两张拒判表 `[[74,10,6],[0,1,9]]`／`[[78,6,6],[0,5,5]]`、图 44.7、末尾三问已独立对原页核对；式 (44.12) 印本确为 $P(t)/P(t\mid y)$，疑点照录，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] PDF539 本章简短中文导读已明确标为非原书正文，独立 Agent 已核对位置与分隔，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
- [x] PDF539–545 七页正文、图表、习题、跨页接续与原书疑点已由未承担初译的 Agent 逐页对原页核对；S44-01 已修复复核，整章草稿结构待核。
- [x] 以下五节标题、起始页、逐节段落和无编号小标题均已由独立 Agent 对原页核对，见 `translation/chapter-44/REVIEW_PARTIAL.md`。
  - [x] 44.1 Multilayer perceptrons（PDF539–540；标题、图 44.1–44.4、式 (44.1)–(44.2) 与正文已独立原页核对）
  - [x] 44.2 How a regression network is traditionally trained（PDF540–541；标题、反向传播、正则化与历史应用已独立原页核对）
  - [x] 44.3 Neural network learning as inference（PDF541–542；标题、概率解释、二／多分类网络及式 (44.4)–(44.11) 已独立原页核对）
  - [x] 44.4 Benefits of the Bayesian approach to supervised feedforward neural networks（PDF542–544；图 44.5／44.6、复杂度、贝叶斯四项优势及末段已独立原页核对）
  - [x] 44.5 Exercises（PDF544–545；习题 44.1 五张频数表、第二条问题与图 44.7 已独立逐项核对）
- [x] 图 44.1–44.7 的画面、图内英文、图注与裁边，以及习题 44.1 的五张频数表每个单元格均已独立原页核对；正式网页六视口图与表排版通过。
- [x] 图编号实核为连续 44.1–44.7；五张 A–E 频数表无独立表号，已在习题顺序内保留。
- [x] 式 (44.1)–(44.12)、符号、上下标与交叉引用已独立对原页核对；正式网页 12 式全可复制，手机局部横滑通过。
- [x] 编号式实核为连续 (44.1)–(44.12)，式 (44.9) 和 (44.12) 的印本疑点照原页登记于 `translation/chapter-44/SOURCE_NOTES.md`。
- [x] 冻结草稿 `chapter-44.draft.json` 三处 H2 等文字术语 span 后为 87,942 字节、SHA-256 `6fe26652663d3a5e5c369d66ca7d17ecdf92d2b85b577942e5cd7c25329ee237`（89 块、6 目录、7 图、12 编号式、五张频数表、习题 44.1）；独立 Agent 删除新增三个 `heading.html` 后精确还原旧审定 SHA，正式 JSON 与新草稿逐字节相同，源审和网站 QA 均通过。
- [x] S44-SITE-01/02：三处节标题拆技术词和十一处正文／列表短尾用等文字术语 span 与精确块 CSS 修复；独立 Agent 草稿与正式路径六视口复测短尾为零，见 `translation/chapter-44/SITE_QA.md`。
- [x] 术语、交叉引用、6 项目录、窄屏和深色模式排版已在草稿与正式路径由独立 Agent 复核通过。
- [x] 未承担初译的 Agent 完成 PDF539–545 原页与冻结草稿结构审查，S44-01 修复复核、五张表逐格通过；见 `translation/chapter-44/REVIEW.md`。
- [x] S44-01 与 S44-SITE-01/02 已修复复核；第 44 章独立原页和正式网站验收完成，正式 JSON SHA-256 `6fe26652663d3a5e5c369d66ca7d17ecdf92d2b85b577942e5cd7c25329ee237`。

## 第 45 章导页（PDF 546）

- [x] PDF546 “About Chapter 45” 全文、章前导引、习题 45.1 和两条原书网址已独立对原页核对；冻结草稿与正式 JSON 逐字节一致（4,252 字节；7 块／1 目录；SHA-256 `b24825171362126007c16454504d00144b1673fb027b01e556403c8816505407`），源审见 `translation/chapter-45-prelude/REVIEW.md`。
- [x] 本导页原页无图、表或编号式；习题 45.1、交叉引用、两条 URL、标题字形、44↔导页导航、窄屏及末块 100% 已由独立 Agent 在草稿与正式路径六视口复核；桌面短尾修复见 `translation/chapter-45-prelude/SITE_QA.md`。

## 第 45 章：Gaussian Processes（PDF 547–560）

- [x] 初译 PDF547：章题、独立导读、函数先验和式 (45.1)、参数模型／高斯过程解释及跨 PDF548 的 Kalman／kriging 完整句已独立对原页核对；后页无重复，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF548：§45.1 问题设定／参数化方法、例 45.2、式 (45.2)／(45.3)、多项式基函数与斜体层级已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF549：例 45.3、式 (45.4)–(45.8) 的求和／权重／偏置／Bayes 条件／Hessian 与 MCMC／边缘化段落已独立对原页核对；式 (45.7) 印本测度确为 $d^H w$，照录并登记疑点，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF550：§45.1 非参数／样条平滑、式 (45.9)–(45.12)、贝叶斯 MAP、斜体小标题及高斯过程形式已独立对原页核对；三次样条结点二阶导数和补 $(p-1)$ 项的印本措辞确实如此，照录留证，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF551：式 (45.13)–(45.16)、样条傅里叶基和高斯先验、预测／证据不依赖参数表示已独立对原页核对；印本 $A$ 定义确无 $\alpha$、式 (45.15) 指数确为 $h^{p/2}$，照录留证，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF552：§45.2 线性模型、高斯过程定义、式 (45.17)–(45.25) 九式、$R/Q/C$ 矩阵维度与 $H<N$ 退化均已独立对原页核对；印本 (45.20)／(45.21) 确分别编号，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF553：式 (45.26)–(45.33)、例 45.4 均匀径向基函数推得协方差核、噪声项、目标值高斯先验及图 45.1 跨后页引用均已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF554：图 45.1 四面板曲线、轴刻度、下方四条协方差公式及图内译注、§45.3 式 (45.34) 已独立对原页核对；跨 PDF555 的 $C_{N+1}$ 定义完整且只译一次，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF555：§45.3 续段、分块矩阵与预测分布式 (45.35)–(45.43)、§45.4 起段已独立对原页核对；S45-01 式 (45.39) 的恒等号已改回印本普通等号并复核。
- [x] 初译 PDF556：式 (45.44)–(45.48)、两支噪声模型、平稳／均匀术语、功率谱、例 45.5 与 $\theta_1/\theta_2/r_i$ 解释均已独立对原页核对；绝对值幂 $|x-x'|^\nu$ 与印本一致，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF557：图 45.2 三面板的五菱形数据、两组误差曲线、等高线叉号与 $r_1/\theta_3$ 刻度、式 (45.49)／(45.50)、$\nu$ 范围及跨 PDF558 句均已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF558：式 (45.51)–(45.55) 的超参数积分／近似／证据梯度、矩阵次序与正负号、两种方法、$N^3$／$O(N^2)$ 复杂度和评注均已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF559：§45.6／45.7、式 (45.56)、分类器的 Laplace／Monte Carlo／变分三种处理、斜体小标题及跨页接续已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] 初译 PDF560：§45.7 章末讨论、斜体“延伸阅读”、作者年份与 Chu 四条引用，以及 PDF559→560 接续和 PDF561 新章边界已独立对原页核对，见 `translation/chapter-45/REVIEW_PARTIAL.md`。
- [x] PDF547–560 的 14 份页稿已构建为审定草稿并注册正式 `chapter-45.json`；四个手机小节标题增加等文字术语 span，PDF551 一句作忠于原意的短尾精简后，草稿与正式版逐字节相同（202,932 字节；SHA-256 `e522500c9c7642ff561f3d4fdffaec5062804bf6dfe31e2e121d0b63e0451547`）。两次差异均经独立 Agent 反证并对可视原页复核。
- [x] PDF547 本章简短中文导读已明确标为非原书正文，独立 Agent 已核对位置与分隔。
- [x] PDF547–560 逐节逐段原页核对正文、列表、跨页接续和文献；原书本章无脚注、习题、答案或代码，习题 45.1 位于 PDF546 独立导页；见 `translation/chapter-45/REVIEW.md`。
- [x] 核实以下七节标题、起始页、段落和无编号斜体小标题；逐页源审通过。
  - [x] 45.1 Standard methods for nonlinear regression（PDF548–551；标题、参数／非参数方法、例 45.2／45.3 与式 (45.2)–(45.16) 已独立原页核对）
  - [x] 45.2 From parametric models to Gaussian processes（PDF552–554；标题、定义、协方差核与图 45.1 已独立原页核对）
  - [x] 45.3 Using a given Gaussian process model in regression（PDF554–555；标题、预测分布、分块矩阵及式 (45.34)–(45.43) 已独立原页核对）
  - [x] 45.4 Examples of covariance functions（PDF555–557；标题、噪声模型、例 45.5、图 45.2 与式 (45.44)–(45.50) 已独立原页核对）
  - [x] 45.5 Adaptation of Gaussian process models（PDF557–558；标题、超参数积分／近似及式 (45.51)–(45.55) 已独立原页核对）
  - [x] 45.6 Classification（PDF559；标题、式 (45.56) 与三种近似方法已独立原页核对）
  - [x] 45.7 Discussion（PDF559–560；标题、全部讨论段落、延伸阅读及跨页接续已独立原页核对）
- [x] 图 45.1／45.2 的面板、曲线、轴刻度、图内公式、图注与紧邻中文译注均已独立原页核对；本章无表格。
- [x] 两张原书图的编号与资产均已核实，PDF554 图 45.1、PDF557 图 45.2，无缺图或未编号图，见 `translation/chapter-45/REVIEW.md`。
- [x] 逐式核对 (45.1)–(45.56) 的变量、上下标、矩阵方向与列表间编号；冻结 JSON 均含 MathML，网站可读和复制已通过独立验收。
- [x] 原页核对 (45.1)–(45.56) 连续、无重号；本章无其他独立展示式、代码或算法，见 `translation/chapter-45/REVIEW.md`。
- [x] 独立 Agent 在草稿和正式路径六视口核对术语、交叉引用、8 项目录、56 式、两图、窄屏局部横滑、深色模式和末页 100% 阅读进度；见 `translation/chapter-45/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成 PDF547–560 逐页原页与冻结 JSON 结构审查；S45-01 修复复核、印本疑点留证，见 `translation/chapter-45/REVIEW.md`。
- [x] S45-01 符号、四处手机标题拆词及 27 处短尾均修复并经原页与六视口复核；正式路径、三次刷新、本地 `verify_registered.py` 和全站 smoke test 均通过，完成本章验收。

## 第 46 章：Deconvolution（PDF 561–566）

- [x] 初译 PDF561：章题、独立导读、§46.1 的两处斜体小标题、点扩散函数与内禀相关函数及式 (46.1)–(46.3) 已独立对原页核对，见 `translation/chapter-46/REVIEW_PARTIAL.md`。
- [x] 初译 PDF562：贝叶斯与最小平方误差两种推导、式 (46.4)–(46.11)、证据、最可能图像、误差棒与隐含求和已独立对原页核对；式 (46.4) 印本多一个右括号已目视确认并留证。
- [x] 初译 PDF563：式 (46.12)–(46.15)、线性滤波关系、最大熵与内禀相关函数模型及概率影像序列小节已独立对原页核对；跨 PDF564 的 $z$ 与 $c^2+s^2=1$ 解释仅译一次，见 `translation/chapter-46/REVIEW_PARTIAL.md`。
- [x] 初译 PDF564：式 (46.16) 与 Cholesky、§46.2 两条编号理由、§46.3 人眼去卷积起段、1/5 角分与 25 倍面积，以及跨 PDF565 的方括号说明均已独立对原页核对，见 `translation/chapter-46/REVIEW_PARTIAL.md`。
- [x] 初译 PDF565：卡纸狭缝实验的条件、数字、步骤与观察结果、早期视觉去卷积论证、McCollough effect、脚注 1 原 URL 及跨 PDF566 句已独立对原页核对，见 `translation/chapter-46/REVIEW_PARTIAL.md`。
- [x] 初译 PDF566：§46.3 末两段猜想、1/5–10 角分、§46.4 题名、习题 46.1 的 $3^C$ 难度及 PDF567 独立扉页边界均已独立对原页核对；节题前原书实心三角在草稿 heading.html 中保留为可见 `▶`。
- [x] PDF561–566 六份页稿的审定草稿与正式 `chapter-46.json` 逐字节相同（65,198 字节；SHA-256 `0d7a3e2b03125b63319fa8c1738f9d3ee798f2b7041a42b907bd546c4a4625af`；67 块／5 目录／16 编号式／1 题／1 脚注／末块 `p566-b004`）。手机 §46.2 标题等文字 span 的唯一新增字段经独立反证，源审与六视口网站验收通过。
- [x] PDF561 本章简短中文导读已明确标为非原书正文，位置与分隔经独立 Agent 核对。
- [x] PDF561–566 逐节逐段原页核对正文、编号列表、脚注、习题与跨页接续；本章无答案或单列参考文献，见 `translation/chapter-46/REVIEW.md`。
- [x] 核实以下四节标题、起始页、段落和无编号斜体小标题；逐页源审通过。
  - [x] 46.1 Traditional image reconstruction methods（PDF561–564；标题、两种线性滤波推导与式 (46.1)–(46.15) 已独立原页核对）
  - [x] 46.2 Supervised neural networks for image deconvolution（PDF564；标题、两项编号理由已独立原页核对）
  - [x] 46.3 Deconvolution in humans（PDF564–566；标题、视觉实验、脚注和跨页接续已独立原页核对）
  - [x] 46.4 Exercises（PDF566；实心三角标题和习题 46.1 已独立原页及草稿结构核对）
- [x] 六页可视原页及冻结 JSON 核实本章无图、表或代码；不存在待译图内文字或表格单元格。
- [x] 原页核实无编号图表或未编号图表，见 `translation/chapter-46/REVIEW.md`。
- [x] 逐式核对 (46.1)–(46.16) 的变量、上下标与符号；正式网站 16 条 MathML 均可读可复制，经独立验收。
- [x] 原页核对 (46.1)–(46.16) 连续、无重号；式 (46.4) 多余右括号为印本疑点，忠实照录并留证。
- [x] 独立 Agent 在草稿与正式路径六视口核对术语、交叉引用、5 项目录、16 式、脚注 URL、窄屏局部横滑、深色模式和末页 100% 阅读进度，见 `translation/chapter-46/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成 PDF561–566 逐页原页与冻结 JSON 结构审查，见 `translation/chapter-46/REVIEW.md`。
- [x] §46.4 实心三角、§46.2 手机标题拆词及七处短尾均修复复核；正式路径、三次刷新、本地 `verify_registered.py` 与全站 smoke test 通过，完成本章验收。

## Part VI: Sparse Graph Codes（PDF 567）

- [x] PDF567 双行扉页题名与 1260×1270 原页递归圆环图已独立原页审查并接入正式 `chapter-VI.json`；审定草稿与正式版逐字节相同（595 字节；SHA-256 `f2cfa40497281989a41349a1d5dd988351f6e9a4dba968d9880c18d44d94e4ba`；2 块／1 目录），见 `translation/part-VI/REVIEW.md`。
- [x] 第六部分扉页已按原书位于第 46 章与 PDF568 导页之间；独立 Agent 在草稿及正式路径六视口复核图像、目录、46↔VI 导航、PDF567 末块与 100% 进度，见 `translation/part-VI/SITE_QA.md`。

## Part VI 导页（PDF 568）

- [x] PDF568 “About Part VI” 四段、香农极限、$R=K/N$、$M=N-K$、四类稀疏图码与和积译码已独立对原页核对；审定草稿与正式 `chapter-VI-intro.json` 逐字节相同（3,869 字节；SHA-256 `8855f5e49eb555da1ce5ee716a8e48aece87418badb4ad69040dc207480ea584`；5 块／1 目录／末块 `p568-b005`）。独立源文／结构和六视口网站审查均通过。
- [x] 对照原 PDF 独立核对“About Part VI” 全文、章节路线、五处斜体、五处行内数学和交叉引用；与扉页及第 47 章分开，见 `translation/part-VI/about-part-VI/REVIEW.md`。
- [x] 原页无图、表、代码、习题、展示式；五处行内数学、标题横线和居中斜体、三处短尾经不同 Agent 草稿与正式路径六视口审查并复核，见 `translation/part-VI/about-part-VI/REVIEW.md`、`SITE_QA.md`；本地注册路径及 smoke test 通过。

## 第 47 章：Low-Density Parity-Check Codes（PDF 569–585）

- [x] 初译 PDF569：章题与独立导读、§47.1／47.2、图 47.1 矩阵与二部图、式 (47.1)、斜体强调及数字／交叉引用已独立对原页核对；两个节题前实心三角待冻结 JSON 结构复核，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF570：图 47.2 三幅因子图、全部图内英文与式的紧邻译注、式 (47.2)–(47.4)、码字／伴随式双视角及跨 PDF571 的高斯信道句已独立对原页核对；S47-01 次序和 S47-05 后置 caption 均修复复核。
- [x] 初译 PDF571：式 (47.5)／(47.6)、无编号 $\mathbf H\mathbf x=\mathbf z\pmod2$、§47.3 起段及 PDF570→571→572 两处断句均已独立对原页核对；原书噪声段突然写“比特 $x_n$”照录留证，§47.3 三角待冻结 JSON 核查。
- [x] 初译 PDF572：$\mathcal N(m)$／$\mathcal M(n)$、$q/r$ 消息、加粗“初始化／水平步骤”、式 (47.7)／(47.8) 的求和集合与乘积指数，以及二态马尔可夫链和前向—后向算法已独立对原页核对，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF573：式 (47.9)–(47.14)、垂直步骤、伪后验、完成即停止译码法及跨 PDF574 的未检出／检出错误段已独立对原页核对；后页稿须核不重复，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF574：图 47.3 全图及图内文字译注、版权图注、代价三段、§47.4 起段与脚注 URL 均已独立对原页核对；PDF573→574 断句及印本 $6Nj$／$120t/R$ 差异留证。S47-02 漫画气泡首词按印本可辨 `REDUNDAN…` 表达，已修复复核。
- [x] 初译 PDF575：图 47.4 稀疏 $\mathbf H$ 矩阵、图注 $N/M$ 与 $j/k$、斜体编码／迭代译码、7.5% 及 0／1／2／3／10／11／12／13 轮、十万次一次失败均已独立对原页核对，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF576：图 47.5 八个迭代面板与最终 DECODED 画面、图 47.6 曲线／坐标／误差棒／GV/C 标签及两图完整图注与图内文字译注已独立对原页核对，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF577：图 47.7 四面板、图 47.8 两曲线、两图图注和图内术语译注、灰度似然公式、两处斜体小标题及跨 PDF578 的 $j=3$ 结论已独立对原页核对；$N=816$／$10^{-5}$ 只译一次。
- [x] 初译 PDF578：图 47.9 规则／近规则构造、图 47.10 密度演化曲线、图 47.11 无限树局部拓扑及各图注、§47.5 起段和跨 PDF579 的蒙特卡罗长句已独立对原页核对；节题三角在冻结 JSON 保留。
- [x] 初译 PDF579：图 47.12、表 47.13–47.15 逐格、GF(4) 四个 $2\times2$ 映射矩阵、§47.5 阈值／EXIT 图、§47.6 起段及跨 PDF580 的 GF(4／8／16) 结论已独立对原页核对；节题三角与三表结构在冻结 JSON 复核通过。
- [x] 初译 PDF580：算法 47.16 四行公式、GF(2)／GF($2^k$)、图 47.17 曲线与七码长图注、式 (47.15)、不规则图段及跨 PDF581 的 0.4／0.6／0.9 dB 结论已独立对原页核对；图内 `Gallileo`／图注 `Galileo` 印本拼写差异留证，算法单描边框在冻结 JSON 复核通过。
- [x] 初译 PDF581：图 47.18 差集循环码表逐格与曲线资产、§47.7 起段、式 (47.16) 及跨 PDF582 的阶梯结构条件句已独立对原页核对；S47-03 表头与 S47-06 的 11 个粗体 MathML 数字均修复复核。
- [x] 初译 PDF582：式 (47.17)–(47.20)、图 47.19 的 A／B／T／C／D／E 分块、右上零三角与 $M/N/g$ 箭头、阶梯码累加器及一般快速编码前两步已独立对原页核对，见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] 初译 PDF583：快速编码步骤 3–6、式 (47.21)–(47.25) 的符号／矩阵顺序、§47.8 文献名单及跨 PDF584 段落已独立对原页核对；节题三角在冻结 JSON 保留。
- [x] 初译 PDF584：§47.8 末句、§47.9 习题 47.1–47.4、式 (47.26)／(47.27)、§47.10 习题 47.2 解答首段及跨 PDF585 句已独立对原页核对；S47-04 定语句法已修复复核，节题三角在冻结 JSON 保留。
- [x] 初译 PDF585：习题 47.2 解答、式 (47.28)–(47.30)、两条无编号页边公式及 PDF586 第 48 章边界已独立对原页核对；PDF569–585 全十七页源页稿审查记录见 `translation/chapter-47/REVIEW_PARTIAL.md`。
- [x] PDF569–585 十七份页稿的审定草稿与正式 `chapter-47.json` 逐字节相同（269,193 字节；SHA-256 `aa1cdc5e9499b080c2956c9f113c207b5a490f7c3a2f334a2d0e08c5c27edb22`；202 顶层／203 递归块、11 目录、16 图像、4 表、30 条连续编号 MathML 式加 4 条无编号式、1 算法框、4 题／1 解答／1 脚注、末块 `p585-b009`）；式 (47.16) 的原图与逐格可复制 12×28 矩阵均经独立源审和网站验收通过。
- [x] PDF569 本章简短中文导读已明确标为非原书正文，独立 Agent 核对其位置与分隔。
- [x] PDF569–585 逐节逐段原页核对正文、列表、脚注、习题 47.1–47.4、习题 47.2 解答、文献与跨页接续，见 `translation/chapter-47/REVIEW.md`。
- [x] 核实以下十节标题、起始页、段落与无编号小标题；十个节题前三角均在冻结 JSON 可见保留。
  - [x] 47.1 Theoretical properties（PDF569 起；标题与正文已独立原页核对）
  - [x] 47.2 Practical decoding（PDF569 起；标题与正文已独立原页核对）
  - [x] 47.3 Decoding with the sum–product algorithm（PDF571 起；标题、算法与式已独立原页核对）
  - [x] 47.4 Pictorial demonstration of Gallager codes（PDF574 起；标题与图已独立原页核对）
  - [x] 47.5 Density evolution（PDF578 起；标题、图与正文已独立原页核对）
  - [x] 47.6 Improving Gallager codes（PDF579 起；标题、图表与正文已独立原页核对）
  - [x] 47.7 Fast encoding of low-density parity-check codes（PDF581 起；标题、算法步骤与式已独立原页核对）
  - [x] 47.8 Further reading（PDF583 起；标题与文献已独立原页核对）
  - [x] 47.9 Exercises（PDF584 起；标题与四题已独立原页核对）
  - [x] 47.10 Solutions（PDF584 起；标题与唯一解答已独立原页核对）
- [x] 逐项核对 15 幅编号原图及式 (47.16) 原图、图内英文、图注和四张表每个单元格；见 `translation/chapter-47/REVIEW.md`。
- [x] 原页核实编号图 47.1–47.12、47.17–47.19，表 47.13–47.15 及图 47.18 左侧可复制表，无遗漏或重号。
- [x] 逐式核对式 (47.1)–(47.30) 的变量、上下标、算法 47.16 单描边框与四条无编号展示式；正式网站 34 条 MathML 均可读可复制，经独立验收。
- [x] 原页核实式 (47.1)–(47.30) 连续、无重号；四条无编号式及算法框边界均已独立核对。
- [x] 式 (47.16) 保留原书图像，且新增准确可复制的 12×28 MathML 矩阵；独立 Agent 从 PDF581 核 336 格、71 个 $1$ 和第 16 列分隔，逐格一致。
- [x] 独立 Agent 在草稿与正式路径六视口核对术语、交叉引用、11 项目录、34 式、16 图、4 表、算法框、脚注、窄屏局部横滑、深色模式及末页 100% 阅读进度，见 `translation/chapter-47/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成十七页原页与冻结 JSON 源文／结构审查，S47-01～06 全部修复复核，见 `translation/chapter-47/REVIEW.md`。
- [x] S47-01～06 源文／构建问题、三处手机标题拆词与 29 处短尾均修复并经独立复核；正式路径、三次刷新、本地 `verify_registered.py` 与全站 smoke test 通过，完成本章验收。

## 第 48 章：Convolutional Codes and Turbo Codes（PDF 586–593）

- [x] 初译 PDF586：章题与非原书导读、§48.1 三项列表及代数方法三条理由、§48.2 移位寄存器起段和跨 PDF587 的约束长度 7 句已独立对原页核对；S48-01 已改为“在内容上紧密承接第 25 章”并复核。
- [x] 初译 PDF587：图 48.1 三种寄存器及图内英文／八进制名译注、表 48.2 原图和可复制二进制→八进制对应、两类无反馈码段落已独立对原页核对，见 `translation/chapter-48/REVIEW_PARTIAL.md`。
- [x] 初译 PDF588：系统递归码与两编码器码字集合等价、图 48.3 及图内译注、式 (48.1)–(48.3)、有限／无限冲激响应和习题 48.1 已独立对原页核对；S48-02 空心三角已补并复核，冻结 JSON 尚须核图标可见。
- [x] 初译 PDF589：原页纯图页的图 48.4 双网格图、图 48.5 单网格图、transmit／source 与状态轴译注及两条完整图注已独立对原页核对，见 `translation/chapter-48/REVIEW_PARTIAL.md`。
- [x] 初译 PDF590：图 48.6 滤波器与十六状态网格、三种边线／received 行、周期 $2^k-1$、BCJR／Viterbi、路径代价 0／1／2 及习题 48.2 已独立对原页核对；§48.3 实心三角待冻结 JSON 核查。
- [x] 初译 PDF591：图 48.7 双路径、图 48.8 终止网格、图 48.10 编码器及图内译注、非均等保护、§48.4 Turbo 码起段与跨 PDF592 的码率 $1/3$ 句已独立对原页核对；图 48.9 位于下一页，见 `translation/chapter-48/REVIEW_PARTIAL.md`。
- [x] 初译 PDF592：图 48.9 两幅因子图及完整图注、组成网格与迭代消息、停止准则和跨 PDF593 的句子已独立对原页核对；印本关于删余后码率的疑点照原文保留并记于 `translation/chapter-48/SOURCE_NOTES.md`，见 `translation/chapter-48/REVIEW_PARTIAL.md`。
- [x] 初译 PDF593：图 48.11、§48.5、习题 48.3、延伸阅读、§48.6 唯一解答及跨页接句已独立对原页核对；S48-03 语气修订完成并复核，见 `translation/chapter-48/REVIEW_PARTIAL.md`。
- [x] PDF586–593 八份页稿已重建为冻结 `chapter-48.draft.json`（75,691 字节；SHA-256 `8cbcbd6b8b62e767901e196bb482f17946fa5314dcb931b949a6c7cc5f21f579`；69 块、7 目录、11 图像对象、3 条编号 MathML、3 题／1 解答、末块 `p593-b012`），独立 Agent 只读重编译逐字节一致，见 `translation/chapter-48/REVIEW.md`。
- [x] 编写本章简短中文导读，以独立 `intro` 块与原书正文区分。
- [x] 逐节逐段翻译和核对正文、列表、三道习题、唯一解答与参考文献；三处跨页句各合译一次；原页无脚注、代码或算法框。
- [x] 逐节核实标题、起始页、实心三角和无编号“延伸阅读”小标题，见 `translation/chapter-48/REVIEW.md`。
  - [x] 48.1 Introduction to convolutional codes（PDF 586 起）
  - [x] 48.2 Linear-feedback shift-registers（PDF 586 起）
  - [x] 48.3 Decoding convolutional codes（PDF 590 起）
  - [x] 48.4 Turbo codes（PDF 591 起）
  - [x] 48.5 Parity-check matrices of convolutional codes and turbo codes（PDF 593 起）
  - [x] 48.6 Solutions（PDF 593 起）
- [x] 逐项核对 10 幅编号图与表 48.2 原图、图内英文、图注和表内二进制／八进制对应；表 48.2 在图注中另附可复制 MathML。
- [x] 原页核实图 48.1、48.3–48.11 及表 48.2，共 11 份原图资产；48.2 是表号，不是缺图。
- [x] 逐式核对式 (48.1)–(48.3) 的变量、上下标、编号及行内 MathML；原页无代码或算法框；公式网页显示和复制经独立六视口站点 QA 通过。
- [x] 原页核实式 (48.1)–(48.3) 连续、无重号，全部可解析；见 `translation/chapter-48/REVIEW.md`。
- [x] 独立 Agent 在草稿与正式路径六视口核对术语、交叉引用、7 项目录、3 式、11 图像、3 题、窄屏横滑、深色模式和末页阅读进度，见 `translation/chapter-48/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成 PDF586–593 逐页及冻结草稿源文／结构审查，S48-01～03 均修复复核，见 `translation/chapter-48/REVIEW.md`。
- [x] S48-01～03 与 S48-SITE-01～02 均修复复核；正式 `chapter-48.json` 与审定草稿逐字节相同，真实路径六视口、`verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 均通过，完成本章验收。

## 第 49 章：Repeat–Accumulate Codes（PDF 594–599）

- [x] 初译 PDF594：章题、独立导读、§49.1 五步编码框与式 (49.1)、§49.2 四类节点及两段已独立对原页核对；算法单描边框、章题样式和两节实心三角待冻结 JSON／站点核查，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] 初译 PDF595：图 49.1 两面板与小网格、图 49.2 六组曲线及图例、§49.2 两类因子和 §49.3 迭代译码段落已独立对原页核对；§49.3 实心三角与图注块归属待冻结 JSON 核查，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] 初译 PDF596：图 49.3 五面板、标签与全部数值、§49.4 幂律论述、习题 49.1 两问及 §49.5 跨页定义句已独立对原页核对；原页习题题号前无三角，译稿忠实保留，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] 初译 PDF597：图 49.4、五条图示记号、定义与式 (49.2)–(49.5) 已独立对原页核对；印本对 $A$ 的 $L\times M'$ 尺寸和“码率大于等于”后接等号式的两处疑点均按原页保留并记 `translation/chapter-49/SOURCE_NOTES.md`，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] 初译 PDF598：四组实例、图 49.5–49.7 三张矩阵图及图内顶划线、式 (49.6)–(49.11) 的转置／矩阵维数已独立对原页核对，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] 初译 PDF599：图 49.8／49.9 的横线、置换与对角带、线性 MN 码、卷积码、并／串行拼接、Turbo 码、重复—累积码和码的交集六段及交叉引用已独立对原页核对；PDF600 是独立第 50 章导页，见 `translation/chapter-49/REVIEW_PARTIAL.md`。
- [x] PDF594–599 六份页稿重建为冻结 `chapter-49.draft.json`（61,167 字节；SHA-256 `92c74dcbb7654e54d4b8c366f9261a660eddc0e32d50ca0d3c0326a606c58aa8`；62 顶层／65 JSON 节点、64 阅读块、6 目录、9 图、11 条编号 MathML、1 五步单描边框、1 题、末块 `p599-b008`），独立 Agent 只读重编译逐字节一致，见 `translation/chapter-49/REVIEW.md`。
- [x] 编写本章简短中文导读，以独立 `intro` 块与原书正文区分。
- [x] 逐节逐段翻译和核对正文、列表、习题和跨页接续；原页无表格、代码块或脚注。
- [x] 逐节核实标题、起始页、实心三角与章题横线／斜体，见 `translation/chapter-49/REVIEW.md`。
  - [x] 49.1 The encoder（PDF 594 起）
  - [x] 49.2 Graph（PDF 594 起）
  - [x] 49.3 Decoding（PDF 595 起）
  - [x] 49.4 Empirical distribution of decoding times（PDF 596 起）
  - [x] 49.5 Generalized parity-check matrices（PDF 596 起）
- [x] 逐项核对图 49.1–49.9、图内英文与符号、图注、裁图边界；原页无表格。
- [x] 原页核实图 49.1–49.9 连续，共 9 份原图资产；无遗漏或重号。
- [x] 逐式核对式 (49.1)–(49.11) 的变量、上下标、编号与五步算法框；式 (49.1) 两处多余逗号 S49-01 已修复复核；编号式和算法框文字网页显示与复制经独立站点 QA 通过。
- [x] 原页核实式 (49.1)–(49.11) 连续、无重号；113 个 MathML 片段可解析，见 `translation/chapter-49/REVIEW.md`。
- [x] 独立 Agent 在草稿与正式路径六视口核对术语、交叉引用、6 项目录、11 式、9 图、五步单框、习题、窄屏横滑、深色模式和末页阅读进度，见 `translation/chapter-49/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成 PDF594–599 逐页及冻结草稿源文／结构审查，S49-01 修复复核；PDF597 两处印本疑点照页保留，见 `translation/chapter-49/REVIEW.md`。
- [x] S49-01 与 S49-SITE-01～02 均修复复核；正式 `chapter-49.json` 与审定草稿逐字节相同，真实路径六视口、`verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 均通过，完成本章验收。

## 第 50 章导页（PDF 600）

- [x] 对照 PDF600 独立翻译并核对 “About Chapter 50” 全文，包括数字喷泉码导引、习题 50.1 三问和球入箱注；冻结草稿 `chapter-50-intro.draft.json` 为 3,701 字节／SHA-256 `5db5e8d52214c697b65e46185517be6d33f185e49aab5d2258f7852cf6f39f08`，不同于初译者的 Agent 原页／结构审查 PASS，见 `translation/chapter-50-intro/REVIEW.md`。
- [x] 独立 Agent 已对 PDF600 原页、习题 50.1 的三问／空心三角、球入箱说明、9 处可复制行内 MathML 及顶线居中斜体标题完成核对；原页无图表或编号式。正式 `chapter-50-intro.json` 与审定草稿逐字节一致，六视口草稿／正式 QA、`verify_registered.py`、全站 smoke、Node 语法及 `git diff --check` 均通过，见 `translation/chapter-50-intro/{REVIEW.md,SITE_QA.md}`。

## 第 50 章：Digital Fountain Codes（PDF 601–608）

- [x] 初译 PDF601：章题与独立导读、$q$ 元擦除信道、两种反馈协议、广播、RS 码及 $N<q$ 括注、复杂度和跨 PDF602 句已独立对原页核对；本页无图、编号式或习题，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF602：LT 名称及页边注、rateless／universal 术语、$K'$ 与译码成本、§50.1 两步单描边编码框和跨 PDF603 伪随机密钥段已独立对原页核对；节题实心三角与单框仍待冻结 JSON 核查，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF603：§50.2 同一描边译码框的步骤 1／(a–c)／式 (50.1)／步骤 2 层级、图 50.1 六面板与例子数值、§50.3 跨 PDF604 句已独立对原页核对；算法单框待冻结 JSON 核查，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF604：图 50.2 的 $\rho/\tau$ 与图 50.3 三条 $\delta$ 曲线、数值、式 (50.2)–(50.5) 及习题 50.2 已独立对原页核对；印本 $Z$ 求和式无括号照录并记 `translation/chapter-50/SOURCE_NOTES.md`，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF605：Luby 保证与约 5% 开销、图 50.4 三直方图的参数和横轴、§50.4 存储案例、习题 50.3 与跨 PDF606 广播句已独立对原页核对；印本正文称“两种参数设定”而图注列三组，译稿照录，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF606：广播 $0.1\%$／$fK$／$1.1K$、汽车轮播引语与 5% 数值、延伸阅读和 Raptor、习题 50.4 与式 (50.6) 的两项求和任务已独立对原页核对；§50.5 实心三角待冻结草稿核查，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF607：习题 50.5–50.13 九题的题意、难度、数值、交叉引用与原页有无空心三角均独立核对；S50-01 三处难度 $C$ 上标已在页稿修复复核，冻结草稿 MathML 待核，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] 初译 PDF608：§50.6 三段、§50.7 唯一结论句及其居中描边阴影框已独立对原页核对；框样式待冻结草稿／网站核，PDF609 为第七部分扉页，见 `translation/chapter-50/REVIEW_PARTIAL.md`。
- [x] PDF601–608 八份页稿重建为冻结 `chapter-50.draft.json`（93,212 字节；SHA-256 `8b8f4371c3f85a66aa0f3ca787bcf556f0e20dd313889c6eca56fe10d96ebb96`；83 顶层／92 含框 JSON 节点、89 阅读块、8 目录、4 图、6 条编号 MathML、12 题、3 原书框、末块 `box-50-conclusion`），独立 Agent 只读重编译逐字节一致，见 `translation/chapter-50/REVIEW.md`。
- [x] 编写本章简短中文导读，以独立 `intro` 块与原书正文区分。
- [x] 逐节逐段翻译和核对正文、列表、12 道习题、参考文献与跨页句；原页无表格、独立代码块或脚注。
- [x] 逐节核实标题、起始页、实心三角和章题横线／斜体，见 `translation/chapter-50/REVIEW.md`。
  - [x] 50.1 A digital fountain’s encoder（PDF 602 起）
  - [x] 50.2 The decoder（PDF 603 起）
  - [x] 50.3 Designing the degree distribution（PDF 603 起）
  - [x] 50.4 Applications（PDF 605 起）
  - [x] 50.5 Further exercises（PDF 606 起）
  - [x] 50.6 Summary of sparse-graph codes（PDF 608 起）
  - [x] 50.7 Conclusion（PDF 608 起）
- [x] 逐项核对图 50.1–50.4、图内英文与数值、图注、裁图边界；原页无表格。
- [x] 原页核实图 50.1–50.4 连续，共 4 份原图资产；无遗漏或重号。
- [x] 逐式核对式 (50.1)–(50.6) 的变量、上下标、编号及三处原书描边框；S50-01 三处难度 $C$ 上标已在冻结 MathML 修复复核，公式网页显示与复制经独立六视口 QA 通过。
- [x] 原页核实式 (50.1)–(50.6) 连续、无重号；217 个 MathML 片段可解析，见 `translation/chapter-50/REVIEW.md`。
- [x] 独立 Agent 在草稿与正式路径六视口核对术语、交叉引用、8 项目录、6 式、4 图、12 题、三框、窄屏横滑、深色模式和末页阅读进度，见 `translation/chapter-50/SITE_QA.md`。
- [x] 不同于初译者的 Agent 已完成 PDF601–608 逐页及冻结草稿源文／结构审查，S50-01 修复复核；PDF604、605 两处印本疑点照页保留，见 `translation/chapter-50/REVIEW.md`。
- [x] S50-01 与 S50-SITE-01 均修复复核；正式 `chapter-50.json` 与审定草稿逐字节相同，真实路径六视口、`verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 均通过，完成本章验收。

## Part VII: Appendices（PDF 609）

- [x] PDF609 第七部分扉页已独立对原书核题名双行、2590×2620 原图、四边裁切和与附录 A 边界；冻结 `chapter-VII.draft.json` 为 572 字节／SHA-256 `b63bf02e97586398bab47d3c954e619304265b90ab6e9ca05faa9ebb03453a43`、2 块／1 目录，S-VII-01 换行已由本书限定 CSS 修复并在真实浏览器复核，见 `translation/part-VII/REVIEW.md`。
- [x] 独立 Agent 在草稿与正式路径六视口复核双行标题、2590×2620 图像手机局部横滑、320px 图提示、50↔VII 导航、PDF609 末块／100% 与三次刷新；正式 JSON 与审定草稿逐字节相同，本轮 `verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 均通过，见 `translation/part-VII/SITE_QA.md`。

## 附录 A：Notation（PDF 610–612）

- [x] 初译 PDF610：七项记号问答、式 (A.1)–(A.3)、斜体、第 2 章引用与跨 PDF611 接句已独立对原页核对；独立字母 A、横线及居中斜体题名待冻结 JSON／网站核，见 `translation/appendix-A/REVIEW_PARTIAL.md`。
- [x] 初译 PDF611：式 (A.4) 对 PDF610 的接续、七项问答、式 (A.5)–(A.8)、斜体和方括号说明已独立对原页核对；式 (A.7) 上限、指数和积分变量均印作 $z$，照页保留并记 `translation/appendix-A/SOURCE_NOTES.md`，见 `translation/appendix-A/REVIEW_PARTIAL.md`。
- [x] 初译 PDF612：迹／行列式、单位矩阵无编号分段式、真值函数、赋值与等号、式 (A.9)–(A.11) 及第 23／29 章引用已独立对原页核对；S-A-01 分段式多余逗号已修复复核，PDF613 为附录 B，见 `translation/appendix-A/REVIEW_PARTIAL.md`。
- [x] 编写简短中文导读，以独立 `intro` 块与原书 19 条记号问答区分；保留条目顺序和可复制记号。
- [x] 独立 Agent 逐项盘点：原页无图、表、代码、习题或脚注；式 (A.1)–(A.11) 与一条无编号分段式、122 处行内 MathML、真值函数和单位矩阵字形均核对；窄屏局部横滑和深色模式六视口通过。
- [x] PDF610–612 逐条译编和核对文字、符号、公式与第 2／23／29 章引用；S-A-01 分段式标点与 S-A-02 直立转置 `T` 已修复并由不同 Agent 复核，见 `translation/appendix-A/REVIEW.md`。
- [x] 审定草稿与正式 `chapter-A.json` 逐字节相同（46,165 字节；SHA-256 `a37cdca41f77cc597326349571dc9c2e47940b55fe4cd14b2e6dec2574530b01`；49 阅读块、1 目录、12 展示式、末块 `p612-b014`）。独立 Agent 在草稿和正式真实路径的 1440／390／320px 明暗六视口核对题名、记号、公式复制、VII↔A 导航、PDF612／100% 与三次刷新，见 `translation/appendix-A/SITE_QA.md`；`verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 通过，完成本附录验收。

## 附录 B：Some Physics（PDF 613–616）

- [x] 初译 PDF613：附录题与独立导读、§B.1 正文、式 (B.1)–(B.4)、$Z_{(1)}/Z_{(N)}$ 下标和 $10^{23}$ 已独立对原页核对；B／斜体题名与横线、§B.1 实心三角及单个描边投影框待冻结结构／网站核，见 `translation/appendix-B/REVIEW_PARTIAL.md`。
- [x] 初译 PDF614：第二投影框、两条斜体小标题、$1/\sqrt N$ 涨落、耦合／独立自旋和式 (B.5)–(B.10) 已独立对原页核对；图 B.1a 引用保留待后页图核，两个框与小标题目录归属待冻结结构核，见 `translation/appendix-B/REVIEW_PARTIAL.md`。
- [x] 初译 PDF615：图 B.1 三联原布局、图 B.2 双联、曲线／箭头／图例／译注、式 (B.11)／(B.12)、斜体小标题与跨 PDF616 序参量句已独立对原页核对；图注 $\log 2/\epsilon$ 与式 $\ln 2/\epsilon$ 的印本差异照录，见 `translation/appendix-B/REVIEW_PARTIAL.md`。
- [x] 初译 PDF616：临界点典型性失效、50% 与约 $1/2^{N+1}$、第 4 章引用、信息量／能量关系、末段斜体及跨页句不重复已独立对原页核对；PDF617 为附录 C，见 `translation/appendix-B/REVIEW_PARTIAL.md`。
- [x] 简短中文导读独立于原书正文；原页无表格、代码、习题或脚注，2 图、12 式、2 投影结论框和 3 条斜体无编号小标题逐项盘点，见 `translation/appendix-B/REVIEW.md`。
- [x] B.1 About phase transitions（PDF613 起）：原书实心三角、标题层级、正文及交叉引用经可视原页独立核对。
- [x] PDF613–616 逐节逐段译编并由不同于初译者的 Agent 独立审查：式 (B.1)–(B.12) 连续，图 B.1／B.2 的图内译注与图注完整；PDF613／615 两段手机短尾经等义精简后原页复核通过，S-B-01 与 S-B-SITE-01 均关闭。
- [x] 审定草稿与正式 `chapter-B.json` 逐字节相同（37,672 字节；SHA-256 `9d7c313f10ba06aeb68bcf854069743cc8d299baef4554da7a3fbaa07ec494c3`；53 阅读块、2 目录、12 编号式／71 行内 MathML、2 图／2 投影框、末块 `p616-b002`）。独立 Agent 在草稿和正式路径 1440／390／320px 明暗六视口核对框体、图、公式复制、局部横滑、A↔B 导航、PDF616／100% 与三次刷新，见 `translation/appendix-B/SITE_QA.md`；`verify_registered.py`、全站 smoke、Node 语法和 `git diff --check` 通过，完成本附录验收。

## 附录 C：Some Mathematics（PDF 617–624）

- [x] 初译 PDF617：附录题、导读、C.1、三条域公理及表 C.1–C.3 已独立对可视原页逐格核对；冻结结构与网站已在后续验收通过，见 `translation/appendix-C/REVIEW_PARTIAL.md`、`REVIEW.md`、`SITE_QA.md`。
- [x] 初译 PDF618：GF(8) 元素表与 64 格乘法表、§C.2、式 (C.1)/(C.2) 和三项列表已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF619：四条斜体小标题、式 (C.3)–(C.6)、三项编号陈述及跨页接续已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF620：表 C.4／C.5 的 14 组特征值与左右向量、式 (C.7)/(C.8) 和 §C.3 起段已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF621：表 C.6 三组矩阵及 12 组特征对、式 (C.9)–(C.14) 和跨页接续已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF622：式 (C.15)–(C.26)、两行同号推导与印本 C.19 预引均已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF623：式 (C.27)–(C.37)、二阶推导及两条斜体小标题已独立对原页核对；冻结结构与网站已在后续验收通过。
- [x] 初译 PDF624：§C.4 原书数值表 43 行及高清原表图、栏位和分组线已独立逐格核对；`unix` 等宽字形 S-C-01 已修，PDF625 为独立参考文献起页，见 `translation/appendix-C/REVIEW.md`。
- [x] 简短中文导读与原书正文独立分开；原书 10 张可复制表、1 张数值原表图、37 条编号式及 430 处 MathML 已对原页和冻结草稿独立盘点，见 `translation/appendix-C/REVIEW.md`；窄屏排版已通过网站 QA。
- [x] C.1 Finite field theory（PDF617 起）：标题、实心三角、三条域公理与 GF(2/4/8) 表格逐格对原页核对。
- [x] C.2 Eigenvectors and eigenvalues（PDF618 起）：标题、实心三角、左右特征向量与宽矩阵表逐格对原页核对。
- [x] C.3 Perturbation theory（PDF620 起）：标题、实心三角、一阶和二阶推导逐式对原页核对。
- [x] C.4 Some numbers（PDF624 起）：标题、实心三角、43 行数值表与原图逐格对原页核对。
- [x] 八页页稿与冻结 `chapter-C.draft.json` 已由不同于初译者的 Agent 独立源审 PASS；PDF619 一句等义精简后复核。正式 `chapter-C.json` 与草稿逐字节一致（217,367 字节；SHA-256 `fdbb899c3e68dd23efa60b136e86e2ab4af142f5fdb42b6bd0434af5a0849041`；125 块／5 目录／37 式／10 表／1 图，末块 `p624-b003`）。独立 Agent 在草稿和真实正式路径各以 1440／390／320px 明暗六视口验收，短尾清零，公式复制、宽表／原图局部横滑、B↔C 导航及 PDF624／100% 三次刷新通过，见 `translation/appendix-C/REVIEW.md`、`SITE_QA.md`。

## Bibliography（PDF 625–631）

- [x] PDF625–631 七页已按可视双栏原页分别初译 37／49／44／47／47／49／45 条参考文献；共 318 条，保留英文文题及书目信息于 `translation/bibliography/pdf-625.md`–`pdf-631.md`。`chapter-REF.draft.json` 构建为 318 条参考文献块加 1 个标题，原页及网站独立审查均通过。
- [x] PDF625：左栏 17 条、右栏 20 条 Abrahamsen 至 Braunstein 已由不同 Agent 对可视原页逐条核作者、年份、双语题名、书刊、卷期、页码及两栏顺序，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF626：左栏 24 条、右栏 25 条 Bretthorst 至 Gilks 已独立逐条核原页、四处网址与跨页排序；无待修问题，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF627：44 条（左 24／右 20）已由不同 Agent 对可视原页逐条核作者、年份、双语题名、报告／专利／书刊、卷期页码及顺序，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF628：47 条（左 25／右 22）已独立对可视原页逐条核 MacKay 年份后缀、双语题名、Luby 系列、卷期页码、网址与两栏顺序，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF629：47 条（左 22／右 25）已独立对可视原页逐条核 MacKay／Neal 年份后缀、双语题名、卷期页码、网址与重刊说明，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF630：49 条（左 24／右 25）已独立对可视原页逐条核作者、双语题名、编者、卷期页码、报告／会议、Raptor 网址及跨页顺序，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] PDF631：45 条已由不同 Agent 对可视原页逐条核至 Ziv 与 Lempel 两条末项；PDF632 为独立索引起页，七页 318 条源审无待修问题，见 `translation/bibliography/REVIEW_PARTIAL.md`。
- [x] 不同于初译者的 Agent 已对 PDF625–631 可视原页及冻结 `chapter-REF.draft.json` 独立审查 PASS：318 条无漏项、错序、元数据或译义待修；319 块／1 目录／末块 `p631-b045`，SHA-256 `9f45cca6a19491868f184ddd8ce84e8947d20a4f4f825b20c81d86e6aab7e3f8`，见 `translation/bibliography/REVIEW.md`。
- [x] 保留可检索的原作者和英文书刊名，并为文题提供准确中文译名；318 条原书条目与正文年份引用已独立核对。原书 PDF192 所引 McEliece（1977）未收于书目，照原页保留并记 `translation/GLOBAL_REVIEW.md` 的 G-01。
- [x] 独立 Agent 在草稿和正式参考文献路径以 1440／390／320px 明暗六视口验收，318 条内容、226 处斜体、标题顶线、悬挂缩进、短尾清零、C↔REF 导航及 PDF631／100% 三次刷新均通过；正式与草稿六张整页截图逐字节相同，见 `translation/bibliography/SITE_QA.md`。

## Index（PDF 632–640）

- [x] PDF632：三栏 112 个主词项、35 个从属项已译编并独立对可视原页审查；S-I-01 补回 `ban (unit)` 的英文限定并复核，见 `translation/index/REVIEW_PARTIAL.md`。
- [x] PDF633：三栏 106 个主词项、65 个从属项及 1 个第三层项，`channel` 跨栏接续和 8 处粗体页码已独立对原页核过。
- [x] PDF634：三栏 121 个主词项、69 个二级项及 2 个三级项已独立对原页核过；S-I-02 补回 `deciban (unit)` 的英文限定并复核，`error-correcting code` 跨至 PDF635。
- [x] PDF635：三栏 117 个主词项、63 个二级项及 5 个三级项，前 43 项承接 PDF634；粗体页码、符号和等宽词已独立对原页核过，`weight enumerator` 译名与正文统一为「重量枚举函数」。
- [x] PDF636：三栏 144 个主词项、34 个子项、无页码父项 `key points`、罗马页码 `xii` 与 13 处粗体页码均经不同于初译者的 Agent 对原页审查通过；PDF637 从 `life in high dimensions` 开始。
- [x] PDF637：三栏 118 个主项、52 个子项、3 个三级项、9 处粗体页码及 Monte Carlo 多级层级已独立对原页核过；S-I-03 恢复两处 *a posteriori* 原书斜体后复核关闭。
- [x] PDF638：三栏 135 个主项、47 个子项、11 处粗体页码及 notation／paradox／prior 层级已独立对原页核过；S-I-04/05 恢复 `noisy typewriter` 的 **148** 与 `$p$-value` 原书字形后复核关闭。
- [x] PDF639：三栏 125 个主项、56 个子项、3 处粗体页码，`puzzle` 五项跨页接续、sermon／software／source code 层级及 xi／xii 罗马页码均独立对原页核过；S-I-06/07 恢复五处等宽原词并澄清 `spell` 为拼写检查程序，复核关闭。
- [x] PDF640：末页三栏 169 个主项、20 个子项、9 处粗体页码，无页码父项 test／weight、Student-$t$ 数学斜体和两处等宽专名均经不同于初译者的 Agent 对原页核过；S-I-08 将 syndrome 译名统一为正文的「伴随式」，复核关闭。PDF640 为原书末页。
- [x] 保留原书印刷页码、范围、子项缩进、`see`/`see also` 指向及英文原词可检索性；1599 词项、2435 个印刷页码链接、101 个 `see` 链接及全部对应阅读锚点经非初译 Agent 独立核对，见 `translation/index/REVIEW.md`。正式网站六视口和断网跳转已通过。
- [x] 不同于初译者的 Agent 对可视 PDF632–640 逐条独立审查，S-I-01–08 修复复核；全书术语统一后的七处标签另经非初译 Agent 增量原页和网站审查。最终草稿与正式 JSON 逐字节一致（705,257 字节，SHA-256 `230ba57c067299b3d41c180da363925a3f7b657e2016b3a6ca52c21136c85bac`）。独立 Edge 1440／390／320px 明暗六视口草稿与正式路径验收通过：1150 块、1599 项、2435 页码链接、101 `see` 链接、短尾与横溢为零，REF↔IDX 导航及 PDF640／100% 三次刷新稳定；见 `translation/index/REVIEW.md`、`REVIEW_TERMS_2026-10-04.md`、`SITE_QA.md`。
