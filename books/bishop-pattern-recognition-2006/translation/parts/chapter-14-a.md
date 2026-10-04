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
