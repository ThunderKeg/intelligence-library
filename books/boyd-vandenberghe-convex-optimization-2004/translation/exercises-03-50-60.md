<!-- pdf-page: 137 -->

**3.50 多项式系数作为根的函数。** 证明：如果一个多项式的根都是负实数，那么它的系数是这些根的对数凹函数。换句话说，由恒等式

$$
s^n+a_1(\lambda)s^{n-1}+\cdots+a_{n-1}(\lambda)s+a_n(\lambda)=(s-\lambda_1)\cdots(s-\lambda_n)
$$

定义的函数 $a_i:\mathbf{R}^n\to\mathbf{R}$ 在 $-\mathbf{R}_{++}^n$ 上是对数凹的。

**提示：** 函数

$$
S_k(x)=\sum_{1\leq i_1<i_2<\cdots<i_k\leq n}x_{i_1}\cdots x_{i_k},
$$

其中 $\operatorname{dom}S_k\in\mathbf{R}_+^n$、$1\leq k\leq n$，称为 $\mathbf{R}^n$ 上的第 $k$ 个初等对称函数。可以证明，$S_k^{1/k}$ 是凹函数（见 [ML57]）。

**3.51** [BL00, 第 41 页] 设 $p$ 是 $\mathbf{R}$ 上的一个多项式，它的所有根都是实数。证明：在 $p$ 为正的任意区间上，$p$ 都是对数凹的。

**3.52** [MO79, 第 3.E.2 节] **矩函数的对数凸性。** 设 $f:\mathbf{R}\to\mathbf{R}$ 是一个非负函数，且 $\mathbf{R}_+\subseteq\operatorname{dom}f$。对于 $x\geq0$，定义

$$
\phi(x)=\int_0^\infty u^xf(u)\,du.
$$

证明 $\phi$ 是对数凸函数。（当 $x$ 是正整数、$f$ 是概率密度时，$\phi(x)$ 就是其 $x$ 阶矩。）利用这一结论证明 Gamma 函数

$$
\Gamma(x)=\int_0^\infty u^{x-1}e^{-u}\,du
$$

在 $x\geq1$ 时是对数凸的。

**3.53** 设 $x$ 和 $y$ 是 $\mathbf{R}^n$ 中相互独立的随机向量，其概率密度 $f$ 和 $g$ 都是对数凹的。证明 $z=x+y$ 的概率密度是对数凹的。

**3.54 高斯累积分布函数的对数凹性。** 高斯累积分布函数

$$
f(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt
$$

是对数凹的；这一点可由对数凹函数的卷积仍为对数凹函数这一结论推出。本题将引导你给出一个简单、独立的证明。回忆一下，$f$ 是对数凹函数，当且仅当对所有 $x$ 都有 $f''(x)f(x)\leq f'(x)^2$。

- (a) 验证：当 $x\geq0$ 时，有 $f''(x)f(x)\leq f'(x)^2$。剩下的难点是 $x<0$ 的情形。
- (b) 证明：对所有 $t$ 和 $x$，都有 $t^2/2\geq-x^2/2+xt$。
- (c) 利用 (b) 中的结论得到 $e^{-t^2/2}\leq e^{x^2/2-xt}$，进而说明：当 $x<0$ 时，

    $$
    \int_{-\infty}^x e^{-t^2/2}\,dt\leq e^{x^2/2}\int_{-\infty}^x e^{-xt}\,dt.
    $$

- (d) 利用 (c) 中的结论，验证：当 $x\leq0$ 时，有 $f''(x)f(x)\leq f'(x)^2$。

<!-- pdf-page: 138 -->

**3.55 对数凹概率密度的累积分布函数的对数凹性。** 将习题 3.54 的结果推广到对数凹概率密度。设 $g(t)=\exp(-h(t))$ 是一个可微的对数凹概率密度，其累积分布函数为

$$
f(x)=\int_{-\infty}^x g(t)\,dt=\int_{-\infty}^x e^{-h(t)}\,dt.
$$

证明 $f$ 是对数凹的，也就是说，对所有 $x$ 都有 $f''(x)f(x)\leq f'(x)^2$。

- (a) 用 $h$ 表示 $f$ 的一阶和二阶导数，并验证：当 $h'(x)\geq0$ 时，有 $f''(x)f(x)\leq f'(x)^2$。
- (b) 现在假设 $h'(x)<0$。利用不等式

    $$
    h(t)\geq h(x)+h'(x)(t-x)
    $$

    （该不等式由 $h$ 的凸性得到），证明

    $$
    \int_{-\infty}^x e^{-h(t)}\,dt\leq\frac{e^{-h(x)}}{-h'(x)}.
    $$

    利用这一结论，验证：当 $h'(x)<0$ 时，有 $f''(x)f(x)\leq f'(x)^2$。

**3.56 更多对数凹密度。** 证明下列概率密度是对数凹的。

- (a) [MO79, 第 493 页] Gamma 密度

    $$
    f(x)=\frac{\alpha^\lambda}{\Gamma(\lambda)}x^{\lambda-1}e^{-\alpha x},
    $$

    其中 $\operatorname{dom}f=\mathbf{R}_+$，$\lambda\geq1$，$\alpha>0$。

- (b) [MO79, 第 306 页] Dirichlet 密度

    $$
    f(x)=\frac{\Gamma(\mathbf{1}^T\lambda)}{\Gamma(\lambda_1)\cdots\Gamma(\lambda_{n+1})}x_1^{\lambda_1-1}\cdots x_n^{\lambda_n-1}\left(1-\sum_{i=1}^n x_i\right)^{\lambda_{n+1}-1},
    $$

    其中 $\operatorname{dom}f=\{x\in\mathbf{R}_{++}^n\mid\mathbf{1}^Tx<1\}$，参数为 $\lambda\succeq\mathbf{1}$。

### 关于广义不等式的凸性

**3.57** 证明：$f(X)=X^{-1}$ 在 $\mathbf{S}_{++}^n$ 上是矩阵凸的。

**3.58 Schur 补。** 设 $X\in\mathbf{S}^n$，并将其分块为

$$
X=\begin{bmatrix}A&B\\B^T&C\end{bmatrix},
$$

其中 $A\in\mathbf{S}^k$。$X$ 关于 $A$ 的 Schur 补为 $S=C-B^TA^{-1}B$（见第 A.5.5 节）。证明：把 Schur 补看作从 $\mathbf{S}^n$ 到 $\mathbf{S}^{n-k}$ 的函数时，它在 $\mathbf{S}_{++}^n$ 上是矩阵凹的。

**3.59 $K$-凸性的二阶条件。** 设 $K\subseteq\mathbf{R}^m$ 是正常凸锥，其对应的广义不等式为 $\preceq_K$。证明：对于定义域为凸集的二次可微函数 $f:\mathbf{R}^n\to\mathbf{R}^m$，$f$ 是 $K$-凸函数，当且仅当对所有 $x\in\operatorname{dom}f$ 和 $y\in\mathbf{R}^n$，都有

$$
\sum_{i,j=1}^n\frac{\partial^2 f(x)}{\partial x_i\partial x_j}y_i y_j\succeq_K0.
$$

也就是说，二阶导数是一个 $K$-非负双线性型。（这里 $\partial^2 f(x)/\partial x_i\partial x_j\in\mathbf{R}^m$，其各分量为 $\partial^2f_k(x)/\partial x_i\partial x_j$，$k=1,\ldots,m$；见第 A.4.1 节。）

<!-- pdf-page: 139 -->

**3.60 $K$-凸函数的下水平集与上图。** 设 $K\subseteq\mathbf{R}^m$ 是正常凸锥，其对应的广义不等式为 $\preceq_K$，并设 $f:\mathbf{R}^n\to\mathbf{R}^m$。对于 $\alpha\in\mathbf{R}^m$，$f$（关于广义不等式 $\preceq_K$）的 $\alpha$-下水平集定义为

$$
C_\alpha=\{x\in\mathbf{R}^n\mid f(x)\preceq_K\alpha\}.
$$

$f$（关于广义不等式 $\preceq_K$）的上图定义为

$$
\operatorname{epi}_K f=\{(x,t)\in\mathbf{R}^{n+m}\mid f(x)\preceq_K t\}.
$$

证明以下各项。

- (a) 如果 $f$ 是 $K$-凸函数，那么对所有 $\alpha\in\mathbf{R}^m$，$C_\alpha$ 都是凸集。
- (b) $f$ 是 $K$-凸函数，当且仅当 $\operatorname{epi}_K f$ 是凸集。

<!-- pdf-page: 140 -->
