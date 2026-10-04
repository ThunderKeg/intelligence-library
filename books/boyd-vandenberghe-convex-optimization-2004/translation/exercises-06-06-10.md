**6.6 一些罚函数逼近问题的对偶。** 对于下面各个罚函数 $\phi:\mathbf{R}\to\mathbf{R}$，推导问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m\phi(r_i)\\
\text{约束条件} & r=Ax-b,
\end{array}
$$

的一个拉格朗日对偶。变量为 $x\in\mathbf{R}^n$、$r\in\mathbf{R}^m$。

- (a) **死区线性罚函数**（死区宽度为 $a=1$）：

    $$
    \phi(u)=\begin{cases}
    0 & |u|\leq1\\
    |u|-1 & |u|>1.
    \end{cases}
    $$

- (b) **Huber 罚函数**（$M=1$）：

    $$
    \phi(u)=\begin{cases}
    u^2 & |u|\leq1\\
    2|u|-1 & |u|>1.
    \end{cases}
    $$

    <!-- pdf-page: 360 -->

- (c) **对数障碍罚函数**（界限为 $a=1$）：

    $$
    \phi(u)=-\log(1-u^2),\qquad\operatorname{dom}\phi=(-1,1).
    $$

- (d) **相对 1 的偏差**：

    $$
    \phi(u)=\max\{u,1/u\}=\begin{cases}
    u & u\geq1\\
    1/u & u\leq1,
    \end{cases}
    $$

    其中 $\operatorname{dom}\phi=\mathbf{R}_{++}$。

### 正则化与鲁棒逼近

**6.7 采用欧几里得范数的双准则优化。** 考虑双准则优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{R}_+^2\text{）} & (\|Ax-b\|_2^2,\ \|x\|_2^2),
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$ 的秩为 $r$，$b\in\mathbf{R}^m$。说明如何利用 $A$ 的奇异值分解

$$
A=U\operatorname{diag}(\sigma)V^T=\sum_{i=1}^r\sigma_i u_i v_i^T
$$

（见 §A.5.4），求出下面各个问题的解。

- (a) **Tikhonov 正则化：** 最小化 $\|Ax-b\|_2^2+\delta\|x\|_2^2$。

- (b) 在约束 $\|x\|_2^2=\gamma$ 下，最小化 $\|Ax-b\|_2^2$。

- (c) 在约束 $\|x\|_2^2=\gamma$ 下，最大化 $\|Ax-b\|_2^2$。

这里 $\delta$ 和 $\gamma$ 是正参数。

你的结果将为计算这个双准则问题的最优权衡曲线和可达值集合提供高效方法。

**6.8** 将下面的鲁棒逼近问题表述为 LP、QP、SOCP 或 SDP。对每个小问，分别考虑 $\ell_1$、$\ell_2$ 和 $\ell_\infty$ 范数。

- (a) **参数取值只有有限个的随机鲁棒逼近**，即范数和问题

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{i=1}^k p_i\|A_i x-b\|
    \end{array}
    $$

    其中 $p\succeq0$ 且 $\mathbf{1}^Tp=1$。（见 §6.4.1。）

- (b) **系数有上下界的最坏情形鲁棒逼近：**

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sup_{A\in\mathcal{A}}\|Ax-b\|
    \end{array}
    $$

    其中

    $$
    \mathcal{A}=\{A\in\mathbf{R}^{m\times n}\mid l_{ij}\leq a_{ij}\leq u_{ij},\ i=1,\ldots,m,\ j=1,\ldots,n\}.
    $$

    这里通过给出 $A$ 各个元素的上下界来描述不确定性集合。假设 $l_{ij}<u_{ij}$。

- (c) **具有多面体不确定性的最坏情形鲁棒逼近：**

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sup_{A\in\mathcal{A}}\|Ax-b\|
    \end{array}
    $$

    其中

    $$
    \mathcal{A}=\{[a_1\ \cdots\ a_m]^T\mid C_i a_i\preceq d_i,\ i=1,\ldots,m\}.
    $$

    不确定性通过给出每一行的可能取值所构成的多面体 $\mathcal{P}_i=\{a_i\mid C_i a_i\preceq d_i\}$ 来描述。参数 $C_i\in\mathbf{R}^{p_i\times n}$、$d_i\in\mathbf{R}^{p_i}$，$i=1,\ldots,m$，均已给定。假设多面体 $\mathcal{P}_i$ 非空且有界。

<!-- pdf-page: 361 -->

### 函数拟合与插值

**6.9 极小极大有理函数拟合。** 证明下面的问题是拟凸的：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\max_{i=1,\ldots,k}\left|\frac{p(t_i)}{q(t_i)}-y_i\right|
\end{array}
$$

其中

$$
p(t)=a_0+a_1t+a_2t^2+\cdots+a_m t^m,\qquad
q(t)=1+b_1t+\cdots+b_n t^n,
$$

目标函数的定义域定义为

$$
D=\{(a,b)\in\mathbf{R}^{m+1}\times\mathbf{R}^n\mid q(t)>0,\ \alpha\leq t\leq\beta\}.
$$

在这个问题中，我们用有理函数 $p(t)/q(t)$ 拟合给定数据，同时约束分母多项式在区间 $[\alpha,\beta]$ 上为正。优化变量为分子和分母的系数 $a_i$、$b_i$。插值点 $t_i\in[\alpha,\beta]$ 以及期望函数值 $y_i$，$i=1,\ldots,k$，均已给定。

**6.10 用凹、非负且非递减的二次函数拟合数据。** 给定数据

$$
x_1,\ldots,x_N\in\mathbf{R}^n,\qquad y_1,\ldots,y_N\in\mathbf{R},
$$

我们希望拟合一个形如

$$
f(x)=(1/2)x^TPx+q^Tx+r,
$$

的二次函数，其中 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$ 和 $r\in\mathbf{R}$ 是模型中的参数（因此也是拟合问题中的变量）。

这个模型只在盒 $\mathcal{B}=\{x\in\mathbf{R}^n\mid l\preceq x\preceq u\}$ 上使用。可以假设 $l\prec u$，并且给定的数据点 $x_i$ 都位于这个盒内。

我们使用简单的误差平方和目标

$$
\sum_{i=1}^N(f(x_i)-y_i)^2,
$$

作为拟合的准则。此外，还对函数 $f$ 施加若干约束。首先，它必须是凹函数。其次，它在 $\mathcal{B}$ 上必须非负，即对于所有 $z\in\mathcal{B}$，都有 $f(z)\geq0$。第三，$f$ 在 $\mathcal{B}$ 上必须非递减，即只要 $z,\widetilde{z}\in\mathcal{B}$ 满足 $z\preceq\widetilde{z}$，就有 $f(z)\leq f(\widetilde{z})$。

说明如何将这个拟合问题表述为一个凸问题。尽量简化你的表述。
