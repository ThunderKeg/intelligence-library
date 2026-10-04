# 第 11 章 采样方法

<aside class="chapter-guide"><strong>本章导读</strong><p>当积分难以直接计算时，可以用随机样本估计所需的期望。本章从简单分布的采样出发，介绍拒绝采样、重要性采样和马尔可夫链方法，并讨论样本相关性、随机游走与高维空间怎样影响计算效率。</p></aside>

<!-- pdf-page: 543 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-chapter-opening.png" alt="水面纹理上的第 11 章标题"><p class="figure-translation">Sampling Methods → 采样方法。</p></figure>

对于大多数具有实际意义的概率模型，精确推断难以处理，因此必须采用某种近似方法。第 10 章讨论了基于确定性近似的推断算法，包括变分贝叶斯和期望传播等方法。这里将讨论基于数值采样的近似推断方法，也称为蒙特卡洛（Monte Carlo）技术。

在某些应用中，未观测变量的后验分布本身就是直接关心的对象；但在多数情况下，我们需要后验分布，主要是为了计算期望，例如作出预测。因此，本章要解决的基本问题，是计算某个函数 $f(\mathbf{z})$ 关于概率分布 $p(\mathbf{z})$ 的期望。这里，$\mathbf{z}$ 的各分量可以是离散变量、连续变量，也可以是两者的组合。因此，对于连续

<!-- pdf-page: 544 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-1.png" alt="红色概率密度 p(z) 与蓝色函数 f(z)，示意相对于分布计算函数期望"><figcaption>图 11.1：函数 $f(z)$ 的示意图，我们要计算它关于分布 $p(z)$ 的期望。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
变量，我们希望计算期望

$$
\mathbb{E}[f]=\int f(\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}
\tag{11.1}
$$

如果变量是离散的，就用求和代替积分。图 11.1 对单个连续变量的情形作了示意。我们假定这些期望过于复杂，无法用解析方法精确计算。

采样方法的基本思想是，从分布 $p(\mathbf{z})$ 独立抽取一组样本 $\mathbf{z}^{(l)}$，其中 $l=1,\ldots,L$。这样，就可以用有限项求和近似期望（11.1）：

$$
\widehat{f}=\frac{1}{L}\sum_{l=1}^{L}f(\mathbf{z}^{(l)}).
\tag{11.2}
$$

只要样本 $\mathbf{z}^{(l)}$ 是从分布 $p(\mathbf{z})$ 中抽取的，就有 $\mathbb{E}[\widehat{f}]=\mathbb{E}[f]$，所以估计量 $\widehat{f}$ 具有正确的均值。该估计量的方差为<span class="margin-reference">习题 11.1</span>

$$
\operatorname{var}[\widehat{f}]=\frac{1}{L}\mathbb{E}\left[(f-\mathbb{E}[f])^2\right]
\tag{11.3}
$$

其中的期望是函数 $f(\mathbf{z})$ 在分布 $p(\mathbf{z})$ 下的方差。需要强调，由此可见，估计量的精度不依赖于 $\mathbf{z}$ 的维数，而且原则上只用相对较少的样本 $\mathbf{z}^{(l)}$，就可能达到很高的精度。在实践中，十个或二十个独立样本就可能足以将期望估计到所需精度。

然而，问题在于样本 $\{\mathbf{z}^{(l)}\}$ 可能并不独立，因此有效样本量可能远小于表面上的样本量。此外，回看图 11.1，可以注意到：如果在 $p(\mathbf{z})$ 较大的区域 $f(\mathbf{z})$ 很小，反之亦然，那么期望可能主要由概率很小的区域决定，这意味着需要较大的样本量才能达到足够精度。

对于许多模型，使用图模型可以很方便地指定联合分布 $p(\mathbf{z})$。如果是没有观测变量的有向图，就可以

<!-- pdf-page: 545 -->

<!-- join-previous-paragraph -->
很容易地通过下面的祖先采样（ancestral sampling）方法，从联合分布中采样，前提是能够从每个节点的条件分布中采样。第 8.1.2 节曾简要讨论过这种方法。联合分布写为

$$
p(\mathbf{z})=\prod_{i=1}^{M}p(\mathbf{z}_i\mid\mathrm{pa}_i)
\tag{11.4}
$$

其中，$\mathbf{z}_i$ 是与节点 $i$ 对应的一组变量，$\mathrm{pa}_i$ 表示与节点 $i$ 的父节点对应的变量集合。要从联合分布中获得一个样本，只需按 $\mathbf{z}_1,\ldots,\mathbf{z}_M$ 的顺序遍历这些变量一次，依次从条件分布 $p(\mathbf{z}_i\mid\mathrm{pa}_i)$ 中采样。这个过程总是可行的，因为在每一步，所有父节点的取值都已确定。遍历图一次后，就得到了联合分布的一个样本。

现在考虑某些节点已由观测值赋值的有向图。原则上，至少对于表示离散变量的节点，我们可以扩展上述过程，得到下面的逻辑采样（logic sampling）方法（Henrion, 1988），它可以看作第 11.1.4 节将讨论的重要性采样的一个特例。在每一步，如果为已观测变量 $\mathbf{z}_i$ 抽得一个值，就将它与观测值比较；若两者相同，则保留该采样值，并继续处理下一个变量。但是，如果采样值与观测值不同，就丢弃到目前为止得到的整个样本，并从图中的第一个节点重新开始。这个算法能够正确地从后验分布中采样，因为它实际上就是从隐藏变量与数据变量的联合分布中抽取样本，然后丢弃与观测数据不符的样本；其中稍作节省的地方是，一旦发现一个不符的值，就立即停止从联合分布继续采样。不过，随着观测变量数量增加，以及这些变量可取的状态数增加，接受一个后验样本的总概率会迅速下降，所以实践中很少使用这种方法。

如果概率分布由无向图定义，那么即使没有任何观测变量，也不存在只遍历一次就能从先验分布中采样的策略。此时必须使用计算开销更大的技术，例如第 11.3 节将讨论的 Gibbs 采样。

除了从条件分布中采样，我们也可能需要从边缘分布中采样。如果已经有从联合分布 $p(\mathbf{u},\mathbf{v})$ 中采样的方法，那么只需忽略每个样本中 $\mathbf{v}$ 的取值，就能很容易地得到边缘分布 $p(\mathbf{u})$ 的样本。

讨论蒙特卡洛方法的著作很多。从统计推断的角度看，尤其值得关注的包括 Chen et al.（2001）、Gamerman（1997）、Gilks et al.（1996）、Liu（2001）、Neal（1996）以及 Robert and Casella（1999）。此外，Besag et al.（1995）、Brooks（1998）、Diaconis and Saloff-Coste（1998）、Jerrum and Sinclair（1996）、Neal（1993）、Tierney（1994）以及 Andrieu et al.（2003）的综述文章，提供了关于采样

<!-- pdf-page: 546 -->

<!-- join-previous-paragraph -->
方法在统计推断中应用的更多信息。

Robert and Casella（1999）总结了马尔可夫链蒙特卡洛算法的收敛诊断检验，Bishop and Nabney（2008）则给出了在机器学习中使用采样方法的一些实践指导。

## 11.1 基本采样算法

本节考虑一些简单的策略，用来从给定分布中生成随机样本。由于这些样本由计算机算法生成，它们实际上是伪随机数（pseudo-random numbers），也就是说，它们通过确定性的计算得到，但仍然必须通过适当的随机性检验。生成这类随机数涉及一些细微问题（Press et al., 1992），超出了本书的讨论范围。这里假定已有一个算法，能够生成在 $(0,1)$ 上均匀分布的伪随机数；事实上，大多数软件环境都内置了这一功能。

### 11.1.1 标准分布

首先考虑如何从简单的非均匀分布中生成随机数，并假定我们已经有均匀分布随机数的来源。设 $z$ 在区间 $(0,1)$ 上均匀分布，再用某个函数 $f(\cdot)$ 变换 $z$ 的值，令 $y=f(z)$。那么，$y$ 的分布满足

$$
p(y)=p(z)\left|\frac{\mathrm{d}z}{\mathrm{d}y}\right|
\tag{11.5}
$$

其中，在当前情形下有 $p(z)=1$。我们的目标是选择函数 $f(z)$，使所得的 $y$ 服从某个指定的目标分布 $p(y)$。对式（11.5）积分，得到

$$
z=h(y)\equiv\int_{-\infty}^{y}p(\widehat{y})\,\mathrm{d}\widehat{y}
\tag{11.6}
$$

它是 $p(y)$ 的不定积分。因此，$y=h^{-1}(z)$，所以需要用目标分布不定积分的反函数，对均匀分布的随机数进行变换。<span class="margin-reference">习题 11.2</span>图 11.2 展示了这一过程。

例如，考虑指数分布

$$
p(y)=\lambda\exp(-\lambda y)
\tag{11.7}
$$

其中 $0\leqslant y<\infty$。此时，式（11.6）的积分下限为 $0$，因此 $h(y)=1-\exp(-\lambda y)$。于是，如果用 $y=-\lambda^{-1}\ln(1-z)$ 变换均匀分布变量 $z$，所得 $y$ 就服从指数分布。

<!-- pdf-page: 547 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-2.png" alt="红色密度 p(y) 及蓝色积分函数 h(y)，利用反函数将均匀随机数变换为目标分布"><figcaption>图 11.2：用变换方法生成非均匀分布随机数的几何解释。$h(y)$ 是目标分布 $p(y)$ 的不定积分。如果对均匀分布随机变量 $z$ 作变换 $y=h^{-1}(z)$，那么 $y$ 就服从分布 $p(y)$。</figcaption></figure>

另一个可以使用变换方法的例子是柯西分布：

$$
p(y)=\frac{1}{\pi}\frac{1}{1+y^2}.
\tag{11.8}
$$

此时，不定积分的反函数可以用正切函数 $\tan$ 表示。<span class="margin-reference">习题 11.3</span>

很容易将这种方法推广到多个变量，此时需要使用变量变换的雅可比行列式，即

$$
p(y_1,\ldots,y_M)=p(z_1,\ldots,z_M)\left|\frac{\partial(z_1,\ldots,z_M)}{\partial(y_1,\ldots,y_M)}\right|.
\tag{11.9}
$$

作为变换方法的最后一个例子，我们考虑从高斯分布中生成样本的 Box–Muller 方法。首先，生成成对的均匀分布随机数 $z_1,z_2\in(-1,1)$，这可以通过对 $(0,1)$ 上的均匀分布变量作变换 $z\to2z-1$ 来实现。接着，丢弃所有不满足 $z_1^2+z_2^2\leqslant1$ 的随机数对。这样就得到了单位圆内的均匀分布，其概率密度为 $p(z_1,z_2)=1/\pi$，如图 11.3 所示。然后，对每一对 $z_1,z_2$ 计算

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-3.png" alt="蓝色正方形内的绿色单位圆，坐标为 z_1 和 z_2，范围均为负一至一"><figcaption>图 11.3：用于生成高斯分布随机数的 Box–Muller 方法，首先从单位圆内的均匀分布中生成样本。</figcaption></figure>

<!-- pdf-page: 548 -->

$$
y_1=z_1\left(\frac{-2\ln z_1}{r^2}\right)^{1/2}
\tag{11.10}
$$

$$
y_2=z_2\left(\frac{-2\ln z_2}{r^2}\right)^{1/2}
\tag{11.11}
$$

其中 $r^2=z_1^2+z_2^2$。于是，$y_1$ 与 $y_2$ 的联合分布为<span class="margin-reference">习题 11.4</span>

$$
\begin{aligned}
p(y_1,y_2)&=p(z_1,z_2)\left|\frac{\partial(z_1,z_2)}{\partial(y_1,y_2)}\right|\\
&=\left[\frac{1}{\sqrt{2\pi}}\exp(-y_1^2/2)\right]\left[\frac{1}{\sqrt{2\pi}}\exp(-y_2^2/2)\right]
\end{aligned}
\tag{11.12}
$$

因此，$y_1$ 和 $y_2$ 相互独立，并且都服从均值为零、方差为一的高斯分布。

如果 $y$ 服从均值为零、方差为一的高斯分布，那么 $\sigma y+\mu$ 就服从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布。要生成服从多元高斯分布、均值为 $\boldsymbol{\mu}$、协方差为 $\boldsymbol{\Sigma}$ 的向量值变量，可以利用形式为 $\boldsymbol{\Sigma}=\mathbf{L}\mathbf{L}^{\mathrm{T}}$ 的 Cholesky 分解（Press et al., 1992）。此时，如果 $\mathbf{z}$ 是一个向量值随机变量，各分量相互独立，且都服从均值为零、方差为一的高斯分布，那么 $\mathbf{y}=\boldsymbol{\mu}+\mathbf{L}\mathbf{z}$ 的均值就是 $\boldsymbol{\mu}$，协方差就是 $\boldsymbol{\Sigma}$。<span class="margin-reference">习题 11.5</span>

显然，变换技术能否奏效，取决于能否计算目标分布的不定积分，再求其反函数。这些操作只对少数简单分布可行，因此，要寻找更通用的策略，就必须转向其他方法。这里考虑两种技术，分别称为拒绝采样（rejection sampling）和重要性采样（importance sampling）。虽然它们主要适用于一元分布，不能直接处理复杂的高维问题，但仍是更通用采样策略的重要组成部分。

### 11.1.2 拒绝采样

在满足一定约束的条件下，拒绝采样框架能够从较复杂的分布中采样。我们先考虑一元分布，再讨论如何扩展到多个维度。

假设我们希望从分布 $p(z)$ 中采样，但它不属于前面考虑过的简单标准分布，直接从 $p(z)$ 中采样也很困难。再假设，对任意给定的 $z$，我们都能很容易地计算 $p(z)$，只是差一个归一化常数 $Z$；这种情况经常出现。也就是说，

$$
p(z)=\frac{1}{Z_p}\widetilde{p}(z)
\tag{11.13}
$$

其中 $\widetilde{p}(z)$ 很容易计算，但 $Z_p$ 未知。

为了应用拒绝采样，需要某个更简单的分布 $q(z)$，使我们能很容易地从中抽取样本；它有时称为提议分布（proposal distribution）。

<!-- pdf-page: 549 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-4.png" alt="拒绝采样的蓝色比较函数与红色未归一化密度，灰色区域中的样本被拒绝"><figcaption>图 11.4：拒绝采样方法从简单分布 $q(z)$ 中抽取样本；如果样本落在未归一化分布 $\widetilde{p}(z)$ 与缩放后的分布 $kq(z)$ 之间的灰色区域中，就将其拒绝。最终得到的样本服从 $p(z)$，即 $\widetilde{p}(z)$ 的归一化版本。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
接着，引入常数 $k$，选择其值，使所有 $z$ 都满足 $kq(z)\geqslant\widetilde{p}(z)$。函数 $kq(z)$ 称为比较函数（comparison function），图 11.4 对一元分布作了示意。拒绝采样的每一步都要生成两个随机数。首先，从分布 $q(z)$ 生成随机数 $z_0$。然后，从区间 $[0,kq(z_0)]$ 上的均匀分布生成随机数 $u_0$。这对随机数在函数 $kq(z)$ 曲线下方均匀分布。最后，如果 $u_0>\widetilde{p}(z_0)$，就拒绝该样本，否则保留 $u_0$。因此，当随机数对落入图 11.4 的灰色阴影区域时，就会被拒绝。留下的随机数对在 $\widetilde{p}(z)$ 曲线下方均匀分布，因此对应的 $z$ 值就服从所需分布 $p(z)$。<span class="margin-reference">习题 11.6</span>

最初的 $z$ 值从分布 $q(z)$ 中生成，然后以概率 $\widetilde{p}(z)/kq(z)$ 被接受，因此一个样本被接受的概率为

$$
\begin{aligned}
p(\mathrm{accept})&=\int\{\widetilde{p}(z)/kq(z)\}\,q(z)\,\mathrm{d}z\\
&=\frac{1}{k}\int\widetilde{p}(z)\,\mathrm{d}z.
\end{aligned}
\tag{11.14}
$$

因此，用这种方法时，被拒绝的点所占的比例，取决于未归一化分布 $\widetilde{p}(z)$ 曲线下方面积与 $kq(z)$ 曲线下方面积的比值。可见，在 $kq(z)$ 处处不小于 $\widetilde{p}(z)$ 的约束下，常数 $k$ 应尽可能小。

为说明拒绝采样的用法，考虑从伽马分布中采样的任务：

$$
\operatorname{Gam}(z\mid a,b)=\frac{b^az^{a-1}\exp(-bz)}{\Gamma(a)}
\tag{11.15}
$$

当 $a>1$ 时，它呈钟形，如图 11.5 所示。因此，柯西分布（11.8）是一个合适的提议分布，因为它同样呈钟形，而且可以用前面讨论的变换方法从中采样。我们需要对柯西分布稍作推广，以保证其值处处不小于伽马分布。这可以通过变换均匀随机变量 $y$ 来实现：令 $z=b\tan y+c$，得到的随机数服从如下分布。<span class="margin-reference">习题 11.7</span>

<!-- pdf-page: 550 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-5.png" alt="绿色伽马密度及其上方红色缩放柯西提议分布"><figcaption>图 11.5：绿色曲线表示式（11.15）给出的伽马分布，红色曲线表示缩放后的柯西提议分布。先从柯西分布中采样，再应用拒绝采样判据，就可以得到伽马分布的样本。</figcaption></figure>

$$
q(z)=\frac{k}{1+(z-c)^2/b^2}.
\tag{11.16}
$$

令 $c=a-1$、$b^2=2a-1$，并在仍满足 $kq(z)\geqslant\widetilde{p}(z)$ 的条件下，将常数 $k$ 取得尽可能小，就能得到最小的拒绝率。图 11.5 也展示了所得比较函数。

### 11.1.3 自适应拒绝采样

在许多适合考虑使用拒绝采样的场合，很难为包络分布 $q(z)$ 确定一个合适的解析形式。另一种方法是，根据计算得到的分布 $p(z)$ 的值，在运行过程中逐步构建包络函数（Gilks and Wild, 1992）。当 $p(z)$ 为对数凹函数，即 $\ln p(z)$ 的导数是关于 $z$ 的非增函数时，构建包络函数尤其简单。图 11.6 展示了如何构建合适的包络函数。

先在一组初始网格点上计算函数 $\ln p(z)$ 及其梯度，再用所得切线的交点构建包络函数。然后，从包络分布中抽取一个样本值。<span class="margin-reference">习题 11.9</span>这很容易做到，因为包络分布的对数是一系列

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-6.png" alt="红色对数密度及蓝色分段切线包络，标出三个网格点 z_1、z_2、z_3"><figcaption>图 11.6：对于对数凹分布，可以利用在一组网格点处计算的切线，构建用于拒绝采样的包络函数。如果某个样本点被拒绝，就将它加入网格点集合，并用来改进包络分布。</figcaption></figure>

<!-- pdf-page: 551 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-7.png" alt="绿色目标高斯密度与红色缩放高斯提议分布的比较"><figcaption>图 11.7：拒绝采样的一个示例：从同样为高斯分布的提议分布 $q(z)$ 中抽取样本，再利用拒绝采样，得到绿色曲线所示高斯分布 $p(z)$ 的样本。红色曲线表示缩放后的提议分布 $kq(z)$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
线性函数，所以包络分布本身是如下形式的分段指数分布：

$$
q(z)=k_i\lambda_i\exp\{-\lambda_i(z-z_{i-1})\}\qquad z_{i-1}<z\leqslant z_i.
\tag{11.17}
$$

抽得样本后，就可以应用通常的拒绝判据。如果样本被接受，它就是目标分布的一个样本。但如果样本被拒绝，就将它纳入网格点集合，计算一条新切线，从而改进包络函数。随着网格点数量增加，包络函数会越来越接近目标分布 $p(z)$，拒绝概率也会下降。

这一算法有一种变体，可以避免计算导数（Gilks, 1992）。自适应拒绝采样框架也可以扩展到非对数凹的分布：只需在每一步拒绝采样之后，再执行一步 Metropolis–Hastings 更新（将在第 11.2.2 节讨论），就得到了自适应拒绝 Metropolis 采样（Gilks et al., 1995）。

显然，要使拒绝采样具有实际价值，就要求比较函数接近目标分布，从而使拒绝率尽可能低。现在考察把拒绝采样用于高维空间时会发生什么。为便于说明，考虑一个略显人为的例子：我们希望从一个均值为零、协方差为 $\sigma_p^2\mathbf{I}$ 的多元高斯分布中采样，其中 $\mathbf{I}$ 是单位矩阵；为此，使用拒绝采样，而提议分布本身也是一个均值为零的高斯分布，协方差为 $\sigma_q^2\mathbf{I}$。显然，必须有 $\sigma_q^2\geqslant\sigma_p^2$，才存在某个 $k$ 使 $kq(z)\geqslant p(z)$。在 $D$ 维空间中，$k$ 的最优值为 $k=(\sigma_q/\sigma_p)^D$；图 11.7 展示了 $D=1$ 的情况。接受率等于 $p(z)$ 与 $kq(z)$ 下方体积的比值，由于两个分布都已经归一化，这个比值就是 $1/k$。因此，接受率随维数呈指数下降。即使 $\sigma_q$ 仅比 $\sigma_p$ 大百分之一，当 $D=1{,}000$ 时，接受率也仅约为 $1/20{,}000$。在这个示例中，比较函数已经很接近目标分布。对于更实际的例子，目标分布可能具有多个尖锐的峰，此时要找到好的提议分布和比较函数会极为困难。

<!-- pdf-page: 552 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-8.png" alt="红色目标分布 p(z)、绿色提议分布 q(z) 与蓝色函数 f(z)，示意重要性采样"><figcaption>图 11.8：重要性采样用于计算函数 $f(z)$ 关于分布 $p(z)$ 的期望，而直接从 $p(z)$ 中采样很困难。它改为从更简单的分布 $q(z)$ 中抽取样本 $\{z^{(l)}\}$，再用比值 $p(z^{(l)})/q(z^{(l)})$ 对求和中的相应项加权。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
此外，接受率随维数呈指数下降，是拒绝采样普遍具有的特性。虽然拒绝采样在一维或二维空间中可能很有用，但它不适合高维问题。不过，在更复杂的高维空间采样算法中，它仍然可以作为子程序发挥作用。

### 11.1.4 重要性采样

我们希望从复杂概率分布中采样，一个主要原因就是要计算形如式（11.1）的期望。重要性采样提供了直接近似期望的框架，但它本身并不提供从分布 $p(\mathbf{z})$ 中抽取样本的机制。

式（11.2）所给出的期望的有限求和近似，依赖于能够从分布 $p(\mathbf{z})$ 中抽取样本。现在假设，直接从 $p(\mathbf{z})$ 中采样不可行，但对于任意给定的 $\mathbf{z}$，都能很容易地计算 $p(\mathbf{z})$。一种过于简单的期望计算策略，是把 $\mathbf{z}$ 空间离散化为均匀网格，再把被积函数求和，写成

$$
\mathbb{E}[f]\simeq\sum_{l=1}^{L}p(\mathbf{z}^{(l)})f(\mathbf{z}^{(l)}).
\tag{11.18}
$$

这种方法有一个明显问题：求和项数随 $\mathbf{z}$ 的维数呈指数增长。此外，如前所述，我们关心的这类概率分布，往往将大部分概率质量集中在 $\mathbf{z}$ 空间中相对很小的区域里，因此均匀采样会非常低效；在高维问题中，只有极少数样本会对求和结果作出显著贡献。我们真正希望的是，让采样点落在 $p(\mathbf{z})$ 较大的区域，或者更理想地，落在乘积 $p(\mathbf{z})f(\mathbf{z})$ 较大的区域。

与拒绝采样一样，重要性采样也使用易于抽样的提议分布 $q(\mathbf{z})$，如图 11.8 所示。然后，我们可以把期望表示为关于

<!-- pdf-page: 553 -->

<!-- join-previous-paragraph -->
从 $q(\mathbf{z})$ 中抽取的样本 $\{\mathbf{z}^{(l)}\}$ 的有限求和：

$$
\begin{aligned}
\mathbb{E}[f]&=\int f(\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&=\int f(\mathbf{z})\frac{p(\mathbf{z})}{q(\mathbf{z})}q(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&\simeq\frac{1}{L}\sum_{l=1}^{L}\frac{p(\mathbf{z}^{(l)})}{q(\mathbf{z}^{(l)})}f(\mathbf{z}^{(l)}).
\end{aligned}
\tag{11.19}
$$

量 $r_l=p(\mathbf{z}^{(l)})/q(\mathbf{z}^{(l)})$ 称为重要性权重（importance weights），它们用于校正从错误分布采样所引入的偏差。注意，与拒绝采样不同，这里会保留生成的全部样本。

经常会出现这样的情况：分布 $p(\mathbf{z})$ 只能计算到相差一个归一化常数，即 $p(\mathbf{z})=\widetilde{p}(\mathbf{z})/Z_p$，其中 $\widetilde{p}(\mathbf{z})$ 很容易计算，而 $Z_p$ 未知。同样，我们可能希望使用具有相同性质的重要性采样分布 $q(\mathbf{z})=\widetilde{q}(\mathbf{z})/Z_q$。于是有

$$
\begin{aligned}
\mathbb{E}[f]&=\int f(\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&=\frac{Z_q}{Z_p}\int f(\mathbf{z})\frac{\widetilde{p}(\mathbf{z})}{\widetilde{q}(\mathbf{z})}q(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&\simeq\frac{Z_q}{Z_p}\frac{1}{L}\sum_{l=1}^{L}\widetilde{r}_lf(\mathbf{z}^{(l)}).
\end{aligned}
\tag{11.20}
$$

其中 $\widetilde{r}_l=\widetilde{p}(\mathbf{z}^{(l)})/\widetilde{q}(\mathbf{z}^{(l)})$。可以用同一组样本计算比值 $Z_p/Z_q$，结果为

$$
\begin{aligned}
\frac{Z_p}{Z_q}&=\frac{1}{Z_q}\int\widetilde{p}(\mathbf{z})\,\mathrm{d}\mathbf{z}=\int\frac{\widetilde{p}(\mathbf{z})}{\widetilde{q}(\mathbf{z})}q(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&\simeq\frac{1}{L}\sum_{l=1}^{L}\widetilde{r}_l
\end{aligned}
\tag{11.21}
$$

所以

$$
\mathbb{E}[f]\simeq\sum_{l=1}^{L}w_lf(\mathbf{z}^{(l)})
\tag{11.22}
$$

其中定义

$$
w_l=\frac{\widetilde{r}_l}{\sum_m\widetilde{r}_m}=\frac{\widetilde{p}(\mathbf{z}^{(l)})/q(\mathbf{z}^{(l)})}{\sum_m\widetilde{p}(\mathbf{z}^{(m)})/q(\mathbf{z}^{(m)})}.
\tag{11.23}
$$

与拒绝采样一样，重要性采样能否成功，关键取决于采样分布 $q(\mathbf{z})$ 与目标

<!-- pdf-page: 554 -->

<!-- join-previous-paragraph -->
分布 $p(\mathbf{z})$ 的匹配程度。如果 $p(\mathbf{z})f(\mathbf{z})$ 变化剧烈，而且很大一部分质量集中在 $\mathbf{z}$ 空间中相对很小的区域里——这种情况很常见——那么重要性权重集合 $\{r_l\}$ 可能由少数几个很大的权重主导，其余权重则相对微不足道。因此，有效样本量可能远小于表面上的样本量 $L$。如果没有任何样本落在 $p(\mathbf{z})f(\mathbf{z})$ 较大的区域，问题会更加严重。此时，即使期望的估计已经严重错误，$r_l$ 和 $r_lf(\mathbf{z}^{(l)})$ 的表观方差仍可能很小。因此，重要性采样的一个主要缺点是：它可能产生误差任意大的结果，却没有任何诊断迹象。这也说明了对采样分布 $q(\mathbf{z})$ 的一项关键要求：在 $p(\mathbf{z})$ 可能显著的区域，$q(\mathbf{z})$ 不应很小或为零。

对于用图模型定义的分布，可以用多种方式应用重要性采样。对离散变量，一种简单的方法称为均匀采样（uniform sampling）。有向图的联合分布由式（11.4）定义。要从该联合分布中得到一个样本，首先将证据集合中的变量 $\mathbf{z}_i$ 设为各自的观测值。然后，对其余每个变量，独立地从其所有可能取值上的均匀分布中采样。为确定样本 $\mathbf{z}^{(l)}$ 对应的权重，注意采样分布 $\widetilde{q}(\mathbf{z})$ 在 $\mathbf{z}$ 的所有可能选择上均匀分布，而且 $\widetilde{p}(\mathbf{z}\mid\mathbf{x})=\widetilde{p}(\mathbf{z})$，其中 $\mathbf{x}$ 表示被观测的变量子集；这个等式成立，是因为生成的每个样本 $\mathbf{z}$ 都必然与证据一致。因此，权重 $r_l$ 直接与 $p(\mathbf{z})$ 成正比。注意，各变量可以按任意顺序采样。如果后验分布远非均匀分布，这种方法的效果就可能很差，而这种情况在实践中很常见。

对上述方法的一种改进称为似然加权采样（likelihood weighted sampling）（Fung and Chang, 1990; Shachter and Peot, 1990），它以变量的祖先采样为基础。依次处理每个变量：如果它位于证据集合中，就直接设为其已观测到的值；如果不在证据集合中，就从条件分布 $p(\mathbf{z}_i\mid\mathrm{pa}_i)$ 中采样，其中条件变量取当前已经采样得到的值。所得样本 $\mathbf{z}$ 对应的权重为

$$
r(\mathbf{z})=\prod_{\mathbf{z}_i\notin\mathbf{e}}\frac{p(\mathbf{z}_i\mid\mathrm{pa}_i)}{p(\mathbf{z}_i\mid\mathrm{pa}_i)}\prod_{\mathbf{z}_i\in\mathbf{e}}\frac{p(\mathbf{z}_i\mid\mathrm{pa}_i)}{1}=\prod_{\mathbf{z}_i\in\mathbf{e}}p(\mathbf{z}_i\mid\mathrm{pa}_i).
\tag{11.24}
$$

还可以用自重要性采样（self-importance sampling）（Shachter and Peot, 1990）进一步扩展这种方法，持续更新重要性采样分布，使其反映当前估计的后验分布。

### 11.1.5 采样重要性重采样

第 11.1.2 节讨论的拒绝采样方法，能否成功，部分取决于能否为常数 $k$ 确定一个合适的值。对于许多分布对 $p(\mathbf{z})$ 和 $q(\mathbf{z})$，确定合适的

<!-- pdf-page: 555 -->

<!-- join-previous-paragraph -->
$k$ 值并不可行，因为任何大到足以保证包住目标分布的值，都会使接受率低到无法实际使用。

与拒绝采样一样，采样重要性重采样（sampling-importance-resampling，SIR）方法也使用采样分布 $q(\mathbf{z})$，但避免了确定常数 $k$ 的需要。这个方案包含两个阶段。第一阶段，从 $q(\mathbf{z})$ 抽取 $L$ 个样本 $\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(L)}$。第二阶段，利用式（11.23）构造权重 $w_1,\ldots,w_L$。最后，再从离散分布 $(\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(L)})$ 中抽取第二组 $L$ 个样本，各取值的概率由权重 $(w_1,\ldots,w_L)$ 给出。

所得的 $L$ 个样本只是近似服从 $p(\mathbf{z})$，但在 $L\to\infty$ 的极限下，分布会变得正确。为说明这一点，考虑一元情形，并注意重采样所得值的累积分布为

$$
\begin{aligned}
p(z\leqslant a)&=\sum_{l:z^{(l)}\leqslant a}w_l\\
&=\frac{\sum_l I(z^{(l)}\leqslant a)\widetilde{p}(z^{(l)})/q(z^{(l)})}{\sum_l\widetilde{p}(z^{(l)})/q(z^{(l)})}
\end{aligned}
\tag{11.25}
$$

其中 $I(\cdot)$ 是指示函数：自变量中的条件成立时等于 $1$，否则等于 $0$。取 $L\to\infty$ 的极限，并假设这些分布满足适当的正则条件，就可以用按原始采样分布 $q(z)$ 加权的积分代替求和：

$$
\begin{aligned}
p(z\leqslant a)&=\frac{\int I(z\leqslant a)\{\widetilde{p}(z)/q(z)\}q(z)\,\mathrm{d}z}{\int\{\widetilde{p}(z)/q(z)\}q(z)\,\mathrm{d}z}\\
&=\frac{\int I(z\leqslant a)\widetilde{p}(z)\,\mathrm{d}z}{\int\widetilde{p}(z)\,\mathrm{d}z}\\
&=\int I(z\leqslant a)p(z)\,\mathrm{d}z
\end{aligned}
\tag{11.26}
$$

这就是 $p(z)$ 的累积分布函数。再次可以看到，无须知道 $p(z)$ 的归一化常数。

当 $L$ 有限，并且给定初始样本集时，重采样所得的值只近似服从目标分布。与拒绝采样一样，采样分布 $q(\mathbf{z})$ 越接近目标分布 $p(\mathbf{z})$，近似就越好。当 $q(\mathbf{z})=p(\mathbf{z})$ 时，初始样本 $(\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(L)})$ 已服从目标分布，而权重为 $w_n=1/L$，因此重采样所得值也服从目标分布。

如果需要计算关于分布 $p(\mathbf{z})$ 的矩，可以

<!-- pdf-page: 556 -->

<!-- join-previous-paragraph -->
直接利用原始样本及其权重来计算，因为

$$
\begin{aligned}
\mathbb{E}[f(\mathbf{z})]&=\int f(\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}\\
&=\frac{\int f(\mathbf{z})[\widetilde{p}(\mathbf{z})/q(\mathbf{z})]q(\mathbf{z})\,\mathrm{d}\mathbf{z}}{\int[\widetilde{p}(\mathbf{z})/q(\mathbf{z})]q(\mathbf{z})\,\mathrm{d}\mathbf{z}}\\
&\simeq\sum_{l=1}^{L}w_lf(\mathbf{z}_l).
\end{aligned}
\tag{11.27}
$$

### 11.1.6 采样与 EM 算法

蒙特卡洛方法不仅为直接实现贝叶斯框架提供了机制，也可以在频率学派的方法中发挥作用，例如求最大似然解。特别是，对于无法解析执行 E 步的模型，可以用采样方法近似 EM 算法的 E 步。考虑一个具有隐藏变量 $\mathbf{Z}$、可见的（已观测）变量 $\mathbf{X}$ 以及参数 $\boldsymbol{\theta}$ 的模型。在 M 步中相对于 $\boldsymbol{\theta}$ 优化的函数，是完整数据对数似然的期望，写为

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\int p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{Z},\mathbf{X}\mid\boldsymbol{\theta})\,\mathrm{d}\mathbf{Z}.
\tag{11.28}
$$

可以利用采样方法，把这个积分近似为样本 $\{\mathbf{Z}^{(l)}\}$ 上的有限求和。这些样本从当前估计的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$ 中抽取，于是

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})\simeq\frac{1}{L}\sum_{l=1}^{L}\ln p(\mathbf{Z}^{(l)},\mathbf{X}\mid\boldsymbol{\theta}).
\tag{11.29}
$$

随后，在 M 步中照常优化 $Q$ 函数。这一过程称为蒙特卡洛 EM 算法。

如果已经为参数定义先验分布 $p(\boldsymbol{\theta})$，那么只需在执行 M 步之前，将 $\ln p(\boldsymbol{\theta})$ 加到函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 上，就能很容易地将这一方法扩展到寻找 $\boldsymbol{\theta}$ 后验分布的众数，也就是 MAP 估计。

如果考虑有限混合模型，并在每个 E 步中只抽取一个样本，就得到了蒙特卡洛 EM 算法的一个特例，称为随机 EM（stochastic EM）。这里，潜变量 $\mathbf{Z}$ 指明混合模型的 $K$ 个分量中，由哪个分量负责生成每个数据点。在 E 步中，从后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$ 中抽取一个 $\mathbf{Z}$ 的样本，其中 $\mathbf{X}$ 是数据集。这实际上是将每个数据点硬分配给某一个混合分量。在 M 步中，利用这个基于采样的后验分布近似，照常更新模型参数。

<!-- pdf-page: 557 -->

现在假设从最大似然方法转向完全贝叶斯处理，希望从参数向量 $\boldsymbol{\theta}$ 的后验分布中采样。原则上，我们希望从联合后验 $p(\boldsymbol{\theta},\mathbf{Z}\mid\mathbf{X})$ 中抽取样本，但假定这在计算上很困难。再假设，从完整数据下的参数后验 $p(\boldsymbol{\theta}\mid\mathbf{Z},\mathbf{X})$ 中采样相对容易。这启发了数据增广算法（data augmentation algorithm），它交替执行两个步骤：I 步（imputation step，填补步，类似 E 步）和 P 步（posterior step，后验步，类似 M 步）。

<aside class="procedure"><h3>IP 算法</h3>
<p><strong>I 步。</strong>我们希望从 $p(\mathbf{Z}\mid\mathbf{X})$ 中采样，但无法直接实现。于是，注意到以下关系：</p>
<p>$$
p(\mathbf{Z}\mid\mathbf{X})=\int p(\mathbf{Z}\mid\boldsymbol{\theta},\mathbf{X})p(\boldsymbol{\theta}\mid\mathbf{X})\,\mathrm{d}\boldsymbol{\theta}
\tag{11.30}
$$</p>
<p>因此，对于 $l=1,\ldots,L$，先从当前估计的 $p(\boldsymbol{\theta}\mid\mathbf{X})$ 中抽取样本 $\boldsymbol{\theta}^{(l)}$，再利用它从 $p(\mathbf{Z}\mid\boldsymbol{\theta}^{(l)},\mathbf{X})$ 中抽取样本 $\mathbf{Z}^{(l)}$。</p>
<p><strong>P 步。</strong>根据关系</p>
<p>$$
p(\boldsymbol{\theta}\mid\mathbf{X})=\int p(\boldsymbol{\theta}\mid\mathbf{Z},\mathbf{X})p(\mathbf{Z}\mid\mathbf{X})\,\mathrm{d}\mathbf{Z}
\tag{11.31}
$$</p>
<p>利用 I 步得到的样本 $\{\mathbf{Z}^{(l)}\}$，计算 $\boldsymbol{\theta}$ 后验分布的更新估计：</p>
<p>$$
p(\boldsymbol{\theta}\mid\mathbf{X})\simeq\frac{1}{L}\sum_{l=1}^{L}p(\boldsymbol{\theta}\mid\mathbf{Z}^{(l)},\mathbf{X}).
\tag{11.32}
$$</p>
<p>根据假设，在 I 步中从这个近似分布采样是可行的。</p>
</aside>

注意，我们在这里对参数 $\boldsymbol{\theta}$ 与隐藏变量 $\mathbf{Z}$ 作了一个多少有些人为的区分。从现在起，不再强调这一区分，而只关注从给定后验分布中抽取样本的问题。

## 11.2 马尔可夫链蒙特卡洛

上一节讨论了用拒绝采样和重要性采样计算函数期望的策略，也看到了它们的严重局限，尤其是在高维空间中。因此，本节转向一个十分通用且强大的框架，称为马尔可夫链蒙特卡洛（Markov chain Monte Carlo，MCMC）。它可以从很大一类分布中采样，

<!-- pdf-page: 558 -->

<!-- join-previous-paragraph -->
并且在样本空间维数增加时仍具有良好的扩展性。马尔可夫链蒙特卡洛方法起源于物理学（Metropolis and Ulam, 1949），直到 20 世纪 80 年代末才开始对统计学领域产生显著影响。

与拒绝采样和重要性采样一样，这里仍从提议分布中采样。不过，这一次要记录当前状态 $\mathbf{z}^{(\tau)}$，而提议分布 $q(\mathbf{z}\mid\mathbf{z}^{(\tau)})$ 依赖于这一状态，因此样本序列 $\mathbf{z}^{(1)},\mathbf{z}^{(2)},\ldots$ 构成一条马尔可夫链。<span class="margin-reference">第 11.2.1 节</span>同样，将 $p(\mathbf{z})$ 写成 $p(\mathbf{z})=\widetilde{p}(\mathbf{z})/Z_p$，并假定对于任意给定的 $\mathbf{z}$，都可以很容易地计算 $\widetilde{p}(\mathbf{z})$，尽管 $Z_p$ 的值可能未知。提议分布本身应选得足够简单，以便直接从中抽取样本。在算法的每一轮中，先从提议分布生成一个候选样本 $\mathbf{z}^\star$，再按适当的判据决定是否接受它。

在基本的 Metropolis 算法（Metropolis et al., 1953）中，假定提议分布是对称的，也就是说，对任意 $\mathbf{z}_A$ 与 $\mathbf{z}_B$，都有 $q(\mathbf{z}_A\mid\mathbf{z}_B)=q(\mathbf{z}_B\mid\mathbf{z}_A)$。候选样本以如下概率被接受：

$$
A(\mathbf{z}^\star,\mathbf{z}^{(\tau)})=\min\left(1,\frac{\widetilde{p}(\mathbf{z}^\star)}{\widetilde{p}(\mathbf{z}^{(\tau)})}\right).
\tag{11.33}
$$

实现时，可以从单位区间 $(0,1)$ 上的均匀分布抽取随机数 $u$，若 $A(\mathbf{z}^\star,\mathbf{z}^{(\tau)})>u$，就接受该样本。注意，如果从 $\mathbf{z}^{(\tau)}$ 移到 $\mathbf{z}^\star$ 会使 $p(\mathbf{z})$ 增大，那么候选点一定会被保留。

如果候选样本被接受，就令 $\mathbf{z}^{(\tau+1)}=\mathbf{z}^\star$；否则，丢弃候选点 $\mathbf{z}^\star$，将 $\mathbf{z}^{(\tau+1)}$ 设为 $\mathbf{z}^{(\tau)}$，再从分布 $q(\mathbf{z}\mid\mathbf{z}^{(\tau+1)})$ 中抽取另一个候选样本。这与拒绝采样不同，后者只是将被拒绝的样本丢弃。在 Metropolis 算法中，候选点被拒绝时，会把前一个样本再次纳入最终样本序列，因此样本可能出现多个副本。当然，在实际实现中，每个保留样本只需存储一份，同时记录一个整数权重，表示该状态出现了多少次。我们将看到，只要对于任意 $\mathbf{z}_A$ 与 $\mathbf{z}_B$，$q(\mathbf{z}_A\mid\mathbf{z}_B)$ 都为正，那么当 $\tau\to\infty$ 时，$\mathbf{z}^{(\tau)}$ 的分布就趋于 $p(\mathbf{z})$；这是充分条件，但不是必要条件。不过必须强调，序列 $\mathbf{z}^{(1)},\mathbf{z}^{(2)},\ldots$ 并不是从 $p(\mathbf{z})$ 中抽取的一组独立样本，因为相邻样本高度相关。如果希望得到独立样本，可以丢弃序列中的大部分，只保留每第 $M$ 个样本。当 $M$ 足够大时，留下的样本在实际应用中就可以视为相互独立。图 11.9 给出了一个简单示例：使用 Metropolis 算法从二维高斯分布中采样，其中提议分布为各向同性高斯分布。

通过考察一个具体例子的性质，可以进一步理解马尔可夫链蒙特卡洛算法的特点。这个例子就是简单的随机

<!-- pdf-page: 559 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-11/a-fig-11-9.png" alt="Metropolis 算法在黑色高斯椭圆中的路径，绿色为接受的移动，红色为拒绝的移动"><figcaption>图 11.9：使用 Metropolis 算法从高斯分布中采样的简单示例，椭圆表示该分布的一个标准差等高线。提议分布为标准差 $0.2$ 的各向同性高斯分布。被接受的移动用绿色线段表示，被拒绝的移动用红色线段表示。共生成 $150$ 个候选样本，其中 $43$ 个被拒绝。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
游走。考虑由整数组成的状态空间 $z$，其概率为

$$
p(z^{(\tau+1)}=z^{(\tau)})=0.5
\tag{11.34}
$$

$$
p(z^{(\tau+1)}=z^{(\tau)}+1)=0.25
\tag{11.35}
$$

$$
p(z^{(\tau+1)}=z^{(\tau)}-1)=0.25
\tag{11.36}
$$

其中 $z^{(\tau)}$ 表示第 $\tau$ 步的状态。如果初始状态为 $z^{(1)}=0$，那么根据对称性，时刻 $\tau$ 的状态期望也为零，即 $\mathbb{E}[z^{(\tau)}]=0$；同样，很容易看出 $\mathbb{E}[(z^{(\tau)})^2]=\tau/2$。<span class="margin-reference">习题 11.10</span>因此，在 $\tau$ 步之后，随机游走平均只走过了与 $\tau$ 的平方根成正比的距离。这种平方根依赖是随机游走行为的典型特征，表明随机游走探索状态空间的效率很低。我们将看到，设计马尔可夫链蒙特卡洛方法的一个核心目标，就是避免随机游走行为。

### 11.2.1 马尔可夫链

在更详细地讨论马尔可夫链蒙特卡洛方法之前，先进一步研究马尔可夫链的一些一般性质很有帮助。我们尤其关心：在什么条件下，马尔可夫链会收敛到所需分布。一阶马尔可夫链定义为一列随机变量 $\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(M)}$，对于 $m\in\{1,\ldots,M-1\}$，满足如下条件独立性质：

$$
p(\mathbf{z}^{(m+1)}\mid\mathbf{z}^{(1)},\ldots,\mathbf{z}^{(m)})=p(\mathbf{z}^{(m+1)}\mid\mathbf{z}^{(m)}).
\tag{11.37}
$$

当然，它可以表示为链状有向图，图 8.38 就给出了一个例子。随后，只要给出初始变量的概率分布 $p(\mathbf{z}^{(0)})$，以及后续变量的

<!-- pdf-page: 560 -->

<!-- join-previous-paragraph -->
条件概率，就可以指定这条马尔可夫链；这些条件概率用转移概率 $T_m(\mathbf{z}^{(m)},\mathbf{z}^{(m+1)})\equiv p(\mathbf{z}^{(m+1)}\mid\mathbf{z}^{(m)})$ 表示。如果转移概率对所有 $m$ 都相同，就称该马尔可夫链是齐次的（homogeneous）。

某个变量的边缘概率，可以用链中前一个变量的边缘概率表示为

$$
p(\mathbf{z}^{(m+1)})=\sum_{\mathbf{z}^{(m)}}p(\mathbf{z}^{(m+1)}\mid\mathbf{z}^{(m)})p(\mathbf{z}^{(m)}).
\tag{11.38}
$$

如果马尔可夫链的每一步都使某个分布保持不变，就称该分布关于这条马尔可夫链是不变的（invariant），或平稳的（stationary）。因此，对于转移概率为 $T(\mathbf{z}',\mathbf{z})$ 的齐次马尔可夫链，如果分布 $p^\star(\mathbf{z})$ 满足

$$
p^\star(\mathbf{z})=\sum_{\mathbf{z}'}T(\mathbf{z}',\mathbf{z})p^\star(\mathbf{z}').
\tag{11.39}
$$

它就是不变分布。注意，给定的马尔可夫链可能有不止一个不变分布。例如，如果转移概率对应于恒等变换，那么任何分布都会保持不变。

保证所需分布 $p(\mathbf{z})$ 不变的一个充分条件（但不是必要条件），是选择满足细致平衡（detailed balance）性质的转移概率。对于特定分布 $p^\star(\mathbf{z})$，细致平衡定义为

$$
p^\star(\mathbf{z})T(\mathbf{z},\mathbf{z}')=p^\star(\mathbf{z}')T(\mathbf{z}',\mathbf{z})
\tag{11.40}
$$

很容易看出，如果转移概率对于某个分布满足细致平衡，就会使该分布保持不变，因为

$$
\sum_{\mathbf{z}'}p^\star(\mathbf{z}')T(\mathbf{z}',\mathbf{z})=\sum_{\mathbf{z}'}p^\star(\mathbf{z})T(\mathbf{z},\mathbf{z}')=p^\star(\mathbf{z})\sum_{\mathbf{z}'}p(\mathbf{z}'\mid\mathbf{z})=p^\star(\mathbf{z}).
\tag{11.41}
$$

满足细致平衡的马尔可夫链称为可逆的（reversible）。

我们的目标是利用马尔可夫链从给定分布中采样。为此，可以构建一条使目标分布保持不变的马尔可夫链。不过，还必须要求：当 $m\to\infty$ 时，无论初始分布 $p(\mathbf{z}^{(0)})$ 如何选择，分布 $p(\mathbf{z}^{(m)})$ 都收敛到所需的不变分布 $p^\star(\mathbf{z})$。这个性质称为遍历性（ergodicity），此时的不变分布称为平衡分布（equilibrium distribution）。显然，遍历马尔可夫链只能有一个平衡分布。可以证明，只需对不变分布和转移概率施加较弱的限制，齐次马尔可夫链就具有遍历性（Neal, 1993）。

在实践中，我们常从一组“基本”转移 $B_1,\ldots,B_K$ 构造转移概率。一种方法是采用如下形式的混合分布：

$$
T(\mathbf{z}',\mathbf{z})=\sum_{k=1}^{K}\alpha_kB_k(\mathbf{z}',\mathbf{z})
\tag{11.42}
$$

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
