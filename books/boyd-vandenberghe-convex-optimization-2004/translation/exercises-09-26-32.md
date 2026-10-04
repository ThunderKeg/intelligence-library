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
