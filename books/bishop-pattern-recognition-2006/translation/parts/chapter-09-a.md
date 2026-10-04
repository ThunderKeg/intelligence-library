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
