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
