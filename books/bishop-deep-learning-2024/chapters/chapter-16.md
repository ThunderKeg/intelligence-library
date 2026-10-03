<!-- pdf-page: 509 -->

# 第 16 章 连续潜变量

<aside class="chapter-guide"><strong>本章导读</strong><p>本章讨论连续潜变量如何解释高维数据中的低维结构。先从主成分分析（PCA）的几何定义出发，再进入概率形式、参数估计和非线性潜变量模型。理解“投影误差”与“生成数据的噪声”之间的关系，是连接这两部分的关键。</p></aside>

<figure class="chapter-opener">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/chapter-opener.png" alt="第 16 章彩色章首插图，题为 Continuous Latent Variables">
  <p class="figure-translation">图中文字：Continuous Latent Variables → 连续潜变量。</p>
</figure>

上一章讨论了高斯混合模型等具有离散潜变量的概率模型。现在探讨部分或全部潜变量为连续量的模型。研究这类模型的一个重要原因是：许多数据集中的数据点，分布在一个**流形**（manifold）附近；这个流形的维度远低于原始数据空间的维度（见第 6.1.3 节）。为理解它为何出现，考虑一个人工数据集：从 MNIST 数据集（LeCun et al.，1998）取一张 $64\times64$ 像素的手写数字灰度图，将其嵌入更大的 $100\times100$ 图像；扩展部分填充值为零，对应白色像素，并随机改变数字在图中的位置和朝向，如图 16.1 所示。得到的每张图像都对应于 $100\times100=10{,}000$ 维数据空间中的一个点。然而，在这样的图像数据集中，变化只有三个自由度：水平平移、竖直平移与

<!-- pdf-page: 510 -->
<!-- join-previous-paragraph -->

旋转。因此，数据点位于数据空间中内在维度为三的子空间上。注意，这个流形是非线性的。例如，当数字平移经过某个特定像素时，该像素的值会由零（白）变成一（黑），再变回零；它显然是数字位置的非线性函数。在这一例子中，平移和旋转参数是潜变量，因为我们只观测到图像向量，却不知道生成它们时使用了什么平移或旋转值。

<figure id="fig-16-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-1.png" alt="同一手写数字在更大图像区域中随机平移和旋转，形成五个样本">
  <figcaption>图 16.1：取一张手写数字图像，在较大的图像区域中对它随机平移、旋转，生成多个副本，得到合成数据集。每张生成图像都有 $100\times100=10{,}000$ 个像素。</figcaption>
</figure>

真实手写数字数据集还有更多自由度，例如缩放，以及同一人的书写变化、不同人的书写风格差异。不过，这些自由度的数量相对于数据空间的维度仍然很小。

在实践中，数据点不会精确地落在光滑的低维流形上；数据点偏离流形的部分可以解释为“噪声”。这自然带来一种生成式理解：先根据某个潜变量分布选取流形上的一点，再从给定潜变量时数据变量的某个条件分布中抽取噪声，生成观测数据点。

最简单的连续潜变量模型，假设潜变量和观测变量都服从高斯分布，且观测变量对潜变量状态的依赖是线性高斯形式（见第 11.1.4 节）。由此可以得到著名的**主成分分析**（principal component analysis，PCA）的一种概率形式，以及一个相关模型——**因子分析**。本章先按常规的非概率方式介绍 PCA（第 16.1 节），再说明 PCA 如何自然地成为线性高斯潜变量模型的极大似然解（第 16.2 节）。这种概率化改写有许多好处，例如可以用 EM 估计参数，有原则地扩展成 PCA 混合模型，以及使用贝叶斯形式让模型从数据中自动确定主成分个数（Bishop，2006）。本章也为含连续潜变量的非线性模型奠定基础，包括归一化流、变分自编码器和扩散模型。

<!-- pdf-page: 511 -->

<figure id="fig-16-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-2.png" alt="二维数据投影到主子空间的几何示意，绿色投影点的方差最大，蓝色投影误差最小">
  <figcaption>图 16.2：主成分分析寻找较低维的空间，称为主子空间（洋红线）。数据点（红点）正交投影到这个空间后，投影点（绿点）的方差最大。PCA 的另一种定义是使投影误差的平方和最小；蓝线表示这些误差。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf x_n$ 为原始数据点；$\widetilde{\mathbf x}_n$ 为投影点；$\mathbf u_1$ 为主方向；$x_1,x_2$ 为坐标轴。</p>
</figure>

## 16.1 主成分分析

**主成分分析**，简称 **PCA**，广泛用于降维、有损数据压缩、特征提取和数据可视化（Jolliffe，2002）。它也称 Kosambi–Karhunen–Loève 变换。

考虑把数据集正交投影到较低维的线性空间，即**主子空间**，如图 16.2 所示。PCA 可以定义为使投影后数据的方差最大的线性投影（Hotelling，1933）。等价地，也可以把它定义为使平均投影代价最小的线性投影；该代价是数据点到其投影点的均方距离（Pearson，1901）。下面依次考察这两种定义。

### 16.1.1 最大方差形式

考虑数据集 $\{\mathbf x_n\}$，其中 $n=1,\ldots,N$，$\mathbf x_n$ 是 $D$ 维欧几里得变量。目标是把数据投影到维度 $M<D$ 的空间，同时使投影数据的方差最大。暂时假定 $M$ 已知；本章后面会讨论如何由数据确定合适的 $M$。

先考虑投影到一维空间，即 $M=1$。用 $D$ 维向量 $\mathbf u_1$ 定义这一空间的方向。为方便起见，不失一般性地令它为单位向量，满足 $\mathbf u_1^{\mathsf T}\mathbf u_1=1$，因为我们只关心 $\mathbf u_1$ 的方向，不关心其长度。每个数据点 $\mathbf x_n$ 投影为标量 $\mathbf u_1^{\mathsf T}\mathbf x_n$。投影后数据的均值是 $\mathbf u_1^{\mathsf T}\bar{\mathbf x}$，其中 $\bar{\mathbf x}$ 为样本均值：

$$
\bar{\mathbf x}=\frac{1}{N}\sum_{n=1}^{N}\mathbf x_n. \tag{16.1}
$$

<!-- pdf-page: 512 -->

投影数据的方差为

$$
\frac{1}{N}\sum_{n=1}^{N}\left(\mathbf u_1^{\mathsf T}\mathbf x_n-\mathbf u_1^{\mathsf T}\bar{\mathbf x}\right)^2
=\mathbf u_1^{\mathsf T}\mathbf S\mathbf u_1, \tag{16.2}
$$

其中 $\mathbf S$ 是数据协方差矩阵，定义为

$$
\mathbf S=\frac{1}{N}\sum_{n=1}^{N}(\mathbf x_n-\bar{\mathbf x})(\mathbf x_n-\bar{\mathbf x})^{\mathsf T}. \tag{16.3}
$$

现在要对 $\mathbf u_1$ 最大化投影方差 $\mathbf u_1^{\mathsf T}\mathbf S\mathbf u_1$。显然，必须对优化加约束，防止 $\lVert\mathbf u_1\rVert\to\infty$。约束来自单位化条件 $\mathbf u_1^{\mathsf T}\mathbf u_1=1$。为施加该约束，引入拉格朗日乘子 $\lambda_1$（见附录 C），转而无约束地最大化

$$
\mathbf u_1^{\mathsf T}\mathbf S\mathbf u_1
+\lambda_1\left(1-\mathbf u_1^{\mathsf T}\mathbf u_1\right). \tag{16.4}
$$

对 $\mathbf u_1$ 求导并令其为零，可知该量在以下条件成立时达到驻点：

$$
\mathbf S\mathbf u_1=\lambda_1\mathbf u_1. \tag{16.5}
$$

也就是说，$\mathbf u_1$ 必须是 $\mathbf S$ 的特征向量。两边左乘 $\mathbf u_1^{\mathsf T}$，再利用 $\mathbf u_1^{\mathsf T}\mathbf u_1=1$，便知方差等于

$$
\mathbf u_1^{\mathsf T}\mathbf S\mathbf u_1=\lambda_1. \tag{16.6}
$$

因此，让 $\mathbf u_1$ 等于最大特征值 $\lambda_1$ 对应的特征向量，方差便达到最大。这个特征向量称为**第一主成分**。

可以逐个定义其他主成分：每选一个新方向，都要求它与此前选取的方向正交，并使该方向上的投影方差在所有候选方向中最大。一般地，若投影空间维度为 $M$，使投影数据方差最大的线性投影由数据协方差矩阵 $\mathbf S$ 的 $M$ 个特征向量 $\mathbf u_1,\ldots,\mathbf u_M$ 定义，它们对应于最大的 $M$ 个特征值 $\lambda_1,\ldots,\lambda_M$。利用数学归纳法很容易证明这一点（习题 16.1）。

综上，PCA 先计算数据集的均值 $\bar{\mathbf x}$ 和协方差矩阵 $\mathbf S$，再找出 $\mathbf S$ 最大的 $M$ 个特征值及相应特征向量。特征值和特征向量的计算算法，以及特征向量分解的更多定理，可参见 Golub 和 Van Loan（1996）。对 $D\times D$ 矩阵求完整特征向量分解的计算成本是 $O(D^3)$。如果只计划投影到前 $M$ 个主成分，就只需求前 $M$ 个特征值及特征向量。这可以用更高效的幂法（Golub 和 Van Loan，1996）求得，其复杂度约为 $O(MD^2)$；也可以使用 EM 算法（见第 16.3.2 节）。

<!-- pdf-page: 513 -->

### 16.1.2 最小误差形式

现在讨论 PCA 的另一种形式：使投影误差最小。为此，引入一组完备的 $D$ 维标准正交基向量 $\{\mathbf u_i\}$（$i=1,\ldots,D$；见附录 A），满足

$$
\mathbf u_i^{\mathsf T}\mathbf u_j=\delta_{ij}. \tag{16.7}
$$

由于这组基是完备的，每个数据点都能由基向量的线性组合精确表示：

$$
\mathbf x_n=\sum_{i=1}^{D}\alpha_{ni}\mathbf u_i, \tag{16.8}
$$

系数 $\alpha_{ni}$ 因数据点而异。这相当于把坐标系旋转到由 $\{\mathbf u_i\}$ 定义的新坐标系，原来的 $D$ 个分量 $\{x_{n1},\ldots,x_{nD}\}$ 由等价的一组 $\{\alpha_{n1},\ldots,\alpha_{nD}\}$ 代替。两边与 $\mathbf u_j$ 作内积，并利用正交归一性质，得到 $\alpha_{nj}=\mathbf x_n^{\mathsf T}\mathbf u_j$，因此不失一般性地可写为

$$
\mathbf x_n=\sum_{i=1}^{D}(\mathbf x_n^{\mathsf T}\mathbf u_i)\mathbf u_i. \tag{16.9}
$$

不过，我们的目标是只用 $M<D$ 个变量表示数据点，将其投影到较低维子空间，近似每个数据点 $\mathbf x_n$。不失一般性，可用前 $M$ 个基向量表示这一 $M$ 维线性子空间，把 $\mathbf x_n$ 近似为

$$
\widetilde{\mathbf x}_n=\sum_{i=1}^{M}z_{ni}\mathbf u_i+\sum_{i=M+1}^{D}b_i\mathbf u_i, \tag{16.10}
$$

其中 $\{z_{ni}\}$ 随数据点变化，而 $\{b_i\}$ 对所有数据点都是相同的常数。可以自由选择 $\{\mathbf u_i\}$、$\{z_{ni}\}$ 和 $\{b_i\}$，使降维引入的误差最小。这里用原始数据点 $\mathbf x_n$ 与其近似值 $\widetilde{\mathbf x}_n$ 之间的平方距离作为误差，再对数据集取平均。目标是最小化

$$
J=\frac{1}{N}\sum_{n=1}^{N}\lVert\mathbf x_n-\widetilde{\mathbf x}_n\rVert^2. \tag{16.11}
$$

先对 $\{z_{ni}\}$ 最小化。将式 (16.10) 代入 $J$，对 $z_{nj}$ 求导并令其为零，再利用正交归一条件，可得

$$
z_{nj}=\mathbf x_n^{\mathsf T}\mathbf u_j, \tag{16.12}
$$

<!-- pdf-page: 514 -->

其中 $j=1,\ldots,M$。类似地，对 $b_i$ 求导并令导数为零，再利用正交归一关系，得到

$$
b_j=\bar{\mathbf x}^{\mathsf T}\mathbf u_j, \tag{16.13}
$$

其中 $j=M+1,\ldots,D$。将 $z_{ni}$ 和 $b_i$ 代回式 (16.10)，并利用一般展开式 (16.9)，得到

$$
\mathbf x_n-\widetilde{\mathbf x}_n
=\sum_{i=M+1}^{D}\left[(\mathbf x_n-\bar{\mathbf x})^{\mathsf T}\mathbf u_i\right]\mathbf u_i. \tag{16.14}
$$

由此可见，从 $\mathbf x_n$ 指向 $\widetilde{\mathbf x}_n$ 的位移向量，位于与主子空间正交的空间中，因为它是 $i=M+1,\ldots,D$ 的 $\{\mathbf u_i\}$ 的线性组合，如图 16.2 所示。这符合预期：投影点 $\widetilde{\mathbf x}_n$ 必须位于主子空间内，又可以在该空间内自由移动，所以误差最小的点就是正交投影点。

因此，误差 $J$ 可以只用 $\{\mathbf u_i\}$ 表示为

$$
J=\frac{1}{N}\sum_{n=1}^{N}\sum_{i=M+1}^{D}
\left(\mathbf x_n^{\mathsf T}\mathbf u_i-\bar{\mathbf x}^{\mathsf T}\mathbf u_i\right)^2
=\sum_{i=M+1}^{D}\mathbf u_i^{\mathsf T}\mathbf S\mathbf u_i. \tag{16.15}
$$

还须对 $\{\mathbf u_i\}$ 最小化 $J$。这同样是有约束的优化，否则会得到毫无意义的 $\mathbf u_i=0$。约束来自正交归一条件；稍后会看到，解可用协方差矩阵的特征向量分解表示。在正式求解前，先考虑二维数据空间 $D=2$、一维主子空间 $M=1$，以便建立直觉。须选择方向 $\mathbf u_2$，在 $\mathbf u_2^{\mathsf T}\mathbf u_2=1$ 的约束下使 $J=\mathbf u_2^{\mathsf T}\mathbf S\mathbf u_2$ 最小。用拉格朗日乘子 $\lambda_2$ 施加约束，考察

$$
\widetilde J=\mathbf u_2^{\mathsf T}\mathbf S\mathbf u_2
+\lambda_2(1-\mathbf u_2^{\mathsf T}\mathbf u_2). \tag{16.16}
$$

对 $\mathbf u_2$ 求导并令其为零，得到 $\mathbf S\mathbf u_2=\lambda_2\mathbf u_2$，因此 $\mathbf u_2$ 是 $\mathbf S$ 的特征向量，其特征值为 $\lambda_2$。任何特征向量都对应误差的一个驻点。把 $\mathbf u_2$ 的解代回误差式，得到 $J=\lambda_2$。所以，选择两个特征值中较小者对应的特征向量作为 $\mathbf u_2$，$J$ 最小；主子空间则应沿较大特征值对应的特征向量。这与直觉一致：若要使平均投影距离平方最小，主成分子空间应经过数据点的均值，并沿方差最大的方向。如果

<!-- pdf-page: 515 -->
<!-- join-previous-paragraph -->

两个特征值相等，则选择任何主方向都会得到相同的 $J$。

对于任意 $D$ 和 $M<D$，使 $J$ 最小的一般解是选取协方差矩阵的特征向量 $\{\mathbf u_i\}$（习题 16.2），满足

$$
\mathbf S\mathbf u_i=\lambda_i\mathbf u_i, \tag{16.17}
$$

其中 $i=1,\ldots,D$，并像通常一样令特征向量 $\{\mathbf u_i\}$ 标准正交。相应的误差值为

$$
J=\sum_{i=M+1}^{D}\lambda_i, \tag{16.18}
$$

即与主子空间正交的那些特征向量所对应的特征值之和。因此，令这些向量对应于最小的 $D-M$ 个特征值，$J$ 便最小；定义主子空间的向量则对应于最大的 $M$ 个特征值。

虽然以上讨论假设 $M<D$，当 $M=D$ 时 PCA 分析仍然成立，只是没有降维，而仅仅把坐标轴旋转到与主成分对齐。

最后，还有一种相关的线性降维技术称为**典型相关分析**（canonical correlation analysis；Hotelling，1936；Bach and Jordan，2002）。PCA 只涉及一个随机变量，而典型相关分析涉及两个或更多变量，试图找到一对具有较高交叉相关性的线性子空间，使其中一个子空间的每个分量与另一子空间的一个分量相关。其解可以表示为一个广义特征向量问题。

### 16.1.3 数据压缩

PCA 的一种应用是数据压缩，可以用手写数字图像数据集来说明。协方差矩阵的每个特征向量都位于原始 $D$ 维空间，因此可以将它表示成与数据点相同尺寸的图像。图 16.3 展示了均值图像、前四个特征向量及其对应特征值。

图 16.4(a) 给出按降序排列的完整特征值谱。选定某个 $M$ 后，误差 $J$ 等于从第 $M+1$ 个到第 $D$ 个特征值之和；图 16.4(b) 绘出了不同 $M$ 下的 $J$。

把式 (16.12) 和 (16.13) 代入式 (16.10)，可将 PCA 近似

<!-- pdf-page: 516 -->
<!-- join-previous-paragraph -->

数据向量 $\mathbf x_n$ 的结果写成

<figure id="fig-16-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-3.png" alt="手写数字 3 图像数据的均值图像与前四个 PCA 特征向量图像">
  <figcaption>图 16.3：对 6,000 张 $28\times28$ 像素手写数字“3”的图像应用 PCA：展示均值向量 $\bar{\mathbf x}$、前四个特征向量 $\mathbf u_1,\ldots,\mathbf u_4$ 及其对应特征值。</figcaption>
  <p class="figure-translation">图内文字：Mean → 均值；$\lambda_1=3.4\cdot10^5$、$\lambda_2=2.8\cdot10^5$、$\lambda_3=2.4\cdot10^5$、$\lambda_4=1.6\cdot10^5$ → 前四个特征值。</p>
</figure>

$$
\widetilde{\mathbf x}_n
=\sum_{i=1}^{M}(\mathbf x_n^{\mathsf T}\mathbf u_i)\mathbf u_i
+\sum_{i=M+1}^{D}(\bar{\mathbf x}^{\mathsf T}\mathbf u_i)\mathbf u_i, \tag{16.19}
$$

也可写为

$$
\widetilde{\mathbf x}_n
=\bar{\mathbf x}+\sum_{i=1}^{M}
\left(\mathbf x_n^{\mathsf T}\mathbf u_i-\bar{\mathbf x}^{\mathsf T}\mathbf u_i\right)\mathbf u_i, \tag{16.20}
$$

这里利用了由 $\{\mathbf u_i\}$ 的完备性得到的关系

$$
\bar{\mathbf x}=\sum_{i=1}^{D}(\bar{\mathbf x}^{\mathsf T}\mathbf u_i)\mathbf u_i. \tag{16.21}
$$

这表示数据集被压缩：每个数据点原先是 $D$ 维向量 $\mathbf x_n$，现在由分量为 $\mathbf x_n^{\mathsf T}\mathbf u_i-\bar{\mathbf x}^{\mathsf T}\mathbf u_i$ 的 $M$ 维向量代替。$M$ 越小，压缩程度越高。图 16.5 给出手写数字数据中一些点的 PCA 重建结果。

### 16.1.4 数据白化

PCA 的另一种用途是数据预处理。此时目的不是降维，而是变换数据集，使它的某些性质标准化，以便后续机器学习算法能更好地处理数据。通常，当原始变量采用不同计量单位，或各变量的变化幅度差别很大时，需要这么做。例如在“老忠实”数据集中，两次喷发间隔的时间通常比单次喷发的持续时间大一个数量级。对这份数据应用 K 均值算法时（见第 15.1 节），我们先对各变量分别做线性重新缩放，使它们的均值为零，

<!-- pdf-page: 517 -->
<!-- join-previous-paragraph -->

方差为一。这称为对数据做**标准化**。标准化数据的协方差矩阵元素为

<figure id="fig-16-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-4.png" alt="手写数字数据的 PCA 特征值谱及按主成分维度计算的丢弃特征值之和">
  <figcaption>图 16.4：(a) 图 16.3 的手写数字数据集的特征值谱；(b) 被丢弃的特征值之和，即把数据投影到维度为 $M$ 的主成分子空间后引入的平方和误差 $J$。</figcaption>
</figure>

$$
\rho_{ij}=\frac{1}{N}\sum_{n=1}^{N}
\frac{(x_{ni}-\bar x_i)}{\sigma_i}
\frac{(x_{nj}-\bar x_j)}{\sigma_j}, \tag{16.22}
$$

其中 $\sigma_i$ 是 $x_i$ 的标准差。这个矩阵称为原始数据的**相关矩阵**。若数据的两个分量 $x_i$、$x_j$ 完全相关，则 $\rho_{ij}=1$；若它们不相关，则 $\rho_{ij}=0$。

不过，利用 PCA 可以进一步归一化数据，使其均值为零、协方差为单位矩阵，从而消除不同变量之间的相关性。

<figure id="fig-16-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-5.png" alt="原始手写数字 3 与保留一、十、五十、二百五十个主成分后的 PCA 重建图">
  <figcaption>图 16.5：手写数字数据集中的一张图像，以及保留不同数量 $M$ 的主成分后的 PCA 重建结果。$M$ 增大，重建更准确；当 $M=D=28\times28=784$ 时，重建将完全准确。</figcaption>
  <p class="figure-translation">图内文字：Original → 原图；$M=1,10,50,250$ → 分别保留 1、10、50、250 个主成分。</p>
</figure>

<!-- pdf-page: 518 -->

<figure id="fig-16-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-6.png" alt="老忠实间歇泉数据的原始、标准化和白化三种散点图">
  <figcaption>图 16.6：“老忠实”数据经过线性预处理的效果。左图为原始数据；中图为各变量分别标准化到零均值、单位方差后的结果，还画出标准化数据集的主轴，主轴范围为 $\pm\lambda_i^{1/2}$；右图为白化后零均值、单位协方差的数据。</figcaption>
</figure>

为此，先把特征向量方程 (16.17) 写成

$$
\mathbf S\mathbf U=\mathbf U\mathbf L, \tag{16.23}
$$

其中 $\mathbf L$ 是元素为 $\lambda_i$ 的 $D\times D$ 对角矩阵，$\mathbf U$ 是以 $\mathbf u_i$ 为列的 $D\times D$ 正交矩阵。然后对每个数据点 $\mathbf x_n$ 定义变换值

$$
\mathbf y_n=\mathbf L^{-1/2}\mathbf U^{\mathsf T}(\mathbf x_n-\bar{\mathbf x}), \tag{16.24}
$$

其中 $\bar{\mathbf x}$ 是式 (16.1) 的样本均值。显然，$\{\mathbf y_n\}$ 的均值为零，协方差为单位矩阵，因为

$$
\begin{aligned}
\frac{1}{N}\sum_{n=1}^{N}\mathbf y_n\mathbf y_n^{\mathsf T}
&=\frac{1}{N}\sum_{n=1}^{N}\mathbf L^{-1/2}\mathbf U^{\mathsf T}
(\mathbf x_n-\bar{\mathbf x})(\mathbf x_n-\bar{\mathbf x})^{\mathsf T}
\mathbf U\mathbf L^{-1/2}\\
&=\mathbf L^{-1/2}\mathbf U^{\mathsf T}\mathbf S\mathbf U\mathbf L^{-1/2}
=\mathbf L^{-1/2}\mathbf L\mathbf L^{-1/2}=\mathbf I.
\end{aligned} \tag{16.25}
$$

这种操作称为对数据做**白化**（whitening）或“球化”（sphering）。图 16.6 用“老忠实”数据集说明它（见第 15.1 节）。

### 16.1.5 高维数据

在某些 PCA 应用中，数据点数量小于数据空间的维度。例如，对数百张图像做 PCA，每张图像可能对应于数百万维空间中的一个向量，因为每个像素有三个颜色值。在 $D$ 维空间中，$N<D$ 个点张成的线性子空间维度最多是 $N-1$，因此把 $M$ 取到大于 $N-1$ 没有多少意义。事实上，执行 PCA 后，至少有 $D-N+1$ 个特征值

<!-- pdf-page: 519 -->
<!-- join-previous-paragraph -->

为零；相应特征向量方向上的数据方差也是零。而常见的 $D\times D$ 矩阵特征向量计算算法需要 $O(D^3)$ 成本，因此对于上述图像例子，直接应用 PCA 在计算上不可行。

可以这样解决。先定义中心化的 $N\times D$ 数据矩阵 $\mathbf X$，其第 $n$ 行为 $(\mathbf x_n-\bar{\mathbf x})^{\mathsf T}$。协方差矩阵 (16.3) 可写为 $\mathbf S=N^{-1}\mathbf X^{\mathsf T}\mathbf X$，相应的特征向量方程变成

$$
\frac{1}{N}\mathbf X^{\mathsf T}\mathbf X\mathbf u_i=\lambda_i\mathbf u_i. \tag{16.26}
$$

两边左乘 $\mathbf X$，得到

$$
\frac{1}{N}\mathbf X\mathbf X^{\mathsf T}(\mathbf X\mathbf u_i)=\lambda_i(\mathbf X\mathbf u_i). \tag{16.27}
$$

若定义 $\mathbf v_i=\mathbf X\mathbf u_i$，就有

$$
\frac{1}{N}\mathbf X\mathbf X^{\mathsf T}\mathbf v_i=\lambda_i\mathbf v_i, \tag{16.28}
$$

这是 $N\times N$ 矩阵 $N^{-1}\mathbf X\mathbf X^{\mathsf T}$ 的特征向量方程。它与原协方差矩阵有相同的 $N-1$ 个非零特征值；原协方差矩阵另外还有 $D-N+1$ 个零特征值。因此，我们可以在较低维空间求解特征向量问题，计算成本从 $O(D^3)$ 降为 $O(N^3)$。为求原始空间中的特征向量，在式 (16.28) 两边左乘 $\mathbf X^{\mathsf T}$：

$$
\frac{1}{N}\mathbf X^{\mathsf T}\mathbf X(\mathbf X^{\mathsf T}\mathbf v_i)
=\lambda_i(\mathbf X^{\mathsf T}\mathbf v_i). \tag{16.29}
$$

可见，$\mathbf X^{\mathsf T}\mathbf v_i$ 是 $\mathbf S$ 对应特征值 $\lambda_i$ 的特征向量，但不一定已归一化。令 $\mathbf u_i\propto\mathbf X^{\mathsf T}\mathbf v_i$，再用常数缩放，使 $\lVert\mathbf u_i\rVert=1$；若已将 $\mathbf v_i$ 归一化为单位长度，就得到（习题 16.3）

$$
\mathbf u_i=\frac{1}{(N\lambda_i)^{1/2}}\mathbf X^{\mathsf T}\mathbf v_i. \tag{16.30}
$$

综上，先计算 $\mathbf X\mathbf X^{\mathsf T}$，求它的特征值和特征向量，再用式 (16.30) 计算原始数据空间中的特征向量。

<!-- pdf-page: 520 -->

## 16.2 概率潜变量

上一节已看到，PCA 可以定义为把数据线性投影到一个比原始数据空间维度更低的子空间。每个数据点都投影到式 (16.12) 的量 $z_{nj}$ 的唯一取值，因此可以把它们视为确定性的潜变量。为引入并说明**概率型连续潜变量**，现在证明 PCA 也可以表示成概率潜变量模型的极大似然解。这种改写称为**概率 PCA**，与常规 PCA 相比有以下优点：

- 概率 PCA 模型是一种受约束的高斯分布形式，可以限制自由参数的数量，同时仍捕捉数据集中的主要相关性。
- 可以为 PCA 推导 EM 算法：当只需要少数几个前导特征向量时，它在计算上很高效，而且不必把数据协方差矩阵作为中间结果求出来（见第 16.3.2 节）。
- 概率模型与 EM 的结合能够处理数据集中的缺失值。
- 可以有原则地构造概率 PCA 模型的混合模型，并用 EM 算法训练。
- 似然函数的存在使概率 PCA 可直接与其他概率密度模型比较。相比之下，常规 PCA 会对靠近主子空间的点给出较低的重建代价，即使它们距离训练数据任意远。
- 概率 PCA 可以描述类别条件密度，因此可用于分类。
- 概率 PCA 可按生成模型运行，从分布中采样。
- 概率 PCA 为贝叶斯 PCA 提供基础；在贝叶斯形式下，主子空间的维度可由数据自动确定（Bishop，2006）。

将 PCA 表示为概率模型的形式，由 Tipping 和 Bishop（1997、1999）与 Roweis（1998）独立提出。稍后会看到，它与因子分析密切相关（Basilevsky，1994）。

### 16.2.1 生成模型

概率 PCA 是线性高斯框架（见第 11.1.4 节）的一个简单例子：全部边缘分布与条件分布都是高斯分布。构造概率 PCA 时，先为主成分子空间引入一个显式的 $M$ 维潜变量

<!-- pdf-page: 521 -->
<!-- join-previous-paragraph -->

$\mathbf z$。接着，为潜变量定义高斯先验分布 $p(\mathbf z)$，再定义在给定潜变量取值时，$D$ 维观测变量 $\mathbf x$ 的高斯条件分布 $p(\mathbf x\mid\mathbf z)$。具体而言，$\mathbf z$ 的先验是零均值、单位协方差的高斯分布：

$$
p(\mathbf z)=\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I). \tag{16.31}
$$

同样，给定潜变量 $\mathbf z$ 时，观测变量 $\mathbf x$ 的条件分布也是高斯分布：

$$
p(\mathbf x\mid\mathbf z)=\mathcal N(\mathbf x\mid\mathbf W\mathbf z+\boldsymbol\mu,\sigma^2\mathbf I). \tag{16.32}
$$

其中，$\mathbf x$ 的均值是 $\mathbf z$ 的一般线性函数，由 $D\times M$ 矩阵 $\mathbf W$ 和 $D$ 维向量 $\boldsymbol\mu$ 决定。请注意，条件分布对 $\mathbf x$ 的各分量可分解成乘积；换句话说，这是一个朴素贝叶斯模型的例子（见第 11.2.3 节）。很快我们会看到，$\mathbf W$ 的列在数据空间中张成一个线性子空间，它对应于主子空间。模型中的另一个参数是标量 $\sigma^2$，决定条件分布的方差。令潜变量分布 $p(\mathbf z)$ 为零均值、单位协方差的高斯分布不会失去一般性，因为采用更一般的高斯分布会得到一个等价的概率模型（习题 16.4）。

也可以从生成过程来理解概率 PCA 模型：先为潜变量抽取一个值，再根据这个值从观测变量的条件分布中抽样，得到观测值。具体地说，$D$ 维观测变量 $\mathbf x$ 由 $M$ 维潜变量 $\mathbf z$ 经线性变换、再加上高斯噪声得到，即

$$
\mathbf x=\mathbf W\mathbf z+\boldsymbol\mu+\boldsymbol\epsilon, \tag{16.33}
$$

其中，$\mathbf z$ 是 $M$ 维高斯潜变量，$\boldsymbol\epsilon$ 是 $D$ 维、均值为零、协方差为 $\sigma^2\mathbf I$ 的高斯噪声变量。图 16.7 展示了这个生成过程。注意，这个框架从潜空间映射到数据空间，而前面介绍的常规 PCA 采用相反方向的映射。稍后我们会用贝叶斯定理得到从数据空间到潜空间的逆向映射。

### 16.2.2 似然函数

现在假设要用极大似然法确定参数 $\mathbf W$、$\boldsymbol\mu$ 和 $\sigma^2$。要写出似然函数，先需要观测变量的边缘分布 $p(\mathbf x)$。根据概率的求和规则与乘积规则，它为

$$
p(\mathbf x)=\int p(\mathbf x\mid\mathbf z)p(\mathbf z)\,\mathrm d\mathbf z. \tag{16.34}
$$

由于这是线性高斯模型，边缘分布仍是高斯分布，其形式为（习题 16.6）

<!-- pdf-page: 522 -->

<figure id="fig-16-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-7.png" alt="概率 PCA 的生成过程：先从一维潜变量分布采样，再映射到二维数据空间并叠加各向同性高斯噪声">
  <figcaption>图 16.7：二维数据空间、一维潜空间中的概率 PCA 生成过程。先从先验分布 $p(\mathbf z)$ 中抽取潜变量值 $\hat{\mathbf z}$，再从均值为 $\mathbf w\hat{\mathbf z}+\boldsymbol\mu$、协方差为 $\sigma^2\mathbf I$ 的各向同性高斯分布中抽取观测点 $\mathbf x$。红色圆圈表示这个条件分布，绿色椭圆表示边缘分布 $p(\mathbf x)$ 的等密度线。</figcaption>
</figure>

$$
p(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu,\mathbf C), \tag{16.35}
$$

其中，$D\times D$ 协方差矩阵 $\mathbf C$ 定义为

$$
\mathbf C=\mathbf W\mathbf W^{\mathsf T}+\sigma^2\mathbf I. \tag{16.36}
$$

也可以更直接地推导这个结果：先注意到预测分布仍是高斯分布，再利用式 (16.33) 计算它的均值和协方差：

$$
\mathbb E[\mathbf x]=\mathbb E[\mathbf W\mathbf z+\boldsymbol\mu+\boldsymbol\epsilon]
=\boldsymbol\mu, \tag{16.37}
$$

$$
\begin{aligned}
\operatorname{cov}[\mathbf x]
&=\mathbb E\!\left[(\mathbf W\mathbf z+\boldsymbol\epsilon)(\mathbf W\mathbf z+\boldsymbol\epsilon)^{\mathsf T}\right]\\
&=\mathbb E[\mathbf W\mathbf z\mathbf z^{\mathsf T}\mathbf W^{\mathsf T}]
+\mathbb E[\boldsymbol\epsilon\boldsymbol\epsilon^{\mathsf T}],
\end{aligned} \tag{16.38}
$$

$$
\operatorname{cov}[\mathbf x]=\mathbf W\mathbf W^{\mathsf T}+\sigma^2\mathbf I. \tag{16.39}
$$

这里利用了 $\mathbf z$ 与 $\boldsymbol\epsilon$ 是独立随机变量，因此二者不相关。

直观地说，可以想象拿着一罐喷出各向同性高斯分布“墨雾”的喷雾罐，沿着主子空间移动；墨雾的密度由 $\sigma^2$ 决定，喷洒的位置由先验分布加权。累积的墨迹形成一个“薄饼”状分布，也就是边缘密度 $p(\mathbf x)$。

预测分布 $p(\mathbf x)$ 由 $\boldsymbol\mu$、$\mathbf W$ 和 $\sigma^2$ 决定，但由于潜空间坐标可以旋转，这组参数存在冗余。为说明这一点，令 $\widetilde{\mathbf W}=\mathbf W\mathbf R$，其中 $\mathbf R$ 是正交矩阵。利用 $\mathbf R\mathbf R^{\mathsf T}=\mathbf I$，协方差矩阵 $\mathbf C$ 中的 $\widetilde{\mathbf W}\widetilde{\mathbf W}^{\mathsf T}$ 为

$$
\widetilde{\mathbf W}\widetilde{\mathbf W}^{\mathsf T}
=\mathbf W\mathbf R\mathbf R^{\mathsf T}\mathbf W^{\mathsf T}
=\mathbf W\mathbf W^{\mathsf T}. \tag{16.40}
$$

<!-- pdf-page: 523 -->

<figure id="fig-16-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-8.png" alt="概率 PCA 的有向图：每个观测值 x_n 对应潜变量 z_n，另有参数 mu、W 和 sigma 平方">
  <figcaption>图 16.8：对于包含 $N$ 个 $\mathbf x$ 观测值的数据集，概率 PCA 模型可表示为有向图；每个观测值 $\mathbf x_n$ 对应一个潜变量值 $\mathbf z_n$。</figcaption>
</figure>

因此，式 (16.40) 与 $\mathbf R$ 无关：一整族不同的矩阵 $\widetilde{\mathbf W}$ 都产生相同的预测分布。这种不变性对应于潜空间内的旋转。后文还会讨论该模型中独立参数的个数。

计算预测分布时需要 $\mathbf C^{-1}$，它涉及 $D\times D$ 矩阵求逆。利用矩阵求逆恒等式 (A.7) 可以减少计算量，得到

$$
\mathbf C^{-1}=\sigma^{-2}\mathbf I-\sigma^{-2}\mathbf W\mathbf M^{-1}\mathbf W^{\mathsf T}, \tag{16.41}
$$

其中，$M\times M$ 矩阵 $\mathbf M$ 定义为

$$
\mathbf M=\mathbf W^{\mathsf T}\mathbf W+\sigma^2\mathbf I. \tag{16.42}
$$

由于这里求逆的是 $\mathbf M$，无需直接对 $\mathbf C$ 求逆，计算 $\mathbf C^{-1}$ 的成本由 $O(D^3)$ 降为 $O(M^3)$。

除预测分布 $p(\mathbf x)$ 外，还需要后验分布 $p(\mathbf z\mid\mathbf x)$。利用线性高斯模型的结果 (3.100)，可以直接写成（习题 16.8）

$$
p(\mathbf z\mid\mathbf x)=\mathcal N\!\left(
\mathbf z\mid\mathbf M^{-1}\mathbf W^{\mathsf T}(\mathbf x-\boldsymbol\mu),
\sigma^2\mathbf M^{-1}\right). \tag{16.43}
$$

注意，后验均值依赖于 $\mathbf x$，而后验协方差与 $\mathbf x$ 无关。

### 16.2.3 极大似然

接下来考虑如何用极大似然法确定模型参数。给定观测数据集 $\mathcal X=\{\mathbf x_n\}$，概率 PCA 模型可表示为图 16.8 中的有向图。由式 (16.35)，相应的对数似然函数是

$$
\begin{aligned}
\ln p(\mathcal X\mid\boldsymbol\mu,\mathbf W,\sigma^2)
&=\sum_{n=1}^{N}\ln p(\mathbf x_n\mid\mathbf W,\boldsymbol\mu,\sigma^2)\\
&=-\frac{ND}{2}\ln(2\pi)-\frac{N}{2}\ln|\mathbf C|
-\frac{1}{2}\sum_{n=1}^{N}(\mathbf x_n-\boldsymbol\mu)^{\mathsf T}
\mathbf C^{-1}(\mathbf x_n-\boldsymbol\mu).
\end{aligned} \tag{16.44}
$$

<!-- pdf-page: 524 -->

令对数似然对 $\boldsymbol\mu$ 的导数为零，得到预期的结果 $\boldsymbol\mu=\bar{\mathbf x}$，其中 $\bar{\mathbf x}$ 是式 (16.1) 定义的样本均值（习题 16.9）。由于对数似然是 $\boldsymbol\mu$ 的二次函数，这个解是唯一的最大值；计算二阶导数也可验证。将它代回，对数似然可写为

$$
\ln p(\mathcal X\mid\mathbf W,\boldsymbol\mu,\sigma^2)
=-\frac{N}{2}\left\{D\ln(2\pi)+\ln|\mathbf C|
+\operatorname{Tr}(\mathbf C^{-1}\mathbf S)\right\}, \tag{16.45}
$$

其中 $\mathbf S$ 是式 (16.3) 定义的数据协方差矩阵。

对 $\mathbf W$ 和 $\sigma^2$ 做极大化更复杂，但仍有精确的闭式解。Tipping 和 Bishop（1999）证明，对数似然函数的全部驻点都可写成

$$
\mathbf W_{\mathrm{ML}}=\mathbf U_M(\mathbf L_M-\sigma^2\mathbf I)^{1/2}\mathbf R, \tag{16.46}
$$

其中，$\mathbf U_M$ 是 $D\times M$ 矩阵，其列是数据协方差矩阵 $\mathbf S$ 的任意 $M$ 个特征向量；$\mathbf L_M$ 是 $M\times M$ 对角矩阵，对角元素为对应的特征值 $\lambda_i$；$\mathbf R$ 是任意 $M\times M$ 正交矩阵。

Tipping 和 Bishop（1999）还证明，取最大 $M$ 个特征值对应的特征向量时，似然函数达到最大值；其他解都是鞍点。Roweis（1998）也独立提出过类似猜想，但未给出证明。我们仍假定特征向量按对应特征值递减排序，因此前 $M$ 个主特征向量为 $\mathbf u_1,\ldots,\mathbf u_M$。这时，$\mathbf W$ 的列张成常规 PCA 的主子空间。相应的 $\sigma^2$ 极大似然解是

$$
\sigma^2_{\mathrm{ML}}=\frac{1}{D-M}\sum_{i=M+1}^{D}\lambda_i, \tag{16.47}
$$

即 $\sigma^2_{\mathrm{ML}}$ 是被丢弃维度所对应方差的平均值。

由于 $\mathbf R$ 正交，可以把它解释为 $M$ 维潜空间中的旋转矩阵。把 $\mathbf W$ 的解代入 $\mathbf C$，并利用 $\mathbf R\mathbf R^{\mathsf T}=\mathbf I$，就会发现 $\mathbf C$ 与 $\mathbf R$ 无关。这正是前文所述：潜空间中的旋转不会改变预测密度。当取 $\mathbf R=\mathbf I$ 时，$\mathbf W$ 的列就是主成分特征向量乘上缩放因子 $(\lambda_i-\sigma^2)^{1/2}$。这些因子的意义可从独立高斯分布卷积的方差相加性质看出：沿特征向量 $\mathbf u_i$ 的总方差 $\lambda_i$，由单位方差潜空间分布经 $\mathbf W$ 对应列投影到数据空间后贡献的 $\lambda_i-\sigma^2$，以及噪声模型在所有方向都加入的各向同性方差 $\sigma^2$ 组成。

<!-- pdf-page: 525 -->

这里值得仔细看式 (16.36) 中协方差矩阵的形式。沿单位向量 $\mathbf v$（$\mathbf v^{\mathsf T}\mathbf v=1$）方向，预测分布的方差为 $\mathbf v^{\mathsf T}\mathbf C\mathbf v$。先假设 $\mathbf v$ 与主子空间正交，即它是若干个被丢弃特征向量的线性组合。此时 $\mathbf v^{\mathsf T}\mathbf U_M=0$，所以 $\mathbf v^{\mathsf T}\mathbf C\mathbf v=\sigma^2$。模型在主子空间的正交方向上给出的噪声方差，正是式 (16.47) 中被丢弃特征值的平均值。再假设 $\mathbf v=\mathbf u_i$ 是定义主子空间的一个保留特征向量，则 $\mathbf v^{\mathsf T}\mathbf C\mathbf v=(\lambda_i-\sigma^2)+\sigma^2=\lambda_i$。也就是说，模型准确捕捉了数据沿主轴方向的方差，而其余方向的方差都用同一个平均值 $\sigma^2$ 近似。

构造这个极大似然密度模型的一种方法，是先求数据协方差矩阵的特征向量和特征值，再用上述结果计算 $\mathbf W$ 与 $\sigma^2$；这时可为方便起见取 $\mathbf R=\mathbf I$。不过，若通过对似然函数做数值优化来求极大似然解，例如使用共轭梯度算法（Fletcher，1987；Nocedal 和 Wright，1999），或使用 EM 算法（见第 16.3.2 节），则最终得到的 $\mathbf R$ 基本上是任意的。这意味着 $\mathbf W$ 的列未必正交。若需要正交基，可再对 $\mathbf W$ 做适当处理（Golub 和 Van Loan，1996）。另一种方法是修改 EM 算法，使它直接得到正交归一的主方向，并按对应特征值递减排序（Ahn 和 Oh，2003）。

潜空间中的旋转不变性是一种统计上的**不可辨识性**（non-identifiability），类似于离散潜变量混合模型中的情况。这里存在一整套连续的参数取值，每一组都给出相同的预测密度；而混合模型中，交换分量标签所导致的不可辨识性是离散的。

若取 $M=D$，就不再降维，此时 $\mathbf U_M=\mathbf U$、$\mathbf L_M=\mathbf L$。利用 $\mathbf U\mathbf U^{\mathsf T}=\mathbf I$ 和 $\mathbf R\mathbf R^{\mathsf T}=\mathbf I$，$\mathbf x$ 的边缘分布的协方差 $\mathbf C$ 变为

$$
\mathbf C=\mathbf U(\mathbf L-\sigma^2\mathbf I)^{1/2}
\mathbf R\mathbf R^{\mathsf T}(\mathbf L-\sigma^2\mathbf I)^{1/2}
\mathbf U^{\mathsf T}+\sigma^2\mathbf I
=\mathbf U\mathbf L\mathbf U^{\mathsf T}=\mathbf S, \tag{16.48}
$$

这就得到不受约束的高斯分布的标准极大似然解，其协方差矩阵是样本协方差。

常规 PCA 通常把数据点从 $D$ 维数据空间投影到 $M$ 维线性子空间；相比之下，概率 PCA 最自然的表达是通过式 (16.33)，从潜空间映射到数据空间。在可视化和数据压缩等应用中，可以利用贝叶斯定理把这个映射反过来。此时，数据空间中任意点 $\mathbf x$ 可由它在潜空间中的后验均值和协方差来概括。由式 (16.43)，后验均值为

$$
\mathbb E[\mathbf z\mid\mathbf x]
=\mathbf M^{-1}\mathbf W_{\mathrm{ML}}^{\mathsf T}(\mathbf x-\bar{\mathbf x}). \tag{16.49}
$$

<!-- pdf-page: 526 -->

其中 $\mathbf M$ 由式 (16.42) 给出。该均值映射回数据空间中的点为

$$
\mathbf W\mathbb E[\mathbf z\mid\mathbf x]+\boldsymbol\mu. \tag{16.50}
$$

注意，这与正则化线性回归中的方程形式相同，是线性高斯模型似然极大化的结果（见第 4.1.6 节）。同样由式 (16.43)，后验协方差为 $\sigma^2\mathbf M^{-1}$，与 $\mathbf x$ 无关。

令 $\sigma^2\to0$，后验均值退化为

$$
(\mathbf W_{\mathrm{ML}}^{\mathsf T}\mathbf W_{\mathrm{ML}})^{-1}
\mathbf W_{\mathrm{ML}}^{\mathsf T}(\mathbf x-\bar{\mathbf x}), \tag{16.51}
$$

这表示把数据点正交投影到潜空间，从而恢复标准 PCA 模型（习题 16.11）。不过，这时后验协方差为零，密度变为奇异的。当 $\sigma^2>0$ 时，相比正交投影，潜空间投影会向原点收缩（习题 16.12）。

最后，概率 PCA 模型的一个重要用途，是构造多元高斯分布：它既能捕捉数据中的主要相关性，又能控制自由度，也就是独立参数的个数。一般高斯分布的协方差矩阵有 $D(D+1)/2$ 个独立参数（另有 $D$ 个均值参数，见第 3.2 节），所以参数量随 $D$ 二次增长，在高维空间中可能过大。若将协方差矩阵限制为对角矩阵，就只剩 $D$ 个独立参数，参数量随维度线性增长；但这样会把变量视为彼此独立，无法表达它们之间的相关性。概率 PCA 提供一种折中：既捕捉最重要的 $M$ 个相关方向，又让参数总数只随 $D$ 线性增长。计算自由度即可看出这一点。协方差矩阵 $\mathbf C$ 依赖大小为 $D\times M$ 的 $\mathbf W$ 和 $\sigma^2$，表面上有 $DM+1$ 个参数。但潜空间坐标旋转使其中一些参数冗余。表示这些旋转的正交矩阵 $\mathbf R$ 为 $M\times M$；第一列向量必须归一化，因此有 $M-1$ 个独立参数；第二列还必须与第一列正交，因此有 $M-2$ 个；依此类推。将这个等差数列相加，$\mathbf R$ 共有 $M(M-1)/2$ 个独立参数。因此，$\mathbf C$ 的自由度是

$$
DM+1-\frac{M(M-1)}{2}. \tag{16.52}
$$

固定 $M$ 时，这个模型的独立参数个数只随 $D$ 线性增长。若取 $M=D-1$，就得到完整协方差高斯分布的标准结果（习题 16.14）。这时，沿 $D-1$ 个线性无关方向的方差由 $\mathbf W$ 的列控制，而剩余方向的方差由

<!-- pdf-page: 527 -->
<!-- join-previous-paragraph -->

$\sigma^2$ 决定。若 $M=0$，模型等价于各向同性协方差的情况。

### 16.2.4 因子分析

**因子分析**（factor analysis）也是线性高斯潜变量模型，与概率 PCA 密切相关。两者定义上的唯一区别是：给定潜变量 $\mathbf z$ 时，观测变量 $\mathbf x$ 的条件分布采用对角协方差，而非各向同性协方差，即

$$
p(\mathbf x\mid\mathbf z)
=\mathcal N(\mathbf x\mid\mathbf W\mathbf z+\boldsymbol\mu,\boldsymbol\Psi), \tag{16.53}
$$

其中 $\boldsymbol\Psi$ 是 $D\times D$ 对角矩阵。和概率 PCA 一样，因子分析假设给定潜变量 $\mathbf z$ 后，观测变量 $x_1,\ldots,x_D$ 相互独立。本质上，因子分析用 $\boldsymbol\Psi$ 表示每个坐标自身的独立方差，用 $\mathbf W$ 捕捉变量之间的协方差，从而解释数据中观察到的协方差结构。在因子分析文献中，$\mathbf W$ 的列捕捉观测变量之间的相关性，称为**因子载荷**（factor loadings）；$\boldsymbol\Psi$ 的对角元素表示各变量独立噪声的方差，称为**特殊方差**（uniquenesses）。

因子分析与 PCA 的历史一样悠久；Everitt（1984）、Bartholomew（1987）和 Basilevsky（1994）的著作均有相关讨论。Lawley（1953）和 Anderson（1963）研究了因子分析与 PCA 的联系。他们证明，若因子分析模型取 $\boldsymbol\Psi=\sigma^2\mathbf I$，则在似然函数的驻点处，$\mathbf W$ 的列是经过缩放的样本协方差矩阵特征向量，$\sigma^2$ 是被丢弃特征值的平均值。后来，Tipping 和 Bishop（1999）证明，构成 $\mathbf W$ 的特征向量取主特征向量时，对数似然达到最大值。

利用式 (16.34)，观测变量的边缘分布为 $p(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu,\mathbf C)$，此时

$$
\mathbf C=\mathbf W\mathbf W^{\mathsf T}+\boldsymbol\Psi. \tag{16.54}
$$

与概率 PCA 一样，这个模型在潜空间旋转下保持不变（习题 16.16）。

从历史上看，试图解释各个因子（即 $\mathbf z$ 空间中的坐标）一直存在争议。原因是，潜空间旋转造成因子分析不可辨识，使单个因子的解释遇到困难。但在这里，我们把因子分析视为一种潜变量密度模型；我们关心潜空间的形式，而不关心具体选用哪组坐标来描述它。若想消除潜空间旋转造成的退化，必须考虑非高斯潜变量分布，由此得到独立成分分析模型（见第 16.2.5 节）。

概率 PCA 与因子分析的另一个区别，是它们面对数据集变换时的表现。对于 PCA 和概率 PCA，如果我们

<!-- pdf-page: 528 -->
<!-- join-previous-paragraph -->

旋转数据空间中的坐标系，便会得到对数据完全相同的拟合，只是矩阵 $\mathbf W$ 经相应旋转矩阵变换。然而，对于因子分析，相应的性质是：若按分量重新缩放数据向量，这种变化会被 $\boldsymbol\Psi$ 的元素相应的重新缩放所吸收。

### 16.2.5 独立成分分析

线性高斯潜变量模型的一种推广，是让观测变量与潜变量保持线性关系，但潜变量分布不再是高斯分布。一类重要模型称为**独立成分分析**（independent component analysis，ICA），其潜变量分布可分解为

$$
p(\mathbf z)=\prod_{j=1}^{M}p(z_j).\tag{16.55}
$$

为了理解这类模型的用途，设有两个人同时说话，我们用两个麦克风录下他们的声音。若忽略时间延迟、回声等影响，麦克风在任一时刻收到的信号都是两个人声幅度的线性组合。该线性组合的系数保持不变。若能从样本数据推断这些系数，就可以在混合过程非奇异的前提下将其逆转，得到两路干净信号，每路只包含一个人的声音。这是**盲源分离**问题的一个例子。“盲”表示我们只有混合数据，原始信号源和混合系数都未被观测到（Cardoso，1998）。

处理这类问题的一种方法（MacKay，2003）忽略信号的时间性质，把连续样本当作独立同分布数据。构造一个生成模型：两个潜变量分别表示未观测语音信号的幅度，两个观测变量表示麦克风处的信号值。潜变量的联合分布按上式分解，观测变量则是潜变量的线性组合。这里无需加入噪声分布，因为潜变量与观测变量数目相同，所以观测变量的边缘分布一般不会是奇异的；观测变量可直接视为潜变量的确定性线性组合。给定观测数据集，该模型的似然函数是线性组合系数的函数。可用基于梯度的优化最大化对数似然，从而得到一种特定形式的 ICA。

这一方法要成功，潜变量必须具有非高斯分布。为说明原因，回顾在概率 PCA（以及因子分析）中，潜空间分布是均值为零的各向同性高斯。因此，对于仅差一次潜空间旋转的两种潜变量选择，模型无法将它们区分开。

<!-- pdf-page: 529 -->
<!-- join-previous-paragraph -->

可直接验证这一点：若将 $\mathbf W\mapsto\mathbf W\mathbf R$，其中 $\mathbf R$ 是满足 $\mathbf R\mathbf R^{\mathsf T}=\mathbf I$ 的正交矩阵，则式 (16.36) 的矩阵 $\mathbf C$ 不变，所以边缘密度 (16.35) 与似然函数均不变。即便扩展模型，允许更一般的高斯潜变量分布，也不会改变结论，因为这种模型等价于均值为零的各向同性高斯潜变量模型。

还有一种解释：在线性模型中，高斯潜变量分布不足以识别独立成分，是因为主成分相当于旋转数据空间中的坐标系，使协方差矩阵对角化。新坐标下的数据分布因此不相关。虽然零相关是独立的必要条件，却不是充分条件。实际中，潜变量分布的一种常见选择是（见习题 2.39）

$$
p(z_j)=\frac{1}{\pi\cosh(z_j)}=\frac{2}{\pi(e^{z_j}+e^{-z_j})},\tag{16.56}
$$

其尾部比高斯分布更重，反映出许多真实世界分布也有这一性质。

原始 ICA 模型（Bell 和 Sejnowski，1995）基于最大化信息量所定义的目标函数。概率潜变量表述的一个优点，是有助于说明并建立基本 ICA 的推广。例如，**独立因子分析**（Attias，1999）允许潜变量和观测变量的数量不同、观测变量含噪声，并用高斯混合分布为各潜变量建立灵活的分布。该模型的对数似然用 EM 最大化，潜变量的重建则用变分方法近似。人们还研究了很多其他模型，ICA 及其应用已有大量文献（Jutten 和 Herault，1991；Comon、Jutten 和 Herault，1991；Amari、Cichocki 和 Yang，1996；Pearlmutter 和 Parra，1997；Hyvärinen 和 Oja，1997；Hinton 等，2001；Miskin 和 MacKay，2001；Hojen-Sorensen、Winther 和 Hansen，2002；Choudrey 和 Roberts，2003；Chan、Lee 和 Sejnowski，2003；Stone，2004）。

### 16.2.6 卡尔曼滤波器

到目前为止，我们假定数据值独立同分布。数据点构成有序序列时，这一假设通常不成立。前面看到，隐藏马尔可夫模型可视为混合模型的扩展，用于允许数据中存在序列相关性（见第 15.3.1 节）。类似地，把连续潜变量连接为一条马尔可夫链，也可使连续潜变量模型处理序列数据，如图 16.9 的图模型所示。这称为**线性动力系统**或**卡尔曼滤波器**（Zarchan 和 Musoff，2005）。注意，它与隐藏马尔可夫模型的图结构相同。有意思的是，隐藏马尔可夫模型与线性动力系统在历史上是独立发展出来的；一旦都表示为图模型，它们之间的深层关系就

<!-- pdf-page: 530 -->
<!-- join-previous-paragraph -->

立即显现。卡尔曼滤波器广泛用于许多实时跟踪应用，例如利用雷达反射跟踪飞机。

<figure id="fig-16-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-9.png" alt="卡尔曼滤波器中连续潜变量链与观测变量的概率图模型">
  <figcaption>图 16.9：一种序列数据概率图模型，称为线性动力系统或卡尔曼滤波器；其中潜变量形成一条马尔可夫链。</figcaption>
  <p class="figure-translation">图内符号：$z_1,z_2,\ldots,z_N$ 为潜变量链；$x_1,x_2,\ldots,x_N$ 为相应观测值；箭头表示条件依赖。</p>
</figure>

在最简单的此类模型中，图 16.9 的分布 $p(\mathbf x_n\mid\mathbf z_n)$ 表示该观测值的线性高斯潜变量模型，与前面讨论独立同分布数据时的模型相同。但潜变量 $\{\mathbf z_n\}$ 不再独立，而是形成马尔可夫链：每个潜变量的分布 $p(\mathbf z_n\mid\mathbf z_{n-1})$ 以前一潜变量的状态为条件。它们也可以选择为线性高斯形式，此时 $\mathbf z_n$ 服从均值为 $\mathbf z_{n-1}$ 的线性函数的高斯分布。通常所有 $p(\mathbf x_n\mid\mathbf z_n)$ 共享参数，所有 $p(\mathbf z_n\mid\mathbf z_{n-1})$ 也共享参数，使模型参数总数固定，不随序列长度改变。可用极大似然方法从数据中学习这些参数；高效算法会在图上传播消息（Bishop，2006）。不过，本章余下部分继续关注独立同分布数据。

## 16.3 证据下界

讨论离散潜变量模型时，我们推导了边缘对数似然的证据下界（ELBO），并说明了它如何成为推导期望最大化（EM）算法及其变分推断等推广的基础（见第 15.4 节）。相同框架也适用于连续潜变量，以及同时包含离散和连续变量的模型。这里给出 ELBO 的一种略有不同的推导，并假设潜变量 $\mathbf z$ 连续。

考虑模型 $p(\mathbf x,\mathbf z\mid\mathbf w)$，其中 $\mathbf x$ 是观测变量，$\mathbf z$ 是潜变量，$\mathbf w$ 是可学习参数向量。若引入潜变量上的任意分布 $q(\mathbf z)$，就能把对数似然 $\ln p(\mathbf x\mid\mathbf w)$ 写成两项之和：

$$
\ln p(\mathbf x\mid\mathbf w)=\mathcal L(\mathbf w)+\operatorname{KL}\bigl(q(\mathbf z)\parallel p(\mathbf z\mid\mathbf x,\mathbf w)\bigr),\tag{16.57}
$$

其中定义

$$
\mathcal L(q,\mathbf w)=\int q(\mathbf z)\ln\left\{\frac{p(\mathbf x,\mathbf z\mid\mathbf w)}{q(\mathbf z)}\right\}\,\mathrm d\mathbf z,\tag{16.58}
$$

**译注：** 原书式 (16.57) 记为 $\mathcal L(\mathbf w)$，式 (16.58) 则将同一证据下界记为 $\mathcal L(q,\mathbf w)$；该下界也依赖于 $q$。这里保留两处原记号。

$$
\operatorname{KL}\bigl(q(\mathbf z)\parallel p(\mathbf z\mid\mathbf x,\mathbf w)\bigr)=-\int q(\mathbf z)\ln\left\{\frac{p(\mathbf z\mid\mathbf x,\mathbf w)}{q(\mathbf z)}\right\}\,\mathrm d\mathbf z.\tag{16.59}
$$

<!-- pdf-page: 531 -->

由于 $\operatorname{KL}(q(\mathbf z)\parallel p(\mathbf z\mid\mathbf x,\mathbf w))$ 是 KL 散度，故满足 $\operatorname{KL}(\cdot\parallel\cdot)\geqslant0$（见第 2.5.5 节），从而

$$
\ln p(\mathbf x\mid\mathbf w)\geqslant\mathcal L(\mathbf w).\tag{16.60}
$$

因此，式 (16.58) 的 $\mathcal L(q,\mathbf w)$ 构成对数似然的下界，称为**证据下界**或 ELBO。它与离散情形推导出的式 (15.53) 形式相同，只是以积分代替求和。

可以用称为**期望最大化算法**或 EM 算法的两阶段迭代过程，交替对 $q(\mathbf z)$（E 步）和 $\mathbf w$（M 步）最大化 $\mathcal L(q,\mathbf w)$，从而最大化对数似然。首先初始化参数 $\mathbf w^{(\mathrm{old})}$。在 E 步，固定 $\mathbf w$，对 $q(\mathbf z)$ 最大化下界。由式 (16.59)，下界的最大值在 KL 散度最小时取得，即当 $q(\mathbf z)=p(\mathbf z\mid\mathbf x,\mathbf w^{(\mathrm{old})})$ 时，KL 散度为零。在 M 步，固定这一 $q(\mathbf z)$，对 $\mathbf w$ 最大化 $\mathcal L(q,\mathbf w)$。将 $q(\mathbf z)$ 代入式 (16.58)，得

$$
\begin{aligned}\mathcal L(q,\mathbf w)&=\int p(\mathbf z\mid\mathbf x,\mathbf w^{(\mathrm{old})})\ln p(\mathbf x,\mathbf z\mid\mathbf w)\,\mathrm d\mathbf z\\&\quad-\int p(\mathbf z\mid\mathbf x,\mathbf w^{(\mathrm{old})})\ln p(\mathbf z\mid\mathbf x,\mathbf w^{(\mathrm{old})})\,\mathrm d\mathbf z.\end{aligned}\tag{16.61}
$$

在 M 步保持 $\mathbf w^{(\mathrm{old})}$ 固定，对 $\mathbf w$ 最大化上式。注意，式 (16.61) 右边第二项与 $\mathbf w$ 无关，M 步中可忽略。第一项是完整数据对数似然的期望，其期望分布是用 $\mathbf w^{(\mathrm{old})}$ 计算的 $\mathbf z$ 后验分布（见第 15.3 节）。

对于由独立同分布观测值 $\mathbf x_1,\ldots,\mathbf x_N$ 组成的数据集，似然函数为

$$
\ln p(\mathbf X\mid\mathbf w)=\sum_{n=1}^{N}\ln p(\mathbf x_n\mid\mathbf w),\tag{16.62}
$$

其中数据矩阵 $\mathbf X$ 包含 $\mathbf x_1,\ldots,\mathbf x_N$，参数 $\mathbf w$ 在所有数据点间共享。为每个数据点引入相应潜变量 $\mathbf z_n$ 及分布 $q(\mathbf z_n)$，按推导式 (16.58) 的类似步骤，得到

$$
\mathcal L(q,\mathbf w)=\sum_{n=1}^{N}\int q(\mathbf z_n)\ln\left\{\frac{p(\mathbf x_n,\mathbf z_n\mid\mathbf w)}{q(\mathbf z_n)}\right\}\,\mathrm d\mathbf z_n.\tag{16.63}
$$

第 19.2 节讨论变分自编码器时，会遇到 E 步无法精确求解的模型；因此要用深度神经网络建模 $q(\mathbf z)$，只作部分最大化，再用 ELBO 学习网络参数。

<!-- pdf-page: 532 -->

### 16.3.1 期望最大化

现在可以用通过迭代最大化证据下界而得到的 EM 算法，学习概率 PCA 模型的参数。这似乎没有必要，因为我们已经得到了极大似然参数的精确闭式解。然而，在高维空间中，迭代 EM 过程可能比直接处理样本协方差矩阵更省计算。该 EM 过程还能推广到没有闭式解的因子分析模型（见第 16.2.4 节）。最后，它允许以有原则的方式处理缺失数据。

可按 EM 的一般框架推导概率 PCA 的 EM 算法：先写出完整数据对数似然，再对使用“旧”参数值计算的潜变量后验分布取期望；最大化这一完整数据对数似然的期望，即得到“新”参数值（见第 15.3 节）。由于假定数据点相互独立，完整数据对数似然函数为

$$
\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\mathbf W,\sigma^2)=\sum_{n=1}^{N}\{\ln p(\mathbf x_n\mid\mathbf z_n)+\ln p(\mathbf z_n)\},\tag{16.64}
$$

其中矩阵 $\mathbf Z$ 的第 $n$ 行为 $\mathbf z_n$。已知 $\boldsymbol\mu$ 的精确极大似然解是式 (16.1) 定义的样本均值 $\bar{\mathbf x}$，此时将其代入很方便。利用潜变量分布式 (16.31) 与条件分布式 (16.32)，再对潜变量的后验分布取期望，得到

$$
\begin{aligned}\mathbb E[\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\mathbf W,\sigma^2)]=-\sum_{n=1}^{N}\biggl\{&\frac{D}{2}\ln(2\pi\sigma^2)+\frac12\operatorname{Tr}\bigl(\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]\bigr)\\&+\frac{1}{2\sigma^2}\lVert\mathbf x_n-\boldsymbol\mu\rVert^2-\frac{1}{\sigma^2}\mathbb E[\mathbf z_n]^{\mathsf T}\mathbf W^{\mathsf T}(\mathbf x_n-\boldsymbol\mu)\\&+\frac{1}{2\sigma^2}\operatorname{Tr}\bigl(\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]\mathbf W^{\mathsf T}\mathbf W\bigr)+\frac{M}{2}\ln(2\pi)\biggr\}.\end{aligned}\tag{16.65}
$$

注意，这一表达式只通过高斯分布的充分统计量依赖后验分布。因此，在 E 步，使用旧参数值计算

$$
\mathbb E[\mathbf z_n]=\mathbf M^{-1}\mathbf W^{\mathsf T}(\mathbf x_n-\bar{\mathbf x}),\tag{16.66}
$$

$$
\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]=\sigma^2\mathbf M^{-1}+\mathbb E[\mathbf z_n]\mathbb E[\mathbf z_n]^{\mathsf T},\tag{16.67}
$$

它们由后验分布 (16.43) 和标准关系 $\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]=\operatorname{cov}[\mathbf z_n]+\mathbb E[\mathbf z_n]\mathbb E[\mathbf z_n]^{\mathsf T}$ 直接得到。这里 $\mathbf M$ 由式 (16.42) 定义。

在 M 步，保持后验统计量固定，对 $\mathbf W$ 和 $\sigma^2$ 最大化。对 $\sigma^2$ 最大化很直接。对 $\mathbf W$ 最大化时，利用式 (A.24)，得到以下 M 步方程：

<!-- pdf-page: 533 -->

$$
\mathbf W_{\mathrm{new}}=\left[\sum_{n=1}^{N}(\mathbf x_n-\bar{\mathbf x})\mathbb E[\mathbf z_n]^{\mathsf T}\right]\left[\sum_{n=1}^{N}\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]\right]^{-1},\tag{16.68}
$$

$$
\begin{aligned}\sigma_{\mathrm{new}}^2=\frac{1}{ND}\sum_{n=1}^{N}\biggl\{&\lVert\mathbf x_n-\bar{\mathbf x}\rVert^2-2\mathbb E[\mathbf z_n]^{\mathsf T}\mathbf W_{\mathrm{new}}^{\mathsf T}(\mathbf x_n-\bar{\mathbf x})\\&+\operatorname{Tr}\bigl(\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]\mathbf W_{\mathrm{new}}^{\mathsf T}\mathbf W_{\mathrm{new}}\bigr)\biggr\}.\end{aligned}\tag{16.69}
$$

概率 PCA 的 EM 算法先初始化参数，然后交替进行：E 步用式 (16.66)、(16.67) 计算潜空间后验分布的充分统计量，M 步用式 (16.68)、(16.69) 更新参数值。

EM 算法用于 PCA 的一个优点是，在大规模应用中计算效率高（Roweis，1998）。与基于样本协方差矩阵特征向量分解的常规 PCA 不同，EM 是迭代方法，乍看之下似乎吸引力较小。但在高维空间中，EM 每个循环的计算效率可能远高于常规 PCA。协方差矩阵的特征分解需要 $O(D^3)$ 计算。若只需前 $M$ 个特征向量及对应特征值，可采用 $O(MD^2)$ 的算法。然而，计算协方差矩阵本身仍需 $O(ND^2)$ 次运算，$N$ 为数据点数。快照法等算法（Sirovich，1987）假设特征向量是数据向量的线性组合，避免直接计算协方差矩阵，但其代价为 $O(N^3)$，因此不适合大型数据集。这里的 EM 算法也不显式构造协方差矩阵，最耗计算的是对整个数据集求和的步骤，代价为 $O(NDM)$。当 $D$ 很大且 $M\ll D$ 时，相比 $O(ND^2)$ 可显著节省计算，足以抵消 EM 迭代所需的额外开销。

注意，该 EM 算法可以在线实现：读入并处理一个 $D$ 维数据点后，先将其丢弃，再处理下一个。原因是，E 步中的量——一个 $M$ 维向量和一个 $M\times M$ 矩阵——可以分别为每个数据点计算，而 M 步所需的数据点求和可以增量累积。如果 $N$ 与 $D$ 都很大，这种方法很有利。

有了完全概率化的 PCA 模型，就可以处理缺失数据，前提是它们**随机缺失**；换言之，决定哪些值缺失的过程不依赖任何已观测或未观测变量的值。可对未观测变量的分布进行边缘化来处理这类数据集，再用 EM 最大化所得的似然函数。

**译注：** 原书称这一条件为 *missing at random*，但它在此明确要求缺失机制同时独立于已观测和未观测值；这比通常的“随机缺失”条件更强，通常称为“完全随机缺失”（missing completely at random）。习题 16.22 沿用原书用词。

### 16.3.2 用于 PCA 的 EM

EM 方法还有一个优雅的性质：令 $\sigma^2\to0$，对应标准 PCA，仍可得到有效的类 EM 算法（Roweis，1998）。

<!-- pdf-page: 534 -->
<!-- join-previous-paragraph -->

由式 (16.67)，E 步中唯一需要计算的量是 $\mathbb E[\mathbf z_n]$。而且，由于 $\mathbf M=\mathbf W^{\mathsf T}\mathbf W$，M 步也得到简化。为了突出算法的简洁，定义 $\widetilde{\mathbf X}$ 为一个 $N\times D$ 矩阵，第 $n$ 行是向量 $\mathbf x_n-\bar{\mathbf x}$；再定义 $\boldsymbol\Omega$ 为 $M\times N$ 矩阵，第 $n$ 列是 $\mathbb E[\mathbf z_n]$。那么，用于 PCA 的 EM 算法的 E 步 (16.66) 为

$$
\boldsymbol\Omega=(\mathbf W_{\mathrm{old}}^{\mathsf T}\mathbf W_{\mathrm{old}})^{-1}\mathbf W_{\mathrm{old}}^{\mathsf T}\widetilde{\mathbf X}^{\mathsf T},\tag{16.70}
$$

M 步 (16.68) 为

$$
\mathbf W_{\mathrm{new}}=\widetilde{\mathbf X}^{\mathsf T}\boldsymbol\Omega^{\mathsf T}(\boldsymbol\Omega\boldsymbol\Omega^{\mathsf T})^{-1}.\tag{16.71}
$$

两步同样可以在线实现。其含义也很简单。根据前面的讨论，E 步把数据点正交投影到当前估计的主子空间；M 步则在投影固定时重新估计主子空间，使重建误差最小。

这个 EM 算法有一个容易想象的物理类比，取 $D=2$、$M=1$ 时尤其直观。考虑一组二维数据点，用一根刚性杆表示一维主子空间。以服从胡克定律的弹簧，将每个数据点连到杆上：弹簧的力与其长度成正比，故储存的能量与长度平方成正比。E 步固定杆，让连接点沿杆滑动以使能量最小；每个连接点会独立地移动到相应数据点在杆上的正交投影处。M 步固定连接点，放开杆使之移动至能量最低的位置。如此重复 E 步和 M 步，直到满足适当的收敛准则，如图 16.10 所示。

### 16.3.3 用于因子分析的 EM

可以通过极大似然确定因子分析模型的参数 $\boldsymbol\mu$、$\mathbf W$、$\boldsymbol\Psi$（见第 16.2.4 节）。$\boldsymbol\mu$ 的解仍是样本均值。然而，与概率 PCA 不同，$\mathbf W$ 不再有闭式极大似然解，必须迭代求出。因子分析是潜变量模型，因此可以使用与概率 PCA 类似的 EM 算法（Rubin 和 Thayer，1982）。具体而言，E 步方程为

$$
\mathbb E[\mathbf z_n]=\mathbf G\mathbf W^{\mathsf T}\boldsymbol\Psi^{-1}(\mathbf x_n-\bar{\mathbf x}),\tag{16.72}
$$

$$
\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]=\mathbf G+\mathbb E[\mathbf z_n]\mathbb E[\mathbf z_n]^{\mathsf T},\tag{16.73}
$$

其中定义

$$
\mathbf G=(\mathbf I+\mathbf W^{\mathsf T}\boldsymbol\Psi^{-1}\mathbf W)^{-1}.\tag{16.74}
$$

<!-- pdf-page: 535 -->

<figure id="fig-16-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-10.png" alt="PCA 的 EM 算法在六个连续阶段中的二维数据点与主子空间">
  <figcaption>图 16.10：说明式 (16.70)、(16.71) 所定义的 PCA EM 算法的合成数据。(a) 绿色点是一组数据，另有真实主成分，以乘上对应特征值平方根的特征向量表示。(b) 红色为 $\mathbf W$ 定义的主子空间初始配置；青色是潜变量点 $\mathbf Z$ 到数据空间的投影 $\mathbf Z\mathbf W^{\mathsf T}$。(c) 一次 M 步后，固定 $\mathbf Z$ 并更新 $\mathbf W$。(d) 随后的 E 步中，固定 $\mathbf W$ 并更新 $\mathbf Z$，得到正交投影。(e) 第二次 M 步后。(f) 收敛后的解。</figcaption>
  <p class="figure-translation">图内标记：(a)–(f) 对应图注的六个阶段；绿色点为数据，青色点与线为投影，红线为当前主子空间；坐标刻度为 $-2,0,2$。</p>
</figure>

注意，这些方程只需对 $M\times M$ 矩阵求逆，不需要对 $D\times D$ 矩阵求逆；唯一的例外是 $D\times D$ 对角矩阵 $\boldsymbol\Psi$，它的逆可用 $O(D)$ 步求出。这很方便，因为通常 $M\ll D$。类似地，M 步方程为

$$
\mathbf W_{\mathrm{new}}=\left[\sum_{n=1}^{N}(\mathbf x_n-\bar{\mathbf x})\mathbb E[\mathbf z_n]^{\mathsf T}\right]\left[\sum_{n=1}^{N}\mathbb E[\mathbf z_n\mathbf z_n^{\mathsf T}]\right]^{-1},\tag{16.75}
$$

$$
\boldsymbol\Psi_{\mathrm{new}}=\operatorname{diag}\left\{\mathbf S-\mathbf W_{\mathrm{new}}\frac{1}{N}\sum_{n=1}^{N}\mathbb E[\mathbf z_n](\mathbf x_n-\bar{\mathbf x})^{\mathsf T}\right\},\tag{16.76}
$$

其中 $\operatorname{diag}$ 算子把矩阵的全部非对角元素置为零。

<!-- pdf-page: 536 -->

## 16.4 非线性潜变量模型

本章迄今关注的潜变量模型，都基于从潜空间到数据空间的线性变换。自然会问：能否利用深度神经网络的灵活性表示更复杂的变换，同时利用其学习能力将所得分布拟合到数据集？考虑向量变量 $\mathbf z$ 的简单分布，例如高斯分布

$$
p_z(\mathbf z)=\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I).\tag{16.77}
$$

设用深度神经网络给出的函数 $\mathbf x=\mathbf g(\mathbf z,\mathbf w)$ 变换 $\mathbf z$，其中 $\mathbf w$ 表示权重和偏置。$\mathbf z$ 上的分布与神经网络共同定义了 $\mathbf x$ 上的分布。从该模型采样很直接：先从 $p_z(\mathbf z)$ 生成样本，再用神经网络函数将每个样本变换为相应的 $\mathbf x$。这是一个高效过程，因为不需迭代。

为从数据中学习 $\mathbf g(\mathbf z,\mathbf w)$，考虑如何计算似然函数 $p(\mathbf x\mid\mathbf w)$。$\mathbf x$ 的分布由概率密度的变量变换公式给出（见第 2.4 节）：

$$
p_x(\mathbf x)=p_z(\mathbf z(\mathbf x))\,|\det\mathbf J(\mathbf x)|,\tag{16.78}
$$

其中 $\mathbf J$ 为偏导数组成的雅可比矩阵，其元素为

$$
J_{ij}(\mathbf x)=\frac{\partial z_i}{\partial x_j}.\tag{16.79}
$$

对于给定数据向量 $\mathbf x$，要计算式 (16.78) 右侧的 $p_z(\mathbf z(\mathbf x))$，以及同一 $\mathbf x$ 处式 (16.79) 的雅可比矩阵，必须有神经网络函数的反函数 $\mathbf z=\mathbf g^{-1}(\mathbf x,\mathbf w)$。对多数神经网络，这个反函数并没有明确定义。例如，网络可能表示多对一函数，若干不同输入映射到同一输出，此时变量变换公式不能给出明确定义的密度。而且，如果潜空间与数据空间维度不同，变换也无法求逆。

一种方法是只考虑可逆函数 $\mathbf g(\mathbf z,\mathbf w)$，这要求 $\mathbf z$ 与 $\mathbf x$ 具有相同维度。第 18 章介绍归一化流时将更详细讨论这一方法。

### 16.4.1 非线性流形

要求潜空间与数据空间具有相同维数，是很大的限制。设 $\mathbf z$ 为 $M$ 维、$\mathbf x$ 为 $D$ 维，且 $M<D$。此时 $\mathbf x$ 上的分布局限于一个 $M$ 维**流形**或子空间，如图 16.11 所示。低维流形存在于许多机器学习应用中，

<!-- pdf-page: 537 -->
<!-- join-previous-paragraph -->

例如自然图像的分布建模（见第 6.1.4 节）。非线性潜变量模型很适合这类数据，因为它们表达了一种很强的归纳偏置：数据并不“填满”整个数据空间，而是局限于流形；但流形的形状和维度通常事先未知。

<figure id="fig-16-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-11.png" alt="神经网络将二维潜空间中的点映射到三维数据空间的曲面">
  <figcaption>图 16.11：用参数向量为 $\mathbf w$ 的神经网络所表示的非线性函数 $\mathbf x=\mathbf g(\mathbf z,\mathbf w)$，把二维潜空间 $\mathbf z=(z_1,z_2)$ 映射到三维数据空间 $\mathbf x=(x_1,x_2,x_3)$。</figcaption>
  <p class="figure-translation">图内符号：$z_1,z_2$ 为潜空间坐标；$x_1,x_2,x_3$ 为数据空间坐标；$\mathbf g(\mathbf z,\mathbf w)$ 为映射函数；$\mathbf z$ 为潜点，$\mathbf x$ 为对应数据点。</p>
</figure>

然而，这一框架有一个问题：任何不精确落在流形上的数据向量，都被赋予零概率密度。对任何现实数据集，各数据点的似然函数都会为零，而 $\mathbf w$ 的微小改变不会改变这一点，因而基于梯度的学习会遇到困难。为此，沿用前面回归和分类问题的做法，在整个数据空间定义条件分布，其参数由神经网络输出给出。例如，若 $\mathbf x$ 是连续变量向量，可选择高斯条件分布：

$$
p(\mathbf x\mid\mathbf z,\mathbf w)=\mathcal N(\mathbf x\mid\mathbf g(\mathbf z,\mathbf w),\sigma^2\mathbf I),\tag{16.80}
$$

其中神经网络 $\mathbf g(\mathbf z,\mathbf w)$ 的输出单元使用线性激活函数，且 $\mathbf g\in\mathbb R^D$。生成模型由 $\mathbf z$ 的潜变量分布和 $\mathbf x$ 的条件分布共同指定，可表示为图 16.12 的简单图模型。

从该分布抽取独立样本既直接又高效。先用标准方法从高斯分布 (16.77) 抽样，再把所得值输入神经网络，得到输出 $\mathbf g(\mathbf z,\mathbf w)$；最后从均值为该输出、协方差为 $\sigma^2\mathbf I$ 的高斯分布 (16.80) 抽样。重复这个三步过程即可得到多个独立样本（见第 14.1.2 节）。

潜变量分布 $p(\mathbf z)$ 与条件分布 $p(\mathbf x\mid\mathbf z)$ 共同定义数据空间上的边缘分布：

<figure id="fig-16-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-12.png" alt="潜变量 z 指向观测变量 x 的两节点有向图">
  <figcaption>图 16.12：表示式 (16.77) 和 (16.80) 所给分布的图模型；二者共同定义联合分布 $p(\mathbf x,\mathbf z)=p(\mathbf x\mid\mathbf z)p(\mathbf z)$。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf z$ 为潜变量，$\mathbf x$ 为观测变量；箭头表示 $\mathbf x$ 以 $\mathbf z$ 为条件。</p>
</figure>

<!-- pdf-page: 538 -->

$$
p(\mathbf x)=\int p(\mathbf z)p(\mathbf x\mid\mathbf z)\,\mathrm d\mathbf z.\tag{16.81}
$$

图 16.13 用一个一维潜空间、二维数据空间的简单例子说明这一点。

<figure id="fig-16-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-13.png" alt="一维高斯潜变量映射到二维圆形数据流形并形成条件及边缘分布">
  <figcaption>图 16.13：一维潜空间与二维数据空间的非线性潜变量模型示例。(a) 潜空间中的先验为均值为零、方差为一的高斯分布。(b) 左侧三个图展示不同 $z$ 值的高斯条件分布 $p(\mathbf x\mid z)$，最右图展示边缘分布 $p(\mathbf x)$。定义条件分布均值的非线性函数为 $g_1(z)=\sin z$、$g_2(z)=\cos z$，因此在数据空间画出一个圆。条件分布的标准差为 $\sigma=0.3$。［据 Prince（2020）图，原书经许可使用。］</figcaption>
  <p class="figure-translation">图内标记：$z$ 为潜空间横轴；$p(z)$ 为先验密度；$x_1,x_2$ 为数据空间坐标；(a)、(b) 对应图注中的两部分；白色箭头示出沿流形的位置变化。</p>
</figure>

### 16.4.2 似然函数

已经看到，从非线性潜变量模型抽样很容易。现在假设要通过最大化似然函数，把模型拟合到观测数据集。由概率的乘法与加法规则，对 $\mathbf z$ 积分即可得到似然：

$$
\begin{aligned}p(\mathbf x\mid\mathbf w)&=\int p(\mathbf x\mid\mathbf z,\mathbf w)p(\mathbf z)\,\mathrm d\mathbf z\\&=\int\mathcal N(\mathbf x\mid\mathbf g(\mathbf z,\mathbf w),\sigma^2\mathbf I)\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I)\,\mathrm d\mathbf z.\end{aligned}\tag{16.82}
$$

虽然积分内部的两个分布都是高斯，但由于神经网络定义的 $\mathbf g(\mathbf z,\mathbf w)$ 高度非线性，该积分无法解析求解。

<!-- pdf-page: 539 -->

<figure id="fig-16-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-14.png" alt="三个手写数字 2 图像：原图、缺失一段笔画、平移半像素">
  <figcaption>图 16.14：三幅手写数字示例，说明用潜空间采样计算似然函数为何需要大量样本。(a) 原图；(b) 笔画的一部分被移除；(c) 原图向下、向右各平移半个像素。按似然衡量，图 (b) 比图 (c) 更接近图 (a)，尽管视觉上图 (c) 与图 (a) 更相近。［据 Doersch（2016）图，原书经许可使用。］</figcaption>
  <p class="figure-translation">图内标记：(a) 原始数字“2”；(b) 笔画受损的数字；(c) 平移后的数字。</p>
</figure>

一种计算似然函数的方法，是从潜空间分布抽取样本，以它们将式 (16.82) 近似为

$$
p(\mathbf x\mid\mathbf w)\simeq\frac{1}{K}\sum_{i=1}^{K}p(\mathbf x\mid\mathbf z_i,\mathbf w),\tag{16.83}
$$

其中 $\mathbf z_i\sim p(\mathbf z)$。这相当于把 $\mathbf z$ 上的分布表示成一个混合系数固定为 $1/K$ 的高斯混合；当样本数趋于无穷时，就得到真实的似然函数。然而，有效训练通常需要大得无法实践的 $K$。为理解原因，考虑图 16.14 的三幅手写数字，设图 (a) 是要计算似然的向量 $\mathbf x$。如果训练好的模型生成图 (b)，我们会认为模型很差，因为这不是数字“2”的良好表示，因此应赋予它低得多的似然。反过来，图 (c) 是把 (a) 向下、向右各移动半个像素所得，是数字“2”的好例子，应有较高的似然。然而，式 (16.80) 是高斯分布，因此似然与网络输出和数据向量 $\mathbf x$ 之间负平方距离的指数成正比。图 (a) 与 (b) 的平方距离为 $0.0387$，而 (a) 与 (c) 的平方距离为 $0.2693$。所以，如果把方差参数 $\sigma^2$ 设得足够小，使图 (b) 的似然较低，那么图 (c) 的似然会更低。即使模型擅长生成数字，也必须考察数量极多的 $\mathbf z$ 样本，才可能遇到与图 (a) 足够接近的数字。因此，我们需要更精巧、适于实际应用的非线性潜变量模型训练方法。在概述这些方法之前，先简要讨论离散数据空间的若干问题。

<!-- pdf-page: 540 -->

<figure id="fig-16-15">
  <img src="books/bishop-deep-learning-2024/assets/chapter-16/fig-16-15.png" alt="离散概率柱与去量化后连续概率密度柱的对照">
  <figcaption>图 16.15：去量化示意图。(a) 单变量的离散分布；(b) 与之对应的去量化连续分布。</figcaption>
  <p class="figure-translation">图内标记：(a) 离散分布，(b) 去量化后的连续分布；横轴数字 $0,1,2$ 为变量的离散取值。</p>
</figure>

### 16.4.3 离散数据

如果观测数据集由独立二元变量构成，可使用如下条件分布：

$$
p(\mathbf x\mid\mathbf z,\mathbf w)=\prod_{i=1}^{D}g_i(\mathbf z,\mathbf w)^{x_i}\bigl(1-g_i(\mathbf z,\mathbf w)\bigr)^{1-x_i},\tag{16.84}
$$

其中 $g_i(\mathbf z,\mathbf w)=\sigma(a_i(\mathbf z,\mathbf w))$ 是输出单元 $i$ 的激活值，$\sigma(\cdot)$ 为 logistic sigmoid 激活函数，$a_i(\mathbf z,\mathbf w)$ 为输出单元 $i$ 的预激活值。同样，对于独热编码的类别变量，可用多项分布：

$$
p(\mathbf x\mid\mathbf z,\mathbf w)=\prod_{i=1}^{D}g_i(\mathbf z,\mathbf w)^{x_i},\tag{16.85}
$$

其中

$$
g_i(\mathbf z,\mathbf w)=\frac{\exp(a_i(\mathbf z,\mathbf w))}{\sum_j\exp(a_j(\mathbf z,\mathbf w))}\tag{16.86}
$$

是 softmax 激活函数。把相应条件分布相乘，也可以处理离散与连续变量的组合。

实际中，连续变量以离散数值表示。例如，图像的红、绿、蓝三通道强度可以用表示 $\{0,\ldots,255\}$ 的 8 位数值。采用深度神经网络构建高度灵活的模型时，这可能带来问题：若密度坍缩到一个或多个离散值上，似然函数可能趋于零。**去量化**（dequantization）可以解决这个问题：对变量加入噪声，通常从相邻离散值之间的区间上的均匀分布抽取，如图 16.15 所示。对训练集去量化时，将每个观测值替换为与该离散值对应的连续分布中随机抽取的样本，这会降低模型发现病态解的可能性。

<!-- pdf-page: 541 -->

### 16.4.4 生成建模的四种方法

我们已经看到，基于深度神经网络的非线性潜变量模型为生成模型提供了高度灵活的框架。由于神经网络变换具有通用性，原则上，这类模型能高精度近似几乎任何目标分布。训练完成后，它们还有可能通过高效、非迭代的过程从分布生成样本。不过，训练这类模型存在一些挑战，迫使我们发展比线性模型更精巧的方法。人们提出了许多方法，各有优势和局限，大体可分为以下四类。

**生成对抗网络**（generative adversarial network，GAN）放宽了网络映射必须可逆的要求，因此允许潜空间维度低于数据空间。它还放弃似然函数的概念，转而引入第二个神经网络，为生成网络提供训练信号。由于没有明确定义的似然函数，训练过程可能不稳定；但训练完成后，从模型生成样本很直接，结果也可能质量很高（见第 17 章）。

**变分自编码器**（variational autoencoder，VAE）框架同样使用第二个神经网络，其作用是近似潜变量的后验分布，从而能够近似计算似然函数。训练比 GAN 更稳健，从训练好的模型采样也很直接，但获得最高质量的结果可能更难（见第 19 章）。

对于**归一化流**，将潜空间维度设为与数据空间相同，再修改生成神经网络，使其可逆。可逆性要求限制了网络的函数形式，但允许无近似地计算似然，也允许高效采样（见第 18 章）。

最后，**扩散模型**使用网络学习通过一系列去噪步骤，把先验分布的样本转换为数据分布的样本。它在许多应用中达到最先进的性能，但由于必须多次通过网络去噪，采样成本可能很高（见第 20 章）。

本书最后四章将详细探讨这些方法。

## 习题

**16.1（★★）** 本题用数学归纳法证明：使投影后数据方差最大的 $M$ 维子空间线性投影，是由数据协方差矩阵 $\mathbf S$（式 (16.3)）中对应最大 $M$ 个特征值的特征向量定义的。第 16.1 节已证明 $M=1$ 的情形。现在假设结论对一般的 $M$ 成立，证明它对 $M+1$ 也成立。为此，先对定义数据空间中新方向的向量 $\mathbf u_{M+1}$ 求投影数据方差的导数并令其为零，

<!-- pdf-page: 542 -->
<!-- join-previous-paragraph -->

同时要求 $\mathbf u_{M+1}$ 与已有向量 $\mathbf u_1,\ldots,\mathbf u_M$ 正交，且自身归一化为单位长度。用拉格朗日乘子强制满足这些约束（见附录 C）。再利用 $\mathbf u_1,\ldots,\mathbf u_M$ 的正交归一性质，证明新向量 $\mathbf u_{M+1}$ 是 $\mathbf S$ 的特征向量。最后，若特征值已按降序排列，证明选取对应 $\lambda_{M+1}$ 的特征向量时方差最大。

**16.2（★★）** 证明：在正交归一约束 (16.7) 下，对 $\mathbf u_i$ 而言，PCA 误差度量 $J$（式 (16.15)）的最小值在 $\mathbf u_i$ 为数据协方差矩阵 $\mathbf S$ 的特征向量时取得。为此，对每个约束引入一个拉格朗日乘子，组成矩阵 $\mathbf H$。用矩阵记号写出的修正误差度量为

$$
\widetilde J=\operatorname{Tr}\{\widehat{\mathbf U}^{\mathsf T}\mathbf S\widehat{\mathbf U}\}+\operatorname{Tr}\{\mathbf H(\mathbf I-\widehat{\mathbf U}^{\mathsf T}\widehat{\mathbf U})\},\tag{16.87}
$$

其中 $\widehat{\mathbf U}$ 是 $D\times(D-M)$ 矩阵，其列为 $\mathbf u_i$。对 $\widehat{\mathbf U}$ 最小化 $\widetilde J$，证明解满足 $\mathbf S\widehat{\mathbf U}=\widehat{\mathbf U}\mathbf H$。显然，一种可能的解是 $\widehat{\mathbf U}$ 各列为 $\mathbf S$ 的特征向量，此时 $\mathbf H$ 是由相应特征值构成的对角矩阵。为求一般解，证明可把 $\mathbf H$ 视为对称矩阵；再利用它的特征向量展开，证明 $\mathbf S\widehat{\mathbf U}=\widehat{\mathbf U}\mathbf H$ 的一般解所给出的 $\widetilde J$，与将 $\widehat{\mathbf U}$ 各列取为 $\mathbf S$ 特征向量的特定解相同。这些解既然等价，选用特征向量解最方便。

**16.3（★）** 假设特征向量 $\mathbf v_i$ 长度为一，验证式 (16.30) 定义的特征向量也已归一化为单位长度。

**16.4（★）** 假设在概率 PCA 模型中，用一般高斯分布 $\mathcal N(\mathbf z\mid\mathbf m,\boldsymbol\Sigma)$ 替换式 (16.31) 的均值为零、单位协方差的潜空间分布。通过重新定义模型参数，证明对于任何有效的 $\mathbf m$ 和 $\boldsymbol\Sigma$，观测变量的边缘分布 $p(\mathbf x)$ 都可得到完全相同的模型。

**16.5（★★）** 设 $D$ 维随机变量 $\mathbf x$ 服从高斯分布 $\mathcal N(\mathbf x\mid\boldsymbol\mu,\boldsymbol\Sigma)$，考虑 $M$ 维随机变量 $\mathbf y=\mathbf A\mathbf x+\mathbf b$，其中 $\mathbf A$ 为 $M\times D$ 矩阵。证明 $\mathbf y$ 也服从高斯分布，求出其均值与协方差，并讨论 $M<D$、$M=D$、$M>D$ 三种情形下该高斯分布的形式。

**16.6（★★）** 利用一般分布的均值与协方差结果 (2.122)、(2.123)，推导概率 PCA 模型中边缘分布 $p(\mathbf x)$ 的结果 (16.35)。

**16.7（★）** 为第 16.2 节描述的概率 PCA 模型画出有向概率图，其中把观测变量 $\mathbf x$ 的各分量显式画为独立节点。

<!-- pdf-page: 543 -->
<!-- join-previous-paragraph -->

进而验证该模型具有与第 11.2.3 节讨论的朴素贝叶斯模型相同的独立性结构。

**16.8（★★）** 利用式 (3.100) 的结果，证明概率 PCA 模型的后验分布 $p(\mathbf z\mid\mathbf x)$ 由式 (16.43) 给出。

**16.9（★）** 验证：对参数 $\boldsymbol\mu$ 最大化概率 PCA 模型的对数似然 (16.44)，得到 $\boldsymbol\mu_{\mathrm{ML}}=\bar{\mathbf x}$，其中 $\bar{\mathbf x}$ 为数据向量均值。

**16.10（★★）** 计算概率 PCA 模型的对数似然函数 (16.44) 对参数 $\boldsymbol\mu$ 的二阶导数，证明驻点 $\boldsymbol\mu_{\mathrm{ML}}=\bar{\mathbf x}$ 是唯一最大值。

**16.11（★★）** 证明当 $\sigma^2\to0$ 时，概率 PCA 模型的后验均值成为对主子空间的正交投影，与常规 PCA 相同。

**16.12（★★）** 证明当 $\sigma^2>0$ 时，概率 PCA 模型的后验均值相对正交投影朝原点移动。

**16.13（★★）** 按常规 PCA 的最小二乘投影代价，证明概率 PCA 下数据点的最优重建为

$$
\widetilde{\mathbf x}=\mathbf W_{\mathrm{ML}}(\mathbf W_{\mathrm{ML}}^{\mathsf T}\mathbf W_{\mathrm{ML}})^{-1}\mathbf M\mathbb E[\mathbf z\mid\mathbf x].\tag{16.88}
$$

**16.14（★）** 具有 $M$ 维潜空间与 $D$ 维数据空间的概率 PCA 模型，其协方差矩阵的独立参数个数由式 (16.52) 给出。验证：当 $M=D-1$，独立参数个数与一般协方差的高斯分布相同；当 $M=0$，与各向同性协方差的高斯分布相同。

**16.15（★）** 推导第 16.2.4 节所述因子分析模型的独立参数个数表达式。

**16.16（★★）** 证明第 16.2.4 节的因子分析模型对潜空间坐标旋转保持不变。

**16.17（★★）** 考虑一个线性高斯潜变量模型，其潜空间分布为 $p(\mathbf z)=\mathcal N(\mathbf x\mid\mathbf 0,\mathbf I)$，观测变量的条件分布为 $p(\mathbf x\mid\mathbf z)=\mathcal N(\mathbf x\mid\mathbf W\mathbf z+\boldsymbol\mu,\boldsymbol\Phi)$，其中 $\boldsymbol\Phi$ 是任意对称正定噪声协方差矩阵。现在对数据变量作非奇异线性变换 $\mathbf x\mapsto\mathbf A\mathbf x$，$\mathbf A$ 为 $D\times D$ 矩阵。若 $\boldsymbol\mu_{\mathrm{ML}}$、$\mathbf W_{\mathrm{ML}}$、$\boldsymbol\Phi_{\mathrm{ML}}$ 是原始未变换数据对应的极大似然解，证明 $\mathbf A\boldsymbol\mu_{\mathrm{ML}}$、$\mathbf A\mathbf W_{\mathrm{ML}}$ 和 $\mathbf A\boldsymbol\Phi_{\mathrm{ML}}\mathbf A^{\mathsf T}$ 是变换后数据集的相应极大似然解。最后证明模型的形式在以下两种情况下保持不变：(i) $\mathbf A$ 和 $\boldsymbol\Phi$ 都是对角矩阵。这对应因子分析。变换后的 $\boldsymbol\Phi$ 仍为对角矩阵，因此因子分析在按分量重新缩放数据变量时具有协变性；

<!-- pdf-page: 544 -->
<!-- join-previous-paragraph -->

(ii) $\mathbf A$ 正交，$\boldsymbol\Phi$ 与单位矩阵成正比，即 $\boldsymbol\Phi=\sigma^2\mathbf I$。这对应概率 PCA。变换后的 $\boldsymbol\Phi$ 仍与单位矩阵成正比，因此概率 PCA 在旋转数据空间坐标轴时具有协变性，与常规 PCA 一样。

**译注：** 习题 16.17 的原书将潜空间分布写为 $p(\mathbf z)=\mathcal N(\mathbf x\mid\mathbf 0,\mathbf I)$。按左侧变量及式 (16.31) 的先验定义，高斯密度的自变量应为 $\mathbf z$；上文保留了原式。

**16.18（★）** 验证连续潜变量模型的对数似然函数可写成式 (16.57) 的两项之和，两项分别由式 (16.58)、(16.59) 定义。可先用概率的乘法规则：

$$
p(\mathbf x,\mathbf z\mid\mathbf w)=p(\mathbf z\mid\mathbf x,\mathbf w)p(\mathbf x\mid\mathbf w),\tag{16.89}
$$

再将 $p(\mathbf x,\mathbf z\mid\mathbf w)$ 代入式 (16.58)。

**16.19（★）** 证明独立同分布数据集的证据下界（ELBO）具有式 (16.63) 的形式。

**16.20（★★）** 画出一个有向概率图模型，表示概率 PCA 模型的离散混合，其中每个 PCA 模型都有各自的 $\mathbf W$、$\boldsymbol\mu$ 和 $\sigma^2$。再画一张修改后的图，使混合分量之间共享这些参数值。

**16.21（★★）** 通过最大化式 (16.65) 的完整数据对数似然期望，推导概率 PCA 模型的 M 步方程 (16.68) 和 (16.69)。

**16.22（★★★）** 概率化的主成分分析有一个优点：只要数据是随机缺失的，就可以用于部分值缺失的数据集。推导在这种情况下最大化概率 PCA 模型似然函数的 EM 算法。注意，此时 $\{\mathbf z_n\}$ 以及数据向量 $\{\mathbf x_n\}$ 中的缺失值，都是潜变量。证明在所有数据值均被观测到的特例中，这会化为第 16.3.2 节推导的概率 PCA EM 算法。

**16.23（★★）** 设 $\mathbf W$ 为 $D\times M$ 矩阵，其各列定义嵌入 $D$ 维数据空间的 $M$ 维线性子空间；设 $\boldsymbol\mu$ 是 $D$ 维向量。给定数据集 $\{\mathbf x_n\}$，$n=1,\ldots,N$，可用一组 $M$ 维向量 $\{\mathbf z_n\}$ 的线性映射近似数据点，即用 $\mathbf W\mathbf z_n+\boldsymbol\mu$ 近似 $\mathbf x_n$。相应的平方和重建代价为

$$
J=\sum_{n=1}^{N}\lVert\mathbf x_n-\boldsymbol\mu-\mathbf W\mathbf z_n\rVert^2.\tag{16.90}
$$

首先证明，对 $\boldsymbol\mu$ 最小化 $J$，可得类似的表达式，但其中 $\mathbf x_n$ 与 $\mathbf z_n$ 分别替换为零均值变量 $\mathbf x_n-\bar{\mathbf x}$ 和 $\mathbf z_n-\bar{\mathbf z}$；这里 $\bar{\mathbf x}$ 和 $\bar{\mathbf z}$ 为样本均值。随后证明，在

<!-- pdf-page: 545 -->
<!-- join-previous-paragraph -->

固定 $\mathbf W$ 时对 $\mathbf z_n$ 最小化 $J$，得到 PCA 的 E 步 (16.70)；而固定 $\{\mathbf z_n\}$ 时对 $\mathbf W$ 最小化 $J$，得到 PCA 的 M 步 (16.71)。

**16.24（★★）** 推导因子分析 EM 算法 E 步的公式 (16.72)、(16.73)。注意，由习题 16.26 的结果，可用样本均值 $\bar{\mathbf x}$ 代替参数 $\boldsymbol\mu$。

**16.25（★★）** 写出因子分析模型的完整数据对数似然期望的表达式，进而推导相应的 M 步方程 (16.75)、(16.76)。

**16.26（★★）** 考察二阶导数，证明第 16.2.4 节讨论的因子分析模型的对数似然函数，关于参数 $\boldsymbol\mu$ 的唯一驻点是式 (16.1) 定义的样本均值，并证明该驻点为最大值。
