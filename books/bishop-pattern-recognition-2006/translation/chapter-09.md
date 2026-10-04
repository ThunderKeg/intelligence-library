# 第 9 章 混合模型与 EM

<aside class="chapter-guide"><strong>本章导读</strong><p>本章从 K 均值聚类出发，说明如何用混合模型表达数据中的不同群体，并用潜变量描述每个样本属于哪个分量。随后推导 EM 算法，展示它如何交替估计潜变量与更新模型参数，以及它与 K 均值、最大似然和贝叶斯方法的联系。</p></aside>

<!-- pdf-page: 443 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-chapter-opening.png" alt="水面纹理上的第 9 章标题"><p class="figure-translation">Mixture Models and EM → 混合模型与 EM。</p></figure>

如果我们在观测变量与潜变量上定义联合分布，那么仅包含观测变量的相应分布可以通过边缘化得到。这样，观测变量上较复杂的边缘分布，就能用扩展后的观测变量与潜变量空间上更容易处理的联合分布来表达。因此，引入潜变量使我们能够用较简单的组成部分构造复杂分布。本章将看到，混合分布，例如第 2.3.9 节讨论的高斯混合，可以用离散潜变量来解释。连续潜变量则是第 12 章的主题。

混合模型不仅为构建更复杂的概率分布提供了框架，还可以用于数据聚类。因此，我们从在一组数据点中寻找簇的问题开始讨论混合分布，首先采用一种称为 K 均值（K-means）算法的非概率方法（Lloyd, 1982）。<span class="margin-reference">第 9.1 节</span>随后，我们再从潜变量的

<!-- pdf-page: 444 -->
<!-- join-previous-paragraph -->
角度来看混合分布，其中离散潜变量可以解释为规定了如何把数据点分配给混合分布的特定分量。<span class="margin-reference">第 9.2 节</span>在潜变量模型中求最大似然估计的一种通用技术，是期望最大化（expectation-maximization，EM）算法。我们先用高斯混合分布，以较为直观的方式引出 EM 算法，然后再从潜变量的角度作更严谨的讨论。<span class="margin-reference">第 9.3 节</span>我们将看到，K 均值算法对应于把 EM 应用于高斯混合时的一种特殊的非概率极限情形。最后，我们对 EM 作较一般的讨论。<span class="margin-reference">第 9.4 节</span>

高斯混合模型广泛应用于数据挖掘、模式识别、机器学习和统计分析。在许多应用中，模型参数通过最大似然来确定，通常采用 EM 算法。不过，我们将看到，最大似然方法存在一些明显的局限。第 10 章将说明，使用变分推断框架可以给出一种简洁的贝叶斯处理方法。与 EM 相比，这种方法几乎不增加计算量，却能解决最大似然的主要困难，还能根据数据自动推断混合分布的分量数。

## 9.1 K 均值聚类

我们首先考虑如何在多维空间中识别数据点的群组，也就是簇。假设数据集 $\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 包含一个 $D$ 维欧氏随机变量 $\mathbf{x}$ 的 $N$ 个观测。我们的目标是把数据集划分为 $K$ 个簇，暂且假设 $K$ 的值已经给定。直观地说，一个簇由一组数据点组成，与到簇外数据点的距离相比，这些点彼此之间的距离较小。要把这一想法形式化，我们先引入一组 $D$ 维向量 $\boldsymbol{\mu}_k$，其中 $k=1,\ldots,K$，$\boldsymbol{\mu}_k$ 是与第 $k$ 个簇关联的原型。我们很快就会看到，可以把 $\boldsymbol{\mu}_k$ 看作簇的中心。于是，我们的目标是找出数据点到簇的分配方式，以及一组向量 $\{\boldsymbol{\mu}_k\}$，使每个数据点到最近向量 $\boldsymbol{\mu}_k$ 的距离平方之和最小。

这里先定义一些符号，以便描述数据点到簇的分配。对每个数据点 $\mathbf{x}_n$，我们引入一组对应的二元指示变量 $r_{nk}\in\{0,1\}$，其中 $k=1,\ldots,K$，用来说明数据点 $\mathbf{x}_n$ 被分配给了 $K$ 个簇中的哪一个。如果数据点 $\mathbf{x}_n$ 被分配给簇 $k$，就有 $r_{nk}=1$，而对于 $j\ne k$，则有 $r_{nj}=0$。这称为 1-of-K 编码方案。随后，我们可以定义一个目标函数，有时也称为失真度量（distortion measure）：

$$
J=\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2
\tag{9.1}
$$

它表示各数据点到所分配的

<!-- pdf-page: 445 -->
<!-- join-previous-paragraph -->
向量 $\boldsymbol{\mu}_k$ 的距离平方之和。我们的目标是找出使 $J$ 最小的 $\{r_{nk}\}$ 和 $\{\boldsymbol{\mu}_k\}$。为此可以采用迭代过程，每轮迭代包含两个相继执行的步骤，分别依次对 $r_{nk}$ 和 $\boldsymbol{\mu}_k$ 进行优化。首先，我们为 $\boldsymbol{\mu}_k$ 选择一些初始值。然后在第一阶段，固定 $\boldsymbol{\mu}_k$，对 $r_{nk}$ 最小化 $J$；在第二阶段，固定 $r_{nk}$，对 $\boldsymbol{\mu}_k$ 最小化 $J$。反复进行这两个阶段的优化，直到收敛。我们将看到，更新 $r_{nk}$ 和更新 $\boldsymbol{\mu}_k$ 这两个阶段，分别对应于 EM 算法的 E（期望）步和 M（最大化）步。<span class="margin-reference">第 9.4 节</span>为了强调这一点，在讨论 K 均值算法时，我们也使用 E 步和 M 步这两个名称。

先考虑如何确定 $r_{nk}$。由于式（9.1）中的 $J$ 是 $r_{nk}$ 的线性函数，很容易完成这一优化并得到闭式解。涉及不同 $n$ 的项相互独立，因此可以分别对每个 $n$ 进行优化：对于使 $\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2$ 最小的那个 $k$，将 $r_{nk}$ 设为 $1$。换言之，我们只需把第 $n$ 个数据点分配给最近的簇中心。更正式地，可以写为

$$
r_{nk}=\begin{cases}
1&\text{若 }k=\arg\min_j\|\mathbf{x}_n-\boldsymbol{\mu}_j\|^2\\
0&\text{其他情况。}
\end{cases}
\tag{9.2}
$$

现在考虑固定 $r_{nk}$ 时对 $\boldsymbol{\mu}_k$ 的优化。目标函数 $J$ 是 $\boldsymbol{\mu}_k$ 的二次函数，将它对 $\boldsymbol{\mu}_k$ 的导数设为零，就可以求出最小值，得到

$$
2\sum_{n=1}^{N}r_{nk}(\mathbf{x}_n-\boldsymbol{\mu}_k)=0
\tag{9.3}
$$

由此很容易解出 $\boldsymbol{\mu}_k$：

$$
\boldsymbol{\mu}_k=\frac{\sum_n r_{nk}\mathbf{x}_n}{\sum_n r_{nk}}.
\tag{9.4}
$$

这个表达式的分母等于分配给簇 $k$ 的数据点数，因此该结果有一个简单的解释：把 $\boldsymbol{\mu}_k$ 设为所有分配给簇 $k$ 的数据点 $\mathbf{x}_n$ 的均值。这也正是该过程被称为 K 均值算法的原因。

把数据点重新分配给各簇、重新计算簇均值，这两个阶段交替重复，直到分配不再发生变化，或者超过某个最大迭代次数。由于每个阶段都会减小目标函数 $J$ 的值，算法的收敛是有保证的。<span class="margin-reference">习题 9.1</span>不过，它可能收敛到 $J$ 的局部极小值，而非全局极小值。MacQueen（1967）研究了 K 均值算法的收敛性质。

图 9.1 用 Old Faithful 数据集说明 K 均值算法。<span class="margin-reference">附录 A</span>在这个例子中，我们对数据进行了称为标准化（standardizing）的线性缩放，使每个变量的均值为零、标准差为一。我们选择 $K=2$，因此在这个

<!-- pdf-page: 446 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-1.png" alt="K 均值算法从初始中心到收敛的九幅散点图"><figcaption>图 9.1：用重新缩放后的 Old Faithful 数据集说明 K 均值算法。（a）绿色点表示二维欧氏空间中的数据集。中心 $\boldsymbol{\mu}_1$ 和 $\boldsymbol{\mu}_2$ 的初始选择分别用红色和蓝色叉号表示。（b）在最初的 E 步中，根据哪个簇中心更近，把每个数据点分配给红色簇或蓝色簇。这等价于按照数据点位于两个簇中心的垂直平分线哪一侧来进行分类；该垂直平分线用品红色直线表示。（c）在随后的 M 步中，把每个簇中心重新计算为分配给相应簇的所有点的均值。（d）—（i）展示了后续的 E 步与 M 步，直到算法最终收敛。</figcaption></figure>

<!-- pdf-page: 447 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-2.png" alt="K 均值每次 E 步和 M 步之后的代价函数 J"><figcaption>图 9.2：对于图 9.1 的例子，绘出 K 均值算法每次 E 步（蓝点）和 M 步（红点）之后由式（9.1）给出的代价函数 $J$。算法在第三次 M 步后已经收敛，最后一轮 EM 循环没有改变数据点的分配或原型向量。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
例子中，把每个数据点分配给最近的簇中心，等价于按照数据点位于两个簇中心的垂直平分线哪一侧来分类。图 9.2 绘出了 Old Faithful 例子中由式（9.1）给出的代价函数 $J$。

注意，我们刻意为簇中心选择了较差的初始值，使算法需要经过几个步骤才收敛。在实践中，更好的初始化方法是随机选取 $K$ 个数据点组成一个子集，并将簇中心 $\boldsymbol{\mu}_k$ 设为这些点。还应注意，在对高斯混合模型应用 EM 算法之前，经常使用 K 均值算法本身来初始化模型参数。<span class="margin-reference">第 9.2.2 节</span>

直接实现这里讨论的 K 均值算法，速度可能较慢，因为每次 E 步都必须计算每个原型向量与每个数据点之间的欧氏距离。人们提出了多种加速 K 均值算法的方案。其中一些方案会预先计算树之类的数据结构，使相近的点位于同一子树中（Ramasubramanian and Paliwal, 1990; Moore, 2000）。另一些方法利用距离的三角不等式，避免不必要的距离计算（Hodgson, 1998; Elkan, 2003）。

到目前为止，我们考虑的是 K 均值的批量版本，它使用整个数据集一起更新原型向量。我们还可以把 Robbins–Monro 方法用于寻找回归函数的根，从而推导出一种在线随机算法（MacQueen, 1967）；这里的回归函数由式（9.1）中的 $J$ 对 $\boldsymbol{\mu}_k$ 求导得到。<span class="margin-reference">第 2.3.5 节</span>由此得到一种顺序更新方法：依次对每个数据点 $\mathbf{x}_n$，用下式更新最近的原型 $\boldsymbol{\mu}_k$：<span class="margin-reference">习题 9.2</span>

$$
\boldsymbol{\mu}_k^{\mathrm{new}}=\boldsymbol{\mu}_k^{\mathrm{old}}+\eta_n(\mathbf{x}_n-\boldsymbol{\mu}_k^{\mathrm{old}})
\tag{9.5}
$$

其中 $\eta_n$ 是学习率参数，通常随着处理的数据点增多而单调减小。

K 均值算法使用欧氏距离的平方来衡量数据点与原型向量之间的不相似程度。这不仅限制了可以考虑的数据变量类型，例如当部分或全部变量表示类别标签时，这种度量就不合适，

<!-- pdf-page: 448 -->
<!-- join-previous-paragraph -->
而且可能使簇均值的确定对离群点缺乏鲁棒性。<span class="margin-reference">第 2.3.7 节</span>我们可以在两个向量 $\mathbf{x}$ 和 $\mathbf{x}'$ 之间引入更一般的不相似度量 $\mathcal{V}(\mathbf{x},\mathbf{x}')$，然后最小化下列失真度量，从而推广 K 均值算法：

$$
\widetilde{J}=\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\mathcal{V}(\mathbf{x}_n,\boldsymbol{\mu}_k)
\tag{9.6}
$$

这样就得到 K 中心点（K-medoids）算法。其 E 步仍然是在给定簇原型 $\boldsymbol{\mu}_k$ 后，把每个数据点分配给与它不相似度最小的原型所对应的簇。与标准 K 均值算法一样，这一步的计算代价为 $O(KN)$。对于一般的不相似度量，M 步可能比 K 均值中的 M 步更复杂。因此，通常把每个簇原型限制为分配给该簇的某个数据向量。这样，只要不相似度量 $\mathcal{V}(\cdot,\cdot)$ 容易计算，不论选用何种度量，都可以实现这一算法。因此，对于每个簇 $k$，M 步需要在分配给该簇的 $N_k$ 个点中进行离散搜索，需要计算 $O(N_k^2)$ 次 $\mathcal{V}(\cdot,\cdot)$。

K 均值算法的一个显著特点是，每轮迭代中，每个数据点都被唯一地分配给一个且仅一个簇。对于一些数据点，它们到某个特定中心 $\boldsymbol{\mu}_k$ 的距离远小于到其他中心的距离；但另一些数据点可能大致位于簇中心之间的中间位置。对于后一种情况，把数据点硬性分配给最近的簇是否最合适，并不明确。下一节将看到，采用概率方法后，我们可以对数据点进行“软”分配，使这种分配反映对最佳簇归属的不确定程度。这种概率表述带来了许多好处。

### 9.1.1 图像分割与压缩

为了说明 K 均值算法的应用，我们考虑图像分割和图像压缩这两个相关问题。分割的目标是把图像划分为多个区域，每个区域的视觉外观相对一致，或者对应于物体或物体的一部分（Forsyth and Ponce, 2003）。图像中的每个像素，都是由红、蓝、绿通道的强度组成的三维空间中的一个点。我们的分割算法仅把图像中的每个像素当作单独的数据点。注意，严格来说，这个空间不是欧氏空间，因为各通道的强度被限制在区间 $[0,1]$ 内。尽管如此，我们仍可以直接应用 K 均值算法。对于任意给定的 $K$，为了展示 K 均值运行到收敛后的结果，我们重新绘制图像，将每个像素向量替换为分配给它的中心 $\boldsymbol{\mu}_k$ 所给出的 $\{R,G,B\}$ 强度三元组。图 9.3 展示了不同 $K$ 值的结果。可以看到，对于给定的 $K$，算法用仅含 $K$ 种颜色的调色板表示整幅图像。必须强调，把 K 均值用于图像分割并不是一种特别精细的方法，其中一个明显原因是它没有考虑不同像素在空间上是否相邻。一般来说，图像分割是一个极其困难的

<!-- pdf-page: 449 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-3.png" alt="两幅原始图像及分别用 2、3、10 种颜色分割后的图像"><figcaption>图 9.3：将 K 均值聚类算法用于图像分割的两个例子，展示了原始图像，以及采用不同 $K$ 值得到的 K 均值分割结果。这也说明了如何用向量量化进行数据压缩：较小的 $K$ 带来更高的压缩程度，但代价是图像质量降低。</figcaption><p class="figure-translation">Original image → 原始图像。</p></figure>

<!-- join-previous-paragraph-across-figures -->
问题，至今仍是活跃的研究课题；这里引入它，只是为了说明 K 均值算法的行为。

我们也可以使用聚类算法的结果进行数据压缩。必须区分无损数据压缩（lossless data compression）与有损数据压缩（lossy data compression）：前者的目标是能够从压缩表示中精确重建原始数据；后者则允许重建时出现一定误差，以换取比无损压缩更高的压缩程度。我们可以按以下方式把 K 均值算法用于有损数据压缩。对于 $N$ 个数据点中的每一个，只存储它被分配到的簇的标识 $k$。此外，还要存储 $K$ 个簇中心 $\boldsymbol{\mu}_k$ 的值。只要选择 $K\ll N$，通常就能显著减少所需存储的数据量。然后，用最近的中心 $\boldsymbol{\mu}_k$ 来近似每个数据点。新数据点也可以按同样的方法压缩：先找出最近的 $\boldsymbol{\mu}_k$，再存储标签 $k$，而不存储原始数据向量。这一框架通常称为向量量化（vector quantization），向量 $\boldsymbol{\mu}_k$ 则称为码本向量（code-book vector）。

<!-- pdf-page: 450 -->

上面讨论的图像分割问题，也说明了如何用聚类进行数据压缩。假设原始图像有 $N$ 个像素，每个像素由 $\{R,G,B\}$ 值组成，其中每个值都以 $8$ 位精度存储。那么，直接传输整幅图像需要 $24N$ 比特。现在假设我们先对图像数据运行 K 均值算法，然后传输最近向量 $\boldsymbol{\mu}_k$ 的标识，而不传输原始像素强度向量。由于这样的向量有 $K$ 个，每个像素需要 $\log_2 K$ 比特。我们还必须传输 $K$ 个码本向量 $\boldsymbol{\mu}_k$，这需要 $24K$ 比特。因此，传输图像所需的总比特数为 $24K+N\log_2 K$，向上取到最近的整数。图 9.3 所示原始图像有 $240\times180=43{,}200$ 个像素，因此直接传输需要 $24\times43{,}200=1{,}036{,}800$ 比特。相比之下，压缩后的图像分别需要 $43{,}248$ 比特（$K=2$）、$86{,}472$ 比特（$K=3$）和 $173{,}040$ 比特（$K=10$）。相对于原始图像，这些压缩后的大小分别为 $4.2\%$、$8.3\%$ 和 $16.7\%$。我们看到，压缩程度与图像质量之间需要权衡。注意，这个例子的目的是说明 K 均值算法。如果我们要设计一个好的图像压缩器，那么考虑由相邻像素组成的小块，例如 $5\times5$ 的像素块，会更有成效，因为这样可以利用自然图像中相邻像素之间的相关性。

## 9.2 高斯混合

在第 2.3.9 节中，我们把高斯混合模型作为高斯分量的简单线性叠加引入，目的是得到比单个高斯分布更丰富的一类密度模型。现在，我们转而用离散潜变量来表述高斯混合。这将使我们更深入地理解这一重要分布，并有助于引出期望最大化算法。

回顾式（2.188），高斯混合分布可以写成高斯分布的线性叠加：

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k).
\tag{9.7}
$$

我们引入一个采用 1-of-K 表示的 $K$ 维二元随机变量 $\mathbf{z}$，其中某个特定元素 $z_k$ 等于 $1$，其余所有元素均等于 $0$。因此，$z_k$ 的取值满足 $z_k\in\{0,1\}$ 和 $\sum_k z_k=1$；根据非零元素的位置不同，向量 $\mathbf{z}$ 有 $K$ 种可能的状态。我们用边缘分布 $p(\mathbf{z})$ 和条件分布 $p(\mathbf{x}\mid\mathbf{z})$ 定义联合分布 $p(\mathbf{x},\mathbf{z})$，对应于图 9.4 中的图模型。$\mathbf{z}$ 上的边缘分布由混合系数 $\pi_k$ 指定，使得

$$
p(z_k=1)=\pi_k
$$

<!-- pdf-page: 451 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-4.png" alt="潜变量 z 指向观测变量 x 的混合模型有向图"><figcaption>图 9.4：混合模型的图表示，其中联合分布写成 $p(\mathbf{x},\mathbf{z})=p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})$ 的形式。</figcaption></figure>

其中，为了成为有效的概率，参数 $\{\pi_k\}$ 必须满足

$$
0\leqslant\pi_k\leqslant1
\tag{9.8}
$$

以及

$$
\sum_{k=1}^{K}\pi_k=1
\tag{9.9}
$$

这两个条件。由于 $\mathbf{z}$ 使用 1-of-K 表示，我们还可以把这个分布写成

$$
p(\mathbf{z})=\prod_{k=1}^{K}\pi_k^{z_k}.
\tag{9.10}
$$

类似地，给定 $\mathbf{z}$ 的某个特定取值后，$\mathbf{x}$ 的条件分布是高斯分布：

$$
p(\mathbf{x}\mid z_k=1)=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)
$$

也可以写成

$$
p(\mathbf{x}\mid\mathbf{z})=\prod_{k=1}^{K}\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)^{z_k}.
\tag{9.11}
$$

联合分布由 $p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})$ 给出。对 $\mathbf{z}$ 的所有可能状态求和，就得到 $\mathbf{x}$ 的边缘分布：<span class="margin-reference">习题 9.3</span>

$$
p(\mathbf{x})=\sum_{\mathbf{z}}p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)
\tag{9.12}
$$

这里使用了式（9.10）和式（9.11）。因此，$\mathbf{x}$ 的边缘分布就是式（9.7）形式的高斯混合。如果我们有多个观测 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，那么，由于已经把边缘分布表示为 $p(\mathbf{x})=\sum_{\mathbf{z}}p(\mathbf{x},\mathbf{z})$ 的形式，每个观测数据点 $\mathbf{x}_n$ 都有一个对应的潜变量 $\mathbf{z}_n$。

因此，我们找到了高斯混合的一种等价表述，其中显式引入了潜变量。这样做似乎没有带来多少好处。然而，我们现在能够处理联合分布 $p(\mathbf{x},\mathbf{z})$，

<!-- pdf-page: 452 -->
<!-- join-previous-paragraph -->
而不必处理边缘分布 $p(\mathbf{x})$。这将带来显著的简化，其中最突出的是可以引入期望最大化（EM）算法。

另一个将发挥重要作用的量，是给定 $\mathbf{x}$ 时 $\mathbf{z}$ 的条件概率。我们用 $\gamma(z_k)$ 表示 $p(z_k=1\mid\mathbf{x})$，其值可以通过贝叶斯定理求得：

$$
\begin{aligned}
\gamma(z_k)\equiv p(z_k=1\mid\mathbf{x})&=\frac{p(z_k=1)p(\mathbf{x}\mid z_k=1)}{\displaystyle\sum_{j=1}^{K}p(z_j=1)p(\mathbf{x}\mid z_j=1)}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\displaystyle\sum_{j=1}^{K}\pi_j\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}.
\end{aligned}
\tag{9.13}
$$

我们把 $\pi_k$ 看作 $z_k=1$ 的先验概率，把 $\gamma(z_k)$ 看作观测到 $\mathbf{x}$ 之后相应的后验概率。后面将看到，$\gamma(z_k)$ 也可以理解为分量 $k$ 在“解释”观测 $\mathbf{x}$ 时承担的责任度（responsibility）。

我们可以使用祖先采样技术，生成服从高斯混合模型的随机样本。<span class="margin-reference">第 8.1.2 节</span>为此，先从边缘分布 $p(\mathbf{z})$ 中生成 $\mathbf{z}$ 的一个取值，记为 $\widehat{\mathbf{z}}$，再从条件分布 $p(\mathbf{x}\mid\widehat{\mathbf{z}})$ 中生成 $\mathbf{x}$ 的一个取值。第 11 章将讨论如何从标准分布中采样。为了展示联合分布 $p(\mathbf{x},\mathbf{z})$ 的样本，我们可以在对应的 $\mathbf{x}$ 位置画点，再根据 $\mathbf{z}$ 的取值给这些点着色，也就是根据哪个高斯分量负责生成该点来着色，如图 9.5（a）所示。类似地，只要取联合分布的样本并忽略 $\mathbf{z}$ 的值，就得到边缘分布 $p(\mathbf{x})$ 的样本。图 9.5（b）绘出不带任何颜色标签的 $\mathbf{x}$ 值，展示了这些样本。

我们也可以用这个合成数据集来说明“责任度”：对于每个数据点，计算生成该数据集的混合分布中各个分量的后验概率。具体来说，数据点 $\mathbf{x}_n$ 对应的责任度 $\gamma(z_{nk})$ 可以通过颜色来表示：绘制该点时，分别按照 $k=1,2,3$ 对应的 $\gamma(z_{nk})$ 值，混合相应比例的红、蓝、绿三种墨色，如图 9.5（c）所示。例如，若某个数据点的 $\gamma(z_{n1})=1$，就把它涂成红色；若 $\gamma(z_{n2})=\gamma(z_{n3})=0.5$，则以相等比例混合蓝色和绿色，使其呈青色。可以把这与图 9.5（a）比较：后者根据实际生成各数据点的分量身份来标记颜色。

### 9.2.1 最大似然

假设我们有一组观测数据 $\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，希望用高斯混合对这些数据建模。我们可以把这个数据集表示为一个 $N\times D$

<!-- pdf-page: 453 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-5.png" alt="高斯混合的五百个样本，分别按真实分量、无标签和责任度着色"><figcaption>图 9.5：从图 2.23 所示的三个高斯分量的混合分布中抽取 $500$ 个点的例子。（a）联合分布 $p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})$ 的样本，$\mathbf{z}$ 的三种状态对应于混合分布的三个分量，分别用红、绿、蓝表示。（b）边缘分布 $p(\mathbf{x})$ 的对应样本，只需忽略 $\mathbf{z}$ 的值、仅绘制 $\mathbf{x}$ 的值即可得到。（a）中的数据集称为完整数据，而（b）中的数据集是不完整数据。（c）同一组样本，其颜色表示数据点 $\mathbf{x}_n$ 对应的责任度 $\gamma(z_{nk})$；绘制各点时，分别按照 $k=1,2,3$ 对应的 $\gamma(z_{nk})$ 值，混合相应比例的红、蓝、绿三种墨色。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
矩阵 $\mathbf{X}$，其中第 $n$ 行为 $\mathbf{x}_n^{\mathrm{T}}$。类似地，用一个 $N\times K$ 矩阵 $\mathbf{Z}$ 表示相应的潜变量，其各行为 $\mathbf{z}_n^{\mathrm{T}}$。如果假设各数据点独立地从该分布中抽取，那么对于这个独立同分布数据集，可以用图 9.6 所示的图表示来表达高斯混合模型。根据式（9.7），似然函数的对数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{9.14}
$$

在讨论如何最大化这个函数之前，需要强调：由于存在奇异性，把最大似然框架应用于高斯混合模型时，会遇到一个严重问题。为简单起见，考虑各分量协方差矩阵为 $\boldsymbol{\Sigma}_k=\sigma_k^2\mathbf{I}$ 的高斯混合，其中 $\mathbf{I}$ 是单位矩阵；不过，对一般协方差矩阵，结论同样成立。假设混合模型的某个分量，例如第 $j$ 个分量，其均值 $\boldsymbol{\mu}_j$ 恰好等于某个数据

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-6.png" alt="高斯混合模型的板表示，包含未观测的 z_n、观测的 x_n 及三组参数"><figcaption>图 9.6：对于 $N$ 个独立同分布数据点 $\{\mathbf{x}_n\}$ 及对应潜在点 $\{\mathbf{z}_n\}$ 的高斯混合模型的图表示，其中 $n=1,\ldots,N$。</figcaption></figure>

<!-- pdf-page: 454 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-7.png" alt="高斯混合的一个分量收缩到单个数据点形成尖峰"><figcaption>图 9.7：说明高斯混合的似然函数如何产生奇异性。可以把它与图 1.14 所示单个高斯分布的情形作比较，后者不会出现奇异性。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
点，即对于某个 $n$，有 $\boldsymbol{\mu}_j=\mathbf{x}_n$。这个数据点将对似然函数贡献如下形式的一项：

$$
\mathcal{N}(\mathbf{x}_n\mid\mathbf{x}_n,\sigma_j^2\mathbf{I})=\frac{1}{(2\pi)^{1/2}}\frac{1}{\sigma_j}.
\tag{9.15}
$$

如果考虑极限 $\sigma_j\to0$，就会发现这一项趋于无穷大，因此对数似然函数也趋于无穷大。于是，最大化对数似然函数并不是一个适定问题，因为这种奇异性始终存在：只要某个高斯分量“塌缩”到某个特定数据点，就会发生。回想一下，对于单个高斯分布，并没有出现这一问题。要理解两者的区别，可以注意到：如果单个高斯分布塌缩到某个数据点，其他数据点仍会给似然函数贡献相乘的因子，而这些因子将以指数速度趋于零，使整个似然趋于零，而不是无穷大。但是，只要混合分布中至少有两个分量，其中一个分量就可以保持有限方差，从而给所有数据点赋予有限概率；另一个分量则可以收缩到某个特定数据点，给对数似然贡献一个不断增大的加性值。图 9.7 展示了这一情形。这些奇异性是最大似然方法可能发生严重过拟合的又一个例子。我们将看到，采用贝叶斯方法时不会出现这一困难。<span class="margin-reference">第 10.1 节</span>不过，目前只需注意：对高斯混合模型应用最大似然时，必须采取措施避免得到这种病态解，转而寻找似然函数中性质良好的局部极大值。我们可以借助适当的启发式方法来尝试避免奇异性。例如，当检测到某个高斯分量正在塌缩时，把它的均值重设为随机选取的值，同时把协方差重设为较大的值，然后继续优化。

寻找最大似然解时还有一个问题：对于任意给定的最大似然解，含 $K$ 个分量的混合分布总共有 $K!$ 个等价解，对应于把 $K$ 组参数分配给 $K$ 个分量的 $K!$ 种方式。换言之，对于参数值空间中任意给定的非退化点，还存在另外 $K!-1$ 个点，它们全都产生完全相同的分布。这一问题称为

<!-- pdf-page: 455 -->
<!-- join-previous-paragraph -->
可辨识性（identifiability；Casella and Berger, 2002）。当我们希望解释模型所得到的参数值时，它是一个重要问题。第 12 章讨论具有连续潜变量的模型时，也会遇到可辨识性问题。不过，如果目的只是寻找一个好的密度模型，这并无影响，因为这些等价解同样好。

最大化高斯混合模型的对数似然函数（9.14），比单个高斯分布的情形更复杂。困难来自式（9.14）中位于对数内部的关于 $k$ 的求和，使得对数函数不再直接作用于高斯分布。我们很快就会看到，即使把对数似然的导数设为零，也不再能得到闭式解。

一种方法是应用基于梯度的优化技术（Fletcher, 1987; Nocedal and Wright, 1999; Bishop and Nabney, 2008）。基于梯度的技术是可行的，而且当我们讨论第 5 章的混合密度网络时，它们会发挥重要作用。不过，现在我们考虑另一种方法，即 EM 算法。它的适用范围很广，也将为第 10 章讨论变分推断技术奠定基础。

### 9.2.2 高斯混合的 EM 算法

对于含潜变量的模型，有一种简洁而有力的最大似然求解方法，称为期望最大化算法，或 EM 算法（Dempster et al., 1977; McLachlan and Krishnan, 1997）。后面我们会对 EM 作一般性的讨论，并说明如何推广 EM，从而得到变分推断框架。<span class="margin-reference">第 10.1 节</span>首先，我们在高斯混合模型的背景下，通过较为直观的讨论来引出 EM 算法。不过需要强调，EM 有很广的适用范围，本书中许多不同模型都会用到它。

我们先写出似然函数达到极大值时必须满足的条件。把式（9.14）中的 $\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})$ 对各高斯分量均值 $\boldsymbol{\mu}_k$ 的导数设为零，得到

$$
0=-\sum_{n=1}^{N}\underbrace{\frac{\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_j\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}}_{\gamma(z_{nk})}\boldsymbol{\Sigma}_k(\mathbf{x}_n-\boldsymbol{\mu}_k)
\tag{9.16}
$$

其中使用了高斯分布的形式（2.43）。注意，式（9.13）给出的后验概率，也就是责任度，自然地出现在右侧。乘以 $\boldsymbol{\Sigma}_k^{-1}$，这里假设它非奇异，再整理可得

$$
\boldsymbol{\mu}_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf{x}_n
\tag{9.17}
$$

其中我们定义了

$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk}).
\tag{9.18}
$$

<!-- pdf-page: 456 -->

我们可以把 $N_k$ 解释为分配给簇 $k$ 的有效数据点数。请仔细注意这个解的形式。第 $k$ 个高斯分量的均值 $\boldsymbol{\mu}_k$，是对数据集中的所有点取加权平均得到的；数据点 $\mathbf{x}_n$ 的权重，就是分量 $k$ 负责生成 $\mathbf{x}_n$ 的后验概率 $\gamma(z_{nk})$。

如果把 $\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})$ 对 $\boldsymbol{\Sigma}_k$ 的导数设为零，并沿用类似的推理，利用单个高斯分布协方差矩阵的最大似然解，就得到<span class="margin-reference">第 2.3.4 节</span>

$$
\boldsymbol{\Sigma}_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})(\mathbf{x}_n-\boldsymbol{\mu}_k)(\mathbf{x}_n-\boldsymbol{\mu}_k)^{\mathrm{T}}
\tag{9.19}
$$

它与用单个高斯分布拟合数据集时的相应结果形式相同，只是每个数据点同样要用对应的后验概率加权，分母则是对应分量的有效数据点数。

最后，我们对混合系数 $\pi_k$ 最大化 $\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})$。这里必须考虑约束（9.9），即各混合系数之和为一。为此，可以使用拉格朗日乘子并最大化以下量：<span class="margin-reference">附录 E</span>

$$
\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})+\lambda\left(\sum_{k=1}^{K}\pi_k-1\right)
\tag{9.20}
$$

从而得到

$$
0=\sum_{n=1}^{N}\frac{\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_j\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}+\lambda
\tag{9.21}
$$

这里又出现了责任度。如果将两边乘以 $\pi_k$，再对 $k$ 求和，并利用约束（9.9），就会得到 $\lambda=-N$。用它消去 $\lambda$ 并整理可得

$$
\pi_k=\frac{N_k}{N}
\tag{9.22}
$$

因此，第 $k$ 个分量的混合系数，等于该分量在解释各数据点时承担的平均责任度。

需要强调，结果（9.17）、（9.19）和（9.22）并不构成混合模型参数的闭式解，因为责任度 $\gamma(z_{nk})$ 通过式（9.13）以复杂的方式依赖这些参数。不过，这些结果提示了一种求解最大似然问题的简单迭代方案。我们将看到，它恰好是 EM 算法在高斯混合模型这一特例下的实例。我们先为均值、协方差和混合系数选择初始值，然后交替进行以下两种更新，分别称为 E 步

<!-- pdf-page: 457 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-8.png" alt="EM 算法拟合两个高斯分量的六幅图，展示初始状态及一、二、五、二十轮迭代"><figcaption>图 9.8：使用 Old Faithful 数据集说明 EM 算法；图 9.1 说明 K 均值算法时使用的也是这一数据集。详见正文。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
和 M 步，原因很快就会清楚。在期望步，也就是 E 步中，我们用当前参数值计算式（9.13）给出的后验概率，即责任度。然后在最大化步，也就是 M 步中，利用这些概率和结果（9.17）、（9.19）、（9.22），重新估计均值、协方差与混合系数。注意，这样做时，要先用式（9.17）计算新的均值，再把这些新值代入式（9.19）求协方差，这与单个高斯分布的相应结果一致。我们将证明，每次依次进行 E 步与 M 步所得到的参数更新，都保证使对数似然函数增大。<span class="margin-reference">第 9.4 节</span>在实践中，当对数似然函数的变化，或者参数的变化，小于某个阈值时，就认为算法已经收敛。图 9.8 展示了将两个高斯分量的混合模型及其 EM 算法应用于重新缩放后的 Old Faithful 数据集的情况。这里使用两个高斯分量，其中心的初始值与图 9.1 中 K 均值算法的初始值相同，精度矩阵则初始化为与单位矩阵成比例。图（a）用绿色表示数据点，并同时展示混合模型的初始配置，其中两个

<!-- pdf-page: 458 -->
<!-- join-previous-paragraph-across-figures -->
高斯分量的一个标准差等高线分别用蓝色和红色圆圈表示。图（b）给出最初 E 步的结果。绘制每个数据点时，蓝色墨色的比例等于该点由蓝色分量生成的后验概率，而相应的红色墨色比例由该点来自红色分量的后验概率给出。因此，对两个簇都具有较大归属概率的点会呈紫色。第一次 M 步之后的情况如图（c）所示：蓝色高斯分量的均值移动到了数据集的加权均值，权重为每个数据点属于蓝色簇的概率；换言之，它移动到了蓝色墨色的重心。类似地，蓝色高斯分量的协方差被设为蓝色墨色的协方差。红色分量也有相应的结果。图（d）、（e）、（f）分别展示完成 $2$、$5$、$20$ 轮完整 EM 循环之后的结果。在图（f）中，算法已接近收敛。

注意，与 K 均值算法相比，EM 算法需要更多次迭代才能达到近似收敛，而且每轮循环所需的计算量也显著更大。因此，通常先运行 K 均值算法，为高斯混合模型寻找合适的初始值，再用 EM 调整模型。可以方便地把协方差矩阵初始化为 K 均值算法得到的各簇的样本协方差，并把混合系数设为分配给各簇的数据点所占的比例。与通过梯度方法最大化对数似然时一样，必须采取措施避免似然函数的奇异性，即某个高斯分量塌缩到特定数据点的情况。还应强调，对数似然函数通常具有多个局部极大值，EM 并不保证找到其中最大的那个。由于高斯混合的 EM 算法十分重要，我们在下面将其归纳列出。

<aside class="procedure">
<h3>高斯混合的 EM 算法</h3>
<p>给定一个高斯混合模型，目标是对模型参数最大化似然函数；这些参数包括各分量的均值、协方差和混合系数。</p>
<ol>
<li>初始化均值 $\boldsymbol{\mu}_k$、协方差 $\boldsymbol{\Sigma}_k$ 和混合系数 $\pi_k$，并计算对数似然的初始值。</li>
<li><strong>E 步。</strong>用当前参数值计算责任度：</li>
</ol>
<p>$$
\gamma(z_{nk})=\frac{\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\displaystyle\sum_{j=1}^{K}\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}.
\tag{9.23}
$$</p>
</aside>

<!-- pdf-page: 459 -->
<!-- join-previous-procedure -->

<aside class="procedure">
<ol start="3">
<li><strong>M 步。</strong>使用当前责任度重新估计参数：</li>
</ol>
<p>$$
\boldsymbol{\mu}_k^{\mathrm{new}}=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf{x}_n
\tag{9.24}
$$</p>
<p>$$
\boldsymbol{\Sigma}_k^{\mathrm{new}}=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})(\mathbf{x}_n-\boldsymbol{\mu}_k^{\mathrm{new}})(\mathbf{x}_n-\boldsymbol{\mu}_k^{\mathrm{new}})^{\mathrm{T}}
\tag{9.25}
$$</p>
<p>$$
\pi_k^{\mathrm{new}}=\frac{N_k}{N}
\tag{9.26}
$$</p>
<p>其中</p>
<p>$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk}).
\tag{9.27}
$$</p>
<ol start="4">
<li>计算对数似然：</li>
</ol>
<p>$$
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}
\tag{9.28}
$$</p>
<p>并检查参数或对数似然是否收敛。如果不满足收敛准则，返回第2步。</p>
</aside>

## 9.3 从另一角度看 EM

本节从一个补充的角度介绍 EM 算法，着重认识潜变量所发挥的关键作用。我们先在抽象的情形下讨论这一方法，再以高斯混合为例加以说明。

EM 算法的目标，是为含潜变量的模型寻找最大似然解。我们用 $\mathbf{X}$ 表示全部观测数据的集合，其中第 $n$ 行表示 $\mathbf{x}_n^{\mathrm{T}}$；类似地，用 $\mathbf{Z}$ 表示全部潜变量的集合，其对应的行为 $\mathbf{z}_n^{\mathrm{T}}$。全部模型参数的集合记为 $\boldsymbol{\theta}$，于是对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\theta})=\ln\left\{\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})\right\}.
\tag{9.29}
$$

注意，只需把对 $\mathbf{Z}$ 的求和替换成积分，我们的讨论就同样适用于连续潜变量。

关键的一点是，对潜变量的求和位于对数内部。即使联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 属于指数

<!-- pdf-page: 460 -->
<!-- join-previous-paragraph -->
族，由于这次求和，边缘分布 $p(\mathbf{X}\mid\boldsymbol{\theta})$ 通常也不再属于指数族。求和的存在使对数不能直接作用于联合分布，从而导致最大似然解的表达式变得复杂。

现在假设，对于 $\mathbf{X}$ 中的每个观测，我们都知道相应潜变量 $\mathbf{Z}$ 的取值。我们将 $\{\mathbf{X},\mathbf{Z}\}$ 称为完整数据集（complete data set），而把实际观测到的数据 $\mathbf{X}$ 称为不完整数据，如图 9.5 所示。完整数据集的似然函数直接写成 $\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 的形式，我们假设最大化这个完整数据对数似然函数是容易的。

然而在实践中，我们得到的并非完整数据集 $\{\mathbf{X},\mathbf{Z}\}$，而只是其中的不完整数据 $\mathbf{X}$。对于 $\mathbf{Z}$ 中潜变量的取值，我们掌握的信息仅由后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$ 给出。由于无法使用完整数据对数似然，我们转而考虑它在潜变量后验分布下的期望值；正如后面将看到的，这对应于 EM 算法的 E 步。随后的 M 步则最大化这个期望。如果将当前参数估计记为 $\boldsymbol{\theta}^{\mathrm{old}}$，那么接连执行的一对 E 步和 M 步，会得到更新后的估计 $\boldsymbol{\theta}^{\mathrm{new}}$。算法通过为参数选择某个初始值 $\boldsymbol{\theta}_0$ 来初始化。使用期望似乎有些随意。不过，在第 9.4 节更深入地讨论 EM 时，我们将看到作出这一选择的原因。

在 E 步中，我们使用当前参数值 $\boldsymbol{\theta}^{\mathrm{old}}$ 求出潜变量的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$。然后利用这个后验分布，计算在一般参数值 $\boldsymbol{\theta}$ 下的完整数据对数似然的期望。将此期望记为 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$，则有

$$
\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{9.30}
$$

在 M 步中，我们通过最大化这个函数，确定更新后的参数估计 $\boldsymbol{\theta}^{\mathrm{new}}$：

$$
\boldsymbol{\theta}^{\mathrm{new}}=\arg\max_{\boldsymbol{\theta}}\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}}).
\tag{9.31}
$$

注意，在 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 的定义中，对数直接作用于联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$。因此，按照前面的假设，相应的 M 步最大化是可以处理的。

下面归纳一般的 EM 算法。我们稍后将证明，它具有如下性质：每一轮 EM 都会使不完整数据对数似然增大，除非它已经位于某个局部极大值处。<span class="margin-reference">第 9.4 节</span>

<aside class="procedure">
<h3>通用 EM 算法</h3>
<p>给定观测变量 $\mathbf{X}$ 和潜变量 $\mathbf{Z}$ 上、由参数 $\boldsymbol{\theta}$ 控制的联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$，目标是对 $\boldsymbol{\theta}$ 最大化似然函数 $p(\mathbf{X}\mid\boldsymbol{\theta})$。</p>
<ol>
<li>为参数 $\boldsymbol{\theta}^{\mathrm{old}}$ 选择一个初始设置。</li>
</ol>
</aside>

<!-- pdf-page: 461 -->
<!-- join-previous-procedure -->

<aside class="procedure">
<ol start="2">
<li><strong>E 步。</strong>计算 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$。</li>
<li><strong>M 步。</strong>按下式计算 $\boldsymbol{\theta}^{\mathrm{new}}$：</li>
</ol>
<p>$$
\boldsymbol{\theta}^{\mathrm{new}}=\arg\max_{\boldsymbol{\theta}}\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})
\tag{9.32}
$$</p>
<p>其中</p>
<p>$$
\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{9.33}
$$</p>
<ol start="4">
<li>检查对数似然或参数值是否收敛。如果尚未满足收敛准则，则令</li>
</ol>
<p>$$
\boldsymbol{\theta}^{\mathrm{old}}\leftarrow\boldsymbol{\theta}^{\mathrm{new}}
\tag{9.34}
$$</p>
<p>并返回第2步。</p>
</aside>

对于在参数上定义了先验 $p(\boldsymbol{\theta})$ 的模型，EM 算法也可以用于寻找 MAP（最大后验）解。<span class="margin-reference">习题 9.4</span>此时，E 步与最大似然情形相同，而 M 步需要最大化的量变为 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})+\ln p(\boldsymbol{\theta})$。适当选择先验，可以消除图 9.7 所示的那类奇异性。

这里，我们考虑了在存在离散潜变量时，用 EM 算法最大化似然函数。不过，当未观测变量对应于数据集中的缺失值时，也可以应用 EM。观测值的分布可以通过所有变量的联合分布，对缺失变量进行边缘化而得到。然后，就能用 EM 最大化相应的似然函数。我们将在图 12.11 中结合主成分分析，展示这一技术的应用示例。当数据值随机缺失（missing at random）时，这一过程是有效的；所谓随机缺失，是指导致数据缺失的机制不依赖于未观测值。在许多情况下，这一条件并不成立。例如，只要所测量的量超过某个阈值，传感器就无法返回数值。

### 9.3.1 再论高斯混合

现在，我们把这种从潜变量角度理解 EM 的方式，应用于高斯混合模型这一具体情形。回顾一下，我们的目标是最大化使用观测数据集 $\mathbf{X}$ 计算的对数似然函数（9.14）。我们已经看到，由于对 $k$ 的求和出现在对数内部，这比单个高斯分布的情形更难。现在假设，除了观测数据集 $\mathbf{X}$，我们还知道相应离散变量 $\mathbf{Z}$ 的值。回顾图 9.5（a），它展示了一个“完整”数据集，也就是带有标签、指出每个数据点由哪个分量生成的数据集；图 9.5（b）则展示了对应的“不完整”数据集。完整数据的图模型如图 9.9 所示。

<!-- pdf-page: 462 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/a-fig-9-9.png" alt="完整数据的高斯混合图模型，x_n 和 z_n 都表示为已观测节点"><figcaption>图 9.9：这幅图与图 9.6 相同，只是现在假设除了数据变量 $\mathbf{x}_n$ 之外，离散变量 $\mathbf{z}_n$ 也已被观测。</figcaption></figure>

现在考虑如何最大化完整数据集 $\{\mathbf{X},\mathbf{Z}\}$ 的似然。根据式（9.10）和式（9.11），这一似然函数为

$$
p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})=\prod_{n=1}^{N}\prod_{k=1}^{K}\pi_k^{z_{nk}}\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)^{z_{nk}}
\tag{9.35}
$$

其中 $z_{nk}$ 表示 $\mathbf{z}_n$ 的第 $k$ 个分量。取对数，得到

$$
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})=\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\left\{\ln\pi_k+\ln\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{9.36}
$$

与不完整数据的对数似然函数（9.14）比较，可以看到，对 $k$ 的求和与取对数的次序已经交换。现在，对数直接作用于高斯分布，而高斯分布本身属于指数族。因此，最大似然问题的解变得简单得多，这并不意外；下面就来说明。先考虑对均值和协方差的最大化。由于 $\mathbf{z}_n$ 是一个 $K$ 维向量，只有一个元素为 $1$，其余元素全部为 $0$，完整数据对数似然函数就只是 $K$ 个独立部分之和，每个混合分量对应其中一部分。因此，对某个均值或协方差进行最大化时，情况与单个高斯分布完全相同，只不过涉及的数据仅限于“分配”给该分量的那些点。对于混合系数的最大化，我们注意到，由于求和约束（9.9），不同 $k$ 对应的混合系数是相互耦合的。与前面一样，可以用拉格朗日乘子来施加这一约束，得到

$$
\pi_k=\frac{1}{N}\sum_{n=1}^{N}z_{nk}
\tag{9.37}
$$

因此，混合系数等于分配给相应分量的数据点所占的比例。

由此可见，完整数据对数似然函数很容易以闭式形式最大化。不过在实践中，我们并不知道潜变量的值。因此，正如前面讨论的，我们考虑完整数据对数似然在潜变量后验分布下的期望。

<!-- pdf-page: 463 -->

将（9.10）、（9.11）与贝叶斯定理结合，可知这个后验分布具有如下形式：

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})\propto\prod_{n=1}^{N}\prod_{k=1}^{K}\left[\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right]^{z_{nk}}.
\tag{9.38}
$$

因此，它可以按 $n$ 分解，于是在后验分布下，各个 $\{\mathbf{z}_n\}$ 相互独立。查看图 9.6 的有向图，并使用 d 分离判据，就很容易验证这一点（习题 9.5；8.2 节）。指示变量 $z_{nk}$ 在这个后验分布下的期望为

$$
\begin{aligned}
\mathbb{E}[z_{nk}]&=\frac{\sum_{z_{nk}}z_{nk}\left[\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right]^{z_{nk}}}{\sum_{z_{nj}}\left[\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)\right]^{z_{nj}}}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_{j=1}^{K}\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}=\gamma(z_{nk})
\end{aligned}
\tag{9.39}
$$

这正是分量 $k$ 对数据点 $\mathbf{x}_n$ 的责任度。因此，完整数据对数似然函数的期望为

$$
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})]=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\left\{\ln\pi_k+\ln\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{9.40}
$$

现在可以按以下步骤进行。首先为参数 $\boldsymbol{\mu}^{\mathrm{old}}$、$\boldsymbol{\Sigma}^{\mathrm{old}}$ 和 $\boldsymbol{\pi}^{\mathrm{old}}$ 选择初始值，用它们计算责任度，即 E 步。随后固定责任度，关于 $\boldsymbol{\mu}_k$、$\boldsymbol{\Sigma}_k$ 和 $\pi_k$ 最大化（9.40），即 M 步。这与前面一样，得到由（9.17）、（9.19）和（9.22）给出的 $\boldsymbol{\mu}^{\mathrm{new}}$、$\boldsymbol{\Sigma}^{\mathrm{new}}$ 和 $\boldsymbol{\pi}^{\mathrm{new}}$ 的闭式解（习题 9.8）。这正是此前推导的高斯混合 EM 算法。在 9.4 节给出 EM 算法收敛性的证明时，我们将更深入地理解完整数据对数似然期望的作用。

### 9.3.2 与 K 均值的关系

比较 K 均值算法与高斯混合的 EM 算法，可以看到两者非常相似。K 均值算法将数据点*硬分配*给各个簇，每个数据点唯一地对应一个簇；EM 算法则根据后验概率进行*软分配*。事实上，可以按以下方式，把 K 均值算法推导为高斯混合 EM 算法的一个特定极限。

考虑一个高斯混合模型，各混合分量的协方差矩阵为 $\epsilon\mathbf{I}$，其中 $\epsilon$ 是

<!-- pdf-page: 464 -->

<!-- join-previous-paragraph -->
所有分量共享的方差参数，$\mathbf{I}$ 是单位矩阵，因此

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)=\frac{1}{(2\pi\epsilon)^{1/2}}\exp\left\{-\frac{1}{2\epsilon}\|\mathbf{x}-\boldsymbol{\mu}_k\|^2\right\}.
\tag{9.41}
$$

现在考虑由 $K$ 个这种高斯分布组成的混合模型的 EM 算法，将 $\epsilon$ 视为固定常数，而不是需要重估的参数。由（9.13），对于某个数据点 $\mathbf{x}_n$，后验概率，即责任度，为

$$
\gamma(z_{nk})=\frac{\pi_k\exp\{-\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2/2\epsilon\}}{\sum_j\pi_j\exp\{-\|\mathbf{x}_n-\boldsymbol{\mu}_j\|^2/2\epsilon\}}.
\tag{9.42}
$$

考虑极限 $\epsilon\to0$。在分母中，使 $\|\mathbf{x}_n-\boldsymbol{\mu}_j\|^2$ 最小的那一项趋于零的速度最慢。因此，对于数据点 $\mathbf{x}_n$，除第 $j$ 项的责任度 $\gamma(z_{nj})$ 趋于 $1$ 以外，其余责任度 $\gamma(z_{nk})$ 都趋于零。注意，只要没有任何 $\pi_k$ 等于零，这个结论就与 $\pi_k$ 的取值无关。因此，在这一极限下，就像 K 均值算法一样，得到数据点到簇的硬分配，即 $\gamma(z_{nk})\to r_{nk}$，其中 $r_{nk}$ 由（9.2）定义。每个数据点由此被分配给均值与其最近的簇。

此时，（9.17）给出的 $\boldsymbol{\mu}_k$ 的 EM 重估方程，简化为 K 均值的结果（9.4）。注意，混合系数的重估公式（9.22）只是把 $\pi_k$ 重新设为分配到簇 $k$ 的数据点所占的比例，不过这些参数此时已不再对算法起实际作用。

最后，在极限 $\epsilon\to0$ 下，由（9.40）给出的完整数据对数似然的期望变为（习题 9.11）

$$
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})]\to-\frac{1}{2}\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2+\mathrm{const}.
\tag{9.43}
$$

因此，在这一极限下，最大化完整数据对数似然的期望，等价于最小化 K 均值算法中由（9.1）给出的失真度量 $J$。

注意，K 均值算法只估计簇均值，并不估计簇的协方差。Sung and Poggio（1994）研究过一种具有一般协方差矩阵的高斯混合模型的硬分配版本，称为*椭圆 K 均值算法*（elliptical K-means algorithm）。

### 9.3.3 伯努利分布的混合

本章到目前为止，着重讨论了用高斯混合描述的连续变量分布。作为混合建模的另一个例子，也为了在不同背景下说明 EM 算法，现在讨论用伯努利分布描述的离散二元变量的混合。这一模型也称为*潜在类别分析*（latent class analysis）（Lazarsfeld and Henry, 1968; McLachlan and Peel, 2000）。除本身具有实际价值外，对伯努利混合的讨论也将为研究离散变量的隐马尔可夫模型打下基础（13.2 节）。

<!-- pdf-page: 465 -->

考虑 $D$ 个二元变量 $x_i$，其中 $i=1,\ldots,D$，每个变量都服从参数为 $\mu_i$ 的伯努利分布，因此

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{i=1}^{D}\mu_i^{x_i}(1-\mu_i)^{(1-x_i)}
\tag{9.44}
$$

其中 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathrm T}$，$\boldsymbol{\mu}=(\mu_1,\ldots,\mu_D)^{\mathrm T}$。可以看到，给定 $\boldsymbol{\mu}$ 后，各个变量 $x_i$ 相互独立。容易看出，这个分布的均值和协方差为

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}
\tag{9.45}
$$

$$
\operatorname{cov}[\mathbf{x}]=\operatorname{diag}\{\mu_i(1-\mu_i)\}.
\tag{9.46}
$$

现在考虑这些分布的有限混合：

$$
p(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\pi})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid\boldsymbol{\mu}_k)
\tag{9.47}
$$

其中 $\boldsymbol{\mu}=\{\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K\}$、$\boldsymbol{\pi}=\{\pi_1,\ldots,\pi_K\}$，并且

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k)=\prod_{i=1}^{D}\mu_{ki}^{x_i}(1-\mu_{ki})^{(1-x_i)}.
\tag{9.48}
$$

这个混合分布的均值和协方差为（习题 9.12）

$$
\mathbb{E}[\mathbf{x}]=\sum_{k=1}^{K}\pi_k\boldsymbol{\mu}_k
\tag{9.49}
$$

$$
\operatorname{cov}[\mathbf{x}]=\sum_{k=1}^{K}\pi_k\left\{\boldsymbol{\Sigma}_k+\boldsymbol{\mu}_k\boldsymbol{\mu}_k^{\mathrm T}\right\}-\mathbb{E}[\mathbf{x}]\mathbb{E}[\mathbf{x}]^{\mathrm T}
\tag{9.50}
$$

其中 $\boldsymbol{\Sigma}_k=\operatorname{diag}\{\mu_{ki}(1-\mu_{ki})\}$。由于协方差矩阵 $\operatorname{cov}[\mathbf{x}]$ 不再是对角矩阵，这个混合分布能够描述变量之间的相关性，而单个伯努利分布不能。

若给定数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，这个模型的对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\pi})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\right\}.
\tag{9.51}
$$

这里又出现了对数内部的求和，因此最大似然解不再具有闭式形式。

现在推导最大化伯努利混合分布似然函数的 EM 算法。为此，首先显式引入一个潜

<!-- pdf-page: 466 -->

<!-- join-previous-paragraph -->
变量 $\mathbf{z}$，使其与 $\mathbf{x}$ 的每个实例关联。与高斯混合一样，$\mathbf{z}=(z_1,\ldots,z_K)^{\mathrm T}$ 是一个 $K$ 维二元变量，只有一个分量为 $1$，其余分量全为 $0$。于是，给定潜变量后，$\mathbf{x}$ 的条件分布可以写为

$$
p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})=\prod_{k=1}^{K}p(\mathbf{x}\mid\boldsymbol{\mu}_k)^{z_k}
\tag{9.52}
$$

而潜变量的先验分布与高斯混合模型相同，因此

$$
p(\mathbf{z}\mid\boldsymbol{\pi})=\prod_{k=1}^{K}\pi_k^{z_k}.
\tag{9.53}
$$

将 $p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})$ 与 $p(\mathbf{z}\mid\boldsymbol{\pi})$ 相乘，再对 $\mathbf{z}$ 进行边缘化，就能重新得到（9.47）（习题 9.14）。

为了推导 EM 算法，先写出完整数据对数似然函数：

$$
\begin{aligned}
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\pi})={}&\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\Biggl\{\ln\pi_k\\
&+\sum_{i=1}^{D}\left[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\right]\Biggr\}
\end{aligned}
\tag{9.54}
$$

其中 $\mathbf{X}=\{\mathbf{x}_n\}$，$\mathbf{Z}=\{\mathbf{z}_n\}$。接着，关于潜变量的后验分布，对完整数据对数似然取期望，得到

$$
\begin{aligned}
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\pi})]={}&\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\Biggl\{\ln\pi_k\\
&+\sum_{i=1}^{D}\left[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\right]\Biggr\}
\end{aligned}
\tag{9.55}
$$

其中，$\gamma(z_{nk})=\mathbb{E}[z_{nk}]$ 是给定数据点 $\mathbf{x}_n$ 后分量 $k$ 的后验概率，即责任度。在 E 步中，利用贝叶斯定理计算这些责任度，其形式为

$$
\begin{aligned}
\gamma(z_{nk})=\mathbb{E}[z_{nk}]&=\frac{\sum_{z_{nk}}z_{nk}\left[\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\right]^{z_{nk}}}{\sum_{z_{nj}}\left[\pi_j p(\mathbf{x}_n\mid\boldsymbol{\mu}_j)\right]^{z_{nj}}}\\
&=\frac{\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)}{\sum_{j=1}^{K}\pi_j p(\mathbf{x}_n\mid\boldsymbol{\mu}_j)}.
\end{aligned}
\tag{9.56}
$$

<!-- pdf-page: 467 -->

考察（9.55）中关于 $n$ 的求和，可以看到，责任度只通过以下两项起作用：

$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk})
\tag{9.57}
$$

$$
\overline{\mathbf{x}}_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf{x}_n
\tag{9.58}
$$

其中 $N_k$ 是与分量 $k$ 关联的有效数据点数。在 M 步中，关于参数 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\pi}$ 最大化完整数据对数似然的期望。将（9.55）关于 $\boldsymbol{\mu}_k$ 的导数设为零，并整理各项，得到（习题 9.15）

$$
\boldsymbol{\mu}_k=\overline{\mathbf{x}}_k.
\tag{9.59}
$$

这使分量 $k$ 的均值等于数据的加权均值，权重为该分量对各数据点的责任度。要关于 $\pi_k$ 最大化，需要引入拉格朗日乘子来实施约束 $\sum_k\pi_k=1$。按照与高斯混合类似的步骤，得到（习题 9.16）

$$
\pi_k=\frac{N_k}{N}
\tag{9.60}
$$

这一结果在直观上很合理：分量 $k$ 的混合系数，就是数据集中由该分量解释的点所占的有效比例。

注意，与高斯混合不同，这里不存在似然函数趋于无穷大的奇异点。这可以从似然函数有上界看出，因为 $0\leqslant p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\leqslant1$（习题 9.17）。虽然存在使似然函数趋于零的奇异点，但只要不把 EM 初始化在病态的起点上，算法就不会到达这些点，因为 EM 算法始终提高似然函数的值，直到找到一个局部最大值（9.4 节）。图 9.10 用手写数字建模展示了伯努利混合模型。这里将数字图像转换为二元向量：把所有大于 $0.5$ 的元素设为 $1$，其余元素设为 $0$。现在对由数字“2”“3”和“4”组成的 $N=600$ 个数字样本，运行 10 轮 EM 迭代，用 $K=3$ 个伯努利分布的混合进行拟合。混合系数初始化为 $\pi_k=1/K$；参数 $\mu_{kj}$ 则在区间 $(0.25,0.75)$ 内均匀随机选取，再归一化以满足约束 $\sum_j\mu_{kj}=1$。可以看到，3 个伯努利分布的混合能够找出数据集中与不同数字对应的三个簇。

伯努利分布参数的共轭先验是 Beta 分布；我们已经看到，Beta 先验等价于引入

<!-- pdf-page: 468 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-10.png" alt="二值数字样本与伯努利混合三个分量及单个伯努利分布的均值图像"><figcaption>图 9.10：伯努利混合模型示例。上排为数字数据集中的样本，像素值已用 $0.5$ 的阈值从灰度转换为二值。下排前三幅图显示混合模型中三个分量各自的参数 $\mu_{ki}$。作为比较，我们也再次使用最大似然，用单个多元伯努利分布拟合同一数据集。这相当于直接对每个像素的计数取平均，结果如最右下方的图像所示。</figcaption><p class="figure-translation">上排五幅图为二值样本；下排左侧三幅图为混合分量的均值，最右侧图为单个多元伯努利分布的均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
额外的 $\mathbf{x}$ 的有效观测（2.1.1 节）。同样，可以为伯努利混合模型引入先验，并用 EM 最大化后验概率分布（习题 9.18）。

利用离散分布（2.26），很容易把伯努利混合的分析扩展到具有 $M>2$ 个状态的多项二元变量（multinomial binary variables）的情况（习题 9.19）。如果需要，同样可以为模型参数引入狄利克雷先验。

### 9.3.4 用于贝叶斯线性回归的 EM

作为 EM 应用的第三个例子，回到贝叶斯线性回归的证据近似。在 3.5.2 节中，我们先计算证据，再令所得表达式的导数为零，得到了超参数 $\alpha$ 和 $\beta$ 的重估方程。现在考虑另一种基于 EM 算法求 $\alpha$ 和 $\beta$ 的方法。回顾一下，目标是关于 $\alpha$ 和 $\beta$ 最大化（3.77）给出的证据函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$。由于参数向量 $\mathbf{w}$ 被边缘化消去了，可以把它视为潜变量，从而用 EM 优化这个边缘似然函数。在 E 步中，给定当前参数 $\alpha$ 和 $\beta$，计算 $\mathbf{w}$ 的后验分布，再利用它求完整数据对数似然的期望。在 M 步中，关于 $\alpha$ 和 $\beta$ 最大化这个量。我们已经推导过 $\mathbf{w}$ 的后验分布，它由（3.49）给出。完整数据对数似然函数于是为

$$
\ln p(\boldsymbol{\mathsf{t}},\mathbf{w}\mid\alpha,\beta)=\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)+\ln p(\mathbf{w}\mid\alpha)
\tag{9.61}
$$

<!-- pdf-page: 469 -->

其中，似然 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)$ 和先验 $p(\mathbf{w}\mid\alpha)$ 分别由（3.10）和（3.52）给出，$y(\mathbf{x},\mathbf{w})$ 由（3.3）给出。关于 $\mathbf{w}$ 的后验分布取期望，得到

$$
\begin{aligned}
\mathbb{E}[\ln p(\boldsymbol{\mathsf{t}},\mathbf{w}\mid\alpha,\beta)]={}&\frac{M}{2}\ln\left(\frac{\alpha}{2\pi}\right)-\frac{\alpha}{2}\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]+\frac{N}{2}\ln\left(\frac{\beta}{2\pi}\right)\\
&-\frac{\beta}{2}\sum_{n=1}^{N}\mathbb{E}\left[(t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n)^2\right].
\end{aligned}
\tag{9.62}
$$

将关于 $\alpha$ 的导数设为零，得到 M 步的重估方程（习题 9.20）

$$
\alpha=\frac{M}{\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]}=\frac{M}{\mathbf{m}_N^{\mathrm T}\mathbf{m}_N+\operatorname{Tr}(\mathbf{S}_N)}.
\tag{9.63}
$$

对于 $\beta$，也有类似结果（习题 9.21）。

注意，这个重估方程与直接计算证据函数得到的相应结果（3.92），形式略有不同。不过，两者都涉及一个 $M\times M$ 矩阵的计算及求逆，或特征分解，因此每次迭代的计算成本相近。

当然，这两种确定 $\alpha$ 的方法应当收敛到相同的结果，前提是它们找到证据函数的同一个局部最大值。要验证这一点，先注意量 $\gamma$ 的定义为

$$
\gamma=M-\alpha\sum_{i=1}^{M}\frac{1}{\lambda_i+\alpha}=M-\alpha\operatorname{Tr}(\mathbf{S}_N).
\tag{9.64}
$$

在证据函数的驻点，重估方程（3.92）会自洽地成立，因此可以代入 $\gamma$，得到

$$
\alpha\mathbf{m}_N^{\mathrm T}\mathbf{m}_N=\gamma=M-\alpha\operatorname{Tr}(\mathbf{S}_N)
\tag{9.65}
$$

解出 $\alpha$，就得到（9.63），恰好就是 EM 重估方程。

最后一个例子考虑一个密切相关的模型，即 7.2.1 节讨论的回归相关向量机。那里通过直接最大化边缘似然，推导了超参数 $\alpha$ 和 $\beta$ 的重估方程。这里考虑另一种方法，把权重向量 $\mathbf{w}$ 视为潜变量，应用 EM 算法。E 步求权重的后验分布，它由（7.81）给出。M 步则最大化完整数据对数似然的期望，其定义为

$$
\mathbb{E}_{\mathbf{w}}\left[\ln\left\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\alpha})\right\}\right]
\tag{9.66}
$$

其中，期望是关于使用“旧”参数值计算出的后验分布取的。为求新参数值，关于 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化，得到（习题 9.22）

<!-- pdf-page: 470 -->

$$
\alpha_i^{\mathrm{new}}=\frac{1}{m_i^2+\Sigma_{ii}}
\tag{9.67}
$$

$$
(\beta^{\mathrm{new}})^{-1}=\frac{\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}_N\|^2+\beta^{-1}\sum_i\gamma_i}{N}.
\tag{9.68}
$$

这些重估方程与直接最大化得到的方程在形式上等价（习题 9.23）。

## 9.4 一般的 EM 算法

*期望最大化算法*（expectation maximization algorithm），简称 EM 算法，是为含潜变量的概率模型寻找最大似然解的一般方法（Dempster et al., 1977; McLachlan and Krishnan, 1997）。这里将对 EM 算法作一般性的讨论，并在此过程中证明：9.2 节和 9.3 节中为高斯混合启发式推导的 EM 算法，确实能够最大化似然函数（Csiszàr and Tusnàdy, 1984; Hathaway, 1986; Neal and Hinton, 1999）。这里的讨论也将为推导变分推断框架打下基础（10.1 节）。

考虑一个概率模型，用 $\mathbf{X}$ 统称所有观测变量，用 $\mathbf{Z}$ 统称所有隐藏变量。联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 由一组记为 $\boldsymbol{\theta}$ 的参数控制。目标是最大化如下似然函数：

$$
p(\mathbf{X}\mid\boldsymbol{\theta})=\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{9.69}
$$

这里假设 $\mathbf{Z}$ 是离散的；如果 $\mathbf{Z}$ 包含连续变量，或同时包含离散变量和连续变量，只需在相应位置将求和替换为积分，讨论完全相同。

假设直接优化 $p(\mathbf{X}\mid\boldsymbol{\theta})$ 很困难，而优化完整数据似然函数 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 则容易得多。接着，在潜变量上引入一个分布 $q(\mathbf{Z})$。可以看到，无论如何选择 $q(\mathbf{Z})$，以下分解都成立：

$$
\ln p(\mathbf{X}\mid\boldsymbol{\theta})=\mathcal{L}(q,\boldsymbol{\theta})+\operatorname{KL}(q\|p)
\tag{9.70}
$$

其中定义了

$$
\mathcal{L}(q,\boldsymbol{\theta})=\sum_{\mathbf{Z}}q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}{q(\mathbf{Z})}\right\}
\tag{9.71}
$$

$$
\operatorname{KL}(q\|p)=-\sum_{\mathbf{Z}}q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})}{q(\mathbf{Z})}\right\}.
\tag{9.72}
$$

注意，$\mathcal{L}(q,\boldsymbol{\theta})$ 是分布 $q(\mathbf{Z})$ 的泛函，关于泛函的讨论见附录 D；同时，它是参数 $\boldsymbol{\theta}$ 的函数。值得仔细研究

<!-- pdf-page: 471 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-11.png" alt="对数似然分解为下界与KL散度之和"><figcaption>图 9.11：（9.70）所给分解的示意图；该分解对分布 $q(\mathbf{Z})$ 的任意选择都成立。由于 Kullback–Leibler 散度满足 $\operatorname{KL}(q\|p)\geqslant0$，量 $\mathcal{L}(q,\boldsymbol{\theta})$ 是对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的一个下界。</figcaption><p class="figure-translation">红线表示对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$，蓝线表示下界 $\mathcal{L}(q,\boldsymbol{\theta})$，两者之差为 $\operatorname{KL}(q\|p)$。</p></figure>

<!-- join-previous-paragraph-across-figures -->
表达式（9.71）和（9.72）的形式，尤其要注意：它们的符号相反；此外，$\mathcal{L}(q,\boldsymbol{\theta})$ 包含 $\mathbf{X}$ 和 $\mathbf{Z}$ 的联合分布，而 $\operatorname{KL}(q\|p)$ 包含给定 $\mathbf{X}$ 后 $\mathbf{Z}$ 的条件分布。为验证分解（9.70），先利用概率的乘积规则，得到（习题 9.24）

$$
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})=\ln p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})+\ln p(\mathbf{X}\mid\boldsymbol{\theta})
\tag{9.73}
$$

将它代入 $\mathcal{L}(q,\boldsymbol{\theta})$ 的表达式，会得到两项。其中一项抵消 $\operatorname{KL}(q\|p)$；对于另一项，利用 $q(\mathbf{Z})$ 是求和为 $1$ 的归一化分布，就得到所需的对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。

由（9.72）可知，$\operatorname{KL}(q\|p)$ 是 $q(\mathbf{Z})$ 与后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$ 之间的 Kullback–Leibler 散度。回顾一下，Kullback–Leibler 散度满足 $\operatorname{KL}(q\|p)\geqslant0$，当且仅当 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$ 时取等号（1.6.1 节）。因此，由（9.70）可得 $\mathcal{L}(q,\boldsymbol{\theta})\leqslant\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。换言之，$\mathcal{L}(q,\boldsymbol{\theta})$ 是 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的下界。图 9.11 展示了分解（9.70）。

EM 算法是一种寻找最大似然解的两阶段迭代优化方法。可以用分解（9.70）定义 EM 算法，并证明它确实能够最大化对数似然。假设参数向量的当前值为 $\boldsymbol{\theta}^{\mathrm{old}}$。在 E 步中，保持 $\boldsymbol{\theta}^{\mathrm{old}}$ 不变，关于 $q(\mathbf{Z})$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$。这个最大化问题的解很容易看出：$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{old}})$ 的值不依赖于 $q(\mathbf{Z})$，因此，当 Kullback–Leibler 散度为零时，$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$ 达到最大值；也就是说，此时 $q(\mathbf{Z})$ 等于后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$。在这种情况下，下界等于对数似然，如图 9.12 所示。

在随后的 M 步中，保持分布 $q(\mathbf{Z})$ 不变，关于 $\boldsymbol{\theta}$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta})$，得到新值 $\boldsymbol{\theta}^{\mathrm{new}}$。这会使下界 $\mathcal{L}$ 增大，除非它已经达到最大值；相应的对数似然函数也必然增大。由于分布 $q$ 是由旧参数值而不是新参数值确定的，并且在 M 步中保持不变，它不会等于新的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{new}})$，因此 KL 散度不为零。所以，对数似然函数的增加量大于下界的增加量，正如

<!-- pdf-page: 472 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-12.png" alt="E步将分布q设为当前参数下的后验分布，使蓝色下界升到红色对数似然，KL散度降为零"><figcaption>图 9.12：EM 算法的 E 步示意图。将分布 $q$ 设为当前参数值 $\boldsymbol{\theta}^{\mathrm{old}}$ 下的后验分布，使下界上移到与对数似然函数相同的值，此时 KL 散度为零。</figcaption><p class="figure-translation">$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{old}})$：当前参数下的对数似然；$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$：下界；$\operatorname{KL}(q\|p)=0$：KL 散度为零。</p></figure>

<!-- join-previous-paragraph-across-figures -->
图 9.13 所示。将 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$ 代入（9.71），可知在 E 步之后，下界具有如下形式：

$$
\begin{aligned}
\mathcal{L}(q,\boldsymbol{\theta})
&=\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})-\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\\
&=\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})+\mathrm{const}
\end{aligned}
\tag{9.74}
$$

这里的常数就是分布 $q$ 的负熵，因此与 $\boldsymbol{\theta}$ 无关。由此可见，在 M 步中最大化的量是完整数据对数似然的期望，这与前面讨论高斯混合时的结论一致。注意，要优化的变量 $\boldsymbol{\theta}$ 只出现在对数内部。如果联合分布 $p(\mathbf{Z},\mathbf{X}\mid\boldsymbol{\theta})$ 属于指数族，或者是若干指数族分布的乘积，那么对数会消去指数运算，得到的 M 步通常会比最大化相应的不完整数据对数似然函数 $p(\mathbf{X}\mid\boldsymbol{\theta})$ 简单得多。

也可以在参数空间中观察 EM 算法的运行过程，如图 9.14 的示意图所示。图中的红色曲线表示我们希望最大化的（不完

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-13.png" alt="M步固定q并提升蓝色下界，对数似然的增加量至少与下界的增加量相同"><figcaption>图 9.13：EM 算法的 M 步示意图。保持分布 $q(\mathbf{Z})$ 不变，关于参数向量 $\boldsymbol{\theta}$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta})$，得到更新后的值 $\boldsymbol{\theta}^{\mathrm{new}}$。由于 KL 散度非负，对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的增加量至少与下界的增加量相同。</figcaption><p class="figure-translation">$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{new}})$：新参数下的对数似然；$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{new}})$：新参数下的下界；$\operatorname{KL}(q\|p)$：KL 散度。</p></figure>

<!-- pdf-page: 473 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-14.png" alt="EM参数空间示意图，红色对数似然曲线与蓝色和绿色下界分别在旧参数和新参数处相切"><figcaption>图 9.14：EM 算法交替执行两个操作：根据当前参数值计算对数似然的下界，再最大化这个下界以获得新的参数值。完整讨论见正文。</figcaption><p class="figure-translation">$\boldsymbol{\theta}^{\mathrm{old}}$、$\boldsymbol{\theta}^{\mathrm{new}}$：旧参数、新参数；$\ln p(\mathbf{X}\mid\boldsymbol{\theta})$：对数似然；$\mathcal{L}(q,\boldsymbol{\theta})$：下界。蓝色曲线是在旧参数处构造的下界，绿色曲线是在新参数处构造的下界。</p></figure>

<!-- join-previous-paragraph-across-figures -->
整数据）对数似然函数。首先选取初始参数值 $\boldsymbol{\theta}^{\mathrm{old}}$；在第一个 E 步中，计算潜变量的后验分布，由此得到下界 $\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\theta}^{(\mathrm{old})})$，它在 $\boldsymbol{\theta}^{(\mathrm{old})}$ 处的值等于对数似然，如蓝色曲线所示。注意，这个下界在 $\boldsymbol{\theta}^{(\mathrm{old})}$ 处与对数似然相切，因此两条曲线具有相同的梯度（习题 9.25）。这个下界是一个具有唯一最大值的凸函数（对于属于指数族的混合分量而言）。在 M 步中，最大化这个下界，得到参数值 $\boldsymbol{\theta}^{(\mathrm{new})}$，它所对应的对数似然值大于 $\boldsymbol{\theta}^{(\mathrm{old})}$ 对应的值。随后的 E 步再构造一个在 $\boldsymbol{\theta}^{(\mathrm{new})}$ 处相切的下界，如绿色曲线所示。

对于独立同分布数据集这一特殊情况，$\mathbf{X}$ 包含 $N$ 个数据点 $\{\mathbf{x}_n\}$，而 $\mathbf{Z}$ 包含 $N$ 个对应的潜变量 $\{\mathbf{z}_n\}$，其中 $n=1,\ldots,N$。由独立性假设，有 $p(\mathbf{X},\mathbf{Z})=\prod_n p(\mathbf{x}_n,\mathbf{z}_n)$；对 $\{\mathbf{z}_n\}$ 边缘化，得到 $p(\mathbf{X})=\prod_n p(\mathbf{x}_n)$。利用求和规则和乘积规则，可知在 E 步中计算的后验概率具有如下形式：

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})=\frac{p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}{\displaystyle\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}=\frac{\displaystyle\prod_{n=1}^{N}p(\mathbf{x}_n,\mathbf{z}_n\mid\boldsymbol{\theta})}{\displaystyle\sum_{\mathbf{Z}}\prod_{n=1}^{N}p(\mathbf{x}_n,\mathbf{z}_n\mid\boldsymbol{\theta})}=\prod_{n=1}^{N}p(\mathbf{z}_n\mid\mathbf{x}_n,\boldsymbol{\theta})
\tag{9.75}
$$

因此，后验分布也可以按 $n$ 分解。对于高斯混合模型，这只是说：各混合分量对某个数据点 $\mathbf{x}_n$ 的责任度，只依赖于 $\mathbf{x}_n$ 的值和混合分量的参数 $\boldsymbol{\theta}$，而不依赖于其他数据点的值。

我们已经看到，EM 算法的 E 步和 M 步都会增大对数似然函数的一个定义明确的下界，并且

<!-- pdf-page: 474 -->
<!-- join-previous-paragraph -->
一个完整的 EM 迭代周期会改变模型参数，使对数似然增大（除非它已经达到最大值，此时参数保持不变）。

对于引入了参数先验 $p(\boldsymbol{\theta})$ 的模型，我们也可以用 EM 算法最大化后验分布 $p(\boldsymbol{\theta}\mid\mathbf{X})$。为说明这一点，注意，作为 $\boldsymbol{\theta}$ 的函数，有 $p(\boldsymbol{\theta}\mid\mathbf{X})=p(\boldsymbol{\theta},\mathbf{X})/p(\mathbf{X})$，因此

$$
\ln p(\boldsymbol{\theta}\mid\mathbf{X})=\ln p(\boldsymbol{\theta},\mathbf{X})-\ln p(\mathbf{X}).
\tag{9.76}
$$

利用分解（9.70），得到

$$
\begin{aligned}
\ln p(\boldsymbol{\theta}\mid\mathbf{X})&=\mathcal{L}(q,\boldsymbol{\theta})+\operatorname{KL}(q\|p)+\ln p(\boldsymbol{\theta})-\ln p(\mathbf{X})\\
&\geqslant\mathcal{L}(q,\boldsymbol{\theta})+\ln p(\boldsymbol{\theta})-\ln p(\mathbf{X}).
\end{aligned}
\tag{9.77}
$$

其中 $\ln p(\mathbf{X})$ 是常数。我们可以再次交替关于 $q$ 和 $\boldsymbol{\theta}$ 优化右侧表达式。由于 $q$ 只出现在 $\mathcal{L}(q,\boldsymbol{\theta})$ 中，关于 $q$ 的优化会得到与标准 EM 算法相同的 E 步方程。先验项 $\ln p(\boldsymbol{\theta})$ 的引入会改变 M 步方程，通常只需对标准最大似然 M 步方程作少量修改。

EM 算法把可能很难求解的似然函数最大化问题分成 E 步和 M 步这两个阶段，每个阶段通常都更容易实现。不过，对于复杂模型，E 步或 M 步，甚至两者，仍有可能难以处理。这就引出了 EM 算法的以下两种扩展。

*广义 EM*（generalized EM，GEM）算法处理 M 步难以求解的问题。它的目标不是关于 $\boldsymbol{\theta}$ 最大化 $\mathcal{L}(q,\boldsymbol{\theta})$，而是改变参数，使这个函数的值增大。同样，由于 $\mathcal{L}(q,\boldsymbol{\theta})$ 是对数似然函数的下界，GEM 算法的每个完整 EM 迭代周期都保证对数似然的值增大（除非当前参数已经对应一个局部最大值）。使用 GEM 方法的一种方式，是在 M 步中采用某种非线性优化策略，例如共轭梯度算法。GEM 算法的另一种形式称为*期望条件最大化*（expectation conditional maximization，ECM）算法，它在每个 M 步中执行多次有约束的优化（Meng and Rubin，1993）。例如，可以把参数划分为若干组，再将 M 步分成多个子步骤；每个子步骤只优化其中一个参数子集，而其余参数保持不变。

类似地，我们可以通过关于 $q(\mathbf{Z})$ 对 $\mathcal{L}(q,\boldsymbol{\theta})$ 执行部分优化而不是完全优化，来推广 EM 算法的 E 步（Neal and Hinton，1999）。正如前面所见，对于任意给定的 $\boldsymbol{\theta}$，$\mathcal{L}(q,\boldsymbol{\theta})$ 关于 $q(\mathbf{Z})$ 有唯一的最大值，对应于后验分布 $q_{\boldsymbol{\theta}}(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$；选择这个 $q(\mathbf{Z})$ 时，下界 $\mathcal{L}(q,\boldsymbol{\theta})$ 等于对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。因此，任何收敛到 $\mathcal{L}(q,\boldsymbol{\theta})$ 的全局最大值的算法，都会找到一个同时使对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 达到全局最大值的 $\boldsymbol{\theta}$。只要 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 是 $\boldsymbol{\theta}$ 的连续函数，

<!-- pdf-page: 475 -->
<!-- join-previous-paragraph -->
那么根据连续性，$\mathcal{L}(q,\boldsymbol{\theta})$ 的任何局部最大值也都是 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的局部最大值。

考虑 $N$ 个独立的数据点 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，以及相应的潜变量 $\mathbf{z}_1,\ldots,\mathbf{z}_N$。联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 可以按数据点分解；利用这种结构，可以得到一种增量形式的 EM 算法，每个 EM 迭代周期只处理一个数据点。在 E 步中，我们只重新计算一个数据点的责任度，而不重新计算所有数据点的责任度。乍看之下，随后的 M 步似乎仍然需要涉及所有数据点责任度的计算。然而，如果混合分量属于指数族，那么责任度只通过简单的充分统计量参与计算，而这些统计量可以高效地更新。例如，考虑高斯混合的情形，假设对数据点 $m$ 执行一次更新，将其责任度的旧值和新值分别记为 $\gamma^{\mathrm{old}}(z_{mk})$ 和 $\gamma^{\mathrm{new}}(z_{mk})$。在 M 步中，可以增量更新所需的充分统计量。例如，均值所需的充分统计量由（9.17）和（9.18）定义，由此可得（习题 9.26）

$$
\boldsymbol{\mu}_k^{\mathrm{new}}=\boldsymbol{\mu}_k^{\mathrm{old}}+\left(\frac{\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk})}{N_k^{\mathrm{new}}}\right)\left(\mathbf{x}_m-\boldsymbol{\mu}_k^{\mathrm{old}}\right)
\tag{9.78}
$$

以及

$$
N_k^{\mathrm{new}}=N_k^{\mathrm{old}}+\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk}).
\tag{9.79}
$$

协方差和混合系数的相应结果与此类似。

因此，E 步和 M 步所需的时间都是固定的，与数据点总数无关。由于每处理一个数据点就更新参数，而不必等到整个数据集处理完毕，这种增量版本可能比批量版本收敛得更快。这个增量算法中的每个 E 步或 M 步都会增大 $\mathcal{L}(q,\boldsymbol{\theta})$ 的值；正如前面已经证明的，如果算法收敛到 $\mathcal{L}(q,\boldsymbol{\theta})$ 的一个局部（或全局）最大值，那么它也对应于对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的一个局部（或全局）最大值。

## 习题

**9.1（⋆）www** 考虑 9.1 节讨论的 K 均值算法。证明：由于这组离散指示变量 $r_{nk}$ 的可能赋值只有有限种，而且每一种赋值都对应于 $\{\boldsymbol{\mu}_k\}$ 的唯一最优值，K 均值算法一定会在有限次迭代后收敛。

**9.2（⋆）** 将 2.3.5 节介绍的 Robbins–Monro 序贯估计过程应用于如下问题：求解一个回归函数的根，该回归函数由（9.1）中的 $J$ 对 $\boldsymbol{\mu}_k$ 的导数给出。证明，这会得到一种随机 K 均值算法；对于每个数据点 $\mathbf{x}_n$，它使用（9.5）更新最近的原型 $\boldsymbol{\mu}_k$。

<!-- pdf-page: 476 -->

**9.3（⋆）www** 考虑一个高斯混合模型，其中潜变量的边缘分布 $p(\mathbf{z})$ 由（9.10）给出，观测变量的条件分布 $p(\mathbf{x}\mid\mathbf{z})$ 由（9.11）给出。证明：对 $\mathbf{z}$ 的所有可能取值求和 $p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})$，得到的边缘分布 $p(\mathbf{x})$ 是（9.7）形式的高斯混合。

**9.4（⋆）** 假设我们希望用 EM 算法最大化一个含潜变量模型的参数后验分布 $p(\boldsymbol{\theta}\mid\mathbf{X})$，其中 $\mathbf{X}$ 是观测数据集。证明：E 步与最大似然情形相同，而在 M 步中需要最大化的量是 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})+\ln p(\boldsymbol{\theta})$，其中 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 由（9.30）定义。

**9.5（⋆）** 考虑图 9.6 所示的高斯混合模型的有向图。利用 8.2 节讨论的 d 分离准则，证明潜变量的后验分布可按不同数据点分解，即

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})=\prod_{n=1}^{N}p(\mathbf{z}_n\mid\mathbf{x}_n,\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi}).
\tag{9.80}
$$

**9.6（⋆⋆）** 考虑高斯混合模型的一种特殊情况，其中各分量的协方差矩阵 $\boldsymbol{\Sigma}_k$ 都被约束为相同的值 $\boldsymbol{\Sigma}$。推导在这种模型下最大化似然函数的 EM 方程。

**9.7（⋆）www** 验证：最大化高斯混合模型的完整数据对数似然（9.36），会使各分量的均值和协方差分别独立地拟合对应的数据点组，且混合系数等于各组数据点占总数的比例。

**9.8（⋆）www** 证明：保持责任度 $\gamma(z_{nk})$ 不变，关于 $\boldsymbol{\mu}_k$ 最大化（9.40），会得到（9.17）给出的闭式解。

**9.9（⋆）** 证明：保持责任度 $\gamma(z_{nk})$ 不变，关于 $\boldsymbol{\Sigma}_k$ 和 $\pi_k$ 最大化（9.40），会得到（9.19）和（9.22）给出的闭式解。

**9.10（⋆⋆）** 考虑由混合分布给出的密度模型

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid k)
\tag{9.81}
$$

并假设将向量 $\mathbf{x}$ 分成两部分，使得 $\mathbf{x}=(\mathbf{x}_a,\mathbf{x}_b)$。证明，条件密度 $p(\mathbf{x}_b\mid\mathbf{x}_a)$ 本身也是一个混合分布，并求出混合系数和分量密度的表达式。

<!-- pdf-page: 477 -->

**9.11（⋆）** 在 9.3.2 节中，我们考虑了所有分量的协方差都为 $\epsilon\mathbf{I}$ 的混合模型，从而得到了 K 均值与高斯混合 EM 算法之间的关系。证明：在 $\epsilon\to0$ 的极限下，最大化（9.40）给出的该模型完整数据对数似然的期望，等价于最小化（9.1）给出的 K 均值算法的失真度量 $J$。

**9.12（⋆）www** 考虑如下形式的混合分布

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid k)
\tag{9.82}
$$

其中，$\mathbf{x}$ 的元素可以是离散的、连续的，也可以同时包含这两类。将 $p(\mathbf{x}\mid k)$ 的均值和协方差分别记为 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Sigma}_k$。证明，该混合分布的均值和协方差由（9.49）和（9.50）给出。

**9.13（⋆⋆）** 利用 EM 算法的重估方程，证明：当伯努利混合分布的参数设为对应于似然函数最大值的取值时，它具有如下性质：

$$
\mathbb{E}[\mathbf{x}]=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n\equiv\overline{\mathbf{x}}.
\tag{9.83}
$$

由此证明：如果将这个模型的参数初始化为所有分量都具有相同的均值 $\boldsymbol{\mu}_k=\widehat{\boldsymbol{\mu}}$，其中 $k=1,\ldots,K$，那么无论初始混合系数如何选择，EM 算法都会在一次迭代后收敛，而且这个解具有 $\boldsymbol{\mu}_k=\overline{\mathbf{x}}$ 的性质。注意，这表示混合模型的一种退化情形，其中所有分量都完全相同；实践中，我们会通过恰当的初始化来尽量避免这种解。

**9.14（⋆）** 考虑将（9.52）给出的 $p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})$ 与（9.53）给出的 $p(\mathbf{z}\mid\boldsymbol{\pi})$ 相乘，得到的伯努利分布潜变量与观测变量的联合分布。证明，对这个联合分布关于 $\mathbf{z}$ 边缘化，会得到（9.47）。

**9.15（⋆）www** 证明：关于 $\boldsymbol{\mu}_k$ 最大化伯努利混合分布的完整数据对数似然期望（9.55），会得到 M 步方程（9.59）。

**9.16（⋆）** 证明：关于混合系数 $\pi_k$ 最大化伯努利混合分布的完整数据对数似然期望（9.55），并使用一个拉格朗日乘子来施加求和约束，会得到 M 步方程（9.60）。

**9.17（⋆）www** 证明：由于离散变量 $\mathbf{x}_n$ 满足约束 $0\leqslant p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\leqslant1$，伯努利混合分布的不完整数据对数似然函数具有上界，因此不存在使似然趋于无穷大的奇异点。

<!-- pdf-page: 478 -->

**9.18（⋆⋆）** 考虑 9.3.3 节讨论的伯努利混合模型，并为每个参数向量 $\boldsymbol{\mu}_k$ 引入由 Beta 分布（2.13）给出的先验分布 $p(\boldsymbol{\mu}_k\mid a_k,b_k)$，同时引入（2.38）给出的狄利克雷先验 $p(\boldsymbol{\pi}\mid\boldsymbol{\alpha})$。推导最大化后验概率 $p(\boldsymbol{\mu},\boldsymbol{\pi}\mid\mathbf{X})$ 的 EM 算法。

**9.19（⋆⋆）** 考虑一个 $D$ 维变量 $\mathbf{x}$，它的每个分量 $i$ 本身都是一个 $M$ 阶多项变量，因此 $\mathbf{x}$ 是一个二元向量，其分量为 $x_{ij}$，其中 $i=1,\ldots,D$，$j=1,\ldots,M$，并且对所有 $i$ 都满足约束 $\sum_j x_{ij}=1$。假设这些变量的分布由 2.2 节所讨论的离散多项分布的混合来描述，即

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid\boldsymbol{\mu}_k)
\tag{9.84}
$$

其中

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k)=\prod_{i=1}^{D}\prod_{j=1}^{M}\mu_{kij}^{x_{ij}}.
\tag{9.85}
$$

参数 $\mu_{kij}$ 表示概率 $p(x_{ij}=1\mid\boldsymbol{\mu}_k)$，必须满足 $0\leqslant\mu_{kij}\leqslant1$，且对所有 $k$ 和 $i$ 都满足约束 $\sum_j\mu_{kij}=1$。给定观测数据集 $\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，推导 EM 算法的 E 步和 M 步方程，以最大似然方法优化该分布的混合系数 $\pi_k$ 和分量参数 $\mu_{kij}$。

**9.20（⋆）www** 证明：最大化贝叶斯线性回归模型的完整数据对数似然期望（9.62），会得到 $\alpha$ 的 M 步重估结果（9.63）。

**9.21（⋆⋆）** 利用 3.5 节的证据框架，推导贝叶斯线性回归模型中参数 $\beta$ 的 M 步重估方程，与 $\alpha$ 的结果（9.63）相对应。

**9.22（⋆⋆）** 通过最大化（9.66）定义的完整数据对数似然期望，推导用于重估回归相关向量机超参数的 M 步方程（9.67）和（9.68）。

**9.23（⋆⋆）www** 在 7.2.1 节中，我们直接最大化边缘似然，推导出了重估方程（7.87）和（7.88），用于求回归 RVM 的超参数 $\boldsymbol{\alpha}$ 和 $\beta$ 的值。类似地，在 9.3.4 节中，我们用 EM 算法最大化同一个边缘似然，得到了重估方程（9.67）和（9.68）。证明，这两组重估方程在形式上等价。

**9.24（⋆）** 验证关系式（9.70），其中 $\mathcal{L}(q,\boldsymbol{\theta})$ 和 $\operatorname{KL}(q\|p)$ 分别由（9.71）和（9.72）定义。

<!-- pdf-page: 479 -->

**9.25（⋆）www** 证明：当 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{(\mathrm{old})})$ 时，（9.71）给出的下界 $\mathcal{L}(q,\boldsymbol{\theta})$ 与对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 在 $\boldsymbol{\theta}=\boldsymbol{\theta}^{(\mathrm{old})}$ 处关于 $\boldsymbol{\theta}$ 的梯度相同。

**9.26（⋆）www** 考虑高斯混合 EM 算法的增量形式，其中只重新计算某个特定数据点 $\mathbf{x}_m$ 的责任度。从 M 步公式（9.17）和（9.18）出发，推导用于更新分量均值的结果（9.78）和（9.79）。

**9.27（⋆⋆）** 当责任度以增量方式更新时，推导高斯混合模型中更新协方差矩阵和混合系数的 M 步公式，与更新均值的结果（9.78）相对应。

<!-- pdf-page: 480 -->
