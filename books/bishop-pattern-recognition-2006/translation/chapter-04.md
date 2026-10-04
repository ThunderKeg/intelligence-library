# 第 4 章 用于分类的线性模型

<aside class="chapter-guide"><strong>本章导读</strong><p>本章把线性模型用于分类，先从决策边界的几何性质出发，讨论最小二乘、Fisher 判别和感知机。随后比较两种概率建模方式：先描述各类别的数据分布，或直接描述类别的后验概率，并说明这些模型如何用于分类决策。</p></aside>

<!-- pdf-page: 199 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-chapter-opening.png" alt="第 4 章章首装饰图：水面反光纹理"><p class="figure-translation">Linear Models for Classification → 用于分类的线性模型。</p></figure>

上一章研究了一类解析性质和计算性质都特别简单的回归模型。现在讨论用于解决分类问题的类似模型。分类的目标是，给定输入向量 $\mathbf{x}$，把它分配到 $K$ 个离散类别 $\mathcal{C}_k$ 中的某一类，其中 $k=1,\ldots,K$。最常见的情形是，各类别互不相交，因此每个输入恰好被分到一个类别。这样，输入空间就被划分为若干决策区域（decision region），区域之间的边界称为决策边界（decision boundary）或决策面（decision surface）。本章考虑用于分类的线性模型，即决策面是输入向量 $\mathbf{x}$ 的线性函数，因此对应于 $D$ 维输入空间中的 $(D-1)$ 维超平面。如果一个数据集的各类别可以由线性决策面完全分开，就称它是线性可分的（linearly separable）。

对于回归问题，目标变量 $\mathbf{t}$ 就是由希望预测的实数值组成的向量。对于分类问题，可以用不同的

<!-- pdf-page: 200 -->
<!-- join-previous-paragraph -->
目标值表示方式来表达类别标签。对于概率模型，在二分类问题中最方便的是二元表示：只有一个目标变量 $t\in\{0,1\}$，其中 $t=1$ 表示类别 $\mathcal{C}_1$，$t=0$ 表示类别 $\mathcal{C}_2$。可以把 $t$ 的值解释为属于类别 $\mathcal{C}_1$ 的概率，只是概率仅取 0 和 1 这两个极端值。对于 $K>2$ 个类别，采用 1-of-$K$ 编码很方便：$\mathbf{t}$ 是长度为 $K$ 的向量，如果类别为 $\mathcal{C}_j$，那么除了 $t_j=1$ 以外，$\mathbf{t}$ 的所有元素 $t_k$ 都为零。例如，当 $K=5$ 时，来自第 2 类的模式对应的目标向量为

$$
\mathbf{t}=(0,1,0,0,0)^{\mathrm T}.
\tag{4.1}
$$

同样，可以把 $t_k$ 的值解释为属于类别 $\mathcal{C}_k$ 的概率。对于非概率模型，其他目标变量表示有时会更方便。

第 1 章区分了三种解决分类问题的方法。最简单的方法是构造判别函数（discriminant function），直接把每个向量 $\mathbf{x}$ 分配到一个具体类别。另一种更有力的方法，是在推断阶段对条件概率分布 $p(\mathcal{C}_k\mid\mathbf{x})$ 建模，再利用这个分布作出最优决策。如第 1.5.4 节所讨论的，把推断与决策分开有许多好处。确定条件概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 有两种不同的方法。一种是直接对它们建模，例如用参数模型表示这些概率，再利用训练集优化参数。另一种是采用生成式方法，对类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 和类别先验概率 $p(\mathcal{C}_k)$ 建模，再使用贝叶斯定理计算所需的后验概率：

$$
p(\mathcal{C}_k\mid\mathbf{x})=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{p(\mathbf{x})}.
\tag{4.2}
$$

本章将讨论这三种方法的例子。

在第 3 章的线性回归模型中，模型预测 $y(\mathbf{x},\mathbf{w})$ 是参数 $\mathbf{w}$ 的线性函数。在最简单的情况下，模型对输入变量也呈线性关系，因此形式为 $y(\mathbf{x})=\mathbf{w}^{\mathrm T}\mathbf{x}+w_0$，其中 $y$ 是实数。不过，在分类问题中，我们希望预测离散的类别标签，或更一般地，预测位于区间 $(0,1)$ 内的后验概率。为此，考虑对这个模型进行推广：用非线性函数 $f(\cdot)$ 变换 $\mathbf{w}$ 的线性函数，即

$$
y(\mathbf{x})=f(\mathbf{w}^{\mathrm T}\mathbf{x}+w_0).
\tag{4.3}
$$

在机器学习文献中，$f(\cdot)$ 称为激活函数（activation function）；在统计学文献中，它的反函数称为连接函数（link function）。决策面对应于 $y(\mathbf{x})=\text{常数}$，因此 $\mathbf{w}^{\mathrm T}\mathbf{x}+w_0=\text{常数}$；即使 $f(\cdot)$ 非线性，决策面仍然是 $\mathbf{x}$ 的线性函数。因此，式（4.3）所描述的这类模型称为广义线性模型（generalized linear model）

<!-- pdf-page: 201 -->
<!-- join-previous-paragraph -->
（McCullagh and Nelder, 1989）。不过，与用于回归的模型不同，由于存在非线性函数 $f(\cdot)$，它们对参数已不再是线性的。这使其解析性质和计算性质比线性回归模型更复杂。尽管如此，与后续章节将研究的更一般的非线性模型相比，这些模型仍然相对简单。

如果像第 3 章的回归模型那样，先利用基函数向量 $\boldsymbol{\phi}(\mathbf{x})$ 对输入变量作固定的非线性变换，本章讨论的算法也同样适用。我们先考虑直接在原始输入空间 $\mathbf{x}$ 中分类；到第 4.3 节，为与后续章节一致，再改用包含基函数的记号。

## 4.1 判别函数

判别函数接受一个输入向量 $\mathbf{x}$，并把它分配到 $K$ 个类别中的一个，类别记为 $\mathcal{C}_k$。本章只讨论线性判别函数（linear discriminant），即决策面为超平面的情形。为简化讨论，先考虑二分类，再研究如何推广到 $K>2$ 个类别。

### 4.1.1 二分类

最简单的线性判别函数，是输入向量的线性函数，即

$$
y(\mathbf{x})=\mathbf{w}^{\mathrm T}\mathbf{x}+w_0
\tag{4.4}
$$

其中，$\mathbf{w}$ 称为权重向量（weight vector），$w_0$ 为偏置（bias，不要与统计意义上的偏差混淆）。偏置的负值有时称为阈值（threshold）。如果 $y(\mathbf{x})\geqslant0$，就将输入向量 $\mathbf{x}$ 分配到类别 $\mathcal{C}_1$，否则分配到类别 $\mathcal{C}_2$。因此，相应的决策边界由关系 $y(\mathbf{x})=0$ 定义，对应于 $D$ 维输入空间中的 $(D-1)$ 维超平面。考虑决策面上的两点 $\mathbf{x}_{\mathrm A}$ 和 $\mathbf{x}_{\mathrm B}$。由于 $y(\mathbf{x}_{\mathrm A})=y(\mathbf{x}_{\mathrm B})=0$，有 $\mathbf{w}^{\mathrm T}(\mathbf{x}_{\mathrm A}-\mathbf{x}_{\mathrm B})=0$。因此，向量 $\mathbf{w}$ 与决策面内的每个向量正交，$\mathbf{w}$ 也就决定了决策面的方向。同样，如果 $\mathbf{x}$ 是决策面上的一点，则 $y(\mathbf{x})=0$，因此，从原点到决策面的法向距离为

$$
\frac{\mathbf{w}^{\mathrm T}\mathbf{x}}{\|\mathbf{w}\|}=-\frac{w_0}{\|\mathbf{w}\|}.
\tag{4.5}
$$

由此可见，偏置参数 $w_0$ 决定决策面的位置。图 4.1 用 $D=2$ 的情形说明了这些性质。

另外，$y(\mathbf{x})$ 的值还给出了点 $\mathbf{x}$ 到决策面的垂直距离 $r$ 的一种带符号度量。为说明这一点，考虑

<!-- pdf-page: 202 -->
<!-- join-previous-paragraph -->
任意一点 $\mathbf{x}$，令 $\mathbf{x}_{\perp}$ 为它在决策面上的正交投影，则

$$
\mathbf{x}=\mathbf{x}_{\perp}+r\frac{\mathbf{w}}{\|\mathbf{w}\|}.
\tag{4.6}
$$

在等式两边左乘 $\mathbf{w}^{\mathrm T}$ 再加上 $w_0$，利用 $y(\mathbf{x})=\mathbf{w}^{\mathrm T}\mathbf{x}+w_0$ 和 $y(\mathbf{x}_{\perp})=\mathbf{w}^{\mathrm T}\mathbf{x}_{\perp}+w_0=0$，得到

$$
r=\frac{y(\mathbf{x})}{\|\mathbf{w}\|}.
\tag{4.7}
$$

图 4.1 展示了这个结果。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-1.png" alt="二维线性判别函数的法向量、偏置和有符号距离"><figcaption>图 4.1：二维线性判别函数的几何示意。红色决策面垂直于 $\mathbf{w}$，它相对于原点的位移由偏置参数 $w_0$ 控制。此外，任意点 $\mathbf{x}$ 到决策面的有符号正交距离为 $y(\mathbf{x})/\|\mathbf{w}\|$。</figcaption></figure>

与第 3 章的线性回归模型一样，有时采用更紧凑的记号会更方便：引入一个额外的形式“输入” $x_0=1$，再定义 $\widetilde{\mathbf{w}}=(w_0,\mathbf{w})$ 和 $\widetilde{\mathbf{x}}=(x_0,\mathbf{x})$，于是

$$
y(\mathbf{x})=\widetilde{\mathbf{w}}^{\mathrm T}\widetilde{\mathbf{x}}.
\tag{4.8}
$$

此时，决策面是扩展后的 $(D+1)$ 维输入空间中经过原点的 $D$ 维超平面。

### 4.1.2 多分类

现在考虑把线性判别函数推广到 $K>2$ 个类别。我们可能会想到，把多个二分类判别函数组合起来，构造一个 $K$ 分类判别函数。但下面会看到，这会带来一些严重困难（Duda and Hart, 1973）。

考虑使用 $K-1$ 个分类器，每个分类器解决一个二分类问题：把特定类别 $\mathcal{C}_k$ 中的点与不属于该类的点分开。这称为一对其余（one-versus-the-rest）分类器。图 4.2 左图给出了一个

<!-- pdf-page: 203 -->
<!-- join-previous-paragraph -->
三分类的例子，这种方法会在输入空间中产生分类不明确的区域。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-2.png" alt="一对其余和一对一分类器中出现的分类不明确区域"><figcaption>图 4.2：试图由一组二分类判别函数构造 $K$ 分类判别函数，会产生图中绿色所示的分类不明确区域。左图使用两个判别函数，每个都用于区分类别 $\mathcal{C}_k$ 中的点与不属于 $\mathcal{C}_k$ 的点。右图使用三个判别函数，每个用于分开一对类别 $\mathcal{C}_k$ 和 $\mathcal{C}_j$。</figcaption><p class="figure-translation">not $\mathcal{C}_1$ → 不属于 $\mathcal{C}_1$；not $\mathcal{C}_2$ → 不属于 $\mathcal{C}_2$；? → 分类不明确。</p></figure>

另一种方法是引入 $K(K-1)/2$ 个二元判别函数，每一对可能的类别对应一个函数。这称为一对一（one-versus-one）分类器。然后，根据这些判别函数的多数投票结果对每个点分类。但这种方法也会遇到分类不明确区域的问题，如图 4.2 右图所示。

可以采用一个由 $K$ 个线性函数组成的 $K$ 分类判别函数，来避免这些困难。各线性函数形式为

$$
y_k(\mathbf{x})=\mathbf{w}_k^{\mathrm T}\mathbf{x}+w_{k0}
\tag{4.9}
$$

如果对于所有 $j\ne k$ 都有 $y_k(\mathbf{x})>y_j(\mathbf{x})$，就把点 $\mathbf{x}$ 分配到类别 $\mathcal{C}_k$。因此，类别 $\mathcal{C}_k$ 与 $\mathcal{C}_j$ 之间的决策边界由 $y_k(\mathbf{x})=y_j(\mathbf{x})$ 给出，对应于如下定义的 $(D-1)$ 维超平面：

$$
(\mathbf{w}_k-\mathbf{w}_j)^{\mathrm T}\mathbf{x}+(w_{k0}-w_{j0})=0.
\tag{4.10}
$$

这与第 4.1.1 节讨论的二分类决策边界形式相同，因此也具有相似的几何性质。

这种判别函数的决策区域总是单连通且凸的。为说明这一点，考虑同处于决策区域 $\mathcal{R}_k$ 内的两点 $\mathbf{x}_{\mathrm A}$ 和 $\mathbf{x}_{\mathrm B}$，如图 4.3 所示。连接这两点的线段上任一点 $\widehat{\mathbf{x}}$ 都可表示为

$$
\widehat{\mathbf{x}}=\lambda\mathbf{x}_{\mathrm A}+(1-\lambda)\mathbf{x}_{\mathrm B}
\tag{4.11}
$$

<!-- pdf-page: 204 -->

其中，$0\leqslant\lambda\leqslant1$。由判别函数的线性性质，有

$$
y_k(\widehat{\mathbf{x}})=\lambda y_k(\mathbf{x}_{\mathrm A})+(1-\lambda)y_k(\mathbf{x}_{\mathrm B}).
\tag{4.12}
$$

由于 $\mathbf{x}_{\mathrm A}$ 和 $\mathbf{x}_{\mathrm B}$ 都位于 $\mathcal{R}_k$ 内，对于所有 $j\ne k$，都有 $y_k(\mathbf{x}_{\mathrm A})>y_j(\mathbf{x}_{\mathrm A})$ 和 $y_k(\mathbf{x}_{\mathrm B})>y_j(\mathbf{x}_{\mathrm B})$。因此 $y_k(\widehat{\mathbf{x}})>y_j(\widehat{\mathbf{x}})$，所以 $\widehat{\mathbf{x}}$ 也位于 $\mathcal{R}_k$ 内。由此可见，$\mathcal{R}_k$ 是单连通且凸的。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-3.png" alt="多分类线性判别函数的凸决策区域"><figcaption>图 4.3：多分类线性判别函数的决策区域示意，红色线条表示决策边界。如果两点 $\mathbf{x}_{\mathrm A}$ 和 $\mathbf{x}_{\mathrm B}$ 都位于同一个决策区域 $\mathcal{R}_k$ 内，那么连接两点的线段上的任一点 $\widehat{\mathbf{x}}$ 也必定位于 $\mathcal{R}_k$ 内，因此决策区域必须是单连通且凸的。</figcaption></figure>

注意，对于二分类，既可以采用这里基于两个判别函数 $y_1(\mathbf{x})$ 和 $y_2(\mathbf{x})$ 的形式，也可以采用第 4.1.1 节基于单个判别函数 $y(\mathbf{x})$ 的更简单但等价的形式。

现在研究三种学习线性判别函数参数的方法，分别基于最小二乘、Fisher 线性判别和感知机算法。

### 4.1.3 用于分类的最小二乘

在第 3 章中，我们考虑了对参数呈线性关系的模型，并看到，最小化平方和误差函数可以得到参数的简单闭式解。因此，我们自然会想，是否可以把同样的方法用于分类问题。考虑一个具有 $K$ 个类别的一般分类问题，目标向量 $\mathbf{t}$ 采用 1-of-$K$ 二元编码。在这种情境下使用最小二乘的一个理由是，它近似给定输入向量时目标值的条件期望 $\mathbb{E}[\mathbf{t}\mid\mathbf{x}]$。对于这种二元编码，该条件期望就是类别后验概率组成的向量。但遗憾的是，这些概率通常近似得很差；由于线性模型的灵活性有限，近似值甚至可能超出区间 $(0,1)$，我们马上就会看到这一点。

每个类别 $\mathcal{C}_k$ 由各自的线性模型描述，即

$$
y_k(\mathbf{x})=\mathbf{w}_k^{\mathrm T}\mathbf{x}+w_{k0}
\tag{4.13}
$$

其中，$k=1,\ldots,K$。可以方便地用向量记号把它们合并，得到

$$
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm T}\widetilde{\mathbf{x}}
\tag{4.14}
$$

<!-- pdf-page: 205 -->

其中，$\widetilde{\mathbf{W}}$ 的第 $k$ 列是 $(D+1)$ 维向量 $\widetilde{\mathbf{w}}_k=(w_{k0},\mathbf{w}_k^{\mathrm T})^{\mathrm T}$，$\widetilde{\mathbf{x}}$ 是相应的扩充输入向量 $(1,\mathbf{x}^{\mathrm T})^{\mathrm T}$，其中包含形式输入 $x_0=1$。第 3.1 节详细讨论过这种表示。对于新的输入 $\mathbf{x}$，将其分配到输出 $y_k=\widetilde{\mathbf{w}}_k^{\mathrm T}\widetilde{\mathbf{x}}$ 最大的类别。

现在，像第 3 章的回归问题一样，通过最小化平方和误差函数来确定参数矩阵 $\widetilde{\mathbf{W}}$。考虑训练数据集 $\{\mathbf{x}_n,\mathbf{t}_n\}$，其中 $n=1,\ldots,N$。定义矩阵 $\mathbf{T}$，其第 $n$ 行为向量 $\mathbf{t}_n^{\mathrm T}$；再定义矩阵 $\widetilde{\mathbf{X}}$，其第 $n$ 行为 $\widetilde{\mathbf{x}}_n^{\mathrm T}$。于是，平方和误差函数可以写成

$$
E_D(\widetilde{\mathbf{W}})=\frac{1}{2}\operatorname{Tr}\left\{(\widetilde{\mathbf{X}}\widetilde{\mathbf{W}}-\mathbf{T})^{\mathrm T}(\widetilde{\mathbf{X}}\widetilde{\mathbf{W}}-\mathbf{T})\right\}.
\tag{4.15}
$$

令其对 $\widetilde{\mathbf{W}}$ 的导数等于零并整理，得到 $\widetilde{\mathbf{W}}$ 的解：

$$
\widetilde{\mathbf{W}}=(\widetilde{\mathbf{X}}^{\mathrm T}\widetilde{\mathbf{X}})^{-1}\widetilde{\mathbf{X}}^{\mathrm T}\mathbf{T}=\widetilde{\mathbf{X}}^{\dagger}\mathbf{T}
\tag{4.16}
$$

其中，$\widetilde{\mathbf{X}}^{\dagger}$ 是矩阵 $\widetilde{\mathbf{X}}$ 的伪逆，第 3.1.1 节已讨论过。由此得到判别函数

$$
\mathbf{y}(\mathbf{x})=\widetilde{\mathbf{W}}^{\mathrm T}\widetilde{\mathbf{x}}=\mathbf{T}^{\mathrm T}(\widetilde{\mathbf{X}}^{\dagger})^{\mathrm T}\widetilde{\mathbf{x}}.
\tag{4.17}
$$

多目标变量的最小二乘解有一个有趣的性质：如果训练集中的每个目标向量都满足某个线性约束

$$
\mathbf{a}^{\mathrm T}\mathbf{t}_n+b=0
\tag{4.18}
$$

其中 $\mathbf{a}$ 和 $b$ 是常量，那么，对任意 $\mathbf{x}$ 值，模型预测也满足同样的约束，即 <span class="margin-reference">习题 4.2</span>

$$
\mathbf{a}^{\mathrm T}\mathbf{y}(\mathbf{x})+b=0.
\tag{4.19}
$$

因此，若对 $K$ 个类别采用 1-of-$K$ 编码，模型预测就具有如下性质：对于任意 $\mathbf{x}$，$\mathbf{y}(\mathbf{x})$ 的各元素之和均为 1。不过，仅有这一求和约束，还不足以把模型输出解释为概率，因为它们没有被限制在区间 $(0,1)$ 内。

最小二乘方法给出了判别函数参数的精确闭式解。但是，即使只将其作为判别函数使用，即直接用它作决策而不赋予概率解释，它仍有一些严重问题。前面已经看到，最小二乘解对离群点缺乏鲁棒性，这同样适用于分类，如图 4.4 所示。<span class="margin-reference">第 2.3.7 节</span> 可以看到，右图新增的数据点使决策边界的位置发生明显变化，尽管这些点原本就能被左图中的决策边界正确分类。平方和误差函数会惩罚“过于正确”的预测，也就是那些处于决策边界正确一侧、而且距离

<!-- pdf-page: 206 -->
<!-- join-previous-paragraph -->
边界很远的预测。在第 7.1.2 节中，我们将考察其他几种分类误差函数，并看到它们没有这个问题。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-4.png" alt="加入离群点前后最小二乘和逻辑回归决策边界的比较"><figcaption>图 4.4：左图展示两个类别的数据，分别用红色叉号和蓝色圆圈表示，同时给出最小二乘方法得到的决策边界（品红色曲线），以及第 4.3.2 节将讨论的逻辑回归（logistic regression）模型得到的决策边界（绿色曲线）。右图展示在图的左下方增加数据点后的对应结果，说明最小二乘对离群点高度敏感，而逻辑回归并非如此。</figcaption></figure>

不过，最小二乘的问题可能比缺乏鲁棒性更严重，如图 4.5 所示。该图展示一个二维输入空间 $(x_1,x_2)$ 中的三类合成数据集，其特点是，线性决策边界可以很好地分开各类别。事实上，本章后面将介绍的逻辑回归方法给出了令人满意的解，如右图所示。但最小二乘解的结果很差，只有输入空间中很小的一块区域被分配给绿色类别。

回想一下，最小二乘对应于假设条件分布为高斯分布时的最大似然，而二元目标向量的分布显然与高斯分布相差很大；这样，最小二乘的失败就不足为奇了。采用更合适的概率模型，能够得到比最小二乘性质好得多的分类方法。不过，目前我们先继续研究其他非概率方法，用它们来确定线性分类模型中的参数。

### 4.1.4 Fisher 线性判别

理解线性分类模型的一种方式，是把它看作降维。先考虑二分类，假设把 $D$

<!-- pdf-page: 207 -->
<!-- join-previous-paragraph -->
维输入向量 $\mathbf{x}$ 投影到一维，采用

$$
y=\mathbf{w}^{\mathrm T}\mathbf{x}.
\tag{4.20}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-5.png" alt="三分类数据上最小二乘与逻辑回归决策区域的比较"><figcaption>图 4.5：一个包含三个类别的合成数据集，训练数据点分别用红色（×）、绿色（＋）和蓝色（○）表示。线条表示决策边界，背景颜色表示各决策区域对应的类别。左图是使用最小二乘判别函数的结果：分配给绿色类别的输入空间区域过小，因此该类大多数点被错误分类。右图是使用第 4.3.2 节所述逻辑回归的结果，训练数据均得到正确分类。</figcaption></figure>

如果在 $y$ 上设定一个阈值，把 $y\geqslant-w_0$ 分到类别 $\mathcal{C}_1$，否则分到类别 $\mathcal{C}_2$，就得到前一节讨论的标准线性分类器。通常，投影到一维会造成相当大的信息损失，原本在 $D$ 维空间中分得很开的类别，投影后可能严重重叠。不过，通过调整权重向量 $\mathbf{w}$ 的各个分量，可以选择使类别分离程度最大的投影。首先，考虑一个二分类问题：类别 $\mathcal{C}_1$ 有 $N_1$ 个点，类别 $\mathcal{C}_2$ 有 $N_2$ 个点，两类的均值向量为

$$
\mathbf{m}_1=\frac{1}{N_1}\sum_{n\in\mathcal{C}_1}\mathbf{x}_n,\qquad \mathbf{m}_2=\frac{1}{N_2}\sum_{n\in\mathcal{C}_2}\mathbf{x}_n.
\tag{4.21}
$$

投影到 $\mathbf{w}$ 后，衡量类别分离程度最简单的方法，是计算两类投影均值之间的距离。这提示我们，可以选择 $\mathbf{w}$，使下式最大：

$$
m_2-m_1=\mathbf{w}^{\mathrm T}(\mathbf{m}_2-\mathbf{m}_1)
\tag{4.22}
$$

其中

$$
m_k=\mathbf{w}^{\mathrm T}\mathbf{m}_k
\tag{4.23}
$$

<!-- pdf-page: 208 -->

是类别 $\mathcal{C}_k$ 的数据投影后的均值。但是，只要增大 $\mathbf{w}$ 的长度，就能使这一表达式任意大。为解决这个问题，可以约束 $\mathbf{w}$ 的长度为 1，即 $\sum_i w_i^2=1$。使用拉格朗日乘子进行约束最大化，就得到 $\mathbf{w}\propto(\mathbf{m}_2-\mathbf{m}_1)$。<span class="margin-reference">附录 E；习题 4.4</span> 不过，这种方法仍然有问题，如图 4.6 所示。图中的两个类别在原始二维空间 $(x_1,x_2)$ 中分得很开，但投影到连接两类均值的直线上后，却出现了明显重叠。产生这个问题的原因是，类分布的协方差具有很强的非对角成分。Fisher 的思路是，最大化一个函数，使投影后的类均值相距较远，同时使每个类别内部的方差较小，从而尽量减小类别之间的重叠。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-6.png" alt="按均值连线投影与 Fisher 线性判别投影的类分离效果比较"><figcaption>图 4.6：左图展示两个类别的样本（分别为红色和蓝色），以及把它们投影到两类均值的连线上所得到的直方图。可以看到，在投影空间中两类有明显重叠。右图给出基于 Fisher 线性判别的相应投影，类别分离程度显著提高。</figcaption></figure>

投影公式（4.20）把 $\mathbf{x}$ 空间中的带标签数据点集，变为一维空间 $y$ 中的带标签数据集。因此，类别 $\mathcal{C}_k$ 的数据变换后的类内方差为

$$
s_k^2=\sum_{n\in\mathcal{C}_k}(y_n-m_k)^2
\tag{4.24}
$$

其中，$y_n=\mathbf{w}^{\mathrm T}\mathbf{x}_n$。整个数据集的总类内方差可以简单定义为 $s_1^2+s_2^2$。Fisher 准则定义为类间方差与类内方差的比值，即

$$
J(\mathbf{w})=\frac{(m_2-m_1)^2}{s_1^2+s_2^2}.
\tag{4.25}
$$

利用式（4.20）、（4.23）和（4.24），可以把 Fisher 准则改写成显式依赖于 $\mathbf{w}$ 的形式：<span class="margin-reference">习题 4.5</span>

<!-- pdf-page: 209 -->

$$
J(\mathbf{w})=\frac{\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm B}\mathbf{w}}{\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm W}\mathbf{w}}
\tag{4.26}
$$

其中，$\mathbf{S}_{\mathrm B}$ 是类间协方差矩阵，定义为

$$
\mathbf{S}_{\mathrm B}=(\mathbf{m}_2-\mathbf{m}_1)(\mathbf{m}_2-\mathbf{m}_1)^{\mathrm T}
\tag{4.27}
$$

而 $\mathbf{S}_{\mathrm W}$ 是总类内协方差矩阵，定义为

$$
\mathbf{S}_{\mathrm W}=\sum_{n\in\mathcal{C}_1}(\mathbf{x}_n-\mathbf{m}_1)(\mathbf{x}_n-\mathbf{m}_1)^{\mathrm T}+\sum_{n\in\mathcal{C}_2}(\mathbf{x}_n-\mathbf{m}_2)(\mathbf{x}_n-\mathbf{m}_2)^{\mathrm T}.
\tag{4.28}
$$

对式（4.26）关于 $\mathbf{w}$ 求导，可以得到，当下式成立时 $J(\mathbf{w})$ 最大：

$$
(\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm B}\mathbf{w})\mathbf{S}_{\mathrm W}\mathbf{w}=(\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm W}\mathbf{w})\mathbf{S}_{\mathrm B}\mathbf{w}.
\tag{4.29}
$$

由式（4.27）可知，$\mathbf{S}_{\mathrm B}\mathbf{w}$ 总是沿着 $(\mathbf{m}_2-\mathbf{m}_1)$ 的方向。另外，我们只关心 $\mathbf{w}$ 的方向，不关心其长度，因此可以舍去标量因子 $(\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm B}\mathbf{w})$ 和 $(\mathbf{w}^{\mathrm T}\mathbf{S}_{\mathrm W}\mathbf{w})$。在式（4.29）两边左乘 $\mathbf{S}_{\mathrm W}^{-1}$，得到

$$
\mathbf{w}\propto\mathbf{S}_{\mathrm W}^{-1}(\mathbf{m}_2-\mathbf{m}_1).
\tag{4.30}
$$

注意，如果类内协方差是各向同性的，即 $\mathbf{S}_{\mathrm W}$ 正比于单位矩阵，那么 $\mathbf{w}$ 就正比于两类均值之差，与前面的讨论一致。

结果（4.30）称为 Fisher 线性判别（Fisher's linear discriminant）。严格来说，它本身并不是判别函数，而是把数据投影到一维时，对投影方向的一种具体选择。不过，随后可以利用投影后的数据构造判别函数：选择阈值 $y_0$，若新数据点满足 $y(\mathbf{x})\geqslant y_0$，就分到 $\mathcal{C}_1$，否则分到 $\mathcal{C}_2$。例如，可以用高斯分布对类条件密度 $p(y\mid\mathcal{C}_k)$ 建模，再使用第 1.2.4 节的方法，通过最大似然确定高斯分布的参数。得到投影后各类别的高斯近似后，第 1.5.1 节的方法就能给出最优阈值的表达式。高斯假设的一个依据来自中心极限定理：注意到 $y=\mathbf{w}^{\mathrm T}\mathbf{x}$ 是一组随机变量的和。

### 4.1.5 与最小二乘的关系

用最小二乘确定线性判别函数，是为了使模型预测尽可能接近一组目标值。相比之下，Fisher 准则要求输出空间中的类别分离程度最大。考察这两种方法的关系很有意义。特别是，我们将说明，对于二分类问题，Fisher 准则可以作为最小二乘的一个特例得到。

到目前为止，我们对目标值采用的是 1-of-$K$ 编码。但如果采用略有不同的目标编码，那么权重的最小二乘解就

<!-- pdf-page: 210 -->
<!-- join-previous-paragraph -->
等价于 Fisher 解（Duda and Hart, 1973）。具体来说，对类别 $\mathcal{C}_1$，将目标值设为 $N/N_1$，其中 $N_1$ 是类别 $\mathcal{C}_1$ 中的模式数，$N$ 是模式总数。这个目标值近似等于类别 $\mathcal{C}_1$ 先验概率的倒数。对于类别 $\mathcal{C}_2$，将目标值设为 $-N/N_2$，其中 $N_2$ 是类别 $\mathcal{C}_2$ 中的模式数。平方和误差函数可以写成

$$
E=\frac{1}{2}\sum_{n=1}^{N}(\mathbf{w}^{\mathrm T}\mathbf{x}_n+w_0-t_n)^2.
\tag{4.31}
$$

令 $E$ 对 $w_0$ 和 $\mathbf{w}$ 的导数分别为零，得到

$$
\sum_{n=1}^{N}(\mathbf{w}^{\mathrm T}\mathbf{x}_n+w_0-t_n)=0
\tag{4.32}
$$

$$
\sum_{n=1}^{N}(\mathbf{w}^{\mathrm T}\mathbf{x}_n+w_0-t_n)\mathbf{x}_n=0.
\tag{4.33}
$$

由式（4.32），再利用所选择的目标编码 $t_n$，得到偏置的表达式

$$
w_0=-\mathbf{w}^{\mathrm T}\mathbf{m}
\tag{4.34}
$$

其中使用了

$$
\sum_{n=1}^{N}t_n=N_1\frac{N}{N_1}-N_2\frac{N}{N_2}=0
\tag{4.35}
$$

这里，$\mathbf{m}$ 是整个数据集的均值，定义为

$$
\mathbf{m}=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n=\frac{1}{N}(N_1\mathbf{m}_1+N_2\mathbf{m}_2).
\tag{4.36}
$$

经过直接的代数运算，再次利用所选择的 $t_n$，第二个方程（4.33）变为 <span class="margin-reference">习题 4.6</span>

$$
\left(\mathbf{S}_{\mathrm W}+\frac{N_1N_2}{N}\mathbf{S}_{\mathrm B}\right)\mathbf{w}=N(\mathbf{m}_1-\mathbf{m}_2)
\tag{4.37}
$$

其中，$\mathbf{S}_{\mathrm W}$ 由式（4.28）定义，$\mathbf{S}_{\mathrm B}$ 由式（4.27）定义，并已利用式（4.34）代入偏置。由式（4.27）可知，$\mathbf{S}_{\mathrm B}\mathbf{w}$ 总是沿着 $(\mathbf{m}_2-\mathbf{m}_1)$ 的方向。因此可以写成

$$
\mathbf{w}\propto\mathbf{S}_{\mathrm W}^{-1}(\mathbf{m}_2-\mathbf{m}_1)
\tag{4.38}
$$

其中忽略了不相关的比例因子。因此，这个权重向量与由 Fisher 准则得到的权重向量一致。另外，我们还求得了式（4.34）所给出的偏置 $w_0$。它说明，若新向量 $\mathbf{x}$ 满足 $y(\mathbf{x})=\mathbf{w}^{\mathrm T}(\mathbf{x}-\mathbf{m})>0$，就应分到类别 $\mathcal{C}_1$，否则分到类别 $\mathcal{C}_2$。

<!-- pdf-page: 211 -->

### 4.1.6 多分类的 Fisher 判别

现在考虑把 Fisher 判别推广到 $K>2$ 个类别，并假设输入空间维数 $D$ 大于类别数 $K$。接着，引入 $D'>1$ 个线性“特征” $y_k=\mathbf{w}_k^{\mathrm T}\mathbf{x}$，其中 $k=1,\ldots,D'$。可以方便地把这些特征值组成向量 $\mathbf{y}$。同样，可以把权重向量 $\{\mathbf{w}_k\}$ 看作矩阵 $\mathbf{W}$ 的各列，于是

$$
\mathbf{y}=\mathbf{W}^{\mathrm T}\mathbf{x}.
\tag{4.39}
$$

注意，这里在定义 $\mathbf{y}$ 时同样没有加入偏置参数。由式（4.28），类内协方差矩阵推广到 $K$ 个类别后为

$$
\mathbf{S}_{\mathrm W}=\sum_{k=1}^{K}\mathbf{S}_k
\tag{4.40}
$$

其中

$$
\mathbf{S}_k=\sum_{n\in\mathcal{C}_k}(\mathbf{x}_n-\mathbf{m}_k)(\mathbf{x}_n-\mathbf{m}_k)^{\mathrm T}
\tag{4.41}
$$

$$
\mathbf{m}_k=\frac{1}{N_k}\sum_{n\in\mathcal{C}_k}\mathbf{x}_n
\tag{4.42}
$$

而 $N_k$ 是类别 $\mathcal{C}_k$ 中的模式数。为推广类间协方差矩阵，我们采用 Duda and Hart（1973）的方法，先考虑总协方差矩阵

$$
\mathbf{S}_{\mathrm T}=\sum_{n=1}^{N}(\mathbf{x}_n-\mathbf{m})(\mathbf{x}_n-\mathbf{m})^{\mathrm T}
\tag{4.43}
$$

其中，$\mathbf{m}$ 是整个数据集的均值，

$$
\mathbf{m}=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n=\frac{1}{N}\sum_{k=1}^{K}N_k\mathbf{m}_k
\tag{4.44}
$$

而 $N=\sum_k N_k$ 是数据点总数。总协方差矩阵可以分解为式（4.40）、（4.41）给出的类内协方差矩阵，加上一个额外的矩阵 $\mathbf{S}_{\mathrm B}$；我们把后者作为类间协方差的度量：

$$
\mathbf{S}_{\mathrm T}=\mathbf{S}_{\mathrm W}+\mathbf{S}_{\mathrm B}
\tag{4.45}
$$

其中

$$
\mathbf{S}_{\mathrm B}=\sum_{k=1}^{K}N_k(\mathbf{m}_k-\mathbf{m})(\mathbf{m}_k-\mathbf{m})^{\mathrm T}.
\tag{4.46}
$$

<!-- pdf-page: 212 -->

这些协方差矩阵都定义在原始的 $\mathbf{x}$ 空间中。现在可以在投影后的 $D'$ 维 $\mathbf{y}$ 空间中定义类似的矩阵：

$$
\mathbf{s}_{\mathrm W}=\sum_{k=1}^{K}\sum_{n\in\mathcal{C}_k}(\mathbf{y}_n-\boldsymbol{\mu}_k)(\mathbf{y}_n-\boldsymbol{\mu}_k)^{\mathrm T}
\tag{4.47}
$$

以及

$$
\mathbf{s}_{\mathrm B}=\sum_{k=1}^{K}N_k(\boldsymbol{\mu}_k-\boldsymbol{\mu})(\boldsymbol{\mu}_k-\boldsymbol{\mu})^{\mathrm T}
\tag{4.48}
$$

其中

$$
\boldsymbol{\mu}_k=\frac{1}{N_k}\sum_{n\in\mathcal{C}_k}\mathbf{y}_n,\qquad \boldsymbol{\mu}=\frac{1}{N}\sum_{k=1}^{K}N_k\boldsymbol{\mu}_k.
\tag{4.49}
$$

同样，我们希望构造一个标量，使它在类间协方差大、类内协方差小时取较大的值。此时有许多可选准则（Fukunaga, 1990）。其中一个例子是

$$
J(\mathbf{W})=\operatorname{Tr}\{\mathbf{s}_{\mathrm W}^{-1}\mathbf{s}_{\mathrm B}\}.
\tag{4.50}
$$

可以把这个准则改写成投影矩阵 $\mathbf{W}$ 的显式函数：

$$
J(\mathbf{w})=\operatorname{Tr}\{(\mathbf{W}\mathbf{S}_{\mathrm W}\mathbf{W}^{\mathrm T})^{-1}(\mathbf{W}\mathbf{S}_{\mathrm B}\mathbf{W}^{\mathrm T})\}.
\tag{4.51}
$$

这类准则的最大化在思路上直接，但运算稍繁，Fukunaga（1990）作了详细讨论。权重值由 $\mathbf{S}_{\mathrm W}^{-1}\mathbf{S}_{\mathrm B}$ 中对应最大 $D'$ 个特征值的特征向量确定。

所有这些准则都有一个重要的共同结果，需要强调。首先，由式（4.46）可见，$\mathbf{S}_{\mathrm B}$ 是 $K$ 个矩阵的和，每个矩阵都是两个向量的外积，因此秩为 1。另外，由于约束（4.44），其中只有 $K-1$ 个矩阵是独立的。所以，$\mathbf{S}_{\mathrm B}$ 的秩最多为 $K-1$，非零特征值也最多有 $K-1$ 个。这表明，投影到 $\mathbf{S}_{\mathrm B}$ 的特征向量张成的 $(K-1)$ 维子空间，不会改变 $J(\mathbf{w})$ 的值。因此，用这种方法不可能找到多于 $K-1$ 个线性“特征”（Fukunaga, 1990）。

### 4.1.7 感知机算法

线性判别模型的另一个例子是 Rosenblatt（1962）的感知机（perceptron），它在模式识别算法的发展史上占有重要地位。感知机是一个二分类模型：先通过固定的非线性变换，把输入向量 $\mathbf{x}$ 转为特征向量 $\boldsymbol{\phi}(\mathbf{x})$，再由此构造如下形式的广义线性模型：

$$
y(\mathbf{x})=f(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}))
\tag{4.52}
$$

<!-- pdf-page: 213 -->

其中，非线性激活函数 $f(\cdot)$ 是如下形式的阶跃函数：

$$
f(a)=\begin{cases}+1,&a\geqslant0\\-1,&a<0.\end{cases}
\tag{4.53}
$$

向量 $\boldsymbol{\phi}(\mathbf{x})$ 通常包含偏置分量 $\phi_0(\mathbf{x})=1$。前面讨论二分类问题时，主要采用 $t\in\{0,1\}$ 的目标编码，这适合概率模型。但对于感知机，把类别 $\mathcal{C}_1$ 的目标值设为 $t=+1$、类别 $\mathcal{C}_2$ 的目标值设为 $t=-1$ 更方便，也与激活函数的选择一致。

用于确定感知机参数 $\mathbf{w}$ 的算法，最容易从误差函数最小化的角度导出。一个自然的误差函数选择，是错误分类的模式总数。但这样无法得到简单的学习算法，因为误差是 $\mathbf{w}$ 的分段常数函数；每当 $\mathbf{w}$ 的变化使决策边界跨过一个数据点时，误差就会发生跳变。因此，不能利用误差函数的梯度来更新 $\mathbf{w}$，因为这个梯度几乎处处为零。

所以，我们考虑另一个误差函数，称为感知机准则（perceptron criterion）。为推导这个准则，注意我们希望找到一个权重向量 $\mathbf{w}$，使类别 $\mathcal{C}_1$ 中的模式 $\mathbf{x}_n$ 满足 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)>0$，类别 $\mathcal{C}_2$ 中的模式满足 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)<0$。使用 $t\in\{-1,+1\}$ 的目标编码后，就希望所有模式都满足 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)t_n>0$。感知机准则把正确分类的模式的误差设为零，而对于错误分类的模式 $\mathbf{x}_n$，则试图最小化 $-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)t_n$。因此，感知机准则为

$$
E_{\mathrm P}(\mathbf{w})=-\sum_{n\in\mathcal{M}}\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n t_n
\tag{4.54}
$$

<aside class="biography"><p><strong>弗兰克·罗森布拉特（Frank Rosenblatt）</strong><br>1928–1969</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-rosenblatt.png" alt="弗兰克·罗森布拉特与感知机设备"><p class="figure-translation">perceptron → 感知机。</p><p>Rosenblatt 的感知机在机器学习史上发挥了重要作用。最初，他于 1957 年在康奈尔大学的一台 IBM 704 计算机上模拟感知机；到 20 世纪 60 年代初，他已建造专用硬件，直接并行实现感知机学习。他的许多想法集中写在 1962 年出版的《神经动力学原理：感知机与脑机制理论》（Principles of Neurodynamics: Perceptrons and the Theory of Brain Mechanisms）中。Rosenblatt 的工作受到马文·明斯基（Marvin Minksy）的批评；明斯基的观点发表在他与 Seymour Papert 合著的《感知机》（Perceptrons）一书中。当时，这本书被广泛误读为证明了神经网络存在致命缺陷，只能学习线性可分问题的解。实际上，它只对感知机这类单层网络证明了这些局限，并且只是猜想这些局限也适用于更一般的网络模型，而这个猜想是错误的。但遗憾的是，这本书促成了神经计算研究经费的大幅减少，直到 20 世纪 80 年代中期，情况才发生逆转。如今，神经网络已经有数百种、甚至数千种广泛使用的应用；其中，手写识别和信息检索等领域的应用，已成为数百万人日常使用的工具。</p></aside>

<!-- pdf-page: 214 -->

其中，$\mathcal{M}$ 表示所有错误分类模式的集合。对于某个被错误分类的模式，在 $\mathbf{w}$ 空间中使它被错误分类的区域内，它对误差的贡献是 $\mathbf{w}$ 的线性函数；在使它被正确分类的区域内，误差贡献为零。因此，总误差函数是分段线性的。

现在对这个误差函数应用随机梯度下降算法。<span class="margin-reference">第 3.1.3 节</span> 权重向量 $\mathbf{w}$ 按如下方式更新：

$$
\mathbf{w}^{(\tau+1)}=\mathbf{w}^{(\tau)}-\eta\nabla E_{\mathrm P}(\mathbf{w})=\mathbf{w}^{(\tau)}+\eta\boldsymbol{\phi}_n t_n
\tag{4.55}
$$

其中，$\eta$ 是学习率参数，整数 $\tau$ 用来标记算法的步骤。由于把 $\mathbf{w}$ 乘以一个常数不会改变感知机函数 $y(\mathbf{x},\mathbf{w})$，因此不失一般性，可以把学习率参数 $\eta$ 设为 1。注意，在训练过程中，随着权重向量的变化，被错误分类的模式集合也会改变。

感知机学习算法可以作如下简单解释。依次循环遍历训练模式，对每个模式 $\mathbf{x}_n$，计算感知机函数（4.52）。如果分类正确，权重向量保持不变；如果分类错误，对于类别 $\mathcal{C}_1$，就在当前权重向量 $\mathbf{w}$ 上加上向量 $\boldsymbol{\phi}(\mathbf{x}_n)$，而对于类别 $\mathcal{C}_2$，则从 $\mathbf{w}$ 中减去向量 $\boldsymbol{\phi}(\mathbf{x}_n)$。图 4.7 展示了感知机学习算法。

考虑感知机学习算法中一次更新的影响，可以看到，被错误分类的模式对误差的贡献会减小，因为由式（4.55），有

$$
-\mathbf{w}^{(\tau+1){\mathrm T}}\boldsymbol{\phi}_n t_n=-\mathbf{w}^{(\tau){\mathrm T}}\boldsymbol{\phi}_n t_n-(\boldsymbol{\phi}_n t_n)^{\mathrm T}\boldsymbol{\phi}_n t_n<-\mathbf{w}^{(\tau){\mathrm T}}\boldsymbol{\phi}_n t_n
\tag{4.56}
$$

其中设定了 $\eta=1$，并利用了 $\|\boldsymbol{\phi}_n t_n\|^2>0$。当然，这并不意味着其他错误分类模式对误差函数的贡献也会减小。另外，权重向量的变化还可能使原本正确分类的模式变成错误分类。因此，感知机学习规则并不保证每一步都减小总误差函数。

不过，感知机收敛定理（perceptron convergence theorem）指出：如果存在精确解，换言之，训练数据集线性可分，那么感知机学习算法保证在有限步内找到精确解。该定理的证明可见 Rosenblatt（1962）、Block（1962）、Nilsson（1965）、Minsky and Papert（1969）、Hertz et al.（1991）以及 Bishop（1995a）等文献。但要注意，达到收敛所需的步骤数仍可能很多；在实践中，在收敛之前，我们无法区分问题本身不可分，还是仅仅收敛缓慢。

即使数据集线性可分，也可能存在许多解，最终找到哪一个，取决于参数的初始化以及数据点的输入顺序。另外，对于非线性可分的数据集，感知机学习算法永远不会收敛。

<!-- pdf-page: 215 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-7.png" alt="感知机通过依次更新错误分类点而收敛的四步示意"><figcaption>图 4.7：感知机学习算法的收敛过程，展示二维特征空间 $(\phi_1,\phi_2)$ 中两个类别的数据点（红色和蓝色）。左上图中的黑色箭头表示初始参数向量 $\mathbf{w}$，黑色直线表示相应决策边界；箭头指向被判为红色类别的决策区域。绿色圆圈标出的数据点被错误分类，因此把它的特征向量加到当前权重向量上，得到右上图所示的新决策边界。左下图中，绿色圆圈标出接下来处理的错误分类点，再次把它的特征向量加到权重向量上，得到右下图的决策边界，此时所有数据点都被正确分类。</figcaption></figure>

<!-- pdf-page: 216 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-8.png" alt="Mark 1 感知机的相机、接线板和自适应权重硬件"><figcaption>图 4.8：Mark 1 感知机硬件。左侧照片展示了如何用一个简单的相机系统获取输入：强光照亮输入场景，这里是一个印刷字符，再把图像聚焦到一个 $20\times20$ 的硫化镉光电池阵列上，得到一幅原始的 400 像素图像。感知机还配有接线板，如中间照片所示，可以尝试不同的输入特征配置。这些接线往往随机连接，用来说明感知机能够学习，而不需要像现代数字计算机那样精确布线。右侧照片展示了一个自适应权重机架。每个权重由电动机驱动的旋转可变电阻实现，这种电阻也称电位器，因此学习算法可以自动调整权重值。</figcaption></figure>

除了学习算法存在困难外，感知机既不能给出概率输出，也不容易推广到 $K>2$ 个类别。不过，它最重要的局限在于：与本章和上一章讨论的所有模型一样，它建立在固定基函数的线性组合之上。关于感知机局限性的更详细讨论，见 Minsky and Papert（1969）和 Bishop（1995a）。

Rosenblatt 曾用电动机驱动的可变电阻实现自适应参数 $w_j$，由此建造感知机的模拟硬件，见图 4.8。输入来自一个基于光传感器阵列的简单相机系统；基函数 $\boldsymbol{\phi}$ 可以有多种选择，例如，可以对从输入图像随机选取的像素子集应用简单的固定函数。典型应用是学习区分简单形状或字符。

在感知机发展的同时，Widrow 及其同事也在研究一个密切相关的系统，称为 adaline，是“adaptive linear element”（自适应线性单元）的缩写。它的模型函数形式与感知机相同，但采用不同的训练方法（Widrow and Hoff, 1960；Widrow and Lehr, 1990）。

## 4.2 概率生成式模型

接下来从概率角度考察分类，说明如何从对数据分布的简单假设，得到具有线性决策边界的模型。第 1.5.4 节讨论了分类中的判别式方法与生成式方法的区别。这里采用生成式

<!-- pdf-page: 217 -->
<!-- join-previous-paragraph -->
方法：对类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 和类别先验 $p(\mathcal{C}_k)$ 建模，再利用贝叶斯定理计算后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$。

先考虑二分类。类别 $\mathcal{C}_1$ 的后验概率可以写成

$$
\begin{aligned}
p(\mathcal{C}_1\mid\mathbf{x})&=\frac{p(\mathbf{x}\mid\mathcal{C}_1)p(\mathcal{C}_1)}{p(\mathbf{x}\mid\mathcal{C}_1)p(\mathcal{C}_1)+p(\mathbf{x}\mid\mathcal{C}_2)p(\mathcal{C}_2)}\\
&=\frac{1}{1+\exp(-a)}=\sigma(a)
\end{aligned}
\tag{4.57}
$$

其中定义

$$
a=\ln\frac{p(\mathbf{x}\mid\mathcal{C}_1)p(\mathcal{C}_1)}{p(\mathbf{x}\mid\mathcal{C}_2)p(\mathcal{C}_2)}
\tag{4.58}
$$

而 $\sigma(a)$ 是 logistic sigmoid 函数，定义为

$$
\sigma(a)=\frac{1}{1+\exp(-a)}
\tag{4.59}
$$

其曲线如图 4.9 所示。“sigmoid”意为 S 形。这类函数有时也称为“压缩函数”（squashing function），因为它把整条实数轴映射到一个有限区间。前几章已经遇到过 logistic sigmoid，它在许多分类算法中都起着重要作用。很容易验证，它满足以下对称性质：

$$
\sigma(-a)=1-\sigma(a).
\tag{4.60}
$$

logistic sigmoid 的反函数为

$$
a=\ln\left(\frac{\sigma}{1-\sigma}\right)
\tag{4.61}
$$

称为 logit 函数。它表示两个类别概率之比的对数 $\ln[p(\mathcal{C}_1\mid\mathbf{x})/p(\mathcal{C}_2\mid\mathbf{x})]$，也称对数几率（log odds）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-9.png" alt="logistic sigmoid 函数与缩放后 probit 函数的曲线比较"><figcaption>图 4.9：式（4.59）定义的 logistic sigmoid 函数 $\sigma(a)$（红色），以及缩放后的 probit 函数 $\Phi(\lambda a)$（蓝色虚线），其中 $\lambda^2=\pi/8$，$\Phi(a)$ 由式（4.114）定义。选择缩放因子 $\pi/8$，使两条曲线在 $a=0$ 处的导数相等。</figcaption></figure>

<!-- pdf-page: 218 -->

注意，在式（4.57）中，我们只是把后验概率改写为等价形式，因此 logistic sigmoid 的出现似乎并没有带来实质内容。但只要 $a(\mathbf{x})$ 具有简单的函数形式，这个表达就有意义。我们很快会讨论 $a(\mathbf{x})$ 是 $\mathbf{x}$ 的线性函数的情形；这时，后验概率就由广义线性模型描述。

对于 $K>2$ 个类别，有

$$
\begin{aligned}
p(\mathcal{C}_k\mid\mathbf{x})&=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{\sum_j p(\mathbf{x}\mid\mathcal{C}_j)p(\mathcal{C}_j)}\\
&=\frac{\exp(a_k)}{\sum_j\exp(a_j)}
\end{aligned}
\tag{4.62}
$$

这称为归一化指数（normalized exponential），可以看作 logistic sigmoid 的多分类推广。其中，$a_k$ 定义为

$$
a_k=\ln p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k).
\tag{4.63}
$$

归一化指数也称为 softmax 函数，因为它相当于“max”函数的平滑版本：如果对于所有 $j\ne k$ 都有 $a_k\gg a_j$，则 $p(\mathcal{C}_k\mid\mathbf{x})\simeq1$，且 $p(\mathcal{C}_j\mid\mathbf{x})\simeq0$。

现在研究为类条件密度选择具体形式后会得到什么结果。先考虑连续输入变量 $\mathbf{x}$，再简要讨论离散输入。

### 4.2.1 连续输入

假设类条件密度为高斯分布，考察相应的后验概率形式。首先，假设所有类别共享同一个协方差矩阵。于是，类别 $\mathcal{C}_k$ 的密度为

$$
p(\mathbf{x}\mid\mathcal{C}_k)=\frac{1}{(2\pi)^{D/2}}\frac{1}{|\boldsymbol{\Sigma}|^{1/2}}\exp\left\{-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu}_k)^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu}_k)\right\}.
\tag{4.64}
$$

先考虑二分类。由式（4.57）和（4.58），有

$$
p(\mathcal{C}_1\mid\mathbf{x})=\sigma(\mathbf{w}^{\mathrm T}\mathbf{x}+w_0)
\tag{4.65}
$$

其中定义

$$
\mathbf{w}=\boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu}_1-\boldsymbol{\mu}_2)
\tag{4.66}
$$

$$
w_0=-\frac{1}{2}\boldsymbol{\mu}_1^{\mathrm T}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_1+\frac{1}{2}\boldsymbol{\mu}_2^{\mathrm T}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_2+\ln\frac{p(\mathcal{C}_1)}{p(\mathcal{C}_2)}.
\tag{4.67}
$$

可以看到，由于假设各类别具有相同的协方差矩阵，高斯密度指数中关于 $\mathbf{x}$ 的二次项相互抵消，使 logistic sigmoid 的自变量成为 $\mathbf{x}$ 的线性函数。图 4.10 用二维输入空间 $\mathbf{x}$ 的情形说明了这个结果。得到的

<!-- pdf-page: 219 -->
<!-- join-previous-paragraph -->
决策边界对应于后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 保持不变的曲面，因此由 $\mathbf{x}$ 的线性函数给出，也就是说，决策边界在输入空间中是线性的。先验概率 $p(\mathcal{C}_k)$ 只通过偏置参数 $w_0$ 起作用，因此改变先验会使决策边界平行移动；更一般地，也会使后验概率保持不变的那些平行等值线平移。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-10.png" alt="两个高斯类条件密度及对应 logistic 后验概率曲面"><figcaption>图 4.10：左图展示两个类别的类条件密度，分别用红色和蓝色表示。右图是相应的后验概率 $p(\mathcal{C}_1\mid\mathbf{x})$，它等于对 $\mathbf{x}$ 的线性函数应用 logistic sigmoid。右图曲面的颜色由红、蓝两种颜色混合而成：红色比例为 $p(\mathcal{C}_1\mid\mathbf{x})$，蓝色比例为 $p(\mathcal{C}_2\mid\mathbf{x})=1-p(\mathcal{C}_1\mid\mathbf{x})$。</figcaption></figure>

对于一般的 $K$ 分类情形，由式（4.62）和（4.63），有

$$
a_k(\mathbf{x})=\mathbf{w}_k^{\mathrm T}\mathbf{x}+w_{k0}
\tag{4.68}
$$

其中定义

$$
\mathbf{w}_k=\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k
\tag{4.69}
$$

$$
w_{k0}=-\frac{1}{2}\boldsymbol{\mu}_k^{\mathrm T}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}_k+\ln p(\mathcal{C}_k).
\tag{4.70}
$$

同样，由于共享协方差使二次项相互抵消，$a_k(\mathbf{x})$ 是 $\mathbf{x}$ 的线性函数。对应于最小错误分类率的决策边界，出现在两个最大的后验概率相等的位置，因此仍由 $\mathbf{x}$ 的线性函数定义，得到的仍是广义线性模型。

如果放宽共享协方差矩阵的假设，允许每个类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 都有自己的协方差矩阵 $\boldsymbol{\Sigma}_k$，前面的抵消就不再发生，会得到 $\mathbf{x}$ 的二次函数，从而产生二次判别函数（quadratic discriminant）。图 4.11 展示了线性和二次决策边界。

<!-- pdf-page: 220 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/a-fig-4-11.png" alt="共享或不同协方差下三类高斯模型的线性与二次决策边界"><figcaption>图 4.11：左图展示三个高斯类别的类条件密度，分别为红色、绿色和蓝色，其中红色和绿色类别具有相同的协方差矩阵。右图展示相应的后验概率，RGB 颜色向量表示三个类别各自的后验概率，同时标出了决策边界。注意，红色和绿色类别的协方差矩阵相同，它们之间的边界是线性的；其余类别对之间的边界则是二次的。</figcaption></figure>

### 4.2.2 最大似然解

一旦为类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 指定了参数化函数形式，就可以用最大似然确定参数值以及类别先验概率 $p(\mathcal{C}_k)$。这需要一个同时包含 $\mathbf{x}$ 的观测值及其相应类别标签的数据集。

先考虑二分类，每个类别的类条件密度都是高斯分布，并共享协方差矩阵。假设有数据集 $\{\mathbf{x}_n,t_n\}$，其中 $n=1,\ldots,N$。这里，$t_n=1$ 表示类别 $\mathcal{C}_1$，$t_n=0$ 表示类别 $\mathcal{C}_2$。记类别先验概率为 $p(\mathcal{C}_1)=\pi$，于是 $p(\mathcal{C}_2)=1-\pi$。对于来自类别 $\mathcal{C}_1$ 的数据点 $\mathbf{x}_n$，有 $t_n=1$，因此

$$
p(\mathbf{x}_n,\mathcal{C}_1)=p(\mathcal{C}_1)p(\mathbf{x}_n\mid\mathcal{C}_1)=\pi\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_1,\boldsymbol{\Sigma}).
$$

同样，对于类别 $\mathcal{C}_2$，有 $t_n=0$，因此

$$
p(\mathbf{x}_n,\mathcal{C}_2)=p(\mathcal{C}_2)p(\mathbf{x}_n\mid\mathcal{C}_2)=(1-\pi)\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_2,\boldsymbol{\Sigma}).
$$

于是，似然函数为

$$
p(\boldsymbol{\mathsf{t}}\mid\pi,\boldsymbol{\mu}_1,\boldsymbol{\mu}_2,\boldsymbol{\Sigma})=\prod_{n=1}^{N}[\pi\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_1,\boldsymbol{\Sigma})]^{t_n}[(1-\pi)\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_2,\boldsymbol{\Sigma})]^{1-t_n}
\tag{4.71}
$$

其中，$\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。与通常的做法一样，最大化似然的对数更方便。先考虑对 $\pi$ 最大化。对数似然函数中

<!-- pdf-page: 221 -->
<!-- join-previous-paragraph -->
依赖于 $\pi$ 的项为

$$
\sum_{n=1}^{N}\{t_n\ln\pi+(1-t_n)\ln(1-\pi)\}.
\tag{4.72}
$$

令其对 $\pi$ 的导数等于零并整理，得到

$$
\pi=\frac{1}{N}\sum_{n=1}^{N}t_n=\frac{N_1}{N}=\frac{N_1}{N_1+N_2}
\tag{4.73}
$$

其中，$N_1$ 表示类别 $\mathcal{C}_1$ 的数据点总数，$N_2$ 表示类别 $\mathcal{C}_2$ 的数据点总数。因此，与预期一致，$\pi$ 的最大似然估计就是类别 $\mathcal{C}_1$ 的点所占的比例。这个结果很容易推广到多分类：类别 $\mathcal{C}_k$ 的先验概率的最大似然估计，同样等于训练集中被分配到该类别的点所占的比例。<span class="margin-reference">习题 4.9</span>

现在考虑对 $\boldsymbol{\mu}_1$ 最大化。同样，可以从对数似然函数中提取依赖于 $\boldsymbol{\mu}_1$ 的项，得到

$$
\sum_{n=1}^{N}t_n\ln\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_1,\boldsymbol{\Sigma})=-\frac{1}{2}\sum_{n=1}^{N}t_n(\mathbf{x}_n-\boldsymbol{\mu}_1)^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}_1)+\text{常数}.
\tag{4.74}
$$

令其对 $\boldsymbol{\mu}_1$ 的导数等于零并整理，得到

$$
\boldsymbol{\mu}_1=\frac{1}{N_1}\sum_{n=1}^{N}t_n\mathbf{x}_n
\tag{4.75}
$$

这就是分到类别 $\mathcal{C}_1$ 的全部输入向量 $\mathbf{x}_n$ 的均值。类似地，$\boldsymbol{\mu}_2$ 的结果为

$$
\boldsymbol{\mu}_2=\frac{1}{N_2}\sum_{n=1}^{N}(1-t_n)\mathbf{x}_n
\tag{4.76}
$$

同样，它是分到类别 $\mathcal{C}_2$ 的全部输入向量 $\mathbf{x}_n$ 的均值。

最后，考虑共享协方差矩阵 $\boldsymbol{\Sigma}$ 的最大似然解。从对数似然函数中提取依赖于 $\boldsymbol{\Sigma}$ 的项，得到

$$
\begin{aligned}
&-\frac{1}{2}\sum_{n=1}^{N}t_n\ln|\boldsymbol{\Sigma}|-\frac{1}{2}\sum_{n=1}^{N}t_n(\mathbf{x}_n-\boldsymbol{\mu}_1)^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}_1)\\
&\quad-\frac{1}{2}\sum_{n=1}^{N}(1-t_n)\ln|\boldsymbol{\Sigma}|-\frac{1}{2}\sum_{n=1}^{N}(1-t_n)(\mathbf{x}_n-\boldsymbol{\mu}_2)^{\mathrm T}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\boldsymbol{\mu}_2)\\
&\quad=-\frac{N}{2}\ln|\boldsymbol{\Sigma}|-\frac{N}{2}\operatorname{Tr}\{\boldsymbol{\Sigma}^{-1}\mathbf{S}\}
\end{aligned}
\tag{4.77}
$$

<!-- pdf-page: 222 -->

其中定义

$$
\mathbf{S}=\frac{N_1}{N}\mathbf{S}_1+\frac{N_2}{N}\mathbf{S}_2
\tag{4.78}
$$

$$
\mathbf{S}_1=\frac{1}{N_1}\sum_{n\in\mathcal{C}_1}(\mathbf{x}_n-\boldsymbol{\mu}_1)(\mathbf{x}_n-\boldsymbol{\mu}_1)^{\mathrm T}
\tag{4.79}
$$

$$
\mathbf{S}_2=\frac{1}{N_2}\sum_{n\in\mathcal{C}_2}(\mathbf{x}_n-\boldsymbol{\mu}_2)(\mathbf{x}_n-\boldsymbol{\mu}_2)^{\mathrm T}.
\tag{4.80}
$$

利用高斯分布最大似然解的标准结果，可以得到 $\boldsymbol{\Sigma}=\mathbf{S}$，它是两个类别各自协方差矩阵的加权平均。

这个结果很容易推广到 $K$ 分类问题，从而得到各类条件密度为高斯分布、并共享协方差矩阵时的参数最大似然解。<span class="margin-reference">习题 4.10</span> 注意，为各类别拟合高斯分布的方法对离群点缺乏鲁棒性，因为高斯分布的最大似然估计本身就缺乏鲁棒性。<span class="margin-reference">第 2.3.7 节</span>

### 4.2.3 离散特征

现在考虑离散特征值 $x_i$。为简便起见，先讨论二元特征 $x_i\in\{0,1\}$，稍后再说明如何推广到更一般的离散特征。如果有 $D$ 个输入，那么一般分布对每个类别都需要一张含 $2^D$ 个数值的表；由于求和约束，其中独立变量数为 $2^D-1$。这个数目随特征数指数增长，因此我们可能需要限制更多的表示。这里采用朴素贝叶斯（naive Bayes）假设：给定类别 $\mathcal{C}_k$ 后，各特征值相互独立。<span class="margin-reference">第 8.2.2 节</span> 因此，类条件分布为

$$
p(\mathbf{x}\mid\mathcal{C}_k)=\prod_{i=1}^{D}\mu_{ki}^{x_i}(1-\mu_{ki})^{1-x_i}
\tag{4.81}
$$

每个类别有 $D$ 个独立参数。代入式（4.63），得到

$$
a_k(\mathbf{x})=\sum_{i=1}^{D}\{x_i\ln\mu_{ki}+(1-x_i)\ln(1-\mu_{ki})\}+\ln p(\mathcal{C}_k)
\tag{4.82}
$$

它们同样是输入值 $x_i$ 的线性函数。对于 $K=2$ 个类别，也可以使用式（4.57）给出的 logistic sigmoid 形式。对于每个变量都可取 $M>2$ 个状态的离散变量，可以得到类似结果。<span class="margin-reference">习题 4.11</span>

### 4.2.4 指数族

正如前面所见，无论输入服从高斯分布，还是取离散值，类别后验概率都由广义线性模型给出，其激活函数为

<!-- pdf-page: 223 -->
<!-- join-previous-paragraph -->
logistic sigmoid（$K=2$ 类）或 softmax（$K\geqslant2$ 类）函数。这些都是一个更一般结果的特例：假设类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 属于指数族分布，就可以得到这一结果。

使用指数族成员的形式（2.194），可知 $\mathbf{x}$ 的分布可以写为

$$
p(\mathbf{x}\mid\boldsymbol{\lambda}_k)=h(\mathbf{x})g(\boldsymbol{\lambda}_k)\exp\left\{\boldsymbol{\lambda}_k^{\mathrm T}\mathbf{u}(\mathbf{x})\right\}.
\tag{4.83}
$$

现在，只考虑这些分布中满足 $\mathbf{u}(\mathbf{x})=\mathbf{x}$ 的子类。再利用（2.236）引入尺度参数 $s$，就得到如下形式的一组受限指数族类条件密度：

$$
p(\mathbf{x}\mid\boldsymbol{\lambda}_k,s)=\frac{1}{s}h\left(\frac{1}{s}\mathbf{x}\right)g(\boldsymbol{\lambda}_k)\exp\left\{\frac{1}{s}\boldsymbol{\lambda}_k^{\mathrm T}\mathbf{x}\right\}.
\tag{4.84}
$$

注意，这里允许每个类别有自己的参数向量 $\boldsymbol{\lambda}_k$，但假定所有类别共享同一个尺度参数 $s$。

对于二分类问题，将这个类条件密度表达式代入（4.58），可见类别后验概率仍由作用在线性函数 $a(\mathbf{x})$ 上的 logistic sigmoid 给出，其中

$$
a(\mathbf{x})=(\boldsymbol{\lambda}_1-\boldsymbol{\lambda}_2)^{\mathrm T}\mathbf{x}+\ln g(\boldsymbol{\lambda}_1)-\ln g(\boldsymbol{\lambda}_2)+\ln p(\mathcal{C}_1)-\ln p(\mathcal{C}_2).
\tag{4.85}
$$

同样，对于 $K$ 类问题，将类条件密度表达式代入（4.63），得到

$$
a_k(\mathbf{x})=\boldsymbol{\lambda}_k^{\mathrm T}\mathbf{x}+\ln g(\boldsymbol{\lambda}_k)+\ln p(\mathcal{C}_k)
\tag{4.86}
$$

因此，它仍是 $\mathbf{x}$ 的线性函数。

## 4.3 概率判别式模型

对于二分类问题，我们已经看到，在相当广泛的类条件分布 $p(\mathbf{x}\mid\mathcal{C}_k)$ 选择下，类别 $\mathcal{C}_1$ 的后验概率都可以写成作用于 $\mathbf{x}$ 的线性函数之上的 logistic sigmoid。类似地，对于多分类问题，类别 $\mathcal{C}_k$ 的后验概率由 $\mathbf{x}$ 的线性函数的 softmax 变换给出。针对类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 的具体选择，我们用最大似然确定了这些密度的参数以及类别先验 $p(\mathcal{C}_k)$，然后使用贝叶斯定理求出类别后验概率。

不过，还有另一种方法：直接采用广义线性模型的函数形式，并用最大似然直接确定它的参数。我们将看到，有一种高效求解算法，称为*迭代重加权最小二乘*（iterative reweighted least squares，IRLS）。

分别拟合类条件密度与类别先验，再应用

<!-- pdf-page: 224 -->
<!-- join-previous-paragraph -->
贝叶斯定理，这种间接求取广义线性模型参数的方法，是*生成式建模*的一个例子，因为可以使用这样的模型，从边缘分布 $p(\mathbf{x})$ 中抽取 $\mathbf{x}$ 的值，从而生成合成数据。直接方法则最大化通过条件分布 $p(\mathcal{C}_k\mid\mathbf{x})$ 定义的似然函数，属于一种*判别式训练*。判别式方法的一个优点是，通常需要确定的可调参数较少，我们很快就会看到这一点。它也可能带来更好的预测性能，尤其是在所假设的类条件密度不能很好地近似真实分布时。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/b-fig-4-12.png" alt="两个类别在原始输入空间与高斯基函数特征空间中的分布及决策边界"><figcaption>图 4.12：非线性基函数在线性分类模型中所起作用的示意图。左图展示原始输入空间 $(x_1,x_2)$，以及用红色和蓝色标识的两个类别的数据点。在这个空间中定义了两个“高斯”基函数 $\phi_1(\mathbf{x})$ 和 $\phi_2(\mathbf{x})$，其中心由绿色叉号表示，等高线由绿色圆表示。右图展示相应的特征空间 $(\phi_1,\phi_2)$，以及由 4.3.2 节所讨论形式的逻辑回归模型得到的线性决策边界。它对应于原始输入空间中的非线性决策边界，即左图中的黑色曲线。</figcaption><p class="figure-translation">$x_1$、$x_2$：原始输入的两个分量；$\phi_1$、$\phi_2$：两个基函数的输出。</p></figure>

### 4.3.1 固定基函数

本章到目前为止讨论的分类模型，都是直接处理原始输入向量 $\mathbf{x}$ 的。不过，如果先使用基函数向量 $\boldsymbol{\phi}(\mathbf{x})$ 对输入作固定的非线性变换，所有这些算法仍然同样适用。所得决策边界在特征空间 $\boldsymbol{\phi}$ 中是线性的，而在原始 $\mathbf{x}$ 空间中则对应于非线性决策边界，如图 4.12 所示。在特征空间 $\boldsymbol{\phi}(\mathbf{x})$ 中线性可分的类别，在原始观测空间 $\mathbf{x}$ 中不一定线性可分。注意，与讨论线性回归模型时一样，通常将其中一个

<!-- pdf-page: 225 -->
<!-- join-previous-paragraph -->
基函数设为常数，例如 $\phi_0(\mathbf{x})=1$，使相应的参数 $w_0$ 起到偏置的作用。本章余下部分将包含一个固定的基函数变换 $\boldsymbol{\phi}(\mathbf{x})$，因为这样可以凸显与第 3 章回归模型之间一些有用的相似之处。

在许多有实际意义的问题中，类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$ 之间存在明显重叠。这对应于这样一类后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$：至少对于某些 $\mathbf{x}$ 值，它们既不是 0，也不是 1。在这种情况下，最优解需要先准确地建模后验概率，再应用标准决策论，如第 1 章所述。注意，非线性变换 $\boldsymbol{\phi}(\mathbf{x})$ 无法消除这种类别重叠。事实上，它可能增加重叠程度，甚至在原始观测空间中没有重叠的情况下引入重叠。不过，适当地选择非线性形式，可以使后验概率的建模更容易。

这些固定基函数模型存在重要的局限性（3.6 节）。在后续章节中，我们将允许基函数本身适应数据，以解决这些问题。尽管有这些局限性，具有固定非线性基函数的模型在应用中仍起着重要作用。讨论这类模型，也会引出理解更复杂模型所需的许多关键概念。

### 4.3.2 逻辑回归

我们从二分类问题开始讨论广义线性模型。在 4.2 节讨论生成式方法时，我们看到，在相当一般的假设下，类别 $\mathcal{C}_1$ 的后验概率可以写成作用于特征向量 $\boldsymbol{\phi}$ 的线性函数之上的 logistic sigmoid，即

$$
p(\mathcal{C}_1\mid\boldsymbol{\phi})=y(\boldsymbol{\phi})=\sigma\left(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}\right)
\tag{4.87}
$$

并且 $p(\mathcal{C}_2\mid\boldsymbol{\phi})=1-p(\mathcal{C}_1\mid\boldsymbol{\phi})$。这里，$\sigma(\cdot)$ 是（4.59）定义的 logistic sigmoid 函数。在统计学术语中，这个模型称为*逻辑回归*（logistic regression），不过需要强调，它是分类模型，而不是回归模型。

对于 $M$ 维特征空间 $\boldsymbol{\phi}$，该模型有 $M$ 个可调参数。相比之下，如果使用最大似然拟合高斯类条件密度，就需要用 $2M$ 个参数表示均值，用 $M(M+1)/2$ 个参数表示（共享的）协方差矩阵。加上类别先验 $p(\mathcal{C}_1)$，总共需要 $M(M+5)/2+1$ 个参数，随 $M$ 以二次速度增长；而逻辑回归的参数数目则随 $M$ 线性增长。当 $M$ 很大时，直接使用逻辑回归模型具有明显优势。

现在用最大似然来确定逻辑回归模型的参数。为此，需要用到 logistic sigmoid 函数的导数，它可以方便地用 sigmoid 函数自身表示（习题 4.12）：

$$
\frac{d\sigma}{da}=\sigma(1-\sigma).
\tag{4.88}
$$

<!-- pdf-page: 226 -->

对于数据集 $\{\boldsymbol{\phi}_n,t_n\}$，其中 $t_n\in\{0,1\}$、$\boldsymbol{\phi}_n=\boldsymbol{\phi}(\mathbf{x}_n)$，$n=1,\ldots,N$，似然函数可以写为

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})=\prod_{n=1}^{N}y_n^{t_n}\{1-y_n\}^{1-t_n}
\tag{4.89}
$$

其中 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$，$y_n=p(\mathcal{C}_1\mid\boldsymbol{\phi}_n)$。像通常那样，取似然的负对数来定义误差函数，得到如下形式的*交叉熵*误差函数：

$$
E(\mathbf{w})=-\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})=-\sum_{n=1}^{N}\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}
\tag{4.90}
$$

其中 $y_n=\sigma(a_n)$，$a_n=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n$。对误差函数求关于 $\mathbf{w}$ 的梯度，得到（习题 4.13）

$$
\nabla E(\mathbf{w})=\sum_{n=1}^{N}(y_n-t_n)\boldsymbol{\phi}_n
\tag{4.91}
$$

这里使用了（4.88）。可见，含有 logistic sigmoid 导数的因子已经消去，因此对数似然的梯度具有较简单的形式。具体来说，数据点 $n$ 对梯度的贡献，等于目标值与模型预测之间的“误差” $y_n-t_n$，乘以基函数向量 $\boldsymbol{\phi}_n$。此外，与（3.13）比较可以发现，这恰好与线性回归模型的平方和误差函数的梯度具有相同形式（3.1.1 节）。

如果需要，可以利用结果（4.91）得到一个序贯算法：每次提供一个模式，并用（3.22）更新各个权重向量，其中 $\nabla E_n$ 是（4.91）的第 $n$ 项。

需要注意，对于线性可分的数据集，最大似然可能出现严重的过拟合。这是因为，最大似然解出现在这样一种情形：对应于 $\sigma=0.5$，即 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}=0$ 的超平面将两个类别分开，而 $\mathbf{w}$ 的大小趋于无穷。在这种情况下，logistic sigmoid 函数在特征空间中变得无限陡峭，对应于 Heaviside 阶跃函数，从而每个类别 $k$ 中的所有训练点都会被赋予后验概率 $p(\mathcal{C}_k\mid\mathbf{x})=1$（习题 4.14）。此外，这样的解通常构成一个连续集合，因为任意一个分离超平面都会在训练数据点处给出相同的后验概率，我们将在后面的图 10.13 中看到这一点。最大似然无法在这些解之间作出偏好选择，实际找到哪个解，取决于所选的优化算法和参数初始化。注意，只要训练数据集线性可分，即使数据点的数目远大于模型参数的数目，也会出现这一问题。引入先验并求出 $\mathbf{w}$ 的 MAP 解，或者等价地在误差函数中加入正则化项，就可以避免这种奇异性。

<!-- pdf-page: 227 -->

### 4.3.3 迭代重加权最小二乘

对于第 3 章讨论的线性回归模型，在假设噪声为高斯模型时，最大似然解可以写成闭式形式。这是因为对数似然函数关于参数向量 $\mathbf{w}$ 是二次函数。对于逻辑回归，由于 logistic sigmoid 函数的非线性，闭式解不再存在。不过，它与二次形式的差别并不大。更准确地说，误差函数是凹函数，因此具有唯一的最小值，我们马上就会看到这一点。此外，可以采用一种基于 Newton–Raphson 迭代优化方案的高效迭代方法来最小化误差函数。该方法对对数似然函数作局部二次近似。用于最小化函数 $E(\mathbf{w})$ 的 Newton–Raphson 更新具有如下形式（Fletcher, 1987; Bishop and Nabney, 2008）：

$$
\mathbf{w}^{\mathrm{(new)}}=\mathbf{w}^{\mathrm{(old)}}-\mathbf{H}^{-1}\nabla E(\mathbf{w}).
\tag{4.92}
$$

其中 $\mathbf{H}$ 是 Hessian 矩阵，其元素由 $E(\mathbf{w})$ 关于 $\mathbf{w}$ 各分量的二阶导数组成。

首先，将 Newton–Raphson 方法用于具有平方和误差函数（3.12）的线性回归模型（3.3）。该误差函数的梯度与 Hessian 矩阵分别为

$$
\nabla E(\mathbf{w})=\sum_{n=1}^{N}(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n-t_n)\boldsymbol{\phi}_n=\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}\mathbf{w}-\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{4.93}
$$

$$
\mathbf{H}=\nabla\nabla E(\mathbf{w})=\sum_{n=1}^{N}\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}=\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}
\tag{4.94}
$$

其中 $\boldsymbol{\Phi}$ 是 $N\times M$ 设计矩阵，其第 $n$ 行为 $\boldsymbol{\phi}_n^{\mathrm T}$（3.1.1 节）。于是 Newton–Raphson 更新变为

$$
\begin{aligned}
\mathbf{w}^{\mathrm{(new)}}&=\mathbf{w}^{\mathrm{(old)}}-(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\left\{\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}\mathbf{w}^{\mathrm{(old)}}-\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}\right\}\\
&=(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\end{aligned}
\tag{4.95}
$$

这就是标准的最小二乘解。注意，此时误差函数是二次函数，因此 Newton–Raphson 公式只需一步就能给出精确解。

现在，将 Newton–Raphson 更新用于逻辑回归模型的交叉熵误差函数（4.90）。由（4.91）可知，该误差函数的梯度与 Hessian 矩阵分别为

$$
\nabla E(\mathbf{w})=\sum_{n=1}^{N}(y_n-t_n)\boldsymbol{\phi}_n=\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{y}}-\boldsymbol{\mathsf{t}})
\tag{4.96}
$$

$$
\mathbf{H}=\nabla\nabla E(\mathbf{w})=\sum_{n=1}^{N}y_n(1-y_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}=\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\Phi}
\tag{4.97}
$$

<!-- pdf-page: 228 -->

这里使用了（4.88）。另外，引入了 $N\times N$ 对角矩阵 $\mathbf{R}$，其元素为

$$
R_{nn}=y_n(1-y_n).
\tag{4.98}
$$

可见，Hessian 矩阵不再是常量，而是通过权重矩阵 $\mathbf{R}$ 依赖于 $\mathbf{w}$，这与误差函数不再是二次函数相对应。利用 logistic sigmoid 函数的形式所蕴含的性质 $0<y_n<1$，可知对于任意向量 $\mathbf{u}$ 都有 $\mathbf{u}^{\mathrm T}\mathbf{H}\mathbf{u}>0$，所以 Hessian 矩阵 $\mathbf{H}$ 是正定的。因此，误差函数是 $\mathbf{w}$ 的凹函数，从而具有唯一的最小值（习题 4.15）。

逻辑回归模型的 Newton–Raphson 更新公式于是变为

$$
\begin{aligned}
\mathbf{w}^{\mathrm{(new)}}&=\mathbf{w}^{\mathrm{(old)}}-(\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{y}}-\boldsymbol{\mathsf{t}})\\
&=(\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\Phi})^{-1}\left\{\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\Phi}\mathbf{w}^{\mathrm{(old)}}-\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{y}}-\boldsymbol{\mathsf{t}})\right\}\\
&=(\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}\mathbf{R}\boldsymbol{\mathsf{z}}
\end{aligned}
\tag{4.99}
$$

其中 $\boldsymbol{\mathsf{z}}$ 是一个 $N$ 维向量，其元素由下式给出：

$$
\boldsymbol{\mathsf{z}}=\boldsymbol{\Phi}\mathbf{w}^{\mathrm{(old)}}-\mathbf{R}^{-1}(\boldsymbol{\mathsf{y}}-\boldsymbol{\mathsf{t}}).
\tag{4.100}
$$

可见，更新公式（4.99）具有加权最小二乘问题的一组正规方程的形式。由于权重矩阵 $\mathbf{R}$ 不是常量，而是依赖于参数向量 $\mathbf{w}$，所以必须反复应用正规方程，每次用新的权重向量 $\mathbf{w}$ 计算更新后的权重矩阵 $\mathbf{R}$。因此，这个算法称为*迭代重加权最小二乘*，简称 IRLS（Rubin, 1983）。与加权最小二乘问题中一样，对角权重矩阵 $\mathbf{R}$ 的元素可以解释为方差，因为在逻辑回归模型中，$t$ 的均值与方差为

$$
\mathbb{E}[t]=\sigma(\mathbf{x})=y
\tag{4.101}
$$

$$
\operatorname{var}[t]=\mathbb{E}[t^2]-\mathbb{E}[t]^2=\sigma(\mathbf{x})-\sigma(\mathbf{x})^2=y(1-y)
\tag{4.102}
$$

这里使用了当 $t\in\{0,1\}$ 时 $t^2=t$ 这一性质。事实上，可以将 IRLS 解释为变量 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$ 所在空间中一个线性化问题的解。于是，$\boldsymbol{\mathsf{z}}$ 的第 $n$ 个元素 $z_n$ 就有了一个简单解释：它是在当前工作点 $\mathbf{w}^{\mathrm{(old)}}$ 附近对 logistic sigmoid 函数作局部线性近似，得到的该空间中的有效目标值：

$$
\begin{aligned}
a_n(\mathbf{w})&\simeq a_n(\mathbf{w}^{\mathrm{(old)}})+\left.\frac{da_n}{dy_n}\right|_{\mathbf{w}^{\mathrm{(old)}}}(t_n-y_n)\\
&=\boldsymbol{\phi}_n^{\mathrm T}\mathbf{w}^{\mathrm{(old)}}-\frac{(y_n-t_n)}{y_n(1-y_n)}=z_n.
\end{aligned}
\tag{4.103}
$$

<!-- pdf-page: 229 -->

### 4.3.4 多类别逻辑回归

讨论多分类的生成式模型时（4.2 节），我们已经看到，对一大类分布而言，后验概率由特征变量的线性函数经过 softmax 变换给出，即

$$
p(\mathcal{C}_k\mid\boldsymbol{\phi})=y_k(\boldsymbol{\phi})=\frac{\exp(a_k)}{\sum_j\exp(a_j)}
\tag{4.104}
$$

其中“激活值” $a_k$ 为

$$
a_k=\mathbf{w}_k^{\mathrm T}\boldsymbol{\phi}.
\tag{4.105}
$$

当时，我们使用最大似然分别确定类条件密度和类别先验，再通过贝叶斯定理求出相应的后验概率，从而隐式地确定参数 $\{\mathbf{w}_k\}$。这里考虑用最大似然直接确定这个模型的参数 $\{\mathbf{w}_k\}$。为此，需要求 $y_k$ 关于所有激活值 $a_j$ 的导数，它们为（习题 4.17）

$$
\frac{\partial y_k}{\partial a_j}=y_k(I_{kj}-y_j)
\tag{4.106}
$$

其中 $I_{kj}$ 是单位矩阵的元素。

接下来写出似然函数。使用 1-of-$K$ 编码最为方便：对于属于类别 $\mathcal{C}_k$ 的特征向量 $\boldsymbol{\phi}_n$，其目标向量 $\mathbf{t}_n$ 是一个二元向量，除第 $k$ 个元素等于 1 外，其余元素均为零。于是似然函数为

$$
p(\mathbf{T}\mid\mathbf{w}_1,\ldots,\mathbf{w}_K)=\prod_{n=1}^{N}\prod_{k=1}^{K}p(\mathcal{C}_k\mid\boldsymbol{\phi}_n)^{t_{nk}}=\prod_{n=1}^{N}\prod_{k=1}^{K}y_{nk}^{t_{nk}}
\tag{4.107}
$$

其中 $y_{nk}=y_k(\boldsymbol{\phi}_n)$，$\mathbf{T}$ 是由目标变量构成的 $N\times K$ 矩阵，其元素为 $t_{nk}$。取负对数，得到

$$
E(\mathbf{w}_1,\ldots,\mathbf{w}_K)=-\ln p(\mathbf{T}\mid\mathbf{w}_1,\ldots,\mathbf{w}_K)=-\sum_{n=1}^{N}\sum_{k=1}^{K}t_{nk}\ln y_{nk}
\tag{4.108}
$$

这称为多分类问题的*交叉熵*误差函数。

现在对误差函数求关于其中一个参数向量 $\mathbf{w}_j$ 的梯度。利用 softmax 函数导数的结果（4.106），得到（习题 4.18）

$$
\nabla_{\mathbf{w}_j}E(\mathbf{w}_1,\ldots,\mathbf{w}_K)=\sum_{n=1}^{N}(y_{nj}-t_{nj})\boldsymbol{\phi}_n
\tag{4.109}
$$

<!-- pdf-page: 230 -->

这里使用了 $\sum_k t_{nk}=1$。我们再次看到，梯度的形式与线性模型的平方和误差函数以及逻辑回归模型的交叉熵误差函数相同，即误差 $(y_{nj}-t_{nj})$ 与基函数 $\boldsymbol{\phi}_n$ 的乘积。同样，可以据此构造一个序贯算法，每次提供一个模式，并使用（3.22）更新各个权重向量。

我们已经看到，对线性回归模型而言，数据点 $n$ 对应的对数似然函数关于参数向量 $\mathbf{w}$ 的导数，具有“误差” $y_n-t_n$ 乘以特征向量 $\boldsymbol{\phi}_n$ 的形式。同样，将 logistic sigmoid 激活函数与交叉熵误差函数（4.90）组合，或者将 softmax 激活函数与多类别交叉熵误差函数（4.108）组合，也会得到相同的简单形式。这是一个更一般结果的例子，我们将在 4.3.6 节看到这一点。

为了得到批量算法，再次使用 Newton–Raphson 更新，便可得到多分类问题的相应 IRLS 算法。为此，需要计算 Hessian 矩阵。它由大小为 $M\times M$ 的子块组成，其中第 $(j,k)$ 个子块为

$$
\nabla_{\mathbf{w}_k}\nabla_{\mathbf{w}_j}E(\mathbf{w}_1,\ldots,\mathbf{w}_K)=-\sum_{n=1}^{N}y_{nk}(I_{kj}-y_{nj})\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{4.110}
$$

与二分类问题一样，多类别逻辑回归模型的 Hessian 矩阵是正定的，因此误差函数也有唯一的最小值（习题 4.20）。多类别情形下 IRLS 的实际实现细节可参见 Bishop and Nabney（2008）。

### 4.3.5 Probit 回归

我们已经看到，对于由指数族描述的广泛类条件分布，得到的类别后验概率都是对特征变量的线性函数进行 logistic（或 softmax）变换的结果。不过，并非所有类条件密度的选择都会使后验概率具有这么简单的形式，例如使用高斯混合来建模类条件密度时就不是如此。这提示我们，值得探索其他类型的判别式概率模型。不过，在本章中，我们将回到二分类情形，并继续采用广义线性模型的框架，即

$$
p(t=1\mid a)=f(a)
\tag{4.111}
$$

其中 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$，$f(\cdot)$ 是激活函数。

为连接函数寻找另一种选择的一条思路，是考虑如下带噪声的阈值模型。对于每个输入 $\boldsymbol{\phi}_n$，计算 $a_n=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n$，然后按下面的规则设定目标值：

$$
\begin{cases}
t_n=1&\text{若 }a_n\geqslant\theta\\
t_n=0&\text{否则。}
\end{cases}
\tag{4.112}
$$

<!-- pdf-page: 231 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/b-fig-4-13.png" alt="双高斯混合概率密度及其累积分布函数，以及密度、斜率和积分面积的对应关系"><figcaption>图 4.13：概率密度 $p(\theta)$ 及其累积分布函数 $f(a)$ 的示意例子。蓝色曲线表示概率密度，在此例中是两个高斯分布的混合；红色曲线表示累积分布函数。注意，蓝色曲线在任意一点的值，例如绿色竖线所标位置的值，对应于红色曲线在同一位置的斜率。反过来，红色曲线在该位置的值，对应于绿色阴影区域所表示的蓝色曲线下方面积。在随机阈值模型中，如果 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$ 的值超过阈值，类别标签就取 $t=1$，否则取 $t=0$。这等价于以累积分布函数 $f(a)$ 作为激活函数。</figcaption></figure>

如果 $\theta$ 的值从概率密度 $p(\theta)$ 中抽取，那么相应的激活函数就由累积分布函数给出：

$$
f(a)=\int_{-\infty}^{a}p(\theta)\,d\theta
\tag{4.113}
$$

如图 4.13 所示。

作为一个具体例子，假设密度 $p(\theta)$ 是均值为零、方差为 1 的高斯分布。相应的累积分布函数为

$$
\Phi(a)=\int_{-\infty}^{a}\mathcal{N}(\theta\mid0,1)\,d\theta
\tag{4.114}
$$

它称为 *probit 函数*。它具有 S 形外观，图 4.9 将它与 logistic sigmoid 函数作了比较。注意，使用更一般的高斯分布不会改变模型，因为这等价于重新缩放线性系数 $\mathbf{w}$。许多数值计算软件包都提供一个密切相关函数的计算，该函数定义为

$$
\operatorname{erf}(a)=\frac{2}{\sqrt{\pi}}\int_0^a\exp(-\theta^2/2)\,d\theta
\tag{4.115}
$$

称为 *erf 函数*或*误差函数*（不要与机器学习模型的误差函数混淆）。它与 probit 函数的关系为（习题 4.21）

$$
\boldsymbol{\Phi}(a)=\frac{1}{2}\left\{1+\frac{1}{\sqrt{2}}\operatorname{erf}(a)\right\}.
\tag{4.116}
$$

采用 probit 激活函数的广义线性模型称为 *Probit 回归*。

稍加推广前面讨论的思路，就可以用最大似然确定这个模型的参数。实际中，Probit 回归的结果通常与逻辑回归相似。不过，

<!-- pdf-page: 232 -->
<!-- join-previous-paragraph -->
在 4.5 节讨论逻辑回归的贝叶斯处理时，我们将会发现 probit 模型的另一种用途。

实际应用中可能遇到的一个问题是离群点，例如它们可能来自输入向量 $\mathbf{x}$ 的测量错误，或者目标值 $t$ 的标签标错。由于这些点可能深入理想决策边界的错误一侧，它们会严重扭曲分类器。注意，逻辑回归与 Probit 回归在这方面表现不同：当 $x\to\infty$ 时，logistic sigmoid 的尾部按 $\exp(-x)$ 渐近衰减，而 probit 激活函数的尾部则按 $\exp(-x^2)$ 衰减，因此 probit 模型可能对离群点敏感得多。

不过，logistic 和 probit 模型都假定数据的标签是正确的。引入一个概率 $\epsilon$，表示目标值 $t$ 被翻转为错误值的概率，就能很容易地将标签错误的影响纳入概率模型（Opper and Winther, 2000a）。这样，数据点 $\mathbf{x}$ 的目标值分布具有如下形式：

$$
\begin{aligned}
p(t\mid\mathbf{x})&=(1-\epsilon)\sigma(\mathbf{x})+\epsilon(1-\sigma(\mathbf{x}))\\
&=\epsilon+(1-2\epsilon)\sigma(\mathbf{x})
\end{aligned}
\tag{4.117}
$$

其中 $\sigma(\mathbf{x})$ 是以向量 $\mathbf{x}$ 为输入的激活函数。这里，$\epsilon$ 可以预先设定，也可以视为一个超参数，根据数据推断其值。

### 4.3.6 典范连接函数

对于噪声服从高斯分布的线性回归模型，与负对数似然相对应的误差函数由（3.12）给出。对数据点 $n$ 对误差函数的贡献求关于参数向量 $\mathbf{w}$ 的导数，得到的形式为“误差” $y_n-t_n$ 乘以特征向量 $\boldsymbol{\phi}_n$，其中 $y_n=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n$。同样，将 logistic sigmoid 激活函数与交叉熵误差函数（4.90）组合，或者将 softmax 激活函数与多类别交叉熵误差函数（4.108）组合，也会得到这一简单形式。下面将证明，这是一个一般性结果：假设目标变量的条件分布属于指数族，并相应地选择一种称为*典范连接函数*（canonical link function）的激活函数，就会得到这一结果。

我们再次使用指数族分布的受限形式（4.84）。注意，这里将指数族分布的假设用于目标变量 $t$；而在 4.2.4 节中，该假设用于输入向量 $\mathbf{x}$。因此，考虑如下形式的目标变量条件分布：

$$
p(t\mid\eta,s)=\frac{1}{s}h\left(\frac{t}{s}\right)g(\eta)\exp\left\{\frac{\eta t}{s}\right\}.
\tag{4.118}
$$

沿用推导结果（2.226）时的论证思路，可知 $t$ 的条件均值（记为 $y$）为

$$
y\equiv\mathbb{E}[t\mid\eta]=-s\frac{d}{d\eta}\ln g(\eta).
\tag{4.119}
$$

<!-- pdf-page: 233 -->

因此，$y$ 与 $\eta$ 必然相关，我们用 $\eta=\psi(y)$ 表示这种关系。

遵循 Nelder and Wedderburn（1972）的定义，*广义线性模型*是这样一种模型：$y$ 是输入变量（或特征变量）线性组合的非线性函数，即

$$
y=f(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})
\tag{4.120}
$$

其中，机器学习文献将 $f(\cdot)$ 称为*激活函数*，而统计学将 $f^{-1}(\cdot)$ 称为*连接函数*。

现在考虑该模型的对数似然函数，将它看作 $\eta$ 的函数，可写为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\eta,s)=\sum_{n=1}^{N}\ln p(t_n\mid\eta,s)=\sum_{n=1}^{N}\left\{\ln g(\eta_n)+\frac{\eta_nt_n}{s}\right\}+\text{const}
\tag{4.121}
$$

这里假设所有观测共享同一个尺度参数（例如，在高斯分布中，它对应于噪声方差），所以 $s$ 与 $n$ 无关。于是，对数似然关于模型参数 $\mathbf{w}$ 的导数为

$$
\begin{aligned}
\nabla_{\mathbf{w}}\ln p(\boldsymbol{\mathsf{t}}\mid\eta,s)&=\sum_{n=1}^{N}\left\{\frac{d}{d\eta_n}\ln g(\eta_n)+\frac{t_n}{s}\right\}\frac{d\eta_n}{dy_n}\frac{dy_n}{da_n}\nabla a_n\\
&=\sum_{n=1}^{N}\frac{1}{s}\{t_n-y_n\}\psi'(y_n)f'(a_n)\boldsymbol{\phi}_n
\end{aligned}
\tag{4.122}
$$

其中 $a_n=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n$，并且使用了 $y_n=f(a_n)$ 和 $\mathbb{E}[t\mid\eta]$ 的结果（4.119）。现在可以看到，如果为连接函数 $f^{-1}(y)$ 选择如下特定形式，就会带来很大的简化：

$$
f^{-1}(y)=\psi(y)
\tag{4.123}
$$

它给出 $f(\psi(y))=y$，因而 $f'(\psi)\psi'(y)=1$。另外，由于 $a=f^{-1}(y)$，有 $a=\psi$，因此 $f'(a)\psi'(y)=1$。在这种情况下，误差函数的梯度简化为

$$
\nabla\ln E(\mathbf{w})=\frac{1}{s}\sum_{n=1}^{N}\{y_n-t_n\}\boldsymbol{\phi}_n.
\tag{4.124}
$$

对于高斯分布，$s=\beta^{-1}$；对于 logistic 模型，$s=1$。

## 4.4 拉普拉斯近似

在 4.5 节中，我们将讨论逻辑回归的贝叶斯处理。我们将看到，它比 3.3 节和 3.5 节中线性回归模型的贝叶斯处理更复杂。特别是，我们无法精确地

<!-- pdf-page: 234 -->
<!-- join-previous-paragraph -->
对参数向量 $\mathbf{w}$ 积分，因为后验分布不再是高斯分布。因此，必须引入某种近似。本书后面将讨论一系列基于解析近似（第 10 章）和数值采样（第 11 章）的方法。

这里介绍一种简单但应用广泛的框架，称为*拉普拉斯近似*（Laplace approximation）。其目标是对定义在一组连续变量上的概率密度，求出一个高斯近似。先考虑单个连续变量 $z$，假设其分布 $p(z)$ 定义为

$$
p(z)=\frac{1}{Z}f(z)
\tag{4.125}
$$

其中 $Z=\int f(z)\,dz$ 是归一化系数。假设 $Z$ 的值未知。拉普拉斯方法的目标，是找到一个以分布 $p(z)$ 的某个众数为中心的高斯近似 $q(z)$。第一步是找到 $p(z)$ 的一个众数，也就是一个使 $p'(z_0)=0$ 的点 $z_0$，或者等价地，满足

$$
\left.\frac{df(z)}{dz}\right|_{z=z_0}=0.
\tag{4.126}
$$

高斯分布具有这样一个性质：其对数是变量的二次函数。因此，考虑在众数 $z_0$ 处对 $\ln f(z)$ 作泰勒展开：

$$
\ln f(z)\simeq\ln f(z_0)-\frac{1}{2}A(z-z_0)^2
\tag{4.127}
$$

其中

$$
A=-\left.\frac{d^2}{dz^2}\ln f(z)\right|_{z=z_0}.
\tag{4.128}
$$

注意，由于 $z_0$ 是分布的一个局部极大值点，泰勒展开中的一阶项没有出现。取指数得到

$$
f(z)\simeq f(z_0)\exp\left\{-\frac{A}{2}(z-z_0)^2\right\}.
\tag{4.129}
$$

然后利用高斯分布归一化的标准结果，就能得到归一化分布 $q(z)$：

$$
q(z)=\left(\frac{A}{2\pi}\right)^{1/2}\exp\left\{-\frac{A}{2}(z-z_0)^2\right\}.
\tag{4.130}
$$

图 4.14 展示了拉普拉斯近似。注意，只有当精度 $A>0$ 时，这个高斯近似才有良好定义。换句话说，驻点 $z_0$ 必须是局部极大值点，使 $f(z)$ 在 $z_0$ 处的二阶导数为负。

<!-- pdf-page: 235 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-04/b-fig-4-14.png" alt="非高斯分布及其拉普拉斯近似，以及两条曲线的负对数"><figcaption>图 4.14：对分布 $p(z)\propto\exp(-z^2/2)\sigma(20z+4)$ 作拉普拉斯近似的示意图，其中 $\sigma(z)$ 是定义为 $\sigma(z)=(1+e^{-z})^{-1}$ 的 logistic sigmoid 函数。左图用黄色表示归一化分布 $p(z)$，用红色表示以 $p(z)$ 的众数 $z_0$ 为中心的拉普拉斯近似。右图给出相应两条曲线的负对数。</figcaption></figure>

可以将拉普拉斯方法推广到定义在 $M$ 维空间 $\mathbf{z}$ 上的分布 $p(\mathbf{z})=f(\mathbf{z})/Z$ 的近似。在驻点 $\mathbf{z}_0$ 处，梯度 $\nabla f(\mathbf{z})$ 为零。围绕该驻点展开，得到

$$
\ln f(\mathbf{z})\simeq\ln f(\mathbf{z}_0)-\frac{1}{2}(\mathbf{z}-\mathbf{z}_0)^{\mathrm T}\mathbf{A}(\mathbf{z}-\mathbf{z}_0)
\tag{4.131}
$$

其中 $M\times M$ 的 Hessian 矩阵 $\mathbf{A}$ 定义为

$$
\mathbf{A}=-\left.\nabla\nabla\ln f(\mathbf{z})\right|_{\mathbf{z}=\mathbf{z}_0}
\tag{4.132}
$$

而 $\nabla$ 是梯度算子。两边取指数，得到

$$
f(\mathbf{z})\simeq f(\mathbf{z}_0)\exp\left\{-\frac{1}{2}(\mathbf{z}-\mathbf{z}_0)^{\mathrm T}\mathbf{A}(\mathbf{z}-\mathbf{z}_0)\right\}.
\tag{4.133}
$$

分布 $q(\mathbf{z})$ 正比于 $f(\mathbf{z})$。利用归一化多元高斯分布的标准结果（2.43），通过观察即可确定适当的归一化系数，从而得到

$$
q(\mathbf{z})=\frac{|\mathbf{A}|^{1/2}}{(2\pi)^{M/2}}\exp\left\{-\frac{1}{2}(\mathbf{z}-\mathbf{z}_0)^{\mathrm T}\mathbf{A}(\mathbf{z}-\mathbf{z}_0)\right\}=\mathcal{N}(\mathbf{z}\mid\mathbf{z}_0,\mathbf{A}^{-1})
\tag{4.134}
$$

其中 $|\mathbf{A}|$ 表示 $\mathbf{A}$ 的行列式。只要精度矩阵 $\mathbf{A}$ 为正定矩阵，该高斯分布就有良好定义；这意味着驻点 $\mathbf{z}_0$ 必须是局部极大值点，而不能是极小值点或鞍点。

要应用拉普拉斯近似，首先需要找到众数 $\mathbf{z}_0$，再计算该众数处的 Hessian 矩阵。在实际中，通常通过运行某种数值优化算法来寻找众数（Bishop

<!-- pdf-page: 236 -->
<!-- join-previous-paragraph -->
and Nabney, 2008）。实际遇到的许多分布是多峰的，因此，选择不同的众数就会得到不同的拉普拉斯近似。注意，应用拉普拉斯方法不需要知道真实分布的归一化常数 $Z$。根据中心极限定理，随着观测数据点数增加，模型的后验分布预计会越来越接近高斯分布，因此可以预期，拉普拉斯近似在数据点数相对较多时最有用。

拉普拉斯近似的一个主要缺点是：由于它以高斯分布为基础，只能直接用于实变量。在其他情况下，或许可以对变量作变换后再应用拉普拉斯近似。例如，如果 $0\leqslant\tau<\infty$，就可以考虑对 $\ln\tau$ 作拉普拉斯近似。不过，拉普拉斯框架最严重的局限性在于，它完全依据真实分布在变量某个特定值处的性质，因此可能无法反映一些重要的全局性质。第 10 章将讨论从更全局的角度出发的其他方法。

### 4.4.1 模型比较与 BIC

除了近似分布 $p(\mathbf{z})$，还可以得到归一化常数 $Z$ 的近似。利用近似式（4.133），有

$$
\begin{aligned}
Z&=\int f(\mathbf{z})\,d\mathbf{z}\\
&\simeq f(\mathbf{z}_0)\int\exp\left\{-\frac{1}{2}(\mathbf{z}-\mathbf{z}_0)^{\mathrm T}\mathbf{A}(\mathbf{z}-\mathbf{z}_0)\right\}\,d\mathbf{z}\\
&=f(\mathbf{z}_0)\frac{(2\pi)^{M/2}}{|\mathbf{A}|^{1/2}}
\end{aligned}
\tag{4.135}
$$

这里注意到被积函数为高斯形式，并使用了归一化高斯分布的标准结果（2.43）。可以利用结果（4.135）得到模型证据的近似；正如 3.4 节讨论过的，模型证据在贝叶斯模型比较中起着核心作用。

考虑数据集 $\mathcal{D}$，以及一组具有参数 $\{\boldsymbol{\theta}_i\}$ 的模型 $\{\mathcal{M}_i\}$。对每个模型，定义似然函数 $p(\mathcal{D}\mid\boldsymbol{\theta}_i,\mathcal{M}_i)$。如果在参数上引入先验 $p(\boldsymbol{\theta}_i\mid\mathcal{M}_i)$，那么我们感兴趣的是计算各个模型的证据 $p(\mathcal{D}\mid\mathcal{M}_i)$。以下省略以 $\mathcal{M}_i$ 为条件的记号，以保持简洁。根据贝叶斯定理，模型证据为

$$
p(\mathcal{D})=\int p(\mathcal{D}\mid\boldsymbol{\theta})p(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{4.136}
$$

令 $f(\boldsymbol{\theta})=p(\mathcal{D}\mid\boldsymbol{\theta})p(\boldsymbol{\theta})$、$Z=p(\mathcal{D})$，并应用结果（4.135），得到（习题 4.22）

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid\boldsymbol{\theta}_{\mathrm{MAP}})+\underbrace{\ln p(\boldsymbol{\theta}_{\mathrm{MAP}})+\frac{M}{2}\ln(2\pi)-\frac{1}{2}\ln|\mathbf{A}|}_{\text{奥卡姆因子}}
\tag{4.137}
$$

<!-- pdf-page: 237 -->

其中 $\boldsymbol{\theta}_{\mathrm{MAP}}$ 是后验分布众数处的 $\boldsymbol{\theta}$ 值，而 $\mathbf{A}$ 是负对数后验的二阶导数构成的 Hessian 矩阵：

$$
\mathbf{A}=-\nabla\nabla\ln p(\mathcal{D}\mid\boldsymbol{\theta}_{\mathrm{MAP}})p(\boldsymbol{\theta}_{\mathrm{MAP}})=-\nabla\nabla\ln p(\boldsymbol{\theta}_{\mathrm{MAP}}\mid\mathcal{D}).
\tag{4.138}
$$

（4.137）右侧第一项表示用优化后的参数计算的对数似然，其余三项构成惩罚模型复杂度的“奥卡姆因子”（Occam factor）。

如果假设参数的高斯先验分布较宽，并且 Hessian 矩阵满秩，那么就可以对（4.137）作如下非常粗略的近似（习题 4.23）：

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid\boldsymbol{\theta}_{\mathrm{MAP}})-\frac{1}{2}M\ln N
\tag{4.139}
$$

其中 $N$ 是数据点数，$M$ 是 $\boldsymbol{\theta}$ 中的参数数目，并且略去了加法常数。这称为*贝叶斯信息准则*（Bayesian Information Criterion，BIC）或 *Schwarz 准则*（Schwarz, 1978）。注意，与（1.73）给出的 AIC 相比，它对模型复杂度的惩罚更重。

AIC 和 BIC 这样的复杂度度量具有易于计算的优点，但也可能给出误导性的结果。特别是，Hessian 矩阵满秩这一假设往往不成立，因为许多参数并非“充分确定”（3.5.3 节）。从拉普拉斯近似出发，使用结果（4.137）可以对模型证据作更准确的估计；我们将在 5.7 节中用神经网络来说明这一点。

## 4.5 贝叶斯逻辑回归

现在转向逻辑回归的贝叶斯处理。逻辑回归的精确贝叶斯推断难以求解。具体来说，计算后验分布需要对先验分布与似然函数的乘积进行归一化，而似然函数本身又由若干 logistic sigmoid 函数的乘积构成，每个数据点对应一个函数。预测分布的计算同样难以求解。这里考虑将拉普拉斯近似用于贝叶斯逻辑回归问题（Spiegelhalter and Lauritzen, 1990; MacKay, 1992b）。

### 4.5.1 拉普拉斯近似

回顾 4.4 节，拉普拉斯近似先找到后验分布的众数，再拟合一个以该众数为中心的高斯分布。这需要计算对数后验的二阶导数，也就是求 Hessian 矩阵。

由于希望用高斯分布表示后验分布，自然可以从高斯先验开始，其一般形式写为

$$
p(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\mathbf{S}_0)
\tag{4.140}
$$

<!-- pdf-page: 238 -->

其中 $\mathbf{m}_0$ 和 $\mathbf{S}_0$ 是固定的超参数。$\mathbf{w}$ 的后验分布为

$$
p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})\propto p(\mathbf{w})p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})
\tag{4.141}
$$

其中 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。两边取对数，并使用（4.140）代入先验分布、使用（4.89）代入似然函数，得到

$$
\begin{aligned}
\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})&=-\frac{1}{2}(\mathbf{w}-\mathbf{m}_0)^{\mathrm T}\mathbf{S}_0^{-1}(\mathbf{w}-\mathbf{m}_0)\\
&\quad+\sum_{n=1}^{N}\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}+\text{const}
\end{aligned}
\tag{4.142}
$$

其中 $y_n=\sigma(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n)$。为了获得后验分布的高斯近似，首先最大化后验分布，得到 MAP（最大后验）解 $\mathbf{w}_{\mathrm{MAP}}$，它确定了高斯分布的均值。协方差则由负对数似然的二阶导数矩阵的逆给出，其形式为

$$
\mathbf{S}_N=-\nabla\nabla\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})=\mathbf{S}_0^{-1}+\sum_{n=1}^{N}y_n(1-y_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{4.143}
$$

因此，后验分布的高斯近似具有如下形式：

$$
q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{w}_{\mathrm{MAP}},\mathbf{S}_N).
\tag{4.144}
$$

得到后验分布的高斯近似后，还需要对这个分布进行边缘化，才能作出预测。

### 4.5.2 预测分布

给定新的特征向量 $\boldsymbol{\phi}(\mathbf{x})$，类别 $\mathcal{C}_1$ 的预测分布通过对后验分布 $p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})$ 进行边缘化得到。而这个后验分布又用高斯分布 $q(\mathbf{w})$ 近似，因此

$$
p(\mathcal{C}_1\mid\boldsymbol{\phi},\boldsymbol{\mathsf{t}})=\int p(\mathcal{C}_1\mid\boldsymbol{\phi},\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})\,d\mathbf{w}\simeq\int\sigma(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})q(\mathbf{w})\,d\mathbf{w}
\tag{4.145}
$$

类别 $\mathcal{C}_2$ 的相应概率为 $p(\mathcal{C}_2\mid\boldsymbol{\phi},\boldsymbol{\mathsf{t}})=1-p(\mathcal{C}_1\mid\boldsymbol{\phi},\boldsymbol{\mathsf{t}})$。为了计算预测分布，首先注意到，函数 $\sigma(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})$ 对 $\mathbf{w}$ 的依赖，仅通过 $\mathbf{w}$ 在 $\boldsymbol{\phi}$ 上的投影体现。记 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$，有

$$
\sigma(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})=\int\delta(a-\mathbf{w}^{\mathrm T}\boldsymbol{\phi})\sigma(a)\,da
\tag{4.146}
$$

其中 $\delta(\cdot)$ 是 Dirac delta 函数。由此得到

$$
\int\sigma(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})q(\mathbf{w})\,d\mathbf{w}=\int\sigma(a)p(a)\,da
\tag{4.147}
$$

<!-- pdf-page: 239 -->

其中

$$
p(a)=\int\delta(a-\mathbf{w}^{\mathrm T}\boldsymbol{\phi})q(\mathbf{w})\,d\mathbf{w}.
\tag{4.148}
$$

计算 $p(a)$ 时，可以注意到 delta 函数对 $\mathbf{w}$ 施加了一个线性约束，因此，它通过将所有与 $\boldsymbol{\phi}$ 正交的方向积分掉，从联合分布 $q(\mathbf{w})$ 得到一个边缘分布。由于 $q(\mathbf{w})$ 是高斯分布，根据 2.3.2 节可知，边缘分布也一定是高斯分布。通过求矩，并交换关于 $a$ 和 $\mathbf{w}$ 的积分次序，可以计算该分布的均值和协方差，从而得到

$$
\mu_a=\mathbb{E}[a]=\int p(a)a\,da=\int q(\mathbf{w})\mathbf{w}^{\mathrm T}\boldsymbol{\phi}\,d\mathbf{w}=\mathbf{w}_{\mathrm{MAP}}^{\mathrm T}\boldsymbol{\phi}
\tag{4.149}
$$

这里使用了变分后验分布 $q(\mathbf{w})$ 的结果（4.144）。同样，

$$
\begin{aligned}
\sigma_a^2&=\operatorname{var}[a]=\int p(a)\left\{a^2-\mathbb{E}[a]^2\right\}\,da\\
&=\int q(\mathbf{w})\left\{(\mathbf{w}^{\mathrm T}\boldsymbol{\phi})^2-(\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi})^2\right\}\,d\mathbf{w}=\boldsymbol{\phi}^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}.
\end{aligned}
\tag{4.150}
$$

注意，$a$ 的分布与将噪声方差设为零后的线性回归模型预测分布（3.58）具有相同形式。因此，对预测分布的变分近似变为

$$
p(\mathcal{C}_1\mid\boldsymbol{\mathsf{t}})=\int\sigma(a)p(a)\,da=\int\sigma(a)\mathcal{N}(a\mid\mu_a,\sigma_a^2)\,da.
\tag{4.151}
$$

这一结果也可以直接利用 2.3.2 节中关于高斯分布边缘分布的结果推导出来（习题 4.24）。

关于 $a$ 的积分表示高斯分布与 logistic sigmoid 的卷积，无法解析计算。不过，可以利用（4.59）定义的 logistic sigmoid 函数 $\sigma(a)$ 与（4.114）定义的 probit 函数 $\Phi(a)$ 之间的高度相似性，得到一个良好的近似（Spiegelhalter and Lauritzen, 1990; MacKay, 1992b; Barber and Bishop, 1998a）。为了尽可能准确地近似 logistic 函数，需要重新缩放横轴，也就是用 $\Phi(\lambda a)$ 近似 $\sigma(a)$。可以通过要求两个函数在原点处具有相同斜率来确定合适的 $\lambda$ 值，得到 $\lambda^2=\pi/8$（习题 4.25）。在这种 $\lambda$ 选择下，logistic sigmoid 与 probit 函数的相似性见图 4.9。

使用 probit 函数的优点是：它与高斯分布的卷积可以解析地表示为另一个 probit 函数。具体来说，可以证明（习题 4.26）

$$
\int\Phi(\lambda a)\mathcal{N}(a\mid\mu,\sigma^2)\,da=\Phi\left(\frac{\mu}{(\lambda^{-2}+\sigma^2)^{1/2}}\right).
\tag{4.152}
$$

<!-- pdf-page: 240 -->

现在，对该方程两侧的 probit 函数应用近似 $\sigma(a)\simeq\Phi(\lambda a)$，得到 logistic sigmoid 与高斯分布卷积的如下近似：

$$
\int\sigma(a)\mathcal{N}(a\mid\mu,\sigma^2)\,da\simeq\sigma\left(\kappa(\sigma^2)\mu\right)
\tag{4.153}
$$

其中定义

$$
\kappa(\sigma^2)=(1+\pi\sigma^2/8)^{-1/2}.
\tag{4.154}
$$

将这一结果用于（4.151），得到如下形式的近似预测分布：

$$
p(\mathcal{C}_1\mid\boldsymbol{\phi},\boldsymbol{\mathsf{t}})=\sigma\left(\kappa(\sigma_a^2)\mu_a\right)
\tag{4.155}
$$

其中 $\mu_a$ 与 $\sigma_a^2$ 分别由（4.149）和（4.150）定义，$\kappa(\sigma_a^2)$ 由（4.154）定义。

注意，对应于 $p(\mathcal{C}_1\mid\boldsymbol{\phi},\boldsymbol{\mathsf{t}})=0.5$ 的决策边界为 $\mu_a=0$，它与使用 $\mathbf{w}$ 的 MAP 值得到的决策边界相同。因此，如果决策准则是在先验概率相等的条件下最小化误分类率，那么对 $\mathbf{w}$ 的边缘化就没有影响。不过，对于更复杂的决策准则，边缘化会起到重要作用。图 10.13 将在变分推断的背景下，展示如何在后验分布的高斯近似下，对 logistic sigmoid 模型进行边缘化。

## 习题

**4.1（⋆⋆）** 给定一组数据点 $\{\mathbf{x}_n\}$，可以将*凸包*定义为满足下式的所有点 $\mathbf{x}$ 构成的集合：

$$
\mathbf{x}=\sum_n\alpha_n\mathbf{x}_n
\tag{4.156}
$$

其中 $\alpha_n\geqslant0$，且 $\sum_n\alpha_n=1$。考虑第二组点 $\{\mathbf{y}_n\}$ 及其相应的凸包。根据定义，如果存在向量 $\widehat{\mathbf{w}}$ 和标量 $w_0$，使得对所有 $\mathbf{x}_n$ 都有 $\widehat{\mathbf{w}}^{\mathrm T}\mathbf{x}_n+w_0>0$，并且对所有 $\mathbf{y}_n$ 都有 $\widehat{\mathbf{w}}^{\mathrm T}\mathbf{y}_n+w_0<0$，那么这两组点就是线性可分的。证明，如果它们的凸包相交，这两组点就不可能线性可分；反过来，如果它们线性可分，其凸包就不相交。

**4.2（⋆⋆）www** 考虑最小化平方和误差函数（4.15），假设训练集中所有目标向量都满足一个线性约束

$$
\mathbf{a}^{\mathrm T}\mathbf{t}_n+b=0
\tag{4.157}
$$

其中 $\mathbf{t}_n$ 对应于（4.15）中矩阵 $\mathbf{T}$ 的第 $n$ 行。证明，由于这个约束，由最小二乘解（4.17）给出的模型预测 $\mathbf{y}(\mathbf{x})$ 的各元素也满足该约束，即

$$
\mathbf{a}^{\mathrm T}\mathbf{y}(\mathbf{x})+b=0.
\tag{4.158}
$$

<!-- pdf-page: 241 -->

为此，假设有一个基函数 $\phi_0(\mathbf{x})=1$，使相应的参数 $w_0$ 起偏置作用。

**4.3（⋆⋆）** 推广习题 4.2 的结果，证明：如果目标向量同时满足多个线性约束，那么线性模型的最小二乘预测也会满足这些约束。

**4.4（⋆）www** 使用拉格朗日乘数来施加约束 $\mathbf{w}^{\mathrm T}\mathbf{w}=1$，证明关于 $\mathbf{w}$ 最大化（4.23）给出的类别分离准则，会得到 $\mathbf{w}\propto(\mathbf{m}_2-\mathbf{m}_1)$。

**4.5（⋆）** 利用（4.20）、（4.23）和（4.24），证明 Fisher 准则（4.25）可以写成（4.26）的形式。

**4.6（⋆）** 利用（4.27）与（4.28）分别给出的类间和类内协方差矩阵定义，结合（4.34）、（4.36）以及 4.1.5 节所描述的目标值选择，证明使平方和误差函数最小的表达式（4.33）可以写成（4.37）的形式。

**4.7（⋆）www** 证明，logistic sigmoid 函数（4.59）满足性质 $\sigma(-a)=1-\sigma(a)$，其反函数为 $\sigma^{-1}(y)=\ln\{y/(1-y)\}$。

**4.8（⋆）** 利用（4.57）和（4.58），推导采用高斯密度的二类生成式模型中类别后验概率的结果（4.65），并验证参数 $\mathbf{w}$ 与 $w_0$ 的结果（4.66）和（4.67）。

**4.9（⋆）www** 考虑一个 $K$ 类的生成式分类模型，它由类别先验概率 $p(\mathcal{C}_k)=\pi_k$ 和一般的类条件密度 $p(\boldsymbol{\phi}\mid\mathcal{C}_k)$ 定义，其中 $\boldsymbol{\phi}$ 是输入特征向量。假设给定训练数据集 $\{\boldsymbol{\phi}_n,\mathbf{t}_n\}$，其中 $n=1,\ldots,N$，$\mathbf{t}_n$ 是采用 1-of-$K$ 编码、长度为 $K$ 的二元目标向量：若模式 $n$ 来自类别 $\mathcal{C}_k$，则其分量为 $t_{nj}=I_{jk}$。假设数据点独立地从该模型中抽取，证明先验概率的最大似然解为

$$
\pi_k=\frac{N_k}{N}
\tag{4.159}
$$

其中 $N_k$ 是被分配到类别 $\mathcal{C}_k$ 的数据点数。

**4.10（⋆⋆）** 考虑习题 4.9 的分类模型，现在假设类条件密度是具有共享协方差矩阵的高斯分布，即

$$
p(\boldsymbol{\phi}\mid\mathcal{C}_k)=\mathcal{N}(\boldsymbol{\phi}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}).
\tag{4.160}
$$

证明，类别 $\mathcal{C}_k$ 的高斯分布均值的最大似然解为

$$
\boldsymbol{\mu}_k=\frac{1}{N_k}\sum_{n=1}^{N}t_{nk}\boldsymbol{\phi}_n
\tag{4.161}
$$

<!-- pdf-page: 242 -->

它表示被分配到类别 $\mathcal{C}_k$ 的那些特征向量的均值。同样，证明共享协方差矩阵的最大似然解为

$$
\boldsymbol{\Sigma}=\sum_{k=1}^{K}\frac{N_k}{N}\mathbf{S}_k
\tag{4.162}
$$

其中

$$
\mathbf{S}_k=\frac{1}{N_k}\sum_{n=1}^{N}t_{nk}(\boldsymbol{\phi}_n-\boldsymbol{\mu}_k)(\boldsymbol{\phi}_n-\boldsymbol{\mu}_k)^{\mathrm T}.
\tag{4.163}
$$

因此，$\boldsymbol{\Sigma}$ 是各个类别数据协方差的加权平均，权重系数由类别先验概率给出。

**4.11（⋆⋆）** 考虑一个 $K$ 类分类问题，其特征向量 $\boldsymbol{\phi}$ 有 $M$ 个分量，每个分量可取 $L$ 个离散状态。用 1-of-$L$ 二元编码表示各分量的值。进一步假设，给定类别 $\mathcal{C}_k$ 时，$\boldsymbol{\phi}$ 的 $M$ 个分量相互独立，因此类条件密度可以按特征向量的分量分解。证明，（4.63）给出的 $a_k$，也就是描述类别后验概率的 softmax 函数的自变量，是 $\boldsymbol{\phi}$ 各分量的线性函数。注意，这是 8.2.2 节所讨论的朴素贝叶斯模型的一个例子。

**4.12（⋆）www** 验证（4.59）定义的 logistic sigmoid 函数的导数满足关系（4.88）。

**4.13（⋆）www** 利用 logistic sigmoid 导数的结果（4.88），证明逻辑回归模型的误差函数（4.90）的导数由（4.91）给出。

**4.14（⋆）** 证明，对于线性可分的数据集，逻辑回归模型的最大似然解可以通过以下方式获得：找到一个向量 $\mathbf{w}$，使其决策边界 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})=0$ 将各类别分开，再令 $\mathbf{w}$ 的大小趋于无穷。

**4.15（⋆⋆）** 证明，（4.97）给出的逻辑回归模型的 Hessian 矩阵 $\mathbf{H}$ 是正定的。这里，$\mathbf{R}$ 是元素为 $y_n(1-y_n)$ 的对角矩阵，$y_n$ 是输入向量 $\mathbf{x}_n$ 对应的逻辑回归模型输出。由此证明，误差函数是 $\mathbf{w}$ 的凹函数，并具有唯一的最小值。

**4.16（⋆）** 考虑一个二分类问题，已知每个观测 $\mathbf{x}_n$ 属于两个类别之一，分别对应 $t=0$ 和 $t=1$。假设收集训练数据的过程并不完善，训练点有时会被标错。对于每个数据点 $\mathbf{x}_n$，得到的不是类别标签值 $t$，而是一个表示 $t_n=1$ 概率的值 $\pi_n$。给定概率模型 $p(t=1\mid\boldsymbol{\phi})$，写出适用于这种数据集的对数似然函数。

<!-- pdf-page: 243 -->

**4.17（⋆）www** 证明，softmax 激活函数（4.104）的导数由（4.106）给出，其中 $a_k$ 由（4.105）定义。

**4.18（⋆）** 利用 softmax 激活函数导数的结果（4.91），证明交叉熵误差（4.108）的梯度由（4.109）给出。

**4.19（⋆）www** 对于 4.3.5 节定义的 Probit 回归模型，写出对数似然梯度及其相应 Hessian 矩阵的表达式。使用 IRLS 训练这类模型时，就需要这些量。

**4.20（⋆⋆）** 证明，（4.110）定义的多类别逻辑回归问题的 Hessian 矩阵是半正定的。注意，该问题的完整 Hessian 矩阵大小为 $MK\times MK$，其中 $M$ 是参数数目，$K$ 是类别数。为了证明半正定性，考虑乘积 $\mathbf{u}^{\mathrm T}\mathbf{H}\mathbf{u}$，其中 $\mathbf{u}$ 是长度为 $MK$ 的任意向量，然后应用 Jensen 不等式。

**4.21（⋆）** 证明，probit 函数（4.114）与 erf 函数（4.115）之间存在关系（4.116）。

**4.22（⋆）** 利用结果（4.135），推导拉普拉斯近似下对数模型证据的表达式（4.137）。

**4.23（⋆⋆）www** 本题从（4.137）给出的模型证据的拉普拉斯近似出发，推导 BIC 结果（4.139）。证明，如果参数的先验为高斯分布 $p(\boldsymbol{\theta})=\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{m},\mathbf{V}_0)$，那么拉普拉斯近似下的对数模型证据具有如下形式：

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid\boldsymbol{\theta}_{\mathrm{MAP}})-\frac{1}{2}(\boldsymbol{\theta}_{\mathrm{MAP}}-\mathbf{m})^{\mathrm T}\mathbf{V}_0^{-1}(\boldsymbol{\theta}_{\mathrm{MAP}}-\mathbf{m})-\frac{1}{2}\ln|\mathbf{H}|+\text{const}
$$

其中 $\mathbf{H}$ 是对数似然 $\ln p(\mathcal{D}\mid\boldsymbol{\theta})$ 在 $\boldsymbol{\theta}_{\mathrm{MAP}}$ 处的二阶导数矩阵。现在假设先验较宽，使 $\mathbf{V}_0^{-1}$ 较小，从而可以忽略上式右侧的第二项。再考虑数据独立同分布的情况，此时 $\mathbf{H}$ 是各数据点所对应项的总和。证明，这时对数模型证据可以近似写成 BIC 表达式（4.139）的形式。

**4.24（⋆⋆）** 利用 2.3.2 节的结果，推导对逻辑回归模型按参数 $\mathbf{w}$ 的高斯后验分布进行边缘化的结果（4.151）。

**4.25（⋆⋆）** 假设要用经过缩放的 probit 函数 $\Phi(\lambda a)$ 近似（4.59）定义的 logistic sigmoid $\sigma(a)$，其中 $\Phi(a)$ 由（4.114）定义。证明，如果选择 $\lambda$ 使两个函数在 $a=0$ 处的导数相等，则 $\lambda^2=\pi/8$。

<!-- pdf-page: 244 -->

**4.26（⋆⋆）** 本题证明 probit 函数与高斯分布卷积的关系（4.152）。为此，先证明左侧关于 $\mu$ 的导数等于右侧的导数，再对两侧关于 $\mu$ 积分，并证明积分常数为零。注意，在对左侧求导之前，先引入变量代换 $a=\mu+\sigma z$ 会更方便，使关于 $a$ 的积分变成关于 $z$ 的积分。这样，在对关系（4.152）的左侧求导时，就会得到一个可以解析计算的关于 $z$ 的高斯积分。
