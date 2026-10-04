# 索引术语定点独立复核（2026-10-04）

## `sum–product` 五处：定点 PASS

以仓库 MacKay 原书 PDF **物理页 632、637、638、640 的可视页**逐项核对：原书在 PDF632 的 `algorithm` 子项印 `sum–product, 336`，在 `belief propagation` 项印 `see message passing and sum–product algorithm`；PDF637 在 `message passing` 下印 `sum–product algorithm, 336`；PDF638 的 `probability propagation` 指向 `sum–product algorithm`；PDF640 主词条印 `sum–product algorithm, 187, 245, 326, **336**, 407, 434, 556, 572, 578`。现页稿分别为下列五项，英文原词、所在层级、页码和参见关系与原页一致。

| PDF 页 | 索引项锚点 | 修订后的中文术语 |
| --- | --- | --- |
| 632 | `idx-p632-e042` | `sum–product（和积算法）` |
| 632 | `idx-p632-e110` | `belief propagation（信念传播）` 的 `sum–product algorithm（和积算法）` 参见项 |
| 637 | `idx-p637-e077` | `sum–product algorithm（和积算法）` |
| 638 | `idx-p638-e159` | `probability propagation（概率传播）` 的 `sum–product algorithm（和积算法）` 参见项 |
| 640 | `idx-p640-e034` | `sum–product algorithm（和积算法）`；336 的粗体保留 |

第 16 章 PDF257 首次定义把 *sum–product algorithm* 译为“和积算法”；第 25、26、47 章正文和标题也持续使用“和积算法”。四章页稿未见旧称“求和—乘积”；`belief propagation` 的“信念传播”保持独立术语。

从旧审定快照 `mackay-index-before-global-terms.json`（SHA-256 `d5d5a66da51d5c7f625270cbc7a81e9661f0d2e0c00c6f6570ab59dcb52de6b4`，705,347 字节）独立逐字段比较到新草稿／正式 JSON（两者逐字节一致，SHA-256 `05d9dab91f2af1ad4b684bfdad2630617ba85ac3230a7f90a06ca1405016062c`，705,269 字节）：只有 `p632-b024`、`p632-b078`、`p637-b063`、`p638-b120`、`p640-b033` 五块的 `text`／`html` 共十个字符串字段发生预期中文替换。其他字段、英文原词、全部 1599 个索引项锚点和 2536 个链接 `href` 顺序完全不变；其中印刷页码链接 2435、`see` 链接 101。PDF640 粗体 336 与旧版一致。

五处术语修订本身通过独立原页与差异复核；随后 G-08 两处修订的复核见下节。

## G-08 两处 `Gibbs sampling`：定点 PASS

逐项目视核对原书 PDF 物理页 635、637：PDF635 的主词条为 `Gibbs sampling, **370**, 391, 418, see Monte Carlo methods`；PDF637 在 `Monte Carlo methods` 下列同名子项，页码为 **370**、391、418。现稿 `pdf-635.md:173` 和 `pdf-637.md:135` 均写为 `Gibbs sampling（Gibbs 采样）`，层级、英文原词、三个页码、粗体 370 与主词条参见关系均保留。正文第 29 章 §29.5 和第 43 章也使用“Gibbs 采样”，术语一致。

独立比较修订前快照 `mackay-index-before-gibbs.json`（SHA-256 `05d9dab91f2af1ad4b684bfdad2630617ba85ac3230a7f90a06ca1405016062c`）与当前草稿、正式 JSON：后二者逐字节一致，705,257 字节，SHA-256 `230ba57c067299b3d41c180da363925a3f7b657e2016b3a6ca52c21136c85bac`。仅 `p635-b099`（`idx-p635-e163`）和 `p637-b096`（`idx-p637-e125`）两块的 `text`／`html` 四个字符串字段将“吉布斯采样”改为“Gibbs 采样”；其余块及字段未变。全部 1599 个索引项锚点、2435 个印刷页码链接与 101 个参见链接保持原 ID、`href` 和顺序。

从最初审定快照 `d5d5a66d…52de6b4` 直接逐字段比较到当前最终版，差异也仅限上述五处 `sum–product` 与两处 `Gibbs sampling`，共七个块的 `text`／`html` 十四个字符串字段。**两组共七处术语修订的独立原页、正文术语和 JSON 结构复核通过；G-08 关闭。** 正式页面回归记录见 `SITE_QA.md`。
