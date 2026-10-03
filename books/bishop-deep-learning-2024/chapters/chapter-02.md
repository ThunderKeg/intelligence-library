# 第 2 章 概率

<aside class="chapter-guide"><strong>本章导读</strong><p>机器学习必须处理不确定性。本章从筛查检测出发，介绍概率法则、贝叶斯定理、概率密度、期望与高斯分布；随后讨论变量变换、信息论和贝叶斯方法。这些概念为后续的模型训练与预测提供数学基础。</p></aside>

<!-- pdf-page: 43 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/chapter-art.jpeg" alt="本章开篇的彩色抽象图案">
</figure>

在几乎所有机器学习应用中，我们都必须处理不确定性。例如，把皮肤病变图像分类为良性或恶性的系统，在实践中不可能达到完全准确。我们可以区分两类不确定性。第一类是认知不确定性（epistemic uncertainty；词根来自意为“知识”的希腊语 *episteme*），有时也称为系统性不确定性。它之所以存在，是因为我们只能看到有限大小的数据集。随着我们观察到更多数据，例如更多良性和恶性皮肤病变的图像，我们就能更好地预测新样本的类别。然而，即使数据集无限大，我们仍然无法达到完全准确，因为还存在第二类不确定性，即偶然不确定性（aleatoric uncertainty），又称内在不确定性或随机不确定性，有时简称为噪声。一般来说，噪声源于我们只能观察到世界的部分信息，因此减少这类不确定性的一种方法是收集不同类型的数据。图 2.1 把第 1.2 节的正弦曲线示例扩展到二维，说明了这一点。

<!-- pdf-page: 44 -->

<figure id="fig-2-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-1.png" alt="二维正弦曲面，以及未观察与固定第二个输入变量时的两组散点图">
  <figcaption>图 2.1：把简单的正弦曲线回归问题扩展到二维。(a) 函数 $y(x_1,x_2)=\sin(2\pi x_1)\sin(2\pi x_2)$ 的图像。选取 $x_1$ 和 $x_2$ 的值，计算对应的 $y(x_1,x_2)$，再加入高斯噪声，即生成数据。(b) 未观测 $x_2$ 时的 100 个数据点，表现出较高的噪声水平。(c) 将 $x_2$ 固定为 $\pi/2$ 时的 100 个数据点，模拟除 $x_1$ 外还能测量 $x_2$ 的情况，噪声水平明显降低。</figcaption>
</figure>

举一个实际例子：与单独观察皮肤病变图像相比，病变部位的活检样本能提供多得多的信息，并可能大幅提高我们判断新病变是否为恶性的准确率。如果同时得到图像和活检数据，内在不确定性可能很小；再通过收集大型训练数据集，我们或许能把系统性不确定性也降到较低水平，从而高准确率地预测病变类别。

两类不确定性都可以用概率论的框架处理。概率论为量化和处理不确定性提供了统一的方法，因此是机器学习的核心基础之一。我们将看到，概率遵循两个简单的公式，称为加法法则和乘法法则。将这两条法则与决策理论结合，即使掌握的信息不完整或有歧义，原则上也能根据全部可用信息作出最优预测（见第 2.1 节和第 5.2 节）。

概率通常从可重复事件的频率来介绍。例如，考虑图 2.2 所示的弯曲硬币。假设它的形状使其经过大量抛掷后，有 60% 的次数凹面朝上，因此有 40% 的次数凸面朝上。我们说，凹面朝上的概率是 60%，即 0.6。严格来说，这里的概率由“试验”次数趋于无穷时的极限定义；在这个例子中，试验就是抛掷硬币。硬币落下后只能凹面朝上或凸面朝上，因此两种概率之和为 100%，即 1.0。用可重复事件的频率定义概率，是统计学频率学派观点的基础。

现在假设我们知道这枚硬币凹面朝上的概率是 0.6，却不能看硬币本身，也不知道哪一面是正面、哪一面是反面。

<!-- pdf-page: 45 -->

<figure id="fig-2-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-2.png" alt="弯曲硬币的凹面和凸面，朝上的频率分别为百分之六十与百分之四十">
  <figcaption>图 2.2：概率既可以看作可重复事件的频率，也可以用来量化不确定性。如正文所述，可以用一枚弯曲硬币说明二者的区别。</figcaption>
</figure>

如果有人问我们，抛出这枚硬币时正面朝上还是反面朝上，应该押哪一种结果，那么对称性表明，我们应按正面朝上的概率为 0.5 来下注。更仔细的分析也说明，在没有任何额外信息时，这确实是理性的选择。此处我们使用的概率概念比单纯的事件频率更一般。硬币凸面究竟是正面还是反面，本身不是一个可重复事件；我们只是尚不知道答案。把概率用于量化不确定性，是贝叶斯学派的观点。它更一般，因为它把频率概率包含为一个特例。若给出一系列抛币结果，我们可以运用贝叶斯推理，逐渐了解硬币的哪一面是正面（见第 2.6 节和习题 2.40）。观察到的结果越多，我们对正反面对应关系的不确定性就越小。

在非正式地引入概率概念之后，我们现在更详细地研究概率，并讨论如何定量运用它。本章其余部分建立的概念，将成为全书许多主题的核心基础。

## 2.1 概率法则

本节将推导两条支配概率行为的简单法则。尽管它们看起来很简单，却非常有力，而且适用范围很广。我们先用一个简单例子引出概率法则。

### 2.1.1 医学筛查示例

考虑对人群进行癌症筛查，以便及早发现癌症。假设其中有 1% 的人确实患癌。理想的癌症检测应该让每位患癌者得到阳性结果，让每位未患癌者得到阴性结果。但检测并不完美：假设未患癌者中有 3% 会检测出阳性，称为假阳性；患癌者中有 10% 会检测出阴性，称为假阴性。图 2.3 展示了这些错误率。

根据这些信息，我们可能会问：(1)“如果对人群进行筛查，一个人检测出阳性的概率是多少？”(2)“如果一个人的检测结果为阳性，他实际上患癌的概率是多少？”我们可以针对癌症筛查逐项计算，但这里先暂时放下这个具体例子，推导概率的一般法则，即概率的加法法则和乘法法则，再用它们回答这两个问题。

<!-- pdf-page: 46 -->

<figure id="fig-2-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-3.png" alt="每百名未患癌者中三名呈阳性，每百名患癌者中九十名呈阳性的示意图">
  <figcaption>图 2.3：癌症检测准确率示意。左侧表示未患癌者：每 100 名接受检测者平均有 3 人呈阳性。右侧表示患癌者：每 100 名接受检测者平均有 90 人呈阳性。</figcaption>
  <p class="figure-translation">图内文字：No Cancer → 未患癌；Cancer → 患癌。</p>
</figure>

### 2.1.2 加法法则和乘法法则

为推导概率法则，考虑图 2.4 所示的稍一般化的例子，其中有两个变量 $X$ 和 $Y$。在癌症示例中，$X$ 可以表示是否患癌，$Y$ 则可以表示检测结果。由于这些变量的取值因人而异，而且通常事先未知，所以称为随机变量（random variable 或 stochastic variable）。设 $X$ 可以取 $x_i$，其中 $i=1,\ldots,L$；$Y$ 可以取 $y_j$，其中 $j=1,\ldots,M$。考虑共 $N$ 次试验，每次都对 $X$ 和 $Y$ 取样。记同时满足 $X=x_i$ 和 $Y=y_j$ 的试验次数为 $n_{ij}$。另外，记 $X=x_i$ 的次数为 $c_i$（不论 $Y$ 取什么值），类似地记 $Y=y_j$ 的次数为 $r_j$。

$X$ 取 $x_i$ 且 $Y$ 取 $y_j$ 的概率写作 $p(X=x_i,Y=y_j)$，称为 $X=x_i$ 和 $Y=y_j$ 的联合概率（joint probability）。它等于落在第 $i,j$ 个格子中的点数占总点数的比例，因此

$$
p(X=x_i,Y=y_j)=\frac{n_{ij}}{N}. \tag{2.1}
$$

这里隐含考虑的是 $N\to\infty$ 的极限。类似地，$X$ 取 $x_i$ 而不考虑 $Y$ 取值的概率写作 $p(X=x_i)$，它等于第 $i$ 列点数占总点数的比例。

<!-- pdf-page: 47 -->

<figure id="fig-2-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-4.png" alt="按随机变量 X 与 Y 的取值划分的五列三行计数网格">
  <figcaption>图 2.4：用随机变量 $X$ 和 $Y$ 推导概率的加法法则与乘法法则。$X$ 的可能取值是 $\{x_i\}$，$i=1,\ldots,L$；$Y$ 的可能取值是 $\{y_j\}$，$j=1,\ldots,M$。图中 $L=5$、$M=3$。在共 $N$ 个变量实例中，$X=x_i$ 且 $Y=y_j$ 的实例数记为 $n_{ij}$，即网格中相应格子的实例数。与 $X=x_i$ 对应的第 $i$ 列实例数记为 $c_i$；与 $Y=y_j$ 对应的第 $j$ 行实例数记为 $r_j$。</figcaption>
</figure>

于是有

$$
p(X=x_i)=\frac{c_i}{N}. \tag{2.2}
$$

因为 $\sum_i c_i=N$，所以

$$
\sum_{i=1}^{L}p(X=x_i)=1, \tag{2.3}
$$

可见概率之和确实为 1。在图 2.4 中，第 $i$ 列的实例数等于该列各格的实例数之和，即 $c_i=\sum_j n_{ij}$。由式 (2.1) 和 (2.2) 可得

$$
p(X=x_i)=\sum_{j=1}^{M}p(X=x_i,Y=y_j), \tag{2.4}
$$

这就是概率的加法法则。注意，$p(X=x_i)$ 有时称为边缘概率（marginal probability），它通过将其他变量（这里是 $Y$）边缘化，即求和消去而得到。

如果只考虑 $X=x_i$ 的实例，那么其中满足 $Y=y_j$ 的实例所占的比例写作 $p(Y=y_j\mid X=x_i)$，称为给定 $X=x_i$ 时 $Y=y_j$ 的条件概率（conditional probability）。它等于第 $i$ 列中落在第 $i,j$ 个格子的点数比例，因此

$$
p(Y=y_j\mid X=x_i)=\frac{n_{ij}}{c_i}. \tag{2.5}
$$

对等式两边关于 $j$ 求和，并利用 $\sum_j n_{ij}=c_i$，得到

$$
\sum_{j=1}^{M}p(Y=y_j\mid X=x_i)=1, \tag{2.6}
$$

<!-- pdf-page: 48 -->

说明条件概率也正确地归一化了。由式 (2.1)、(2.2) 和 (2.5)，又可推导出

$$
\begin{aligned}
p(X=x_i,Y=y_j)&=\frac{n_{ij}}{N}=\frac{n_{ij}}{c_i}\cdot\frac{c_i}{N}\\
&=p(Y=y_j\mid X=x_i)p(X=x_i),
\end{aligned} \tag{2.7}
$$

这就是概率的乘法法则。

到目前为止，我们一直小心区分随机变量（如 $X$）与它可能取到的值（如 $x_i$）。因此，$X$ 取 $x_i$ 的概率记为 $p(X=x_i)$。虽然这样可以避免歧义，但记号显得繁琐，而且很多时候没有必要如此严格。只要上下文足够清楚，我们也可以简单地用 $p(X)$ 表示随机变量 $X$ 上的概率分布，用 $p(x_i)$ 表示该分布在具体取值 $x_i$ 处的值。

采用这种更简洁的记号，概率论的两条基本法则可写为

$$
\text{加法法则}\qquad p(X)=\sum_Y p(X,Y), \tag{2.8}
$$

$$
\text{乘法法则}\qquad p(X,Y)=p(Y\mid X)p(X). \tag{2.9}
$$

其中，$p(X,Y)$ 是联合概率，读作“$X$ 和 $Y$ 的概率”；$p(Y\mid X)$ 是条件概率，读作“给定 $X$ 时 $Y$ 的概率”；$p(X)$ 是边缘概率，读作“$X$ 的概率”。这两条简单的法则，是本书其余部分所用全部概率方法的基础。

### 2.1.3 贝叶斯定理

利用乘法法则及对称性 $p(X,Y)=p(Y,X)$，立即得到两个条件概率之间的关系：

$$
p(Y\mid X)=\frac{p(X\mid Y)p(Y)}{p(X)}. \tag{2.10}
$$

这称为贝叶斯定理（Bayes’ theorem），在机器学习中发挥重要作用。注意，它把等式左边的条件分布 $p(Y\mid X)$ 与右边“反向”的条件分布 $p(X\mid Y)$ 联系起来。利用加法法则，贝叶斯定理中的分母可以用分子中出现的量表示：

$$
p(X)=\sum_Y p(X\mid Y)p(Y). \tag{2.11}
$$

因此，可以把贝叶斯定理中的分母看作归一化常数：它使式 (2.10) 左侧的条件概率分布对 $Y$ 的所有取值求和后等于 1。

<!-- pdf-page: 49 -->

<figure id="fig-2-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-5.png" alt="两个离散变量的联合分布散点图，以及对应的边缘和条件分布直方图">
  <figcaption>图 2.5：两个变量上的分布示例：$X$ 有 9 个可能取值，$Y$ 有 2 个可能取值。左上图是从这两个变量的联合概率分布中抽取的 60 个点。其余图分别给出边缘分布 $p(X)$、$p(Y)$，以及对应于左上图底行的条件分布 $p(X\mid Y=1)$ 的直方图估计。</figcaption>
</figure>

图 2.5 用一个涉及两个变量的联合分布的简单例子，说明边缘分布和条件分布。左上图显示从联合分布抽取的有限样本，共 $N=60$ 个数据点。右上图是具有 $Y$ 两种取值的数据点比例的直方图。按照概率的定义，当样本量 $N\to\infty$ 时，这些比例就等于相应的概率 $p(Y)$。对于只知道从某分布抽出的有限个点的情况，直方图可以看作建立概率分布模型的一种简单方法（见第 3.5.1 节）。图 2.5 余下两幅图分别给出 $p(X)$ 和 $p(X\mid Y=1)$ 的直方图估计。

<!-- pdf-page: 50 -->

### 2.1.4 再看医学筛查

现在回到癌症筛查示例，运用概率的加法法则和乘法法则回答前面的两个问题。为使推导清楚，我们再次明确区分随机变量及其具体取值。用变量 $C$ 表示是否患癌：$C=0$ 表示“未患癌”，$C=1$ 表示“患癌”。根据假设，人群中每 100 人有 1 人患癌，因此分别有

$$
p(C=1)=\frac{1}{100}, \tag{2.12}
$$

$$
p(C=0)=\frac{99}{100}. \tag{2.13}
$$

注意，它们满足 $p(C=0)+p(C=1)=1$。

再引入第二个随机变量 $T$ 表示筛查结果：$T=1$ 是提示可能患癌的阳性结果，$T=0$ 是提示可能未患癌的阴性结果。如图 2.3 所示，已知患癌者中检测呈阳性的概率是 90%，而未患癌者中检测呈阳性的概率是 3%。因此，四个条件概率可以全部写出：

$$
p(T=1\mid C=1)=\frac{90}{100}, \tag{2.14}
$$

$$
p(T=0\mid C=1)=\frac{10}{100}, \tag{2.15}
$$

$$
p(T=1\mid C=0)=\frac{3}{100}, \tag{2.16}
$$

$$
p(T=0\mid C=0)=\frac{97}{100}. \tag{2.17}
$$

同样注意，这些概率已归一化，因此

$$
p(T=1\mid C=1)+p(T=0\mid C=1)=1, \tag{2.18}
$$

类似地，

$$
p(T=1\mid C=0)+p(T=0\mid C=0)=1. \tag{2.19}
$$

现在运用概率的加法法则和乘法法则回答第一个问题，计算随机抽取一人接受检测时，检测结果为阳性的总体概率：

$$
\begin{aligned}
p(T=1)&=p(T=1\mid C=0)p(C=0)+p(T=1\mid C=1)p(C=1)\\
&=\frac{3}{100}\times\frac{99}{100}+\frac{90}{100}\times\frac{1}{100}
=\frac{387}{10\,000}=0.0387.
\end{aligned} \tag{2.20}
$$

可以看到，随机抽取一人接受检测，结果为阳性的概率约为 4%，而此人实际患癌的概率为 1%。由加法法则还可得 $p(T=0)=1-387/10\,000=9613/10\,000=0.9613$，因此检测结果为阴性的概率约为 96%。

接着考虑第二个问题，也是接受筛查的人特别关心的问题：如果检测结果为阳性，此人患癌的概率是多少？

<!-- pdf-page: 51 -->

这要求我们计算给定检测结果后患癌的条件概率，而式 (2.14) 至 (2.17) 给出的是给定是否患癌后检测结果的概率分布。用贝叶斯定理 (2.10) 可以反转条件方向：

$$
p(C=1\mid T=1)=\frac{p(T=1\mid C=1)p(C=1)}{p(T=1)}, \tag{2.21}
$$

$$
=\frac{90}{100}\times\frac{1}{100}\times\frac{10\,000}{387}
=\frac{90}{387}\simeq 0.23. \tag{2.22}
$$

所以，若随机抽取一人接受检测且结果为阳性，此人实际患癌的概率为 23%。同样由加法法则，$p(C=0\mid T=1)=1-90/387=297/387\simeq 0.77$，即此人未患癌的概率为 77%。

### 2.1.5 先验概率与后验概率

癌症筛查示例还提供了对贝叶斯定理的一种重要解释。如果在某人接受检测之前，问他是否可能患癌，那么我们掌握的最完整信息就是概率 $p(C)$。它称为先验概率（prior probability），因为它是在观察检测结果之前可用的概率。一旦得知此人检测呈阳性，就可以利用贝叶斯定理计算 $p(C\mid T)$。它称为后验概率（posterior probability），因为它是在观察到检测结果 $T$ 之后得到的概率。

在这个例子中，患癌的先验概率为 1%。但观察到检测呈阳性后，患癌的后验概率为 23%，明显更高，也符合直觉。不过，即使检测结果看起来相当“准确”（见图 2.3），呈阳性的人实际患癌的概率仍然只有 23%。许多人会觉得这个结论违反直觉（见习题 2.1）。原因在于患癌的先验概率很低。虽然阳性结果为患癌提供了有力证据，但仍必须通过贝叶斯定理把这份证据与先验概率结合，才能得到正确的后验概率。

### 2.1.6 独立变量

最后，如果两个变量的联合分布可以分解为各自边缘分布的乘积，即 $p(X,Y)=p(X)p(Y)$，就称 $X$ 与 $Y$ 相互独立。连续抛掷一枚硬币就是独立事件的例子。根据乘法法则，此时 $p(Y\mid X)=p(Y)$，所以给定 $X$ 后，$Y$ 的条件分布确实不依赖于 $X$ 的取值。在癌症筛查示例中，如果检测呈阳性的概率与此人是否患癌无关，那么 $p(T\mid C)=p(T)$。由贝叶斯定理 (2.10) 得 $p(C\mid T)=p(C)$，也就是说观察检测结果不会改变患癌的概率。这样的检测当然毫无用处，因为结果不提供任何关于此人是否患癌的信息。

<!-- pdf-page: 52 -->

<figure id="fig-2-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-6.png" alt="连续变量的概率密度曲线与累积分布函数曲线，标出宽度为 delta x 的小区间">
  <figcaption>图 2.6：离散变量的概率概念可推广为连续变量 $x$ 上的概率密度 $p(x)$：当 $\delta x\to0$ 时，$x$ 落在区间 $(x,x+\delta x)$ 内的概率为 $p(x)\delta x$。概率密度可表示为累积分布函数 $P(x)$ 的导数。</figcaption>
</figure>

## 2.2 概率密度

除了定义在离散取值集合上的概率，我们也需要考虑连续变量上的概率。例如，我们可能要预测给病人使用多大剂量的药物。由于这种预测存在不确定性，我们希望把不确定性量化，而概率仍可用于此。但不能直接套用前面讨论的概率概念，因为以无限精度观测到连续变量某个特定数值的概率实际上为零。因此，需要引入概率密度（probability density）的概念。这里我们只作相对非正式的讨论。

对于连续变量 $x$，定义概率密度 $p(x)$，使得在 $\delta x\to0$ 时，$x$ 落在区间 $(x,x+\delta x)$ 内的概率为 $p(x)\delta x$，如图 2.6 所示。于是，$x$ 落在区间 $(a,b)$ 内的概率是

$$
p\bigl(x\in(a,b)\bigr)=\int_a^b p(x)\,\mathrm dx. \tag{2.23}
$$

由于概率非负，而且 $x$ 必然位于实数轴的某处，概率密度 $p(x)$ 必须满足两个条件：

$$
p(x)\geqslant0, \tag{2.24}
$$

$$
\int_{-\infty}^{\infty}p(x)\,\mathrm dx=1. \tag{2.25}
$$

$x$ 落在区间 $(-\infty,z)$ 内的概率由累积分布函数（cumulative distribution function）给出，定义为

$$
P(z)=\int_{-\infty}^{z}p(x)\,\mathrm dx, \tag{2.26}
$$

<!-- pdf-page: 53 -->

它满足 $P'(x)=p(x)$，如图 2.6 所示。

如果有多个连续变量 $x_1,\ldots,x_D$，合在一起记作向量 $\mathbf{x}$，就可以定义联合概率密度 $p(\mathbf{x})=p(x_1,\ldots,x_D)$，使得 $\mathbf{x}$ 落在包含点 $\mathbf{x}$ 的无穷小体积 $\delta\mathbf{x}$ 中的概率为 $p(\mathbf{x})\delta\mathbf{x}$。这个多变量概率密度必须满足

$$
p(\mathbf{x})\geqslant0, \tag{2.27}
$$

$$
\int p(\mathbf{x})\,\mathrm d\mathbf{x}=1, \tag{2.28}
$$

其中积分遍及整个 $\mathbf{x}$ 空间。更一般地，还可以考虑同时包含离散变量和连续变量的联合概率分布。

概率的加法法则、乘法法则和贝叶斯定理同样适用于概率密度，也适用于离散变量与连续变量的组合。若 $x$ 和 $y$ 是两个实变量，加法法则与乘法法则分别写成

$$
\text{加法法则}\qquad p(x)=\int p(x,y)\,\mathrm dy, \tag{2.29}
$$

$$
\text{乘法法则}\qquad p(x,y)=p(y\mid x)p(x). \tag{2.30}
$$

类似地，贝叶斯定理可写成

$$
p(y\mid x)=\frac{p(x\mid y)p(y)}{p(x)}, \tag{2.31}
$$

其中分母为

$$
p(x)=\int p(x\mid y)p(y)\,\mathrm dy. \tag{2.32}
$$

对连续变量严格证明加法法则和乘法法则，需要用到称为测度论的数学分支（Feller，1966），这超出了本书的范围。不过，我们可以用非正式的方法看出它们为何成立：把每个实变量划分为宽度为 $\Delta$ 的区间，考虑这些区间上的离散概率分布；再令 $\Delta\to0$，求和就变成积分，从而得到上述结果。

### 2.2.1 分布示例

有许多概率密度形式被广泛使用。它们本身很重要，也可作为构造更复杂概率模型的组成部分。最简单的形式是 $p(x)$ 为与 $x$ 无关的常数，但这种形式无法归一化，因为式 (2.28) 中的积分会发散。不能归一化的分布称为非正规分布（improper distribution）。不过，可以构造在有限区间（例如 $(c,d)$）内为常数、在区间外为零的均匀分布（uniform distribution）。此时由式 (2.28) 得

$$
p(x)=\frac{1}{d-c},\qquad x\in(c,d). \tag{2.33}
$$

<!-- pdf-page: 54 -->

<figure id="fig-2-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-7.png" alt="均匀分布、指数分布和拉普拉斯分布的三条概率密度曲线">
  <figcaption>图 2.7：红色曲线为区间 $(-1,1)$ 上的均匀分布，蓝色曲线为 $\lambda=1$ 的指数分布，绿色曲线为 $\mu=1$、$\gamma=1$ 的拉普拉斯分布。</figcaption>
</figure>

另一种简单的概率密度是指数分布（exponential distribution）：

$$
p(x\mid\lambda)=\lambda\exp(-\lambda x),\qquad x\geqslant0. \tag{2.34}
$$

指数分布的一种变体称为拉普拉斯分布（Laplace distribution）。它允许把峰值移到位置 $\mu$，形式为

$$
p(x\mid\mu,\gamma)=\frac{1}{2\gamma}\exp\!\left(-\frac{|x-\mu|}{\gamma}\right). \tag{2.35}
$$

图 2.7 展示了均匀分布、指数分布和拉普拉斯分布。

另一个重要的分布是狄拉克 delta 函数（Dirac delta function），写作

$$
p(x\mid\mu)=\delta(x-\mu). \tag{2.36}
$$

它在 $x=\mu$ 以外的所有位置都定义为零，并且具有按式 (2.28) 积分等于 1 的性质。非正式地说，可以把它看成位于 $x=\mu$ 的一根无限窄、无限高的尖峰，其面积为 1。最后，若有 $x$ 的有限个观测值 $\mathcal D=\{x_1,\ldots,x_N\}$，就可以用 delta 函数构造经验分布（empirical distribution）：

$$
p(x\mid\mathcal D)=\frac{1}{N}\sum_{n=1}^{N}\delta(x-x_n), \tag{2.37}
$$

也就是在每个数据点处各放置一个狄拉克 delta 函数。式 (2.37) 定义的概率密度按要求积分为 1（见习题 2.6）。

### 2.2.2 期望与协方差

涉及概率的最重要运算之一，是求函数的加权平均。函数 $f(x)$ 在概率分布 $p(x)$ 下的加权平均称为 $f(x)$ 的期望（expectation），记作 $\mathbb E[f]$。对于离散分布，它通过对 $x$ 的所有可能取值求和得到：

$$
\mathbb E[f]=\sum_x p(x)f(x), \tag{2.38}
$$

<!-- pdf-page: 55 -->

其中不同取值的相对概率决定了平均时各自的权重。对于连续变量，期望表示为对相应概率密度积分：

$$
\mathbb E[f]=\int p(x)f(x)\,\mathrm dx. \tag{2.39}
$$

在这两种情况下，如果从概率分布或概率密度中抽取了有限的 $N$ 个点，就可以用这些点上的有限求和来近似期望（见习题 2.7）：

$$
\mathbb E[f]\simeq\frac{1}{N}\sum_{n=1}^{N}f(x_n). \tag{2.40}
$$

当 $N\to\infty$ 时，式 (2.40) 中的近似变为精确结果。

有时我们考虑多个变量的函数的期望，可以用下标标明对哪个变量取平均。例如，

$$
\mathbb E_x[f(x,y)] \tag{2.41}
$$

表示函数 $f(x,y)$ 关于 $x$ 的分布取平均。注意，$\mathbb E_x[f(x,y)]$ 是 $y$ 的函数。

我们还可以考虑相对于条件分布的条件期望，例如

$$
\mathbb E_x[f\mid y]=\sum_x p(x\mid y)f(x), \tag{2.42}
$$

它也是 $y$ 的函数。对于连续变量，条件期望写作

$$
\mathbb E_x[f\mid y]=\int p(x\mid y)f(x)\,\mathrm dx. \tag{2.43}
$$

$f(x)$ 的方差定义为

$$
\operatorname{var}[f]=\mathbb E\!\left[(f(x)-\mathbb E[f(x)])^2\right], \tag{2.44}
$$

它衡量 $f(x)$ 围绕其均值 $\mathbb E[f(x)]$ 的变化程度。展开平方项，可将方差写成 $f(x)$ 与 $f(x)^2$ 的期望之差（见习题 2.8）：

$$
\operatorname{var}[f]=\mathbb E[f(x)^2]-\mathbb E[f(x)]^2. \tag{2.45}
$$

特别地，变量 $x$ 本身的方差为

$$
\operatorname{var}[x]=\mathbb E[x^2]-\mathbb E[x]^2. \tag{2.46}
$$

对于两个随机变量 $x$ 和 $y$，协方差（covariance）衡量它们共同变化的程度，定义为

$$
\begin{aligned}
\operatorname{cov}[x,y]&=\mathbb E_{x,y}\!\left[\{x-\mathbb E[x]\}\{y-\mathbb E[y]\}\right]\\
&=\mathbb E_{x,y}[xy]-\mathbb E[x]\mathbb E[y].
\end{aligned} \tag{2.47}
$$

<!-- pdf-page: 56 -->

<figure id="fig-2-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-8.png" alt="标出均值 mu 和两倍标准差宽度的单变量高斯分布曲线">
  <figcaption>图 2.8：单个连续变量 $x$ 的高斯分布曲线，标出了均值 $\mu$ 和标准差 $\sigma$。</figcaption>
</figure>

如果 $x$ 和 $y$ 相互独立，它们的协方差等于零（见习题 2.9）。

对于两个向量 $\mathbf{x}$ 和 $\mathbf{y}$，它们的协方差是矩阵：

$$
\begin{aligned}
\operatorname{cov}[\mathbf{x},\mathbf{y}]
&=\mathbb E_{\mathbf{x},\mathbf{y}}\!\left[\{\mathbf{x}-\mathbb E[\mathbf{x}]\}\{\mathbf{y}^{\mathsf T}-\mathbb E[\mathbf{y}^{\mathsf T}]\}\right]\\
&=\mathbb E_{\mathbf{x},\mathbf{y}}[\mathbf{x}\mathbf{y}^{\mathsf T}]
-\mathbb E[\mathbf{x}]\mathbb E[\mathbf{y}^{\mathsf T}].
\end{aligned} \tag{2.48}
$$

如果考察向量 $\mathbf{x}$ 各分量之间的协方差，我们使用稍简洁的记号 $\operatorname{cov}[\mathbf{x}]\equiv\operatorname{cov}[\mathbf{x},\mathbf{x}]$。

## 2.3 高斯分布

连续变量最重要的概率分布之一是正态分布（normal distribution），也称高斯分布（Gaussian distribution）。本书后面的内容会大量使用它。对于单个实值变量 $x$，高斯分布定义为

$$
\mathcal N(x\mid\mu,\sigma^2)
=\frac{1}{(2\pi\sigma^2)^{1/2}}
\exp\!\left\{-\frac{1}{2\sigma^2}(x-\mu)^2\right\}. \tag{2.49}
$$

它是 $x$ 上的概率密度，由两个参数控制：$\mu$ 称为均值（mean），$\sigma^2$ 称为方差（variance）。方差的平方根 $\sigma$ 称为标准差（standard deviation），方差的倒数 $\beta=1/\sigma^2$ 称为精度（precision）。稍后我们会看到这一术语的由来。图 2.8 给出了高斯分布的曲线。虽然高斯分布的形式看起来可能有些随意，但后面会看到，它会从最大熵概念和中心极限定理的角度自然出现（见第 2.5.4 节和第 3.2 节）。

由式 (2.49) 可见，高斯分布满足

$$
\mathcal N(x\mid\mu,\sigma^2)>0. \tag{2.50}
$$

<!-- pdf-page: 57 -->

此外，不难证明高斯分布已经归一化（见习题 2.12）：

$$
\int_{-\infty}^{\infty}\mathcal N(x\mid\mu,\sigma^2)\,\mathrm dx=1. \tag{2.51}
$$

因此，式 (2.49) 满足有效概率密度的两个条件。

### 2.3.1 均值与方差

在高斯分布下，不难求出 $x$ 的函数的期望。特别是，$x$ 的平均值为（见习题 2.13）

$$
\mathbb E[x]=\int_{-\infty}^{\infty}\mathcal N(x\mid\mu,\sigma^2)x\,\mathrm dx=\mu. \tag{2.52}
$$

因为参数 $\mu$ 是该分布下 $x$ 的平均值，所以称为均值。式 (2.52) 中的积分称为分布的一阶矩（first-order moment），因为它是 $x$ 的一次幂的期望。类似地，二阶矩为

$$
\mathbb E[x^2]=\int_{-\infty}^{\infty}\mathcal N(x\mid\mu,\sigma^2)x^2\,\mathrm dx
=\mu^2+\sigma^2. \tag{2.53}
$$

由式 (2.52) 和 (2.53) 可得 $x$ 的方差：

$$
\operatorname{var}[x]=\mathbb E[x^2]-\mathbb E[x]^2=\sigma^2. \tag{2.54}
$$

因此 $\sigma^2$ 称为方差参数。分布的最大值所在位置称为众数（mode）；对于高斯分布，众数与均值重合（见习题 2.14）。

### 2.3.2 似然函数

假设有一个观测数据集，表示为行向量 $\boldsymbol{x}=(x_1,\ldots,x_N)$，包含标量变量 $x$ 的 $N$ 个观测值。注意，我们用粗体 $\boldsymbol{x}$ 区分这组观测值和一个 $D$ 维向量变量的单次观测；后者表示为列向量 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathsf T}$。设各观测值独立抽自一个均值 $\mu$ 和方差 $\sigma^2$ 都未知的高斯分布，我们希望根据数据集确定这些参数。根据有限的观测值估计一个分布，称为密度估计（density estimation）。必须强调，密度估计本质上是一个不适定问题，因为可能产生这组有限数据的概率分布有无限多种。事实上，任何在每个数据点 $x_1,\ldots,x_N$ 处都不为零的分布 $p(x)$，都有可能是候选分布。这里我们把候选范围限制为高斯分布，于是得到一个有明确解的问题。

从同一个分布中彼此独立抽取的数据点，称为独立同分布（independent and identically distributed），通常缩写为 i.i.d. 或 IID。我们已经看到，两个独立事件的联合概率等于各自边缘概率的乘积。由于数据集

<!-- pdf-page: 58 -->

<!-- join-previous-paragraph -->

$\boldsymbol{x}$ 独立同分布，所以在给定 $\mu$ 和 $\sigma^2$ 时，数据集的概率可写为

$$
p(\boldsymbol{x}\mid\mu,\sigma^2)
=\prod_{n=1}^{N}\mathcal N(x_n\mid\mu,\sigma^2). \tag{2.55}
$$

<figure id="fig-2-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-9.png" alt="高斯曲线上的样本点与似然乘积的示意图">
  <figcaption>图 2.9：高斯分布似然函数的示意。红色曲线是高斯分布，灰色点是一组数据 $\{x_n\}$；式 (2.55) 的似然函数，是蓝色点所表示的相应 $p(x)$ 值的乘积。极大化似然，就是调整高斯分布的均值与方差，使这一乘积最大。</figcaption>
</figure>

将它视为 $\mu$ 和 $\sigma^2$ 的函数时，就称为高斯分布的似然函数（likelihood function）。图 2.9 给出了图解。

利用观测数据集确定概率分布参数的一种常用方法，称为极大似然（maximum likelihood）：选择使似然函数最大的参数值。这个准则或许显得奇怪，因为根据前面对概率论的讨论，最大化“给定数据时参数的概率”，似乎比最大化“给定参数时数据的概率”更自然。事实上，这两种准则之间有联系（见第 2.6.2 节）。

不过这里先通过最大化似然函数 (2.55)，确定高斯分布中未知参数 $\mu$ 和 $\sigma^2$ 的值。在实践中，最大化似然函数的对数更方便。对数函数随自变量单调递增，因此最大化函数的对数与最大化函数本身是等价的。取对数不仅能简化后面的数学分析，也有助于数值计算：大量很小的概率相乘，很容易小到超出计算机数值精度的表示范围；改为计算对数概率之和就能避免这种下溢。根据式 (2.49) 和 (2.55)，对数似然函数为

$$
\ln p(\boldsymbol{x}\mid\mu,\sigma^2)
=-\frac{1}{2\sigma^2}\sum_{n=1}^{N}(x_n-\mu)^2
-\frac{N}{2}\ln\sigma^2-\frac{N}{2}\ln(2\pi). \tag{2.56}
$$

对 $\mu$ 最大化式 (2.56)，得到极大似然解（见习题 2.15）：

$$
\mu_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}x_n, \tag{2.57}
$$

<!-- pdf-page: 59 -->

它就是样本均值，即观测值 $\{x_n\}$ 的均值。类似地，对 $\sigma^2$ 最大化式 (2.56)，得到方差的极大似然解：

$$
\sigma^2_{\mathrm{ML}}
=\frac{1}{N}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2, \tag{2.58}
$$

即相对于样本均值 $\mu_{\mathrm{ML}}$ 计算的样本方差。注意，我们实际上是对 $\mu$ 和 $\sigma^2$ 联合最大化式 (2.56)，但对于高斯分布，$\mu$ 的解与 $\sigma^2$ 的解可以分开求：先计算式 (2.57)，再用它计算式 (2.58)。

### 2.3.3 极大似然的偏差

极大似然方法在深度学习中被广泛使用，也是多数机器学习算法的基础。不过，它也有局限性，可以用单变量高斯分布来说明。

首先注意，极大似然解 $\mu_{\mathrm{ML}}$ 和 $\sigma^2_{\mathrm{ML}}$ 都是数据集取值 $x_1,\ldots,x_N$ 的函数。假设每个取值都独立地从一个真实参数为 $\mu$ 和 $\sigma^2$ 的高斯分布中生成。现在，考虑 $\mu_{\mathrm{ML}}$ 和 $\sigma^2_{\mathrm{ML}}$ 对数据集取值的期望。不难证明（见习题 2.16）：

$$
\mathbb E[\mu_{\mathrm{ML}}]=\mu, \tag{2.59}
$$

$$
\mathbb E[\sigma^2_{\mathrm{ML}}]=\left(\frac{N-1}{N}\right)\sigma^2. \tag{2.60}
$$

可见，当对固定大小的多个数据集取平均时，均值的极大似然解等于真实均值；而方差的极大似然估计平均只有真实方差的 $(N-1)/N$。这是偏差（bias）的一个例子：对随机量的估计量会系统性地偏离真实值。图 2.10 给出了这一结果背后的直观解释。

偏差产生的原因在于，方差是相对于均值的极大似然估计来测量的，而这个均值估计本身也根据数据作了调整。假如我们能知道真实均值 $\mu$，并用它构造下面的方差估计量：

$$
\widehat{\sigma}^{2}=\frac{1}{N}\sum_{n=1}^{N}(x_n-\mu)^2, \tag{2.61}
$$

那么就会得到（见习题 2.17）

$$
\mathbb E[\widehat{\sigma}^{2}]=\sigma^2, \tag{2.62}
$$

这是无偏的。当然，我们不知道真实均值，只知道观测数据。根据式 (2.60)，对于高斯分布，以下方差参数估计是无偏的：

$$
\widetilde{\sigma}^{2}
=\frac{N}{N-1}\sigma^2_{\mathrm{ML}}
=\frac{1}{N-1}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2. \tag{2.63}
$$

<!-- pdf-page: 60 -->

<figure id="fig-2-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-10.png" alt="三组各有两个数据点的样本拟合高斯分布，展示极大似然方差偏小">
  <figcaption>图 2.10：用极大似然估计高斯分布的均值和方差时，偏差如何出现。红色曲线是真实的高斯分布，绿色点表示三个数据集中的数据点，每个数据集各有两个点；蓝色曲线是分别用式 (2.57) 和 (2.58) 拟合这些数据集得到的高斯分布。对三个数据集取平均，均值是正确的，但方差被系统性低估，因为方差是相对于样本均值而非真实均值测量的。</figcaption>
</figure>

不过，在神经网络这类复杂模型中，纠正极大似然的偏差并不那么容易。

注意，随着数据点数 $N$ 增加，极大似然解的偏差会越来越不明显。当 $N\to\infty$ 时，方差的极大似然解等于生成数据的分布的真实方差。对于高斯分布，只要 $N$ 不太小，这种偏差就不会造成严重问题。然而，本书始终关注含有大量参数的复杂模型；在这些模型中，与极大似然相关的偏差问题会严重得多。事实上，极大似然中的偏差问题与过拟合问题密切相关（见第 2.6.3 节）。

### 2.3.4 线性回归

我们已经看到，线性回归问题可以表示为误差最小化（见第 1.2 节）。现在回到这个例子，从概率角度重新考察它，以加深对误差函数和正则化的理解。

回归问题的目标是：利用由 $N$ 个输入值 $\boldsymbol{x}=(x_1,\ldots,x_N)$ 和对应目标值 $\boldsymbol{t}=(t_1,\ldots,t_N)$ 组成的训练数据，在给定一个新的输入值 $x$ 时预测目标变量 $t$。可以用概率分布表示对目标值的不确定性。为此，我们假设给定 $x$ 后，相应的 $t$ 服从高斯分布，其均值等于式 (1.1) 中多项式曲线的值 $y(x,\mathbf{w})$，其中 $\mathbf{w}$ 是多项式系数；方差为 $\sigma^2$。因此，

$$
p(t\mid x,\mathbf{w},\sigma^2)
=\mathcal N\bigl(t\mid y(x,\mathbf{w}),\sigma^2\bigr). \tag{2.64}
$$

图 2.11 给出了示意。现在用训练数据 $\{\boldsymbol{x},\boldsymbol{t}\}$，通过极大似然确定未知参数 $\mathbf{w}$ 和 $\sigma^2$。若假设数据独立地从分布 (2.64) 中抽取，则似然函数为

<!-- pdf-page: 61 -->

$$
p(\boldsymbol{t}\mid\boldsymbol{x},\mathbf{w},\sigma^2)
=\prod_{n=1}^{N}\mathcal N\bigl(t_n\mid y(x_n,\mathbf{w}),\sigma^2\bigr). \tag{2.65}
$$

<figure id="fig-2-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-11.png" alt="多项式回归曲线和给定输入 x 时目标 t 的条件高斯分布示意图">
  <figcaption>图 2.11：式 (2.64) 定义的给定 $x$ 时 $t$ 的高斯条件分布示意图。其中，均值由多项式函数 $y(x,\mathbf{w})$ 给出，方差由参数 $\sigma^2$ 给出。</figcaption>
</figure>

和前面处理简单高斯分布时一样，最大化似然函数的对数更方便。将式 (2.49) 给出的高斯分布代入，得到对数似然函数：

$$
\ln p(\boldsymbol{t}\mid\boldsymbol{x},\mathbf{w},\sigma^2)
=-\frac{1}{2\sigma^2}\sum_{n=1}^{N}\{y(x_n,\mathbf{w})-t_n\}^2
-\frac{N}{2}\ln\sigma^2-\frac{N}{2}\ln(2\pi). \tag{2.66}
$$

先考虑多项式系数的极大似然解，记作 $\mathbf{w}_{\mathrm{ML}}$。它通过对 $\mathbf{w}$ 最大化式 (2.66) 得到。为此，可以略去等式右边最后两项，因为它们不依赖于 $\mathbf{w}$。此外，把对数似然乘以一个正常数不会改变关于 $\mathbf{w}$ 的最大值位置，因此可以把系数 $1/(2\sigma^2)$ 换成 $1/2$。最后，最大化对数似然等价于最小化负对数似然。于是，对于确定 $\mathbf{w}$ 而言，最大化似然等价于最小化以下平方和误差函数：

$$
E(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{y(x_n,\mathbf{w})-t_n\}^2. \tag{2.67}
$$

因此，平方和误差函数是从高斯噪声分布的假设下最大化似然得到的。

<!-- pdf-page: 62 -->

我们也可以用极大似然法确定方差参数 $\sigma^2$。对式 (2.66) 关于 $\sigma^2$ 最大化，可得（见习题 2.18）

$$
\sigma^2_{\mathrm{ML}}=\frac{1}{N}\sum_{n=1}^{N}\bigl\{y(x_n,\mathbf{w}_{\mathrm{ML}})-t_n\bigr\}^2.\tag{2.68}
$$

注意，我们可以先确定控制均值的参数向量 $\mathbf{w}_{\mathrm{ML}}$，再用它求出方差 $\sigma^2_{\mathrm{ML}}$，这与简单高斯分布的情形相同。

确定参数 $\mathbf{w}$ 和 $\sigma^2$ 后，就可以对新的 $x$ 值作预测。现在模型是概率模型，因此预测由 $t$ 的**预测分布**表示，而不只是一个点估计。把极大似然参数代入式 (2.64)，得到

$$
p(t\mid x,\mathbf{w}_{\mathrm{ML}},\sigma^2_{\mathrm{ML}})
=\mathcal{N}\bigl(t\mid y(x,\mathbf{w}_{\mathrm{ML}}),\sigma^2_{\mathrm{ML}}\bigr).\tag{2.69}
$$

## 2.4 概率密度的变换

现在讨论概率密度在非线性变量变换下如何变化。我们在第 18 章讨论一类称为**归一化流**（normalizing flows）的生成模型时，这一性质将起关键作用。它也说明，概率密度在这种变换下的行为不同于普通函数。

考虑单个变量 $x$，并设变量变换为 $x=g(y)$。函数 $f(x)$ 会变成一个由下式定义的新函数 $\widetilde f(y)$：

$$
\widetilde f(y)=f(g(y)).\tag{2.70}
$$

再考虑概率密度 $p_x(x)$。同样按 $x=g(y)$ 变换变量，会得到关于新变量 $y$ 的密度 $p_y(y)$。下标表明 $p_x(x)$ 和 $p_y(y)$ 是两个不同的密度。当 $\delta x$ 很小时，落在区间 $(x,x+\delta x)$ 内的观测值会映射到区间 $(y,y+\delta y)$；其中 $x=g(y)$，且 $p_x(x)\delta x\simeq p_y(y)\delta y$。因此，令 $\delta x\to0$，得到

$$
p_y(y)=p_x(x)\left|\frac{\mathrm dx}{\mathrm dy}\right|
=p_x(g(y))\left|\frac{\mathrm dg}{\mathrm dy}\right|.\tag{2.71}
$$

这里取绝对值 $|\cdot|$，是因为导数 $\mathrm dy/\mathrm dx$ 可能为负，而密度要按长度之比缩放，这个比值始终为正。

<!-- pdf-page: 63 -->

这种密度变换方法非常有用：从一个处处非零的固定密度 $q(x)$ 出发，经过非线性变量变换 $y=f(x)$，原则上可以得到任意密度 $p(y)$；其中 $f(x)$ 是单调函数，满足 $0\leq f'(x)<\infty$（见习题 2.19）。

式 (2.71) 的一个推论是：概率密度最大值所在的位置依赖于变量的选择。假设函数 $f(x)$ 在 $\widehat x$ 处有众数（即最大值），因此 $f'(\widehat x)=0$。对应的新函数 $\widetilde f(y)$ 的众数位于 $\widehat y$。对式 (2.70) 两边关于 $y$ 求导，有

$$
\widetilde f'(\widehat y)=f'(g(\widehat y))g'(\widehat y)=0.\tag{2.72}
$$

若众数处 $g'(\widehat y)\neq0$，则 $f'(g(\widehat y))=0$。又已知 $f'(\widehat x)=0$，所以用 $x$ 和 $y$ 表示的众数位置满足 $\widehat x=g(\widehat y)$，这正符合预期。因此，直接对变量 $x$ 求函数的众数，等价于先把函数变换到变量 $y$，再对 $y$ 求众数，最后变换回 $x$。

现在看概率密度 $p_x(x)$ 在变量变换 $x=g(y)$ 下的行为。新变量的密度为 $p_y(y)$，由式 (2.71) 给出。为处理该式中的绝对值，写成 $g'(y)=s|g'(y)|$，其中 $s\in\{-1,+1\}$。于是式 (2.71) 可以写成

$$
p_y(y)=p_x(g(y))s g'(y),
$$

这里用到了 $1/s=s$。两边对 $y$ 求导，得到

$$
p'_y(y)=s p'_x(g(y))\{g'(y)\}^2+s p_x(g(y))g''(y).\tag{2.73}
$$

由于式 (2.73) 右边存在第二项，$\widehat x=g(\widehat y)$ 这一关系对密度的众数不再成立。也就是说，直接最大化 $p_x(x)$ 所得的 $x$，与先把密度变为 $p_y(y)$、对 $y$ 最大化、再变换回 $x$ 的结果一般不同。因此，密度的众数依赖于变量的选择。不过，对线性变换，式 (2.73) 右边的第二项为零，此时最大值的位置仍按 $\widehat x=g(\widehat y)$ 变换。

图 2.12 给出了一个简单例子。先考虑关于 $x$ 的高斯分布 $p_x(x)$，它是图中的红色曲线。我们从中抽取 $N=50{,}000$ 个样本并绘制直方图；如预期，直方图与 $p_x(x)$ 一致。现在考虑从 $x$ 到 $y$ 的非线性变量变换

$$
x=g(y)=\ln(y)-\ln(1-y)+5.\tag{2.74}
$$

它的反函数为

$$
y=g^{-1}(x)=\frac{1}{1+\exp(-x+5)},\tag{2.75}
$$

这是一个逻辑 sigmoid 函数，在图 2.12 中画为蓝色曲线。

<!-- pdf-page: 64 -->

<figure id="fig-2-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-12.png" alt="非线性变量变换下的密度众数：红色为 x 上的高斯密度，绿色为直接变换的函数，品红色为 y 上的密度，蓝色为反变换 sigmoid 函数；两组直方图分别对应 x 和 y 的样本">
  <figcaption>图 2.12：非线性变量变换下密度众数的变化示例，说明它与普通函数的行为不同。</figcaption>
  <p class="figure-translation">图内文字：$p_y(y)$ → 关于 $y$ 的概率密度；$g^{-1}(x)$ → 反变换函数；$p_x(x)$ → 关于 $x$ 的概率密度；$x$、$y$ → 横、纵坐标变量。</p>
</figure>

如果只把 $p_x(x)$ 当作 $x$ 的普通函数进行变换，就会得到图 2.12 中的绿色曲线 $p_x(g(y))$。此时，密度 $p_x(x)$ 的众数经 sigmoid 函数变换，恰好成为绿色曲线的众数。然而，关于 $y$ 的密度要按式 (2.71) 变换，对应图左侧的品红色曲线。注意，它的众数相对于绿色曲线的众数发生了偏移。

为验证这个结果，我们把抽取的 $50{,}000$ 个 $x$ 值用式 (2.75) 转换为相应的 $y$ 值，再绘制这些值的直方图。图中可以看到，该直方图与图 2.12 的品红色曲线一致，而不是与绿色曲线一致。

### 2.4.1 多元分布

式 (2.71) 可以推广到多个变量上的密度。考虑 $D$ 维变量 $\mathbf{x}=(x_1,\ldots,x_D)^\mathsf{T}$ 的密度 $p(\mathbf{x})$，并设 $\mathbf{x}=\mathbf{g}(\mathbf{y})$，变换到新变量 $\mathbf{y}=(y_1,\ldots,y_D)^\mathsf{T}$。这里仅讨论 $\mathbf{x}$ 和 $\mathbf{y}$ 维数相同的情形。变换后的密度是式 (2.71) 的推广：

$$
p_y(\mathbf{y})=p_x(\mathbf{x})\,|\det\mathbf{J}|,\tag{2.76}
$$

其中 $\mathbf{J}$ 是**雅可比矩阵**（Jacobian matrix），其元素为偏导数 $J_{ij}=\partial g_i/\partial y_j$，因此

$$
\mathbf{J}=\begin{bmatrix}
\dfrac{\partial g_1}{\partial y_1}&\cdots&\dfrac{\partial g_1}{\partial y_D}\\
\vdots&\ddots&\vdots\\
\dfrac{\partial g_D}{\partial y_1}&\cdots&\dfrac{\partial g_D}{\partial y_D}
\end{bmatrix}.\tag{2.77}
$$

直观地看，变量变换会拉伸某些空间区域、压缩另一些区域。点 $\mathbf{x}$ 附近的微小区域 $\Delta\mathbf{x}$ 被变换到相应的 $\Delta\mathbf{y}$。雅可比矩阵行列式的绝对值给出这些区域体积的比值，与积分换元时出现的是同一个因子。

<!-- pdf-page: 65 -->

<figure id="fig-2-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-13.png" alt="二维变量变换示意：左列网格从 x 空间扭曲到 y 空间，中列高斯密度变成四峰形状，右列样本点相应分成四簇">
  <figcaption>图 2.13：二维概率分布在变量变换下的变化。左列显示变量本身的变换；中列和右列分别显示这种变换对高斯分布及该分布样本的影响。</figcaption>
  <p class="figure-translation">图内符号：$x_1$、$x_2$ 为变换前的坐标；$y_1$、$y_2$ 为变换后的坐标。箭头表示由 $\mathbf{x}$ 空间到 $\mathbf{y}$ 空间。</p>
</figure>

式 (2.77) 源于区域 $\Delta\mathbf{x}$ 与区域 $\Delta\mathbf{y}$ 的概率质量相同。这里再次取绝对值，以保证密度非负。

译注：这里沿用前文的 $\mathbf{x}=\mathbf g(\mathbf y)$ 记法，因此从 $\mathbf x$ 到 $\mathbf y$ 用的是逆变换；概率质量守恒对应密度变换式 (2.76)，式 (2.77) 只是雅可比矩阵的展开。原书此处的变换方向与式号有不一致之处。

图 2.13 上排以二维高斯分布展示变量变换的效果。从 $\mathbf{x}$ 到 $\mathbf{y}$ 的变换为（见习题 2.20）

$$
y_1=x_1+\tanh(5x_1),\tag{2.78}
$$

$$
y_2=x_2+\tanh(5x_2)+\frac{x_1^3}{3}.\tag{2.79}
$$

下排还展示了 $\mathbf{x}$ 空间中的高斯分布样本，以及这些样本变换到 $\mathbf{y}$ 空间后的结果。

<!-- pdf-page: 66 -->

## 2.5 信息论

概率论也是另一个重要框架——**信息论**（information theory）——的基础。信息论量化数据集包含的信息，在机器学习中发挥重要作用。这里简要介绍本书后面将用到的几个信息论核心概念，包括各种形式的熵。关于信息论及其与机器学习的联系，更全面的介绍可参阅 MacKay (2003)。

### 2.5.1 熵

先考虑离散随机变量 $x$：观察到它的某个具体取值，会得到多少信息？信息量可以理解为得知 $x$ 的取值时的“意外程度”。如果得知一个极不可能的事件刚刚发生，我们得到的信息会多于得知一个很可能发生的事件；如果事先知道事件必然发生，我们就不会得到新信息。因此，信息量应取决于概率分布 $p(x)$。我们要找一个概率 $p(x)$ 的单调函数 $h(x)$ 来表示信息量。

要确定 $h(\cdot)$ 的形式，注意：对两个互不相关的事件 $x$ 和 $y$，同时观察到两者所获得的信息，应等于分别观察到它们所获信息之和，即 $h(x,y)=h(x)+h(y)$。两个互不相关的事件在统计上独立，因此 $p(x,y)=p(x)p(y)$。由这两个关系很容易看出，$h(x)$ 必须与 $p(x)$ 的对数有关，于是得到（见习题 2.21）

$$
h(x)=-\log_2 p(x).\tag{2.80}
$$

负号使信息量非负。概率较低的事件 $x$ 对应较高的信息量。对数的底可以任意选择；目前采用信息论中常用的以 $2$ 为底的对数。稍后会看到，此时 $h(x)$ 的单位是比特（bit，即“二进制位”）。

现在假设发送者要把某个随机变量的取值传给接收者。传输过程的平均信息量，是按分布 $p(x)$ 对式 (2.80) 求期望：

$$
H[x]=-\sum_x p(x)\log_2 p(x).\tag{2.81}
$$

这个重要的量称为随机变量 $x$ 的**熵**（entropy）。注意，$\lim_{\epsilon\to0}\epsilon\ln\epsilon=0$，因此遇到 $p(x)=0$ 时，把 $p(x)\ln p(x)$ 取为 $0$。

到目前为止，我们对信息量的定义 (2.80) 和相应熵的定义 (2.81) 只是作了比较直观的解释。接下来说明这些定义确实具有有用的性质。

<!-- pdf-page: 67 -->

考虑一个有八种可能状态且各状态等概率的随机变量 $x$。要把 $x$ 的取值传给接收者，需要发送长度为 $3$ 比特的消息。它的熵也正是

$$
H[x]=-8\times\frac18\log_2\frac18=3\text{ 比特}.
$$

再看 Cover 和 Thomas (1991) 的一个例子：变量有八种可能状态 $\{a,b,c,d,e,f,g,h\}$，其概率依次为 $(1/2,1/4,1/8,1/16,1/64,1/64,1/64,1/64)$。此时的熵为

$$
H[x]=-\frac12\log_2\frac12-\frac14\log_2\frac14-\frac18\log_2\frac18-\frac1{16}\log_2\frac1{16}-\frac4{64}\log_2\frac1{64}=2\text{ 比特}.
$$

可见，这个非均匀分布的熵比均匀分布小。稍后从无序程度的角度解释熵时，我们会更清楚地理解这一点。眼下先想想怎样把变量的状态传给接收者。像前面一样，我们可以用 $3$ 比特的数字。但也可以利用概率不均匀这一点：给更可能出现的事件分配较短的码，代价是给较少出现的事件分配较长的码，以期缩短平均码长。例如，按顺序用 $0$、$10$、$110$、$1110$、$111100$、$111101$、$111110$ 和 $111111$ 表示状态 $\{a,b,c,d,e,f,g,h\}$。需要传输的平均码长为

$$
\text{平均码长}=\frac12\times1+\frac14\times2+\frac18\times3+\frac1{16}\times4+4\times\frac1{64}\times6=2\text{ 比特},
$$

它再次等于该随机变量的熵。不能再使用更短的码串，因为多个码串连接后必须仍能被唯一地拆分。例如，$11001110$ 只能解码为状态序列 $c,a,d$。熵与最短编码长度之间的这种关系具有普遍性。**无噪声编码定理**（noiseless coding theorem；Shannon，1948）指出：传输随机变量状态所需的比特数以下界形式由熵给出。

从现在起，定义熵时将改用自然对数，这样与本书其他概念的联系更方便。此时熵的单位是纳特（nat，来自 natural logarithm），而不是比特；两种单位只相差一个 $\ln2$ 的因子。

### 2.5.2 物理学视角

我们刚才用指定随机变量状态所需的平均信息量来引入熵。事实上，熵在物理学中出现得更早：最初用于平衡态热力学，后来随着统计力学的发展，被赋予了衡量无序程度的更深层解释。为理解这一视角，考虑把 $N$ 个相同的物体分到若干箱中，设第 $i$ 个箱中有 $n_i$ 个物体。

<!-- pdf-page: 68 -->

现在计算把物体分配到各箱有多少种不同方式。选择第一个物体有 $N$ 种方式，选择第二个有 $N-1$ 种，以此类推；分配全部 $N$ 个物体共有 $N!$ 种方式，其中 $N!$ 读作“$N$ 的阶乘”，等于 $N\times(N-1)\times\cdots\times2\times1$。但我们不区分同一箱内物体的重新排列。第 $i$ 个箱内有 $n_i!$ 种排列，所以总分配方式数为

$$
W=\frac{N!}{\prod_i n_i!},\tag{2.82}
$$

称为**多重度**（multiplicity）。熵定义为多重度的对数再乘以常数因子 $1/N$：

$$
H=\frac1N\ln W=\frac1N\ln N!-\frac1N\sum_i\ln n_i!.\tag{2.83}
$$

令 $N\to\infty$，同时保持各比值 $n_i/N$ 不变，并使用斯特林近似：

$$
\ln N!\simeq N\ln N-N,\tag{2.84}
$$

便得到

$$
H=-\lim_{N\to\infty}\sum_i\left(\frac{n_i}{N}\right)\ln\left(\frac{n_i}{N}\right)
=-\sum_i p_i\ln p_i,\tag{2.85}
$$

这里用到了 $\sum_i n_i=N$，而 $p_i=\lim_{N\to\infty}(n_i/N)$ 表示物体被分到第 $i$ 个箱的概率。按物理学术语，物体在各箱中的具体分配叫作**微观态**（microstate）；由各箱占用数通过比值 $n_i/N$ 表示的整体分布叫作**宏观态**（macrostate）。多重度 $W$ 表示某个宏观态包含的微观态数，也称为该宏观态的权重。

可以把这些箱看成离散随机变量 $X$ 的状态 $x_i$，其中 $p(X=x_i)=p_i$。于是 $X$ 的熵为

$$
H[p]=-\sum_i p(x_i)\ln p(x_i).\tag{2.86}
$$

如果分布 $p(x_i)$ 的概率高度集中在少数几个取值上，熵就比较低；如果概率更均匀地散布在多个取值上，熵就较高，如图 2.14 所示。

由于 $0\leq p_i\leq1$，熵非负。当某一个 $p_i=1$、其余所有 $p_{j\ne i}=0$ 时，熵取得最小值 $0$。要找熵最大的配置，可以使用拉格朗日乘子处理概率归一化约束（见附录 C）。为此，最大化

$$
\widetilde H=-\sum_i p(x_i)\ln p(x_i)+\lambda\left(\sum_i p(x_i)-1\right).\tag{2.87}
$$

<!-- pdf-page: 69 -->

<figure id="fig-2-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-14.png" alt="三十个箱上的两个概率直方图：左侧概率集中，熵为 1.77；右侧分布较宽，熵为 3.09">
  <figcaption>图 2.14：两个分布在 30 个箱上的概率直方图。分布越宽，熵 $H$ 越高。均匀分布的熵最大，为 $H=-\ln(1/30)=3.40$。</figcaption>
  <p class="figure-translation">图内文字：probabilities → 概率；$H=1.77$、$H=3.09$ → 两个分布各自的熵值。</p>
</figure>

由此可得，所有 $p(x_i)$ 都相等，等于 $1/M$，其中 $M$ 是状态 $x_i$ 的总数。对应的熵为 $H=\ln M$（见习题 2.22）。也可由稍后要讨论的 Jensen 不等式推出这个结果（见习题 2.23）。为确认驻点确实是最大值，计算熵的二阶导数：

$$
\frac{\partial^2\widetilde H}{\partial p(x_i)\partial p(x_j)}=-I_{ij}\frac1{p_i},\tag{2.88}
$$

其中 $I_{ij}$ 是单位矩阵的元素。可见这些值都为负，因此驻点确实是最大值。

译注：按式 (2.88)，非对角元为零，严格为负的是对角元；Hessian 矩阵在 $p_i>0$ 时负定，最大值结论仍成立。

### 2.5.3 微分熵

熵的定义还可以推广到连续变量 $x$ 的分布 $p(x)$。先把 $x$ 轴分成宽度为 $\Delta$ 的小区间。假设 $p(x)$ 连续，由积分中值定理（Weisstein，1999），每个区间内都存在 $i\Delta\leq x_i\leq(i+1)\Delta$，使得

$$
\int_{i\Delta}^{(i+1)\Delta}p(x)\,\mathrm dx=p(x_i)\Delta.\tag{2.89}
$$

现在量化连续变量 $x$：只要 $x$ 落在第 $i$ 个小区间，就把它记为 $x_i$。观察到 $x_i$ 的概率于是为 $p(x_i)\Delta$。

<!-- pdf-page: 70 -->

这给出一个离散分布，它的熵为

$$
H_\Delta=-\sum_i p(x_i)\Delta\ln\bigl(p(x_i)\Delta\bigr)
=-\sum_i p(x_i)\Delta\ln p(x_i)-\ln\Delta.\tag{2.90}
$$

这里用到了 $\sum_i p(x_i)\Delta=1$，这一点由式 (2.89) 和式 (2.25) 得到。接下来去掉式 (2.90) 右侧的第二项 $-\ln\Delta$，因为它不依赖于 $p(x)$，再考虑 $\Delta\to0$ 的极限。右侧第一项在这一极限下趋向于 $p(x)\ln p(x)$ 的积分：

$$
\lim_{\Delta\to0}\left\{-\sum_i p(x_i)\Delta\ln p(x_i)\right\}
=-\int p(x)\ln p(x)\,\mathrm dx.\tag{2.91}
$$

右侧这个量称为**微分熵**（differential entropy）。离散熵与连续形式之间相差 $\ln\Delta$；当 $\Delta\to0$ 时，这一项发散。这反映出：若要非常精确地指定一个连续变量，需要大量比特。对于由向量 $\mathbf{x}$ 统一表示的多个连续变量，其概率密度的微分熵为

$$
H[\mathbf{x}]=-\int p(\mathbf{x})\ln p(\mathbf{x})\,\mathrm d\mathbf{x}.\tag{2.92}
$$

### 2.5.4 最大熵

前面看到，对离散分布，所有可能状态上的概率均匀分配时熵最大。现在考察连续变量的对应结论。要让这个最大值有确定意义，需要约束 $p(x)$ 的一阶矩、二阶矩，并保持归一化。因此，在以下三个约束下最大化微分熵：

$$
\int_{-\infty}^{\infty}p(x)\,\mathrm dx=1,\tag{2.93}
$$

$$
\int_{-\infty}^{\infty}xp(x)\,\mathrm dx=\mu,\tag{2.94}
$$

$$
\int_{-\infty}^{\infty}(x-\mu)^2p(x)\,\mathrm dx=\sigma^2.\tag{2.95}
$$

用拉格朗日乘子可进行这种带约束的最大化（见附录 C）：关于 $p(x)$ 最大化下面的泛函

$$
\begin{aligned}
&-\int_{-\infty}^{\infty}p(x)\ln p(x)\,\mathrm dx
+\lambda_1\left(\int_{-\infty}^{\infty}p(x)\,\mathrm dx-1\right)\\
&\quad+\lambda_2\left(\int_{-\infty}^{\infty}xp(x)\,\mathrm dx-\mu\right)
+\lambda_3\left(\int_{-\infty}^{\infty}(x-\mu)^2p(x)\,\mathrm dx-\sigma^2\right).
\end{aligned}\tag{2.96}
$$

<!-- pdf-page: 71 -->

使用变分法（见附录 B），把这个泛函的导数设为零，得到

$$
p(x)=\exp\bigl\{-1+\lambda_1+\lambda_2x+\lambda_3(x-\mu)^2\bigr\}.\tag{2.97}
$$

把这一结果代回三个约束方程，可以求得各拉格朗日乘子，最后得到（见习题 2.24）

$$
p(x)=\frac{1}{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac{(x-\mu)^2}{2\sigma^2}\right\}.\tag{2.98}
$$

所以，在上述约束下，微分熵最大的分布是高斯分布。注意，最大化熵时并没有显式要求分布非负。但结果确实非负，事后看来无须另加这个约束。

计算高斯分布的微分熵，可得（见习题 2.25）

$$
H[x]=\frac12\bigl\{1+\ln(2\pi\sigma^2)\bigr\}.\tag{2.99}
$$

这再次说明，分布越宽，即 $\sigma^2$ 越大，熵越高。式 (2.99) 还表明：微分熵与离散熵不同，可以为负；当 $\sigma^2<1/(2\pi e)$ 时，$H[x]<0$。

### 2.5.5 Kullback–Leibler 散度

本节至此介绍了一些信息论概念，核心是熵。现在开始把它们与机器学习联系起来。设 $p(x)$ 是未知分布，我们用近似分布 $q(x)$ 来建模。若按 $q(x)$ 构造编码方案，将 $x$ 的值传给接收者，那么与使用真实分布 $p(x)$ 相比，因改用 $q(x)$ 而平均额外需要的信息量（单位：纳特；假设采用高效编码）为

$$
\begin{aligned}
\operatorname{KL}(p\|q)
&=-\int p(x)\ln q(x)\,\mathrm dx
-\left\{-\int p(x)\ln p(x)\,\mathrm dx\right\}\\
&=-\int p(x)\ln\left\{\frac{q(x)}{p(x)}\right\}\,\mathrm dx.
\end{aligned}\tag{2.100}
$$

这个量称为分布 $p(x)$ 与 $q(x)$ 之间的**相对熵**（relative entropy）、**Kullback–Leibler 散度**，或简称 **KL 散度**（Kullback and Leibler，1951）。注意，它不对称：$\operatorname{KL}(p\|q)\not\equiv\operatorname{KL}(q\|p)$。

下面证明 $\operatorname{KL}(p\|q)\geq0$，且当且仅当 $p(x)=q(x)$ 时取等号。首先引入凸函数：若函数 $f(x)$ 的任意弦都位于函数图像之上或与之重合，就称 $f(x)$ 为**凸函数**（convex function），如图 2.15 所示。

区间 $[a,b]$ 中的任意 $x$ 都可写为 $\lambda a+(1-\lambda)b$，其中 $0\leq\lambda\leq1$。弦上相应点的函数值为 $\lambda f(a)+(1-\lambda)f(b)$，函数本身在该处的值则为 $f(\lambda a+(1-\lambda)b)$。

<!-- pdf-page: 72 -->

<figure id="fig-2-15">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-15.png" alt="红色凸函数 f(x) 位于连接其两点的蓝色弦下方，标出了 a、x_lambda、b 和对应垂线">
  <figcaption>图 2.15：凸函数 $f(x)$ 的任意弦（蓝色）都位于函数图像（红色）之上或与之重合。</figcaption>
  <p class="figure-translation">图内文字：chord → 弦；$f(x)$ → 函数值；$a$、$x_\lambda$、$b$ → 横轴上的三个位置。</p>
</figure>

凸性因而意味着

$$
f\bigl(\lambda a+(1-\lambda)b\bigr)\leq\lambda f(a)+(1-\lambda)f(b).\tag{2.101}
$$

这等价于要求函数的二阶导数处处为正（见习题 2.32）。凸函数的例子包括 $x\ln x$（$x>0$）和 $x^2$。如果仅在 $\lambda=0$ 或 $\lambda=1$ 时取等号，函数就叫作**严格凸函数**。相反，若每条弦都位于函数图像之下或与之重合，函数叫作**凹函数**（concave function）；严格凹函数的定义类似。如果 $f(x)$ 是凸函数，则 $-f(x)$ 是凹函数。

译注：对二阶可导函数，凸性的判据是二阶导数非负；二阶导数处处为正足以保证严格凸，但并非必要条件。

通过数学归纳法，可以由式 (2.101) 证明：凸函数 $f(x)$ 满足（见习题 2.33）

$$
f\left(\sum_{i=1}^{M}\lambda_i x_i\right)\leq\sum_{i=1}^{M}\lambda_i f(x_i),\tag{2.102}
$$

其中 $\lambda_i\geq0$、$\sum_i\lambda_i=1$，点集 $\{x_i\}$ 可以任取。式 (2.102) 称为 **Jensen 不等式**。如果把 $\lambda_i$ 看成取值为 $\{x_i\}$ 的离散变量 $x$ 的概率分布，该式可写成

$$
f(\mathbb{E}[x])\leq\mathbb{E}[f(x)],\tag{2.103}
$$

其中 $\mathbb{E}[\cdot]$ 表示期望。对连续变量，Jensen 不等式为

$$
f\left(\int x p(x)\,\mathrm dx\right)\leq\int f(x)p(x)\,\mathrm dx.\tag{2.104}
$$

把式 (2.104) 的 Jensen 不等式应用于式 (2.100) 的 KL 散度，得到

$$
\operatorname{KL}(p\|q)
=-\int p(x)\ln\left\{\frac{q(x)}{p(x)}\right\}\,\mathrm dx
\geq-\ln\int q(x)\,\mathrm dx=0.\tag{2.105}
$$

<!-- pdf-page: 73 -->

这里用到了 $-\ln x$ 是凸函数，以及归一化条件 $\int q(x)\,\mathrm dx=1$。实际上，$-\ln x$ 是严格凸函数，因此当且仅当所有 $x$ 都满足 $q(x)=p(x)$ 时等号成立。所以，KL 散度可以看作两个分布 $p(x)$ 与 $q(x)$ 不相似程度的度量。

数据压缩和密度估计（即对未知概率分布建模）有密切联系：知道真实分布时，可以实现最高效的压缩。若使用的分布不同于真实分布，编码必然较低效；平均额外需要传输的信息量至少等于两个分布之间的 KL 散度。

设数据来自我们想要建模的未知分布 $p(x)$。可以用参数分布 $q(x\mid\boldsymbol\theta)$ 来近似它，其中 $\boldsymbol\theta$ 是一组可调整参数。确定 $\boldsymbol\theta$ 的一种方法，是最小化 $p(x)$ 与 $q(x\mid\boldsymbol\theta)$ 之间的 KL 散度。但由于不知道 $p(x)$，不能直接这样做。假设我们已经观察到从 $p(x)$ 抽取的有限个训练点 $x_n$，$n=1,\ldots,N$。用式 (2.40)，可以把关于 $p(x)$ 的期望近似为训练点上的有限求和：

$$
\operatorname{KL}(p\|q)\simeq\frac1N\sum_{n=1}^{N}\bigl\{-\ln q(x_n\mid\boldsymbol\theta)+\ln p(x_n)\bigr\}.\tag{2.106}
$$

式 (2.106) 右侧第二项与 $\boldsymbol\theta$ 无关；第一项则是用训练集计算的 $q(x\mid\boldsymbol\theta)$ 对参数 $\boldsymbol\theta$ 的负对数似然。因此，最小化这个 KL 散度等价于最大化对数似然（见习题 2.34）。

### 2.5.6 条件熵

现在考虑两组变量 $\mathbf{x}$ 和 $\mathbf{y}$ 的联合分布 $p(\mathbf{x},\mathbf{y})$，并从中抽取成对的取值。若 $\mathbf{x}$ 的值已经知道，那么指定相应的 $\mathbf{y}$ 值还需要的信息量为 $-\ln p(\mathbf{y}\mid\mathbf{x})$。因此，指定 $\mathbf{y}$ 平均还需的信息量为

$$
H[\mathbf{y}\mid\mathbf{x}]
=-\iint p(\mathbf{y},\mathbf{x})\ln p(\mathbf{y}\mid\mathbf{x})\,\mathrm d\mathbf{y}\,\mathrm d\mathbf{x},\tag{2.107}
$$

称为**给定 $\mathbf{x}$ 时 $\mathbf{y}$ 的条件熵**。由概率乘法规则容易看出，条件熵满足（见习题 2.35）

$$
H[\mathbf{x},\mathbf{y}]=H[\mathbf{y}\mid\mathbf{x}]+H[\mathbf{x}],\tag{2.108}
$$

其中 $H[\mathbf{x},\mathbf{y}]$ 是 $p(\mathbf{x},\mathbf{y})$ 的微分熵，$H[\mathbf{x}]$ 是边缘分布 $p(\mathbf{x})$ 的微分熵。换句话说，描述 $\mathbf{x}$ 和 $\mathbf{y}$ 所需的信息量，等于单独描述 $\mathbf{x}$ 所需的信息量，加上已知 $\mathbf{x}$ 后指定 $\mathbf{y}$ 还需的信息量。

<!-- pdf-page: 74 -->

### 2.5.7 互信息

当两个变量 $\mathbf{x}$ 和 $\mathbf{y}$ 独立时，联合分布可分解为边缘分布之积：$p(\mathbf{x},\mathbf{y})=p(\mathbf{x})p(\mathbf{y})$。若它们不独立，可以用联合分布与边缘分布之积之间的 KL 散度，了解它们在多大程度上“接近”独立：

$$
\begin{aligned}
I[\mathbf{x},\mathbf{y}]
&\equiv\operatorname{KL}\bigl(p(\mathbf{x},\mathbf{y})\|p(\mathbf{x})p(\mathbf{y})\bigr)\\
&=-\iint p(\mathbf{x},\mathbf{y})\ln\left\{\frac{p(\mathbf{x})p(\mathbf{y})}{p(\mathbf{x},\mathbf{y})}\right\}\,\mathrm d\mathbf{x}\,\mathrm d\mathbf{y}.
\end{aligned}\tag{2.109}
$$

这称为 $\mathbf{x}$ 与 $\mathbf{y}$ 的**互信息**（mutual information）。由 KL 散度的性质可知，$I[\mathbf{x},\mathbf{y}]\geq0$；当且仅当 $\mathbf{x}$ 与 $\mathbf{y}$ 独立时，等号成立。利用概率加法和乘法规则，可以得到互信息与条件熵的关系（见习题 2.38）：

$$
I[\mathbf{x},\mathbf{y}]=H[\mathbf{x}]-H[\mathbf{x}\mid\mathbf{y}]
=H[\mathbf{y}]-H[\mathbf{y}\mid\mathbf{x}].\tag{2.110}
$$

因此，互信息表示知道 $\mathbf{y}$ 后，对 $\mathbf{x}$ 的不确定性减少了多少；反过来也一样。从贝叶斯视角看，$p(\mathbf{x})$ 可以视为 $\mathbf{x}$ 的先验分布，而观察到新数据 $\mathbf{y}$ 后，$p(\mathbf{x}\mid\mathbf{y})$ 是其后验分布。于是，互信息表示新观测 $\mathbf{y}$ 使我们对 $\mathbf{x}$ 的不确定性降低了多少。

## 2.6 贝叶斯概率

在图 2.2 的弯曲硬币例子中，我们用可重复随机事件的频率引入了概率，例如硬币以凹面朝上的概率。这里把这种解释称为概率的**经典解释**或**频率学派解释**。我们也引入了更一般的贝叶斯观点：用概率量化不确定性。在硬币例子里，我们不确定的是硬币凹面印着正面还是反面。

用概率表示不确定性不是随意选择：如果要遵循常识，进行理性而连贯的推断，就必然会用到概率。例如，Cox (1946) 证明，如果用数值表示信念程度，那么一组编码了这类信念的常识性质的简单公理，会唯一地导出一套处理信念程度的规则；这套规则等价于概率的加法和乘法规则。因此，把这些量称为（贝叶斯）概率是自然的。

对于弯曲硬币，我们假设在没有更多信息时，凹面是正面的概率为 $0.5$。现在设想有人告诉我们几次抛掷硬币的结果。直觉上，这些结果应该能提供关于凹面是否为正面的信息。例如，若反面朝上的次数远多于正面，而硬币更容易以凹面朝上，就有证据认为凹面更可能是反面。

<!-- pdf-page: 75 -->

这一判断确实正确，而且可以用概率规则量化（见习题 2.40）。贝叶斯定理由此有了新的用途：把硬币凹面为正面的先验概率，与抛掷结果提供的数据结合，转换成后验概率。这一过程还能反复进行：上一次的后验概率成为纳入下一批抛掷数据时的先验概率。

贝叶斯观点的一个特点是能自然地纳入先验知识。例如，一枚看起来公平的硬币连续抛三次，每次都是正面。正面概率的极大似然估计会给出 $1$，等于断言此后每次抛掷都会是正面！相反，使用任何合理先验的贝叶斯方法都会给出不那么极端的结论（参见第 3.1.2 节）。

### 2.6.1 模型参数

贝叶斯视角有助于理解机器学习的多个方面，这里仍以第 1.2 节的正弦曲线回归为例。记训练数据集为 $\mathcal D$。在线性回归中，我们已经看到，可通过极大似然法选择参数：把 $\mathbf w$ 设为使似然函数 $p(\mathcal D\mid\mathbf w)$ 最大的值。也就是说，选出使观测数据集概率最大的 $\mathbf w$。机器学习文献把似然函数的负对数称为**误差函数**。负对数是单调递减函数，所以最大化似然等价于最小化误差。这样会得到一组特定参数值 $\mathbf w_{\mathrm{ML}}$，随后用它预测新数据。

我们已经看到，训练集的不同选择，例如数据点数量不同，会产生不同的 $\mathbf w_{\mathrm{ML}}$。从贝叶斯视角，也可以用概率论描述模型参数中的这种不确定性。观察数据之前对 $\mathbf w$ 的假设，可用先验概率分布 $p(\mathbf w)$ 表示；观测数据 $\mathcal D$ 的作用通过似然函数 $p(\mathcal D\mid\mathbf w)$ 表示。贝叶斯定理在这里写成

$$
p(\mathbf w\mid\mathcal D)
=\frac{p(\mathcal D\mid\mathbf w)p(\mathbf w)}{p(\mathcal D)},\tag{2.111}
$$

它给出观察到 $\mathcal D$ 后对 $\mathbf w$ 的不确定性，即后验概率 $p(\mathbf w\mid\mathcal D)$。

需要强调：把 $p(\mathcal D\mid\mathbf w)$ 看作参数向量 $\mathbf w$ 的函数时，它称为**似然函数**，表示不同 $\mathbf w$ 值下已观测数据集出现的可能程度。似然 $p(\mathcal D\mid\mathbf w)$ 不是 $\mathbf w$ 上的概率分布，关于 $\mathbf w$ 积分也不一定等于 $1$。

按这个似然定义，贝叶斯定理可以用文字概括为

$$
\text{后验}\ \propto\ \text{似然}\times\text{先验},\tag{2.112}
$$

<!-- pdf-page: 76 -->

这里所有量都看作 $\mathbf w$ 的函数。式 (2.111) 的分母是归一化常数，保证左侧后验分布是有效的概率密度，即积分为 $1$。对式 (2.111) 两边关于 $\mathbf w$ 积分，可以把这个分母写成先验分布和似然函数的积分：

$$
p(\mathcal D)=\int p(\mathcal D\mid\mathbf w)p(\mathbf w)\,\mathrm d\mathbf w.\tag{2.113}
$$

贝叶斯范式和频率学派范式都以似然函数 $p(\mathcal D\mid\mathbf w)$ 为核心，但两者的用法根本不同。在频率学派的框架中，$\mathbf w$ 被视为固定参数，其值由某种“估计量”确定。这个估计值的误差棒，至少从概念上讲，是通过考虑可能出现的不同数据集 $\mathcal D$ 的分布来确定的。相比之下，贝叶斯观点只考虑一个数据集 $\mathcal D$——实际观察到的那个；参数的不确定性则由 $\mathbf w$ 上的概率分布表示。

### 2.6.2 正则化

用贝叶斯视角还能理解第 1.2.5 节正弦曲线回归例子中用于减轻过拟合的正则化。除了最大化似然函数来选模型参数 $\mathbf w$，还可以最大化式 (2.111) 的后验概率。这称为**最大后验估计**（maximum a posteriori estimate，MAP）。等价地，也可以最小化后验概率的负对数。对式 (2.111) 两边取负对数，得到

$$
-\ln p(\mathbf w\mid\mathcal D)
=-\ln p(\mathcal D\mid\mathbf w)-\ln p(\mathbf w)+\ln p(\mathcal D).\tag{2.114}
$$

式 (2.114) 右侧第一项是通常的负对数似然；第三项不依赖 $\mathbf w$，可以省去。第二项是 $\mathbf w$ 的函数，加在负对数似然上，因此可以看作正则化。为看得更清楚，设先验 $p(\mathbf w)$ 是 $\mathbf w$ 各元素的独立零均值高斯分布之积，并且它们都有相同方差 $s^2$：

$$
p(\mathbf w\mid s)
=\prod_{i=0}^{M}\mathcal N(w_i\mid0,s^2)
=\prod_{i=0}^{M}\left(\frac1{2\pi s^2}\right)^{1/2}
\exp\left\{-\frac{w_i^2}{2s^2}\right\}.\tag{2.115}
$$

把它代入式 (2.114)，得到

$$
-\ln p(\mathbf w\mid\mathcal D)
=-\ln p(\mathcal D\mid\mathbf w)
+\frac1{2s^2}\sum_{i=0}^{M}w_i^2+\mathrm{const}.\tag{2.116}
$$

对于对数似然由式 (2.66) 给出的线性回归模型，最大化后验分布等价于最小化如下函数（见习题 2.41）：

<!-- pdf-page: 77 -->

$$
E(\mathbf w)=\frac1{2\sigma^2}\sum_{n=1}^{N}\bigl\{y(x_n,\mathbf w)-t_n\bigr\}^2
+\frac1{2s^2}\mathbf w^\mathsf{T}\mathbf w.\tag{2.117}
$$

它正是前面式 (1.4) 的正则化平方和误差函数的形式。

### 2.6.3 贝叶斯机器学习

贝叶斯视角帮助我们理解为何使用正则化，并推导出了正则项的一种具体形式。不过，仅使用贝叶斯定理还不构成真正的贝叶斯机器学习处理方法：它仍然只求出一个 $\mathbf w$ 值，因此没有考虑 $\mathbf w$ 取值的不确定性。设有训练集 $\mathcal D$，目标是对新输入 $x$ 预测目标变量 $t$。我们关心的是给定 $x$ 和 $\mathcal D$ 时 $t$ 的分布。利用概率加法和乘法规则，得到

$$
p(t\mid x,\mathcal D)=\int p(t\mid x,\mathbf w)p(\mathbf w\mid\mathcal D)\,\mathrm d\mathbf w.\tag{2.118}
$$

可见，预测是在所有可能的 $\mathbf w$ 值上对 $p(t\mid x,\mathbf w)$ 作加权平均，权重由后验概率分布 $p(\mathbf w\mid\mathcal D)$ 给出。贝叶斯方法的关键区别就在于对参数空间的这种积分。通常的频率学派方法则通过优化某个损失函数——例如正则化平方和——得到参数的点估计。

这样完整的贝叶斯机器学习处理方法带来一些重要认识。例如，第 1.2 节多项式回归中的过拟合，是极大似然法所造成的一种问题；用贝叶斯方法对参数边缘化时，这个问题不会出现。类似地，对于同一个问题，我们可能有多个候选模型，例如回归例子中不同阶数的多项式。极大似然法只选使数据概率最高的模型，但这会偏向越来越复杂的模型，从而造成过拟合。完整的贝叶斯处理方法对所有可能模型求平均，每个模型的贡献由其后验概率加权（参见第 9.6 节）。而且，后验概率通常在复杂度适中的模型上最高。非常简单的模型（例如低阶多项式）不能充分拟合数据，因此概率低；非常复杂的模型（例如极高阶多项式）的概率也低，因为对参数进行贝叶斯积分会自动惩罚复杂度。有关贝叶斯方法在机器学习（包括神经网络）中的全面介绍，可参阅 Bishop (2006)。

不幸的是，贝叶斯框架有一个主要缺点，式 (2.118) 已显示出这一点：需要在参数空间上积分。现代深度学习模型可能有数百万甚至数十亿个参数，即便是对这种积分作简单近似，通常也不可行。事实上，若计算资源有限而训练数据充足，

<!-- pdf-page: 78 -->

相比对小得多的模型采用贝叶斯方法，对大型神经网络使用极大似然方法，并通常辅以一种或多种正则化，往往效果更好。

## 习题

**2.1（★）** 在癌症筛查例子中，癌症的先验概率取为 $p(C=1)=0.01$。现实中的癌症患病率通常低得多。设 $p(C=1)=0.001$，重新计算检测结果为阳性时患癌的概率 $p(C=1\mid T=1)$。这个结果直觉上可能令许多人意外：检测看起来很准确，但阳性结果对应的患癌概率仍然很低。

**2.2（★★）** 确定的数满足传递性：若 $x>y$ 且 $y>z$，则 $x>z$。但对随机数，传递性未必成立。图 2.16 给出按循环顺序排列的四枚立方骰子。证明：循环中的每枚骰子掷出比前一枚更大点数的概率都是 $2/3$。这种骰子叫作**非传递骰子**（non-transitive dice）；图中的具体例子称为 **Efron 骰子**。

<figure id="fig-2-16">
  <img src="books/bishop-deep-learning-2024/assets/chapter-02/fig-2-16.png" alt="四枚展开的立方骰子按箭头排列成循环：黄色六面全为 3，蓝色六面为 0、0、4、4、4、4，绿色六面为 1、1、1、5、5、5，红色六面为 2、2、2、2、6、6">
  <figcaption>图 2.16：非传递立方骰子的例子。每枚骰子都已“展开”，展示六个面的点数。骰子按循环排列，每枚骰子掷出比循环中前一枚更大点数的概率都是 $2/3$。</figcaption>
</figure>

**2.3（★）** 设变量 $y$ 是两个独立随机变量的和：$y=u+v$，其中 $u\sim p_u(u)$、$v\sim p_v(v)$。证明 $p_y(y)$ 为

$$
p(y)=\int p_u(u)p_v(y-u)\,\mathrm du.\tag{2.119}
$$

这称为 $p_u(u)$ 与 $p_v(v)$ 的**卷积**（convolution）。

**2.4（★★）** 验证均匀分布 (2.33) 已正确归一化，并求出它的均值和方差表达式。

**2.5（★★）** 验证指数分布 (2.34) 和拉普拉斯分布 (2.35) 均已正确归一化。

<!-- pdf-page: 79 -->

**2.6（★）** 利用狄拉克 delta 函数的性质，证明经验密度 (2.37) 已正确归一化。

**2.7（★）** 利用经验密度 (2.37)，证明式 (2.39) 的期望可按式 (2.40) 的形式，用从该密度抽取的有限个样本求和来近似。

**2.8（★）** 利用定义 (2.44)，证明 $\operatorname{var}[f(x)]$ 满足式 (2.45)。

**2.9（★）** 证明：若变量 $x$ 和 $y$ 独立，则它们的协方差为零。

**2.10（★）** 设变量 $x$ 和 $z$ 在统计上独立。证明它们的和的均值与方差满足

$$
\mathbb E[x+z]=\mathbb E[x]+\mathbb E[z],\tag{2.120}
$$

$$
\operatorname{var}[x+z]=\operatorname{var}[x]+\operatorname{var}[z].\tag{2.121}
$$

**2.11（★）** 考虑联合分布为 $p(x,y)$ 的两个变量 $x$ 和 $y$。证明以下两个结果：

$$
\mathbb E[x]=\mathbb E_y\bigl[\mathbb E_x[x\mid y]\bigr],\tag{2.122}
$$

$$
\operatorname{var}[x]=\mathbb E_y\bigl[\operatorname{var}_x[x\mid y]\bigr]
+\operatorname{var}_y\bigl[\mathbb E_x[x\mid y]\bigr].\tag{2.123}
$$

其中 $\mathbb E_x[x\mid y]$ 表示在条件分布 $p(x\mid y)$ 下对 $x$ 求期望；条件方差的记号与此类似。

**2.12（★★★）** 本题证明一元高斯分布的归一化条件 (2.51)。考虑积分

$$
I=\int_{-\infty}^{\infty}\exp\left(-\frac{x^2}{2\sigma^2}\right)\,\mathrm dx,\tag{2.124}
$$

先把它的平方写成

$$
I^2=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}
\exp\left(-\frac{x^2}{2\sigma^2}-\frac{y^2}{2\sigma^2}\right)
\,\mathrm dx\,\mathrm dy.\tag{2.125}
$$

然后，把笛卡尔坐标 $(x,y)$ 变换为极坐标 $(r,\theta)$，再令 $u=r^2$。证明：分别对 $\theta$ 和 $u$ 积分，并在最后对两边开平方，可得

$$
I=(2\pi\sigma^2)^{1/2}.\tag{2.126}
$$

最后用这一结果证明高斯分布 $\mathcal N(x\mid\mu,\sigma^2)$ 已归一化。

<!-- pdf-page: 80 -->

**2.13（★★）** 通过变量变换，验证式 (2.49) 的一元高斯分布满足式 (2.52)。接着，对归一化条件

$$
\int_{-\infty}^{\infty}\mathcal N(x\mid\mu,\sigma^2)\,\mathrm dx=1\tag{2.127}
$$

两边关于 $\sigma^2$ 求导，验证高斯分布满足式 (2.53)。最后，证明式 (2.54) 成立。

**2.14（★）** 证明高斯分布 (2.49) 的众数（即最大值所在位置）为 $\mu$。

**2.15（★）** 把对数似然函数 (2.56) 关于 $\mu$ 和 $\sigma^2$ 的导数设为零，验证式 (2.57) 和式 (2.58) 的结果。

**2.16（★★）** 利用式 (2.52) 和式 (2.53)，证明

$$
\mathbb E[x_nx_m]=\mu^2+I_{nm}\sigma^2,\tag{2.128}
$$

其中 $x_n$ 和 $x_m$ 是从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布中抽取的数据点；当 $n=m$ 时 $I_{nm}=1$，否则 $I_{nm}=0$。进而证明式 (2.59) 和式 (2.60)。

**2.17（★★）** 利用定义 (2.61)，证明式 (2.62)：对高斯分布，如果方差估计量使用真实均值，则其期望等于真实方差 $\sigma^2$。

**2.18（★）** 证明：对式 (2.66) 关于 $\sigma^2$ 最大化，可得式 (2.68)。

**2.19（★★）** 利用概率密度在变量变换下的性质 (2.71)，证明：从一个处处非零的固定密度 $q(x)$ 出发，作非线性变量变换 $y=f(x)$，就能得到任意密度 $p(y)$；其中 $f(x)$ 为单调函数，满足 $0\leq f'(x)<\infty$。写出 $f(x)$ 所满足的微分方程，并画图说明密度如何变换。

**2.20（★）** 求式 (2.78) 和式 (2.79) 所定义变换的雅可比矩阵各元素。

**2.21（★）** 在第 2.5 节，我们把熵 $h(x)$ 理解为：观察到分布为 $p(x)$ 的随机变量 $x$ 的取值时所得到的信息量。已经看到，对满足 $p(x,y)=p(x)p(y)$ 的独立变量 $x$ 和 $y$，信息量具有可加性，即 $h(x,y)=h(x)+h(y)$。本题要以函数 $h(p)$ 的形式推导 $h$ 与 $p$ 的关系。先证明 $h(p^2)=2h(p)$，再用归纳法证明，对正整数 $n$，有 $h(p^n)=nh(p)$。进而证明，对正整数 $m$，有 $h(p^{n/m})=(n/m)h(p)$。这意味着对正有理数 $x$，有 $h(p^x)=xh(p)$；由连续性，这对正实数 $x$ 也成立。最后证明 $h(p)$ 必须具有 $h(p)\propto\ln p$ 的形式。

<!-- pdf-page: 81 -->

**2.22（★）** 用拉格朗日乘子证明：对离散变量最大化熵 (2.86)，所得分布的所有概率 $p(x_i)$ 都相等，而对应的熵为 $\ln M$。

**2.23（★）** 考虑一个有 $M$ 个状态的离散随机变量 $x$。用式 (2.102) 的 Jensen 不等式证明，其分布 $p(x)$ 的熵满足 $H[x]\leq\ln M$。

**2.24（★★）** 用变分法证明泛函 (2.96) 的驻点由式 (2.97) 给出。然后用约束 (2.93)、(2.94) 和 (2.95) 消去拉格朗日乘子，证明最大熵解是式 (2.98) 的高斯分布。

**2.25（★）** 利用式 (2.94) 和式 (2.95)，证明一元高斯分布 (2.98) 的熵由式 (2.99) 给出。

**2.26（★★）** 设 $p(\mathbf x)$ 是某个固定分布，我们希望用高斯分布 $q(\mathbf x)=\mathcal N(\mathbf x\mid\boldsymbol\mu,\boldsymbol\Sigma)$ 来近似它。写出高斯 $q(\mathbf x)$ 情形下 KL 散度 $\operatorname{KL}(p\|q)$ 的形式，再对其求导，证明：关于 $\boldsymbol\mu$ 和 $\boldsymbol\Sigma$ 最小化 $\operatorname{KL}(p\|q)$，所得 $\boldsymbol\mu$ 等于在 $p(\mathbf x)$ 下 $\mathbf x$ 的期望，$\boldsymbol\Sigma$ 等于其协方差矩阵。

**2.27（★★）** 计算两个高斯分布 $p(x)=\mathcal N(x\mid\mu,\sigma^2)$ 与 $q(x)=\mathcal N(x\mid m,s^2)$ 之间的 KL 散度 (2.100)。

**2.28（★★）** 散度的 **alpha 族**定义为

$$
D_\alpha(p\|q)=\frac4{1-\alpha^2}
\left(1-\int p(x)^{(1+\alpha)/2}q(x)^{(1-\alpha)/2}\,\mathrm dx\right),\tag{2.129}
$$

其中 $\alpha$ 是满足 $-\infty<\alpha<\infty$ 的连续参数。证明：当 $\alpha\to1$ 时，它对应 KL 散度 $\operatorname{KL}(p\|q)$。可以把 $p^\epsilon$ 写成 $\exp(\epsilon\ln p)=1+\epsilon\ln p+O(\epsilon^2)$，再令 $\epsilon\to0$。同样证明，当 $\alpha\to-1$ 时，它对应 $\operatorname{KL}(q\|p)$。

**2.29（★★）** 考虑联合分布为 $p(\mathbf x,\mathbf y)$ 的两个变量 $\mathbf x$ 和 $\mathbf y$。证明它们的联合微分熵满足

$$
H[\mathbf x,\mathbf y]\leq H[\mathbf x]+H[\mathbf y],\tag{2.130}
$$

当且仅当 $\mathbf x$ 与 $\mathbf y$ 在统计上独立时，等号成立。

**2.30（★）** 设连续变量向量 $\mathbf x$ 的分布为 $p(\mathbf x)$，熵为 $H[\mathbf x]$。通过非奇异线性变换 $\mathbf y=\mathbf A\mathbf x$ 得到新变量 $\mathbf y$。证明对应的熵为 $H[\mathbf y]=H[\mathbf x]+\ln\det\mathbf A$，其中 $\det\mathbf A$ 是 $\mathbf A$ 的行列式。

译注：原题按原式保留；若 $\det\mathbf A<0$，实数对数需要把行列式改为 $|\det\mathbf A|$。

**2.31（★★）** 设两个离散随机变量 $x$ 与 $y$ 的条件熵 $H[y\mid x]$ 为零。证明：对每个满足 $p(x)>0$ 的 $x$ 值，$y$ 都是 $x$ 的函数。换句话说，对每个这样的 $x$，仅有一个 $y$ 值使 $p(y\mid x)\neq0$。

<!-- pdf-page: 82 -->

**2.32（★）** 严格凸函数定义为每条弦都位于函数图像上方的函数。证明这等价于函数的二阶导数为正。

**2.33（★★）** 用数学归纳法证明：凸函数的不等式 (2.101) 蕴含式 (2.102)。

**2.34（★）** 证明：经验分布 (2.37) 与模型分布 $q(x\mid\boldsymbol\theta)$ 之间的 KL 散度 (2.100)，除一个加法常数外，等于负对数似然函数。

**2.35（★）** 利用定义 (2.107) 和概率乘法规则，证明式 (2.108)。

**2.36（★★★）** 考虑两个二元变量 $x$ 和 $y$，其联合分布为

| $x\backslash y$ | $0$ | $1$ |
|:---:|:---:|:---:|
| $0$ | $1/3$ | $1/3$ |
| $1$ | $0$ | $1/3$ |

计算下列各量：

|  |  |  |
|:---|:---|:---|
| (a) $H[x]$ | (c) $H[y\mid x]$ | (e) $H[x,y]$ |
| (b) $H[y]$ | (d) $H[x\mid y]$ | (f) $I[x,y]$ |

画出维恩图，说明这些量之间的关系。

**2.37（★）** 对 $f(x)=\ln x$ 应用 Jensen 不等式 (2.102)，证明一组实数的算术平均值不小于它们的几何平均值。

译注：原题按原文保留。几何平均须取正实数；$\ln x$ 是凹函数，应使用 Jensen 不等式的反向形式，或对凸函数 $-\ln x$ 使用式 (2.102)。

**2.38（★）** 利用概率加法和乘法规则，证明互信息 $I(\mathbf x,\mathbf y)$ 满足式 (2.110)。

**2.39（★★）** 设变量 $z_1$ 和 $z_2$ 独立，因此 $p(z_1,z_2)=p(z_1)p(z_2)$。证明它们的协方差矩阵是对角矩阵。这说明独立是两个变量不相关的充分条件。现在考虑变量 $y_1$ 与 $y_2$：$y_1$ 的分布关于 $0$ 对称，且 $y_2=y_1^2$。写出条件分布 $p(y_2\mid y_1)$，并注意它依赖于 $y_1$，因此两个变量并不独立。再证明它们的协方差矩阵仍是对角矩阵。为此，利用关系 $p(y_1,y_2)=p(y_1)p(y_2\mid y_1)$，证明非对角元素为零。这个反例表明，零相关性并不足以推出独立性。

**2.40（★）** 考虑图 2.2 中的弯曲硬币。假设凸面是正面的先验概率为 $0.1$。现在抛掷硬币 $10$ 次，已知其中 $8$ 次正面朝上、$2$ 次反面朝上。用贝叶斯定理求凹面是正面的后验概率，并计算下一次抛掷正面朝上的概率。

<!-- pdf-page: 83 -->

**2.41（★）** 把式 (2.115) 代入式 (2.114)，并利用线性回归模型的对数似然结果 (2.66)，推导正则化误差函数 (2.117)。
