### 分类

**8.23 鲁棒线性判别。** 考虑 (8.23) 给出的鲁棒线性判别问题。

- (a) 证明：最优值 $t^\star$ 为正，当且仅当这两个点集可以被线性分离。当这两个点集可以被线性分离时，证明不等式 $\|a\|_2\leq1$ 在最优点处取等号，即最优的 $a^\star$ 满足 $\|a^\star\|_2=1$。

- (b) 利用变量代换 $\widetilde a=a/t$、$\widetilde b=b/t$，证明问题 (8.23) 等价于以下 QP：

    $$
    \begin{array}{ll}
    \text{最小化} & \|\widetilde a\|_2\\
    \text{约束条件} & \widetilde a^Tx_i-\widetilde b\geq1,\quad i=1,\ldots,N\\
    & \widetilde a^Ty_i-\widetilde b\leq-1,\quad i=1,\ldots,M.
    \end{array}
    $$

**8.24 对权重误差最鲁棒的线性判别。** 假设给定 $\mathbf{R}^n$ 中两个可以被线性分离的点集 $\{x_1,\ldots,x_N\}$ 和 $\{y_1,\ldots,y_M\}$。§8.6.1 说明了如何找到一个既能将两点集分类，又能使函数值间隔最大的仿射函数。也可以考虑它对向量 $a$ 变化的鲁棒性；$a$ 有时称为*权重向量*。给定使 $f(x)=a^Tx-b$ 将这两个点集分离的 $a$ 和 $b$，定义*权重误差余量*（weight error margin）为：使仿射函数 $(a+u)^Tx-b$ 不再将两个点集分离的最小扰动 $u\in\mathbf{R}^n$ 的范数。换句话说，权重误差余量是使

$$
(a+u)^Tx_i\geq b,\quad i=1,\ldots,N,\qquad
(a+u)^Ty_j\leq b,\quad i=1,\ldots,M,
$$

对所有满足 $\|u\|_2\leq\rho$ 的 $u$ 都成立的最大 $\rho$。

说明如何在归一化约束 $\|a\|_2\leq1$ 下，求出使权重误差余量最大的 $a$ 和 $b$。

**8.25 最接近球形的分离椭球。** 给定两组向量 $x_1,\ldots,x_N\in\mathbf{R}^n$ 和 $y_1,\ldots,y_M\in\mathbf{R}^n$，希望找到偏心率最小（即定义椭球的矩阵的条件数最小）的椭球 $\mathcal{E}$，使它满足 $x_i\in\mathcal{E}$，$i=1,\ldots,N$，以及 $y_i\notin\mathbf{int}\mathcal{E}$，$i=1,\ldots,M$。将其表述为凸优化问题。

### 布置与平面布局

**8.26 二次布置。** 考虑 $\mathbf{R}^2$ 中的一个布置问题，由含 $N$ 个节点的无向图 $\mathcal{A}$ 定义，并采用二次代价：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{(i,j)\in\mathcal{A}}\|x_i-x_j\|_2^2.
\end{array}
$$

变量为位置 $x_i\in\mathbf{R}^2$，$i=1,\ldots,M$。位置 $x_i$，$i=M+1,\ldots,N$，是给定的。定义两个向量 $u,v\in\mathbf{R}^M$：

$$
u=(x_{11},x_{21},\ldots,x_{M1}),\qquad
v=(x_{12},x_{22},\ldots,x_{M2}),
$$

它们分别包含自由节点位置的第一分量和第二分量。

<!-- pdf-page: 466 -->

证明可以通过求解两组线性方程

$$
Cu=d_1,\qquad Cv=d_2,
$$

得到 $u$ 和 $v$，其中 $C\in\mathbf{S}^M$。用图 $\mathcal{A}$ 给出 $C$ 各系数的简单表达式。

**8.27 带最小距离约束的问题。** 考虑变量为 $x_1,\ldots,x_N\in\mathbf{R}^k$ 的问题。目标函数 $f_0(x_1,\ldots,x_N)$ 为凸，约束

$$
f_i(x_1,\ldots,x_N)\leq0,\qquad i=1,\ldots,m,
$$

也是凸的（即函数 $f_i:\mathbf{R}^{Nk}\to\mathbf{R}$ 为凸）。此外，还有最小距离约束

$$
\|x_i-x_j\|_2\geq D_{\min},\qquad i\ne j,\quad i,j=1,\ldots,N.
$$

一般来说，这是一个难以求解的非凸问题。

沿用平面布局中的方法，可以构造原问题的*凸限制*（convex restriction），即一个可行集更小的凸问题。（因此，受限问题容易求解，而且它的任何解都保证是原非凸问题的可行解。）设 $a_{ij}\in\mathbf{R}^k$，$i<j$，$i,j=1,\ldots,N$，满足 $\|a_{ij}\|_2=1$。证明受限问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x_1,\ldots,x_N)\\
\text{约束条件} & f_i(x_1,\ldots,x_N)\leq0,\quad i=1,\ldots,m\\
& a_{ij}^T(x_i-x_j)\geq D_{\min},\quad i<j,\quad i,j=1,\ldots,N,
\end{array}
$$

是凸问题，而且每个可行点都满足最小距离约束。

*注。* 选择方向 $a_{ij}$ 有许多很好的启发式方法。一种简单的方法从一个近似解 $\widehat x_1,\ldots,\widehat x_N$ 出发，该近似解不必满足最小距离约束。然后取 $a_{ij}=(\widehat x_i-\widehat x_j)/\|\widehat x_i-\widehat x_j\|_2$。

### 其他问题

**8.28** 设 $\mathcal{P}_1$ 和 $\mathcal{P}_2$ 是两个多面体，表示为

$$
\mathcal{P}_1=\{x\mid Ax\preceq b\},\qquad
\mathcal{P}_2=\{x\mid-\mathbf{1}\preceq Cx\preceq\mathbf{1}\},
$$

其中 $A\in\mathbf{R}^{m\times n}$、$C\in\mathbf{R}^{p\times n}$、$b\in\mathbf{R}^m$。多面体 $\mathcal{P}_2$ 关于原点对称。对 $t\geq0$ 和 $x_c\in\mathbf{R}^n$，用 $t\mathcal{P}_2+x_c$ 表示多面体

$$
t\mathcal{P}_2+x_c=\{tx+x_c\mid x\in\mathcal{P}_2\},
$$

它先将 $\mathcal{P}_2$ 以原点为中心按因子 $t$ 缩放，再把中心平移到 $x_c$。

说明如何通过一个 LP 或一组 LP 求解下面两个问题。

- (a) 找出包含在 $\mathcal{P}_1$ 内的最大多面体 $t\mathcal{P}_2+x_c$，即

    $$
    \begin{array}{ll}
    \text{最大化} & t\\
    \text{约束条件} & t\mathcal{P}_2+x_c\subseteq\mathcal{P}_1\\
    & t\geq0.
    \end{array}
    $$

- (b) 找出包含 $\mathcal{P}_1$ 的最小多面体 $t\mathcal{P}_2+x_c$，即

    $$
    \begin{array}{ll}
    \text{最小化} & t\\
    \text{约束条件} & \mathcal{P}_1\subseteq t\mathcal{P}_2+x_c\\
    & t\geq0.
    \end{array}
    $$

<!-- pdf-page: 467 -->

两个问题中的变量均为 $t\in\mathbf{R}$ 和 $x_c\in\mathbf{R}^n$。

**8.29 多面体外逼近。** 设 $\mathcal{P}=\{x\in\mathbf{R}^n\mid Ax\preceq b\}$ 是一个多面体，$C\subseteq\mathbf{R}^n$ 是给定的集合，不要求它为凸集。利用支撑函数 $S_C$，将下面的问题表述为 LP：

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & C\subseteq t\mathcal{P}+x\\
& t\geq0.
\end{array}
$$

这里，$t\mathcal{P}+x=\{tu+x\mid u\in\mathcal{P}\}$，即将多面体 $\mathcal{P}$ 以原点为中心按因子 $t$ 缩放，再平移 $x$。变量为 $t\in\mathbf{R}$ 和 $x\in\mathbf{R}^n$。

**8.30 用分段圆弧曲线插值。** 给定一串点 $a_1,\ldots,a_n\in\mathbf{R}^2$。构造一条按顺序通过这些点的曲线，并要求每两个相邻点之间都是一段圆弧（即圆的一部分）或线段；线段视为半径无限大的圆弧。连接 $a_i$ 和 $a_{i+1}$ 的圆弧有很多条，可以用圆弧在 $a_i$ 处的切线与线段 $[a_i,a_{i+1}]$ 之间的夹角 $\theta_i\in(-\pi,\pi)$ 对这些圆弧作参数化。因此，$\theta_i=0$ 表示 $a_i$ 与 $a_{i+1}$ 之间的圆弧实际上就是线段 $[a_i,a_{i+1}]$；$\theta_i=\pi/2$ 表示该圆弧是位于线段 $[a_1,a_2]$ 上方的半圆；$\theta_i=-\pi/2$ 表示该圆弧是位于线段 $[a_1,a_2]$ 下方的半圆。如下图所示。

<figure id="fig-exercise-8-30-a" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/exercise-8-30-a.png" alt="相同端点 aᵢ 与 aᵢ₊₁ 之间的四条圆弧或线段，分别标注 θᵢ 等于零、π/4、π/2 和 3π/4，虚线表示端点处的切线方向" data-source-page="467" data-source-rect="221,321,350,436">
</figure>

曲线完全由角 $\theta_1,\ldots,\theta_n$ 确定，各角都可以在区间 $(-\pi,\pi)$ 内选取。$\theta_i$ 的取值会影响曲线的多种性质，例如总弧长 $L$，以及下面介绍的接合角跳变（joint angle discontinuity）。在每个点 $a_i$，$i=2,\ldots,n-1$，都有两段圆弧相接，一段来自前一个点，另一段通向下一个点。如果这两段圆弧在该点的切线方向恰好相反，从而曲线在 $a_i$ 处可微，就称 $a_i$ 处没有接合角跳变。一般地，把 $a_i$ 处的接合角跳变定义为 $|\theta_{i-1}+\theta_i+\psi_i|$，其中 $\psi_i$ 是线段 $[a_i,a_{i+1}]$ 与线段 $[a_{i-1},a_i]$ 之间的夹角，即 $\psi_i=\angle(a_i-a_{i+1},a_{i-1}-a_i)$。如下图所示。注意，角 $\psi_i$ 是已知的，因为 $a_i$ 已知。

<figure id="fig-exercise-8-30-b" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/exercise-8-30-b.png" alt="相邻两段圆弧在 aᵢ 处连接，图中标出端点 aᵢ₋₁、aᵢ、aᵢ₊₁、切线方向以及角 θᵢ₋₁、θᵢ、ψᵢ，虚线画出两段弦及其延长线" data-source-page="467" data-source-rect="155,532,408,607">
</figure>

定义总接合角跳变为

$$
D=\sum_{i=2}^n|\theta_{i-1}+\theta_i+\psi_i|.
$$

将最小化总弧长 $L$ 和总接合角跳变 $D$ 的问题，表述为一个双准则凸优化问题。说明如何求出最优权衡曲线上的端点。

<!-- pdf-page: 468 -->
