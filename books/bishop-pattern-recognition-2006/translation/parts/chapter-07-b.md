<!-- pdf-page: 364 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-8.png" alt="采用高斯核的ν-SVM对正弦数据的回归预测与支持向量"><figcaption>图 7.8：将用于回归的 $\nu$-SVM 应用于正弦合成数据集的示例，采用高斯核。红色线为预测的回归曲线，阴影区域对应于 $\epsilon$ 不敏感管道。数据点以绿色表示，其中对应支持向量的数据点用蓝色圆圈标出。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

### 7.1.5 计算学习理论

从历史上看，支持向量机的提出和分析在很大程度上基于一种称为*计算学习理论*（computational learning theory）的理论框架，它有时也称为*统计学习理论*（statistical learning theory）（Anthony and Biggs, 1992; Kearns and Vazirani, 1994; Vapnik, 1995; Vapnik, 1998）。它起源于 Valiant（1984）提出的*概率近似正确*（probably approximately correct，PAC）学习框架。PAC 框架的目标是理解：要获得良好的泛化能力，需要多大的数据集。它还给出学习所需计算成本的界，不过这里不讨论这一点。

假设大小为 $N$ 的数据集 $\mathcal{D}$ 从某个联合分布 $p(\mathbf{x},t)$ 中抽取，其中 $\mathbf{x}$ 是输入变量，$t$ 表示类别标记。我们将注意力限制在“无噪声”的情况，即类别标记由某个未知的确定性函数 $t=g(\mathbf{x})$ 决定。在 PAC 学习中，根据训练集 $\mathcal{D}$，从函数空间 $\mathcal{F}$ 中选择函数 $f(\mathbf{x};\mathcal{D})$。如果它的期望错误率低于某个预先指定的阈值 $\epsilon$，即

$$
\mathbb{E}_{\mathbf{x},t}\left[I\left(f(\mathbf{x};\mathcal{D})\ne t\right)\right]<\epsilon
\tag{7.75}
$$

就说它具有良好的泛化能力。这里 $I(\cdot)$ 是指示函数，期望关于分布 $p(\mathbf{x},t)$ 计算。左端的量是随机变量，因为它依赖于训练集 $\mathcal{D}$；PAC 框架要求，对于从 $p(\mathbf{x},t)$ 随机抽取的数据集 $\mathcal{D}$，（7.75）以大于 $1-\delta$ 的概率成立。这里 $\delta$ 是另一个预先指定的参数。“概率近似正确”这一名称，来自这样的要求：以很高的概率，大于 $1-\delta$，使错误率很小，小于 $\epsilon$。对于给定的模型空间 $\mathcal{F}$，以及给定的参数 $\epsilon$ 和 $\delta$，PAC 学习旨在为满足这一准则所需的最小数据集大小 $N$ 提供界。PAC 学习中的一个关键量是 *Vapnik–Chervonenkis 维数*，简称 *VC 维*；它衡量函数空间的复杂度，并使 PAC 框架能够扩展到包含无穷多个函数的空间。

PAC 框架中推导出的界通常被称为最坏

<!-- pdf-page: 365 -->

<!-- join-previous-paragraph -->
情况下的界，因为它们适用于分布 $p(\mathbf{x},t)$ 的任意选择，只要训练样本和测试样本都从同一分布中独立抽取；它们也适用于函数 $f(\mathbf{x})$ 的任意选择，只要该函数属于 $\mathcal{F}$。在现实世界的机器学习应用中，所处理的分布通常具有明显的规律，例如，输入空间的大片区域具有相同的类别标记。由于不对分布形式作任何假设，PAC 界非常保守；换言之，它们会严重高估达到给定泛化性能所需的数据集大小。因此，PAC 界在实际应用中即使有所使用，也很少见。

一种使 PAC 界更紧的尝试是 PAC–Bayesian 框架（McAllester, 2003）。它考虑函数空间 $\mathcal{F}$ 上的一个分布，这与贝叶斯处理中的先验有些类似。它仍然考虑 $p(\mathbf{x},t)$ 的任意可能选择，因此，虽然所得的界更紧，但仍然非常保守。

## 7.2 相关向量机

支持向量机已被用于多种分类和回归应用。不过，它有若干局限，本章已经强调了其中几项。特别是，SVM 的输出表示决策，而不是后验概率。另外，SVM 最初是针对二类问题提出的，扩展到 $K>2$ 个类别时会遇到困难。复杂度参数 $C$ 或 $\nu$，以及回归中的参数 $\epsilon$，必须通过交叉验证等留出方法来确定。最后，预测表示为核函数的线性组合，这些核函数以训练数据点为中心，而且必须是正定的。

*相关向量机*（relevance vector machine，RVM）（Tipping, 2001）是一种用于回归和分类的贝叶斯稀疏核技术。它具有 SVM 的许多特征，同时避免了 SVM 的主要局限。此外，它通常能得到稀疏得多的模型，因此在测试数据上的计算速度相应更快，同时保持相近的泛化误差。

与介绍 SVM 时不同，先介绍 RVM 的回归形式，再考虑如何扩展到分类任务，会更加方便。

### 7.2.1 用于回归的 RVM

用于回归的相关向量机，是第 3 章研究过的那种线性模型，但使用了经过修改的先验，从而得到稀疏解。给定输入向量 $\mathbf{x}$，模型为实值目标变量 $t$ 定义如下条件分布：

$$
p(t\mid\mathbf{x},\mathbf{w},\beta)=\mathcal{N}(t\mid y(\mathbf{x}),\beta^{-1})
\tag{7.76}
$$

<!-- pdf-page: 366 -->

其中 $\beta=\sigma^{-2}$ 是噪声精度，即噪声方差的倒数，均值由如下形式的线性模型给出：

$$
y(\mathbf{x})=\sum_{i=1}^{M}w_i\phi_i(\mathbf{x})=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{7.77}
$$

其中非线性基函数 $\phi_i(\mathbf{x})$ 固定不变，通常还包含一个常数项，使相应的权重参数表示“偏置”。

相关向量机是这个模型的一个具体实例，其结构意在与支持向量机相对应。具体来说，基函数由核给出，训练集中的每个数据点都关联一个核。于是，一般表达式（7.77）具有类似 SVM 的形式：

$$
y(\mathbf{x})=\sum_{n=1}^{N}w_n k(\mathbf{x},\mathbf{x}_n)+b
\tag{7.78}
$$

其中 $b$ 是偏置参数。此时参数数目为 $M=N+1$，$y(\mathbf{x})$ 与 SVM 的预测模型（7.64）形式相同，只是这里将系数 $a_n$ 记为 $w_n$。应强调的是，后续分析对任意基函数选择都成立；为保持一般性，我们将使用（7.77）的形式。与 SVM 不同，这里不局限于正定核，基函数的数目和位置也不必与训练数据点绑定。

假设给定输入向量 $\mathbf{x}$ 的 $N$ 个观测，将它们统记为数据矩阵 $\mathbf{X}$，其第 $n$ 行为 $\mathbf{x}_n^{\mathrm T}$，其中 $n=1,\ldots,N$。相应的目标值为 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。于是，似然函数为

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)=\prod_{n=1}^{N}p(t_n\mid\mathbf{x}_n,\mathbf{w},\beta^{-1}).
\tag{7.79}
$$

接下来为参数向量 $\mathbf{w}$ 引入先验分布。与第 3 章一样，考虑零均值的高斯先验。不过，RVM 的关键区别在于：为每个权重参数 $w_i$ 分别引入超参数 $\alpha_i$，而不是共享单个超参数。因此，权重先验具有如下形式：

$$
p(\mathbf{w}\mid\boldsymbol{\alpha})=\prod_{i=1}^{M}\mathcal{N}(w_i\mid0,\alpha_i^{-1})
\tag{7.80}
$$

其中 $\alpha_i$ 表示相应参数 $w_i$ 的精度，$\boldsymbol{\alpha}$ 表示 $(\alpha_1,\ldots,\alpha_M)^{\mathrm T}$。我们将看到，当关于这些超参数最大化证据时，其中相当大一部分会趋于无穷大，相应权重参数的后验分布则集中于零。因此，与这些参数关联的基函数在

<!-- pdf-page: 367 -->

<!-- join-previous-paragraph -->
模型作出的预测中不起作用，实际上就被剪除，从而得到稀疏模型。

利用线性回归模型的结果（3.49），可知权重的后验分布仍然是高斯分布，形式为

$$
p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\mathbf{X},\boldsymbol{\alpha},\beta)=\mathcal{N}(\mathbf{w}\mid\mathbf{m},\boldsymbol{\Sigma})
\tag{7.81}
$$

其中均值和协方差分别为

$$
\mathbf{m}=\beta\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{7.82}
$$

$$
\boldsymbol{\Sigma}=(\mathbf{A}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}
\tag{7.83}
$$

这里 $\boldsymbol{\Phi}$ 是一个 $N\times M$ 设计矩阵，元素为 $\Phi_{ni}=\phi_i(\mathbf{x}_n)$，而 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。注意，对于模型（7.78）这一特殊情况，有 $\boldsymbol{\Phi}=\mathbf{K}$，其中 $\mathbf{K}$ 是元素为 $k(\mathbf{x}_n,\mathbf{x}_m)$ 的对称 $(N+1)\times(N+1)$ 核矩阵。

$\boldsymbol{\alpha}$ 和 $\beta$ 的值通过第二类最大似然确定，也称为证据近似（3.5 节）。在这一方法中，通过对权重参数积分消元得到边缘似然函数，再将其最大化：

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\boldsymbol{\alpha},\beta)=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\alpha})\,d\mathbf{w}.
\tag{7.84}
$$

由于这表示两个高斯分布的卷积，很容易计算（习题 7.10），得到如下形式的对数边缘似然：

$$
\begin{aligned}
\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\boldsymbol{\alpha},\beta)&=\ln\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\mathbf{0},\mathbf{C})\\
&=-\frac{1}{2}\{N\ln(2\pi)+\ln|\mathbf{C}|+\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\mathsf{t}}\}
\end{aligned}
\tag{7.85}
$$

其中 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$，并定义了如下 $N\times N$ 矩阵 $\mathbf{C}$：

$$
\mathbf{C}=\beta^{-1}\mathbf{I}+\boldsymbol{\Phi}\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}.
\tag{7.86}
$$

现在的目标是关于超参数 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化（7.85）。这只需对 3.5 节中线性回归模型的证据近似结果稍作修改。同样可以采用两种方法。第一种方法是直接令边缘似然的相应导数为零，得到以下重估方程（习题 7.12）：

$$
\alpha_i^{\mathrm{new}}=\frac{\gamma_i}{m_i^2}
\tag{7.87}
$$

$$
(\beta^{\mathrm{new}})^{-1}=\frac{\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}\|^2}{N-\sum_i\gamma_i}
\tag{7.88}
$$

其中 $m_i$ 是（7.82）定义的后验均值 $\mathbf{m}$ 的第 $i$ 个分量。量 $\gamma_i$ 衡量相应参数 $w_i$ 被数据确定的程度（3.5.3 节），其定义为

<!-- pdf-page: 368 -->

$$
\gamma_i=1-\alpha_i\Sigma_{ii}
\tag{7.89}
$$

其中 $\Sigma_{ii}$ 是（7.83）给出的后验协方差 $\boldsymbol{\Sigma}$ 的第 $i$ 个对角元素。因此，学习过程如下：先选择 $\boldsymbol{\alpha}$ 和 $\beta$ 的初始值，分别利用（7.82）和（7.83）计算后验分布的均值与协方差，再交替执行超参数重估和后验均值、协方差的重估；前者使用（7.87）和（7.88），后者使用（7.82）和（7.83），直到满足适当的收敛准则。

第二种方法使用 EM 算法，将在 9.3.4 节讨论。这两种寻找使证据最大的超参数值的方法在形式上等价（习题 9.23）。不过，从数值计算看，与（7.87）和（7.88）对应的直接优化方法收敛稍快（Tipping, 2001）。

优化的结果是，一部分超参数 $\{\alpha_i\}$ 被推向很大的值，原则上为无穷大（7.2.2 节），因此对应权重参数 $w_i$ 的后验分布，其均值和方差都为零。于是，这些参数和相应基函数 $\phi_i(\mathbf{x})$ 被从模型中删除，在对新输入作预测时不起作用。对于（7.78）形式的模型，剩余非零权重对应的输入 $\mathbf{x}_n$ 称为*相关向量*（relevance vectors），因为它们通过自动相关性确定机制识别出来，与 SVM 的支持向量类似。不过，需要强调的是，这种通过自动相关性确定在概率模型中实现稀疏性的机制相当一般，可用于任何表示为基函数可调线性组合的模型。

找到使边缘似然最大的超参数值 $\boldsymbol{\alpha}^{\star}$ 和 $\beta^{\star}$ 后，就可以计算新输入 $\mathbf{x}$ 对应的 $t$ 的预测分布。利用（7.76）和（7.81），得到（习题 7.14）

$$
\begin{aligned}
p(t\mid\mathbf{x},\mathbf{X},\boldsymbol{\mathsf{t}},\boldsymbol{\alpha}^{\star},\beta^{\star})&=\int p(t\mid\mathbf{x},\mathbf{w},\beta^{\star})p(\mathbf{w}\mid\mathbf{X},\boldsymbol{\mathsf{t}},\boldsymbol{\alpha}^{\star},\beta^{\star})\,d\mathbf{w}\\
&=\mathcal{N}\left(t\mid\mathbf{m}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}),\sigma^2(\mathbf{x})\right).
\end{aligned}
\tag{7.90}
$$

因此，预测均值由（7.76）给出，其中将 $\mathbf{w}$ 设为后验均值 $\mathbf{m}$；预测分布的方差为

$$
\sigma^2(\mathbf{x})=(\beta^{\star})^{-1}+\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\Sigma}\boldsymbol{\phi}(\mathbf{x})
\tag{7.91}
$$

其中 $\boldsymbol{\Sigma}$ 由（7.83）给出，并将其中的 $\boldsymbol{\alpha}$ 和 $\beta$ 设为优化后的值 $\boldsymbol{\alpha}^{\star}$ 和 $\beta^{\star}$。这就是在线性回归背景下得到的熟悉结果（3.59）。回顾一下，对于局部化基函数，线性回归模型的预测方差会在输入空间中没有基函数的区域变小。对于基函数以数据点为中心的 RVM，在数据范围之外进行外推时，模型会对自己的预测越来越确信（Rasmussen and Quiñonero-Candela, 2005），这当然是不希望发生的。高斯过程回归中的预测分布（6.4.2 节）没有

<!-- pdf-page: 369 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-9.png" alt="相关向量机回归的预测均值、一个标准差区间及三个相关向量"><figcaption>图 7.9：RVM 回归示例，使用与图 7.8 中 $\nu$-SVM 回归模型相同的数据集和高斯核函数。红色线表示 RVM 预测分布的均值，阴影区域表示预测分布的一个标准差范围。数据点以绿色表示，相关向量用蓝色圆圈标出。注意，这里只有 3 个相关向量，而图 7.8 中的 $\nu$-SVM 有 7 个支持向量。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
这一问题。不过，高斯过程作预测的计算成本通常比 RVM 高得多。

图 7.9 给出了将 RVM 应用于正弦回归数据集的一个例子。这里，噪声精度参数 $\beta$ 也通过证据最大化来确定。可以看到，RVM 中的相关向量数目明显少于 SVM 使用的支持向量数目。在广泛的回归和分类任务中，RVM 所得模型的规模通常比相应支持向量机小一个数量级，从而显著提高处理测试数据的速度。引人注意的是，与相应的 SVM 相比，泛化误差几乎没有降低或完全未降低，却实现了这种更强的稀疏性。

与 SVM 相比，RVM 的主要缺点是训练涉及非凸函数的优化，而且训练时间可能比相当的 SVM 更长。对于具有 $M$ 个基函数的模型，RVM 需要求一个 $M\times M$ 矩阵的逆，通常需要 $O(M^3)$ 的计算量。在类似 SVM 的模型（7.78）这一特殊情况下，有 $M=N+1$。前面已经指出，一些 SVM 训练技术的计算成本大致随 $N$ 的平方增长。当然，对于 RVM，始终可以选择从少于 $N+1$ 个基函数开始。更重要的是，在相关向量机中，控制复杂度和噪声方差的参数通过一次训练就能自动确定；而在支持向量机中，参数 $C$ 和 $\epsilon$（或 $\nu$）一般通过交叉验证来确定，这涉及多次训练。此外，下一节将推导相关向量机的另一种训练过程，它能显著提高训练速度。

### 7.2.2 稀疏性分析

前面已经指出，自动相关性确定机制使一部分参数被推向零。现在更详细地研究

<!-- pdf-page: 370 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-10.png" alt="与目标向量方向不一致的基向量如何使贝叶斯线性回归选择稀疏解"><figcaption>图 7.10：贝叶斯线性回归模型中稀疏性机制的示意图。叉号表示训练集目标值向量 $\boldsymbol{\mathsf{t}}=(t_1,t_2)^{\mathrm T}$；模型只有一个基向量 $\boldsymbol{\varphi}=(\phi(\mathbf{x}_1),\phi(\mathbf{x}_2))^{\mathrm T}$，其方向与目标数据向量 $\boldsymbol{\mathsf{t}}$ 的方向相差较大。左图的模型只有各向同性噪声，因此 $\mathbf{C}=\beta^{-1}\mathbf{I}$，对应于 $\alpha=\infty$，并将 $\beta$ 设为其最可能的值。右图是相同的模型，但 $\alpha$ 取有限值。两幅图中的红色椭圆都对应于单位马氏距离（Mahalanobis distance），并且 $|\mathbf{C}|$ 的值相同；绿色虚线圆表示噪声项 $\beta^{-1}$ 的贡献。可以看到，$\alpha$ 的任何有限取值都会降低观测数据的概率，因此，在最可能的解中，这个基向量被移除。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
相关向量机中的稀疏性机制。在这一过程中，将得到一个优化超参数的过程，其速度比前面给出的直接方法快得多。

在进行数学分析之前，先对贝叶斯线性模型中稀疏性的来源作一些直观说明。考虑一个包含 $N=2$ 个观测 $t_1$、$t_2$ 的数据集，模型具有单个基函数 $\phi(\mathbf{x})$、超参数 $\alpha$，以及精度为 $\beta$ 的各向同性噪声。由（7.85），边缘似然为 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\mathbf{0},\mathbf{C})$，其中协方差矩阵的形式为

$$
\mathbf{C}=\frac{1}{\beta}\mathbf{I}+\frac{1}{\alpha}\boldsymbol{\varphi}\boldsymbol{\varphi}^{\mathrm T}
\tag{7.92}
$$

这里 $\boldsymbol{\varphi}$ 表示 $N$ 维向量 $(\phi(\mathbf{x}_1),\phi(\mathbf{x}_2))^{\mathrm T}$，类似地，$\boldsymbol{\mathsf{t}}=(t_1,t_2)^{\mathrm T}$。注意，这就是 $\mathbf{t}$ 上均值为零、协方差为 $\mathbf{C}$ 的高斯过程模型。给定 $\mathbf{t}$ 的某个观测，目标是通过最大化边缘似然，求得 $\alpha^{\star}$ 和 $\beta^{\star}$。由图 7.10 可以看到，如果 $\boldsymbol{\varphi}$ 的方向与训练数据向量 $\mathbf{t}$ 的方向相差较大，那么相应超参数 $\alpha$ 就会被推向 $\infty$，该基向量将从模型中被剪除。这是因为，只要 $\beta$ 设为其最优值，$\alpha$ 的任何有限取值都会给数据分配更低的概率，从而降低 $\boldsymbol{\mathsf{t}}$ 处的密度值。可以看到，$\alpha$ 取任何有限值都会使分布沿着偏离数据的方向拉长，从而增加远离观测数据区域的概率质量，降低目标数据向量本身所在位置的密度值。对于具有 $M$ 个

<!-- pdf-page: 371 -->

<!-- join-previous-paragraph -->
基向量 $\boldsymbol{\varphi}_1,\ldots,\boldsymbol{\varphi}_M$ 的更一般情况，也有类似的直观解释：如果某个基向量与数据向量 $\mathbf{t}$ 的方向相差较大，它就很可能从模型中被剪除。

现在，对于包含 $M$ 个基函数的一般情况，从更严格的数学角度研究稀疏性机制。为引出这一分析，先注意，在重估参数 $\alpha_i$ 的结果（7.87）中，右端各项本身也是 $\alpha_i$ 的函数。因此，这些结果给出的是隐式解；即使固定所有其他 $\alpha_j$（$j\ne i$），只确定单个 $\alpha_i$，也需要迭代。

这提示了求解 RVM 优化问题的另一种方法：显式写出边缘似然（7.85）对某个 $\alpha_i$ 的全部依赖，再显式求出其驻点（Faul and Tipping, 2002; Tipping and Faul, 2003）。为此，先从（7.86）定义的矩阵 $\mathbf{C}$ 中分离出 $\alpha_i$ 的贡献，得到

$$
\begin{aligned}
\mathbf{C}&=\beta^{-1}\mathbf{I}+\sum_{j\ne i}\alpha_j^{-1}\boldsymbol{\varphi}_j\boldsymbol{\varphi}_j^{\mathrm T}+\alpha_i^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}\\
&=\mathbf{C}_{-i}+\alpha_i^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}
\end{aligned}
\tag{7.93}
$$

其中 $\boldsymbol{\varphi}_i$ 表示 $\boldsymbol{\Phi}$ 的第 $i$ 列，即元素为 $(\phi_i(\mathbf{x}_1),\ldots,\phi_i(\mathbf{x}_N))$ 的 $N$ 维向量；它不同于表示 $\boldsymbol{\Phi}$ 第 $n$ 行的 $\boldsymbol{\phi}_n$。矩阵 $\mathbf{C}_{-i}$ 表示从矩阵 $\mathbf{C}$ 中去掉基函数 $i$ 的贡献所得的矩阵。利用矩阵恒等式（C.7）和（C.15），可以将 $\mathbf{C}$ 的行列式和逆矩阵写为

$$
|\mathbf{C}|=|\mathbf{C}_{-i}|\,|1+\alpha_i^{-1}\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i|
\tag{7.94}
$$

$$
\mathbf{C}^{-1}=\mathbf{C}_{-i}^{-1}-\frac{\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}}{\alpha_i+\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i}.
\tag{7.95}
$$

利用这些结果，就可以将对数边缘似然函数（7.85）写成如下形式（习题 7.15）：

$$
L(\boldsymbol{\alpha})=L(\boldsymbol{\alpha}_{-i})+\lambda(\alpha_i)
\tag{7.96}
$$

其中 $L(\boldsymbol{\alpha}_{-i})$ 就是去掉基函数 $\boldsymbol{\varphi}_i$ 后的对数边缘似然，而量 $\lambda(\alpha_i)$ 定义为

$$
\lambda(\alpha_i)=\frac{1}{2}\left[\ln\alpha_i-\ln(\alpha_i+s_i)+\frac{q_i^2}{\alpha_i+s_i}\right]
\tag{7.97}
$$

它包含对 $\alpha_i$ 的全部依赖。这里引入了两个量

$$
s_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i
\tag{7.98}
$$

$$
q_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\mathsf{t}}.
\tag{7.99}
$$

其中 $s_i$ 称为 $\boldsymbol{\varphi}_i$ 的*稀疏度*（sparsity），$q_i$ 称为其*质量*（quality）。我们将看到，相对于 $q_i$ 的值，$s_i$ 越大，就意味着基函数 $\boldsymbol{\varphi}_i$

<!-- pdf-page: 372 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-11.png" alt="质量与稀疏度两种相对大小下，对数边缘似然的有限及无穷大最优超参数"><figcaption>图 7.11：对数边缘似然 $\lambda(\alpha_i)$ 随 $\ln\alpha_i$ 变化的曲线。左图中，$q_i^2=4$、$s_i=1$，因此 $q_i^2>s_i$，在有限的 $\alpha_i$ 处有唯一极大值；右图中，$q_i^2=1$、$s_i=2$，因此 $q_i^2<s_i$，极大值在 $\alpha_i=\infty$ 处取得。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
越有可能从模型中被剪除。“稀疏度”衡量基函数 $\boldsymbol{\varphi}_i$ 与模型中其他基向量的重叠程度；“质量”则衡量基向量 $\boldsymbol{\varphi}_n$ 的方向与一种误差方向的一致程度，这种误差是训练集目标值 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$ 与去掉向量 $\boldsymbol{\varphi}_i$ 后模型所给预测向量 $\boldsymbol{\mathsf{y}}_{-i}$ 之间的差（Tipping and Faul, 2003）。

边缘似然关于 $\alpha_i$ 的驻点，出现在导数

$$
\frac{d\lambda(\alpha_i)}{d\alpha_i}=\frac{\alpha_i^{-1}s_i^2-(q_i^2-s_i)}{2(\alpha_i+s_i)^2}
\tag{7.100}
$$

等于零的位置。解有两种可能的形式。回顾 $\alpha_i\geqslant0$，可以看到，如果 $q_i^2<s_i$，那么 $\alpha_i\to\infty$ 给出一个解。反之，如果 $q_i^2>s_i$，就可以解出 $\alpha_i$：

$$
\alpha_i=\frac{s_i^2}{q_i^2-s_i}.
\tag{7.101}
$$

图 7.11 展示了这两种解。可以看到，质量项与稀疏度项的相对大小，决定某个基向量是否会从模型中被剪除。基于边缘似然二阶导数的更完整分析（Faul and Tipping, 2002），确认这些解确实是 $\lambda(\alpha_i)$ 的唯一极大值（习题 7.16）。

注意，对于给定的其他超参数值，这种方法给出了 $\alpha_i$ 的闭式解。除了帮助理解 RVM 中稀疏性的来源，这一分析还导出一种优化超参数的实用算法，具有显著的速度优势。它使用一组固定的候选基向量，依次循环考察它们，决定是否将每个向量纳入模型。所得的顺序稀疏贝叶斯学习算法如下。

<aside class="procedure">
<h3>顺序稀疏贝叶斯学习算法</h3>
<ol>
<li>如果求解的是回归问题，初始化 $\beta$。</li>
<li>使用一个基函数 $\boldsymbol{\varphi}_1$ 初始化，并利用（7.101）设置超参数 $\alpha_1$；其余超参数 $\alpha_j$（$j\ne i$）初始化为无穷大，使模型中仅包含 $\boldsymbol{\varphi}_1$。</li>
</ol>
</aside>

<!-- pdf-page: 373 -->

<!-- join-previous-procedure -->
<aside class="procedure">
<ol start="3">
<li>计算 $\boldsymbol{\Sigma}$ 和 $\mathbf{m}$，以及所有基函数的 $q_i$ 和 $s_i$。</li>
<li>选择一个候选基函数 $\boldsymbol{\varphi}_i$。</li>
<li>如果 $q_i^2>s_i$ 且 $\alpha_i<\infty$，即基向量 $\boldsymbol{\varphi}_i$ 已经包含在模型中，则利用（7.101）更新 $\alpha_i$。</li>
<li>如果 $q_i^2>s_i$ 且 $\alpha_i=\infty$，则将 $\boldsymbol{\varphi}_i$ 加入模型，并利用（7.101）计算超参数 $\alpha_i$。</li>
<li>如果 $q_i^2\leqslant s_i$ 且 $\alpha_i<\infty$，则将基函数 $\boldsymbol{\varphi}_i$ 从模型中移除，并令 $\alpha_i=\infty$。</li>
<li>如果求解的是回归问题，更新 $\beta$。</li>
<li>如果已经收敛，则终止；否则返回第 3 步。</li>
</ol>
</aside>

注意，如果 $q_i^2\leqslant s_i$ 且 $\alpha_i=\infty$，那么基函数 $\boldsymbol{\varphi}_i$ 本来就没有包含在模型中，无需采取任何操作。

在实际计算中，先计算下列量比较方便：

$$
Q_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\mathsf{t}}
\tag{7.102}
$$

$$
S_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\varphi}_i.
\tag{7.103}
$$

随后，可以将质量和稀疏度变量表示为

$$
q_i=\frac{\alpha_i Q_i}{\alpha_i-S_i}
\tag{7.104}
$$

$$
s_i=\frac{\alpha_i S_i}{\alpha_i-S_i}.
\tag{7.105}
$$

注意，当 $\alpha_i=\infty$ 时，有 $q_i=Q_i$ 且 $s_i=S_i$。利用（C.7），可以写出（习题 7.17）

$$
Q_i=\beta\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\mathsf{t}}-\beta^2\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\Phi}\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{7.106}
$$

$$
S_i=\beta\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\varphi}_i-\beta^2\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\Phi}\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\varphi}_i
\tag{7.107}
$$

其中 $\boldsymbol{\Phi}$ 和 $\boldsymbol{\Sigma}$ 只涉及与有限超参数 $\alpha_i$ 对应的基向量。因此，每个阶段所需计算量为 $O(M^3)$，其中 $M$ 为模型中活跃基向量的数目，通常远小于训练模式的数目 $N$。

### 7.2.3 用于分类的 RVM

将权重的 ARD 先验用于第 4 章研究过的概率线性分类模型，就可以将相关向量机框架扩展到分类问题。首先考虑目标变量为二元变量 $t\in\{0,1\}$ 的二类问题。现在，模型采用基函数的线性组合，再通过 logistic sigmoid 函数变换的形式：

$$
y(\mathbf{x},\mathbf{w})=\sigma\left(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})\right)
\tag{7.108}
$$

<!-- pdf-page: 374 -->

其中 $\sigma(\cdot)$ 是（4.59）定义的 logistic sigmoid 函数。如果为权重向量 $\mathbf{w}$ 引入高斯先验，就得到第 4 章已经考虑过的模型。这里的区别在于，RVM 使用 ARD 先验（7.80），每个权重参数都关联一个独立的精度超参数。

与回归模型不同，现在无法再对参数向量 $\mathbf{w}$ 进行解析积分。这里遵循 Tipping（2001）的方法，使用拉普拉斯近似（4.4 节）；4.5.1 节已将它用于密切相关的贝叶斯逻辑回归问题。

首先初始化超参数向量 $\boldsymbol{\alpha}$。对于给定的 $\boldsymbol{\alpha}$，构建后验分布的高斯近似，进而得到边缘似然的近似。最大化这个近似边缘似然，就得到重估后的 $\boldsymbol{\alpha}$，重复这一过程直到收敛。

更详细地考察这个模型的拉普拉斯近似。对于固定的 $\boldsymbol{\alpha}$，通过最大化下式，求得 $\mathbf{w}$ 的后验分布的众数：

$$
\begin{aligned}
\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})&=\ln\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\alpha})\}-\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha})\\
&=\sum_{n=1}^{N}\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}-\frac{1}{2}\mathbf{w}^{\mathrm T}\mathbf{A}\mathbf{w}+\mathrm{const}
\end{aligned}
\tag{7.109}
$$

其中 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。这可以通过 4.3.3 节讨论的迭代重加权最小二乘（IRLS）完成。为此，需要对数后验分布的梯度向量和 Hessian 矩阵，由（7.109）可得（习题 7.18）

$$
\nabla\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})=\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{t}}-\boldsymbol{\mathsf{y}})-\mathbf{A}\mathbf{w}
\tag{7.110}
$$

$$
\nabla\nabla\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})=-(\boldsymbol{\Phi}^{\mathrm T}\mathbf{B}\boldsymbol{\Phi}+\mathbf{A})
\tag{7.111}
$$

其中 $\mathbf{B}$ 是 $N\times N$ 对角矩阵，对角元素为 $b_n=y_n(1-y_n)$，向量 $\boldsymbol{\mathsf{y}}=(y_1,\ldots,y_N)^{\mathrm T}$，$\boldsymbol{\Phi}$ 是元素为 $\Phi_{ni}=\phi_i(\mathbf{x}_n)$ 的设计矩阵。这里使用了 logistic sigmoid 函数导数的性质（4.88）。当 IRLS 算法收敛时，Hessian 矩阵的负值就是后验分布高斯近似的协方差矩阵的逆。

所得后验近似的众数，对应于高斯近似的均值，通过令（7.110）为零来求得。由此得到拉普拉斯近似的均值和协方差：

$$
\mathbf{w}^{\star}=\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{t}}-\boldsymbol{\mathsf{y}})
\tag{7.112}
$$

$$
\boldsymbol{\Sigma}=(\boldsymbol{\Phi}^{\mathrm T}\mathbf{B}\boldsymbol{\Phi}+\mathbf{A})^{-1}.
\tag{7.113}
$$

现在可以用这个拉普拉斯近似计算边缘似然。利用通过拉普拉斯近似计算积分的一般结果（4.135），

<!-- pdf-page: 375 -->

<!-- join-previous-paragraph -->
得到

$$
\begin{aligned}
p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha})&=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\alpha})\,d\mathbf{w}\\
&\simeq p(\boldsymbol{\mathsf{t}}\mid\mathbf{w}^{\star})p(\mathbf{w}^{\star}\mid\boldsymbol{\alpha})(2\pi)^{M/2}|\boldsymbol{\Sigma}|^{1/2}.
\end{aligned}
\tag{7.114}
$$

代入 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w}^{\star})$ 和 $p(\mathbf{w}^{\star}\mid\boldsymbol{\alpha})$，再令边缘似然关于 $\alpha_i$ 的导数等于零，得到（习题 7.19）

$$
-\frac{1}{2}(w_i^{\star})^2+\frac{1}{2\alpha_i}-\frac{1}{2}\Sigma_{ii}=0.
\tag{7.115}
$$

定义 $\gamma_i=1-\alpha_i\Sigma_{ii}$ 并整理，得到

$$
\alpha_i^{\mathrm{new}}=\frac{\gamma_i}{(w_i^{\star})^2}
\tag{7.116}
$$

这与用于回归的 RVM 所得到的重估公式（7.87）相同。

如果定义

$$
\widehat{\boldsymbol{\mathsf{t}}}=\boldsymbol{\Phi}\mathbf{w}^{\star}+\mathbf{B}^{-1}(\boldsymbol{\mathsf{t}}-\mathbf{y})
\tag{7.117}
$$

就可以将近似对数边缘似然写成

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha},\beta)=-\frac{1}{2}\left\{N\ln(2\pi)+\ln|\mathbf{C}|+(\widehat{\boldsymbol{\mathsf{t}}})^{\mathrm T}\mathbf{C}^{-1}\widehat{\boldsymbol{\mathsf{t}}}\right\}
\tag{7.118}
$$

其中

$$
\mathbf{C}=\mathbf{B}+\boldsymbol{\Phi}\mathbf{A}\boldsymbol{\Phi}^{\mathrm T}.
\tag{7.119}
$$

它与回归情况下的（7.85）具有相同形式，因此可以应用相同的稀疏性分析，得到相同的快速学习算法：每一步都充分优化一个超参数 $\alpha_i$。

图 7.12 给出了将相关向量机应用于合成分类数据集的结果（附录 A）。与支持向量机不同，相关向量往往不位于决策边界附近。这与前面对 RVM 稀疏性的讨论一致，因为以边界附近数据点为中心的基函数 $\phi_i(\mathbf{x})$，其向量 $\boldsymbol{\varphi}_i$ 的方向与训练数据向量 $\boldsymbol{\mathsf{t}}$ 的方向相差较大。

与 SVM 相比，相关向量机的一项潜在优点是它能给出概率预测。例如，这使得 RVM 可以辅助构建发射密度，用于线性动态系统的一种非线性扩展，从而在视频序列中跟踪人脸（Williams et al., 2005；13.3 节）。

到目前为止，考虑的都是用于二类分类问题的 RVM。对于 $K>2$ 个类别，再次利用 4.3.4 节的概率方法，其中有 $K$ 个如下形式的线性模型：

$$
a_k=\mathbf{w}_k^{\mathrm T}\mathbf{x}
\tag{7.120}
$$

<!-- pdf-page: 376 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-12.png" alt="相关向量机的分类边界、相关向量及类别后验概率"><figcaption>图 7.12：相关向量机应用于一个合成数据集的示例。左图给出决策边界和数据点，相关向量用圆圈标出。与图 7.4 中相应支持向量机的结果相比，可以看到 RVM 给出的模型要稀疏得多。右图给出 RVM 输出的后验概率，其中红色（蓝色）颜料所占的比例，表示该点属于红色（蓝色）类别的概率。</figcaption><p class="figure-translation">左图中的红色与蓝色叉号表示两个类别的数据点，绿色圆圈标出相关向量，黑线表示决策边界；右图中红色与蓝色的比例表示相应类别的后验概率。</p></figure>

这些模型通过 softmax 函数组合起来，得到输出

$$
y_k(\mathbf{x})=\frac{\exp(a_k)}{\sum_j\exp(a_j)}.
\tag{7.121}
$$

相应的对数似然函数为

$$
\ln p(\mathbf{T}\mid\mathbf{w}_1,\ldots,\mathbf{w}_K)=\prod_{n=1}^{N}\prod_{k=1}^{K}y_{nk}^{t_{nk}}
\tag{7.122}
$$

其中，每个数据点 $n$ 的目标值 $t_{nk}$ 采用 1-of-$K$ 编码，$\mathbf{T}$ 是元素为 $t_{nk}$ 的矩阵。同样，可以使用拉普拉斯近似优化超参数（Tipping, 2001），其中模型及其 Hessian 矩阵通过 IRLS 求得。与支持向量机采用的两两配对方法相比，这为多类分类提供了理论依据更充分的方法，也能为新数据点给出概率预测。它的主要缺点是 Hessian 矩阵的大小为 $MK\times MK$，其中 $M$ 为有效基函数的数量；因此，与二类 RVM 相比，训练计算量多出一个 $K^3$ 的因子。

相关向量机的主要缺点是，与 SVM 相比，训练时间较长。不过，它无需通过交叉验证运行来设定模型复杂度参数，这在一定程度上抵消了上述缺点。此外，由于它得到的模型更稀疏，测试点上的计算时间通常短得多，而在实践中，这往往是更重要的考虑因素。

<!-- pdf-page: 377 -->

## 习题

**7.1（⋆⋆）www** 假设有一个由输入向量 $\{\mathbf{x}_n\}$ 构成的数据集，相应的目标值为 $t_n\in\{-1,1\}$；再假设使用核为 $k(\mathbf{x},\mathbf{x}')$ 的 Parzen 核密度估计器（见 2.5.1 节），分别对每个类别中的输入向量密度建模。假定两个类别的先验概率相等，写出使误分类率最小的决策规则。进一步证明，如果选择核 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm T}\mathbf{x}'$，那么分类规则就简化为：把新的输入向量分配给均值与它最近的类别。最后证明，如果核的形式为 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')$，分类就依据特征空间 $\boldsymbol{\phi}(\mathbf{x})$ 中最近的均值进行。

**7.2（⋆）** 证明，如果将约束（7.5）右侧的 $1$ 替换为任意常数 $\gamma>0$，最大间隔超平面的解保持不变。

**7.3（⋆⋆）** 证明，无论数据空间的维数是多少，一个仅含两个数据点、每个类别各有一个点的数据集，就足以确定最大间隔超平面的位置。

**7.4（⋆⋆）www** 证明，最大间隔超平面的间隔值 $\rho$ 满足

$$
\frac{1}{\rho^2}=\sum_{n=1}^{N}a_n
\tag{7.123}
$$

其中，$\{a_n\}$ 是在约束（7.11）和（7.12）下最大化（7.10）得到的。

**7.5（⋆⋆）** 证明，上一题中的 $\rho$ 和 $\{a_n\}$ 还满足

$$
\frac{1}{\rho^2}=2\widetilde{L}(\mathbf{a})
\tag{7.124}
$$

其中，$\widetilde{L}(\mathbf{a})$ 由（7.10）定义。类似地，证明

$$
\frac{1}{\rho^2}=\|\mathbf{w}\|^2.
\tag{7.125}
$$

**7.6（⋆）** 考虑目标变量为 $t\in\{-1,1\}$ 的逻辑回归模型。若定义 $p(t=1\mid y)=\sigma(y)$，其中 $y(\mathbf{x})$ 由（7.1）给出，证明在负对数似然中加入二次正则化项后，所得表达式具有（7.47）的形式。

**7.7（⋆）** 考虑用于回归的支持向量机的拉格朗日函数（7.56）。将拉格朗日函数关于 $\mathbf{w}$、$b$、$\xi_n$ 和 $\widehat{\xi}_n$ 的导数设为零，再回代消去相应变量，证明对偶拉格朗日函数由（7.61）给出。

<!-- pdf-page: 378 -->

**7.8（⋆）www** 对于 7.1.4 节讨论的回归支持向量机，证明所有满足 $\xi_n>0$ 的训练数据点都有 $a_n=C$；类似地，所有满足 $\widehat{\xi}_n>0$ 的点都有 $\widehat{a}_n=C$。

**7.9（⋆）** 验证回归 RVM 中权重后验分布的均值和协方差满足（7.82）和（7.83）。

**7.10（⋆⋆）www** 在（7.84）的指数项中运用配方法，完成关于 $\mathbf{w}$ 的高斯积分，推导回归 RVM 的边缘似然函数的结果（7.85）。

**7.11（⋆⋆）** 重做上一题，但这次使用一般结果（2.115）。

**7.12（⋆⋆）www** 证明，直接最大化回归相关向量机的对数边缘似然（7.85），会得到重估方程（7.87）和（7.88），其中 $\gamma_i$ 由（7.89）定义。

**7.13（⋆⋆）** 在 RVM 回归的证据框架中，我们通过最大化（7.85）给出的边缘似然，得到了重估公式（7.87）和（7.88）。加入形如（B.26）的伽马分布（gamma distribution）作为超先验，扩展这一方法；关于 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化相应的后验概率 $p(\boldsymbol{\mathsf{t}},\boldsymbol{\alpha},\beta\mid\mathbf{X})$，求出 $\boldsymbol{\alpha}$ 和 $\beta$ 的相应重估公式。

**7.14（⋆⋆）** 推导用于回归的相关向量机的预测分布的结果（7.90）。证明其预测方差由（7.91）给出。

**7.15（⋆⋆）www** 利用（7.94）和（7.95），证明边缘似然（7.85）可以写成（7.96）的形式，其中 $\lambda(\alpha_n)$ 由（7.97）定义，稀疏度因子和质量因子分别由（7.98）和（7.99）定义。

**7.16（⋆）** 对回归 RVM 的对数边缘似然（7.97）求关于超参数 $\alpha_i$ 的二阶导数，证明（7.101）给出的驻点是边缘似然的极大值点。

**7.17（⋆⋆）** 利用（7.83）和（7.86），以及矩阵恒等式（C.7），证明（7.102）和（7.103）定义的量 $S_n$ 和 $Q_n$ 可以写成（7.106）和（7.107）的形式。

**7.18（⋆）www** 证明，用于分类的相关向量机的对数后验分布（7.109）的梯度向量和 Hessian 矩阵分别由（7.110）和（7.111）给出。

**7.19（⋆⋆）** 验证，最大化用于分类的相关向量机的近似对数边缘似然函数（7.114），会得到用于重估超参数的结果（7.116）。
