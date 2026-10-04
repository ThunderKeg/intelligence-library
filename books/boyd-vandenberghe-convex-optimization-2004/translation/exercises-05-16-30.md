**5.16 不等式约束的精确罚函数法。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}
\tag{5.110}
$$

其中函数 $f_i:\mathbf{R}^n\to\mathbf{R}$ 可微且凸。在**精确罚函数法**（exact penalty method）中，我们求解辅助问题

$$
\begin{array}{ll}
\text{最小化} & \phi(x)=f_0(x)+\alpha\max_{i=1,\ldots,m}\max\{0,f_i(x)\},
\end{array}
\tag{5.111}
$$

其中 $\alpha>0$ 为参数。$\phi$ 中的第二项用于惩罚 $x$ 违反约束的程度。如果 $\alpha$ 充分大时，辅助问题 (5.111) 的解也都是原问题 (5.110) 的解，就称这种方法为精确罚函数法。

- (a) 证明 $\phi$ 是凸函数。

- (b) 辅助问题可以表示为

    $$
    \begin{array}{ll}
    \text{最小化} & f_0(x)+\alpha y\\
    \text{约束条件} & f_i(x)\leq y,\quad i=1,\ldots,m\\
    & 0\leq y,
    \end{array}
    $$

    其中变量为 $x$ 和 $y\in\mathbf{R}$。求这个问题的拉格朗日对偶，并用 (5.110) 的拉格朗日对偶函数 $g$ 表示它。

    <!-- pdf-page: 292 -->

- (c) 利用 (b) 中的结果证明下面的性质。设 $\lambda^\star$ 是 (5.110) 的拉格朗日对偶的一个最优解，并且强对偶性成立。如果 $\alpha>\mathbf{1}^T\lambda^\star$，则辅助问题 (5.111) 的任意解也是 (5.110) 的最优解。

**5.17 具有多面体不确定性的鲁棒线性规划。** 考虑鲁棒 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \displaystyle\sup_{a\in\mathcal{P}_i}a^Tx\leq b_i,\quad i=1,\ldots,m,
\end{array}
$$

变量为 $x\in\mathbf{R}^n$，其中 $\mathcal{P}_i=\{a\mid C_i a\preceq d_i\}$。问题数据为 $c\in\mathbf{R}^n$、$C_i\in\mathbf{R}^{m_i\times n}$、$d_i\in\mathbf{R}^{m_i}$ 和 $b\in\mathbf{R}^m$。我们假设各多面体 $\mathcal{P}_i$ 非空。

证明这个问题等价于 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & d_i^Tz_i\leq b_i,\quad i=1,\ldots,m\\
& C_i^Tz_i=x,\quad i=1,\ldots,m\\
& z_i\succeq0,\quad i=1,\ldots,m,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $z_i\in\mathbf{R}^{m_i}$，$i=1,\ldots,m$。*提示：* 求在 $a_i\in\mathcal{P}_i$ 上最大化 $a_i^Tx$ 的问题的对偶，其中变量为 $a_i$。

**5.18 两个多面体之间的分离超平面。** 将下面的问题表示为一个 LP 或 LP 可行性问题。求一个分离超平面，严格分离两个多面体

$$
\mathcal{P}_1=\{x\mid Ax\preceq b\},\qquad
\mathcal{P}_2=\{x\mid Cx\preceq d\},
$$

即求向量 $a\in\mathbf{R}^n$ 和标量 $\gamma$，使得

$$
a^Tx>\gamma\quad\text{对 }x\in\mathcal{P}_1,\qquad
a^Tx<\gamma\quad\text{对 }x\in\mathcal{P}_2.
$$

可以假设 $\mathcal{P}_1$ 与 $\mathcal{P}_2$ 不相交。

*提示：* 向量 $a$ 和标量 $\gamma$ 必须满足

$$
\inf_{x\in\mathcal{P}_1}a^Tx>\gamma>\sup_{x\in\mathcal{P}_2}a^Tx.
$$

利用 LP 对偶性简化这些条件中的下确界和上确界。

**5.19 向量中最大的若干个元素之和。** 定义 $f:\mathbf{R}^n\to\mathbf{R}$ 为

$$
f(x)=\sum_{i=1}^r x_{[i]},
$$

其中 $r$ 是 $1$ 到 $n$ 之间的整数，$x_{[1]}\geq x_{[2]}\geq\cdots\geq x_{[r]}$ 是 $x$ 的分量按降序排列后的结果。换言之，$f(x)$ 是 $x$ 中最大的 $r$ 个元素之和。本题研究约束

$$
f(x)\leq\alpha.
$$

正如第 3 章第 80 页中所述，这是一个凸约束，等价于下面这组含 $n!/(r!(n-r)!)$ 个线性不等式的约束：

$$
x_{i_1}+\cdots+x_{i_r}\leq\alpha,\qquad
1\leq i_1<i_2<\cdots<i_r\leq n.
$$

本题的目的是推导一种更紧凑的表示。

<!-- pdf-page: 293 -->

- (a) 给定向量 $x\in\mathbf{R}^n$，证明 $f(x)$ 等于 LP

    $$
    \begin{array}{ll}
    \text{最大化} & x^Ty\\
    \text{约束条件} & 0\preceq y\preceq\mathbf{1}\\
    & \mathbf{1}^Ty=r
    \end{array}
    $$

    的最优值，其中变量为 $y\in\mathbf{R}^n$。

- (b) 推导 (a) 中 LP 的对偶。证明它可以写成

    $$
    \begin{array}{ll}
    \text{最小化} & rt+\mathbf{1}^Tu\\
    \text{约束条件} & t\mathbf{1}+u\succeq x\\
    & u\succeq0,
    \end{array}
    $$

    其中变量为 $t\in\mathbf{R}$、$u\in\mathbf{R}^n$。由对偶性，这个 LP 与 (a) 中的 LP 有相同的最优值，即 $f(x)$。因此得到如下结果：$x$ 满足 $f(x)\leq\alpha$，当且仅当存在 $t\in\mathbf{R}$、$u\in\mathbf{R}^n$，使得

    $$
    rt+\mathbf{1}^Tu\leq\alpha,\qquad
    t\mathbf{1}+u\succeq x,\qquad
    u\succeq0.
    $$

    这些条件构成关于 $x,u,t$ 这 $2n+1$ 个变量的一组 $2n+1$ 个线性不等式。

- (c) 作为一个应用，我们考虑第 4 章第 155 页讨论过的经典 Markowitz 投资组合优化问题

    $$
    \begin{array}{ll}
    \text{最小化} & x^T\Sigma x\\
    \text{约束条件} & \bar p^Tx\geq r_{\min}\\
    & \mathbf{1}^Tx=1,\quad x\succeq0
    \end{array}
    $$

    的一个扩展。变量为投资组合 $x\in\mathbf{R}^n$；$\bar p$ 和 $\Sigma$ 分别是价格变化向量 $p$ 的均值和协方差矩阵。

    假设增加一个*分散化约束*，要求投向任意 $10\%$ 的资产的资金不得超过总预算的 $80\%$。这个约束可以表示为

    $$
    \sum_{i=1}^{\lfloor0.1n\rfloor}x_{[i]}\leq0.8.
    $$

    将带有分散化约束的投资组合优化问题表示为一个 QP。

**5.20 信道容量问题的对偶。** 推导问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle-c^Tx+\sum_{i=1}^m y_i\log y_i\\
\text{约束条件} & Px=y\\
& x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

的一个对偶问题，其中 $P\in\mathbf{R}^{m\times n}$ 的元素非负，且各列元素之和为一（即 $P^T\mathbf{1}=\mathbf{1}$）。变量为 $x\in\mathbf{R}^n$、$y\in\mathbf{R}^m$。（当 $c_j=\sum_{i=1}^m p_{ij}\log p_{ij}$ 时，最优值与信道转移概率矩阵为 $P$ 的离散无记忆信道容量的负值只相差一个 $\log2$ 因子；见习题 4.57。）

尽可能简化对偶问题。

<!-- pdf-page: 294 -->

### 强对偶性与 Slater 条件

**5.21 强对偶性不成立的凸问题。** 考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & e^{-x}\\
\text{约束条件} & x^2/y\leq0,
\end{array}
$$

变量为 $x$ 和 $y$，定义域为 $\mathcal{D}=\{(x,y)\mid y>0\}$。

- (a) 验证这是一个凸优化问题。求其最优值。

- (b) 给出拉格朗日对偶问题，并求对偶问题的最优解 $\lambda^\star$ 和最优值 $d^\star$。最优对偶间隙是多少？

- (c) 这个问题满足 Slater 条件吗？

- (d) 扰动问题

    $$
    \begin{array}{ll}
    \text{最小化} & e^{-x}\\
    \text{约束条件} & x^2/y\leq u
    \end{array}
    $$

    的最优值 $p^\star(u)$ 作为 $u$ 的函数是什么？验证全局灵敏度不等式

    $$
    p^\star(u)\geq p^\star(0)-\lambda^\star u
    $$

    不成立。

**5.22 对偶性的几何解释。** 对下面每个优化问题，画出集合

$$
\begin{aligned}
\mathcal{G}&=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)=t,\ f_1(x)=u\},\\
\mathcal{A}&=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)\leq t,\ f_1(x)\leq u\}
\end{aligned}
$$

的示意图，给出对偶问题，并求解原问题和对偶问题。问题是凸的吗？是否满足 Slater 条件？强对偶性是否成立？

除非另有说明，问题的定义域为 $\mathbf{R}$。

- (a) 在 $x^2\leq1$ 的约束下最小化 $x$。

- (b) 在 $x^2\leq0$ 的约束下最小化 $x$。

- (c) 在 $|x|\leq0$ 的约束下最小化 $x$。

- (d) 在 $f_1(x)\leq0$ 的约束下最小化 $x$，其中

    $$
    f_1(x)=
    \begin{cases}
    -x+2 & x\geq1,\\
    x & -1\leq x\leq1,\\
    -x-2 & x\leq-1.
    \end{cases}
    $$

- (e) 在 $-x+1\leq0$ 的约束下最小化 $x^3$。

- (f) 在 $-x+1\leq0$ 的约束下最小化 $x^3$，定义域为 $\mathcal{D}=\mathbf{R}_+$。

**5.23 线性规划中的强对偶性。** 我们证明，只要 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b
\end{array}
$$

及其对偶

$$
\begin{array}{ll}
\text{最大化} & -b^Tz\\
\text{约束条件} & A^Tz+c=0,\quad z\succeq0
\end{array}
$$

中至少一个问题可行，强对偶性就成立。换言之，强对偶性唯一可能不成立的情形是 $p^\star=\infty$ 且 $d^\star=-\infty$。

<!-- pdf-page: 295 -->

- (a) 假设 $p^\star$ 有限，且 $x^\star$ 是一个最优解。（LP 的最优值若有限，就一定能达到。）设 $I\subseteq\{1,2,\ldots,m\}$ 为在 $x^\star$ 处的有效约束的指标集：

    $$
    a_i^Tx^\star=b_i,\quad i\in I,\qquad
    a_i^Tx^\star<b_i,\quad i\notin I.
    $$

    证明存在 $z\in\mathbf{R}^m$，满足

    $$
    z_i\geq0,\quad i\in I,\qquad
    z_i=0,\quad i\notin I,\qquad
    \sum_{i\in I}z_i a_i+c=0.
    $$

    证明 $z$ 是对偶最优解，其目标值为 $c^Tx^\star$。

    *提示：* 假设不存在这样的 $z$，即 $-c\notin\{\sum_{i\in I}z_i a_i\mid z_i\geq0\}$。利用第 49 页例 2.20 中的严格分离超平面定理导出矛盾。也可以使用 Farkas 引理（见 §5.8.3）。

- (b) 假设 $p^\star=\infty$ 且对偶问题可行。证明 $d^\star=\infty$。*提示：* 证明存在非零的 $v\in\mathbf{R}^m$，使得 $A^Tv=0$、$v\succeq0$、$b^Tv<0$。如果对偶问题可行，它就沿方向 $v$ 无界。

- (c) 考虑例子

    $$
    \begin{array}{ll}
    \text{最小化} & x\\
    \text{约束条件} &
    \begin{bmatrix}0\\1\end{bmatrix}x
    \preceq
    \begin{bmatrix}-1\\1\end{bmatrix}.
    \end{array}
    $$

    写出对偶 LP，并求解原问题和对偶问题。证明 $p^\star=\infty$ 且 $d^\star=-\infty$。

**5.24 弱极大极小不等式。** 证明弱极大极小不等式

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)
\leq
\inf_{w\in W}\sup_{z\in Z}f(w,z)
$$

*总是*成立，无须对 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$、$W\subseteq\mathbf{R}^n$ 或 $Z\subseteq\mathbf{R}^m$ 作任何假设。

**5.25** [BL00，第 95 页] **凸凹函数与鞍点性质。** 我们推导鞍点性质

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)
=
\inf_{w\in W}\sup_{z\in Z}f(w,z)
\tag{5.112}
$$

成立的条件，其中 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$、$W\times Z\subseteq\operatorname{dom}f$，且 $W$ 和 $Z$ 非空。我们假设，对每个 $z\in Z$，函数

$$
g_z(w)=
\begin{cases}
f(w,z) & w\in W,\\
\infty & \text{其他情形}
\end{cases}
$$

都是闭凸函数；对每个 $w\in W$，函数

$$
h_w(z)=
\begin{cases}
-f(w,z) & z\in Z,\\
\infty & \text{其他情形}
\end{cases}
$$

也都是闭凸函数。

- (a) (5.112) 的右端可以表示为 $p(0)$，其中

    $$
    p(u)=\inf_{w\in W}\sup_{z\in Z}\bigl(f(w,z)+u^Tz\bigr).
    $$

    证明 $p$ 是凸函数。

    <!-- pdf-page: 296 -->

- (b) 证明 $p$ 的共轭函数为

    $$
    p^*(v)=
    \begin{cases}
    -\inf_{w\in W}f(w,v) & v\in Z,\\
    \infty & \text{其他情形}.
    \end{cases}
    $$

- (c) 证明 $p^*$ 的共轭函数为

    $$
    p^{**}(u)=\sup_{z\in Z}\inf_{w\in W}\bigl(f(w,z)+u^Tz\bigr).
    $$

    将此式与 (a) 结合，就可以把极大极小等式 (5.112) 表示为 $p^{**}(0)=p(0)$。

- (d) 由习题 3.28 和 3.39(d) 可知，若 $0\in\operatorname{int}\operatorname{dom}p$，则 $p^{**}(0)=p(0)$。由此得出，若 $W$ 和 $Z$ 有界，这一等式成立。

- (e) 习题 3.28 和 3.39 还有一个推论：若 $0\in\operatorname{dom}p$ 且 $p$ 是闭函数，则 $p^{**}(0)=p(0)$。证明，如果 $g_z$ 的下水平集有界，则 $p$ 是闭函数。

### 最优性条件

**5.26** 考虑 QCQP

$$
\begin{array}{ll}
\text{最小化} & x_1^2+x_2^2\\
\text{约束条件} & (x_1-1)^2+(x_2-1)^2\leq1\\
& (x_1-1)^2+(x_2+1)^2\leq1,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^2$。

- (a) 画出可行集和目标函数等值线的示意图。求最优点 $x^\star$ 和最优值 $p^\star$。

- (b) 给出 KKT 条件。是否存在拉格朗日乘子 $\lambda_1^\star$ 和 $\lambda_2^\star$，能够证明 $x^\star$ 最优？

- (c) 推导并求解拉格朗日对偶问题。强对偶性成立吗？

**5.27 带等式约束的最小二乘。** 考虑带等式约束的最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2\\
\text{约束条件} & Gx=h,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$ 且 $\operatorname{rank}A=n$，$G\in\mathbf{R}^{p\times n}$ 且 $\operatorname{rank}G=p$。

给出 KKT 条件，并推导原问题解 $x^\star$ 和对偶问题解 $\nu^\star$ 的表达式。

**5.28** 证明（不使用任何线性规划代码），LP

$$
\begin{array}{ll}
\text{最小化} & 47x_1+93x_2+17x_3-93x_4\\
\text{约束条件} &
\begin{bmatrix}
-1&-6&1&3\\
-1&-2&7&1\\
0&3&-10&-1\\
-6&-11&-2&12\\
1&6&-1&-3
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\\x_3\\x_4\end{bmatrix}
\preceq
\begin{bmatrix}-3\\5\\-8\\-7\\4\end{bmatrix}
\end{array}
$$

的最优解唯一，且为 $x^\star=(1,1,1,1)$。

**5.29** 问题

$$
\begin{array}{ll}
\text{最小化} & -3x_1^2+x_2^2+2x_3^2+2(x_1+x_2+x_3)\\
\text{约束条件} & x_1^2+x_2^2+x_3^2=1,
\end{array}
$$

是 (5.32) 的一个特例，所以即使该问题不是凸问题，强对偶性仍然成立。推导 KKT 条件。求所有满足 KKT 条件的解 $x,\nu$。其中哪一对对应最优解？

<!-- pdf-page: 297 -->

**5.30** 推导问题

$$
\begin{array}{ll}
\text{最小化} & \operatorname{tr}X-\log\det X\\
\text{约束条件} & Xs=y,
\end{array}
$$

的 KKT 条件，其中变量为 $X\in\mathbf{S}^n$，定义域为 $\mathbf{S}_{++}^n$。给定 $y\in\mathbf{R}^n$ 和 $s\in\mathbf{R}^n$，且 $s^Ty=1$。验证最优解为

$$
X^\star=I+yy^T-\frac{1}{s^Ts}ss^T.
$$
