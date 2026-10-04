# 全书一致性修订：b 分片作者记录

## 修订范围与依据

本次按 root 的全书审查分工，仅修改下列三个原有分片：

- translation/parts/chapter-05-b.md
- translation/parts/chapter-12-b.md
- translation/parts/chapter-13-b.md

另新增本记录；未改 a 分片、合并稿、章节 JSON、站点文件、术语表或任务清单。首轮正文修订时，索引 b 冻结于 a5f0ad7069cf825ae948f78dacf72764b741c7927d70bd0d095189b96c45081a；后续索引 IB-01 的独立修复与新指纹另记于 index-b-author.md。

修改前已检查 git status，逐个复制原字节快照至 tmp/prml-source/global-b-before/，并记录上述三章全部 31 张 b 图片的 SHA-256。修改前后均以原字节读写，保留各文件原有行结束符。

重新渲染并亲自查看 PDF 284、306、611、613、649、650、651 共七个原页，原页文件在 tmp/prml-source/global-b-before/page-NNN.png。所有修改只涉及术语与中文表达，不修改原书数学内容或对模型的判断。

## 逐处差异

| 文件与行号 | PDF 页 | 源文定位 | 修订 |
| --- | ---: | --- | --- |
| chapter-05-b.md:190 | 284 | 式 5.126 后 Jacobian matrix J | Jacobian 矩阵 → 雅可比矩阵；去除替换后不再需要的中英文间空格 |
| chapter-05-b.md:208 | 284 | 正则化函数通过 Jacobian J 依赖权重 | Jacobian 矩阵 → 雅可比矩阵 |
| chapter-05-b.md:928 | 306 | 习题 5.15 的 Jacobian matrix / Jacobian | 两处 Jacobian 矩阵 → 雅可比矩阵；保留前向传播、反向传播关系 |
| chapter-12-b.md:286 | 611 | ICA 段 a generative model | 考虑一个生成模型 → 考虑一个生成式模型 |
| chapter-12-b.md:316 | 613 | Such a network is said to form an autoassociative mapping | “这样的网络称为构成了 *自联想*（autoassociative）映射。”改为“这种网络形成的映射称为 *自联想*（autoassociative）映射。”；消除重复谓语，保留“映射”的命名关系 |
| chapter-13-b.md:9 | 649 | 展开 HMM 得到 lattice diagram，随后 through the lattice | 格架图、格架各一处 → 格图 |
| chapter-13-b.md:25 | 650 | 图 13.16 的 HMM lattice | alt 和图注各一处格架 → 格图；图片文件及图内译注未改 |
| chapter-13-b.md:61 | 651 | Viterbi 直观解释中的 lattice / lattice diagram | 三处格架、一处格架图 → 格图 |
| chapter-13-b.md:67 | 651 | generative models for the data | 作为数据生成模型 → 作为数据的生成式模型 |
| chapter-13-b.md:67 | 651 | using discriminative rather than maximum likelihood techniques | 使用判别方法 → 使用判别式方法；这处同段补字经 root 明确纳入范围，保留与最大似然方法的原对照 |

首轮合计九个源文件行发生变化，十个定位项。第 5 章共四处术语替换；第 12 章一处术语、一句中文修顺；第 13 章八处格图词形和两处生成式/判别式词形。其余文字保持原样。

第 13 章重新查看的 lattice 与图 13.16 均为同一种沿时间展开状态转移的图，故沿第 8 章首次译名“格图”统一。没有将其他普通“生成”动词机械替换成术语。第 12 章修句未把两层网络改称不同模型，也未把映射的名称移到网络本身。

## 守恒检查

| 检查 | 第 5 章 b | 第 12 章 b | 第 13 章 b |
| --- | --- | --- | --- |
| 全部行内/显示数学原串及顺序 | 502 段完全一致 | 375 段完全一致 | 447 段完全一致 |
| 页标、跨页接续标记 | 完全一致 | 完全一致 | 完全一致 |
| HTML 标签、类名、src 与其他属性 | 完全一致 | 完全一致 | 除图 13.16 alt 的“格架→格图”外完全一致 |
| 标题与习题编号/星数/www 标签 | 完全一致 | 完全一致 | 完全一致 |
| 所有 b 图片文件 | 全部一致 | 全部一致 | 全部一致 |

31 张图片的逐文件指纹已与修改前快照核对，全部相同。数学原串的比较同时涵盖编号式、未编号式、变量字体命令、上下标与式号。作者自检逐行查看了差异，未出现超出上述限定替换的编辑。

辅助检查证据：

- tmp/prml-source/global-b-before/changes.json：前后 raw/LF SHA、精确替换计数、数学与结构检查结果。
- 同目录 chapter-05-b.md.diff、chapter-12-b.md.diff、chapter-13-b.md.diff：相对于原字节快照的完整逐行差异。
- 同目录 assets-sha256.json：31 张图片的修改前指纹；已复算修改后指纹并逐一比较。

## 追加泰勒术语统一（2026-10-04）

a 分片作者在对本轮 b 增量做独立原页审查时指出，下列三处旧译的 Taylor 展开与本分片 PDF 286 和其他章“泰勒展开”不同。root 明确将三处纳入全书一致性修订，已限定修改并再次冻结：

| 文件与行号 | PDF 页 | 精确修订 |
| --- | ---: | --- |
| chapter-05-b.md:670 | 299 | 作 Taylor 级数展开 → 作泰勒级数展开 |
| chapter-05-b.md:922 | 306，习题 5.12 | 局部 Taylor 展开 → 局部泰勒展开 |
| chapter-05-b.md:926 | 306，习题 5.14 | 通过 Taylor 展开 → 通过泰勒展开 |

除这三处及相邻不再需要的中英文间空格外，其他字节保持不变；未改其他 Taylor 人名或引用。全部 502 个数学片段、HTML 标签/属性、页标和接续标记、标题、习题编号/星数/www 与行结束符逐项守恒，没有编辑图片或 JSON。

本次前稿 raw SHA-256：20c13285acff74d8da7c223607f622e57f377f13b08317219091d2219c005296。精确前稿与 diff 保存在 tmp/prml-contents-final-b/chapter-05-b-before-taylor.md、chapter-05-b-taylor.diff；此前 global-b-before 中首轮证据继续保留，不能单独代表这三处追加修订。下方最终指纹已更新。独立原页/语义及追加 UI 复查由未初译本分片的 prml_translate_a 负责，尚不以作者自检替代独审。

## 最终指纹

| 文件 | 修改前 raw SHA-256 | 修改后 raw SHA-256 |
| --- | --- | --- |
| chapter-05-b.md | 0e180b5b3a3af067ed87122f1fdafb479af91c01c8f9c728b55e5842037f96b8 | 3da532e4cf9af6630c7bc5ebd58fc2fbf0caeee3fa96104630cf9466d034ee83 |
| chapter-12-b.md | 857c83775ff6236a7ae63d3a0bf2f94e77772d059d560fdf49b1f60fdc803419 | 39b83ede15b9f95f5c795498606a353665017ad693474c945877be7726d631a2 |
| chapter-13-b.md | 67db5de3bf2994306905b5128a7923ae8fc3ef13f3c54d065e74c4ad58b4a52e | 25e2e5f64dde0146b2c4df720aaa18a34563aa2396bc847a4dcd379606b7dc29 |

修改后 LF 规范化 SHA-256：

- chapter-05-b.md：6c3243b591eb1b61678985154d670376a9d414ea028b8f1f9765f6f0b7e80b9f
- chapter-12-b.md：39b83ede15b9f95f5c795498606a353665017ad693474c945877be7726d631a2
- chapter-13-b.md：25e2e5f64dde0146b2c4df720aaa18a34563aa2396bc847a4dcd379606b7dc29

作者修订和自检完成，等待独立差异复核与 root 集成后的网页核验；不以本记录宣告全书验收。
