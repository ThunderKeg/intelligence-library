<!-- pdf-page: 463 -->

**8.11 包含给定点的最小欧几里得锥。** 在 $\mathbf{R}^n$ 中，中心方向为 $c\ne0$、角半径为 $\theta$（$0\leq\theta\leq\pi/2$）的*欧几里得锥*定义为集合

$$
\{x\in\mathbf{R}^n\mid\angle(c,x)\leq\theta\}.
$$

（欧几里得锥是一种二阶锥，即它可以表示为二阶锥在非奇异线性映射下的像。）

设 $a_1,\ldots,a_m\in\mathbf{R}^n$。如何求出包含 $a_1,\ldots,a_m$ 且角半径最小的欧几里得锥？（特别地，应说明如何求解可行性问题，即如何判断是否存在包含这些点的欧几里得锥。）

### 极值体积椭球

**8.12** 证明：包含在一个集合内的最大体积椭球是唯一的。证明：一个集合的 Löwner-John 椭球是唯一的。

**8.13 单纯形的 Löwner-John 椭球。** 本题将证明：要使 $\mathbf{R}^n$ 中单纯形的 Löwner-John 椭球位于该单纯形内，必须将椭球的尺度除以 $n$。由于 Löwner-John 椭球具有仿射不变性，只需对某个特定的单纯形证明这一结论。

求出单纯形 $C=\mathbf{conv}\{0,e_1,\ldots,e_n\}$ 的 Löwner-John 椭球 $\mathcal{E}_{\mathrm{lj}}$。证明：$\mathcal{E}_{\mathrm{lj}}$ 必须按比例 $1/n$ 缩小，才能放入该单纯形内。

**8.14 椭球内逼近的效果。** 设 $C$ 是 $\mathbf{R}^n$ 中的多面体，表示为 $C=\{x\mid Ax\preceq b\}$，并假设 $\{x\mid Ax\prec b\}$ 非空。

- (a) 证明：将包含在 $C$ 内的最大体积椭球以其中心为基准放大 $n$ 倍，得到的椭球包含 $C$。

- (b) 证明：如果 $C$ 关于原点对称，即具有 $C=\{x\mid-\mathbf{1}\preceq Ax\preceq\mathbf{1}\}$ 的形式，那么将最大体积内接椭球放大 $\sqrt n$ 倍，得到的椭球包含 $C$。

**8.15 覆盖椭球之并的最小体积椭球。** 将下面的问题表述为凸优化问题。求最小体积椭球 $\mathcal{E}=\{x\mid(x-x_0)^TA^{-1}(x-x_0)\leq1\}$，使其包含给定的 $K$ 个椭球

$$
\mathcal{E}_i=\{x\mid x^TA_i x+2b_i^Tx+c_i\leq0\},\qquad i=1,\ldots,K.
$$

**提示。** 见附录 B。

**8.16 多面体内的最大体积矩形。** 将下面的问题表述为凸优化问题。求矩形

$$
\mathcal{R}=\{x\in\mathbf{R}^n\mid l\preceq x\preceq u\}
$$

使其包含在多面体 $\mathcal{P}=\{x\mid Ax\preceq b\}$ 内，且体积最大。变量为 $l,u\in\mathbf{R}^n$。所给出的表述不应包含指数级数量的约束。

### 求中心

**8.17 解析中心的仿射不变性。** 证明：一组不等式的解析中心具有仿射不变性。证明：对这些不等式作正比例缩放，解析中心保持不变。

**8.18 解析中心与冗余不等式。** 描述同一个多面体的两组线性不等式，可能具有不同的解析中心。证明：通过添加冗余不等式，可以使多面体

$$
\mathcal{P}=\{x\in\mathbf{R}^n\mid Ax\preceq b\}
$$

的任意内点 $x_0$ 成为<!-- pdf-page: 464 -->解析中心。更具体地，假设 $A\in\mathbf{R}^{m\times n}$ 且 $Ax_0\prec b$。证明：存在 $c\in\mathbf{R}^n$、$\gamma\in\mathbf{R}$ 和正整数 $q$，使得 $\mathcal{P}$ 是以下 $m+q$ 个不等式的解集：

$$
Ax\preceq b,\qquad c^Tx\leq\gamma,\qquad c^Tx\leq\gamma,\qquad\ldots,\qquad c^Tx\leq\gamma
\tag{8.36}
$$

（其中不等式 $c^Tx\leq\gamma$ 被添加了 $q$ 次），并且 $x_0$ 是 (8.36) 的解析中心。

**8.19** 设 $x_{\mathrm{ac}}$ 是一组线性不等式

$$
a_i^Tx\leq b_i,\qquad i=1,\ldots,m
$$

的解析中心，并将 $H$ 定义为对数障碍函数在 $x_{\mathrm{ac}}$ 处的 Hessian 矩阵：

$$
H=\sum_{i=1}^m\frac{1}{(b_i-a_i^Tx_{\mathrm{ac}})^2}a_i a_i^T.
$$

证明：如果

$$
b_k-a_k^Tx_{\mathrm{ac}}\geq m(a_k^TH^{-1}a_k)^{1/2},
$$

那么第 $k$ 个不等式是冗余的，即删除它不会改变可行集。

**8.20 由线性矩阵不等式的解析中心得到椭球逼近。** 设 $C$ 是线性矩阵不等式（LMI）

$$
x_1A_1+x_2A_2+\cdots+x_nA_n\preceq B
$$

的解集，其中 $A_i,B\in\mathbf{S}^m$，并设 $x_{\mathrm{ac}}$ 为其解析中心。证明：

$$
\mathcal{E}_{\mathrm{inner}}\subseteq C\subseteq\mathcal{E}_{\mathrm{outer}},
$$

其中

$$
\begin{aligned}
\mathcal{E}_{\mathrm{inner}}&=\{x\mid(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})\leq1\},\\
\mathcal{E}_{\mathrm{outer}}&=\{x\mid(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})\leq m(m-1)\},
\end{aligned}
$$

$H$ 是对数障碍函数

$$
-\log\det(B-x_1A_1-x_2A_2-\cdots-x_nA_n)
$$

在 $x_{\mathrm{ac}}$ 处的 Hessian 矩阵。

**8.21 [BYT99] 解析中心的最大似然解释。** 使用第 352 页的线性测量模型

$$
y=Ax+v,
$$

其中 $A\in\mathbf{R}^{m\times n}$。假设噪声分量 $v_i$ 独立同分布，支撑集为 $[-1,1]$。与测量值 $y\in\mathbf{R}^m$ 相容的参数 $x$ 所构成的集合，是由线性不等式

$$
-\mathbf{1}+y\preceq Ax\preceq\mathbf{1}+y
\tag{8.37}
$$

定义的多面体。

假设 $v_i$ 的概率密度函数具有以下形式：

$$
p(v)=
\begin{cases}
\alpha_r(1-v^2)^r&-1\leq v\leq1,\\
0&\text{其他情况},
\end{cases}
$$

其中 $r\geq1$ 且 $\alpha_r>0$。证明：$x$ 的最大似然估计是 (8.37) 的解析中心。

**8.22 重心。** 内部非空的集合 $C\subseteq\mathbf{R}^n$ 的*重心*（center of gravity）定义为

$$
x_{\mathrm{cg}}=\frac{\int_C u\,du}{\int_C1\,du}.
$$

<!-- pdf-page: 465 -->

重心具有仿射不变性，而且显然只由集合 $C$ 本身决定，与集合的具体描述方式无关。不过，与本章介绍的其他中心不同，除了简单的情况（例如椭球、球、单纯形），重心很难计算。

证明：下列凸函数在重心 $x_{\mathrm{cg}}$ 处取得最小值：

$$
f(x)=\int_C\|u-x\|_2^2\,du.
$$
