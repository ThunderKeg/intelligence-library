# 索引链接代码独立审查

审查者：`prml_translate_a`。范围：`tools/index_links.py` 及 `tools/build.py` 的索引富文本和调用入口；只读审查共享实现，仅新增本报告。

## 原页与调用路径

- 实际查看 PDF 749–758 全部 10 页的 5 张双页原图，核对原书主条、缩进子条、无页码父条、参见目标、同时带参见与页码的条目、罗马页码、跨栏续行及粗体／斜体。
- 读取 `build.py` 的 `index-entry` / `index-subentry` 富文本分支以及组装后调用 `link_index` 的入口；读取站点富文本渲染、块 ID 与 URL/hash 恢复逻辑。
- 索引页码保持原印文字；正文阿拉伯页码映射为 PDF 物理页加 20，`vii` 映射为前言 PDF 7。块级 `continuedPdfPages` 可定位跨页续段。

## 发现与修复复核

### IL-01：页码／参见数量约束拒绝原书合法结构（已解决）

旧实现要求 `len(spans) + len(see_spans) == 1`，实际原书有两种反例：

- PDF 750 的 `covariance matrix` 是无独立页码的父条目，下接 diagonal / isotropic / partitioned / positive definite 子条；旧检查计数为 0 并报错。
- PDF 757 的 `statistical learning theory` 同时含 `see computational learning theory` 和 `326, 344` 页码；旧检查计数为 2 并报错。

两例均用内存条目复现过 `ValueError`。集成者修复后，主条存在 `::` 子键时允许不带页码，且允许一个参见目标与一个页码列表并存；无目标叶条仍被拒绝。复核通过，没有要求作者补造原书未印的页码。

## 修复后验证

以内存中的条目调用当前 `link_index`，共 9 项通过：

| 检查 | 结果 |
| --- | --- |
| 无页码 covariance matrix 父条及 diagonal 子条 | 父条文字保留，子条 84 正确链接到 PDF 104 的内容 |
| statistical learning theory 同时带 see 与 326, 344 | 参见目标与两个页码均生成链接 |
| 1-of-K 的 K 斜体、424 粗体，Bayesian analysis 的 vii / 9 / 21 | 所有可见文字、em 与 strong 文本守恒；阿拉伯／罗马映射正确 |
| GEM 参见 expectation maximization::generalized | 正确指向索引子条块，显示文字不变 |
| 无页码、无参见且无子条的叶条 | 正确拒绝 |
| 同条重复页码列表 | 正确拒绝 |
| 重复英文键 | 正确拒绝 |
| 不存在的参见目标 | 正确拒绝 |
| 不完整罗马页码 v | 正确拒绝 |

- 正向病例同时比较链接前后整段文字、各个 strong 文本和各个 em 文本，全部相同。
- 页码 424 映射到 `chapter-09 / p01-b005`，页码 9 映射到 `chapter-01 / p08-b006`，均覆盖原页跨页续段；`vii` 映射到 `preface / p01-b001`。
- 测试时参考文献尚未完成整章构建，因此只在当前 Python 进程中将缺失的 `references.json` 读取替换为空块集合；所测页码均来自已有的正文／前言 JSON。屏蔽报告写入，未生成或修改共享导航报告、章节 JSON、工具或译稿。
- 验证范围为内存中的入口函数；完整索引构建、所有实际条目与浏览器跳转待索引译稿集成后检查。此次审查没有剩余待修代码项。

## 复核版本

- `tools/index_links.py` raw SHA-256：`bc341e0c1a2a25be59d261c11f729c2bd4d1341d4d5b2f5ac16852d05d0e29f9`。
- `tools/build.py` raw SHA-256：`9ffe5dd6ced9cd6f321a1e5cbb0a305ce5576c46558c0b399c232a8152ceafab`。
