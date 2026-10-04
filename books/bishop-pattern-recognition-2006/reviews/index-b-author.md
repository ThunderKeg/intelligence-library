# 索引后半部作者核对记录

## 范围与状态

- 负责 PDF 物理页 753–758（印刷页 733–738），从 Hooke’s law 至 Yellowstone National Park。
- 唯一译稿为 translation/parts/index-b.md。未修改另一分片、共享索引工具、组装后的 Markdown/JSON、站点文件或任务清单。
- 已亲自逐页查看仓库原 PDF 的完整页面渲染，按每页左栏、右栏顺序逐项译写；另查看 752 页确认分片接口。原页截图为 tmp/prml-source/b-page-752.png 至 b-page-758.png。
- 477 项全部初译并完成作者自检：415 个主条、62 个子条，54 处参见关系，103 个粗体页码。
- 独立审查由未承担初译的 reviewer 进行；本记录不代替整段及整站验收。

## 逐页检查

| PDF 页 | 主条 | 子条 | 合计 | 粗体页码 | 参见 | 核对范围 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 753 | 79 | 6 | 85 | 20 | 10 | Hooke’s law 至 latent variable；两个独立同分布条目、IRLS、核函数子项 |
| 754 | 70 | 20 | 90 | 15 | 12 | lattice diagram 至 Metropolis-Hastings algorithm；线性回归、马尔可夫模型、消息传递子项 |
| 755 | 79 | 9 | 88 | 25 | 11 | microstate 至 perfect map；混合模型、神经网络、感知机子项 |
| 756 | 69 | 19 | 88 | 19 | 4 | periodic variable 至 scale invariance；PCA、先验、概率跨栏子项 |
| 757 | 82 | 4 | 86 | 14 | 10 | scale parameter 至 treewidth；统计学习理论参见与页码并存，和积算法与 SVM 子项 |
| 758 | 36 | 4 | 40 | 10 | 7 | trellis diagram 至 Yellowstone National Park；变分推断与权重共享子项 |
| 总计 | 415 | 62 | 477 | 103 | 54 | 六页全部条目 |

每项均核对英文词条、中文译名、源排序、主条/子条关系、所有页码、页码字重及参见目标。源页没有图片、表格、脚注、习题或显示公式。758 页仅右栏为空，左栏 40 项完整保留。

## 结构与术语

- 使用 index-entry 和 index-subentry；子项 key 为“英文父条::英文子条”。中文译名后保留源英文，不重新按中文排序，不合并重复含义或别名条目。
- 原印刷页码仅置于 index-pages，原粗体数字保留为 strong。753 的三个 K 及 755 的 ν 使用 em 与 Unicode，源英文不转为图片或不可检索公式。
- 754 的 machine learning、755 的 pattern recognition 保留罗马页码 vii。
- 756 右栏首 sum rule/theory 仍为 probability 的子项。757 的 statistical learning theory 保留参见 computational learning theory，随后仍保留页码 326、344。
- 所有 see 目标均以 data-index-see 标识；与 a 片合并进行只读检查，全部 54 个本片参见目标存在，整个索引 key 没有重复。
- 与 a 协调 intensive/extensive variables：分别译为“数量固定的变量”“数量随数据集增长的变量”，沿第 10 章的具体解释。
- 沿全书采用雅可比矩阵、非正常先验、不起作用的约束、逻辑回归、主成分分析、序贯最小优化、切向传播、跳层连接、马氏距离、缠绕分布等用语。logistic sigmoid、Ising、Jensen 等按已验收正文保留英文名称。
- lattice diagram 与 trellis diagram 均沿第 8 章首次定义译“格图”。已将第 13 章 a 稿“格架图”的异形通知 root，由全书审查协调处理。

## 原印细节及作者自检调整

1. 753 页右栏主条实印 **iterative reweighted least squares**，含 re；与左栏 IRLS 的参见目标一致。原页 4 倍局部图 b-index-753-irls.png 已亲自查看。未沿辅助基线误写成 iterative weighted least squares。
2. 753 页的 independent identically distributed 与 independent, identically distributed 是两条不同原条，均保留；页码分别为粗体 26、379 与 605。
3. Karhunen-Loève 的 è 是组合排印的重音，已亲自查看 4 倍 b-index-karhunen.png 并保留正确可检索字符。自动提取时单独出现的重音符号不作为额外的词内标点。
4. 756 页确为 protected conjugate gradients；与已验收第 7 章保留的原词相同。保留英文，未擅改成 projected conjugate gradients。4 倍局部图 b-index-protected.png 已亲自查看。
5. 757 页确为 Shur complement，缺 c。中文仍为已定义的“舒尔补”，英文按此原印保留，不静默修成 Schur。4 倍局部图 b-index-shur.png 已亲自查看。
6. 757 页 Student’s t-distribution 的 t 源页为正体。作者末轮查看原页 4 倍 b-index-student.png 并核字体后，移除了该条中初译多加的两个 em；中文、英文、页码、字重及 metadata 均未改变。这是完整初译交接后唯一自检调整。
7. 原页 source key、页码、粗体和层级经只读辅助脚本 tmp/prml-source/b-index-check.py 再次比对，477/477 项一致，0 项差异。工具仅辅助作者逐项自检，未替代实际原页阅读或独立审查。源码里的 ID3 数字及组合重音均已单独处理，避免错误计作页码或字母差异。

## 最终指纹

- translation/parts/index-b.md raw SHA-256：f41a736308eefaa258d0624c66f816ab66a08186a0cd26195d58e33d616e5df8
- LF 规范化 SHA-256：f41a736308eefaa258d0624c66f816ab66a08186a0cd26195d58e33d616e5df8
- 本片没有新增图片或数学公式资源。

## 独立审查修复 IB-01

2026-10-04，reviewer 在 PDF 758 / index-b.md 第 458 行指出 undetermined multiplier 的中文术语与附录 E 不一致。已仅将“待定乘子”改为“未定乘子”，沿附录 E 的两处定义和解释。源英文、data-index-key、参见目标与英文、页码、层级、strong/em 和所有标签保持逐字不变。精确差异保存于 tmp/prml-contents-final-b/index-b-IB01.diff；修订前源码快照同目录 index-b-before-IB01.md。以上最终指纹已更新；本修改等待 reviewer 独立差异复核，不自行视为索引整体验收。

## 逐项字段核对清单

以下清单记录每项原英文 key、原页码、粗体数字及参见目标，均已与实际原页核对。子项 key 中的 :: 仅用于记录所属主条，不是增加到读者可见原文的文字。

### PDF 753

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | Hooke’s law | 580 | — | — |
| 2 | hybrid Monte Carlo | 548 | — | — |
| 3 | hyperparameter | 71, 280, 311, 346, 372, 502 | 71 | — |
| 4 | hyperprior | 372 | — | — |
| 5 | I map | — | — | independence map |
| 6 | i.i.d. | — | — | independent identically distributed |
| 7 | ICA | — | — | independent component analysis |
| 8 | ICM | — | — | iterated conditional modes |
| 9 | ID3 | 663 | — | — |
| 10 | identifiability | 435 | — | — |
| 11 | image de-noising | 387 | — | — |
| 12 | importance sampling | 525, 532 | 532 | — |
| 13 | importance weights | 533 | — | — |
| 14 | improper prior | 118, 259, 472 | 118 | — |
| 15 | imputation step | 537 | — | — |
| 16 | imputation-posterior algorithm | 537 | — | — |
| 17 | inactive constraint | 328, 709 | 709 | — |
| 18 | incomplete data set | 440 | — | — |
| 19 | independence map | 392 | — | — |
| 20 | independent component analysis | 591 | — | — |
| 21 | independent factor analysis | 592 | — | — |
| 22 | independent identically distributed | 26, 379 | 26 | — |
| 23 | independent variables | 17 | — | — |
| 24 | independent, identically distributed | 605 | — | — |
| 25 | induced factorization | 485 | — | — |
| 26 | inequality constraint | 709 | — | — |
| 27 | inference | 38, 42 | 42 | — |
| 28 | information criterion | 33 | — | — |
| 29 | information geometry | 298 | — | — |
| 30 | information theory | 48 | — | — |
| 31 | input-output hidden Markov model | 633 | — | — |
| 32 | intensive variables | 490 | — | — |
| 33 | intrinsic dimensionality | 559 | — | — |
| 34 | invariance | 261 | — | — |
| 35 | inverse gamma distribution | 101 | — | — |
| 36 | inverse kinematics | 272 | — | — |
| 37 | inverse problem | 272 | — | — |
| 38 | inverse Wishart distribution | 102 | — | — |
| 39 | IP algorithm | — | — | imputation-posterior algorithm |
| 40 | IRLS | — | — | iterative reweighted least squares |
| 41 | Ising model | 389 | — | — |
| 42 | isomap | 596 | — | — |
| 43 | isometric feature map | 596 | — | — |
| 44 | iterated conditional modes | 389, 415 | 389 | — |
| 45 | iterative reweighted least squares | 207, 210, 316, 354, 672 | 207 | — |
| 46 | Jacobian matrix | 247, 264 | 247 | — |
| 47 | Jensen’s inequality | 56 | — | — |
| 48 | join tree | 416 | — | — |
| 49 | junction tree algorithm | 392, 416 | 416 | — |
| 50 | K nearest neighbours | 125 | — | — |
| 51 | K-means clustering algorithm | 424, 443 | 424 | — |
| 52 | K-medoids algorithm | 428 | — | — |
| 53 | Kalman filter | 304, 637 | 637 | — |
| 54 | Kalman filter::extended | 644 | — | — |
| 55 | Kalman gain matrix | 639 | — | — |
| 56 | Kalman smoother | 637 | — | — |
| 57 | Karhunen-Loève transform | 561 | — | — |
| 58 | Karush-Kuhn-Tucker conditions | 330, 333, 342, 710 | 710 | — |
| 59 | kernel density estimator | 122, 326 | 122 | — |
| 60 | kernel function | 123, 292, 294 | 292 | — |
| 61 | kernel function::Fisher | 298 | — | — |
| 62 | kernel function::Gaussian | 296 | — | — |
| 63 | kernel function::homogeneous | 292 | — | — |
| 64 | kernel function::nonvectorial inputs | 297 | — | — |
| 65 | kernel function::stationary | 292 | — | — |
| 66 | kernel PCA | 586 | — | — |
| 67 | kernel regression | 300, 302 | 302 | — |
| 68 | kernel substitution | 292 | — | — |
| 69 | kernel trick | 292 | — | — |
| 70 | kinetic energy | 549 | — | — |
| 71 | KKT | — | — | Karush-Kuhn-Tucker conditions |
| 72 | KL divergence | — | — | Kullback-Leibler divergence |
| 73 | kriging | — | — | Gaussian process |
| 74 | Kullback-Leibler divergence | 55, 451, 468, 505 | 55 | — |
| 75 | Lagrange multiplier | 707 | — | — |
| 76 | Lagrange, Joseph-Louis | 329 | — | — |
| 77 | Lagrangian | 328, 332, 341, 708 | 708 | — |
| 78 | laminar flow | 678 | — | — |
| 79 | Laplace approximation | 213, 217, 278, 315, 354 | 213 | — |
| 80 | Laplace, Pierre-Simon | 24 | — | — |
| 81 | large margin | — | — | margin |
| 82 | lasso | 145 | — | — |
| 83 | latent class analysis | 444 | — | — |
| 84 | latent trait model | 597 | — | — |
| 85 | latent variable | 84, 364, 430, 559 | 364 | — |

### PDF 754

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | lattice diagram | 414, 611, 621, 629 | 414 | — |
| 2 | LDS | — | — | linear dynamical system |
| 3 | leapfrog discretization | 551 | — | — |
| 4 | learning | 2 | — | — |
| 5 | learning rate parameter | 240 | — | — |
| 6 | least-mean-squares algorithm | 144 | — | — |
| 7 | leave-one-out | 33 | — | — |
| 8 | likelihood function | 22 | — | — |
| 9 | likelihood weighted sampling | 534 | — | — |
| 10 | linear discriminant | 181 | — | — |
| 11 | linear discriminant::Fisher | 186 | — | — |
| 12 | linear dynamical system | 84, 635 | 635 | — |
| 13 | linear dynamical system::inference | 638 | — | — |
| 14 | linear independence | 696 | — | — |
| 15 | linear regression | 138 | — | — |
| 16 | linear regression::EM | 448 | — | — |
| 17 | linear regression::mixture model | 667 | — | — |
| 18 | linear regression::variational | 486 | — | — |
| 19 | linear smoother | 159 | — | — |
| 20 | linear-Gaussian model | 87, 370 | 370 | — |
| 21 | linearly separable | 179 | — | — |
| 22 | link | 360 | — | — |
| 23 | link function | 180, 213 | — | — |
| 24 | Liouville’s Theorem | 550 | — | — |
| 25 | LLE | — | — | locally linear embedding |
| 26 | LMS algorithm | — | — | least-mean-squares algorithm |
| 27 | local minimum | 237 | — | — |
| 28 | local receptive field | 268 | — | — |
| 29 | locally linear embedding | 596 | — | — |
| 30 | location parameter | 118 | — | — |
| 31 | log odds | 197 | — | — |
| 32 | logic sampling | 525 | — | — |
| 33 | logistic regression | 205, 336 | 205 | — |
| 34 | logistic regression::Bayesian | 217, 498 | — | — |
| 35 | logistic regression::mixture model | 670 | — | — |
| 36 | logistic regression::multiclass | 209 | — | — |
| 37 | logistic sigmoid | 114, 139, 197, 205, 220, 227, 495 | 197 | — |
| 38 | logit function | 197 | — | — |
| 39 | loopy belief propagation | 417 | — | — |
| 40 | loss function | 41 | — | — |
| 41 | loss matrix | 41 | — | — |
| 42 | lossless data compression | 429 | — | — |
| 43 | lossy data compression | 429 | — | — |
| 44 | lower bound | 484 | — | — |
| 45 | M step | — | — | maximization step |
| 46 | machine learning | vii | — | — |
| 47 | macrostate | 51 | — | — |
| 48 | Mahalanobis distance | 80 | — | — |
| 49 | manifold | 38, 590, 595, 681 | 38 | — |
| 50 | MAP | — | — | maximum posterior |
| 51 | margin | 326, 327, 502 | 327 | — |
| 52 | margin::error | 334 | — | — |
| 53 | margin::soft | 332 | — | — |
| 54 | marginal likelihood | 162, 165 | 162 | — |
| 55 | marginal probability | 14 | — | — |
| 56 | Markov blanket | 382, 384, 545 | 382 | — |
| 57 | Markov boundary | — | — | Markov blanket |
| 58 | Markov chain | 397, 539 | 539 | — |
| 59 | Markov chain::first order | 607 | — | — |
| 60 | Markov chain::homogeneous | 540, 608 | 540 | — |
| 61 | Markov chain::second order | 608 | — | — |
| 62 | Markov chain Monte Carlo | 537 | — | — |
| 63 | Markov model | 607 | — | — |
| 64 | Markov model::homogeneous | 612 | — | — |
| 65 | Markov network | — | — | Markov random field |
| 66 | Markov random field | 84, 360, 383 | 383 | — |
| 67 | max-sum algorithm | 411, 629 | 411 | — |
| 68 | maximal clique | 385 | — | — |
| 69 | maximal spanning tree | 416 | — | — |
| 70 | maximization step | 437 | — | — |
| 71 | maximum likelihood | 9, 23, 26, 116 | 23 | — |
| 72 | maximum likelihood::Gaussian mixture | 432 | — | — |
| 73 | maximum likelihood::singularities | 480 | — | — |
| 74 | maximum likelihood::type 2 | — | — | evidence approximation |
| 75 | maximum margin | — | — | margin |
| 76 | maximum posterior | 30, 441 | 30 | — |
| 77 | MCMC | — | — | Markov chain Monte Carlo |
| 78 | MDN | — | — | mixture density network |
| 79 | MDS | — | — | multidimensional scaling |
| 80 | mean | 24 | — | — |
| 81 | mean field theory | 465 | — | — |
| 82 | mean value theorem | 52 | — | — |
| 83 | measure theory | 19 | — | — |
| 84 | memory-based methods | 292 | — | — |
| 85 | message passing | 396 | — | — |
| 86 | message passing::pending message | 417 | — | — |
| 87 | message passing::schedule | 417 | — | — |
| 88 | message passing::variational | 491 | — | — |
| 89 | Metropolis algorithm | 538 | — | — |
| 90 | Metropolis-Hastings algorithm | 541 | — | — |

### PDF 755

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | microstate | 51 | — | — |
| 2 | minimum risk | 44 | — | — |
| 3 | Minkowski loss | 48 | — | — |
| 4 | missing at random | 441, 579 | 441 | — |
| 5 | missing data | 579 | — | — |
| 6 | mixing coefficient | 111 | — | — |
| 7 | mixture component | 111 | — | — |
| 8 | mixture density network | 272, 673 | 272 | — |
| 9 | mixture distribution | — | — | mixture model |
| 10 | mixture model | 162, 423 | 423 | — |
| 11 | mixture model::conditional | 273, 666 | 666 | — |
| 12 | mixture model::linear regression | 667 | — | — |
| 13 | mixture model::logistic regression | 670 | — | — |
| 14 | mixture model::symmetries | 483 | — | — |
| 15 | mixture of experts | 672 | — | — |
| 16 | mixture of Gaussians | 110, 270, 273, 430 | 430 | — |
| 17 | MLP | — | — | multilayer perceptron |
| 18 | MNIST data | 677 | — | — |
| 19 | model comparison | 6, 32, 161, 473, 483 | 161 | — |
| 20 | model evidence | 161 | — | — |
| 21 | model selection | 162 | — | — |
| 22 | moment matching | 506, 510 | 506 | — |
| 23 | momentum variable | 548 | — | — |
| 24 | Monte Carlo EM algorithm | 536 | — | — |
| 25 | Monte Carlo sampling | 24, 523 | 523 | — |
| 26 | Moore-Penrose pseudo-inverse | — | — | pseudo-inverse |
| 27 | moralization | 391, 401 | 391 | — |
| 28 | MRF | — | — | Markov random field |
| 29 | multidimensional scaling | 596 | — | — |
| 30 | multilayer perceptron | 226, 229 | 229 | — |
| 31 | multimodality | 272 | — | — |
| 32 | multinomial distribution | 76, 114, 690 | 690 | — |
| 33 | multiplicity | 51 | — | — |
| 34 | mutual information | 55, 57 | 57 | — |
| 35 | Nadaraya-Watson | — | — | kernel regression |
| 36 | naive Bayes model | 46, 380 | 380 | — |
| 37 | nats | 50 | — | — |
| 38 | natural language modelling | 610 | — | — |
| 39 | natural parameters | 113 | — | — |
| 40 | nearest-neighbour methods | 124 | — | — |
| 41 | neural network | 225 | — | — |
| 42 | neural network::convolutional | 267 | — | — |
| 43 | neural network::regularization | 256 | — | — |
| 44 | neural network::relation to Gaussian process | 319 | — | — |
| 45 | Newton-Raphson | 207, 317 | 207 | — |
| 46 | node | 360 | — | — |
| 47 | noiseless coding theorem | 50 | — | — |
| 48 | nonidentifiability | 585 | — | — |
| 49 | noninformative prior | 23, 117 | 117 | — |
| 50 | nonparametric methods | 68, 120 | 120 | — |
| 51 | normal distribution | — | — | Gaussian |
| 52 | normal equations | 142 | — | — |
| 53 | normal-gamma distribution | 101, 691 | 101 | — |
| 54 | normal-Wishart distribution | 102, 475, 478, 691 | 102 | — |
| 55 | normalized exponential | — | — | softmax function |
| 56 | novelty detection | 44 | — | — |
| 57 | ν-SVM | 334 | — | — |
| 58 | object recognition | 366 | — | — |
| 59 | observed variable | 364 | — | — |
| 60 | Occam factor | 217 | — | — |
| 61 | oil flow data | 34, 560, 568, 678 | 678 | — |
| 62 | Old Faithful data | 110, 479, 484, 681 | 681 | — |
| 63 | on-line learning | — | — | sequential learning |
| 64 | one-versus-one classifier | 183, 339 | 183 | — |
| 65 | one-versus-the-rest classifier | 182, 338 | 182 | — |
| 66 | ordered over-relaxation | 545 | — | — |
| 67 | Ornstein-Uhlenbeck process | 305 | — | — |
| 68 | orthogonal least squares | 301 | — | — |
| 69 | outlier | 44, 185, 212 | — | — |
| 70 | outliers | 103 | 103 | — |
| 71 | over-fitting | 6, 147, 434, 464 | 6 | — |
| 72 | over-relaxation | 544 | — | — |
| 73 | PAC learning | — | — | probably approximately correct |
| 74 | PAC-Bayesian framework | 345 | — | — |
| 75 | parameter shrinkage | 144 | — | — |
| 76 | parent node | 361 | — | — |
| 77 | particle filter | 645 | — | — |
| 78 | partition function | 386, 554 | 386 | — |
| 79 | Parzen estimator | — | — | kernel density estimator |
| 80 | Parzen window | 123 | — | — |
| 81 | pattern recognition | vii | — | — |
| 82 | PCA | — | — | principal component analysis |
| 83 | pending message | 417 | — | — |
| 84 | perceptron | 192 | — | — |
| 85 | perceptron::convergence theorem | 194 | — | — |
| 86 | perceptron::hardware | 196 | — | — |
| 87 | perceptron criterion | 193 | — | — |
| 88 | perfect map | 392 | — | — |

### PDF 756

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | periodic variable | 105 | — | — |
| 2 | phase space | 549 | — | — |
| 3 | photon noise | 680 | — | — |
| 4 | plate | 363 | — | — |
| 5 | polynomial curve fitting | 4, 362 | — | — |
| 6 | polytree | 399 | — | — |
| 7 | position variable | 548 | — | — |
| 8 | positive definite covariance | 81 | — | — |
| 9 | positive definite matrix | 701 | — | — |
| 10 | positive semidefinite covariance | 81 | — | — |
| 11 | positive semidefinite matrix | 701 | — | — |
| 12 | posterior probability | 17 | — | — |
| 13 | posterior step | 537 | — | — |
| 14 | potential energy | 549 | — | — |
| 15 | potential function | 386 | — | — |
| 16 | power EP | 517 | — | — |
| 17 | power method | 563 | — | — |
| 18 | precision matrix | 85 | — | — |
| 19 | precision parameter | 24 | — | — |
| 20 | predictive distribution | 30, 156 | 30 | — |
| 21 | preprocessing | 2 | — | — |
| 22 | principal component analysis | 561, 572, 593 | 561 | — |
| 23 | principal component analysis::Bayesian | 580 | — | — |
| 24 | principal component analysis::EM algorithm | 577 | — | — |
| 25 | principal component analysis::Gibbs sampling | 583 | — | — |
| 26 | principal component analysis::mixture distribution | 595 | — | — |
| 27 | principal component analysis::physical analogy | 580 | — | — |
| 28 | principal curve | 595 | — | — |
| 29 | principal subspace | 561 | — | — |
| 30 | principal surface | 596 | — | — |
| 31 | prior | 17 | — | — |
| 32 | prior::conjugate | 68, 98, 117, 490 | 117 | — |
| 33 | prior::consistent | 257 | — | — |
| 34 | prior::improper | 118, 259, 472 | 118 | — |
| 35 | prior::noninformative | 23, 117 | 117 | — |
| 36 | probabilistic graphical model | — | — | graphical model |
| 37 | probabilistic PCA | 570 | — | — |
| 38 | probability | 12 | — | — |
| 39 | probability::Bayesian | 21 | — | — |
| 40 | probability::classical | 21 | — | — |
| 41 | probability::density | 17 | — | — |
| 42 | probability::frequentist | 21 | — | — |
| 43 | probability::mass function | 19 | — | — |
| 44 | probability::prior | 45 | — | — |
| 45 | probability::product rule | 13, 14, 359 | 14 | — |
| 46 | probability::sum rule | 13, 14, 359 | 14 | — |
| 47 | probability::theory | 12 | — | — |
| 48 | probably approximately correct | 344 | — | — |
| 49 | probit function | 211, 219 | 211 | — |
| 50 | probit regression | 210 | — | — |
| 51 | product rule of probability | 13, 14, 359 | 14 | — |
| 52 | proposal distribution | 528, 532, 538 | 528 | — |
| 53 | protected conjugate gradients | 335 | — | — |
| 54 | protein sequence | 610 | — | — |
| 55 | pseudo-inverse | 142, 185 | 142 | — |
| 56 | pseudo-random numbers | 526 | — | — |
| 57 | quadratic discriminant | 199 | — | — |
| 58 | quality parameter | 351 | — | — |
| 59 | radial basis function | 292, 299 | 299 | — |
| 60 | Rauch-Tung-Striebel equations | 637 | — | — |
| 61 | regression | 3 | — | — |
| 62 | regression function | 47, 95 | 47 | — |
| 63 | regularization | 10 | — | — |
| 64 | regularization::Tikhonov | 267 | — | — |
| 65 | regularized least squares | 144 | — | — |
| 66 | reinforcement learning | 3 | — | — |
| 67 | reject option | 42, 45 | 42 | — |
| 68 | rejection sampling | 528 | — | — |
| 69 | relative entropy | 55 | — | — |
| 70 | relevance vector | 348 | — | — |
| 71 | relevance vector machine | 161, 345 | 345 | — |
| 72 | responsibility | 112, 432, 477 | 432 | — |
| 73 | ridge regression | 10 | — | — |
| 74 | RMS error | — | — | root-mean-square error |
| 75 | Robbins-Monro algorithm | 95 | — | — |
| 76 | robot arm | 272 | — | — |
| 77 | robustness | 103, 185 | 103 | — |
| 78 | root node | 399 | — | — |
| 79 | root-mean-square error | 6 | — | — |
| 80 | Rosenblatt, Frank | 193 | — | — |
| 81 | rotation invariance | 573, 585 | 573 | — |
| 82 | RTS equations | — | — | Rauch-Tung-Striebel equations |
| 83 | running intersection property | 416 | — | — |
| 84 | RVM | — | — | relevance vector machine |
| 85 | sample mean | 27 | — | — |
| 86 | sample variance | 27 | — | — |
| 87 | sampling-importance-resampling | 534 | — | — |
| 88 | scale invariance | 119, 261 | 261 | — |

### PDF 757

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | scale parameter | 119 | — | — |
| 2 | scaling factor | 627 | — | — |
| 3 | Schwarz criterion | — | — | Bayesian information criterion |
| 4 | self-organizing map | 598 | — | — |
| 5 | sequential data | 605 | — | — |
| 6 | sequential estimation | 94 | — | — |
| 7 | sequential gradient descent | 144, 240 | — | — |
| 8 | sequential learning | 73, 143 | 73 | — |
| 9 | sequential minimal optimization | 335 | — | — |
| 10 | serial message passing schedule | 417 | — | — |
| 11 | Shannon, Claude | 55 | — | — |
| 12 | shared parameters | 368 | — | — |
| 13 | shrinkage | 10 | — | — |
| 14 | Shur complement | 87 | — | — |
| 15 | sigmoid | — | — | logistic sigmoid |
| 16 | simplex | 76 | — | — |
| 17 | single-class support vector machine | 339 | — | — |
| 18 | singular value decomposition | 143 | — | — |
| 19 | sinusoidal data | 682 | — | — |
| 20 | SIR | — | — | sampling-importance-resampling |
| 21 | skip-layer connection | 229 | — | — |
| 22 | slack variable | 331 | — | — |
| 23 | slice sampling | 546 | — | — |
| 24 | SMO | — | — | sequential minimal optimization |
| 25 | smoother matrix | 159 | — | — |
| 26 | smoothing parameter | 122 | — | — |
| 27 | soft margin | 332 | — | — |
| 28 | soft weight sharing | 269 | — | — |
| 29 | softmax function | 115, 198, 236, 274, 356, 497 | 198 | — |
| 30 | SOM | — | — | self-organizing map |
| 31 | sparsity | 145, 347, 349, 582 | 349 | — |
| 32 | sparsity parameter | 351 | — | — |
| 33 | spectrogram | 606 | — | — |
| 34 | speech recognition | 605, 610 | 605 | — |
| 35 | sphereing | 568 | — | — |
| 36 | spline functions | 139 | — | — |
| 37 | standard deviation | 24 | — | — |
| 38 | standardizing | 425, 567 | 567 | — |
| 39 | state space model | 609 | — | — |
| 40 | state space model::switching | 644 | — | — |
| 41 | stationary kernel | 292 | — | — |
| 42 | statistical bias | — | — | bias |
| 43 | statistical independence | — | — | independent variables |
| 44 | statistical learning theory | 326, 344 | — | computational learning theory |
| 45 | steepest descent | 240 | — | — |
| 46 | Stirling’s approximation | 51 | — | — |
| 47 | stochastic | 5 | — | — |
| 48 | stochastic EM | 536 | — | — |
| 49 | stochastic gradient descent | 144, 240 | — | — |
| 50 | stochastic process | 305 | — | — |
| 51 | stratified flow | 678 | — | — |
| 52 | Student’s t-distribution | 102, 483, 691 | 102 | — |
| 53 | subsampling | 268 | — | — |
| 54 | sufficient statistics | 69, 75, 116 | 116 | — |
| 55 | sum rule of probability | 13, 14, 359 | 14 | — |
| 56 | sum-of-squares error | 5, 29, 184, 232, 662 | 5 | — |
| 57 | sum-product algorithm | 399, 402 | 402 | — |
| 58 | sum-product algorithm::for hidden Markov model | 625 | — | — |
| 59 | supervised learning | 3 | — | — |
| 60 | support vector | 330 | — | — |
| 61 | support vector machine | 225 | — | — |
| 62 | support vector machine::for regression | 339 | — | — |
| 63 | support vector machine::multiclass | 338 | — | — |
| 64 | survival of the fittest | 646 | — | — |
| 65 | SVD | — | — | singular value decomposition |
| 66 | SVM | — | — | support vector machine |
| 67 | switching hidden Markov model | 644 | — | — |
| 68 | switching state space model | 644 | — | — |
| 69 | synthetic data sets | 682 | — | — |
| 70 | tail-to-tail path | 374 | — | — |
| 71 | tangent distance | 265 | — | — |
| 72 | tangent propagation | 262, 263 | 263 | — |
| 73 | tapped delay line | 609 | — | — |
| 74 | target vector | 2 | — | — |
| 75 | test set | 2, 32 | 32 | — |
| 76 | threshold parameter | 181 | — | — |
| 77 | tied parameters | 368 | — | — |
| 78 | Tikhonov regularization | 267 | — | — |
| 79 | time warping | 615 | — | — |
| 80 | tomography | 679 | — | — |
| 81 | training | 2 | — | — |
| 82 | training set | 2 | — | — |
| 83 | transition probability | 540, 610 | 540 | — |
| 84 | translation invariance | 118, 261 | 261 | — |
| 85 | tree-reweighted message passing | 517 | — | — |
| 86 | treewidth | 417 | — | — |

### PDF 758

| 序号 | 原英文 key | 页码 | 粗体页码 | 参见 |
| ---: | --- | --- | --- | --- |
| 1 | trellis diagram | — | — | lattice diagram |
| 2 | triangulated graph | 416 | — | — |
| 3 | type 2 maximum likelihood | — | — | evidence approximation |
| 4 | undetermined multiplier | — | — | Lagrange multiplier |
| 5 | undirected graph | — | — | Markov random field |
| 6 | uniform distribution | 692 | — | — |
| 7 | uniform sampling | 534 | — | — |
| 8 | uniquenesses | 584 | — | — |
| 9 | unobserved variable | — | — | latent variable |
| 10 | unsupervised learning | 3 | — | — |
| 11 | utility function | 41 | — | — |
| 12 | validation set | 11, 32 | 32 | — |
| 13 | Vapnik-Chervonenkis dimension | 344 | — | — |
| 14 | variance | 20, 24, 149 | 20 | — |
| 15 | variational inference | 315, 462, 635 | 462 | — |
| 16 | variational inference::for Gaussian mixture | 474 | — | — |
| 17 | variational inference::for hidden Markov model | 625 | — | — |
| 18 | variational inference::local | 493 | — | — |
| 19 | VC dimension | — | — | Vapnik-Chervonenkis dimension |
| 20 | vector quantization | 429 | — | — |
| 21 | vertex | — | — | node |
| 22 | visualization | 3 | — | — |
| 23 | Viterbi algorithm | 415, 629 | 629 | — |
| 24 | von Mises distribution | 108, 693 | 108 | — |
| 25 | wavelets | 139 | — | — |
| 26 | weak learner | 657 | — | — |
| 27 | weight decay | 10, 144, 257 | 144 | — |
| 28 | weight parameter | 227 | — | — |
| 29 | weight sharing | 268 | — | — |
| 30 | weight sharing::soft | 269 | — | — |
| 31 | weight vector | 181 | — | — |
| 32 | weight-space symmetry | 231, 281 | 231 | — |
| 33 | weighted least squares | 668 | — | — |
| 34 | well-determined parameters | 170 | — | — |
| 35 | whitening | 299, 568 | 568 | — |
| 36 | Wishart distribution | 102, 693 | 102 | — |
| 37 | within-class covariance | 189 | — | — |
| 38 | Woodbury identity | 696 | — | — |
| 39 | wrapped distribution | 110 | — | — |
| 40 | Yellowstone National Park | 110, 681 | 681 | — |
