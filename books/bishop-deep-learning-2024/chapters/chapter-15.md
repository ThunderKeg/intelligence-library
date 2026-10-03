<!-- pdf-page: 474 -->

# 第 15 章 离散潜变量

<aside class="chapter-guide"><strong>本章导读</strong><p>本章从 K 均值聚类进入离散潜变量模型，说明高斯混合模型如何用隐藏的类别变量表示数据，再推导期望最大化（EM）算法及证据下界（ELBO）。阅读时可留意“硬分配”与“软责任度”的区别。</p></aside>

<figure class="chapter-opener">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/chapter-opener.png" alt="第 15 章彩色章首插图，题为 Discrete Latent Variables">
  <p class="figure-translation">图中文字：Discrete Latent Variables → 离散潜变量。</p>
</figure>

前面已经看到，可以通过组合多个简单分布来构造复杂分布，并用有向图描述得到的模型（见第 11 章）。除数据集中观测到的变量外，这类模型还常引入额外的隐藏变量，也称**潜变量**（latent variable）。它们有时对应数据生成过程中的具体量，例如图像中物体在三维空间里的未知朝向；有时则只是为建立表达能力更强的模型而引入的建模工具。若在观测变量与潜变量上定义联合分布，对潜变量做边缘化，就能得到仅关于观测变量的分布。这样，观测变量上的较复杂边缘分布便可以通过扩展后的观测变量与潜变量空间中更容易处理的联合分布来表示。

本章将看到，对离散潜变量做边缘化会得到

<!-- pdf-page: 475 -->
<!-- join-previous-paragraph -->

混合分布。我们将重点讨论**高斯混合模型**：它既能清楚展示混合分布的性质，也广泛用于机器学习。混合模型的一种简单用途是从数据中发现簇，因此我们首先讨论一种聚类方法，即 **K 均值算法**。它对应高斯混合模型的一个特定的非概率极限。然后，我们从潜变量的角度解释混合分布；其中的离散潜变量可以看作把数据点分配给混合分布中特定成分的指示变量。

**期望最大化**（expectation–maximization，EM）算法是在潜变量模型中求极大似然估计的一种通用方法。我们先用高斯混合分布以较直观的方式引出 EM 算法，再从潜变量角度更严谨地讨论它。最后介绍更一般的**证据下界**（evidence lower bound，ELBO）。它将在变分自编码器和扩散模型等生成模型中发挥重要作用。

## 15.1 K 均值聚类

首先考虑如何在多维空间中找出数据点的组，即**簇**。设数据集 $\{\mathbf x_1,\ldots,\mathbf x_N\}$ 包含 $D$ 维欧几里得变量 $\mathbf x$ 的 $N$ 个观测值。我们的目标是把数据集划分为 $K$ 个簇，暂且假定 $K$ 已知。直观地说，一个簇中的点彼此距离较近，而它们与簇外点的距离较远。为使这一想法形式化，先引入 $D$ 维向量 $\boldsymbol\mu_k$（$k=1,\ldots,K$），其中 $\boldsymbol\mu_k$ 是第 $k$ 个簇的“原型”。稍后会看到，它可以视为该簇的中心。我们要同时找到一组簇向量 $\{\boldsymbol\mu_k\}$ 和数据点到簇的分配，使每个数据点到其最近簇向量的距离平方之和最小。

现在用一些记号描述数据点的簇分配。对每个数据点 $\mathbf x_n$，引入一组二值指示变量 $r_{nk}\in\{0,1\}$，其中 $k=1,\ldots,K$。它们说明 $\mathbf x_n$ 分配给了哪个簇：若分配给第 $k$ 个簇，则 $r_{nk}=1$，且所有 $j\ne k$ 的 $r_{nj}=0$。这是 **1-of-K 编码**的一例。于是可定义误差函数

$$
J=\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\lVert\mathbf x_n-\boldsymbol\mu_k\rVert^2, \tag{15.1}
$$

它是各数据点到其所属簇向量 $\boldsymbol\mu_k$ 的距离平方之和。我们的目标是选取 $\{r_{nk}\}$ 和 $\{\boldsymbol\mu_k\}$，使 $J$ 最小。可用迭代方法完成：每轮迭代

<!-- pdf-page: 476 -->
<!-- join-previous-paragraph -->

依次针对 $\{r_{nk}\}$ 和 $\{\boldsymbol\mu_k\}$ 做两步优化。先给 $\{\boldsymbol\mu_k\}$ 取初值。第一步固定 $\{\boldsymbol\mu_k\}$，对 $\{r_{nk}\}$ 最小化 $J$；第二步固定 $\{r_{nk}\}$，对 $\{\boldsymbol\mu_k\}$ 最小化 $J$。重复这两步直至收敛。稍后会看到，更新 $\{r_{nk}\}$ 和更新 $\{\boldsymbol\mu_k\}$ 分别对应 EM 算法的 E 步（期望步）和 M 步（最大化步；见第 15.3 节）。因此，我们在讨论 K 均值算法时也使用这两个名称。

先考虑固定 $\{\boldsymbol\mu_k\}$ 时确定 $\{r_{nk}\}$，即 E 步。因为式 (15.1) 中 $J$ 是 $\{r_{nk}\}$ 的线性函数，这一步有简单的闭式解。不同 $n$ 对应的项互不相关，因此可对每个 $n$ 单独优化：让使 $\lVert\mathbf x_n-\boldsymbol\mu_k\rVert^2$ 最小的那个 $k$ 对应的 $r_{nk}$ 取 1。换言之，把第 $n$ 个数据点分配给最近的簇中心。形式上可写为

$$
r_{nk}=\begin{cases}
1,&\text{若 }k=\operatorname*{arg\,min}_{j}\lVert\mathbf x_n-\boldsymbol\mu_j\rVert^2,\\
0,&\text{其他情况。}
\end{cases} \tag{15.2}
$$

再考虑固定 $\{r_{nk}\}$ 时优化 $\{\boldsymbol\mu_k\}$，即 M 步。目标函数 $J$ 是 $\boldsymbol\mu_k$ 的二次函数，对 $\boldsymbol\mu_k$ 求导并令导数为零，可得

$$
2\sum_{n=1}^{N}r_{nk}(\mathbf x_n-\boldsymbol\mu_k)=0, \tag{15.3}
$$

从而容易解出

$$
\boldsymbol\mu_k=\frac{\sum_n r_{nk}\mathbf x_n}{\sum_n r_{nk}}. \tag{15.4}
$$

分母就是分配给第 $k$ 个簇的数据点数量。因此，这一结果有简单的解释：$\boldsymbol\mu_k$ 等于分配给第 $k$ 个簇的所有数据点 $\mathbf x_n$ 的均值。这也是 **K 均值算法**名称的由来（Lloyd，1982）。算法 15.1 对其作了总结。由于分配 $\{r_{nk}\}$ 是离散的，而且每轮迭代不会使误差函数增大，K 均值算法保证在有限步内收敛（习题 15.1）。

数据点重新分配到簇、重新计算簇均值，这两个阶段轮流重复，直到分配不再变化，或迭代达到预设的最大次数。不过，这种方法可能收敛到 $J$ 的局部最小值，而非全局最小值。MacQueen（1967）研究了 K 均值算法的收敛性质。

图 15.1 用美国黄石国家公园“老忠实”间歇泉的喷发数据（见第 3.2.9 节）说明 K 均值算法。数据集有 272 个点；每个点的横轴是一次喷发的持续时间，

<!-- pdf-page: 477 -->

<!-- join-previous-paragraph -->

纵轴是到下一次喷发的间隔时间。这里对数据做了线性重新缩放，即**标准化**，使每个变量均值为零、标准差为一。

**算法 15.1：K 均值算法**

```text
输入：初始原型向量 μ₁, …, μ_K
      数据集 x₁, …, x_N
输出：最终原型向量 μ₁, …, μ_K
{r_nk ← 0}
// 初始时所有分配设为零
重复：
  {r_nk^(old)} ← {r_nk}
  // 更新分配
  对 N ∈ {1, …, N}：
    k ← arg min_j
         ‖x_n − μ_j‖²
    r_nk ← 1
    对所有 j ∈ {1, …, K}
      且 j ≠ k：r_nj ← 0
  结束循环
  // 更新原型向量
  对 k ∈ {1, …, K}：
    μ_k ← (Σ_n r_nk x_n)
          / (Σ_n r_nk)
  结束循环
直到 {r_nk} = {r_nk^(old)}
  // 分配不再变化
返回 μ₁, …, μ_K, {r_nk}
```

**译注：** 原书算法 15.1 的循环变量印作大写 $N$，但循环体使用 $x_n$ 和 $r_{nk}$；上面保留原书的 $N$。结合式 (15.2)，循环索引应为小写 $n$。

在这个例子中，取 $K=2$。因此，将每个数据点分配给最近的簇中心，等同于依据数据点位于两簇中心连线的垂直平分线哪一侧来分类。图 15.2 展示了“老忠实”数据在各步中的式 (15.1) 代价函数 $J$。注意，我们特意选了较差的簇中心初值，以便算法经过多步才收敛。实际使用时，更好的初始化方法是从数据集中随机选取 $K$ 个数据点作为簇中心 $\boldsymbol\mu_k$。还要注意，在对高斯混合模型应用 EM 算法之前，常用 K 均值算法来初始化其参数（见第 15.2.2 节）。

到目前为止，我们考虑的是 K 均值的**批量版本**：每次利用整个数据集更新原型向量。也可以推导顺序更新方式：依次处理各数据点 $\mathbf x_n$，每次用下式更新最近的原型 $\boldsymbol\mu_k$（习题 15.2）：

<!-- pdf-page: 478 -->

<figure id="fig-15-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-1.png" alt="老忠实间歇泉二维数据上的 K 均值聚类九步迭代过程">
  <figcaption>图 15.1：在重新缩放的“老忠实”数据集上运行 K 均值算法。(a) 绿色点是二维欧几里得空间中的数据集；红色和蓝色叉号分别是簇中心 $\boldsymbol\mu_1$ 与 $\boldsymbol\mu_2$ 的初值。(b) 第一次 E 步根据与哪个中心更近，将每个数据点分配给红色或蓝色簇；这等同于按照数据点位于两簇中心垂直平分线（洋红线）的哪一侧分类。(c) 随后的 M 步把每个簇中心重新设为分配给该簇的数据点均值。(d)–(i) 展示此后连续的 E 步与 M 步，直至算法最终收敛。</figcaption>
</figure>

<!-- pdf-page: 479 -->

<figure id="fig-15-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-2.png" alt="老忠实数据 K 均值各次 E 步和 M 步后的代价函数 J 曲线">
  <figcaption>图 15.2：图 15.1 的例子中，每次 E 步（蓝点）和 M 步（红点）之后，式 (15.1) 的代价函数 $J$。算法在第三次 M 步后收敛；最后一轮 EM 对分配和原型向量均未造成变化。</figcaption>
</figure>

$$
\boldsymbol\mu_k^{\mathrm{new}}=\boldsymbol\mu_k^{\mathrm{old}}+\frac{1}{N_k}(\mathbf x_n-\boldsymbol\mu_k^{\mathrm{old}}), \tag{15.5}
$$

其中 $N_k$ 是到目前为止用于更新 $\boldsymbol\mu_k$ 的数据点数量。这样，每个数据点使用一次后就可以丢弃，再处理下一个数据点。

K 均值算法的一个值得注意的特点是：每轮迭代都把每个数据点分配给一个、且只分配给一个簇。有些数据点明显比其他簇中心更靠近某个特定的 $\boldsymbol\mu_k$；另一些点却可能大致位于多个簇中心的中间。对于后一种点，硬性分配给最近的簇是否最合适，并不明确。后面会看到，采用概率方法后，可以按照分配结果的不确定程度，对数据点作“软”分配。这种概率形式有许多优点（见第 15.2 节）。

### 15.1.1 图像分割

为了说明 K 均值算法的应用，考虑相互关联的**图像分割**与**图像压缩**问题。分割的目标是把图像划成若干区域，让各区域有大致均匀的视觉外观，或对应物体及其部分（Forsyth and Ponce，2003）。图像中的每个像素都可视为红、蓝、绿三个通道强度组成的三维空间中的一个点；分割算法把每个像素当作单独的数据点。严格说来，由于通道强度被限制在 $[0,1]$，这个空间并不是欧几里得空间；不过，K 均值算法仍可直接应用。对于某个给定的 $K$，让 K 均值算法运行至收敛，再用每个像素所属簇中心 $\boldsymbol\mu_k$ 的 $\{R,G,B\}$ 强度三元组代替原像素向量，重新绘制图像。图 15.3 展示了不同 $K$ 值的结果。由此可见，对于给定 $K$，算法只用

<!-- pdf-page: 480 -->

<!-- join-previous-paragraph -->

$K$ 种颜色的调色板表示图像。

<figure id="fig-15-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-3.png" alt="原图与 K 等于 2、3、10 时的 K 均值图像分割及压缩效果">
  <figcaption>图 15.3：K 均值聚类用于图像分割的例子：展示原图及取不同 $K$ 值时得到的分割图。这也说明了用向量量化压缩数据：$K$ 越小，压缩程度越高，但图像质量越差。</figcaption>
  <p class="figure-translation">图中文字：Original image → 原始图像；$K=2,3,10$ → 分别使用 2、3、10 个簇。</p>
</figure>

必须强调，这种用 K 均值进行图像分割的方法并不精细，至少因为它完全没有考虑不同像素在空间上的邻近关系。图像分割通常十分困难，至今仍是活跃的研究课题。这里介绍它，只是为了展示 K 均值算法的行为。

聚类算法还可以用于数据压缩。必须区分**无损压缩**与**有损压缩**：前者要求从压缩后的表示中精确重建原始数据；后者接受一定的重建误差，以获得高于无损压缩的压缩程度。K 均值算法可用于有损压缩。对 $N$ 个数据点中的每一个，只存储其所属簇的标识 $k$；另外还存储 $K$ 个簇中心 $\{\boldsymbol\mu_k\}$ 的值。只要选取 $K\ll N$，后者通常只需少量数据。之后用每个数据点最近的中心 $\boldsymbol\mu_k$ 近似该点。新数据点也可先找到最近的 $\boldsymbol\mu_k$，再存储标签 $k$ 而非原始数据向量。这一框架通常称为**向量量化**（vector quantization），向量 $\{\boldsymbol\mu_k\}$ 称为**码本向量**（codebook vector）。

前面的图像分割也说明了如何用聚类压缩数据。设原图有 $N$ 个像素，每个像素的 $\{R,G,B\}$ 值各以 8 位精度存储。直接传输整幅图像需要 $24N$ 位。现在先对图像数据运行 K 均值算法，再传输每个像素最近的 $\boldsymbol\mu_k$ 的标识，而非原始像素强度向量。由于共有 $K$ 个向量，每个像素需要 $\log_2 K$ 位。还须传输 $K$ 个码本向量 $\{\boldsymbol\mu_k\}$，需要 $24K$ 位，因此传输图像总共需要 $24K+N\log_2 K$ 位（向上取整为最接近的

<!-- pdf-page: 481 -->
<!-- join-previous-paragraph -->

整数）。图 15.3 中的原始图像有 $240\times180=43{,}200$ 个像素，直接传输需要 $24\times43{,}200=1{,}036{,}800$ 位。相比之下，压缩图像分别需要 $43{,}248$ 位（$K=2$）、$86{,}472$ 位（$K=3$）和 $173{,}040$ 位（$K=10$），分别是原始图像大小的 $4.2\%$、$8.3\%$ 和 $16.7\%$。可见压缩程度与图像质量需要权衡。这里的目标只是说明 K 均值算法。若要构造优秀的图像压缩器，更有成效的做法是考虑相邻像素的小块，例如 $5\times5$ 的像素块，从而利用自然图像中邻近像素之间的相关性。

## 15.2 高斯混合模型

前面曾将高斯混合模型作为高斯成分的简单线性叠加引入，以便构造比单个高斯分布更丰富的密度模型（见第 3.2.9 节）。现在从离散潜变量的角度讨论高斯混合模型。这既能帮助我们更深入地理解这一重要分布，也能引出期望最大化算法。

由式 (3.111)，高斯混合分布可以写成

$$
p(\mathbf x)=\sum_{k=1}^{K}\pi_k\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k). \tag{15.6}
$$

引入一个 $K$ 维二值随机变量 $\mathbf z$，采用 1-of-K 表示：其中一个元素等于 1，其余元素都等于 0。因此，$z_k\in\{0,1\}$ 且 $\sum_k z_k=1$；非零元素的位置决定 $\mathbf z$ 的状态，所以 $\mathbf z$ 共有 $K$ 种可能的状态。我们用边缘分布 $p(\mathbf z)$ 和条件分布 $p(\mathbf x\mid\mathbf z)$ 定义联合分布 $p(\mathbf x,\mathbf z)$。$\mathbf z$ 的边缘分布由混合系数 $\pi_k$ 指定，使

$$
p(z_k=1)=\pi_k,
$$

参数 $\{\pi_k\}$ 必须满足

$$
0\leq\pi_k\leq1 \tag{15.7}
$$

以及

$$
\sum_{k=1}^{K}\pi_k=1. \tag{15.8}
$$

<!-- pdf-page: 482 -->

<figure id="fig-15-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-4.png" alt="潜变量 z 指向观测变量 x 的混合模型有向图">
  <figcaption>图 15.4：混合模型的图表示，其中联合分布写作 $p(\mathbf x,\mathbf z)=p(\mathbf z)p(\mathbf x\mid\mathbf z)$。</figcaption>
</figure>

满足上述条件，$\{\pi_k\}$ 才是合法概率。

由于 $\mathbf z$ 采用 1-of-K 表示，还可以写成

$$
p(\mathbf z)=\prod_{k=1}^{K}\pi_k^{z_k}. \tag{15.9}
$$

类似地，给定 $\mathbf z$ 的某个值时，$\mathbf x$ 的条件分布是高斯分布：

$$
p(\mathbf x\mid z_k=1)=\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k),
$$

也可写成

$$
p(\mathbf x\mid\mathbf z)=\prod_{k=1}^{K}\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)^{z_k}. \tag{15.10}
$$

联合分布为 $p(\mathbf z)p(\mathbf x\mid\mathbf z)$，图 15.4 给出了对应的图模型。对 $\mathbf z$ 的所有可能状态求和，即可将它从联合分布中边缘化，得到 $\mathbf x$ 的边缘分布（习题 15.3）：

$$
p(\mathbf x)=\sum_{\mathbf z}p(\mathbf z)p(\mathbf x\mid\mathbf z)
=\sum_{k=1}^{K}\pi_k\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k). \tag{15.11}
$$

这里使用了式 (15.9) 和 (15.10)。因此，$\mathbf x$ 的边缘分布就是式 (15.6) 的高斯混合分布。如果观测值有 $\mathbf x_1,\ldots,\mathbf x_N$ 多个，那么，由于把边缘分布表示成 $p(\mathbf x)=\sum_{\mathbf z}p(\mathbf x,\mathbf z)$，每个观测数据点 $\mathbf x_n$ 都有一个对应的潜变量 $\mathbf z_n$。

至此，我们得到了引入显式潜变量的另一种等价的高斯混合模型表示。这样做乍看似乎收获不大。不过，我们现在可以处理联合分布 $p(\mathbf x,\mathbf z)$，而不只处理边缘分布 $p(\mathbf x)$；这会显著简化后续推导，尤其是引入 EM 算法后。

另一个重要量是给定 $\mathbf x$ 时 $\mathbf z$ 的条件概率。用 $\gamma(z_k)$ 记 $p(z_k=1\mid\mathbf x)$，它的值可

<!-- pdf-page: 483 -->
<!-- join-previous-paragraph -->

用贝叶斯定理求得：

$$
\begin{aligned}
\gamma(z_k)&\equiv p(z_k=1\mid\mathbf x)
=\frac{p(z_k=1)p(\mathbf x\mid z_k=1)}{\sum_{j=1}^{K}p(z_j=1)p(\mathbf x\mid z_j=1)}\\
&=\frac{\pi_k\mathcal N(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)}{\sum_{j=1}^{K}\pi_j\mathcal N(\mathbf x\mid\boldsymbol\mu_j,\boldsymbol\Sigma_j)}.
\end{aligned} \tag{15.12}
$$

我们把 $\pi_k$ 看作 $z_k=1$ 的先验概率，把观测到 $\mathbf x$ 后得到的 $\gamma(z_k)$ 看作相应的后验概率。后面还会看到，$\gamma(z_k)$ 也可理解为第 $k$ 个成分对“解释”观测值 $\mathbf x$ 所承担的**责任度**（responsibility）。

可以用**祖先采样**（见第 14.2.5 节）生成服从高斯混合模型的随机样本。先从边缘分布 $p(\mathbf z)$ 中抽取一个值 $\hat{\mathbf z}$，再从条件分布 $p(\mathbf x\mid\hat{\mathbf z})$ 中抽取 $\mathbf x$。要表示联合分布 $p(\mathbf x,\mathbf z)$ 的样本，可在 $\mathbf x$ 的相应位置绘出数据点，并根据 $\mathbf z$ 的值，也就是生成该点的高斯成分，给它着色，如图 15.5(a) 所示。若忽略 $\mathbf z$，同一批联合分布样本就成为边缘分布 $p(\mathbf x)$ 的样本；图 15.5(b) 只绘出 $\mathbf x$ 的位置，不带彩色标签。

还可用这份合成数据展示“责任度”：针对每个数据点，计算生成该数据集的混合分布中各个成分的后验概率。具体说，对数据点 $\mathbf x_n$，按照 $k=1,2,3$ 的责任度 $\gamma(z_{nk})$，分别以相应比例混合红、蓝、绿三色绘出该点，如图 15.5(c) 所示。例如，$\gamma(z_{n1})=1$ 的点呈红色；$\gamma(z_{n2})=\gamma(z_{n3})=0.5$ 的点，则由等量蓝色与绿色混合，呈青色。应将其与图 15.5(a) 比较：后者的颜色标签取自实际生成各点的成分身份。

### 15.2.1 似然函数

假设观测数据集为 $\{\mathbf x_1,\ldots,\mathbf x_N\}$，我们希望用高斯混合模型描述这些数据。可将数据集表示为 $N\times D$ 矩阵 $\mathbf X$，其中第 $n$ 行为 $\mathbf x_n^{\mathsf T}$。由式 (15.6)，对数似然函数为

$$
\ln p(\mathbf X\mid\boldsymbol\pi,\boldsymbol\mu,\boldsymbol\Sigma)
=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)\right\}. \tag{15.13}
$$

<!-- pdf-page: 484 -->

<figure id="fig-15-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-5.png" alt="三个高斯成分生成的五百个点，分别显示真实成分、忽略成分的观测值和软责任度着色">
  <figcaption>图 15.5：从图 3.8 的三高斯混合模型中抽取 500 个点。(a) 联合分布 $p(\mathbf z)p(\mathbf x\mid\mathbf z)$ 的样本，$\mathbf z$ 的三个状态分别用红、绿、蓝表示；(b) 对应的边缘分布 $p(\mathbf x)$ 的样本，即忽略 $\mathbf z$ 的取值，只绘制 $\mathbf x$。(a) 的数据称为完整数据，(b) 的数据称为不完整数据；第 15.3 节会进一步讨论。(c) 同一批样本按各点 $\mathbf x_n$ 的责任度 $\gamma(z_{nk})$ 着色，红、蓝、绿的比例分别由 $k=1,2,3$ 的 $\gamma(z_{nk})$ 决定。</figcaption>
</figure>

与单个高斯分布相比，最大化式 (15.13) 的对数似然更复杂。难点在于式中对 $k$ 的求和位于对数内部，因此对数不能直接作用于高斯分布。稍后会看到，若把对数似然的导数设为零，就不能再得到闭式解。

在讨论如何最大化之前，应注意：高斯混合模型的极大似然框架存在一个重要问题，即**奇异点**。为简单起见，考虑各成分的协方差矩阵满足 $\boldsymbol\Sigma_k=\sigma_k^2\mathbf I$ 的高斯混合模型，$\mathbf I$ 是单位矩阵；不过结论也适用于一般协方差矩阵。假设某个成分，例如第 $j$ 个成分，其均值 $\boldsymbol\mu_j$ 恰好等于某个数据点 $\mathbf x_n$，即 $\boldsymbol\mu_j=\mathbf x_n$。于是该点给似然函数带来一项

$$
\mathcal N(\mathbf x_n\mid\mathbf x_n,\sigma_j^2\mathbf I)
=\frac{1}{(2\pi)^{1/2}}\frac{1}{\sigma_j}. \tag{15.14}
$$

**译注：** 原书在讨论 $D$ 维变量时，将式 (15.14) 写成一维高斯在均值处的密度；一般 $D$ 维情形下，右侧应带 $D$ 次幂。此处保留原书印式，不影响 $\sigma_j\to0$ 时密度发散的结论。

当 $\sigma_j\to0$ 时，这一项趋于无穷大，对数似然也会趋于无穷大。因此，最大化对数似然并非一个良定义的问题：只要某个高斯成分“坍缩”到特定数据点，就总会出现这样的奇异点。回想单个高斯分布并没有这个问题。区别在于，若单个高斯分布坍缩到某个数据点，其他数据点产生的似然乘法因子会以指数速度趋于零，因此整体似然趋于零而非无穷大。若混合模型中有至少两个成分，就可以由一个成分维持有限方差，给所有数据点赋予有限概率，而另一个成分缩到某个特定数据点上，

<!-- pdf-page: 485 -->
<!-- join-previous-paragraph -->

从而给对数似然带来不断增大的附加值。图 15.6 说明了这一点。这样的奇异点是极大似然方法可能出现过拟合的一个例子。把极大似然应用于高斯混合模型时，必须采取措施避开这种病态解，转而寻找性质正常的局部似然最大值。可以使用合适的启发式办法，例如发现某个高斯成分正在坍缩时，把它的均值重置为随机选择的值，将协方差重置为较大的值，然后继续优化。也可以在对数似然中加入对应于参数先验分布的正则化项来避开奇异点（见第 15.4.3 节）。

<figure id="fig-15-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-6.png" alt="高斯混合模型中一个成分坍缩到数据点导致似然奇异的示意图">
  <figcaption>图 15.6：高斯混合模型中似然函数出现奇异点的方式。可与图 2.9 中不会产生奇异点的单个高斯分布比较。</figcaption>
</figure>

求极大似然解还有另一个问题：对于任意一个极大似然解，包含 $K$ 个成分的混合模型都有 $K!$ 个等价解，它们对应于把 $K$ 组参数分配给 $K$ 个成分的 $K!$ 种方式。换言之，参数空间中任何一个非退化点，另外还有 $K!-1$ 个点恰好定义同一个分布。这称为**可辨识性问题**（identifiability；Casella and Berger，2002）；当我们希望解释模型得到的参数值时，它尤其重要。讨论连续潜变量模型时还会遇到可辨识性问题（见第 16 章）。不过，如果目的只是找到良好的密度模型，这一问题并无影响，因为等价解中的任意一个都同样有用。

### 15.2.2 极大似然

对含潜变量的模型，求极大似然解的一种简洁而有力的方法是**期望最大化算法**，即 **EM 算法**（Dempster、Laird 和 Rubin，1977；McLachlan 和 Krishnan，1997）。本章将给出三种推导，每一种都比前一种

<!-- pdf-page: 486 -->
<!-- join-previous-paragraph -->

更一般。先从高斯混合模型的一种较直观的推导开始。不过，EM 算法的适用范围远不止于此，本书讨论其他模型时还会反复遇到它的基本概念。

先写出似然函数在最大值处必须满足的条件。对式 (15.13) 的 $\ln p(\mathbf X\mid\boldsymbol\pi,\boldsymbol\mu,\boldsymbol\Sigma)$ 关于高斯成分均值 $\boldsymbol\mu_k$ 求导并令其为零，得到

$$
0=\sum_{n=1}^{N}\underbrace{\frac{\pi_k\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)}{\sum_j\pi_j\mathcal N(\mathbf x_n\mid\boldsymbol\mu_j,\boldsymbol\Sigma_j)}}_{\gamma(z_{nk})}
\boldsymbol\Sigma_k^{-1}(\mathbf x_n-\boldsymbol\mu_k). \tag{15.15}
$$

这里使用了高斯分布的式 (3.26)。注意，式 (15.12) 的后验概率，也就是责任度 $\gamma(z_{nk})$，自然地出现在右侧。将式子乘以 $\boldsymbol\Sigma_k$（假设它非奇异）并整理，得到

$$
\boldsymbol\mu_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf x_n, \tag{15.16}
$$

其中定义

$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk}). \tag{15.17}
$$

$N_k$ 可以解释为有效分配给第 $k$ 个簇的数据点数。仔细看这个解的形式：第 $k$ 个高斯成分的均值 $\boldsymbol\mu_k$ 是数据集所有点的加权均值；数据点 $\mathbf x_n$ 的权重，是第 $k$ 个成分生成它的后验概率 $\gamma(z_{nk})$。

类似地，对 $\ln p(\mathbf X\mid\boldsymbol\pi,\boldsymbol\mu,\boldsymbol\Sigma)$ 关于 $\boldsymbol\Sigma_k$ 求导并令其为零，利用单个高斯分布协方差矩阵的极大似然解（见第 3.2.7 节），可得

$$
\boldsymbol\Sigma_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})(\mathbf x_n-\boldsymbol\mu_k)(\mathbf x_n-\boldsymbol\mu_k)^{\mathsf T}, \tag{15.18}
$$

这与对数据集拟合单个高斯分布的结果形式相同，只是每个数据点同样由对应的后验概率加权，分母则是与相应成分关联的有效数据点数。

最后，对混合系数 $\pi_k$ 最大化 $\ln p(\mathbf X\mid\boldsymbol\pi,\boldsymbol\mu,\boldsymbol\Sigma)$。这里必须考虑约束 (15.8)，即混合系数之和为 1。可用拉格朗日乘子 $\lambda$（见附录 C），最大化

<!-- pdf-page: 487 -->

$$
\ln p(\mathbf X\mid\boldsymbol\pi,\boldsymbol\mu,\boldsymbol\Sigma)
+\lambda\left(\sum_{k=1}^{K}\pi_k-1\right), \tag{15.19}
$$

由此得到

$$
0=\sum_{n=1}^{N}\frac{\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)}{\sum_j\pi_j\mathcal N(\mathbf x_n\mid\boldsymbol\mu_j,\boldsymbol\Sigma_j)}+\lambda, \tag{15.20}
$$

责任度再次出现。将等式两边乘以 $\pi_k$，再对 $k$ 求和，并利用约束 (15.8)，可得 $\lambda=-N$。消去 $\lambda$ 后整理，得到

$$
\pi_k=\frac{N_k}{N}. \tag{15.21}
$$

因此，第 $k$ 个成分的混合系数是它对解释各数据点所承担责任度的平均值。

注意，式 (15.16)、(15.18)、(15.21) 并未给出混合模型参数的闭式解，因为责任度 $\gamma(z_{nk})$ 通过式 (15.12) 以复杂方式依赖这些参数。不过，这些式子提示我们用简单的迭代方法求极大似然解；稍后会看到，它正是高斯混合模型这一特定情形下的 EM 算法。先给均值、协方差和混合系数选取初值，再交替执行两步更新。为后面将明确的原因，称其为 E 步和 M 步。在**期望步**（E 步），利用当前参数值，根据式 (15.12) 计算后验概率，也就是责任度。在**最大化步**（M 步），利用这些概率，通过式 (15.16)、(15.18)、(15.21) 重新估计均值、协方差和混合系数。具体地，先用式 (15.16) 算出新均值，再用新均值和式 (15.18) 计算协方差；这与单个高斯分布的相应结果一致。后面会证明，每次 E 步接 M 步的参数更新都保证使对数似然函数增大（见第 15.3 节）。实践中，若对数似然或参数的变化低于某个阈值，就认为算法已经收敛。

图 15.7 以重新缩放的“老忠实”数据和两个高斯成分说明 EM 算法。中心初值与图 15.1 中 K 均值算法的初值相同，协方差矩阵则初始化为单位矩阵的常数倍。图 (a) 中数据点为绿色；初始模型的两个高斯成分以蓝、红圆形显示其一个标准差等密度轮廓。图 (b) 是第一次 E 步后的结果：每个数据点所含蓝色的比例，等于它由蓝色成分生成的后验概率；

<!-- pdf-page: 488 -->
<!-- join-previous-paragraph -->

红色比例则等于它由红色成分生成的后验概率。因此，属于两个簇的概率大致相等的点呈紫色。图 (c) 是第一次 M 步后的情形：蓝色高斯的均值移动到以各点属于蓝簇的概率加权后的数据集均值；换言之，它移动到了蓝色“墨水”的重心。蓝色高斯的协方差也设为蓝色“墨水”的协方差。红色成分同理。图 (d)、(e)、(f) 分别展示完整执行 2、5、20 轮 EM 后的结果。到图 (f) 时，算法已接近收敛。

<figure id="fig-15-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-7.png" alt="两个高斯成分对老忠实间歇泉数据运行 EM 算法的六个阶段">
  <figcaption>图 15.7：对图 15.1 中用于说明 K 均值算法的“老忠实”数据集应用 EM 算法。各阶段的详细解释见正文。</figcaption>
</figure>

与 K 均值算法相比，EM 算法达到近似收敛所需的迭代次数多得多，每轮的计算量也明显更大。因此，常先运行 K 均值算法，为随后由 EM 调整的高斯混合模型寻找合适初值。协方差矩阵可方便地初始化为 K 均值算法找到的各簇的样本协方差，混合系数可设为分配给相应

<!-- pdf-page: 489 -->
<!-- join-previous-paragraph -->

簇的数据点比例。

<figure id="fig-15-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-8.png" alt="用多个高斯成分拟合双月牙数据分布，展示复杂分布所需的成分数量">
  <figcaption>图 15.8：拟合“双月牙”数据集的高斯混合模型，说明准确表示复杂数据分布可能需要大量混合成分。图中的椭圆是相应成分的等密度线。空间维度增大时，准确建模分布所需的成分数量可能大到无法接受。</figcaption>
  <p class="figure-translation">图内坐标：$x_1$、$x_2$ 为两个数据维度。</p>
</figure>

必须使用参数正则化等方法，避开高斯成分坍缩到特定数据点时的似然奇异点。还要强调，对数似然通常有多个局部最大值，EM 算法并不保证找到其中最大的一个。由于高斯混合模型的 EM 算法十分重要，算法 15.2 对其作了总结。

只要成分足够多，而且模型参数选择得当，混合模型就能以很高的精度近似复杂分布，非常灵活。不过，实践中所需成分数量可能极大，在高维空间尤其如此。图 15.8 用“双月牙”数据集说明这一问题。尽管如此，混合模型在许多应用中仍然有用。理解混合模型还为连续潜变量模型（见第 16 章）以及基于深度神经网络的生成模型奠定基础；后者能更好地扩展到高维空间。

## 15.3 期望最大化算法

现在从更一般的角度讨论 EM 算法，重点是潜变量的作用。仍用 $\mathbf X$ 表示所有观测数据点组成的集合，其中第 $n$ 行为 $\mathbf x_n^{\mathsf T}$。相应潜变量表示为 $N\times K$ 矩阵 $\mathbf Z$，其第 $n$ 行为 $\mathbf z_n^{\mathsf T}$。若假定各数据点独立地从分布中抽取，便可用图 15.9 所示的图模型，表示这一独立同分布数据集的高斯混合模型。用 $\boldsymbol\theta$ 表示全部模型参数。

<!-- pdf-page: 490 -->

**算法 15.2：高斯混合模型的 EM 算法**

```text
输入：模型参数初值
  {μ_k}, {Σ_k}, {π_k}
  数据集 {x₁, …, x_N}
输出：最终模型参数
  {μ_k}, {Σ_k}, {π_k}
重复：
  // E 步
  对 n ∈ {1, …, N}：
    对 k ∈ {1, …, K}：
      γ(z_nk) ←
        π_k N(x_n|μ_k,Σ_k)
        / Σ_(j=1)^K
          π_j N(x_n|μ_j,Σ_j)
    结束循环
  结束循环
  // M 步
  对 k ∈ {1, …, K}：
    N_k ← Σ_(n=1)^N γ(z_nk)
    μ_k ← (1/N_k) Σ_(n=1)^N
           γ(z_nk) x_n
    Σ_k ← (1/N_k) Σ_(n=1)^N
           γ(z_nk)
           (x_n−μ_k)(x_n−μ_k)ᵀ
    π_k ← N_k/N
  结束循环
  // 对数似然
  L ← Σ_(n=1)^N ln{
    Σ_(k=1)^K π_k
      N(x_n|μ_k,Σ_k)}
直到收敛
返回 {x_k}, {Σ_k}, {π_k}
```

**译注：** 原书算法 15.2 最后一行印作“返回 $\{\mathbf x_k\}$”，而输入、输出和 M 步都把该组参数记为 $\{\boldsymbol\mu_k\}$。上面保留原书返回行的记号。

<!-- pdf-page: 491 -->

<figure id="fig-15-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-9.png" alt="高斯混合模型板图：混合系数和高斯参数指向 N 组潜变量及观测变量">
  <figcaption>图 15.9：$N$ 个独立同分布数据点 $\{\mathbf x_n\}$ 及对应潜变量 $\{\mathbf z_n\}$ 的高斯混合模型图表示，$n=1,\ldots,N$。</figcaption>
  <p class="figure-translation">图内符号：$\boldsymbol\pi$ 为混合系数；$\boldsymbol\mu$ 为高斯成分均值；$\boldsymbol\Sigma$ 为协方差；外框中的 $N$ 表示重复 $N$ 次。</p>
</figure>

由此，对数似然函数为

$$
\ln p(\mathbf X\mid\boldsymbol\theta)
=\ln\left\{\sum_{\mathbf Z}p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)\right\}. \tag{15.22}
$$

把对 $\mathbf Z$ 的求和换成积分后，下面的讨论也适用于连续潜变量（见第 16 章）。

关键在于：潜变量的求和位于对数内部。即便联合分布 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$ 属于指数族，这种求和通常使边缘分布 $p(\mathbf X\mid\boldsymbol\theta)$ 不再属于指数族。由于求和挡住了对数，无法让它直接作用于联合分布，因此极大似然解会出现复杂的表达式。

设想我们不仅知道 $\mathbf X$ 中的每个观测值，还知道相应潜变量 $\mathbf Z$ 的值。我们把 $\{\mathbf X,\mathbf Z\}$ 称为**完整数据集**，把实际观测到的 $\mathbf X$ 称为**不完整数据集**，如图 15.5 所示。完整数据的对数似然就是 $\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$，并假定最大化它并不困难。

但实际情况是，我们没有完整数据 $\{\mathbf X,\mathbf Z\}$，只有不完整数据 $\mathbf X$。关于 $\mathbf Z$ 取值的信息仅由后验分布 $p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)$ 给出。既然不能直接使用完整数据的对数似然，就改为考虑它在潜变量后验分布下的期望；稍后会看到，这对应 EM 算法的 E 步。随后在 M 步中最大化这一期望。若当前参数估计为 $\boldsymbol\theta^{\mathrm{old}}$，连续执行一轮 E 步和 M 步就得到修订后的估计 $\boldsymbol\theta^{\mathrm{new}}$。算法从某个初始参数值 $\boldsymbol\theta_0$ 开始。取期望这一做法也许显得有些随意；第 15.4 节更深入地讨论 EM 时会说明其原因。

在 E 步，用当前参数 $\boldsymbol\theta^{\mathrm{old}}$ 求出潜变量的后验分布 $p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})$，再用该分布计算在一般参数值 $\boldsymbol\theta$ 下的完整数据对数似然的期望。这个期望记为 $Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})$，即

$$
Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})
=\sum_{\mathbf Z}p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})
\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\theta). \tag{15.23}
$$

<!-- pdf-page: 492 -->

**算法 15.3：一般 EM 算法**

```text
输入：联合分布 p(X, Z | θ)
      参数初值 θ^old
      数据集 x₁, …, x_N
输出：最终参数 θ
重复：
    Q(θ, θ^old) ←
      Σ_Z p(Z | X, θ^old)
          ln p(X, Z | θ)
    // E 步
    θ^new ← arg max_θ
              Q(θ, θ^old)
    // M 步
    L ← p(X | θ^new)
    // 评估对数似然
    θ^old ← θ^new
    // 更新参数
直到收敛
返回 θ^new
```

**译注：** 原书算法 15.3 将 $L$ 写为 $p(\mathbf X\mid\boldsymbol\theta^{\mathrm{new}})$，旁注却称“评估对数似然”；若按旁注，应取其对数。算法行保留原书写法。

在 M 步，通过最大化该函数得到新的参数估计 $\boldsymbol\theta^{\mathrm{new}}$：

$$
\boldsymbol\theta^{\mathrm{new}}
=\operatorname*{arg\,max}_{\boldsymbol\theta}
Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}}). \tag{15.24}
$$

注意，$Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})$ 中的对数直接作用于联合分布 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$，因此按照前面的假设，M 步的最大化是可处理的。算法 15.3 总结了通用 EM 算法。后面会证明，每轮 EM 都会使不完整数据的对数似然增加，除非它已经位于一个局部最大值（见第 15.4.1 节）。

EM 算法也可用于求参数上定义了先验 $p(\boldsymbol\theta)$ 的模型的 **MAP 解**，即最大后验解（习题 15.5）。这时，E 步与极大似然情形相同；M 步则最大化 $Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})+\ln p(\boldsymbol\theta)$。适当选取先验，可以消除图 15.6 那类奇异点。

以上讨论的是有离散潜变量时，用 EM 算法最大化似然函数。若未观测变量对应数据集中的缺失值，也可以应用 EM。将所有变量的联合分布对缺失变量边缘化，就得到观测值的分布；然后用 EM 最大化相应的似然函数。若数据是**随机缺失**（missing at random），即造成缺失的机制不依赖未观测值，这种做法有效。但很多时候这一条件不成立。例如，传感器测量值一旦超过某个阈值便不给出读数，就不是随机缺失。

<!-- pdf-page: 493 -->

<figure id="fig-15-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-10.png" alt="高斯混合模型中数据变量与离散潜变量均被观测的图模型">
  <figcaption>图 15.10：与图 15.9 相同的图，但现在假设除数据变量 $\mathbf x_n$ 外，离散变量 $\mathbf z_n$ 也被观测到。</figcaption>
  <p class="figure-translation">图内符号：$\boldsymbol\pi$ 为混合系数；$\mathbf z_n$ 为离散变量；$\mathbf x_n$ 为数据变量；$\boldsymbol\mu$、$\boldsymbol\Sigma$ 为高斯分量参数；$N$ 表示重复 $N$ 次的板式结构。</p>
</figure>

### 15.3.1 高斯混合分布

现在考虑将 EM 的潜变量视角用于高斯混合模型。回顾一下，我们的目标是最大化根据观测数据集 $\mathbf X$ 计算的对数似然函数 (15.13)。由于对数内部有对 $k$ 的求和，这比单个高斯分布更难处理。假设除了观测数据集 $\mathbf X$，我们还知道相应离散变量 $\mathbf Z$ 的取值。回顾图 15.5(a) 展示的是完整数据集，即包含标明每个数据点由哪个分量生成的标签；图 15.5(b) 则是相应的不完整数据集。完整数据的图模型如图 15.10 所示。

现在考虑最大化完整数据集 $\{\mathbf X,\mathbf Z\}$ 的似然。由式 (15.9) 和 (15.10)，似然函数为

$$
p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)=\prod_{n=1}^{N}\prod_{k=1}^{K}\pi_k^{z_{nk}}\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)^{z_{nk}}.\tag{15.25}
$$

其中 $z_{nk}$ 为 $\mathbf z_n$ 的第 $k$ 个分量。取对数，得到

$$
\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)=\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\{\ln\pi_k+\ln\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)\}.\tag{15.26}
$$

与不完整数据的对数似然函数 (15.13) 相比，对 $k$ 的求和与对数交换了位置。现在，对数直接作用于高斯分布，而高斯分布属于指数族。不出所料，这使极大似然问题的求解简单许多，下面加以说明。先考虑对均值和协方差的最大化。由于 $\mathbf z_n$ 是 $K$ 维向量，仅有一个元素为 $1$，其余元素全为 $0$，完整数据的对数似然函数就是 $K$ 个独立贡献之和，每个混合分量贡献一项。因此，对均值或协方差的最大化与单个高斯分布的情形完全一样，只是仅涉及“分配”给该分量的数据点子集。至于对混合系数的最大化，由于求和约束 (15.8)，不同 $k$ 的系数相互关联。与前面一样，可以用拉格朗日

<!-- pdf-page: 494 -->
<!-- join-previous-paragraph -->

乘子强制满足约束，得到

$$
\pi_k=\frac{1}{N}\sum_{n=1}^{N}z_{nk},\tag{15.27}
$$

即混合系数等于分配给相应分量的数据点所占的比例。

可见，完整数据的对数似然函数很容易用闭式解最大化。然而，实际中并不知道潜变量的取值。因此，如前所述，我们考虑完整数据对数似然相对于潜变量后验分布的期望。由式 (15.9)、(15.10) 和贝叶斯定理，该后验分布为

$$
p(\mathbf Z\mid\mathbf X,\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)\propto\prod_{n=1}^{N}\prod_{k=1}^{K}[\pi_k\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)]^{z_{nk}}.\tag{15.28}
$$

它对于 $n$ 可分解，因此在后验分布下，$\{\mathbf z_n\}$ 相互独立。查看图 15.9 的有向图并应用 d 分离准则（见第 11.2 节），也容易验证这一点。此后验分布下，指示变量 $z_{nk}$ 的期望为

$$
\begin{aligned}\mathbb E[z_{nk}]&=\frac{\sum_{\mathbf z_n}z_{nk}\prod_{k'}[\pi_{k'}\mathcal N(\mathbf x_n\mid\boldsymbol\mu_{k'},\boldsymbol\Sigma_{k'})]^{z_{nk'}}}{\sum_{\mathbf z_n}\prod_j[\pi_j\mathcal N(\mathbf x_n\mid\boldsymbol\mu_j,\boldsymbol\Sigma_j)]^{z_{nj}}}\\&=\frac{\pi_k\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)}{\sum_{j=1}^{K}\pi_j\mathcal N(\mathbf x_n\mid\boldsymbol\mu_j,\boldsymbol\Sigma_j)}=\gamma(z_{nk}),\end{aligned}\tag{15.29}
$$

这恰是分量 $k$ 对数据点 $\mathbf x_n$ 的责任度。因此，完整数据对数似然函数的期望为

$$
\mathbb E_{\mathbf Z}[\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)]=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\{\ln\pi_k+\ln\mathcal N(\mathbf x_n\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)\}.\tag{15.30}
$$

接下来这样进行：首先选择参数 $\boldsymbol\mu^{\mathrm{old}}$、$\boldsymbol\Sigma^{\mathrm{old}}$ 和 $\boldsymbol\pi^{\mathrm{old}}$ 的初值，据此计算责任度，即 E 步；然后保持责任度不变，对 $\boldsymbol\mu_k$、$\boldsymbol\Sigma_k$、$\pi_k$ 最大化式 (15.30)，即 M 步。这再次得到式 (15.16)、(15.18) 和 (15.21) 所给出的 $\boldsymbol\mu^{\mathrm{new}}$、$\boldsymbol\Sigma^{\mathrm{new}}$ 和 $\boldsymbol\pi^{\mathrm{new}}$ 的闭式解。这正是前面推导的高斯混合分布 EM 算法。第 15.4 节讨论 EM 算法的收敛时，会进一步阐明完整数据对数似然期望的作用。

<!-- pdf-page: 495 -->

<figure id="fig-15-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-11.png" alt="隐藏马尔可夫模型中离散潜变量构成链并各自生成观测变量">
  <figcaption>图 15.11：与隐藏马尔可夫模型相对应的序列数据概率图模型。离散潜变量不再独立，而是形成一条马尔可夫链。</figcaption>
  <p class="figure-translation">图内符号：$z_1,z_2,\ldots,z_N$ 为潜变量链；$x_1,x_2,\ldots,x_N$ 为相应观测变量；箭头表示条件依赖。</p>
</figure>

本章迄今均假定数据观测值独立同分布。对于形成序列的有序观测值，可以通过把潜变量连成一条马尔可夫链来扩展混合模型，得到图 15.11 所示结构的隐藏马尔可夫模型。EM 算法也可推广到这一更复杂的模型；其 E 步涉及沿潜变量链传递消息的顺序计算（Bishop，2006）。

### 15.3.2 与 K 均值的关系

比较 K 均值算法与高斯混合分布的 EM 算法，可以发现两者十分相似。K 均值将每个数据点唯一地分配给某个簇，是**硬分配**；EM 则根据后验概率进行**软分配**。事实上，可以把 K 均值算法推导为高斯混合分布 EM 的一个特殊极限。

考虑各混合分量的协方差矩阵均为 $\epsilon\mathbf I$ 的高斯混合模型，其中 $\epsilon$ 是所有分量共享的方差参数，$\mathbf I$ 为单位矩阵。于是

$$
p(\mathbf x\mid\boldsymbol\mu_k,\boldsymbol\Sigma_k)=\frac{1}{(2\pi\epsilon)^{D/2}}\exp\left\{-\frac{1}{2\epsilon}\lVert\mathbf x-\boldsymbol\mu_k\rVert^2\right\}.\tag{15.31}
$$

考虑由 $K$ 个此类高斯分布组成的混合模型的 EM 算法，但将 $\epsilon$ 视为固定常数，而不是需要重新估计的参数。由式 (15.12)，某数据点 $\mathbf x_n$ 的后验概率或责任度为

$$
\gamma(z_{nk})=\frac{\pi_k\exp\{-\lVert\mathbf x_n-\boldsymbol\mu_k\rVert^2/(2\epsilon)\}}{\sum_j\pi_j\exp\{-\lVert\mathbf x_n-\boldsymbol\mu_j\rVert^2/(2\epsilon)\}}.\tag{15.32}
$$

现在令 $\epsilon\to0$。分母是按 $j$ 编号的一组趋于零的项之和。使 $\lVert\mathbf x_n-\boldsymbol\mu_j\rVert^2$ 最小的那项，设其为 $j=l$，趋于零的速度最慢，因而最终主导该和。因此，对数据点 $\mathbf x_n$，除第 $l$ 项外的责任度 $\gamma(z_{nk})$ 都趋于零，而 $\gamma(z_{nl})$ 趋于一。只要所有 $\pi_k$ 均不为零，这一结论就不依赖于其具体值。所以在该极限下，数据点对簇形成与 K 均值算法一样的硬分配：$\gamma(z_{nk})\to r_{nk}$，其中 $r_{nk}$ 由式 (15.2) 定义。每个数据点因此被分配给均值最近的簇。式 (15.16) 的 $\boldsymbol\mu_k$ 的 EM 重估公式，也就化为式 (15.4) 的 K 均值结果。注意，混合系数的重估公式 (15.21) 只是把 $\pi_k$ 重新设为分配给簇 $k$ 的数据点比例，

<!-- pdf-page: 496 -->
<!-- join-previous-paragraph -->

尽管这些参数已不再在算法中发挥主动作用。

最后，当 $\epsilon\to0$ 时，式 (15.30) 给出的完整数据对数似然期望变为

$$
\mathbb E_{\mathbf Z}[\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)]\to-\frac{1}{2}\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\lVert\mathbf x_n-\boldsymbol\mu_k\rVert^2+\mathrm{const}.\tag{15.33}
$$

**译注：** 若直接将式 (15.31) 的协方差 $\epsilon\mathbf I$ 代入式 (15.30)，平方距离项带有 $1/\epsilon$。原书式 (15.33) 未说明是否隐含了正比例缩放；这里保留原式。

可见，在此极限下，最大化完整数据对数似然期望，等价于最小化式 (15.1) 给出的 K 均值算法误差度量 $J$。注意，K 均值算法只估计簇均值，而不估计簇协方差。

### 15.3.3 伯努利分布的混合

本章到目前为止，重点讨论的是以高斯混合描述的连续变量分布。作为混合建模的另一示例，也为了在不同背景下说明 EM 算法，现在讨论由伯努利分布描述的离散二元变量的混合。该模型也称为**潜类分析**（Lazarsfeld 和 Henry，1968；McLachlan 和 Peel，2000）。

考虑一组 $D$ 个二元变量 $x_i$，其中 $i=1,\ldots,D$，每个变量服从参数为 $\mu_i$ 的伯努利分布（见第 3.1.1 节），于是

$$
p(\mathbf x\mid\boldsymbol\mu)=\prod_{i=1}^{D}\mu_i^{x_i}(1-\mu_i)^{1-x_i},\tag{15.34}
$$

其中 $\mathbf x=(x_1,\ldots,x_D)^{\mathsf T}$，$\boldsymbol\mu=(\mu_1,\ldots,\mu_D)^{\mathsf T}$。可见，给定 $\boldsymbol\mu$ 后，各变量 $x_i$ 相互独立。该分布的均值和协方差容易求得：

$$
\mathbb E[\mathbf x]=\boldsymbol\mu,\tag{15.35}
$$

$$
\operatorname{cov}[\mathbf x]=\operatorname{diag}\{\mu_i(1-\mu_i)\}.\tag{15.36}
$$

现在考虑这些分布的有限混合：

$$
p(\mathbf x\mid\boldsymbol\mu,\boldsymbol\pi)=\sum_{k=1}^{K}\pi_k p(\mathbf x\mid\boldsymbol\mu_k),\tag{15.37}
$$

其中 $\boldsymbol\mu=\{\boldsymbol\mu_1,\ldots,\boldsymbol\mu_K\}$，$\boldsymbol\pi=\{\pi_1,\ldots,\pi_K\}$，且

$$
p(\mathbf x\mid\boldsymbol\mu_k)=\prod_{i=1}^{D}\mu_{ki}^{x_i}(1-\mu_{ki})^{1-x_i}.\tag{15.38}
$$

混合系数满足式 (15.7) 和 (15.8)。该混合分布的均值与协方差为

<!-- pdf-page: 497 -->

$$
\mathbb E[\mathbf x]=\sum_{k=1}^{K}\pi_k\boldsymbol\mu_k,\tag{15.39}
$$

$$
\operatorname{cov}[\mathbf x]=\sum_{k=1}^{K}\pi_k\{\boldsymbol\Sigma_k+\boldsymbol\mu_k\boldsymbol\mu_k^{\mathsf T}\}-\mathbb E[\mathbf x]\mathbb E[\mathbf x]^{\mathsf T},\tag{15.40}
$$

其中 $\boldsymbol\Sigma_k=\operatorname{diag}\{\mu_{ki}(1-\mu_{ki})\}$。由于 $\operatorname{cov}[\mathbf x]$ 不再是对角矩阵，混合分布能刻画变量之间的相关性，而单个伯努利分布做不到这一点。

若给定数据集 $\mathbf X=\{\mathbf x_1,\ldots,\mathbf x_N\}$，该模型的对数似然函数为

$$
\ln p(\mathbf X\mid\boldsymbol\mu,\boldsymbol\pi)=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k p(\mathbf x_n\mid\boldsymbol\mu_k)\right\}.\tag{15.41}
$$

这里又出现对数内部的求和，因此极大似然解不再具有闭式形式。

现在推导用于最大化伯努利混合分布似然函数的 EM 算法。首先，为每个 $\mathbf x$ 显式引入一个离散潜变量 $\mathbf z$。与高斯混合模型一样，$\mathbf z$ 采用 1-of-$K$ 编码：$\mathbf z=(z_1,\ldots,z_K)^{\mathsf T}$ 是 $K$ 维二元向量，恰有一个分量为 $1$，其余全为 $0$。于是，给定潜变量后，$\mathbf x$ 的条件分布为

$$
p(\mathbf x\mid\mathbf z,\boldsymbol\mu)=\prod_{k=1}^{K}p(\mathbf x\mid\boldsymbol\mu_k)^{z_k},\tag{15.42}
$$

潜变量的先验分布与高斯混合模型中相同：

$$
p(\mathbf z\mid\boldsymbol\pi)=\prod_{k=1}^{K}\pi_k^{z_k}.\tag{15.43}
$$

将 $p(\mathbf x\mid\mathbf z,\boldsymbol\mu)$ 与 $p(\mathbf z\mid\boldsymbol\pi)$ 相乘，再对 $\mathbf z$ 边缘化，就能恢复式 (15.37)。

为推导 EM 算法，先写出完整数据对数似然函数：

$$
\begin{aligned}\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\pi)=\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\biggl\{\ln\pi_k+\sum_{i=1}^{D}\bigl[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\bigr]\biggr\}.\end{aligned}\tag{15.44}
$$

<!-- pdf-page: 498 -->

其中 $\mathbf X=\{\mathbf x_n\}$，$\mathbf Z=\{\mathbf z_n\}$。接着，对潜变量的后验分布求完整数据对数似然的期望，得到

$$
\begin{aligned}\mathbb E_{\mathbf Z}[\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\mu,\boldsymbol\pi)]=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\biggl\{\ln\pi_k+\sum_{i=1}^{D}\bigl[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\bigr]\biggr\}.\end{aligned}\tag{15.45}
$$

其中 $\gamma(z_{nk})=\mathbb E[z_{nk}]$ 是给定数据点 $\mathbf x_n$ 时分量 $k$ 的后验概率，即责任度。在 E 步，用贝叶斯定理计算这些责任度：

$$
\begin{aligned}\gamma(z_{nk})=\mathbb E[z_{nk}]&=\frac{\sum_{\mathbf z_n}z_{nk}\prod_{k'}[\pi_{k'}p(\mathbf x_n\mid\boldsymbol\mu_{k'})]^{z_{nk'}}}{\sum_{\mathbf z_n}\prod_j[\pi_jp(\mathbf x_n\mid\boldsymbol\mu_j)]^{z_{nj}}}\\&=\frac{\pi_kp(\mathbf x_n\mid\boldsymbol\mu_k)}{\sum_{j=1}^{K}\pi_jp(\mathbf x_n\mid\boldsymbol\mu_j)}.\end{aligned}\tag{15.46}
$$

考察式 (15.45) 中对 $n$ 的求和，可以发现责任度仅通过以下两项进入：

$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk}),\tag{15.47}
$$

$$
\bar{\mathbf x}_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf x_n,\tag{15.48}
$$

其中 $N_k$ 是与分量 $k$ 关联的数据点的有效数量。在 M 步，对参数 $\boldsymbol\mu_k$ 和 $\boldsymbol\pi$ 最大化完整数据对数似然的期望。令式 (15.45) 对 $\boldsymbol\mu_k$ 的导数为零，再整理，得

$$
\boldsymbol\mu_k=\bar{\mathbf x}_k.\tag{15.49}
$$

即分量 $k$ 的均值等于数据的加权均值，权重为该分量对各数据点的责任度。对于 $\pi_k$ 的最大化，须引入拉格朗日乘子以强制满足 $\sum_k\pi_k=1$。与高斯混合分布的推导类似，得

$$
\pi_k=\frac{N_k}{N},\tag{15.50}
$$

<!-- pdf-page: 499 -->

<figure id="fig-15-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-12.png" alt="伯努利混合模型对二值手写数字的三个分量与单个伯努利模型的比较">
  <figcaption>图 15.12：伯努利混合模型示例。上排是数字数据集的样本，像素值以 $0.5$ 为阈值由灰度转为二值。下排前三幅是混合模型三个分量各自的参数 $\mu_{ki}$。作为对比，我们还用极大似然拟合了单个多元伯努利分布；这等于对每个像素的计数直接取平均，结果见下排最右图。</figcaption>
  <p class="figure-translation">图内无英文词语；上排像素分别展示手写数字样本，下排展示三个混合分量与单个伯努利模型的像素概率图。</p>
</figure>

这与直觉一致：分量 $k$ 的混合系数，等于该分量解释的数据点在数据集中的有效比例。

注意，与高斯混合分布不同，这里不存在使似然函数趋于无穷大的奇异点。因为 $0\leqslant p(\mathbf x_n\mid\boldsymbol\mu_k)\leqslant1$，似然函数有上界。某些解会使似然函数为零；但只要 EM 没有从病态初值开始，就不会找到这些解，因为 EM 算法总会提高似然函数值，直至找到局部最大值（见第 15.3 节）。

图 15.12 用伯努利混合模型刻画手写数字。先把数字图像转为二元向量：像素值大于 $0.5$ 的元素置为 $1$，其余置为 $0$。然后取 $N=600$ 个数字“2”“3”“4”的图像，使用 $K=3$ 个伯努利分布的混合模型，运行 EM 算法 $10$ 次迭代来拟合。混合系数初始化为 $\pi_k=1/K$；参数 $\mu_{kj}$ 则在 $(0.25,0.75)$ 上均匀随机选取，再归一化以满足 $\sum_j\mu_{kj}=1$。可以看到，三个伯努利分布的混合能够找到数据集中对应不同数字的三个簇。利用离散分布 (3.14)，也容易把伯努利混合的分析推广到具有 $M>2$ 个状态的多项二元变量。

**译注：** 独立伯努利像素模型的每个参数通常只需在 $[0,1]$ 内，不要求跨像素的 $\sum_j\mu_{kj}=1$。这里照录原书给出的初始化步骤。

<!-- pdf-page: 500 -->

## 15.4 证据下界

现在从更一般的角度看 EM 算法：推导对数似然函数的一个下界，称为**证据下界**（evidence lower bound，ELBO），有时也称**变分下界**。这里的“证据”指（对数）似然函数；在贝叶斯语境中，它有时称为“模型证据”，因为无需留出数据就可以用它比较不同模型（Bishop，2006）。作为下界的应用，我们将从第三种角度重新推导高斯混合分布的 EM 算法。ELBO 在后续章节讨论的几种深度生成模型中十分重要。它也是变分框架的一个例子：引入潜变量上的分布 $q(\mathbf Z)$，再用变分法对此分布优化（见附录 B）。

考虑一个概率模型，把所有观测变量统称为 $\mathbf X$，所有隐藏变量统称为 $\mathbf Z$。联合分布 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$ 由参数集合 $\boldsymbol\theta$ 控制。目标是最大化似然函数：

$$
p(\mathbf X\mid\boldsymbol\theta)=\sum_{\mathbf Z}p(\mathbf X,\mathbf Z\mid\boldsymbol\theta).\tag{15.51}
$$

这里假设 $\mathbf Z$ 为离散变量。如果它包含连续变量，或离散与连续变量的组合，只需适当地用积分替换求和，以下讨论仍然相同。

假设直接优化 $p(\mathbf X\mid\boldsymbol\theta)$ 很困难，但优化完整数据似然 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$ 要容易得多。引入定义在潜变量上的分布 $q(\mathbf Z)$。对于任意 $q(\mathbf Z)$，都有分解

$$
\ln p(\mathbf X\mid\boldsymbol\theta)=\mathcal L(q,\boldsymbol\theta)+\operatorname{KL}(q\parallel p),\tag{15.52}
$$

其中定义

$$
\mathcal L(q,\boldsymbol\theta)=\sum_{\mathbf Z}q(\mathbf Z)\ln\left\{\frac{p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)}{q(\mathbf Z)}\right\},\tag{15.53}
$$

$$
\operatorname{KL}(q\parallel p)=-\sum_{\mathbf Z}q(\mathbf Z)\ln\left\{\frac{p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)}{q(\mathbf Z)}\right\}.\tag{15.54}
$$

注意，$\mathcal L(q,\boldsymbol\theta)$ 对分布 $q(\mathbf Z)$ 是泛函，对参数 $\boldsymbol\theta$ 则是函数（见附录 B）。值得仔细比较式 (15.53) 与 (15.54)：二者符号不同；$\mathcal L$ 包含 $\mathbf X$ 和 $\mathbf Z$ 的联合分布，而 $\operatorname{KL}$ 包含给定 $\mathbf X$ 时 $\mathbf Z$ 的条件分布。为验证式 (15.52)，先用概率的乘法规则得到

$$
\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)=\ln p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)+\ln p(\mathbf X\mid\boldsymbol\theta),\tag{15.55}
$$

<!-- pdf-page: 501 -->

<figure id="fig-15-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-13.png" alt="对数似然、证据下界和 KL 散度的高度关系">
  <figcaption>图 15.13：式 (15.52) 给出的分解，对任意分布 $q(\mathbf Z)$ 都成立。由于 KL 散度满足 $\operatorname{KL}(q\parallel p)\geqslant0$，$\mathcal L(q,\boldsymbol\theta)$ 是对数似然函数 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 的下界。</figcaption>
  <p class="figure-translation">图内文字：$\ln p(\mathbf X\mid\boldsymbol\theta)$ → 对数似然；$\mathcal L(q,\boldsymbol\theta)$ → 下界；$\operatorname{KL}(q\parallel p)$ → 两者之间的 KL 散度。</p>
</figure>

再将式 (15.55) 代入 $\mathcal L(q,\boldsymbol\theta)$。得到两项，其中一项抵消 $\operatorname{KL}(q\parallel p)$；注意到 $q(\mathbf Z)$ 已归一化、求和为 $1$，另一项便给出所需的对数似然 $\ln p(\mathbf X\mid\boldsymbol\theta)$。

由式 (15.54)，$\operatorname{KL}(q\parallel p)$ 是 $q(\mathbf Z)$ 与后验分布 $p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)$ 之间的 KL 散度。回顾 KL 散度满足 $\operatorname{KL}(q\parallel p)\geqslant0$，当且仅当 $q(\mathbf Z)=p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)$ 时取等号（见第 2.5.7 节）。因此由式 (15.52) 得 $\mathcal L(q,\boldsymbol\theta)\leqslant\ln p(\mathbf X\mid\boldsymbol\theta)$，即 $\mathcal L(q,\boldsymbol\theta)$ 是对数似然的下界。图 15.13 示意了式 (15.52) 的分解。

### 15.4.1 再看 EM

可以利用分解式 (15.52) 推导 EM 算法，并证明它确实会最大化对数似然。设参数向量当前值为 $\boldsymbol\theta^{\mathrm{old}}$。在 E 步，保持 $\boldsymbol\theta^{\mathrm{old}}$ 不变，对 $q(\mathbf Z)$ 最大化下界 $\mathcal L(q,\boldsymbol\theta^{\mathrm{old}})$。解很容易看出：$\ln p(\mathbf X\mid\boldsymbol\theta^{\mathrm{old}})$ 不依赖 $q(\mathbf Z)$，因此 $\operatorname{KL}$ 散度为零时，下界取最大值；也就是说，$q(\mathbf Z)$ 等于后验分布 $p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})$。此时，下界等于对数似然，如图 15.14 所示。

在随后的 M 步，分布 $q(\mathbf Z)$ 保持不变，对参数向量 $\boldsymbol\theta$ 最大化下界。

<figure id="fig-15-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-14.png" alt="EM 算法 E 步中下界上升并与对数似然相接的示意图">
  <figcaption>图 15.14：EM 算法 E 步示意图。令 $q$ 分布等于当前参数 $\boldsymbol\theta^{\mathrm{old}}$ 下的后验分布，使下界升至与对数似然函数相同的值，KL 散度因而为零。</figcaption>
  <p class="figure-translation">图内文字：$\operatorname{KL}(q\parallel p)=0$ → KL 散度为零；$\mathcal L(q,\boldsymbol\theta^{\mathrm{old}})$ → 当前参数下的下界；$\ln p(\mathbf X\mid\boldsymbol\theta^{\mathrm{old}})$ → 当前参数下的对数似然。</p>
</figure>

<!-- pdf-page: 502 -->

<figure id="fig-15-15">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-15.png" alt="EM 算法 M 步中下界与对数似然同步升高的示意图">
  <figcaption>图 15.15：EM 算法 M 步示意图。保持分布 $q(\mathbf Z)$ 不变，对参数向量 $\boldsymbol\theta$ 最大化下界 $\mathcal L(q,\boldsymbol\theta)$，得到更新值 $\boldsymbol\theta^{\mathrm{new}}$。由于 KL 散度非负，对数似然 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 的增幅至少与下界的增幅相同。</figcaption>
  <p class="figure-translation">图内文字：$\operatorname{KL}(q\parallel p)$ → KL 散度；$\mathcal L(q,\boldsymbol\theta^{\mathrm{new}})$ → 新参数下的下界；$\ln p(\mathbf X\mid\boldsymbol\theta^{\mathrm{new}})$ → 新参数下的对数似然。</p>
</figure>

这给出新参数 $\boldsymbol\theta^{\mathrm{new}}$。下界 $\mathcal L$ 因而上升，除非它已处于最大值；相应的对数似然也必然上升。由于 $q$ 是根据旧参数而非新参数确定、且在 M 步保持固定，它不等于新的后验分布 $p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{new}})$，因此 KL 散度非零。故对数似然的增幅大于下界的增幅，如图 15.15 所示。若将 $q(\mathbf Z)=p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})$ 代入式 (15.53)，E 步之后下界为

$$
\begin{aligned}\mathcal L(q,\boldsymbol\theta)&=\sum_{\mathbf Z}p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})\ln p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)\\&\quad-\sum_{\mathbf Z}p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})\ln p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{\mathrm{old}})\\&=Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})+\mathrm{const}.\end{aligned}\tag{15.56}
$$

其中常数就是 $q$ 分布的负熵，因此不依赖 $\boldsymbol\theta$。这里的 $Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})$ 正是式 (15.23) 定义的完整数据对数似然期望，也就是 M 步中最大化的量，正如前面在高斯混合分布中看到的（见第 15.3 节）。注意，待优化的变量 $\boldsymbol\theta$ 只出现在对数内部。如果联合分布 $p(\mathbf Z,\mathbf X\mid\boldsymbol\theta)$ 属于指数族，或是指数族成员的乘积，对数便会抵消指数，使 M 步通常远比最大化相应的不完整数据对数似然 $p(\mathbf X\mid\boldsymbol\theta)$ 容易。

**译注：** 式 (15.56) 的常数项是 $-\sum_{\mathbf Z}q(\mathbf Z)\ln q(\mathbf Z)$，按通常定义为熵；原书称其为“负熵”，这里保留原文措辞。

EM 算法的运行也可从参数空间的角度理解，如图 15.16 所示。红色曲线为我们想最大化的（不完整数据）对数似然函数。从初始参数 $\boldsymbol\theta^{\mathrm{old}}$ 出发，在第一次 E 步计算潜变量的后验分布，得到蓝色曲线所示的下界 $\mathcal L(q,\boldsymbol\theta)$；在 $\boldsymbol\theta^{\mathrm{old}}$ 处，其值等于对数似然。注意，下界在 $\boldsymbol\theta^{\mathrm{old}}$ 处与对数似然相切，因而两条

<!-- pdf-page: 503 -->
<!-- join-previous-paragraph -->

曲线的梯度相同。

<figure id="fig-15-16">
  <img src="books/bishop-deep-learning-2024/assets/chapter-15/fig-15-16.png" alt="EM 算法在参数空间中交替计算下界并最大化的三条曲线">
  <figcaption>图 15.16：EM 算法交替计算当前参数下对数似然的下界，再最大化该下界以得到新的参数值。详见正文。</figcaption>
  <p class="figure-translation">图内文字：$\boldsymbol\theta^{(\mathrm{old})}$ → 旧参数；$\boldsymbol\theta^{(\mathrm{new})}$ → 新参数；$\ln p(\mathbf X\mid\boldsymbol\theta)$ → 对数似然；$\mathcal L(\boldsymbol\theta,\boldsymbol\theta^{(\mathrm{old})})$ → 旧参数对应的下界；E → E 步；M → M 步。</p>
</figure>

对于来自指数族的混合分量，这一下界是具有唯一最大值的凸函数。在 M 步，将下界最大化，得到 $\boldsymbol\theta^{(\mathrm{new})}$；对应的对数似然值高于 $\boldsymbol\theta^{(\mathrm{old})}$ 处的值。随后的 E 步构造在 $\boldsymbol\theta^{(\mathrm{new})}$ 处相切的下界，即图中的绿色曲线。

**译注：** 原书称这个有唯一最大值的下界为“凸函数”；按照常用定义，最大化图示的形状对应凹函数。这里保留原文。

我们已经看到，EM 算法的 E 步与 M 步都会提高一个明确定义的对数似然下界；完整的 EM 循环会改变模型参数，使对数似然增加，除非它已经处于最大值，此时参数保持不变。

### 15.4.2 独立同分布数据

对于独立同分布数据集，$\mathbf X$ 包含 $N$ 个数据点 $\{\mathbf x_n\}$，$\mathbf Z$ 则包含 $N$ 个相应的潜变量 $\{\mathbf z_n\}$，其中 $n=1,\ldots,N$。由独立性假设，$p(\mathbf X,\mathbf Z)=\prod_n p(\mathbf x_n,\mathbf z_n)$；对 $\{\mathbf z_n\}$ 边缘化后，$p(\mathbf X)=\prod_n p(\mathbf x_n)$。利用加法和乘法规则，E 步计算的后验概率为

$$
\begin{aligned}p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)&=\frac{p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)}{\sum_{\mathbf Z}p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)}\\&=\frac{\prod_{n=1}^{N}p(\mathbf x_n,\mathbf z_n\mid\boldsymbol\theta)}{\sum_{\mathbf Z}\prod_{n=1}^{N}p(\mathbf x_n,\mathbf z_n\mid\boldsymbol\theta)}\\&=\prod_{n=1}^{N}p(\mathbf z_n\mid\mathbf x_n,\boldsymbol\theta),\end{aligned}\tag{15.57}
$$

因此，后验分布对于 $n$ 也可分解。对于高斯混合模型，这只是说某分量对数据点 $\mathbf x_n$ 的责任度仅取决于 $\mathbf x_n$ 的值及混合分量的参数 $\boldsymbol\theta$，

<!-- pdf-page: 504 -->
<!-- join-previous-paragraph -->

而不依赖其他数据点的值。

### 15.4.3 参数先验

若为模型参数引入先验 $p(\boldsymbol\theta)$，也可用 EM 算法最大化参数的后验分布 $p(\boldsymbol\theta\mid\mathbf X)$。因为将其视作 $\boldsymbol\theta$ 的函数时，有 $p(\boldsymbol\theta\mid\mathbf X)=p(\boldsymbol\theta,\mathbf X)/p(\mathbf X)$，所以

$$
\ln p(\boldsymbol\theta\mid\mathbf X)=\ln p(\boldsymbol\theta,\mathbf X)-\ln p(\mathbf X).\tag{15.58}
$$

利用分解式 (15.52)，得到

$$
\begin{aligned}\ln p(\boldsymbol\theta\mid\mathbf X)&=\mathcal L(q,\boldsymbol\theta)+\operatorname{KL}(q\parallel p)+\ln p(\boldsymbol\theta)-\ln p(\mathbf X)\\&\geqslant\mathcal L(q,\boldsymbol\theta)+\ln p(\boldsymbol\theta)-\ln p(\mathbf X),\end{aligned}\tag{15.59}
$$

其中 $\ln p(\mathbf X)$ 为常数。可以再次交替对 $q$ 和 $\boldsymbol\theta$ 优化右边。对 $q$ 优化得到与标准 EM 相同的 E 步方程，因为 $q$ 只出现在 $\mathcal L(q,\boldsymbol\theta)$ 中。由于加入先验项 $\ln p(\boldsymbol\theta)$，M 步方程会改变，不过通常只需对标准极大似然 M 步方程略作修改。新增项是一种正则化形式（见第 9 章），能消除高斯混合模型的似然函数奇异点。

### 15.4.4 广义 EM

EM 算法把可能很难的似然最大化问题拆分为 E 步和 M 步两个阶段，通常分别更容易实现。不过，对于复杂模型，E 步、M 步或两者仍可能难以精确求解，于是有以下两种扩展。

**广义 EM**（generalized EM，GEM）算法处理 M 步难以求解的情形。它不求对 $\boldsymbol\theta$ 完全最大化 $\mathcal L(q,\boldsymbol\theta)$，而是改变参数以提高该值。由于 $\mathcal L(q,\boldsymbol\theta)$ 是对数似然的下界，GEM 每个完整的 EM 循环仍保证提高对数似然，除非参数已对应一个局部最大值。GEM 的一种用法是，在 M 步采用基于梯度的迭代优化算法。另一种 GEM 形式称为**期望条件最大化**算法，每个 M 步包含若干受约束的优化（Meng 和 Rubin，1993）。例如，可将参数分组，把 M 步拆成多个步骤，每一步优化一组参数，固定其余组。

同样，也可通过对 $q(\mathbf Z)$ 只作部分而非完整的 $\mathcal L(q,\boldsymbol\theta)$ 优化，推广 EM 的 E 步（Neal 和 Hinton，1999）。如前所见，对于任意给定的 $\boldsymbol\theta$，$\mathcal L(q,\boldsymbol\theta)$ 关于 $q(\mathbf Z)$ 有唯一最大值，对应后验分布 $q_{\boldsymbol\theta}(\mathbf Z)=$

<!-- pdf-page: 505 -->
<!-- join-previous-paragraph -->

$p(\mathbf Z\mid\mathbf X,\boldsymbol\theta)$；对该 $q(\mathbf Z)$，下界 $\mathcal L(q,\boldsymbol\theta)$ 等于对数似然 $\ln p(\mathbf X\mid\boldsymbol\theta)$。因此，任何收敛到 $\mathcal L(q,\boldsymbol\theta)$ 全局最大值的算法，也会找到使对数似然 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 全局最大的 $\boldsymbol\theta$。只要 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$ 是 $\boldsymbol\theta$ 的连续函数，由连续性，$\mathcal L(q,\boldsymbol\theta)$ 的任一局部最大值也对应 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 的局部最大值。

### 15.4.5 顺序 EM

考虑 $N$ 个独立数据点 $\mathbf x_1,\ldots,\mathbf x_N$ 及对应的潜变量 $\mathbf z_1,\ldots,\mathbf z_N$。联合分布 $p(\mathbf X,\mathbf Z\mid\boldsymbol\theta)$ 对各数据点可分解，因此可以利用这一结构构造**增量式 EM**，在每个 EM 循环中只处理一个数据点。E 步不重新计算所有数据点的责任度，而只重新计算一个数据点的责任度。随后 M 步似乎仍需对所有数据点的责任度进行计算；但如果混合分量属于指数族，责任度只通过简单的充分统计量进入，这些量可以高效更新。

例如，考虑一个高斯混合分布，并假设更新数据点 $m$ 时，其责任度的旧值和新值分别为 $\gamma^{\mathrm{old}}(z_{mk})$ 与 $\gamma^{\mathrm{new}}(z_{mk})$。在 M 步，所需充分统计量可增量更新。对于均值，由式 (15.16) 和 (15.17) 定义的充分统计量可得

$$
\boldsymbol\mu_k^{\mathrm{new}}=\boldsymbol\mu_k^{\mathrm{old}}+\left(\frac{\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk})}{N_k^{\mathrm{new}}}\right)(\mathbf x_m-\boldsymbol\mu_k^{\mathrm{old}}),\tag{15.60}
$$

同时

$$
N_k^{\mathrm{new}}=N_k^{\mathrm{old}}+\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk}).\tag{15.61}
$$

协方差及混合系数的相应结果与之类似。

因此，E 步和 M 步都只需固定时间，与数据点总数无关。参数在处理每个数据点后立即更新，而不是等处理完整个数据集，所以增量版可能比批量版收敛更快。增量算法中的每个 E 步或 M 步都提高 $\mathcal L(q,\boldsymbol\theta)$ 的值。正如上面已经证明的，如果算法收敛到 $\mathcal L(q,\boldsymbol\theta)$ 的局部或全局最大值，也就对应于对数似然 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 的局部或全局最大值。

## 习题

**15.1（★）** 考虑第 15.1 节讨论的 K 均值算法。证明：由于离散指示变量 $r_{nk}$ 的分配方式只有有限种，而且对每种分配，$\{\boldsymbol\mu_k\}$ 都有唯一最优值，K 均值算法必会在有限次迭代后收敛。

<!-- pdf-page: 506 -->

**15.2（★★）** 本题推导 K 均值算法的顺序形式。每一步考虑一个新数据点 $\mathbf x_n$，只更新离它最近的原型向量。从批量情形下原型向量的式 (15.4) 出发，把最后一个数据点 $\mathbf x_n$ 的贡献单独分离出来。整理公式，证明更新具有式 (15.5) 的形式。注意，此推导没有作近似，因此所得每个原型向量仍等于分配给它的所有数据向量的均值。

**15.3（★）** 考虑一个高斯混合模型，潜变量的边缘分布 $p(\mathbf z)$ 由式 (15.9) 给出，给定潜变量时观测变量的条件分布 $p(\mathbf x\mid\mathbf z)$ 由式 (15.10) 给出。证明对所有可能的 $\mathbf z$ 求和以边缘化联合分布 $p(\mathbf z)p(\mathbf x\mid\mathbf z)$，所得的 $p(\mathbf x)$ 是式 (15.6) 形式的高斯混合分布。

**15.4（★）** 证明：在有 $K$ 个分量的混合模型中，因交换对称性而等价的参数设置有 $K!$ 种。

**15.5（★★）** 假设希望用 EM 算法最大化含有潜变量的模型的参数后验分布 $p(\boldsymbol\theta\mid\mathbf X)$，其中 $\mathbf X$ 是观测数据集。证明 E 步与极大似然情形相同，而 M 步要最大化的是 $Q(\boldsymbol\theta,\boldsymbol\theta^{\mathrm{old}})+\ln p(\boldsymbol\theta)$，其中 $Q$ 由式 (15.23) 定义。

**15.6（★）** 考虑图 15.9 所示高斯混合模型的有向图。利用 d 分离准则（见第 11.2 节），证明潜变量的后验分布对不同数据点可分解，即

$$
p(\mathbf Z\mid\mathbf X,\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi)=\prod_{n=1}^{N}p(\mathbf z_n\mid\mathbf x_n,\boldsymbol\mu,\boldsymbol\Sigma,\boldsymbol\pi).\tag{15.62}
$$

**15.7（★★）** 考虑高斯混合模型的一个特例：所有分量的协方差矩阵 $\boldsymbol\Sigma_k$ 都被约束为共同的 $\boldsymbol\Sigma$。推导在此模型下最大化似然函数的 EM 方程。

**15.8（★★）** 验证：对于高斯混合模型，最大化完整数据对数似然 (15.26) 后，各分量的均值与协方差分别独立地拟合相应数据点组，混合系数等于各组数据点所占的比例。

**15.9（★★）** 证明：保持责任度 $\gamma(z_{nk})$ 不变，对 $\boldsymbol\mu_k$ 最大化式 (15.30)，得到式 (15.16) 给出的闭式解。

**15.10（★★）** 证明：保持责任度 $\gamma(z_{nk})$ 不变，对 $\boldsymbol\Sigma_k$ 和 $\pi_k$ 最大化式 (15.30)，得到式 (15.18) 和 (15.21) 给出的闭式解。

<!-- pdf-page: 507 -->

**15.11（★★）** 考虑由下列混合分布给出的密度模型：

$$
p(\mathbf x)=\sum_{k=1}^{K}\pi_kp(\mathbf x\mid k).\tag{15.63}
$$

设将向量 $\mathbf x$ 分成 $\mathbf x=(\mathbf x_a,\mathbf x_b)$ 两部分。证明条件密度 $p(\mathbf x_b\mid\mathbf x_a)$ 本身也是混合分布，并求出其混合系数和分量密度的表达式。

**15.12（★）** 在第 15.3.2 节，通过考虑各分量协方差均为 $\epsilon\mathbf I$ 的混合模型，建立了 K 均值与高斯混合分布 EM 的关系。证明当 $\epsilon\to0$ 时，最大化式 (15.30) 给出的该模型完整数据对数似然期望，等价于最小化式 (15.1) 给出的 K 均值误差度量 $J$。

**15.13（★★）** 验证伯努利分布均值与协方差的式 (15.35) 和 (15.36)。

**15.14（★★）** 考虑如下形式的混合分布：

$$
p(\mathbf x)=\sum_{k=1}^{K}\pi_kp(\mathbf x\mid k),\tag{15.64}
$$

其中 $\mathbf x$ 的分量可以是离散变量、连续变量或二者的组合。设 $p(\mathbf x\mid k)$ 的均值和协方差分别为 $\boldsymbol\mu_k$ 和 $\boldsymbol\Sigma_k$。利用习题 15.13 的结果，证明混合分布的均值与协方差由式 (15.39) 和 (15.40) 给出。

**15.15（★★）** 利用 EM 算法的重估方程，证明伯努利混合分布若参数对应于似然函数的最大值，则具有以下性质：

$$
\mathbb E[\mathbf x]=\frac{1}{N}\sum_{n=1}^{N}\mathbf x_n\equiv\bar{\mathbf x}.\tag{15.65}
$$

进而证明：若此模型的参数初始化为所有分量都具有相同均值 $\boldsymbol\mu_k=\hat{\boldsymbol\mu}$，其中 $k=1,\ldots,K$，那么不论初始混合系数如何选取，EM 算法均会在一次迭代后收敛，并且此解满足 $\boldsymbol\mu_k=\bar{\mathbf x}$。注意，这是混合模型的退化情形：所有分量完全相同。实际中，应采用适当初始化以避免这类解。

**15.16（★）** 考虑将式 (15.42) 的 $p(\mathbf x\mid\mathbf z,\boldsymbol\mu)$ 与式 (15.43) 的 $p(\mathbf z\mid\boldsymbol\pi)$ 相乘得到的伯努利模型潜变量与观测变量的联合分布。证明对该联合分布中的 $\mathbf z$ 边缘化后，得到式 (15.37)。

<!-- pdf-page: 508 -->

**15.17（★）** 证明：对 $\boldsymbol\mu_k$ 最大化伯努利混合分布的完整数据对数似然期望 (15.45)，得到 M 步方程 (15.49)。

**15.18（★）** 证明：对混合系数 $\pi_k$ 最大化伯努利混合分布的完整数据对数似然期望 (15.45)，并用拉格朗日乘子强制满足求和约束，得到 M 步方程 (15.50)。

**15.19（★）** 证明：由离散变量 $\mathbf x_n$ 满足的约束 $0\leqslant p(\mathbf x_n\mid\boldsymbol\mu_k)\leqslant1$，可知伯努利混合分布的不完整数据对数似然函数有上界，因而不存在使似然趋于无穷大的奇异点。

**15.20（★★★）** 考虑 $D$ 维变量 $\mathbf x$，其中每个分量 $i$ 本身都是具有 $M$ 个状态的多项变量。因此，$\mathbf x$ 是具有分量 $x_{ij}$ 的二元向量，其中 $i=1,\ldots,D$、$j=1,\ldots,M$，且对所有 $i$ 满足 $\sum_jx_{ij}=1$。设这些变量的分布由离散多项分布的混合描述（见第 3.1.3 节）：

$$
p(\mathbf x)=\sum_{k=1}^{K}\pi_kp(\mathbf x\mid\boldsymbol\mu_k),\tag{15.66}
$$

其中

$$
p(\mathbf x\mid\boldsymbol\mu_k)=\prod_{i=1}^{D}\prod_{j=1}^{M}\mu_{kij}^{x_{ij}}.\tag{15.67}
$$

参数 $\mu_{kij}$ 表示概率 $p(x_{ij}=1\mid\boldsymbol\mu_k)$，须满足 $0\leqslant\mu_{kij}\leqslant1$，且对所有 $k$ 和 $i$ 有 $\sum_j\mu_{kij}=1$。给定观测数据集 $\{\mathbf x_n\}$，其中 $n=1,\ldots,N$，推导用极大似然优化该分布的混合系数 $\pi_k$ 和分量参数 $\mu_{kij}$ 的 EM 算法 E 步和 M 步方程。

**15.21（★）** 验证关系式 (15.52)，其中 $\mathcal L(q,\boldsymbol\theta)$ 与 $\operatorname{KL}(q\parallel p)$ 分别由式 (15.53) 和 (15.54) 定义。

**15.22（★）** 证明：式 (15.53) 给出的下界 $\mathcal L(q,\boldsymbol\theta)$，当 $q(\mathbf Z)=p(\mathbf Z\mid\mathbf X,\boldsymbol\theta^{(\mathrm{old})})$ 时，在 $\boldsymbol\theta=\boldsymbol\theta^{(\mathrm{old})}$ 处对 $\boldsymbol\theta$ 的梯度与对数似然函数 $\ln p(\mathbf X\mid\boldsymbol\theta)$ 的梯度相同。

**15.23（★★）** 考虑高斯混合分布 EM 算法的增量形式，其中只重新计算某个数据点 $\mathbf x_m$ 的责任度。从 M 步公式 (15.16) 和 (15.17) 出发，推导分量均值的更新式 (15.60) 和 (15.61)。

**15.24（★★）** 当责任度以增量方式更新时，推导高斯混合模型中协方差矩阵与混合系数的 M 步更新公式，形式应类似于均值更新式 (15.60)。
