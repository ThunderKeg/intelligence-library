<!-- pdf-page: 647 -->

# 附录 A 数学基础

<aside class="chapter-guide"><p>导读（编者）：本附录汇总阅读正文所需的数学概念与记号，包括范数、集合与函数、导数，以及常用的线性代数结论。可以按需查阅，尤其注意同一记号用于向量和矩阵时的含义，以及各个结论所要求的条件。</p></aside>

本附录简要回顾分析与线性代数中的一些基本概念。这里的介绍远非完整，主要目的是说明我们采用的记号。

## A.1 范数

### A.1.1 内积、欧几里得范数与夹角

实 $n$ 维向量的集合 $\mathbf{R}^n$ 上的标准内积为

$$
\langle x,y\rangle=x^Ty=\sum_{i=1}^n x_i y_i,
$$

其中 $x,y\in\mathbf{R}^n$。本书使用记号 $x^Ty$，而不用 $\langle x,y\rangle$。向量 $x\in\mathbf{R}^n$ 的欧几里得范数，或称 $\ell_2$ 范数，定义为

$$
\|x\|_2=(x^Tx)^{1/2}=(x_1^2+\cdots+x_n^2)^{1/2}.
\tag{A.1}
$$

Cauchy–Schwartz 不等式指出，对任意 $x,y\in\mathbf{R}^n$，都有 $|x^Ty|\leq\|x\|_2\|y\|_2$。非零向量 $x,y\in\mathbf{R}^n$ 之间的（无符号）夹角定义为

$$
\angle(x,y)=\cos^{-1}\left(\frac{x^Ty}{\|x\|_2\|y\|_2}\right),
$$

其中取 $\cos^{-1}(u)\in[0,\pi]$。若 $x^Ty=0$，则称 $x$ 与 $y$ 正交。

实 $m\times n$ 矩阵的集合 $\mathbf{R}^{m\times n}$ 上的标准内积为

$$
\langle X,Y\rangle=\mathbf{tr}(X^TY)=\sum_{i=1}^m\sum_{j=1}^n X_{ij}Y_{ij},
$$

其中 $X,Y\in\mathbf{R}^{m\times n}$。（这里 $\mathbf{tr}$ 表示矩阵的迹，即对角元素之和。）我们使用记号 $\mathbf{tr}(X^TY)$，而不用 $\langle X,Y\rangle$。注意，两个矩阵的<!-- pdf-page: 648 -->内积，等于将各矩阵的元素按某种顺序（例如逐行）排列后得到的两个 $\mathbf{R}^{mn}$ 中的向量的内积。

矩阵 $X\in\mathbf{R}^{m\times n}$ 的 Frobenius 范数为

$$
\|X\|_F=\bigl(\mathbf{tr}(X^TX)\bigr)^{1/2}
=\left(\sum_{i=1}^m\sum_{j=1}^n X_{ij}^2\right)^{1/2}.
\tag{A.2}
$$

Frobenius 范数就是将矩阵各元素排列成向量后，该向量的欧几里得范数。（矩阵的 $\ell_2$ 范数是另一种范数；见 §A.1.5。）

对称 $n\times n$ 矩阵的集合 $\mathbf{S}^n$ 上的标准内积为

$$
\langle X,Y\rangle=\mathbf{tr}(XY)
=\sum_{i=1}^n\sum_{j=1}^n X_{ij}Y_{ij}
=\sum_{i=1}^n X_{ii}Y_{ii}+2\sum_{i<j}X_{ij}Y_{ij}.
$$

### A.1.2 范数、距离与单位球

若定义域为 $\mathbf{dom}\,f=\mathbf{R}^n$ 的函数 $f:\mathbf{R}^n\to\mathbf{R}$ 满足下列条件，则称它为范数：

- $f$ 非负：对所有 $x\in\mathbf{R}^n$，都有 $f(x)\geq0$。
- $f$ 具有正定性（definite）：仅当 $x=0$ 时才有 $f(x)=0$。
- $f$ 是齐次的：对所有 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}$，都有 $f(tx)=|t|f(x)$。
- $f$ 满足三角不等式：对所有 $x,y\in\mathbf{R}^n$，都有 $f(x+y)\leq f(x)+f(y)$。

我们使用记号 $f(x)=\|x\|$，意在表明范数是 $\mathbf{R}$ 上绝对值的推广。需要指定某个范数时，使用记号 $\|x\|_{\mathrm{symb}}$，其中下标是用来辨认该范数的助记符号。

范数衡量向量 $x$ 的长度；两个向量 $x$ 和 $y$ 之间的距离，可以用它们之差的长度来衡量，即

$$
\mathbf{dist}(x,y)=\|x-y\|.
$$

我们称 $\mathbf{dist}(x,y)$ 为范数 $\|\cdot\|$ 下 $x$ 与 $y$ 之间的距离。

所有范数不超过一的向量组成的集合

$$
\mathcal{B}=\{x\in\mathbf{R}^n\mid\|x\|\leq1\},
$$

称为范数 $\|\cdot\|$ 的单位球。单位球满足下列性质：

- $\mathcal{B}$ 关于原点对称，即 $x\in\mathcal{B}$ 当且仅当 $-x\in\mathcal{B}$。
- $\mathcal{B}$ 是凸集。
- $\mathcal{B}$ 是闭集、有界，而且内部非空。

反过来，若集合 $C\subseteq\mathbf{R}^n$ 满足这三个条件，它就是某个范数的单位球，这个范数为

$$
\|x\|=\bigl(\sup\{t\geq0\mid tx\in C\}\bigr)^{-1}.
$$

<!-- pdf-page: 649 -->

### A.1.3 例子

范数最简单的例子是 $\mathbf{R}$ 上的绝对值。另一个简单例子是 $\mathbf{R}^n$ 上的欧几里得范数，即 $\ell_2$ 范数，其定义见上面的式 (A.1)。$\mathbf{R}^n$ 上另外两个常用范数是绝对值之和范数（sum-absolute-value norm），即 $\ell_1$ 范数，

$$
\|x\|_1=|x_1|+\cdots+|x_n|,
$$

以及 Chebyshev 范数，即 $\ell_\infty$ 范数，

$$
\|x\|_\infty=\max\{|x_1|,\ldots,|x_n|\}.
$$

这三个范数属于同一个范数族，其参数通常记为常数 $p$，满足 $p\geq1$：$\ell_p$ 范数定义为

$$
\|x\|_p=(|x_1|^p+\cdots+|x_n|^p)^{1/p}.
$$

当 $p=1$ 时，它就是 $\ell_1$ 范数；当 $p=2$ 时，它就是欧几里得范数。容易证明，对任意 $x\in\mathbf{R}^n$，都有

$$
\lim_{p\to\infty}\|x\|_p=\max\{|x_1|,\ldots,|x_n|\},
$$

因此 $\ell_\infty$ 范数也作为一个极限包含在这个范数族中。

另一类重要的范数是二次范数。对于 $P\in\mathbf{S}_{++}^n$，我们将 $P$ 二次范数定义为

$$
\|x\|_P=(x^TPx)^{1/2}=\|P^{1/2}x\|_2.
$$

二次范数的单位球是椭球；反过来，如果一个范数的单位球是椭球，那么这个范数就是二次范数。

$\mathbf{R}^{m\times n}$ 上的一些常用范数包括上面式 (A.2) 定义的 Frobenius 范数、绝对值之和范数

$$
\|X\|_{\mathrm{sav}}=\sum_{i=1}^m\sum_{j=1}^n|X_{ij}|,
$$

以及最大绝对值范数

$$
\|X\|_{\mathrm{mav}}=\max\{|X_{ij}|\mid i=1,\ldots,m,\ j=1,\ldots,n\}.
$$

我们将在 §A.1.5 中介绍另外几种重要的矩阵范数。

### A.1.4 范数的等价性

设 $\|\cdot\|_{\mathrm{a}}$ 和 $\|\cdot\|_{\mathrm{b}}$ 是 $\mathbf{R}^n$ 上的范数。分析中的一个基本结论是，存在正常数 $\alpha$ 和 $\beta$，使得对所有 $x\in\mathbf{R}^n$，都有

$$
\alpha\|x\|_{\mathrm{a}}\leq\|x\|_{\mathrm{b}}\leq\beta\|x\|_{\mathrm{a}}.
$$

<!-- pdf-page: 650 -->

这意味着这些范数是等价的，即它们定义相同的开子集、相同的收敛序列等（见 §A.2）。（由此可知，任意有限维向量空间上的所有范数都等价；但在无限维向量空间中，这个结论未必成立。）借助凸分析，可以给出一个更具体的结论：若 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的任意范数，则存在一个二次范数 $\|\cdot\|_P$，使得

$$
\|x\|_P\leq\|x\|\leq\sqrt{n}\|x\|_P
$$

对所有 $x$ 都成立。换言之，$\mathbf{R}^n$ 上的任意范数都能由某个二次范数一致逼近，两者相差的倍数不超过 $\sqrt{n}$。（见 §8.4.1。）

### A.1.5 算子范数

设 $\|\cdot\|_{\mathrm{a}}$ 和 $\|\cdot\|_{\mathrm{b}}$ 分别是 $\mathbf{R}^m$ 和 $\mathbf{R}^n$ 上的范数。由这两个范数诱导的矩阵 $X\in\mathbf{R}^{m\times n}$ 的算子范数定义为

$$
\|X\|_{\mathrm{a,b}}=\sup\{\|Xu\|_{\mathrm{a}}\mid\|u\|_{\mathrm{b}}\leq1\}.
$$

（可以证明，这在 $\mathbf{R}^{m\times n}$ 上定义了一个范数。）

当 $\|\cdot\|_{\mathrm{a}}$ 和 $\|\cdot\|_{\mathrm{b}}$ 都是欧几里得范数时，$X$ 的算子范数就是它的最大奇异值，记为 $\|X\|_2$：

$$
\|X\|_2=\sigma_{\max}(X)=\bigl(\lambda_{\max}(X^TX)\bigr)^{1/2}.
$$

（当 $X\in\mathbf{R}^{m\times1}$ 时，这与 $\mathbf{R}^m$ 上的欧几里得范数一致，因此记号并不冲突。）这个范数也称为 $X$ 的谱范数，或 $\ell_2$ 范数。

另一个例子是由 $\mathbf{R}^m$ 和 $\mathbf{R}^n$ 上的 $\ell_\infty$ 范数诱导的范数，记为 $\|X\|_\infty$，它是最大行和范数（max-row-sum norm）：

$$
\|X\|_\infty=\sup\{\|Xu\|_\infty\mid\|u\|_\infty\leq1\}
=\max_{i=1,\ldots,m}\sum_{j=1}^n|X_{ij}|.
$$

由 $\mathbf{R}^m$ 和 $\mathbf{R}^n$ 上的 $\ell_1$ 范数诱导的范数，记为 $\|X\|_1$，是最大列和范数（max-column-sum norm）：

$$
\|X\|_1=\max_{j=1,\ldots,n}\sum_{i=1}^m|X_{ij}|.
$$

### A.1.6 对偶范数

设 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的一个范数。与之对应的对偶范数记为 $\|\cdot\|_*$，定义为

$$
\|z\|_*=\sup\{z^Tx\mid\|x\|\leq1\}.
$$

（可以证明，这确实是一个范数。）把 $z^T$ 看作 $1\times n$ 矩阵，并在 $\mathbf{R}^n$ 上取范数 $\|\cdot\|$、在 $\mathbf{R}$ 上取绝对值，则对偶范数可以解释为 $z^T$ 的算子范数：

$$
\|z\|_*=\sup\{|z^Tx|\mid\|x\|\leq1\}.
$$

<!-- pdf-page: 651 -->

由对偶范数的定义可得不等式

$$
z^Tx\leq\|x\|\|z\|_*,
$$

它对所有 $x$ 和 $z$ 都成立。这个不等式是紧的，含义如下：对于任意 $x$，都存在一个 $z$，使不等式取等号。（类似地，对于任意 $z$，都存在一个 $x$ 使等号成立。）对偶范数的对偶就是原范数：对所有 $x$，都有 $\|x\|_{**}=\|x\|$。（在无限维向量空间中，这未必成立。）

欧几里得范数的对偶是欧几里得范数，因为

$$
\sup\{z^Tx\mid\|x\|_2\leq1\}=\|z\|_2.
$$

（这由 Cauchy–Schwarz 不等式得到；对于非零的 $z$，在 $\|x\|_2\leq1$ 上使 $z^Tx$ 最大的 $x$ 为 $z/\|z\|_2$。）

$\ell_\infty$ 范数的对偶是 $\ell_1$ 范数：

$$
\sup\{z^Tx\mid\|x\|_\infty\leq1\}=\sum_{i=1}^n|z_i|=\|z\|_1,
$$

而 $\ell_1$ 范数的对偶是 $\ell_\infty$ 范数。更一般地，$\ell_p$ 范数的对偶是 $\ell_q$ 范数，其中 $q$ 满足 $1/p+1/q=1$，即 $q=p/(p-1)$。

再看一个例子，考虑 $\mathbf{R}^{m\times n}$ 上的 $\ell_2$ 范数，即谱范数。其对应的对偶范数为

$$
\|Z\|_{2*}=\sup\{\mathbf{tr}(Z^TX)\mid\|X\|_2\leq1\},
$$

它恰好等于所有奇异值之和，

$$
\|Z\|_{2*}=\sigma_1(Z)+\cdots+\sigma_r(Z)=\mathbf{tr}(Z^TZ)^{1/2},
$$

其中 $r=\mathbf{rank}\,Z$。这个范数有时称为核范数（nuclear norm）。

## A.2 分析

### A.2.1 开集与闭集

若存在 $\epsilon>0$，使得

$$
\{y\mid\|y-x\|_2\leq\epsilon\}\subseteq C,
$$

即存在一个以 $x$ 为中心、完全包含在 $C$ 中的球，则称元素 $x\in C\subseteq\mathbf{R}^n$ 为 $C$ 的内点。$C$ 的所有内点组成的集合称为 $C$ 的内部，记为 $\mathbf{int}\,C$。（由于 $\mathbf{R}^n$ 上的所有范数都与欧几里得范数等价，用任何范数都会得到相同的内点集合。）若 $\mathbf{int}\,C=C$，即 $C$ 中的每个点都是内点，则称集合 $C$ 为开集。若集合 $C\subseteq\mathbf{R}^n$ 的补集 $\mathbf{R}^n\setminus C=\{x\in\mathbf{R}^n\mid x\notin C\}$ 是开集，则称 $C$ 为闭集。

<!-- pdf-page: 652 -->

集合 $C$ 的闭包定义为

$$
\mathbf{cl}\,C=\mathbf{R}^n\setminus\mathbf{int}(\mathbf{R}^n\setminus C),
$$

即先取 $C$ 的补集，再取其内部，最后再取补集。如果对每个 $\epsilon>0$，都存在 $y\in C$，使 $\|x-y\|_2\leq\epsilon$，那么点 $x$ 属于 $C$ 的闭包。

也可以用收敛序列及其极限点来描述闭集与闭包。集合 $C$ 是闭集，当且仅当它包含其中每个收敛序列的极限点。换言之，如果 $x_1,x_2,\ldots$ 收敛到 $x$，且 $x_i\in C$，那么 $x\in C$。$C$ 的闭包是 $C$ 中所有收敛序列的极限点组成的集合。

集合 $C$ 的边界定义为

$$
\mathbf{bd}\,C=\mathbf{cl}\,C\setminus\mathbf{int}\,C.
$$

边界点 $x$（即 $x\in\mathbf{bd}\,C$）满足下列性质：对所有 $\epsilon>0$，都存在 $y\in C$ 和 $z\notin C$，使

$$
\|y-x\|_2\leq\epsilon,\qquad\|z-x\|_2\leq\epsilon,
$$

即在 $C$ 中和 $C$ 外，都能找到任意接近 $x$ 的点。可以借助边界运算刻画闭集和开集：如果 $C$ 包含自己的边界，即 $\mathbf{bd}\,C\subseteq C$，那么它是闭集。如果它不包含任何边界点，即 $C\cap\mathbf{bd}\,C=\emptyset$，那么它是开集。

### A.2.2 上确界与下确界

设 $C\subseteq\mathbf{R}$。若对每个 $x\in C$，都有 $x\leq a$，则称数 $a$ 为 $C$ 的一个上界。集合 $C$ 的所有上界组成的集合，或者为空集（这时称 $C$ 上方无界），或者为整个 $\mathbf{R}$（仅在 $C=\emptyset$ 时出现），或者为一个闭的无穷区间 $[b,\infty)$。数 $b$ 称为集合 $C$ 的最小上界，或称上确界（supremum），记为 $\sup C$。约定 $\sup\emptyset=-\infty$；若 $C$ 上方无界，则 $\sup C=\infty$。当 $\sup C\in C$ 时，称 $C$ 的上确界能够取到。

当 $C$ 是有限集时，$\sup C$ 就是其中最大的元素。有些作者在上确界能够取到时，用记号 $\max C$ 表示上确界；但我们遵循标准的数学约定，仅在 $C$ 是有限集时使用 $\max C$。

下界和下确界以类似方式定义。若对每个 $x\in C$，都有 $a\leq x$，则数 $a$ 为 $C\subseteq\mathbf{R}$ 的一个下界。集合 $C\subseteq\mathbf{R}$ 的下确界（infimum），或称最大下界，定义为 $\inf C=-\sup(-C)$。当 $C$ 是有限集时，下确界就是其中最小的元素。约定 $\inf\emptyset=\infty$；若 $C$ 下方无界，即没有下界，则 $\inf C=-\infty$。

<!-- pdf-page: 653 -->

## A.3 函数

### A.3.1 函数记号

我们的函数记号大体遵循通常约定，但有一个例外。写

$$
f:A\to B
$$

时，我们表示的是一个从集合 $\mathbf{dom}\,f\subseteq A$ 映入集合 $B$ 的函数 $f$；特别地，$\mathbf{dom}\,f$ 可以是 $A$ 的真子集。因此，记号 $f:\mathbf{R}^n\to\mathbf{R}^m$ 表示 $f$ 将（某些）$n$ 维向量映为 $m$ 维向量，并不表示对每个 $x\in\mathbf{R}^n$，$f(x)$ 都有定义。这个约定类似于计算机语言中的函数声明。指定函数输入、输出参数的数据类型，只是给出了这个函数的语法形式，并不保证具有所指定数据类型的每个输入参数都是有效的。

例如，考虑函数 $f:\mathbf{S}^n\to\mathbf{R}$，

$$
f(X)=\log\det X,
\tag{A.3}
$$

其定义域为 $\mathbf{dom}\,f=\mathbf{S}_{++}^n$。记号 $f:\mathbf{S}^n\to\mathbf{R}$ 规定了 $f$ 的语法形式：它接受一个对称 $n\times n$ 矩阵作为参数，返回一个实数。记号 $\mathbf{dom}\,f=\mathbf{S}_{++}^n$ 则说明哪些对称 $n\times n$ 矩阵是 $f$ 的有效输入参数（即仅有正定矩阵）。公式 (A.3) 说明，对于 $X\in\mathbf{dom}\,f$，$f(X)$ 的值是什么。

### A.3.2 连续性

若对所有 $\epsilon>0$，都存在 $\delta$，使

$$
y\in\mathbf{dom}\,f,\quad\|y-x\|_2\leq\delta
\quad\Longrightarrow\quad
\|f(y)-f(x)\|_2\leq\epsilon,
$$

则称函数 $f:\mathbf{R}^n\to\mathbf{R}^m$ 在 $x\in\mathbf{dom}\,f$ 处连续。

<div class="translator-note" markdown="1">

**译注（连续性定义中的正数条件）：** 这里的 $\delta$ 应要求 $\delta>0$。原文未明确写出这一条件；若允许 $\delta=0$，上面的蕴含式对任何函数都成立，不能用来定义连续性。

</div>

可以用极限来描述连续性：只要 $\mathbf{dom}\,f$ 中的序列 $x_1,x_2,\ldots$ 收敛到某点 $x\in\mathbf{dom}\,f$，序列 $f(x_1),f(x_2),\ldots$ 就收敛到 $f(x)$，即

$$
\lim_{i\to\infty}f(x_i)=f\left(\lim_{i\to\infty}x_i\right).
$$

如果函数 $f$ 在其定义域中的每一点都连续，则称 $f$ 是连续函数。

### A.3.3 闭函数

如果对于每个 $\alpha\in\mathbf{R}$，下水平集

$$
\{x\in\mathbf{dom}\,f\mid f(x)\leq\alpha\}
$$

都是闭集，则称函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是闭函数。这等价于要求 $f$ 的上图

$$
\mathbf{epi}\,f=\{(x,t)\in\mathbf{R}^{n+1}\mid x\in\mathbf{dom}\,f,\ f(x)\leq t\},
$$

<!-- pdf-page: 654 -->

是闭集。（这个定义是一般性的，但通常只用于凸函数。）

若 $f:\mathbf{R}^n\to\mathbf{R}$ 连续，且 $\mathbf{dom}\,f$ 是闭集，那么 $f$ 是闭函数。若 $f:\mathbf{R}^n\to\mathbf{R}$ 连续，且 $\mathbf{dom}\,f$ 是开集，那么 $f$ 是闭函数，当且仅当沿着每个收敛到 $\mathbf{dom}\,f$ 边界点的序列，$f$ 都趋于 $\infty$。换言之，若 $\lim_{i\to\infty}x_i=x\in\mathbf{bd}\,\mathbf{dom}\,f$，且 $x_i\in\mathbf{dom}\,f$，则有 $\lim_{i\to\infty}f(x_i)=\infty$。

<div class="example" id="example-A-1" markdown="1">

**例 A.1 $\mathbf{R}$ 上的例子。**

- 函数 $f:\mathbf{R}\to\mathbf{R}$，$f(x)=x\log x$，$\mathbf{dom}\,f=\mathbf{R}_{++}$，不是闭函数。

- 函数 $f:\mathbf{R}\to\mathbf{R}$，其中

    $$
    f(x)=
    \begin{cases}
    x\log x&x>0,\\
    0&x=0,
    \end{cases}
    \qquad\mathbf{dom}\,f=\mathbf{R}_+,
    $$

    是闭函数。

- 函数 $f(x)=-\log x$，$\mathbf{dom}\,f=\mathbf{R}_{++}$，是闭函数。

</div>

## A.4 导数

### A.4.1 导数与梯度

设 $f:\mathbf{R}^n\to\mathbf{R}^m$，且 $x\in\mathbf{int}\,\mathbf{dom}\,f$。若存在矩阵 $Df(x)\in\mathbf{R}^{m\times n}$，满足

$$
\lim_{\substack{z\in\mathbf{dom}\,f,\ z\ne x,\ z\to x}}
\frac{\|f(z)-f(x)-Df(x)(z-x)\|_2}{\|z-x\|_2}=0,
\tag{A.4}
$$

则称函数 $f$ 在 $x$ 处可微，并称 $Df(x)$ 为 $f$ 在 $x$ 处的导数，或 Jacobian 矩阵。（满足 (A.4) 的矩阵至多有一个。）若 $\mathbf{dom}\,f$ 是开集，且 $f$ 在其定义域的每一点都可微，则称 $f$ 是可微函数。

关于 $z$ 的仿射函数

$$
f(x)+Df(x)(z-x)
$$

称为 $f$ 在 $x$ 处（或附近）的一阶近似。显然，在 $z=x$ 处，这个函数与 $f$ 相等；当 $z$ 接近 $x$ 时，这个仿射函数与 $f$ 非常接近。

可以通过推导函数 $f$ 在 $x$ 处的一阶近似，求出其导数（即满足 (A.4) 的矩阵 $Df(x)$）；也可以由偏导数求得：

$$
Df(x)_{ij}=\frac{\partial f_i(x)}{\partial x_j},
\qquad i=1,\ldots,m,\quad j=1,\ldots,n.
$$

<!-- pdf-page: 655 -->

#### 梯度

当 $f$ 为实值函数（即 $f:\mathbf{R}^n\to\mathbf{R}$）时，导数 $Df(x)$ 是 $1\times n$ 矩阵，即行向量。它的转置称为函数的梯度：

$$
\nabla f(x)=Df(x)^T,
$$

这是一个（列）向量，即属于 $\mathbf{R}^n$。它的各分量是 $f$ 的偏导数：

$$
\nabla f(x)_i=\frac{\partial f(x)}{\partial x_i},
\qquad i=1,\ldots,n.
$$

$f$ 在点 $x\in\mathbf{int}\,\mathbf{dom}\,f$ 处的一阶近似可表示为（关于 $z$ 的仿射函数）

$$
f(x)+\nabla f(x)^T(z-x).
$$

#### 例子

先看一个简单例子，考虑二次函数 $f:\mathbf{R}^n\to\mathbf{R}$，

$$
f(x)=(1/2)x^TPx+q^Tx+r,
$$

其中 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$、$r\in\mathbf{R}$。它在 $x$ 处的导数为行向量 $Df(x)=x^TP+q^T$，梯度为

$$
\nabla f(x)=Px+q.
$$

再看一个更有意思的例子，考虑函数 $f:\mathbf{S}^n\to\mathbf{R}$，

$$
f(X)=\log\det X,\qquad\mathbf{dom}\,f=\mathbf{S}_{++}^n.
$$

求 $f$ 的梯度的一种（繁琐）方法是，为 $\mathbf{S}^n$ 引入一组基，求出相应函数的梯度，最后再把结果转换回 $\mathbf{S}^n$。我们将直接求 $f$ 在 $X\in\mathbf{S}_{++}^n$ 处的一阶近似。设 $Z\in\mathbf{S}_{++}^n$ 接近 $X$，令 $\Delta X=Z-X$，并假设它很小。于是有

$$
\begin{aligned}
\log\det Z
&=\log\det(X+\Delta X)\\
&=\log\det\left(X^{1/2}(I+X^{-1/2}\Delta X X^{-1/2})X^{1/2}\right)\\
&=\log\det X+\log\det(I+X^{-1/2}\Delta X X^{-1/2})\\
&=\log\det X+\sum_{i=1}^n\log(1+\lambda_i),
\end{aligned}
$$

其中 $\lambda_i$ 是 $X^{-1/2}\Delta X X^{-1/2}$ 的第 $i$ 个特征值。现在利用 $\Delta X$ 很小这一事实，可知 $\lambda_i$ 也很小，因此一阶近似给出 $\log(1+\lambda_i)\approx\lambda_i$。将这个一阶近似用于上式，得到

$$
\begin{aligned}
\log\det Z
&\approx\log\det X+\sum_{i=1}^n\lambda_i\\
&=\log\det X+\mathbf{tr}(X^{-1/2}\Delta X X^{-1/2})\\
&=\log\det X+\mathbf{tr}(X^{-1}\Delta X)\\
&=\log\det X+\mathbf{tr}\bigl(X^{-1}(Z-X)\bigr),
\end{aligned}
$$

<!-- pdf-page: 656 -->

这里利用了特征值之和等于迹这一事实，以及 $\mathbf{tr}(AB)=\mathbf{tr}(BA)$ 的性质。

因此，$f$ 在 $X$ 处的一阶近似是如下关于 $Z$ 的仿射函数：

$$
f(Z)\approx f(X)+\mathbf{tr}\bigl(X^{-1}(Z-X)\bigr).
$$

注意，右侧第二项就是 $X^{-1}$ 与 $Z-X$ 的标准内积，因此可以确定，$X^{-1}$ 就是 $f$ 在 $X$ 处的梯度。于是得到简单的公式

$$
\nabla f(X)=X^{-1}.
$$

这个结果并不意外，因为 $\log x$ 在 $\mathbf{R}_{++}$ 上的导数为 $1/x$。

### A.4.2 链式法则

设 $f:\mathbf{R}^n\to\mathbf{R}^m$ 在 $x\in\mathbf{int}\,\mathbf{dom}\,f$ 处可微，$g:\mathbf{R}^m\to\mathbf{R}^p$ 在 $f(x)\in\mathbf{int}\,\mathbf{dom}\,g$ 处可微。令 $h(z)=g(f(z))$，定义复合函数 $h:\mathbf{R}^n\to\mathbf{R}^p$。则 $h$ 在 $x$ 处可微，且其导数为

$$
Dh(x)=Dg(f(x))Df(x).
\tag{A.5}
$$

例如，设 $f:\mathbf{R}^n\to\mathbf{R}$、$g:\mathbf{R}\to\mathbf{R}$，且 $h(x)=g(f(x))$。对 $Dh(x)=Dg(f(x))Df(x)$ 取转置，得到

$$
\nabla h(x)=g'(f(x))\nabla f(x).
\tag{A.6}
$$

#### 与仿射函数复合

设 $f:\mathbf{R}^n\to\mathbf{R}^m$ 可微，$A\in\mathbf{R}^{n\times p}$，$b\in\mathbf{R}^n$。令 $g(x)=f(Ax+b)$，定义 $g:\mathbf{R}^p\to\mathbf{R}^m$，其定义域为 $\mathbf{dom}\,g=\{x\mid Ax+b\in\mathbf{dom}\,f\}$。由链式法则 (A.5)，$g$ 的导数为 $Dg(x)=Df(Ax+b)A$。

当 $f$ 为实值函数（即 $m=1$）时，得到函数与仿射函数复合后的梯度公式

$$
\nabla g(x)=A^T\nabla f(Ax+b).
$$

例如，设 $f:\mathbf{R}^n\to\mathbf{R}$，$x,v\in\mathbf{R}^n$，并以 $\tilde f(t)=f(x+tv)$ 定义函数 $\tilde f:\mathbf{R}\to\mathbf{R}$。（粗略地说，$\tilde f$ 是 $f$ 在直线 $\{x+tv\mid t\in\mathbf{R}\}$ 上的限制。）于是有

$$
D\tilde f(t)=\tilde f'(t)=\nabla f(x+tv)^Tv.
$$

（标量 $\tilde f'(0)$ 是 $f$ 在 $x$ 处沿方向 $v$ 的方向导数。）

<div class="example" id="example-A-2" markdown="1">

**例 A.2** 考虑函数 $f:\mathbf{R}^n\to\mathbf{R}$，其定义域为 $\mathbf{dom}\,f=\mathbf{R}^n$，且

$$
f(x)=\log\sum_{i=1}^m\exp(a_i^Tx+b_i),
$$

<!-- pdf-page: 657 -->

其中 $a_1,\ldots,a_m\in\mathbf{R}^n$，$b_1,\ldots,b_m\in\mathbf{R}$。注意，$f$ 是仿射函数 $Ax+b$ 与函数 $g:\mathbf{R}^m\to\mathbf{R}$ 的复合，其中 $A\in\mathbf{R}^{m\times n}$ 的各行为 $a_1^T,\ldots,a_m^T$，$g(y)=\log(\sum_{i=1}^m\exp y_i)$。利用这一点，可以得到其梯度的简单表达式。直接求导（或使用公式 (A.6)）可得

$$
\nabla g(y)=\frac{1}{\sum_{i=1}^m\exp y_i}
\begin{bmatrix}
\exp y_1\\
\vdots\\
\exp y_m
\end{bmatrix},
\tag{A.7}
$$

因此，由复合函数公式有

$$
\nabla f(x)=\frac{1}{\mathbf{1}^Tz}A^Tz
$$

其中 $z_i=\exp(a_i^Tx+b_i)$，$i=1,\ldots,m$。

</div>

<div class="example" id="example-A-3" markdown="1">

**例 A.3** 我们推导 $\nabla f(x)$ 的表达式，其中

$$
f(x)=\log\det(F_0+x_1F_1+\cdots+x_nF_n),
$$

$F_0,\ldots,F_n\in\mathbf{S}^p$，并且

$$
\mathbf{dom}\,f=\{x\in\mathbf{R}^n\mid F_0+x_1F_1+\cdots+x_nF_n\succ0\}.
$$

函数 $f$ 是从 $x\in\mathbf{R}^n$ 到 $F_0+x_1F_1+\cdots+x_nF_n\in\mathbf{S}^p$ 的仿射映射与函数 $\log\det X$ 的复合。利用链式法则计算

$$
\frac{\partial f(x)}{\partial x_i}
=\mathbf{tr}\bigl(F_i\nabla\log\det(F)\bigr)
=\mathbf{tr}(F^{-1}F_i),
$$

其中 $F=F_0+x_1F_1+\cdots+x_nF_n$。因此有

$$
\nabla f(x)=
\begin{bmatrix}
\mathbf{tr}(F^{-1}F_1)\\
\vdots\\
\mathbf{tr}(F^{-1}F_n)
\end{bmatrix}.
$$

</div>

### A.4.3 二阶导数

本节回顾实值函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的二阶导数。若 $f$ 在 $x\in\mathbf{int}\,\mathbf{dom}\,f$ 处二阶可微，则 $f$ 在 $x$ 处的二阶导数，或 Hessian 矩阵，记为 $\nabla^2f(x)$，其元素为

$$
\nabla^2f(x)_{ij}=\frac{\partial^2f(x)}{\partial x_i\partial x_j},
\qquad i=1,\ldots,n,\quad j=1,\ldots,n,
$$

其中各偏导数均在 $x$ 处取值。$f$ 在 $x$ 处或附近的二阶近似，是如下定义的关于 $z$ 的二次函数：

$$
\hat f(z)=f(x)+\nabla f(x)^T(z-x)+(1/2)(z-x)^T\nabla^2f(x)(z-x).
$$

<!-- pdf-page: 658 -->

这个二阶近似满足

$$
\lim_{\substack{z\in\mathbf{dom}\,f,\ z\ne x,\ z\to x}}
\frac{|f(z)-\hat f(z)|}{\|z-x\|_2^2}=0.
$$

不难理解，二阶导数可以解释为一阶导数的导数。若 $f$ 可微，则梯度映射是函数 $\nabla f:\mathbf{R}^n\to\mathbf{R}^n$，定义域为 $\mathbf{dom}\,\nabla f=\mathbf{dom}\,f$，在 $x$ 处的值为 $\nabla f(x)$。这个映射的导数为

$$
D\nabla f(x)=\nabla^2f(x).
$$

#### 例子

先看一个简单例子，考虑二次函数 $f:\mathbf{R}^n\to\mathbf{R}$，

$$
f(x)=(1/2)x^TPx+q^Tx+r,
$$

其中 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$、$r\in\mathbf{R}$。它的梯度为 $\nabla f(x)=Px+q$，因此 Hessian 矩阵为 $\nabla^2f(x)=P$。二次函数的二阶近似就是它自身。

再看一个较复杂的例子，仍考虑函数 $f:\mathbf{S}^n\to\mathbf{R}$，$f(X)=\log\det X$，定义域为 $\mathbf{dom}\,f=\mathbf{S}_{++}^n$。为了求出二阶近似，进而确定 Hessian 矩阵，我们将推导梯度 $\nabla f(X)=X^{-1}$ 的一阶近似。对于接近 $X\in\mathbf{S}_{++}^n$ 的 $Z\in\mathbf{S}_{++}^n$，令 $\Delta X=Z-X$，则有

$$
\begin{aligned}
Z^{-1}
&=(X+\Delta X)^{-1}\\
&=\left(X^{1/2}(I+X^{-1/2}\Delta X X^{-1/2})X^{1/2}\right)^{-1}\\
&=X^{-1/2}(I+X^{-1/2}\Delta X X^{-1/2})^{-1}X^{-1/2}\\
&\approx X^{-1/2}(I-X^{-1/2}\Delta X X^{-1/2})X^{-1/2}\\
&=X^{-1}-X^{-1}\Delta X X^{-1},
\end{aligned}
$$

这里使用了在 $A$ 很小时成立的一阶近似 $(I+A)^{-1}\approx I-A$。

这个近似足以让我们确定 $f$ 在 $X$ 处的 Hessian 矩阵。Hessian 矩阵是 $\mathbf{S}^n$ 上的一个二次型。一般情形下，描述这样的二次型很繁琐，因为需要四个下标。但由上面梯度的一阶近似，这个二次型可以表示为

$$
-\mathbf{tr}(X^{-1}UX^{-1}V),
$$

其中 $U,V\in\mathbf{S}^n$ 是二次型的自变量。（这是标量情形下公式 $(\log x)''=-1/x^2$ 的推广。）

现在得到 $f$ 在 $X$ 附近的二阶近似：

$$
\begin{aligned}
f(Z)
&=f(X+\Delta X)\\
&\approx f(X)+\mathbf{tr}(X^{-1}\Delta X)
-(1/2)\mathbf{tr}(X^{-1}\Delta X X^{-1}\Delta X)\\
&\approx f(X)+\mathbf{tr}\bigl(X^{-1}(Z-X)\bigr)
-(1/2)\mathbf{tr}\bigl(X^{-1}(Z-X)X^{-1}(Z-X)\bigr).
\end{aligned}
$$

<!-- pdf-page: 659 -->

### A.4.4 二阶导数的链式法则

二阶导数的一般链式法则在大多数情况下很繁琐，因此这里只给出我们需要的几个特殊情形。

#### 与标量函数复合

设 $f:\mathbf{R}^n\to\mathbf{R}$、$g:\mathbf{R}\to\mathbf{R}$，且 $h(x)=g(f(x))$。直接计算偏导数，得到

$$
\nabla^2h(x)=g'(f(x))\nabla^2f(x)+g''(f(x))\nabla f(x)\nabla f(x)^T.
\tag{A.8}
$$

#### 与仿射函数复合

设 $f:\mathbf{R}^n\to\mathbf{R}$，$A\in\mathbf{R}^{n\times m}$，$b\in\mathbf{R}^n$。令 $g(x)=f(Ax+b)$，定义 $g:\mathbf{R}^m\to\mathbf{R}$。则有

$$
\nabla^2g(x)=A^T\nabla^2f(Ax+b)A.
$$

例如，考虑实值函数 $f$ 在一条直线上的限制，即函数 $\tilde f(t)=f(x+tv)$，其中 $x$ 和 $v$ 固定。则有

$$
\nabla^2\tilde f(t)=\tilde f''(t)=v^T\nabla^2f(x+tv)v.
$$

<div class="example" id="example-A-4" markdown="1">

**例 A.4** 考虑例 A.2 中的函数 $f:\mathbf{R}^n\to\mathbf{R}$，

$$
f(x)=\log\sum_{i=1}^m\exp(a_i^Tx+b_i),
$$

其中 $a_1,\ldots,a_m\in\mathbf{R}^n$，$b_1,\ldots,b_m\in\mathbf{R}$。注意到 $f(x)=g(Ax+b)$，其中 $g(y)=\log(\sum_{i=1}^m\exp y_i)$，可以得到 $f$ 的 Hessian 矩阵的简单公式。计算偏导数，或者注意到 $g$ 是 $\log$ 与 $\sum_{i=1}^m\exp y_i$ 的复合并使用公式 (A.8)，得到

$$
\nabla^2g(y)=\mathbf{diag}(\nabla g(y))-\nabla g(y)\nabla g(y)^T,
$$

其中 $\nabla g(y)$ 由 (A.7) 给出。由复合函数公式，有

$$
\nabla^2f(x)=A^T\left(
\frac{1}{\mathbf{1}^Tz}\mathbf{diag}(z)
-\frac{1}{(\mathbf{1}^Tz)^2}zz^T
\right)A,
$$

其中 $z_i=\exp(a_i^Tx+b_i)$，$i=1,\ldots,m$。

</div>

## A.5 线性代数

### A.5.1 值域与零空间

设 $A\in\mathbf{R}^{m\times n}$（即 $A$ 是一个有 $m$ 行、$n$ 列的实矩阵）。$A$ 的值域记为 $\mathcal{R}(A)$，是 $\mathbf{R}^m$ 中所有能够表示成 $A$ 各列的线性<!-- pdf-page: 660 -->组合的向量所构成的集合，即

$$
\mathcal{R}(A)=\{Ax\mid x\in\mathbf{R}^n\}.
$$

值域 $\mathcal{R}(A)$ 是 $\mathbf{R}^m$ 的一个子空间，即它本身也是一个向量空间。它的维数就是 $A$ 的秩，记为 $\mathbf{rank}\,A$。$A$ 的秩不可能大于 $m$ 和 $n$ 中的较小者。如果 $\mathbf{rank}\,A=\min\{m,n\}$，则称 $A$ 满秩。

$A$ 的零空间（nullspace），或称核（kernel），记为 $\mathcal{N}(A)$，是所有被 $A$ 映为零的向量 $x$ 组成的集合：

$$
\mathcal{N}(A)=\{x\mid Ax=0\}.
$$

零空间是 $\mathbf{R}^n$ 的一个子空间。

#### 由 $A$ 诱导的正交分解

若 $\mathcal{V}$ 是 $\mathbf{R}^n$ 的一个子空间，则其正交补记为 $\mathcal{V}^\perp$，定义为

$$
\mathcal{V}^\perp=\{x\mid z^Tx=0\text{ 对所有 }z\in\mathcal{V}\text{ 成立}\}.
$$

（正如对补空间所预期的，我们有 $\mathcal{V}^{\perp\perp}=\mathcal{V}$。）

线性代数的一个基本结论是，对任意 $A\in\mathbf{R}^{m\times n}$，都有

$$
\mathcal{N}(A)=\mathcal{R}(A^T)^\perp.
$$

（将这个结论用于 $A^T$，还可得 $\mathcal{R}(A)=\mathcal{N}(A^T)^\perp$。）这个结论常写为

$$
\mathcal{N}(A)\mathbin{\overset{\perp}{\oplus}}\mathcal{R}(A^T)=\mathbf{R}^n.
\tag{A.9}
$$

这里的符号 $\mathbin{\overset{\perp}{\oplus}}$ 表示正交直和，即两个相互正交的子空间之和。$\mathbf{R}^n$ 的分解 (A.9) 称为由 $A$ 诱导的正交分解。

### A.5.2 对称矩阵的特征值分解

设 $A\in\mathbf{S}^n$，即 $A$ 是实对称 $n\times n$ 矩阵。则 $A$ 可以分解为

$$
A=Q\Lambda Q^T,
\tag{A.10}
$$

其中 $Q\in\mathbf{R}^{n\times n}$ 是正交矩阵，即满足 $Q^TQ=I$，而 $\Lambda=\mathbf{diag}(\lambda_1,\ldots,\lambda_n)$。实数 $\lambda_i$ 是 $A$ 的特征值，也是特征多项式 $\det(sI-A)$ 的根。$Q$ 的各列构成 $A$ 的一组标准正交特征向量。分解 (A.10) 称为 $A$ 的谱分解，或（对称）特征值分解。

我们将特征值按 $\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_n$ 排序。用记号 $\lambda_i(A)$ 表示 $A\in\mathbf{S}$ 的第 $i$ 大特征值。通常将最大特征值写为 $\lambda_1(A)=\lambda_{\max}(A)$，将最小特征值写为 $\lambda_n(A)=\lambda_{\min}(A)$。

<!-- pdf-page: 661 -->

行列式和迹可以用特征值表示：

$$
\det A=\prod_{i=1}^n\lambda_i,\qquad
\mathbf{tr}\,A=\sum_{i=1}^n\lambda_i,
$$

谱范数和 Frobenius 范数也一样：

$$
\|A\|_2=\max_{i=1,\ldots,n}|\lambda_i|=\max\{\lambda_1,-\lambda_n\},
\qquad
\|A\|_F=\left(\sum_{i=1}^n\lambda_i^2\right)^{1/2}.
$$

#### 定性与矩阵不等式

最大和最小特征值满足

$$
\lambda_{\max}(A)=\sup_{x\ne0}\frac{x^TAx}{x^Tx},
\qquad
\lambda_{\min}(A)=\inf_{x\ne0}\frac{x^TAx}{x^Tx}.
$$

特别地，对任意 $x$，都有

$$
\lambda_{\min}(A)x^Tx\leq x^TAx\leq\lambda_{\max}(A)x^Tx,
$$

并且，选择（不同的）$x$，两个不等式都可以取到等号。

如果对所有 $x\ne0$，都有 $x^TAx>0$，则称矩阵 $A\in\mathbf{S}^n$ 为正定矩阵，记为 $A\succ0$。由上面的不等式可知，$A\succ0$ 当且仅当其所有特征值都为正，即 $\lambda_{\min}(A)>0$。若 $-A$ 正定，则称 $A$ 负定，记为 $A\prec0$。我们用 $\mathbf{S}_{++}^n$ 表示 $\mathbf{S}^n$ 中所有正定矩阵的集合。

如果 $A$ 对所有 $x$ 都满足 $x^TAx\geq0$，则称 $A$ 半正定（positive semidefinite），也称非负定（nonnegative definite）。若 $-A$ 非负定，即对所有 $x$ 都有 $x^TAx\leq0$，则称 $A$ 半负定（negative semidefinite），也称非正定（nonpositive definite）。我们用 $\mathbf{S}_+^n$ 表示 $\mathbf{S}^n$ 中所有非负定矩阵的集合。

对于 $A,B\in\mathbf{S}^n$，用 $A\prec B$ 表示 $B-A\succ0$，其他不等式记号依此类推。这些不等式称为矩阵不等式，或与半正定锥对应的广义不等式。

#### 对称平方根

设 $A\in\mathbf{S}_+^n$，其特征值分解为 $A=Q\mathbf{diag}(\lambda_1,\ldots,\lambda_n)Q^T$。将 $A$ 的（对称）平方根定义为

$$
A^{1/2}=Q\mathbf{diag}(\lambda_1^{1/2},\ldots,\lambda_n^{1/2})Q^T.
$$

平方根 $A^{1/2}$ 是方程 $X^2=A$ 唯一的对称半正定解。

### A.5.3 广义特征值分解

一对对称矩阵 $(A,B)\in\mathbf{S}^n\times\mathbf{S}^n$ 的广义特征值，定义为多项式 $\det(sB-A)$ 的根。

<!-- pdf-page: 662 -->

我们通常关注满足 $B\in\mathbf{S}_{++}^n$ 的矩阵对。这时，广义特征值也是 $B^{-1/2}AB^{-1/2}$ 的特征值（它们都是实数）。与标准特征值分解一样，将广义特征值按非增顺序排列，即 $\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_n$，并用 $\lambda_{\max}(A,B)$ 表示最大广义特征值。

当 $B\in\mathbf{S}_{++}^n$ 时，这对矩阵可以分解为

$$
A=V\Lambda V^T,\qquad B=VV^T,
\tag{A.11}
$$

其中 $V\in\mathbf{R}^{n\times n}$ 非奇异，$\Lambda=\mathbf{diag}(\lambda_1,\ldots,\lambda_n)$，而 $\lambda_i$ 是矩阵对 $(A,B)$ 的广义特征值。分解 (A.11) 称为广义特征值分解。

广义特征值分解与矩阵 $B^{-1/2}AB^{-1/2}$ 的标准特征值分解有关。若 $Q\Lambda Q^T$ 是 $B^{-1/2}AB^{-1/2}$ 的特征值分解，则取 $V=B^{1/2}Q$ 时，(A.11) 成立。

### A.5.4 奇异值分解

设 $A\in\mathbf{R}^{m\times n}$，且 $\mathbf{rank}\,A=r$。则 $A$ 可以分解为

$$
A=U\Sigma V^T,
\tag{A.12}
$$

其中 $U\in\mathbf{R}^{m\times r}$ 满足 $U^TU=I$，$V\in\mathbf{R}^{n\times r}$ 满足 $V^TV=I$，而 $\Sigma=\mathbf{diag}(\sigma_1,\ldots,\sigma_r)$，并有

$$
\sigma_1\geq\sigma_2\geq\cdots\geq\sigma_r>0.
$$

分解 (A.12) 称为 $A$ 的奇异值分解（singular value decomposition，SVD）。$U$ 的各列称为 $A$ 的左奇异向量，$V$ 的各列称为右奇异向量，数 $\sigma_i$ 称为奇异值。奇异值分解可以写为

$$
A=\sum_{i=1}^r\sigma_i u_i v_i^T,
$$

其中 $u_i\in\mathbf{R}^m$ 是左奇异向量，$v_i\in\mathbf{R}^n$ 是右奇异向量。

矩阵 $A$ 的奇异值分解，与（对称、非负定）矩阵 $A^TA$ 的特征值分解密切相关。利用 (A.12)，可以写成

$$
A^TA=V\Sigma^2V^T
=\begin{bmatrix}V&\tilde V\end{bmatrix}
\begin{bmatrix}\Sigma^2&0\\0&0\end{bmatrix}
\begin{bmatrix}V&\tilde V\end{bmatrix}^T,
$$

其中 $\tilde V$ 是任意使 $\begin{bmatrix}V&\tilde V\end{bmatrix}$ 为正交矩阵的矩阵。右侧表达式就是 $A^TA$ 的特征值分解，因此可知，它的非零特征值是 $A$ 的各奇异值的平方，而 $A^TA$ 对应的特征向量就是 $A$ 的右奇异向量。对 $AA^T$ 作类似分析可知，它的非零<!-- pdf-page: 663 -->特征值也等于 $A$ 的各奇异值的平方，对应的特征向量则是 $A$ 的左奇异向量。

第一个、也就是最大的奇异值还记为 $\sigma_{\max}(A)$。它可以表示为

$$
\sigma_{\max}(A)=\sup_{x,y\ne0}\frac{x^TAy}{\|x\|_2\|y\|_2}
=\sup_{y\ne0}\frac{\|Ay\|_2}{\|y\|_2}.
$$

右侧表达式表明，最大奇异值就是 $A$ 的 $\ell_2$ 算子范数。$A\in\mathbf{R}^{m\times n}$ 的最小奇异值为

$$
\sigma_{\min}(A)=
\begin{cases}
\sigma_r(A)&r=\min\{m,n\}\\
0&r<\min\{m,n\},
\end{cases}
$$

它为正，当且仅当 $A$ 满秩。

对称矩阵的奇异值，是将其所有非零特征值的绝对值按降序排列得到的。对称半正定矩阵的奇异值与其非零特征值相同。

非奇异矩阵 $A\in\mathbf{R}^{n\times n}$ 的条件数记为 $\mathbf{cond}(A)$ 或 $\kappa(A)$，定义为

$$
\mathbf{cond}(A)=\|A\|_2\|A^{-1}\|_2
=\sigma_{\max}(A)/\sigma_{\min}(A).
$$

#### 伪逆

设 $A=U\Sigma V^T$ 是 $A\in\mathbf{R}^{m\times n}$ 的奇异值分解，且 $\mathbf{rank}\,A=r$。将 $A$ 的伪逆（pseudo-inverse），或 Moore–Penrose 逆，定义为

$$
A^\dagger=V\Sigma^{-1}U^T\in\mathbf{R}^{n\times m}.
$$

它还有如下表达式：

$$
A^\dagger=\lim_{\epsilon\to0}(A^TA+\epsilon I)^{-1}A^T
=\lim_{\epsilon\to0}A^T(AA^T+\epsilon I)^{-1},
$$

其中极限从 $\epsilon>0$ 一侧取，这保证表达式中的逆矩阵存在。如果 $\mathbf{rank}\,A=n$，那么 $A^\dagger=(A^TA)^{-1}A^T$。如果 $\mathbf{rank}\,A=m$，那么 $A^\dagger=A^T(AA^T)^{-1}$。如果 $A$ 是非奇异方阵，那么 $A^\dagger=A^{-1}$。

伪逆出现在最小二乘、最小范数、二次最小化以及（欧几里得）投影等问题中。例如，一般而言，$A^\dagger b$ 是最小二乘问题

$$
\text{最小化}\quad\|Ax-b\|_2^2
$$

的一个解。当解不唯一时，$A^\dagger b$ 给出具有最小（欧几里得）范数的解。再如，矩阵 $AA^\dagger=UU^T$ 给出了到 $\mathcal{R}(A)$ 上的（欧几里得）投影，矩阵 $A^\dagger A=VV^T$ 给出了到 $\mathcal{R}(A^T)$ 上的（欧几里得）投影。

对于（一般的、非凸的）二次优化问题

$$
\text{最小化}\quad(1/2)x^TPx+q^Tx+r,
$$

其中 $P\in\mathbf{S}^n$，其最优值 $p^\star$ 可以表示为

$$
p^\star=
\begin{cases}
-(1/2)q^TP^\dagger q+r&P\succeq0,\quad q\in\mathcal{R}(P)\\
-\infty&\text{其他情形。}
\end{cases}
$$

（这是在 $P\succ0$ 时成立的表达式 $p^\star=-(1/2)q^TP^{-1}q+r$ 的推广。）

<!-- pdf-page: 664 -->

### A.5.5 Schur 补

考虑矩阵 $X\in\mathbf{S}^n$，将其分块为

$$
X=\begin{bmatrix}A&B\\B^T&C\end{bmatrix},
$$

其中 $A\in\mathbf{S}^k$。若 $\det A\ne0$，则矩阵

$$
S=C-B^TA^{-1}B
$$

称为 $X$ 中关于 $A$ 的 Schur 补。Schur 补出现在多种情形中，也出现在许多重要的公式和定理中。例如，有

$$
\det X=\det A\det S.
$$

#### 分块矩阵的逆

求解线性方程组时，消去一组分块变量，就会遇到 Schur 补。从方程组

$$
\begin{bmatrix}A&B\\B^T&C\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
=\begin{bmatrix}u\\v\end{bmatrix}
$$

出发，假设 $\det A\ne0$。如果从上面的分块方程中消去 $x$，再代入下面的分块方程，就得到 $v=B^TA^{-1}u+Sy$，因此

$$
y=S^{-1}(v-B^TA^{-1}u).
$$

将其代回第一个方程，得到

$$
x=\bigl(A^{-1}+A^{-1}BS^{-1}B^TA^{-1}\bigr)u-A^{-1}BS^{-1}v.
$$

这两个方程可以写成分块矩阵求逆公式：

$$
\begin{bmatrix}A&B\\B^T&C\end{bmatrix}^{-1}
=
\begin{bmatrix}
A^{-1}+A^{-1}BS^{-1}B^TA^{-1}&-A^{-1}BS^{-1}\\
-S^{-1}B^TA^{-1}&S^{-1}
\end{bmatrix}.
$$

特别地，可以看出，Schur 补就是 $X$ 的逆矩阵中第 $(2,2)$ 个分块的逆。

#### 最小化与定性

对二次型中的部分变量求最小值时，也会遇到 Schur 补。设 $A\succ0$，考虑最小化问题

$$
\text{最小化}\quad u^TAu+2v^TB^Tu+v^TCv
\tag{A.13}
$$

其中变量为 $u$。其解为 $u=-A^{-1}Bv$，最优值为

$$
\inf_u
\begin{bmatrix}u\\v\end{bmatrix}^T
\begin{bmatrix}A&B\\B^T&C\end{bmatrix}
\begin{bmatrix}u\\v\end{bmatrix}
=v^TSv.
\tag{A.14}
$$

由此可以导出分块矩阵 $X$ 正定或半正定的下列刻画：

- $X\succ0$ 当且仅当 $A\succ0$ 且 $S\succ0$。
- 若 $A\succ0$，则 $X\succeq0$ 当且仅当 $S\succeq0$。

<!-- pdf-page: 665 -->

#### $A$ 奇异时的 Schur 补

关于 Schur 补的一些结论可以推广到 $A$ 奇异的情形，只是细节更复杂。例如，若 $A\succeq0$ 且 $Bv\in\mathcal{R}(A)$，那么以 $u$ 为变量的二次最小化问题 (A.13) 有最优解，且最优值为

$$
v^T(C-B^TA^\dagger B)v,
$$

其中 $A^\dagger$ 是 $A$ 的伪逆。如果 $Bv\notin\mathcal{R}(A)$，或者 $A\not\succeq0$，则该问题无界。

值域条件 $Bv\in\mathcal{R}(A)$ 也可以写为 $(I-AA^\dagger)Bv=0$，因此得到分块矩阵 $X$ 半正定的如下刻画：

$$
X\succeq0
\quad\Longleftrightarrow\quad
A\succeq0,\quad
(I-AA^\dagger)B=0,\quad
C-B^TA^\dagger B\succeq0.
$$

这里，在 $A$ 奇异时，矩阵 $C-B^TA^\dagger B$ 起到广义 Schur 补的作用。

<!-- pdf-page: 666 -->

## 文献说明

本附录内容的一些基础参考书包括：分析方面的 Rudin [Rud76]，以及线性代数方面的 Strang [Str80] 和 Meyer [Mey00]。较高阶的线性代数教材有 Horn 与 Johnson [HJ85, HJ91]、Parlett [Par98]、Golub 与 Van Loan [GL89]、Trefethen 与 Bau [TB97]，以及 Demmel [Dem97]。

闭函数（§A.3.3）的概念在凸优化中经常出现，尽管所用术语不尽相同。Rockafellar [Roc70，第 51 页]、Hiriart-Urruty 与 Lemaréchal [HUL93，第 1 卷，第 149 页]、Borwein 与 Lewis [BL00，第 76 页]，以及 Bertsekas、Nedić 与 Ozdaglar [Ber03，第 28 页] 都使用了这个术语。
