# 第 17 章 生成对抗网络

<aside class="chapter-guide"><strong>本章导读</strong><p>本章介绍生成器与判别器如何通过对抗训练学习数据分布，说明训练中可能出现的梯度过小与模式坍塌，并以图像生成和 CycleGAN 展示这类模型的应用。</p></aside>

<!-- pdf-page: 546 -->

<figure class="chapter-opener">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/chapter-opener.png" alt="第 17 章彩色章首图，英文标题为 Generative Adversarial Networks">
  <p class="figure-translation">图内文字：Generative Adversarial Networks → 生成对抗网络。</p>
</figure>

生成模型使用机器学习算法，从一组训练数据中学习分布，再从该分布生成新样本。例如，可以用动物图像训练生成模型，再用它生成新的动物图像。可以用分布 $p(\mathbf x\mid\mathbf w)$ 来理解这样的模型，其中 $\mathbf x$ 是数据空间中的向量，$\mathbf w$ 表示模型的可学习参数。许多时候，我们关注形式为 $p(\mathbf x\mid\mathbf c,\mathbf w)$ 的条件生成模型，其中 $\mathbf c$ 表示条件变量向量。对于动物图像生成模型，我们可能希望指定所生成的图像属于某种动物，比如由 $\mathbf c$ 的取值指定的猫或狗。

在图像生成等实际应用中，分布极为复杂，因此深度学习的引入大幅提升了生成模型的性能。我们在讨论基于 Transformer 的自回归大语言模型时，已经介绍过

<!-- pdf-page: 547 -->
<!-- join-previous-paragraph -->

一类重要的深度生成模型（见第 12 章）。我们还概述了基于非线性潜变量模型的四类重要生成模型（见第 16.4.4 节）；本章讨论其中第一类，即生成对抗网络。另外三类方法将在后续章节讨论。

<figure id="fig-17-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-1.png" alt="生成器产生合成小猫图像，与真实小猫图像一起送入判别器的 GAN 示意图">
  <figcaption>图 17.1：GAN 的示意图。判别器神经网络 $d(\mathbf x,\boldsymbol\phi)$ 经过训练，区分来自训练集的真实样本（这里是小猫图像）与生成器网络 $\mathbf g(\mathbf z,\mathbf w)$ 产生的合成样本。生成器通过生成逼真图像，力图最大化判别器的误差；判别器则通过更好地区分真实样本与合成样本，力图最小化同一误差。</figcaption>
  <p class="figure-translation">图内文字：real images → 真实图像；synthetic images → 合成图像；Generator → 生成器；Discriminator → 判别器；$\mathbf z$ 为潜变量，$t$ 为真实或合成的目标标签；$\mathbf g(\mathbf z,\mathbf w)$ 与 $d(\mathbf x,\boldsymbol\phi)$ 分别为生成器和判别器函数。</p>
</figure>

## 17.1 对抗训练

考虑一个生成模型，它通过非线性变换，把潜空间 $\mathbf z$ 映射到数据空间 $\mathbf x$。我们引入潜变量分布 $p(\mathbf z)$，它可以是简单的高斯分布：

$$
p(\mathbf z)=\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I),\tag{17.1}
$$

另有非线性变换 $\mathbf x=\mathbf g(\mathbf z,\mathbf w)$，由一个带可学习参数 $\mathbf w$ 的深度神经网络定义，这个网络称为**生成器**。两者共同隐式定义了 $\mathbf x$ 上的分布；我们的目标是使该分布拟合训练样本集 $\{\mathbf x_n\}$，其中 $n=1,\ldots,N$。然而，似然函数通常不能以闭式求值，因此不能通过优化似然函数来确定 $\mathbf w$。**生成对抗网络**（generative adversarial network，GAN；Goodfellow 等，2014；Ruthotto 和 Haber，2021）的关键思想是引入第二个网络——**判别器**，它与生成器一同训练，并提供用于更新生成器权重的训练信号。图 17.1 说明了这一点。

<!-- pdf-page: 548 -->

判别器网络的目标是区分数据集中的真实样本与生成器网络产生的合成样本，即“假”样本；它通过最小化常规的分类误差函数来训练。反过来，生成器网络的目标是合成与训练集服从同一分布的样本，以最大化此误差。因此，生成器与判别器彼此对抗，这也是“对抗”一词的由来。这是一个**零和博弈**的例子：一个网络的收益就是另一个网络的损失。判别器由此能够提供训练信号，用来训练生成器，将无监督的密度建模问题转化为一种监督学习形式。

### 17.1.1 损失函数

为准确表述这一过程，定义二元目标变量：

$$
t=1,\qquad\text{真实数据},\tag{17.2}
$$

$$
t=0,\qquad\text{合成数据}.\tag{17.3}
$$

判别器网络只有一个输出单元，使用 logistic sigmoid 激活函数，其输出表示数据向量 $\mathbf x$ 为真实样本的概率：

$$
P(t=1)=d(\mathbf x,\boldsymbol\phi).\tag{17.4}
$$

我们使用标准的交叉熵误差函数训练判别器网络，其形式为

$$
E(\mathbf w,\boldsymbol\phi)=-\frac{1}{N}\sum_{n=1}^{N}\left\{t_n\ln d_n+(1-t_n)\ln(1-d_n)\right\}.\tag{17.5}
$$

其中 $d_n=d(\mathbf x_n,\boldsymbol\phi)$ 是判别器网络针对输入向量 $\mathbf x_n$ 的输出，误差已除以数据点总数（交叉熵见第 1.2.4 节）。训练集既包含记为 $\mathbf x_n$ 的真实样本，也包含生成器网络输出的合成样本 $\mathbf g(\mathbf z_n,\mathbf w)$；这里 $\mathbf z_n$ 是从潜空间分布 $p(\mathbf z)$ 抽取的随机样本。真实样本的 $t_n=1$，合成样本的 $t_n=0$，因此可以把式 (17.5) 写成

$$
\begin{aligned}E_{\mathrm{GAN}}(\mathbf w,\boldsymbol\phi)
&=-\frac{1}{N_{\mathrm{real}}}\sum_{n\in\mathrm{real}}\ln d(\mathbf x_n,\boldsymbol\phi)\\
&\quad-\frac{1}{N_{\mathrm{synth}}}\sum_{n\in\mathrm{synth}}\ln\left(1-d\bigl(\mathbf g(\mathbf z_n,\mathbf w),\boldsymbol\phi\bigr)\right).
\end{aligned}\tag{17.6}
$$

**译注：** 式 (17.5) 以真实与合成数据的总数 $N$ 归一化，原书式 (17.6) 则分别以 $N_{\mathrm{real}}$ 和 $N_{\mathrm{synth}}$ 归一化。若两类样本各占一半，按字面计算，式 (17.6) 是式 (17.5) 的两倍；这里保留原书写法。

通常，真实数据点数 $N_{\mathrm{real}}$ 等于合成数据点数 $N_{\mathrm{synth}}$。生成器与判别器的组合可以通过随机梯度下降（见第 7 章）端到端训练，梯度由反向传播计算。不过，对抗训练的特殊之处在于：相对于 $\boldsymbol\phi$ 最小化误差，相对于 $\mathbf w$ 最大化误差。

<!-- pdf-page: 549 -->

可以使用标准的基于梯度的方法来实现这一最大化，只须反转梯度的符号。参数更新于是变为

$$
\Delta\boldsymbol\phi=-\lambda\nabla_{\boldsymbol\phi}E_n(\mathbf w,\boldsymbol\phi),\tag{17.7}
$$

$$
\Delta\mathbf w=\lambda\nabla_{\mathbf w}E_n(\mathbf w,\boldsymbol\phi).\tag{17.8}
$$

其中 $E_n(\mathbf w,\boldsymbol\phi)$ 表示针对数据点 $n$，或更一般地针对一个数据小批量定义的误差。式 (17.7) 与 (17.8) 中两项的符号不同，因为判别器接受训练以降低误差，而生成器接受训练以增大误差。实际训练时，交替更新生成器和判别器的参数，每次使用一个小批量只做一步梯度下降，随后重新生成一组合成样本。如果生成器找到了完美的解，判别器就无法区分真实数据和合成数据，其输出因而总是 $0.5$。GAN 训练完成后，可以丢弃判别器，从潜空间采样，并把样本送入已训练的生成器，以合成数据空间中的新样本。可以证明，如果生成网络和判别网络的灵活性没有限制，完全优化后的 GAN 的生成分布会与数据分布完全一致。图 1.3 展示了 GAN 生成的令人印象深刻的人脸图像；参见习题 17.1。

迄今讨论的 GAN 模型从无条件分布 $p(\mathbf x)$ 生成样本。例如，若用狗的图像训练，它可以生成合成的狗图像。我们也可以建立**条件 GAN**（Mirza 和 Osindero，2014），从条件分布 $p(\mathbf x\mid\mathbf c)$ 采样；条件向量 $\mathbf c$ 例如可以表示不同的犬种。为此，生成器与判别器都以 $\mathbf c$ 为额外输入，并用由图像及其标签组成的成对样本 $\{\mathbf x_n,\mathbf c_n\}$ 训练。GAN 训练完成后，把 $\mathbf c$ 设为相应类别向量，便可生成目标类别的图像。与为每个类别分别训练 GAN 相比，这样可以在所有类别之间联合学习共享的内部表示，从而更充分地利用数据。

### 17.1.2 GAN 训练实践

GAN 虽然能产生高质量结果，却因对抗学习而不易成功训练。此外，与常规的误差函数最小化不同，训练中目标函数既可能上升也可能下降，因此没有衡量进展的指标。

一种可能出现的问题称为**模式坍塌**（mode collapse）：训练期间，生成器网络的权重发生变化，使所有潜变量样本 $\mathbf z$ 都映射到有效输出的某个子集。极端情况下，输出可能只对应一个或少数几个 $\mathbf x$ 值。判别器随后会给这些实例赋值 $0.5$，训练便停止。例如，用手写数字训练的 GAN 可能只学会生成数字“3”的样本；尽管

<!-- pdf-page: 550 -->
<!-- join-previous-paragraph -->

判别器无法把这些样本与真正的“3”区分开，却没有发现生成器并未生成全部数字。

<figure id="fig-17-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-2.png" alt="真实数据分布和生成分布相距较远时判别器梯度接近零的曲线示意图">
  <figcaption>图 17.2：GAN 难以训练的概念示意图。一维数据空间 $x$ 中有固定但未知的数据分布 $p_{\mathrm{Data}}(x)$，以及初始生成分布 $p_G(x)$。最优判别函数 $d(x)$ 在真实或合成数据点附近的梯度几乎为零，使学习十分缓慢。平滑后的判别函数 $\tilde d(x)$ 可以加快学习。</figcaption>
  <p class="figure-translation">图内文字：$p_{\mathrm{Data}}(x)$ → 数据分布；$p_G(x)$ → 生成分布；$d(x)$ → 判别函数；$\tilde d(x)$ → 平滑后的判别函数；$x$ → 数据空间坐标。</p>
</figure>

观察图 17.2 可以理解 GAN 训练的困难。图中是一维数据空间 $x$，样本 $\{x_n\}$ 来自固定但未知的数据分布 $p_{\mathrm{Data}}(x)$；图中也有初始生成分布 $p_G(x)$ 及其样本。由于数据分布与生成分布相差很大，最优判别函数 $d(x)$ 很容易学到：它在两组样本之间有非常陡峭的下降段，但在真实样本或合成样本附近梯度几乎为零。考虑 GAN 误差函数 (17.6) 中的第二项。由于在生成样本所在的区域，$d\bigl(\mathbf g(\mathbf z,\mathbf w),\boldsymbol\phi\bigr)$ 等于零，生成器参数 $\mathbf w$ 的微小变化几乎不会改变判别器输出；因此梯度很小，学习也很慢。

可以用图 17.2 所示的平滑判别函数 $\tilde d(x)$ 来解决这一问题，使驱动生成器训练的梯度更强。**最小二乘 GAN**（least-squares GAN；Mao 等，2016）让判别器输出实数，而非 $(0,1)$ 内的概率，并以平方和误差函数取代交叉熵误差函数，从而实现平滑。另一种**实例噪声**（instance noise）技术（Sønderby 等，2016）同时向真实数据和合成样本加入高斯噪声，也能得到更平滑的判别函数。

为改进训练，研究者还提出了许多其他修改 GAN 误差函数及训练过程的方法（Mescheder、Geiger 和 Nowozin，2018）。一种常用改变是替换原始误差函数中的生成器网络项

<!-- pdf-page: 551 -->

$$
-\frac{1}{N_{\mathrm{synth}}}\sum_{n\in\mathrm{synth}}\ln\left(1-d\bigl(\mathbf g(\mathbf z_n,\mathbf w),\boldsymbol\phi\bigr)\right)\tag{17.9}
$$

为如下修改形式：

$$
\frac{1}{N_{\mathrm{synth}}}\sum_{n\in\mathrm{synth}}\ln d\bigl(\mathbf g(\mathbf z_n,\mathbf w),\boldsymbol\phi\bigr).\tag{17.10}
$$

第一种形式使图像为假样本的概率最小化，第二种形式则使图像为真实样本的概率最大化。图 17.3 可以帮助理解两者不同的性质。当生成分布 $p_G(x)$ 与真实数据分布 $p_{\mathrm{Data}}(x)$ 相差很大时，$d\bigl(\mathbf g(\mathbf z,\mathbf w)\bigr)$ 接近零，第一种形式的梯度很小；第二种形式的梯度则很大，因此训练更快。

<figure id="fig-17-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-3.png" alt="负对数 d 与对数一减 d 的曲线，在零和一附近斜率明显不同">
  <figcaption>图 17.3：$-\ln(d)$ 与 $\ln(1-d)$ 的曲线，显示当 $d$ 接近 $0$ 或 $1$ 时，两者的梯度行为截然不同。</figcaption>
  <p class="figure-translation">图内文字：$-\ln(d)$ → 负对数判别输出；$\ln(1-d)$ → 一减判别输出的对数；横轴 $x$ 标示图中从 $0$ 到 $1$ 的判别输出取值。</p>
</figure>

要更直接地确保生成分布 $p_G(x)$ 向数据分布 $p_{\mathrm{data}}(x)$ 靠近，可以修改误差准则，使其反映两个分布在数据空间中的距离。可用 **Wasserstein 距离**衡量，也称为**推土机距离**（earth mover's distance）。想象把生成分布 $p_G(x)$ 当作一堆土，经过一小步一小步搬运，形成数据分布 $p_{\mathrm{data}}(x)$。Wasserstein 度量是搬运的土的总量乘以平均搬运距离。把这堆土重新排列成 $p_{\mathrm{data}}(x)$ 有很多种方式，该度量选取平均搬运距离最小的方式。实际中无法直接实现这一过程，可以用实值输出的判别器网络近似，再通过权重裁剪限制判别函数相对于 $x$ 的梯度 $\nabla_xd(x,\boldsymbol\phi)$，得到 **Wasserstein GAN**（Arjovsky、Chintala 和 Bottou，2017）。

一种改进方法是对梯度引入惩罚，得到**梯度惩罚 Wasserstein GAN**（Gulrajani 等，2017），其误差函数为

$$
\begin{aligned}E_{\mathrm{WGAN\text{-}GP}}(\mathbf w,\boldsymbol\phi)
&=-\frac{1}{N_{\mathrm{real}}}\sum_{n\in\mathrm{real}}\left[\ln d(\mathbf x_n,\boldsymbol\phi)-\eta\left(\left\|\nabla_{\mathbf x_n}d(\mathbf x_n,\boldsymbol\phi)\right\|^2-1\right)^2\right]\\
&\quad+\frac{1}{N_{\mathrm{synth}}}\sum_{n\in\mathrm{synth}}\ln d\bigl(\mathbf g(\mathbf z_n,\mathbf w,\boldsymbol\phi)\bigr).
\end{aligned}\tag{17.11}
$$

**译注：** 原书式 (17.11) 最后一项把生成器写为 $\mathbf g(\mathbf z_n,\mathbf w,\boldsymbol\phi)$，与前文 $\mathbf g(\mathbf z_n,\mathbf w)$ 的参数形式不同；此外，前文称判别器为实值输出，本式却对 $d$ 取对数，若 $d\leq0$ 则无定义。这两处均照录原式，不能直接将其视为无歧义的标准 WGAN-GP 目标。

其中 $\eta$ 控制惩罚项的相对重要性。

<!-- pdf-page: 552 -->

## 17.2 图像 GAN

GAN 的基本思想催生了大量研究成果，包括许多算法进展和应用。图像生成是 GAN 最广泛、最成功的应用领域之一。早期 GAN 模型的生成器和判别器都使用全连接网络。然而，卷积网络（见第 10 章）有许多优点，尤其适合高分辨率图像。判别器网络以图像为输入、输出标量概率，因此标准卷积网络很合适。生成器网络则需把低维潜空间映射为高分辨率图像，因此使用基于**转置卷积**的网络（见第 10.5.3 节），如图 17.4 所示。

<figure id="fig-17-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-4.png" alt="从 100 维潜向量经过投影、重整形和四个卷积阶段生成 64 乘 64 彩色人脸图像">
  <figcaption>图 17.4：深度卷积 GAN 的架构示例，展示如何在网络的连续模块中使用转置卷积扩展维度。</figcaption>
  <p class="figure-translation">图内文字：project and reshape → 投影并重整形；conv 1–4 → 卷积阶段 1–4；$\mathbf z$ 为潜向量；$100$、$4\times4\times1024$、$8\times8\times512$、$16\times16\times256$、$32\times32\times128$、$64\times64\times3$ 分别标示输入维度和各阶段特征图尺寸。</p>
</figure>

可以从低分辨率开始，随着训练推进，逐步增添用于建模更精细细节的新层，使生成器和判别器网络逐渐增长，从而获得高质量图像（Karras 等，2017）。这会加快训练，并使模型能够从 $4\times4$ 图像开始，最终合成 $1024\times1024$ 的高分辨率图像。为了解某些 GAN 架构的规模和复杂度，考虑用于按类别条件生成图像的 **BigGAN** 模型，其架构如图 17.5 所示。

### 17.2.1 CycleGAN

作为 GAN 多样性的一个例子，我们来考察名为 **CycleGAN** 的架构（Zhu 等，2017）。它也说明，深度学习技术可以调整以解决传统的分类和密度估计等任务之外的其他问题，例如

<!-- pdf-page: 553 -->
<!-- join-previous-paragraph -->

把一张照片变成同一场景的莫奈风格绘画，或反过来把绘画变成照片。图 17.6 给出了经过训练的 CycleGAN 所生成的成对图像，展示它学会了这样的图像到图像转换。

<figure id="fig-17-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-5.png" alt="BigGAN 生成器整体架构及其残差块内部的上采样、卷积、归一化和跳跃连接">
  <figcaption>图 17.5：(a) BigGAN 模型中生成网络的架构，它有超过 $7{,}000$ 万个参数。(b) 生成网络中每个残差块的细节。判别网络有 $8{,}800$ 万个参数，结构与之有些类似，但用平均池化层降低维度，而不是用上采样增加维度。[根据 Brock、Donahue 和 Simonyan（2018）绘制。]</figcaption>
  <p class="figure-translation">图内文字：Residual Block → 残差块；Concat → 拼接；Non-Local → 非局部模块；Linear → 线性层；Split → 拆分；Add → 相加；Convolution → 卷积；ReLU → ReLU 激活；Batch Norm → 批量归一化；Up-sample → 上采样；$\mathbf z$ 为潜变量，$\mathbf c$ 为条件输入，$\mathbf x$ 为输出。</p>
</figure>

目标是学习两个双射（一一对应的映射）：一个把照片所在的域 $X$ 映射到莫奈绘画所在的域 $Y$，另一个沿反方向映射。为此，CycleGAN 使用两个条件生成器 $\mathbf g_X$ 与 $\mathbf g_Y$，以及两个判别器 $d_X$ 与 $d_Y$。生成器 $\mathbf g_X(\mathbf y,\mathbf w_X)$ 以一幅样本绘画 $\mathbf y\in Y$ 为输入，生成对应的合成照片；判别器 $d_X(\mathbf x,\boldsymbol\phi_X)$ 区分合成照片与真实照片。类似地，生成器 $\mathbf g_Y(\mathbf x,\mathbf w_Y)$ 以照片 $\mathbf x\in X$ 为输入，生成合成绘画 $\mathbf y$；判别器 $d_Y(\mathbf y,\boldsymbol\phi_Y)$ 区分合成绘画与真实绘画。因此，训练 $d_X$ 时使用 $\mathbf g_X$ 生成的合成照片与真实照片，训练 $d_Y$ 时则使用 $\mathbf g_Y$ 生成的合成绘画与

<!-- pdf-page: 554 -->
<!-- join-previous-paragraph -->

真实绘画。

<figure id="fig-17-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-6.png" alt="CycleGAN 将莫奈风格绘画转换为照片，以及将照片转换为莫奈风格绘画的两组成对图像">
  <figcaption>图 17.6：CycleGAN 的图像转换示例：上排由莫奈绘画合成照片风格图像，下排由照片合成莫奈绘画风格图像。[经许可引自 Zhu 等（2017）。]</figcaption>
  <p class="figure-translation">图内文字：Monet → photograph → 莫奈绘画 → 照片；photograph → Monet → 照片 → 莫奈绘画。</p>
</figure>

如果用标准 GAN 损失函数训练这一架构，模型会学会生成逼真的莫奈风格合成绘画和逼真的合成照片，却没有任何约束使生成绘画与对应照片看起来相像，反之亦然。因此，我们在损失函数中加入称为**循环一致性误差**的额外项；它包含两项，其构造如图 17.7 所示。

<figure id="fig-17-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-7.png" alt="照片经生成器转换为绘画再转换回照片，以原始照片与重建照片之间的差异计算循环一致性误差">
  <figcaption>图 17.7：计算样本照片 $\mathbf x_n$ 的循环一致性误差。首先，生成器 $\mathbf g_Y$ 把照片映射到绘画域，再由生成器 $\mathbf g_X$ 将所得向量映射回照片域。重建照片与原始照片 $\mathbf x_n$ 的差异构成循环一致性误差的一部分。对于绘画 $\mathbf y_n$，先由 $\mathbf g_X$ 映射成照片，再由 $\mathbf g_Y$ 映射回绘画，以类似过程计算另一部分。</figcaption>
  <p class="figure-translation">图内文字：photographs → 照片；paintings → 绘画；$X$ 与 $Y$ 分别为照片域与绘画域；$\mathbf x_n$ 为原始照片，$\mathbf g_Y(\mathbf x_n)$ 为合成绘画，$\mathbf g_X(\mathbf g_Y(\mathbf x_n))$ 为重建照片，$E_{\mathrm{cyc}}$ 表示循环一致性误差。</p>
</figure>

这样做的目标是：把照片转换为绘画，再转换回照片时，结果应接近原始照片；这可确保生成绘画保留了足够的照片信息，以供重建照片。类似地，把一幅绘画转换成照片，再转换回绘画，结果应接近

<!-- pdf-page: 555 -->
<!-- join-previous-paragraph -->

原始绘画。对训练集中的全部照片与绘画应用这一准则，得到如下形式的循环一致性误差：

$$
\begin{aligned}E_{\mathrm{cyc}}(\mathbf w_X,\mathbf w_Y)
&=\frac{1}{N_X}\sum_{n\in X}\left\|\mathbf g_X(\mathbf g_Y(\mathbf x_n))-\mathbf x_n\right\|_1\\
&\quad+\frac{1}{N_Y}\sum_{n\in Y}\left\|\mathbf g_Y(\mathbf g_X(\mathbf y_n))-\mathbf y_n\right\|_1.
\end{aligned}\tag{17.12}
$$

其中 $\|\cdot\|_1$ 表示 $L_1$ 范数。把循环一致性误差加到式 (17.6) 定义的通常 GAN 损失函数上，得到总误差函数：

$$
E_{\mathrm{GAN}}(\mathbf w_X,\boldsymbol\phi_X)+E_{\mathrm{GAN}}(\mathbf w_Y,\boldsymbol\phi_Y)+\eta E_{\mathrm{cyc}}(\mathbf w_X,\mathbf w_Y).\tag{17.13}
$$

其中系数 $\eta$ 决定 GAN 误差与循环一致性误差的相对重要性。图 17.8 展示了 CycleGAN 对一张照片与一幅绘画计算误差函数时的信息流。

<figure id="fig-17-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-8.png" alt="CycleGAN 两个方向的生成、判别与循环重建信息流示意图">
  <figcaption>图 17.8：CycleGAN 中的信息流。数据点 $\mathbf x_n$ 与 $\mathbf y_n$ 的总误差是四项误差之和。</figcaption>
  <p class="figure-translation">图内文字：$\mathbf x_n$、$\mathbf y_n$ 分别为照片与绘画样本；$\mathbf g_X$、$\mathbf g_Y$ 为两个方向的生成器；$d_X$、$d_Y$ 为判别器；$E_{\mathrm{GAN}}$ 为对抗误差，$E_{\mathrm{cyc}}$ 为循环一致性误差。</p>
</figure>

我们已看到 GAN 作为生成模型表现良好，但它也可以用于**表示学习**（见第 6.3.3 节）：通过无监督学习揭示数据集中丰富的统计结构。用卧室图像数据集训练图 17.4 所示的深度卷积 GAN 后（Radford、Metz 和 Chintala，2015），把从潜空间随机抽取的样本送入已训练的网络，生成图像也会如预期那样呈现卧室。此外，潜空间会以具有语义意义的方式组织起来。例如，沿潜空间中的平滑轨迹移动，并生成相应图像序列，就会得到一张图像到下一张图像的平滑过渡，如图 17.9 所示。

此外，还可以找出潜空间中对应于有语义意义的变换的方向。例如，对于人脸，一个方向可能对应人脸朝向的变化，其他方向则可能对应光照的变化，或微笑程度的变化。这些称为**解耦表示**，能够按指定属性合成新图像。图 17.10 来自一个用人脸图像训练的 GAN；它表明，性别或是否戴眼镜等语义属性对应潜空间中的特定方向。

<!-- pdf-page: 556 -->

<figure id="fig-17-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-9.png" alt="深度卷积 GAN 在潜空间连续移动时生成的多排卧室图像序列">
  <figcaption>图 17.9：用卧室图像训练的深度卷积 GAN 所生成的样本。每排图像都来自潜空间中随机位置之间的一段平滑路径。图像平滑过渡，而且每一张都像一间可信的卧室。例如，在最下面一排，墙上的电视逐渐变成窗户。[经许可引自 Radford、Metz 和 Chintala（2015）。]</figcaption>
</figure>

<figure id="fig-17-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-17/fig-17-10.png" alt="GAN 潜空间中的戴眼镜男性减去不戴眼镜男性加上不戴眼镜女性，生成戴眼镜女性的向量运算">
  <figcaption>图 17.10：已训练 GAN 潜空间中的向量运算示例。前三列中，先对生成这些图像的潜空间向量分别求平均，再对所得均值向量做运算，形成与右侧 $3\times3$ 阵列中央图像对应的新向量。给此向量加入噪声，可生成另外八张样本图像。最下面一排的四幅图说明：若直接在数据空间执行相同的运算，由于图像未对齐，只会得到模糊图像。[经许可引自 Radford、Metz 和 Chintala（2015）。]</figcaption>
  <p class="figure-translation">图内文字：man with glasses → 戴眼镜男性；man without glasses → 不戴眼镜男性；woman without glasses → 不戴眼镜女性；woman with glasses → 戴眼镜女性；Results of doing the same arithmetic in pixel space → 在像素空间执行同样运算的结果。减号、加号与等号分别表示向量减、加及其结果。</p>
</figure>

<!-- pdf-page: 557 -->

## 习题

**17.1（★★★）** 我们希望式 (17.6) 的 GAN 误差函数具有以下性质：当神经网络足够灵活时，生成器分布与真实数据分布相匹配之处是一个平稳点。本题考虑具有无限灵活性的网络模型，分别在对应于生成网络的整个概率分布 $p_G(\mathbf x)$ 空间，以及对应于判别网络的整个函数 $d(\mathbf x)$ 空间上优化，以证明这一结果。具体而言，假设在内部循环中已将判别模型优化，从而得到生成模型的有效外部循环误差函数。首先证明：当数据样本数量趋于无穷大时，GAN 误差函数 (17.6) 可以写成

$$
E(p_G,d)=-\int p_{\mathrm{data}}(\mathbf x)\ln d(\mathbf x)\,\mathrm d\mathbf x-\int p_G(\mathbf x)\ln\bigl(1-d(\mathbf x)\bigr)\,\mathrm d\mathbf x.\tag{17.14}
$$

其中 $p_{\mathrm{data}}(\mathbf x)$ 是真实数据点的固定分布。现在考虑在所有函数 $d(\mathbf x)$ 上进行变分优化（见附录 B）。证明：固定生成网络时，使 $E$ 最小化的判别器 $d(\mathbf x)$ 为

$$
d^\star(\mathbf x)=\frac{p_{\mathrm{data}}(\mathbf x)}{p_{\mathrm{data}}(\mathbf x)+p_G(\mathbf x)}.\tag{17.15}
$$

据此证明：误差函数 $E$ 可以写成关于生成网络 $p_G(\mathbf x)$ 的函数：

$$
\begin{aligned}C(p_G)
&=-\int p_{\mathrm{data}}(\mathbf x)\ln\left\{\frac{p_{\mathrm{data}}(\mathbf x)}{p_{\mathrm{data}}(\mathbf x)+p_G(\mathbf x)}\right\}\,\mathrm d\mathbf x\\
&\quad-\int p_G(\mathbf x)\ln\left\{\frac{p_G(\mathbf x)}{p_{\mathrm{data}}(\mathbf x)+p_G(\mathbf x)}\right\}\,\mathrm d\mathbf x.
\end{aligned}\tag{17.16}
$$

然后证明它可以改写成

$$
C(p_G)=-\ln(4)+\operatorname{KL}\!\left(p_{\mathrm{data}}\middle\|\frac{p_{\mathrm{data}}+p_G}{2}\right)+\operatorname{KL}\!\left(p_G\middle\|\frac{p_{\mathrm{data}}+p_G}{2}\right),\tag{17.17}
$$

其中 KL 散度 $\operatorname{KL}(p\|q)$ 由式 (2.100) 定义。最后，利用 $\operatorname{KL}(p\|q)\geqslant0$，且当且仅当所有 $\mathbf x$ 都满足 $p(\mathbf x)=q(\mathbf x)$ 时等号成立，证明 $p_G(\mathbf x)=p_{\mathrm{data}}(\mathbf x)$ 时 $C(p_G)$ 取最小值。注意，式 (17.17) 中两个 KL 散度项之和称为 $p_{\mathrm{data}}$ 与 $p_G$ 之间的 **Jensen–Shannon 散度**（见第 2.5.5 节）。与 KL 散度一样，它是非负的，且当且仅当两个分布相等时为零；但与 KL 散度不同，它对两个分布是对称的。

**译注：** 原书将两项 KL 散度之和称为 Jensen–Shannon 散度；按常用定义，Jensen–Shannon 散度是该和的一半。式 (17.17) 的代数形式与原书一致。

**17.2（★★★）** 本题探讨 GAN 训练的对抗性质可能造成的问题。考虑定义在两个参数 $a$ 和 $b$ 上的代价函数 $E(a,b)=ab$，它们分别类似于生成网络和判别

<!-- pdf-page: 558 -->
<!-- join-previous-paragraph -->

网络的参数。证明 $(a,b)=(0,0)$ 是该代价函数的平稳点。考察沿直线 $b=a$ 与 $b=-a$ 的二阶导数，证明 $(0,0)$ 是鞍点。再假设以无穷小步长优化这个误差函数，使变量成为连续时间函数 $a(t)$ 与 $b(t)$，由连续时间梯度下降定义：更新生成网络参数 $a(t)$ 以增大 $E(a,b)$，更新参数 $b(t)$ 以减小 $E(a,b)$。证明参数的演化服从

$$
\frac{\mathrm da}{\mathrm dt}=\eta\frac{\partial E}{\partial a},\qquad\frac{\mathrm db}{\mathrm dt}=-\eta\frac{\partial E}{\partial b}.\tag{17.18}
$$

据此证明 $a(t)$ 满足二阶微分方程

$$
\frac{\mathrm d^2a}{\mathrm dt^2}=-\eta^2a(t).\tag{17.19}
$$

验证下式是 (17.19) 的一个解：

$$
a(t)=C\cos(\eta t)+D\sin(\eta t),\tag{17.20}
$$

其中 $C$ 和 $D$ 是任意常数。若系统在 $t=0$ 时以 $a=1$、$b=0$ 初始化，求出 $C$、$D$ 的值，进而证明 $a(t)$ 和 $b(t)$ 在 $a,b$ 空间中沿以原点为中心、半径为一的圆运动，因此永远不会收敛到鞍点。

**17.3（★）** 考虑一个 GAN：训练集包含相同数量的猫图像和狗图像，而生成器网络已学会生成高质量的狗图像。证明：当判别器网络看到一张狗图像时，其最优输出为 $1/3$；判别器接受训练，输出的是该图像为真实图像的概率。
