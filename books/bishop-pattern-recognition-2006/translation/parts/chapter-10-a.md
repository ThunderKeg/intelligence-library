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
