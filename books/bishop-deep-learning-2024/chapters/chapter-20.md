# 第 20 章 扩散模型

<aside class="chapter-guide"><strong>本章导读</strong><p>本章先把逐步加噪写成固定的前向编码过程，再训练神经网络逐步去噪，从高斯噪声生成新样本。随后从证据下界和得分匹配两个角度推导训练方法，最后讨论如何引导生成结果。</p></aside>

<!-- pdf-page: 591 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/chapter-opener.png" alt="第 20 章 Diffusion Models 的彩色抽象章首页图">
  <p class="figure-translation">图内文字：Diffusion Models → 扩散模型。</p>
</figure>

前面已经看到，构造表达能力强的生成模型的一种有效方法，是先给潜变量 $\mathbf z$ 定义分布 $p(\mathbf z)$，再通过深度神经网络将 $\mathbf z$ 变换到数据空间 $\mathbf x$。$p(\mathbf z)$ 只需采用简单、固定的分布，例如高斯分布 $\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I)$；神经网络的灵活性会使 $\mathbf x$ 上的分布具有很强的表达能力。前几章探讨了符合这一框架的几种模型，它们用不同的方法定义和训练深度神经网络，分别基于生成对抗网络、变分自编码器和归一化流。

本章介绍这一框架中的第四类模型：**扩散模型**（diffusion models），也称**去噪扩散概率模型**（denoising diffusion probabilistic models，DDPM；Sohl-Dickstein 等，2015；Ho、Jain 和 Abbeel，2020）。它们已在许多应用中达到领先水平。为便于说明，我们重点讨论图像数据，尽管这一框架的适用范围

<!-- pdf-page: 592 -->
<!-- join-previous-paragraph -->

更广（见第 16.4.4 节）。

<figure id="fig-20-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-1.png" alt="一张猫的图像经过多轮加性高斯噪声后逐渐变为纯噪声">
  <figcaption>图 20.1：扩散模型的编码过程。一张图像经过多轮加性高斯噪声扰动，形成噪声逐渐增强的图像序列。经过大量 $T$ 步后，结果与从高斯分布抽取的样本难以区分。随后训练深度神经网络来逆转这一过程。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf x$ → 原始图像；$\mathbf z_1,\mathbf z_2$ → 逐步加噪的图像；$\mathbf z_T$ → 最后的噪声图像。</p>
</figure>

核心思路是对每张训练图像施加多步噪声过程，把它变为高斯分布的一个样本，如图 20.1 所示。然后训练深度神经网络来逆转这一过程。训练完成后，网络便能以高斯分布的样本为输入，生成新图像。

扩散模型可视为一种层次化的变分自编码器：编码器分布由噪声过程固定定义，只学习生成分布（Luo，2022；见第 19.2 节）。它们易于训练，能很好地利用并行硬件；不必面对对抗训练的挑战和不稳定性，却能生成质量与生成对抗网络相当或更好的结果。不过，生成新样本需要反复运行解码器网络，计算成本可能很高（Dhariwal 和 Nichol，2021）。

## 20.1 前向编码器

从训练集中取一幅图像，记为 $\mathbf x$。对每个像素分别混入高斯噪声，得到受噪声扰动的图像 $\mathbf z_1$：

$$
\mathbf z_1=\sqrt{1-\beta_1}\,\mathbf x+\sqrt{\beta_1}\,\boldsymbol\epsilon_1, \tag{20.1}
$$

其中 $\boldsymbol\epsilon_1\sim\mathcal N(\boldsymbol\epsilon_1\mid\mathbf 0,\mathbf I)$，$\beta_1<1$ 是噪声分布的方差。在式 (20.1) 和 (20.3) 中选用 $\sqrt{1-\beta_1}$ 与 $\sqrt{\beta_1}$ 作为系数，可保证 $\mathbf z_t$ 的分布均值比 $\mathbf z_{t-1}$ 更接近零，方差比 $\mathbf z_{t-1}$ 更接近单位矩阵（习题 20.1）。也可把变换 (20.1) 写为（习题 20.2）

$$
q(\mathbf z_1\mid\mathbf x)=\mathcal N(\mathbf z_1\mid\sqrt{1-\beta_1}\,\mathbf x,\beta_1\mathbf I). \tag{20.2}
$$

接下来反复加入独立的高斯噪声，得到噪声逐渐增强的图像序列 $\mathbf z_2,\ldots,\mathbf z_T$。扩散模型文献有时把这些潜变量写作 $\mathbf x_1,\ldots,\mathbf x_T$，把观测变量写作 $\mathbf x_0$；为与本书其他章节一致，我们用 $\mathbf z$ 表示潜变量，用 $\mathbf x$

<!-- pdf-page: 593 -->
<!-- join-previous-paragraph -->

表示观测变量。

<figure id="fig-20-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-2.png" alt="扩散模型的概率图：红色箭头表示逐步加噪，蓝色箭头表示学习到的逆过程，绿色虚线表示以原图为条件的逆分布">
  <figcaption>图 20.2：扩散过程的概率图模型。阴影节点表示已观测的原图 $\mathbf x$，受噪声扰动的图像 $\mathbf z_1,\ldots,\mathbf z_T$ 是潜变量。前向分布 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 定义噪声过程，可视为编码器。我们希望学习模型 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$ 来逆转加噪过程，可视为解码器。条件分布 $q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$ 将在训练过程的定义中发挥重要作用。</figcaption>
  <p class="figure-translation">图内符号：$q(\mathbf z_t\mid\mathbf z_{t-1})$ → 前向加噪分布；$p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$ → 学习到的逆向生成分布；$q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$ → 以原图为条件的逆向分布。</p>
</figure>

每一步的图像为

$$
\mathbf z_t=\sqrt{1-\beta_t}\,\mathbf z_{t-1}+\sqrt{\beta_t}\,\boldsymbol\epsilon_t, \tag{20.3}
$$

其中 $\boldsymbol\epsilon_t\sim\mathcal N(\boldsymbol\epsilon_t\mid\mathbf 0,\mathbf I)$。同样，式 (20.3) 可写成

$$
q(\mathbf z_t\mid\mathbf z_{t-1})
=\mathcal N(\mathbf z_t\mid\sqrt{1-\beta_t}\,\mathbf z_{t-1},\beta_t\mathbf I). \tag{20.4}
$$

式 (20.4) 的条件分布序列构成一条马尔可夫链，可表示成图 20.2 的概率图模型（见第 11.3 节）。方差参数 $\beta_t\in(0,1)$ 的取值由人工设定，通常按照预先规定的方案沿链递增，即 $\beta_1<\beta_2<\cdots<\beta_T$。

### 20.1.1 扩散核

给定观测数据向量 $\mathbf x$ 时，潜变量的联合分布为

$$
q(\mathbf z_1,\ldots,\mathbf z_t\mid\mathbf x)
=q(\mathbf z_1\mid\mathbf x)\prod_{\tau=2}^{t}q(\mathbf z_\tau\mid\mathbf z_{\tau-1}). \tag{20.5}
$$

将中间变量 $\mathbf z_1,\ldots,\mathbf z_{t-1}$ 边缘化，就得到**扩散核**（diffusion kernel；习题 20.3）：

$$
q(\mathbf z_t\mid\mathbf x)
=\mathcal N(\mathbf z_t\mid\sqrt{\alpha_t}\,\mathbf x,(1-\alpha_t)\mathbf I), \tag{20.6}
$$

其中定义

$$
\alpha_t=\prod_{\tau=1}^{t}(1-\beta_\tau). \tag{20.7}
$$

<!-- pdf-page: 594 -->

可见，每个中间分布都是简单的闭式高斯分布，能直接从中采样。这在训练 DDPM 时很有用：我们可以随机选取马尔可夫链中的中间项，使用高效的随机梯度下降，而无须运行整条链。也可将式 (20.6) 写成

$$
\mathbf z_t=\sqrt{\alpha_t}\,\mathbf x+\sqrt{1-\alpha_t}\,\boldsymbol\epsilon_t, \tag{20.8}
$$

其中 $\boldsymbol\epsilon_t\sim\mathcal N(\boldsymbol\epsilon_t\mid\mathbf 0,\mathbf I)$。注意，此处 $\boldsymbol\epsilon_t$ 表示相对于原图累积加入的总噪声，而不再只是马尔可夫链这一步加入的增量噪声。

经过许多步后，图像与高斯噪声难以区分；在 $T\to\infty$ 的极限下，有（习题 20.4）

$$
q(\mathbf z_T\mid\mathbf x)=\mathcal N(\mathbf z_T\mid\mathbf 0,\mathbf I), \tag{20.9}
$$

因此，关于原始图像的全部信息都已丢失。式 (20.3) 中的系数 $\sqrt{1-\beta_t}$ 与 $\sqrt{\beta_t}$ 可保证：马尔可夫链一旦收敛到零均值、单位协方差的分布，后续更新会使该分布保持不变（习题 20.5）。

由于式 (20.9) 右边与 $\mathbf x$ 无关，$\mathbf z_T$ 的边缘分布为

$$
q(\mathbf z_T)=\mathcal N(\mathbf z_T\mid\mathbf 0,\mathbf I). \tag{20.10}
$$

式 (20.4) 的马尔可夫链通常称为**前向过程**，它类似于 VAE 的编码器，只是这里固定不变，不需要学习。要注意，归一化流文献通常采用相反的术语：它们把从潜空间到数据空间的映射称为前向过程。

### 20.1.2 条件分布

我们的目标是学会撤销加噪过程，因此自然会考虑条件分布 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 的逆向形式。由贝叶斯定理，

$$
q(\mathbf z_{t-1}\mid\mathbf z_t)
=\frac{q(\mathbf z_t\mid\mathbf z_{t-1})q(\mathbf z_{t-1})}{q(\mathbf z_t)}. \tag{20.11}
$$

边缘分布 $q(\mathbf z_{t-1})$ 可写为

$$
q(\mathbf z_{t-1})=\int q(\mathbf z_{t-1}\mid\mathbf x)p(\mathbf x)\,\mathrm d\mathbf x, \tag{20.12}
$$

其中 $q(\mathbf z_{t-1}\mid\mathbf x)$ 是式 (20.6) 给出的条件高斯分布。然而，这个边缘分布难以处理，因为需要对未知的数据密度 $p(\mathbf x)$ 积分。若用训练数据集中的样本近似积分，得到的会是复杂的高斯混合分布。

<!-- pdf-page: 595 -->

因此，转而考虑以原始数据向量 $\mathbf x$ 为条件的逆向分布 $q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$。稍后会看到，它是简单的高斯分布。这也符合直觉：只看到一张带噪图像时，很难猜到是哪张噪声较少的图像产生了它；若同时知道起始图像，问题便容易许多。使用贝叶斯定理，得到

$$
q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)
=\frac{q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)q(\mathbf z_{t-1}\mid\mathbf x)}{q(\mathbf z_t\mid\mathbf x)}. \tag{20.13}
$$

利用前向过程的马尔可夫性质，

$$
q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)
=q(\mathbf z_t\mid\mathbf z_{t-1}), \tag{20.14}
$$

右边由式 (20.4) 给出。将其看作 $\mathbf z_{t-1}$ 的函数，它是一个二次型的指数。式 (20.13) 分子中的 $q(\mathbf z_{t-1}\mid\mathbf x)$ 是式 (20.6) 的扩散核，同样含有关于 $\mathbf z_{t-1}$ 的二次型指数。分母对 $\mathbf z_{t-1}$ 为常数，可以略去。因此，式 (20.13) 右边是高斯分布。通过“配方”可求出均值与协方差（习题 20.6）：

$$
q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)
=\mathcal N\!\left(\mathbf z_{t-1}\mid\mathbf m_t(\mathbf x,\mathbf z_t),\sigma_t^2\mathbf I\right), \tag{20.15}
$$

其中

$$
\mathbf m_t(\mathbf x,\mathbf z_t)
=\frac{(1-\alpha_{t-1})\sqrt{1-\beta_t}\,\mathbf z_t
+\sqrt{\alpha_{t-1}}\,\beta_t\mathbf x}{1-\alpha_t}, \tag{20.16}
$$

$$
\sigma_t^2=\frac{\beta_t(1-\alpha_{t-1})}{1-\alpha_t}, \tag{20.17}
$$

这里使用了式 (20.7)。

## 20.2 逆向解码器

前向编码器由一系列高斯条件分布 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 定义；直接将其反转，却得到难以处理的 $q(\mathbf z_{t-1}\mid\mathbf z_t)$。原因是，这需要对所有可能的初始向量 $\mathbf x$ 积分，而它们服从我们希望建模的未知数据分布 $p(\mathbf x)$。因此，我们改为学习一个逆向分布的近似 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$，由深度神经网络控制，$\mathbf w$ 表示网络的权重与偏置。这一步逆向变换类似于变分自编码器的解码器（见第 19 章），如图 20.2 所示。训练完成后，可从 $\mathbf z_T$ 上的简单高斯分布采样，再重复应用已训练网络进行一系列逆向采样，最终得到来自数据分布 $p(\mathbf x)$ 的样本。

<!-- pdf-page: 596 -->

<figure id="fig-20-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-3.png" alt="一元扩散变量在大噪声方差时的前向高斯分布、逆向多峰分布及边缘分布">
  <figcaption>图 20.3：一元变量中，利用贝叶斯定理 (20.13) 计算逆向分布 $q(z_{t-1}\mid z_t)$ 的示例。右图红线表示边缘分布 $q(z_{t-1})$，用三个高斯分布的混合示意；左图表示以前一步值 $z_{t-1}$ 为中心的高斯前向噪声分布 $q(z_t\mid z_{t-1})$。两者相乘并归一化后，对于给定的 $z_t$，得到右图蓝线所示的 $q(z_{t-1}\mid z_t)$。左图分布较宽，对应较大的方差 $\beta_t$，因此逆向分布呈复杂的多峰形状。</figcaption>
</figure>

**译注：** 图 20.3 的原书图注引用式 (20.13)；该式在给定原始 $\mathbf x$ 时定义逆向条件分布，而图中无条件的 $q(\mathbf z_{t-1}\mid\mathbf z_t)$ 对应式 (20.11)。这里保留原图注编号。

直观地说，若使方差保持较小，即 $\beta_t\ll1$，潜向量在相邻步骤间的变化就较小，因而更容易学习逆向变换。更具体地说，$\beta_t\ll1$ 时，$q(\mathbf z_{t-1}\mid\mathbf z_t)$ 近似为关于 $\mathbf z_{t-1}$ 的高斯分布。由式 (20.11) 可看出：其右边对 $\mathbf z_{t-1}$ 的依赖来自 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 和 $q(\mathbf z_{t-1})$。如果前者是足够窄的高斯分布，那么在它具有显著概率质量的区域，后者变化很小；因此，逆向分布也近似高斯。图 20.3 和 20.4 用简单例子说明这种直觉。不过，每一步方差较小时，必须使用大量步骤，才能使前向加噪所得的最后一个潜变量 $\mathbf z_T$ 的分布仍接近高斯，这又提高了生成新样本的成本。实际中，$T$ 可能达到几千。

<figure id="fig-20-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-4.png" alt="一元扩散变量在小噪声方差时的前向窄高斯分布与近似高斯的逆向分布">
  <figcaption>图 20.4：与图 20.3 相同，但左图的高斯分布 $q(z_t\mid z_{t-1})$ 具有小得多的方差 $\beta_t$。右图蓝线所示的对应逆向分布 $q(z_{t-1}\mid z_t)$ 接近高斯分布，方差也与前向分布相近。</figcaption>
</figure>

更正式的说明方法，是将 $\ln q(\mathbf z_{t-1}\mid\mathbf z_t)$ 视为 $\mathbf z_{t-1}$ 的函数，在 $\mathbf z_t$ 处作泰勒级数展开，

<!-- pdf-page: 597 -->
<!-- join-previous-paragraph -->

从而看出 $q(\mathbf z_{t-1}\mid\mathbf z_t)$ 近似高斯。这也表明，当方差较小时，逆向分布的协方差接近前向噪声过程的协方差 $\beta_t\mathbf I$（习题 20.7）。因此，我们用如下高斯分布建模逆向过程：

$$
p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)
=\mathcal N(\mathbf z_{t-1}\mid\boldsymbol\mu(\mathbf z_t,\mathbf w,t),\beta_t\mathbf I). \tag{20.18}
$$

其中，$\boldsymbol\mu(\mathbf z_t,\mathbf w,t)$ 是由参数 $\mathbf w$ 控制的深度神经网络。注意，网络显式接收步骤索引 $t$ 作为输入，以适应链上不同步骤的方差 $\beta_t$ 的变化。这使得我们可以用同一个网络逆转马尔可夫链中的所有步骤，而不必为每一步学习一个独立的网络。也可以为网络增加输出，使其学习去噪过程的协方差，刻画 $\mathbf z_t$ 附近 $q(\mathbf z_{t-1})$ 分布的曲率（Nichol 和 Dhariwal，2021）。用于建模 $\boldsymbol\mu(\mathbf z_t,\mathbf w,t)$ 的神经网络架构有很大选择空间，只须保证输出与输入维度相同。满足这一限制时，U-net 是图像处理应用的常见选择（见第 10.5.4 节）。

整个逆向去噪过程构成马尔可夫链，其联合分布为

$$
p(\mathbf x,\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf w)
=p(\mathbf z_T)\left\{\prod_{t=2}^{T}p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)\right\}
p(\mathbf x\mid\mathbf z_1,\mathbf w). \tag{20.19}
$$

这里假设 $p(\mathbf z_T)$ 与 $q(\mathbf z_T)$ 相同，故为 $\mathcal N(\mathbf z_T\mid\mathbf 0,\mathbf I)$。模型训练好后，采样很直接：先从简单高斯分布 $p(\mathbf z_T)$ 采样，再依次从各条件分布 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$ 采样，最后从 $p(\mathbf x\mid\mathbf z_1,\mathbf w)$ 采样，得到数据空间中的样本 $\mathbf x$。

### 20.2.1 训练解码器

下一步要为神经网络选择训练目标。最明显的选择是似然函数；对数据点 $\mathbf x$，它为

$$
p(\mathbf x\mid\mathbf w)=\int\cdots\int
p(\mathbf x,\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf w)
\,\mathrm d\mathbf z_1\cdots\mathrm d\mathbf z_T, \tag{20.20}
$$

其中联合分布由式 (20.19) 定义。这是一般潜变量模型 (16.81) 的一个实例，潜变量为 $\mathbf z=(\mathbf z_1,\ldots,\mathbf z_T)$，观测变量为 $\mathbf x$。所有潜变量都与数据空间维度相同；归一化流也是如此，但变分自编码器或生成对抗网络并不要求这一点。式 (20.20) 的似然需要对所有可能产生所观测数据点的噪声轨迹积分。由于积分包含高度复杂的神经网络函数，式 (20.20) 无法直接求解。

<!-- pdf-page: 598 -->

### 20.2.2 证据下界

精确似然难以求解，可以仿照变分自编码器，最大化对数似然的下界，即**证据下界**（evidence lower bound，ELBO；见第 16.3 节）。下面在扩散模型的语境下重新推导。对任意选取的分布 $q(\mathbf z)$，下列关系始终成立：

$$
\ln p(\mathbf x\mid\mathbf w)
=\mathcal L(\mathbf w)
+\operatorname{KL}\!\left(q(\mathbf z)\,\Vert\,p(\mathbf z\mid\mathbf x,\mathbf w)\right), \tag{20.21}
$$

其中 $\mathcal L$ 为证据下界，也称变分下界：

$$
\mathcal L(\mathbf w)
=\int q(\mathbf z)\ln\!\left\{\frac{p(\mathbf x,\mathbf z\mid\mathbf w)}{q(\mathbf z)}\right\}
\,\mathrm d\mathbf z. \tag{20.22}
$$

两个概率密度 $f(\mathbf z)$ 与 $g(\mathbf z)$ 之间的 Kullback–Leibler 散度定义为（见第 2.5.7 节）

$$
\operatorname{KL}\!\left(f(\mathbf z)\,\Vert\,g(\mathbf z)\right)
=-\int f(\mathbf z)\ln\!\left\{\frac{g(\mathbf z)}{f(\mathbf z)}\right\}
\,\mathrm d\mathbf z. \tag{20.23}
$$

为验证式 (20.21)，先由概率的乘积规则得到

$$
p(\mathbf x,\mathbf z\mid\mathbf w)
=p(\mathbf z\mid\mathbf x,\mathbf w)p(\mathbf x\mid\mathbf w). \tag{20.24}
$$

将式 (20.24) 代入 (20.22)，再利用 (20.23)，就得到 (20.21)（习题 20.8）。KL 散度具有 $\operatorname{KL}(\cdot\Vert\cdot)\geqslant0$ 的性质（见第 2.5.7 节），因此

$$
\ln p(\mathbf x\mid\mathbf w)\geqslant\mathcal L(\mathbf w). \tag{20.25}
$$

由于对数似然无法直接计算，我们通过最大化下界 $\mathcal L(\mathbf w)$ 来训练神经网络。

为此，先推导扩散模型的下界的显式形式。定义下界时，只要 $q(\mathbf z)$ 是有效概率分布，即非负且积分为 $1$，就可自由选择它的形式。在许多 ELBO 应用中，例如变分自编码器，我们为 $q(\mathbf z)$ 选择含可调参数的形式，通常用深度神经网络表示，然后同时对这些参数和 $p(\mathbf x,\mathbf z\mid\mathbf w)$ 中的参数最大化 ELBO。优化 $q(\mathbf z)$ 可使下界更紧，从而使对 $p(\mathbf x,\mathbf z\mid\mathbf w)$ 参数的优化更接近极大似然。扩散模型则将 $q(\mathbf z)$ 固定为式 (20.5) 马尔可夫链定义的 $q(\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf x)$；因此，可调参数只存在于逆向马尔可夫链的模型 $p(\mathbf x,\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf w)$ 中。注意，这里利用了选择 $q(\mathbf z)$ 的自由，使它依赖于 $\mathbf x$。

将式 (20.5) 的 $q(\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf x)$ 和式 (20.19) 的 $p(\mathbf x,\mathbf z_1,\ldots,\mathbf z_T\mid\mathbf w)$ 代入 ELBO，得到

<!-- pdf-page: 599 -->

$$
\begin{aligned}
\mathcal L(\mathbf w)
&=\mathbb E_q\!\left[
\ln\frac{p(\mathbf z_T)
\left\{\prod_{t=2}^{T}p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)\right\}
p(\mathbf x\mid\mathbf z_1,\mathbf w)}
{q(\mathbf z_1\mid\mathbf x)
\prod_{t=2}^{T}q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)}
\right]\\
&=\mathbb E_q\!\left[
\ln p(\mathbf z_T)
+\sum_{t=2}^{T}\ln\frac{p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)}{q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)}
-\ln q(\mathbf z_1\mid\mathbf x)
+\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)
\right].
\end{aligned} \tag{20.26}
$$

这里定义

$$
\mathbb E_q[\,\cdot\,]
\equiv\int\cdots\int q(\mathbf z_1\mid\mathbf x)
\prod_{t=2}^{T}q(\mathbf z_t\mid\mathbf z_{t-1})[\,\cdot\,]
\,\mathrm d\mathbf z_1\cdots\mathrm d\mathbf z_T. \tag{20.27}
$$

式 (20.26) 右边第一项 $\ln p(\mathbf z_T)$ 对应固定分布 $\mathcal N(\mathbf z_T\mid\mathbf 0,\mathbf I)$，不含可训练参数，因而只是一个固定的加性常数，可从 ELBO 的优化目标中省去。同样，第三项 $-\ln q(\mathbf z_1\mid\mathbf x)$ 与 $\mathbf w$ 无关，也可省去。

式 (20.26) 右边第四项对应变分自编码器中的重建项。可以从式 (20.2) 定义的 $\mathbf z_1$ 分布抽样，以蒙特卡罗估计近似期望 $\mathbb E_q[\,\cdot\,]$：

$$
\mathbb E_q[\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)]
\simeq\sum_{l=1}^{L}\ln p(\mathbf x\mid\mathbf z_1^{(l)},\mathbf w), \tag{20.28}
$$

其中 $\mathbf z_1^{(l)}\sim\mathcal N(\mathbf z_1\mid\sqrt{1-\beta_1}\,\mathbf x,\beta_1\mathbf I)$。与 VAE 不同，这里无须让误差信号反向传播穿过采样值，因为 $q$ 分布固定，不需要重参数化技巧（见第 19.2.2 节）。

**译注：** 原书式 (20.28) 的右边未写蒙特卡罗均值通常应有的 $1/L$ 因子；这里保留原式。

剩下的是式 (20.26) 右边第二项：它包含求和，每项依赖相邻两个潜变量 $\mathbf z_{t-1}$ 和 $\mathbf z_t$。推导扩散核 (20.6) 时，我们看到可直接从高斯分布 $q(\mathbf z_{t-1}\mid\mathbf x)$ 采样，再用同为高斯分布的式 (20.4) 生成对应的 $\mathbf z_t$。当样本数趋于无穷时，这样做是正确的；但以成对的采样值估计会产生高方差和较大噪声，要求不必要的多量样本。因此，我们改写 ELBO，使每一项只需采样一个值就能估计。

### 20.2.3 改写 ELBO

沿用对变分自编码器 ELBO 的讨论，我们希望把下界写成 KL 散度的形式，然后用闭式表达式求值。神经网络建模的是逆向分布 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$，而 $q$ 分布写成前向形式 $q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)$，因此利用贝叶斯定理将条件分布

<!-- pdf-page: 600 -->
<!-- join-previous-paragraph -->

逆转为

$$
q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)
=\frac{q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)q(\mathbf z_t\mid\mathbf x)}
{q(\mathbf z_{t-1}\mid\mathbf x)}. \tag{20.29}
$$

因此，式 (20.26) 中的第二项可写为

$$
\ln\frac{p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)}
{q(\mathbf z_t\mid\mathbf z_{t-1},\mathbf x)}
=\ln\frac{p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)}
{q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)}
+\ln\frac{q(\mathbf z_{t-1}\mid\mathbf x)}{q(\mathbf z_t\mid\mathbf x)}. \tag{20.30}
$$

式 (20.30) 右边第二项与 $\mathbf w$ 无关，可以省去。把式 (20.30) 代入 (20.26)，得到

$$
\mathcal L(\mathbf w)
=\mathbb E_q\!\left[
\sum_{t=2}^{T}\ln\frac{p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)}
{q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)}
+\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)
\right]. \tag{20.31}
$$

最后，式 (20.31) 可改写为（习题 20.9）

$$
\begin{aligned}
\mathcal L(\mathbf w)
&=\underbrace{\int q(\mathbf z_1\mid\mathbf x)
\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)\,\mathrm d\mathbf z_1}
_{\text{重建项}}\\
&\quad-\underbrace{\sum_{t=2}^{T}\int
\operatorname{KL}\!\left(q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)
\,\Vert\,p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)\right)
q(\mathbf z_t\mid\mathbf x)\,\mathrm d\mathbf z_t}
_{\text{一致性项}}.
\end{aligned} \tag{20.32}
$$

第一项的被积函数只含潜变量 $\mathbf z_1$，因此，式 (20.27) 定义的期望中其他所有条件分布都积分为 $1$，只剩对 $\mathbf z_1$ 的积分。类似地，第二项的每个积分最初只涉及相邻的 $\mathbf z_{t-1}$ 和 $\mathbf z_t$，其余变量都可积分消去。

式 (20.32) 与变分自编码器的 ELBO (19.14) 很相似，只是这里有多级编码器和解码器。重建项鼓励模型为观测数据样本赋予高概率，可用式 (20.28) 的采样近似，按与 VAE 对应项相同的方法训练（见第 19 章）。一致性项在两个高斯分布之间定义，因此有闭式表达式：$q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$ 由式 (20.15) 给出，$p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$ 由式 (20.18) 给出，于是 KL 散度为（习题 20.11）

$$
\begin{aligned}
&\operatorname{KL}\!\left(q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)
\,\Vert\,p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)\right)\\
&\qquad=\frac{1}{2\beta_t}\left\lVert
\mathbf m_t(\mathbf x,\mathbf z_t)-\boldsymbol\mu(\mathbf z_t,\mathbf w,t)
\right\rVert^2+\text{const}.
\end{aligned} \tag{20.33}
$$

<!-- pdf-page: 601 -->

其中 $\mathbf m_t(\mathbf x,\mathbf z_t)$ 由式 (20.16) 定义；所有与网络参数 $\mathbf w$ 无关的加性项都并入常数项，对训练不起作用。式 (20.32) 中每个一致性项还剩一个对 $\mathbf z_t$ 的积分，以 $q(\mathbf z_t\mid\mathbf x)$ 加权。可从该分布采样来近似积分，并利用式 (20.6) 的扩散核高效完成采样。

可见，式 (20.33) 的 KL 散度是简单的平方损失。训练时通过调整网络参数来最大化式 (20.32) 的下界；由于 ELBO 中 KL 散度项前有负号，我们实际是在最小化这个平方误差。

### 20.2.4 预测噪声

一种能提高生成质量的改动，是改变神经网络的预测目标：不再预测马尔可夫链每一步去噪后的图像，而是预测原图为形成该步带噪图像而累积加入的总噪声（Ho、Jain 和 Abbeel，2020）。为此，先整理式 (20.8)，得到

$$
\mathbf x=\frac{1}{\sqrt{\alpha_t}}\mathbf z_t
-\frac{\sqrt{1-\alpha_t}}{\sqrt{\alpha_t}}\boldsymbol\epsilon_t. \tag{20.34}
$$

将它代入式 (20.16)，可把逆向条件分布 $q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$ 的均值 $\mathbf m_t(\mathbf x,\mathbf z_t)$ 写成 $\mathbf z_t$ 与噪声 $\boldsymbol\epsilon_t$ 的形式（习题 20.12）：

$$
\mathbf m_t(\mathbf x,\mathbf z_t)
=\frac{1}{\sqrt{1-\beta_t}}
\left\{\mathbf z_t-\frac{\beta_t}{\sqrt{1-\alpha_t}}\boldsymbol\epsilon_t\right\}. \tag{20.35}
$$

类似地，用神经网络 $\mathbf g(\mathbf z_t,\mathbf w,t)$ 来预测从 $\mathbf x$ 生成 $\mathbf z_t$ 时累积加入的总噪声，而不再用 $\boldsymbol\mu(\mathbf z_t,\mathbf w,t)$ 预测去噪后的图像。与推导式 (20.35) 相同，可得两个网络函数的关系：

$$
\boldsymbol\mu(\mathbf z_t,\mathbf w,t)
=\frac{1}{\sqrt{1-\beta_t}}
\left\{\mathbf z_t-\frac{\beta_t}{\sqrt{1-\alpha_t}}
\mathbf g(\mathbf z_t,\mathbf w,t)\right\}. \tag{20.36}
$$

将式 (20.35) 和 (20.36) 代入 (20.33)，得到

$$
\begin{aligned}
&\operatorname{KL}\!\left(q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)
\,\Vert\,p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)\right)\\
&=\frac{\beta_t}{2(1-\alpha_t)(1-\beta_t)}
\left\lVert\mathbf g(\mathbf z_t,\mathbf w,t)-\boldsymbol\epsilon_t\right\rVert^2
+\text{const}\\
&=\frac{\beta_t}{2(1-\alpha_t)(1-\beta_t)}
\left\lVert\mathbf g\!\left(\sqrt{\alpha_t}\,\mathbf x
+\sqrt{1-\alpha_t}\,\boldsymbol\epsilon_t,\mathbf w,t\right)
-\boldsymbol\epsilon_t\right\rVert^2+\text{const}.
\end{aligned} \tag{20.37}
$$

最后一行使用式 (20.8) 代入了 $\mathbf z_t$。

<!-- pdf-page: 602 -->

ELBO (20.32) 中的重建项可用式 (20.28) 近似，从中抽取一个 $\mathbf z_1$。若 $p(\mathbf x\mid\mathbf z_1,\mathbf w)$ 采用式 (20.18) 的形式，则

$$
\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)
=-\frac{1}{2\beta_1}
\left\lVert\mathbf x-\boldsymbol\mu(\mathbf z_1,\mathbf w,1)\right\rVert^2
+\text{const}. \tag{20.38}
$$

用式 (20.36) 代入 $\boldsymbol\mu(\mathbf z_1,\mathbf w,1)$，用式 (20.1) 代入 $\mathbf x$，再利用式 (20.7) 给出的 $\alpha_1=1-\beta_1$，得到（习题 20.13）

$$
\ln p(\mathbf x\mid\mathbf z_1,\mathbf w)
=-\frac{1}{2(1-\beta_t)}
\left\lVert\mathbf g(\mathbf z_1,\mathbf w,1)-\boldsymbol\epsilon_1\right\rVert^2
+\text{const}. \tag{20.39}
$$

**译注：** 原书式 (20.39) 的分母写 $1-\beta_t$，而本式取 $t=1$；按代入过程应检查是否应为 $1-\beta_1$。这里照录原式。

这恰是式 (20.37) 在 $t=1$ 时的形式，因此重建项与一致性项可以合并。

Ho、Jain 和 Abbeel（2020）进一步发现，若省去式 (20.37) 前面的系数 $\beta_t/[2(1-\alpha_t)(1-\beta_t)]$，使马尔可夫链的所有步骤权重相等，生成效果还会提高。将式 (20.37) 的这一简化版本代入训练目标，得到

$$
\mathcal L(\mathbf w)
=-\sum_{t=1}^{T}
\left\lVert\mathbf g\!\left(\sqrt{\alpha_t}\,\mathbf x
+\sqrt{1-\alpha_t}\,\boldsymbol\epsilon_t,\mathbf w,t\right)
-\boldsymbol\epsilon_t\right\rVert^2. \tag{20.40}
$$

式 (20.40) 右边的平方误差含义简单：对马尔可夫链中的某一步 $t$ 和某个训练点 $\mathbf x$，抽取噪声向量 $\boldsymbol\epsilon_t$，并用它构造该步对应的带噪潜向量 $\mathbf z_t$；损失函数就是预测噪声与实际噪声之间的平方差。注意，网络 $\mathbf g(\cdot,\cdot,\cdot)$ 预测的是相对于原始数据向量 $\mathbf x$ 累积加入的总噪声，不只是第 $t$ 步的增量噪声。

用随机梯度下降时，针对训练集中随机选取的数据点 $\mathbf x$，计算损失函数对网络参数的梯度。对于每个数据点，还沿马尔可夫链随机选一步 $t$，无须计算式 (20.40) 中所有 $t$ 项的误差。这些梯度在数据小批量上累积，用于更新权重。

这一损失函数还自然包含了数据增强：每次使用某个训练样本 $\mathbf x$，都会给它配一个新抽取的噪声样本 $\boldsymbol\epsilon_t$。以上都针对训练集中的单个数据点 $\mathbf x$。算法 20.1 总结相应的梯度计算过程。

### 20.2.5 生成新样本

网络训练完成后，先从高斯分布 $p(\mathbf z_T)$ 采样，再沿马尔可夫链逐步去噪，就能生成数据空间中的新样本。给定第 $t$ 步的带噪样本 $\mathbf z_t$，生成 $\mathbf z_{t-1}$ 分三步：先计算神经网络输出 $\mathbf g(\mathbf z_t,\mathbf w,t)$，再利用式 (20.36) 计算 $\boldsymbol\mu(\mathbf z_t,\mathbf w,t)$。

<!-- pdf-page: 603 -->

**算法 20.1：训练去噪扩散概率模型**

```text
输入：训练数据 D = {x_n}
      噪声方案 {β₁,…,β_T}
输出：网络参数 w

for t ∈ {1,…,T} do
  α_t ← ∏_{τ=1}^t(1−β_τ)
  // 由 β 计算 α
end for
repeat
  x ∼ D
  // 抽取数据点
  t ∼ {1,…,T}
  // 抽取链中一步
  ε ∼ N(ε|0,I)
  // 抽取噪声
  z_t ← √α_t x + √(1−α_t)ε
  // 计算带噪潜变量
  L(w) ← ||g(z_t,w,t)−ε||²
  // 计算损失项
  执行一次优化器更新
until 收敛
return w
```

最后从 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)
=\mathcal N(\mathbf z_{t-1}\mid\boldsymbol\mu(\mathbf z_t,\mathbf w,t),\beta_t\mathbf I)$ 生成样本：加入按方差缩放的噪声，得到

$$
\mathbf z_{t-1}=\boldsymbol\mu(\mathbf z_t,\mathbf w,t)
+\sqrt{\beta_t}\,\boldsymbol\epsilon, \tag{20.41}
$$

其中 $\boldsymbol\epsilon\sim\mathcal N(\boldsymbol\epsilon\mid\mathbf 0,\mathbf I)$。网络 $\mathbf g(\cdot,\cdot,\cdot)$ 预测的是为得到 $\mathbf z_t$ 而加到原始向量 $\mathbf x$ 上的总噪声；但在采样步中，只从 $\mathbf z_t$ 中减去该噪声的 $\beta_t/\sqrt{1-\alpha_t}$ 部分，再加入方差为 $\beta_t$ 的噪声，得到 $\mathbf z_{t-1}$。最后计算合成数据样本 $\mathbf x$ 时，不再加入额外噪声，因为目标是无噪输出。算法 20.2 总结采样过程。

**译注：** 原书上述说明写“从 $\mathbf z_{t-1}$ 中减去”，但按式 (20.36) 和采样顺序，被减去一部分噪声的是输入 $\mathbf z_t$；译文按公式说明。

扩散模型用于生成数据的主要缺点，是需要让已训练网络依次作多次推断，计算成本可能很高。加速方法之一，是先将去噪过程变成连续时间的微分方程，再用其他高效的离散化方法求解（见第 20.3.4 节）。

本章假设数据和潜变量连续，因此可以采用高斯噪声模型。扩散模型也可定义在离散空间上（Austin 等，2021）。例如，生成候选药物分子时，部分生成步骤需要从一组化学元素中选择原子类型。

前面已经看到，扩散模型的计算可能很密集，因为

<!-- pdf-page: 604 -->
<!-- join-previous-paragraph -->

它们依次逆转一个可能包含数百或数千步的噪声过程。Song、Meng 和 Ermon（2020）提出一种相关技术，称为**去噪扩散隐式模型**（denoising diffusion implicit models）。它放宽了噪声过程的马尔可夫假设，同时保留相同的训练目标。因此，采样速度可以提高一到两个数量级，而生成质量不下降。

**算法 20.2：从去噪扩散概率模型采样**

```text
输入：已训练去噪网络 g(z,w,t)
      噪声方案 {β₁,…,β_T}
输出：数据空间中的样本向量 x

z_T ∼ N(z|0,I)
// 从最终潜空间采样
for t ∈ {T,…,2} do
  α_t ← ∏_{τ=1}^t(1−β_τ)
  // 计算 α
  // 计算网络输出
  μ(z_t,w,t) ← 1/√(1−β_t) ×
    {z_t−β_t/√(1−α_t)
      g(z_t,w,t)}
  ε ∼ N(ε|0,I)
  // 抽取噪声向量
  z_{t−1} ← μ(z_t,w,t)+√β_t ε
  // 加入缩放后的噪声
end for
x ← 1/√(1−β₁) ×
  {z₁−β₁/√(1−α₁)g(z₁,w,t)}
  // 最后一步去噪
return x
```

**译注：** 原书算法 20.2 最后一步仍写 $\mathbf g(\mathbf z_1,\mathbf w,t)$，但循环已结束；按该步索引应取 $t=1$。上面保留原算法写法。

## 20.3 得分匹配

本章前面讨论的去噪扩散模型，与另一类相对独立发展起来、基于**得分匹配**（score matching）的深度生成模型密切相关（Hyvärinen，2005；Song 和 Ermon，2019）。它们使用**得分函数**（score function），也称 **Stein 得分**（Stein score），定义为对数似然对数据向量 $\mathbf x$ 的梯度：

$$
\mathbf s(\mathbf x)=\nabla_{\mathbf x}\ln p(\mathbf x). \tag{20.42}
$$

这里须强调，梯度是相对于数据向量求的，不是相对于任何参数向量。$\mathbf s(\mathbf x)$ 是与 $\mathbf x$ 维度相同的向量函数，其中每个元素 $s_i(\mathbf x)=\partial\ln p(\mathbf x)/\partial x_i$ 对应 $\mathbf x$ 的一个元素 $x_i$。例如，若 $\mathbf x$ 是图像，$\mathbf s(\mathbf x)$ 也可表示为一张维度相同的图像，其相应的

<!-- pdf-page: 605 -->
<!-- join-previous-paragraph -->

元素就是对应的像素。图 20.5 给出一个二维概率密度及其对应得分函数的例子。

<figure id="fig-20-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-5.png" alt="二维高斯混合密度的热图与规则网格上的得分函数向量">
  <figcaption>图 20.5：得分函数示意。图中用热图表示由高斯混合组成的二维分布，并在 $\mathbf x$ 的规则网格上以向量表示式 (20.42) 定义的对应得分函数。</figcaption>
</figure>

得分函数为何有用？考虑两个函数 $q(\mathbf x)$ 和 $p(\mathbf x)$：它们在所有 $\mathbf x$ 处的得分都相同，即 $\nabla_{\mathbf x}\ln q(\mathbf x)=\nabla_{\mathbf x}\ln p(\mathbf x)$。对等式两边相对于 $\mathbf x$ 积分，再取指数，可得 $q(\mathbf x)=Kp(\mathbf x)$，其中 $K$ 是不依赖 $\mathbf x$ 的常数。因此，只要能学得得分函数的模型 $\mathbf s(\mathbf x,\mathbf w)$，就等于在一个乘法常数的意义下建模了原始数据密度。

### 20.3.1 得分损失函数

为训练该模型，我们需要定义损失函数，让模型得分函数 $\mathbf s(\mathbf x,\mathbf w)$ 逼近生成数据的分布 $p(\mathbf x)$ 的得分函数 $\nabla_{\mathbf x}\ln p(\mathbf x)$。例如，取模型得分与真实得分之间平方误差的期望：

$$
J(\mathbf w)=\frac{1}{2}\int
\left\lVert\mathbf s(\mathbf x,\mathbf w)-\nabla_{\mathbf x}\ln p(\mathbf x)\right\rVert^2
p(\mathbf x)\,\mathrm d\mathbf x. \tag{20.43}
$$

如第 14.3.1 节讨论基于能量的模型时所见，得分函数不要求相应的概率密度已归一化，因为梯度运算会消去归一化常数，所以模型形式有相当大的选择余地。用深度神经网络表示得分函数 $\mathbf s(\mathbf x,\mathbf w)$ 大致有两种方式。$\mathbf s$ 的每个分量 $s_i$ 对应 $\mathbf x$ 的分量 $x_i$，因此第一种方式让网络的输出个数等于输入个数。不过，得分函数被定义为标量函数（对数概率密度）的梯度，这是一类限制更强的函数（习题 20.14）。另一种方式则让网络只有一个输出 $\phi(\mathbf x)$

<!-- pdf-page: 606 -->
<!-- join-previous-paragraph -->

，再通过自动微分计算 $\nabla_{\mathbf x}\phi(\mathbf x)$。但第二种方式需要两次反向传播，计算成本更高。因此，多数应用直接采用第一种方式（习题 20.15）。

### 20.3.2 修正后的得分损失

损失函数 (20.43) 的一个问题是无法直接将其最小化，因为我们不知道真实的数据得分 $\nabla_{\mathbf x}\ln p(\mathbf x)$。手中只有有限的数据集 $\mathcal D=(\mathbf x_1,\ldots,\mathbf x_N)$，可用它构造经验分布：

$$
p_{\mathcal D}(\mathbf x)=\frac{1}{N}\sum_{n=1}^{N}\delta(\mathbf x-\mathbf x_n). \tag{20.44}
$$

这里的 $\delta(\mathbf x)$ 是狄拉克 delta 函数。非正式地说，它是在 $\mathbf x=\mathbf 0$ 处无限高的“尖峰”，满足

$$
\delta(\mathbf x)=0,\quad\mathbf x\ne\mathbf 0 \tag{20.45}
$$

以及

$$
\int\delta(\mathbf x)\,\mathrm d\mathbf x=1. \tag{20.46}
$$

式 (20.44) 不是 $\mathbf x$ 的可微函数，所以无法计算其得分函数。为解决这个问题，可以引入噪声模型，将数据点“抹开”，得到平滑且可微的密度表示。这称为 **Parzen 估计**（Parzen estimator）或**核密度估计**（kernel density estimator，见第 3.5.2 节），定义为

$$
q_\sigma(\mathbf z)=\int q(\mathbf z\mid\mathbf x,\sigma)p(\mathbf x)\,\mathrm d\mathbf x, \tag{20.47}
$$

其中 $q(\mathbf z\mid\mathbf x,\sigma)$ 是噪声核。常见选择是高斯核：

$$
q(\mathbf z\mid\mathbf x,\sigma)
=\mathcal N(\mathbf z\mid\mathbf x,\sigma^2\mathbf I). \tag{20.48}
$$

我们不再最小化损失函数 (20.43)，而是最小化相对于平滑后的 Parzen 密度所定义的相应损失：

$$
J(\mathbf w)=\frac{1}{2}\int
\left\lVert\mathbf s(\mathbf z,\mathbf w)-\nabla_{\mathbf z}\ln q_\sigma(\mathbf z)\right\rVert^2
q_\sigma(\mathbf z)\,\mathrm d\mathbf z. \tag{20.49}
$$

一个关键结果是：把式 (20.47) 代入 (20.49)，便可将此损失函数等价地改写为（Vincent，2011；习题 20.17）

$$
J(\mathbf w)=\frac{1}{2}\iint
\left\lVert\mathbf s(\mathbf z,\mathbf w)
-\nabla_{\mathbf z}\ln q(\mathbf z\mid\mathbf x,\sigma)\right\rVert^2
q(\mathbf z\mid\mathbf x,\sigma)p(\mathbf x)
\,\mathrm d\mathbf z\,\mathrm d\mathbf x+\mathrm{const}. \tag{20.50}
$$

再用经验密度 (20.44) 代入 $p(\mathbf x)$，得到

$$
J(\mathbf w)=\frac{1}{2N}\sum_{n=1}^{N}\int
\left\lVert\mathbf s(\mathbf z,\mathbf w)
-\nabla_{\mathbf z}\ln q(\mathbf z\mid\mathbf x_n,\sigma)\right\rVert^2
q(\mathbf z\mid\mathbf x_n,\sigma)\,\mathrm d\mathbf z
+\mathrm{const}. \tag{20.51}
$$

<!-- pdf-page: 607 -->

<figure id="fig-20-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-6.png" alt="三条从图中心出发的朗之万动力学采样轨迹">
  <figcaption>图 20.6：对图 20.5 中的分布，使用式 (14.61) 定义的朗之万动力学得到的采样轨迹示例。三条轨迹均从图中心出发。</figcaption>
</figure>

对高斯 Parzen 核 (20.48)，得分函数成为

$$
\nabla_{\mathbf z}\ln q(\mathbf z\mid\mathbf x,\sigma)
=-\frac{1}{\sigma}\boldsymbol\epsilon. \tag{20.52}
$$

原书此处将 $\boldsymbol\epsilon=\mathbf z-\mathbf x$ 写为从 $\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I)$ 抽取。若考虑式 (20.6) 的具体噪声模型，则得到

$$
\nabla_{\mathbf z}\ln q(\mathbf z\mid\mathbf x,\sigma)
=-\frac{1}{\sqrt{1-\alpha_t}}\boldsymbol\epsilon. \tag{20.53}
$$

**译注：** 式 (20.52) 中的 $-\boldsymbol\epsilon/\sigma$ 要求 $\boldsymbol\epsilon=(\mathbf z-\mathbf x)/\sigma$ 才与高斯核 (20.48) 一致；原书同时写 $\boldsymbol\epsilon=\mathbf z-\mathbf x$ 与单位高斯，符号定义似有遗漏。这里保留原式并指出差异。

可见，得分损失 (20.50) 衡量神经网络的预测值与噪声 $\boldsymbol\epsilon$ 之间的差别。因此，此损失函数与去噪扩散模型所用的式 (20.37) 具有相同的最小值；得分函数 $\mathbf s(\mathbf z,\mathbf w)$ 所起的作用，与噪声预测网络 $\mathbf g(\mathbf z,\mathbf w)$ 相同，只差一个常数缩放因子 $-1/\sqrt{1-\alpha_t}$（Song 和 Ermon，2019）。最小化式 (20.50) 称为**去噪得分匹配**（denoising score matching），这也显示它与去噪扩散模型的紧密联系。如何选择噪声方差 $\sigma^2$，稍后再讨论。

训练得分模型后，还需要从中生成新样本。朗之万动力学基于得分函数，不要求归一化的概率分布，因此很适合基于得分的模型（见第 14.3 节）。图 20.6 给出了示例。

### 20.3.3 噪声方差

前面已经说明如何从训练数据学习得分函数，并用朗之万采样从学到的分布生成新样本。不过，这种方法可能有三个问题（Song 和

<!-- pdf-page: 608 -->
<!-- join-previous-paragraph -->

Ermon，2019；Luo，2022）。第一，如果数据分布位于维度低于数据空间的流形上，那么流形外的概率密度为零；由于 $\ln p(\mathbf x)$ 在那里未定义，得分函数也未定义（见第 16 章）。第二，在数据密度低的区域，得分函数的估计可能不准确，因为损失函数 (20.43) 以密度为权重。不准确的得分函数会使朗之万采样的轨迹变差。第三，即使得分函数模型准确，若数据分布由相互分离的分布混合而成，朗之万过程仍可能无法正确采样（习题 20.18）。

增大核函数 (20.48) 使用的噪声方差 $\sigma^2$，可以把数据分布抹开，从而缓解以上三个问题。但方差过大会使原分布明显失真，也会使得分函数的建模不准确。为权衡两者，可以采用一系列方差 $\sigma_1^2<\sigma_2^2<\cdots<\sigma_T^2$（Song 和 Ermon，2019）。其中 $\sigma_1^2$ 足够小，以准确表示数据分布；$\sigma_T^2$ 足够大，以避开上述问题。然后让得分网络额外接收方差作为输入，写为 $\mathbf s(\mathbf x,\mathbf w,\sigma^2)$，并用形如式 (20.51) 的损失函数的加权和训练它；每项都衡量相应网络与相应扰动数据集之间的误差。对于数据向量 $\mathbf x_n$，损失函数为

$$
\frac{1}{2}\sum_{i=1}^{L}\lambda(i)
\int\left\lVert
\mathbf s(\mathbf z,\mathbf w,\sigma_i^2)
-\nabla_{\mathbf z}\ln q(\mathbf z\mid\mathbf x_n,\sigma_i)
\right\rVert^2
q(\mathbf z\mid\mathbf x_n,\sigma_i)\,\mathrm d\mathbf z. \tag{20.54}
$$

其中 $\lambda(i)$ 为权重系数。可以看到，该训练过程与训练分层去噪网络的过程完全对应（见第 20.2.1 节）。

**译注：** 原书先把噪声方差序列的上限写为 $T$，式 (20.54) 及下文退火步骤却写为 $L$；两处都表示噪声尺度的个数，本书此处未说明改换记号。

训练完成后，依次对 $i=L,L-1,\ldots,2,1$ 的每个模型运行若干步朗之万采样，便可生成样本。这种技术称为**退火朗之万动力学**（annealed Langevin dynamics），与从去噪扩散模型采样的算法 20.2 类似。

### 20.3.4 随机微分方程

构造扩散模型的噪声过程时，采用大量步骤（通常数千步）会有帮助。因此可以自然地问：如果步骤数趋于无穷，会发生什么？这类似第 18.3.1 节引入神经微分方程时对无限深神经网络所作的处理。在取此极限时，必须确保每一步的噪声方差 $\beta_t$ 随步长一起缩小。这样便得到以**随机微分方程**（stochastic differential equation，SDE）描述的连续时间扩散模型（Song 等，2020）。于是，去噪扩散概率模型和得分匹配模型都可视为连续时间 SDE 的离散化形式。

一般 SDE 可写为对向量 $\mathbf z$ 的无穷小更新：

$$
\mathrm d\mathbf z
=\underbrace{\mathbf f(\mathbf z,t)\,\mathrm dt}_{\text{漂移}}
+\underbrace{g(t)\,\mathrm d\mathbf v}_{\text{扩散}}. \tag{20.55}
$$

<!-- pdf-page: 609 -->

其中漂移项与常微分方程一样是确定性的；扩散项则是随机的，例如由无穷小的高斯步给出。这里的参数 $t$ 类比物理系统，通常称为“时间”。对扩散模型的前向噪声过程 (20.3) 取连续时间极限，便可写成式 (20.55) 的 SDE（习题 20.19）。

对应于 SDE (20.55)，存在一个逆向 SDE（Song 等，2020）：

$$
\mathrm d\mathbf z=
\left[\mathbf f(\mathbf z,t)-g^2(t)\nabla_{\mathbf z}\ln p(\mathbf z)\right]\mathrm dt
+g(t)\,\mathrm d\mathbf v. \tag{20.56}
$$

其中 $\nabla_{\mathbf z}\ln p(\mathbf z)$ 正是得分函数。式 (20.55) 给出的 SDE 要从 $t=T$ 到 $t=0$ 逆向求解。

**译注：** 上句按原书引用式 (20.55)，但 (20.55) 是前向 SDE；按紧邻的逆向方程，需核对是否应为式 (20.56)。

数值求解 SDE 时，需要将时间变量离散化。最简单的方法是采用固定且等间距的时间步，称为 **Euler–Maruyama 求解法**。对于逆向 SDE，这会重新得到一种形式的朗之万方程（见第 14.3 节）。也可以采用更灵活的离散化方法及更复杂的求解器（Kloeden 和 Platen，2013）。

对每个受 SDE 支配的扩散过程，都存在一个用常微分方程（ODE）描述的对应确定性过程；它的轨迹与 SDE 具有相同的边缘概率密度 $p(\mathbf z\mid t)$（Song 等，2020）。对形如式 (20.56) 的 SDE，对应的 ODE 为

$$
\frac{\mathrm d\mathbf z}{\mathrm dt}
=\mathbf f(\mathbf z,t)-\frac{1}{2}g^2(t)
\nabla_{\mathbf z}\ln p(\mathbf z). \tag{20.57}
$$

ODE 形式允许使用高效的自适应步长求解器，大幅减少函数计算次数。它还使概率扩散模型与归一化流模型联系起来，后者的变量变换公式 (18.1) 可用于精确计算对数似然（见第 18 章）。

## 20.4 引导式扩散

到目前为止，我们将扩散模型用于表示无条件密度 $p(\mathbf x)$；它从独立采自 $p(\mathbf x)$ 的训练样本 $\mathbf x_1,\ldots,\mathbf x_N$ 中学得。模型训练完成后，就可以从这一分布生成新样本。图 1.3 已给出一个深度生成模型对人脸图像作无条件采样的例子，当时使用的是 GAN。

然而，许多应用需要从条件分布 $p(\mathbf x\mid c)$ 采样。条件变量 $c$ 例如可以是类别标签，或描述期望图像内容的文字。这也是图像超分辨率、图像修补、视频生成等应用的基础。最简单的做法，是将 $c$ 作为去噪神经网络 $\mathbf g(\mathbf z,\mathbf w,t,c)$ 的额外输入，用匹配的数据对 $\{\mathbf x_n,c_n\}$ 训练。此方法的主要局限是，

<!-- pdf-page: 610 -->
<!-- join-previous-paragraph -->

网络可能未充分重视条件变量，甚至将其忽略。因此，需要一种方法来控制条件信息所占的权重，并在遵循条件信息与样本多样性之间作权衡。这种促使生成结果符合条件信息的额外作用称为**引导**（guidance）。按是否使用独立的分类器模型，引导主要分为两种方法。

### 20.4.1 分类器引导

假设已有训练好的分类器 $p(c\mid\mathbf x)$，从得分函数的角度考察扩散模型。利用贝叶斯定理，可将条件扩散模型的得分函数写为

$$
\begin{aligned}
\nabla_{\mathbf x}\ln p(\mathbf x\mid c)
&=\nabla_{\mathbf x}\ln\left\{
\frac{p(c\mid\mathbf x)p(\mathbf x)}{p(c)}
\right\}\\
&=\nabla_{\mathbf x}\ln p(\mathbf x)
+\nabla_{\mathbf x}\ln p(c\mid\mathbf x).
\end{aligned}\tag{20.58}
$$

这里使用了 $\nabla_{\mathbf x}\ln p(c)=0$，因为 $p(c)$ 不依赖 $\mathbf x$。式 (20.58) 右边第一项是通常的无条件得分函数；第二项则推动去噪过程，朝着提高分类器给定标签 $c$ 概率的方向前进（Dhariwal 和 Nichol，2021）。引入称为**引导强度**（guidance scale）的超参数 $\lambda$，便能控制分类器梯度的权重。用于采样的得分函数成为

$$
\operatorname{score}(\mathbf x,c,\lambda)
=\nabla_{\mathbf x}\ln p(\mathbf x)
+\lambda\nabla_{\mathbf x}\ln p(c\mid\mathbf x). \tag{20.59}
$$

当 $\lambda=0$ 时，回到原来的无条件扩散模型；$\lambda=1$ 时，得到与条件分布 $p(\mathbf x\mid c)$ 对应的得分。$\lambda>1$ 时，模型会受到更强的推动以遵守条件标签，因此可用远大于 $1$ 的值，例如 $\lambda=10$。代价是样本多样性下降，因为模型偏向生成分类器容易正确分类的“简单”样本。

基于分类器的引导有一个问题：必须单独训练分类器。此外，分类器还需要能够对噪声程度各异的样本分类，而标准分类器是在干净样本上训练的。下面讨论一种无须单独分类器的方法。

### 20.4.2 无分类器引导

用式 (20.58) 代换 (20.59) 中的 $\nabla_{\mathbf x}\ln p(c\mid\mathbf x)$，便可将得分函数写为（习题 20.20）

$$
\operatorname{score}(\mathbf x,c,\lambda)
=\lambda\nabla_{\mathbf x}\ln p(\mathbf x\mid c)
+(1-\lambda)\nabla_{\mathbf x}\ln p(\mathbf x). \tag{20.60}
$$

当 $0<\lambda<1$ 时，它是条件对数密度 $\ln p(\mathbf x\mid c)$ 与无条件对数密度 $\ln p(\mathbf x)$ 的凸组合。$\lambda>1$ 时，

<!-- pdf-page: 611 -->
<!-- join-previous-paragraph -->

无条件得分项的系数变为负数，也就是说，模型会主动降低那些忽略条件信息的样本的生成概率，转而偏向符合条件信息的样本。

另外，训练时以一定概率（通常约 $10\%$–$20\%$）将条件变量 $c$ 设为空值，例如 $c=0$，就可以用单个条件模型同时表示 $p(\mathbf x\mid c)$ 和 $p(\mathbf x)$，其中 $p(\mathbf x)$ 由 $p(\mathbf x\mid c=0)$ 表示。这在某种程度上类似 dropout：训练时对随机选取的一部分样本，将其全部条件输入置零（见第 9.6.1 节）。

训练完成后，可用得分函数 (20.60) 加强条件信息的影响。在实践中，无分类器引导的结果质量远高于分类器引导（Nichol 等，2021；Saharia 等，2022）。原因是分类器 $p(c\mid\mathbf x)$ 只要能正确预测 $c$，便可以忽略输入向量 $\mathbf x$ 的大部分内容；无分类器引导则基于条件密度 $p(\mathbf x\mid c)$，必须对 $\mathbf x$ 的所有方面都赋予高概率。

文本引导的扩散模型可借用大型语言模型中的技术（见第 12 章），使条件输入成为一般的文本序列，也就是**提示词**（prompt），而非只能从预先定义的类别标签中选择。文本输入可以通过两种方式影响去噪：一是将基于 Transformer 的语言模型产生的内部表示与去噪网络的输入拼接；二是让去噪网络中的交叉注意力层关注文本 token 序列。图 20.7 展示了以文本提示词为条件的无分类器引导。

条件扩散模型的另一个应用是图像超分辨率，即将低分辨率图像转换为相应的高分辨率图像。这本质上是一个逆问题：一张低分辨率图像可以对应多张不同的高分辨率图像。超分辨率可通过从高斯分布出发，对高分辨率样本去噪，并以低分辨率图像为条件来实现（Saharia、Ho 等，2021）。图 20.8 给出此方法的例子。这类模型可级联以获得很高的分辨率（Ho 等，2021），例如先从 $64\times64$ 到 $256\times256$，再从 $256\times256$ 到 $1024\times1024$。每一级通常采用 U-net 架构，并以前一级最终去噪输出为条件（见第 10.5.4 节）。

类似的级联也可用于图像生成扩散模型：先在较低分辨率下完成图像去噪，再用独立的网络对结果上采样（该网络也可接收文本提示词），得到最终的高分辨率输出（Nichol 等，2021；Saharia 等，2022）。这能显著降低计算成本，因为去噪过程可能需要让去噪网络运行数百次，而直接在高维空间工作成本更高。注意，这些方法仍在图像空间中运行，只是分辨率较低。

另一种降低直接在高分辨率图像空间中运行扩散模型所需计算成本的方法，称为**潜空间扩散模型**（latent diffusion

<!-- pdf-page: 612 -->
<!-- join-previous-paragraph-with-space -->

models；Rombach 等，2021）。它先在无噪声图像上训练自编码器（见第 19.1 节），得到图像的低维表示，然后固定自编码器。接着训练 U-net 架构在这个低维空间中去噪；这个空间本身不能直接解释为图像。最后，用固定自编码器网络的输出半部，将去噪后的表示映射回高分辨率图像空间。此方法能更有效地利用低维空间，使它专注于图像语义，而将从去噪后的低维表示构建清晰的高分辨率图像留给解码器。

<figure id="fig-20-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-7.png" alt="GLIDE 模型生成的两组彩色玻璃熊猫图像，分别为无引导与有引导">
  <figcaption>图 20.7：扩散模型的无分类器引导示意。以提示词“A stained glass window of a panda eating bamboo”（一扇描绘熊猫吃竹子的彩色玻璃窗）为条件，用 GLIDE 模型生成。左侧示例采用 $\lambda=0$（没有引导，仅使用普通条件模型）；右侧采用 $\lambda=3$。［据 Nichol 等（2021），经许可使用。］</figcaption>
</figure>

**译注：** 图 20.7 的原书图注称 $\lambda=0$ 为“没有引导、仅使用普通条件模型”；但本节式 (20.59)–(20.60) 以 $\lambda=0$ 表示无条件得分、$\lambda=1$ 表示普通条件得分。两处的 $\lambda$ 基线不一致，图中的实验标记在此照录。

条件图像生成还有许多其他应用，包括图像修补、扩画、复原、形变、风格迁移、上色、去模糊及视频生成（Yang、Srivastava 和 Mandt，2022）。图 20.9 展示了图像修补的例子。

<!-- pdf-page: 613 -->

<figure id="fig-20-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-8.png" alt="低分辨率人脸和花朵图像及其两幅高分辨率生成结果">
  <figcaption>图 20.8：两组低分辨率图像及其由扩散模型生成的相应高分辨率图像。上排输入为 $16\times16$，对应的输出为 $128\times128$；被上排输入模糊化的原始图像在该排右侧。下排输入为 $64\times64$，输出为 $256\times256$；下排也在右侧给出原始图像以供比较。［据 Saharia、Ho 等（2021），经许可使用。］</figcaption>
  <p class="figure-translation">图内文字：Input → 输入；Output → 输出；Original → 原图。</p>
</figure>

<figure id="fig-20-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-20/fig-20-9.png" alt="原图、删除面部区域的图像及图像修补结果">
  <figcaption>图 20.9：图像修补示例。左侧为原图，中间将脸部区域删除，右侧用图像修补重新填入。［据 Saharia、Chan、Chang 等（2021），经许可使用。］</figcaption>
</figure>

## 习题

**20.1（★）** 利用式 (20.3)，写出 $\mathbf z_t$ 的均值和协方差关于 $\mathbf z_{t-1}$ 的均值和协方差的表达式。由此证明，当 $0<\beta_t<1$ 时，$\mathbf z_t$ 的分布均值比 $\mathbf z_{t-1}$ 的分布均值更接近零，且 $\mathbf z_t$ 的协方差比 $\mathbf z_{t-1}$ 的协方差更接近单位矩阵 $\mathbf I$。

**20.2（★）** 证明变换 (20.1) 可写成等价形式 (20.2)。

**20.3（★★★）** 本题用数学归纳法证明：由式 (20.4) 定义的扩散模型前向过程，其 $\mathbf x_t$ 的边缘分布由式 (20.6) 给出，其中 $\alpha_t$ 由式 (20.7) 定义。先验证 $t=1$ 时式 (20.6) 成立。再假设某个特定 $t$ 值下式 (20.6) 成立，推导 $t+1$ 时的相应结果。最简单的方法是采用式 (20.3) 的表示来写前向过程，并使用式 (3.212)：两个独立高斯随机变量之和仍为高斯，其均值和协方差分别相加。

**译注：** 本题原文写“$\mathbf x_t$ 的边缘分布”，本章前向过程的相应潜变量记号为 $\mathbf z_t$；这里照录原文并指出差异。

**20.4（★）** 利用式 (20.6) 的结果（$\alpha_t$ 由式 (20.7) 定义），证明当 $T\to\infty$ 时得到式 (20.9)。

<!-- pdf-page: 614 -->

**20.5（★★）** 考虑两个独立随机变量 $\mathbf a$ 和 $\mathbf b$，以及一个固定标量 $\lambda$。证明

$$
\operatorname{cov}[\mathbf a+\mathbf b]
=\operatorname{cov}[\mathbf a]+\operatorname{cov}[\mathbf b] \tag{20.61}
$$

及

$$
\operatorname{cov}[\lambda\mathbf a]
=\lambda^2\operatorname{cov}[\mathbf a]. \tag{20.62}
$$

利用这些结果证明：若 $\mathbf z_{t-1}$ 的分布均值为零、协方差为单位矩阵，则不论 $\beta_t$ 的值是多少，式 (20.3) 定义的 $\mathbf z_t$ 分布也有零均值和单位协方差。

**20.6（★★★）** 本题从贝叶斯定理 (20.13) 出发，用配方法推导式 (20.15)。先注意，式 (20.13) 右边分子中的两项由式 (20.4) 和 (20.6) 给出，它们都是 $\mathbf z_{t-1}$ 的二次函数的指数。因此，所求分布是高斯分布，只须求出均值和协方差。为此，仅考虑指数中依赖 $\mathbf z_{t-1}$ 的项，并注意两个指数相乘等于其指数部分相加后再取指数。合并所有关于 $\mathbf z_{t-1}$ 的二次项与一次项，再将其重排为 $(\mathbf z_{t-1}-\mathbf m_t)^{\mathsf T}\mathbf S_t^{-1}(\mathbf z_{t-1}-\mathbf m_t)$ 的形式。然后通过观察求出 $\mathbf m_t(\mathbf x,\mathbf z_t)$ 和 $\mathbf S_t$ 的表达式。注意，可忽略与 $\mathbf z_{t-1}$ 无关的加性项。

**20.7（★★★）** 本题证明：在噪声方差较小时，扩散模型前向噪声过程的条件分布 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 的逆向分布可用高斯分布近似。考虑由贝叶斯定理以式 (20.11) 给出的逆向条件分布 $q(\mathbf z_{t-1}\mid\mathbf z_t)$，其中前向分布 $q(\mathbf z_t\mid\mathbf z_{t-1})$ 由式 (20.4) 给出。对式 (20.11) 两边取对数，然后以 $\mathbf z_t$ 为中心对 $q(\mathbf z_{t-1})$ 作泰勒展开，证明：当噪声方差 $\beta_t$ 较小时，$q(\mathbf z_{t-1}\mid\mathbf z_t)$ 近似为均值 $\mathbf z_t$、协方差 $\beta_t\mathbf I$ 的高斯分布。求均值和协方差关于 $\beta_t$ 的幂展开中最低阶修正项。

**20.8（★★）** 将式 (20.24) 的概率乘积规则代入扩散模型 ELBO 的定义 (20.22)，并利用 Kullback–Leibler 散度的定义 (20.23)，验证对数似然函数可按式 (20.21) 写成下界与 Kullback–Leibler 散度之和。

**20.9（★★）** 验证由式 (20.31) 给出的扩散模型 ELBO 可写为式 (20.32)，其中 Kullback–Leibler 散度由式 (20.23) 定义。

**20.10（★★）** 推导式 (20.32) 的扩散模型 ELBO 时，我们省去了式 (20.26) 的第一项和第三项，因为它们与 $\mathbf w$ 无关。类似地，也省去了式 (20.30) 右边的第二项，因为它也与 $\mathbf w$ 无关。证明：若保留所有这些被省去的项，它们会使 ELBO $\mathcal L(\mathbf x)$ 多出一项：

$$
\operatorname{KL}\!\left(q(\mathbf z_T\mid\mathbf x)\Vert p(\mathbf z_T)\right). \tag{20.63}
$$

<!-- pdf-page: 615 -->

注意，噪声过程被构造为使 $q(\mathbf z_T\mid\mathbf x)$ 等于高斯分布 $\mathcal N(\mathbf x\mid\mathbf 0,\mathbf I)$。类似地，$p(\mathbf z_T)$ 被定义为等于 $\mathcal N(\mathbf x\mid\mathbf 0,\mathbf I)$，因此式 (20.63) 中的两个分布相等，Kullback–Leibler 散度为零。

**译注：** 上段高斯分布的自变量均按原文记为 $\mathbf x$；按所讨论的 $\mathbf z_T$ 分布，通常应记为 $\mathbf z_T$。另外，从式 (20.26) 和 (20.30) 保留被省略项所得的末端贡献是 $-\operatorname{KL}(q(\mathbf z_T\mid\mathbf x)\Vert p(\mathbf z_T))$，与原书式 (20.63) 的正号相反。式 (20.9) 只在 $T\to\infty$ 的极限下给出标准高斯；有限 $T$ 时，式 (20.6) 给出 $q(\mathbf z_T\mid\mathbf x)=\mathcal N(\mathbf z_T\mid\sqrt{\alpha_T}\mathbf x,(1-\alpha_T)\mathbf I)$，因此“两分布相等”通常只是近似。

**20.11（★★）** 利用式 (20.15) 给出的分布 $q(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf x)$ 和式 (20.18) 给出的分布 $p(\mathbf z_{t-1}\mid\mathbf z_t,\mathbf w)$，证明式 (20.32) 一致性项中的 Kullback–Leibler 散度由式 (20.33) 给出。

**20.12（★★）** 将式 (20.34) 代入 (20.16)，把均值 $\mathbf m_t(\mathbf x,\mathbf z_t)$ 改写为式 (20.35) 中用原始数据向量 $\mathbf x$ 和噪声 $\boldsymbol\epsilon$ 表示的形式，其中 $\alpha_t$ 由式 (20.7) 定义。

**20.13（★★）** 证明扩散模型 ELBO 的重建项 (20.38) 可写成式 (20.39)。为此，用式 (20.36) 代入 $\boldsymbol\mu(\mathbf z_1,\mathbf w,1)$，用式 (20.1) 代入 $\mathbf x$，再利用从式 (20.7) 得到的 $\alpha_1=1-\beta_1$。

**20.14（★）** 得分函数在原文此处定义为 $\mathbf s(\mathbf x)=\nabla_{\mathbf x}p(\mathbf x\mid\mathbf w)$，因此它是与输入向量 $\mathbf x$ 维度相同的向量。考虑元素定义为下式的矩阵：

$$
M_{ij}=\frac{\partial s_i}{\partial x_j}
-\frac{\partial s_j}{\partial x_i}. \tag{20.64}
$$

证明：若得分函数由只有一个输出变量 $\phi(\mathbf x)$ 的神经网络的梯度 $\mathbf s=\nabla_{\mathbf x}\phi(\mathbf x)$ 定义，则对所有 $i,j$，矩阵元素 $M_{ij}=0$。注意，若用输入输出维度相同的深度神经网络直接表示得分函数 $\mathbf s(\mathbf x)=\nabla_{\mathbf x}p(\mathbf x\mid\mathbf w)$，则只有对角元素 $M_{ii}=0$；因此网络输出一般不是任何标量函数的梯度。

**译注：** 本题原文两处写 $\nabla_{\mathbf x}p(\mathbf x\mid\mathbf w)$；本章式 (20.42) 的得分函数定义是对数密度的梯度 $\nabla_{\mathbf x}\ln p(\mathbf x)$。此处照录原文。

**20.15（★★）** 考虑式 (20.42) 定义的得分函数的深度神经网络表示 $\mathbf s(\mathbf x,\mathbf w)$，其中 $\mathbf x$ 与 $\mathbf s$ 都是 $D$ 维。比较两种网络计算得分的复杂度：一种有 $D$ 个输出，直接表示得分函数；另一种只计算一个标量函数 $\phi(\mathbf x,\mathbf w)$，再通过自动微分间接计算得分函数。证明后一种方式通常计算成本更高。

**20.16（★★★）** 无法直接最小化得分函数损失 (20.43)，因为我们不知道真实数据密度 $p(\mathbf x)$ 的函数形式，因而无法写出得分函数 $\nabla_{\mathbf x}\ln p(\mathbf x)$ 的表达式。不过，利用分部积分（Hyvärinen，2005），可将式 (20.43) 改写为

$$
J(\mathbf w)=\int
\left\{\nabla\cdot\mathbf s(\mathbf x,\mathbf w)
+\frac{1}{2}\left\lVert\mathbf s(\mathbf x,\mathbf w)\right\rVert^2\right\}
p(\mathbf x)\,\mathrm d\mathbf x+\mathrm{const}, \tag{20.65}
$$

<!-- pdf-page: 616 -->

其中常数项与网络参数 $\mathbf w$ 无关，散度 $\nabla\cdot\mathbf s(\mathbf x,\mathbf w)$ 定义为

$$
\nabla\cdot\mathbf s
=\sum_{i=1}^{D}\frac{\partial s_i}{\partial x_i}
=\sum_{i=1}^{D}\frac{\partial^2\ln p(\mathbf x)}{\partial x_i^2}, \tag{20.66}
$$

其中 $D$ 是 $\mathbf x$ 的维度。推导式 (20.65) 时，先将式 (20.43) 中的平方展开。注意，包含 $\lVert\mathbf s(\mathbf x,\mathbf w)\rVert^2$ 的项已经出现，而包含 $\lVert\mathbf s_{\mathcal D}\rVert^2$ 的项可并入加性常数，其中 $\mathbf s_{\mathcal D}=\nabla\ln p_{\mathcal D}(\mathbf x)$。接着考虑两个函数乘积的求导公式：

$$
\frac{\mathrm d}{\mathrm dx}\{p(x)g(x)\}
=\frac{\mathrm dp(x)}{\mathrm dx}g(x)
+p(x)\frac{\mathrm dg(x)}{\mathrm dx}. \tag{20.67}
$$

对等式两边关于 $x$ 积分，重新整理，得到分部积分公式：

$$
\int_{-\infty}^{\infty}\frac{\mathrm dp(x)}{\mathrm dx}g(x)\,\mathrm dx
=-\int_{-\infty}^{\infty}p(x)\frac{\mathrm dg(x)}{\mathrm dx}\,\mathrm dx, \tag{20.68}
$$

其中假设 $p(\infty)=p(-\infty)=0$。将这一结果和定义 $\mathbf s_{\mathcal D}=\nabla\ln p(\mathbf x)$ 用于包含 $\mathbf s(\mathbf x,\mathbf w)^{\mathsf T}\mathbf s_{\mathcal D}$ 的项，即可完成证明。注意，计算式 (20.66) 中的二阶导数需要对每个导数单独作一次反向传播，因此总体计算成本随数据空间维度 $D$ 的平方增长（Martens、Sutskever 和 Swersky，2012）。这使该损失函数无法直接用于高维空间，所以研究者提出了**切片得分匹配**（sliced score matching）等技术，以减轻这种低效（Song 等，2019）。

**译注：** 式 (20.66) 的右端将模型得分 $\mathbf s(\mathbf x,\mathbf w)$ 的散度直接写成真实对数密度的拉普拉斯算子；两者一般不恒等。上段原文先写 $\mathbf s_{\mathcal D}=\nabla\ln p_{\mathcal D}(\mathbf x)$，后又写 $\mathbf s_{\mathcal D}=\nabla\ln p(\mathbf x)$。这里均照录原文。

**20.17（★★）** 本题证明得分函数损失 (20.50) 与式 (20.49) 在一个加性常数的意义下等价。先展开式 (20.49) 的平方，利用式 (20.47) 证明，来自式 (20.49) 的 $\mathbf s^{\mathsf T}\mathbf s$ 项与展开式 (20.50) 得到的对应项相同。再注意，式 (20.49) 中包含 $\lVert\nabla_{\mathbf z}\ln q\rVert^2$ 的项与 $\mathbf w$ 无关；式 (20.50) 的对应项也与 $\mathbf w$ 无关。因此，它们可视为损失函数中的加性常数，不影响训练。最后考虑式 (20.49) 中的交叉项。用式 (20.47) 代入 $q(\mathbf z)$，证明它等于式 (20.50) 的对应交叉项。由此证明两个损失函数只差一个加性常数。

**20.18（★）** 考虑由两个互不重叠的分布混合而成的概率分布。“互不重叠”是指：其中一个分布非零的位置，另一个分布必为零。分布形式为

$$
p(\mathbf x)=\lambda p_A(\mathbf x)+(1-\lambda)p_B(\mathbf x). \tag{20.69}
$$

<!-- pdf-page: 617 -->

证明：按式 (20.42) 在任意给定点 $\mathbf x$ 计算得分函数时，混合系数 $\lambda$ 不会出现。由此可知，式 (14.61) 定义的朗之万动力学不能以正确的比例从两个分量分布采样。如正文所述，加入来自一个宽分布的噪声可解决这个问题。

**20.19（★★）** 对于离散步骤，扩散模型中的前向噪声过程由式 (20.3) 定义。本题取连续时间极限，将其变为 SDE。先引入连续变化的方差函数 $\beta(t)$，使 $\beta_t=\beta(t)\Delta t$。对式 (20.3) 右边第一项中的平方根作泰勒展开，证明无穷小更新可写为

$$
\mathrm d\mathbf z=-\frac{1}{2}\beta(t)\mathbf z\,\mathrm dt
+\sqrt{\beta(t)}\,\mathrm d\mathbf v. \tag{20.70}
$$

可见，这是一般 SDE (20.55) 的一个特例。

**20.20（★）** 用式 (20.58) 代换 $\nabla_{\mathbf x}\ln p(c\mid\mathbf x)$，证明式 (20.59) 的得分函数可写为式 (20.60)。
