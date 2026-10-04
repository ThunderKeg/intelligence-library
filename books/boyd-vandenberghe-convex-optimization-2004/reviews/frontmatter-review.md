# 卷首独立审查

审查日期：2026-10-03。审查者：`convex_review` Agent，未参与这些文件的初译。本次仅修改本审查记录。

## 结论与验收边界

**卷首内容、网页排版及卷首阅读功能审查通过。** 全书尚未完成；FM-V04 的跨章一致性检查保留到全书审查阶段，不表示卷首内容不完整。

已逐页目视核对唯一来源 `Convex Optimization – Boyd and Vandenberghe.pdf` 的物理第 1–14 页，并逐段核对 `translation/frontmatter.md`、`translation/contents.md`、`translation/preface.md`。目录 130 条记录已逐项核对标题含义、编号、顺序和原书页码。未发现可确认的漏译、改变原意、目录页码错误或图形裁剪缺失。此内容结论仅适用于下列文件快照，不代表后续章节已通过；网页复核结果另见后文。

目视依据为 `tmp/convex/render/pdf-001.png`、`pdf-003.png` 至 `pdf-005.png`、`pdf-007.png` 至 `pdf-013.png`；另外从同一 PDF 实际渲染并查看物理第 2、6、14 页，确认三页均为空白，图像位于 `tmp/convex/review-frontmatter/`。没有仅凭提取文本认定原页已核对，也没有调用本机模型。

## 逐页核对结果

| PDF 物理页 | 原页内容 | 已核对结果 |
| --- | --- | --- |
| 1 | 半书名页 | `Convex Optimization` 对应“凸优化”，未漏正文。 |
| 2 | 空白页 | 实际查看渲染图，确认无正文、图形或页下注。译稿保留页标记。 |
| 3 | 扉页 | 书名、两位作者、两所大学及电气工程系完整。出版社徽记保留，附中文名称与完整英文名称译注。 |
| 4 | 出版信息及 CIP 数据 | 出版城市 8 项、地址、美国出版说明、两个网址、2004 年版权与首次出版、2009 年第七次印刷及修订说明、印刷地、英国图书馆说明、CIP 编目数据、两种 ISBN、网址责任说明均在。编号逐一相符。 |
| 5 | 献词 | Anna、Nicholas、Nora、Daniël、Margriet 五个人名及两组关系完整；Daniël 的变音符号保留。 |
| 6 | 空白页 | 实际查看渲染图，确认无内容。 |
| 7（目录首页） | 前言、第 1 章、第一部分、第 2–3 章 | 28 条目录记录均已对照原页；章节、各节、文献说明、习题及页码相符。 |
| 8（viii） | 第 4–5 章、第二部分、第 6–7 章 | 39 条目录记录均已对照原页；未漏节或改变页码。 |
| 9（ix） | 第 8 章、第三部分、第 9–11 章 | 40 条目录记录均已对照原页；未漏节或改变页码。 |
| 10（x） | 附录 A–C、参考文献、符号表 | 23 条目录记录均已对照原页；`LDL^T` 的上标在 Markdown 数学源中保留，后续网页复核显示正常。原目录最后为 Notation，未自行添加 Index。 |
| 11（xi） | 前言开头 5 段 | 最小二乘和线性规划的地位、内点法的发展、应用范围、识别与表述为凸问题的好处、建议学习路径逐段对应。各处范围限定与“我们相信”等作者判断保留。 |
| 12（xii） | 本书目标、读者对象 | 目标强调段、数学基础要求、书的定位、算法与复杂度论述的简化程度、适用读者均完整。导读明确标为“导读（编者）”，没有混入原书正文。 |
| 13（xiii） | 读者对象续段、课程使用、致谢、作者署名 | 与前页“我们也希望”连续衔接；学季与学期、两个学季课程的区别保留。名单、贡献、交叉引用、1994 年资助说明、两位作者及所在城市均已核对。 |
| 14 | 空白页 | 实际查看渲染图，确认无内容。 |

## 专项核对

- 目录：物理第 7–10 页分别为 28、39、40、23 条，共 130 条。原书三个部分、11 章、3 个附录以及未编号的文献说明、习题、参考文献和符号表顺序一致。章节编号、部分名称及粗体区分保留了文字层面的目录层级。
- 出版数据：`0 521 83378 7`、`978-0-521-83378-3`、`QA402.5.B69 2004`、`519.6–dc22`、`2003063284` 与原页一致；出版网址所含 `9780521833783` 一致。
- 致谢：从 A. Aggarwal 至 Y. Ye 的 26 项名单完整；J. Jalden、A. d’Aspremont 的两项例子及 `§6.5.4`、`§6.5.5` 的分别对应关系正确；P. Parrilo 与习题 `4.4`、`4.56` 的对应关系保留；Igal Sason、Arkadi Nemirovski、Kishan Baheti 的贡献均完整。
- 图片：已将 `assets/frontmatter/cambridge-university-press.png` 与物理第 3 页目视比较。盾形徽记及两行英文名称完整，边缘未截掉文字或纹章内容，旁注“剑桥大学出版社”对应准确。图片文件本身清晰；后续网页复核中尺寸与深色背景表现正常。
- 公式、代码、表格及脚注：本范围没有编号公式、算法代码、数据表格或原书脚注。目录 C.3 唯一数学片段 `$LDL^T$` 的转置上标源文本正确；目录改排为表格，记录逐项已核对，窄屏复核及其修复记录见后文。
- 跨页与读者边界：`preface.md` 中物理第 12–13 页跨页段落保持为一个连续段落。页标记属于 HTML 注释，后续实际阅读器测试确认其正确隐藏。

## 排版复核及问题修复

已查看当前阅读器下的 1440 像素浅色、390 像素浅色、390 像素深色、320 像素深色截图。目视依据包括 `tmp/convex/reader-qa/` 中的开头、徽记及目录末表截图，并独立补充了 CIP、献词、前言第 12–13 页的跨页段落、致谢与署名截图，保存于 `tmp/convex/review-frontmatter-reader/`。320 像素致谢另使用两个有重叠的实际视口截图复核，避免长元素截图中的固定导航栏遮挡干扰判断。上述内容均可阅读，未见段落丢失、字形缺失或内容横向溢出，页标记没有显示在正文中。

排版复核发现并关闭 1 项实际问题：

| 编号 | 严重程度与状态 | 位置 | 证据与修复复核 |
| --- | --- | --- | --- |
| FM-P01 | P2，已修复并复核 | 原目录 PDF 7–10 对应的 4 张两列表格，右列表头 | 首次自适应修复使用末列 `4.2em`，4 个视图中“原书页码”的末字均被裁切。审查者实际测得单元格宽约 54.59 像素，文字右缘超出单元格 7.40625 像素，`scrollWidth=62` 大于 `clientWidth=55`。构建 Agent 将本书目录末列改为 `6em`，并增加所有 `th`/`td` 的文本边界断言。审查者重新目视 320 像素深色与 390 像素浅色表头，末字已完整；随后独立执行更新后的测试，卷首 3 页 × 4 视图共 12 项通过，全部表格单元格左右文本边界均通过检查。 |

独立补充测试确认：目录仍为 130 行，`LDL^T` 保留原生 MathML、`data-tex` 和 `application/x-tex` 注释；图像已解码；三个阅读页的块数与构建文件一致；无公式错误、未解析数学标记、页标记外露、失效页内锚点或整页 PDF 嵌入。徽记、导读、CIP、跨页段落与署名的浅深色显示正常。最终复测材料位于 `tmp/convex/review-frontmatter-reader/final/`，`results.json` 中 `checksPassed=true`、`errors=[]`。测试使用当前 `app.js`、`styles.css`，仅在浏览器请求中注入本书目录，没有修改共享 `books.js`；这不是发布状态验收。

后续第 1 章修复为本书引入本地 STIX Two Math 字体，并为已具备内容的目录条目添加 8 条链接。审查者再次独立运行了包括卷首在内的 5 个阅读页 × 4 个视图检查，共 20 项通过，并目视确认 320 像素目录中的 `LDL^T`、长标题换行及数字页码仍完整。补充复测证据位于 `tmp/convex/review-chapter01/final-stix/`。下方同时记录此轮 JSON 快照；后续新增图片点击行为尚不属于本记录的验证范围。

## 验收状态

下表记录本阶段已关闭的检查项及需在全书结束时处理的检查项。

| 编号 | 状态/重要程度 | 源页与目标 | 待核内容及关闭条件 |
| --- | --- | --- | --- |
| FM-V01 | 已通过 | PDF 1–14；三个卷首阅读页 | 内容块、导读、徽记、署名显示正常，页标记隐藏；实际阅读器中无 HTML 源码外露或内容被吞掉的现象。 |
| FM-V02 | 已通过 | PDF 7–10；目录 | 130 行、原书页码与标题层级完整；数字页码及表头在窄屏均完整可见；长标题正常换行，`LDL^T` 显示正常并保留可复制数学源。卷首之间的导航及移动目录测试通过；未译完章节的全书导航在最终审查时处理。 |
| FM-V03 | 已通过 | PDF 3、11–13；图片及前言 | 浅深色及窄屏下的徽记、长致谢段、导读、CIP、署名和跨页段落正常。 |
| FM-V04 | 待验，后续全书一致性项 | PDF 7–13；章节目录与前言 | 后续译完有关章节后，统一目录与正文标题、`self-concordance`、`S-procedure`、`phase I` 等术语及 `§6.5.4`、`§6.5.5`、习题 `4.4`、`4.56` 引用目标；目前未发现本范围内的含义错误。 |

## 本次文件快照

SHA-256：

| 文件 | 哈希 |
| --- | --- |
| 根目录源 PDF | `40D976C83C18CCE1900EFF8C41BD5AD408C102B813AF39D05FF85678CCF8D76E` |
| `translation/frontmatter.md` | `5FA9213B485068CEDEAAD2DB5D8EF84F0D3D9963F39037090C2C38DCE951ED3D` |
| `translation/contents.md` | `8892333505C743BFFA73B360D976EB3FF72F3B99DBE7D00A631341465231CBDE` |
| `translation/preface.md` | `8EA026C635B14435D2DAB8907B6CCD6C21E025855B4551BE5B4430B2FB352168` |
| `assets/frontmatter/cambridge-university-press.png` | `0F5967D61B20E75C1A2E7EE8CCA0C839C6F80DE71A8B2090A3EA8EBE93334F29` |
| 排版复核 `chapter-frontmatter.json` | `6835C83C27376D474B94DBC79E45D4180E668F76ED1AC46DC8A4660A26EFCE8E` |
| 表头修复后 `chapter-contents.json` | `7BB4A028E1B3392363F1A3E489CB2EC12F7069DA7C04DB494CC129F8E9FAB22B` |
| 排版复核 `chapter-preface.json` | `BFBF7EC56C159EE6B6EC49A79040F8742BD55D303AFF33DB06750A4FC12601F9` |
| 本地字体更新后 `chapter-frontmatter.json` | `0279CF4C19A64DB78E42706DBB787456671F55F3826C1EA465A1C56CACF22DAA` |
| 本地字体及链接更新后 `chapter-contents.json` | `AB059E28541746E7A67DD8790EBD3E640E57858453830D5D40119189C6BB5029` |
| 本地字体更新后 `chapter-preface.json` | `98EBC585479ABEB1B01FBAE1B9EA73E51D3C1D3BECD1AF5BD1BD64AB28CA82A0` |

本记录不授权将未验收章节发布为已完成。后续修订须基于新文件快照补充复核结果。

## 原尺寸图片链接补验

2026-10-03，针对后续新增的 `figure-image-link` 包装单独补验。审查者使用实际阅读器的 1440 像素浅色与 320 像素深色两种视图，点击剑桥大学出版社徽记，均在新标签页打开同一本地 PNG，浏览器报告自然尺寸为 444×108；原阅读页文字不变。已目视两种视图的图片、中文图注及英文名称译注，没有裁切或遮挡。证据为 `tmp/convex/review-frontmatter-reader/image-link/` 中的两张截图及 `results.json`。该功能补验通过。

此次 `chapter-frontmatter.json` 的 SHA-256 为 `A45CA496686706E99CDA192570215311FDD2A5DD9ACE6F4B343E17DB47D3DD9F`。本次只补验新增图片链接，不把其他书页或尚未完成章节视为已验收。

## 第 3 章集成后的差异补验

2026-10-03，集成器已把本书样式改为同步嵌入首块，并为第 2、3 章已生成目标补充目录链接。审查者没有据此重译卷首，而是独立核对字节级差异：将当前 `chapter-frontmatter.json`、`chapter-preface.json` 的受控 style 换回原精确 link，按原紧凑 JSON 与 Windows CRLF 序列化，分别精确重构上节图片链接版 SHA `A45CA496…` 和原已审前言 SHA `98EBC585…`。目录另剥离指向第 2、3 章的 14 条自动链接，同样精确重构原已审 SHA `AB059E28…`。所有卷首 Markdown SHA 仍与上表相同，图片与数学源未变。独立证据为 `tmp/convex/review-chapter03/final-snapshot/earlier-frontmatter-delta.json`，保留完整哈希及快照。

当前目录自动链接共 22 条，本轮第 3 章贡献 7 条。审查者逐一验证全部链接目标，并在桌面与 320 深色实际点击目录“3 凸函数”，均打开第 3 章首块且定位顶部 85px；证据为 `tmp/convex/review-chapter03/navigation-final/`。既有卷首内容结论保持有效，后续全书术语和全部引用仍按 FM-V04 复核。

审查者再次独立运行当前目录/第 1/第 2 章四视图共 12 项检查，全部通过，包含目录所有表格单元格的左右文本边界；结果位于 `tmp/convex/review-chapter03/earlier-chapters-qa/`。

| 当前文件 | SHA-256 |
| --- | --- |
| `chapter-frontmatter.json` | `6FE9C5D339F8E3B010BDE84974C269185290813AAF1E40E8E2612DE526815A9C` |
| `chapter-contents.json` | `41C9D6A1D7FC6E6E363A402EEE64B2084FD3AF9CEE297EC259557B8F72DB0158` |
| `chapter-preface.json` | `EC4477A0A2E6519C6B050637BCE638F09B5580043FB4CAAF8DD642D423ACEBBB` |

## 第 4 章集成后的生成增量复验（2026-10-04）

原文译稿 SHA 与此前已审版本全部相同。本次独立将自动引用链接移除，并只把嵌入 CSS 中的 `:is(.example, .remark)` 扩为 `:is(.example, .remark, .algorithm)` 后，与前次已审 JSON 的正文、数学、结构和元数据完全一致；本单元不含 `.algorithm` 元素。新增跨章引用已随第 4 章检查，当前八单元共 499 个链接目标全部有效，桌面/窄屏共 14 次真实目录及引用点击通过。没有重新翻译或遗漏已审内容，原验收结论继续有效。

最新有效 JSON：

| 单元 | SHA-256 | 自动引用数 |
| --- | --- | --- |
| frontmatter | `8054A55DCE1D7007212AFCCF6EEFBB9ED6CD093CA23EBEDB26177A1371DB5513` | 0 → 0 |
| contents | `346A0B4E4AB6E5F568EF86B26480E408749B76EB1386E96B01A030551EB8C3D9` | 22 → 30 |
| preface | `5A64B863CB91066B0981A190F47C1B4AB16BF4B6A2CB12C50B88CD046C49A5F0` | 0 → 1 |

独立旧/新哈希与逐块差异证据：`tmp/convex/review-chapter04/final-snapshot/generated-delta-independent.json`；引用实测：`tmp/convex/review-chapter04/navigation-final/results.json`。详见第 4 章审查记录。


### 第 5 章集成后的引用增量复验（2026-10-04）

独立比较 `tmp/convex/chapter05-integration-before/` 与当前生成文件：源稿 SHA 全部不变；剥离自动引用链接后所有 JSON 字段及 MathML 完全一致，本书 CSS 未变。当前全书已构建 10 单元的 856 条链接目标逐项存在，中文标点外部引文的章/节没有误链到本书。证据 `tmp/convex/review-chapter05/prior-units-independent-delta.json`、`external-citations-independent.json` 和 `navigation-final/results.json`。本单元先前内容与网页验收结论维持。

- `frontmatter` JSON SHA-256 `8054A55DCE1D7007212AFCCF6EEFBB9ED6CD093CA23EBEDB26177A1371DB5513`。
- `contents` JSON SHA-256 `128689492DDFEBEE20844B7CBF18D2A2DA4329B33D3D3A39CB577FE2BD171FE8`。
- `preface` JSON SHA-256 `5A64B863CB91066B0981A190F47C1B4AB16BF4B6A2CB12C50B88CD046C49A5F0`。


## 第 6 章集成后的引用增量复核

独立以 `tmp/convex/chapter06-integration-before/` 的已验收快照为基线，核验源稿 SHA 不变；逐块仅剥离 `data-convex-reference` 链接后，正文、全部 MathML 和块元数据完全一致。本书 CSS 未变。本轮仅新增可用的第 6 章静态引用，原内容审查结论继续有效。11 单元的 982 个现有引用目标均已独立检查，相关跨章点击已实测。证据 `tmp/convex/review-chapter06/integration-independent.json` 与 `navigation-final/results.json`。

- `contents` 当前 JSON SHA-256：`AE97D6BAD5F877894E469B44EB5D59BD71CBC271DDFD7AD8EC61B741CB3ADBDC`。

- `preface` 当前 JSON SHA-256：`D9158FDBC78EC50196C996935B7F42F0C3C31B3D9F81E0AFF3AB5DB62BA3A947`。


## 第 7 章集成后的静态引用增量复验

独立将本次生成稿与 `tmp/convex/chapter07-integration-before/` 中的已验收快照比较：源稿 SHA 未变；剥离 `data-convex-reference` 自动链接后，JSON 内容、数学、结构、元数据及同步嵌入样式完全一致。仅增加已经存在的第 7 章目标链接。当前 contents JSON SHA-256 为 `32A00B2E9586E288809B563F8F34BE1D28ABF19B250327E5708BA8E738D5363A`。证据 `tmp/convex/review-chapter07/integration-independent.json`；全部 12 单元 1082 条静态引用目标独立核实存在，并已在桌面/窄屏实际点击本单元进入第 7 章。此前正文和排版验收仍有效。


## 第 8 章与第三部分集成后的引用增量复核

独立 baseline `tmp/convex/review-chapter08/old-units-before/` 与最终稿比对通过：本单元译文源 SHA-256 `8892333505C743BFFA73B360D976EB3FF72F3B99DBE7D00A631341465231CBDE` 未变；剥离自动引用锚点后，正文、全部 MathML、结构、元数据及嵌入样式完全相同。当前 JSON SHA-256 `C30CC16B0C59ADAE74C7F3FC78DADD4557623D2C5D96D84242C5C34FECCA59F5`。仅增加可用的生成引用；第 8 章测试另核准全部 1,200 个静态目标和实际跨章导航。本单元已有内容验收结论保持有效。证据 `tmp/convex/review-chapter08/integration-independent.json`、`navigation-final/results.json`。

## 第 9 章集成后的引用增量复核

独立比较 `tmp/convex/chapter09-integration-before/` 与当前生成文件，通过。旧源稿哈希未变；解开自动引用 anchor 后，正文、数学、样式、结构和元数据完全相同，本单元仅新增指向第 9 章的有效引用。当前目录 JSON SHA-256：`1e498e655af2ef8e16abfeb015b0b08adce24cf914d5e523e476ca7a33d251b8`。证据 `tmp/convex/review-chapter09/integration-independent.json`；所有 1379 条已生成引用目标存在，并在桌面与 320px 窄屏实际点击本单元到第 9 章验证落点。既有内容审查结论保持。


## 第 10 章集成后的自动引用增量复核

独立核对 `tmp/convex/review-chapter10/integration-independent.json`：本单元源稿 SHA `8892333505c743bffa73b360d976eb3ff72f3b99dbe7d00a631341465231cbde` 不变；去除自动生成的引用链接后，JSON 与第 10 章集成前的已审版本完全一致。新增链接指向已独立验收的第 10 章，正文、MathML、样式、页码和原图片均不变。旧 JSON SHA `1e498e655af2ef8e16abfeb015b0b08adce24cf914d5e523e476ca7a33d251b8`，当前 JSON SHA `3bc8245b1dfa09a88e52441218f063e948c6165c15535de7ff45b5556f96890c`。全部 1,528 条静态目标校验通过，并已在桌面浅色/320 深色阅读器中实际点击本单元到第 10 章的引用，目标定位正确。该增量不改变此前内容审查结论。


## 第 11 章集成后的自动引用增量复核

独立对照 `tmp/convex/chapter11-integration-before/` 冻结基线：本单元源码 SHA `8892333505c743bffa73b360d976eb3ff72f3b99dbe7d00a631341465231cbde` 未变；去除自动引用链接后，全部正文、数学、结构、源页和 CSS 与已审版本完全一致。只新增指向现已译出的内容的静态引用，不涉及原文重译。旧 JSON SHA `3bc8245b1dfa09a88e52441218f063e948c6165c15535de7ff45b5556f96890c`；当前 JSON SHA `7a6785c7012a4402b0d30a352dc50a35531d94970c27be524a050fa29061c0f8`。

证据 `tmp/convex/review-chapter11/integration-independent.json`；本轮全部 18 单元的 1837 条引用目标均独立核准。第 11 章实际导航另测 32 次，通过。本单元既有内容审查结论保持有效；全书一致性仍以最后整体审查为准。


后续稳定单元接入造成的静态引用更新，统一见 [引用链接后续记录](reference-link-updates.md)。本章上述冻结哈希保留为独立审查时的证据快照。
