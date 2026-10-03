# 第 3 章 标准分布

<aside class="chapter-guide"><strong>本章导读</strong><p>本章介绍若干常用概率分布及其性质：先研究离散变量，再研究连续变量的高斯分布，并讨论怎样从数据估计分布参数。最后介绍直方图、最近邻和核方法等非参数密度估计方法。</p></aside>

<!-- pdf-page: 84 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/chapter-art.jpeg" alt="本章开篇的彩色抽象图案">
</figure>

本章讨论一些具体的概率分布及其性质。这些分布本身值得研究，也可以作为更复杂模型的构件，因此全书会广泛使用它们。

本章所讨论分布的一个用途是：给定随机变量 $\mathbf{x}$ 的有限个观测值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，对其概率分布 $p(\mathbf{x})$ 建模。这称为密度估计（density estimation）。必须强调，密度估计问题从根本上说是病态的，因为可能生成已观测的有限数据集的概率分布有无穷多个。事实上，任何在每个数据点 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 处均非零的分布 $p(\mathbf{x})$，都可能是候选分布。如何选择适当的分布，涉及模型选择问题；我们在多项式曲线拟合的语境中已遇到这一问题（第 1.2 节），它也是机器

<!-- pdf-page: 85 -->

学习中的核心问题。

我们先考虑离散变量的分布，再研究连续变量的高斯分布。这些都是参数分布（parametric distribution）的具体例子；之所以这样称呼，是因为它们由相对少量的可调参数决定，例如高斯分布的均值和方差。要将这类模型用于密度估计，就需要一套根据观测数据集确定适当参数值的方法。本章主要关注似然函数的最大化。这里我们假设各数据观测值独立同分布（independent and identically distributed，i.i.d.）；在后续章节中，我们将研究具有结构的数据等更复杂的情形，这一假设在那些情形下不再成立。

参数方法的一个局限是它预设分布具有某种特定的函数形式，而这种形式对具体应用可能并不合适。另一种选择是非参数密度估计方法（nonparametric density estimation），其中分布的形式通常取决于数据集大小。这类模型仍然包含参数，但参数控制的是模型复杂度，而不是分布的形式。本章最后简要讨论分别基于直方图、最近邻和核的三种非参数方法。这些非参数技术的一个主要局限是需要存储全部训练数据。换言之，参数数量会随数据集大小增长，因此面对大型数据集时，方法会变得非常低效。深度学习采用参数数量很多、但数量固定的神经网络来构造灵活的分布，从而结合参数模型的效率与非参数方法的通用性。

## 3.1 离散变量

我们先研究离散变量的简单分布：从二值变量开始，然后转向多状态变量。

### 3.1.1 伯努利分布

考虑一个二值随机变量 $x\in\{0,1\}$。例如，$x$ 可以描述抛硬币的结果，$x=1$ 表示“正面”，$x=0$ 表示“反面”。如果硬币有损伤，比如图 2.2 所示的硬币，那么正面朝上的概率不一定等于反面朝上的概率。我们用参数 $\mu$ 表示 $x=1$ 的概率，即

$$
p(x=1\mid\mu)=\mu. \tag{3.1}
$$

其中 $0\leqslant\mu\leqslant 1$，所以 $p(x=0\mid\mu)=1-\mu$。因此，$x$ 上的概率分布可写为

$$
\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}, \tag{3.2}
$$

称为伯努利分布（Bernoulli distribution）。容易验证（习题 3.1），这一分布

<!-- pdf-page: 86 -->

已归一化，其均值和方差分别为

$$
\mathbb{E}[x]=\mu \tag{3.3}
$$

$$
\operatorname{var}[x]=\mu(1-\mu). \tag{3.4}
$$

现在设观测到的 $x$ 的取值构成数据集 $\mathcal{D}=\{x_1,\ldots,x_N\}$。假设这些观测值从 $p(x\mid\mu)$ 中独立抽取，就可以构造关于 $\mu$ 的函数，即似然函数：

$$
p(\mathcal{D}\mid\mu)=\prod_{n=1}^{N}p(x_n\mid\mu)=\prod_{n=1}^{N}\mu^{x_n}(1-\mu)^{1-x_n}. \tag{3.5}
$$

我们可以通过最大化似然函数来估计 $\mu$，也可以等价地最大化似然函数的对数，因为对数是单调函数。伯努利分布的对数似然函数为

$$
\ln p(\mathcal{D}\mid\mu)=\sum_{n=1}^{N}\ln p(x_n\mid\mu)=\sum_{n=1}^{N}\{x_n\ln\mu+(1-x_n)\ln(1-\mu)\}. \tag{3.6}
$$

此时注意，对数似然函数仅通过 $\sum_n x_n$ 这一总和依赖于 $N$ 个观测值 $x_n$。对这种分布而言，该总和是数据的一个充分统计量（sufficient statistic），我们将在第 3.4 节进一步讨论。令 $\ln p(\mathcal{D}\mid\mu)$ 对 $\mu$ 的导数为零，得到极大似然估计量：

$$
\mu_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}x_n, \tag{3.7}
$$

这也称为样本均值。若用 $m$ 表示此数据集中 $x=1$（正面朝上）的观测次数，那么式 (3.7) 可写为

$$
\mu_{\mathrm{ML}}=\frac{m}{N}, \tag{3.8}
$$

因此，在极大似然框架下，正面朝上的概率等于数据集中正面朝上次数所占的比例。

### 3.1.2 二项分布

在数据集大小为 $N$ 的条件下，我们还可以求出二值变量 $x$ 取值为 1 的观测次数 $m$ 的分布。这称为二项分布（binomial distribution）。从式 (3.5) 可知，它正比于 $\mu^m(1-\mu)^{N-m}$。为得到归一化系数，需要计入在 $N$ 次抛币中得到 $m$ 次正面的所有可能方式。因此，二项分布可写为

$$
\operatorname{Bin}(m\mid N,\mu)=\binom{N}{m}\mu^m(1-\mu)^{N-m}, \tag{3.9}
$$

<!-- pdf-page: 87 -->

<figure id="fig-3-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-1.png" alt="N 等于 10、μ 等于 0.25 时二项分布随 m 变化的蓝色直方图">
  <figcaption>图 3.1：$N=10$、$\mu=0.25$ 时，二项分布 (3.9) 关于 $m$ 的直方图。</figcaption>
</figure>

其中

$$
\binom{N}{m}\equiv\frac{N!}{(N-m)!m!} \tag{3.10}
$$

表示从总共 $N$ 个相同物体中不放回地选取 $m$ 个物体的方式数（习题 3.3）。图 3.1 给出了 $N=10$、$\mu=0.25$ 时二项分布的图像。

利用独立事件的和的均值等于各均值之和、其方差等于各方差之和（习题 2.10），可以求出二项分布的均值和方差。由于 $m=x_1+\cdots+x_N$，且每个观测值的均值和方差分别由式 (3.3) 和 (3.4) 给出，因此

$$
\mathbb{E}[m]\equiv\sum_{m=0}^{N}m\operatorname{Bin}(m\mid N,\mu)=N\mu \tag{3.11}
$$

$$
\operatorname{var}[m]\equiv\sum_{m=0}^{N}(m-\mathbb{E}[m])^2\operatorname{Bin}(m\mid N,\mu)=N\mu(1-\mu). \tag{3.12}
$$

也可以直接用微积分证明这些结果（习题 3.4）。

### 3.1.3 多项分布

二值变量可以描述只能取两种可能值之一的量。不过，我们经常会遇到能取 $K$ 种互斥状态之一的离散变量。这样的变量有多种表示法。我们很快会看到，一种特别方便的表示法是 1-of-$K$ 方案，有时称为独热编码（one-hot encoding）：用一个 $K$ 维向量 $\mathbf{x}$ 表示变量，其中一个分量 $x_k$ 等于 1，其余分量均等于 0。例如，假设一个变量可以取 $K=6$ 种状态，某次观测的状态恰好

<!-- pdf-page: 88 -->

对应 $x_3=1$，那么 $\mathbf{x}$ 表示为

$$
\mathbf{x}=(0,0,1,0,0,0)^{\mathrm T}. \tag{3.13}
$$

注意，这类向量满足 $\sum_{k=1}^{K}x_k=1$。若用参数 $\mu_k$ 表示 $x_k=1$ 的概率，则 $\mathbf{x}$ 的分布为

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{k=1}^{K}\mu_k^{x_k} \tag{3.14}
$$

其中 $\boldsymbol{\mu}=(\mu_1,\ldots,\mu_K)^{\mathrm T}$。由于 $\mu_k$ 表示概率，这些参数须满足 $\mu_k\geqslant0$ 和 $\sum_k\mu_k=1$。分布 (3.14) 可以视为把伯努利分布推广到多于两种结果的情形。容易看出它已归一化：

$$
\sum_{\mathbf{x}}p(\mathbf{x}\mid\boldsymbol{\mu})=\sum_{k=1}^{K}\mu_k=1 \tag{3.15}
$$

并且

$$
\mathbb{E}[\mathbf{x}\mid\boldsymbol{\mu}]=\sum_{\mathbf{x}}p(\mathbf{x}\mid\boldsymbol{\mu})\mathbf{x}=\boldsymbol{\mu}. \tag{3.16}
$$

现在考虑由 $N$ 个独立观测值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 组成的数据集 $\mathcal{D}$。相应的似然函数为

$$
p(\mathcal{D}\mid\boldsymbol{\mu})=\prod_{n=1}^{N}\prod_{k=1}^{K}\mu_k^{x_{nk}}=\prod_{k=1}^{K}\mu_k^{\left(\sum_n x_{nk}\right)}=\prod_{k=1}^{K}\mu_k^{m_k} \tag{3.17}
$$

可见，似然函数只通过以下 $K$ 个量依赖于 $N$ 个数据点：

$$
m_k=\sum_{n=1}^{N}x_{nk}, \tag{3.18}
$$

它们表示 $x_k=1$ 的观测次数，称为这一分布的充分统计量（见第 3.4 节）。注意变量 $m_k$ 满足约束

$$
\sum_{k=1}^{K}m_k=N. \tag{3.19}
$$

为求 $\boldsymbol{\mu}$ 的极大似然解，需要对 $\mu_k$ 最大化 $\ln p(\mathcal{D}\mid\boldsymbol{\mu})$，同时顾及式 (3.15) 中 $\mu_k$ 之和必须为 1 的约束。可以使用拉格朗日乘子 $\lambda$，最大化（见附录 C）

$$
\sum_{k=1}^{K}m_k\ln\mu_k+\lambda\left(\sum_{k=1}^{K}\mu_k-1\right). \tag{3.20}
$$

<!-- pdf-page: 89 -->

令式 (3.20) 对 $\mu_k$ 的导数为零，得到

$$
\mu_k=-m_k/\lambda. \tag{3.21}
$$

将式 (3.21) 代入约束 $\sum_k\mu_k=1$，可解得拉格朗日乘子 $\lambda=-N$。于是 $\mu_k$ 的极大似然解为

$$
\mu_k^{\mathrm{ML}}=\frac{m_k}{N}, \tag{3.22}
$$

即 $N$ 个观测值中 $x_k=1$ 的比例。

也可以考虑：在给定参数向量 $\boldsymbol{\mu}$ 和观测总数 $N$ 的条件下，$m_1,\ldots,m_K$ 的联合分布。由式 (3.17) 可得

$$
\operatorname{Mult}(m_1,m_2,\ldots,m_K\mid\boldsymbol{\mu},N)=\binom{N}{m_1m_2\cdots m_K}\prod_{k=1}^{K}\mu_k^{m_k}, \tag{3.23}
$$

这称为多项分布（multinomial distribution）。归一化系数是把 $N$ 个物体分成 $K$ 组、各组大小分别为 $m_1,\ldots,m_K$ 的方式数，即

$$
\binom{N}{m_1m_2\cdots m_K}=\frac{N!}{m_1!m_2!\cdots m_K!}. \tag{3.24}
$$

注意，两状态的量可以表示为二值变量，用二项分布 (3.9) 建模；也可以表示为 1-of-2 变量，用 $K=2$ 时的分布 (3.14) 建模。

## 3.2 多元高斯分布

高斯分布（Gaussian distribution），又称正态分布（normal distribution），是为连续变量的分布建模时广泛使用的一种模型。我们在第 2.3 节已经看到，对于单个变量 $x$，高斯分布可写为

$$
\mathcal{N}(x\mid\mu,\sigma^2)=\frac{1}{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac{1}{2\sigma^2}(x-\mu)^2\right\} \tag{3.25}
$$

其中 $\mu$ 是均值，$\sigma^2$ 是方差。对于 $D$ 维向量 $\mathbf{x}$，多元高斯分布为

$$
\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})=\frac{1}{(2\pi)^{D/2}|\boldsymbol{\Sigma}|^{1/2}}\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\} \tag{3.26}
$$

其中 $\boldsymbol{\mu}$ 是 $D$ 维均值向量，$\boldsymbol{\Sigma}$ 是 $D\times D$ 协方差矩阵，$\det\boldsymbol{\Sigma}$ 表示 $\boldsymbol{\Sigma}$ 的行列式。

高斯分布出现在许多不同的情境中，也可以从多个不同角度理解。例如，我们在第 2.5 节已经看到，对于

<!-- pdf-page: 90 -->

<!-- join-previous-paragraph -->

单个实变量，使熵最大的分布是高斯分布。这一性质对多元高斯分布也成立（习题 3.8）。

<figure id="fig-3-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-2.png" alt="N 分别为 1、2、10 时，均匀分布随机数的平均值的三幅直方图，形状逐渐趋近钟形">
  <figcaption>图 3.2：不同 $N$ 值下，$N$ 个均匀分布随机数的平均值的直方图。可以看到，随着 $N$ 增大，该分布趋向高斯分布。</figcaption>
</figure>

高斯分布还出现在多个随机变量求和的情形。中心极限定理告诉我们，在满足某些温和条件时，一组随机变量的和——它本身当然也是随机变量——的分布会随着求和项数增多而越来越接近高斯分布（Walker，1969）。我们可以用 $N$ 个变量 $x_1,\ldots,x_N$ 来说明：每个变量都在区间 $[0,1]$ 上均匀分布，然后考察平均值 $(x_1+\cdots+x_N)/N$ 的分布。如图 3.2 所示，$N$ 很大时，这个分布趋向高斯分布。实际上，随着 $N$ 增大，向高斯分布的收敛可能非常快。由此可知，二项分布 (3.9) 定义在 $m$ 上，而 $m$ 是随机二值变量 $x$ 的 $N$ 个观测值之和；当 $N\to\infty$ 时，二项分布将趋向高斯分布（$N=10$ 的情形见图 3.1）。

高斯分布有许多重要的解析性质，下面我们将详细讨论其中一些。因此，本节会比前面某些章节在技术上更深入，需要熟悉各种矩阵恒等式（见附录 A）。

### 3.2.1 高斯分布的几何结构

我们先考察高斯分布的几何形式。高斯分布对 $\mathbf{x}$ 的函数依赖通过指数中的二次型体现：

$$
\Delta^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}), \tag{3.27}
$$

$\Delta$ 称为从 $\boldsymbol{\mu}$ 到 $\mathbf{x}$ 的马氏距离（Mahalanobis distance）。当 $\boldsymbol{\Sigma}$ 为单位矩阵时，它化为欧氏距离。在 $\mathbf{x}$ 空间中，这个二次型取常数的曲面上，高斯分布也取常数。

首先注意，不失一般性，可取 $\boldsymbol{\Sigma}$ 为对称矩阵，因为任何反对称分量都会从指数中消失（习题 3.11）。现在考虑协方差矩阵的特征向量方程

$$
\boldsymbol{\Sigma}\mathbf{u}_i=\lambda_i\mathbf{u}_i \tag{3.28}
$$

<!-- pdf-page: 91 -->

其中 $i=1,\ldots,D$。因为 $\boldsymbol{\Sigma}$ 是实对称矩阵，所以它的特征值都是实数，且可以选取其特征向量，使之构成一组标准正交向量（习题 3.12），因此

$$
\mathbf{u}_i^{\mathrm T}\mathbf{u}_j=I_{ij} \tag{3.29}
$$

其中 $I_{ij}$ 是单位矩阵的第 $i,j$ 个元素，满足

$$
I_{ij}=\begin{cases}1,&i=j,\\0,&i\ne j.\end{cases} \tag{3.30}
$$

协方差矩阵 $\boldsymbol{\Sigma}$ 可按其特征向量展开为（习题 3.13）

$$
\boldsymbol{\Sigma}=\sum_{i=1}^{D}\lambda_i\mathbf{u}_i\mathbf{u}_i^{\mathrm T} \tag{3.31}
$$

类似地，逆协方差矩阵 $\boldsymbol{\Sigma}^{-1}$ 可写为

$$
\boldsymbol{\Sigma}^{-1}=\sum_{i=1}^{D}\frac{1}{\lambda_i}\mathbf{u}_i\mathbf{u}_i^{\mathrm T}. \tag{3.32}
$$

将式 (3.32) 代入式 (3.27)，二次型变成

$$
\Delta^2=\sum_{i=1}^{D}\frac{y_i^2}{\lambda_i} \tag{3.33}
$$

其中定义了

$$
y_i=\mathbf{u}_i^{\mathrm T}(\mathbf{x}-\boldsymbol{\mu}). \tag{3.34}
$$

可将 $\{y_i\}$ 理解为一套新坐标系：它由标准正交向量 $\mathbf{u}_i$ 定义，相对于原坐标 $x_i$ 经过了平移和旋转。构造向量 $\mathbf{y}=(y_1,\ldots,y_D)^{\mathrm T}$，便有

$$
\mathbf{y}=\mathbf{U}(\mathbf{x}-\boldsymbol{\mu}) \tag{3.35}
$$

其中矩阵 $\mathbf{U}$ 的各行是 $\mathbf{u}_i^{\mathrm T}$。由式 (3.29) 可知，$\mathbf{U}$ 是正交矩阵，即满足 $\mathbf{U}\mathbf{U}^{\mathrm T}=\mathbf{U}^{\mathrm T}\mathbf{U}=\mathbf{I}$，其中 $\mathbf{I}$ 是单位矩阵（见附录 A）。

二次型以及高斯密度在式 (3.33) 取常数的曲面上取常数。如果所有特征值 $\lambda_i$ 均为正，这些曲面就是椭球面，中心在 $\boldsymbol{\mu}$，各轴沿 $\mathbf{u}_i$ 方向，各轴方向的缩放因子是 $\lambda_i^{1/2}$，如图 3.3 所示。

为了使高斯分布有良好定义，协方差矩阵的所有特征值 $\lambda_i$ 都必须严格为正，否则分布无法恰当归一化。所有特征值严格为正的矩阵称为正定矩阵（positive definite）。第 16 章讨论潜变量模型时，我们会遇到一个或多个特征值为零的高斯分布，在

<!-- pdf-page: 92 -->

<!-- join-previous-paragraph -->

这种情形下，分布是奇异的，并被限制在一个维数更低的子空间内。如果所有特征值均非负，就称协方差矩阵为半正定矩阵（positive semidefinite）。

<figure id="fig-3-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-3.png" alt="二维高斯分布的红色等密度椭圆、均值、特征向量和旋转坐标轴">
  <figcaption>图 3.3：红色曲线是二维空间 $\mathbf{x}=(x_1,x_2)$ 中，高斯分布的概率密度保持不变的椭圆；其上的密度是 $\mathbf{x}=\boldsymbol{\mu}$ 处密度的 $\exp(-1/2)$ 倍。椭圆的轴由协方差矩阵的特征向量 $\mathbf{u}_i$ 确定，对应的特征值为 $\lambda_i$。</figcaption>
</figure>

现在考察在 $y_i$ 所定义的新坐标系中，高斯分布的形式。从 $\mathbf{x}$ 坐标系变换到 $\mathbf{y}$ 坐标系时，雅可比矩阵 $\mathbf{J}$ 的元素为

$$
J_{ij}=\frac{\partial x_i}{\partial y_j}=U_{ji} \tag{3.36}
$$

其中 $U_{ji}$ 是矩阵 $\mathbf{U}^{\mathrm T}$ 的元素。利用矩阵 $\mathbf{U}$ 的标准正交性质，雅可比矩阵行列式的平方为

$$
|\mathbf{J}|^2=|\mathbf{U}^{\mathrm T}|^2=|\mathbf{U}^{\mathrm T}||\mathbf{U}|=|\mathbf{U}^{\mathrm T}\mathbf{U}|=|\mathbf{I}|=1 \tag{3.37}
$$

因此 $|\mathbf{J}|=1$。另外，协方差矩阵的行列式 $|\boldsymbol{\Sigma}|$ 可写为其特征值之积，因此

$$
|\boldsymbol{\Sigma}|^{1/2}=\prod_{j=1}^{D}\lambda_j^{1/2}. \tag{3.38}
$$

于是，在 $y_j$ 坐标系中，高斯分布变为

$$
p(\mathbf{y})=p(\mathbf{x})|\mathbf{J}|=\prod_{j=1}^{D}\frac{1}{(2\pi\lambda_j)^{1/2}}\exp\left\{-\frac{y_j^2}{2\lambda_j}\right\}, \tag{3.39}
$$

即 $D$ 个相互独立的一元高斯分布之积。因此，特征向量定义了一组经过平移和旋转的新坐标；相对于这组坐标，联合概率分布分解为独立分布之积。该分布在 $\mathbf{y}$ 坐标系中的积分于是为

$$
\int p(\mathbf{y})\,\mathrm{d}\mathbf{y}
=\prod_{j=1}^{D}\int_{-\infty}^{\infty}\frac{1}{(2\pi\lambda_j)^{1/2}}\exp\left\{-\frac{y_j^2}{2\lambda_j}\right\}\mathrm{d}y_j=1. \tag{3.40}
$$

<!-- pdf-page: 93 -->

这里用到了式 (2.51) 给出的一元高斯分布归一化结果。由此确认多元高斯分布 (3.26) 确实已归一化。

### 3.2.2 矩

下面研究高斯分布的矩，以解释参数 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 的含义。高斯分布下 $\mathbf{x}$ 的期望为

$$
\begin{aligned}
\mathbb{E}[\mathbf{x}]
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\int\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}\mathbf{x}\,\mathrm{d}\mathbf{x}\\
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\int\exp\left\{-\frac{1}{2}\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})\,\mathrm{d}\mathbf{z}.
\end{aligned} \tag{3.41}
$$

这里作了变量替换 $\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}$。注意指数是 $\mathbf{z}$ 的各分量的偶函数，而积分区间为 $(-\infty,\infty)$，因此 $(\mathbf{z}+\boldsymbol{\mu})$ 中的 $\mathbf{z}$ 项因对称性而积分为零。所以

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}, \tag{3.42}
$$

我们因而称 $\boldsymbol{\mu}$ 为高斯分布的均值。

下面考虑高斯分布的二阶矩。一元情形的二阶矩是 $\mathbb{E}[x^2]$。多元高斯分布则有 $D^2$ 个二阶矩 $\mathbb{E}[x_i x_j]$，可以将它们组合成矩阵 $\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]$。这个矩阵可写为

$$
\begin{aligned}
\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\int\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right\}\mathbf{x}\mathbf{x}^{\mathrm T}\,\mathrm{d}\mathbf{x}\\
&=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\int\exp\left\{-\frac{1}{2}\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}(\mathbf{z}+\boldsymbol{\mu})(\mathbf{z}+\boldsymbol{\mu})^{\mathrm T}\,\mathrm{d}\mathbf{z}.
\end{aligned} \tag{3.43}
$$

这里再次使用了变量替换 $\mathbf{z}=\mathbf{x}-\boldsymbol{\mu}$。注意涉及 $\boldsymbol{\mu}\mathbf{z}^{\mathrm T}$ 和 $\boldsymbol{\mu}^{\mathrm T}\mathbf{z}$ 的交叉项也因对称性而消失。$\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}$ 项是常量，可移到积分号外；积分本身等于 1，因为高斯分布已归一化。再考虑涉及 $\mathbf{z}\mathbf{z}^{\mathrm T}$ 的项。利用式 (3.28) 给出的协方差矩阵特征向量展开式，以及这组特征向量的完备性，可以写出

$$
\mathbf{z}=\sum_{j=1}^{D}y_j\mathbf{u}_j \tag{3.44}
$$

<!-- pdf-page: 94 -->

其中 $y_j=\mathbf{u}_j^{\mathrm T}\mathbf{z}$，因此

$$
\begin{aligned}
&\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\int\exp\left\{-\frac{1}{2}\mathbf{z}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{z}\right\}\mathbf{z}\mathbf{z}^{\mathrm T}\,\mathrm{d}\mathbf{z}\\
&\quad=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}
\sum_{i=1}^{D}\sum_{j=1}^{D}\mathbf{u}_i\mathbf{u}_j^{\mathrm T}
\int\exp\left\{-\sum_{k=1}^{D}\frac{y_k^2}{2\lambda_k}\right\}y_i y_j\,\mathrm{d}\mathbf{y}\\
&\quad=\sum_{i=1}^{D}\mathbf{u}_i\mathbf{u}_i^{\mathrm T}\lambda_i
=\boldsymbol{\Sigma}.
\end{aligned} \tag{3.45}
$$

这里用到了特征向量方程 (3.28)，以及中间一行的积分在 $i\ne j$ 时因对称性而为零这一事实。最后一行还用到了式 (2.53)、(3.38) 和 (3.31)。于是

$$
\mathbb{E}[\mathbf{x}\mathbf{x}^{\mathrm T}]=\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}+\boldsymbol{\Sigma}. \tag{3.46}
$$

定义单个随机变量的方差时，我们先减去均值，再求二阶矩。类似地，在多元情形下，减去均值也很方便，由此得到随机向量 $\mathbf{x}$ 的协方差定义：

$$
\operatorname{cov}[\mathbf{x}]=\mathbb{E}\left[(\mathbf{x}-\mathbb{E}[\mathbf{x}])(\mathbf{x}-\mathbb{E}[\mathbf{x}])^{\mathrm T}\right]. \tag{3.47}
$$

对于高斯分布，利用 $\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}$ 和式 (3.46)，得到

$$
\operatorname{cov}[\mathbf{x}]=\boldsymbol{\Sigma}. \tag{3.48}
$$

由于参数矩阵 $\boldsymbol{\Sigma}$ 决定高斯分布下 $\mathbf{x}$ 的协方差，所以它称为协方差矩阵。

### 3.2.3 局限性

尽管高斯分布 (3.26) 经常用作简单的密度模型，但它有一些重要局限。先看分布的自由参数数量。一般的对称协方差矩阵 $\boldsymbol{\Sigma}$ 有 $D(D+1)/2$ 个独立参数（习题 3.15），$\boldsymbol{\mu}$ 中另有 $D$ 个独立参数，总计 $D(D+3)/2$ 个。因此，$D$ 很大时，参数总数随 $D$ 的平方增长，处理和求逆大型矩阵的计算量可能高到无法承受。解决这一问题的一种方法是限制协方差矩阵的形式。如果只考虑对角协方差矩阵，即 $\boldsymbol{\Sigma}=\operatorname{diag}(\sigma_i^2)$，密度模型就只有 $2D$ 个独立参数，相应的等密度轮廓是轴与坐标轴对齐的椭球。还可以进一步要求协方差矩阵与单位矩阵成正比，即 $\boldsymbol{\Sigma}=\sigma^2\mathbf{I}$，称为各向同性协方差；这时模型有 $D+1$ 个独立参数，等密度曲面是球面。一般、对角和各向同性协方差矩阵对应的三种情形见图 3.4。不过，

<!-- pdf-page: 95 -->

<!-- join-previous-paragraph -->

这些方法虽然限制了分布的自由度，并大幅加快协方差矩阵的求逆，却也极大地限制了概率密度的形式，使模型捕捉数据中有意义的相关性的能力受到限制。

<figure id="fig-3-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-4.png" alt="二维高斯分布在一般、对角和各向同性协方差矩阵下的三种等密度轮廓">
  <figcaption>图 3.4：二维高斯分布的等概率密度轮廓，其中协方差矩阵 (a) 为一般形式，(b) 为对角矩阵，此时椭圆轮廓与坐标轴对齐，(c) 与单位矩阵成正比，此时轮廓为同心圆。</figcaption>
</figure>

高斯分布的另一局限是它本质上是单峰的，即只有一个最大值，因此无法很好地近似多峰分布。这样，高斯分布一方面可能因为参数过多而过于灵活，另一方面又可能因为能充分表示的分布类型有限而过于受限。后文会看到，引入潜变量（latent variable），又称隐藏变量或未观测变量，可以同时解决这两个问题。具体而言，引入离散潜变量将产生高斯混合分布，从而得到丰富的多峰分布族（见第 3.2.9 节）。类似地，引入连续潜变量可得到这样的模型：自由参数的数量可以独立于数据空间的维数 $D$ 而受到控制，同时仍能捕捉数据集中的主要相关性（见第 16 章）。

### 3.2.4 条件分布

多元高斯分布有一项重要性质：如果两组变量服从联合高斯分布，那么在给定其中一组变量的条件下，另一组变量的条件分布仍然是高斯分布。同样，任一组变量的边缘分布也是高斯分布。

先考虑条件分布。设 $\mathbf{x}$ 是服从高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 的 $D$ 维向量，把 $\mathbf{x}$ 划分为互不相交的两部分 $\mathbf{x}_a$ 和 $\mathbf{x}_b$。不失一般性，可令 $\mathbf{x}_a$ 包含 $\mathbf{x}$ 的前 $M$ 个分量，$\mathbf{x}_b$ 包含其余 $D-M$ 个分量，于是

$$
\mathbf{x}=\begin{pmatrix}\mathbf{x}_a\\\mathbf{x}_b\end{pmatrix}. \tag{3.49}
$$

均值向量 $\boldsymbol{\mu}$ 也相应划分为

$$
\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\end{pmatrix}. \tag{3.50}
$$

<!-- pdf-page: 96 -->

协方差矩阵 $\boldsymbol{\Sigma}$ 相应划分为

$$
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}. \tag{3.51}
$$

注意，协方差矩阵的对称性 $\boldsymbol{\Sigma}^{\mathrm T}=\boldsymbol{\Sigma}$ 意味着 $\boldsymbol{\Sigma}_{aa}$ 和 $\boldsymbol{\Sigma}_{bb}$ 都是对称矩阵，而且 $\boldsymbol{\Sigma}_{ba}=\boldsymbol{\Sigma}_{ab}^{\mathrm T}$。

很多时候，使用协方差矩阵的逆更方便：

$$
\boldsymbol{\Lambda}\equiv\boldsymbol{\Sigma}^{-1}, \tag{3.52}
$$

它称为精度矩阵（precision matrix）。事实上，我们将看到，高斯分布的某些性质以协方差表示最自然，另一些性质以精度表示则更简单。因此，我们也引入精度矩阵的分块形式：

$$
\boldsymbol{\Lambda}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}, \tag{3.53}
$$

它与式 (3.49) 对向量 $\mathbf{x}$ 的划分相对应。由于对称矩阵的逆仍然对称，可知 $\boldsymbol{\Lambda}_{aa}$ 和 $\boldsymbol{\Lambda}_{bb}$ 也是对称矩阵，且 $\boldsymbol{\Lambda}_{ba}=\boldsymbol{\Lambda}_{ab}^{\mathrm T}$（习题 3.16）。此处必须强调，例如，$\boldsymbol{\Lambda}_{aa}$ 并不简单地等于 $\boldsymbol{\Sigma}_{aa}$ 的逆。我们很快会考察分块矩阵的逆与各分块的逆之间的关系。

先求条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的表达式。根据概率的乘法法则，原则上只需在联合分布 $p(\mathbf{x})=p(\mathbf{x}_a,\mathbf{x}_b)$ 中把 $\mathbf{x}_b$ 固定为观测值，再将所得表达式归一化，使它成为 $\mathbf{x}_a$ 上的有效概率分布。我们无需显式完成归一化；更高效的方法是考察式 (3.27) 给出的高斯分布指数中的二次型，最后再补回归一化系数。利用式 (3.49)、(3.50) 和 (3.53) 的分块形式，可得

$$
\begin{aligned}
&-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\\
&=-\frac{1}{2}(\mathbf{x}_a-\boldsymbol{\mu}_a)^{\mathrm T}\boldsymbol{\Lambda}_{aa}(\mathbf{x}_a-\boldsymbol{\mu}_a)
-\frac{1}{2}(\mathbf{x}_a-\boldsymbol{\mu}_a)^{\mathrm T}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\\
&\quad-\frac{1}{2}(\mathbf{x}_b-\boldsymbol{\mu}_b)^{\mathrm T}\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)
-\frac{1}{2}(\mathbf{x}_b-\boldsymbol{\mu}_b)^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\mu}_b).
\end{aligned} \tag{3.54}
$$

可见，作为 $\mathbf{x}_a$ 的函数，它仍是二次型，因此对应的条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 是高斯分布。由于均值和协方差完全确定这个分布，我们的目标是观察式 (3.54)，找出 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值和协方差表达式。

这涉及高斯分布中的一种很常见的运算，称为“配方”：已知定义高斯分布指数项的二次型，需要确定相应的均值和协方差。这类问题可以直接求解，只要注意一般高斯分布

<!-- pdf-page: 97 -->

$\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 的指数可写为

$$
-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})
=-\frac{1}{2}\mathbf{x}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\mathbf{x}
+\mathbf{x}^{\mathrm T}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}+\mathrm{const} \tag{3.55}
$$

其中 $\mathrm{const}$ 表示与 $\mathbf{x}$ 无关的项；这里还利用了 $\boldsymbol{\Sigma}$ 的对称性。因此，把一般二次型写成式 (3.55) 右侧的形式后，就可以立即把 $\mathbf{x}$ 二阶项的系数矩阵认作逆协方差矩阵 $\boldsymbol{\Sigma}^{-1}$，把 $\mathbf{x}$ 线性项的系数认作 $\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}$，进而求出 $\boldsymbol{\mu}$。

现在将这一方法用于条件高斯分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$，其指数中的二次型由式 (3.54) 给出。分别用 $\boldsymbol{\mu}_{a\mid b}$ 和 $\boldsymbol{\Sigma}_{a\mid b}$ 表示该分布的均值和协方差。把 $\mathbf{x}_b$ 视为常量，考察式 (3.54) 对 $\mathbf{x}_a$ 的函数依赖。取出所有关于 $\mathbf{x}_a$ 的二阶项，得到

$$
-\frac{1}{2}\mathbf{x}_a^{\mathrm T}\boldsymbol{\Lambda}_{aa}\mathbf{x}_a \tag{3.56}
$$

由此立刻可知，$p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的协方差（精度矩阵的逆）为

$$
\boldsymbol{\Sigma}_{a\mid b}=\boldsymbol{\Lambda}_{aa}^{-1}. \tag{3.57}
$$

再考虑式 (3.54) 中所有关于 $\mathbf{x}_a$ 的线性项：

$$
\mathbf{x}_a^{\mathrm T}\{\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\} \tag{3.58}
$$

这里用到了 $\boldsymbol{\Lambda}_{ba}^{\mathrm T}=\boldsymbol{\Lambda}_{ab}$。根据对一般形式 (3.55) 的讨论，式中 $\mathbf{x}_a$ 的系数必须等于 $\boldsymbol{\Sigma}_{a\mid b}^{-1}\boldsymbol{\mu}_{a\mid b}$，因此

$$
\begin{aligned}
\boldsymbol{\mu}_{a\mid b}
&=\boldsymbol{\Sigma}_{a\mid b}\{\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b)\}\\
&=\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{aa}^{-1}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b),
\end{aligned} \tag{3.59}
$$

其中使用了式 (3.57)。

式 (3.57) 和 (3.59) 用原联合分布 $p(\mathbf{x}_a,\mathbf{x}_b)$ 的分块精度矩阵来表示。也可以用相应的分块协方差矩阵表示。为此，使用以下分块矩阵求逆恒等式（习题 3.18）：

$$
\begin{pmatrix}\mathbf{A}&\mathbf{B}\\\mathbf{C}&\mathbf{D}\end{pmatrix}^{-1}
=\begin{pmatrix}
\mathbf{M}&-\mathbf{M}\mathbf{B}\mathbf{D}^{-1}\\
-\mathbf{D}^{-1}\mathbf{C}\mathbf{M}&\mathbf{D}^{-1}+\mathbf{D}^{-1}\mathbf{C}\mathbf{M}\mathbf{B}\mathbf{D}^{-1}
\end{pmatrix}, \tag{3.60}
$$

其中定义

$$
\mathbf{M}=(\mathbf{A}-\mathbf{B}\mathbf{D}^{-1}\mathbf{C})^{-1}. \tag{3.61}
$$

<!-- pdf-page: 98 -->

$\mathbf{M}^{-1}$ 称为式 (3.60) 左侧矩阵相对于子矩阵 $\mathbf{D}$ 的舒尔补（Schur complement）。根据定义

$$
\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}^{-1}
=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix} \tag{3.62}
$$

并利用式 (3.60)，可得

$$
\boldsymbol{\Lambda}_{aa}=(\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba})^{-1} \tag{3.63}
$$

$$
\boldsymbol{\Lambda}_{ab}=-(\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba})^{-1}\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}. \tag{3.64}
$$

由此得到条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值和协方差：

$$
\boldsymbol{\mu}_{a\mid b}=\boldsymbol{\mu}_a+\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}(\mathbf{x}_b-\boldsymbol{\mu}_b) \tag{3.65}
$$

$$
\boldsymbol{\Sigma}_{a\mid b}=\boldsymbol{\Sigma}_{aa}-\boldsymbol{\Sigma}_{ab}\boldsymbol{\Sigma}_{bb}^{-1}\boldsymbol{\Sigma}_{ba}. \tag{3.66}
$$

比较式 (3.57) 和 (3.66)，可以看到，用分块精度矩阵表示条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 比用分块协方差矩阵表示更简洁。注意，式 (3.65) 给出的条件均值是 $\mathbf{x}_b$ 的线性函数，而式 (3.66) 给出的协方差与 $\mathbf{x}_b$ 无关。这是线性高斯模型的一个例子（见第 11.1.4 节）。

### 3.2.5 边缘分布

我们已经看到，如果联合分布 $p(\mathbf{x}_a,\mathbf{x}_b)$ 是高斯分布，那么条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 仍然是高斯分布。现在讨论边缘分布

$$
p(\mathbf{x}_a)=\int p(\mathbf{x}_a,\mathbf{x}_b)\,\mathrm{d}\mathbf{x}_b, \tag{3.67}
$$

后面将看到它也是高斯分布。计算该分布时，我们仍着重考察联合分布指数中的二次型，由此确定边缘分布 $p(\mathbf{x}_a)$ 的均值和协方差。

利用分块精度矩阵，联合分布的二次型可写为式 (3.54)。我们的目标是对 $\mathbf{x}_b$ 积分；最简便的方法是先考察涉及 $\mathbf{x}_b$ 的项，然后配方，以便积分。只取出包含 $\mathbf{x}_b$ 的项，可得

$$
\begin{aligned}
-\frac{1}{2}\mathbf{x}_b^{\mathrm T}\boldsymbol{\Lambda}_{bb}\mathbf{x}_b+\mathbf{x}_b^{\mathrm T}\mathbf{m}
&=-\frac{1}{2}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})\\
&\quad+\frac{1}{2}\mathbf{m}^{\mathrm T}\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m},
\end{aligned} \tag{3.68}
$$

其中定义

$$
\mathbf{m}=\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a). \tag{3.69}
$$

<!-- pdf-page: 99 -->

可见，式 (3.68) 右侧第一项把对 $\mathbf{x}_b$ 的依赖写成了高斯分布的标准二次型，另一项则与 $\mathbf{x}_b$ 无关（但与 $\mathbf{x}_a$ 有关）。因此，对该二次型取指数后，式 (3.67) 所需的 $\mathbf{x}_b$ 积分变为

$$
\int\exp\left\{-\frac{1}{2}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})^{\mathrm T}\boldsymbol{\Lambda}_{bb}(\mathbf{x}_b-\boldsymbol{\Lambda}_{bb}^{-1}\mathbf{m})\right\}\mathrm{d}\mathbf{x}_b. \tag{3.70}
$$

这是对一个未归一化的高斯分布积分，结果是归一化系数的倒数，因此很容易求出。由式 (3.26) 的归一化高斯分布可知，这个系数与均值无关，只取决于协方差矩阵的行列式。所以，对 $\mathbf{x}_b$ 配方后即可将它积分掉；式 (3.68) 左侧各项中，唯一剩下的与 $\mathbf{x}_a$ 有关的项，就是式 (3.68) 右侧最后一项，其中 $\mathbf{m}$ 由式 (3.69) 给出。将它与式 (3.54) 中其余依赖 $\mathbf{x}_a$ 的项合并，得到

$$
\begin{aligned}
&\frac{1}{2}[\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)]^{\mathrm T}
\boldsymbol{\Lambda}_{bb}^{-1}[\boldsymbol{\Lambda}_{bb}\boldsymbol{\mu}_b-\boldsymbol{\Lambda}_{ba}(\mathbf{x}_a-\boldsymbol{\mu}_a)]\\
&\qquad-\frac{1}{2}\mathbf{x}_a^{\mathrm T}\boldsymbol{\Lambda}_{aa}\mathbf{x}_a
+\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}\boldsymbol{\mu}_a+\boldsymbol{\Lambda}_{ab}\boldsymbol{\mu}_b)+\mathrm{const}\\
&=-\frac{1}{2}\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})\mathbf{x}_a\\
&\qquad+\mathbf{x}_a^{\mathrm T}(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})\boldsymbol{\mu}_a+\mathrm{const}.
\end{aligned} \tag{3.71}
$$

这里 $\mathrm{const}$ 表示与 $\mathbf{x}_a$ 无关的量。再次与式 (3.55) 比较，可知边缘分布 $p(\mathbf{x}_a)$ 的协方差为

$$
\boldsymbol{\Sigma}_a=(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})^{-1}. \tag{3.72}
$$

类似地，其均值为

$$
\boldsymbol{\Sigma}_a(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})\boldsymbol{\mu}_a=\boldsymbol{\mu}_a, \tag{3.73}
$$

这里使用了式 (3.72)。协方差 (3.72) 用式 (3.53) 的分块精度矩阵表示。我们可以像处理条件分布时一样，依据式 (3.51) 中协方差矩阵的相应分块重写它。这些分块矩阵满足

$$
\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}^{-1}
=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix}. \tag{3.74}
$$

利用式 (3.60)，便有

$$
(\boldsymbol{\Lambda}_{aa}-\boldsymbol{\Lambda}_{ab}\boldsymbol{\Lambda}_{bb}^{-1}\boldsymbol{\Lambda}_{ba})^{-1}=\boldsymbol{\Sigma}_{aa}. \tag{3.75}
$$

<!-- pdf-page: 100 -->

因此得到符合直觉的结果：边缘分布 $p(\mathbf{x}_a)$ 的均值和协方差分别为

$$
\mathbb{E}[\mathbf{x}_a]=\boldsymbol{\mu}_a \tag{3.76}
$$

$$
\operatorname{cov}[\mathbf{x}_a]=\boldsymbol{\Sigma}_{aa}. \tag{3.77}
$$

可见，对于边缘分布，用分块协方差矩阵表示均值和协方差最简单；相比之下，对于条件分布，用分块精度矩阵表示更简单。

分块高斯分布的边缘分布和条件分布的结果可概括如下。给定联合高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，令 $\boldsymbol{\Lambda}\equiv\boldsymbol{\Sigma}^{-1}$，并作以下分块：

$$
\mathbf{x}=\begin{pmatrix}\mathbf{x}_a\\\mathbf{x}_b\end{pmatrix},\qquad
\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\end{pmatrix} \tag{3.78}
$$

$$
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}\end{pmatrix},\qquad
\boldsymbol{\Lambda}=\begin{pmatrix}\boldsymbol{\Lambda}_{aa}&\boldsymbol{\Lambda}_{ab}\\\boldsymbol{\Lambda}_{ba}&\boldsymbol{\Lambda}_{bb}\end{pmatrix}. \tag{3.79}
$$

那么条件分布为

$$
p(\mathbf{x}_a\mid\mathbf{x}_b)=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_{a\mid b},\boldsymbol{\Lambda}_{aa}^{-1}) \tag{3.80}
$$

译注：原书式 (3.80) 右端写作 $\mathbf x$，但左端的条件分布以 $\mathbf x_a$ 为自变量；按上下文，右端此处应为 $\mathbf x_a$。

$$
\boldsymbol{\mu}_{a\mid b}=\boldsymbol{\mu}_a-\boldsymbol{\Lambda}_{aa}^{-1}\boldsymbol{\Lambda}_{ab}(\mathbf{x}_b-\boldsymbol{\mu}_b) \tag{3.81}
$$

而边缘分布为

$$
p(\mathbf{x}_a)=\mathcal{N}(\mathbf{x}_a\mid\boldsymbol{\mu}_a,\boldsymbol{\Sigma}_{aa}). \tag{3.82}
$$

图 3.5 用两个变量的例子说明多元高斯分布对应的条件分布和边缘分布。

### 3.2.6 贝叶斯定理

在第 3.2.4 和 3.2.5 小节，我们考察高斯分布 $p(\mathbf{x})$：把向量 $\mathbf{x}$ 划分为两个子向量 $\mathbf{x}=(\mathbf{x}_a,\mathbf{x}_b)$，然后求出条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 和边缘分布 $p(\mathbf{x}_a)$。我们注意到，条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的均值是 $\mathbf{x}_b$ 的线性函数。现在假设已知高斯边缘分布 $p(\mathbf{x})$ 和高斯条件分布 $p(\mathbf{y}\mid\mathbf{x})$，后者的均值是 $\mathbf{x}$ 的线性函数，协方差与 $\mathbf{x}$ 无关。这是线性高斯模型的一个例子（Roweis 和 Ghahramani，1999；见第 11.1.4 节）。我们希望求出边缘分布 $p(\mathbf{y})$ 和条件分布 $p(\mathbf{x}\mid\mathbf{y})$。这种结构出现在多类生成模型中（见第 16 章），在这里先推导一般结果将很方便。

令边缘分布和条件分布分别为

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1}) \tag{3.83}
$$

$$
p(\mathbf{y}\mid\mathbf{x})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\mathbf{x}+\mathbf{b},\mathbf{L}^{-1}) \tag{3.84}
$$

<!-- pdf-page: 101 -->

<figure id="fig-3-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-5.png" alt="双变量高斯分布的等密度轮廓及 x_b 等于 0.7 时的边缘与条件密度曲线">
  <figcaption>图 3.5：(a) 两个变量上的高斯分布 $p(x_a,x_b)$ 的等密度轮廓。(b) 边缘分布 $p(x_a)$（蓝色曲线），以及 $x_b=0.7$ 时的条件分布 $p(x_a\mid x_b)$（红色曲线）。</figcaption>
</figure>

其中 $\boldsymbol{\mu}$、$\mathbf{A}$ 和 $\mathbf{b}$ 是控制均值的参数，$\boldsymbol{\Lambda}$ 和 $\mathbf{L}$ 是精度矩阵。如果 $\mathbf{x}$ 的维数为 $M$，$\mathbf{y}$ 的维数为 $D$，那么矩阵 $\mathbf{A}$ 的大小为 $D\times M$。

首先求 $\mathbf{x}$ 和 $\mathbf{y}$ 的联合分布。定义

$$
\mathbf{z}=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix} \tag{3.85}
$$

然后考察联合分布的对数：

$$
\begin{aligned}
\ln p(\mathbf{z})
&=\ln p(\mathbf{x})+\ln p(\mathbf{y}\mid\mathbf{x})\\
&=-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu})\\
&\quad-\frac{1}{2}(\mathbf{y}-\mathbf{A}\mathbf{x}-\mathbf{b})^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{A}\mathbf{x}-\mathbf{b})+\mathrm{const},
\end{aligned} \tag{3.86}
$$

其中 $\mathrm{const}$ 表示与 $\mathbf{x}$ 和 $\mathbf{y}$ 无关的项。和前面一样，它是 $\mathbf{z}$ 的分量的二次函数，因此 $p(\mathbf{z})$ 是高斯分布。为求这一高斯分布的精度，考虑式 (3.86) 的二阶项，可写为

$$
\begin{aligned}
&-\frac{1}{2}\mathbf{x}^{\mathrm T}(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})\mathbf{x}
-\frac{1}{2}\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{y}
+\frac{1}{2}\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{A}\mathbf{x}
+\frac{1}{2}\mathbf{x}^{\mathrm T}\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{y}\\
&=-\frac{1}{2}\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}^{\mathrm T}
\begin{pmatrix}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A}&-\mathbf{A}^{\mathrm T}\mathbf{L}\\
-\mathbf{L}\mathbf{A}&\mathbf{L}
\end{pmatrix}
\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}
=-\frac{1}{2}\mathbf{z}^{\mathrm T}\mathbf{R}\mathbf{z}
\end{aligned} \tag{3.87}
$$

所以 $\mathbf{z}$ 上的高斯分布的精度（逆协方差）矩阵为

<!-- pdf-page: 102 -->

$$
\mathbf{R}=
\begin{pmatrix}
\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A}&-\mathbf{A}^{\mathrm T}\mathbf{L}\\
-\mathbf{L}\mathbf{A}&\mathbf{L}
\end{pmatrix}. \tag{3.88}
$$

协方差矩阵可由精度矩阵求逆得到。利用式 (3.60) 的矩阵求逆公式（习题 3.23），得到

$$
\operatorname{cov}[\mathbf{z}]=\mathbf{R}^{-1}
=\begin{pmatrix}
\boldsymbol{\Lambda}^{-1}&\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}\\
\mathbf{A}\boldsymbol{\Lambda}^{-1}&\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}
\end{pmatrix}. \tag{3.89}
$$

类似地，可以从式 (3.86) 中找出线性项，从而确定 $\mathbf{z}$ 上高斯分布的均值。这些线性项为

$$
\mathbf{x}^{\mathrm T}\boldsymbol{\Lambda}\boldsymbol{\mu}
-\mathbf{x}^{\mathrm T}\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}
+\mathbf{y}^{\mathrm T}\mathbf{L}\mathbf{b}
=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}^{\mathrm T}
\begin{pmatrix}\boldsymbol{\Lambda}\boldsymbol{\mu}-\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}\\\mathbf{L}\mathbf{b}\end{pmatrix}. \tag{3.90}
$$

使用前面通过多元高斯分布的二次型配方得到的式 (3.55)，可知 $\mathbf{z}$ 的均值为

$$
\mathbb{E}[\mathbf{z}]
=\mathbf{R}^{-1}
\begin{pmatrix}\boldsymbol{\Lambda}\boldsymbol{\mu}-\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{b}\\\mathbf{L}\mathbf{b}\end{pmatrix}. \tag{3.91}
$$

利用式 (3.89)（习题 3.24），可得

$$
\mathbb{E}[\mathbf{z}]=\begin{pmatrix}\boldsymbol{\mu}\\\mathbf{A}\boldsymbol{\mu}+\mathbf{b}\end{pmatrix}. \tag{3.92}
$$

接着求对 $\mathbf{x}$ 边缘化后的分布 $p(\mathbf{y})$。回顾：高斯随机向量的一部分分量的边缘分布，用分块协方差矩阵表示时，形式特别简单；其均值和协方差分别由式 (3.76) 和 (3.77) 给出（见第 3.2 节）。使用式 (3.89) 和 (3.92)，可得 $p(\mathbf{y})$ 的均值和协方差为

$$
\mathbb{E}[\mathbf{y}]=\mathbf{A}\boldsymbol{\mu}+\mathbf{b} \tag{3.93}
$$

$$
\operatorname{cov}[\mathbf{y}]=\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}. \tag{3.94}
$$

一个特例是 $\mathbf{A}=\mathbf{I}$，此时边缘分布化为两个高斯分布的卷积。可以看到，卷积的均值等于两个高斯分布均值之和，协方差等于它们协方差之和。

最后求条件分布 $p(\mathbf{x}\mid\mathbf{y})$。回顾：根据式 (3.57) 和 (3.59)，条件分布用分块精度矩阵表示最简单（见第 3.2 节）。将这些结果应用于式 (3.89) 和 (3.92)，得到条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 的均值和协方差：

$$
\mathbb{E}[\mathbf{x}\mid\mathbf{y}]
=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}
\{\mathbf{A}^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda}\boldsymbol{\mu}\} \tag{3.95}
$$

$$
\operatorname{cov}[\mathbf{x}\mid\mathbf{y}]
=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}. \tag{3.96}
$$

<!-- pdf-page: 103 -->

求解这一条件分布可视为贝叶斯定理的一个例子：将 $p(\mathbf{x})$ 理解为 $\mathbf{x}$ 上的先验分布；如果观测到变量 $\mathbf{y}$，那么条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 就是相应的后验分布。求得边缘分布和条件分布后，我们实际上把联合分布 $p(\mathbf{z})=p(\mathbf{x})p(\mathbf{y}\mid\mathbf{x})$ 写成了 $p(\mathbf{x}\mid\mathbf{y})p(\mathbf{y})$。

上述结果可概括如下。给定 $\mathbf{x}$ 的高斯边缘分布，以及给定 $\mathbf{x}$ 时 $\mathbf{y}$ 的高斯条件分布：

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1}) \tag{3.97}
$$

$$
p(\mathbf{y}\mid\mathbf{x})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\mathbf{x}+\mathbf{b},\mathbf{L}^{-1}), \tag{3.98}
$$

则 $\mathbf{y}$ 的边缘分布和给定 $\mathbf{y}$ 时 $\mathbf{x}$ 的条件分布分别为

$$
p(\mathbf{y})=\mathcal{N}(\mathbf{y}\mid\mathbf{A}\boldsymbol{\mu}+\mathbf{b},\mathbf{L}^{-1}+\mathbf{A}\boldsymbol{\Lambda}^{-1}\mathbf{A}^{\mathrm T}) \tag{3.99}
$$

$$
p(\mathbf{x}\mid\mathbf{y})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\Sigma}\{\mathbf{A}^{\mathrm T}\mathbf{L}(\mathbf{y}-\mathbf{b})+\boldsymbol{\Lambda}\boldsymbol{\mu}\},\boldsymbol{\Sigma}), \tag{3.100}
$$

其中

$$
\boldsymbol{\Sigma}=(\boldsymbol{\Lambda}+\mathbf{A}^{\mathrm T}\mathbf{L}\mathbf{A})^{-1}. \tag{3.101}
$$

### 3.2.7 极大似然

给定数据集 $\mathbf{X}=(\mathbf{x}_1,\ldots,\mathbf{x}_N)^{\mathrm T}$，假设观测值 $\{\mathbf{x}_n\}$ 是从多元高斯分布中独立抽取的，就可以用极大似然法估计分布参数。对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})
=-\frac{ND}{2}\ln(2\pi)-\frac{N}{2}\ln|\boldsymbol{\Sigma}|
-\frac{1}{2}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}). \tag{3.102}
$$

简单整理后可见，似然函数只通过以下两个量依赖数据集：

$$
\sum_{n=1}^{N}\mathbf{x}_n,\qquad
\sum_{n=1}^{N}\mathbf{x}_n\mathbf{x}_n^{\mathrm T}. \tag{3.103}
$$

它们称为高斯分布的充分统计量。利用式 (A.19)（见附录 A），对数似然函数对 $\boldsymbol{\mu}$ 的导数为

$$
\frac{\partial}{\partial\boldsymbol{\mu}}\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})
=\sum_{n=1}^{N}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}), \tag{3.104}
$$

令此导数为零，得到均值的极大似然估计解：

$$
\boldsymbol{\mu}_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n, \tag{3.105}
$$

<!-- pdf-page: 104 -->

即观测数据点集合的均值。关于 $\boldsymbol{\Sigma}$ 最大化式 (3.102) 则复杂一些。最简单的方法是先忽略对称性约束，再证明得到的解确实如要求那样对称（习题 3.28）。也可以显式加入对称性和正定性约束来推导此结果，参见 Magnus 和 Neudecker（1999）。结果符合预期，为

$$
\boldsymbol{\Sigma}_{\mathrm{ML}}
=\frac{1}{N}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})^{\mathrm T}, \tag{3.106}
$$

其中包含 $\boldsymbol{\mu}_{\mathrm{ML}}$，因为这是对 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 联合最大化的结果。注意，式 (3.105) 给出的 $\boldsymbol{\mu}_{\mathrm{ML}}$ 不依赖 $\boldsymbol{\Sigma}_{\mathrm{ML}}$，因此可以先计算前者，再用它计算后者。

如果在真实分布下求极大似然解的期望（习题 3.29），得到

$$
\mathbb{E}[\boldsymbol{\mu}_{\mathrm{ML}}]=\boldsymbol{\mu} \tag{3.107}
$$

$$
\mathbb{E}[\boldsymbol{\Sigma}_{\mathrm{ML}}]=\frac{N-1}{N}\boldsymbol{\Sigma}. \tag{3.108}
$$

可见，均值的极大似然估计的期望等于真实均值。然而，协方差的极大似然估计的期望小于真实值，因此是有偏的。可以定义另一个估计量 $\widetilde{\boldsymbol{\Sigma}}$ 来修正这一偏差：

$$
\widetilde{\boldsymbol{\Sigma}}
=\frac{1}{N-1}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})(\mathbf{x}_n-\boldsymbol{\mu}_{\mathrm{ML}})^{\mathrm T}. \tag{3.109}
$$

由式 (3.106) 和 (3.108) 显然可知，$\widetilde{\boldsymbol{\Sigma}}$ 的期望等于 $\boldsymbol{\Sigma}$。

### 3.2.8 序贯估计

前面讨论的极大似然解是一种批量方法，要一次处理整个训练数据集。另一种方法是序贯方法（sequential method），它允许逐个处理数据点，然后将已处理的数据点丢弃。这对在线应用，以及一次批量处理所有数据点不可行的大型数据，都很重要。

考虑式 (3.105) 中均值 $\boldsymbol{\mu}_{\mathrm{ML}}$ 的极大似然估计量。若它基于 $N$ 个观测值，我们记作 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$。如果把

<!-- pdf-page: 105 -->

<!-- join-previous-paragraph -->

最后一个数据点 $\mathbf{x}_N$ 的贡献单独分离出来，可得

$$
\begin{aligned}
\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}
&=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n\\
&=\frac{1}{N}\mathbf{x}_N+\frac{1}{N}\sum_{n=1}^{N-1}\mathbf{x}_n\\
&=\frac{1}{N}\mathbf{x}_N+\frac{N-1}{N}\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}\\
&=\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}
+\frac{1}{N}\left(\mathbf{x}_N-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}\right).
\end{aligned} \tag{3.110}
$$

<figure id="fig-3-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-6.png" alt="老忠实间歇泉数据的散点图，与一个高斯分布及两个高斯分布组合的等密度轮廓比较">
  <figcaption>图 3.6：“老忠实间歇泉”数据图，红色曲线为等概率密度轮廓。(a) 用极大似然法拟合数据的单个高斯分布。它未能捕捉数据的两个聚集区域，甚至把大量概率质量放在两个区域之间、数据相对稀疏的中间地带。(b) 同样由极大似然法拟合的两个高斯分布的线性组合，它更好地表示了数据。</figcaption>
</figure>

这一结果可以这样理解：观察前 $N-1$ 个数据点后，我们用 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}$ 估计 $\boldsymbol{\mu}$。现在又观察到数据点 $\mathbf{x}_N$，便沿着“误差信号”方向 $\mathbf{x}_N-\boldsymbol{\mu}_{\mathrm{ML}}^{(N-1)}$，将旧估计移动一小步，步长比例为 $1/N$，从而得到更新后的估计 $\boldsymbol{\mu}_{\mathrm{ML}}^{(N)}$。注意，随着 $N$ 增大，后续各数据点的贡献逐渐减小。

### 3.2.9 高斯混合分布

高斯分布虽然有一些重要的解析性质，但用于真实数据集建模时存在明显局限。以图 3.6(a) 为例。这是“老忠实间歇泉”（Old Faithful）数据集，包含美国黄石国家公园老忠实间歇泉的 272 次喷发测量。每次测量记录喷发持续时间（分钟，横轴）和距离下一次喷发的时间（分钟，纵轴）。可以看到，数据形成两个主要的聚集区域，单个高斯分布无法捕捉这种结构。

我们可以预期，两个高斯分布的叠加能更好地表示这一数据集的结构；事实上，

<!-- pdf-page: 106 -->

<!-- join-previous-paragraph -->

图 3.6(b) 确实表明如此。像这样的叠加，是由高斯分布等更基本分布的线性组合形成的，可以构建成称为混合分布的概率模型（见第 15 章）。本节用高斯分布说明混合模型的框架。更一般地，混合模型也可以是其他分布的线性组合，例如二值变量的伯努利分布混合。图 3.7 表明，高斯分布的线性组合可以形成十分复杂的密度。只要使用足够多的高斯分布，并调整它们的均值、协方差以及线性组合中的系数，就可以把几乎任何连续分布近似到任意精度。

<figure id="fig-3-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-7.png" alt="三条蓝色高斯密度曲线及其红色混合密度曲线">
  <figcaption>图 3.7：一维高斯混合分布示例：三条蓝色曲线分别表示乘以各自系数的高斯分布，红色曲线表示它们之和。</figcaption>
</figure>

因此，考虑以下由 $K$ 个高斯密度叠加而成的形式：

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k), \tag{3.111}
$$

它称为高斯混合分布（mixture of Gaussians）。每个高斯密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$ 称为混合分布的一个分量（component），有自己的均值 $\boldsymbol{\mu}_k$ 和协方差 $\boldsymbol{\Sigma}_k$。图 3.8 展示了含三个分量的二维高斯混合分布的轮廓图和曲面图。

式 (3.111) 中的参数 $\pi_k$ 称为混合系数（mixing coefficient）。对式 (3.111) 两边关于 $\mathbf{x}$ 积分，并注意 $p(\mathbf{x})$ 与各个高斯分量都已归一化，可得

$$
\sum_{k=1}^{K}\pi_k=1. \tag{3.112}
$$

另外，由于 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\geqslant0$，要使 $p(\mathbf{x})\geqslant0$，一个充分条件是对所有 $k$ 都有 $\pi_k\geqslant0$。将它与式 (3.112) 结合，得到

$$
0\leqslant\pi_k\leqslant1. \tag{3.113}
$$

因此，混合系数满足作为概率的条件。我们将在第 15 章看到，混合分布的这种概率解释非常有用。

<!-- pdf-page: 107 -->

<figure id="fig-3-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-8.png" alt="二维空间中的三个高斯分量、混合密度等值线及其三维曲面">
  <figcaption>图 3.8：二维空间中三个高斯分布的混合示意。(a) 各混合分量的等密度轮廓，三个分量分别用红、蓝、绿表示，各分量下方标出相应的混合系数值。(b) 混合分布的边缘概率密度 $p(\mathbf{x})$ 的等密度轮廓。(c) 分布 $p(\mathbf{x})$ 的曲面图。</figcaption>
</figure>

译注：原书图注称三个系数都在对应分量下方；图中绿色分量的 $\pi_3=0.2$ 实际标在上方。

根据概率的加法法则和乘法法则，边缘密度可写为

$$
p(\mathbf{x})=\sum_{k=1}^{K}p(k)p(\mathbf{x}\mid k), \tag{3.114}
$$

这与式 (3.111) 等价：可将 $\pi_k=p(k)$ 看作选中第 $k$ 个分量的先验概率，将密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)=p(\mathbf{x}\mid k)$ 看作给定 $k$ 时 $\mathbf{x}$ 的概率。后续章节将看到，相应的后验概率 $p(k\mid\mathbf{x})$ 起着重要作用，它也称为责任度（responsibility）。根据贝叶斯定理，

$$
\begin{aligned}
\gamma_k(\mathbf{x})&\equiv p(k\mid\mathbf{x})\\
&=\frac{p(k)p(\mathbf{x}\mid k)}{\sum_l p(l)p(\mathbf{x}\mid l)}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}
{\sum_l\pi_l\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_l,\boldsymbol{\Sigma}_l)}.
\end{aligned} \tag{3.115}
$$

高斯混合分布的形式由参数 $\boldsymbol{\pi}$、$\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 决定；这里使用记法 $\boldsymbol{\pi}\equiv\{\pi_1,\ldots,\pi_K\}$、$\boldsymbol{\mu}\equiv\{\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K\}$、$\boldsymbol{\Sigma}\equiv\{\boldsymbol{\Sigma}_1,\ldots,\boldsymbol{\Sigma}_K\}$。确定这些参数的一种方法是极大似然法。由式 (3.111)，对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})
=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\} \tag{3.116}
$$

其中 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$。由于对 $k$ 的求和位于对数运算内部，我们立刻看到，此时的情况比单个高斯分布复杂得多。

<!-- pdf-page: 108 -->

因此，这些参数的极大似然解不再有封闭形式的解析表达式。一种最大化似然函数的方法是使用迭代数值优化技术。另一种方法是采用称为**期望最大化**（expectation maximization）的有力框架；它广泛适用于多种深度生成模型（见第 15 章）。

## 3.3 周期变量

高斯分布本身具有很高的实用价值，也是更复杂概率模型的构件，但在某些情形下，它并不适合用来描述连续变量的密度。实际应用中一个重要的例子就是周期变量。

周期变量的一个例子是某个地理位置的风向。例如，我们可以测量多个地点的风向，并希望用一个参数化分布概括这些数据。另一个例子是日历时间：我们可能希望对具有 24 小时周期或年度周期的量建模。用角坐标（极坐标）$0\leqslant\theta<2\pi$ 表示这类量很方便。

一种看似可行的办法是选取某个方向作为原点，然后对周期变量使用高斯分布等常规分布。然而，所得结果会强烈依赖于这个任意选择的原点。例如，假设有两个观测值 $\theta_1=1^\circ$ 和 $\theta_2=359^\circ$，并用标准的一元高斯分布对其建模。若把原点放在 $0^\circ$，样本均值就是 $180^\circ$，标准差为 $179^\circ$；若把原点放在 $180^\circ$，均值则为 $0^\circ$，标准差为 $1^\circ$。显然，我们需要一种专门处理周期变量的方法。

### 3.3.1 冯·米塞斯分布

考虑求周期变量 $\theta$ 的一组观测 $\mathcal D=\{\theta_1,\ldots,\theta_N\}$ 的均值，其中 $\theta$ 以弧度计量。我们已经看到，简单平均 $(\theta_1+\cdots+\theta_N)/N$ 会强烈依赖坐标选择。为了得到不随坐标系变化的均值度量，注意这些观测可以视为单位圆上的点，因此可用二维单位向量 $\mathbf x_1,\ldots,\mathbf x_N$ 描述，其中对 $n=1,\ldots,N$ 有 $\|\mathbf x_n\|=1$，如图 3.9 所示。我们可以改为对向量 $\{\mathbf x_n\}$ 求平均：

$$
\bar{\mathbf x}=\frac1N\sum_{n=1}^{N}\mathbf x_n.\tag{3.117}
$$

然后求出该平均向量对应的角度 $\bar\theta$。显然，这样定义的均值位置不依赖于角坐标的原点。注意，$\bar{\mathbf x}$ 通常位于单位圆内部。各观测的笛卡儿坐标为

<!-- pdf-page: 109 -->

<!-- join-previous-paragraph -->

$\mathbf x_n=(\cos\theta_n,\sin\theta_n)$，样本均值的笛卡儿坐标可写为 $\bar{\mathbf x}=(\bar r\cos\bar\theta,\bar r\sin\bar\theta)$。将其代入式 (3.117)，并分别比较 $x_1$ 和 $x_2$ 分量，得到

$$
\bar x_1=\bar r\cos\bar\theta=\frac1N\sum_{n=1}^{N}\cos\theta_n,
\qquad
\bar x_2=\bar r\sin\bar\theta=\frac1N\sum_{n=1}^{N}\sin\theta_n.\tag{3.118}
$$

<figure id="fig-3-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-9.png" alt="单位圆上的四个二维观测向量及其平均向量；平均向量的长度和角度分别标为 r 上加横线与 θ 上加横线">
  <figcaption>图 3.9：将周期变量的取值 $\theta_n$ 表示为位于单位圆上的二维向量 $\mathbf x_n$。图中还画出了这些向量的平均值 $\bar{\mathbf x}$。</figcaption>
</figure>

两式相除，利用恒等式 $\tan\bar\theta=\sin\bar\theta/\cos\bar\theta$，即可解得

$$
\bar\theta=\tan^{-1}\!\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.\tag{3.119}
$$

译注：式 (3.119) 与后面的式 (3.134) 只给出正切值；实际确定角度时，还须根据正弦和余弦两个和式判断象限，例如使用 `atan2`。

稍后我们会看到，这一结果会自然地成为极大似然估计量。

首先，需要定义高斯分布在周期变量上的推广，称为**冯·米塞斯分布**（von Mises distribution）。这里我们只讨论一元分布，尽管任意维超球面上也存在类似的周期分布（Mardia and Jupp, 2000）。

按照惯例，我们考虑周期为 $2\pi$ 的分布 $p(\theta)$。定义在 $\theta$ 上的概率密度 $p(\theta)$ 除了必须非负、积分为一，还必须具有周期性。因此，它要满足以下三个条件：

$$
p(\theta)\geqslant0,\tag{3.120}
$$

$$
\int_0^{2\pi}p(\theta)\,\mathrm d\theta=1,\tag{3.121}
$$

$$
p(\theta+2\pi)=p(\theta).\tag{3.122}
$$

由式 (3.122) 可知，对任意整数 $M$，有 $p(\theta+M2\pi)=p(\theta)$。

如下可以容易地得到一个满足这三个性质、形状类似高斯分布的分布。考虑定义在两个变量 $\mathbf x=(x_1,x_2)$ 上的高斯分布，

<!-- pdf-page: 110 -->

<!-- join-previous-paragraph -->

其均值为 $\boldsymbol\mu=(\mu_1,\mu_2)$，协方差矩阵为 $\boldsymbol\Sigma=\sigma^2\mathbf I$，其中 $\mathbf I$ 为 $2\times2$ 单位矩阵。于是

$$
p(x_1,x_2)=\frac1{2\pi\sigma^2}\exp\!\left\{-\frac{(x_1-\mu_1)^2+(x_2-\mu_2)^2}{2\sigma^2}\right\}.\tag{3.123}
$$

<figure id="fig-3-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-10.png" alt="二维高斯的蓝色等密度圆与红色单位圆相交，坐标轴为 x1 和 x2">
  <figcaption>图 3.10：考虑式 (3.123) 所示的二维高斯分布，其等密度轮廓以蓝色表示，再将其限制在红色的单位圆上，便可导出冯·米塞斯分布。</figcaption>
</figure>

$p(\mathbf x)$ 的等值轮廓是圆，如图 3.10 所示。

现在考虑这一分布在固定半径的圆上的取值。按构造，它必然具有周期性，尽管尚未归一化。将笛卡儿坐标 $(x_1,x_2)$ 变换为极坐标 $(r,\theta)$，即可确定该分布的形式：

$$
x_1=r\cos\theta,\qquad x_2=r\sin\theta.\tag{3.124}
$$

我们还将均值 $\boldsymbol\mu$ 表示为极坐标：

$$
\mu_1=r_0\cos\theta_0,\qquad \mu_2=r_0\sin\theta_0.\tag{3.125}
$$

接着，把这些变换代入二维高斯分布 (3.123)，然后将其限制在单位圆 $r=1$ 上，并注意我们只关心对 $\theta$ 的依赖。聚焦于高斯分布的指数部分，有

$$
\begin{aligned}
&-\frac1{2\sigma^2}\left\{(r\cos\theta-r_0\cos\theta_0)^2+(r\sin\theta-r_0\sin\theta_0)^2\right\}\\
&\quad=-\frac1{2\sigma^2}\left\{1+r_0^2-2r_0\cos\theta\cos\theta_0-2r_0\sin\theta\sin\theta_0\right\}\\
&\quad=\frac{r_0}{\sigma^2}\cos(\theta-\theta_0)+\mathrm{const},
\end{aligned}\tag{3.126}
$$

其中“const”表示与 $\theta$ 无关的项。这里用到了三角恒等式

$$
\cos^2 A+\sin^2 A=1,\tag{3.127}
$$

$$
\cos A\cos B+\sin A\sin B=\cos(A-B).\tag{3.128}
$$

若定义 $m=r_0/\sigma^2$，便得到单位圆 $r=1$ 上 $p(\theta)$ 的最终表达式：

$$
p(\theta\mid\theta_0,m)=\frac1{2\pi I_0(m)}\exp\{m\cos(\theta-\theta_0)\}.\tag{3.129}
$$

<!-- pdf-page: 111 -->

<figure id="fig-3-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-11.png" alt="两组参数下冯·米塞斯分布的笛卡儿曲线图和极坐标图；红色参数 m 等于 5、θ0 等于 π/4，蓝色参数 m 等于 1、θ0 等于 3π/4">
  <figcaption>图 3.11：两组不同参数下的冯·米塞斯分布。左图为笛卡儿坐标图，右图为相应的极坐标图。</figcaption>
</figure>

该分布称为**冯·米塞斯分布**，也称**圆形正态分布**（circular normal）。参数 $\theta_0$ 对应分布的均值；$m$ 称为**集中度参数**，类似于高斯分布的逆方差（即精度）。式 (3.129) 中的归一化系数由 $I_0(m)$ 表示，它是第一类零阶修正贝塞尔函数（Abramowitz and Stegun, 1965），定义为

$$
I_0(m)=\frac1{2\pi}\int_0^{2\pi}\exp\{m\cos\theta\}\,\mathrm d\theta.\tag{3.130}
$$

当 $m$ 很大时，该分布近似为高斯分布（见习题 3.31）。图 3.11 画出了冯·米塞斯分布，图 3.12 画出了函数 $I_0(m)$。

现在考虑冯·米塞斯分布的参数 $\theta_0$ 和 $m$ 的极大似然估计量。对数似然函数为

$$
\ln p(\mathcal D\mid\theta_0,m)=-N\ln(2\pi)-N\ln I_0(m)+m\sum_{n=1}^{N}\cos(\theta_n-\theta_0).\tag{3.131}
$$

令其关于 $\theta_0$ 的导数为零，得到

$$
\sum_{n=1}^{N}\sin(\theta_n-\theta_0)=0.\tag{3.132}
$$

为了求解 $\theta_0$，我们利用三角恒等式

$$
\sin(A-B)=\cos B\sin A-\cos A\sin B,\tag{3.133}
$$

由此得到（见习题 3.32）

<!-- pdf-page: 112 -->

<figure id="fig-3-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-12.png" alt="左图是第一类零阶修正贝塞尔函数 I0(m)，右图是 A(m) 等于 I1(m) 除以 I0(m) 的曲线">
  <figcaption>图 3.12：式 (3.130) 定义的贝塞尔函数 $I_0(m)$ 与式 (3.136) 定义的函数 $A(m)$ 的图像。</figcaption>
</figure>

$$
\theta_0^{\mathrm{ML}}=\tan^{-1}\!\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.\tag{3.134}
$$

这正是先前在二维笛卡儿空间中求观测均值时得到的式 (3.119)。

类似地，对式 (3.131) 关于 $m$ 最大化，并利用 $I'_0(m)=I_1(m)$（Abramowitz and Stegun, 1965），有

$$
A(m_{\mathrm{ML}})=\frac1N\sum_{n=1}^{N}\cos(\theta_n-\theta_0^{\mathrm{ML}}),\tag{3.135}
$$

其中代入了 $\theta_0$ 的极大似然解 $\theta_0^{\mathrm{ML}}$（请记住，我们是在联合优化 $\theta_0$ 和 $m$），并定义了

$$
A(m)=\frac{I_1(m)}{I_0(m)}.\tag{3.136}
$$

图 3.12 给出了函数 $A(m)$ 的图像。利用三角恒等式 (3.128)，式 (3.135) 可以写成

$$
A(m_{\mathrm{ML}})=\left(\frac1N\sum_{n=1}^{N}\cos\theta_n\right)\cos\theta_0^{\mathrm{ML}}+\left(\frac1N\sum_{n=1}^{N}\sin\theta_n\right)\sin\theta_0^{\mathrm{ML}}.\tag{3.137}
$$

式 (3.137) 的右边容易计算，而函数 $A(m)$ 可以用数值方法求逆。冯·米塞斯分布的一个局限是它只有单个众数。将多个冯·米塞斯分布构成混合分布，就能得到一种灵活的周期变量建模框架，可以处理多个众数。

为求完整，这里简要提及构造周期分布的其他方法。最简单的是对观测值作直方图，将角坐标划分为固定的区间。这种方法简单而灵活，但也有明显局限；稍后更详细讨论直方图方法时会看到这一点（见第 3.5 节）。

<!-- pdf-page: 113 -->

另一种方法与冯·米塞斯分布一样，从欧几里得空间上的高斯分布出发，但不是把它限制在单位圆上，而是将其边缘化到单位圆上（Mardia and Jupp, 2000）。不过，这会得到更复杂的分布形式，这里不再讨论。最后，任何实数轴上的有效分布（例如高斯分布）都可以通过将连续的宽度为 $2\pi$ 的区间映射到周期变量 $(0,2\pi)$ 上，变成周期分布；这相当于把实数轴“缠绕”在单位圆上。所得分布同样比冯·米塞斯分布更难处理。

## 3.4 指数族

本章迄今研究的概率分布（混合模型除外）都是一大类分布——**指数族**（exponential family）——的具体例子（Duda and Hart, 1973; Bernardo and Smith, 1994）。指数族成员具有许多共同的重要性质；从一般形式讨论这些性质有助于理解它们。

给定参数 $\boldsymbol\eta$，定义在 $\mathbf x$ 上的指数族分布，是具有以下形式的分布集合：

$$
p(\mathbf x\mid\boldsymbol\eta)=h(\mathbf x)g(\boldsymbol\eta)\exp\{\boldsymbol\eta^{\mathsf T}\mathbf u(\mathbf x)\}.\tag{3.138}
$$

$\mathbf x$ 可以是标量或向量，也可以是离散或连续变量。$\boldsymbol\eta$ 称为分布的**自然参数**（natural parameters），$\mathbf u(\mathbf x)$ 是 $\mathbf x$ 的某个函数。函数 $g(\boldsymbol\eta)$ 可以理解为保证分布归一化的系数，因此满足

$$
g(\boldsymbol\eta)\int h(\mathbf x)\exp\{\boldsymbol\eta^{\mathsf T}\mathbf u(\mathbf x)\}\,\mathrm d\mathbf x=1.\tag{3.139}
$$

如果 $\mathbf x$ 是离散变量，则以求和代替积分。

先看本章前面介绍的几个分布，说明它们确实属于指数族。首先考虑伯努利分布：

$$
p(x\mid\mu)=\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}.\tag{3.140}
$$

将右边表示为其对数的指数，有

$$
\begin{aligned}
p(x\mid\mu)&=\exp\{x\ln\mu+(1-x)\ln(1-\mu)\}\\
&=(1-\mu)\exp\!\left\{\ln\!\left(\frac\mu{1-\mu}\right)x\right\}.
\end{aligned}\tag{3.141}
$$

与式 (3.138) 比较，可知

$$
\eta=\ln\!\left(\frac\mu{1-\mu}\right).\tag{3.142}
$$

<!-- pdf-page: 114 -->

由此可以解出 $\mu=\sigma(\eta)$，其中

$$
\sigma(\eta)=\frac1{1+\exp(-\eta)}\tag{3.143}
$$

称为**逻辑 sigmoid 函数**。于是可用式 (3.138) 的标准表示，将伯努利分布写为

$$
p(x\mid\eta)=\sigma(-\eta)\exp(\eta x),\tag{3.144}
$$

这里用到了 $1-\sigma(\eta)=\sigma(-\eta)$，这一等式很容易由式 (3.143) 证明。与式 (3.138) 比较，有

$$
u(x)=x,\tag{3.145}
$$

$$
h(x)=1,\tag{3.146}
$$

$$
g(\eta)=\sigma(-\eta).\tag{3.147}
$$

接着考虑多项分布。对于单个观测 $\mathbf x$，它具有如下形式：

$$
p(\mathbf x\mid\boldsymbol\mu)=\prod_{k=1}^{M}\mu_k^{x_k}=\exp\!\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\}.\tag{3.148}
$$

其中 $\mathbf x=(x_1,\ldots,x_M)^{\mathsf T}$。仍然可以把它写成式 (3.138) 的标准形式：

$$
p(\mathbf x\mid\boldsymbol\eta)=\exp(\boldsymbol\eta^{\mathsf T}\mathbf x),\tag{3.149}
$$

其中 $\eta_k=\ln\mu_k$，且 $\boldsymbol\eta=(\eta_1,\ldots,\eta_M)^{\mathsf T}$。再与式 (3.138) 比较，得到

$$
\mathbf u(\mathbf x)=\mathbf x,\tag{3.150}
$$

$$
h(\mathbf x)=1,\tag{3.151}
$$

$$
g(\boldsymbol\eta)=1.\tag{3.152}
$$

注意，各参数 $\eta_k$ 并不独立，因为参数 $\mu_k$ 受约束

$$
\sum_{k=1}^{M}\mu_k=1.\tag{3.153}
$$

因此，给定任意 $M-1$ 个 $\mu_k$，剩下那个参数的值也就确定了。在某些情况下，只用 $M-1$ 个参数表示分布以消除这一约束会更方便。利用式 (3.153)，将 $\mu_M$ 表示为其余 $\{\mu_k\}$（$k=1,\ldots,M-1$）的函数，即可得到 $M-1$ 个参数。注意，余下参数仍受下列约束：

$$
0\leqslant\mu_k\leqslant1,\qquad\sum_{k=1}^{M-1}\mu_k\leqslant1.\tag{3.154}
$$

<!-- pdf-page: 115 -->

利用约束 (3.153)，这一表示下的多项分布变为

$$
\begin{aligned}
\exp\!\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\}
&=\exp\!\left\{\sum_{k=1}^{M-1}x_k\ln\mu_k+\left(1-\sum_{k=1}^{M-1}x_k\right)\ln\!\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}\\
&=\exp\!\left\{\sum_{k=1}^{M-1}x_k\ln\!\left(\frac{\mu_k}{1-\sum_{j=1}^{M-1}\mu_j}\right)+\ln\!\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}.
\end{aligned}\tag{3.155}
$$

于是可定义

$$
\ln\!\left(\frac{\mu_k}{1-\sum_j\mu_j}\right)=\eta_k,\tag{3.156}
$$

先对两边关于 $k$ 求和，再整理并回代，可解出 $\mu_k$：

$$
\mu_k=\frac{\exp(\eta_k)}{1+\sum_j\exp(\eta_j)}.\tag{3.157}
$$

这称为 **softmax 函数**，或称**归一化指数函数**。在这种表示下，多项分布因而具有形式

$$
p(\mathbf x\mid\boldsymbol\eta)=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}\exp(\boldsymbol\eta^{\mathsf T}\mathbf x).\tag{3.158}
$$

这就是参数向量 $\boldsymbol\eta=(\eta_1,\ldots,\eta_{M-1})^{\mathsf T}$ 下的指数族标准形式，其中

$$
\mathbf u(\mathbf x)=\mathbf x,\tag{3.159}
$$

$$
h(\mathbf x)=1,\tag{3.160}
$$

$$
g(\boldsymbol\eta)=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}.\tag{3.161}
$$

最后，考虑高斯分布。对于一元高斯分布，有

$$
p(x\mid\mu,\sigma^2)=\frac1{(2\pi\sigma^2)^{1/2}}\exp\!\left\{-\frac1{2\sigma^2}(x-\mu)^2\right\},\tag{3.162}
$$

$$
=\frac1{(2\pi\sigma^2)^{1/2}}\exp\!\left\{-\frac1{2\sigma^2}x^2+\frac\mu{\sigma^2}x-\frac1{2\sigma^2}\mu^2\right\}.\tag{3.163}
$$

稍加整理后，即可把它写成指数族的标准形式 (3.138)（多元情形见习题 3.35），其中

<!-- pdf-page: 116 -->

$$
\boldsymbol\eta=\begin{pmatrix}\mu/\sigma^2\\-1/(2\sigma^2)\end{pmatrix},\tag{3.164}
$$

$$
\mathbf u(x)=\begin{pmatrix}x\\x^2\end{pmatrix},\tag{3.165}
$$

$$
h(x)=(2\pi)^{-1/2},\tag{3.166}
$$

$$
g(\boldsymbol\eta)=(-2\eta_2)^{1/2}\exp\!\left(\frac{\eta_1^2}{4\eta_2}\right).\tag{3.167}
$$

最后，我们有时还会使用式 (3.138) 的一种受限形式，取 $\mathbf u(\mathbf x)=\mathbf x$。不过，注意到若 $f(\mathbf x)$ 是归一化密度，则

$$
\frac1s f\!\left(\frac1s\mathbf x\right)\tag{3.168}
$$

也是归一化密度，其中 $s>0$ 是尺度参数，因此这一形式还可以稍作推广。综合两点，得到一组受限的指数族类条件密度：

$$
p(\mathbf x\mid\boldsymbol\lambda_k,s)=\frac1s h\!\left(\frac1s\mathbf x\right)g(\boldsymbol\lambda_k)\exp\!\left\{\frac1s\boldsymbol\lambda_k^{\mathsf T}\mathbf x\right\}.\tag{3.169}
$$

译注：式 (3.168)–(3.169) 按原书保留。若 $\mathbf x$ 为 $D$ 维向量，单靠尺度变换保持密度归一化通常需要 $s^{-D}$；原书的 $s^{-1}$ 只对应一维缩放。

注意，我们允许每个类别有自己的参数向量 $\boldsymbol\lambda_k$，但假定所有类别共用尺度参数 $s$。

### 3.4.1 充分统计量

现在考虑用极大似然法估计一般指数族分布 (3.138) 中的参数向量 $\boldsymbol\eta$。对式 (3.139) 两边关于 $\boldsymbol\eta$ 求梯度，有

$$
\begin{aligned}
&\nabla g(\boldsymbol\eta)\int h(\mathbf x)\exp\{\boldsymbol\eta^{\mathsf T}\mathbf u(\mathbf x)\}\,\mathrm d\mathbf x\\
&\quad+g(\boldsymbol\eta)\int h(\mathbf x)\exp\{\boldsymbol\eta^{\mathsf T}\mathbf u(\mathbf x)\}\mathbf u(\mathbf x)\,\mathrm d\mathbf x=0.
\end{aligned}\tag{3.170}
$$

整理，并再次利用式 (3.139)，得到

$$
-\frac1{g(\boldsymbol\eta)}\nabla g(\boldsymbol\eta)
=g(\boldsymbol\eta)\int h(\mathbf x)\exp\{\boldsymbol\eta^{\mathsf T}\mathbf u(\mathbf x)\}\mathbf u(\mathbf x)\,\mathrm d\mathbf x
=\mathbb E[\mathbf u(\mathbf x)].\tag{3.171}
$$

因此得到

$$
-\nabla\ln g(\boldsymbol\eta)=\mathbb E[\mathbf u(\mathbf x)].\tag{3.172}
$$

$\mathbf u(\mathbf x)$ 的协方差也可用 $g(\boldsymbol\eta)$ 的二阶导数表示，更高阶矩亦然（见习题 3.36）。因此，只要能归一化一个指数族分布，就总能通过简单求导得到它的矩。

<!-- pdf-page: 117 -->

现在考虑一组独立同分布的数据，记为 $\mathcal X=\{\mathbf x_1,\ldots,\mathbf x_N\}$。其似然函数为

$$
p(\mathcal X\mid\boldsymbol\eta)=\left(\prod_{n=1}^{N}h(\mathbf x_n)\right)g(\boldsymbol\eta)^N\exp\!\left\{\boldsymbol\eta^{\mathsf T}\sum_{n=1}^{N}\mathbf u(\mathbf x_n)\right\}.\tag{3.173}
$$

译注：原书此处把样本集末项写作 $\mathbf x_n$，式 (3.173) 却按 $N$ 个样本求积；这里按该式统一记作 $\mathbf x_N$。

令 $\ln p(\mathcal X\mid\boldsymbol\eta)$ 关于 $\boldsymbol\eta$ 的梯度为零，可得极大似然估计量 $\boldsymbol\eta_{\mathrm{ML}}$ 必须满足

$$
-\nabla\ln g(\boldsymbol\eta_{\mathrm{ML}})=\frac1N\sum_{n=1}^{N}\mathbf u(\mathbf x_n).\tag{3.174}
$$

原则上，可以求解该式得到 $\boldsymbol\eta_{\mathrm{ML}}$。可以看到，极大似然估计量的解只通过 $\sum_n\mathbf u(\mathbf x_n)$ 依赖于数据，因此这个量称为分布 (3.138) 的**充分统计量**（sufficient statistic）。我们无需保存整个数据集，只需保存充分统计量的值。例如，伯努利分布的 $u(x)$ 就是 $x$，因此只需保留数据点 $\{x_n\}$ 之和；高斯分布的 $\mathbf u(x)=(x,x^2)^{\mathsf T}$，所以要同时保留 $\{x_n\}$ 之和与 $\{x_n^2\}$ 之和。

考虑极限 $N\to\infty$，式 (3.174) 的右边变为 $\mathbb E[\mathbf u(\mathbf x)]$。与式 (3.172) 比较可知，在这一极限下，$\boldsymbol\eta_{\mathrm{ML}}$ 等于真实值 $\boldsymbol\eta$。

## 3.5 非参数方法

本章到目前为止，主要使用由少量参数控制特定函数形式的概率分布，并从数据集确定这些参数的值。这称为密度建模的**参数化方法**。它的一个重要局限是：所选密度可能无法很好地描述产生数据的分布，从而导致较差的预测表现。例如，如果数据生成过程具有多个众数，必然只有单个众数的高斯分布便永远无法捕捉这一特征。在本章最后一节，我们讨论一些对分布形式只作少量假设的非参数密度估计方法。

### 3.5.1 直方图

先讨论用直方图估计密度的方法。我们在图 2.5 的边缘分布和条件分布中，以及图 3.2 的中心极限定理中，已经见过直方图。这里更详细地探讨直方图密度模型的性质，着重考虑只有一个连续变量 $x$ 的情况。标准直方图把 $x$ 划分为宽度为 $\Delta_i$、互不重叠的区间，然后统计落入

<!-- pdf-page: 118 -->

<!-- join-previous-paragraph -->

第 $i$ 个区间的观测值个数 $n_i$。为了将计数转为归一化的概率密度，只需除以观测总数 $N$ 和该区间宽度 $\Delta_i$，便得到每个区间的密度值：

$$
p_i=\frac{n_i}{N\Delta_i}.\tag{3.175}
$$

<figure id="fig-3-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-13.png" alt="同一组 50 个数据点的三幅直方图密度估计，区间宽度依次为 0.04、0.08 和 0.25，绿色曲线为生成数据的真实分布">
  <figcaption>图 3.13：直方图密度估计示例。50 个数据点来自绿色曲线所示的分布。图中展示了根据式 (3.175) 得到的直方图密度估计，三个直方图分别采用不同的公共区间宽度 $\Delta$。</figcaption>
</figure>

容易看出，它满足 $\int p(x)\,\mathrm dx=1$。这得到一个在各区间内部取常数值的密度模型 $p(x)$。通常各区间取相同宽度 $\Delta_i=\Delta$。

图 3.13 给出了直方图密度估计的例子。数据来自绿色曲线对应的分布，该分布由两个高斯分布混合而成。图中还给出了区间宽度 $\Delta$ 的三种选择所对应的估计。当 $\Delta$ 很小（上图）时，得到的密度模型非常尖锐，其中有大量数据生成分布并不具有的结构。反之，如果 $\Delta$ 太大（下图），模型会过于平滑，无法表现绿色曲线的双峰特征。在中间某个 $\Delta$ 值（中图）下，效果最好。原则上，直方图密度模型还依赖区间边界的位置，不过其影响通常远小于区间宽度 $\Delta$。

注意，与稍后讨论的方法不同，直方图算出后可以丢弃原始数据集；当数据集很大时，这是一个优点。而且，数据点逐个到来时，直方图方法也很容易应用。

在实践中，直方图有助于快速可视化一维或二维数据，但不适合大多数密度估计应用。一个明显问题是：估计密度在区间边界处不连续，而这种不连续来自人为划分的边界，并非数据生成分布本身的性质。直方图方法还有一个主要局限，即它随维度增长的扩展性差。如果将 $D$ 维空间的每个变量划分为

<!-- pdf-page: 119 -->

$M$ 个区间，区间总数就是 $M^D$。这种随 $D$ 指数增长的现象是**维度灾难**的一个例子（见第 6.1.1 节）。在高维空间中，要获得有意义的局部概率密度估计，所需的数据量会大得难以承受。

不过，直方图密度估计给了我们两点重要启示。第一，估计某个位置的概率密度时，应考虑该位置某个局部邻域内的数据点。注意，“局部”的概念要求预先选定某种距离度量；这里我们一直假定为欧几里得距离。对直方图而言，邻域由区间定义，且存在一个描述局部区域空间范围的自然“平滑”参数，即区间宽度。第二，要得到好的结果，平滑参数既不应过大，也不应过小。这让人想起多项式回归中模型复杂度的选择：无论使用多项式次数 $M$，还是正则化参数 $\lambda$，最优值都处于中间，不会太大或太小（见第 1 章）。有了这些认识，下面讨论两种广泛使用的非参数密度估计技术：核估计和最近邻方法。相比简单直方图模型，它们随维度增长的扩展性更好。

### 3.5.2 核密度

假设观测值来自某个未知概率密度 $p(\mathbf x)$，其定义在一个 $D$ 维空间中；这里取欧几里得空间。我们希望估计 $p(\mathbf x)$ 的值。根据前面对局部性的讨论，考虑包含 $\mathbf x$ 的一个小区域 $\mathcal R$。该区域对应的概率质量为

$$
P=\int_{\mathcal R}p(\mathbf x)\,\mathrm d\mathbf x.\tag{3.176}
$$

现在假设从 $p(\mathbf x)$ 中抽取了 $N$ 个观测值，形成一个数据集。每个数据点落在 $\mathcal R$ 内的概率为 $P$，因此区域内的数据点总数 $K$ 服从二项分布（见第 3.1.2 节）：

$$
\operatorname{Bin}(K\mid N,P)=\frac{N!}{K!(N-K)!}P^K(1-P)^{N-K}.\tag{3.177}
$$

由式 (3.11) 可知，落在区域内的数据点比例的均值为 $\mathbb E[K/N]=P$；类似地，由式 (3.12) 可知，围绕这个均值的方差为 $\operatorname{var}[K/N]=P(1-P)/N$。当 $N$ 很大时，该分布会高度集中在均值附近，因此

$$
K\simeq NP.\tag{3.178}
$$

另一方面，如果区域 $\mathcal R$ 足够小，使得区域内的概率密度 $p(\mathbf x)$ 大致恒定，则有

$$
P\simeq p(\mathbf x)V,\tag{3.179}
$$

<!-- pdf-page: 120 -->

其中 $V$ 是 $\mathcal R$ 的体积。结合式 (3.178) 和式 (3.179)，得到密度估计

$$
p(\mathbf x)=\frac K{NV}.\tag{3.180}
$$

注意，式 (3.180) 的有效性依赖两个相互矛盾的假设：一方面，区域 $\mathcal R$ 要足够小，使密度在区域内近似恒定；另一方面，相对于该密度的值，区域又要足够大，使落在其中的数据点数 $K$ 足以让二项分布高度集中。

我们可以用两种方式利用式 (3.180)。可以固定 $K$，由数据确定 $V$，从而得到稍后讨论的 $K$ 最近邻技术；也可以固定 $V$，由数据确定 $K$，从而得到核方法。可以证明，只要 $V$ 随 $N$ 以适当速度缩小，且 $K$ 随 $N$ 以适当速度增大，$K$ 最近邻密度估计量和核密度估计量在 $N\to\infty$ 时都会收敛到真实概率密度（Duda and Hart, 1973）。

先详细讨论核方法。首先，取区域 $\mathcal R$ 为一个小超立方体，其中心位于待估计概率密度的点 $\mathbf x$。为统计其中的数据点数 $K$，定义如下函数会很方便：

$$
k(\mathbf u)=\begin{cases}
1,& |u_i|\leqslant\frac12,\quad i=1,\ldots,D,\\
0,& \text{其他情况},
\end{cases}\tag{3.181}
$$

它表示以原点为中心的单位立方体。函数 $k(\mathbf u)$ 是**核函数**的一个例子，在这里也称为 **Parzen 窗**。由式 (3.181) 可知，若数据点 $\mathbf x_n$ 位于以 $\mathbf x$ 为中心、边长为 $h$ 的立方体内，$k((\mathbf x-\mathbf x_n)/h)$ 就等于 1；否则等于 0。因此，立方体内的数据点总数为

$$
K=\sum_{n=1}^{N}k\!\left(\frac{\mathbf x-\mathbf x_n}{h}\right).\tag{3.182}
$$

将其代入式 (3.180)，得到点 $\mathbf x$ 处的估计密度：

$$
p(\mathbf x)=\frac1N\sum_{n=1}^{N}\frac1{h^D}k\!\left(\frac{\mathbf x-\mathbf x_n}{h}\right).\tag{3.183}
$$

这里用了边长为 $h$ 的 $D$ 维超立方体的体积 $V=h^D$。利用函数 $k(\mathbf u)$ 的对称性，现在可以重新理解这一公式：它不是以 $\mathbf x$ 为中心的单个立方体，而是分别以 $N$ 个数据点 $\mathbf x_n$ 为中心的 $N$ 个立方体的贡献之和。

照目前的形式，核密度估计量 (3.183) 会与直方图方法有同样的问题：存在人为的不连续，在这里出现在立方体边界处。选择更平滑的核函数即可得到更平滑的

<!-- pdf-page: 121 -->

<!-- join-previous-paragraph -->

密度模型。一种常见选择是高斯核，它给出如下核密度模型：

$$
p(\mathbf x)=\frac1N\sum_{n=1}^{N}\frac1{(2\pi h^2)^{D/2}}\exp\!\left\{-\frac{\|\mathbf x-\mathbf x_n\|^2}{2h^2}\right\}.\tag{3.184}
$$

<figure id="fig-3-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-14.png" alt="同一数据集的三幅高斯核密度估计，带宽 h 分别为 0.005、0.07 和 0.2；绿色为真实分布，蓝色为估计密度">
  <figcaption>图 3.14：将核密度模型 (3.184) 应用于图 3.13 用来展示直方图方法的同一数据集。$h$ 是平滑参数；$h$ 太小（上图）时，密度模型噪声很大；$h$ 太大（下图）时，生成数据的底层分布（绿色曲线）的双峰性质被抹平；在中间某个 $h$ 值（中图）下，模型效果最好。</figcaption>
</figure>

其中 $h$ 表示高斯分量的标准差。也就是说，在每个数据点上放置一个高斯分布，将它们对整个数据集的贡献相加，最后除以 $N$，便得到正确归一化的密度。图 3.14 将模型 (3.184) 用于此前展示直方图技术的数据集。符合预期，参数 $h$ 起平滑作用：$h$ 小时对噪声敏感，$h$ 大时会过度平滑。优化 $h$ 同样是模型复杂度问题，类似于为直方图密度估计选择区间宽度，或为曲线拟合选择多项式次数。

在式 (3.183) 中还可以选择任何其他核函数 $k(\mathbf u)$，只要它满足

$$
k(\mathbf u)\geqslant0,\tag{3.185}
$$

$$
\int k(\mathbf u)\,\mathrm d\mathbf u=1,\tag{3.186}
$$

这样所得概率分布才能处处非负，且积分为一。式 (3.183) 所给的一类密度模型称为**核密度估计量**，或 **Parzen 估计量**。它的一大优点是“训练”阶段无须计算，只需存储训练集；但这也是一大缺点，因为估计密度的计算成本会随数据集大小线性增长。

<!-- pdf-page: 122 -->

<figure id="fig-3-15">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-15.png" alt="同一数据集的 K 最近邻密度估计，K 分别为 1、5 和 30；绿色为真实分布，蓝色为估计密度">
  <figcaption>图 3.15：用图 3.13 和图 3.14 的同一数据集展示 $K$ 最近邻密度估计。参数 $K$ 控制平滑程度：$K$ 较小（上图）会得到噪声很大的密度模型；$K$ 较大（下图）则会抹平数据生成分布（绿色曲线）的双峰性质。</figcaption>
</figure>

### 3.5.3 最近邻方法

核密度估计方法的一个难点是：控制核宽度的参数 $h$ 对所有核都固定。在数据密度高的区域，较大的 $h$ 可能造成过度平滑，抹去本可从数据中提取的结构。然而，减小 $h$ 又可能使数据空间中密度较低的区域产生噪声很大的估计。因此，$h$ 的最优选择可能依赖于数据空间中的位置。最近邻密度估计方法就是为解决这个问题而提出的。

回到局部密度估计的一般结果 (3.180)。现在不固定 $V$ 再由数据确定 $K$，而是固定 $K$，利用数据寻找合适的 $V$。具体地，在待估计密度 $p(\mathbf x)$ 的点 $\mathbf x$ 周围画一个小球，并逐渐增大球的半径，直到球内恰好包含 $K$ 个数据点。随后将所得球的体积作为 $V$ 代入式 (3.180)，得到 $p(\mathbf x)$ 的估计。这项技术称为 **$K$ 最近邻**，图 3.15 用图 3.13 和图 3.14 的同一数据集展示了参数 $K$ 的不同选择。可以看到，$K$ 决定了平滑程度，且最优值同样既不会太大也不会太小。注意，$K$ 最近邻方法产生的模型并非真正的密度模型，因为它在整个空间上的积分发散（见习题 3.38）。

最后，我们说明如何把用于密度估计的 $K$ 最近邻技术扩展到分类问题。为此，分别对每个类别应用 $K$ 最近邻密度估计，再使用贝叶斯定理。假设数据集共有 $N$ 个点，其中属于类别 $\mathcal C_k$ 的有 $N_k$ 个，因此 $\sum_kN_k=N$。要对新点 $\mathbf x$ 分类，就以它为中心画一个球，使球内恰好包含 $K$ 个点，而不考虑这些点的类别。假设这个球的体积是 $V$，其中有 $K_k$ 个点来自类别 $\mathcal C_k$。那么，式 (3.180) 给出与

<!-- pdf-page: 123 -->

<!-- join-previous-paragraph -->

各类别对应的密度估计：

$$
p(\mathbf x\mid\mathcal C_k)=\frac{K_k}{N_kV}.\tag{3.187}
$$

<figure id="fig-3-16">
  <img src="books/bishop-deep-learning-2024/assets/chapter-03/fig-3-16.png" alt="K 最近邻分类示意：左图黑色菱形按三个最近的训练点归类；右图绿色边界由不同类别训练点之间连线的垂直平分超平面组成">
  <figcaption>图 3.16：(a) 在 $K$ 最近邻分类器中，新点以黑色菱形表示，按距离最近的 $K$ 个训练数据点的多数类别归类，此处 $K=3$。(b) 在最近邻（$K=1$）分类方法中，得到的决策边界由不同类别的点对之间的垂直平分超平面组成。</figcaption>
</figure>

类似地，无条件密度为

$$
p(\mathbf x)=\frac K{NV},\tag{3.188}
$$

类别先验概率为

$$
p(\mathcal C_k)=\frac{N_k}{N}.\tag{3.189}
$$

利用贝叶斯定理，结合式 (3.187)、(3.188) 和 (3.189)，得到类别归属的后验概率：

$$
p(\mathcal C_k\mid\mathbf x)=\frac{p(\mathbf x\mid\mathcal C_k)p(\mathcal C_k)}{p(\mathbf x)}=\frac{K_k}{K}.\tag{3.190}
$$

将测试点 $\mathbf x$ 分配给后验概率最大的类别，也就是 $K_k/K$ 最大的类别，可以使误分类概率最小。因此，对新点分类时，先找出训练数据集中离它最近的 $K$ 个点，再把它分配给这组点中数量最多的类别。若各类别数量相同，可以随机决定。$K=1$ 的特殊情形称为**最近邻规则**：测试点直接归入训练集中最近的那个点所属的类别。这些概念如图 3.16 所示。

最近邻（$K=1$）分类器有一个有趣的性质：在 $N\to\infty$ 的极限下，它的错误率永远不超过最优分类器可达到的最低错误率的两倍；这里的最优分类器指使用真实类别分布的分类器（Cover and Hart, 1967）。

到目前为止，$K$ 最近邻方法和核密度估计量都要求存储整个训练数据集，因此如果数据集很大，计算成本就会很高。

<!-- pdf-page: 124 -->

可以花费一定的一次性额外计算成本，构建树形搜索结构，从而无须穷尽搜索整个数据集，就能高效找到（近似）最近邻，以抵消这一影响。尽管如此，这些非参数方法仍然受到严重限制。另一方面，我们也看到简单参数模型在可表示的分布形式上非常受限。因此，需要一种既很灵活、又能独立于训练集大小控制模型复杂度的密度模型；深度神经网络可以做到这一点。

## 习题

**3.1（★）** 验证伯努利分布 (3.2) 满足以下性质：

$$
\sum_{x=0}^{1}p(x\mid\mu)=1,\tag{3.191}
$$

$$
\mathbb E[x]=\mu,\tag{3.192}
$$

$$
\operatorname{var}[x]=\mu(1-\mu).\tag{3.193}
$$

证明服从伯努利分布的二元随机变量 $x$ 的熵 $H[x]$ 为

$$
H[x]=-\mu\ln\mu-(1-\mu)\ln(1-\mu).\tag{3.194}
$$

**3.2（★★）** 式 (3.2) 给出的伯努利分布在 $x$ 的两个取值之间并不对称。在某些情况下，使用一种等价表述会更方便，其中 $x\in\{-1,1\}$；此时分布可写为

$$
p(x\mid\mu)=\left(\frac{1-\mu}{2}\right)^{(1-x)/2}\left(\frac{1+\mu}{2}\right)^{(1+x)/2},\tag{3.195}
$$

其中 $\mu\in[-1,1]$。证明分布 (3.195) 已归一化，并求出它的均值、方差和熵。

**3.3（★★）** 本题证明二项分布 (3.9) 已归一化。首先，利用式 (3.10) 中从总共 $N$ 个对象里选出 $m$ 个相同对象的组合数定义，证明

$$
\binom Nm+\binom N{m-1}=\binom{N+1}m.\tag{3.196}
$$

再利用该结果，通过归纳法证明

$$
(1+x)^N=\sum_{m=0}^{N}\binom Nm x^m,\tag{3.197}
$$

<!-- pdf-page: 125 -->

这就是**二项式定理**，它对 $x$ 的所有实数值都成立。最后证明二项分布已归一化，即

$$
\sum_{m=0}^{N}\binom Nm\mu^m(1-\mu)^{N-m}=1.\tag{3.198}
$$

可以先把因子 $(1-\mu)^N$ 提到求和号外，再使用二项式定理。

**3.4（★★）** 证明二项分布的均值由式 (3.11) 给出。方法是对归一化条件 (3.198) 两边关于 $\mu$ 求导，然后整理，得到 $n$ 的均值表达式。类似地，对式 (3.198) 关于 $\mu$ 求二阶导数，并利用二项分布均值的结果 (3.11)，证明方差满足式 (3.12)。

译注：原题的“$n$ 的均值”按二项分布变量及式 (3.11) 应为“$m$ 的均值”。

**3.5（★）** 证明多元高斯分布 (3.26) 的众数是 $\boldsymbol\mu$。

**3.6（★★）** 假设 $\mathbf x$ 服从均值为 $\boldsymbol\mu$、协方差为 $\boldsymbol\Sigma$ 的高斯分布。证明线性变换后的变量 $\mathbf A\mathbf x+\mathbf b$ 也服从高斯分布，并求出其均值和协方差。

**3.7（★★★）** 证明两个高斯分布 $q(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu_q,\boldsymbol\Sigma_q)$ 与 $p(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu_p,\boldsymbol\Sigma_p)$ 之间的 Kullback–Leibler 散度为

$$
\begin{aligned}
\operatorname{KL}(q(\mathbf x)\|p(\mathbf x))
=\frac12\bigg\{&\ln\frac{|\boldsymbol\Sigma_p|}{|\boldsymbol\Sigma_q|}-D
+\operatorname{Tr}(\boldsymbol\Sigma_p^{-1}\boldsymbol\Sigma_q)\\
&+(\boldsymbol\mu_p-\boldsymbol\mu_q)^{\mathsf T}\boldsymbol\Sigma_p^{-1}(\boldsymbol\mu_p-\boldsymbol\mu_q)\bigg\},
\end{aligned}\tag{3.199}
$$

其中 $\operatorname{Tr}(\cdot)$ 表示矩阵的迹，$D$ 是 $\mathbf x$ 的维度。

**3.8（★★★）** 本题说明：在协方差给定的条件下，熵最大的多元分布是高斯分布。分布 $p(\mathbf x)$ 的熵为

$$
H[\mathbf x]=-\int p(\mathbf x)\ln p(\mathbf x)\,\mathrm d\mathbf x.\tag{3.200}
$$

我们希望在所有分布 $p(\mathbf x)$ 上最大化 $H[\mathbf x]$，同时要求 $p(\mathbf x)$ 归一化，且具有指定的均值和协方差，即

$$
\int p(\mathbf x)\,\mathrm d\mathbf x=1,\tag{3.201}
$$

$$
\int p(\mathbf x)\mathbf x\,\mathrm d\mathbf x=\boldsymbol\mu,\tag{3.202}
$$

$$
\int p(\mathbf x)(\mathbf x-\boldsymbol\mu)(\mathbf x-\boldsymbol\mu)^{\mathsf T}\,\mathrm d\mathbf x=\boldsymbol\Sigma.\tag{3.203}
$$

对式 (3.200) 作变分最大化，并用拉格朗日乘子施加约束 (3.201)、(3.202) 和 (3.203)，证明所得的极大似然分布由高斯分布 (3.26) 给出。

译注：原题此处写 *maximum likelihood distribution*，但本题要求最大化熵，结论对应的是最大熵分布。

<!-- pdf-page: 126 -->

**3.9（★★★）** 证明多元高斯分布 $\mathcal N(\mathbf x\mid\boldsymbol\mu,\boldsymbol\Sigma)$ 的熵为

$$
H[\mathbf x]=\frac12\ln|\boldsymbol\Sigma|+\frac D2\bigl(1+\ln(2\pi)\bigr),\tag{3.204}
$$

其中 $D$ 是 $\mathbf x$ 的维度。

**3.10（★★★）** 考虑两个随机变量 $x_1$ 和 $x_2$，它们分别服从均值为 $\mu_1,\mu_2$、精度为 $\tau_1,\tau_2$ 的高斯分布。推导变量 $x=x_1+x_2$ 的微分熵表达式。为此，先用关系式

$$
p(x)=\int_{-\infty}^{\infty}p(x\mid x_2)p(x_2)\,\mathrm dx_2\tag{3.205}
$$

并在指数中配方，求出 $x$ 的分布。然后注意到，这代表两个高斯分布的卷积，其结果仍是高斯分布；最后利用式 (2.99) 给出的一元高斯分布的熵。

**3.11（★）** 考虑式 (3.26) 给出的多元高斯分布。把精度矩阵（协方差矩阵的逆）写成对称矩阵与反对称矩阵之和，证明反对称项不出现在高斯分布的指数中，因此不失一般性，可以取精度矩阵为对称矩阵。由于对称矩阵的逆也对称（见习题 3.16），因此协方差矩阵同样可以不失一般性地取为对称矩阵。

**3.12（★★★）** 考虑实对称矩阵 $\boldsymbol\Sigma$，其特征值方程由式 (3.28) 给出。对该方程取复共轭，再减去原方程，随后与特征向量 $\mathbf u_i$ 作内积，证明特征值 $\lambda_i$ 是实数。类似地，利用 $\boldsymbol\Sigma$ 的对称性，证明若 $\lambda_j\ne\lambda_i$，则两个特征向量 $\mathbf u_i$ 和 $\mathbf u_j$ 正交。最后证明，即使某些特征值为零，也总能不失一般性地选取一组正交归一的特征向量，使其满足式 (3.29)。

**3.13（★★）** 证明满足特征向量方程 (3.28) 的实对称矩阵 $\boldsymbol\Sigma$，可以按式 (3.31) 展开为特征向量的线性组合，其系数是特征值。类似地，证明逆矩阵 $\boldsymbol\Sigma^{-1}$ 具有式 (3.32) 的表示。

**3.14（★★）** 正定矩阵 $\boldsymbol\Sigma$ 可以定义为：对向量 $\mathbf a$ 的任意实数取值，二次型

$$
\mathbf a^{\mathsf T}\boldsymbol\Sigma\mathbf a\tag{3.206}
$$

都为正。证明 $\boldsymbol\Sigma$ 为正定矩阵的充要条件是：由式 (3.28) 定义的 $\boldsymbol\Sigma$ 的所有特征值 $\lambda_i$ 都为正。

译注：二次型在 $\mathbf a=\mathbf 0$ 时等于零；正定条件中的“为正”应限定 $\mathbf a$ 为非零向量。

**3.15（★）** 证明一个 $D\times D$ 实对称矩阵有 $D(D+1)/2$ 个独立参数。

<!-- pdf-page: 127 -->

**3.16（★）** 证明对称矩阵的逆矩阵仍然对称。

**3.17（★★）** 利用特征向量展开 (3.31) 对角化坐标系，证明对应恒定马氏距离 $\Delta$ 的超椭球内部体积为

$$
V_D|\boldsymbol\Sigma|^{1/2}\Delta^D,\tag{3.207}
$$

其中 $V_D$ 是 $D$ 维单位球的体积，马氏距离由式 (3.27) 定义。

**3.18（★★）** 用矩阵

$$
\begin{pmatrix}\mathbf A&\mathbf B\\\mathbf C&\mathbf D\end{pmatrix}\tag{3.208}
$$

乘式 (3.60) 两边，并利用定义 (3.61)，证明该恒等式。

**3.19（★★★）** 第 3.2.4 节和第 3.2.5 节讨论了多元高斯分布的条件分布和边缘分布。更一般地，可将 $\mathbf x$ 的分量划分为三组 $\mathbf x_a,\mathbf x_b,\mathbf x_c$，并相应地把均值向量 $\boldsymbol\mu$ 和协方差矩阵 $\boldsymbol\Sigma$ 划分为

$$
\boldsymbol\mu=\begin{pmatrix}\boldsymbol\mu_a\\\boldsymbol\mu_b\\\boldsymbol\mu_c\end{pmatrix},\qquad
\boldsymbol\Sigma=\begin{pmatrix}
\boldsymbol\Sigma_{aa}&\boldsymbol\Sigma_{ab}&\boldsymbol\Sigma_{ac}\\
\boldsymbol\Sigma_{ba}&\boldsymbol\Sigma_{bb}&\boldsymbol\Sigma_{bc}\\
\boldsymbol\Sigma_{ca}&\boldsymbol\Sigma_{cb}&\boldsymbol\Sigma_{cc}
\end{pmatrix}.\tag{3.209}
$$

利用第 3.2 节的结果，求出将 $\mathbf x_c$ 边缘化后的条件分布 $p(\mathbf x_a\mid\mathbf x_b)$ 的表达式。

**3.20（★★）** 线性代数中一个非常有用的结果是 **Woodbury 矩阵求逆公式**：

$$
(\mathbf A+\mathbf B\mathbf C\mathbf D)^{-1}
=\mathbf A^{-1}-\mathbf A^{-1}\mathbf B(\mathbf C^{-1}+\mathbf D\mathbf A^{-1}\mathbf B)^{-1}\mathbf D\mathbf A^{-1}.\tag{3.210}
$$

用 $(\mathbf A+\mathbf B\mathbf C\mathbf D)$ 乘等式两边，证明此公式正确。

**3.21（★）** 令 $\mathbf x$ 和 $\mathbf z$ 为两个独立随机向量，因此 $p(\mathbf x,\mathbf z)=p(\mathbf x)p(\mathbf z)$。证明它们的和 $\mathbf y=\mathbf x+\mathbf z$ 的均值等于各变量均值之和。类似地，证明 $\mathbf y$ 的协方差矩阵等于 $\mathbf x$ 和 $\mathbf z$ 的协方差矩阵之和。

**3.22（★★★）** 考虑变量

$$
\mathbf z=\begin{pmatrix}\mathbf x\\\mathbf y\end{pmatrix}\tag{3.211}
$$

上的联合分布，其均值和协方差分别由式 (3.92) 和式 (3.89) 给出。利用式 (3.76) 和式 (3.77)，证明边缘分布 $p(\mathbf x)$ 由式 (3.83) 给出。类似地，利用式 (3.65) 和式 (3.66)，证明条件分布 $p(\mathbf y\mid\mathbf x)$ 由式 (3.84) 给出。

<!-- pdf-page: 128 -->

**3.23（★★）** 利用分块矩阵求逆公式 (3.60)，证明精度矩阵 (3.88) 的逆由协方差矩阵 (3.89) 给出。

**3.24（★★）** 从式 (3.91) 出发，利用结果 (3.89) 验证式 (3.92)。

**3.25（★★）** 考虑两个多维随机向量 $\mathbf x$ 和 $\mathbf z$，它们分别服从高斯分布 $p(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu_x,\boldsymbol\Sigma_x)$ 与 $p(\mathbf z)=\mathcal N(\mathbf z\mid\boldsymbol\mu_z,\boldsymbol\Sigma_z)$，以及它们的和 $\mathbf y=\mathbf x+\mathbf z$。考虑由边缘分布 $p(\mathbf x)$ 与条件分布 $p(\mathbf y\mid\mathbf x)$ 的乘积构成的线性高斯模型，并利用式 (3.93) 和式 (3.94)，证明 $\mathbf y$ 的边缘分布为

$$
p(\mathbf y)=\mathcal N(\mathbf y\mid\boldsymbol\mu_x+\boldsymbol\mu_z,\boldsymbol\Sigma_x+\boldsymbol\Sigma_z).\tag{3.212}
$$

**3.26（★★★）** 本题和下一题提供了练习线性高斯模型中二次型运算的机会，也可独立核验正文推导的结果。考虑由式 (3.83) 和式 (3.84) 所给边缘分布与条件分布定义的联合分布 $p(\mathbf x,\mathbf y)$。考察联合分布指数中的二次型，并使用第 3.2 节讨论的“配方法”，求出将 $\mathbf x$ 积分消去后，$\mathbf y$ 的边缘分布 $p(\mathbf y)$ 的均值与协方差表达式。为此，请使用 Woodbury 矩阵求逆公式 (3.210)。验证所得结果与式 (3.93) 和式 (3.94) 一致。

**3.27（★★★）** 考虑与习题 3.26 相同的联合分布，这次使用配方法求条件分布 $p(\mathbf x\mid\mathbf y)$ 的均值与协方差表达式。再次验证它们与相应的式 (3.95) 和式 (3.96) 一致。

**3.28（★★）** 为求多元高斯分布协方差矩阵的极大似然解，需要对 $\boldsymbol\Sigma$ 最大化对数似然函数 (3.102)，并注意协方差矩阵必须对称且正定。这里暂时忽略这些约束，直接进行最大化。利用附录 A 的式 (A.21)、(A.26) 和 (A.28)，证明使对数似然函数 (3.102) 最大的协方差矩阵 $\boldsymbol\Sigma$ 由样本协方差 (3.106) 给出。注意，只要样本协方差非奇异，最终结果必然对称且正定。

**3.29（★★）** 利用式 (3.42) 证明式 (3.46)。再利用式 (3.42) 和式 (3.46)，证明

$$
\mathbb E[\mathbf x_n\mathbf x_m^{\mathsf T}]=\boldsymbol\mu\boldsymbol\mu^{\mathsf T}+I_{nm}\boldsymbol\Sigma,\tag{3.213}
$$

其中 $\mathbf x_n$ 是从均值为 $\boldsymbol\mu$、协方差为 $\boldsymbol\Sigma$ 的高斯分布抽取的数据点，$I_{nm}$ 是单位矩阵的第 $(n,m)$ 个元素。进而证明式 (3.108)。

**3.30（★）** 本章讨论周期变量时使用的各个三角恒等式，可以很容易地从关系式

$$
\exp(\mathrm i A)=\cos A+\mathrm i\sin A\tag{3.214}
$$

<!-- pdf-page: 129 -->

推出，其中 $\mathrm i$ 是 $-1$ 的平方根。利用恒等式

$$
\exp(\mathrm i A)\exp(-\mathrm i A)=1\tag{3.215}
$$

证明式 (3.127)。类似地，利用恒等式

$$
\cos(A-B)=\Re\exp\{\mathrm i(A-B)\},\tag{3.216}
$$

其中 $\Re$ 表示实部，证明式 (3.128)。最后，利用 $\sin(A-B)=\Im\exp\{\mathrm i(A-B)\}$（其中 $\Im$ 表示虚部），证明式 (3.133)。

**3.31（★★）** 当 $m$ 很大时，冯·米塞斯分布 (3.129) 会高度集中在众数 $\theta_0$ 附近。定义 $\xi=m^{1/2}(\theta-\theta_0)$，并使用余弦函数的泰勒展开

$$
\cos\alpha=1-\frac{\alpha^2}{2}+O(\alpha^4),\tag{3.217}
$$

证明 $m\to\infty$ 时，冯·米塞斯分布趋近于高斯分布。

**3.32（★）** 利用三角恒等式 (3.133)，证明式 (3.132) 关于 $\theta_0$ 的解由式 (3.134) 给出。

**3.33（★）** 计算冯·米塞斯分布 (3.129) 的一阶和二阶导数，并利用当 $m>0$ 时 $I_0(m)>0$，证明分布在 $\theta=\theta_0$ 处取得最大值，在 $\theta=\theta_0+\pi\pmod{2\pi}$ 处取得最小值。

**3.34（★）** 利用式 (3.118)、式 (3.134) 和三角恒等式 (3.128)，证明冯·米塞斯分布集中度参数的极大似然解 $m_{\mathrm{ML}}$ 满足 $A(m_{\mathrm{ML}})=\bar r$。这里 $\bar r$ 是把观测视为二维欧几里得平面上的单位向量后，其平均向量的长度，如图 3.9 所示。

**3.35（★）** 验证多元高斯分布可以写成指数族形式 (3.138)，并推导与式 (3.164) 至式 (3.167) 类似的 $\boldsymbol\eta$、$\mathbf u(\mathbf x)$、$h(\mathbf x)$ 和 $g(\boldsymbol\eta)$ 的表达式。

**3.36（★）** 式 (3.172) 表明，指数族的 $\ln g(\boldsymbol\eta)$ 的负梯度等于 $\mathbf u(\mathbf x)$ 的期望。对式 (3.139) 求二阶导数，证明

$$
-\nabla\nabla\ln g(\boldsymbol\eta)
=\mathbb E[\mathbf u(\mathbf x)\mathbf u(\mathbf x)^{\mathsf T}]
-\mathbb E[\mathbf u(\mathbf x)]\mathbb E[\mathbf u(\mathbf x)^{\mathsf T}]
=\operatorname{cov}[\mathbf u(\mathbf x)].\tag{3.218}
$$

**3.37（★★）** 考虑一个类似直方图的密度模型：将 $\mathbf x$ 所在空间划分为固定区域，并使密度 $p(\mathbf x)$ 在第 $i$ 个区域内取常数值 $h_i$。第 $i$ 个区域的体积记为 $\Delta_i$。假设有 $N$ 个 $\mathbf x$ 的观测，其中 $n_i$ 个落在区域 $i$ 内。使用拉格朗日乘子施加密度归一化约束，推导 $\{h_i\}$ 的极大似然估计量表达式。

**3.38（★）** 证明 $K$ 最近邻密度模型定义了一个不正规的分布，其在整个空间上的积分发散。
