# 第 18 章 归一化流

<aside class="chapter-guide"><strong>本章导读</strong><p>本章讨论用可逆变换建立生成模型：先从潜变量分布出发，通过耦合流和自回归流计算数据密度；再把变换扩展到连续时间，用神经常微分方程构造连续归一化流。</p></aside>

<!-- pdf-page: 559 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/chapter-art.png" alt="第 18 章归一化流彩色抽象章首页图，含英文标题 Normalizing Flows">
  <p class="figure-translation">图内文字：Normalizing Flows → 归一化流。</p>
</figure>

我们已经看到，生成对抗网络（GAN）如何扩展线性潜变量模型的框架：它用深度神经网络表示从潜空间到数据空间的高度灵活、可学习的非线性变换。然而，其似然函数通常难以求解，因为网络函数无法求逆；若潜空间的维度低于数据空间，甚至可能根本不存在逆函数。因此，GAN 引入第二个判别网络，以便进行对抗训练（见第 17 章）。

这里讨论训练非线性潜变量模型的四种方法中的第二种（见第 16.4.4 节）。这种方法限制神经网络模型的形式，使似然函数可以不经近似地计算，同时仍可直接从训练好的模型采样。假设我们在潜变量 $\mathbf z$ 上定义分布 $p_z(\mathbf z)$，它有时也称为**基础分布**（base distribution），并定义一个由深度神经网络给出的非线性函数 $\mathbf x=\mathbf f(\mathbf z,\mathbf w)$，将

<!-- pdf-page: 560 -->
<!-- join-previous-paragraph -->

潜空间变换为数据空间。若 $p_z(\mathbf z)$ 是高斯分布等简单分布，采样便很容易：只须将每个潜变量样本 $\mathbf z^*\sim p_z(\mathbf z)$ 输入神经网络，就得到相应的数据样本 $\mathbf x^*=\mathbf f(\mathbf z^*,\mathbf w)$。

为了计算这个模型的似然函数，需要数据空间中的分布，而它依赖神经网络函数的**逆函数**。将逆函数记为 $\mathbf z=\mathbf g(\mathbf x,\mathbf w)$，它满足 $\mathbf z=\mathbf g(\mathbf f(\mathbf z,\mathbf w),\mathbf w)$。这要求对每个 $\mathbf w$，函数 $\mathbf f(\mathbf z,\mathbf w)$ 和 $\mathbf g(\mathbf x,\mathbf w)$ 都可逆，即为**双射**；因此，每个 $\mathbf x$ 值都唯一对应一个 $\mathbf z$ 值，反之亦然。于是可用变量变换公式计算数据密度（见第 2.4 节）：

$$
p_x(\mathbf x\mid\mathbf w)=p_z(\mathbf g(\mathbf x,\mathbf w))\,|\det\mathbf J(\mathbf x)|. \tag{18.1}
$$

其中 $\mathbf J(\mathbf x)$ 是雅可比矩阵，其元素为

$$
J_{ij}(\mathbf x)=\frac{\partial g_i(\mathbf x,\mathbf w)}{\partial x_j}, \tag{18.2}
$$

而 $|\cdot|$ 表示模或绝对值。下文仍将 $\mathbf z$ 称为“潜”变量，尽管在确定性映射下，给定任意数据值 $\mathbf x$ 后，相应的 $\mathbf z$ 值也是唯一确定的。

稍后将用一种特殊的神经网络定义映射函数 $\mathbf f(\mathbf z,\mathbf w)$，并讨论它的结构。要求映射可逆的一个后果是：潜空间必须与数据空间具有相同维度。对于图像等高维数据，这可能导致模型规模很大。另外，一般情况下计算 $D\times D$ 矩阵的行列式需要 $O(D^3)$ 的成本，因此我们将进一步限制模型，使雅可比行列式能够更高效地计算。

如果训练集 $\mathcal D=\{\mathbf x_1,\ldots,\mathbf x_N\}$ 包含 $N$ 个相互独立的数据点，由式 (18.1) 得到对数似然函数

$$
\ln p(\mathcal D\mid\mathbf w)=\sum_{n=1}^{N}\ln p_x(\mathbf x_n\mid\mathbf w) \tag{18.3}
$$

$$
=\sum_{n=1}^{N}\left\{\ln p_z(\mathbf g(\mathbf x_n,\mathbf w))+\ln|\det\mathbf J(\mathbf x_n)|\right\}, \tag{18.4}
$$

目标是用这个似然函数训练神经网络。为建模范围广泛的分布，变换函数 $\mathbf x=\mathbf f(\mathbf z,\mathbf w)$ 必须足够灵活，因此我们采用深度神经网络架构。只要网络的每一层都可逆，就能保证整体函数可逆。考虑三个连续变换，每个对应一层，形式为（习题 18.2）

$$
\mathbf x=\mathbf f^A\!\left(\mathbf f^B\!\left(\mathbf f^C(\mathbf z)\right)\right). \tag{18.5}
$$

逆函数则为

$$
\mathbf z=\mathbf g^C\!\left(\mathbf g^B\!\left(\mathbf g^A(\mathbf x)\right)\right), \tag{18.6}
$$

<!-- pdf-page: 561 -->

其中 $\mathbf g^A$、$\mathbf g^B$ 和 $\mathbf g^C$ 分别是 $\mathbf f^A$、$\mathbf f^B$ 和 $\mathbf f^C$ 的逆函数。对这样的分层结构，也容易根据各层雅可比行列式计算整体雅可比行列式。利用微积分的链式法则，

$$
J_{ij}=\frac{\partial z_i}{\partial x_j}=\sum_k\sum_l\frac{\partial g_i^C}{\partial g_k^B}\frac{\partial g_k^B}{\partial g_l^A}\frac{\partial g_l^A}{\partial x_j}. \tag{18.7}
$$

可以看出，右侧是三个矩阵的乘积，而矩阵乘积的行列式等于各矩阵行列式的乘积。因此，整体雅可比行列式的对数是各层对应对数行列式之和（见附录 A）。

这种用一系列映射变换概率分布以建模灵活分布的方法，称为**归一化流**（normalizing flow），因为它在一定程度上类似流体的流动。逆映射的效果则是将复杂的数据分布变换为归一化形式，通常是高斯或正态分布。Kobyzev、Prince 和 Brubaker（2019）以及 Papamakarios 等（2019）综述了归一化流。下面讨论实践中两类主要归一化流的核心概念：**耦合流**与**自回归流**。我们还将利用神经微分方程定义可逆映射，由此得到**连续流**。

## 18.1 耦合流

我们的目标是设计一个可逆的单层函数，然后将许多这样的层组合起来，定义高度灵活的可逆函数类。先考虑线性变换

$$
x=az+b. \tag{18.8}
$$

它容易求逆，得到

$$
z=\frac1a(x-b). \tag{18.9}
$$

然而，线性变换对复合运算封闭：一串线性变换等价于一个整体线性变换。此外，高斯分布经过线性变换后仍为高斯分布（见习题 3.6）。因此，即便堆叠许多线性变换“层”，最终仍只能得到高斯分布。问题是能否既保留线性变换的可逆性，又增加灵活性，使所得分布可以是非高斯分布。

一种解决方法是名为 **real NVP** 的归一化流模型（Dinh、Krueger 和 Bengio，2014；Dinh、Sohl-Dickstein 和 Bengio，2016）。其名称是“real-valued non-volume-preserving”（实值非体积保持）的缩写。它把潜变量向量 $\mathbf z$ 分成两部分 $\mathbf z=(\mathbf z_A,\mathbf z_B)$；若 $\mathbf z$ 的维度为 $D$，则 $\mathbf z_A$ 的维度为 $d$，$\mathbf z_B$ 的维度为 $D-d$。输出向量也采用相同的分组方式。

<!-- pdf-page: 562 -->

<figure id="fig-18-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-1.png" alt="real NVP 单层流的两部分输入和输出，两个神经网络控制下半部分的逐元素缩放与平移">
  <figcaption>图 18.1：real NVP 归一化流模型的单层。网络 NN1 计算函数 $\exp(\mathbf s(\mathbf z_A,\mathbf w))$，网络 NN2 计算函数 $\mathbf b(\mathbf z_A,\mathbf w)$。输出向量由式 (18.10) 和 (18.11) 定义。</figcaption>
  <p class="figure-translation">图内文字与符号：NN1、NN2 → 两个神经网络；$\mathbf z_A,\mathbf z_B$ → 输入向量的两部分；$\mathbf x_A,\mathbf x_B$ → 输出向量的两部分；$\exp(\mathbf s(\cdot))$ → 逐元素缩放系数；$\mathbf b(\cdot)$ → 平移项；$\odot$ → 逐元素乘积；$+$ → 相加。</p>
</figure>

具体地，令 $\mathbf x=(\mathbf x_A,\mathbf x_B)$，其中 $\mathbf x_A$ 的维度为 $d$，$\mathbf x_B$ 的维度为 $D-d$。对输出向量的第一部分，只须复制输入：

$$
\mathbf x_A=\mathbf z_A. \tag{18.10}
$$

向量的第二部分经历一个线性变换，但其中的系数不再是常数，而是 $\mathbf z_A$ 的非线性函数：

$$
\mathbf x_B=\exp(\mathbf s(\mathbf z_A,\mathbf w))\odot\mathbf z_B+\mathbf b(\mathbf z_A,\mathbf w), \tag{18.11}
$$

其中 $\mathbf s(\mathbf z_A,\mathbf w)$ 和 $\mathbf b(\mathbf z_A,\mathbf w)$ 是神经网络输出的实值向量；指数函数保证乘法项非负。这里的 $\odot$ 表示两个向量之间逐元素相乘的**Hadamard 积**，式 (18.11) 中的指数函数同样逐元素作用。注意，我们为两个网络函数都写了同一个向量 $\mathbf w$。实际实现时，可以让它们是各有参数的独立网络，也可以用一个有两组输出的网络。

由于使用了神经网络函数，$\mathbf x_B$ 可以是 $\mathbf x_A$ 的高度灵活的函数。尽管如此，整体变换却容易求逆：给定 $\mathbf x=(\mathbf x_A,\mathbf x_B)$，先计算

$$
\mathbf z_A=\mathbf x_A, \tag{18.12}
$$

再求 $\mathbf s(\mathbf z_A,\mathbf w)$ 和 $\mathbf b(\mathbf z_A,\mathbf w)$，最后用下式计算 $\mathbf z_B$：

$$
\mathbf z_B=\exp(-\mathbf s(\mathbf z_A,\mathbf w))\odot\bigl(\mathbf x_B-\mathbf b(\mathbf z_A,\mathbf w)\bigr). \tag{18.13}
$$

图 18.1 展示了整体变换。注意，并不要求单个神经网络函数 $\mathbf s(\mathbf z_A,\mathbf w)$ 和 $\mathbf b(\mathbf z_A,\mathbf w)$ 自身可逆。

现在考虑式 (18.2) 定义的雅可比矩阵及其行列式。可依照 $\mathbf z$ 和 $\mathbf x$ 的分组，把雅可比矩阵分块，得到

$$
\mathbf J=\begin{bmatrix}\mathbf I_d&\mathbf0\\[3pt]\dfrac{\partial\mathbf z_B}{\partial\mathbf x_A}&\operatorname{diag}\!\bigl(\exp(-\mathbf s)\bigr)\end{bmatrix}. \tag{18.14}
$$

<!-- pdf-page: 563 -->

<figure id="fig-18-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-2.png" alt="两层 real NVP 耦合流交替更新向量的上下两部分">
  <figcaption>图 18.2：将图 18.1 所示形式的两层组合起来，得到更灵活、但仍可逆的非线性层。每个子层都可逆，雅可比矩阵易于计算，因此整体双层结构也具有这些性质。</figcaption>
  <p class="figure-translation">图内文字与符号：NN1–NN4 → 四个神经网络；$\mathbf z_A,\mathbf z_B$ → 两部分输入；$\odot$ → 逐元素相乘；$+$ → 相加。第一层保持上半部分不变，第二层保持下半部分不变。</p>
</figure>

左上块对应 $\mathbf z_A$ 对 $\mathbf x_A$ 的导数，因此根据式 (18.12) 是 $d\times d$ 单位矩阵。右上块对应 $\mathbf z_A$ 对 $\mathbf x_B$ 的导数，式 (18.12) 表明它们为零。左下块对应 $\mathbf z_B$ 对 $\mathbf x_A$ 的导数；由式 (18.13) 可知，它们是涉及神经网络函数的复杂表达式。最后，右下块对应 $\mathbf z_B$ 对 $\mathbf x_B$ 的导数。由式 (18.13)，它是一个对角矩阵，对角元素由 $\mathbf s(\mathbf z_A,\mathbf w)$ 各元素取负后求指数得到。因此，雅可比矩阵 (18.14) 是下三角矩阵：主对角线上方的所有元素均为零。对这样的矩阵，行列式就是主对角线上各元素的乘积（见附录 A），不依赖左下块中复杂的表达式。因而雅可比行列式就是 $\exp(-\mathbf s(\mathbf z_A,\mathbf w))$ 各元素之积。

这种方法的一个明显局限是：$\mathbf z_A$ 的值在变换中保持不变。增加一层并对调 $\mathbf z_A$ 与 $\mathbf z_B$ 的角色，就很容易解决这个问题，如图 18.2 所示。接着可以多次重复这一双层结构，形成一类非常灵活的生成模型。

整体训练过程先构造数据点的小批量，再从式 (18.4) 得到每个数据点对对数似然函数的贡献。对于 $\mathcal N(\mathbf z\mid\mathbf0,\mathbf I)$ 形式的潜变量分布，对数密度除了一个可加常数外，就是 $-\|\mathbf z\|^2/2$。计算逆变换 $\mathbf z=\mathbf g(\mathbf x)$ 时，依次应用式 (18.13) 形式的逆变换。类似地，雅可比行列式的对数是各层对数行列式之和，其中每一项本身又是 $-s_i(\mathbf z_A,\mathbf w)$ 形式的项之和。可用自动微分求出对数似然的梯度，再用随机梯度下降更新网络参数。

real NVP 模型属于范围更广的一类归一化流，称为**耦合流**。在这类模型中，式 (18.11) 的线性变换可以换成更一般的形式。

<!-- pdf-page: 564 -->

<figure id="fig-18-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-3.png" alt="real NVP 从二维高斯基础分布逐层变形成双月亮数据分布的六幅子图">
  <figcaption>图 18.3：real NVP 归一化流模型用于“双月亮”数据集的示意。(a) 高斯基础分布；(b) 只变换竖直轴后的分布；(c) 随后变换水平轴后的分布；(d) 第二次变换竖直轴后的分布；(e) 第二次变换水平轴后的分布；(f) 模型训练所用的数据集。</figcaption>
  <p class="figure-translation">图内 (a)–(f) 为六个阶段，含义与图注逐项对应；图中无其他英文。</p>
</figure>

具体形式为

$$
\mathbf x_B=\mathbf h\bigl(\mathbf z_B,\mathbf g(\mathbf z_A,\mathbf w)\bigr), \tag{18.15}
$$

其中 $\mathbf h(\mathbf z_B,\mathbf g)$ 是一种耦合函数：对任意给定的 $\mathbf g$ 值，它都能高效求逆。函数 $\mathbf g(\mathbf z_A,\mathbf w)$ 称为**条件器**（conditioner），通常用神经网络表示。

可以用一个简单的数据集说明 real NVP 归一化流，这个数据集有时称为“双月亮”，见图 18.3。这里用两个连续层将二维高斯分布变换成更复杂的分布；每层都交替变换两个维度中的一个。

## 18.2 自回归流

归一化流的一种相关形式可以从下述事实出发：一组变量的联合分布总能写成各变量条件分布的乘积（见第 11.1 节）。我们先为向量 $\mathbf x$ 中的变量选定一个顺序。

<!-- pdf-page: 565 -->

<figure id="fig-18-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-4.png" alt="自回归流的两种依赖图：掩码自回归流由先前输出决定后续输出，逆自回归流由先前潜变量决定后续输出">
  <figcaption>图 18.4：自回归归一化流的两种结构。(a) 掩码自回归流可高效计算似然函数；(b) 逆自回归流可高效采样。</figcaption>
  <p class="figure-translation">图内符号：$z_1,z_2,z_3,\ldots,z_n$ → 潜变量分量；$x_1,x_2,x_3,\ldots,x_n$ → 数据分量；(a)、(b) 分别对应图注中的两种结构。箭头表示计算依赖。</p>
</figure>

于是，不失一般性，可将联合分布写为

$$
p(x_1,\ldots,x_D)=\prod_{i=1}^{D}p(x_i\mid\mathbf x_{1:i-1}), \tag{18.16}
$$

其中 $\mathbf x_{1:i-1}$ 表示 $x_1,\ldots,x_{i-1}$。这种分解可用于构造一类称为**掩码自回归流**（masked autoregressive flow，MAF）的归一化流（Papamakarios、Pavlakou 和 Murray，2017），其形式为

$$
x_i=h\bigl(z_i,\mathbf g_i(\mathbf x_{1:i-1},\mathbf w_i)\bigr), \tag{18.17}
$$

如图 18.4(a) 所示。这里 $h(z_i,\cdot)$ 是耦合函数，选取时要求它易于针对 $z_i$ 求逆；$\mathbf g_i$ 是**条件器**，通常由深度神经网络表示。“掩码”一词指用单个神经网络实现一组式 (18.17) 形式的方程，同时用二值掩码（Germain 等，2015）强制部分网络权重为零，从而实现式 (18.16) 的自回归约束。

此时，为计算似然函数所需的逆向计算为

$$
z_i=h^{-1}\!\bigl(x_i,\mathbf g_i(\mathbf x_{1:i-1},\mathbf w_i)\bigr), \tag{18.18}
$$

它可以在现代硬件上高效进行，因为计算 $z_1,\ldots,z_D$ 所需的各个式 (18.18) 可以并行求值。这组变换 (18.18) 的雅可比矩阵包含 $\partial z_i/\partial x_j$，构成上三角矩阵，其行列式是主对角线元素之积，因此也能高效计算（见习题 18.4）。然而，从这个模型采样必须计算式 (18.17)。它本质上是顺序计算，因而较慢：在求出 $x_i$ 之前，必须先求出 $x_1,\ldots,x_{i-1}$。

**译注：** 原书正文在此称雅可比为“上三角”，但习题 18.4 称“下三角”。按 $z_i$ 仅依赖 $x_1,\ldots,x_i$ 及 $J_{ij}=\partial z_i/\partial x_j$，非零元素在主对角线及其下方；这里保留正文原词，习题按原文译为“下三角”。

为避免这种低效采样，也可改用**逆自回归流**（inverse autoregressive flow，IAF；Kingma 等，2016），形式为

$$
x_i=h\bigl(z_i,\widetilde{\mathbf g}_i(\mathbf z_{1:i-1},\mathbf w_i)\bigr), \tag{18.19}
$$

<!-- pdf-page: 566 -->

如图 18.4(b) 所示。现在采样很高效：给定一个 $\mathbf z$，用式 (18.19) 计算 $x_1,\ldots,x_D$ 的各分量可以并行完成。然而，计算似然函数所需的逆函数要进行一系列形式为

$$
z_i=h^{-1}\!\bigl(x_i,\widetilde{\mathbf g}_i(\mathbf z_{1:i-1},\mathbf w_i)\bigr) \tag{18.20}
$$

的计算。这些计算本质上是顺序的，因此较慢。具体应用会决定选用掩码自回归流还是逆自回归流。

可见耦合流与自回归流关系密切。自回归流引入了相当大的灵活性，但由于采样要依序进行，计算成本随数据空间的维度 $D$ 线性增长。耦合流可以看作自回归流的一个特例：它只把变量分成两组，而非 $D$ 组，因而牺牲一些一般性以换取效率。

## 18.3 连续流

本章考虑的最后一种归一化流方法，是用常微分方程（ordinary differential equation，ODE）定义深度神经网络。这可以视为层数无穷多的深度网络。我们先介绍神经 ODE 的概念，再看如何用它构造归一化流模型。

### 18.3.1 神经微分方程

我们已经看到，神经网络往往由很多处理层组成时特别有用，因此可以问：若把层数推至无穷大，会发生什么？考虑一个残差网络，每个处理层都通过向输入向量加上某个带参数的非线性函数，产生输出：

$$
\mathbf z^{(t+1)}=\mathbf z^{(t)}+\mathbf f(\mathbf z^{(t)},\mathbf w), \tag{18.21}
$$

其中 $t=1,\ldots,T$ 标记网络各层。注意，每层使用同一个函数和共享的参数向量 $\mathbf w$，这样在保持参数数量有界的同时，可以考虑任意多的层。设想不断增加层数，同时让每层引入的变化相应减小。取极限后，隐藏单元激活向量成为连续变量 $t$ 的函数 $\mathbf z(t)$，它在网络中的演化可表示为微分方程（见习题 18.5）：

$$
\frac{\mathrm d\mathbf z(t)}{\mathrm dt}=\mathbf f(\mathbf z(t),\mathbf w). \tag{18.22}
$$

这里 $t$ 常被称为“时间”。式 (18.22) 的形式称为**神经常微分方程**，简称**神经 ODE**（Chen 等，2018）。其中“常”表示方程只有一个独立变量 $t$。

<!-- pdf-page: 567 -->

<figure id="fig-18-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-5.png" alt="五层残差网络与连续神经常微分方程网络的路径对比图">
  <figcaption>图 18.5：传统分层网络与神经微分方程的对比。左图为五层残差网络，展示若干标量输入初值的轨迹；右图为连续神经 ODE 的数值积分结果。右图的函数并非在均匀间隔的时间点求值；数值求解器会根据输入取值自适应选择求值点。［经 Chen 等（2018）许可转载。］</figcaption>
  <p class="figure-translation">图内文字：Residual Network → 残差网络；ODE Network → ODE 网络；Depth → 深度；Input/Hidden/Output → 输入／隐藏／输出。黑点为网络层或求解器选择的求值点，曲线显示不同输入的轨迹。</p>
</figure>

若用向量 $\mathbf z(0)$ 表示网络输入，则输出 $\mathbf z(T)$ 可通过对微分方程积分得到：

$$
\mathbf z(T)=\int_0^T\mathbf f(\mathbf z(t),\mathbf w)\,\mathrm dt. \tag{18.23}
$$

**译注：** 对一般初值 $\mathbf z(0)$，右边还应加上 $\mathbf z(0)$。原书式 (18.23) 未写这一项，也未限定初值为零；这里保留原式。

可以用标准数值积分软件包计算这个积分。求解微分方程最简单的方法是**欧拉前向积分法**，对应式 (18.21)。实际中，更强大的数值积分算法能够自适应地选择函数求值点。特别是，它们选择的 $t$ 值通常不是均匀间隔的。在传统分层网络中，深度对应层数；这里则由函数求值次数取代。图 18.5 对比了标准分层神经网络与神经微分方程。

### 18.3.2 神经 ODE 的反向传播

现在需要解决如何训练神经 ODE：通过最小化损失函数来确定 $\mathbf w$。假设数据集包含网络输入向量 $\mathbf z(0)$，以及对应的输出目标向量；损失函数 $L(\cdot)$ 依赖输出向量 $\mathbf z(T)$。一种方法是用自动微分对前向传播期间 ODE 求解器执行的全部操作求导（见第 8.2 节）。虽然

<!-- pdf-page: 568 -->
<!-- join-previous-paragraph -->

这并不难实现，但内存成本很高，在控制数值误差方面也不理想。Chen 等（2018）改为把 ODE 求解器视为黑箱，并使用一种称为**伴随敏感度方法**（adjoint sensitivity method）的技术；它可视为显式反向传播的连续版本。回顾一下，对每个数据点，反向传播包含三个连续阶段：先前向传播，求出网络每层的激活向量；再从输出端开始，利用微积分的链式法则向后传播，求损失对各层激活值的导数；最后，将前向传播的激活值与反向传播的梯度相乘，求出对网络参数的导数。计算神经 ODE 的梯度时，也有相应的步骤（见第 8 章）。

为了将反向传播用于神经 ODE，定义一个称为**伴随量**（adjoint）的量：

$$
\mathbf a(t)=\frac{\mathrm dL}{\mathrm d\mathbf z(t)}. \tag{18.24}
$$

可见 $\mathbf a(T)$ 对应通常的损失对输出向量的导数。伴随量满足自身的微分方程（见习题 18.6）：

$$
\frac{\mathrm d\mathbf a(t)}{\mathrm dt}=-\mathbf a(t)^\mathsf T\nabla_{\mathbf z}\mathbf f(\mathbf z(t),\mathbf w), \tag{18.25}
$$

这是微积分链式法则的连续形式。可从 $\mathbf a(T)$ 出发向后积分，仍可用黑箱 ODE 求解器。原则上，这要求存储前向传播期间计算出的整条轨迹 $\mathbf z(t)$；如果反向求解器希望在不同于前向求解器的 $t$ 值上求值，这会造成问题。为此，只须从输出值 $\mathbf z(T)$ 出发，沿式 (18.25) 反向积分时，同时积分式 (18.22)，即可重新计算所需的 $\mathbf z(t)$。

反向传播方法的第三步，是把激活值和梯度适当地相乘，求损失对网络参数的导数。在常规网络中，如果一个参数值由多个连接共享，总导数就是各连接的导数之和（见习题 9.7）。对于整个网络共享同一参数向量 $\mathbf w$ 的神经 ODE，这个求和变为对 $t$ 的积分，形式为（见习题 18.7）：

$$
\nabla_{\mathbf w}L=-\int_0^T\mathbf a(t)^\mathsf T\nabla_{\mathbf w}\mathbf f(\mathbf z(t),\mathbf w)\,\mathrm dt. \tag{18.26}
$$

式 (18.25) 中的 $\nabla_{\mathbf z}\mathbf f$ 和式 (18.26) 中的 $\nabla_{\mathbf w}\mathbf f$，均可用自动微分高效求值。注意，上述结果也适用于更一般的神经网络函数 $\mathbf f(\mathbf z(t),t,\mathbf w)$，其中除通过 $\mathbf z(t)$ 产生隐式依赖外，还显式依赖 $t$（见第 8.2 节）。

与传统分层网络相比，用伴随方法训练神经 ODE 的一个好处是无须存储前向传播的中间结果，因此内存成本为常数。此外，

<!-- pdf-page: 569 -->
<!-- join-previous-paragraph -->

神经 ODE 能自然处理连续时间数据，其中观测可以在任意时刻发生。如果误差函数 $L$ 还依赖于输出以外的某些 $\mathbf z(t)$ 值，逆向求解器就需要运行多次：每对相邻的输出值之间运行一次，从而把单次求解拆成多段连续求解，以访问中间状态（Chen 等，2018）。注意，训练期间可提高求解器精度；在计算资源有限的推断应用中，则可以使用较低精度和较少的函数求值次数。

### 18.3.3 神经 ODE 流

可以利用神经常微分方程，以另一种方法构造可求解的归一化流模型。神经 ODE 通过下式微分方程，定义从输入向量 $\mathbf z(0)$ 到输出向量 $\mathbf z(T)$ 的高度灵活的变换：

$$
\frac{\mathrm d\mathbf z(t)}{\mathrm dt}=\mathbf f(\mathbf z(t),\mathbf w). \tag{18.27}
$$

若在输入向量上定义基础分布 $p(\mathbf z(0))$，神经 ODE 随时间向前传播后，在每个 $t$ 都产生一个分布 $p(\mathbf z(t))$，最终得到输出分布 $p(\mathbf z(T))$。Chen 等（2018）表明，对神经 ODE，可通过积分以下微分方程来计算密度的变换（见习题 18.8）：

$$
\frac{\mathrm d\ln p(\mathbf z(t))}{\mathrm dt}=-\operatorname{Tr}\!\left(\frac{\partial\mathbf f}{\partial\mathbf z(t)}\right), \tag{18.28}
$$

其中 $\partial\mathbf f/\partial\mathbf z$ 是雅可比矩阵，其元素为 $\partial f_i/\partial z_j$。可以用标准 ODE 求解器进行这一积分。同样，也可以从选定的基础密度 $p(\mathbf z(0))$ 中采样；基础密度通常是高斯分布等简单分布。再利用 ODE 求解器积分式 (18.27)，将各样本传播至输出。所得框架称为**连续归一化流**，如图 18.6 所示。连续归一化流可用训练神经 ODE 的伴随敏感度方法进行训练；该方法可视为反向传播在连续时间中的对应形式（见第 18.3.1 节）。

**译注：** 原书此处指向第 18.3.1 节；伴随敏感度方法实际在第 18.3.2 节讨论。

式 (18.28) 涉及雅可比矩阵的迹，而不是离散归一化流中的行列式，因此看上去可能更高效。一般情况下，计算 $D\times D$ 矩阵的行列式需要 $O(D^3)$ 次运算，而计算迹只需 $O(D)$ 次。然而，如果所求的是下三角矩阵的行列式，它就等于对角元素之积，也只涉及 $O(D)$ 次运算。由于计算雅可比矩阵的每一个元素都需要一次独立的前向传播，而一次前向传播本身需要 $O(D)$ 次运算，因此整体计算迹或下三角矩阵的行列式都需要 $O(D^2)$ 次运算。不过，可以用 **Hutchinson 迹估计量**（Grathwohl 等，2018）把计算迹的成本降到 $O(D)$。其定义如下。

<!-- pdf-page: 570 -->

<figure id="fig-18-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-6.png" alt="一维高斯基础分布随连续流线演化成多峰分布的示意图">
  <figcaption>图 18.6：连续归一化流示意图。$t=0$ 时的简单高斯分布连续变换为 $t=T$ 时的多峰分布。流线显示 $z$ 轴上的点如何随 $t$ 演化；流线散开之处密度降低，聚拢之处密度升高。</figcaption>
  <p class="figure-translation">图内符号：$p(\mathbf z(0))$ → 初始分布；$p(\mathbf z(T))$ → 输出分布；$t$ → 时间；$T$ → 终止时刻；$z$ → 一维状态变量。曲线与箭头的含义见图注。</p>
</figure>

对于矩阵 $\mathbf A$，有

$$
\operatorname{Tr}(\mathbf A)=\mathbb E_{\boldsymbol\epsilon}\!\left[\boldsymbol\epsilon^\mathsf T\mathbf A\boldsymbol\epsilon\right], \tag{18.29}
$$

其中 $\boldsymbol\epsilon$ 是均值为零、协方差为单位矩阵的随机向量，例如来自高斯分布 $\mathcal N(\mathbf0,\mathbf I)$。对于给定的 $\boldsymbol\epsilon$，可在单次使用反向模式自动微分的过程中高效计算矩阵向量积 $\mathbf A\boldsymbol\epsilon$。因此，可用有限个样本近似迹：

$$
\operatorname{Tr}(\mathbf A)\simeq\frac1M\sum_{m=1}^{M}\boldsymbol\epsilon_m^\mathsf T\mathbf A\boldsymbol\epsilon_m. \tag{18.30}
$$

实际中可以设 $M=1$，即每个新数据点只使用一个重新抽取的样本。虽然估计有噪声，但它本来就是带噪声的随机梯度下降过程的一部分，因此影响可能并不严重。关键在于估计无偏，即估计量的期望等于真值（见习题 18.11）。

使用一种称为**流匹配**（flow matching）的技术，可以显著提高连续归一化流的训练效率（Lipman 等，2022）。它使归一化流更接近扩散模型（见第 20 章）：训练时不再需要通过积分器进行反向传播，同时大幅降低内存需求，使推断更快、训练更稳定。

<!-- pdf-page: 571 -->

## 习题

**18.1（★★）** 考虑变换 $\mathbf x=\mathbf f(\mathbf z)$ 及其逆变换 $\mathbf z=\mathbf g(\mathbf x)$。对 $\mathbf x=\mathbf f(\mathbf g(\mathbf x))$ 求导，证明

$$
\mathbf J\mathbf K=\mathbf I, \tag{18.31}
$$

其中 $\mathbf I$ 是单位矩阵，$\mathbf J$ 和 $\mathbf K$ 的元素分别为

$$
J_{ij}=\frac{\partial g_i}{\partial x_j},\qquad K_{ij}=\frac{\partial f_i}{\partial z_j}. \tag{18.32}
$$

利用矩阵乘积的行列式等于各矩阵行列式之积，证明

$$
\det(\mathbf J)=\frac1{\det(\mathbf K)}. \tag{18.33}
$$

由此证明，式 (18.1) 的变量变换密度公式可改写为

$$
p_x(\mathbf x)=p_z(\mathbf g(\mathbf x))\,|\det\mathbf K|^{-1}, \tag{18.34}
$$

其中 $\mathbf K$ 在 $\mathbf z=\mathbf g(\mathbf x)$ 处计算。

**18.2（★）** 考虑一串形式为

$$
\mathbf x=\mathbf f_1\!\left(\mathbf f_2\!\left(\cdots\mathbf f_{M-1}\!\left(\mathbf f_M(\mathbf z)\right)\cdots\right)\right) \tag{18.35}
$$

的可逆变换。证明逆函数为

$$
\mathbf z=\mathbf f_M^{-1}\!\left(\mathbf f_{M-1}^{-1}\!\left(\cdots\mathbf f_2^{-1}\!\left(\mathbf f_1^{-1}(\mathbf x)\right)\cdots\right)\right). \tag{18.36}
$$

**18.3（★）** 考虑如下线性变量变换：

$$
\mathbf x=\mathbf z+\mathbf b. \tag{18.37}
$$

证明这个变换的雅可比矩阵是单位矩阵。比较 $\mathbf z$ 空间中一个小区域的体积与 $\mathbf x$ 空间中对应区域的体积，并解释这一结果。

**18.4（★★）** 证明式 (18.18) 给出的自回归归一化流变换的雅可比矩阵是下三角矩阵。此类矩阵的行列式等于主对角线上各元素的乘积，因此容易计算。

**18.5（★）** 考虑式 (18.21) 给出的残差网络前向传播方程，其中“时间”变量 $t$ 有一个很小的增量 $\epsilon$：

$$
\mathbf z^{(t+\epsilon)}=\mathbf z^{(t)}+\epsilon\mathbf f(\mathbf z^{(t)},\mathbf w). \tag{18.38}
$$

这里，神经网络函数的加性贡献由 $\epsilon$ 缩放。注意，式 (18.21) 对应于 $\epsilon=1$。通过取极限 $\epsilon\to0$，推导式 (18.22) 给出的前向传播微分方程。

<!-- pdf-page: 572 -->

**18.6（★★）** 本题和下一题将非正式地推导神经 ODE 的反向传播及梯度计算方程。更形式化的推导见 Chen 等（2018）。写出与前向方程 (18.38) 对应的反向传播方程。取极限 $\epsilon\to0$，推导式 (18.25) 的反向传播方程；其中 $\mathbf a(t)$ 由式 (18.24) 定义。

**18.7（★★）** 利用式 (8.10) 的结果，为式 (18.38) 定义、所有层共享同一参数向量 $\mathbf w$ 的多层残差网络，写出损失函数 $L(\mathbf z(T))$ 的梯度表达式。取极限 $\epsilon\to0$，推导损失函数导数的式 (18.26)。

**18.8（★★★）** 本题将对一维分布非正式地推导式 (18.28)。考虑时间 $t$ 的分布 $q(z)$；由于从 $z$ 到 $x$ 的变换，它在时间 $t+\delta t$ 变为新的分布 $p(x)$。再考虑与图 18.7 一致的邻近取值 $z$ 与 $z+\Delta z$，以及对应的取值 $x$ 与 $x+\Delta x$。首先，写出一个方程，表示区间 $\Delta z$ 内的概率质量与区间 $\Delta x$ 内的概率质量相同。其次，写出一个方程，用导数 $\mathrm dq(t)/\mathrm dt$ 表示密度从 $t$ 到 $t+\delta t$ 的变化。第三，引入演化函数 $f(z)=\mathrm dz/\mathrm dt$，写出一个方程，用 $\Delta z$ 表示 $\Delta x$。最后，综合这三个方程并取极限 $\delta t\to0$，证明

$$
\frac{\mathrm d}{\mathrm dt}\ln q(z)=-f'(z), \tag{18.39}
$$

这是一维版本的式 (18.28)。

<figure id="fig-18-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-18/fig-18-7.png" alt="一维连续归一化流在时间 t 到 t 加 δt 间变换概率密度的示意">
  <figcaption>图 18.7：一维连续归一化流的方程推导所用的概率密度变换示意图。</figcaption>
  <p class="figure-translation">图内符号：$q(z)$ → 时刻 $t$ 的密度；$p(x)$ → 时刻 $t+\delta t$ 的密度；$z,z+\Delta z$ → 原空间的邻近位置；$x,x+\Delta x$ → 变换后的邻近位置；$t,t+\delta t$ → 变换前后的时刻。箭头表示位置的映射。</p>
</figure>

**18.9（★★）** 绘制图 18.6 的流线时，在每个 $t$ 值上取一组等间隔的数，并用累积分布函数的逆函数找出 $z$ 空间中的对应位置。证明：这等价于用微分方程 (18.27) 计算流线，其中 $\mathbf f$ 由式 (18.28) 定义。

**译注：** 原书习题 18.9 称流场 $\mathbf f$ “由式 (18.28) 定义”；式 (18.28) 实为密度的演化方程，流场出现在式 (18.27)。题目引用照录。

**18.10（★★）** 利用微分方程 (18.27)，写出连续归一化流的基础密度关于输出密度的表达式，用关于 $t$ 的积分表示。由此利用定积分变号相当于交换积分上下限这一事实，证明对连续归一化流求逆的计算成本与正向流相同。

**译注：** 原书习题 18.10 仅提式 (18.27)；把密度写成积分还需要式 (18.28) 给出的密度变化关系。

<!-- pdf-page: 573 -->

**18.11（★）** 证明：Hutchinson 迹估计量 (18.30) 右侧的期望对任意 $M$ 都等于 $\operatorname{Tr}(\mathbf A)$。这表明该估计量是无偏的。
