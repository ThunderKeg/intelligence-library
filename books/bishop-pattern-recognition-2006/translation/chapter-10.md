# 第 10 章 近似推断

<aside class="chapter-guide"><strong>本章导读</strong><p>本章讨论后验分布难以直接计算时，如何构造可计算的近似。我们将看到，变分推断如何通过优化下界选择近似分布，因子化假设会带来哪些误差，以及这些方法怎样用于高斯混合、回归和模型比较。最后介绍局部变分方法与期望传播。</p></aside>

<!-- pdf-page: 481 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-chapter-opening.png" alt="水面纹理上的第 10 章标题"><p class="figure-translation">Approximate Inference → 近似推断。</p></figure>

应用概率模型时，一项核心任务是在给定观测到的、也称可见的数据变量 $\mathbf{X}$ 后，计算潜变量 $\mathbf{Z}$ 的后验分布 $p(\mathbf{Z}\mid\mathbf{X})$，以及相对于这一分布的期望。模型还可能包含某些确定性参数，暂时不在记号中显式写出；也可能是一个完全贝叶斯模型，所有未知参数都设有先验分布，并被纳入向量 $\mathbf{Z}$ 所表示的潜变量集合。例如，在 EM 算法中，我们需要计算完整数据对数似然在潜变量后验分布下的期望。对于许多有实际意义的模型，计算后验分布，甚至计算这一分布下的期望，都不可行。原因可能是潜在空间的维数过高，无法直接处理；也可能是后验分布的形式过于复杂，使期望无法解析计算。对于连续变量，所需积分可能不存在闭式的

<!-- pdf-page: 482 -->
<!-- join-previous-paragraph -->
解析解，而空间维数和被积函数的复杂性又可能使数值积分无法实行。对于离散变量，边缘化涉及对隐变量的所有可能配置求和。虽然原则上总能这样做，但实践中隐状态的数量往往随问题规模指数增长，使精确计算的代价高得难以承受。

在这些情况下，我们必须采用近似方法。根据依赖随机近似还是确定性近似，大体可以分为两类。第 11 章将介绍的马尔可夫链蒙特卡洛等随机技术，使贝叶斯方法得以在许多领域广泛应用。这些方法通常具有如下性质：如果计算资源无限，就能生成精确结果；近似来自处理器时间有限。在实践中，采样方法的计算开销可能很大，往往只能用于小规模问题。此外，要判断某种采样方法是否正在从所需分布中生成独立样本，也可能很困难。

本章介绍一系列确定性近似方法，其中一些能够较好地扩展到大型应用。这些方法对后验分布作解析近似，例如假设它按某种特定方式因子化，或者具有高斯分布之类的特定参数形式。因此，它们无法生成精确结果，其优缺点与采样方法形成互补。

第 4.4 节讨论了拉普拉斯近似，它在分布的某个众数，即极大值处，作局部高斯近似。这里我们转而讨论一类称为变分推断（variational inference）或变分贝叶斯（variational Bayes）的近似技术。它们使用更全局性的准则，并已得到广泛应用。最后，我们简要介绍另一种称为期望传播（expectation propagation）的变分框架。

## 10.1 变分推断

变分方法起源于 18 世纪 Euler、Lagrange 等人关于变分法（calculus of variations）的工作。通常的微积分研究函数的导数。我们可以把函数看作一种映射：输入一个变量值，输出函数值。函数的导数描述了输入值发生无穷小变化时，输出值如何变化。类似地，我们可以把泛函（functional）定义为这样一种映射：输入一个函数，输出泛函的值。例如，熵 $\mathrm{H}[p]$ 以概率分布 $p(x)$ 为输入，返回

$$
\mathrm{H}[p]=\int p(x)\ln p(x)\,\mathrm{d}x
\tag{10.1}
$$

<!-- pdf-page: 483 -->

作为输出。于是我们可以引入泛函导数（functional derivative）的概念，它表示当输入函数发生无穷小变化时，泛函值如何变化（Feynman et al., 1964）。变分法的规则与通常的微积分规则相对应，附录 D 对此作了讨论。许多问题可以表述为优化问题，其中被优化的量是一个泛函。求解时，考察所有可能的输入函数，找出使泛函最大或最小的那个函数。变分方法的应用范围很广，包括有限元方法（Kapur, 1989）和最大熵（Schwarz, 1988）等领域。

虽然变分方法本身并不意味着近似，但它很适合用来寻找近似解。做法是限制参与优化的函数范围，例如只考虑二次函数，或者只考虑固定基函数的线性组合，并且仅允许线性组合的系数变化。在概率推断应用中，这种限制可以表现为因子化假设（Jordan et al., 1999; Jaakkola, 2001）。

现在更详细地考察如何把变分优化的思想用于推断问题。假设我们有一个完全贝叶斯模型，所有参数都设有先验分布。除了参数，模型还可能包含潜变量；我们用 $\mathbf{Z}$ 表示所有潜变量和参数的集合。类似地，用 $\mathbf{X}$ 表示全部观测变量的集合。例如，可能有 $N$ 个独立同分布数据，此时 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，$\mathbf{Z}=\{\mathbf{z}_1,\ldots,\mathbf{z}_N\}$。概率模型指定了联合分布 $p(\mathbf{X},\mathbf{Z})$，我们的目标是近似后验分布 $p(\mathbf{Z}\mid\mathbf{X})$ 和模型证据 $p(\mathbf{X})$。与讨论 EM 时一样，可以将对数边缘概率分解为

$$
\ln p(\mathbf{X})=\mathcal{L}(q)+\mathrm{KL}(q\Vert p)
\tag{10.2}
$$

其中我们定义

$$
\mathcal{L}(q)=\int q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{X},\mathbf{Z})}{q(\mathbf{Z})}\right\}\,\mathrm{d}\mathbf{Z}
\tag{10.3}
$$

$$
\mathrm{KL}(q\Vert p)=-\int q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{Z}\mid\mathbf{X})}{q(\mathbf{Z})}\right\}\,\mathrm{d}\mathbf{Z}.
\tag{10.4}
$$

与讨论 EM 时相比，唯一区别是参数向量 $\boldsymbol{\theta}$ 不再出现，因为参数现在是随机变量，已被纳入 $\mathbf{Z}$。本章主要关注连续变量，所以在写出这一分解时使用积分而不是求和。不过，如果某些或全部变量是离散的，只需按需要将积分替换为求和，分析过程并不改变。与前面一样，我们可以通过对分布 $q(\mathbf{Z})$ 进行优化来最大化下界 $\mathcal{L}(q)$，这等价于最小化 KL 散度。如果允许任意选择 $q(\mathbf{Z})$，那么下界在 KL 散度为零时达到最大值，也就是当 $q(\mathbf{Z})$ 等于后验分布 $p(\mathbf{Z}\mid\mathbf{X})$ 时。

<!-- pdf-page: 484 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-1.png" alt="原分布、拉普拉斯近似、变分近似及其负对数的比较"><figcaption>图 10.1：对于前面图 4.14 中的例子，展示变分近似。左图给出原始分布（黄色）、拉普拉斯近似（红色）和变分近似（绿色）；右图给出相应曲线的负对数。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
不过，我们假设模型的真实后验分布难以处理。

因此，我们转而考虑受限制的分布族 $q(\mathbf{Z})$，并寻找其中使 KL 散度最小的成员。我们的目标是对这个分布族施加足够的限制，使其只包含可处理的分布，同时又让它足够丰富、灵活，能够很好地近似真实后验分布。必须强调，施加限制纯粹是为了使计算可行；在满足这一要求的前提下，应尽可能使用丰富的近似分布族。尤其要注意，高度灵活的分布不会带来“过拟合”。采用更灵活的近似，只会使我们更接近真实后验分布。

限制近似分布族的一种方法，是使用由一组参数 $\boldsymbol{\omega}$ 控制的参数化分布 $q(\mathbf{Z}\mid\boldsymbol{\omega})$。此时，下界 $\mathcal{L}(q)$ 成为 $\boldsymbol{\omega}$ 的函数，我们可以利用标准的非线性优化技术确定最优参数值。图 10.1 展示了这种方法的一个例子：变分分布为高斯分布，我们对它的均值和方差进行优化。

### 10.1.1 因子化分布

这里考虑另一种限制分布族 $q(\mathbf{Z})$ 的方式。假设将 $\mathbf{Z}$ 的各元素划分为互不相交的组，记为 $\mathbf{Z}_i$，其中 $i=1,\ldots,M$。然后假设 $q$ 分布可以按这些组因子化，即

$$
q(\mathbf{Z})=\prod_{i=1}^{M}q_i(\mathbf{Z}_i).
\tag{10.5}
$$

<!-- pdf-page: 485 -->

需要强调，我们没有对分布作进一步假设。尤其是，我们并不限制各个因子 $q_i(\mathbf{Z}_i)$ 的函数形式。这种因子化的变分推断，对应于物理学中称为平均场理论（mean field theory）的近似框架（Parisi, 1988）。

现在，我们要在所有具有式（10.5）形式的分布 $q(\mathbf{Z})$ 中，寻找使下界 $\mathcal{L}(q)$ 最大的分布。因此，我们希望对全部分布 $q_i(\mathbf{Z}_i)$ 作自由形式的变分优化，通过依次优化每个因子来实现。为此，先把式（10.5）代入式（10.3），再把其中对某个因子 $q_j(\mathbf{Z}_j)$ 的依赖分离出来。为保持记号简洁，将 $q_j(\mathbf{Z}_j)$ 简记为 $q_j$，得到

$$
\begin{aligned}
\mathcal{L}(q)&=\int\prod_i q_i\left\{\ln p(\mathbf{X},\mathbf{Z})-\sum_i\ln q_i\right\}\,\mathrm{d}\mathbf{Z}\\
&=\int q_j\left\{\int\ln p(\mathbf{X},\mathbf{Z})\prod_{i\ne j}q_i\,\mathrm{d}\mathbf{Z}_i\right\}\mathrm{d}\mathbf{Z}_j-\int q_j\ln q_j\,\mathrm{d}\mathbf{Z}_j+\mathrm{const}\\
&=\int q_j\ln\widetilde{p}(\mathbf{X},\mathbf{Z}_j)\,\mathrm{d}\mathbf{Z}_j-\int q_j\ln q_j\,\mathrm{d}\mathbf{Z}_j+\mathrm{const}
\end{aligned}
\tag{10.6}
$$

其中，我们通过以下关系定义一个新分布 $\widetilde{p}(\mathbf{X},\mathbf{Z}_j)$：

$$
\ln\widetilde{p}(\mathbf{X},\mathbf{Z}_j)=\mathbb{E}_{i\ne j}[\ln p(\mathbf{X},\mathbf{Z})]+\mathrm{const}.
\tag{10.7}
$$

这里，记号 $\mathbb{E}_{i\ne j}[\cdots]$ 表示相对于所有满足 $i\ne j$ 的变量 $\mathbf{z}_i$ 上的 $q$ 分布取期望，因此

$$
\mathbb{E}_{i\ne j}[\ln p(\mathbf{X},\mathbf{Z})]=\int\ln p(\mathbf{X},\mathbf{Z})\prod_{i\ne j}q_i\,\mathrm{d}\mathbf{Z}_i.
\tag{10.8}
$$

现在假设我们固定 $\{q_{i\ne j}\}$，对分布 $q_j(\mathbf{Z}_j)$ 的所有可能形式，最大化式（10.6）中的 $\mathcal{L}(q)$。注意到式（10.6）是 $q_j(\mathbf{Z}_j)$ 与 $\widetilde{p}(\mathbf{X},\mathbf{Z}_j)$ 之间 Kullback–Leibler 散度的负值，就很容易完成这一步。因此，最大化式（10.6）等价于最小化 Kullback–Leibler

<aside class="biography"><p><strong>莱昂哈德·欧拉（Leonhard Euler）</strong><br>1707–1783</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-euler-portrait.png" alt="莱昂哈德·欧拉肖像"><p>Euler 是瑞士数学家和物理学家，曾在圣彼得堡和柏林工作，被广泛认为是有史以来最伟大的数学家之一。他无疑是最多产的数学家，著作全集多达75卷。他的众多贡献包括建立现代函数理论，与 Lagrange 一同发展变分法，以及发现公式 $e^{i\pi}=-1$，它把数学中四个最重要的数联系起来。在生命的最后17年里，他几乎完全失明，却在这一时期完成了近一半的研究成果。</p></aside>

<!-- pdf-page: 486 -->
<!-- join-previous-paragraph-across-biography -->
散度，而最小值出现在 $q_j(\mathbf{Z}_j)=\widetilde{p}(\mathbf{X},\mathbf{Z}_j)$ 时。因此，我们得到最优解 $q_j^\star(\mathbf{Z}_j)$ 的一般表达式：

$$
\ln q_j^\star(\mathbf{Z}_j)=\mathbb{E}_{i\ne j}[\ln p(\mathbf{X},\mathbf{Z})]+\mathrm{const}.
\tag{10.9}
$$

值得花一些时间考察这个解的形式，因为它是应用变分方法的基础。它告诉我们，要得到因子 $q_j$ 最优解的对数，只需考虑所有隐变量和可见变量的联合分布的对数，再对其余所有满足 $i\ne j$ 的因子 $\{q_i\}$ 取期望。

式（10.9）中的加性常数由分布 $q_j^\star(\mathbf{Z}_j)$ 的归一化确定。因此，对两边取指数并归一化，就有

$$
q_j^\star(\mathbf{Z}_j)=\frac{\exp\bigl(\mathbb{E}_{i\ne j}[\ln p(\mathbf{X},\mathbf{Z})]\bigr)}{\displaystyle\int\exp\bigl(\mathbb{E}_{i\ne j}[\ln p(\mathbf{X},\mathbf{Z})]\bigr)\,\mathrm{d}\mathbf{Z}_j}.
$$

在实践中，使用式（10.9）的形式，然后在需要时通过观察补回归一化常数，会更方便。后面的例子将说明这一点。

对 $j=1,\ldots,M$，式（10.9）给出一组一致性条件，它们对应于因子化约束下下界的极大值。不过，这些方程并不是显式解，因为最优分布 $q_j^\star(\mathbf{Z}_j)$ 在式（10.9）右侧的表达式，依赖于相对于其他因子 $q_i(\mathbf{Z}_i)$（$i\ne j$）计算的期望。因此，我们先适当初始化所有因子 $q_i(\mathbf{Z}_i)$，然后循环遍历各因子，利用其余因子的当前估计计算式（10.9）的右侧，并依次用得到的新估计替换该因子，以寻找一致的解。收敛是有保证的，因为下界关于每个因子 $q_i(\mathbf{Z}_i)$ 都是凸的（Boyd and Vandenberghe, 2004）。

### 10.1.2 因子化近似的性质

我们的变分推断方法以真实后验分布的因子化近似为基础。现在暂且考虑用因子化分布近似一般分布的问题。首先，讨论如何用因子化高斯分布近似一个高斯分布，这有助于我们理解因子化近似会引入哪些误差。考虑两个相关变量 $\mathbf{z}=(z_1,z_2)$ 上的高斯分布 $p(\mathbf{z})=\mathcal{N}(\mathbf{z}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1})$，其均值和精度的各元素为

$$
\boldsymbol{\mu}=\begin{pmatrix}\mu_1\\\mu_2\end{pmatrix},\qquad
\boldsymbol{\Lambda}=\begin{pmatrix}\Lambda_{11}&\Lambda_{12}\\\Lambda_{21}&\Lambda_{22}\end{pmatrix}
\tag{10.10}
$$

由于精度矩阵对称，有 $\Lambda_{21}=\Lambda_{12}$。现在假设我们希望使用 $q(\mathbf{z})=q_1(z_1)q_2(z_2)$ 形式的因子化高斯分布来近似它。首先应用一般结果（10.9），求出

<!-- pdf-page: 487 -->
<!-- join-previous-paragraph -->
最优因子 $q_1^\star(z_1)$ 的表达式。这里要注意，在右侧只需保留以某种函数形式依赖于 $z_1$ 的项，因为其他项都可以吸收到归一化常数中。因此有

$$
\begin{aligned}
\ln q_1^\star(z_1)&=\mathbb{E}_{z_2}[\ln p(\mathbf{z})]+\mathrm{const}\\
&=\mathbb{E}_{z_2}\left[-\frac{1}{2}(z_1-\mu_1)^2\Lambda_{11}-(z_1-\mu_1)\Lambda_{12}(z_2-\mu_2)\right]+\mathrm{const}\\
&=-\frac{1}{2}z_1^2\Lambda_{11}+z_1\mu_1\Lambda_{11}-z_1\Lambda_{12}\bigl(\mathbb{E}[z_2]-\mu_2\bigr)+\mathrm{const}.
\end{aligned}
\tag{10.11}
$$

接着注意到，右侧是 $z_1$ 的二次函数，因此可以认出 $q^\star(z_1)$ 是高斯分布。必须强调，我们并没有假设 $q(z_i)$ 是高斯分布，而是对所有可能分布 $q(z_i)$ 的 KL 散度作变分优化，推导出了这一结果。还要注意，不必显式考虑式（10.9）中的加性常数，因为它代表归一化常数，在需要时可以在最后通过观察确定。使用配方法，可以确定这个高斯分布的均值和精度，得到<span class="margin-reference">第 2.3.1 节</span>

$$
q^\star(z_1)=\mathcal{N}(z_1\mid m_1,\Lambda_{11}^{-1})
\tag{10.12}
$$

其中

$$
m_1=\mu_1-\Lambda_{11}^{-1}\Lambda_{12}\bigl(\mathbb{E}[z_2]-\mu_2\bigr).
\tag{10.13}
$$

由对称性，$q_2^\star(z_2)$ 也为高斯分布，可写成

$$
q_2^\star(z_2)=\mathcal{N}(z_2\mid m_2,\Lambda_{22}^{-1})
\tag{10.14}
$$

其中

$$
m_2=\mu_2-\Lambda_{22}^{-1}\Lambda_{21}\bigl(\mathbb{E}[z_1]-\mu_1\bigr).
\tag{10.15}
$$

注意，这些解相互耦合，$q^\star(z_1)$ 依赖于相对于 $q^\star(z_2)$ 计算的期望，反过来也一样。通常，我们把这些变分解看作重估方程，依次循环更新各变量，直到满足某个收敛准则。很快会看到这样的例子。不过，这里的问题足够简单，可以得到闭式解。具体来说，由于 $\mathbb{E}[z_1]=m_1$ 且 $\mathbb{E}[z_2]=m_2$，只要取 $\mathbb{E}[z_1]=\mu_1$ 和 $\mathbb{E}[z_2]=\mu_2$，两个方程就都得到满足。很容易证明，只要分布非奇异，这就是唯一解。<span class="margin-reference">习题 10.2</span>图 10.2（a）展示了这一结果。可以看到，均值被正确捕捉，但 $q(\mathbf{z})$ 的方差受 $p(\mathbf{z})$ 方差最小的方向控制，正交方向上的方差被显著低估。因子化变分近似往往会给出过于集中的后验近似，这是一个一般性结论。

作为比较，假设我们最小化的是反向 Kullback–Leibler 散度 $\mathrm{KL}(p\Vert q)$。我们将看到，这种形式的 KL 散度

<!-- pdf-page: 488 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-2.png" alt="最小化两种方向 KL 散度所得因子化高斯近似的比较"><figcaption>图 10.2：比较 Kullback–Leibler 散度的两种形式。绿色等高线对应于两个变量 $z_1$、$z_2$ 上的相关高斯分布 $p(\mathbf{z})$ 的 $1$、$2$、$3$ 个标准差；红色等高线表示同一组变量上的近似分布 $q(\mathbf{z})$ 的对应水平。近似分布由两个独立的一元高斯分布相乘得到，其参数分别通过最小化（a）Kullback–Leibler 散度 $\mathrm{KL}(q\Vert p)$，以及（b）反向 Kullback–Leibler 散度 $\mathrm{KL}(p\Vert q)$ 得到。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
用于另一种称为期望传播的近似推断框架。<span class="margin-reference">第 10.7 节</span>因此，我们考虑这样一个一般问题：当 $q(\mathbf{Z})$ 是式（10.5）形式的因子化近似时，如何最小化 $\mathrm{KL}(p\Vert q)$。此时，KL 散度可以写成

$$
\mathrm{KL}(p\Vert q)=-\int p(\mathbf{Z})\left[\sum_{i=1}^{M}\ln q_i(\mathbf{Z}_i)\right]\mathrm{d}\mathbf{Z}+\mathrm{const}
\tag{10.16}
$$

其中，常数项就是 $p(\mathbf{Z})$ 的熵，因此不依赖于 $q(\mathbf{Z})$。现在可以对每个因子 $q_j(\mathbf{Z}_j)$ 进行优化，利用拉格朗日乘子很容易得到<span class="margin-reference">习题 10.3</span>

$$
q_j^\star(\mathbf{Z}_j)=\int p(\mathbf{Z})\prod_{i\ne j}\mathrm{d}\mathbf{Z}_i=p(\mathbf{Z}_j).
\tag{10.17}
$$

在这种情况下，$q_j(\mathbf{Z}_j)$ 的最优解就是 $p(\mathbf{Z})$ 相应的边缘分布。注意，这是一个闭式解，因此不需要迭代。

要将这个结果用于向量 $\mathbf{z}$ 上的高斯分布 $p(\mathbf{z})$ 这一示例，可以使用式（2.98），得到图 10.2（b）所示的结果。我们看到，近似分布的均值仍然正确，但它在变量空间中真实概率很低的区域放置了相当大的概率质量。

考察以下 Kullback–Leibler 散度中某些区域所产生的很大正贡献，就能理解这两个结果的差别：

$$
\mathrm{KL}(q\Vert p)=-\int q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{Z})}{q(\mathbf{Z})}\right\}\mathrm{d}\mathbf{Z}
\tag{10.18}
$$

<!-- pdf-page: 489 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-3.png" alt="双峰分布的三种单高斯近似，分别覆盖双峰或集中于某一峰"><figcaption>图 10.3：Kullback–Leibler 散度两种形式的另一个比较。（a）蓝色等高线表示由两个高斯分量混合而成的双峰分布 $p(\mathbf{Z})$；红色等高线对应于在最小化 Kullback–Leibler 散度 $\mathrm{KL}(p\Vert q)$ 的意义下，最佳近似 $p(\mathbf{Z})$ 的单个高斯分布 $q(\mathbf{Z})$。（b）与（a）相同，但红色等高线对应的高斯分布 $q(\mathbf{Z})$，通过数值最小化 Kullback–Leibler 散度 $\mathrm{KL}(q\Vert p)$ 得到。（c）与（b）相同，但展示 Kullback–Leibler 散度的另一个局部极小值。</figcaption></figure>

这种贡献来自 $\mathbf{Z}$ 空间中 $p(\mathbf{Z})$ 接近零的区域，除非 $q(\mathbf{Z})$ 也接近零。因此，最小化这种形式的 KL 散度，会使分布 $q(\mathbf{Z})$ 避开 $p(\mathbf{Z})$ 很小的区域。反过来，使 $\mathrm{KL}(p\Vert q)$ 最小的分布 $q(\mathbf{Z})$，会在 $p(\mathbf{Z})$ 非零的区域中保持非零。

如果考虑用单峰分布近似多峰分布，如图 10.3 所示，就能进一步理解两种 KL 散度的不同行为。在实际应用中，真实后验分布往往是多峰的，大部分后验概率质量集中在参数空间中若干相对较小的区域。多个峰可能来自潜在空间中的不可辨识性，也可能来自对参数的复杂非线性依赖。第 9 章讨论高斯混合时，我们遇到过这两类多峰性，它们表现为似然函数的多个极大值。基于最小化 $\mathrm{KL}(q\Vert p)$ 的变分方法，往往会找到这些峰中的某一个。相比之下，如果最小化 $\mathrm{KL}(p\Vert q)$，得到的近似会在所有峰之间取平均；对于混合模型，这会导致较差的预测分布，因为两个好的参数值的平均，通常并不是一个好的参数值。虽然可以利用 $\mathrm{KL}(p\Vert q)$ 定义有用的推断过程，但所需方法与这里讨论的相当不同。我们将在讨论期望传播时详细考察。<span class="margin-reference">第 10.7 节</span>

这两种形式的 Kullback–Leibler 散度都属于

<!-- pdf-page: 490 -->
<!-- join-previous-paragraph -->
如下定义的 alpha 散度族（Ali and Silvey, 1966; Amari, 1985; Minka, 2005）：

$$
\mathrm{D}_\alpha(p\Vert q)=\frac{4}{1-\alpha^2}\left(1-\int p(x)^{(1+\alpha)/2}q(x)^{(1-\alpha)/2}\,\mathrm{d}x\right)
\tag{10.19}
$$

其中 $-\infty<\alpha<\infty$ 是连续参数。Kullback–Leibler 散度 $\mathrm{KL}(p\Vert q)$ 对应于极限 $\alpha\to1$，而 $\mathrm{KL}(q\Vert p)$ 对应于极限 $\alpha\to-1$。对于所有 $\alpha$，都有 $\mathrm{D}_\alpha(p\Vert q)\geqslant0$，且等号成立当且仅当 $p(x)=q(x)$。<span class="margin-reference">习题 10.6</span>假设 $p(x)$ 是固定分布，我们在某个分布集合 $q(x)$ 中最小化 $\mathrm{D}_\alpha(p\Vert q)$。当 $\alpha\leqslant-1$ 时，散度具有迫零（zero forcing）性质：对于满足 $p(x)=0$ 的任意 $x$，都会有 $q(x)=0$。通常，$q(x)$ 会低估 $p(x)$ 的支撑集，并倾向于寻找概率质量最大的那个峰。反过来，当 $\alpha\geqslant1$ 时，散度具有避零（zero-avoiding）性质：凡是 $p(x)>0$ 的 $x$，都会有 $q(x)>0$。通常，$q(x)$ 会扩展以覆盖整个 $p(x)$，并高估它的支撑集。当 $\alpha=0$ 时，得到一种对称散度，它与下面给出的 Hellinger 距离呈线性关系：

$$
\mathrm{D}_{\mathrm{H}}(p\Vert q)=\int\bigl(p(x)^{1/2}-q(x)^{1/2}\bigr)\,\mathrm{d}x.
\tag{10.20}
$$

Hellinger 距离的平方根是一个有效的距离度量。

### 10.1.3 示例：一元高斯分布

现在，我们用单个变量 $x$ 上的高斯分布说明因子化变分近似（MacKay, 2003）。给定观测值数据集 $\mathcal{D}=\{x_1,\ldots,x_N\}$，假设这些 $x$ 值独立地从高斯分布中抽取，我们的目标是推断均值 $\mu$ 和精度 $\tau$ 的后验分布。似然函数为

$$
p(\mathcal{D}\mid\mu,\tau)=\left(\frac{\tau}{2\pi}\right)^{N/2}\exp\left\{-\frac{\tau}{2}\sum_{n=1}^{N}(x_n-\mu)^2\right\}.
\tag{10.21}
$$

现在为 $\mu$ 和 $\tau$ 引入共轭先验分布：

$$
p(\mu\mid\tau)=\mathcal{N}\bigl(\mu\mid\mu_0,(\lambda_0\tau)^{-1}\bigr)
\tag{10.22}
$$

$$
p(\tau)=\operatorname{Gam}(\tau\mid a_0,b_0)
\tag{10.23}
$$

其中 $\operatorname{Gam}(\tau\mid a_0,b_0)$ 是式（2.146）定义的伽马分布。这两个分布共同构成高斯-伽马共轭先验分布。<span class="margin-reference">第 2.3.6 节</span>

对于这个简单问题，可以精确求出后验分布，它仍然是高斯-伽马分布。<span class="margin-reference">习题 2.44</span>不过，为了说明方法，我们考虑如下后验分布的因子化变分近似：

$$
q(\mu,\tau)=q_\mu(\mu)q_\tau(\tau).
\tag{10.24}
$$

<!-- pdf-page: 491 -->

注意，真实后验分布并不能按这种方式因子化。最优因子 $q_\mu(\mu)$ 和 $q_\tau(\tau)$ 可以由一般结果（10.9）得到。对于 $q_\mu(\mu)$，有

$$
\begin{aligned}
\ln q_\mu^\star(\mu)&=\mathbb{E}_\tau[\ln p(\mathcal{D}\mid\mu,\tau)+\ln p(\mu\mid\tau)]+\mathrm{const}\\
&=-\frac{\mathbb{E}[\tau]}{2}\left\{\lambda_0(\mu-\mu_0)^2+\sum_{n=1}^{N}(x_n-\mu)^2\right\}+\mathrm{const}.
\end{aligned}
\tag{10.25}
$$

对 $\mu$ 配方，可见 $q_\mu(\mu)$ 是高斯分布 $\mathcal{N}(\mu\mid\mu_N,\lambda_N^{-1})$，其均值和精度为<span class="margin-reference">习题 10.7</span>

$$
\mu_N=\frac{\lambda_0\mu_0+N\overline{x}}{\lambda_0+N}
\tag{10.26}
$$

$$
\lambda_N=(\lambda_0+N)\mathbb{E}[\tau].
\tag{10.27}
$$

注意，当 $N\to\infty$ 时，这给出最大似然结果，即 $\mu_N=\overline{x}$，而精度为无穷大。

类似地，因子 $q_\tau(\tau)$ 的最优解为

$$
\begin{aligned}
\ln q_\tau^\star(\tau)&=\mathbb{E}_\mu[\ln p(\mathcal{D}\mid\mu,\tau)+\ln p(\mu\mid\tau)]+\ln p(\tau)+\mathrm{const}\\
&=(a_0-1)\ln\tau-b_0\tau+\frac{N}{2}\ln\tau\\
&\quad-\frac{\tau}{2}\mathbb{E}_\mu\left[\sum_{n=1}^{N}(x_n-\mu)^2+\lambda_0(\mu-\mu_0)^2\right]+\mathrm{const}
\end{aligned}
\tag{10.28}
$$

因此，$q_\tau(\tau)$ 是伽马分布 $\operatorname{Gam}(\tau\mid a_N,b_N)$，其参数为

$$
a_N=a_0+\frac{N}{2}
\tag{10.29}
$$

$$
b_N=b_0+\frac{1}{2}\mathbb{E}_\mu\left[\sum_{n=1}^{N}(x_n-\mu)^2+\lambda_0(\mu-\mu_0)^2\right].
\tag{10.30}
$$

当 $N\to\infty$ 时，它同样表现出预期的行为。<span class="margin-reference">习题 10.8</span>

必须强调，我们没有事先假设最优分布 $q_\mu(\mu)$ 和 $q_\tau(\tau)$ 具有这些特定的函数形式。它们自然地来自似然函数及相应共轭先验的结构。<span class="margin-reference">第 10.4.1 节</span>

于是，我们得到了最优分布 $q_\mu(\mu)$ 和 $q_\tau(\tau)$ 的表达式，每个分布都依赖于相对于另一个分布计算的矩。因此，一种求解方式是先为某个矩，例如 $\mathbb{E}[\tau]$，作初始猜测，再用它重新计算分布 $q_\mu(\mu)$。根据更新后的分布，可以求出所需的矩 $\mathbb{E}[\mu]$ 和 $\mathbb{E}[\mu^2]$，再用它们重新计算分布 $q_\tau(\tau)$，如此继续。由于本例的隐变量空间只有两维，我们可以绘制真实后验分布和因子化近似的等高线，来展示后验分布的变分近似，如图 10.4 所示。

<!-- pdf-page: 492 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-4.png" alt="一元高斯均值与精度的真实后验和变分近似的四幅等高线图"><figcaption>图 10.4：对一元高斯分布的均值 $\mu$ 和精度 $\tau$ 进行变分推断的示例。真实后验分布 $p(\mu,\tau\mid\mathcal{D})$ 的等高线用绿色表示。（a）初始因子化近似 $q_\mu(\mu)q_\tau(\tau)$ 的等高线用蓝色表示。（b）重新估计因子 $q_\mu(\mu)$ 之后。（c）重新估计因子 $q_\tau(\tau)$ 之后。（d）迭代方案所收敛到的最优因子化近似，其等高线用红色表示。</figcaption></figure>

通常，为了求出最优因子化后验分布，我们需要使用这样的迭代方法。不过，对于这里非常简单的例子，可以联立最优因子 $q_\mu(\mu)$ 和 $q_\tau(\tau)$ 的方程，得到显式解。在此之前，考虑宽广的非信息性先验，令 $\mu_0=a_0=b_0=\lambda_0=0$，可以简化这些表达式。虽然这样的参数设置对应于非正常先验，但后验分布仍然定义良好。利用伽马分布均值的标准结果 $\mathbb{E}[\tau]=a_N/b_N$，并结合式（10.29）和式（10.30），有<span class="margin-reference">附录 B</span>

$$
\frac{1}{\mathbb{E}[\tau]}=\mathbb{E}\left[\frac{1}{N}\sum_{n=1}^{N}(x_n-\mu)^2\right]=\overline{x^2}-2\overline{x}\mathbb{E}[\mu]+\mathbb{E}[\mu^2].
\tag{10.31}
$$

然后使用式（10.26）和式（10.27），得到

<!-- pdf-page: 493 -->
<!-- join-previous-paragraph -->
$q_\mu(\mu)$ 的一阶矩和二阶矩：

$$
\mathbb{E}[\mu]=\overline{x},\qquad\mathbb{E}[\mu^2]=\overline{x}^{\,2}+\frac{1}{N\mathbb{E}[\tau]}.
\tag{10.32}
$$

现在将这些矩代入式（10.31），再解出 $\mathbb{E}[\tau]$，得到<span class="margin-reference">习题 10.9</span>

$$
\begin{aligned}
\frac{1}{\mathbb{E}[\tau]}&=\frac{1}{N-1}\bigl(\overline{x^2}-\overline{x}^{\,2}\bigr)\\
&=\frac{1}{N-1}\sum_{n=1}^{N}(x_n-\overline{x})^2.
\end{aligned}
\tag{10.33}
$$

我们认出，右侧就是熟悉的一元高斯分布方差的无偏估计量。因此可以看到，使用贝叶斯方法避免了最大似然解的偏差。<span class="margin-reference">第 1.2.4 节</span>

### 10.1.4 模型比较

除了对隐变量 $\mathbf{Z}$ 进行推断，我们也可能希望比较一组候选模型。这些模型由索引 $m$ 标记，具有先验概率 $p(m)$。此时，目标是近似后验概率 $p(m\mid\mathbf{X})$，其中 $\mathbf{X}$ 是观测数据。这比前面考虑的情况稍复杂，因为不同模型的隐变量 $\mathbf{Z}$ 可能具有不同结构，甚至不同维数。因此，不能仅考虑因子化近似 $q(\mathbf{Z})q(m)$，而必须认识到，$\mathbf{Z}$ 的后验需要以 $m$ 为条件，所以应考虑 $q(\mathbf{Z},m)=q(\mathbf{Z}\mid m)q(m)$。很容易验证，基于这个变分分布有如下分解：<span class="margin-reference">习题 10.10</span>

$$
\ln p(\mathbf{X})=\mathcal{L}_m-\sum_m\sum_{\mathbf{Z}}q(\mathbf{Z}\mid m)q(m)\ln\left\{\frac{p(\mathbf{Z},m\mid\mathbf{X})}{q(\mathbf{Z}\mid m)q(m)}\right\}
\tag{10.34}
$$

其中，$\mathcal{L}_m$ 是 $\ln p(\mathbf{X})$ 的下界，给定为

$$
\mathcal{L}_m=\sum_m\sum_{\mathbf{Z}}q(\mathbf{Z}\mid m)q(m)\ln\left\{\frac{p(\mathbf{Z},\mathbf{X},m)}{q(\mathbf{Z}\mid m)q(m)}\right\}.
\tag{10.35}
$$

这里假设 $\mathbf{Z}$ 是离散的，但只要将求和替换为积分，同样的分析就适用于连续潜变量。利用拉格朗日乘子，可以对分布 $q(m)$ 最大化 $\mathcal{L}_m$，结果为<span class="margin-reference">习题 10.11</span>

$$
q(m)\propto p(m)\exp\{\mathcal{L}_m\}.
\tag{10.36}
$$

不过，如果对 $q(\mathbf{Z}\mid m)$ 最大化 $\mathcal{L}_m$，就会发现不同 $m$ 对应的解相互耦合。这在预料之中，因为它们以 $m$ 为条件。我们转而先分别优化每个 $q(\mathbf{Z}\mid m)$，通过优化

<!-- pdf-page: 494 -->
<!-- join-previous-paragraph -->
式（10.35）来完成，再用式（10.36）确定 $q(m)$。归一化之后，所得 $q(m)$ 值就可以按通常的方式用于模型选择或模型平均。

## 10.2 示例：高斯混合的变分推断

现在回到高斯混合模型，应用上一节建立的变分推断方法。这不仅能很好地说明变分方法的应用，还将展示贝叶斯处理如何简洁地解决最大似然方法中的许多困难（Attias, 1999b）。建议读者详细推演这个例子，因为它有助于理解变分方法的实际应用。对这里的分析作直接扩展和推广，就能求解许多对应于更复杂分布的贝叶斯模型。

我们的起点是高斯混合模型的似然函数，其图模型如图 9.6 所示。每个观测 $\mathbf{x}_n$ 都有一个对应潜变量 $\mathbf{z}_n$，它是一个采用 1-of-K 编码的二元向量，各元素为 $z_{nk}$，其中 $k=1,\ldots,K$。与前面一样，用 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 表示观测数据集，用 $\mathbf{Z}=\{\mathbf{z}_1,\ldots,\mathbf{z}_N\}$ 表示潜变量。由式（9.10），给定混合系数 $\boldsymbol{\pi}$ 时，$\mathbf{Z}$ 的条件分布为

$$
p(\mathbf{Z}\mid\boldsymbol{\pi})=\prod_{n=1}^{N}\prod_{k=1}^{K}\pi_k^{z_{nk}}.
\tag{10.37}
$$

类似地，由式（9.11）可以写出给定潜变量与分量参数时，观测数据向量的条件分布：

$$
p(\mathbf{X}\mid\mathbf{Z},\boldsymbol{\mu},\boldsymbol{\Lambda})=\prod_{n=1}^{N}\prod_{k=1}^{K}\mathcal{N}\bigl(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k^{-1}\bigr)^{z_{nk}}
\tag{10.38}
$$

其中 $\boldsymbol{\mu}=\{\boldsymbol{\mu}_k\}$，$\boldsymbol{\Lambda}=\{\boldsymbol{\Lambda}_k\}$。注意，这里使用精度矩阵而不是协方差矩阵，因为这样可以使数学表达稍微简化。

接着，为参数 $\boldsymbol{\mu}$、$\boldsymbol{\Lambda}$ 和 $\boldsymbol{\pi}$ 引入先验。使用共轭先验分布可以大幅简化分析。<span class="margin-reference">第 10.4.1 节</span>因此，我们为混合系数 $\boldsymbol{\pi}$ 选择狄利克雷分布：

$$
p(\boldsymbol{\pi})=\operatorname{Dir}(\boldsymbol{\pi}\mid\boldsymbol{\alpha}_0)=C(\boldsymbol{\alpha}_0)\prod_{k=1}^{K}\pi_k^{\alpha_0-1}
\tag{10.39}
$$

其中，出于对称性，为每个分量选择相同的参数 $\alpha_0$；$C(\boldsymbol{\alpha}_0)$ 是

<!-- pdf-page: 495 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-5.png" alt="贝叶斯高斯混合的有向图，包含混合系数、均值、精度及 N 个观测的板"><figcaption>图 10.5：表示贝叶斯高斯混合模型的有向无环图，其中方框（板）表示一组 $N$ 个独立同分布观测。这里 $\boldsymbol{\mu}$ 表示 $\{\boldsymbol{\mu}_k\}$，$\boldsymbol{\Lambda}$ 表示 $\{\boldsymbol{\Lambda}_k\}$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
式（B.23）定义的狄利克雷分布归一化常数。正如我们已经看到的，参数 $\alpha_0$ 可以解释为先验中与混合分布每个分量关联的有效观测数。<span class="margin-reference">第 2.2.1 节</span>如果 $\alpha_0$ 很小，那么后验分布主要受数据影响，而不是受先验影响。

类似地，为每个高斯分量的均值和精度引入独立的高斯 Wishart 先验，给定为

$$
\begin{aligned}
p(\boldsymbol{\mu},\boldsymbol{\Lambda})&=p(\boldsymbol{\mu}\mid\boldsymbol{\Lambda})p(\boldsymbol{\Lambda})\\
&=\prod_{k=1}^{K}\mathcal{N}\bigl(\boldsymbol{\mu}_k\mid\mathbf{m}_0,(\beta_0\boldsymbol{\Lambda}_k)^{-1}\bigr)\mathcal{W}(\boldsymbol{\Lambda}_k\mid\mathbf{W}_0,\nu_0)
\end{aligned}
\tag{10.40}
$$

因为在均值和精度都未知时，这正是共轭先验分布。通常，出于对称性，我们会选择 $\mathbf{m}_0=\mathbf{0}$。<span class="margin-reference">第 2.3.6 节</span>

所得模型可以表示为图 10.5 所示的有向图。注意，存在从 $\boldsymbol{\Lambda}$ 到 $\boldsymbol{\mu}$ 的链接，因为式（10.40）中 $\boldsymbol{\mu}$ 分布的方差是 $\boldsymbol{\Lambda}$ 的函数。

这个例子很好地说明了潜变量与参数的区别。板内的 $\mathbf{z}_n$ 等变量被视为潜变量，因为它们的数量随数据集大小增长。相比之下，板外的 $\boldsymbol{\mu}$ 等变量数量固定，与数据集大小无关，因此被视为参数。不过，从图模型的角度看，两者实际上并没有根本区别。

### 10.2.1 变分分布

为了对这个模型作变分处理，接下来写出所有随机变量的联合分布：

$$
p(\mathbf{X},\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})=p(\mathbf{X}\mid\mathbf{Z},\boldsymbol{\mu},\boldsymbol{\Lambda})p(\mathbf{Z}\mid\boldsymbol{\pi})p(\boldsymbol{\pi})p(\boldsymbol{\mu}\mid\boldsymbol{\Lambda})p(\boldsymbol{\Lambda})
\tag{10.41}
$$

其中各因子已在上面定义。读者可以花些时间验证，这一分解确实对应于图 10.5 中的概率图模型。注意，只有变量 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 被观测到。

<!-- pdf-page: 496 -->

现在考虑一个在潜变量与参数之间因子化的变分分布，即

$$
q(\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})=q(\mathbf{Z})q(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}).
\tag{10.42}
$$

令人注意的是，要为贝叶斯混合模型得到可计算的实用解，我们只需要作出这一个假设。尤其是，因子 $q(\mathbf{Z})$ 和 $q(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})$ 的函数形式，将通过优化变分分布自动确定。注意，与式（10.41）中对 $p$ 分布的处理一样，我们省略了 $q$ 分布的下标，依靠自变量区分不同分布。

利用一般结果（10.9），很容易推导这些因子相应的顺序更新方程。先考虑因子 $q(\mathbf{Z})$ 的更新方程。优化后因子的对数为

$$
\ln q^\star(\mathbf{Z})=\mathbb{E}_{\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}}[\ln p(\mathbf{X},\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})]+\mathrm{const}.
\tag{10.43}
$$

现在使用分解（10.41）。注意，我们只关心右侧对变量 $\mathbf{Z}$ 的函数依赖。因此，与 $\mathbf{Z}$ 无关的项都可以吸收到加性的归一化常数中，得到

$$
\ln q^\star(\mathbf{Z})=\mathbb{E}_{\boldsymbol{\pi}}[\ln p(\mathbf{Z}\mid\boldsymbol{\pi})]+\mathbb{E}_{\boldsymbol{\mu},\boldsymbol{\Lambda}}[\ln p(\mathbf{X}\mid\mathbf{Z},\boldsymbol{\mu},\boldsymbol{\Lambda})]+\mathrm{const}.
\tag{10.44}
$$

代入右侧的两个条件分布，再把与 $\mathbf{Z}$ 无关的项吸收到加性常数中，有

$$
\ln q^\star(\mathbf{Z})=\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\ln\rho_{nk}+\mathrm{const}
\tag{10.45}
$$

其中定义

$$
\begin{aligned}
\ln\rho_{nk}&=\mathbb{E}[\ln\pi_k]+\frac{1}{2}\mathbb{E}[\ln|\boldsymbol{\Lambda}_k|]-\frac{D}{2}\ln(2\pi)\\
&\quad-\frac{1}{2}\mathbb{E}_{\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k}\bigl[(\mathbf{x}_n-\boldsymbol{\mu}_k)^{\mathrm{T}}\boldsymbol{\Lambda}_k(\mathbf{x}_n-\boldsymbol{\mu}_k)\bigr]
\end{aligned}
\tag{10.46}
$$

这里 $D$ 是数据变量 $\mathbf{x}$ 的维数。对式（10.45）两边取指数，得到

$$
q^\star(\mathbf{Z})\propto\prod_{n=1}^{N}\prod_{k=1}^{K}\rho_{nk}^{z_{nk}}.
\tag{10.47}
$$

要求这个分布归一化，并注意对每个 $n$，各 $z_{nk}$ 都是二元量，且对所有 $k$ 的和为 $1$，可得<span class="margin-reference">习题 10.12</span>

$$
q^\star(\mathbf{Z})=\prod_{n=1}^{N}\prod_{k=1}^{K}r_{nk}^{z_{nk}}
\tag{10.48}
$$

<!-- pdf-page: 497 -->

其中

$$
r_{nk}=\frac{\rho_{nk}}{\displaystyle\sum_{j=1}^{K}\rho_{nj}}.
\tag{10.49}
$$

可以看到，因子 $q(\mathbf{Z})$ 的最优解与先验 $p(\mathbf{Z}\mid\boldsymbol{\pi})$ 具有相同的函数形式。注意，由于 $\rho_{nk}$ 是某个实数的指数，各个 $r_{nk}$ 非负且总和为一，符合要求。对于离散分布 $q^\star(\mathbf{Z})$，有标准结果

$$
\mathbb{E}[z_{nk}]=r_{nk}
\tag{10.50}
$$

由此可见，$r_{nk}$ 起着责任度的作用。注意，$q^\star(\mathbf{Z})$ 的最优解依赖于相对于其他变量分布计算的矩，因此变分更新方程同样相互耦合，必须迭代求解。

这里，定义三个利用责任度计算的观测数据集统计量会很方便：

$$
N_k=\sum_{n=1}^{N}r_{nk}
\tag{10.51}
$$

$$
\overline{\mathbf{x}}_k=\frac{1}{N_k}\sum_{n=1}^{N}r_{nk}\mathbf{x}_n
\tag{10.52}
$$

$$
\mathbf{S}_k=\frac{1}{N_k}\sum_{n=1}^{N}r_{nk}(\mathbf{x}_n-\overline{\mathbf{x}}_k)(\mathbf{x}_n-\overline{\mathbf{x}}_k)^{\mathrm{T}}.
\tag{10.53}
$$

注意，它们与高斯混合模型的最大似然 EM 算法中所计算的量相对应。

现在考虑变分后验分布中的因子 $q(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})$。再次使用一般结果（10.9），有

$$
\begin{aligned}
\ln q^\star(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})&=\ln p(\boldsymbol{\pi})+\sum_{k=1}^{K}\ln p(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)+\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{Z}\mid\boldsymbol{\pi})]\\
&\quad+\sum_{k=1}^{K}\sum_{n=1}^{N}\mathbb{E}[z_{nk}]\ln\mathcal{N}\bigl(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k^{-1}\bigr)+\mathrm{const}.
\end{aligned}
\tag{10.54}
$$

这个表达式的右侧可以分解为两类项之和：一类只涉及 $\boldsymbol{\pi}$，另一类只涉及 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Lambda}$。这意味着变分后验 $q(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})$ 因子化为 $q(\boldsymbol{\pi})q(\boldsymbol{\mu},\boldsymbol{\Lambda})$。此外，涉及 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Lambda}$ 的项，本身也是对 $k$ 的求和，每项只涉及 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Lambda}_k$，因此进一步得到

$$
q(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})=q(\boldsymbol{\pi})\prod_{k=1}^{K}q(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k).
\tag{10.55}
$$

<!-- pdf-page: 498 -->

找出式（10.54）右侧依赖于 $\boldsymbol{\pi}$ 的项，有

$$
\ln q^\star(\boldsymbol{\pi})=(\alpha_0-1)\sum_{k=1}^{K}\ln\pi_k+\sum_{k=1}^{K}\sum_{n=1}^{N}r_{nk}\ln\pi_k+\mathrm{const}
\tag{10.56}
$$

其中使用了式（10.50）。对两边取指数，可以认出 $q^\star(\boldsymbol{\pi})$ 是狄利克雷分布：

$$
q^\star(\boldsymbol{\pi})=\operatorname{Dir}(\boldsymbol{\pi}\mid\boldsymbol{\alpha})
\tag{10.57}
$$

其中 $\boldsymbol{\alpha}$ 的各分量 $\alpha_k$ 为

$$
\alpha_k=\alpha_0+N_k.
\tag{10.58}
$$

最后，变分后验分布 $q^\star(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)$ 不能分解成边缘分布的乘积，但总可以利用乘积规则写成 $q^\star(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)=q^\star(\boldsymbol{\mu}_k\mid\boldsymbol{\Lambda}_k)q^\star(\boldsymbol{\Lambda}_k)$。观察式（10.54），找出涉及 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Lambda}_k$ 的项，就能得到这两个因子。正如预期，结果为高斯 Wishart 分布：<span class="margin-reference">习题 10.13</span>

$$
q^\star(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)=\mathcal{N}\bigl(\boldsymbol{\mu}_k\mid\mathbf{m}_k,(\beta_k\boldsymbol{\Lambda}_k)^{-1}\bigr)\mathcal{W}(\boldsymbol{\Lambda}_k\mid\mathbf{W}_k,\nu_k)
\tag{10.59}
$$

其中定义

$$
\beta_k=\beta_0+N_k
\tag{10.60}
$$

$$
\mathbf{m}_k=\frac{1}{\beta_k}(\beta_0\mathbf{m}_0+N_k\overline{\mathbf{x}}_k)
\tag{10.61}
$$

$$
\mathbf{W}_k^{-1}=\mathbf{W}_0^{-1}+N_k\mathbf{S}_k+\frac{\beta_0N_k}{\beta_0+N_k}(\overline{\mathbf{x}}_k-\mathbf{m}_0)(\overline{\mathbf{x}}_k-\mathbf{m}_0)^{\mathrm{T}}
\tag{10.62}
$$

$$
\nu_k=\nu_0+N_k.
\tag{10.63}
$$

这些更新方程对应于用 EM 算法求高斯混合最大似然解时的 M 步方程。我们看到，为更新模型参数的变分后验分布，所需计算涉及对数据集求和，而这些求和与最大似然处理时出现的相同。

要执行这个变分 M 步，需要表示责任度的期望 $\mathbb{E}[z_{nk}]=r_{nk}$。它们通过归一化式（10.46）给出的 $\rho_{nk}$ 得到。该表达式涉及相对于参数变分分布的期望，这些期望很容易计算，得到<span class="margin-reference">习题 10.14</span>

$$
\begin{aligned}
\mathbb{E}_{\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k}\bigl[(\mathbf{x}_n-\boldsymbol{\mu}_k)^{\mathrm{T}}\boldsymbol{\Lambda}_k(\mathbf{x}_n-\boldsymbol{\mu}_k)\bigr]\\
{}=D\beta_k^{-1}+\nu_k(\mathbf{x}_n-\mathbf{m}_k)^{\mathrm{T}}\mathbf{W}_k(\mathbf{x}_n-\mathbf{m}_k)
\end{aligned}
\tag{10.64}
$$

$$
\ln\widetilde{\Lambda}_k\equiv\mathbb{E}[\ln|\boldsymbol{\Lambda}_k|]=\sum_{i=1}^{D}\psi\left(\frac{\nu_k+1-i}{2}\right)+D\ln2+\ln|\mathbf{W}_k|
\tag{10.65}
$$

$$
\ln\widetilde{\pi}_k\equiv\mathbb{E}[\ln\pi_k]=\psi(\alpha_k)-\psi(\widehat{\alpha})
\tag{10.66}
$$

<!-- pdf-page: 499 -->

这里引入了 $\widetilde{\Lambda}_k$ 和 $\widetilde{\pi}_k$ 的定义，$\psi(\cdot)$ 是式（B.25）定义的 digamma 函数，且 $\widehat{\alpha}=\sum_k\alpha_k$。式（10.65）和式（10.66）来自 Wishart 分布与狄利克雷分布的标准性质。<span class="margin-reference">附录 B</span>

将式（10.64）、（10.65）和（10.66）代入式（10.46），并使用式（10.49），得到责任度的以下结果：

$$
r_{nk}\propto\widetilde{\pi}_k\widetilde{\Lambda}_k^{1/2}\exp\left\{-\frac{D}{2\beta_k}-\frac{\nu_k}{2}(\mathbf{x}_n-\mathbf{m}_k)^{\mathrm{T}}\mathbf{W}_k(\mathbf{x}_n-\mathbf{m}_k)\right\}.
\tag{10.67}
$$

注意，它与最大似然 EM 中责任度的相应结果很相似。根据式（9.13），后者可写成

$$
r_{nk}\propto\pi_k|\boldsymbol{\Lambda}_k|^{1/2}\exp\left\{-\frac{1}{2}(\mathbf{x}_n-\boldsymbol{\mu}_k)^{\mathrm{T}}\boldsymbol{\Lambda}_k(\mathbf{x}_n-\boldsymbol{\mu}_k)\right\}
\tag{10.68}
$$

这里用精度代替了协方差，以突出它与式（10.67）的相似性。

因此，优化变分后验分布需要在两个阶段之间循环，它们类似于最大似然 EM 算法的 E 步和 M 步。在与 E 步对应的变分步骤中，我们使用模型参数的当前分布，计算式（10.64）、（10.65）、（10.66）中的矩，从而得到 $\mathbb{E}[z_{nk}]=r_{nk}$。接着，在与 M 步对应的变分步骤中，保持这些责任度不变，利用式（10.57）和式（10.59）重新计算参数的变分分布。每种情况下，变分后验分布都与联合分布（10.41）中的相应因子具有相同的函数形式。这是选择共轭分布带来的一般性结果。<span class="margin-reference">第 10.4.1 节</span>

图 10.6 展示了把这一方法应用于重新缩放后的 Old Faithful 数据集的结果，所用高斯混合模型包含 $K=6$ 个分量。可以看到，收敛之后，只有两个分量的混合系数期望值，在数值上与各自的先验值有可辨别的差异。对此可以作定性解释：贝叶斯模型会自动在拟合数据和模型复杂度之间进行权衡，复杂度惩罚来自参数被推离先验值的那些分量。<span class="margin-reference">第 3.4 节</span>对于几乎不承担解释数据点责任的分量，有 $r_{nk}\simeq0$，因而 $N_k\simeq0$。从式（10.58）可见 $\alpha_k\simeq\alpha_0$，从式（10.60）—（10.63）可见其他参数也回到各自的先验值。原则上，这些分量仍会对数据点作少量拟合，但对于宽广的先验，这种影响很小，无法在数值上看出来。对于变分高斯混合模型，后验分布中混合系数的期望为<span class="margin-reference">习题 10.15</span>

$$
\mathbb{E}[\pi_k]=\frac{\alpha_k+N_k}{K\alpha_0+N}.
\tag{10.69}
$$

考虑某个满足 $N_k\simeq0$、$\alpha_k\simeq\alpha_0$ 的分量。如果先验很宽广，使得 $\alpha_0\to0$，那么 $\mathbb{E}[\pi_k]\to0$，这个分量在模型中不起作用；而如果

<!-- pdf-page: 500 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-6.png" alt="六分量变分贝叶斯高斯混合在零、十五、六十和一百二十次迭代后的结果"><figcaption>图 10.6：将含 $K=6$ 个高斯分量的变分贝叶斯混合模型应用于 Old Faithful 数据集。椭圆表示各分量一个标准差处的密度等高线，每个椭圆内部红色墨色的浓度对应于该分量混合系数的均值。每幅图左上角的数字表示变分推断的迭代次数。若某分量的混合系数期望在数值上与零无法区分，则不将其画出。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
先验对混合系数施加强约束，使得 $\alpha_0\to\infty$，那么 $\mathbb{E}[\pi_k]\to1/K$。

图 10.6 中，混合系数的先验是式（10.39）形式的狄利克雷分布。回顾图 2.5，当 $\alpha_0<1$ 时，先验偏好某些混合系数为零的解。图 10.6 使用 $\alpha_0=10^{-3}$ 得到，结果有两个分量具有非零混合系数。如果改用 $\alpha_0=1$，则得到三个混合系数非零的分量；当 $\alpha=10$ 时，全部六个分量的混合系数都非零。

我们已经看到，贝叶斯高斯混合的变分解与最大似然 EM 算法非常相似。事实上，在极限 $N\to\infty$ 下，贝叶斯处理收敛于最大似然 EM 算法。除非数据集非常小，高斯混合变分算法的主要计算代价都来自责任度的计算，以及加权数据协方差矩阵的计算和求逆。这些运算与最大似然 EM 算法中的运算完全对应，因此与传统最大似然方法相比，使用这种贝叶斯方法几乎没有额外计算开销。不过，它有一些显著优点。首先，最大似然中某个高斯分量“塌缩”到特定数据点所产生的奇异性，在贝叶斯处理中不会出现。

<!-- pdf-page: 501 -->
<!-- join-previous-paragraph -->
事实上，只需引入先验，再用 MAP 估计代替最大似然，就能消除这些奇异性。此外，即使为混合分布选择较大的分量数 $K$，也不会过拟合，图 10.6 已经展示了这一点。最后，变分处理使我们有可能确定混合模型的最优分量数，而不必求助于交叉验证之类的技术。<span class="margin-reference">第 10.2.4 节</span>

### 10.2.2 变分下界

对于这个模型，也可以直接计算下界（10.3）。在实践中，在重估过程中监测下界以判断收敛很有用。它还可以检验解的数学表达式和软件实现，因为在迭代重估过程的每一步中，下界值都不应下降。还可以进一步使用有限差分，检查每次更新是否确实给出了下界在约束条件下的极大值，从而更深入地检验更新方程的数学推导及其软件实现是否正确（Svensén and Bishop, 2004）。

对于变分高斯混合，下界（10.3）为

$$
\begin{aligned}
\mathcal{L}&=\sum_{\mathbf{Z}}\iiint q(\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})\ln\left\{\frac{p(\mathbf{X},\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})}{q(\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})}\right\}\mathrm{d}\boldsymbol{\pi}\,\mathrm{d}\boldsymbol{\mu}\,\mathrm{d}\boldsymbol{\Lambda}\\
&=\mathbb{E}[\ln p(\mathbf{X},\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})]-\mathbb{E}[\ln q(\mathbf{Z},\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda})]\\
&=\mathbb{E}[\ln p(\mathbf{X}\mid\mathbf{Z},\boldsymbol{\mu},\boldsymbol{\Lambda})]+\mathbb{E}[\ln p(\mathbf{Z}\mid\boldsymbol{\pi})]+\mathbb{E}[\ln p(\boldsymbol{\pi})]+\mathbb{E}[\ln p(\boldsymbol{\mu},\boldsymbol{\Lambda})]\\
&\quad-\mathbb{E}[\ln q(\mathbf{Z})]-\mathbb{E}[\ln q(\boldsymbol{\pi})]-\mathbb{E}[\ln q(\boldsymbol{\mu},\boldsymbol{\Lambda})]
\end{aligned}
\tag{10.70}
$$

为使记号简洁，这里省略了 $q$ 分布上的 $\star$ 上标，以及期望算子的下标，因为每个期望都是对其自变量中的所有随机变量计算的。下界中的各项很容易求得，结果如下：<span class="margin-reference">习题 10.16</span>

$$
\begin{aligned}
\mathbb{E}[\ln p(\mathbf{X}\mid\mathbf{Z},\boldsymbol{\mu},\boldsymbol{\Lambda})]&=\frac{1}{2}\sum_{k=1}^{K}N_k\Bigl\{\ln\widetilde{\Lambda}_k-D\beta_k^{-1}-\nu_k\operatorname{Tr}(\mathbf{S}_k\mathbf{W}_k)\\
&\qquad-\nu_k(\overline{\mathbf{x}}_k-\mathbf{m}_k)^{\mathrm{T}}\mathbf{W}_k(\overline{\mathbf{x}}_k-\mathbf{m}_k)-D\ln(2\pi)\Bigr\}
\end{aligned}
\tag{10.71}
$$

$$
\mathbb{E}[\ln p(\mathbf{Z}\mid\boldsymbol{\pi})]=\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\ln\widetilde{\pi}_k
\tag{10.72}
$$

$$
\mathbb{E}[\ln p(\boldsymbol{\pi})]=\ln C(\boldsymbol{\alpha}_0)+(\alpha_0-1)\sum_{k=1}^{K}\ln\widetilde{\pi}_k
\tag{10.73}
$$

<!-- pdf-page: 502 -->

$$
\begin{aligned}
\mathbb{E}[\ln p(\boldsymbol{\mu},\boldsymbol{\Lambda})]&=\frac{1}{2}\sum_{k=1}^{K}\Bigl\{D\ln(\beta_0/2\pi)+\ln\widetilde{\Lambda}_k-\frac{D\beta_0}{\beta_k}\\
&\qquad-\beta_0\nu_k(\mathbf{m}_k-\mathbf{m}_0)^{\mathrm{T}}\mathbf{W}_k(\mathbf{m}_k-\mathbf{m}_0)\Bigr\}+K\ln B(\mathbf{W}_0,\nu_0)\\
&\quad+\frac{\nu_0-D-1}{2}\sum_{k=1}^{K}\ln\widetilde{\Lambda}_k-\frac{1}{2}\sum_{k=1}^{K}\nu_k\operatorname{Tr}(\mathbf{W}_0^{-1}\mathbf{W}_k)
\end{aligned}
\tag{10.74}
$$

$$
\mathbb{E}[\ln q(\mathbf{Z})]=\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\ln r_{nk}
\tag{10.75}
$$

$$
\mathbb{E}[\ln q(\boldsymbol{\pi})]=\sum_{k=1}^{K}(\alpha_k-1)\ln\widetilde{\pi}_k+\ln C(\boldsymbol{\alpha})
\tag{10.76}
$$

$$
\mathbb{E}[\ln q(\boldsymbol{\mu},\boldsymbol{\Lambda})]=\sum_{k=1}^{K}\left\{\frac{1}{2}\ln\widetilde{\Lambda}_k+\frac{D}{2}\ln\left(\frac{\beta_k}{2\pi}\right)-\frac{D}{2}-\mathrm{H}[q(\boldsymbol{\Lambda}_k)]\right\}
\tag{10.77}
$$

其中，$D$ 是 $\mathbf{x}$ 的维数，$\mathrm{H}[q(\boldsymbol{\Lambda}_k)]$ 是式（B.82）给出的 Wishart 分布的熵，系数 $C(\boldsymbol{\alpha})$ 和 $B(\mathbf{W},\nu)$ 分别由式（B.23）和式（B.79）定义。注意，各个 $q$ 分布的对数期望，就是这些分布的负熵。把上述表达式相加得到下界时，可以对某些项进行化简和合并。不过，为便于理解，这里将它们分别保留。

最后，下界还提供了另一种推导第 10.2.1 节变分重估方程的方法。为此，我们利用模型具有共轭先验这一事实，因此变分后验各因子的函数形式已经知道：$\mathbf{Z}$ 为离散分布，$\boldsymbol{\pi}$ 为狄利克雷分布，而 $(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)$ 为高斯 Wishart 分布。为这些分布采用一般的参数形式，就能把下界写成各分布参数的函数。对这些参数最大化下界，即可得到所需的重估方程。<span class="margin-reference">习题 10.18</span>

### 10.2.3 预测密度

应用贝叶斯高斯混合模型时，我们常常关心观测变量的新值 $\widehat{\mathbf{x}}$ 的预测密度。与这个观测相伴的，还有对应潜变量 $\widehat{\mathbf{z}}$。预测密度为

$$
p(\widehat{\mathbf{x}}\mid\mathbf{X})=\sum_{\widehat{\mathbf{z}}}\iiint p(\widehat{\mathbf{x}}\mid\widehat{\mathbf{z}},\boldsymbol{\mu},\boldsymbol{\Lambda})p(\widehat{\mathbf{z}}\mid\boldsymbol{\pi})p(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\mathbf{X})\,\mathrm{d}\boldsymbol{\pi}\,\mathrm{d}\boldsymbol{\mu}\,\mathrm{d}\boldsymbol{\Lambda}
\tag{10.78}
$$

<!-- pdf-page: 503 -->

其中 $p(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\mathbf{X})$ 是参数的真实后验分布，它是未知的。利用式（10.37）和式（10.38），可以先对 $\widehat{\mathbf{z}}$ 求和，得到

$$
p(\widehat{\mathbf{x}}\mid\mathbf{X})=\sum_{k=1}^{K}\iiint\pi_k\mathcal{N}\bigl(\widehat{\mathbf{x}}\mid\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k^{-1}\bigr)p(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\mathbf{X})\,\mathrm{d}\boldsymbol{\pi}\,\mathrm{d}\boldsymbol{\mu}\,\mathrm{d}\boldsymbol{\Lambda}.
\tag{10.79}
$$

由于剩余积分无法直接处理，我们用变分近似 $q(\boldsymbol{\pi})q(\boldsymbol{\mu},\boldsymbol{\Lambda})$ 替换真实后验分布 $p(\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\mathbf{X})$，从而近似预测密度：

$$
p(\widehat{\mathbf{x}}\mid\mathbf{X})=\sum_{k=1}^{K}\iiint\pi_k\mathcal{N}\bigl(\widehat{\mathbf{x}}\mid\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k^{-1}\bigr)q(\boldsymbol{\pi})q(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)\,\mathrm{d}\boldsymbol{\pi}\,\mathrm{d}\boldsymbol{\mu}_k\,\mathrm{d}\boldsymbol{\Lambda}_k
\tag{10.80}
$$

这里使用了因子化（10.55），并且在每一项中，已隐式积掉所有满足 $j\ne k$ 的变量 $\{\boldsymbol{\mu}_j,\boldsymbol{\Lambda}_j\}$。剩余积分现在可以解析计算，得到 Student t 分布的混合：<span class="margin-reference">习题 10.19</span>

$$
p(\widehat{\mathbf{x}}\mid\mathbf{X})=\frac{1}{\widehat{\alpha}}\sum_{k=1}^{K}\alpha_k\operatorname{St}(\widehat{\mathbf{x}}\mid\mathbf{m}_k,\mathbf{L}_k,\nu_k+1-D)
\tag{10.81}
$$

其中第 $k$ 个分量的均值为 $\mathbf{m}_k$，精度为

$$
\mathbf{L}_k=\frac{(\nu_k+1-D)\beta_k}{1+\beta_k}\mathbf{W}_k
\tag{10.82}
$$

这里 $\nu_k$ 由式（10.63）给出。当数据集大小 $N$ 很大时，预测分布（10.81）退化为高斯混合。<span class="margin-reference">习题 10.20</span>

### 10.2.4 确定分量数

我们已经看到，变分下界可以用来确定混合模型中分量数 $K$ 的后验分布。<span class="margin-reference">第 10.1.4 节</span>不过，有一个细节需要处理。对于高斯混合模型中任意给定的参数设置，除了某些特定退化情形，总会存在其他参数设置，使观测变量上的密度完全相同。这些参数值的差别仅在于分量标签的重新排列。例如，考虑单个观测变量 $x$ 上的两个高斯分量混合，参数值为 $\pi_1=a$、$\pi_2=b$、$\mu_1=c$、$\mu_2=d$、$\sigma_1=e$、$\sigma_2=f$。那么，交换两个分量后得到的参数值 $\pi_1=b$、$\pi_2=a$、$\mu_1=d$、$\mu_2=c$、$\sigma_1=f$、$\sigma_2=e$，由于对称性，会给出同样的 $p(x)$ 值。如果混合模型包含 $K$ 个分量，那么每种参数设置都属于一个含有 $K!$ 个等价设置的集合。<span class="margin-reference">习题 10.21</span>

在最大似然的背景下，这种冗余没有影响，因为参数优化算法，例如 EM，会根据参数的初始化找到某个具体解，其他等价解不起作用。然而，在贝叶斯处理中，我们要对所有可能的

<!-- pdf-page: 504 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-7.png" alt="Old Faithful 数据上不同高斯混合分量数的变分下界，K 等于二时最高"><figcaption>图 10.7：对于 Old Faithful 数据，绘制变分下界 $\mathcal{L}$ 随高斯混合模型分量数 $K$ 的变化，在 $K=2$ 处出现明显峰值。对每个 $K$ 值，模型从 $100$ 个不同的随机初始状态开始训练；结果用“+”符号表示，并在水平方向加入小幅随机扰动，以便区分各点。注意，一些解落在次优的局部极大值处，但这种情况不常见。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
参数值进行边缘化。图 10.2 已经展示，如果真实后验分布是多峰的，基于最小化 $\mathrm{KL}(q\Vert p)$ 的变分推断往往只近似其中一个峰附近的分布，而忽略其余峰。同样，因为等价峰具有等价的预测密度，只要我们考虑的是分量数固定为 $K$ 的模型，这就没有影响。但是，如果要比较不同 $K$ 值，就必须考虑这种多峰性。一种简单的近似处理是：在用下界作模型比较和模型平均时，加上 $\ln K!$ 这一项。<span class="margin-reference">习题 10.22</span>

图 10.7 展示了 Old Faithful 数据集上包含多峰性修正因子的下界，随分量数 $K$ 的变化。需要再次强调，最大似然会使似然函数的值随 $K$ 单调增加，这里假设已经避免奇异解，并且不考虑局部极大值的影响，因此不能用它确定合适的模型复杂度。相比之下，贝叶斯推断会自动权衡模型复杂度和数据拟合。<span class="margin-reference">第 3.4 节</span>

这种确定 $K$ 的方法，需要训练并比较一系列不同 $K$ 值的模型。另一种寻找合适 $K$ 值的方法，是把混合系数 $\boldsymbol{\pi}$ 当作参数，对 $\boldsymbol{\pi}$ 最大化下界以求出它们的点估计（Corduneanu and Bishop, 2001），而不采用完全贝叶斯方法中为这些系数保留概率分布的做法。由此得到重估方程<span class="margin-reference">习题 10.23</span>

$$
\pi_k=\frac{1}{N}\sum_{n=1}^{N}r_{nk}
\tag{10.83}
$$

这一最大化步骤，与对其余参数的 $q$ 分布进行变分更新交替执行。那些贡献不足以

<!-- pdf-page: 505 -->

<!-- join-previous-paragraph -->
解释数据的分量，其混合系数会在优化过程中趋于零，因此会通过自动相关性确定从模型中有效地移除。这样，我们只需进行一次训练：从较大的初始 $K$ 值开始，让多余的分量在训练中被剪除。对超参数进行优化时，稀疏性从何而来，我们已在相关向量机的讨论中作过详细说明。<span class="margin-reference">第 7.2.2 节</span>

### 10.2.5 诱导的因子化

推导高斯混合模型的这些变分更新方程时，我们假定变分后验分布具有式（10.42）给出的特定因子化形式。不过，各因子的最优解还表现出额外的因子化。具体来说，$q^\star(\boldsymbol{\mu},\boldsymbol{\Lambda})$ 的解是各混合分量 $k$ 上独立分布 $q^\star(\boldsymbol{\mu}_k,\boldsymbol{\Lambda}_k)$ 的乘积；而式（10.48）给出的潜变量变分后验分布 $q^\star(\mathbf{Z})$，则分解为每个观测 $n$ 对应的独立分布 $q^\star(\mathbf{z}_n)$（注意，它不能再对 $k$ 作进一步因子化，因为对于每个 $n$，$z_{nk}$ 对 $k$ 求和必须等于一）。这些额外的因子化，是假定的因子化形式与真实分布的条件独立性质共同作用的结果；后者由图 10.5 的有向图刻画。

我们将这些额外的因子化称为“诱导的因子化”，因为它们来自变分后验分布中假定的因子化形式与真实联合分布的条件独立性质之间的相互作用。在变分方法的数值实现中，必须考虑这些额外的因子化。例如，如果一组变量的高斯分布，其最优形式总具有对角精度矩阵（对应于该高斯分布对各个变量的因子化），却仍为它保留完整的精度矩阵，就会非常低效。

利用下面这种基于 d 分离的简单图检验，可以很容易地发现这些诱导的因子化。把潜变量划分为三个互不相交的组 $\mathbf{A}$、$\mathbf{B}$、$\mathbf{C}$，并假设我们在 $\mathbf{C}$ 与其余潜变量之间采用因子化形式，即

$$
q(\mathbf{A},\mathbf{B},\mathbf{C})=q(\mathbf{A},\mathbf{B})q(\mathbf{C}).
\tag{10.84}
$$

结合一般结果（10.9）与概率的乘积法则，可知 $q(\mathbf{A},\mathbf{B})$ 的最优解为

$$
\begin{aligned}
\ln q^\star(\mathbf{A},\mathbf{B})&=\mathbb{E}_{\mathbf{C}}[\ln p(\mathbf{X},\mathbf{A},\mathbf{B},\mathbf{C})]+\mathrm{const}\\
&=\mathbb{E}_{\mathbf{C}}[\ln p(\mathbf{A},\mathbf{B}\mid\mathbf{X},\mathbf{C})]+\mathrm{const}.
\end{aligned}
\tag{10.85}
$$

现在考察所得解是否会在 $\mathbf{A}$ 与 $\mathbf{B}$ 之间因子化，也就是是否有 $q^\star(\mathbf{A},\mathbf{B})=q^\star(\mathbf{A})q^\star(\mathbf{B})$。当且仅当 $\ln p(\mathbf{A},\mathbf{B}\mid\mathbf{X},\mathbf{C})=\ln p(\mathbf{A}\mid\mathbf{X},\mathbf{C})+\ln p(\mathbf{B}\mid\mathbf{X},\mathbf{C})$ 时，才会出现这种情况，也就是说，条件独立关系

$$
\mathbf{A}\perp\!\!\!\perp\mathbf{B}\mid\mathbf{X},\mathbf{C}
\tag{10.86}
$$

<!-- pdf-page: 506 -->

成立。对于任意选定的 $\mathbf{A}$ 和 $\mathbf{B}$，都可以用 d 分离判据来检验这一关系是否成立。

为说明这一点，再次考虑图 10.5 的有向图所表示的贝叶斯高斯混合模型，其中假设的变分因子化形式由式（10.42）给出。我们可以立即看出，参数的变分后验分布必然会在 $\boldsymbol{\pi}$ 与其余参数 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Lambda}$ 之间因子化，因为连接 $\boldsymbol{\pi}$ 与 $\boldsymbol{\mu}$ 或 $\boldsymbol{\Lambda}$ 的所有路径，都必须经过某个节点 $\mathbf{z}_n$；这些节点都在条件独立检验的条件集合中，而且在这些路径上都是头尾相接的。

## 10.3 变分线性回归

作为变分推断的第二个例子，我们回到第 3.3 节的贝叶斯线性回归模型。在证据框架中，我们通过最大化对数边缘似然得到点估计，以此近似对 $\alpha$ 和 $\beta$ 的积分。完全贝叶斯方法则要同时对超参数和参数进行积分。虽然精确积分无法直接处理，但可以利用变分方法找到易于处理的近似。为简化讨论，我们假定噪声精度参数 $\beta$ 已知，并固定为其真实值；不过，很容易将这一框架扩展为包含 $\beta$ 的分布。<span class="margin-reference">习题 10.26</span>对于线性回归模型，变分处理最终会与证据框架等价。尽管如此，它仍是运用变分方法的一个很好的练习，也将为第 10.6 节贝叶斯逻辑回归的变分处理奠定基础。

回顾 $\mathbf{w}$ 的似然函数及其先验分布：

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})=\prod_{n=1}^{N}\mathcal{N}(t_n\mid\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}_n,\beta^{-1})
\tag{10.87}
$$

$$
p(\mathbf{w}\mid\alpha)=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I})
\tag{10.88}
$$

其中 $\boldsymbol{\phi}_n=\boldsymbol{\phi}(\mathbf{x}_n)$。现在为 $\alpha$ 引入先验分布。根据第 2.3.6 节的讨论，我们知道高斯分布精度的共轭先验是伽马分布，因此选择

$$
p(\alpha)=\operatorname{Gam}(\alpha\mid a_0,b_0)
\tag{10.89}
$$

其中 $\operatorname{Gam}(\cdot\mid\cdot,\cdot)$ 由式（B.26）定义。于是，所有变量的联合分布为

$$
p(\boldsymbol{\mathsf{t}},\mathbf{w},\alpha)=p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\alpha)p(\alpha).
\tag{10.90}
$$

它可以表示为图 10.8 所示的有向图模型。

### 10.3.1 变分分布

我们首先要找到后验分布 $p(\mathbf{w},\alpha\mid\boldsymbol{\mathsf{t}})$ 的近似。为此，采用第 10.1 节的变分框架，并令变分

<!-- pdf-page: 507 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-8.png" alt="贝叶斯线性回归的有向图，超参数 alpha 指向权重 w，w、基函数向量和 beta 指向观测目标 t_n"><figcaption>图 10.8：表示贝叶斯线性回归模型联合分布（10.90）的概率图模型。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
后验分布具有如下因子化形式：

$$
q(\mathbf{w},\alpha)=q(\mathbf{w})q(\alpha).
\tag{10.91}
$$

可以利用一般结果（10.9），求出该分布各因子的重估方程。回顾一下：对于每个因子，我们先取所有变量联合分布的对数，再对不在该因子中的变量求平均。首先考虑 $\alpha$ 的分布。只保留在函数形式上依赖于 $\alpha$ 的项，有

$$
\begin{aligned}
\ln q^\star(\alpha)&=\ln p(\alpha)+\mathbb{E}_{\mathbf{w}}[\ln p(\mathbf{w}\mid\alpha)]+\mathrm{const}\\
&=(a_0-1)\ln\alpha-b_0\alpha+\frac{M}{2}\ln\alpha-\frac{\alpha}{2}\mathbb{E}[\mathbf{w}^{\mathrm{T}}\mathbf{w}]+\mathrm{const}.
\end{aligned}
\tag{10.92}
$$

可以认出，这是伽马分布的对数，因此确定 $\alpha$ 与 $\ln\alpha$ 的系数便得到

$$
q^\star(\alpha)=\operatorname{Gam}(\alpha\mid a_N,b_N)
\tag{10.93}
$$

其中

$$
a_N=a_0+\frac{M}{2}
\tag{10.94}
$$

$$
b_N=b_0+\frac{1}{2}\mathbb{E}[\mathbf{w}^{\mathrm{T}}\mathbf{w}].
\tag{10.95}
$$

同样，可以求出 $\mathbf{w}$ 的后验分布的变分重估方程。再次利用一般结果（10.9），只保留在函数形式上依赖于 $\mathbf{w}$ 的项，有

$$
\ln q^\star(\mathbf{w})=\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})+\mathbb{E}_{\alpha}[\ln p(\mathbf{w}\mid\alpha)]+\mathrm{const}
\tag{10.96}
$$

$$
{}=-\frac{\beta}{2}\sum_{n=1}^{N}\{\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}_n-t_n\}^2-\frac{1}{2}\mathbb{E}[\alpha]\mathbf{w}^{\mathrm{T}}\mathbf{w}+\mathrm{const}
\tag{10.97}
$$

$$
{}=-\frac{1}{2}\mathbf{w}^{\mathrm{T}}\bigl(\mathbb{E}[\alpha]\mathbf{I}+\beta\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\Phi}\bigr)\mathbf{w}+\beta\mathbf{w}^{\mathrm{T}}\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\mathsf{t}}+\mathrm{const}.
\tag{10.98}
$$

这是一个二次型，因此分布 $q^\star(\mathbf{w})$ 为高斯分布。于是，可以照常通过配方确定均值和协方差，得到

$$
q^\star(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\mathbf{S}_N)
\tag{10.99}
$$

<!-- pdf-page: 508 -->

其中

$$
\mathbf{m}_N=\beta\mathbf{S}_N\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\mathsf{t}}
\tag{10.100}
$$

$$
\mathbf{S}_N=\bigl(\mathbb{E}[\alpha]\mathbf{I}+\beta\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\Phi}\bigr)^{-1}.
\tag{10.101}
$$

注意，这与将 $\alpha$ 当作固定参数时得到的后验分布（3.52）非常相似。区别在于，这里的 $\alpha$ 被它在变分分布下的期望 $\mathbb{E}[\alpha]$ 所替代。因此，我们有意在这两种情况下，对协方差矩阵 $\mathbf{S}_N$ 使用相同的符号。

利用标准结果（B.27）、（B.38）和（B.39），可以得到所需的矩：

$$
\mathbb{E}[\alpha]=a_N/b_N
\tag{10.102}
$$

$$
\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm{T}}]=\mathbf{m}_N\mathbf{m}_N^{\mathrm{T}}+\mathbf{S}_N.
\tag{10.103}
$$

计算变分后验分布时，先初始化 $q(\mathbf{w})$ 或 $q(\alpha)$ 中某个分布的参数，再依次交替重估这两个因子，直到满足适当的收敛判据为止（通常用下文即将讨论的下界来规定这一判据）。

将变分解与第 3.5 节用证据框架得到的解联系起来，能帮助我们理解这两种方法。为此，考虑 $a_0=b_0=0$ 的情形，它对应于 $\alpha$ 的先验无限宽的极限。此时，变分后验分布 $q(\alpha)$ 的均值为

$$
\mathbb{E}[\alpha]=\frac{a_N}{b_N}=\frac{M/2}{\mathbb{E}[\mathbf{w}^{\mathrm{T}}\mathbf{w}]/2}=\frac{M}{\mathbf{m}_N^{\mathrm{T}}\mathbf{m}_N+\operatorname{Tr}(\mathbf{S}_N)}.
\tag{10.104}
$$

与式（9.63）比较可知，对于这个特别简单的模型，变分方法得到的表达式与利用 EM 最大化证据函数得到的表达式完全相同，只是用 $\alpha$ 的期望代替了它的点估计。由于分布 $q(\mathbf{w})$ 只通过期望 $\mathbb{E}[\alpha]$ 依赖于 $q(\alpha)$，因此，当先验无限宽时，这两种方法会给出相同的结果。

### 10.3.2 预测分布

给定新输入 $\mathbf{x}$，利用参数的高斯变分后验，可以很容易地计算这个模型关于 $t$ 的预测分布：

$$
\begin{aligned}
p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}})&=\int p(t\mid\mathbf{x},\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})\,\mathrm{d}\mathbf{w}\\
&\simeq\int p(t\mid\mathbf{x},\mathbf{w})q(\mathbf{w})\,\mathrm{d}\mathbf{w}\\
&=\int\mathcal{N}(t\mid\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}),\beta^{-1})\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\mathbf{S}_N)\,\mathrm{d}\mathbf{w}\\
&=\mathcal{N}(t\mid\mathbf{m}_N^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}),\sigma^2(\mathbf{x}))
\end{aligned}
\tag{10.105}
$$

<!-- pdf-page: 509 -->

这里利用线性高斯模型的结果（2.115）计算了积分。其中，依赖于输入的方差为

$$
\sigma^2(\mathbf{x})=\frac{1}{\beta}+\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}).
\tag{10.106}
$$

注意，它与固定 $\alpha$ 时得到的结果（3.59）具有相同的形式，只是现在 $\mathbf{S}_N$ 的定义中出现的是期望值 $\mathbb{E}[\alpha]$。

### 10.3.3 下界

另一个重要的量是下界 $\mathcal{L}$，定义为

$$
\begin{aligned}
\mathcal{L}(q)&=\mathbb{E}[\ln p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})]-\mathbb{E}[\ln q(\mathbf{w},\alpha)]\\
&=\mathbb{E}_{\mathbf{w}}[\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})]+\mathbb{E}_{\mathbf{w},\alpha}[\ln p(\mathbf{w}\mid\alpha)]+\mathbb{E}_{\alpha}[\ln p(\alpha)]\\
&\quad-\mathbb{E}_{\alpha}[\ln q(\mathbf{w})]_{\mathbf{w}}-\mathbb{E}[\ln q(\alpha)].
\end{aligned}
\tag{10.107}
$$

利用前面各章得到的结果，可以直接计算各项，得到<span class="margin-reference">习题 10.27</span>

$$
\begin{aligned}
\mathbb{E}[\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})]_{\mathbf{w}}&=\frac{N}{2}\ln\left(\frac{\beta}{2\pi}\right)-\frac{\beta}{2}\boldsymbol{\mathsf{t}}^{\mathrm{T}}\boldsymbol{\mathsf{t}}+\beta\mathbf{m}_N^{\mathrm{T}}\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\mathsf{t}}\\
&\quad-\frac{\beta}{2}\operatorname{Tr}\left[\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\Phi}(\mathbf{m}_N\mathbf{m}_N^{\mathrm{T}}+\mathbf{S}_N)\right]
\end{aligned}
\tag{10.108}
$$

$$
\begin{aligned}
\mathbb{E}[\ln p(\mathbf{w}\mid\alpha)]_{\mathbf{w},\alpha}&=-\frac{M}{2}\ln(2\pi)+\frac{M}{2}(\psi(a_N)-\ln b_N)\\
&\quad-\frac{a_N}{2b_N}\left[\mathbf{m}_N^{\mathrm{T}}\mathbf{m}_N+\operatorname{Tr}(\mathbf{S}_N)\right]
\end{aligned}
\tag{10.109}
$$

$$
\begin{aligned}
\mathbb{E}[\ln p(\alpha)]_{\alpha}&=a_0\ln b_0+(a_0-1)[\psi(a_N)-\ln b_N]\\
&\quad-b_0\frac{a_N}{b_N}-\ln\Gamma(a_N)
\end{aligned}
\tag{10.110}
$$

$$
-\mathbb{E}[\ln q(\mathbf{w})]_{\mathbf{w}}=\frac{1}{2}\ln|\mathbf{S}_N|+\frac{M}{2}[1+\ln(2\pi)]
\tag{10.111}
$$

$$
-\mathbb{E}[\ln q(\alpha)]_{\alpha}=\ln\Gamma(a_N)-(a_N-1)\psi(a_N)-\ln b_N+a_N.
\tag{10.112}
$$

图 10.9 给出了下界 $\mathcal{L}(q)$ 随多项式模型次数的变化，使用的是由三次多项式生成的合成数据集。这里将先验参数设为 $a_0=b_0=0$，对应于无信息先验 $p(\alpha)\propto1/\alpha$；如第 2.3.6 节所述，这一先验在 $\ln\alpha$ 上是均匀的。正如第 10.1 节所见，$\mathcal{L}$ 表示模型的对数边缘似然 $p(\boldsymbol{\mathsf{t}}\mid M)$ 的下界。如果对不同的 $M$ 值赋予相等的先验概率 $p(M)$，就可以把 $\mathcal{L}$ 解释为模型后验概率 $p(M\mid\boldsymbol{\mathsf{t}})$ 的近似。因此，变分框架把最高概率赋给 $M=3$ 的模型。与之相比，最大似然方法会随着模型复杂度增加，不断给出更小的残差，直到残差降为零，因此会偏向严重过拟合的模型。

<!-- pdf-page: 510 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/a-fig-10-9.png" alt="多项式模型的变分下界随次数 M 变化，在 M 等于三时达到峰值"><figcaption>图 10.9：多项式模型的下界 $\mathcal{L}$ 随多项式次数 $M$ 的变化。数据集包含 $10$ 个数据点，由 $M=3$ 的多项式在区间 $(-5,5)$ 上采样，并加入方差为 $0.09$ 的高斯噪声生成。下界的值给出模型的对数概率，可以看到下界在 $M=3$ 处达到峰值，对应于生成该数据集的真实模型。</figcaption></figure>

## 10.4 指数族分布

在第 2 章，我们讨论过指数族分布及其共轭先验的重要作用。对于本书讨论的许多模型，完整数据的似然属于指数族。但是，观测数据的边缘似然函数通常并非如此。例如，在高斯混合模型中，观测 $\mathbf{x}_n$ 与对应隐藏变量 $\mathbf{z}_n$ 的联合分布属于指数族，而 $\mathbf{x}_n$ 的边缘分布是高斯混合，因此不属于指数族。

到目前为止，我们把模型中的变量分为观测变量和隐藏变量。现在进一步区分潜变量与参数，分别用 $\mathbf{Z}$ 和 $\boldsymbol{\theta}$ 表示。参数的数量固定，不随数据集大小改变（intensive）；潜变量的数量则随数据集大小增长（extensive）。例如，在高斯混合模型中，指示变量 $z_{kn}$ 表示潜变量，它指定由哪个分量 $k$ 负责生成数据点 $\mathbf{x}_n$；而均值 $\boldsymbol{\mu}_k$、精度 $\boldsymbol{\Lambda}_k$ 和混合比例 $\pi_k$ 则表示参数。

考虑数据独立同分布的情形。将数据值记为 $\mathbf{X}=\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，相应的潜变量为 $\mathbf{Z}=\{\mathbf{z}_n\}$。现在假设观测变量与潜变量的联合分布属于指数族，以自然参数 $\boldsymbol{\eta}$ 参数化，即

$$
p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\eta})=\prod_{n=1}^{N}h(\mathbf{x}_n,\mathbf{z}_n)g(\boldsymbol{\eta})\exp\left\{\boldsymbol{\eta}^{\mathrm{T}}\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)\right\}.
\tag{10.113}
$$

我们还将对 $\boldsymbol{\eta}$ 使用共轭先验，它可以写为

$$
p(\boldsymbol{\eta}\mid\nu_0,\mathbf{v}_0)=f(\nu_0,\boldsymbol{\chi}_0)g(\boldsymbol{\eta})^{\nu_0}\exp\left\{\nu_o\boldsymbol{\eta}^{\mathrm{T}}\boldsymbol{\chi}_0\right\}.
\tag{10.114}
$$

回顾一下，这个共轭先验分布可以解释为预先拥有 $\nu_0$ 个观测，并且这些观测的 $\mathbf{u}$ 向量都取值 $\boldsymbol{\chi}_0$。现在考虑一个变分

<!-- pdf-page: 511 -->

<!-- join-previous-paragraph -->
分布，它在潜变量与参数之间因子化，即 $q(\mathbf{Z},\boldsymbol{\eta})=q(\mathbf{Z})q(\boldsymbol{\eta})$。利用一般结果（10.9），可以按如下方式求出这两个因子：

$$
\begin{aligned}
\ln q^\star(\mathbf{Z})&=\mathbb{E}_{\boldsymbol{\eta}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\eta})]+\mathrm{const}\\
&=\sum_{n=1}^{N}\left\{\ln h(\mathbf{x}_n,\mathbf{z}_n)+\mathbb{E}[\boldsymbol{\eta}^{\mathrm{T}}]\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)\right\}+\mathrm{const}.
\end{aligned}
\tag{10.115}
$$

可见，它分解成了彼此独立的各项之和，每个 $n$ 对应一项，因此 $q^\star(\mathbf{Z})$ 的解会对 $n$ 因子化，即 $q^\star(\mathbf{Z})=\prod_nq^\star(\mathbf{z}_n)$。这是诱导的因子化的一个例子。<span class="margin-reference">第 10.2.5 节</span>对等式两边取指数，有

$$
q^\star(\mathbf{z}_n)=h(\mathbf{x}_n,\mathbf{z}_n)g\bigl(\mathbb{E}[\boldsymbol{\eta}]\bigr)\exp\left\{\mathbb{E}[\boldsymbol{\eta}^{\mathrm{T}}]\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)\right\}
\tag{10.116}
$$

其中，通过与指数族的标准形式比较，已重新补入归一化系数。

同样，对于参数的变分分布，有

$$
\ln q^\star(\boldsymbol{\eta})=\ln p(\boldsymbol{\eta}\mid\nu_0,\boldsymbol{\chi}_0)+\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\eta})]+\mathrm{const}
\tag{10.117}
$$

$$
{}=\nu_0\ln g(\boldsymbol{\eta})+\boldsymbol{\eta}^{\mathrm{T}}\boldsymbol{\chi}_0+\sum_{n=1}^{N}\left\{\ln g(\boldsymbol{\eta})+\boldsymbol{\eta}^{\mathrm{T}}\mathbb{E}_{\mathbf{z}_n}[\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)]\right\}+\mathrm{const}.
\tag{10.118}
$$

再次对等式两边取指数，并通过观察补入归一化系数，得到

$$
q^\star(\boldsymbol{\eta})=f(\nu_N,\boldsymbol{\chi}_N)g(\boldsymbol{\eta})^{\nu_N}\exp\left\{\boldsymbol{\eta}^{\mathrm{T}}\boldsymbol{\chi}_N\right\}
\tag{10.119}
$$

其中定义

$$
\nu_N=\nu_0+N
\tag{10.120}
$$

$$
\boldsymbol{\chi}_N=\boldsymbol{\chi}_0+\sum_{n=1}^{N}\mathbb{E}_{\mathbf{z}_n}[\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)].
\tag{10.121}
$$

注意，$q^\star(\mathbf{z}_n)$ 与 $q^\star(\boldsymbol{\eta})$ 的解相互耦合，因此要通过包含两个阶段的迭代过程求解。在变分 E 步中，利用当前潜变量后验分布 $q(\mathbf{z}_n)$ 计算充分统计量的期望 $\mathbb{E}[\mathbf{u}(\mathbf{x}_n,\mathbf{z}_n)]$，再用它计算更新后的参数后验分布 $q(\boldsymbol{\eta})$。接下来的变分 M 步则利用这个更新后的参数后验分布，求出自然参数的期望 $\mathbb{E}[\boldsymbol{\eta}^{\mathrm{T}}]$，从而得到更新后的潜变量变分分布。

### 10.4.1 变分消息传递

我们已经较详细地讨论了贝叶斯高斯混合这一具体模型，以说明变分方法的应用。这个模型可以用

<!-- pdf-page: 512 -->

<!-- join-previous-paragraph -->
图 10.5 所示的有向图描述。这里将更一般地讨论：对于用有向图描述的模型，如何使用变分方法，并推导出一些广泛适用的结果。

有向图对应的联合分布可以分解为

$$
p(\mathbf{x})=\prod_i p(\mathbf{x}_i\mid\mathrm{pa}_i)
\tag{10.122}
$$

其中，$\mathbf{x}_i$ 表示与节点 $i$ 对应的一个或多个变量，$\mathrm{pa}_i$ 表示节点 $i$ 的父节点集合。注意，$\mathbf{x}_i$ 可以是潜变量，也可以属于观测变量集合。现在考虑一种变分近似，假定分布 $q(\mathbf{x})$ 对 $\mathbf{x}_i$ 因子化，即

$$
q(\mathbf{x})=\prod_i q_i(\mathbf{x}_i).
\tag{10.123}
$$

注意，对于观测节点，变分分布中并不存在因子 $q(\mathbf{x}_i)$。现在将式（10.122）代入一般结果（10.9），得到

$$
\ln q_j^\star(\mathbf{x}_j)=\mathbb{E}_{i\ne j}\left[\sum_i\ln p(\mathbf{x}_i\mid\mathrm{pa}_i)\right]+\mathrm{const}.
\tag{10.124}
$$

右侧任何不依赖于 $\mathbf{x}_j$ 的项都可以吸收到加法常数中。实际上，依赖于 $\mathbf{x}_j$ 的项只有两类：$\mathbf{x}_j$ 自身的条件分布 $p(\mathbf{x}_j\mid\mathrm{pa}_j)$，以及条件集合中含有 $\mathbf{x}_j$ 的其他条件分布。根据定义，后一类条件分布对应于节点 $j$ 的子节点，因此也依赖于这些子节点的共同父节点，也就是除节点 $\mathbf{x}_j$ 自身以外，这些子节点的其他父节点。可见，$q^\star(\mathbf{x}_j)$ 所依赖的全部节点，恰好构成节点 $\mathbf{x}_j$ 的马尔可夫毯，如图 8.26 所示。因此，更新变分后验分布中的各个因子，对应于图上的局部计算。这样，就可以构建通用的变分推断软件，无须事先指定模型的形式（Bishop et al., 2003）。

现在进一步考虑所有条件分布都具有共轭指数族结构的模型，此时变分更新过程可以表示为局部消息传递算法（Winn and Bishop, 2005）。具体来说，一个节点收到其所有父节点和所有子节点的消息后，就可以更新与它对应的分布。这又要求其子节点事先已经收到来自共同父节点的消息。下界的计算也可以简化，因为许多所需的量已经在消息传递过程中算出。这种分布式消息传递形式具有良好的规模扩展特性，很适合大型网络。

<!-- pdf-page: 513 -->

## 10.5 局部变分方法

10.1 节和 10.2 节讨论的变分框架可以看作一种“全局”方法，因为它直接寻找所有随机变量的完整后验分布的近似。另一种“局部”方法，则为模型中单个变量或变量组上的函数寻找界。例如，我们可以为条件分布 $p(y\mid x)$ 寻找一个界，而这个条件分布本身只是在有向图所描述的更大概率模型中的一个因子。引入这个界的目的，当然是简化所得的分布。可以依次对多个变量应用这种局部近似，直到得到一个可处理的近似；在 10.6.1 节中，我们将以逻辑回归为背景，给出这种方法的实际例子。这里先着重讨论如何构造这些界。

在讨论 Kullback–Leibler 散度时，我们已经看到，对数函数的凸性在构造全局变分方法的下界时起了关键作用。此前，我们把（严格）凸函数定义为每条弦都位于函数图像上方的函数（1.6.1 节）。凸性在局部变分框架中同样起着核心作用。注意，只要互换“min”和“max”，并将下界换为上界，以下讨论也同样适用于凹函数。

先考虑一个简单例子，即函数 $f(x)=\exp(-x)$。它是关于 $x$ 的凸函数，如图 10.10 左图所示。我们的目标是用一个更简单的函数来近似 $f(x)$，具体而言，用 $x$ 的线性函数。由图 10.10 可以看到，如果这个线性函数对应于一条切线，它就是 $f(x)$ 的下界。对某个特定的 $x$ 值，例如 $x=\xi$，作一阶泰勒展开，就能得到切线 $y(x)$：

$$
y(x)=f(\xi)+f'(\xi)(x-\xi)
\tag{10.125}
$$

因此 $y(x)\leqslant f(x)$，在 $x=\xi$ 时取等号。对于我们的示例函数 $f(x)=$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-10.png" alt="左图以红色指数曲线及蓝绿切线示意下界，右图显示对偶目标关于斜率的最大值"><figcaption>图 10.10：左图中的红色曲线表示函数 $\exp(-x)$，蓝色直线表示由（10.125）定义的、在 $x=\xi$ 处的切线，其中 $\xi=1$。这条直线的斜率为 $\lambda=f'(\xi)=-\exp(-\xi)$。注意，任何其他切线，例如图中的绿色直线，在 $x=\xi$ 处都会有更小的 $y$ 值。右图给出了相应的函数 $\lambda\xi-g(\lambda)$ 关于 $\lambda$ 的图像，其中 $g(\lambda)$ 由（10.131）给出，$\xi=1$；最大值对应于 $\lambda=-\exp(-\xi)=-1/e$。</figcaption><p class="figure-translation">$x$：自变量；$\xi$：切点的横坐标；$\lambda$：切线斜率；$\lambda\xi-g(\lambda)$：在给定 $\xi$ 处的对偶表达式。</p></figure>

<!-- pdf-page: 514 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-11.png" alt="凸函数与给定斜率直线之间的最短竖直距离决定切线截距，左右两图展示上移前后"><figcaption>图 10.11：左图中的红色曲线表示凸函数 $f(x)$，蓝色直线表示线性函数 $\lambda x$。它是 $f(x)$ 的下界，因为对所有 $x$ 都有 $f(x)>\lambda x$。对于给定的斜率 $\lambda$，关于 $x$ 最小化差值 $f(x)-\lambda x$（以绿色虚线表示），就能找到具有相同斜率的切线的切点。由此定义对偶函数 $g(\lambda)$，它对应于斜率为 $\lambda$ 的切线的截距的负值。</figcaption><p class="figure-translation">$x$、$y$：横轴和纵轴变量；$f(x)$：凸函数；$\lambda x$：上移前的直线；$\lambda x-g(\lambda)$：切线；$-g(\lambda)$：切线在纵轴上的截距。</p></figure>

<!-- join-previous-paragraph-across-figures -->
$\exp(-x)$，因此得到如下形式的切线：

$$
y(x)=\exp(-\xi)-\exp(-\xi)(x-\xi)
\tag{10.126}
$$

这是一个由 $\xi$ 参数化的线性函数。为与后面的讨论一致，定义 $\lambda=-\exp(-\xi)$，于是

$$
y(x,\lambda)=\lambda x-\lambda+\lambda\ln(-\lambda).
\tag{10.127}
$$

不同的 $\lambda$ 值对应不同的切线；由于所有这些直线都是函数的下界，有 $f(x)\geqslant y(x,\lambda)$。因此，可以将该函数写为

$$
f(x)=\max_{\lambda}\{\lambda x-\lambda+\lambda\ln(-\lambda)\}.
\tag{10.128}
$$

我们已经成功地用一个更简单的线性函数 $y(x,\lambda)$ 来近似凸函数 $f(x)$。付出的代价是引入了一个变分参数 $\lambda$；为得到最紧的界，必须关于 $\lambda$ 进行优化。

利用*凸对偶性*（convex duality）的框架，可以更一般地表述这种方法（Rockafellar, 1972; Jordan et al., 1999）。考虑图 10.11 左图所示的凸函数 $f(x)$。在这个例子中，函数 $\lambda x$ 是 $f(x)$ 的下界，但它不是斜率为 $\lambda$ 的线性函数所能达到的最佳下界，因为最紧的界由切线给出。将斜率为 $\lambda$ 的切线方程写成 $\lambda x-g(\lambda)$，其中截距的负值 $g(\lambda)$ 显然依赖于切线斜率 $\lambda$。为了确定截距，注意，直线必须竖直移动一段距离，其大小等于直线与函数之间的最小竖直距离，如图 10.11 所示。因此

$$
\begin{aligned}
g(\lambda)&=-\min_x\{f(x)-\lambda x\}\\
&=\max_x\{\lambda x-f(x)\}.
\end{aligned}
\tag{10.129}
$$

<!-- pdf-page: 515 -->

现在，可以不固定 $\lambda$ 并改变 $x$，而是考虑一个特定的 $x$，然后调整 $\lambda$，直到切平面恰好在这个 $x$ 处相切。因为对于某个特定的 $x$，当它恰好对应于切点时，切线的 $y$ 值达到最大，所以有

$$
f(x)=\max_{\lambda}\{\lambda x-g(\lambda)\}.
\tag{10.130}
$$

可以看到，函数 $f(x)$ 和 $g(\lambda)$ 具有对偶的作用，并通过（10.129）和（10.130）相联系。

将这些对偶关系应用于简单例子 $f(x)=\exp(-x)$。由（10.129）可知，使其达到最大值的 $x$ 由 $\xi=-\ln(-\lambda)$ 给出，回代后得到共轭函数 $g(\lambda)$：

$$
g(\lambda)=\lambda-\lambda\ln(-\lambda)
\tag{10.131}
$$

这与前面得到的结果相同。图 10.10 右图显示了 $\xi=1$ 时的函数 $\lambda\xi-g(\lambda)$。为了验证，将（10.131）代入（10.130），得到使其达到最大值的 $\lambda=-\exp(-x)$，再回代就恢复了原函数 $f(x)=\exp(-x)$。

对于凹函数，可以通过类似论证得到上界，只需把“max”换成“min”，于是

$$
f(x)=\min_{\lambda}\{\lambda x-g(\lambda)\}
\tag{10.132}
$$

$$
g(\lambda)=\min_x\{\lambda x-f(x)\}.
\tag{10.133}
$$

如果所关注的函数不是凸函数（或凹函数），就不能直接应用上述方法来得到界。不过，可以先对函数或其自变量寻找可逆变换，将其变为凸形式。然后计算共轭函数，再变换回原来的变量。

一个在模式识别中经常出现的重要例子，是如下定义的 logistic sigmoid 函数：

$$
\sigma(x)=\frac{1}{1+e^{-x}}.
\tag{10.134}
$$

这个函数本身既不是凸函数，也不是凹函数。不过，对它取对数后得到的是凹函数，这很容易通过求二阶导数来验证（习题 10.30）。根据（10.133），相应的共轭函数具有如下形式：

$$
g(\lambda)=\min_x\{\lambda x-f(x)\}=-\lambda\ln\lambda-(1-\lambda)\ln(1-\lambda)
\tag{10.135}
$$

可以看出，这正是一个取值为 $1$ 的概率为 $\lambda$ 的变量的二元熵函数（附录 B）。利用（10.132），得到对数 sigmoid 的上界：

$$
\ln\sigma(x)\leqslant\lambda x-g(\lambda)
\tag{10.136}
$$

<!-- pdf-page: 516 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-12.png" alt="左图以指数函数给出logistic sigmoid的两个上界，右图以高斯形函数给出在正负ξ处相切的下界"><figcaption>图 10.12：左图以红色显示（10.134）定义的 logistic sigmoid 函数 $\sigma(x)$，并以蓝色显示指数上界（10.137）的两个例子。右图同样以红色显示 logistic sigmoid，以蓝色显示高斯下界（10.144）。这里参数 $\xi=2.5$，在绿色虚线标出的 $x=\xi$ 和 $x=-\xi$ 处，这个界是精确的。</figcaption><p class="figure-translation">左图的 $\lambda=0.2$ 和 $\lambda=0.7$ 为两个上界的参数值；右图的 $\xi=2.5$ 为下界参数，$-\xi$ 与 $\xi$ 标出下界与原函数相等的两个位置。</p></figure>

对两边取指数，就得到 logistic sigmoid 本身的上界：

$$
\sigma(x)\leqslant\exp(\lambda x-g(\lambda))
\tag{10.137}
$$

图 10.12 左图绘出了两个不同 $\lambda$ 值对应的上界。

我们还可以得到一个具有高斯函数形式的 sigmoid 下界。为此，按照 Jaakkola and Jordan（2000）的方法，同时对输入变量和函数本身作变换。首先对 logistic 函数取对数，再分解为

$$
\begin{aligned}
\ln\sigma(x)&=-\ln(1+e^{-x})=-\ln\left\{e^{-x/2}(e^{x/2}+e^{-x/2})\right\}\\
&=x/2-\ln(e^{x/2}+e^{-x/2}).
\end{aligned}
\tag{10.138}
$$

注意，函数 $f(x)=-\ln(e^{x/2}+e^{-x/2})$ 是变量 $x^2$ 的凸函数，这同样可以通过求二阶导数来验证（习题 10.31）。由此得到 $f(x)$ 的下界，它是 $x^2$ 的线性函数，其共轭函数为

$$
g(\lambda)=\max_{x^2}\left\{\lambda x^2-f\left(\sqrt{x^2}\right)\right\}.
\tag{10.139}
$$

驻点条件给出

$$
0=\lambda-\frac{dx}{dx^2}\frac{d}{dx}f(x)=\lambda+\frac{1}{4x}\tanh\left(\frac{x}{2}\right).
\tag{10.140}
$$

将这个 $x$ 值记为 $\xi$，它对应于给定 $\lambda$ 值时切线的切点，于是

$$
\lambda(\xi)=-\frac{1}{4\xi}\tanh\left(\frac{\xi}{2}\right)=-\frac{1}{2\xi}\left[\sigma(\xi)-\frac{1}{2}\right].
\tag{10.141}
$$

<!-- pdf-page: 517 -->

可以让 $\xi$ 而不是 $\lambda$ 充当变分参数，因为这样能得到更简单的共轭函数表达式：

$$
g(\lambda)=\lambda(\xi)\xi^2-f(\xi)=\lambda(\xi)\xi^2+\ln(e^{\xi/2}+e^{-\xi/2}).
\tag{10.142}
$$

因此，$f(x)$ 的界可以写成

$$
f(x)\geqslant\lambda x^2-g(\lambda)=\lambda x^2-\lambda\xi^2-\ln(e^{\xi/2}+e^{-\xi/2}).
\tag{10.143}
$$

于是，sigmoid 的界变为

$$
\sigma(x)\geqslant\sigma(\xi)\exp\left\{(x-\xi)/2-\lambda(\xi)(x^2-\xi^2)\right\}
\tag{10.144}
$$

其中 $\lambda(\xi)$ 由（10.141）定义。图 10.12 右图展示了这个界。可以看到，它具有对 $x$ 的二次函数取指数的形式；当我们希望用高斯分布表示通过 logistic sigmoid 函数定义的后验分布时，这种形式将很有用（4.5 节）。

logistic sigmoid 经常出现在二元变量的概率模型中，因为它能把对数几率转换为后验概率。对于多类别分布，相应的变换由 softmax 函数给出（4.3 节）。遗憾的是，这里为 logistic sigmoid 推导的下界不能直接推广到 softmax。Gibbs（1997）提出了一种构造高斯分布的方法，并推测该分布是一个界（虽然没有给出严格证明）；这种方法可以将局部变分方法应用于多类别问题。

我们将在 10.6.1 节看到局部变分界的应用示例。不过，现在先从一般角度考察如何使用这些界，会有助于理解。假设要计算如下形式的积分：

$$
I=\int\sigma(a)p(a)\,da
\tag{10.145}
$$

其中 $\sigma(a)$ 是 logistic sigmoid，$p(a)$ 是高斯概率密度。例如，在贝叶斯模型中计算预测分布时，就会出现这样的积分，此时 $p(a)$ 表示参数的后验分布。由于这个积分难以求解，我们采用变分界（10.144），并将其写成 $\sigma(a)\geqslant f(a,\xi)$，其中 $\xi$ 是变分参数。积分中的函数现在成为两个二次指数函数的乘积，因此可以解析积分，得到 $I$ 的界：

$$
I\geqslant\int f(a,\xi)p(a)\,da=F(\xi).
\tag{10.146}
$$

现在可以自由选择变分参数 $\xi$；具体做法是寻找使函数 $F(\xi)$ 最大的值 $\xi^{\star}$。所得的 $F(\xi^{\star})$ 表示这一族界中最紧的界，可以用来近似 $I$。不过，这个优化后的界通常并不精确。

<!-- pdf-page: 518 -->
<!-- join-previous-paragraph -->
虽然 logistic sigmoid 的界 $\sigma(a)\geqslant f(a,\xi)$ 可以精确优化，但所需的 $\xi$ 取值依赖于 $a$，所以这个界只在一个 $a$ 值处精确。由于 $F(\xi)$ 是对 $a$ 的所有取值积分得到的，$\xi^{\star}$ 就代表一种由分布 $p(a)$ 加权的折中。

## 10.6 变分逻辑回归

现在回到 4.5 节研究的贝叶斯逻辑回归模型，以此说明局部变分方法的使用。此前我们着重使用拉普拉斯近似，这里则考虑基于 Jaakkola and Jordan（2000）方法的变分处理。与拉普拉斯方法一样，这种处理也得到后验分布的高斯近似。不过，变分近似具有更大的灵活性，因此比拉普拉斯方法更精确。此外，与拉普拉斯方法不同，变分方法优化的是一个定义明确的目标函数，它由模型证据的严格界给出。Dybowski and Roberts（2005）还使用蒙特卡洛采样技术，从贝叶斯角度研究了逻辑回归。

### 10.6.1 变分后验分布

这里将使用基于 10.5 节所介绍的局部界的变分近似。这样，由 logistic sigmoid 决定的逻辑回归似然函数，就能用一个二次型的指数来近似。因此，再次选用（4.140）形式的共轭高斯先验会很方便。暂时把超参数 $\mathbf{m}_0$ 和 $\mathbf{S}_0$ 视为固定常数。10.6.3 节将说明，如何把变分方法推广到存在未知超参数、需要从数据推断这些超参数取值的情况。

在变分框架中，我们希望最大化边缘似然的下界。对于贝叶斯逻辑回归模型，边缘似然具有如下形式：

$$
p(\boldsymbol{\mathsf{t}})=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\,d\mathbf{w}=\int\left[\prod_{n=1}^{N}p(t_n\mid\mathbf{w})\right]p(\mathbf{w})\,d\mathbf{w}.
\tag{10.147}
$$

首先注意，$t$ 的条件分布可以写成

$$
\begin{aligned}
p(t\mid\mathbf{w})&=\sigma(a)^t\{1-\sigma(a)\}^{1-t}\\
&=\left(\frac{1}{1+e^{-a}}\right)^t\left(1-\frac{1}{1+e^{-a}}\right)^{1-t}\\
&=e^{at}\frac{e^{-a}}{1+e^{-a}}=e^{at}\sigma(-a)
\end{aligned}
\tag{10.148}
$$

其中 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$。为了得到 $p(\boldsymbol{\mathsf{t}})$ 的下界，我们利用（10.144）给出的 logistic sigmoid 函数的变分下界。为方便起见，

<!-- pdf-page: 519 -->
<!-- join-previous-paragraph -->
在这里将它重列如下：

$$
\sigma(z)\geqslant\sigma(\xi)\exp\left\{(z-\xi)/2-\lambda(\xi)(z^2-\xi^2)\right\}
\tag{10.149}
$$

其中

$$
\lambda(\xi)=\frac{1}{2\xi}\left[\sigma(\xi)-\frac{1}{2}\right].
\tag{10.150}
$$

因此，可以写成

$$
p(t\mid\mathbf{w})=e^{at}\sigma(-a)\geqslant e^{at}\sigma(\xi)\exp\left\{-(a+\xi)/2-\lambda(\xi)(a^2-\xi^2)\right\}.
\tag{10.151}
$$

注意，由于这个界分别应用于似然函数中的每一项，每个训练集观测 $(\boldsymbol{\phi}_n,t_n)$ 都对应一个变分参数 $\xi_n$。使用 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$，再乘以先验分布，得到 $\boldsymbol{\mathsf{t}}$ 和 $\mathbf{w}$ 的联合分布的如下界：

$$
p(\boldsymbol{\mathsf{t}},\mathbf{w})=p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\geqslant h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})
\tag{10.152}
$$

其中 $\boldsymbol{\xi}$ 表示变分参数的集合 $\{\xi_n\}$，并且

$$
\begin{aligned}
h(\mathbf{w},\boldsymbol{\xi})={}&\prod_{n=1}^{N}\sigma(\xi_n)\exp\Bigl\{\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n t_n-(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n+\xi_n)/2\\
&-\lambda(\xi_n)([\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n]^2-\xi_n^2)\Bigr\}.
\end{aligned}
\tag{10.153}
$$

计算精确后验分布，需要将这个不等式的左侧归一化。由于这难以处理，我们改为处理右侧。注意，右侧函数尚未归一化，因此不能解释为概率密度。不过，一旦将它归一化，得到变分后验分布 $q(\mathbf{w})$，它就不再表示一个界。

由于对数函数单调递增，不等式 $A\geqslant B$ 意味着 $\ln A\geqslant\ln B$。由此得到 $\boldsymbol{\mathsf{t}}$ 和 $\mathbf{w}$ 的联合分布的对数下界：

$$
\begin{aligned}
\ln\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\}\geqslant{}&\ln p(\mathbf{w})+\sum_{n=1}^{N}\Bigl\{\ln\sigma(\xi_n)+\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n t_n\\
&-(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n+\xi_n)/2-\lambda(\xi_n)([\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n]^2-\xi_n^2)\Bigr\}.
\end{aligned}
\tag{10.154}
$$

代入先验 $p(\mathbf{w})$，这个不等式的右侧作为 $\mathbf{w}$ 的函数，变为

$$
\begin{aligned}
&-\frac{1}{2}(\mathbf{w}-\mathbf{m}_0)^{\mathrm T}\mathbf{S}_0^{-1}(\mathbf{w}-\mathbf{m}_0)\\
&+\sum_{n=1}^{N}\left\{\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n(t_n-1/2)-\lambda(\xi_n)\mathbf{w}^{\mathrm T}(\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T})\mathbf{w}\right\}+\mathrm{const}.
\end{aligned}
\tag{10.155}
$$

<!-- pdf-page: 520 -->

这是 $\mathbf{w}$ 的二次函数，因此可以通过识别 $\mathbf{w}$ 的一次项和二次项，得到相应的后验分布变分近似，从而得到如下形式的高斯变分后验：

$$
q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\mathbf{S}_N)
\tag{10.156}
$$

其中

$$
\mathbf{m}_N=\mathbf{S}_N\left(\mathbf{S}_0^{-1}\mathbf{m}_0+\sum_{n=1}^{N}(t_n-1/2)\boldsymbol{\phi}_n\right)
\tag{10.157}
$$

$$
\mathbf{S}_N^{-1}=\mathbf{S}_0^{-1}+2\sum_{n=1}^{N}\lambda(\xi_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{10.158}
$$

与拉普拉斯框架一样，我们再次得到了后验分布的高斯近似。不过，变分参数 $\{\xi_n\}$ 提供了额外的灵活性，提高了近似的精度（Jaakkola and Jordan，2000）。

这里考虑的是一次性获得全部训练数据的批量学习情形。不过，贝叶斯方法本来就很适合序贯学习：每次处理一个数据点，处理后就将它丢弃。将这个变分方法写成序贯形式很直接（习题 10.32）。

注意，（10.149）给出的界只适用于两类问题，因此这种方法不能直接推广到具有 $K>2$ 个类别的分类问题。Gibbs（1997）研究了适用于多类别情形的另一种界。

### 10.6.2 优化变分参数

现在已经得到了后验分布的归一化高斯近似，稍后将用它计算新数据点的预测分布。不过，首先需要通过最大化边缘似然的下界，来确定变分参数 $\{\xi_n\}$。

为此，将不等式（10.152）代回边缘似然，得到

$$
\ln p(\boldsymbol{\mathsf{t}})=\ln\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\,d\mathbf{w}\geqslant\ln\int h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})\,d\mathbf{w}=\mathcal{L}(\boldsymbol{\xi}).
\tag{10.159}
$$

与 3.5 节线性回归模型中超参数 $\alpha$ 的优化一样，确定 $\xi_n$ 有两种方法。第一种方法注意到，函数 $\mathcal{L}(\boldsymbol{\xi})$ 是通过对 $\mathbf{w}$ 积分定义的，因此可以把 $\mathbf{w}$ 视为潜变量，并使用 EM 算法。第二种方法先对 $\mathbf{w}$ 作解析积分，再直接关于 $\boldsymbol{\xi}$ 最大化。先考虑 EM 方法。

EM 算法首先为参数 $\{\xi_n\}$ 选择初始值，将它们合记为 $\boldsymbol{\xi}^{\mathrm{old}}$。在 EM 算法的 E 步中，

<!-- pdf-page: 521 -->
<!-- join-previous-paragraph -->
用这些参数值求出（10.156）给出的 $\mathbf{w}$ 的后验分布。在 M 步中，最大化完整数据对数似然的期望：

$$
\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})=\mathbb{E}\left[\ln\{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})\}\right]
\tag{10.160}
$$

其中，期望是关于使用 $\boldsymbol{\xi}^{\mathrm{old}}$ 计算出的后验分布 $q(\mathbf{w})$ 取的。注意到 $p(\mathbf{w})$ 不依赖于 $\boldsymbol{\xi}$，再代入 $h(\mathbf{w},\boldsymbol{\xi})$，得到

$$
\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})=\sum_{n=1}^{N}\left\{\ln\sigma(\xi_n)-\xi_n/2-\lambda(\xi_n)\left(\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n-\xi_n^2\right)\right\}+\mathrm{const}
\tag{10.161}
$$

其中“const”表示与 $\boldsymbol{\xi}$ 无关的项。现在令关于 $\xi_n$ 的导数等于零。利用 $\sigma(\xi)$ 和 $\lambda(\xi)$ 的定义，经过几步代数运算，得到

$$
0=\lambda'(\xi_n)\left(\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n-\xi_n^2\right).
\tag{10.162}
$$

注意，对于 $\xi\geqslant0$，$\lambda'(\xi)$ 是 $\xi$ 的单调函数；而且由于这个界关于 $\xi=0$ 对称，可以不失一般性地只考虑 $\xi$ 的非负值。因此 $\lambda'(\xi)\neq0$，从而得到如下重估方程（习题 10.33）：

$$
(\xi_n^{\mathrm{new}})^2=\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n=\boldsymbol{\phi}_n^{\mathrm T}\left(\mathbf{S}_N+\mathbf{m}_N\mathbf{m}_N^{\mathrm T}\right)\boldsymbol{\phi}_n
\tag{10.163}
$$

这里使用了（10.156）。

下面归纳求变分后验分布的 EM 算法。首先初始化变分参数 $\boldsymbol{\xi}^{\mathrm{old}}$。在 E 步中，计算（10.156）给出的 $\mathbf{w}$ 的后验分布，其中均值和协方差由（10.157）和（10.158）定义。在 M 步中，利用这个变分后验，通过（10.163）计算新的 $\boldsymbol{\xi}$ 值。反复执行 E 步和 M 步，直到满足合适的收敛判据；在实践中，通常只需少量迭代。

另一种获得 $\boldsymbol{\xi}$ 的重估方程的方法，是注意到下界 $\mathcal{L}(\boldsymbol{\xi})$ 的定义（10.159）中，对 $\mathbf{w}$ 的积分具有类高斯的被积函数，因此可以解析求出该积分。求出积分后，再对 $\xi_n$ 求导。结果表明，这得到的重估方程与 EM 方法的（10.163）完全相同（习题 10.34）。

正如前面已经强调的，在应用变分方法时，能够计算（10.159）给出的下界 $\mathcal{L}(\boldsymbol{\xi})$ 很有用。注意到 $p(\mathbf{w})$ 是高斯分布，而 $h(\mathbf{w},\boldsymbol{\xi})$ 是 $\mathbf{w}$ 的二次函数的指数，就可以对 $\mathbf{w}$ 作解析积分。因此，通过配方并使用高斯分布归一化系数的标准结果，可以得到如下形式的闭式解（习题 10.35）：

<!-- pdf-page: 522 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-13.png" alt="线性可分的两类数据，左图显示变分预测等高线，右图显示后验抽样的五条决策边界"><figcaption>图 10.13：对一个简单的线性可分数据集应用贝叶斯逻辑回归的示例。左图显示用变分推断得到的预测分布。可以看到，决策边界大致位于两簇数据点的中间；预测分布的等高线在远离数据的地方向外展开，反映出这些区域的分类具有更大的不确定性。右图显示从后验分布 $p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})$ 中抽取的五个参数向量 $\mathbf{w}$ 样本所对应的决策边界。</figcaption><p class="figure-translation">左图标出的 $0.01$、$0.25$、$0.75$、$0.99$ 为预测概率等高线的值；红色叉号与圆圈表示两个类别；右图的五条直线对应五次后验抽样。</p></figure>

$$
\begin{aligned}
\mathcal{L}(\boldsymbol{\xi})={}&\frac{1}{2}\ln\frac{|\mathbf{S}_N|}{|\mathbf{S}_0|}-\frac{1}{2}\mathbf{m}_N^{\mathrm T}\mathbf{S}_N^{-1}\mathbf{m}_N+\frac{1}{2}\mathbf{m}_0^{\mathrm T}\mathbf{S}_0^{-1}\mathbf{m}_0\\
&+\sum_{n=1}^{N}\left\{\ln\sigma(\xi_n)-\frac{1}{2}\xi_n-\lambda(\xi_n)\xi_n^2\right\}.
\end{aligned}
\tag{10.164}
$$

这种变分框架也可以应用于数据依次到达的情况（Jaakkola and Jordan，2000）。此时，维护一个关于 $\mathbf{w}$ 的高斯后验分布，并用先验 $p(\mathbf{w})$ 来初始化它。每到达一个数据点，就利用界（10.151）更新后验，然后归一化，得到更新后的后验分布。

预测分布通过对后验分布边缘化得到，其形式与 4.5.2 节讨论的拉普拉斯近似相同。图 10.13 显示了一个合成数据集的变分预测分布。这个例子有助于理解 7.1 节讨论的“大间隔”概念；它的行为与贝叶斯解在定性上相似。

### 10.6.3 超参数推断

到目前为止，我们一直把先验分布中的超参数 $\alpha$ 视为已知常数。现在扩展贝叶斯逻辑回归模型，使这个参数的值可以从数据集中推断出来。将全局和局部变分近似结合在同一个框架中，就能做到这一点，同时在每个阶段都保持边缘似然的下界。Bishop and Svensén（2003）在对层次专家混合模型进行贝叶斯处理时，采用过这种结合的方法。

<!-- pdf-page: 523 -->

具体而言，再次考虑一个简单的各向同性高斯先验分布：

$$
p(\mathbf{w}\mid\alpha)=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I}).
\tag{10.165}
$$

这种分析很容易推广到更一般的高斯先验，例如，希望对参数 $w_j$ 的不同子集关联不同的超参数时。与通常的做法一样，为 $\alpha$ 选择伽马分布形式的共轭超先验：

$$
p(\alpha)=\operatorname{Gam}(\alpha\mid a_0,b_0)
\tag{10.166}
$$

它由常数 $a_0$ 和 $b_0$ 控制。

这个模型的边缘似然现在具有如下形式：

$$
p(\boldsymbol{\mathsf{t}})=\iint p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})\,d\mathbf{w}\,d\alpha
\tag{10.167}
$$

其中联合分布为

$$
p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})=p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\alpha)p(\alpha).
\tag{10.168}
$$

现在面对的是一个难以解析求解的、关于 $\mathbf{w}$ 和 $\alpha$ 的积分。我们将在同一个模型中同时使用局部和全局变分方法来处理它。

首先引入变分分布 $q(\mathbf{w},\alpha)$，再应用分解（10.2），在这里它的形式为

$$
\ln p(\boldsymbol{\mathsf{t}})=\mathcal{L}(q)+\operatorname{KL}(q\|p)
\tag{10.169}
$$

其中，下界 $\mathcal{L}(q)$ 和 Kullback–Leibler 散度 $\operatorname{KL}(q\|p)$ 定义为

$$
\mathcal{L}(q)=\iint q(\mathbf{w},\alpha)\ln\left\{\frac{p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha
\tag{10.170}
$$

$$
\operatorname{KL}(q\|p)=-\iint q(\mathbf{w},\alpha)\ln\left\{\frac{p(\mathbf{w},\alpha\mid\boldsymbol{\mathsf{t}}))}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha.
\tag{10.171}
$$

此时，由于似然因子 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})$ 的形式，下界 $\mathcal{L}(q)$ 仍然难以处理。因此，像前面一样，对每个 logistic sigmoid 因子应用局部变分界。这样就能利用不等式（10.152），为 $\mathcal{L}(q)$ 再给出一个下界，它也因此是对数边缘似然的下界：

$$
\begin{aligned}
\ln p(\boldsymbol{\mathsf{t}})&\geqslant\mathcal{L}(q)\geqslant\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})\\
&=\iint q(\mathbf{w},\alpha)\ln\left\{\frac{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w}\mid\alpha)p(\alpha)}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha.
\end{aligned}
\tag{10.172}
$$

接着，假设变分分布可以在参数和超参数之间分解，即

$$
q(\mathbf{w},\alpha)=q(\mathbf{w})q(\alpha).
\tag{10.173}
$$

<!-- pdf-page: 524 -->

有了这种因子化，就可以利用一般结果（10.9）求出最优因子的表达式。先考虑分布 $q(\mathbf{w})$。去掉与 $\mathbf{w}$ 无关的项，得到

$$
\begin{aligned}
\ln q(\mathbf{w})&=\mathbb{E}_{\alpha}\left[\ln\{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w}\mid\alpha)p(\alpha)\}\right]+\mathrm{const}\\
&=\ln h(\mathbf{w},\boldsymbol{\xi})+\mathbb{E}_{\alpha}[\ln p(\mathbf{w}\mid\alpha)]+\mathrm{const}.
\end{aligned}
$$

现在使用（10.153）代入 $\ln h(\mathbf{w},\boldsymbol{\xi})$，并使用（10.165）代入 $\ln p(\mathbf{w}\mid\alpha)$，得到

$$
\ln q(\mathbf{w})=-\frac{\mathbb{E}[\alpha]}{2}\mathbf{w}^{\mathrm T}\mathbf{w}+\sum_{n=1}^{N}\left\{(t_n-1/2)\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n-\lambda(\xi_n)\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}\mathbf{w}\right\}+\mathrm{const}.
$$

可以看到，这是 $\mathbf{w}$ 的二次函数，因此 $q(\mathbf{w})$ 的解将是高斯分布。按通常的方法配方，得到

$$
q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\boldsymbol{\mu}_N,\boldsymbol{\Sigma}_N)
\tag{10.174}
$$

其中定义

$$
\boldsymbol{\Sigma}_N^{-1}\boldsymbol{\mu}_N=\sum_{n=1}^{N}(t_n-1/2)\boldsymbol{\phi}_n
\tag{10.175}
$$

$$
\boldsymbol{\Sigma}_N^{-1}=\mathbb{E}[\alpha]\mathbf{I}+2\sum_{n=1}^{N}\lambda(\xi_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{10.176}
$$

类似地，因子 $q(\alpha)$ 的最优解由下式得到：

$$
\ln q(\alpha)=\mathbb{E}_{\mathbf{w}}[\ln p(\mathbf{w}\mid\alpha)]+\ln p(\alpha)+\mathrm{const}.
$$

使用（10.165）代入 $\ln p(\mathbf{w}\mid\alpha)$，并使用（10.166）代入 $\ln p(\alpha)$，得到

$$
\ln q(\alpha)=\frac{M}{2}\ln\alpha-\frac{\alpha}{2}\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]+(a_0-1)\ln\alpha-b_0\alpha+\mathrm{const}.
$$

可以看出，这是伽马分布的对数，因此得到

$$
q(\alpha)=\operatorname{Gam}(\alpha\mid a_N,b_N)=\frac{1}{\Gamma(a_0)}a_0^{b_0}\alpha^{a_0-1}e^{-b_0\alpha}
\tag{10.177}
$$

其中

$$
a_N=a_0+\frac{M}{2}
\tag{10.178}
$$

$$
b_N=b_0+\frac{1}{2}\mathbb{E}_{\mathbf{w}}[\mathbf{w}^{\mathrm T}\mathbf{w}].
\tag{10.179}
$$

<!-- pdf-page: 525 -->

还需要优化变分参数 $\xi_n$，这同样通过最大化下界 $\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})$ 来实现。省略与 $\boldsymbol{\xi}$ 无关的项，并对 $\alpha$ 积分，得到

$$
\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})=\int q(\mathbf{w})\ln h(\mathbf{w},\boldsymbol{\xi})\,d\mathbf{w}+\mathrm{const}.
\tag{10.180}
$$

注意，它的形式与（10.159）完全相同，因此可以再次利用之前的结果（10.163）。该结果可以通过直接优化边缘似然函数得到，从而产生如下形式的重估方程：

$$
(\xi_n^{\mathrm{new}})^2=\boldsymbol{\phi}_n^{\mathrm T}\left(\boldsymbol{\Sigma}_N+\boldsymbol{\mu}_N\boldsymbol{\mu}_N^{\mathrm T}\right)\boldsymbol{\phi}_n.
\tag{10.181}
$$

我们已经得到了 $q(\mathbf{w})$、$q(\alpha)$ 和 $\boldsymbol{\xi}$ 这三个量的重估方程，因此，在适当初始化之后，就可以循环地依次更新它们。所需的矩为（附录 B）

$$
\mathbb{E}[\alpha]=\frac{a_N}{b_N}
\tag{10.182}
$$

$$
\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]=\boldsymbol{\Sigma}_N+\boldsymbol{\mu}_N^{\mathrm T}\boldsymbol{\mu}_N.
\tag{10.183}
$$

## 10.7 期望传播

本章最后讨论另一种确定性近似推断，称为*期望传播*（expectation propagation，EP）（Minka, 2001a; Minka, 2001b）。与前面讨论的变分贝叶斯方法一样，它也基于最小化 Kullback–Leibler 散度，但使用相反方向的形式，因此得到的近似具有很不相同的性质。

先考虑关于 $q(\mathbf{z})$ 最小化 $\operatorname{KL}(p\|q)$ 的问题，其中 $p(\mathbf{z})$ 是固定分布，而 $q(\mathbf{z})$ 属于指数族，因此由（2.194）可写成

$$
q(\mathbf{z})=h(\mathbf{z})g(\boldsymbol{\eta})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{z})\}.
\tag{10.184}
$$

作为 $\boldsymbol{\eta}$ 的函数，Kullback–Leibler 散度变为

$$
\operatorname{KL}(p\|q)=-\ln g(\boldsymbol{\eta})-\boldsymbol{\eta}^{\mathrm T}\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})]+\mathrm{const}
\tag{10.185}
$$

其中常数项与自然参数 $\boldsymbol{\eta}$ 无关。令关于 $\boldsymbol{\eta}$ 的梯度为零，就能在这族分布中最小化 $\operatorname{KL}(p\|q)$，得到

$$
-\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})].
\tag{10.186}
$$

不过，由（2.226）已经知道，$\ln g(\boldsymbol{\eta})$ 的负梯度等于 $\mathbf{u}(\mathbf{z})$ 在分布 $q(\mathbf{z})$ 下的期望。令这两个结果相等，得到

$$
\mathbb{E}_{q(\mathbf{z})}[\mathbf{u}(\mathbf{z})]=\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})].
\tag{10.187}
$$

<!-- pdf-page: 526 -->

可以看到，最优解就对应于匹配充分统计量的期望。例如，如果 $q(\mathbf{z})$ 是高斯分布 $\mathcal{N}(\mathbf{z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，那么令 $q(\mathbf{z})$ 的均值 $\boldsymbol{\mu}$ 等于分布 $p(\mathbf{z})$ 的均值，协方差 $\boldsymbol{\Sigma}$ 等于 $p(\mathbf{z})$ 的协方差，就能最小化 Kullback–Leibler 散度。这有时称为*矩匹配*（moment matching）。图 10.3(a) 已展示过一个例子。

现在利用这个结果，得到一种实用的近似推断算法。对于许多概率模型，数据 $\mathcal{D}$ 和隐藏变量（包括参数）$\boldsymbol{\theta}$ 的联合分布由若干因子的乘积组成，其形式为

$$
p(\mathcal{D},\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta}).
\tag{10.188}
$$

例如，在独立同分布数据的模型中，每个数据点 $\mathbf{x}_n$ 对应一个因子 $f_n(\boldsymbol{\theta})=p(\mathbf{x}_n\mid\boldsymbol{\theta})$，再加上与先验对应的因子 $f_0(\boldsymbol{\theta})=p(\boldsymbol{\theta})$，就会出现这种形式。更一般地，它也适用于任何由有向概率图定义的模型，其中每个因子是对应某个节点的条件分布；或者适用于无向图模型，其中每个因子是一个团势函数。我们希望计算后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$ 来进行预测，同时计算模型证据 $p(\mathcal{D})$ 来比较模型。由（10.188），后验分布为

$$
p(\boldsymbol{\theta}\mid\mathcal{D})=\frac{1}{p(\mathcal{D})}\prod_i f_i(\boldsymbol{\theta})
\tag{10.189}
$$

模型证据为

$$
p(\mathcal{D})=\int\prod_i f_i(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.190}
$$

这里考虑的是连续变量，不过，将积分换成求和后，以下讨论同样适用于离散变量。假设对 $\boldsymbol{\theta}$ 的边缘化，以及为了预测而需要对后验分布进行的边缘化，都难以求解，因此需要某种近似。

期望传播基于一个后验分布的近似，这个近似同样由因子的乘积给出：

$$
q(\boldsymbol{\theta})=\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.191}
$$

其中，近似中的每个因子 $\widetilde{f}_i(\boldsymbol{\theta})$ 都对应于真实后验（10.189）中的一个因子 $f_i(\boldsymbol{\theta})$，而因子 $1/Z$ 是归一化常数，用来保证（10.191）左侧积分为 $1$。为了得到实用的算法，需要以某种方式约束因子 $\widetilde{f}_i(\boldsymbol{\theta})$；具体而言，假设这些因子属于指数族。因此，因子的乘积也属于指数族，从而可以

<!-- pdf-page: 527 -->
<!-- join-previous-paragraph -->
用有限个充分统计量来描述。例如，如果每个 $\widetilde{f}_i(\boldsymbol{\theta})$ 都是高斯函数，那么整体近似 $q(\boldsymbol{\theta})$ 也将是高斯分布。

理想情况下，我们希望通过最小化真实后验与近似之间的 Kullback–Leibler 散度来确定 $\widetilde{f}_i(\boldsymbol{\theta})$，即

$$
\operatorname{KL}(p\|q)=\operatorname{KL}\left(\frac{1}{p(\mathcal{D})}\prod_i f_i(\boldsymbol{\theta})\,\middle\|\,\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta})\right).
\tag{10.192}
$$

注意，与变分推断所使用的 KL 散度相比，这里的方向相反。一般来说，这个最小化问题难以处理，因为 KL 散度涉及关于真实分布求平均。一种粗略近似，是改为最小化各对对应因子 $f_i(\boldsymbol{\theta})$ 和 $\widetilde{f}_i(\boldsymbol{\theta})$ 之间的 KL 散度。这个问题容易求解得多，而且算法不需要迭代。不过，由于每个因子都是单独近似的，因子乘积所得到的近似很可能很差。

期望传播在所有其他因子所给定的环境中，依次优化每个因子，因而得到好得多的近似。它先初始化因子 $\widetilde{f}_i(\boldsymbol{\theta})$，然后循环遍历这些因子，每次改进其中一个。这与前面变分贝叶斯框架中更新因子的思路相近。假设要改进因子 $\widetilde{f}_j(\boldsymbol{\theta})$。首先从乘积中移除这个因子，得到 $\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})$。从概念上说，现在要确定因子 $\widetilde{f}_j(\boldsymbol{\theta})$ 的新形式，使乘积

$$
q^{\mathrm{new}}(\boldsymbol{\theta})\propto\widetilde{f}_j(\boldsymbol{\theta})\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.193}
$$

尽可能接近

$$
f_j(\boldsymbol{\theta})\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.194}
$$

同时保持所有 $i\neq j$ 的因子 $\widetilde{f}_i(\boldsymbol{\theta})$ 不变。这样可以保证，在其余因子所确定的后验概率较高的区域中，近似最为精确。把 EP 应用于“杂波问题”时，将看到这一效果的例子（10.7.1 节）。为此，先定义未归一化分布，从当前后验近似中移除因子 $\widetilde{f}_j(\boldsymbol{\theta})$：

$$
q^{\backslash j}(\boldsymbol{\theta})=\frac{q(\boldsymbol{\theta})}{\widetilde{f}_j(\boldsymbol{\theta})}.
\tag{10.195}
$$

注意，也可以通过所有 $i\neq j$ 的因子乘积来求 $q^{\backslash j}(\boldsymbol{\theta})$，不过实践中做除法通常更容易。现在将它与因子 $f_j(\boldsymbol{\theta})$ 结合，得到分布

$$
\frac{1}{Z_j}f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})
\tag{10.196}
$$

<!-- pdf-page: 528 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-14.png" alt="左图比较真实分布及拉普拉斯、全局变分、期望传播的高斯近似，右图比较对应的负对数"><figcaption>图 10.14：对之前图 4.14 和图 10.1 中的例子，使用高斯分布进行期望传播近似。左图显示原分布（黄色）、拉普拉斯近似（红色）、全局变分近似（绿色）和 EP 近似（蓝色），右图显示这些分布相应的负对数。注意，由于 KL 散度形式不同，EP 分布比变分推断得到的分布更宽。</figcaption><p class="figure-translation">黄色：原分布；红色：拉普拉斯近似；绿色：全局变分近似；蓝色：期望传播近似。左图为分布，右图为负对数。</p></figure>

其中 $Z_j$ 是归一化常数，给定为

$$
Z_j=\int f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.197}
$$

现在通过最小化 Kullback–Leibler 散度来确定更新后的因子 $\widetilde{f}_j(\boldsymbol{\theta})$：

$$
\operatorname{KL}\left(\frac{f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})}{Z_j}\,\middle\|\,q^{\mathrm{new}}(\boldsymbol{\theta})\right).
\tag{10.198}
$$

这很容易求解，因为近似分布 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 属于指数族，所以可以利用结果（10.187）：将它的充分统计量的期望与（10.196）的对应矩匹配，就能得到 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的参数。这里假设这项操作是可处理的。例如，如果选择 $q(\boldsymbol{\theta})$ 为高斯分布 $\mathcal{N}(\boldsymbol{\theta}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，那么将 $\boldsymbol{\mu}$ 设为（未归一化）分布 $f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})$ 的均值，将 $\boldsymbol{\Sigma}$ 设为它的协方差。更一般地，只要能对指数族中的分布归一化，就很容易得到所需的期望，因为充分统计量的期望可以与归一化系数的导数联系起来，如（2.226）所示。图 10.14 展示了 EP 近似。

由（10.193）可以看到，将 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 除以其余因子，就能得到更新后的因子 $\widetilde{f}_j(\boldsymbol{\theta})$，即

$$
\widetilde{f}_j(\boldsymbol{\theta})=K\frac{q^{\mathrm{new}}(\boldsymbol{\theta})}{q^{\backslash j}(\boldsymbol{\theta})}
\tag{10.199}
$$

这里使用了（10.195）。为确定系数 $K$，将等式两边

<!-- pdf-page: 529 -->
<!-- join-previous-paragraph -->
乘以 $q^{\backslash i}(\boldsymbol{\theta})$，再对（10.199）积分，得到

$$
K=\int\widetilde{f}_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}
\tag{10.200}
$$

这里使用了 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 已归一化这一事实。因此，可以通过匹配零阶矩来确定 $K$ 的值：

$$
\int\widetilde{f}_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}=\int f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.201}
$$

将它与（10.197）结合，可知 $K=Z_j$，因此可以通过计算（10.197）中的积分来求出它。

实践中，会对因子集合遍历多轮，每次依次更新各个因子。随后用（10.191）近似后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$，并在（10.190）中将因子 $f_i(\boldsymbol{\theta})$ 替换为其近似 $\widetilde{f}_i(\boldsymbol{\theta})$，以近似模型证据 $p(\mathcal{D})$。

<aside class="procedure">
<h3>期望传播</h3>
<p>给定观测数据 $\mathcal{D}$ 和随机变量 $\boldsymbol{\theta}$ 的联合分布，它具有因子乘积的形式</p>
<p>$$
p(\mathcal{D},\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta})
\tag{10.202}
$$</p>
<p>我们希望用如下形式的分布近似后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$：</p>
<p>$$
q(\boldsymbol{\theta})=\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta}).
\tag{10.203}
$$</p>
<p>还希望近似模型证据 $p(\mathcal{D})$。</p>
<ol>
<li>初始化所有近似因子 $\widetilde{f}_i(\boldsymbol{\theta})$。</li>
<li>通过如下设置，初始化后验近似：</li>
</ol>
<p>$$
q(\boldsymbol{\theta})\propto\prod_i\widetilde{f}_i(\boldsymbol{\theta}).
\tag{10.204}
$$</p>
<ol start="3">
<li>反复执行以下操作，直到收敛：</li>
</ol>
<p>（a）选择一个因子 $\widetilde{f}_j(\boldsymbol{\theta})$ 进行改进。</p>
<p>（b）通过除法，从后验中移除 $\widetilde{f}_j(\boldsymbol{\theta})$：</p>
<p>$$
q^{\backslash j}(\boldsymbol{\theta})=\frac{q(\boldsymbol{\theta})}{\widetilde{f}_j(\boldsymbol{\theta})}.
\tag{10.205}
$$</p>
</aside>

<!-- pdf-page: 530 -->
<!-- join-previous-procedure -->

<aside class="procedure">
<p>（c）将 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的充分统计量（矩）设为与 $q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta})$ 的相同，从而计算新的后验；这包括计算归一化常数</p>
<p>$$
Z_j=\int q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.206}
$$</p>
<p>（d）计算并存储新的因子</p>
<p>$$
\widetilde{f}_j(\boldsymbol{\theta})=Z_j\frac{q^{\mathrm{new}}(\boldsymbol{\theta})}{q^{\backslash j}(\boldsymbol{\theta})}.
\tag{10.207}
$$</p>
<ol start="4">
<li>计算模型证据的近似：</li>
</ol>
<p>$$
p(\mathcal{D})\simeq\int\prod_i\widetilde{f}_i(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.208}
$$</p>
</aside>

EP 的一个特殊情形称为*假定密度滤波*（assumed density filtering，ADF），也称为*矩匹配*（Maybeck, 1982; Lauritzen, 1992; Boyen and Koller, 1998; Opper and Winther, 1999）。其做法是：除第一个因子外，将所有近似因子都初始化为 $1$，然后只遍历一轮因子，每个因子更新一次。假定密度滤波适用于在线学习：数据点依次到达，需要从每个数据点学习，然后在处理下一个点之前丢弃它。不过，在批量情形中，可以多次使用数据点来提高精度，期望传播正是利用了这一思路。此外，如果将 ADF 应用于批量数据，结果会依赖于处理数据点的（任意）顺序；这种依赖并不理想，而 EP 同样能够克服这一问题。

期望传播的一个缺点是，不能保证迭代收敛。不过，对于指数族中的近似 $q(\boldsymbol{\theta})$，如果迭代确实收敛，所得的解将是某个特定能量函数的驻点（Minka，2001a），尽管每次 EP 迭代不一定降低这个能量函数的值。这与变分贝叶斯不同：后者迭代地最大化对数边缘似然的一个下界，并保证每次迭代都不会减小这个下界。也可以直接优化 EP 的代价函数，这时能够保证收敛，不过所得算法可能较慢，而且实现更复杂。

变分贝叶斯与 EP 的另一个区别，来自这两种算法所最小化的 KL 散度形式：前者最小化 $\operatorname{KL}(q\|p)$，后者最小化 $\operatorname{KL}(p\|q)$。如图 10.3 所示，对于多峰分布 $p(\boldsymbol{\theta})$，最小化 $\operatorname{KL}(p\|q)$ 可能得到较差的近似。特别是，将 EP 应用于混合模型时，结果并不合理，因为近似试图涵盖后验分布的所有峰。相反，在 logistic 类型的模型中，EP 往往优于局部变分方法和拉普拉斯近似（Kuss and Rasmussen，2006）。

<!-- pdf-page: 531 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-15.png" alt="一维杂波问题，绿色目标高斯与红色背景高斯的混合生成由叉号表示的数据点"><figcaption>图 10.15：数据空间维数为 $D=1$ 时的杂波问题示例。叉号表示的训练数据点来自两个高斯分布的混合，两个分量分别用红色和绿色显示。目标是从观测数据推断绿色高斯分布的均值。</figcaption><p class="figure-translation">$x$：观测变量；$\theta$：绿色高斯分布的均值；红色曲线：背景杂波分布；绿色曲线：目标分布；叉号：训练数据点。</p></figure>

### 10.7.1 示例：杂波问题

按照 Minka（2001b），使用一个简单例子说明 EP 算法。给定从变量 $\mathbf{x}$ 的多元高斯分布中抽取的一组观测，目标是推断该分布的均值 $\boldsymbol{\theta}$。为使问题更有趣，观测混杂在背景杂波中，而背景杂波本身也服从高斯分布，如图 10.15 所示。因此，观测值 $\mathbf{x}$ 的分布是高斯混合，采用如下形式：

$$
p(\mathbf{x}\mid\boldsymbol{\theta})=(1-w)\mathcal{N}(\mathbf{x}\mid\boldsymbol{\theta},\mathbf{I})+w\mathcal{N}(\mathbf{x}\mid\mathbf{0},a\mathbf{I})
\tag{10.209}
$$

其中 $w$ 是背景杂波的比例，假设它已知。$\boldsymbol{\theta}$ 的先验取为高斯分布：

$$
p(\boldsymbol{\theta})=\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{0},b\mathbf{I})
\tag{10.210}
$$

Minka（2001a）选择的参数值为 $a=10$、$b=100$ 和 $w=0.5$。$N$ 个观测 $\mathcal{D}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 与 $\boldsymbol{\theta}$ 的联合分布为

$$
p(\mathcal{D},\boldsymbol{\theta})=p(\boldsymbol{\theta})\prod_{n=1}^{N}p(\mathbf{x}_n\mid\boldsymbol{\theta})
\tag{10.211}
$$

因此，后验分布由 $2^N$ 个高斯分布的混合组成。精确求解这个问题的计算成本会随数据集大小指数增长，所以当 $N$ 达到中等规模时，精确解就难以求得。

为了将 EP 应用于杂波问题，首先确定因子 $f_0(\boldsymbol{\theta})=p(\boldsymbol{\theta})$ 和 $f_n(\boldsymbol{\theta})=p(\mathbf{x}_n\mid\boldsymbol{\theta})$。接着从指数族中选择一个近似分布；在这个例子中，选用球形高斯分布较为方便：

$$
q(\boldsymbol{\theta})=\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{m},v\mathbf{I}).
\tag{10.212}
$$

<!-- pdf-page: 532 -->

因此，因子的近似将是如下形式的二次指数函数：

$$
\widetilde{f}_n(\boldsymbol{\theta})=s_n\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{m}_n,v_n\mathbf{I})
\tag{10.213}
$$

其中 $n=1,\ldots,N$，并令 $\widetilde{f}_0(\boldsymbol{\theta})$ 等于先验 $p(\boldsymbol{\theta})$。注意，使用 $\mathcal{N}(\boldsymbol{\theta}\mid\cdot,\cdot)$ 并不意味着右侧是一个合法的高斯密度（事实上，稍后会看到，方差参数 $v_n$ 可以为负），它只是一个方便的简写记号。对于 $n=1,\ldots,N$，可以将近似 $\widetilde{f}_n(\boldsymbol{\theta})$ 初始化为 $1$，对应于 $s_n=(2\pi v_n)^{D/2}$、$v_n\to\infty$ 和 $\mathbf{m}_n=\mathbf{0}$，其中 $D$ 是 $\mathbf{x}$ 的维数，也就是 $\boldsymbol{\theta}$ 的维数。因此，由（10.191）定义的初始 $q(\boldsymbol{\theta})$ 等于先验。

然后，每次选取一个因子 $f_n(\boldsymbol{\theta})$，应用（10.205）、（10.206）和（10.207），迭代地改进这些因子。注意，不需要更新项 $f_0(\boldsymbol{\theta})$，因为 EP 更新会使这一项保持不变（习题 10.37）。这里给出结果，具体细节留给读者完成。

首先，利用（10.205），通过除法从 $q(\boldsymbol{\theta})$ 中移除当前估计 $\widetilde{f}_n(\boldsymbol{\theta})$，得到 $q^{\backslash n}(\boldsymbol{\theta})$；其均值和逆方差为（习题 10.38）

$$
\mathbf{m}^{\backslash n}=\mathbf{m}+v^{\backslash n}v_n^{-1}(\mathbf{m}-\mathbf{m}_n)
\tag{10.214}
$$

$$
(v^{\backslash n})^{-1}=v^{-1}-v_n^{-1}.
\tag{10.215}
$$

接着，利用（10.206）计算归一化常数 $Z_n$，得到

$$
Z_n=(1-w)\mathcal{N}(\mathbf{x}_n\mid\mathbf{m}^{\backslash n},(v^{\backslash n}+1)\mathbf{I})+w\mathcal{N}(\mathbf{x}_n\mid\mathbf{0},a\mathbf{I}).
\tag{10.216}
$$

类似地，通过求 $q^{\backslash n}(\boldsymbol{\theta})f_n(\boldsymbol{\theta})$ 的均值和方差，来计算 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的均值和方差，得到（习题 10.39）

$$
\mathbf{m}=\mathbf{m}^{\backslash n}+\rho_n\frac{v^{\backslash n}}{v^{\backslash n}+1}(\mathbf{x}_n-\mathbf{m}^{\backslash n})
\tag{10.217}
$$

$$
v=v^{\backslash n}-\rho_n\frac{(v^{\backslash n})^2}{v^{\backslash n}+1}+\rho_n(1-\rho_n)\frac{(v^{\backslash n})^2\|\mathbf{x}_n-\mathbf{m}^{\backslash n}\|^2}{D(v^{\backslash n}+1)^2}
\tag{10.218}
$$

其中

$$
\rho_n=1-\frac{w}{Z_n}\mathcal{N}(\mathbf{x}_n\mid\mathbf{0},a\mathbf{I})
\tag{10.219}
$$

具有简单的解释：它是数据点 $\mathbf{x}_n$ 不属于杂波的概率。然后，利用（10.207）计算改进后的因子 $\widetilde{f}_n(\boldsymbol{\theta})$，其参数为

$$
v_n^{-1}=(v^{\mathrm{new}})^{-1}-(v^{\backslash n})^{-1}
\tag{10.220}
$$

$$
\mathbf{m}_n=\mathbf{m}^{\backslash n}+(v_n+v^{\backslash n})(v^{\backslash n})^{-1}(\mathbf{m}^{\mathrm{new}}-\mathbf{m}^{\backslash n})
\tag{10.221}
$$

$$
s_n=\frac{Z_n}{(2\pi v_n)^{D/2}\mathcal{N}(\mathbf{m}_n\mid\mathbf{m}^{\backslash n},(v_n+v^{\backslash n})\mathbf{I})}.
\tag{10.222}
$$

反复执行这个改进过程，直到满足适当的终止条件，例如，完整

<!-- pdf-page: 533 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-16.png" alt="一维杂波模型两个局部因子近似，蓝色为真实因子、红色为近似因子、绿色为移除该因子后的分布"><figcaption>图 10.16：一维杂波问题中特定因子的近似示例，其中 $f_n(\theta)$ 用蓝色显示，$\widetilde{f}_n(\theta)$ 用红色显示，$q^{\backslash n}(\theta)$ 用绿色显示。注意，$q^{\backslash n}(\theta)$ 的当前形式决定了 $\widetilde{f}_n(\theta)$ 能够很好地近似 $f_n(\theta)$ 的 $\theta$ 取值范围。</figcaption><p class="figure-translation">$\theta$：一维参数；蓝色：真实因子 $f_n(\theta)$；红色：近似因子 $\widetilde{f}_n(\theta)$；绿色：移除该近似因子后的 $q^{\backslash n}(\theta)$。</p></figure>

<!-- join-previous-paragraph-across-figures -->
遍历所有因子一轮后，参数值的最大变化小于某个阈值。最后，使用（10.208）计算模型证据的近似，得到

$$
p(\mathcal{D})\simeq(2\pi v^{\mathrm{new}})^{D/2}\exp(B/2)\prod_{n=1}^{N}\left\{s_n(2\pi v_n)^{-D/2}\right\}
\tag{10.223}
$$

其中

$$
B=\frac{(\mathbf{m}^{\mathrm{new}})^{\mathrm T}\mathbf{m}^{\mathrm{new}}}{v}-\sum_{n=1}^{N}\frac{\mathbf{m}_n^{\mathrm T}\mathbf{m}_n}{v_n}.
\tag{10.224}
$$

图 10.16 给出了一维参数空间 $\theta$ 下杂波问题的因子近似示例。注意，近似因子的“方差”参数 $v_n$ 可以取无穷大，甚至取负值。这只意味着近似曲线向上弯而不是向下弯；只要整体近似后验 $q(\boldsymbol{\theta})$ 具有正方差，就不一定有问题。图 10.17 比较了 EP、变分贝叶斯（平均场理论）和拉普拉斯近似在杂波问题上的表现。

### 10.7.2 图上的期望传播

在此前对 EP 的一般讨论中，我们允许分布 $p(\boldsymbol{\theta})$ 中的因子 $f_i(\boldsymbol{\theta})$ 依赖于 $\boldsymbol{\theta}$ 的所有分量，近似分布 $q(\boldsymbol{\theta})$ 中的近似因子 $\widetilde{f}(\boldsymbol{\theta})$ 也一样。现在考虑因子只依赖于变量子集的情况。这种限制可以方便地用第 8 章讨论的概率图模型框架表示。这里使用因子图表示，因为它同时涵盖有向图和无向图。

<!-- pdf-page: 534 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-17.png" alt="杂波问题中三种近似算法的误差与浮点运算次数比较，左图为后验均值，右图为模型证据"><figcaption>图 10.17：期望传播、变分推断和拉普拉斯近似在杂波问题上的比较。左图显示预测后验均值的误差与浮点运算次数的关系，右图显示模型证据的相应结果。</figcaption><p class="figure-translation">Posterior mean → 后验均值；Evidence → 模型证据；Error → 误差；FLOPS → 浮点运算次数；laplace → 拉普拉斯近似（蓝色）；vb → 变分贝叶斯（红色）；ep → 期望传播（绿色）。</p></figure>

我们将着重讨论近似分布完全因子化的情况，并证明，此时期望传播会化为有环信念传播（Minka，2001a）。先通过一个简单例子说明这一点，再研究一般情形。

首先，回顾（10.17）：如果关于因子化分布 $q$ 最小化 Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$，那么每个因子的最优解就是 $p$ 的对应边缘分布。

现在考虑图 10.18 左侧的因子图，它在前面讨论和积算法时已经出现过（8.4.4 节）。联合分布为

$$
p(\mathbf{x})=f_a(x_1,x_2)f_b(x_2,x_3)f_c(x_2,x_4).
\tag{10.225}
$$

我们寻找具有相同因子分解的近似 $q(\mathbf{x})$，即

$$
q(\mathbf{x})\propto\widetilde{f}_a(x_1,x_2)\widetilde{f}_b(x_2,x_3)\widetilde{f}_c(x_2,x_4).
\tag{10.226}
$$

注意，这里省略了归一化常数；可以在最后通过局部归一化重新加入这些常数，这也是信念传播通常的做法。现在进一步限制近似形式，令因子本身也按各个变量分解，使得

$$
q(\mathbf{x})\propto\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)
\tag{10.227}
$$

这对应于图 10.18 右侧的因子图。由于各个因子都已分解，整体分布 $q(\mathbf{x})$ 本身也完全因子化。

现在使用这个完全因子化的近似来应用 EP 算法。假设已经初始化了所有因子，并选择改进因子

<!-- pdf-page: 535 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-18.png" alt="左侧为四变量三因子的原始因子图，右侧为各因子进一步分解后的完全因子化近似"><figcaption>图 10.18：左侧是图 8.51 中的一个简单因子图，为方便起见在此再次给出。右侧是相应的因子化近似。</figcaption><p class="figure-translation">$x_1$、$x_2$、$x_3$、$x_4$：变量节点；$f_a$、$f_b$、$f_c$：原因子；$\widetilde{f}_{a1}$、$\widetilde{f}_{a2}$、$\widetilde{f}_{b2}$、$\widetilde{f}_{b3}$、$\widetilde{f}_{c2}$、$\widetilde{f}_{c4}$：按单个变量分解后的近似因子。圆圈表示变量，方块表示因子。</p></figure>

<!-- join-previous-paragraph-across-figures -->
$\widetilde{f}_b(x_2,x_3)=\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)$。首先从近似分布中移除这个因子，得到

$$
q^{\backslash b}(\mathbf{x})=\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)
\tag{10.228}
$$

然后乘以精确因子 $f_b(x_2,x_3)$，得到

$$
\widehat{p}(\mathbf{x})=q^{\backslash b}(\mathbf{x})f_b(x_2,x_3)=\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)f_b(x_2,x_3).
\tag{10.229}
$$

现在通过最小化 Kullback–Leibler 散度 $\operatorname{KL}(\widehat{p}\|q^{\mathrm{new}})$ 来求 $q^{\mathrm{new}}(\mathbf{x})$。如前所述，结果是 $q^{\mathrm{new}}(\mathbf{z})$ 由因子的乘积组成，每个变量 $x_i$ 对应一个因子，并且每个因子由 $\widehat{p}(\mathbf{x})$ 的相应边缘分布给出。这四个边缘分布为

$$
\widehat{p}(x_1)\propto\widetilde{f}_{a1}(x_1)
\tag{10.230}
$$

$$
\widehat{p}(x_2)\propto\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\sum_{x_3}f_b(x_2,x_3)
\tag{10.231}
$$

$$
\widehat{p}(x_3)\propto\sum_{x_2}\left\{f_b(x_2,x_3)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\right\}
\tag{10.232}
$$

$$
\widehat{p}(x_4)\propto\widetilde{f}_{c4}(x_4)
\tag{10.233}
$$

将这些边缘分布相乘，就得到 $q^{\mathrm{new}}(\mathbf{x})$。可以看到，当更新 $\widetilde{f}_b(x_2,x_3)$ 时，$q(\mathbf{x})$ 中只有涉及 $f_b$ 中变量的因子会发生变化，也就是涉及 $x_2$ 和 $x_3$ 的因子。要得到改进后的因子 $\widetilde{f}_b(x_2,x_3)=\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)$，只需将 $q^{\mathrm{new}}(\mathbf{x})$ 除以 $q^{\backslash b}(\mathbf{x})$，得到

$$
\widetilde{f}_{b2}(x_2)\propto\sum_{x_3}f_b(x_2,x_3)
\tag{10.234}
$$

$$
\widetilde{f}_{b3}(x_3)\propto\sum_{x_2}\left\{f_b(x_2,x_3)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\right\}.
\tag{10.235}
$$

<!-- pdf-page: 536 -->

这些正是信念传播得到的消息，其中从变量节点到因子节点的消息已经并入从因子节点到变量节点的消息（8.4.4 节）。具体来说，$\widetilde{f}_{b2}(x_2)$ 对应于因子节点 $f_b$ 发送给变量节点 $x_2$ 的消息 $\mu_{f_b\to x_2}(x_2)$，由（8.81）给出。类似地，将（8.78）代入（8.79），就得到（10.235）；其中 $\widetilde{f}_{a2}(x_2)$ 对应于 $\mu_{f_a\to x_2}(x_2)$，$\widetilde{f}_{c2}(x_2)$ 对应于 $\mu_{f_c\to x_2}(x_2)$，由此得到的消息 $\widetilde{f}_{b3}(x_3)$ 对应于 $\mu_{f_b\to x_3}(x_3)$。

这个结果与标准信念传播略有不同，因为消息同时沿两个方向传递。只需每次更新一个因子，就能很容易地把 EP 过程改为标准形式的和积算法。例如，如果只改进 $\widetilde{f}_{b3}(x_3)$，那么按定义，$\widetilde{f}_{b2}(x_2)$ 保持不变，而 $\widetilde{f}_{b3}(x_3)$ 的改进形式仍由（10.235）给出。如果每次只改进一项，就可以按需要选择改进顺序。特别是，对于树结构图，可以采用与标准信念传播调度相对应的两轮更新方案，从而对变量边缘和因子边缘进行精确推断。在这种情况下，近似因子的初始化并不重要。

现在考虑与如下分布对应的一般因子图：

$$
p(\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta}_i)
\tag{10.236}
$$

其中 $\boldsymbol{\theta}_i$ 表示与因子 $f_i$ 关联的变量子集。使用如下形式的完全因子化分布来近似它：

$$
q(\boldsymbol{\theta})\propto\prod_i\prod_k\widetilde{f}_{ik}(\theta_k)
\tag{10.237}
$$

其中 $\theta_k$ 对应于单个变量节点。假设希望改进某一项 $\widetilde{f}_{jl}(\theta_l)$，同时保持所有其他项不变。首先从 $q(\boldsymbol{\theta})$ 中移除项 $\widetilde{f}_j(\boldsymbol{\theta}_j)$，得到

$$
q^{\backslash j}(\boldsymbol{\theta})\propto\prod_{i\neq j}\prod_k\widetilde{f}_{ik}(\theta_k)
\tag{10.238}
$$

然后乘以精确因子 $f_j(\boldsymbol{\theta}_j)$。为确定改进后的项 $\widetilde{f}_{jl}(\theta_l)$，只需考虑对 $\theta_l$ 的函数依赖，因此只需找出下式相应的边缘分布：

$$
q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta}_j).
\tag{10.239}
$$

忽略一个乘法常数，这意味着先将 $f_j(\boldsymbol{\theta}_j)$ 与 $q^{\backslash j}(\boldsymbol{\theta})$ 中所有依赖于 $\boldsymbol{\theta}_j$ 内任意变量的项相乘，再取边缘分布。随后除以 $q^{\backslash j}(\boldsymbol{\theta})$ 时，对应于其他因子 $\widetilde{f}_i(\boldsymbol{\theta}_i)$（$i\neq j$）的项会在分子和分母之间消去。因此得到

$$
\widetilde{f}_{jl}(\theta_l)\propto\sum_{\theta_{m\neq l}\in\boldsymbol{\theta}_j}f_j(\boldsymbol{\theta}_j)\prod_k\prod_{m\neq l}\widetilde{f}_{km}(\theta_m).
\tag{10.240}
$$

<!-- pdf-page: 537 -->

可以看出，这就是消去了变量节点到因子节点消息之后的和积规则，图 8.50 中的例子展示了这种形式。$\widetilde{f}_{jm}(\theta_m)$ 对应于因子节点 $j$ 发送给变量节点 $m$ 的消息 $\mu_{f_j\to\theta_m}(\theta_m)$；（10.240）中关于 $k$ 的乘积，遍历所有依赖于变量 $\theta_m$、且与因子 $f_j(\boldsymbol{\theta}_j)$ 具有共同变量（变量 $\theta_l$ 除外）的因子。换言之，要计算一个因子节点的输出消息，先将来自其他因子节点的全部输入消息相乘，再乘以局部因子，最后进行边缘化。

因此，使用完全因子化的近似分布时，和积算法就是期望传播的一个特殊情形。这表明，可以用对应于部分断开连接图的、更灵活的近似分布来提高精度。另一种推广方式，是将因子 $f_i(\boldsymbol{\theta}_i)$ 分组为若干集合，在每次迭代中同时改进一个集合内的全部因子。这两种方法都可能提高精度（Minka，2001b）。一般而言，如何选择最佳的分组与断开连接组合，仍是一个开放的研究问题。

我们已经看到，变分消息传递和期望传播优化的是两种不同形式的 Kullback–Leibler 散度。Minka（2005）证明，许多消息传递算法都可以从一个共同框架中推导出来，即最小化（10.19）给出的 alpha 散度族中的某个散度。其中包括变分消息传递、有环信念传播和期望传播，也包括这里没有篇幅讨论的其他一系列算法，例如*树重加权消息传递*（tree-reweighted message passing）（Wainwright et al.，2005）、*分数信念传播*（fractional belief propagation）（Wiegerinck and Heskes，2003）和*幂 EP*（power EP）（Minka，2004）。

## 习题

**10.1（⋆）www** 验证：观测数据的对数边缘分布 $\ln p(\mathbf{X})$ 可以分解为（10.2）形式的两项，其中 $\mathcal{L}(q)$ 由（10.3）给出，$\operatorname{KL}(q\|p)$ 由（10.4）给出。

**10.2（⋆）** 利用性质 $\mathbb{E}[z_1]=m_1$ 和 $\mathbb{E}[z_2]=m_2$，求解联立方程（10.13）和（10.15），由此证明：只要原分布 $p(\mathbf{z})$ 非奇异，近似分布中各因子均值的唯一解就是 $\mathbb{E}[z_1]=\mu_1$ 和 $\mathbb{E}[z_2]=\mu_2$。

**10.3（⋆⋆）www** 考虑（10.5）形式的因子化变分分布 $q(\mathbf{Z})$。利用拉格朗日乘子法，验证：保持其他所有因子不变，关于某个因子 $q_i(\mathbf{Z}_i)$ 最小化 Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$，会得到解（10.17）。

**10.4（⋆⋆）** 假设 $p(\mathbf{x})$ 是某个固定分布，希望使用高斯分布 $q(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 来近似它。写出 $q(\mathbf{x})$ 为高斯分布时 KL 散度 $\operatorname{KL}(p\|q)$ 的形式，再通过求导，证明

<!-- pdf-page: 538 -->
<!-- join-previous-paragraph -->
关于 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 最小化 $\operatorname{KL}(p\|q)$，会使 $\boldsymbol{\mu}$ 等于 $\mathbf{x}$ 在 $p(\mathbf{x})$ 下的期望，$\boldsymbol{\Sigma}$ 等于其协方差。

**10.5（⋆⋆）www** 考虑一个模型，其中全部隐藏随机变量的集合统记为 $\mathbf{Z}$，它由一些潜变量 $\mathbf{z}$ 和一些模型参数 $\boldsymbol{\theta}$ 组成。假设使用一个在潜变量与参数之间因子化的变分分布，即 $q(\mathbf{z},\boldsymbol{\theta})=q_{\mathbf{z}}(\mathbf{z})q_{\boldsymbol{\theta}}(\boldsymbol{\theta})$，其中分布 $q_{\boldsymbol{\theta}}(\boldsymbol{\theta})$ 用点估计近似，其形式为 $q_{\boldsymbol{\theta}}(\boldsymbol{\theta})=\delta(\boldsymbol{\theta}-\boldsymbol{\theta}_0)$，$\boldsymbol{\theta}_0$ 是自由参数向量。证明，对这个因子化分布进行变分优化，等价于一个 EM 算法：E 步优化 $q_{\mathbf{z}}(\mathbf{z})$，M 步则关于 $\boldsymbol{\theta}_0$，最大化 $\boldsymbol{\theta}$ 的完整数据对数后验分布的期望。

**10.6（⋆⋆）** alpha 散度族由（10.19）定义。证明，Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$ 对应于 $\alpha\to1$。可以通过写出 $p^{\epsilon}=\exp(\epsilon\ln p)=1+\epsilon\ln p+O(\epsilon^2)$，再取 $\epsilon\to0$ 来完成。类似地，证明 $\operatorname{KL}(q\|p)$ 对应于 $\alpha\to-1$。

**10.7（⋆⋆）** 考虑 10.1.3 节研究的问题：用因子化变分近似推断一元高斯分布的均值和精度。证明，因子 $q_{\mu}(\mu)$ 是 $\mathcal{N}(\mu\mid\mu_N,\lambda_N^{-1})$ 形式的高斯分布，其均值和精度分别由（10.26）和（10.27）给出。类似地，证明因子 $q_{\tau}(\tau)$ 是 $\operatorname{Gam}(\tau\mid a_N,b_N)$ 形式的伽马分布，其参数由（10.29）和（10.30）给出。

**10.8（⋆）** 考虑一元高斯分布精度的变分后验分布，其参数由（10.29）和（10.30）给出。利用（B.27）和（B.28）给出的伽马分布均值与方差的标准结果，证明：当 $N\to\infty$ 时，这个变分后验分布的均值等于数据方差的最大似然估计量的倒数，而其方差趋于零。

**10.9（⋆⋆）** 利用伽马分布均值的标准结果 $\mathbb{E}[\tau]=a_N/b_N$，结合（10.26）、（10.27）、（10.29）和（10.30），推导一元高斯分布的因子化变分处理中精度期望值的倒数结果（10.33）。

**10.10（⋆）www** 推导（10.34）给出的分解，它用于通过变分推断求模型的近似后验分布。

**10.11（⋆⋆）www** 使用拉格朗日乘子对分布 $q(m)$ 施加归一化约束，证明下界（10.35）的最大值由（10.36）给出。

**10.12（⋆⋆）** 从联合分布（10.41）出发，应用一般结果（10.9），验证正文中的各个步骤，证明贝叶斯高斯混合模型中潜变量的最优变分分布 $q^{\star}(\mathbf{Z})$ 由（10.48）给出。

<!-- pdf-page: 539 -->

**10.13（⋆⋆）www** 从（10.54）出发，推导贝叶斯高斯混合模型中 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Lambda}_k$ 的最优变分后验分布结果（10.59），由此验证（10.60）—（10.63）给出的这个分布的参数表达式。

**10.14（⋆⋆）** 使用分布（10.59），验证结果（10.64）。

**10.15（⋆）** 使用结果（B.17），证明变分高斯混合模型中混合系数的期望值由（10.69）给出。

**10.16（⋆⋆）www** 对于（10.70）给出的变分高斯混合模型下界，验证其前两项的结果（10.71）和（10.72）。

**10.17（⋆⋆⋆）** 对于（10.70）给出的变分高斯混合模型下界，验证其余各项的结果（10.73）—（10.77）。

**10.18（⋆⋆⋆）** 本题通过直接对下界求导，推导高斯混合模型的变分重估方程。为此，假设变分分布具有（10.42）和（10.55）定义的因子分解，其中各因子由（10.48）、（10.57）和（10.59）给出。将它们代入（10.70），得到下界作为变分分布参数的函数。然后，关于这些参数最大化下界，推导变分分布各因子的重估方程，并证明它们与 10.2.1 节得到的方程相同。

**10.19（⋆⋆）** 推导贝叶斯高斯混合模型的变分处理中预测分布的结果（10.81）。

**10.20（⋆⋆）www** 本题研究数据集大小 $N$ 很大时高斯混合模型的变分贝叶斯解，并证明它会化为第 9 章基于 EM 推导的最大似然解，这与我们的预期一致。注意，可以借助附录 B 的结果来解答本题。首先证明，精度的后验分布 $q^{\star}(\boldsymbol{\Lambda}_k)$ 会在最大似然解附近形成尖锐的峰。对均值的后验分布 $q^{\star}(\boldsymbol{\mu}_k\mid\boldsymbol{\Lambda}_k)$ 证明同样的结论。接着考虑混合系数的后验分布 $q^{\star}(\boldsymbol{\pi})$，证明它也会在最大似然解附近形成尖锐的峰。类似地，利用 digamma 函数在 $x$ 很大时的如下渐近结果，证明当 $N$ 很大时，责任度等于相应的最大似然值：

$$
\psi(x)=\ln x+O(1/x).
\tag{10.241}
$$

最后，利用（10.80），证明当 $N$ 很大时，预测分布变为高斯混合。

**10.21（⋆）** 证明：具有 $K$ 个分量的混合模型中，由交换对称性产生的等价参数配置共有 $K!$ 种。

<!-- pdf-page: 540 -->

**10.22（⋆⋆）** 我们已经看到，高斯混合模型后验分布的每一个峰，都属于由 $K!$ 个等价峰构成的一族。假设运行变分推断算法得到的近似后验分布 $q$ 集中在其中一个峰的邻域。于是，可以用 $K!$ 个这样的 $q$ 分布的混合来近似完整后验分布，每个峰上各放一个，并取相等的混合系数。证明：若假设这个 $q$ 混合的各分量之间的重叠可忽略不计，那么所得下界与单个分量 $q$ 分布对应的下界相比，多出一项 $\ln K!$。

**10.23（⋆⋆）www** 考虑一个变分高斯混合模型，其中没有为混合系数 $\{\pi_k\}$ 设置先验分布，而是将混合系数视为参数，通过最大化对数边缘似然的变分下界来确定其值。证明：关于混合系数最大化这个下界，并使用拉格朗日乘子施加混合系数之和为 $1$ 的约束，会得到重估结果（10.83）。注意，不必考虑下界的所有项，只需考虑下界对 $\{\pi_k\}$ 的依赖。

**10.24（⋆⋆）www** 在 10.2 节中已经看到，对高斯混合模型进行最大似然处理时出现的奇异性，在贝叶斯处理中不会出现。讨论：如果使用最大后验（MAP）估计来求解贝叶斯模型，是否还会出现这种奇异性？

**10.25（⋆⋆）** 10.2 节讨论的贝叶斯高斯混合模型的变分处理，对后验分布采用了因子化近似（10.5）。如图 10.2 所示，因子化假设会导致参数空间中某些方向上的后验分布方差被低估。定性讨论这对模型证据的变分近似有什么影响，以及这种影响如何随混合分量数变化。由此说明，变分高斯混合模型倾向于低估还是高估最优分量数。

**10.26（⋆⋆⋆）** 扩展贝叶斯线性回归的变分处理，为 $\beta$ 加入伽马超先验 $\operatorname{Gam}(\beta\mid c_0,d_0)$，并假设变分分布具有 $q(\mathbf{w})q(\alpha)q(\beta)$ 的因子化形式，以变分方法求解。推导变分分布中三个因子的变分更新方程，并求出下界和预测分布的表达式。

**10.27（⋆⋆）** 利用附录 B 给出的公式，证明：（10.107）定义的线性基函数回归模型的变分下界可以写成（10.107）的形式，其中各项由（10.108）—（10.112）定义。

**10.28（⋆⋆⋆）** 将 10.2 节介绍的贝叶斯高斯混合模型，改写成 10.4 节讨论的指数族共轭模型。然后利用一般结果（10.115）和（10.119），推导具体结果（10.48）、（10.57）和（10.59）。

<!-- pdf-page: 541 -->

**10.29（⋆）www** 通过计算二阶导数，证明函数 $f(x)=\ln(x)$ 在 $0<x<\infty$ 上是凹函数。确定（10.133）定义的对偶函数 $g(\lambda)$ 的形式，并验证：根据（10.132），关于 $\lambda$ 最小化 $\lambda x-g(\lambda)$，确实能恢复函数 $\ln(x)$。

**10.30（⋆）** 通过求二阶导数，证明对数 logistic 函数 $f(x)=-\ln(1+e^{-x})$ 是凹函数。对这个对数 logistic 函数在点 $x=\xi$ 附近作二阶泰勒展开，直接推导变分上界（10.137）。

**10.31（⋆⋆）** 通过求关于 $x$ 的二阶导数，证明函数 $f(x)=-\ln(e^{x/2}+e^{-x/2})$ 是 $x$ 的凹函数。再考虑关于变量 $x^2$ 的二阶导数，由此证明它是 $x^2$ 的凸函数。分别画出 $f(x)$ 关于 $x$ 和关于 $x^2$ 的图像。把 $f(x)$ 视为变量 $x^2$ 的函数，在 $\xi^2$ 处作一阶泰勒级数展开，直接推导 logistic sigmoid 函数的下界（10.144）。

**10.32（⋆⋆）www** 考虑序贯学习中的逻辑回归变分处理：数据点逐个到达，每个数据点都必须在下一个数据点到达之前处理完毕并丢弃。证明，利用下界（10.151），可以维护一个后验分布的高斯近似；该分布用先验初始化，每吸收一个数据点，就优化其对应的变分参数 $\xi_n$。

**10.33（⋆）** 对（10.161）定义的量 $\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})$ 关于变分参数 $\xi_n$ 求导，证明贝叶斯逻辑回归模型中 $\xi_n$ 的更新方程由（10.163）给出。

**10.34（⋆⋆）** 本题通过直接最大化（10.164）给出的下界，推导 4.5 节贝叶斯逻辑回归模型中变分参数 $\boldsymbol{\xi}$ 的重估方程。为此，令 $\mathcal{L}(\boldsymbol{\xi})$ 关于 $\xi_n$ 的导数等于零，并利用行列式对数求导的结果（3.117），以及定义变分后验分布 $q(\mathbf{w})$ 的均值和协方差的表达式（10.157）和（10.158）。

**10.35（⋆⋆）** 推导变分逻辑回归模型中下界 $\mathcal{L}(\boldsymbol{\xi})$ 的结果（10.164）。最简单的做法，是把高斯先验 $q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\mathbf{S}_0)$ 的表达式，以及似然函数的下界 $h(\mathbf{w},\boldsymbol{\xi})$，代入定义 $\mathcal{L}(\boldsymbol{\xi})$ 的积分（10.159）。然后，将指数中依赖于 $\mathbf{w}$ 的项归并并配方，得到高斯积分，再利用多元高斯分布归一化系数的标准结果来计算它。最后取对数，得到（10.164）。

**10.36（⋆⋆）** 考虑 10.7 节讨论的 ADF 近似方案，证明加入因子 $f_j(\boldsymbol{\theta})$ 后，模型证据会按如下形式更新：

$$
p_j(\mathcal{D})\simeq p_{j-1}(\mathcal{D})Z_j
\tag{10.242}
$$

<!-- pdf-page: 542 -->

其中 $Z_j$ 是（10.197）定义的归一化常数。递归应用这个结果，并以 $p_0(\mathcal{D})=1$ 初始化，推导

$$
p(\mathcal{D})\simeq\prod_j Z_j.
\tag{10.243}
$$

**10.37（⋆）www** 考虑 10.7 节的期望传播算法，假设定义（10.188）中的一个因子 $f_0(\boldsymbol{\theta})$，与近似分布 $q(\boldsymbol{\theta})$ 具有相同的指数族函数形式。证明：若将因子 $\widetilde{f}_0(\boldsymbol{\theta})$ 初始化为 $f_0(\boldsymbol{\theta})$，那么用于改进 $\widetilde{f}_0(\boldsymbol{\theta})$ 的 EP 更新会使 $\widetilde{f}_0(\boldsymbol{\theta})$ 保持不变。这通常出现在某个因子为先验 $p(\boldsymbol{\theta})$ 的情况下，因此可知，先验因子可以一次性精确地并入，无需再改进。

**10.38（⋆⋆⋆）** 本题和下一题将验证期望传播算法应用于杂波问题时的结果（10.214）—（10.224）。先使用除法公式（10.205），在指数中配方以识别均值和方差，从而推导表达式（10.214）和（10.215）。另外，证明（10.206）定义的归一化常数 $Z_n$ 在杂波问题中由（10.216）给出。可以利用一般结果（2.115）完成证明。

**10.39（⋆⋆⋆）** 证明：EP 应用于杂波问题时，$q^{\mathrm{new}}(\boldsymbol{\theta})$ 的均值和方差由（10.217）和（10.218）给出。为此，先证明 $\boldsymbol{\theta}$ 和 $\boldsymbol{\theta}\boldsymbol{\theta}^{\mathrm T}$ 在 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 下的期望满足如下结果：

$$
\mathbb{E}[\boldsymbol{\theta}]=\mathbf{m}^{\backslash n}+v^{\backslash n}\nabla_{\mathbf{m}^{\backslash n}}\ln Z_n
\tag{10.244}
$$

$$
\mathbb{E}[\boldsymbol{\theta}^{\mathrm T}\boldsymbol{\theta}]=2(v^{\backslash n})^2\nabla_{v^{\backslash n}}\ln Z_n+2\mathbb{E}[\boldsymbol{\theta}]^{\mathrm T}\mathbf{m}^{\backslash n}-\|\mathbf{m}^{\backslash n}\|^2
\tag{10.245}
$$

然后利用 $Z_n$ 的结果（10.216）。接着，使用（10.207）并在指数中配方，证明结果（10.220）—（10.222）。最后，使用（10.208）推导结果（10.223）。
