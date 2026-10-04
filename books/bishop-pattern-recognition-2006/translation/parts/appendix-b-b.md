<!-- pdf-page: 710 -->

边缘分布 $p(\mathbf{x}_a)$ 则为

$$
p(\mathbf{x}_a)=\mathcal{N}(\mathbf{x}_a\mid\boldsymbol{\mu}_a,\boldsymbol{\Sigma}_{aa}).
\tag{B.51}
$$

## 高斯-伽马分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/b-gaussian-gamma.png" alt="高斯-伽马分布的红色等高线示意图"></figure>

这是均值 $\mu$ 和精度 $\lambda$ 均未知时，一元高斯分布 $\mathcal{N}(x\mid\mu,\lambda^{-1})$ 的共轭先验分布，也称为*正态-伽马*分布。它是 $\mu$ 上的一个高斯分布与 $\lambda$ 上的一个伽马分布的乘积，其中高斯分布的精度与 $\lambda$ 成正比。

$$
p(\mu,\lambda\mid\mu_0,\beta,a,b)=\mathcal{N}\left(\mu\mid\mu_o,(\beta\lambda)^{-1}\right)\operatorname{Gam}(\lambda\mid a,b).
\tag{B.52}
$$

## 高斯 Wishart 分布

这是均值 $\boldsymbol{\mu}$ 和精度 $\boldsymbol{\Lambda}$ 均未知时，多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda})$ 的共轭先验分布，也称为正态 Wishart 分布。它是 $\boldsymbol{\mu}$ 上的一个高斯分布与 $\boldsymbol{\Lambda}$ 上的一个 Wishart 分布的乘积，其中高斯分布的精度与 $\boldsymbol{\Lambda}$ 成正比。

$$
p(\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\boldsymbol{\mu}_0,\beta,\mathbf{W},\nu)=\mathcal{N}\left(\boldsymbol{\mu}\mid\boldsymbol{\mu}_0,(\beta\boldsymbol{\Lambda})^{-1}\right)\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu).
\tag{B.53}
$$

对于标量 $x$ 这一特殊情形，它等价于高斯-伽马分布。

## 多项分布

如果将伯努利分布推广到一个 $K$ 维二元变量 $\mathbf{x}$，其分量 $x_k\in\{0,1\}$ 且满足 $\sum_k x_k=1$，就得到下列离散分布

$$
p(\mathbf{x})=\prod_{k=1}^{K}\mu_k^{x_k}
\tag{B.54}
$$

$$
\mathbb{E}[x_k]=\mu_k
\tag{B.55}
$$

$$
\operatorname{var}[x_k]=\mu_k(1-\mu_k)
\tag{B.56}
$$

$$
\operatorname{cov}[x_jx_k]=I_{jk}\mu_k
\tag{B.57}
$$

$$
\mathrm{H}[\mathbf{x}]=-\sum_{k=1}^{M}\mu_k\ln\mu_k
\tag{B.58}
$$

<!-- pdf-page: 711 -->

其中，$I_{jk}$ 是单位矩阵的第 $j,k$ 个元素。由于 $p(x_k=1)=\mu_k$，参数必须满足 $0\leqslant\mu_k\leqslant1$ 和 $\sum_k\mu_k=1$。

多项分布是二项分布的多元推广。在观测总数为 $N$ 时，它给出一个具有 $K$ 个状态的离散变量处于状态 $k$ 的计数 $m_k$ 的分布。

$$
\operatorname{Mult}(m_1,m_2,\ldots,m_K\mid\boldsymbol{\mu},N)=\binom{N}{m_1m_2\ldots m_M}\prod_{k=1}^{M}\mu_k^{m_k}
\tag{B.59}
$$

$$
\mathbb{E}[m_k]=N\mu_k
\tag{B.60}
$$

$$
\operatorname{var}[m_k]=N\mu_k(1-\mu_k)
\tag{B.61}
$$

$$
\operatorname{cov}[m_jm_k]=-N\mu_j\mu_k
\tag{B.62}
$$

其中，$\boldsymbol{\mu}=(\mu_1,\ldots,\mu_K)^{\mathrm{T}}$，而

$$
\binom{N}{m_1m_2\ldots m_K}=\frac{N!}{m_1!\ldots m_K!}
\tag{B.63}
$$

给出了将 $N$ 个相同物体分别放入各个箱子的方法数，其中第 $k$ 个箱子放入 $m_k$ 个物体，$k=1,\ldots,K$。$\mu_k$ 的值给出随机变量取状态 $k$ 的概率，因此这些参数受到约束 $0\leqslant\mu_k\leqslant1$ 和 $\sum_k\mu_k=1$。参数 $\{\mu_k\}$ 的共轭先验分布是狄利克雷分布。

## 正态分布

正态分布只是高斯分布的另一种名称。本书始终使用“高斯”这一术语，但仍保留用符号 $\mathcal{N}$ 表示这一分布的惯例。为保持一致，我们将正态-伽马分布称为高斯-伽马分布，同样将正态 Wishart 称为高斯 Wishart。

## Student t 分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/b-student-t.png" alt="Student t 分布的红绿蓝三条密度曲线，展示不同峰高与尾部"></figure>

William Gosset 于 1908 年发表了这一分布，但他的雇主 Guinness Breweries 要求他使用笔名发表，于是他选择了“Student”。在一元情形中，对一元高斯分布的精度设置共轭伽马先验，再将精度变量积分消去，就得到 Student t 分布。因此，它可以看作由无限多个

<!-- pdf-page: 712 -->
<!-- join-previous-paragraph -->
均值相同但方差不同的高斯分布组成的混合。

$$
\operatorname{St}(x\mid\mu,\lambda,\nu)=\frac{\Gamma(\nu/2+1/2)}{\Gamma(\nu/2)}\left(\frac{\lambda}{\pi\nu}\right)^{1/2}\left[1+\frac{\lambda(x-\mu)^2}{\nu}\right]^{-\nu/2-1/2}
\tag{B.64}
$$

$$
\mathbb{E}[x]=\mu\quad\text{当}\;\nu>1
\tag{B.65}
$$

$$
\operatorname{var}[x]=\frac{1}{\lambda}\frac{\nu}{\nu-2}\quad\text{当}\;\nu>2
\tag{B.66}
$$

$$
\operatorname{mode}[x]=\mu.
\tag{B.67}
$$

这里，$\nu>0$ 称为该分布的自由度数。$\nu=1$ 的特殊情形称为*柯西*分布。

对于 $D$ 维变量 $\mathbf{x}$，Student t 分布对应于关于共轭 Wishart 先验，将多元高斯分布的精度矩阵边缘化，形式为

$$
\operatorname{St}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda},\nu)=\frac{\Gamma(\nu/2+D/2)}{\Gamma(\nu/2)}\frac{|\boldsymbol{\Lambda}|^{1/2}}{(\nu\pi)^{D/2}}\left[1+\frac{\Delta^2}{\nu}\right]^{-\nu/2-D/2}
\tag{B.68}
$$

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}\quad\text{当}\;\nu>1
\tag{B.69}
$$

$$
\operatorname{cov}[\mathbf{x}]=\frac{\nu}{\nu-2}\boldsymbol{\Lambda}^{-1}\quad\text{当}\;\nu>2
\tag{B.70}
$$

$$
\operatorname{mode}[\mathbf{x}]=\boldsymbol{\mu}
\tag{B.71}
$$

其中，$\Delta^2$ 是平方马氏距离，定义为

$$
\Delta^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}}\boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu}).
\tag{B.72}
$$

在 $\nu\to\infty$ 的极限下，t 分布化为均值为 $\boldsymbol{\mu}$、精度为 $\boldsymbol{\Lambda}$ 的高斯分布。Student t 分布是高斯分布的一种推广，其最大似然参数值对离群点具有鲁棒性。

## 均匀分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/b-uniform.png" alt="有限区间上的三条均匀密度曲线，区间越窄密度越高"></figure>

这是定义在有限区间 $x\in[a,b]$（$b>a$）上的连续变量 $x$ 的一种简单分布。

$$
\mathrm{U}(x\mid a,b)=\frac{1}{b-a}
\tag{B.73}
$$

$$
\mathbb{E}[x]=\frac{(b+a)}{2}
\tag{B.74}
$$

$$
\operatorname{var}[x]=\frac{(b-a)^2}{12}
\tag{B.75}
$$

$$
\mathrm{H}[x]=\ln(b-a).
\tag{B.76}
$$

如果 $x$ 服从分布 $\mathrm{U}(x\mid0,1)$，那么 $a+(b-a)x$ 将服从分布 $\mathrm{U}(x\mid a,b)$。

<!-- pdf-page: 713 -->

## von Mises 分布

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/appendix-b/b-von-mises.png" alt="von Mises 分布的红色周期密度曲线示意图"></figure>

von Mises 分布也称为圆周正态分布或圆周高斯分布，是变量 $\theta\in[0,2\pi)$ 上的一种类似高斯分布的一元周期分布。

$$
p(\theta\mid\theta_0,m)=\frac{1}{2\pi I_0(m)}\exp\{m\cos(\theta-\theta_0)\}
\tag{B.77}
$$

其中，$I_0(m)$ 是第一类零阶贝塞尔函数。该分布的周期为 $2\pi$，因此对所有 $\theta$ 都有 $p(\theta+2\pi)=p(\theta)$。解释这一分布时必须谨慎，因为简单的期望会依赖于变量 $\theta$ 的原点如何选取，而原点可以任意选择。参数 $\theta_0$ 类似于一元高斯分布的均值，参数 $m>0$ 称为*集中参数*，类似于精度（方差的倒数）。当 $m$ 很大时，von Mises 分布近似于以 $\theta_0$ 为中心的高斯分布。

## Wishart 分布

Wishart 分布是多元高斯分布的精度矩阵的共轭先验分布。

$$
\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu)=B(\mathbf{W},\nu)|\boldsymbol{\Lambda}|^{(\nu-D-1)/2}\exp\left(-\frac{1}{2}\operatorname{Tr}(\mathbf{W}^{-1}\boldsymbol{\Lambda})\right)
\tag{B.78}
$$

其中

$$
B(\mathbf{W},\nu)\equiv|\mathbf{W}|^{-\nu/2}\left(2^{\nu D/2}\pi^{D(D-1)/4}\prod_{i=1}^{D}\Gamma\left(\frac{\nu+1-i}{2}\right)\right)^{-1}
\tag{B.79}
$$

$$
\mathbb{E}[\boldsymbol{\Lambda}]=\nu\mathbf{W}
\tag{B.80}
$$

$$
\mathbb{E}[\ln|\boldsymbol{\Lambda}|]=\sum_{i=1}^{D}\psi\left(\frac{\nu+1-i}{2}\right)+D\ln2+\ln|\mathbf{W}|
\tag{B.81}
$$

$$
\mathrm{H}[\boldsymbol{\Lambda}]=-\ln B(\mathbf{W},\nu)-\frac{(\nu-D-1)}{2}\mathbb{E}[\ln|\boldsymbol{\Lambda}|]+\frac{\nu D}{2}
\tag{B.82}
$$

这里，$\mathbf{W}$ 是一个 $D\times D$ 的对称正定矩阵，$\psi(\cdot)$ 是由式（B.25）定义的 digamma 函数。参数 $\nu$ 称为该分布的*自由度数*，它受到约束 $\nu>D-1$，以确保归一化因子中的伽马函数有良好定义。在一维情形中，Wishart 分布化为式（B.26）给出的伽马分布 $\operatorname{Gam}(\lambda\mid a,b)$，其中参数为 $a=\nu/2$ 和 $b=1/2W$。

<!-- pdf-page: 714 -->
