# 第 4 章 单层网络：回归

<aside class="chapter-guide"><strong>本章导读</strong><p>本章用线性回归介绍单层神经网络的基本结构，并从似然函数、误差函数和贝叶斯方法研究参数学习与预测。单层模型便于解析，也为后续深层网络的讨论奠定基础。</p></aside>

<!-- pdf-page: 130 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/chapter-art.jpeg" alt="本章开篇的彩色抽象图案">
</figure>

本章以线性回归为框架，讨论神经网络背后的一些基本思想。我们在多项式曲线拟合中已经简要接触过线性回归（见第 1.2 节）。我们将看到，线性回归模型对应于一种简单的神经网络形式，只有一层可学习参数。单层网络在实践中的适用范围虽然很有限，但具有简单的解析性质，是引入许多核心概念的良好框架；这些概念将为后续章节讨论深层神经网络奠定基础。

<!-- pdf-page: 131 -->

## 4.1 线性回归

回归的目标是：给定由输入变量组成的 $D$ 维向量 $\mathbf{x}$，预测一个或多个连续目标变量 $\mathbf{t}$ 的值。通常，我们有包含 $N$ 个观测值 $\{\mathbf{x}_n\}$（$n=1,\ldots,N$）及相应目标值 $\{\mathbf{t}_n\}$ 的训练数据集，目标是预测新输入 $\mathbf{x}$ 对应的 $\mathbf{t}$。为此，构造函数 $y(\mathbf{x},\mathbf{w})$，它在新输入处的取值就是对相应目标值的预测；其中 $\mathbf{w}$ 是可从训练数据学习的参数向量。

最简单的回归模型是输入变量的线性组合：

$$
y(\mathbf{x},\mathbf{w})=w_0+w_1x_1+\cdots+w_Dx_D \tag{4.1}
$$

其中 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathrm T}$。“线性回归”有时专指这一形式的模型。该模型的关键性质是它关于参数 $w_0,\ldots,w_D$ 为线性函数。不过，它关于输入变量 $x_i$ 也为线性函数，这给模型带来很大限制。

### 4.1.1 基函数

考虑输入变量的固定非线性函数的线性组合，就可以扩展式 (4.1) 定义的模型类别：

$$
y(\mathbf{x},\mathbf{w})=w_0+\sum_{j=1}^{M-1}w_j\phi_j(\mathbf{x}) \tag{4.2}
$$

其中 $\phi_j(\mathbf{x})$ 称为基函数（basis function）。索引 $j$ 的最大值记为 $M-1$，因此模型共有 $M$ 个参数。

参数 $w_0$ 允许数据有任意固定偏移，有时称为偏置参数（bias parameter；不要与统计意义上的偏差混淆，见第 4.3 节）。通常，定义一个额外的虚设基函数 $\phi_0(\mathbf{x})$ 很方便，令其恒为 $\phi_0(\mathbf{x})=1$，于是式 (4.2) 变为

$$
y(\mathbf{x},\mathbf{w})=\sum_{j=0}^{M-1}w_j\phi_j(\mathbf{x})=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}) \tag{4.3}
$$

其中 $\mathbf{w}=(w_0,\ldots,w_{M-1})^{\mathrm T}$，$\boldsymbol{\phi}=(\phi_0,\ldots,\phi_{M-1})^{\mathrm T}$。模型 (4.3) 可以用神经网络图示表示，如图 4.1 所示。

使用非线性基函数，函数 $y(\mathbf{x},\mathbf{w})$ 就可以成为输入向量 $\mathbf{x}$ 的非线性函数。不过，形如式 (4.2) 的函数仍称为线性模型，因为它们关于 $\mathbf{w}$ 是线性的。正是参数上的线性性，极大地简化了对此类模型的分析；但它也造成了一些重要限制（见第 6.1 节）。

<!-- pdf-page: 132 -->

<figure id="fig-4-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-1.png" alt="输入基函数与单个输出节点之间由参数权重连接的单层网络">
  <figcaption>图 4.1：线性回归模型 (4.3) 可以表示为只含一层参数的简单神经网络图。每个基函数 $\phi_j(\mathbf{x})$ 由一个输入节点表示，其中实心节点对应“偏置”基函数 $\phi_0$；函数 $y(\mathbf{x},\mathbf{w})$ 由输出节点表示。每个参数 $w_j$ 以连接相应基函数和输出的线表示。</figcaption>
</figure>

深度学习出现以前，机器学习通常会对输入变量 $\mathbf{x}$ 进行某种固定的预处理，也称为特征提取（feature extraction），用一组基函数 $\{\phi_j(\mathbf{x})\}$ 来表示。目标是选择一组足够强大的基函数，使得到的学习任务可以用简单的网络模型解决。遗憾的是，除了最简单的应用，手工设计合适的基函数都非常困难。深度学习通过从数据集本身学习所需的非线性数据变换，避免了这一问题。

讨论多项式曲线拟合时，我们已经遇到过回归问题（见第 1 章）。对于单个输入变量 $x$，如果选择 $\phi_j(x)=x^j$ 作为基函数，那么多项式函数 (1.1) 就可以写成式 (4.3) 的形式。基函数还有许多其他选择，例如

$$
\phi_j(x)=\exp\left\{-\frac{(x-\mu_j)^2}{2s^2}\right\} \tag{4.4}
$$

其中 $\mu_j$ 控制基函数在输入空间中的位置，参数 $s$ 控制其空间尺度。这些函数通常称为“高斯”基函数，但不要求它们具有概率解释。特别是，归一化系数并不重要，因为这些基函数要乘以可学习参数 $w_j$。

另一种选择是 S 形基函数，其形式为

$$
\phi_j(x)=\sigma\left(\frac{x-\mu_j}{s}\right) \tag{4.5}
$$

其中 $\sigma(a)$ 是逻辑 sigmoid 函数（logistic sigmoid function），定义为

$$
\sigma(a)=\frac{1}{1+\exp(-a)}. \tag{4.6}
$$

也可以等价地使用双曲正切函数，因为 $\tanh(a)=2\sigma(2a)-1$。因此，在能够表示相同一类输入—输出函数的意义上，逻辑 sigmoid 函数的一般线性组合等价于双曲正切函数的一般线性组合（习题 4.3）。图 4.2 展示了以上几种基函数。

<!-- pdf-page: 133 -->

<figure id="fig-4-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-2.png" alt="多项式、高斯及 S 形基函数的三组彩色曲线">
  <figcaption>图 4.2：基函数示例：左侧为多项式，中间为式 (4.4) 形式的高斯基函数，右侧为式 (4.5) 形式的 S 形基函数。</figcaption>
</figure>

基函数还可以选择傅里叶基，这会得到正弦函数的展开式。每个基函数对应一个特定频率，并在空间上无限延伸。相反，局限于输入空间有限区域的基函数必然包含不同空间频率构成的频谱。在信号处理应用中，人们常关注同时在空间和频率上局部化的基函数，由此得到一类称为小波（wavelet）的函数（Ogden，1997；Mallat，1999；Vidakovic，1999）。小波还被定义为相互正交，以便简化应用。当输入值位于规则网格上，例如时间序列中连续的时间点或图像中的像素时，小波最为适用。

不过，本章的大部分讨论不依赖于基函数集合的选择，因此，除数值示例外，我们不指定基函数的具体形式。此外，为使记号简洁，我们将重点讨论单个目标变量 $t$ 的情形，不过也会简要说明处理多个目标变量所需的改动（见第 4.1.7 小节）。

### 4.1.2 似然函数

前面我们通过最小化平方和误差函数来解决多项式函数的数据拟合问题，也说明了在假设高斯噪声模型时，这个误差函数可由极大似然解引出（见第 1.2 节）。现在重新讨论这一问题，进一步考察最小二乘法及其与极大似然的关系。

和前面一样，假设目标变量 $t$ 由确定性函数 $y(\mathbf{x},\mathbf{w})$ 加上高斯噪声给出，即

$$
t=y(\mathbf{x},\mathbf{w})+\epsilon \tag{4.7}
$$

其中 $\epsilon$ 是均值为零、方差为 $\sigma^2$ 的高斯随机变量。因此可以写为

$$
p(t\mid\mathbf{x},\mathbf{w},\sigma^2)=\mathcal{N}(t\mid y(\mathbf{x},\mathbf{w}),\sigma^2). \tag{4.8}
$$

<!-- pdf-page: 134 -->

现在考虑输入数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 及对应的目标值 $t_1,\ldots,t_N$。我们把目标变量 $\{t_n\}$ 组成列向量，记作 $\mathbf{t}$；这里的字体用于区别单个多元目标的观测值，后者记为 $\boldsymbol{t}$。假设这些数据点从分布 (4.8) 中独立抽取，就得到关于可调参数 $\mathbf{w}$ 和 $\sigma^2$ 的似然函数：

$$
p(\mathbf{t}\mid\mathbf{X},\mathbf{w},\sigma^2)
=\prod_{n=1}^{N}\mathcal{N}(t_n\mid\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\sigma^2), \tag{4.9}
$$

这里使用了式 (4.3)。对似然函数取对数，并使用式 (2.49) 中一元高斯分布的标准形式，得到

$$
\begin{aligned}
\ln p(\mathbf{t}\mid\mathbf{X},\mathbf{w},\sigma^2)
&=\sum_{n=1}^{N}\ln\mathcal{N}(t_n\mid\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\sigma^2)\\
&=-\frac{N}{2}\ln\sigma^2-\frac{N}{2}\ln(2\pi)-\frac{1}{\sigma^2}E_D(\mathbf{w}),
\end{aligned} \tag{4.10}
$$

其中平方和误差函数定义为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2. \tag{4.11}
$$

确定 $\mathbf{w}$ 时，式 (4.10) 的前两项与 $\mathbf{w}$ 无关，可以视为常数。因此，正如前面看到的（见第 2.3.4 小节），在高斯噪声分布下最大化似然函数，等价于最小化平方和误差函数 (4.11)。

### 4.1.3 极大似然

写出似然函数后，就可以用极大似然法确定 $\mathbf{w}$ 和 $\sigma^2$。先考虑对 $\mathbf{w}$ 最大化。对数似然函数 (4.10) 关于 $\mathbf{w}$ 的梯度为

$$
\nabla_{\mathbf{w}}\ln p(\mathbf{t}\mid\mathbf{X},\mathbf{w},\sigma^2)
=\frac{1}{\sigma^2}\sum_{n=1}^{N}
\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}. \tag{4.12}
$$

令此梯度为零，得到

$$
0=\sum_{n=1}^{N}t_n\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}
-\mathbf{w}^{\mathrm T}\left(\sum_{n=1}^{N}\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm T}\right). \tag{4.13}
$$

解出 $\mathbf{w}$，得到

$$
\mathbf{w}_{\mathrm{ML}}=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{t}, \tag{4.14}
$$

<!-- pdf-page: 135 -->

这称为最小二乘问题的正规方程（normal equations）。这里 $\boldsymbol{\Phi}$ 是一个 $N\times M$ 矩阵，称为设计矩阵（design matrix），其元素为 $\Phi_{nj}=\phi_j(\mathbf{x}_n)$，因此

$$
\boldsymbol{\Phi}=
\begin{pmatrix}
\phi_0(\mathbf{x}_1)&\phi_1(\mathbf{x}_1)&\cdots&\phi_{M-1}(\mathbf{x}_1)\\
\phi_0(\mathbf{x}_2)&\phi_1(\mathbf{x}_2)&\cdots&\phi_{M-1}(\mathbf{x}_2)\\
\vdots&\vdots&\ddots&\vdots\\
\phi_0(\mathbf{x}_N)&\phi_1(\mathbf{x}_N)&\cdots&\phi_{M-1}(\mathbf{x}_N)
\end{pmatrix}. \tag{4.15}
$$

量

$$
\boldsymbol{\Phi}^{\dagger}\equiv(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T} \tag{4.16}
$$

称为矩阵 $\boldsymbol{\Phi}$ 的穆尔—彭罗斯伪逆（Moore–Penrose pseudo-inverse；Rao 和 Mitra，1971；Golub 和 Van Loan，1996）。它可视为把矩阵求逆的概念推广到非方阵。实际上，如果 $\boldsymbol{\Phi}$ 是可逆方阵，利用性质 $(\mathbf{A}\mathbf{B})^{-1}=\mathbf{B}^{-1}\mathbf{A}^{-1}$，可得 $\boldsymbol{\Phi}^{\dagger}\equiv\boldsymbol{\Phi}^{-1}$。

译注：式 (4.16) 中的显式逆要求设计矩阵 $\boldsymbol\Phi$ 满列秩，使 $\boldsymbol\Phi^{\mathrm T}\boldsymbol\Phi$ 可逆；仅有 $N\geqslant M$ 并不足够。一般矩阵的穆尔—彭罗斯伪逆可用奇异值分解定义，原式及后续使用该逆的等式需在满列秩条件下理解。

此时我们可以进一步理解偏置参数 $w_0$ 的作用。若显式写出偏置参数，误差函数 (4.11) 变为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}
\left\{t_n-w_0-\sum_{j=1}^{M-1}w_j\phi_j(\mathbf{x}_n)\right\}^2. \tag{4.17}
$$

令其对 $w_0$ 的导数为零，再解出 $w_0$，得到

$$
w_0=\bar{t}-\sum_{j=1}^{M-1}w_j\bar{\phi}_j \tag{4.18}
$$

其中定义

$$
\bar{t}=\frac{1}{N}\sum_{n=1}^{N}t_n,\qquad
\bar{\phi}_j=\frac{1}{N}\sum_{n=1}^{N}\phi_j(\mathbf{x}_n). \tag{4.19}
$$

因此，偏置 $w_0$ 补偿了训练集目标值的平均值与基函数值平均值的加权和之间的差异。

我们还可以对方差 $\sigma^2$ 最大化对数似然函数 (4.10)，得到

$$
\sigma_{\mathrm{ML}}^2=\frac{1}{N}\sum_{n=1}^{N}
\{t_n-\mathbf{w}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2, \tag{4.20}
$$

因此，方差参数的极大似然值就是目标值围绕回归函数的残差方差。

<!-- pdf-page: 136 -->

<figure id="fig-4-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-3.png" alt="目标向量投影到基函数张成子空间的最小二乘几何图">
  <figcaption>图 4.3：在以 $t_1,\ldots,t_N$ 为坐标轴的 $N$ 维空间中，最小二乘解的几何解释。把每个基函数 $\phi_j(\mathbf{x})$ 看作长度为 $N$、元素为 $\phi_j(\mathbf{x}_n)$ 的向量 $\boldsymbol{\varphi}_j$；将数据向量 $\mathbf{t}$ 正交投影到这些基函数张成的子空间，就得到最小二乘回归函数。</figcaption>
</figure>

### 4.1.4 最小二乘法的几何解释

现在考察最小二乘解的几何解释。为此，考虑一个以 $t_n$ 为坐标轴的 $N$ 维空间，$\mathbf{t}=(t_1,\ldots,t_N)^{\mathrm T}$ 是该空间中的一个向量。在 $N$ 个数据点上计算的每个基函数 $\phi_j(\mathbf{x}_n)$，也可表示为这个空间中的向量，记为 $\boldsymbol{\varphi}_j$，如图 4.3 所示。注意，$\boldsymbol{\varphi}_j$ 对应 $\boldsymbol{\Phi}$ 的第 $j$ 列，而 $\boldsymbol{\phi}(\mathbf{x}_n)$ 对应 $\boldsymbol{\Phi}$ 的第 $n$ 行的转置。若基函数数目 $M$ 小于数据点数目 $N$，则这 $M$ 个向量 $\boldsymbol{\varphi}_j$ 张成一个 $M$ 维线性子空间 $S$。定义 $N$ 维向量 $\mathbf{y}$，其第 $n$ 个元素为 $y(\mathbf{x}_n,\mathbf{w})$，$n=1,\ldots,N$。由于 $\mathbf{y}$ 是向量 $\boldsymbol{\varphi}_j$ 的任意线性组合，它可以位于这个 $M$ 维子空间的任意位置。平方和误差 (4.11) 等于 $\mathbf{y}$ 与 $\mathbf{t}$ 之间欧氏距离的平方，只差一个 $1/2$ 的因子。因此，$\mathbf{w}$ 的最小二乘解对应于位于子空间 $S$ 中、且最接近 $\mathbf{t}$ 的那个 $\mathbf{y}$。由图 4.3 可直观预期，这个解对应 $\mathbf{t}$ 在 $S$ 上的正交投影。事实确实如此：只要注意 $\mathbf{y}$ 的解由 $\boldsymbol{\Phi}\mathbf{w}_{\mathrm{ML}}$ 给出，并验证它具有正交投影形式即可（习题 4.4）。

实际计算时，如果 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 接近奇异矩阵，直接求解正规方程可能造成数值困难。特别是，当两个或更多基向量 $\boldsymbol{\varphi}_j$ 共线或近乎共线时，得到的参数值可能很大。处理真实数据集时，这种近似退化并不少见。可用奇异值分解（singular value decomposition，SVD）处理由此产生的数值困难（Deisenroth、Faisal 和 Ong，2020）。还要注意，加入正则化项即使存在退化，也能确保矩阵非奇异。

### 4.1.5 序贯学习

极大似然解 (4.14) 要一次处理整个训练集，称为批量方法。对于大型数据集，这可能耗费大量计算。如果数据集足够大，使用序贯算法（sequential algorithm）可能更合算；它也称为在线算法，逐个处理数据点，每次呈现一个数据点后更新模型参数。序贯学习也适合实时应用：数据观测值不断流入，而预测必须在看到所有数据点

<!-- pdf-page: 137 -->

之前作出。

可以运用随机梯度下降（stochastic gradient descent），也称序贯梯度下降，得到序贯学习算法（见第 7 章）。如果误差函数由各数据点的误差求和组成，即 $E=\sum_n E_n$，那么呈现第 $n$ 个数据点后，随机梯度下降算法按下式更新参数向量 $\mathbf{w}$：

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta\nabla E_n \tag{4.21}
$$

其中 $\tau$ 表示迭代次数，$\eta$ 是适当选取的学习率参数。$\mathbf{w}$ 的初值为某个起始向量 $\mathbf{w}^{(0)}$。对于平方和误差函数 (4.11)，更新式为

$$
\mathbf{w}^{(\tau+1)}
=\mathbf{w}^{(\tau)}+\eta\{t_n-\mathbf{w}^{(\tau)\mathrm T}\boldsymbol{\phi}_n\}\boldsymbol{\phi}_n, \tag{4.22}
$$

其中 $\boldsymbol{\phi}_n=\boldsymbol{\phi}(\mathbf{x}_n)$。这称为最小均方（least-mean-squares，LMS）算法。

### 4.1.6 正则化最小二乘法

前面我们已经介绍过：在误差函数中加入正则化项可以控制过拟合（见第 1.2 节），于是要最小化的总误差函数为

$$
E_D(\mathbf{w})+\lambda E_W(\mathbf{w}) \tag{4.23}
$$

其中 $\lambda$ 是正则化系数，控制依赖数据的误差 $E_D(\mathbf{w})$ 与正则化项 $E_W(\mathbf{w})$ 的相对重要性。一种最简单的正则化项，是权重向量各元素的平方和：

$$
E_W(\mathbf{w})=\frac{1}{2}\sum_j w_j^2=\frac{1}{2}\mathbf{w}^{\mathrm T}\mathbf{w}. \tag{4.24}
$$

若再考虑平方和误差函数

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2, \tag{4.25}
$$

则总误差函数为

$$
\frac{1}{2}\sum_{n=1}^{N}\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2
+\frac{\lambda}{2}\mathbf{w}^{\mathrm T}\mathbf{w}. \tag{4.26}
$$

在统计学中，这种正则化项是参数收缩方法（parameter shrinkage）的一个例子，因为它把参数值向零收缩。它的优点是误差函数仍为 $\mathbf{w}$ 的二次函数，因此可以求得闭式的精确最小值。具体来说，与前面一样，令式 (4.26) 对 $\mathbf{w}$ 的梯度为零，再解出 $\mathbf{w}$（习题 4.6），得到

$$
\mathbf{w}=(\lambda\mathbf{I}+\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{t}. \tag{4.27}
$$

这是最小二乘解 (4.14) 的一个简单扩展。

<!-- pdf-page: 138 -->

<figure id="fig-4-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-4.png" alt="多个基函数输入连接到多个输出节点的单层回归网络">
  <figcaption>图 4.4：把线性回归模型表示为具有单层连接的神经网络。每个基函数由一个节点表示，其中实心节点表示“偏置”基函数 $\phi_0$。各输出 $y_1,\ldots,y_K$ 也分别由节点表示。节点之间的连线表示相应的权重和偏置参数。</figcaption>
</figure>

### 4.1.7 多个输出

到目前为止，我们考察的都是只有一个目标变量 $t$ 的情形。在某些应用中，可能需要预测 $K>1$ 个目标变量，它们合称目标向量 $\boldsymbol{t}=(t_1,\ldots,t_K)^{\mathrm T}$。一种做法是为 $\boldsymbol{t}$ 的每个分量引入不同的基函数集合，得到多个相互独立的回归问题。但更常见的做法是用同一组基函数为目标向量的所有分量建模：

$$
\mathbf{y}(\mathbf{x},\mathbf{w})=\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}) \tag{4.28}
$$

其中 $\mathbf{y}$ 是 $K$ 维列向量，$\mathbf{W}$ 是 $M\times K$ 参数矩阵，$\boldsymbol{\phi}(\mathbf{x})$ 是 $M$ 维列向量，元素为 $\phi_j(\mathbf{x})$，且与前面一样，$\phi_0(\mathbf{x})=1$。这个模型同样可以表示为只有一层参数的神经网络，如图 4.4 所示。

假设目标向量的条件分布是以下各向同性高斯分布：

$$
p(\boldsymbol{t}\mid\mathbf{x},\mathbf{W},\sigma^2)
=\mathcal{N}(\boldsymbol{t}\mid\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}),\sigma^2\mathbf{I}). \tag{4.29}
$$

若有观测值 $\boldsymbol{t}_1,\ldots,\boldsymbol{t}_N$，可以把它们组成大小为 $N\times K$ 的矩阵 $\mathbf{T}$，其第 $n$ 行为 $\boldsymbol{t}_n^{\mathrm T}$。类似地，可把输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 组成矩阵 $\mathbf{X}$。于是对数似然函数为

$$
\begin{aligned}
\ln p(\mathbf{T}\mid\mathbf{X},\mathbf{W},\sigma^2)
&=\sum_{n=1}^{N}\ln\mathcal{N}(\boldsymbol{t}_n\mid\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n),\sigma^2\mathbf{I})\\
&=-\frac{NK}{2}\ln(2\pi\sigma^2)
-\frac{1}{2\sigma^2}\sum_{n=1}^{N}
\|\boldsymbol{t}_n-\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\|^2.
\end{aligned} \tag{4.30}
$$

和前面一样，对 $\mathbf{W}$ 最大化这个函数，得到

$$
\mathbf{W}_{\mathrm{ML}}=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{T} \tag{4.31}
$$

其中把输入特征向量 $\boldsymbol{\phi}(\mathbf{x}_1),\ldots,\boldsymbol{\phi}(\mathbf{x}_N)$ 组成矩阵 $\boldsymbol{\Phi}$。若分别考察各目标变量 $t_k$，则有

$$
\mathbf{w}_k=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{t}_k
=\boldsymbol{\Phi}^{\dagger}\mathbf{t}_k \tag{4.32}
$$

<!-- pdf-page: 139 -->

其中 $\mathbf{t}_k$ 是一个 $N$ 维列向量，分量为 $t_{nk}$（$n=1,\ldots,N$）。因此，不同目标变量的回归问题可以分开求解，只需计算一个供所有向量 $\mathbf{w}_k$ 共用的伪逆矩阵 $\boldsymbol{\Phi}^{\dagger}$。

将此方法推广到具有任意协方差矩阵的一般高斯噪声分布也很直接（习题 4.7）。它同样会分解为 $K$ 个独立的回归问题。这并不意外，因为参数 $\mathbf{W}$ 只定义高斯噪声分布的均值，而我们知道，多元高斯分布均值的极大似然解与协方差无关（见第 3.2.7 小节）。因此，从现在起，为简单起见，我们只考虑单个目标变量 $t$。

## 4.2 决策理论

我们把回归任务表述为对条件概率分布 $p(t\mid\mathbf{x})$ 建模，并选定了条件概率的具体形式：式 (4.8) 中的高斯分布，其依赖于 $\mathbf{x}$ 的均值 $y(\mathbf{x},\mathbf{w})$ 由参数 $\mathbf{w}$ 控制，方差由参数 $\sigma^2$ 给出。$\mathbf{w}$ 和 $\sigma^2$ 都可以通过极大似然法从数据中学习。结果是如下预测分布：

$$
p(t\mid\mathbf{x},\mathbf{w}_{\mathrm{ML}},\sigma_{\mathrm{ML}}^2)
=\mathcal{N}(t\mid y(\mathbf{x},\mathbf{w}_{\mathrm{ML}}),\sigma_{\mathrm{ML}}^2). \tag{4.33}
$$

预测分布表达了我们对新输入 $\mathbf{x}$ 所对应目标值 $t$ 的不确定性。不过，很多实际应用需要预测 $t$ 的一个具体值，而不是返回整个分布；尤其是必须采取具体行动的时候。例如，要确定治疗肿瘤的最佳放射剂量，模型预测了剂量上的概率分布，随后仍须利用这个分布决定实际使用的具体剂量。因此，任务分为两个阶段。第一阶段称为推断阶段（inference stage），使用训练数据确定预测分布 $p(t\mid\mathbf{x})$。第二阶段称为决策阶段（decision stage），根据这个预测分布确定具体数值 $f(\mathbf{x})$，它依赖输入向量 $\mathbf{x}$，并按照某个标准达到最优。可以通过最小化同时依赖预测分布 $p(t\mid\mathbf{x})$ 和 $f$ 的损失函数来做到这一点。

直觉上，我们可能选择条件分布的均值，即令 $f(\mathbf{x})=y(\mathbf{x},\mathbf{w}_{\mathrm{ML}})$。某些情形下这种直觉是对的，但另一些情形下可能给出很差的结果。因此，有必要将这一问题形式化，以理解它何时成立、需要什么假设。处理这一问题的框架称为决策理论（decision theory）。

假设真实值为 $t$ 时，我们选择 $f(\mathbf{x})$ 作为预测值。这样做会产生某种惩罚或代价，它由损失 $L(t,f(\mathbf{x}))$ 决定。当然，我们不知道真实的 $t$，所以不直接最小化 $L$，而是最小化平均损失，即期望损失：

<!-- pdf-page: 140 -->

<figure id="fig-4-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-5.png" alt="使期望平方损失最小的红色回归曲线与给定输入时的蓝色条件分布">
  <figcaption>图 4.5：使期望平方损失最小的回归函数 $f^\star(\mathbf{x})$，由条件分布 $p(t\mid\mathbf{x})$ 的均值给出。</figcaption>
</figure>

$$
\mathbb{E}[L]=\iint L(t,f(\mathbf{x}))p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t \tag{4.34}
$$

这里对输入变量和目标变量的分布求平均，并以其联合分布 $p(\mathbf{x},t)$ 为权重。回归问题中常用的一种损失函数是平方损失 $L(t,f(\mathbf{x}))=\{f(\mathbf{x})-t\}^2$。此时期望损失可写为

$$
\mathbb{E}[L]=\iint\{f(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t. \tag{4.35}
$$

注意不要混淆平方损失函数与前面引入的平方和误差函数。误差函数用于训练阶段设定参数，以确定条件概率分布 $p(t\mid\mathbf{x})$；损失函数则决定如何使用该条件分布，得到预测函数 $f(\mathbf{x})$，为每个 $\mathbf{x}$ 指定预测值。

我们的目标是选择 $f(\mathbf{x})$，使 $\mathbb{E}[L]$ 最小。若假设 $f(\mathbf{x})$ 是完全灵活的函数，就可以用变分法（见附录 B）形式化地求解：

$$
\frac{\delta\mathbb{E}[L]}{\delta f(\mathbf{x})}
=2\int\{f(\mathbf{x})-t\}p(\mathbf{x},t)\,\mathrm{d}t=0. \tag{4.36}
$$

解出 $f(\mathbf{x})$，并使用概率的加法法则和乘法法则，可得

$$
f^\star(\mathbf{x})
=\frac{1}{p(\mathbf{x})}\int t\,p(\mathbf{x},t)\,\mathrm{d}t
=\int t\,p(t\mid\mathbf{x})\,\mathrm{d}t
=\mathbb{E}_t[t\mid\mathbf{x}], \tag{4.37}
$$

它是在给定 $\mathbf{x}$ 条件下 $t$ 的条件均值，称为回归函数。图 4.5 展示了这个结果。它可直接推广到以向量 $\boldsymbol{t}$ 表示多个目标变量的情形，此时最优解是条件均值 $\mathbf{f}^\star(\mathbf{x})=\mathbb{E}_{\boldsymbol{t}}[\boldsymbol{t}\mid\mathbf{x}]$（习题 4.8）。对于式 (4.8) 形式的高斯条件分布，

<!-- pdf-page: 141 -->

其条件均值就是

$$
\mathbb{E}[t\mid\mathbf{x}]
=\int t\,p(t\mid\mathbf{x})\,\mathrm{d}t
=y(\mathbf{x},\mathbf{w}). \tag{4.38}
$$

使用变分法推导式 (4.37)，意味着我们是在所有可能的函数 $f(\mathbf{x})$ 中寻优。虽然实践中可实现的任何参数模型，其能表示的函数范围都有限，但后续章节将深入讨论的深层神经网络框架提供了非常灵活的函数类别，对许多实际目的而言，能以很高精度近似任意期望的函数。

也可以稍换一种方式推导这一结果，同时进一步了解回归问题的性质。已知最优解是条件期望，就可以如下展开平方项：

$$
\begin{aligned}
\{f(\mathbf{x})-t\}^2
&=\{f(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]+\mathbb{E}[t\mid\mathbf{x}]-t\}^2\\
&=\{f(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}^2
+2\{f(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}\{\mathbb{E}[t\mid\mathbf{x}]-t\}\\
&\quad+\{\mathbb{E}[t\mid\mathbf{x}]-t\}^2.
\end{aligned}
$$

这里为简洁起见，用 $\mathbb{E}[t\mid\mathbf{x}]$ 表示 $\mathbb{E}_t[t\mid\mathbf{x}]$。将展开式代入损失函数 (4.35)，对 $t$ 积分后，交叉项消失，得到

$$
\mathbb{E}[L]
=\int\{f(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}
+\int\operatorname{var}[t\mid\mathbf{x}]p(\mathbf{x})\,\mathrm{d}\mathbf{x}. \tag{4.39}
$$

待确定的函数 $f(\mathbf{x})$ 只出现在第一项中。当 $f(\mathbf{x})=\mathbb{E}[t\mid\mathbf{x}]$ 时，该项消失，从而达到最小值。这正是前面推导的结果，说明最优最小二乘预测量是条件均值。第二项是 $t$ 的分布方差对 $\mathbf{x}$ 取平均，代表目标数据的内在变异性，可视作噪声。因为它与 $f(\mathbf{x})$ 无关，所以它是损失函数不可约的最小值。

平方损失并非回归损失函数的唯一选择。这里简要讨论平方损失的一种简单推广，称为闵可夫斯基损失（Minkowski loss），其期望为

$$
\mathbb{E}[L_q]
=\iint|f(\mathbf{x})-t|^q p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t, \tag{4.40}
$$

当 $q=2$ 时，它化为期望平方损失。图 4.6 绘出了不同 $q$ 值下，$|f-t|^q$ 随 $f-t$ 的变化。$\mathbb{E}[L_q]$ 的最小值在 $q=2$ 时由条件均值给出，在 $q=1$ 时由条件中位数给出，在 $q\to0$ 时由条件众数给出（习题 4.12）。

注意，高斯噪声假设意味着给定 $\mathbf{x}$ 时 $t$ 的条件分布是单峰的，这对某些应用可能并不适当。在这种情形下，平方损失可能产生很差的结果，需要更复杂的方法。例如，可以通过使用混合

<!-- pdf-page: 142 -->

<!-- join-previous-paragraph -->

高斯分布得到多峰的条件分布；这类分布经常出现在逆问题的求解中（见第 6.5 节）。本节主要讨论回归问题的决策理论；下一章将针对分类任务建立类似概念（见第 5.2 节）。

<figure id="fig-4-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-6.png" alt="q 分别等于 0.3、1、2、10 时的四幅闵可夫斯基损失曲线">
  <figcaption>图 4.6：不同 $q$ 值下，量 $L_q=|f-t|^q$ 的图像。</figcaption>
</figure>

## 4.3 偏差—方差权衡

到目前为止，讨论用于回归的线性模型时，我们都假设基函数的形式和数目已给定。我们也看到，如果用规模有限的数据集训练复杂模型，极大似然法可能导致严重过拟合（见第 1.2 节）。但是，为避免过拟合而限制基函数数目，又会降低模型捕捉数据中有意义的重要趋势的灵活性。虽然正则化项可以控制多参数模型的过拟合，但这又引出一个问题：如何确定正则化系数 $\lambda$ 的适当取值？如果同时对权重向量 $\mathbf{w}$ 和正则化系数 $\lambda$ 最小化

<!-- pdf-page: 143 -->

正则化误差函数，显然不是正确做法，因为那样会得到 $\lambda=0$ 的无正则化解。

从频率学派视角考察模型复杂度问题很有启发性；这一视角称为偏差—方差权衡（bias–variance trade-off）。虽然我们会在线性基函数模型的语境中介绍这一概念，以便用简单例子说明，但后续讨论具有非常广泛的适用性。不过要注意，过拟合其实是极大似然法的一个不幸特性；在贝叶斯框架中对参数进行边缘化时，它不会出现（Bishop，2006）。

讨论回归问题的决策理论时，我们考虑了多种损失函数。在给定条件分布 $p(t\mid\mathbf{x})$ 后，每种损失函数都对应一个最优预测。常用选择是平方损失函数，此时最优预测为条件期望。将它记为 $h(\mathbf{x})$，有（见第 4.2 节）

$$
h(\mathbf{x})=\mathbb{E}[t\mid\mathbf{x}]
=\int t\,p(t\mid\mathbf{x})\,\mathrm{d}t. \tag{4.41}
$$

我们还看到，期望平方损失可写为

$$
\mathbb{E}[L]
=\int\{f(\mathbf{x})-h(\mathbf{x})\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}
+\iint\{h(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t. \tag{4.42}
$$

回顾：第二项与 $f(\mathbf{x})$ 无关，来自数据的内在噪声，代表期望损失可达到的最小值。第一项取决于函数 $f(\mathbf{x})$ 的选择，我们将寻找使它最小的 $f(\mathbf{x})$。它非负，所以能期望达到的最小值是零。如果有无限的数据（以及无限的计算资源），原则上就能以任意精度求出回归函数 $h(\mathbf{x})$，它就是 $f(\mathbf{x})$ 的最优选择。但实践中只有包含有限个数据点的有限数据集 $\mathcal{D}$，因此无法准确知道回归函数 $h(\mathbf{x})$。

如果用参数向量 $\mathbf{w}$ 控制的函数为 $h(\mathbf{x})$ 建模，贝叶斯视角会通过 $\mathbf{w}$ 上的后验分布表达模型的不确定性。频率学派则根据数据集 $\mathcal{D}$ 对 $\mathbf{w}$ 作点估计，并尝试用以下思想实验解释该估计的不确定性。设想有大量数据集，每个都包含 $N$ 个数据点，且都独立地从分布 $p(t,\mathbf{x})$ 中抽取。对任一给定数据集 $\mathcal{D}$，运行学习算法可得到预测函数 $f(\mathbf{x};\mathcal{D})$。这一数据集集合中的不同数据集会得到不同函数，因此也会得到不同的平方损失值。于是，通过对这一数据集集合取平均，评估特定学习算法的表现。

考虑式 (4.42) 第一项的被积函数，对某个数据集 $\mathcal{D}$，其形式为

$$
\{f(\mathbf{x};\mathcal{D})-h(\mathbf{x})\}^2. \tag{4.43}
$$

<!-- pdf-page: 144 -->

由于这个量依赖于具体数据集 $\mathcal{D}$，我们对数据集集合求其平均值。先在大括号中加上、再减去 $\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]$，随后展开，得到

$$
\begin{aligned}
&\{f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]
+\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2\\
&=\{f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]\}^2
+\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2\\
&\quad+2\{f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]\}
\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}.
\end{aligned} \tag{4.44}
$$

现在对该表达式关于 $\mathcal{D}$ 取期望。注意最后一项消失，因此

$$
\begin{aligned}
\mathbb{E}_{\mathcal{D}}\!\left[\{f(\mathbf{x};\mathcal{D})-h(\mathbf{x})\}^2\right]
&=
\underbrace{\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2}_{(\mathrm{bias})^2}\\
&\quad+
\underbrace{\mathbb{E}_{\mathcal{D}}\!\left[\{f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]\}^2\right]}_{\mathrm{variance}}.
\end{aligned} \tag{4.45}
$$

这里两项的标签分别是“偏差的平方”和“方差”。可见，$f(\mathbf{x};\mathcal{D})$ 与回归函数 $h(\mathbf{x})$ 之间的期望平方差可分解为两项。第一项称为偏差的平方，表示对所有数据集取平均后的预测与期望的回归函数之间的差异。第二项称为方差，衡量各个数据集给出的解围绕其平均值变化的程度，因此也衡量函数 $f(\mathbf{x};\mathcal{D})$ 对具体所选数据集的敏感度。稍后我们会用一个简单例子直观说明这些定义。

到目前为止，我们只考虑了单个输入值 $\mathbf{x}$。把上述展开式代入式 (4.42)，得到期望平方损失的分解：

$$
\text{expected loss}=(\mathrm{bias})^2+\mathrm{variance}+\mathrm{noise} \tag{4.46}
$$

其中“expected loss”“bias”“variance”“noise”依次表示期望损失、偏差、方差和噪声，并且

$$
(\mathrm{bias})^2
=\int\{\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]-h(\mathbf{x})\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x} \tag{4.47}
$$

$$
\mathrm{variance}
=\int\mathbb{E}_{\mathcal{D}}\!\left[\{f(\mathbf{x};\mathcal{D})-\mathbb{E}_{\mathcal{D}}[f(\mathbf{x};\mathcal{D})]\}^2\right]p(\mathbf{x})\,\mathrm{d}\mathbf{x} \tag{4.48}
$$

$$
\mathrm{noise}
=\iint\{h(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t \tag{4.49}
$$

此处的偏差和方差指积分后的量。

我们的目标是最小化期望损失，它已被分解为偏差的平方、方差和常数噪声项之和。后面将看到，偏差和方差之间存在权衡：很灵活的模型偏差低、方差高；相对僵硬的模型偏差高、方差低。预测能力最优的模型，是在偏差和方差之间达到最佳平衡的模型。可用前面介绍的正弦曲线数据集说明这一点（见第 1.2 节）。这里独立生成 100 个数据集，每个包含

<!-- pdf-page: 145 -->

从正弦曲线 $h(x)=\sin(2\pi x)$ 生成的 $N=25$ 个数据点。数据集以 $l=1,\ldots,L$ 编号，其中 $L=100$。对于每个数据集 $\mathcal{D}^{(l)}$，我们拟合一个模型，使用 $M=24$ 个高斯基函数和一个常数“偏置”基函数，共有 25 个参数。通过最小化正则化误差函数 (4.26)，得到图 4.7 所示的预测函数 $f^{(l)}(x)$。

图 4.7 的上排对应较大的正则化系数 $\lambda$：方差低（因为左图的红色曲线看起来相似），但偏差高（因为右图的两条曲线差异很大）。相反，在 $\lambda$ 较小的下排，方差很大（左图红色曲线变化很大），偏差却很小（平均模型拟合曲线与原始正弦函数吻合良好）。注意，虽然使用 $M=25$ 的复杂模型，对许多解求平均后却能很好地拟合回归函数，这表明平均可能是一种有益的方法。事实上，对多个解加权平均正是贝叶斯方法的核心；不过，贝叶斯方法是相对于参数的后验分布求平均，而不是相对于多个数据集求平均。

我们还可以定量考察这个例子的偏差—方差权衡。平均预测估计为

$$
\bar{f}(x)=\frac{1}{L}\sum_{l=1}^{L}f^{(l)}(x), \tag{4.50}
$$

积分后的偏差平方和方差分别为

$$
(\mathrm{bias})^2
=\frac{1}{N}\sum_{n=1}^{N}\{\bar{f}(x_n)-h(x_n)\}^2 \tag{4.51}
$$

$$
\mathrm{variance}
=\frac{1}{N}\sum_{n=1}^{N}\frac{1}{L}\sum_{l=1}^{L}
\{f^{(l)}(x_n)-\bar{f}(x_n)\}^2, \tag{4.52}
$$

这里用从分布 $p(x)$ 中抽取的数据点上的有限求和，近似对 $x$ 进行的加权积分。这两个量及其总和在图 4.8 中被绘为 $\ln\lambda$ 的函数。可以看到，$\lambda$ 较小时，模型会针对各数据集的噪声作精细调整，导致方差很大；相反，$\lambda$ 较大时，权重参数被拉向零，导致偏差很大。

注意，偏差—方差分解的实际价值有限，因为它基于对数据集集合取平均，而实践中只有一个观测到的数据集。如果有大量给定大小的独立训练集，最好把它们合并成一个更大的训练集；在给定模型复杂度下，这当然会降低过拟合程度。尽管如此，偏差—方差分解常能帮助我们理解模型复杂度问题。虽然这里是从回归问题角度介绍，但其基本直觉有广泛的适用性。

<!-- pdf-page: 146 -->

<figure id="fig-4-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-7.png" alt="三个正则化强度下，100 组正弦数据的多条拟合曲线及平均拟合与真实函数的比较">
  <figcaption>图 4.7：用第 1 章的正弦曲线数据，说明偏差和方差如何依赖于正则化参数 $\lambda$ 所控制的模型复杂度。共有 $L=100$ 个数据集，每个包含 $N=25$ 个数据点；模型中有 24 个高斯基函数，连同偏置参数，总参数数目为 $M=25$。左列显示不同 $\ln\lambda$ 值下模型对数据集的拟合结果（为清楚起见，仅显示 100 次拟合中的 20 次）。右列显示相应的 100 次拟合的平均值（红色），以及生成数据集的正弦函数（绿色）。</figcaption>
</figure>

<!-- pdf-page: 147 -->

<figure id="fig-4-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-04/fig-4-8.png" alt="偏差平方、方差、两者之和与测试误差随对数正则化系数变化的曲线">
  <figcaption>图 4.8：与图 4.7 的结果对应的偏差平方、方差及两者之和。图中也显示了大小为 1,000 个点的测试集上的平均误差。$(\mathrm{bias})^2+\mathrm{variance}$ 在约 $\ln\lambda=0.43$ 时达到最小，与测试数据误差最小时的取值相近。</figcaption>
  <p class="figure-translation">图内文字：(bias)² → 偏差平方；variance → 方差；(bias)² + variance → 偏差平方与方差之和；test error → 测试误差。</p>
</figure>

## 习题

**4.1（★）** 考虑式 (1.2) 给出的平方和误差函数，其中函数 $y(x,\mathbf{w})$ 由多项式 (1.1) 给出。证明使这个误差函数最小的系数 $\mathbf{w}=\{w_i\}$，由以下线性方程组的解给出：

$$
\sum_{j=0}^{M}A_{ij}w_j=T_i \tag{4.53}
$$

其中

$$
A_{ij}=\sum_{n=1}^{N}(x_n)^{i+j},\qquad
T_i=\sum_{n=1}^{N}(x_n)^it_n. \tag{4.54}
$$

这里，下标 $i$ 或 $j$ 表示分量的索引，而 $(x)^i$ 表示 $x$ 的 $i$ 次幂。

**4.2（★）** 写出类似于式 (4.53) 的耦合线性方程组，它由使式 (1.4) 的正则化平方和误差函数最小的系数 $w_i$ 满足。

**4.3（★）** 证明由下式定义的双曲正切函数

$$
\tanh(a)=\frac{e^a-e^{-a}}{e^a+e^{-a}} \tag{4.55}
$$

与式 (4.6) 定义的逻辑 sigmoid 函数满足

$$
\tanh(a)=2\sigma(2a)-1. \tag{4.56}
$$

由此证明，以下形式的逻辑 sigmoid 函数的一般线性组合

$$
y(x,\mathbf{w})=w_0+\sum_{j=1}^{M}w_j\sigma\left(\frac{x-\mu_j}{s}\right) \tag{4.57}
$$

<!-- pdf-page: 148 -->

等价于以下形式的双曲正切函数线性组合：

$$
y(x,\mathbf{u})=u_0+\sum_{j=1}^{M}u_j\tanh\left(\frac{x-\mu_j}{2s}\right), \tag{4.58}
$$

并求出把新参数 $\{u_1,\ldots,u_M\}$ 与原参数 $\{w_1,\ldots,w_M\}$ 联系起来的表达式。

**4.4（★★★）** 证明矩阵

$$
\boldsymbol{\Phi}(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T} \tag{4.59}
$$

可将任意向量 $\mathbf{v}$ 投影到 $\boldsymbol{\Phi}$ 的列张成的空间。利用这一结果证明，最小二乘解 (4.14) 对应于向量 $\mathbf{t}$ 在流形 $S$ 上的正交投影，如图 4.3 所示。

**4.5（★）** 考虑一个数据集，其中每个数据点 $t_n$ 都对应一个权重因子 $r_n>0$，于是平方和误差函数变为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}
r_n\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\}^2. \tag{4.60}
$$

求使这一误差函数最小的解 $\mathbf{w}^\star$ 的表达式。再从以下两个角度分别解释加权平方和误差函数：(i) 依赖于数据的噪声方差；(ii) 重复的数据点。

**4.6（★）** 令式 (4.26) 对 $\mathbf{w}$ 的梯度为零，证明线性回归的正则化平方和误差函数的精确最小值由式 (4.27) 给出。

**4.7（★★）** 考虑一个针对多元目标变量 $\boldsymbol{t}$ 的线性基函数回归模型，其高斯分布形式为

$$
p(\boldsymbol{t}\mid\mathbf{W},\boldsymbol{\Sigma})
=\mathcal{N}(\boldsymbol{t}\mid\mathbf{y}(\mathbf{x},\mathbf{W}),\boldsymbol{\Sigma}) \tag{4.61}
$$

其中

$$
\mathbf{y}(\mathbf{x},\mathbf{W})=\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}) \tag{4.62}
$$

另有一个训练数据集，其中包含输入基向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 及对应的目标向量 $\boldsymbol{t}_n$，$n=1,\ldots,N$。证明参数矩阵 $\mathbf{W}$ 的极大似然解 $\mathbf{W}_{\mathrm{ML}}$ 的每一列都由式 (4.14) 的形式给出，而式 (4.14) 是各向同性噪声分布时的解。注意，这一结果与协方差矩阵 $\boldsymbol{\Sigma}$ 无关。证明 $\boldsymbol{\Sigma}$ 的极大似然解为

$$
\boldsymbol{\Sigma}
=\frac{1}{N}\sum_{n=1}^{N}
\bigl(\boldsymbol{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\bigr)
\bigl(\boldsymbol{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\bigr)^{\mathrm T}. \tag{4.63}
$$

<!-- pdf-page: 149 -->

**4.8（★）** 将式 (4.35) 针对单个目标变量 $t$ 的平方损失函数推广到以向量 $\boldsymbol{t}$ 描述的多个目标变量：

$$
\mathbb{E}[L(\boldsymbol{t},\mathbf{f}(\mathbf{x}))]
=\iint\|\mathbf{f}(\mathbf{x})-\boldsymbol{t}\|^2p(\mathbf{x},\boldsymbol{t})\,\mathrm{d}\mathbf{x}\,\mathrm{d}\boldsymbol{t}. \tag{4.64}
$$

使用变分法，证明使这一期望损失最小的函数 $\mathbf{f}(\mathbf{x})$ 为

$$
\mathbf{f}(\mathbf{x})=\mathbb{E}_{\boldsymbol{t}}[\boldsymbol{t}\mid\mathbf{x}]. \tag{4.65}
$$

**4.9（★）** 展开式 (4.64) 中的平方项，推导与式 (4.39) 类似的结果，并由此证明：对于目标变量向量 $\boldsymbol{t}$，使期望平方损失最小的函数 $\mathbf{f}(\mathbf{x})$ 仍由式 (4.65) 形式的 $\boldsymbol{t}$ 的条件期望给出。

**4.10（★★）** 先仿照式 (4.39) 展开式 (4.64)，再重新推导式 (4.65) 的结果。

**4.11（★★）** 以下分布

$$
p(x\mid\sigma^2,q)
=\frac{q}{2(2\sigma^2)^{1/q}\Gamma(1/q)}
\exp\left\{-\frac{|x|^q}{2\sigma^2}\right\} \tag{4.66}
$$

是一元高斯分布的推广。其中 $\Gamma(x)$ 是伽马函数，定义为

$$
\Gamma(x)=\int_{-\infty}^{\infty}u^{x-1}e^{-u}\,\mathrm{d}u. \tag{4.67}
$$

译注：式 (4.67) 按原书保留。伽马函数在 $x>0$ 时的常用积分定义下限是 $0$；原书印成 $-\infty$，此时例如 $x=1$ 的积分会发散。下一个式 (4.68) 对密度的积分上下限则正确。

证明该分布已归一化，即

$$
\int_{-\infty}^{\infty}p(x\mid\sigma^2,q)\,\mathrm{d}x=1, \tag{4.68}
$$

并证明当 $q=2$ 时它化为高斯分布。考虑一个回归模型，其目标变量由 $t=y(\mathbf{x},\mathbf{w})+\epsilon$ 给出，其中 $\epsilon$ 是从分布 (4.66) 中抽取的随机噪声变量。证明对于观测到的输入向量数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 和对应目标变量 $\mathbf{t}=(t_1,\ldots,t_N)^{\mathrm T}$，关于 $\mathbf{w}$ 和 $\sigma^2$ 的对数似然函数为

$$
\ln p(\mathbf{t}\mid\mathbf{X},\mathbf{w},\sigma^2)
=-\frac{1}{2\sigma^2}\sum_{n=1}^{N}|y(\mathbf{x}_n,\mathbf{w})-t_n|^q
-\frac{N}{q}\ln(2\sigma^2)+\mathrm{const}, \tag{4.69}
$$

其中 $\mathrm{const}$ 表示与 $\mathbf{w}$ 和 $\sigma^2$ 都无关的项。注意，把它看作 $\mathbf{w}$ 的函数时，它就是第 4.2 节讨论的 $L_q$ 误差函数。

**4.12（★★）** 考虑式 (4.40) 给出的 $L_q$ 损失函数下，回归问题的期望损失。写出使 $\mathbb{E}[L_q]$ 最小的 $y(\mathbf{x})$ 必须满足的条件。证明当 $q=1$ 时，这个解是条件中位数，即函数 $y(\mathbf{x})$ 使 $t<y(\mathbf{x})$ 的概率质量与 $t\geqslant y(\mathbf{x})$ 的概率质量相同。还要证明，当 $q\to0$ 时，使期望 $L_q$ 损失最小的是条件众数，即对于每个 $\mathbf{x}$，函数 $y(\mathbf{x})$ 等于使 $p(t\mid\mathbf{x})$ 最大的 $t$ 值。
