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
