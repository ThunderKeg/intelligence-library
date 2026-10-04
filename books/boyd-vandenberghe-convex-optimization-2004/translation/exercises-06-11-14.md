**6.11 最小二乘方向插值。** 设 $F_1,\ldots,F_n:\mathbf{R}^k\to\mathbf{R}^p$，将它们作线性组合，得到 $F:\mathbf{R}^k\to\mathbf{R}^p$，

$$
F(u)=x_1F_1(u)+\cdots+x_nF_n(u),
$$

其中 $x$ 是插值问题的变量。

在这个问题中，我们要求 $\angle(F(v_j),q_j)=0$，$j=1,\ldots,m$，其中 $q_j$ 是给定的 $\mathbf{R}^p$ 中的向量，并假设满足 $\|q_j\|_2=1$。换言之，要求 $F$ 在各点 $v_j$ 处的方向取指定的值。为了确保 $F(v_j)$ 不为零（否则夹角没有定义），还施加最小长度约束 $\|F(v_j)\|_2\geq\epsilon$，$j=1,\ldots,m$，其中 $\epsilon>0$ 是给定的。

说明如何用凸优化求出使 $\|x\|^2$ 最小、并满足上述方向条件（及最小长度条件）的 $x$。

**6.12 用单调函数插值。** 如果只要 $u\succeq v$ 就有 $f(u)\geq f(v)$，就称函数 $f:\mathbf{R}^k\to\mathbf{R}$（关于 $\mathbf{R}_+^k$）单调不减。

<!-- pdf-page: 362 -->

- (a) 证明：存在单调不减函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当

    $$
    y_i\geq y_j\quad\text{只要 }u_i\succeq u_j,\qquad i,j=1,\ldots,m.
    $$

- (b) 证明：存在定义域为 $\operatorname{dom}f=\mathbf{R}^k$ 的凸且单调不减的函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当存在 $g_i\in\mathbf{R}^k$，$i=1,\ldots,m$，使得

    $$
    g_i\succeq0,\quad i=1,\ldots,m,\qquad
    y_j\geq y_i+g_i^T(u_j-u_i),\quad i,j=1,\ldots,m.
    $$

**6.13 用拟凸函数插值。** 证明：存在拟凸函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当存在 $g_i\in\mathbf{R}^k$，$i=1,\ldots,m$，使得

$$
g_i^T(u_j-u_i)\leq-1\quad\text{只要 }y_j<y_i,\qquad i,j=1,\ldots,m.
$$

**6.14 [Nes00] 用正实函数插值。** 设 $z_1,\ldots,z_n\in\mathbf{C}$ 是 $n$ 个互不相同的点，且 $|z_i|>1$。将 $K_{\mathrm{np}}$ 定义为所有满足如下条件的向量 $y\in\mathbf{C}^n$ 构成的集合：存在函数 $f:\mathbf{C}\to\mathbf{C}$，使得以下条件成立。

- $f$ 是**正实函数（positive-real function）**，也就是说，它在单位圆外（即 $|z|>1$）解析，且在单位圆外实部非负（$|z|>1$ 时 $\Re f(z)\geq0$）。

- $f$ 满足插值条件

    $$
    f(z_1)=y_1,\qquad f(z_2)=y_2,\qquad\ldots,\qquad f(z_n)=y_n.
    $$

若用 $\mathcal{F}$ 表示正实函数的集合，就可以将 $K_{\mathrm{np}}$ 写为

$$
K_{\mathrm{np}}=\{y\in\mathbf{C}^n\mid\exists f\in\mathcal{F},\ y_k=f(z_k),\ k=1,\ldots,n\}.
$$

- (a) 可以证明，$f$ 为正实函数，当且仅当存在一个不减函数 $\rho$，使得对所有满足 $|z|>1$ 的 $z$，都有

    $$
    f(z)=i\Im f(\infty)+\int_0^{2\pi}\frac{e^{i\theta}+z^{-1}}{e^{i\theta}-z^{-1}}\,d\rho(\theta),
    $$

    其中 $i=\sqrt{-1}$（见 [KN77，第 389 页]）。利用这种表示证明 $K_{\mathrm{np}}$ 是闭凸锥。

- (b) 对于向量 $x,y\in\mathbf{C}^n$，我们使用内积 $\Re(x^Hy)$，其中 $x^H$ 表示 $x$ 的共轭转置。证明 $K_{\mathrm{np}}$ 的对偶锥为

    $$
    K_{\mathrm{np}}^*=\left\{x\in\mathbf{C}^n\ \middle|\ \Im(\mathbf{1}^Tx)=0,\ \Re\left(\sum_{l=1}^nx_l\frac{e^{-i\theta}+\bar z_l^{-1}}{e^{-i\theta}-\bar z_l^{-1}}\right)\geq0\ \forall\theta\in[0,2\pi]\right\}.
    $$

- (c) 证明

    $$
    K_{\mathrm{np}}^*=\left\{x\in\mathbf{C}^n\ \middle|\ \exists Q\in\mathbf{H}_+^n,\ x_l=\sum_{k=1}^n\frac{Q_{kl}}{1-z_k^{-1}\bar z_l^{-1}},\ l=1,\ldots,n\right\},
    $$

    其中 $\mathbf{H}_+^n$ 表示所有 $n\times n$ 半正定 Hermitian 矩阵构成的集合。

    使用下面的结论（称为 Riesz–Fejér 定理，见 [KN77，第 60 页]）：形如

    $$
    \sum_{k=0}^n(y_ke^{-ik\theta}+\bar y_ke^{ik\theta})
    $$

    的函数对所有 $\theta$ 均非负，当且仅当存在 $a_0,\ldots,a_n\in\mathbf{C}$，使得

    $$
    \sum_{k=0}^n(y_ke^{-ik\theta}+\bar y_ke^{ik\theta})=\left|\sum_{k=0}^na_ke^{ik\theta}\right|^2.
    $$

    <!-- pdf-page: 363 -->

- (d) 证明 $K_{\mathrm{np}}=\{y\in\mathbf{C}^n\mid P(y)\succeq0\}$，其中 $P(y)\in\mathbf{H}^n$ 定义为

    $$
    P(y)_{kl}=\frac{y_k+\bar y_l}{1-z_k^{-1}\bar z_l^{-1}},\qquad l,k=1,\ldots,n.
    $$

    矩阵 $P(y)$ 称为与各点 $z_k,y_k$ 对应的 **Nevanlinna–Pick 矩阵**。

    *提示：* 如 (a) 中所述，$K_{\mathrm{np}}$ 是闭凸锥，因此 $K_{\mathrm{np}}=K_{\mathrm{np}}^{**}$。

- (e) 作为一个应用，将下面的问题表述为凸优化问题：

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{k=1}^n|f(z_k)-w_k|^2\\
    \text{约束条件} & f\in\mathcal{F}.
    \end{array}
    $$

    问题数据为满足 $|z_k|>1$ 的 $n$ 个点 $z_k$，以及 $n$ 个复数 $w_1,\ldots,w_n$。我们在所有正实函数 $f$ 中进行优化。

<!-- pdf-page: 364 -->
