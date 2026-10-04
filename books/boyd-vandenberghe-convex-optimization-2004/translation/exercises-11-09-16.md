**11.9 中心路径附近的对偶可行点。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$。假设函数 $f_i$ 是凸函数且二阶可微。（为简单起见，假设没有等式约束。）回顾 §11.2.2（第 565 页），$\lambda_i=-1/(tf_i(x^\star(t)))$，$i=1,\ldots,m$，是对偶可行的，而且 $x^\star(t)$ 实际上使 $L(x,\lambda)$ 最小。由此可以算出 $\lambda$ 处的对偶函数值为 $g(\lambda)=f_0(x^\star(t))-m/t$。特别地，可以断定 $x^\star(t)$ 的次优程度不超过 $m/t$。

本题考察点 $x$ 接近 $x^\star(t)$、但尚未完全中心化时的情况。（如果中心化步骤提前停止，或者没有计算到足够高的精度，就会出现这种情况。）此时，当然不能断言 $\lambda_i=-1/(tf_i(x))$，$i=1,\ldots,m$，是对偶可行的，也不能断言 $x$ 的次优程度不超过 $m/t$。不过，只要 $x$ 足够接近中心点，一个稍复杂的公式就能给出对偶可行点。

设 $\Delta x_{\mathrm{nt}}$ 是中心化问题

$$
\begin{array}{ll}
\text{最小化} & tf_0(x)-\sum_{i=1}^m\log(-f_i(x))
\end{array}
$$

在 $x$ 处的牛顿步。当 $\Delta x_{\mathrm{nt}}$ 很小（即 $x$ 已接近中心点）时，下面的公式往往能给出一个对偶可行点：

$$
\lambda_i=\frac{1}{-tf_i(x)}\left(1+\frac{\nabla f_i(x)^T\Delta x_{\mathrm{nt}}}{-f_i(x)}\right),
\qquad i=1,\ldots,m.
$$

在这种情况下，向量 $x$ 并不使 $L(x,\lambda)$ 最小，因此没有适用于一般情形的公式来计算与 $\lambda$ 对应的对偶函数值 $g(\lambda)$。（不过，如果已知对偶目标的解析表达式，就可以直接计算 $g(\lambda)$。）

验证，对于 QCQP

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TP_0x+q_0^Tx+r_0\\
\text{约束条件} & (1/2)x^TP_ix+q_i^Tx+r_i\leq0,\quad i=1,\ldots,m,
\end{array}
$$

当 $\Delta x_{\mathrm{nt}}$ 足够小时，上述 $\lambda$ 的公式会给出一个对偶可行点（即 $\lambda\succeq0$，且 $L(x,\lambda)$ 下方有界）。

<!-- pdf-page: 640 -->

*提示。* 定义

$$
x_0=x+\Delta x_{\mathrm{nt}},\qquad
x_i=x-\frac{1}{t\lambda_if_i(x)}\Delta x_{\mathrm{nt}},\quad i=1,\ldots,m.
$$

证明

$$
\nabla f_0(x_0)+\sum_{i=1}^m\lambda_i\nabla f_i(x_i)=0.
$$

然后利用 $f_i(z)\geq f_i(x_i)+\nabla f_i(x_i)^T(z-x_i)$，$i=0,\ldots,m$，推导 $L(z,\lambda)$ 的一个下界。

**11.10 中心路径的另一种参数化。** 考虑问题 (11.1)。对于 $t>0$，其中心路径 $x^\star(t)$ 定义为下列问题的解：

$$
\begin{array}{ll}
\text{最小化} & tf_0(x)-\sum_{i=1}^m\log(-f_i(x))\\
\text{约束条件} & Ax=b.
\end{array}
$$

本题探讨中心路径的另一种参数化。

对于 $u>p^\star$，用 $z^\star(u)$ 表示下列问题的解：

$$
\begin{array}{ll}
\text{最小化} & -\log(u-f_0(x))-\sum_{i=1}^m\log(-f_i(x))\\
\text{约束条件} & Ax=b.
\end{array}
$$

证明，当 $u>p^\star$ 时，由 $z^\star(u)$ 定义的曲线就是中心路径。（换言之，对于每个 $u>p^\star$，都存在 $t>0$，使 $x^\star(t)=z^\star(u)$；反过来，对于每个 $t>0$，都存在 $u>p^\star$，使 $z^\star(u)=x^\star(t)$。）

**11.11 解析中心法。** 本题考虑障碍法的一种变体，它以习题 11.10 描述的中心路径参数化为基础。为简单起见，考虑没有等式约束的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

解析中心法从任意严格可行初始点 $x^{(0)}$ 和任意 $u^{(0)}>f_0(x^{(0)})$ 出发。先令

$$
u^{(1)}=\theta u^{(0)}+(1-\theta)f_0(x^{(0)}),
$$

其中 $\theta\in(0,1)$ 是算法参数（通常取较小的值），再计算下一个迭代点

$$
x^{(1)}=z^\star(u^{(1)})
$$

（使用牛顿法，以 $x^{(0)}$ 为初始点）。这里 $z^\star(s)$ 表示

$$
-\log(s-f_0(x))-\sum_{i=1}^m\log(-f_i(x))
$$

的极小点，假设它存在且唯一。然后重复上述过程。

点 $z^\star(s)$ 是不等式

$$
f_0(x)\leq s,\qquad f_1(x)\leq0,\ldots,f_m(x)\leq0
$$

的解析中心，算法由此得名。

证明，中心法是有效的，即 $x^{(k)}$ 收敛到一个最优点。找出一个停止准则，保证 $x$ 是 $\epsilon$ 次优点，其中 $\epsilon>0$。

*提示。* 点 $x^{(k)}$ 位于中心路径上，见习题 11.10。利用这一点证明

$$
u^+-p^\star\leq\frac{m+\theta}{m+1}(u-p^\star),
$$

其中 $u$ 和 $u^+$ 是相邻两次迭代中的 $u$ 值。

<!-- pdf-page: 641 -->

**11.12 凸–凹博弈的障碍法。** 考虑带不等式约束的凸–凹博弈

$$
\begin{array}{ll}
\text{最小化}_w\ \text{最大化}_z & f_0(w,z)\\
\text{约束条件} & f_i(w)\leq0,\quad i=1,\ldots,m\\
& \tilde f_i(z)\leq0,\quad i=1,\ldots,\tilde m.
\end{array}
$$

这里，$w\in\mathbf{R}^n$ 是用于最小化目标的变量，$z\in\mathbf{R}^{\tilde n}$ 是用于最大化目标的变量。约束函数 $f_i$ 和 $\tilde f_i$ 是凸函数且可微，目标函数 $f_0$ 可微且为凸–凹函数，即固定任意 $z$ 时关于 $w$ 是凸的，固定任意 $w$ 时关于 $z$ 是凹的。为简单起见，假设 $\mathbf{dom}\,f_0=\mathbf{R}^n\times\mathbf{R}^{\tilde n}$。

博弈的一个*解*或*鞍点*是一对 $w^\star,z^\star$，使

$$
f_0(w^\star,z)\leq f_0(w^\star,z^\star)\leq f_0(w,z^\star)
$$

对每个可行的 $w$ 和 $z$ 都成立。（凸–凹博弈和凸–凹函数的背景，见 §5.4.3、§10.3.4，以及习题 3.14、5.24、5.25、10.10 和 10.13。）本题将说明如何利用障碍法的一个扩展和不可行初始点牛顿法（见 §10.3）求解这个博弈。

- (a) 设 $t>0$。说明为什么函数

    $$
    tf_0(w,z)-\sum_{i=1}^m\log(-f_i(w))+\sum_{i=1}^{\tilde m}\log(-\tilde f_i(z))
    $$

    关于 $(w,z)$ 是凸–凹函数。假设它有唯一的鞍点 $(w^\star(t),z^\star(t))$，可以用不可行初始点牛顿法求出。

- (b) 与用于求解凸优化问题的障碍法一样，可以推导出 $(w^\star(t),z^\star(t))$ 次优程度的一个简单上界。该上界只依赖于问题维度，并随着 $t$ 增大而减小到零。用 $W$ 和 $Z$ 分别表示 $w$ 和 $z$ 的可行集：

    $$
    W=\{w\mid f_i(w)\leq0,\ i=1,\ldots,m\},\qquad
    Z=\{z\mid\tilde f_i(z)\leq0,\ i=1,\ldots,\tilde m\}.
    $$

    证明

    $$
    \begin{aligned}
    f_0(w^\star(t),z^\star(t))&\leq\inf_{w\in W}f_0(w,z^\star(t))+\frac{m}{t},\\
    f_0(w^\star(t),z^\star(t))&\geq\sup_{z\in Z}f_0(w^\star(t),z)-\frac{\tilde m}{t},
    \end{aligned}
    $$

    因而

    $$
    \sup_{z\in Z}f_0(w^\star(t),z)-\inf_{w\in W}f_0(w,z^\star(t))\leq\frac{m+\tilde m}{t}.
    $$

### 自协调性与复杂度分析

**11.13 自协调性与负熵。**

- (a) 证明，负熵函数 $x\log x$（定义在 $\mathbf{R}_{++}$ 上）不是自协调函数。

- (b) 证明，对于任意 $t>0$，$tx\log x-\log x$（定义在 $\mathbf{R}_{++}$ 上）都是自协调函数。

**11.14 自协调性与中心化问题。** 设 $\phi$ 是问题 (11.1) 的对数障碍函数。假设 (11.1) 的下水平集有界，并且 $tf_0+\phi$ 是闭函数且自协调。证明，对于所有 $x\in\mathbf{dom}\,\phi$，都有 $t\nabla^2f_0(x)+\nabla^2\phi(x)\succ0$。*提示。* 见习题 9.17 和 11.3。

<!-- pdf-page: 642 -->

### 广义不等式的障碍法

**11.15 广义对数是 $K$ 递增的。** 设 $\psi$ 是正常锥 $K$ 的一个广义对数，且 $y\succ_K0$。

- (a) 证明，$\nabla\psi(y)\succeq_{K^*}0$，即 $\psi$ 是 $K$ 非减的。*提示。* 如果 $\nabla\psi(y)\nsucceq_{K^*}0$，那么存在某个 $w\succ_K0$，使 $w^T\nabla\psi(y)\leq0$。利用不等式 $\psi(sw)\leq\psi(y)+\nabla\psi(y)^T(sw-y)$，其中 $s>0$。

- (b) 进一步证明，$\nabla\psi(y)\succ_{K^*}0$，即 $\psi$ 是 $K$ 递增的。*提示。* 证明，$\nabla^2\psi(y)\prec0$ 和 $\nabla\psi(y)\succeq_{K^*}0$ 蕴含 $\nabla\psi(y)\succ_{K^*}0$。

**11.16 [NN94，第 41 页] 广义对数的性质。** 设 $\psi$ 是正常锥 $K$ 的一个广义对数，次数为 $\theta$。证明，下列性质对任意 $y\succ_K0$ 都成立。

- (a) 对所有 $s>0$，都有 $\nabla\psi(sy)=\nabla\psi(y)/s$。

- (b) $\nabla\psi(y)=-\nabla^2\psi(y)y$。

- (c) $y^T\nabla\psi^2(y)y=-\theta$。

- (d) $\nabla\psi(y)^T\nabla^2\psi(y)^{-1}\nabla\psi(y)=-\theta$。
