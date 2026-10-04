# 第 3 章 用于回归的线性模型

<aside class="chapter-guide"><strong>本章导读</strong><p>本章从基函数的线性组合出发，说明最小二乘、最大似然和正则化之间的关系，并用偏差与方差分析模型的预测表现。随后引入贝叶斯线性回归、模型证据和模型比较，讨论如何根据数据控制模型复杂度，以及固定基函数方法的局限。</p></aside>

<!-- pdf-page: 157 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-chapter-opening.png" alt="第 3 章章首装饰图：水面反光纹理"><p class="figure-translation">Linear Models for Regression → 用于回归的线性模型。</p></figure>

到目前为止，本书主要讨论无监督学习，包括密度估计、数据聚类等主题。现在转向监督学习，先从回归开始。回归的目标是：给定由输入变量组成的 $D$ 维向量 $\mathbf{x}$，预测一个或多个连续目标变量 $\mathbf{t}$ 的值。在第 1 章讨论多项式曲线拟合时，我们已经遇到过一个回归问题。多项式是一大类函数中的一个具体例子，这类函数称为线性回归模型；它们的共同性质是，都是可调参数的线性函数，本章将重点讨论这类模型。最简单的线性回归模型也是输入变量的线性函数。不过，把输入变量的一组固定非线性函数（称为基函数，basis function）作线性组合，就能得到一类用途广泛得多的函数。这些模型是参数的线性函数，因此具有简单的解析性质，同时又可以是输入变量的非线性函数。

<!-- pdf-page: 158 -->

给定由 $N$ 个观测 $\{\mathbf{x}_n\}$（其中 $n=1,\ldots,N$）及相应目标值 $\{t_n\}$ 组成的训练数据集，我们的目标是，对于一个新的 $\mathbf{x}$ 值预测 $t$ 的值。最简单的做法是直接构造合适的函数 $y(\mathbf{x})$，以它在新输入 $\mathbf{x}$ 处的函数值，作为相应目标值 $t$ 的预测。更一般地，从概率的角度，我们希望对预测分布 $p(t\mid\mathbf{x})$ 建模，因为它表达了对于每个 $\mathbf{x}$ 值，我们对 $t$ 的值有多大不确定性。利用这个条件分布，可以对任意新的 $\mathbf{x}$ 值预测 $t$，使适当选择的损失函数的期望最小。如第 1.5.5 节所述，对于实值变量，常用的损失函数是平方损失，对应的最优解由 $t$ 的条件期望给出。

作为实际的模式识别方法，线性模型有明显局限，对于涉及高维输入空间的问题尤其如此。不过，它们具有良好的解析性质，也是后续章节中更复杂模型的基础。

## 3.1 线性基函数模型

最简单的回归线性模型，是对输入变量作线性组合：

$$
y(\mathbf{x},\mathbf{w})=w_0+w_1x_1+\ldots+w_Dx_D
\tag{3.1}
$$

其中，$\mathbf{x}=(x_1,\ldots,x_D)^{\mathrm T}$。这通常就称为线性回归（linear regression）。这个模型的关键性质是，它是参数 $w_0,\ldots,w_D$ 的线性函数。但是，它同时也是输入变量 $x_i$ 的线性函数，这给模型带来了很大的限制。因此，我们考虑对输入变量的固定非线性函数作线性组合，从而扩展这类模型，得到如下形式：

$$
y(\mathbf{x},\mathbf{w})=w_0+\sum_{j=1}^{M-1}w_j\phi_j(\mathbf{x})
\tag{3.2}
$$

其中，$\phi_j(\mathbf{x})$ 称为基函数。将索引 $j$ 的最大值记为 $M-1$，则模型中的参数总数为 $M$。

参数 $w_0$ 用于表示数据中的固定偏移，有时称为偏置参数（bias parameter，不要与统计意义上的“偏差”混淆）。通常，为方便起见，可以额外定义一个形式上的“基函数” $\phi_0(\mathbf{x})=1$，于是

$$
y(\mathbf{x},\mathbf{w})=\sum_{j=0}^{M-1}w_j\phi_j(\mathbf{x})=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{3.3}
$$

其中，$\mathbf{w}=(w_0,\ldots,w_{M-1})^{\mathrm T}$，$\boldsymbol{\phi}=(\phi_0,\ldots,\phi_{M-1})^{\mathrm T}$。在许多实际的模式识别应用中，我们会对原始数据变量进行某种固定的预处理

<!-- pdf-page: 159 -->
<!-- join-previous-paragraph -->
或特征提取。如果原始变量组成向量 $\mathbf{x}$，那么这些特征就可以用基函数 $\{\phi_j(\mathbf{x})\}$ 表示。

采用非线性基函数后，函数 $y(\mathbf{x},\mathbf{w})$ 就可以是输入向量 $\mathbf{x}$ 的非线性函数。不过，形式为式（3.2）的函数仍称为线性模型，因为它对于 $\mathbf{w}$ 是线性的。正是这种对参数的线性关系，大幅简化了对这类模型的分析。但它也带来了一些明显的局限，我们将在第 3.6 节讨论。

第 1 章中的多项式回归，是这个模型的一个特例：只有一个输入变量 $x$，基函数取 $x$ 的各次幂，即 $\phi_j(x)=x^j$。多项式基函数有一个局限：它们是输入变量的全局函数，因此，输入空间中一个区域的变化会影响其他所有区域。可以把输入空间划分成若干区域，并在每个区域拟合不同的多项式来解决这个问题，由此得到样条函数（spline function）（Hastie et al., 2001）。

基函数还有许多其他选择，例如

$$
\phi_j(x)=\exp\left\{-\frac{(x-\mu_j)^2}{2s^2}\right\}
\tag{3.4}
$$

其中，$\mu_j$ 控制各基函数在输入空间中的位置，参数 $s$ 控制它们的空间尺度。这些基函数通常称为“高斯”基函数，不过，并不要求它们具有概率解释；尤其是，归一化系数并不重要，因为这些基函数还要乘以可调参数 $w_j$。

另一种选择是如下形式的 sigmoid 基函数：

$$
\phi_j(x)=\sigma\left(\frac{x-\mu_j}{s}\right)
\tag{3.5}
$$

其中，$\sigma(a)$ 是 logistic sigmoid 函数，定义为

$$
\sigma(a)=\frac{1}{1+\exp(-a)}.
\tag{3.6}
$$

等价地，也可以使用“tanh”函数，因为它与 logistic sigmoid 的关系为 $\tanh(a)=2\sigma(a)-1$，所以，logistic sigmoid 函数的一般线性组合，等价于“tanh”函数的一般线性组合。图 3.1 展示了这些不同的基函数选择。

另一种可能的基函数选择是傅里叶基，它对应于正弦函数展开。每个基函数表示一个特定频率，并在空间上无限延伸。相比之下，局限在输入空间有限区域内的基函数，必然包含由不同空间频率组成的频谱。在许多信号处理应用中，人们希望采用在空间和频率上都局部化的基函数，由此得到一类称为小波（wavelet）的函数。为简化应用，小波还被定义为彼此正交。当输入值位于

<!-- pdf-page: 160 -->
<!-- join-previous-paragraph -->
规则网格上时，小波最为适用，例如时间序列中连续的时间点，或者图像中的像素。介绍小波的实用参考书包括 Ogden（1997）、Mallat（1999）和 Vidakovic（1999）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-1.png" alt="多项式、高斯和 sigmoid 三类基函数的示例"><figcaption>图 3.1：基函数示例。左图为多项式，中图为式（3.4）所示的高斯函数，右图为式（3.5）所示的 sigmoid 函数。</figcaption></figure>

不过，本章的大多数讨论并不依赖于具体选择哪组基函数。因此，除用于数值示例外，我们在大多数讨论中都不会指定基函数的具体形式。事实上，许多讨论同样适用于基函数向量 $\boldsymbol{\phi}(\mathbf{x})$ 就是恒等映射 $\boldsymbol{\phi}(\mathbf{x})=\mathbf{x}$ 的情形。另外，为使记号简洁，我们将主要讨论单个目标变量 $t$ 的情况。在第 3.1.5 节中，我们会简要说明，处理多个目标变量时需要作哪些修改。

### 3.1.1 最大似然与最小二乘

在第 1 章中，我们通过最小化平方和误差函数，把多项式函数拟合到数据集。我们还说明，在假设高斯噪声模型的条件下，这个误差函数可以由最大似然解导出。现在回到这个话题，更详细地讨论最小二乘方法及其与最大似然的关系。

与前面一样，假设目标变量 $t$ 由确定性函数 $y(\mathbf{x},\mathbf{w})$ 加上高斯噪声给出，即

$$
t=y(\mathbf{x},\mathbf{w})+\epsilon
\tag{3.7}
$$

其中，$\epsilon$ 是均值为零、精度（方差的倒数）为 $\beta$ 的高斯随机变量。因此，可以写成

$$
p(t\mid\mathbf{x},\mathbf{w},\beta)=\mathcal{N}(t\mid y(\mathbf{x},\mathbf{w}),\beta^{-1}).
\tag{3.8}
$$

回顾前面，如果采用平方损失函数，那么对一个新的 $\mathbf{x}$ 值，最优预测由目标变量的条件均值给出。<span class="margin-reference">第 1.5.5 节</span> 对于形式为式（3.8）的高斯条件分布，条件均值

<!-- pdf-page: 161 -->
<!-- join-previous-paragraph -->
就是

$$
\mathbb{E}[t\mid\mathbf{x}]=\int tp(t\mid\mathbf{x})\,\mathrm{d}t=y(\mathbf{x},\mathbf{w}).
\tag{3.9}
$$

注意，高斯噪声假设意味着，给定 $\mathbf{x}$ 时 $t$ 的条件分布是单峰的；这对某些应用可能并不合适。第 14.5.1 节将讨论如何扩展为条件高斯分布的混合，从而允许条件分布具有多个峰。

现在考虑一个输入数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，对应的目标值为 $t_1,\ldots,t_N$。把目标变量 $\{t_n\}$ 组成一个列向量，记为 $\boldsymbol{\mathsf{t}}$；这里特意选择了不同的字体，以便与多元目标的一次观测相区分，后者记为 $\mathbf{t}$。假设这些数据点独立地取自分布（3.8），则以可调参数 $\mathbf{w}$ 和 $\beta$ 为自变量的似然函数为

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)=\prod_{n=1}^{N}\mathcal{N}(t_n\mid\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\beta^{-1})
\tag{3.10}
$$

其中使用了式（3.3）。注意，对于回归（以及分类）这类监督学习问题，我们并不试图对输入变量的分布建模。因此，$\mathbf{x}$ 总是出现在条件变量中；为了使记号简洁，从现在起，对于 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{x},\mathbf{w},\beta)$ 这样的表达式，我们将不再显式写出 $\mathbf{x}$。对似然函数取对数，并利用一元高斯分布的标准形式（1.46），得到

$$
\begin{aligned}
\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)&=\sum_{n=1}^{N}\ln\mathcal{N}(t_n\mid\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\beta^{-1})\\
&=\frac{N}{2}\ln\beta-\frac{N}{2}\ln(2\pi)-\beta E_D(\mathbf{w})
\end{aligned}
\tag{3.11}
$$

其中，平方和误差函数定义为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2.
\tag{3.12}
$$

写出似然函数后，就可以用最大似然来确定 $\mathbf{w}$ 和 $\beta$。先考虑对 $\mathbf{w}$ 最大化。正如第 1.2.5 节已经指出的，在条件高斯噪声分布下，线性模型的似然最大化，等价于最小化平方和误差函数 $E_D(\mathbf{w})$。对数似然函数（3.11）的梯度为

$$
\nabla\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)=\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}.
\tag{3.13}
$$

<!-- pdf-page: 162 -->

令这个梯度等于零，得到

$$
0=\sum_{n=1}^{N}t_n\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}-\mathbf{w}^{\mathrm T}\left(\sum_{n=1}^{N}\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}\right).
\tag{3.14}
$$

解出 $\mathbf{w}$，得到

$$
\mathbf{w}_{\mathrm{ML}}=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{3.15}
$$

这称为最小二乘问题的正规方程（normal equation）。这里，$\boldsymbol{\Phi}$ 是一个 $N\times M$ 矩阵，称为设计矩阵（design matrix），其元素为 $\Phi_{nj}=\phi_j(\mathbf{x}_n)$，即

$$
\boldsymbol{\Phi}=\begin{pmatrix}
\phi_0(\mathbf{x}_1)&\phi_1(\mathbf{x}_1)&\cdots&\phi_{M-1}(\mathbf{x}_1)\\
\phi_0(\mathbf{x}_2)&\phi_1(\mathbf{x}_2)&\cdots&\phi_{M-1}(\mathbf{x}_2)\\
\vdots&\vdots&\ddots&\vdots\\
\phi_0(\mathbf{x}_N)&\phi_1(\mathbf{x}_N)&\cdots&\phi_{M-1}(\mathbf{x}_N)
\end{pmatrix}.
\tag{3.16}
$$

量

$$
\boldsymbol{\Phi}^{\dagger}\equiv(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}
\tag{3.17}
$$

称为矩阵 $\boldsymbol{\Phi}$ 的 Moore–Penrose 伪逆（pseudo-inverse）（Rao and Mitra, 1971；Golub and Van Loan, 1996）。可以把它看作矩阵求逆概念向非方阵的推广。事实上，如果 $\boldsymbol{\Phi}$ 是可逆方阵，利用性质 $(\mathbf{A}\mathbf{B})^{-1}=\mathbf{B}^{-1}\mathbf{A}^{-1}$，就有 $\boldsymbol{\Phi}^{\dagger}\equiv\boldsymbol{\Phi}^{-1}$。

现在可以进一步理解偏置参数 $w_0$ 的作用。显式写出偏置参数后，误差函数（3.12）变为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\left\{t_n-w_0-\sum_{j=1}^{M-1}w_j\phi_j(\mathbf{x}_n)\right\}^2.
\tag{3.18}
$$

令其对 $w_0$ 的导数等于零，并解出 $w_0$，得到

$$
w_0=\overline{t}-\sum_{j=1}^{M-1}w_j\overline{\phi_j}
\tag{3.19}
$$

其中定义

$$
\overline{t}=\frac{1}{N}\sum_{n=1}^{N}t_n,\qquad \overline{\phi_j}=\frac{1}{N}\sum_{n=1}^{N}\phi_j(\mathbf{x}_n).
\tag{3.20}
$$

因此，偏置 $w_0$ 补偿的是：目标值在训练集上的平均值，与各基函数值在训练集上平均值的加权和之间的差。

也可以对噪声精度参数 $\beta$ 最大化对数似然函数（3.11），得到

$$
\frac{1}{\beta_{\mathrm{ML}}}=\frac{1}{N}\sum_{n=1}^{N}\{t_n-\mathbf{w}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2
\tag{3.21}
$$

<!-- pdf-page: 163 -->

由此可见，噪声精度的倒数，等于目标值相对于回归函数的残差方差。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-2.png" alt="数据向量向基函数张成子空间的正交投影"><figcaption>图 3.2：最小二乘解的几何解释。所在空间有 $N$ 个维度，其各坐标轴对应 $t_1,\ldots,t_N$ 的取值。最小二乘回归函数通过以下方式得到：把数据向量 $\boldsymbol{\mathsf{t}}$ 正交投影到基函数 $\phi_j(\mathbf{x})$ 张成的子空间；这里，每个基函数都被看成一个长度为 $N$ 的向量 $\boldsymbol{\varphi}_j$，其元素为 $\phi_j(\mathbf{x}_n)$。</figcaption></figure>

### 3.1.2 最小二乘的几何解释

此时，考察最小二乘解的几何解释很有帮助。为此，考虑一个 $N$ 维空间，各坐标轴由 $t_n$ 给出，因此 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$ 是这个空间中的一个向量。每个基函数 $\phi_j(\mathbf{x}_n)$ 在 $N$ 个数据点上的取值，也可以表示为同一空间中的向量，记为 $\boldsymbol{\varphi}_j$，如图 3.2 所示。注意，$\boldsymbol{\varphi}_j$ 对应于 $\boldsymbol{\Phi}$ 的第 $j$ 列，而 $\boldsymbol{\phi}(\mathbf{x}_n)$ 对应于 $\boldsymbol{\Phi}$ 的第 $n$ 行。如果基函数数目 $M$ 小于数据点数目 $N$，那么这 $M$ 个向量 $\phi_j(\mathbf{x}_n)$ 就张成一个维数为 $M$ 的线性子空间 $\mathcal{S}$。定义 $\boldsymbol{\mathsf{y}}$ 为一个 $N$ 维向量，其第 $n$ 个元素为 $y(\mathbf{x}_n,\mathbf{w})$，其中 $n=1,\ldots,N$。由于 $\boldsymbol{\mathsf{y}}$ 是向量 $\boldsymbol{\varphi}_j$ 的任意线性组合，它可以位于这个 $M$ 维子空间中的任意位置。此时，平方和误差（3.12）等于 $\boldsymbol{\mathsf{y}}$ 与 $\boldsymbol{\mathsf{t}}$ 之间的欧氏距离平方，再乘以因子 $1/2$。因此，$\mathbf{w}$ 的最小二乘解对应于这样的 $\boldsymbol{\mathsf{y}}$：它位于子空间 $\mathcal{S}$ 中，并且距离 $\boldsymbol{\mathsf{t}}$ 最近。从图 3.2 可以直观地推测，这个解就是 $\boldsymbol{\mathsf{t}}$ 在子空间 $\mathcal{S}$ 上的正交投影。事实也确实如此：注意到 $\boldsymbol{\mathsf{y}}$ 的解由 $\boldsymbol{\Phi}\mathbf{w}_{\mathrm{ML}}$ 给出，再验证它具有正交投影的形式，就很容易确认这一点。<span class="margin-reference">习题 3.2</span>

在实践中，当 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 接近奇异时，直接求解正规方程可能遇到数值困难。特别是，当两个或多个基向量 $\boldsymbol{\varphi}_j$ 共线或接近共线时，得到的参数值可能很大。处理真实数据集时，这种近乎退化的情况并不少见。可以用奇异值分解（singular value decomposition，SVD）来处理由此产生的数值困难（Press et al., 1992；Bishop and Nabney, 2008）。注意，即使存在退化，加入正则化项也能保证矩阵非奇异。

### 3.1.3 序贯学习

像最大似然解（3.15）这样的批量方法，需要一次处理整个训练集；对于大型数据集，计算开销可能很高。正如第 1 章所讨论的，如果数据集足够大，采用序贯算法（也称在线算法，on-line algorithm）可能更合适，

<!-- pdf-page: 164 -->
<!-- join-previous-paragraph -->
这类算法每次处理一个数据点，并在每次输入数据点后更新模型参数。序贯学习也适合实时应用：观测数据不断到来，而在看到全部数据点之前，就必须作出预测。

可以采用随机梯度下降（stochastic gradient descent），也称序贯梯度下降（sequential gradient descent），得到如下的序贯学习算法。如果误差函数是各数据点对应误差的和，即 $E=\sum_n E_n$，那么在输入第 $n$ 个模式后，随机梯度下降算法按下式更新参数向量 $\mathbf{w}$：

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta\nabla E_n
\tag{3.22}
$$

其中，$\tau$ 表示迭代次数，$\eta$ 是学习率参数。我们马上会讨论如何选择 $\eta$ 的值。将 $\mathbf{w}$ 初始化为某个起始向量 $\mathbf{w}^{(0)}$。对于平方和误差函数（3.12），得到

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}+\eta(t_n-\mathbf{w}^{(\tau){\mathrm T}}\boldsymbol{\phi}_n)\boldsymbol{\phi}_n
\tag{3.23}
$$

其中，$\boldsymbol{\phi}_n=\boldsymbol{\phi}(\mathbf{x}_n)$。这称为最小均方（least-mean-squares，LMS）算法。需要谨慎选择 $\eta$ 的值，以保证算法收敛（Bishop and Nabney, 2008）。

### 3.1.4 正则化最小二乘

在第 1.1 节中，我们介绍了通过在误差函数中加入正则化项来控制过拟合的思路，于是，需要最小化的总误差函数为

$$
E_D(\mathbf{w})+\lambda E_W(\mathbf{w})
\tag{3.24}
$$

其中，$\lambda$ 是正则化系数，它控制依赖数据的误差 $E_D(\mathbf{w})$ 与正则化项 $E_W(\mathbf{w})$ 的相对重要程度。最简单的一种正则化项，是权重向量各元素的平方和：

$$
E_W(\mathbf{w})=\frac{1}{2}\mathbf{w}^{\mathrm T}\mathbf{w}.
\tag{3.25}
$$

如果同时采用如下的平方和误差函数

$$
E(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2
\tag{3.26}
$$

那么，总误差函数变为

$$
\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2+\frac{\lambda}{2}\mathbf{w}^{\mathrm T}\mathbf{w}.
\tag{3.27}
$$

在机器学习文献中，这种特定的正则化项称为权重衰减（weight decay），因为在序贯学习算法中，除非数据提供支持，否则它会促使权重值向零衰减。在统计学中，它属于参数收缩（parameter shrinkage）方法，因为它使参数值向

<!-- pdf-page: 165 -->
<!-- join-previous-paragraph -->
零收缩。它的一个优点是，误差函数仍然是 $\mathbf{w}$ 的二次函数，因此可以求出使其最小的精确闭式解。具体来说，令式（3.27）对 $\mathbf{w}$ 的梯度等于零，并像前面一样解出 $\mathbf{w}$，得到

$$
\mathbf{w}=(\lambda\mathbf{I}+\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}.
\tag{3.28}
$$

这是对最小二乘解（3.15）的简单扩展。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-3.png" alt="q 分别为 0.5、1、2、4 时正则化项的等值线"><figcaption>图 3.3：参数 $q$ 取不同值时，式（3.29）中正则化项的等值线。</figcaption></figure>

有时会使用更一般的正则化项，对应的正则化误差为

$$
\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2+\frac{\lambda}{2}\sum_{j=1}^{M}|w_j|^q
\tag{3.29}
$$

其中，$q=2$ 对应于式（3.27）中的二次正则化项。图 3.3 给出了不同 $q$ 值对应的正则化函数等值线。

在统计学文献中，$q=1$ 的情形称为 lasso（Tibshirani, 1996）。它具有这样的性质：如果 $\lambda$ 足够大，一些系数 $w_j$ 就会被压到零，从而得到一个稀疏（sparse）模型，对应的基函数在其中不起作用。要理解这一点，首先注意，最小化式（3.29）等价于在以下约束下最小化未正则化的平方和误差（3.12）：<span class="margin-reference">习题 3.5</span>

$$
\sum_{j=1}^{M}|w_j|^q\leqslant\eta
\tag{3.30}
$$

其中参数 $\eta$ 取适当的值；这两种方法可以通过拉格朗日乘子联系起来。<span class="margin-reference">附录 E</span> 图 3.4 展示了误差函数在约束（3.30）下的最小值，从中可以看出稀疏性是如何产生的。随着 $\lambda$ 增大，越来越多的参数被压到零。

正则化主要通过限制有效模型复杂度，使复杂模型可以在有限大小的数据集上训练，而不发生严重的过拟合。不过，确定最优模型复杂度的问题，也由寻找合适的基函数数目，转变为确定正则化系数 $\lambda$ 的合适取值。本章后面将再次讨论模型复杂度问题。

<!-- pdf-page: 166 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-4.png" alt="二次正则化与 lasso 的约束区域及最优解比较"><figcaption>图 3.4：未正则化误差函数的等值线（蓝色）与约束区域（3.30）。左图为二次正则化 $q=2$，右图为 lasso 正则化 $q=1$；参数向量 $\mathbf{w}$ 的最优值记为 $\mathbf{w}^{\star}$。lasso 得到一个稀疏解，其中 $w_1^{\star}=0$。</figcaption></figure>

考虑到二次正则化项（3.27）的实际重要性和便于解析处理的性质，本章余下部分将主要讨论这一形式。

### 3.1.5 多输出

到目前为止，我们考虑的都是单个目标变量 $t$。在某些应用中，可能希望预测 $K>1$ 个目标变量，把它们合起来记为目标向量 $\mathbf{t}$。一种方法是，对 $\mathbf{t}$ 的每个分量引入不同的一组基函数，从而得到多个相互独立的回归问题。不过，一种更有意思、也更常见的方法，是使用同一组基函数，对目标向量的所有分量建模，即

$$
\mathbf{y}(\mathbf{x},\mathbf{w})=\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{3.31}
$$

其中，$\mathbf{y}$ 是一个 $K$ 维列向量，$\mathbf{W}$ 是一个 $M\times K$ 参数矩阵，$\boldsymbol{\phi}(\mathbf{x})$ 是一个 $M$ 维列向量，其元素为 $\phi_j(\mathbf{x})$，并且与前面一样，$\phi_0(\mathbf{x})=1$。假设目标向量的条件分布为各向同性高斯分布：

$$
p(\mathbf{t}\mid\mathbf{x},\mathbf{W},\beta)=\mathcal{N}(\mathbf{t}\mid\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}),\beta^{-1}\mathbf{I}).
\tag{3.32}
$$

若有一组观测 $\mathbf{t}_1,\ldots,\mathbf{t}_N$，可以把它们组成一个大小为 $N\times K$ 的矩阵 $\mathbf{T}$，其第 $n$ 行为 $\mathbf{t}_n^{\mathrm T}$。同样，也可以把输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 组成矩阵 $\mathbf{X}$。于是，对数似然函数为

$$
\begin{aligned}
\ln p(\mathbf{T}\mid\mathbf{X},\mathbf{W},\beta)&=\sum_{n=1}^{N}\ln\mathcal{N}(\mathbf{t}_n\mid\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\beta^{-1}\mathbf{I})\\
&=\frac{NK}{2}\ln\left(\frac{\beta}{2\pi}\right)-\frac{\beta}{2}\sum_{n=1}^{N}\left\|\mathbf{t}_n-\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\|^2.
\end{aligned}
\tag{3.33}
$$

<!-- pdf-page: 167 -->

与前面一样，对 $\mathbf{W}$ 最大化这个函数，得到

$$
\mathbf{W}_{\mathrm{ML}}=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{T}.
\tag{3.34}
$$

分别考察每个目标变量 $t_k$ 的结果，得到

$$
\mathbf{w}_k=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}_k=\boldsymbol{\Phi}^{\dagger}\boldsymbol{\mathsf{t}}_k
\tag{3.35}
$$

其中，$\boldsymbol{\mathsf{t}}_k$ 是一个 $N$ 维列向量，其分量为 $t_{nk}$，$n=1,\ldots,N$。因此，这个回归问题的解在不同目标变量之间是相互独立的；只需计算一个伪逆矩阵 $\boldsymbol{\Phi}^{\dagger}$，供所有向量 $\mathbf{w}_k$ 共用。

推广到具有任意协方差矩阵的一般高斯噪声分布很直接。<span class="margin-reference">习题 3.6</span> 同样，问题会分解为 $K$ 个独立的回归问题。这个结果并不意外，因为参数 $\mathbf{W}$ 只决定高斯噪声分布的均值，而由第 2.3.4 节可知，多元高斯均值的最大似然解与协方差无关。因此，为简便起见，以下仍只考虑单个目标变量 $t$。

## 3.2 偏差—方差分解

到目前为止，在讨论用于回归的线性模型时，我们都假设基函数的形式和数目固定不变。正如第 1 章所示，用有限大小的数据集训练复杂模型时，最大似然方法（也就是最小二乘方法）可能导致严重过拟合。不过，为避免过拟合而限制基函数数目，也会降低模型的灵活性，使其难以捕捉数据中值得关注的重要趋势。虽然引入正则化项可以控制参数众多的模型的过拟合，却又带来了另一个问题：如何确定正则化系数 $\lambda$ 的合适取值。显然，不能同时对权重向量 $\mathbf{w}$ 和正则化系数 $\lambda$ 求解，使正则化误差函数最小，因为这样会得到 $\lambda=0$ 的未正则化解。

正如前几章所见，过拟合实际上是最大似然方法的一个不理想性质；在贝叶斯框架中对参数进行边缘化时，就不会出现这一现象。本章将较深入地讨论模型复杂度的贝叶斯观点。不过，在此之前，先考察一种关于模型复杂度的频率学派观点很有帮助，这就是偏差—方差权衡（bias-variance trade-off）。我们将在易于用简单例子说明的线性基函数模型中介绍这一概念，但这些讨论具有更广泛的适用性。

在第 1.5.5 节讨论回归问题的决策论时，我们考察了不同的损失函数；给定条件分布 $p(t\mid\mathbf{x})$ 后，每一种损失函数都会给出相应的最优预测。一种常见选择是

<!-- pdf-page: 168 -->
<!-- join-previous-paragraph -->
平方损失函数，其最优预测由条件期望给出。将这个条件期望记为 $h(\mathbf{x})$，则

$$
h(\mathbf{x})=\mathbb{E}[t\mid\mathbf{x}]=\int tp(t\mid\mathbf{x})\,\mathrm{d}t.
\tag{3.36}
$$

这里需要区分决策论中的平方损失函数，与模型参数最大似然估计中出现的平方和误差函数。我们可以用比最小二乘更复杂的方法，例如正则化或完整的贝叶斯方法，来确定条件分布 $p(t\mid\mathbf{x})$。这些方法都可以与平方损失函数结合，用于作出预测。

第 1.5.5 节已经说明，平方损失的期望可以写为

$$
\mathbb{E}[L]=\int\{y(\mathbf{x})-h(\mathbf{x})\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}+\int\{h(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t.
\tag{3.37}
$$

回顾前面，第二项与 $y(\mathbf{x})$ 无关，来自数据本身的噪声，表示期望损失所能达到的最小值。第一项取决于函数 $y(\mathbf{x})$ 的选择，我们希望找到使这一项最小的 $y(\mathbf{x})$。由于它非负，能够期待的最小值就是零。如果有无限多的数据（以及无限的计算资源），原则上就可以求得任意所需精度的回归函数 $h(\mathbf{x})$，它就是 $y(\mathbf{x})$ 的最优选择。但在实践中，数据集 $\mathcal{D}$ 只包含有限的 $N$ 个数据点，因此我们并不能精确地知道回归函数 $h(\mathbf{x})$。

如果用由参数向量 $\mathbf{w}$ 控制的参数函数 $y(\mathbf{x},\mathbf{w})$ 对 $h(\mathbf{x})$ 建模，那么，从贝叶斯观点看，模型中的不确定性由 $\mathbf{w}$ 的后验分布表达。而频率学派的处理方式，是根据数据集 $\mathcal{D}$ 对 $\mathbf{w}$ 作点估计，再通过下面的思想实验来解释这一估计的不确定性。假设有大量数据集，每个数据集的大小都是 $N$，并且都是独立地从分布 $p(t,\mathbf{x})$ 中抽取的。对于任何给定的数据集 $\mathcal{D}$，都可以运行学习算法，得到预测函数 $y(\mathbf{x};\mathcal{D})$。这组数据集中的不同数据集会给出不同的函数，进而得到不同的平方损失值。某一学习算法的表现，就通过在这组数据集上取平均来评估。

考虑式（3.37）第一项的被积函数，对于一个特定数据集 $\mathcal{D}$，它为

$$
\{y(\mathbf{x};\mathcal{D})-h(\mathbf{x})\}^2.
\tag{3.38}
$$

由于这个量依赖于具体的数据集 $\mathcal{D}$，我们对这组数据集取平均。如果在花括号内加上并减去 $\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]$

<!-- pdf-page: 169 -->
<!-- join-previous-paragraph -->
这个量，再展开，就得到

$$
\begin{aligned}
&\{y(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]+\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2\\
&\quad=\{y(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]\}^2+\{\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2\\
&\qquad\quad+2\{y(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]\}\{\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}.
\end{aligned}
\tag{3.39}
$$

现在对这个表达式关于 $\mathcal{D}$ 取期望，并注意到最后一项会消失，得到

$$
\begin{aligned}
&\mathbb{E}_{\mathcal{D}}\left[\{y(\mathbf{x};\mathcal{D})-h(\mathbf{x})\}^2\right]\\
&\quad=\underbrace{\{\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2}_{\text{（偏差）}^{2}}+\underbrace{\mathbb{E}_{\mathcal{D}}\left[\{y(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]\}^2\right]}_{\text{方差}}.
\end{aligned}
\tag{3.40}
$$

可见，$y(\mathbf{x};\mathcal{D})$ 与回归函数 $h(\mathbf{x})$ 之差的平方期望，可以表示为两项之和。第一项称为偏差平方，表示在所有数据集上得到的平均预测，与所希望的回归函数相差多大。第二项称为方差，衡量各个数据集得到的解围绕其平均值变化的程度，因此也衡量函数 $y(\mathbf{x};\mathcal{D})$ 对具体数据集选择的敏感程度。稍后讨论一个简单例子时，将为这些定义提供直观解释。

到目前为止，我们考虑的是一个输入值 $\mathbf{x}$。把这个展开式代回式（3.37），就得到平方损失期望的如下分解：

$$
\text{期望损失}=(\text{偏差})^2+\text{方差}+\text{噪声}
\tag{3.41}
$$

其中

$$
(\text{偏差})^2=\int\{\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}
\tag{3.42}
$$

$$
\text{方差}=\int\mathbb{E}_{\mathcal{D}}\left[\{y(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[y(\mathbf{x};\mathcal{D})]\}^2\right]p(\mathbf{x})\,\mathrm{d}\mathbf{x}
\tag{3.43}
$$

$$
\text{噪声}=\int\{h(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t
\tag{3.44}
$$

此时，偏差和方差指的是积分后的量。

我们的目标是最小化期望损失；现在已经把它分解为偏差平方、方差和常数噪声项之和。下面会看到，偏差与方差之间存在权衡：十分灵活的模型偏差小、方差大，而相对受限的模型偏差大、方差小。预测能力最好的模型，就是在偏差和方差之间取得最佳平衡的模型。可以用第 1 章的正弦数据集来说明这一点。这里，我们独立地根据正弦曲线 $h(x)=\sin(2\pi x)$ 生成 100 个数据集，每个包含 $N=25$ 个数据点。<span class="margin-reference">附录 A</span> 用 $l=1,\ldots,L$ 对数据集编号，其中 $L=100$；对于每个数据集 $\mathcal{D}^{(l)}$，我们

<!-- pdf-page: 170 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-5.png" alt="不同正则化强度下多个数据集的拟合曲线和平均拟合曲线"><figcaption>图 3.5：使用第 1 章的正弦数据集，说明偏差和方差如何依赖于由正则化参数 $\lambda$ 控制的模型复杂度。共有 $L=100$ 个数据集，每个包含 $N=25$ 个数据点；模型中有 24 个高斯基函数，加上偏置参数，参数总数为 $M=25$。左列展示 $\ln\lambda$ 取不同值时，把模型拟合到各数据集的结果（为清晰起见，100 条拟合曲线中只画出 20 条）。右列展示相应的 100 条拟合曲线的平均值（红色），以及用于生成数据集的正弦函数（绿色）。</figcaption></figure>

<!-- pdf-page: 171 -->
<!-- join-previous-paragraph-across-figures -->
通过最小化正则化误差函数（3.27），拟合一个含 24 个高斯基函数的模型，得到预测函数 $y^{(l)}(x)$，如图 3.5 所示。最上面一行对应较大的正则化系数 $\lambda$：方差较小（因为左图中的红色曲线彼此相近），但偏差较大（因为右图中的两条曲线相差很大）。相反，最下面一行的 $\lambda$ 较小，方差很大（左图中的红色曲线变化很大），但偏差较小（平均拟合曲线与原始正弦函数很接近）。注意，对于参数数目为 $M=25$ 的复杂模型，把多个解平均后，得到的结果能很好地拟合回归函数，这说明取平均可能有益。事实上，对多个解进行加权平均正是贝叶斯方法的核心，只不过它是对参数的后验分布取平均，而不是对多个数据集取平均。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-6.png" alt="偏差平方、方差、两者之和及测试误差随正则化强度的变化"><figcaption>图 3.6：与图 3.5 结果对应的偏差平方、方差及两者之和。图中还给出了在含 1,000 个点的测试数据集上的平均测试误差。$(\text{偏差})^2+\text{方差}$ 在 $\ln\lambda=-0.31$ 附近达到最小值，这与使测试数据误差最小的取值接近。</figcaption><p class="figure-translation">(bias)² →（偏差）²；variance → 方差；(bias)² + variance →（偏差）² ＋ 方差；test error → 测试误差。</p></figure>

对于这个例子，也可以定量考察偏差—方差权衡。平均预测估计为

$$
\overline{y}(x)=\frac{1}{L}\sum_{l=1}^{L}y^{(l)}(x)
\tag{3.45}
$$

积分后的偏差平方和方差则分别为

$$
(\text{偏差})^2=\frac{1}{N}\sum_{n=1}^{N}\{\overline{y}(x_n)-h(x_n)\}^2
\tag{3.46}
$$

$$
\text{方差}=\frac{1}{N}\sum_{n=1}^{N}\frac{1}{L}\sum_{l=1}^{L}\{y^{(l)}(x_n)-\overline{y}(x_n)\}^2
\tag{3.47}
$$

其中，对 $x$ 按分布 $p(x)$ 加权的积分，用从该分布抽取的有限个数据点上的求和来近似。图 3.6 以 $\ln\lambda$ 为横轴，绘出了这些量及其总和。可见，较小的 $\lambda$ 允许模型细致地适应每个

<!-- pdf-page: 172 -->
<!-- join-previous-paragraph -->
数据集中的噪声，从而导致较大的方差。相反，较大的 $\lambda$ 会把权重参数拉向零，导致较大的偏差。

虽然偏差—方差分解可以从频率学派角度帮助理解模型复杂度问题，但它的实际价值有限，因为这种分解依赖于在多组数据集上取平均，而实践中我们只有一个观测数据集。若有大量给定大小的独立训练集，更好的做法是把它们合并成一个大训练集；对于给定的模型复杂度，这当然会减轻过拟合。

考虑到这些局限，下一节将转向线性基函数模型的贝叶斯处理。它不仅能帮助我们深入理解过拟合，还能给出处理模型复杂度问题的实用方法。

## 3.3 贝叶斯线性回归

在讨论用最大似然确定线性回归模型的参数时，我们看到，由基函数数目决定的有效模型复杂度，需要根据数据集大小来控制。在对数似然函数中加入正则化项后，可以通过正则化系数的取值控制有效模型复杂度。当然，基函数的数目和形式仍然会重要地影响模型的整体表现。

这样仍然留下一个问题：对于具体任务，什么样的模型复杂度才合适？单纯最大化似然函数不能回答这个问题，因为它总会导致过于复杂的模型和过拟合。正如第 1.3 节所讨论的，可以使用独立留出的数据来确定模型复杂度，但这既可能需要较高的计算开销，也可能浪费宝贵的数据。因此，我们转向线性回归的贝叶斯处理方式。它能够避免最大似然的过拟合问题，还能给出仅用训练数据就自动确定模型复杂度的方法。同样，为简便起见，以下重点考虑单个目标变量 $t$。按照第 3.1.5 节的讨论，可以直接推广到多个目标变量。

### 3.3.1 参数分布

首先，为模型参数 $\mathbf{w}$ 引入先验概率分布，以此开始线性回归的贝叶斯处理。目前，先把噪声精度参数 $\beta$ 视为已知常量。注意，式（3.10）定义的似然函数 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})$ 是 $\mathbf{w}$ 的二次函数的指数。因此，相应的共轭先验是如下形式的高斯分布：

$$
p(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\mathbf{S}_0)
\tag{3.48}
$$

其均值为 $\mathbf{m}_0$，协方差为 $\mathbf{S}_0$。

<!-- pdf-page: 173 -->

接下来计算后验分布，它正比于似然函数与先验的乘积。由于选择了共轭高斯先验，后验也是高斯分布。可以按通常的方法，先对指数中的二次式配方，再利用归一化高斯分布的标准结果求出归一化系数，从而得到这个分布。<span class="margin-reference">习题 3.7</span> 不过，在推导一般结果（2.116）时，我们已经完成了所需的工作，因此可以直接写出后验分布：

$$
p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\mathbf{S}_N)
\tag{3.49}
$$

其中

$$
\mathbf{m}_N=\mathbf{S}_N(\mathbf{S}_0^{-1}\mathbf{m}_0+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}})
\tag{3.50}
$$

$$
\mathbf{S}_N^{-1}=\mathbf{S}_0^{-1}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}.
\tag{3.51}
$$

注意，由于后验为高斯分布，其众数与均值相同。因此，最大后验权重向量就是 $\mathbf{w}_{\mathrm{MAP}}=\mathbf{m}_N$。若考虑无限宽的先验 $\mathbf{S}_0=\alpha^{-1}\mathbf{I}$，并令 $\alpha\to0$，后验分布的均值 $\mathbf{m}_N$ 就退化为式（3.15）给出的最大似然值 $\mathbf{w}_{\mathrm{ML}}$。同样，如果 $N=0$，后验分布就恢复为先验。另外，如果数据点依次到来，那么任一阶段的后验分布都可作为下一个数据点的先验分布，新的后验仍由式（3.49）给出。<span class="margin-reference">习题 3.8</span>

在本章余下部分，为简化处理，我们将考虑一种特定形式的高斯先验。具体来说，采用均值为零、由单个精度参数 $\alpha$ 控制的各向同性高斯分布，即

$$
p(\mathbf{w}\mid\alpha)=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I})
\tag{3.52}
$$

相应的 $\mathbf{w}$ 的后验分布仍由式（3.49）给出，其中

$$
\mathbf{m}_N=\beta\mathbf{S}_N\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{3.53}
$$

$$
\mathbf{S}_N^{-1}=\alpha\mathbf{I}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}.
\tag{3.54}
$$

后验分布的对数等于对数似然与先验的对数之和。把它看作 $\mathbf{w}$ 的函数，可以写成

$$
\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})=-\frac{\beta}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2-\frac{\alpha}{2}\mathbf{w}^{\mathrm T}\mathbf{w}+\text{常数}.
\tag{3.55}
$$

因此，对 $\mathbf{w}$ 最大化这个后验分布，等价于最小化带二次正则化项的平方和误差函数，对应于式（3.27）中 $\lambda=\alpha/\beta$ 的情形。

可以用一个直线拟合的简单例子，说明线性基函数模型中的贝叶斯学习，以及后验分布的序贯更新。考虑单个输入变量 $x$、单个目标变量 $t$，以及

<!-- pdf-page: 174 -->
<!-- join-previous-paragraph -->
形式为 $y(x,\mathbf{w})=w_0+w_1x$ 的线性模型。这个模型只有两个可调参数，因此可以直接在参数空间中绘出先验和后验分布。我们使用函数 $f(x,\mathbf{a})=a_0+a_1x$ 生成合成数据，其中参数值为 $a_0=-0.3$、$a_1=0.5$：首先从均匀分布 $\mathcal{U}(x\mid-1,1)$ 中选取 $x_n$，然后计算 $f(x_n,\mathbf{a})$，最后加入标准差为 0.2 的高斯噪声，得到目标值 $t_n$。我们的目标是从这些数据中恢复 $a_0$ 和 $a_1$ 的值，并考察结果如何依赖于数据集大小。这里假设噪声方差已知，因此把精度参数设为其真值 $\beta=(1/0.2)^2=25$。同样，把参数 $\alpha$ 固定为 2.0。稍后将讨论如何根据训练数据确定 $\alpha$ 和 $\beta$。图 3.7 展示了数据集逐渐增大时，这个模型的贝叶斯学习结果，也展示了贝叶斯学习的序贯性质：观测到一个新数据点时，当前后验分布就成为先验。值得花时间仔细研究这幅图，因为它说明了贝叶斯推断的几个重要方面。第一行对应尚未观测到任何数据点的情况，给出了 $\mathbf{w}$ 空间中的先验分布，以及函数 $y(x,\mathbf{w})$ 的六个样本，其中 $\mathbf{w}$ 的值从先验中抽取。第二行展示观测到一个数据点后的情况。右列中的蓝色圆圈标出了该数据点的位置 $(x,t)$。左列绘出该数据点的似然函数 $p(t\mid x,\mathbf{w})$，把它看作 $\mathbf{w}$ 的函数。注意，似然函数给出一个软约束：直线必须经过数据点附近，而“附近”的程度由噪声精度 $\beta$ 决定。为便于比较，图 3.7 左列用白色十字标出了生成数据集所用的真实参数值 $a_0=-0.3$ 和 $a_1=0.5$。把这个似然函数乘以第一行的先验，再归一化，就得到第二行中图所示的后验分布。从这个后验分布中抽取 $\mathbf{w}$ 的样本，便得到右图中的回归函数 $y(x,\mathbf{w})$ 的样本。注意，这些样本直线都经过数据点附近。第三行展示观测到第二个数据点后的结果，该点同样用右图中的蓝色圆圈表示。仅由第二个数据点得到的相应似然函数显示在左图中。把这个似然函数乘以第二行的后验分布，就得到第三行中图所示的后验分布。注意，这个后验与将原始先验和两个数据点的似然函数结合后得到的后验完全相同。此时，后验已经受到两个数据点的影响；由于两点足以确定一条直线，后验分布已经相对集中。从这个后验中抽样，得到第三列中的红色函数曲线，可以看到，这些函数都经过两个数据点附近。第四行展示一共观测到 20 个数据点后的结果。左图是仅针对第 20 个数据点的似然函数，中图是已经吸收全部 20 次观测信息的后验分布。注意，与第三行相比，这个后验尖锐得多。在数据点数目趋于无穷的极限下，

<!-- pdf-page: 175 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-7.png" alt="直线拟合中随观测增加而更新的似然、先验或后验及数据空间样本"><figcaption>图 3.7：形式为 $y(x,\mathbf{w})=w_0+w_1x$ 的简单线性模型的序贯贝叶斯学习示意图。正文对该图作了详细说明。</figcaption><p class="figure-translation">likelihood → 似然；prior/posterior → 先验／后验；data space → 数据空间。</p></figure>

<!-- pdf-page: 176 -->
<!-- join-previous-paragraph-across-figures -->
后验分布将变成以真实参数值（白色十字所示）为中心的 delta 函数。

还可以考虑参数先验的其他形式。例如，可以将高斯先验推广为

$$
p(\mathbf{w}\mid\alpha)=\left[\frac{q}{2}\left(\frac{\alpha}{2}\right)^{1/q}\frac{1}{\Gamma(1/q)}\right]^M\exp\left(-\frac{\alpha}{2}\sum_{j=1}^{M}|w_j|^q\right)
\tag{3.56}
$$

其中，$q=2$ 对应高斯分布，而且只有这种情况下，先验才与似然函数（3.10）共轭。求 $\mathbf{w}$ 的后验分布最大值，对应于最小化正则化误差函数（3.29）。采用高斯先验时，后验分布的众数等于均值；但当 $q\ne2$ 时，这一点就不再成立。

### 3.3.2 预测分布

在实践中，我们通常并不关心 $\mathbf{w}$ 本身的值，而是希望对新的 $\mathbf{x}$ 值预测 $t$。为此，需要计算如下定义的预测分布：

$$
p(t\mid\boldsymbol{\mathsf{t}},\alpha,\beta)=\int p(t\mid\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\alpha,\beta)\,\mathrm{d}\mathbf{w}
\tag{3.57}
$$

其中，$\boldsymbol{\mathsf{t}}$ 是训练集中目标值组成的向量；为简化记号，我们省略了条件竖线右侧相应的输入向量。目标变量的条件分布 $p(t\mid\mathbf{x},\mathbf{w},\beta)$ 由式（3.8）给出，权重的后验分布由式（3.49）给出。可见，式（3.57）涉及两个高斯分布的卷积，因此利用第 8.1.4 节的结果（2.115），预测分布可写为 <span class="margin-reference">习题 3.10</span>

$$
p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}},\alpha,\beta)=\mathcal{N}(t\mid\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}),\sigma_N^2(\mathbf{x}))
\tag{3.58}
$$

其中，预测分布的方差 $\sigma_N^2(\mathbf{x})$ 为

$$
\sigma_N^2(\mathbf{x})=\frac{1}{\beta}+\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}).
\tag{3.59}
$$

式（3.59）的第一项表示数据中的噪声，第二项反映参数 $\mathbf{w}$ 的不确定性。由于噪声过程与 $\mathbf{w}$ 的分布是相互独立的高斯分布，它们的方差可以相加。注意，随着观测到更多数据点，后验分布会变窄。由此可以证明（Qazaz et al., 1997），$\sigma_{N+1}^2(\mathbf{x})\leqslant\sigma_N^2(\mathbf{x})$。<span class="margin-reference">习题 3.11</span> 当 $N\to\infty$ 时，式（3.59）的第二项趋于零，预测分布的方差完全来自由参数 $\beta$ 控制的加性噪声。

为了说明贝叶斯线性回归模型的预测分布，我们回到第 1.1 节的合成正弦数据集。在图 3.8 中，

<!-- pdf-page: 177 -->
<!-- join-previous-paragraph -->
我们把由高斯基函数线性组合构成的模型，拟合到大小不同的数据集上，再考察相应的后验分布。这里，绿色曲线对应函数 $\sin(2\pi x)$，数据点由这个函数加上高斯噪声生成。四幅图中的蓝色圆圈分别表示大小为 $N=1$、$N=2$、$N=4$ 和 $N=25$ 的数据集。每幅图中，红色曲线表示相应高斯预测分布的均值，红色阴影表示均值上下各一个标准差的范围。注意，预测的不确定性取决于 $x$，并且在数据点附近最小。还要注意，随着观测到更多数据点，不确定性会减小。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-8.png" alt="不同样本量下高斯基函数回归的预测均值和不确定性范围"><figcaption>图 3.8：使用第 1.1 节的合成正弦数据集，展示由 9 个式（3.4）形式的高斯基函数组成的模型的预测分布（3.58）。详细讨论见正文。</figcaption></figure>

图 3.8 只展示了随 $x$ 变化的逐点预测方差。为了理解不同 $x$ 值处的预测之间的协方差，可以从 $\mathbf{w}$ 的后验分布中抽取样本，再绘出相应的函数 $y(x,\mathbf{w})$，如图 3.9 所示。

<!-- pdf-page: 178 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/a-fig-3-9.png" alt="从不同数据量对应的权重后验中抽样得到的回归函数"><figcaption>图 3.9：从图 3.8 各图对应的 $\mathbf{w}$ 后验分布中抽取样本，并绘出函数 $y(x,\mathbf{w})$。</figcaption></figure>

如果采用高斯函数这类局部基函数，那么在远离基函数中心的区域，预测方差（3.59）中第二项的贡献会趋于零，只剩下噪声贡献 $\beta^{-1}$。因此，当外推到基函数所覆盖区域之外时，模型会对自己的预测非常确信，这通常并不是我们希望的表现。采用另一种称为高斯过程（Gaussian process）的贝叶斯回归方法，可以避免这个问题。<span class="margin-reference">第 6.4 节</span>

注意，如果把 $\mathbf{w}$ 和 $\beta$ 都视为未知量，就可以引入共轭先验分布 $p(\mathbf{w},\beta)$；根据第 2.3.6 节的讨论，它是一个高斯-伽马分布（Denison et al., 2002）。<span class="margin-reference">习题 3.12</span> 在这种情况下，预测分布是 Student t 分布。<span class="margin-reference">习题 3.13</span>

<!-- pdf-page: 179 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-10.png" alt="高斯基函数的等效核矩阵，以及对应三个不同输入位置的核切片"><figcaption>图 3.10：图 3.1 中高斯基函数的等效核 $k(x,x')$。右图以 $x$ 和 $x'$ 为坐标展示这个核，左边给出该矩阵在三个不同 $x$ 值处的切片。用于生成这个核的数据集包含 200 个 $x$ 值，它们在区间 $(-1,1)$ 上等间隔分布。</figcaption></figure>

### 3.3.3 等效核

线性基函数模型的后验均值解（3.53）有一种有趣的解释，它将为包括高斯过程在内的核方法奠定基础（第 6 章）。将（3.53）代入表达式（3.3），可以看到预测均值可写为

$$
y(\mathbf{x},\mathbf{m}_N)=\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})=\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}=\sum_{n=1}^{N}\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}_n)t_n
\tag{3.60}
$$

其中 $\mathbf{S}_N$ 由（3.51）定义。因此，点 $\mathbf{x}$ 处预测分布的均值是训练集目标变量 $t_n$ 的线性组合，所以可以写成

$$
y(\mathbf{x},\mathbf{m}_N)=\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)t_n
\tag{3.61}
$$

其中函数

$$
k(\mathbf{x},\mathbf{x}')=\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}')
\tag{3.62}
$$

称为*平滑矩阵*（smoother matrix）或*等效核*（equivalent kernel）。像这样通过训练集目标值的线性组合来进行预测的回归函数，称为*线性平滑器*（linear smoother）。注意，等效核依赖于数据集中的输入值 $\mathbf{x}_n$，因为 $\mathbf{S}_N$ 的定义中包含这些输入值。图 3.10 展示了高斯基函数的等效核，图中对三个不同的 $x$ 值，将核函数 $k(x,x')$ 画成了 $x'$ 的函数。可以看到，这些函数都集中在 $x$ 附近，因此，$x$ 处预测分布的均值 $y(x,\mathbf{m}_N)$ 是目标值的加权组合，其中靠近 $x$ 的数据点得到的权重高于离 $x$ 较远的数据点。直观上，赋予局部证据比远处证据更大的权重是合理的。注意，这种局部性不仅适用于具有局部性的高斯基函数，也适用于非局部的多项式基函数和 sigmoid（S 形）基函数，如图 3.11 所示。

<!-- pdf-page: 180 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-11.png" alt="在 x 等于零处，多项式基函数和 sigmoid 基函数的等效核均表现出局部性"><figcaption>图 3.11：当 $x=0$ 时，将等效核 $k(x,x')$ 画成 $x'$ 的函数。左图对应图 3.1 中的多项式基函数，右图对应其中的 sigmoid 基函数。注意，虽然相应的基函数是非局部的，但这些核都是具有局部性的 $x'$ 的函数。</figcaption></figure>

考察 $y(\mathbf{x})$ 与 $y(\mathbf{x}')$ 之间的协方差，可以进一步理解等效核的作用。该协方差为

$$
\begin{aligned}
\operatorname{cov}[y(\mathbf{x}),y(\mathbf{x}')]&=\operatorname{cov}[\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{w},\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')]\\
&=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}')=\beta^{-1}k(\mathbf{x},\mathbf{x}')
\end{aligned}
\tag{3.63}
$$

这里使用了（3.49）和（3.62）。由等效核的形式可以看出，邻近位置的预测均值会高度相关，而相距较远的两个位置之间的相关性则较小。

图 3.8 所示的预测分布，使我们能够直观地看到各个位置处预测的不确定性，这种不确定性由（3.59）决定。但是，从 $\mathbf{w}$ 的后验分布中抽取样本，并像图 3.9 那样画出相应的模型函数 $y(\mathbf{x},\mathbf{w})$，则可以直观地展示后验分布中两个（或更多个）$x$ 值所对应的 $y$ 值之间的联合不确定性；这种不确定性由等效核决定。

用核函数来表述线性回归，启发了下面另一种回归方法。我们可以直接定义一个具有局部性的核，而不必先引入一组基函数来隐式地确定等效核；然后，给定观测到的训练集，就用这个核对新的输入向量 $\mathbf{x}$ 进行预测。这样就得到了一种称为*高斯过程*的实用回归（及分类）框架，我们将在 6.4 节详细讨论。

我们已经看到，有效核确定了组合训练集目标值所用的权重，从而对新的 $\mathbf{x}$ 值进行预测。可以证明，这些权重之和为 1，也就是说，对于所有 $\mathbf{x}$ 值，都有

$$
\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)=1.
\tag{3.64}
$$

这个符合直觉的结果可以用一种非严格的方式轻易证明（习题 3.14）：注意，上述求和等价于考虑这样一组目标数据的预测均值 $\widehat{y}(\mathbf{x})$，其中对所有 $n$ 都有 $t_n=1$。只要基函数线性无关、数据点的数目多于基函数的数目，并且其中一个基函数是常数（对应于偏置参数），显然就能精确拟合训练数据，因而预测均值

<!-- pdf-page: 181 -->
<!-- join-previous-paragraph -->
就是 $\widehat{y}(\mathbf{x})=1$，由此得到（3.64）。注意，核函数既可以为正，也可以为负，因此，虽然它满足一个求和约束，相应的预测却不一定是训练集目标变量的凸组合。

最后要指出，等效核（3.62）满足核函数普遍具有的一个重要性质（第 6 章），即它可以表示为非线性函数向量 $\boldsymbol{\psi}(\mathbf{x})$ 的内积形式：

$$
k(\mathbf{x},\mathbf{z})=\boldsymbol{\psi}(\mathbf{x})^{\mathrm T}\boldsymbol{\psi}(\mathbf{z})
\tag{3.65}
$$

其中 $\boldsymbol{\psi}(\mathbf{x})=\beta^{1/2}\mathbf{S}_N^{1/2}\boldsymbol{\phi}(\mathbf{x})$。

## 3.4 贝叶斯模型比较

在第 1 章中，我们着重介绍了过拟合问题，以及如何使用交叉验证来设定正则化参数的值，或在不同的候选模型之间作出选择。这里，我们从贝叶斯角度考察模型选择问题。本节将作一般性的讨论，随后在 3.5 节中，我们将看到如何将这些思想用于确定线性回归的正则化参数。

我们将会看到，对模型参数进行边缘化（求和或积分），而不是对它们的值进行点估计，就可以避免最大似然方法中的过拟合。这样，就能直接根据训练数据比较模型，而不需要验证集。这使得所有可用数据都可以用于训练，也免去了交叉验证要求对每个模型进行的多次训练。此外，这种方法还允许在训练过程中同时确定多个复杂度参数。例如，我们将在第 7 章介绍相关向量机，这是一种贝叶斯模型，每个训练数据点都有一个复杂度参数。

贝叶斯模型比较的做法，就是用概率表示模型选择的不确定性，并一致地运用概率的求和规则与乘积规则。假设要比较一组 $L$ 个模型 $\{\mathcal{M}_i\}$，其中 $i=1,\ldots,L$。这里，模型指的是观测数据 $\mathcal{D}$ 上的一个概率分布。在多项式曲线拟合问题中，该分布定义在目标值集合 $\boldsymbol{\mathsf{t}}$ 上，而输入值集合 $\mathbf{X}$ 则假定为已知。其他类型的模型会定义 $\mathbf{X}$ 与 $\boldsymbol{\mathsf{t}}$ 上的联合分布（1.5.4 节）。我们假设数据由这些模型中的某一个生成，但不确定具体是哪一个。这种不确定性通过先验概率分布 $p(\mathcal{M}_i)$ 来表示。给定训练集 $\mathcal{D}$，我们希望计算后验分布

$$
p(\mathcal{M}_i\mid\mathcal{D})\propto p(\mathcal{M}_i)p(\mathcal{D}\mid\mathcal{M}_i).
\tag{3.66}
$$

先验允许我们表达对不同模型的偏好。这里简单地假设所有模型具有相等的先验概率。值得关注的是模型证据 $p(\mathcal{D}\mid\mathcal{M}_i)$，它表示数据对

<!-- pdf-page: 182 -->
<!-- join-previous-paragraph -->
不同模型的偏好，我们马上就会更详细地考察这一项。模型证据有时也称为*边缘似然*（marginal likelihood），因为它可以看作模型空间上的似然函数，其中的参数已经被边缘化。两个模型的证据之比 $p(\mathcal{D}\mid\mathcal{M}_i)/p(\mathcal{D}\mid\mathcal{M}_j)$ 称为*贝叶斯因子*（Bayes factor；Kass and Raftery, 1995）。

一旦知道了模型的后验分布，根据求和规则与乘积规则，预测分布就为

$$
p(t\mid\mathbf{x},\mathcal{D})=\sum_{i=1}^{L}p(t\mid\mathbf{x},\mathcal{M}_i,\mathcal{D})p(\mathcal{M}_i\mid\mathcal{D}).
\tag{3.67}
$$

这是混合分布的一个例子：总体预测分布，是以各个模型的后验概率 $p(\mathcal{M}_i\mid\mathcal{D})$ 为权重，对它们各自的预测分布 $p(t\mid\mathbf{x},\mathcal{M}_i,\mathcal{D})$ 求平均得到的。例如，假设两个模型的后验概率相等，一个预测 $t=a$ 附近的窄分布，另一个预测 $t=b$ 附近的窄分布，那么总体预测分布将是一个双峰分布，峰分别位于 $t=a$ 和 $t=b$，而不是在 $t=(a+b)/2$ 处的单一模型。

对模型平均的一种简单近似，是只使用概率最大的那个模型进行预测。这称为*模型选择*。

对于由一组参数 $\mathbf{w}$ 控制的模型，依据概率的求和规则与乘积规则，模型证据为

$$
p(\mathcal{D}\mid\mathcal{M}_i)=\int p(\mathcal{D}\mid\mathbf{w},\mathcal{M}_i)p(\mathbf{w}\mid\mathcal{M}_i)\,d\mathbf{w}.
\tag{3.68}
$$

从采样的角度看（第 11 章），边缘似然可以理解为：先从先验中随机抽取模型参数，然后由该模型生成数据集 $\mathcal{D}$ 的概率。还有一点值得注意：在使用贝叶斯定理计算参数的后验分布时，证据恰好就是分母中的归一化项，因为

$$
p(\mathbf{w}\mid\mathcal{D},\mathcal{M}_i)=\frac{p(\mathcal{D}\mid\mathbf{w},\mathcal{M}_i)p(\mathbf{w}\mid\mathcal{M}_i)}{p(\mathcal{D}\mid\mathcal{M}_i)}.
\tag{3.69}
$$

对参数积分作一个简单近似，有助于理解模型证据。先考虑只有一个参数 $w$ 的模型。参数的后验分布正比于 $p(\mathcal{D}\mid w)p(w)$；为简化记号，这里略去了对模型 $\mathcal{M}_i$ 的依赖。假设后验分布在概率最大的值 $w_{\mathrm{MAP}}$ 附近有一个尖峰，宽度为 $\Delta w_{\mathrm{posterior}}$，那么就可以用被积函数的最大值乘以峰的宽度来近似积分。如果再假设先验是宽度为 $\Delta w_{\mathrm{prior}}$ 的平坦分布，即 $p(w)=1/\Delta w_{\mathrm{prior}}$，那么有

$$
p(\mathcal{D})=\int p(\mathcal{D}\mid w)p(w)\,dw\simeq p(\mathcal{D}\mid w_{\mathrm{MAP}})\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}
\tag{3.70}
$$

<!-- pdf-page: 183 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-12.png" alt="宽先验与窄后验分布示意，以及两者宽度和后验众数"><figcaption>图 3.12：如果假设参数的后验分布在其众数 $w_{\mathrm{MAP}}$ 附近具有尖峰，就可以得到模型证据的粗略近似。</figcaption><p class="figure-translation">$\Delta w_{\mathrm{posterior}}$：后验分布的宽度；$\Delta w_{\mathrm{prior}}$：先验分布的宽度；$w_{\mathrm{MAP}}$：最大后验参数值；$w$：参数。</p></figure>

于是取对数得到

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid w_{\mathrm{MAP}})+\ln\left(\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}\right).
\tag{3.71}
$$

图 3.12 展示了这一近似。第一项表示使用概率最大的参数值时对数据的拟合程度；对于平坦先验，它就对应于对数似然。第二项则根据模型的复杂度施加惩罚。由于 $\Delta w_{\mathrm{posterior}}<\Delta w_{\mathrm{prior}}$，这一项为负，而且随着比值 $\Delta w_{\mathrm{posterior}}/\Delta w_{\mathrm{prior}}$ 减小，其绝对值会增大。因此，如果后验分布中的参数需要针对数据作精细调节，惩罚项就会很大。

对于具有 $M$ 个参数的模型，可以依次对每个参数作类似近似。假设所有参数的 $\Delta w_{\mathrm{posterior}}/\Delta w_{\mathrm{prior}}$ 比值相同，则得到

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid\mathbf{w}_{\mathrm{MAP}})+M\ln\left(\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}\right).
\tag{3.72}
$$

因此，在这个很简单的近似中，复杂度惩罚的大小随模型中可调参数的数目 $M$ 线性增长。当模型复杂度增加时，第一项通常会减小，因为更复杂的模型更能拟合数据；而第二项则由于依赖于 $M$ 而增大。由最大证据确定的最优模型复杂度，将取决于这两个相互竞争的项之间的权衡。我们将在后面基于后验分布的高斯近似，给出这一近似的更精细版本（4.4.1 节）。

考察图 3.13，可以进一步理解贝叶斯模型比较，并明白边缘似然为什么可能偏好复杂度适中的模型。这里，横轴是所有可能数据集所构成空间的一维表示，因此轴上的每一点都对应于一个特定的数据集。现在考虑复杂度依次增加的三个模型 $\mathcal{M}_1$、$\mathcal{M}_2$ 和 $\mathcal{M}_3$。设想用这些模型来生成一些示例数据集，然后考察所得数据集的分布。任意给定的

<!-- pdf-page: 184 -->
<!-- join-previous-paragraph -->
模型都可以生成多种不同的数据集，因为参数由先验概率分布决定，而且对于任何给定的参数值，目标变量都可能带有随机噪声。要从一个特定模型生成一个数据集，首先从参数的先验分布 $p(\mathbf{w})$ 中选取参数值，然后在这些参数值下从 $p(\mathcal{D}\mid\mathbf{w})$ 中对数据采样。简单模型（例如基于一次多项式的模型）的变化范围很小，因此生成的数据集彼此相当相似。于是，其分布 $p(\mathcal{D})$ 被限制在横轴上一个相对较小的区域内。相比之下，复杂模型（例如九次多项式）可以生成多种多样的数据集，所以其分布 $p(\mathcal{D})$ 分散在数据集空间的较大区域中。由于分布 $p(\mathcal{D}\mid\mathcal{M}_i)$ 都经过了归一化，可以看到，对于特定数据集 $\mathcal{D}_0$，复杂度适中的模型可能具有最大的证据。实质上，较简单的模型不能很好地拟合数据，而较复杂的模型则将预测概率分散到过于广泛的数据集上，从而只给每个数据集分配相对较小的概率。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-13.png" alt="不同复杂度模型生成数据集的分布，以及数据集 D0 对应的模型证据"><figcaption>图 3.13：三个不同复杂度模型的数据集分布示意图，其中 $\mathcal{M}_1$ 最简单，$\mathcal{M}_3$ 最复杂。注意，这些分布都经过了归一化。在这个例子中，对于观测到的特定数据集 $\mathcal{D}_0$，复杂度适中的模型 $\mathcal{M}_2$ 具有最大的证据。</figcaption><p class="figure-translation">$p(\mathcal{D})$：数据集的概率；$\mathcal{D}$：数据集；$\mathcal{D}_0$：观测到的数据集；$\mathcal{M}_1$、$\mathcal{M}_2$、$\mathcal{M}_3$：复杂度依次增加的三个模型。</p></figure>

贝叶斯模型比较框架隐含着一个假设：生成数据的真实分布包含在所考察的模型集合中。只要这一条件成立，就可以证明，贝叶斯模型比较平均而言会偏好正确模型。为此，考虑两个模型 $\mathcal{M}_1$ 和 $\mathcal{M}_2$，其中真实情况对应于 $\mathcal{M}_1$。对于一个给定的有限数据集，错误模型可能具有更大的贝叶斯因子。但是，如果按照数据集的分布对贝叶斯因子求平均，就得到如下形式的期望贝叶斯因子：

$$
\int p(\mathcal{D}\mid\mathcal{M}_1)\ln\frac{p(\mathcal{D}\mid\mathcal{M}_1)}{p(\mathcal{D}\mid\mathcal{M}_2)}\,d\mathcal{D}
\tag{3.73}
$$

这里按数据的真实分布求平均。这个量是 Kullback–Leibler 散度的一个例子（1.6.1 节），它总是为正，只有两个分布相等时才为零。因此，平均而言，贝叶斯因子总会偏好正确模型。

我们已经看到，贝叶斯框架可以避免过拟合问题，并允许仅根据训练数据来比较模型。不过，

<!-- pdf-page: 185 -->
<!-- join-previous-paragraph -->
贝叶斯方法与所有模式识别方法一样，都需要对模型的形式作出假设；如果这些假设不成立，结果就可能产生误导。特别是，从图 3.12 可以看出，模型证据可能对先验的许多方面都很敏感，例如其尾部的行为。事实上，如果先验是非正常先验，证据就没有定义。原因在于，非正常先验具有任意的缩放因子（换句话说，由于分布无法归一化，归一化系数也就没有定义）。如果先考虑一个正常先验，再取适当的极限得到非正常先验（例如，对高斯先验取方差趋于无穷大的极限），那么证据将趋于零，这可以从（3.70）和图 3.12 看出。不过，也许可以先考虑两个模型的证据之比，再取极限，从而得到有意义的答案。

因此，在实际应用中，明智的做法是留出一个独立的测试数据集，用它评估最终系统的总体性能。

## 3.5 证据近似

在线性基函数模型的完全贝叶斯处理中，我们会为超参数 $\alpha$ 和 $\beta$ 引入先验分布，并在预测时同时对这些超参数以及参数 $\mathbf{w}$ 进行边缘化。但是，虽然可以对 $\mathbf{w}$ 或超参数中的任一部分进行解析积分，要对所有这些变量完成全部边缘化，却无法解析求解。这里讨论一种近似方法：先对参数 $\mathbf{w}$ 积分，得到边缘似然函数，再通过最大化这个函数，将超参数设定为具体的值。在统计学文献中，这一框架称为*经验贝叶斯*（empirical Bayes；Bernardo and Smith, 1994; Gelman et al., 2004）、*第二类最大似然*（type 2 maximum likelihood；Berger, 1985）或*广义最大似然*（generalized maximum likelihood；Wahba, 1975）；在机器学习文献中，它也称为*证据近似*（evidence approximation；Gull, 1989; MacKay, 1992a）。

如果在 $\alpha$ 和 $\beta$ 上引入超先验，那么对 $\mathbf{w}$、$\alpha$ 和 $\beta$ 进行边缘化，就得到预测分布

$$
p(t\mid\boldsymbol{\mathsf{t}})=\iiint p(t\mid\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\alpha,\beta)p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})\,d\mathbf{w}\,d\alpha\,d\beta
\tag{3.74}
$$

其中 $p(t\mid\mathbf{w},\beta)$ 由（3.8）给出，$p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\alpha,\beta)$ 由（3.49）给出，$\mathbf{m}_N$ 和 $\mathbf{S}_N$ 则分别由（3.53）和（3.54）定义。为了简化记号，这里略去了对输入变量 $\mathbf{x}$ 的依赖。如果后验分布 $p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})$ 在 $\widehat{\alpha}$ 和 $\widehat{\beta}$ 附近有尖峰，那么只需将 $\alpha$ 和 $\beta$ 固定为 $\widehat{\alpha}$ 和 $\widehat{\beta}$，再对 $\mathbf{w}$ 进行边缘化，就可得到预测分布，即

$$
p(t\mid\boldsymbol{\mathsf{t}})\simeq p(t\mid\boldsymbol{\mathsf{t}},\widehat{\alpha},\widehat{\beta})=\int p(t\mid\mathbf{w},\widehat{\beta})p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\widehat{\alpha},\widehat{\beta})\,d\mathbf{w}.
\tag{3.75}
$$

<!-- pdf-page: 186 -->

根据贝叶斯定理，$\alpha$ 和 $\beta$ 的后验分布为

$$
p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})\propto p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)p(\alpha,\beta).
\tag{3.76}
$$

如果先验比较平坦，那么在证据框架中，$\widehat{\alpha}$ 和 $\widehat{\beta}$ 的值就通过最大化边缘似然函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 来确定。下面先计算线性基函数模型的边缘似然，再寻找其最大值。这样，仅使用训练数据就能确定这些超参数，而不必借助交叉验证。回忆一下，比值 $\alpha/\beta$ 的作用类似于正则化参数。

顺便指出，如果为 $\alpha$ 和 $\beta$ 定义共轭的伽马先验分布，那么（3.74）中对这些超参数的边缘化就可以解析完成，并得到 $\mathbf{w}$ 上的 Student $t$ 分布（见 2.3.7 节）。虽然此后对 $\mathbf{w}$ 的积分已无法解析求解，但人们可能会想到，对这个积分作近似，例如使用 4.4 节讨论的拉普拉斯近似，或许能够得到证据框架的一种实用替代方法（Buntine and Weigend, 1991）。拉普拉斯近似是在后验分布的众数处构造局部高斯近似。不过，将被积函数看作 $\mathbf{w}$ 的函数时，其峰通常存在很强的偏斜，因此拉普拉斯近似无法覆盖大部分概率质量，所得结果也就差于最大化证据的方法（MacKay, 1999）。

回到证据框架，可以用两种方法最大化对数证据。一种是解析计算证据函数，再令其导数为零，从而得到 $\alpha$ 和 $\beta$ 的重新估计方程；我们将在 3.5.2 节采用这种方法。另一种则使用*期望最大化*（expectation maximization，EM）算法。我们将在 9.3.4 节讨论这一算法，并证明这两种方法会收敛到相同的解。

### 3.5.1 计算证据函数

边缘似然函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 是对权重参数 $\mathbf{w}$ 积分得到的，即

$$
p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)p(\mathbf{w}\mid\alpha)\,d\mathbf{w}.
\tag{3.77}
$$

计算这一积分的一种方法，是再次利用线性高斯模型中关于条件分布的结果（2.115）（习题 3.16）。这里改用另一种方法：对指数中的表达式配方，再利用高斯分布归一化系数的标准形式来计算积分。

由（3.11）、（3.12）和（3.52），可以将证据函数写为（习题 3.17）

$$
p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\left(\frac{\beta}{2\pi}\right)^{N/2}\left(\frac{\alpha}{2\pi}\right)^{M/2}\int\exp\{-E(\mathbf{w})\}\,d\mathbf{w}
\tag{3.78}
$$

<!-- pdf-page: 187 -->

其中 $M$ 是 $\mathbf{w}$ 的维数，并且定义

$$
\begin{aligned}
E(\mathbf{w})&=\beta E_D(\mathbf{w})+\alpha E_W(\mathbf{w})\\
&=\frac{\beta}{2}\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{w}\|^2+\frac{\alpha}{2}\mathbf{w}^{\mathrm T}\mathbf{w}.
\end{aligned}
\tag{3.79}
$$

可以看出，除了一个常数比例因子外，（3.79）就是正则化的平方和误差函数（3.27）。现在对 $\mathbf{w}$ 配方，得到（习题 3.18）

$$
E(\mathbf{w})=E(\mathbf{m}_N)+\frac{1}{2}(\mathbf{w}-\mathbf{m}_N)^{\mathrm T}\mathbf{A}(\mathbf{w}-\mathbf{m}_N)
\tag{3.80}
$$

其中引入了

$$
\mathbf{A}=\alpha\mathbf{I}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}
\tag{3.81}
$$

以及

$$
E(\mathbf{m}_N)=\frac{\beta}{2}\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}_N\|^2+\frac{\alpha}{2}\mathbf{m}_N^{\mathrm T}\mathbf{m}_N.
\tag{3.82}
$$

注意，$\mathbf{A}$ 对应于误差函数的二阶导数矩阵

$$
\mathbf{A}=\nabla\nabla E(\mathbf{w})
\tag{3.83}
$$

称为*Hessian 矩阵*。这里还定义了 $\mathbf{m}_N$：

$$
\mathbf{m}_N=\beta\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}.
\tag{3.84}
$$

由（3.54）可知，$\mathbf{A}=\mathbf{S}_N^{-1}$，因此（3.84）与前面的定义（3.53）等价，所以它表示后验分布的均值。

现在，只需利用多元高斯分布归一化系数的标准结果，就可以计算对 $\mathbf{w}$ 的积分，得到（习题 3.19）

$$
\begin{aligned}
\int\exp\{-E(\mathbf{w})\}\,d\mathbf{w}
&=\exp\{-E(\mathbf{m}_N)\}\int\exp\left\{-\frac{1}{2}(\mathbf{w}-\mathbf{m}_N)^{\mathrm T}\mathbf{A}(\mathbf{w}-\mathbf{m}_N)\right\}\,d\mathbf{w}\\
&=\exp\{-E(\mathbf{m}_N)\}(2\pi)^{M/2}|\mathbf{A}|^{-1/2}.
\end{aligned}
\tag{3.85}
$$

利用（3.78），就可以将边缘似然的对数写为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\frac{M}{2}\ln\alpha+\frac{N}{2}\ln\beta-E(\mathbf{m}_N)-\frac{1}{2}\ln|\mathbf{A}|-\frac{N}{2}\ln(2\pi)
\tag{3.86}
$$

这就是所需的证据函数表达式。

回到多项式回归问题，可以将模型证据画成多项式次数的函数，如图 3.14 所示。这里假设先验具有（1.65）的形式，并将参数 $\alpha$ 固定为 $\alpha=5\times10^{-3}$。这张图的形状很有启发性。回顾图 1.4 可以看到，$M=0$ 的多项式对数据的拟合很差，因此证据的值也

<!-- pdf-page: 188 -->
<!-- join-previous-paragraph -->
相对较低。改用 $M=1$ 的多项式后，数据拟合有了很大改善，因而证据明显提高。不过，从 $M=1$ 增至 $M=2$ 时，数据拟合只得到很微小的改善，因为生成数据的底层正弦函数是奇函数，所以其多项式展开中没有偶数次项。事实上，图 1.5 表明，从 $M=1$ 增至 $M=2$ 时，残余的数据误差只略有下降。由于这个更丰富的模型受到更大的复杂度惩罚，从 $M=1$ 增至 $M=2$ 时，证据实际上反而降低。增至 $M=3$ 时，数据拟合又得到明显改善，如图 1.4 所示，因此证据再次增加，达到所有这些多项式中的最大值。继续增大 $M$，只能带来数据拟合上的小幅改善，却会受到越来越大的复杂度惩罚，综合结果就是证据值下降。再看图 1.5，可见泛化误差在 $M=3$ 到 $M=8$ 之间大致保持不变，仅根据这张图很难在这些模型之间作出选择。不过，证据值明确偏好 $M=3$，因为这是能够很好解释观测数据的最简单模型。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-14.png" alt="多项式回归的模型证据随次数变化，在三次时最大"><figcaption>图 3.14：多项式回归模型的模型证据随次数 $M$ 的变化。图中显示，证据偏好 $M=3$ 的模型。</figcaption><p class="figure-translation">$M$：多项式的次数。</p></figure>

### 3.5.2 最大化证据函数

先考虑如何关于 $\alpha$ 最大化 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$。为此，首先定义下列特征向量方程：

$$
\left(\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}\right)\mathbf{u}_i=\lambda_i\mathbf{u}_i.
\tag{3.87}
$$

由（3.81）可知，$\mathbf{A}$ 的特征值为 $\alpha+\lambda_i$。现在考虑（3.86）中含有 $\ln|\mathbf{A}|$ 的项对 $\alpha$ 的导数。有

$$
\frac{d}{d\alpha}\ln|\mathbf{A}|=\frac{d}{d\alpha}\ln\prod_i(\lambda_i+\alpha)=\frac{d}{d\alpha}\sum_i\ln(\lambda_i+\alpha)=\sum_i\frac{1}{\lambda_i+\alpha}.
\tag{3.88}
$$

因此，（3.86）关于 $\alpha$ 的驻点满足

$$
0=\frac{M}{2\alpha}-\frac{1}{2}\mathbf{m}_N^{\mathrm T}\mathbf{m}_N-\frac{1}{2}\sum_i\frac{1}{\lambda_i+\alpha}.
\tag{3.89}
$$

<!-- pdf-page: 189 -->

两边乘以 $2\alpha$ 并整理，得到

$$
\alpha\mathbf{m}_N^{\mathrm T}\mathbf{m}_N=M-\alpha\sum_i\frac{1}{\lambda_i+\alpha}=\gamma.
\tag{3.90}
$$

由于对 $i$ 的求和中有 $M$ 项，$\gamma$ 可以写为

$$
\gamma=\sum_i\frac{\lambda_i}{\alpha+\lambda_i}.
\tag{3.91}
$$

稍后将讨论 $\gamma$ 的含义。由（3.90）可见，使边缘似然最大的 $\alpha$ 值满足（习题 3.20）

$$
\alpha=\frac{\gamma}{\mathbf{m}_N^{\mathrm T}\mathbf{m}_N}.
\tag{3.92}
$$

注意，这是 $\alpha$ 的隐式解，不仅因为 $\gamma$ 依赖于 $\alpha$，还因为后验分布的众数 $\mathbf{m}_N$ 本身也依赖于 $\alpha$ 的选择。因此，我们采用迭代过程：首先选择 $\alpha$ 的初始值，用它求出（3.53）给出的 $\mathbf{m}_N$，并计算（3.91）给出的 $\gamma$。再将这些值代入（3.92），重新估计 $\alpha$，反复进行直至收敛。注意，由于矩阵 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 是固定的，可以在开始时只计算一次它的特征值，然后将这些特征值乘以 $\beta$，就得到 $\lambda_i$。

需要强调，$\alpha$ 的值完全是根据训练数据确定的。与最大似然方法不同，这里不需要独立的数据集来优化模型复杂度。

同样，也可以关于 $\beta$ 最大化对数边缘似然（3.86）。为此，注意（3.87）定义的特征值 $\lambda_i$ 正比于 $\beta$，因此 $d\lambda_i/d\beta=\lambda_i/\beta$，于是

$$
\frac{d}{d\beta}\ln|\mathbf{A}|=\frac{d}{d\beta}\sum_i\ln(\lambda_i+\alpha)=\frac{1}{\beta}\sum_i\frac{\lambda_i}{\lambda_i+\alpha}=\frac{\gamma}{\beta}.
\tag{3.93}
$$

因此，边缘似然的驻点满足

$$
0=\frac{N}{2\beta}-\frac{1}{2}\sum_{n=1}^{N}\left\{t_n-\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2-\frac{\gamma}{2\beta}
\tag{3.94}
$$

整理后得到（习题 3.22）

$$
\frac{1}{\beta}=\frac{1}{N-\gamma}\sum_{n=1}^{N}\left\{t_n-\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2.
\tag{3.95}
$$

这仍然是 $\beta$ 的隐式解。可以先选取 $\beta$ 的初值，用它计算 $\mathbf{m}_N$ 和 $\gamma$，再利用（3.95）重新估计 $\beta$，重复这一过程直至收敛。如果 $\alpha$ 和 $\beta$ 都要根据数据确定，则每次更新 $\gamma$ 后，可以一并重新估计它们的值。

<!-- pdf-page: 190 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-15.png" alt="似然与先验的等高线，两个特征方向上最大后验解所受约束不同"><figcaption>图 3.15：似然函数（红色）和先验（绿色）的等高线。参数空间中的坐标轴经过旋转，与 Hessian 矩阵的特征向量 $\mathbf{u}_i$ 对齐。当 $\alpha=0$ 时，后验的众数由最大似然解 $\mathbf{w}_{\mathrm{ML}}$ 给出；当 $\alpha$ 非零时，众数位于 $\mathbf{w}_{\mathrm{MAP}}=\mathbf{m}_N$。在 $w_1$ 方向上，（3.87）定义的特征值 $\lambda_1$ 与 $\alpha$ 相比较小，因此 $\lambda_1/(\lambda_1+\alpha)$ 接近于零，相应的 $w_1$ 的 MAP 值也接近于零。相比之下，在 $w_2$ 方向上，特征值 $\lambda_2$ 与 $\alpha$ 相比较大，因此 $\lambda_2/(\lambda_2+\alpha)$ 接近于 1，而 $w_2$ 的 MAP 值接近其最大似然值。</figcaption><p class="figure-translation">$w_1$、$w_2$：参数坐标；$\mathbf{u}_1$、$\mathbf{u}_2$：特征向量；$\mathbf{w}_{\mathrm{MAP}}$：最大后验解；$\mathbf{w}_{\mathrm{ML}}$：最大似然解。</p></figure>

### 3.5.3 参数的有效数目

结果（3.92）有一个很简洁的解释（MacKay, 1992a），有助于理解 $\alpha$ 的贝叶斯解。为此，考虑图 3.15 所示的似然函数和先验的等高线。这里隐式地将参数空间的坐标轴作了旋转，使它们与（3.87）定义的特征向量 $\mathbf{u}_i$ 对齐。这样，似然函数的等高线就成为与坐标轴对齐的椭圆。特征值 $\lambda_i$ 衡量似然函数的曲率，因此，在图 3.15 中，特征值 $\lambda_1$ 比 $\lambda_2$ 小（因为曲率较小，对应于似然函数的等高线沿该方向拉得更长）。由于 $\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 是正定矩阵，其特征值为正，所以比值 $\lambda_i/(\lambda_i+\alpha)$ 位于 0 与 1 之间。因此，（3.91）定义的 $\gamma$ 位于 $0\leqslant\gamma\leqslant M$ 的范围内。对于 $\lambda_i\gg\alpha$ 的方向，相应的参数 $w_i$ 接近其最大似然值，而比值 $\lambda_i/(\lambda_i+\alpha)$ 接近 1。这些参数称为*充分确定的*（well determined）参数，因为它们的值受到数据的严格约束。相反，对于 $\lambda_i\ll\alpha$ 的方向，相应的参数 $w_i$ 接近于零，比值 $\lambda_i/(\lambda_i+\alpha)$ 也接近于零。在这些方向上，似然函数对参数值相对不敏感，因此先验将该参数设定为较小的值。所以，（3.91）定义的 $\gamma$ 衡量的是充分确定的参数的有效总数。

将重新估计 $\beta$ 的结果（3.95）与相应的最大似然结果（3.21）作比较，可以更深入地理解它。两个公式都将方差（即精度的倒数）表示为目标值与模型预测之差的平方的平均值。不过，两者的区别在于，最大似然结果分母中的数据点数 $N$，在贝叶斯结果中被替换为 $N-\gamma$。回忆（1.56），对于

<!-- pdf-page: 191 -->
<!-- join-previous-paragraph -->
单个变量 $x$ 上的高斯分布，方差的最大似然估计为

$$
\sigma_{\mathrm{ML}}^2=\frac{1}{N}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2
\tag{3.96}
$$

而且这一估计是有偏的，因为均值的最大似然解 $\mu_{\mathrm{ML}}$ 拟合了数据中的一部分噪声。这实际上消耗了模型中的一个自由度。相应的无偏估计由（1.59）给出，形式为

$$
\sigma_{\mathrm{MAP}}^2=\frac{1}{N-1}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2.
\tag{3.97}
$$

我们将在 10.1.3 节看到，对未知均值进行边缘化的贝叶斯处理可以得到这一结果。贝叶斯结果分母中的因子 $N-1$ 考虑了拟合均值已使用一个自由度这一事实，从而消除了最大似然估计的偏差。现在考虑线性回归模型的相应结果。目标分布的均值由函数 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})$ 给出，其中包含 $M$ 个参数。不过，这些参数并非全都由数据调节。由数据确定的参数的有效数目为 $\gamma$，其余 $M-\gamma$ 个参数则由先验设为较小的值。这体现为方差的贝叶斯结果在分母中具有因子 $N-\gamma$，从而修正了最大似然结果的偏差。

我们可以用 1.1 节的正弦合成数据集，以及包含 9 个基函数的高斯基函数模型，来说明如何用证据框架设定超参数。计入偏置后，模型的参数总数为 $M=10$。这里，为了便于展示，将 $\beta$ 设为其真实值 11.1，再使用证据框架确定 $\alpha$，如图 3.16 所示。

将各个参数画成参数有效数目 $\gamma$ 的函数，还可以看到参数 $\alpha$ 如何控制参数 $\{w_i\}$ 的大小，如图 3.17 所示。

考虑 $N\gg M$ 的极限情形，此时数据点的数目远大于参数的数目。由（3.87）可知，所有参数都能由数据充分确定，因为 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 中隐含了对数据点的求和，所以特征值 $\lambda_i$ 会随数据集的增大而增大。在这种情况下，$\gamma=M$，而 $\alpha$ 和 $\beta$ 的重新估计方程变为

$$
\alpha=\frac{M}{2E_W(\mathbf{m}_N)}
\tag{3.98}
$$

$$
\beta=\frac{N}{2E_D(\mathbf{m}_N)}
\tag{3.99}
$$

其中 $E_W$ 和 $E_D$ 分别由（3.25）和（3.26）定义。这些结果可以作为完整证据重新估计公式的一种易于计算的近似，

<!-- pdf-page: 192 -->
<!-- join-previous-paragraph -->
因为它们不需要计算 Hessian 矩阵的特征值谱。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-16.png" alt="证据近似确定超参数的交点、对数证据的峰值与测试集误差的比较"><figcaption>图 3.16：左图针对正弦合成数据集，画出了 $\gamma$（红色曲线）和 $2\alpha E_W(\mathbf{m}_N)$（蓝色曲线）随 $\ln\alpha$ 的变化。两条曲线的交点确定了证据方法给出的最优 $\alpha$ 值。右图给出了相应的对数证据 $\ln p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 随 $\ln\alpha$ 的变化（红色曲线），可以看到其峰值与左图中两条曲线的交点相对应。图中还给出了测试集误差（蓝色曲线），表明证据的最大值位于最佳泛化性能的位置附近。</figcaption><p class="figure-translation">$\ln\alpha$：超参数 $\alpha$ 的自然对数。</p></figure>

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-17.png" alt="高斯基函数模型的十个参数随参数有效数目变化的曲线"><figcaption>图 3.17：高斯基函数模型中的 10 个参数 $w_i$ 随参数有效数目 $\gamma$ 的变化。超参数 $\alpha$ 在 $0\leqslant\alpha\leqslant\infty$ 范围内变化，使 $\gamma$ 在 $0\leqslant\gamma\leqslant M$ 范围内变化。</figcaption><p class="figure-translation">$w_i$：第 $i$ 个权重参数；$\gamma$：参数的有效数目；曲线旁的 0 至 9 表示参数的下标。</p></figure>

## 3.6 固定基函数的局限性

本章始终关注由固定的非线性基函数的线性组合构成的模型。我们已经看到，对参数的线性假设带来了一系列有用的性质，包括最小二乘问题的闭式解，以及可以求解的贝叶斯处理。此外，只要适当地选择基函数，就可以对输入变量到目标值的映射中的任意非线性

<!-- pdf-page: 193 -->
<!-- join-previous-paragraph -->
进行建模。下一章中，我们将研究用于分类的一类类似模型。

因此，这些线性模型似乎构成了解决模式识别问题的通用框架。遗憾的是，线性模型存在一些明显的缺点，所以在后面的章节中，我们会转而讨论更复杂的模型，例如支持向量机和神经网络。

困难来源于这样一个假设：在观测训练数据集之前，基函数 $\phi_j(\mathbf{x})$ 已经固定。这是 1.4 节所讨论的维数灾难的一种表现。其结果是，基函数的数目需要随输入空间的维数 $D$ 快速增长，而且往往是指数增长。

好在真实数据集具有两个性质，可以用来缓解这一问题。首先，由于输入变量之间存在很强的相关性，数据向量 $\{\mathbf{x}_n\}$ 通常位于某个非线性流形附近，而该流形的内在维数低于输入空间的维数。第 12 章讨论手写数字图像时，我们将看到一个例子。如果使用具有局部性的基函数，可以让它们只分布在输入空间中有数据的区域。径向基函数网络，以及支持向量机和相关向量机，都采用了这种方法。神经网络模型使用具有 sigmoid 非线性的自适应基函数，可以调节参数，使基函数发生变化的输入空间区域与数据流形相对应。第二个性质是，目标变量可能仅对数据流形中少数几个可能方向有显著依赖。神经网络可以通过选择基函数所响应的输入空间方向来利用这一性质。

## 习题

**3.1（⋆）www** 证明，双曲正切函数 $\tanh$ 与 logistic sigmoid 函数（3.6）之间存在关系

$$
\tanh(a)=2\sigma(2a)-1.
\tag{3.100}
$$

由此证明，具有如下形式的 logistic sigmoid 函数的一般线性组合

$$
y(x,\mathbf{w})=w_0+\sum_{j=1}^{M}w_j\sigma\left(\frac{x-\mu_j}{s}\right)
\tag{3.101}
$$

等价于如下形式的 $\tanh$ 函数的线性组合

$$
y(x,\mathbf{u})=u_0+\sum_{j=1}^{M}u_j\tanh\left(\frac{x-\mu_j}{s}\right)
\tag{3.102}
$$

并求出新参数 $\{u_1,\ldots,u_M\}$ 与原参数 $\{w_1,\ldots,w_M\}$ 之间的关系式。

<!-- pdf-page: 194 -->

**3.2（⋆⋆）** 证明，矩阵

$$
\boldsymbol{\Phi}(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}
\tag{3.103}
$$

会将任意向量 $\mathbf{v}$ 投影到 $\boldsymbol{\Phi}$ 的列所张成的空间。利用这一结果，证明最小二乘解（3.15）对应于将向量 $\boldsymbol{\mathsf{t}}$ 正交投影到流形 $\mathcal{S}$ 上，如图 3.2 所示。

**3.3（⋆）** 考虑一个数据集，其中每个数据点 $t_n$ 都对应于一个权重因子 $r_n>0$，从而平方和误差函数变为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}r_n\left\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2.
\tag{3.104}
$$

求出使该误差函数最小的解 $\mathbf{w}^{\star}$ 的表达式。从两个角度分别解释这个加权平方和误差函数：（i）依赖于数据的噪声方差；（ii）重复的数据点。

**3.4（⋆）www** 考虑如下形式的线性模型

$$
y(\mathbf{x},\mathbf{w})=w_0+\sum_{i=1}^{D}w_ix_i
\tag{3.105}
$$

以及如下形式的平方和误差函数

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{y(\mathbf{x}_n,\mathbf{w})-t_n\}^2.
\tag{3.106}
$$

现在假设，向每个输入变量 $x_i$ 独立地加入均值为零、方差为 $\sigma^2$ 的高斯噪声 $\epsilon_i$。利用 $\mathbb{E}[\epsilon_i]=0$ 和 $\mathbb{E}[\epsilon_i\epsilon_j]=\delta_{ij}\sigma^2$，证明：最小化对噪声分布取平均后的 $E_D$，等价于最小化无噪声输入变量对应的平方和误差，加上一个权重衰减正则化项，其中正则化项不包含偏置参数 $w_0$。

**3.5（⋆）www** 使用附录 E 中讨论的拉格朗日乘数法，证明：最小化正则化误差函数（3.29），等价于在约束（3.30）下最小化未正则化的平方和误差（3.12）。讨论参数 $\eta$ 与 $\lambda$ 之间的关系。

**3.6（⋆）www** 考虑以多维目标变量 $\mathbf{t}$ 为输出的线性基函数回归模型，目标变量具有如下形式的高斯分布：

$$
p(\mathbf{t}\mid\mathbf{W},\boldsymbol{\Sigma})=\mathcal{N}(\mathbf{t}\mid\mathbf{y}(\mathbf{x},\mathbf{W}),\boldsymbol{\Sigma})
\tag{3.107}
$$

其中

$$
\mathbf{y}(\mathbf{x},\mathbf{W})=\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{3.108}
$$

<!-- pdf-page: 195 -->

此外，训练数据集由输入基向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 及其对应的目标向量 $\mathbf{t}_n$ 构成，其中 $n=1,\ldots,N$。证明，参数矩阵 $\mathbf{W}$ 的最大似然解 $\mathbf{W}_{\mathrm{ML}}$ 的每一列都由形如（3.15）的表达式给出，而（3.15）是各向同性噪声分布下的解。注意，这一结果与协方差矩阵 $\boldsymbol{\Sigma}$ 无关。证明，$\boldsymbol{\Sigma}$ 的最大似然解为

$$
\boldsymbol{\Sigma}=\frac{1}{N}\sum_{n=1}^{N}\left(\mathbf{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right)\left(\mathbf{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right)^{\mathrm T}.
\tag{3.109}
$$

**3.7（⋆）** 利用配方法，验证线性基函数模型中参数 $\mathbf{w}$ 的后验分布的结果（3.49），其中 $\mathbf{m}_N$ 和 $\mathbf{S}_N$ 分别由（3.50）和（3.51）定义。

**3.8（⋆⋆）www** 考虑 3.1 节的线性基函数模型，假设已经观测到 $N$ 个数据点，因此 $\mathbf{w}$ 的后验分布由（3.49）给出。这个后验可以看作下一次观测的先验。考虑额外的一个数据点 $(\mathbf{x}_{N+1},t_{N+1})$，通过对指数中的表达式配方，证明所得后验分布仍由（3.49）给出，只需将 $\mathbf{S}_N$ 替换为 $\mathbf{S}_{N+1}$，将 $\mathbf{m}_N$ 替换为 $\mathbf{m}_{N+1}$。

**3.9（⋆⋆）** 重做上一题，但不手动配方，而是利用（2.116）给出的线性高斯模型的一般结果。

**3.10（⋆⋆）www** 利用结果（2.115）计算（3.57）中的积分，验证贝叶斯线性回归模型的预测分布由（3.58）给出，其中依赖于输入的方差由（3.59）给出。

**3.11（⋆⋆）** 我们已经看到，随着数据集增大，模型参数的后验分布所具有的不确定性会减小。利用矩阵恒等式（附录 C）

$$
\left(\mathbf{M}+\mathbf{v}\mathbf{v}^{\mathrm T}\right)^{-1}=\mathbf{M}^{-1}-\frac{(\mathbf{M}^{-1}\mathbf{v})(\mathbf{v}^{\mathrm T}\mathbf{M}^{-1})}{1+\mathbf{v}^{\mathrm T}\mathbf{M}^{-1}\mathbf{v}}
\tag{3.110}
$$

证明，（3.59）给出的线性回归函数的不确定性 $\sigma_N^2(\mathbf{x})$ 满足

$$
\sigma_{N+1}^2(\mathbf{x})\leqslant\sigma_N^2(\mathbf{x}).
\tag{3.111}
$$

**3.12（⋆⋆）** 我们在 2.3.6 节看到，均值与精度（方差的倒数）均未知的高斯分布，其共轭先验是正态-伽马分布。对于线性回归模型的条件高斯分布 $p(t\mid\mathbf{x},\mathbf{w},\beta)$，这一性质同样成立。如果考虑似然函数（3.10），那么 $\mathbf{w}$ 和 $\beta$ 的共轭先验为

$$
p(\mathbf{w},\beta)=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\beta^{-1}\mathbf{S}_0)\operatorname{Gam}(\beta\mid a_0,b_0).
\tag{3.112}
$$

<!-- pdf-page: 196 -->

证明，相应的后验分布具有相同的函数形式，即

$$
p(\mathbf{w},\beta\mid\boldsymbol{\mathsf{t}})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\beta^{-1}\mathbf{S}_N)\operatorname{Gam}(\beta\mid a_N,b_N)
\tag{3.113}
$$

并求出后验参数 $\mathbf{m}_N$、$\mathbf{S}_N$、$a_N$ 和 $b_N$ 的表达式。

**3.13（⋆⋆）** 证明，习题 3.12 所讨论模型的预测分布 $p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}})$ 是如下形式的 Student $t$ 分布：

$$
p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}})=\operatorname{St}(t\mid\mu,\lambda,\nu)
\tag{3.114}
$$

并求出 $\mu$、$\lambda$ 和 $\nu$ 的表达式。

**3.14（⋆⋆）** 本题更详细地考察（3.62）定义的等效核的性质，其中 $\mathbf{S}_N$ 由（3.54）定义。假设基函数 $\phi_j(\mathbf{x})$ 线性无关，而且数据点数目 $N$ 大于基函数数目 $M$。此外，设其中一个基函数为常数，例如 $\phi_0(\mathbf{x})=1$。通过对这些基函数取适当的线性组合，可以构造一组新的基函数 $\psi_j(\mathbf{x})$，它们张成同一空间，但满足标准正交条件，即

$$
\sum_{n=1}^{N}\psi_j(\mathbf{x}_n)\psi_k(\mathbf{x}_n)=I_{jk}
\tag{3.115}
$$

其中，$j=k$ 时 $I_{jk}$ 定义为 1，否则为 0，并且取 $\psi_0(\mathbf{x})=1$。证明，当 $\alpha=0$ 时，等效核可以写成 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\psi}(\mathbf{x})^{\mathrm T}\boldsymbol{\psi}(\mathbf{x}')$，其中 $\boldsymbol{\psi}=(\psi_1,\ldots,\psi_M)^{\mathrm T}$。利用这一结果，证明该核满足求和约束

$$
\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)=1.
\tag{3.116}
$$

**3.15（⋆）www** 考虑一个用于回归的线性基函数模型，其中参数 $\alpha$ 和 $\beta$ 通过证据框架设定。证明，（3.82）定义的函数 $E(\mathbf{m}_N)$ 满足关系 $2E(\mathbf{m}_N)=N$。

**3.16（⋆⋆）** 利用（2.115）直接计算积分（3.77），推导线性回归模型的对数证据函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 的结果（3.86）。

**3.17（⋆）** 证明，贝叶斯线性回归模型的证据函数可以写成（3.78）的形式，其中 $E(\mathbf{w})$ 由（3.79）定义。

**3.18（⋆⋆）www** 对 $\mathbf{w}$ 配方，证明贝叶斯线性回归中的误差函数（3.79）可以写成（3.80）的形式。

**3.19（⋆⋆）** 证明，对贝叶斯线性回归模型中的 $\mathbf{w}$ 积分可得到结果（3.85）。由此证明，对数边缘似然由（3.86）给出。

<!-- pdf-page: 197 -->

**3.20（⋆⋆）www** 从（3.86）出发，逐步验证：关于 $\alpha$ 最大化对数边缘似然函数（3.86），会得到重新估计方程（3.92）。

**3.21（⋆⋆）** 在证据框架中推导 $\alpha$ 的最优值（3.92），还有一种方法，即利用恒等式

$$
\frac{d}{d\alpha}\ln|\mathbf{A}|=\operatorname{Tr}\left(\mathbf{A}^{-1}\frac{d}{d\alpha}\mathbf{A}\right).
\tag{3.117}
$$

考虑实对称矩阵 $\mathbf{A}$ 的特征值展开，并利用以特征值表示 $\mathbf{A}$ 的行列式与迹的标准结果（附录 C），证明这一恒等式。再利用（3.117），从（3.86）推导（3.92）。

**3.22（⋆⋆）** 从（3.86）出发，逐步验证：关于 $\beta$ 最大化对数边缘似然函数（3.86），会得到重新估计方程（3.95）。

**3.23（⋆⋆）www** 先对 $\mathbf{w}$ 边缘化，再对 $\beta$ 边缘化，证明习题 3.12 所描述模型的数据边缘概率，也就是模型证据，为

$$
p(\boldsymbol{\mathsf{t}})=\frac{1}{(2\pi)^{N/2}}\frac{b_0^{a_0}}{b_N^{a_N}}\frac{\Gamma(a_N)}{\Gamma(a_0)}\frac{|\mathbf{S}_N|^{1/2}}{|\mathbf{S}_0|^{1/2}}.
\tag{3.118}
$$

**3.24（⋆⋆）** 重做上一题，但这次使用如下形式的贝叶斯定理

$$
p(\boldsymbol{\mathsf{t}})=\frac{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)p(\mathbf{w},\beta)}{p(\mathbf{w},\beta\mid\boldsymbol{\mathsf{t}})}
\tag{3.119}
$$

然后代入先验分布、后验分布以及似然函数，推导结果（3.118）。

<!-- pdf-page: 198 -->
