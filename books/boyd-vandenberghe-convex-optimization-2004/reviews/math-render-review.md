# 数学字形与叠置符号修复独立复验

结论：**冻结的 20 个单元数学显示修复通过；没有未解决的显示回归问题。** 本次只验收该范围的数学显示、内容保全与阅读回归，不代替附录 A/C 或全书最终内容审查。

审查者 `/root/convex_review` 未实施本次构建器修复。证据统一在 `tmp/convex/review-appendixB/`；所有测试仅写独立目录、浏览器临时注入本书目录，不修改共享站点文件。

## 冻结范围与问题

范围为卷首三单元、第 1–11 章、三部分扉页、附录总扉页、附录 A/B，共 20 单元。修复前 MathML `mathvariant` 在当前 Chromium 的 rich 路径未稳定显示粗体/花体；附录 A 的两个正交直和符号又被非法 `mo` 层包住，成为横排。原始 TeX 记号正确。

构建器 SHA-256 `5d781b4057d259dab33c2da80ed97bf9f61a03ce8e5c5f74f8b1c3035f11cf55`。修复前基线为 `tmp/convex/math-render-before/manifest.json` 与逐单元 JSON；下列结果均以 `final-inputs.json` 的冻结字节运行，测试结束再次核对哈希。

## 原文保全与字形核准

- 独立脚本 `preservation_independent.py` 没有调用构建器的字形映射函数，按 Unicode 字符名称与 NFKC 分别核对每个输出。全部 4,576 个 bold 节点与 697 个 script 节点符合原属性，合计 5,273。扫描无遗留的未转换 bold/script 节点。
- 对 2 个叠置节点，确认 `mover` 直接包含 ⊕/⊥ 两子节点，未继续套入 `mo`；保存的原节点可逆还原。
- 去掉两边自动生成的交叉引用包裹、反向恢复上述显示节点及相应纯文本摘要后，20 份整个 JSON 结构相等；包括正文、图像路径/归属、块 ID、来源页、目录、顺序和元数据。全部 19,163 个数学的 `data-tex` 与 TeX annotation 前后逐项相等，且各节点两份原始 TeX 互相一致。
- 全部源 Markdown 与书内 CSS 的 SHA 与修复前基线相同。没有用重新翻译或更改公式来取得显示通过。

原 PDF 28/44/144/667 的高倍率局部已实际查看，核对粗体 R/S/1、花体 E/D/R 和一般斜体变量；原页 660 已实际查看，核对 (A.9) 及下段两个正交直和。新浏览器截图共 16 个粗体/花体代表样本（8 种×桌面与 320 深色）已目视，符号清晰且不与普通变量混同。A 两处叠置符号×两视图另有 4 个新截图，垂直排列、水平中心及行内行高均正确。没有声称测试原稿中不存在的黑板体或 Fraktur 类型。

证据：`preservation-independent.json`、`variant-coverage-independent.json`、`source-typography-evidence.json`、`glyph-final/results.json`、`stacked-final/results.json`。

## 网页与阅读回归

- 独立实际 reader：1440×960 浅色、390×844 浅色、390×844 深色、320×740 深色。标准检查 20×4=80 视图全部通过，含数学文本/单元格对齐、伸缩括号、表格、图片、目录和最后单元的进度恢复；结果 `all20-reader-independent/results.json`。
- 另外独立遍历同样 80 视图的所有数学叶节点，累计 76,652 次数学节点测量。所有初始左端、滚动内容右端、滚至末端的右边界可达；行内数学没有被祖先容器截断，页面没有横向溢出。结果 `typography-regression/results.json` 与逐视图 geometry 文件。
- 第 1、2、4、8、11 章与附录 B，每章四视图两处位置，48 个情景逐一保存后刷新并重新打开，共 96 次恢复检查通过，目标块 ID 保持、目标位置为顶栏后约 85 px。结果 `restore-typography/results.json`。
- 20 单元全部 1,972 个静态链接均找到实际目标；附录 B 的目录、章内/跨章链接、前后章导航共 18 次实际点击通过。4 处外部被引著作段落的节号没有误连本书。结果 `navigation-final/results.json`。

## 当前 JSON 哈希

下表供集成者为旧审查记录统一闭合当前字节。未在本轮并行改写旧章审查文件。

| 单元 | 数学数 | 字形节点 | 叠置节点 | 当前 JSON SHA-256 |
| --- | ---: | ---: | ---: | --- |
| frontmatter | 0 | 0 | 0 | `8054a55dce1d7007212afccf6eefbb9ed6cd093ca23ebedb26177a1371db5513` |
| contents | 1 | 0 | 0 | `1470c9f084ec0dd64699dc188303fbe1f6fc2b70fa1f9a22747676aa9a32d05a` |
| preface | 0 | 0 | 0 | `d9158fdbc78ec50196c996935b7f42f0c3c31b3d9f81e0aff3ab5db62ba3a947` |
| 01 | 149 | 72 | 0 | `2ba2a24779e950116930590e2503bf44d227a02bd8cfd6c15dc99b00bf287f66` |
| part-I | 0 | 0 | 0 | `d4ed7d5712d50625292013728556abf0616256b67af11a0a4cde1a5fde14047c` |
| 02 | 1745 | 355 | 0 | `441ef631295ca78e262b3d8736e3b0207df89408bb043b5da0e7777b9a9899ad` |
| 03 | 2430 | 557 | 0 | `0aa4a61b6121694bce7136c639005c13ea44e8da27d7edfbd86f56610f62319d` |
| 04 | 2726 | 641 | 0 | `808cdcae17369ebe364bccb53458ea25b09c471b35a175b6455dbc7b41b5dcb9` |
| 05 | 1947 | 454 | 0 | `4e84538c379f63477a8ed49d876be6337d6a00b2a10892d08f1c7e8ec45ae85b` |
| part-II | 0 | 0 | 0 | `424539bae793664c2f180b261e9bf26df02e0955e909e8411730b4baf15a59cc` |
| 06 | 1490 | 290 | 0 | `f09553dd938bb6d42c995cc960a22ddad3b9b9ec4feb1a35b7f546d2d529093b` |
| 07 | 1425 | 571 | 0 | `693af1b291dfd586283315a665078edd9af256f481bfac90f7fc2ff32839b620` |
| 08 | 1614 | 606 | 0 | `4cb96da4dfdf8df4e557db5d644cbd1e4d14c21abff322eaa8f06e7633a398bd` |
| part-III | 0 | 0 | 0 | `15fabe8ee349eb827e5e366cc833d04f9ba215e7eb2a3af68d39a8bf4b1bc9a5` |
| 09 | 1829 | 374 | 0 | `01006ed8acc073c785870f6a4414de9db1890c911c4ab32a7c9ecad5ec5cf06c` |
| 10 | 1062 | 314 | 0 | `499db83a361ba7b492cf1725920073ed22dd580b9c04d95a8bdd706cde57d3f3` |
| 11 | 1820 | 424 | 0 | `3d4f31ea473ff11e3ab137ca22c32189e42c9dd4366b2fb5a0617f252cc9e2bd` |
| appendices | 0 | 0 | 0 | `34708c62cd4b3c870d66471aaca38f05a9758ed7507414d6a11c38e9c40d281b` |
| A | 750 | 503 | 2 | `1d7ac078c0fb16182c33e1c8cb50493179bb8b1ba8bb5cd21f0b47f7f28fbdec` |
| B | 175 | 112 | 0 | `3ce46346ae70b729bd17ae37254fbf1da4a2a2c2c0c0d17b67f9140ecbcb0624` |

本次显示验收不意味着全书工作完成；剩余内容单元、参考文献及全局一致性仍须按任务清单独立审查。
