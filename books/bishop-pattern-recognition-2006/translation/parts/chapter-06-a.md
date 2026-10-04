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
