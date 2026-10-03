# 《Deep Learning: Foundations and Concepts》全书整体独立审查

审查者未承担本书各章初译；本报告只记录全书层面的交叉检查和站点复验，不替代各单元对 PDF 原页的逐页审查。原书依据为仓库根目录 656 页 PDF。检查对象为 28 份主源稿与 JSON、术语表、任务清单、各单元审查记录，以及阅读器、样式、Service Worker 和 GitHub Pages 工作流。

## 全书交叉引用问题及修订复验

### G1：原书页边交叉引用

PDF 页边红字中的 `Chapter`、`Section`、`Appendix` 是原书提供的阅读指向。按 PDF 物理页定位，将 93 条 `Chapter`、275 条 `Section`、27 条独立的 `Appendix` 指向与同页及相邻页的译文对照，并对疑似遗漏查看原页语境。初检得到下列 18 处候选；章节负责 Agent 已逐项查看原页，其中 15 处确有遗漏并已补入，3 处原稿已有引用。页码均指 PDF 物理页。

| PDF 页 | 原书页边指向 | 译稿定位 | 对应语境 |
| ---: | --- | --- | --- |
| 113 | Section 3.5 | `chapters/chapter-03.md`，`pdf-page: 113` | 后文详细讨论直方图方法 |
| 164 | Section 2.1.1 | `chapters/chapter-05.md`，`pdf-page: 164` | 癌症筛查示例与类别先验 |
| 165 | Section 11.2 | `chapters/chapter-05.md`，`pdf-page: 165` | 条件独立假设 |
| 166 | Section 11.2.3、Section 2.1.1 | `chapters/chapter-05.md`，`pdf-page: 166` | 朴素贝叶斯与筛查错误类型 |
| 175 | Section 11.2.3 | `chapters/chapter-05.md`，`pdf-page: 175` | 再次采用朴素贝叶斯假设 |
| 179 | Section 4.1.3、Chapter 7 | `chapters/chapter-05.md`，`pdf-page: 179` | 回归误差函数梯度与随机梯度下降 |
| 180 | Section 5.3 | `chapters/chapter-05.md`，`pdf-page: 180` | 多类逻辑回归与 softmax |
| 212 | Chapter 4、Chapter 5 | `chapters/chapter-06.md`，`pdf-page: 212` | 前文回归、分类误差函数 |
| 322 | Chapter 8 | `chapters/chapter-10.md`，`pdf-page: 322` | 通过反向传播计算输入图像梯度 |
| 425 | Chapter 12 | `chapters/chapter-13.md`，`pdf-page: 425` | 图神经网络与 Transformer 的表示学习类比 |
| 429 | Section 10.2 | `chapters/chapter-13.md`，`pdf-page: 429` | 卷积网络局部滤波器 |
| 476 | Section 15.3 | `chapters/chapter-15.md`，`pdf-page: 476` | K 均值迭代与后文 EM 算法 |
| 516 | Section 15.1 | `chapters/chapter-16.md`，`pdf-page: 516` | Old Faithful 数据的 K 均值预处理 |
| 520 | Section 16.3.2 | `chapters/chapter-16.md`，`pdf-page: 520` | 概率 PCA 模型的 EM 求解 |
| 563 | Appendix A | `chapters/chapter-18.md`，`pdf-page: 563` | 下三角雅可比矩阵的行列式 |

修订记录见 `reviews/global-crossrefs-early.md` 与 `reviews/global-crossrefs-late.md`。PDF 第 212 页 `Chapter 4` 与 `Chapter 5` 原已合写为“第 4、5 章”；第 520 页 `Section 16.3.2` 原已写在列表第二项，初检程序未展开 `list.items` 而误报。其余 15 处均已在相应译稿句内补入，并在重建的 JSON 中逐项复验：第 3 章 p29-b011；第 5 章 p15-b006、p16-b004、p17-b002/b005、p26-b008、p30-b009/b010、p31-b003；第 10 章 p20-b006；第 13 章 p03-b007、p07-b005；第 15 章 p02-b007；第 16 章 p08-b010；第 18 章 p05-b002。第 3、15 章的两个段落从前一 PDF 页延续，故 JSON 块的 `pdfPage` 是段落起始页。

PDF 第 291 页的 `Section 7.4.2` 与第 582 页的 `Section 15.2` 也分别以“见第 7.4.2 和 7.2.5 节”“见第 15.2、16.2 节”保留，属于多个节号共用“节”的正常写法。PDF 第 611 页的 `Chapter 12` 曾遗漏，已在第 20 章文本引导扩散模型段补为“见第 12 章”，重建 JSON 的 p21-b004 复验通过。以上边注所指章节或节号在全书目录中均存在。**G1 已通过修订复验。**

## 已通过的全书结构核对

- 28 个阅读单元按 PDF 顺序覆盖物理页 1–656，每个单元内部的页码连续；共 6,625 个顶层阅读块、328 个图像引用。JSON 中没有重复阅读块 ID、失效的目录锚点或不存在的图片文件。
- 正文第 1–20 章和附录 A–C 的带编号公式从各自 `(章号.1)` 连续到末项；全文公式、图、表、算法及节的文本引用所指编号均存在。重新运行 `python scripts/qa_bishop_chapters.py`，PDF 文本层与 JSON 的标签数量对照通过；这一自动结果不能替代原页目视审查。
- 原书目录 407 条在 `contents.json` 中保留原顺序、三级层级与印刷页码；将各章、附录的编号标题与目录逐项对照，译名一致。站点目录有 28 个全书单元，顺序为封面、前言、原书目录、第 1–20 章、附录 A–C、参考文献、索引。
- 术语抽样与当前术语表一致：正文使用“归一化流”“证据下界”“潜变量”“变分自编码器”“极大似然”“KL 散度”；未见“正规化流”“变分自动编码器”“最大似然”等同义混用。第 11、14 章个别“隐变量”对应原书的 *hidden variable* 语境，不能仅凭字面视为潜变量译名不一致。20 章均有单独标识的简短导读。

## 站点与发布链路复验

- 在模拟 GitHub Pages 项目子路径 `/intelligence-library/` 的本地 HTTP 服务下，独立用 Chromium 打开全部 28 单元；320 px 深色模式均无脚本错误或整页横向溢出，图像未报加载错误。补入交叉引用后的第 3、5、10、13、15、16、18、20 章又定向复验一遍，结果相同。目视检查了原书目录、算法 20.1 和索引的 320 px 页面；目录层级、代码、粗体索引页码可读。第 20 章 → 附录 A → 第 20 章导航正常，进度按本书的 localStorage 键保存并恢复。
- `books.js` 接入 28 个 JSON，`sw.js` 预缓存这 28 个正文文件；Pages 工作流暂存 `chapter-*.json`、七种前后材料 JSON、图片资源，并以提交 SHA 替换缓存版本标记。相对资源路径在上述项目子路径下可用。此检查是本地部署结构验证，GitHub Pages 线上发布状态仍需在发布后核实。
- PWA 图片采用按访问缓存：在干净浏览器中，图 20.9 首次离线请求失败；联机获取后进入 CacheStorage，随后离线返回 200。新版本 Service Worker 已将图片移入独立持久缓存；独立模拟旧版缓存迁移后，旧缓存中的图 20.9 在新版本激活、切换离线后仍返回 200。**未联机看过的图片，首次离线阅读仍不可用**，属于当前策略的明确边界。
- 全书交叉引用的文字编号及目标均保留，但 Bishop JSON 正文没有内部 `ref` 链接段，正文“见第 X 章／节／图／式”目前只能阅读，不能点按跳转。这是阅读体验改进项；若以后加链接，应将跨单元 URL 与单元内锚点一起生成，并保持原有编号可读。

## 当前结论

全书结构、术语抽样、编号目标、目录、页边交叉引用、移动端、深色模式、章节导航、阅读进度、离线正文、图片缓存迁移及 Pages 项目子路径检查已通过。**本地全书整体审查通过。** 未联机看过的图片不能首次离线打开，正文交叉引用目前不可点击；这两点已在上文记录为当前阅读策略的边界与改进项。实际 GitHub Pages 发布结果需由集成端另行检查。
