# 第 12 章 连续潜变量

<aside class="chapter-guide"><strong>本章导读</strong><p>高维数据往往可以由少量连续变量来描述。本章先从主成分分析的方差与重构误差两种视角出发，再建立相应的概率模型，讨论参数学习、缺失数据和维数选择，并介绍因子分析、核方法及非线性潜变量模型。</p></aside>

<!-- pdf-page: 579 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-chapter-opening.png" alt="黑白水纹背景上的第 12 章标题"><p class="figure-translation">Continuous Latent Variables → 连续潜变量。</p></figure>

第 9 章讨论了具有离散潜变量的概率模型，例如高斯混合模型。现在，我们来研究某些或全部潜变量为连续变量的模型。这类模型的一个重要动机是：许多数据集中的数据点，都位于某个流形附近，而这个流形的维数远低于原始数据空间的维数。为理解这种情况为何会出现，考虑如下构造的人工数据集：取一个用 $64\times64$ 像素灰度图像表示的离线手写数字，<span class="margin-reference">附录 A</span>在周围填充取值为零的像素（对应白色像素），将它嵌入大小为 $100\times100$ 的较大图像中，同时随机改变数字的位置和方向，如图 12.1 所示。每幅所得图像，都可以表示为 $100\times100=10{,}000$ 维数据空间中的一个点。然而，在这样一组图像中，变化实际上只有三个自由度，分别对应竖直平移、水平平移和旋转。因此，数据点将位于数据空间的某个子空间内，而该子空间的内在维数为三。注意，

<!-- pdf-page: 580 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-1.png" alt="同一个手写数字 3 在较大图像区域中的五种平移和旋转"><figcaption>图 12.1：人工数据集的构造方法是，取一幅离线手写数字图像，生成多个副本，并在较大的图像区域内，对每个副本中的数字作随机位移和旋转。所得图像各含 $100\times100=10{,}000$ 个像素。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
这个流形是非线性的。例如，当数字平移经过某个像素时，该像素值会从零（白色）变为一（黑色），然后再变回零；显然，这是数字位置的非线性函数。在这个例子中，平移与旋转参数是潜变量，因为我们只观测到图像向量，并不知道生成它们时使用了怎样的平移或旋转变量值。

对于真实的数字图像数据，缩放还会带来一个额外的自由度。此外，同一个人书写时的变化，以及不同人之间书写风格的差异，会造成更复杂的形变，从而引入多个额外自由度。即便如此，这些自由度的数量与数据集的维数相比仍然很小。

另一个例子是油流数据集。<span class="margin-reference">附录 A</span>对于气、水、油三相的某种给定几何分布，变化只有两个自由度，分别对应管道中油的比例和水的比例；气体的比例随之确定。虽然数据空间包含 $12$ 个测量值，但数据点会落在嵌入该空间的二维流形附近。在这个例子中，流形包含对应不同流型的几个独立部分，每一部分都是一个带噪声的连续二维流形。如果目标是数据压缩或密度建模，利用这种流形结构就可能带来好处。

在实践中，数据点不会恰好落在一个光滑的低维流形上，我们可以把数据点偏离流形的部分解释为“噪声”。由此自然得到这类模型的生成式观点：先根据某个潜变量分布在流形内选取一个点，再加入噪声，生成一个观测数据点；噪声根据给定潜变量时数据变量的某个条件分布抽取。

最简单的连续潜变量模型假定潜变量和观测变量都服从高斯分布，并用线性高斯关系描述观测变量对潜变量状态的依赖。<span class="margin-reference">第 8.1.4 节</span>这样就得到了著名的主成分分析（principal component analysis，PCA）技术的概率形式，以及一个相关模型——因子分析。

本章先介绍标准的、非概率形式的 PCA，<span class="margin-reference">第 12.1 节</span>再说明 PCA 如何自然地作为

<!-- pdf-page: 581 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-2.png" alt="二维红色数据点正交投影到紫色主轴，绿色为投影点，蓝线为投影误差"><figcaption>图 12.2：主成分分析寻找一个较低维的空间，称为主子空间，图中用紫红色直线表示，使数据点（红点）到该子空间的正交投影具有最大的方差，投影点用绿点表示。PCA 的另一种定义，是使蓝线所示的投影误差平方和最小。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
某种特定线性高斯潜变量模型的最大似然解出现。<span class="margin-reference">第 12.2 节</span>这种概率形式带来许多优点，例如可以用 EM 估计参数，依据概率原理构建 PCA 模型的混合，以及建立贝叶斯形式，从数据中自动确定主成分的数量。最后，我们简要讨论几种超出线性高斯假设的潜变量推广，包括使用非高斯潜变量而得到的独立成分分析框架，以及潜变量与观测变量之间具有非线性关系的模型。<span class="margin-reference">第 12.4 节</span>

## 12.1 主成分分析

主成分分析，简称 PCA，是一种广泛用于降维、有损数据压缩、特征提取和数据可视化等应用的技术（Jolliffe, 2002）。它也称为 Karhunen–Loève 变换。

PCA 有两种常用定义，它们导向同一个算法。一种定义是：将数据正交投影到一个较低维的线性空间，使投影后数据的方差最大；这个线性空间称为主子空间（principal subspace）（Hotelling, 1933）。等价地，也可以将 PCA 定义为使平均投影代价最小的线性投影，其中平均投影代价是数据点与其投影之间距离的均方值（Pearson, 1901）。图 12.2 展示了正交投影的过程。下面依次考虑这两种定义。

### 12.1.1 最大方差表述

考虑观测数据集 $\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，$\mathbf{x}_n$ 是 $D$ 维欧几里得变量。我们的目标是将数据投影到维数为 $M<D$ 的空间，同时使投影后数据的方差最大。暂时假定 $M$ 的值已经给定。本章后面

<!-- pdf-page: 582 -->

<!-- join-previous-paragraph -->
将讨论从数据中确定合适 $M$ 值的方法。

首先，考虑投影到一维空间的情况，即 $M=1$。可以用一个 $D$ 维向量 $\mathbf{u}_1$ 定义该空间的方向。为方便起见，不失一般性地将它选为单位向量，使 $\mathbf{u}_1^{\mathrm{T}}\mathbf{u}_1=1$；注意，我们只关心 $\mathbf{u}_1$ 所定义的方向，并不关心其本身的大小。每个数据点 $\mathbf{x}_n$ 随后被投影为标量值 $\mathbf{u}_1^{\mathrm{T}}\mathbf{x}_n$。投影后数据的均值为 $\mathbf{u}_1^{\mathrm{T}}\overline{\mathbf{x}}$，其中 $\overline{\mathbf{x}}$ 是样本均值，定义为

$$
\overline{\mathbf{x}}=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n
\tag{12.1}
$$

而投影后数据的方差为

$$
\frac{1}{N}\sum_{n=1}^{N}\{\mathbf{u}_1^{\mathrm{T}}\mathbf{x}_n-\mathbf{u}_1^{\mathrm{T}}\overline{\mathbf{x}}\}^2=\mathbf{u}_1^{\mathrm{T}}\mathbf{S}\mathbf{u}_1
\tag{12.2}
$$

其中 $\mathbf{S}$ 是数据协方差矩阵，定义为

$$
\mathbf{S}=\frac{1}{N}\sum_{n=1}^{N}(\mathbf{x}_n-\overline{\mathbf{x}})(\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}.
\tag{12.3}
$$

现在，相对于 $\mathbf{u}_1$ 最大化投影后的方差 $\mathbf{u}_1^{\mathrm{T}}\mathbf{S}\mathbf{u}_1$。显然，必须进行有约束的最大化，以防止 $\|\mathbf{u}_1\|\to\infty$。适当的约束来自归一化条件 $\mathbf{u}_1^{\mathrm{T}}\mathbf{u}_1=1$。为施加这一约束，引入记为 $\lambda_1$ 的拉格朗日乘子，<span class="margin-reference">附录 E</span>然后对下式作无约束最大化：

$$
\mathbf{u}_1^{\mathrm{T}}\mathbf{S}\mathbf{u}_1+\lambda_1(1-\mathbf{u}_1^{\mathrm{T}}\mathbf{u}_1).
\tag{12.4}
$$

将关于 $\mathbf{u}_1$ 的导数置为零，可知当

$$
\mathbf{S}\mathbf{u}_1=\lambda_1\mathbf{u}_1
\tag{12.5}
$$

时，这个量处于驻点。这说明 $\mathbf{u}_1$ 必须是 $\mathbf{S}$ 的特征向量。如果左乘 $\mathbf{u}_1^{\mathrm{T}}$，并利用 $\mathbf{u}_1^{\mathrm{T}}\mathbf{u}_1=1$，就得到方差

$$
\mathbf{u}_1^{\mathrm{T}}\mathbf{S}\mathbf{u}_1=\lambda_1
\tag{12.6}
$$

因此，当把 $\mathbf{u}_1$ 设为最大特征值 $\lambda_1$ 对应的特征向量时，方差达到最大。这个特征向量称为第一主成分。

我们可以逐个定义其余主成分：每次选择一个新的方向，使它最大化投影后的方差，

<!-- pdf-page: 583 -->

<!-- join-previous-paragraph -->
选择范围限于与先前所有方向正交的方向。对于一般的 $M$ 维投影空间，使投影后数据方差最大的最优线性投影，由数据协方差矩阵 $\mathbf{S}$ 的 $M$ 个特征向量 $\mathbf{u}_1,\ldots,\mathbf{u}_M$ 定义，它们分别对应最大的 $M$ 个特征值 $\lambda_1,\ldots,\lambda_M$。这一结论很容易用归纳法证明。<span class="margin-reference">习题 12.1</span>

概括来说，主成分分析先计算数据集的均值 $\overline{\mathbf{x}}$ 和协方差矩阵 $\mathbf{S}$，再求出 $\mathbf{S}$ 中对应最大 $M$ 个特征值的 $M$ 个特征向量。求特征值、特征向量的算法，以及与特征向量分解有关的其他定理，可见 Golub and Van Loan（1996）。注意，对一个 $D\times D$ 矩阵计算完整的特征向量分解，其计算代价为 $O(D^3)$。如果只打算将数据投影到前 $M$ 个主成分，就只需找到前 $M$ 个特征值和特征向量。可以使用幂法（power method）等更高效的技术（Golub and Van Loan, 1996），其计算量为 $O(MD^2)$；也可以使用 EM 算法。<span class="margin-reference">第 12.2.2 节</span>

### 12.1.2 最小误差表述

现在讨论 PCA 的另一种表述，它以最小化投影误差为基础。为此，引入一组完备的标准正交 $D$ 维基向量 $\{\mathbf{u}_i\}$，其中 $i=1,\ldots,D$，<span class="margin-reference">附录 C</span>满足

$$
\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_j=\delta_{ij}.
\tag{12.7}
$$

由于这组基是完备的，每个数据点都能精确表示为基向量的线性组合：

$$
\mathbf{x}_n=\sum_{i=1}^{D}\alpha_{ni}\mathbf{u}_i
\tag{12.8}
$$

其中，对于不同的数据点，系数 $\alpha_{ni}$ 也不同。这只是把坐标系旋转到由 $\{\mathbf{u}_i\}$ 定义的新坐标系，原来的 $D$ 个分量 $\{x_{n1},\ldots,x_{nD}\}$ 被一组等价分量 $\{\alpha_{n1},\ldots,\alpha_{nD}\}$ 替代。与 $\mathbf{u}_j$ 作内积，并利用标准正交性，得到 $\alpha_{nj}=\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_j$，所以不失一般性地可以写成

$$
\mathbf{x}_n=\sum_{i=1}^{D}(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i.
\tag{12.9}
$$

不过，我们的目标是只用有限的 $M<D$ 个变量来近似表示这个数据点，也就是将它投影到较低维子空间。不失一般性，可以用前 $M$ 个基向量表示这个 $M$ 维线性子空间，于是将每个数据点 $\mathbf{x}_n$ 近似为

$$
\widetilde{\mathbf{x}}_n=\sum_{i=1}^{M}z_{ni}\mathbf{u}_i+\sum_{i=M+1}^{D}b_i\mathbf{u}_i
\tag{12.10}
$$

<!-- pdf-page: 584 -->

其中，$\{z_{ni}\}$ 取决于具体数据点，而 $\{b_i\}$ 是对所有数据点都相同的常数。可以自由选择 $\{\mathbf{u}_i\}$、$\{z_{ni}\}$ 和 $\{b_i\}$，使降维引入的畸变最小。我们用原始数据点 $\mathbf{x}_n$ 与近似点 $\widetilde{\mathbf{x}}_n$ 之间的平方距离在数据集上的平均值，作为畸变度量，因此目标是最小化

$$
J=\frac{1}{N}\sum_{n=1}^{N}\|\mathbf{x}_n-\widetilde{\mathbf{x}}_n\|^2.
\tag{12.11}
$$

首先考虑相对于 $\{z_{ni}\}$ 的最小化。代入 $\widetilde{\mathbf{x}}_n$ 的表达式，将关于 $z_{nj}$ 的导数置为零，并利用标准正交条件，得到

$$
z_{nj}=\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_j
\tag{12.12}
$$

其中 $j=1,\ldots,M$。类似地，将 $J$ 关于 $b_i$ 的导数置为零，并再次利用标准正交关系，得到

$$
b_j=\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_j
\tag{12.13}
$$

其中 $j=M+1,\ldots,D$。代入 $z_{ni}$ 和 $b_i$，再利用一般展开式（12.9），得到

$$
\mathbf{x}_n-\widetilde{\mathbf{x}}_n=\sum_{i=M+1}^{D}\{(\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}\mathbf{u}_i\}\mathbf{u}_i
\tag{12.14}
$$

由此可见，从 $\mathbf{x}_n$ 到 $\widetilde{\mathbf{x}}_n$ 的位移向量，位于与主子空间正交的空间中，因为它是 $i=M+1,\ldots,D$ 对应的基向量 $\{\mathbf{u}_i\}$ 的线性组合，如图 12.2 所示。这符合预期：投影点 $\widetilde{\mathbf{x}}_n$ 必须位于主子空间中，但可以在这个子空间内自由移动，所以正交投影给出最小误差。

因此，可以将畸变度量 $J$ 写成仅依赖于 $\{\mathbf{u}_i\}$ 的函数：

$$
J=\frac{1}{N}\sum_{n=1}^{N}\sum_{i=M+1}^{D}(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i-\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_i)^2=\sum_{i=M+1}^{D}\mathbf{u}_i^{\mathrm{T}}\mathbf{S}\mathbf{u}_i.
\tag{12.15}
$$

剩下的任务是相对于 $\{\mathbf{u}_i\}$ 最小化 $J$。这必须是有约束的最小化，否则只会得到没有意义的结果 $\mathbf{u}_i=0$。约束来自标准正交条件；我们将看到，解可以用协方差矩阵的特征向量展开来表示。在给出正式解法之前，先考虑二维数据空间 $D=2$ 和一维主子空间 $M=1$ 的情形，以直观理解结果。我们要选择方向 $\mathbf{u}_2$，使

<!-- pdf-page: 585 -->

<!-- join-previous-paragraph -->
$J=\mathbf{u}_2^{\mathrm{T}}\mathbf{S}\mathbf{u}_2$ 最小，同时满足归一化约束 $\mathbf{u}_2^{\mathrm{T}}\mathbf{u}_2=1$。用拉格朗日乘子 $\lambda_2$ 施加约束，需要最小化

$$
\widetilde{J}=\mathbf{u}_2^{\mathrm{T}}\mathbf{S}\mathbf{u}_2+\lambda_2(1-\mathbf{u}_2^{\mathrm{T}}\mathbf{u}_2).
\tag{12.16}
$$

将关于 $\mathbf{u}_2$ 的导数置为零，得到 $\mathbf{S}\mathbf{u}_2=\lambda_2\mathbf{u}_2$，所以 $\mathbf{u}_2$ 是 $\mathbf{S}$ 的特征向量，对应特征值 $\lambda_2$。因此，任意一个特征向量都定义了畸变度量的一个驻点。要找到 $J$ 在极小点处的值，将 $\mathbf{u}_2$ 的解代回畸变度量，得到 $J=\lambda_2$。所以，选择两个特征值中较小者对应的特征向量作为 $\mathbf{u}_2$，就能使 $J$ 最小。由此，主子空间应沿着较大特征值对应的特征向量方向。这个结果符合直觉：为使平均平方投影距离最小，主成分子空间应经过数据点的均值，并沿着方差最大的方向。如果两个特征值相等，任意选择主方向都会得到相同的 $J$ 值。

对于任意 $D$ 和任意 $M<D$，最小化 $J$ 的一般解，是将 $\{\mathbf{u}_i\}$ 选为协方差矩阵的特征向量，<span class="margin-reference">习题 12.2</span>满足

$$
\mathbf{S}\mathbf{u}_i=\lambda_i\mathbf{u}_i
\tag{12.17}
$$

其中 $i=1,\ldots,D$，并且照常将特征向量 $\{\mathbf{u}_i\}$ 选为标准正交的。此时，畸变度量为

$$
J=\sum_{i=M+1}^{D}\lambda_i
\tag{12.18}
$$

这就是所有与主子空间正交的特征向量所对应特征值的和。因此，将这些特征向量选为最小的 $D-M$ 个特征值所对应的向量，就能使 $J$ 最小；相应地，定义主子空间的特征向量，就是最大的 $M$ 个特征值所对应的向量。

虽然以上考虑的是 $M<D$，但当 $M=D$ 时，PCA 分析仍然成立。此时不进行降维，只是旋转坐标轴，使其与主成分方向一致。

最后，还有一种与此密切相关的线性降维技术，称为典型相关分析（canonical correlation analysis，CCA）（Hotelling, 1936; Bach and Jordan, 2002）。PCA 处理单个随机变量，而 CCA 考虑两个或更多变量，试图找到一对具有较高互相关的相应线性子空间，使一个子空间中的每个分量都与另一个子空间中的某个单独分量相关。它的解可以表示为一个广义特征向量问题。

### 12.1.3 PCA 的应用

可以用离线手写数字数据集，说明 PCA 在数据压缩中的应用。<span class="margin-reference">附录 A</span>由于协方差矩阵的每个特征向量都是

<!-- pdf-page: 586 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-3.png" alt="离线手写数字的均值图像、前四个主成分图像及其特征值"><figcaption>图 12.3：离线手写数字数据集的均值向量 $\overline{\mathbf{x}}$，以及前四个 PCA 特征向量 $\mathbf{u}_1,\ldots,\mathbf{u}_4$ 和对应的特征值。</figcaption><p class="figure-translation">Mean → 均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
原始 $D$ 维空间中的向量，所以可以把特征向量表示为与数据点大小相同的图像。图 12.3 展示了前五个特征向量及其对应的特征值。将全部特征值按从大到小排列后得到的完整谱，绘于图 12.4（a）。选定 $M$ 值所对应的畸变度量 $J$，等于从第 $M+1$ 个到第 $D$ 个特征值之和；图 12.4（b）给出了它随 $M$ 的变化。

将式（12.12）和式（12.13）代入式（12.10），可以将数据向量 $\mathbf{x}_n$ 的 PCA 近似写为

$$
\widetilde{\mathbf{x}}_n=\sum_{i=1}^{M}(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i+\sum_{i=M+1}^{D}(\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i
\tag{12.19}
$$

$$
{}=\overline{\mathbf{x}}+\sum_{i=1}^{M}(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i-\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i
\tag{12.20}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-4.png" alt="离线数字数据的特征值谱以及舍弃特征值之和随主子空间维数 M 的变化"><figcaption>图 12.4：（a）离线手写数字数据集的特征值谱。（b）舍弃的特征值之和，它表示将数据投影到 $M$ 维主成分子空间所引入的平方和畸变 $J$。</figcaption></figure>

<!-- pdf-page: 587 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-5.png" alt="一个原始数字 3 与保留 1、10、50、250 个主成分时的 PCA 重构"><figcaption>图 12.5：离线手写数字数据集中的一个原始样本，以及保留不同数量 $M$ 个主成分时得到的 PCA 重构。随着 $M$ 增大，重构变得更加准确；当 $M=D=28\times28=784$ 时，重构将完全精确。</figcaption><p class="figure-translation">Original → 原始图像。</p></figure>

这里使用了关系

$$
\overline{\mathbf{x}}=\sum_{i=1}^{D}(\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i
\tag{12.21}
$$

它由 $\{\mathbf{u}_i\}$ 的完备性得到。这实现了对数据集的压缩，因为对于每个数据点，我们用一个 $M$ 维向量替代了 $D$ 维向量 $\mathbf{x}_n$，新向量的分量为 $(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i-\overline{\mathbf{x}}^{\mathrm{T}}\mathbf{u}_i)$。$M$ 越小，压缩程度越高。图 12.5 给出了数字数据集的数据点经 PCA 重构的示例。

主成分分析的另一个应用是数据预处理。此时，目标并非降维，而是通过变换数据集，使其某些性质标准化。这对后续模式识别算法能否成功应用于数据集可能很重要。通常，当原始变量采用不同单位测量，或者变异程度相差很大时，会进行这种处理。例如，在 Old Faithful 数据集中，<span class="margin-reference">附录 A</span>两次喷发之间的间隔通常比一次喷发的持续时间大一个数量级。在对该数据集应用 $K$ 均值算法之前，<span class="margin-reference">第 9.1 节</span>我们先分别对各个变量作线性缩放，使每个变量的均值为零、方差为一。这称为数据标准化（standardizing），标准化后数据的协方差矩阵各分量为

$$
\rho_{ij}=\frac{1}{N}\sum_{n=1}^{N}\frac{(x_{ni}-\overline{x}_i)}{\sigma_i}\frac{(x_{nj}-\overline{x}_j)}{\sigma_j}
\tag{12.22}
$$

其中 $\sigma_i$ 是 $x_i$ 的方差。这个矩阵称为原始数据的相关矩阵（correlation matrix），具有如下性质：如果数据的两个分量 $x_i$ 与 $x_j$ 完全相关，则 $\rho_{ij}=1$；如果它们不相关，则 $\rho_{ij}=0$。

不过，利用 PCA 可以对数据作更进一步的归一化，使其均值为零、协方差为单位矩阵，从而使不同变量去相关。为此，先把特征向量方程（12.17）写成

$$
\mathbf{S}\mathbf{U}=\mathbf{U}\mathbf{L}
\tag{12.23}
$$

<!-- pdf-page: 588 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-6.png" alt="Old Faithful 数据的三个视图：原始数据、逐变量标准化以及白化"><figcaption>图 12.6：对 Old Faithful 数据集进行线性预处理的效果。左图显示原始数据。中图显示将各变量分别标准化为零均值、单位方差后的结果；图中还画出了这个归一化数据集的主轴，范围为 $\pm\lambda_i^{1/2}$。右图显示白化后的结果，其均值为零、协方差为单位矩阵。</figcaption></figure>

其中，$\mathbf{L}$ 是一个 $D\times D$ 对角矩阵，对角元素为 $\lambda_i$；$\mathbf{U}$ 是一个 $D\times D$ 正交矩阵，其各列为 $\mathbf{u}_i$。然后，对每个数据点 $\mathbf{x}_n$ 定义变换后的值

$$
\mathbf{y}_n=\mathbf{L}^{-1/2}\mathbf{U}^{\mathrm{T}}(\mathbf{x}_n-\overline{\mathbf{x}})
\tag{12.24}
$$

其中 $\overline{\mathbf{x}}$ 是式（12.1）定义的样本均值。显然，集合 $\{\mathbf{y}_n\}$ 的均值为零，协方差为单位矩阵，因为

$$
\begin{aligned}
\frac{1}{N}\sum_{n=1}^{N}\mathbf{y}_n\mathbf{y}_n^{\mathrm{T}}&=\frac{1}{N}\sum_{n=1}^{N}\mathbf{L}^{-1/2}\mathbf{U}^{\mathrm{T}}(\mathbf{x}_n-\overline{\mathbf{x}})(\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}\mathbf{U}\mathbf{L}^{-1/2}\\
&=\mathbf{L}^{-1/2}\mathbf{U}^{\mathrm{T}}\mathbf{S}\mathbf{U}\mathbf{L}^{-1/2}=\mathbf{L}^{-1/2}\mathbf{L}\mathbf{L}^{-1/2}=\mathbf{I}.
\end{aligned}
\tag{12.25}
$$

这个操作称为数据白化（whitening）或球形化（sphereing），图 12.6 用 Old Faithful 数据集展示了它的效果。<span class="margin-reference">附录 A</span>

将 PCA 与第 4.1.4 节讨论的 Fisher 线性判别作比较很有启发。两者都可以看作线性降维技术。然而，PCA 是无监督方法，只依赖于 $\mathbf{x}_n$ 的值，而 Fisher 线性判别还使用类别标签信息。图 12.7 的例子突出展示了这一区别。

主成分分析另一个常见应用是数据可视化。此时，将每个数据点投影到二维主子空间（$M=2$），于是数据点 $\mathbf{x}_n$ 被画在笛卡尔坐标 $\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_1$ 和 $\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_2$ 处，其中 $\mathbf{u}_1$ 与 $\mathbf{u}_2$ 分别是最大和第二大特征值对应的特征向量。图 12.8 给出了油流数据集的这种可视化示例。<span class="margin-reference">附录 A</span>

<!-- pdf-page: 589 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-7.png" alt="PCA 的紫红色最大方差方向与 Fisher 判别的绿色方向，红蓝两类数据的分离效果不同"><figcaption>图 12.7：比较主成分分析与 Fisher 线性判别在降维中的作用。这里要将属于两个类别的二维数据投影到一维，两个类别分别用红色和蓝色表示。PCA 选择紫红色直线所示的最大方差方向，导致两个类别严重重叠；Fisher 线性判别则考虑类别标签，将数据投影到绿色直线上，使类别分离得好得多。</figcaption></figure>

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-8.png" alt="油流数据投影到前两个主成分形成的二维散点图，包含红蓝绿三类流型"><figcaption>图 12.8：将油流数据投影到前两个主成分上得到的可视化。红色、蓝色和绿色数据点分别对应层状（laminar）、均匀（homogeneous）和环状（annular）流型。</figcaption></figure>

### 12.1.4 高维数据的 PCA

在主成分分析的某些应用中，数据点的数量少于数据空间的维数。例如，我们可能希望对几百幅图像组成的数据集应用 PCA，而每幅图像都对应于一个可能达到数百万维的向量空间中的点，这些维度来自图像中每个像素的三个颜色值。注意，在 $D$ 维空间中，当 $N<D$ 时，$N$ 个点定义的线性子空间最多只有 $N-1$ 维，所以取大于 $N-1$ 的 $M$ 值进行 PCA 没有多少意义。实际上，进行 PCA 时会发现至少有 $D-N+1$ 个特征值为零，对应的特征向量方向上，数据集的方差为零。此外，求一个 $D\times D$ 矩阵特征向量的典型算法，其计算代价为 $O(D^3)$，因此对于上述图像示例，直接应用 PCA 在计算上不可行。

可以按以下方式解决这一问题。首先，将 $\mathbf{X}$ 定义为一个 $(N\times D)$

<!-- pdf-page: 590 -->

<!-- join-previous-paragraph -->
维的中心化数据矩阵，第 $n$ 行为 $(\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}$。于是，协方差矩阵（12.3）可以写成 $\mathbf{S}=N^{-1}\mathbf{X}^{\mathrm{T}}\mathbf{X}$，相应的特征向量方程变为

$$
\frac{1}{N}\mathbf{X}^{\mathrm{T}}\mathbf{X}\mathbf{u}_i=\lambda_i\mathbf{u}_i.
\tag{12.26}
$$

现在左乘 $\mathbf{X}$，得到

$$
\frac{1}{N}\mathbf{X}\mathbf{X}^{\mathrm{T}}(\mathbf{X}\mathbf{u}_i)=\lambda_i(\mathbf{X}\mathbf{u}_i).
\tag{12.27}
$$

定义 $\mathbf{v}_i=\mathbf{X}\mathbf{u}_i$，则有

$$
\frac{1}{N}\mathbf{X}\mathbf{X}^{\mathrm{T}}\mathbf{v}_i=\lambda_i\mathbf{v}_i
\tag{12.28}
$$

这是 $N\times N$ 矩阵 $N^{-1}\mathbf{X}\mathbf{X}^{\mathrm{T}}$ 的特征向量方程。可见，它具有与原协方差矩阵相同的 $N-1$ 个特征值，而原协方差矩阵还额外具有 $D-N+1$ 个零特征值。因此，可以在较低维空间中求解特征向量问题，将计算代价从 $O(D^3)$ 降至 $O(N^3)$。为确定特征向量，将式（12.28）两边左乘 $\mathbf{X}^{\mathrm{T}}$，得到

$$
\left(\frac{1}{N}\mathbf{X}^{\mathrm{T}}\mathbf{X}\right)(\mathbf{X}^{\mathrm{T}}\mathbf{v}_i)=\lambda_i(\mathbf{X}^{\mathrm{T}}\mathbf{v}_i)
\tag{12.29}
$$

可见，$(\mathbf{X}^{\mathrm{T}}\mathbf{v}_i)$ 是 $\mathbf{S}$ 的一个特征向量，对应特征值 $\lambda_i$。不过要注意，这些特征向量未必已经归一化。为确定适当的归一化，对 $\mathbf{u}_i\propto\mathbf{X}^{\mathrm{T}}\mathbf{v}_i$ 乘以一个常数，使 $\|\mathbf{u}_i\|=1$。假设 $\mathbf{v}_i$ 已归一化为单位长度，就得到

$$
\mathbf{u}_i=\frac{1}{(N\lambda_i)^{1/2}}\mathbf{X}^{\mathrm{T}}\mathbf{v}_i.
\tag{12.30}
$$

概括来说，应用这种方法时，先计算 $\mathbf{X}\mathbf{X}^{\mathrm{T}}$，求出它的特征向量与特征值，再利用式（12.30）计算原始数据空间中的特征向量。

## 12.2 概率 PCA

上一节讨论的 PCA 表述，是将数据线性投影到一个维数低于原始数据空间的子空间。现在将说明，PCA 也可以表示为某个概率潜变量模型的最大似然解。这种重新表述称为概率 PCA（probabilistic PCA），与常规 PCA 相比，它具有以下优点：

- 概率 PCA 表示高斯分布的一种受约束形式，可以限制自由参数的数量，同时仍让模型捕捉数据集中的主要相关性。

<!-- pdf-page: 591 -->

- 可以为 PCA 推导出一种 EM 算法；只需要少量最大特征值对应的特征向量时，这种算法计算效率很高，而且不必在中间步骤计算数据的协方差矩阵。<span class="margin-reference">第 12.2.2 节</span>
- 将概率模型与 EM 结合，就可以处理数据集中的缺失值。
- 可以依据概率原理建立概率 PCA 模型的混合，并用 EM 算法训练。
- 概率 PCA 是对 PCA 进行贝叶斯处理的基础；在这种处理中，主子空间的维数可以自动从数据中确定。<span class="margin-reference">第 12.2.3 节</span>
- 由于存在似然函数，可以将它与其他概率密度模型直接比较。相比之下，常规 PCA 会给靠近主子空间的数据点赋予很低的重构代价，即使这些点离训练数据任意远。
- 概率 PCA 可以用来建模类条件密度，从而应用于分类问题。
- 可以按生成方式运行概率 PCA 模型，从该分布中产生样本。

将 PCA 表述为概率模型的方法，由 Tipping 和 Bishop（1997，1999b）以及 Roweis（1998）独立提出。后面我们将看到，它与因子分析（factor analysis；Basilevsky，1994）密切相关。

概率 PCA 是线性高斯框架的一个简单例子，其中所有边缘分布和条件分布都是高斯分布。我们可以先引入与主成分子空间对应的显式潜变量 $\mathbf{z}$，由此构造概率 PCA。接着，为潜变量定义高斯先验分布 $p(\mathbf{z})$，并为给定潜变量取值时的观测变量 $\mathbf{x}$ 定义高斯条件分布 $p(\mathbf{x}\mid\mathbf{z})$。具体来说，$\mathbf{z}$ 的先验分布是均值为零、协方差为单位矩阵的高斯分布<span class="margin-reference">第 8.1.4 节</span>

$$
p(\mathbf{z})=\mathcal{N}(\mathbf{z}\mid\mathbf{0},\mathbf{I}).
\tag{12.31}
$$

类似地，给定潜变量 $\mathbf{z}$ 的取值时，观测变量 $\mathbf{x}$ 的条件分布也是高斯分布，形式为

$$
p(\mathbf{x}\mid\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{W}\mathbf{z}+\boldsymbol{\mu},\sigma^2\mathbf{I})
\tag{12.32}
$$

其中，$\mathbf{x}$ 的均值是 $\mathbf{z}$ 的一般线性函数，由 $D\times M$ 矩阵 $\mathbf{W}$ 和 $D$ 维向量 $\boldsymbol{\mu}$ 决定。注意，这个分布可以按 $\mathbf{x}$ 的各个元素因子化，也就是说，这是朴素贝叶斯模型的一个例子。<span class="margin-reference">第 8.2.2 节</span>稍后我们将说明，$\mathbf{W}$ 的各列在数据空间中张成一个线性子空间，它就是主子空间。这个模型的另一个参数是标量 $\sigma^2$，它控制条件分布的方差。注意，假定

<!-- pdf-page: 592 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-9.png" alt="概率 PCA 的三个生成过程面板：采样潜变量，将它映射到数据空间，并形成边缘高斯分布"><figcaption>图 12.9：用二维数据空间和一维潜空间，说明概率 PCA 模型的生成观点。生成观测数据点 $\mathbf{x}$ 时，首先从潜变量的先验分布 $p(z)$ 中抽取一个值 $\widehat{z}$，然后从均值为 $\mathbf{w}\widehat{z}+\boldsymbol{\mu}$、协方差为 $\sigma^2\mathbf{I}$ 的各向同性高斯分布中抽取 $\mathbf{x}$ 的值；红色圆圈表示这个高斯分布。绿色椭圆表示边缘分布 $p(\mathbf{x})$ 的等密度轮廓。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
潜变量的分布 $p(\mathbf{z})$ 是均值为零、协方差为单位矩阵的高斯分布，并不损失一般性，因为更一般的高斯分布会产生一个等价的概率模型。<span class="margin-reference">习题 12.4</span>

我们可以从生成的角度看待概率 PCA 模型：先选择潜变量的一个取值，再以这个潜变量值为条件对观测变量采样，就得到观测变量的一个样本值。具体而言，$D$ 维观测变量 $\mathbf{x}$ 定义为 $M$ 维潜变量 $\mathbf{z}$ 的线性变换再加上高斯“噪声”，即

$$
\mathbf{x}=\mathbf{W}\mathbf{z}+\boldsymbol{\mu}+\boldsymbol{\epsilon}
\tag{12.33}
$$

其中，$\mathbf{z}$ 是一个 $M$ 维高斯潜变量，$\boldsymbol{\epsilon}$ 是一个 $D$ 维噪声变量，服从零均值、协方差为 $\sigma^2\mathbf{I}$ 的高斯分布。图 12.9 展示了这一生成过程。注意，这个框架以从潜空间到数据空间的映射为基础，与前面讨论的较为常规的 PCA 观点不同。稍后将利用贝叶斯定理得到从数据空间到潜空间的反向映射。

假设我们希望用最大似然方法确定参数 $\mathbf{W}$、$\boldsymbol{\mu}$ 和 $\sigma^2$ 的值。要写出似然函数，需要观测变量的边缘分布 $p(\mathbf{x})$ 的表达式。根据概率的求和规则和乘积规则，可以将其表示为

$$
p(\mathbf{x})=\int p(\mathbf{x}\mid\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}.
\tag{12.34}
$$

因为这是一个线性高斯模型，所以边缘分布也是高斯分布，具体为<span class="margin-reference">习题 12.7</span>

$$
p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\mathbf{C})
\tag{12.35}
$$

<!-- pdf-page: 593 -->

其中，$D\times D$ 协方差矩阵 $\mathbf{C}$ 定义为

$$
\mathbf{C}=\mathbf{W}\mathbf{W}^{\mathrm{T}}+\sigma^2\mathbf{I}.
\tag{12.36}
$$

也可以更直接地推导这个结果：注意到预测分布是高斯分布，再利用式（12.33）计算其均值和协方差，得到

$$
\mathbb{E}[\mathbf{x}]=\mathbb{E}[\mathbf{W}\mathbf{z}+\boldsymbol{\mu}+\boldsymbol{\epsilon}]=\boldsymbol{\mu}
\tag{12.37}
$$

$$
\begin{aligned}
\operatorname{cov}[\mathbf{x}]&=\mathbb{E}\left[(\mathbf{W}\mathbf{z}+\boldsymbol{\epsilon})(\mathbf{W}\mathbf{z}+\boldsymbol{\epsilon})^{\mathrm{T}}\right]\\
&=\mathbb{E}\left[\mathbf{W}\mathbf{z}\mathbf{z}^{\mathrm{T}}\mathbf{W}^{\mathrm{T}}\right]+\mathbb{E}\left[\boldsymbol{\epsilon}\boldsymbol{\epsilon}^{\mathrm{T}}\right]=\mathbf{W}\mathbf{W}^{\mathrm{T}}+\sigma^2\mathbf{I}
\end{aligned}
\tag{12.38}
$$

这里利用了 $\mathbf{z}$ 和 $\boldsymbol{\epsilon}$ 是独立随机变量、因而不相关这一事实。

直观上，可以把分布 $p(\mathbf{x})$ 想象为拿着一个各向同性高斯“喷罐”，沿主子空间移动，喷出高斯形状的墨水；墨水的密度由 $\sigma^2$ 决定，并按先验分布加权。累积的墨水密度形成一个“薄饼”形状的分布，它表示边缘密度 $p(\mathbf{x})$。

预测分布 $p(\mathbf{x})$ 由参数 $\boldsymbol{\mu}$、$\mathbf{W}$ 和 $\sigma^2$ 决定。不过，这种参数化存在冗余，对应于潜空间坐标的旋转。为说明这一点，考虑矩阵 $\widetilde{\mathbf{W}}=\mathbf{W}\mathbf{R}$，其中 $\mathbf{R}$ 是正交矩阵。利用正交性 $\mathbf{R}\mathbf{R}^{\mathrm{T}}=\mathbf{I}$，可见协方差矩阵 $\mathbf{C}$ 中出现的量 $\widetilde{\mathbf{W}}\widetilde{\mathbf{W}}^{\mathrm{T}}$ 可以写成

$$
\widetilde{\mathbf{W}}\widetilde{\mathbf{W}}^{\mathrm{T}}=\mathbf{W}\mathbf{R}\mathbf{R}^{\mathrm{T}}\mathbf{W}^{\mathrm{T}}=\mathbf{W}\mathbf{W}^{\mathrm{T}}
\tag{12.39}
$$

因此它与 $\mathbf{R}$ 无关。于是，存在一整族矩阵 $\widetilde{\mathbf{W}}$，它们都产生同一个预测分布。这种不变性可以从潜空间中的旋转来理解。后面我们会再讨论模型中独立参数的数量。

计算预测分布时，需要求 $\mathbf{C}^{-1}$，这涉及一个 $D\times D$ 矩阵的求逆。利用矩阵求逆恒等式（C.7），可以减少这一步所需的计算，得到

$$
\mathbf{C}^{-1}=\sigma^{-1}\mathbf{I}-\sigma^{-2}\mathbf{W}\mathbf{M}^{-1}\mathbf{W}^{\mathrm{T}}
\tag{12.40}
$$

其中，$M\times M$ 矩阵 $\mathbf{M}$ 定义为

$$
\mathbf{M}=\mathbf{W}^{\mathrm{T}}\mathbf{W}+\sigma^2\mathbf{I}.
\tag{12.41}
$$

由于求逆的是 $\mathbf{M}$，而不直接对 $\mathbf{C}$ 求逆，计算 $\mathbf{C}^{-1}$ 的代价便从 $O(D^3)$ 降为 $O(M^3)$。

除了预测分布 $p(\mathbf{x})$，我们还需要后验分布 $p(\mathbf{z}\mid\mathbf{x})$。同样，可以直接利用线性高斯模型的结果（2.116）写出<span class="margin-reference">习题 12.8</span>

$$
p(\mathbf{z}\mid\mathbf{x})=\mathcal{N}\left(\mathbf{z}\mid\mathbf{M}^{-1}\mathbf{W}^{\mathrm{T}}(\mathbf{x}-\boldsymbol{\mu}),\sigma^{-2}\mathbf{M}\right).
\tag{12.42}
$$

注意，后验均值依赖于 $\mathbf{x}$，而后验协方差与 $\mathbf{x}$ 无关。

<!-- pdf-page: 594 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-10.png" alt="概率 PCA 的有向图：潜变量 z_n 指向观测变量 x_n，参数为均值、W 和噪声方差，N 表示重复观测"><figcaption>图 12.10：对于包含 $N$ 个 $\mathbf{x}$ 观测值的数据集，概率 PCA 模型可以表示为一个有向图，其中每个观测值 $\mathbf{x}_n$ 都对应于潜变量的一个值 $\mathbf{z}_n$。</figcaption></figure>

### 12.2.1 最大似然 PCA

接下来考虑用最大似然方法确定模型参数。给定由观测数据点组成的数据集 $\mathbf{X}=\{\mathbf{x}_n\}$，概率 PCA 模型可以表示为图 12.10 所示的有向图。根据式（12.35），相应的对数似然函数为

$$
\begin{aligned}
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\mathbf{W},\sigma^2)&=\sum_{n=1}^{N}\ln p(\mathbf{x}_n\mid\mathbf{W},\boldsymbol{\mu},\sigma^2)\\
&=-\frac{ND}{2}\ln(2\pi)-\frac{N}{2}\ln|\mathbf{C}|-\frac{1}{2}\sum_{n=1}^{N}(\mathbf{x}_n-\boldsymbol{\mu})^{\mathrm{T}}\mathbf{C}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}).
\end{aligned}
\tag{12.43}
$$

令对数似然关于 $\boldsymbol{\mu}$ 的导数为零，得到预期的结果 $\boldsymbol{\mu}=\overline{\mathbf{x}}$，其中 $\overline{\mathbf{x}}$ 是式（12.1）定义的数据均值。将这个结果代回去，就可以把对数似然函数写为

$$
\ln p(\mathbf{X}\mid\mathbf{W},\boldsymbol{\mu},\sigma^2)=-\frac{N}{2}\left\{D\ln(2\pi)+\ln|\mathbf{C}|+\operatorname{Tr}\left(\mathbf{C}^{-1}\mathbf{S}\right)\right\}
\tag{12.44}
$$

其中，$\mathbf{S}$ 是式（12.3）定义的数据协方差矩阵。由于对数似然是 $\boldsymbol{\mu}$ 的二次函数，这个解就是唯一的极大值点；计算二阶导数即可确认这一点。

对 $\mathbf{W}$ 和 $\sigma^2$ 进行极大化更复杂，但仍有精确的闭式解。Tipping 和 Bishop（1999b）证明，对数似然函数的所有驻点都可以写成

$$
\mathbf{W}_{\mathrm{ML}}=\mathbf{U}_M(\mathbf{L}_M-\sigma^2\mathbf{I})^{1/2}\mathbf{R}
\tag{12.45}
$$

其中，$\mathbf{U}_M$ 是一个 $D\times M$ 矩阵，其各列可取为数据协方差矩阵 $\mathbf{S}$ 的任意 $M$ 个特征向量；$M\times M$ 对角矩阵 $\mathbf{L}_M$ 的元素为相应的特征值 $\lambda_i$；$\mathbf{R}$ 是任意的 $M\times M$ 正交矩阵。

此外，Tipping 和 Bishop（1999b）还证明，选择最大 $M$ 个特征值对应的 $M$ 个特征向量时，就得到似然函数的最大值，其他解都是鞍点。Roweis（1998）曾独立猜想过一个类似结果，但没有给出证明。

<!-- pdf-page: 595 -->

我们仍然假设，特征向量已按对应特征值的降序排列，因此 $M$ 个主特征向量为 $\mathbf{u}_1,\ldots,\mathbf{u}_M$。此时，$\mathbf{W}$ 的各列定义了标准 PCA 的主子空间。$\sigma^2$ 对应的最大似然解为

$$
\sigma_{\mathrm{ML}}^2=\frac{1}{D-M}\sum_{i=M+1}^{D}\lambda_i
\tag{12.46}
$$

因此，$\sigma_{\mathrm{ML}}^2$ 是被舍弃的各个维度所对应方差的平均值。

由于 $\mathbf{R}$ 是正交矩阵，可以把它解释为 $M\times M$ 潜空间中的旋转矩阵。将 $\mathbf{W}$ 的解代入 $\mathbf{C}$ 的表达式，并利用正交性 $\mathbf{R}\mathbf{R}^{\mathrm{T}}=\mathbf{I}$，可见 $\mathbf{C}$ 与 $\mathbf{R}$ 无关。这正是前面讨论过的结论：潜空间中的旋转不会改变预测密度。在 $\mathbf{R}=\mathbf{I}$ 的特殊情形下，$\mathbf{W}$ 的各列是按方差参数 $\lambda_i-\sigma^2$ 缩放的主成分特征向量。只要注意到独立高斯分布的卷积具有可相加的方差，就能理解这些缩放因子的含义；这里的两个分布分别是潜空间分布和噪声模型。因此，沿特征向量 $\mathbf{u}_i$ 方向的方差 $\lambda_i$，由两部分之和构成：一部分是单位方差的潜空间分布通过 $\mathbf{W}$ 的相应列投影到数据空间后产生的 $\lambda_i-\sigma^2$；另一部分是噪声模型在所有方向上添加的、方差为 $\sigma^2$ 的各向同性贡献。

值得仔细考察一下式（12.36）中协方差矩阵的形式。考虑预测分布在单位向量 $\mathbf{v}$ 指定方向上的方差，其中 $\mathbf{v}^{\mathrm{T}}\mathbf{v}=1$；这个方差为 $\mathbf{v}^{\mathrm{T}}\mathbf{C}\mathbf{v}$。首先，假设 $\mathbf{v}$ 与主子空间正交，也就是说，它是被舍弃的特征向量的某个线性组合。此时 $\mathbf{v}^{\mathrm{T}}\mathbf{U}=0$，因此 $\mathbf{v}^{\mathrm{T}}\mathbf{C}\mathbf{v}=\sigma^2$。所以，模型在正交于主子空间的方向上预测的噪声方差，根据式（12.46），就是被舍弃特征值的平均值。现在假设 $\mathbf{v}=\mathbf{u}_i$，其中 $\mathbf{u}_i$ 是定义主子空间的某个被保留的特征向量。此时 $\mathbf{v}^{\mathrm{T}}\mathbf{C}\mathbf{v}=(\lambda_i-\sigma^2)+\sigma^2=\lambda_i$。换言之，这个模型正确地捕捉了数据沿主轴方向的方差，并用单一的平均值 $\sigma^2$ 近似其余所有方向的方差。

构造最大似然密度模型的一种方法，就是求出数据协方差矩阵的特征向量和特征值，然后利用上面的结果计算 $\mathbf{W}$ 和 $\sigma^2$。此时，为方便起见，可以选择 $\mathbf{R}=\mathbf{I}$。不过，如果通过数值优化似然函数来寻找最大似然解，例如采用共轭梯度之类的算法（Fletcher，1987；Nocedal 和 Wright，1999；Bishop 和 Nabney，2008），或采用 EM 算法，那么得到的 $\mathbf{R}$ 的值基本上是任意的。<span class="margin-reference">第 12.2.2 节</span>这意味着 $\mathbf{W}$ 的各列不一定正交。如果需要正交基，可以对矩阵 $\mathbf{W}$ 作适当的后处理（Golub 和 Van Loan，1996）。另一种做法是修改 EM 算法，使它直接得到标准正交的主方向，并按对应特征值的降序排列（Ahn 和 Oh，2003）。

<!-- pdf-page: 596 -->

潜空间中的旋转不变性是一种统计上的不可辨识性（nonidentifiability），与离散潜变量的混合模型中遇到的情形类似。这里存在一个连续的参数集合，其中所有参数都会产生相同的预测密度；而混合模型中，由分量标签重新编号引起的是离散的不可辨识性。

如果考虑 $M=D$ 的情形，即没有降低维数，那么 $\mathbf{U}_M=\mathbf{U}$ 且 $\mathbf{L}_M=\mathbf{L}$。利用正交性 $\mathbf{U}\mathbf{U}^{\mathrm{T}}=\mathbf{I}$ 和 $\mathbf{R}\mathbf{R}^{\mathrm{T}}=\mathbf{I}$，可见 $\mathbf{x}$ 的边缘分布的协方差 $\mathbf{C}$ 变为

$$
\mathbf{C}=\mathbf{U}(\mathbf{L}-\sigma^2\mathbf{I})^{1/2}\mathbf{R}\mathbf{R}^{\mathrm{T}}(\mathbf{L}-\sigma^2\mathbf{I})^{1/2}\mathbf{U}^{\mathrm{T}}+\sigma^2\mathbf{I}=\mathbf{U}\mathbf{L}\mathbf{U}^{\mathrm{T}}=\mathbf{S}
\tag{12.47}
$$

于是得到无约束高斯分布的标准最大似然解，其协方差矩阵就是样本协方差。

常规 PCA 通常表示为从 $D$ 维数据空间到 $M$ 维线性子空间的点投影。而对于概率 PCA，最自然的表述是通过式（12.33）从潜空间映射到数据空间。在可视化和数据压缩等应用中，可以利用贝叶斯定理将这一映射反向进行。于是，数据空间中的任意点 $\mathbf{x}$ 都可以用它在潜空间中的后验均值和协方差来概括。根据式（12.42），均值为

$$
\mathbb{E}[\mathbf{z}\mid\mathbf{x}]=\mathbf{M}^{-1}\mathbf{W}_{\mathrm{ML}}^{\mathrm{T}}(\mathbf{x}-\overline{\mathbf{x}})
\tag{12.48}
$$

其中 $\mathbf{M}$ 由式（12.41）给出。它投影到数据空间中的点为

$$
\mathbf{W}\mathbb{E}[\mathbf{z}\mid\mathbf{x}]+\boldsymbol{\mu}.
\tag{12.49}
$$

注意，这与正则化线性回归的方程具有相同形式，是对线性高斯模型的似然函数进行极大化的结果。类似地，根据式（12.42），后验协方差为 $\sigma^2\mathbf{M}^{-1}$，并且与 $\mathbf{x}$ 无关。<span class="margin-reference">第 3.3.1 节</span>

如果取极限 $\sigma^2\to 0$，后验均值就简化为

$$
(\mathbf{W}_{\mathrm{ML}}^{\mathrm{T}}\mathbf{W}_{\mathrm{ML}})^{-1}\mathbf{W}_{\mathrm{ML}}^{\mathrm{T}}(\mathbf{x}-\overline{\mathbf{x}})
\tag{12.50}
$$

这表示数据点到潜空间的正交投影，于是我们重新得到标准 PCA 模型。<span class="margin-reference">习题 12.11</span>不过，在这个极限下，后验协方差为零，密度变为奇异的。当 $\sigma^2>0$ 时，与正交投影相比，潜空间中的投影会向原点偏移。<span class="margin-reference">习题 12.12</span>

最后，我们指出，概率 PCA 模型的一个重要作用，是定义一种多元高斯分布：既能控制自由度，也就是独立参数的数量，又能让模型捕捉数据中的主要相关性。回顾一下，一般高斯分布的协方差矩阵有 $D(D+1)/2$ 个独立参数，均值中还另有 $D$ 个参数。<span class="margin-reference">第 2.3 节</span>因此，参数数量随 $D$ 呈二次增长，在高维

<!-- pdf-page: 597 -->

<!-- join-previous-paragraph -->
空间中可能会变得过多。如果把协方差矩阵限制为对角矩阵，就只剩 $D$ 个独立参数，参数数量便随维数线性增长。但此时模型把各变量视为相互独立，因此无法再表示它们之间的任何相关性。概率 PCA 提供了一种巧妙的折中：既能捕捉最显著的 $M$ 个相关性，又能保证参数总数只随 $D$ 线性增长。通过如下计算 PPCA 模型中的自由度，可以看清这一点。协方差矩阵 $\mathbf{C}$ 依赖于大小为 $D\times M$ 的参数 $\mathbf{W}$，以及 $\sigma^2$，参数总数为 $DM+1$。不过，我们已经看到，这种参数化存在一定冗余，对应于潜空间坐标系的旋转。表示这些旋转的正交矩阵 $\mathbf{R}$ 的大小为 $M\times M$。这个矩阵的第一列有 $M-1$ 个独立参数，因为列向量必须归一化为单位长度。第二列有 $M-2$ 个独立参数，因为这一列既要归一化，又要与前一列正交，后面的列依此类推。对这个等差数列求和，可见 $\mathbf{R}$ 共有 $M(M-1)/2$ 个独立参数。因此，协方差矩阵 $\mathbf{C}$ 的自由度为

$$
DM+1-M(M-1)/2.
\tag{12.51}
$$

因此，固定 $M$ 时，这个模型中独立参数的数量只随 $D$ 线性增长。如果取 $M=D-1$，就重新得到完整协方差高斯分布的标准结果。<span class="margin-reference">习题 12.14</span>此时，沿 $D-1$ 个线性无关方向的方差由 $\mathbf{W}$ 的各列控制，其余一个方向上的方差由 $\sigma^2$ 给出。如果 $M=0$，模型就等价于各向同性协方差的情形。

### 12.2.2 PCA 的 EM 算法

我们已经看到，概率 PCA 模型可以表示为对连续潜空间 $\mathbf{z}$ 的边缘化，其中每个数据点 $\mathbf{x}_n$ 都有对应的潜变量 $\mathbf{z}_n$。因此，可以利用 EM 算法求模型参数的最大似然估计。这似乎没有多少意义，因为我们已经得到了最大似然参数值的精确闭式解。不过，在高维空间中，迭代的 EM 过程可能比直接处理样本协方差矩阵具有计算优势。这个 EM 过程还可以扩展到不存在闭式解的因子分析模型。<span class="margin-reference">第 12.2.4 节</span>最后，它还能够依据概率原理处理缺失数据。

遵循 EM 的一般框架，就可以推导出概率 PCA 的 EM 算法。<span class="margin-reference">第 9.4 节</span>具体来说，先写出完整数据的对数似然，再对用“旧”参数值计算出的潜变量后验分布求期望。将这个完整数据对数似然的期望极大化，就得到“新”参数值。由于假设各数据点

<!-- pdf-page: 598 -->

<!-- join-previous-paragraph -->
相互独立，完整数据的对数似然函数具有如下形式

$$
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\mathbf{W},\sigma^2)=\sum_{n=1}^{N}\left\{\ln p(\mathbf{x}_n\mid\mathbf{z}_n)+\ln p(\mathbf{z}_n)\right\}
\tag{12.52}
$$

其中，矩阵 $\mathbf{Z}$ 的第 $n$ 行由 $\mathbf{z}_n$ 给出。我们已经知道，$\boldsymbol{\mu}$ 的精确最大似然解就是式（12.1）定义的样本均值 $\overline{\mathbf{x}}$，在这一步代入 $\boldsymbol{\mu}$ 会比较方便。分别利用潜变量分布和条件分布的表达式（12.31）与（12.32），再对潜变量的后验分布求期望，得到

$$
\begin{aligned}
\mathbb{E}\left[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\mathbf{W},\sigma^2)\right]
&=-\sum_{n=1}^{N}\left\{\frac{D}{2}\ln(2\pi\sigma^2)+\frac{1}{2}\operatorname{Tr}\left(\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\right)\right.\\
&\qquad+\frac{1}{2\sigma^2}\|\mathbf{x}_n-\boldsymbol{\mu}\|^2-\frac{1}{\sigma^2}\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\mathbf{W}^{\mathrm{T}}(\mathbf{x}_n-\boldsymbol{\mu})\\
&\qquad\left.+\frac{1}{2\sigma^2}\operatorname{Tr}\left(\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\mathbf{W}^{\mathrm{T}}\mathbf{W}\right)\right\}.
\end{aligned}
\tag{12.53}
$$

注意，它对后验分布的依赖只通过高斯分布的充分统计量体现出来。因此，在 E 步中，我们使用旧参数值计算

$$
\mathbb{E}[\mathbf{z}_n]=\mathbf{M}^{-1}\mathbf{W}^{\mathrm{T}}(\mathbf{x}_n-\overline{\mathbf{x}})
\tag{12.54}
$$

$$
\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]=\sigma^2\mathbf{M}^{-1}+\mathbb{E}[\mathbf{z}_n]\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}
\tag{12.55}
$$

这两个式子直接来自后验分布（12.42），并利用了标准结果 $\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]=\operatorname{cov}[\mathbf{z}_n]+\mathbb{E}[\mathbf{z}_n]\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}$。这里的 $\mathbf{M}$ 由式（12.41）定义。

在 M 步中，固定后验统计量，对 $\mathbf{W}$ 和 $\sigma^2$ 进行极大化。关于 $\sigma^2$ 的极大化很直接。关于 $\mathbf{W}$ 的极大化则利用式（C.24），得到如下 M 步方程<span class="margin-reference">习题 12.15</span>

$$
\mathbf{W}_{\mathrm{new}}=\left[\sum_{n=1}^{N}(\mathbf{x}_n-\overline{\mathbf{x}})\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\right]\left[\sum_{n=1}^{N}\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\right]^{-1}
\tag{12.56}
$$

$$
\begin{aligned}
\sigma_{\mathrm{new}}^2=\frac{1}{ND}\sum_{n=1}^{N}\biggl\{&\|\mathbf{x}_n-\overline{\mathbf{x}}\|^2-2\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\mathbf{W}_{\mathrm{new}}^{\mathrm{T}}(\mathbf{x}_n-\overline{\mathbf{x}})\\
&+\operatorname{Tr}\left(\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\mathbf{W}_{\mathrm{new}}^{\mathrm{T}}\mathbf{W}_{\mathrm{new}}\right)\biggr\}.
\end{aligned}
\tag{12.57}
$$

概率 PCA 的 EM 算法先初始化参数，然后交替执行两步：在 E 步中，利用式（12.54）和（12.55）计算潜空间后验分布的充分统计量；在 M 步中，利用式（12.56）和（12.57）更新参数值。

PCA 的 EM 算法的一个优点，是在大规模应用中具有较高的计算效率（Roweis，1998）。常规 PCA 基于

<!-- pdf-page: 599 -->

<!-- join-previous-paragraph -->
样本协方差矩阵的特征向量分解，而 EM 方法需要迭代，因此看起来可能不那么有吸引力。不过，在高维空间中，EM 算法每轮迭代的计算效率可能远高于常规 PCA。为说明这一点，注意到协方差矩阵的特征分解需要 $O(D^3)$ 的计算。我们往往只关心前 $M$ 个特征向量及其对应特征值，此时可以采用计算代价为 $O(MD^2)$ 的算法。但是，计算协方差矩阵本身就需要 $O(ND^2)$ 的运算，其中 $N$ 是数据点的数量。快照方法（snapshot method；Sirovich，1987）等算法假设特征向量是数据向量的线性组合，避免直接计算协方差矩阵，但其计算代价为 $O(N^3)$，因此不适用于大型数据集。这里介绍的 EM 算法同样不显式构造协方差矩阵。相应地，计算量最大的步骤是对数据集求和，代价为 $O(NDM)$。当 $D$ 很大且 $M\ll D$ 时，与 $O(ND^2)$ 相比，这可以节省大量计算，足以抵消 EM 算法需要迭代带来的代价。

注意，这个 EM 算法可以实现为在线形式：每次读入一个 $D$ 维数据点，处理后将其丢弃，再考虑下一个数据点。这是因为，E 步中计算的量——一个 $M$ 维向量和一个 $M\times M$ 矩阵——可以针对每个数据点分别计算；而 M 步需要对数据点累加求和，这也可以逐步完成。如果 $N$ 和 $D$ 都很大，这种方法可能很有优势。

由于我们现在有了一个完整的 PCA 概率模型，只要数据是随机缺失的，就可以通过对未观测变量的分布进行边缘化来处理缺失数据。这些缺失值同样可以用 EM 算法处理。图 12.11 给出了将这种方法用于数据可视化的例子。

EM 方法还有一个巧妙的特点：取对应于标准 PCA 的极限 $\sigma^2\to 0$ 时，仍能得到一种有效的类似 EM 的算法（Roweis，1998）。根据式（12.55），E 步中唯一需要计算的量是 $\mathbb{E}[\mathbf{z}_n]$。此外，由于 $\mathbf{M}=\mathbf{W}^{\mathrm{T}}\mathbf{W}$，M 步也简化了。为了突出这个算法的简洁性，将 $\widetilde{\mathbf{X}}$ 定义为一个 $N\times D$ 矩阵，其第 $n$ 行由向量 $\mathbf{x}_n-\overline{\mathbf{x}}$ 给出；类似地，将 $\boldsymbol{\Omega}$ 定义为一个 $D\times M$ 矩阵，其第 $n$ 行由向量 $\mathbb{E}[\mathbf{z}_n]$ 给出。于是，PCA 的 EM 算法的 E 步（12.54）变为

$$
\boldsymbol{\Omega}=(\mathbf{W}_{\mathrm{old}}^{\mathrm{T}}\mathbf{W}_{\mathrm{old}})^{-1}\mathbf{W}_{\mathrm{old}}^{\mathrm{T}}\widetilde{\mathbf{X}}
\tag{12.58}
$$

而 M 步（12.56）的形式为

$$
\mathbf{W}_{\mathrm{new}}=\widetilde{\mathbf{X}}^{\mathrm{T}}\boldsymbol{\Omega}^{\mathrm{T}}(\boldsymbol{\Omega}\boldsymbol{\Omega}^{\mathrm{T}})^{-1}.
\tag{12.59}
$$

同样，这两步可以实现为在线形式。这些方程有如下简单解释。根据前面的讨论，E 步把数据点正交投影到当前估计的主子空间上。相应地，M 步则重新估计主

<!-- pdf-page: 600 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-11.png" alt="油流数据前一百个点的概率 PCA 可视化，左侧使用完整观测，右侧使用随机缺失三成变量值的数据"><figcaption>图 12.11：用概率 PCA 对油流数据集的一部分进行可视化，这里取前 100 个数据点。左图显示各数据点按后验均值投影到主子空间的结果。右图先随机删去 30% 的变量值，再用 EM 处理缺失值。注意，此时每个数据点至少缺失一项测量值，但所得图形与没有缺失值时的结果十分相似。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
子空间，在投影保持不变的情况下，使重构误差的平方最小。<span class="margin-reference">习题 12.17</span>

可以用一个简单的物理类比来说明这个 EM 算法，在 $D=2$、$M=1$ 时尤其容易直观呈现。考虑一组二维数据点，用一根刚性杆表示一维主子空间。现在，把每个数据点用一根服从胡克定律的弹簧连接到杆上，弹簧储存的能量与其长度的平方成正比。在 E 步中，保持杆不动，让各连接点沿杆来回滑动，使能量最小。这样，每个连接点都会独立地移到对应数据点在杆上的正交投影处。在 M 步中，保持连接点固定，然后松开杆，让它运动到能量最小的位置。随后重复 E 步和 M 步，直到满足适当的收敛判据，如图 12.12 所示。

### 12.2.3 贝叶斯 PCA

到目前为止，讨论 PCA 时，我们一直假设主子空间的维数 $M$ 已经给定。在实践中，必须根据应用选择合适的值。对于可视化，通常选择 $M=2$；而对于其他应用，$M$ 的恰当取值可能没有那么明确。一种方法是画出数据集的特征值谱，类似于图 12.4 中离线手写数字数据集的例子，再观察这些特征值是否自然地分成两组：一组是较小的值，另一组是相对较大的值，两组之间有明显的间隔。这种间隔提示了 $M$ 的一个自然选择。然而在实践中，往往看不到这样的间隔。

<!-- pdf-page: 601 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-12.png" alt="用六幅合成数据图展示 PCA 的 EM 算法，红色主轴与青色投影点在 E 步和 M 步之间交替更新"><figcaption>图 12.12：用合成数据说明式（12.58）和（12.59）定义的 PCA 的 EM 算法。（a）数据集 $\mathbf{X}$，数据点以绿色表示，同时画出真正的主成分，表示为按特征值平方根缩放后的特征向量。（b）$\mathbf{W}$ 定义的主子空间的初始配置，以红色表示；潜空间中的点 $\mathbf{Z}$ 投影到数据空间后的结果为 $\mathbf{Z}\mathbf{W}^{\mathrm{T}}$，以青色表示。（c）执行一次 M 步后，保持 $\mathbf{Z}$ 不变，潜空间得到更新。（d）随后执行 E 步，保持 $\mathbf{W}$ 不变，更新 $\mathbf{Z}$ 的值，得到正交投影。（e）第二次 M 步后的结果。（f）第二次 E 步后的结果。</figcaption></figure>

因为概率 PCA 模型具有定义明确的似然函数，我们可以采用交叉验证，选择验证数据集上对数似然最大的维数。<span class="margin-reference">第 1.3 节</span>不过，这种方法的计算代价可能很高，特别是在考虑 PCA 模型的概率混合（Tipping 和 Bishop，1999a）时；此时需要为混合中的每个分量分别确定合适的维数。

既然已经有了 PCA 的概率表述，寻求一种贝叶斯模型选择方法似乎很自然。为此，需要相对于适当的先验分布，将模型参数 $\boldsymbol{\mu}$、$\mathbf{W}$ 和 $\sigma^2$ 边缘化掉。可以用变分框架近似这些无法解析计算的边缘化积分（Bishop，1999b）。随后，对一系列不同的 $M$ 值，比较由变分下界给出的边缘似然值，并选择边缘似然最大的那个值。

这里考虑一种更简单的方法，它基于证据

<!-- pdf-page: 602 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/a-fig-12-13.png" alt="贝叶斯 PCA 的概率图模型，在概率 PCA 的图中加入受超参数 alpha 控制的随机参数矩阵 W"><figcaption>图 12.13：贝叶斯 PCA 的概率图模型，其中参数矩阵 $\mathbf{W}$ 上的分布由超参数向量 $\boldsymbol{\alpha}$ 控制。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
近似，适用于数据点数量相对较多、相应后验分布高度集中的情况（Bishop，1999a）。这种方法为 $\mathbf{W}$ 选择一种特定的先验，使主子空间中的多余维度能够从模型中剪除。这是第 7.2.2 节讨论的自动相关性确定（automatic relevance determination，ARD）的一个例子。具体而言，为 $\mathbf{W}$ 的每一列定义一个独立的高斯先验；这些列正是定义主子空间的向量。每个高斯分布都有独立的方差，由精度超参数 $\alpha_i$ 控制，因此

$$
p(\mathbf{W}\mid\boldsymbol{\alpha})=\prod_{i=1}^{M}\left(\frac{\alpha_i}{2\pi}\right)^{D/2}\exp\left\{-\frac{1}{2}\alpha_i\mathbf{w}_i^{\mathrm{T}}\mathbf{w}_i\right\}
\tag{12.60}
$$

其中，$\mathbf{w}_i$ 是 $\mathbf{W}$ 的第 $i$ 列。所得模型可以用图 12.13 中的有向图表示。

将 $\mathbf{W}$ 积分掉以后，通过极大化边缘似然函数，迭代求出 $\alpha_i$ 的值。这种优化可能使某些 $\alpha_i$ 趋向无穷大，对应的参数向量 $\mathbf{w}_i$ 趋向零，即后验分布变为原点处的 delta 函数，从而得到稀疏解。主子空间的有效维数由取有限值的 $\alpha_i$ 的数量确定，而相应向量 $\mathbf{w}_i$ 可以看作与数据分布建模“相关”。这样，贝叶斯方法就自动在两个目标之间进行权衡：一方面，使用更多向量 $\mathbf{w}_i$，并将每个对应特征值 $\lambda_i$ 都调到适合数据的值，以改善对数据的拟合；另一方面，通过抑制某些 $\mathbf{w}_i$ 向量来降低模型复杂度。前面讨论相关向量机时，已经说明过这种稀疏性的来源。<span class="margin-reference">第 7.2 节</span>

训练过程中，通过极大化下面给出的对数边缘似然，重新估计 $\alpha_i$ 的值

$$
p(\mathbf{X}\mid\boldsymbol{\alpha},\boldsymbol{\mu},\sigma^2)=\int p(\mathbf{X}\mid\mathbf{W},\boldsymbol{\mu},\sigma^2)p(\mathbf{W}\mid\boldsymbol{\alpha})\,\mathrm{d}\mathbf{W}
\tag{12.61}
$$

其中，$p(\mathbf{X}\mid\mathbf{W},\boldsymbol{\mu},\sigma^2)$ 的对数由式（12.43）给出。注意，为简单起见，我们还将 $\boldsymbol{\mu}$ 和 $\sigma^2$ 作为待估计的参数，而不为这些参数定义先验。

<!-- pdf-page: 603 -->

由于这一积分难以计算，我们使用拉普拉斯近似（第 4.4 节）。假设后验分布具有尖锐的峰，这在数据集足够大时会出现，那么关于 $\alpha_i$ 最大化边缘似然所得到的重估方程，就具有如下简单形式（第 3.5.3 节）：

$$
\alpha_i^{\mathrm{new}}=\frac{D}{\mathbf{w}_i^{\mathrm{T}}\mathbf{w}_i}
\tag{12.62}
$$

注意到 $\mathbf{w}_i$ 的维数为 $D$，这个结果即可由（3.98）得到。这些重估步骤与用于确定 $\mathbf{W}$ 和 $\sigma^2$ 的 EM 算法更新交替进行。E 步的方程仍由（12.54）和（12.55）给出。类似地，$\sigma^2$ 的 M 步方程仍由（12.57）给出。唯一的变化是 $\mathbf{W}$ 的 M 步方程，它修改为

$$
\mathbf{W}_{\mathrm{new}}=\left[\sum_{n=1}^N(\mathbf{x}_n-\overline{\mathbf{x}})\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\right]\left[\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]+\sigma^2\mathbf{A}\right]^{-1}
\tag{12.63}
$$

其中 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。与前面一样，$\boldsymbol{\mu}$ 的值由样本均值给出。

如果选择 $M=D-1$，那么，当所有 $\alpha_i$ 都是有限值时，模型表示一个具有完整协方差的高斯分布；当所有 $\alpha_i$ 都趋于无穷大时，模型等价于各向同性高斯分布。因此，模型能够涵盖主子空间有效维数的所有允许值。也可以考虑较小的 $M$，这样会节省计算成本，但会限制子空间的最大维数。图 12.14 比较了这一算法与标准概率 PCA 的结果。

贝叶斯 PCA 提供了一个展示第 11.3 节所讨论的 Gibbs 采样算法的机会。图 12.15 给出了超参数 $\ln\alpha_i$ 的采样示例：数据集位于 $D=4$ 维空间，潜空间的维数为 $M=3$，但数据集是由一个概率 PCA 模型生成的，该模型只有一个方向具有较高方差，其余方向都是低方差噪声。这个结果清楚地显示，后验分布存在三个不同的模态。在每一步迭代中，一个超参数较小，其余两个较大，因此三个潜变量中的两个受到抑制。在 Gibbs 采样过程中，解会在这三个模态之间突然切换。

这里描述的模型只对矩阵 $\mathbf{W}$ 引入了先验。Bishop（1999b）介绍了一种完全贝叶斯的 PCA 处理方式，其中还对 $\boldsymbol{\mu}$、$\sigma^2$ 和 $\boldsymbol{\alpha}$ 引入先验，并使用变分方法求解。关于确定 PCA 模型合适维数的各种贝叶斯方法，参见 Minka（2001c）。

### 12.2.4 因子分析

因子分析是一种线性高斯潜变量模型，与概率 PCA 密切相关。它的定义与概率 PCA 只有一点不同：给定潜变量 $\mathbf{z}$ 时，观测变量 $\mathbf{x}$ 的条件分布

<!-- pdf-page: 604 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-14.png" alt="矩阵 W 的两个 Hinton 图，用面积不同的黑白方块表现各矩阵元素及部分列被抑制的结果"><figcaption>图 12.14：矩阵 $\mathbf{W}$ 的“Hinton 图”，其中每个矩阵元素都表示为一个正方形（白色表示正值，黑色表示负值），其面积与该元素的绝对值成正比。合成数据集包含 $D=10$ 维空间中的 300 个数据点，它们采样自一个高斯分布，该分布在 3 个方向上的标准差为 1.0，在其余 7 个方向上的标准差为 0.5；这是一个 $D=10$ 维数据集，其中 $M=3$ 个方向的方差大于其余 7 个方向。左图显示最大似然概率 PCA 的结果，左图显示贝叶斯 PCA 的相应结果。可以看到，贝叶斯模型能够通过抑制 6 个多余的自由度，发现合适的维数。</figcaption><p class="figure-translation">白色方块：正的矩阵元素；黑色方块：负的矩阵元素；方块面积：相应矩阵元素的绝对值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
采用对角协方差，而不是各向同性协方差，即

$$
p(\mathbf{x}\mid\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{W}\mathbf{z}+\boldsymbol{\mu},\boldsymbol{\Psi})
\tag{12.64}
$$

其中，$\boldsymbol{\Psi}$ 是一个 $D\times D$ 对角矩阵。注意，因子分析模型与概率 PCA 一样，假设给定潜变量 $\mathbf{z}$ 后，观测变量 $x_1,\ldots,x_D$ 相互独立。实质上，因子分析模型将与每个坐标相关的独立方差表示在矩阵 $\boldsymbol{\Psi}$ 中，将变量之间的协方差表示在矩阵 $\mathbf{W}$ 中，从而解释数据中观察到的协方差结构。在因子分析文献中，$\mathbf{W}$ 的各列捕捉观测变量之间的相关性，称为 *因子载荷*（factor loadings）；$\boldsymbol{\Psi}$ 的对角元素表示各变量的独立噪声方差，称为 *独特性*（uniquenesses）。

因子分析的起源与 PCA 同样久远，Everitt（1984）、Bartholomew（1987）和 Basilevsky（1994）的著作中都有关于因子分析的讨论。Lawley（1953）和 Anderson（1963）研究了因子分析与 PCA 之间的联系。他们证明，对于满足 $\boldsymbol{\Psi}=\sigma^2\mathbf{I}$ 的因子分析模型，在似然函数的驻点处，$\mathbf{W}$ 的各列是样本协方差矩阵经过缩放的特征向量，而 $\sigma^2$ 是被舍弃的特征值的平均值。随后，Tipping and Bishop（1999b）证明，当构成 $\mathbf{W}$ 的特征向量选为主特征向量时，对数似然函数达到最大值。

利用（2.115）可知，观测

<!-- pdf-page: 605 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-15.png" alt="贝叶斯 PCA 的三个对数超参数 Gibbs 采样轨迹，分别用红绿蓝曲线显示三个后验模态间的切换"><figcaption>图 12.15：贝叶斯 PCA 的 Gibbs 采样，展示三个 $\alpha$ 值各自的 $\ln\alpha_i$ 随迭代次数变化的曲线，可以看到后验分布三个模态之间的切换。</figcaption><p class="figure-translation">横向：迭代次数；纵向：$\ln\alpha_i$。上、中、下三条轨迹分别对应三个超参数，以红色、绿色、蓝色表示。</p></figure>

<!-- join-previous-paragraph-across-figures -->
变量的边缘分布为 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\mathbf{C})$，其中现在有

$$
\mathbf{C}=\mathbf{W}\mathbf{W}^{\mathrm{T}}+\boldsymbol{\Psi}.
\tag{12.65}
$$

与概率 PCA 一样，这个模型在潜空间旋转下保持不变（习题 12.19）。

历史上，当人们尝试解释各个因子（即 $\mathbf{z}$ 空间中的坐标）时，因子分析曾引发争议。由于这个空间中的旋转造成因子分析不可辨识，这种解释被证明存在问题。不过，从我们的角度看，因子分析是一种潜变量密度模型，我们关心的是潜空间的形式，而不是用来描述它的具体坐标选择。如果希望消除潜空间旋转带来的退化，就必须考虑非高斯的潜变量分布，这会得到独立成分分析（ICA）模型（第 12.4 节）。

可以通过最大似然确定因子分析模型中的参数 $\boldsymbol{\mu}$、$\mathbf{W}$ 和 $\boldsymbol{\Psi}$。$\boldsymbol{\mu}$ 的解仍由样本均值给出。不过，与概率 PCA 不同，$\mathbf{W}$ 不再具有闭式的最大似然解，因此必须通过迭代求得。由于因子分析是一种潜变量模型，可以使用类似于概率 PCA 的 EM 算法（Rubin and Thayer，1982）完成这一点（习题 12.21）。具体来说，E 步方程为

$$
\mathbb{E}[\mathbf{z}_n]=\mathbf{G}\mathbf{W}^{\mathrm{T}}\boldsymbol{\Psi}^{-1}(\mathbf{x}_n-\overline{\mathbf{x}})
\tag{12.66}
$$

$$
\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]=\mathbf{G}+\mathbb{E}[\mathbf{z}_n]\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}
\tag{12.67}
$$

其中定义了

$$
\mathbf{G}=(\mathbf{I}+\mathbf{W}^{\mathrm{T}}\boldsymbol{\Psi}^{-1}\mathbf{W})^{-1}.
\tag{12.68}
$$

注意，这种表达形式只涉及对 $M\times M$ 矩阵求逆，而不是对 $D\times D$ 矩阵求逆（$D\times D$ 对角矩阵 $\boldsymbol{\Psi}$ 除外，它的逆很容易

<!-- pdf-page: 606 -->
<!-- join-previous-paragraph -->
在 $O(D)$ 步内算出），这很方便，因为通常 $M\ll D$。类似地，M 步方程为（习题 12.22）

$$
\mathbf{W}^{\mathrm{new}}=\left[\sum_{n=1}^N(\mathbf{x}_n-\overline{\mathbf{x}})\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\right]\left[\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\right]^{-1}
\tag{12.69}
$$

$$
\boldsymbol{\Psi}^{\mathrm{new}}=\operatorname{diag}\left\{\mathbf{S}-\mathbf{W}_{\mathrm{new}}\frac{1}{N}\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n](\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}\right\}
\tag{12.70}
$$

其中，“diag”算子将矩阵的所有非对角元素设为零。直接应用本书讨论的技术，就可以得到因子分析模型的贝叶斯处理方式。

概率 PCA 与因子分析的另一个区别，是它们在数据集变换下的行为不同（习题 12.25）。对于 PCA 和概率 PCA，如果旋转数据空间中的坐标系，就会得到完全相同的数据拟合，但 $\mathbf{W}$ 矩阵要由相应的旋转矩阵进行变换。对于因子分析，相应的性质则是：如果对数据向量的各个分量分别重新缩放，那么这种变换就会被吸收到 $\boldsymbol{\Psi}$ 各元素相应的重新缩放中。

## 12.3 核 PCA

第 6 章已经介绍，核替换技术允许我们将一个以 $\mathbf{x}^{\mathrm{T}}\mathbf{x}'$ 形式的标量积表达的算法，通过把这些标量积替换为非线性核，推广为更一般的算法。这里将核替换技术应用于主成分分析，从而得到一种称为 *核 PCA*（kernel PCA）的非线性推广（Schölkopf et al.，1998）。

考虑一个由观测 $\{\mathbf{x}_n\}$ 组成的数据集，其中 $n=1,\ldots,N$，每个观测位于 $D$ 维空间中。为了使记号简洁，假设已经从每个向量 $\mathbf{x}_n$ 中减去了样本均值，因此 $\sum_n\mathbf{x}_n=\mathbf{0}$。第一步是将传统 PCA 写成一种形式，使数据向量 $\{\mathbf{x}_n\}$ 仅以标量积 $\mathbf{x}_n^{\mathrm{T}}\mathbf{x}_m$ 的形式出现。回顾主成分由协方差矩阵的特征向量 $\mathbf{u}_i$ 定义：

$$
\mathbf{S}\mathbf{u}_i=\lambda_i\mathbf{u}_i
\tag{12.71}
$$

其中 $i=1,\ldots,D$。这里，$D\times D$ 样本协方差矩阵 $\mathbf{S}$ 定义为

$$
\mathbf{S}=\frac{1}{N}\sum_{n=1}^N\mathbf{x}_n\mathbf{x}_n^{\mathrm{T}},
\tag{12.72}
$$

并且对特征向量归一化，使 $\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_i=1$。

现在考虑将数据映射到一个 $M$ 维特征空间的非线性变换 $\boldsymbol{\phi}(\mathbf{x})$，从而将每个数据点 $\mathbf{x}_n$ 投影为一个点 $\boldsymbol{\phi}(\mathbf{x}_n)$。这样，就可以

<!-- pdf-page: 607 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-16.png" alt="原数据空间中的非线性投影曲线与特征空间中的线性主轴及投影线"><figcaption>图 12.16：核 PCA 的示意图。原数据空间中的数据集（左图），通过非线性变换 $\boldsymbol{\phi}(\mathbf{x})$ 投影到特征空间（右图）。在特征空间中进行 PCA，就得到主成分，其中第一个以蓝色表示，并用向量 $\mathbf{v}_1$ 标记。特征空间中的绿色线表示到第一主成分的线性投影，它们对应于原数据空间中的非线性投影。注意，一般无法用 $\mathbf{x}$ 空间中的一个向量来表示非线性主成分。</figcaption><p class="figure-translation">$x_1$、$x_2$：原数据空间的坐标；$\phi_1$、$\phi_2$：特征空间的坐标；$\mathbf{v}_1$：特征空间中的第一主成分方向。红点表示数据，蓝线表示第一主轴，绿线表示相应投影。</p></figure>

<!-- join-previous-paragraph-across-figures -->
在特征空间中进行标准 PCA，它隐式地在原数据空间中定义了一个非线性主成分模型，如图 12.16 所示。

暂时假设投影后的数据集也具有零均值，即 $\sum_n\boldsymbol{\phi}(\mathbf{x}_n)=\mathbf{0}$。稍后会回到这一点。特征空间中的 $M\times M$ 样本协方差矩阵为

$$
\mathbf{C}=\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}
\tag{12.73}
$$

其特征向量展开由下式定义：

$$
\mathbf{C}\mathbf{v}_i=\lambda_i\mathbf{v}_i
\tag{12.74}
$$

其中 $i=1,\ldots,M$。我们的目标是在不显式进入特征空间运算的情况下，求解这个特征值问题。由 $\mathbf{C}$ 的定义，特征向量方程表明 $\mathbf{v}_i$ 满足

$$
\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\left\{\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\mathbf{v}_i\right\}=\lambda_i\mathbf{v}_i
\tag{12.75}
$$

因此，只要 $\lambda_i>0$，向量 $\mathbf{v}_i$ 就是各 $\boldsymbol{\phi}(\mathbf{x}_n)$ 的线性组合，可以写成

$$
\mathbf{v}_i=\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x}_n).
\tag{12.76}
$$

<!-- pdf-page: 608 -->

将这个展开式代回特征向量方程，得到

$$
\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\sum_{m=1}^N a_{im}\boldsymbol{\phi}(\mathbf{x}_m)=\lambda_i\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x}_n).
\tag{12.77}
$$

关键的一步，是用核函数 $k(\mathbf{x}_n,\mathbf{x}_m)=\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)$ 表达这一结果。为此，在两边乘以 $\boldsymbol{\phi}(\mathbf{x}_l)^{\mathrm{T}}$，得到

$$
\frac{1}{N}\sum_{n=1}^N k(\mathbf{x}_l,\mathbf{x}_n)\sum_{m=1}^{m}a_{im}k(\mathbf{x}_n,\mathbf{x}_m)=\lambda_i\sum_{n=1}^N a_{in}k(\mathbf{x}_l,\mathbf{x}_n).
\tag{12.78}
$$

写成矩阵形式为

$$
\mathbf{K}^2\mathbf{a}_i=\lambda_i N\mathbf{K}\mathbf{a}_i
\tag{12.79}
$$

其中，$\mathbf{a}_i$ 是一个 $N$ 维列向量，其元素为 $a_{ni}$，$n=1,\ldots,N$。通过求解下面的特征值问题，就可以找到 $\mathbf{a}_i$ 的解：

$$
\mathbf{K}\mathbf{a}_i=\lambda_i N\mathbf{a}_i
\tag{12.80}
$$

这里从（12.79）两边各消去了一个因子 $\mathbf{K}$。注意，（12.79）与（12.80）的解，只在 $\mathbf{K}$ 的零特征值所对应的特征向量上存在差异，而这些特征向量不会影响主成分投影（习题 12.26）。

系数 $\mathbf{a}_i$ 的归一化条件，通过要求特征空间中的特征向量归一化来得到。利用（12.76）和（12.80），有

$$
1=\mathbf{v}_i^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N\sum_{m=1}^N a_{in}a_{im}\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)=\mathbf{a}_i^{\mathrm{T}}\mathbf{K}\mathbf{a}_i=\lambda_i N\mathbf{a}_i^{\mathrm{T}}\mathbf{a}_i.
\tag{12.81}
$$

求解特征向量问题后，所得的主成分投影也可以用核函数表达。利用（12.76），点 $\mathbf{x}$ 在第 $i$ 个特征向量上的投影为

$$
y_i(\mathbf{x})=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)=\sum_{n=1}^N a_{in}k(\mathbf{x},\mathbf{x}_n)
\tag{12.82}
$$

因此，它同样由核函数表达。

在原来的 $D$ 维 $\mathbf{x}$ 空间中，有 $D$ 个正交特征向量，因此最多只能找到 $D$ 个线性主成分。不过，特征空间的维数 $M$ 可以远大于 $D$（甚至为无穷），所以非线性主成分的数量可以超过 $D$。但要注意，非零特征值的数量不能超过数据点的数量 $N$，因为即使 $M>N$，特征空间中的协方差矩阵的秩也至多为 $N$。这一点也体现在，核 PCA 所涉及的是 $N\times N$ 矩阵 $\mathbf{K}$ 的特征向量展开。

<!-- pdf-page: 609 -->

到目前为止，我们假设由 $\boldsymbol{\phi}(\mathbf{x}_n)$ 给出的投影数据集具有零均值，但一般并非如此。由于希望避免直接在特征空间中运算，不能简单地计算均值并将它减去。因此，再次完全用核函数来表述算法。中心化后的投影数据点记为 $\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)$，由下式给出：

$$
\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)=\boldsymbol{\phi}(\mathbf{x}_n)-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_l)
\tag{12.83}
$$

相应的 Gram 矩阵元素为

$$
\begin{aligned}
\widetilde{K}_{nm}&=\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)^{\mathrm{T}}\widetilde{\boldsymbol{\phi}}(\mathbf{x}_m)\\
&=\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_l)\\
&\quad-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_l)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)+\frac{1}{N^2}\sum_{j=1}^N\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_j)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_l)\\
&=k(\mathbf{x}_n,\mathbf{x}_m)-\frac{1}{N}\sum_{l=1}^N k(\mathbf{x}_l,\mathbf{x}_m)\\
&\quad-\frac{1}{N}\sum_{l=1}^N k(\mathbf{x}_n,\mathbf{x}_l)+\frac{1}{N^2}\sum_{j=1}^N\sum_{l=1}^N k(\mathbf{x}_j,\mathbf{x}_l).
\end{aligned}
\tag{12.84}
$$

写成矩阵形式为

$$
\widetilde{\mathbf{K}}=\mathbf{K}-\mathbf{1}_N\mathbf{K}-\mathbf{K}\mathbf{1}_N+\mathbf{1}_N\mathbf{K}\mathbf{1}_N
\tag{12.85}
$$

其中，$\mathbf{1}_N$ 表示每个元素都等于 $1/N$ 的 $N\times N$ 矩阵。因此，仅利用核函数就能计算 $\widetilde{\mathbf{K}}$，再用 $\widetilde{\mathbf{K}}$ 确定特征值和特征向量。注意，如果使用线性核 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$，就会恢复标准 PCA 算法这一特殊情形（习题 12.27）。图 12.17 给出了将核 PCA 应用于合成数据集的示例（Schölkopf et al.，1998）。这里，将如下形式的“高斯”核

$$
k(\mathbf{x},\mathbf{x}')=\exp(-\|\mathbf{x}-\mathbf{x}'\|^2/0.1)
\tag{12.86}
$$

应用于合成数据集。图中的线是等高线，沿这些线，在相应主成分上的投影保持不变；这一投影定义为

$$
\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N a_{in}k(\mathbf{x},\mathbf{x}_n).
\tag{12.87}
$$

<!-- pdf-page: 610 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-17.png" alt="高斯核 PCA 的八个特征函数与特征值，按两行四列展示三个红色点簇及投影等高线"><figcaption>图 12.17：核 PCA 的示例，将高斯核应用于二维合成数据集，展示前八个特征函数及其特征值。等高线表示在相应主成分上的投影保持不变的线。注意，前两个特征向量将三个簇分开；接下来的三个特征向量把各个簇分为两半；再接下来的三个特征向量，则沿与前面划分正交的方向，再次将各簇分为两半。</figcaption><p class="figure-translation">Eigenvalue → 特征值。上排从左到右：21.72、21.65、4.11、3.93；下排从左到右：3.66、3.09、2.60、2.53。红色圆点表示数据，曲线表示相应主成分投影的等高线。</p></figure>

核 PCA 的一个明显缺点，是需要求 $N\times N$ 矩阵 $\widetilde{\mathbf{K}}$ 的特征向量，而不是传统线性 PCA 中 $D\times D$ 矩阵 $\mathbf{S}$ 的特征向量。因此，在实际处理大型数据集时，往往使用近似方法。

最后注意，在标准线性 PCA 中，常常只保留较少的 $L<D$ 个特征向量，然后用数据向量 $\mathbf{x}_n$ 在 $L$ 维主子空间上的投影 $\widehat{\mathbf{x}}_n$ 来近似它，这个投影定义为

$$
\widehat{\mathbf{x}}_n=\sum_{i=1}^L(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i.
\tag{12.88}
$$

在核 PCA 中，一般无法这样做。要理解这一点，注意映射 $\boldsymbol{\phi}(\mathbf{x})$ 将 $D$ 维 $\mathbf{x}$ 空间，映射为 $M$ 维特征空间 $\boldsymbol{\phi}$ 中的一个 $D$ 维 *流形*。向量 $\mathbf{x}$ 称为对应点 $\boldsymbol{\phi}(\mathbf{x})$ 的 *原像*（pre-image）。不过，将特征空间中的点投影到该空间的线性 PCA 子空间后，所得点通常不会落在这个非线性的 $D$ 维流形上，因此在数据空间中没有对应的原像。为此，人们提出了寻找近似原像的方法（Bakir et al.，2004）。

<!-- pdf-page: 611 -->

## 12.4 非线性潜变量模型

本章主要讨论了具有连续潜变量的最简单的一类模型，即基于线性高斯分布的模型。除了具有重要的实际用途，这些模型也相对容易分析、容易拟合数据，还可以作为更复杂模型的组成部分。这里简要考虑这个框架的一些推广，它们是非线性模型、非高斯模型，或同时具有这两种性质的模型。

事实上，非线性与非高斯性是相关的：通过非线性的变量变换，可以从一个简单而固定的参考密度（例如高斯密度）得到一般的概率密度（习题 12.28）。稍后会看到，这个思想是若干实用潜变量模型的基础。

### 12.4.1 独立成分分析

首先考虑这样一类模型：观测变量与潜变量之间是线性关系，但潜变量分布是非高斯的。其中重要的一类称为 *独立成分分析*（independent component analysis，ICA）；当潜变量上的分布可以因子化时，就得到这类模型，即

$$
p(\mathbf{z})=\prod_{j=1}^M p(z_j).
\tag{12.89}
$$

为了理解这类模型的作用，考虑两个人同时说话，并用两个麦克风录下他们声音的情形。如果忽略时间延迟和回声等影响，那么在任意时刻，各麦克风接收到的信号，都是两个人声音振幅的线性组合。这个线性组合的系数是常数；如果能从样本数据推断出这些系数，就可以逆转混合过程（假定它是非奇异的），从而得到两个干净的信号，每个信号只包含一个人的声音。这是一类称为 *盲源分离*（blind source separation）的问题的例子，其中“盲”是指只有混合后的数据，既观测不到原始信号源，也观测不到混合系数（Cardoso，1998）。

有时可以用下面的方法处理这类问题（MacKay，2003）：忽略信号的时间性质，将相继样本视为独立同分布。考虑一个生成式模型，其中有两个潜变量，对应于未观测到的语音信号振幅；有两个观测变量，对应于两个麦克风处的信号值。潜变量的联合分布如上所示进行因子化，观测变量则由潜变量的线性组合给出。不需要引入噪声分布，因为潜变量的数量等于观测变量的数量，观测变量的边缘分布一般不会是奇异的。因此，观测变量就是潜变量的确定性线性组合。给定一个观测数据集，

<!-- pdf-page: 612 -->
<!-- join-previous-paragraph -->
这个模型的似然函数就是线性组合系数的函数。使用基于梯度的优化方法最大化对数似然，就得到独立成分分析的一个具体版本。

这种方法要取得成功，要求潜变量具有非高斯分布。要理解这一点，回顾概率 PCA（以及因子分析）中，潜空间的分布是零均值、各向同性高斯分布。因此，如果两种潜变量选择仅相差潜空间中的一次旋转，模型就无法区分它们。可以直接验证这一点：进行变换 $\mathbf{W}\to\mathbf{W}\mathbf{R}$，其中 $\mathbf{R}$ 是满足 $\mathbf{R}\mathbf{R}^{\mathrm{T}}=\mathbf{I}$ 的正交矩阵，边缘密度（12.35）以及似然函数都保持不变，因为（12.36）给出的矩阵 $\mathbf{C}$ 本身就是不变的。将模型推广为允许更一般的高斯潜变量分布，并不会改变这一结论，因为前面已经看到，这样的模型与零均值、各向同性的高斯潜变量模型等价。

还可以从另一个角度理解，为什么线性模型中的高斯潜变量分布不足以找到独立成分：主成分对应于数据空间中坐标系的一次旋转，使协方差矩阵对角化，从而使数据分布在新坐标下不相关。零相关虽然是独立性的必要条件，却不是充分条件（习题 12.29）。在实践中，潜变量分布的一种常见选择是

$$
p(z_j)=\frac{1}{\pi\cosh(z_j)}=\frac{1}{\pi(e^{z_j}+e^{-z_j})}
\tag{12.90}
$$

它比高斯分布具有更重的尾部，反映了许多现实世界中的分布也具有这一性质的观察结果。

最初的 ICA 模型（Bell and Sejnowski，1995），基于对一个由信息最大化定义的目标函数进行优化。概率潜变量表述的一个优点，是有助于提出并构建基本 ICA 的推广。例如，*独立因子分析*（independent factor analysis）（Attias，1999a）考虑这样一种模型：潜变量和观测变量的数量可以不同，观测变量包含噪声，各个潜变量的分布由高斯混合建模，因而具有较大的灵活性。这个模型的对数似然使用 EM 最大化，潜变量的重建则用变分方法近似。人们还研究了许多其他类型的模型，目前已经有大量关于 ICA 及其应用的文献（Jutten and Herault，1991；Comon et al.，1991；Amari et al.，1996；Pearlmutter and Parra，1997；Hyvärinen and Oja，1997；Hinton et al.，2001；Miskin and MacKay，2001；Hojen-Sorensen et al.，2002；Choudrey and Roberts，2003；Chan et al.，2003；Stone，2004）。

### 12.4.2 自联想神经网络

第 5 章在监督学习的背景下讨论了神经网络，网络的作用是根据

<!-- pdf-page: 613 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-18.png" alt="具有输入层、较窄隐藏层和输出层的自联想多层感知机"><figcaption>图 12.18：具有两层权重的自联想多层感知机。通过最小化平方和误差，训练这样的网络将输入向量映射到自身。即使隐藏层使用非线性单元，这样的网络仍然等价于线性主成分分析。为清晰起见，图中省略了表示偏置参数的连线。</figcaption><p class="figure-translation">inputs → 输入；outputs → 输出。$x_1,\ldots,x_D$：输入和输出变量；$z_1,\ldots,z_M$：隐藏单元；上方箭头表示从输入到输出的映射方向。</p></figure>

<!-- join-previous-paragraph-across-figures -->
给定的输入变量值，预测输出变量。不过，神经网络也被应用于无监督学习，用来进行降维。实现方式是使用一个输出数量与输入数量相同的网络，并对一组训练数据优化权重，使输入与输出之间的某种重建误差度量最小。

首先考虑图 12.18 所示的多层感知机，它具有 $D$ 个输入、$D$ 个输出单元和 $M$ 个隐藏单元，其中 $M<D$。用于训练网络的目标就是输入向量本身，因此网络试图将每个输入向量映射到自身。这种网络形成的映射称为 *自联想*（autoassociative）映射。由于隐藏单元的数量少于输入的数量，一般不可能完美重建所有输入向量。因此，通过最小化一个误差函数，来确定网络参数 $\mathbf{w}$；这个函数衡量输入向量与重建结果之间的不匹配程度。具体而言，选择如下形式的平方和误差：

$$
E(\mathbf{w})=\frac{1}{2}\sum_{n=1}^N\|\mathbf{y}(\mathbf{x}_n,\mathbf{w})-\mathbf{x}_n\|^2.
\tag{12.91}
$$

如果隐藏单元的激活函数是线性的，可以证明，误差函数具有唯一的全局最小值，并且在这个最小值处，网络将输入投影到由数据的前 $M$ 个主成分张成的 $M$ 维子空间上（Bourlard and Kamp，1988；Baldi and Hornik，1989）。因此，图 12.18 中通向各隐藏单元的权重向量，构成一组张成主子空间的基。不过要注意，这些向量不必正交，也不必归一化。这个结果并不令人意外，因为主成分分析和该神经网络都在进行线性降维，并最小化同一个平方和误差函数。

人们可能认为，在图 12.18 的网络中，为隐藏单元使用非线性的 sigmoid 激活函数，就能克服线性降维的限制。不过，即使隐藏单元是非线性的，最小误差解仍然是向主成分子空间的投影（Bourlard and Kamp，1988）。因此，用两层神经网络进行降维并没有优势。主成分分析的标准方法（基于奇异值分解）保证能在有限时间内得到正确解，还能生成一组按顺序排列的特征值及相应的标准正交特征向量。

<!-- pdf-page: 614 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-19.png" alt="增加两层非线性隐藏单元的自联想网络，显示从输入到低维中间层的 F1 与从中间层到输出的 F2"><figcaption>图 12.19：增加由非线性单元构成的隐藏层，就得到能够进行非线性降维的自联想网络。</figcaption><p class="figure-translation">inputs → 输入；outputs → 输出；non-linear → 非线性。$x_1,\ldots,x_D$：输入和输出变量；$\mathbf{F}_1$、$\mathbf{F}_2$：网络前半部分和后半部分的映射。两支向上箭头指出具有非线性单元的隐藏层。</p></figure>

不过，如果允许网络增加隐藏层，情况就不同了。考虑图 12.19 所示的四层自联想网络。输出单元仍然是线性的，第二隐藏层中的 $M$ 个单元也可以是线性的，但第一和第三隐藏层使用非线性的 sigmoid 激活函数。网络仍通过最小化误差函数（12.91）来训练。可以将这个网络看成两个依次进行的函数映射 $\mathbf{F}_1$ 和 $\mathbf{F}_2$，如图 12.19 所示。第一个映射 $\mathbf{F}_1$ 将原始的 $D$ 维数据投影到一个 $M$ 维子空间 $\mathcal{S}$，该子空间由第二隐藏层各单元的激活值定义。由于第一隐藏层包含非线性单元，这个映射十分一般，尤其不局限于线性映射。类似地，网络的后半部分定义了一个任意的函数映射，将 $M$ 维空间映射回原来的 $D$ 维输入空间。这有一个简单的几何解释，图 12.20 展示了 $D=3$、$M=2$ 时的情形。

这样的网络实际上进行了非线性主成分分析。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-20.png" alt="三维数据经 F1 映射到二维空间 S，再经 F2 映射为原三维空间中的非平面曲面"><figcaption>图 12.20：当输入数 $D=3$、中间隐藏层单元数 $M=2$ 时，图 12.19 的网络所实现映射的几何解释。函数 $\mathbf{F}_2$ 从 $M$ 维空间 $\mathcal{S}$ 映射到 $D$ 维空间，因此定义了空间 $\mathcal{S}$ 嵌入原始 $\mathbf{x}$ 空间的方式。由于映射 $\mathbf{F}_2$ 可以是非线性的，$\mathcal{S}$ 的嵌入也可以不是平面，如图所示。映射 $\mathbf{F}_1$ 则定义了从原始 $D$ 维空间中的点到 $M$ 维子空间 $\mathcal{S}$ 的投影。</figcaption><p class="figure-translation">$x_1,x_2,x_3$：原数据空间的坐标；$z_1,z_2$：中间空间的坐标；$\mathcal{S}$：二维中间空间；$\mathbf{F}_1$：到中间空间的映射；$\mathbf{F}_2$：回到原数据空间的映射。</p></figure>

<!-- pdf-page: 615 -->
<!-- join-previous-paragraph-across-figures -->
它的优点是不局限于线性变换，同时又包含标准主成分分析这一特殊情形。不过，训练网络现在涉及一个非线性优化问题，因为误差函数（12.91）不再是网络参数的二次函数。必须使用计算量较大的非线性优化方法，并且可能找到误差函数的一个次优局部最小值。此外，必须在训练网络之前指定子空间的维数。

### 12.4.3 非线性流形建模

前面已经指出，许多自然数据源对应于嵌入较高维观测数据空间中的低维非线性流形，并且可能带有噪声。与更一般的方法相比，显式地刻画这一性质，可以改进密度建模。这里简要介绍一些尝试实现这一目标的技术。

建模非线性结构的一种方式，是组合多个线性模型，从而对流形作分段线性近似。例如，可以使用基于欧氏距离的 K 均值等聚类技术，将数据集划分为若干局部组，再对每一组应用标准 PCA。更好的方法是使用重建误差来决定簇归属（Kambhatla and Leen，1997；Hinton et al.，1997），因为这样每个阶段都在优化同一个代价函数。不过，由于缺乏整体的密度模型，这些方法仍然存在局限。使用概率 PCA 时，只要考虑一个各分量都是概率 PCA 模型的混合分布，就能直接定义一个完全概率化的模型（Tipping and Bishop，1999a）。这样的模型既有对应于离散混合的离散潜变量，也有连续潜变量，并且可以使用 EM 算法最大化似然函数。基于变分推断的完全贝叶斯处理（Bishop and Winn，2000），能够从数据推断混合分量的数量，以及各个模型的有效维数。这个模型还有许多变体，例如让不同混合分量共享 $\mathbf{W}$ 矩阵或噪声方差等参数，或者将各向同性噪声分布替换为对角协方差的分布，从而得到因子分析器的混合（Ghahramani and Hinton，1996a；Ghahramani and Beal，2000）。还可以对概率 PCA 混合模型进行层次扩展，得到一种交互式数据可视化算法（Bishop and Tipping，1998）。

除了考虑线性模型的混合，也可以考虑单个非线性模型。回顾传统 PCA，它寻找一个在最小二乘意义下接近数据的线性子空间。这个概念可以通过 *主曲线*（principal curves）的形式，推广到一维非线性曲面（Hastie and Stuetzle，1989）。可以用向量值函数 $\mathbf{f}(\lambda)$，描述 $D$ 维数据空间中的一条曲线；这个向量的每个元素都是标量 $\lambda$ 的函数。曲线有许多可能的参数化方式，其中一个自然的选择是沿曲线的弧长。对于数据空间中任意给定的点 $\widehat{\mathbf{x}}$，可以找到曲线上与它的欧氏距离最近的点。将这个点记为

<!-- pdf-page: 616 -->
<!-- join-previous-paragraph -->
$\lambda=g_{\mathbf{f}}(\mathbf{x})$，因为它依赖于具体的曲线 $\mathbf{f}(\lambda)$。对于连续的数据密度 $p(\mathbf{x})$，主曲线定义为满足如下性质的曲线：曲线上的每一个点，都是数据空间中所有投影到该点的数据点的均值，即

$$
\mathbb{E}[\mathbf{x}\mid g_{\mathbf{f}}(\mathbf{x})=\lambda]=\mathbf{f}(\lambda).
\tag{12.92}
$$

对于给定的连续密度，可以存在多条主曲线。在实践中，我们关心的是有限数据集，并且也希望将注意力限制在光滑曲线上。Hastie and Stuetzle（1989）提出了一个寻找这类主曲线的两阶段迭代过程，有些类似于 PCA 的 EM 算法。先用第一主成分初始化曲线，然后交替执行数据投影步骤和曲线重估步骤。在投影步骤中，将每个数据点分配到一个 $\lambda$ 值，它对应于曲线上最近的点。随后在重估步骤中，曲线上的每个点由一个加权平均给出：对投影到曲线上邻近位置的数据点进行加权，其中在曲线上距离最近的点具有最大权重。当子空间被限制为线性时，这个过程收敛到第一主成分，并等价于求协方差矩阵最大特征值所对应特征向量的幂法。主曲线可以推广为称作 *主曲面*（principal surfaces）的多维流形，但由于高维数据平滑很困难，即使对二维流形也是如此，这种推广的应用一直有限。

PCA 经常用于将数据集投影到低维空间（例如二维空间），以实现可视化。另一种具有类似目标的线性技术是 *多维尺度分析*（multidimensional scaling，MDS）（Cox and Cox，2000）。它寻找数据的低维投影，使数据点之间的两两距离尽可能保持不变，这涉及求距离矩阵的特征向量。当使用欧氏距离时，它得到的结果与 PCA 等价。MDS 的概念可以推广到以相似度矩阵指定的多种数据类型，从而得到非度量 MDS。

另有两种用于降维和数据可视化的非概率方法值得介绍。*局部线性嵌入*（locally linear embedding，LLE）（Roweis and Saul，2000）首先计算一组系数，使每个数据点都能最好地由其邻居重建。这些系数被设定为对该数据点及其邻居的旋转、平移和缩放不变，因此刻画了邻域的局部几何性质。随后，LLE 在保持这些邻域系数不变的条件下，将高维数据点映射到低维空间。如果某个数据点的局部邻域可以视为线性，就可以通过平移、旋转和缩放的组合来实现这一变换，保持数据点与其邻居形成的夹角不变。由于权重对这些变换不变，我们期望同样的权重值，能够像在高维数据空间中一样，在低维空间中重建数据点。尽管这是非线性方法，LLE 的优化过程并不存在局部最小值。

在 *等距特征映射*（isometric feature mapping，isomap）（Tenenbaum et al.，2000）中，目标是使用 MDS 将数据投影到低维空间，但这里的不相似度，是由沿流形

<!-- pdf-page: 617 -->
<!-- join-previous-paragraph -->
测得的测地距离定义的。例如，如果两个点位于一个圆上，那么测地距离是沿圆周测得的弧长，而不是沿连接两点的弦测得的直线距离。算法首先为每个数据点定义邻域，可以寻找 $K$ 个最近邻，也可以寻找半径为 $\epsilon$ 的球内的所有点。然后通过连接所有相邻点来构造一个图，并用欧氏距离标记这些连接。任意一对点之间的测地距离，就由连接它们的最短路径上各弧段长度之和近似（最短路径本身用标准算法求得）。最后，将度量 MDS 应用于测地距离矩阵，得到低维投影。

本章主要关注观测变量为连续变量的模型。也可以考虑连续潜变量与离散观测变量相结合的模型，从而得到 *潜在特质模型*（latent trait models）（Bartholomew，1987）。在这种情况下，即使潜变量与观测变量之间是线性关系，也无法解析地对连续潜变量进行边缘化，因此需要更复杂的技术。Tipping（1999）在一个具有二维潜空间的模型中使用变分推断，使二元数据集能够像使用 PCA 可视化连续数据那样进行可视化。注意，这个模型是第 4.5 节讨论的贝叶斯逻辑回归问题的对偶。在逻辑回归中，特征向量 $\boldsymbol{\phi}_n$ 有 $N$ 个观测，它们由单个参数向量 $\mathbf{w}$ 参数化；而在潜空间可视化模型中，只有一个潜空间变量 $\mathbf{x}$（对应于 $\boldsymbol{\phi}$），以及潜变量的 $N$ 个副本 $\mathbf{w}_n$。Collins et al.（2002）介绍了将概率潜变量模型推广到一般指数族分布的方法。

前面已经指出，对高斯随机变量施加适当的非线性变换，可以构造任意分布。一个称为 *密度网络*（density network）的通用潜变量模型（MacKay，1995；MacKay and Gibbs，1999）利用了这一点，其中非线性函数由多层神经网络控制。如果网络具有足够多的隐藏单元，就能以任意要求的精度近似给定的非线性函数（第 5 章）。这种灵活模型的代价是，为得到似然函数而必须进行的潜变量边缘化，不再能解析求解。于是，改用蒙特卡洛技术，从高斯先验中抽取样本来近似似然（第 11 章）。对潜变量的边缘化就变成了一个简单求和，每个样本对应其中一项。不过，为了准确表示边缘分布，可能需要大量采样点，因此这一过程的计算成本可能很高。

如果对非线性函数的形式加以限制，并适当选择潜变量分布，就可以构造一种既非线性又能高效训练的潜变量模型。*生成拓扑映射*（generative topographic mapping，GTM）（Bishop et al.，1996；Bishop et al.，1997a；Bishop et al.，1998b）所用的潜变量分布，由潜空间（通常是二维空间）中规则排列的有限个 $\delta$ 函数网格定义。这样，对潜空间的边缘化只需将各个网格位置的贡献相加。

<!-- pdf-page: 618 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-21.png" alt="油流数据的 PCA 与 GTM 二维可视化，左侧点簇重叠较多，右侧各组更清楚地分开"><figcaption>图 12.21：油流数据集的可视化，左图使用 PCA，右图使用 GTM。对于 GTM 模型，每个数据点画在其潜空间后验分布的均值位置。GTM 模型的非线性，使各组数据点之间的分离更加清楚。</figcaption><p class="figure-translation">左图：PCA；右图：GTM。红色叉号、蓝色加号和绿色圆圈表示数据的三个类别。</p></figure>

非线性映射由一个线性回归模型给出，它允许一般的非线性，同时仍是可调参数的线性函数（第 3 章）。注意，线性回归模型通常受到维数灾难的限制（第 1.4 节），但这个限制不会在 GTM 中出现，因为无论数据空间的维数是多少，流形通常只有二维。这两个选择带来的结果是，似然函数可以解析地写成闭式，并使用 EM 算法高效优化。所得 GTM 模型为数据集拟合一个二维非线性流形；通过计算各数据点在潜空间上的后验分布，就可以将它们投影回潜空间，以实现可视化。图 12.21 比较了使用线性 PCA 与非线性 GTM 对油流数据集进行可视化的结果。

GTM 可以看作更早的一种模型——*自组织映射*（self organizing map，SOM）（Kohonen，1982；Kohonen，1995）——的概率版本。SOM 也用规则排列的离散点表示二维非线性流形。它有些类似于 K 均值算法：先将数据点分配给附近的原型向量，再更新这些原型。最初，原型随机分布；训练过程中，它们“自组织”起来，以近似一个光滑流形。不过，与 K 均值不同，SOM 并不优化任何定义明确的代价函数（Erwin et al.，1992），因此难以设置模型参数和判断收敛。此外，也不能保证一定会发生“自组织”，因为这取决于是否为具体数据集选择了合适的参数值。

相比之下，GTM 优化的是对数似然函数，所得模型在数据空间中定义了一个概率密度。事实上，它对应于一个受约束的高斯混合模型：所有分量共享同一个方差，均值则被限制在一个光滑的二维流形上。这种概率

<!-- pdf-page: 619 -->
<!-- join-previous-paragraph -->
基础也使 GTM 的推广十分直接（Bishop et al.，1998a），例如贝叶斯处理、缺失值处理、依据明确原理推广到离散变量、使用高斯过程定义流形（第 6.4 节），或者构造层次 GTM 模型（Tino and Nabney，2002）。

由于 GTM 中的流形被定义为一个连续曲面，而不像 SOM 那样只在原型向量处定义，因此可以计算 *放大因子*（magnification factors），它对应于为拟合数据集所需的流形局部伸展和压缩（Bishop et al.，1997b）；还可以计算流形的 *方向曲率*（directional curvatures）（Tino et al.，2001）。将这些量与投影后的数据一起可视化，可以更深入地了解模型。

## 习题

**12.1（⋆⋆）www** 本题使用数学归纳法证明：使投影数据方差最大的、到 $M$ 维子空间的线性投影，由数据协方差矩阵 $\mathbf{S}$ 的最大 $M$ 个特征值所对应的 $M$ 个特征向量定义，其中 $\mathbf{S}$ 由（12.3）给出。第 12.1 节已经证明了 $M=1$ 时的结果。现在假设这一结果对某个一般的 $M$ 值成立，证明它因此也对维数 $M+1$ 成立。为此，首先令投影数据的方差关于向量 $\mathbf{u}_{M+1}$ 的导数为零，这个向量定义数据空间中的新方向。同时要求 $\mathbf{u}_{M+1}$ 与已有向量 $\mathbf{u}_1,\ldots,\mathbf{u}_M$ 正交，并归一化为单位长度。使用拉格朗日乘子施加这些约束（附录 E）。然后，利用向量 $\mathbf{u}_1,\ldots,\mathbf{u}_M$ 的标准正交性质，证明新向量 $\mathbf{u}_{M+1}$ 是 $\mathbf{S}$ 的特征向量。最后，证明当选择与特征向量 $\lambda_{M+1}$ 对应的那个特征向量时，方差达到最大；这里特征值已按从大到小排列。

**12.2（⋆⋆）** 证明，在标准正交约束（12.7）下，关于 $\mathbf{u}_i$ 最小化（12.15）给出的 PCA 畸变度量 $J$，会在 $\mathbf{u}_i$ 是数据协方差矩阵 $\mathbf{S}$ 的特征向量时取得最小值。为此，引入一个拉格朗日乘子矩阵 $\mathbf{H}$，每个约束对应一个乘子，使修改后的畸变度量写成如下矩阵形式：

$$
\widetilde{J}=\operatorname{Tr}\left\{\widehat{\mathbf{U}}^{\mathrm{T}}\mathbf{S}\widehat{\mathbf{U}}\right\}+\operatorname{Tr}\left\{\mathbf{H}(\mathbf{I}-\widehat{\mathbf{U}}^{\mathrm{T}}\widehat{\mathbf{U}})\right\}
\tag{12.93}
$$

其中，$\widehat{\mathbf{U}}$ 是一个 $D\times(D-M)$ 矩阵，其各列由 $\mathbf{u}_i$ 给出。现在关于 $\widehat{\mathbf{U}}$ 最小化 $\widetilde{J}$，证明解满足 $\mathbf{S}\widehat{\mathbf{U}}=\widehat{\mathbf{U}}\mathbf{H}$。显然，一个可能的解是 $\widehat{\mathbf{U}}$ 的各列为 $\mathbf{S}$ 的特征向量，此时 $\mathbf{H}$ 是包含相应特征值的对角矩阵。为了得到一般解，证明可以假设 $\mathbf{H}$ 是对称矩阵，并利用它的特征向量展开，证明 $\mathbf{S}\widehat{\mathbf{U}}=\widehat{\mathbf{U}}\mathbf{H}$ 的一般解给出的 $\widetilde{J}$ 值，与 $\widehat{\mathbf{U}}$ 的各列为

<!-- pdf-page: 620 -->
<!-- join-previous-paragraph -->
$\mathbf{S}$ 的特征向量时的特殊解相同。由于这些解全部等价，选择特征向量解会比较方便。

**12.3（⋆）** 假设特征向量 $\mathbf{v}_i$ 的长度为一，验证（12.30）定义的特征向量也归一化为单位长度。

**12.4（⋆）www** 假设将概率 PCA 模型中零均值、单位协方差的潜空间分布（12.31），替换为形式为 $\mathcal{N}(\mathbf{z}\mid\mathbf{m},\boldsymbol{\Sigma})$ 的一般高斯分布。通过重新定义模型参数，证明对于任意有效的 $\mathbf{m}$ 和 $\boldsymbol{\Sigma}$ 选择，这都会使观测变量的边缘分布 $p(\mathbf{x})$ 得到相同的模型。

**12.5（⋆⋆）** 设 $\mathbf{x}$ 是一个 $D$ 维随机变量，服从高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$。考虑 $M$ 维随机变量 $\mathbf{y}=\mathbf{A}\mathbf{x}+\mathbf{b}$，其中 $\mathbf{A}$ 是 $M\times D$ 矩阵。证明 $\mathbf{y}$ 也服从高斯分布，并求其均值和协方差的表达式。分别讨论 $M<D$、$M=D$ 和 $M>D$ 时这个高斯分布的形式。

**12.6（⋆）www** 为第 12.2 节描述的概率 PCA 模型画出有向概率图，将观测变量 $\mathbf{x}$ 的各分量明确地分别表示为不同节点。由此验证，概率 PCA 模型具有与第 8.2.2 节讨论的朴素贝叶斯模型相同的独立性结构。

**12.7（⋆⋆）** 利用一般分布的均值和协方差结果（2.270）和（2.271），推导概率 PCA 模型中边缘分布 $p(\mathbf{x})$ 的结果（12.35）。

**12.8（⋆⋆）www** 利用结果（2.116），证明概率 PCA 模型的后验分布 $p(\mathbf{z}\mid\mathbf{x})$ 由（12.42）给出。

**12.9（⋆）** 验证，对于概率 PCA 模型，关于参数 $\boldsymbol{\mu}$ 最大化对数似然（12.43），会得到 $\boldsymbol{\mu}_{\mathrm{ML}}=\overline{\mathbf{x}}$，其中 $\overline{\mathbf{x}}$ 是数据向量的均值。

**12.10（⋆⋆）** 通过计算概率 PCA 模型的对数似然函数（12.43）关于参数 $\boldsymbol{\mu}$ 的二阶导数，证明驻点 $\boldsymbol{\mu}_{\mathrm{ML}}=\overline{\mathbf{x}}$ 是唯一的最大值点。

**12.11（⋆⋆）www** 证明，当 $\sigma^2\to0$ 时，概率 PCA 模型的后验均值变成到主子空间的正交投影，与传统 PCA 一样。

**12.12（⋆⋆）** 对于 $\sigma^2>0$，证明相对于正交投影，概率 PCA 模型的后验均值向原点偏移。

**12.13（⋆⋆）** 证明，按照传统 PCA 的最小二乘投影代价，概率 PCA 下对数据点的最优重建为

$$
\widetilde{\mathbf{x}}=\mathbf{W}_{\mathrm{ML}}(\mathbf{W}_{\mathrm{ML}}^{\mathrm{T}}\mathbf{W}_{\mathrm{ML}})^{-1}\mathbf{M}\mathbb{E}[\mathbf{z}\mid\mathbf{x}].
\tag{12.94}
$$

<!-- pdf-page: 621 -->

**12.14（⋆）** 对于具有 $M$ 维潜空间和 $D$ 维数据空间的概率 PCA 模型，协方差矩阵中独立参数的数量由（12.51）给出。验证，当 $M=D-1$ 时，独立参数的数量与一般协方差高斯分布相同；当 $M=0$ 时，则与各向同性协方差的高斯分布相同。

**12.15（⋆⋆）www** 通过最大化（12.53）给出的完整数据对数似然的期望，推导概率 PCA 模型的 M 步方程（12.56）和（12.57）。

**12.16（⋆⋆⋆）** 图 12.11 展示了将概率 PCA 应用于部分数据值随机缺失的数据集。推导在这种情况下最大化概率 PCA 模型似然函数的 EM 算法。注意，现在 $\{\mathbf{z}_n\}$ 以及向量 $\{\mathbf{x}_n\}$ 中缺失的数据分量，都是潜变量。证明，在所有数据值均被观测到的特殊情况下，这一算法退化为第 12.2.2 节推导的概率 PCA 的 EM 算法。

**12.17（⋆⋆）www** 设 $\mathbf{W}$ 是一个 $D\times M$ 矩阵，其各列定义了嵌入 $D$ 维数据空间中的 $M$ 维线性子空间；$\boldsymbol{\mu}$ 是一个 $D$ 维向量。给定数据集 $\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，可以通过一组 $M$ 维向量 $\{\mathbf{z}_n\}$ 的线性映射来近似数据点，即用 $\mathbf{W}\mathbf{z}_n+\boldsymbol{\mu}$ 近似 $\mathbf{x}_n$。相应的平方和重建代价为

$$
J=\sum_{n=1}^N\|\mathbf{x}_n-\boldsymbol{\mu}-\mathbf{W}\mathbf{z}_n\|^2.
\tag{12.95}
$$

首先证明，关于 $\boldsymbol{\mu}$ 最小化 $J$，会得到一个类似的表达式，其中 $\mathbf{x}_n$ 和 $\mathbf{z}_n$ 分别替换为零均值变量 $\mathbf{x}_n-\overline{\mathbf{x}}$ 和 $\mathbf{z}_n-\overline{\mathbf{z}}$，这里 $\overline{\mathbf{x}}$ 和 $\overline{\mathbf{z}}$ 表示样本均值。然后证明，在固定 $\mathbf{W}$ 时，关于 $\mathbf{z}_n$ 最小化 $J$ 会得到 PCA 的 E 步（12.58）；而在固定 $\{\mathbf{z}_n\}$ 时，关于 $\mathbf{W}$ 最小化 $J$ 会得到 PCA 的 M 步（12.59）。

**12.18（⋆）** 推导第 12.2.4 节描述的因子分析模型中，独立参数数量的表达式。

**12.19（⋆⋆）www** 证明，第 12.2.4 节描述的因子分析模型在潜空间坐标的旋转下保持不变。

**12.20（⋆⋆）** 通过考虑二阶导数，证明第 12.2.4 节讨论的因子分析模型的对数似然函数，关于参数 $\boldsymbol{\mu}$ 的唯一驻点，由（12.1）定义的样本均值给出。进一步证明，这个驻点是最大值点。

**12.21（⋆⋆）** 推导因子分析的 EM 算法中 E 步的公式（12.66）和（12.67）。注意，根据习题 12.20 的结果，参数 $\boldsymbol{\mu}$ 可以替换为样本均值 $\overline{\mathbf{x}}$。

<!-- pdf-page: 622 -->

**12.22（⋆⋆）** 写出因子分析模型的完整数据对数似然期望的表达式，并由此推导相应的 M 步方程（12.69）和（12.70）。

**12.23（⋆）www** 画一个有向概率图模型，表示概率 PCA 模型的离散混合，其中每个 PCA 模型都有自己的 $\mathbf{W}$、$\boldsymbol{\mu}$ 和 $\sigma^2$ 值。然后修改这个图，使这些参数值在混合的各分量之间共享。

**12.24（⋆⋆⋆）** 第 2.3.7 节已经看到，Student t 分布可以看作高斯分布的无限混合，其中对一个连续潜变量进行边缘化。利用这一表示，为给定观测数据点集的多元 Student t 分布，构造最大化其对数似然函数的 EM 算法，并推导 E 步和 M 步方程的形式。

**12.25（⋆⋆）www** 考虑一个线性高斯潜变量模型，它的潜空间分布为 $p(\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{0},\mathbf{I})$，观测变量的条件分布为 $p(\mathbf{x}\mid\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{W}\mathbf{z}+\boldsymbol{\mu},\boldsymbol{\Phi})$，其中 $\boldsymbol{\Phi}$ 是任意对称正定的噪声协方差矩阵。现在假设对数据变量进行非奇异线性变换 $\mathbf{x}\to\mathbf{A}\mathbf{x}$，其中 $\mathbf{A}$ 是 $D\times D$ 矩阵。如果 $\boldsymbol{\mu}_{\mathrm{ML}}$、$\mathbf{W}_{\mathrm{ML}}$ 和 $\boldsymbol{\Phi}_{\mathrm{ML}}$ 表示对应于原始未变换数据的最大似然解，证明 $\mathbf{A}\boldsymbol{\mu}_{\mathrm{ML}}$、$\mathbf{A}\mathbf{W}_{\mathrm{ML}}$ 和 $\mathbf{A}\boldsymbol{\Phi}_{\mathrm{ML}}\mathbf{A}^{\mathrm{T}}$ 表示对应于变换后数据集的最大似然解。最后，证明在以下两种情况下，模型的形式保持不变：（i）$\mathbf{A}$ 和 $\boldsymbol{\Phi}$ 都是对角矩阵。这对应于因子分析的情形。变换后的 $\boldsymbol{\Phi}$ 仍然是对角矩阵，因此因子分析对数据变量按分量重新缩放具有协变性；（ii）$\mathbf{A}$ 是正交矩阵，$\boldsymbol{\Phi}$ 与单位矩阵成比例，即 $\boldsymbol{\Phi}=\sigma^2\mathbf{I}$。这对应于概率 PCA。变换后的 $\boldsymbol{\Phi}$ 矩阵仍然与单位矩阵成比例，因此与传统 PCA 一样，概率 PCA 对数据空间坐标轴的旋转具有协变性。

**12.26（⋆⋆）** 证明，满足（12.80）的任意向量 $\mathbf{a}_i$ 也满足（12.79）。再证明，对于（12.80）的任意一个特征值为 $\lambda$ 的解，加上 $\mathbf{K}$ 的一个零特征值所对应的特征向量的任意倍数，仍会得到（12.79）的一个特征值为 $\lambda$ 的解。最后，证明这样的修改不会影响（12.82）给出的主成分投影。

**12.27（⋆⋆）** 证明，如果选择线性核函数 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$，传统线性 PCA 算法就是核 PCA 的一个特殊情形。

**12.28（⋆⋆）www** 利用概率密度在变量变换下的变换性质（1.27），证明任意密度 $p(y)$ 都可以由一个处处非零的固定密度 $q(x)$，通过非线性变量变换 $y=f(x)$ 得到；其中 $f(x)$ 是单调函数，满足 $0\leqslant f'(x)<\infty$。写出 $f(x)$ 满足的微分方程，并画图说明密度的变换。

<!-- pdf-page: 623 -->

**12.29（⋆⋆）www** 假设两个变量 $z_1$ 和 $z_2$ 相互独立，即 $p(z_1,z_2)=p(z_1)p(z_2)$。证明，这两个变量之间的协方差矩阵是对角矩阵。这说明，独立是两个变量不相关的充分条件。现在考虑两个变量 $y_1$ 和 $y_2$，其中 $-1\leqslant y_1\leqslant1$，且 $y_2=y_2^2$。写出条件分布 $p(y_2\mid y_1)$，并观察到它依赖于 $y_1$，从而说明这两个变量不独立。然后证明，这两个变量之间的协方差矩阵仍然是对角矩阵。为此，利用关系 $p(y_1,y_2)=p(y_1)p(y_2\mid y_1)$，证明非对角项为零。这个反例说明，零相关不是独立性的充分条件。

<!-- pdf-page: 624 -->
