# 《Reinforcement Learning: An Introduction》第二版翻译与编撰任务清单

> 唯一正文依据：仓库根目录 Reinforcement_ Learning_An_Introduction.pdf，Richard S. Sutton、Andrew G. Barto，MIT Press，第二版。PDF 共 **548 个物理页**；SHA-256：2DD0D71D9EE883FBEB99F9B888C65AC3255FAE2512203D11B18E838BEFFFE9A6。书中阿拉伯页码与 PDF 物理页码相差 22（书第 1 页 = PDF 第 23 页）。目录经 PDF 第 7–12 页定位；原页仍是逐项验收依据。

## 当前进度（2026-10-03）

| 范围 | 状态 | 验收依据 |
| --- | --- | --- |
| 前置页、三部分引言、第 1–17 章 | 已译编、逐章独立审查通过、全书修订复核通过并加入本地书架 | 各 `REVIEW-*.md`；下方逐项勾选 |
| 参考文献 481–518 页 | 782 条已译编、独立复审通过并加入书架 | `REVIEW-REFS-503-527.md`、`REVIEW-REFS-528-540.md` |
| 索引 519–524 页 | 529 个列表项已译编、独立复审通过并加入书架 | `REVIEW-INDEX.md`；`chapter-IDX.json` |
| 系列书目 525–526 页 | 24 条已译编、独立复审通过并加入书架 | `REVIEW-SERIES.md`；`chapter-SERIES.json` |
| 全书复审 | 整体独立审查通过；八项问题均已修复并复核 | `REVIEW-GLOBAL.md`、`REVIEW-GLOBAL-FIXES.md`、`REVIEW-CH9-11-REBUNDLE.md` |

## 判定规则

- [x] 建立 PDF **第 1–548 物理页**的逐页核对记录，记录每页的正文、图、表、公式、伪代码、练习、脚注、注释与跨页续接；空白页和扉页也要确认。不能以目录或自动提取文本代替原页核对。
- [x] 所有内容保持原书次序、标题层级、段落、列表、图注、表题、公式编号、代码、习题、书目与交叉引用；译文与每章中文导读明确区分。
- [x] 图内英文逐项翻译并保留图形信息；表格逐单元格复核；公式、变量、上下标和编号逐项复核。网页内检查复制、窄屏与深色模式。
- [x] 每章由未承担该章初译的 Agent 对照 PDF 独立审查，记录问题、修复并复核后，方可勾选该章完成。已有译稿也须重新核对。
- [x] 全书完成后，再由独立 Agent 做跨章术语、符号、编号、引用、目录、阅读进度和站点整体复核。

## 前置页（PDF 第 1–22 页）

- [x] PDF 1–22：逐页视觉核对与中文初译已落入 frontmatter/page-01.md–page-22.md；跨页段落归起始页，目录逐项附中文标题，记号表逐行初核。
- [x] PDF 1–6：系列页、书名页、版权/出版信息、献词及空白页，逐页核对并按站点编排。
- [x] PDF 7–12（书页 vii–xii）：目录 171 项（含 166 条编号节/小节），与原页及站点列表逐项核对。
- [x] PDF 7–12：全书章节与小节全部上架后，191 个目录跳转链接逐项核对并独立复审通过；见 `REVIEW-FRONTMATTER-TOC-LINKS.md`。
- [x] PDF 13–16（书页 xiii–xvi）：第二版前言，完整翻译与核对。
- [x] PDF 17–18（书页 xvii–xviii）：第一版前言，完整翻译与核对。
- [x] PDF 19–22（书页 xix–xxii）：记号表 116 行，逐条核对数学符号、上下标、解释及排版。
- [x] 前置页独立复审并修复问题（REVIEW-FRONTMATTER.md）。

### 第 1 章 Introduction（书页 1–22；PDF 23–44）

- [x] 中文导读：初稿、原页自查与独立审查通过（REVIEW-CH1.md）。
- [x] 1.1 Reinforcement Learning：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.2 Examples：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.3 Elements of Reinforcement Learning：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.4 Limitations and Scope：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.5 An Extended Example: Tic-Tac-Toe：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.6 Summary：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 1.7 Early History of Reinforcement Learning：初译、原页逐段核对与独立审查通过（REVIEW-CH1.md）。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

## 第一部分：表格型方法（Tabular Solution Methods）

- [x] PDF 45–46（书页 23–24）：部分扉页及引言/空白页，逐页核对并编排；独立审查发现的一处漏译已修复并复核。

### 第 2 章 Multi-armed Bandits（书页 25–46；PDF 47–68）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 2.1 A k-armed Bandit Problem：对照原页完成逐段译文与核对。
- [x] 2.2 Action-value Methods：对照原页完成逐段译文与核对。
- [x] 2.3 The 10-armed Testbed：对照原页完成逐段译文与核对。
- [x] 2.4 Incremental Implementation：对照原页完成逐段译文与核对。
- [x] 2.5 Tracking a Nonstationary Problem：对照原页完成逐段译文与核对。
- [x] 2.6 Optimistic Initial Values：对照原页完成逐段译文与核对。
- [x] 2.7 Upper-Confidence-Bound Action Selection：对照原页完成逐段译文与核对。
- [x] 2.8 Gradient Bandit Algorithms：对照原页完成逐段译文与核对。
- [x] 2.9 Associative Search (Contextual Bandits)：对照原页完成逐段译文与核对。
- [x] 2.10 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核（REVIEW-CH2.md）。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 3 章 Finite Markov Decision Processes（书页 47–72；PDF 69–94）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 3.1 The Agent–Environment Interface：对照原页完成逐段译文与核对。
- [x] 3.2 Goals and Rewards：对照原页完成逐段译文与核对。
- [x] 3.3 Returns and Episodes：对照原页完成逐段译文与核对。
- [x] 3.4 Unified Notation for Episodic and Continuing Tasks：对照原页完成逐段译文与核对。
- [x] 3.5 Policies and Value Functions：对照原页完成逐段译文与核对。
- [x] 3.6 Optimal Policies and Optimal Value Functions：对照原页完成逐段译文与核对。
- [x] 3.7 Optimality and Approximation：对照原页完成逐段译文与核对。
- [x] 3.8 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 4 章 Dynamic Programming（书页 73–90；PDF 95–112）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 4.1 Policy Evaluation (Prediction)：对照原页完成逐段译文与核对。
- [x] 4.2 Policy Improvement：对照原页完成逐段译文与核对。
- [x] 4.3 Policy Iteration：对照原页完成逐段译文与核对。
- [x] 4.4 Value Iteration：对照原页完成逐段译文与核对。
- [x] 4.5 Asynchronous Dynamic Programming：对照原页完成逐段译文与核对。
- [x] 4.6 Generalized Policy Iteration：对照原页完成逐段译文与核对。
- [x] 4.7 Efficiency of Dynamic Programming：对照原页完成逐段译文与核对。
- [x] 4.8 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 5 章 Monte Carlo Methods（书页 91–118；PDF 113–140）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 5.1 Monte Carlo Prediction：对照原页完成逐段译文与核对。
- [x] 5.2 Monte Carlo Estimation of Action Values：对照原页完成逐段译文与核对。
- [x] 5.3 Monte Carlo Control：对照原页完成逐段译文与核对。
- [x] 5.4 Monte Carlo Control without Exploring Starts：对照原页完成逐段译文与核对。
- [x] 5.5 Off-policy Prediction via Importance Sampling：对照原页完成逐段译文与核对。
- [x] 5.6 Incremental Implementation：对照原页完成逐段译文与核对。
- [x] 5.7 Off-policy Monte Carlo Control：对照原页完成逐段译文与核对。
- [x] 5.8 *Discounting-aware Importance Sampling：对照原页完成逐段译文与核对。
- [x] 5.9 *Per-decision Importance Sampling：对照原页完成逐段译文与核对。
- [x] 5.10 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 6 章 Temporal-Difference Learning（书页 119–140；PDF 141–162）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 6.1 TD Prediction：对照原页完成逐段译文与核对。
- [x] 6.2 Advantages of TD Prediction Methods：对照原页完成逐段译文与核对。
- [x] 6.3 Optimality of TD(0)：对照原页完成逐段译文与核对。
- [x] 6.4 Sarsa: On-policy TD Control：对照原页完成逐段译文与核对。
- [x] 6.5 Q-learning: Off-policy TD Control：对照原页完成逐段译文与核对。
- [x] 6.6 Expected Sarsa：对照原页完成逐段译文与核对。
- [x] 6.7 Maximization Bias and Double Learning：对照原页完成逐段译文与核对。
- [x] 6.8 Games, Afterstates, and Other Special Cases：对照原页完成逐段译文与核对。
- [x] 6.9 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 7 章 n-step Bootstrapping（书页 141–158；PDF 163–180）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 7.1 n-step TD Prediction：对照原页完成逐段译文与核对。
- [x] 7.2 n-step Sarsa：对照原页完成逐段译文与核对。
- [x] 7.3 n-step Off-policy Learning：对照原页完成逐段译文与核对。
- [x] 7.4 *Per-decision Methods with Control Variates：对照原页完成逐段译文与核对。
- [x] 7.5 Off-policy Learning Without Importance Sampling: The n-step Tree Backup Algorithm：对照原页完成逐段译文与核对。
- [x] 7.6 *A Unifying Algorithm: n-step Q(σ)：对照原页完成逐段译文与核对。
- [x] 7.7 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 8 章 Planning and Learning with Tabular Methods（书页 159–194；PDF 181–216）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 8.1 Models and Planning：对照原页完成逐段译文与核对。
- [x] 8.2 Dyna: Integrated Planning, Acting, and Learning：对照原页完成逐段译文与核对。
- [x] 8.3 When the Model Is Wrong：对照原页完成逐段译文与核对。
- [x] 8.4 Prioritized Sweeping：对照原页完成逐段译文与核对。
- [x] 8.5 Expected vs. Sample Updates：对照原页完成逐段译文与核对。
- [x] 8.6 Trajectory Sampling：对照原页完成逐段译文与核对。
- [x] 8.7 Real-time Dynamic Programming：对照原页完成逐段译文与核对。
- [x] 8.8 Planning at Decision Time：对照原页完成逐段译文与核对。
- [x] 8.9 Heuristic Search：对照原页完成逐段译文与核对。
- [x] 8.10 Rollout Algorithms：对照原页完成逐段译文与核对。
- [x] 8.11 Monte Carlo Tree Search：对照原页完成逐段译文与核对。
- [x] 8.12 Summary of the Chapter：对照原页完成逐段译文与核对。
- [x] 8.13 Summary of Part I: Dimensions：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

## 第二部分：近似解法（Approximate Solution Methods）

- [x] PDF 217–218（书页 195–196）：部分扉页及引言/空白页，逐页核对并编排。

### 第 9 章 On-policy Prediction with Approximation（书页 197–242；PDF 219–264）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 9.1 Value-function Approximation：对照原页完成逐段译文与核对。
- [x] 9.2 The Prediction Objective (上划线 VE)：对照原页完成逐段译文与核对。
- [x] 9.3 Stochastic-gradient and Semi-gradient Methods：对照原页完成逐段译文与核对。
- [x] 9.4 Linear Methods：对照原页完成逐段译文与核对。
- [x] 9.5 Feature Construction for Linear Methods：对照原页完成逐段译文与核对。
  - [x] 9.5.1 Polynomials：对照原页完成逐段译文与核对。
  - [x] 9.5.2 Fourier Basis：对照原页完成逐段译文与核对。
  - [x] 9.5.3 Coarse Coding：对照原页完成逐段译文与核对。
  - [x] 9.5.4 Tile Coding：对照原页完成逐段译文与核对。
  - [x] 9.5.5 Radial Basis Functions：对照原页完成逐段译文与核对。
- [x] 9.6 Selecting Step-Size Parameters Manually：对照原页完成逐段译文与核对。
- [x] 9.7 Nonlinear Function Approximation: Artificial Neural Networks：对照原页完成逐段译文与核对。
- [x] 9.8 Least-Squares TD：对照原页完成逐段译文与核对。
- [x] 9.9 Memory-based Function Approximation：对照原页完成逐段译文与核对。
- [x] 9.10 Kernel-based Function Approximation：对照原页完成逐段译文与核对。
- [x] 9.11 Looking Deeper at On-policy Learning: Interest and Emphasis：对照原页完成逐段译文与核对。
- [x] 9.12 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 10 章 On-policy Control with Approximation（书页 243–256；PDF 265–278）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 10.1 Episodic Semi-gradient Control：对照原页完成逐段译文与核对。
- [x] 10.2 Semi-gradient n-step Sarsa：对照原页完成逐段译文与核对。
- [x] 10.3 Average Reward: A New Problem Setting for Continuing Tasks：对照原页完成逐段译文与核对。
- [x] 10.4 Deprecating the Discounted Setting：对照原页完成逐段译文与核对。
- [x] 10.5 Differential Semi-gradient n-step Sarsa：对照原页完成逐段译文与核对。
- [x] 10.6 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 11 章 *Off-policy Methods with Approximation（书页 257–286；PDF 279–308）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 11.1 Semi-gradient Methods：对照原页完成逐段译文与核对。
- [x] 11.2 Examples of Off-policy Divergence：对照原页完成逐段译文与核对。
- [x] 11.3 The Deadly Triad：对照原页完成逐段译文与核对。
- [x] 11.4 Linear Value-function Geometry：对照原页完成逐段译文与核对。
- [x] 11.5 Gradient Descent in the Bellman Error：对照原页完成逐段译文与核对。
- [x] 11.6 The Bellman Error is Not Learnable：对照原页完成逐段译文与核对。
- [x] 11.7 Gradient-TD Methods：对照原页完成逐段译文与核对。
- [x] 11.8 Emphatic-TD Methods：对照原页完成逐段译文与核对。
- [x] 11.9 Reducing Variance：对照原页完成逐段译文与核对。
- [x] 11.10 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 12 章 Eligibility Traces（书页 287–320；PDF 309–342）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 12.1 The λ-return：对照原页完成逐段译文与核对。
- [x] 12.2 TD(λ)：对照原页完成逐段译文与核对。
- [x] 12.3 n-step Truncated λ-return Methods：对照原页完成逐段译文与核对。
- [x] 12.4 Redoing Updates: Online λ-return Algorithm：对照原页完成逐段译文与核对。
- [x] 12.5 True Online TD(λ)：对照原页完成逐段译文与核对。
- [x] 12.6 *Dutch Traces in Monte Carlo Learning：对照原页完成逐段译文与核对。
- [x] 12.7 Sarsa(λ)：对照原页完成逐段译文与核对。
- [x] 12.8 Variable λ and γ：对照原页完成逐段译文与核对。
- [x] 12.9 Off-policy Traces with Control Variates：对照原页完成逐段译文与核对。
- [x] 12.10 Watkins’s Q(λ) to Tree-Backup(λ)：对照原页完成逐段译文与核对。
- [x] 12.11 Stable Off-policy Methods with Traces：对照原页完成逐段译文与核对。
- [x] 12.12 Implementation Issues：对照原页完成逐段译文与核对。
- [x] 12.13 Conclusions：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 13 章 Policy Gradient Methods（书页 321–338；PDF 343–360）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 13.1 Policy Approximation and its Advantages：对照原页完成逐段译文与核对。
- [x] 13.2 The Policy Gradient Theorem：对照原页完成逐段译文与核对。
- [x] 13.3 REINFORCE: Monte Carlo Policy Gradient：对照原页完成逐段译文与核对。
- [x] 13.4 REINFORCE with Baseline：对照原页完成逐段译文与核对。
- [x] 13.5 Actor–Critic Methods：对照原页完成逐段译文与核对。
- [x] 13.6 Policy Gradient for Continuing Problems：对照原页完成逐段译文与核对。
- [x] 13.7 Policy Parameterization for Continuous Actions：对照原页完成逐段译文与核对。
- [x] 13.8 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

## 第三部分：深入探讨（Looking Deeper）

- [x] PDF 361–362（书页 339–340）：部分扉页及引言/空白页，逐页核对并编排；源稿 `parts/part-03.md`，阅读器数据 `chapter-III.json`，已加入书架。

### 第 14 章 Psychology（书页 341–376；PDF 363–398）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 14.1 Prediction and Control：对照原页完成逐段译文与核对。
- [x] 14.2 Classical Conditioning：对照原页完成逐段译文与核对。
  - [x] 14.2.1 Blocking and Higher-order Conditioning：对照原页完成逐段译文与核对。
  - [x] 14.2.2 The Rescorla–Wagner Model：对照原页完成逐段译文与核对。
  - [x] 14.2.3 The TD Model：对照原页完成逐段译文与核对。
  - [x] 14.2.4 TD Model Simulations：对照原页完成逐段译文与核对。
- [x] 14.3 Instrumental Conditioning：对照原页完成逐段译文与核对。
- [x] 14.4 Delayed Reinforcement：对照原页完成逐段译文与核对。
- [x] 14.5 Cognitive Maps：对照原页完成逐段译文与核对。
- [x] 14.6 Habitual and Goal-directed Behavior：对照原页完成逐段译文与核对。
- [x] 14.7 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 15 章 Neuroscience（书页 377–420；PDF 399–442）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 15.1 Neuroscience Basics：对照原页完成逐段译文与核对。
- [x] 15.2 Reward Signals, Reinforcement Signals, Values, and Prediction Errors：对照原页完成逐段译文与核对。
- [x] 15.3 The Reward Prediction Error Hypothesis：对照原页完成逐段译文与核对。
- [x] 15.4 Dopamine：对照原页完成逐段译文与核对。
- [x] 15.5 Experimental Support for the Reward Prediction Error Hypothesis：对照原页完成逐段译文与核对。
- [x] 15.6 TD Error/Dopamine Correspondence：对照原页完成逐段译文与核对。
- [x] 15.7 Neural Actor–Critic：对照原页完成逐段译文与核对。
- [x] 15.8 Actor and Critic Learning Rules：对照原页完成逐段译文与核对。
- [x] 15.9 Hedonistic Neurons：对照原页完成逐段译文与核对。
- [x] 15.10 Collective Reinforcement Learning：对照原页完成逐段译文与核对。
- [x] 15.11 Model-based Methods in the Brain：对照原页完成逐段译文与核对。
- [x] 15.12 Addiction：对照原页完成逐段译文与核对。
- [x] 15.13 Summary：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 16 章 Applications and Case Studies（书页 421–458；PDF 443–480）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 16.1 TD-Gammon：对照原页完成逐段译文与核对。
- [x] 16.2 Samuel’s Checkers Player：对照原页完成逐段译文与核对。
- [x] 16.3 Watson’s Daily-Double Wagering：对照原页完成逐段译文与核对。
- [x] 16.4 Optimizing Memory Control：对照原页完成逐段译文与核对。
- [x] 16.5 Human-level Video Game Play：对照原页完成逐段译文与核对。
- [x] 16.6 Mastering the Game of Go：对照原页完成逐段译文与核对。
  - [x] 16.6.1 AlphaGo：对照原页完成逐段译文与核对。
  - [x] 16.6.2 AlphaGo Zero：对照原页完成逐段译文与核对。
- [x] 16.7 Personalized Web Services：对照原页完成逐段译文与核对。
- [x] 16.8 Thermal Soaring：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

### 第 17 章 Frontiers（书页 459–480；PDF 481–502）

- [x] 中文导读：简短、准确，与原书译文清楚区分。
- [x] 17.1 General Value Functions and Auxiliary Tasks：对照原页完成逐段译文与核对。
- [x] 17.2 Temporal Abstraction via Options：对照原页完成逐段译文与核对。
- [x] 17.3 Observations and State：对照原页完成逐段译文与核对。
- [x] 17.4 Designing Reward Signals：对照原页完成逐段译文与核对。
- [x] 17.5 Remaining Issues：对照原页完成逐段译文与核对。
- [x] 17.6 Reinforcement Learning and the Future of Artificial Intelligence：对照原页完成逐段译文与核对。
- [x] 本章未列入目录的正文、示例、练习、脚注、书目与历史说明逐页核对；不因目录未列而跳过。
- [x] 本章全部图片/图内文字/图注、表格各单元格及编号逐一核对并完成中文编排。
- [x] 本章全部公式、变量、上下标、编号、伪代码/代码与交叉引用逐一核对。
- [x] 本章网页排版：桌面、窄屏、深色模式及公式复制性检查。
- [x] 独立 Agent 对照 PDF 审查完整性、语义、术语、图表、公式、代码和排版；问题记录、修复、复核。
- [x] 本章完成：上述事项全部勾选，且无未解决问题。

## 书后内容（PDF 第 503–548 页）

- [x] PDF 503–540（书页 481–518）：References，逐条保留作者、年份、标题、出版信息与正文引用对应关系；两段独立审查均通过。
- [x] PDF 541–546（书页 519–524）：Index，逐条核对索引词、页码与网站检索/链接的编排方式，保留原书斜体与粗体页码的含义；独立审查通过。
- [x] PDF 547–548（书页 525–526）：Adaptive Computation and Machine Learning 系列书目，24 项书名与作者已核对、译编并独立审查通过。
- [x] 复核 PDF 全部 548 页是否另有目录未列的附录、勘误或补充内容；末尾两页系列书目已纳入；`PAGE-AUDIT.csv` 连续覆盖 548 页。
- [x] 书后内容独立复审并修复问题；参考文献、索引与系列书目的独立审查均通过。

## 全书验收

- [x] PDF 1–548 页连续覆盖核查，无未登记的物理页；每章与前后置材料的审查结论可追溯；见 `PAGE-AUDIT.md` 与 `PAGE-AUDIT.csv`。
- [x] 全书术语表统一：policy、value function、return、reward、state、action、on-policy、off-policy、bootstrapping、eligibility trace 等首次出现时可附英文。
- [x] 全书符号、公式编号、图表编号、习题编号及跨章引用链接核对。
- [x] 全书导读风格、目录层级、阅读进度和站点显示（桌面/移动端/深色模式）核对。
- [x] 独立 Agent 完成全书整体 review，逐条记录并修复问题。
- [x] 最终完成：全部任务项和审查项勾选，无缺页、缺图、缺表、缺公式或未解决问题。

## 阅读功能改进（2026-10-03）

- [x] 建立 156 张图片的离线清单，阅读时预取并显示完成状态；全部章节及引用索引列入首次离线缓存。
- [x] 建立章节、部分、小节、图、表、公式、习题和示例的编号目标索引，并在正文中生成可点击的站内跳转。
- [x] 全新浏览器缓存中，预取完成后断网打开未访问的第 16 章，再跳到未访问的第 9 章；两处原图、正文与引用索引均可离线加载。移动端交叉引用跳转测试通过；见 `scripts/qa_sutton_reader_features.py`。
