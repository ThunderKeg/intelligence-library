**4.27 用 SOCP 求解矩阵分式最小化问题。** 将下面的问题表示为一个 SOCP：

$$
\begin{array}{ll}
\text{最小化} & (Ax+b)^T(I+B\operatorname{diag}(x)B^T)^{-1}(Ax+b)\\
\text{约束条件} & x\succeq0,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$B\in\mathbf{R}^{m\times n}$。变量为 $x\in\mathbf{R}^n$。

**提示：** 先证明该问题等价于

$$
\begin{array}{ll}
\text{最小化} & v^Tv+w^T\operatorname{diag}(x)^{-1}w\\
\text{约束条件} & v+Bw=Ax+b\\
& x\succeq0,
\end{array}
$$

其中变量为 $v\in\mathbf{R}^m$、$w,x\in\mathbf{R}^n$。（如果 $x_i=0$，则在 $w_i=0$ 时将 $w_i^2/x_i$ 解释为零，否则解释为 $\infty$。）然后利用习题 4.26 的结果。

**4.28 鲁棒二次规划。** 在 §4.4.2 中，我们讨论了鲁棒线性规划，将其作为二阶锥规划的一个应用。本题考虑下面这个（凸）二次规划的类似鲁棒形式：

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r\\
\text{约束条件} & Ax\preceq b.
\end{array}
$$

为简单起见，假设只有矩阵 $P$ 存在误差，其余参数 $(q,r,A,b)$ 都准确已知。鲁棒二次规划定义为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sup_{P\in\mathcal{E}}\bigl((1/2)x^TPx+q^Tx+r\bigr)\\
\text{约束条件} & Ax\preceq b,
\end{array}
$$

其中 $\mathcal{E}$ 是所有可能矩阵 $P$ 构成的集合。

对于下面每一个集合 $\mathcal{E}$，将鲁棒 QP 表示为一个凸问题。表述应尽量具体。如果能把问题表示为某种标准形式（例如 QP、QCQP、SOCP、SDP），请指出这一点。

- (a) 有限个矩阵构成的集合：$\mathcal{E}=\{P_1,\ldots,P_K\}$，其中 $P_i\in\mathbf{S}_+^n$，$i=1,\ldots,K$。

- (b) 由名义值 $P_0\in\mathbf{S}_+^n$ 和偏差 $P-P_0$ 的特征值界给出的集合：

    $$
    \mathcal{E}=\{P\in\mathbf{S}^n\mid-\gamma I\preceq P-P_0\preceq\gamma I\},
    $$

    其中 $\gamma\in\mathbf{R}$，$P_0\in\mathbf{S}_{++}^n$。

- (c) 矩阵椭球：

    $$
    \mathcal{E}=\left\{P_0+\sum_{i=1}^K P_i u_i\;\middle|\;\|u\|_2\leq1\right\}.
    $$

    可以假设 $P_i\in\mathbf{S}_+^n$，$i=0,\ldots,K$。

<!-- pdf-page: 213 -->

**4.29 最大化满足线性不等式的概率。** 设 $c$ 是 $\mathbf{R}^n$ 中的随机向量，服从均值为 $\bar c$、协方差矩阵为 $R$ 的正态分布。考虑问题

$$
\begin{array}{ll}
\text{最大化} & \operatorname{prob}(c^Tx\geq\alpha)\\
\text{约束条件} & Fx\succeq g,\quad Ax=b.
\end{array}
$$

假设存在一个可行点 $\tilde x$，使得 $\bar c^T\tilde x\geq\alpha$。证明该问题等价于一个凸优化问题或拟凸优化问题。如果该问题是凸的，将其写成 QP、QCQP 或 SOCP；如果该问题是拟凸的，说明如何通过求解一系列 QP、QCQP 或 SOCP 可行性问题来求解它。

### 几何规划

**4.30** 温度为 $T$（比环境温度高出的度数）的热流体，在一根长度固定、横截面为半径 $r$ 的圆形管道中流动。管道外包裹一层厚度为 $w\ll r$ 的保温材料，以减少穿过管壁的热损失。本问题中的设计变量为 $T$、$r$ 和 $w$。

热损失（近似）正比于 $Tr/w$，因此，在固定的使用寿命内，由热损失造成的能源成本为 $\alpha_1Tr/w$。管道的壁厚固定，其成本近似正比于管道材料总量，即为 $\alpha_2r$。保温层的成本同样近似正比于保温材料总量，即为 $\alpha_3rw$（这里利用了 $w\ll r$）。总成本是这三项成本之和。

沿管道输送的热流完全来自流体的流动，流体的速度固定，因此热流为 $\alpha_4Tr^2$。常数 $\alpha_i$ 均为正，变量 $T$、$r$ 和 $w$ 也均为正。

现在的问题是：在总成本不超过上限 $C_{\max}$，并满足约束

$$
T_{\min}\leq T\leq T_{\max},\qquad
r_{\min}\leq r\leq r_{\max},\qquad
w_{\min}\leq w\leq w_{\max},\qquad
w\leq0.1r
$$

的条件下，最大化沿管道输送的总热流。将该问题表示为一个几何规划。

**4.31 最优梁设计问题的递推形式。** 证明 GP (4.46) 等价于下面的 GP：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^N w_i h_i\\
\text{约束条件} & w_i/w_{\max}\leq1,\quad w_{\min}/w_i\leq1,\quad i=1,\ldots,N\\
& h_i/h_{\max}\leq1,\quad h_{\min}/h_i\leq1,\quad i=1,\ldots,N\\
& h_i/(w_iS_{\max})\leq1,\quad S_{\min}w_i/h_i\leq1,\quad i=1,\ldots,N\\
& 6iF/(\sigma_{\max}w_i h_i^2)\leq1,\quad i=1,\ldots,N\\
& (2i-1)d_i/v_i+v_{i+1}/v_i\leq1,\quad i=1,\ldots,N\\
& (i-1/3)d_i/y_i+v_{i+1}/y_i+y_{i+1}/y_i\leq1,\quad i=1,\ldots,N\\
& y_1/y_{\max}\leq1\\
& Ew_i h_i^3d_i/(6F)=1,\quad i=1,\ldots,N.
\end{array}
$$

变量为 $w_i,h_i,v_i,d_i,y_i$，$i=1,\ldots,N$。

**4.32 用单项式逼近函数。** 假设函数 $f:\mathbf{R}^n\to\mathbf{R}$ 在点 $x_0\succ0$ 处可微，且 $f(x_0)>0$。如何找到一个单项式函数 $\widehat f:\mathbf{R}^n\to\mathbf{R}$，使得 $f(x_0)=\widehat f(x_0)$，并且当 $x$ 接近 $x_0$ 时，$\widehat f(x)$ 非常接近 $f(x)$？

**4.33** 将下列问题表示为凸优化问题。

- (a) 最小化 $\max\{p(x),q(x)\}$，其中 $p$ 和 $q$ 是正项式。

- (b) 最小化 $\exp(p(x))+\exp(q(x))$，其中 $p$ 和 $q$ 是正项式。

- (c) 在约束 $r(x)>q(x)$ 下最小化 $p(x)/(r(x)-q(x))$，其中 $p$、$q$ 是正项式，$r$ 是单项式。

<!-- pdf-page: 214 -->

**4.34 Perron–Frobenius 特征值的对数凸性。** 设 $A\in\mathbf{R}^{n\times n}$ 是一个逐元素为正的矩阵，即 $A_{ij}>0$。（本题的结果也适用于不可约的非负矩阵。）用 $\lambda_{\mathrm{pf}}(A)$ 表示其 Perron–Frobenius 特征值，即模最大的特征值。（定义和例子见第 165 页。）证明 $\log\lambda_{\mathrm{pf}}(A)$ 是 $\log A_{ij}$ 的凸函数。例如，这意味着有不等式

$$
\lambda_{\mathrm{pf}}(C)\leq\bigl(\lambda_{\mathrm{pf}}(A)\lambda_{\mathrm{pf}}(B)\bigr)^{1/2},
$$

其中 $C_{ij}=(A_{ij}B_{ij})^{1/2}$，$A$、$B$ 均为逐元素为正的矩阵。

**提示：** 使用 (4.47) 给出的 Perron–Frobenius 特征值刻画，或者使用下面的刻画：

$$
\log\lambda_{\mathrm{pf}}(A)=\lim_{k\to\infty}(1/k)\log(\mathbf{1}^TA^k\mathbf{1}).
$$

**4.35 Signomial 规划与几何规划。** **Signomial** 是关于正变量 $x_1,\ldots,x_n$ 的单项式的线性组合。Signomial 比正项式更一般；正项式就是所有系数均为正的 signomial。**Signomial 规划**是形如

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
$$

的优化问题，其中 $f_0,\ldots,f_m$ 和 $h_1,\ldots,h_p$ 都是 signomial。一般来说，signomial 规划非常难以求解。

有些 signomial 规划可以转化为 GP，从而能够高效求解。对于具有下列形式的 signomial 规划，说明如何进行这种转化：

- 目标 signomial $f_0$ 是正项式，即它的各项都只有正系数。
- 每个不等式约束 signomial $f_1,\ldots,f_m$ 都恰好有一个负系数项：$f_i=p_i-q_i$，其中 $p_i$ 是正项式，$q_i$ 是单项式。
- 每个等式约束 signomial $h_1,\ldots,h_p$ 都恰好有一个正系数项和一个负系数项：$h_i=r_i-s_i$，其中 $r_i$、$s_i$ 都是单项式。

**4.36** 说明如何将一般 GP 改写为一个等价的 GP，使得其中的每个正项式（包括目标和约束中的正项式）都至多含有两个单项式项。**提示：** 将每个（单项式的）和表示为若干个和的和，每个和都只有两项。

**4.37 广义正项式与几何规划。** 设 $x_1,\ldots,x_n$ 为正变量，函数 $f_i:\mathbf{R}^n\to\mathbf{R}$，$i=1,\ldots,k$，都是关于 $x_1,\ldots,x_n$ 的正项式。如果 $\phi:\mathbf{R}^k\to\mathbf{R}$ 是一个系数非负的多项式，那么复合函数

$$
h(x)=\phi(f_1(x),\ldots,f_k(x))
\tag{4.69}
$$

也是正项式，因为正项式对乘积、求和以及与非负标量相乘这些运算封闭。例如，设 $f_1$ 和 $f_2$ 是正项式，并考虑多项式 $\phi(z_1,z_2)=3z_1^2z_2+2z_1+3z_2^3$（其系数非负）。那么 $h=3f_1^2f_2+2f_1+f_2^3$ 是一个正项式。

本题考虑这一想法的一种推广：允许 $\phi$ 是正项式，即可以含有分数指数。具体来说，假设 $\phi:\mathbf{R}^k\to\mathbf{R}$ 是一个所有指数均非负的正项式。在这种情况下，将 (4.69) 定义的函数 $h$ 称为**广义正项式**（generalized posynomial）。例如，设 $f_1$、$f_2$ 为正项式，并考虑指数非负的正项式 $\phi(z_1,z_2)=2z_1^{0.3}z_2^{1.2}+z_1z_2^{0.5}+2$。那么函数

$$
h(x)=2f_1(x)^{0.3}f_2(x)^{1.2}+f_1(x)f_2(x)^{0.5}+2
$$

<!-- pdf-page: 215 -->

是一个广义正项式。不过请注意，它并不是正项式（除非 $f_1$、$f_2$ 是单项式或常数）。

**广义几何规划**（generalized geometric program，GGP）是形如

$$
\begin{array}{ll}
\text{最小化} & h_0(x)\\
\text{约束条件} & h_i(x)\leq1,\quad i=1,\ldots,m\\
& g_i(x)=1,\quad i=1,\ldots,p,
\end{array}
\tag{4.70}
$$

的优化问题，其中 $g_1,\ldots,g_p$ 是单项式，$h_0,\ldots,h_m$ 是广义正项式。

说明如何将这个广义几何规划表示为一个等价的几何规划。解释你引入的所有新变量，并说明所得 GP 为什么与 GGP (4.70) 等价。

### 半正定规划与锥形式问题

**4.38 只有一个变量的 LMI 与 SDP。** 矩阵对 $(A,B)$（其中 $A,B\in\mathbf{S}^n$）的**广义特征值**定义为多项式 $\det(\lambda B-A)$ 的根（见 §A.5.3）。假设 $B$ 非奇异，而且 $A$、$B$ 可以通过合同变换同时对角化，即存在非奇异矩阵 $R\in\mathbf{R}^{n\times n}$，使得

$$
R^TAR=\operatorname{diag}(a),\qquad R^TBR=\operatorname{diag}(b),
$$

其中 $a,b\in\mathbf{R}^n$。（满足这一条件的一个充分条件是存在 $t_1,t_2$，使得 $t_1A+t_2B\succ0$。）

- (a) 证明 $(A,B)$ 的广义特征值都是实数，并且为 $\lambda_i=a_i/b_i$，$i=1,\ldots,n$。

- (b) 用 $a$ 和 $b$ 表示 SDP

    $$
    \begin{array}{ll}
    \text{最小化} & ct\\
    \text{约束条件} & tB\preceq A,
    \end{array}
    $$

    的解，其中变量为 $t\in\mathbf{R}$。

**4.39 SDP 与合同变换。** 考虑 SDP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & x_1F_1+x_2F_2+\cdots+x_nF_n+G\preceq0,
\end{array}
$$

其中 $F_i,G\in\mathbf{S}^k$，$c\in\mathbf{R}^n$。

- (a) 假设 $R\in\mathbf{R}^{k\times k}$ 非奇异。证明该 SDP 等价于下面的 SDP：

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & x_1\widetilde F_1+x_2\widetilde F_2+\cdots+x_n\widetilde F_n+\widetilde G\preceq0,
    \end{array}
    $$

    其中 $\widetilde F_i=R^TF_iR$，$\widetilde G=R^TGR$。

- (b) 假设存在非奇异矩阵 $R$，使得 $\widetilde F_i$ 和 $\widetilde G$ 都是对角矩阵。证明该 SDP 等价于一个 LP。

- (c) 假设存在非奇异矩阵 $R$，使得 $\widetilde F_i$ 和 $\widetilde G$ 具有如下形式：

    $$
    \widetilde F_i=
    \begin{bmatrix}
    \alpha_i I & a_i\\
    a_i^T & \alpha_i
    \end{bmatrix},\quad i=1,\ldots,n,\qquad
    \widetilde G=
    \begin{bmatrix}
    \beta I & b\\
    b^T & \beta
    \end{bmatrix},
    $$

    其中 $\alpha_i,\beta\in\mathbf{R}$，$a_i,b\in\mathbf{R}^{k-1}$。证明该 SDP 等价于一个只有单个二阶锥约束的 SOCP。

<!-- pdf-page: 216 -->

**4.40 将 LP、QP、QCQP 和 SOCP 表示为 SDP。** 将下列问题表示为 SDP。

- (a) LP (4.27)。

- (b) QP (4.34)、QCQP (4.35) 和 SOCP (4.36)。**提示：** 假设 $A\in\mathbf{S}_{++}^r$、$C\in\mathbf{S}^s$、$B\in\mathbf{R}^{r\times s}$。则

    $$
    \begin{bmatrix}
    A & B\\
    B^T & C
    \end{bmatrix}\succeq0
    \quad\Longleftrightarrow\quad
    C-B^TA^{-1}B\succeq0.
    $$

    更完整的表述（也适用于奇异矩阵 $A$）及其证明见 §A.5.5。

- (c) 矩阵分式优化问题

    $$
    \text{最小化}\quad (Ax+b)^TF(x)^{-1}(Ax+b),
    $$

    其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，

    $$
    F(x)=F_0+x_1F_1+\cdots+x_nF_n,
    $$

    $F_i\in\mathbf{S}^m$。目标函数的定义域取为 $\{x\mid F(x)\succ0\}$。可以假设该问题可行，即至少存在一个 $x$ 使得 $F(x)\succ0$。

**4.41 共正矩阵与 $P_0$ 矩阵的 LMI 检验。** 如果矩阵 $A\in\mathbf{S}^n$ 对所有 $x\succeq0$ 都满足 $x^TAx\geq0$，就称 $A$ 是共正矩阵（见习题 2.35）。如果矩阵 $A\in\mathbf{R}^{n\times n}$ 对所有 $x$ 都满足 $\max_{i=1,\ldots,n}x_i(Ax)_i\geq0$，就称 $A$ 是 $P_0$ 矩阵。一般来说，检验一个矩阵是否为共正矩阵或 $P_0$ 矩阵非常困难。不过，存在一些有用的充分条件，可以通过半正定规划加以检验。

- (a) 证明：如果 $A$ 可以分解为一个半正定矩阵与一个逐元素非负矩阵之和，那么 $A$ 是共正矩阵：

    $$
    A=B+C,\qquad B\succeq0,\qquad C_{ij}\geq0,\quad i,j=1,\ldots,n.
    \tag{4.71}
    $$

    将寻找满足 (4.71) 的 $B$ 和 $C$ 的问题表示为一个 SDP 可行性问题。

- (b) 证明：如果存在一个正对角矩阵 $D$，使得

    $$
    DA+A^TD\succeq0,
    \tag{4.72}
    $$

    那么 $A$ 是 $P_0$ 矩阵。将寻找满足 (4.72) 的 $D$ 的问题表示为一个 SDP 可行性问题。

**4.42 复 LMI 与复 SDP。** 复 LMI 具有如下形式：

$$
x_1F_1+\cdots+x_nF_n+G\preceq0,
$$

其中 $F_1,\ldots,F_n,G$ 是复 $n\times n$ Hermitian 矩阵，即 $F_i^H=F_i$、$G^H=G$，而 $x\in\mathbf{R}^n$ 是实变量。复 SDP 是在一个复 LMI 约束下，最小化 $x$ 的某个（实）线性函数的问题。

利用下面的事实，可以将复 LMI 和复 SDP 转化为实 LMI 和实 SDP：

$$
X\succeq0
\quad\Longleftrightarrow\quad
\begin{bmatrix}
\Re X & -\Im X\\
\Im X & \Re X
\end{bmatrix}\succeq0,
$$

其中 $\Re X\in\mathbf{R}^{n\times n}$ 是复 Hermitian 矩阵 $X$ 的实部，$\Im X\in\mathbf{R}^{n\times n}$ 是 $X$ 的虚部。

验证这一结果，并说明如何将复 SDP 写成实 SDP。

<!-- pdf-page: 217 -->

**4.43 通过 SDP 进行特征值优化。** 假设 $A:\mathbf{R}^n\to\mathbf{S}^m$ 是仿射映射，即

$$
A(x)=A_0+x_1A_1+\cdots+x_nA_n,
$$

其中 $A_i\in\mathbf{S}^m$。用 $\lambda_1(x)\geq\lambda_2(x)\geq\cdots\geq\lambda_m(x)$ 表示 $A(x)$ 的特征值。说明如何将下列问题写成 SDP。

- (a) 最小化最大特征值 $\lambda_1(x)$。

- (b) 最小化特征值的跨度 $\lambda_1(x)-\lambda_m(x)$。

- (c) 在约束 $A(x)\succ0$ 下，最小化 $A(x)$ 的条件数。条件数定义为 $\kappa(A(x))=\lambda_1(x)/\lambda_m(x)$，定义域为 $\{x\mid A(x)\succ0\}$。可以假设至少存在一个 $x$ 使得 $A(x)\succ0$。

    **提示：** 需要在约束

    $$
    0\prec\gamma I\preceq A(x)\preceq\lambda I
    $$

    下最小化 $\lambda/\gamma$。进行变量代换 $y=x/\gamma$、$t=\lambda/\gamma$、$s=1/\gamma$。

- (d) 最小化特征值绝对值之和 $|\lambda_1(x)|+\cdots+|\lambda_m(x)|$。

    **提示：** 将 $A(x)$ 表示为 $A(x)=A_+-A_-$，其中 $A_+\succeq0$、$A_-\succeq0$。

**4.44 多项式上的优化。** 将下列问题写成 SDP。寻找多项式 $p:\mathbf{R}\to\mathbf{R}$，

$$
p(t)=x_1+x_2t+\cdots+x_{2k+1}t^{2k},
$$

使其在 $m$ 个指定点 $t_i$ 处满足给定界 $l_i\leq p(t_i)\leq u_i$，并且在所有满足这些界的多项式中，它的最小值最大：

$$
\begin{array}{ll}
\text{最大化} & \inf_t p(t)\\
\text{约束条件} & l_i\leq p(t_i)\leq u_i,\quad i=1,\ldots,m.
\end{array}
$$

变量为 $x\in\mathbf{R}^{2k+1}$。

**提示：** 使用习题 2.37(b) 中推导出的非负多项式的 LMI 刻画。

**4.45** [Nes00, Par00] **通过 LMI 表示平方和。** 考虑一个次数为 $2k$ 的多项式 $p:\mathbf{R}^n\to\mathbf{R}$。如果对所有 $x\in\mathbf{R}^n$ 都有 $p(x)\geq0$，就称多项式 $p$ 是半正定的（positive semidefinite，PSD）。除了一些特殊情形（例如 $n=1$ 或 $k=1$），判断给定多项式是否为 PSD 极其困难，更不用说在约束 $p$ 为 PSD 的条件下，以 $p$ 的系数为变量求解优化问题了。

多项式为 PSD 的一个著名充分条件是它具有如下形式：

$$
p(x)=\sum_{i=1}^r q_i(x)^2,
$$

其中 $q_i$ 是次数不超过 $k$ 的多项式。具有这种平方和形式的多项式称为 SOS 多项式。

多项式 $p$ 为 SOS 这一条件（将其看作对 $p$ 的系数的约束）实际上等价于一个 LMI，因此，许多带有 SOS 约束的优化问题都可以写成 SDP。本题将引导你研究这些想法。

- (a) 设 $f_1,\ldots,f_s$ 是次数不超过 $k$ 的所有单项式。（这里的单项式采用通常的含义，即 $x_1^{m_1}\cdots x_n^{m_n}$，其中 $m_i\in\mathbf{Z}_+$，而不是几何规划中的含义。）证明：如果 $p$ 能表示为半正定二次型 $p=f^TVf$，其中 $V\in\mathbf{S}_+^s$，那么 $p$ 是 SOS 多项式。反过来，证明：如果 $p$ 是 SOS 多项式，那么它就能表示为这些单项式的半正定二次型，即存在某个 $V\in\mathbf{S}_+^s$，使得 $p=f^TVf$。

<!-- pdf-page: 218 -->

- (b) 证明条件 $p=f^TVf$ 是一组联系 $p$ 的系数与矩阵 $V$ 的线性等式约束。结合上面的 (a)，这说明：$p$ 为 SOS 多项式这一条件，等价于一组联系 $V$ 和 $p$ 的系数的线性等式，以及矩阵不等式 $V\succeq0$。

- (c) 对于 $p$ 是二变量四次多项式的情形，明确写出它为 SOS 多项式的 LMI 条件。

**4.46 多维矩。** $\mathbf{R}^2$ 上随机变量 $t$ 的矩定义为 $\mu_{ij}=\mathbf{E}t_1^it_2^j$，其中 $i,j$ 是非负整数。本题将推导一组数 $\mu_{ij}$，$0\leq i,j\leq2k$、$i+j\leq2k$，成为 $\mathbf{R}^2$ 上某个分布的矩所必须满足的条件。

设 $p:\mathbf{R}^2\to\mathbf{R}$ 是一个次数为 $k$、系数为 $c_{ij}$ 的多项式，

$$
p(t)=\sum_{i=0}^k\sum_{j=0}^{k-i}c_{ij}t_1^it_2^j,
$$

并设 $t$ 是矩为 $\mu_{ij}$ 的随机变量。假设 $c\in\mathbf{R}^{(k+1)(k+2)/2}$ 按某种指定顺序包含系数 $c_{ij}$，而 $\mu\in\mathbf{R}^{(k+1)(2k+1)}$ 按相同顺序包含矩 $\mu_{ij}$。证明 $\mathbf{E}p(t)^2$ 可以表示为关于 $c$ 的二次型：

$$
\mathbf{E}p(t)^2=c^TH(\mu)c,
$$

其中 $H:\mathbf{R}^{(k+1)(2k+1)}\to\mathbf{S}^{(k+1)(k+2)/2}$ 是 $\mu$ 的线性函数。由此得出，$\mu$ 必须满足 LMI $H(\mu)\succeq0$。

**注：** 对于 $\mathbf{R}$ 上的随机变量，矩阵 $H$ 可以取为 (4.52) 定义的 Hankel 矩阵。在这种情况下，$H(\mu)\succeq0$ 是 $\mu$ 为某个分布的矩、或为某个矩序列的极限的充要条件。但在 $\mathbf{R}^2$ 上，该 LMI 只是必要条件。

**4.47 最大行列式半正定矩阵补全。** 考虑矩阵 $A\in\mathbf{S}^n$，其中一些元素已指定，另一些元素未指定。**半正定矩阵补全问题**是确定矩阵中未指定元素的取值，使得 $A\succeq0$（或者确定不存在这样的补全）。

- (a) 解释为什么可以不失一般性地假设 $A$ 的对角元素都已指定。

- (b) 说明如何将半正定补全问题写成一个 SDP 可行性问题。

- (c) 假设 $A$ 至少有一个正定补全，而且 $A$ 的对角元素都已指定（即固定）。行列式最大的正定补全称为**最大行列式补全**。证明最大行列式补全是唯一的。证明：如果 $A^\star$ 是最大行列式补全，那么 $(A^\star)^{-1}$ 在原矩阵所有未指定元素的位置上都为零。**提示：** 函数 $f(X)=\log\det X$ 的梯度为 $\nabla f(X)=X^{-1}$（见 §A.4.1）。

- (d) 假设 $A$ 的三对角部分已指定，即给定了 $A_{11},\ldots,A_{nn}$ 和 $A_{12},\ldots,A_{n-1,n}$。证明：如果 $A$ 存在正定补全，那么它就存在一个逆矩阵为三对角矩阵的正定补全。

**4.48 广义特征值最小化。** 回忆一下（见例 3.37 或 §A.5.3），矩阵对 $(A,B)\in\mathbf{S}^k\times\mathbf{S}_{++}^k$ 的最大广义特征值为

$$
\lambda_{\max}(A,B)=\sup_{u\ne0}\frac{u^TAu}{u^TBu}
=\max\{\lambda\mid\det(\lambda B-A)=0\}.
$$

我们已经知道，如果以 $\mathbf{S}^k\times\mathbf{S}_{++}^k$ 为定义域，这个函数是拟凸的。

<!-- pdf-page: 219 -->

考虑问题

$$
\text{最小化}\quad\lambda_{\max}(A(x),B(x)),
\tag{4.73}
$$

其中 $A,B:\mathbf{R}^n\to\mathbf{S}^k$ 是仿射函数，定义为

$$
A(x)=A_0+x_1A_1+\cdots+x_nA_n,\qquad
B(x)=B_0+x_1B_1+\cdots+x_nB_n,
$$

其中 $A_i,B_i\in\mathbf{S}^k$。

- (a) 给出一族凸函数 $\phi_t:\mathbf{S}^k\times\mathbf{S}^k\to\mathbf{R}$，使得对所有 $(A,B)\in\mathbf{S}^k\times\mathbf{S}_{++}^k$ 都有

    $$
    \lambda_{\max}(A,B)\leq t
    \quad\Longleftrightarrow\quad
    \phi_t(A,B)\leq0.
    $$

    说明利用这一点，可以通过求解一系列凸可行性问题来求解 (4.73)。

- (b) 给出一族矩阵凸函数 $\Phi_t:\mathbf{S}^k\times\mathbf{S}^k\to\mathbf{S}^k$，使得对所有 $(A,B)\in\mathbf{S}^k\times\mathbf{S}_{++}^k$ 都有

    $$
    \lambda_{\max}(A,B)\leq t
    \quad\Longleftrightarrow\quad
    \Phi_t(A,B)\preceq0.
    $$

    说明利用这一点，可以通过求解一系列带 LMI 约束的凸可行性问题来求解 (4.73)。

- (c) 假设 $B(x)=(a^Tx+b)I$，其中 $a\ne0$。证明 (4.73) 等价于下面的凸问题：

    $$
    \begin{array}{ll}
    \text{最小化} & \lambda_{\max}(sA_0+y_1A_1+\cdots+y_nA_n)\\
    \text{约束条件} & a^Ty+bs=1\\
    & s\geq0,
    \end{array}
    $$

    其中变量为 $y\in\mathbf{R}^n$、$s\in\mathbf{R}$。

**4.49 广义分式规划。** 设 $K\in\mathbf{R}^m$ 是一个正常锥。证明由

$$
f_0(x)=\inf\{t\mid Cx+d\preceq_K t(Fx+g)\},\qquad
\operatorname{dom}f_0=\{x\mid Fx+g\succ_K0\},
$$

定义的函数 $f_0:\mathbf{R}^n\to\mathbf{R}^m$ 是拟凸的，其中 $C,F\in\mathbf{R}^{m\times n}$，$d,g\in\mathbf{R}^m$。

以这种形式的函数为目标的拟凸优化问题称为**广义分式规划**（generalized fractional program）。将第 152 页的广义线性分式规划，以及广义特征值最小化问题 (4.73)，表示为广义分式规划。

### 向量优化与多准则优化

**4.50 双准则优化。** 图 4.11 给出了双准则优化问题

$$
\text{最小化（关于 }\mathbf{R}_+^2\text{）}\quad
\bigl(\|Ax-b\|_2^2,\|x\|_2^2\bigr),
$$

的最优权衡曲线和可达值集合，其中 $A\in\mathbf{R}^{100\times10}$，$b\in\mathbf{R}^{100}$。利用图中的信息回答下列问题。用 $x_{\mathrm{ls}}$ 表示最小二乘问题

$$
\text{最小化}\quad\|Ax-b\|_2^2
$$

的解。

- (a) $\|x_{\mathrm{ls}}\|_2$ 是多少？

- (b) $\|Ax_{\mathrm{ls}}-b\|_2$ 是多少？

- (c) $\|b\|_2$ 是多少？

<!-- pdf-page: 220 -->

- (d) 给出下面问题的最优值：

    $$
    \begin{array}{ll}
    \text{最小化} & \|Ax-b\|_2^2\\
    \text{约束条件} & \|x\|_2^2=1.
    \end{array}
    $$

- (e) 给出下面问题的最优值：

    $$
    \begin{array}{ll}
    \text{最小化} & \|Ax-b\|_2^2\\
    \text{约束条件} & \|x\|_2^2\leq1.
    \end{array}
    $$

- (f) 给出下面问题的最优值：

    $$
    \text{最小化}\quad\|Ax-b\|_2^2+\|x\|_2^2.
    $$

- (g) $A$ 的秩是多少？
