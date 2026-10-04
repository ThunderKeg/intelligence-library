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
