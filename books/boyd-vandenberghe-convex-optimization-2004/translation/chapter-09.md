<!-- pdf-page: 471 -->

# 第 9 章 无约束最小化

<aside class="chapter-guide"><p>导读（编者）：本章开始讨论怎样实际求解凸优化问题。先从无约束最小化出发，说明梯度、Hessian 矩阵和下水平集的形状如何影响误差与收敛速度，再介绍下降方向、步长选择、梯度下降、最速下降和牛顿法。阅读算法时，可以对照每一步需要计算什么，以及哪些条件保证目标值继续下降。后面的自协调性分析和实现讨论，进一步说明牛顿法的收敛保证与计算代价。</p></aside>

## 9.1 无约束最小化问题

本章讨论求解无约束优化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)
\end{array}
\tag{9.1}
$$

的方法，其中 $f:\mathbf{R}^n\to\mathbf{R}$ 为凸函数，且二阶连续可微（这意味着 $\mathbf{dom}\,f$ 是开集）。我们假设问题可解，即存在最优点 $x^\star$。（更确切地说，本章后面引入的假设将保证 $x^\star$ 存在且唯一。）将最优值 $\inf_x f(x)=f(x^\star)$ 记为 $p^\star$。

由于 $f$ 可微且凸，点 $x^\star$ 最优的充要条件为

$$
\nabla f(x^\star)=0
\tag{9.2}
$$

（见 §4.2.3）。因此，求解无约束最小化问题 (9.1)，等价于求解 (9.2)；后者是关于 $n$ 个变量 $x_1,\ldots,x_n$ 的 $n$ 个方程。在少数特殊情况下，可以通过解析地求解最优性方程 (9.2)，得到问题 (9.1) 的解；但通常必须使用迭代算法。这里的迭代算法，是指计算点列 $x^{(0)},x^{(1)},\ldots\in\mathbf{dom}\,f$，使得当 $k\to\infty$ 时 $f(x^{(k)})\to p^\star$ 的算法。这样的点列称为问题 (9.1) 的*最小化序列*（minimizing sequence）。当 $f(x^{(k)})-p^\star\leq\epsilon$ 时终止算法，其中 $\epsilon>0$ 是给定的容差。

#### 初始点与下水平集

本章介绍的方法需要一个合适的初始点 $x^{(0)}$。初始点必须属于 $\mathbf{dom}\,f$，此外，下水平集

$$
S=\{x\in\mathbf{dom}\,f\mid f(x)\leq f(x^{(0)})\}
\tag{9.3}
$$

必须为闭集。如果 $f$ 是*闭函数*，即它的所有下水平集都闭（见 §A.3.3），那么对任意 $x^{(0)}\in\mathbf{dom}\,f$，这一条件都成立。满足<!-- pdf-page: 472 -->$\mathbf{dom}\,f=\mathbf{R}^n$ 的连续函数都是闭函数，因此，如果 $\mathbf{dom}\,f=\mathbf{R}^n$，任意 $x^{(0)}$ 都满足初始下水平集的条件。另一类重要的闭函数，是具有开定义域的连续函数，并且当 $x$ 趋近 $\mathbf{bd}\,\mathbf{dom}\,f$ 时，$f(x)$ 趋于无穷大。

### 9.1.1 例子

#### 二次最小化与最小二乘

一般的凸二次最小化问题具有如下形式：

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r,
\end{array}
\tag{9.4}
$$

其中 $P\in\mathbf{S}_+^n$、$q\in\mathbf{R}^n$、$r\in\mathbf{R}$。这个问题可以通过最优性条件 $Px^\star+q=0$ 求解，这是一组线性方程。当 $P\succ0$ 时，解唯一，为 $x^\star=-P^{-1}q$。在 $P$ 不是正定矩阵的更一般情形中，$Px^\star=-q$ 的任何解都是 (9.4) 的最优解；如果 $Px^\star=-q$ 无解，那么问题 (9.4) 无下界（见习题 9.1）。能够解析地求解二次最小化问题 (9.4)，是牛顿法的基础；牛顿法是一种强有力的无约束最小化方法，将在 §9.5 中介绍。

二次最小化问题中一个非常常见的特例，是最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2=x^T(A^TA)x-2(A^Tb)^Tx+b^Tb.
\end{array}
$$

最优性条件

$$
A^TAx^\star=A^Tb
$$

称为最小二乘问题的*正规方程*。

#### 无约束几何规划

作为第二个例子，考虑凸形式的无约束几何规划：

$$
\begin{array}{ll}
\text{最小化} & f(x)=\log\left(\sum_{i=1}^m\exp(a_i^Tx+b_i)\right).
\end{array}
$$

最优性条件为

$$
\nabla f(x^\star)=\frac{1}{\sum_{j=1}^m\exp(a_j^Tx^\star+b_j)}\sum_{i=1}^m\exp(a_i^Tx^\star+b_i)a_i=0,
$$

一般没有解析解，因此这里必须使用迭代算法。对这个问题，$\mathbf{dom}\,f=\mathbf{R}^n$，所以可以选择任意点作为初始点 $x^{(0)}$。

#### 线性不等式的解析中心

考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx),
\end{array}
\tag{9.5}
$$

<!-- pdf-page: 473 -->

其中 $f$ 的定义域是开集

$$
\mathbf{dom}\,f=\{x\mid a_i^Tx<b_i,\ i=1,\ldots,m\}.
$$

这个问题的目标函数 $f$ 称为不等式 $a_i^Tx\leq b_i$ 的*对数障碍函数*。如果 (9.5) 的解存在，则称其为这些不等式的*解析中心*。初始点 $x^{(0)}$ 必须满足严格不等式 $a_i^Tx^{(0)}<b_i$，$i=1,\ldots,m$。由于 $f$ 是闭函数，任何这样的点所对应的下水平集 $S$ 都是闭集。

#### 线性矩阵不等式的解析中心

一个密切相关的问题是

$$
\begin{array}{ll}
\text{最小化} & f(x)=\log\det F(x)^{-1}
\end{array}
\tag{9.6}
$$

其中 $F:\mathbf{R}^n\to\mathbf{S}^p$ 为仿射函数，即

$$
F(x)=F_0+x_1F_1+\cdots+x_nF_n,
$$

且 $F_i\in\mathbf{S}^p$。这里 $f$ 的定义域为

$$
\mathbf{dom}\,f=\{x\mid F(x)\succ0\}.
$$

目标函数 $f$ 称为线性矩阵不等式 $F(x)\succeq0$ 的*对数障碍函数*，其解（如果存在）称为该线性矩阵不等式的*解析中心*。初始点 $x^{(0)}$ 必须满足严格线性矩阵不等式 $F(x^{(0)})\succ0$。与上一个例子一样，由于 $f$ 是闭函数，任何这样的点所对应的下水平集都闭。

### 9.1.2 强凸性及其推论

在本章的大部分内容中（§9.6 除外），我们假设目标函数在 $S$ 上*强凸*（strongly convex），即存在 $m>0$，使得对所有 $x\in S$，都有

$$
\nabla^2f(x)\succeq mI.
\tag{9.7}
$$

强凸性有几个有趣的推论。对 $x,y\in S$，有

$$
f(y)=f(x)+\nabla f(x)^T(y-x)+\frac{1}{2}(y-x)^T\nabla^2f(z)(y-x),
$$

其中 $z$ 是线段 $[x,y]$ 上的某个点。根据强凸性假设 (9.7)，右端最后一项至少为 $(m/2)\|y-x\|_2^2$，因此，对 $S$ 中所有的 $x$ 和 $y$，都有不等式

$$
f(y)\geq f(x)+\nabla f(x)^T(y-x)+\frac{m}{2}\|y-x\|_2^2.
\tag{9.8}
$$

当 $m=0$ 时，就得到刻画凸性的基本不等式；当 $m>0$ 时，这给出的 $f(y)$ 下界比仅根据凸性得到的下界更好。

<!-- pdf-page: 474 -->

我们先证明：利用不等式 (9.8)，可以根据 $\|\nabla f(x)\|_2$ 给出 $f(x)-p^\star$ 的界，后者就是点 $x$ 的次优程度。在固定 $x$ 时，(9.8) 的右端是 $y$ 的凸二次函数。令它对 $y$ 的梯度为零，得到 $\widetilde y=x-(1/m)\nabla f(x)$，它使右端最小。因此有

$$
\begin{aligned}
f(y)&\geq f(x)+\nabla f(x)^T(y-x)+\frac{m}{2}\|y-x\|_2^2\\
&\geq f(x)+\nabla f(x)^T(\widetilde y-x)+\frac{m}{2}\|\widetilde y-x\|_2^2\\
&=f(x)-\frac{1}{2m}\|\nabla f(x)\|_2^2.
\end{aligned}
$$

由于这对任意 $y\in S$ 都成立，得到

$$
p^\star\geq f(x)-\frac{1}{2m}\|\nabla f(x)\|_2^2.
\tag{9.9}
$$

这个不等式说明，如果某一点处的梯度很小，那么该点就接近最优。不等式 (9.9) 也可以解释为一个次优性条件，它推广了最优性条件 (9.2)：

$$
\|\nabla f(x)\|_2\leq(2m\epsilon)^{1/2}\quad\Longrightarrow\quad f(x)-p^\star\leq\epsilon.
\tag{9.10}
$$

还可以根据 $\|\nabla f(x)\|_2$，推导出 $x$ 到任意最优点 $x^\star$ 的距离 $\|x-x^\star\|_2$ 的一个界：

$$
\|x-x^\star\|_2\leq\frac{2}{m}\|\nabla f(x)\|_2.
\tag{9.11}
$$

为此，在 (9.8) 中取 $y=x^\star$，得到

$$
\begin{aligned}
p^\star=f(x^\star)&\geq f(x)+\nabla f(x)^T(x^\star-x)+\frac{m}{2}\|x^\star-x\|_2^2\\
&\geq f(x)-\|\nabla f(x)\|_2\|x^\star-x\|_2+\frac{m}{2}\|x^\star-x\|_2^2,
\end{aligned}
$$

其中第二个不等式使用了 Cauchy-Schwarz 不等式。由于 $p^\star\leq f(x)$，必有

$$
-\|\nabla f(x)\|_2\,\|x^\star-x\|_2+\frac{m}{2}\|x^\star-x\|_2^2\leq0,
$$

由此得到 (9.11)。(9.11) 的一个推论是，最优点 $x^\star$ 唯一。

#### $\nabla^2f(x)$ 的上界

不等式 (9.8) 意味着，包含在 $S$ 内的下水平集有界；特别地，$S$ 有界。因此，$\nabla^2f(x)$ 的最大特征值，作为 $S$ 上关于 $x$ 的连续函数，在 $S$ 上有上界；也就是说，存在常数 $M$，使得

$$
\nabla^2f(x)\preceq MI
\tag{9.12}
$$

<!-- pdf-page: 475 -->

对所有 $x\in S$ 都成立。Hessian 矩阵的这个上界意味着，对任意 $x,y\in S$，有

$$
f(y)\leq f(x)+\nabla f(x)^T(y-x)+\frac{M}{2}\|y-x\|_2^2,
\tag{9.13}
$$

它与 (9.8) 类似。两边分别对 $y$ 最小化，得到

$$
p^\star\leq f(x)-\frac{1}{2M}\|\nabla f(x)\|_2^2,
\tag{9.14}
$$

这是与 (9.9) 对应的不等式。

#### 下水平集的条件数

由强凸性不等式 (9.7) 和不等式 (9.12)，对所有 $x\in S$，有

$$
mI\preceq\nabla^2f(x)\preceq MI.
\tag{9.15}
$$

因此，比值 $\kappa=M/m$ 是矩阵 $\nabla^2f(x)$ 的条件数的一个上界，这里的条件数是其最大特征值与最小特征值之比。还可以用 $f$ 的下水平集，为 (9.15) 给出一个几何解释。

凸集 $C\subseteq\mathbf{R}^n$ 在方向 $q$（$\|q\|_2=1$）上的*宽度*定义为

$$
W(C,q)=\sup_{z\in C}q^Tz-\inf_{z\in C}q^Tz.
$$

$C$ 的*最小宽度*和*最大宽度*为

$$
W_{\min}=\inf_{\|q\|_2=1}W(C,q),\qquad W_{\max}=\sup_{\|q\|_2=1}W(C,q).
$$

凸集 $C$ 的*条件数*定义为

$$
\mathbf{cond}(C)=\frac{W_{\max}^2}{W_{\min}^2},
$$

即最大宽度与最小宽度之比的平方。$C$ 的条件数衡量其各向异性或偏心程度。如果集合 $C$ 的条件数很小（例如接近 $1$），就意味着这个集合在各个方向上的宽度大致相同，即它接近球形。如果条件数很大，则意味着它在某些方向上远比其他方向宽。

<div class="example" markdown="1">

**例 9.1 椭球的条件数。** 设 $\mathcal{E}$ 为椭球

$$
\mathcal{E}=\{x\mid(x-x_0)^TA^{-1}(x-x_0)\leq1\},
$$

其中 $A\in\mathbf{S}_{++}^n$。$\mathcal{E}$ 在方向 $q$ 上的宽度为

$$
\begin{aligned}
\sup_{z\in\mathcal{E}}q^Tz-\inf_{z\in\mathcal{E}}q^Tz
&=(\|A^{1/2}q\|_2+q^Tx_0)-(-\|A^{1/2}q\|_2+q^Tx_0)\\
&=2\|A^{1/2}q\|_2.
\end{aligned}
$$

<!-- pdf-page: 476 -->

因此，它的最小宽度与最大宽度为

$$
W_{\min}=2\lambda_{\min}(A)^{1/2},\qquad W_{\max}=2\lambda_{\max}(A)^{1/2},
$$

条件数为

$$
\mathbf{cond}(\mathcal{E})=\frac{\lambda_{\max}(A)}{\lambda_{\min}(A)}=\kappa(A),
$$

其中 $\kappa(A)$ 表示矩阵 $A$ 的条件数，即其最大奇异值与最小奇异值之比。因此，椭球 $\mathcal{E}$ 的条件数等于定义它的矩阵 $A$ 的条件数。

</div>

现在假设 $f$ 对所有 $x\in S$ 都满足 $mI\preceq\nabla^2f(x)\preceq MI$。我们将推导 $\alpha$-下水平集 $C_\alpha=\{x\mid f(x)\leq\alpha\}$ 的条件数的界，其中 $p^\star<\alpha\leq f(x^{(0)})$。在 (9.13) 和 (9.8) 中取 $x=x^\star$，得到

$$
p^\star+(M/2)\|y-x^\star\|_2^2\geq f(y)\geq p^\star+(m/2)\|y-x^\star\|_2^2.
$$

这意味着 $B_{\mathrm{inner}}\subseteq C_\alpha\subseteq B_{\mathrm{outer}}$，其中

$$
\begin{aligned}
B_{\mathrm{inner}}&=\{y\mid\|y-x^\star\|_2\leq(2(\alpha-p^\star)/M)^{1/2}\},\\
B_{\mathrm{outer}}&=\{y\mid\|y-x^\star\|_2\leq(2(\alpha-p^\star)/m)^{1/2}\}.
\end{aligned}
$$

换言之，$\alpha$-下水平集包含 $B_{\mathrm{inner}}$，并且包含在 $B_{\mathrm{outer}}$ 内；这两个球的半径分别为

$$
(2(\alpha-p^\star)/M)^{1/2},\qquad (2(\alpha-p^\star)/m)^{1/2}.
$$

半径之比的平方给出 $C_\alpha$ 的条件数的一个上界：

$$
\mathbf{cond}(C_\alpha)\leq\frac{M}{m}.
$$

还可以对最优点处 Hessian 矩阵的条件数 $\kappa(\nabla^2f(x^\star))$ 给出几何解释。由 $f$ 在 $x^\star$ 附近的 Taylor 展开

$$
f(y)\approx p^\star+\frac{1}{2}(y-x^\star)^T\nabla^2f(x^\star)(y-x^\star),
$$

可知，当 $\alpha$ 接近 $p^\star$ 时，

$$
C_\alpha\approx\{y\mid(y-x^\star)^T\nabla^2f(x^\star)(y-x^\star)\leq2(\alpha-p^\star)\},
$$

即这个下水平集可以用一个以 $x^\star$ 为中心的椭球很好地逼近。因此

$$
\lim_{\alpha\to p^\star}\mathbf{cond}(C_\alpha)=\kappa(\nabla^2f(x^\star)).
$$

我们将看到，$f$ 的下水平集的条件数（其上界为 $M/m$），会显著影响一些常见无约束最小化方法的效率。

<!-- pdf-page: 477 -->

#### 强凸性常数

必须牢记，只有在少数情况下才知道常数 $m$ 和 $M$，所以不等式 (9.10) 不能作为实际的停止准则。可以把它看作概念上的停止准则：它表明，如果 $f$ 在 $x$ 处的梯度足够小，那么 $f(x)$ 与 $p^\star$ 之差就很小。如果在 $\|\nabla f(x^{(k)})\|_2\leq\eta$ 时终止算法，并且将 $\eta$ 选得足够小，使其极有可能小于 $(m\epsilon)^{1/2}$，那么就极有可能有 $f(x^{(k)})-p^\star\leq\epsilon$。

在接下来的各节中，我们将证明算法的收敛性，并给出达到 $f(x^{(k)})-p^\star\leq\epsilon$ 所需迭代次数的界，其中 $\epsilon$ 是某个正容差。许多这样的界都涉及通常未知的常数 $m$ 和 $M$，所以上述说明同样适用。这些结果至少在概念上是有用的：它们确立了算法的收敛性，即使达到给定精度所需的迭代次数界依赖于未知常数。

我们将遇到一个重要的例外。在 §9.6 中，将研究一类特殊的凸函数，称为*自协调函数*（self-concordant functions）。对这一类函数，可以给出不依赖任何未知常数的完整牛顿法收敛性分析。

## 9.2 下降法

本章介绍的算法产生最小化序列 $x^{(k)}$，$k=1,\ldots$，其中

$$
x^{(k+1)}=x^{(k)}+t^{(k)}\Delta x^{(k)},
$$

并且 $t^{(k)}>0$（除非 $x^{(k)}$ 已经最优）。这里，组成 $\Delta x$ 的两个相连符号 $\Delta$ 和 $x$，应作为一个整体理解：它是 $\mathbf{R}^n$ 中的一个向量，称为*迭代步*（step）或*搜索方向*（尽管它的范数不必为 $1$）；$k=0,1,\ldots$ 表示迭代编号。标量 $t^{(k)}\geq0$ 称为第 $k$ 次迭代的*步长*（step size 或 step length），尽管只有在 $\|\Delta x^{(k)}\|=1$ 时，它才等于 $\|x^{(k+1)}-x^{(k)}\|$。“搜索步”和“缩放因子”是更准确的说法，但广泛使用的是“搜索方向”和“步长”。在只关注算法的一次迭代时，我们有时省略上标，使用更简洁的记号 $x^+=x+t\Delta x$ 或 $x:=x+t\Delta x$，代替 $x^{(k+1)}=x^{(k)}+t^{(k)}\Delta x^{(k)}$。

我们研究的方法都是*下降法*，即除非 $x^{(k)}$ 已经最优，否则有

$$
f(x^{(k+1)})<f(x^{(k)}).
$$

这意味着，对所有 $k$，都有 $x^{(k)}\in S$，即迭代点属于初始下水平集；特别地，有 $x^{(k)}\in\mathbf{dom}\,f$。根据凸性，$\nabla f(x^{(k)})^T(y-x^{(k)})\geq0$ 意味着 $f(y)\geq f(x^{(k)})$，所以下降法的搜索方向必须满足

$$
\nabla f(x^{(k)})^T\Delta x^{(k)}<0,
$$

即它与负梯度的夹角必须为锐角。这样的方向称为（$f$ 在 $x^{(k)}$ 处的）*下降方向*。

<!-- pdf-page: 478 -->

一般下降法的框架如下。它交替执行两个步骤：确定下降方向 $\Delta x$，以及选择步长 $t$。

<div class="algorithm" id="algorithm-9-1" data-algorithm="9.1" markdown="1">

**算法 9.1 一般下降法。**

**给定** 初始点 $x\in\mathbf{dom}\,f$。

**重复执行**

1. 确定下降方向 $\Delta x$。
2. *直线搜索。* 选择步长 $t>0$。
3. *更新。* $x:=x+t\Delta x$。

**直到** 满足停止准则。

</div>

第二步称为*直线搜索*，因为选择步长 $t$ 就确定了下一个迭代点位于直线 $\{x+t\Delta x\mid t\in\mathbf{R}_+\}$ 上的哪个位置。（更准确的说法可能是*射线搜索*。）

实际的下降法具有相同的一般结构，但组织方式可能不同。例如，常常在计算下降方向 $\Delta x$ 的过程中，或在刚计算完之后，就检查停止准则。正如次优性条件 (9.9) 所提示的，停止准则通常具有 $\|\nabla f(x)\|_2\leq\eta$ 的形式，其中 $\eta$ 是一个很小的正数。

#### 精确直线搜索

实际中有时使用一种称为*精确直线搜索*的方法，它选择 $t$，使 $f$ 在射线 $\{x+t\Delta x\mid t\geq0\}$ 上最小：

$$
t=\operatorname*{argmin}_{s\geq0}f(x+s\Delta x).
\tag{9.16}
$$

如果求解 (9.16) 中单变量最小化问题的代价，相比计算搜索方向本身的代价较低，就会使用精确直线搜索。在某些特殊情况下，可以解析地求出射线上的最小点；在另一些情况下，也可以高效计算它。（§9.7.1 将讨论这一点。）

#### 回溯直线搜索

实际中使用的大多数直线搜索都是*非精确的*：所选步长使 $f$ 在射线 $\{x+t\Delta x\mid t\geq0\}$ 上近似最小，甚至只需让 $f$ 下降“足够多”。已有许多非精确直线搜索方法。其中一种非常简单而且很有效的方法，称为*回溯直线搜索*。它取决于两个常数 $\alpha$、$\beta$，满足 $0<\alpha<0.5$、$0<\beta<1$。

<div class="algorithm" id="algorithm-9-2" data-algorithm="9.2" markdown="1">

**算法 9.2 回溯直线搜索。**

**给定** $f$ 在 $x\in\mathbf{dom}\,f$ 处的下降方向 $\Delta x$，以及 $\alpha\in(0,0.5)$、$\beta\in(0,1)$。

$t:=1$。

**只要** $f(x+t\Delta x)>f(x)+\alpha t\nabla f(x)^T\Delta x$，**就重复执行** $t:=\beta t$。

</div>

<!-- pdf-page: 479 -->

<figure id="fig-9-1" data-figure="9.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-1.png" alt="沿方向 Δx 搜索时，函数曲线随步长 t 先下降后上升；两条虚线从 t=0 处出发，上方虚线在 t₀ 处与曲线相交。" data-source-page="479" data-source-rect="181,126,478,292">
<figcaption>图 9.1 回溯直线搜索。曲线表示函数 $f$ 限制在搜索直线上时的取值。下方虚线表示 $f$ 的线性外推，上方虚线的斜率是下方虚线斜率的 $\alpha$ 倍。回溯条件要求 $f$ 不高于上方虚线，即 $0\leq t\leq t_0$。</figcaption>
</figure>

这种直线搜索称为回溯，是因为它从单位步长开始，再反复乘以因子 $\beta$ 缩小步长，直到满足停止条件 $f(x+t\Delta x)\leq f(x)+\alpha t\nabla f(x)^T\Delta x$。由于 $\Delta x$ 是下降方向，有 $\nabla f(x)^T\Delta x<0$，因此，当 $t$ 足够小时，有

$$
f(x+t\Delta x)\approx f(x)+t\nabla f(x)^T\Delta x<f(x)+\alpha t\nabla f(x)^T\Delta x,
$$

这说明回溯直线搜索最终会终止。常数 $\alpha$ 可以解释为：我们愿意接受的 $f$ 的下降量，占线性外推所预测下降量的比例。（要求 $\alpha$ 小于 $0.5$ 的原因，将在后面说明。）

图 9.1 展示了回溯条件。从图中可以看出，并且可以证明，回溯的退出不等式 $f(x+t\Delta x)\leq f(x)+\alpha t\nabla f(x)^T\Delta x$，在非负 $t$ 的区间 $(0,t_0]$ 内成立。因此，回溯直线搜索终止时的步长 $t$ 满足

$$
t=1,\qquad\text{或}\qquad t\in(\beta t_0,t_0].
$$

第一种情况发生在步长 $t=1$ 满足回溯条件时，即 $1\leq t_0$。特别地，可以说，回溯直线搜索得到的步长满足

$$
t\geq\min\{1,\beta t_0\}.
$$

当 $\mathbf{dom}\,f$ 不是整个 $\mathbf{R}^n$ 时，必须谨慎理解回溯直线搜索中的条件 $f(x+t\Delta x)\leq f(x)+\alpha t\nabla f(x)^T\Delta x$。按照函数在定义域外取无穷大的约定，这个不等式意味着 $x+t\Delta x\in\mathbf{dom}\,f$。在实际实现中，先反复将 $t$ 乘以 $\beta$，直到 $x+t\Delta x\in\mathbf{dom}\,f$；<!-- pdf-page: 480 -->然后才开始检查不等式 $f(x+t\Delta x)\leq f(x)+\alpha t\nabla f(x)^T\Delta x$ 是否成立。

参数 $\alpha$ 通常取在 $0.01$ 到 $0.3$ 之间，这意味着接受的 $f$ 的下降量，为线性外推所预测下降量的 $1\%$ 到 $30\%$。参数 $\beta$ 常取在 $0.1$（对应很粗略的搜索）到 $0.8$（对应较细的搜索）之间。

## 9.3 梯度下降法

搜索方向的一个自然选择是负梯度 $\Delta x=-\nabla f(x)$。由此得到的算法称为*梯度算法*或*梯度下降法*。

<div class="algorithm" id="algorithm-9-3" data-algorithm="9.3" markdown="1">

**算法 9.3 梯度下降法。**

**给定** 初始点 $x\in\mathbf{dom}\,f$。

**重复执行**

1. $\Delta x:=-\nabla f(x)$。
2. *直线搜索。* 通过精确直线搜索或回溯直线搜索选择步长 $t$。
3. *更新。* $x:=x+t\Delta x$。

**直到** 满足停止准则。

</div>

停止准则通常具有 $\|\nabla f(x)\|_2\leq\eta$ 的形式，其中 $\eta$ 是很小的正数。在大多数实现中，这个条件在第 1 步之后检查，而不是在更新之后检查。

### 9.3.1 收敛性分析

本节对梯度法作一个简单的收敛性分析，用简洁记号 $x^+=x+t\Delta x$ 代替 $x^{(k+1)}=x^{(k)}+t^{(k)}\Delta x^{(k)}$，其中 $\Delta x=-\nabla f(x)$。假设 $f$ 在 $S$ 上强凸，因此存在正常数 $m$ 和 $M$，使得对所有 $x\in S$，都有 $mI\preceq\nabla^2f(x)\preceq MI$。定义函数 $\widetilde f:\mathbf{R}\to\mathbf{R}$ 为 $\widetilde f(t)=f(x-t\nabla f(x))$，即把沿负梯度方向的 $f$ 看作步长 $t$ 的函数。以下讨论只考虑满足 $x-t\nabla f(x)\in S$ 的 $t$。在不等式 (9.13) 中取 $y=x-t\nabla f(x)$，得到 $\widetilde f$ 的二次上界：

$$
\widetilde f(t)\leq f(x)-t\|\nabla f(x)\|_2^2+\frac{Mt^2}{2}\|\nabla f(x)\|_2^2.
\tag{9.17}
$$

#### 精确直线搜索的分析

现在假设使用精确直线搜索，并将不等式 (9.17) 两边分别对 $t$ 最小化。左端得到 $\widetilde f(t_{\mathrm{exact}})$，其中 $t_{\mathrm{exact}}$ 是使<!-- pdf-page: 481 -->$\widetilde f$ 最小的步长。右端是一个简单的二次函数，在 $t=1/M$ 时取得最小值 $f(x)-(1/(2M))\|\nabla f(x)\|_2^2$。因此有

$$
f(x^+)=\widetilde f(t_{\mathrm{exact}})\leq f(x)-\frac{1}{2M}\|\nabla(f(x))\|_2^2.
$$

两边减去 $p^\star$，得到

$$
f(x^+)-p^\star\leq f(x)-p^\star-\frac{1}{2M}\|\nabla f(x)\|_2^2.
$$

将其与 $\|\nabla f(x)\|_2^2\geq2m(f(x)-p^\star)$（由 (9.9) 得到）结合，可得

$$
f(x^+)-p^\star\leq(1-m/M)(f(x)-p^\star).
$$

递归应用这个不等式，得到

$$
f(x^{(k)})-p^\star\leq c^k(f(x^{(0)})-p^\star)
\tag{9.18}
$$

其中 $c=1-m/M<1$。这表明当 $k\to\infty$ 时，$f(x^{(k)})$ 收敛到 $p^\star$。特别地，采用精确直线搜索的梯度法至多经过

$$
\frac{\log((f(x^{(0)})-p^\star)/\epsilon)}{\log(1/c)}
\tag{9.19}
$$

次迭代，就一定有 $f(x^{(k)})-p^\star\leq\epsilon$。

这个所需迭代次数的界虽然粗略，仍能帮助理解梯度法。分子

$$
\log((f(x^{(0)})-p^\star)/\epsilon)
$$

可以解释为初始次优程度（即 $f(x^{(0)})$ 与 $p^\star$ 之间的差距）与最终次优程度（即小于 $\epsilon$）之比的对数。这一项表明，迭代次数取决于初始点的好坏，以及最终要求的精度。

界 (9.19) 中的分母 $\log(1/c)$ 是 $M/m$ 的函数。前面已经看到，$M/m$ 是 $\nabla^2f(x)$ 在 $S$ 上的条件数的界，也是下水平集 $\{z\mid f(z)\leq\alpha\}$ 的条件数的界。当条件数的界 $M/m$ 很大时，有

$$
\log(1/c)=-\log(1-m/M)\approx m/M,
$$

所以给出的所需迭代次数的界，随 $M/m$ 增大而近似线性增长。

我们将看到，如果 $f$ 在 $x^\star$ 附近的 Hessian 矩阵条件数很大，梯度法确实需要很多次迭代。反之，如果 $f$ 的下水平集比较接近各向同性，使条件数的界 $M/m$ 可以选得较小，那么 (9.18) 表明收敛很快，因为 $c$ 很小，或者至少不会太接近 $1$。

界 (9.18) 表明，误差 $f(x^{(k)})-p^\star$ 至少按等比数列的速度收敛到零。在迭代数值方法中，这称为*线性收敛*（linear convergence），因为在误差取对数、迭代次数取线性刻度的图上，误差位于一条直线之下。

<!-- pdf-page: 482 -->

#### 回溯直线搜索的分析

现在考虑梯度下降法使用回溯直线搜索的情况。我们将证明，只要 $0\leq t\leq1/M$，就满足回溯退出条件

$$
\widetilde f(t)\leq f(x)-\alpha t\|\nabla f(x)\|_2^2.
$$

首先注意到

$$
0\leq t\leq1/M\quad\Longrightarrow\quad-t+\frac{Mt^2}{2}\leq-t/2
$$

（这可以由 $-t+Mt^2/2$ 的凸性得到）。利用这一结果和界 (9.17)，当 $0\leq t\leq1/M$ 时，有

$$
\begin{aligned}
\widetilde f(t)&\leq f(x)-t\|\nabla f(x)\|_2^2+\frac{Mt^2}{2}\|\nabla(f(x))\|_2^2\\
&\leq f(x)-(t/2)\|\nabla f(x)\|_2^2\\
&\leq f(x)-\alpha t\|\nabla f(x)\|_2^2,
\end{aligned}
$$

因为 $\alpha<1/2$。因此，回溯直线搜索终止时，要么 $t=1$，要么 $t\geq\beta/M$。这给出了目标函数下降量的下界。第一种情况下，有

$$
f(x^+)\leq f(x)-\alpha\|\nabla f(x)\|_2^2,
$$

第二种情况下，有

$$
f(x^+)\leq f(x)-(\beta\alpha/M)\|\nabla f(x)\|_2^2.
$$

将两种情况合起来，总有

$$
f(x^+)\leq f(x)-\min\{\alpha,\beta\alpha/M\}\|\nabla f(x)\|_2^2.
$$

现在可以完全按照精确直线搜索的情况继续推导。两边减去 $p^\star$，得到

$$
f(x^+)-p^\star\leq f(x)-p^\star-\min\{\alpha,\beta\alpha/M\}\|\nabla f(x)\|_2^2,
$$

再与 $\|\nabla f(x)\|_2^2\geq2m(f(x)-p^\star)$ 结合，得到

$$
f(x^+)-p^\star\leq\bigl(1-\min\{2m\alpha,2\beta\alpha m/M\}\bigr)(f(x)-p^\star).
$$

由此得出

$$
f(x^{(k)})-p^\star\leq c^k(f(x^{(0)})-p^\star)
$$

其中

$$
c=1-\min\{2m\alpha,2\beta\alpha m/M\}<1.
$$

特别地，$f(x^{(k)})$ 至少按等比数列的速度收敛到 $p^\star$，其中指数衰减的快慢至少部分取决于条件数的界 $M/m$。用迭代方法的术语来说，收敛至少是线性的。

<!-- pdf-page: 483 -->

<figure id="fig-9-2" data-figure="9.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-2.png" alt="二次函数的虚线椭圆等值线中，梯度法的迭代点从 x⁽⁰⁾=(10,1) 出发，上下交替地向原点逼近；横轴为 x₁，纵轴为 x₂。" data-source-page="483" data-source-rect="148,122,413,246">
<figcaption>图 9.2 函数 $f(x)=(1/2)(x_1^2+10x_2^2)$ 的若干等值线。它的下水平集是椭球，条件数恰为 $10$。图中给出了采用精确直线搜索的梯度法从 $x^{(0)}=(10,1)$ 出发时的迭代点。</figcaption>
</figure>

### 9.3.2 例子

#### $\mathbf{R}^2$ 中的一个二次问题

第一个例子很简单。考虑 $\mathbf{R}^2$ 上的二次目标函数

$$
f(x)=\frac{1}{2}(x_1^2+\gamma x_2^2),
$$

其中 $\gamma>0$。显然，最优点为 $x^\star=0$，最优值为 $0$。$f$ 的 Hessian 矩阵是常数矩阵，特征值为 $1$ 和 $\gamma$，所以 $f$ 的所有下水平集的条件数都恰好为

$$
\frac{\max\{1,\gamma\}}{\min\{1,\gamma\}}=\max\{\gamma,1/\gamma\}.
$$

强凸性常数 $m$ 和 $M$ 的最紧取值为

$$
m=\min\{1,\gamma\},\qquad M=\max\{1,\gamma\}.
$$

从点 $x^{(0)}=(\gamma,1)$ 出发，应用采用精确直线搜索的梯度下降法。在这种情况下，可以推导出迭代点 $x^{(k)}$ 及其函数值的如下闭式表达式（习题 9.6）：

$$
x_1^{(k)}=\gamma\left(\frac{\gamma-1}{\gamma+1}\right)^k,\qquad
x_2^{(k)}=\left(-\frac{\gamma-1}{\gamma+1}\right)^k,
$$

以及

$$
f(x^{(k)})=\frac{\gamma(\gamma+1)}{2}\left(\frac{\gamma-1}{\gamma+1}\right)^{2k}
=\left(\frac{\gamma-1}{\gamma+1}\right)^{2k}f(x^{(0)}).
$$

图 9.2 展示了 $\gamma=10$ 时的情况。

对这个简单例子，收敛恰好是线性的，即误差恰好构成等比数列，每次迭代后变为前一次的 $|(\gamma-1)/(\gamma+1)|^2$。当<!-- pdf-page: 484 -->$\gamma=1$ 时，一次迭代就找到精确解；当 $\gamma$ 与 $1$ 相差不远时（例如在 $1/3$ 与 $3$ 之间），收敛很快。当 $\gamma\gg1$ 或 $\gamma\ll1$ 时，收敛很慢。

可以将这个收敛结果与上面 §9.3.1 推导的界作比较。取最不保守的 $m=\min\{1,\gamma\}$ 和 $M=\max\{1,\gamma\}$，界 (9.18) 保证每次迭代后的误差至多是前一次的 $c=1-m/M$。我们已经看到，实际每次迭代后的误差恰好是前一次的

$$
\left(\frac{1-m/M}{1+m/M}\right)^2.
$$

当 $m/M$ 很小，即条件数很大时，上界 (9.19) 表明，达到给定精度所需的迭代次数至多按 $M/m$ 的量级增长。对这个例子，实际所需迭代次数近似按 $(M/m)/4$ 增长，即约为该界的四分之一。这说明，对这个简单例子，在 $m$ 和 $M$ 取最不保守的值时，简单分析给出的迭代次数界仅约为实际所需次数的四倍。特别地，收敛速度及其上界都很依赖于下水平集的条件数。

#### $\mathbf{R}^2$ 中的一个非二次问题

现在考虑 $\mathbf{R}^2$ 中的一个非二次例子，其中

$$
f(x_1,x_2)=e^{x_1+3x_2-0.1}+e^{x_1-3x_2-0.1}+e^{-x_1-0.1}.
\tag{9.20}
$$

采用带回溯直线搜索的梯度法，参数取 $\alpha=0.1$、$\beta=0.7$。图 9.3 给出了 $f$ 的一些等值线，以及梯度法产生的迭代点 $x^{(k)}$（用小圆圈表示）。连接相邻迭代点的线段表示缩放后的迭代步：

$$
x^{(k+1)}-x^{(k)}=-t^{(k)}\nabla f(x^{(k)}).
$$

图 9.4 给出了误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化。从图上可见，误差近似按等比数列收敛到零，即收敛近似为线性的。在这个例子中，经过 $20$ 次迭代，误差从约 $10$ 降至约 $10^{-7}$，所以每次迭代后的误差约为前一次的 $10^{-8/20}\approx0.4$。这种相当快的收敛可以由前面的收敛性分析预见，因为 $f$ 的下水平集的条件数不算太大，这又意味着 $M/m$ 可以选得不太大。

为比较回溯直线搜索与精确直线搜索，在同一问题上，采用相同的初始点，运行带精确直线搜索的梯度法。结果见图 9.5 和图 9.4。这里的收敛也近似为线性的，速度约为采用回溯直线搜索的梯度法的两倍。采用精确直线搜索时，经过 $15$ 次迭代，误差约降为原来的 $10^{-11}$，即每次迭代后的误差约为前一次的 $10^{-11/15}\approx0.2$。

<!-- pdf-page: 485 -->

<figure id="fig-9-3" data-figure="9.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-3.png" alt="虚线等值曲线内，梯度法从 x⁽⁰⁾ 出发，经过 x⁽¹⁾、x⁽²⁾ 等迭代点，沿往返折线逐渐逼近中心。" data-source-page="485" data-source-rect="175,143,394,272">
<figcaption>图 9.3 采用回溯直线搜索的梯度法的迭代点，所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。虚线是 $f$ 的等值线，小圆圈是梯度法的迭代点。连接相邻迭代点的实线表示缩放后的迭代步 $t^{(k)}\Delta x^{(k)}$。</figcaption>
</figure>

<figure id="fig-9-4" data-figure="9.4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-4.png" alt="梯度法的误差随迭代次数 k 下降，纵轴采用对数刻度；采用精确直线搜索的曲线比采用回溯直线搜索的曲线下降得更快。" data-source-page="485" data-source-rect="148,400,394,586">
<figcaption>图 9.4 采用回溯直线搜索和精确直线搜索的梯度法，其误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化；所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。图中表现出近似线性收敛：采用回溯直线搜索时，梯度法每次迭代后的误差约为前一次的 $0.4$ 倍；采用精确直线搜索时，每次迭代后的误差约为前一次的 $0.2$ 倍。</figcaption>
<p class="figure-translation">图内文字：backtracking l.s.——回溯直线搜索；exact l.s.——精确直线搜索。</p>
</figure>

<!-- pdf-page: 486 -->

<figure id="fig-9-5" data-figure="9.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-5.png" alt="采用精确直线搜索的梯度法从 x⁽⁰⁾ 到 x⁽¹⁾，再用几步到达虚线等值曲线的中心附近；空心圆表示迭代点，实线连接相邻点。" data-source-page="486" data-source-rect="229,120,448,249">
<figcaption>图 9.5 采用精确直线搜索的梯度法的迭代点，所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。</figcaption>
</figure>

#### $\mathbf{R}^{100}$ 中的一个问题

接下来考虑一个规模更大的例子，形式为

$$
f(x)=c^Tx-\sum_{i=1}^m\log(b_i-a_i^Tx),
\tag{9.21}
$$

其中有 $m=500$ 项和 $n=100$ 个变量。

图 9.6 给出了采用回溯直线搜索、参数取 $\alpha=0.1$、$\beta=0.5$ 时，梯度法的迭代过程。在这个例子中，最初约 $20$ 次迭代呈现近似线性且相当快的收敛，随后进入较慢的线性收敛。总体上，经过约 $175$ 次迭代，误差缩小约 $10^6$ 倍，平均每次迭代后的误差约为前一次的 $10^{-6/175}\approx0.92$。在最初 $20$ 次迭代中，每次误差约变为前一次的 $0.8$；在此后的较慢收敛阶段，每次误差约变为前一次的 $0.94$。

图 9.6 还给出了采用精确直线搜索的梯度法的收敛情况。收敛同样近似为线性的，总体上每次迭代后的误差约为前一次的 $10^{-6/140}\approx0.91$。这只比采用回溯直线搜索的梯度法略快。

最后，通过测定达到 $f(x^{(k)})-p^\star\leq10^{-5}$ 所需的迭代次数，考察回溯直线搜索参数 $\alpha$ 和 $\beta$ 对收敛速度的影响。第一个实验固定 $\beta=0.5$，令 $\alpha$ 从 $0.05$ 变化到 $0.5$。当 $\alpha$ 较大、处于 $0.2$–$0.5$ 范围时，所需迭代次数约为 $80$；当 $\alpha$ 较小时，约为 $170$。这个实验以及其他实验表明，取较大的 $\alpha$，例如 $0.2$–$0.5$，梯度法的表现更好。

类似地，可以固定 $\alpha=0.1$，令 $\beta$ 从 $0.05$ 变化到 $0.95$，研究 $\beta$ 的选择所带来的影响。总迭代次数的变化同样不大，从约 $80$ 次（$\beta\approx0.5$ 时）到约 $200$ 次（$\beta$ 很小或接近 $1$ 时）。这个实验以及其他实验表明，$\beta\approx0.5$ 是一个较好的选择。

<!-- pdf-page: 487 -->

<figure id="fig-9-6" data-figure="9.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-6.png" alt="一百维问题中，采用回溯直线搜索和精确直线搜索的梯度法的误差随迭代次数 k 整体下降，两条曲线在后半段相交；纵轴为对数刻度。" data-source-page="487" data-source-rect="148,122,416,306">
<figcaption>图 9.6 对于 $\mathbf{R}^{100}$ 中的一个问题，采用回溯直线搜索和精确直线搜索的梯度法，其误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化。</figcaption>
<p class="figure-translation">图内文字：exact l.s.——精确直线搜索；backtracking l.s.——回溯直线搜索。</p>
</figure>

这些实验表明，回溯参数对收敛的影响不大，差异不超过约两倍。

#### 梯度法与条件数

最后一个实验将说明，$\nabla^2f(x)$ 或下水平集的条件数，对梯度法的收敛速度有多大影响。从 (9.21) 给出的函数出发，作变量代换 $x=T\bar x$，其中

$$
T=\mathbf{diag}\bigl((1,\gamma^{1/n},\gamma^{2/n},\ldots,\gamma^{(n-1)/n})\bigr),
$$

即最小化

$$
\bar f(\bar x)=c^TT\bar x-\sum_{i=1}^m\log(b_i-a_i^TT\bar x).
\tag{9.22}
$$

这给出一族以 $\gamma$ 为参数的优化问题，$\gamma$ 会影响问题的条件数。

图 9.7 给出了达到 $\bar f(\bar x^{(k)})-\bar p^\star<10^{-5}$ 所需的迭代次数随 $\gamma$ 的变化，使用回溯直线搜索，取 $\alpha=0.3$、$\beta=0.7$。图中表明，对角缩放比例仅为 $10:1$（即 $\gamma=10$）时，迭代次数就增长到一千次以上；当对角缩放比例达到 $20$ 或更大时，梯度法慢到基本上无法使用。

最优点处 Hessian 矩阵 $\nabla^2\bar f(\bar x^\star)$ 的条件数见图 9.8。当 $\gamma$ 很大或很小时，条件数大致按 $\max\{\gamma^2,1/\gamma^2\}$ 增长，与迭代次数对 $\gamma$ 的依赖非常相似。这再次说明，条件数与收敛速度之间的关系确实存在，并非仅仅是分析方法造成的表象。

<!-- pdf-page: 488 -->

<figure id="fig-9-7" data-figure="9.7">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-7.png" alt="双对数坐标图中，梯度法所需迭代次数随对角缩放参数 γ 呈谷形变化，在 γ 接近 1 时较少，在两侧明显增加。" data-source-page="488" data-source-rect="213,164,448,348">
<figcaption>图 9.7 将梯度法用于问题 (9.22) 时的迭代次数。纵轴表示达到 $\bar f(\bar x^{(k)})-\bar p^\star<10^{-5}$ 所需的迭代次数。横轴表示控制对角缩放程度的参数 $\gamma$。这里使用回溯直线搜索，参数为 $\alpha=0.3$、$\beta=0.7$。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>

<figure id="fig-9-8" data-figure="9.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-8.png" alt="函数在最小值点处的 Hessian 矩阵条件数随 γ 变化，曲线在 γ 接近 1 时较低，在两侧升高；横纵轴都采用对数刻度。" data-source-page="488" data-source-rect="211,412,448,596">
<figcaption>图 9.8 函数在最小值点处的 Hessian 矩阵条件数随 $\gamma$ 的变化。将本图与图 9.7 比较，可以看出条件数对收敛速度有很强的影响。</figcaption>
</figure>

<!-- pdf-page: 489 -->

#### 结论

根据上述数值例子以及其他例子，可以得出以下结论。

- 梯度法常表现出近似线性收敛，即误差 $f(x^{(k)})-p^\star$ 近似按等比数列收敛到零。

- 回溯参数 $\alpha$、$\beta$ 的选择对收敛有可见的影响，但影响并不显著。精确直线搜索有时能改善梯度法的收敛，但效果不大，可能并不值得为此实现精确直线搜索。

- 收敛速度很依赖于 Hessian 矩阵或下水平集的条件数。即使问题的条件状况尚可，例如条件数为几百，收敛也可能很慢。当条件数更大，例如达到 $1000$ 或更多时，梯度法慢到在实际中无法使用。

梯度法的主要优点是简单。主要缺点是，收敛速度对 Hessian 矩阵或下水平集的条件数过于敏感。

## 9.4 最速下降法

$f(x+v)$ 在 $x$ 附近的一阶 Taylor 逼近为

$$
f(x+v)\approx\widehat f(x+v)=f(x)+\nabla f(x)^Tv.
$$

右端第二项 $\nabla f(x)^Tv$ 是 $f$ 在 $x$ 处沿方向 $v$ 的*方向导数*。当迭代步 $v$ 很小时，它给出 $f$ 的近似变化量。如果方向导数为负，那么 $v$ 就是下降方向。

现在考虑如何选择 $v$，使方向导数尽可能小。由于方向导数 $\nabla f(x)^Tv$ 是 $v$ 的线性函数，只要 $v$ 是下降方向，即 $\nabla f(x)^Tv<0$，就可以通过增大 $v$，使方向导数任意小。要使这个问题有意义，必须限制 $v$ 的大小，或按 $v$ 的长度进行归一化。

设 $\|\cdot\|$ 为 $\mathbf{R}^n$ 上的任意范数。相对于范数 $\|\cdot\|$ 的一个*归一化最速下降方向*定义为

$$
\Delta x_{\mathrm{nsd}}=\operatorname*{argmin}\{\nabla f(x)^Tv\mid\|v\|=1\}.
\tag{9.23}
$$

这里说“一个”最速下降方向，是因为可能存在多个最小点。归一化最速下降方向 $\Delta x_{\mathrm{nsd}}$ 是范数为 $1$ 的迭代步，它使 $f$ 的线性逼近下降最多。

归一化最速下降方向可以作如下几何解释。也可以将 $\Delta x_{\mathrm{nsd}}$ 定义为

$$
\Delta x_{\mathrm{nsd}}=\operatorname*{argmin}\{\nabla f(x)^Tv\mid\|v\|\leq1\},
$$

<!-- pdf-page: 490 -->

即在范数 $\|\cdot\|$ 的单位球内，沿 $-\nabla f(x)$ 方向伸得最远的向量。

还可以按一种特定方式缩放归一化最速下降方向，得到*未归一化的最速下降步* $\Delta x_{\mathrm{sd}}$；考虑这样的迭代步也很方便：

$$
\Delta x_{\mathrm{sd}}=\|\nabla f(x)\|_*\Delta x_{\mathrm{nsd}},
\tag{9.24}
$$

其中 $\|\cdot\|_*$ 表示对偶范数。注意，对最速下降步，有

$$
\nabla f(x)^T\Delta x_{\mathrm{sd}}
=\|\nabla f(x)\|_*\nabla f(x)^T\Delta x_{\mathrm{nsd}}
=-\|\nabla f(x)\|_*^2
$$

（见习题 9.7）。

*最速下降法*以最速下降方向作为搜索方向。

<div class="algorithm" id="algorithm-9-4" data-algorithm="9.4" markdown="1">

**算法 9.4 最速下降法。**

**给定** 初始点 $x\in\mathbf{dom}\,f$。

**重复执行**

1. 计算最速下降方向 $\Delta x_{\mathrm{sd}}$。
2. *直线搜索。* 通过回溯直线搜索或精确直线搜索选择 $t$。
3. *更新。* $x:=x+t\Delta x_{\mathrm{sd}}$。

**直到** 满足停止准则。

</div>

采用精确直线搜索时，下降方向的缩放因子不影响结果，因此可以使用归一化或未归一化的方向。

### 9.4.1 欧几里得范数与二次范数下的最速下降

#### 欧几里得范数下的最速下降

若将范数 $\|\cdot\|$ 取为欧几里得范数，最速下降方向就是负梯度，即 $\Delta x_{\mathrm{sd}}=-\nabla f(x)$。欧几里得范数下的最速下降法与梯度下降法相同。

#### 二次范数下的最速下降

考虑二次范数

$$
\|z\|_P=(z^TPz)^{1/2}=\|P^{1/2}z\|_2,
$$

其中 $P\in\mathbf{S}_{++}^n$。归一化最速下降方向为

$$
\Delta x_{\mathrm{nsd}}=-\bigl(\nabla f(x)^TP^{-1}\nabla f(x)\bigr)^{-1/2}P^{-1}\nabla f(x).
$$

对偶范数为 $\|z\|_*=\|P^{-1/2}z\|_2$，所以相对于 $\|\cdot\|_P$ 的最速下降步为

$$
\Delta x_{\mathrm{sd}}=-P^{-1}\nabla f(x).
\tag{9.25}
$$

图 9.9 展示了二次范数下的归一化最速下降方向。

<!-- pdf-page: 491 -->

<figure id="fig-9-9" data-figure="9.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-9.png" alt="灰色椭圆表示平移后的二次范数单位球；从中心出发的负梯度箭头指向右上方，归一化最速下降箭头指向椭圆右下侧与支撑直线的接触点。" data-source-page="491" data-source-rect="211,121,393,276">
<figcaption>图 9.9 二次范数下的归一化最速下降方向。图中的椭球是该范数的单位球平移到点 $x$ 后得到的。点 $x$ 处的归一化最速下降方向 $\Delta x_{\mathrm{nsd}}$ 在保持端点位于椭球内的同时，使端点在 $-\nabla f(x)$ 方向上的投影尽可能远。图中画出了梯度方向和归一化最速下降方向。</figcaption>
</figure>

#### 通过坐标变换解释

最速下降方向 $\Delta x_{\mathrm{sd}}$ 还有一个有趣的解释：它是对问题作坐标变换后得到的梯度搜索方向。定义 $\bar u=P^{1/2}u$，于是有 $\|u\|_P=\|\bar u\|_2$。利用这个坐标变换，可以通过最小化函数 $\bar f:\mathbf{R}^n\to\mathbf{R}$ 的等价问题，来求解原来的 $f$ 最小化问题，其中

$$
\bar f(\bar u)=f(P^{-1/2}\bar u)=f(u).
$$

如果对 $\bar f$ 应用梯度法，那么在点 $\bar x$（对应原问题中的点 $x=P^{-1/2}\bar x$）处，搜索方向为

$$
\Delta\bar x=-\nabla\bar f(\bar x)=-P^{-1/2}\nabla f(P^{-1/2}\bar x)=-P^{-1/2}\nabla f(x).
$$

这个梯度搜索方向对应原变量 $x$ 的方向

$$
\Delta x=P^{-1/2}\bigl(-P^{-1/2}\nabla f(x)\bigr)=-P^{-1}\nabla f(x).
$$

换言之，二次范数 $\|\cdot\|_P$ 下的最速下降法，可以看作对问题作坐标变换 $\bar x=P^{1/2}x$ 后再应用梯度法。

### 9.4.2 $\ell_1$ 范数下的最速下降

作为另一个例子，考虑 $\ell_1$ 范数下的最速下降法。归一化最速下降方向

$$
\Delta x_{\mathrm{nsd}}=\operatorname*{argmin}\{\nabla f(x)^Tv\mid\|v\|_1\leq1\}
$$

<!-- pdf-page: 492 -->

<figure id="fig-9-10" data-figure="9.10" data-no-english-text="true" data-reader-after="l1-steepest-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-10.png" alt="灰色菱形表示平移后的 ℓ₁ 范数单位球；负梯度箭头指向右上方，归一化最速下降箭头水平指向菱形最右侧的顶点。" data-source-page="492" data-source-rect="265,121,447,281">
<figcaption>图 9.10 $\ell_1$ 范数下的归一化最速下降方向。菱形是 $\ell_1$ 范数的单位球平移到点 $x$ 后得到的。归一化最速下降方向总可以选在某个标准基向量的方向上；本例中有 $\Delta x_{\mathrm{nsd}}=e_1$。</figcaption>
</figure>

很容易刻画。设 $i$ 是任意一个满足 $\|\nabla f(x)\|_\infty=|(\nabla f(x))_i|$ 的下标。那么，$\ell_1$ 范数下的一个归一化最速下降方向 $\Delta x_{\mathrm{nsd}}$ 为

$$
\Delta x_{\mathrm{nsd}}=-\operatorname{sign}\left(\frac{\partial f(x)}{\partial x_i}\right)e_i,
$$

其中 $e_i$ 是第 $i$ 个标准基向量。相应的未归一化最速下降步为

$$
\Delta x_{\mathrm{sd}}=\Delta x_{\mathrm{nsd}}\|\nabla f(x)\|_\infty=-\frac{\partial f(x)}{\partial x_i}e_i.
$$

<p id="l1-steepest-explanation" markdown="1">因此，$\ell_1$ 范数下的归一化最速下降步，总可以选为一个标准基向量或其相反向量。这个坐标轴方向使 $f$ 的近似下降量最大。图 9.10 展示了这一点。</p>

$\ell_1$ 范数下的最速下降算法有很自然的解释：每次迭代选择 $\nabla f(x)$ 中绝对值最大的一个分量，然后根据 $(\nabla f(x))_i$ 的符号，减小或增大 $x$ 的对应分量。这种算法有时称为*坐标下降算法*，因为每次迭代只更新变量 $x$ 的一个分量。这可以大大简化直线搜索，甚至使其非常容易求解。

<div class="example" markdown="1">

**例 9.2 Frobenius 范数缩放。** 在 §4.5.4 中，我们遇到过无约束几何规划

$$
\begin{array}{ll}
\text{最小化} & \sum_{i,j=1}^n M_{ij}^2d_i^2/d_j^2,
\end{array}
$$

其中 $M\in\mathbf{R}^{n\times n}$ 已知，变量为 $d\in\mathbf{R}^n$。通过变量代换 $x_i=2\log d_i$，可以将这个几何规划写成凸形式：

$$
\begin{array}{ll}
\text{最小化} & f(x)=\log\left(\sum_{i,j=1}^nM_{ij}^2e^{x_i-x_j}\right).
\end{array}
$$

<!-- pdf-page: 493 -->

每次只对一个分量最小化 $f$，是很容易的。固定除第 $k$ 个分量以外的所有分量，可以写成 $f(x)=\log(\alpha_k+\beta_ke^{-x_k}+\gamma_ke^{x_k})$，其中

$$
\alpha_k=M_{kk}^2+\sum_{i,j\ne k}M_{ij}^2e^{x_i-x_j},\qquad
\beta_k=\sum_{i\ne k}M_{ik}^2e^{x_i},\qquad
\gamma_k=\sum_{j\ne k}M_{kj}^2e^{-x_j}.
$$

把 $f(x)$ 看作 $x_k$ 的函数，其最小值在 $x_k=\log(\beta_k/\gamma_k)/2$ 处取得。因此，对这个问题，可以利用一个简单的解析公式执行精确直线搜索。

采用精确直线搜索的 $\ell_1$ 最速下降算法，就是重复执行以下步骤。

1. 计算梯度

    $$
    (\nabla f(x))_i=\frac{-\beta_ie^{-x_i}+\gamma_ie^{x_i}}{\alpha_i+\beta_ie^{-x_i}+\gamma_ie^{x_i}},\qquad i=1,\ldots,n.
    $$

2. 选择 $\nabla f(x)$ 中绝对值最大的一个分量：$|\nabla f(x)|_k=\|\nabla f(x)\|_\infty$。

3. 令 $x_k=\log(\beta_k/\gamma_k)/2$，从而对标量变量 $x_k$ 最小化 $f$。

</div>

### 9.4.3 收敛性分析

本节将带回溯直线搜索的梯度法的收敛性分析，推广到任意范数下的最速下降法。我们将利用一个事实：任意范数都可以用欧几里得范数来给出界，因此存在常数 $\gamma,\widetilde\gamma\in(0,1]$，使得

$$
\|x\|\geq\gamma\|x\|_2,\qquad\|x\|_*\geq\widetilde\gamma\|x\|_2
$$

（见 §A.1.4）。

仍假设 $f$ 在初始下水平集 $S$ 上强凸。上界 $\nabla^2f(x)\preceq MI$ 给出了函数 $f(x+t\Delta x_{\mathrm{sd}})$ 关于 $t$ 的上界：

$$
\begin{aligned}
f(x+t\Delta x_{\mathrm{sd}})&\leq f(x)+t\nabla f(x)^T\Delta x_{\mathrm{sd}}+\frac{M\|\Delta x_{\mathrm{sd}}\|_2^2}{2}t^2\\
&\leq f(x)+t\nabla f(x)^T\Delta x_{\mathrm{sd}}+\frac{M\|\Delta x_{\mathrm{sd}}\|^2}{2\gamma^2}t^2\\
&=f(x)-t\|\nabla f(x)\|_*^2+\frac{M}{2\gamma^2}t^2\|\nabla f(x)\|_*^2.
\end{aligned}
\tag{9.26}
$$

步长 $\widehat t=\gamma^2/M$ 使二次上界 (9.26) 最小，并满足回溯直线搜索的退出条件：

$$
f(x+\widehat t\Delta x_{\mathrm{sd}})\leq f(x)-\frac{\gamma^2}{2M}\|\nabla f(x)\|_*^2
\leq f(x)+\frac{\alpha\gamma^2}{M}\nabla f(x)^T\Delta x_{\mathrm{sd}}
\tag{9.27}
$$

<!-- pdf-page: 494 -->

因为 $\alpha<1/2$，且 $\nabla f(x)^T\Delta x_{\mathrm{sd}}=-\|\nabla f(x)\|_*^2$。所以直线搜索返回的步长满足 $t\geq\min\{1,\beta\gamma^2/M\}$，并且有

$$
\begin{aligned}
f(x^+)=f(x+t\Delta x_{\mathrm{sd}})&\leq f(x)-\alpha\min\{1,\beta\gamma^2/M\}\|\nabla f(x)\|_*^2\\
&\leq f(x)-\alpha\widetilde\gamma^2\min\{1,\beta\gamma^2/M\}\|\nabla f(x)\|_2^2.
\end{aligned}
$$

两边减去 $p^\star$，再利用 (9.9)，得到

$$
f(x^+)-p^\star\leq c(f(x)-p^\star),
$$

其中

$$
c=1-2m\alpha\widetilde\gamma^2\min\{1,\beta\gamma^2/M\}<1.
$$

因此有

$$
f(x^{(k)})-p^\star\leq c^k(f(x^{(0)})-p^\star),
$$

即与梯度法一样，得到线性收敛。

### 9.4.4 讨论与例子

#### 最速下降范数的选择

用于定义最速下降方向的范数，会对收敛速度产生显著影响。为简单起见，考虑二次 $P$ 范数下的最速下降法。在 §9.4.1 中已经证明，二次 $P$ 范数下的最速下降法，等价于对问题作坐标变换 $\bar x=P^{1/2}x$ 后再应用梯度法。我们知道，当下水平集或最优点附近的 Hessian 矩阵的条件数不太大时，梯度法表现良好；当条件数很大时，表现很差。因此，若作坐标变换 $\bar x=P^{1/2}x$ 后，下水平集的条件数不太大，最速下降法就会表现良好。

这个观察给出了选择 $P$ 的方法：应使 $f$ 的下水平集经过 $P^{-1/2}$ 变换后具有良好的条件状况。例如，如果知道最优点处 Hessian 矩阵 $H(x^\star)$ 的一个近似 $\widehat H$，那么一个很好的选择是 $P=\widehat H$，因为此时 $\widetilde f$ 在最优点处的 Hessian 矩阵为

$$
\widehat H^{-1/2}\nabla^2f(x^\star)\widehat H^{-1/2}\approx I,
$$

所以很可能具有较小的条件数。

<div class="translator-note" markdown="1">

**译注：坐标变换的两个方向。** 原文此处写下水平集经 $P^{-1/2}$ 变换。按本节定义的 $\bar x=P^{1/2}x$，若用 $C$ 表示原函数的一个下水平集，那么它在新坐标中的像是 $P^{1/2}C$。而 $P^{-1/2}$ 是返回原坐标的映射，出现在新目标函数 $\bar f(\bar x)=f(P^{-1/2}\bar x)$ 的代入式中。

</div>

不借助坐标变换，也可以描述同样的想法。说下水平集在坐标变换 $\bar x=P^{1/2}x$ 后具有较小的条件数，等价于说椭球

$$
\mathcal{E}=\{x\mid x^TPx\leq1\}
$$

逼近下水平集的形状。换言之，经过适当缩放和平移后，它能给出较好的逼近。

<p id="steepest-norm-choice-start" markdown="1">收敛速度对 $P$ 的选择的依赖，可以从两个角度看。乐观的看法是：对任意问题，总有一种</p>

<!-- pdf-page: 495 -->

<figure id="fig-9-11" data-figure="9.11" data-no-english-text="true" data-reader-after="steepest-two-norms-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-11.png" alt="采用 P₁ 二次范数的最速下降法迭代路径；x⁽⁰⁾ 和 x⁽¹⁾ 周围各有一个横向椭圆，虚线等值曲线内的迭代点经 x⁽²⁾ 向中心收敛。" data-source-page="495" data-source-rect="175,122,395,256">
<figcaption>图 9.11 采用二次范数 $\|\cdot\|_{P_1}$ 的最速下降法。图中的椭圆是分别以 $x^{(0)}$ 和 $x^{(1)}$ 为中心的范数球 $\{x\mid\|x-x^{(k)}\|_{P_1}\leq 1\}$ 的边界。</figcaption>
</figure>

<p id="steepest-norm-choice-end" markdown="1" data-reader-continue="steepest-norm-choice-start">$P$ 的选择，使最速下降法表现很好。当然，难点在于找出这样的 $P$。悲观的看法是：对任意问题，都有大量的 $P$ 会使最速下降法表现很差。总的来说，如果能找到一个矩阵 $P$，使变换后问题的条件数不太大，最速下降法就能表现良好。</p>

#### 例子

本节用目标函数为 (9.20) 的 $\mathbf{R}^2$ 中非二次问题，说明上述一些想法。对这个问题应用最速下降法，分别采用由

$$
P_1=\begin{bmatrix}2&0\\0&8\end{bmatrix},\qquad
P_2=\begin{bmatrix}8&0\\0&2\end{bmatrix}
$$

定义的两个二次范数。两种情况都采用回溯直线搜索，取 $\alpha=0.1$、$\beta=0.7$。

图 9.11 和图 9.12 分别给出了采用范数 $\|\cdot\|_{P_1}$ 和 $\|\cdot\|_{P_2}$ 的最速下降法的迭代点。图 9.13 给出了两种范数下误差随迭代次数的变化。图 9.13 表明，范数的选择强烈影响收敛。采用 $\|\cdot\|_{P_1}$ 时，收敛比梯度法稍快；采用 $\|\cdot\|_{P_2}$ 时，收敛则慢得多。

<p id="steepest-two-norms-end" markdown="1">分别考察坐标变换 $\bar x=P_1^{1/2}x$ 和 $\bar x=P_2^{1/2}x$ 后的问题，就能解释这一现象。图 9.14 和图 9.15 给出了变换后坐标中的问题。与 $P_1$ 对应的变量代换使下水平集具有不太大的条件数，所以收敛很快。与 $P_2$ 对应的变量代换使下水平集的条件状况更差，这就解释了收敛较慢的原因。</p>

<!-- pdf-page: 496 -->

<figure id="fig-9-12" data-figure="9.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-12.png" alt="采用 P₂ 二次范数的最速下降法迭代路径；x⁽⁰⁾ 和 x⁽¹⁾ 周围各有一个竖向椭圆，迭代点上下往返，逐渐靠近虚线等值曲线的中心。" data-source-page="496" data-source-rect="229,156,448,319">
<figcaption>图 9.12 采用二次范数 $\|\cdot\|_{P_2}$ 的最速下降法。</figcaption>
</figure>

<figure id="fig-9-13" data-figure="9.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-13.png" alt="最速下降法的误差随迭代次数 k 变化；纵轴采用对数刻度，P₁ 曲线在约 15 次迭代内降至 10⁻¹⁰，P₂ 曲线至 40 次迭代仍缓慢下降。" data-source-page="496" data-source-rect="201,420,451,605">
<figcaption>图 9.13 分别采用二次范数 $\|\cdot\|_{P_1}$ 和 $\|\cdot\|_{P_2}$ 时，最速下降法的误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化。采用范数 $\|\cdot\|_{P_1}$ 时收敛很快，采用范数 $\|\cdot\|_{P_2}$ 时收敛则很慢。</figcaption>
</figure>

<!-- pdf-page: 497 -->

<figure id="fig-9-14" data-figure="9.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-14.png" alt="P₁ 范数最速下降法的迭代点经坐标变换后的图形；变换后的前两个迭代点旁画有圆形范数球，虚线等值曲线较为均匀，折线路径迅速接近中心。" data-source-page="497" data-source-rect="211,222,359,400">
<figcaption>图 9.14 采用范数 $\|\cdot\|_{P_1}$ 的最速下降法，其迭代点经坐标变换后的情形。这一坐标变换减小了下水平集的条件数，因此加快了收敛。</figcaption>
</figure>

<figure id="fig-9-15" data-figure="9.15" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-15.png" alt="P₂ 范数最速下降法的迭代点经坐标变换后的图形；前两个迭代点旁画有两个完整的圆，虚线等值曲线被横向拉长，迭代路径反复上下摆动。" data-source-page="497" data-source-rect="175,448,395,532">
<figcaption>图 9.15 采用范数 $\|\cdot\|_{P_2}$ 的最速下降法，其迭代点经坐标变换后的情形。这一坐标变换增大了下水平集的条件数，因此减慢了收敛。</figcaption>
</figure>

<!-- pdf-page: 498 -->

<figure id="fig-9-16" data-figure="9.16" data-no-english-text="true" data-reader-after="newton-quadratic-model-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-16.png" alt="函数 f 的实线曲线与在 x 处相切的二阶近似虚线；虚线最低点和其正下方实际函数上的点具有相同横坐标 x+Δx_nt，两个点分别标出。" data-source-page="498" data-source-rect="227,121,431,249">
<figcaption>图 9.16 函数 $f$（实线）及其在点 $x$ 处的二阶近似 $\widehat f$（虚线）。将牛顿步 $\Delta x_{\mathrm{nt}}$ 加到 $x$ 上，就得到 $\widehat f$ 的最小值点。</figcaption>
</figure>

## 9.5 牛顿法

### 9.5.1 牛顿步

对 $x\in\mathbf{dom}\,f$，向量

$$
\Delta x_{\mathrm{nt}}=-\nabla^2f(x)^{-1}\nabla f(x)
$$

称为（$f$ 在 $x$ 处的）*牛顿步*（Newton step）。由 $\nabla^2f(x)$ 正定可知，除非 $\nabla f(x)=0$，否则

$$
\nabla f(x)^T\Delta x_{\mathrm{nt}}=-\nabla f(x)^T\nabla^2f(x)^{-1}\nabla f(x)<0,
$$

所以牛顿步是一个下降方向（除非 $x$ 已经最优）。可以从几个角度解释牛顿步，并说明采用它的理由。

#### 二阶近似的最小化点

$f$ 在 $x$ 处的二阶 Taylor 近似（或模型）$\widehat f$ 为

$$
\widehat f(x+v)=f(x)+\nabla f(x)^Tv+\frac12v^T\nabla^2f(x)v,
\tag{9.28}
$$

这是关于 $v$ 的凸二次函数，在 $v=\Delta x_{\mathrm{nt}}$ 时达到最小值。因此，将牛顿步 $\Delta x_{\mathrm{nt}}$ 加到点 $x$ 上，就得到 $f$ 在 $x$ 处二阶近似的最小化点。图 9.16 说明了这一点。

<p id="newton-quadratic-model-end" markdown="1">这种解释有助于理解牛顿步。如果函数 $f$ 是二次函数，那么 $x+\Delta x_{\mathrm{nt}}$ 就是 $f$ 的精确最小化点。如果函数 $f$ 接近二次函数，直觉上，$x+\Delta x_{\mathrm{nt}}$ 应当是 $f$ 的最小化点，即 $x^\star$，的一个很好的估计。由于 $f$ 二阶可微，当 $x$ 接近 $x^\star$ 时，$f$ 的二次模型会十分准确。因此，当 $x$ 接近 $x^\star$ 时，点 $x+\Delta x_{\mathrm{nt}}$ 应当能很好地估计 $x^\star$。后面将看到，这一直觉是正确的。</p>

<!-- pdf-page: 499 -->

<figure id="fig-9-17" data-figure="9.17" data-no-english-text="true" data-reader-after="newton-hessian-norm-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-17.png" alt="凸函数的虚线等值曲线和以 x 为中心的实线椭圆；负梯度箭头斜向右下方，归一化最速下降步的端点位于椭圆边界，牛顿步的端点位于椭圆外。" data-source-page="499" data-source-rect="229,122,342,300">
<figcaption>图 9.17 虚线是某个凸函数的等值线。实线所示的椭球为 $\{x+v\mid v^T\nabla^2 f(x)v\leq 1\}$。箭头表示 $-\nabla f(x)$，即梯度下降方向。牛顿步 $\Delta x_{\mathrm{nt}}$ 是范数 $\|\cdot\|_{\nabla^2 f(x)}$ 下的最速下降方向。图中还给出了 $\Delta x_{\mathrm{nsd}}$，即同一范数下的归一化最速下降方向。</figcaption>
</figure>

#### Hessian 范数下的最速下降方向

牛顿步也是在 $x$ 处、采用由 Hessian 矩阵 $\nabla^2f(x)$ 定义的二次范数时的最速下降方向。这个范数为

$$
\|u\|_{\nabla^2f(x)}=(u^T\nabla^2f(x)u)^{1/2}.
$$

这从另一个角度说明，为什么牛顿步应当是一个好的搜索方向，以及为什么当 $x$ 接近 $x^\star$ 时，这一搜索方向尤其好。

<p id="newton-hessian-norm-end" markdown="1">回顾前面的讨论：采用二次范数 $\|\cdot\|_P$ 的最速下降法，在相应坐标变换后的 Hessian 矩阵条件数很小时，收敛非常快。特别地，在 $x^\star$ 附近，$P=\nabla^2f(x^\star)$ 是一个很好的选择。当 $x$ 接近 $x^\star$ 时，有 $\nabla^2f(x)\approx\nabla^2f(x^\star)$，这就解释了为什么牛顿步是很好的搜索方向。图 9.17 说明了这一点。</p>

#### 线性化最优性条件的解

在 $x$ 附近将最优性条件 $\nabla f(x^\star)=0$ 线性化，可得

$$
\nabla f(x+v)\approx\nabla f(x)+\nabla^2f(x)v=0,
$$

这是关于 $v$ 的线性方程，其解为 $v=\Delta x_{\mathrm{nt}}$。因此，将牛顿步 $\Delta x_{\mathrm{nt}}$ 加到 $x$ 上，就能使线性化的最优性条件成立。这再次表明，当 $x$ 接近 $x^\star$ 时（此时最优性条件几乎成立），更新后的点 $x+\Delta x_{\mathrm{nt}}$ 应当是 $x^\star$ 的一个很好的近似。

<p id="newton-zero-crossing-start" markdown="1">当 $n=1$，即 $f:\mathbf{R}\to\mathbf{R}$ 时，这一解释尤其简单。最小化问题的解 $x^\star$ 由 $f'(x^\star)=0$ 刻画，也就是说，它是</p>

<!-- pdf-page: 500 -->

<figure id="fig-9-18" data-figure="9.18" data-no-english-text="true" data-reader-after="newton-zero-crossing-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-18.png" alt="函数导数 f′ 的实线曲线与在 x 处的线性近似虚线；虚线在 x+Δx_nt 处穿过水平零线，该横坐标对应的实际导数值仍小于零。" data-source-page="500" data-source-rect="247,122,449,253">
<figcaption>图 9.18 实线曲线是图 9.16 中函数 $f$ 的导数 $f'$。$\widehat f'$ 是 $f'$ 在点 $x$ 处的线性近似。牛顿步 $\Delta x_{\mathrm{nt}}$ 等于 $\widehat f'$ 的根与点 $x$ 之差。</figcaption>
</figure>

<p id="newton-zero-crossing-end" markdown="1" data-reader-continue="newton-zero-crossing-start">导数 $f'$ 的过零点；由于 $f$ 是凸函数，$f'$ 单调递增。给定当前对解的近似 $x$，在 $x$ 处构造 $f'$ 的一阶 Taylor 近似。这个仿射近似的过零点就是 $x+\Delta x_{\mathrm{nt}}$。图 9.18 说明了这一解释。</p>

#### 牛顿步的仿射不变性

牛顿步的一个重要特点是，它不依赖于线性（或仿射）坐标变换。设 $T\in\mathbf{R}^{n\times n}$ 非奇异，并定义 $\bar f(y)=f(Ty)$。则有

$$
\nabla\bar f(y)=T^T\nabla f(x),\qquad
\nabla^2\bar f(y)=T^T\nabla^2f(x)T,
$$

其中 $x=Ty$。因此，$\bar f$ 在 $y$ 处的牛顿步为

$$
\begin{aligned}
\Delta y_{\mathrm{nt}}
&=-\bigl(T^T\nabla^2f(x)T\bigr)^{-1}\bigl(T^T\nabla f(x)\bigr)\\
&=-T^{-1}\nabla^2f(x)^{-1}\nabla f(x)\\
&=T^{-1}\Delta x_{\mathrm{nt}},
\end{aligned}
$$

其中 $\Delta x_{\mathrm{nt}}$ 是 $f$ 在 $x$ 处的牛顿步。因此，$f$ 与 $\bar f$ 的牛顿步由同一个线性变换联系起来，并且

$$
x+\Delta x_{\mathrm{nt}}=T(y+\Delta y_{\mathrm{nt}}).
$$

#### 牛顿减量

量

$$
\lambda(x)=\bigl(\nabla f(x)^T\nabla^2f(x)^{-1}\nabla f(x)\bigr)^{1/2}
$$

称为 $x$ 处的*牛顿减量*（Newton decrement）。后面将看到，牛顿减量在牛顿法的分析中起重要作用，也可用作<!-- pdf-page: 501 -->停止准则。牛顿减量与量 $f(x)-\inf_y\widehat f(y)$ 有如下关系，其中 $\widehat f$ 是 $f$ 在 $x$ 处的二阶近似：

$$
f(x)-\inf_y\widehat f(y)=f(x)-\widehat f(x+\Delta x_{\mathrm{nt}})=\frac12\lambda(x)^2.
$$

因此，$\lambda^2/2$ 是根据 $f$ 在 $x$ 处的二次近似得到的 $f(x)-p^\star$ 的估计。

牛顿减量也可以写成

$$
\lambda(x)=\bigl(\Delta x_{\mathrm{nt}}^T\nabla^2f(x)\Delta x_{\mathrm{nt}}\bigr)^{1/2}.
\tag{9.29}
$$

这表明，$\lambda$ 是牛顿步在 Hessian 矩阵定义的二次范数下的范数，即采用范数

$$
\|u\|_{\nabla^2f(x)}=\bigl(u^T\nabla^2f(x)u\bigr)^{1/2}.
$$

牛顿减量也出现在回溯直线搜索中，因为有

$$
\nabla f(x)^T\Delta x_{\mathrm{nt}}=-\lambda(x)^2.
\tag{9.30}
$$

这是回溯直线搜索中使用的常数，可以解释为 $f$ 在 $x$ 处沿牛顿步方向的方向导数：

$$
-\lambda(x)^2=\nabla f(x)^T\Delta x_{\mathrm{nt}}
=\left.\frac{d}{dt}f(x+\Delta x_{\mathrm{nt}}t)\right|_{t=0}.
$$

最后指出，牛顿减量与牛顿步一样具有仿射不变性。换言之，若 $T$ 非奇异，则 $\bar f(y)=f(Ty)$ 在 $y$ 处的牛顿减量，与 $f$ 在 $x=Ty$ 处的牛顿减量相同。

### 9.5.2 牛顿法

下面给出的牛顿法有时称为*阻尼牛顿法*（damped Newton method）或*带保护的牛顿法*（guarded Newton method），以区别于采用固定步长 $t=1$ 的*纯牛顿法*（pure Newton method）。

<div class="algorithm" id="algorithm-9-5" data-algorithm="9.5" markdown="1">

**算法 9.5 牛顿法。**

**给定** 起始点 $x\in\mathbf{dom}\,f$，容差 $\epsilon>0$。

**重复执行**

1. *计算牛顿步和牛顿减量。*

    $$
    \Delta x_{\mathrm{nt}}:=-\nabla^2f(x)^{-1}\nabla f(x);\qquad
    \lambda^2:=\nabla f(x)^T\nabla^2f(x)^{-1}\nabla f(x).
    $$

2. *停止准则。* 如果 $\lambda^2/2\leq\epsilon$，则退出。
3. *直线搜索。* 用回溯直线搜索选择步长 $t$。
4. *更新。* $x:=x+t\Delta x_{\mathrm{nt}}$。

</div>

这实质上是 §9.2 中介绍的一般下降法，只是采用牛顿步作为搜索方向。唯一的区别（很小的区别）是：停止准则在计算搜索方向之后检查，而不是在更新之后检查。

<!-- pdf-page: 502 -->

### 9.5.3 收敛分析

与前面一样，假设 $f$ 二阶连续可微，且以 $m$ 为常数强凸，即对 $x\in S$ 有 $\nabla^2f(x)\succeq mI$。已经看到，这还意味着存在 $M>0$，使得对所有 $x\in S$ 都有 $\nabla^2f(x)\preceq MI$。

此外，假设 $f$ 的 Hessian 矩阵在 $S$ 上 Lipschitz 连续，常数为 $L$，即对所有 $x,y\in S$，

$$
\|\nabla^2f(x)-\nabla^2f(y)\|_2\leq L\|x-y\|_2.
\tag{9.31}
$$

系数 $L$ 可以解释为 $f$ 的三阶导数的一个界；对于二次函数，可以取 $L=0$。更一般地，$L$ 衡量用二次模型近似 $f$ 的好坏，因此可以预期，Lipschitz 常数 $L$ 会对牛顿法的性能起关键作用。直觉上，对于二次模型变化缓慢（即 $L$ 很小）的函数，牛顿法应当表现很好。

#### 收敛证明的思路和概要

先介绍收敛证明的思路、概要和主要结论，再给出证明的细节。我们将证明，存在数 $\eta$ 和 $\gamma$，满足 $0<\eta\leq m^2/L$ 和 $\gamma>0$，使下列结论成立。

- 如果 $\|\nabla f(x^{(k)})\|_2\geq\eta$，则

    $$
    f(x^{(k+1)})-f(x^{(k)})\leq-\gamma.
    \tag{9.32}
    $$

- 如果 $\|\nabla f(x^{(k)})\|_2<\eta$，则回溯直线搜索选择 $t^{(k)}=1$，并且

    $$
    \frac{L}{2m^2}\|\nabla f(x^{(k+1)})\|_2
    \leq\left(\frac{L}{2m^2}\|\nabla f(x^{(k)})\|_2\right)^2.
    \tag{9.33}
    $$

下面分析第二个条件的含义。假设第 $k$ 次迭代满足这一条件，即 $\|\nabla f(x^{(k)})\|_2<\eta$。由于 $\eta\leq m^2/L$，有 $\|\nabla f(x^{(k+1)})\|_2<\eta$，即第 $k+1$ 次迭代也满足第二个条件。递推下去可知，一旦第二个条件成立，以后的所有迭代点都会满足它，即对所有 $l\geq k$，都有 $\|\nabla f(x^{(l)})\|_2<\eta$。因此，对所有 $l\geq k$，算法都采用完整的牛顿步 $t=1$，并且

$$
\frac{L}{2m^2}\|\nabla f(x^{(l+1)})\|_2
\leq\left(\frac{L}{2m^2}\|\nabla f(x^{(l)})\|_2\right)^2.
\tag{9.34}
$$

递推应用这个不等式，可得对 $l\geq k$，

$$
\frac{L}{2m^2}\|\nabla f(x^{(l)})\|_2
\leq\left(\frac{L}{2m^2}\|\nabla f(x^{(k)})\|_2\right)^{2^{l-k}}
\leq\left(\frac12\right)^{2^{l-k}},
$$

从而

$$
f(x^{(l)})-p^\star
\leq\frac{1}{2m}\|\nabla f(x^{(l)})\|_2^2
\leq\frac{2m^3}{L^2}\left(\frac12\right)^{2^{l-k+1}}.
\tag{9.35}
$$

<!-- pdf-page: 503 -->

最后这个不等式表明，一旦第二个条件满足，收敛就极其迅速。这一现象称为*二次收敛*（quadratic convergence）。粗略地说，不等式 (9.35) 意味着，在经过足够多次迭代后，每次迭代都会使正确数字的位数翻倍。

牛顿法的迭代自然分成两个阶段。第二个阶段从条件 $\|\nabla f(x)\|_2\leq\eta$ 成立时开始，称为*二次收敛阶段*。第一个阶段称为*阻尼牛顿阶段*，因为算法可能选择步长 $t<1$。二次收敛阶段也称为*纯牛顿阶段*，因为在这个阶段的迭代中，总是选择步长 $t=1$。

现在可以估计总的复杂度。首先推导阻尼牛顿阶段迭代次数的上界。由于每次迭代都使 $f$ 至少减小 $\gamma$，阻尼牛顿步的次数不可能超过

$$
\frac{f(x^{(0)})-p^\star}{\gamma},
$$

否则 $f$ 就会小于 $p^\star$，这是不可能的。

利用不等式 (9.35)，可以给出二次收敛阶段的迭代次数界。它意味着，在二次收敛阶段经过不超过

$$
\log_2\log_2(\epsilon_0/\epsilon)
$$

次迭代后，必有 $f(x)-p^\star\leq\epsilon$，其中 $\epsilon_0=2m^3/L^2$。

因此，总的来说，达到 $f(x)-p^\star\leq\epsilon$ 所需的迭代次数上界为

$$
\frac{f(x^{(0)})-p^\star}{\gamma}+\log_2\log_2(\epsilon_0/\epsilon).
\tag{9.36}
$$

其中 $\log_2\log_2(\epsilon_0/\epsilon)$ 是二次收敛阶段的迭代次数界；随着精度要求 $\epsilon$ 的提高，它增长得*极其缓慢*，在实际应用中可以视为常数，例如五或六。（二次收敛阶段的六次迭代能达到约 $\epsilon\approx5\cdot10^{-20}\epsilon_0$ 的精度。）

因此，虽不完全准确，但可以说，使 $f$ 最小所需的牛顿迭代次数的上界为

$$
\frac{f(x^{(0)})-p^\star}{\gamma}+6.
\tag{9.37}
$$

更准确的说法是，(9.37) 给出了算出一个极为精确的解的近似所需的迭代次数界。

#### 阻尼牛顿阶段

现在证明不等式 (9.32)。假设 $\|\nabla f(x)\|_2\geq\eta$。先推导直线搜索所选步长的下界。由强凸性可知，在 $S$ 上有 $\nabla^2f(x)\preceq MI$，因此

$$
\begin{aligned}
f(x+t\Delta x_{\mathrm{nt}})
&\leq f(x)+t\nabla f(x)^T\Delta x_{\mathrm{nt}}+\frac{M\|\Delta x_{\mathrm{nt}}\|_2^2}{2}t^2\\
&\leq f(x)-t\lambda(x)^2+\frac{M}{2m}t^2\lambda(x)^2,
\end{aligned}
$$

<!-- pdf-page: 504 -->

这里使用了 (9.30) 和

$$
\lambda(x)^2=\Delta x_{\mathrm{nt}}^T\nabla^2f(x)\Delta x_{\mathrm{nt}}\geq m\|\Delta x_{\mathrm{nt}}\|_2^2.
$$

步长 $\hat t=m/M$ 满足直线搜索的退出条件，因为

$$
f(x+\hat t\Delta x_{\mathrm{nt}})\leq f(x)-\frac{m}{2M}\lambda(x)^2
\leq f(x)-\alpha\hat t\lambda(x)^2.
$$

因此，直线搜索返回的步长满足 $t\geq\beta m/M$，从而目标函数的变化满足

$$
\begin{aligned}
f(x^+)-f(x)&\leq-\alpha t\lambda(x)^2\\
&\leq-\alpha\beta\frac{m}{M}\lambda(x)^2\\
&\leq-\alpha\beta\frac{m}{M^2}\|\nabla f(x)\|_2^2\\
&\leq-\alpha\beta\eta^2\frac{m}{M^2},
\end{aligned}
$$

这里使用了

$$
\lambda(x)^2=\nabla f(x)^T\nabla^2f(x)^{-1}\nabla f(x)\geq(1/M)\|\nabla f(x)\|_2^2.
$$

因此，取

$$
\gamma=\alpha\beta\eta^2\frac{m}{M^2}
\tag{9.38}
$$

就能使 (9.32) 成立。

#### 二次收敛阶段

现在证明不等式 (9.33)。假设 $\|\nabla f(x)\|_2<\eta$。首先证明，只要

$$
\eta\leq3(1-2\alpha)\frac{m^2}{L},
$$

回溯直线搜索就会选择单位步长。

由 Lipschitz 条件 (9.31)，对 $t\geq0$，有

$$
\|\nabla^2f(x+t\Delta x_{\mathrm{nt}})-\nabla^2f(x)\|_2\leq tL\|\Delta x_{\mathrm{nt}}\|_2,
$$

因此

$$
\left|\Delta x_{\mathrm{nt}}^T\bigl(\nabla^2f(x+t\Delta x_{\mathrm{nt}})-\nabla^2f(x)\bigr)\Delta x_{\mathrm{nt}}\right|
\leq tL\|\Delta x_{\mathrm{nt}}\|_2^3.
$$

令 $\widetilde f(t)=f(x+t\Delta x_{\mathrm{nt}})$，则有 $\widetilde f''(t)=\Delta x_{\mathrm{nt}}^T\nabla^2f(x+t\Delta x_{\mathrm{nt}})\Delta x_{\mathrm{nt}}$，所以上述不等式就是

$$
|\widetilde f''(t)-\widetilde f''(0)|\leq tL\|\Delta x_{\mathrm{nt}}\|_2^3.
$$

将利用这个不等式确定 $\widetilde f(t)$ 的上界。首先有

$$
\widetilde f''(t)\leq\widetilde f''(0)+tL\|\Delta x_{\mathrm{nt}}\|_2^3
\leq\lambda(x)^2+t\frac{L}{m^{3/2}}\lambda(x)^3,
$$

<!-- pdf-page: 505 -->

这里使用了 $\widetilde f''(0)=\lambda(x)^2$ 和 $\lambda(x)^2\geq m\|\Delta x_{\mathrm{nt}}\|_2^2$。对这个不等式积分，得到

$$
\begin{aligned}
\widetilde f'(t)&\leq\widetilde f'(0)+t\lambda(x)^2+t^2\frac{L}{2m^{3/2}}\lambda(x)^3\\
&=-\lambda(x)^2+t\lambda(x)^2+t^2\frac{L}{2m^{3/2}}\lambda(x)^3,
\end{aligned}
$$

这里使用了 $\widetilde f'(0)=-\lambda(x)^2$。再次积分，得到

$$
\widetilde f(t)\leq\widetilde f(0)-t\lambda(x)^2+t^2\frac12\lambda(x)^2
+t^3\frac{L}{6m^{3/2}}\lambda(x)^3.
$$

最后，取 $t=1$，得到

$$
f(x+\Delta x_{\mathrm{nt}})\leq f(x)-\frac12\lambda(x)^2
+\frac{L}{6m^{3/2}}\lambda(x)^3.
\tag{9.39}
$$

现在假设 $\|\nabla f(x)\|_2\leq\eta\leq3(1-2\alpha)m^2/L$。由强凸性，有

$$
\lambda(x)\leq3(1-2\alpha)m^{3/2}/L,
$$

再由 (9.39)，有

$$
\begin{aligned}
f(x+\Delta x_{\mathrm{nt}})&\leq f(x)-\lambda(x)^2\left(\frac12-\frac{L\lambda(x)}{6m^{3/2}}\right)\\
&\leq f(x)-\alpha\lambda(x)^2\\
&=f(x)+\alpha\nabla f(x)^T\Delta x_{\mathrm{nt}},
\end{aligned}
$$

这表明回溯直线搜索会接受单位步长 $t=1$。

下面考察收敛速度。应用 Lipschitz 条件，得到

$$
\begin{aligned}
\|\nabla f(x^+)\|_2
&=\|\nabla f(x+\Delta x_{\mathrm{nt}})-\nabla f(x)-\nabla^2f(x)\Delta x_{\mathrm{nt}}\|_2\\
&=\left\|\int_0^1\bigl(\nabla^2f(x+t\Delta x_{\mathrm{nt}})-\nabla^2f(x)\bigr)\Delta x_{\mathrm{nt}}\,dt\right\|_2\\
&\leq\frac{L}{2}\|\Delta x_{\mathrm{nt}}\|_2^2\\
&=\frac{L}{2}\|\nabla^2f(x)^{-1}\nabla f(x)\|_2^2\\
&\leq\frac{L}{2m^2}\|\nabla f(x)\|_2^2,
\end{aligned}
$$

即不等式 (9.33)。

总之，如果 $\|\nabla f(x^{(k)})\|_2<\eta$，其中

$$
\eta=\min\{1,3(1-2\alpha)\}\frac{m^2}{L},
$$

那么算法会选择单位步长，并满足条件 (9.33)。将这个界和 (9.38) 代入 (9.37)，可得迭代次数的上界为

$$
6+\frac{M^2L^2/m^5}{\alpha\beta\min\{1,9(1-2\alpha)^2\}}\bigl(f(x^{(0)})-p^\star\bigr).
\tag{9.40}
$$

<!-- pdf-page: 506 -->

<figure id="fig-9-19" data-figure="9.19" data-no-english-text="true" data-reader-after="newton-r2-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-19.png" alt="二维问题中牛顿法的迭代路径；在 x⁽⁰⁾ 和 x⁽¹⁾ 处各画有一个倾斜椭圆，少量相连的迭代点迅速到达虚线等值曲线的中心附近。" data-source-page="506" data-source-rect="229,121,448,252">
<figcaption>图 9.19 将牛顿法用于 $\mathbf{R}^2$ 中的问题，目标函数 $f$ 由 (9.20) 给出，回溯直线搜索参数为 $\alpha=0.1$、$\beta=0.7$。图中还画出了前两个迭代点处的椭球 $\{x\mid\|x-x^{(k)}\|_{\nabla^2 f(x^{(k)})}\leq 1\}$。</figcaption>
</figure>

### 9.5.4 例子

#### $\mathbf{R}^2$ 中的例子

首先，对测试函数 (9.20) 应用采用回溯直线搜索的牛顿法，直线搜索参数取 $\alpha=0.1$、$\beta=0.7$。图 9.19 给出了牛顿迭代点，以及前两个迭代点 $k=0,1$ 处的椭球

$$
\{x\mid\|x-x^{(k)}\|_{\nabla^2f(x^{(k)})}\leq1\}.
$$

这种方法效果很好，因为这些椭球很好地近似了下水平集的形状。

<p id="newton-r2-example-end" markdown="1">图 9.20 给出了同一个例子中误差随迭代次数的变化。图中表明，只需五次迭代就能收敛到很高的精度。二次收敛十分明显：最后一步使误差从约 $10^{-5}$ 减小到 $10^{-10}$。</p>

#### $\mathbf{R}^{100}$ 中的例子

图 9.21 给出了对于 $\mathbf{R}^{100}$ 中一个问题，分别采用回溯直线搜索和精确直线搜索的牛顿法的收敛情况。目标函数具有 (9.21) 的形式，问题数据和起始点与图 9.6 使用的相同。回溯直线搜索对应的曲线表明，八次迭代就能达到很高的精度。与 $\mathbf{R}^2$ 中的例子一样，大约从第三次迭代之后开始，二次收敛就十分明显。采用精确直线搜索的牛顿法，迭代次数只比采用回溯直线搜索时少一次。这也是一种典型情形。精确直线搜索通常只能使牛顿法的收敛略有改善。图 9.22 给出了这个例子中的步长。在两个阻尼步之后，回溯直线搜索所取的步长都是完整步长，即 $t=1$。

<p id="newton-backtracking-parameters-start" markdown="1">对回溯参数 $\alpha$ 和 $\beta$ 的取值进行实验可知，它们对这个例子</p>

<!-- pdf-page: 507 -->

<figure id="fig-9-20" data-figure="9.20" data-no-english-text="true" data-reader-after="newton-backtracking-parameters-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-20.png" alt="二维问题中牛顿法的误差随迭代次数 k 从 0 到 5 迅速下降；纵轴采用对数刻度，最后一次迭代后的误差低于 10⁻¹⁰。" data-source-page="507" data-source-rect="148,142,394,326">
<figcaption>图 9.20 对于 $\mathbf{R}^2$ 中的问题，牛顿法的误差随迭代次数 $k$ 的变化。经过 $5$ 次迭代就达到了很高的精度。</figcaption>
</figure>

<figure id="fig-9-21" data-figure="9.21" data-reader-after="newton-backtracking-parameters-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-21.png" alt="一百维问题中牛顿法的两条误差曲线，纵轴采用对数刻度；菱形标记的精确直线搜索曲线在第 7 次迭代、圆圈标记的回溯直线搜索曲线在第 8 次迭代达到很小的误差。" data-source-page="507" data-source-rect="148,413,406,599">
<figcaption>图 9.21 对于 $\mathbf{R}^{100}$ 中的问题，牛顿法的误差随迭代次数的变化。回溯直线搜索参数为 $\alpha=0.01$、$\beta=0.5$。这里的收敛同样极快：仅需 $7$ 次或 $8$ 次迭代便达到了很高的精度。采用精确直线搜索时，牛顿法达到收敛所需的迭代次数仅比采用回溯直线搜索时少一次。</figcaption>
<p class="figure-translation">图内文字：backtracking l.s.——回溯直线搜索；exact l.s.——精确直线搜索。</p>
</figure>

<!-- pdf-page: 508 -->

<figure id="fig-9-22" data-figure="9.22" data-reader-after="newton-backtracking-parameters-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-22.png" alt="牛顿法的步长随迭代次数 k 变化；回溯直线搜索前两次的步长为 0.5，此后为 1，精确直线搜索的步长先升至约 1.6，再逐渐接近 1。" data-source-page="508" data-source-rect="211,122,447,307">
<figcaption>图 9.22 将采用回溯直线搜索和精确直线搜索的牛顿法用于 $\mathbf{R}^{100}$ 中的问题时，步长 $t$ 随迭代次数的变化。回溯直线搜索在前两次迭代中各回溯一步。前两次迭代之后，它总是选择 $t=1$。</figcaption>
<p class="figure-translation">图内文字：step size $t^{(k)}$——步长 $t^{(k)}$；exact l.s.——精确直线搜索；backtracking l.s.——回溯直线搜索。</p>
</figure>

<p id="newton-backtracking-parameters-end" markdown="1" data-reader-continue="newton-backtracking-parameters-start">（以及其他例子）中牛顿法的性能影响很小。将 $\alpha$ 固定为 $0.01$，让 $\beta$ 在 $0.2$ 到 $1$ 之间变化，所需迭代次数在 $8$ 到 $12$ 之间变化。将 $\beta$ 固定为 $0.5$，则对 $0.005$ 到 $0.5$ 之间的所有 $\alpha$ 值，迭代次数都是 $8$。因此，大多数实际实现采用回溯直线搜索，并选择较小的 $\alpha$（如 $0.01$）和较大的 $\beta$（如 $0.5$）。</p>

#### $\mathbf{R}^{10000}$ 中的例子

最后这个例子考虑一个更大的问题，其形式为

$$
\begin{array}{ll}
\text{最小化} & -\displaystyle\sum_{i=1}^n\log(1-x_i^2)-\displaystyle\sum_{i=1}^m\log(b_i-a_i^Tx),
\end{array}
$$

其中 $m=100000$，$n=10000$。问题数据 $a_i$ 是随机生成的稀疏向量。图 9.23 给出了采用回溯直线搜索的牛顿法的收敛情况，参数为 $\alpha=0.01$、$\beta=0.5$。其表现与前面的收敛曲线非常相似。开始时约 $13$ 次迭代构成一个线性收敛阶段，随后进入二次收敛阶段，再经过 $4$ 或 $5$ 次迭代，就能达到很高的精度。

#### 牛顿法的仿射不变性

<p id="newton-affine-equivalence-start" markdown="1">牛顿法的一个非常重要的特点是，它不依赖于线性（或仿射）坐标变换。设 $x^{(k)}$ 是对 $f:\mathbf{R}^n\to\mathbf{R}$ 应用牛顿法得到的第 $k$ 个迭代点。设 $T\in\mathbf{R}^{n\times n}$ 非奇异，并定义 $\bar f(y)=f(Ty)$。如果采用牛顿法（回溯参数保持相同），</p>

<!-- pdf-page: 509 -->

<figure id="fig-9-23" data-figure="9.23" data-no-english-text="true" data-reader-after="newton-affine-equivalence-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-23.png" alt="一万维问题中牛顿法的误差随迭代次数 k 下降，纵轴采用对数刻度；曲线在后几次迭代明显变陡，第 18 次迭代后的误差低于 10⁻⁵。" data-source-page="509" data-source-rect="150,122,398,306">
<figcaption>图 9.23 对于 $\mathbf{R}^{10000}$ 中的一个问题，牛顿法的误差随迭代次数的变化。这里使用回溯直线搜索，参数为 $\alpha=0.01$、$\beta=0.5$。即使对于这样的大规模问题，牛顿法也只需 $18$ 次迭代就能达到很高的精度。</figcaption>
</figure>

<p id="newton-affine-equivalence-middle" markdown="1" data-reader-continue="newton-affine-equivalence-start">从 $y^{(0)}=T^{-1}x^{(0)}$ 出发最小化 $\bar f$，则对所有 $k$ 都有</p>

$$
Ty^{(k)}=x^{(k)}.
$$

<p id="newton-affine-equivalence-end" markdown="1">换言之，牛顿法保持不变：两组迭代点由同一个坐标变换联系起来。甚至停止准则也相同，因为 $\bar f$ 在 $y^{(k)}$ 处的牛顿减量，与 $f$ 在 $x^{(k)}$ 处的牛顿减量相同。这与梯度法（或最速下降法）形成鲜明对比；后两者会受到坐标变换的强烈影响。</p>

例如，考虑 (9.22) 给出的一族问题，以参数 $\gamma$ 为索引；$\gamma$ 会影响下水平集的条件数。前面（在图 9.7 和图 9.8 中）已经看到，当 $\gamma$ 小于 $0.05$ 或大于 $20$ 时，梯度法慢到失去实用价值。相比之下，对 $10^{-10}$ 到 $10^{10}$ 之间的所有 $\gamma$ 值，牛顿法（取 $\alpha=0.01$、$\beta=0.5$）都只需九次迭代就能求解这个问题（而且实际上达到的精度还高得多）。

在使用有限精度运算的实际实现中，牛顿法并非完全不受仿射坐标变换或下水平集条件数的影响。不过，可以说，条件数即使大到 $10^{10}$，也不会给牛顿法的实际实现带来不利影响。梯度法能够容忍的条件数范围要小得多。坐标的选择（或下水平集的条件数）对梯度法和最速下降法是首要问题，对牛顿法则是次要问题；它只会影响计算牛顿步所需的数值线性代数运算。

<!-- pdf-page: 510 -->

#### 小结

与梯度法和最速下降法相比，牛顿法有几个突出的优点：

- 牛顿法通常收敛很快，在 $x^\star$ 附近则二次收敛。一旦进入二次收敛阶段，最多再用六次左右的迭代，就能得到精度很高的解。

- 牛顿法具有仿射不变性。它对坐标的选择以及目标函数下水平集的条件数不敏感。

- 问题规模增大时，牛顿法仍有良好的表现。它对 $\mathbf{R}^{10000}$ 中问题的表现，与对 $\mathbf{R}^{10}$ 中问题的表现相似，所需步数只略有增加。

- 牛顿法的良好性能不依赖于算法参数的选择。相比之下，最速下降法中范数的选择对其性能起关键作用。

牛顿法的主要缺点，是形成和存储 Hessian 矩阵的开销，以及计算牛顿步的开销；后者需要求解一组线性方程。§9.7 将说明，在许多情况下，可以利用问题结构大幅降低计算牛顿步的开销。

另一种选择是一类称为*拟牛顿法*（quasi-Newton methods）的无约束优化算法。这些方法形成搜索方向所需的计算量较少，同时又具有牛顿法的一些突出优点，例如在 $x^\star$ 附近快速收敛。许多书籍已经介绍了拟牛顿法，而且它们与本书的主线关系不大，因此本书不讨论这些方法。

## 9.6 自协调性

§9.5.3 给出的牛顿法经典收敛分析有两个主要不足。第一个与实际应用有关：得到的复杂度估计涉及三个常数 $m$、$M$ 和 $L$，而它们在实际中几乎总是未知的。因此，牛顿步所需次数的界 (9.40) 几乎总是无法具体确定，因为它依赖于这三个通常未知的常数。当然，收敛分析和复杂度估计在概念上仍然有用。

第二个不足是：牛顿法本身具有仿射不变性，但对牛顿法的经典分析却非常依赖所用的坐标系。如果改变坐标，常数 $m$、$M$ 和 $L$ 都会改变。即使仅仅出于形式上的美感，也应当寻找一种与牛顿法本身一样、不依赖仿射坐标变换的分析方法。<!-- pdf-page: 511 -->换言之，希望用一种不依赖仿射坐标变换、同时又能用来分析牛顿法的假设，替代

$$
mI\preceq\nabla^2f(x)\preceq MI,\qquad
\|\nabla^2f(x)-\nabla^2f(y)\|_2\leq L\|x-y\|_2.
$$

Nesterov 和 Nemirovski 找到了一种简单而优美、能达到这个目标的假设，并将这个条件命名为*自协调性*（self-concordance）。自协调函数的重要性体现在以下几个方面。

- 它们包括许多对数障碍函数；这些函数在求解凸优化问题的内点法中起重要作用。

- 对自协调函数进行牛顿法分析，不依赖任何未知常数。

- 自协调性是一个仿射不变的性质，即对自协调函数的变量作线性变换，得到的仍是自协调函数。因此，将牛顿法用于自协调函数时，得到的复杂度估计不依赖仿射坐标变换。

### 9.6.1 定义和例子

#### $\mathbf{R}$ 上的自协调函数

先考虑 $\mathbf{R}$ 上的函数。如果凸函数 $f:\mathbf{R}\to\mathbf{R}$ 对所有 $x\in\mathbf{dom}\,f$ 都满足

$$
|f'''(x)|\leq2f''(x)^{3/2},
\tag{9.41}
$$

就称它为*自协调函数*（self-concordant function）。由于线性函数和（凸）二次函数的三阶导数为零，它们显然都是自协调函数。下面给出一些更有意思的例子。

<div class="example" id="example-9-3" markdown="1">

**例 9.3 对数和熵。**

- *负对数。* 函数 $f(x)=-\log x$ 是自协调的。利用 $f''(x)=1/x^2$、$f'''(x)=-2/x^3$，可得

    $$
    \frac{|f'''(x)|}{2f''(x)^{3/2}}=\frac{2/x^3}{2(1/x^2)^{3/2}}=1,
    $$

    所以定义中的不等式 (9.41) 取等号。

- *负熵加负对数。* 函数 $f(x)=x\log x-\log x$ 是自协调的。为验证这一点，利用

    $$
    f''(x)=\frac{x+1}{x^2},\qquad f'''(x)=-\frac{x+2}{x^3},
    $$

    得到

    $$
    \frac{|f'''(x)|}{2f''(x)^{3/2}}=\frac{x+2}{2(x+1)^{3/2}}.
    $$

    <!-- pdf-page: 512 -->

    右端的函数在 $\mathbf{R}_+$ 上于 $x=0$ 处达到最大值，值为 $1$。

    负熵函数本身*不是*自协调的；见习题 11.13。

</div>

关于自协调性的定义 (9.41)，有两点重要说明。第一点与定义中看似神秘的常数 $2$ 有关。实际上，选择这个常数是为了方便，以简化后面的公式；也可以用任何其他正常数替代。例如，假设凸函数 $f:\mathbf{R}\to\mathbf{R}$ 满足

$$
|f'''(x)|\leq kf''(x)^{3/2},
\tag{9.42}
$$

其中 $k$ 是某个正常数。则函数 $\widetilde f(x)=(k^2/4)f(x)$ 满足

$$
\begin{aligned}
|\widetilde f'''(x)|&=(k^2/4)|f'''(x)|\\
&\leq(k^3/4)f''(x)^{3/2}\\
&=(k^3/4)\bigl((4/k^2)\widetilde f''(x)\bigr)^{3/2}\\
&=2\widetilde f''(x)^{3/2},
\end{aligned}
$$

因而是自协调的。这说明，只要一个函数对某个正的 $k$ 满足 (9.42)，就可以通过缩放，使它满足标准的自协调不等式 (9.41)。因此，重要的是函数三阶导数的绝对值，以其二阶导数的 $3/2$ 次幂的某个倍数为界。通过适当缩放函数，可以将这个倍数变成常数 $2$。

第二点说明只需一个简单计算，就能显示自协调性为什么如此重要：它具有仿射不变性。设通过 $\widetilde f(y)=f(ay+b)$ 定义函数 $\widetilde f$，其中 $a\neq0$。则 $\widetilde f$ 自协调，当且仅当 $f$ 自协调。为说明这一点，将

$$
\widetilde f''(y)=a^2f''(x),\qquad \widetilde f'''(y)=a^3f'''(x),
$$

其中 $x=ay+b$，代入 $\widetilde f$ 的自协调不等式，即 $|\widetilde f'''(y)|\leq2\widetilde f''(y)^{3/2}$，得到

$$
|a^3f'''(x)|\leq2(a^2f''(x))^{3/2},
$$

这个式子（除以 $a^3$ 后）就是 $f$ 的自协调不等式。粗略地说，自协调条件 (9.41) 是一种限制函数三阶导数、同时又不依赖仿射坐标变换的方法。

<div class="translator-note" markdown="1">

**译注：缩放因子的绝对值。** 此处两端的公共因子是 $|a|^3$；因 $a\ne0$，除以 $|a|^3$ 后即得 $f$ 的自协调不等式。

</div>

#### $\mathbf{R}^n$ 上的自协调函数

现在考虑 $\mathbf{R}^n$ 上的函数，其中 $n>1$。如果函数 $f:\mathbf{R}^n\to\mathbf{R}$ 沿其定义域内的每一条直线都是自协调的，即对所有 $x\in\mathbf{dom}\,f$ 和所有 $v$，函数 $\widetilde f(t)=f(x+tv)$ 都是关于 $t$ 的自协调函数，就称 $f$ 为*自协调函数*。

<!-- pdf-page: 513 -->

### 9.6.2 自协调函数的运算规则

#### 缩放与求和

乘以大于一的因子会保持自协调性：如果 $f$ 自协调，且 $a\geq1$，则 $af$ 自协调。相加也保持自协调性：如果 $f_1$、$f_2$ 自协调，则 $f_1+f_2$ 自协调。为证明这一点，只需考虑函数 $f_1,f_2:\mathbf{R}\to\mathbf{R}$。有

$$
\begin{aligned}
|f_1'''(x)+f_2'''(x)|&\leq|f_1'''(x)|+|f_2'''(x)|\\
&\leq2\bigl(f_1''(x)^{3/2}+f_2''(x)^{3/2}\bigr)\\
&\leq2\bigl(f_1''(x)+f_2''(x)\bigr)^{3/2}.
\end{aligned}
$$

最后一步使用了对 $u,v\geq0$ 成立的不等式

$$
(u^{3/2}+v^{3/2})^{2/3}\leq u+v.
$$

#### 与仿射函数复合

如果 $f:\mathbf{R}^n\to\mathbf{R}$ 自协调，且 $A\in\mathbf{R}^{n\times m}$、$b\in\mathbf{R}^n$，则 $f(Ax+b)$ 自协调。

<div class="example" id="example-9-4" markdown="1">

**例 9.4 线性不等式的对数障碍函数。** 函数

$$
f(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx),
$$

定义域为 $\mathbf{dom}\,f=\{x\mid a_i^Tx<b_i,\ i=1,\ldots,m\}$，是自协调的。每一项 $-\log(b_i-a_i^Tx)$ 都是 $-\log y$ 与仿射变换 $y=b_i-a_i^Tx$ 的复合，因此是自协调的。所以，它们的和也自协调。

</div>

<div class="example" id="example-9-5" markdown="1">

**例 9.5 对数行列式。** 函数 $f(X)=-\log\det X$ 在 $\mathbf{dom}\,f=\mathbf{S}_{++}^n$ 上自协调。为证明这一点，考虑函数 $\widetilde f(t)=f(X+tV)$，其中 $X\succ0$，$V\in\mathbf{S}^n$。它可以写成

$$
\begin{aligned}
\widetilde f(t)&=-\log\det\bigl(X^{1/2}(I+tX^{-1/2}VX^{-1/2})X^{1/2}\bigr)\\
&=-\log\det X-\log\det(I+tX^{-1/2}VX^{-1/2})\\
&=-\log\det X-\sum_{i=1}^n\log(1+t\lambda_i),
\end{aligned}
$$

其中 $\lambda_i$ 是 $X^{-1/2}VX^{-1/2}$ 的特征值。每一项 $-\log(1+t\lambda_i)$ 都是关于 $t$ 的自协调函数，所以其和 $\widetilde f$ 是自协调的。因此 $f$ 自协调。

</div>

<div class="example" id="example-9-6" markdown="1">

**例 9.6 凹二次函数的对数。** 函数

$$
f(x)=-\log(x^TPx+q^Tx+r),
$$

<!-- pdf-page: 514 -->

其中 $P\in-\mathbf{S}_+^n$，在

$$
\mathbf{dom}\,f=\{x\mid x^TPx+q^Tx+r>0\}
$$

上自协调。为证明这一点，只需考虑 $n=1$ 的情形（因为将 $f$ 限制到一条直线上，就能将一般情形化为 $n=1$ 的情形）。此时可以将 $f$ 写成

$$
f(x)=-\log(px^2+qx+r)=-\log\bigl(-p(x-a)(b-x)\bigr),
$$

其中 $\mathbf{dom}\,f=(a,b)$（即 $a$ 和 $b$ 是 $px^2+qx+r$ 的根）。利用这个表达式，有

$$
f(x)=-\log(-p)-\log(x-a)-\log(b-x),
$$

由此可知 $f$ 自协调。

</div>

#### 与对数函数复合

设 $g:\mathbf{R}\to\mathbf{R}$ 是凸函数，$\mathbf{dom}\,g=\mathbf{R}_{++}$，并且对所有 $x$，

$$
|g'''(x)|\leq3\frac{g''(x)}{x}.
\tag{9.43}
$$

则

$$
f(x)=-\log(-g(x))-\log x
$$

在 $\{x\mid x>0,\ g(x)<0\}$ 上自协调。（证明见习题 9.14。）

条件 (9.43) 是齐次的，并且在相加时保持成立。所有（凸）二次函数，即形如 $ax^2+bx+c$、其中 $a\geq0$ 的函数，都满足这个条件。因此，如果函数 $g$ 满足 (9.43)，那么函数 $g(x)+ax^2+bx+c$ 也满足这个条件，其中 $a\geq0$。

<div class="example" id="example-9-7" markdown="1">

**例 9.7** 下列函数 $g$ 满足条件 (9.43)。

- $g(x)=-x^p$，其中 $0<p\leq1$。
- $g(x)=-\log x$。
- $g(x)=x\log x$。
- $g(x)=x^p$，其中 $-1\leq p\leq0$。
- $g(x)=(ax+b)^2/x$。

因此，在每种情形下，函数 $f(x)=-\log(-g(x))-\log x$ 都是自协调的。更一般地，只要 $a\geq0$，函数 $f(x)=-\log(-g(x)-ax^2-bx-c)-\log x$ 就在其定义域

$$
\{x\mid x>0,\ g(x)+ax^2+bx+c<0\}
$$

上自协调。

</div>

<div class="example" id="example-9-8" markdown="1">

**例 9.8** 利用与对数函数复合的规则，可以证明下列函数的自协调性。

- $f(x,y)=-\log(y^2-x^Tx)$，定义域为 $\{(x,y)\mid\|x\|_2<y\}$。
- $f(x,y)=-2\log y-\log(y^{2/p}-x^2)$，其中 $p\geq1$，定义域为 $\{(x,y)\in\mathbf{R}^2\mid|x|^p<y\}$。
- $f(x,y)=-\log y-\log(\log y-x)$，定义域为 $\{(x,y)\mid e^x<y\}$。

细节留作习题（习题 9.15）。

</div>

<!-- pdf-page: 515 -->

### 9.6.3 自协调函数的性质

在 §9.1.2 中，利用强凸性，根据点 $x$ 处梯度的范数，推导了 $x$ 的次优程度界。对于严格凸的自协调函数，可以用牛顿减量

$$
\lambda(x)=\bigl(\nabla f(x)^T\nabla^2f(x)^{-1}\nabla f(x)\bigr)^{1/2}
$$

得到类似的界。（可以证明，严格凸自协调函数的 Hessian 矩阵处处正定；见习题 9.17。）与基于梯度范数的界不同，基于牛顿减量的界不受仿射坐标变换影响。

为供后面使用，指出牛顿减量还可以表示为

$$
\lambda(x)=\sup_{v\neq0}\frac{-v^T\nabla f(x)}{(v^T\nabla^2f(x)v)^{1/2}}
$$

（见习题 9.9）。换言之，对任意非零的 $v$，有

$$
\frac{-v^T\nabla f(x)}{(v^T\nabla^2f(x)v)^{1/2}}\leq\lambda(x),
\tag{9.44}
$$

当 $v=\Delta x_{\mathrm{nt}}$ 时取等号。

#### 二阶导数的上下界

设 $f:\mathbf{R}\to\mathbf{R}$ 是严格凸的自协调函数。可以将自协调不等式 (9.41) 写成

$$
\left|\frac{d}{dt}\bigl(f''(t)^{-1/2}\bigr)\right|\leq1,
\tag{9.45}
$$

对所有 $t\in\mathbf{dom}\,f$ 成立（见习题 9.16）。假设 $t\geq0$，且 $0$ 与 $t$ 之间的区间包含在 $\mathbf{dom}\,f$ 中，那么将 (9.45) 从 $0$ 到 $t$ 积分，可得

$$
-t\leq\int_0^t\frac{d}{d\tau}\bigl(f''(\tau)^{-1/2}\bigr)\,d\tau\leq t,
$$

即 $-t\leq f''(t)^{-1/2}-f''(0)^{-1/2}\leq t$。由此得到 $f''(t)$ 的下界和上界：

$$
\frac{f''(0)}{\bigl(1+tf''(0)^{1/2}\bigr)^2}
\leq f''(t)\leq
\frac{f''(0)}{\bigl(1-tf''(0)^{1/2}\bigr)^2}.
\tag{9.46}
$$

下界对所有非负的 $t\in\mathbf{dom}\,f$ 有效；上界在 $t\in\mathbf{dom}\,f$ 且 $0\leq t<f''(0)^{-1/2}$ 时有效。

#### 次优程度界

设 $f:\mathbf{R}^n\to\mathbf{R}$ 是严格凸的自协调函数，$v$ 是一个下降方向（即任何满足 $v^T\nabla f(x)<0$ 的方向，不一定是<!-- pdf-page: 516 -->牛顿方向）。定义 $\widetilde f:\mathbf{R}\to\mathbf{R}$ 为 $\widetilde f(t)=f(x+tv)$。根据定义，函数 $\widetilde f$ 是自协调的。

对 (9.46) 中的下界积分，得到 $\widetilde f'(t)$ 的一个下界：

$$
\widetilde f'(t)\geq\widetilde f'(0)+\widetilde f''(0)^{1/2}
-\frac{\widetilde f''(0)^{1/2}}{1+t\widetilde f''(0)^{1/2}}.
\tag{9.47}
$$

再次积分，得到 $\widetilde f(t)$ 的一个下界：

$$
\widetilde f(t)\geq\widetilde f(0)+t\widetilde f'(0)+t\widetilde f''(0)^{1/2}
-\log\bigl(1+t\widetilde f''(0)^{1/2}\bigr).
\tag{9.48}
$$

右端在

$$
\bar t=\frac{-\widetilde f'(0)}{\widetilde f''(0)+\widetilde f''(0)^{1/2}\widetilde f'(0)}
$$

处达到最小值；在 $\bar t$ 处求值，得到 $\widetilde f$ 的一个下界：

$$
\begin{aligned}
\inf_{t\geq0}\widetilde f(t)
&\geq\widetilde f(0)+\bar t\widetilde f'(0)+\bar t\widetilde f''(0)^{1/2}
-\log\bigl(1+\bar t\widetilde f''(0)^{1/2}\bigr)\\
&=\widetilde f(0)-\widetilde f'(0)\widetilde f''(0)^{-1/2}
+\log\bigl(1+\widetilde f'(0)\widetilde f''(0)^{-1/2}\bigr).
\end{aligned}
$$

不等式 (9.44) 可以写成

$$
\lambda(x)\geq-\widetilde f'(0)\widetilde f''(0)^{-1/2}
$$

（当 $v=\Delta x_{\mathrm{nt}}$ 时取等号），因为有

$$
\widetilde f'(0)=v^T\nabla f(x),\qquad
\widetilde f''(0)=v^T\nabla^2f(x)v.
$$

现在利用 $u+\log(1-u)$ 关于 $u$ 单调递减这一事实，以及上面的不等式，得到

$$
\inf_{t\geq0}\widetilde f(t)\geq\widetilde f(0)+\lambda(x)+\log(1-\lambda(x)).
$$

这个不等式对任何下降方向 $v$ 都成立。因此，只要 $\lambda(x)<1$，就有

$$
p^\star\geq f(x)+\lambda(x)+\log(1-\lambda(x)).
\tag{9.49}
$$

图 9.24 绘出了函数 $-(\lambda+\log(1-\lambda))$。当 $\lambda$ 很小时，它满足

$$
-(\lambda+\log(1-\lambda))\approx\lambda^2/2,
$$

当 $\lambda\leq0.68$ 时，则满足界

$$
-(\lambda+\log(1-\lambda))\leq\lambda^2.
$$

因此，得到次优程度界

$$
p^\star\geq f(x)-\lambda(x)^2,
\tag{9.50}
$$

它在 $\lambda(x)\leq0.68$ 时有效。

回顾前面的结论：$\lambda(x)^2/2$ 是基于 $x$ 处二次模型得到的 $f(x)-p^\star$ 的估计；不等式 (9.50) 表明，对于自协调函数，将这个估计乘以二，就得到一个可以证明的界。特别地，这说明对于自协调函数，可以采用停止准则

$$
\lambda(x)^2\leq\epsilon,
$$

其中 $\epsilon<0.68^2$，并保证退出时有 $f(x)-p^\star\leq\epsilon$。

<!-- pdf-page: 517 -->

<figure id="fig-9-24" data-figure="9.24" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-24.png" alt="实线函数 −(λ+log(1−λ)) 与虚线 λ² 从原点出发；在 λ 不超过约 0.68 的区间，虚线位于实线上方，之后实线增长更快。" data-source-page="517" data-source-rect="185,121,375,274">
<figcaption>图 9.24 实线表示函数 $-(\lambda+\log(1-\lambda))$，当 $\lambda$ 较小时，它近似等于 $\lambda^2/2$。虚线表示 $\lambda^2$，在区间 $0\leq\lambda\leq 0.68$ 内，它是前者的上界。</figcaption>
</figure>

### 9.6.4 自协调函数的牛顿法分析

现在分析将采用回溯直线搜索的牛顿法用于严格凸自协调函数 $f$ 的情形。与前面一样，假设已知起始点 $x^{(0)}$，且下水平集 $S=\{x\mid f(x)\leq f(x^{(0)})\}$ 是闭集。还假设 $f$ 有下界。（这意味着 $f$ 有最小化点 $x^\star$；见习题 9.19。）

这一分析与 §9.5.2 给出的经典分析非常相似，只是用自协调性作为基本假设，替代强凸性和 Hessian 矩阵的 Lipschitz 条件，同时用牛顿减量起到梯度范数的作用。我们将证明，存在数 $\eta$ 和 $\gamma>0$，满足 $0<\eta\leq1/4$，它们仅依赖于直线搜索参数 $\alpha$ 和 $\beta$，并使下列结论成立：

- 如果 $\lambda(x^{(k)})>\eta$，则

    $$
    f(x^{(k+1)})-f(x^{(k)})\leq-\gamma.
    \tag{9.51}
    $$

- 如果 $\lambda(x^{(k)})\leq\eta$，则回溯直线搜索选择 $t=1$，并且

    $$
    2\lambda(x^{(k+1)})\leq\bigl(2\lambda(x^{(k)})\bigr)^2.
    \tag{9.52}
    $$

它们分别对应于 (9.32) 和 (9.33)。与 §9.5.3 一样，可以递推应用第二个条件，因此可知，对所有 $l\geq k$，都有 $\lambda(x^{(l)})\leq\eta$，并且

$$
2\lambda(x^{(l)})\leq\bigl(2\lambda(x^{(k)})\bigr)^{2^{l-k}}
\leq(2\eta)^{2^{l-k}}\leq\left(\frac12\right)^{2^{l-k}}.
$$

从而，对所有 $l\geq k$，

$$
f(x^{(l)})-p^\star\leq\lambda(x^{(l)})^2
\leq\frac14\left(\frac12\right)^{2^{l-k+1}}
\leq\left(\frac12\right)^{2^{l-k+1}},
$$

<!-- pdf-page: 518 -->

因此，当 $l-k\geq\log_2\log_2(1/\epsilon)$ 时，就有 $f(x^{(l)})-p^\star\leq\epsilon$。

第一个不等式意味着，阻尼阶段所需步数不会超过 $(f(x^{(0)})-p^\star)/\gamma$。因此，从点 $x^{(0)}$ 出发，达到精度 $f(x)-p^\star\leq\epsilon$ 所需的总迭代次数，以

$$
\frac{f(x^{(0)})-p^\star}{\gamma}+\log_2\log_2(1/\epsilon)
\tag{9.53}
$$

为界。它对应于牛顿法经典分析中的界 (9.36)。

#### 阻尼牛顿阶段

令 $\widetilde f(t)=f(x+t\Delta x_{\mathrm{nt}})$，则有

$$
\widetilde f'(0)=-\lambda(x)^2,\qquad \widetilde f''(0)=\lambda(x)^2.
$$

将 (9.46) 中的上界积分两次，就得到 $\widetilde f(t)$ 的上界：

$$
\begin{aligned}
\widetilde f(t)&\leq\widetilde f(0)+t\widetilde f'(0)-t\widetilde f''(0)^{1/2}
-\log\bigl(1-t\widetilde f''(0)^{1/2}\bigr)\\
&=\widetilde f(0)-t\lambda(x)^2-t\lambda(x)-\log(1-t\lambda(x)),
\end{aligned}
\tag{9.54}
$$

它在 $0\leq t<1/\lambda(x)$ 时有效。

利用这个界，可以证明回溯直线搜索返回的步长总是满足 $t\geq\beta/(1+\lambda(x))$。为证明这一点，注意到 $\hat t=1/(1+\lambda(x))$ 满足直线搜索的退出条件：

$$
\begin{aligned}
\widetilde f(\hat t)&\leq\widetilde f(0)-\hat t\lambda(x)^2-\hat t\lambda(x)-\log(1-\hat t\lambda(x))\\
&=\widetilde f(0)-\lambda(x)+\log(1+\lambda(x))\\
&\leq\widetilde f(0)-\alpha\frac{\lambda(x)^2}{1+\lambda(x)}\\
&=\widetilde f(0)-\alpha\lambda(x)^2\hat t.
\end{aligned}
$$

第二个不等式来自以下事实：对 $x\geq0$，

$$
-x+\log(1+x)+\frac{x^2}{2(1+x)}\leq0.
$$

由于 $t\geq\beta/(1+\lambda(x))$，有

$$
\widetilde f(t)-\widetilde f(0)\leq-\alpha\beta\frac{\lambda(x)^2}{1+\lambda(x)},
$$

所以取

$$
\gamma=\alpha\beta\frac{\eta^2}{1+\eta}
$$

就能使 (9.51) 成立。

<!-- pdf-page: 519 -->

#### 二次收敛阶段

我们将证明，可以取

$$
\eta=(1-2\alpha)/4,
$$

（由于 $0<\alpha<1/2$，它满足 $0<\eta<1/4$），即如果 $\lambda(x^{(k)})\leq(1-2\alpha)/4$，则回溯直线搜索接受单位步长，并且 (9.52) 成立。

首先注意到，上界 (9.54) 意味着，如果 $\lambda(x)<1$，则采用单位步长 $t=1$ 后得到的点属于 $\mathbf{dom}\,f$。此外，如果 $\lambda(x)\leq(1-2\alpha)/2$，则由 (9.54) 有

$$
\begin{aligned}
\widetilde f(1)&\leq\widetilde f(0)-\lambda(x)^2-\lambda(x)-\log(1-\lambda(x))\\
&\leq\widetilde f(0)-\frac12\lambda(x)^2+\lambda(x)^3\\
&\leq\widetilde f(0)-\alpha\lambda(x)^2,
\end{aligned}
$$

所以单位步长满足充分下降条件。（第二行来自以下事实：对 $0\leq x\leq0.81$，有 $-x-\log(1-x)\leq\frac12x^2+x^3$。）

不等式 (9.52) 来自下面这个结论，其证明见习题 9.18。如果 $\lambda(x)<1$，且 $x^+=x-\nabla^2f(x)^{-1}\nabla f(x)$，则

$$
\lambda(x^+)\leq\frac{\lambda(x)^2}{(1-\lambda(x))^2}.
\tag{9.55}
$$

特别地，如果 $\lambda(x)\leq1/4$，则

$$
\lambda(x^+)\leq2\lambda(x)^2,
$$

这就证明了，当 $\lambda(x^{(k)})\leq\eta$ 时，(9.52) 成立。

#### 最终的复杂度界

综合以上结果，牛顿迭代次数的界 (9.53) 变为

$$
\frac{f(x^{(0)})-p^\star}{\gamma}+\log_2\log_2(1/\epsilon)
=\frac{20-8\alpha}{\alpha\beta(1-2\alpha)^2}\bigl(f(x^{(0)})-p^\star\bigr)+\log_2\log_2(1/\epsilon).
\tag{9.56}
$$

这个表达式只依赖于直线搜索参数 $\alpha$、$\beta$ 和最终精度 $\epsilon$。而且，涉及 $\epsilon$ 的项可以放心地用常数六替代，因此这个界实际上只依赖于 $\alpha$ 和 $\beta$。对于 $\alpha$、$\beta$ 的典型取值，乘在 $f(x^{(0)})-p^\star$ 前面的常数为几百的量级。例如，取 $\alpha=0.1$、$\beta=0.8$ 时，这个系数为 $375$。容差为 $\epsilon=10^{-10}$ 时，得到界

$$
375\bigl(f(x^{(0)})-p^\star\bigr)+6.
\tag{9.57}
$$

后面将看到，这个界相当保守，但它确实反映了所需牛顿步数在最坏情况下看来具有的一般形式。更精细的分析，例如 Nesterov 和 Nemirovski 最初给出的分析，能得到类似的界，但乘在 $f(x^{(0)})-p^\star$ 前面的常数小得多。

<!-- pdf-page: 520 -->

<figure id="fig-9-25" data-figure="9.25" data-reader-after="self-concordant-experiments-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-25.png" alt="散点图以初始目标值与最优值之差 f(x⁽⁰⁾)−p⋆ 为横轴，以牛顿迭代次数为纵轴；圆圈、方形和菱形分别表示三组不同维数的问题实例。" data-source-page="520" data-source-rect="225,122,440,291">
<figcaption>图 9.25 最小化自协调函数所需的牛顿迭代次数随 $f(x^{(0)})-p^\star$ 的变化。函数 $f$ 的形式为 $f(x)=-\sum_{i=1}^m\log(b_i-a_i^T x)$，其中问题数据 $a_i$ 和 $b$ 随机生成。圆圈表示 $m=100$、$n=50$ 的问题；方形表示 $m=1000$、$n=500$ 的问题；菱形表示 $m=1000$、$n=50$ 的问题。每组均给出了 $50$ 个实例。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>

### 9.6.5 讨论和数值例子

#### 一族自协调函数

将上界 (9.57) 与最小化自协调函数实际所需的迭代次数比较，是很有意思的。考虑一族具有以下形式的问题：

$$
f(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx).
$$

问题数据 $a_i$ 和 $b$ 按如下方式生成。对于每个问题实例，$a_i$ 的系数从均值为零、方差为一的独立正态分布中生成，$b$ 的系数从 $[0,1]$ 上的均匀分布中生成。舍弃没有下界的问题实例。对于每个问题，先计算 $x^\star$。然后，选择一个随机方向 $v$，并取 $x^{(0)}=x^\star+sv$，以此生成起始点；选择 $s$，使 $f(x^{(0)})-p^\star$ 等于 $0$ 到 $35$ 之间的一个指定值。（需要指出，满足 $f(x^{(0)})-p^\star=10$ 或更大值的起始点，实际上已经非常接近多面体的边界。）随后，用采用回溯直线搜索的牛顿法最小化这个函数，参数取 $\alpha=0.1$、$\beta=0.8$，容差取 $\epsilon=10^{-10}$。

<p id="self-concordant-experiments-end" markdown="1">图 9.25 给出了 $150$ 个问题实例中，所需牛顿迭代次数随 $f(x^{(0)})-p^\star$ 的变化。圆圈表示 $m=100$、$n=50$ 的 $50$ 个问题；方块表示 $m=1000$、$n=500$ 的 $50$ 个问题；菱形表示 $m=1000$、$n=50$ 的 $50$ 个问题。</p>

<!-- pdf-page: 521 -->

对于所用的回溯参数值，上面得到的复杂度界为

$$
375\bigl(f(x^{(0)})-p^\star\bigr)+6,
\tag{9.58}
$$

这显然远大于（这 $150$ 个实例）实际所需的迭代次数。图中结果表明，可能存在一个形式相同的有效界，但乘在 $f(x^{(0)})-p^\star$ 前面的常数小得多（例如约为 $1.5$）。事实上，表达式

$$
f(x^{(0)})-p^\star+6
$$

可以较好地粗略预测所需的牛顿步数，虽然它显然不是唯一的影响因素。首先，有许多问题实例所需的牛顿步数要少一些，可以猜测，这些实例对应于“幸运”的起始点。还可以注意到，对于含有 $500$ 个变量的较大问题（由方块表示），牛顿步数异常少的情形似乎更多。

这里还应说明，所研究的这族问题不仅是自协调的，实际上还是*极小自协调的*（minimally self-concordant）；这意味着，当 $\alpha<1$ 时，$\alpha f$ 不再自协调。因此，不能仅通过缩放 $f$ 来改进界 (9.58)。（函数 $f(x)=-20\log x$ 是一个自协调但并非极小自协调的例子，因为 $(1/20)f$ 也是自协调的。）

#### 自协调性在实际中的重要性

已经看到，对于强凸目标函数，牛顿法通常表现很好。这个不够精确的说法既可以由实验支持，也可以用牛顿法的经典分析来说明；经典分析给出了一个复杂度界，但这个界依赖于几个几乎总是未知的常数。

对于自协调函数，可以作出更进一步的论断。我们有一个完全明确、不依赖任何未知常数的复杂度界。实验研究表明，这个界还可以收紧很多，但它的一般形式，即一个小常数加上 $f(x^{(0)})-p^\star$ 的某个倍数，看来至少能够粗略预测：最小化一个近似极小自协调函数需要多少个牛顿步。

自协调函数在实际中是否比非自协调函数更容易用牛顿法最小化，目前还不清楚。（甚至如何精确定义这一说法也不清楚。）目前能说的是，相比非自协调函数，对于自协调函数这一类函数，我们能对牛顿法的复杂度作出更多明确的论断。

<!-- pdf-page: 522 -->

## 9.7 实现

本节讨论实现无约束最小化算法时遇到的一些问题。关于数值线性代数的更多细节，请参阅附录 C。

### 9.7.1 直线搜索中的预计算

在最简单的直线搜索实现中，对于每一个 $t$ 值，都用计算任意 $z\in\mathbf{dom}\,f$ 处的 $f(z)$ 的相同方法，计算 $f(x+t\Delta x)$。但在某些情况下，可以利用这样一个事实：需要在射线 $\{x+t\Delta x\mid t\geq0\}$ 上的许多点计算 $f$（在精确直线搜索中还要计算其导数），从而减少总计算量。这通常需要进行一些预计算，其计算量往往与在任意一点计算 $f$ 同阶；完成这些预计算后，就可以更高效地沿射线计算 $f$（及其导数）。

设 $x\in\mathbf{dom}\,f$，$\Delta x\in\mathbf{R}^n$，定义 $\widetilde f$ 为 $f$ 在由 $x$ 和 $\Delta x$ 确定的直线或射线上的限制，即 $\widetilde f(t)=f(x+t\Delta x)$。在回溯直线搜索中，必须对若干个、可能是很多个 $t$ 值计算 $\widetilde f$；在精确直线搜索方法中，必须对若干个 $t$ 值计算 $\widetilde f$ 以及它的一阶或更多阶导数。在上述简单方法中，为计算 $\widetilde f(t)$，先形成 $z=x+t\Delta x$，然后计算 $f(z)$。为计算 $\widetilde f'(t)$，先形成 $z=x+t\Delta x$，然后计算 $\nabla f(z)$，再计算 $\widetilde f'(t)=\nabla f(z)^T\Delta x$。下面通过几个有代表性的例子，说明如何更高效地在多个 $t$ 值处计算 $\widetilde f$。

#### 与仿射函数复合

预计算能够加快直线搜索过程的一种非常普遍的情形，是目标函数具有形式 $f(x)=\phi(Ax+b)$，其中 $A\in\mathbf{R}^{p\times n}$，而 $\phi$ 易于计算（例如，它是可分的）。若用简单方法对 $k$ 个 $t$ 值计算 $\widetilde f(t)=f(x+t\Delta x)$，则要为每个 $t$ 值形成 $A(x+t\Delta x)+b$（共需 $2kpn$ 次浮点运算，flops），再为每个 $t$ 值计算 $\phi(A(x+t\Delta x)+b)$。更高效的做法是先计算 $Ax+b$ 和 $A\Delta x$（$4pn$ 次浮点运算），然后利用

$$
A(x+t\Delta x)+b=(Ax+b)+t(A\Delta x)
$$

为每个 $t$ 值形成 $A(x+t\Delta x)+b$，这需要 $2kp$ 次浮点运算。仅保留主导项，总开销为 $4pn+2kp$ 次浮点运算，而简单方法需要 $2kpn$ 次。

#### 线性矩阵不等式的解析中心

下面给出一个更具体、也更完整的例子。考虑计算线性矩阵不等式解析中心的问题 (9.6)，即最小化 $\log\det F(x)^{-1}$，其中 $x\in\mathbf{R}^n$，$F:\mathbf{R}^n\to\mathbf{S}^p$ 是仿射函数。沿经过 $x$、方向为 $\Delta x$ 的直线，有

$$
\widetilde f(t)=\log\det(F(x+t\Delta x))^{-1}=-\log\det(A+tB),
$$

<!-- pdf-page: 523 -->

其中

$$
A=F(x),\qquad B=\Delta x_1F_1+\cdots+\Delta x_nF_n\in\mathbf{S}^p.
$$

由于 $A\succ0$，它有 Cholesky 分解 $A=LL^T$，其中 $L$ 是非奇异的下三角矩阵。因此，可以将 $\widetilde f$ 写成

$$
\widetilde f(t)=-\log\det\bigl(L(I+tL^{-1}BL^{-T})L^T\bigr)
=-\log\det A-\sum_{i=1}^p\log(1+t\lambda_i),
\tag{9.59}
$$

其中 $\lambda_1,\ldots,\lambda_p$ 是 $L^{-1}BL^{-T}$ 的特征值。一旦算出这些特征值，对于任意 $t$，利用 (9.59) 右端的公式，只需 $4p$ 次简单算术运算，就能计算 $\widetilde f(t)$。利用公式

$$
\widetilde f'(t)=-\sum_{i=1}^p\frac{\lambda_i}{1+t\lambda_i},
$$

也可以用 $4p$ 次运算计算 $\widetilde f'(t)$（同样也能计算任意更高阶的导数）。

下面比较这两种进行直线搜索的方法，假设需要对 $k$ 个 $t$ 值计算 $f(x+t\Delta x)$。在简单方法中，对于每个 $t$ 值，先形成 $F(x+t\Delta x)$，再通过 $-\log\det F(x+t\Delta x)$ 计算 $f(x+t\Delta x)$。例如，可以求出 Cholesky 分解 $F(x+t\Delta x)=LL^T$，然后计算

$$
-\log\det F(x+t\Delta x)=-2\sum_{i=1}^p\log L_{ii}.
$$

形成 $F(x+t\Delta x)$ 的开销为 $np^2$，Cholesky 分解还需 $(1/3)p^3$。因此，直线搜索的总开销为

$$
k\bigl(np^2+(1/3)p^3\bigr)=knp^2+(1/3)kp^3.
$$

采用上面的方法，先形成 $A$，开销为 $np^2$，再对它分解，开销为 $(1/3)p^3$。还要形成 $B$（开销为 $np^2$），以及 $L^{-1}BL^{-T}$（开销为 $2p^3$）。随后计算这个矩阵的特征值，开销约为 $(4/3)p^3$ 次浮点运算。这些预计算总共需要 $2np^2+(11/3)p^3$ 次浮点运算。预计算完成后，对每个 $t$ 值，只需 $4p$ 次浮点运算就能计算 $\widetilde f(t)$。因此，总开销为

$$
2np^2+(11/3)p^3+4kp.
$$

假设 $k$ 远小于 $p(2n+(11/3)p)$，这意味着整个直线搜索的计算量与单次计算 $f$ 相当。根据 $k$、$p$ 和 $n$ 的取值，相对简单方法所节省的倍数可达 $k$ 的量级。

### 9.7.2 计算牛顿步

本节简要介绍实现牛顿法时遇到的一些问题。在大多数情况下，计算牛顿步 $\Delta x_{\mathrm{nt}}$ 的工作量<!-- pdf-page: 524 -->占主导，超过直线搜索的工作量。为计算牛顿步 $\Delta x_{\mathrm{nt}}$，先计算并形成 $x$ 处的 Hessian 矩阵 $H=\nabla^2f(x)$ 和梯度 $g=\nabla f(x)$。然后求解线性方程组 $H\Delta x_{\mathrm{nt}}=-g$，得到牛顿步。这组方程有时称为*牛顿方程组*（Newton system），因为它的解给出牛顿步；也称为*正规方程*，因为在求解最小二乘问题时也会出现同类方程（见 §9.1.1）。

虽然可以使用通用的线性方程求解器，但利用 $H$ 的对称性和正定性的方法更好。最常见的做法是对 $H$ 作 Cholesky 分解，即计算满足 $LL^T=H$ 的下三角矩阵 $L$（见 §C.3.2）。然后用前代（forward substitution）求解 $Lw=-g$，得到 $w=-L^{-1}g$，再用回代（back substitution）求解 $L^T\Delta x_{\mathrm{nt}}=w$，得到

$$
\Delta x_{\mathrm{nt}}=L^{-T}w=-L^{-T}L^{-1}g=-H^{-1}g.
$$

可以通过 $\lambda^2=-\Delta x_{\mathrm{nt}}^Tg$ 计算牛顿减量，也可以使用公式

$$
\lambda^2=g^TH^{-1}g=\|L^{-1}g\|_2^2=\|w\|_2^2.
$$

如果采用稠密（无结构）的 Cholesky 分解，前代和回代的开销小于占主导的 Cholesky 分解开销，后者为 $(1/3)n^3$ 次浮点运算。因此，计算牛顿步 $\Delta x_{\mathrm{nt}}$ 的总开销为 $F+(1/3)n^3$ 次浮点运算，其中 $F$ 是形成 $H$ 和 $g$ 的开销。

利用 $H$ 的特殊结构，例如带状结构或稀疏性，通常可以更高效地求解牛顿方程组 $H\Delta x_{\mathrm{nt}}=-g$。这里，“$H$ 的结构”指的是对所有 $x$ 都相同的结构。例如，说“$H$ 是三对角的”，意味着对每个 $x\in\mathbf{dom}\,f$，$\nabla^2f(x)$ 都是三对角矩阵。

#### 带状结构

如果 Hessian 矩阵 $H$ 是带状矩阵，带宽为 $k$，即当 $|i-j|>k$ 时 $H_{ij}=0$，那么可以使用带状 Cholesky 分解，以及带状的前代和回代。此时，计算牛顿步 $\Delta x_{\mathrm{nt}}=-H^{-1}g$ 的开销为 $F+nk^2$ 次浮点运算（假设 $k\ll n$）；相比之下，稠密分解及代入方法需要 $F+(1/3)n^3$ 次浮点运算。

Hessian 矩阵的带状结构条件

$$
\nabla^2f(x)_{ij}=\frac{\partial^2f(x)}{\partial x_i\partial x_j}=0
\qquad\text{当 }|i-j|>k,
$$

对所有 $x\in\mathbf{dom}\,f$ 成立；从目标函数 $f$ 的角度看，它有一个有意思的解释。粗略地说，这意味着在目标函数中，每个变量 $x_i$ 只与 $2k+1$ 个变量 $x_j$（$j=i-k,\ldots,i+k$）存在非线性耦合。当 $f$ 具有以下部分可分的形式时，就会出现这种结构：

$$
f(x)=\psi_1(x_1,\ldots,x_{k+1})+\psi_2(x_2,\ldots,x_{k+2})
+\cdots+\psi_{n-k}(x_{n-k},\ldots,x_n),
$$

其中 $\psi_i:\mathbf{R}^{k+1}\to\mathbf{R}$。换言之，$f$ 可以表示为若干函数之和，每个函数依赖于 $k$ 个连续变量。

<div class="translator-note" markdown="1">

**译注：连续变量的个数。** 按上式，各 $\psi_i$ 依赖 $k+1$ 个连续变量；这与 Hessian 矩阵带宽 $k$ 的定义一致。

</div>

<!-- pdf-page: 525 -->

<div class="example" id="example-9-9" markdown="1">

**例 9.9** 考虑最小化 $f:\mathbf{R}^n\to\mathbf{R}$ 的问题，其中 $f$ 具有形式

$$
f(x)=\psi_1(x_1,x_2)+\psi_2(x_2,x_3)+\cdots+\psi_{n-1}(x_{n-1},x_n),
$$

$\psi_i:\mathbf{R}^2\to\mathbf{R}$ 都是凸函数且二阶可微。由于这种形式，Hessian 矩阵 $\nabla^2f$ 是三对角的，因为当 $|i-j|>1$ 时，$\partial^2f/\partial x_i\partial x_j=0$。（反过来，如果一个函数的 Hessian 矩阵对所有 $x$ 都是三对角的，那么这个函数就具有上述形式。）

利用针对三对角矩阵的 Cholesky 分解以及前代、回代算法，可以用 $n$ 量级的浮点运算求解这个问题的牛顿方程组。如果不利用 $f$ 的特殊形式，则需要 $n^3$ 量级的浮点运算。

</div>

#### 稀疏结构

更一般地，可以在求解牛顿方程组时利用 Hessian 矩阵 $H$ 的稀疏性。只要每个变量 $x_i$（在目标函数中）仅与少数其他变量存在非线性耦合，就会出现这种稀疏结构；等价地，目标函数可以表示为若干函数之和，每个函数只依赖少数几个变量，而且每个变量只出现在其中少数几个函数中。

当 $H$ 稀疏时，为求解 $H\Delta x=-g$，使用稀疏 Cholesky 分解，计算一个置换矩阵 $P$ 和一个下三角矩阵 $L$，使

$$
H=PLL^TP^T.
$$

分解的开销取决于具体的稀疏模式，但通常远小于 $(1/3)n^3$；（对于较大的 $n$）实际观测到 $n$ 量级的复杂度也很常见。前代和回代与不进行置换的基本方法十分相似。先用前代求解 $Lw=-P^Tg$，再用回代求解 $L^Tv=w$，得到

$$
v=L^{-T}w=-L^{-T}L^{-1}P^Tg.
$$

于是牛顿步为 $\Delta x=Pv$。

由于 $H$ 的稀疏模式不随 $x$ 改变（更准确地说，我们只利用不随 $x$ 改变的稀疏性），每个牛顿步都可以使用同一个置换矩阵 $P$。确定一个好的置换矩阵 $P$ 的步骤称为*符号分解*（symbolic factorization）步骤，在整个牛顿迭代过程中只需进行一次。

#### 对角加低秩结构

在求解牛顿方程组 $H\Delta x_{\mathrm{nt}}=-g$ 时，还有许多其他类型的结构可以利用。这里简要介绍一种，更多细节请参阅附录 C。假设 Hessian 矩阵 $H$ 可以表示为一个对角矩阵与一个低秩矩阵之和，后者的秩记为 $p$。当目标函数 $f$ 具有以下特殊形式时，就会出现这种结构：

$$
f(x)=\sum_{i=1}^n\psi_i(x_i)+\psi_0(Ax+b),
\tag{9.60}
$$

<!-- pdf-page: 526 -->

其中 $A\in\mathbf{R}^{p\times n}$，$\psi_1,\ldots,\psi_n:\mathbf{R}\to\mathbf{R}$，$\psi_0:\mathbf{R}^p\to\mathbf{R}$。换言之，$f$ 是一个可分函数，加上一个依赖于 $x$ 的低维仿射函数的函数。

为求出 (9.60) 的牛顿步 $\Delta x_{\mathrm{nt}}$，必须求解牛顿方程组 $H\Delta x_{\mathrm{nt}}=-g$，其中

$$
H=D+A^TH_0A.
$$

这里 $D=\mathbf{diag}(\psi_1''(x_1),\ldots,\psi_n''(x_n))$ 是对角矩阵，$H_0=\nabla^2\psi_0(Ax+b)$ 是 $\psi_0$ 的 Hessian 矩阵。如果计算牛顿步时不利用这种结构，求解牛顿方程组的开销为 $(1/3)n^3$ 次浮点运算。

设 $H_0=L_0L_0^T$ 是 $H_0$ 的 Cholesky 分解。引入临时变量 $w=L_0^TA\Delta x_{\mathrm{nt}}\in\mathbf{R}^p$，将牛顿方程组写成

$$
D\Delta x_{\mathrm{nt}}+A^TL_0w=-g,\qquad w=L_0^TA\Delta x_{\mathrm{nt}}.
$$

将（由第一个方程得到的）$\Delta x_{\mathrm{nt}}=-D^{-1}(A^TL_0w+g)$ 代入第二个方程，得到

$$
(I+L_0^TAD^{-1}A^TL_0)w=-L_0^TAD^{-1}g,
\tag{9.61}
$$

这是一个包含 $p$ 个线性方程的方程组。

现在按如下步骤计算牛顿步 $\Delta x_{\mathrm{nt}}$。首先计算 $H_0$ 的 Cholesky 分解，开销为 $(1/3)p^3$。然后形成 (9.61) 左端的稠密对称正定矩阵，开销为 $2p^2n$。再用 Cholesky 分解以及回代和前代求解 (9.61)，得到 $w$，开销为 $(1/3)p^3$ 次浮点运算。最后，利用 $\Delta x_{\mathrm{nt}}=-D^{-1}(A^TL_0w+g)$ 计算 $\Delta x_{\mathrm{nt}}$，开销为 $2np$ 次浮点运算。因此，计算 $\Delta x_{\mathrm{nt}}$ 的总开销（只保留主导项）为 $2p^2n$ 次浮点运算；当 $p\ll n$ 时，它远小于 $(1/3)n^3$。

<!-- pdf-page: 527 -->

## 文献说明

Dennis 和 Schnabel [DS96] 以及 Ortega 和 Rheinboldt [OR00] 是关于无约束最小化与非线性方程算法的两部标准参考著作。在强凸性和 Hessian 矩阵 Lipschitz 连续的假设下，关于二次收敛的结论归功于 Kantorovich [Kan52]。Polyak [Pol87, §1.6] 对涉及未知常数的收敛结论所起的作用，给出了一些富有启发的评论；§9.5.3 推导的结果就是这类结论的例子。

自协调函数由 Nesterov 和 Nemirovski [NN94] 引入。§9.6 以及习题 9.14–9.20 中的所有结果，都可以在他们的书中找到，不过往往以更一般的形式或不同的记号表述。Renegar [Ren01] 简洁而优美地介绍了自协调函数，以及它们在原始–对偶内点算法分析中的作用。Peng、Roos 和 Terlaky [PRT02] 从*自正则函数*（self-regular functions）的角度研究内点法；这是一类与自协调函数相似但并不相同的函数。

§9.7 内容的参考文献列在附录 C 的末尾。

<!-- pdf-page: 528 -->

## 习题

### 无约束最小化

**9.1 二次函数最小化。** 考虑最小化二次函数的问题：

$$
\begin{array}{ll}
\text{最小化} & f(x)=(1/2)x^TPx+q^Tx+r,
\end{array}
$$

其中 $P\in\mathbf{S}^n$（但不假设 $P\succeq0$）。

- (a) 证明，如果 $P\not\succeq0$，即目标函数 $f$ 不是凸函数，那么该问题无下界。

- (b) 现在假设 $P\succeq0$（因此目标函数是凸函数），但最优性条件 $Px^\star=-q$ 无解。证明该问题无下界。

**9.2 二次除以线性的分式函数最小化。** 考虑最小化函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的问题，其中

$$
f(x)=\frac{\|Ax-b\|_2^2}{c^Tx+d},\qquad
\mathbf{dom}\,f=\{x\mid c^Tx+d>0\}.
$$

假设 $\mathbf{rank}\,A=n$，且 $b\notin\mathcal{R}(A)$。

- (a) 证明 $f$ 是闭函数。

- (b) 证明 $f$ 的最小化点 $x^\star$ 为

    $$
    x^\star=x_1+tx_2,
    $$

    其中 $x_1=(A^TA)^{-1}A^Tb$、$x_2=(A^TA)^{-1}c$，而 $t\in\mathbf{R}$ 可以通过求解一个二次方程得到。

**9.3 初始点与下水平集条件。** 考虑函数 $f(x)=x_1^2+x_2^2$，定义域为 $\mathbf{dom}\,f=\{(x_1,x_2)\mid x_1>1\}$。

- (a) $p^\star$ 是多少？

- (b) 对 $x^{(0)}=(2,2)$，画出下水平集 $S=\{x\mid f(x)\leq f(x^{(0)})\}$。下水平集 $S$ 是闭集吗？$f$ 在 $S$ 上强凸吗？

- (c) 从 $x^{(0)}$ 出发，应用采用回溯直线搜索的梯度法，会发生什么？$f(x^{(k)})$ 会收敛到 $p^\star$ 吗？

**9.4** 你同意下面的论证吗？向量 $x\in\mathbf{R}^m$ 的 $\ell_1$ 范数可以表示为

$$
\|x\|_1=(1/2)\inf_{y\succ0}\left(\sum_{i=1}^m x_i^2/y_i+\mathbf{1}^Ty\right).
$$

因此，$\ell_1$ 范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_1
\end{array}
$$

等价于最小化问题

$$
\begin{array}{ll}
\text{最小化} & f(x,y)=\displaystyle\sum_{i=1}^m(a_i^Tx-b_i)^2/y_i+\mathbf{1}^Ty,
\end{array}
\tag{9.62}
$$

其定义域为 $\mathbf{dom}\,f=\{(x,y)\in\mathbf{R}^n\times\mathbf{R}^m\mid y\succ0\}$，其中 $a_i^T$ 是 $A$ 的第 $i$ 行。由于 $f$ 二阶可微且凸，可以将牛顿法应用于 (9.62)，从而求解这个 $\ell_1$ 范数逼近问题。

**9.5 回溯直线搜索。** 假设 $f$ 强凸，且 $mI\preceq\nabla^2f(x)\preceq MI$。设 $\Delta x$ 是 $x$ 处的一个下降方向。证明，当

$$
0<t\leq-\frac{\nabla f(x)^T\Delta x}{M\|\Delta x\|_2^2}
$$

时，回溯的停止条件成立。利用这个结论，给出回溯迭代次数的上界。

<!-- pdf-page: 529 -->

### 梯度法与最速下降法

**9.6 $\mathbf{R}^2$ 中的二次问题。** 验证 §9.3.2 第一个例子中迭代点 $x^{(k)}$ 的表达式。

**9.7** 设 $\Delta x_{\mathrm{nsd}}$ 和 $\Delta x_{\mathrm{sd}}$ 分别是范数 $\|\cdot\|$ 下，在 $x$ 处归一化和未归一化的最速下降方向。证明下列恒等式。

- (a) $\nabla f(x)^T\Delta x_{\mathrm{nsd}}=-\|\nabla f(x)\|_*$。

- (b) $\nabla f(x)^T\Delta x_{\mathrm{sd}}=-\|\nabla f(x)\|_*^2$。

- (c) $\Delta x_{\mathrm{sd}}=\operatorname*{argmin}_v\bigl(\nabla f(x)^Tv+(1/2)\|v\|^2\bigr)$。

**9.8 $\ell_\infty$ 范数下的最速下降法。** 说明如何求出 $\ell_\infty$ 范数下的一个最速下降方向，并给出一个简单的解释。

### 牛顿法

**9.9 牛顿减量。** 证明牛顿减量 $\lambda(x)$ 满足

$$
\lambda(x)=\sup_{v^T\nabla^2f(x)v=1}\bigl(-v^T\nabla f(x)\bigr)
=\sup_{v\neq0}\frac{-v^T\nabla f(x)}{(v^T\nabla^2f(x)v)^{1/2}}.
$$

**9.10 纯牛顿法。** 如果初始点不接近 $x^\star$，固定步长为 $t=1$ 的牛顿法可能发散。本题考虑两个例子。

- (a) $f(x)=\log(e^x+e^{-x})$ 有唯一的最小化点 $x^\star=0$。分别从 $x^{(0)}=1$ 和 $x^{(0)}=1.1$ 出发，运行固定步长为 $t=1$ 的牛顿法。

- (b) $f(x)=-\log x+x$ 有唯一的最小化点 $x^\star=1$。从 $x^{(0)}=3$ 出发，运行固定步长为 $t=1$ 的牛顿法。

绘出 $f$ 和 $f'$，并标出最初几个迭代点。

**9.11 复合函数的梯度法与牛顿法。** 假设 $\phi:\mathbf{R}\to\mathbf{R}$ 递增且凸，$f:\mathbf{R}^n\to\mathbf{R}$ 为凸函数，因此 $g(x)=\phi(f(x))$ 是凸函数。（假设 $f$ 和 $g$ 二阶可微。）最小化 $f$ 与最小化 $g$ 这两个问题显然等价。

比较分别用于 $f$ 和 $g$ 的梯度法与牛顿法。搜索方向有何关系？如果采用精确直线搜索，这些方法有何关系？

*提示。* 使用矩阵求逆引理（见 §C.4.3）。

**9.12 信赖域牛顿法。** 如果 $\nabla^2f(x)$ 奇异（或条件数极大），用 $\Delta x_{\mathrm{nt}}=-\nabla^2f(x)^{-1}\nabla f(x)$ 定义牛顿步就会有问题。此时，可以将搜索方向 $\Delta x_{\mathrm{tr}}$ 定义为以下问题的解：

$$
\begin{array}{ll}
\text{最小化} & (1/2)v^THv+g^Tv\\
\text{约束条件} & \|v\|_2\leq\gamma,
\end{array}
$$

其中 $H=\nabla^2f(x)$，$g=\nabla f(x)$，$\gamma$ 为正常数。点 $x+\Delta x_{\mathrm{tr}}$ 在约束 $\|(x+\Delta x_{\mathrm{tr}})-x\|_2\leq\gamma$ 下，使 $f$ 在 $x$ 处的二阶近似最小。集合 $\{v\mid\|v\|_2\leq\gamma\}$ 称为*信赖域*（trust region）。参数 $\gamma$ 表示信赖域的大小，反映了我们对二阶模型的信任程度。

证明，对某个 $\hat\beta$，$\Delta x_{\mathrm{tr}}$ 最小化

$$
(1/2)v^THv+g^Tv+\hat\beta\|v\|_2^2.
$$

这个二次函数可以解释为 $f$ 在 $x$ 附近的一个正则化二次模型。

<!-- pdf-page: 530 -->

### 自协调性

**9.13 自协调性与倒数障碍函数（inverse barrier）。**

- (a) 证明，定义域为 $(0,8/9)$ 的函数 $f(x)=1/x$ 是自协调的。

- (b) 证明，函数

    $$
    f(x)=\alpha\sum_{i=1}^m\frac{1}{b_i-a_i^Tx},
    $$

    定义域为 $\mathbf{dom}\,f=\{x\in\mathbf{R}^n\mid a_i^Tx<b_i,\ i=1,\ldots,m\}$；如果 $\mathbf{dom}\,f$ 有界，且

    $$
    \alpha>(9/8)\max_{i=1,\ldots,m}\sup_{x\in\mathbf{dom}\,f}(b_i-a_i^Tx),
    $$

    那么该函数是自协调的。

**9.14 与对数函数复合。** 设 $g:\mathbf{R}\to\mathbf{R}$ 是凸函数，$\mathbf{dom}\,g=\mathbf{R}_{++}$，并且对所有 $x$，

$$
|g'''(x)|\leq3\frac{g''(x)}{x}.
$$

证明，$f(x)=-\log(-g(x))-\log x$ 在 $\{x\mid x>0,\ g(x)<0\}$ 上自协调。*提示。* 利用不等式

$$
\frac32rp^2+q^3+\frac32p^2q+r^3\leq1,
$$

它对满足 $p^2+q^2+r^2=1$ 的 $p,q,r\in\mathbf{R}_+$ 成立。

**9.15** 证明下列函数是自协调函数。证明时，将函数限制在一条直线上，并应用与对数函数复合的规则。

- (a) $f(x,y)=-\log(y^2-x^Tx)$，定义在 $\{(x,y)\mid\|x\|_2<y\}$ 上。

- (b) $f(x,y)=-2\log y-\log(y^{2/p}-x^2)$，其中 $p\geq1$，定义在 $\{(x,y)\in\mathbf{R}^2\mid|x|^p<y\}$ 上。

- (c) $f(x,y)=-\log y-\log(\log y-x)$，定义在 $\{(x,y)\mid e^x<y\}$ 上。

**9.16** 设 $f:\mathbf{R}\to\mathbf{R}$ 是自协调函数。

- (a) 假设 $f''(x)\ne0$。证明，自协调性条件 (9.41) 可以表示为

    $$
    \left|\frac{d}{dx}\left(f''(x)^{-1/2}\right)\right|\leq1.
    $$

    求出“极端”的一元自协调函数，即分别满足

    $$
    \frac{d}{dx}\left(f''(x)^{-1/2}\right)=1,\qquad
    \frac{d}{dx}\left(\widetilde f''(x)^{-1/2}\right)=-1
    $$

    的函数 $f$ 和 $\widetilde f$。

- (b) 证明，以下两种情况必有一种成立：对所有 $x\in\mathbf{dom}\,f$ 都有 $f''(x)=0$；或者，对所有 $x\in\mathbf{dom}\,f$ 都有 $f''(x)>0$。

**9.17 自协调函数 Hessian 矩阵的上下界。**

- (a) 设 $f:\mathbf{R}^2\to\mathbf{R}$ 是自协调函数。证明，对所有 $x\in\mathbf{dom}\,f$，都有

    $$
    \begin{aligned}
    \left|\frac{\partial^3 f(x)}{\partial^3 x_i}\right|
    &\leq2\left(\frac{\partial^2 f(x)}{\partial x_i^2}\right)^{3/2},
    &&i=1,2,\\
    \left|\frac{\partial^3 f(x)}{\partial x_i^2\partial x_j}\right|
    &\leq2\frac{\partial^2 f(x)}{\partial x_i^2}
    \left(\frac{\partial^2 f(x)}{\partial x_j^2}\right)^{1/2},
    &&i\ne j.
    \end{aligned}
    $$

    <!-- pdf-page: 531 -->

    **提示。** 如果 $h:\mathbf{R}^2\times\mathbf{R}^2\times\mathbf{R}^2\to\mathbf{R}$ 是对称三线性形式，即

    $$
    \begin{aligned}
    h(u,v,w)={}&a_1u_1v_1w_1+a_2(u_1v_1w_2+u_1v_2w_1+u_2v_1w_1)\\
    &+a_3(u_1v_2w_2+u_2v_1w_1+u_2v_2w_1)+a_4u_2v_2w_2,
    \end{aligned}
    $$

    则

    $$
    \sup_{u,v,w\ne0}\frac{h(u,v,w)}{\|u\|_2\|v\|_2\|w\|_2}
    =\sup_{u\ne0}\frac{h(u,u,u)}{\|u\|_2^3}.
    $$

- (b) 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是自协调函数。证明，$\nabla^2f(x)$ 的零空间与 $x$ 无关。证明，如果 $f$ 严格凸，则对所有 $x\in\mathbf{dom}\,f$，$\nabla^2f(x)$ 都非奇异。

    **提示。** 证明：如果对某个 $x\in\mathbf{dom}\,f$ 有 $w^T\nabla^2f(x)w=0$，那么对所有 $y\in\mathbf{dom}\,f$ 都有 $w^T\nabla^2f(y)w=0$。为此，将 (a) 中的结果应用于自协调函数 $\widetilde f(t,s)=f(x+t(y-x)+sw)$。

- (c) 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是自协调函数。假设 $x\in\mathbf{dom}\,f$、$v\in\mathbf{R}^n$。证明，当 $x+tv\in\mathbf{dom}\,f$、$0\leq t<\alpha$ 时，有

    $$
    (1-t\alpha)^2\nabla^2f(x)\preceq\nabla^2f(x+tv)
    \preceq\frac{1}{(1-t\alpha)^2}\nabla^2f(x),
    $$

    其中 $\alpha=(v^T\nabla^2f(x)v)^{1/2}$。

<div class="translator-note" markdown="1">

**译注：习题 9.17 的两处原式。** (a) 的提示把 $h$ 称为对称三线性形式，但 $a_3$ 括号中的第二项印作 $u_2v_1w_1$；与该对称性相符的项应为 $u_2v_1w_2$。

(c) 中仍需保留 $x+tv\in\mathbf{dom}\,f$ 的条件；步长范围应为 $0\leq t$ 且 $t\alpha<1$。当 $\alpha>0$ 时，这等价于 $0\leq t<1/\alpha$。原印 $0\leq t<\alpha$ 可能令分母 $1-t\alpha$ 等于零，也不能保证所给的 Hessian 下界。

</div>

**9.18 二次收敛。** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是严格凸的自协调函数。假设 $\lambda(x)<1$，并定义 $x^+=x-\nabla^2f(x)^{-1}\nabla f(x)$。证明 $\lambda(x^+)\leq\lambda(x)^2/(1-\lambda(x))^2$。**提示。** 使用习题 9.17(c) 中的不等式。

**9.19 到最优点的距离界。** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是严格凸的自协调函数。

- (a) 假设 $\lambda(\bar x)<1$，且下水平集 $\{x\mid f(x)\leq f(\bar x)\}$ 是闭集。证明，$f$ 的最小值可以达到，并且

    $$
    \left((\bar x-x^\star)^T\nabla^2f(\bar x)(\bar x-x^\star)\right)^{1/2}
    \leq\frac{\lambda(\bar x)}{1-\lambda(\bar x)}.
    $$

- (b) 证明：如果 $f$ 有一个闭的下水平集，并且有下界，那么它的最小值可以达到。

**9.20 自协调函数的共轭。** 假设 $f:\mathbf{R}^n\to\mathbf{R}$ 是闭的、严格凸的自协调函数。本题将证明，它的共轭（或 Legendre 变换）$f^*$ 也是自协调函数。

- (a) 证明：对每个 $y\in\mathbf{dom}\,f^*$，都存在唯一的 $x\in\mathbf{dom}\,f$ 满足 $y=\nabla f(x)$。**提示。** 参见习题 9.19 的结果。

- (b) 假设 $\bar y=\nabla f(\bar x)$。定义

    $$
    g(t)=f(\bar x+tv),\qquad h(t)=f^*(\bar y+tw),
    $$

    其中 $v\in\mathbf{R}^n$，$w=\nabla^2f(\bar x)v$。证明

    $$
    g''(0)=h''(0),\qquad g'''(0)=-h'''(0).
    $$

    利用这些恒等式，证明 $f^*$ 是自协调函数。

**9.21 最优直线搜索参数。** 考虑对严格凸的自协调函数进行最小化所需牛顿迭代次数的上界 (9.56)。如果对 $\alpha$ 和 $\beta$ 最小化，这个上界的最小值是多少？

**9.22** 假设 $f$ 严格凸且满足 (9.42)。给出从 $x^{(0)}$ 出发、以 $\epsilon$ 精度求得 $p^\star$ 所需牛顿步数的一个上界。

<!-- pdf-page: 532 -->

### 实现

**9.23 直线搜索中的预计算。** 对以下每个函数，说明如何通过预计算来降低直线搜索的计算代价。给出预计算的代价，以及进行和不进行预计算时，计算 $g(t)=f(x+t\Delta x)$ 与 $g'(t)$ 的代价。

- (a) $f(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx)$。

- (b) $f(x)=\log\left(\sum_{i=1}^m\exp(a_i^Tx+b_i)\right)$。

- (c) $f(x)=(Ax-b)^T(P_0+x_1P_1+\cdots+x_nP_n)^{-1}(Ax-b)$，其中 $P_i\in\mathbf{S}^m$、$A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，且 $\mathbf{dom}\,f=\{x\mid P_0+\sum_{i=1}^n x_iP_i\succ0\}$。

**9.24 利用牛顿方程组的分块对角结构。** 假设凸函数 $f$ 的 Hessian 矩阵 $\nabla^2f(x)$ 是分块对角矩阵。计算牛顿步时，如何利用这一结构？这一结构意味着 $f$ 具有什么性质？

**9.25 给定数据的平滑拟合。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=\displaystyle\sum_{i=1}^n\psi(x_i-y_i)
+\lambda\displaystyle\sum_{i=1}^{n-1}(x_{i+1}-x_i)^2
\end{array}
$$

其中 $\lambda>0$ 是平滑参数，$\psi$ 是凸罚函数，$x\in\mathbf{R}^n$ 是变量。可以将 $x$ 理解为对向量 $y$ 的平滑拟合。

- (a) $f$ 的 Hessian 矩阵具有怎样的结构？

- (b) 将上述问题扩展到二维数据的平滑拟合，即最小化函数

    $$
    \begin{aligned}
    &\sum_{i,j=1}^n\psi(x_{ij}-y_{ij})\\
    &\quad+\lambda\left(
    \sum_{i=1}^{n-1}\sum_{j=1}^n(x_{i+1,j}-x_{ij})^2
    +\sum_{i=1}^n\sum_{j=1}^{n-1}(x_{i,j+1}-x_{ij})^2
    \right),
    \end{aligned}
    $$

    变量为 $X\in\mathbf{R}^{n\times n}$，其中 $Y\in\mathbf{R}^{n\times n}$ 和 $\lambda>0$ 已给定。

**9.26 具有线性结构的牛顿方程组。** 考虑最小化具有如下形式的函数：

$$
f(x)=\sum_{i=1}^N\psi_i(A_ix+b_i),
\tag{9.63}
$$

其中 $A_i\in\mathbf{R}^{m_i\times n}$、$b_i\in\mathbf{R}^{m_i}$，函数 $\psi_i:\mathbf{R}^{m_i}\to\mathbf{R}$ 二阶可微且凸。$f$ 在 $x$ 处的 Hessian 矩阵 $H$ 和梯度 $g$ 为

$$
H=\sum_{i=1}^NA_i^TH_iA_i,\qquad
g=\sum_{i=1}^NA_i^Tg_i.
\tag{9.64}
$$

其中 $H_i=\nabla^2\psi_i(A_ix+b_i)$，$g_i=\nabla\psi_i(A_ix+b_i)$。

说明如何实现用于最小化 $f$ 的牛顿法。假设 $n\gg m_i$，矩阵 $A_i$ 非常稀疏，但 Hessian 矩阵 $H$ 是稠密的。

**9.27 带变量界限的线性不等式的解析中心。** 给出计算下列函数的牛顿步的最高效方法：

$$
f(x)=-\sum_{i=1}^n\log(x_i+1)-\sum_{i=1}^n\log(1-x_i)-\sum_{i=1}^m\log(b_i-a_i^Tx),
$$

其定义域为 $\mathbf{dom}\,f=\{x\in\mathbf{R}^n\mid-\mathbf{1}\prec x\prec\mathbf{1},\ Ax\prec b\}$，其中 $a_i^T$ 是 $A$ 的第 $i$ 行。假设 $A$ 稠密，并区分 $m\geq n$ 和 $m\leq n$ 两种情形。（另见习题 9.30。）

<!-- pdf-page: 533 -->

**9.28 二次不等式的解析中心。** 说明一种高效计算下列函数的牛顿步的方法：

$$
f(x)=-\sum_{i=1}^m\log(-x^TA_ix-b_i^Tx-c_i),
$$

其定义域为 $\mathbf{dom}\,f=\{x\mid x^TA_ix+b_i^Tx+c_i<0,\ i=1,\ldots,m\}$。假设矩阵 $A_i\in\mathbf{S}_{++}^n$ 规模很大且稀疏，并且 $m\ll n$。

*提示。* $f$ 在 $x$ 处的 Hessian 矩阵和梯度为

$$
H=\sum_{i=1}^m\left(2\alpha_iA_i+\alpha_i^2(2A_ix+b_i)(2A_ix+b_i)^T\right),\qquad
g=\sum_{i=1}^m\alpha_i(2A_ix+b_i),
$$

其中 $\alpha_i=1/(-x^TA_ix-b_i^Tx-c_i)$。

**9.29 利用两阶段优化的结构。** 本题延续习题 4.64；该题介绍了带补救决策的优化，也称两阶段优化。沿用习题 4.64 的记号和假设，并进一步假设：对于每个情景 $i=1,\ldots,S$，代价函数 $f$ 都是关于 $(x,z)$ 的二阶可微函数。

说明如何高效计算求最优策略这一问题的牛顿步。以情景数 $S$ 为自变量，比较你的方法与通用方法（不利用任何结构）的近似浮点运算次数。

### 数值实验

**9.30 梯度法与牛顿法。** 考虑无约束问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=-\displaystyle\sum_{i=1}^m\log(1-a_i^Tx)-\displaystyle\sum_{i=1}^n\log(1-x_i^2),
\end{array}
$$

变量为 $x\in\mathbf{R}^n$，定义域为 $\mathbf{dom}\,f=\{x\mid a_i^Tx<1,\ i=1,\ldots,m,\ |x_i|<1,\ i=1,\ldots,n\}$。这是计算下列一组线性不等式所定义集合的解析中心的问题：

$$
a_i^Tx\leq1,\quad i=1,\ldots,m,\qquad
|x_i|\leq1,\quad i=1,\ldots,n.
$$

注意，可以选择 $x^{(0)}=0$ 作为初始点。可以从 $\mathbf{R}^n$ 上的某个分布中抽取 $a_i$，以生成这个问题的实例。

- (a) 用梯度法求解这个问题，合理选择回溯参数，并采用 $\|\nabla f(x)\|_2\leq\eta$ 形式的停止准则。画出目标函数值和步长随迭代次数变化的曲线。（在高精度确定 $p^\star$ 之后，也可以画出 $f-p^\star$ 随迭代次数变化的曲线。）试验不同的回溯参数 $\alpha$ 和 $\beta$，观察它们对所需总迭代次数的影响。对不同规模的若干问题实例进行这些实验。

- (b) 改用牛顿法重复上述实验，停止准则基于牛顿减量 $\lambda^2$。观察是否出现二次收敛。这里不必像习题 9.27 那样用高效方法计算牛顿步，可以使用通用的稠密求解器，不过最好使用基于 Cholesky 分解的求解器。

*提示。* 用链式法则求出 $\nabla f(x)$ 和 $\nabla^2f(x)$ 的表达式。

**9.31 一些近似牛顿法。** 牛顿法的主要计算代价来自计算 Hessian 矩阵 $\nabla^2f(x)$ 以及求解牛顿方程组。对于大规模问题，有时可以用一个正定近似矩阵代替 Hessian 矩阵，使搜索步更容易构造和求解。本题探讨这种思路的几个常见例子。

对于下面介绍的每种近似牛顿法，用习题 9.30 所述解析中心问题的若干实例测试该方法，并将结果与牛顿法和梯度法得到的结果比较。

<!-- pdf-page: 534 -->

- (a) *复用 Hessian 矩阵。* 每隔 $N$ 次迭代才计算并分解一次 Hessian 矩阵，其中 $N>1$；采用搜索步 $\Delta x=-H^{-1}\nabla f(x)$，其中 $H$ 是最近一次计算得到的 Hessian 矩阵。（每 $N$ 步需要计算并分解一次 Hessian 矩阵；其余各步用回代和前代计算搜索方向。）

- (b) *对角近似。* 用 Hessian 矩阵的对角部分代替整个矩阵，于是只需计算 $n$ 个二阶导数 $\partial^2f(x)/\partial x_i^2$，而且搜索步很容易计算。

**9.32 凸非线性最小二乘问题的 Gauss–Newton 法。** 考虑一个（非线性）最小二乘问题，即最小化如下形式的函数：

$$
f(x)=\frac{1}{2}\sum_{i=1}^mf_i(x)^2,
$$

其中 $f_i$ 是二阶可微函数。$f$ 在 $x$ 处的梯度和 Hessian 矩阵为

$$
\nabla f(x)=\sum_{i=1}^mf_i(x)\nabla f_i(x),\qquad
\nabla^2f(x)=\sum_{i=1}^m\left(\nabla f_i(x)\nabla f_i(x)^T+f_i(x)\nabla^2f_i(x)\right).
$$

我们考虑 $f$ 为凸函数的情形。例如，如果每个 $f_i$ 都是非负凸函数、非正凹函数或仿射函数，就属于这种情形。

Gauss–Newton 法采用搜索方向

$$
\Delta x_{\mathrm{gn}}=-\left(\sum_{i=1}^m\nabla f_i(x)\nabla f_i(x)^T\right)^{-1}\left(\sum_{i=1}^mf_i(x)\nabla f_i(x)\right).
$$

（这里假设逆矩阵存在，即向量 $\nabla f_1(x),\ldots,\nabla f_m(x)$ 张成 $\mathbf{R}^n$。）这个搜索方向可以看作一种近似牛顿方向（见习题 9.31），它通过去掉 $f$ 的 Hessian 矩阵中的二阶导数项得到。

还可以对 Gauss–Newton 搜索方向 $\Delta x_{\mathrm{gn}}$ 给出另一种简单解释。利用一阶近似 $f_i(x+v)\approx f_i(x)+\nabla f_i(x)^Tv$，可得近似式

$$
f(x+v)\approx\frac{1}{2}\sum_{i=1}^m\left(f_i(x)+\nabla f_i(x)^Tv\right)^2.
$$

Gauss–Newton 搜索步 $\Delta x_{\mathrm{gn}}$ 恰好就是使 $f$ 的这个近似式最小的 $v$ 值。（此外，由此可知，求解一个线性最小二乘问题即可算出 $\Delta x_{\mathrm{gn}}$。）

用具有下列形式的若干问题实例测试 Gauss–Newton 法：

$$
f_i(x)=(1/2)x^TA_ix+b_i^Tx+1,
$$

其中 $A_i\in\mathbf{S}_{++}^n$，且 $b_i^TA_i^{-1}b_i\leq2$（这保证 $f$ 为凸函数）。
