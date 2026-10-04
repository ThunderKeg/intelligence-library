# 索引 b 分片独立审查

状态：**最终通过，可绑定当前索引验收。** 本 reviewer 未参与初译，完成 PDF 753–758 全部 477 项独审、全索引 793 项 JSON 守恒和 IB-01 最终两种视口复核；a 的 316 项与原 56 张网页证据采用 root 的独立审查结果，并验证其最终快照及证据指纹。无遗留问题。只修改本记录与个人临时证据，不编辑作者源稿、生成 JSON 或共享文件。

- [x] 实际逐页查看 PDF 753–758，核对全部主条/子条、中文义项、英文顺序及页码。
- [x] 核对全部粗体页码、变量斜体和“参见”的目标。
- [x] 核对 752/753 分片接口、同页跨栏续项和 758 末页。
- [x] 登记问题并在作者稳定修复后逐项复核；IB-01 源稿、生成 JSON 和双视口增量均通过。
- [x] 核对最终作者版本与 root 的 a 独审快照，完成全索引 JSON 守恒。
- [x] 静态核验全部页码/参见链接目标，并结合 root 的实际导航与网页审查完成最终验收。

## 逐页进度

| PDF 物理页 | 状态 |
|---|---|
| 753 | 85 项已逐项核对，暂无问题 |
| 754 | 90 项已逐项核对，暂无问题 |
| 755 | 88 项已逐项核对，暂无问题 |
| 756 | 88 项已逐项核对，probability 跨栏子项归属正确 |
| 757 | 86 项已逐项核对，Student t 正体与 see+页码完整 |
| 758 | 40 项已逐项核对，IB-01 全部修复通过；右栏为空但全页不为空 |

## 问题台账

| 编号 | 位置与发现 | 限定修复与复核 | 状态 |
|---|---|---|---|
| IB-01 | PDF 758，`translation/parts/index-b.md:458`，undetermined multiplier 的中文“待定乘子”与附录 E 定义及解释两处“未定乘子”不一致。 | 仅“待定乘子”→“未定乘子”；本人反向替换后字节完全恢复 a5f0ad… 原已审稿，英文/key/see/页码/标签均不变。最终 JSON 同步；本人实际查看双视口增量截图，词条和参见完整。 | 已关闭 |

## 原页与首批记录

实际逐张打开 753–758 全部六张源页及 752 分片接口，查看指纹见 `tmp/prml-review/index/source-pages-viewed.json`。753–755 的稳定译文共 263 项已按左栏→右栏逐条核对，原英文顺序、译义、全部页码、粗体页码、变量斜体、层级及参见语义暂无发现。保留 independent identically distributed 与 independent, identically distributed、outlier 与 outliers 等不同原词条，不把源书重复义项合并。

从 PDF 坐标独立识别主条/缩进子条/更深的折行接续，与稳定译文逐项比较英文及页码的字母数字顺序、粗体数字、层级；首批前三页全部相等，最终已扩展至全部六页并再次通过。结果只是逐项人工原页检查的补充。复查工具 `tmp/prml-review/index/compare_source_entries.py`，结果 `source-entry-comparison.json`。

原页特别核实：753 的 IRLS 和右栏首条都为 iterative reweighted least squares；K 近邻/K-means/K-medoids 的 K 为斜体，755 ν-SVM 的 ν 为斜体。754 machine learning 与 755 pattern recognition 指向罗马页 vii；755 的 normal distribution 参见 Gaussian，按原词保留。752 末 homogeneous Markov chain 已完整结束，753 首 Hooke’s law 是新条，不作跨页合并。

后三页的源页边界已登记并在最终稿逐项核实：756 probability 的 sum rule/theory 子项续到右栏；757 statistical learning theory 同时有参见 computational learning theory 和页码 326、344；758 右栏为空，左栏 40 项至 Yellowstone National Park，整页不为空。

## 后三页完整核对及最终 b 版本

恢复工作后重新打开 756–758 原页，与作者最终稳定译稿逐项对照剩余 214 项，未重复审已经完成的前三页。前三页与当前文件的差异也已比对：753/754 无变化，755 只多一个页尾空行，没有未核译文修改。后续三页的所有中文义项、原英文键、页码与粗体、变量字体、主子项层级及 see 的原对象均逐项核完。全部 477 项的辅助英文/数字顺序、粗体页码和原 PDF 缩进比较零差异；辅助脚本和记录已按全稿重跑。

756 的 PCA 五个子项、prior 四个子项和 probability 九个子项没有错挂或漏项；sum rule/theory 从左栏父项延续至右栏仍是子项。757 的 statistical learning theory 保留完整 see 对象和 326、344 两页码；SMO 与 tangent propagation 沿正文采用“序贯最小优化/切向传播”。758 的变分推断三子项、weight sharing 的 soft 子项和末项 110/粗体 681 全部保留。原印 protected conjugate gradients 与 Shur complement 按原文保留，未用惯常拼写擅改。

额外实际查看 `tmp/prml-source/b-index-student.png` 的放大原页，Student’s t-distribution 中的 t 确为正体；最终稿不再添加斜体，页码 102 仍为粗体。该字体保真不同于正文数学变量采用斜体的约定。

IB-01 后 b 原始字节及 LF SHA-256 均为 `f41a736308eefaa258d0624c66f816ab66a08186a0cd26195d58e33d616e5df8`；已审快照 `tmp/prml-review/index/reviewed-b-final.md`，前稿与单字差异证据在同目录 `reviewed-b-before-IB01.md` / `IB01-diff.json`。b 源稿没有遗留内容问题。

## 整索引 JSON 与链接守恒

独立执行 `tmp/prml-review/index/verify_integration.py`，当前 a 与 root 已审快照逐字节相等，b 与本人的最终已审快照逐字节相等。两分片的 316+477 条按原顺序与合并源稿、JSON 的 793 个 rich 块逐项比较；仅解除构建器添加的链接包装并规范空白后，全部 HTML 相等，包括中文、英文、标点、key、层级、em/strong 和全部页码。总计 795 根块为标题、原索引说明及 793 条词条；主条 679、子条 114、粗体页码 176，无数学或图片。原说明中的“粗体”仍用粗体强调。

全部 1,020 个页码链接已静态逐一核验：目标书、单元、块存在，显示原页码对应物理页（阿拉伯页码加 20；vii 对应物理页 7），目标块的 pdfPage 或 continuedPdfPages 包含该页。全部 77 个参见链接的目标 key 和块也逐一相符。页码分布至 20 个目标单元。完整证据为 `integration-verification.json`、`all-793-entry-content-and-format.json` 与 `all-static-link-targets.json`，均位于 `tmp/prml-review/index/`。

## 网页与交互证据

已阅读 `reviews/index-a-review.md`、`index-ui-review.md`、`index-navigation-qa.json` 和 IB-01 增量报告。root 实际查看的原 56 个文件版本由 `tmp/prml-root-review/index/viewed-ui-history.json` 记录；本人重新计算全部 56 个文件 SHA，均与查看记录一致，校验结果见 `tmp/prml-review/index/root-ui-proof-verified.json`。这些截图由 root 实际查看，本人没有将其计作自己的逐张目视。

root 的 194 次真实跳转为两模式各 77 条参见逐条点击和 20 个目的单元各一个页码样例；不声称 1,020 个页码都经过实际点击。该交互证据与本人的全部静态目标核验互补。原双模式证据同时覆盖首尾、索引层级、窄屏换行、无页级横向溢出和末块阅读进度恢复。

IB-01 仅改变一个中文字符，root 的 `index-ib01-qa.json` 证明反向恢复该字后 source/render/image 与原 56 图所绑定版本完全相等，全部 1,097 个 href 未改变。本人已实际打开最终 `p10-b004-1440-light.png` 和 `p10-b004-390-dark.png`：未定乘子、英文、参见及链接均显示完整，窄屏换行正常。两张实际查看指纹见 `tmp/prml-review/index/IB01-ui-viewed.json`。本次共采用 root 原 56 文件版本及最终 2 文件版本，明确保留阶段边界。

## 最终绑定版本

| 项目 | SHA-256 |
|---|---|
| a 原始字节/LF | `eb4ab6ddd14985e25bcbf6b5ba45b6c2362b5cc0f7cb69faa0a74c585d755093` |
| b 原始字节/LF | `f41a736308eefaa258d0624c66f816ab66a08186a0cd26195d58e33d616e5df8` |
| 合并源稿原始字节 | `1e78916bb619e3360975e3f6c4678008804ce02b0c86957087c058a1c8ce862b` |
| 合并源稿 LF | `d5d87f058e2acdb1b44195a0f49903f16a8026e5d404bfb502a150df5f48b805` |
| renderedContentSha256 | `78a299e251219eb00848a0c53249795cd0e466c6307bb0e4457dc46ea5861a44` |
| imagesSha256（空集） | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

依据上述逐项内容、独立守恒和分工网页证据，当前完整索引可验收；此结论不提前覆盖尚待完成的全书最终目录与公共站点接入。
