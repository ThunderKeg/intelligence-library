# 第 6 章 核方法

<aside class="chapter-guide"><strong>本章导读</strong><p>本章说明如何用核函数表达数据之间的关系，并在不显式计算高维特征的情况下建立预测模型。先从线性回归的对偶表示引出核，再介绍有效核的构造方法和径向基函数网络，最后用高斯过程把核与函数的概率分布联系起来，讨论回归、分类及超参数学习。</p></aside>

<!-- pdf-page: 311 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/a-chapter-opening.png" alt="水面纹理上的第 6 章标题"><p class="figure-translation">Kernel Methods → 核方法。</p></figure>

在第 3 章和第 4 章中，我们考察了用于回归与分类的线性参数模型。在这些模型中，从输入 $\mathbf{x}$ 到输出 $y$ 的映射 $y(\mathbf{x},\mathbf{w})$ 的形式，由可自适应参数向量 $\mathbf{w}$ 控制。在学习阶段，使用一组训练数据来获得参数向量的点估计，或者确定这个向量的后验分布。随后丢弃训练数据，对新输入的预测完全基于学到的参数向量 $\mathbf{w}$。神经网络等非线性参数模型也采用这种方式。<span class="margin-reference">第 5 章</span>

不过，还有一类模式识别方法，会保留训练数据点或其中的一个子集，并在预测阶段继续使用。例如，Parzen 概率密度模型由“核”函数的线性组合构成，每个核函数都以一个训练数据点为中心。<span class="margin-reference">第 2.5.1 节</span>类似地，在第 2.5.2 节，我们介绍了一种称为最近邻的简单分类方法，它为每个新的测试向量赋予与训练集中

<!-- pdf-page: 312 -->
<!-- join-previous-paragraph -->
最近的样例相同的标记。这些都是基于记忆的方法（memory-based methods）的例子：存储整个训练集，以便对未来的数据点作出预测。它们通常需要定义一种度量，用来衡量输入空间中任意两个向量的相似程度；一般“训练”很快，但对测试数据点进行预测较慢。

许多线性参数模型都可以改写为等价的“对偶表示”（dual representation），其中预测同样基于核函数在训练数据点处取值的线性组合。我们将看到，对于基于固定非线性特征空间映射 $\boldsymbol{\phi}(\mathbf{x})$ 的模型，核函数由以下关系给出：

$$
k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}').
\tag{6.1}
$$

由这个定义可知，核是其两个自变量的对称函数，即 $k(\mathbf{x},\mathbf{x}')=k(\mathbf{x}',\mathbf{x})$。Aizerman et al.（1964）在势函数方法的背景下，将核的概念引入模式识别领域；势函数的名称来自与静电学的类比。虽然这一概念被忽视了很多年，Boser et al.（1992）又在大间隔分类器的背景下将它重新引入机器学习，由此产生了支持向量机技术。<span class="margin-reference">第 7 章</span>此后，这一主题在理论和应用两方面都引起了广泛兴趣。其中最重要的进展之一，是将核扩展到符号对象的处理，从而大大扩大了可以解决的问题范围。

最简单的核函数例子，是在式（6.1）中对特征空间采用恒等映射，即 $\boldsymbol{\phi}(\mathbf{x})=\mathbf{x}$，此时 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$。我们将其称为线性核（linear kernel）。

把核表述为特征空间中的内积，使我们能够利用核技巧（kernel trick），也称为核替换（kernel substitution），为许多熟知的算法构造有意义的扩展。其基本思想是：如果某个算法的表达方式使输入向量 $\mathbf{x}$ 只以标量积的形式出现，那么就可以用其他核来替换这个标量积。例如，核替换技术可以用于主成分分析，从而得到 PCA 的非线性版本（Schölkopf et al., 1998）。<span class="margin-reference">第 12.3 节</span>核替换的其他例子包括最近邻分类器和核 Fisher 判别方法（Mika et al., 1999；Roth and Steinhage, 2000；Baudat and Anouar, 2000）。

常用的核函数形式很多，本章将介绍其中的若干例子。许多核只依赖于两个自变量之差，即 $k(\mathbf{x},\mathbf{x}')=k(\mathbf{x}-\mathbf{x}')$；它们称为平稳核（stationary kernels），因为它们在输入空间的平移下保持不变。进一步的特殊情形是齐次核（homogeneous kernels），也称为径向基函数（radial basis functions），它们只依赖于两个自变量之间距离的大小，通常采用欧氏距离，即 $k(\mathbf{x},\mathbf{x}')=k(\|\mathbf{x}-\mathbf{x}'\|)$。<span class="margin-reference">第 6.3 节</span>

关于核方法的近期教材，可参见 Schölkopf and Smola（2002）、Herbrich（2002）以及 Shawe-Taylor and Cristianini（2004）。

<!-- pdf-page: 313 -->

## 6.1 对偶表示

许多用于回归与分类的线性模型，都可以改写成对偶表示，核函数会在其中自然出现。下一章讨论支持向量机时，这一概念将发挥重要作用。这里考虑一个线性回归模型，其参数通过最小化以下带正则化的平方和误差函数来确定：

$$
J(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)-t_n\}^2+\frac{\lambda}{2}\mathbf{w}^{\mathrm{T}}\mathbf{w}
\tag{6.2}
$$

其中 $\lambda\geqslant0$。如果令 $J(\mathbf{w})$ 对 $\mathbf{w}$ 的梯度等于零，可以看到，$\mathbf{w}$ 的解具有向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 的线性组合形式，其系数是 $\mathbf{w}$ 的函数，即

$$
\mathbf{w}=-\frac{1}{\lambda}\sum_{n=1}^{N}\{\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)-t_n\}\boldsymbol{\phi}(\mathbf{x}_n)=\sum_{n=1}^{N}a_n\boldsymbol{\phi}(\mathbf{x}_n)=\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{a}
\tag{6.3}
$$

其中 $\boldsymbol{\Phi}$ 是设计矩阵，其第 $n$ 行为 $\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}$。这里，向量 $\mathbf{a}=(a_1,\ldots,a_N)^{\mathrm{T}}$，并定义

$$
a_n=-\frac{1}{\lambda}\{\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)-t_n\}.
\tag{6.4}
$$

现在，我们可以用参数向量 $\mathbf{a}$ 重新表述最小二乘算法，而不再使用参数向量 $\mathbf{w}$，由此得到对偶表示。将 $\mathbf{w}=\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{a}$ 代入 $J(\mathbf{w})$，得到

$$
J(\mathbf{a})=\frac{1}{2}\mathbf{a}^{\mathrm{T}}\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{a}-\mathbf{a}^{\mathrm{T}}\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}\boldsymbol{\mathsf{t}}+\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm{T}}\boldsymbol{\mathsf{t}}+\frac{\lambda}{2}\mathbf{a}^{\mathrm{T}}\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}\mathbf{a}
\tag{6.5}
$$

其中 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm{T}}$。现在定义 Gram 矩阵 $\mathbf{K}=\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}$，它是一个 $N\times N$ 对称矩阵，元素为

$$
K_{nm}=\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)=k(\mathbf{x}_n,\mathbf{x}_m)
\tag{6.6}
$$

这里引入了式（6.1）定义的核函数 $k(\mathbf{x},\mathbf{x}')$。用 Gram 矩阵，可以将平方和误差函数写为

$$
J(\mathbf{a})=\frac{1}{2}\mathbf{a}^{\mathrm{T}}\mathbf{K}\mathbf{K}\mathbf{a}-\mathbf{a}^{\mathrm{T}}\mathbf{K}\boldsymbol{\mathsf{t}}+\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm{T}}\boldsymbol{\mathsf{t}}+\frac{\lambda}{2}\mathbf{a}^{\mathrm{T}}\mathbf{K}\mathbf{a}.
\tag{6.7}
$$

令 $J(\mathbf{a})$ 对 $\mathbf{a}$ 的梯度为零，得到如下解：

$$
\mathbf{a}=(\mathbf{K}+\lambda\mathbf{I}_N)^{-1}\boldsymbol{\mathsf{t}}.
\tag{6.8}
$$

<!-- pdf-page: 314 -->

把它代回线性回归模型，得到对新输入 $\mathbf{x}$ 的如下预测：

$$
y(\mathbf{x})=\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x})=\mathbf{a}^{\mathrm{T}}\boldsymbol{\Phi}\boldsymbol{\phi}(\mathbf{x})=\mathbf{k}(\mathbf{x})^{\mathrm{T}}(\mathbf{K}+\lambda\mathbf{I}_N)^{-1}\boldsymbol{\mathsf{t}}
\tag{6.9}
$$

其中定义了向量 $\mathbf{k}(\mathbf{x})$，其元素为 $k_n(\mathbf{x})=k(\mathbf{x}_n,\mathbf{x})$。由此可见，对偶形式允许我们完全用核函数 $k(\mathbf{x},\mathbf{x}')$ 表示最小二乘问题的解。之所以称为对偶形式，是因为注意到 $\mathbf{a}$ 的解可表示为 $\boldsymbol{\phi}(\mathbf{x})$ 各元素的线性组合后，就可以恢复用参数向量 $\mathbf{w}$ 表示的原始形式。<span class="margin-reference">习题 6.1</span>注意，在 $\mathbf{x}$ 处的预测由训练集目标值的线性组合给出。事实上，我们已经在第 3.3.3 节使用略有不同的记号得到了这一结果。

在对偶形式中，我们通过对一个 $N\times N$ 矩阵求逆来确定参数向量 $\mathbf{a}$；而在原来的参数空间形式中，需要对一个 $M\times M$ 矩阵求逆来确定 $\mathbf{w}$。由于 $N$ 通常远大于 $M$，对偶形式看起来并没有特别大的用处。然而，我们将看到，对偶形式的优点是它完全以核函数 $k(\mathbf{x},\mathbf{x}')$ 表示。因此可以直接使用核，避免显式引入特征向量 $\boldsymbol{\phi}(\mathbf{x})$，从而隐式使用高维甚至无限维的特征空间。

存在基于 Gram 矩阵的对偶表示，是许多线性模型的一个性质，包括感知机。<span class="margin-reference">习题 6.2</span>在第 6.4 节，我们将建立用于回归的概率线性模型与高斯过程方法之间的对偶关系。第 7 章讨论支持向量机时，对偶性也将发挥重要作用。

## 6.2 核的构造

为了利用核替换，我们需要能够构造有效的核函数。一种方法是选择特征空间映射 $\boldsymbol{\phi}(\mathbf{x})$，再用它求出相应的核，如图 6.1 所示。这里，对一维输入空间，核函数定义为

$$
k(x,x')=\boldsymbol{\phi}(x)^{\mathrm{T}}\boldsymbol{\phi}(x')=\sum_{i=1}^{M}\phi_i(x)\phi_i(x')
\tag{6.10}
$$

其中 $\phi_i(x)$ 是基函数。

另一种方法是直接构造核函数。在这种情况下，必须保证所选函数是有效的核，换言之，它对应于某个特征空间中的标量积，这个特征空间可能是无限维的。作为一个简单例子，考虑如下核函数：

$$
k(\mathbf{x},\mathbf{z})=(\mathbf{x}^{\mathrm{T}}\mathbf{z})^2.
\tag{6.11}
$$

<!-- pdf-page: 315 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/a-fig-6-1.png" alt="多项式、高斯和 logistic sigmoid 基函数及各自对应的核函数，六个分图"><figcaption>图 6.1：从相应的一组基函数出发构造核函数的示意图。每一列下方的图，表示式（6.10）定义的核函数 $k(x,x')$ 在 $x'=0$ 时随 $x$ 的变化；上方的图表示相应的基函数，依次为多项式（左列）、“高斯”函数（中列）以及 logistic sigmoid 函数（右列）。</figcaption></figure>

如果取二维输入空间 $\mathbf{x}=(x_1,x_2)$ 这一具体情形，就可以展开各项，从而识别出相应的非线性特征映射：

$$
\begin{aligned}
k(\mathbf{x},\mathbf{z})&=(\mathbf{x}^{\mathrm{T}}\mathbf{z})^2=(x_1z_1+x_2z_2)^2\\
&=x_1^2z_1^2+2x_1z_1x_2z_2+x_2^2z_2^2\\
&=(x_1^2,\sqrt{2}x_1x_2,x_2^2)(z_1^2,\sqrt{2}z_1z_2,z_2^2)^{\mathrm{T}}\\
&=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{z}).
\end{aligned}
\tag{6.12}
$$

可以看到，特征映射的形式为 $\boldsymbol{\phi}(\mathbf{x})=(x_1^2,\sqrt{2}x_1x_2,x_2^2)^{\mathrm{T}}$，因此它包含所有可能的二次项，并在这些项之间采用特定的权重。

不过，更一般地，我们需要一种简单方法，在不显式构造函数 $\boldsymbol{\phi}(\mathbf{x})$ 的情况下，检验一个函数是否构成有效的核。函数 $k(\mathbf{x},\mathbf{x}')$ 是有效核的充要条件（Shawe-Taylor and Cristianini, 2004）是：对于集合 $\{\mathbf{x}_n\}$ 的所有可能选择，以 $k(\mathbf{x}_n,\mathbf{x}_m)$ 为元素的 Gram 矩阵 $\mathbf{K}$ 都应当半正定。注意，半正定矩阵与所有元素都非负的矩阵并不是一回事。<span class="margin-reference">附录 C</span>

构造新核的一种强有力的方法，是把较简单的核作为组成部分来组合。可以利用以下性质来实现：

<!-- pdf-page: 316 -->

<aside class="procedure"><h3>构造新核的方法</h3><p>给定有效核 $k_1(\mathbf{x},\mathbf{x}')$ 和 $k_2(\mathbf{x},\mathbf{x}')$，以下新核也都是有效的：</p><p>$$k(\mathbf{x},\mathbf{x}')=c k_1(\mathbf{x},\mathbf{x}')\tag{6.13}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=f(\mathbf{x})k_1(\mathbf{x},\mathbf{x}')f(\mathbf{x}')\tag{6.14}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=q\left(k_1(\mathbf{x},\mathbf{x}')\right)\tag{6.15}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=\exp\left(k_1(\mathbf{x},\mathbf{x}')\right)\tag{6.16}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=k_1(\mathbf{x},\mathbf{x}')+k_2(\mathbf{x},\mathbf{x}')\tag{6.17}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=k_1(\mathbf{x},\mathbf{x}')k_2(\mathbf{x},\mathbf{x}')\tag{6.18}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=k_3\left(\boldsymbol{\phi}(\mathbf{x}),\boldsymbol{\phi}(\mathbf{x}')\right)\tag{6.19}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{x}'\tag{6.20}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=k_a(\mathbf{x}_a,\mathbf{x}'_a)+k_b(\mathbf{x}_b,\mathbf{x}'_b)\tag{6.21}$$</p><p>$$k(\mathbf{x},\mathbf{x}')=k_a(\mathbf{x}_a,\mathbf{x}'_a)k_b(\mathbf{x}_b,\mathbf{x}'_b)\tag{6.22}$$</p><p>其中 $c>0$ 是常数，$f(\cdot)$ 是任意函数，$q(\cdot)$ 是系数非负的多项式，$\boldsymbol{\phi}(\mathbf{x})$ 是从 $\mathbf{x}$ 到 $\mathbb{R}^M$ 的函数，$k_3(\cdot,\cdot)$ 是 $\mathbb{R}^M$ 中的有效核，$\mathbf{A}$ 是对称半正定矩阵，$\mathbf{x}_a$ 和 $\mathbf{x}_b$ 是两组不必互不相交的变量，满足 $\mathbf{x}=(\mathbf{x}_a,\mathbf{x}_b)$，而 $k_a$ 和 $k_b$ 是各自空间上的有效核函数。</p></aside>

有了这些性质，我们就可以开始构造适合特定应用的更复杂的核。我们要求核 $k(\mathbf{x},\mathbf{x}')$ 对称且半正定，并且根据预定应用，表达 $\mathbf{x}$ 与 $\mathbf{x}'$ 之间恰当形式的相似性。这里考察几个常见的核函数例子。关于“核工程”更广泛的讨论，可参见 Shawe-Taylor and Cristianini（2004）。

我们已经看到，简单的多项式核 $k(\mathbf{x},\mathbf{x}')=(\mathbf{x}^{\mathrm{T}}\mathbf{x}')^2$ 只包含二次项。如果考虑略作推广的核 $k(\mathbf{x},\mathbf{x}')=(\mathbf{x}^{\mathrm{T}}\mathbf{x}'+c)^2$，其中 $c>0$，那么相应的特征映射 $\boldsymbol{\phi}(\mathbf{x})$ 除了包含二次项，还包含常数项和线性项。类似地，$k(\mathbf{x},\mathbf{x}')=(\mathbf{x}^{\mathrm{T}}\mathbf{x}')^M$ 包含所有 $M$ 次单项式。例如，如果 $\mathbf{x}$ 和 $\mathbf{x}'$ 是两幅图像，那么这个核表示第一幅图像中 $M$ 个像素与第二幅图像中 $M$ 个像素的所有可能乘积的某种特定加权和。同样，考虑 $k(\mathbf{x},\mathbf{x}')=(\mathbf{x}^{\mathrm{T}}\mathbf{x}'+c)^M$，其中 $c>0$，就能将其推广为包含所有不超过 $M$ 次的项。利用组合核的式（6.17）和式（6.18），可以看到这些都是有效的核函数。

另一种常用核的形式为

$$
k(\mathbf{x},\mathbf{x}')=\exp\left(-\|\mathbf{x}-\mathbf{x}'\|^2/2\sigma^2\right)
\tag{6.23}
$$

它常被称为“高斯”核。不过要注意，在这里它并不被解释为概率密度，因此归一化系数被

<!-- pdf-page: 317 -->
<!-- join-previous-paragraph -->
省略。要看出这是一个有效核，可以展开平方项

$$
\|\mathbf{x}-\mathbf{x}'\|^2=\mathbf{x}^{\mathrm{T}}\mathbf{x}+(\mathbf{x}')^{\mathrm{T}}\mathbf{x}'-2\mathbf{x}^{\mathrm{T}}\mathbf{x}'
\tag{6.24}
$$

得到

$$
k(\mathbf{x},\mathbf{x}')=\exp(-\mathbf{x}^{\mathrm{T}}\mathbf{x}/2\sigma^2)\exp(\mathbf{x}^{\mathrm{T}}\mathbf{x}'/\sigma^2)\exp(-(\mathbf{x}')^{\mathrm{T}}\mathbf{x}'/2\sigma^2)
\tag{6.25}
$$

再结合线性核 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$ 的有效性，利用式（6.14）和式（6.16）即可。注意，与高斯核对应的特征向量是无限维的。<span class="margin-reference">习题 6.11</span>

高斯核并不局限于使用欧氏距离。如果在式（6.24）中使用核替换，将 $\mathbf{x}^{\mathrm{T}}\mathbf{x}'$ 替换为非线性核 $\kappa(\mathbf{x},\mathbf{x}')$，就得到

$$
k(\mathbf{x},\mathbf{x}')=\exp\left\{-\frac{1}{2\sigma^2}\left(\kappa(\mathbf{x},\mathbf{x})+\kappa(\mathbf{x}',\mathbf{x}')-2\kappa(\mathbf{x},\mathbf{x}')\right)\right\}.
\tag{6.26}
$$

核的观点带来的一项重要贡献，是将输入扩展到符号对象，而不只是实数向量。核函数可以定义在图、集合、字符串和文本文档等多种对象上。例如，考虑一个固定集合，并定义由这个集合所有可能子集组成的非向量空间。如果 $A_1$ 和 $A_2$ 是其中两个子集，那么核的一种简单选择是

$$
k(A_1,A_2)=2^{|A_1\cap A_2|}
\tag{6.27}
$$

其中 $A_1\cap A_2$ 表示集合 $A_1$ 与 $A_2$ 的交集，$|A|$ 表示 $A$ 中子集的数量。这是有效的核函数，因为可以证明它对应于某个特征空间中的内积。<span class="margin-reference">习题 6.12</span>

一种很有力的核构造方法，是从概率生成式模型出发（Haussler, 1999），从而在判别式框架中使用生成式模型。生成式模型能自然地处理缺失数据，隐马尔可夫模型还可以处理长度不同的序列。相比之下，在判别任务中，判别式模型通常比生成式模型表现更好。因此，将这两类方法结合起来很值得研究（Lasserre et al., 2006）。一种结合方式是用生成式模型定义核，再将这个核用于判别式方法。

给定生成式模型 $p(\mathbf{x})$，可以定义核

$$
k(\mathbf{x},\mathbf{x}')=p(\mathbf{x})p(\mathbf{x}').
\tag{6.28}
$$

显然，这是一个有效核函数，因为它可以解释为映射 $p(\mathbf{x})$ 所定义的一维特征空间中的内积。它表示，如果两个输入 $\mathbf{x}$ 和 $\mathbf{x}'$ 都具有较高的概率，那么它们就是相似的。可以利用式（6.13）和式（6.17）扩展这类核：对不同概率分布的乘积求和，并采用正的加权系数 $p(i)$，形式为

$$
k(\mathbf{x},\mathbf{x}')=\sum_i p(\mathbf{x}\mid i)p(\mathbf{x}'\mid i)p(i).
\tag{6.29}
$$

<!-- pdf-page: 318 -->

除相差一个整体乘法常数外，这等价于一个各分量可分解的混合分布，其中下标 $i$ 起着“潜”变量的作用。<span class="margin-reference">第 9.2 节</span>如果两个输入 $\mathbf{x}$ 和 $\mathbf{x}'$ 在多个不同分量下都具有可观的概率，那么它们会给出较大的核函数值，因而显得相似。取无限求和的极限，还可以考虑如下形式的核：

$$
k(\mathbf{x},\mathbf{x}')=\int p(\mathbf{x}\mid\mathbf{z})p(\mathbf{x}'\mid\mathbf{z})p(\mathbf{z})\,\mathrm{d}\mathbf{z}
\tag{6.30}
$$

其中 $\mathbf{z}$ 是连续潜变量。

现在假设数据由长度为 $L$ 的有序序列构成，因此一个观测记为 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_L\}$。一种常用的序列生成式模型是隐马尔可夫模型，它通过对相应的隐藏状态序列 $\mathbf{Z}=\{\mathbf{z}_1,\ldots,\mathbf{z}_L\}$ 进行边缘化来表示分布 $p(\mathbf{X})$。<span class="margin-reference">第 13.2 节</span>我们可以利用这一方法，扩展混合表示（6.29），定义一个度量两个序列 $\mathbf{X}$ 和 $\mathbf{X}'$ 相似性的核函数：

$$
k(\mathbf{X},\mathbf{X}')=\sum_{\mathbf{Z}}p(\mathbf{X}\mid\mathbf{Z})p(\mathbf{X}'\mid\mathbf{Z})p(\mathbf{Z})
\tag{6.31}
$$

这样，两个观测序列都由同一个隐藏序列 $\mathbf{Z}$ 生成。这个模型很容易扩展，以便比较不同长度的序列。

利用生成式模型定义核函数的另一种方法，称为 Fisher 核（Jaakkola and Haussler, 1999）。考虑参数化生成式模型 $p(\mathbf{x}\mid\boldsymbol{\theta})$，其中 $\boldsymbol{\theta}$ 表示参数向量。目标是找到一个核，度量生成式模型所诱导的两个输入向量 $\mathbf{x}$ 与 $\mathbf{x}'$ 之间的相似性。Jaakkola and Haussler（1999）考虑对 $\boldsymbol{\theta}$ 的梯度，它在一个与 $\boldsymbol{\theta}$ 维数相同的“特征”空间中定义了一个向量。具体来说，他们考虑 Fisher 得分（Fisher score）

$$
\mathbf{g}(\boldsymbol{\theta},\mathbf{x})=\nabla_{\boldsymbol{\theta}}\ln p(\mathbf{x}\mid\boldsymbol{\theta})
\tag{6.32}
$$

由此定义 Fisher 核

$$
k(\mathbf{x},\mathbf{x}')=\mathbf{g}(\boldsymbol{\theta},\mathbf{x})^{\mathrm{T}}\mathbf{F}^{-1}\mathbf{g}(\boldsymbol{\theta},\mathbf{x}').
\tag{6.33}
$$

这里 $\mathbf{F}$ 是 Fisher 信息矩阵，由下式给出：

$$
\mathbf{F}=\mathbb{E}_{\mathbf{x}}\left[\mathbf{g}(\boldsymbol{\theta},\mathbf{x})\mathbf{g}(\boldsymbol{\theta},\mathbf{x})^{\mathrm{T}}\right]
\tag{6.34}
$$

其中，期望是关于服从分布 $p(\mathbf{x}\mid\boldsymbol{\theta})$ 的 $\mathbf{x}$ 取的。这一构造可以从信息几何（information geometry）的角度得到解释；信息几何研究模型参数空间的微分几何（Amari, 1998）。这里仅指出，由于包含 Fisher 信息矩阵，这个核在密度模型的非线性重参数化 $\boldsymbol{\theta}\to\boldsymbol{\psi}(\boldsymbol{\theta})$ 下保持不变。<span class="margin-reference">习题 6.13</span>

在实践中，往往无法计算 Fisher 信息矩阵。一种方法是直接用样本平均替代 Fisher 信息定义中的期望，得到

$$
\mathbf{F}\simeq\frac{1}{N}\sum_{n=1}^{N}\mathbf{g}(\boldsymbol{\theta},\mathbf{x}_n)\mathbf{g}(\boldsymbol{\theta},\mathbf{x}_n)^{\mathrm{T}}.
\tag{6.35}
$$

<!-- pdf-page: 319 -->

这是 Fisher 得分的协方差矩阵，因此 Fisher 核对应于对这些得分进行白化。<span class="margin-reference">第 12.1.3 节</span>更简单的做法，是完全省略 Fisher 信息矩阵，使用不具备这种不变性的核

$$
k(\mathbf{x},\mathbf{x}')=\mathbf{g}(\boldsymbol{\theta},\mathbf{x})^{\mathrm{T}}\mathbf{g}(\boldsymbol{\theta},\mathbf{x}').
\tag{6.36}
$$

Hofmann（2000）给出了 Fisher 核在文档检索中的一个应用。

核函数的最后一个例子是 S 形核，其形式为

$$
k(\mathbf{x},\mathbf{x}')=\tanh(a\mathbf{x}^{\mathrm{T}}\mathbf{x}'+b)
\tag{6.37}
$$

它的 Gram 矩阵一般并非半正定。不过，这种形式的核在实践中也被使用过（Vapnik, 1995），可能是因为它使支持向量机等核展开在表面上类似于神经网络模型。我们将看到，在基函数数量趋于无穷的极限下，采用适当先验的贝叶斯神经网络会化为高斯过程，从而在神经网络与核方法之间建立更深层的联系。<span class="margin-reference">第 6.4.7 节</span>

## 6.3 径向基函数网络

在第 3 章中，我们讨论了基于固定基函数线性组合的回归模型，但没有详细讨论这些基函数可以采用什么形式。一个得到广泛应用的选择是径向基函数，其性质是每个基函数只依赖于到某个中心 $\boldsymbol{\mu}_j$ 的径向距离，通常采用欧氏距离，即 $\phi_j(\mathbf{x})=h(\|\mathbf{x}-\boldsymbol{\mu}_j\|)$。

从历史上看，径向基函数是为精确函数插值而引入的（Powell, 1987）。给定一组输入向量 $\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 及对应的目标值 $\{t_1,\ldots,t_N\}$，目标是找到一个光滑函数 $f(\mathbf{x})$，精确拟合每个目标值，即对 $n=1,\ldots,N$，都有 $f(\mathbf{x}_n)=t_n$。为此，将 $f(\mathbf{x})$ 表示为径向基函数的线性组合，每个数据点都对应一个以它为中心的基函数：

$$
f(\mathbf{x})=\sum_{n=1}^{N}w_nh(\|\mathbf{x}-\mathbf{x}_n\|).
\tag{6.38}
$$

系数 $\{w_n\}$ 的值通过最小二乘法求得；由于系数数量与约束数量相同，所得函数能够精确拟合每个目标值。不过，在模式识别应用中，目标值一般带有噪声，而精确插值并不可取，因为它对应于过拟合的解。

径向基函数展开也出现在正则化理论中（Poggio and Girosi, 1990；Bishop, 1995a）。对于平方和误差函数，如果正则化项用微分算子定义，那么最优解由该算子的格林函数（Green's functions）展开给出；这些函数类似于离散矩阵的特征向量，并且仍然以每个数据

<!-- pdf-page: 320 -->
<!-- join-previous-paragraph -->
点为中心设置一个基函数。如果微分算子具有各向同性，那么格林函数就只依赖于到相应数据点的径向距离。由于存在正则化项，所得解不再精确插值训练数据。

径向基函数的另一个动机，是考察输入变量而非目标变量带有噪声时的插值问题（Webb, 1994；Bishop, 1995a）。如果输入变量 $\mathbf{x}$ 上的噪声由变量 $\boldsymbol{\xi}$ 描述，且其分布为 $\nu(\boldsymbol{\xi})$，那么平方和误差函数变为

$$
E=\frac{1}{2}\sum_{n=1}^{N}\int\{y(\mathbf{x}_n+\boldsymbol{\xi})-t_n\}^2\nu(\boldsymbol{\xi})\,\mathrm{d}\boldsymbol{\xi}.
\tag{6.39}
$$

利用变分法，可以对函数 $f(\mathbf{x})$ 进行优化，得到<span class="margin-reference">附录 D；习题 6.17</span>

$$
y(\mathbf{x}_n)=\sum_{n=1}^{N}t_nh(\mathbf{x}-\mathbf{x}_n)
\tag{6.40}
$$

其中基函数由下式给出：

$$
h(\mathbf{x}-\mathbf{x}_n)=\frac{\nu(\mathbf{x}-\mathbf{x}_n)}{\sum_{n=1}^{N}\nu(\mathbf{x}-\mathbf{x}_n)}.
\tag{6.41}
$$

可以看到，每个数据点都对应一个以它为中心的基函数。这称为 Nadaraya–Watson 模型；第 6.3.1 节将从另一个角度再次推导它。如果噪声分布 $\nu(\boldsymbol{\xi})$ 具有各向同性，即它只依赖于 $\|\boldsymbol{\xi}\|$，那么基函数就是径向的。

注意，基函数（6.41）已经归一化，因此对于任意 $\mathbf{x}$，都有 $\sum_n h(\mathbf{x}-\mathbf{x}_n)=1$。图 6.2 展示了这种归一化的效果。实践中有时会使用归一化，因为它能避免输入空间中出现所有基函数都很小的区域；否则，这些区域内的预测必然也很小，或者完全由偏置参数控制。

归一化径向基函数展开出现的另一种情形，是将核密度估计用于回归问题，第 6.3.1 节将对此进行讨论。

由于每个数据点都对应一个基函数，当预测新数据点时，相应模型的求值可能需要很大计算量。因此，人们提出了一些模型（Broomhead and Lowe, 1988；Moody and Darken, 1989；Poggio and Girosi, 1990），仍然保留径向基函数展开，但基函数数量 $M$ 少于数据点数量 $N$。通常，仅根据输入数据 $\{\mathbf{x}_n\}$ 来确定基函数的数量及中心位置 $\boldsymbol{\mu}_i$。随后固定这些基函数，并按照第 3.1.1 节讨论的方法，通过求解通常的线性方程组，用最小二乘法确定系数 $\{w_i\}$。

<!-- pdf-page: 321 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/a-fig-6-2.png" alt="一组高斯基函数与相应归一化基函数的对比"><figcaption>图 6.2：左图是一组高斯基函数，右图是相应的归一化基函数。</figcaption></figure>

选择基函数中心的最简单方法之一，是从数据点中随机选取一个子集。更系统的方法称为正交最小二乘法（orthogonal least squares）（Chen et al., 1991）。这是一个序贯选择过程：每一步都选择能使平方和误差下降最多的数据点，作为下一个基函数的中心。展开系数的值也在算法过程中确定。人们还使用过 $K$ 均值等聚类算法；这样得到的一组基函数中心不再与训练数据点重合。<span class="margin-reference">第 9.1 节</span>

### 6.3.1 Nadaraya–Watson 模型

在第 3.3.3 节，我们看到，线性回归模型对新输入 $\mathbf{x}$ 的预测，是训练集目标值的线性组合，系数由“等效核”（3.62）给出，而且等效核满足求和约束（3.64）。

从核密度估计出发，可以从另一个角度引出核回归模型（3.61）。假设有训练集 $\{\mathbf{x}_n,t_n\}$，并使用 Parzen 密度估计器建模联合分布 $p(\mathbf{x},t)$，即<span class="margin-reference">第 2.5.1 节</span>

$$
p(\mathbf{x},t)=\frac{1}{N}\sum_{n=1}^{N}f(\mathbf{x}-\mathbf{x}_n,t-t_n)
\tag{6.42}
$$

其中 $f(\mathbf{x},t)$ 是分量密度函数，每个数据点都对应一个以它为中心的分量。现在求回归函数 $y(\mathbf{x})$ 的表达式，它对应于给定

<!-- pdf-page: 322 -->
<!-- join-previous-paragraph -->
输入变量时目标变量的条件平均值，由下式给出：

$$
\begin{aligned}
y(\mathbf{x})&=\mathbb{E}[t\mid\mathbf{x}]=\int_{-\infty}^{\infty}t p(t\mid\mathbf{x})\,\mathrm{d}t\\
&=\frac{\int t p(\mathbf{x},t)\,\mathrm{d}t}{\int p(\mathbf{x},t)\,\mathrm{d}t}\\
&=\frac{\sum_n\int t f(\mathbf{x}-\mathbf{x}_n,t-t_n)\,\mathrm{d}t}{\sum_m\int f(\mathbf{x}-\mathbf{x}_m,t-t_m)\,\mathrm{d}t}.
\end{aligned}
\tag{6.43}
$$

现在为简单起见，假设分量密度函数的均值为零，即

$$
\int_{-\infty}^{\infty}f(\mathbf{x},t)t\,\mathrm{d}t=0
\tag{6.44}
$$

对所有 $\mathbf{x}$ 都成立。通过简单的变量替换，得到

$$
\begin{aligned}
y(\mathbf{x})&=\frac{\sum_n g(\mathbf{x}-\mathbf{x}_n)t_n}{\sum_m g(\mathbf{x}-\mathbf{x}_m)}\\
&=\sum_n k(\mathbf{x},\mathbf{x}_n)t_n
\end{aligned}
\tag{6.45}
$$

其中 $n,m=1,\ldots,N$，核函数 $k(\mathbf{x},\mathbf{x}_n)$ 为

$$
k(\mathbf{x},\mathbf{x}_n)=\frac{g(\mathbf{x}-\mathbf{x}_n)}{\sum_m g(\mathbf{x}-\mathbf{x}_m)}
\tag{6.46}
$$

并且定义

$$
g(\mathbf{x})=\int_{-\infty}^{\infty}f(\mathbf{x},t)\,\mathrm{d}t.
\tag{6.47}
$$

结果（6.45）称为 Nadaraya–Watson 模型，或核回归（kernel regression）（Nadaraya, 1964；Watson, 1964）。对于局部化的核函数，它会给予靠近 $\mathbf{x}$ 的数据点 $\mathbf{x}_n$ 更大的权重。注意，核（6.46）满足求和约束

$$
\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)=1.
$$

<!-- pdf-page: 323 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/a-fig-6-3.png" alt="正弦数据上的 Nadaraya–Watson 回归、条件均值与两标准差区域"><figcaption>图 6.3：对正弦数据集使用各向同性高斯核的 Nadaraya–Watson 核回归模型示例。绿色曲线表示原始正弦函数，蓝点表示数据点，每个数据点都是一个各向同性高斯核的中心。红线表示由条件均值给出的回归函数，红色阴影表示条件分布 $p(t\mid x)$ 的两个标准差范围。每个数据点周围的蓝色椭圆，是相应核的一个标准差等高线。由于横轴与纵轴的尺度不同，它们看起来不是圆形。</figcaption></figure>

事实上，这个模型不仅定义了条件期望，还定义了完整的条件分布：

$$
p(t\mid\mathbf{x})=\frac{p(t,\mathbf{x})}{\int p(t,\mathbf{x})\,\mathrm{d}t}=\frac{\sum_n f(\mathbf{x}-\mathbf{x}_n,t-t_n)}{\sum_m\int f(\mathbf{x}-\mathbf{x}_m,t-t_m)\,\mathrm{d}t}
\tag{6.48}
$$

从中可以计算其他期望。

作为示例，考虑只有一个输入变量 $x$ 的情况，其中 $f(x,t)$ 是变量 $\mathbf{z}=(x,t)$ 上均值为零、方差为 $\sigma^2$ 的各向同性高斯分布。相应的条件分布（6.48）是一个高斯混合分布。图 6.3 对正弦合成数据集展示了该分布及其条件均值。<span class="margin-reference">习题 6.18</span>

这个模型的一个显然扩展，是允许高斯分量采用更灵活的形式，例如为输入变量和目标变量使用不同的方差参数。更一般地，可以用高斯混合模型来建模联合分布 $p(t,\mathbf{x})$，并用第 9 章介绍的方法进行训练（Ghahramani and Jordan, 1994），然后求出相应的条件分布 $p(t\mid\mathbf{x})$。在后一种情况下，我们不再使用核函数在训练集数据点处求值的表示。不过，混合模型的分量数量可以少于训练点数量，从而使模型在测试数据点上的求值更快。由此，我们接受训练阶段更高的计算成本，以得到预测速度更快的模型。

## 6.4 高斯过程

在第 6.1 节，我们通过把对偶性的概念用于一个非概率回归模型，引入了核。这里，我们将核的作用扩展到概率

<!-- pdf-page: 324 -->
<!-- join-previous-paragraph -->
判别式模型，从而得到高斯过程（Gaussian processes）框架。由此将看到，核如何在贝叶斯框架中自然出现。

在第 3 章，我们考察了形式为 $y(\mathbf{x},\mathbf{w})=\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x})$ 的线性回归模型，其中 $\mathbf{w}$ 是参数向量，$\boldsymbol{\phi}(\mathbf{x})$ 是由依赖输入向量 $\mathbf{x}$ 的固定非线性基函数组成的向量。我们说明了，$\mathbf{w}$ 上的先验分布会诱导函数 $y(\mathbf{x},\mathbf{w})$ 上相应的先验分布。给定训练数据集后，计算 $\mathbf{w}$ 的后验分布，由此得到回归函数上相应的后验分布，再加上噪声，就得到针对新输入向量 $\mathbf{x}$ 的预测分布 $p(t\mid\mathbf{x})$。

从高斯过程的观点看，我们不再使用参数模型，而是直接定义函数上的先验概率分布。乍看之下，处理不可数无限函数空间上的分布似乎很困难。不过，我们将看到，对于有限训练集，只需考虑函数在一组离散输入值 $\mathbf{x}_n$ 处的取值，这些输入值对应于训练集和测试集的数据点，因此实际计算可以在有限空间中进行。

与高斯过程等价的模型，在许多不同领域中都得到了广泛研究。例如，在地统计学文献中，高斯过程回归称为克里金法（kriging）（Cressie, 1993）。类似地，ARMA（自回归移动平均）模型、Kalman 滤波器和径向基函数网络，都可以看作高斯过程模型的不同形式。从机器学习角度介绍高斯过程的综述，可参见 MacKay（1998）、Williams（1999）和 MacKay（2003）；Rasmussen（1996）比较了高斯过程模型与其他方法。另可参见近期的高斯过程教材 Rasmussen and Williams（2006）。

### 6.4.1 重新考察线性回归

为了引出高斯过程的观点，我们回到线性回归的例子，通过考察函数 $y(\mathbf{x},\mathbf{w})$ 上的分布，重新推导预测分布。这将给出高斯过程的一个具体例子。

考虑由 $M$ 个固定基函数的线性组合定义的模型，这些基函数由向量 $\boldsymbol{\phi}(\mathbf{x})$ 的各元素给出，即

$$
y(\mathbf{x})=\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x})
\tag{6.49}
$$

其中 $\mathbf{x}$ 是输入向量，$\mathbf{w}$ 是 $M$ 维权重向量。现在考虑 $\mathbf{w}$ 上的先验分布，设它为如下形式的各向同性高斯分布：

$$
p(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I})
\tag{6.50}
$$

该分布由超参数 $\alpha$ 控制，$\alpha$ 表示分布的精度，即方差的倒数。对于任意给定的 $\mathbf{w}$，定义（6.49）都给出了 $\mathbf{x}$ 的一个具体函数。因此，式（6.50）定义的 $\mathbf{w}$ 的概率分布，会诱导函数 $y(\mathbf{x})$ 上的概率分布。在实践中，我们希望在 $\mathbf{x}$ 的特定值处计算这个函数，例如在训练数据点

<!-- pdf-page: 325 -->
<!-- join-previous-paragraph -->
$\mathbf{x}_1,\ldots,\mathbf{x}_N$ 处。因此，我们关心的是函数值 $y(\mathbf{x}_1),\ldots,y(\mathbf{x}_N)$ 的联合分布。用向量 $\boldsymbol{\mathsf{y}}$ 表示这些值，其元素为 $y_n=y(\mathbf{x}_n)$，其中 $n=1,\ldots,N$。由式（6.49），这个向量为

$$
\boldsymbol{\mathsf{y}}=\boldsymbol{\Phi}\mathbf{w}
\tag{6.51}
$$

其中 $\boldsymbol{\Phi}$ 是设计矩阵，元素为 $\Phi_{nk}=\phi_k(\mathbf{x}_n)$。我们可以按如下方式求 $\boldsymbol{\mathsf{y}}$ 的概率分布。首先注意，$\boldsymbol{\mathsf{y}}$ 是由 $\mathbf{w}$ 各元素给出的高斯分布变量的线性组合，因此它本身也服从高斯分布。于是，只需确定其均值与协方差；由式（6.50），它们为<span class="margin-reference">习题 2.31</span>

$$
\mathbb{E}[\boldsymbol{\mathsf{y}}]=\boldsymbol{\Phi}\mathbb{E}[\mathbf{w}]=\mathbf{0}
\tag{6.52}
$$

$$
\operatorname{cov}[\boldsymbol{\mathsf{y}}]=\mathbb{E}[\boldsymbol{\mathsf{y}}\boldsymbol{\mathsf{y}}^{\mathrm{T}}]=\boldsymbol{\Phi}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm{T}}]\boldsymbol{\Phi}^{\mathrm{T}}=\frac{1}{\alpha}\boldsymbol{\Phi}\boldsymbol{\Phi}^{\mathrm{T}}=\mathbf{K}
\tag{6.53}
$$

其中 $\mathbf{K}$ 是 Gram 矩阵，其元素为

$$
K_{nm}=k(\mathbf{x}_n,\mathbf{x}_m)=\frac{1}{\alpha}\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)
\tag{6.54}
$$

而 $k(\mathbf{x},\mathbf{x}')$ 是核函数。

这个模型给出了高斯过程的一个具体例子。一般来说，高斯过程定义为函数 $y(\mathbf{x})$ 上的概率分布，使得在任意一组点 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 处计算出的 $y(\mathbf{x})$ 值共同服从高斯分布。当输入向量 $\mathbf{x}$ 是二维时，它也称为高斯随机场（Gaussian random field）。更一般地，通过以相互一致的方式给出任意有限组函数值 $y(\mathbf{x}_1),\ldots,y(\mathbf{x}_N)$ 的联合概率分布，就可以确定随机过程（stochastic process）$y(\mathbf{x})$。

高斯随机过程的一个关键性质是，$N$ 个变量 $y_1,\ldots,y_N$ 的联合分布，完全由二阶统计量，即均值和协方差确定。在大多数应用中，我们对 $y(\mathbf{x})$ 的均值没有先验知识，因此根据对称性，将它取为零。从基函数的观点看，这等价于将权重先验 $p(\mathbf{w}\mid\alpha)$ 的均值选为零。然后，只需给出 $y(\mathbf{x})$ 在任意两个 $\mathbf{x}$ 值处的协方差，就完成了高斯过程的定义；这一协方差由核函数给出：

$$
\mathbb{E}[y(\mathbf{x}_n)y(\mathbf{x}_m)]=k(\mathbf{x}_n,\mathbf{x}_m).
\tag{6.55}
$$

对于由线性回归模型（6.49）和权重先验（6.50）定义的高斯过程这一具体情形，核函数由式（6.54）给出。

我们也可以直接定义核函数，而不是通过选择基函数来间接定义。图 6.4 展示了采用两种不同核函数时，从高斯过程中抽取的函数样本。第一种是式（6.23）形式的“高斯”核，第二种是如下指数核：

$$
k(x,x')=\exp(-\theta|x-x'|)
\tag{6.56}
$$

它对应于 Ornstein–Uhlenbeck 过程，最初由 Uhlenbeck and Ornstein（1930）引入，用来描述布朗运动。

<!-- pdf-page: 326 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/a-fig-6-4.png" alt="高斯核和指数核对应的高斯过程函数样本"><figcaption>图 6.4：采用“高斯”核（左图）和指数核（右图）时，从高斯过程中抽取的样本。</figcaption></figure>

### 6.4.2 用于回归的高斯过程

为了把高斯过程模型用于回归问题，需要考虑观测目标值中的噪声；目标值为

$$
t_n=y_n+\epsilon_n
\tag{6.57}
$$

其中 $y_n=y(\mathbf{x}_n)$，$\epsilon_n$ 是随机噪声变量，对每个观测 $n$ 独立选取其值。这里考虑具有高斯分布的噪声过程，即

$$
p(t_n\mid y_n)=\mathcal{N}(t_n\mid y_n,\beta^{-1})
\tag{6.58}
$$

其中 $\beta$ 是表示噪声精度的超参数。由于各数据点的噪声相互独立，给定 $\boldsymbol{\mathsf{y}}=(y_1,\ldots,y_N)^{\mathrm{T}}$ 时，目标值 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm{T}}$ 的联合分布是如下形式的各向同性高斯分布：

$$
p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\mathsf{y}})=\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\mathsf{y}},\beta^{-1}\mathbf{I}_N)
\tag{6.59}
$$

其中 $\mathbf{I}_N$ 表示 $N\times N$ 单位矩阵。根据高斯过程的定义，边缘分布 $p(\boldsymbol{\mathsf{y}})$ 是均值为零、协方差由 Gram 矩阵 $\mathbf{K}$ 定义的高斯分布，即

$$
p(\boldsymbol{\mathsf{y}})=\mathcal{N}(\boldsymbol{\mathsf{y}}\mid\mathbf{0},\mathbf{K}).
\tag{6.60}
$$

决定 $\mathbf{K}$ 的核函数，通常应当表达如下性质：对于相似的点 $\mathbf{x}_n$ 和 $\mathbf{x}_m$，相应值 $y(\mathbf{x}_n)$ 与 $y(\mathbf{x}_m)$ 的相关性，应当强于不相似的点。这里，相似性的具体含义取决于应用。

为了求出给定输入值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 时的边缘分布 $p(\boldsymbol{\mathsf{t}})$，需要对 $\boldsymbol{\mathsf{y}}$ 积分。可以利用第 2.3.3 节中关于线性高斯模型的结果来完成。由式（2.115）可知，$\boldsymbol{\mathsf{t}}$ 的边缘分布为

$$
p(\boldsymbol{\mathsf{t}})=\int p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\mathsf{y}})p(\boldsymbol{\mathsf{y}})\,\mathrm{d}\boldsymbol{\mathsf{y}}=\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\mathbf{0},\mathbf{C})
\tag{6.61}
$$

<!-- pdf-page: 327 -->

其中协方差矩阵 $\mathbf{C}$ 的元素为

$$
C(\mathbf{x}_n,\mathbf{x}_m)=k(\mathbf{x}_n,\mathbf{x}_m)+\beta^{-1}\delta_{nm}.
\tag{6.62}
$$

这一结果反映了如下事实：与 $y(\mathbf{x})$ 和与 $\epsilon$ 分别相关的两个高斯随机来源相互独立，因此它们的协方差可以直接相加。

高斯过程回归中一种广泛使用的核函数，是二次型的指数，再加上常数项和线性项，即

$$
k(\mathbf{x}_n,\mathbf{x}_m)=\theta_0\exp\left\{-\frac{\theta_1}{2}\|\mathbf{x}_n-\mathbf{x}_m\|^2\right\}+\theta_2+\theta_3\mathbf{x}_n^{\mathrm{T}}\mathbf{x}_m.
\tag{6.63}
$$

注意，含 $\theta_3$ 的项对应于一个参数模型，它是输入变量的线性函数。图 6.5 对参数 $\theta_0,\ldots,\theta_3$ 的不同取值，画出了从这一先验中抽取的样本；图 6.6 则展示了从联合分布（6.60）抽取的一组点，以及式（6.61）定义的相应值。

到目前为止，我们已经用高斯过程的观点，为一组数据点上的联合分布建立了模型。不过，回归的目标是在给定一组训练数据后，预测新输入对应的目标变量。假设与输入值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 对应的 $\boldsymbol{\mathsf{t}}_N=(t_1,\ldots,t_N)^{\mathrm{T}}$ 构成观测训练集，我们的目标是预测新输入向量 $\mathbf{x}_{N+1}$ 对应的目标变量 $t_{N+1}$。为此，需要计算预测分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$。注意，这个分布也以变量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 和 $\mathbf{x}_{N+1}$ 为条件。不过，为了保持记号简单，我们不显式写出这些条件变量。

为了求条件分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}})$，先写出联合分布 $p(\boldsymbol{\mathsf{t}}_{N+1})$，其中 $\boldsymbol{\mathsf{t}}_{N+1}$ 表示向量 $(t_1,\ldots,t_N,t_{N+1})^{\mathrm{T}}$。然后应用第 2.3.1 节的结果，得到所需的条件分布，如图 6.7 所示。

由式（6.61），$t_1,\ldots,t_{N+1}$ 的联合分布为

$$
p(\boldsymbol{\mathsf{t}}_{N+1})=\mathcal{N}(\boldsymbol{\mathsf{t}}_{N+1}\mid\mathbf{0},\mathbf{C}_{N+1})
\tag{6.64}
$$

其中 $\mathbf{C}_{N+1}$ 是一个 $(N+1)\times(N+1)$ 协方差矩阵，元素由式（6.62）给出。由于这个联合分布是高斯分布，可以应用第 2.3.1 节的结果，求出条件高斯分布。为此，将协方差矩阵分块如下：

$$
\mathbf{C}_{N+1}=\begin{pmatrix}\mathbf{C}_N&\mathbf{k}\\\mathbf{k}^{\mathrm{T}}&c\end{pmatrix}
\tag{6.65}
$$

其中 $\mathbf{C}_N$ 是 $N\times N$ 协方差矩阵，其元素由式（6.62）在 $n,m=1,\ldots,N$ 时给出；向量 $\mathbf{k}$ 的元素为 $k(\mathbf{x}_n,\mathbf{x}_{N+1})$，其中 $n=1,\ldots,N$，而标量

<!-- pdf-page: 328 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-5.png" alt="六组不同核参数下从高斯过程先验抽取的函数样本"><figcaption>图 6.5：从协方差函数（6.63）定义的高斯过程先验中抽取的样本。每张图上方的标题表示 $(\theta_0,\theta_1,\theta_2,\theta_3)$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
$c=k(\mathbf{x}_{N+1},\mathbf{x}_{N+1})+\beta^{-1}$。利用结果（2.81）和（2.82），可知条件分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}})$ 是高斯分布，其均值和协方差分别为

$$
m(\mathbf{x}_{N+1})=\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}
\tag{6.66}
$$

$$
\sigma^2(\mathbf{x}_{N+1})=c-\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{k}.
\tag{6.67}
$$

这两个关键结果定义了高斯过程回归。由于向量 $\mathbf{k}$ 是测试点输入值 $\mathbf{x}_{N+1}$ 的函数，预测分布是一个均值和方差都依赖于 $\mathbf{x}_{N+1}$ 的高斯分布。图 6.8 给出了高斯过程回归的一个例子。

对核函数唯一的限制是，（6.62）给出的协方差矩阵必须正定。如果 $\lambda_i$ 是 $\mathbf{K}$ 的一个特征值，那么 $\mathbf{C}$ 的相应特征值为 $\lambda_i+\beta^{-1}$。因此，只需核矩阵 $k(\mathbf{x}_n,\mathbf{x}_m)$ 对任意一对点 $\mathbf{x}_n$、$\mathbf{x}_m$ 都是半正定的，从而有 $\lambda_i\geqslant0$；因为 $\beta>0$，即使某个特征值 $\lambda_i$ 为零，$\mathbf{C}$ 的相应特征值仍然为正。这与前面对核函数讨论过的限制相同，因此可以再次利用 6.2 节中的所有技术来构造

<!-- pdf-page: 329 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-6.png" alt="高斯过程函数样本、在输入点的函数值及加入高斯噪声后的观测值"><figcaption>图 6.6：从高斯过程中采样数据点 $\{t_n\}$ 的示意图。蓝色曲线是从函数的高斯过程先验中抽取的一个函数样本，红色点是在一组输入值 $\{x_n\}$ 处计算该函数而得到的 $y_n$ 值。绿色表示相应的 $\{t_n\}$，它们通过向每个 $\{y_n\}$ 加入独立高斯噪声而得到。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
合适的核。

注意，将预测分布的均值（6.66）看作 $\mathbf{x}_{N+1}$ 的函数时，可以写成

$$
m(\mathbf{x}_{N+1})=\sum_{n=1}^{N}a_n k(\mathbf{x}_n,\mathbf{x}_{N+1})
\tag{6.68}
$$

其中 $a_n$ 是 $\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}$ 的第 $n$ 个分量。因此，如果核函数 $k(\mathbf{x}_n,\mathbf{x}_m)$ 仅依赖于距离 $\|\mathbf{x}_n-\mathbf{x}_m\|$，就得到了径向基函数展开。

结果（6.66）和（6.67）定义了任意核函数 $k(\mathbf{x}_n,\mathbf{x}_m)$ 下高斯过程回归的预测分布。在一个特殊情况下，核函数 $k(\mathbf{x},\mathbf{x}')$ 由有限个基函数定义，这时可以从高斯过程的观点出发，推导出此前在 3.3.2 节中得到的线性回归结果（习题 6.21）。

因此，对于这样的模型，既可以采用参数空间的观点，利用线性回归的结果来得到预测分布，也可以采用函数空间的观点，利用高斯过程的结果来得到预测分布。

使用高斯过程时，核心计算操作涉及一个 $N\times N$ 矩阵的求逆，标准方法需要 $O(N^3)$ 的计算量。相比之下，在基函数模型中，需要求一个 $M\times M$ 矩阵 $\mathbf{S}_N$ 的逆，计算复杂度为 $O(M^3)$。注意，对两种观点而言，对于给定训练集都只需进行一次矩阵求逆。对于每个新的测试点，两种方法都需要进行向量与矩阵的乘法；高斯过程的代价为 $O(N^2)$，线性基函数模型的代价为 $O(M^2)$。如果基函数数目 $M$ 小于数据点数目 $N$，那么采用基函数

<!-- pdf-page: 330 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-7.png" alt="由一个训练点的条件值从联合高斯分布得到测试点的条件分布"><figcaption>图 6.7：只有一个训练点和一个测试点时，高斯过程回归机制的示意图。红色椭圆为联合分布 $p(t_1,t_2)$ 的等高线。这里 $t_1$ 是训练数据点，以 $t_1$ 的值为条件，对应于蓝色竖线，就得到 $p(t_2\mid t_1)$，绿色曲线表示它作为 $t_2$ 的函数。</figcaption><p class="figure-translation">$t_1$：训练点目标值；$t_2$：测试点目标值；$m(\mathbf{x}_2)$：条件均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
框架在计算上会更高效。不过，高斯过程观点的一个优点是，可以考虑那些只能用无穷多个基函数来表示的协方差函数。

然而，对于大型训练数据集，直接应用高斯过程方法可能不可行，因此已经发展出一系列近似方案。与精确方法相比，这些方案的计算量随训练集规模增长得更慢（Gibbs, 1997; Tresp, 2001; Smola and Bartlett, 2001; Williams and Seeger, 2001; Csató and Opper, 2002; Seeger et al., 2003）。Bishop and Nabney（2008）讨论了高斯过程应用中的实际问题。

我们已经介绍了单个目标变量情况下的高斯过程回归。将这一形式扩展到多个目标变量很直接，这称为*协同克里金*（co-kriging）（Cressie, 1993；习题 6.23）。高斯

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-8.png" alt="高斯过程回归的预测均值与两标准差区间，右侧缺少观测时不确定性增大"><figcaption>图 6.8：将高斯过程回归应用于图 A.6 中正弦数据集的示例，其中省略了最右边的三个数据点。绿色曲线是正弦函数；蓝色数据点通过对该函数采样并加入高斯噪声得到。红色线表示高斯过程预测分布的均值，阴影区域对应于均值上下各两个标准差的范围。注意，在数据点右侧的区域，不确定性如何增大。</figcaption></figure>

<!-- pdf-page: 331 -->

<!-- join-previous-paragraph-across-figures -->
过程回归的其他扩展也已有研究，例如，为无监督学习对低维流形上的分布建模（Bishop et al., 1998a），以及求解随机微分方程（Graepel, 2003）。

### 6.4.3 学习超参数

高斯过程模型的预测，部分取决于协方差函数的选择。在实际应用中，我们可能更愿意使用一个参数化的函数族，再从数据中推断参数值，而不是固定协方差函数。这些参数控制相关性的长度尺度、噪声精度等性质，对应于标准参数模型中的超参数。

学习超参数的技术以计算似然函数 $p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 为基础，其中 $\boldsymbol{\theta}$ 表示高斯过程模型的超参数。最简单的方法是通过最大化对数似然函数，得到 $\boldsymbol{\theta}$ 的点估计。由于 $\boldsymbol{\theta}$ 表示这个回归问题的一组超参数，这可以看作与线性回归模型的第二类最大似然过程类似（3.5 节）。可以使用共轭梯度等高效的基于梯度的优化算法，来最大化对数似然（Fletcher, 1987; Nocedal and Wright, 1999; Bishop and Nabney, 2008）。

利用多元高斯分布的标准形式，很容易计算高斯过程回归模型的对数似然函数，得到

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=-\frac{1}{2}\ln|\mathbf{C}_N|-\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}-\frac{N}{2}\ln(2\pi).
\tag{6.69}
$$

对于非线性优化，还需要对数似然函数关于参数向量 $\boldsymbol{\theta}$ 的梯度。假设 $\mathbf{C}_N$ 的导数很容易计算，本章所考虑的协方差函数都满足这一点。利用 $\mathbf{C}_N^{-1}$ 的导数结果（C.21）和 $\ln|\mathbf{C}_N|$ 的导数结果（C.22），得到

$$
\frac{\partial}{\partial\theta_i}\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=-\frac{1}{2}\operatorname{Tr}\left(\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_i}\right)+\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_i}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}.
\tag{6.70}
$$

由于 $\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 一般是非凸函数，它可能具有多个极大值。

很容易为 $\boldsymbol{\theta}$ 引入先验，再使用基于梯度的方法最大化对数后验。在完全贝叶斯处理中，需要对 $\boldsymbol{\theta}$ 进行边缘化，权重为先验 $p(\boldsymbol{\theta})$ 与似然函数 $p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 的乘积。不过，一般情况下，精确边缘化难以完成，必须借助近似。

高斯过程回归模型给出的预测分布，其均值和方差都是输入向量 $\mathbf{x}$ 的函数。不过，我们假设预测方差中来自加性噪声、由参数 $\beta$ 控制的那部分贡献是一个常数。对于某些称为*异方差*（heteroscedastic）的问题，噪声方差本身也依赖于 $\mathbf{x}$。为此，可以扩展

<!-- pdf-page: 332 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-9.png" alt="两个高斯过程ARD先验曲面样本，比较不同输入方向精度参数的影响"><figcaption>图 6.9：从高斯过程的 ARD 先验中抽取的样本，其中核函数由（6.71）给出。左图对应于 $\eta_1=\eta_2=1$，右图对应于 $\eta_1=1,\eta_2=0.01$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
高斯过程框架，引入第二个高斯过程，表示 $\beta$ 对输入 $\mathbf{x}$ 的依赖关系（Goldberg et al., 1998）。由于 $\beta$ 是方差，因此非负，所以使用高斯过程对 $\ln\beta(\mathbf{x})$ 建模。

### 6.4.4 自动相关性确定

在上一节中，我们看到，可以利用最大似然来确定高斯过程中的相关长度尺度参数。为每个输入变量分别引入一个参数，可以有效地扩展这一技术（Rasmussen and Williams, 2006）。我们将看到，通过最大似然优化这些参数，就能够从数据中推断不同输入的相对重要性。这是高斯过程背景下*自动相关性确定*（automatic relevance determination，ARD）的一个例子；ARD 最初是在神经网络框架中提出的（MacKay, 1994; Neal, 1996）。7.2.2 节将讨论偏好适当输入的机制。

考虑一个输入空间为二维 $\mathbf{x}=(x_1,x_2)$ 的高斯过程，其核函数具有如下形式：

$$
k(\mathbf{x},\mathbf{x}')=\theta_0\exp\left\{-\frac{1}{2}\sum_{i=1}^{2}\eta_i(x_i-x_i')^2\right\}.
\tag{6.71}
$$

图 6.9 给出了精度参数 $\eta_i$ 取两组不同值时，从所得到的函数 $y(\mathbf{x})$ 的先验中抽取的样本。可以看到，随着某个参数 $\eta_i$ 变小，函数对相应输入变量 $x_i$ 的变化变得相对不敏感。利用最大似然，根据数据集调整这些参数，就可以检测出对预测分布几乎没有影响的输入变量，因为相应的 $\eta_i$ 值会很小。这在实际应用中很有用，因为可以据此舍弃这样的输入。图 6.10 使用一个具有三个输入 $x_1$、$x_2$ 和 $x_3$ 的简单合成数据集说明 ARD（Nabney, 2002）。目标变量 $t$ 的生成方法是：从高斯分布中采样 100 个 $x_1$ 值，计算函数 $\sin(2\pi x_1)$，然后加入

<!-- pdf-page: 333 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-10.png" alt="三个输入对应的自动相关性超参数在边缘似然优化过程中的变化"><figcaption>图 6.10：在一个具有三个输入 $x_1$、$x_2$ 和 $x_3$ 的合成问题中，高斯过程自动相关性确定的示例。曲线表示优化边缘似然时，相应超参数 $\eta_1$（红色）、$\eta_2$（绿色）和 $\eta_3$（蓝色）随迭代次数的变化。详情见正文。注意，纵轴采用对数刻度。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
高斯噪声。$x_2$ 的值由相应的 $x_1$ 值加上噪声得到，$x_3$ 的值则从一个独立的高斯分布中采样。因此，$x_1$ 能很好地预测 $t$，$x_2$ 也能预测 $t$，但噪声更大，而 $x_3$ 与 $t$ 之间只有偶然的相关性。使用缩放共轭梯度算法，优化具有 ARD 参数 $\eta_1,\eta_2,\eta_3$ 的高斯过程的边缘似然。由图 6.10 可见，$\eta_1$ 收敛到一个相对较大的值，$\eta_2$ 收敛到一个小得多的值，而 $\eta_3$ 变得非常小，表明 $x_3$ 与预测 $t$ 无关。

很容易将 ARD 框架纳入指数二次核（6.63），得到如下形式的核函数。在将高斯过程用于多种回归问题时，这种核函数已被证明很有用：

$$
k(\mathbf{x}_n,\mathbf{x}_m)=\theta_0\exp\left\{-\frac{1}{2}\sum_{i=1}^{D}\eta_i(x_{ni}-x_{mi})^2\right\}+\theta_2+\theta_3\sum_{i=1}^{D}x_{ni}x_{mi}
\tag{6.72}
$$

其中 $D$ 是输入空间的维数。

### 6.4.5 用于分类的高斯过程

在分类的概率方法中，目标是在给定训练数据集后，为一个新的输入向量建立目标变量的后验概率模型。这些概率必须位于区间 $(0,1)$ 内，而高斯过程模型的预测值可以位于整个实轴。不过，利用适当的非线性激活函数变换高斯过程的输出，就很容易将高斯过程用于分类问题。

首先考虑目标变量为 $t\in\{0,1\}$ 的二类问题。如果为函数 $a(\mathbf{x})$ 定义一个高斯过程，再利用（4.59）给出的 logistic sigmoid 函数 $y=\sigma(a)$ 进行变换，就得到函数 $y(\mathbf{x})$ 上的非高斯随机过程，其中 $y\in(0,1)$。图 6.11 展示了一维输入空间的情况，此时目标变量 $t$ 的概率分布

<!-- pdf-page: 334 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-11.png" alt="高斯过程潜在函数样本及其经过logistic sigmoid变换后的结果"><figcaption>图 6.11：左图是从函数 $a(\mathbf{x})$ 的高斯过程先验中抽取的一个样本，右图是将这个样本通过 logistic sigmoid 函数变换后的结果。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
由伯努利分布给出：

$$
p(t\mid a)=\sigma(a)^t(1-\sigma(a))^{1-t}.
\tag{6.73}
$$

像通常一样，将训练集的输入记为 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，对应的观测目标变量为 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。还考虑一个测试点 $\mathbf{x}_{N+1}$，其目标值为 $t_{N+1}$。目标是确定预测分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}})$，其中对输入变量的条件依赖隐含在表达式中。为此，对向量 $\mathbf{a}_{N+1}$ 引入一个高斯过程先验，其分量为 $a(\mathbf{x}_1),\ldots,a(\mathbf{x}_{N+1})$。这又定义了 $\mathbf{t}_{N+1}$ 上的一个非高斯过程；以训练数据 $\mathbf{t}_N$ 为条件，就得到所需的预测分布。$\mathbf{a}_{N+1}$ 的高斯过程先验具有如下形式：

$$
p(\mathbf{a}_{N+1})=\mathcal{N}(\mathbf{a}_{N+1}\mid\mathbf{0},\mathbf{C}_{N+1}).
\tag{6.74}
$$

与回归情况不同，协方差矩阵不再包含噪声项，因为假设所有训练数据点的标记都是正确的。不过，出于数值计算的原因，引入一个由参数 $\nu$ 控制的类噪声项会更方便，它可以确保协方差矩阵正定。因此，协方差矩阵 $\mathbf{C}_{N+1}$ 的元素为

$$
C(\mathbf{x}_n,\mathbf{x}_m)=k(\mathbf{x}_n,\mathbf{x}_m)+\nu\delta_{nm}
\tag{6.75}
$$

其中 $k(\mathbf{x}_n,\mathbf{x}_m)$ 可以是 6.2 节所考虑的任意半正定核函数，而 $\nu$ 的值通常预先固定。假设核函数 $k(\mathbf{x},\mathbf{x}')$ 由参数向量 $\boldsymbol{\theta}$ 控制，稍后将讨论如何从训练数据中学习 $\boldsymbol{\theta}$。

对于二类问题，只需预测 $p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)$，因为 $p(t_{N+1}=0\mid\boldsymbol{\mathsf{t}}_N)$ 的值为 $1-p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)$。所需的

<!-- pdf-page: 335 -->

<!-- join-previous-paragraph -->
预测分布为

$$
p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)=\int p(t_{N+1}=1\mid a_{N+1})p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)\,da_{N+1}
\tag{6.76}
$$

其中 $p(t_{N+1}=1\mid a_{N+1})=\sigma(a_{N+1})$。

这个积分无法解析求出，因此可以用采样方法近似（Neal, 1997）。另一种选择是考虑基于解析近似的技术。在 4.5.2 节中，我们推导了 logistic sigmoid 函数与高斯分布的卷积的近似公式（4.153）。只要有后验分布 $p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 的高斯近似，就可以利用这个结果计算（6.76）中的积分。通常，用高斯分布近似后验分布的依据是：由中心极限定理，真实后验分布会随着数据点数目的增加而趋于高斯分布（2.3 节）。对于高斯过程，变量数目随数据点数目一起增长，因此不能直接应用这一论证。不过，如果考虑增加 $\mathbf{x}$ 空间某个固定区域内的数据点数目，那么函数 $a(\mathbf{x})$ 的相应不确定性就会减小，同样会渐近地得到高斯分布（Williams and Barber, 1998）。

已有研究考虑了三种不同的高斯近似方法。第一种技术基于变分推断（Gibbs and MacKay, 2000；10.1 节），并利用 logistic sigmoid 函数的局部变分界（10.144）。这样可以将 sigmoid 函数的乘积近似为高斯函数的乘积，从而对 $\mathbf{a}_N$ 进行解析边缘化。该方法还给出了似然函数 $p(\mathbf{t}_N\mid\boldsymbol{\theta})$ 的一个下界。通过对 softmax 函数作高斯近似，高斯过程分类的变分框架还可以扩展到多类（$K>2$）问题（Gibbs, 1997）。

第二种方法使用期望传播（Opper and Winther, 2000b; Minka, 2001b; Seeger, 2003；10.7 节）。正如马上将会看到的，真实后验分布是单峰的，因此期望传播方法可以取得较好的结果。

### 6.4.6 拉普拉斯近似

高斯过程分类的第三种方法基于拉普拉斯近似（4.4 节），现在对它作详细讨论。为了计算预测分布（6.76），我们寻找 $a_{N+1}$ 的后验分布的高斯近似。根据贝叶斯定理，该后验分布为

$$
\begin{aligned}
p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)&=\int p(a_{N+1},\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)\,d\mathbf{a}_N\\
&=\frac{1}{p(\boldsymbol{\mathsf{t}}_N)}\int p(a_{N+1},\mathbf{a}_N)p(\boldsymbol{\mathsf{t}}_N\mid a_{N+1},\mathbf{a}_N)\,d\mathbf{a}_N\\
&=\frac{1}{p(\boldsymbol{\mathsf{t}}_N)}\int p(a_{N+1}\mid\mathbf{a}_N)p(\mathbf{a}_N)p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)\,d\mathbf{a}_N\\
&=\int p(a_{N+1}\mid\mathbf{a}_N)p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)\,d\mathbf{a}_N
\end{aligned}
\tag{6.77}
$$

<!-- pdf-page: 336 -->

这里使用了 $p(\boldsymbol{\mathsf{t}}_N\mid a_{N+1},\mathbf{a}_N)=p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)$。利用高斯过程回归的结果（6.66）和（6.67），得到条件分布 $p(a_{N+1}\mid\mathbf{a}_N)$：

$$
p(a_{N+1}\mid\mathbf{a}_N)=\mathcal{N}(a_{N+1}\mid\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{a}_N,c-\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{k}).
\tag{6.78}
$$

因此，可以先求出后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的拉普拉斯近似，再使用两个高斯分布卷积的标准结果，来计算（6.77）中的积分。

先验 $p(\mathbf{a}_N)$ 由均值为零、协方差矩阵为 $\mathbf{C}_N$ 的高斯过程给出，而在假设数据点相互独立时，数据项为

$$
p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)=\prod_{n=1}^{N}\sigma(a_n)^{t_n}(1-\sigma(a_n))^{1-t_n}=\prod_{n=1}^{N}e^{a_nt_n}\sigma(-a_n).
\tag{6.79}
$$

随后，对 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的对数作 Taylor 展开，得到拉普拉斯近似。除了一个加性的归一化常数外，这个对数由下列量给出：

$$
\begin{aligned}
\Psi(\mathbf{a}_N)&=\ln p(\mathbf{a}_N)+\ln p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)\\
&=-\frac{1}{2}\mathbf{a}_N^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{a}_N-\frac{N}{2}\ln(2\pi)-\frac{1}{2}\ln|\mathbf{C}_N|+\boldsymbol{\mathsf{t}}_N^{\mathrm T}\mathbf{a}_N\\
&\quad-\sum_{n=1}^{N}\ln(1+e^{a_n})+\mathrm{const}.
\end{aligned}
\tag{6.80}
$$

首先，需要找到后验分布的众数，这要求计算 $\Psi(\mathbf{a}_N)$ 的梯度，它为

$$
\nabla\Psi(\mathbf{a}_N)=\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N-\mathbf{C}_N^{-1}\mathbf{a}_N
\tag{6.81}
$$

其中 $\boldsymbol{\sigma}_N$ 是元素为 $\sigma(a_n)$ 的向量。不能简单地令这个梯度为零来求众数，因为 $\boldsymbol{\sigma}_N$ 非线性地依赖于 $\mathbf{a}_N$；因此，采用基于 Newton–Raphson 方法的迭代方案，由此得到迭代重加权最小二乘（IRLS）算法（4.3.3 节）。这需要 $\Psi(\mathbf{a}_N)$ 的二阶导数，而拉普拉斯近似本来也需要这些导数，它们为

$$
\nabla\nabla\Psi(\mathbf{a}_N)=-\mathbf{W}_N-\mathbf{C}_N^{-1}
\tag{6.82}
$$

其中 $\mathbf{W}_N$ 是对角矩阵，对角元素为 $\sigma(a_n)(1-\sigma(a_n))$，这里使用了 logistic sigmoid 函数的导数结果（4.88）。注意，这些对角元素位于区间 $(0,1/4)$ 内，因此 $\mathbf{W}_N$ 是正定矩阵。由于按构造 $\mathbf{C}_N$ 及其逆矩阵都是正定的，而且两个正定矩阵之和仍为正定矩阵（习题 6.24），可知 Hessian 矩阵 $\mathbf{A}=-\nabla\nabla\Psi(\mathbf{a}_N)$ 正定，因此后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 是对数凸的，只有一个众数，并且它是全局

<!-- pdf-page: 337 -->

<!-- join-previous-paragraph -->
最大值。不过，后验分布并不是高斯分布，因为 Hessian 矩阵是 $\mathbf{a}_N$ 的函数。

使用 Newton–Raphson 公式（4.92），$\mathbf{a}_N$ 的迭代更新方程为（习题 6.25）

$$
\mathbf{a}_N^{\mathrm{new}}=\mathbf{C}_N(\mathbf{I}+\mathbf{W}_N\mathbf{C}_N)^{-1}\{\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N+\mathbf{W}_N\mathbf{a}_N\}.
\tag{6.83}
$$

反复应用这些方程，直到收敛到众数，将它记为 $\mathbf{a}_N^{\star}$。在众数处，梯度 $\nabla\Psi(\mathbf{a}_N)$ 为零，因此 $\mathbf{a}_N^{\star}$ 满足

$$
\mathbf{a}_N^{\star}=\mathbf{C}_N(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N).
\tag{6.84}
$$

一旦找到后验分布的众数 $\mathbf{a}_N^{\star}$，就可以计算 Hessian 矩阵

$$
\mathbf{H}=-\nabla\nabla\Psi(\mathbf{a}_N)=\mathbf{W}_N+\mathbf{C}_N^{-1}
\tag{6.85}
$$

其中 $\mathbf{W}_N$ 的元素利用 $\mathbf{a}_N^{\star}$ 计算。这就定义了后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的高斯近似：

$$
q(\mathbf{a}_N)=\mathcal{N}(\mathbf{a}_N\mid\mathbf{a}_N^{\star},\mathbf{H}^{-1}).
\tag{6.86}
$$

现在可以将它与（6.78）结合，计算积分（6.77）。由于这对应于线性高斯模型，可以使用一般结果（2.115），得到（习题 6.26）

$$
\mathbb{E}[a_{N+1}\mid\boldsymbol{\mathsf{t}}_N]=\mathbf{k}^{\mathrm T}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N)
\tag{6.87}
$$

$$
\operatorname{var}[a_{N+1}\mid\boldsymbol{\mathsf{t}}_N]=c-\mathbf{k}^{\mathrm T}(\mathbf{W}_N^{-1}+\mathbf{C}_N)^{-1}\mathbf{k}.
\tag{6.88}
$$

现在，$p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 已经是高斯分布，就可以利用结果（4.153）来近似积分（6.76）。与 4.5 节的贝叶斯逻辑回归模型一样，如果只关心对应于 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}}_N)=0.5$ 的决策边界，那么只需考虑均值，可以忽略方差的影响。

还需要确定协方差函数的参数 $\boldsymbol{\theta}$。一种方法是最大化似然函数 $p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})$，这需要对数似然及其梯度的表达式。如有需要，还可以加入合适的正则化项，得到带惩罚的最大似然解。似然函数定义为

$$
p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})=\int p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)p(\mathbf{a}_N\mid\boldsymbol{\theta})\,d\mathbf{a}_N.
\tag{6.89}
$$

这个积分无法解析求出，因此再次使用拉普拉斯近似。利用结果（4.135），得到似然函数对数的如下近似：

$$
\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})=\Psi(\mathbf{a}_N^{\star})-\frac{1}{2}\ln|\mathbf{W}_N+\mathbf{C}_N^{-1}|+\frac{N}{2}\ln(2\pi)
\tag{6.90}
$$

<!-- pdf-page: 338 -->

其中 $\Psi(\mathbf{a}_N^{\star})=\ln p(\mathbf{a}_N^{\star}\mid\boldsymbol{\theta})+\ln p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N^{\star})$。还需要计算 $\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})$ 关于参数向量 $\boldsymbol{\theta}$ 的梯度。注意，$\boldsymbol{\theta}$ 的变化会引起 $\mathbf{a}_N^{\star}$ 的变化，从而在梯度中产生额外的项。因此，对（6.90）关于 $\boldsymbol{\theta}$ 求导时，会得到两组项：第一组来自协方差矩阵 $\mathbf{C}_N$ 对 $\boldsymbol{\theta}$ 的依赖，其余项来自 $\mathbf{a}_N^{\star}$ 对 $\boldsymbol{\theta}$ 的依赖。

利用（6.80）以及结果（C.21）、（C.22），可以求出由对 $\boldsymbol{\theta}$ 的显式依赖产生的项：

$$
\begin{aligned}
\frac{\partial\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})}{\partial\theta_j}
&=\frac{1}{2}(\mathbf{a}_N^{\star})^{\mathrm T}\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_j}\mathbf{C}_N^{-1}\mathbf{a}_N^{\star}\\
&\quad-\frac{1}{2}\operatorname{Tr}\left[(\mathbf{I}+\mathbf{C}_N\mathbf{W}_N)^{-1}\mathbf{W}_N\frac{\partial\mathbf{C}_N}{\partial\theta_j}\right].
\end{aligned}
\tag{6.91}
$$

为了计算由 $\mathbf{a}_N^{\star}$ 对 $\boldsymbol{\theta}$ 的依赖所产生的项，注意拉普拉斯近似的构造保证 $\Psi(\mathbf{a}_N)$ 在 $\mathbf{a}_N=\mathbf{a}_N^{\star}$ 处的梯度为零。因此，$\Psi(\mathbf{a}_N^{\star})$ 对 $\mathbf{a}_N^{\star}$ 的依赖不会对梯度产生贡献。剩下关于 $\boldsymbol{\theta}$ 的分量 $\theta_j$ 的导数贡献为

$$
\begin{aligned}
&-\frac{1}{2}\sum_{n=1}^{N}\frac{\partial\ln|\mathbf{W}_N+\mathbf{C}_N^{-1}|}{\partial a_n^{\star}}\frac{\partial a_n^{\star}}{\partial\theta_j}\\
&\quad=-\frac{1}{2}\sum_{n=1}^{N}\left[(\mathbf{I}+\mathbf{C}_N\mathbf{W}_N)^{-1}\mathbf{C}_N\right]_{nn}\sigma_n^{\star}(1-\sigma_n^{\star})(1-2\sigma_n^{\star})\frac{\partial a_n^{\star}}{\partial\theta_j}
\end{aligned}
\tag{6.92}
$$

其中 $\sigma_n^{\star}=\sigma(a_n^{\star})$，这里再次使用了结果（C.22）和 $\mathbf{W}_N$ 的定义。对关系式（6.84）关于 $\theta_j$ 求导，就可以计算 $\mathbf{a}_N^{\star}$ 关于 $\theta_j$ 的导数，得到

$$
\frac{\partial a_n^{\star}}{\partial\theta_j}=\frac{\partial\mathbf{C}_N}{\partial\theta_j}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N)-\mathbf{C}_N\mathbf{W}_N\frac{\partial a_n^{\star}}{\partial\theta_j}.
\tag{6.93}
$$

整理得到

$$
\frac{\partial a_n^{\star}}{\partial\theta_j}=(\mathbf{I}+\mathbf{W}_N\mathbf{C}_N)^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_j}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N).
\tag{6.94}
$$

结合（6.91）、（6.92）和（6.94），就可以计算对数似然函数的梯度，并将它与标准非线性优化算法结合，用来确定 $\boldsymbol{\theta}$ 的值。

可以使用图 6.12 所示的合成二类数据集（附录 A），说明拉普拉斯近似在高斯过程中的应用。利用 softmax 激活函数，很容易将拉普拉斯近似扩展到涉及 $K>2$ 个类别的高斯过程（Williams and Barber, 1998）。

<!-- pdf-page: 339 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-12.png" alt="高斯过程分类的训练数据、决策边界及两个类别的预测后验概率"><figcaption>图 6.12：使用高斯过程进行分类的示例。左图给出数据，以及真实分布的最优决策边界（绿色）和高斯过程分类器的决策边界（黑色）。右图给出蓝色、红色两个类别的预测后验概率，以及高斯过程的决策边界。</figcaption></figure>

### 6.4.7 与神经网络的联系

我们已经看到，神经网络能够表示的函数范围由隐藏单元数目 $M$ 决定；当 $M$ 足够大时，两层网络可以以任意精度近似任何给定函数。在最大似然框架中，为避免过拟合，需要将隐藏单元的数目限制在一个取决于训练集大小的水平。不过，从贝叶斯观点看，根据训练集的大小来限制网络中的参数数目并没有多少意义。

在贝叶斯神经网络中，参数向量 $\mathbf{w}$ 的先验分布与网络函数 $f(\mathbf{x},\mathbf{w})$ 相结合，会产生函数 $\mathbf{y}(\mathbf{x})$ 上的先验分布，其中 $\mathbf{y}$ 是网络输出向量。Neal（1996）证明，对于一大类 $\mathbf{w}$ 的先验分布，在 $M\to\infty$ 的极限下，神经网络生成的函数分布将趋于一个高斯过程。不过，应该注意，在这一极限下，神经网络的输出变量变得相互独立。神经网络的一项重要优点是，各输出共享隐藏单元，因此能够彼此“借用统计信息”；也就是说，与每个隐藏单元关联的权重都受到所有输出变量的影响，而不仅受到其中一个输出变量的影响。因此，在高斯过程极限下，这一性质就丢失了。

我们已经看到，高斯过程由它的协方差函数，也就是核函数确定。对于隐藏单元激活函数的两种具体选择——probit 函数和高斯函数，Williams（1998）给出了协方差的显式形式。这些核函数 $k(\mathbf{x},\mathbf{x}')$ 是非平稳的，即不能表示成差值 $\mathbf{x}-\mathbf{x}'$ 的函数。这是因为高斯权重先验以零为中心，破坏了权重空间中的平移不变性。

<!-- pdf-page: 340 -->

直接使用协方差函数，相当于隐式地对权重分布进行了边缘化。如果权重先验由超参数控制，那么这些超参数的值将决定函数分布的长度尺度；通过研究图 5.11 中隐藏单元数目有限时的例子，可以理解这一点。注意，无法解析地将超参数边缘化掉，必须借助 6.4 节讨论的那类技术。

## 习题

**6.1（⋆⋆）www** 考虑 6.1 节给出的最小二乘线性回归问题的对偶形式。证明，向量 $\mathbf{a}$ 的分量 $a_n$ 的解可以表示为向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 各元素的线性组合。将这些系数记为向量 $\mathbf{w}$，证明对偶形式的对偶，就是原先用参数向量 $\mathbf{w}$ 表示的形式。

**6.2（⋆⋆）** 本题推导感知机学习算法的对偶形式。利用感知机学习规则（4.55），证明学到的权重向量 $\mathbf{w}$ 可以写成向量 $t_n\boldsymbol{\phi}(\mathbf{x}_n)$ 的线性组合，其中 $t_n\in\{-1,+1\}$。将这个线性组合的系数记为 $\alpha_n$，推导用 $\alpha_n$ 表示的感知机学习算法和感知机预测函数。证明，特征向量 $\boldsymbol{\phi}(\mathbf{x})$ 仅以核函数 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')$ 的形式出现。

**6.3（⋆）** 最近邻分类器（2.5.2 节）将新输入向量 $\mathbf{x}$ 分到训练集中距它最近的输入向量 $\mathbf{x}_n$ 所属的类别；在最简单的情况下，距离由欧氏度量 $\|\mathbf{x}-\mathbf{x}_n\|^2$ 定义。用标量积表示这一规则，再利用核替换，给出一般非线性核下的最近邻分类器。

**6.4（⋆）** 在附录 C 中，我们给出了一个矩阵的例子，它的元素均为正，却具有负特征值，因此不是正定矩阵。找出一个具有相反性质的例子，即一个特征值均为正、但至少有一个负元素的 $2\times2$ 矩阵。

**6.5（⋆）www** 验证构造有效核的结果（6.13）和（6.14）。

**6.6（⋆）** 验证构造有效核的结果（6.15）和（6.16）。

**6.7（⋆）www** 验证构造有效核的结果（6.17）和（6.18）。

**6.8（⋆）** 验证构造有效核的结果（6.19）和（6.20）。

**6.9（⋆）** 验证构造有效核的结果（6.21）和（6.22）。

**6.10（⋆）** 证明，对于学习函数 $f(\mathbf{x})$，一个很好的核选择是 $k(\mathbf{x},\mathbf{x}')=f(\mathbf{x})f(\mathbf{x}')$；为此，证明基于这个核的线性学习机器总会找到一个与 $f(\mathbf{x})$ 成正比的解。

<!-- pdf-page: 341 -->

**6.11（⋆）** 利用展开式（6.25），再将中间的因子展开为幂级数，证明高斯核（6.23）可以表示为无穷维特征向量的内积。

**6.12（⋆⋆）www** 考虑一个给定固定集合 $D$ 的所有可能子集 $A$ 所构成的空间。证明，核函数（6.27）对应于由映射 $\boldsymbol{\phi}(A)$ 定义的 $2^{|D|}$ 维特征空间中的内积，其中 $A$ 是 $D$ 的一个子集，而以子集 $U$ 为索引的元素 $\phi_U(A)$ 为

$$
\phi_U(A)=\begin{cases}
1,&\text{若 }U\subseteq A;\\
0,&\text{否则。}
\end{cases}
\tag{6.95}
$$

这里 $U\subseteq A$ 表示 $U$ 是 $A$ 的子集，或者等于 $A$。

**6.13（⋆）** 证明，在对参数向量进行非线性变换 $\boldsymbol{\theta}\to\boldsymbol{\psi}(\boldsymbol{\theta})$ 后，由（6.33）定义的 Fisher 核保持不变，其中函数 $\boldsymbol{\psi}(\cdot)$ 可逆且可微。

**6.14（⋆）www** 对于均值为 $\boldsymbol{\mu}$、协方差 $\mathbf{S}$ 固定的高斯分布 $p(\mathbf{x}\mid\boldsymbol{\mu})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\mathbf{S})$，写出（6.33）定义的 Fisher 核的形式。

**6.15（⋆）** 考虑一个 $2\times2$ Gram 矩阵的行列式，证明正定核函数 $k(x,x')$ 满足 Cauchy–Schwartz 不等式

$$
k(x_1,x_2)^2\leqslant k(x_1,x_1)k(x_2,x_2).
\tag{6.96}
$$

**6.16（⋆⋆）** 考虑一个由参数向量 $\mathbf{w}$ 控制的参数模型，以及由输入值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 构成的数据集和非线性特征映射 $\boldsymbol{\phi}(\mathbf{x})$。假设误差函数对 $\mathbf{w}$ 的依赖具有如下形式：

$$
J(\mathbf{w})=f(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_1),\ldots,\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_N))+g(\mathbf{w}^{\mathrm T}\mathbf{w})
\tag{6.97}
$$

其中 $g(\cdot)$ 是单调递增函数。将 $\mathbf{w}$ 写成

$$
\mathbf{w}=\sum_{n=1}^{N}\alpha_n\boldsymbol{\phi}(\mathbf{x}_n)+\mathbf{w}_{\perp}
\tag{6.98}
$$

证明，使 $J(\mathbf{w})$ 最小的 $\mathbf{w}$，是基函数 $\boldsymbol{\phi}(\mathbf{x}_n)$（$n=1,\ldots,N$）的线性组合。

**6.17（⋆⋆）www** 考虑针对输入含噪声的数据的平方和误差函数（6.39），其中 $\nu(\boldsymbol{\xi})$ 是噪声分布。利用变分法，关于函数 $y(\mathbf{x})$ 最小化这个误差函数，从而证明最优解由（6.40）形式的展开给出，其中基函数由（6.41）给出。

<!-- pdf-page: 342 -->

**6.18（⋆）** 考虑一个具有单个输入变量 $x$ 和单个目标变量 $t$ 的 Nadaraya–Watson 模型，其高斯分量具有各向同性协方差，因此协方差矩阵为 $\sigma^2\mathbf{I}$，其中 $\mathbf{I}$ 为单位矩阵。用核函数 $k(x,x_n)$ 写出条件密度 $p(t\mid x)$、条件均值 $\mathbb{E}[t\mid x]$ 和方差 $\operatorname{var}[t\mid x]$ 的表达式。

**6.19（⋆⋆）** 核回归的另一种观点，来自输入变量和目标变量都受到加性噪声污染的回归问题。假设每个目标值 $t_n$ 都像通常一样生成：在点 $\mathbf{z}_n$ 处计算函数 $y(\mathbf{z}_n)$，再加入高斯噪声。不过，无法直接观测到 $\mathbf{z}_n$ 的值，只能观测到受噪声污染的版本 $\mathbf{x}_n=\mathbf{z}_n+\boldsymbol{\xi}_n$，其中随机变量 $\boldsymbol{\xi}$ 服从某个分布 $g(\boldsymbol{\xi})$。考虑一组观测 $\{\mathbf{x}_n,t_n\}$，其中 $n=1,\ldots,N$，以及通过对输入噪声分布取平均而定义的相应平方和误差函数：

$$
E=\frac{1}{2}\sum_{n=1}^{N}\int\{y(\mathbf{x}_n-\boldsymbol{\xi}_n)-t_n\}^2g(\boldsymbol{\xi}_n)\,d\boldsymbol{\xi}_n.
\tag{6.99}
$$

利用变分法（附录 D），关于函数 $y(\mathbf{z})$ 最小化 $E$，证明 $y(\mathbf{x})$ 的最优解由（6.45）形式的 Nadaraya–Watson 核回归解给出，其核具有（6.46）的形式。

**6.20（⋆⋆）www** 验证结果（6.66）和（6.67）。

**6.21（⋆⋆）www** 考虑一个高斯过程回归模型，其核函数由一组固定的非线性基函数定义。证明，它的预测分布与 3.3.2 节针对贝叶斯线性回归模型得到的结果（3.58）相同。为此，注意两个模型的预测分布都是高斯分布，因此只需证明条件均值和方差相同。对于均值，使用矩阵恒等式（C.6）；对于方差，使用矩阵恒等式（C.7）。

**6.22（⋆⋆）** 考虑一个回归问题，具有 $N$ 个训练集输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 和 $L$ 个测试集输入向量 $\mathbf{x}_{N+1},\ldots,\mathbf{x}_{N+L}$，并假设为函数 $t(\mathbf{x})$ 定义了一个高斯过程先验。给定 $t(\mathbf{x}_1),\ldots,t(\mathbf{x}_N)$ 的值，推导 $t(\mathbf{x}_{N+1}),\ldots,t(\mathbf{x}_{N+L})$ 的联合预测分布的表达式。证明，对于其中一个测试观测 $t_j$，其中 $N+1\leqslant j\leqslant N+L$，该分布的边缘分布由通常的高斯过程回归结果（6.66）和（6.67）给出。

**6.23（⋆⋆）www** 考虑一个高斯过程回归模型，其中目标变量 $\mathbf{t}$ 的维数为 $D$。给定由输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_{N+1}$ 和相应目标观测 $\mathbf{t}_1,\ldots,\mathbf{t}_N$ 构成的训练集，写出测试输入向量 $\mathbf{x}_{N+1}$ 对应的 $\mathbf{t}_{N+1}$ 的条件分布。

**6.24（⋆）** 证明，一个对角元素满足 $0<W_{ii}<1$ 的对角矩阵 $\mathbf{W}$ 是正定矩阵。证明，两个正定矩阵之和本身也是正定矩阵。

<!-- pdf-page: 343 -->

**6.25（⋆）www** 利用 Newton–Raphson 公式（4.92），推导用于寻找高斯过程分类模型中后验分布众数 $\mathbf{a}_N^{\star}$ 的迭代更新公式（6.83）。

**6.26（⋆）** 利用结果（2.115），推导高斯过程分类模型中后验分布 $p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 的均值和方差的表达式（6.87）和（6.88）。

**6.27（⋆⋆⋆）** 推导高斯过程分类的拉普拉斯近似框架中，对数似然函数的结果（6.90）。类似地，推导对数似然梯度各项的结果（6.91）、（6.92）和（6.94）。

<!-- pdf-page: 344 -->
