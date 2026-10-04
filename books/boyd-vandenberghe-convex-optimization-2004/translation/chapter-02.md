# 第 2 章 凸集

<aside class="chapter-guide">导读（编者）：凸集的关键性质是：任意两点之间的整条线段都留在集合内。本章从仿射组合、凸组合和锥出发，介绍常用凸集以及保持凸性的运算，再用广义不等式、分离超平面和对偶锥描述集合之间的关系。这些工具既用于证明集合是凸的，也为后续建立凸优化模型打下基础。</aside>

<!-- pdf-page: 35 -->

## 2.1 仿射集与凸集

### 2.1.1 直线与线段

设 $x_1\ne x_2$ 是 $\mathbf{R}^n$ 中的两个点。形如

$$
y=\theta x_1+(1-\theta)x_2,
$$

其中 $\theta\in\mathbf{R}$ 的点，构成经过 $x_1$ 和 $x_2$ 的直线。参数值 $\theta=0$ 对应于 $y=x_2$，参数值 $\theta=1$ 对应于 $y=x_1$。参数 $\theta$ 在 0 与 1 之间的取值，对应于 $x_1$ 与 $x_2$ 之间的闭线段。

把 $y$ 写成

$$
y=x_2+\theta(x_1-x_2)
$$

可以得到另一种解释：$y$ 是**基点** $x_2$（对应于 $\theta=0$）与方向 $x_1-x_2$ 乘以参数 $\theta$ 后的和，其中这个方向由 $x_2$ 指向 $x_1$。因此，$\theta$ 表示从 $x_2$ 到 $x_1$ 的路程中，$y$ 所处位置对应的比例。当 $\theta$ 从 0 增大到 1 时，点 $y$ 从 $x_2$ 移到 $x_1$；当 $\theta>1$ 时，点 $y$ 位于这条直线上越过 $x_1$ 的位置。图 2.1 对此作了说明。

### 2.1.2 仿射集

如果集合 $C\subseteq\mathbf{R}^n$ 中任意两个不同点所在的直线都包含在 $C$ 内，就称 $C$ 是**仿射集**（affine set）。也就是说，对于任意 $x_1,x_2\in C$ 和 $\theta\in\mathbf{R}$，都有 $\theta x_1+(1-\theta)x_2\in C$。换言之，只要线性组合的系数之和为 1，$C$ 就包含其中任意两点的线性组合。

这个概念可以推广到两个以上的点。我们把形如 $\theta_1x_1+\cdots+\theta_kx_k$、其中 $\theta_1+\cdots+\theta_k=1$ 的点，称为点 $x_1,\ldots,x_k$ 的**仿射组合**（affine combination）。从仿射集的定义出发，即仿射集包含其中任意两点的所有仿射组合，可以用归纳法证明，仿射集包含其中各点的任意仿射组合：<!-- pdf-page: 36 -->如果 $C$ 是仿射集，$x_1,\ldots,x_k\in C$，并且 $\theta_1+\cdots+\theta_k=1$，那么点 $\theta_1x_1+\cdots+\theta_kx_k$ 也属于 $C$。

<figure id="fig-2-1" data-figure="2.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-1.png" alt="通过两点的直线，标有不同参数值对应的位置，连接两点的线段用深色表示" data-source-page="36" data-source-rect="210,118,458,241">
<figcaption>图 2.1 通过 $x_1$ 和 $x_2$ 的直线可用参数形式 $\theta x_1+(1-\theta)x_2$ 表示，其中 $\theta$ 遍历 $\mathbf{R}$。$x_1$ 与 $x_2$ 之间的线段对应于 $\theta$ 在 $0$ 和 $1$ 之间的取值，图中用较深的线条表示。</figcaption>
</figure>

如果 $C$ 是仿射集且 $x_0\in C$，那么集合

$$
V=C-x_0=\{x-x_0\mid x\in C\}
$$

是一个子空间，也就是说，它对加法和数乘封闭。为说明这一点，设 $v_1,v_2\in V$，$\alpha,\beta\in\mathbf{R}$。于是 $v_1+x_0\in C$、$v_2+x_0\in C$，因此

$$
\alpha v_1+\beta v_2+x_0=\alpha(v_1+x_0)+\beta(v_2+x_0)+(1-\alpha-\beta)x_0\in C,
$$

因为 $C$ 是仿射集，且 $\alpha+\beta+(1-\alpha-\beta)=1$。由 $\alpha v_1+\beta v_2+x_0\in C$，可得 $\alpha v_1+\beta v_2\in V$。

所以仿射集 $C$ 可以表示为

$$
C=V+x_0=\{v+x_0\mid v\in V\},
$$

即一个子空间加上一个偏移量。仿射集 $C$ 对应的子空间 $V$ 不依赖于 $x_0$ 的选择，因此 $x_0$ 可以取为 $C$ 中任意一点。我们把仿射集 $C$ 的**维数**定义为子空间 $V=C-x_0$ 的维数，其中 $x_0$ 是 $C$ 的任意元素。

<div class="example" markdown="1">

**例 2.1 线性方程组的解集。** 线性方程组的解集 $C=\{x\mid Ax=b\}$ 是仿射集，其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$。为证明这一点，设 $x_1,x_2\in C$，即 $Ax_1=b$、$Ax_2=b$。于是对任意 $\theta$，都有

$$
\begin{aligned}
A(\theta x_1+(1-\theta)x_2)&=\theta Ax_1+(1-\theta)Ax_2\\
&=\theta b+(1-\theta)b\\
&=b,
\end{aligned}
$$

这说明仿射组合 $\theta x_1+(1-\theta)x_2$ 也属于 $C$。仿射集 $C$ 对应的子空间是 $A$ 的零空间。

反过来也成立：每个仿射集都可以表示为某个线性方程组的解集。

</div>

<!-- pdf-page: 37 -->

集合 $C\subseteq\mathbf{R}^n$ 中各点的所有仿射组合构成的集合，称为 $C$ 的**仿射包**（affine hull），记作 $\operatorname{\mathbf{aff}}C$：

$$
\operatorname{\mathbf{aff}}C=\{\theta_1x_1+\cdots+\theta_kx_k\mid x_1,\ldots,x_k\in C,\ \theta_1+\cdots+\theta_k=1\}.
$$

仿射包是包含 $C$ 的最小仿射集，具体含义是：如果 $S$ 是任意满足 $C\subseteq S$ 的仿射集，那么 $\operatorname{\mathbf{aff}}C\subseteq S$。

### 2.1.3 仿射维数与相对内部

集合 $C$ 的**仿射维数**（affine dimension）定义为其仿射包的维数。仿射维数在凸分析和优化中很有用，但它并不总与其他维数定义一致。例如，考虑 $\mathbf{R}^2$ 中的单位圆，即 $\{x\in\mathbf{R}^2\mid x_1^2+x_2^2=1\}$。它的仿射包是整个 $\mathbf{R}^2$，所以仿射维数是 2。但按多数维数定义，$\mathbf{R}^2$ 中单位圆的维数是 1。

如果集合 $C\subseteq\mathbf{R}^n$ 的仿射维数小于 $n$，那么该集合包含在仿射集 $\operatorname{\mathbf{aff}}C\ne\mathbf{R}^n$ 中。我们把集合 $C$ 相对于 $\operatorname{\mathbf{aff}}C$ 的内部定义为它的**相对内部**（relative interior），记为 $\operatorname{\mathbf{relint}}C$：

$$
\operatorname{\mathbf{relint}}C=\{x\in C\mid \text{存在 }r>0,\ B(x,r)\cap\operatorname{\mathbf{aff}}C\subseteq C\},
$$

其中 $B(x,r)=\{y\mid\|y-x\|\leq r\}$ 是按范数 $\|\cdot\|$ 定义的、以 $x$ 为中心、半径为 $r$ 的球。（这里 $\|\cdot\|$ 可以是任意范数；所有范数定义的相对内部都相同。）由此还可以把集合 $C$ 的**相对边界**定义为 $\operatorname{\mathbf{cl}}C\setminus\operatorname{\mathbf{relint}}C$，其中 $\operatorname{\mathbf{cl}}C$ 是 $C$ 的闭包。

<div class="example" markdown="1">

**例 2.2** 考虑 $\mathbf{R}^3$ 的 $(x_1,x_2)$ 平面中的一个正方形，定义为

$$
C=\{x\in\mathbf{R}^3\mid -1\leq x_1\leq1,\ -1\leq x_2\leq1,\ x_3=0\}.
$$

它的仿射包是 $(x_1,x_2)$ 平面，即 $\operatorname{\mathbf{aff}}C=\{x\in\mathbf{R}^3\mid x_3=0\}$。$C$ 的内部为空，但相对内部是

$$
\operatorname{\mathbf{relint}}C=\{x\in\mathbf{R}^3\mid -1<x_1<1,\ -1<x_2<1,\ x_3=0\}.
$$

它在 $\mathbf{R}^3$ 中的边界就是自身；它的相对边界则是线框轮廓，

$$
\{x\in\mathbf{R}^3\mid\max\{|x_1|,|x_2|\}=1,\ x_3=0\}.
$$

</div>

### 2.1.4 凸集

如果集合 $C$ 中任意两点之间的线段都包含在 $C$ 中，就称 $C$ 是**凸集**（convex set）。也就是说，对于任意 $x_1,x_2\in C$ 及任意满足 $0\leq\theta\leq1$ 的 $\theta$，都有

$$
\theta x_1+(1-\theta)x_2\in C.
$$

<!-- pdf-page: 38 -->

<figure id="fig-2-2" data-figure="2.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-2.png" alt="三个集合：包含边界的凸六边形、含凹陷的非凸肾形集合，以及仅包含部分边界点的非凸正方形" data-source-page="38" data-source-rect="190,119,488,193">
<figcaption>图 2.2 几个简单的凸集和非凸集。左：六边形包含其边界（用较深的线条表示），是凸集。中：肾形集合不是凸集，因为集合内两个点（用圆点表示）之间的线段并不完全包含在该集合中。右：正方形包含一些边界点，但不包含另外一些边界点，因此不是凸集。</figcaption>
</figure>

<figure id="fig-2-3" data-figure="2.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-3.png" alt="左侧十五个点的凸包为五边形；右侧肾形集合的凸包填平了凹陷" data-source-page="38" data-source-rect="218,274,460,362">
<figcaption>图 2.3 $\mathbf{R}^2$ 中两个集合的凸包。左：由十五个点（用圆点表示）组成的集合，其凸包是五边形（阴影区域）。右：<a href="#fig-2-2">图 2.2</a> 中肾形集合的凸包是阴影所示的集合。</figcaption>
</figure>

粗略地说，如果集合中每一点都能沿着一条没有阻挡的直线路径“看到”其他每一点，那么这个集合就是凸的；这里“没有阻挡”是指整条路径都位于集合内。每个仿射集也都是凸集，因为它包含经过其中任意两个不同点的整条直线，因此也包含这两点之间的线段。图 2.2 展示了 $\mathbf{R}^2$ 中一些简单的凸集和非凸集。

形如 $\theta_1x_1+\cdots+\theta_kx_k$、其中 $\theta_1+\cdots+\theta_k=1$ 且 $\theta_i\geq0$（$i=1,\ldots,k$）的点，称为 $x_1,\ldots,x_k$ 的**凸组合**（convex combination）。与仿射集类似，可以证明，一个集合是凸集，当且仅当它包含其中各点的所有凸组合。各点的凸组合可以看作这些点的混合或加权平均，其中 $\theta_i$ 是混合中 $x_i$ 所占的比例。

集合 $C$ 的**凸包**（convex hull），记为 $\operatorname{\mathbf{conv}}C$，是 $C$ 中各点的所有凸组合构成的集合：

$$
\operatorname{\mathbf{conv}}C=\{\theta_1x_1+\cdots+\theta_kx_k\mid x_i\in C,\ \theta_i\geq0,\ i=1,\ldots,k,\ \theta_1+\cdots+\theta_k=1\}.
$$

顾名思义，凸包 $\operatorname{\mathbf{conv}}C$ 总是凸集。它是包含 $C$ 的最小凸集：如果 $B$ 是任意包含 $C$ 的凸集，那么 $\operatorname{\mathbf{conv}}C\subseteq B$。图 2.3 说明了凸包的定义。

凸组合的概念可以推广到无穷和、积分，以及最一般形式的概率分布。设 $\theta_1,\theta_2,\ldots$<!-- pdf-page: 39 -->满足

$$
\theta_i\geq0,\quad i=1,2,\ldots,\qquad\sum_{i=1}^{\infty}\theta_i=1,
$$

并且 $x_1,x_2,\ldots\in C$，其中 $C\subseteq\mathbf{R}^n$ 是凸集。那么，只要级数收敛，就有

$$
\sum_{i=1}^{\infty}\theta_i x_i\in C.
$$

更一般地，设 $p:\mathbf{R}^n\to\mathbf{R}$ 对所有 $x\in C$ 都满足 $p(x)\geq0$，且 $\int_Cp(x)\,dx=1$，其中 $C\subseteq\mathbf{R}^n$ 是凸集。那么，只要积分存在，就有

$$
\int_Cp(x)x\,dx\in C.
$$

在最一般的形式下，设 $C\subseteq\mathbf{R}^n$ 是凸集，$x$ 是随机向量，并且 $x\in C$ 的概率为 1。那么 $\mathbf{E}x\in C$。实际上，这一形式把前面的其他形式都包含为特殊情况。例如，设随机变量 $x$ 只取 $x_1$ 和 $x_2$ 两个值，且 $\operatorname{\mathbf{prob}}(x=x_1)=\theta$、$\operatorname{\mathbf{prob}}(x=x_2)=1-\theta$，其中 $0\leq\theta\leq1$。于是 $\mathbf{E}x=\theta x_1+(1-\theta)x_2$，便回到了两点的简单凸组合。

### 2.1.5 锥

如果对每个 $x\in C$ 和 $\theta\geq0$ 都有 $\theta x\in C$，就称集合 $C$ 是一个**锥**（cone），或称它具有**非负齐次性**（nonnegative homogeneous）。如果集合 $C$ 既是凸集又是锥，就称它是**凸锥**（convex cone）；这意味着，对于任意 $x_1,x_2\in C$ 和 $\theta_1,\theta_2\geq0$，都有

$$
\theta_1x_1+\theta_2x_2\in C.
$$

从几何上看，这种形式的点构成一个二维扇形区域，其顶点为 0，两条边分别经过 $x_1$ 和 $x_2$，见图 2.4。

形如 $\theta_1x_1+\cdots+\theta_kx_k$、其中 $\theta_1,\ldots,\theta_k\geq0$ 的点，称为 $x_1,\ldots,x_k$ 的**锥组合**（conic combination），或**非负线性组合**。如果各个 $x_i$ 都属于凸锥 $C$，那么它们的每个锥组合也属于 $C$。反过来，集合 $C$ 是凸锥，当且仅当它包含其元素的所有锥组合。与凸组合或仿射组合一样，锥组合的概念也可以推广到无穷和及积分。

集合 $C$ 的**锥包**（conic hull）是 $C$ 中各点的所有锥组合构成的集合，即

$$
\{\theta_1x_1+\cdots+\theta_kx_k\mid x_i\in C,\ \theta_i\geq0,\ i=1,\ldots,k\},
$$

它也是包含 $C$ 的最小凸锥，见图 2.5。

<!-- pdf-page: 40 -->

<figure id="fig-2-4" data-figure="2.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-4.png" alt="以原点为顶点、两边分别经过两给定点的扇形锥" data-source-page="40" data-source-rect="240,173,435,301">
<figcaption>图 2.4 扇形区域表示所有形如 $\theta_1x_1+\theta_2x_2$ 的点，其中 $\theta_1,\theta_2\geq 0$。扇形的顶点位于 $0$，对应于 $\theta_1=\theta_2=0$；它的两条边分别对应于 $\theta_1=0$ 或 $\theta_2=0$，并经过点 $x_1$ 和 $x_2$。</figcaption>
</figure>

<figure id="fig-2-5" data-figure="2.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-5.png" alt="十五个点组成的集合与肾形集合各自的锥包，锥的顶点均位于原点" data-source-page="40" data-source-rect="200,462,480,614">
<figcaption>图 2.5 <a href="#fig-2-3">图 2.3</a> 中两个集合的锥包，用阴影表示。</figcaption>
</figure>

<!-- pdf-page: 41 -->

## 2.2 一些重要例子

本节介绍一些重要的凸集例子，本书后续部分会反复遇到它们。先从几个简单例子开始。

- 空集 $\varnothing$、任意单个点构成的集合（即单点集）$\{x_0\}$，以及整个空间 $\mathbf{R}^n$，都是 $\mathbf{R}^n$ 的仿射子集，因此也都是凸集。
- 任何直线都是仿射集。如果它经过零点，就是一个子空间，因此也是凸锥。
- 线段是凸集，但不是仿射集，除非它退化成一个点。
- **射线**具有形式 $\{x_0+\theta v\mid\theta\geq0\}$，其中 $v\ne0$。射线是凸集，但不是仿射集。如果其起点 $x_0$ 为 0，它就是凸锥。
- 任意子空间都是仿射集，也是凸锥，因此是凸集。

### 2.2.1 超平面与半空间

**超平面**（hyperplane）是形如下式的集合：

$$
\{x\mid a^Tx=b\},
$$

其中 $a\in\mathbf{R}^n$、$a\ne0$，$b\in\mathbf{R}$。从解析角度看，它是关于 $x$ 各分量的一个非平凡线性方程的解集，因此是仿射集。从几何角度看，超平面 $\{x\mid a^Tx=b\}$ 可以解释为与给定向量 $a$ 的内积为某个常数的所有点，也可以解释为以 $a$ 为法向量的超平面；常数 $b\in\mathbf{R}$ 决定超平面相对于原点的偏移。将超平面写成

$$
\{x\mid a^T(x-x_0)=0\},
$$

就能理解这种几何解释，其中 $x_0$ 是超平面中的任意一点，即任意满足 $a^Tx_0=b$ 的点。这个表示还可以写成

$$
\{x\mid a^T(x-x_0)=0\}=x_0+a^\perp,
$$

其中 $a^\perp$ 表示 $a$ 的正交补，即所有与 $a$ 正交的向量构成的集合：

$$
a^\perp=\{v\mid a^Tv=0\}.
$$

这说明，超平面由一个偏移 $x_0$ 加上所有与法向量 $a$ 正交的向量构成。图 2.6 展示了这些几何解释。

一个超平面把 $\mathbf{R}^n$ 分成两个半空间。**闭半空间**（closed halfspace）是形如下式的集合：

$$
\{x\mid a^Tx\leq b\},
\tag{2.1}
$$

其中 $a\ne0$，也就是一个非平凡线性不等式的解集。半空间是凸集，但不是仿射集，见图 2.7。

<!-- pdf-page: 42 -->

<figure id="fig-2-6" data-figure="2.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-6.png" alt="二维超平面、其法向量以及平面内两点的差向量" data-source-page="42" data-source-rect="246,161,449,275">
<figcaption>图 2.6 $\mathbf{R}^2$ 中的一个超平面，法向量为 $a$，$x_0$ 是超平面上的一点。对于超平面上的任意点 $x$，向量 $x-x_0$（图中较深的箭头）都与 $a$ 正交。</figcaption>
</figure>

<figure id="fig-2-7" data-figure="2.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-7.png" alt="超平面分出的两个半空间，以及指向非阴影一侧的法向量" data-source-page="42" data-source-rect="246,415,436,572">
<figcaption>图 2.7 在 $\mathbf{R}^2$ 中，由 $a^Tx=b$ 定义的超平面确定了两个半空间。由 $a^Tx\geq b$ 确定的半空间（未加阴影）向 $a$ 的方向延伸。由 $a^Tx\leq b$ 确定的半空间（用阴影表示）向 $-a$ 的方向延伸。向量 $a$ 是这个半空间的外法向量。</figcaption>
</figure>

<!-- pdf-page: 43 -->

<figure id="fig-2-8" data-figure="2.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-8.png" alt="一个点位于阴影半空间外，另一个点位于半空间内，其差向量分别与外法向量成锐角和钝角" data-source-page="43" data-source-rect="191,119,379,307">
<figcaption>图 2.8 阴影集合是由 $a^T(x-x_0)\leq 0$ 确定的半空间。向量 $x_1-x_0$ 与 $a$ 成锐角，因此 $x_1$ 不在该半空间内。向量 $x_2-x_0$ 与 $a$ 成钝角，因此 $x_2$ 在该半空间内。</figcaption>
</figure>

半空间 (2.1) 也可以表示为

$$
\{x\mid a^T(x-x_0)\leq0\},
\tag{2.2}
$$

其中 $x_0$ 是对应超平面上的任意点，即满足 $a^Tx_0=b$。表示式 (2.2) 给出了一个简单的几何解释：半空间由 $x_0$ 加上所有与外法向量 $a$ 的夹角为钝角或直角的向量构成，见图 2.8。

半空间 (2.1) 的边界是超平面 $\{x\mid a^Tx=b\}$。集合 $\{x\mid a^Tx<b\}$ 是半空间 $\{x\mid a^Tx\leq b\}$ 的内部，称为**开半空间**。

### 2.2.2 欧几里得球与椭球

$\mathbf{R}^n$ 中的**欧几里得球**（Euclidean ball），或简称球，具有形式

$$
B(x_c,r)=\{x\mid\|x-x_c\|_2\leq r\}=\{x\mid(x-x_c)^T(x-x_c)\leq r^2\},
$$

其中 $r>0$，$\|\cdot\|_2$ 表示欧几里得范数，即 $\|u\|_2=(u^Tu)^{1/2}$。向量 $x_c$ 是球的中心，标量 $r$ 是它的半径；$B(x_c,r)$ 包含与中心 $x_c$ 的距离不超过 $r$ 的所有点。欧几里得球的另一种常见表示为

$$
B(x_c,r)=\{x_c+ru\mid\|u\|_2\leq1\}.
$$

<!-- pdf-page: 44 -->

<figure id="fig-2-9" data-figure="2.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-9.png" alt="阴影椭球、中心点以及两条半轴" data-source-page="44" data-source-rect="264,121,413,226">
<figcaption>图 2.9 $\mathbf{R}^2$ 中的一个椭球，用阴影表示。中心 $x_c$ 用圆点表示，两条半轴用线段表示。</figcaption>
</figure>

欧几里得球是凸集：如果 $\|x_1-x_c\|_2\leq r$、$\|x_2-x_c\|_2\leq r$，且 $0\leq\theta\leq1$，那么

$$
\begin{aligned}
\|\theta x_1+(1-\theta)x_2-x_c\|_2
&=\|\theta(x_1-x_c)+(1-\theta)(x_2-x_c)\|_2\\
&\leq\theta\|x_1-x_c\|_2+(1-\theta)\|x_2-x_c\|_2\\
&\leq r.
\end{aligned}
$$

（这里使用了 $\|\cdot\|_2$ 的齐次性和三角不等式，见第 A.1.2 节。）

与球相关的一族凸集是**椭球**（ellipsoid），其形式为

$$
\mathcal{E}=\{x\mid(x-x_c)^TP^{-1}(x-x_c)\leq1\},
\tag{2.3}
$$

其中 $P=P^T\succ0$，即 $P$ 是对称正定矩阵。向量 $x_c\in\mathbf{R}^n$ 是椭球的中心。矩阵 $P$ 决定椭球从 $x_c$ 沿各个方向延伸多远；$\mathcal{E}$ 的各半轴长度为 $\sqrt{\lambda_i}$，其中 $\lambda_i$ 是 $P$ 的特征值。球是 $P=r^2I$ 时的椭球。图 2.9 展示了 $\mathbf{R}^2$ 中的一个椭球。

椭球的另一种常见表示为

$$
\mathcal{E}=\{x_c+Au\mid\|u\|_2\leq1\},
\tag{2.4}
$$

其中 $A$ 是非奇异方阵。在这个表示中，可以不失一般性地假设 $A$ 对称且正定。取 $A=P^{1/2}$，就得到 (2.3) 中定义的椭球。如果 (2.4) 中的矩阵 $A$ 对称半正定但奇异，那么 (2.4) 中的集合称为**退化椭球**（degenerate ellipsoid）；它的仿射维数等于 $A$ 的秩。退化椭球也是凸集。

### 2.2.3 范数球与范数锥

设 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的任意范数，见第 A.1.2 节。根据范数的一般性质，可以证明以 $x_c$ 为中心、半径为 $r$ 的**范数球** $\{x\mid\|x-x_c\|\leq r\}$ 是凸集。与范数 $\|\cdot\|$ 对应的**范数锥**（norm cone）是集合

$$
C=\{(x,t)\mid\|x\|\leq t\}\subseteq\mathbf{R}^{n+1}.
$$

<!-- pdf-page: 45 -->

<figure id="fig-2-10" data-figure="2.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-10.png" alt="三维二阶锥的边界曲面，坐标轴为两空间分量与锥高度" data-source-page="45" data-source-rect="145,131,411,320">
<figcaption>图 2.10 $\mathbf{R}^3$ 中二阶锥 $\{(x_1,x_2,t)\mid (x_1^2+x_2^2)^{1/2}\leq t\}$ 的边界。</figcaption>
</figure>

顾名思义，它是一个凸锥。

<div class="example" markdown="1">

**例 2.3** **二阶锥**（second-order cone）是欧几里得范数所对应的范数锥，即

$$
\begin{aligned}
C&=\{(x,t)\in\mathbf{R}^{n+1}\mid\|x\|_2\leq t\}\\
&=\left\{\begin{bmatrix}x\\t\end{bmatrix}\ \middle|\ \begin{bmatrix}x\\t\end{bmatrix}^{T}\begin{bmatrix}I&0\\0&-1\end{bmatrix}\begin{bmatrix}x\\t\end{bmatrix}\leq0,\ t\geq0\right\}.
\end{aligned}
$$

二阶锥还有几个别名。由于它由一个二次不等式定义，也称为**二次锥**（quadratic cone）。它还称为 **Lorentz 锥**或**冰淇淋锥**（ice-cream cone）。图 2.10 展示了 $\mathbf{R}^3$ 中的二阶锥。

</div>

### 2.2.4 多面体

**多面体**（polyhedron）定义为有限个线性等式和线性不等式的解集：

$$
\mathcal{P}=\{x\mid a_j^Tx\leq b_j,\ j=1,\ldots,m,\ c_j^Tx=d_j,\ j=1,\ldots,p\}.
\tag{2.5}
$$

因此，多面体是有限个半空间和超平面的交集。仿射集（例如子空间、超平面、直线）、射线、线段和半空间都是多面体。容易证明，多面体是凸集。有界多面体有时称为**多胞体**（polytope），但有些作者采用相反约定，即把任何形如 (2.5) 的集合都称为 polytope，<!-- pdf-page: 46 -->仅在它有界时称为 polyhedron。图 2.11 给出了一个由五个半空间的交集定义的多面体例子。

<figure id="fig-2-11" data-figure="2.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-11.png" alt="五个半空间相交得到的五边形多面体，各边标出外法向量" data-source-page="46" data-source-rect="237,115,435,289">
<figcaption>图 2.11 多面体 $\mathcal{P}$（阴影区域）是五个半空间的交，这些半空间的外法向量分别为 $a_1,\ldots,a_5$。</figcaption>
</figure>

把 (2.5) 写成紧凑形式会很方便：

$$
\mathcal{P}=\{x\mid Ax\preceq b,\ Cx=d\},
\tag{2.6}
$$

其中

$$
A=\begin{bmatrix}a_1^T\\\vdots\\a_m^T\end{bmatrix},\qquad
C=\begin{bmatrix}c_1^T\\\vdots\\c_p^T\end{bmatrix},
$$

符号 $\preceq$ 表示 $\mathbf{R}^m$ 中的**向量不等式**，或**逐分量不等式**：$u\preceq v$ 表示对 $i=1,\ldots,m$ 都有 $u_i\leq v_i$。

<div class="example" markdown="1">

**例 2.4** **非负正交象限**（nonnegative orthant）由所有分量非负的点构成，即

$$
\mathbf{R}_+^n=\{x\in\mathbf{R}^n\mid x_i\geq0,\ i=1,\ldots,n\}=\{x\in\mathbf{R}^n\mid x\succeq0\}.
$$

（这里 $\mathbf{R}_+$ 表示非负数集：$\mathbf{R}_+=\{x\in\mathbf{R}\mid x\geq0\}$。）非负正交象限既是多面体，又是锥，因此称为**多面锥**（polyhedral cone）。

</div>

#### 单纯形

**单纯形**（simplex）是另一类重要的多面体。设 $k+1$ 个点 $v_0,\ldots,v_k\in\mathbf{R}^n$ **仿射无关**（affinely independent），即 $v_1-v_0,\ldots,v_k-v_0$ 线性无关。它们所确定的单纯形为

$$
C=\operatorname{\mathbf{conv}}\{v_0,\ldots,v_k\}=\{\theta_0v_0+\cdots+\theta_kv_k\mid\theta\succeq0,\ \mathbf{1}^T\theta=1\},
\tag{2.7}
$$

<!-- pdf-page: 47 -->

其中 $\mathbf{1}$ 表示所有元素均为 1 的向量。这个单纯形的仿射维数是 $k$，因此有时称为 $\mathbf{R}^n$ 中的 $k$ 维单纯形。

<div class="example" markdown="1">

**例 2.5 一些常见单纯形。** 一维单纯形是线段；二维单纯形是三角形，包括它的内部；三维单纯形是四面体。

**单位单纯形**是由零向量和各单位向量，即 $0,e_1,\ldots,e_n\in\mathbf{R}^n$，确定的 $n$ 维单纯形。它可以表示为满足以下条件的向量集合：

$$
x\succeq0,\qquad\mathbf{1}^Tx\leq1.
$$

**概率单纯形**是由单位向量 $e_1,\ldots,e_n\in\mathbf{R}^n$ 确定的 $(n-1)$ 维单纯形。它是满足以下条件的向量集合：

$$
x\succeq0,\qquad\mathbf{1}^Tx=1.
$$

概率单纯形中的向量，对应于一个含有 $n$ 个元素的集合上的概率分布，其中 $x_i$ 解释为第 $i$ 个元素的概率。

</div>

要把单纯形 (2.7) 描述为多面体，即写成 (2.6) 的形式，可以按下述步骤进行。根据定义，$x\in C$ 当且仅当存在满足 $\theta\succeq0$、$\mathbf{1}^T\theta=1$ 的 $\theta$，使得 $x=\theta_0v_0+\theta_1v_1+\cdots+\theta_kv_k$。等价地，如果定义 $y=(\theta_1,\ldots,\theta_k)$，并令

$$
B=\begin{bmatrix}v_1-v_0&\cdots&v_k-v_0\end{bmatrix}\in\mathbf{R}^{n\times k},
$$

那么 $x\in C$ 当且仅当存在满足 $y\succeq0$、$\mathbf{1}^Ty\leq1$ 的 $y$，使得

$$
x=v_0+By.
\tag{2.8}
$$

现在注意，点 $v_0,\ldots,v_k$ 仿射无关，意味着矩阵 $B$ 的秩为 $k$。因此，存在非奇异矩阵 $A=(A_1,A_2)\in\mathbf{R}^{n\times n}$，使得

$$
AB=\begin{bmatrix}A_1\\A_2\end{bmatrix}B=\begin{bmatrix}I\\0\end{bmatrix}.
$$

在 (2.8) 两边左乘 $A$，得到

$$
A_1x=A_1v_0+y,\qquad A_2x=A_2v_0.
$$

由此可见，$x\in C$ 当且仅当 $A_2x=A_2v_0$，并且向量 $y=A_1x-A_1v_0$ 满足 $y\succeq0$ 和 $\mathbf{1}^Ty\leq1$。换句话说，$x\in C$ 当且仅当

$$
A_2x=A_2v_0,\qquad A_1x\succeq A_1v_0,\qquad\mathbf{1}^TA_1x\leq1+\mathbf{1}^TA_1v_0,
$$

这些是关于 $x$ 的一组线性等式和不等式，因此描述了一个多面体。

<!-- pdf-page: 48 -->

#### 多面体的凸包描述

有限集合 $\{v_1,\ldots,v_k\}$ 的凸包为

$$
\operatorname{\mathbf{conv}}\{v_1,\ldots,v_k\}=\{\theta_1v_1+\cdots+\theta_kv_k\mid\theta\succeq0,\ \mathbf{1}^T\theta=1\}.
$$

这个集合是有界多面体，但除单纯形等特殊情况外，要把它写成 (2.5) 的形式，即用一组线性等式和不等式来表示，并不容易。

这种凸包描述的一种推广是

$$
\{\theta_1v_1+\cdots+\theta_kv_k\mid\theta_1+\cdots+\theta_m=1,\ \theta_i\geq0,\ i=1,\ldots,k\},
\tag{2.9}
$$

其中 $m\leq k$。这里考虑 $v_i$ 的非负线性组合，但只要求前 $m$ 个系数之和为 1。也可以把 (2.9) 解释为点 $v_1,\ldots,v_m$ 的凸包，加上点 $v_{m+1},\ldots,v_k$ 的锥包。集合 (2.9) 定义了一个多面体；反过来，每个多面体都可以用这种形式表示，不过这里不作证明。

多面体采用哪种表示是一个微妙的问题，在实践中具有非常重要的影响。作为简单例子，考虑 $\mathbf{R}^n$ 中的 $\ell_\infty$ 范数单位球：

$$
C=\{x\mid|x_i|\leq1,\ i=1,\ldots,n\}.
$$

集合 $C$ 可以用 $2n$ 个线性不等式 $\pm e_i^Tx\leq1$ 写成 (2.5) 的形式，其中 $e_i$ 是第 $i$ 个单位向量。若要用凸包形式 (2.9) 描述它，则至少需要 $2^n$ 个点：

$$
C=\operatorname{\mathbf{conv}}\{v_1,\ldots,v_{2^n}\},
$$

其中 $v_1,\ldots,v_{2^n}$ 是所有分量均为 1 或 $-1$ 的 $2^n$ 个向量。因此，当 $n$ 很大时，这两种描述的规模相差悬殊。

### 2.2.5 半正定锥

我们用 $\mathbf{S}^n$ 表示对称 $n\times n$ 矩阵的集合：

$$
\mathbf{S}^n=\{X\in\mathbf{R}^{n\times n}\mid X=X^T\},
$$

它是维数为 $n(n+1)/2$ 的向量空间。用 $\mathbf{S}_+^n$ 表示对称半正定矩阵的集合：

$$
\mathbf{S}_+^n=\{X\in\mathbf{S}^n\mid X\succeq0\},
$$

用 $\mathbf{S}_{++}^n$ 表示对称正定矩阵的集合：

$$
\mathbf{S}_{++}^n=\{X\in\mathbf{S}^n\mid X\succ0\}.
$$

（这些记号是对表示非负实数的 $\mathbf{R}_+$、表示正实数的 $\mathbf{R}_{++}$ 的类比。）

<!-- pdf-page: 49 -->

<figure id="fig-2-12" data-figure="2.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-12.png" alt="二阶对称矩阵空间中半正定锥的边界，以矩阵三个独立元素为坐标" data-source-page="49" data-source-rect="144,122,412,317">
<figcaption>图 2.12 $\mathbf{S}^2$ 中半正定锥的边界。</figcaption>
</figure>

集合 $\mathbf{S}_+^n$ 是凸锥：如果 $\theta_1,\theta_2\geq0$ 且 $A,B\in\mathbf{S}_+^n$，那么 $\theta_1A+\theta_2B\in\mathbf{S}_+^n$。这可以直接从半正定性的定义看出：对于任意 $x\in\mathbf{R}^n$，如果 $A\succeq0$、$B\succeq0$ 且 $\theta_1,\theta_2\geq0$，那么

$$
x^T(\theta_1A+\theta_2B)x=\theta_1x^TAx+\theta_2x^TBx\geq0.
$$

<div class="example" markdown="1">

**例 2.6 $\mathbf{S}^2$ 中的半正定锥。** 有

$$
X=\begin{bmatrix}x&y\\y&z\end{bmatrix}\in\mathbf{S}_+^2
\quad\Longleftrightarrow\quad x\geq0,\ z\geq0,\ xz\geq y^2.
$$

图 2.12 给出了这个锥的边界，以 $(x,y,z)$ 为坐标画在 $\mathbf{R}^3$ 中。

</div>

## 2.3 保持凸性的运算

本节介绍一些保持集合凸性的运算，也就是从已有凸集构造新凸集的方法。这些运算与第 2.2 节的简单例子共同构成了一套凸集运算规则，可用于判断或证明集合的凸性。

<!-- pdf-page: 50 -->

### 2.3.1 交集

取交集保持凸性：如果 $S_1$ 和 $S_2$ 都是凸集，那么 $S_1\cap S_2$ 也是凸集。这一性质可以推广到无穷多个集合的交集：如果对每个 $\alpha\in\mathcal{A}$，$S_\alpha$ 都是凸集，那么 $\bigcap_{\alpha\in\mathcal{A}}S_\alpha$ 是凸集。（子空间、仿射集和凸锥也都对任意交集运算封闭。）一个简单例子是，多面体是半空间和超平面的交集，而后两者都是凸集，因此多面体是凸集。

<div class="example" markdown="1">

**例 2.7** 半正定锥 $\mathbf{S}_+^n$ 可以表示为

$$
\bigcap_{z\ne0}\{X\in\mathbf{S}^n\mid z^TXz\geq0\}.
$$

对每个 $z\ne0$，$z^TXz$ 都是 $X$ 的一个不恒为零的线性函数，所以集合

$$
\{X\in\mathbf{S}^n\mid z^TXz\geq0\}
$$

实际上是 $\mathbf{S}^n$ 中的半空间。因此，半正定锥是无穷多个半空间的交集，所以是凸集。

</div>

<div class="example" markdown="1">

**例 2.8** 考虑集合

$$
S=\{x\in\mathbf{R}^m\mid\text{对 }|t|\leq\pi/3\text{，有 }|p(t)|\leq1\},
\tag{2.10}
$$

其中 $p(t)=\sum_{k=1}^{m}x_k\cos kt$。集合 $S$ 可以写成无穷多个条带（slab）的交集：$S=\bigcap_{|t|\leq\pi/3}S_t$，其中

$$
S_t=\{x\mid-1\leq(\cos t,\ldots,\cos mt)^Tx\leq1\},
$$

因此是凸集。图 2.13 和图 2.14 展示了 $m=2$ 时的定义和集合。

</div>

在上面的例子中，我们通过把集合表示为半空间的交集来证明凸性，其中半空间的数量可以是无穷的。第 2.5.1 节将说明，反过来也成立：每个闭凸集 $S$ 都是一些半空间的交集，通常需要无穷多个。实际上，闭凸集 $S$ 就是所有包含它的半空间的交集：

$$
S=\bigcap\{\mathcal{H}\mid\mathcal{H}\text{ 是半空间},\ S\subseteq\mathcal{H}\}.
$$

### 2.3.2 仿射函数

回顾一下，如果函数 $f:\mathbf{R}^n\to\mathbf{R}^m$ 是线性函数与常数之和，即具有形式 $f(x)=Ax+b$，其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，就称它是仿射函数。设 $S\subseteq\mathbf{R}^n$ 是凸集，$f:\mathbf{R}^n\to\mathbf{R}^m$ 是仿射函数。那么 $S$ 在 $f$ 下的像

$$
f(S)=\{f(x)\mid x\in S\}
$$

<!-- pdf-page: 51 -->

<figure id="fig-2-13" data-figure="2.13" data-no-english-text="true" data-reader-after="affine-image-preimage-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-13.png" alt="三个三角多项式的曲线，其中虚线是另外两条曲线的平均" data-source-page="51" data-source-rect="167,187,386,356">
<figcaption>图 2.13 当 $m=2$ 时，与 <a href="#eq-2-10">(2.10)</a> 定义的集合 $S$ 中的点对应的三个三角多项式。用虚线绘出的三角多项式是另外两个的平均。</figcaption>
</figure>

<figure id="fig-2-14" data-figure="2.14" data-no-english-text="true" data-reader-after="affine-image-preimage-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-14.png" alt="无穷多个条带的交形成中心白色凸集，图中画出其中二十个条带" data-source-page="51" data-source-rect="169,400,396,582">
<figcaption>图 2.14 当 $m=2$ 时，<a href="#eq-2-10">(2.10)</a> 定义的集合 $S$ 是图中央的白色区域。该集合是无穷多个条带的交（图中画出了其中的 20 个），因此是凸集。</figcaption>
</figure>

<!-- pdf-page: 52 -->

也是凸集。同样，如果 $f:\mathbf{R}^k\to\mathbf{R}^n$ 是仿射函数，那么 $S$ 在 $f$ 下的原像

$$
f^{-1}(S)=\{x\mid f(x)\in S\}
$$

<p id="affine-image-preimage-end">也是凸集。</p>

两个简单例子是缩放和平移。如果 $S\subseteq\mathbf{R}^n$ 是凸集，$\alpha\in\mathbf{R}$、$a\in\mathbf{R}^n$，那么集合 $\alpha S$ 和 $S+a$ 都是凸集，其中

$$
\alpha S=\{\alpha x\mid x\in S\},\qquad S+a=\{x+a\mid x\in S\}.
$$

凸集在部分坐标上的投影也是凸集：如果 $S\subseteq\mathbf{R}^m\times\mathbf{R}^n$ 是凸集，那么

$$
T=\{x_1\in\mathbf{R}^m\mid\text{存在 }x_2\in\mathbf{R}^n\text{，使 }(x_1,x_2)\in S\}
$$

是凸集。

两个集合的和定义为

$$
S_1+S_2=\{x+y\mid x\in S_1,\ y\in S_2\}.
$$

如果 $S_1$ 和 $S_2$ 是凸集，那么 $S_1+S_2$ 也是凸集。为说明这一点，注意当 $S_1$ 和 $S_2$ 为凸集时，它们的直积或笛卡尔积

$$
S_1\times S_2=\{(x_1,x_2)\mid x_1\in S_1,\ x_2\in S_2\}
$$

也是凸集。该集合在线性函数 $f(x_1,x_2)=x_1+x_2$ 下的像就是和 $S_1+S_2$。

还可以考虑 $\mathbf{R}^n\times\mathbf{R}^m$ 中集合 $S_1,S_2$ 的**部分和**（partial sum），定义为

$$
S=\{(x,y_1+y_2)\mid(x,y_1)\in S_1,\ (x,y_2)\in S_2\},
$$

其中 $x\in\mathbf{R}^n$，$y_i\in\mathbf{R}^m$。当 $m=0$ 时，部分和就是 $S_1$ 和 $S_2$ 的交集；当 $n=0$ 时，它就是集合加法。凸集的部分和仍是凸集，见习题 2.16。

<div class="example" markdown="1">

**例 2.9 多面体。** 多面体 $\{x\mid Ax\preceq b,\ Cx=d\}$ 可以表示为非负正交象限与原点的笛卡尔积，在仿射函数 $f(x)=(b-Ax,d-Cx)$ 下的原像：

$$
\{x\mid Ax\preceq b,\ Cx=d\}=\{x\mid f(x)\in\mathbf{R}_+^m\times\{0\}\}.
$$

</div>

<div class="example" markdown="1">

**例 2.10 线性矩阵不等式的解集。** 条件

$$
A(x)=x_1A_1+\cdots+x_nA_n\preceq B,
\tag{2.11}
$$

其中 $B,A_i\in\mathbf{S}^m$，称为关于 $x$ 的**线性矩阵不等式**（linear matrix inequality，LMI）。（注意它与普通线性不等式

$$
a^Tx=x_1a_1+\cdots+x_na_n\leq b,
$$

的相似性，其中 $b,a_i\in\mathbf{R}$。）

线性矩阵不等式的解集 $\{x\mid A(x)\preceq B\}$ 是凸集。实际上，它是半正定锥在仿射函数 $f:\mathbf{R}^n\to\mathbf{S}^m$、$f(x)=B-A(x)$ 下的原像。

</div>

<!-- pdf-page: 53 -->

<div class="example" markdown="1">

**例 2.11 双曲锥（hyperbolic cone）。** 集合

$$
\{x\mid x^TPx\leq(c^Tx)^2,\ c^Tx\geq0\},
$$

其中 $P\in\mathbf{S}_+^n$、$c\in\mathbf{R}^n$，是凸集，因为它是二阶锥

$$
\{(z,t)\mid z^Tz\leq t^2,\ t\geq0\}
$$

在仿射函数 $f(x)=(P^{1/2}x,c^Tx)$ 下的原像。

</div>

<div class="example" markdown="1">

**例 2.12 椭球。** 椭球

$$
\mathcal{E}=\{x\mid(x-x_c)^TP^{-1}(x-x_c)\leq1\},
$$

其中 $P\in\mathbf{S}_{++}^n$，是单位欧几里得球 $\{u\mid\|u\|_2\leq1\}$ 在仿射映射 $f(u)=P^{1/2}u+x_c$ 下的像。（它也是单位球在仿射映射 $g(x)=P^{-1/2}(x-x_c)$ 下的原像。）

</div>

### 2.3.3 线性分式函数与透视函数

本节研究一类称为线性分式函数的函数，它们比仿射函数更一般，但仍然保持凸性。

#### 透视函数

定义**透视函数**（perspective function）$P:\mathbf{R}^{n+1}\to\mathbf{R}^n$ 为 $P(z,t)=z/t$，其定义域为 $\operatorname{\mathbf{dom}}P=\mathbf{R}^n\times\mathbf{R}_{++}$。（这里 $\mathbf{R}_{++}$ 表示正数集：$\mathbf{R}_{++}=\{x\in\mathbf{R}\mid x>0\}$。）透视函数先缩放或归一化向量，使最后一个分量等于 1，再去掉最后一个分量。

<div class="remark" markdown="1">

**注 2.1** 可以把透视函数解释为针孔相机的作用。$\mathbf{R}^3$ 中的针孔相机由不透明的水平平面 $x_3=0$ 和水平成像平面 $x_3=-1$ 组成；前者只在原点处有一个能让光线通过的针孔。位于相机上方的 $x$ 处的物体，即 $x_3>0$ 的物体，会在成像平面的点 $-(x_1/x_3,x_2/x_3,1)$ 处成像。去掉像点的最后一个分量，因为它总为 $-1$，则 $x$ 处的点在成像平面上对应于 $y=-(x_1/x_3,x_2/x_3)=-P(x)$。图 2.15 展示了这一过程。

</div>

<figure id="fig-2-15" data-figure="2.15" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-15.png" alt="光线穿过原点处的小孔，在下方像平面上形成对应像点" data-source-page="54" data-source-rect="229,120,475,242">
<figcaption>图 2.15 透视函数的针孔相机解释。深色水平线表示 $\mathbf{R}^3$ 中的平面 $x_3=0$；除原点处有一个针孔外，这个平面均不透光。位于该平面上方的物体或光源会在像平面 $x_3=-1$ 上成像，像平面用较浅的水平线表示。从光源位置到其像的位置的映射与透视函数有关。</figcaption>
</figure>

如果 $C\subseteq\operatorname{\mathbf{dom}}P$ 是凸集，那么它的像

$$
P(C)=\{P(x)\mid x\in C\}
$$

也是凸集。这个结果当然符合直觉：通过针孔相机观察凸物体，得到的像仍是凸的。为了证明这一事实，我们说明透视函数会把线段映成线段。（这同样符合直觉：<!-- pdf-page: 54 -->通过针孔相机观察线段，得到的像仍是一条线段。）设 $x=(\widetilde{x},x_{n+1})$、$y=(\widetilde{y},y_{n+1})\in\mathbf{R}^{n+1}$，且 $x_{n+1}>0$、$y_{n+1}>0$。那么对于 $0\leq\theta\leq1$，有

$$
P(\theta x+(1-\theta)y)=\frac{\theta\widetilde{x}+(1-\theta)\widetilde{y}}{\theta x_{n+1}+(1-\theta)y_{n+1}}=\mu P(x)+(1-\mu)P(y),
$$

其中

$$
\mu=\frac{\theta x_{n+1}}{\theta x_{n+1}+(1-\theta)y_{n+1}}\in[0,1].
$$

$\theta$ 与 $\mu$ 之间的这个对应关系是单调的：当 $\theta$ 从 0 变化到 1，即扫过线段 $[x,y]$ 时，$\mu$ 也从 0 变化到 1，即扫过线段 $[P(x),P(y)]$。这说明 $P([x,y])=[P(x),P(y)]$。

现在设 $C$ 是凸集，且 $C\subseteq\operatorname{\mathbf{dom}}P$，也就是对所有 $x\in C$ 都有 $x_{n+1}>0$，并设 $x,y\in C$。要证明 $P(C)$ 的凸性，只需证明线段 $[P(x),P(y)]$ 包含在 $P(C)$ 中。但这条线段正是线段 $[x,y]$ 在 $P$ 下的像，因此包含在 $P(C)$ 中。

凸集在透视函数下的原像也是凸集：如果 $C\subseteq\mathbf{R}^n$ 是凸集，那么

$$
P^{-1}(C)=\{(x,t)\in\mathbf{R}^{n+1}\mid x/t\in C,\ t>0\}
$$

是凸集。为证明这一点，设 $(x,t)\in P^{-1}(C)$、$(y,s)\in P^{-1}(C)$，且 $0\leq\theta\leq1$。需要证明

$$
\theta(x,t)+(1-\theta)(y,s)\in P^{-1}(C),
$$

也就是证明

$$
\frac{\theta x+(1-\theta)y}{\theta t+(1-\theta)s}\in C
$$

<!-- pdf-page: 55 -->

（$\theta t+(1-\theta)s>0$ 显然成立）。这可以由下式推出：

$$
\frac{\theta x+(1-\theta)y}{\theta t+(1-\theta)s}=\mu(x/t)+(1-\mu)(y/s),
$$

其中

$$
\mu=\frac{\theta t}{\theta t+(1-\theta)s}\in[0,1].
$$

#### 线性分式函数

线性分式函数由透视函数与仿射函数复合而成。设 $g:\mathbf{R}^n\to\mathbf{R}^{m+1}$ 是仿射函数，即

$$
g(x)=\begin{bmatrix}A\\c^T\end{bmatrix}x+\begin{bmatrix}b\\d\end{bmatrix},
\tag{2.12}
$$

其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$c\in\mathbf{R}^n$、$d\in\mathbf{R}$。由 $f=P\circ g$ 给出的函数 $f:\mathbf{R}^n\to\mathbf{R}^m$，即

$$
f(x)=(Ax+b)/(c^Tx+d),\qquad\operatorname{\mathbf{dom}}f=\{x\mid c^Tx+d>0\},
\tag{2.13}
$$

称为**线性分式函数**（linear-fractional function），也称**射影函数**（projective function）。如果 $c=0$ 且 $d>0$，那么 $f$ 的定义域是 $\mathbf{R}^n$，而 $f$ 是仿射函数。因此，可以把仿射函数和线性函数看成线性分式函数的特殊情况。

<div class="remark" markdown="1">

**注 2.2 射影解释。** 把线性分式函数表示为矩阵

$$
Q=\begin{bmatrix}A&b\\c^T&d\end{bmatrix}\in\mathbf{R}^{(m+1)\times(n+1)}
\tag{2.14}
$$

通常很方便：让矩阵作用于形如 $(x,1)$ 的点，也就是作矩阵乘法，得到 $(Ax+b,c^Tx+d)$。再把结果缩放或归一化，使最后一个分量等于 1，就得到 $(f(x),1)$。

把 $\mathbf{R}^n$ 与 $\mathbf{R}^{n+1}$ 中的一组射线按下述方式对应起来，就能给出这种表示的几何解释。对于 $\mathbf{R}^n$ 中每个点 $z$，令它对应于 $\mathbf{R}^{n+1}$ 中的开射线 $\mathcal{P}(z)=\{t(z,1)\mid t>0\}$。这条射线的最后一个分量取正值。反过来，$\mathbf{R}^{n+1}$ 中任何以原点为起点、最后一个分量取正值的射线，都可以对某个 $v\in\mathbf{R}^n$ 写成 $\mathcal{P}(v)=\{t(v,1)\mid t\geq0\}$。$\mathbf{R}^n$ 与最后一个分量为正的半空间中的射线之间，这个射影对应 $\mathcal{P}$ 是一一对应且满射的。

线性分式函数 (2.13) 可以表示为

$$
f(x)=\mathcal{P}^{-1}(Q\mathcal{P}(x)).
$$

因此，我们从 $x\in\operatorname{\mathbf{dom}}f$ 出发，即 $c^Tx+d>0$。先构造 $\mathbf{R}^{n+1}$ 中的射线 $\mathcal{P}(x)$。矩阵为 $Q$ 的线性变换作用在这条射线上，得到另一条射线 $Q\mathcal{P}(x)$。由于 $x\in\operatorname{\mathbf{dom}}f$，这条射线的最后一个分量取正值。最后应用逆射影变换，恢复出 $f(x)$。

</div>

<div class="translator-note" markdown="1">

**译注（注 2.2）：** 这里讨论的是不包含原点的开射线。按前述定义，后一式的参数也应满足 $t>0$；原式中的 $t\geq0$ 会把原点包括在内，与“最后一个分量为正”不一致。

</div>

<!-- pdf-page: 56 -->

<figure id="fig-2-16" data-figure="2.16" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-16.png" alt="左侧原集合及线性分式函数定义域边界，右侧为映射后的集合及逆函数定义域边界" data-source-page="56" data-source-rect="153,121,519,303">
<figcaption>图 2.16 左：集合 $C\subseteq\mathbf{R}^2$。虚线表示线性分式函数 $f(x)=x/(x_1+x_2+1)$ 的定义域边界，其中 $\operatorname{\mathbf{dom}}f=\{(x_1,x_2)\mid x_1+x_2+1>0\}$。右：$C$ 在 $f$ 下的像。虚线表示 $f^{-1}$ 的定义域边界。</figcaption>
</figure>

与透视函数一样，线性分式函数也保持凸性。如果 $C$ 是凸集，且包含在 $f$ 的定义域中，即对 $x\in C$ 有 $c^Tx+d>0$，那么它的像 $f(C)$ 是凸集。这可直接由前面的结果推出：$C$ 在仿射映射 (2.12) 下的像是凸集，而所得集合在透视函数 $P$ 下的像，即 $f(C)$，仍是凸集。同样，如果 $C\subseteq\mathbf{R}^m$ 是凸集，那么原像 $f^{-1}(C)$ 也是凸集。

<div class="example" markdown="1">

**例 2.13 条件概率。** 设随机变量 $u$ 和 $v$ 分别在 $\{1,\ldots,n\}$ 和 $\{1,\ldots,m\}$ 中取值，用 $p_{ij}$ 表示 $\operatorname{\mathbf{prob}}(u=i,v=j)$。那么条件概率 $f_{ij}=\operatorname{\mathbf{prob}}(u=i\mid v=j)$ 为

$$
f_{ij}=\frac{p_{ij}}{\sum_{k=1}^{n}p_{kj}}.
$$

因此，$f$ 由 $p$ 经过线性分式映射得到。

于是，如果 $C$ 是 $(u,v)$ 的联合概率所构成的一个凸集，那么与之对应的、给定 $v$ 时 $u$ 的条件概率所构成的集合也是凸集。

</div>

图 2.16 展示了集合 $C\subseteq\mathbf{R}^2$，以及它在线性分式函数

$$
f(x)=\frac{1}{x_1+x_2+1}x,\qquad\operatorname{\mathbf{dom}}f=\{(x_1,x_2)\mid x_1+x_2+1>0\}
$$

下的像。

<!-- pdf-page: 57 -->

## 2.4 广义不等式

### 2.4.1 正常锥与广义不等式

如果锥 $K\subseteq\mathbf{R}^n$ 满足以下条件，就称它是**正常锥**（proper cone）：

- $K$ 是凸集。
- $K$ 是闭集。
- $K$ 是**实心的**（solid），也就是说，它的内部非空。
- $K$ 是**尖的**（pointed），也就是说，它不包含任何直线；等价地，$x\in K$、$-x\in K$ 蕴含 $x=0$。

正常锥 $K$ 可以用来定义**广义不等式**，也就是 $\mathbf{R}^n$ 上的一种偏序，它具有 $\mathbf{R}$ 上标准序关系的许多性质。与正常锥 $K$ 对应的 $\mathbf{R}^n$ 上的偏序定义为

$$
x\preceq_K y\quad\Longleftrightarrow\quad y-x\in K.
$$

也用 $x\succeq_K y$ 表示 $y\preceq_K x$。类似地，定义相应的严格偏序为

$$
x\prec_K y\quad\Longleftrightarrow\quad y-x\in\operatorname{\mathbf{int}}K,
$$

并用 $x\succ_K y$ 表示 $y\prec_K x$。（为了把广义不等式 $\preceq_K$ 与严格广义不等式区分开，有时也将 $\preceq_K$ 称为非严格广义不等式。）

当 $K=\mathbf{R}_+$ 时，偏序 $\preceq_K$ 就是 $\mathbf{R}$ 上通常的序关系 $\leq$，严格偏序 $\prec_K$ 也就是 $\mathbf{R}$ 上通常的严格序关系 $<$。因此，广义不等式把 $\mathbf{R}$ 上普通的非严格和严格不等式都包含为特殊情况。

<div class="example" markdown="1">

**例 2.14 非负正交象限与逐分量不等式。** 非负正交象限 $K=\mathbf{R}_+^n$ 是正常锥。它对应的广义不等式 $\preceq_K$ 就是向量之间的逐分量不等式：$x\preceq_K y$ 表示 $x_i\leq y_i$，$i=1,\ldots,n$。相应的严格不等式则是逐分量严格不等式：$x\prec_K y$ 表示 $x_i<y_i$，$i=1,\ldots,n$。

由于与非负正交象限对应的非严格和严格偏序十分常见，我们省略下标 $\mathbf{R}_+^n$；当符号 $\preceq$ 或 $\prec$ 出现在向量之间时，就默认是这个含义。

</div>

<div class="example" markdown="1">

**例 2.15 半正定锥与矩阵不等式。** 半正定锥 $\mathbf{S}_+^n$ 是 $\mathbf{S}^n$ 中的正常锥。相应的广义不等式 $\preceq_K$ 就是通常的矩阵不等式：$X\preceq_K Y$ 表示 $Y-X$ 半正定。$\mathbf{S}_+^n$ 在 $\mathbf{S}^n$ 中的内部由正定矩阵构成，因此严格广义不等式也与对称矩阵之间通常的严格不等式一致：$X\prec_K Y$ 表示 $Y-X$ 正定。

这里的偏序也十分常见，所以同样省略下标：对于对称矩阵，直接写 $X\preceq Y$ 或 $X\prec Y$，默认这些广义不等式是相对于半正定锥定义的。

</div>

<!-- pdf-page: 58 -->

<div class="example" markdown="1">

**例 2.16 在 $[0,1]$ 上非负的多项式锥。** 定义 $K$ 为

$$
K=\{c\in\mathbf{R}^n\mid\text{对 }t\in[0,1]\text{，有 }c_1+c_2t+\cdots+c_nt^{n-1}\geq0\},
\tag{2.15}
$$

即 $K$ 是在区间 $[0,1]$ 上非负的 $n-1$ 次多项式的系数所构成的锥。可以证明，$K$ 是正常锥；其内部是由在区间 $[0,1]$ 上为正的多项式的系数构成的集合。

两个向量 $c,d\in\mathbf{R}^n$ 满足 $c\preceq_K d$，当且仅当对所有 $t\in[0,1]$ 都有

$$
c_1+c_2t+\cdots+c_nt^{n-1}\leq d_1+d_2t+\cdots+d_nt^{n-1}.
$$

</div>

#### 广义不等式的性质

广义不等式 $\preceq_K$ 满足许多性质，例如：

- $\preceq_K$ 在相加后保持成立：如果 $x\preceq_K y$ 且 $u\preceq_K v$，那么 $x+u\preceq_K y+v$。
- $\preceq_K$ 具有传递性：如果 $x\preceq_K y$ 且 $y\preceq_K z$，那么 $x\preceq_K z$。
- $\preceq_K$ 在非负缩放后保持成立：如果 $x\preceq_K y$ 且 $\alpha\geq0$，那么 $\alpha x\preceq_K\alpha y$。
- $\preceq_K$ 具有自反性：$x\preceq_K x$。
- $\preceq_K$ 具有反对称性：如果 $x\preceq_K y$ 且 $y\preceq_K x$，那么 $x=y$。
- $\preceq_K$ 在取极限后保持成立：如果 $x_i\preceq_K y_i$，$i=1,2,\ldots$，且当 $i\to\infty$ 时，$x_i\to x$、$y_i\to y$，那么 $x\preceq_K y$。

相应的严格广义不等式 $\prec_K$ 则满足例如以下性质：

- 如果 $x\prec_K y$，那么 $x\preceq_K y$。
- 如果 $x\prec_K y$ 且 $u\preceq_K v$，那么 $x+u\prec_K y+v$。
- 如果 $x\prec_K y$ 且 $\alpha>0$，那么 $\alpha x\prec_K\alpha y$。
- $x\not\prec_K x$。
- 如果 $x\prec_K y$，那么当 $u$ 和 $v$ 足够小时，有 $x+u\prec_K y+v$。

这些性质都来自 $\preceq_K$ 和 $\prec_K$ 的定义，以及正常锥的性质，见习题 2.30。

<!-- pdf-page: 59 -->

### 2.4.2 最小元素与极小元素

广义不等式记号 $\preceq_K$、$\prec_K$ 的设计，是为了体现它与 $\mathbf{R}$ 上普通不等式 $\leq$、$<$ 的类比。虽然普通不等式的许多性质对广义不等式也成立，但某些重要性质却不成立。最明显的区别是，$\mathbf{R}$ 上的 $\leq$ 是一个**全序**（linear ordering）：任意两点都是可比较的，即必有 $x\leq y$ 或 $y\leq x$。其他广义不等式并不具有这一性质。一个结果是，最小和最大等概念在广义不等式的背景下变得更加复杂。本节对此作简要讨论。

如果对每个 $y\in S$ 都有 $x\preceq_K y$，就称 $x\in S$ 是 $S$ 相对于广义不等式 $\preceq_K$ 的**最小元素**（minimum element）。可以类似地定义集合 $S$ 相对于广义不等式的**最大元素**。如果一个集合有最小元素或最大元素，那么它是唯一的。一个相关概念是**极小元素**（minimal element）：如果 $y\in S$ 且 $y\preceq_K x$ 只有在 $y=x$ 时才成立，就称 $x\in S$ 是 $S$ 相对于广义不等式 $\preceq_K$ 的极小元素。**极大元素**可以类似地定义。一个集合可以有许多不同的极小元素或极大元素。

可以用简单的集合记号描述最小元素与极小元素。点 $x\in S$ 是 $S$ 的最小元素，当且仅当

$$
S\subseteq x+K.
$$

这里 $x+K$ 表示所有能与 $x$ 比较，并且按 $\preceq_K$ 大于或等于 $x$ 的点。点 $x\in S$ 是极小元素，当且仅当

$$
(x-K)\cap S=\{x\}.
$$

这里 $x-K$ 表示所有能与 $x$ 比较，并且按 $\preceq_K$ 小于或等于 $x$ 的点；它与 $S$ 唯一的公共点是 $x$。

当 $K=\mathbf{R}_+$ 时，它诱导出 $\mathbf{R}$ 上通常的序关系，此时极小和最小的概念相同，都与集合最小元素的通常定义一致。

<div class="example" markdown="1">

**例 2.17** 考虑锥 $\mathbf{R}_+^2$，它诱导出 $\mathbf{R}^2$ 中的逐分量不等式。这时可以对极小元素和最小元素给出简单的几何描述。不等式 $x\preceq y$ 表示 $y$ 位于 $x$ 的右上方。说 $x\in S$ 是集合 $S$ 的最小元素，意味着 $S$ 中所有其他点都位于其右上方。说 $x$ 是集合 $S$ 的极小元素，意味着 $S$ 中没有其他点位于 $x$ 的左下方，见图 2.17。

</div>

<div class="example" markdown="1">

**例 2.18 对称矩阵集合的最小元素与极小元素。** 对每个 $A\in\mathbf{S}_{++}^n$，令它对应于以原点为中心的椭球

$$
\mathcal{E}_A=\{x\mid x^TA^{-1}x\leq1\}.
$$

有 $A\preceq B$ 当且仅当 $\mathcal{E}_A\subseteq\mathcal{E}_B$。

给定 $v_1,\ldots,v_k\in\mathbf{R}^n$，定义

$$
S=\{P\in\mathbf{S}_{++}^n\mid v_i^TP^{-1}v_i\leq1,\ i=1,\ldots,k\},
$$

<!-- pdf-page: 60 -->

它对应于所有包含点 $v_1,\ldots,v_k$ 的椭球。集合 $S$ 没有最小元素：对于任意包含点 $v_1,\ldots,v_k$ 的椭球，都可以找到另一个同样包含这些点、却与它不可比较的椭球。如果一个椭球包含这些点，但任何更小的椭球都不能包含这些点，它就是极小的。图 2.18 展示了 $\mathbf{R}^2$ 中 $k=2$ 时的一个例子。

</div>

<figure id="fig-2-17" data-figure="2.17" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-17.png" alt="左图为一个最小元素及其右上方锥，右图为一个极小元素及其左下方锥" data-source-page="60" data-source-rect="183,120,487,263">
<figcaption>图 2.17 左：相对于 $\mathbf{R}^2$ 中的逐分量不等式，集合 $S_1$ 有一个最小元素 $x_1$。集合 $x_1+K$ 用浅色阴影表示；由于 $S_1\subseteq x_1+K$，$x_1$ 是 $S_1$ 的最小元素。右：点 $x_2$ 是 $S_2$ 的一个极小点。集合 $x_2-K$ 用浅色阴影表示。由于 $x_2-K$ 与 $S_2$ 仅在 $x_2$ 处相交，点 $x_2$ 是极小点。</figcaption>
</figure>

## 2.5 分离超平面与支撑超平面

### 2.5.1 分离超平面定理

本节介绍一个后面会起重要作用的思想：用超平面或仿射函数分离不相交的凸集。基本结果是**分离超平面定理**（separating hyperplane theorem）：设 $C$ 和 $D$ 是非空且不相交的凸集，即 $C\cap D=\varnothing$。那么存在 $a\ne0$ 和 $b$，使得对所有 $x\in C$ 都有 $a^Tx\leq b$，对所有 $x\in D$ 都有 $a^Tx\geq b$。换句话说，仿射函数 $a^Tx-b$ 在 $C$ 上非正，在 $D$ 上非负。超平面 $\{x\mid a^Tx=b\}$ 称为集合 $C$ 和 $D$ 的**分离超平面**，或者说它**分离**了集合 $C$ 和 $D$，见图 2.19。

#### 分离超平面定理的证明

这里考虑一种特殊情况，证明向一般情况的推广留作习题，见习题 2.22。我们假设 $C$ 与 $D$ 之间的欧几里得距离，定义为

$$
\operatorname{\mathbf{dist}}(C,D)=\inf\{\|u-v\|_2\mid u\in C,\ v\in D\},
$$

<!-- pdf-page: 61 -->

<figure id="fig-2-18" data-figure="2.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-18.png" alt="三个以原点为中心并包含两个给定点的椭球，其中倾斜的细长椭球是极小的" data-source-page="61" data-source-rect="219,159,351,290">
<figcaption>图 2.18 $\mathbf{R}^2$ 中的三个椭球，它们都以原点（下方的圆点）为中心，并包含上方两个圆点所示的点。椭球 $\mathcal{E}_1$ 不是极小的，因为存在更小且仍包含这些点的椭球，例如 $\mathcal{E}_3$。$\mathcal{E}_3$ 也因同样的原因不是极小的。椭球 $\mathcal{E}_2$ 是极小的，因为不存在另一个以原点为中心、包含这些点且包含于 $\mathcal{E}_2$ 的椭球。</figcaption>
</figure>

<figure id="fig-2-19" data-figure="2.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-19.png" alt="分离超平面将两个不相交凸集置于两侧" data-source-page="61" data-source-rect="209,459,394,603">
<figcaption>图 2.19 超平面 $\{x\mid a^Tx=b\}$ 分离了不相交的凸集 $C$ 和 $D$。仿射函数 $a^Tx-b$ 在 $C$ 上非正，在 $D$ 上非负。</figcaption>
</figure>

<!-- pdf-page: 62 -->

<figure id="fig-2-20" data-figure="2.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-20.png" alt="两个凸集间最近点的连线，其中垂面给出分离超平面" data-source-page="62" data-source-rect="255,120,422,270">
<figcaption>图 2.20 两个凸集之间分离超平面的构造。点 $c\in C$ 和 $d\in D$ 是两个集合中彼此距离最近的一对点。分离超平面与 $c$、$d$ 之间的线段垂直，并平分这条线段。</figcaption>
</figure>

为正，并且存在点 $c\in C$ 和 $d\in D$ 达到这个最小距离，即 $\|c-d\|_2=\operatorname{\mathbf{dist}}(C,D)$。（例如，当 $C$、$D$ 都是闭集，且其中一个有界时，这些条件就成立。）

定义

$$
a=d-c,\qquad b=\frac{\|d\|_2^2-\|c\|_2^2}{2}.
$$

我们将证明，仿射函数

$$
f(x)=a^Tx-b=(d-c)^T(x-(1/2)(d+c))
$$

在 $C$ 上非正，在 $D$ 上非负，即超平面 $\{x\mid a^Tx=b\}$ 分离 $C$ 与 $D$。这个超平面垂直于连接 $c$ 和 $d$ 的线段，并且经过线段的中点，如图 2.20 所示。

先证明 $f$ 在 $D$ 上非负。$f$ 在 $C$ 上非正的证明类似，也可以交换 $C$ 和 $D$，并考虑 $-f$ 得到。假设存在点 $u\in D$，使得

$$
f(u)=(d-c)^T(u-(1/2)(d+c))<0.
\tag{2.16}
$$

可将 $f(u)$ 写成

$$
f(u)=(d-c)^T(u-d+(1/2)(d-c))=(d-c)^T(u-d)+(1/2)\|d-c\|_2^2.
$$

可见，(2.16) 蕴含 $(d-c)^T(u-d)<0$。现在注意到

$$
\left.\frac{d}{dt}\|d+t(u-d)-c\|_2^2\right|_{t=0}=2(d-c)^T(u-d)<0,
$$

因此，对某个足够小且满足 $t\leq1$ 的 $t>0$，有

$$
\|d+t(u-d)-c\|_2<\|d-c\|_2,
$$

<!-- pdf-page: 63 -->

即点 $d+t(u-d)$ 比 $d$ 更接近 $c$。由于 $D$ 是凸集并且包含 $d$ 和 $u$，所以 $d+t(u-d)\in D$。但这不可能，因为已经假设 $d$ 是 $D$ 中距离 $C$ 最近的点。

<div class="example" markdown="1">

**例 2.19 仿射集与凸集的分离。** 设 $C$ 是凸集，$D$ 是仿射集，即 $D=\{Fu+g\mid u\in\mathbf{R}^m\}$，其中 $F\in\mathbf{R}^{n\times m}$。假设 $C$ 与 $D$ 不相交，那么根据分离超平面定理，存在 $a\ne0$ 和 $b$，使得对所有 $x\in C$ 有 $a^Tx\leq b$，对所有 $x\in D$ 有 $a^Tx\geq b$。

对所有 $x\in D$ 都有 $a^Tx\geq b$，意味着对所有 $u\in\mathbf{R}^m$ 都有 $a^TFu\geq b-a^Tg$。但线性函数只有恒为零时，才在 $\mathbf{R}^m$ 上有下界，因此 $a^TF=0$，从而 $b\leq a^Tg$。

所以，存在 $a\ne0$，使得 $F^Ta=0$，且对所有 $x\in C$ 都有 $a^Tx\leq a^Tg$。

</div>

#### 严格分离

上面构造的分离超平面满足更强的条件：对所有 $x\in C$ 有 $a^Tx<b$，对所有 $x\in D$ 有 $a^Tx>b$。这称为集合 $C$ 与 $D$ 的**严格分离**（strict separation）。简单例子表明，一般情况下，不相交的凸集未必能用超平面严格分离，即使它们都是闭集也如此，见习题 2.23。不过，在许多特殊情况下可以证明严格分离成立。

<div class="example" markdown="1">

**例 2.20 点与闭凸集的严格分离。** 设 $C$ 是闭凸集，且 $x_0\notin C$。那么存在一个超平面，将 $x_0$ 与 $C$ 严格分离。

为说明这一点，注意对于某个 $\epsilon>0$，集合 $C$ 与 $B(x_0,\epsilon)$ 不相交。根据分离超平面定理，存在 $a\ne0$ 和 $b$，使得当 $x\in C$ 时有 $a^Tx\leq b$，当 $x\in B(x_0,\epsilon)$ 时有 $a^Tx\geq b$。

利用 $B(x_0,\epsilon)=\{x_0+u\mid\|u\|_2\leq\epsilon\}$，第二个条件可以写成

$$
a^T(x_0+u)\geq b\qquad\text{对所有 }\|u\|_2\leq\epsilon.
$$

使左端最小的向量为 $u=-\epsilon a/\|a\|_2$；代入这个值，得到

$$
a^Tx_0-\epsilon\|a\|_2\geq b.
$$

因此，仿射函数

$$
f(x)=a^Tx-b-\epsilon\|a\|_2/2
$$

在 $C$ 上为负，在 $x_0$ 处为正。

由此可以直接证明前面已经提到的事实：闭凸集是所有包含它的半空间的交集。事实上，设 $C$ 为闭凸集，$S$ 为所有包含 $C$ 的半空间的交集。显然，$x\in C\Rightarrow x\in S$。为了证明反向包含关系，假设存在 $x\in S$ 且 $x\notin C$。根据严格分离的结果，存在一个超平面将 $x$ 与 $C$ 严格分离，即存在一个包含 $C$、却不包含 $x$ 的半空间。换言之，$x\notin S$。

</div>

<!-- pdf-page: 64 -->

#### 分离超平面的逆定理

除非对 $C$ 或 $D$ 加上凸性之外的附加条件，否则分离超平面定理的逆命题并不成立；这个逆命题是说，存在分离超平面就意味着 $C$ 和 $D$ 不相交。一个简单的反例是 $C=D=\{0\}\subseteq\mathbf{R}$，此时超平面 $x=0$ 就分离了 $C$ 和 $D$。

通过对 $C$ 和 $D$ 添加条件，可以得到各种逆向分离定理。一个很简单的例子是：设 $C$ 和 $D$ 为凸集，$C$ 是开集，并且存在仿射函数 $f$，使其在 $C$ 上非正，在 $D$ 上非负。那么 $C$ 和 $D$ 不相交。（为说明这一点，先注意到 $f$ 在 $C$ 上必定为负；如果 $f$ 在 $C$ 的某点为零，那么它就会在该点附近取到正值，产生矛盾。由于 $f$ 在 $C$ 上为负、在 $D$ 上非负，因此 $C$ 与 $D$ 必不相交。）把这个逆命题与分离超平面定理结合起来，得到以下结果：任意两个凸集 $C$ 和 $D$，只要其中至少一个是开集，它们不相交当且仅当存在分离超平面。

<div class="example" markdown="1">

**例 2.21 严格线性不等式的择一定理（theorem of alternatives）。** 我们推导严格线性不等式组

$$
Ax\prec b
\tag{2.17}
$$

有解的充要条件。这组不等式不可行，当且仅当凸集

$$
C=\{b-Ax\mid x\in\mathbf{R}^n\},\qquad D=\mathbf{R}_{++}^m=\{y\in\mathbf{R}^m\mid y\succ0\}
$$

不相交。集合 $D$ 是开集，$C$ 是仿射集。因此根据上述结果，$C$ 和 $D$ 不相交，当且仅当存在分离超平面，也就是说，存在非零 $\lambda\in\mathbf{R}^m$ 和 $\mu\in\mathbf{R}$，使得在 $C$ 上有 $\lambda^Ty\leq\mu$，在 $D$ 上有 $\lambda^Ty\geq\mu$。

这两个条件都可以简化。第一个条件表示对所有 $x$ 都有 $\lambda^T(b-Ax)\leq\mu$。与例 2.19 一样，这意味着 $A^T\lambda=0$ 且 $\lambda^Tb\leq\mu$。第二个不等式表示对所有 $y\succ0$ 都有 $\lambda^Ty\geq\mu$。这意味着 $\mu\leq0$，且 $\lambda\succeq0$、$\lambda\ne0$。

综合起来，严格不等式组 (2.17) 不可行，当且仅当存在 $\lambda\in\mathbf{R}^m$，使得

$$
\lambda\ne0,\qquad\lambda\succeq0,\qquad A^T\lambda=0,\qquad\lambda^Tb\leq0.
\tag{2.18}
$$

这也是关于变量 $\lambda\in\mathbf{R}^m$ 的一组线性不等式和线性等式。我们称 (2.17) 和 (2.18) 构成一对择一系统：对于任意数据 $A$ 和 $b$，它们恰好有一个有解。

</div>

### 2.5.2 支撑超平面

设 $C\subseteq\mathbf{R}^n$，$x_0$ 是其边界 $\operatorname{\mathbf{bd}}C$ 上的一点，即

$$
x_0\in\operatorname{\mathbf{bd}}C=\operatorname{\mathbf{cl}}C\setminus\operatorname{\mathbf{int}}C.
$$

如果 $a\ne0$ 满足对所有 $x\in C$ 都有 $a^Tx\leq a^Tx_0$，那么超平面 $\{x\mid a^Tx=a^Tx_0\}$ 称为 $C$ 在点 $x_0$ 处的**支撑超平面**（supporting hyperplane）。这等价于说，<!-- pdf-page: 65 -->点 $x_0$ 和集合 $C$ 被超平面 $\{x\mid a^Tx=a^Tx_0\}$ 分离。其几何解释是，超平面 $\{x\mid a^Tx=a^Tx_0\}$ 在 $x_0$ 处与 $C$ 相切，并且半空间 $\{x\mid a^Tx\leq a^Tx_0\}$ 包含 $C$，见图 2.21。

<figure id="fig-2-21" data-figure="2.21" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-21.png" alt="集合边界上一点处的支撑超平面与外法向量" data-source-page="65" data-source-rect="193,121,378,262">
<figcaption>图 2.21 超平面 $\{x\mid a^Tx=a^Tx_0\}$ 在 $x_0$ 处支撑集合 $C$。</figcaption>
</figure>

一个称为**支撑超平面定理**的基本结果指出：对于任意非空凸集 $C$ 和任意 $x_0\in\operatorname{\mathbf{bd}}C$，都存在 $C$ 在 $x_0$ 处的支撑超平面。支撑超平面定理容易由分离超平面定理证明。分两种情况讨论。如果 $C$ 的内部非空，对集合 $\{x_0\}$ 和 $\operatorname{\mathbf{int}}C$ 应用分离超平面定理，就立即得到结论。如果 $C$ 的内部为空，那么 $C$ 必定位于某个维数小于 $n$ 的仿射集中；任何包含这个仿射集的超平面都同时包含 $C$ 与 $x_0$，因而是一个平凡的支撑超平面。

支撑超平面定理也有一个部分逆命题：如果集合是闭集、内部非空，并且在边界的每一点都有支撑超平面，那么它是凸集，见习题 2.27。

## 2.6 对偶锥与广义不等式

### 2.6.1 对偶锥

设 $K$ 是一个锥。集合

$$
K^*=\{y\mid\text{对所有 }x\in K\text{，有 }x^Ty\geq0\}
\tag{2.19}
$$

称为 $K$ 的**对偶锥**（dual cone）。顾名思义，$K^*$ 是锥，而且总是凸的，即使原锥 $K$ 不是凸锥也如此，见习题 2.31。

从几何上看，$y\in K^*$ 当且仅当 $-y$ 是某个在原点处支撑 $K$ 的超平面的法向量，见图 2.22。

<div class="example" markdown="1">

**例 2.22 子空间。** 子空间 $V\subseteq\mathbf{R}^n$ 也是锥，它的对偶锥就是正交补 $V^\perp=\{y\mid\text{对所有 }v\in V\text{，有 }v^Ty=0\}$。

</div>

<!-- pdf-page: 66 -->

<figure id="fig-2-22" data-figure="2.22" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-22.png" alt="左侧半空间包含整个锥，右侧半空间未包含整个锥，展示对偶锥的判据" data-source-page="66" data-source-rect="192,121,486,246">
<figcaption>图 2.22 左：内法向量为 $y$ 的半空间包含锥 $K$，因此 $y\in K^*$。右：内法向量为 $z$ 的半空间不包含 $K$，因此 $z\notin K^*$。</figcaption>
</figure>

<div class="example" markdown="1">

**例 2.23 非负正交象限。** 锥 $\mathbf{R}_+^n$ 的对偶是它自身：

$$
\text{对所有 }x\succeq0\text{，有 }x^Ty\geq0\quad\Longleftrightarrow\quad y\succeq0.
$$

这样的锥称为**自对偶锥**（self-dual cone）。

</div>

<div class="example" markdown="1">

**例 2.24 半正定锥。** 在对称 $n\times n$ 矩阵集合 $\mathbf{S}^n$ 上，使用标准内积 $\operatorname{\mathbf{tr}}(XY)=\sum_{i,j=1}^{n}X_{ij}Y_{ij}$，见第 A.1.1 节。半正定锥 $\mathbf{S}_+^n$ 是自对偶的，即对于 $X,Y\in\mathbf{S}^n$，有

$$
\text{对所有 }X\succeq0\text{，有 }\operatorname{\mathbf{tr}}(XY)\geq0\quad\Longleftrightarrow\quad Y\succeq0.
$$

下面证明这一事实。

假设 $Y\notin\mathbf{S}_+^n$。那么存在 $q\in\mathbf{R}^n$，使得

$$
q^TYq=\operatorname{\mathbf{tr}}(qq^TY)<0.
$$

因此，半正定矩阵 $X=qq^T$ 满足 $\operatorname{\mathbf{tr}}(XY)<0$，所以 $Y\notin(\mathbf{S}_+^n)^*$。

现在设 $X,Y\in\mathbf{S}_+^n$。利用特征值分解，可将 $X$ 表示为 $X=\sum_{i=1}^{n}\lambda_iq_iq_i^T$，其中特征值 $\lambda_i\geq0$，$i=1,\ldots,n$。于是有

$$
\operatorname{\mathbf{tr}}(YX)=\operatorname{\mathbf{tr}}\left(Y\sum_{i=1}^{n}\lambda_iq_iq_i^T\right)=\sum_{i=1}^{n}\lambda_iq_i^TYq_i\geq0.
$$

这说明 $Y\in(\mathbf{S}_+^n)^*$。

</div>

<div class="example" markdown="1">

**例 2.25 范数锥的对偶。** 设 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的一个范数。对应的锥 $K=\{(x,t)\in\mathbf{R}^{n+1}\mid\|x\|\leq t\}$ 的对偶，是由对偶范数定义的锥，即

$$
K^*=\{(u,v)\in\mathbf{R}^{n+1}\mid\|u\|_*\leq v\},
$$

<!-- pdf-page: 67 -->

其中对偶范数为 $\|u\|_*=\sup\{u^Tx\mid\|x\|\leq1\}$，见式 (A.1.6)。

为了证明这个结果，需要证明

$$
\text{只要 }\|x\|\leq t\text{，就有 }x^Tu+tv\geq0\quad\Longleftrightarrow\quad\|u\|_*\leq v.
\tag{2.20}
$$

先证明关于 $(u,v)$ 的右侧条件蕴含左侧条件。设 $\|u\|_*\leq v$，且对某个 $t>0$ 有 $\|x\|\leq t$。（如果 $t=0$，那么 $x$ 必须为零，显然有 $u^Tx+vt\geq0$。）由对偶范数的定义，以及 $\|-x/t\|\leq1$，得到

$$
u^T(-x/t)\leq\|u\|_*\leq v,
$$

所以 $u^Tx+vt\geq0$。

再证明 (2.20) 中的左侧条件蕴含右侧条件。假设 $\|u\|_*>v$，即右侧条件不成立。根据对偶范数的定义，存在 $x$ 满足 $\|x\|\leq1$ 且 $x^Tu>v$。取 $t=1$，就有

$$
u^T(-x)+v<0,
$$

这与 (2.20) 中的左侧条件矛盾。

</div>

对偶锥具有若干性质，例如：

- $K^*$ 是闭凸集。
- $K_1\subseteq K_2$ 蕴含 $K_2^*\subseteq K_1^*$。
- 如果 $K$ 的内部非空，那么 $K^*$ 是尖的。
- 如果 $K$ 的闭包是尖的，那么 $K^*$ 的内部非空。
- $K^{**}$ 是 $K$ 的凸包的闭包。因此，如果 $K$ 是闭凸集，就有 $K^{**}=K$。

见习题 2.31。这些性质表明，如果 $K$ 是正常锥，那么其对偶 $K^*$ 也是正常锥，而且 $K^{**}=K$。

### 2.6.2 对偶广义不等式

现在假设凸锥 $K$ 是正常锥，因此它诱导出广义不等式 $\preceq_K$。它的对偶锥 $K^*$ 也是正常锥，所以同样诱导出一个广义不等式。我们把广义不等式 $\preceq_{K^*}$ 称为广义不等式 $\preceq_K$ 的**对偶**。

广义不等式与其对偶之间，有以下重要关系：

- $x\preceq_K y$ 当且仅当对于所有 $\lambda\succeq_{K^*}0$ 都有 $\lambda^Tx\leq\lambda^Ty$。
- $x\prec_K y$ 当且仅当对于所有满足 $\lambda\succeq_{K^*}0$、$\lambda\ne0$ 的 $\lambda$，都有 $\lambda^Tx<\lambda^Ty$。

由于 $K=K^{**}$，与 $\preceq_{K^*}$ 对应的对偶广义不等式就是 $\preceq_K$，因此交换广义不等式与其对偶之后，这些性质仍然成立。一个具体例子是：$\lambda\preceq_{K^*}\mu$ 当且仅当对所有 $x\succeq_K0$ 都有 $\lambda^Tx\leq\mu^Tx$。

<!-- pdf-page: 68 -->

<div class="example" markdown="1">

**例 2.26 线性严格广义不等式的择一定理。** 设 $K\subseteq\mathbf{R}^m$ 是正常锥。考虑严格广义不等式

$$
Ax\prec_K b,
\tag{2.21}
$$

其中 $x\in\mathbf{R}^n$。

我们将推导这个不等式的择一定理。假设它不可行，即仿射集 $\{b-Ax\mid x\in\mathbf{R}^n\}$ 与开凸集 $\operatorname{\mathbf{int}}K$ 不相交。那么存在分离超平面，也就是说，存在非零 $\lambda\in\mathbf{R}^m$ 和 $\mu\in\mathbf{R}$，使得对所有 $x$ 有 $\lambda^T(b-Ax)\leq\mu$，对所有 $y\in\operatorname{\mathbf{int}}K$ 有 $\lambda^Ty\geq\mu$。第一个条件蕴含 $A^T\lambda=0$ 和 $\lambda^Tb\leq\mu$。第二个条件蕴含对所有 $y\in K$ 都有 $\lambda^Ty\geq\mu$，而这只有在 $\lambda\in K^*$ 且 $\mu\leq0$ 时才可能成立。

综合起来，如果 (2.21) 不可行，那么存在 $\lambda$，使得

$$
\lambda\ne0,\qquad\lambda\succeq_{K^*}0,\qquad A^T\lambda=0,\qquad\lambda^Tb\leq0.
\tag{2.22}
$$

现在证明反向命题：如果 (2.22) 成立，那么不等式组 (2.21) 不可能可行。假设两个不等式组同时成立。由于 $\lambda\ne0$、$\lambda\succeq_{K^*}0$，且 $b-Ax\succ_K0$，有 $\lambda^T(b-Ax)>0$。但利用 $A^T\lambda=0$，又得到 $\lambda^T(b-Ax)=\lambda^Tb\leq0$，产生矛盾。

因此，不等式组 (2.21) 和 (2.22) 是择一的：对于任意数据 $A,b$，它们恰好有一个可行。（这推广了特殊情况 $K=\mathbf{R}_+^m$ 下的择一系统 (2.17)、(2.18)。）

</div>

### 2.6.3 用对偶不等式刻画最小元素与极小元素

可以利用对偶广义不等式，刻画集合 $S\subseteq\mathbf{R}^m$ 相对于正常锥 $K$ 诱导的广义不等式的最小元素和极小元素；这里 $S$ 不一定是凸集。

#### 最小元素的对偶刻画

先考虑最小元素的一种刻画：$x$ 是 $S$ 相对于广义不等式 $\preceq_K$ 的最小元素，当且仅当对于所有 $\lambda\succ_{K^*}0$，$x$ 都是在 $z\in S$ 上使 $\lambda^Tz$ 最小的唯一点。几何上，这意味着对于任意 $\lambda\succ_{K^*}0$，超平面

$$
\{z\mid\lambda^T(z-x)=0\}
$$

都是 $S$ 在 $x$ 处的严格支撑超平面。（所谓严格支撑超平面，是指它仅在点 $x$ 处与 $S$ 相交。）注意，这里不要求集合 $S$ 具有凸性，见图 2.23。

为证明这个结果，设 $x$ 是 $S$ 的最小元素，即对所有 $z\in S$ 都有 $x\preceq_K z$，并取 $\lambda\succ_{K^*}0$。设 $z\in S$ 且 $z\ne x$。因为 $x$ 是 $S$ 的最小元素，所以 $z-x\succeq_K0$。由 $\lambda\succ_{K^*}0$ 以及 $z-x\succeq_K0$、$z-x\ne0$，可得 $\lambda^T(z-x)>0$。由于 $z$ 是 $S$ 中任意不等于 $x$ 的元素，这就说明 $x$ 是在 $z\in S$ 上使 $\lambda^Tz$ 最小的唯一点。反过来，假设对所有 $\lambda\succ_{K^*}0$，$x$ 都是在 $z\in S$ 上使 $\lambda^Tz$ 最小的唯一点，但 $x$ 不是 $S$ 的最小元素。<!-- pdf-page: 69 -->那么存在 $z\in S$，使得 $z\not\succeq_K x$。由于 $z-x\not\succeq_K0$，存在 $\widetilde{\lambda}\succeq_{K^*}0$，使得 $\widetilde{\lambda}^T(z-x)<0$。所以在 $\widetilde{\lambda}$ 附近，存在 $\lambda\succ_{K^*}0$ 使得 $\lambda^T(z-x)<0$。这与 $x$ 是在 $S$ 上使 $\lambda^Tz$ 最小的唯一点这一假设矛盾。

<figure id="fig-2-23" data-figure="2.23" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-23.png" alt="集合的最小元素，以及在该点严格支撑集合的若干超平面" data-source-page="69" data-source-rect="175,122,394,278">
<figcaption>图 2.23 最小元素的对偶刻画。点 $x$ 是集合 $S$ 相对于 $\mathbf{R}_+^2$ 的最小元素。这等价于：对于每个 $\lambda\succ 0$，超平面 $\{z\mid\lambda^T(z-x)=0\}$ 都在 $x$ 处严格支撑 $S$，也就是说，$S$ 位于超平面的一侧，而且只在 $x$ 处与超平面接触。</figcaption>
</figure>

#### 极小元素的对偶刻画

现在考虑极小元素的类似刻画。在这里，必要条件与充分条件之间存在差距。如果 $\lambda\succ_{K^*}0$，并且 $x$ 在 $z\in S$ 上使 $\lambda^Tz$ 最小，那么 $x$ 是极小元素，见图 2.24。

为证明这一点，设 $\lambda\succ_{K^*}0$，$x$ 在 $S$ 上使 $\lambda^Tz$ 最小，但 $x$ 不是极小元素，即存在 $z\in S$，$z\ne x$，且 $z\preceq_K x$。那么 $\lambda^T(x-z)>0$，这与 $x$ 是在 $S$ 上使 $\lambda^Tz$ 最小的点这一假设矛盾。

反向命题一般不成立：点 $x$ 可以是 $S$ 的极小元素，但对于任何 $\lambda$，都不是在 $z\in S$ 上使 $\lambda^Tz$ 最小的点，如图 2.25 所示。该图提示，凸性在反向命题中起着重要作用，事实确实如此。只要集合 $S$ 是凸集，就可以说：对于任意极小元素 $x$，存在非零 $\lambda\succeq_{K^*}0$，使得 $x$ 在 $z\in S$ 上使 $\lambda^Tz$ 最小。

为证明这一点，设 $x$ 是极小元素，也就是说 $((x-K)\setminus\{x\})\cap S=\varnothing$。对凸集 $(x-K)\setminus\{x\}$ 和 $S$ 应用分离超平面定理，可知存在 $\lambda\ne0$ 和 $\mu$，使得对所有 $y\in K$ 有 $\lambda^T(x-y)\leq\mu$，对所有 $z\in S$ 有 $\lambda^Tz\geq\mu$。由第一个不等式得到 $\lambda\succeq_{K^*}0$。由于 $x\in S$ 且 $x\in x-K$，有 $\lambda^Tx=\mu$，所以第二个不等式意味着 $\mu$ 是 $\lambda^Tz$ 在 $S$ 上的最小值。因此，$x$ 是在 $S$ 上使 $\lambda^Tz$ 最小的点，其中 $\lambda\ne0$、$\lambda\succeq_{K^*}0$。

这个逆定理不能加强为 $\lambda\succ_{K^*}0$。有些例子表明，点 $x$ 可以是凸集 $S$ 的极小点，但对于任何 $\lambda\succ_{K^*}0$，都不是在 $z\in S$ 上使 $\lambda^Tz$ 最小的点，见图 2.26 左图。同样，当 $\lambda\succeq_{K^*}0$ 时，在 $z\in S$ 上使 $\lambda^Tz$ 最小的点也未必都是极小元素，见图 2.26 右图。

<!-- pdf-page: 70 -->

<figure id="fig-2-24" data-figure="2.24" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-24.png" alt="非凸集合左下边界上的极小点，以及两个正向量对应的线性函数最小点" data-source-page="70" data-source-rect="247,167,431,287">
<figcaption>图 2.24 集合 $S\subseteq\mathbf{R}^2$。它相对于 $\mathbf{R}_+^2$ 的极小点集，用左下边界上较深的一段表示。在 $S$ 上使 $\lambda_1^Tz$ 最小的点是 $x_1$；由于 $\lambda_1\succ 0$，$x_1$ 是极小点。在 $S$ 上使 $\lambda_2^Tz$ 最小的点是 $x_2$；由于 $\lambda_2\succ 0$，$x_2$ 是 $S$ 的另一个极小点。</figcaption>
</figure>

<figure id="fig-2-25" data-figure="2.25" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-25.png" alt="非凸集合凹陷处的极小元素及其左下方锥" data-source-page="70" data-source-rect="274,461,404,592">
<figcaption>图 2.25 点 $x$ 是 $S\subseteq\mathbf{R}^2$ 相对于 $\mathbf{R}_+^2$ 的一个极小元素。然而，不存在这样的 $\lambda$，使得 $x$ 在所有 $z\in S$ 中使 $\lambda^Tz$ 取得最小值。</figcaption>
</figure>

<!-- pdf-page: 71 -->

<figure id="fig-2-26" data-figure="2.26" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-26.png" alt="圆盘左端的极小点与正方形下边的非极小点，说明非负权重和严格正权重的区别" data-source-page="71" data-source-rect="139,120,432,221">
<figcaption>图 2.26 左：点 $x_1\in S_1$ 是极小点，但对于任何 $\lambda\succ 0$，它都不是 $\lambda^Tz$ 在 $S_1$ 上的最小点。（不过，当 $\lambda=(1,0)$ 时，它确实使 $\lambda^Tz$ 在所有 $z\in S_1$ 中取得最小值。）右：点 $x_2\in S_2$ 不是极小点，但当 $\lambda=(0,1)\succeq 0$ 时，它确实使 $\lambda^Tz$ 在所有 $z\in S_2$ 中取得最小值。</figcaption>
</figure>

<div class="example" markdown="1">

**例 2.27 Pareto 最优生产前沿。** 考虑一种制造时需要 $n$ 种资源的产品，例如劳动力、电力、天然气和水。这种产品可以采用许多不同方式制造或生产。对每种生产方式，令它对应一个**资源向量** $x\in\mathbf{R}^n$，其中 $x_i$ 表示该方式制造产品时消耗的第 $i$ 种资源的数量。假设 $x_i\geq0$，即生产方式会消耗资源，并且这些资源都有价值，因此任何一种资源都以少用为好。

**生产集** $P\subseteq\mathbf{R}^n$ 定义为所有与某种生产方式对应的资源向量 $x$ 构成的集合。

如果一种生产方式的资源向量是 $P$ 相对于逐分量不等式的极小元素，就称这种生产方式为 **Pareto 最优的**（Pareto optimal）或**有效的**（efficient）。$P$ 的极小元素集合称为**有效生产前沿**（efficient production frontier）。

可以对 Pareto 最优性给出一个简单解释。如果对所有 $i$ 都有 $x_i\leq y_i$，并且对某个 $i$ 有 $x_i<y_i$，就说资源向量为 $x$ 的生产方式比资源向量为 $y$ 的生产方式更好。换句话说，一种生产方式更好，是指它对每种资源的使用量都不超过另一种方式，并且至少有一种资源用得更少。这对应于 $x\preceq y$、$x\ne y$。于是可以说：如果不存在更好的生产方式，那么该生产方式就是 Pareto 最优的或有效的。

对于任意满足 $\lambda\succ0$ 的 $\lambda$，在生产向量集合 $P$ 上最小化

$$
\lambda^Tx=\lambda_1x_1+\cdots+\lambda_nx_n,
$$

就可以找到 Pareto 最优生产方式，即极小资源向量。

这里向量 $\lambda$ 有一个简单解释：$\lambda_i$ 是第 $i$ 种资源的价格。在 $P$ 上最小化 $\lambda^Tx$，就是按照资源价格 $\lambda_i$，寻找总成本最低的生产方式。只要价格均为正，就能保证所得生产方式是有效的。

图 2.27 展示了这些思想。

</div>

<!-- pdf-page: 72 -->

<figure id="fig-2-27" data-figure="2.27">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-02/fig-2-27.png" alt="以劳动力和燃料消耗为坐标的生产集，包含有效生产前沿、五种生产方式及价格向量" data-source-page="72" data-source-rect="238,259,462,438">
<figcaption>图 2.27 某种产品的生产需要劳动力和燃料，其生产集 $P$ 用阴影表示。两段深色曲线表示有效生产前沿。点 $x_1$、$x_2$ 和 $x_3$ 是有效的，点 $x_4$ 和 $x_5$ 则不是（特别是，$x_2$ 对应的生产方式使用的燃料并不更多，而使用的劳动力更少）。对于价格向量 $\lambda$（各分量均为正），点 $x_1$ 也是成本最低的生产方式。点 $x_2$ 是有效的，但对于任何价格向量 $\lambda\succeq 0$，都无法通过最小化总成本 $\lambda^Tx$ 找到它。</figcaption>
<p class="figure-translation">图内文字：fuel——燃料；labor——劳动力。</p>
</figure>

<!-- pdf-page: 73 -->

## 文献说明

人们通常认为，Minkowski 最早对凸集进行了系统研究，并引入了支撑超平面及支撑超平面定理、Minkowski 距离函数（习题 3.34）、凸集的极点等许多基本概念。

一些著名的早期综述包括 Bonnesen 与 Fenchel [BF48]、Eggleston [Egg58]、Klee [Kle63] 和 Valentine [Val64] 的著作。较新的专门讨论凸集几何的书包括 Lay [Lay82] 和 Webster [Web94]。Klee [Kle71]、Fenchel [Fen83]、Tikhomorov [Tik90] 和 Berger [Ber90] 对凸性的历史及其在数学各领域中的应用，给出了可读性很好的概述。

人们在线性规划问题的背景下，对线性不等式和多面体集合进行了广泛研究；相关参考文献见第 4 章末尾。在线性不等式和线性规划发展史上，具有里程碑意义的著作包括 Motzkin [Mot33]、von Neumann 与 Morgenstern [vNM53]、Kantorovich [Kan60]、Koopmans [Koo51] 和 Dantzig [Dan63]。Dantzig [Dan63, 第 2 章] 包含一篇线性不等式的历史综述，覆盖到约 1963 年。

广义不等式在 20 世纪 60 年代被引入非线性优化，见 Luenberger [Lue69, §8.2] 和 Isii [Isi64]；它们在锥规划中得到广泛使用，相关文献见第 4 章。Bellman 与 Fan [BF63] 是一篇较早研究相对于半正定锥的广义线性不等式组的论文。

关于分离超平面定理的推广和证明，请参阅 Rockafellar [Roc70, 第三部分]，以及 Hiriart-Urruty 与 Lemaréchal [HUL93, 第 1 卷，§III4]。Dantzig [Dan63, 第 21 页] 将“择一定理”（theorem of the alternative）这一术语归于 von Neumann 与 Morgenstern [vNM53, 第 138 页]。关于择一定理的更多参考文献，见第 5 章。

Luenberger [Lue95] 详细讨论了例 2.27 的术语，包括 Pareto 最优性、有效生产以及 $\lambda$ 的价格解释。

凸几何在经典矩理论中发挥着重要作用，见 Krein 与 Nudelman [KN77]、Karlin 与 Studden [KS66]。一个著名例子是非负多项式锥与幂矩锥之间的对偶性，见习题 2.37。

<!-- pdf-page: 74 -->

## 习题

### 凸性的定义

**2.1** 设 $C\subseteq\mathbf{R}^n$ 是凸集，$x_1,\ldots,x_k\in C$，且 $\theta_1,\ldots,\theta_k\in\mathbf{R}$ 满足 $\theta_i\geq0$、$\theta_1+\cdots+\theta_k=1$。证明 $\theta_1x_1+\cdots+\theta_kx_k\in C$。（凸性的定义只要求这一结论在 $k=2$ 时成立；你需要证明它对任意 $k$ 成立。）*提示：* 对 $k$ 使用归纳法。

**2.2** 证明：集合是凸集，当且仅当它与任意直线的交集都是凸集。证明：集合是仿射集，当且仅当它与任意直线的交集都是仿射集。

**2.3 中点凸性。** 如果每当 $a,b\in C$ 时，其平均点或中点 $(a+b)/2$ 也属于 $C$，就称集合 $C$ 是**中点凸的**（midpoint convex）。显然，凸集具有中点凸性。可以证明，在较弱的条件下，中点凸性蕴含凸性。作为一个简单情形，证明：如果 $C$ 是闭集并且具有中点凸性，那么 $C$ 是凸集。

**2.4** 证明：集合 $S$ 的凸包，是所有包含 $S$ 的凸集的交集。（同样的方法也可以证明，集合 $S$ 的锥包、仿射包或线性包，分别是所有包含 $S$ 的锥集、仿射集或子空间的交集。）

### 例子

**2.5** 两个平行超平面 $\{x\in\mathbf{R}^n\mid a^Tx=b_1\}$ 和 $\{x\in\mathbf{R}^n\mid a^Tx=b_2\}$ 之间的距离是多少？

**2.6 一个半空间何时包含另一个半空间？** 给出使下式成立的条件：

$$
\{x\mid a^Tx\leq b\}\subseteq\{x\mid\widetilde{a}^Tx\leq\widetilde{b}\},
$$

其中 $a\ne0$、$\widetilde{a}\ne0$。也求出两个半空间相等的条件。

**2.7 半空间的 Voronoi 描述。** 设 $a$ 和 $b$ 是 $\mathbf{R}^n$ 中两个不同的点。证明：按欧几里得范数衡量，到 $a$ 的距离不大于到 $b$ 的距离的所有点，即 $\{x\mid\|x-a\|_2\leq\|x-b\|_2\}$，构成一个半空间。把它明确写成 $c^Tx\leq d$ 形式的不等式，并画图说明。

**2.8** 以下哪些集合 $S$ 是多面体？如果可能，将 $S$ 写成 $S=\{x\mid Ax\preceq b,\ Fx=g\}$ 的形式。

- (a) $S=\{y_1a_1+y_2a_2\mid-1\leq y_1\leq1,\ -1\leq y_2\leq1\}$，其中 $a_1,a_2\in\mathbf{R}^n$。
- (b) $S=\{x\in\mathbf{R}^n\mid x\succeq0,\ \mathbf{1}^Tx=1,\ \sum_{i=1}^{n}x_ia_i=b_1,\ \sum_{i=1}^{n}x_ia_i^2=b_2\}$，其中 $a_1,\ldots,a_n\in\mathbf{R}$，$b_1,b_2\in\mathbf{R}$。
- (c) $S=\{x\in\mathbf{R}^n\mid x\succeq0,\ \text{对所有满足 }\|y\|_2=1\text{ 的 }y\text{，有 }x^Ty\leq1\}$。
- (d) $S=\{x\in\mathbf{R}^n\mid x\succeq0,\ \text{对所有满足 }\sum_{i=1}^{n}|y_i|=1\text{ 的 }y\text{，有 }x^Ty\leq1\}$。

**2.9 Voronoi 集与多面体分解。** 设 $x_0,\ldots,x_K\in\mathbf{R}^n$ 互不相同。考虑按欧几里得范数衡量，比起其他 $x_i$ 更接近 $x_0$ 的点构成的集合，即

$$
V=\{x\in\mathbf{R}^n\mid\|x-x_0\|_2\leq\|x-x_i\|_2,\ i=1,\ldots,K\}.
$$

$V$ 称为 $x_0$ 相对于 $x_1,\ldots,x_K$ 的 **Voronoi 区域**。

- (a) 证明 $V$ 是多面体，并把 $V$ 写成 $V=\{x\mid Ax\preceq b\}$ 的形式。
- (b) 反过来，给定内部非空的多面体 $P$，说明怎样找到 $x_0,\ldots,x_K$，使这个多面体成为 $x_0$ 相对于 $x_1,\ldots,x_K$ 的 Voronoi 区域。
- (c) 还可以考虑集合

    $$
    V_k=\{x\in\mathbf{R}^n\mid\|x-x_k\|_2\leq\|x-x_i\|_2,\ i\ne k\}.
    $$

    集合 $V_k$ 由 $\mathbf{R}^n$ 中这样的点构成：集合 $\{x_0,\ldots,x_K\}$ 中距离它最近的点是 $x_k$。

    <!-- pdf-page: 75 -->

    集合 $V_0,\ldots,V_K$ 给出了 $\mathbf{R}^n$ 的一个**多面体分解**。更准确地说，各 $V_k$ 是内部非空的多面体，$\bigcup_{k=0}^{K}V_k=\mathbf{R}^n$，并且对于 $i\ne j$，有 $\operatorname{\mathbf{int}}V_i\cap\operatorname{\mathbf{int}}V_j=\varnothing$；也就是说，$V_i$ 和 $V_j$ 至多沿边界相交。

    假设 $P_1,\ldots,P_m$ 是内部非空的多面体，并且 $\bigcup_{i=1}^{m}P_i=\mathbf{R}^n$，对 $i\ne j$ 有 $\operatorname{\mathbf{int}}P_i\cap\operatorname{\mathbf{int}}P_j=\varnothing$。这个 $\mathbf{R}^n$ 的多面体分解，能否表示为某组适当点所生成的 Voronoi 区域？

**2.10 二次不等式的解集。** 设 $C\subseteq\mathbf{R}^n$ 是二次不等式的解集：

$$
C=\{x\in\mathbf{R}^n\mid x^TAx+b^Tx+c\leq0\},
$$

其中 $A\in\mathbf{S}^n$、$b\in\mathbf{R}^n$、$c\in\mathbf{R}$。

- (a) 证明：如果 $A\succeq0$，那么 $C$ 是凸集。
- (b) 证明：如果存在 $\lambda\in\mathbf{R}$，使得 $A+\lambda gg^T\succeq0$，那么 $C$ 与超平面 $g^Tx+h=0$ 的交集是凸集，其中 $g\ne0$。

这些命题的逆命题成立吗？

**2.11 双曲集合。** 证明双曲集合 $\{x\in\mathbf{R}_+^2\mid x_1x_2\geq1\}$ 是凸集。作为推广，证明 $\{x\in\mathbf{R}_+^n\mid\prod_{i=1}^{n}x_i\geq1\}$ 是凸集。*提示：* 如果 $a,b\geq0$ 且 $0\leq\theta\leq1$，那么 $a^\theta b^{1-\theta}\leq\theta a+(1-\theta)b$，见第 3.1.9 节。

**2.12** 以下哪些集合是凸集？

- (a) 条带，即形如 $\{x\in\mathbf{R}^n\mid\alpha\leq a^Tx\leq\beta\}$ 的集合。
- (b) 矩形，即形如 $\{x\in\mathbf{R}^n\mid\alpha_i\leq x_i\leq\beta_i,\ i=1,\ldots,n\}$ 的集合。当 $n>2$ 时，矩形有时称为**超矩形**（hyperrectangle）。
- (c) 楔形区域（wedge），即 $\{x\in\mathbf{R}^n\mid a_1^Tx\leq b_1,\ a_2^Tx\leq b_2\}$。
- (d) 到给定点的距离不大于到给定集合的距离的点集，即

    $$
    \{x\mid\text{对所有 }y\in S\text{，有 }\|x-x_0\|_2\leq\|x-y\|_2\},
    $$

    其中 $S\subseteq\mathbf{R}^n$。

- (e) 到一个集合的距离不大于到另一个集合的距离的点集，即

    $$
    \{x\mid\operatorname{\mathbf{dist}}(x,S)\leq\operatorname{\mathbf{dist}}(x,T)\},
    $$

    其中 $S,T\subseteq\mathbf{R}^n$，并且

    $$
    \operatorname{\mathbf{dist}}(x,S)=\inf\{\|x-z\|_2\mid z\in S\}.
    $$

- (f) [HUL93, 第 1 卷，第 93 页] 集合 $\{x\mid x+S_2\subseteq S_1\}$，其中 $S_1,S_2\subseteq\mathbf{R}^n$，且 $S_1$ 为凸集。
- (g) 到 $a$ 的距离不超过到 $b$ 的距离的一个固定比例 $\theta$ 的点集，即 $\{x\mid\|x-a\|_2\leq\theta\|x-b\|_2\}$。可以假设 $a\ne b$ 且 $0\leq\theta\leq1$。

**2.13 外积的锥包。** 考虑秩为 $k$ 的外积构成的集合，定义为 $\{XX^T\mid X\in\mathbf{R}^{n\times k},\ \operatorname{\mathbf{rank}}X=k\}$。用简单形式描述它的锥包。

**2.14 扩张集与收缩集。** 设 $S\subseteq\mathbf{R}^n$，$\|\cdot\|$ 是 $\mathbf{R}^n$ 上的范数。

- (a) 对 $a\geq0$，定义 $S_a=\{x\mid\operatorname{\mathbf{dist}}(x,S)\leq a\}$，其中 $\operatorname{\mathbf{dist}}(x,S)=\inf_{y\in S}\|x-y\|$。称 $S_a$ 为将 $S$ 扩张或扩展 $a$ 后的集合。证明：如果 $S$ 是凸集，那么 $S_a$ 也是凸集。
- (b) 对 $a\geq0$，定义 $S_{-a}=\{x\mid B(x,a)\subseteq S\}$，其中 $B(x,a)$ 是以 $x$ 为中心、半径为 $a$、按范数 $\|\cdot\|$ 定义的球。称 $S_{-a}$ 为将 $S$ 收缩或限制 $a$ 后的集合，因为 $S_{-a}$ 由距离 $\mathbf{R}^n\setminus S$ 至少为 $a$ 的点构成。证明：如果 $S$ 是凸集，那么 $S_{-a}$ 也是凸集。

<!-- pdf-page: 76 -->

**2.15 一些概率分布集合。** 设 $x$ 是实值随机变量，满足 $\operatorname{\mathbf{prob}}(x=a_i)=p_i$，$i=1,\ldots,n$，其中 $a_1<a_2<\cdots<a_n$。当然，$p\in\mathbf{R}^n$ 位于标准概率单纯形 $P=\{p\mid\mathbf{1}^Tp=1,\ p\succeq0\}$ 中。以下哪些条件关于 $p$ 是凸的？也就是说，对于以下哪些条件，满足条件的 $p\in P$ 构成凸集？

- (a) $\alpha\leq\mathbf{E}f(x)\leq\beta$，其中 $\mathbf{E}f(x)$ 是 $f(x)$ 的期望，即 $\mathbf{E}f(x)=\sum_{i=1}^{n}p_if(a_i)$。函数 $f:\mathbf{R}\to\mathbf{R}$ 已给定。
- (b) $\operatorname{\mathbf{prob}}(x>\alpha)\leq\beta$。
- (c) $\mathbf{E}|x^3|\leq\alpha\mathbf{E}|x|$。
- (d) $\mathbf{E}x^2\leq\alpha$。
- (e) $\mathbf{E}x^2\geq\alpha$。
- (f) $\operatorname{\mathbf{var}}(x)\leq\alpha$，其中 $\operatorname{\mathbf{var}}(x)=\mathbf{E}(x-\mathbf{E}x)^2$ 是 $x$ 的方差。
- (g) $\operatorname{\mathbf{var}}(x)\geq\alpha$。
- (h) $\operatorname{\mathbf{quartile}}(x)\geq\alpha$，其中 $\operatorname{\mathbf{quartile}}(x)=\inf\{\beta\mid\operatorname{\mathbf{prob}}(x\leq\beta)\geq0.25\}$。
- (i) $\operatorname{\mathbf{quartile}}(x)\leq\alpha$。

### 保持凸性的运算

**2.16** 证明：如果 $S_1$ 和 $S_2$ 是 $\mathbf{R}^{m+n}$ 中的凸集，那么它们的部分和

$$
S=\{(x,y_1+y_2)\mid x\in\mathbf{R}^m,\ y_1,y_2\in\mathbf{R}^n,\ (x,y_1)\in S_1,\ (x,y_2)\in S_2\}
$$

也是凸集。

**2.17 多面体集合在透视函数下的像。** 本题研究超平面、半空间和多面体在透视函数 $P(x,t)=x/t$ 下的像，其中 $\operatorname{\mathbf{dom}}P=\mathbf{R}^n\times\mathbf{R}_{++}$。对于下列每个集合 $C$，用简单形式描述

$$
P(C)=\{v/t\mid(v,t)\in C,\ t>0\}.
$$

- (a) 多面体 $C=\operatorname{\mathbf{conv}}\{(v_1,t_1),\ldots,(v_K,t_K)\}$，其中 $v_i\in\mathbf{R}^n$ 且 $t_i>0$。
- (b) 超平面 $C=\{(v,t)\mid f^Tv+gt=h\}$，其中 $f$ 与 $g$ 不同时为零。
- (c) 半空间 $C=\{(v,t)\mid f^Tv+gt\leq h\}$，其中 $f$ 与 $g$ 不同时为零。
- (d) 多面体 $C=\{(v,t)\mid Fv+gt\preceq h\}$。

**2.18 可逆线性分式函数。** 设 $f:\mathbf{R}^n\to\mathbf{R}^n$ 是线性分式函数

$$
f(x)=(Ax+b)/(c^Tx+d),\qquad\operatorname{\mathbf{dom}}f=\{x\mid c^Tx+d>0\}.
$$

假设矩阵

$$
Q=\begin{bmatrix}A&b\\c^T&d\end{bmatrix}
$$

非奇异。证明 $f$ 可逆，并且 $f^{-1}$ 是线性分式映射。用 $A,b,c,d$ 给出 $f^{-1}$ 及其定义域的显式表达式。*提示：* 用 $Q$ 表示 $f^{-1}$ 可能更容易。

**2.19 线性分式函数与凸集。** 设 $f:\mathbf{R}^m\to\mathbf{R}^n$ 是线性分式函数

$$
f(x)=(Ax+b)/(c^Tx+d),\qquad\operatorname{\mathbf{dom}}f=\{x\mid c^Tx+d>0\}.
$$

本题研究凸集 $C$ 在 $f$ 下的原像，即

$$
f^{-1}(C)=\{x\in\operatorname{\mathbf{dom}}f\mid f(x)\in C\}.
$$

对于下列每个集合 $C\subseteq\mathbf{R}^n$，用简单形式描述 $f^{-1}(C)$。

- (a) 半空间 $C=\{y\mid g^Ty\leq h\}$，其中 $g\ne0$。
- (b) 多面体 $C=\{y\mid Gy\preceq h\}$。
- (c) 椭球 $\{y\mid y^TP^{-1}y\leq1\}$，其中 $P\in\mathbf{S}_{++}^n$。
- (d) 线性矩阵不等式的解集 $C=\{y\mid y_1A_1+\cdots+y_nA_n\preceq B\}$，其中 $A_1,\ldots,A_n,B\in\mathbf{S}^p$。

<!-- pdf-page: 77 -->

### 分离定理与支撑超平面

**2.20 线性方程组的严格正解。** 设 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，且 $b\in\mathcal{R}(A)$。证明：存在 $x$ 满足

$$
x\succ0,\qquad Ax=b,
$$

当且仅当不存在 $\lambda$ 满足

$$
A^T\lambda\succeq0,\qquad A^T\lambda\ne0,\qquad b^T\lambda\leq0.
$$

*提示：* 先证明下面这个线性代数事实：对于所有满足 $Ax=b$ 的 $x$，都有 $c^Tx=d$，当且仅当存在向量 $\lambda$，使得 $c=A^T\lambda$、$d=b^T\lambda$。

**2.21 分离超平面的集合。** 设 $C$ 和 $D$ 是 $\mathbf{R}^n$ 中不相交的子集。考虑满足以下条件的 $(a,b)\in\mathbf{R}^{n+1}$ 所构成的集合：对所有 $x\in C$ 有 $a^Tx\leq b$，对所有 $x\in D$ 有 $a^Tx\geq b$。证明这个集合是凸锥；如果没有超平面能够分离 $C$ 与 $D$，它就是单点集 $\{0\}$。

**2.22** 补全第 2.5.1 节中分离超平面定理的证明：证明任意两个不相交凸集 $C$ 和 $D$ 都存在分离超平面。可以使用第 2.5.1 节已经证明的结果，即当两个集合中存在一对点，其距离等于两个集合之间的距离时，分离超平面存在。

*提示：* 如果 $C$ 和 $D$ 是不相交凸集，那么集合 $\{x-y\mid x\in C,\ y\in D\}$ 是凸集，并且不包含原点。

**2.23** 给出两个闭凸集的例子，使它们不相交，却不能被严格分离。

**2.24 支撑超平面。**

- (a) 把闭凸集 $\{x\in\mathbf{R}_+^2\mid x_1x_2\geq1\}$ 表示为半空间的交集。
- (b) 设 $C=\{x\in\mathbf{R}^n\mid\|x\|_\infty\leq1\}$ 是 $\mathbf{R}^n$ 中的 $\ell_\infty$ 范数单位球，$\widehat{x}$ 是 $C$ 的边界上的一点。明确给出 $C$ 在 $\widehat{x}$ 处的支撑超平面。

**2.25 内外多面体逼近。** 设 $C\subseteq\mathbf{R}^n$ 是闭凸集，$x_1,\ldots,x_K$ 位于 $C$ 的边界上。假设对每个 $i$，$a_i^T(x-x_i)=0$ 定义了 $C$ 在 $x_i$ 处的支撑超平面，即 $C\subseteq\{x\mid a_i^T(x-x_i)\leq0\}$。考虑两个多面体

$$
P_{\mathrm{inner}}=\operatorname{\mathbf{conv}}\{x_1,\ldots,x_K\},\qquad P_{\mathrm{outer}}=\{x\mid a_i^T(x-x_i)\leq0,\ i=1,\ldots,K\}.
$$

证明 $P_{\mathrm{inner}}\subseteq C\subseteq P_{\mathrm{outer}}$，并画图说明。

**2.26 支撑函数。** 集合 $C\subseteq\mathbf{R}^n$ 的**支撑函数**（support function）定义为

$$
S_C(y)=\sup\{y^Tx\mid x\in C\}.
$$

允许 $S_C(y)$ 取值 $+\infty$。设 $C$ 和 $D$ 是 $\mathbf{R}^n$ 中的闭凸集。证明：$C=D$ 当且仅当它们的支撑函数相等。

**2.27 支撑超平面定理的逆命题。** 假设集合 $C$ 是闭集、内部非空，并且在边界的每一点都有支撑超平面。证明 $C$ 是凸集。

### 凸锥与广义不等式

**2.28 $n=1,2,3$ 时的半正定锥。** 对于 $n=1,2,3$，用矩阵元素和普通不等式显式描述半正定锥 $\mathbf{S}_+^n$。分别用以下记号表示 $n=1,2,3$ 时 $\mathbf{S}^n$ 的一般元素：

$$
x_1,\qquad\begin{bmatrix}x_1&x_2\\x_2&x_3\end{bmatrix},\qquad\begin{bmatrix}x_1&x_2&x_3\\x_2&x_4&x_5\\x_3&x_5&x_6\end{bmatrix}.
$$

<!-- pdf-page: 78 -->

**2.29 $\mathbf{R}^2$ 中的锥。** 设 $K\subseteq\mathbf{R}^2$ 是闭凸锥。

- (a) 用 $K$ 中元素的极坐标给出 $K$ 的简单描述，其中 $x=r(\cos\varphi,\sin\varphi)$，$r\geq0$。
- (b) 给出 $K^*$ 的简单描述，并画图说明 $K$ 与 $K^*$ 的关系。
- (c) $K$ 何时是尖的？
- (d) $K$ 何时是正常锥，从而定义一个广义不等式？画图说明在 $K$ 是正常锥时，$x\preceq_K y$ 的含义。

**2.30 广义不等式的性质。** 证明第 2.4.1 节列出的非严格和严格广义不等式的性质。

**2.31 对偶锥的性质。** 设 $K^*$ 是凸锥 $K$ 的对偶锥，定义如 (2.19)。证明以下结论。

- (a) $K^*$ 确实是凸锥。
- (b) $K_1\subseteq K_2$ 蕴含 $K_2^*\subseteq K_1^*$。
- (c) $K^*$ 是闭集。
- (d) $K^*$ 的内部为 $\operatorname{\mathbf{int}}K^*=\{y\mid\text{对所有 }x\in\operatorname{\mathbf{cl}}K\text{，有 }y^Tx>0\}$。
- (e) 如果 $K$ 的内部非空，那么 $K^*$ 是尖的。
- (f) $K^{**}$ 是 $K$ 的闭包。因此，如果 $K$ 是闭集，则 $K^{**}=K$。
- (g) 如果 $K$ 的闭包是尖的，那么 $K^*$ 的内部非空。

<div class="translator-note" markdown="1">

**译注（习题 2.31(d)）：** 当 $K$ 非空时，它的闭包中含有零向量，而 $y^T0=0$。因此，式中的严格不等式应只对 $\operatorname{\mathbf{cl}}K$ 中的非零向量要求。

</div>

**2.32** 求锥 $\{Ax\mid x\succeq0\}$ 的对偶锥，其中 $A\in\mathbf{R}^{m\times n}$。

**2.33 单调非负锥。** 定义**单调非负锥**（monotone nonnegative cone）为

$$
K_{\mathrm{m+}}=\{x\in\mathbf{R}^n\mid x_1\geq x_2\geq\cdots\geq x_n\geq0\},
$$

即所有分量按非增顺序排列的非负向量。

- (a) 证明 $K_{\mathrm{m+}}$ 是正常锥。
- (b) 求对偶锥 $K_{\mathrm{m+}}^*$。*提示：* 使用恒等式

    $$
    \begin{aligned}
    \sum_{i=1}^{n}x_iy_i={}&(x_1-x_2)y_1+(x_2-x_3)(y_1+y_2)+(x_3-x_4)(y_1+y_2+y_3)+\cdots\\
    &+(x_{n-1}-x_n)(y_1+\cdots+y_{n-1})+x_n(y_1+\cdots+y_n).
    \end{aligned}
    $$

**2.34 字典序锥与字典序。** **字典序锥**（lexicographic cone）定义为

$$
K_{\mathrm{lex}}=\{0\}\cup\{x\in\mathbf{R}^n\mid\text{存在 }0\leq k<n\text{，使 }x_1=\cdots=x_k=0,\ x_{k+1}>0\},
$$

即首个非零分量为正的所有向量，并包括没有非零分量的零向量。

- (a) 验证 $K_{\mathrm{lex}}$ 是锥，但不是正常锥。
- (b) 定义 $\mathbf{R}^n$ 上的**字典序**（lexicographic ordering）如下：$x\leq_{\mathrm{lex}}y$ 当且仅当 $y-x\in K_{\mathrm{lex}}$。由于 $K_{\mathrm{lex}}$ 不是正常锥，字典序不是广义不等式。证明字典序是全序：对于任意 $x,y\in\mathbf{R}^n$，必有 $x\leq_{\mathrm{lex}}y$ 或 $y\leq_{\mathrm{lex}}x$。因此，任何向量集合都可以按照字典序锥排序，得到的就是熟悉的字典排序方式。
- (c) 求 $K_{\mathrm{lex}}^*$。

**2.35 共正矩阵。** 如果矩阵 $X\in\mathbf{S}^n$ 对所有 $z\succeq0$ 都满足 $z^TXz\geq0$，就称 $X$ 是**共正的**（copositive）。验证共正矩阵集合是正常锥，并求出它的对偶锥。

<!-- pdf-page: 79 -->

**2.36 欧几里得距离矩阵。** 设 $x_1,\ldots,x_n\in\mathbf{R}^k$。由 $D_{ij}=\|x_i-x_j\|_2^2$ 定义的矩阵 $D\in\mathbf{S}^n$，称为**欧几里得距离矩阵**（Euclidean distance matrix）。它满足一些显然的性质，例如 $D_{ij}=D_{ji}$、$D_{ii}=0$、$D_{ij}\geq0$；由三角不等式还可得 $D_{ik}^{1/2}\leq D_{ij}^{1/2}+D_{jk}^{1/2}$。

现在提出一个问题：矩阵 $D\in\mathbf{S}^n$ 何时是某个 $k$ 下、$\mathbf{R}^k$ 中某些点的欧几里得距离矩阵？一个著名结果回答了这一问题：$D\in\mathbf{S}^n$ 是欧几里得距离矩阵，当且仅当 $D_{ii}=0$，并且对所有满足 $\mathbf{1}^Tx=0$ 的 $x$，都有 $x^TDx\leq0$，见第 8.3.3 节。

证明欧几里得距离矩阵集合是凸锥。

**2.37 非负多项式与 Hankel 线性矩阵不等式。** 设 $K_{\mathrm{pol}}$ 是 $\mathbf{R}$ 上非负的 $2k$ 次多项式的系数所构成的集合：

$$
K_{\mathrm{pol}}=\{x\in\mathbf{R}^{2k+1}\mid\text{对所有 }t\in\mathbf{R}\text{，有 }x_1+x_2t+x_3t^2+\cdots+x_{2k+1}t^{2k}\geq0\}.
$$

- (a) 证明 $K_{\mathrm{pol}}$ 是正常锥。
- (b) 一个基本结果指出：一个 $2k$ 次多项式在 $\mathbf{R}$ 上非负，当且仅当它可以写成两个次数不超过 $k$ 的多项式的平方和。换句话说，$x\in K_{\mathrm{pol}}$ 当且仅当多项式

    $$
    p(t)=x_1+x_2t+x_3t^2+\cdots+x_{2k+1}t^{2k}
    $$

    可以表示为

    $$
    p(t)=r(t)^2+s(t)^2,
    $$

    其中 $r$ 和 $s$ 是 $k$ 次多项式。

    利用这个结果证明

    $$
    K_{\mathrm{pol}}=\left\{x\in\mathbf{R}^{2k+1}\ \middle|\ \text{存在 }Y\in\mathbf{S}_+^{k+1}\text{，使 }x_i=\sum_{m+n=i+1}Y_{mn}\right\}.
    $$

    换句话说，$p(t)=x_1+x_2t+x_3t^2+\cdots+x_{2k+1}t^{2k}$ 非负，当且仅当存在矩阵 $Y\in\mathbf{S}_+^{k+1}$，使得

    $$
    \begin{aligned}
    x_1&=Y_{11}\\
    x_2&=Y_{12}+Y_{21}\\
    x_3&=Y_{13}+Y_{22}+Y_{31}\\
    &\ \vdots\\
    x_{2k+1}&=Y_{k+1,k+1}.
    \end{aligned}
    $$

- (c) 证明 $K_{\mathrm{pol}}^*=K_{\mathrm{han}}$，其中

    $$
    K_{\mathrm{han}}=\{z\in\mathbf{R}^{2k+1}\mid H(z)\succeq0\},
    $$

    并且

    $$
    H(z)=\begin{bmatrix}
    z_1&z_2&z_3&\cdots&z_k&z_{k+1}\\
    z_2&z_3&z_4&\cdots&z_{k+1}&z_{k+2}\\
    z_3&z_4&z_5&\cdots&z_{k+2}&z_{k+4}\\
    \vdots&\vdots&\vdots&\ddots&\vdots&\vdots\\
    z_k&z_{k+1}&z_{k+2}&\cdots&z_{2k-1}&z_{2k}\\
    z_{k+1}&z_{k+2}&z_{k+3}&\cdots&z_{2k}&z_{2k+1}
    \end{bmatrix}.
    $$

    这就是以 $z_1,\ldots,z_{2k+1}$ 为系数的 Hankel 矩阵。

- (d) <!-- pdf-page: 80 -->设 $K_{\mathrm{mom}}$ 是所有形如 $(1,t,t^2,\ldots,t^{2k})$、其中 $t\in\mathbf{R}$ 的向量所构成的集合的锥包。证明 $y\in K_{\mathrm{mom}}$ 当且仅当 $y_1\geq0$，并且对某个随机变量 $u$ 有

    $$
    y=y_1(1,\mathbf{E}u,\mathbf{E}u^2,\ldots,\mathbf{E}u^{2k}).
    $$

    换句话说，$K_{\mathrm{mom}}$ 的元素是 $\mathbf{R}$ 上所有可能分布的矩向量的非负倍数。证明 $K_{\mathrm{pol}}=K_{\mathrm{mom}}^*$。

- (e) 结合 (c) 和 (d) 的结果，推出 $K_{\mathrm{han}}=\operatorname{\mathbf{cl}}K_{\mathrm{mom}}$。

    作为说明 $K_{\mathrm{mom}}$ 与 $K_{\mathrm{han}}$ 之间关系的例子，取 $k=2$，$z=(1,0,0,0,1)$。证明 $z\in K_{\mathrm{han}}$、$z\notin K_{\mathrm{mom}}$。显式构造一个 $K_{\mathrm{mom}}$ 中的点列，使它收敛到 $z$。

<div class="translator-note" markdown="1">

**译注（习题 2.37(c)）：** Hankel 矩阵沿反对角线取值相同，这里应满足 $H_{ij}(z)=z_{i+j-1}$。按此规律，第三行最后一项应为 $z_{k+3}$，与其对称位置一致；上面的原式写作 $z_{k+4}$。

</div>

**2.38** [Roc70, 第 15、61 页] **由集合构造凸锥。**

- (a) 集合 $C$ 的**障碍锥**（barrier cone）定义为所有使 $y^Tx$ 在 $x\in C$ 上有上界的向量 $y$ 构成的集合。换句话说，非零向量 $y$ 属于障碍锥，当且仅当它是某个包含 $C$ 的半空间 $\{x\mid y^Tx\leq\alpha\}$ 的法向量。验证障碍锥是凸锥，不需要对 $C$ 作任何假设。
- (b) 集合 $C$ 的**衰退锥**（recession cone，也称**渐近锥**，asymptotic cone）定义为所有满足以下条件的向量 $y$：对每个 $x\in C$ 和所有 $t\geq0$，都有 $x-ty\in C$。证明凸集的衰退锥是凸锥。证明：如果 $C$ 非空、闭且凸，那么 $C$ 的衰退锥是障碍锥的对偶。
- (c) 集合 $C$ 在边界点 $x_0$ 处的**法锥**（normal cone）是所有满足以下条件的向量 $y$ 构成的集合：对所有 $x\in C$ 都有 $y^T(x-x_0)\leq0$；也就是所有在 $x_0$ 处为 $C$ 定义支撑超平面的向量。证明法锥是凸锥，不需要对 $C$ 作任何假设。用简单形式描述多面体 $\{x\mid Ax\preceq b\}$ 在其某个边界点处的法锥。

**2.39 锥的分离。** 设 $K$ 和 $\widetilde{K}$ 是两个凸锥，它们的内部均非空且彼此不相交。证明：存在非零 $y$，使得 $y\in K^*$、$-y\in\widetilde{K}^*$。
