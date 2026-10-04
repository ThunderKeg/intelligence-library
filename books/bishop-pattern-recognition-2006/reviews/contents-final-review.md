# 原书目录最终增量独立审查

审查人：prml_translate_b（未承担目录初译）。审查日期：2026-10-04。

**最终结论：通过。原书目录 285 项、实际 31 处题名对齐、285 个导航目标和两种显示模式均已独立核验；CF-01 已修复并关闭，无待修问题，可纳入本书最终验收。**

## 原页与内容核验

已通过 view_image 实际逐页查看仓库原 PDF 物理页 13–20，并逐项核对未链接目录及最终链接目录。原书目录共有 285 项。自动提取只用于已读原页的页码、字体、缩进和序号辅助复核，未将提取文本、候选列表或旧审查记录当作已核原文。

旧基线 reviews/frontmatter-review.md 已查阅；本次重新实际查看全部 8 原页。审查者只写本报告及自己的 tmp 证据，未编辑目录译稿、生成 JSON、其他正文或共享工具。

| PDF 物理页 | 条目数 | 实际逐项阅读范围 | 结果 |
| ---: | ---: | --- | --- |
| 13 | 23 | 前言、数学记号、目录、第 1 章全部标题与习题 | 原顺序、题意、层级、字重和页码完整 |
| 14 | 42 | 第 2、3 章全部标题与习题 | 原顺序、题意、层级、字重和页码完整 |
| 15 | 44 | 第 4 章及第 5 章至 5.4.3 | 原顺序、题意、层级、字重和页码完整 |
| 16 | 43 | 5.4.4 起、第 6、7 章及习题 | 原顺序、题意、层级、字重和页码完整 |
| 17 | 44 | 第 8、9 章及第 10 章至 10.2 | 原顺序、题意、层级、字重和页码完整 |
| 18 | 44 | 10.2.1 起、第 11 章及第 12 章至 12.1.4 | 原顺序、题意、层级、字重和页码完整 |
| 19 | 41 | 12.2 起、第 13、14 章与附录 A–C | 原顺序、题意、层级、字重和页码完整 |
| 20 | 4 | 附录 D/E、参考文献、索引 | 原顺序、题意、层级、字重和页码完整 |

全部条目的顺序和编号均保留；罗马页码 vii/xi/xiii 与所有阿拉伯页码对应原书。depth 0/1/2 分别为 24/82/179；24 个顶层标题 strong=true，另外 261 项 strong=false。原书第 7 章习题的页码 357 也已保留。最终前后守恒检查逐项通过，目录没有新增、缺失或重复项。

## 31 处实际题名对齐的语义复核

仅以下 31 项中文题名变化；其余 254 项题名未变。已将每项与实际阅读的原 PDF 英文题名及目标正文标题比对，均未改变原题所指。下表列的是最终文件的实际差异，不沿用早期 34/32 项候选数。

| 项次 / 原目录 PDF 页 | 英文原题 | 对齐前 → 最终题名 | 原印页码 | 独立语义结论 |
| --- | --- | --- | --- | --- |
| 26 / 14 | 2.1.1 The beta distribution | 2.1.1 贝塔分布 → 2.1.1 Beta 分布 | 71 | 保留 Beta 原词，所指分布未变。 |
| 44 / 14 | 2.5.1 Kernel density estimators | 2.5.1 核密度估计器 → 2.5.1 核密度估计 | 122 | 按方法标题译作“核密度估计”，仍指本节的估计方法。 |
| 45 / 14 | 2.5.2 Nearest-neighbour methods | 2.5.2 最近邻方法 → 2.5.2 近邻方法 | 124 | “近邻方法”与正文标题一致，保留近邻分类/估计方法的所指。 |
| 58 / 14 | 3.3.3 Equivalent kernel | 3.3.3 等价核 → 3.3.3 等效核 | 159 | 等效核与正文和全书术语统一。 |
| 61 / 14 | 3.5.1 Evaluation of the evidence function | 3.5.1 证据函数的计算 → 3.5.1 计算证据函数 | 166 | 名词性题名改为动宾表达，计算证据函数的含义相同。 |
| 62 / 14 | 3.5.2 Maximizing the evidence function | 3.5.2 证据函数的最大化 → 3.5.2 最大化证据函数 | 168 | 名词性题名改为动宾表达，最大化证据函数的含义相同。 |
| 63 / 14 | 3.5.3 Effective number of parameters | 3.5.3 参数的有效个数 → 3.5.3 参数的有效数目 | 170 | “有效数目”对应 effective number，语义相同。 |
| 64 / 14 | 3.6 Limitations of Fixed Basis Functions | 3.6 固定基函数的局限 → 3.6 固定基函数的局限性 | 172 | 补“性”使中文题名自然，仍为固定基函数的局限。 |
| 68 / 15 | 4.1.1 Two classes | 4.1.1 两个类别 → 4.1.1 二分类 | 181 | 二分类准确对应两个类别的情形。 |
| 69 / 15 | 4.1.2 Multiple classes | 4.1.2 多个类别 → 4.1.2 多分类 | 182 | 多分类准确对应多个类别的情形。 |
| 73 / 15 | 4.1.6 Fisher’s discriminant for multiple classes | 4.1.6 多类别 Fisher 判别 → 4.1.6 多分类的 Fisher 判别 | 191 | 多分类保留 multiple classes 的所指及 Fisher 判别方法。 |
| 103 / 15 | 5.3.2 A simple example | 5.3.2 一个简单示例 → 5.3.2 一个简单例子 | 245 | “示例/例子”同义，简单示例范围未变。 |
| 109 / 15 | 5.4.3 Inverse Hessian | 5.4.3 Hessian 逆矩阵 → 5.4.3 Hessian 矩阵的逆 | 252 | 明确为 Hessian 矩阵的逆，未改变数学所指。 |
| 129 / 16 | 6.2 Constructing Kernels | 6.2 构造核 → 6.2 核的构造 | 294 | “构造核/核的构造”语义相同。 |
| 133 / 16 | 6.4.1 Linear regression revisited | 6.4.1 再谈线性回归 → 6.4.1 重新考察线性回归 | 304 | “重新考察”对应 revisited，保留回顾线性回归的含义。 |
| 143 / 16 | 7.1.1 Overlapping class distributions | 7.1.1 相互重叠的类别分布 → 7.1.1 类别分布重叠 | 331 | 仍指类别的分布相互重叠。 |
| 145 / 16 | 7.1.3 Multiclass SVMs | 7.1.3 多类别 SVM → 7.1.3 多类 SVM | 338 | 多类 SVM 与 multiclass SVMs 对应。 |
| 160 / 17 | 8.2.1 Three example graphs | 8.2.1 三个图示例 → 8.2.1 三个图的例子 | 373 | 仍是三个用作示例的图。 |
| 161 / 17 | 8.2.2 D-separation | 8.2.2 D 分离 → 8.2.2 d 分离 | 378 | d 大小写与正文术语一致，未改变 d 分离概念。 |
| 174 / 17 | 8.4.7 Loopy belief propagation | 8.4.7 有环置信传播 → 8.4.7 有环信念传播 | 417 | “信念传播”与全书术语一致，保留 loopy 的“有环”。 |
| 183 / 17 | 9.3 An Alternative View of EM | 9.3 EM 的另一种解释 → 9.3 从另一角度看 EM | 439 | “从另一角度看”忠实表达 alternative view。 |
| 184 / 17 | 9.3.1 Gaussian mixtures revisited | 9.3.1 再谈高斯混合 → 9.3.1 再论高斯混合 | 441 | “再论”保留 revisited 的重新考察含义。 |
| 187 / 17 | 9.3.4 EM for Bayesian linear regression | 9.3.4 贝叶斯线性回归的 EM 算法 → 9.3.4 用于贝叶斯线性回归的 EM | 448 | 保留 EM 用于贝叶斯线性回归的关系。 |
| 188 / 17 | 9.4 The EM Algorithm in General | 9.4 一般形式的 EM 算法 → 9.4 一般的 EM 算法 | 450 | “一般的 EM 算法”保留 in general 的范围。 |
| 196 / 17 | 10.2 Illustration: Variational Mixture of Gaussians | 10.2 示例：变分高斯混合 → 10.2 示例：高斯混合的变分推断 | 474 | 明确为高斯混合的变分推断，保留 illustration 和 variational 的含义。 |
| 200 / 18 | 10.2.4 Determining the number of components | 10.2.4 确定分量个数 → 10.2.4 确定分量数 | 483 | “分量数”与 number of components 对应。 |
| 201 / 18 | 10.2.5 Induced factorizations | 10.2.5 诱导出的因子分解 → 10.2.5 诱导的因子化 | 485 | “因子化”与本章正文一致，保留 induced 的含义。 |
| 223 / 18 | 11.1.5 Sampling-importance-resampling | 11.1.5 采样—重要性—重采样 → 11.1.5 采样重要性重采样 | 534 | 三项名称及顺序完整，中文标题去除连接破折号未改变方法。 |
| 255 / 19 | 13.2.1 Maximum likelihood for the HMM | 13.2.1 HMM 的最大似然估计 → 13.2.1 HMM 的最大似然 | 615 | 保留 HMM 和 maximum likelihood 的所指。 |
| 270 / 19 | 14.3 Boosting | 14.3 提升方法 → 14.3 提升 | 657 | 提升与 boosting 的已定义术语对应。 |
| 272 / 19 | 14.3.2 Error functions for boosting | 14.3.2 提升方法的误差函数 → 14.3.2 提升的误差函数 | 661 | 保留 error functions 与 boosting 的从属关系。 |

## 285 个目标与结构复核

独立脚本 audit_final.py 从最终 Markdown 与实际生成的单元 JSON 重新读取全部目录行，不以 link_contents.py 的成功结果代替检查。逐条验证：链接的 book、单元与块 ID 存在且唯一；目标块是相应 heading；章节号、实际标题、H1/H2/H3 层级和 PDF 页与原印页码对应。三个前置单元分别对应 PDF 7/11/13，其余目标对应原印页码加 20。285 条全部通过，285 个链接互异。

最终内容为 9 个块（1 个标题与 8 个原页目录列表），图片列表为空。对齐前后每项的目录原页、印刷页码、顺序、depth 与 strong 完全守恒。独立结果还与 root 的 contents-navigation-build.json 逐行比对：285 个目标和 31 处题名变化均一致。所有目标 JSON 的核验时原始 SHA 记录在 final-target-audit.json 中。

## 最终网页实际检查与 CF-01 关闭

独立运行 qa_targets.py 的私有证据包装器，报告和图片仅写 tmp/prml-contents-final-b；每次滚动后等待两个绘制帧与 250 ms，避免将尚未完成绘制的瞬间当作页面内容。实际逐张查看所有输出：1440×1000 浅色目录 20 张、390×844 深色目录 22 张，覆盖全部 9 块及长列表连续截图；另外实际查看两模式各 5 次点击落点截图，共 10 张。总计 52 张均已通过 view_image 查看，没有把截图生成成功当作目视通过。

目录长标题可以换行，三层缩进与右侧页码保持清楚；未见文字相互遮挡、横向页面溢出、链接丢失、深色不可读或错位。逐模式 DOM 辅检确认全部 285 项的可见文字、页码、链接、层级与 strong 与最终 JSON 一致；两模式均无脚本错误。

| ID | 级别与位置 | 原问题 | 最终修复及独立复核 | 状态 |
| --- | --- | --- | --- | --- |
| CF-01 | P3，24 个顶层目录行的右侧页码 | 原 PDF 的顶层标题和页码均加粗；初审时网页仅标题加粗，页码为普通 span。 | root 增加仅 PRML 生效的 strong.contents-title + .contents-page 样式。实际查看两模式所有目录截图，24 个顶层标题与页码均有对应强调；DOM 的 24 个页码 font-weight=700，另外 261 个为 400，原层级/strong 结构未改。 | 已关闭 |

代表性实际点击选择前置单元、两处已对齐小节、附录和索引；每项在两种模式各点击一次，均到达对应可见标题，URL 的单元和 read- 块锚点正确：

| 目录项次 | 最终题名 | 实际目标 | 模式与结果 |
| ---: | --- | --- | --- |
| 1 | 前言 | preface / p01-b001 | 1440 浅色、390 深色均通过 |
| 58 | 3.3.3 等效核 | chapter-03 / p23-b002 | 1440 浅色、390 深色均通过 |
| 161 | 8.2.2 d 分离 | chapter-08 / p20-b004 | 1440 浅色、390 深色均通过 |
| 279 | 附录 A 数据集 | appendix-a / p01-b001 | 1440 浅色、390 深色均通过 |
| 285 | 索引 | index / p01-b001 | 1440 浅色、390 深色均通过 |

这 10 次点击是本审查者实际执行并查看的代表性导航验证；全部 285 条的目标存在性与页码/标题/层级已另行全量核验。root 另做的 48 次导航测试不计入本报告的独立点击数量。本报告确认目录增量，不以这些目标截图替代全书正文各章的原页语义审查。

## 冻结版本与证据

| 对象 | 指纹类型 | SHA-256 |
| --- | --- | --- |
| 原书 PDF | raw | `4ee767e0a6b04fa05ba7e599e9dbb4637a94a4407ccedf0b4d316b1fd7c8ec64` |
| translation/contents.md | raw | `eaae16bdd37d751a3abf45711198cd1e579f22672b9a3a5e2025f894f4be7f84` |
| translation/contents.md | LF 归一化 | `027afd298316f481f33b48319ed73f5fbc43e7e999e3cb95c505a0bfbeebc615` |
| contents.json | raw | `a8707101a7e6c4d41fd716dd62b4f7a73eb46f495303f61af857073fbb6daee6` |
| contents.json 内容（排除验收元数据） | renderedContentSha256 | `486fa7a99e3c94dcf3b8685edcf30e2717c6a18554e07a09db33b03ad19c722a` |
| 空图片列表 | imagesSha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

下列所有路径均相对于仓库。source-audit.json 中 finalLinksReviewed=false 是链接生成前的历史基线；最终链接、31 项人工语义检查和网页目视结果以 final-target-audit.json 及本报告为准，其中两个 manual 标记均已在实际完成后设为 true。

| 辅助文件 | raw SHA-256 |
| --- | --- |
| tmp/prml-contents-final-b/contents-before.md | `4e809908d0440db7435aa5deb6f88c9d4e3a37b94eceba572162a14e54cb382e` |
| tmp/prml-contents-final-b/contents-json-before.json | `df2d9ea963c01eb3b55fa7ab0242928886e03f2a387405c1f69833a9836d4378` |
| tmp/prml-contents-final-b/source-audit.json | `dd8d0a53571532e08fcfbe4d9258a48e8caf6b6d4edd58b0b934d3b2ac6e240d` |
| tmp/prml-contents-final-b/audit_source.py | `10ca40b0efda70b2ed2abf0a2aaf2ab8d644932d51a20edf8e9b50294d1244f5` |
| tmp/prml-contents-final-b/audit_final.py | `8abdd523a987abfc700cf5c92e79455ad1d9eeeb02243fd451fc3fcb7dec7cd4` |
| tmp/prml-contents-final-b/audit_navigation.py | `907065282b5b9ce8a38b2bd5ddf244a828b15dc34fefd5c705dafcfa2f5dff1d` |
| tmp/prml-contents-final-b/run_targets.py | `419bc5b7260b75c0637e87e67fe257d259fff0f4c8d3decc92b9527a1f92a1cd` |
| tmp/prml-contents-final-b/finalize_review.py | `70d036954071f918ecf0b0c8da397f253c66ebe92a131656c79e4aa063033eeb` |
| tmp/prml-contents-final-b/contents-final-source.md | `eaae16bdd37d751a3abf45711198cd1e579f22672b9a3a5e2025f894f4be7f84` |
| tmp/prml-contents-final-b/contents-final-json.json | `a8707101a7e6c4d41fd716dd62b4f7a73eb46f495303f61af857073fbb6daee6` |
| tmp/prml-contents-final-b/final-target-audit.json | `571e9376720e2ec25680036470b23f002b9d9432159a6365ab60519a4a3a61e0` |
| tmp/prml-contents-final-b/navigation-audit.json | `4a26af83e3bb28e081b33c052985b8d38fd758550ba3ee9e6a5ef2cc3c7bf6d3` |
| tmp/prml-contents-final-b/ui-all/reader-qa-contents-targets-contents-final-b.json | `45aaed802f9acb65f5d1025af65607fa123142e48b9e3f60969310032fdfcd88` |
| tmp/prml-contents-final-b/actual-view-manifest.json | `9835bae5f9f57de26432b9b0f16363d01d7e13bae5eda64b24887e3937155b69` |
| books/bishop-pattern-recognition-2006/reviews/contents-navigation-build.json | `0a4bb2d425a9a57f09d32ea1068b2c52fb1ef8ba1ab65c88bc1cbc609078671d` |
| tmp/prml-contents-final-b/pdf-013.png | `96e7822d3f2c8d6034e5e736adfae61fae9fab87f77bae0cf8f1d6cc476214a3` |
| tmp/prml-contents-final-b/pdf-014.png | `50b21d5b7d2e8b83c119da1f5cd9ea2e52d5006e830244b16440e45926b89dd8` |
| tmp/prml-contents-final-b/pdf-015.png | `3dc86924552d43712af8a4849a5dee70f9fd18ed5f96ad5e23c9ac9cb9610347` |
| tmp/prml-contents-final-b/pdf-016.png | `1a2507418a8fa9d9be7da6d1903476a3735d5e970bed5519f71a2188e67c7bbe` |
| tmp/prml-contents-final-b/pdf-017.png | `2d31ad8225fac025ff08a1e25f6f65f963c5b362757b3593a97d0ad42f440682` |
| tmp/prml-contents-final-b/pdf-018.png | `09dd21aef52eaf933f4a21c0abb87afbf6f3a959fd0834d9b43db9d07e8dddb7` |
| tmp/prml-contents-final-b/pdf-019.png | `5ff50f978f32b7b3ef4d86816c51af318676a26d53b9aacfc644bd650d85c504` |
| tmp/prml-contents-final-b/pdf-020.png | `167d593512d96a68b54f20658d6ed18211c56743c93cc221805e3298d4ce55fe` |

## 已实际查看的 52 张最终网页图片

全部条目均已实际查看且结果通过；manifest 同时保存模式、类型与逐文件 SHA。

| 路径（相对于 tmp/prml-contents-final-b） | raw SHA-256 |
| --- | --- |
| ui-all/p01-b001-1440-light.png | `3eea97db676d966a9be5d677dcee4bbfeb3a6975b472cc11dbdbf2df0d56bbed` |
| ui-all/p01-b001-390-dark.png | `a7f0e2c16d22aab05b8c585cc31482404e32e1357749b99fcd90ebedecee67bc` |
| ui-all/p01-b002-1440-light-continuation-1.png | `d28d14ada64682d94b8608b21b01ad70ddf914662b5af630ffd003caded47c3b` |
| ui-all/p01-b002-1440-light.png | `a32bf944ee42f2818ee99b3527e6318b4a2dbba99b94d9d52d02a082ac2c6fe5` |
| ui-all/p01-b002-390-dark-continuation-1.png | `f532460bfa93da008a5efeac51c490bf636d23ea6189b61b6289aefb3772eb13` |
| ui-all/p01-b002-390-dark.png | `7a851f26df636403adb48a1cd82f0ebcc602aea753c1486211c616d20f7fd443` |
| ui-all/p02-b001-1440-light-continuation-1.png | `90ad2301c721277a9d52a82072d74c69f4c2c1e4cb5c65437fcd7b8b0ef7f36e` |
| ui-all/p02-b001-1440-light.png | `ab87c00831238389250b31d68d2b31fbf894983ef43c1c1e9242550397e44266` |
| ui-all/p02-b001-390-dark-continuation-1.png | `67336b99f911af550c4585c84ec9961f8b088ad51fd3acf86fea621f18310843` |
| ui-all/p02-b001-390-dark-continuation-2.png | `ea823633555e4c6fcc8ceb69b91a94483e68f47a060c108e3f54614ec729a58e` |
| ui-all/p02-b001-390-dark.png | `4426e07e7dc521cd9e40662f73d3325d67836f4fe6e678b2f37bcbd6899dbf7a` |
| ui-all/p03-b001-1440-light-continuation-1.png | `1886cd572288d7b35f5a17854966071d1d9ed9eb91bc52319ead54e8889a64b0` |
| ui-all/p03-b001-1440-light-continuation-2.png | `4eec07a30e5b1e32de15b924a42efa6cf733ca79bd22c68ab8515330c25900ab` |
| ui-all/p03-b001-1440-light.png | `f7b684358868a9f2f91ac6eed70d5ffa825881a1fdcdc3bd6a2d6c9c632d8c5f` |
| ui-all/p03-b001-390-dark-continuation-1.png | `72cc212d78060b44f1d17fa13a1831048e86f89cad563ad701f95fbca821bc38` |
| ui-all/p03-b001-390-dark-continuation-2.png | `f877f9690986b97109bb7ca747ef26231431e0c078ff573e415c49847cc21608` |
| ui-all/p03-b001-390-dark.png | `3145875e8475bc8a0f4ca19b20d6b7638729a527367c159852dfef9a28ee2691` |
| ui-all/p04-b001-1440-light-continuation-1.png | `6975fea359e76cc8762abf74ff43e5a3db15a4f72ba7b7568c616b203357e8cc` |
| ui-all/p04-b001-1440-light-continuation-2.png | `67ab3e3fd98e5c1886623cd185e1518b7e80a5c4a31caa9c94a7aea89ff62a6b` |
| ui-all/p04-b001-1440-light.png | `dd687cd35e9d08117b1a45a1b6245f13e0bbc7b7c47ba5e51ced00a212d163fa` |
| ui-all/p04-b001-390-dark-continuation-1.png | `da0ddfbcb2f376f16d7979898afb3c47c83ee7382bdfc2a40817b037ce5e427f` |
| ui-all/p04-b001-390-dark-continuation-2.png | `2ecacbe66f3fa4c07c1a20f3ebdc9a86ed838b8d3a62929f98da9f64887d2e3a` |
| ui-all/p04-b001-390-dark.png | `420bb63721b90c3175b879eb5a6c63eeebda758b0c581e596297d06634ca7924` |
| ui-all/p05-b001-1440-light-continuation-1.png | `528d2d9980b722b0a599709d113a7875826231021608ea8dec99f8c0a382e9cd` |
| ui-all/p05-b001-1440-light-continuation-2.png | `aa3702646d51fa926f2bb92dc35e27f2c8093a32a08e02fef1040291149a58a4` |
| ui-all/p05-b001-1440-light.png | `8b58bc120a1ceac2d4902c92505f397cc25a67c9e14a90b84975bcffd261893a` |
| ui-all/p05-b001-390-dark-continuation-1.png | `e4684a2111a50cdf7bf90e4f785b13efc6677120e5946072d71645ba98ae64a2` |
| ui-all/p05-b001-390-dark-continuation-2.png | `1b803902fcb904926433ec22db26d500452cce99031981dd61711023d87afe6b` |
| ui-all/p05-b001-390-dark.png | `38839ebf7f9e2dff14aaab1144a85187d3327bfe7077c6c89b47a8bb71167e69` |
| ui-all/p06-b001-1440-light-continuation-1.png | `92ac0295f8cd8184600d9be553a756b6b3f90f445f3e9319477182265a0c9f28` |
| ui-all/p06-b001-1440-light-continuation-2.png | `5d6aa46ac80951c7373538e58dfa7aaae6a93b21d4bc23862889c2309e2d1e46` |
| ui-all/p06-b001-1440-light.png | `389a8936f251979bd469cfd2f89c6d478b7fff7bb39082f5619e14d1431a6f5d` |
| ui-all/p06-b001-390-dark-continuation-1.png | `1c0dd1f215e2e42a010a0469e06204816ebccbb12fc31b8f644427006b6a1996` |
| ui-all/p06-b001-390-dark-continuation-2.png | `97b1fb3ad1edc05e6ad19ca5ef4401e744eca0ace697fe7ba8a380a491dfe0c6` |
| ui-all/p06-b001-390-dark.png | `8509f185b8c6c018f6aa3ec2ebd0a4d22c33e25446780450c0838e6bb8262fc2` |
| ui-all/p07-b001-1440-light-continuation-1.png | `589dc165e7ac3a6b35ed3d772e200d914ebb0cebdca09ae42e3f197988ef3bb9` |
| ui-all/p07-b001-1440-light.png | `0538e93320ae9108a762345f912c52b7ddd1a79b912c9603a78f1575c5dd3fd2` |
| ui-all/p07-b001-390-dark-continuation-1.png | `59dd5bcdb30da76cc1cf395691e09a14af42015fe353b537ad9c646c9c043a7d` |
| ui-all/p07-b001-390-dark-continuation-2.png | `ff6497facff7dd99ee23cf85dd23ee2b0c130071331d7d8361b621478a593727` |
| ui-all/p07-b001-390-dark.png | `b16b8a43f46d25f3396683cae5f88701d64e28a33e07119369b44f48a12cc20d` |
| ui-all/p08-b001-1440-light.png | `5e167d9e077fbe05f7b8c07454a927cb027d4af06e05af394e0cd1a6e4817ea2` |
| ui-all/p08-b001-390-dark.png | `ff6497facff7dd99ee23cf85dd23ee2b0c130071331d7d8361b621478a593727` |
| ui-navigation/click-001-1440-light.png | `55d31ac951da584e555a4a81aebc2ff6833f4aabd79afef03d76d244b11aa169` |
| ui-navigation/click-001-390-dark.png | `07b1c2b58d8abfeaa6852c8e9091a5fe96b92f31d09d6964472069fd46bca70a` |
| ui-navigation/click-058-1440-light.png | `6098a92a6441cea10eb9015d87b58afe36920c78335eaea97fa49ea0f0d5730d` |
| ui-navigation/click-058-390-dark.png | `284f7c80011a6d9c3754a35bf7b787a584f6fb32ef882894bebac8616b5c64c4` |
| ui-navigation/click-161-1440-light.png | `134779b7d8d3f1d8acff7286389922c083f22974616f820a123b084e3749d2db` |
| ui-navigation/click-161-390-dark.png | `feec600f0e3584c6f1ff01807cf81b4341b170cce442a97c09edaeffcf3c9155` |
| ui-navigation/click-279-1440-light.png | `3153e22d10393e5d4cfc927f3c75c372cab942cf0b240ba8dd0b6326b23e20c9` |
| ui-navigation/click-279-390-dark.png | `707ee7e5c67551a9eb9649940638e12293baf18900819530f04839190d6da7b0` |
| ui-navigation/click-285-1440-light.png | `8ae9655891d5e4aae48153f7990ba8c707c60aa4c5fa8eb7defc83391d959114` |
| ui-navigation/click-285-390-dark.png | `31f97405703509ac0e47c149894f48af1cbf60899064ee417c4e07916c9b818b` |

## 最终完成项

- [x] 实际查看全部 8 原目录页，逐项核对原顺序、中文题意、页码、层级和粗体。
- [x] 冻结最终目录源稿与 JSON，并复算与 root 一致的 LF、rendered 与空图片指纹。
- [x] 独立复核最终实际 31 处题名对齐的含义。
- [x] 全量核对 285 个链接的目标单元、块、页码、标题和层级。
- [x] 核对前后原印页码、顺序、depth 与 strong 守恒。
- [x] 实际查看两模式全部 42 张目录截图及 10 张点击落点截图。
- [x] CF-01 已修复，原页的 24 个顶层页码强调已在最终网页中复核关闭。
- [x] 无未解决问题，目录最终增量可验收，交 root 与全书 reviewer 汇总。
