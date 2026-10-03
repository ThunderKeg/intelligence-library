# 《Deep Learning: Foundations and Concepts》翻译编撰任务

原书：仓库根目录 PDF，共 656 个 PDF 页面。页码均指 PDF 物理页（从 1 开始），以免与书内印刷页码混淆。
现有第 1 章译稿须重新按原书核对，并补齐图片、公式、导读及审查。所有未勾选项均未通过验收。

## 总体进展

- [x] 将翻译、编撰、审查和多 Agent 协作要求写入仓库根目录 `AGENTS.md`。
- [x] 核实 PDF 为 656 页，盘点正文 20 章及前后附属内容，建立逐章逐节任务。
- [x] 定义逐页可追溯的章节 Markdown 格式与图、表、公式编写约定。
- [x] 编写章节构建器，样例验证行内和独立公式能转换为 MathML。
- [ ] 将章节图片纳入 GitHub Pages 发布，并在阅读器中验证图片、公式、代码和表格。
- [x] 从原书 PDF 文本层生成逐页图、表、算法、公式编号定位索引（仍需目视核对）。
- [x] 增加原书与章节 JSON 的图、表、算法、公式编号和逐页内容自动对照；第 1–20 章标签检查通过（自动结果仍需逐页审查）。
- [x] 建立正文与附录 A–C 的逐页图、表、算法、公式定位索引；章节源稿以 PDF 页标记与译文对应，JSON 为每个阅读块记录 `pdfPage`。代码由逐章审查核对。
- [x] 图片、图内译注、数学公式、代码、表格与跨章引用文字在阅读页显示，并完成手机与深色模式检查；正文引用暂不支持点按跳转。
- [x] PDF 第 1–656 页的前置材料、前言、正文 20 章、附录 A–C、参考文献及索引均完成编撰与独立单元审查。
- [x] 独立 Agent 完成全书一致性复审，页边引用遗漏已修复并复验；见 `reviews/global-review.md`。
- [x] 本地站点完整性、按书阅读进度、28 个单元离线文本与已访问图片、移动端检查通过；首次离线尚未访问的图片不可用。

## 分工与完成标准

每章由初译 Agent 与不同的审查 Agent 负责；审查人需记录问题，初译或集成 Agent 修复后方可勾选完成。
各章独立写入自己的源文件和章节 JSON；共享站点文件由集成 Agent 统一修改。
对照 PDF 原页检查内容、图表和公式；自动提取结果仅作定位辅助。

## 封面、题名页与版权页（PDF 第 1–4 页）

- [x] 初编图书题名、作者和出版信息；依阅读页简洁原则编排。
- [x] 保留封面图并翻译封面文字，已生成阅读页数据。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/frontmatter-review.md`。

## Preface：Preface（PDF 第 5–10 页）

- [x] 前言 PDF 第 5–10 页已逐页初译、独立审查、修复问题并通过站点验收。
- [x] 翻译并核对前言开篇正文。
- [x] Goals of the book（PDF 第 5 页起）
- [x] Responsible use of technology（PDF 第 6 页起）
- [x] Structure of the book（PDF 第 6 页起）
- [x] References（PDF 第 7 页起）
- [x] Exercises（PDF 第 8 页起）
- [x] Mathematical notation（PDF 第 8 页起）
- [x] Acknowledgements（PDF 第 9 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## Contents：Contents（PDF 第 11–20 页）

- [x] 按原书 10 页初编 407 条目录项，保留标题层级与印刷页码。
- [x] 核对附录 A 在原书目录中出现，但 PDF 书签缺失。
- [x] 按 PDF 原页核对 407 个目录项、编号、层级、顺序与印刷页码，无遗漏。
- [x] 核对原书目录无图片、图注或表格。
- [x] 核对原书目录无编号公式或代码。
- [x] 检查目录导航、缩进、加粗、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复目录层级丢失问题，完成本部分验收；见 `reviews/contents-review.md`。

## 第 1 章：1 The Deep Learning Revolution（PDF 第 21–42 页）

- [x] 第 1 章已按 PDF 物理页 21–42 重译、逐页审查、修复排版问题并通过站点验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 1.1. The Impact of Deep Learning（PDF 第 22 页起）
  - [x] 1.1.1 Medical diagnosis（PDF 第 22 页起）
  - [x] 1.1.2 Protein structure（PDF 第 23 页起）
  - [x] 1.1.3 Image synthesis（PDF 第 24 页起）
  - [x] 1.1.4 Large language models（PDF 第 25 页起）
- [x] 1.2. A Tutorial Example（PDF 第 26 页起）
  - [x] 1.2.1 Synthetic data（PDF 第 26 页起）
  - [x] 1.2.2 Linear models（PDF 第 28 页起）
  - [x] 1.2.3 Error function（PDF 第 28 页起）
  - [x] 1.2.4 Model complexity（PDF 第 29 页起）
  - [x] 1.2.5 Regularization（PDF 第 32 页起）
  - [x] 1.2.6 Model selection（PDF 第 34 页起）
- [x] 1.3. A Brief History of Machine Learning（PDF 第 36 页起）
  - [x] 1.3.1 Single-layer networks（PDF 第 37 页起）
  - [x] 1.3.2 Backpropagation（PDF 第 38 页起）
  - [x] 1.3.3 Deep networks（PDF 第 40 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 2 章：2 Probabilities（PDF 第 43–83 页）

- [x] 第 2 章 PDF 第 43–83 页已逐页初译、独立审查、修复问题并通过站点验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 2.1. The Rules of Probability（PDF 第 45 页起）
  - [x] 2.1.1 A medical screening example（PDF 第 45 页起）
  - [x] 2.1.2 The sum and product rules（PDF 第 46 页起）
  - [x] 2.1.3 Bayes’ theorem（PDF 第 48 页起）
  - [x] 2.1.4 Medical screening revisited（PDF 第 50 页起）
  - [x] 2.1.5 Prior and posterior probabilities（PDF 第 51 页起）
  - [x] 2.1.6 Independent variables（PDF 第 51 页起）
- [x] 2.2. Probability Densities（PDF 第 52 页起）
  - [x] 2.2.1 Example distributions（PDF 第 53 页起）
  - [x] 2.2.2 Expectations and covariances（PDF 第 54 页起）
- [x] 2.3. The Gaussian Distribution（PDF 第 56 页起）
  - [x] 2.3.1 Mean and variance（PDF 第 57 页起）
  - [x] 2.3.2 Likelihood function（PDF 第 57 页起）
  - [x] 2.3.3 Bias of maximum likelihood（PDF 第 59 页起）
  - [x] 2.3.4 Linear regression（PDF 第 60 页起）
- [x] 2.4. Transformation of Densities（PDF 第 62 页起）
  - [x] 2.4.1 Multivariate distributions（PDF 第 64 页起）
- [x] 2.5. Information Theory（PDF 第 66 页起）
  - [x] 2.5.1 Entropy（PDF 第 66 页起）
  - [x] 2.5.2 Physics perspective（PDF 第 67 页起）
  - [x] 2.5.3 Differential entropy（PDF 第 69 页起）
  - [x] 2.5.4 Maximum entropy（PDF 第 70 页起）
  - [x] 2.5.5 Kullback–Leibler divergence（PDF 第 71 页起）
  - [x] 2.5.6 Conditional entropy（PDF 第 73 页起）
  - [x] 2.5.7 Mutual information（PDF 第 74 页起）
- [x] 2.6. Bayesian Probabilities（PDF 第 74 页起）
  - [x] 2.6.1 Model parameters（PDF 第 75 页起）
  - [x] 2.6.2 Regularization（PDF 第 76 页起）
  - [x] 2.6.3 Bayesian machine learning（PDF 第 77 页起）
- [x] Exercises（PDF 第 78 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 3 章：3 Standard Distributions（PDF 第 84–129 页）

- [x] 第 3 章 PDF 第 84–129 页已逐页初译、独立审查、修复问题并通过站点验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 3.1. Discrete Variables（PDF 第 85 页起）
  - [x] 3.1.1 Bernoulli distribution（PDF 第 85 页起）
  - [x] 3.1.2 Binomial distribution（PDF 第 86 页起）
  - [x] 3.1.3 Multinomial distribution（PDF 第 87 页起）
- [x] 3.2. The Multivariate Gaussian（PDF 第 89 页起）
  - [x] 3.2.1 Geometry of the Gaussian（PDF 第 90 页起）
  - [x] 3.2.2 Moments（PDF 第 93 页起）
  - [x] 3.2.3 Limitations（PDF 第 94 页起）
  - [x] 3.2.4 Conditional distribution（PDF 第 95 页起）
  - [x] 3.2.5 Marginal distribution（PDF 第 98 页起）
  - [x] 3.2.6 Bayes’ theorem（PDF 第 100 页起）
  - [x] 3.2.7 Maximum likelihood（PDF 第 103 页起）
  - [x] 3.2.8 Sequential estimation（PDF 第 104 页起）
  - [x] 3.2.9 Mixtures of Gaussians（PDF 第 105 页起）
- [x] 3.3. Periodic Variables（PDF 第 108 页起）
  - [x] 3.3.1 Von Mises distribution（PDF 第 108 页起）
- [x] 3.4. The Exponential Family（PDF 第 113 页起）
  - [x] 3.4.1 Sufficient statistics（PDF 第 116 页起）
- [x] 3.5. Nonparametric Methods（PDF 第 117 页起）
  - [x] 3.5.1 Histograms（PDF 第 117 页起）
  - [x] 3.5.2 Kernel densities（PDF 第 119 页起）
  - [x] 3.5.3 Nearest-neighbours（PDF 第 122 页起）
- [x] Exercises（PDF 第 124 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 4 章：4 Single-layer Networks: Regression（PDF 第 130–149 页）

- [x] 第 4 章 PDF 第 130–149 页已逐页初译、独立审查、修复问题并通过站点验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 4.1. Linear Regression（PDF 第 131 页起）
  - [x] 4.1.1 Basis functions（PDF 第 131 页起）
  - [x] 4.1.2 Likelihood function（PDF 第 133 页起）
  - [x] 4.1.3 Maximum likelihood（PDF 第 134 页起）
  - [x] 4.1.4 Geometry of least squares（PDF 第 136 页起）
  - [x] 4.1.5 Sequential learning（PDF 第 136 页起）
  - [x] 4.1.6 Regularized least squares（PDF 第 137 页起）
  - [x] 4.1.7 Multiple outputs（PDF 第 138 页起）
- [x] 4.2. Decision theory（PDF 第 139 页起）
- [x] 4.3. The Bias–Variance Trade-off（PDF 第 142 页起）
- [x] Exercises（PDF 第 147 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 5 章：5 Single-layer Networks: Classification（PDF 第 150–188 页）

- [x] PDF 第 150–188 页初译与逐页自检完成，图 5.1–5.17、式 (5.1)–(5.105)、习题 5.1–5.24 已入源稿；独立审查的 5 项问题及跨图断句已修复并复验通过。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 5.1. Discriminant Functions（PDF 第 151 页起）
  - [x] 5.1.1 Two classes（PDF 第 151 页起）
  - [x] 5.1.2 Multiple classes（PDF 第 153 页起）
  - [x] 5.1.3 1-of-K coding（PDF 第 154 页起）
  - [x] 5.1.4 Least squares for classification（PDF 第 155 页起）
- [x] 5.2. Decision Theory（PDF 第 157 页起）
  - [x] 5.2.1 Misclassification rate（PDF 第 158 页起）
  - [x] 5.2.2 Expected loss（PDF 第 159 页起）
  - [x] 5.2.3 The reject option（PDF 第 161 页起）
  - [x] 5.2.4 Inference and decision（PDF 第 162 页起）
  - [x] 5.2.5 Classifier accuracy（PDF 第 166 页起）
  - [x] 5.2.6 ROC curve（PDF 第 167 页起）
- [x] 5.3. Generative Classifiers（PDF 第 169 页起）
  - [x] 5.3.1 Continuous inputs（PDF 第 171 页起）
  - [x] 5.3.2 Maximum likelihood solution（PDF 第 172 页起）
  - [x] 5.3.3 Discrete features（PDF 第 175 页起）
  - [x] 5.3.4 Exponential family（PDF 第 175 页起）
- [x] 5.4. Discriminative Classifiers（PDF 第 176 页起）
  - [x] 5.4.1 Activation functions（PDF 第 177 页起）
  - [x] 5.4.2 Fixed basis functions（PDF 第 177 页起）
  - [x] 5.4.3 Logistic regression（PDF 第 178 页起）
  - [x] 5.4.4 Multi-class logistic regression（PDF 第 180 页起）
  - [x] 5.4.5 Probit regression（PDF 第 182 页起）
  - [x] 5.4.6 Canonical link functions（PDF 第 183 页起）
- [x] Exercises（PDF 第 185 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 6 章：6 Deep Neural Networks（PDF 第 189–225 页）

- [x] 第 6 章 PDF 第 189–225 页已逐页初译、独立审查、修复并复验通过；图 6.1–6.19、式 (6.1)–(6.66)、习题 6.1–6.21 齐全，站点验收通过。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 6.1. Limitations of Fixed Basis Functions（PDF 第 190 页起）
  - [x] 6.1.1 The curse of dimensionality（PDF 第 190 页起）
  - [x] 6.1.2 High-dimensional spaces（PDF 第 193 页起）
  - [x] 6.1.3 Data manifolds（PDF 第 194 页起）
  - [x] 6.1.4 Data-dependent basis functions（PDF 第 196 页起）
- [x] 6.2. Multilayer Networks（PDF 第 198 页起）
  - [x] 6.2.1 Parameter matrices（PDF 第 199 页起）
  - [x] 6.2.2 Universal approximation（PDF 第 199 页起）
  - [x] 6.2.3 Hidden unit activation functions（PDF 第 200 页起）
  - [x] 6.2.4 Weight-space symmetries（PDF 第 203 页起）
- [x] 6.3. Deep Networks（PDF 第 204 页起）
  - [x] 6.3.1 Hierarchical representations（PDF 第 205 页起）
  - [x] 6.3.2 Distributed representations（PDF 第 205 页起）
  - [x] 6.3.3 Representation learning（PDF 第 206 页起）
  - [x] 6.3.4 Transfer learning（PDF 第 207 页起）
  - [x] 6.3.5 Contrastive learning（PDF 第 209 页起）
  - [x] 6.3.6 General network architectures（PDF 第 211 页起）
  - [x] 6.3.7 Tensors（PDF 第 212 页起）
- [x] 6.4. Error Functions（PDF 第 212 页起）
  - [x] 6.4.1 Regression（PDF 第 212 页起）
  - [x] 6.4.2 Binary classification（PDF 第 214 页起）
  - [x] 6.4.3 multiclass classification（PDF 第 215 页起）
- [x] 6.5. Mixture Density Networks（PDF 第 216 页起）
  - [x] 6.5.1 Robot kinematics example（PDF 第 216 页起）
  - [x] 6.5.2 Conditional mixture distributions（PDF 第 217 页起）
  - [x] 6.5.3 Gradient optimization（PDF 第 219 页起）
  - [x] 6.5.4 Predictive distribution（PDF 第 220 页起）
- [x] Exercises（PDF 第 222 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题；见 `reviews/chapter-06-review.md`。
- [x] 修复审查问题，完成本部分验收；见 `reviews/chapter-06-acceptance.md`。

## 第 7 章：7 Gradient Descent（PDF 第 226–249 页）

- [x] 第 7 章 PDF 第 226–249 页已初译、独立审查、修复并复验通过；图 7.1–7.8、算法 7.1–7.4、式 (7.1)–(7.69)、习题 7.1–7.14 齐全，站点验收通过。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 7.1. Error Surfaces（PDF 第 227 页起）
  - [x] 7.1.1 Local quadratic approximation（PDF 第 228 页起）
- [x] 7.2. Gradient Descent Optimization（PDF 第 230 页起）
  - [x] 7.2.1 Use of gradient information（PDF 第 231 页起）
  - [x] 7.2.2 Batch gradient descent（PDF 第 231 页起）
  - [x] 7.2.3 Stochastic gradient descent（PDF 第 231 页起）
  - [x] 7.2.4 Mini-batches（PDF 第 233 页起）
  - [x] 7.2.5 Parameter initialization（PDF 第 233 页起）
- [x] 7.3. Convergence（PDF 第 235 页起）
  - [x] 7.3.1 Momentum（PDF 第 237 页起）
  - [x] 7.3.2 Learning rate schedule（PDF 第 239 页起）
  - [x] 7.3.3 RMSProp and Adam（PDF 第 240 页起）
- [x] 7.4. Normalization（PDF 第 241 页起）
  - [x] 7.4.1 Data normalization（PDF 第 243 页起）
  - [x] 7.4.2 Batch normalization（PDF 第 244 页起）
  - [x] 7.4.3 Layer normalization（PDF 第 246 页起）
- [x] Exercises（PDF 第 247 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题；见 `reviews/chapter-07-review.md`。
- [x] 修复审查问题，完成本部分验收；见 `reviews/chapter-07-acceptance.md`。

## 第 8 章：8 Backpropagation（PDF 第 250–269 页）

- [x] 第 8 章 PDF 第 250–269 页已初译、独立审查、修复并复验通过；图 8.1–8.5、算法 8.1、式 (8.1)–(8.80)、习题 8.1–8.18 齐全，站点验收通过。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 8.1. Evaluation of Gradients（PDF 第 251 页起）
  - [x] 8.1.1 Single-layer networks（PDF 第 251 页起）
  - [x] 8.1.2 General feed-forward networks（PDF 第 252 页起）
  - [x] 8.1.3 A simple example（PDF 第 255 页起）
  - [x] 8.1.4 Numerical differentiation（PDF 第 256 页起）
  - [x] 8.1.5 The Jacobian matrix（PDF 第 257 页起）
  - [x] 8.1.6 The Hessian matrix（PDF 第 259 页起）
- [x] 8.2. Automatic Differentiation（PDF 第 261 页起）
  - [x] 8.2.1 Forward-mode automatic differentiation（PDF 第 263 页起）
  - [x] 8.2.2 Reverse-mode automatic differentiation（PDF 第 266 页起）
- [x] Exercises（PDF 第 267 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题；见 `reviews/chapter-08-review.md`。
- [x] 修复审查问题，完成本部分验收；见 `reviews/chapter-08-acceptance.md`。

## 第 9 章：9 Regularization（PDF 第 270–302 页）

- [x] PDF 第 270–302 页初译与逐页自检完成，图 9.1–9.17、式 (9.1)–(9.73)、习题 9.1–9.18 已入源稿，自动标签对照通过。
- [x] 独立审查已记录六处原书疑点；对应译注或排印修正已加入，重建和布局自检通过。
- [x] 由独立 Agent 对修订后的第 9 章复验，已通过验收；见 reviews/chapter-09-acceptance.md。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 9.1. Inductive Bias（PDF 第 271 页起）
  - [x] 9.1.1 Inverse problems（PDF 第 271 页起）
  - [x] 9.1.2 No free lunch theorem（PDF 第 272 页起）
  - [x] 9.1.3 Symmetry and invariance（PDF 第 273 页起）
  - [x] 9.1.4 Equivariance（PDF 第 276 页起）
- [x] 9.2. Weight Decay（PDF 第 277 页起）
  - [x] 9.2.1 Consistent regularizers（PDF 第 279 页起）
  - [x] 9.2.2 Generalized weight decay（PDF 第 281 页起）
- [x] 9.3. Learning Curves（PDF 第 283 页起）
  - [x] 9.3.1 Early stopping（PDF 第 283 页起）
  - [x] 9.3.2 Double descent（PDF 第 285 页起）
- [x] 9.4. Parameter Sharing（PDF 第 287 页起）
  - [x] 9.4.1 Soft weight sharing（PDF 第 288 页起）
- [x] 9.5. Residual Connections（PDF 第 291 页起）
- [x] 9.6. Model Averaging（PDF 第 294 页起）
  - [x] 9.6.1 Dropout（PDF 第 296 页起）
- [x] Exercises（PDF 第 298 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 10 章：10 Convolutional Networks（PDF 第 303–340 页）

- [x] PDF 第 303–340 页初译与逐页自检完成，图 10.1–10.32、式 (10.1)–(10.22)、习题 10.1–10.13 已入源稿；JSON 构建及自动标签对照通过。
- [x] 独立审查已记录六处原书疑点；对应译注已加入，重建和布局自检通过。
- [x] 由独立 Agent 对修订后的第 10 章复验，再决定是否验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 10.1. Computer Vision（PDF 第 304 页起）
  - [x] 10.1.1 Image data（PDF 第 305 页起）
- [x] 10.2. Convolutional Filters（PDF 第 306 页起）
  - [x] 10.2.1 Feature detectors（PDF 第 306 页起）
  - [x] 10.2.2 Translation equivariance（PDF 第 307 页起）
  - [x] 10.2.3 Padding（PDF 第 310 页起）
  - [x] 10.2.4 Strided convolutions（PDF 第 310 页起）
  - [x] 10.2.5 Multi-dimensional convolutions（PDF 第 311 页起）
  - [x] 10.2.6 Pooling（PDF 第 312 页起）
  - [x] 10.2.7 Multilayer convolutions（PDF 第 314 页起）
  - [x] 10.2.8 Example network architectures（PDF 第 315 页起）
- [x] 10.3. Visualizing Trained CNNs（PDF 第 318 页起）
  - [x] 10.3.1 Visual cortex（PDF 第 318 页起）
  - [x] 10.3.2 Visualizing trained filters（PDF 第 319 页起）
  - [x] 10.3.3 Saliency maps（PDF 第 321 页起）
  - [x] 10.3.4 Adversarial attacks（PDF 第 322 页起）
  - [x] 10.3.5 Synthetic images（PDF 第 324 页起）
- [x] 10.4. Object Detection（PDF 第 324 页起）
  - [x] 10.4.1 Bounding boxes（PDF 第 325 页起）
  - [x] 10.4.2 Intersection-over-union（PDF 第 326 页起）
  - [x] 10.4.3 Sliding windows（PDF 第 327 页起）
  - [x] 10.4.4 Detection across scales（PDF 第 329 页起）
  - [x] 10.4.5 Non-max suppression（PDF 第 330 页起）
  - [x] 10.4.6 Fast region CNNs（PDF 第 330 页起）
- [x] 10.5. Image Segmentation（PDF 第 331 页起）
  - [x] 10.5.1 Convolutional segmentation（PDF 第 331 页起）
  - [x] 10.5.2 Up-sampling（PDF 第 332 页起）
  - [x] 10.5.3 Fully convolutional networks（PDF 第 334 页起）
  - [x] 10.5.4 The U-net architecture（PDF 第 335 页起）
- [x] 10.6. Style Transfer（PDF 第 336 页起）
- [x] Exercises（PDF 第 338 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 11 章：11 Structured Distributions（PDF 第 341–372 页）

- [x] PDF 第 341–372 页初译与逐页自检完成，图 11.1–11.32、表 11.1、式 (11.1)–(11.52)、习题 11.1–11.19 已入源稿；JSON 构建及自动标签对照通过。
- [x] 独立 Agent 已逐页审查并记录未通过问题；跨页合段、页码归属、原书疑点译注及习题语义已修订，重建与布局自检通过。
- [x] 由独立 Agent 对修订后的第 11 章复验，再决定是否验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 11.1. Graphical Models（PDF 第 342 页起）
  - [x] 11.1.1 Directed graphs（PDF 第 342 页起）
  - [x] 11.1.2 Factorization（PDF 第 343 页起）
  - [x] 11.1.3 Discrete variables（PDF 第 345 页起）
  - [x] 11.1.4 Gaussian variables（PDF 第 348 页起）
  - [x] 11.1.5 Binary classifier（PDF 第 350 页起）
  - [x] 11.1.6 Parameters and observations（PDF 第 350 页起）
  - [x] 11.1.7 Bayes’ theorem（PDF 第 352 页起）
- [x] 11.2. Conditional Independence（PDF 第 353 页起）
  - [x] 11.2.1 Three example graphs（PDF 第 354 页起）
  - [x] 11.2.2 Explaining away（PDF 第 357 页起）
  - [x] 11.2.3 D-separation（PDF 第 359 页起）
  - [x] 11.2.4 Naive Bayes（PDF 第 360 页起）
  - [x] 11.2.5 Generative models（PDF 第 362 页起）
  - [x] 11.2.6 Markov blanket（PDF 第 363 页起）
  - [x] 11.2.7 Graphs as filters（PDF 第 364 页起）
- [x] 11.3. Sequence Models（PDF 第 365 页起）
  - [x] 11.3.1 Hidden variables（PDF 第 368 页起）
- [x] Exercises（PDF 第 369 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 12 章：12 Transformers（PDF 第 373–422 页）

- [x] PDF 第 373–422 页初译和自检完成，图 12.1–12.27、算法 12.1–12.3、式 (12.1)–(12.46)、习题 12.1–12.16 已入源稿；JSON 构建、自动标签对照及多视口初步排版检查通过，独立审查和定向复验均已通过；见 reviews/chapter-12-acceptance.md。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 12.1. Attention（PDF 第 374 页起）
  - [x] 12.1.1 Transformer processing（PDF 第 376 页起）
  - [x] 12.1.2 Attention coefficients（PDF 第 377 页起）
  - [x] 12.1.3 Self-attention（PDF 第 378 页起）
  - [x] 12.1.4 Network parameters（PDF 第 379 页起）
  - [x] 12.1.5 Scaled self-attention（PDF 第 382 页起）
  - [x] 12.1.6 Multi-head attention（PDF 第 382 页起）
  - [x] 12.1.7 Transformer layers（PDF 第 384 页起）
  - [x] 12.1.8 Computational complexity（PDF 第 386 页起）
  - [x] 12.1.9 Positional encoding（PDF 第 387 页起）
- [x] 12.2. Natural Language（PDF 第 390 页起）
  - [x] 12.2.1 Word embedding（PDF 第 391 页起）
  - [x] 12.2.2 Tokenization（PDF 第 393 页起）
  - [x] 12.2.3 Bag of words（PDF 第 394 页起）
  - [x] 12.2.4 Autoregressive models（PDF 第 395 页起）
  - [x] 12.2.5 Recurrent neural networks（PDF 第 396 页起）
  - [x] 12.2.6 Backpropagation through time（PDF 第 397 页起）
- [x] 12.3. Transformer Language Models（PDF 第 398 页起）
  - [x] 12.3.1 Decoder transformers（PDF 第 399 页起）
  - [x] 12.3.2 Sampling strategies（PDF 第 402 页起）
  - [x] 12.3.3 Encoder transformers（PDF 第 404 页起）
  - [x] 12.3.4 Sequence-to-sequence transformers（PDF 第 406 页起）
  - [x] 12.3.5 Large language models（PDF 第 406 页起）
- [x] 12.4. Multimodal Transformers（PDF 第 410 页起）
  - [x] 12.4.1 Vision transformers（PDF 第 411 页起）
  - [x] 12.4.2 Generative image transformers（PDF 第 412 页起）
  - [x] 12.4.3 Audio data（PDF 第 415 页起）
  - [x] 12.4.4 Text-to-speech（PDF 第 416 页起）
  - [x] 12.4.5 Vision and language transformers（PDF 第 418 页起）
- [x] Exercises（PDF 第 419 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 13 章：13 Graph Neural Networks（PDF 第 423–443 页）

- [x] PDF 第 423–443 页初译与逐页自检完成，图 13.1–13.5、算法 13.1–13.2、式 (13.1)–(13.47)、习题 13.1–13.10 已入源稿；JSON 构建及自动标签对照通过。
- [x] 独立审查已记录算法中文层级和式 (13.21) 译注范围两项问题；均已修订，重建与窄屏排版自检通过。
- [x] 由独立 Agent 对修订后的第 13 章复验，再决定是否验收。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 13.1. Machine Learning on Graphs（PDF 第 425 页起）
  - [x] 13.1.1 Graph properties（PDF 第 426 页起）
  - [x] 13.1.2 Adjacency matrix（PDF 第 426 页起）
  - [x] 13.1.3 Permutation equivariance（PDF 第 427 页起）
- [x] 13.2. Neural Message-Passing（PDF 第 428 页起）
  - [x] 13.2.1 Convolutional filters（PDF 第 429 页起）
  - [x] 13.2.2 Graph convolutional networks（PDF 第 430 页起）
  - [x] 13.2.3 Aggregation operators（PDF 第 432 页起）
  - [x] 13.2.4 Update operators（PDF 第 434 页起）
  - [x] 13.2.5 Node classification（PDF 第 435 页起）
  - [x] 13.2.6 Edge classification（PDF 第 436 页起）
  - [x] 13.2.7 Graph classification（PDF 第 436 页起）
- [x] 13.3. General Graph Networks（PDF 第 436 页起）
  - [x] 13.3.1 Graph attention networks（PDF 第 437 页起）
  - [x] 13.3.2 Edge embeddings（PDF 第 437 页起）
  - [x] 13.3.3 Graph embeddings（PDF 第 438 页起）
  - [x] 13.3.4 Over-smoothing（PDF 第 438 页起）
  - [x] 13.3.5 Regularization（PDF 第 439 页起）
  - [x] 13.3.6 Geometric deep learning（PDF 第 440 页起）
- [x] Exercises（PDF 第 441 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 14 章：14 Sampling（PDF 第 444–473 页）

- [x] PDF 第 444–473 页初译和自检完成，图 14.1–14.14、算法 14.1–14.4、式 (14.1)–(14.62)、习题 14.1–14.18 已入源稿；JSON 构建、自动标签对照及多视口初步排版检查通过，独立审查待完成。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 14.1. Basic Sampling Algorithms（PDF 第 445 页起）
  - [x] 14.1.1 Expectations（PDF 第 445 页起）
  - [x] 14.1.2 Standard distributions（PDF 第 446 页起）
  - [x] 14.1.3 Rejection sampling（PDF 第 448 页起）
  - [x] 14.1.4 Adaptive rejection sampling（PDF 第 450 页起）
  - [x] 14.1.5 Importance sampling（PDF 第 452 页起）
  - [x] 14.1.6 Sampling-importance-resampling（PDF 第 454 页起）
- [x] 14.2. Markov Chain Monte Carlo（PDF 第 455 页起）
  - [x] 14.2.1 The Metropolis algorithm（PDF 第 456 页起）
  - [x] 14.2.2 Markov chains（PDF 第 457 页起）
  - [x] 14.2.3 The Metropolis–Hastings algorithm（PDF 第 460 页起）
  - [x] 14.2.4 Gibbs sampling（PDF 第 461 页起）
  - [x] 14.2.5 Ancestral sampling（PDF 第 465 页起）
- [x] 14.3. Langevin Sampling（PDF 第 466 页起）
  - [x] 14.3.1 Energy-based models（PDF 第 467 页起）
  - [x] 14.3.2 Maximizing the likelihood（PDF 第 468 页起）
  - [x] 14.3.3 Langevin dynamics（PDF 第 469 页起）
- [x] Exercises（PDF 第 471 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 reviews/chapter-14-acceptance.md。

## 第 15 章：15 Discrete Latent Variables（PDF 第 474–508 页）

- [x] PDF 第 474–508 页完整译稿、17 张图、算法 15.1–15.3、式 (15.1)–(15.67) 和习题 15.1–15.24 已通过独立审查与修订复验；见 `reviews/chapter-15-acceptance.md`。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 15.1. K-means Clustering（PDF 第 475 页起）
  - [x] 15.1.1 Image segmentation（PDF 第 479 页起）
- [x] 15.2. Mixtures of Gaussians（PDF 第 481 页起）
  - [x] 15.2.1 Likelihood function（PDF 第 483 页起）
  - [x] 15.2.2 Maximum likelihood（PDF 第 485 页起）
- [x] 15.3. Expectation–Maximization Algorithm（PDF 第 489 页起）
  - [x] 15.3.1 Gaussian mixtures（PDF 第 493 页起）
  - [x] 15.3.2 Relation to K-means（PDF 第 495 页起）
  - [x] 15.3.3 Mixtures of Bernoulli distributions（PDF 第 496 页起）
- [x] 15.4. Evidence Lower Bound（PDF 第 500 页起）
  - [x] 15.4.1 EM revisited（PDF 第 501 页起）
  - [x] 15.4.2 Independent and identically distributed data（PDF 第 503 页起）
  - [x] 15.4.3 Parameter priors（PDF 第 504 页起）
  - [x] 15.4.4 Generalized EM（PDF 第 504 页起）
  - [x] 15.4.5 Sequential EM（PDF 第 505 页起）
- [x] Exercises（PDF 第 505 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 16 章：16 Continuous Latent Variables（PDF 第 509–545 页）

- [x] PDF 第 509–545 页完整译稿、章首图、图 16.1–16.15、式 (16.1)–(16.90)、习题 16.1–16.26 已通过独立审查与修订复验；见 `reviews/chapter-16-acceptance.md`。
- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 16.1. Principal Component Analysis（PDF 第 511 页起）
  - [x] 16.1.1 Maximum variance formulation（PDF 第 511 页起）
  - [x] 16.1.2 Minimum-error formulation（PDF 第 513 页起）
  - [x] 16.1.3 Data compression（PDF 第 515 页起）
  - [x] 16.1.4 Data whitening（PDF 第 516 页起）
  - [x] 16.1.5 High-dimensional data（PDF 第 518 页起）
- [x] 16.2. Probabilistic Latent Variables（PDF 第 520 页起）
  - [x] 16.2.1 Generative model（PDF 第 520 页起）
  - [x] 16.2.2 Likelihood function（PDF 第 521 页起）
  - [x] 16.2.3 Maximum likelihood（PDF 第 523 页起）
  - [x] 16.2.4 Factor analysis（PDF 第 527 页起）
  - [x] 16.2.5 Independent component analysis（PDF 第 528 页起）
  - [x] 16.2.6 Kalman filters（PDF 第 529 页起）
- [x] 16.3. Evidence Lower Bound（PDF 第 530 页起）
  - [x] 16.3.1 Expectation maximization（PDF 第 532 页起）
  - [x] 16.3.2 EM for PCA（PDF 第 533 页起）
  - [x] 16.3.3 EM for factor analysis（PDF 第 534 页起）
- [x] 16.4. Nonlinear Latent Variable Models（PDF 第 536 页起）
  - [x] 16.4.1 Nonlinear manifolds（PDF 第 536 页起）
  - [x] 16.4.2 Likelihood function（PDF 第 538 页起）
  - [x] 16.4.3 Discrete data（PDF 第 540 页起）
  - [x] 16.4.4 Four approaches to generative modelling（PDF 第 541 页起）
- [x] Exercises（PDF 第 541 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 17 章：17 Generative Adversarial Networks（PDF 第 546–558 页）

- [x] PDF 第 546–558 页完整译稿、图 17.1–17.10、式 (17.1)–(17.20)、习题 17.1–17.3 已通过独立审查与修订复验；见 `reviews/chapter-17-acceptance.md`。

- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 17.1. Adversarial Training（PDF 第 547 页起）
  - [x] 17.1.1 Loss function（PDF 第 548 页起）
  - [x] 17.1.2 GAN training in practice（PDF 第 549 页起）
- [x] 17.2. Image GANs（PDF 第 552 页起）
  - [x] 17.2.1 CycleGAN（PDF 第 552 页起）
- [x] Exercises（PDF 第 557 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 18 章：18 Normalizing Flows（PDF 第 559–573 页）

- [x] PDF 第 559–573 页完整译稿、图 18.1–18.7、式 (18.1)–(18.39)、习题已通过独立审查与修订复验；见 `reviews/chapter-18-acceptance.md`。

- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 18.1. Coupling Flows（PDF 第 561 页起）
- [x] 18.2. Autoregressive Flows（PDF 第 564 页起）
- [x] 18.3. Continuous Flows（PDF 第 566 页起）
  - [x] 18.3.1 Neural differential equations（PDF 第 566 页起）
  - [x] 18.3.2 Neural ODE backpropagation（PDF 第 567 页起）
  - [x] 18.3.3 Neural ODE flows（PDF 第 569 页起）
- [x] Exercises（PDF 第 571 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 19 章：19 Autoencoders（PDF 第 574–590 页）

- [x] PDF 第 574–590 页完整译稿、图 19.1–19.11、式 (19.1)–(19.25)、算法及习题已通过独立审查与修订复验；见 `reviews/chapter-19-acceptance.md`。

- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 19.1. Deterministic Autoencoders（PDF 第 575 页起）
  - [x] 19.1.1 Linear autoencoders（PDF 第 575 页起）
  - [x] 19.1.2 Deep autoencoders（PDF 第 576 页起）
  - [x] 19.1.3 Sparse autoencoders（PDF 第 577 页起）
  - [x] 19.1.4 Denoising autoencoders（PDF 第 578 页起）
  - [x] 19.1.5 Masked autoencoders（PDF 第 578 页起）
- [x] 19.2. Variational Autoencoders（PDF 第 580 页起）
  - [x] 19.2.1 Amortized inference（PDF 第 583 页起）
  - [x] 19.2.2 The reparameterization trick（PDF 第 585 页起）
- [x] Exercises（PDF 第 589 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## 第 20 章：20 Diffusion Models（PDF 第 591–617 页）

- [x] PDF 第 591–617 页完整译稿、图 20.1–20.9、式 (20.1)–(20.70)、算法及习题 20.1–20.20 已通过独立审查与修订复验；见 `reviews/chapter-20-acceptance.md`。

- [x] 编写本章简短导读，与原书正文清楚区分。
- [x] 翻译并核对章节开篇正文。
- [x] 20.1. Forward Encoder（PDF 第 592 页起）
  - [x] 20.1.1 Diffusion kernel（PDF 第 593 页起）
  - [x] 20.1.2 Conditional distribution（PDF 第 594 页起）
- [x] 20.2. Reverse Decoder（PDF 第 595 页起）
  - [x] 20.2.1 Training the decoder（PDF 第 597 页起）
  - [x] 20.2.2 Evidence lower bound（PDF 第 598 页起）
  - [x] 20.2.3 Rewriting the ELBO（PDF 第 599 页起）
  - [x] 20.2.4 Predicting the noise（PDF 第 601 页起）
  - [x] 20.2.5 Generating new samples（PDF 第 602 页起）
- [x] 20.3. Score Matching（PDF 第 604 页起）
  - [x] 20.3.1 Score loss function（PDF 第 605 页起）
  - [x] 20.3.2 Modified score loss（PDF 第 606 页起）
  - [x] 20.3.3 Noise variance（PDF 第 607 页起）
  - [x] 20.3.4 Stochastic differential equations（PDF 第 608 页起）
- [x] 20.4. Guided Diffusion（PDF 第 609 页起）
  - [x] 20.4.1 Classifier guidance（PDF 第 610 页起）
  - [x] 20.4.2 Classifier-free guidance（PDF 第 610 页起）
- [x] Exercises（PDF 第 613 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收。

## Appendix A. Linear Algebra：Appendix A. Linear Algebra（PDF 第 618–624 页）

- [x] 翻译并核对本部分开篇正文。
- [x] A.1 Matrix Identities（PDF 第 618 页起）
- [x] A.2 Traces and Determinants（PDF 第 619 页起）
- [x] A.3 Matrix Derivatives（PDF 第 620 页起）
- [x] A.4 Eigenvectors（PDF 第 621 页起）
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/appendix-a-acceptance.md`。

## Appendix B. Calculus of Variations：Appendix B. Calculus of Variations（PDF 第 625–627 页）

- [x] 翻译并核对本部分开篇正文。
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/appendix-b-review.md`。

## Appendix C. Lagrange Multipliers：Appendix C. Lagrange Multipliers（PDF 第 628–631 页）

- [x] 翻译并核对本部分开篇正文。
- [x] 按 PDF 原页核对段落、脚注、列表、习题和交叉引用，无遗漏。
- [x] 逐项核对图片、图内英文、图注和表格，并在网页中保留与翻译。
- [x] 逐项核对公式、编号、变量、上下标和代码，并检查网页呈现。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/appendix-c-review.md`。

## Bibliography：Bibliography（PDF 第 632–647 页）

- [x] 按原书顺序初编并核对 331 条参考文献；见 `reviews/backmatter-initial.md`。
- [x] 按 PDF 原页核对正文、双栏顺序、条目信息、跨页续接，无遗漏。
- [x] 核对原书此部分无图片、图注或表格。
- [x] 核对原书此部分无编号公式或代码。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/bibliography-review.md`。

## Index：Index（PDF 第 648–656 页）

- [x] 初编并核对 678 个双语词条、页码、粗体和交叉参见；见 `reviews/backmatter-initial.md`。
- [x] 按 PDF 原页核对双栏顺序、词条、页码、粗体和交叉参见，无遗漏。
- [x] 核对原书此部分无图片、图注或表格。
- [x] 核对原书此部分无编号公式或代码。
- [x] 检查术语、语言、目录导航、窄屏和深色模式排版。
- [x] 不同 Agent 对照原书完成独立审查并记录问题。
- [x] 修复审查问题，完成本部分验收；见 `reviews/index-review.md`。
