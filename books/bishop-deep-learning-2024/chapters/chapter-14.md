# 第 14 章 采样

<aside class="chapter-guide"><strong>本章导读</strong><p>本章先介绍由均匀随机数构造样本、用样本估计期望，以及拒绝采样和重要性采样；随后讨论马尔可夫链蒙特卡罗方法，包括 Metropolis、Metropolis–Hastings 和 Gibbs 采样；最后介绍用于能量模型的朗之万采样。</p></aside>

<!-- pdf-page: 444 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/chapter-art.png" alt="第 14 章 Sampling 的彩色抽象章首页图">
  <p class="figure-translation">图内文字：Sampling → 采样。</p>
</figure>

在深度学习中，很多场合都需要从概率分布 $p(\mathbf z)$ 中生成变量 $\mathbf z$ 的合成实例。这里的 $\mathbf z$ 可能是一个标量，分布可能是一元高斯分布；也可能是一幅高分辨率图像，而 $p(\mathbf z)$ 是由深度神经网络定义的生成模型。生成这类实例的过程称为**采样**，也称**蒙特卡罗采样**。对于许多简单分布，可以用数值方法直接生成适当的样本；对于更复杂的分布，包括隐式定义的分布，可能需要更精巧的方法。本书约定把每一个具体生成的值称为一个*样本*，这与经典统计学把一组值称为“样本”的惯例不同。

本章聚焦于与深度学习最相关的采样问题。关于蒙特卡罗方法的一般性介绍，可参见 Gilks、Richardson 和 Spiegelhalter（1996）以及 Robert 和 Casella（1999）。

<!-- pdf-page: 445 -->

## 14.1 基本采样算法

本节探讨从给定分布生成随机样本的多种相对简单的方法。由于样本由计算机算法生成，它们实际上是*伪随机*的：虽然是确定性算法算出来的，却必须通过适当的随机性检验。这里假定我们已经有一种算法，能够生成在 $(0,1)$ 上均匀分布的伪随机数；事实上，多数软件环境内置了这种功能。

### 14.1.1 期望

有些应用直接关注样本本身，另一些应用则旨在计算相对于某一分布的期望。假设我们希望求函数 $f(\mathbf z)$ 在概率分布 $p(\mathbf z)$ 下的期望。$\mathbf z$ 的分量可以是离散变量、连续变量，或两者的组合。对于连续变量，期望定义为

$$
\mathbb E[f]=\int f(\mathbf z)p(\mathbf z)\,\mathrm d\mathbf z.\tag{14.1}
$$

对于离散变量，以求和代替积分。图 14.1 示意了单个连续变量的情形。这里假设这样的期望过于复杂，无法用解析方法精确求出。

采样方法的一般思路是从分布 $p(\mathbf z)$ 中独立地抽取一组样本 $\mathbf z^{(l)}$，其中 $l=1,\ldots,L$。于是，可用有限和近似式 (14.1) 的期望：

$$
\bar f=\frac{1}{L}\sum_{l=1}^{L}f\bigl(\mathbf z^{(l)}\bigr).\tag{14.2}
$$

如果 $\mathbf z^{(l)}$ 确实来自分布 $p(\mathbf z)$，那么 $\mathbb E[\bar f]=\mathbb E[f(\mathbf z)]$，因而估计量 $\bar f$ 的均值正确。

<figure id="fig-14-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-1.png" alt="函数 f(z) 与分布 p(z) 的示意曲线">
  <figcaption>图 14.1：函数 $f(z)$ 的示意图，其相对于分布 $p(z)$ 的期望有待计算。</figcaption>
  <p class="figure-translation">图内文字：$p(z)$ 为概率密度；$f(z)$ 为函数；$z$ 为横轴变量。</p>
</figure>

也可以写成以下形式：

<!-- pdf-page: 446 -->

$$
\mathbb E[f(\mathbf z)]\simeq\frac{1}{L}\sum_{l=1}^{L}f\bigl(\mathbf z^{(l)}\bigr),\tag{14.3}
$$

其中符号 $\simeq$ 表示右边是左边的无偏估计量，即对噪声分布取平均后，两边相等。

式 (14.2) 中估计量的方差为

$$
\operatorname{var}[\bar f]=\frac{1}{L}\mathbb E\bigl[(f-\mathbb E[f])^2\bigr],\tag{14.4}
$$

其中期望项是函数 $f(\mathbf z)$ 在分布 $p(\mathbf z)$ 下的方差。注意，方差随 $L$ 增大而线性下降，这一关系不依赖于 $\mathbf z$ 的维度；原则上，只用相对少量的样本 $\{\mathbf z^{(l)}\}$ 就可能获得较高精度。然而，问题在于这些样本可能并不独立，因此有效样本量可能远小于表面上的样本量。再看图 14.1：若 $f(z)$ 在 $p(z)$ 较大的区域较小，而在 $p(z)$ 较小的区域较大，则期望可能主要由低概率区域决定，意味着要达到足够的精度，需要相对大量的样本。

### 14.1.2 标准分布

现在假定已经有均匀分布随机数的来源，考虑如何生成来自简单非均匀分布的随机数。设 $z$ 在区间 $(0,1)$ 上均匀分布，我们用某个函数 $g(\cdot)$ 变换 $z$ 的取值，得到 $y=g(z)$。$y$ 的分布由下式决定（见第 2.4 节）：

$$
p(y)=p(z)\left|\frac{\mathrm dz}{\mathrm dy}\right|.\tag{14.5}
$$

在这里，$p(z)=1$。我们的目标是选择函数 $g(z)$，使所得的 $y$ 服从某个指定的目标分布 $p(y)$。对式 (14.5) 积分，得到

$$
z=\int_{-\infty}^{y}p(\hat y)\,\mathrm d\hat y\equiv h(y),\tag{14.6}
$$

**译注：** 式 (14.6) 按上下文整理了原书的排版；因积分下限固定，$h(y)$ 是累积分布函数。原书将它称为“不定积分”，以下保留其用语。

它是 $p(y)$ 的不定积分。因此，$y=h^{-1}(z)$：我们须用目标分布的不定积分的反函数，去变换均匀分布的随机数。图 14.2 给出了示意。

例如，考虑指数分布

$$
p(y)=\lambda\exp(-\lambda y),\tag{14.7}
$$

其中 $0\leqslant y<\infty$。此时式 (14.6) 的积分下限是 $0$，故 $h(y)=1-\exp(-\lambda y)$。因此，用 $y=-\lambda^{-1}\ln(1-z)$ 变换均匀分布变量 $z$，所得的 $y$ 就服从指数分布。

<!-- pdf-page: 447 -->

<figure id="fig-14-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-2.png" alt="逆变换法中概率密度与累计函数的几何示意">
  <figcaption>图 14.2：用变换法生成非均匀分布随机数的几何解释。$h(y)$ 是目标分布 $p(y)$ 的不定积分。将均匀分布的随机变量 $z$ 变换为 $y=h^{-1}(z)$ 后，$y$ 便服从 $p(y)$。</figcaption>
  <p class="figure-translation">图内文字：$p(y)$ 为目标概率密度；$h(y)$ 为其积分函数；$y$ 为横轴变量；$0$、$1$ 标示积分函数的范围。</p>
</figure>

另一个可用变换法处理的分布是柯西分布

$$
p(y)=\frac{1}{\pi}\frac{1}{1+y^2}.\tag{14.8}
$$

此时，不定积分的反函数可以用正切函数表示。

推广到多变量时，须使用变量变换的雅可比行列式（见第 2.4 节）：

$$
p(y_1,\ldots,y_M)=p(z_1,\ldots,z_M)\left|\frac{\partial(z_1,\ldots,z_M)}{\partial(y_1,\ldots,y_M)}\right|.\tag{14.9}
$$

作为变换法的最后一个例子，考虑从高斯分布生成样本的 Box–Muller 方法。首先，生成在 $(-1,1)$ 上均匀分布的随机数对 $z_1,z_2$；对 $(0,1)$ 上均匀分布的变量施加 $z\mapsto2z-1$ 即可做到。随后，舍弃不满足 $z_1^2+z_2^2\leqslant1$ 的数对。这样便得到单位圆内的均匀点分布，其密度为 $p(z_1,z_2)=1/\pi$，如图 14.3 所示。对每一对 $z_1,z_2$，计算

$$
y_1=z_1\left(\frac{-2\ln r^2}{r^2}\right)^{1/2},\tag{14.10}
$$

$$
y_2=z_2\left(\frac{-2\ln r^2}{r^2}\right)^{1/2},\tag{14.11}
$$

其中 $r^2=z_1^2+z_2^2$。于是，$y_1$ 和 $y_2$ 的联合分布为

$$
\begin{aligned}p(y_1,y_2)&=p(z_1,z_2)\left|\frac{\partial(z_1,z_2)}{\partial(y_1,y_2)}\right|\\&=\left[\frac{1}{\sqrt{2\pi}}\exp(-y_1^2/2)\right]\left[\frac{1}{\sqrt{2\pi}}\exp(-y_2^2/2)\right].\end{aligned}\tag{14.12}
$$

<!-- pdf-page: 448 -->

<figure id="fig-14-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-3.png" alt="单位圆内均匀分布的点用于 Box–Muller 方法">
  <figcaption>图 14.3：生成高斯分布随机数的 Box–Muller 方法，首先在单位圆内的均匀分布中生成样本。</figcaption>
  <p class="figure-translation">图内文字：$z_1$ 为横轴，$z_2$ 为纵轴；$-1$ 和 $1$ 标示坐标界限。</p>
</figure>

由此，$y_1$ 和 $y_2$ 相互独立，且各自服从均值为零、方差为一的高斯分布。

若 $y$ 服从均值为零、方差为一的高斯分布，那么 $\sigma y+\mu$ 服从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布。为了生成均值为 $\boldsymbol\mu$、协方差为 $\boldsymbol\Sigma$ 的多元高斯分布向量变量，可以使用 Cholesky 分解 $\boldsymbol\Sigma=\mathbf L\mathbf L^{\mathsf T}$（Deisenroth、Faisal 和 Ong，2020）。若随机向量 $\mathbf z$ 的各分量相互独立，且分别服从均值为零、方差为一的高斯分布，则 $\mathbf y=\boldsymbol\mu+\mathbf L\mathbf z$ 服从均值为 $\boldsymbol\mu$、协方差为 $\boldsymbol\Sigma$ 的高斯分布。

显然，变换法能否成功，取决于能否计算目标分布的不定积分并求其反函数。只有少数简单分布能做到这一点，因此我们需要寻求更一般的方法。这里考虑两种方法：**拒绝采样**和**重要性采样**。它们主要局限于一元分布，因而不能直接用于许多高维复杂问题，却是更一般方法的重要组成部分。

### 14.1.3 拒绝采样

拒绝采样框架允许我们在满足一定条件时从相对复杂的分布采样。先考虑一元分布，再讨论向多维情形的扩展。

假设我们希望从分布 $p(z)$ 中采样，它不是前述简单的标准分布之一，直接采样也很困难。再假设可以方便地计算任意 $z$ 处的 $p(z)$，只是差一个归一化常数 $Z$；这通常是可行的。于是

$$
p(z)=\frac{1}{Z_p}\tilde p(z),\tag{14.13}
$$

其中 $\tilde p(z)$ 易于计算，而 $Z_p$ 未知。

应用拒绝采样时，需要另一个较简单、易于采样的分布 $q(z)$，有时称为**提议分布**。再引入常数 $k$，使所有 $z$ 都满足 $kq(z)\geqslant\tilde p(z)$。函数 $kq(z)$ 称为**比较函数**，

<!-- pdf-page: 449 -->
<!-- join-previous-paragraph -->

图 14.4 给出了示意。

<figure id="fig-14-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-4.png" alt="拒绝采样比较函数与未归一化目标分布的曲线及拒绝区域">
  <figcaption>图 14.4：拒绝采样从简单分布 $q(z)$ 抽取样本；若样本落在未归一化分布 $\tilde p(z)$ 与缩放分布 $kq(z)$ 之间的灰色区域，就将其拒绝。留下的样本服从 $p(z)$，即 $\tilde p(z)$ 的归一化形式。</figcaption>
  <p class="figure-translation">图内文字：$kq(z)$ 为比较函数；$\tilde p(z)$ 为未归一化目标函数；$z_0$ 为候选样本；$u_0$ 为辅助均匀随机数；$z$ 为横轴。</p>
</figure>

图 14.4 展示的是一元分布。拒绝采样器的每一步要生成两个随机数。先从 $q(z)$ 生成 $z_0$，再从区间 $[0,kq(z_0)]$ 上的均匀分布生成 $u_0$。这对随机数在曲线 $kq(z)$ 下方呈均匀分布。最后，如果 $u_0>\tilde p(z_0)$，就拒绝该样本；否则保留它。因此，落在图 14.4 灰色阴影区域中的点对会被拒绝。剩下的点对在 $\tilde p(z)$ 曲线下方均匀分布，相应的 $z$ 值也就按所需的 $p(z)$ 分布。

原始 $z$ 值来自分布 $q(z)$，随后以概率 $\tilde p(z)/kq(z)$ 被接受，因此样本被接受的概率是

$$
\begin{aligned}p(\mathrm{accept})&=\int\left\{\frac{\tilde p(z)}{kq(z)}\right\}q(z)\,\mathrm dz\\&=\frac{1}{k}\int\tilde p(z)\,\mathrm dz.\end{aligned}\tag{14.14}
$$

所以，被拒绝点所占的比例取决于 $\tilde p(z)$ 曲线下面积与 $kq(z)$ 曲线下面积之比。由此可见，须在处处满足 $kq(z)\geqslant\tilde p(z)$ 的前提下尽量减小 $k$。

以从伽马分布采样为例：

$$
\operatorname{Gam}(z\mid a,b)=\frac{b^az^{a-1}\exp(-bz)}{\Gamma(a)}.\tag{14.15}
$$

当 $a>1$ 时，该分布呈钟形，如图 14.5 所示。柯西分布 (14.8) 也是钟形的，而且可以用前述变换法从中采样，因此适合作为提议分布。我们需要稍微推广柯西分布，使它在任何地方都不会低于伽马分布。对均匀随机变量 $y$ 施加 $z=b\tan y+c$，可得到服从下式分布的随机数：

$$
q(z)=\frac{k}{1+(z-c)^2/b^2}.\tag{14.16}
$$

**译注：** 原书式 (14.16) 的 $k$ 与比较函数的缩放常数重名；任意 $k$ 时右边也不是归一化密度。若 $b>0$，标准的位置尺度柯西密度为 $1/[\pi b\{1+((z-c)/b)^2\}]$，可由 $z=b\tan[\pi(u-1/2)]+c$、$u\sim\mathcal U(0,1)$ 生成。习题 14.8 的角度区间另有对应疑点。

<!-- pdf-page: 450 -->

<figure id="fig-14-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-5.png" alt="绿色伽马密度曲线和红色缩放柯西提议曲线">
  <figcaption>图 14.5：绿色曲线为式 (14.15) 给出的伽马分布，红色曲线为缩放后的柯西提议分布。可以先从柯西分布采样，再应用拒绝采样准则，从而得到伽马分布的样本。</figcaption>
  <p class="figure-translation">图内文字：$p(z)$ 为纵轴概率密度，$z$ 为横轴变量。</p>
</figure>

令 $c=a-1$、$b^2=2a-1$，并在仍满足 $kq(z)\geqslant\tilde p(z)$ 的条件下取尽可能小的 $k$，就能使拒绝率最低。图 14.5 还画出了所得比较函数。

### 14.1.4 自适应拒绝采样

在许多想要应用拒绝采样的情形中，很难为包络分布 $q(z)$ 确定合适的解析形式。另一种做法是根据测得的 $p(z)$ 值，动态构造包络函数（Gilks 和 Wild，1992）。当 $p(z)$ 为对数凹分布时，构造包络函数尤为直接；换言之，$\ln p(z)$ 的导数是 $z$ 的非增函数。图 14.6 示意了合适的包络函数是如何构造的。

首先在一组初始网格点上计算 $\ln p(z)$ 及其梯度，再利用所得切线的交点构造包络函数。然后从包络分布中抽取样本。这很容易实现，因为包络分布的对数由一系列线性函数组成，所以包络分布本身是一种如下形式的分段指数分布：

$$
q(z)=k_i\lambda_i\exp\{-\lambda_i(z-z_{i-1})\},\qquad z_{i-1}<z\leqslant z_i.\tag{14.17}
$$

抽取样本后，即可应用通常的拒绝准则。如果样本被接受，它就是目标分布的一次抽样；如果被拒绝，则把它加入网格点集合，计算一条新切线，以此改进包络函数。随着网格点增多，包络函数会更接近目标分布 $p(z)$，拒绝概率随之降低。

该算法还有一种无需计算导数的变体（Gilks，1992）。自适应拒绝采样框架也可以推广到非对数凹分布：只需在每次拒绝采样

<!-- pdf-page: 451 -->
<!-- join-previous-paragraph -->

步骤后接一个 Metropolis–Hastings 步骤（将在第 14.2.3 节讨论），便得到**自适应拒绝 Metropolis 采样**（Gilks、Best 和 Tan，1995）。

<figure id="fig-14-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-6.png" alt="对数凹曲线及在网格点上的切线构成包络">
  <figcaption>图 14.6：在拒绝采样中，如果分布是对数凹的，可以利用一组网格点处的切线构造包络函数。若某样本点被拒绝，则将其加入网格点集合，用于改进包络分布。</figcaption>
  <p class="figure-translation">图内文字：$\ln p(z)$ 为纵轴函数值；$z$ 为横轴；$z_1,z_2,z_3$ 为网格点。</p>
</figure>

<figure id="fig-14-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-7.png" alt="高斯目标分布和较宽的缩放高斯提议分布曲线">
  <figcaption>图 14.7：说明拒绝采样局限性的例子。绿色曲线为待采样的高斯分布 $p(z)$；用同样为高斯分布的提议分布 $q(z)$ 进行拒绝采样，红色曲线是其缩放形式 $kq(z)$。</figcaption>
  <p class="figure-translation">图内文字：$p(z)$ 为纵轴概率密度；$z$ 为横轴变量。</p>
</figure>

要使拒绝采样具有实用价值，比较函数须接近目标分布，以尽量降低拒绝率。再来看在高维空间中应用拒绝采样会怎样。考虑一个略显人为的例子：我们想从均值为零、协方差为 $\sigma_p^2\mathbf I$ 的多元高斯分布采样，其中 $\mathbf I$ 是单位矩阵；所用提议分布本身也是均值为零、协方差为 $\sigma_q^2\mathbf I$ 的高斯分布。显然，必须有 $\sigma_q^2\geqslant\sigma_p^2$，才能找到使 $kq(\mathbf z)\geqslant p(\mathbf z)$ 的 $k$。在 $D$ 维空间中，$k$ 的最佳值为 $(\sigma_q/\sigma_p)^D$；图 14.7 画出了 $D=1$ 的情形。接受率等于 $p(\mathbf z)$ 和 $kq(\mathbf z)$ 曲线下体积之比；由于两个分布都已归一化，它就是 $1/k$。因此，接受率随维度呈指数下降。即使 $\sigma_q$ 仅比 $\sigma_p$ 大 $1\%$，当 $D=1{,}000$ 时，接受率也大约只有 $1/20{,}000$。在这个示例中，比较函数已经接近目标分布。对于更实际的例子，目标分布可能有多个模态和尖锐峰值，寻找好的

<!-- pdf-page: 452 -->
<!-- join-previous-paragraph -->

提议分布及比较函数将极其困难。

此外，接受率随维度呈指数下降是拒绝采样的普遍特性。拒绝采样在一维或二维可能有用，却不适合高维问题。不过，它可以作为更复杂的高维采样算法中的一个子程序。

### 14.1.5 重要性采样

希望从复杂概率分布采样的一个原因，是要计算式 (14.1) 那样的期望。**重要性采样**提供了直接近似期望的框架，但它本身并不提供从分布 $p(\mathbf z)$ 抽取样本的机制。

式 (14.2) 给出的期望有限和近似依赖于能否从 $p(\mathbf z)$ 采样。若直接从 $p(\mathbf z)$ 采样不可行，但容易计算任意给定 $\mathbf z$ 处的 $p(\mathbf z)$，一个简单的期望计算策略是把 $\mathbf z$ 空间离散为均匀网格，再用下式求和：

$$
\mathbb E[f]\simeq\sum_{l=1}^{L}p\bigl(\mathbf z^{(l)}\bigr)f\bigl(\mathbf z^{(l)}\bigr).\tag{14.18}
$$

这一做法的明显问题是，求和项数随 $\mathbf z$ 的维度呈指数增长。而且，正如前面指出的，我们感兴趣的概率分布，其概率质量往往集中在 $\mathbf z$ 空间中的较小区域。因此在高维问题中，均匀采样效率很低，只有很少的样本会对求和有显著贡献。我们真正想选的是 $p(\mathbf z)$ 较大的区域，理想情况下是乘积 $p(\mathbf z)f(\mathbf z)$ 较大的区域中的采样点。

与拒绝采样一样，重要性采样也基于易于采样的提议分布 $q(\mathbf z)$，如图 14.8 所示。于是，期望可表示为从 $q(\mathbf z)$ 抽取的样本 $\{\mathbf z^{(l)}\}$ 上的有限和：

$$
\begin{aligned}\mathbb E[f]&=\int f(\mathbf z)p(\mathbf z)\,\mathrm d\mathbf z\\&=\int f(\mathbf z)\frac{p(\mathbf z)}{q(\mathbf z)}q(\mathbf z)\,\mathrm d\mathbf z\\&\simeq\frac{1}{L}\sum_{l=1}^{L}\frac{p(\mathbf z^{(l)})}{q(\mathbf z^{(l)})}f(\mathbf z^{(l)}).\end{aligned}\tag{14.19}
$$

量 $r_l=p(\mathbf z^{(l)})/q(\mathbf z^{(l)})$ 称为**重要性权重**，用于修正从非目标分布采样引入的偏差。与拒绝采样不同，所有生成的样本都会被保留。

很多时候只能计算到归一化常数的 $p(\mathbf z)=\tilde p(\mathbf z)/Z_p$，其中 $\tilde p(\mathbf z)$ 易于计算，而 $Z_p$ 未知。

<!-- pdf-page: 453 -->

<figure id="fig-14-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-8.png" alt="目标分布、提议分布和待求期望函数的曲线">
  <figcaption>图 14.8：重要性采样用于计算函数 $f(z)$ 在难以直接采样的分布 $p(z)$ 下的期望。样本 $\{z^{(l)}\}$ 改从较简单的 $q(z)$ 中抽取，并用比值 $p(z^{(l)})/q(z^{(l)})$ 为求和项加权。</figcaption>
  <p class="figure-translation">图内文字：$p(z)$ 为目标分布；$q(z)$ 为提议分布；$f(z)$ 为待求期望的函数；$z$ 为横轴。</p>
</figure>

同样，也可能希望使用具有相同性质的重要性采样分布 $q(\mathbf z)=\tilde q(\mathbf z)/Z_q$。那么

$$
\begin{aligned}\mathbb E[f]&=\int f(\mathbf z)p(\mathbf z)\,\mathrm d\mathbf z\\&=\frac{Z_q}{Z_p}\int f(\mathbf z)\frac{\tilde p(\mathbf z)}{\tilde q(\mathbf z)}q(\mathbf z)\,\mathrm d\mathbf z\\&\simeq\frac{Z_q}{Z_p}\frac{1}{L}\sum_{l=1}^{L}\tilde r_l f(\mathbf z^{(l)}),\end{aligned}\tag{14.20}
$$

其中 $\tilde r_l=\tilde p(\mathbf z^{(l)})/\tilde q(\mathbf z^{(l)})$。用同一组样本可求出 $Z_p/Z_q$ 的估计值：

$$
\begin{aligned}\frac{Z_p}{Z_q}&=\frac{1}{Z_q}\int\tilde p(\mathbf z)\,\mathrm d\mathbf z=\int\frac{\tilde p(\mathbf z)}{\tilde q(\mathbf z)}q(\mathbf z)\,\mathrm d\mathbf z\\&\simeq\frac{1}{L}\sum_{l=1}^{L}\tilde r_l.\end{aligned}\tag{14.21}
$$

因此，式 (14.20) 中的期望可写为加权和：

$$
\mathbb E[f]\simeq\sum_{l=1}^{L}w_l f(\mathbf z^{(l)}),\tag{14.22}
$$

其中定义

$$
w_l=\frac{\tilde r_l}{\sum_m\tilde r_m}=\frac{\tilde p(\mathbf z^{(l)})/q(\mathbf z^{(l)})}{\sum_m\tilde p(\mathbf z^{(m)})/q(\mathbf z^{(m)})}.\tag{14.23}
$$

注意，$\{w_l\}$ 是非负数，且总和为一。

与拒绝采样类似，重要性采样能否成功，关键在于采样分布 $q(\mathbf z)$ 与目标分布 $p(\mathbf z)$ 是否足够匹配。假如 $p(\mathbf z)f(\mathbf z)$ 变化剧烈，且其质量有很大一部分集中在 $\mathbf z$ 空间中相对较小的区域——这种情况很常见——那么

<!-- pdf-page: 454 -->
<!-- join-previous-paragraph -->

重要性权重集合 $\{r_l\}$ 就可能被少数较大的权重主导，其余权重则相对无足轻重。这样，有效样本量可能远小于表面上的 $L$。若没有样本落入 $p(\mathbf z)f(\mathbf z)$ 较大的区域，问题会更严重：即使 $r_l$ 和 $r_lf(\mathbf z^{(l)})$ 的表面方差可能很小，期望估计也可能严重错误。因此，重要性采样的一大缺点是可能产生任意大的误差，却没有诊断信号。这也凸显了对采样分布 $q(\mathbf z)$ 的一项关键要求：在 $p(\mathbf z)$ 可能显著的区域，它不能很小，更不能为零。

### 14.1.6 采样—重要性—重采样

第 14.1.3 节讨论的拒绝采样方法能否成功，部分取决于能否选出合适的常数 $k$。对于许多分布对 $p(\mathbf z)$ 和 $q(\mathbf z)$，实际上无法选出合适的 $k$：大到足以确保包住目标分布的值，又会导致接受率低得不可用。

**采样—重要性—重采样**同样使用采样分布 $q(\mathbf z)$，但不必确定常数 $k$。该方案分两个阶段。第一阶段，从 $q(\mathbf z)$ 抽取 $L$ 个样本 $\mathbf z^{(1)},\ldots,\mathbf z^{(L)}$。第二阶段，用式 (14.23) 构造权重 $w_1,\ldots,w_L$。最后，从以 $\mathbf z^{(1)},\ldots,\mathbf z^{(L)}$ 为取值、以 $w_1,\ldots,w_L$ 为概率的离散分布中，再抽取 $L$ 个样本。

所得的 $L$ 个样本仅近似服从 $p(\mathbf z)$，但当 $L\to\infty$ 时分布趋于正确。为说明这一点，考虑一元情形。重采样值的累积分布为

$$
\begin{aligned}p(z\leqslant a)&=\sum_{l:z^{(l)}\leqslant a}w_l\\&=\frac{\sum_l I(z^{(l)}\leqslant a)\tilde p(z^{(l)})/q(z^{(l)})}{\sum_l\tilde p(z^{(l)})/q(z^{(l)})},\end{aligned}\tag{14.24}
$$

其中 $I(\cdot)$ 是指示函数，参数为真时取 $1$，否则取 $0$。令 $L\to\infty$，并假定分布满足适当的正则条件，就可以把求和替换为按原始

<!-- pdf-page: 455 -->
<!-- join-previous-paragraph -->

采样分布 $q(z)$ 加权的积分：

$$
\begin{aligned}p(z\leqslant a)&=\frac{\int I(z\leqslant a)\{\tilde p(z)/q(z)\}q(z)\,\mathrm dz}{\int\{\tilde p(z)/q(z)\}q(z)\,\mathrm dz}\\&=\frac{\int I(z\leqslant a)\tilde p(z)\,\mathrm dz}{\int\tilde p(z)\,\mathrm dz}\\&=\int I(z\leqslant a)p(z)\,\mathrm dz,\end{aligned}\tag{14.25}
$$

这就是 $p(z)$ 的累积分布函数。再次可见，无须知道 $p(z)$ 的归一化常数。

当 $L$ 有限、且初始样本集已给定时，重采样所得的值仅近似来自目标分布。与拒绝采样一样，$q(z)$ 越接近 $p(z)$，近似就越好。若 $q(z)=p(z)$，初始样本 $z^{(1)},\ldots,z^{(L)}$ 已有目标分布，且权重 $w_n=1/L$，所以重采样后的值也服从目标分布。

如需计算 $p(z)$ 下的矩，可以直接结合原始样本和权重求值，因为

$$
\begin{aligned}\mathbb E[f(z)]&=\int f(z)p(z)\,\mathrm dz\\&=\frac{\int f(z)[\tilde p(z)/q(z)]q(z)\,\mathrm dz}{\int[\tilde p(z)/q(z)]q(z)\,\mathrm dz}\\&\simeq\sum_{l=1}^{L}w_l f(z_l).\end{aligned}\tag{14.26}
$$

**译注：** 式 (14.26) 的 $z_l$ 对应前文的第 $l$ 个样本 $z^{(l)}$；原书此处更换了写法。

## 14.2 马尔可夫链蒙特卡罗

上一节讨论了通过拒绝采样和重要性采样计算函数期望的策略，也看到它们在高维空间中受到严重限制。因此，本节转向一种非常一般而强大的框架——**马尔可夫链蒙特卡罗**（Markov chain Monte Carlo，MCMC）。它允许从一大类分布中采样，并且随样本空间维度增加仍有较好的扩展性。MCMC 方法起源于物理学（Metropolis 和 Ulam，1949），但直到

<!-- pdf-page: 456 -->
<!-- join-previous-paragraph -->

20 世纪 80 年代末才开始对统计学领域产生显著影响。

与拒绝采样和重要性采样一样，这里仍从提议分布采样。但这一次，我们记录当前状态 $\mathbf z^{(\tau)}$，并让提议分布 $q(\mathbf z\mid\mathbf z^{(\tau)})$ 以当前状态为条件，因而样本序列 $\mathbf z^{(1)},\mathbf z^{(2)},\ldots$ 构成马尔可夫链（见第 14.2.2 节）。仍令 $p(\mathbf z)=\tilde p(\mathbf z)/Z_p$，并假设可方便地计算任意给定 $\mathbf z$ 处的 $\tilde p(\mathbf z)$，尽管 $Z_p$ 可能未知。提议分布应足够简单，使得直接从中采样并不困难。在算法的每个循环中，先从提议分布生成候选样本 $\mathbf z^\star$，再按照适当的准则决定是否接受。

### 14.2.1 Metropolis 算法

在基本的 Metropolis 算法（Metropolis 等，1953）中，假定提议分布对称，即对任意 $\mathbf z_A,\mathbf z_B$，都有 $q(\mathbf z_A\mid\mathbf z_B)=q(\mathbf z_B\mid\mathbf z_A)$。于是，以如下概率接受候选样本：

$$
A(\mathbf z^\star,\mathbf z^{(\tau)})=\min\left(1,\frac{\tilde p(\mathbf z^\star)}{\tilde p(\mathbf z^{(\tau)})}\right).\tag{14.27}
$$

可从单位区间 $(0,1)$ 上均匀抽取随机数 $u$，若 $A(\mathbf z^\star,\mathbf z^{(\tau)})>u$，则接受候选样本。注意，如果从 $\mathbf z^{(\tau)}$ 到 $\mathbf z^\star$ 使 $p(\mathbf z)$ 增大，候选点必然被保留。

若接受候选样本，则 $\mathbf z^{(\tau+1)}=\mathbf z^\star$；否则丢弃 $\mathbf z^\star$，令 $\mathbf z^{(\tau+1)}=\mathbf z^{(\tau)}$，再从 $q(\mathbf z\mid\mathbf z^{(\tau+1)})$ 抽取另一个候选样本。这与直接丢弃拒绝样本的拒绝采样不同。在 Metropolis 算法中，拒绝候选点时，前一个样本仍进入最终样本列表，于是同一样本可能出现多次。实际实现中当然只需保存每个保留样本的一份副本，以及记录该状态出现次数的整数权重。后面将看到，若任意 $\mathbf z_A,\mathbf z_B$ 的 $q(\mathbf z_A\mid\mathbf z_B)$ 都为正（这是充分而非必要条件），则当 $\tau\to\infty$ 时，$\mathbf z^{(\tau)}$ 的分布趋于 $p(\mathbf z)$。但必须强调，序列 $\mathbf z^{(1)},\mathbf z^{(2)},\ldots$ 并非来自 $p(\mathbf z)$ 的独立样本，因为相邻样本高度相关。若需要独立样本，可以丢弃序列中的大部分，只保留每第 $M$ 个样本。当 $M$ 足够大时，保留的样本在实际用途上可视为独立。算法 14.1 汇总了 Metropolis 算法。图 14.9 给出一个简单示例：用各向同性高斯提议分布，通过 Metropolis 算法从二维高斯分布采样。

进一步了解 MCMC 算法的性质，可以考察一个具体例子，即简单随机

<!-- pdf-page: 457 -->
<!-- join-previous-paragraph -->

游走。

**算法 14.1：Metropolis 采样**

```text
输入：
  未归一化分布 p̃(z)
  提议分布 q(z|ẑ)
  初始状态 z⁽⁰⁾
  迭代次数 T
输出：z ∼ p̃(z)

z_prev ← z⁽⁰⁾
// 迭代消息传递
for τ ∈ {1,…,T} do
  z* ∼ q(z|z_prev)
  // 从提议分布采样
  u ∼ U(0,1)
  // 从均匀分布采样
  if p̃(z*) / p̃(z_prev)
     > u then
    z_prev ← z*
    // z⁽τ⁾ = z*
  else
    z_prev ← z_prev
    // z⁽τ⁾ = z⁽τ⁻¹⁾
  end if
end for
return z_prev
// z⁽ᵀ⁾
```

**译注：** 算法 14.1 的输出在原书写为 $z\sim\tilde p(z)$；$\tilde p$ 尚未归一化，链的目标平稳分布应为归一化后的 $p(z)$。代码中的“迭代消息传递”是原书注释的直译。

考虑由整数组成的状态空间 $z$，其转移概率为

$$
p(z^{(\tau+1)}=z^{(\tau)})=0.5,\tag{14.28}
$$

$$
p(z^{(\tau+1)}=z^{(\tau)}+1)=0.25,\tag{14.29}
$$

$$
p(z^{(\tau+1)}=z^{(\tau)}-1)=0.25,\tag{14.30}
$$

其中 $z^{(\tau)}$ 是第 $\tau$ 步的状态。若初始状态 $z^{(0)}=0$，由对称性可知第 $\tau$ 步状态的期望也为零，即 $\mathbb E[z^{(\tau)}]=0$；同样容易看出 $\mathbb E[(z^{(\tau)})^2]=\tau/2$。因此，经过 $\tau$ 步，随机游走的平均移动距离仅与 $\sqrt\tau$ 成正比。这种平方根依赖关系是随机游走的典型特征，说明随机游走探索状态空间的效率很低。后面将看到，设计 MCMC 方法的一项核心目标就是避免随机游走行为。

### 14.2.2 马尔可夫链

在更详细地讨论 MCMC 方法之前，有必要了解马尔可夫链的一般性质。特别是，我们要问：马尔可夫链在什么条件下会收敛到目标分布？一阶

<!-- pdf-page: 458 -->
<!-- join-previous-paragraph -->

马尔可夫链定义为一系列随机变量 $\mathbf z^{(1)},\ldots,\mathbf z^{(M)}$，满足以下条件独立性质：对 $m\in\{1,\ldots,M-1\}$，

$$
p(\mathbf z^{(m+1)}\mid\mathbf z^{(1)},\ldots,\mathbf z^{(m)})=p(\mathbf z^{(m+1)}\mid\mathbf z^{(m)}),\tag{14.31}
$$

<figure id="fig-14-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-9.png" alt="Metropolis 算法在二维高斯分布中的接受与拒绝轨迹">
  <figcaption>图 14.9：用 Metropolis 算法从高斯分布采样的简单示例。椭圆是其一个标准差处的等高线。提议分布是标准差为 $0.2$ 的各向同性高斯分布。绿色线段表示被接受的步骤，红色线段表示被拒绝的步骤。共生成 $150$ 个候选样本，其中 $43$ 个被拒绝。</figcaption>
  <p class="figure-translation">图内数字 $0$ 至 $3$ 为横、纵坐标刻度；绿色为接受的移动，红色为拒绝的移动。</p>
</figure>

它可以表示为链式有向图模型（见图 11.29）。指定初始变量的概率分布 $p(\mathbf z^{(0)})$，再给出后续变量的条件分布，即转移概率 $T_m(\mathbf z^{(m)},\mathbf z^{(m+1)})\equiv p(\mathbf z^{(m+1)}\mid\mathbf z^{(m)})$，就能确定马尔可夫链。如果转移概率对所有 $m$ 都相同，就称马尔可夫链是**齐次的**。

链中某变量的边缘概率可用其前一变量的边缘概率表示：

$$
p(\mathbf z^{(m+1)})=\int p(\mathbf z^{(m+1)}\mid\mathbf z^{(m)})p(\mathbf z^{(m)})\,\mathrm d\mathbf z^{(m)},\tag{14.32}
$$

对于离散变量，以求和代替积分。如果链中的每一步都使某一分布保持不变，就称该分布对于此马尔可夫链是**不变的**或**平稳的**。因此，对于转移概率为 $T(\mathbf z',\mathbf z)$ 的齐次马尔可夫链，若

$$
p^\star(\mathbf z)=\int T(\mathbf z',\mathbf z)p^\star(\mathbf z')\,\mathrm d\mathbf z',\tag{14.33}
$$

则 $p^\star(\mathbf z)$ 是不变分布。注意，给定马尔可夫链可能有多个不变分布。例如，若转移概率对应恒等变换，那么任何分布都不变。

<!-- pdf-page: 459 -->

保证目标分布 $p(\mathbf z)$ 不变的一项充分但非必要条件，是选择满足**细致平衡**性质的转移概率。对于特定分布 $p^\star(\mathbf z)$，细致平衡定义为

$$
p^\star(\mathbf z)T(\mathbf z,\mathbf z')=p^\star(\mathbf z')T(\mathbf z',\mathbf z).\tag{14.34}
$$

容易看出，相对于某分布满足细致平衡的转移概率会使该分布保持不变，因为

$$
\int p^\star(\mathbf z')T(\mathbf z',\mathbf z)\,\mathrm d\mathbf z'=\int p^\star(\mathbf z)T(\mathbf z,\mathbf z')\,\mathrm d\mathbf z',\tag{14.35}
$$

$$
=p^\star(\mathbf z)\int p(\mathbf z'\mid\mathbf z)\,\mathrm d\mathbf z',\tag{14.36}
$$

$$
=p^\star(\mathbf z).\tag{14.37}
$$

满足细致平衡的马尔可夫链称为**可逆的**。

我们的目标是利用马尔可夫链从给定分布中采样。只要构造的马尔可夫链以目标分布为不变分布，就可能达到目标。不过，还必须要求：无论初始分布 $p(\mathbf z^{(0)})$ 如何选择，当 $m\to\infty$ 时，$p(\mathbf z^{(m)})$ 都收敛到所需的不变分布 $p^\star(\mathbf z)$。这种性质称为**遍历性**，此时的不变分布称为**平衡分布**。显然，遍历的马尔可夫链只能有一个平衡分布。可以证明，在对不变分布和转移概率作出一些宽松限制后，齐次马尔可夫链是遍历的（Neal，1993）。

实际中，常用一组“基础”转移 $B_1,\ldots,B_K$ 构造转移概率。一种做法是使用混合分布

$$
T(\mathbf z',\mathbf z)=\sum_{k=1}^{K}\alpha_k B_k(\mathbf z',\mathbf z),\tag{14.38}
$$

其中混合系数 $\alpha_1,\ldots,\alpha_K$ 满足 $\alpha_k\geqslant0$，且 $\sum_k\alpha_k=1$。另一种做法是依次应用基础转移：

$$
T(\mathbf z',\mathbf z)=\sum_{\mathbf z_1}\cdots\sum_{\mathbf z_{n-1}}B_1(\mathbf z',\mathbf z_1)\cdots B_{K-1}(\mathbf z_{K-2},\mathbf z_{K-1})B_K(\mathbf z_{K-1},\mathbf z).\tag{14.39}
$$

**译注：** 原书式 (14.39) 的求和上限写作 $\mathbf z_{n-1}$，但最后一项是 $B_K$；若有 $K$ 次基础转移，索引应与 $\mathbf z_{K-1}$ 对应。

如果某分布对于每个基础转移都不变，那么对于式 (14.38) 或式 (14.39) 给出的 $T(\mathbf z',\mathbf z)$，它显然也不变。对于式 (14.38) 的混合，若每个基础转移都满足细致平衡，则混合转移 $T$ 也满足细致平衡；但式 (14.39) 构造的转移概率一般不满足。不过，若将基础转移的应用顺序对称化为 $B_1,B_2,\ldots,B_K,B_K,\ldots,B_2,B_1$，就能恢复细致平衡。复合转移概率的一个常见例子是每个基础转移只改变变量的一个子集。

<!-- pdf-page: 460 -->

### 14.2.3 Metropolis–Hastings 算法

前面介绍了基本 Metropolis 算法，但尚未证明它确实能从目标分布采样。在给出证明前，先讨论一种推广，即 **Metropolis–Hastings 算法**（Hastings，1970）；当提议分布的两个参数不再对称时，它仍然适用。具体地，在算法第 $\tau$ 步，当前状态为 $\mathbf z^{(\tau)}$，从分布 $q_k(\mathbf z\mid\mathbf z^{(\tau)})$ 抽取候选 $\mathbf z^\star$，再以概率 $A_k(\mathbf z^\star,\mathbf z^{(\tau)})$ 接受它，其中

$$
A_k(\mathbf z^\star,\mathbf z^{(\tau)})=\min\left(1,\frac{\tilde p(\mathbf z^\star)q_k(\mathbf z^{(\tau)}\mid\mathbf z^\star)}{\tilde p(\mathbf z^{(\tau)})q_k(\mathbf z^\star\mid\mathbf z^{(\tau)})}\right).\tag{14.40}
$$

$k$ 标记所考虑的一组可能转移中的成员。与前面一样，计算接受准则无须知道 $p(\mathbf z)=\tilde p(\mathbf z)/Z_p$ 中的归一化常数 $Z_p$。如果提议分布对称，式 (14.40) 的 Metropolis–Hastings 准则就化为式 (14.27) 的标准 Metropolis 准则。算法 14.2 汇总了 Metropolis–Hastings 采样。

可以用验证式 (14.34) 的细致平衡来证明，$p(\mathbf z)$ 是 Metropolis–Hastings 算法所定义的马尔可夫链的不变分布。由式 (14.40) 得

$$
\begin{aligned}p(\mathbf z)q_k(\mathbf z'\mid\mathbf z)A_k(\mathbf z',\mathbf z)&=\min\bigl(p(\mathbf z)q_k(\mathbf z'\mid\mathbf z),p(\mathbf z')q_k(\mathbf z\mid\mathbf z')\bigr)\\&=\min\bigl(p(\mathbf z')q_k(\mathbf z\mid\mathbf z'),p(\mathbf z)q_k(\mathbf z'\mid\mathbf z)\bigr)\\&=p(\mathbf z')q_k(\mathbf z\mid\mathbf z')A_k(\mathbf z,\mathbf z'),\end{aligned}\tag{14.41}
$$

正是所需的条件。

提议分布的具体选择对算法性能影响很大。对于连续状态空间，一种常见选择是以当前状态为中心的高斯分布，而其方差参数涉及重要的权衡。方差小时，接受的转移比例高，但状态空间中的移动成为缓慢的随机游走，相关时间很长。方差大时，拒绝率又会升高，因为对于我们所考虑的复杂问题，许多提议步都会到达 $p(\mathbf z)$ 很低的状态。考虑各分量间高度相关的多元分布 $p(\mathbf z)$，如图 14.10 所示。应在避免高拒绝率的条件下，使提议分布的尺度 $\rho$ 尽可能大。这意味着 $\rho$ 应与最小长度尺度 $\sigma_{\min}$ 同一数量级。系统沿较长方向以随机游走方式探索分布，因此，到达一个与初始状态大致独立的状态，所需步数为 $(\sigma_{\max}/\sigma_{\min})^2$ 的数量级。事实上，在二维中，增大 $\rho$ 虽会提高拒绝率，但被接受转移的步长也会增大，两者相抵；更一般地，对多元高斯分布，得到独立样本所需的步数按

<!-- pdf-page: 461 -->
<!-- join-previous-paragraph -->

$(\sigma_{\max}/\sigma_2)^2$ 缩放，其中 $\sigma_2$ 是第二小的标准差（Neal，1993）。撇开这些细节，若分布在不同方向上变化的长度尺度差异很大，Metropolis–Hastings 算法的收敛就可能非常慢。

**算法 14.2：Metropolis–Hastings 采样**

```text
输入：
  未归一化分布 p̃(z)
  提议分布
  {q_k(z|ẑ): k∈1,…,K}
  迭代索引到分布索引的映射
  M(·)
  初始状态 z⁽⁰⁾
  迭代次数 T
输出：z ∼ p̃(z)

z_prev ← z⁽⁰⁾
// 迭代消息传递
for τ ∈ {1,…,T} do
  k ← M(τ)
  // 取得本次分布索引
  z* ∼ q_k(z|z_prev)
  // 从提议分布采样
  u ∼ U(0,1)
  // 从均匀分布采样
  if p̃(z*)q(z_prev|z*)
     / [p̃(z_prev)
        q(z*|z_prev)] > u
  then
    z_prev ← z*
    // z⁽τ⁾ = z*
  else
    z_prev ← z_prev
    // z⁽τ⁾ = z⁽τ⁻¹⁾
  end if
end for
return z_prev
// z⁽ᵀ⁾
```

**译注：** 算法 14.2 的输出在原书写为 $z\sim\tilde p(z)$，平稳目标实际是归一化后的 $p(z)$；接受比中的 $q$ 应按当前选中的 $q_k$ 理解。“迭代消息传递”为原书注释的直译。

### 14.2.4 Gibbs 采样

**Gibbs 采样**（Geman 和 Geman，1984）是一种简单、应用广泛的 MCMC 算法，也可视为 Metropolis–Hastings 算法的特例。考虑待采样分布 $p(\mathbf z)=p(z_1,\ldots,z_M)$，并假设已为马尔可夫链选定某个初始状态。Gibbs 采样每一步都从一个变量在其余变量给定条件下的分布抽取新值，替换该变量的旧值。即从 $p(z_i\mid\mathbf z_{\backslash i})$ 抽取值来替换 $z_i$；这里 $z_i$ 是 $\mathbf z$ 的第 $i$ 个分量，$\mathbf z_{\backslash i}$ 是去掉 $z_i$ 后的 $\{z_1,\ldots,z_M\}$。可以按某一特定顺序循环更新各变量，也可以在每一步从某个分布随机选择

<!-- pdf-page: 462 -->
<!-- join-previous-paragraph -->

待更新的变量。

<figure id="fig-14-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-10.png" alt="细长的相关高斯椭圆和各向同性高斯提议圆">
  <figcaption>图 14.10：用 Metropolis–Hastings 算法，以各向同性高斯提议分布（蓝色圆）从各方向标准差差异很大的相关多元高斯分布（红色椭圆）采样的示意图。为维持低拒绝率，提议分布的尺度 $\rho$ 应与最小标准差 $\sigma_{\min}$ 同一数量级。这会产生随机游走行为：近似独立的状态之间相隔约 $(\sigma_{\max}/\sigma_{\min})^2$ 步，其中 $\sigma_{\max}$ 是最大标准差。</figcaption>
  <p class="figure-translation">图内文字：$\sigma_{\max}$ 为最长方向的标准差；$\sigma_{\min}$ 为最短方向的标准差；$\rho$ 为提议分布尺度。</p>
</figure>

例如，设三变量的分布为 $p(z_1,z_2,z_3)$，在算法第 $\tau$ 步已得到 $z_1^{(\tau)},z_2^{(\tau)},z_3^{(\tau)}$。首先，从条件分布

$$
p(z_1\mid z_2^{(\tau)},z_3^{(\tau)})\tag{14.42}
$$

采样得到 $z_1^{(\tau+1)}$，替换 $z_1^{(\tau)}$。随后，从条件分布

$$
p(z_2\mid z_1^{(\tau+1)},z_3^{(\tau)})\tag{14.43}
$$

采样得到 $z_2^{(\tau+1)}$，替换 $z_2^{(\tau)}$；可见，$z_1$ 的新值立即用于后续采样步骤。然后从

$$
p(z_3\mid z_1^{(\tau+1)},z_2^{(\tau+1)})\tag{14.44}
$$

抽取 $z_3^{(\tau+1)}$ 更新 $z_3$，如此循环遍历这三个变量。算法 14.3 汇总了 Gibbs 采样。

为了证明这一过程确实从目标分布采样，首先注意 $p(\mathbf z)$ 对每个 Gibbs 步骤分别不变，从而对整条马尔可夫链也不变。原因是，从 $p(z_i\mid\mathbf z_{\backslash i})$ 采样时，$\mathbf z_{\backslash i}$ 不改变，因此其边缘分布 $p(\mathbf z_{\backslash i})$ 显然不变。同时，每一步按定义从正确的条件分布 $p(z_i\mid\mathbf z_{\backslash i})$ 采样。由于条件分布与边缘分布共同确定联合分布，联合分布自身也保持不变。

确保 Gibbs 采样得到正确分布的第二项要求是遍历性。一项充分条件是所有条件分布处处非零。如果满足，$\mathbf z$ 空间中任意点都能通过有限步到达任意其他点，其中每个分量变量都更新一次。若不满足，某些条件分布存在零值，则必须明确证明遍历性是否成立。

<!-- pdf-page: 463 -->

**算法 14.3：Gibbs 采样**

```text
输入：
  初始值 {z_i: i∈1,…,M}
  条件分布：
  {p(z_i|{z_j:j≠i}):
   i∈1,…,M}
  迭代次数 T
输出：最终值
  {z_i: i∈1,…,M}

for τ ∈ {1,…,T} do
  for i ∈ {1,…,M} do
    z_i ∼ p(z_i|
             {z_j:j≠i})
  end for
end for
return {z_i: i∈1,…,M}
```

要完整指定算法，还需给出初始状态的分布；但经过多次迭代后抽取的样本，实际上会摆脱对初始分布的依赖。当然，马尔可夫链中相邻样本高度相关，要得到近似独立的样本，就必须对序列作子采样。

下面可将 Gibbs 采样视为 Metropolis–Hastings 算法的特例。考虑一次更新变量 $z_k$、保持其余变量 $\mathbf z_{\backslash k}$ 不变的 Metropolis–Hastings 步骤，从 $\mathbf z$ 到 $\mathbf z^\star$ 的提议概率为 $q_k(\mathbf z^\star\mid\mathbf z)=p(z_k^\star\mid\mathbf z_{\backslash k})$。注意 $\mathbf z^\star_{\backslash k}=\mathbf z_{\backslash k}$，因为这些分量在采样步骤中不变。还有 $p(\mathbf z)=p(z_k\mid\mathbf z_{\backslash k})p(\mathbf z_{\backslash k})$。所以，式 (14.40) 中决定接受概率的比值为

$$
\begin{aligned}A(\mathbf z^\star,\mathbf z)&=\frac{p(\mathbf z^\star)q_k(\mathbf z\mid\mathbf z^\star)}{p(\mathbf z)q_k(\mathbf z^\star\mid\mathbf z)}\\&=\frac{p(z_k^\star\mid\mathbf z^\star_{\backslash k})p(\mathbf z^\star_{\backslash k})p(z_k\mid\mathbf z^\star_{\backslash k})}{p(z_k\mid\mathbf z_{\backslash k})p(\mathbf z_{\backslash k})p(z_k^\star\mid\mathbf z_{\backslash k})}=1,\end{aligned}\tag{14.45}
$$

其中用到了 $\mathbf z^\star_{\backslash k}=\mathbf z_{\backslash k}$。因此，Metropolis–Hastings 步骤总是被接受。

与 Metropolis 算法一样，通过考察 Gibbs 采样在高斯分布上的应用，可以了解其行为。考虑图 14.11 的二维相关高斯分布，其条件分布的宽度为 $l$，边缘分布的宽度为 $L$。典型步长由条件分布决定，属于 $l$ 的数量级。状态以随机游走方式演变，因此从该分布得到独立样本所需的步数约为 $(L/l)^2$。当然，如果高斯分布不相关，Gibbs 采样的效率就能达到最优。对于这个简单问题，可以旋转坐标系使新变量不相关；但在实际应用中，

<!-- pdf-page: 464 -->
<!-- join-previous-paragraph -->

通常不可能找到这样的变换。

<figure id="fig-14-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-11.png" alt="Gibbs 采样在二维相关高斯分布中的交替更新轨迹">
  <figcaption>图 14.11：对分布为相关高斯的两个变量交替更新，说明 Gibbs 采样。步长由条件分布（绿色曲线）的标准差决定，是 $O(l)$，因此沿联合分布（红色椭圆）的伸长方向前进缓慢。从该分布取得独立样本所需的步数是 $O((L/l)^2)$。</figcaption>
  <p class="figure-translation">图内文字：$z_1,z_2$ 为两个坐标；$L$ 是边缘分布的宽度，$l$ 是条件分布的宽度。</p>
</figure>

减轻 Gibbs 采样随机游走行为的一种方法称为**过度松弛**（Adler，1981）。其最初形式适用于条件分布为高斯的情形。它涵盖的分布类别比多元高斯更广：例如，非高斯分布 $p(z,y)\propto\exp(-z^2y^2)$ 的条件分布也是高斯的。在 Gibbs 采样算法的每一步，某分量 $z_i$ 的条件分布有均值 $\mu_i$ 和方差 $\sigma_i^2$。过度松弛框架用下式替换 $z_i$：

$$
z_i'=\mu_i+\alpha_i(z_i-\mu_i)+\sigma_i(1-\alpha_i^2)^{1/2}\nu,\tag{14.46}
$$

其中 $\nu$ 是均值为零、方差为一的高斯随机变量，而 $\alpha$ 是满足 $-1<\alpha<1$ 的参数。当 $\alpha=0$，该方法等同于标准 Gibbs 采样；当 $\alpha<0$，更新会偏向均值的另一侧。由于若 $z_i$ 的均值和方差分别为 $\mu_i$ 与 $\sigma_i^2$，则 $z_i'$ 也一样，这一步使目标分布保持不变。当变量高度相关时，过度松弛会促进状态空间中的定向移动。**有序过度松弛**框架（Neal，1999）将这一方法推广到非高斯分布。

Gibbs 采样能否用于实际问题，取决于是否易于从条件分布 $p(z_k\mid\mathbf z_{\backslash k})$ 抽取样本。对于由有向图模型指定的概率分布，单个节点的条件分布只依赖相应马尔可夫毯中的变量，如图 14.12 所示。对于有向图，只要为各节点选择的、以其父节点为条件的分布足够广泛，就能得到对数凹的 Gibbs 条件分布。因此，第 14.1.4 节讨论的自适应拒绝采样方法，为具有广泛适用性的有向图蒙特卡罗采样提供了框架。

<!-- pdf-page: 465 -->

<figure id="fig-14-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-12.png" alt="有向图中节点 z 的父节点、子节点和共父节点组成马尔可夫毯">
  <figcaption>图 14.12：Gibbs 采样须从变量 $z$ 在其余变量给定条件下的条件分布抽取样本。对于有向图模型，此条件分布仅取决于马尔可夫毯中节点的状态。蓝色阴影所示的马尔可夫毯包括父节点、子节点和共父节点。</figcaption>
  <p class="figure-translation">图内文字：$z$ 为待更新节点；蓝色阴影节点构成它的马尔可夫毯。</p>
</figure>

基本 Gibbs 采样每次只考虑一个变量，所以相邻样本间有很强的依赖性。在另一极端，若能直接从联合分布抽取样本（这里假定该操作不可行），相邻样本就会独立。可采用一种折中策略改进简单 Gibbs 采样器：依次从变量组而非单个变量采样。**分块 Gibbs 采样**算法选取不必互不相交的变量块，再依次以其余变量为条件，对每个块内的变量联合采样（Jensen、Kong 和 Kjaerulff，1995）。

### 14.2.5 祖先采样

对于许多模型，用图模型指定联合分布 $p(\mathbf z)$ 很方便。对于没有观测变量的有向图，用下述**祖先采样**方法即可从联合分布采样。联合分布表示为

$$
p(\mathbf z)=\prod_{i=1}^{M}p(\mathbf z_i\mid\operatorname{pa}(i)),\tag{14.47}
$$

其中 $\mathbf z_i$ 是与节点 $i$ 关联的一组变量，$\operatorname{pa}(i)$ 表示与节点 $i$ 的父节点关联的一组变量。为了得到联合分布的一个样本，按 $\mathbf z_1,\ldots,\mathbf z_M$ 的顺序遍历变量一次，每一步从条件分布 $p(\mathbf z_i\mid\operatorname{pa}(i))$ 采样。这总是可行的，因为每一步都已为所有父节点赋值。遍历完整张图后，就得到联合分布的一个样本。这里假定可以从每个节点的条件分布采样。

再考虑一张有向图，其中某些节点构成证据集合 $\mathcal E$，并已赋予观测值。原则上，至少对于表示离散变量的节点，可将上述过程推广成**逻辑采样**方法（Henrion，1988），它可视为重要性采样的一种特例（见第 14.1.5 节）。每一步，当采得一个已观测变量 $z_i$ 的值时，将采样值与观测值比较；若相符，保留并继续下一个变量。若不相符，就丢弃至此为止的整份样本，算法便

<!-- pdf-page: 466 -->
<!-- join-previous-paragraph -->

从图中的第一个节点重新开始。该算法确实从后验分布采样，因为它等同于从隐变量与数据变量的联合分布抽样，再丢弃与观测数据不符的样本；只是发现第一个冲突值时就提前停止，从而稍省计算。然而，随着观测变量数目及其可能状态数的增加，从后验分布接受样本的总概率迅速下降，因此实际中很少使用这种方法。

对此方法的一种改进称为**似然加权采样**（Fung 和 Chang，1990；Shachter 和 Peot，1990），它把祖先采样与重要性采样结合起来。依次处理每个变量：若它属于证据集合，就直接将其设为已观测值；否则从 $p(z_i\mid\operatorname{pa}(i))$ 采样，其中条件变量采用目前已采得的值。所得样本 $\mathbf z$ 的权重为

$$
r(\mathbf z)=\prod_{z_i\notin\mathcal E}\frac{p(z_i\mid\operatorname{pa}(i))}{p(z_i\mid\operatorname{pa}(i))}\prod_{z_i\in\mathcal E}\frac{p(z_i\mid\operatorname{pa}(i))}{1}=\prod_{z_i\in\mathcal E}p(z_i\mid\operatorname{pa}(i)).\tag{14.48}
$$

此方法还可扩展为**自重要性采样**（Shachter 和 Peot，1990），不断更新重要性采样分布，以反映当前估计的后验分布。

## 14.3 朗之万采样

Metropolis–Hastings 算法通过提议分布形成候选样本的马尔可夫链，再以式 (14.40) 的准则决定接受或拒绝，从而从概率分布采样。这可能效率不高，因为提议分布往往是简单且固定的，能向数据空间中的任意方向提出更新，导致随机游走。

我们已经看到，训练神经网络时，为使似然函数最大化，利用对数似然对模型可学习参数的梯度极为有利。类似地，我们可以构造马尔可夫链采样算法，利用概率密度对数据向量的梯度，优先朝概率较高的区域移动。一种方法称为**哈密顿蒙特卡罗**，也称**混合蒙特卡罗**，它同样使用 Metropolis 接受检验（Duane 等，1987；Bishop，2006）。这里聚焦于深度学习中广泛使用的另一种方法——**朗之万采样**。它虽然不使用接受检验，但必须谨慎设计，才能确保所得样本无偏。朗之万采样的重要应用之一，是由能量函数定义的机器学习模型。

<!-- pdf-page: 467 -->

### 14.3.1 基于能量的模型

许多生成模型可表示为条件概率分布 $p(\mathbf x\mid\mathbf w)$，其中 $\mathbf x$ 是数据向量，$\mathbf w$ 是可学习参数向量。可通过最大化针对训练数据集定义的似然函数来训练这类模型。不过，为了表示有效的概率分布，模型必须满足

$$
\int p(\mathbf x\mid\mathbf w)p(\mathbf x)\,\mathrm d\mathbf x=1.\tag{14.49}
$$

**译注：** 原书式 (14.49) 左边多写了一个 $p(\mathbf x)$；条件密度通常应满足 $\int p(\mathbf x\mid\mathbf w)\,\mathrm d\mathbf x=1$，也与后文式 (14.50)–(14.51) 一致。

确保满足这一要求可能大幅限制模型可采用的形式。若暂不考虑归一化约束，就可以研究更广泛的一类模型，称为**基于能量的模型**（LeCun 等，2006）。设 $E(\mathbf x,\mathbf w)$ 为**能量函数**，是其参数的实值函数，除此之外没有其他约束。指数 $\exp\{-E(\mathbf x,\mathbf w)\}$ 非负，因而可视为 $\mathbf x$ 上的未归一化概率分布。指数中的负号只是约定，表示能量越高，概率越低。于是，可以定义归一化分布

$$
p(\mathbf x\mid\mathbf w)=\frac{1}{Z(\mathbf w)}\exp\{-E(\mathbf x,\mathbf w)\},\tag{14.50}
$$

其中归一化常数 $Z(\mathbf w)$ 称为**配分函数**，定义为

$$
Z(\mathbf w)=\int\exp\{-E(\mathbf x,\mathbf w)\}\,\mathrm d\mathbf x.\tag{14.51}
$$

能量函数常由深度神经网络建模：输入为向量 $\mathbf x$，输出为标量 $E(\mathbf x,\mathbf w)$，$\mathbf w$ 是网络中的权重和偏置。

注意，配分函数依赖 $\mathbf w$，这给训练带来困难。例如，对独立同分布数据组成的数据集 $\mathcal D=(\mathbf x_1,\ldots,\mathbf x_N)$，对数似然函数为

$$
\ln p(\mathcal D\mid\mathbf w)=-\sum_{n=1}^{N}E(\mathbf x_n,\mathbf w)-N\ln Z(\mathbf w).\tag{14.52}
$$

要计算 $\ln p(\mathcal D\mid\mathbf w)$ 对 $\mathbf w$ 的梯度，须知道 $Z(\mathbf w)$ 的形式。然而，对能量函数 $E(\mathbf x,\mathbf w)$ 的许多选择，计算式 (14.51) 的配分函数并不可行，因为这要对整个 $\mathbf x$ 空间积分（离散变量则求和）。“基于能量的模型”通常指该积分无法求解的模型。不过，概率模型也可视为基于能量的模型的特例，因此本书讨论的许多模型都可从能量模型的角度理解。能量模型的主要优点，是绕开归一化要求所带来的形式限制，从而具有灵活性；相应的缺点是，归一化常数未知，训练可能更困难。

<!-- pdf-page: 468 -->

### 14.3.2 极大化似然

为了在不计算配分函数的情况下训练能量模型，人们已开发出多种近似方法（Song 和 Kingma，2021）。这里讨论基于 MCMC 的方法。另一种称为**得分匹配**（score matching）的方法将在第 20 章讨论扩散模型时介绍。

我们已经看到，能量模型的配分函数 $Z(\mathbf w)$ 未知，因此似然函数无法显式求值。不过，可以利用蒙特卡罗采样方法，近似对数似然对模型参数的梯度。能量模型无论采用什么方法训练好后，还需要从中抽取样本的方法；蒙特卡罗方法同样可以派上用场。

由式 (14.50)，能量模型的对数似然函数对模型参数的梯度可写为

$$
\nabla_{\mathbf w}\ln p(\mathbf x\mid\mathbf w)=-\nabla_{\mathbf w}E(\mathbf x,\mathbf w)-\nabla_{\mathbf w}\ln Z(\mathbf w).\tag{14.53}
$$

这针对单个数据点 $\mathbf x$；实际中，我们想最大化对来自某个未知分布 $p_D(\mathbf x)$ 的训练集所定义的似然。若假设数据点独立同分布，就可以考虑对数似然在 $p_D(\mathbf x)$ 下的期望的梯度：

$$
\mathbb E_{\mathbf x\sim p_D}\bigl[\nabla_{\mathbf w}\ln p(\mathbf x\mid\mathbf w)\bigr]=-\mathbb E_{\mathbf x\sim p_D}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr]-\nabla_{\mathbf w}\ln Z(\mathbf w).\tag{14.54}
$$

这里用到了最后一项 $-\nabla_{\mathbf w}\ln Z(\mathbf w)$ 不依赖 $\mathbf x$，故可移到期望之外。虽然配分函数 $Z(\mathbf w)$ 未知，但可利用式 (14.51) 并整理，得到

$$
-\nabla_{\mathbf w}\ln Z(\mathbf w)=\int\{\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\}p(\mathbf x\mid\mathbf w)\,\mathrm d\mathbf x.\tag{14.55}
$$

式 (14.55) 的右边是模型分布 $p(\mathbf x\mid\mathbf w)$ 下的期望：

$$
\int\{\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\}p(\mathbf x\mid\mathbf w)\,\mathrm d\mathbf x=\mathbb E_{\mathbf x\sim M}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr].\tag{14.56}
$$

**译注：** 式 (14.56) 的期望下标 $\mathbf x\sim M$，按相邻的式 (14.57) 应理解为 $\mathbf x\sim p_M(\mathbf x)$，即从模型分布取样。

合并式 (14.54)、(14.55) 和 (14.56)，得

$$
\nabla_{\mathbf w}\mathbb E_{\mathbf x\sim p_D}\bigl[\ln p(\mathbf x\mid\mathbf w)\bigr]=-\mathbb E_{\mathbf x\sim p_D}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr]+\mathbb E_{\mathbf x\sim p_M(\mathbf x)}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr].\tag{14.57}
$$

图 14.13 说明了这一结果，其含义如下。目标是找到使似然函数最大化的参数 $\mathbf w$，因此考虑沿 $\nabla_{\mathbf w}\ln p(\mathbf x\mid\mathbf w)$ 方向对 $\mathbf w$ 作微小改变。式 (14.57) 表明，此梯度的期望可分为符号相反的两项。右边第一项使

<!-- pdf-page: 469 -->
<!-- join-previous-paragraph -->

来自 $p_D(\mathbf x)$ 的点的能量 $E(\mathbf x,\mathbf w)$ 降低，模型所定义的概率密度随之增大。右边第二项使模型自身抽取的数据点的能量升高，模型所定义的概率密度随之减小。在模型密度高于训练数据密度的区域，净效应是提高能量、降低概率；反之，在训练数据密度高于模型密度的区域，净效应是降低能量、提高概率密度。两项共同把概率质量从训练数据密度低的区域移往密度高的区域，正符合目标。当模型分布与数据分布相同时，两项大小相等，此时式 (14.57) 左边的梯度为零。

<figure id="fig-14-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-13.png" alt="能量函数、模型密度和真实数据密度的曲线及样本点">
  <figcaption>图 14.13：通过极大化似然训练能量模型的示意图。绿色曲线是能量函数 $E(\mathbf x,\mathbf w)$，另有相应的模型分布 $p_M(\mathbf x)$ 和真实数据分布 $p_D(\mathbf x)$。利用式 (14.57) 提高期望对数似然时，模型样本对应位置（蓝点）的能量上升，数据集样本对应位置（红点）的能量下降。</figcaption>
  <p class="figure-translation">图内文字：$E(\mathbf x,\mathbf w)$ 为能量函数；$p_D(\mathbf x)$ 为数据分布；$p_M(\mathbf x)$ 为模型分布；$\mathbf x$ 为横轴数据变量。</p>
</figure>

### 14.3.3 朗之万动力学

若把式 (14.57) 用作实际训练方法，就须近似其右边两项。对于任意给定的 $\mathbf x$，可用自动微分计算 $\nabla_{\mathbf w}E(\mathbf x,\mathbf w)$。对于第一项，可用训练数据集估计对 $\mathbf x$ 的期望：

$$
\mathbb E_{\mathbf x\sim p_D}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr]\simeq\frac{1}{N}\sum_{n=1}^{N}\nabla_{\mathbf w}E(\mathbf x_n,\mathbf w).\tag{14.58}
$$

<!-- pdf-page: 470 -->

第二项更具挑战，因为我们须从能量函数定义的模型分布抽取样本，而相应配分函数难以计算。MCMC 方法可以做到这一点。一种常用方法称为**随机梯度朗之万动力学**，也简称朗之万采样（Parisi，1981；Welling 和 Teh，2011）。该方法只通过**得分函数**（score function）依赖分布 $p(\mathbf x\mid\mathbf w)$。得分函数定义为对数似然对数据向量 $\mathbf x$ 的梯度：

$$
\mathbf s(\mathbf x,\mathbf w)=\nabla_{\mathbf x}\ln p(\mathbf x\mid\mathbf w).\tag{14.59}
$$

要强调的是，这一梯度针对数据点 $\mathbf x$，并非通常对可学习参数 $\mathbf w$ 求取的梯度。将式 (14.50) 代入式 (14.59)，得到

$$
\mathbf s(\mathbf x,\mathbf w)=-\nabla_{\mathbf x}E(\mathbf x,\mathbf w),\tag{14.60}
$$

可见配分函数不再出现，因为它与 $\mathbf x$ 无关。

首先从先验分布抽取初值 $\mathbf x^{(0)}$，随后迭代以下马尔可夫链步骤：

$$
\mathbf x^{(\tau+1)}=\mathbf x^{(\tau)}+\eta\nabla_{\mathbf x}\ln p(\mathbf x^{(\tau)},\mathbf w)+\sqrt{2\eta}\,\boldsymbol\epsilon^{(\tau)},\qquad\tau\in1,\ldots,T.\tag{14.61}
$$

**译注：** 原书式 (14.61) 从 $\mathbf x^{(0)}$ 开始，却令 $\tau=1,\ldots,T$ 并更新到 $\mathbf x^{(\tau+1)}$，迭代索引有错位。以下正文中的“$\mathbf z^{(T)}$”也是原书写法；按本节变量应为 $\mathbf x^{(T)}$。

其中 $\boldsymbol\epsilon^{(\tau)}\sim\mathcal N(\mathbf 0,\mathbf I)$ 是从均值为零、单位协方差的高斯分布独立抽取的样本，参数 $\eta$ 控制步长。朗之万方程每次迭代先沿对数似然梯度方向走一步，再加上高斯噪声。可以证明，在 $\eta\to0$ 且 $T\to\infty$ 的极限下，$\mathbf z^{(T)}$ 是来自 $p(\mathbf x)$ 的独立样本。算法 14.4 汇总了朗之万采样。

重复这一过程可以得到样本集 $\{\mathbf x_1,\ldots,\mathbf x_M\}$，进而用下式近似式 (14.57) 的第二项：

$$
\mathbb E_{\mathbf x\sim p_M(\mathbf x)}\bigl[\nabla_{\mathbf w}E(\mathbf x,\mathbf w)\bigr]\simeq\frac{1}{M}\sum_{m=1}^{M}\nabla_{\mathbf w}E(\mathbf x_m,\mathbf w).\tag{14.62}
$$

运行很长的马尔可夫链以生成独立样本，计算成本可能很高，因此需要考虑实际近似。一种方法称为**对比散度**（Hinton，2002）。用于估计式 (14.62) 的样本，是从训练数据点 $\mathbf x_n$ 出发运行蒙特卡罗链得到的。如果链运行足够多步，最终值基本就是来自模型分布的无偏样本。但 Hinton（2002）提出只运行少数几步蒙特卡罗，甚至一步，以大幅降低计算成本。所得样本远非无偏，且靠近数据流形。因此，使用梯度下降的效果是只在数据流形附近塑造能量曲面，从而塑造概率密度。这对判别等任务可能有效，但预计不太有利于学习生成模型。

<!-- pdf-page: 471 -->

**算法 14.4：朗之万采样**

```text
输入：初值 x⁽⁰⁾
      概率密度 p(x,w)
      学习率参数 η
      迭代次数 T
输出：最终值 x⁽ᵀ⁾

x ← x₀
for τ ∈ {1,…,T} do
  ε ∼ N(ε|0,I)
  x ← x + η∇ₓ ln p(x,w)
         + √(2η)ε
end for
return x
// 最终值 x⁽ᵀ⁾
```

## 习题

**14.1（★）** 证明式 (14.2) 定义的 $\bar f$ 是无偏估计量，换言之，证明其右边的期望等于 $\mathbb E[f(\mathbf z)]$。

**14.2（★）** 证明式 (14.2) 定义的 $\bar f$ 的方差由式 (14.4) 给出。

**14.3（★）** 假设随机变量 $z$ 在 $(0,1)$ 上均匀分布，并用 $y=h^{-1}(z)$ 变换 $z$，其中 $h(y)$ 由式 (14.6) 给出。证明 $y$ 服从分布 $p(y)$。

**14.4（★★）** 给定在 $(0,1)$ 上均匀分布的随机变量 $z$，找出变换 $y=f(z)$，使 $y$ 服从式 (14.8) 给出的柯西分布。

**14.5（★★）** 设 $z_1,z_2$ 在单位圆内均匀分布，如图 14.3 所示，并按式 (14.10)、(14.11) 作变量变换。证明 $(y_1,y_2)$ 服从式 (14.12) 给出的分布。

**14.6（★★）** 设 $\mathbf z$ 是均值为零、协方差矩阵为单位矩阵的 $D$ 维高斯随机变量，正定对称矩阵 $\boldsymbol\Sigma$ 的 Cholesky 分解为 $\boldsymbol\Sigma=\mathbf L\mathbf L^{\mathsf T}$，其中 $\mathbf L$ 是下三角矩阵，即主对角线上方的元素全为零。证明 $\mathbf y=\boldsymbol\mu+\mathbf L\mathbf z$ 服从均值为 $\boldsymbol\mu$、协方差为 $\boldsymbol\Sigma$ 的高斯分布。这提供了一种方法：利用来自均值为零、方差为一的一元高斯分布的样本，生成一般多元高斯分布的样本。

**14.7（★★）** 本题更仔细地证明拒绝采样确实从目标分布 $p(z)$ 抽取样本。设提议分布为 $q(z)$。证明值为 $z$ 的样本被接受的概率为

<!-- pdf-page: 472 -->
<!-- join-previous-paragraph -->

$\tilde p(z)/kq(z)$，其中 $\tilde p$ 是任何与 $p(z)$ 成正比的未归一化分布，而常数 $k$ 取为使所有 $z$ 均满足 $kq(z)\geqslant\tilde p(z)$ 的最小值。注意，抽取到值 $z$ 的概率等于从 $q(z)$ 抽到该值的概率，乘以在已抽到该值的条件下接受它的概率。利用这一点及概率的加法、乘法规则，写出 $z$ 的归一化分布，并证明它等于 $p(z)$。

**14.8（★）** 假设 $z$ 在区间 $[0,1]$ 上均匀分布。证明变量 $y=b\tan z+c$ 服从式 (14.16) 给出的柯西分布。

**译注：** 按原题的角度区间，$b\tan z+c$ 只覆盖一段有限范围，不能产生整条实轴上的柯西分布；可参见式 (14.16) 后的标准取角方式。题干与原书保持一致。

**14.9（★★）** 利用连续性和归一化要求，确定自适应拒绝采样包络分布 (14.17) 中系数 $k_i$ 的表达式。

**14.10（★★）** 利用第 14.1.2 节讨论的单个指数分布采样方法，设计一个从式 (14.17) 定义的分段指数分布采样的算法。

**14.11（★）** 证明式 (14.28)、(14.29)、(14.30) 定义的整数上的简单随机游走满足 $\mathbb E[(z^{(\tau)})^2]=\mathbb E[(z^{(\tau-1)})^2]+1/2$，并由归纳法得到 $\mathbb E[(z^{(\tau)})^2]=\tau/2$。

**14.12（★★）** 证明第 14.2.4 节讨论的 Gibbs 采样算法满足式 (14.34) 定义的细致平衡。

**14.13（★）** 考虑图 14.14 所示的分布。讨论针对该分布的标准 Gibbs 采样过程是否具有遍历性，因而是否能正确地从该分布采样。

<figure id="fig-14-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-14/fig-14-14.png" alt="二维坐标中两个互相分离的着色概率区域">
  <figcaption>图 14.14：两个变量 $z_1,z_2$ 的概率分布，在着色区域均匀分布，其他位置概率为零。</figcaption>
  <p class="figure-translation">图内文字：$z_1$ 为横轴，$z_2$ 为纵轴；两个粉红色区域为非零概率区域。</p>
</figure>

**14.14（★）** 验证过度松弛更新式 (14.46) 给出的 $z_i'$ 的均值为 $\mu_i$、方差为 $\sigma_i^2$；其中 $z_i$ 的均值为 $\mu_i$、方差为 $\sigma_i$，$\nu$ 的均值为零、方差为一。

**译注：** 原题把 $\sigma_i$ 称为 $z_i$ 的方差；按式 (14.46) 的定义，方差应为 $\sigma_i^2$，$\sigma_i$ 是标准差。

<!-- pdf-page: 473 -->

**14.15（★）** 证明从有向图作似然加权采样时，重要性采样权重由式 (14.48) 给出。

**14.16（★）** 证明如果 $Z(\mathbf w)$ 满足式 (14.51)，则分布 (14.50) 相对于 $\mathbf x$ 已归一化。

**14.17（★★）** 利用式 (14.50)，证明能量模型的对数似然函数的梯度可以写为式 (14.52) 的形式。

**译注：** 原题的式 (14.52) 是对数似然本身；梯度表达式是式 (14.53)，因此此处交叉引用应指向 (14.53)。

**14.18（★★）** 利用式 (14.54)、(14.55) 和 (14.56)，证明能量模型的对数似然函数的梯度可以写为式 (14.57) 的形式。
