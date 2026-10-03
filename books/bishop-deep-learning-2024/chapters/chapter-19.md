# 第 19 章 自编码器

<aside class="chapter-guide"><strong>本章导读</strong><p>本章先讨论确定性自编码器如何学习数据的内部表示，再引入变分自编码器，用证据下界、摊销推断和重参数化方法训练概率生成模型。</p></aside>

<!-- pdf-page: 574 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/chapter-opener.png" alt="第 19 章章首页彩色抽象图，原图写有 Autoencoders">
  <figcaption>第 19 章章首页图：自编码器。</figcaption>
  <p class="figure-translation">图内文字：Autoencoders → 自编码器。</p>
</figure>

深度学习的一个核心目标，是发现对后续一个或多个应用有用的数据表示。一种由来已久的内部表示学习方法，称为**自联想神经网络**（auto-associative neural network）或**自编码器**（autoencoder）。它是一个输入单元与输出单元数目相同的神经网络，训练目标是生成接近输入 $\mathbf x$ 的输出 $\mathbf y$。训练后，网络内某一层会为每个新输入给出表示 $\mathbf z(\mathbf x)$。这个网络可以视为两部分：**编码器**把输入 $\mathbf x$ 映射到隐藏表示 $\mathbf z(\mathbf x)$；**解码器**把隐藏表示映射到输出 $\mathbf y(\mathbf z)$。

若希望自编码器找到非平凡解，必须加入某种约束，否则网络只要把输入值复制到输出即可。例如，可限制 $\mathbf z$ 相对 $\mathbf x$ 的维度，或要求 $\mathbf z$ 是稀疏表示。

<!-- pdf-page: 575 -->
<!-- join-previous-paragraph -->

另一种方法是改变训练过程，迫使网络学会修复输入向量中的损坏，如加性噪声或缺失值。此类约束鼓励网络发现数据中有趣的结构，以取得良好的训练表现。

本章从确定性自编码器开始，随后推广到学习编码器分布 $p(\mathbf z\mid\mathbf x)$ 和解码器分布 $p(\mathbf y\mid\mathbf z)$ 的随机模型。这些概率模型称为**变分自编码器**，是学习非线性潜变量模型的四种方法中的第三种（见第 16.4.4 节）。

## 19.1 确定性自编码器

研究主成分分析（PCA）时，我们已经见过自编码器的一种简单形式（见第 16.1 节）。该模型通过线性变换，把输入向量投影到低维流形上，再通过另一线性变换，将投影近似重建到原数据空间。利用神经网络的非线性，可以定义一种非线性 PCA，此时潜在流形不再是数据空间中的线性子空间。方法是令网络的输出数与输入数相同，并针对训练集优化权重，使输入与输出之间的重建误差度量最小。

简单自编码器很少直接用于现代深度学习，因为它们既不能在潜空间提供语义上有意义的表示，也不能直接从数据分布生成新样本。不过，它们是变分自编码器等更强大深度生成模型的重要概念基础（见第 19.2 节）。

### 19.1.1 线性自编码器

先考虑图 19.1 所示的多层感知机：它有 $D$ 个输入、$D$ 个输出单元和 $M$ 个隐藏单元，且 $M<D$。训练目标就是输入向量自身，因此网络尝试把每个输入向量映射回自身。这种网络称为形成一种**自联想映射**。由于隐藏单元少于输入单元，一般无法完美重建全部输入向量。因此，通过最小化衡量输入向量与其重建结果不一致程度的误差函数，确定网络参数 $\mathbf w$。具体选择如下平方和误差：

$$
E(\mathbf w)=\frac12\sum_{n=1}^{N}\lVert\mathbf y(\mathbf x_n,\mathbf w)-\mathbf x_n\rVert^2.\tag{19.1}
$$

若隐藏单元使用线性激活函数，可以证明误差函数有唯一的全局最小值，在此最小值处，网络

<!-- pdf-page: 576 -->
<!-- join-previous-paragraph -->

把数据投影到由前 $M$ 个主成分张成的 $M$ 维子空间（Bourlard 和 Kamp，1988；Baldi 和 Hornik，1989）。因此，图 19.1 中通向隐藏单元的权重向量构成张成主子空间的一组基。但这些向量未必正交或归一化。这一结果并不令人意外，因为 PCA 与神经网络都依靠线性降维，并最小化相同的平方和误差函数。

<figure id="fig-19-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-1.png" alt="D 个输入、M 个隐藏单元和 D 个输出的两层权重自编码器">
  <figcaption>图 19.1：具有两层权重的自编码器神经网络。通过最小化平方和误差，训练该网络把输入向量映射回自身。即使隐藏层使用非线性单元，这种网络仍等价于线性主成分分析。为清晰起见，图中省略了表示偏置参数的连线。</figcaption>
  <p class="figure-translation">图内文字：inputs → 输入；outputs → 输出。$x_1,x_D$ 为输入单元，$z_1,z_M$ 为隐藏单元，$y_1,y_D$ 为输出单元。</p>
</figure>

也许会以为，在图 19.1 的网络中让隐藏单元使用非线性激活函数，就能突破线性流形的限制。然而，即使隐藏单元是非线性的，误差最小的解仍是向主成分子空间的投影（Bourlard 和 Kamp，1988）。因此，使用两层神经网络降维并无优势。基于奇异值分解（SVD）的标准 PCA 方法保证在有限时间内得到正确解，还会生成有序的特征值及对应的正交归一特征向量。

### 19.1.2 深层自编码器

不过，若网络增加更多非线性层，情况就不同了。考虑图 19.2 的四层自联想网络。输出单元仍是线性的，第二层的 $M$ 个单元也可以是线性的，但第一层和第三层使用 sigmoid 非线性激活函数。网络仍通过最小化式 (19.1) 的误差函数训练。可以把它视为图 19.2 所示的两个连续函数映射 $F_1$ 和 $F_2$。第一个映射 $F_1$ 把原始 $D$ 维数据投影到第二层单元激活值所定义的 $M$ 维子空间 $S$。由于第一层使用非线性单元，该映射十分一般，并不局限于线性形式。同样，网络后半部分定义了一个从 $M$ 维隐藏空间返回原始 $D$ 维输入空间的任意函数映射。图 19.3 以 $D=3$、$M=2$ 展示了简单的几何解释。

这样的网络实际上执行非线性 PCA。它的优点是不局限于线性变换，不过它包含标准

<!-- pdf-page: 577 -->
<!-- join-previous-paragraph -->

PCA 作为特例。然而，训练网络需要非线性优化，因为式 (19.1) 的误差函数不再是网络参数的二次函数。必须使用计算代价较高的非线性优化技术，而且可能找到误差函数的次优局部最小值。此外，必须在训练前指定子空间的维度。

<figure id="fig-19-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-2.png" alt="加入非线性隐藏层的四层自联想网络，映射 F1 和 F2 分别编码与解码">
  <figcaption>图 19.2：加入额外的非线性隐藏层，可得到能够执行非线性降维的自联想网络。</figcaption>
  <p class="figure-translation">图内文字：inputs → 输入；outputs → 输出；nonlinear → 非线性。$F_1$ 为编码映射，$F_2$ 为解码映射；$x_1,x_D$、$z_1,z_M$、$y_1,y_D$ 分别为输入、潜变量和输出单元。</p>
</figure>

### 19.1.3 稀疏自编码器

约束内部表示的另一种方法，是不限制某个隐藏层的节点数，而用正则项鼓励稀疏表示，使有效维度降低。一个简单选择是 $L_1$ 正则项，因为它鼓励稀疏性（见第 9.2.2 节），由此得到如下正则化误差函数：

<figure id="fig-19-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-3.png" alt="三维输入经 F1 投影到二维潜空间，再经 F2 映射到三维非平面流形">
  <figcaption>图 19.3：图 19.2 中网络映射的几何解释，其中模型有 $D=3$ 个输入和第二层中的 $M=2$ 个单元。从潜空间出发的函数 $F_2$，定义流形 $S$ 如何嵌入较高维数据空间。由于 $F_2$ 可为非线性，$S$ 的嵌入可以不是平面，如图所示。函数 $F_1$ 则定义了从原始 $D$ 维数据空间到 $M$ 维潜空间的投影。</figcaption>
  <p class="figure-translation">图内符号：$x_1,x_2,x_3$ 为输入坐标；$z_1,z_2$ 为潜空间坐标；$y_1,y_2,y_3$ 为输出坐标；$F_1$ 为投影，$F_2$ 为非线性映射，$S$ 为嵌入流形；$\mathbf x,\mathbf z,\mathbf y$ 分别标出输入点、潜点与输出点。</p>
</figure>

<!-- pdf-page: 578 -->

$$
\widetilde E(\mathbf w)=E(\mathbf w)+\lambda\sum_{k=1}^{K}|z_k|.\tag{19.2}
$$

其中 $E(\mathbf w)$ 是未正则化的误差，$k$ 的求和遍及某个隐藏层中所有单元的激活值。注意，正则化通常施加于网络参数，这里却施加于单元激活值。梯度下降训练所需的导数仍可按通常方式，用自动微分求出。

### 19.1.4 去噪自编码器

前面看到，对简单自编码器潜空间层的维度加以约束很重要，可避免模型仅学会恒等映射。另一种同样迫使模型发现数据中有趣内部结构的方法，是使用**去噪自编码器**（Vincent 等，2008）。做法是将每个输入向量 $\mathbf x_n$ 用噪声损坏，得到修改后的向量 $\widetilde{\mathbf x}_n$，再将其输入自编码器，得到输出 $\mathbf y(\widetilde{\mathbf x}_n,\mathbf w)$。训练网络时，最小化如下平方和误差等函数，以重建原始无噪声输入：

$$
E(\mathbf w)=\sum_{n=1}^{N}\lVert\mathbf y(\widetilde{\mathbf x}_n,\mathbf w)-\mathbf x_n\rVert^2.\tag{19.3}
$$

一种噪声形式，是将随机选取的一部分输入变量置为零。这类输入的比例 $\nu$ 表示噪声水平，范围为 $0\leqslant\nu\leqslant1$。也可以给每个输入变量加入独立的零均值高斯噪声，其大小由高斯分布的方差控制。网络通过学习为输入数据去噪，被迫学习数据结构的某些方面。例如，若数据是图像，学习到相邻像素值高度相关，便可修复受噪声损坏的像素。

更正式地说，去噪自编码器的训练与**分数匹配**（score matching）有关（Vincent，2011），其中分数定义为 $\mathbf s(\mathbf x)=\nabla_{\mathbf x}\ln p(\mathbf x)$。图 19.4 为这种关系提供了直观解释。自编码器学会逆转扰动向量 $\widetilde{\mathbf x}_n-\mathbf x_n$，因而在数据空间的每一点学到一个指向流形、亦即指向高数据密度区域的向量。分数向量 $\nabla\ln p(\mathbf x)$ 也指向高数据密度区域。讨论同样学习从受噪声损坏输入中移除噪声的扩散模型时，我们将更深入探讨分数匹配与去噪的关系（见第 20.3 节）。

### 19.1.5 掩码自编码器

前面看到，BERT 等 Transformer 模型可以通过随机遮盖输入的部分内容，借助自监督学习得到丰富的自然语言内部表示。自然会问，类似方法能否用于

<!-- pdf-page: 579 -->
<!-- join-previous-paragraph -->

自然图像（见第 12.2 节）。在**掩码自编码器**（masked autoencoder；He 等，2021）中，深层网络以图像的受损版本为输入，重建原图，这与去噪自编码器类似。不过，这里的损坏形式是遮盖或丢弃部分输入图像。该方法通常与视觉 Transformer 架构合用，因为只需将随机选取的一部分输入图块 token 传给编码器，就能轻松实现遮盖（见第 12.4.1 节）。整个算法概括于图 19.5。

<figure id="fig-19-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-4.png" alt="被加性噪声扰动的数据点由箭头映回低维数据流形">
  <figcaption>图 19.4：在去噪自编码器中，假定位于数据空间低维流形上的数据点受到加性噪声污染。自编码器学习把受损数据点映回原值，从而在数据空间各点学得一个指向流形的向量。</figcaption>
  <p class="figure-translation">图内文字：corrupted data point → 受损数据点；original data point → 原始数据点；data manifold → 数据流形。</p>
</figure>

与语言相比，图像具有更高的冗余性和更强的局部相关性。句子中漏掉一个词可能大幅增加歧义，而从图像中移除随机图块，通常对图像语义影响很小。因此，在遮盖相当高比例的输入图像时，往往能学到最好的内部表示：典型比例是 $75\%$，而 BERT 的遮盖比例是 $15\%$。BERT 用固定的掩码 token 替换被遮盖输入；掩码自编码器则直接省去被遮盖图块。省去大量输入图块能显著节约计算，尤其是 Transformer 处理单个训练样本的计算需求会随输入序列长度不利地增长，所以掩码自编码器很适合大型 Transformer 编码器的预训练。

解码器层也是 Transformer，因此必须在原图像的维度上工作。由于 Transformer 的输出维度与输入相同，需要在编码器输出与解码器输入之间恢复图像维度。具体方法是重新放入被遮盖的图块，用固定的掩码 token 向量表示，并给每个图块 token 加入位置编码信息。尽管解码器表示的维度高得多，解码器 Transformer 的可学习参数仍远少于编码器。解码器输出后接一个可学习线性层，

<!-- pdf-page: 580 -->
<!-- join-previous-paragraph -->

将输出表示映射到像素值空间；训练误差函数就是每张图像缺失图块上的平均平方误差。图 19.6 给出了训练后的掩码自编码器所重建的图像，展示了它生成语义上可信重建的能力。不过，最终目标是学得供后续任务使用的内部表示。为此，丢弃解码器，对不经遮盖的完整图像应用编码器，再接上针对目标应用微调的一组新输出层。还要注意，虽然该算法最初为图像数据设计，理论上也可用于任何模态。

<figure id="fig-19-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-5.png" alt="掩码自编码器的训练架构：输入图块经编码器和解码器重建遮盖图块">
  <figcaption>图 19.5：训练阶段的掩码自编码器架构。目标是输入的补集，因为损失只施加于被遮盖的图块。训练后丢弃解码器，使用编码器将图像映射为内部表示，以供后续任务使用。</figcaption>
  <p class="figure-translation">图内文字：inputs → 输入；encoder → 编码器；decoder → 解码器；outputs → 输出；predictions → 预测结果；targets → 目标值。</p>
</figure>

## 19.2 变分自编码器

前面已经看到，由下式给出的潜变量模型似然函数

$$
p(\mathbf x\mid\mathbf w)=\int p(\mathbf x\mid\mathbf z,\mathbf w)p(\mathbf z)\,\mathrm d\mathbf z,\tag{19.4}
$$

当 $p(\mathbf x\mid\mathbf z,\mathbf w)$ 由深度神经网络定义时无法直接计算，因为对 $\mathbf z$ 的积分不能解析求出。**变分自编码器**（variational autoencoder，简称

<!-- pdf-page: 581 -->
<!-- join-previous-paragraph -->

VAE；Kingma 和 Welling，2013；Rezende、Mohamed 和 Wierstra，2014；Doersch，2016；Kingma 和 Welling，2019）在训练模型时改用这个似然的近似。VAE 有三个关键思想：(i) 用证据下界（ELBO）近似似然函数，因此与 EM 算法密切相关（见第 15.3 节）；(ii) **摊销推断**，即使用第二个模型——编码器网络——近似 E 步中潜变量的后验分布，而不为每个数据点精确计算后验；(iii) 使用**重参数化技巧**，使编码器模型可以实际训练。

<figure id="fig-19-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-6.png" alt="四组图像，每组依次为遮盖八成图块的输入、重建图像和原图">
  <figcaption>图 19.6：训练后的掩码自编码器重建图像的四个例子，输入图块中有 $80\%$ 被遮盖。每组左侧为遮盖图像，中间为重建图像，右侧为原图。［原书据 He 等（2021），经许可使用。］</figcaption>
  <p class="figure-translation">图内无英文标签；每组三幅图从左至右依次是被遮盖的输入、重建结果、原始图像。</p>
</figure>

考虑一个生成模型：$D$ 维数据变量 $\mathbf x$ 的条件分布 $p(\mathbf x\mid\mathbf z,\mathbf w)$ 由深度神经网络 $\mathbf g(\mathbf z,\mathbf w)$ 的输出控制。例如，$\mathbf g(\mathbf z,\mathbf w)$ 可表示高斯条件分布的均值。再考虑 $M$ 维潜变量 $\mathbf z$ 的分布，取为零均值、单位方差的高斯分布：

$$
p(\mathbf z)=\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I).\tag{19.5}
$$

为推导 VAE 近似，先回顾：对于描述潜变量 $\mathbf z$ 空间的任意概率分布 $q(\mathbf z)$，存在如下关系（见第 15.4 节）：

$$
\ln p(\mathbf x\mid\mathbf w)=\mathcal L(\mathbf w)+\operatorname{KL}\bigl(q(\mathbf z)\parallel p(\mathbf z\mid\mathbf x,\mathbf w)\bigr),\tag{19.6}
$$

其中 $\mathcal L$ 是**证据下界**（ELBO），也称变分下界，定义为

$$
\mathcal L(\mathbf w)=\int q(\mathbf z)\ln\left\{\frac{p(\mathbf x\mid\mathbf z,\mathbf w)p(\mathbf z)}{q(\mathbf z)}\right\}\,\mathrm d\mathbf z.\tag{19.7}
$$

<!-- pdf-page: 582 -->

KL 散度 $\operatorname{KL}(\cdot\parallel\cdot)$ 定义为

$$
\operatorname{KL}\bigl(q(\mathbf z)\parallel p(\mathbf z\mid\mathbf x,\mathbf w)\bigr)=-\int q(\mathbf z)\ln\left\{\frac{p(\mathbf z\mid\mathbf x,\mathbf w)}{q(\mathbf z)}\right\}\,\mathrm d\mathbf z.\tag{19.8}
$$

由于 KL 散度满足 $\operatorname{KL}(q\parallel p)\geqslant0$，可知

$$
\ln p(\mathbf x\mid\mathbf w)\geqslant\mathcal L.\tag{19.9}
$$

因此，$\mathcal L$ 是 $\ln p(\mathbf x\mid\mathbf w)$ 的下界。虽然对数似然 $\ln p(\mathbf x\mid\mathbf w)$ 无法直接计算，下文将说明如何用蒙特卡洛估计求出下界，因此它可用于近似真实对数似然。

现在考虑训练集 $\mathcal D=\{\mathbf x_1,\ldots,\mathbf x_N\}$，假设这些数据点从模型分布 $p(\mathbf x)$ 独立抽取。该数据集的对数似然函数为

$$
\ln p(\mathcal D\mid\mathbf w)=\sum_{n=1}^{N}\mathcal L_n+\sum_{n=1}^{N}\operatorname{KL}\bigl(q_n(\mathbf z_n)\parallel p(\mathbf z_n\mid\mathbf x_n,\mathbf w)\bigr),\tag{19.10}
$$

其中

$$
\mathcal L_n=\int q_n(\mathbf z_n)\ln\left\{\frac{p(\mathbf x_n\mid\mathbf z_n,\mathbf w)p(\mathbf z_n)}{q_n(\mathbf z_n)}\right\}\,\mathrm d\mathbf z_n.\tag{19.11}
$$

注意，这里给每个数据向量 $\mathbf x_n$ 引入了相应潜变量 $\mathbf z_n$，与先前的混合模型和概率 PCA 模型一样（见第 15.2、16.2 节）。因此，每个潜变量都有独立的分布 $q_n(\mathbf z_n)$，可以分别优化。

式 (19.10) 对分布 $q_n(\mathbf z)$ 的任何选择都成立，所以可选择使下界 $\mathcal L_n$ 最大的分布；等价地，选择使 KL 散度 $\operatorname{KL}(q_n(\mathbf z_n)\parallel p(\mathbf z_n\mid\mathbf x_n,\mathbf w))$ 最小的分布。对于前面讨论的简单高斯混合模型和概率 PCA 模型，我们可以在 EM 算法的 E 步精确计算后验分布，即把每个 $q_n(\mathbf z_n)$ 设为对应后验分布 $p(\mathbf z_n\mid\mathbf x_n,\mathbf w)$。这使 KL 散度为零，下界便等于真实对数似然。图 19.7 用前面讨论生成对抗网络时介绍的简单例子，说明后验分布的含义（见第 16.4.1 节）。

由贝叶斯定理，$\mathbf z_n$ 的精确后验分布为

$$
p(\mathbf z_n\mid\mathbf x_n,\mathbf w)=\frac{p(\mathbf x_n\mid\mathbf z_n,\mathbf w)p(\mathbf z_n)}{p(\mathbf x_n\mid\mathbf w)}.\tag{19.12}
$$

对于深度生成模型，分子容易计算。但分母是前述无法直接求出的似然函数，因此必须近似后验分布。原则上，可以为每个分布 $q_n(\mathbf z_n)$ 分别设立参数化模型，并对每个模型做数值优化，

<!-- pdf-page: 583 -->
<!-- join-previous-paragraph -->

但这会消耗大量计算，特别是数据集很大时；此外，每次更新 $\mathbf w$ 后，还须重新计算这些分布。下面改用基于第二个神经网络的另一种更高效的近似框架。

<figure id="fig-19-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-7.png" alt="香蕉形二维数据分布与双峰后验密度曲线">
  <figcaption>图 19.7：对图 16.13 相同模型的后验分布进行计算。(b) 最右图中的边缘分布 $p(\mathbf x)$ 呈香蕉形，指定数据点 $\mathbf x^\star$ 更靠近该形状的两端而非中部。因此，尽管先验分布 $p(\mathbf z)$ 是单峰的，(a) 所示后验分布 $p(\mathbf z\mid\mathbf x^\star)$ 却是双峰的。［据 Prince（2020）图，原书经许可使用。］</figcaption>
  <p class="figure-translation">图内符号：$z$ 为潜空间横轴；$p(z)$ 为先验密度，$p(z\mid x^\star)$ 为指定数据点的后验密度；$x_1,x_2$ 为数据空间坐标；$x^\star$ 为指定数据点；(a)、(b) 对应两部分。</p>
</figure>

### 19.2.1 摊销推断

在变分自编码器中，不再试图为每个数据点 $\mathbf x_n$ 分别计算后验分布 $p(\mathbf z_n\mid\mathbf x_n,\mathbf w)$，而是训练一个称为**编码器网络**的神经网络，近似所有这些分布。这种方法称为**摊销推断**（amortized inference），要求编码器产生一个以 $\mathbf x$ 为条件的分布 $q(\mathbf z\mid\mathbf x,\boldsymbol\phi)$，其中 $\boldsymbol\phi$ 表示网络参数。证据下界给出的目标函数此时同时依赖 $\boldsymbol\phi$ 和 $\mathbf w$；我们用基于梯度的优化方法，对两组参数联合最大化该下界。

因此，VAE 包含两个参数互不相同、但一起训练的神经网络：编码器网络把数据向量映射到潜空间；原有网络把潜空间向量映射回数据空间，所以可视为解码器网络。这与简单的神经网络自编码器模型相似，只是现在定义了潜空间上的概率分布（见第 19.1 节）。下文将看到，编码器按贝叶斯定理计算解码器的近似概率逆映射。

编码器的一个典型选择，是具有对角协方差矩阵的高斯分布，其均值参数 $\mu_j$ 与方差参数 $\sigma_j^2$ 由以 $\mathbf x$ 为输入的神经网络的

<!-- pdf-page: 584 -->
<!-- join-previous-paragraph -->

输出给出：

$$
q(\mathbf z\mid\mathbf x,\boldsymbol\phi)=\prod_{j=1}^{M}\mathcal N\bigl(z_j\mid\mu_j(\mathbf x,\boldsymbol\phi),\sigma_j^2(\mathbf x,\boldsymbol\phi)\bigr).\tag{19.13}
$$

<figure id="fig-19-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-8.png" alt="两幅曲线图展示固定解码器和固定编码器参数时提高证据下界">
  <figcaption>图 19.8：证据下界（ELBO）的优化示意。(a) 给定解码器网络参数 $\mathbf w$ 的值 $\mathbf w_0$，优化编码器网络参数 $\boldsymbol\phi$ 可提高下界。(b) 给定 $\boldsymbol\phi$，优化 $\mathbf w$ 可提高 ELBO。蓝线表示的 ELBO 总低于红线表示的对数似然，因为编码器网络通常无法与真实后验分布完全吻合。</figcaption>
  <p class="figure-translation">图内符号：横轴 $\mathbf w$ 为解码器参数；红线 $\ln p(\mathbf x\mid\mathbf w)$ 为对数似然；蓝线 $\mathcal L(\mathbf w,\boldsymbol\phi)$ 为不同编码器参数下的证据下界；$\mathbf w_0,\mathbf w_1$ 为参数位置；(a)、(b) 为两个优化步骤。</p>
</figure>

注意，均值 $\mu_j(\mathbf x,\boldsymbol\phi)$ 可取区间 $(-\infty,\infty)$ 内的值，因此相应输出单元的激活函数可以是线性的；而方差 $\sigma_j^2(\mathbf x,\boldsymbol\phi)$ 必须非负，所以相应输出单元通常使用 $\exp(\cdot)$ 作为激活函数。

目标是用基于梯度的优化方法，同时对两组参数 $\boldsymbol\phi$ 和 $\mathbf w$ 最大化下界，通常采用基于小批量的随机梯度下降。虽然实际联合优化参数，概念上仍可仿照 EM 算法，想象交替优化 $\boldsymbol\phi$ 和 $\mathbf w$，如图 19.8 所示。

与 EM 的一个关键区别是：对给定 $\mathbf w$，优化编码器参数 $\boldsymbol\phi$ 一般不会使 KL 散度降为零。编码器网络不能完美预测潜变量的后验分布，因此下界与真实对数似然之间仍有差距。虽然基于深度神经网络的编码器很灵活，但不应期待它精确建模真实后验分布，因为：(i) 真实的条件后验分布不会是

<!-- pdf-page: 585 -->
<!-- join-previous-paragraph -->

可分解的高斯分布；(ii) 即使大型神经网络，灵活性也有限；(iii) 训练过程只是近似优化。图 19.9 概括了 EM 算法与 ELBO 优化之间的关系。

<figure id="fig-19-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-9.png" alt="两幅曲线示意图比较 EM 迭代与 VAE 联合优化证据下界">
  <figcaption>图 19.9：比较 EM 算法与 VAE 中的 ELBO 优化。(a) 在 EM 算法中，交替执行 E 步更新变分后验分布、M 步更新模型参数。E 步精确时，每次 E 步后下界与对数似然之间的差距降为零。(b) 在 VAE 中，联合优化编码器网络参数 $\boldsymbol\phi$（类似 E 步）与解码器网络参数 $\mathbf w$（类似 M 步）。</figcaption>
  <p class="figure-translation">图内标记：E → E 步；M → M 步；红线 $\ln p(\mathbf x\mid\mathbf w)$ 为对数似然；蓝线为证据下界；(a)、(b) 分别表示 EM 与 VAE。</p>
</figure>

### 19.2.2 重参数化技巧

遗憾的是，按当前形式，下界 (19.11) 仍无法直接计算，因为它对潜变量 $\{\mathbf z_n\}$ 积分，而解码器网络使被积函数以复杂方式依赖潜变量。对于数据点 $\mathbf x_n$，它对下界的贡献可写为

$$
\begin{aligned}\mathcal L_n(\mathbf w,\boldsymbol\phi)&=\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln\left\{\frac{p(\mathbf x_n\mid\mathbf z_n,\mathbf w)p(\mathbf z_n)}{q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)}\right\}\,\mathrm d\mathbf z_n\\&=\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln p(\mathbf x_n\mid\mathbf z_n,\mathbf w)\,\mathrm d\mathbf z_n-\operatorname{KL}\bigl(q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\parallel p(\mathbf z_n)\bigr).\end{aligned}\tag{19.14}
$$

右边第二项是两个高斯分布间的 KL 散度，可以解析计算（见习题 2.27）：

$$
\operatorname{KL}\bigl(q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\parallel p(\mathbf z_n)\bigr)=\frac12\sum_{j=1}^{M}\left\{1+\ln\sigma_j^2(\mathbf x_n)-\mu_j^2(\mathbf x_n)-\sigma_j^2(\mathbf x_n)\right\}.\tag{19.15}
$$

**译注：** 原书式 (19.15) 右边实际是这两个高斯分布的**负 KL 散度**，与左边标记的 KL 符号相反。式 (19.14) 的目标为“重建期望减 KL”；式 (19.19) 以加号使用此负 KL 表达式。这里保留原式，计算时须注意符号。

<!-- pdf-page: 586 -->

<figure id="fig-19-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-10.png" alt="直接固定潜变量抽样值会阻断从解码器向编码器的误差信号反向传播">
  <figcaption>图 19.10：用固定为某个抽样值的潜变量 $\mathbf z$ 估计 ELBO 时，误差信号无法反向传播到编码器网络。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf x$ 为输入，$\boldsymbol\phi$ 为编码器参数，$\mu_i,\sigma_i^2$ 为编码器输出的均值与方差，$\mathbf z$ 为抽样潜变量，$\mathbf w$ 为解码器参数，$p(\mathbf x\mid\mathbf z,\mathbf w)$ 为条件分布；红箭头为误差反向传播，断开处表示传播受阻。</p>
</figure>

对于式 (19.14) 的第一项，可以尝试用简单的蒙特卡洛估计近似对 $\mathbf z_n$ 的积分：

$$
\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln p(\mathbf x_n\mid\mathbf z_n,\mathbf w)\,\mathrm d\mathbf z_n\simeq\frac1L\sum_{l=1}^{L}\ln p(\mathbf x_n\mid\mathbf z_n^{(l)},\mathbf w),\tag{19.16}
$$

其中 $\{\mathbf z_n^{(l)}\}$ 是从编码器分布 $q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)$ 抽取的样本。右边容易对 $\mathbf w$ 求导；但对 $\boldsymbol\phi$ 求梯度存在困难。$\boldsymbol\phi$ 的变化会改变抽样所用的分布 $q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)$，而已抽出的样本是固定值，因此无法得到样本对 $\boldsymbol\phi$ 的导数。从概念上看，把 $\mathbf z_n$ 固定为某个样本值，会阻断误差信号向编码器网络反向传播，如图 19.10 所示。

可用**重参数化技巧**解决这个问题：重新表述蒙特卡洛抽样过程，使对 $\boldsymbol\phi$ 的导数可以显式计算。先注意，若 $\epsilon$ 是零均值、单位方差的高斯随机变量，则

$$
z=\sigma\epsilon+\mu\tag{19.17}
$$

服从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布（见习题 19.2）。现在将其用于式 (19.16) 的样本，其中 $\mu$ 和 $\sigma$ 由编码器网络输出 $\mu_j(\mathbf x_n,\boldsymbol\phi)$、$\sigma_j^2(\mathbf x_n,\boldsymbol\phi)$ 定义，分别代表分布 (19.13) 的均值与方差。不直接抽取 $\mathbf z_n$，而是抽取 $\epsilon$，再用式 (19.17) 计算相应的 $\mathbf z_n$ 样本：

$$
z_{nj}^{(l)}=\mu_j(\mathbf x_n,\boldsymbol\phi)\epsilon_{nj}^{(l)}+\sigma_j^2(\mathbf x_n,\boldsymbol\phi),\tag{19.18}
$$

**译注：** 式 (19.18) 按原书照录，但与式 (19.17) 不一致。按式 (19.17)，应以标准差乘标准高斯噪声，再加均值，即 $z_{nj}^{(l)}=\sigma_j(\mathbf x_n,\boldsymbol\phi)\epsilon_{nj}^{(l)}+\mu_j(\mathbf x_n,\boldsymbol\phi)$；本章式 (19.19) 后也恢复了这一写法。原式不能直接用于实现重参数化抽样。

其中 $l=1,\ldots,L$ 为样本索引。这使对 $\boldsymbol\phi$ 的依赖显式化，从而能计算对 $\boldsymbol\phi$ 的梯度，如图 19.11 所示。重参数化技巧可推广到其他分布，但仅限连续变量。也有不使用该技巧、直接求梯度的方法（Williams，1992），但估计量方差很高；因此，重参数化也可看作一种方差缩减技术。

根据上述特定建模假设，VAE 的完整误差函数为

$$
\mathcal L=\sum_n\left\{\frac12\sum_{j=1}^{M}\bigl(1+\ln\sigma_{nj}^2-\mu_{nj}^2-\sigma_{nj}^2\bigr)+\frac1L\sum_{l=1}^{L}\ln p(\mathbf x_n\mid\mathbf z_n^{(l)},\mathbf w)\right\}.\tag{19.19}
$$

<!-- pdf-page: 587 -->

其中 $\mathbf z_n^{(l)}$ 的分量为 $z_{nj}^{(l)}=\sigma_{nj}\epsilon^{(l)}+\mu_{nj}$，$\mu_{nj}=\mu_j(\mathbf x_n,\boldsymbol\phi)$，$\sigma_{nj}=\sigma_j(\mathbf x_n,\boldsymbol\phi)$；式 (19.19) 对 $n$ 的求和遍及一个小批量中的数据点。每个数据点 $\mathbf x_n$ 的样本数 $L$ 通常设为 1，即只用一个样本。虽然这给出有噪声的下界估计，但它本就是随机梯度优化步骤的一部分，而该步骤也带有噪声，总体上反而使优化更高效。

<figure id="fig-19-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-19/fig-19-11.png" alt="重参数化用独立随机变量 epsilon 计算潜变量样本，使梯度能穿过编码器">
  <figcaption>图 19.11：重参数化技巧把直接抽取的 $\mathbf z$ 样本，换成由独立随机变量 $\epsilon$ 的样本计算得到的值，使误差信号可以反向传播到编码器网络。所得模型可通过基于梯度的优化，同时学习编码器与解码器网络的参数。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf x$ 为输入，$\boldsymbol\phi$ 为编码器参数，$\mu_i,\sigma_i^2$ 为均值和方差输出，$\epsilon$ 为独立噪声，$\mathbf z$ 为计算所得的潜变量，$\mathbf w$ 为解码器参数，$p(\mathbf x\mid\mathbf z,\mathbf w)$ 为条件分布；红箭头表示可贯通编码器的误差反向传播。</p>
</figure>

可将 VAE 训练概括如下。对于小批量中的每个数据点，先通过编码器网络前向传播，求出近似潜变量分布的均值和方差；再用重参数化技巧从该分布抽样；最后把样本送入解码器网络，计算 ELBO (19.19)。随后用自动微分计算对 $\mathbf w$ 和 $\boldsymbol\phi$ 的梯度。算法 19.1 概述了 VAE 训练；为清晰起见，算法省略了通常使用小批量这一点。模型训练后，丢弃编码器网络，从先验 $p(\mathbf z)$ 抽样并经解码器网络前向传播，生成数据空间中的新样本。

训练后，可能还想评估模型对新测试点 $\widehat{\mathbf x}$ 的表示效果。由于对数似然无法直接计算，可用下界 $\mathcal L$ 近似。估计时可以从 $q(\mathbf z\mid\widehat{\mathbf x},\boldsymbol\phi)$ 抽样，因为这比从 $p(\mathbf z)$ 抽样更准确。

VAE 有许多变体。用于图像数据时，编码器通常基于卷积，解码器基于转置卷积（见第 10.5.3 节）。在**条件 VAE** 中，编码器和解码器都以条件变量 $c$ 为额外输入。例如，要生成物体图像时，$c$ 可表示物体类别。潜空间先验 $p(\mathbf z)$ 仍可取简单高斯，也可扩展为由另一神经网络给出的条件分布 $p(\mathbf z\mid c)$。训练与测试过程与前面相同。

注意，ELBO (19.14) 的第一项鼓励编码器分布 $q(\mathbf z\mid\mathbf x,\boldsymbol\phi)$ 接近先验 $p(\mathbf z)$，因此训练好的模型从 $p(\mathbf z)$ 抽样进行生成时，解码器倾向于产生逼真的输出。训练 VAE 时，变分分布 $q(\mathbf z\mid\mathbf x,\boldsymbol\phi)$ 可能收敛到先验分布 $p(\mathbf z)$，从而不再依赖 $\mathbf x$，失去信息。此时潜编码实际上被忽

<!-- pdf-page: 588 -->
<!-- join-previous-paragraph -->

略。这称为**后验坍缩**。它的一个症状是：输入经过编码再解码，所得重建效果差、看起来模糊。此时 KL 散度 $\operatorname{KL}(q(\mathbf z\mid\mathbf x,\boldsymbol\phi)\parallel p(\mathbf z))$ 接近零。

**译注：** 上段按原书写“第一项”，但式 (19.14) 右边第一项是重建期望；鼓励 $q$ 接近先验的是第二项中的 KL 惩罚。

**算法 19.1：变分自编码器训练**

```text
输入：训练数据集
  D = {x_1,...,x_N}
  编码器网络
  {μ_j(x_n,φ), σ_j²(x_n,φ)}
  j∈{1,...,M}
  解码器网络 g(z,w)
  初始权重向量 w、φ
  学习率 η
输出：最终权重向量 w、φ
重复：
  ℒ ← 0
  对 j∈{1,...,M}：
    ε_nj ∼ N(0,1)
    z_nj ← μ_j(x_n,φ) ε_nj
           + σ_j²(x_n,φ)
    ℒ ← ℒ + 1/2 {
      1 + ln σ_nj²
      − μ_nj² − σ_nj²}
  结束循环
  ℒ ← ℒ + ln p(x_n|z_n,w)
  w ← w + η ∇_w ℒ
  // 更新解码器权重
  φ ← φ + η ∇_φ ℒ
  // 更新编码器权重
直到收敛
返回 w、φ
```

**译注：** 算法 19.1 的 $z_{nj}$ 更新式与原书式 (19.18) 相同，仍把均值乘噪声、再加方差；正确采样关系见式 (19.17) 和上文译注。原算法也未显式写出选择数据点索引 $n$ 或遍历小批量的步骤，不能原样作为完整程序运行。

另一个问题出现在潜编码没有被压缩时：重建结果高度准确，但从 $p(\mathbf z)$ 抽样、经解码器生成的输出质量很差，不像训练数据。此时 KL 散度相对较大。训练后的系统的变分分布与先验差别很大，因此从先验抽样无法生成逼真的输出。

可在式 (19.14) 第一项前引入系数 $\beta$，控制 KL 散度的正则化作用，以处理这两个问题；通常 $\beta>1$（Higgins 等，2017）。若重建结果差，可以增大 $\beta$；若生成样本差，可以减小 $\beta$。$\beta$ 也可按退火计划变化：从较小值开始，在训练过程中逐渐增大。

**译注：** 原书称在式 (19.14)“第一项”前加 $\beta$ 控制 KL，但 KL 是右边第二项。若使用常见的“重建期望 $-\beta\operatorname{KL}$”目标，增大 $\beta$ 会增强靠近先验的约束，可能改善从先验采样的质量，却常以重建质量为代价；原书给出的两种调参方向与这一直接权衡相反。

最后要注意，前面考虑的解码器网络 $\mathbf g(\mathbf z,\mathbf w)$ 表示

<!-- pdf-page: 589 -->
<!-- join-previous-paragraph -->

高斯输出分布的均值。可以扩展 VAE，使输出也表示高斯分布的方差，或更一般地，表示刻画其他复杂分布的参数（见第 6.5 节）。

## 习题

**19.1（★★）** 证明对于任何分布 $q(\mathbf z\mid\boldsymbol\phi)$ 和任何函数 $G(\mathbf z)$，都有

$$
\nabla_{\boldsymbol\phi}\int q(\mathbf z\mid\boldsymbol\phi)G(\mathbf z)\,\mathrm d\mathbf z=\int q(\mathbf z\mid\boldsymbol\phi)G(\mathbf z)\nabla_{\boldsymbol\phi}\ln q(\mathbf z\mid\boldsymbol\phi)\,\mathrm d\mathbf z.\tag{19.20}
$$

由此证明，式 (19.20) 左边可用以下蒙特卡洛估计量近似：

$$
\nabla_{\boldsymbol\phi}\int q(\mathbf z\mid\boldsymbol\phi)G(\mathbf z)\,\mathrm d\mathbf z\simeq\sum_i G(\mathbf z^{(i)})\nabla_{\boldsymbol\phi}\ln q(\mathbf z^{(i)}\mid\boldsymbol\phi),\tag{19.21}
$$

其中样本 $\{\mathbf z^{(i)}\}$ 从分布 $q(\mathbf z\mid\boldsymbol\phi)$ 独立抽取。验证该估计量是无偏的，即式 (19.21) 右边对样本分布求得的平均值等于左边。原则上，令 $G(\mathbf z)=p(\mathbf x\mid\mathbf z,\mathbf w)$，这一结果就能不使用重参数化技巧，求式 (19.14) 右边第二项对 $\boldsymbol\phi$ 的梯度。由于该方法无偏，样本数趋于无穷时也会得到精确结果。但重参数化技巧效率更高，即达到良好精度所需的样本更少，因为它直接计算由 $\boldsymbol\phi$ 的变化引起的 $\mathbf z$ 变化，进而造成 $p(\mathbf x\mid\mathbf z,\mathbf w)$ 的变化。

**译注：** 原书式 (19.21) 的样本和未除以样本数，一般不能作为题面所说的无偏**平均值**估计量。题末令 $G=p(\mathbf x\mid\mathbf z,\mathbf w)$，未取对数；式 (19.14) 中相应的对数似然是右边**第一项**，而非原书所说的“第二项”。这些疑点均保留原题措辞。

**19.2（★）** 验证：若 $\epsilon$ 服从零均值、单位方差的高斯分布，则式 (19.17) 的变量 $z$ 服从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布。

**19.3（★★）** 本题把具有对角协方差的 VAE 编码器网络 (19.13) 扩展为一般协方差矩阵。考虑从简单高斯分布抽取的 $K$ 维随机向量：

$$
\boldsymbol\epsilon\sim\mathcal N(\mathbf z\mid\mathbf 0,\mathbf I),\tag{19.22}
$$

再按下式线性变换：

$$
\mathbf z=\boldsymbol\mu+\mathbf L\boldsymbol\epsilon,\tag{19.23}
$$

其中 $\mathbf L$ 为下三角矩阵，即一个主对角线以上元素全为零的 $K\times K$ 矩阵。证明 $\mathbf z$ 服从 $\mathcal N(\mathbf z\mid\boldsymbol\mu,\boldsymbol\Sigma)$，写出 $\boldsymbol\Sigma$ 关于 $\mathbf L$ 的表达式。解释为什么 $\mathbf L$ 的对角元素必须非负。说明如何用神经网络的输出表示 $\boldsymbol\mu$ 和 $\mathbf L$，并讨论适合的输出单元激活函数。

**译注：** 原书式 (19.22) 左边为随机向量 $\boldsymbol\epsilon$，右边高斯密度的自变量却为 $\mathbf z$；按上下文应为 $\boldsymbol\epsilon$。另外，$\boldsymbol\Sigma=\mathbf L\mathbf L^{\mathsf T}$ 本身不要求 $\mathbf L$ 的对角元素非负；取非负对角线是选用 Cholesky 因子等规范表示时的约束。原题要求照录。

<!-- pdf-page: 590 -->

**19.4（★★）** 计算式 (19.14) 的 KL 散度项，进而说明如何求该项对 $\mathbf w$ 和 $\boldsymbol\phi$ 的梯度，以训练编码器与解码器网络。

**译注：** 该 KL 项只依赖编码器参数 $\boldsymbol\phi$ 和先验，不依赖解码器参数 $\mathbf w$，因此它对 $\mathbf w$ 的梯度为零；原题仍同时要求对两组参数求梯度。

**19.5（★）** 前面看到，式 (19.11) 的 ELBO 可写为式 (19.14) 的形式。证明它也可写为

$$
\begin{aligned}\mathcal L_n(\mathbf w,\boldsymbol\phi)&=\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln\{p(\mathbf x_n\mid\mathbf z_n,\mathbf w)p(\mathbf z_n)\}\,\mathrm d\mathbf z_n\\&\quad-\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\,\mathrm d\mathbf z_n.\end{aligned}\tag{19.24}
$$

**19.6（★）** 证明式 (19.11) 的 ELBO 可写为

$$
\begin{aligned}\mathcal L_n(\mathbf w,\boldsymbol\phi)&=\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln p(\mathbf z_n)\,\mathrm d\mathbf z_n\\&\quad+\int q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)\ln\left\{\frac{p(\mathbf x_n\mid\mathbf z_n,\mathbf w)}{q(\mathbf z_n\mid\mathbf x_n,\boldsymbol\phi)}\right\}\,\mathrm d\mathbf z_n.\end{aligned}\tag{19.25}
$$
