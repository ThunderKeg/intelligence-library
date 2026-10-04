# 附录 B 概率分布

<aside class="chapter-guide"><strong>附录导读</strong><p>本附录可作为概率分布的速查资料，列出参数范围、概率密度或概率质量函数、常用统计量及共轭关系。使用时应同时核对变量的取值范围和参数约束，并留意一元与多元高斯分布的参数写法。</p></aside>

<!-- pdf-page: 705 -->

本附录概述若干最常用概率分布的主要性质，并为每种分布列出一些关键统计量，例如期望 $\mathbb{E}[x]$、方差或协方差、众数，以及熵 $\mathrm{H}[x]$。这些分布都是指数族的成员，广泛用于构造更复杂的概率模型。

## 伯努利分布

这是单个二元变量 $x\in\{0,1\}$ 的分布，例如可以表示一次抛硬币的结果。它由一个连续参数 $\mu\in[0,1]$ 控制，该参数表示 $x=1$ 的概率。

$$
\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}
\tag{B.1}
$$

$$
\mathbb{E}[x]=\mu
\tag{B.2}
$$

$$
\operatorname{var}[x]=\mu(1-\mu)
\tag{B.3}
$$

$$
\operatorname{mode}[x]=\begin{cases}1&\text{若 }\mu\geqslant0.5,\\0&\text{其他情况}\end{cases}
\tag{B.4}
$$

$$
\mathrm{H}[x]=-\mu\ln\mu-(1-\mu)\ln(1-\mu).
\tag{B.5}
$$

伯努利分布是二项分布在只有一个观测时的特例。其参数 $\mu$ 的共轭先验为 Beta 分布。

<!-- pdf-page: 706 -->

## Beta 分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/a-beta.png" alt="四组不同参数下的Beta概率密度曲线"></figure>

这是连续变量 $\mu\in[0,1]$ 上的分布，常用于表示某个二元事件的概率。它由两个参数 $a$ 和 $b$ 控制，为保证分布可以归一化，参数需满足 $a>0$ 和 $b>0$。

$$
\operatorname{Beta}(\mu\mid a,b)=\frac{\Gamma(a+b)}{\Gamma(a)\Gamma(b)}\mu^{a-1}(1-\mu)^{b-1}
\tag{B.6}
$$

$$
\mathbb{E}[\mu]=\frac{a}{a+b}
\tag{B.7}
$$

$$
\operatorname{var}[\mu]=\frac{ab}{(a+b)^2(a+b+1)}
\tag{B.8}
$$

$$
\operatorname{mode}[\mu]=\frac{a-1}{a+b-2}.
\tag{B.9}
$$

Beta 分布是伯努利分布的共轭先验，其中 $a$ 和 $b$ 可以分别解释为 $x=1$ 和 $x=0$ 的有效先验观测次数。当 $a\geqslant1$ 且 $b\geqslant1$ 时，其密度为有限值；否则，在 $\mu=0$ 和/或 $\mu=1$ 处存在奇点。当 $a=b=1$ 时，它化为均匀分布。Beta 分布是具有 $K$ 个状态的狄利克雷分布在 $K=2$ 时的特例。

## 二项分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/a-binomial.png" alt="二项分布的概率质量柱状图"></figure>

从一个伯努利分布中抽取 $N$ 个样本，其中观测到 $x=1$ 的概率为 $\mu\in[0,1]$；二项分布给出了这些样本中 $x=1$ 出现 $m$ 次的概率。

$$
\operatorname{Bin}(m\mid N,\mu)=\binom{N}{m}\mu^m(1-\mu)^{N-m}
\tag{B.10}
$$

$$
\mathbb{E}[m]=N\mu
\tag{B.11}
$$

$$
\operatorname{var}[m]=N\mu(1-\mu)
\tag{B.12}
$$

$$
\operatorname{mode}[m]=\lfloor(N+1)\mu\rfloor
\tag{B.13}
$$

其中，$\lfloor(N+1)\mu\rfloor$ 表示不大于 $(N+1)\mu$ 的最大整数，而

$$
\binom{N}{m}=\frac{N!}{m!(N-m)!}
\tag{B.14}
$$

表示从总共 $N$ 个相同物体中选出 $m$ 个的方式数。这里，$m!$ 读作“$m$ 的阶乘”，表示乘积 $m\times(m-1)\times\ldots\times2\times1$。二项分布在 $N=1$ 时的特例称为伯努利分布；当 $N$ 很大时，二项分布近似为高斯分布。$\mu$ 的共轭先验为 Beta 分布。

<!-- pdf-page: 707 -->

## 狄利克雷分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/a-dirichlet.png" alt="狄利克雷分布的三维密度曲面缩略图"></figure>

狄利克雷分布是定义在 $K$ 个随机变量 $0\leqslant\mu_k\leqslant1$ 上的多元分布，其中 $k=1,\ldots,K$，并满足约束

$$
0\leqslant\mu_k\leqslant1,\qquad\sum_{k=1}^{K}\mu_k=1.
\tag{B.15}
$$

记 $\boldsymbol{\mu}=(\mu_1,\ldots,\mu_K)^{\mathrm{T}}$、$\boldsymbol{\alpha}=(\alpha_1,\ldots,\alpha_K)^{\mathrm{T}}$，则有

$$
\operatorname{Dir}(\boldsymbol{\mu}\mid\boldsymbol{\alpha})=C(\boldsymbol{\alpha})\prod_{k=1}^{K}\mu_k^{\alpha_k-1}
\tag{B.16}
$$

$$
\mathbb{E}[\mu_k]=\frac{\alpha_k}{\widehat{\alpha}}
\tag{B.17}
$$

$$
\operatorname{var}[\mu_k]=\frac{\alpha_k(\widehat{\alpha}-\alpha_k)}{\widehat{\alpha}^{2}(\widehat{\alpha}+1)}
\tag{B.18}
$$

$$
\operatorname{cov}[\mu_j\mu_k]=-\frac{\alpha_j\alpha_k}{\widehat{\alpha}^{2}(\widehat{\alpha}+1)}
\tag{B.19}
$$

$$
\operatorname{mode}[\mu_k]=\frac{\alpha_k-1}{\widehat{\alpha}-K}
\tag{B.20}
$$

$$
\mathbb{E}[\ln\mu_k]=\psi(\alpha_k)-\psi(\widehat{\alpha})
\tag{B.21}
$$

$$
\mathrm{H}[\boldsymbol{\mu}]=-\sum_{k=1}^{K}(\alpha_k-1)\{\psi(\alpha_k)-\psi(\widehat{\alpha})\}-\ln C(\boldsymbol{\alpha})
\tag{B.22}
$$

其中

$$
C(\boldsymbol{\alpha})=\frac{\Gamma(\widehat{\alpha})}{\Gamma(\alpha_1)\cdots\Gamma(\alpha_K)}
\tag{B.23}
$$

并且

$$
\widehat{\alpha}=\sum_{k=1}^{K}\alpha_k.
\tag{B.24}
$$

这里，

$$
\psi(a)\equiv\frac{d}{da}\ln\Gamma(a)
\tag{B.25}
$$

称为 digamma 函数（Abramowitz 和 Stegun，1965）。为保证分布可以归一化，参数 $\alpha_k$ 需满足约束 $\alpha_k>0$。

狄利克雷分布是多项分布的共轭先验，也是 Beta 分布的推广。此时，参数 $\alpha_k$ 可以解释为 $K$ 维二元观测向量 $\mathbf{x}$ 相应取值的有效观测次数。与 Beta 分布一样，只要所有 $k$ 都满足 $\alpha_k\geqslant1$，狄利克雷分布的密度就在各处均为有限值。

<!-- pdf-page: 708 -->

## 伽马分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/a-gamma.png" alt="三组不同参数下的伽马概率密度曲线"></figure>

伽马分布是正随机变量 $\tau>0$ 上的概率分布，由参数 $a$ 和 $b$ 控制。为保证分布可以归一化，参数需满足约束 $a>0$ 和 $b>0$。

$$
\operatorname{Gam}(\tau\mid a,b)=\frac{1}{\Gamma(a)}b^a\tau^{a-1}e^{-b\tau}
\tag{B.26}
$$

$$
\mathbb{E}[\tau]=\frac{a}{b}
\tag{B.27}
$$

$$
\operatorname{var}[\tau]=\frac{a}{b^2}
\tag{B.28}
$$

$$
\operatorname{mode}[\tau]=\frac{a-1}{b}\quad\text{当}\;\alpha\geqslant1
\tag{B.29}
$$

$$
\mathbb{E}[\ln\tau]=\psi(a)-\ln b
\tag{B.30}
$$

$$
\mathrm{H}[\tau]=\ln\Gamma(a)-(a-1)\psi(a)-\ln b+a
\tag{B.31}
$$

其中 $\psi(\cdot)$ 是式（B.25）定义的 digamma 函数。伽马分布是一元高斯分布的精度（方差的倒数）的共轭先验。当 $a\geqslant1$ 时，密度在各处均为有限值；$a=1$ 这一特例称为指数分布。

## 高斯分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/a-gaussian.png" alt="三个不同方差下的高斯概率密度曲线"></figure>

高斯分布是连续变量最常用的分布，也称为正态分布。对于单个变量 $x\in(-\infty,\infty)$，它由两个参数控制，即均值 $\mu\in(-\infty,\infty)$ 和方差 $\sigma^2>0$。

$$
\mathcal{N}(x\mid\mu,\sigma^2)=\frac{1}{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac{1}{2\sigma^2}(x-\mu)^2\right\}
\tag{B.32}
$$

$$
\mathbb{E}[x]=\mu
\tag{B.33}
$$

$$
\operatorname{var}[x]=\sigma^2
\tag{B.34}
$$

$$
\operatorname{mode}[x]=\mu
\tag{B.35}
$$

$$
\mathrm{H}[x]=\frac{1}{2}\ln\sigma^2+\frac{1}{2}(1+\ln(2\pi)).
\tag{B.36}
$$

方差的倒数 $\tau=1/\sigma^2$ 称为精度，方差的平方根 $\sigma$ 称为标准差。$\mu$ 的共轭先验为高斯分布，$\tau$ 的共轭先验为伽马分布。如果 $\mu$ 和 $\tau$ 都未知，那么它们的联合共轭先验就是高斯-伽马分布。

对于 $D$ 维向量 $\mathbf{x}$，高斯分布由一个 $D$ 维均值向量 $\boldsymbol{\mu}$ 和一个 $D\times D$ 的协方差矩阵 $\boldsymbol{\Sigma}$ 控制，该矩阵必须对称且

<!-- pdf-page: 709 -->
<!-- join-previous-paragraph -->

正定。

$$
\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}
\tag{B.37}
$$

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}
\tag{B.38}
$$

$$
\operatorname{cov}[\mathbf{x}]=\boldsymbol{\Sigma}
\tag{B.39}
$$

$$
\operatorname{mode}[\mathbf{x}]=\boldsymbol{\mu}
\tag{B.40}
$$

$$
\mathrm{H}[\mathbf{x}]=\frac{1}{2}\ln|\boldsymbol{\Sigma}|+\frac{D}{2}(1+\ln(2\pi)).
\tag{B.41}
$$

协方差矩阵的逆 $\boldsymbol{\Lambda}=\boldsymbol{\Sigma}^{-1}$ 是精度矩阵，它也对称且正定。根据中心极限定理，随机变量的平均值趋于高斯分布，而两个高斯变量之和仍然服从高斯分布。给定方差或协方差时，高斯分布的熵最大。对高斯随机变量作任何线性变换，得到的变量仍服从高斯分布。多元高斯分布对某个变量子集的边缘分布仍是高斯分布，同样，其条件分布也为高斯分布。$\boldsymbol{\mu}$ 的共轭先验为高斯分布，$\boldsymbol{\Lambda}$ 的共轭先验为 Wishart 分布，而 $(\boldsymbol{\mu},\boldsymbol{\Lambda})$ 的共轭先验为高斯 Wishart 分布。

若 $\mathbf{x}$ 的边缘高斯分布和给定 $\mathbf{x}$ 时 $\mathbf{y}$ 的条件高斯分布具有如下形式：

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1})
\tag{B.42}
$$

$$
p(\mathbf{y}\mid\mathbf{x})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\mathbf{x}+\mathbf{b},\mathbf{L}^{-1})
\tag{B.43}
$$

那么 $\mathbf{y}$ 的边缘分布以及给定 $\mathbf{y}$ 时 $\mathbf{x}$ 的条件分布分别为

$$
p(\mathbf{y})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\boldsymbol{\mu}+\mathbf{b},\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm{T}})
\tag{B.44}
$$

$$
p(\mathbf{x}\mid\mathbf{y})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\Sigma}\{\mathbf{A}^{\mathrm{T}}\mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda}\boldsymbol{\mu}\},\boldsymbol{\Sigma})
\tag{B.45}
$$

其中

$$
\boldsymbol{\Sigma}=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm{T}}\mathbf{L}\mathbf{A})^{-1}.
\tag{B.46}
$$

若有一个联合高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，其中 $\boldsymbol{\Lambda}\equiv\boldsymbol{\Sigma}^{-1}$，并定义如下分块：

$$
\mathbf{x}=\begin{pmatrix}\mathbf{x}_a\\\mathbf{x}_b\end{pmatrix},\qquad\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\end{pmatrix}
\tag{B.47}
$$

$$
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix},\qquad\boldsymbol{\Lambda}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}
\tag{B.48}
$$

则条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 为

$$
p(\mathbf{x}_a\mid\mathbf{x}_b)=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_{a\mid b},\boldsymbol{\Lambda}_{aa}^{-1})
\tag{B.49}
$$

$$
\boldsymbol{\mu}_{a\mid b}=\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{aa}^{-1}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)
\tag{B.50}
$$
