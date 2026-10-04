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
