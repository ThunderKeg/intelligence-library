<!-- pdf-page: 561 -->

其中，混合系数 $\alpha_1,\ldots,\alpha_K$ 满足 $\alpha_k\geqslant0$ 和 $\sum_k\alpha_k=1$。也可以依次应用基本转移来组合它们，使得

$$
T(\mathbf{z}',\mathbf{z})=\sum_{\mathbf{z}_1}\cdots\sum_{\mathbf{z}_{n-1}}B_1(\mathbf{z}',\mathbf{z}_1)\cdots B_{K-1}(\mathbf{z}_{K-2},\mathbf{z}_{K-1})B_K(\mathbf{z}_{K-1},\mathbf{z}).
\tag{11.43}
$$

如果一个分布对于每个基本转移都是不变的，那么显然，对于（11.42）或（11.43）给出的任一种 $T(\mathbf{z}',\mathbf{z})$，它也保持不变。对于混合形式（11.42），若每个基本转移都满足细致平衡，那么混合转移 $T$ 也满足细致平衡。对使用（11.43）构造的转移概率，这一点并不成立；不过，将基本转移的应用顺序对称化为 $B_1,B_2,\ldots,B_K,B_K,\ldots,B_2,B_1$，就可以恢复细致平衡。组合转移概率的一个常见应用，是每个基本转移只改变变量的一个子集。

### 11.2.2 Metropolis–Hastings 算法

前面介绍了基本的 Metropolis 算法，但尚未真正证明它会从所需分布中采样。在给出证明之前，先讨论一种推广，称为 *Metropolis–Hastings 算法*（Hastings，1970），它适用于提议分布关于其自变量不再对称的情况。具体而言，在算法的第 $\tau$ 步，当前状态为 $\mathbf{z}^{(\tau)}$，从分布 $q_k(\mathbf{z}\mid\mathbf{z}^{(\tau)})$ 抽取样本 $\mathbf{z}^{\star}$，再以概率 $A_k(\mathbf{z}^{\star},\mathbf{z}_{\tau})$ 接受它，其中

$$
A_k(\mathbf{z}^{\star},\mathbf{z}^{(\tau)})=\min\left(1,\frac{\widetilde{p}(\mathbf{z}^{\star})q_k(\mathbf{z}^{(\tau)}\mid\mathbf{z}^{\star})}{\widetilde{p}(\mathbf{z}^{(\tau)})q_k(\mathbf{z}^{\star}\mid\mathbf{z}^{(\tau)})}\right).
\tag{11.44}
$$

这里，$k$ 标识所考虑的可能转移集合中的成员。同样，计算接受判据并不需要知道概率分布 $p(\mathbf{z})=\widetilde{p}(\mathbf{z})/Z_p$ 中的归一化常数 $Z_p$。对于对称的提议分布，Metropolis–Hastings 判据（11.44）会化为（11.33）给出的标准 Metropolis 判据。

通过证明满足（11.40）定义的细致平衡，可以证明 $p(\mathbf{z})$ 是 Metropolis–Hastings 算法所定义的马尔可夫链的不变分布。由（11.44），有

$$
\begin{aligned}
p(\mathbf{z})q_k(\mathbf{z}\mid\mathbf{z}')A_k(\mathbf{z}',\mathbf{z})&=\min\left(p(\mathbf{z})q_k(\mathbf{z}\mid\mathbf{z}'),p(\mathbf{z}')q_k(\mathbf{z}'\mid\mathbf{z})\right)\\
&=\min\left(p(\mathbf{z}')q_k(\mathbf{z}'\mid\mathbf{z}),p(\mathbf{z})q_k(\mathbf{z}\mid\mathbf{z}')\right)\\
&=p(\mathbf{z}')q_k(\mathbf{z}'\mid\mathbf{z})A_k(\mathbf{z},\mathbf{z}')
\end{aligned}
\tag{11.45}
$$

这就是所需的结果。

提议分布的具体选择会显著影响算法的表现。对于连续状态空间，常见的选择是以当前状态为中心的高斯分布，这使得选择该分布的方差参数时需要作重要权衡。如果方差较小，那么

<!-- pdf-page: 562 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-10.png" alt="蓝色各向同性高斯提议圆与红色细长相关高斯椭圆，标示最大最小标准差和提议尺度"><figcaption>图 11.10：使用 Metropolis–Hastings 算法，通过各向同性高斯提议分布（蓝色圆）从相关的多元高斯分布（红色椭圆）采样的示意图；目标分布在不同方向上的标准差相差很大。为了使拒绝率较低，提议分布的尺度 $\rho$ 应与最小标准差 $\sigma_{\min}$ 具有相同数量级，这会导致随机游走行为；相隔大约 $(\sigma_{\max}/\sigma_{\min})^2$ 步的状态才近似独立，其中 $\sigma_{\max}$ 是最大标准差。</figcaption><p class="figure-translation">$\sigma_{\max}$：最大标准差；$\sigma_{\min}$：最小标准差；$\rho$：提议分布的尺度。红色椭圆表示目标分布，蓝色圆表示提议分布。</p></figure>

<!-- join-previous-paragraph-across-figures -->
接受的转移比例会较高，但状态在空间中的移动表现为缓慢的随机游走，导致很长的相关时间。如果方差参数较大，拒绝率就会很高，因为在这里考虑的复杂问题中，许多提议的步骤会到达概率 $p(\mathbf{z})$ 很低的状态。考虑一个多元分布 $p(\mathbf{z})$，其变量 $\mathbf{z}$ 的各分量之间具有强相关性，如图 11.10 所示。提议分布的尺度 $\rho$ 应在不造成高拒绝率的前提下尽可能大。因此，$\rho$ 应与最小长度尺度 $\sigma_{\min}$ 具有相同数量级。系统随后通过随机游走，沿较为伸展的方向探索分布，因此到达一个与初始状态大体独立的状态，所需步数的数量级为 $(\sigma_{\max}/\sigma_{\min})^2$。事实上，在二维情况下，$\rho$ 增大所带来的拒绝率上升，会被那些获接受转移的更大步长抵消；更一般地，对于多元高斯分布，获得独立样本所需步数按 $(\sigma_{\max}/\sigma_2)^2$ 缩放，其中 $\sigma_2$ 是第二小的标准差（Neal，1993）。撇开这些细节，如果分布在不同方向上变化的长度尺度相差很大，Metropolis–Hastings 算法的收敛仍然可能非常缓慢。

## 11.3 Gibbs 采样

Gibbs 采样（Geman and Geman，1984）是一种简单且适用范围广的马尔可夫链蒙特卡洛算法，可以视为 Metropolis–Hastings 算法的一个特殊情形。

考虑希望从中采样的分布 $p(\mathbf{z})=p(z_1,\ldots,z_M)$，并假设已经为马尔可夫链选定初始状态。Gibbs 采样的每一步都将某个变量的值替换为一个新值，这个新值从以其余变量当前值为条件的该变量分布中抽取。因此，将 $z_i$ 替换为从分布 $p(z_i\mid\mathbf{z}_{\backslash i})$ 中抽取的值，其中 $z_i$ 是 $\mathbf{z}$ 的第 $i$ 个分量，$\mathbf{z}_{\backslash i}$ 表示从 $z_1,\ldots,z_M$ 中去掉 $z_i$。这一过程可以通过循环遍历变量来反复进行，

<!-- pdf-page: 563 -->
<!-- join-previous-paragraph -->
每次采用某个特定的顺序；也可以在每一步按照某个分布，随机选取要更新的变量。

例如，假设有一个关于三个变量的分布 $p(z_1,z_2,z_3)$，并且在算法的第 $\tau$ 步，已经选定了值 $z_1^{(\tau)}$、$z_2^{(\tau)}$ 和 $z_3^{(\tau)}$。首先，将 $z_1^{(\tau)}$ 替换为新值 $z_1^{(\tau+1)}$，后者通过从条件分布

$$
p(z_1\mid z_2^{(\tau)},z_3^{(\tau)})
\tag{11.46}
$$

采样得到。接下来，将 $z_2^{(\tau)}$ 替换为从条件分布

$$
p(z_2\mid z_1^{(\tau+1)},z_3^{(\tau)})
\tag{11.47}
$$

中采样得到的值 $z_2^{(\tau+1)}$，这样，$z_1$ 的新值就立即用于后续的采样步骤。然后，用从

$$
p(z_3\mid z_1^{(\tau+1)},z_2^{(\tau+1)})
\tag{11.48}
$$

中抽取的样本 $z_3^{(\tau+1)}$ 更新 $z_3$，如此继续，依次循环遍历这三个变量。

<aside class="procedure">
<h3>Gibbs 采样</h3>
<ol>
<li>初始化 $\{z_i:i=1,\ldots,M\}$。</li>
<li>对于 $\tau=1,\ldots,T$：</li>
</ol>
<p>— 采样：</p>
<p>$$z_1^{(\tau+1)}\sim p(z_1\mid z_2^{(\tau)},z_3^{(\tau)},\ldots,z_M^{(\tau)}).$$</p>
<p>— 采样：</p>
<p>$$z_2^{(\tau+1)}\sim p(z_2\mid z_1^{(\tau+1)},z_3^{(\tau)},\ldots,z_M^{(\tau)}).$$</p>
<p>$\vdots$</p>
<p>— 采样：</p>
<p>$$z_j^{(\tau+1)}\sim p(z_j\mid z_1^{(\tau+1)},\ldots,z_{j-1}^{(\tau+1)},z_{j+1}^{(\tau)},\ldots,z_M^{(\tau)}).$$</p>
<p>$\vdots$</p>
<p>— 采样：</p>
<p>$$z_M^{(\tau+1)}\sim p(z_M\mid z_1^{(\tau+1)},z_2^{(\tau+1)},\ldots,z_{M-1}^{(\tau+1)}).$$</p>
</aside>

<aside class="biography">
<p><strong>乔赛亚·威拉德·吉布斯（Josiah Willard Gibbs）</strong><br>1839–1903</p>
<img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-gibbs.png" alt="乔赛亚·威拉德·吉布斯的肖像">
<p>吉布斯几乎一生都住在父亲于康涅狄格州纽黑文建造的一所房子里。1863 年，他获得了美国第一个工程学博士学位；1871 年，他在耶鲁大学被任命为美国第一个数学物理学讲席教授。由于当时他尚未发表过论著，这个职位没有薪水。他发展了向量分析这一领域，并对晶体学和行星轨道研究作出了贡献。他最著名的著作《论非均相物质的平衡》（On the Equilibrium of Heterogeneous Substances）为物理化学奠定了基础。</p>
</aside>

<!-- pdf-page: 564 -->

为了说明这一过程能够从所需分布中采样，首先注意到，分布 $p(\mathbf{z})$ 对每个单独的 Gibbs 采样步骤都是不变的，因此对于整条马尔可夫链也是不变的。这是因为，当从 $p(z_i\mid\{\mathbf{z}_{\backslash i})$ 采样时，边缘分布 $p(\mathbf{z}_{\backslash i})$ 显然保持不变，因为 $\mathbf{z}_{\backslash i}$ 的值没有改变。此外，按照定义，每一步都从正确的条件分布 $p(z_i\mid\mathbf{z}_{\backslash i})$ 中采样。这些条件分布和边缘分布共同确定了联合分布，因此联合分布本身也保持不变。

要使 Gibbs 采样过程能够从正确的分布中采样，还必须满足第二个要求，即过程具有遍历性。遍历性的一个充分条件是，所有条件分布在任何位置都不为零。如果满足这一条件，那么只需对每个分量变量更新一次，就能在有限步内从 $\mathbf{z}$ 空间中的任意一点到达任意其他点。如果不满足这一要求，即某些条件分布存在零值，那么即使过程具有遍历性，也必须明确加以证明。

为了完整规定算法，还必须指定初始状态的分布，尽管经过多次迭代后抽取的样本实际上会与这一分布无关。当然，马尔可夫链中的相继样本具有很强的相关性，因此，要得到近似独立的样本，就必须对这个序列进行子采样。

可以按照如下方式，将 Gibbs 采样过程看作 Metropolis–Hastings 算法的一个特例。考虑一个只涉及变量 $z_k$ 的 Metropolis–Hastings 采样步骤，其余变量 $\mathbf{z}_{\backslash k}$ 保持固定，从 $\mathbf{z}$ 到 $\mathbf{z}^{\star}$ 的转移概率为 $q_k(\mathbf{z}^{\star}\mid\mathbf{z})=p(z_k^{\star}\mid\mathbf{z}_{\backslash k})$。注意到，$\mathbf{z}_{\backslash k}^{\star}=\mathbf{z}_{\backslash k}$，因为这些分量不因采样步骤而改变。另外，$p(\mathbf{z})=p(z_k\mid\mathbf{z}_{\backslash k})p(\mathbf{z}_{\backslash k})$。于是，Metropolis–Hastings 判据（11.44）中决定接受概率的因子为

$$
A(\mathbf{z}^{\star},\mathbf{z})=\frac{p(\mathbf{z}^{\star})q_k(\mathbf{z}\mid\mathbf{z}^{\star})}{p(\mathbf{z})q_k(\mathbf{z}^{\star}\mid\mathbf{z})}=\frac{p(z_k^{\star}\mid\mathbf{z}_{\backslash k}^{\star})p(\mathbf{z}_{\backslash k}^{\star})p(z_k\mid\mathbf{z}_{\backslash k}^{\star})}{p(z_k\mid\mathbf{z}_{\backslash k})p(\mathbf{z}_{\backslash k})p(z_k^{\star}\mid\mathbf{z}_{\backslash k})}=1
\tag{11.49}
$$

其中用到了 $\mathbf{z}_{\backslash k}^{\star}=\mathbf{z}_{\backslash k}$。因此，这些 Metropolis–Hastings 步骤总会被接受。

与 Metropolis 算法一样，可以通过研究 Gibbs 采样在高斯分布上的应用，来了解它的行为。考虑图 11.11 所示的二变量相关高斯分布，其条件分布的宽度为 $l$，边缘分布的宽度为 $L$。典型步长由条件分布决定，其数量级为 $l$。由于状态按照随机游走演化，要从分布中得到独立样本，所需步数的数量级为 $(L/l)^2$。当然，如果高斯分布中的变量不相关，Gibbs 采样过程就会达到最优效率。对于这个简单问题，可以旋转坐标系来消除变量之间的相关性。不过，在实际应用中，通常无法找到这样的变换。

减少 Gibbs 采样中随机游走行为的一种方法称为 *过松弛*（over-relaxation）（Adler，1981）。这一方法最初适用于

<!-- pdf-page: 565 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-11.png" alt="在二变量相关高斯分布上交替更新的 Gibbs 采样路径，标示边缘宽度 L 与条件宽度 l"><figcaption>图 11.11：通过交替更新两个变量来进行 Gibbs 采样的示意图，这两个变量服从相关高斯分布。步长由条件分布（绿色曲线）的标准差决定，为 $O(l)$，因此沿联合分布（红色椭圆）的伸展方向前进得很慢。从分布中得到一个独立样本所需的步数为 $O((L/l)^2)$。</figcaption><p class="figure-translation">$z_1$、$z_2$：两个变量；$L$：边缘分布的宽度；$l$：条件分布的宽度。红色椭圆表示联合分布，绿色曲线表示条件分布，蓝色折线表示交替更新的路径。</p></figure>

<!-- join-previous-paragraph-across-figures -->
条件分布为高斯分布的问题。这类分布比多元高斯分布更广泛，例如，非高斯分布 $p(z,y)\propto\exp(-z^2y^2)$ 的条件分布就是高斯分布。在 Gibbs 采样算法的每一步，某个特定分量 $z_i$ 的条件分布具有均值 $\mu_i$ 和方差 $\sigma_i^2$。在过松弛框架中，将 $z_i$ 的值替换为

$$
z_i'=\mu_i+\alpha(z_i-\mu_i)+\sigma_i(1-\alpha_i^2)^{1/2}\nu
\tag{11.50}
$$

其中，$\nu$ 是均值为零、方差为一的高斯随机变量，$\alpha$ 是满足 $-1<\alpha<1$ 的参数。当 $\alpha=0$ 时，这一方法等价于标准 Gibbs 采样；当 $\alpha<0$ 时，这一步会倾向于移向均值的另一侧。这一步使所需分布保持不变，因为如果 $z_i$ 的均值为 $\mu_i$、方差为 $\sigma_i^2$，那么 $z_i'$ 也同样如此。过松弛的作用是，当变量高度相关时，促进状态在状态空间中沿一定方向运动。*有序过松弛*（ordered over-relaxation）框架（Neal，1999）将这一方法推广到了非高斯分布。

Gibbs 采样在实践中的适用性，取决于从条件分布 $p(z_k\mid\mathbf{z}_{\backslash k})$ 抽取样本是否容易。对于使用图模型指定的概率分布，各节点的条件分布仅依赖于相应马尔可夫毯中的变量，如图 11.12 所示。对于有向图，为各节点在其父节点给定时的条件分布作出许多不同选择，都能使 Gibbs 采样所用的条件分布具有对数凹性。因此，第 11.1.3 节讨论的自适应拒绝采样方法，提供了一种具有广泛适用性的有向图蒙特卡洛采样框架。

如果图由指数族分布构成，并且父子关系保持共轭性，那么 Gibbs 采样中出现的完全条件分布，就与最初定义各节点的

<!-- pdf-page: 566 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-12.png" alt="无向图与有向图中一个节点的马尔可夫毯，邻居或父节点、子节点及共同父节点用填色标出"><figcaption>图 11.12：Gibbs 采样方法需要从一个变量在其余变量给定时的条件分布中抽取样本。对于图模型，这个条件分布仅是马尔可夫毯中各节点状态的函数。对于无向图，马尔可夫毯由邻居节点组成，如左图所示；对于有向图，马尔可夫毯由父节点、子节点以及子节点的其他父节点组成，如右图所示。</figcaption><p class="figure-translation">左图：无向图的马尔可夫毯。右图：有向图的马尔可夫毯。填色节点组成白色节点的马尔可夫毯。</p></figure>

<!-- join-previous-paragraph-across-figures -->
条件分布（以父节点为条件）具有相同的函数形式，因而可以使用标准采样技术。一般来说，完全条件分布的形式会比较复杂，无法使用标准采样算法。不过，如果这些条件分布是对数凹的，就可以利用自适应拒绝采样高效地采样（假定相应变量是标量）。

如果在 Gibbs 采样算法的每一步，都不从相应的条件分布中抽取样本，而是取使该条件分布达到最大值的变量值作为点估计，就得到第 8.3.3 节讨论的迭代条件众数（ICM）算法。因此，可以将 ICM 看作 Gibbs 采样的一种贪心近似。

由于基本的 Gibbs 采样技术每次只考虑一个变量，相继样本之间具有很强的依赖关系。相反，在另一个极端，如果能够直接从联合分布中抽取样本（我们假定这一步难以实现），那么相继样本就是独立的。采用一种居于两者之间的策略，即依次从一组组变量中采样，而不是从单个变量中采样，有望改进简单的 Gibbs 采样器。*分块 Gibbs 采样*（blocking Gibbs sampling）算法通过选择若干变量块来实现这一点；这些块不一定互不相交，然后以其余变量为条件，依次对每一块中的变量进行联合采样（Jensen et al.，1995）。

## 11.4 切片采样

前面已经看到，Metropolis 算法的一个困难是对步长敏感。如果步长过小，随机游走行为会导致相关性消退缓慢；如果步长过大，高拒绝率又会造成效率低下。*切片采样*（slice sampling）技术（Neal，2003）提供了一种自适应步长，能够自动调整以适应分布的特征。这一方法同样要求能够计算未归一化的分布 $\widetilde{p}(\mathbf{z})$。

先考虑单变量情形。切片采样引入一个额外变量 $u$ 来扩充 $z$，然后在联合的 $(z,u)$ 空间中抽取样本。第 11.5 节讨论混合蒙特卡洛时，还会看到这种方法的另一个例子。目标是在分布

<!-- pdf-page: 567 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-13.png" alt="切片采样的两个面板：固定高度的切片与包含当前状态的采样区间"><figcaption>图 11.13：切片采样的示意图。（a）给定 $z^{(\tau)}$，在区域 $0\leqslant u\leqslant\widetilde{p}(z^{(\tau)})$ 内均匀选取一个 $u$ 值，从而定义穿过分布的一条“切片”，以水平实线表示。（b）由于无法直接从切片中采样，因此从区域 $z_{\min}\leqslant z\leqslant z_{\max}$ 中抽取一个新的 $z$ 样本，该区域包含先前的值 $z^{(\tau)}$。</figcaption><p class="figure-translation">（a）固定 $u$ 后得到的切片；（b）包含当前状态的采样区间。$\widetilde{p}(z)$：未归一化分布；$z^{(\tau)}$：当前状态；$u$：切片的高度；$z_{\min}$、$z_{\max}$：采样区间的两个端点；$z$：采样变量。</p></figure>

<!-- join-previous-paragraph-across-figures -->
下方的区域中均匀采样，其联合分布为

$$
\widehat{p}(z,u)=\begin{cases}1/Z_p&\text{若 }0\leqslant u\leqslant\widetilde{p}(z)\\0&\text{其他情况}\end{cases}
\tag{11.51}
$$

其中 $Z_p=\int\widetilde{p}(z)\,\mathrm{d}z$。关于 $z$ 的边缘分布为

$$
\int\widehat{p}(z,u)\,\mathrm{d}u=\int_0^{\widetilde{p}(z)}\frac{1}{Z_p}\,\mathrm{d}u=\frac{\widetilde{p}(z)}{Z_p}=p(z)
\tag{11.52}
$$

因此，可以从 $\widehat{p}(z,u)$ 中采样，再忽略 $u$ 的值，从而得到 $p(z)$ 的样本。这可以通过交替采样 $z$ 和 $u$ 来实现。给定 $z$ 的值，计算 $\widetilde{p}(z)$，再在范围 $0\leqslant u\leqslant\widetilde{p}(z)$ 内均匀采样 $u$，这很容易实现。然后固定 $u$，从穿过分布的“切片”中均匀采样 $z$，该切片定义为 $\{z:\widetilde{p}(z)>u\}$。图 11.13（a）对此作了说明。

在实践中，直接从分布的切片中采样可能很困难，因此改为定义一种采样方案，使 $\widehat{p}(z,u)$ 所规定的均匀分布保持不变；保证满足细致平衡就可以做到这一点。假设 $z$ 的当前值记为 $z^{(\tau)}$，并且已经得到了一个对应的 $u$ 样本。通过考虑一个包含 $z^{(\tau)}$ 的区域 $z_{\min}\leqslant z\leqslant z_{\max}$，来得到 $z$ 的下一个值。正是在选择这一区域时，方法适应了分布的特征长度尺度。我们希望这个区域尽可能覆盖切片的大部分，以便在 $z$ 空间中作较大幅度的移动；同时又希望该区域落在切片以外的部分尽可能少，因为这部分会降低采样效率。

一种选择区域的方法是，先取一个包含 $z^{(\tau)}$、宽度为 $w$ 的区域，然后检查它的两个端点是否位于切片内。如果某个端点不在切片内，就沿那个方向以 $w$ 为增量扩展区域，直到该端点位于区域之外。然后在这个区域内均匀选取一个候选值 $z'$；如果它位于切片内，就将它作为 $z^{(\tau+1)}$。如果它位于切片外，就收缩区域，使 $z'$ 成为一个端点，同时仍使区域包含 $z^{(\tau)}$。然后再

<!-- pdf-page: 568 -->
<!-- join-previous-paragraph -->
从这个缩小后的区域中均匀抽取另一个候选点，如此继续，直到找到一个位于切片内的 $z$ 值。

采用 Gibbs 采样的方式，反复依次对每个变量采样，就可以将切片采样应用于多元分布。这要求对于每个分量 $z_i$，都能够计算一个与 $p(z_i\mid\mathbf{z}_{\backslash i})$ 成比例的函数。

## 11.5 混合蒙特卡洛算法

前面已经指出，Metropolis 算法的主要局限之一，是它可能表现出随机游走行为，即在状态空间中走过的距离仅按步数的平方根增长。简单地增大步长无法解决这一问题，因为这样会导致很高的拒绝率。

本节介绍一类更复杂的转移，它们以物理系统的类比为基础，能够在保持较低拒绝概率的同时，使系统状态发生较大变化。这类方法适用于连续变量上的分布，并且要求能够方便地计算对数概率关于状态变量的梯度。第 11.5.1 节将讨论动力系统框架，然后在第 11.5.2 节说明，如何将它与 Metropolis 算法结合，得到强大的混合蒙特卡洛算法。阅读本节不需要物理学背景，因为本节自成体系，所有关键结果都从基本原理推导而来。

### 11.5.1 动力系统

利用动力学进行随机采样的方法，源自模拟物理系统在哈密顿动力学支配下演化行为的算法。在马尔可夫链蒙特卡洛模拟中，目标是从给定的概率分布 $p(\mathbf{z})$ 中采样。通过将概率模拟写成哈密顿系统的形式，就可以利用 *哈密顿动力学*（Hamiltonian dynamics）框架。为了与这一领域的文献保持一致，在适当之处会使用相关的动力系统术语，并在介绍过程中给出定义。

我们考虑的动力学，描述状态变量 $\mathbf{z}=\{z_i\}$ 随连续时间的演化，这里的时间记为 $\tau$。经典动力学由牛顿第二运动定律描述，即物体的加速度与所受的力成正比，对应于一个关于时间的二阶微分方程。通过引入中间的 *动量* 变量 $\mathbf{r}$，可以将一个二阶方程分解为两个相互耦合的一阶方程。动量变量对应于状态变量 $\mathbf{z}$ 的变化率，其分量为

$$
r_i=\frac{\mathrm{d}z_i}{\mathrm{d}\tau}
\tag{11.53}
$$

其中，从动力学的角度看，$z_i$ 可以视为 *位置* 变量。因此，

<!-- pdf-page: 569 -->
<!-- join-previous-paragraph -->
每个位置变量都有一个对应的动量变量，位置变量和动量变量构成的联合空间称为 *相空间*（phase space）。

不失一般性，可以将概率分布 $p(\mathbf{z})$ 写成

$$
p(\mathbf{z})=\frac{1}{Z_p}\exp\left(-E(\mathbf{z})\right)
\tag{11.54}
$$

其中，$E(\mathbf{z})$ 被解释为系统处于状态 $\mathbf{z}$ 时的 *势能*。系统的加速度是动量的变化率，由施加的 *力* 决定，而这个力本身就是势能的负梯度

$$
\frac{\mathrm{d}r_i}{\mathrm{d}\tau}=-\frac{\partial E(\mathbf{z})}{\partial z_i}.
\tag{11.55}
$$

使用哈密顿框架重新表述这个动力系统会很方便。为此，首先定义 *动能*

$$
K(\mathbf{r})=\frac{1}{2}\|\mathbf{r}\|^2=\frac{1}{2}\sum_i r_i^2.
\tag{11.56}
$$

系统的总能量就是势能与动能之和

$$
H(\mathbf{z},\mathbf{r})=E(\mathbf{z})+K(\mathbf{r})
\tag{11.57}
$$

其中，$H$ 是 *哈密顿函数*。利用（11.53）、（11.55）、（11.56）和（11.57），现在可以用如下 *哈密顿方程* 表达系统的动力学（习题 11.15）：

$$
\frac{\mathrm{d}z_i}{\mathrm{d}\tau}=\frac{\partial H}{\partial r_i}
\tag{11.58}
$$

$$
\frac{\mathrm{d}r_i}{\mathrm{d}\tau}=-\frac{\partial H}{\partial z_i}.
\tag{11.59}
$$

<aside class="biography">
<p><strong>威廉·哈密顿（William Hamilton）</strong><br>1805–1865</p>
<img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-hamilton.png" alt="威廉·哈密顿的肖像">
<p>威廉·罗恩·哈密顿是一位爱尔兰数学家和物理学家，自幼聪颖过人。1827 年，他尚未毕业，就被任命为都柏林三一学院的天文学教授。哈密顿最重要的贡献之一，是提出了动力学的一种新表述，它在后来量子力学的发展中发挥了重要作用。他的另一项重大成就是创立了四元数，通过引入三个不同的负一平方根，推广了复数的概念；这三个平方根满足 $i^2=j^2=k^2=ijk=-1$。据说，1843 年 10 月 16 日，他与妻子沿都柏林皇家运河散步时，脑海中浮现了这些方程，随后便立即将它们刻在布鲁姆桥的侧面。如今已经找不到这些刻痕，但桥上有一块石牌，纪念这一发现，并展示四元数方程。</p>
</aside>

<!-- pdf-page: 570 -->

在这个动力系统的演化过程中，哈密顿量 $H$ 的值保持不变，通过求导很容易看出这一点：

$$
\begin{aligned}
\frac{\mathrm{d}H}{\mathrm{d}\tau}&=\sum_i\left\{\frac{\partial H}{\partial z_i}\frac{\mathrm{d}z_i}{\mathrm{d}\tau}+\frac{\partial H}{\partial r_i}\frac{\mathrm{d}r_i}{\mathrm{d}\tau}\right\}\\
&=\sum_i\left\{\frac{\partial H}{\partial z_i}\frac{\partial H}{\partial r_i}-\frac{\partial H}{\partial r_i}\frac{\partial H}{\partial z_i}\right\}=0.
\end{aligned}
\tag{11.60}
$$

哈密顿动力系统的第二个重要性质，是保持相空间中的体积不变，这称为 *刘维尔定理*（Liouville's Theorem）。换言之，如果考虑变量 $(\mathbf{z},\mathbf{r})$ 空间中的一个区域，那么这个区域按照哈密顿动力学方程演化时，形状可以改变，但体积不变。为说明这一点，注意到流场（相空间中位置的变化率）为

$$
\mathbf{V}=\left(\frac{\mathrm{d}\mathbf{z}}{\mathrm{d}\tau},\frac{\mathrm{d}\mathbf{r}}{\mathrm{d}\tau}\right)
\tag{11.61}
$$

而这个场的散度为零：

$$
\begin{aligned}
\operatorname{div}\mathbf{V}&=\sum_i\left\{\frac{\partial}{\partial z_i}\frac{\mathrm{d}z_i}{\mathrm{d}\tau}+\frac{\partial}{\partial r_i}\frac{\mathrm{d}r_i}{\mathrm{d}\tau}\right\}\\
&=\sum_i\left\{-\frac{\partial}{\partial z_i}\frac{\partial H}{\partial r_i}+\frac{\partial}{\partial r_i}\frac{\partial H}{\partial z_i}\right\}=0.
\end{aligned}
\tag{11.62}
$$

现在考虑相空间上的联合分布，其总能量为哈密顿量，即

$$
p(\mathbf{z},\mathbf{r})=\frac{1}{Z_H}\exp(-H(\mathbf{z},\mathbf{r})).
\tag{11.63}
$$

利用体积守恒和 $H$ 守恒这两个结果，可以得出，哈密顿动力学使 $p(\mathbf{z},\mathbf{r})$ 保持不变。考虑相空间中的一个小区域，在这个区域上 $H$ 近似为常数，就可以看出这一点。如果按照哈密顿方程演化一段有限的时间，那么这个区域的体积保持不变，区域内的 $H$ 值也保持不变。因此，仅为 $H$ 的函数的概率密度也保持不变。

尽管 $H$ 不变，$\mathbf{z}$ 和 $\mathbf{r}$ 的值却会变化。因此，将哈密顿动力学积分一段有限的时间，就能以有规律的方式使 $\mathbf{z}$ 发生较大变化，同时避免随机游走行为。

不过，按照哈密顿动力学演化，并不能遍历地从 $p(\mathbf{z},\mathbf{r})$ 中采样，因为 $H$ 的值不变。为了得到具有遍历性的采样方案，可以在相空间中引入额外的移动，在改变 $H$ 值的同时，仍使分布 $p(\mathbf{z},\mathbf{r})$ 保持不变。最简单的做法是，将 $\mathbf{r}$ 的值替换为从以 $\mathbf{z}$ 为条件的分布中抽取的值。这可以看作一个 Gibbs 采样步骤，因此，根据

<!-- pdf-page: 571 -->
<!-- join-previous-paragraph -->
第 11.3 节可知，它也使所需分布保持不变。注意到 $\mathbf{z}$ 和 $\mathbf{r}$ 在分布 $p(\mathbf{z},\mathbf{r})$ 中相互独立，因此条件分布 $p(\mathbf{r}\mid\mathbf{z})$ 是一个高斯分布，很容易从中采样（习题 11.16）。

在实际应用这一方法时，必须解决哈密顿方程的数值积分问题。这不可避免地会引入数值误差，因此应设计一种方案，尽量减小这些误差的影响。事实上，可以设计出使刘维尔定理仍然严格成立的积分方案。这一性质在第 11.5.2 节讨论的混合蒙特卡洛算法中很重要。实现这一点的一种方案称为 *蛙跳离散化*（leapfrog discretization），它交替更新位置和动量变量的离散时间近似 $\widehat{\mathbf{z}}$ 和 $\widehat{\mathbf{r}}$：

$$
\widehat{r}_i(\tau+\epsilon/2)=\widehat{r}_i(\tau)-\frac{\epsilon}{2}\frac{\partial E}{\partial z_i}(\widehat{\mathbf{z}}(\tau))
\tag{11.64}
$$

$$
\widehat{z}_i(\tau+\epsilon)=\widehat{z}_i(\tau)+\epsilon\widehat{r}_i(\tau+\epsilon/2)
\tag{11.65}
$$

$$
\widehat{r}_i(\tau+\epsilon)=\widehat{r}_i(\tau+\epsilon/2)-\frac{\epsilon}{2}\frac{\partial E}{\partial z_i}(\widehat{\mathbf{z}}(\tau+\epsilon)).
\tag{11.66}
$$

可以看到，它先以步长 $\epsilon/2$ 对动量变量作半步更新，再以步长 $\epsilon$ 对位置变量作整步更新，最后对动量变量作第二次半步更新。如果连续执行若干个蛙跳步骤，就可以将动量变量的半步更新合并成步长为 $\epsilon$ 的整步更新。这样，位置变量和动量变量的相继更新就彼此交错，如同相互蛙跳。为了让动力学演化时间间隔 $\tau$，需要执行 $\tau/\epsilon$ 步。假定函数 $E(\mathbf{z})$ 光滑，那么当 $\epsilon\to0$ 时，离散近似相对于连续时间动力学的误差也趋于零。不过，实际使用的是非零 $\epsilon$，因此仍会残留一些误差。第 11.5.2 节将说明，混合蒙特卡洛算法如何消除这些误差的影响。

总之，哈密顿动力学方法交替执行一系列蛙跳更新，以及从动量变量的边缘分布中重新采样这两个过程。

注意，与基本的 Metropolis 算法不同，哈密顿动力学方法既能利用概率分布本身的信息，也能利用对数概率分布的梯度信息。在函数优化领域，我们熟悉一种类似的情况：在大多数能够获得梯度信息的场合，利用它都很有好处。直观地说，这是因为在一个 $D$ 维空间中，与计算函数本身相比，计算梯度所增加的计算量通常只是一个不依赖于 $D$ 的固定倍数；而 $D$ 维梯度向量提供了 $D$ 项信息，函数值本身却只提供一项信息。

<!-- pdf-page: 572 -->

### 11.5.2 混合蒙特卡洛

上一节已经讨论，对于非零步长 $\epsilon$，蛙跳算法的离散化会在哈密顿动力学方程的积分中引入误差。*混合蒙特卡洛*（hybrid Monte Carlo）（Duane et al.，1987；Neal，1996）将哈密顿动力学与 Metropolis 算法相结合，从而消除离散化带来的偏差。

具体而言，算法所用的马尔可夫链交替进行两种更新：随机更新动量变量 $\mathbf{r}$，以及利用蛙跳算法进行哈密顿动力学更新。每次应用蛙跳算法后，根据哈密顿量 $H$ 的值，按照 Metropolis 判据接受或拒绝所得的候选状态。因此，如果 $(\mathbf{z},\mathbf{r})$ 是初始状态，$(\mathbf{z}^{\star},\mathbf{r}^{\star})$ 是蛙跳积分后的状态，那么接受这个候选状态的概率为

$$
\min\left(1,\exp\{H(\mathbf{z},\mathbf{r})-H(\mathbf{z}^{\star},\mathbf{r}^{\star})\}\right).
\tag{11.67}
$$

如果蛙跳积分能够完美模拟哈密顿动力学，那么每一个这样的候选步骤都会自动被接受，因为 $H$ 的值不会改变。由于数值误差，$H$ 的值有时可能减小；我们希望 Metropolis 判据能消除这种影响造成的偏差，确保所得样本确实来自所需分布。为此，需要确保蛙跳积分对应的更新方程满足细致平衡（11.40）。按照如下方式修改蛙跳方案，就很容易做到这一点。

在每一段蛙跳积分序列开始之前，以相同概率随机选择沿时间正向积分（使用步长 $\epsilon$），还是沿时间反向积分（使用步长 $-\epsilon$）。首先注意到，（11.64）、（11.65）和（11.66）给出的蛙跳积分方案在时间上可逆，因此，以步长 $-\epsilon$ 积分 $L$ 步，会恰好抵消以步长 $\epsilon$ 积分 $L$ 步的效果。接下来说明，蛙跳积分严格保持相空间体积不变。这是因为，蛙跳方案中的每一步只更新一个 $z_i$ 变量或一个 $r_i$ 变量，而更新量只依赖于另一个变量。如图 11.14 所示，这会使相空间中的一个区域发生剪切，却不改变它的体积。

最后，利用这些结果来说明细致平衡成立。考虑相空间中的一个小区域 $\mathcal{R}$，经过步长为 $\epsilon$ 的 $L$ 次蛙跳迭代后，它被映射到区域 $\mathcal{R}'$。根据蛙跳迭代中的体积守恒可知，如果 $\mathcal{R}$ 的体积为 $\delta V$，那么 $\mathcal{R}'$ 的体积也为 $\delta V$。如果从分布（11.63）中选择一个初始点，再用 $L$ 次蛙跳更新来更新它，那么从 $\mathcal{R}$ 转移到 $\mathcal{R}'$ 的概率为

$$
\frac{1}{Z_H}\exp(-H(\mathcal{R}))\delta V\frac{1}{2}\min\left\{1,\exp(-H(\mathcal{R})+H(\mathcal{R}'))\right\}.
\tag{11.68}
$$

其中，因子 $1/2$ 来自选择使用正步长而非负步长进行积分的概率。同样，从

<!-- pdf-page: 573 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-14.png" alt="蛙跳更新将相空间矩形剪切为曲边区域，蓝色竖条显示体积不变"><figcaption>图 11.14：蛙跳算法（11.64）—（11.66）的每一步，都修改一个位置变量 $z_i$ 或一个动量变量 $r_i$。由于一个变量的变化量只依赖于另一个变量，相空间中的任意区域都会发生剪切，而体积保持不变。</figcaption><p class="figure-translation">$z_i$、$r_i$：更新前的位置变量和动量变量；$z_i'$、$r_i'$：更新后的变量。红色边界表示相空间中的区域，蓝色竖条表示剪切前后对应的部分。</p></figure>

<!-- join-previous-paragraph-across-figures -->
区域 $\mathcal{R}'$ 出发并沿时间反向积分，最终到达区域 $\mathcal{R}$ 的概率为

$$
\frac{1}{Z_H}\exp(-H(\mathcal{R}'))\delta V\frac{1}{2}\min\left\{1,\exp(-H(\mathcal{R}')+H(\mathcal{R}))\right\}.
\tag{11.69}
$$

很容易看出，概率（11.68）和（11.69）相等，因此细致平衡成立（习题 11.17）。注意，这个证明没有考虑区域 $\mathcal{R}$ 和 $\mathcal{R}'$ 之间的重叠，但很容易推广到允许这种重叠的情况。

不难构造这样的例子：蛙跳算法经过有限次迭代后，返回起始位置。在这些情形中，每次蛙跳积分之前随机替换动量值，并不足以保证遍历性，因为位置变量永远不会被更新。只要在每次蛙跳积分之前，从一个较小的区间内随机选择步长的大小，就很容易避免这种现象。

通过考虑混合蒙特卡洛算法在多元高斯分布上的应用，可以了解它的行为。为方便起见，考虑各分量相互独立的高斯分布 $p(\mathbf{z})$，其哈密顿量为

$$
H(\mathbf{z},\mathbf{r})=\frac{1}{2}\sum_i\frac{1}{\sigma_i^2}z_i^2+\frac{1}{2}\sum_i r_i^2.
\tag{11.70}
$$

我们的结论对于各分量相关的高斯分布同样成立，因为混合蒙特卡洛算法具有旋转各向同性。在蛙跳积分过程中，每一对相空间变量 $z_i,r_i$ 都独立演化。不过，候选点的接受或拒绝取决于 $H$ 的值，而 $H$ 又取决于所有变量的值。因此，任意一个变量中较大的积分误差，都可能造成很高的拒绝概率。为了使离散蛙跳积分能够足够好地

<!-- pdf-page: 574 -->
<!-- join-previous-paragraph -->
近似真实的连续时间动力学，蛙跳积分尺度 $\epsilon$ 必须小于势能发生显著变化的最短长度尺度。这个尺度由 $\sigma_i$ 的最小值决定，将它记为 $\sigma_{\min}$。回顾混合蒙特卡洛中蛙跳积分的目标：在相空间中移动足够远，到达一个与初始状态相对独立的新状态，同时仍保持较高的接受概率。为实现这一目标，蛙跳积分必须持续执行数量级为 $\sigma_{\max}/\sigma_{\min}$ 的迭代。

相比之下，考虑前面讨论过的简单 Metropolis 算法，其提议分布为方差 $s^2$ 的各向同性高斯分布。为了避免高拒绝率，$s$ 的数量级必须为 $\sigma_{\min}$。随后，对状态空间的探索通过随机游走进行，需要数量级为 $(\sigma_{\max}/\sigma_{\min})^2$ 的步数，才能到达一个近似独立的状态。

## 11.6 估计配分函数

前面已经看到，本章考虑的大多数采样算法，只要求知道概率分布的函数形式，而不必知道其中的乘法常数。因此，如果写成

$$
p_E(\mathbf{z})=\frac{1}{Z_E}\exp(-E(\mathbf{z}))
\tag{11.71}
$$

那么，为了从 $p(\mathbf{z})$ 中抽取样本，并不需要知道归一化常数 $Z_E$ 的值，这个常数也称为配分函数。不过，知道 $Z_E$ 的值可能有助于贝叶斯模型比较，因为它表示模型证据（即给定模型时观测数据的概率），所以值得考虑如何求出它的值。假定无法通过在 $\mathbf{z}$ 的状态空间上，对函数 $\exp(-E(\mathbf{z}))$ 求和或积分来直接计算它。

对于模型比较，实际需要的是两个模型的配分函数之比。将这个比值乘以先验概率之比，就得到后验概率之比，进而可以用于模型选择或模型平均。

估计配分函数之比的一种方法，是从能量函数为 $G(\mathbf{z})$ 的分布中进行重要性采样：

$$
\begin{aligned}
\frac{Z_E}{Z_G}&=\frac{\sum_{\mathbf{z}}\exp(-E(\mathbf{z}))}{\sum_{\mathbf{z}}\exp(-G(\mathbf{z}))}\\
&=\frac{\sum_{\mathbf{z}}\exp(-E(\mathbf{z})+G(\mathbf{z}))\exp(-G(\mathbf{z}))}{\sum_{\mathbf{z}}\exp(-G(\mathbf{z}))}\\
&=\mathbb{E}_{G(\mathbf{z})}[\exp(-E+G)]\\
&\simeq\sum_l\exp(-E(\mathbf{z}^{(l)})+G(\mathbf{z}^{(l)}))
\end{aligned}
\tag{11.72}
$$

<!-- pdf-page: 575 -->

其中，$\{\mathbf{z}^{(l)}\}$ 是从 $p_G(\mathbf{z})$ 所定义的分布中抽取的样本。如果分布 $p_G$ 的配分函数可以解析计算，例如它是高斯分布，那么就能得到 $Z_E$ 的绝对值。

只有当重要性采样分布 $p_G$ 与分布 $p_E$ 很接近，使比值 $p_E/p_G$ 不会大幅变化时，这种方法才能给出准确结果。在实践中，对于本书考虑的这类复杂模型，很难找到适当的、能够用解析形式指定的重要性采样分布。

因此，另一种方法是利用从马尔可夫链获得的样本，来定义重要性采样分布。如果马尔可夫链的转移概率为 $T(\mathbf{z},\mathbf{z}')$，样本集为 $\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(L)}$，那么采样分布可以写成

$$
\frac{1}{Z_G}\exp\left(-G(\mathbf{z})\right)=\sum_{l=1}^L T(\mathbf{z}^{(l)},\mathbf{z})
\tag{11.73}
$$

并直接用于（11.72）。

要成功估计两个配分函数之比，相应的两个分布必须足够接近。如果希望求得复杂分布的配分函数绝对值，这一要求就尤其难以满足，因为只有相对简单的分布，才能直接计算配分函数，所以试图直接估计配分函数之比不太可能成功。可以用一种称为 *链式连接*（chaining）的技术（Neal，1993；Barber and Bishop，1997）处理这个问题：引入一系列中间分布 $p_2,\ldots,p_{M-1}$，在能够计算归一化系数 $Z_1$ 的简单分布 $p_1(\mathbf{z})$ 与所需的复杂分布 $p_M(\mathbf{z})$ 之间进行插值。于是有

$$
\frac{Z_M}{Z_1}=\frac{Z_2}{Z_1}\frac{Z_3}{Z_2}\cdots\frac{Z_M}{Z_{M-1}}
\tag{11.74}
$$

其中，中间各个比值可以用前面讨论的蒙特卡洛方法确定。构造这样一系列中间系统的一种方式，是使用一个包含连续参数 $0\leqslant\alpha\leqslant1$ 的能量函数，在两个分布之间进行插值：

$$
E_\alpha(\mathbf{z})=(1-\alpha)E_1(\mathbf{z})+\alpha E_M(\mathbf{z}).
\tag{11.75}
$$

如果使用蒙特卡洛方法求（11.74）中的中间比值，那么让同一条马尔可夫链连续运行，可能比为每个比值重新启动马尔可夫链更高效。在这种情况下，马尔可夫链最初针对系统 $p_1$ 运行，经过适当数量的步骤后，再转到序列中的下一个分布。不过要注意，系统在每个阶段都必须保持接近平衡分布。

<!-- pdf-page: 576 -->

## 习题

**11.1（⋆）www** 证明，（11.2）定义的有限样本估计量 $\widehat{f}$ 的均值等于 $\mathbb{E}[f]$，方差由（11.3）给出。

**11.2（⋆）** 假设随机变量 $z$ 在 $(0,1)$ 上服从均匀分布，并对它进行变换 $y=h^{-1}(z)$，其中 $h(y)$ 由（11.6）给出。证明，$y$ 服从分布 $p(y)$。

**11.3（⋆）** 给定一个在 $(0,1)$ 上均匀分布的随机变量 $z$，求一个变换 $y=f(z)$，使 $y$ 服从（11.8）给出的柯西分布。

**11.4（⋆⋆）** 假设 $z_1$ 和 $z_2$ 在单位圆内均匀分布，如图 11.3 所示，并进行（11.10）和（11.11）给出的变量变换。证明，$(y_1,y_2)$ 服从（11.12）给出的分布。

**11.5（⋆）www** 设 $\mathbf{z}$ 是一个 $D$ 维随机变量，服从零均值、单位协方差矩阵的高斯分布，并假设正定对称矩阵 $\boldsymbol{\Sigma}$ 的 Cholesky 分解为 $\boldsymbol{\Sigma}=\mathbf{L}\mathbf{L}^{\mathrm{T}}$，其中 $\mathbf{L}$ 为下三角矩阵（即主对角线上方的元素均为零）。证明，变量 $\mathbf{y}=\boldsymbol{\mu}+\mathbf{L}\mathbf{z}$ 服从均值为 $\boldsymbol{\mu}$、协方差为 $\boldsymbol{\Sigma}$ 的高斯分布。这给出了一种利用零均值、单位方差的一元高斯样本，生成一般多元高斯样本的方法。

**11.6（⋆⋆）www** 本题将更仔细地证明，拒绝采样确实能从所需的分布 $p(\mathbf{z})$ 中抽取样本。假设提议分布为 $q(\mathbf{z})$，证明样本值 $\mathbf{z}$ 被接受的概率为 $\widetilde{p}(\mathbf{z})/kq(\mathbf{z})$，其中 $\widetilde{p}$ 是任意一个与 $p(\mathbf{z})$ 成比例的未归一化分布，常数 $k$ 取为使所有 $\mathbf{z}$ 都满足 $kq(\mathbf{z})\geqslant\widetilde{p}(\mathbf{z})$ 的最小值。注意，抽得一个值 $\mathbf{z}$ 的概率，等于从 $q(\mathbf{z})$ 抽得该值的概率，乘以在已抽得该值的条件下接受它的概率。利用这一点，以及概率的求和法则和乘积法则，写出关于 $\mathbf{z}$ 的分布的归一化形式，并证明它等于 $p(\mathbf{z})$。

**11.7（⋆）** 假设 $z$ 在区间 $[0,1]$ 上服从均匀分布。证明，变量 $y=b\tan z+c$ 服从（11.16）给出的柯西分布。

**11.8（⋆⋆）** 利用连续性和归一化的要求，确定自适应拒绝采样的包络分布（11.17）中系数 $k_i$ 的表达式。

**11.9（⋆⋆）** 利用第 11.1.1 节讨论的从单个指数分布中采样的技术，设计一个从（11.17）所定义的分段指数分布中采样的算法。

**11.10（⋆）** 证明，（11.34）、（11.35）和（11.36）定义的整数上的简单随机游走，具有性质 $\mathbb{E}[(z^{(\tau)})^2]=\mathbb{E}[(z^{(\tau-1)})^2]+1/2$，并由此通过归纳法证明 $\mathbb{E}[(z^{(\tau)})^2]=\tau/2$。

<!-- pdf-page: 577 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-15.png" alt="二变量平面中两个互不相连的红色区域，概率密度仅在这两个区域内为常数"><figcaption>图 11.15：两个变量 $z_1$ 和 $z_2$ 上的概率分布，它在阴影区域内均匀，在其他所有位置均为零。</figcaption><p class="figure-translation">$z_1$：横轴变量；$z_2$：纵轴变量。两个红色区域表示概率分布非零且均匀的区域。</p></figure>

**11.11（⋆⋆）www** 证明，第 11.3 节讨论的 Gibbs 采样算法满足（11.40）定义的细致平衡。

**11.12（⋆）** 考虑图 11.15 所示的分布。讨论针对这个分布的标准 Gibbs 采样过程是否具有遍历性，以及它能否正确地从这个分布中采样。

**11.13（⋆⋆）** 考虑图 11.16 所示的简单三节点图，其中，观测节点 $x$ 服从均值为 $\mu$、精度为 $\tau$ 的高斯分布 $\mathcal{N}(x\mid\mu,\tau^{-1})$。假设均值和精度的边缘分布分别为 $\mathcal{N}(\mu\mid\mu_0,s_0)$ 和 $\operatorname{Gam}(\tau\mid a,b)$，其中 $\operatorname{Gam}(\cdot\mid\cdot,\cdot)$ 表示伽马分布。写出将 Gibbs 采样应用于后验分布 $p(\mu,\tau\mid x)$ 时所需的条件分布 $p(\mu\mid x,\tau)$ 和 $p(\tau\mid x,\mu)$ 的表达式。

**11.14（⋆）** 验证过松弛更新（11.50）：其中 $z_i$ 的均值为 $\mu_i$、方差为 $\sigma_i$，$\nu$ 的均值为零、方差为一，更新得到的值 $z_i'$ 的均值为 $\mu_i$、方差为 $\sigma_i^2$。

**11.15（⋆）www** 利用（11.56）和（11.57），证明哈密顿方程（11.58）等价于（11.53）。类似地，利用（11.57），证明（11.59）等价于（11.55）。

**11.16（⋆）** 利用（11.56）、（11.57）和（11.63），证明条件分布 $p(\mathbf{r}\mid\mathbf{z})$ 是高斯分布。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/b-fig-11-16.png" alt="均值 μ 与精度 τ 指向观测高斯变量 x 的三节点有向图"><figcaption>图 11.16：一个包含观测高斯变量 $x$ 的图，其均值 $\mu$ 和精度 $\tau$ 具有先验分布。</figcaption><p class="figure-translation">$\mu$：均值；$\tau$：精度；$x$：已观测的高斯变量，以填色节点表示。</p></figure>

<!-- pdf-page: 578 -->

**11.17（⋆）www** 验证概率（11.68）和（11.69）相等，从而证明混合蒙特卡洛算法满足细致平衡。
