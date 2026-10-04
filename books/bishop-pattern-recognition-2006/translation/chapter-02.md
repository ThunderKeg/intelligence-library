# 第 2 章 概率分布

<aside class="chapter-guide"><strong>本章导读</strong><p>本章介绍离散变量和连续变量的常用概率分布，并通过简单模型说明如何从数据估计参数、如何用先验和观测数据形成后验分布。重点包括共轭先验、高斯分布及其条件与边缘分布，随后讨论指数族和非参数密度估计，为后续模型提供基础。</p></aside>

<!-- pdf-page: 87 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-chapter-opening.png" alt="第 2 章章首装饰图：水面反光纹理"><p class="figure-translation">Probability Distributions → 概率分布。</p></figure>

第 1 章强调了概率论在解决模式识别问题时所起的核心作用。现在，我们来研究一些具体的概率分布及其性质。这些分布本身就很有研究价值，同时也可以作为构造更复杂模型的组成部分，在本书中会得到广泛使用。本章介绍的分布还有一个重要用途：让我们先在简单模型中讨论贝叶斯推断等一些关键的统计概念，再在后续章节中将它们用于更复杂的情形。

本章讨论的分布的一项用途，是在给定有限个观测 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 的情况下，对随机变量 $\mathbf{x}$ 的概率分布 $p(\mathbf{x})$ 建模。这个问题称为密度估计（density estimation）。在本章中，假设各数据点独立同分布。需要强调，密度估计问题从根本上说是

<!-- pdf-page: 88 -->
<!-- join-previous-paragraph -->
不适定的（ill-posed），因为有无穷多个概率分布，都可能生成所观测到的有限数据集。事实上，只要一个分布 $p(\mathbf{x})$ 在每个数据点 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 处都不为零，它就可能是候选分布。如何选择合适的分布，与模型选择问题有关；第 1 章讨论多项式曲线拟合时已经遇到这个问题，它也是模式识别的核心问题之一。

我们首先考虑离散随机变量的二项分布和多项分布，以及连续随机变量的高斯分布。这些都是参数分布（parametric distribution）的具体例子；之所以这样称呼，是因为它们由少量可调参数决定，例如高斯分布的均值和方差。要用这些模型解决密度估计问题，就需要一种方法，在给定观测数据集后确定合适的参数值。在频率学派的处理中，我们通过优化似然函数等某种准则，为参数选择具体数值。相比之下，在贝叶斯处理中，我们为参数引入先验分布，再利用贝叶斯定理，根据观测数据计算相应的后验分布。

后面会看到，共轭先验（conjugate prior）起着重要作用：它使后验分布与先验具有相同的函数形式，因此能够大幅简化贝叶斯分析。例如，多项分布参数的共轭先验称为狄利克雷分布（Dirichlet distribution）；高斯分布均值的共轭先验，则是另一个高斯分布。这些分布都属于指数族（exponential family）。指数族具有许多重要性质，我们将作较详细的讨论。

参数方法的一个局限，是预先假设了分布的具体函数形式，而这种形式可能并不适合某项应用。另一种选择是非参数（nonparametric）密度估计方法，其中分布的形式通常取决于数据集的大小。这类模型仍然包含参数，不过这些参数控制的是模型复杂度，而不是分布的形式。本章最后将讨论三种非参数方法，分别基于直方图、最近邻和核。

## 2.1 二元变量

首先考虑单个二元随机变量 $x\in\{0,1\}$。例如，$x$ 可以描述抛硬币的结果，$x=1$ 表示“正面”，$x=0$ 表示“反面”。可以设想这是一枚受损的硬币，因此正面朝上的概率不一定等于反面朝上的概率。用参数 $\mu$ 表示 $x=1$ 的概率，即

$$
p(x=1\mid\mu)=\mu.
\tag{2.1}
$$

<!-- pdf-page: 89 -->

其中 $0\leqslant\mu\leqslant1$，由此有 $p(x=0\mid\mu)=1-\mu$。因此，$x$ 的概率分布可以写成

$$
\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}.
\tag{2.2}
$$

这称为伯努利分布（Bernoulli distribution）。很容易验证，这个分布是归一化的，其均值和方差分别为 <span class="margin-reference">习题 2.1</span>

$$
\mathbb{E}[x]=\mu,
\tag{2.3}
$$

$$
\operatorname{var}[x]=\mu(1-\mu).
\tag{2.4}
$$

现在假设有一个由 $x$ 的观测值组成的数据集 $\mathcal{D}=\{x_1,\ldots,x_N\}$。若假设各观测独立地取自 $p(x\mid\mu)$，就可以构造以 $\mu$ 为自变量的似然函数：

$$
p(\mathcal{D}\mid\mu)=\prod_{n=1}^{N}p(x_n\mid\mu)=\prod_{n=1}^{N}\mu^{x_n}(1-\mu)^{1-x_n}.
\tag{2.5}
$$

在频率学派框架中，可以通过最大化似然函数，或者等价地最大化似然的对数，估计 $\mu$ 的值。对于伯努利分布，对数似然函数为

$$
\ln p(\mathcal{D}\mid\mu)=\sum_{n=1}^{N}\ln p(x_n\mid\mu)=\sum_{n=1}^{N}\{x_n\ln\mu+(1-x_n)\ln(1-\mu)\}.
\tag{2.6}
$$

这里应当注意，对数似然函数只通过 $N$ 个观测 $x_n$ 的和 $\sum_n x_n$ 依赖于这些观测。在这个分布下，该和是数据的充分统计量（sufficient statistic）的一个例子；后面将较详细地讨论充分统计量的重要作用。<span class="margin-reference">第 2.4 节</span> 令 $\ln p(\mathcal{D}\mid\mu)$ 对 $\mu$ 的导数等于零，得到最大似然估计量

$$
\mu_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}x_n.
\tag{2.7}
$$

<aside class="biography"><p><strong>雅各布·伯努利（Jacob Bernoulli）</strong><br>1654–1705</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-jacob-bernoulli.png" alt="雅各布·伯努利肖像"><p>雅各布·伯努利也称 Jacques Bernoulli 或 James Bernoulli，是瑞士数学家，也是伯努利家族中众多投身科学与数学者的第一人。虽然父母违背他的意愿，强迫他学习哲学和神学，但毕业后他广泛游历，拜访当时许多杰出的科学家，其中包括英国的玻意耳和胡克。回到瑞士后，他教授力学，并于 1687 年成为巴塞尔的数学教授。不幸的是，雅各布与弟弟约翰之间的竞争，把最初成果丰硕的合作变成了激烈的公开争执。雅各布对数学最重要的贡献见于《猜度术》（The Art of Conjecture）；该书于 1713 年，也就是他去世八年后出版，讨论了概率论中的一些主题，其中包括后来被称为伯努利分布的内容。</p></aside>

<!-- pdf-page: 90 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-1.png" alt="N 等于 10、正面概率等于 0.25 时的二项分布直方图"><figcaption>图 2.1：当 $N=10$、$\mu=0.25$ 时，二项分布（2.9）关于 $m$ 的直方图。</figcaption></figure>

式（2.7）也称为样本均值。如果用 $m$ 表示这个数据集中 $x=1$（正面）的观测次数，就可以将式（2.7）写成

$$
\mu_{\mathrm{ML}}=\frac{m}{N}.
\tag{2.8}
$$

因此，在这个最大似然框架下，正面朝上的概率，就是数据集中正面观测所占的比例。

现在假设抛硬币 3 次，恰好观察到 3 次正面。此时，$N=m=3$，且 $\mu_{\mathrm{ML}}=1$。最大似然的结果会预测，今后所有观测都应当是正面。常识告诉我们，这并不合理；事实上，这是最大似然所产生的过拟合的一个极端例子。稍后会看到，如何通过为 $\mu$ 引入先验分布，得到更合理的结论。

还可以在数据集大小为 $N$ 的条件下，求出 $x=1$ 的观测次数 $m$ 的分布。这称为二项分布（binomial distribution）。由式（2.5）可知，它正比于 $\mu^m(1-\mu)^{N-m}$。为了求得归一化系数，需要把 $N$ 次抛硬币中出现 $m$ 次正面的所有可能方式加起来，因此，二项分布可以写成

$$
\operatorname{Bin}(m\mid N,\mu)=\binom{N}{m}\mu^m(1-\mu)^{N-m}.
\tag{2.9}
$$

其中，

$$
\binom{N}{m}\equiv\frac{N!}{(N-m)!m!}
\tag{2.10}
$$

是在总共 $N$ 个相同对象中选取 $m$ 个对象的方式数。<span class="margin-reference">习题 2.3</span> 图 2.1 绘出了 $N=10$、$\mu=0.25$ 时的二项分布。

利用习题 1.10 的结果，可以求得二项分布的均值和方差。该结果表明，对于独立事件，和的均值等于均值的和，和的方差等于方差的和。由于 $m=x_1+\ldots+x_N$，而每次观测的均值和方差由

<!-- pdf-page: 91 -->
<!-- join-previous-paragraph -->
式（2.3）和式（2.4）分别给出，因此有

$$
\mathbb{E}[m]\equiv\sum_{m=0}^{N}m\operatorname{Bin}(m\mid N,\mu)=N\mu,
\tag{2.11}
$$

$$
\operatorname{var}[m]\equiv\sum_{m=0}^{N}(m-\mathbb{E}[m])^2\operatorname{Bin}(m\mid N,\mu)=N\mu(1-\mu).
\tag{2.12}
$$

这些结果也可以直接用微积分证明。<span class="margin-reference">习题 2.4</span>

### 2.1.1 Beta 分布

由式（2.8）可知，伯努利分布参数 $\mu$ 的最大似然取值，也就是二项分布中该参数的最大似然取值，等于数据集中 $x=1$ 的观测所占的比例。前面已经指出，对于小数据集，这可能产生严重过拟合的结果。要对这个问题作贝叶斯处理，需要为参数 $\mu$ 引入先验分布 $p(\mu)$。这里考虑一种既容易解释、又有一些有用解析性质的先验分布。为了说明为什么选择这种先验，注意似然函数是若干形如 $\mu^x(1-\mu)^{1-x}$ 的因子的乘积。如果选择与 $\mu$ 和 $(1-\mu)$ 的幂的乘积成正比的先验，那么，正比于先验与似然函数乘积的后验分布，就会与先验具有相同的函数形式。这种性质称为共轭性（conjugacy），本章后面还会遇到几个例子。因此，我们选择称为 Beta 分布的先验，其形式为

$$
\operatorname{Beta}(\mu\mid a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\mu^{a-1}(1-\mu)^{b-1}.
\tag{2.13}
$$

其中，$\Gamma(x)$ 是式（1.141）定义的伽马函数；式（2.13）中的系数保证 Beta 分布归一化，即 <span class="margin-reference">习题 2.5</span>

$$
\int_0^1\operatorname{Beta}(\mu\mid a,b)\,\mathrm{d}\mu=1.
\tag{2.14}
$$

Beta 分布的均值和方差分别为 <span class="margin-reference">习题 2.6</span>

$$
\mathbb{E}[\mu]=\frac{a}{a+b},
\tag{2.15}
$$

$$
\operatorname{var}[\mu]=\frac{ab}{(a+b)^2(a+b+1)}.
\tag{2.16}
$$

参数 $a$ 和 $b$ 通常称为超参数，因为它们控制参数 $\mu$ 的分布。图 2.2 绘出了超参数取不同值时的 Beta 分布。

将 Beta 先验（2.13）与二项似然函数（2.9）相乘并归一化，就得到 $\mu$ 的后验分布。只保留依赖于 $\mu$ 的因子，可以看到该后验分布的形式为

$$
p(\mu\mid m,l,a,b)\propto\mu^{m+a-1}(1-\mu)^{l+b-1}.
\tag{2.17}
$$

<!-- pdf-page: 92 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-2.png" alt="四组超参数下的 Beta 分布曲线，分别展示两端高、中间平坦和单峰等形状"><figcaption>图 2.2：超参数 $a$、$b$ 取不同值时，式（2.13）给出的 Beta 分布 $\operatorname{Beta}(\mu\mid a,b)$ 关于 $\mu$ 的曲线。</figcaption></figure>

其中，$l=N-m$，因此，在硬币的例子中，它对应“反面”的次数。可以看到，式（2.17）对 $\mu$ 的函数依赖与先验分布相同，反映了先验相对于似然函数的共轭性质。事实上，它就是另一个 Beta 分布，因此，可以通过与式（2.13）比较来求得归一化系数，得到

$$
p(\mu\mid m,l,a,b)=\frac{\Gamma(m+a+l+b)}{\Gamma(m+a)\Gamma(l+b)}\mu^{m+a-1}(1-\mu)^{l+b-1}.
\tag{2.18}
$$

可以看到，在观测到一个包含 $m$ 次 $x=1$ 和 $l$ 次 $x=0$ 的数据集之后，从先验分布到后验分布的变化，只是把 $a$ 增加了 $m$，把 $b$ 增加了 $l$。因此，可以把先验中的超参数 $a$ 和 $b$ 简单解释为：分别与 $x=1$ 和 $x=0$ 对应的有效观测次数。注意，$a$ 和 $b$ 不必是整数。另外，如果之后又观测到新的数据，当前的后验分布就可以作为先验。为理解这一点，可以设想每次只取得一个观测，并在每次观测后，将当前的后验

<!-- pdf-page: 93 -->
<!-- join-previous-paragraph -->
分布乘以新观测的似然函数，再归一化，从而得到更新后的后验分布。在每个阶段，后验都是一个 Beta 分布；参数 $a$ 和 $b$ 分别给出 $x=1$ 与 $x=0$ 的先验观测和实际观测的总次数。加入一次新的 $x=1$ 观测，只需把 $a$ 增加 1；若观测为 $x=0$，则把 $b$ 增加 1。图 2.3 说明了这个过程的一步。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-3.png" alt="一次序贯贝叶斯更新的先验、似然函数与后验三幅曲线"><figcaption>图 2.3：序贯贝叶斯推断的一步。先验是参数为 $a=2$、$b=2$ 的 Beta 分布；似然函数由式（2.9）取 $N=m=1$ 给出，对应一次 $x=1$ 的观测。因此，后验是参数为 $a=3$、$b=2$ 的 Beta 分布。</figcaption><p class="figure-translation">prior → 先验；likelihood function → 似然函数；posterior → 后验。</p></figure>

采用贝叶斯观点时，这种序贯（sequential）学习方法就自然出现了。它与先验和似然函数的选择无关，只依赖于数据独立同分布的假设。序贯方法每次使用一个观测或一小批观测，并在使用下一批观测之前丢弃先前的数据。例如，它可用于实时学习：数据不断到来，而在看到全部数据之前，就必须作出预测。由于不需要把整个数据集存储起来或载入内存，序贯方法也适用于大数据集。最大似然方法同样可以写成序贯形式。<span class="margin-reference">第 2.3.5 节</span>

如果目标是尽可能准确地预测下一次试验的结果，就必须在给定观测数据集 $\mathcal{D}$ 的条件下，计算 $x$ 的预测分布。由概率的求和法则和乘积法则，有

$$
p(x=1\mid\mathcal{D})=\int_0^1 p(x=1\mid\mu)p(\mu\mid\mathcal{D})\,\mathrm{d}\mu=\int_0^1\mu p(\mu\mid\mathcal{D})\,\mathrm{d}\mu=\mathbb{E}[\mu\mid\mathcal{D}].
\tag{2.19}
$$

利用后验分布 $p(\mu\mid\mathcal{D})$ 的结果（2.18），以及 Beta 分布均值的结果（2.15），得到

$$
p(x=1\mid\mathcal{D})=\frac{m+a}{m+a+l+b}.
\tag{2.20}
$$

它有一个简单的解释：在所有观测（包括实际观测和虚构的先验观测）中，对应 $x=1$ 的观测所占的总比例。注意，当数据集无限增大，即 $m,l\to\infty$ 时，结果（2.20）退化为最大似然结果（2.8）。后面会看到，这是一个很普遍的性质：在数据集无限

<!-- pdf-page: 94 -->
<!-- join-previous-paragraph -->
大的极限下，贝叶斯结果与最大似然结果相同。对于有限数据集，$\mu$ 的后验均值总是位于先验均值和 $\mu$ 的最大似然估计之间；后者就是式（2.7）给出的事件相对频率。<span class="margin-reference">习题 2.7</span>

从图 2.2 可以看到，随着观测次数增加，后验分布的峰变得更尖。由 Beta 分布方差的结果（2.16）也能看出这一点：当 $a\to\infty$ 或 $b\to\infty$ 时，方差趋于零。事实上，我们可能会问：随着观测到的数据越来越多，后验分布所表达的不确定性是否会持续减小？这是否是贝叶斯学习的一般性质？

为回答这一问题，可以从频率学派的角度考察贝叶斯学习，并证明这一性质确实在平均意义下成立。考虑关于参数 $\boldsymbol{\theta}$ 的一般贝叶斯推断问题，已经观测到数据集 $\mathcal{D}$，用联合分布 $p(\boldsymbol{\theta},\mathcal{D})$ 描述。下面的结果 <span class="margin-reference">习题 2.8</span>

$$
\mathbb{E}_{\boldsymbol{\theta}}[\boldsymbol{\theta}]=\mathbb{E}_{\mathcal{D}}\left[\mathbb{E}_{\boldsymbol{\theta}}[\boldsymbol{\theta}\mid\mathcal{D}]\right],
\tag{2.21}
$$

其中，

$$
\mathbb{E}_{\boldsymbol{\theta}}[\boldsymbol{\theta}]\equiv\int p(\boldsymbol{\theta})\boldsymbol{\theta}\,\mathrm{d}\boldsymbol{\theta},
\tag{2.22}
$$

$$
\mathbb{E}_{\mathcal{D}}[\mathbb{E}_{\boldsymbol{\theta}}[\boldsymbol{\theta}\mid\mathcal{D}]]\equiv\int\left\{\int\boldsymbol{\theta}p(\boldsymbol{\theta}\mid\mathcal{D})\,\mathrm{d}\boldsymbol{\theta}\right\}p(\mathcal{D})\,\mathrm{d}\mathcal{D},
\tag{2.23}
$$

说明：对生成数据的分布取平均后，$\boldsymbol{\theta}$ 的后验均值等于 $\boldsymbol{\theta}$ 的先验均值。类似地，可以证明

$$
\operatorname{var}_{\boldsymbol{\theta}}[\boldsymbol{\theta}]=\mathbb{E}_{\mathcal{D}}\left[\operatorname{var}_{\boldsymbol{\theta}}[\boldsymbol{\theta}\mid\mathcal{D}]\right]+\operatorname{var}_{\mathcal{D}}\left[\mathbb{E}_{\boldsymbol{\theta}}[\boldsymbol{\theta}\mid\mathcal{D}]\right].
\tag{2.24}
$$

式（2.24）左侧是 $\boldsymbol{\theta}$ 的先验方差。右侧第一项是 $\boldsymbol{\theta}$ 的平均后验方差，第二项度量 $\boldsymbol{\theta}$ 的后验均值的方差。由于这个方差是正量，结果表明，在平均意义下，$\boldsymbol{\theta}$ 的后验方差小于先验方差。后验均值的方差越大，方差减小得就越多。不过要注意，这个结果只在平均意义下成立；对于某个具体的观测数据集，后验方差可能大于先验方差。

## 2.2 多项变量

二元变量可用于描述只能取两个可能值之一的量。然而，我们常常遇到可以取 $K$ 个互斥状态之一的离散变量。虽然这类变量有多种表示方法，但稍后会看到，一种特别方便的表示是 1-of-$K$ 方案：用一个 $K$ 维向量 $\mathbf{x}$ 表示变量，其中一个分量 $x_k$ 等于 1，其余所有分量都等于

<!-- pdf-page: 95 -->
<!-- join-previous-paragraph -->
0。例如，某个变量可以取 $K=6$ 个状态，而一次观测恰好对应 $x_3=1$ 的状态，则 $\mathbf{x}$ 表示为

$$
\mathbf{x}=(0,0,1,0,0,0)^{\mathrm T}.
\tag{2.25}
$$

注意，这样的向量满足 $\sum_{k=1}^{K}x_k=1$。若用参数 $\mu_k$ 表示 $x_k=1$ 的概率，则 $\mathbf{x}$ 的分布为

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{k=1}^{K}\mu_k^{x_k}.
\tag{2.26}
$$

其中，$\boldsymbol{\mu}=(\mu_1,\ldots,\mu_K)^{\mathrm T}$；由于参数 $\mu_k$ 表示概率，它们必须满足 $\mu_k\geqslant0$ 和 $\sum_k\mu_k=1$。可以将分布（2.26）看作把伯努利分布推广到多于两种结果的情形。很容易看出，该分布是归一化的：

$$
\sum_{\mathbf{x}}p(\mathbf{x}\mid\boldsymbol{\mu})=\sum_{k=1}^{K}\mu_k=1,
\tag{2.27}
$$

并且

$$
\mathbb{E}[\mathbf{x}\mid\boldsymbol{\mu}]=\sum_{\mathbf{x}}p(\mathbf{x}\mid\boldsymbol{\mu})\mathbf{x}=(\mu_1,\ldots,\mu_M)^{\mathrm T}=\boldsymbol{\mu}.
\tag{2.28}
$$

现在考虑由 $N$ 个独立观测 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 组成的数据集 $\mathcal{D}$。相应的似然函数为

$$
p(\mathcal{D}\mid\boldsymbol{\mu})=\prod_{n=1}^{N}\prod_{k=1}^{K}\mu_k^{x_{nk}}=\prod_{k=1}^{K}\mu_k^{(\sum_n x_{nk})}=\prod_{k=1}^{K}\mu_k^{m_k}.
\tag{2.29}
$$

可以看到，似然函数只通过下面 $K$ 个量依赖于 $N$ 个数据点：

$$
m_k=\sum_n x_{nk}.
\tag{2.30}
$$

这些量表示 $x_k=1$ 的观测次数，称为该分布的充分统计量。<span class="margin-reference">第 2.4 节</span>

为了求出 $\boldsymbol{\mu}$ 的最大似然解，需要在考虑 $\mu_k$ 之和必须为 1 的约束下，对 $\mu_k$ 最大化 $\ln p(\mathcal{D}\mid\boldsymbol{\mu})$。这可以通过引入拉格朗日乘子 $\lambda$，最大化下式来实现：<span class="margin-reference">附录 E</span>

$$
\sum_{k=1}^{K}m_k\ln\mu_k+\lambda\left(\sum_{k=1}^{K}\mu_k-1\right).
\tag{2.31}
$$

令式（2.31）对 $\mu_k$ 的导数为零，得到

$$
\mu_k=-m_k/\lambda.
\tag{2.32}
$$

<!-- pdf-page: 96 -->

将式（2.32）代入约束 $\sum_k\mu_k=1$，可以求出拉格朗日乘子 $\lambda=-N$。于是得到最大似然解

$$
\mu_k^{\mathrm{ML}}=\frac{m_k}{N}.
\tag{2.33}
$$

它就是 $N$ 次观测中 $x_k=1$ 所占的比例。

可以考虑给定参数 $\boldsymbol{\mu}$ 和观测总次数 $N$ 时，$m_1,\ldots,m_K$ 的联合分布。由式（2.29）可知，其形式为

$$
\operatorname{Mult}(m_1,m_2,\ldots,m_K\mid\boldsymbol{\mu},N)=\binom{N}{m_1m_2\ldots m_K}\prod_{k=1}^{K}\mu_k^{m_k}.
\tag{2.34}
$$

这称为多项分布（multinomial distribution）。归一化系数等于把 $N$ 个对象分为 $K$ 组、各组大小分别为 $m_1,\ldots,m_K$ 的方式数，其值为

$$
\binom{N}{m_1m_2\ldots m_K}=\frac{N!}{m_1!m_2!\ldots m_K!}.
\tag{2.35}
$$

注意，变量 $m_k$ 满足约束

$$
\sum_{k=1}^{K}m_k=N.
\tag{2.36}
$$

### 2.2.1 狄利克雷分布

现在为多项分布（2.34）的参数 $\{\mu_k\}$ 引入一个先验分布族。观察多项分布的形式，可以看出其共轭先验为

$$
p(\boldsymbol{\mu}\mid\boldsymbol{\alpha})\propto\prod_{k=1}^{K}\mu_k^{\alpha_k-1}.
\tag{2.37}
$$

其中，$0\leqslant\mu_k\leqslant1$，且 $\sum_k\mu_k=1$。这里，$\alpha_1,\ldots,\alpha_K$ 是该分布的参数，$\boldsymbol{\alpha}$ 表示 $(\alpha_1,\ldots,\alpha_K)^{\mathrm T}$。注意，由于求和约束，$\{\mu_k\}$ 空间上的分布被限制在一个 $K-1$ 维单纯形（simplex）上；图 2.4 示意了 $K=3$ 的情形。

该分布归一化后的形式为 <span class="margin-reference">习题 2.9</span>

$$
\operatorname{Dir}(\boldsymbol{\mu}\mid\boldsymbol{\alpha})=\frac{\Gamma(\alpha_0)}{\Gamma(\alpha_1)\cdots\Gamma(\alpha_K)}\prod_{k=1}^{K}\mu_k^{\alpha_k-1}.
\tag{2.38}
$$

这称为狄利克雷分布（Dirichlet distribution）。这里，$\Gamma(x)$ 是式（1.141）定义的伽马函数，而

$$
\alpha_0=\sum_{k=1}^{K}\alpha_k.
\tag{2.39}
$$

<!-- pdf-page: 97 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-4.png" alt="三维坐标空间中由三个坐标轴截点构成的三角形单纯形"><figcaption>图 2.4：由于约束 $0\leqslant\mu_k\leqslant1$ 和 $\sum_k\mu_k=1$，三个变量 $\mu_1,\mu_2,\mu_3$ 的狄利克雷分布被限制在图示的单纯形上，即一个有界线性流形。</figcaption></figure>

图 2.5 绘出了参数 $\alpha_k$ 取不同值时，单纯形上的狄利克雷分布。

将先验（2.38）与似然函数（2.34）相乘，得到参数 $\{\mu_k\}$ 的后验分布：

$$
p(\boldsymbol{\mu}\mid\mathcal{D},\boldsymbol{\alpha})\propto p(\mathcal{D}\mid\boldsymbol{\mu})p(\boldsymbol{\mu}\mid\boldsymbol{\alpha})\propto\prod_{k=1}^{K}\mu_k^{\alpha_k+m_k-1}.
\tag{2.40}
$$

可以看到，后验分布仍然是狄利克雷分布，这证实了狄利克雷分布确实是多项分布的共轭先验。因此，可以通过与式（2.38）比较来确定归一化系数，得到

$$
\begin{aligned}
p(\boldsymbol{\mu}\mid\mathcal{D},\boldsymbol{\alpha})&=\operatorname{Dir}(\boldsymbol{\mu}\mid\boldsymbol{\alpha}+\mathbf{m})\\
&=\frac{\Gamma(\alpha_0+N)}{\Gamma(\alpha_1+m_1)\cdots\Gamma(\alpha_K+m_K)}\prod_{k=1}^{K}\mu_k^{\alpha_k+m_k-1}.
\end{aligned}
\tag{2.41}
$$

其中，$\mathbf{m}=(m_1,\ldots,m_K)^{\mathrm T}$。与二项分布及其 Beta 先验的情形一样，可以把狄利克雷先验中的参数 $\alpha_k$ 解释为 $x_k=1$ 的有效观测次数。

<aside class="biography"><p><strong>勒热纳·狄利克雷（Lejeune Dirichlet）</strong><br>1805–1859</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-dirichlet.png" alt="勒热纳·狄利克雷肖像"><p>约翰·彼得·古斯塔夫·勒热纳·狄利克雷是一位谦逊、内敛的数学家。他在数论、力学和天文学方面作出了贡献，并首次对傅里叶级数进行了严格分析。他的家族来自比利时的 Richelet，Lejeune Dirichlet 这个名字源自“le jeune de Richelet”，意为“来自 Richelet 的年轻人”。狄利克雷的第一篇论文发表于 1825 年，使他立即成名。论文讨论了费马大定理，即当 $n>2$ 时，方程 $x^n+y^n=z^n$ 没有正整数解。狄利克雷给出了 $n=5$ 情形的部分证明，随后将其交给勒让德审阅，后者完成了证明。后来，狄利克雷又给出了 $n=14$ 情形的完整证明；但任意 $n$ 的费马大定理的完整证明，要等到 20 世纪末安德鲁·怀尔斯的工作才出现。</p></aside>

注意，两状态的量既可以表示为二元变量，并用

<!-- pdf-page: 98 -->
<!-- join-previous-paragraph -->
二项分布（2.9）建模；也可以表示为 1-of-2 变量，并用 $K=2$ 的多项分布（2.34）建模。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-5.png" alt="三个变量的三幅狄利克雷密度曲面，分别在边缘集中、均匀和中央集中"><figcaption>图 2.5：三个变量的狄利克雷分布。两个水平轴是单纯形所在平面内的坐标，竖直轴对应密度值。左图中 $\{\alpha_k\}=0.1$，中图中 $\{\alpha_k\}=1$，右图中 $\{\alpha_k\}=10$。</figcaption></figure>

## 2.3 高斯分布

高斯分布也称正态分布，是连续变量分布的一种广泛使用的模型。对于单个变量 $x$，高斯分布可以写成

$$
\mathcal{N}(x\mid\mu,\sigma^2)=\frac{1}{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac{1}{2\sigma^2}(x-\mu)^2\right\}.
\tag{2.42}
$$

其中，$\mu$ 是均值，$\sigma^2$ 是方差。对于 $D$ 维向量 $\mathbf{x}$，多元高斯分布的形式为

$$
\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}.
\tag{2.43}
$$

其中，$\boldsymbol{\mu}$ 是 $D$ 维均值向量，$\boldsymbol{\Sigma}$ 是 $D\times D$ 协方差矩阵，$|\boldsymbol{\Sigma}|$ 表示 $\boldsymbol{\Sigma}$ 的行列式。

高斯分布会出现在许多不同的情境中，可以从多个不同角度说明它为何重要。例如，前面已经看到，对于单个实值变量，使熵最大的分布就是高斯分布。<span class="margin-reference">第 1.6 节</span> 这一性质也适用于多元高斯分布。<span class="margin-reference">习题 2.14</span>

考虑多个随机变量的和时，也会出现高斯分布。拉普拉斯提出的中心极限定理（central limit theorem）指出，在满足某些较宽松条件的情况下，一组随机变量的和（它本身当然也是随机变量）的分布，会随着求和项数的增加而越来越接近高斯分布（Walker, 1969）。我们可以

<!-- pdf-page: 99 -->
<!-- join-previous-paragraph -->
用如下例子说明：考虑 $N$ 个变量 $x_1,\ldots,x_N$，每个变量都在区间 $[0,1]$ 上服从均匀分布，再考察它们的平均值 $(x_1+\cdots+x_N)/N$ 的分布。当 $N$ 很大时，这个分布趋近于高斯分布，如图 2.6 所示。在实际情形中，随着 $N$ 增大，向高斯分布的收敛可能非常快。这个结果的一个推论是：二项分布（2.9）是关于 $m$ 的分布，而 $m$ 是二元随机变量 $x$ 的 $N$ 次观测之和，因此，当 $N\to\infty$ 时，二项分布将趋近于高斯分布（$N=10$ 的情形见图 2.1）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-6.png" alt="分别对一个、两个和十个均匀分布数取平均所得分布的直方图"><figcaption>图 2.6：不同 $N$ 值下，$N$ 个均匀分布的数的平均值的直方图。可以看到，随着 $N$ 增加，分布趋近于高斯分布。</figcaption></figure>

高斯分布具有许多重要的解析性质，我们将详细讨论其中几项。因此，本节比前面的部分章节涉及更多数学推导，并要求读者熟悉各种矩阵恒等式。<span class="margin-reference">附录 C</span> 不过，我们强烈建议读者熟练掌握这里介绍的高斯分布运算方法，因为这对于理解后续章节中更复杂的模型极有帮助。

<aside class="biography"><p><strong>卡尔·弗里德里希·高斯（Carl Friedrich Gauss）</strong><br>1777–1855</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-gauss.png" alt="卡尔·弗里德里希·高斯肖像"><p>据说，高斯 7 岁上小学时，老师 Büttner 为了让全班有事可做，要求学生计算从 1 到 100 的整数之和。令老师惊讶的是，高斯片刻间就算出了答案：他注意到，可以把这个和分成 50 对（1＋100、2＋99 等），每对的和都是 101，因此答案为 5,050。如今人们认为，当时实际布置的题目形式相同，但要难一些，因为数列的起始值和公差都更大。高斯是德国数学家和科学家，以勤奋和追求完美著称。他的众多贡献之一，是证明在误差服从正态分布的假设下可以推导出最小二乘法。他还建立了非欧几何的一种早期形式；这种几何理论内部自洽，却不满足欧几里得的公理。但他担心，公开承认自己相信这种几何会损害声誉，因此不愿公开讨论。高斯曾受托对汉诺威进行大地测量，这促使他建立了正态分布，也就是今天所称的高斯分布。他去世后，人们研究他的日记发现，有些重要数学结果早在其他人发表的数年、甚至数十年前，他就已经发现了。</p></aside>

我们先考察高斯分布的几何形式。高斯分布对

<!-- pdf-page: 100 -->
<!-- join-previous-paragraph -->
$\mathbf{x}$ 的函数依赖，是通过指数中的二次型

$$
\Delta^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})
\tag{2.44}
$$

体现的。量 $\Delta$ 称为从 $\boldsymbol{\mu}$ 到 $\mathbf{x}$ 的马氏距离（Mahalanobis distance）；当 $\boldsymbol{\Sigma}$ 为单位矩阵时，它就退化为欧氏距离。在 $\mathbf{x}$ 空间中，使这一二次型保持不变的曲面上，高斯分布也保持不变。

首先，不失一般性，可以把矩阵 $\boldsymbol{\Sigma}$ 取为对称矩阵，因为任何反对称分量都会从指数中消失。<span class="margin-reference">习题 2.17</span> 现在考虑协方差矩阵的特征向量方程

$$
\boldsymbol{\Sigma}\mathbf{u}_i=\lambda_i\mathbf{u}_i.
\tag{2.45}
$$

其中，$i=1,\ldots,D$。由于 $\boldsymbol{\Sigma}$ 是实对称矩阵，它的特征值都是实数，而且可以选取一组标准正交的特征向量，因此 <span class="margin-reference">习题 2.18</span>

$$
\mathbf{u}_i^{\mathrm T}\mathbf{u}_j=I_{ij}.
\tag{2.46}
$$

这里，$I_{ij}$ 是单位矩阵的第 $(i,j)$ 个元素，满足

$$
I_{ij}=\begin{cases}1,&\text{若 }i=j,\\0,&\text{否则。}\end{cases}
\tag{2.47}
$$

协方差矩阵 $\boldsymbol{\Sigma}$ 可以用它的特征向量展开为 <span class="margin-reference">习题 2.19</span>

$$
\boldsymbol{\Sigma}=\sum_{i=1}^{D}\lambda_i\mathbf{u}_i\mathbf{u}_i^{\mathrm T}.
\tag{2.48}
$$

类似地，逆协方差矩阵 $\boldsymbol{\Sigma}^{-1}$ 可以表示为

$$
\boldsymbol{\Sigma}^{-1}=\sum_{i=1}^{D}\frac{1}{\lambda_i}\mathbf{u}_i\mathbf{u}_i^{\mathrm T}.
\tag{2.49}
$$

将式（2.49）代入式（2.44），二次型变为

$$
\Delta^2=\sum_{i=1}^{D}\frac{y_i^2}{\lambda_i}.
\tag{2.50}
$$

其中定义了

$$
y_i=\mathbf{u}_i^{\mathrm T}(\mathbf{x}-\boldsymbol{\mu}).
\tag{2.51}
$$

可以把 $\{y_i\}$ 理解为由标准正交向量 $\mathbf{u}_i$ 定义的新坐标系，它相对于原来的 $x_i$ 坐标系作了平移和旋转。构造向量 $\mathbf{y}=(y_1,\ldots,y_D)^{\mathrm T}$，有

$$
\mathbf{y}=\mathbf{U}(\mathbf{x}-\boldsymbol{\mu}).
\tag{2.52}
$$

<!-- pdf-page: 101 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-7.png" alt="二维高斯分布的椭圆等密度线以及由协方差特征向量定义的新坐标轴"><figcaption>图 2.7：红色曲线表示二维空间 $\mathbf{x}=(x_1,x_2)$ 中高斯分布的椭圆等概率密度曲面。该曲面上的密度为 $\mathbf{x}=\boldsymbol{\mu}$ 处密度的 $\exp(-1/2)$ 倍。椭圆主轴由协方差矩阵的特征向量 $\mathbf{u}_i$ 决定，对应特征值为 $\lambda_i$。</figcaption></figure>

其中，$\mathbf{U}$ 是各行分别为 $\mathbf{u}_i^{\mathrm T}$ 的矩阵。由式（2.46）可知，$\mathbf{U}$ 是正交矩阵（orthogonal matrix），即满足 $\mathbf{U}\mathbf{U}^{\mathrm T}=\mathbf{I}$，因而也有 $\mathbf{U}^{\mathrm T}\mathbf{U}=\mathbf{I}$，其中 $\mathbf{I}$ 为单位矩阵。<span class="margin-reference">附录 C</span>

在使式（2.51）保持不变的曲面上，二次型以及高斯密度都保持不变。如果所有特征值 $\lambda_i$ 都为正，这些曲面就是椭球面：中心位于 $\boldsymbol{\mu}$，各轴沿 $\mathbf{u}_i$ 方向，对应方向的尺度因子为 $\lambda_i^{1/2}$，如图 2.7 所示。

要使高斯分布有良好定义，协方差矩阵的所有特征值 $\lambda_i$ 必须严格为正，否则该分布不能正确归一化。特征值全都严格为正的矩阵，称为正定（positive definite）矩阵。第 12 章将会遇到一个或多个特征值为零的高斯分布；此时，该分布是奇异的（singular），被限制在一个维数更低的子空间中。如果所有特征值均非负，则称协方差矩阵为半正定（positive semidefinite）矩阵。

现在考虑高斯分布在由 $y_i$ 定义的新坐标系中的形式。从 $\mathbf{x}$ 坐标系变到 $\mathbf{y}$ 坐标系时，雅可比矩阵 $\mathbf{J}$ 的元素为

$$
J_{ij}=\frac{\partial x_i}{\partial y_j}=U_{ji}.
\tag{2.53}
$$

其中，$U_{ji}$ 是矩阵 $\mathbf{U}^{\mathrm T}$ 的元素。利用矩阵 $\mathbf{U}$ 的标准正交性质，可以看出雅可比矩阵行列式的平方为

$$
|\mathbf{J}|^2=|\mathbf{U}^{\mathrm T}|^2=|\mathbf{U}^{\mathrm T}||\mathbf{U}|=|\mathbf{U}^{\mathrm T}\mathbf{U}|=|\mathbf{I}|=1.
\tag{2.54}
$$

因此 $|\mathbf{J}|=1$。此外，协方差矩阵的行列式 $|\boldsymbol{\Sigma}|$ 可以写成

<!-- pdf-page: 102 -->
<!-- join-previous-paragraph -->
其特征值的乘积，因此

$$
|\boldsymbol{\Sigma}|^{1/2}=\prod_{j=1}^{D}\lambda_j^{1/2}.
\tag{2.55}
$$

所以，在 $y_j$ 坐标系中，高斯分布的形式为

$$
p(\mathbf{y})=p(\mathbf{x})|\mathbf{J}|=\prod_{j=1}^{D}\frac{1}{(2\pi\lambda_j)^{1/2}}\exp\left\{-\frac{y_j^2}{2\lambda_j}\right\}.
\tag{2.56}
$$

这是 $D$ 个相互独立的一元高斯分布的乘积。因此，特征向量定义了一组经过平移和旋转的新坐标，在该坐标系中，联合概率分布分解为各个独立分布的乘积。于是，分布在 $\mathbf{y}$ 坐标系中的积分为

$$
\int p(\mathbf{y})\,\mathrm{d}\mathbf{y}=\prod_{j=1}^{D}\int_{-\infty}^{\infty}\frac{1}{(2\pi\lambda_j)^{1/2}}\exp\left\{-\frac{y_j^2}{2\lambda_j}\right\}\mathrm{d}y_j=1.
\tag{2.57}
$$

这里使用了一元高斯分布的归一化结果（1.48）。这证实了多元高斯分布（2.43）确实已经归一化。

现在考察高斯分布的矩，从而解释参数 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 的含义。高斯分布下 $\mathbf{x}$ 的期望为

$$
\begin{aligned}
\mathbb{E}[\mathbf{x}]&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\int\exp\left\{-\frac12(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}\mathbf{x}\,\mathrm{d}\mathbf{x}\\
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\int\exp\left\{-\frac12\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})\,\mathrm{d}\mathbf{z}.
\end{aligned}
\tag{2.58}
$$

这里作了变量替换 $\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}$。注意，指数是 $\mathbf{z}$ 各分量的偶函数，而对这些分量的积分区间为 $(-\infty,\infty)$，因此，因子 $(\mathbf{z}+\boldsymbol{\mu})$ 中的 $\mathbf{z}$ 项会因对称性而消失。于是

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}.
\tag{2.59}
$$

因此，把 $\boldsymbol{\mu}$ 称为高斯分布的均值。

现在考虑高斯分布的二阶矩。在一元情形下，我们考察了二阶矩 $\mathbb{E}[x^2]$。对于多元高斯分布，有 $D^2$ 个二阶矩 $\mathbb{E}[x_ix_j]$，可以将它们合成矩阵 $\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]$。该矩阵可以写为

$$
\begin{aligned}
\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\int\exp\left\{-\frac12(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}\mathbf{x}\mathbf{x}^{\mathrm T}\,\mathrm{d}\mathbf{x}\\
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\int\exp\left\{-\frac12\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm T}\,\mathrm{d}\mathbf{z}.
\end{aligned}
$$

<!-- pdf-page: 103 -->

这里再次作了变量替换 $\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}$。注意，含有 $\boldsymbol{\mu}\mathbf{z}^{\mathrm T}$ 和 $\boldsymbol{\mu}^{\mathrm T}\mathbf{z}$ 的交叉项同样会因对称性而消失。$\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}$ 项为常量，可以移到积分号外；由于高斯分布已归一化，积分本身等于 1。接着考虑含 $\mathbf{z}\mathbf{z}^{\mathrm T}$ 的项。再次利用式（2.45）给出的协方差矩阵的特征向量展开，以及特征向量组的完备性，可以写出

$$
\mathbf{z}=\sum_{j=1}^{D}y_j\mathbf{u}_j.
\tag{2.60}
$$

其中，$y_j=\mathbf{u}_j^{\mathrm T}\mathbf{z}$，于是得到

$$
\begin{aligned}
&\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\int\exp\left\{-\frac12\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}\mathbf{z}\mathbf{z}^{\mathrm T}\,\mathrm{d}\mathbf{z}\\
&\quad=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\sum_{i=1}^{D}\sum_{j=1}^{D}\mathbf{u}_i\mathbf{u}_j^{\mathrm T}\int\exp\left\{-\sum_{k=1}^{D}\frac{y_k^2}{2\lambda_k}\right\}y_iy_j\,\mathrm{d}\mathbf{y}\\
&\quad=\sum_{i=1}^{D}\mathbf{u}_i\mathbf{u}_i^{\mathrm T}\lambda_i=\boldsymbol{\Sigma}.
\end{aligned}
\tag{2.61}
$$

这里使用了特征向量方程（2.45），以及如下事实：除非 $i=j$，否则中间一行右侧的积分会因对称性而消失；最后一行使用了结果（1.50）、（2.55）和（2.48）。因此有

$$
\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]=\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}+\boldsymbol{\Sigma}.
\tag{2.62}
$$

对于单个随机变量，我们在求二阶矩之前先减去均值，以此定义方差。同样，在多元情形下，先减去均值也很方便，由此得到随机向量 $\mathbf{x}$ 的协方差（covariance），定义为

$$
\operatorname{cov}[\mathbf{x}]=\mathbb{E}\left[(\mathbf{x}-\mathbb{E}[\mathbf{x}])(\mathbf{x}-\mathbb{E}[\mathbf{x}])^{\mathrm T}\right].
\tag{2.63}
$$

对于高斯分布这一特例，利用 $\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}$ 和结果（2.62），得到

$$
\operatorname{cov}[\mathbf{x}]=\boldsymbol{\Sigma}.
\tag{2.64}
$$

由于参数矩阵 $\boldsymbol{\Sigma}$ 决定高斯分布下 $\mathbf{x}$ 的协方差，因此称为协方差矩阵。

虽然高斯分布（2.43）被广泛用作密度模型，它也有一些显著局限。先考虑分布中自由参数的数目。一般的对称协方差矩阵 $\boldsymbol{\Sigma}$ 有 $D(D+1)/2$ 个独立参数，而 $\boldsymbol{\mu}$ 中还有另外 $D$ 个独立参数，总共是 $D(D+3)/2$ 个参数。<span class="margin-reference">习题 2.21</span> 当 $D$ 很大时，参数总数

<!-- pdf-page: 104 -->
<!-- join-previous-paragraph -->
随 $D$ 的平方增长，对大矩阵进行运算和求逆的计算量可能大到难以承受。一种处理办法，是限制协方差矩阵的形式。如果只考虑对角协方差矩阵，即 $\boldsymbol{\Sigma}=\operatorname{diag}(\sigma_i^2)$，那么密度模型中总共只有 $2D$ 个独立参数。相应的等密度曲面为各轴与坐标轴对齐的椭球面。还可以进一步要求协方差矩阵正比于单位矩阵，即 $\boldsymbol{\Sigma}=\sigma^2\mathbf{I}$，称为各向同性（isotropic）协方差。此时模型只有 $D+1$ 个独立参数，等密度曲面为球面。图 2.8 展示了协方差矩阵的一般形式、对角形式和各向同性形式。不过，这些方法虽然限制了分布中的自由度，并大幅加快了协方差矩阵的求逆，却也严重限制了概率密度的形状，使其难以表示数据中值得关注的相关关系。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-8.png" alt="一般、对角和各向同性协方差对应的二维高斯等密度线"><figcaption>图 2.8：二维高斯分布的等概率密度线，其协方差矩阵分别为：(a) 一般形式；(b) 对角形式，此时椭圆等密度线与坐标轴对齐；(c) 与单位矩阵成正比，此时等密度线为同心圆。</figcaption></figure>

高斯分布的另一个局限，是它本质上为单峰（unimodal）分布，即只有一个极大值，因此无法很好地近似多峰分布。所以，高斯分布一方面可能过于灵活，因为参数太多；另一方面，它能够充分表示的分布类型又过于有限。后面会看到，引入潜变量（latent variable），也称隐藏变量（hidden variable）或未观测变量（unobserved variable），可以处理这两个问题。具体来说，引入离散潜变量会得到高斯混合，从而形成丰富的多峰分布族，第 2.3.9 节将对此进行讨论。同样，按照第 12 章的方法引入连续潜变量，可以得到这样一类模型：其自由参数数目能够独立于数据空间的维数 $D$ 来控制，同时仍然能够表示数据集中的主要相关关系。事实上，这两种方法可以结合起来并进一步扩展，构造出十分丰富的层次模型，以适应广泛的实际应用。例如，马尔可夫随机场（Markov random field）的高斯形式被广泛用作图像的概率模型。<span class="margin-reference">第 8.3 节</span> 它是像素亮度联合空间上的高斯分布，但通过施加反映像素空间组织关系的大量结构，使计算变得可行。同样，用于跟踪等应用中时间序列数据建模的线性动力系统（linear dynamical system），也是定义在可能非常多的观测变量与潜变量上的联合高斯分布；同样，是对分布施加的结构使其计算可行。<span class="margin-reference">第 13.3 节</span> 表达这类复杂分布的形式与性质的一种有力框架，

<!-- pdf-page: 105 -->
<!-- join-previous-paragraph -->
是概率图模型（probabilistic graphical model），它将是第 8 章的主题。

### 2.3.1 条件高斯分布

多元高斯分布的一个重要性质是：如果两组变量的联合分布是高斯分布，那么以一组为条件时，另一组的条件分布仍然是高斯分布。同样，任一组变量的边缘分布也都是高斯分布。

先考虑条件分布。假设 $\mathbf{x}$ 是一个 $D$ 维向量，服从高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，并将 $\mathbf{x}$ 划分为两个不相交的子集 $\mathbf{x}_a$ 和 $\mathbf{x}_b$。不失一般性，可以取 $\mathbf{x}$ 的前 $M$ 个分量组成 $\mathbf{x}_a$，其余 $D-M$ 个分量组成 $\mathbf{x}_b$，即

$$
\mathbf{x}=\begin{pmatrix}\mathbf{x}_a\\\mathbf{x}_b\end{pmatrix}.
\tag{2.65}
$$

相应地，将均值向量 $\boldsymbol{\mu}$ 分块为

$$
\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\end{pmatrix},
\tag{2.66}
$$

将协方差矩阵 $\boldsymbol{\Sigma}$ 分块为

$$
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}.
\tag{2.67}
$$

注意，协方差矩阵的对称性 $\boldsymbol{\Sigma}^{\mathrm T}=\boldsymbol{\Sigma}$ 意味着 $\boldsymbol{\Sigma}_{aa}$ 和 $\boldsymbol{\Sigma}_{bb}$ 都是对称的，且 $\boldsymbol{\Sigma}_{ba}=\boldsymbol{\Sigma}_{ab}^{\mathrm T}$。

在许多情形下，使用协方差矩阵的逆会更方便，即

$$
\boldsymbol{\Lambda}\equiv\boldsymbol{\Sigma}^{-1}.
\tag{2.68}
$$

它称为精度矩阵（precision matrix）。事实上，后面会看到，高斯分布有些性质用协方差表达最自然，而另一些性质用精度表达则更简单。因此，按照向量 $\mathbf{x}$ 的分块（2.65），也引入精度矩阵的分块形式

$$
\boldsymbol{\Lambda}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}.
\tag{2.69}
$$

由于对称矩阵的逆仍然对称，可以看到 $\boldsymbol{\Lambda}_{aa}$ 和 $\boldsymbol{\Lambda}_{bb}$ 都是对称的，且 $\boldsymbol{\Lambda}_{ab}^{\mathrm T}=\boldsymbol{\Lambda}_{ba}$。<span class="margin-reference">习题 2.22</span> 此处需要强调，例如 $\boldsymbol{\Lambda}_{aa}$ 并不简单地等于 $\boldsymbol{\Sigma}_{aa}$ 的逆。事实上，我们很快就会考察分块矩阵的逆与各子块的逆之间的关系。

先来求条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的表达式。由概率的乘积法则可知，要计算这个条件分布，可以

<!-- pdf-page: 106 -->
<!-- join-previous-paragraph -->
从联合分布 $p(\mathbf{x})=p(\mathbf{x}_a,\mathbf{x}_b)$ 出发，将 $\mathbf{x}_b$ 固定为观测值，再将所得表达式归一化，得到 $\mathbf{x}_a$ 上的有效概率分布。不必显式执行这一步归一化；更高效的办法是考察式（2.44）给出的高斯分布指数中的二次型，最后再补上归一化系数。利用分块（2.65）、（2.66）和（2.69），得到

$$
\begin{aligned}
&-\frac12(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\\
&\quad=-\frac12(\mathbf{x}_a-\boldsymbol{\mu}_a)^{\mathrm T}\boldsymbol{\Lambda}_{aa}(\mathbf{x}_a-\boldsymbol{\mu}_a)-\frac12(\mathbf{x}_a-\boldsymbol{\mu}_a)^{\mathrm T}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\\
&\qquad-\frac12(\mathbf{x}_b-\boldsymbol{\mu}_b)^{\mathrm T}\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)-\frac12(\mathbf{x}_b-\boldsymbol{\mu}_b)^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\mu}_b).
\end{aligned}
\tag{2.70}
$$

作为 $\mathbf{x}_a$ 的函数，它仍然是二次型，因此相应的条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 是高斯分布。由于这个分布完全由均值和协方差决定，我们的目标就是通过观察式（2.70），找出 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值和协方差的表达式。

这是高斯分布中一种常见运算的例子，有时称为“配方”（completing the square）：已知定义高斯分布指数项的二次型，需要求出对应的均值和协方差。注意一般高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 的指数可以写成

$$
-\frac12(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})=-\frac12\mathbf{x}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{x}+\mathbf{x}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}+\text{const},
\tag{2.71}
$$

就能直接解决这类问题。这里，“const” 表示与 $\mathbf{x}$ 无关的项，并且利用了 $\boldsymbol{\Sigma}$ 的对称性。因此，把一般二次型写成式（2.71）右侧的形式后，就能立即将 $\mathbf{x}$ 二次项中的系数矩阵认作逆协方差矩阵 $\boldsymbol{\Sigma}^{-1}$，将 $\mathbf{x}$ 一次项的系数认作 $\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}$，进而求出 $\boldsymbol{\mu}$。

现在把这一步骤用于条件高斯分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$，其指数中的二次型由式（2.70）给出。将该分布的均值和协方差分别记为 $\boldsymbol{\mu}_{a\mid b}$ 和 $\boldsymbol{\Sigma}_{a\mid b}$。把 $\mathbf{x}_b$ 视为常量，考察式（2.70）对 $\mathbf{x}_a$ 的函数依赖。找出所有关于 $\mathbf{x}_a$ 的二次项，得到

$$
-\frac12\mathbf{x}_a^{\mathrm T}\boldsymbol{\Lambda}_{aa}\mathbf{x}_a.
\tag{2.72}
$$

由此立即得出，$p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的协方差（精度的逆）为

$$
\boldsymbol{\Sigma}_{a\mid b}=\boldsymbol{\Lambda}_{aa}^{-1}.
\tag{2.73}
$$

<!-- pdf-page: 107 -->

现在考虑式（2.70）中所有关于 $\mathbf{x}_a$ 的一次项：

$$
\mathbf{x}_a^{\mathrm T}\{\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\}.
\tag{2.74}
$$

其中利用了 $\boldsymbol{\Lambda}_{ba}^{\mathrm T}=\boldsymbol{\Lambda}_{ab}$。根据对一般形式（2.71）的讨论，这个表达式中 $\mathbf{x}_a$ 的系数必定等于 $\boldsymbol{\Sigma}_{a\mid b}^{-1}\boldsymbol{\mu}_{a\mid b}$，因此

$$
\begin{aligned}
\boldsymbol{\mu}_{a\mid b}&=\boldsymbol{\Sigma}_{a\mid b}\{\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\}\\
&=\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{aa}^{-1}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b).
\end{aligned}
\tag{2.75}
$$

其中使用了式（2.73）。

结果（2.73）和（2.75）是用原始联合分布 $p(\mathbf{x}_a,\mathbf{x}_b)$ 的分块精度矩阵表示的。也可以用相应的分块协方差矩阵表示这些结果。为此，使用下面这个关于分块矩阵求逆的恒等式：<span class="margin-reference">习题 2.24</span>

$$
\begin{pmatrix}\mathbf{A}&\mathbf{B}\\\mathbf{C}&\mathbf{D}\end{pmatrix}^{-1}=\begin{pmatrix}\mathbf{M}&-\mathbf{M}\mathbf{B}\mathbf{D}^{-1}\\-\mathbf{D}^{-1}\mathbf{C}\mathbf{M}&\mathbf{D}^{-1}+\mathbf{D}^{-1}\mathbf{C}\mathbf{M}\mathbf{B}\mathbf{D}^{-1}\end{pmatrix}.
\tag{2.76}
$$

其中定义了

$$
\mathbf{M}=(\mathbf{A}-\mathbf{B}\mathbf{D}^{-1}\mathbf{C})^{-1}.
\tag{2.77}
$$

$\mathbf{M}^{-1}$ 称为式（2.76）左侧矩阵关于子矩阵 $\mathbf{D}$ 的舒尔补（Schur complement）。由定义

$$
\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}^{-1}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix},
\tag{2.78}
$$

并利用式（2.76），得到

$$
\boldsymbol{\Lambda}_{aa}=(\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba})^{-1},
\tag{2.79}
$$

$$
\boldsymbol{\Lambda}_{ab}=-(\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba})^{-1}\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}.
\tag{2.80}
$$

由此得到条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值和协方差：

$$
\boldsymbol{\mu}_{a\mid b}=\boldsymbol{\mu}_a+\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}(\mathbf{x}_b-\boldsymbol{\mu}_b),
\tag{2.81}
$$

$$
\boldsymbol{\Sigma}_{a\mid b}=\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba}.
\tag{2.82}
$$

比较式（2.73）与式（2.82）可以看出，用分块精度矩阵表示条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$，比用分块协方差矩阵表示更简单。注意，式（2.81）给出的条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值是 $\mathbf{x}_b$ 的线性函数，而式（2.82）给出的协方差与 $\mathbf{x}_a$ 无关。这是线性高斯（linear-Gaussian）模型的一个例子。<span class="margin-reference">第 8.1.4 节</span>

<!-- pdf-page: 108 -->

### 2.3.2 边缘高斯分布

前面已经看到，如果联合分布 $p(\mathbf{x}_a,\mathbf{x}_b)$ 为高斯分布，则条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 仍为高斯分布。现在讨论如下边缘分布：

$$
p(\mathbf{x}_a)=\int p(\mathbf{x}_a,\mathbf{x}_b)\,\mathrm{d}\mathbf{x}_b.
\tag{2.83}
$$

后面会看到，它同样是高斯分布。为了高效求出这个分布，我们仍然集中考察联合分布指数中的二次型，借此确定边缘分布 $p(\mathbf{x}_a)$ 的均值和协方差。

利用分块精度矩阵，联合分布的二次型可以写成式（2.70）的形式。由于目标是将 $\mathbf{x}_b$ 积分消去，最方便的办法是先考察含 $\mathbf{x}_b$ 的项，再通过配方使积分容易计算。只取出含 $\mathbf{x}_b$ 的项，得到

$$
-\frac12\mathbf{x}_b^{\mathrm T}\boldsymbol{\Lambda}_{bb}\mathbf{x}_b+\mathbf{x}_b^{\mathrm T}\mathbf{m}=-\frac12(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})+\frac12\mathbf{m}^{\mathrm T}\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m}.
\tag{2.84}
$$

其中定义了

$$
\mathbf{m}=\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a).
\tag{2.85}
$$

可以看到，对 $\mathbf{x}_b$ 的依赖已经写成了高斯分布的标准二次型，即式（2.84）右侧第一项，再加上一个不依赖于 $\mathbf{x}_b$、但依赖于 $\mathbf{x}_a$ 的项。因此，对这个二次型取指数之后，式（2.83）所需的关于 $\mathbf{x}_b$ 的积分具有如下形式：

$$
\int\exp\left\{-\frac12(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})\right\}\mathrm{d}\mathbf{x}_b.
\tag{2.86}
$$

注意，这是一个未归一化高斯函数的积分，结果等于归一化系数的倒数，因此很容易计算。根据式（2.43）给出的归一化高斯分布形式，我们知道，该系数与均值无关，只依赖于协方差矩阵的行列式。因此，通过对 $\mathbf{x}_b$ 配方，可以把 $\mathbf{x}_b$ 积分消去；式（2.84）左侧各项所留下的、唯一依赖于 $\mathbf{x}_a$ 的项，就是该式右侧最后一项，其中 $\mathbf{m}$ 由式（2.85）给出。把这一项与式

<!-- pdf-page: 109 -->
<!-- join-previous-paragraph -->
（2.70）中其余依赖于 $\mathbf{x}_a$ 的项合并，得到

$$
\begin{aligned}
&\frac12[\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)]^{\mathrm T}\boldsymbol{\Lambda}_{bb}^{-1}[\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)]\\
&\quad-\frac12\mathbf{x}_a^{\mathrm T}\boldsymbol{\Lambda}_{aa}\mathbf{x}_a+\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a+\boldsymbol{\Lambda}_{ab}\boldsymbol{\mu}_b)+\text{const}\\
&=-\frac12\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})\mathbf{x}_a\\
&\quad+\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})^{-1}\boldsymbol{\mu}_a+\text{const}.
\end{aligned}
\tag{2.87}
$$

其中，“const” 表示与 $\mathbf{x}_a$ 无关的量。再次与式（2.71）比较，可知边缘分布 $p(\mathbf{x}_a)$ 的协方差为

$$
\boldsymbol{\Sigma}_a=(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})^{-1}.
\tag{2.88}
$$

类似地，均值为

$$
\boldsymbol{\Sigma}_a(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})\boldsymbol{\mu}_a=\boldsymbol{\mu}_a.
\tag{2.89}
$$

这里使用了式（2.88）。式（2.88）中的协方差，是用式（2.69）给出的分块精度矩阵表示的。与条件分布的处理一样，可以用式（2.67）给出的相应分块协方差矩阵重写它。这两组分块矩阵满足

$$
\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}^{-1}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}.
\tag{2.90}
$$

利用式（2.76），得到

$$
(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})^{-1}=\boldsymbol{\Sigma}_{aa}.
\tag{2.91}
$$

由此得到符合直觉的结果：边缘分布 $p(\mathbf{x}_a)$ 的均值和协方差为

$$
\mathbb{E}[\mathbf{x}_a]=\boldsymbol{\mu}_a,
\tag{2.92}
$$

$$
\operatorname{cov}[\mathbf{x}_a]=\boldsymbol{\Sigma}_{aa}.
\tag{2.93}
$$

可以看到，对于边缘分布，均值和协方差用分块协方差矩阵表示最简单；而对于条件分布，用分块精度矩阵则可以得到更简单的表达式。

分块高斯分布的边缘分布和条件分布结果汇总如下。

**分块高斯分布**

给定联合高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，其中 $\boldsymbol{\Lambda}\equiv\boldsymbol{\Sigma}^{-1}$，且

$$
\mathbf{x}=\begin{pmatrix}\mathbf{x}_a\\\mathbf{x}_b\end{pmatrix},\qquad\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\end{pmatrix},
\tag{2.94}
$$

<!-- pdf-page: 110 -->

$$
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix},\qquad\boldsymbol{\Lambda}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}.
\tag{2.95}
$$

条件分布：

$$
p(\mathbf{x}_a\mid\mathbf{x}_b)=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_{a\mid b},\boldsymbol{\Lambda}_{aa}^{-1}),
\tag{2.96}
$$

$$
\boldsymbol{\mu}_{a\mid b}=\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{aa}^{-1}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b).
\tag{2.97}
$$

边缘分布：

$$
p(\mathbf{x}_a)=\mathcal{N}(\mathbf{x}_a\mid\boldsymbol{\mu}_a,\boldsymbol{\Sigma}_{aa}).
\tag{2.98}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-9.png" alt="二维高斯等密度线以及一个变量的边缘分布和给定另一变量后的条件分布"><figcaption>图 2.9：左图显示两个变量的高斯分布 $p(x_a,x_b)$ 的等密度线；右图显示边缘分布 $p(x_a)$（蓝色曲线），以及给定 $x_b=0.7$ 时的条件分布 $p(x_a\mid x_b)$（红色曲线）。</figcaption></figure>

图 2.9 用一个涉及两个变量的例子，说明多元高斯分布的条件分布与边缘分布。

### 2.3.3 高斯变量的贝叶斯定理

在第 2.3.1 节和第 2.3.2 节中，我们考虑了高斯分布 $p(\mathbf{x})$，将向量 $\mathbf{x}$ 分成两个子向量 $\mathbf{x}=(\mathbf{x}_a,\mathbf{x}_b)$，然后求出了条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 和边缘分布 $p(\mathbf{x}_a)$ 的表达式。我们注意到，条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值是 $\mathbf{x}_b$ 的线性函数。这里假设给定一个高斯边缘分布 $p(\mathbf{x})$ 和一个高斯条件分布 $p(\mathbf{y}\mid\mathbf{x})$，其中 $p(\mathbf{y}\mid\mathbf{x})$ 的均值是 $\mathbf{x}$ 的线性函数，协方差与 $\mathbf{x}$ 无关。这是

<!-- pdf-page: 111 -->
<!-- join-previous-paragraph -->
线性高斯模型（Roweis and Ghahramani, 1999）的一个例子，第 8.1.4 节将作更一般的讨论。我们希望求出边缘分布 $p(\mathbf{y})$ 和条件分布 $p(\mathbf{x}\mid\mathbf{y})$。这是后续章节中经常出现的问题，因此在这里推导一般结果会很有用。

设边缘分布和条件分布分别为

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1}),
\tag{2.99}
$$

$$
p(\mathbf{y}\mid\mathbf{x})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\mathbf{x}+\mathbf{b},\mathbf{L}^{-1}).
\tag{2.100}
$$

其中，$\boldsymbol{\mu}$、$\mathbf{A}$ 和 $\mathbf{b}$ 是控制均值的参数，$\boldsymbol{\Lambda}$ 和 $\mathbf{L}$ 是精度矩阵。如果 $\mathbf{x}$ 的维数为 $M$，$\mathbf{y}$ 的维数为 $D$，则矩阵 $\mathbf{A}$ 的大小为 $D\times M$。

首先求出 $\mathbf{x}$ 和 $\mathbf{y}$ 的联合分布。为此，定义

$$
\mathbf{z}=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix},
\tag{2.101}
$$

再考察联合分布的对数：

$$
\begin{aligned}
\ln p(\mathbf{z})&=\ln p(\mathbf{x})+\ln p(\mathbf{y}\mid\mathbf{x})\\
&=-\frac12(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu})\\
&\quad-\frac12(\mathbf{y}-\mathbf{A}\mathbf{x}-\mathbf{b})^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{A}\mathbf{x}-\mathbf{b})+\text{const}.
\end{aligned}
\tag{2.102}
$$

其中，“const” 表示与 $\mathbf{x}$ 和 $\mathbf{y}$ 无关的项。与前面一样，这是 $\mathbf{z}$ 各分量的二次函数，因此 $p(\mathbf{z})$ 是高斯分布。为了求得这个高斯分布的精度，考察式（2.102）中的二次项，它们可以写成

$$
\begin{aligned}
&-\frac12\mathbf{x}^{\mathrm T}(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})\mathbf{x}-\frac12\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{y}+\frac12\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{A}\mathbf{x}+\frac12\mathbf{x}^{\mathrm T}\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{y}\\
&=-\frac12\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}^{\mathrm T}\begin{pmatrix}\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A}&-\mathbf{A}^{\mathrm T}\mathbf{L}\\-\mathbf{L}\mathbf{A}&\mathbf{L}\end{pmatrix}\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}=-\frac12\mathbf{z}^{\mathrm T}\mathbf{R}\mathbf{z}.
\end{aligned}
\tag{2.103}
$$

因此，$\mathbf{z}$ 上的高斯分布的精度矩阵，即逆协方差矩阵，为

$$
\mathbf{R}=\begin{pmatrix}\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A}&-\mathbf{A}^{\mathrm T}\mathbf{L}\\-\mathbf{L}\mathbf{A}&\mathbf{L}\end{pmatrix}.
\tag{2.104}
$$

对精度矩阵求逆即可得到协方差矩阵。利用矩阵求逆公式（2.76），得到 <span class="margin-reference">习题 2.29</span>

$$
\operatorname{cov}[\mathbf{z}]=\mathbf{R}^{-1}=\begin{pmatrix}\boldsymbol{\Lambda}^{-1}&\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}\\\mathbf{A}\boldsymbol{\Lambda}^{-1}&\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}\end{pmatrix}.
\tag{2.105}
$$

<!-- pdf-page: 112 -->

类似地，找出式（2.102）中的一次项，就能求得 $\mathbf{z}$ 上高斯分布的均值。这些一次项为

$$
\mathbf{x}^{\mathrm T}\boldsymbol{\Lambda}\boldsymbol{\mu}-\mathbf{x}^{\mathrm T}\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}+\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{b}=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}^{\mathrm T}\begin{pmatrix}\boldsymbol{\Lambda}\boldsymbol{\mu}-\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}\\\mathbf{L}\mathbf{b}\end{pmatrix}.
\tag{2.106}
$$

利用前面对多元高斯二次型配方得到的结果（2.71），可知 $\mathbf{z}$ 的均值为

$$
\mathbb{E}[\mathbf{z}]=\mathbf{R}^{-1}\begin{pmatrix}\boldsymbol{\Lambda}\boldsymbol{\mu}-\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}\\\mathbf{L}\mathbf{b}\end{pmatrix}.
\tag{2.107}
$$

利用式（2.105），得到 <span class="margin-reference">习题 2.30</span>

$$
\mathbb{E}[\mathbf{z}]=\begin{pmatrix}\boldsymbol{\mu}\\\mathbf{A}\boldsymbol{\mu}+\mathbf{b}\end{pmatrix}.
\tag{2.108}
$$

接着求边缘分布 $p(\mathbf{y})$，即对 $\mathbf{x}$ 进行边缘化。回顾前面的结果：高斯随机向量的部分分量的边缘分布，用分块协方差矩阵表达时具有特别简单的形式。<span class="margin-reference">第 2.3 节</span> 具体来说，均值和协方差分别由式（2.92）和式（2.93）给出。利用式（2.105）和式（2.108），可得边缘分布 $p(\mathbf{y})$ 的均值和协方差为

$$
\mathbb{E}[\mathbf{y}]=\mathbf{A}\boldsymbol{\mu}+\mathbf{b},
\tag{2.109}
$$

$$
\operatorname{cov}[\mathbf{y}]=\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}.
\tag{2.110}
$$

这个结果的一个特例是 $\mathbf{A}=\mathbf{I}$，此时退化为两个高斯分布的卷积。可以看到，卷积的均值是两个高斯分布均值之和，卷积的协方差则是它们的协方差之和。

最后求条件分布 $p(\mathbf{x}\mid\mathbf{y})$。回顾式（2.73）和式（2.75），条件分布的结果用分块精度矩阵表达最方便。<span class="margin-reference">第 2.3 节</span> 将这些结果用于式（2.105）和式（2.108），可以得到条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 的均值和协方差：

$$
\mathbb{E}[\mathbf{x}\mid\mathbf{y}]=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}\{\mathbf{A}^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda}\boldsymbol{\mu}\},
\tag{2.111}
$$

$$
\operatorname{cov}[\mathbf{x}\mid\mathbf{y}]=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}.
\tag{2.112}
$$

求取这个条件分布，可以看作应用贝叶斯定理的一个例子。可以把分布 $p(\mathbf{x})$ 解释为 $\mathbf{x}$ 上的先验分布。如果观测到了变量 $\mathbf{y}$，那么条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 就表示相应的 $\mathbf{x}$ 后验分布。求出边缘分布和条件分布后，实际上就把联合分布 $p(\mathbf{z})=p(\mathbf{x})p(\mathbf{y}\mid\mathbf{x})$ 改写成了 $p(\mathbf{x}\mid\mathbf{y})p(\mathbf{y})$。下面汇总这些结果。

<!-- pdf-page: 113 -->

**边缘高斯分布与条件高斯分布**

给定 $\mathbf{x}$ 的高斯边缘分布，以及给定 $\mathbf{x}$ 时 $\mathbf{y}$ 的高斯条件分布：

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1}),
\tag{2.113}
$$

$$
p(\mathbf{y}\mid\mathbf{x})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\mathbf{x}+\mathbf{b},\mathbf{L}^{-1}),
\tag{2.114}
$$

则 $\mathbf{y}$ 的边缘分布，以及给定 $\mathbf{y}$ 时 $\mathbf{x}$ 的条件分布，为

$$
p(\mathbf{y})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\boldsymbol{\mu}+\mathbf{b},\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}),
\tag{2.115}
$$

$$
p(\mathbf{x}\mid\mathbf{y})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\Sigma}\{\mathbf{A}^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda}\boldsymbol{\mu}\},\boldsymbol{\Sigma}),
\tag{2.116}
$$

其中

$$
\boldsymbol{\Sigma}=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}.
\tag{2.117}
$$

### 2.3.4 高斯分布的最大似然估计

给定数据集 $\mathbf{X}=(\mathbf{x}_1,\ldots,\mathbf{x}_N)^{\mathrm T}$，假设观测 $\{\mathbf{x}_n\}$ 独立地取自多元高斯分布，就可以用最大似然估计该分布的参数。对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})=-\frac{ND}{2}\ln(2\pi)-\frac{N}{2}\ln|\boldsymbol{\Sigma}|-\frac12\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}).
\tag{2.118}
$$

简单整理后，可以看出似然函数仅通过下面两个量依赖于数据集：

$$
\sum_{n=1}^{N}\mathbf{x}_n,\qquad\sum_{n=1}^{N}\mathbf{x}_n\mathbf{x}_n^{\mathrm T}.
\tag{2.119}
$$

它们称为高斯分布的充分统计量。利用式（C.19），对数似然对 $\boldsymbol{\mu}$ 的导数为 <span class="margin-reference">附录 C</span>

$$
\frac{\partial}{\partial\boldsymbol{\mu}}\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})=\sum_{n=1}^{N}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}).
\tag{2.120}
$$

令该导数为零，得到均值的最大似然估计：

$$
\boldsymbol{\mu}_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n.
\tag{2.121}
$$

<!-- pdf-page: 114 -->

它就是观测数据点的均值。对 $\boldsymbol{\Sigma}$ 最大化式（2.118）则更复杂一些。最简单的方法是先忽略对称性约束，再证明得到的解确实具有所要求的对称性。<span class="margin-reference">习题 2.34</span> 显式施加对称性和正定性约束的其他推导方法，可见 Magnus and Neudecker（1999）。结果符合预期，其形式为

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})^{\mathrm T}.
\tag{2.122}
$$

其中含有 $\boldsymbol{\mu}_{\mathrm{ML}}$，因为这是同时对 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 最大化的结果。注意，$\boldsymbol{\mu}_{\mathrm{ML}}$ 的解（2.121）并不依赖于 $\boldsymbol{\Sigma}_{\mathrm{ML}}$，因此可以先求 $\boldsymbol{\mu}_{\mathrm{ML}}$，再利用它求 $\boldsymbol{\Sigma}_{\mathrm{ML}}$。

在真实分布下，计算最大似然解的期望，得到 <span class="margin-reference">习题 2.35</span>

$$
\mathbb{E}[\boldsymbol{\mu}_{\mathrm{ML}}]=\boldsymbol{\mu},
\tag{2.123}
$$

$$
\mathbb{E}[\boldsymbol{\Sigma}_{\mathrm{ML}}]=\frac{N-1}{N}\boldsymbol{\Sigma}.
\tag{2.124}
$$

可以看到，均值的最大似然估计的期望等于真实均值。但协方差的最大似然估计的期望小于真实值，因此它是有偏的。可以定义另一个估计量 $\widetilde{\boldsymbol{\Sigma}}$ 来修正这一偏差：

$$
\widetilde{\boldsymbol{\Sigma}}=\frac{1}{N-1}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})^{\mathrm T}.
\tag{2.125}
$$

由式（2.122）和式（2.124）显然可知，$\widetilde{\boldsymbol{\Sigma}}$ 的期望等于 $\boldsymbol{\Sigma}$。

### 2.3.5 序贯估计

前面对高斯分布参数最大似然解的讨论，为我们提供了一个方便的机会，来更一般地讨论最大似然的序贯估计。序贯方法允许每次处理一个数据点，然后将其丢弃。它们对于在线应用非常重要；对于大数据集也很重要，因为一次性批量处理所有数据点可能无法实现。

考虑均值 $\boldsymbol{\mu}_{\mathrm{ML}}$ 的最大似然估计量（2.121）。当它基于 $N$ 个观测时，记作 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$。如果

<!-- pdf-page: 115 -->
<!-- join-previous-paragraph -->
把最后一个数据点 $\mathbf{x}_N$ 的贡献单独拆出来，就得到

$$
\begin{aligned}
\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}&=\frac1N\sum_{n=1}^{N}\mathbf{x}_n\\
&=\frac1N\mathbf{x}_N+\frac1N\sum_{n=1}^{N-1}\mathbf{x}_n\\
&=\frac1N\mathbf{x}_N+\frac{N-1}{N}\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}\\
&=\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}+\frac1N(\mathbf{x}_N-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}).
\end{aligned}
\tag{2.126}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-10.png" alt="回归函数及其与横轴的交点，示意序贯求根问题"><figcaption>图 2.10：两个相关随机变量 $z$ 和 $\theta$ 的示意图，以及由条件期望 $\mathbb{E}[z\mid\theta]$ 定义的回归函数 $f(\theta)$。Robbins-Monro 算法为求这类函数的根 $\theta^{\star}$ 提供了一般的序贯过程。</figcaption></figure>

这个结果有一个很直观的解释：观测到 $N-1$ 个数据点后，已经用 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}$ 估计了 $\boldsymbol{\mu}$。现在观测到数据点 $\mathbf{x}_N$，沿“误差信号” $(\mathbf{x}_N-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)})$ 的方向，把旧估计移动一个与 $1/N$ 成正比的小量，就得到更新的估计 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$。注意，随着 $N$ 增大，后续数据点的贡献会越来越小。

结果（2.126）显然会给出与批量结果（2.121）相同的答案，因为两个公式等价。然而，并不总能通过这条途径推导序贯算法，因此需要更一般的序贯学习形式，这就引出了 Robbins-Monro 算法。考虑由联合分布 $p(z,\theta)$ 决定的两个随机变量 $\theta$ 和 $z$。给定 $\theta$ 时 $z$ 的条件期望，定义了一个确定性函数 $f(\theta)$：

$$
f(\theta)\equiv\mathbb{E}[z\mid\theta]=\int zp(z\mid\theta)\,\mathrm{d}z.
\tag{2.127}
$$

图 2.10 给出了示意。以这种方式定义的函数称为回归函数（regression function）。

我们的目标是找到满足 $f(\theta^{\star})=0$ 的根 $\theta^{\star}$。如果有一个由 $z$ 和 $\theta$ 的观测组成的大数据集，就可以直接对回归函数建模，再估计其根。但假设每次只观测一个 $z$ 值，希望找到相应的 $\theta^{\star}$ 序贯估计方法。针对这类问题，下面的一般过程由

<!-- pdf-page: 116 -->
<!-- join-previous-paragraph -->
Robbins and Monro（1951）提出。假设 $z$ 的条件方差有限，即

$$
\mathbb{E}[(z-f)^2\mid\theta]<\infty.
\tag{2.128}
$$

另外，不失一般性，考虑与图 2.10 一致的情形：当 $\theta>\theta^{\star}$ 时，$f(\theta)>0$；当 $\theta<\theta^{\star}$ 时，$f(\theta)<0$。于是，Robbins-Monro 过程定义了根 $\theta^{\star}$ 的一系列相继估计：

$$
\theta^{(N)}=\theta^{(N-1)}+a_{N-1}z(\theta^{(N-1)}).
\tag{2.129}
$$

这里，$z(\theta^{(N)})$ 是 $\theta$ 取值 $\theta^{(N)}$ 时 $z$ 的一个观测值。系数 $\{a_N\}$ 是一列正数，满足

$$
\lim_{N\to\infty}a_N=0,
\tag{2.130}
$$

$$
\sum_{N=1}^{\infty}a_N=\infty,
\tag{2.131}
$$

$$
\sum_{N=1}^{\infty}a_N^2<\infty.
\tag{2.132}
$$

可以证明（Robbins and Monro, 1951；Fukunaga, 1990），式（2.129）给出的估计序列确实以概率 1 收敛到根。注意，第一个条件（2.130）保证相继修正的幅度逐渐减小，从而使过程可以收敛到一个极限值。第二个条件（2.131）保证算法不会在尚未到达根的位置就停止前进；第三个条件（2.132）保证累积噪声的方差有限，从而不破坏收敛。

现在考虑如何用 Robbins-Monro 算法，序贯地解决一般的最大似然问题。由定义可知，最大似然解 $\theta_{\mathrm{ML}}$ 是对数似然函数的驻点，因此满足

$$
\left.\frac{\partial}{\partial\theta}\left\{\frac1N\sum_{n=1}^{N}\ln p(x_n\mid\theta)\right\}\right|_{\theta_{\mathrm{ML}}}=0.
\tag{2.133}
$$

交换求导和求和的次序，并取极限 $N\to\infty$，得到

$$
\lim_{N\to\infty}\frac1N\sum_{n=1}^{N}\frac{\partial}{\partial\theta}\ln p(x_n\mid\theta)=\mathbb{E}_x\left[\frac{\partial}{\partial\theta}\ln p(x\mid\theta)\right].
\tag{2.134}
$$

因此，求最大似然解就对应于求某个回归函数的根。于是可以应用 Robbins-Monro 过程，其形式变为

$$
\theta^{(N)}=\theta^{(N-1)}+a_{N-1}\frac{\partial}{\partial\theta^{(N-1)}}\ln p(x_N\mid\theta^{(N-1)}).
\tag{2.135}
$$

<!-- pdf-page: 117 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-11.png" alt="高斯均值估计对应的线性回归函数及随机导数的条件分布"><figcaption>图 2.11：对于高斯分布，当 $\theta$ 对应于均值 $\mu$ 时，图 2.10 中的回归函数为一条直线，如红线所示。此时，随机变量 $z$ 对应于对数似然函数的导数，等于 $(x-\mu_{\mathrm{ML}})/\sigma^2$；定义回归函数的期望则为直线 $(\mu-\mu_{\mathrm{ML}})/\sigma^2$。回归函数的根对应于最大似然估计量 $\mu_{\mathrm{ML}}$。</figcaption></figure>

作为具体例子，再次考虑高斯分布均值的序贯估计。此时，参数 $\theta^{(N)}$ 是高斯均值的估计 $\mu_{\mathrm{ML}}^{(N)}$，随机变量 $z$ 为

$$
z=\frac{\partial}{\partial\mu_{\mathrm{ML}}}\ln p(x\mid\mu_{\mathrm{ML}},\sigma^2)=\frac1{\sigma^2}(x-\mu_{\mathrm{ML}}).
\tag{2.136}
$$

因此，$z$ 的分布是均值为 $\mu-\mu_{\mathrm{ML}}$ 的高斯分布，如图 2.11 所示。把式（2.136）代入式（2.135），只要选择系数 $a_N=\sigma^2/N$，就能得到式（2.126）的一元形式。注意，虽然这里集中讨论了单变量情形，但相同的方法，以及对系数 $a_N$ 的相同限制（2.130）至（2.132），也同样适用于多元情形（Blum, 1965）。

### 2.3.6 高斯分布的贝叶斯推断

最大似然框架给出了参数 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 的点估计。现在通过为这些参数引入先验分布，建立贝叶斯处理方法。先从一个简单例子开始，考虑单个高斯随机变量 $x$。假设方差 $\sigma^2$ 已知，任务是在给定 $N$ 个观测 $\mathbf{X}=\{x_1,\ldots,x_N\}$ 的条件下推断均值 $\mu$。似然函数，即给定 $\mu$ 时观测数据的概率，并将其看作 $\mu$ 的函数，为

$$
p(\mathbf{X}\mid\mu)=\prod_{n=1}^{N}p(x_n\mid\mu)=\frac1{(2\pi\sigma^2)^{N/2}}\exp\left\{-\frac1{2\sigma^2}\sum_{n=1}^{N}(x_n-\mu)^2\right\}.
\tag{2.137}
$$

再次强调，似然函数 $p(\mathbf{X}\mid\mu)$ 不是 $\mu$ 上的概率分布，也没有归一化。

可以看到，似然函数是 $\mu$ 的二次型的指数。因此，如果选择高斯先验 $p(\mu)$，它就是这个似然函数的

<!-- pdf-page: 118 -->
<!-- join-previous-paragraph -->
共轭分布，因为相应的后验是两个关于 $\mu$ 的二次函数的指数的乘积，所以也将是高斯分布。因此，取先验分布为

$$
p(\mu)=\mathcal{N}(\mu\mid\mu_0,\sigma_0^2),
\tag{2.138}
$$

则后验分布为

$$
p(\mu\mid\mathbf{X})\propto p(\mathbf{X}\mid\mu)p(\mu).
\tag{2.139}
$$

对指数中的表达式作简单配方，可以得到后验分布 <span class="margin-reference">习题 2.38</span>

$$
p(\mu\mid\mathbf{X})=\mathcal{N}(\mu\mid\mu_N,\sigma_N^2).
\tag{2.140}
$$

其中，

$$
\mu_N=\frac{\sigma^2}{N\sigma_0^2+\sigma^2}\mu_0+\frac{N\sigma_0^2}{N\sigma_0^2+\sigma^2}\mu_{\mathrm{ML}},
\tag{2.141}
$$

$$
\frac1{\sigma_N^2}=\frac1{\sigma_0^2}+\frac N{\sigma^2}.
\tag{2.142}
$$

这里，$\mu_{\mathrm{ML}}$ 是 $\mu$ 的最大似然解，由样本均值给出：

$$
\mu_{\mathrm{ML}}=\frac1N\sum_{n=1}^{N}x_n.
\tag{2.143}
$$

值得花一点时间研究后验均值和方差的形式。首先，式（2.141）给出的后验均值，是先验均值 $\mu_0$ 与最大似然解 $\mu_{\mathrm{ML}}$ 之间的折中。如果观测数据点数目 $N=0$，式（2.141）就如预期那样退化为先验均值。当 $N\to\infty$ 时，后验均值就是最大似然解。类似地，考察后验分布方差的结果（2.142）。可以看到，用方差的倒数，即精度，来表示最为自然。而且精度可以相加：后验精度等于先验精度，再加上每个观测数据点各自贡献的一份数据精度。随着观测数据点增多，精度持续增大，对应的后验方差持续减小。没有观测数据时，得到先验方差；而当数据点数目 $N\to\infty$ 时，方差 $\sigma_N^2$ 趋于零，后验分布在最大似然解附近形成无限尖锐的峰。因此，在观测次数无限多的极限下，贝叶斯形式精确地恢复了式（2.143）给出的 $\mu$ 的最大似然点估计。还应注意，对于有限 $N$，若取极限 $\sigma_0^2\to\infty$，即先验具有无穷大方差，则后验均值（2.141）退化为最大似然结果，而由式（2.142）可知，后验方差为 $\sigma_N^2=\sigma^2/N$。

<!-- pdf-page: 119 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-12.png" alt="已知方差时，对高斯均值的先验和不同样本数下的后验曲线"><figcaption>图 2.12：在方差已知的条件下，对高斯分布均值 $\mu$ 进行贝叶斯推断。图中显示了 $\mu$ 的先验分布（标为 $N=0$ 的曲线），这里它本身也是高斯分布；同时显示了数据点数目 $N$ 增加时，式（2.140）给出的后验分布。数据点由均值为 0.8、方差为 0.1 的高斯分布生成，先验均值取 0。先验与似然函数中的方差，都设为真实方差值。</figcaption></figure>

图 2.12 展示了对高斯均值进行贝叶斯推断的分析结果。将这一结果推广到协方差已知、均值未知的 $D$ 维高斯随机变量 $\mathbf{x}$，是直接的。<span class="margin-reference">习题 2.40</span>

前面已经看到，高斯均值的最大似然表达式可以改写为序贯更新公式：观测 $N$ 个数据点后的均值，由观测 $N-1$ 个数据点后的均值，加上数据点 $\mathbf{x}_N$ 的贡献来表示。<span class="margin-reference">第 2.3.5 节</span> 事实上，贝叶斯框架很自然地引出了推断问题的序贯观点。以高斯均值的推断为例，将最后一个数据点 $x_N$ 的贡献单独分离，后验分布可以写成

$$
p(\mu\mid\mathcal{D})\propto\left[p(\mu)\prod_{n=1}^{N-1}p(x_n\mid\mu)\right]p(x_N\mid\mu).
\tag{2.144}
$$

方括号内的项，除归一化系数外，正是观测 $N-1$ 个数据点之后的后验分布。可以把它看作先验，再利用贝叶斯定理，与数据点 $x_N$ 对应的似然函数结合，得到观测 $N$ 个数据点之后的后验分布。这种序贯的贝叶斯推断观点十分普遍，适用于任何假设观测数据独立同分布的问题。

到目前为止，我们一直假设数据所服从的高斯分布方差已知，目标是推断均值。现在反过来，假设均值已知，希望推断方差。同样，选择共轭形式的先验分布，可以大幅简化计算。使用精度 $\lambda\equiv1/\sigma^2$ 最为方便。关于 $\lambda$ 的似然函数形式为

$$
p(\mathbf{X}\mid\lambda)=\prod_{n=1}^{N}\mathcal{N}(x_n\mid\mu,\lambda^{-1})\propto\lambda^{N/2}\exp\left\{-\frac\lambda2\sum_{n=1}^{N}(x_n-\mu)^2\right\}.
\tag{2.145}
$$

<!-- pdf-page: 120 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/a-fig-2-13.png" alt="三组参数下的伽马分布，展示不同的衰减和单峰形状"><figcaption>图 2.13：参数 $a$ 和 $b$ 取不同值时，式（2.146）定义的伽马分布 $\operatorname{Gam}(\lambda\mid a,b)$ 的曲线。</figcaption></figure>

因此，相应的共轭先验应当正比于 $\lambda$ 的幂与 $\lambda$ 的线性函数的指数之乘积。这对应于伽马分布（gamma distribution），定义为

$$
\operatorname{Gam}(\lambda\mid a,b)=\frac1{\Gamma(a)}b^a\lambda^{a-1}\exp(-b\lambda).
\tag{2.146}
$$

这里，$\Gamma(a)$ 是式（1.141）定义的伽马函数，它保证式（2.146）正确归一化。<span class="margin-reference">习题 2.41</span> 当 $a>0$ 时，伽马分布的积分有限；当 $a\geqslant1$ 时，分布本身有界。图 2.13 绘出了 $a$ 和 $b$ 取不同值时的分布。伽马分布的均值和方差为 <span class="margin-reference">习题 2.42</span>

$$
\mathbb{E}[\lambda]=\frac ab,
\tag{2.147}
$$

$$
\operatorname{var}[\lambda]=\frac a{b^2}.
\tag{2.148}
$$

考虑先验分布 $\operatorname{Gam}(\lambda\mid a_0,b_0)$。将它乘以似然函数（2.145），得到后验分布

$$
p(\lambda\mid\mathbf{X})\propto\lambda^{a_0-1}\lambda^{N/2}\exp\left\{-b_0\lambda-\frac\lambda2\sum_{n=1}^{N}(x_n-\mu)^2\right\}.
\tag{2.149}
$$

可以认出，它是形如 $\operatorname{Gam}(\lambda\mid a_N,b_N)$ 的伽马分布，其中

$$
a_N=a_0+\frac N2,
\tag{2.150}
$$

$$
b_N=b_0+\frac12\sum_{n=1}^{N}(x_n-\mu)^2=b_0+\frac N2\sigma_{\mathrm{ML}}^2.
\tag{2.151}
$$

这里，$\sigma_{\mathrm{ML}}^2$ 是方差的最大似然估计量。注意，在式（2.149）中，无须保留先验和似然函数的归一化常数；如果需要，可以在最后利用伽马分布的归一化形式（2.146）求出正确的系数。

<!-- pdf-page: 121 -->

由式（2.150）可知，观测 $N$ 个数据点的作用，是把系数 $a$ 增加 $N/2$。因此，可以把先验中的参数 $a_0$ 解释为 $2a_0$ 次“有效”先验观测。类似地，由式（2.151）可知，$N$ 个数据点为参数 $b$ 贡献了 $N\sigma_{\mathrm{ML}}^2/2$，其中 $\sigma_{\mathrm{ML}}^2$ 是方差。因此，可以把先验中的参数 $b_0$ 理解为来自 $2a_0$ 次“有效”先验观测，其方差为 $2b_0/(2a_0)=b_0/a_0$。回顾前面，我们曾对狄利克雷先验作过类似解释。<span class="margin-reference">第 2.2 节</span> 这些分布都属于指数族；后面会看到，对于指数族分布，用有效的虚构数据点解释共轭先验，是一种普遍适用的解释。

除了使用精度，也可以直接考虑方差本身。这时的共轭先验称为逆伽马分布（inverse gamma distribution）。不过我们不再深入讨论，因为使用精度更方便。

现在假设均值和精度都未知。为寻找共轭先验，考察似然函数对 $\mu$ 和 $\lambda$ 的依赖：

$$
\begin{aligned}
p(\mathbf{X}\mid\mu,\lambda)&=\prod_{n=1}^{N}\left(\frac\lambda{2\pi}\right)^{1/2}\exp\left\{-\frac\lambda2(x_n-\mu)^2\right\}\\
&\propto\left[\lambda^{1/2}\exp\left(-\frac{\lambda\mu^2}{2}\right)\right]^N\exp\left\{\lambda\mu\sum_{n=1}^{N}x_n-\frac\lambda2\sum_{n=1}^{N}x_n^2\right\}.
\end{aligned}
\tag{2.152}
$$

现在希望找出一个先验分布 $p(\mu,\lambda)$，使它对 $\mu$ 和 $\lambda$ 的函数依赖与似然函数相同，因此它应当具有如下形式：

$$
\begin{aligned}
p(\mu,\lambda)&\propto\left[\lambda^{1/2}\exp\left(-\frac{\lambda\mu^2}{2}\right)\right]^{\beta}\exp\{c\lambda\mu-d\lambda\}\\
&=\exp\left\{-\frac{\beta\lambda}{2}(\mu-c/\beta)^2\right\}\lambda^{\beta/2}\exp\left\{-\left(d-\frac{c^2}{2\beta}\right)\lambda\right\}.
\end{aligned}
\tag{2.153}
$$

其中，$c$、$d$ 和 $\beta$ 为常量。由于总可以写成 $p(\mu,\lambda)=p(\mu\mid\lambda)p(\lambda)$，观察表达式就能找出 $p(\mu\mid\lambda)$ 和 $p(\lambda)$。具体来说，$p(\mu\mid\lambda)$ 是高斯分布，其精度是 $\lambda$ 的线性函数；而 $p(\lambda)$ 是伽马分布。因此，归一化后的先验形式为

$$
p(\mu,\lambda)=\mathcal{N}(\mu\mid\mu_0,(\beta\lambda)^{-1})\operatorname{Gam}(\lambda\mid a,b).
\tag{2.154}
$$

其中定义了新的常量 $\mu_0=c/\beta$、$a=1+\beta/2$、$b=d-c^2/2\beta$。分布（2.154）称为正态-伽马（normal-gamma）或高斯-伽马（Gaussian-gamma）分布，图 2.14 绘出了它的形状。注意，它并不是一个独立的 $\mu$ 高斯先验与一个 $\lambda$ 伽马先验的简单乘积，因为 $\mu$ 的精度是 $\lambda$ 的线性函数。即使选择了一个使 $\mu$ 和 $\lambda$ 相互独立的先验，后验分布仍然会表现出 $\mu$ 的精度与 $\lambda$ 的值之间的联系。

<!-- pdf-page: 122 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-14.png" alt="正态-伽马分布的等高线图"><figcaption>图 2.14：正态-伽马分布（2.154）的等高线图，参数取值为 $\mu_0=0$、$\beta=2$、$a=5$、$b=6$。</figcaption><p class="figure-translation">$\mu$ 为均值参数，$\lambda$ 为精度参数。</p></figure>

对于 $D$ 维变量 $\mathbf{x}$ 的多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1})$，假设精度已知，则均值 $\boldsymbol{\mu}$ 的共轭先验仍然是高斯分布。对于均值已知、精度矩阵 $\boldsymbol{\Lambda}$ 未知的情况，共轭先验是 *Wishart 分布*（习题 2.45）：

$$
\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu)=B|\boldsymbol{\Lambda}|^{(\nu-D-1)/2}\exp\left(-\frac12\operatorname{Tr}(\mathbf{W}^{-1}\boldsymbol{\Lambda})\right),
\tag{2.155}
$$

其中 $\nu$ 称为分布的*自由度*（degrees of freedom），$\mathbf{W}$ 为 $D\times D$ 的尺度矩阵，$\operatorname{Tr}(\cdot)$ 表示迹。归一化常数 $B$ 为

$$
B(\mathbf{W},\nu)=|\mathbf{W}|^{-\nu/2}\left(2^{\nu D/2}\pi^{D(D-1)/4}\prod_{i=1}^{D}\Gamma\left(\frac{\nu+1-i}{2}\right)\right)^{-1}.
\tag{2.156}
$$

同样，也可以直接在协方差矩阵上定义共轭先验，而不在精度矩阵上定义，这就得到*逆 Wishart 分布*，不过这里不再深入讨论。如果均值和精度均未知，那么沿用与一元情形相似的推理，共轭先验为

$$
p(\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\boldsymbol{\mu}_0,\beta,\mathbf{W},\nu)=\mathcal{N}(\boldsymbol{\mu}\mid\boldsymbol{\mu}_0,(\beta\boldsymbol{\Lambda})^{-1})\,\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu),
\tag{2.157}
$$

称为*正态 Wishart 分布*（normal-Wishart distribution），也称*高斯 Wishart 分布*（Gaussian-Wishart distribution）。

### 2.3.7 Student t 分布

我们已经看到，高斯分布精度的共轭先验是伽马分布（第 2.3.6 节）。如果有一元高斯分布 $\mathcal{N}(x\mid\mu,\tau^{-1})$ 及伽马先验 $\operatorname{Gam}(\tau\mid a,b)$，并将精度积分消去，就得到如下形式的 $x$ 的边缘分布（习题 2.46）：

<!-- pdf-page: 123 -->

$$
\begin{aligned}
p(x\mid\mu,a,b)
&=\int_0^{\infty}\mathcal{N}(x\mid\mu,\tau^{-1})\operatorname{Gam}(\tau\mid a,b)\,\mathrm{d}\tau\\
&=\int_0^{\infty}\frac{b^a e^{-b\tau}\tau^{a-1}}{\Gamma(a)}\left(\frac{\tau}{2\pi}\right)^{1/2}\exp\left\{-\frac{\tau}{2}(x-\mu)^2\right\}\,\mathrm{d}\tau\\
&=\frac{b^a}{\Gamma(a)}\left(\frac1{2\pi}\right)^{1/2}\left[b+\frac{(x-\mu)^2}{2}\right]^{-a-1/2}\Gamma(a+1/2),
\end{aligned}
\tag{2.158}
$$

其中作了变量代换 $z=\tau[b+(x-\mu)^2/2]$。按照惯例，定义新参数 $\nu=2a$ 和 $\lambda=a/b$，则分布 $p(x\mid\mu,a,b)$ 可以写成

$$
\operatorname{St}(x\mid\mu,\lambda,\nu)=\frac{\Gamma(\nu/2+1/2)}{\Gamma(\nu/2)}\left(\frac{\lambda}{\pi\nu}\right)^{1/2}\left[1+\frac{\lambda(x-\mu)^2}{\nu}\right]^{-\nu/2-1/2},
\tag{2.159}
$$

称为 *Student t 分布*。参数 $\lambda$ 有时称为 t 分布的*精度*，尽管一般而言，它并不等于方差的倒数。参数 $\nu$ 称为*自由度*，其作用如图 2.15 所示。在 $\nu=1$ 的特殊情况下，t 分布退化为*柯西分布*（Cauchy distribution）；在 $\nu\to\infty$ 的极限下，t 分布 $\operatorname{St}(x\mid\mu,\lambda,\nu)$ 变为均值 $\mu$、精度 $\lambda$ 的高斯分布 $\mathcal{N}(x\mid\mu,\lambda^{-1})$（习题 2.47）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-15.png" alt="不同自由度的Student t分布曲线及高斯极限"><figcaption>图 2.15：$\mu=0$、$\lambda=1$ 时，不同 $\nu$ 值下的 Student t 分布（2.159）。极限 $\nu\to\infty$ 对应均值为 $\mu$、精度为 $\lambda$ 的高斯分布。</figcaption><p class="figure-translation">$\nu\to\infty$、$\nu=1.0$、$\nu=0.1$ 分别标示绿色、蓝色与红色曲线。</p></figure>

由式（2.158）可见，Student t 分布是将无穷多个均值相同、精度不同的高斯分布相加而得到的。这可以解释为高斯分布的无穷混合（第 2.3.9 节将详细讨论高斯混合）。得到的分布通常比高斯分布有更长的“尾部”，如图 2.15 所示。这使 t 分布具有一个重要性质，称为*鲁棒性*（robustness）：与高斯分布相比，它对少量离群数据点的存在不那么敏感。图 2.16 比较了高斯分布和 t 分布的最大似然解，以说明 t 分布的鲁棒性。注意，t 分布的最大似然解可以用期望最大化（EM）算法求得（习题 12.24）。这里可以看到，少量

<!-- pdf-page: 124 -->
<!-- join-previous-paragraph -->
离群点对 t 分布的影响，远小于对高斯分布的影响。在实际应用中，离群点的产生可能是因为数据生成过程对应一个重尾分布，也可能仅仅是因为数据标注错误。鲁棒性对于回归问题同样重要。最小二乘回归不具备鲁棒性，这并不意外，因为它对应于（条件）高斯分布下的最大似然。如果以 t 分布这类重尾分布为基础建立回归模型，就能得到更鲁棒的模型。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-16.png" alt="加入三个离群点前后高斯分布和Student t分布最大似然拟合对比"><figcaption>图 2.16：Student t 分布相对于高斯分布的鲁棒性。（a）从高斯分布中抽取的 30 个数据点的直方图，以及 t 分布（红线）和高斯分布（绿线，大部分被红线遮住）的最大似然拟合。由于 t 分布包含高斯分布这一特例，它给出的解与高斯分布几乎相同。（b）在同一数据集中额外加入三个离群点。高斯分布（绿线）受到离群点的强烈影响而变形，t 分布（红线）则基本不受影响。</figcaption><p class="figure-translation">（a）原数据集；（b）增加三个离群点的数据集。</p></figure>

回到式（2.158），代入另一组参数 $\nu=2a$、$\lambda=a/b$、$\eta=\tau b/a$，可以将 t 分布写成

$$
\operatorname{St}(x\mid\mu,\lambda,\nu)=\int_0^{\infty}\mathcal{N}(x\mid\mu,(\eta\lambda)^{-1})\operatorname{Gam}(\eta\mid\nu/2,\nu/2)\,\mathrm{d}\eta.
\tag{2.160}
$$

然后将其推广到多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda})$，得到相应的多元 Student t 分布：

$$
\operatorname{St}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda},\nu)=\int_0^{\infty}\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},(\eta\boldsymbol{\Lambda})^{-1})\operatorname{Gam}(\eta\mid\nu/2,\nu/2)\,\mathrm{d}\eta.
\tag{2.161}
$$

采用与一元情形相同的方法，可以算出这一积分（习题 2.48）：

<!-- pdf-page: 125 -->

$$
\operatorname{St}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda},\nu)=\frac{\Gamma(D/2+\nu/2)}{\Gamma(\nu/2)}\frac{|\boldsymbol{\Lambda}|^{1/2}}{(\pi\nu)^{D/2}}\left[1+\frac{\Delta^2}{\nu}\right]^{-D/2-\nu/2},
\tag{2.162}
$$

其中 $D$ 为 $\mathbf{x}$ 的维数，$\Delta^2$ 为马氏距离的平方，定义为

$$
\Delta^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu}).
\tag{2.163}
$$

这是 Student t 分布的多元形式，满足以下性质（习题 2.49）：

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu},\qquad\text{若 }\nu>1,
\tag{2.164}
$$

$$
\operatorname{cov}[\mathbf{x}]=\frac{\nu}{\nu-2}\boldsymbol{\Lambda}^{-1},\qquad\text{若 }\nu>2,
\tag{2.165}
$$

$$
\operatorname{mode}[\mathbf{x}]=\boldsymbol{\mu}.
\tag{2.166}
$$

一元情形也有相应的结果。

### 2.3.8 周期变量

无论直接使用高斯分布，还是将它作为更复杂概率模型的组成部分，它都具有很大的实际意义。但在某些情形下，高斯分布并不适合用作连续变量的密度模型。实际应用中的一个重要情形就是*周期变量*（periodic variable）。

某个地理位置的风向就是周期变量的一个例子。例如，可以在多个日子里测量风向，然后希望用参数分布来描述这些测量值。另一个例子是日历时间：我们可能希望对某些量建模，并认为这些量具有 24 小时或一年的周期。这类量可以方便地用角坐标（极坐标）$0\leqslant\theta<2\pi$ 表示。

我们可能会尝试选定某个方向作为原点，再应用高斯分布等常规分布来处理周期变量。然而，这种方法的结果会强烈依赖于任意选定的原点。例如，假设有两个观测 $\theta_1=1^{\circ}$ 和 $\theta_2=359^{\circ}$，并用标准的一元高斯分布建模。如果选择 $0^{\circ}$ 为原点，那么该数据集的样本均值为 $180^{\circ}$，标准差为 $179^{\circ}$；如果选择 $180^{\circ}$ 为原点，则均值为 $0^{\circ}$，标准差为 $1^{\circ}$。显然，我们需要专门的方法来处理周期变量。

考虑如何计算周期变量的一组观测 $\mathcal{D}=\{\theta_1,\ldots,\theta_N\}$ 的均值。从现在起，假设 $\theta$ 以弧度为单位。前面已经看到，简单平均值 $(\theta_1+\cdots+\theta_N)/N$ 强烈依赖于坐标。为了找到不随坐标原点改变的均值度量，可以将这些观测看作单位圆上的点，从而用二维单位向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 表示，其中对 $n=1,\ldots,N$ 有 $\|\mathbf{x}_n\|=1$，如图 2.17 所示。改为对向量 $\{\mathbf{x}_n\}$ 求平均，

<!-- pdf-page: 126 -->
<!-- join-previous-paragraph -->
得到

$$
\overline{\mathbf{x}}=\frac1N\sum_{n=1}^{N}\mathbf{x}_n,
\tag{2.167}
$$

再求出这个平均向量对应的角度 $\overline{\theta}$。显然，这一定义保证均值的位置不依赖于角坐标原点。注意，$\overline{\mathbf{x}}$ 通常位于单位圆内部。观测的笛卡尔坐标为 $\mathbf{x}_n=(\cos\theta_n,\sin\theta_n)$，样本均值的笛卡尔坐标则可以写为 $\overline{\mathbf{x}}=(\overline{r}\cos\overline{\theta},\overline{r}\sin\overline{\theta})$。代入式（2.167），分别令 $x_1$ 与 $x_2$ 分量相等，得到

$$
\overline{r}\cos\overline{\theta}=\frac1N\sum_{n=1}^{N}\cos\theta_n,\qquad\overline{r}\sin\overline{\theta}=\frac1N\sum_{n=1}^{N}\sin\theta_n.
\tag{2.168}
$$

两式相除，并利用恒等式 $\tan\theta=\sin\theta/\cos\theta$，可以解出

$$
\overline{\theta}=\tan^{-1}\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.
\tag{2.169}
$$

稍后会看到，对周期变量恰当地定义一个分布之后，这个结果会自然地作为其最大似然估计出现。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-17.png" alt="单位圆上表示周期变量的二维向量及平均向量"><figcaption>图 2.17：将周期变量的取值 $\theta_n$ 表示为单位圆上的二维向量 $\mathbf{x}_n$。图中还画出了这些向量的平均值 $\overline{\mathbf{x}}$。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为坐标轴；$\mathbf{x}_1$ 至 $\mathbf{x}_4$ 为观测向量；$\overline{\mathbf{x}}$、$\overline{r}$、$\overline{\theta}$ 分别为平均向量及其极坐标。</p></figure>

现在考虑高斯分布的一种周期性推广，称为 *von Mises 分布*。这里只讨论一元分布，不过任意维数的超球面上也可以定义周期分布。关于周期分布的详细讨论，参见 Mardia and Jupp（2000）。

按照惯例，我们考虑周期为 $2\pi$ 的分布 $p(\theta)$。定义在 $\theta$ 上的概率密度 $p(\theta)$，不仅必须非负、积分

<!-- pdf-page: 127 -->
<!-- join-previous-paragraph -->
为 1，而且还必须具有周期性。因此，$p(\theta)$ 必须满足三个条件：

$$
p(\theta)\geqslant0,
\tag{2.170}
$$

$$
\int_0^{2\pi}p(\theta)\,\mathrm{d}\theta=1,
\tag{2.171}
$$

$$
p(\theta+2\pi)=p(\theta).
\tag{2.172}
$$

由式（2.172）可知，对于任意整数 $M$，有 $p(\theta+M2\pi)=p(\theta)$。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-18.png" alt="在二维高斯分布上以单位圆为条件得到von Mises分布"><figcaption>图 2.18：考虑形式为（2.173）的二维高斯分布，其密度等高线为蓝色，再以红色单位圆为条件，就可以导出 von Mises 分布。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为坐标轴；$p(\mathbf{x})$ 标示高斯密度；$r=1$ 标示单位圆。</p></figure>

可以很容易地构造一个满足这三个性质、类似高斯的分布。考虑两个变量 $\mathbf{x}=(x_1,x_2)$ 的高斯分布，其均值为 $\boldsymbol{\mu}=(\mu_1,\mu_2)$，协方差矩阵为 $\boldsymbol{\Sigma}=\sigma^2\mathbf{I}$，其中 $\mathbf{I}$ 是 $2\times2$ 单位矩阵，于是

$$
p(x_1,x_2)=\frac1{2\pi\sigma^2}\exp\left\{-\frac{(x_1-\mu_1)^2+(x_2-\mu_2)^2}{2\sigma^2}\right\}.
\tag{2.173}
$$

$p(\mathbf{x})$ 的等值线是圆，如图 2.18 所示。现在考虑这个分布沿某个固定半径圆周的取值。这样构造的分布自然具有周期性，但尚未归一化。通过从笛卡尔坐标 $(x_1,x_2)$ 变换为极坐标 $(r,\theta)$，可以确定其形式，其中

$$
x_1=r\cos\theta,\qquad x_2=r\sin\theta.
\tag{2.174}
$$

均值 $\boldsymbol{\mu}$ 也映射到极坐标，写为

$$
\mu_1=r_0\cos\theta_0,\qquad\mu_2=r_0\sin\theta_0.
\tag{2.175}
$$

接着，将这些变换代入二维高斯分布（2.173），并以单位圆 $r=1$ 为条件。注意，我们只关心对 $\theta$ 的依赖。只看高斯分布的指数部分，有

$$
\begin{aligned}
&-\frac1{2\sigma^2}\{(r\cos\theta-r_0\cos\theta_0)^2+(r\sin\theta-r_0\sin\theta_0)^2\}\\
&=-\frac1{2\sigma^2}\{1+r_0^2-2r_0\cos\theta\cos\theta_0-2r_0\sin\theta\sin\theta_0\}\\
&=\frac{r_0}{\sigma^2}\cos(\theta-\theta_0)+\mathrm{const}.
\end{aligned}
\tag{2.176}
$$

<!-- pdf-page: 128 -->

其中 “const” 表示不依赖于 $\theta$ 的项，并使用了以下三角恒等式（习题 2.51）：

$$
\cos^2A+\sin^2A=1,
\tag{2.177}
$$

$$
\cos A\cos B+\sin A\sin B=\cos(A-B).
\tag{2.178}
$$

定义 $m=r_0/\sigma^2$，最终得到沿单位圆 $r=1$ 的分布 $p(\theta)$：

$$
p(\theta\mid\theta_0,m)=\frac1{2\pi I_0(m)}\exp\{m\cos(\theta-\theta_0)\},
\tag{2.179}
$$

这称为 *von Mises 分布*，也称*圆周正态分布*（circular normal）。参数 $\theta_0$ 对应分布的均值，而 $m$ 称为*集中参数*（concentration parameter），类似于高斯分布的方差倒数（精度）。式（2.179）的归一化系数通过 $I_0(m)$ 表示；$I_0(m)$ 是第一类零阶贝塞尔函数（Abramowitz and Stegun，1965），定义为

$$
I_0(m)=\frac1{2\pi}\int_0^{2\pi}\exp\{m\cos\theta\}\,\mathrm{d}\theta.
\tag{2.180}
$$

当 $m$ 很大时，该分布近似为高斯分布（习题 2.52）。图 2.19 画出了 von Mises 分布，图 2.20 画出了函数 $I_0(m)$。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-19.png" alt="两组参数的von Mises分布，左为笛卡尔坐标图，右为极坐标图"><figcaption>图 2.19：两组不同参数下的 von Mises 分布。左侧为笛卡尔坐标图，右侧为对应的极坐标图。</figcaption><p class="figure-translation">红线：$m=5,\theta_0=\pi/4$；蓝线：$m=1,\theta_0=3\pi/4$；$0$、$2\pi$、$\pi/4$、$3\pi/4$ 为角度标记。</p></figure>

现在考虑 von Mises 分布参数 $\theta_0$ 与 $m$ 的最大似然估计。对数似然函数为

$$
\ln p(\mathcal{D}\mid\theta_0,m)=-N\ln(2\pi)-N\ln I_0(m)+m\sum_{n=1}^{N}\cos(\theta_n-\theta_0).
\tag{2.181}
$$

<!-- pdf-page: 129 -->

令对 $\theta_0$ 的导数为零，得到

$$
\sum_{n=1}^{N}\sin(\theta_n-\theta_0)=0.
\tag{2.182}
$$

为解出 $\theta_0$，使用三角恒等式

$$
\sin(A-B)=\cos B\sin A-\cos A\sin B,
\tag{2.183}
$$

由此得到（习题 2.53）

$$
\theta_0^{\mathrm{ML}}=\tan^{-1}\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.
\tag{2.184}
$$

这正是前面将观测看作二维笛卡尔空间中的点时，得到的均值公式（2.169）。

类似地，关于 $m$ 最大化式（2.181），并利用 $I_0'(m)=I_1(m)$（Abramowitz and Stegun，1965），得到

$$
A(m)=\frac1N\sum_{n=1}^{N}\cos(\theta_n-\theta_0^{\mathrm{ML}}),
\tag{2.185}
$$

其中已经代入 $\theta_0^{\mathrm{ML}}$ 的最大似然解（记住，我们在对 $\theta$ 与 $m$ 做联合优化），并定义

$$
A(m)=\frac{I_1(m)}{I_0(m)}.
\tag{2.186}
$$

函数 $A(m)$ 如图 2.20 所示。利用三角恒等式（2.178），式（2.185）可写成

$$
A(m_{\mathrm{ML}})=\left(\frac1N\sum_{n=1}^{N}\cos\theta_n\right)\cos\theta_0^{\mathrm{ML}}-\left(\frac1N\sum_{n=1}^{N}\sin\theta_n\right)\sin\theta_0^{\mathrm{ML}}.
\tag{2.187}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-20.png" alt="贝塞尔函数I0和函数A随集中参数m变化的曲线"><figcaption>图 2.20：式（2.180）定义的贝塞尔函数 $I_0(m)$，以及式（2.186）定义的函数 $A(m)$。</figcaption><p class="figure-translation">两图横轴均为 $m$，左图纵轴为 $I_0(m)$，右图纵轴为 $A(m)$。</p></figure>

<!-- pdf-page: 130 -->

式（2.187）的右侧容易计算，而函数 $A(m)$ 可以数值求逆。

为求完整，简要提及构造周期分布的其他方法。最简单的方法是将角坐标划分为固定区间，使用观测值的直方图。这种方法简单、灵活，但也有明显局限；第 2.5 节详细讨论直方图方法时会看到这一点。另一种方法与 von Mises 分布一样，从欧氏空间中的高斯分布出发，但这次对单位圆进行边缘化，而不是条件化（Mardia and Jupp，2000）。不过，由此得到的分布形式较复杂，这里不再讨论。最后，实轴上的任何有效分布（例如高斯分布），都可以通过将宽度为 $2\pi$ 的连续区间映射到周期变量 $(0,2\pi)$ 上，变成周期分布。这相当于把实轴“缠绕”在单位圆周上。同样，所得分布比 von Mises 分布更难处理。

von Mises 分布的一个局限是它只有单个众数。通过构造 von Mises 分布的混合，可以得到一个能处理多峰情况的灵活框架，用于周期变量建模。使用 von Mises 分布的机器学习应用示例可参见 Lawrence et al.（2002）；将其推广到回归问题的条件密度建模，可参见 Bishop and Nabney（1996）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-21.png" alt="Old Faithful数据集的单高斯拟合与双高斯混合拟合对比"><figcaption>图 2.21：“Old Faithful”数据的散点图，蓝色曲线为概率密度等高线。左图是用最大似然拟合得到的单个高斯分布。注意，这个分布无法刻画数据的两个簇，反而将大量概率质量放在两簇之间数据相对稀疏的中央区域。右图的分布是两个高斯分布的线性组合，用第 9 章介绍的方法进行最大似然拟合，更好地表示了数据。</figcaption><p class="figure-translation">两图横轴表示喷发持续时间（分钟），纵轴表示距离下一次喷发的时间（分钟）。</p></figure>

### 2.3.9 高斯混合

尽管高斯分布具有一些重要的解析性质，但对真实数据集建模时仍有明显局限。考虑图 2.21 的例子。这是“Old Faithful”（老忠实泉）数据集，包含美国黄石国家公园老忠实间歇泉的 272 次喷发测量（附录 A）。每次测量记录

<!-- pdf-page: 131 -->
<!-- join-previous-paragraph -->
喷发持续时间，单位为分钟（横轴），以及距离下一次喷发的时间，单位同样为分钟（纵轴）。可以看到，数据形成了两个明显的簇，简单的高斯分布无法刻画这种结构，而两个高斯分布的线性叠加能更好地描述这个数据集。

通过对高斯分布等较基本的分布作线性组合，可以将这种叠加构造成称为*混合分布*（mixture distribution）的概率模型（McLachlan and Basford，1988；McLachlan and Peel，2000）。图 2.22 表明，高斯分布的线性组合能够产生非常复杂的密度。只要使用足够多的高斯分布，调整它们的均值、协方差以及线性组合的系数，就可以用任意精度近似几乎任何连续密度。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-22.png" alt="三个一维高斯分量相加得到多峰混合密度"><figcaption>图 2.22：一维高斯混合分布的例子。蓝色为三个高斯分布（每个都乘以相应系数），红色为它们的和。</figcaption><p class="figure-translation">横轴为 $x$，纵轴为概率密度 $p(x)$。</p></figure>

因此，考虑如下形式的 $K$ 个高斯密度的叠加：

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k),
\tag{2.188}
$$

称为*高斯混合*（mixture of Gaussians）。每个高斯密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$ 称为混合的一个*分量*（component），具有自己的均值 $\boldsymbol{\mu}_k$ 和协方差 $\boldsymbol{\Sigma}_k$。含有 3 个分量的高斯混合的等高线图和曲面图见图 2.23。

本节以高斯分量为例说明混合模型的框架。更一般地，混合模型也可以由其他分布的线性组合构成。例如，第 9.3.3 节将讨论伯努利分布的混合，作为离散变量混合模型的一个例子。

式（2.188）中的参数 $\pi_k$ 称为*混合系数*（mixing coefficient）。将式（2.188）两边对 $\mathbf{x}$ 积分，并注意 $p(\mathbf{x})$ 和每个高斯分量都已归一化，得到

$$
\sum_{k=1}^{K}\pi_k=1.
\tag{2.189}
$$

此外，要求 $p(\mathbf{x})\geqslant0$，并结合 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\geqslant0$，意味着所有 $k$ 都满足 $\pi_k\geqslant0$。结合条件（2.189），得到

$$
0\leqslant\pi_k\leqslant1.
\tag{2.190}
$$

<!-- pdf-page: 132 -->

因此，混合系数满足作为概率所需的条件。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-23.png" alt="二维空间中三个高斯分量、混合密度等高线及三维曲面"><figcaption>图 2.23：二维空间中由 3 个高斯分布构成的混合。（a）各混合分量的密度等高线，三个分量分别用红色、蓝色和绿色表示，每个分量下方标出了混合系数。（b）混合分布的边缘概率密度 $p(\mathbf{x})$ 的等高线。（c）分布 $p(\mathbf{x})$ 的曲面图。</figcaption><p class="figure-translation">（a）分量等高线，红、蓝、绿分量的混合系数分别为 $0.5$、$0.2$、$0.3$；（b）混合密度等高线；（c）混合密度曲面。</p></figure>

根据求和法则和乘积法则，边缘密度为

$$
p(\mathbf{x})=\sum_{k=1}^{K}p(k)p(\mathbf{x}\mid k),
\tag{2.191}
$$

它与式（2.188）等价，其中可以将 $\pi_k=p(k)$ 看作选择第 $k$ 个分量的先验概率，将密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)=p(\mathbf{x}\mid k)$ 看作给定 $k$ 时 $\mathbf{x}$ 的概率。后续章节将看到，后验概率 $p(k\mid\mathbf{x})$ 起着重要作用，它们也称为*责任度*（responsibility）。由贝叶斯定理，

$$
\begin{aligned}
\gamma_k(\mathbf{x})&\equiv p(k\mid\mathbf{x})\\
&=\frac{p(k)p(\mathbf{x}\mid k)}{\sum_l p(l)p(\mathbf{x}\mid l)}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_l\pi_l\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_l,\boldsymbol{\Sigma}_l)}.
\end{aligned}
\tag{2.192}
$$

第 9 章将更详细地讨论混合分布的概率解释。

高斯混合分布的形式由参数 $\boldsymbol{\pi}$、$\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 决定，这里使用记号 $\boldsymbol{\pi}\equiv\{\pi_1,\ldots,\pi_K\}$、$\boldsymbol{\mu}\equiv\{\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K\}$ 和 $\boldsymbol{\Sigma}\equiv\{\boldsymbol{\Sigma}_1,\ldots,\boldsymbol{\Sigma}_K\}$。设置这些参数的一种方法是最大似然。根据式（2.188），对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{2.193}
$$

<!-- pdf-page: 133 -->

其中 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$。立刻可以看到，由于对 $k$ 的求和出现在对数内部，情况比单个高斯分布复杂得多。因此，参数的最大似然解不再具有闭式解析表达式。最大化似然函数的一种方法是使用迭代数值优化技术（Fletcher，1987；Nocedal and Wright，1999；Bishop and Nabney，2008）。也可以采用一个强有力的框架，称为*期望最大化*（expectation maximization），第 9 章将详细讨论它。

## 2.4 指数族

本章目前研究的概率分布（高斯混合除外），都是一大类称为*指数族*（exponential family）的分布的具体例子（Duda and Hart，1973；Bernardo and Smith，1994）。指数族成员具有许多重要的共同性质，以较一般的形式讨论这些性质很有启发意义。

给定参数 $\boldsymbol{\eta}$，定义在 $\mathbf{x}$ 上的指数族，是具有如下形式的分布集合：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=h(\mathbf{x})g(\boldsymbol{\eta})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\},
\tag{2.194}
$$

其中 $\mathbf{x}$ 可以是标量或向量，也可以是离散或连续的。$\boldsymbol{\eta}$ 称为分布的*自然参数*（natural parameter），$\mathbf{u}(\mathbf{x})$ 是 $\mathbf{x}$ 的某个函数。函数 $g(\boldsymbol{\eta})$ 可以看作确保分布归一化的系数，因此满足

$$
g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\,\mathrm{d}\mathbf{x}=1.
\tag{2.195}
$$

如果 $\mathbf{x}$ 是离散变量，则将积分换成求和。

先以本章前面介绍的一些分布为例，说明它们确实属于指数族。首先考虑伯努利分布

$$
p(x\mid\mu)=\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}.
\tag{2.196}
$$

将右侧写成其对数的指数，得到

$$
\begin{aligned}
p(x\mid\mu)&=\exp\{x\ln\mu+(1-x)\ln(1-\mu)\}\\
&=(1-\mu)\exp\left\{\ln\left(\frac{\mu}{1-\mu}\right)x\right\}.
\end{aligned}
\tag{2.197}
$$

与式（2.194）比较，可知

$$
\eta=\ln\left(\frac{\mu}{1-\mu}\right).
\tag{2.198}
$$

<!-- pdf-page: 134 -->

由此可以解出 $\mu=\sigma(\eta)$，其中

$$
\sigma(\eta)=\frac1{1+\exp(-\eta)}
\tag{2.199}
$$

称为 *logistic sigmoid 函数*。因此，可以用标准表示（2.194）将伯努利分布写为

$$
p(x\mid\eta)=\sigma(-\eta)\exp(\eta x),
\tag{2.200}
$$

其中使用了 $1-\sigma(\eta)=\sigma(-\eta)$，这一恒等式很容易由式（2.199）证明。与式（2.194）比较可知

$$
u(x)=x,
\tag{2.201}
$$

$$
h(x)=1,
\tag{2.202}
$$

$$
g(\eta)=\sigma(-\eta).
\tag{2.203}
$$

接着考虑多项分布。对于单个观测 $\mathbf{x}$，其形式为

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{k=1}^{M}\mu_k^{x_k}=\exp\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\},
\tag{2.204}
$$

其中 $\mathbf{x}=(x_1,\ldots,x_N)^{\mathrm T}$。同样，可以将其写成标准表示（2.194）：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=\exp(\boldsymbol{\eta}^{\mathrm T}\mathbf{x}),
\tag{2.205}
$$

其中 $\eta_k=\ln\mu_k$，并定义 $\boldsymbol{\eta}=(\eta_1,\ldots,\eta_M)^{\mathrm T}$。再次与式（2.194）比较，有

$$
\mathbf{u}(\mathbf{x})=\mathbf{x},
\tag{2.206}
$$

$$
h(\mathbf{x})=1,
\tag{2.207}
$$

$$
g(\boldsymbol{\eta})=1.
\tag{2.208}
$$

注意，参数 $\eta_k$ 并非彼此独立，因为参数 $\mu_k$ 受到约束

$$
\sum_{k=1}^{M}\mu_k=1.
\tag{2.209}
$$

因此，只要给定任意 $M-1$ 个参数 $\mu_k$，剩下一个参数的值就确定了。在某些情况下，只用 $M-1$ 个参数表示分布、消去这个约束，会更方便。可以利用关系（2.209），用其余 $\{\mu_k\}$（$k=1,\ldots,M-1$）表示 $\mu_M$ 并将其消去，从而只留下 $M-1$ 个参数。注意，剩余参数仍然受到如下约束：

$$
0\leqslant\mu_k\leqslant1,\qquad\sum_{k=1}^{M-1}\mu_k\leqslant1.
\tag{2.210}
$$

<!-- pdf-page: 135 -->

利用约束（2.209），在这种表示下，多项分布变为

$$
\begin{aligned}
&\exp\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\}\\
&=\exp\left\{\sum_{k=1}^{M-1}x_k\ln\mu_k+\left(1-\sum_{k=1}^{M-1}x_k\right)\ln\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}\\
&=\exp\left\{\sum_{k=1}^{M-1}x_k\ln\left(\frac{\mu_k}{1-\sum_{j=1}^{M-1}\mu_j}\right)+\ln\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}.
\end{aligned}
\tag{2.211}
$$

于是取

$$
\ln\left(\frac{\mu_k}{1-\sum_j\mu_j}\right)=\eta_k.
\tag{2.212}
$$

先将两边对 $k$ 求和，再整理并代回，就可以解出 $\mu_k$：

$$
\mu_k=\frac{\exp(\eta_k)}{1+\sum_j\exp(\eta_j)}.
\tag{2.213}
$$

这称为 *softmax 函数*，也称*归一化指数函数*（normalized exponential）。因此，在这种表示下，多项分布具有如下形式：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}\exp(\boldsymbol{\eta}^{\mathrm T}\mathbf{x}).
\tag{2.214}
$$

这就是指数族的标准形式，参数向量为 $\boldsymbol{\eta}=(\eta_1,\ldots,\eta_{M-1})^{\mathrm T}$，其中

$$
\mathbf{u}(\mathbf{x})=\mathbf{x},
\tag{2.215}
$$

$$
h(\mathbf{x})=1,
\tag{2.216}
$$

$$
g(\boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}.
\tag{2.217}
$$

最后考虑高斯分布。对于一元高斯分布，有

$$
p(x\mid\mu,\sigma^2)=\frac1{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac1{2\sigma^2}(x-\mu)^2\right\},
\tag{2.218}
$$

$$
\phantom{p(x\mid\mu,\sigma^2)}=\frac1{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac1{2\sigma^2}x^2+\frac{\mu}{\sigma^2}x-\frac1{2\sigma^2}\mu^2\right\}.
\tag{2.219}
$$

<!-- pdf-page: 136 -->

经过简单整理，可以将其写成指数族的标准形式（2.194），其中（习题 2.57）

$$
\boldsymbol{\eta}=\begin{pmatrix}\mu/\sigma^2\\-1/2\sigma^2\end{pmatrix},
\tag{2.220}
$$

$$
\mathbf{u}(x)=\begin{pmatrix}x\\x^2\end{pmatrix},
\tag{2.221}
$$

$$
h(x)=(2\pi)^{-1/2},
\tag{2.222}
$$

$$
g(\boldsymbol{\eta})=(-2\eta_2)^{1/2}\exp\left(\frac{\eta_1^2}{4\eta_2}\right).
\tag{2.223}
$$

### 2.4.1 最大似然与充分统计量

现在考虑如何用最大似然估计一般指数族分布（2.194）的参数向量 $\boldsymbol{\eta}$。对式（2.195）两边关于 $\boldsymbol{\eta}$ 取梯度，有

$$
\begin{aligned}
&\nabla g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\,\mathrm{d}\mathbf{x}\\
&\quad+g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=0.
\end{aligned}
\tag{2.224}
$$

整理，并再次利用式（2.195），得到

$$
-\frac1{g(\boldsymbol{\eta})}\nabla g(\boldsymbol{\eta})=g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}[\mathbf{u}(\mathbf{x})],
\tag{2.225}
$$

其中使用了式（2.194）。因此得到

$$
-\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})].
\tag{2.226}
$$

注意，$\mathbf{u}(\mathbf{x})$ 的协方差可以用 $g(\boldsymbol{\eta})$ 的二阶导数表示，更高阶矩也类似（习题 2.58）。因此，只要能够将指数族中的分布归一化，就总能通过简单求导得到它的各阶矩。

现在考虑一组独立同分布的数据，记为 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_n\}$，其似然函数为

$$
p(\mathbf{X}\mid\boldsymbol{\eta})=\left(\prod_{n=1}^{N}h(\mathbf{x}_n)\right)g(\boldsymbol{\eta})^N\exp\left\{\boldsymbol{\eta}^{\mathrm T}\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n)\right\}.
\tag{2.227}
$$

令 $\ln p(\mathbf{X}\mid\boldsymbol{\eta})$ 关于 $\boldsymbol{\eta}$ 的梯度为零，得到最大似然估计 $\boldsymbol{\eta}_{\mathrm{ML}}$ 必须满足的条件：

$$
-\nabla\ln g(\boldsymbol{\eta}_{\mathrm{ML}})=\frac1N\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n).
\tag{2.228}
$$

<!-- pdf-page: 137 -->

原则上，解这个方程就可以得到 $\boldsymbol{\eta}_{\mathrm{ML}}$。可以看到，最大似然估计的解只通过 $\sum_n\mathbf{u}(\mathbf{x}_n)$ 依赖于数据，所以这个量称为分布（2.194）的*充分统计量*（sufficient statistic）。不必存储整个数据集，只需存储充分统计量的值。例如，伯努利分布中的函数 $u(x)$ 就是 $x$，因此只需保留数据点 $\{x_n\}$ 的和；对于高斯分布，$\mathbf{u}(x)=(x,x^2)^{\mathrm T}$，因此必须同时保留 $\{x_n\}$ 的和与 $\{x_n^2\}$ 的和。

在 $N\to\infty$ 的极限下，式（2.228）的右侧变为 $\mathbb{E}[\mathbf{u}(\mathbf{x})]$。与式（2.226）比较可知，在这个极限下，$\boldsymbol{\eta}_{\mathrm{ML}}$ 等于真实参数值 $\boldsymbol{\eta}$。

事实上，这种充分性也适用于贝叶斯推断，不过我们把讨论推迟到第 8 章。在那里，我们已经掌握图模型的工具，从而能够更深入地理解这些重要概念。

### 2.4.2 共轭先验

我们已经多次遇到共轭先验的概念，例如伯努利分布的共轭先验是Beta 分布；高斯分布中，均值的共轭先验是高斯分布，精度的共轭先验是 Wishart 分布。一般地，对于给定概率分布 $p(\mathbf{x}\mid\boldsymbol{\eta})$，可以寻找与似然函数共轭的先验 $p(\boldsymbol{\eta})$，使后验分布与先验具有相同的函数形式。指数族（2.194）的任意成员，都存在如下形式的共轭先验：

$$
p(\boldsymbol{\eta}\mid\boldsymbol{\chi},\nu)=f(\boldsymbol{\chi},\nu)g(\boldsymbol{\eta})^{\nu}\exp\{\nu\boldsymbol{\eta}^{\mathrm T}\boldsymbol{\chi}\},
\tag{2.229}
$$

其中 $f(\boldsymbol{\chi},\nu)$ 为归一化系数，$g(\boldsymbol{\eta})$ 与式（2.194）中的函数相同。要确认它确实共轭，将先验（2.229）乘以似然函数（2.227），忽略归一化系数，得到后验分布

$$
p(\boldsymbol{\eta}\mid\mathbf{X},\boldsymbol{\chi},\nu)\propto g(\boldsymbol{\eta})^{\nu+N}\exp\left\{\boldsymbol{\eta}^{\mathrm T}\left(\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n)+\nu\boldsymbol{\chi}\right)\right\}.
\tag{2.230}
$$

它与先验（2.229）的函数形式相同，因而确认了共轭性。还可以看到，参数 $\nu$ 可以解释为先验中的有效伪观测数，每个伪观测的充分统计量 $\mathbf{u}(\mathbf{x})$ 都取值为 $\boldsymbol{\chi}$。

### 2.4.3 无信息先验

在概率推断的一些应用中，我们可能具有便于用先验分布表达的先验知识。例如，如果先验对变量的某个值赋予零概率，那么无论

<!-- pdf-page: 138 -->
<!-- join-previous-paragraph -->
随后观测到什么数据，后验分布也必然给这个值零概率。然而，很多时候，我们对先验分布应具有什么形式所知甚少。这时可以寻找一种称为*无信息先验*（noninformative prior）的先验分布，希望它对后验分布的影响尽可能小（Jeffries，1946；Box and Tao，1973；Bernardo and Smith，1994）。这有时被称为“让数据自己说话”。

如果分布 $p(x\mid\lambda)$ 由参数 $\lambda$ 决定，我们可能会认为常数先验 $p(\lambda)=\mathrm{const}$ 很合适。如果 $\lambda$ 是具有 $K$ 个状态的离散变量，这相当于令各状态的先验概率均为 $1/K$。但对于连续参数，这种方法有两个潜在困难。首先，如果 $\lambda$ 的定义域无界，那么对 $\lambda$ 的积分发散，该先验分布无法正确归一化。这种先验称为*非正常先验*（improper prior）。在实践中，只要相应的后验分布是正常的（proper），即能够正确归一化，往往仍然可以使用非正常先验。例如，在高斯分布的均值上采用均匀先验后，只要观测到至少一个数据点，均值的后验分布就是正常的。

第二个困难来自非线性变量变换下概率密度的变换规律，即式（1.27）。如果函数 $h(\lambda)$ 是常数，进行变量代换 $\lambda=\eta^2$ 后，$\widehat{h}(\eta)=h(\eta^2)$ 仍是常数。但如果选择密度 $p_{\lambda}(\lambda)$ 为常数，根据式（1.27），$\eta$ 的密度为

$$
p_{\eta}(\eta)=p_{\lambda}(\lambda)\left|\frac{\mathrm{d}\lambda}{\mathrm{d}\eta}\right|=p_{\lambda}(\eta^2)2\eta\propto\eta,
\tag{2.231}
$$

所以 $\eta$ 的密度不是常数。最大似然方法不会遇到这个问题，因为似然函数 $p(x\mid\lambda)$ 只是 $\lambda$ 的普通函数，可以自由选择任何方便的参数化方式。但是，如果要选择常数先验分布，就必须谨慎地选择参数的合适表示。

这里考察两个简单的无信息先验例子（Berger，1985）。首先，如果密度具有形式

$$
p(x\mid\mu)=f(x-\mu),
\tag{2.232}
$$

则参数 $\mu$ 称为*位置参数*（location parameter）。这个密度族具有*平移不变性*（translation invariance），因为将 $x$ 平移一个常数，得到 $\widehat{x}=x+c$ 后，有

$$
p(\widehat{x}\mid\widehat{\mu})=f(\widehat{x}-\widehat{\mu}),
\tag{2.233}
$$

其中定义了 $\widehat{\mu}=\mu+c$。因此，密度在新变量下与原变量下具有相同形式，也就是说，密度不依赖原点的选择。我们希望选取的先验反映这种平移不变性，因此令先验对

<!-- pdf-page: 139 -->
<!-- join-previous-paragraph -->
区间 $A\leqslant\mu\leqslant B$ 及平移后的区间 $A-c\leqslant\mu\leqslant B-c$ 赋予相同的概率质量。这意味着

$$
\int_A^B p(\mu)\,\mathrm{d}\mu=\int_{A-c}^{B-c}p(\mu)\,\mathrm{d}\mu=\int_A^B p(\mu-c)\,\mathrm{d}\mu.
\tag{2.234}
$$

由于对任意 $A$ 和 $B$ 都必须成立，所以

$$
p(\mu-c)=p(\mu),
\tag{2.235}
$$

即 $p(\mu)$ 是常数。高斯分布的均值 $\mu$ 就是位置参数的一个例子。前面看到，$\mu$ 的共轭先验是高斯分布 $p(\mu\mid\mu_0,\sigma_0^2)=\mathcal{N}(\mu\mid\mu_0,\sigma_0^2)$。取极限 $\sigma_0^2\to\infty$，就得到无信息先验。事实上，由式（2.141）和（2.142）可见，此时 $\mu$ 的后验分布中，先验的贡献消失了。

第二个例子是如下形式的密度：

$$
p(x\mid\sigma)=\frac1{\sigma}f\left(\frac{x}{\sigma}\right),
\tag{2.236}
$$

其中 $\sigma>0$。注意，只要 $f(x)$ 正确归一化，这也是归一化的密度（习题 2.59）。参数 $\sigma$ 称为*尺度参数*（scale parameter），密度具有*尺度不变性*（scale invariance）：将 $x$ 乘以常数，得到 $\widehat{x}=cx$ 后，有

$$
p(\widehat{x}\mid\widehat{\sigma})=\frac1{\widehat{\sigma}}f\left(\frac{\widehat{x}}{\widehat{\sigma}}\right),
\tag{2.237}
$$

其中定义 $\widehat{\sigma}=c\sigma$。这种变换对应于尺度的改变，例如当 $x$ 表示长度时，从米换为千米。我们希望所选先验反映这种尺度不变性。如果考虑区间 $A\leqslant\sigma\leqslant B$ 和缩放后的区间 $A/c\leqslant\sigma\leqslant B/c$，先验应对这两个区间赋予相同的概率质量。因此

$$
\int_A^B p(\sigma)\,\mathrm{d}\sigma=\int_{A/c}^{B/c}p(\sigma)\,\mathrm{d}\sigma=\int_A^B p\left(\frac1c\sigma\right)\frac1c\,\mathrm{d}\sigma.
\tag{2.238}
$$

由于对任意 $A$ 和 $B$ 都必须成立，所以

$$
p(\sigma)=p\left(\frac1c\sigma\right)\frac1c,
\tag{2.239}
$$

从而 $p(\sigma)\propto1/\sigma$。注意，这又是一个非正常先验，因为分布在 $0\leqslant\sigma\leqslant\infty$ 上的积分发散。有时，从参数对数的密度来看尺度参数的先验也很方便。利用密度变换规则（1.27），可知 $p(\ln\sigma)=\mathrm{const}$。因此，在这个先验下，区间 $1\leqslant\sigma\leqslant10$、$10\leqslant\sigma\leqslant100$ 和 $100\leqslant\sigma\leqslant1000$ 的概率质量相同。

<!-- pdf-page: 140 -->

在考虑了位置参数 $\mu$ 之后，高斯分布的标准差 $\sigma$ 就是尺度参数的一个例子，因为

$$
\mathcal{N}(x\mid\mu,\sigma^2)\propto\sigma^{-1}\exp\{-(\widetilde{x}/\sigma)^2\},
\tag{2.240}
$$

其中 $\widetilde{x}=x-\mu$。如前所述，使用精度 $\lambda=1/\sigma^2$ 往往比直接使用 $\sigma$ 更方便。根据密度变换规则，分布 $p(\sigma)\propto1/\sigma$ 对应于形式为 $p(\lambda)\propto1/\lambda$ 的分布。我们已经看到，$\lambda$ 的共轭先验是式（2.146）给出的伽马分布 $\operatorname{Gam}(\lambda\mid a_0,b_0)$（第 2.3 节）。无信息先验是 $a_0=b_0=0$ 的特例。再看 $\lambda$ 的后验分布结果（2.150）和（2.151），当 $a_0=b_0=0$ 时，后验只依赖于来自数据的项，而不依赖先验。

## 2.5 非参数方法

本章一直关注具有特定函数形式的概率分布，这些分布由少量参数决定，参数值则根据数据集确定。这称为密度建模的*参数化方法*（parametric approach）。这种方法的一个重要局限是，所选密度可能无法很好地描述生成数据的分布，导致预测性能较差。例如，如果数据生成过程具有多个众数，那么高斯分布永远无法刻画这一特征，因为它必定是单峰的。

在最后这一节，我们考察一些对分布形式作很少假设的*非参数*（nonparametric）密度估计方法。这里主要关注简单的频率学派方法。不过，读者也应知道，非参数贝叶斯方法正受到越来越多的关注（Walker et al.，1999；Neal，2000；Müller and Quintana，2004；Teh et al.，2006）。

先讨论密度估计的直方图方法。前面在图 1.11 的边缘分布与条件分布，以及图 2.6 的中心极限定理中，已经见过这种方法。这里进一步考察直方图密度模型的性质，重点是单个连续变量 $x$。标准直方图把 $x$ 划分为宽度为 $\Delta_i$ 的互不重叠的区间，再统计落入第 $i$ 个区间的观测数 $n_i$。要将计数变为归一化概率密度，只需除以观测总数 $N$ 和区间宽度 $\Delta_i$，得到每个区间的概率值

$$
p_i=\frac{n_i}{N\Delta_i}.
\tag{2.241}
$$

容易看出，此时 $\int p(x)\,\mathrm{d}x=1$。得到的密度模型 $p(x)$ 在每个区间内都是常数，通常选择各区间具有相同宽度 $\Delta_i=\Delta$。

<!-- pdf-page: 141 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-24.png" alt="三种区间宽度下的直方图密度估计"><figcaption>图 2.24：直方图密度估计示意图。从绿色曲线所表示的分布中生成包含 50 个数据点的数据集。根据式（2.241）进行直方图密度估计，所有区间宽度相同，为 $\Delta$；图中展示了不同 $\Delta$ 值下的结果。</figcaption><p class="figure-translation">从上到下，区间宽度分别为 $\Delta=0.04$、$\Delta=0.08$、$\Delta=0.25$。</p></figure>

图 2.24 展示了直方图密度估计的例子。数据来自绿色曲线对应的分布，它由两个高斯分布混合而成。图中同时给出了三种区间宽度 $\Delta$ 对应的直方图密度估计。当 $\Delta$ 很小（上图）时，得到的密度模型有很多尖峰，其中许多结构并不存在于实际生成数据的分布中。相反，当 $\Delta$ 过大（下图）时，模型过于平滑，无法刻画绿色曲线的双峰特征。某个适中的 $\Delta$ 值（中图）给出了最佳结果。原则上，直方图密度模型也依赖于区间边界位置的选择，不过其影响通常远小于 $\Delta$ 的影响。

注意，直方图方法具有一个特点（稍后介绍的方法没有这一特点）：一旦计算完直方图，就可以丢弃原数据集。数据集很大时，这可能是一个优势。此外，当数据点逐个到达时，直方图方法也容易使用。

实际中，直方图适合快速查看一维或二维数据的分布，但不适合大多数密度估计应用。一个明显问题是，估计密度的不连续性来自区间边界，而不是来自真实数据生成分布的任何性质。另一个重要局限是它随维数的增长情况。如果将 $D$ 维空间中每个变量都划分为 $M$ 个区间，则总单元数为 $M^D$。这种随 $D$ 的指数增长，就是维数灾难的一个例子（第 1.4 节）。在高维空间中，要对局部概率密度作出有意义的估计，所需数据量大得难以承受。

不过，直方图密度估计给出了两点重要启示。第一，为了估计某个位置的概率密度，应考察该点某个局部邻域内的数据点。注意，局部性的概念要求我们假定某种距离度量，这里一直采用欧氏距离。对于直方图，

<!-- pdf-page: 142 -->
<!-- join-previous-paragraph -->
邻域由区间定义，并且自然存在一个描述局部区域空间范围的“平滑”参数，此处就是区间宽度。第二，要获得好的结果，平滑参数既不能太大，也不能太小。这使人想到第 1 章多项式曲线拟合中的模型复杂度选择：多项式阶数 $M$，或者正则化参数 $\alpha$，都在某个不大不小的中间值处最优。带着这些认识，我们转而讨论两种广泛使用的非参数密度估计技术：核估计和近邻方法。它们随维数增长的表现，比简单直方图模型更好。

### 2.5.1 核密度估计

假设在某个 $D$ 维空间中，从未知概率密度 $p(\mathbf{x})$ 抽取观测；这里假定该空间是欧氏空间。我们希望估计 $p(\mathbf{x})$ 的值。根据前面对局部性的讨论，考虑包含 $\mathbf{x}$ 的一个小区域 $\mathcal{R}$。这个区域的概率质量为

$$
P=\int_{\mathcal{R}}p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{2.242}
$$

现在假设已经收集到由 $p(\mathbf{x})$ 抽取的 $N$ 个观测组成的数据集。每个数据点落入 $\mathcal{R}$ 的概率都是 $P$，因此区域内的数据点总数 $K$ 服从二项分布（第 2.1 节）：

$$
\operatorname{Bin}(K\mid N,P)=\frac{N!}{K!(N-K)!}P^K(1-P)^{1-K}.
\tag{2.243}
$$

根据式（2.11），落入该区域的数据点比例的均值为 $\mathbb{E}[K/N]=P$；类似地，根据式（2.12），围绕此均值的方差为 $\operatorname{var}[K/N]=P(1-P)/N$。当 $N$ 很大时，这个分布在均值附近形成尖峰，因此

$$
K\simeq NP.
\tag{2.244}
$$

如果再假设区域 $\mathcal{R}$ 足够小，使概率密度 $p(\mathbf{x})$ 在整个区域内近似不变，则有

$$
P\simeq p(\mathbf{x})V,
\tag{2.245}
$$

其中 $V$ 是 $\mathcal{R}$ 的体积。结合式（2.244）与（2.245），得到密度估计

$$
p(\mathbf{x})=\frac{K}{NV}.
\tag{2.246}
$$

注意，式（2.246）的有效性依赖两个相互矛盾的假设：区域 $\mathcal{R}$ 必须足够小，使区域内密度近似不变；同时，相对于密度的大小，它又必须足够大，使落入区域的数据点数 $K$ 足以让二项分布形成尖峰。

<!-- pdf-page: 143 -->

结果（2.246）有两种用法。可以固定 $K$，根据数据确定 $V$，得到稍后讨论的 $K$ 近邻方法；也可以固定 $V$，根据数据确定 $K$，得到核方法。可以证明，只要 $V$ 随 $N$ 适当缩小，而 $K$ 随 $N$ 增长，$K$ 近邻密度估计和核密度估计在 $N\to\infty$ 的极限下都会收敛于真实概率密度（Duda and Hart，1973）。

先详细讨论核方法。首先，将区域 $\mathcal{R}$ 取为以待估计概率密度的位置 $\mathbf{x}$ 为中心的小超立方体。为了统计落入其中的数据点数 $K$，定义以下函数很方便：

$$
k(\mathbf{u})=\begin{cases}1,&|u_i|\leqslant1/2,\quad i=1,\ldots,D,\\0,&\text{其他情况},\end{cases}
\tag{2.247}
$$

它表示以原点为中心的单位立方体。函数 $k(\mathbf{u})$ 是*核函数*（kernel function）的一个例子，在此也称为 *Parzen 窗*（Parzen window）。由式（2.247），如果数据点 $\mathbf{x}_n$ 位于以 $\mathbf{x}$ 为中心、边长为 $h$ 的立方体内，$k((\mathbf{x}-\mathbf{x}_n)/h)$ 等于 1，否则等于 0。因此，立方体内的数据点总数为

$$
K=\sum_{n=1}^{N}k\left(\frac{\mathbf{x}-\mathbf{x}_n}{h}\right).
\tag{2.248}
$$

将其代入式（2.246），得到 $\mathbf{x}$ 处的密度估计

$$
p(\mathbf{x})=\frac1N\sum_{n=1}^{N}\frac1{h^D}k\left(\frac{\mathbf{x}-\mathbf{x}_n}{h}\right),
\tag{2.249}
$$

这里使用了 $D$ 维空间中边长为 $h$ 的超立方体体积 $V=h^D$。利用 $k(\mathbf{u})$ 的对称性，可以重新解释这个等式：不再看作以 $\mathbf{x}$ 为中心的单个立方体，而是看作分别以 $N$ 个数据点 $\mathbf{x}_n$ 为中心的 $N$ 个立方体的求和。

当前形式的核密度估计（2.249）仍然存在直方图方法的一个问题：人为产生的不连续性，此处出现在立方体边界。如果选择更平滑的核函数，就可以得到更平滑的密度模型。常见选择是高斯函数，对应如下核密度模型：

$$
p(\mathbf{x})=\frac1N\sum_{n=1}^{N}\frac1{(2\pi h^2)^{1/2}}\exp\left\{-\frac{\|\mathbf{x}-\mathbf{x}_n\|^2}{2h^2}\right\},
\tag{2.250}
$$

其中 $h$ 表示高斯分量的标准差。因此，密度模型的构造方法是：在每个数据点上放置一个高斯分布，将整个数据集中各点的贡献相加，再除以 $N$，使密度正确归一化。图 2.25 将模型（2.250）应用于前面用于

<!-- pdf-page: 144 -->
<!-- join-previous-paragraph -->
说明直方图方法的数据集。正如预期，参数 $h$ 起着平滑参数的作用：较小的 $h$ 对噪声敏感，较大的 $h$ 又会过度平滑，需要在两者之间权衡。同样，优化 $h$ 是模型复杂度问题，类似于直方图密度估计中选择区间宽度，或者曲线拟合中选择多项式阶数。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-25.png" alt="三种核宽度的核密度估计，与真实双峰密度比较"><figcaption>图 2.25：将核密度模型（2.250）应用于图 2.24 中说明直方图方法的同一数据集。$h$ 起平滑参数的作用。如果太小（上图），得到的密度模型噪声很大；如果太大（下图），实际生成数据的分布（绿色曲线）的双峰结构会被抹平。某个适中的 $h$ 值（中图）给出最佳密度模型。</figcaption><p class="figure-translation">从上到下分别为 $h=0.005$、$h=0.07$、$h=0.2$；绿色为真实分布，蓝色为核密度估计。</p></figure>

式（2.249）也可以选择任何其他核函数 $k(\mathbf{u})$，只要满足

$$
k(\mathbf{u})\geqslant0,
\tag{2.251}
$$

$$
\int k(\mathbf{u})\,\mathrm{d}\mathbf{u}=1.
\tag{2.252}
$$

这两个条件保证最终的概率分布处处非负，并且积分为 1。式（2.249）给出的这类密度模型称为*核密度估计*（kernel density estimator），也称 *Parzen 估计*。它的一个很大优点是“训练”阶段无需计算，只需存储训练集。不过，这也是它的一个主要弱点，因为计算密度的代价随数据集大小线性增长。

### 2.5.2 近邻方法

核密度估计的一个困难是，控制核宽度的参数 $h$ 对所有核都相同。在数据密集的区域，较大的 $h$ 可能过度平滑，抹去本可从数据中提取的结构；但缩小 $h$，又可能在密度较低的其他区域产生噪声较大的估计。因此，$h$ 的最优选择可能依赖于数据空间中的位置。近邻密度估计方法解决了这一问题。

因此，回到局部密度估计的一般结果（2.246）。这次不固定 $V$ 后根据数据确定 $K$，而是固定 $K$ 后根据数据寻找合适的 $V$。为此，以需要估计

<!-- pdf-page: 145 -->
<!-- join-previous-paragraph -->
密度 $p(\mathbf{x})$ 的点 $\mathbf{x}$ 为中心，画一个小球，并逐渐增大半径，直到球内恰好包含 $K$ 个数据点。然后用式（2.246）估计密度 $p(\mathbf{x})$，其中 $V$ 取最终球体的体积。这称为 *$K$ 近邻*（$K$ nearest neighbours）方法。图 2.26 使用与图 2.24、图 2.25 相同的数据集，展示不同参数 $K$ 下的结果。可以看到，此时由 $K$ 控制平滑程度，同样存在一个既不过大也不过小的最优选择。注意，$K$ 近邻得到的模型不是真正的密度模型，因为它在整个空间上的积分发散（习题 2.61）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-26.png" alt="不同近邻数的K近邻密度估计"><figcaption>图 2.26：$K$ 近邻密度估计示意图，数据集与图 2.25 和图 2.24 相同。参数 $K$ 控制平滑程度：较小的 $K$（上图）得到噪声很大的密度模型；较大的 $K$（下图）会将生成数据的真实分布（绿色曲线）的双峰结构抹平。</figcaption><p class="figure-translation">从上到下分别为 $K=1$、$K=5$、$K=30$；绿色为真实分布，蓝色为近邻密度估计。</p></figure>

作为本章的结尾，下面说明如何将 $K$ 近邻密度估计推广到分类问题。做法是对各类别分别应用 $K$ 近邻密度估计，再使用贝叶斯定理。假设数据集中类别 $\mathcal{C}_k$ 有 $N_k$ 个点，总数为 $N$，因此 $\sum_kN_k=N$。如果要对新点 $\mathbf{x}$ 分类，就以 $\mathbf{x}$ 为中心画一个球，使其恰好包含 $K$ 个点，而不考虑它们的类别。假设球的体积为 $V$，其中有 $K_k$ 个点来自类别 $\mathcal{C}_k$。于是，由式（2.246），各类密度的估计为

$$
p(\mathbf{x}\mid\mathcal{C}_k)=\frac{K_k}{N_kV}.
\tag{2.253}
$$

类似地，无条件密度为

$$
p(\mathbf{x})=\frac{K}{NV},
\tag{2.254}
$$

而类别先验为

$$
p(\mathcal{C}_k)=\frac{N_k}{N}.
\tag{2.255}
$$

利用贝叶斯定理将式（2.253）、（2.254）和（2.255）结合，得到类别归属的后验概率

$$
p(\mathcal{C}_k\mid\mathbf{x})=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{p(\mathbf{x})}=\frac{K_k}{K}.
\tag{2.256}
$$

<!-- pdf-page: 146 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-27.png" alt="K近邻分类器以及最近邻分类边界示意图"><figcaption>图 2.27：（a）在 $K$ 近邻分类器中，新点（黑色菱形）的类别，由距离最近的 $K$ 个训练点中的多数类别决定，这里 $K=3$。（b）最近邻（$K=1$）分类方法得到的决策边界，由不同类别成对数据点的垂直平分超平面组成。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为输入坐标；（a）$K$ 近邻多数类别判定；（b）最近邻决策边界。</p></figure>

若希望最小化误分类概率，应将测试点 $\mathbf{x}$ 归入后验概率最大的类别，也就是 $K_k/K$ 最大的类别。因此，对新点分类时，先找出训练集中最近的 $K$ 个点，再把新点归入这些点中数量最多的类别。出现并列时可以随机决定。$K=1$ 的特殊情形称为*最近邻规则*（nearest-neighbour rule）：测试点直接归入训练集中与它最近的点所属的类别。图 2.27 说明了这些概念。

图 2.28 展示了在第 1 章介绍的油流数据上，不同 $K$ 值下的 $K$ 近邻算法结果。正如预期，$K$ 控制平滑程度：较小的 $K$ 使每个类别形成许多小区域，较大的 $K$ 则产生更少、更大的区域。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-28.png" alt="油流数据在三种近邻数下的分类区域"><figcaption>图 2.28：油流数据集中的 200 个数据点，图中画出了 $x_6$ 与 $x_7$ 的关系。红色、绿色和蓝色点分别对应“层状流”（laminar）、“环状流”（annular）和“均匀流”（homogeneous）类别。图中还展示了不同 $K$ 值下，$K$ 近邻算法对输入空间给出的分类。</figcaption><p class="figure-translation">从左至右为 $K=1$、$K=3$、$K=31$；横轴 $x_6$、纵轴 $x_7$ 为输入变量；背景颜色表示预测类别。</p></figure>

<!-- pdf-page: 147 -->

最近邻（$K=1$）分类器有一个有趣的性质：在 $N\to\infty$ 的极限下，它的错误率绝不会超过最优分类器可达最小错误率的两倍；这里的最优分类器指使用真实类别分布的分类器（Cover and Hart，1967）。

按照目前的讨论，$K$ 近邻方法和核密度估计都必须存储整个训练集；数据集很大时，计算代价很高。可以通过构造树形搜索结构，在不遍历整个数据集的情况下高效找到（近似）近邻，以一次性的额外计算抵消这种代价。尽管如此，这些非参数方法仍然有很大局限。另一方面，我们已经看到，简单参数模型所能表示的分布形式也非常有限。因此，需要寻找足够灵活、同时其复杂度又能独立于训练集大小加以控制的密度模型。后续章节将介绍如何做到这一点。

## 习题

**2.1（⋆）www** 验证伯努利分布（2.2）满足以下性质：

$$
\sum_{x=0}^{1}p(x\mid\mu)=1,
\tag{2.257}
$$

$$
\mathbb{E}[x]=\mu,
\tag{2.258}
$$

$$
\operatorname{var}[x]=\mu(1-\mu).
\tag{2.259}
$$

证明服从伯努利分布的二元随机变量 $x$ 的熵为

$$
\mathrm{H}[x]=-\mu\ln\mu-(1-\mu)\ln(1-\mu).
\tag{2.260}
$$

**2.2（⋆⋆）** 式（2.2）给出的伯努利分布形式，对 $x$ 的两个取值并不对称。在一些情形下，使用 $x\in\{-1,1\}$ 的等价形式会更方便，此时分布可以写为

$$
p(x\mid\mu)=\left(\frac{1-\mu}{2}\right)^{(1-x)/2}\left(\frac{1+\mu}{2}\right)^{(1+x)/2},
\tag{2.261}
$$

其中 $\mu\in[-1,1]$。证明分布（2.261）已归一化，并求它的均值、方差和熵。

**2.3（⋆⋆）www** 本题证明二项分布（2.9）已归一化。先利用从总共 $N$ 个相同物体中选取 $m$ 个的组合数定义（2.10），证明

$$
\binom{N}{m}+\binom{N}{m-1}=\binom{N+1}{m}.
\tag{2.262}
$$

<!-- pdf-page: 148 -->

利用这个结果，通过归纳法证明

$$
(1+x)^N=\sum_{m=0}^{N}\binom{N}{m}x^m,
\tag{2.263}
$$

这称为*二项式定理*（binomial theorem），对任意实数 $x$ 都成立。最后，证明二项分布已归一化，即

$$
\sum_{m=0}^{N}\binom{N}{m}\mu^m(1-\mu)^{N-m}=1.
\tag{2.264}
$$

可以先从求和中提取因子 $(1-\mu)^N$，再使用二项式定理。

**2.4（⋆⋆）** 证明二项分布的均值由式（2.11）给出。为此，将归一化条件（2.264）两边对 $\mu$ 求导，再整理得到 $n$ 的均值表达式。类似地，将式（2.264）对 $\mu$ 求两次导数，并利用二项分布均值的结果（2.11），证明方差的结果（2.12）。

**2.5（⋆⋆）www** 本题证明式（2.13）给出的Beta 分布已正确归一化，即式（2.14）成立。这等价于证明

$$
\int_0^1\mu^{a-1}(1-\mu)^{b-1}\,\mathrm{d}\mu=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}.
\tag{2.265}
$$

由伽马函数定义（1.141），有

$$
\Gamma(a)\Gamma(b)=\int_0^{\infty}\exp(-x)x^{a-1}\,\mathrm{d}x\int_0^{\infty}\exp(-y)y^{b-1}\,\mathrm{d}y.
\tag{2.266}
$$

按以下步骤利用这个表达式证明式（2.265）：先将对 $y$ 的积分移入对 $x$ 积分的被积函数中；再固定 $x$，作变量代换 $t=y+x$；然后交换 $x$ 和 $t$ 的积分顺序；最后固定 $t$，作变量代换 $x=t\mu$。

**2.6（⋆）** 利用结果（2.265），证明Beta 分布（2.13）的均值、方差和众数分别为

$$
\mathbb{E}[\mu]=\frac{a}{a+b},
\tag{2.267}
$$

$$
\operatorname{var}[\mu]=\frac{ab}{(a+b)^2(a+b+1)},
\tag{2.268}
$$

$$
\operatorname{mode}[\mu]=\frac{a-1}{a+b-2}.
\tag{2.269}
$$

<!-- pdf-page: 149 -->

**2.7（⋆⋆）** 考虑式（2.9）给出的二项随机变量 $x$，$\mu$ 的先验为Beta 分布（2.13）。假设观测到 $m$ 次 $x=1$ 和 $l$ 次 $x=0$。证明，$x$ 的后验均值位于先验均值与 $\mu$ 的最大似然估计之间。为此，证明后验均值可以写为先验均值乘以 $\lambda$，加上最大似然估计乘以 $1-\lambda$，其中 $0\leqslant\lambda\leqslant1$。这说明后验分布在先验分布与最大似然解之间作出了折中。

**2.8（⋆）** 考虑具有联合分布 $p(x,y)$ 的两个变量 $x$ 和 $y$。证明以下两个结果：

$$
\mathbb{E}[x]=\mathbb{E}_y\bigl[\mathbb{E}_x[x\mid y]\bigr],
\tag{2.270}
$$

$$
\operatorname{var}[x]=\mathbb{E}_y\bigl[\operatorname{var}_x[x\mid y]\bigr]+\operatorname{var}_y\bigl[\mathbb{E}_x[x\mid y]\bigr].
\tag{2.271}
$$

这里，$\mathbb{E}_x[x\mid y]$ 表示条件分布 $p(x\mid y)$ 下 $x$ 的期望，条件方差的记号含义类似。

**2.9（⋆⋆⋆）www** 本题利用归纳法证明狄利克雷分布（2.38）的归一化。习题 2.5 已经证明，Beta 分布是归一化的，它是 $M=2$ 时狄利克雷分布的特例。现在假设 $M-1$ 个变量的狄利克雷分布已归一化，证明 $M$ 个变量时也归一化。为此，考虑 $M$ 个变量的狄利克雷分布，利用约束 $\sum_{k=1}^{M}\mu_k=1$ 消去 $\mu_M$，将分布写为

$$
p_M(\mu_1,\ldots,\mu_{M-1})=C_M\prod_{k=1}^{M-1}\mu_k^{\alpha_k-1}\left(1-\sum_{j=1}^{M-1}\mu_j\right)^{\alpha_M-1}.
\tag{2.272}
$$

目标是求出 $C_M$ 的表达式。先对 $\mu_{M-1}$ 积分，注意积分限，再作变量代换，使积分限成为 0 和 1。假设 $C_{M-1}$ 的正确结果成立，并利用式（2.265），推导 $C_M$ 的表达式。

**2.10（⋆⋆）** 利用伽马函数性质 $\Gamma(x+1)=x\Gamma(x)$，推导狄利克雷分布（2.38）的均值、方差和协方差的以下结果：

$$
\mathbb{E}[\mu_j]=\frac{\alpha_j}{\alpha_0},
\tag{2.273}
$$

$$
\operatorname{var}[\mu_j]=\frac{\alpha_j(\alpha_0-\alpha_j)}{\alpha_0^2(\alpha_0+1)},
\tag{2.274}
$$

$$
\operatorname{cov}[\mu_j\mu_l]=-\frac{\alpha_j\alpha_l}{\alpha_0^2(\alpha_0+1)},\qquad j\ne l,
\tag{2.275}
$$

其中 $\alpha_0$ 由式（2.39）定义。

<!-- pdf-page: 150 -->

**2.11（⋆）www** 将狄利克雷分布（2.38）下 $\ln\mu_j$ 的期望表示为对 $\alpha_j$ 的导数，证明

$$
\mathbb{E}[\ln\mu_j]=\psi(\alpha_j)-\psi(\alpha_0),
\tag{2.276}
$$

其中 $\alpha_0$ 由式（2.39）给出，而

$$
\psi(a)\equiv\frac{\mathrm{d}}{\mathrm{d}a}\ln\Gamma(a)
\tag{2.277}
$$

是 *digamma 函数*。

**2.12（⋆）** 连续变量 $x$ 的均匀分布定义为

$$
\mathrm{U}(x\mid a,b)=\frac1{b-a},\qquad a\leqslant x\leqslant b.
\tag{2.278}
$$

验证该分布已归一化，并求出其均值和方差的表达式。

**2.13（⋆⋆）** 计算两个高斯分布 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 和 $q(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\mathbf{m},\mathbf{L})$ 之间的 Kullback–Leibler 散度（1.113）。

**2.14（⋆⋆）www** 本题说明，给定协方差时，熵最大的多元分布是高斯分布。分布 $p(\mathbf{x})$ 的熵为

$$
\mathrm{H}[\mathbf{x}]=-\int p(\mathbf{x})\ln p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{2.279}
$$

我们希望在所有 $p(\mathbf{x})$ 中最大化 $\mathrm{H}[\mathbf{x}]$，约束条件是 $p(\mathbf{x})$ 归一化，并且具有指定的均值和协方差，即

$$
\int p(\mathbf{x})\,\mathrm{d}\mathbf{x}=1,
\tag{2.280}
$$

$$
\int p(\mathbf{x})\mathbf{x}\,\mathrm{d}\mathbf{x}=\boldsymbol{\mu},
\tag{2.281}
$$

$$
\int p(\mathbf{x})(\mathbf{x}-\boldsymbol{\mu})(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\,\mathrm{d}\mathbf{x}=\boldsymbol{\Sigma}.
\tag{2.282}
$$

对式（2.279）作变分最大化，并用拉格朗日乘子施加约束（2.280）、（2.281）、（2.282），证明最大似然分布由高斯分布（2.43）给出。

**2.15（⋆⋆）** 证明多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 的熵为

$$
\mathrm{H}[\mathbf{x}]=\frac12\ln|\boldsymbol{\Sigma}|+\frac D2(1+\ln(2\pi)),
\tag{2.283}
$$

其中 $D$ 为 $\mathbf{x}$ 的维数。

<!-- pdf-page: 151 -->

**2.16（⋆⋆⋆）www** 考虑两个随机变量 $x_1$ 和 $x_2$，它们分别服从均值为 $\mu_1$、$\mu_2$，精度为 $\tau_1$、$\tau_2$ 的高斯分布。推导变量 $x=x_1+x_2$ 的微分熵表达式。为此，先利用关系

$$
p(x)=\int_{-\infty}^{\infty}p(x\mid x_2)p(x_2)\,\mathrm{d}x_2
\tag{2.284}
$$

并在指数中配方，求出 $x$ 的分布。然后注意，这表示两个高斯分布的卷积，其结果本身也是高斯分布；最后利用一元高斯熵的结果（1.110）。

**2.17（⋆）www** 考虑式（2.43）给出的多元高斯分布。将精度矩阵（协方差逆矩阵）$\boldsymbol{\Sigma}^{-1}$ 写为对称矩阵与反对称矩阵之和，证明反对称项不出现在高斯分布的指数中，因此不失一般性，可以令精度矩阵对称。由于对称矩阵的逆矩阵也对称（见习题 2.22），所以不失一般性，也可以令协方差矩阵对称。

**2.18（⋆⋆⋆）** 考虑实对称矩阵 $\boldsymbol{\Sigma}$，其特征值方程由式（2.45）给出。对方程取复共轭并减去原方程，再与特征向量 $\mathbf{u}_i$ 作内积，证明特征值 $\lambda_i$ 为实数。类似地，利用 $\boldsymbol{\Sigma}$ 的对称性，证明只要 $\lambda_j\ne\lambda_i$，特征向量 $\mathbf{u}_i$ 与 $\mathbf{u}_j$ 就正交。最后证明，不失一般性，即使某些特征值为零，也可以选择一组标准正交的特征向量，使它们满足式（2.46）。

**2.19（⋆⋆）** 证明：具有特征向量方程（2.45）的实对称矩阵 $\boldsymbol{\Sigma}$，可以展开为以特征向量为基、特征值为系数的形式，即式（2.48）。类似地，证明逆矩阵 $\boldsymbol{\Sigma}^{-1}$ 具有式（2.49）的表示。

**2.20（⋆⋆）www** 正定矩阵 $\boldsymbol{\Sigma}$ 可以定义为：对向量 $\mathbf{a}$ 的任意实数取值，二次型

$$
\mathbf{a}^{\mathrm T}\boldsymbol{\Sigma}\mathbf{a}
\tag{2.285}
$$

都为正。证明：$\boldsymbol{\Sigma}$ 正定的充要条件，是式（2.45）定义的所有特征值 $\lambda_i$ 均为正。

**2.21（⋆）** 证明，一个 $D\times D$ 的实对称矩阵具有 $D(D+1)/2$ 个独立参数。

**2.22（⋆）www** 证明对称矩阵的逆矩阵本身也是对称矩阵。

**2.23（⋆⋆）** 利用特征向量展开（2.45）将坐标系对角化，证明对应于马氏距离

<!-- pdf-page: 152 -->
<!-- join-previous-paragraph -->
恒为 $\Delta$ 的超椭球，其内部体积为

$$
V_D|\boldsymbol{\Sigma}|^{1/2}\Delta^D,
\tag{2.286}
$$

其中 $V_D$ 是 $D$ 维单位球的体积，马氏距离由式（2.44）定义。

**2.24（⋆⋆）www** 在恒等式（2.76）的两边乘以矩阵

$$
\begin{pmatrix}\mathbf{A}&\mathbf{B}\\\mathbf{C}&\mathbf{D}\end{pmatrix},
\tag{2.287}
$$

并利用定义（2.77），证明该恒等式。

**2.25（⋆⋆）** 第 2.3.1 节和第 2.3.2 节讨论了多元高斯分布的条件分布与边缘分布。更一般地，可以将 $\mathbf{x}$ 的分量划分为三组 $\mathbf{x}_a$、$\mathbf{x}_b$ 和 $\mathbf{x}_c$，相应地将均值向量 $\boldsymbol{\mu}$ 与协方差矩阵 $\boldsymbol{\Sigma}$ 划分为

$$
\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\\\boldsymbol{\mu}_c\end{pmatrix},\qquad
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}&\boldsymbol{\Sigma}_{ac}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}&\boldsymbol{\Sigma}_{bc}\\\boldsymbol{\Sigma}_{ca}&\boldsymbol{\Sigma}_{cb}&\boldsymbol{\Sigma}_{cc}\end{pmatrix}.
\tag{2.288}
$$

利用第 2.3 节的结果，求出将 $\mathbf{x}_c$ 边缘化后，条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的表达式。

**2.26（⋆⋆）** 线性代数中一个很有用的结果是 *Woodbury 矩阵求逆公式*：

$$
(\mathbf{A}+\mathbf{B}\mathbf{C}\mathbf{D})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{B}(\mathbf{C}^{-1}+\mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1}\mathbf{D}\mathbf{A}^{-1}.
\tag{2.289}
$$

将两边乘以 $(\mathbf{A}+\mathbf{B}\mathbf{C}\mathbf{D})$，证明这个结果正确。

**2.27（⋆）** 设 $\mathbf{x}$ 与 $\mathbf{z}$ 为两个独立随机向量，即 $p(\mathbf{x},\mathbf{z})=p(\mathbf{x})p(\mathbf{z})$。证明，它们之和 $\mathbf{y}=\mathbf{x}+\mathbf{z}$ 的均值等于两个变量各自均值之和。类似地，证明 $\mathbf{y}$ 的协方差矩阵等于 $\mathbf{x}$ 与 $\mathbf{z}$ 的协方差矩阵之和。确认这个结果与习题 1.10 一致。

**2.28（⋆⋆⋆）www** 考虑变量

$$
\mathbf{z}=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}
\tag{2.290}
$$

的联合分布，其均值和协方差分别由式（2.108）与（2.105）给出。利用结果（2.92）和（2.93），证明边缘分布 $p(\mathbf{x})$ 由式（2.99）给出。类似地，利用结果（2.81）和（2.82），证明条件分布 $p(\mathbf{y}\mid\mathbf{x})$ 由式（2.100）给出。

<!-- pdf-page: 153 -->

**2.29（⋆⋆）** 利用分块矩阵求逆公式（2.76），证明精度矩阵（2.104）的逆矩阵就是协方差矩阵（2.105）。

**2.30（⋆）** 从式（2.107）出发，并利用结果（2.105），验证结果（2.108）。

**2.31（⋆⋆）** 考虑两个多维随机向量 $\mathbf{x}$ 和 $\mathbf{z}$，分别服从高斯分布 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_x,\boldsymbol{\Sigma}_x)$ 和 $p(\mathbf{z})=\mathcal{N}(\mathbf{z}\mid\boldsymbol{\mu}_z,\boldsymbol{\Sigma}_z)$，以及它们的和 $\mathbf{y}=\mathbf{x}+\mathbf{z}$。考虑由边缘分布 $p(\mathbf{x})$ 与条件分布 $p(\mathbf{y}\mid\mathbf{x})$ 的乘积构成的线性高斯模型，利用结果（2.109）和（2.110），求出边缘分布 $p(\mathbf{y})$ 的表达式。

**2.32（⋆⋆⋆）www** 本题和下一题用于练习处理线性高斯模型中的二次型，同时独立核对正文推导的结果。考虑由边缘分布（2.99）和条件分布（2.100）定义的联合分布 $p(\mathbf{x},\mathbf{y})$。考察联合分布指数中的二次型，使用第 2.3 节讨论的“配方”方法，求出将变量 $\mathbf{x}$ 积分消去后，边缘分布 $p(\mathbf{y})$ 的均值和协方差表达式。为此，使用 Woodbury 矩阵求逆公式（2.289）。验证这些结果与利用第 2 章结果所得的式（2.109）、（2.110）一致。

**2.33（⋆⋆⋆）** 考虑与习题 2.32 相同的联合分布，这次用配方方法求出条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 的均值和协方差。再次验证，它们与相应的式（2.111）、（2.112）一致。

**2.34（⋆⋆）www** 为求多元高斯分布协方差矩阵的最大似然解，需要关于 $\boldsymbol{\Sigma}$ 最大化对数似然函数（2.118），同时注意协方差矩阵必须对称且正定。这里先忽略这些约束，直接最大化。利用附录 C 的结果（C.21）、（C.26）和（C.28），证明使对数似然函数（2.118）最大的协方差矩阵 $\boldsymbol{\Sigma}$，由样本协方差（2.122）给出。注意，最终结果必然对称且正定（只要样本协方差非奇异）。

**2.35（⋆⋆）** 利用结果（2.59）证明式（2.62）。然后结合结果（2.59）和（2.62），证明

$$
\mathbb{E}[\mathbf{x}_n\mathbf{x}_m]=\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}+I_{nm}\boldsymbol{\Sigma},
\tag{2.291}
$$

其中 $\mathbf{x}_n$ 表示从均值为 $\boldsymbol{\mu}$、协方差为 $\boldsymbol{\Sigma}$ 的高斯分布抽取的数据点，$I_{nm}$ 为单位矩阵的第 $(n,m)$ 个元素。由此证明结果（2.124）。

**2.36（⋆⋆）www** 采用与推导式（2.126）类似的步骤，推导一元高斯

<!-- pdf-page: 154 -->
<!-- join-previous-paragraph -->
分布方差的序贯估计表达式，从以下最大似然表达式出发：

$$
\sigma_{\mathrm{ML}}^2=\frac1N\sum_{n=1}^{N}(x_n-\mu)^2.
\tag{2.292}
$$

验证，将高斯分布的表达式代入 Robbins–Monro 序贯估计公式（2.135），会得到相同形式的结果，并由此求出相应系数 $a_N$ 的表达式。

**2.37（⋆⋆）** 采用与推导式（2.126）类似的步骤，从最大似然表达式（2.122）出发，推导多元高斯分布协方差的序贯估计表达式。验证，将高斯分布的表达式代入 Robbins–Monro 序贯估计公式（2.135），会得到相同形式的结果，并由此求出相应系数 $a_N$ 的表达式。

**2.38（⋆）** 对指数中的二次型使用配方方法，推导结果（2.141）和（2.142）。

**2.39（⋆⋆）** 从高斯随机变量均值的后验分布结果（2.141）和（2.142）出发，分离前 $N-1$ 个数据点的贡献，由此求出 $\mu_N$ 和 $\sigma_N^2$ 的序贯更新表达式。再从后验分布 $p(\mu\mid x_1,\ldots,x_{N-1})=\mathcal{N}(\mu\mid\mu_{N-1},\sigma_{N-1}^2)$ 出发，乘以似然函数 $p(x_N\mid\mu)=\mathcal{N}(x_N\mid\mu,\sigma^2)$，通过配方并归一化得到 $N$ 次观测后的后验分布，从而推导相同的结果。

**2.40（⋆⋆）www** 考虑 $D$ 维高斯随机变量 $\mathbf{x}$，其分布为 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，协方差 $\boldsymbol{\Sigma}$ 已知。我们希望根据观测集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 推断均值 $\boldsymbol{\mu}$。给定先验分布 $p(\boldsymbol{\mu})=\mathcal{N}(\boldsymbol{\mu}\mid\boldsymbol{\mu}_0,\boldsymbol{\Sigma}_0)$，求相应的后验分布 $p(\boldsymbol{\mu}\mid\mathbf{X})$。

**2.41（⋆）** 利用伽马函数定义（1.141），证明伽马分布（2.146）已归一化。

**2.42（⋆⋆）** 求伽马分布（2.146）的均值、方差和众数。

**2.43（⋆）** 以下分布是一元高斯分布的推广：

$$
p(x\mid\sigma^2,q)=\frac{q}{2(2\sigma^2)^{1/q}\Gamma(1/q)}\exp\left(-\frac{|x|^q}{2\sigma^2}\right).
\tag{2.293}
$$

证明它已归一化，即

$$
\int_{-\infty}^{\infty}p(x\mid\sigma^2,q)\,\mathrm{d}x=1,
\tag{2.294}
$$

并且在 $q=2$ 时退化为高斯分布。考虑一个回归模型，目标变量为 $t=y(\mathbf{x},\mathbf{w})+\epsilon$，其中 $\epsilon$ 是从分布（2.293）抽取的随机噪声

<!-- pdf-page: 155 -->
<!-- join-previous-paragraph -->
变量。证明，对于由输入向量 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 和相应目标变量 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$ 组成的观测数据集，关于 $\mathbf{w}$ 和 $\sigma^2$ 的对数似然函数为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\sigma^2)=-\frac1{2\sigma^2}\sum_{n=1}^{N}|y(\mathbf{x}_n,\mathbf{w})-t_n|^q-\frac Nq\ln(2\sigma^2)+\mathrm{const},
\tag{2.295}
$$

其中 “const” 表示与 $\mathbf{w}$ 及 $\sigma^2$ 都无关的项。注意，将其看作 $\mathbf{w}$ 的函数，它就是第 1.5.5 节讨论的 $L_q$ 误差函数。

**2.44（⋆⋆）** 考虑一元高斯分布 $\mathcal{N}(x\mid\mu,\tau^{-1})$，其共轭高斯-伽马先验由式（2.154）给出。给定独立同分布观测构成的数据集 $\boldsymbol{\mathsf{x}}=\{x_1,\ldots,x_N\}$，证明后验分布仍为与先验具有相同函数形式的高斯-伽马分布，并写出后验分布各参数的表达式。

**2.45（⋆）** 验证式（2.155）定义的 Wishart 分布，确实是多元高斯分布精度矩阵的共轭先验。

**2.46（⋆）www** 验证，计算式（2.158）中的积分会得到结果（2.159）。

**2.47（⋆）www** 证明，在 $\nu\to\infty$ 的极限下，t 分布（2.159）变为高斯分布。提示：忽略归一化系数，只考察对 $x$ 的依赖。

**2.48（⋆）** 按照与推导一元 Student t 分布（2.159）类似的步骤，对式（2.161）中的变量 $\eta$ 进行边缘化，验证多元 Student t 分布的结果（2.162）。利用定义（2.161），通过交换积分变量，证明多元 t 分布正确归一化。

**2.49（⋆⋆）** 利用式（2.161）把多元 Student t 分布定义为高斯分布与伽马分布的卷积，验证式（2.162）定义的多元 t 分布的性质（2.164）、（2.165）和（2.166）。

**2.50（⋆）** 证明，在 $\nu\to\infty$ 的极限下，多元 Student t 分布（2.162）退化为均值 $\boldsymbol{\mu}$、精度 $\boldsymbol{\Lambda}$ 的高斯分布。

**2.51（⋆）www** 本章讨论周期变量时使用的各种三角恒等式，都可以容易地由以下关系证明：

$$
\exp(\mathrm{i}A)=\cos A+\mathrm{i}\sin A,
\tag{2.296}
$$

其中 $\mathrm{i}$ 是负一的平方根。考虑恒等式

$$
\exp(\mathrm{i}A)\exp(-\mathrm{i}A)=1,
\tag{2.297}
$$

证明结果（2.177）。类似地，利用恒等式

$$
\cos(A-B)=\Re\exp\{\mathrm{i}(A-B)\},
\tag{2.298}
$$

<!-- pdf-page: 156 -->

其中 $\Re$ 表示实部，证明式（2.178）。最后，利用 $\sin(A-B)=\Im\exp\{\mathrm{i}(A-B)\}$（$\Im$ 表示虚部），证明结果（2.183）。

**2.52（⋆⋆）** 当 $m$ 很大时，von Mises 分布（2.179）在众数 $\theta_0$ 附近形成尖峰。定义 $\xi=m^{1/2}(\theta-\theta_0)$，并使用余弦函数的泰勒展开

$$
\cos\alpha=1-\frac{\alpha^2}{2}+O(\alpha^4),
\tag{2.299}
$$

证明当 $m\to\infty$ 时，von Mises 分布趋于高斯分布。

**2.53（⋆）** 利用三角恒等式（2.183），证明式（2.182）关于 $\theta_0$ 的解由式（2.184）给出。

**2.54（⋆）** 计算 von Mises 分布（2.179）的一阶和二阶导数，并利用 $m>0$ 时 $I_0(m)>0$，证明分布在 $\theta=\theta_0$ 时取最大值，在 $\theta=\theta_0+\pi\pmod{2\pi}$ 时取最小值。

**2.55（⋆）** 结合结果（2.168）、（2.184）与三角恒等式（2.178），证明 von Mises 分布集中参数的最大似然解 $m_{\mathrm{ML}}$ 满足 $A(m_{\mathrm{ML}})=\overline{r}$，其中 $\overline{r}$ 是将观测看作二维欧氏平面上的单位向量后，其平均向量的长度，如图 2.17 所示。

**2.56（⋆⋆）www** 将Beta 分布（2.13）、伽马分布（2.146）和 von Mises 分布（2.179）写成指数族（2.194）的成员，并确定它们的自然参数。

**2.57（⋆）** 验证多元高斯分布可以写成指数族形式（2.194），并推导与式（2.220）至（2.223）类似的 $\boldsymbol{\eta}$、$\mathbf{u}(\mathbf{x})$、$h(\mathbf{x})$ 和 $g(\boldsymbol{\eta})$ 的表达式。

**2.58（⋆）** 结果（2.226）表明，指数族中 $\ln g(\boldsymbol{\eta})$ 的负梯度由 $\mathbf{u}(\mathbf{x})$ 的期望给出。对式（2.195）求二阶导数，证明

$$
-\nabla\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})\mathbf{u}(\mathbf{x})^{\mathrm T}]-\mathbb{E}[\mathbf{u}(\mathbf{x})]\mathbb{E}[\mathbf{u}(\mathbf{x})^{\mathrm T}]=\operatorname{cov}[\mathbf{u}(\mathbf{x})].
\tag{2.300}
$$

**2.59（⋆）** 作变量代换 $y=x/\sigma$，证明只要 $f(x)$ 正确归一化，密度（2.236）也会正确归一化。

**2.60（⋆⋆）www** 考虑类似直方图的密度模型：将空间 $\mathbf{x}$ 划分为固定区域，第 $i$ 个区域内密度 $p(\mathbf{x})$ 取常数 $h_i$，区域体积记为 $\Delta_i$。假设有 $N$ 个关于 $\mathbf{x}$ 的观测，其中 $n_i$ 个落在第 $i$ 个区域。利用拉格朗日乘子施加密度归一化约束，推导 $\{h_i\}$ 的最大似然估计表达式。

**2.61（⋆）** 证明，$K$ 近邻密度模型定义了一个非正常分布，它在整个空间上的积分发散。
