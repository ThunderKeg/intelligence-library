# 索引 a 作者自检记录

范围：PDF 物理页 749–752。仅负责本分片初译和作者自检，独立审查与整体链接验收由集成者另行登记。

## 任务清单

- [x] 检查 git status、文件所有权和最新术语规范。
- [x] 与 b 确认 752/753 为完整条目边界；GEM 使用 `expectation maximization::generalized` 子项键。
- [x] 实际查看并逐项翻译 PDF 749，核对原说明、主／子／参见、页码及强调。
- [x] 实际查看并逐项翻译 PDF 750，保留 covariance matrix 无页码父条。
- [x] 实际查看并逐项翻译 PDF 751，核对全部缩进子条及变量字形。
- [x] 实际查看并逐项翻译 PDF 752，核对 graphical model 跨栏子条。
- [x] 全部分片条目、页码、强弱字体、英文键与参见目标自检。
- [x] 构建器只读解析、逐项文字／强调守恒、最终 SHA-256 和作者交接。

## 格式与边界

- 仅本分片写“索引”标题与原书使用说明，不增加导读。
- 原书英文顺序、层级与原页码不变；题名用中文并保留英文对照，页码放在 `span.index-pages`，参见目标用 `data-index-see`，链接由集成者生成。
- 父／子键使用 `父::子`，无页码父条不虚构页码。
- 752 最后一条 homogeneous Markov chain 完整结束；b 的 753 从 Hooke’s law 开始，无跨分片 join。
- 根 Agent 的原页提取辅助给出 53 / 87 / 88 / 88 个条目候选，仅作定位，逐项以实际原页为准。

## 逐页核对结果

实际逐页查看 `tmp/prml-root-review/appendix-index/page-749.png` 至 `page-752.png`，按左栏后右栏顺序核完全部条目，再直接编写各条中文译名。排版脚本只将已写好的中文与逐项核对过的英文、页码及层级组合，不调用本机模型或翻译 API。

| PDF 页 | 条目 | 主条 | 子条 | 参见条目 | 原页码数 | 粗体页码数 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 749 | 53 | 50 | 3 | 6 | 77 | 17 |
| 750 | 87 | 81 | 6 | 7 | 110 | 20 |
| 751 | 88 | 80 | 8 | 6 | 109 | 19 |
| 752 | 88 | 53 | 35 | 4 | 118 | 17 |
| 合计 | 316 | 264 | 52 | 23 | 414 | 73 |

- 原书开头说明已完整翻译，“粗体”本身的加粗通过段内 strong 语义保留；未增导读。
- 750 的 covariance matrix 无页码父条完整保留，4 个子条仍归属该父条。
- 752 右栏首项 undirected 保持为 graphical model 的第 9 个子条，未提升为主条；Hessian 与 hidden Markov model 的全部子条均保留。
- 23 个参见目标采用稳定英文键，GEM 精确使用 `expectation maximization::generalized`。其中 von Mises distribution 与 mixture model 两个目标位于 b 分片，其余均存在于本分片。
- 414 个原页码保留原文本及顺序，包括罗马页码 vii；未将可见原页码替换为 PDF 物理页码。73 个粗体页码另外与原 PDF 的 Times-Bold 数字片段逐项比较，内容与顺序完全一致。
- 316 个英文键唯一；数字词条 1-of-K 与 C4.5 等不在 index-pages 内，不会作为页码处理。

## 字形、术语及源页细节

- 749 的 K、两处 α，751 的 K、两处 epsilon 保留原数学斜体；中文对照中出现的对应变量也用 em。源 PDF 的 epsilon 字体映射为 U+03F5 `ϵ`，原页提取辅助曾规范化成 `ε`；实际显示保留 `ϵ`，集成者已独立确认。
- 752 的 evidence ap- / proximation 为原行末拆字，接回 evidence approximation。没有改动原印术语或页码。
- 术语按正文核对：假定密度滤波、典范连接函数、链式连接、共父节点、经典概率、解释消除、特征图、正运动学、正问题、因子载荷、生成式模型、生成拓扑映射、乔赛亚·威拉德·吉布斯等。
- 与 b 协调 extensive variables 为“数量随数据集增长的变量”，与 intensive variables 的“数量固定的变量”配对；沿第 10 章实际解释，未引入不同含义的热力学术语。Gaussian 的 wrapped 子条用“缠绕”，与第 2 章及 b 的“缠绕分布”统一。
- 原索引不同英文别名保留各自条目，未按中文排序、合并或删除。

## 结构自检与稳定交接

- 仅通过 `render_chapter` 将 a 分片解析到临时目录，未写整章 JSON 或运行共享链接报告生成器。
- 解析结果为 318 块：1 个 H1、1 个原说明段、316 个 rich 条目；无新增章节、图像、公式、页间 join 或空白占位。
- 316 条的 key、HTML、全部文字及层级在源码与渲染结果间逐项相等；36 个 em 与 73 个页码 strong 均完整保留。原说明的“粗体”另作为 strong 段内语义保留。
- 从渲染条目重建英文内容，与原 PDF 各页字符顺序比较；统一空白、连字及 Unicode 规范形后，仅剩上述 evidence approximation 行末断词恢复差异。
- 逐条清单：`tmp/prml-indexa/entry-checklist.json`；逐页计数及粗体核对：`tmp/prml-indexa/page-checks.json`；结构 QA：`tmp/prml-indexa/qa-summary.json`；临时解析：`tmp/prml-indexa/rendered-part.json`。
- 最终源码 raw / LF SHA-256 均为：`eb4ab6ddd14985e25bcbf6b5ba45b6c2362b5cc0f7cb69faa0a74c585d755093`。
- 根 Agent 已反馈逐项核对 316 条当前稿未发现内容、页码、层级或强调问题。本记录为作者稳定分片交接；整章链接、浏览器交互和最终验收由集成者另行记录。
