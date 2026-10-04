# 第 14 章 模型组合

<aside class="chapter-guide"><strong>本章导读</strong><p>多个模型如何配合，才能得到更好的预测？本章区分贝叶斯模型平均与模型组合，介绍预测平均、提升和树模型，再讨论由输入决定各模型作用的条件混合，说明不同组合方式的训练方法与适用特点。</p></aside>

<!-- pdf-page: 673 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-chapter-opening.png" alt="水纹背景上的第 14 章标题"><p class="figure-translation">Combining Models → 模型组合。</p></figure>

前面各章研究了一系列用于解决分类和回归问题的不同模型。实践中常常发现，以某种方式将多个模型组合起来，比单独使用一个模型能获得更好的性能。例如，可以训练 $L$ 个不同模型，再对各模型的预测取平均，以此进行预测。这样的模型组合有时称为委员会（committee）。第 14.2 节将讨论如何在实践中应用委员会的概念，并说明为什么它有时会是一种有效的方法。

委员会方法的一个重要变体称为提升（boosting）。它依次训练多个模型，用于训练某个模型的误差函数取决于先前模型的表现。与使用单个模型相比，这种方法能够显著改善性能，第 14.3 节将对此进行讨论。

除了对一组模型的预测取平均，模型组合的另一种形式是

<!-- pdf-page: 674 -->

<!-- join-previous-paragraph -->
从这些模型中选择一个进行预测，模型的选择是输入变量的函数。于是，不同模型负责在输入空间的不同区域中进行预测。这类方法中一个广泛使用的框架称为决策树（decision tree），其选择过程可以描述为一连串二选一的决策，对应于沿树结构的遍历，第 14.4 节将讨论这种方法。此时，各个模型通常选得很简单，整体模型的灵活性来自依赖于输入的选择过程。决策树既可以用于分类问题，也可以用于回归问题。

决策树的一个局限是，它对输入空间采用硬划分：对于任意给定的输入变量值，只有一个模型负责作出预测。如第 14.5 节所述，将模型组合放入概率框架，就可以软化这一决策过程。例如，假设有 $K$ 个模型表示条件分布 $p(t\mid\mathbf{x},k)$，其中 $\mathbf{x}$ 是输入变量，$t$ 是目标变量，$k=1,\ldots,K$ 是模型索引，那么可以构造如下形式的概率混合：

$$
p(t\mid\mathbf{x})=\sum_{k=1}^{K}\pi_k(\mathbf{x})p(t\mid\mathbf{x},k)
\tag{14.1}
$$

其中，$\pi_k(\mathbf{x})=p(k\mid\mathbf{x})$ 表示依赖于输入的混合系数。这类模型可以看作混合分布，其中分量密度和混合系数都以输入变量为条件，称为专家混合（mixture of experts）。它们与第 5.6 节讨论的混合密度网络模型密切相关。

## 14.1 贝叶斯模型平均

有必要区分模型组合方法与贝叶斯模型平均，因为两者经常被混淆。为理解其区别，考虑用高斯混合进行密度估计的例子，其中多个高斯分量以概率方式组合。<span class="margin-reference">第 9.2 节</span>模型包含一个二值潜变量 $\mathbf{z}$，用于指示混合中的哪个分量负责生成对应的数据点。因此，模型由一个联合分布指定：

$$
p(\mathbf{x},\mathbf{z})
\tag{14.2}
$$

将潜变量边缘化掉，就得到相应的观测变量 $\mathbf{x}$ 的密度：

$$
p(\mathbf{x})=\sum_{\mathbf{z}}p(\mathbf{x},\mathbf{z}).
\tag{14.3}
$$

<!-- pdf-page: 675 -->

在高斯混合的例子中，这会得到如下形式的分布：

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)
\tag{14.4}
$$

其中各符号的含义与通常相同。这是模型组合的一个例子。对于独立同分布的数据，可以利用式（14.3），将数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 的边缘概率写成

$$
p(\mathbf{X})=\prod_{n=1}^{N}p(\mathbf{x}_n)=\prod_{n=1}^{N}\left[\sum_{\mathbf{z}_n}p(\mathbf{x}_n,\mathbf{z}_n)\right].
\tag{14.5}
$$

可见，每个观测数据点 $\mathbf{x}_n$ 都有一个对应的潜变量 $\mathbf{z}_n$。

现在假设有几个不同模型，用 $h=1,\ldots,H$ 编号，其先验概率为 $p(h)$。例如，一个模型可能是高斯混合，另一个模型可能是柯西分布的混合。数据集的边缘分布为

$$
p(\mathbf{X})=\sum_{h=1}^{H}p(\mathbf{X}\mid h)p(h).
\tag{14.6}
$$

这是贝叶斯模型平均的一个例子。对 $h$ 求和的解释是：整个数据集只由一个模型负责生成，$h$ 上的概率分布仅仅反映了我们对于究竟是哪一个模型的不确定性。随着数据集增大，这种不确定性会减小，后验概率 $p(h\mid\mathbf{X})$ 会越来越集中于其中某一个模型。

这揭示了贝叶斯模型平均与模型组合之间的关键差别：在贝叶斯模型平均中，整个数据集由单个模型生成。相比之下，当按式（14.5）组合多个模型时，数据集中不同的数据点可能由潜变量 $\mathbf{z}$ 的不同取值生成，因而可能来自不同分量。

虽然这里考虑的是边缘概率 $p(\mathbf{X})$，同样的讨论也适用于预测密度 $p(\mathbf{x}\mid\mathbf{X})$，或 $p(t\mid\mathbf{x},\mathbf{X},\mathbf{T})$ 这样的条件分布。<span class="margin-reference">习题 14.1</span>

## 14.2 委员会

构建委员会最简单的方法，是对一组单独模型的预测取平均。从频率学派的角度考虑偏差与方差的权衡，可以说明这种做法的依据。<span class="margin-reference">第 3.2 节</span>这种分解把模型引起的误差分为两部分：偏差来自模型与要预测的真实函数之间的差异，方差则表示模型对各个数据点的敏感程度。回顾图 3.5，

<!-- pdf-page: 676 -->

<!-- join-previous-paragraph -->
我们用正弦数据训练多个多项式，再对所得函数取平均时，方差项的贡献趋于相互抵消，预测因此得到改善。对一组低偏差模型，也就是较高阶多项式，取平均后，就能准确预测生成数据的那个潜在正弦函数。

当然，在实践中只有一个数据集，因此必须设法让委员会中的不同模型具有差异。一种方法是使用第 1.2.3 节讨论的自助数据集。考虑一个回归问题，目标是预测单个连续变量的值。假设生成 $M$ 个自助数据集，分别用它们训练同一种预测模型的不同副本 $y_m(\mathbf{x})$，其中 $m=1,\ldots,M$。委员会的预测为

$$
y_{\mathrm{COM}}(\mathbf{x})=\frac{1}{M}\sum_{m=1}^{M}y_m(\mathbf{x}).
\tag{14.7}
$$

这一过程称为自助聚合（bootstrap aggregation），也称为 bagging（Breiman，1996）。

假设我们要预测的真实回归函数为 $h(\mathbf{x})$，那么各个模型的输出都可以写成真实值加上一个误差：

$$
y_m(\mathbf{x})=h(\mathbf{x})+\epsilon_m(\mathbf{x}).
\tag{14.8}
$$

于是，平均平方和误差的形式为

$$
\mathbb{E}_{\mathbf{x}}\left[\{y_m(\mathbf{x})-h(\mathbf{x})\}^2\right]=\mathbb{E}_{\mathbf{x}}\left[\epsilon_m(\mathbf{x})^2\right]
\tag{14.9}
$$

其中 $\mathbb{E}_{\mathbf{x}}[\cdot]$ 表示相对于输入向量 $\mathbf{x}$ 的分布求频率学派意义下的期望。因此，各模型单独预测时的平均误差为

$$
E_{\mathrm{AV}}=\frac{1}{M}\sum_{m=1}^{M}\mathbb{E}_{\mathbf{x}}\left[\epsilon_m(\mathbf{x})^2\right].
\tag{14.10}
$$

类似地，委员会（14.7）的期望误差为

$$
\begin{aligned}
E_{\mathrm{COM}}&=\mathbb{E}_{\mathbf{x}}\left[\left\{\frac{1}{M}\sum_{m=1}^{M}y_m(\mathbf{x})-h(\mathbf{x})\right\}^2\right]\\
&=\mathbb{E}_{\mathbf{x}}\left[\left\{\frac{1}{M}\sum_{m=1}^{M}\epsilon_m(\mathbf{x})\right\}^2\right].
\end{aligned}
\tag{14.11}
$$

如果假设误差的均值为零，且彼此不相关，即

$$
\mathbb{E}_{\mathbf{x}}[\epsilon_m(\mathbf{x})]=0
\tag{14.12}
$$

$$
\mathbb{E}_{\mathbf{x}}[\epsilon_m(\mathbf{x})\epsilon_l(\mathbf{x})]=0,\qquad m\neq l
\tag{14.13}
$$

<!-- pdf-page: 677 -->

那么可得<span class="margin-reference">习题 14.2</span>

$$
E_{\mathrm{COM}}=\frac{1}{M}E_{\mathrm{AV}}.
\tag{14.14}
$$

这个结果看起来相当显著：只需将模型的 $M$ 个版本取平均，就能把模型的平均误差降至原来的 $1/M$。遗憾的是，这依赖于一个关键假设，即各模型产生的误差彼此不相关。在实践中，这些误差通常高度相关，因此总误差往往只能减小一点。不过，可以证明，委员会的期望误差不会超过其成员模型的期望误差，即 $E_{\mathrm{COM}}\leqslant E_{\mathrm{AV}}$。<span class="margin-reference">习题 14.3</span>为了获得更显著的改善，我们接下来介绍一种更复杂的委员会构造方法，称为提升。

## 14.3 提升

提升（boosting）是一种强大的方法，它将多个“基”分类器组合成一个委员会，其性能可以显著优于其中任何一个基分类器。这里介绍应用最广泛的一种提升算法，即 Freund 和 Schapire（1996）提出的 AdaBoost，其名称是“自适应提升”（adaptive boosting）的缩写。即使基分类器的性能只比随机猜测稍好，提升也可以取得良好结果，因此有时将这些基分类器称为弱学习器（weak learners）。提升最初是为分类问题设计的，也可以扩展到回归问题（Friedman，2001）。

提升与前面讨论的自助聚合等委员会方法之间的主要区别在于，提升依次训练各个基分类器；每个基分类器都使用带权重的数据集进行训练，其中每个数据点的权重系数取决于前面各分类器的表现。具体来说，当用某个基分类器误分类的数据点训练序列中的下一个分类器时，会为这些点赋予更大的权重。所有分类器训练完成后，再通过加权多数投票将它们的预测组合起来，如图 14.1 所示。

考虑一个二分类问题，其训练数据包括输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 以及对应的二元目标变量 $t_1,\ldots,t_N$，其中 $t_n\in\{-1,1\}$。每个数据点都关联一个权重参数 $w_n$，初始时所有数据点的权重都设为 $1/N$。假设我们已有一种方法，可以使用带权重的数据来训练基分类器，得到函数 $y(\mathbf{x})\in\{-1,1\}$。在算法的每个阶段，AdaBoost 都训练一个新的分类器；所用数据集中的权重系数根据上一个已训练分类器的表现进行调整，从而为误分类的数据点赋予更大的权重。最后，训练好所需数量的基分类器后，再用不同的系数为各个基分类器赋予不同权重，将它们组合成一个委员会。AdaBoost 算法的具体形式如下。

<!-- pdf-page: 678 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-1.png" alt="提升框架：带权重的训练集依次训练基分类器，前一个分类器影响后续数据权重，各分类器加权组成最终预测"><figcaption>图 14.1：提升框架示意图。每个基分类器 $y_m(\mathbf{x})$ 都在带权重的训练集上训练（蓝色箭头），其中权重 $w_n^{(m)}$ 取决于前一个基分类器 $y_{m-1}(\mathbf{x})$ 的表现（绿色箭头）。所有基分类器训练完成后，将它们组合起来，得到最终分类器 $Y_M(\mathbf{x})$（红色箭头）。</figcaption><p class="figure-translation">sign → 符号函数。</p></figure>

<aside class="procedure"><h3>AdaBoost</h3>
<ol><li>初始化数据权重系数 $\{w_n\}$，令 $w_n^{(1)}=1/N$，其中 $n=1,\ldots,N$。</li><li>对 $m=1,\ldots,M$：</li></ol>
<p>（a）通过最小化加权误差函数，将分类器 $y_m(\mathbf{x})$ 拟合到训练数据：</p>
<p>$$J_m=\sum_{n=1}^{N}w_n^{(m)}I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)\tag{14.15}$$</p>
<p>其中 $I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)$ 是指示函数：当 $y_m(\mathbf{x}_n)\neq t_n$ 时等于 $1$，否则等于 $0$。</p>
<p>（b）计算</p>
<p>$$\epsilon_m=\frac{\displaystyle\sum_{n=1}^{N}w_n^{(m)}I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)}{\displaystyle\sum_{n=1}^{N}w_n^{(m)}}\tag{14.16}$$</p>
<p>然后用它计算</p>
<p>$$\alpha_m=\ln\left\{\frac{1-\epsilon_m}{\epsilon_m}\right\}.\tag{14.17}$$</p>
<p>（c）更新数据权重系数</p>
<p>$$w_n^{(m+1)}=w_n^{(m)}\exp\left\{\alpha_m I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)\right\}\tag{14.18}$$</p>
</aside>

<!-- pdf-page: 679 -->
<!-- join-previous-procedure -->

<aside class="procedure"><ol start="3"><li>使用如下最终模型作出预测：</li></ol>
<p>$$Y_M(\mathbf{x})=\operatorname{sign}\left(\sum_{m=1}^{M}\alpha_m y_m(\mathbf{x})\right).\tag{14.19}$$</p>
</aside>

我们看到，第一个基分类器 $y_1(\mathbf{x})$ 使用全都相等的权重系数 $w_n^{(1)}$ 进行训练，因此对应于训练单个分类器的通常过程。由式（14.18）可知，在后续迭代中，误分类数据点的权重系数 $w_n^{(m)}$ 会增大，而正确分类数据点的权重系数会减小。因此，后续分类器不得不更加重视被先前分类器误分类的数据点；连续被后续分类器误分类的数据点会得到越来越大的权重。$\epsilon_m$ 表示各基分类器在数据集上的加权误差率。因此，在计算式（14.19）给出的总体输出时，式（14.17）定义的权重系数 $\alpha_m$ 会为更准确的分类器赋予更大的权重。

图 14.2 用图 A.7 所示人工分类数据集中的 $30$ 个数据点演示了 AdaBoost 算法。这里，每个基学习器都对某个输入变量设置一个阈值。这个简单分类器对应于一种称为“决策树桩”（decision stump）的决策树，即只有一个节点的决策树。<span class="margin-reference">第 14.4 节</span>因此，每个基学习器根据某个输入特征是否超过阈值来对输入进行分类，也就是用一个与某条坐标轴平行的线性决策面，将空间分成两个区域。

### 14.3.1 最小化指数误差

提升最初的动机来自统计学习理论，由此可以得到泛化误差的上界。然而，这些上界过于宽松，缺乏实用价值；提升的实际性能远好于仅从这些上界所能判断出的水平。Friedman 等人（2000）给出了另一种非常简单的解释，将提升看成依次最小化一个指数误差函数的过程。

考虑如下定义的指数误差函数：

$$
E=\sum_{n=1}^{N}\exp\{-t_n f_m(\mathbf{x}_n)\}
\tag{14.20}
$$

其中 $f_m(\mathbf{x})$ 是由基分类器 $y_l(\mathbf{x})$ 的线性组合定义的分类器，其形式为

$$
f_m(\mathbf{x})=\frac{1}{2}\sum_{l=1}^{m}\alpha_l y_l(\mathbf{x})
\tag{14.21}
$$

而 $t_n\in\{-1,1\}$ 是训练集的目标值。我们的目标是同时对权重系数 $\alpha_l$ 和基分类器 $y_l(\mathbf{x})$ 的参数最小化 $E$。

<!-- pdf-page: 680 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-2.png" alt="提升在六个训练阶段的分类结果：基学习器数量为1、2、3、6、10和150，圆的半径表示样本权重"><figcaption>图 14.2：提升示例，其中基学习器只是在某一条坐标轴上施加简单阈值。每幅图都标出了目前已训练的基学习器数量 $m$，以及最新基学习器的决策边界（黑色虚线）和集成模型的组合决策边界（绿色实线）。每个数据点都用一个圆表示，其半径表示训练最新加入的基学习器时为该点赋予的权重。例如可以看到，在训练 $m=2$ 的基学习器时，$m=1$ 的基学习器所误分类的数据点获得了更大的权重。</figcaption></figure>

不过，我们不对误差函数进行全局最小化，而是假设基分类器 $y_1(\mathbf{x}),\ldots,y_{m-1}(\mathbf{x})$ 及其系数 $\alpha_1,\ldots,\alpha_{m-1}$ 均已固定，只对 $\alpha_m$ 和 $y_m(\mathbf{x})$ 进行最优化。将基分类器 $y_m(\mathbf{x})$ 的贡献单独列出，就可以将误差函数写成

$$
\begin{aligned}
E&=\sum_{n=1}^{N}\exp\left\{-t_n f_{m-1}(\mathbf{x}_n)-\frac{1}{2}t_n\alpha_m y_m(\mathbf{x}_n)\right\}\\
&=\sum_{n=1}^{N}w_n^{(m)}\exp\left\{-\frac{1}{2}t_n\alpha_m y_m(\mathbf{x}_n)\right\}
\end{aligned}
\tag{14.22}
$$

其中，系数 $w_n^{(m)}=\exp\{-t_n f_{m-1}(\mathbf{x}_n)\}$ 可以看成常数，因为我们只优化 $\alpha_m$ 和 $y_m(\mathbf{x})$。若用 $\mathcal{T}_m$ 表示被 $y_m(\mathbf{x})$ 正确分类的数据点集合，用 $\mathcal{M}_m$ 表示其余误分类的数据点集合，就可以进一步将误差函数改写为

<!-- pdf-page: 681 -->
<!-- join-previous-paragraph -->

如下形式：

$$
\begin{aligned}
E&=e^{-\alpha_m/2}\sum_{n\in\mathcal{T}_m}w_n^{(m)}+e^{\alpha_m/2}\sum_{n\in\mathcal{M}_m}w_n^{(m)}\\
&=\left(e^{\alpha_m/2}-e^{-\alpha_m/2}\right)\sum_{n=1}^{N}w_n^{(m)}I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)+e^{-\alpha_m/2}\sum_{n=1}^{N}w_n^{(m)}.
\end{aligned}
\tag{14.23}
$$

当我们对 $y_m(\mathbf{x})$ 最小化这个表达式时，第二项是常数，因此这等价于最小化式（14.15），因为求和前面的整体乘法因子不影响极小值的位置。类似地，对 $\alpha_m$ 最小化这个表达式，就能得到式（14.17），其中 $\epsilon_m$ 由式（14.16）定义。<span class="margin-reference">习题 14.6</span>

由式（14.22）可知，求得 $\alpha_m$ 和 $y_m(\mathbf{x})$ 后，数据点的权重按下式更新：

$$
w_n^{(m+1)}=w_n^{(m)}\exp\left\{-\frac{1}{2}t_n\alpha_m y_m(\mathbf{x}_n)\right\}.
\tag{14.24}
$$

利用关系

$$
t_n y_m(\mathbf{x}_n)=1-2I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)
\tag{14.25}
$$

可知，下一次迭代按如下方式更新权重 $w_n^{(m)}$：

$$
w_n^{(m+1)}=w_n^{(m)}\exp(-\alpha_m/2)\exp\left\{\alpha_m I\bigl(y_m(\mathbf{x}_n)\neq t_n\bigr)\right\}.
\tag{14.26}
$$

由于因子 $\exp(-\alpha_m/2)$ 与 $n$ 无关，它对所有数据点施加相同的权重因子，因此可以舍去。这样便得到式（14.18）。

最后，所有基分类器训练完成后，通过计算式（14.21）定义的组合函数的正负号，便可对新数据点分类。由于因子 $1/2$ 不影响正负号，可以将其省略，从而得到式（14.19）。

### 14.3.2 提升的误差函数

AdaBoost 算法所最小化的指数误差函数与前几章考虑过的误差函数不同。为了了解指数误差函数的性质，我们首先考虑如下期望误差：

$$
\mathbb{E}_{\mathbf{x},t}[\exp\{-ty(\mathbf{x})\}]=\sum_t\int\exp\{-ty(\mathbf{x})\}p(t\mid\mathbf{x})p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{14.27}
$$

如果在所有可能的函数 $y(\mathbf{x})$ 上进行变分最小化，就会得到<span class="margin-reference">习题 14.7</span>

$$
y(\mathbf{x})=\frac{1}{2}\ln\left\{\frac{p(t=1\mid\mathbf{x})}{p(t=-1\mid\mathbf{x})}\right\}
\tag{14.28}
$$

<!-- pdf-page: 682 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-3.png" alt="指数误差、缩放后的交叉熵误差、铰链误差和误分类误差随z变化的比较"><figcaption>图 14.3：指数误差函数（绿色）和重新缩放后的交叉熵误差函数（红色），以及支持向量机采用的铰链误差（hinge error，蓝色）和误分类误差（黑色）。注意，当 $z=ty(\mathbf{x})$ 为绝对值较大的负数时，交叉熵产生的惩罚按线性增长，而指数损失产生的惩罚按指数增长。</figcaption></figure>

它是对数几率的一半。因此，AdaBoost 算法是在基分类器线性组合所表示的函数空间内，寻找对数几率比的最佳近似，同时受到依次优化策略所带来的最小化约束。这个结果说明了为什么在式（14.19）中使用符号函数来作出最终分类决策。

我们已经看到，使二分类交叉熵误差（4.90）最小的函数 $y(\mathbf{x})$ 由类别后验概率给出。对于目标变量 $t\in\{-1,1\}$，我们曾经看到，误差函数为 $\ln(1+\exp(-yt))$。<span class="margin-reference">第 7.1.2 节</span>图 14.3 将它与指数误差函数作了比较；为便于比较，我们将交叉熵误差除以常数因子 $\ln(2)$，使其经过点 $(0,1)$。可以看到，两者都可视为理想误分类误差函数的连续近似。指数误差的一个优点是，对它依次最小化就能得到简单的 AdaBoost 方法。不过，它的一个缺点是：当 $ty(\mathbf{x})$ 为绝对值较大的负数时，它施加的惩罚比交叉熵大得多。具体来说，当 $ty$ 为绝对值较大的负数时，交叉熵随 $|ty|$ 线性增长，而指数误差函数随 $|ty|$ 指数增长。因此，指数误差函数对于离群点或被误分类的数据点的鲁棒性要差得多。交叉熵与指数误差函数之间的另一个重要区别在于，后者不能解释为任何定义良好的概率模型的对数似然函数。<span class="margin-reference">习题 14.8</span>此外，指数误差也不能推广到类别数 $K>2$ 的分类问题。这又与概率模型的交叉熵不同，后者很容易推广为式（4.108）。<span class="margin-reference">第 4.3.4 节</span>

将提升解释为在指数误差下依次优化一个加性模型（Friedman 等人，2000），就可以通过改变误差函数的选择，得到广泛的一类类似提升的算法，包括面向多分类的扩展。这也为扩展到回归问题提供了思路（Friedman，2001）。如果在回归中采用平方和误差函数，那么对式（14.21）形式的加性模型依次最小化，就只需将每个新的基分类器拟合到前一个模型的残差 $t_n-f_{m-1}(\mathbf{x}_n)$。<span class="margin-reference">习题 14.9</span>然而，正如我们指出过的，平方和误差对于离群点不具有鲁棒性，这一问题

<!-- pdf-page: 683 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-4.png" alt="平方误差和绝对误差比较：绝对误差对较大误差施加的惩罚增长较慢"><figcaption>图 14.4：平方误差（绿色）与绝对误差（红色）的比较。后者对较大误差的重视程度要低得多，因此对于离群点和标签错误的数据点具有更好的鲁棒性。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->

可以通过改为基于绝对偏差 $|y-t|$ 来构造提升算法加以解决。图 14.4 比较了这两种误差函数。

## 14.4 基于树的模型

有多种简单而又广泛使用的模型，它们将输入空间划分成各条边与坐标轴对齐的长方体区域，再为每个区域指定一个简单模型，例如一个常数。这可以看成一种模型组合方法，其中输入空间中的任意一点都只由一个模型负责作出预测。给定新的输入 $\mathbf{x}$，选择具体模型的过程可以描述为一连串决策，对应于遍历一棵二叉树，即每个节点都分出两个分支的树。这里，我们重点介绍一种称为分类与回归树（classification and regression trees，CART）的树模型框架（Breiman 等人，1984）；此外还有许多变体，例如 ID3 和 C4.5（Quinlan，1986；Quinlan，1993）。

图 14.5 给出了对输入空间进行递归二分的示例，以及对应的树结构。在这个例子中，第一步

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-5.png" alt="二维输入空间由平行坐标轴的边界划分为A至E五个区域"><figcaption>图 14.5：二维输入空间示意图，用与坐标轴对齐的边界将其划分为五个区域。</figcaption></figure>

<!-- pdf-page: 684 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/a-fig-14-6.png" alt="与二维空间五区域划分对应的二叉决策树，叶节点为A至E"><figcaption>图 14.6：与图 14.5 所示输入空间划分相对应的二叉树。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->

根据 $x_1\leqslant\theta_1$ 还是 $x_1>\theta_1$，将整个输入空间分成两个区域，其中 $\theta_1$ 是模型参数。这样就产生了两个子区域，每个子区域都可以独立地继续划分。例如，根据 $x_2\leqslant\theta_2$ 还是 $x_2>\theta_2$，进一步划分区域 $x_1\leqslant\theta_1$，便得到标为 A 和 B 的两个区域。这样的递归划分可以用图 14.6 所示二叉树的遍历来描述。对于任何新的输入 $\mathbf{x}$，我们从树顶端的根节点出发，根据各节点的决策准则沿一条路径向下走，到达某个叶节点，以此确定输入落在哪个区域。注意，这类决策树不是概率图模型。

每个区域都有一个单独的模型，用于预测目标变量。例如，在回归问题中，我们可以在每个区域内直接预测一个常数；在分类问题中，则可以为每个区域指定一个类别。树模型的一个关键性质是，它们对应于依次施加在各个输入变量上的一系列二元决策，因此易于人理解，这使得它们在医疗诊断等领域很受欢迎。例如，为预测患者患有何种疾病，我们可以先问：“体温是否超过某个阈值？”如果答案是肯定的，那么接着可以问：“血压是否低于某个阈值？”于是，树的每个叶节点都对应一个具体诊断。

要从训练集中学习这样的模型，必须确定树的结构，包括在每个节点选择哪个输入变量来构造划分准则，以及该划分的阈值参数 $\theta_i$。我们还需要确定每个区域内预测变量的取值。

首先考虑回归问题，目标是根据由输入变量组成的 $D$ 维向量 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathrm{T}}$，预测单个目标变量 $t$。训练数据由输入向量 $\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 及其对应的连续标签 $\{t_1,\ldots,t_N\}$ 组成。如果输入空间的划分已经给定，并且我们最小化平方和误差函数，那么任一区域内预测变量的最优值，就是落在该区域中的数据点所对应的 $t_n$ 值的平均值。<span class="margin-reference">习题 14.10</span>

现在考虑如何确定决策树的结构。即便树中的节点数固定，要确定最优结构——包括每次划分所选的输入变量及相应的

<!-- pdf-page: 685 -->
<!-- join-previous-paragraph -->
阈值——以使平方和误差最小，通常在计算上也不可行，因为可能解的组合数量过大。因此，通常采用贪心优化：从对应于整个输入空间的单个根节点出发，每次增加一个节点，使树逐步生长。在每一步，输入空间中都会有若干可供划分的候选区域；每次划分对应于在现有树中增加一对叶节点。对于每个候选区域，需要选择按照 $D$ 个输入变量中的哪一个进行划分，并选择阈值。可以通过穷举搜索，高效地联合优化待划分区域、输入变量和阈值的选择。这里利用了前面指出的事实：给定划分变量和阈值后，预测变量的最优选择就是数据的局部平均值。对所有可能的划分变量选择重复这一过程，保留残差平方和误差最小的选择。

在确定了让树生长的贪心策略之后，还需要解决何时停止增加节点的问题。一种简单方法是，当残差误差的下降幅度低于某个阈值时停止。然而，经验表明，经常会出现这样的情况：当前所有可用的划分都不能显著降低误差，但再进行几次划分后，却能获得很大的误差下降。因此，通常的做法是，根据各叶节点对应的数据点数量设置停止准则，先生成一棵较大的树，再对其进行剪枝。剪枝依据的准则，在残差误差与模型复杂度的某种度量之间进行权衡。将剪枝前的树记为 $T_0$；如果一棵树可以通过从 $T_0$ 中剪去节点得到，就定义 $T\subset T_0$ 为 $T_0$ 的子树。换句话说，剪枝是通过合并相应区域来折叠内部节点。假设叶节点编号为 $\tau=1,\ldots,|T|$，叶节点 $\tau$ 表示输入空间中包含 $N_\tau$ 个数据点的区域 $\mathcal{R}_\tau$，$|T|$ 表示叶节点总数。那么，区域 $\mathcal{R}_\tau$ 的最优预测为

$$
y_\tau=\frac{1}{N_\tau}\sum_{\mathbf{x}_n\in\mathcal{R}_\tau}t_n
\tag{14.29}
$$

相应地，它对残差平方和的贡献为

$$
Q_\tau(T)=\sum_{\mathbf{x}_n\in\mathcal{R}_\tau}\{t_n-y_\tau\}^2.
\tag{14.30}
$$

剪枝准则由下式给出

$$
C(T)=\sum_{\tau=1}^{|T|}Q_\tau(T)+\lambda|T|
\tag{14.31}
$$

正则化参数 $\lambda$ 决定总残差平方和误差与模型复杂度之间的权衡，这里的复杂度由叶节点数 $|T|$ 衡量。$\lambda$ 的值通过交叉验证选择。

对于分类问题，树的生长与剪枝过程类似，只需将平方和误差替换为更合适的

<!-- pdf-page: 686 -->
<!-- join-previous-paragraph -->
性能度量。如果将 $p_{\tau k}$ 定义为区域 $\mathcal{R}_\tau$ 中被分配到类别 $k$ 的数据点比例，其中 $k=1,\ldots,K$，那么两个常用选择是交叉熵

$$
Q_\tau(T)=\sum_{k=1}^{K}p_{\tau k}\ln p_{\tau k}
\tag{14.32}
$$

和 *Gini 指数*

$$
Q_\tau(T)=\sum_{k=1}^{K}p_{\tau k}(1-p_{\tau k}).
\tag{14.33}
$$

当 $p_{\tau k}=0$ 或 $p_{\tau k}=1$ 时，两者都为零，并在 $p_{\tau k}=0.5$ 时达到最大。它们鼓励形成这样的区域：其中大部分数据点都属于同一个类别。对于树的生长，交叉熵和 Gini 指数是比误分类率更好的度量，因为它们对节点概率更敏感（习题 14.11）。此外，与误分类率不同，它们是可微的，因此更适合基于梯度的优化方法。对于后续的树剪枝，通常使用误分类率。

CART 等树模型能够被人理解，这通常被视为其主要优势。然而，实践中发现，学得的具体树结构对数据集的细节十分敏感，训练数据的微小变化就可能导致截然不同的一组划分（Hastie et al.，2001）。

本节讨论的这类基于树的方法还存在其他问题。首先，划分与特征空间的坐标轴对齐，这种限制可能使结果远非最优。例如，要分开两个最优决策边界与坐标轴成 45 度角的类别，单次不与坐标轴对齐的划分即可完成，而沿坐标轴方向划分输入空间则需要很多次。此外，决策树中的划分是硬划分，因此输入空间中的每个区域都只对应一个叶节点模型。最后这个问题在回归中尤其明显：我们通常希望对平滑函数建模，而树模型产生的是分段常数预测，在划分边界上不连续。

## 14.5 条件混合模型

前面已经看到，标准决策树受到对输入空间进行硬划分、且划分与坐标轴对齐的限制。可以允许软的概率划分，以可解释性为代价放宽这些约束：划分可以是所有输入变量的函数，而不必每次只依赖一个输入变量。如果还赋予叶节点模型概率解释，就会得到一种完全概率化的树模型，称为*层次专家混合*（hierarchical mixture of experts），第 14.5.3 节将讨论它。

引出层次专家混合模型的另一种方法，是从高斯等无条件密度模型的标准概率混合出发（第 9 章），将各分量的密度替换为条件分布。这里考虑线性回归模型的混合（第 14.5.1 节）和

<!-- pdf-page: 687 -->
<!-- join-previous-paragraph -->
逻辑回归模型的混合（第 14.5.2 节）。在最简单的情形中，混合系数与输入变量无关。如果进一步推广，允许混合系数也依赖于输入，就得到*专家混合*（mixture of experts）模型。最后，如果允许混合模型中的每个分量本身又是一个专家混合模型，就得到层次专家混合。

### 14.5.1 线性回归模型的混合

赋予线性回归模型概率解释有许多优点，其中之一是可以将它用作更复杂概率模型中的一个分量。例如，可以把表示线性回归模型的条件分布，看作有向概率图中的一个节点。这里考虑一个简单例子，即线性回归模型的混合；它是将第 9.2 节讨论的高斯混合模型直接扩展到条件高斯分布的情形。

因此，考虑 $K$ 个线性回归模型，每个模型都有各自的权重参数 $\mathbf{w}_k$。在许多应用中，让全部 $K$ 个分量使用由精度参数 $\beta$ 控制的共同噪声方差，是合适的做法；这里考虑的就是这种情况。再次将讨论限制为单个目标变量 $t$，不过扩展到多个输出也很直接（习题 14.12）。将混合系数记为 $\pi_k$，则混合分布可写为

$$
p(t\mid\boldsymbol{\theta})=\sum_{k=1}^{K}\pi_k\mathcal{N}(t\mid\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi},\beta^{-1})
\tag{14.34}
$$

其中，$\boldsymbol{\theta}$ 表示模型中全部可调参数的集合，即 $\mathbf{W}=\{\mathbf{w}_k\}$、$\boldsymbol{\pi}=\{\pi_k\}$ 和 $\beta$。给定由观测 $\{\boldsymbol{\phi}_n,t_n\}$ 组成的数据集，模型的对数似然函数为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=\sum_{n=1}^{N}\ln\left(\sum_{k=1}^{K}\pi_k\mathcal{N}(t_n\mid\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})\right)
\tag{14.35}
$$

其中，$\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm{T}}$ 表示目标变量向量。

为最大化这个似然函数，可以再次使用 EM 算法。它将是第 9.2 节中无条件高斯混合的 EM 算法的简单扩展。因此，可以利用无条件混合的经验，引入一组二元潜变量 $\mathbf{Z}=\{\mathbf{z}_n\}$，其中 $z_{nk}\in\{0,1\}$。对于每个数据点 $n$，在 $k=1,\ldots,K$ 的所有元素中，除一个取值为 1 外，其余均为零；这个 1 表明混合中的哪个分量负责生成该数据点。潜变量和观测变量的联合分布，可以由图 14.7 所示的图模型表示。

完整数据对数似然函数为（习题 14.13）

$$
\ln p(\boldsymbol{\mathsf{t}},\mathbf{Z}\mid\boldsymbol{\theta})=\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\ln\left\{\pi_k\mathcal{N}(t_n\mid\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})\right\}.
\tag{14.36}
$$

<!-- pdf-page: 688 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/b-fig-14-7.png" alt="线性回归模型混合的有向概率图，含分量指示潜变量、目标观测及参数"><figcaption>图 14.7：表示（14.35）所定义的线性回归模型混合的有向概率图。</figcaption><p class="figure-translation">$\boldsymbol{\pi}$：混合系数；$\beta$：噪声精度；$\mathbf{W}$：回归权重；$\mathbf{z}_n$：分量指示潜变量；$t_n$：目标观测；$\boldsymbol{\phi}_n$：输入特征；$N$：观测数量。蓝色板表示重复，填色圆节点表示已观测的目标。</p></figure>

EM 算法首先为模型参数选择初始值 $\boldsymbol{\theta}^{\mathrm{old}}$。随后，在 E 步中，使用这些参数值，计算每个分量 $k$ 对每个数据点 $n$ 的后验概率，即责任度：

$$
\gamma_{nk}=\mathbb{E}[z_{nk}]=p(k\mid\boldsymbol{\phi}_n,\boldsymbol{\theta}^{\mathrm{old}})=\frac{\pi_k\mathcal{N}(t_n\mid\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})}{\sum_j\pi_j\mathcal{N}(t_n\mid\mathbf{w}_j^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})}.
\tag{14.37}
$$

然后利用这些责任度，计算完整数据对数似然关于后验分布 $p(\mathbf{Z}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\theta}^{\mathrm{old}})$ 的期望，得到

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\mathbb{E}_{\mathbf{Z}}\left[\ln p(\boldsymbol{\mathsf{t}},\mathbf{Z}\mid\boldsymbol{\theta})\right]=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma_{nk}\left\{\ln\pi_k+\ln\mathcal{N}(t_n\mid\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})\right\}.
$$

在 M 步中，固定 $\gamma_{nk}$，关于 $\boldsymbol{\theta}$ 最大化函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$。关于混合系数 $\pi_k$ 的优化需要考虑约束 $\sum_k\pi_k=1$，这可以借助拉格朗日乘子来完成，从而得到 $\pi_k$ 的 M 步重估方程（习题 14.14）

$$
\pi_k=\frac{1}{N}\sum_{n=1}^{N}\gamma_{nk}.
\tag{14.38}
$$

注意，这与（9.22）给出的简单无条件高斯混合的相应结果具有完全相同的形式。

接下来考虑关于第 $k$ 个线性回归模型的参数向量 $\mathbf{w}_k$ 的最大化。代入高斯分布，可见函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 作为参数向量 $\mathbf{w}_k$ 的函数，具有如下形式

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\sum_{n=1}^{N}\gamma_{nk}\left\{-\frac{\beta}{2}\left(t_n-\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n\right)^2\right\}+\mathrm{const}
\tag{14.39}
$$

其中，常数项包含其他权重向量 $\mathbf{w}_j$（$j\ne k$）的贡献。注意，要最大化的量类似于单个线性回归模型的标准平方和误差（3.12）的负值，但加入了责任度 $\gamma_{nk}$。这表示一个*加权最小二乘*

<!-- pdf-page: 689 -->
<!-- join-previous-paragraph -->
问题，其中对应于第 $n$ 个数据点的项带有权重系数 $\beta\gamma_{nk}$，它可以解释为每个数据点的有效精度。可以看到，在 M 步中，混合中的每个线性回归分量模型都由自己的参数向量 $\mathbf{w}_k$ 控制，并分别拟合整个数据集；但每个数据点 $n$ 都以模型 $k$ 对该点的责任度 $\gamma_{nk}$ 加权。令（14.39）关于 $\mathbf{w}_k$ 的导数等于零，得到

$$
0=\sum_{n=1}^{N}\gamma_{nk}\left(t_n-\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n\right)\boldsymbol{\phi}_n
\tag{14.40}
$$

将其写成矩阵形式为

$$
0=\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{R}_k(\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{w}_k)
\tag{14.41}
$$

其中，$\mathbf{R}_k=\operatorname{diag}(\gamma_{nk})$ 是一个 $N\times N$ 的对角矩阵。解出 $\mathbf{w}_k$，得到

$$
\mathbf{w}_k=\left(\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{R}_k\boldsymbol{\Phi}\right)^{-1}\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{R}_k\boldsymbol{\mathsf{t}}.
\tag{14.42}
$$

这是对应于加权最小二乘问题的一组修正后的正规方程，与逻辑回归中得到的（4.99）具有相同形式。注意，每次 E 步之后，矩阵 $\mathbf{R}_k$ 都会改变，因此必须在随后的 M 步中重新求解正规方程。

最后，关于 $\beta$ 最大化 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$。只保留依赖于 $\beta$ 的项，函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 可写为

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma_{nk}\left\{\frac{1}{2}\ln\beta-\frac{\beta}{2}\left(t_n-\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n\right)^2\right\}.
\tag{14.43}
$$

令关于 $\beta$ 的导数等于零并整理，得到 $\beta$ 的 M 步方程

$$
\frac{1}{\beta}=\frac{1}{N}\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma_{nk}\left(t_n-\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n\right)^2.
\tag{14.44}
$$

图 14.8 用一个简单例子说明这一 EM 算法：将两条直线的混合拟合到一个具有单个输入变量 $x$ 和单个目标变量 $t$ 的数据集上。图 14.9 使用 EM 算法收敛后得到的参数值，画出了预测密度（14.34），对应于图 14.8 的右图。图中还显示了拟合单个线性回归模型的结果，它给出单峰预测密度。可以看到，混合模型更好地表示了数据分布，这也体现在较高的似然值上。然而，混合模型也为没有数据的区域分配了相当大的概率质量，因为对于所有 $x$ 值，它的预测分布都是双峰的。可以扩展模型，允许混合系数本身成为 $x$ 的函数，以解决这一问题；由此得到的模型包括第 5.6 节讨论的混合密度网络，以及第 14.5.3 节讨论的层次专家混合。

<!-- pdf-page: 690 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/b-fig-14-8.png" alt="两条线性回归模型混合的EM拟合过程，三列分别显示初始状态、30次和50次迭代及对应责任度"><figcaption>图 14.8：一个具有单个输入变量 $x$ 和单个目标变量 $t$ 的合成数据集示例，以绿色点表示；同时给出了两个线性回归模型的混合，其均值函数 $y(x,\mathbf{w}_k)$（$k\in\{1,2\}$）由蓝色与红色直线表示。上方三幅图分别显示初始配置（左）、运行 30 次 EM 迭代后的结果（中），以及 50 次 EM 迭代后的结果（右）。这里，$\beta$ 初始化为目标值集合真实方差的倒数。下方三幅图显示相应的责任度：每个数据点用一条竖线表示，其中蓝色线段的长度给出蓝色直线对该数据点的后验概率，红色线段同理。</figcaption><p class="figure-translation">三列从左到右：初始配置、30 次 EM 迭代、50 次 EM 迭代；上排绿色圆圈为数据点，蓝线和红线为两个回归分量的均值函数；下排蓝、红线段分别为两个分量的责任度。</p></figure>

### 14.5.2 逻辑模型的混合

逻辑回归模型定义了给定输入向量时目标变量的条件分布，因此很容易将其作为混合模型中的分量分布，从而得到比单个逻辑回归模型更丰富的一族条件分布。这个例子直接组合了本书前面各节中出现的概念，有助于读者巩固对这些概念的理解。

对于 $K$ 个逻辑回归模型的概率混合，目标变量的条件分布为

$$
p(t\mid\boldsymbol{\phi},\boldsymbol{\theta})=\sum_{k=1}^{K}\pi_k y_k^t[1-y_k]^{1-t}
\tag{14.45}
$$

其中，$\boldsymbol{\phi}$ 为特征向量，$y_k=\sigma(\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi})$ 是分量 $k$ 的输出，$\boldsymbol{\theta}$ 表示可调参数，即 $\{\pi_k\}$ 和 $\{\mathbf{w}_k\}$。

现在假设给定数据集 $\{\boldsymbol{\phi}_n,t_n\}$，相应的似然

<!-- pdf-page: 691 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/b-fig-14-9.png" alt="回归混合模型与单个线性回归模型的预测条件密度对比"><figcaption>图 14.9：左图显示了与图 14.8 中收敛解对应的预测条件密度，对数似然值为 $-3.0$。在某个特定的 $x$ 值处，对其中一幅图作竖直切片，就得到对应的条件分布 $p(t\mid x)$；可以看到它是双峰的。右图显示了用最大似然将单个线性回归模型拟合到同一数据集后得到的预测密度。该模型的对数似然较小，为 $-27.6$。</figcaption><p class="figure-translation">左图：两分量线性回归混合；右图：单个线性回归模型。绿色圆圈为数据点，紫色浓淡表示预测条件密度，直线表示回归均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
函数为

$$
p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=\prod_{n=1}^{N}\left(\sum_{k=1}^{K}\pi_k y_{nk}^{t_n}[1-y_{nk}]^{1-t_n}\right)
\tag{14.46}
$$

其中，$y_{nk}=\sigma(\mathbf{w}_k^{\mathrm{T}}\boldsymbol{\phi}_n)$，$\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm{T}}$。可以利用 EM 算法迭代最大化这个似然函数。为此，引入潜变量 $z_{nk}$，它们对应于每个数据点 $n$ 的一个采用 1-of-$K$ 编码的二元指示变量。完整数据似然函数为

$$
p(\boldsymbol{\mathsf{t}},\mathbf{Z}\mid\boldsymbol{\theta})=\prod_{n=1}^{N}\prod_{k=1}^{K}\left\{\pi_k y_{nk}^{t_n}[1-y_{nk}]^{1-t_n}\right\}^{z_{nk}}
\tag{14.47}
$$

其中，$\mathbf{Z}$ 是元素为 $z_{nk}$ 的潜变量矩阵。选择模型参数的初始值 $\boldsymbol{\theta}^{\mathrm{old}}$，以初始化 EM 算法。在 E 步中，用这些参数值计算每个数据点 $n$ 对应的分量 $k$ 的后验概率，即

$$
\gamma_{nk}=\mathbb{E}[z_{nk}]=p(k\mid\boldsymbol{\phi}_n,\boldsymbol{\theta}^{\mathrm{old}})=\frac{\pi_k y_{nk}^{t_n}[1-y_{nk}]^{1-t_n}}{\sum_j\pi_j y_{nj}^{t_n}[1-y_{nj}]^{1-t_n}}.
\tag{14.48}
$$

然后使用这些责任度，得到作为 $\boldsymbol{\theta}$ 的函数的完整数据对数似然的期望：

$$
\begin{aligned}
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})
&=\mathbb{E}_{\mathbf{Z}}[\ln p(\boldsymbol{\mathsf{t}},\mathbf{Z}\mid\boldsymbol{\theta})]\\
&=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma_{nk}\{\ln\pi_k+t_n\ln y_{nk}+(1-t_n)\ln(1-y_{nk})\}.
\end{aligned}
\tag{14.49}
$$

<!-- pdf-page: 692 -->

M 步关于 $\boldsymbol{\theta}$ 最大化这个函数，同时固定 $\boldsymbol{\theta}^{\mathrm{old}}$，因而也固定 $\gamma_{nk}$。关于 $\pi_k$ 的最大化可以按通常的方法进行：用拉格朗日乘子施加求和约束 $\sum_k\pi_k=1$，得到熟悉的结果

$$
\pi_k=\frac{1}{N}\sum_{n=1}^{N}\gamma_{nk}.
\tag{14.50}
$$

为确定 $\{\mathbf{w}_k\}$，注意函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 是一组按 $k$ 编号的项之和，每一项只依赖于一个向量 $\mathbf{w}_k$，因此不同向量在 EM 算法的 M 步中相互解耦。换言之，不同分量只通过责任度相互作用，而责任度在 M 步中保持固定。注意，M 步没有闭式解，必须使用迭代方法求解，例如迭代重加权最小二乘（IRLS）算法（第 4.3.3 节）。向量 $\mathbf{w}_k$ 的梯度和 Hessian 矩阵为

$$
\nabla_k Q=\sum_{n=1}^{N}\gamma_{nk}(t_n-y_{nk})\boldsymbol{\phi}_n
\tag{14.51}
$$

$$
\mathbf{H}_k=-\nabla_k\nabla_k Q=\sum_{n=1}^{N}\gamma_{nk}y_{nk}(1-y_{nk})\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm{T}}
\tag{14.52}
$$

其中，$\nabla_k$ 表示关于 $\mathbf{w}_k$ 的梯度。在 $\gamma_{nk}$ 固定时，这些量与 $j\ne k$ 的 $\{\mathbf{w}_j\}$ 无关，因此可以用 IRLS 算法分别求解每个 $\mathbf{w}_k$（第 4.3.3 节）。因此，分量 $k$ 的 M 步方程，只是将一个逻辑回归模型拟合到加权数据集上，其中数据点 $n$ 的权重为 $\gamma_{nk}$。图 14.10 展示了将逻辑回归模型的混合应用于一个简单分类问题的例子。对于两个以上类别，将这一模型扩展为 softmax 模型的混合也很直接（习题 14.16）。

### 14.5.3 专家混合

在第 14.5.1 节中，我们考虑了线性回归模型的混合；在第 14.5.2 节中，讨论了类似的线性分类器混合。虽然这些简单的混合提高了线性模型的灵活性，使其能够表示更复杂的预测分布，例如多峰分布，但它们仍然有很大局限。可以允许混合系数本身成为输入变量的函数，进一步增强这类模型的能力，使得

$$
p(\mathbf{t}\mid\mathbf{x})=\sum_{k=1}^{K}\pi_k(\mathbf{x})p_k(\mathbf{t}\mid\mathbf{x}).
\tag{14.53}
$$

这称为*专家混合*模型（Jacobs et al.，1991），其中混合系数 $\pi_k(\mathbf{x})$ 称为*门控函数*（gating functions），各个分量密度 $p_k(\mathbf{t}\mid\mathbf{x})$ 称为*专家*（experts）。这一名称背后的想法是，不同分量可以对输入空间不同区域中的分布建模，也就是

<!-- pdf-page: 693 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-14/b-fig-14-10.png" alt="逻辑回归模型混合用于分类，三幅图比较真实类别概率、单模型与双分量混合"><figcaption>图 14.10：逻辑回归模型混合的示意图。左图显示从红、蓝两个类别中抽取的数据点，背景颜色从纯红色变化到纯蓝色，表示类别标记的真实概率。中图显示使用最大似然拟合单个逻辑回归模型的结果，背景颜色表示相应类别标记的概率。由于背景几乎是均匀的紫色，可以看出，在输入空间的大部分区域中，该模型都给两个类别各分配约 0.5 的概率。右图显示拟合两个逻辑回归模型的混合后的结果；现在，对于蓝色类别中的许多数据点，模型给正确标记分配了高得多的概率。</figcaption><p class="figure-translation">左图：真实类别概率；中图：单个逻辑回归模型；右图：两个逻辑回归模型的混合。红、蓝圆圈表示两个类别的数据点，背景颜色表示类别概率。</p></figure>

<!-- join-previous-paragraph-across-figures -->
说，它们是在各自区域中作出预测的“专家”；门控函数则决定哪些分量在哪个区域占主导地位。

门控函数 $\pi_k(\mathbf{x})$ 必须满足混合系数通常的约束，即 $0\leqslant\pi_k(\mathbf{x})\leqslant1$ 和 $\sum_k\pi_k(\mathbf{x})=1$。因此，例如可以用（4.104）和（4.105）形式的线性 softmax 模型来表示它们。如果各专家也是线性回归或线性分类模型，那么整个模型就可以使用 EM 算法高效拟合，并在 M 步中使用迭代重加权最小二乘（Jordan and Jacobs，1994）。

由于门控函数和专家函数都采用线性模型，这种模型仍然存在很大的局限。使用多层门控函数，就能得到灵活得多的*层次专家混合*，即 *HME* 模型（Jordan and Jacobs，1994）。为理解这一模型的结构，可以设想一种混合分布，其中每个混合分量本身又是一个混合分布。对于简单的无条件混合，这种层次混合很容易化为等价的单层混合分布（习题 14.17）。然而，当混合系数依赖于输入时，这个层次模型就不再如此简单。HME 模型也可以看作第 14.4 节讨论的决策树的概率版本；同样可以用 EM 算法进行高效的最大似然训练，并在 M 步中使用 IRLS（第 4.3.3 节）。Bishop and Svensén（2003）基于变分推断给出了 HME 的贝叶斯处理。

这里不详细讨论 HME。不过，需要指出它与第 5.6 节讨论的混合密度网络有密切联系。专家混合模型的主要优势在于，可以用 EM 进行优化，其中每个混合分量和门控模型的 M 步都涉及一个凸优化问题，尽管整体优化是非凸的。相比之下，混合密度网络方法的优势在于，分量

<!-- pdf-page: 694 -->
<!-- join-previous-paragraph -->
密度与混合系数共享神经网络的隐藏单元。此外，与层次专家混合相比，混合密度网络进一步放宽了对输入空间划分的限制：这些划分不仅是软划分、不受坐标轴对齐的约束，而且还可以是非线性的。

## 习题

**14.1（⋆⋆） www** 考虑一组形式为 $p(\mathbf{t}\mid\mathbf{x},\mathbf{z}_h,\boldsymbol{\theta}_h,h)$ 的模型，其中 $\mathbf{x}$ 是输入向量，$\mathbf{t}$ 是目标向量，$h$ 对不同模型编号，$\mathbf{z}_h$ 是模型 $h$ 的潜变量，$\boldsymbol{\theta}_h$ 是模型 $h$ 的参数集合。假设各模型的先验概率为 $p(h)$，并给定训练集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 和 $\mathbf{T}=\{\mathbf{t}_1,\ldots,\mathbf{t}_N\}$。写出计算预测分布 $p(\mathbf{t}\mid\mathbf{x},\mathbf{X},\mathbf{T})$ 所需的公式，其中潜变量和模型索引均被边缘化。利用这些公式，说明对不同模型进行贝叶斯平均与在单个模型内使用潜变量之间的区别。

**14.2（⋆）** 简单委员会模型的期望平方和误差 $E_{\mathrm{AV}}$ 可以由（14.10）定义，委员会本身的期望误差由（14.11）给出。假设各个模型的误差满足（14.12）和（14.13），推导结果（14.14）。

**14.3（⋆） www** 利用 Jensen 不等式（1.115），对凸函数 $f(x)=x^2$ 这一特殊情形，证明由（14.10）给出的简单委员会模型各成员的平均期望平方和误差 $E_{\mathrm{AV}}$，以及由（14.11）给出的委员会本身的期望误差 $E_{\mathrm{COM}}$，满足

$$
E_{\mathrm{COM}}\leqslant E_{\mathrm{AV}}.
\tag{14.54}
$$

**14.4（⋆⋆）** 利用 Jensen 不等式（1.115），证明上一题中推导的结果（14.54）对任意误差函数 $E(y)$ 都成立，而不仅限于平方和误差，只要它是 $y$ 的凸函数。

**14.5（⋆⋆） www** 考虑一个允许对成员模型采用不等权重的委员会，使得

$$
y_{\mathrm{COM}}(\mathbf{x})=\sum_{m=1}^{M}\alpha_m y_m(\mathbf{x}).
\tag{14.55}
$$

为保证预测 $y_{\mathrm{COM}}(\mathbf{x})$ 处于合理范围内，假设对于每个 $\mathbf{x}$，都要求预测值位于委员会所有成员给出的最小值与最大值之间，即

$$
y_{\min}(\mathbf{x})\leqslant y_{\mathrm{COM}}(\mathbf{x})\leqslant y_{\max}(\mathbf{x}).
\tag{14.56}
$$

证明，这一约束成立的充要条件是系数 $\alpha_m$ 满足

$$
\alpha_m\geqslant0,\qquad\sum_{m=1}^{M}\alpha_m=1.
\tag{14.57}
$$

<!-- pdf-page: 695 -->

**14.6（⋆） www** 对误差函数（14.23）关于 $\alpha_m$ 求导，证明 AdaBoost 算法中的参数 $\alpha_m$ 使用（14.17）更新，其中 $\epsilon_m$ 由（14.16）定义。

**14.7（⋆）** 对（14.27）给出的期望指数误差函数，关于所有可能的函数 $y(\mathbf{x})$ 作变分最小化，证明使其最小的函数由（14.28）给出。

**14.8（⋆）** 证明，AdaBoost 算法所最小化的指数误差函数（14.20），并不对应于任何性质良好的概率模型的对数似然。可以通过证明相应的条件分布 $p(t\mid\mathbf{x})$ 无法正确归一化来完成这一点。

**14.9（⋆） www** 证明，对于（14.21）形式的加性模型，按提升方法依次最小化平方和误差函数，只需将每个新的基分类器拟合到前一个模型的残差 $t_n-f_{m-1}(\mathbf{x}_n)$ 上。

**14.10（⋆）** 验证，如果最小化一组训练值 $\{t_n\}$ 与单个预测值 $t$ 之间的平方和误差，那么 $t$ 的最优解就是 $\{t_n\}$ 的平均值。

**14.11（⋆⋆）** 考虑一个包含类别 $\mathcal{C}_1$ 的 400 个数据点和类别 $\mathcal{C}_2$ 的 400 个数据点的数据集。假设树模型 A 将它们划分为：第一个叶节点包含 $(300,100)$，第二个叶节点包含 $(100,300)$，其中 $(n,m)$ 表示有 $n$ 个点被分到 $\mathcal{C}_1$，有 $m$ 个点被分到 $\mathcal{C}_2$。同样，假设另一个树模型 B 将它们划分为 $(200,400)$ 和 $(200,0)$。计算两棵树的误分类率，并据此证明它们相等。同样，计算两棵树的交叉熵（14.32）和 Gini 指数（14.33），并证明树 B 的这两个指标均低于树 A。

**14.12（⋆⋆）** 将第 14.5.1 节中线性回归模型混合的结果，扩展到由向量 $\mathbf{t}$ 描述的多个目标值的情形。为此，利用第 3.1.5 节的结果。

**14.13（⋆） www** 验证，线性回归模型混合的完整数据对数似然函数由（14.36）给出。

**14.14（⋆）** 使用拉格朗日乘子法（附录 E），证明通过最大似然 EM 训练的线性回归模型混合，其混合系数的 M 步重估方程由（14.38）给出。

**14.15（⋆） www** 前面已经指出，如果在回归问题中使用平方损失函数，那么对于一个新的输入向量，目标变量的相应最优预测由预测分布的条件均值给出。证明，第 14.5.1 节讨论的线性回归模型混合的条件均值，是各分量分布均值的线性组合。注意，如果目标数据的条件分布是多峰的，那么条件均值可能给出很差的预测。

<!-- pdf-page: 696 -->

**14.16（⋆⋆⋆）** 将第 14.5.2 节的逻辑回归混合模型，扩展为表示 $C\geqslant2$ 个类别的 softmax 分类器混合。写出通过最大似然确定该模型参数的 EM 算法。

**14.17（⋆⋆） www** 考虑一个条件分布 $p(t\mid\mathbf{x})$ 的混合模型，形式为

$$
p(t\mid\mathbf{x})=\sum_{k=1}^{K}\pi_k\psi_k(t\mid\mathbf{x})
\tag{14.58}
$$

其中，每个混合分量 $\psi_k(t\mid\mathbf{x})$ 本身又是一个混合模型。证明，这种两层的层次混合等价于常规的单层混合模型。现在假设，这种层次模型在两个层次上的混合系数都是 $\mathbf{x}$ 的任意函数。再次证明，该层次模型仍等价于一个混合系数依赖于 $\mathbf{x}$ 的单层模型。最后，考虑这样的情形：层次混合在两个层次上的混合系数都被限定为线性分类模型，即逻辑模型或 softmax 模型。证明，一般情况下，这种层次混合无法用混合系数由线性分类模型给出的单层混合表示。提示：为此，构造一个反例就足够了，因此可以考虑一个含两个分量的混合，其中一个分量本身又是两个分量的混合，混合系数由线性逻辑模型给出。证明，这种模型无法表示为一个含 3 个分量、混合系数由线性 softmax 模型确定的单层混合。
