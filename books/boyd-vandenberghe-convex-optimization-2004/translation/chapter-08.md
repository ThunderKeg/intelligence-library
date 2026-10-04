<!-- pdf-page: 411 -->

# 第 8 章 几何问题

<aside class="chapter-guide"><p>导读（编者）：本章把投影、集合间距离、包围与内接椭球、分类以及空间布置等几何任务写成优化问题。阅读时可以留意两个问题：怎样选择变量，使几何条件成为凸约束；对偶变量又怎样给出分离超平面或其他几何解释。最后的布置与平面布局问题展示了这些方法在设计中的用法。</p></aside>

## 8.1 在集合上的投影

在范数 $\|\cdot\|$ 下，点 $x_0\in\mathbf{R}^n$ 到闭集 $C\subseteq\mathbf{R}^n$ 的*距离*定义为

$$
\mathbf{dist}(x_0,C)=\inf\{\|x_0-x\|\mid x\in C\}.
$$

这里的下确界总能达到。我们把 $C$ 中任何一个最接近 $x_0$ 的点 $z$，即满足 $\|z-x_0\|=\mathbf{dist}(x_0,C)$ 的点，称为 $x_0$ 在 $C$ 上的一个*投影*。一般来说，$x_0$ 在 $C$ 上的投影可能不止一个，也就是说，$C$ 中可能有多个点同样最接近 $x_0$。

在一些特殊情况下，可以证明点在集合上的投影唯一。例如，若 $C$ 是闭凸集，且范数严格凸（例如欧几里得范数），那么对任意 $x_0$，总有且仅有一个 $z\in C$ 最接近 $x_0$。一个有趣的逆命题是：如果对每个 $x_0$，它在 $C$ 上的欧几里得投影都唯一，那么 $C$ 是闭凸集（见习题 8.2）。

我们用记号 $P_C:\mathbf{R}^n\to\mathbf{R}^n$ 表示任何满足以下条件的函数：$P_C(x_0)$ 是 $x_0$ 在 $C$ 上的一个投影，即对所有 $x_0$，

$$
P_C(x_0)\in C,\qquad \|x_0-P_C(x_0)\|=\mathbf{dist}(x_0,C).
$$

换句话说，

$$
P_C(x_0)=\operatorname*{argmin}\{\|x-x_0\|\mid x\in C\}.
$$

我们把 $P_C$ 称为*在 $C$ 上的投影*。

<div class="example" markdown="1">

**例 8.1 在 $\mathbf{R}^2$ 中单位正方形上的投影。** 考虑 $\mathbf{R}^2$ 中的单位正方形（的边界），即 $C=\{x\in\mathbf{R}^2\mid\|x\|_\infty=1\}$。取 $x_0=0$。

在 $\ell_1$ 范数下，四个点 $(1,0)$、$(0,-1)$、$(-1,0)$ 和 $(0,1)$ 最接近 $x_0=0$，距离为 $1$，所以在 $\ell_1$ 范数下有 $\mathbf{dist}(x_0,C)=1$。对 $\ell_2$ 范数，同样的结论也成立。

在 $\ell_\infty$ 范数下，$C$ 中所有点到 $x_0$ 的距离都为 $1$，并且 $\mathbf{dist}(x_0,C)=1$。

</div>

<!-- pdf-page: 412 -->

<div class="example" markdown="1">

**例 8.2 在秩为 $k$ 的矩阵集合上的投影。** 考虑秩小于或等于 $k$ 的 $m\times n$ 矩阵集合

$$
C=\{X\in\mathbf{R}^{m\times n}\mid\mathbf{rank}\,X\leq k\},
$$

其中 $k\leq\min\{m,n\}$，并设 $X_0\in\mathbf{R}^{m\times n}$。在范数 $\|\cdot\|_2$（谱范数或最大奇异值范数）下，可以通过奇异值分解求出 $X_0$ 在 $C$ 上的一个投影。设

$$
X_0=\sum_{i=1}^r\sigma_i u_iv_i^T
$$

是 $X_0$ 的奇异值分解，其中 $r=\mathbf{rank}\,X_0$。那么矩阵 $Y=\sum_{i=1}^{\min\{k,r\}}\sigma_i u_iv_i^T$ 就是 $X_0$ 在 $C$ 上的一个投影。

</div>

### 8.1.1 将点投影到凸集上

若 $C$ 是凸集，那么可以通过求解一个凸优化问题，计算投影 $P_C(x_0)$ 和距离 $\mathbf{dist}(x_0,C)$。我们用一组线性等式和凸不等式表示集合 $C$：

$$
Ax=b,\qquad f_i(x)\leq0,\quad i=1,\ldots,m,
\tag{8.1}
$$

然后求解问题

$$
\begin{array}{ll}
\text{最小化} & \|x-x_0\|\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
\tag{8.2}
$$

以求出 $x_0$ 在 $C$ 上的投影，其中变量为 $x$。这个问题可行当且仅当 $C$ 非空；当问题可行时，最优值为 $\mathbf{dist}(x_0,C)$，任意最优点都是 $x_0$ 在 $C$ 上的一个投影。

#### 在多面体上的欧几里得投影

$x_0$ 在由线性不等式 $Ax\preceq b$ 描述的多面体上的投影，可以通过求解以下 QP 计算：

$$
\begin{array}{ll}
\text{最小化} & \|x-x_0\|_2^2\\
\text{约束条件} & Ax\preceq b.
\end{array}
$$

一些特殊情况有简单的解析解。

- $x_0$ 在超平面 $C=\{x\mid a^Tx=b\}$ 上的欧几里得投影为

    $$
    P_C(x_0)=x_0+(b-a^Tx_0)a/\|a\|_2^2.
    $$

- $x_0$ 在半空间 $C=\{x\mid a^Tx\leq b\}$ 上的欧几里得投影为

    $$
    P_C(x_0)=\begin{cases}
    x_0+(b-a^Tx_0)a/\|a\|_2^2 & a^Tx_0>b\\
    x_0 & a^Tx_0\leq b.
    \end{cases}
    $$

    <!-- pdf-page: 413 -->

- $x_0$ 在矩形 $C=\{x\mid l\preceq x\preceq u\}$（其中 $l\prec u$）上的欧几里得投影为

    $$
    P_C(x_0)_k=\begin{cases}
    l_k & x_{0k}\leq l_k\\
    x_{0k} & l_k\leq x_{0k}\leq u_k\\
    u_k & x_{0k}\geq u_k.
    \end{cases}
    $$

#### 在正常锥上的欧几里得投影

设 $x=P_K(x_0)$ 表示点 $x_0$ 在正常锥 $K$ 上的欧几里得投影。问题

$$
\begin{array}{ll}
\text{最小化} & \|x-x_0\|_2^2\\
\text{约束条件} & x\succeq_K0
\end{array}
$$

的 KKT 条件为

$$
x\succeq_K0,\qquad x-x_0=z,\qquad z\succeq_{K^*}0,\qquad z^Tx=0.
$$

引入记号 $x_+=x$ 和 $x_-=z$，可以把这些条件写成

$$
x_0=x_+-x_-,\qquad x_+\succeq_K0,\qquad x_-\succeq_{K^*}0,\qquad x_+^Tx_-=0.
$$

换句话说，把 $x_0$ 投影到锥 $K$ 上，就将它分解成两个正交元素之差：其中一个关于 $K$ 非负（它就是 $x_0$ 在 $K$ 上的投影），另一个关于 $K^*$ 非负。

下面是一些具体例子：

- 对 $K=\mathbf{R}_+^n$，有 $P_K(x_0)_k=\max\{x_{0k},0\}$。把向量的每个负分量都替换为 $0$，就得到它在非负正交象限上的欧几里得投影。

- 对 $K=\mathbf{S}_+^n$ 和欧几里得范数（或 Frobenius 范数）$\|\cdot\|_F$，有 $P_K(X_0)=\sum_{i=1}^n\max\{0,\lambda_i\}v_iv_i^T$，其中 $X_0=\sum_{i=1}^n\lambda_i v_iv_i^T$ 是 $X_0$ 的特征值分解。要将一个对称矩阵投影到半正定锥上，只需写出它的特征值展开式，然后去掉负特征值对应的项。这个矩阵也是 $\ell_2$ 范数（即谱范数）下在半正定锥上的投影。

### 8.1.2 分离一个点与一个凸集

设 $C$ 是由等式和不等式 (8.1) 描述的闭凸集。若 $x_0\in C$，则 $\mathbf{dist}(x_0,C)=0$，问题 (8.2) 的最优点就是 $x_0$。若 $x_0\notin C$，则 $\mathbf{dist}(x_0,C)>0$，问题 (8.2) 的最优值为正。在这种情况下，我们将看到，任意对偶最优点都能给出点 $x_0$ 与集合 $C$ 之间的一个分离超平面。

<p id="projection-separation-start" markdown="1">把点投影到凸集上，与寻找将这个点和集合分离的超平面（当点不在集合中时），这两者之间存在联系并不意外。事实上，§2.5.1 中分离超平面定理的证明就依靠</p>

<!-- pdf-page: 414 -->

<figure id="fig-8-1" data-figure="8.1" data-no-english-text="true" data-reader-after="projection-separation-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-1.png" alt="点 x₀ 位于灰色凸集 C 外，虚线将它连接到集合边界上的欧几里得投影 P_C(x₀)，两点之间的斜直线垂直平分这条线段并将点与集合分开" data-source-page="414" data-source-rect="246,120,432,259">
<figcaption>图 8.1 点 $x_0$ 及其在凸集 $C$ 上的欧几里得投影 $P_C(x_0)$。位于这两点中间、法向量为 $P_C(x_0)-x_0$ 的超平面，将这个点与该集合严格分离。这一性质对一般范数并不成立；见习题 8.4。</figcaption>
</figure>

<p id="projection-separation-middle" markdown="1" data-reader-continue="projection-separation-start">求出集合之间的欧几里得距离。若 $P_C(x_0)$ 表示 $x_0$ 在 $C$ 上的欧几里得投影，其中 $x_0\notin C$，则超平面</p>

$$
(P_C(x_0)-x_0)^T\bigl(x-(1/2)(x_0+P_C(x_0))\bigr)=0
$$

<p id="projection-separation-end" markdown="1">将 $x_0$ 与 $C$（严格）分离，如图 8.1 所示。不过，对其他范数，投影问题与分离超平面问题之间最清楚的联系是通过拉格朗日对偶性建立的。</p>

首先，把 (8.2) 写成

$$
\begin{array}{ll}
\text{最小化} & \|y\|\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b\\
& x_0-x=y,
\end{array}
$$

其中变量为 $x$ 和 $y$。这个问题的拉格朗日函数为

$$
L(x,y,\lambda,\mu,\nu)=\|y\|+\sum_{i=1}^m\lambda_i f_i(x)+\nu^T(Ax-b)+\mu^T(x_0-x-y),
$$

对偶函数为

$$
g(\lambda,\mu,\nu)=\begin{cases}
\displaystyle\inf_x\left(\sum_{i=1}^m\lambda_i f_i(x)+\nu^T(Ax-b)+\mu^T(x_0-x)\right) & \|\mu\|_*\leq1\\
-\infty & \text{其他情况},
\end{cases}
$$

因此得到对偶问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\mu^Tx_0+\inf_x\left(\sum_{i=1}^m\lambda_i f_i(x)+\nu^T(Ax-b)-\mu^Tx\right)\\
\text{约束条件} & \lambda\succeq0\\
& \|\mu\|_*\leq1,
\end{array}
$$

其中变量为 $\lambda$、$\mu$、$\nu$。可以如下解释这个对偶问题。设 $\lambda$、$\mu$、$\nu$ 对偶可行，并且对偶目标值为正，即 $\lambda\succeq0$、$\|\mu\|_*\leq1$，<!-- pdf-page: 415 -->并且对所有 $x$ 都有

$$
\mu^Tx_0-\mu^Tx+\sum_{i=1}^m\lambda_i f_i(x)+\nu^T(Ax-b)>0.
$$

这意味着对 $x\in C$，有 $\mu^Tx_0>\mu^Tx$，因此 $\mu$ 定义了一个严格分离超平面。特别地，假设 (8.2) 严格可行，从而强对偶性成立。若 $x_0\notin C$，最优值为正，任意对偶最优解都定义了一个严格分离超平面。

注意，这种通过对偶性构造分离超平面的方法适用于任意范数。上面介绍的简单构造方法则只适用于欧几里得范数。

#### 将一个点与多面体分离

问题

$$
\begin{array}{ll}
\text{最小化} & \|y\|\\
\text{约束条件} & Ax\preceq b\\
& x_0-x=y
\end{array}
$$

的对偶问题为

$$
\begin{array}{ll}
\text{最大化} & \mu^Tx_0-b^T\lambda\\
\text{约束条件} & A^T\lambda=\mu\\
& \|\mu\|_*\leq1\\
& \lambda\succeq0,
\end{array}
$$

它可以进一步简化为

$$
\begin{array}{ll}
\text{最大化} & (Ax_0-b)^T\lambda\\
\text{约束条件} & \|A^T\lambda\|_*\leq1\\
& \lambda\succeq0.
\end{array}
$$

容易验证：若对偶目标值为正，那么 $A^T\lambda$ 就是一个分离超平面的法向量。若 $Ax\preceq b$，则

$$
(A^T\lambda)^Tx=\lambda^T(Ax)\leq\lambda^Tb<\lambda^TAx_0,
$$

所以 $\mu=A^T\lambda$ 定义了一个分离超平面。

### 8.1.3 用指示函数和支撑函数表示投影与分离

上面 §8.1.1 和 §8.1.2 中的思路，可以用集合 $C$ 的指示函数 $I_C$ 和支撑函数 $S_C$ 简洁地表达出来。它们的定义为

$$
S_C(x)=\sup_{y\in C}x^Ty,\qquad
I_C(x)=\begin{cases}0 & x\in C\\+\infty & x\notin C.\end{cases}
$$

将 $x_0$ 投影到闭凸集 $C$ 上的问题，可以简洁地写成

$$
\begin{array}{ll}
\text{最小化} & \|x-x_0\|\\
\text{约束条件} & I_C(x)\leq0,
\end{array}
$$

<!-- pdf-page: 416 -->

或者等价地写成

$$
\begin{array}{ll}
\text{最小化} & \|y\|\\
\text{约束条件} & I_C(x)\leq0\\
& x_0-x=y,
\end{array}
$$

其中变量为 $x$ 和 $y$。这个问题的对偶函数为

$$
\begin{aligned}
g(z,\lambda)&=\inf_{x,y}\bigl(\|y\|+\lambda I_C(x)+z^T(x_0-x-y)\bigr)\\
&=\begin{cases}
\displaystyle z^Tx_0+\inf_x\bigl(-z^Tx+I_C(x)\bigr) & \|z\|_*\leq1,\quad\lambda\geq0\\
-\infty & \text{其他情况}
\end{cases}\\
&=\begin{cases}
z^Tx_0-S_C(z) & \|z\|_*\leq1,\quad\lambda\geq0\\
-\infty & \text{其他情况},
\end{cases}
\end{aligned}
$$

因此得到对偶问题

$$
\begin{array}{ll}
\text{最大化} & z^Tx_0-S_C(z)\\
\text{约束条件} & \|z\|_*\leq1.
\end{array}
$$

若 $z$ 对偶最优，且目标值为正，那么对所有 $x\in C$，都有 $z^Tx_0>z^Tx$，即 $z$ 定义了一个分离超平面。

## 8.2 集合之间的距离

在范数 $\|\cdot\|$ 下，两个集合 $C$ 和 $D$ 之间的距离定义为

$$
\mathbf{dist}(C,D)=\inf\{\|x-y\|\mid x\in C,\ y\in D\}.
$$

若 $\mathbf{dist}(C,D)>0$，则两个集合 $C$ 和 $D$ 不相交。若 $\mathbf{dist}(C,D)=0$，并且定义中的下确界能够达到，则它们相交（例如，当两个集合都是闭集，且其中一个有界时，下确界就能够达到）。

集合之间的距离可以用点到集合的距离表示：

$$
\mathbf{dist}(C,D)=\mathbf{dist}(0,D-C),
$$

因此可以应用上一节的结果。不过，本节将专门针对涉及集合间距离的问题推导结果。这样可以利用集合 $C-D$ 的结构，也使结果更容易解释。

### 8.2.1 计算凸集之间的距离

设 $C$ 和 $D$ 由两组凸不等式描述：

$$
C=\{x\mid f_i(x)\leq0,\ i=1,\ldots,m\},\qquad
D=\{x\mid g_i(x)\leq0,\ i=1,\ldots,p\}.
$$

<!-- pdf-page: 417 -->

<figure id="fig-8-2" data-figure="8.2" data-no-english-text="true" data-reader-after="polyhedra-distance-qp-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-2.png" alt="两个分离的灰色多边形 C 和 D，虚线连接各自边界上彼此最接近的两个点，表示两个集合的欧几里得距离" data-source-page="417" data-source-rect="192,120,379,229">
<figcaption>图 8.2 多面体 $C$ 与 $D$ 之间的欧几里得距离。虚线连接分别位于 $C$ 和 $D$ 中、按欧几里得范数衡量时彼此最接近的两个点。这两个点可以通过求解一个 QP 找到。</figcaption>
</figure>

（也可以加入线性等式，但为简单起见，这里不考虑。）通过求解凸优化问题

$$
\begin{array}{ll}
\text{最小化} & \|x-y\|\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& g_i(y)\leq0,\quad i=1,\ldots,p,
\end{array}
\tag{8.3}
$$

就能求出 $\mathbf{dist}(C,D)$。

#### 多面体之间的欧几里得距离

设 $C$ 和 $D$ 是分别由线性不等式组 $A_1x\preceq b_1$ 和 $A_2x\preceq b_2$ 描述的两个多面体。$C$ 与 $D$ 之间的距离，就是分别位于 $C$ 和 $D$ 中、彼此最接近的一对点之间的距离，如图 8.2 所示。这个距离等于问题

$$
\begin{array}{ll}
\text{最小化} & \|x-y\|_2\\
\text{约束条件} & A_1x\preceq b_1\\
& A_2y\preceq b_2
\end{array}
\tag{8.4}
$$

<p id="polyhedra-distance-qp-end" markdown="1">的最优值。将目标函数平方，就得到一个等价的 QP。</p>

### 8.2.2 分离凸集

求两个凸集之间距离的问题 (8.3)，其对偶问题可以用这两个集合之间的分离超平面作出有趣的几何解释。首先把问题写成以下等价形式：

$$
\begin{array}{ll}
\text{最小化} & \|w\|\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& g_i(y)\leq0,\quad i=1,\ldots,p\\
& x-y=w.
\end{array}
\tag{8.5}
$$

对偶函数为

$$
g(\lambda,z,\mu)=\inf_{x,y,w}\left(\|w\|+\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\mu_i g_i(y)+z^T(x-y-w)\right)
$$

<!-- pdf-page: 418 -->

$$
=\begin{cases}
\displaystyle\inf_x\left(\sum_{i=1}^m\lambda_i f_i(x)+z^Tx\right)+\inf_y\left(\sum_{i=1}^p\mu_i g_i(y)-z^Ty\right) & \|z\|_*\leq1\\
-\infty & \text{其他情况},
\end{cases}
$$

由此得到对偶问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\inf_x\left(\sum_{i=1}^m\lambda_i f_i(x)+z^Tx\right)+\inf_y\left(\sum_{i=1}^p\mu_i g_i(y)-z^Ty\right)\\
\text{约束条件} & \|z\|_*\leq1\\
& \lambda\succeq0,\quad\mu\succeq0.
\end{array}
\tag{8.6}
$$

可以给出如下几何解释。若 $\lambda$、$\mu$ 对偶可行，且目标值为正，那么对所有 $x$ 和 $y$ 都有

$$
\sum_{i=1}^m\lambda_i f_i(x)+z^Tx+\sum_{i=1}^p\mu_i g_i(y)-z^Ty>0.
$$

特别地，对 $x\in C$ 和 $y\in D$，有 $z^Tx-z^Ty>0$，因此 $z$ 定义了一个严格分离 $C$ 与 $D$ 的超平面。

所以，若问题 (8.5) 和 (8.6) 之间的强对偶性成立（当 (8.5) 严格可行时就是如此），就可以得出以下结论：如果两个集合之间的距离为正，那么存在一个超平面将它们严格分离。

#### 分离多面体

把这些对偶性结果应用于由线性不等式 $A_1x\preceq b_1$ 和 $A_2x\preceq b_2$ 定义的集合，得到对偶问题

$$
\begin{array}{ll}
\text{最大化} & -b_1^T\lambda-b_2^T\mu\\
\text{约束条件} & A_1^T\lambda+z=0\\
& A_2^T\mu-z=0\\
& \|z\|_*\leq1\\
& \lambda\succeq0,\quad\mu\succeq0.
\end{array}
$$

若 $\lambda$、$\mu$ 和 $z$ 对偶可行，那么对所有 $x\in C$、$y\in D$，

$$
z^Tx=-\lambda^TA_1x\geq-\lambda^Tb_1,\qquad
z^Ty=\mu^TA_2x\leq\mu^Tb_2,
$$

并且，若对偶目标值为正，则

$$
z^Tx-z^Ty\geq-\lambda^Tb_1-\mu^Tb_2>0,
$$

即 $z$ 定义了一个分离超平面。

### 8.2.3 用指示函数和支撑函数表示距离与分离

上面 §8.2.1 和 §8.2.2 中的思路，可以用指示函数和支撑函数简洁地表达出来。求两个凸集之间距离的问题，可以写成凸问题

$$
\begin{array}{ll}
\text{最小化} & \|x-y\|\\
\text{约束条件} & I_C(x)\leq0\\
& I_D(y)\leq0,
\end{array}
$$

<!-- pdf-page: 419 -->

它等价于

$$
\begin{array}{ll}
\text{最小化} & \|w\|\\
\text{约束条件} & I_C(x)\leq0\\
& I_D(y)\leq0\\
& x-y=w.
\end{array}
$$

这个问题的对偶问题为

$$
\begin{array}{ll}
\text{最大化} & -S_C(-z)-S_D(z)\\
\text{约束条件} & \|z\|_*\leq1.
\end{array}
$$

若 $z$ 对偶可行，且目标值为正，那么 $S_D(z)<-S_C(-z)$，即

$$
\sup_{x\in D}z^Tx<\inf_{x\in C}z^Tx.
$$

换句话说，$z$ 定义了一个严格分离 $C$ 与 $D$ 的超平面。

## 8.3 欧几里得距离与角度问题

设 $a_1,\ldots,a_n$ 是 $\mathbf{R}^n$ 中的一组向量，暂且假设它们的欧几里得长度已知：

$$
l_1=\|a_1\|_2,\quad\ldots,\quad l_n=\|a_n\|_2.
$$

我们把这组向量称为一个*构型*（configuration）；当它们线性无关时，也称为一组*基*。本节考虑涉及构型各种几何性质的优化问题，例如向量两两之间的欧几里得距离、夹角，以及衡量基的条件好坏的各种几何量。

### 8.3.1 Gram 矩阵与可实现性

长度、距离和角度都可以用向量 $a_1,\ldots,a_n$ 对应的 *Gram 矩阵*表示。该矩阵为

$$
G=A^TA,\qquad A=\begin{bmatrix}a_1&\cdots&a_n\end{bmatrix},
$$

因此 $G_{ij}=a_i^Ta_j$。$G$ 的对角元素为

$$
G_{ii}=l_i^2,\qquad i=1,\ldots,n,
$$

暂且假设它们已知且固定。$a_i$ 与 $a_j$ 之间的距离 $d_{ij}$ 为

$$
\begin{aligned}
d_{ij}&=\|a_i-a_j\|_2\\
&=(l_i^2+l_j^2-2a_i^Ta_j)^{1/2}\\
&=(l_i^2+l_j^2-2G_{ij})^{1/2}.
\end{aligned}
$$

<!-- pdf-page: 420 -->

反过来，可以用 $d_{ij}$ 表示 $G_{ij}$：

$$
G_{ij}=\frac{l_i^2+l_j^2-d_{ij}^2}{2}.
$$

这里先指出一个后面会用到的事实：它是 $d_{ij}^2$ 的仿射函数。

非零向量 $a_i$ 与 $a_j$ 之间的*相关系数* $\rho_{ij}$ 为

$$
\rho_{ij}=\frac{a_i^Ta_j}{\|a_i\|_2\|a_j\|_2}=\frac{G_{ij}}{l_il_j},
$$

所以 $G_{ij}=l_il_j\rho_{ij}$ 是 $\rho_{ij}$ 的线性函数。非零向量 $a_i$ 与 $a_j$ 之间的*夹角* $\theta_{ij}$ 为

$$
\theta_{ij}=\cos^{-1}\rho_{ij}=\cos^{-1}(G_{ij}/(l_il_j)),
$$

其中取 $\cos^{-1}\rho\in[0,\pi]$。因此，$G_{ij}=l_il_j\cos\theta_{ij}$。

长度、距离和角度在正交变换下保持不变：若 $Q\in\mathbf{R}^{n\times n}$ 是正交矩阵，那么向量组 $Qa_i,\ldots,Qa_n$ 具有相同的 Gram 矩阵，因此长度、距离和角度也相同。

#### 可实现性

Gram 矩阵 $G=A^TA$ 显然对称且半正定。逆命题是线性代数中的一个基本结果：矩阵 $G\in\mathbf{S}^n$ 是某组向量 $a_1,\ldots,a_n$ 的 Gram 矩阵，当且仅当 $G\succeq0$。当 $G\succeq0$ 时，求出满足 $A^TA=G$ 的矩阵 $A$，就可以构造出一个 Gram 矩阵为 $G$ 的构型。这个方程的一个解是对称平方根 $A=G^{1/2}$。当 $G\succ0$ 时，可以通过 $G$ 的 Cholesky 分解求解：若 $LL^T=G$，则可以取 $A=L^T$。而且，给定任意一个解 $A$ 后，就可以通过正交变换，构造出具有给定 Gram 矩阵 $G$ 的所有构型：若 $\widetilde A^T\widetilde A=G$ 是任意一个解，那么对某个正交矩阵 $Q$，有 $\widetilde A=QA$。

因此，一组长度、距离和角度（或相关系数）*可实现*，即它们确实对应某个构型，当且仅当相应的 Gram 矩阵 $G$ 半正定，且对角元素为 $l_1^2,\ldots,l_n^2$。

利用这个事实，可以把若干几何问题写成以 $G\in\mathbf{S}^n$ 为优化变量的凸优化问题。可实现性要求满足约束 $G\succeq0$ 和 $G_{ii}=l_i^2$，$i=1,\ldots,n$；下面列出其他一些凸约束和目标。

#### 角度与距离约束

通过线性等式约束 $G_{ij}=l_il_j\cos\alpha$，可以把夹角固定为某个值 $\theta_{ij}=\alpha$。更一般地，要给夹角施加上下界 $\alpha\leq\theta_{ij}\leq\beta$，可以使用约束

$$
l_il_j\cos\alpha\geq G_{ij}\geq l_il_j\cos\beta,
$$

这是关于 $G$ 的两个线性不等式。（这里用到了 $\cos^{-1}$ 单调递减这一事实。）通过最小化或最大化 $G_{ij}$，就可以最大化或最小化某个夹角 $\theta_{ij}$，这里同样用到了 $\cos^{-1}$ 的单调性。

<!-- pdf-page: 421 -->

类似地，也可以对距离施加约束。要使 $d_{ij}$ 位于某个区间内，可以使用

$$
\begin{aligned}
d_{\min}\leq d_{ij}\leq d_{\max}
&\quad\Longleftrightarrow\quad d_{\min}^2\leq d_{ij}^2\leq d_{\max}^2\\
&\quad\Longleftrightarrow\quad d_{\min}^2\leq l_i^2+l_j^2-2G_{ij}\leq d_{\max}^2,
\end{aligned}
$$

这也是关于 $G$ 的两个线性不等式。通过最小化或最大化距离的平方，就可以最小化或最大化距离；距离的平方是 $G$ 的仿射函数。

举一个简单的例子，假设已知某些夹角和某些距离的取值范围，即可能取值的区间。求解两个 SDP，就能在所有构型中找出另一个夹角或另一段距离可能的最小值和最大值。对得到的最优 Gram 矩阵进行分解，可以重建出这两个极端构型。

#### 奇异值与条件数约束

$A$ 的奇异值 $\sigma_1\geq\cdots\geq\sigma_n$，是 $G$ 的特征值 $\lambda_1\geq\cdots\geq\lambda_n$ 的平方根。因此，$\sigma_1^2$ 是 $G$ 的凸函数，$\sigma_n^2$ 是 $G$ 的凹函数。所以，可以对 $A$ 的最大奇异值施加上界，或者将它最小化；也可以对最小奇异值施加下界，或者将它最大化。$A$ 的条件数 $\sigma_1/\sigma_n$ 是 $G$ 的拟凸函数，因此可以通过拟凸优化，对它施加允许的最大值约束，或者在满足其他几何约束的所有构型中将它最小化。

粗略地说，能够写成关于 $G$ 的凸约束的条件，都是要求 $a_1,\ldots,a_n$ 构成一组良态基的条件。

#### 对偶基

当 $G\succ0$ 时，$a_1,\ldots,a_n$ 构成 $\mathbf{R}^n$ 的一组基。相应的*对偶基*为 $b_1,\ldots,b_n$，其中

$$
b_i^Ta_j=\begin{cases}1 & i=j\\0 & i\ne j.\end{cases}
$$

对偶基向量 $b_1,\ldots,b_n$ 就是矩阵 $A^{-1}$ 的各行。因此，对偶基对应的 Gram 矩阵是 $G^{-1}$。

对偶基上的若干几何条件也可以写成关于 $G$ 的凸约束。对偶基向量的长度平方

$$
\|b_i\|_2^2=e_i^TG^{-1}e_i
$$

是 $G$ 的凸函数，因此可以将它们最小化。$G^{-1}$ 的迹也是 $G$ 的凸函数，它给出对偶基向量长度的平方和，也是衡量基是否良态的另一个量。

#### 椭球与单纯形的体积

椭球 $\{Au\mid\|u\|_2\leq1\}$ 的体积可以作为衡量基是否良态的另一个量，其值为

$$
\gamma(\det(A^TA))^{1/2}=\gamma(\det G)^{1/2},
$$

<!-- pdf-page: 422 -->

其中 $\gamma$ 是 $\mathbf{R}^n$ 中单位球的体积。因此，体积的对数为 $\log\gamma+(1/2)\log\det G$，它是 $G$ 的凹函数。所以，在由构型组成的一个凸集上，最大化 $\log\det G$ 就可以最大化变换后椭球的体积。

对 $\mathbf{R}^n$ 中的任意集合也有同样的结论。它经 $A$ 变换后的像的体积，等于原体积乘以因子 $(\det G)^{1/2}$。例如，考虑单位单纯形 $\mathbf{conv}\{0,e_1,\ldots,e_n\}$ 在 $A$ 下的像，即单纯形 $\mathbf{conv}\{0,a_1,\ldots,a_n\}$。这个单纯形的体积为 $\widetilde\gamma(\det G)^{1/2}$，其中 $\widetilde\gamma$ 是 $\mathbf{R}^n$ 中单位单纯形的体积。通过最大化 $\log\det G$，就能最大化这个单纯形的体积。

### 8.3.2 只涉及角度的问题

假设只关心向量之间的夹角（或相关系数），不规定它们的长度或相互之间的距离。这时，直观上可以直接假设向量 $a_i$ 的长度为 $l_i=1$。这很容易验证：Gram 矩阵可以写成 $G=\mathbf{diag}(l)C\mathbf{diag}(l)$，其中 $l$ 是长度组成的向量，$C$ 是相关矩阵，即 $C_{ij}=\cos\theta_{ij}$。于是，如果某组正长度使 $G\succeq0$ 成立，那么对所有正长度组，都有 $G\succeq0$；特别地，这当且仅当 $C\succeq0$，也就是假设所有长度均为一时的条件。因此，一组夹角 $\theta_{ij}\in[0,\pi]$，$i,j=1,\ldots,n$，可实现当且仅当 $C\succeq0$，这是关于相关系数的线性矩阵不等式。

例如，假设已知某些夹角的上下界，等价地，也就是给某些相关系数施加上下界。通过求解两个 SDP，就能在所有构型中找出另一个夹角可能的最小值和最大值。

<div class="example" markdown="1">

**例 8.3 求相关系数的界。** 考虑 $\mathbf{R}^4$ 中的一个例子，已知

$$
\begin{aligned}
0.6\leq\rho_{12}\leq0.9,\qquad &0.8\leq\rho_{13}\leq0.9,\\
0.5\leq\rho_{24}\leq0.7,\qquad &-0.8\leq\rho_{34}\leq-0.4.
\end{aligned}
\tag{8.7}
$$

为求出 $\rho_{14}$ 可能的最小值和最大值，求解以下两个 SDP：

$$
\begin{array}{ll}
\text{最小化／最大化} & \rho_{14}\\
\text{约束条件} & (8.7)\\
& \begin{bmatrix}
1&\rho_{12}&\rho_{13}&\rho_{14}\\
\rho_{12}&1&\rho_{23}&\rho_{24}\\
\rho_{13}&\rho_{23}&1&\rho_{34}\\
\rho_{14}&\rho_{24}&\rho_{34}&1
\end{bmatrix}\succeq0,
\end{array}
$$

其中变量为 $\rho_{12}$、$\rho_{13}$、$\rho_{14}$、$\rho_{23}$、$\rho_{24}$、$\rho_{34}$。最小值和最大值（保留两位有效数字）分别为 $-0.39$ 和 $0.23$，对应的相关矩阵为

$$
\begin{bmatrix}
1.00&0.60&0.87&-0.39\\
0.60&1.00&0.33&0.50\\
0.87&0.33&1.00&-0.55\\
-0.39&0.50&-0.55&1.00
\end{bmatrix},\qquad
\begin{bmatrix}
1.00&0.71&0.80&0.23\\
0.71&1.00&0.31&0.59\\
0.80&0.31&1.00&-0.40\\
0.23&0.59&-0.40&1.00
\end{bmatrix}.
$$

</div>

<!-- pdf-page: 423 -->

### 8.3.3 欧几里得距离问题

在*欧几里得距离问题*中，我们只关心向量之间的距离 $d_{ij}$，不关心向量的长度或它们之间的夹角。这些距离当然不仅在正交变换下不变，而且在平移下也不变：对任意 $b\in\mathbf{R}^n$，构型 $\widetilde a_1=a_1+b,\ldots,\widetilde a_n=a_n+b$ 与原构型具有相同的距离。特别地，若选择

$$
b=-(1/n)\sum_{i=1}^n a_i=-(1/n)A\mathbf{1},
$$

那么 $\widetilde a_i$ 之间的距离与原构型相同，并且满足 $\sum_{i=1}^n\widetilde a_i=0$。因此，在欧几里得距离问题中，不失一般性，可以假设向量 $a_1,\ldots,a_n$ 的平均值为零，即 $A\mathbf{1}=0$。

求解欧几里得距离问题时，可以把长度作为优化问题中的自由变量；这些长度不会出现在欧几里得距离问题的目标或约束中。这里用到的事实是：存在一个距离为 $d_{ij}\geq0$ 的构型，当且仅当存在长度 $l_1,\ldots,l_n$ 使 $G\succeq0$，其中 $G_{ij}=(l_i^2+l_j^2-d_{ij}^2)/2$。

定义 $z\in\mathbf{R}^n$，其中 $z_i=l_i^2$，并定义 $D\in\mathbf{S}^n$，其中 $D_{ij}=d_{ij}^2$，当然 $D_{ii}=0$。存在某组长度使 $G\succeq0$ 的条件，可以写成

$$
G=(z\mathbf{1}^T+\mathbf{1}z^T-D)/2\succeq0\quad\text{对某个 }z\succeq0\text{ 成立},
\tag{8.8}
$$

这是关于 $D$ 和 $z$ 的 LMI。如果矩阵 $D\in\mathbf{S}^n$ 的元素非负、对角元素为零，并且满足 (8.8)，就称它为*欧几里得距离矩阵*。矩阵是欧几里得距离矩阵，当且仅当它的元素是某个构型中各向量之间欧几里得距离的平方。（给定欧几里得距离矩阵 $D$ 以及相应的长度平方向量 $z$，可以用上面介绍的方法，重建出具有给定两两距离的一个或所有构型。）

条件 (8.8) 其实等价于一个更简单的条件：$D$ 在 $\mathbf{1}^{\perp}$ 上半负定，即

$$
\begin{aligned}
(8.8)&\quad\Longleftrightarrow\quad u^TDu\leq0\quad\text{对所有满足 }\mathbf{1}^Tu=0\text{ 的 }u\\
&\quad\Longleftrightarrow\quad (I-(1/n)\mathbf{1}\mathbf{1}^T)D(I-(1/n)\mathbf{1}\mathbf{1}^T)\preceq0.
\end{aligned}
$$

这个简单的矩阵不等式，加上 $D_{ij}\geq0$ 和 $D_{ii}=0$，就是欧几里得距离矩阵的经典刻画。要看出这种等价性，回顾前面可以假设 $A\mathbf{1}=0$，这意味着 $\mathbf{1}^TG\mathbf{1}=\mathbf{1}^TA^TA\mathbf{1}=0$。因此，$G\succeq0$ 当且仅当 $G$ 在 $\mathbf{1}^{\perp}$ 上半正定，即

$$
\begin{aligned}
0&\preceq(I-(1/n)\mathbf{1}\mathbf{1}^T)G(I-(1/n)\mathbf{1}\mathbf{1}^T)\\
&=(1/2)(I-(1/n)\mathbf{1}\mathbf{1}^T)(z\mathbf{1}^T+\mathbf{1}z^T-D)(I-(1/n)\mathbf{1}\mathbf{1}^T)\\
&=-(1/2)(I-(1/n)\mathbf{1}\mathbf{1}^T)D(I-(1/n)\mathbf{1}\mathbf{1}^T),
\end{aligned}
$$

这正是简化后的条件。

<!-- pdf-page: 424 -->

总之，矩阵 $D\in\mathbf{S}^n$ 是欧几里得距离矩阵，即它给出 $\mathbf{R}^n$ 中一组 $n$ 个向量之间的距离平方，当且仅当

$$
\begin{gathered}
D_{ii}=0,\quad i=1,\ldots,n,\qquad D_{ij}\geq0,\quad i,j=1,\ldots,n,\\
(I-(1/n)\mathbf{1}\mathbf{1}^T)D(I-(1/n)\mathbf{1}\mathbf{1}^T)\preceq0.
\end{gathered}
$$

这是一组关于 $D$ 的线性等式、线性不等式以及一个矩阵不等式。因此，任何关于距离平方为凸的欧几里得距离问题，都可以写成以 $D\in\mathbf{S}^n$ 为变量的凸问题。

## 8.4 极值体积椭球

设 $C\subseteq\mathbf{R}^n$ 有界且内部非空。本节考虑两个问题：求位于 $C$ 内的最大体积椭球，以及覆盖 $C$ 的最小体积椭球。这两个问题都可以表述为凸规划问题，但只有在特殊情况下才能高效求解。

### 8.4.1 Löwner-John 椭球

包含集合 $C$ 的最小体积椭球，称为集合 $C$ 的 *Löwner-John 椭球*，记为 $\mathcal{E}_{\mathrm{lj}}$。为刻画 $\mathcal{E}_{\mathrm{lj}}$，将一般椭球参数化为以下形式比较方便：

$$
\mathcal{E}=\{v\mid\|Av+b\|_2\leq1\},
\tag{8.9}
$$

也就是欧几里得单位球在仿射映射下的原像。不失一般性，可以假设 $A\in\mathbf{S}_{++}^n$，这时 $\mathcal{E}$ 的体积与 $\det A^{-1}$ 成正比。计算包含 $C$ 的最小体积椭球的问题，可以写成

$$
\begin{array}{ll}
\text{最小化} & \log\det A^{-1}\\
\text{约束条件} & \displaystyle\sup_{v\in C}\|Av+b\|_2\leq1,
\end{array}
\tag{8.10}
$$

其中变量为 $A\in\mathbf{S}^n$ 和 $b\in\mathbf{R}^n$，并有隐含约束 $A\succ0$。目标函数和约束函数都关于 $A$、$b$ 为凸，所以问题 (8.10) 是凸问题。然而，计算 (8.10) 中约束函数的值需要求解一个凸函数最大化问题，只有在某些特殊情况下才能高效完成。

#### 覆盖有限集合的最小体积椭球

考虑求包含有限集合 $C=\{x_1,\ldots,x_m\}\subseteq\mathbf{R}^n$ 的最小体积椭球。一个椭球覆盖 $C$，当且仅当它覆盖 $C$ 的凸包，所以求覆盖 $C$ 的最小体积椭球，<!-- pdf-page: 425 -->与求包含多面体 $\mathbf{conv}\{x_1,\ldots,x_m\}$ 的最小体积椭球相同。应用 (8.10)，可以把这个问题写成

$$
\begin{array}{ll}
\text{最小化} & \log\det A^{-1}\\
\text{约束条件} & \|Ax_i+b\|_2\leq1,\quad i=1,\ldots,m,
\end{array}
\tag{8.11}
$$

其中变量为 $A\in\mathbf{S}^n$ 和 $b\in\mathbf{R}^n$，并有隐含约束 $A\succ0$。范数约束 $\|Ax_i+b\|_2\leq1$，$i=1,\ldots,m$，是关于变量 $A$ 和 $b$ 的凸不等式。也可以将它们替换为平方形式 $\|Ax_i+b\|_2^2\leq1$，这是关于 $A$ 和 $b$ 的凸二次不等式。

#### 覆盖椭球之并的最小体积椭球

对某些由二次不等式定义的集合 $C$，也能高效计算最小体积覆盖椭球。特别地，可以计算若干椭球的并或和的 Löwner-John 椭球。

例如，考虑求包含椭球 $\mathcal{E}_1,\ldots,\mathcal{E}_m$ 的最小体积椭球 $\mathcal{E}_{\mathrm{lj}}$；它也就包含这些椭球之并的凸包。用（凸）二次不等式描述椭球 $\mathcal{E}_1,\ldots,\mathcal{E}_m$：

$$
\mathcal{E}_i=\{x\mid x^TA_ix+2b_i^Tx+c_i\leq0\},\qquad i=1,\ldots,m,
$$

其中 $A_i\in\mathbf{S}_{++}^n$。将椭球 $\mathcal{E}_{\mathrm{lj}}$ 参数化为

$$
\begin{aligned}
\mathcal{E}_{\mathrm{lj}}&=\{x\mid\|Ax+b\|_2\leq1\}\\
&=\{x\mid x^TA^TAx+2(A^Tb)^Tx+b^Tb-1\leq0\},
\end{aligned}
$$

其中 $A\in\mathbf{S}^n$、$b\in\mathbf{R}^n$。现在利用 §B.2 中的一个结果：$\mathcal{E}_i\subseteq\mathcal{E}_{\mathrm{lj}}$ 当且仅当存在 $\tau\geq0$，使

$$
\begin{bmatrix}
A^2-\tau A_i & Ab-\tau b_i\\
(Ab-\tau b_i)^T & b^Tb-1-\tau c_i
\end{bmatrix}\preceq0.
$$

$\mathcal{E}_{\mathrm{lj}}$ 的体积与 $\det A^{-1}$ 成正比，因此求解以下问题，就可以找出包含 $\mathcal{E}_1,\ldots,\mathcal{E}_m$ 的最小体积椭球：

$$
\begin{array}{ll}
\text{最小化} & \log\det A^{-1}\\
\text{约束条件} & \tau_1\geq0,\ldots,\tau_m\geq0\\
& \begin{bmatrix}
A^2-\tau_i A_i & Ab-\tau_i b_i\\
(Ab-\tau_i b_i)^T & b^Tb-1-\tau_i c_i
\end{bmatrix}\preceq0,\quad i=1,\ldots,m,
\end{array}
$$

或者用 $\widetilde b=Ab$ 替换变量 $b$，得到

$$
\begin{array}{ll}
\text{最小化} & \log\det A^{-1}\\
\text{约束条件} & \tau_1\geq0,\ldots,\tau_m\geq0\\
& \begin{bmatrix}
A^2-\tau_i A_i & \widetilde b-\tau_i b_i & 0\\
(\widetilde b-\tau_i b_i)^T & -1-\tau_i c_i & \widetilde b^T\\
0 & \widetilde b & -A^2
\end{bmatrix}\preceq0,\quad i=1,\ldots,m.
\end{array}
$$

这个问题关于变量 $A^2\in\mathbf{S}^n$、$\widetilde b$、$\tau_1,\ldots,\tau_m$ 为凸。

<!-- pdf-page: 426 -->

<figure id="fig-8-3" data-figure="8.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-3.png" alt="六个实心点构成的多边形包含在外侧椭圆内；内侧灰色椭圆与外侧椭圆同心，缩小后完全位于多边形中" data-source-page="426" data-source-rect="246,122,430,273">
<figcaption>图 8.3 外侧椭圆是 Löwner-John 椭球的边界，即包含点 $x_1,\ldots,x_6$（以实心点表示）、从而也包含多面体 $\mathcal{P}=\mathbf{conv}\{x_1,\ldots,x_6\}$ 的最小体积椭球的边界。较小的椭圆是将 Löwner-John 椭球以其中心为基准缩小至原来的 $1/n$ 后的边界，这里 $n=2$。可以保证这个椭球位于 $\mathcal{P}$ 内。</figcaption>
</figure>

#### Löwner-John 椭球逼近的效果

设 $\mathcal{E}_{\mathrm{lj}}$ 是有界且内部非空的凸集 $C\subseteq\mathbf{R}^n$ 的 Löwner-John 椭球，$x_0$ 为其中心。如果以中心为基准，将 Löwner-John 椭球缩小至原来的 $1/n$，得到的椭球就位于集合 $C$ 内：

$$
x_0+(1/n)(\mathcal{E}_{\mathrm{lj}}-x_0)\subseteq C\subseteq\mathcal{E}_{\mathrm{lj}}.
$$

换句话说，Löwner-John 椭球可以在一个只取决于维数 $n$ 的比例因子范围内逼近任意凸集。图 8.3 给出了一个简单的例子。

若不对 $C$ 作额外假设，就无法改进因子 $1/n$。例如，$\mathbf{R}^n$ 中任意单纯形的 Löwner-John 椭球，都必须缩小至原来的 $1/n$，才能放入该单纯形内（见习题 8.13）。

下面对特殊情况 $C=\mathbf{conv}\{x_1,\ldots,x_m\}$ 证明这个逼近效果结论。将 (8.11) 中的范数约束平方，并引入变量 $\widetilde A=A^2$ 和 $\widetilde b=Ab$，得到问题

$$
\begin{array}{ll}
\text{最小化} & \log\det\widetilde A^{-1}\\
\text{约束条件} & x_i^T\widetilde A x_i-2\widetilde b^Tx_i+\widetilde b^T\widetilde A^{-1}\widetilde b\leq1,\quad i=1,\ldots,m.
\end{array}
\tag{8.12}
$$

这个问题的 KKT 条件为

$$
\begin{gathered}
\sum_{i=1}^m\lambda_i(x_ix_i^T-\widetilde A^{-1}\widetilde b\widetilde b^T\widetilde A^{-1})=\widetilde A^{-1},\qquad
\sum_{i=1}^m\lambda_i(x_i-\widetilde A^{-1}\widetilde b)=0,\\
\lambda_i\geq0,\qquad x_i^T\widetilde A x_i-2\widetilde b^Tx_i+\widetilde b^T\widetilde A^{-1}\widetilde b\leq1,\quad i=1,\ldots,m,\\
\lambda_i(1-x_i^T\widetilde A x_i+2\widetilde b^Tx_i-\widetilde b^T\widetilde A^{-1}\widetilde b)=0,\quad i=1,\ldots,m.
\end{gathered}
$$

<div class="translator-note" markdown="1">

**译注（变量代换的符号）：** 原书定义 $\widetilde b=Ab$，但 (8.12) 及后续 KKT 条件的一次项使用负号。按 (8.11) 的 $\|Ax_i+b\|_2^2$ 展开，一次项应为 $+2\widetilde b^Tx_i$；若采用后文的负号形式，则变量定义应为 $\widetilde b=-Ab$。

</div>

通过适当的仿射坐标变换，可以假设 $\widetilde A=I$、$\widetilde b=0$，即最小体积椭球是以原点为中心的单位球。于是 KKT <!-- pdf-page: 427 -->条件简化为

$$
\sum_{i=1}^m\lambda_i x_ix_i^T=I,\qquad
\sum_{i=1}^m\lambda_i x_i=0,\qquad
\lambda_i(1-x_i^Tx_i)=0,\quad i=1,\ldots,m,
$$

再加上可行性条件 $\|x_i\|_2\leq1$ 和 $\lambda_i\geq0$。对第一个等式两边取迹，并利用互补松弛性，还可得到 $\sum_{i=1}^m\lambda_i=n$。

在新坐标下，缩小后的椭球是以原点为中心、半径为 $1/n$ 的球。需要证明

$$
\|x\|_2\leq1/n\quad\Longrightarrow\quad x\in C=\mathbf{conv}\{x_1,\ldots,x_m\}.
$$

假设 $\|x\|_2\leq1/n$。由 KKT 条件可知，

$$
x=\sum_{i=1}^m\lambda_i(x^Tx_i)x_i
=\sum_{i=1}^m\lambda_i(x^Tx_i+1/n)x_i
=\sum_{i=1}^m\mu_i x_i,
\tag{8.13}
$$

其中 $\mu_i=\lambda_i(x^Tx_i+1/n)$。由 Cauchy-Schwartz 不等式可得

$$
\mu_i=\lambda_i(x^Tx_i+1/n)
\geq\lambda_i(-\|x\|_2\|x_i\|_2+1/n)
\geq\lambda_i(-1/n+1/n)=0.
$$

此外，

$$
\sum_{i=1}^m\mu_i=\sum_{i=1}^m\lambda_i(x^Tx_i+1/n)=\sum_{i=1}^m\lambda_i/n=1.
$$

结合 (8.13)，这表明 $x$ 是 $x_1,\ldots,x_m$ 的凸组合，因此 $x\in C$。

#### 对称集合的 Löwner-John 椭球逼近效果

若集合 $C$ 关于某点 $x_0$ 对称，因子 $1/n$ 可以改进为 $1/\sqrt n$：

$$
x_0+(1/\sqrt n)(\mathcal{E}_{\mathrm{lj}}-x_0)\subseteq C\subseteq\mathcal{E}_{\mathrm{lj}}.
$$

因子 $1/\sqrt n$ 同样是紧的。立方体

$$
C=\{x\in\mathbf{R}^n\mid-\mathbf{1}\preceq x\preceq\mathbf{1}\}
$$

的 Löwner-John 椭球是半径为 $\sqrt n$ 的球。将它缩小至原来的 $1/\sqrt n$，就得到一个包含在 $C$ 内的球，它在 $x=\pm e_i$ 处与边界相接。

#### 用二次范数逼近一个范数

设 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的任意范数，$C=\{x\mid\|x\|\leq1\}$ 是它的单位球。设 $\mathcal{E}_{\mathrm{lj}}=\{x\mid x^TAx\leq1\}$，其中 $A\in\mathbf{S}_{++}^n$，为 $C$ 的 Löwner-John 椭球。由于 $C$ 关于原点对称，上面的结果表明 $(1/\sqrt n)\mathcal{E}_{\mathrm{lj}}\subseteq C\subseteq\mathcal{E}_{\mathrm{lj}}$。用 $\|\cdot\|_{\mathrm{lj}}$ 表示二次范数

$$
\|z\|_{\mathrm{lj}}=(z^TAz)^{1/2},
$$

<!-- pdf-page: 428 -->

它的单位球为 $\mathcal{E}_{\mathrm{lj}}$。包含关系 $(1/\sqrt n)\mathcal{E}_{\mathrm{lj}}\subseteq C\subseteq\mathcal{E}_{\mathrm{lj}}$ 等价于对所有 $z\in\mathbf{R}^n$ 都成立的不等式

$$
\|z\|_{\mathrm{lj}}\leq\|z\|\leq\sqrt n\,\|z\|_{\mathrm{lj}}.
$$

换句话说，二次范数 $\|\cdot\|_{\mathrm{lj}}$ 在因子 $\sqrt n$ 的范围内逼近范数 $\|\cdot\|$。特别地，$\mathbf{R}^n$ 上的任意范数都能由某个二次范数在因子 $\sqrt n$ 的范围内逼近。

### 8.4.2 最大体积内接椭球

现在考虑求位于凸集 $C$ 内的最大体积椭球，假设 $C$ 有界且内部非空。为表述这个问题，将椭球参数化为单位球在仿射变换下的像，即

$$
\mathcal{E}=\{Bu+d\mid\|u\|_2\leq1\}.
$$

同样，可以假设 $B\in\mathbf{S}_{++}^n$，于是体积与 $\det B$ 成正比。求解凸优化问题

$$
\begin{array}{ll}
\text{最大化} & \log\det B\\
\text{约束条件} & \displaystyle\sup_{\|u\|_2\leq1}I_C(Bu+d)\leq0,
\end{array}
\tag{8.14}
$$

就能求出 $C$ 内的最大体积椭球，其中变量为 $B\in\mathbf{S}^n$ 和 $d\in\mathbf{R}^n$，隐含约束为 $B\succ0$。

#### 多面体内的最大体积椭球

考虑 $C$ 为由一组线性不等式描述的多面体的情况：

$$
C=\{x\mid a_i^Tx\leq b_i,\ i=1,\ldots,m\}.
$$

为应用 (8.14)，先把约束写成更方便的形式：

$$
\begin{aligned}
\sup_{\|u\|_2\leq1}I_C(Bu+d)\leq0
&\quad\Longleftrightarrow\quad\sup_{\|u\|_2\leq1}a_i^T(Bu+d)\leq b_i,\quad i=1,\ldots,m\\
&\quad\Longleftrightarrow\quad\|Ba_i\|_2+a_i^Td\leq b_i,\quad i=1,\ldots,m.
\end{aligned}
$$

因此，可以把 (8.14) 写成变量为 $B$ 和 $d$ 的凸优化问题：

$$
\begin{array}{ll}
\text{最小化} & \log\det B^{-1}\\
\text{约束条件} & \|Ba_i\|_2+a_i^Td\leq b_i,\quad i=1,\ldots,m.
\end{array}
\tag{8.15}
$$

#### 椭球交集内的最大体积椭球

也可以求出位于 $m$ 个椭球 $\mathcal{E}_1,\ldots,\mathcal{E}_m$ 交集内的最大体积椭球 $\mathcal{E}$。将 $\mathcal{E}$ 表示为 $\mathcal{E}=\{Bu+d\mid\|u\|_2\leq1\}$，其中 $B\in\mathbf{S}_{++}^n$，其余椭球用凸二次不等式描述：

$$
\mathcal{E}_i=\{x\mid x^TA_ix+2b_i^Tx+c_i\leq0\},\qquad i=1,\ldots,m,
$$

<!-- pdf-page: 429 -->

其中 $A_i\in\mathbf{S}_{++}^n$。先推导 $\mathcal{E}\subseteq\mathcal{E}_i$ 成立的条件。该包含关系成立当且仅当

$$
\begin{aligned}
&\sup_{\|u\|_2\leq1}\bigl((d+Bu)^TA_i(d+Bu)+2b_i^T(d+Bu)+c_i\bigr)\\
&\quad=d^TA_id+2b_i^Td+c_i+\sup_{\|u\|_2\leq1}\bigl(u^TBA_iBu+2(A_id+b_i)^TBu\bigr)\\
&\quad\leq0.
\end{aligned}
$$

根据 §B.1，

$$
\sup_{\|u\|_2\leq1}\bigl(u^TBA_iBu+2(A_id+b_i)^TBu\bigr)\leq-(d^TA_id+2b_i^Td+c_i)
$$

当且仅当存在 $\lambda_i\geq0$，使

$$
\begin{bmatrix}
-\lambda_i-d^TA_id-2b_i^Td-c_i & (A_id+b_i)^TB\\
B(A_id+b_i) & \lambda_i I-BA_iB
\end{bmatrix}\succeq0.
$$

因此，求解问题

$$
\begin{array}{ll}
\text{最小化} & \log\det B^{-1}\\
\text{约束条件} & \begin{bmatrix}
-\lambda_i-d^TA_id-2b_i^Td-c_i & (A_id+b_i)^TB\\
B(A_id+b_i) & \lambda_i I-BA_iB
\end{bmatrix}\succeq0,\quad i=1,\ldots,m,
\end{array}
$$

就能求出包含在 $\mathcal{E}_1,\ldots,\mathcal{E}_m$ 中的最大体积椭球，其中变量为 $B\in\mathbf{S}^n$、$d\in\mathbf{R}^n$ 和 $\lambda\in\mathbf{R}^m$。等价地，可以求解

$$
\begin{array}{ll}
\text{最小化} & \log\det B^{-1}\\
\text{约束条件} & \begin{bmatrix}
-\lambda_i-c_i+b_i^TA_i^{-1}b_i & 0 & (d+A_i^{-1}b_i)^T\\
0 & \lambda_i I & B\\
d+A_i^{-1}b_i & B & A_i^{-1}
\end{bmatrix}\succeq0,\quad i=1,\ldots,m.
\end{array}
$$

#### 椭球内逼近的效果

最大体积内接椭球也有与 Löwner-John 椭球类似的逼近效果结论。若 $C\subseteq\mathbf{R}^n$ 为凸、有界且内部非空，则将最大体积内接椭球以中心为基准放大 $n$ 倍，就能覆盖集合 $C$。若集合 $C$ 关于某点对称，因子 $n$ 可以改进为 $\sqrt n$。图 8.4 给出了一个例子。

### 8.4.3 极值体积椭球的仿射不变性

Löwner-John 椭球和最大体积内接椭球都具有*仿射不变性*。若 $\mathcal{E}_{\mathrm{lj}}$ 是 $C$ 的 Löwner-John 椭球，且 $T\in\mathbf{R}^{n\times n}$ 非奇异，那么 $TC$ 的 Löwner-John 椭球就是 $T\mathcal{E}_{\mathrm{lj}}$。最大体积内接椭球也有类似结论。

<p id="ellipsoid-affine-proof-start" markdown="1">为证明这个结果，设 $\mathcal{E}$ 是任意覆盖 $C$ 的椭球。那么椭球 $T\mathcal{E}$ 覆盖 $TC$。反过来也成立：每个覆盖 $TC$ 的椭球都具有</p>

<!-- pdf-page: 430 -->

<figure id="fig-8-4" data-figure="8.4" data-no-english-text="true" data-reader-after="ellipsoid-affine-proof-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-4.png" alt="多边形中有一个灰色最大体积内接椭圆，将它以中心为基准放大两倍得到外侧椭圆，覆盖整个多边形" data-source-page="430" data-source-rect="246,121,431,273">
<figcaption>图 8.4 多面体 $\mathcal{P}$ 的最大体积内接椭球，以阴影表示。外侧椭圆是将内侧椭球以其中心为基准放大 $n=2$ 倍后的边界。可以保证放大后的椭球覆盖 $\mathcal{P}$。</figcaption>
</figure>

<p id="ellipsoid-affine-proof-end" markdown="1" data-reader-continue="ellipsoid-affine-proof-start">$T\mathcal{E}$ 的形式，其中 $\mathcal{E}$ 是覆盖 $C$ 的椭球。换句话说，关系 $\widetilde{\mathcal{E}}=T\mathcal{E}$ 建立了覆盖 $TC$ 的椭球与覆盖 $C$ 的椭球之间的一一对应。而且，对应椭球的体积之比都为 $|\det T|$。因此，特别地，若 $\mathcal{E}$ 在所有覆盖 $C$ 的椭球中体积最小，那么 $T\mathcal{E}$ 在所有覆盖 $TC$ 的椭球中也体积最小。</p>

## 8.5 求中心

### 8.5.1 Chebyshev 中心

设 $C\subseteq\mathbf{R}^n$ 有界且内部非空，$x\in C$。点 $x\in C$ 的*深度*定义为

$$
\mathbf{depth}(x,C)=\mathbf{dist}(x,\mathbf{R}^n\setminus C),
$$

即它到 $C$ 外部最近点的距离。深度给出了以 $x$ 为中心、位于 $C$ 内的最大球的半径。集合 $C$ 的 *Chebyshev 中心*定义为 $C$ 中任意一个深度最大的点：

$$
x_{\mathrm{cheb}}(C)=\operatorname*{argmax}\mathbf{depth}(x,C)
=\operatorname*{argmax}\mathbf{dist}(x,\mathbf{R}^n\setminus C).
$$

Chebyshev 中心是 $C$ 内部离 $C$ 外部最远的点，也是位于 $C$ 内的最大球的球心。图 8.5 给出了一个例子，其中 $C$ 是多面体，采用欧几里得范数。

<!-- pdf-page: 431 -->

<figure id="fig-8-5" data-figure="8.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-5.png" alt="多边形中的最大内接欧几里得球以浅灰圆表示，圆心以小空心圆标出并标为 x_cheb" data-source-page="431" data-source-rect="192,121,378,276">
<figcaption>图 8.5 欧几里得范数下，多面体 $C$ 的 Chebyshev 中心。中心 $x_{\mathrm{cheb}}$ 是 $C$ 内部最深的点，意思是它到 $C$ 的外部（即补集）的距离最远。中心 $x_{\mathrm{cheb}}$ 也是包含在 $C$ 内的最大欧几里得球（浅色阴影区域）的球心。</figcaption>
</figure>

#### 凸集的 Chebyshev 中心

当集合 $C$ 为凸时，深度对 $x\in C$ 是凹函数，因此计算 Chebyshev 中心是一个凸优化问题（见习题 8.5）。具体来说，设 $C\subseteq\mathbf{R}^n$ 由一组凸不等式定义：

$$
C=\{x\mid f_1(x)\leq0,\ldots,f_m(x)\leq0\}.
$$

求解问题

$$
\begin{array}{ll}
\text{最大化} & R\\
\text{约束条件} & g_i(x,R)\leq0,\quad i=1,\ldots,m,
\end{array}
\tag{8.16}
$$

就能求出一个 Chebyshev 中心，其中 $g_i$ 定义为

$$
g_i(x,R)=\sup_{\|u\|\leq1}f_i(x+Ru).
$$

问题 (8.16) 是凸优化问题，因为每个函数 $g_i$ 都是一族关于 $x$ 和 $R$ 的凸函数的逐点最大值，因此为凸。不过，计算 $g_i$ 的值需要以数值方法或解析方法求解一个凸函数最大化问题，这可能很困难。实际中，只有在函数 $g_i$ 容易计算时，才能求出 Chebyshev 中心。

#### 多面体的 Chebyshev 中心

设 $C$ 由一组线性不等式 $a_i^Tx\leq b_i$，$i=1,\ldots,m$，定义。我们有

$$
g_i(x,R)=\sup_{\|u\|\leq1}a_i^T(x+Ru)-b_i=a_i^Tx+R\|a_i\|_*-b_i
$$

<!-- pdf-page: 432 -->

当 $R\geq0$ 时成立，因此 Chebyshev 中心可以通过求解 LP

$$
\begin{array}{ll}
\text{最大化} & R\\
\text{约束条件} & a_i^Tx+R\|a_i\|_*\leq b_i,\quad i=1,\ldots,m\\
& R\geq0
\end{array}
$$

得到，其中变量为 $x$ 和 $R$。

#### 椭球交集的欧几里得 Chebyshev 中心

设 $C$ 是由二次不等式定义的 $m$ 个椭球的交集：

$$
C=\{x\mid x^TA_ix+2b_i^Tx+c_i\leq0,\ i=1,\ldots,m\},
$$

其中 $A_i\in\mathbf{S}_{++}^n$。有

$$
\begin{aligned}
g_i(x,R)&=\sup_{\|u\|_2\leq1}\bigl((x+Ru)^TA_i(x+Ru)+2b_i^T(x+Ru)+c_i\bigr)\\
&=x^TA_ix+2b_i^Tx+c_i+\sup_{\|u\|_2\leq1}\bigl(R^2u^TA_iu+2R(A_ix+b_i)^Tu\bigr).
\end{aligned}
$$

根据 §B.1，$g_i(x,R)\leq0$ 当且仅当存在 $\lambda_i$，使矩阵不等式

$$
\begin{bmatrix}
-x^TA_ix_i-2b_i^Tx-c_i-\lambda_i & R(A_ix+b_i)^T\\
R(A_ix+b_i) & \lambda_i I-R^2A_i
\end{bmatrix}\succeq0
\tag{8.17}
$$

成立。利用这个结果，可以将 Chebyshev 中心问题写成

$$
\begin{array}{ll}
\text{最大化} & R\\
\text{约束条件} & \begin{bmatrix}
-\lambda_i-c_i+b_i^TA_i^{-1}b_i & 0 & (x+A_i^{-1}b_i)^T\\
0 & \lambda_i I & RI\\
x+A_i^{-1}b_i & RI & A_i^{-1}
\end{bmatrix}\succeq0,\quad i=1,\ldots,m.
\end{array}
$$

这是一个变量为 $R$、$\lambda$ 和 $x$ 的 SDP。注意，LMI 约束中关于 $A_i^{-1}$ 的 Schur 补等于 (8.17) 的左端。

<div class="translator-note" markdown="1">

**译注（矩阵不等式的记号）：** (8.17) 左上角的 $-x^TA_ix_i$ 按前一式展开应为 $-x^TA_ix$，原书多出一个下标。后面 SDP 中关于 $A_i^{-1}$ 的 Schur 补，其非对角块带负号；它经 $\operatorname{\mathbf{diag}}(1,-I)$ 合同变换后，才得到 (8.17) 的正号形式。因此两者给出等价的半正定约束，并非逐项相等。

</div>

### 8.5.2 最大体积椭球中心

集合 $C\subseteq\mathbf{R}^n$ 的 Chebyshev 中心 $x_{\mathrm{cheb}}$，是位于 $C$ 内的最大球的球心。推广这一思路，将 $C$ 的*最大体积椭球中心*定义为位于 $C$ 内的最大体积椭球的中心，记为 $x_{\mathrm{mve}}$。图 8.6 给出了 $C$ 为多面体时的一个例子。

当 $C$ 由一组线性不等式定义时，求解问题 (8.15)，就能方便地计算最大体积椭球中心。（变量 $d\in\mathbf{R}^n$ 的最优值就是 $x_{\mathrm{mve}}$。）由于 $C$ 内的最大体积椭球具有仿射不变性，最大体积椭球中心也具有仿射不变性。

<!-- pdf-page: 433 -->

<figure id="fig-8-6" data-figure="8.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-6.png" alt="多边形内的最大体积椭球以浅灰椭圆表示，椭圆中心用小空心圆标出并标为 x_mve" data-source-page="433" data-source-rect="192,121,378,276">
<figcaption>图 8.6 浅色阴影椭球表示包含在集合 $C$ 内的最大体积椭球，$C$ 是图 8.5 中的同一个多面体。它的中心 $x_{\mathrm{mve}}$ 就是 $C$ 的最大体积椭球中心。</figcaption>
</figure>

### 8.5.3 一组不等式的解析中心

一组凸不等式和线性等式

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad Fx=g
$$

的*解析中心*（analytic center）$x_{\mathrm{ac}}$，定义为以下凸问题的一个最优点：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle-\sum_{i=1}^m\log(-f_i(x))\\
\text{约束条件} & Fx=g,
\end{array}
\tag{8.18}
$$

其中变量为 $x\in\mathbf{R}^n$，隐含约束为 $f_i(x)<0$，$i=1,\ldots,m$。(8.18) 的目标函数称为这组不等式对应的*对数障碍函数*。这里假设对数障碍函数的定义域与等式定义的仿射集相交，即严格不等式系统

$$
f_i(x)<0,\quad i=1,\ldots,m,\qquad Fx=g
$$

可行。如果可行集

$$
C=\{x\mid f_i(x)<0,\ i=1,\ldots,m,\ Fx=g\}
$$

有界，那么对数障碍函数在该可行集上有下界。

当 $x$ 严格可行，即 $Fx=g$，且对 $i=1,\ldots,m$ 都有 $f_i(x)<0$ 时，可以把 $-f_i(x)$ 解释为第 $i$ 个不等式的余量（margin）或松弛量（slack）。解析中心 $x_{\mathrm{ac}}$ 是在等式约束 $Fx=g$ 和隐含约束 $f_i(x)<0$ 下，使这些松弛量或余量的乘积（或几何平均）最大的点。

解析中心并不是这些不等式和等式所描述的集合 $C$ 的函数；两组不等式和等式可以定义同一个集合，却具有不同的解析中心。尽管如此，人们仍常常非正式地使用<!-- pdf-page: 434 -->“集合 $C$ 的解析中心”一词，来指某组定义该集合的具体等式和不等式的解析中心。

不过，解析中心不依赖于仿射坐标变换。对不等式函数作正比例缩放，或对等式约束作任意重新参数化，也不会改变解析中心。换句话说，若 $\widetilde F$ 和 $\widetilde g$ 满足：$\widetilde Fx=\widetilde g$ 当且仅当 $Fx=g$，并且 $\alpha_1,\ldots,\alpha_m>0$，那么

$$
\alpha_i f_i(x)\leq0,\quad i=1,\ldots,m,\qquad\widetilde Fx=\widetilde g
$$

的解析中心与

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad Fx=g
$$

的解析中心相同（见习题 8.17）。

#### 一组线性不等式的解析中心

一组线性不等式

$$
a_i^Tx\leq b_i,\qquad i=1,\ldots,m,
$$

的解析中心，是无约束最小化问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle-\sum_{i=1}^m\log(b_i-a_i^Tx),
\end{array}
\tag{8.19}
$$

的解，隐含约束为 $b_i-a_i^Tx>0$，$i=1,\ldots,m$。如果这些线性不等式定义的多面体有界，那么对数障碍函数有下界且严格凸，所以解析中心唯一。（见习题 4.2。）

一组线性不等式的解析中心可以作如下几何解释。由于解析中心不受约束函数正比例缩放的影响，不失一般性，可以假设 $\|a_i\|_2=1$。这时，松弛量 $b_i-a_i^Tx$ 就是到超平面 $\mathcal{H}_i=\{x\mid a_i^Tx=b_i\}$ 的距离。因此，解析中心 $x_{\mathrm{ac}}$ 是使到这些定义超平面的距离乘积最大的点。

#### 由线性不等式的解析中心得到内外椭球

一组线性不等式的解析中心隐式地定义了一个内接椭球和一个覆盖椭球。它们由对数障碍函数

$$
-\sum_{i=1}^m\log(b_i-a_i^Tx)
$$

在解析中心处的 Hessian 矩阵定义，即

$$
H=\sum_{i=1}^m d_i^2a_i a_i^T,\qquad
d_i=\frac{1}{b_i-a_i^Tx_{\mathrm{ac}}},\quad i=1,\ldots,m.
$$

有 $\mathcal{E}_{\mathrm{inner}}\subseteq\mathcal{P}\subseteq\mathcal{E}_{\mathrm{outer}}$，其中

$$
\begin{aligned}
\mathcal{P}&=\{x\mid a_i^Tx\leq b_i,\ i=1,\ldots,m\},\\
\mathcal{E}_{\mathrm{inner}}&=\{x\mid(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})\leq1\},\\
\mathcal{E}_{\mathrm{outer}}&=\{x\mid x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})\leq m(m-1)\}.
\end{aligned}
$$

<!-- pdf-page: 435 -->

<figure id="fig-8-7" data-figure="8.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-7.png" alt="同一多边形内部有五条虚线等值曲线，中央的灰色椭圆包围标为 x_ac 的解析中心" data-source-page="435" data-source-rect="192,121,378,276">
<figcaption>图 8.7 虚线表示定义图 8.5 中多面体 $C$ 的不等式所对应的对数障碍函数的五条等值曲线。标为 $x_{\mathrm{ac}}$ 的点是对数障碍函数的极小点，也就是这些不等式的解析中心。内侧椭球 $\mathcal{E}_{\mathrm{inner}}=\{x\mid(x-x_{\mathrm{ac}})H(x-x_{\mathrm{ac}})\leq1\}$ 以阴影表示，其中 $H$ 是对数障碍函数在 $x_{\mathrm{ac}}$ 处的 Hessian 矩阵。</figcaption>
</figure>

<div class="translator-note" markdown="1">

**译注（图注中的二次型）：** 原图注中第一个 $(x-x_{\mathrm{ac}})$ 后漏印转置符号。这里的椭球应按前文定义和随后证明中的二次型 $(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})$ 理解。

</div>

这个结果比最大体积内接椭球的结果弱，后者放大 $n$ 倍就能覆盖该多面体。对数障碍函数的 Hessian 矩阵定义的内外椭球之间，缩放因子则为 $(m(m-1))^{1/2}$，它总是不小于 $n$。

为证明 $\mathcal{E}_{\mathrm{inner}}\subseteq\mathcal{P}$，设 $x\in\mathcal{E}_{\mathrm{inner}}$，即

$$
(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})=\sum_{i=1}^m\bigl(d_i a_i^T(x-x_{\mathrm{ac}})\bigr)^2\leq1.
$$

这意味着

$$
a_i^T(x-x_{\mathrm{ac}})\leq1/d_i=b_i-a_i^Tx_{\mathrm{ac}},\qquad i=1,\ldots,m,
$$

因此对 $i=1,\ldots,m$，有 $a_i^Tx\leq b_i$。（这里没有用到 $x_{\mathrm{ac}}$ 是解析中心这一事实，因此将 $x_{\mathrm{ac}}$ 替换为任意严格可行点，这个结果仍然成立。）

为证明 $\mathcal{P}\subseteq\mathcal{E}_{\mathrm{outer}}$，需要用到 $x_{\mathrm{ac}}$ 是解析中心，因此对数障碍函数的梯度为零这一事实：

$$
\sum_{i=1}^m d_i a_i=0.
$$

现在假设 $x\in\mathcal{P}$。则

$$
\begin{aligned}
&(x-x_{\mathrm{ac}})^TH(x-x_{\mathrm{ac}})\\
&\quad=\sum_{i=1}^m\bigl(d_i a_i^T(x-x_{\mathrm{ac}})\bigr)^2
\end{aligned}
$$

<!-- pdf-page: 436 -->

$$
\begin{aligned}
&\quad=\sum_{i=1}^m d_i^2\bigl(1/d_i-a_i^T(x-x_{\mathrm{ac}})\bigr)^2-m\\
&\quad=\sum_{i=1}^m d_i^2(b_i-a_i^Tx)^2-m\\
&\quad\leq\left(\sum_{i=1}^m d_i(b_i-a_i^Tx)\right)^2-m\\
&\quad=\left(\sum_{i=1}^m d_i(b_i-a_i^Tx_{\mathrm{ac}})+\sum_{i=1}^m d_i a_i^T(x_{\mathrm{ac}}-x)\right)^2-m\\
&\quad=m^2-m,
\end{aligned}
$$

这表明 $x\in\mathcal{E}_{\mathrm{outer}}$。（第二个等号来自 $\sum_{i=1}^m d_i a_i=0$。不等号来自对 $y\succeq0$ 成立的 $\sum_{i=1}^m y_i^2\leq(\sum_{i=1}^m y_i)^2$。最后一个等号来自 $\sum_{i=1}^m d_i a_i=0$ 以及 $d_i$ 的定义。）

#### 线性矩阵不等式的解析中心

如果在锥 $K$ 上定义一个对数函数，那么解析中心的定义就可以推广到由关于 $K$ 的广义不等式描述的集合。例如，线性矩阵不等式

$$
x_1A_1+x_2A_2+\cdots+x_nA_n\preceq B
$$

的解析中心定义为问题

$$
\begin{array}{ll}
\text{最小化} & -\log\det(B-x_1A_1-\cdots-x_nA_n)
\end{array}
$$

的解。

## 8.6 分类

在模式识别和分类问题中，给定 $\mathbf{R}^n$ 中的两个点集 $\{x_1,\ldots,x_N\}$ 和 $\{y_1,\ldots,y_M\}$，希望从给定的函数族中找出一个函数 $f:\mathbf{R}^n\to\mathbf{R}$，使它在第一个集合上为正，在第二个集合上为负，即

$$
f(x_i)>0,\quad i=1,\ldots,N,\qquad f(y_i)<0,\quad i=1,\ldots,M.
$$

若这些不等式成立，就说 $f$ 或它的零水平集 $\{x\mid f(x)=0\}$ 将这两个点集*分离*、*分类*或*判别*。有时也考虑*弱分离*，即这些不等式的非严格形式成立。

<!-- pdf-page: 437 -->

<figure id="fig-8-8" data-figure="8.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-8.png" alt="一条斜直线将左上方的实心点与右下方的空心点完全分开，表示仿射分类函数的零水平集" data-source-page="437" data-source-rect="201,120,370,303">
<figcaption>图 8.8 点 $x_1,\ldots,x_N$ 以空心圆表示，点 $y_1,\ldots,y_M$ 以实心圆表示。用一个仿射函数 $f$ 对这两个点集进行分类，其零水平集（一条直线）将两者分离。</figcaption>
</figure>

### 8.6.1 线性判别

在*线性判别*中，要寻找一个能将这些点分类的仿射函数 $f(x)=a^Tx-b$，即

$$
a^Tx_i-b>0,\quad i=1,\ldots,N,\qquad a^Ty_i-b<0,\quad i=1,\ldots,M.
\tag{8.20}
$$

从几何上说，就是寻找一个能将两个点集分离的超平面。由于严格不等式 (8.20) 关于 $a$ 和 $b$ 齐次，它们可行当且仅当下面这组以 $a$、$b$ 为变量的非严格线性不等式可行：

$$
a^Tx_i-b\geq1,\quad i=1,\ldots,N,\qquad a^Ty_i-b\leq-1,\quad i=1,\ldots,M.
\tag{8.21}
$$

图 8.8 展示了两个点集和一个线性判别函数的简单例子。

#### 线性判别的择一条件

严格不等式组 (8.20) 的强择一系统，是存在 $\lambda$、$\widetilde\lambda$，使

$$
\lambda\succeq0,\quad\widetilde\lambda\succeq0,\quad(\lambda,\widetilde\lambda)\ne0,\quad
\sum_{i=1}^N\lambda_i x_i=\sum_{i=1}^M\widetilde\lambda_i y_i,\quad
\mathbf{1}^T\lambda=\mathbf{1}^T\widetilde\lambda
\tag{8.22}
$$

成立（见 §5.8.3）。利用第三个和最后一个条件，可以把这些择一条件写成

$$
\lambda\succeq0,\quad\mathbf{1}^T\lambda=1,\quad
\widetilde\lambda\succeq0,\quad\mathbf{1}^T\widetilde\lambda=1,\quad
\sum_{i=1}^N\lambda_i x_i=\sum_{i=1}^M\widetilde\lambda_i y_i
$$

<!-- pdf-page: 438 -->

（除以正数 $\mathbf{1}^T\lambda$，归一化后的 $\lambda$ 和 $\widetilde\lambda$ 仍沿用原记号）。这些条件有简单的几何解释：存在一个点，同时属于 $\{x_1,\ldots,x_N\}$ 和 $\{y_1,\ldots,y_M\}$ 的凸包。换句话说，两个点集能够被线性判别，即被一个仿射函数判别，当且仅当它们的凸包不相交。前面已经多次见过这个结果。

#### 鲁棒线性判别

存在一个仿射分类函数 $f(x)=a^Tx-b$，等价于定义它的变量 $a$ 和 $b$ 满足一组线性不等式。如果两个集合可以被线性判别，那么能够判别它们的仿射函数组成一个多面体，可以从中选择一个使某种鲁棒性指标最优的函数。例如，可以寻找一个函数，使它在点 $x_i$ 处的正值与在点 $y_i$ 处的负值之间有尽可能大的“间隔”。为此，必须对 $a$ 和 $b$ 作归一化，否则只要用一个正常数同时缩放 $a$ 和 $b$，就能把函数值间隔任意增大。由此得到问题

$$
\begin{array}{ll}
\text{最大化} & t\\
\text{约束条件} & a^Tx_i-b\geq t,\quad i=1,\ldots,N\\
& a^Ty_i-b\leq-t,\quad i=1,\ldots,M\\
& \|a\|_2\leq1,
\end{array}
\tag{8.23}
$$

其中变量为 $a$、$b$ 和 $t$。这个凸问题的目标为线性函数，约束包括线性不等式和一个二次不等式；其最优值 $t^\star$ 为正，当且仅当这两个点集能够被线性判别。在这种情况下，不等式 $\|a\|_2\leq1$ 在最优点处总是取等号，即 $\|a^\star\|_2=1$。（见习题 8.23。）

鲁棒线性判别问题 (8.23) 有简单的几何解释。若 $\|a\|_2=1$（任意最优点都是如此），那么 $a^Tx_i-b$ 就是点 $x_i$ 到分离超平面 $\mathcal{H}=\{z\mid a^Tz=b\}$ 的欧几里得距离。类似地，$b-a^Ty_i$ 是点 $y_i$ 到该超平面的距离。因此，问题 (8.23) 找到的是一个将两个点集分离，并且到这两个集合的距离最大的超平面。换句话说，它找到了将两个集合分开的最宽条带。

图 8.9 中的例子提示，最优值 $t^\star$，也就是条带宽度的一半，实际上等于两个点集凸包之间距离的一半。从鲁棒线性判别问题 (8.23) 的对偶问题可以清楚地看出这一点。对最小化 $-t$ 的问题，拉格朗日函数为

$$
-t+\sum_{i=1}^N u_i(t+b-a^Tx_i)+\sum_{i=1}^M v_i(t-b+a^Ty_i)+\lambda(\|a\|_2-1).
$$

对 $b$ 和 $t$ 最小化，得到条件 $\mathbf{1}^Tu=1/2$、$\mathbf{1}^Tv=1/2$。当这些条件成立时，有

$$
g(u,v,\lambda)=\inf_a\left(a^T\left(\sum_{i=1}^M v_i y_i-\sum_{i=1}^N u_i x_i\right)+\lambda\|a\|_2-\lambda\right)
$$

<!-- pdf-page: 439 -->

<figure id="fig-8-9" data-figure="8.9" data-no-english-text="true" data-reader-after="robust-classification-dual-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-9.png" alt="两条平行虚线之间的浅灰条带分离实心点与空心点，部分点恰位于条带边界，中央实线是分类边界" data-source-page="439" data-source-rect="200,119,370,308">
<figcaption>图 8.9 通过求解鲁棒线性判别问题 (8.23)，我们找到一个使两个点集的函数值间隔最大的仿射函数，同时对函数的线性部分施加归一化界限。从几何上看，我们在寻找能将这两个点集分开的最宽条带。</figcaption>
</figure>

$$
=\begin{cases}
-\lambda & \displaystyle\left\|\sum_{i=1}^M v_i y_i-\sum_{i=1}^N u_i x_i\right\|_2\leq\lambda\\
-\infty & \text{其他情况}.
\end{cases}
$$

于是对偶问题可以写成

$$
\begin{array}{ll}
\text{最大化} & \displaystyle-\left\|\sum_{i=1}^M v_i y_i-\sum_{i=1}^N u_i x_i\right\|_2\\
\text{约束条件} & u\succeq0,\quad\mathbf{1}^Tu=1/2\\
& v\succeq0,\quad\mathbf{1}^Tv=1/2.
\end{array}
$$

<p id="robust-classification-dual-end" markdown="1">可以把 $2\sum_{i=1}^N u_i x_i$ 解释为 $\{x_1,\ldots,x_N\}$ 的凸包中的一点，把 $2\sum_{i=1}^M v_i y_i$ 解释为 $\{y_1,\ldots,y_M\}$ 的凸包中的一点。对偶目标就是最小化这两点之间距离的一半，也就是求出两个集合凸包之间距离的一半。</p>

#### 支持向量分类器

当两个点集不能被线性分离时，可以寻找一个近似地将它们分类的仿射函数，例如使误分类点的数量最少的函数。遗憾的是，这通常是一个困难的组合优化问题。一种近似线性判别的启发式方法基于*支持向量分类器*（support vector classifier），下面介绍这种方法。

从可行性问题 (8.21) 出发，先引入非负变量 $u_1,\ldots,u_N$ 和 $v_1,\ldots,u_M$ 来放松约束，得到不等式

$$
a^Tx_i-b\geq1-u_i,\quad i=1,\ldots,N,\qquad
a^Ty_i-b\leq-(1-v_i),\quad i=1,\ldots,M.
\tag{8.24}
$$

<!-- pdf-page: 440 -->

<figure id="fig-8-10" data-figure="8.10" data-no-english-text="true" data-reader-after="lp-classification-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-10.png" alt="空心点与实心点的散点图中画出一条实线分类边界及其两侧距离很近的平行虚线；存在被误分类的点和位于条带内的点" data-source-page="440" data-source-rect="237,121,438,312">
<figcaption>图 8.10 通过线性规划进行近似线性判别。以空心圆表示的点 $x_1,\ldots,x_{50}$，无法与以实心圆表示的点 $y_1,\ldots,y_{50}$ 线性分离。实线所示的分类器通过求解 LP (8.25) 得到。这个分类器将一个点分错了类。虚线表示超平面 $a^Tz-b=\pm1$。有四个点被正确分类，但落在两条虚线定义的条带内。</figcaption>
</figure>

当 $u=v=0$ 时，就恢复了原约束；只要令 $u$ 和 $v$ 足够大，总能使这些不等式可行。可以把 $u_i$ 看作对约束 $a^Tx_i-b\geq1$ 违反程度的度量，$v_i$ 也类似。目标是找到 $a$、$b$，以及稀疏且非负的 $u$ 和 $v$，使不等式 (8.24) 成立。作为一种启发式方法，可以求解以下 LP，以最小化变量 $u_i$ 和 $v_i$ 的和：

$$
\begin{array}{ll}
\text{最小化} & \mathbf{1}^Tu+\mathbf{1}^Tv\\
\text{约束条件} & a^Tx_i-b\geq1-u_i,\quad i=1,\ldots,N\\
& a^Ty_i-b\leq-(1-v_i),\quad i=1,\ldots,M\\
& u\succeq0,\quad v\succeq0.
\end{array}
\tag{8.25}
$$

<p id="lp-classification-end" markdown="1">图 8.10 给出了一个例子。其中，仿射函数 $a^Tz-b$ 将 $100$ 个点中的 $1$ 个分错了类。不过要注意，当 $0<u_i<1$ 时，点 $x_i$ 被仿射函数 $a^Tz-b$ 正确分类，但仍违反不等式 $a^Tx_i-b\geq1$；$y_i$ 也类似。LP (8.25) 的目标函数，可以解释为以下数量之和的松弛：违反 $a^Tx_i-b\geq1$ 的点 $x_i$ 的数量，加上违反 $a^Ty_i-b\leq-1$ 的点 $y_i$ 的数量。换句话说，它松弛的是被函数 $a^Tz-b$ 误分类的点数，加上分类正确但位于条带 $-1<a^Tz-b<1$ 内的点数。</p>

<p id="svm-definition-start" markdown="1">更一般地，可以考虑误分类点数与条带 $\{z\mid-1\leq a^Tz-b\leq1\}$ 宽度之间的权衡，该宽度为 $2/\|a\|_2$。点集 $\{x_1,\ldots,x_N\}$、</p>

<!-- pdf-page: 441 -->

<figure id="fig-8-11" data-figure="8.11" data-no-english-text="true" data-reader-after="svm-classification-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-11.png" alt="支持向量分类器的实线边界位于两条平行虚线之间；空心点和实心点分布在其两侧，若干点位于较宽的条带内" data-source-page="441" data-source-rect="183,121,385,311">
<figcaption>图 8.11 通过支持向量分类器进行近似线性判别，其中 $\gamma=0.1$。实线所示的支持向量分类器将三个点分错了类。有十五个点被正确分类，但位于由 $-1<a^Tz-b<1$ 定义、以两条虚线为边界的条带内。</figcaption>
</figure>

<p id="svm-definition-end" markdown="1" data-reader-continue="svm-definition-start">$\{y_1,\ldots,y_M\}$ 的标准支持向量分类器定义为以下问题的解：</p>

$$
\begin{array}{ll}
\text{最小化} & \|a\|_2+\gamma(\mathbf{1}^Tu+\mathbf{1}^Tv)\\
\text{约束条件} & a^Tx_i-b\geq1-u_i,\quad i=1,\ldots,N\\
& a^Ty_i-b\leq-(1-v_i),\quad i=1,\ldots,M\\
& u\succeq0,\quad v\succeq0.
\end{array}
$$

<p id="svm-classification-end" markdown="1">第一项与条带 $-1\leq a^Tz-b\leq1$ 宽度的倒数成正比。第二项的解释与上面相同，即它是误分类点数（包括条带内的点）的凸松弛。正参数 $\gamma$ 给出了误分类点数相对于条带宽度的权重；前者希望尽量小，后者希望尽量大。图 8.11 给出了一个例子。</p>

#### 通过 logistic 建模进行近似线性判别

对于无法线性分离的两个点集，另一种寻找近似分类仿射函数的方法，基于 §7.1.1 中介绍的 logistic 模型。首先用 logistic 模型拟合这两个点集。设 $z$ 是取值为 $0$ 或 $1$ 的随机变量，其分布通过以下形式的 logistic 模型，依赖于某个确定性的解释变量 $u\in\mathbf{R}^n$：

$$
\begin{aligned}
\mathbf{prob}(z=1)&=\exp(a^Tu-b)/(1+\exp(a^Tu-b))\\
\mathbf{prob}(z=0)&=1/(1+\exp(a^Tu-b)).
\end{aligned}
\tag{8.26}
$$

现在假设给定点集 $\{x_1,\ldots,x_N\}$ 和 $\{y_1,\ldots,y_M\}$ 来自这个 logistic 模型的样本。具体来说，$\{x_1,\ldots,x_N\}$ 是<!-- pdf-page: 442 -->$N$ 个 $z=1$ 的样本所对应的 $u$ 值，$\{y_1,\ldots,y_M\}$ 是 $M$ 个 $z=0$ 的样本所对应的 $u$ 值。（这里允许 $x_i=y_j$，而这种情况会使两个集合无法被判别。在 logistic 模型中，它仅仅表示有两个样本的解释变量值相同，但结果不同。）

可以根据观测到的样本作最大似然估计，求出 $a$ 和 $b$，具体是求解凸优化问题

$$
\begin{array}{ll}
\text{最小化} & -l(a,b),
\end{array}
\tag{8.27}
$$

其中变量为 $a$、$b$，$l$ 是对数似然函数

$$
\begin{aligned}
l(a,b)={}&\sum_{i=1}^N(a^Tx_i-b)\\
&-\sum_{i=1}^N\log(1+\exp(a^Tx_i-b))-\sum_{i=1}^M\log(1+\exp(a^Ty_i-b))
\end{aligned}
$$

（见 §7.1.1）。若两个点集可以线性分离，即存在 $a$、$b$，使 $a^Tx_i>b$、$a^Ty_i<b$，那么优化问题 (8.27) 无下界。

<div class="translator-note" markdown="1">

**译注（线性可分时的最优值）：** 对数似然满足 $l(a,b)\leq0$，所以 $-l(a,b)\geq0$。当两点集严格线性可分时，将分离参数 $a$、$b$ 同比放大，可以使 $-l(a,b)$ 趋于 $0$，但有限参数不能达到这个值。因此这里的下确界为 $0$ 而不能达到，原文“无下界”的说法不准确。

</div>

求出 $a$ 和 $b$ 的最大似然估计后，就可以为两个点集构造线性分类器 $f(x)=a^Tx-b$。这个分类器有如下性质：假设数据点确实由参数为 $a$ 和 $b$ 的 logistic 模型生成，那么在所有线性分类器中，它的误分类概率最小。超平面 $a^Tu=b$ 对应 $\mathbf{prob}(z=1)=1/2$ 的点，即两种结果等可能的点。图 8.12 给出了一个例子。

<div class="remark" id="remark-8-1" markdown="1">

**注 8.1 贝叶斯解释。** 设 $x$ 和 $z$ 是两个随机变量，分别在 $\mathbf{R}^n$ 和 $\{0,1\}$ 中取值。假设

$$
\mathbf{prob}(z=1)=\mathbf{prob}(z=0)=1/2,
$$

用 $p_0(x)$ 和 $p_1(x)$ 分别表示给定 $z=0$ 和 $z=1$ 时 $x$ 的条件概率密度。假设对某个 $a$ 和 $b$，$p_0$ 和 $p_1$ 满足

$$
\frac{p_1(x)}{p_0(x)}=e^{a^Tx-b}.
$$

许多常见分布都具有这个性质。例如，$p_0$ 和 $p_1$ 可以是 $\mathbf{R}^n$ 上两个协方差矩阵相同、均值不同的正态密度，也可以是 $\mathbf{R}_+^n$ 上的两个指数密度。

由 Bayes 公式可得

$$
\begin{aligned}
\mathbf{prob}(z=1\mid x=u)&=\frac{p_1(u)}{p_1(u)+p_0(u)}\\
\mathbf{prob}(z=0\mid x=u)&=\frac{p_0(u)}{p_1(u)+p_0(u)},
\end{aligned}
$$

从而得到

$$
\begin{aligned}
\mathbf{prob}(z=1\mid x=u)&=\frac{\exp(a^Tu-b)}{1+\exp(a^Tu-b)}\\
\mathbf{prob}(z=0\mid x=u)&=\frac{1}{1+\exp(a^Tu-b)}.
\end{aligned}
$$

<!-- pdf-page: 443 -->

<figure id="fig-8-12" data-figure="8.12" data-no-english-text="true" data-reader-after-container="remark-8-1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-12.png" alt="logistic 模型给出的实线分类边界与两条平行虚线穿过两组散点之间，实心点与空心点并非完全线性可分" data-source-page="443" data-source-rect="183,133,385,312">
<figcaption>图 8.12 通过 logistic 建模进行近似线性判别。以空心圆表示的点 $x_1,\ldots,x_{50}$，无法与以实心圆表示的点 $y_1,\ldots,y_{50}$ 线性分离。最大似然 logistic 模型给出了图中以深色直线表示的超平面，它只将两个点分错了类。两条虚线表示 $a^Tu-b=\pm1$；根据 logistic 模型，两种结果在各自对应的线上具有 73% 的概率。有三个点被正确分类，但位于两条虚线之间。</figcaption>
</figure>

因此，logistic 模型 (8.26) 可以解释为给定 $x=u$ 时 $z$ 的后验分布。

</div>

### 8.6.2 非线性判别

同样可以从给定的函数子空间中，寻找一个在一个集合上为正、在另一个集合上为负的非线性函数 $f$：

$$
f(x_i)>0,\quad i=1,\ldots,N,\qquad f(y_i)<0,\quad i=1,\ldots,M.
$$

只要 $f$ 关于定义它的参数是线性或仿射的，就可以用与线性判别完全相同的方法求解这些不等式。本节考察一些有趣的特殊情况。

#### 二次判别

设 $f$ 为二次函数：$f(x)=x^TPx+q^Tx+r$。参数 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$、$r\in\mathbf{R}$ 必须满足不等式

$$
\begin{aligned}
x_i^TPx_i+q^Tx_i+r&>0,\quad i=1,\ldots,N\\
y_i^TPy_i+q^Ty_i+r&<0,\quad i=1,\ldots,M,
\end{aligned}
$$

<!-- pdf-page: 444 -->

这是一组关于变量 $P$、$q$、$r$ 的严格线性不等式。与线性判别一样，由于 $f$ 关于 $P$、$q$ 和 $r$ 齐次，求解非严格可行性问题

$$
\begin{aligned}
x_i^TPx_i+q^Tx_i+r&\geq1,\quad i=1,\ldots,N\\
y_i^TPy_i+q^Ty_i+r&\leq-1,\quad i=1,\ldots,M,
\end{aligned}
$$

就能找到上述严格不等式的一个解。

分离曲面 $\{z\mid z^TPz+q^Tz+r=0\}$ 是二次曲面，两个分类区域

$$
\{z\mid z^TPz+q^Tz+r\leq0\},\qquad\{z\mid z^TPz+q^Tz+r\geq0\}
$$

由二次不等式定义。因此，求解二次判别问题，就等价于判断两个点集能否被一个二次曲面分离。

通过对 $P$、$q$ 和 $r$ 增加约束，可以对分离曲面或分类区域的形状施加条件。例如，可以要求 $P\prec0$，这意味着分离曲面为椭球面。更具体地说，要寻找一个椭球，使它包含所有点 $x_1,\ldots,x_N$，却不包含任何点 $y_1,\ldots,y_M$。这个二次判别问题可以作为 SDP 可行性问题来求解：

$$
\begin{array}{ll}
\text{求} & P,\ q,\ r\\
\text{约束条件} & x_i^TPx_i+q^Tx_i+r\geq1,\quad i=1,\ldots,N\\
& y_i^TPy_i+q^Ty_i+r\leq-1,\quad i=1,\ldots,M\\
& P\preceq-I,
\end{array}
$$

其中变量为 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$ 和 $r\in\mathbf{R}$。（这里利用关于 $P$、$q$、$r$ 的齐次性，将约束 $P\prec0$ 写成 $P\preceq-I$。）图 8.13 给出了一个例子。

#### 多项式判别

考虑 $\mathbf{R}^n$ 上次数小于或等于 $d$ 的多项式集合：

$$
f(x)=\sum_{i_1+\cdots+i_n\leq d}a_{i_1\cdots i_d}x_1^{i_1}\cdots x_n^{i_n}.
$$

求解一组以 $a_{i_1\cdots i_d}$ 为变量的线性不等式，就能判断两个集合 $\{x_1,\ldots,x_N\}$ 和 $\{y_1,\ldots,y_M\}$ 能否被这样的多项式分离。从几何上说，就是检查两个集合能否被一个代数曲面分离，该曲面由次数小于或等于 $d$ 的多项式定义。

进一步，求 $\mathbf{R}^n$ 上能分离两个点集的最低次数多项式，也可以通过拟凸规划求解，因为多项式的次数是其系数的拟凸函数。具体可以对 $d$ 作二分，每一步求解一个可行性线性规划。图 8.14 给出了一个例子。

<!-- pdf-page: 445 -->

<figure id="fig-8-13" data-figure="8.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-13.png" alt="一个倾斜椭圆包围全部空心点，并将周围全部实心点排除在外，表示具有负定二次项的分类边界" data-source-page="445" data-source-rect="184,146,385,312">
<figcaption>图 8.13 带有条件 $P\prec0$ 的二次判别。这意味着要寻找一个包含所有 $x_i$（以空心圆表示）、却不包含任何 $y_i$（以实心圆表示）的椭球。这个问题可以作为一个 SDP 可行性问题来求解。</figcaption>
</figure>

<figure id="fig-8-14" data-figure="8.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-14.png" alt="一条右侧向内凹的闭合曲线将中央空心点与周围实心点分离，曲线是四次多项式的零水平集" data-source-page="445" data-source-rect="193,424,376,600">
<figcaption>图 8.14 $\mathbf{R}^2$ 中的最低次数多项式判别。本例中，不存在能将点 $x_1,\ldots,x_N$（以空心圆表示）与点 $y_1,\ldots,y_M$（以实心圆表示）分离的三次多项式，但可以用一个四次多项式将它们分离，图中画出了这个多项式的零水平集。</figcaption>
</figure>

<!-- pdf-page: 446 -->

## 8.7 布置与选址

本节讨论以下问题的几个变体。给定 $\mathbf{R}^2$ 或 $\mathbf{R}^3$ 中的 $N$ 个点，以及一个必须用连线连接的点对列表。其中一些点的位置已经固定；任务是确定其余点的位置，即布置其余的点。目标是在满足一些附加位置约束的条件下，使衡量连线总长度的某个指标最小。

例如，可以把这些点看作某公司工厂或仓库的位置，把连线看作货物运输路线，目标就是寻找使总运输成本最小的选址。在另一个应用中，点表示集成电路上模块或单元的位置，连线表示连接一对单元的导线。此时的目标可能是布置各单元，使连接它们所需的导线总长度最小。

这个问题可以用一个具有 $N$ 个节点的无向图描述，节点代表这 $N$ 个点。每个节点对应一个变量 $x_i\in\mathbf{R}^k$，其中 $k=2$ 或 $k=3$，表示它的位置。问题是最小化

$$
\sum_{(i,j)\in\mathcal{A}}f_{ij}(x_i,x_j),
$$

其中 $\mathcal{A}$ 是图中所有连线的集合，$f_{ij}:\mathbf{R}^k\times\mathbf{R}^k\to\mathbf{R}$ 是弧 $(i,j)$ 对应的代价函数。（也可以对所有 $i$、$j$，或者对 $i<j$ 求和，只需在 $i$、$j$ 之间没有连接时令 $f_{ij}=0$。）一些坐标向量 $x_i$ 已给定，其余坐标为优化变量。只要函数 $f_{ij}$ 为凸，这就是一个凸优化问题。

### 8.7.1 线性设施选址问题

在最简单的情形下，弧 $(i,j)$ 的代价就是节点 $i$ 与 $j$ 之间的距离：$f_{ij}(x_i,x_j)=\|x_i-x_j\|$，即最小化

$$
\sum_{(i,j)\in\mathcal{A}}\|x_i-x_j\|.
$$

可以采用任意范数，但最常见的应用采用欧几里得范数或 $\ell_1$ 范数。例如，在电路设计中，单元之间的导线通常沿分段线性路径布线，每段或者水平、或者竖直。这称为 *Manhattan 布线*：矩形网格城市中沿街道行走的路径同样是分段线性的，每条街道都沿两个正交坐标轴中的一个方向。在这种情况下，连接单元 $i$ 与单元 $j$ 所需的导线长度为 $\|x_i-x_j\|_1$。

还可以引入非负权重，以反映不同弧上单位<!-- pdf-page: 447 -->距离的代价差异：

$$
\sum_{(i,j)\in\mathcal{A}}w_{ij}\|x_i-x_j\|.
$$

对没有连接的节点对赋予权重 $w_{ij}=0$，就可以用以下目标函数更简洁地表示这个问题：

$$
\sum_{i<j}w_{ij}\|x_i-x_j\|.
\tag{8.28}
$$

这个布置问题是凸的。

<div class="example" markdown="1">

**例 8.4 一个自由点。** 考虑只有一个点 $(u,v)\in\mathbf{R}^2$ 可以自由选择的情形，目标是最小化它到固定点 $(u_1,v_1),\ldots,(u_K,v_K)$ 的距离之和。

- *$\ell_1$ 范数。* 可以用解析方法找到使

    $$
    \sum_{i=1}^K(|u-u_i|+|v-v_i|)
    $$

    最小的点。固定点的任意中位数都是最优点。换句话说，$u$ 可以取 $\{u_1,\ldots,u_K\}$ 的任意中位数，$v$ 可以取 $\{v_1,\ldots,v_K\}$ 的任意中位数。（若 $K$ 为奇数，极小点唯一；若 $K$ 为偶数，最优点可能组成一个矩形。）

- *欧几里得范数。* 使欧几里得距离之和

    $$
    \sum_{i=1}^K\bigl((u-u_i)^2+(v-v_i)^2\bigr)^{1/2}
    $$

    最小的点 $(u,v)$，称为给定固定点的 *Weber 点*。

</div>

### 8.7.2 布置约束

下面列出一些可以加入基本布置问题、同时保持凸性的约束。可以要求某些位置 $x_i$ 位于指定的凸集中，例如某条直线、某个区间、正方形或椭球。可以约束一个点相对于一个或多个其他点的位置，例如限制两个点之间的距离。也可以施加相对位置约束，例如要求一个点位于另一个点的左侧。

一组点的*包围盒*（bounding box）是包含这些点的最小矩形。例如，要把点 $x_1,\ldots,x_p$ 限制在周长不超过 $P_{\max}$ 的包围盒内，可以加入约束

$$
u\preceq x_i\preceq v,\quad i=1,\ldots,p,\qquad2\mathbf{1}^T(v-u)\leq P_{\max},
$$

其中 $u$、$v$ 是附加变量。

<!-- pdf-page: 448 -->

### 8.7.3 非线性设施选址问题

更一般地，可以令每条弧的代价是其长度的非线性单调非减函数，即

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i<j}w_{ij}h(\|x_i-x_j\|),
\end{array}
$$

其中 $h$ 是在 $\mathbf{R}_+$ 上单调非减的凸函数，$w_{ij}\geq0$。这称为*非线性布置*或*非线性设施选址*问题。

一个常见的例子使用欧几里得范数和函数 $h(z)=z^2$，即最小化

$$
\sum_{i<j}w_{ij}\|x_i-x_j\|_2^2.
$$

这称为*二次布置问题*。当约束只有线性等式时，二次布置问题可以解析求解；当约束包括线性等式和不等式时，可以作为 QP 求解。

<div class="example" markdown="1">

**例 8.5 一个自由点。** 考虑只有一个点 $x$ 可以自由选择的情形，目标是最小化它到固定点 $x_1,\ldots,x_K$ 的欧几里得距离平方和：

$$
\|x-x_1\|_2^2+\|x-x_2\|_2^2+\cdots+\|x-x_K\|_2^2.
$$

求导可知，最优的 $x$ 为

$$
\frac{1}{K}(x_1+x_2+\cdots+x_K),
$$

即这些固定点的平均值。

</div>

其他一些有意思的选择包括死区宽度为 $2\gamma$ 的“死区”函数 $h$，定义为

$$
h(z)=\begin{cases}0 & |z|\leq\gamma\\|z-\gamma| & |z|\geq\gamma,\end{cases}
$$

以及“二次线性”函数 $h$，定义为

$$
h(z)=\begin{cases}z^2 & |z|\leq\gamma\\2\gamma|z|-\gamma^2 & |z|\geq\gamma.\end{cases}
$$

<div class="example" markdown="1">

**例 8.6** 考虑 $\mathbf{R}^2$ 中一个包含 $6$ 个自由点、$8$ 个固定点和 $27$ 条连线的布置问题。图 8.15–8.17 展示了以下准则对应的最优解：

$$
\sum_{(i,j)\in\mathcal{A}}\|x_i-x_j\|_2,\qquad
\sum_{(i,j)\in\mathcal{A}}\|x_i-x_j\|_2^2,\qquad
\sum_{(i,j)\in\mathcal{A}}\|x_i-x_j\|_2^4,
$$

也就是分别采用罚函数 $h(z)=z$、$h(z)=z^2$ 和 $h(z)=z^4$。图中还给出了相应连线长度的分布。

<p id="placement-comparison-start" markdown="1">比较这些结果可以看到，线性布置使自由点集中在一个较小的区域内，而二次和四次布置使这些点分散在较大的区域内。线性布置中有许多很短的连线，也有少数很长的连线：$3$ 条长度小于 $0.2$，$2$ 条长度大于 $1.5$。二次罚函数</p>

<!-- pdf-page: 449 -->

<figure id="fig-8-15" data-figure="8.15" data-no-english-text="true" data-reader-after="placement-comparison-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-15.png" alt="左图用实心点表示六个自由点、方框表示八个固定点，虚点线表示连线；右图给出连线长度的直方图和一条上升的线性罚函数虚线" data-source-page="449" data-source-rect="92,154,473,309.7">
<figcaption>图 8.15 <em>线性布置。</em>一个包含 6 个自由点（以实心点表示）、8 个固定点（以方框表示）和 27 条连线的布置问题。自由点的坐标使各连线的欧几里得长度之和最小。右图给出了这 27 条连线长度的分布。虚线表示经缩放的罚函数 $h(z)=z$。</figcaption>
</figure>

<figure id="fig-8-16" data-figure="8.16" data-no-english-text="true" data-reader-after="placement-comparison-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-16.png" alt="左图给出自由点较为分散的二次布置及其与固定点之间的连线，右图给出连线长度直方图和二次罚函数虚线" data-source-page="449" data-source-rect="92,451,473,607.1">
<figcaption>图 8.16 <em>二次布置。</em>采用与图 8.15 相同的数据，使各连线的欧几里得长度平方和最小的布置。虚线表示经缩放的罚函数 $h(z)=z^2$。</figcaption>
</figure>

<!-- pdf-page: 450 -->

<figure id="fig-8-17" data-figure="8.17" data-no-english-text="true" data-reader-after="placement-comparison-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-17.png" alt="左图给出四次布置中的自由点、固定点和连线，右图给出连线长度直方图以及随长度增大而快速上升的四次罚函数虚线" data-source-page="450" data-source-rect="146,112,527,265.5">
<figcaption>图 8.17 <em>四次布置。</em>使各连线的欧几里得长度四次方之和最小的布置。虚线表示经缩放的罚函数 $h(z)=z^4$。</figcaption>
</figure>

<p id="placement-comparison-end" markdown="1" data-reader-continue="placement-comparison-start">对长连线施加的惩罚相对于短连线更大，而对长度小于 $0.1$ 的连线，惩罚几乎可以忽略。因此，最大长度减小到小于 $1.4$，但短连线也更少。四次函数对长连线施加的惩罚更大，同时在更宽的区间内，从零到约 $0.4$，惩罚都可以忽略。因此，最大长度比二次布置更短，但长度接近最大值的连线也更多。</p>

</div>

### 8.7.4 带路径约束的选址问题

#### 路径约束

沿点 $x_1,\ldots,x_N$、包含 $p$ 条连线的一条路径，可以用节点序列 $i_0,\ldots,i_p\in\{1,\ldots,N\}$ 描述。路径长度为

$$
\|x_{i_1}-x_{i_0}\|+\|x_{i_2}-x_{i_1}\|+\cdots+\|x_{i_p}-x_{i_{p-1}}\|,
$$

它是 $x_1,\ldots,x_N$ 的凸函数，所以对路径长度施加上界是一个凸约束。若干有用的布置问题包含路径约束，或以路径长度为目标。本节介绍一个典型例子，其目标基于一组路径中的最大路径长度。

#### 极小极大延迟布置

考虑一个节点为 $1,\ldots,N$ 的有向无环图，用有序对集合 $\mathcal{A}$ 表示它的弧或连线：$(i,j)\in\mathcal{A}$ 当且仅当存在一条从 $i$ 指向 $j$ 的弧。如果 $\mathcal{A}$ 中没有弧指向节点 $i$，则称它为*源节点*；如果 $\mathcal{A}$ 中没有弧从它出发，则称它为*汇节点*或*目的节点*。我们关心图中的*极大路径*，它们从源节点开始，在汇节点结束。

图中的弧用来描述节点位于 $x_1,\ldots,x_N$ 的网络中某种流的传递，例如货物流或信息流。流从<!-- pdf-page: 451 -->一个源节点开始，沿路径逐个节点移动，最后到达汇节点或目的节点。用相邻节点之间的距离描述货物在节点间的传播或运输时间；一条路径的总延迟或传播时间与路径上相邻节点间的距离之和成正比。

现在可以描述极小极大延迟布置问题。一些节点的位置固定，其余节点的位置可以自由选择，即为优化变量。目标是选择这些自由节点的位置，使任意源节点到汇节点路径中的最大总延迟最小。显然这是一个凸问题，因为目标

$$
T_{\max}=\max\{\|x_{i_1}-x_{i_0}\|+\cdots+\|x_{i_p}-x_{i_{p-1}}\|\mid i_0,\ldots,i_p\text{ 是一条源汇路径}\}
\tag{8.29}
$$

是位置 $x_1,\ldots,x_N$ 的凸函数。

虽然最小化 (8.29) 是凸问题，但源汇路径的数量可能非常大，随节点数或弧数呈指数增长。可以用一种有用的等价表述，避免枚举所有汇源路径。

首先说明怎样计算最大延迟 $T_{\max}$，使效率远高于逐条计算每条源汇路径的延迟、再取最大值。设 $\tau_k$ 是从节点 $k$ 到某个汇节点的任意路径中的最大总延迟。显然，当 $k$ 是汇节点时，$\tau_k=0$。考虑一个节点 $k$，其出弧通向节点 $j_1,\ldots,j_p$。任何从节点 $k$ 出发并到汇节点结束的路径，第一条弧都必须通向节点 $j_1,\ldots,j_p$ 中的一个。如果路径先沿通向 $j_i$ 的弧，再沿从该处到某个汇节点的最长路径前进，那么总长度为

$$
\|x_{j_i}-x_k\|+\tau_{j_i},
$$

即通向 $j_i$ 的弧长，加上从 $j_i$ 到汇节点的最长路径的总长度。因此，从节点 $k$ 出发到汇节点的路径，其最大延迟满足

$$
\tau_k=\max\{\|x_{j_1}-x_k\|+\tau_{j_1},\ldots,\|x_{j_p}-x_k\|+\tau_{j_p}\}.
\tag{8.30}
$$

（这是一个简单的动态规划论证。）

等式 (8.30) 给出了求任意节点最大延迟的递推方法：从最大延迟为零的汇节点开始，利用 (8.30) 逐步向后推算，直到到达所有源节点。这类路径的最大延迟，就是所有 $\tau_k$ 中的最大值，它会在某个源节点处取得。这个动态规划递推说明，不必枚举全部路径，就能递归计算任意源汇路径上的最大延迟。递推所需的算术运算次数大约等于连线的数量。

下面说明如何用基于 (8.30) 的递推，表述极小极大延迟布置问题。可以把问题写成

$$
\begin{array}{ll}
\text{最小化} & \max\{\tau_k\mid k\text{ 是源节点}\}\\
\text{约束条件} & \tau_k=0,\quad k\text{ 是汇节点}\\
& \tau_k=\max\{\|x_j-x_k\|+\tau_j\mid\text{存在从 }k\text{ 到 }j\text{ 的弧}\},
\end{array}
$$

<!-- pdf-page: 452 -->

其中变量为 $\tau_1,\ldots,\tau_N$ 和自由点的位置。这个问题不是凸问题，但将等式约束替换为不等式后，可以写成一个等价的凸问题。引入新变量 $T_1,\ldots,T_N$，分别作为 $\tau_1,\ldots,\tau_N$ 的上界。对所有汇节点取 $T_k=0$，并用不等式

$$
T_k\geq\max\{\|x_{j_1}-x_k\|+T_{j_1},\ldots,\|x_{j_p}-x_k\|+T_{j_p}\}
$$

代替 (8.30)。若这些不等式成立，则 $T_k\geq\tau_k$。于是构造问题

$$
\begin{array}{ll}
\text{最小化} & \max\{T_k\mid k\text{ 是源节点}\}\\
\text{约束条件} & T_k=0,\quad k\text{ 是汇节点}\\
& T_k\geq\max\{\|x_j-x_k\|+T_j\mid\text{存在从 }k\text{ 到 }j\text{ 的弧}\}.
\end{array}
$$

这个以 $T_1,\ldots,T_N$ 和自由点位置为变量的问题是凸问题，它求解了极小极大延迟选址问题。

## 8.8 平面布局

在布置问题中，变量表示一组待作最优布置的点的坐标。*平面布局问题*（floor planning problem）可以看作对布置问题在以下两方面的推广：

- 待放置的对象是与坐标轴对齐的矩形或长方体，而不是点，并且这些对象不能重叠。

- 每个待放置的矩形或长方体，都可以在一定范围内调整形状。例如，可以固定每个矩形的面积，而不分别固定长度和高度。

目标通常是最小化包围盒的大小，例如面积、体积或周长。包围盒是包含所有待调整形状和放置的矩形或长方体的最小盒子。

不重叠约束使一般的平面布局问题成为复杂的组合优化问题，或矩形装填问题。不过，如果各矩形的相对位置关系已经给定，若干类型的平面布局问题就可以表述为凸优化问题。本节研究其中的一些。我们考虑二维情况，并在向高维推广不够明显时加以说明。

有 $N$ 个单元或模块 $C_1,\ldots,C_N$，需要调整形状并放置在一个宽为 $W$、高为 $H$、左下角位于 $(0,0)$ 的矩形中。第 $i$ 个单元的几何形状和位置，由其宽度 $w_i$、高度 $h_i$ 以及左下角坐标 $(x_i,y_i)$ 确定，如图 8.18 所示。

问题中的变量为 $x_i$、$y_i$、$w_i$、$h_i$，$i=1,\ldots,N$，以及包围矩形的宽 $W$ 和高 $H$。在所有平面布局问题中，都要求单元位于包围矩形内，即

$$
x_i\geq0,\qquad y_i\geq0,\qquad x_i+w_i\leq W,\qquad y_i+h_i\leq H,\qquad i=1,\ldots,N.
\tag{8.31}
$$

<!-- pdf-page: 453 -->

<figure id="fig-8-18" data-figure="8.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-18.png" alt="宽 W、高 H 的大矩形中放置三个互不重叠的小矩形，单元 Cᵢ 标有宽 wᵢ、高 hᵢ 和左下角坐标 (xᵢ,yᵢ)" data-source-page="453" data-source-rect="201,120,375,296.4">
<figcaption>图 8.18 平面布局问题。在一个宽为 $W$、高为 $H$、左下角位于 $(0,0)$ 的矩形中，放置互不重叠的矩形单元。第 $i$ 个单元由其宽度 $w_i$、高度 $h_i$ 以及左下角坐标 $(x_i,y_i)$ 确定。</figcaption>
</figure>

还要求各单元除边界可能接触外不能重叠：

$$
\mathbf{int}(C_i\cap C_j)=\varnothing\qquad\text{对 }i\ne j.
$$

（也可以要求单元之间保留一个正的最小间隙。）不重叠约束 $\mathbf{int}(C_i\cap C_j)=\varnothing$ 成立，当且仅当对 $i\ne j$，

$$
C_i\text{ 在 }C_j\text{ 左侧，或 }C_i\text{ 在 }C_j\text{ 右侧，或 }C_i\text{ 在 }C_j\text{ 下方，或 }C_i\text{ 在 }C_j\text{ 上方}.
$$

这四个几何条件对应不等式

$$
x_i+w_i\leq x_j,\quad\text{或 }x_j+w_j\leq x_i,\quad\text{或 }y_i+h_i\leq y_j,\quad\text{或 }y_j+h_j\leq y_i,
\tag{8.32}
$$

对每个 $i\ne j$，其中至少有一个必须成立。注意这些约束具有组合性质：对每一对 $i\ne j$，上面四个不等式中至少有一个必须成立。

### 8.8.1 相对位置约束

相对位置约束的思路，是对每一对单元指定四种可能的相对位置条件之一，即左、右、上或下。一种简单的指定方法，是在 $\{1,\ldots,N\}$ 上给出两个关系：$\mathcal{L}$ 表示“位于左侧”，$\mathcal{B}$ 表示“位于下方”。当 $(i,j)\in\mathcal{L}$ 时，要求 $C_i$ 位于 $C_j$ 左侧；当 $(i,j)\in\mathcal{B}$ 时，要求 $C_i$ 位于 $C_j$ 下方。于是得到约束

$$
x_i+w_i\leq x_j\quad\text{对 }(i,j)\in\mathcal{L},\qquad
y_i+h_i\leq y_j\quad\text{对 }(i,j)\in\mathcal{B},
\tag{8.33}
$$

<!-- pdf-page: 454 -->

其中 $i,j=1,\ldots,N$。为确保关系 $\mathcal{L}$ 和 $\mathcal{B}$ 指定了每一对单元的相对位置，要求对每个 $i\ne j$ 的 $(i,j)$，以下条件之一成立：

$$
(i,j)\in\mathcal{L},\qquad(j,i)\in\mathcal{L},\qquad(i,j)\in\mathcal{B},\qquad(j,i)\in\mathcal{B},
$$

并且 $(i,i)\notin\mathcal{L}$、$(i,i)\notin\mathcal{B}$。(8.33) 是关于变量的一组 $N(N-1)/2$ 个线性不等式。这些不等式蕴含不重叠条件 (8.32)，后者是 $N(N-1)/2$ 组各由四个线性不等式构成的析取条件。

可以假设关系 $\mathcal{L}$ 和 $\mathcal{B}$ 具有反对称性，即 $(i,j)\in\mathcal{L}\Rightarrow(j,i)\notin\mathcal{L}$，以及传递性，即 $(i,j)\in\mathcal{L}$、$(j,k)\in\mathcal{L}\Rightarrow(i,k)\in\mathcal{L}$。（否则，相对位置约束显然不可行。）传递性对应一个显然的条件：如果单元 $C_i$ 在 $C_j$ 左侧，$C_j$ 又在 $C_k$ 左侧，那么 $C_i$ 必须在 $C_k$ 左侧。在这种情况下，$(i,k)\in\mathcal{L}$ 对应的不等式是冗余的，因为它由另外两个不等式蕴含。利用关系 $\mathcal{L}$ 和 $\mathcal{B}$ 的传递性，可以去掉冗余约束，得到一组精简的相对位置不等式。

用两个有向无环图 $\mathcal{H}$ 和 $\mathcal{V}$，分别表示水平方向和竖直方向，可以方便地描述一组极小的相对位置约束。两个图都有 $N$ 个节点，对应平面布局问题中的 $N$ 个单元。图 $\mathcal{H}$ 按如下方式生成关系 $\mathcal{L}$：$(i,j)\in\mathcal{L}$ 当且仅当 $\mathcal{H}$ 中存在从 $i$ 到 $j$ 的有向路径。类似地，图 $\mathcal{V}$ 生成关系 $\mathcal{B}$：$(i,j)\in\mathcal{B}$ 当且仅当 $\mathcal{V}$ 中存在从 $i$ 到 $j$ 的有向路径。为确保每一对单元都有相对位置约束，要求对每一对单元，在两个图之一中存在从其中一个到另一个的有向路径。

显然，只需施加图 $\mathcal{H}$ 和 $\mathcal{V}$ 的边所对应的不等式，其余不等式由传递性得到。因此得到不等式组

$$
x_i+w_i\leq x_j\quad\text{对 }(i,j)\in\mathcal{H},\qquad
y_i+h_i\leq y_j\quad\text{对 }(i,j)\in\mathcal{V},
\tag{8.34}
$$

这是一组线性不等式，$\mathcal{H}$ 和 $\mathcal{V}$ 中的每条边各对应一个。不等式组 (8.34) 是 (8.33) 的一个子集，并与其等价。

类似地，也可以把 (8.31) 中的 $4N$ 个不等式约简为一组等价的极小不等式。约束 $x_i\geq0$ 只需对最左侧的单元施加，即对关系 $\mathcal{L}$ 中的极小元素 $i$ 施加。这些元素对应图 $\mathcal{H}$ 的源节点，即没有边指向它们的节点。类似地，不等式 $x_i+w_i\leq W$ 只需对最右侧的单元施加。竖直方向的包围盒不等式也可以用同样的方法删减成极小的一组。这样得到等价的极小包围盒不等式组：

$$
\begin{aligned}
x_i\geq0\quad\text{对 }\mathcal{L}\text{ 的极小元素 }i,&\qquad x_i+w_i\leq W\quad\text{对 }\mathcal{L}\text{ 的极大元素 }i,\\
y_i\geq0\quad\text{对 }\mathcal{B}\text{ 的极小元素 }i,&\qquad y_i+h_i\leq H\quad\text{对 }\mathcal{B}\text{ 的极大元素 }i.
\end{aligned}
\tag{8.35}
$$

图 8.19 给出了一个简单的例子。其中，$\mathcal{L}$ 的极小元素，也就是最左侧的单元，为 $C_1$、$C_2$ 和 $C_4$，唯一最右侧的单元是 $C_5$。指定水平相对位置的极小不等式组为

$$
\begin{gathered}
x_1\geq0,\quad x_2\geq0,\quad x_4\geq0,\quad x_5+w_5\leq W,\quad x_1+w_1\leq x_3,\\
x_2+w_2\leq x_3,\quad x_3+w_3\leq x_5,\quad x_4+w_4\leq x_5.
\end{gathered}
$$

<!-- pdf-page: 455 -->

<figure id="fig-8-19" data-figure="8.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-19.png" alt="左侧两个有向图 H 和 V 分别规定五个矩形单元的左右与上下关系，右侧给出满足这些关系的平面布局，单元以一至五编号" data-source-page="455" data-source-rect="152,120,415,266">
<figcaption>图 8.19 用水平图 $\mathcal{H}$ 和竖直图 $\mathcal{V}$ 规定各单元相对位置的示例。如果 $\mathcal{H}$ 中存在从节点 $i$ 到节点 $j$ 的路径，那么单元 $i$ 必须放在单元 $j$ 的左侧。如果 $\mathcal{V}$ 中存在从节点 $i$ 到节点 $j$ 的路径，那么单元 $i$ 必须放在单元 $j$ 的下方。右侧所示的平面布局满足这两个图规定的相对位置关系。</figcaption>
</figure>

指定竖直相对位置的极小不等式组为

$$
\begin{gathered}
y_2\geq0,\quad y_3\geq0,\quad y_5\geq0,\quad y_4+h_4\leq H,\quad y_5+h_5\leq H,\\
y_2+h_2\leq y_1,\quad y_1+h_1\leq y_4,\quad y_3+h_3\leq y_4.
\end{gathered}
$$

### 8.8.2 用凸优化进行平面布局

在这种表述中，变量是包围盒的宽 $W$ 和高 $H$，以及各单元的宽、高和位置：$w_i$、$h_i$、$x_i$ 和 $w_i$，$i=1,\ldots,N$。施加包围盒约束 (8.35) 和相对位置约束 (8.34)，它们都是线性不等式。目标取为包围盒的周长，即 $2(W+H)$，它是变量的线性函数。下面列出一些可以写成变量的凸不等式或线性等式的约束。

#### 最小间距

要在单元之间施加最小间距 $\rho>0$，可以将 $(i,j)\in\mathcal{H}$ 对应的相对位置约束 $x_i+w_i\leq x_j$，改为 $x_i+w_i+\rho\leq x_j$，竖直方向的图也作相同处理。可以为 $\mathcal{H}$ 和 $\mathcal{V}$ 中每条边指定不同的最小间距。另一种做法是固定 $W$ 和 $H$，以最大化最小间距 $\rho$ 为目标。

<!-- pdf-page: 456 -->

#### 单元的最小面积

为每个单元指定最小面积，即要求 $w_ih_i\geq A_i$，其中 $A_i>0$。这些最小面积约束可以用多种方式写成凸不等式，例如 $w_i\geq A_i/h_i$、$(w_ih_i)^{1/2}\geq A_i^{1/2}$，或 $\log w_i+\log h_i\geq\log A_i$。

#### 高宽比约束

可以对每个单元的高宽比施加上下界，即

$$
l_i\leq h_i/w_i\leq u_i.
$$

各边同乘 $w_i$，就把这些约束转化为线性不等式。也可以固定一个单元的高宽比，从而得到线性等式约束。

#### 对齐约束

可以要求两个单元的两条边或中心线对齐。例如，当

$$
y_i+h_i/2=y_j+h_j
$$

时，单元 $i$ 的水平中心线与单元 $j$ 的顶边对齐。

这些都是线性等式约束。类似地，也可以要求一个单元与包围盒的边界齐平。

#### 对称性约束

可以要求一对单元关于竖直轴或水平轴对称，该轴的位置既可以固定，也可以自由变化。例如，要规定单元 $i$ 和 $j$ 关于竖直轴 $x=x_{\mathrm{axis}}$ 对称，就施加线性等式约束

$$
x_{\mathrm{axis}}-(x_i+w_i/2)=x_j+w_j/2-x_{\mathrm{axis}}.
$$

施加这些等式约束，并把 $x_{\mathrm{axis}}$ 作为一个新变量，就可以要求若干对单元关于一条位置未指定的竖直轴对称。

#### 相似性约束

通过等式约束 $w_i=aw_j$、$h_i=ah_j$，可以要求单元 $i$ 是单元 $j$ 缩放 $a$ 倍后再平移得到的。这里的缩放因子 $a$ 必须固定。如果只施加其中一个约束，就要求某个单元的宽或高，是另一个单元相应宽或高的给定倍数。

#### 包含约束

可以要求某个单元包含一个给定点，这会产生两个线性不等式。也可以要求某个单元位于给定多面体内，同样只需施加线性不等式。

<!-- pdf-page: 457 -->

#### 距离约束

可以施加各种约束来限制一对单元之间的距离。最简单的情况是限制单元 $i$ 和 $j$ 的中心点之间的距离，或者限制单元上其他固定点，例如左下角之间的距离。例如，要限制单元 $i$ 和 $j$ 的中心之间的距离，可以使用凸不等式

$$
\|(x_i+w_i/2,y_i+h_i/2)-(x_j+w_j/2,y_j+h_j/2)\|\leq D_{ij}.
$$

与布置问题一样，可以限制距离之和，也可以把距离之和作为目标。

还可以限制单元 $i$ 和单元 $j$ 之间的距离 $\mathbf{dist}(C_i,C_j)$，即单元 $i$ 中一点与单元 $j$ 中一点之间的最小距离。一般可以这样做：为限制范数 $\|\cdot\|$ 下单元 $i$ 与 $j$ 的距离，引入四个新变量 $u_i$、$v_i$、$u_j$、$v_j$。数对 $(u_i,v_i)$ 表示 $C_i$ 中的一点，$(u_j,v_j)$ 表示 $C_j$ 中的一点。为保证这一点，施加线性不等式

$$
x_i\leq u_i\leq x_i+w_i,\qquad y_i\leq v_i\leq y_i+h_i,
$$

对单元 $j$ 也类似。最后，加入凸不等式

$$
\|(u_i,v_i)-(u_j,v_j)\|\leq D_{ij},
$$

以限制 $\mathbf{dist}(C_i,C_j)$。

在许多具体情况下，利用相对位置约束，或推导更明确的表达式，可以更高效地表示这些距离约束。例如，考虑 $\ell_\infty$ 范数，并假设相对位置约束已经规定单元 $i$ 位于单元 $j$ 左侧。两个单元之间的水平间隔为 $x_j-(x_i+w_i)$。这时，$\mathbf{dist}(C_i,C_j)\leq D_{ij}$ 当且仅当

$$
x_j-(x_i+w_i)\leq D_{ij},\qquad y_j-(y_i+h_i)\leq D_{ij},\qquad y_i-(y_j+h_j)\leq D_{ij}.
$$

第一个不等式表示，单元 $i$ 的右边与单元 $j$ 的左边之间的水平间隔不超过 $D_{ij}$。第二个不等式要求单元 $j$ 的底边至多比单元 $i$ 的顶边高 $D_{ij}$；第三个不等式要求单元 $i$ 的底边至多比单元 $j$ 的顶边高 $D_{ij}$。这三个不等式合在一起，等价于 $\mathbf{dist}(C_i,C_j)\leq D_{ij}$。此时无需引入任何新变量。

也可以用类似方法限制两个单元之间的 $\ell_1$ 或 $\ell_2$ 距离。这里引入一个新变量 $d_v$，作为单元间竖直间隔的上界。为限制 $\ell_1$ 距离，加入约束

$$
y_j-(y_i+h_i)\leq d_v,\qquad y_i-(y_j+h_j)\leq d_v,\qquad d_v\geq0,
$$

以及约束

$$
x_j-(x_i+w_i)+d_v\leq D_{ij}.
$$

第一项是水平间隔，第二项是竖直间隔的上界。要限制单元之间的欧几里得距离，则将最后这个约束替换为

$$
(x_j-(x_i+w_i))^2+d_v^2\leq D_{ij}^2.
$$

<!-- pdf-page: 458 -->

<figure id="fig-8-20" data-figure="8.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-20.png" alt="四个子图分别展示五个编号矩形单元的最优平面布局；相对位置相同，各单元的面积与形状随最小面积要求改变" data-source-page="458" data-source-rect="174,122,501,398">
<figcaption>图 8.20 采用图 8.19 所示相对位置约束的四个最优平面布局实例。每种情况下，目标都是最小化周长，并施加相同的单元间最小间距约束。还要求宽高比介于 $1/5$ 和 $5$ 之间。四种情况的区别在于对各单元最小面积的要求不同，但各单元最小面积之和在四种情况下都相同。</figcaption>
</figure>

<div class="example" markdown="1">

**例 8.7** 图 8.20 给出了一个有 $5$ 个单元的例子，采用图 8.19 的次序约束和四组不同的约束。每种情况下，施加的最小间距约束相同，宽高比约束也同为 $1/5\leq w_i/h_i\leq5$。四种情况的区别在于各单元所需的最小面积 $A_i$ 不同。选择 $A_i$ 时，使总的最小面积要求 $\sum_{i=1}^5 A_i$ 在每种情况下都相同。

</div>

### 8.8.3 用几何规划进行平面布局

平面布局问题也可以表述为以 $x_i$、$y_i$、$w_i$、$h_i$、$W$、$H$ 为变量的几何规划。这种表述能够处理的目标和约束，与凸优化表述能够表达的目标和约束略有不同。

首先注意，包围盒约束 (8.35) 和相对<!-- pdf-page: 459 -->位置约束 (8.34) 都是正项式不等式，因为左端是变量之和，右端则是单个变量，因而是单项式。将这些不等式除以右端，就得到标准的正项式不等式。

在几何规划表述中，可以最小化包围盒的面积，因为 $WH$ 是单项式，从而也是正项式。也可以精确指定每个单元的面积，因为 $w_ih_i=A_i$ 是单项式等式约束。另一方面，几何规划表述不能处理对齐、对称性和距离约束。但它可以处理相似性约束；实际上，可以要求一个单元与另一个单元相似，而不指定缩放比例，后者可以作为另一个变量。

<!-- pdf-page: 460 -->

## 文献说明

§8.3.3 中对欧几里得距离矩阵的刻画见 Schoenberg [Sch35]；也可参见 Gower [Gow85]。

本书对 Löwner-John 椭球这一术语的用法，沿用 Grötschel、Lovász 和 Schrijver [GLS88，第 69 页]。§8.4 中关于椭球逼近效果的结果由 John [Joh85] 证明。Boyd、El Ghaoui、Feron 和 Balakrishnan [BEFB94，§3.7] 给出了若干椭球逼近问题的凸表述，所涉及的集合由椭球的并、交或和定义。

§8.5 中定义的不同中心，可用于设计中心化，例如参见 Seifi、Ponnambalan 和 Vlach [SPV99]；也可用于割平面方法，参见 Elzinga 和 Moore [EM75]、Tarasov、Khachiyan 和 Èrlikh [TKE88]，以及 Ye [Ye97，第 8 章]。由对数障碍函数的 Hessian 矩阵定义的内侧椭球（第 420 页），有时称为 *Dikin 椭球*，它是 Dikin 线性规划和二次规划算法 [Dik67] 的基础。解析中心处的外侧椭球表达式由 Sonnevend [Son86] 给出。向非多面体凸集的推广，参见 Boyd 和 El Ghaoui [BE93]、Jarre [Jar94]，以及 Nesterov 和 Nemirovski [NN94，第 34 页]。

自 20 世纪 60 年代起，凸优化就已用于线性和非线性判别问题，见 Mangasarian [Man65] 和 Rosen [Ros65]。讨论模式分类的标准教材包括 Duda、Hart 和 Stork [DHS99]，以及 Hastie、Tibshirani 和 Friedman [HTF01]。关于支持向量分类器的详细讨论，参见 Vapnik [Vap00] 或 Schölkopf 和 Smola [SS01]。

例 8.4 定义的 Weber 点以 Weber [Web71] 命名。线性和二次布置用于电路设计，见 Kleinhaus、Sigl、Johannes 和 Antreich [KSJA91, SDJ91]。Sherwani [She99] 对 VLSI 电路设计中的布置、布局、平面布局及其他几何优化问题的算法，给出了较新的综述。

<!-- pdf-page: 461 -->

## 习题

### 在集合上的投影

**8.1 投影的唯一性。** 证明：如果 $C\subseteq\mathbf{R}^n$ 非空、闭且凸，范数 $\|\cdot\|$ 严格凸，那么对每个 $x_0$，恰好存在一个距 $x_0$ 最近的 $x\in C$。换言之，$x_0$ 在 $C$ 上的投影唯一。

**8.2 [Web94, Val64] 凸性的 Chebyshev 刻画。** 如果对每个 $x_0\in\mathbf{R}^n$，集合 $C\in\mathbf{R}^n$ 中都存在唯一一个距 $x_0$ 最近（按欧几里得范数衡量）的点，则称 $C$ 为 *Chebyshev 集*。由习题 8.1 的结果，每个非空闭凸集都是 Chebyshev 集。本题证明反向命题，这一命题称为 *Motzkin 定理*。

设 $C\in\mathbf{R}^n$ 为 Chebyshev 集。

- (a) 证明 $C$ 非空且闭。

- (b) 证明 $P_C$，即在 $C$ 上的欧几里得投影，是连续的。

- (c) 假设 $x_0\notin C$。证明：对所有 $x=\theta x_0+(1-\theta)P_C(x_0)$，其中 $0\leq\theta\leq1$，都有 $P_C(x)=P_C(x_0)$。

- (d) 假设 $x_0\notin C$。证明：对所有 $x=\theta x_0+(1-\theta)P_C(x_0)$，其中 $\theta\geq1$，都有 $P_C(x)=P_C(x_0)$。

- (e) 结合 (c) 和 (d)，可以得出：以 $P_C(x_0)$ 为起点、$x_0-P_C(x_0)$ 为方向的射线上，所有点的投影都是 $P_C(x_0)$。证明由此可知 $C$ 是凸集。

**8.3 正常锥上的欧几里得投影。**

- (a) *非负正交象限。* 证明：在非负正交象限上的欧几里得投影由第 399 页的表达式给出。

- (b) *半正定锥。* 证明：在半正定锥上的欧几里得投影由第 399 页的表达式给出。

- (c) *二阶锥。* 证明：$(x_0,t_0)$ 在二阶锥

    $$
    K=\{(x,t)\in\mathbf{R}^{n+1}\mid\|x\|_2\leq t\}
    $$

    上的欧几里得投影由下式给出：

    $$
    P_K(x_0,t_0)=\begin{cases}
    0&\|x_0\|_2\leq-t_0\\
    (x_0,t_0)&\|x_0\|_2\leq t_0\\
    (1/2)(1+t_0/\|x_0\|_2)(x_0,\|x_0\|_2)&\|x_0\|_2\geq|t_0|.
    \end{cases}
    $$

**8.4** 一个点在凸集上的欧几里得投影，可以给出一个简单的分离超平面：

$$
(P_C(x_0)-x_0)^T\bigl(x-(1/2)(x_0+P_C(x_0))\bigr)=0.
$$

找出一个反例，说明这种构造对于一般范数并不成立。

**8.5 [HUL93，第 1 卷，第 154 页] 深度函数与到边界的带符号距离。** 设 $C\subseteq\mathbf{R}^n$ 为非空凸集，$\mathbf{dist}(x,C)$ 为按某个范数衡量的 $x$ 到 $C$ 的距离。我们已经知道，$\mathbf{dist}(x,C)$ 是 $x$ 的凸函数。

- (a) 证明深度函数

    $$
    \mathbf{depth}(x,C)=\mathbf{dist}(x,\mathbf{R}^n\setminus C)
    $$

    在 $x\in C$ 上是凹函数。

- (b) 到 $C$ 的边界的带符号距离定义为

    $$
    s(x)=\begin{cases}
    \mathbf{dist}(x,C)&x\notin C\\
    -\mathbf{depth}(x,C)&x\in C.
    \end{cases}
    $$

    因此，$s(x)$ 在 $C$ 外为正，在其边界上为零，在其内部为负。证明 $s$ 是凸函数。

<!-- pdf-page: 462 -->

### 集合之间的距离

**8.6** 设 $C$、$D$ 为凸集。

- (a) 证明 $\mathbf{dist}(C,x+D)$ 是 $x$ 的凸函数。

- (b) 证明在 $t>0$ 时，$\mathbf{dist}(tC,x+tD)$ 是 $(x,t)$ 的凸函数。

**8.7 椭球的分离。** 设 $\mathcal{E}_1$ 和 $\mathcal{E}_2$ 为两个椭球，定义为

$$
\mathcal{E}_1=\{x\mid(x-x_1)^TP_1^{-1}(x-x_1)\leq1\},\qquad
\mathcal{E}_2=\{x\mid(x-x_2)^TP_2^{-1}(x-x_2)\leq1\},
$$

其中 $P_1,P_2\in\mathbf{S}_{++}^n$。证明：$\mathcal{E}_1\cap\mathcal{E}_2=\emptyset$ 当且仅当存在 $a\in\mathbf{R}^n$，使得

$$
\|P_2^{1/2}a\|_2+\|P_1^{1/2}a\|_2<a^T(x_1-x_2).
$$

**8.8 多面体的交与包含。** 设 $\mathcal{P}_1$ 和 $\mathcal{P}_2$ 为两个多面体，定义为

$$
\mathcal{P}_1=\{x\mid Ax\preceq b\},\qquad
\mathcal{P}_2=\{x\mid Fx\preceq g\},
$$

其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$F\in\mathbf{R}^{p\times n}$、$g\in\mathbf{R}^p$。说明如何通过求解一个或数量不多的 LP 可行性问题，完成下列任务。

- (a) 找到交集 $\mathcal{P}_1\cap\mathcal{P}_2$ 中的一个点。

- (b) 判断是否有 $\mathcal{P}_1\subseteq\mathcal{P}_2$。

对于定义为

$$
\mathcal{P}_1=\mathbf{conv}\{v_1,\ldots,v_K\},\qquad
\mathcal{P}_2=\mathbf{conv}\{w_1,\ldots,w_L\}
$$

的两个多面体，重复上述问题，其中 $v_1,\ldots,v_K,w_1,\ldots,w_L\in\mathbf{R}^n$。

### 欧几里得距离与角度问题

**8.9 最接近给定数据的欧几里得距离矩阵。** 给定数据 $\widehat d_{ij}$，$i,j=1,\ldots,n$；这些数据是 $\mathbf{R}^k$ 中向量间欧几里得距离的含误差测量值：

$$
\widehat d_{ij}=\|x_i-x_j\|_2+v_{ij},\qquad i,j=1,\ldots,n,
$$

其中 $v_{ij}$ 为某种噪声或误差。对所有 $i,j$，这些数据都满足 $\widehat d_{ij}\geq0$ 和 $\widehat d_{ij}=\widehat d_{ji}$。维数 $k$ 未指定。

说明如何用凸优化求解下面的问题。求维数 $k$ 和 $x_1,\ldots,x_n\in\mathbf{R}^k$，使 $\sum_{i,j=1}^n(d_{ij}-\widehat d_{ij})^2$ 最小，其中 $d_{ij}=\|x_i-x_j\|_2$，$i,j=1,\ldots,n$。换言之，给定一些近似的欧几里得距离数据，要求找出在最小二乘意义下最接近这些数据的一组真实欧几里得距离。

**8.10 极小极大角度拟合。** 假设 $y_1,\ldots,y_m\in\mathbf{R}^k$ 是变量 $x\in\mathbf{R}^n$ 的仿射函数：

$$
y_i=A_ix+b_i,\qquad i=1,\ldots,m,
$$

且 $z_1,\ldots,z_m\in\mathbf{R}^k$ 为给定的非零向量。我们希望在满足某些凸约束（例如线性不等式）的条件下选择变量 $x$，使 $y_i$ 与 $z_i$ 之间的最大夹角

$$
\max\{\angle(y_1,z_1),\ldots,\angle(y_m,z_m)\}
$$

最小。非零向量之间的夹角按通常的方式定义：

$$
\angle(u,v)=\cos^{-1}\left(\frac{u^Tv}{\|u\|_2\|v\|_2}\right),
$$

其中取 $\cos^{-1}(a)\in[0,\pi]$。我们只关心最优目标值不超过 $\pi/2$ 的情形。

将这个问题表述为凸优化或拟凸优化问题。当对 $x$ 的约束为线性不等式时，需要求解哪类问题（或哪些问题）？

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

<div class="translator-note" markdown="1">

**译注（QP 的目标函数）：** 题中目标为 $\|\widetilde a\|_2$。把这一非负目标平方为 $\|\widetilde a\|_2^2$，就得到具有相同最优解的标准 QP。

</div>

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

<div class="translator-note" markdown="1">

**译注（圆弧和接合点的数量）：** 按题目给出的 $n$ 个点，相邻点之间共有 $n-1$ 段圆弧，相应的角参数应为 $\theta_1,\ldots,\theta_{n-1}$。接合角跳变只在内部接点 $i=2,\ldots,n-1$ 处定义，因此总量 $D$ 的求和上限也应为 $n-1$。

</div>

<!-- pdf-page: 468 -->
