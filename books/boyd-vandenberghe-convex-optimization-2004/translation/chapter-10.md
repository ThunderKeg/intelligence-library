<!-- pdf-page: 535 -->

# 第 10 章 等式约束最小化

<aside class="chapter-guide"><p>导读（编者）：本章把牛顿法扩展到带线性等式约束的问题。先从 KKT 方程了解可行性与最优性的关系，再比较消去约束、求解对偶和直接构造牛顿步三种思路。阅读时注意，可行初始点与不可行初始点两种算法分别怎样处理约束；最后的实现部分说明，矩阵结构如何影响每一步的计算量。</p></aside>

## 10.1 等式约束最小化问题

本章介绍求解带等式约束的凸优化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)\\
\text{约束条件} & Ax=b,
\end{array}
\tag{10.1}
$$

的方法，其中 $f:\mathbf{R}^n\to\mathbf{R}$ 为凸函数且二阶连续可微，$A\in\mathbf{R}^{p\times n}$ 满足 $\mathbf{rank}\,A=p<n$。对 $A$ 的这些假设意味着，等式约束的数量少于变量的数量，而且各等式约束相互独立。假设最优解 $x^\star$ 存在，用 $p^\star$ 表示最优值，$p^\star=\inf\{f(x)\mid Ax=b\}=f(x^\star)$。

回顾 §4.2.3 或 §5.5.3 的结论：点 $x^\star\in\mathbf{dom}\,f$ 是 (10.1) 的最优点，当且仅当存在 $\nu^\star\in\mathbf{R}^p$，使

$$
Ax^\star=b,\qquad \nabla f(x^\star)+A^T\nu^\star=0.
\tag{10.2}
$$

因此，求解等式约束优化问题 (10.1)，等价于求出 KKT 方程 (10.2) 的一个解；这是关于 $n+p$ 个变量 $x^\star$、$\nu^\star$ 的 $n+p$ 个方程。第一组方程 $Ax^\star=b$ 称为*原可行性方程*（primal feasibility equations），它们是线性的。第二组方程 $\nabla f(x^\star)+A^T\nu^\star=0$ 称为*对偶可行性方程*（dual feasibility equations），通常是非线性的。与无约束优化一样，只有少数问题可以解析地求解这些最优性条件。最重要的特殊情形是 $f$ 为二次函数，将在 §10.1.1 中讨论。

任何等式约束最小化问题，都可以通过消去等式约束化为等价的无约束问题，然后使用第 9 章的方法求解。另一种做法是用无约束最小化方法求解对偶问题（假设对偶函数二阶可微），再从对偶解恢复<!-- pdf-page: 536 -->等式约束问题 (10.1) 的解。§10.1.2 和 §10.1.3 将分别简要讨论消元方法和对偶方法。

本章的大部分内容用于介绍直接处理等式约束的牛顿法扩展。在许多情况下，这些方法优于将等式约束问题化为无约束问题的方法。一个原因是，消元（或构造对偶问题）往往会破坏问题的结构，例如稀疏性；相比之下，直接处理等式约束的方法可以利用问题结构。另一个原因来自概念上的理解：直接处理等式约束的方法，可以看成直接求解最优性条件 (10.2) 的方法。

### 10.1.1 等式约束凸二次最小化

考虑等式约束凸二次最小化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=(1/2)x^TPx+q^Tx+r\\
\text{约束条件} & Ax=b,
\end{array}
\tag{10.3}
$$

其中 $P\in\mathbf{S}_+^n$，$A\in\mathbf{R}^{p\times n}$。这个问题本身很重要，而且它还是将牛顿法扩展到等式约束问题的基础。

此时，最优性条件 (10.2) 为

$$
Ax^\star=b,\qquad Px^\star+q+A^T\nu^\star=0,
$$

可以写成

$$
\begin{bmatrix}P&A^T\\A&0\end{bmatrix}
\begin{bmatrix}x^\star\\\nu^\star\end{bmatrix}
=\begin{bmatrix}-q\\b\end{bmatrix}.
\tag{10.4}
$$

这组关于 $n+p$ 个变量 $x^\star$、$\nu^\star$ 的 $n+p$ 个线性方程，称为等式约束二次优化问题 (10.3) 的 *KKT 方程组*（KKT system）。其系数矩阵称为 *KKT 矩阵*（KKT matrix）。

当 KKT 矩阵非奇异时，最优原始–对偶解对 $(x^\star,\nu^\star)$ 唯一。如果 KKT 矩阵奇异，但 KKT 方程组可解，那么任何一个解都给出一个最优解对 $(x^\star,\nu^\star)$。如果 KKT 方程组不可解，那么二次优化问题无下界或不可行。事实上，这种情况下存在 $v\in\mathbf{R}^n$ 和 $w\in\mathbf{R}^p$，使

$$
Pv+A^Tw=0,\qquad Av=0,\qquad -q^Tv+b^Tw>0.
$$

设 $\hat x$ 是任意可行点。点 $x=\hat x+tv$ 对所有 $t$ 都可行，且

$$
\begin{aligned}
f(\hat x+tv)&=f(\hat x)+t(v^TP\hat x+q^Tv)+(1/2)t^2v^TPv\\
&=f(\hat x)+t(-\hat x^TA^Tw+q^Tv)-(1/2)t^2w^TAv\\
&=f(\hat x)+t(-b^Tw+q^Tv),
\end{aligned}
$$

当 $t\to\infty$ 时，它无限下降。

<!-- pdf-page: 537 -->

#### KKT 矩阵的非奇异性

回顾假设 $P\in\mathbf{S}_+^n$ 且 $\mathbf{rank}\,A=p<n$。以下几个条件都与 KKT 矩阵非奇异等价：

- $\mathcal{N}(P)\cap\mathcal{N}(A)=\{0\}$，即 $P$ 和 $A$ 没有非平凡的公共零空间。
- $Ax=0,\ x\neq0\implies x^TPx>0$，即 $P$ 在 $A$ 的零空间上正定。
- $F^TPF\succ0$，其中 $F\in\mathbf{R}^{n\times(n-p)}$ 是满足 $\mathcal{R}(F)=\mathcal{N}(A)$ 的矩阵。

（见习题 10.1。）特别地，一个重要的特殊情形是：如果 $P\succ0$，则 KKT 矩阵一定非奇异。

### 10.1.2 消去等式约束

求解等式约束问题 (10.1) 的一种一般方法，是按照 §4.2.4 的做法消去等式约束，再用无约束最小化方法求解所得的无约束问题。先找出矩阵 $F\in\mathbf{R}^{n\times(n-p)}$ 和向量 $\hat x\in\mathbf{R}^n$，将（仿射）可行集参数化为

$$
\{x\mid Ax=b\}=\{Fz+\hat x\mid z\in\mathbf{R}^{n-p}\}.
$$

这里，$\hat x$ 可以取为 $Ax=b$ 的任意一个特解，$F\in\mathbf{R}^{n\times(n-p)}$ 可以取为任意值域等于 $A$ 的零空间的矩阵。然后构造*约化*或*消元后的*优化问题

$$
\begin{array}{ll}
\text{最小化} & \widetilde f(z)=f(Fz+\hat x),
\end{array}
\tag{10.5}
$$

这是以 $z\in\mathbf{R}^{n-p}$ 为变量的无约束问题。由它的解 $z^\star$，可以求得等式约束问题的解 $x^\star=Fz^\star+\hat x$。

还可以为等式约束问题构造最优对偶变量 $\nu^\star$：

$$
\nu^\star=-(AA^T)^{-1}A\nabla f(x^\star).
$$

为说明这个表达式正确，必须验证对偶可行性条件

$$
\nabla f(x^\star)+A^T\bigl(-(AA^T)^{-1}A\nabla f(x^\star)\bigr)=0
\tag{10.6}
$$

成立。为此，注意到

$$
\begin{bmatrix}F^T\\A\end{bmatrix}
\bigl(\nabla f(x^\star)-A^T(AA^T)^{-1}A\nabla f(x^\star)\bigr)=0,
$$

其中，对上方的块，使用了 $F^T\nabla f(x^\star)=\nabla\widetilde f(z^\star)=0$ 和 $AF=0$。由于左端的矩阵非奇异，由此可得 (10.6)。

<div class="example" id="example-10-1" markdown="1">

**例 10.1 资源约束下的最优分配。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n f_i(x_i)\\
\text{约束条件} & \displaystyle\sum_{i=1}^n x_i=b,
\end{array}
$$

<!-- pdf-page: 538 -->

其中函数 $f_i:\mathbf{R}\to\mathbf{R}$ 为凸函数且二阶可微，$b\in\mathbf{R}$ 是问题参数。可以将这个问题理解为：把总量固定为 $b$（预算）的单一资源，最优地分配给 $n$ 项除此之外彼此独立的活动。

例如，可以利用参数化

$$
x_n=b-x_1-\cdots-x_{n-1}
$$

消去 $x_n$，这对应于选择

$$
\hat x=be_n,\qquad F=\begin{bmatrix}I\\-\mathbf{1}^T\end{bmatrix}\in\mathbf{R}^{n\times(n-1)}.
$$

于是约化问题为

$$
\begin{array}{ll}
\text{最小化} & f_n(b-x_1-\cdots-x_{n-1})+\displaystyle\sum_{i=1}^{n-1}f_i(x_i),
\end{array}
$$

变量为 $x_1,\ldots,x_{n-1}$。

</div>

#### 消元矩阵的选择

当然，消元矩阵 $F$ 有许多种选择；它可以是 $\mathbf{R}^{n\times(n-p)}$ 中任意满足 $\mathcal{R}(F)=\mathcal{N}(A)$ 的矩阵。如果 $F$ 是这样的矩阵，且 $T\in\mathbf{R}^{(n-p)\times(n-p)}$ 非奇异，那么 $\widetilde F=FT$ 也是合适的消元矩阵，因为

$$
\mathcal{R}(\widetilde F)=\mathcal{R}(F)=\mathcal{N}(A).
$$

反过来，如果 $F$ 和 $\widetilde F$ 是任意两个合适的消元矩阵，那么存在某个非奇异矩阵 $T$，使 $\widetilde F=FT$。

如果用 $F$ 消去等式约束，需要求解无约束问题

$$
\begin{array}{ll}
\text{最小化} & f(Fz+\hat x),
\end{array}
$$

而如果采用 $\widetilde F$，则需要求解无约束问题

$$
\begin{array}{ll}
\text{最小化} & f(\widetilde F\widetilde z+\hat x)=f(F(T\widetilde z)+\hat x).
\end{array}
$$

这个问题与前一个问题等价，只是通过坐标变换 $z=T\widetilde z$ 得到的。换言之，改变消元矩阵，可以看作改变约化问题中的变量。

### 10.1.3 通过对偶求解等式约束问题

求解 (10.1) 的另一种方法，是先求解对偶问题，再按 §5.5.5 的方法恢复最优原变量 $x^\star$。(10.1) 的对偶函数为

$$
\begin{aligned}
g(\nu)&=-b^T\nu+\inf_x\bigl(f(x)+\nu^TAx\bigr)\\
&=-b^T\nu-\sup_x\bigl((-A^T\nu)^Tx-f(x)\bigr)\\
&=-b^T\nu-f^*(-A^T\nu),
\end{aligned}
$$

<!-- pdf-page: 539 -->

其中 $f^*$ 是 $f$ 的共轭函数，所以对偶问题为

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu-f^*(-A^T\nu).
\end{array}
$$

根据假设，存在最优点，因此问题严格可行，Slater 条件成立。于是强对偶性成立，且对偶最优值可以达到，即存在满足 $g(\nu^\star)=p^\star$ 的 $\nu^\star$。

如果对偶函数 $g$ 二阶可微，那么可以用第 9 章介绍的无约束最小化方法来最大化 $g$。（一般而言，即使 $f$ 二阶可微，对偶函数 $g$ 也未必二阶可微。）求得最优对偶变量 $\nu^\star$ 后，再由它重构最优原解 $x^\star$。（这一步并不总是很直接；见 §5.5.5。）

<div class="example" id="example-10-2" markdown="1">

**例 10.2 带等式约束的解析中心。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=-\displaystyle\sum_{i=1}^n\log x_i\\
\text{约束条件} & Ax=b,
\end{array}
\tag{10.7}
$$

其中 $A\in\mathbf{R}^{p\times n}$，有隐含约束 $x\succ0$。利用

$$
f^*(y)=\sum_{i=1}^n\bigl(-1-\log(-y_i)\bigr)=-n-\sum_{i=1}^n\log(-y_i)
$$

（其定义域为 $\mathbf{dom}\,f^*=-\mathbf{R}_{++}^n$），得到对偶问题

$$
\begin{array}{ll}
\text{最大化} & g(\nu)=-b^T\nu+n+\displaystyle\sum_{i=1}^n\log(A^T\nu)_i,
\end{array}
\tag{10.8}
$$

隐含约束为 $A^T\nu\succ0$。这里很容易求解对偶可行性方程，即找出使 $L(x,\nu)$ 最小的 $x$：

$$
\nabla f(x)+A^T\nu=-(1/x_1,\ldots,1/x_n)+A^T\nu=0,
$$

所以

$$
x_i(\nu)=1/(A^T\nu)_i.
\tag{10.9}
$$

为求解带等式约束的解析中心问题 (10.7)，先求解（无约束）对偶问题 (10.8)，再通过 (10.9) 恢复 (10.7) 的最优解。

</div>

## 10.2 含等式约束的牛顿法

本节介绍如何将牛顿法扩展到含等式约束的情形。它与无约束牛顿法几乎相同，只有两点区别：初始点必须可行（即满足 $x\in\mathbf{dom}\,f$ 和 $Ax=b$）；牛顿步的定义需要修改，以考虑等式约束。特别地，我们要保证牛顿步 $\Delta x_{\mathrm{nt}}$ 是可行方向，即 $A\Delta x_{\mathrm{nt}}=0$。

<!-- pdf-page: 540 -->

### 10.2.1 牛顿步

#### 通过二阶近似定义牛顿步

为推导等式约束问题

$$
\begin{array}{ll}
\text{最小化} & f(x)\\
\text{约束条件} & Ax=b
\end{array}
$$

在可行点 $x$ 处的牛顿步 $\Delta x_{\mathrm{nt}}$，我们用目标函数在 $x$ 附近的二阶 Taylor 近似替代目标函数，得到问题

$$
\begin{array}{ll}
\text{最小化} & \hat f(x+v)=f(x)+\nabla f(x)^Tv+(1/2)v^T\nabla^2f(x)v\\
\text{约束条件} & A(x+v)=b,
\end{array}
\tag{10.10}
$$

其变量为 $v$。这是一个带等式约束的（凸）二次最小化问题，可以解析求解。假定对应的 KKT 矩阵非奇异，我们把凸二次问题 (10.10) 的解定义为 $x$ 处的牛顿步 $\Delta x_{\mathrm{nt}}$。换言之，当用二次近似替代 $f$ 时，为求解这个问题，需要在 $x$ 上加上牛顿步 $\Delta x_{\mathrm{nt}}$。

根据 §10.1.1 对等式约束二次问题的分析，牛顿步 $\Delta x_{\mathrm{nt}}$ 满足

$$
\begin{bmatrix}
\nabla^2f(x) & A^T\\
A & 0
\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\w\end{bmatrix}
=\begin{bmatrix}-\nabla f(x)\\0\end{bmatrix},
\tag{10.11}
$$

其中 $w$ 是该二次问题对应的最优对偶变量。只有在 KKT 矩阵非奇异的点处，牛顿步才有定义。

与无约束问题的牛顿法一样，当目标函数 $f$ 恰好为二次函数时，牛顿更新 $x+\Delta x_{\mathrm{nt}}$ 就是等式约束最小化问题的精确解，此时向量 $w$ 是原问题的最优对偶变量。这与无约束情形一样，提示我们：当 $f$ 接近二次函数时，$x+\Delta x_{\mathrm{nt}}$ 应当是解 $x^\star$ 的一个很好的估计，而 $w$ 应当是最优对偶变量 $\nu^\star$ 的一个很好的估计。

#### 线性化最优性条件的解

我们可以把牛顿步 $\Delta x_{\mathrm{nt}}$ 及其对应的向量 $w$，解释为最优性条件

$$
Ax^\star=b,\qquad \nabla f(x^\star)+A^T\nu^\star=0
$$

的线性化近似的解。用 $x+\Delta x_{\mathrm{nt}}$ 替代 $x^\star$，用 $w$ 替代 $\nu^\star$，并将第二个方程中的梯度项替换为它在 $x$ 附近的线性化近似，得到方程

$$
A(x+\Delta x_{\mathrm{nt}})=b,\qquad
\nabla f(x+\Delta x_{\mathrm{nt}})+A^Tw
\approx\nabla f(x)+\nabla^2f(x)\Delta x_{\mathrm{nt}}+A^Tw=0.
$$

利用 $Ax=b$，可将其写成

$$
A\Delta x_{\mathrm{nt}}=0,\qquad
\nabla^2f(x)\Delta x_{\mathrm{nt}}+A^Tw=-\nabla f(x),
$$

这正是定义牛顿步的方程组 (10.11)。

<!-- pdf-page: 541 -->

#### 牛顿减量

我们将等式约束问题的牛顿减量定义为

$$
\lambda(x)=\bigl(\Delta x_{\mathrm{nt}}^T\nabla^2f(x)\Delta x_{\mathrm{nt}}\bigr)^{1/2}.
\tag{10.12}
$$

这个表达式与无约束情形使用的 (9.29) 完全相同，也具有相同的解释。例如，$\lambda(x)$ 就是在 Hessian 矩阵所确定的范数下，牛顿步的范数。

设

$$
\hat f(x+v)=f(x)+\nabla f(x)^Tv+(1/2)v^T\nabla^2f(x)v
$$

为 $f$ 在 $x$ 处的二阶 Taylor 近似。$f(x)$ 与二阶模型最小值之差满足

$$
f(x)-\inf\{\hat f(x+v)\mid A(x+v)=b\}=\lambda(x)^2/2,
\tag{10.13}
$$

这与无约束情形完全相同（见习题 10.6）。这意味着，与无约束情形一样，$\lambda(x)^2/2$ 基于 $x$ 处的二次模型给出了 $f(x)-p^\star$ 的一个估计；同时，$\lambda(x)$（或 $\lambda(x)^2$ 的某个倍数）也可作为一个良好停止准则的依据。

牛顿减量也会出现在直线搜索中，因为 $f$ 沿方向 $\Delta x_{\mathrm{nt}}$ 的方向导数为

$$
\left.\frac{d}{dt}f(x+t\Delta x_{\mathrm{nt}})\right|_{t=0}
=\nabla f(x)^T\Delta x_{\mathrm{nt}}=-\lambda(x)^2,
\tag{10.14}
$$

这也与无约束情形相同。

#### 可行下降方向

假设 $Ax=b$。若 $Av=0$，则称 $v\in\mathbf{R}^n$ 为一个可行方向。此时，所有形如 $x+tv$ 的点也都可行，即 $A(x+tv)=b$。若对充分小的 $t>0$，有 $f(x+tv)<f(x)$，则称 $v$ 为 $f$ 在 $x$ 处的下降方向。

牛顿步总是一个可行下降方向（除非 $x$ 已经最优，此时 $\Delta x_{\mathrm{nt}}=0$）。事实上，定义 $\Delta x_{\mathrm{nt}}$ 的第二组方程是 $A\Delta x_{\mathrm{nt}}=0$，这说明它是一个可行方向；由 (10.14) 可知，它也是下降方向。

#### 仿射不变性

与无约束优化的牛顿步和牛顿减量一样，等式约束优化的牛顿步和牛顿减量也具有仿射不变性。假设 $T\in\mathbf{R}^{n\times n}$ 非奇异，并定义 $\bar f(y)=f(Ty)$。有

$$
\nabla\bar f(y)=T^T\nabla f(Ty),\qquad
\nabla^2\bar f(y)=T^T\nabla^2f(Ty)T,
$$

而等式约束 $Ax=b$ 变为 $ATy=b$。

现在考虑在约束 $ATy=b$ 下最小化 $\bar f(y)$ 的问题。$y$ 处的牛顿步 $\Delta y_{\mathrm{nt}}$ 由下列方程组的解给出：

$$
\begin{bmatrix}
T^T\nabla^2f(Ty)T & T^TA^T\\
AT & 0
\end{bmatrix}
\begin{bmatrix}\Delta y_{\mathrm{nt}}\\\bar w\end{bmatrix}
=\begin{bmatrix}-T^T\nabla f(Ty)\\0\end{bmatrix}.
$$

<!-- pdf-page: 542 -->

将它与 (10.11) 给出的 $f$ 在 $x=Ty$ 处的牛顿步 $\Delta x_{\mathrm{nt}}$ 比较，可见

$$
T\Delta y_{\mathrm{nt}}=\Delta x_{\mathrm{nt}}
$$

（并且 $w=\bar w$），即 $y$ 和 $x$ 处的牛顿步之间，与 $Ty=x$ 一样，具有相同的坐标变换关系。

### 10.2.2 含等式约束的牛顿法

含等式约束的牛顿法，其基本流程与无约束情形完全相同。

<div class="algorithm" id="algorithm-10-1" data-algorithm="10.1" markdown="1">

**算法 10.1 等式约束最小化的牛顿法。**

**给定** 满足 $Ax=b$ 的初始点 $x\in\mathbf{dom}\,f$，容差 $\epsilon>0$。

**重复执行**

1. **计算牛顿步和牛顿减量** $\Delta x_{\mathrm{nt}}$、$\lambda(x)$。

2. **停止准则。** 若 $\lambda^2/2\leq\epsilon$，则退出。

3. **直线搜索。** 通过回溯直线搜索选择步长 $t$。

4. **更新。** $x:=x+t\Delta x_{\mathrm{nt}}$。

</div>

这种方法称为可行下降法，因为所有迭代点都可行，并且 $f(x^{(k+1)})<f(x^{(k)})$（除非 $x^{(k)}$ 已经最优）。牛顿法要求每个 $x$ 处的 KKT 矩阵都可逆；§10.2.4 将更精确地说明保证收敛所需的假设。

### 10.2.3 牛顿法与消元

现在证明：对等式约束问题 (10.1) 使用牛顿法得到的迭代点，与对约化问题 (10.5) 使用牛顿法得到的迭代点相同。假设 $F$ 满足 $\mathcal{R}(F)=\mathcal{N}(A)$ 和 $\mathbf{rank}\,F=n-p$，且 $\hat x$ 满足 $A\hat x=b$。约化后的目标函数 $\tilde f(z)=f(Fz+\hat x)$ 的梯度和 Hessian 矩阵为

$$
\nabla\tilde f(z)=F^T\nabla f(Fz+\hat x),\qquad
\nabla^2\tilde f(z)=F^T\nabla^2f(Fz+\hat x)F.
$$

从 Hessian 矩阵的表达式可以看出，等式约束问题的牛顿步有定义，即 KKT 矩阵

$$
\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}
$$

可逆，当且仅当约化问题的牛顿步有定义，即 $\nabla^2\tilde f(z)$ 可逆。

约化问题的牛顿步为

$$
\Delta z_{\mathrm{nt}}=-\nabla^2\tilde f(z)^{-1}\nabla\tilde f(z)
=-(F^T\nabla^2f(x)F)^{-1}F^T\nabla f(x),
\tag{10.15}
$$

<!-- pdf-page: 543 -->

其中 $x=Fz+\hat x$。约化问题的这个搜索方向，对应于原等式约束问题中的方向

$$
F\Delta z_{\mathrm{nt}}=-F(F^T\nabla^2f(x)F)^{-1}F^T\nabla f(x).
$$

我们断言，它恰好就是 (10.11) 定义的原问题的牛顿方向 $\Delta x_{\mathrm{nt}}$。

为证明这一点，取 $\Delta x_{\mathrm{nt}}=F\Delta z_{\mathrm{nt}}$，选取

$$
w=-(AA^T)^{-1}A\bigl(\nabla f(x)+\nabla^2f(x)\Delta x_{\mathrm{nt}}\bigr),
$$

并验证定义牛顿步的方程

$$
\nabla^2f(x)\Delta x_{\mathrm{nt}}+A^Tw+\nabla f(x)=0,\qquad
A\Delta x_{\mathrm{nt}}=0
\tag{10.16}
$$

成立。由于 $AF=0$，第二个方程 $A\Delta x_{\mathrm{nt}}=0$ 成立。为验证第一个方程，注意到

$$
\begin{aligned}
&\begin{bmatrix}F^T\\A\end{bmatrix}
\bigl(\nabla^2f(x)\Delta x_{\mathrm{nt}}+A^Tw+\nabla f(x)\bigr)\\
&\quad=\begin{bmatrix}
F^T\nabla^2f(x)\Delta x_{\mathrm{nt}}+F^TA^Tw+F^T\nabla f(x)\\
A\nabla^2f(x)\Delta x_{\mathrm{nt}}+AA^Tw+A\nabla f(x)
\end{bmatrix}\\
&\quad=0.
\end{aligned}
$$

由于第一行左侧的矩阵非奇异，可知 (10.16) 成立。

类似地，$\tilde f$ 在 $z$ 处的牛顿减量 $\tilde\lambda(z)$ 与 $f$ 在 $x$ 处的牛顿减量也相等：

$$
\begin{aligned}
\tilde\lambda(z)^2
&=\Delta z_{\mathrm{nt}}^T\nabla^2\tilde f(z)\Delta z_{\mathrm{nt}}\\
&=\Delta z_{\mathrm{nt}}^TF^T\nabla^2f(x)F\Delta z_{\mathrm{nt}}\\
&=\Delta x_{\mathrm{nt}}^T\nabla^2f(x)\Delta x_{\mathrm{nt}}\\
&=\lambda(x)^2.
\end{aligned}
$$

### 10.2.4 收敛分析

前面已经看到，使用含等式约束的牛顿法，与消去等式约束后对约化问题使用牛顿法完全相同。因此，无约束问题牛顿法的所有收敛结论，都可以用于等式约束问题的牛顿法。特别地，含等式约束的牛顿法，其实际表现与无约束牛顿法完全一样。一旦 $x^{(k)}$ 接近 $x^\star$，收敛就会极快，只需几次迭代就能达到很高的精度。

#### 假设

我们作如下假设。

<!-- pdf-page: 544 -->

- 下水平集 $S=\{x\mid x\in\mathbf{dom}\,f,\ f(x)\leq f(x^{(0)}),\ Ax=b\}$ 是闭集，其中 $x^{(0)}\in\mathbf{dom}\,f$ 满足 $Ax^{(0)}=b$。若 $f$ 是闭函数，这一条件就成立（见 §A.3.3）。

- 在集合 $S$ 上，有 $\nabla^2f(x)\preceq MI$，并且

    $$
    \left\|\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}^{-1}\right\|_2\leq K,
    \tag{10.17}
    $$

    即 KKT 矩阵的逆在 $S$ 上有界。（当然，为了使 $S$ 中每一点处的牛顿步都有定义，这个逆必须存在。）

- 对 $x,\tilde x\in S$，$\nabla^2f$ 满足 Lipschitz 条件 $\|\nabla^2f(x)-\nabla^2f(\tilde x)\|_2\leq L\|x-\tilde x\|_2$。

#### KKT 矩阵的逆有界这一假设

条件 (10.17) 起到了标准牛顿法中强凸性假设的作用（§9.5.3，第 488 页）。没有等式约束时，(10.17) 化为 $S$ 上的条件 $\|\nabla^2f(x)^{-1}\|_2\leq K$；所以，若在 $S$ 上有 $\nabla^2f(x)\succeq mI$，其中 $m>0$，就可取 $K=1/m$。存在等式约束时，该条件就不像给最小特征值规定一个正下界那样简单了。由于 KKT 矩阵对称，条件 (10.17) 要求其特征值与零保持一定距离；这些特征值中，$n$ 个为正，$p$ 个为负。

#### 通过消元后的问题进行分析

上述假设意味着，消元后的目标函数 $\tilde f$ 及其对应的初始点 $z^{(0)}$（其中 $x^{(0)}=\hat x+Fz^{(0)}$），满足 §9.5.3 无约束牛顿法收敛分析所要求的假设（只是常数变为 $\tilde m$、$\tilde M$ 和 $\tilde L$）。因此，含等式约束的牛顿法收敛到 $x^\star$（相应的对偶变量也收敛到 $\nu^\star$）。

要证明上述假设蕴含消元后的问题满足无约束牛顿法的各项假设，大部分步骤都很直接（见习题 10.4）。这里证明其中较难的一项：KKT 矩阵的逆有界这一条件，加上上界 $\nabla^2f(x)\preceq MI$，能够推出存在某个正常数 $m$，使 $\nabla^2\tilde f(z)\succeq mI$。更具体地，我们将证明，取

$$
m=\frac{\sigma_{\min}(F)^2}{K^2M},
\tag{10.18}
$$

这个不等式就成立；由于 $F$ 满秩，上式给出的 $m$ 为正。

用反证法证明。假设 $F^THF\not\succeq mI$，其中 $H=\nabla^2f(x)$。那么可以找到满足 $\|u\|_2=1$ 的 $u$，使 $u^TF^THFu<m$，即 $\|H^{1/2}Fu\|_2<m^{1/2}$。利用 $AF=0$，有

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}Fu\\0\end{bmatrix}
=\begin{bmatrix}HFu\\0\end{bmatrix},
$$

<!-- pdf-page: 545 -->

所以

$$
\left\|\begin{bmatrix}H&A^T\\A&0\end{bmatrix}^{-1}\right\|_2
\geq\frac{\left\|\begin{bmatrix}Fu\\0\end{bmatrix}\right\|_2}
{\left\|\begin{bmatrix}HFu\\0\end{bmatrix}\right\|_2}
=\frac{\|Fu\|_2}{\|HFu\|_2}.
$$

利用 $\|Fu\|_2\geq\sigma_{\min}(F)$ 和

$$
\|HFu\|_2\leq\|H^{1/2}\|_2\|H^{1/2}Fu\|_2<M^{1/2}m^{1/2},
$$

再使用 (10.18) 给出的 $m$ 的表达式，得到

$$
\left\|\begin{bmatrix}H&A^T\\A&0\end{bmatrix}^{-1}\right\|_2
\geq\frac{\|Fu\|_2}{\|HFu\|_2}
>\frac{\sigma_{\min}(F)}{M^{1/2}m^{1/2}}=K.
$$

#### 自协调函数的收敛分析

若 $f$ 自协调，则 $\tilde f(z)=f(Fz+\hat x)$ 也自协调。因此，若 $f$ 自协调，就得到与无约束问题完全相同的复杂度估计：获得精度为 $\epsilon$ 的解所需的迭代次数不超过

$$
\frac{20-8\alpha}{\alpha\beta(1-2\alpha)^2}\bigl(f(x^{(0)})-p^\star\bigr)
+\log_2\log_2(1/\epsilon),
$$

其中 $\alpha$ 和 $\beta$ 是回溯参数（见 (9.56)）。

## 10.3 不可行初始点牛顿法

§10.2 中介绍的牛顿法是一种可行下降法。本节介绍一种推广后的牛顿法，允许初始点和迭代点不可行。

### 10.3.1 不可行点处的牛顿步

与牛顿法一样，我们从等式约束最小化问题的最优性条件出发：

$$
Ax^\star=b,\qquad \nabla f(x^\star)+A^T\nu^\star=0.
$$

设 $x$ 为当前点，不要求它可行，但假定它满足 $x\in\mathbf{dom}\,f$。我们的目标是找出步 $\Delta x$，使 $x+\Delta x$（至少近似地）满足最优性条件，即 $x+\Delta x\approx x^\star$。为此，<!-- pdf-page: 546 -->在最优性条件中用 $x+\Delta x$ 替代 $x^\star$，用 $w$ 替代 $\nu^\star$，并对梯度使用一阶近似

$$
\nabla f(x+\Delta x)\approx\nabla f(x)+\nabla^2f(x)\Delta x,
$$

得到

$$
A(x+\Delta x)=b,\qquad \nabla f(x)+\nabla^2f(x)\Delta x+A^Tw=0.
$$

这是一组关于 $\Delta x$ 和 $w$ 的线性方程：

$$
\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x\\w\end{bmatrix}
=-\begin{bmatrix}\nabla f(x)\\Ax-b\end{bmatrix}.
\tag{10.19}
$$

这些方程与在可行点 $x$ 处定义牛顿步的方程 (10.11) 相同，只有一点区别：右端的第二个分块中含有 $Ax-b$，它是线性等式约束的残差向量。当 $x$ 可行时，残差为零，方程 (10.19) 就化为在可行点 $x$ 处定义标准牛顿步的方程 (10.11)。因此，若 $x$ 可行，则 (10.19) 定义的步 $\Delta x$ 与前面介绍的牛顿步相同（但后者仅在 $x$ 可行时才有定义）。所以，我们也用记号 $\Delta x_{\mathrm{nt}}$ 表示 (10.19) 定义的步 $\Delta x$，称它为 $x$ 处的牛顿步，而不会产生混淆。

#### 解释为原始–对偶牛顿步

可以用等式约束问题的*原始–对偶方法*来解释方程 (10.19)。所谓原始–对偶方法，是指同时更新原变量 $x$ 和对偶变量 $\nu$，以便（近似）满足最优性条件的方法。

将最优性条件写成 $r(x^\star,\nu^\star)=0$，其中 $r:\mathbf{R}^n\times\mathbf{R}^p\to\mathbf{R}^n\times\mathbf{R}^p$ 定义为

$$
r(x,\nu)=\bigl(r_{\mathrm{dual}}(x,\nu),r_{\mathrm{pri}}(x,\nu)\bigr).
$$

这里

$$
r_{\mathrm{dual}}(x,\nu)=\nabla f(x)+A^T\nu,\qquad
r_{\mathrm{pri}}(x,\nu)=Ax-b
$$

分别为*对偶残差*和*原残差*。$r$ 在当前估计 $y$ 附近的一阶 Taylor 近似为

$$
r(y+z)\approx\hat r(y+z)=r(y)+Dr(y)z,
$$

其中 $Dr(y)\in\mathbf{R}^{(n+p)\times(n+p)}$ 是 $r$ 在 $y$ 处的导数（见 §A.4.1）。我们把使 Taylor 近似 $\hat r(y+z)$ 为零的步 $z$，定义为原始–对偶牛顿步 $\Delta y_{\mathrm{pd}}$，即

$$
Dr(y)\Delta y_{\mathrm{pd}}=-r(y).
\tag{10.20}
$$

注意，这里同时把 $x$ 和 $\nu$ 视为变量；$\Delta y_{\mathrm{pd}}=(\Delta x_{\mathrm{pd}},\Delta\nu_{\mathrm{pd}})$ 同时给出原步和对偶步。

<!-- pdf-page: 547 -->

计算 $r$ 的导数，可将 (10.20) 写成

$$
\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{pd}}\\\Delta\nu_{\mathrm{pd}}\end{bmatrix}
=-\begin{bmatrix}r_{\mathrm{dual}}\\r_{\mathrm{pri}}\end{bmatrix}
=-\begin{bmatrix}\nabla f(x)+A^T\nu\\Ax-b\end{bmatrix}.
\tag{10.21}
$$

将 $\nu+\Delta\nu_{\mathrm{pd}}$ 记为 $\nu^+$，便可写成

$$
\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{pd}}\\\nu^+\end{bmatrix}
=-\begin{bmatrix}\nabla f(x)\\Ax-b\end{bmatrix},
\tag{10.22}
$$

这与方程组 (10.19) 完全相同。因此，(10.19)、(10.21) 和 (10.22) 的解之间满足

$$
\Delta x_{\mathrm{nt}}=\Delta x_{\mathrm{pd}},\qquad
w=\nu^+=\nu+\Delta\nu_{\mathrm{pd}}.
$$

这表明，（不可行）牛顿步就是原始–对偶步中的原变量部分，而相应的对偶向量 $w$ 就是原始–对偶方法更新后的变量 $\nu^+=\nu+\Delta\nu_{\mathrm{pd}}$。

(10.21) 和 (10.22) 给出的牛顿步与对偶变量（或对偶步）的两种表达式当然等价，但它们分别揭示了牛顿步的不同特征。方程 (10.21) 表明，牛顿步及其相应的对偶步，可以通过求解一个以原残差和对偶残差为右端的方程组得到。方程 (10.22) 是最初定义牛顿步的方式，它给出牛顿步和更新后的对偶变量，并表明在计算原步或更新后的对偶变量值时，并不需要对偶变量的当前值。

#### 残差范数的减小性质

不可行点处的牛顿方向不一定是 $f$ 的下降方向。由 (10.19) 可知

$$
\begin{aligned}
\left.\frac{d}{dt}f(x+t\Delta x)\right|_{t=0}
&=\nabla f(x)^T\Delta x\\
&=-\Delta x^T\bigl(\nabla^2f(x)\Delta x+A^Tw\bigr)\\
&=-\Delta x^T\nabla^2f(x)\Delta x+(Ax-b)^Tw,
\end{aligned}
$$

它不一定为负（当然，若 $x$ 可行，即 $Ax=b$，则例外）。不过，原始–对偶解释表明，残差的范数沿牛顿方向减小，即

$$
\left.\frac{d}{dt}\|r(y+t\Delta y_{\mathrm{pd}})\|_2^2\right|_{t=0}
=2r(y)^TDr(y)\Delta y_{\mathrm{pd}}=-2r(y)^Tr(y).
$$

对平方项求导，可得

$$
\left.\frac{d}{dt}\|r(y+t\Delta y_{\mathrm{pd}})\|_2\right|_{t=0}
=-\|r(y)\|_2.
\tag{10.23}
$$

因此，可以用 $\|r\|_2$ 来衡量不可行初始点牛顿法的进展，例如在直线搜索中这样做。（对于标准牛顿法，至少在达到二次收敛之前，我们用函数值 $f$ 来衡量算法的进展。）

<!-- pdf-page: 548 -->

#### 完整步长的可行性性质

由构造可知，(10.19) 定义的牛顿步 $\Delta x_{\mathrm{nt}}$ 具有如下性质：

$$
A(x+\Delta x_{\mathrm{nt}})=b.
\tag{10.24}
$$

因此，若沿牛顿步 $\Delta x_{\mathrm{nt}}$ 采用长度为一的步长，则下一个迭代点将是可行点。一旦 $x$ 可行，牛顿步就成为可行方向，因而无论此后采用什么步长，所有后续迭代点都会可行。

更一般地，可以分析阻尼步对等式约束残差 $r_{\mathrm{pri}}$ 的影响。取步长 $t\in[0,1]$ 时，下一个迭代点为 $x^+=x+t\Delta x_{\mathrm{nt}}$，因此由 (10.24)，下一个迭代点的等式约束残差为

$$
r_{\mathrm{pri}}^+=A(x+\Delta x_{\mathrm{nt}}t)-b
=(1-t)(Ax-b)=(1-t)r_{\mathrm{pri}}.
$$

所以，长度为 $t$ 的阻尼步会将残差缩放为原来的 $1-t$ 倍。现在假设，对于 $i=0,\ldots,k-1$，有 $x^{(i+1)}=x^{(i)}+t^{(i)}\Delta x_{\mathrm{nt}}^{(i)}$，其中 $\Delta x_{\mathrm{nt}}^{(i)}$ 是点 $x^{(i)}\in\mathbf{dom}\,f$ 处的牛顿步，且 $t^{(i)}\in[0,1]$。那么

$$
r^{(k)}=\left(\prod_{i=0}^{k-1}(1-t^{(i)})\right)r^{(0)},
$$

其中 $r^{(i)}=Ax^{(i)}-b$ 是 $x^{(i)}$ 的残差。这个公式表明，每一步的原残差都与初始原残差方向相同，并且每一步都会缩小。它还表明，一旦采用过一次完整步长，所有后续迭代点都满足原可行性。

### 10.3.2 不可行初始点牛顿法

利用 (10.19) 定义的牛顿步 $\Delta x_{\mathrm{nt}}$，可以扩展牛顿法，允许 $x^{(0)}\in\mathbf{dom}\,f$ 不一定满足 $Ax^{(0)}=b$。这里还要使用牛顿步的对偶部分：按 (10.19) 的记号为 $\Delta\nu_{\mathrm{nt}}=w-\nu$，等价地，按 (10.21) 的记号为 $\Delta\nu_{\mathrm{nt}}=\Delta\nu_{\mathrm{pd}}$。

<div class="algorithm" id="algorithm-10-2" data-algorithm="10.2" markdown="1">

**算法 10.2 不可行初始点牛顿法。**

**给定** 初始点 $x\in\mathbf{dom}\,f$、$\nu$，容差 $\epsilon>0$，$\alpha\in(0,1/2)$，$\beta\in(0,1)$。

**重复执行**

1. 计算原牛顿步和对偶牛顿步 $\Delta x_{\mathrm{nt}}$、$\Delta\nu_{\mathrm{nt}}$。

2. 对 $\|r\|_2$ 进行回溯直线搜索。

    $t:=1$。

    **当** $\|r(x+t\Delta x_{\mathrm{nt}},\nu+t\Delta\nu_{\mathrm{nt}})\|_2>(1-\alpha t)\|r(x,\nu)\|_2$ 时，$t:=\beta t$。

3. **更新。** $x:=x+t\Delta x_{\mathrm{nt}}$，$\nu:=\nu+t\Delta\nu_{\mathrm{nt}}$。

**直到** $Ax=b$ 且 $\|r(x,\nu)\|_2\leq\epsilon$。

</div>

<!-- pdf-page: 549 -->

这个算法与从可行初始点出发的标准牛顿法十分相似，但有几处区别。首先，搜索方向中包含依赖于原残差的额外修正项。其次，直线搜索使用的是残差的范数，而不是函数值 $f$。最后，当满足原可行性、且（对偶）残差的范数足够小时，算法终止。

第 2 步的直线搜索值得作一些说明。与基于函数值的直线搜索相比，使用残差的范数可能会增加计算量，但增加的部分通常可以忽略。此外，直线搜索必定在有限步内终止，因为 (10.23) 表明，当 $t$ 足够小时，直线搜索的退出条件成立。

方程 (10.24) 表明，若某次迭代选择步长为一，则下一个迭代点将是可行点。此后，所有迭代点都可行。因此，一旦得到一个可行迭代点，不可行初始点牛顿法的搜索方向，就与 §10.2 中介绍的（可行）牛顿法的搜索方向相同。

不可行初始点牛顿法有许多变体。例如，一旦达到可行性，就可以切换到 §10.2 中介绍的（可行）牛顿法。（换言之，将直线搜索改为基于 $f$ 的搜索，并在 $\lambda(x)^2/2\leq\epsilon$ 时终止。）达到可行性后，不可行初始点牛顿法与标准（可行）牛顿法仅在回溯条件和退出条件上有区别，两者的表现十分相似。

#### 用不可行初始点牛顿法简化初始化

不可行初始点牛顿法的主要优点在于它对初始化的要求。若 $\mathbf{dom}\,f=\mathbf{R}^n$，初始化（可行）牛顿法只需要求出 $Ax=b$ 的一个解，此时使用不可行初始点牛顿法，除了方便之外，并没有特别的优势。

当 $\mathbf{dom}\,f$ 不是整个 $\mathbf{R}^n$ 时，要在 $\mathbf{dom}\,f$ 中找到一个满足 $Ax=b$ 的点，本身就可能很困难。一种通用的办法是使用第一阶段方法（phase I method，见 §11.4），求出这样的点（或验证 $\mathbf{dom}\,f$ 与 $\{z\mid Az=b\}$ 不相交）；当 $\mathbf{dom}\,f$ 复杂，且不知道它是否与 $\{z\mid Az=b\}$ 相交时，这也许是最好的办法。不过，当 $\mathbf{dom}\,f$ 比较简单，且已知其中包含满足 $Ax=b$ 的点时，不可行初始点牛顿法提供了另一种简单的选择。

一个常见的例子是 $\mathbf{dom}\,f=\mathbf{R}_{++}^n$，例如例 10.2 中的带等式约束的解析中心问题。为初始化求解问题

$$
\begin{array}{ll}
\text{最小化} & -\displaystyle\sum_{i=1}^n\log x_i\\
\text{约束条件} & Ax=b
\end{array}
\tag{10.25}
$$

的牛顿法，需要找到满足 $Ax=b$ 的点 $x^{(0)}\succ0$，这等价于求解一个标准形式 LP 的可行性问题。可以用第一阶段方法完成这项工作；也可以使用不可行初始点牛顿法，从任意正初始点出发，例如 $x^{(0)}=\mathbf{1}$。

同样的技巧也能用于初始化无约束问题，此时我们还不知道 $\mathbf{dom}\,f$ 中的初始点。例如，考虑带等式约束的<!-- pdf-page: 550 -->解析中心问题 (10.25) 的对偶问题，

$$
\begin{array}{ll}
\text{最大化} & g(\nu)=-b^T\nu+n+\displaystyle\sum_{i=1}^n\log(A^T\nu)_i.
\end{array}
$$

为了初始化求解这个问题的（可行初始点）牛顿法，必须找到满足 $A^T\nu^{(0)}\succ0$ 的点 $\nu^{(0)}$，即必须求解一组线性不等式。可以使用第一阶段方法，也可以先改写问题，再使用不可行初始点牛顿法。首先将其写成等式约束问题，

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu+n+\displaystyle\sum_{i=1}^n\log y_i\\
\text{约束条件} & y=A^T\nu,
\end{array}
$$

其中新增变量为 $y\in\mathbf{R}^n$。现在就可以使用不可行初始点牛顿法，从任意正的 $y^{(0)}$（以及任意 $\nu^{(0)}$）出发。

对于不知道严格可行初始点的问题，使用不可行初始点牛顿法进行初始化有一个缺点：没有明确的方法可以检测出严格可行点不存在；残差的范数只会缓慢地收敛到某个正值。（相比之下，第一阶段方法可以明确判定这一事实。）此外，在达到可行性之前，不可行初始点牛顿法可能收敛很慢；见 §11.4.2。

### 10.3.3 收敛分析

本节证明，在某些假设成立时，不可行初始点牛顿法收敛到最优点。收敛性证明与标准牛顿法或含等式约束的标准牛顿法的证明十分相似。我们将证明，一旦残差的范数足够小，算法就会采用完整步长（这意味着达到可行性），随后以二次速度收敛。我们还将证明，在进入二次收敛区域之前，每次迭代都会使残差的范数至少减小一个固定量。由于残差的范数不可能为负，这说明在有限步内，残差就会小到足以保证完整步长和二次收敛。

#### 假设

我们作如下假设。

- 下水平集

    $$
    S=\{(x,\nu)\mid x\in\mathbf{dom}\,f,\ \|r(x,\nu)\|_2\leq\|r(x^{(0)},\nu^{(0)})\|_2\}
    \tag{10.26}
    $$

    是闭集。若 $f$ 是闭函数，则 $\|r\|_2$ 是闭函数，因而对任意 $x^{(0)}\in\mathbf{dom}\,f$ 和任意 $\nu^{(0)}\in\mathbf{R}^p$，这个条件都成立（见习题 10.7）。

- 在集合 $S$ 上，有

    $$
    \|Dr(x,\nu)^{-1}\|_2
    =\left\|\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}^{-1}\right\|_2\leq K,
    \tag{10.27}
    $$

    <!-- pdf-page: 551 -->

    其中 $K$ 为某个常数。

- 对 $(x,\nu),(\tilde x,\tilde\nu)\in S$，$Dr$ 满足 Lipschitz 条件

    $$
    \|Dr(x,\nu)-Dr(\tilde x,\tilde\nu)\|_2
    \leq L\|(x,\nu)-(\tilde x,\tilde\nu)\|_2.
    $$

    （这等价于 $\nabla^2f(x)$ 满足 Lipschitz 条件；见习题 10.7。）

下面将会看到，这些假设意味着 $\mathbf{dom}\,f$ 与 $\{z\mid Az=b\}$ 相交，而且存在最优点 $(x^\star,\nu^\star)$。

#### 与标准牛顿法的比较

上述假设与 §10.2.4（第 529 页）分析标准牛顿法时所作的假设十分相似。第二项和第三项，即 KKT 矩阵的逆有界及 Lipschitz 条件，基本相同。不过，不可行初始点牛顿法的下水平集条件 (10.26)，比 §10.2.4 中的下水平集条件更一般。

例如，考虑带等式约束的熵最大化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=\displaystyle\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Ax=b,
\end{array}
$$

其中 $\mathbf{dom}\,f=\mathbf{R}_{++}^n$。目标函数 $f$ 不是闭函数；它有一些下水平集不是闭集，所以标准牛顿法中的假设可能不成立，至少对某些初始点是这样。问题在于，当 $x_i\to0$ 时，负熵函数并不趋于 $\infty$。另一方面，不可行初始点牛顿法的下水平集条件 (10.26) 对这个问题确实成立，因为当 $x_i\to0$ 时，负熵函数梯度的范数确实趋于 $\infty$。因此，可以保证不可行初始点牛顿法求解这个带等式约束的熵最大化问题。（我们并不知道标准牛顿法是否会在这个问题上失败；这里只是指出，我们的收敛分析不适用。）注意，若初始点满足等式约束，则标准牛顿法与不可行初始点牛顿法的唯一区别在于直线搜索，而这些直线搜索仅在阻尼阶段有所不同。

#### 一个基本不等式

首先推导一个基本不等式。设 $y=(x,\nu)\in S$ 且 $\|r(y)\|_2\neq0$，令 $\Delta y_{\mathrm{nt}}=(\Delta x_{\mathrm{nt}},\Delta\nu_{\mathrm{nt}})$ 为 $y$ 处的牛顿步。定义

$$
t_{\max}=\inf\{t>0\mid y+t\Delta y_{\mathrm{nt}}\notin S\}.
$$

若对所有 $t\geq0$ 都有 $y+t\Delta y_{\mathrm{nt}}\in S$，则按通常约定定义 $t_{\max}=\infty$。否则，$t_{\max}$ 是使 $\|r(y+t\Delta y_{\mathrm{nt}})\|_2=\|r(y^{(0)})\|_2$ 成立的最小正数 $t$。特别地，当 $0\leq t\leq t_{\max}$ 时，有 $y+t\Delta y_{\mathrm{nt}}\in S$。

我们将证明

$$
\|r(y+t\Delta y_{\mathrm{nt}})\|_2
\leq(1-t)\|r(y)\|_2+(K^2L/2)t^2\|r(y)\|_2^2
\tag{10.28}
$$

<!-- pdf-page: 552 -->

对 $0\leq t\leq\min\{1,t_{\max}\}$ 成立。

有

$$
\begin{aligned}
r(y+t\Delta y_{\mathrm{nt}})
&=r(y)+\int_0^1Dr(y+\tau t\Delta y_{\mathrm{nt}})t\Delta y_{\mathrm{nt}}\,d\tau\\
&=r(y)+tDr(y)\Delta y_{\mathrm{nt}}
+\int_0^1\bigl(Dr(y+\tau t\Delta y_{\mathrm{nt}})-Dr(y)\bigr)t\Delta y_{\mathrm{nt}}\,d\tau\\
&=r(y)+tDr(y)\Delta y_{\mathrm{nt}}+e\\
&=(1-t)r(y)+e,
\end{aligned}
$$

其中使用了 $Dr(y)\Delta y_{\mathrm{nt}}=-r(y)$，并定义

$$
e=\int_0^1\bigl(Dr(y+\tau t\Delta y_{\mathrm{nt}})-Dr(y)\bigr)t\Delta y_{\mathrm{nt}}\,d\tau.
$$

现在假设 $0\leq t\leq t_{\max}$，所以对 $0\leq\tau\leq1$，有 $y+\tau t\Delta y_{\mathrm{nt}}\in S$。可以如下估计 $\|e\|_2$ 的上界：

$$
\begin{aligned}
\|e\|_2
&\leq\|t\Delta y_{\mathrm{nt}}\|_2\int_0^1\|Dr(y+\tau t\Delta y_{\mathrm{nt}})-Dr(y)\|_2\,d\tau\\
&\leq\|t\Delta y_{\mathrm{nt}}\|_2\int_0^1L\|\tau t\Delta y_{\mathrm{nt}}\|_2\,d\tau\\
&=(L/2)t^2\|\Delta y_{\mathrm{nt}}\|_2^2\\
&=(L/2)t^2\|Dr(y)^{-1}r(y)\|_2^2\\
&\leq(K^2L/2)t^2\|r(y)\|_2^2,
\end{aligned}
$$

其中第二行用了 Lipschitz 条件，最后一行用了界 $\|Dr(y)^{-1}\|_2\leq K$。现在可以推导界 (10.28)：对 $0\leq t\leq\min\{1,t_{\max}\}$，

$$
\begin{aligned}
\|r(y+t\Delta y_{\mathrm{nt}})\|_2
&=\|(1-t)r(y)+e\|_2\\
&\leq(1-t)\|r(y)\|_2+\|e\|_2\\
&\leq(1-t)\|r(y)\|_2+(K^2L/2)t^2\|r(y)\|_2^2.
\end{aligned}
$$

#### 阻尼牛顿阶段

首先证明，若 $\|r(y)\|_2>1/(K^2L)$，则不可行初始点牛顿法的一次迭代会使 $\|r\|_2$ 至少减小某个固定量。

基本不等式 (10.28) 的右端是 $t$ 的二次函数，在 $t=0$ 与其最小点

$$
\bar t=\frac{1}{K^2L\|r(y)\|_2}<1
$$

之间单调递减。

必有 $t_{\max}>\bar t$，否则会推出 $\|r(y+t_{\max}\Delta y_{\mathrm{nt}})\|_2<\|r(y)\|_2$，而这是不成立的。因此，基本不等式在 $t=\bar t$ 处成立，从而

$$
\begin{aligned}
\|r(y+\bar t\Delta y_{\mathrm{nt}})\|_2
&\leq\|r(y)\|_2-1/(2K^2L)\\
&\leq\|r(y)\|_2-\alpha/(K^2L)\\
&=(1-\alpha\bar t)\|r(y)\|_2,
\end{aligned}
$$

<!-- pdf-page: 553 -->

这表明步长 $\bar t$ 满足直线搜索的退出条件。因此有 $t\geq\beta\bar t$，其中 $t$ 是回溯算法选定的步长。由 $t\geq\beta\bar t$ 和回溯直线搜索的退出条件，得到

$$
\begin{aligned}
\|r(y+t\Delta y_{\mathrm{nt}})\|_2
&\leq(1-\alpha t)\|r(y)\|_2\\
&\leq(1-\alpha\beta\bar t)\|r(y)\|_2\\
&=\left(1-\frac{\alpha\beta}{K^2L\|r(y)\|_2}\right)\|r(y)\|_2\\
&=\|r(y)\|_2-\frac{\alpha\beta}{K^2L}.
\end{aligned}
$$

所以，只要 $\|r(y)\|_2>1/(K^2L)$，每次迭代中 $\|r\|_2$ 就至少减小 $\alpha\beta/(K^2L)$。因此，至多经过

$$
\frac{\|r(y^{(0)})\|_2K^2L}{\alpha\beta}
$$

次迭代，就有 $\|r(y^{(k)})\|_2\leq1/(K^2L)$。

#### 二次收敛阶段

现在假设 $\|r(y)\|_2\leq1/(K^2L)$。基本不等式给出

$$
\|r(y+t\Delta y_{\mathrm{nt}})\|_2
\leq\bigl(1-t+(1/2)t^2\bigr)\|r(y)\|_2
\tag{10.29}
$$

对 $0\leq t\leq\min\{1,t_{\max}\}$ 成立。必有 $t_{\max}>1$，否则由 (10.29) 会得到 $\|r(y+t_{\max}\Delta y_{\mathrm{nt}})\|_2<\|r(y)\|_2$，与 $t_{\max}$ 的定义矛盾。因此，不等式 (10.29) 对 $t=1$ 成立，即

$$
\|r(y+\Delta y_{\mathrm{nt}})\|_2
\leq(1/2)\|r(y)\|_2\leq(1-\alpha)\|r(y)\|_2.
$$

这表明 $t=1$ 满足回溯直线搜索的退出准则，所以会采用完整步长。而且，所有后续迭代都满足 $\|r(y)\|_2\leq1/(K^2L)$，所以此后每次迭代也都会采用完整步长。

将不等式 (10.28) 在 $t=1$ 时写成

$$
\frac{K^2L\|r(y^+)\|_2}{2}
\leq\left(\frac{K^2L\|r(y)\|_2}{2}\right)^2,
$$

其中 $y^+=y+\Delta y_{\mathrm{nt}}$。因此，若某次迭代满足 $\|r(y)\|_2\leq1/K^2L$，并用 $r(y^{+k})$ 表示此后 $k$ 步的残差，则

$$
\frac{K^2L\|r(y^{+k})\|_2}{2}
\leq\left(\frac{K^2L\|r(y)\|_2}{2}\right)^{2^k}
\leq\left(\frac12\right)^{2^k},
$$

即 $\|r(y)\|_2$ 以二次速度收敛到零。

为证明迭代点序列收敛，我们证明它是 Cauchy 序列。假设迭代点 $y$ 满足 $\|r(y)\|_2\leq1/(K^2L)$，并用 $y^{+k}$ 表示<!-- pdf-page: 554 -->$y$ 之后的第 $k$ 个迭代点。由于这些迭代点位于二次收敛区域，步长为一，所以有

$$
\begin{aligned}
\|y^{+k}-y\|_2
&\leq\|y^{+k}-y^{+(k-1)}\|_2+\cdots+\|y^+-y\|_2\\
&=\|Dr(y^{+(k-1)})^{-1}r(y^{+(k-1)})\|_2+\cdots+\|Dr(y)^{-1}r(y)\|_2\\
&\leq K\bigl(\|r(y^{+(k-1)})\|_2+\cdots+\|r(y)\|_2\bigr)\\
&\leq K\|r(y)\|_2\sum_{i=0}^{k-1}\left(\frac{K^2L\|r(y)\|_2}{2}\right)^{2^i-1}\\
&\leq K\|r(y)\|_2\sum_{i=0}^{k-1}\left(\frac12\right)^{2^i-1}\\
&\leq2K\|r(y)\|_2,
\end{aligned}
$$

其中第三行使用了对所有迭代点都有 $\|Dr^{-1}\|_2\leq K$ 这一假设。由于 $\|r(y^{(k)})\|_2$ 收敛到零，可知 $y^{(k)}$ 是 Cauchy 序列，因而收敛。由 $r$ 的连续性，极限点 $y^\star$ 满足 $r(y^\star)=0$。这就证明了前面的断言：本节开头的假设意味着存在最优点 $(x^\star,\nu^\star)$。

### 10.3.4 凸–凹博弈

不可行初始点牛顿法的收敛性证明表明，该方法的适用范围比等式约束凸优化问题更广。假设 $r:\mathbf{R}^n\to\mathbf{R}^n$ 可微，其导数在 $S$ 上满足 Lipschitz 条件，且 $\|Dr(x)^{-1}\|_2$ 在 $S$ 上有界，其中

$$
S=\{x\in\mathbf{dom}\,r\mid\|r(x)\|_2\leq\|r(x^{(0)})\|_2\}
$$

是闭集。那么，从 $x^{(0)}$ 出发的不可行初始点牛顿法，收敛到 $S$ 中 $r(x)=0$ 的一个解。在不可行初始点牛顿法中，我们将这一结论用于一个特定情形：$r$ 是等式约束凸优化问题的残差。不过，它也适用于其他一些值得研究的情形。求解凸–凹博弈就是其中一例。（其他相关博弈的讨论见 §5.4.3 和习题 5.25。）

$\mathbf{R}^p\times\mathbf{R}^q$ 上的一个无约束（零和、双人）博弈，由其*支付函数* $f:\mathbf{R}^{p+q}\to\mathbf{R}$ 定义。其含义是：参与者 1 选择一个值（或行动）$u\in\mathbf{R}^p$，参与者 2 选择一个值（或行动）$v\in\mathbf{R}^q$；根据这些选择，参与者 1 向参与者 2 支付金额 $f(u,v)$。参与者 1 的目标是最小化这笔支付，而参与者 2 的目标是最大化它。

若参与者 1 先作出选择 $u$，而参与者 2 知道这个选择，那么参与者 2 就会选择 $v$ 使 $f(u,v)$ 最大，由此得到的支付为 $\sup_v f(u,v)$（假设上确界能够达到）。若参与者 1 预期参与者 2 会作出这样的选择，他就应选择使 $\sup_v f(u,v)$ 最小的 $u$。这样，参与者 1 向参与者 2 的支付将为

$$
\inf_u\sup_v f(u,v)
\tag{10.30}
$$

<!-- pdf-page: 555 -->

（假设上确界能够达到）。另一方面，若参与者 2 先作出选择，双方的策略顺序便会颠倒，参与者 1 向参与者 2 的支付为

$$
\sup_v\inf_u f(u,v).
\tag{10.31}
$$

支付 (10.30) 总是大于或等于支付 (10.31)；两笔支付之差，可以解释为后行动者在知道对方行动的情况下所获得的优势。如果对所有 $u,v$，都有

$$
f(u^\star,v)\leq f(u^\star,v^\star)\leq f(u,v^\star),
$$

则称 $(u^\star,v^\star)$ 为这个博弈的*解*，或博弈的*鞍点*。当解存在时，后行动并无优势；$f(u^\star,v^\star)$ 就是两笔支付 (10.30) 和 (10.31) 的共同值。（见习题 3.14。）

若对每个 $v$，$f(u,v)$ 都是 $u$ 的凸函数，且对每个 $u$，$f(u,v)$ 都是 $v$ 的凹函数，则称该博弈为*凸–凹博弈*。当 $f$ 可微（且凸–凹）时，博弈的鞍点由 $\nabla f(u^\star,v^\star)=0$ 刻画。

#### 用不可行初始点牛顿法求解

对于支付函数二阶可微的凸–凹博弈，可以用不可行初始点牛顿法求解。将残差定义为

$$
r(u,v)=\nabla f(u,v)=\begin{bmatrix}\nabla_u f(u,v)\\\nabla_v f(u,v)\end{bmatrix},
$$

然后使用不可行初始点牛顿法。在博弈的语境下，不可行初始点牛顿法就简称为（凸–凹博弈的）牛顿法。

只要 $Dr=\nabla^2f$ 的逆有界，并且它在下水平集

$$
S=\{(u,v)\in\mathbf{dom}\,f\mid\|r(u,v)\|_2\leq\|r(u^{(0)},v^{(0)})\|_2\}
$$

上满足 Lipschitz 条件，就能保证（不可行初始点）牛顿法收敛，其中 $u^{(0)},v^{(0)}$ 是双方的初始选择。

这里也有一个简单的条件，对应于无约束最小化问题中的强凸性条件。如果存在某个 $m>0$，使得对所有 $(u,v)\in S$ 都有 $\nabla_{uu}^2f(u,v)\succeq mI$ 和 $\nabla_{vv}^2f(u,v)\preceq-mI$，就称支付函数为 $f$ 的博弈是*强凸–凹*的。不难预料，这个强凸–凹假设能推出逆有界的条件（习题 10.10）。

### 10.3.5 算例

#### 一个简单算例

<p id="ch10-simple-example-end" markdown="1">我们用带等式约束的解析中心问题 (10.25) 来展示不可行初始点牛顿法。第一个算例是随机生成的，规模为 $n=100$、$m=50$，问题可行且有下界。采用不可行初始点牛顿法，初始原<!-- pdf-page: 556 -->、对偶点为 $x^{(0)}=\mathbf{1}$、$\nu^{(0)}=0$，回溯参数为 $\alpha=0.01$、$\beta=0.5$。图 10.1 分别给出原残差和对偶残差的范数随迭代次数的变化，图 10.2 给出步长。在第 8 次迭代中，算法采用了完整牛顿步，因此原残差变为（几乎）零，并一直保持为（几乎）零。大约从第 9 次迭代开始，（对偶）残差以二次速度收敛到零。</p>

#### 一个不可行算例

<p id="ch10-infeasible-example-end" markdown="1">再考虑一个与上述算例规模相同的问题，但这次 $\mathbf{dom}\,f$ 与 $\{z\mid Az=b\}$ 不相交，即问题不可行。（这违背了本章关于问题 (10.1) 可解的基本假设，也违背了 §10.2.4 中的假设；这个算例只是为了展示，当 $\mathbf{dom}\,f$ 与 $\{z\mid Az=b\}$ 不相交时，不可行初始点牛顿法会有怎样的表现。）这个算例的残差范数如图 10.3 所示，步长如图 10.4 所示。当然，这里的步长从未等于一，残差也不收敛到零。</p>

#### 一个凸–凹博弈

最后一个算例是 $\mathbf{R}^{100}\times\mathbf{R}^{100}$ 上的凸–凹博弈，支付函数为

$$
f(u,v)=u^TAv+b^Tu+c^Tv-\log(1-u^Tu)+\log(1-v^Tv),
\tag{10.32}
$$

其定义域为

$$
\mathbf{dom}\,f=\{(u,v)\mid u^Tu<1,\ v^Tv<1\}.
$$

<p id="ch10-game-example-end" markdown="1">问题数据 $A$、$b$ 和 $c$ 均随机生成。从 $u^{(0)}=v^{(0)}=0$ 出发、回溯参数为 $\alpha=0.01$ 和 $\beta=0.5$ 的（不可行初始点）牛顿法，其求解过程如图 10.5 所示。</p>

## 10.4 实现

### 10.4.1 消元

为实现消元法，需要计算一个满秩矩阵 $F$ 和一个 $\hat x$，使

$$
\{x\mid Ax=b\}=\{Fz+\hat x\mid z\in\mathbf{R}^{n-p}\}.
$$

§C.5 介绍了几种计算它们的方法。

### 10.4.2 求解 KKT 方程组

<p id="ch10-kkt-intro-start" markdown="1">本节介绍计算牛顿步或不可行牛顿步的方法，两者都需要求解一组线性方程，</p>

<!-- pdf-page: 557 -->

<figure id="fig-10-1" data-figure="10.1" data-reader-after-previous="ch10-simple-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-1.png" alt="不可行初始点牛顿法的原残差和对偶残差范数随迭代次数变化；实线在第 8 次迭代陡降，虚线随后陡降，纵轴为对数刻度。" data-source-page="557" data-source-rect="145,155,418,354.6">
<figcaption>图 10.1 不可行初始点牛顿法求解一个带等式约束的解析中心问题时的迭代过程，该问题有 $100$ 个变量和 $50$ 个约束。图中给出了 $\|r_{\mathrm{pri}}\|_2$（实线）和 $\|r_{\mathrm{dual}}\|_2$（虚线）。注意，经过 $8$ 次迭代后便达到并保持可行，约从第 $9$ 次迭代开始呈二次收敛。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数；$\|r_{\mathrm{pri}}\|_2$ and $\|r_{\mathrm{dual}}\|_2$——$\|r_{\mathrm{pri}}\|_2$ 与 $\|r_{\mathrm{dual}}\|_2$。</p>
</figure>

<figure id="fig-10-2" data-figure="10.2" data-reader-after-previous="ch10-simple-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-2.png" alt="步长 t 随迭代次数变化；第 1 至第 7 次迭代的步长为 0.5，第 8 次起步长为 1，空心圆标出各次迭代的取值。" data-source-page="557" data-source-rect="158,412,398,597.4">
<figcaption>图 10.2 同一个算例中，步长随迭代次数的变化。第 $8$ 次迭代取完整步长，因而从该次迭代起保持可行。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<!-- pdf-page: 558 -->

<figure id="fig-10-3" data-figure="10.3" data-reader-after-previous="ch10-infeasible-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-3.png" alt="不可行算例中，原残差范数的实线下降后逐渐变平，对偶残差范数的虚线经过起伏后也逐渐变平；两者均未趋于零，纵轴为对数刻度。" data-source-page="558" data-source-rect="207,158,471,357.4">
<figcaption>图 10.3 不可行初始点牛顿法求解一个带等式约束的解析中心问题时的迭代过程，该问题有 $100$ 个变量和 $50$ 个约束，且 $\mathbf{dom}\,f=\mathbf{R}_{++}^{100}$ 与 $\{z\mid Az=b\}$ 不相交。图中给出了 $\|r_{\mathrm{pri}}\|_2$（实线）和 $\|r_{\mathrm{dual}}\|_2$（虚线）。在这种情况下，残差不收敛到零。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数；$\|r_{\mathrm{pri}}\|_2$ and $\|r_{\mathrm{dual}}\|_2$——$\|r_{\mathrm{pri}}\|_2$ 与 $\|r_{\mathrm{dual}}\|_2$。</p>
</figure>

<figure id="fig-10-4" data-figure="10.4" data-reader-after-previous="ch10-infeasible-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-4.png" alt="不可行算例的步长 t 随迭代次数变化；最初几次为 0.25，随后逐级下降并趋近零，所有步长都小于 1。" data-source-page="558" data-source-rect="212,413,452,602.5">
<figcaption>图 10.4 不可行算例中，步长随迭代次数的变化。从未取完整步长，且步长收敛到零。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<!-- pdf-page: 559 -->

<figure id="fig-10-5" data-figure="10.5" data-reader-after-previous="ch10-game-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-5.png" alt="凸–凹博弈中，梯度范数 ‖∇f(u,v)‖₂ 随迭代次数下降，约从第 5 次迭代之后下降明显加快；纵轴为对数刻度。" data-source-page="559" data-source-rect="147,112,417,308.5">
<figcaption>图 10.5 将牛顿法（从不可行初始点出发）用于凸–凹博弈时的迭代过程。约在 $5$ 次迭代之后，可以明显看出二次收敛。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<p id="ch10-kkt-intro-end" markdown="1" data-reader-continue="ch10-kkt-intro-start">其 KKT 形式为</p>

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}v\\w\end{bmatrix}
=-\begin{bmatrix}g\\h\end{bmatrix}.
\tag{10.33}
$$

这里假定 $H\in\mathbf{S}_+^n$，$A\in\mathbf{R}^{p\times n}$，且 $\mathbf{rank}\,A=p<n$。也可以用类似方法计算凸–凹博弈的牛顿步，此时系数矩阵右下角的分块为半负定矩阵（见习题 10.13）。

#### 求解完整 KKT 方程组

一种直接的办法是求解 KKT 方程组 (10.33)，它由 $n+p$ 个变量的 $n+p$ 个线性方程组成。KKT 矩阵对称但不正定，因此一种合适的求解方法是使用 $LDL^T$ 分解（见 §C.3.3）。若不利用矩阵的任何结构，计算量为 $(1/3)(n+p)^3$ 次浮点运算。当问题规模较小（即 $n$ 和 $p$ 都不太大），或者 $A$ 和 $H$ 稀疏时，这可能是一种合理的办法。

#### 通过消元求解 KKT 方程组

一种通常比直接求解完整 KKT 方程组更好的方法，是消去变量 $v$（见 §C.4）。首先介绍最简单的情形，即 $H\succ0$。从 KKT 方程组

$$
Hv+A^Tw=-g,\qquad Av=-h
$$

中的第一个方程解出 $v$，得到

$$
v=-H^{-1}(g+A^Tw).
$$

<!-- pdf-page: 560 -->

将其代入第二个 KKT 方程，得到 $AH^{-1}(g+A^Tw)=h$，所以

$$
w=(AH^{-1}A^T)^{-1}(h-AH^{-1}g).
$$

这些公式给出了计算 $v$ 和 $w$ 的一种方法。

$w$ 的公式中出现的矩阵，是 KKT 矩阵中关于 $H$ 的 Schur 补 $S$：

$$
S=-AH^{-1}A^T.
$$

由于 KKT 矩阵的特殊结构，以及 $A$ 的秩为 $p$ 这一假设，矩阵 $S$ 为负定矩阵。

<div class="algorithm" id="algorithm-10-3" data-algorithm="10.3" markdown="1">

**算法 10.3 用分块消元求解 KKT 方程组。**

**给定** 满足 $H\succ0$ 的 KKT 方程组。

1. 形成 $H^{-1}A^T$ 和 $H^{-1}g$。

2. 形成 Schur 补 $S=-AH^{-1}A^T$。

3. 求解 $Sw=AH^{-1}g-h$，确定 $w$。

4. 求解 $Hv=-A^Tw-g$，确定 $v$。

</div>

第 1 步可以先对 $H$ 作 Cholesky 分解，再求解 $p+1$ 个方程组，计算量为 $f+(p+1)s$，其中 $f$ 是分解 $H$ 的计算量，$s$ 是利用该分解求解一次方程组的计算量。第 2 步需要进行一次 $p\times n$ 矩阵与 $n\times p$ 矩阵的乘法。若在计算中不利用任何结构，计算量为 $p^2n$ 次浮点运算。（由于结果对称，只需计算 $S$ 的上三角部分。）在某些情况下，可以利用 $A$ 和 $H$ 的特殊结构，更高效地完成第 2 步。第 3 步可以通过对 $-S$ 作 Cholesky 分解来完成；若不进一步利用 $S$ 的结构，其计算量为 $(1/3)p^3$ 次浮点运算。第 4 步可以利用第 1 步中已经算出的 $H$ 的分解来完成，所以计算量为 $2np+s$ 次浮点运算。假定在形成和分解 Schur 补时不利用任何结构，总浮点运算次数为

$$
f+ps+p^2n+(1/3)p^3
$$

（只保留主导项）。若在形成或分解 $S$ 时利用结构，最后两项还会更小。

若能高效地分解 $H$，则相比于直接用 $LDL^T$ 分解求解 KKT 方程组，分块消元在浮点运算次数上就具有优势。例如，若 $H$ 为对角矩阵（对应于可分离目标函数），则 $f=0$、$s=n$，总计算量为 $p^2n+(1/3)p^3$ 次浮点运算，仅随 $n$ 线性增长。若 $H$ 为带宽 $k\ll n$ 的带状矩阵，则 $f=nk^2$、$s=4nk$，总计算量约为 $nk^2+4nkp+p^2n+(1/3)p^3$，仍然仅随 $n$ 线性增长。$H$ 还可能具有其他可利用的结构，例如分块对角（对应于分块可分离目标函数）、稀疏，或对角加低秩结构；更多细节和例子见附录 C 及 §9.7。

<div class="example" id="example-10-3" markdown="1">

**例 10.3 带等式约束的解析中心。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & -\displaystyle\sum_{i=1}^n\log x_i\\
\text{约束条件} & Ax=b.
\end{array}
$$

<!-- pdf-page: 561 -->

这里目标函数可分离，所以在 $x$ 处的 Hessian 矩阵为对角矩阵：

$$
H=\mathbf{diag}(x_1^{-2},\ldots,x_n^{-2}).
$$

若使用对 KKT 矩阵作 $LDL^T$ 分解这样的通用方法计算牛顿方向，计算量为 $(1/3)(n+p)^3$ 次浮点运算。

若用分块消元计算牛顿步，计算量为 $np^2+(1/3)p^3$ 次浮点运算，远小于通用方法的计算量。

事实上，这与第 525 页例 10.2 中所述对偶问题的牛顿步计算量相同。对于这个（无约束）对偶问题，Hessian 矩阵为

$$
H_{\mathrm{dual}}=-ADA^T,
$$

其中 $D$ 为对角矩阵，$D_{ii}=(A^T\nu)_i^{-2}$。形成该矩阵需要 $np^2$ 次浮点运算，通过对 $-H_{\mathrm{dual}}$ 作 Cholesky 分解求出牛顿步，则需要 $(1/3)p^3$ 次浮点运算。

</div>

<div class="example" id="example-10-4" markdown="1">

**例 10.4 满足等式约束的最短分段线性曲线。** 考虑 $\mathbf{R}^2$ 中的一条分段线性曲线，其节点为 $(0,0),(1,x_1),\ldots,(n,x_n)$。为了找出满足等式约束 $Ax=b$ 的最短曲线，构造问题

$$
\begin{array}{ll}
\text{最小化} & (1+x_1^2)^{1/2}+\displaystyle\sum_{i=1}^{n-1}\bigl(1+(x_{i+1}-x_i)^2\bigr)^{1/2}\\
\text{约束条件} & Ax=b,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$，$A\in\mathbf{R}^{p\times n}$。这个问题的目标函数是若干函数之和，每个函数只依赖于一对相邻变量，所以 Hessian 矩阵 $H$ 为三对角矩阵。用分块消元，可以在约 $p^2n+(1/3)p^3$ 次浮点运算内算出牛顿步。

</div>

#### $H$ 奇异时的消元

当 $H$ 奇异时，上述分块消元法显然无法直接使用，但对该方法稍作修改，就能处理这种更一般的情形。这个更一般的方法基于如下结论：KKT 矩阵非奇异，当且仅当存在某个 $Q\succeq0$，使 $H+A^TQA\succ0$；此时，对所有 $Q\succ0$，都有 $H+A^TQA\succ0$。（见习题 10.1。）例如，可以由此得出，若 KKT 矩阵非奇异，则 $H+A^TA\succ0$。

设 $Q\succeq0$ 满足 $H+A^TQA\succ0$。那么 KKT 方程组 (10.33) 等价于

$$
\begin{bmatrix}H+A^TQA&A^T\\A&0\end{bmatrix}
\begin{bmatrix}v\\w\end{bmatrix}
=-\begin{bmatrix}g+A^TQh\\h\end{bmatrix},
$$

由于 $H+A^TQA\succ0$，可以用消元法求解。

### 10.4.3 算例

本节介绍几个较详细的算例，展示如何利用结构高效地计算牛顿步，同时给出一些数值结果。

<!-- pdf-page: 562 -->

#### 带等式约束的解析中心

考虑带等式约束的解析中心问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=-\displaystyle\sum_{i=1}^n\log x_i\\
\text{约束条件} & Ax=b.
\end{array}
$$

（见例 10.2 和例 10.3。）对于一个规模为 $p=100$、$n=500$ 的问题，我们比较三种方法。

第一种方法是含等式约束的牛顿法（§10.2）。牛顿步 $\Delta x_{\mathrm{nt}}$ 由 KKT 方程组 (10.11) 定义：

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\w\end{bmatrix}
=\begin{bmatrix}-g\\0\end{bmatrix},
$$

其中 $H=\mathbf{diag}(1/x_1^2,\ldots,1/x_n^2)$，$g=-(1/x_1,\ldots,1/x_n)$。如第 546 页例 10.3 所述，这个 KKT 方程组可以通过消元高效求解，即求解

$$
AH^{-1}A^Tw=-AH^{-1}g,
$$

然后令 $\Delta x_{\mathrm{nt}}=-H^{-1}(A^Tw+g)$。换言之，

$$
\Delta x_{\mathrm{nt}}=-\mathbf{diag}(x)^2A^Tw+x,
$$

其中 $w$ 是下列方程的解：

$$
A\mathbf{diag}(x)^2A^Tw=b.
\tag{10.34}
$$

<p id="ch10-primal-method-end" markdown="1">图 10.6 给出误差随迭代次数的变化。不同曲线对应四个不同的初始点。我们采用参数为 $\alpha=0.1$、$\beta=0.5$ 的回溯直线搜索。</p>

第二种方法是对对偶问题使用牛顿法，

$$
\begin{array}{ll}
\text{最大化} & g(\nu)=-b^T\nu+\displaystyle\sum_{i=1}^n\log(A^T\nu)_i+n
\end{array}
$$

（见第 525 页例 10.2）。此时，牛顿步通过求解

$$
A\mathbf{diag}(y)^2A^T\Delta\nu_{\mathrm{nt}}=-b+Ay
\tag{10.35}
$$

<p id="ch10-dual-method-end" markdown="1">得到，其中 $y=(1/(A^T\nu)_1,\ldots,1/(A^T\nu)_n)$。比较 (10.35) 和 (10.34)，可见两种方法具有相同的复杂度。图 10.7 给出四个不同初始点的误差。我们采用参数为 $\alpha=0.1$、$\beta=0.5$ 的回溯直线搜索。</p>

第三种方法是将 §10.3 的不可行初始点牛顿法用于最优性条件

$$
\nabla f(x^\star)+A^T\nu^\star=0,\qquad Ax^\star=b.
$$

牛顿步通过求解

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\Delta\nu_{\mathrm{nt}}\end{bmatrix}
=-\begin{bmatrix}g+A^T\nu\\Ax-b\end{bmatrix}
$$

<p id="ch10-third-kkt-where-start" markdown="1">得到，</p>

<!-- pdf-page: 563 -->

<figure id="fig-10-6" data-figure="10.6" data-no-english-text="true" data-reader-after-previous="ch10-primal-method-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-6.png" alt="四个不同起始点对应的牛顿法误差曲线；横轴为迭代次数 k，纵轴为 f(x⁽ᵏ⁾)−p⋆ 的对数刻度，各曲线在最后几次迭代中迅速下降。" data-source-page="563" data-source-rect="144,132,417,329.6">
<figcaption>图 10.6 将牛顿法用于规模为 $p=100$、$n=500$ 的带等式约束的解析中心问题时，误差 $f(x^{(k)})-p^\star$ 的变化。不同曲线对应四个不同的起始点。最终阶段的二次收敛十分明显。</figcaption>
</figure>

<figure id="fig-10-7" data-figure="10.7" data-no-english-text="true" data-reader-after-previous="ch10-dual-method-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-7.png" alt="对偶问题中四条牛顿法曲线随迭代次数 k 下降；纵轴标为 p⋆−g(ν⁽ᵏ⁾)，采用对数刻度，各曲线在后几次迭代中迅速下降。" data-source-page="563" data-source-rect="144,429,418,627.2">
<figcaption>图 10.7 将牛顿法用于带等式约束的解析中心问题的对偶问题时，误差 $|g(\nu^{(k)})-p^\star|$ 的变化。</figcaption>
</figure>

<!-- pdf-page: 564 -->

<figure id="fig-10-8" data-figure="10.8" data-no-english-text="true" data-reader-after="ch10-infeasible-method-plot-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-8.png" alt="不可行初始点牛顿法的四条残差范数曲线；横轴为迭代次数 k，纵轴为 ‖r(x⁽ᵏ⁾,ν⁽ᵏ⁾)‖₂ 的对数刻度，各曲线先逐渐下降，随后迅速降至很小。" data-source-page="564" data-source-rect="198,112,471,307.3">
<figcaption>图 10.8 将不可行初始点牛顿法用于带等式约束的解析中心问题时，残差 $\|r(x^{(k)},\nu^{(k)})\|_2$ 的变化。</figcaption>
</figure>

<p id="ch10-third-kkt-where-end" markdown="1" data-reader-continue="ch10-third-kkt-where-start">其中 $H=\mathbf{diag}(1/x_1^2,\ldots,1/x_n^2)$，$g=-(1/x_1,\ldots,1/x_n)$。这个 KKT 方程组可以通过消元高效求解，计算量与 (10.34) 或 (10.35) 相同。例如，先求解</p>

$$
A\mathbf{diag}(x)^2A^Tw=2Ax-b,
$$

再由

$$
\Delta\nu_{\mathrm{nt}}=w-\nu,\qquad
\Delta x_{\mathrm{nt}}=x-\mathbf{diag}(x)^2A^Tw
$$

得到 $\Delta\nu_{\mathrm{nt}}$ 和 $\Delta x_{\mathrm{nt}}$。

图 10.8 给出四个不同初始点下，残差

$$
r(x,\nu)=(\nabla f(x)+A^T\nu,Ax-b)
$$

<p id="ch10-infeasible-method-plot-end" markdown="1">的范数随迭代次数的变化。我们采用参数为 $\alpha=0.1$、$\beta=0.5$ 的回溯直线搜索。</p>

这些图表明，对这个问题而言，对偶方法似乎更快，不过也只是快了两三倍。它约需六次迭代便进入二次收敛区域，而原方法需要 12–15 次，不可行初始点牛顿法需要 10–20 次。

这些方法对初始化的要求也有所不同。原方法要求已知一个原可行点，即满足 $Ax^{(0)}=b$、$x^{(0)}\succ0$。对偶方法要求一个对偶可行点，即 $A^T\nu^{(0)}\succ0$。视具体问题而定，其中一种点可能比另一种更容易获得。不可行初始点牛顿法不需要初始化；唯一的要求是 $x^{(0)}\succ0$。

#### 最优网络流

考虑一个连通的有向图或网络，它有 $n$ 条边、$p+1$ 个节点。用 $x_j$ 表示弧 $j$ 上的流量或流，$x_j>0$ 表示沿<!-- pdf-page: 565 -->弧的方向流动，$x_j<0$ 表示沿弧的反方向流动。另外，给定一个外部源（或汇）流量 $s_i$，它进入节点 $i$（若 $s_i>0$）或离开节点 $i$（若 $s_i<0$）。流必须满足守恒方程，即在每个节点，计入外部源和汇后，流入该节点的总流量为零。这个守恒方程可写成 $\tilde Ax=s$，其中 $\tilde A\in\mathbf{R}^{(p+1)\times n}$ 为图的*节点关联矩阵*，

$$
\tilde A_{ij}=\begin{cases}
1 & \text{弧 }j\text{ 离开节点 }i,\\
-1 & \text{弧 }j\text{ 进入节点 }i,\\
0 & \text{其他情形。}
\end{cases}
$$

除非 $\mathbf{1}^Ts=0$，否则流守恒方程 $\tilde Ax=s$ 无解；我们假定这个条件成立。（换言之，所有源流量的总和必须等于所有汇流量的总和。）由于 $\mathbf{1}^T\tilde A=0$，流守恒方程组 $\tilde Ax=s$ 还存在冗余。为了得到一组独立方程，可以删去其中任意一个方程，得到 $Ax=b$，其中 $A\in\mathbf{R}^{p\times n}$ 是图的*约化节点关联矩阵*（即删去一行的节点关联矩阵），$b\in\mathbf{R}^p$ 是约化源向量（即从 $s$ 中删去对应的分量）。

综上，流守恒由 $Ax=b$ 表示，其中 $A$ 为图的约化节点关联矩阵，$b$ 为约化源向量。矩阵 $A$ 非常稀疏，因为每一列至多有两个非零元素（只能为 $+1$ 或 $-1$）。

我们以流量 $x$ 为变量，并将源流量视为给定量。引入目标函数

$$
f(x)=\sum_{i=1}^n\phi_i(x_i),
$$

其中 $\phi_i:\mathbf{R}\to\mathbf{R}$ 是弧 $i$ 的流量代价函数。假设这些流量代价函数严格凸且二阶可微。

在满足流守恒要求的条件下选择最优流的问题为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n\phi_i(x_i)\\
\text{约束条件} & Ax=b.
\end{array}
\tag{10.36}
$$

由于目标函数可分离，这里的 Hessian 矩阵 $H$ 为对角矩阵。

计算最优网络流问题 (10.36) 的牛顿步有几种方法。最直接的是使用稀疏 $LDL^T$ 分解求解完整 KKT 方程组。

对这个问题，采用分块消元来计算牛顿步可能更好。Schur 补 $S=-AH^{-1}A^T$ 的稀疏模式可以用图来描述：$S_{ij}\neq0$ 当且仅当节点 $i$ 和节点 $j$ 之间有一条弧相连。因此，若网络稀疏，即每个节点仅通过弧与少数其他节点相连，则 Schur 补 $S$ 也稀疏。此时，在形成 $S$ 以及随后进行分解和求解的各个步骤中，都可以利用稀疏性。可以预期，计算牛顿步的计算复杂度近似地随弧的数量（即变量个数）线性增长。

<!-- pdf-page: 566 -->

#### 最优控制

考虑问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{t=1}^N\phi_t(z(t))+\displaystyle\sum_{t=0}^{N-1}\psi_t(u(t))\\
\text{约束条件} & z(t+1)=A_tz(t)+B_tu(t),\quad t=0,\ldots,N-1.
\end{array}
$$

这里

- $z(t)\in\mathbf{R}^k$ 是时刻 $t$ 的系统状态；

- $u(t)\in\mathbf{R}^l$ 是时刻 $t$ 的输入或控制动作；

- $\phi_t:\mathbf{R}^k\to\mathbf{R}$ 是状态代价函数；

- $\psi_t:\mathbf{R}^l\to\mathbf{R}$ 是输入代价函数；

- $N$ 称为该问题的*时间跨度*（time horizon）。

假设输入和状态的代价函数都严格凸且二阶可微。问题的变量为 $u(0),\ldots,u(N-1)$ 和 $z(1),\ldots,z(N)$。初始状态 $z(0)$ 已知。线性等式约束称为*状态方程*或*动态演化方程*。将整个优化变量 $x$ 定义为

$$
x=(u(0),z(1),u(1),\ldots,u(N-1),z(N))\in\mathbf{R}^{N(k+l)}.
$$

由于目标函数分块可分离（即分别以 $z(t)$ 或 $u(t)$ 为变量的函数之和），Hessian 矩阵为分块对角矩阵：

$$
H=\mathbf{diag}(R_0,Q_1,\ldots,R_{N-1},Q_N),
$$

其中

$$
R_t=\nabla^2\psi_t(u(t)),\quad t=0,\ldots,N-1,\qquad
Q_t=\nabla^2\phi_t(z(t)),\quad t=1,\ldots,N.
$$

将所有等式约束（即状态方程）合在一起，写成 $Ax=b$，其中

$$
\begin{aligned}
A&=\begin{bmatrix}
-B_0&I&0&0&0&\cdots&0&0&0\\
0&-A_1&-B_1&I&0&\cdots&0&0&0\\
0&0&0&-A_2&-B_2&\cdots&0&0&0\\
\vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots\\
0&0&0&0&0&\cdots&I&0&0\\
0&0&0&0&0&\cdots&-A_{N-1}&-B_{N-1}&I
\end{bmatrix}\\
b&=\begin{bmatrix}A_0z(0)\\0\\0\\\vdots\\0\\0\end{bmatrix}.
\end{aligned}
$$

<!-- pdf-page: 567 -->

$A$ 的行数（即等式约束的数量）为 $Nk$。

若用稠密 $LDL^T$ 分解直接求解 KKT 方程组来得到牛顿步，需要

$$
(1/3)(2Nk+Nl)^3=(1/3)N^3(2k+l)^3
$$

次浮点运算。采用稀疏 $LDL^T$ 分解会有很大改进，因为该方法会利用 $A$ 和 $H$ 中的大量零元素。

事实上，可以利用 $H$ 和 $A$ 的特殊分块结构，通过分块消元来计算牛顿步，进一步提高效率。Schur 补 $S=-AH^{-1}A^T$ 是分块三对角矩阵，每个分块为 $k\times k$：

$$
\begin{aligned}
S&=-AH^{-1}A^T\\
&=\begin{bmatrix}
S_{11}&Q_1^{-1}A_1^T&0&\cdots&0&0\\
A_1Q_1^{-1}&S_{22}&Q_2^{-1}A_2^T&\cdots&0&0\\
0&A_2Q_2^{-1}&S_{33}&\cdots&0&0\\
\vdots&\vdots&\vdots&\ddots&\vdots&\vdots\\
0&0&0&\cdots&S_{N-1,N-1}&Q_{N-1}^{-1}A_{N-1}^T\\
0&0&0&\cdots&A_{N-1}Q_{N-1}^{-1}&S_{NN}
\end{bmatrix},
\end{aligned}
$$

其中

$$
\begin{aligned}
S_{11}&=-B_0R_0^{-1}B_0^T-Q_1^{-1},\\
S_{ii}&=-A_{i-1}Q_{i-1}^{-1}A_{i-1}^T-B_{i-1}R_{i-1}^{-1}B_{i-1}^T-Q_i^{-1},
\quad i=2,\ldots,N.
\end{aligned}
$$

特别地，$S$ 是带宽为 $2k-1$ 的带状矩阵，因此可以用 $k^3N$ 量级的浮点运算完成分解。所以，假设 $k\ll N$，就能用 $k^3N$ 量级的浮点运算算出牛顿步。注意，这仅随时间跨度 $N$ 线性增长，而通用方法的浮点运算次数则按 $N^3$ 增长。

对这个问题，还可以进一步利用 $S$ 的分块三对角结构。应用标准的分块三对角分解方法，就会得到求解二次最优控制问题的经典 Riccati 递推。不过，仅利用 $S$ 的带状结构，也能得到相同量级的算法。

#### 线性矩阵不等式的解析中心

考虑问题

$$
\begin{array}{ll}
\text{最小化} & f(X)=-\log\det X\\
\text{约束条件} & \mathbf{tr}(A_iX)=b_i,\quad i=1,\ldots,p,
\end{array}
\tag{10.37}
$$

其中变量为 $X\in\mathbf{S}^n$，$A_i\in\mathbf{S}^n$，$b_i\in\mathbf{R}$，且 $\mathbf{dom}\,f=\mathbf{S}_{++}^n$。这个问题的 KKT 条件为

$$
-X^{\star-1}+\sum_{i=1}^m\nu_i^\star A_i=0,\qquad
\mathbf{tr}(A_iX^\star)=b_i,\quad i=1,\ldots,p.
\tag{10.38}
$$

<div class="translator-note" markdown="1">

**译注：求和的上限。** 式 (10.38) 的求和上限原印为 $m$；本例有 $p$ 个等式约束，按上下文，上限应为 $p$。

</div>

变量 $X$ 的维数为 $n(n+1)/2$。可以直接忽略 $X$ 的特殊矩阵结构，将其视为（向量）变量 $x\in\mathbf{R}^{n(n+1)/2}$，<!-- pdf-page: 568 -->并用通用方法求解问题 (10.37)，将它当作一个具有 $n(n+1)/2$ 个变量和 $p$ 个等式约束的问题。此时，计算一个牛顿步至少需要

$$
(1/3)(n(n+1)/2+p)^3
$$

次浮点运算，关于 $n$ 而言是 $n^6$ 量级。下面会看到几种好得多的选择。

第一种选择是求解对偶问题。$f$ 的共轭函数为

$$
f^*(Y)=\log\det(-Y)^{-1}-n,
$$

其定义域为 $\mathbf{dom}\,f^*=-\mathbf{S}_{++}^n$（见第 92 页例 3.23），因此对偶问题为

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu+\log\det\left(\displaystyle\sum_{i=1}^p\nu_iA_i\right)+n,
\end{array}
\tag{10.39}
$$

其定义域为 $\{\nu\mid\sum_{i=1}^p\nu_iA_i\succ0\}$。这是一个变量为 $\nu\in\mathbf{R}^p$ 的无约束问题。通过求解 (10.38) 中的第一个（对偶可行性）方程，可以由最优解 $\nu^\star$ 恢复最优解 $X^\star$，即 $X^\star=(\sum_{i=1}^p\nu_i^\star A_i)^{-1}$。

下面计算对偶问题 (10.39) 的牛顿步所需的运算量。需要先形成 $g$ 的梯度和 Hessian 矩阵，再求解牛顿步。梯度和 Hessian 矩阵由下式给出：

$$
\begin{aligned}
\nabla^2g(\nu)_{ij}&=-\mathbf{tr}(A^{-1}A_iA^{-1}A_j),\quad i,j=1,\ldots,p,\\
\nabla g(\nu)_i&=\mathbf{tr}(A^{-1}A_i)-b_i,\quad i=1,\ldots,p,
\end{aligned}
$$

其中 $A=\sum_{i=1}^p\nu_iA_i$。按如下步骤形成 $\nabla^2g(\nu)$ 和 $\nabla g(\nu)$。首先形成 $A$（$pn^2$ 次浮点运算），以及每个 $j$ 对应的 $A^{-1}A_j$（$2pn^3$ 次浮点运算）。然后形成矩阵 $\nabla^2g(\nu)$。$\nabla^2g(\nu)$ 的 $p(p+1)/2$ 个元素，每个都是 $\mathbf{S}^n$ 中两个矩阵的内积，每次内积需要 $n(n+1)$ 次浮点运算，所以总计（忽略低阶项）需要 $(1/2)p^2n^2$ 次浮点运算。由于矩阵 $A^{-1}A_i$ 已经算出，形成 $\nabla g(\nu)$ 的计算量很小。最后，求出牛顿步 $-\nabla^2g(\nu)^{-1}\nabla g(\nu)$，需要 $(1/3)p^3$ 次浮点运算。合起来，只保留主导项，计算牛顿步的总运算量为 $2pn^3+(1/2)p^2n^2+(1/3)p^3$。注意，关于 $n$ 而言，这是 $n^3$ 量级，远优于上述 $n^6$ 量级的简单原方法。

也可以利用特殊的矩阵结构，更高效地求解原问题。为推导可行点 $X$ 处牛顿步 $\Delta X_{\mathrm{nt}}$ 的 KKT 方程组，在 KKT 条件中用 $X+\Delta X_{\mathrm{nt}}$ 替代 $X^\star$，用 $w$ 替代 $\nu^\star$，并利用一阶近似

$$
(X+\Delta X_{\mathrm{nt}})^{-1}\approx X^{-1}-X^{-1}\Delta X_{\mathrm{nt}}X^{-1}
$$

将第一个方程线性化。由此得到 KKT 方程组

$$
-X^{-1}+X^{-1}\Delta X_{\mathrm{nt}}X^{-1}+\sum_{i=1}^pw_iA_i=0,\qquad
\mathbf{tr}(A_i\Delta X_{\mathrm{nt}})=0,\quad i=1,\ldots,p.
\tag{10.40}
$$

这是关于变量 $\Delta X_{\mathrm{nt}}\in\mathbf{S}^n$ 和 $w\in\mathbf{R}^p$ 的 $n(n+1)/2+p$ 个线性方程。若用通用方法求解，计算量将为 $n^6$ 量级。

<!-- pdf-page: 569 -->

利用分块消元，可以高效得多地求解 KKT 方程组 (10.40)。从第一个方程解出变量 $\Delta X_{\mathrm{nt}}$，得到

$$
\Delta X_{\mathrm{nt}}
=X-X\left(\sum_{i=1}^pw_iA_i\right)X
=X-\sum_{i=1}^pw_iXA_iX.
\tag{10.41}
$$

将这个 $\Delta X_{\mathrm{nt}}$ 的表达式代入另一个方程，得到

$$
\mathbf{tr}(A_j\Delta X_{\mathrm{nt}})
=\mathbf{tr}(A_jX)-\sum_{i=1}^pw_i\mathbf{tr}(A_jXA_iX)=0,\quad j=1,\ldots,p.
$$

这是一组关于 $w$ 的 $p$ 个线性方程：

$$
Cw=d,
$$

其中 $C_{ij}=\mathbf{tr}(A_iXA_jX)$，$d_i=\mathbf{tr}(A_iX)$。系数矩阵 $C$ 对称正定，所以可以用 Cholesky 分解求出 $w$。得到 $w$ 后，就能由 (10.41) 算出 $\Delta X_{\mathrm{nt}}$。

这个方法的计算量如下。先形成乘积 $A_iX$（$2pn^3$ 次浮点运算），再形成矩阵 $C$。$C$ 的 $p(p+1)/2$ 个元素，每个都是 $\mathbf{R}^{n\times n}$ 中两个矩阵的内积，所以形成 $C$ 需要 $p^2n^2$ 次浮点运算。然后求出 $w=C^{-1}d$，计算量为 $(1/3)p^3$。最后计算 $\Delta X_{\mathrm{nt}}$。若采用 (10.41) 中的第一个表达式，即先计算求和，再在左、右两侧分别乘以 $X$，计算量约为 $pn^2+3n^3$。合起来，用分块消元计算原问题的牛顿步，总共需要 $2pn^3+p^2n^2+(1/3)p^3$ 次浮点运算。这远优于 $n^6$ 量级的简单方法。还应注意，这与计算对偶问题的牛顿步具有相同的计算量。

<div class="translator-note" markdown="1">

**译注：形成 Hessian 矩阵的计算量。** 前面对偶法先计算的 $A^{-1}A_i$ 一般并不对称。若由这些乘积逐项计算迹，形成 Hessian 矩阵的主导计算量为 $p^2n^2$，与本段原问题的计数一致；若要利用对称矩阵结构，可改用 $A^{-1/2}A_iA^{-1/2}$。原问题与对偶问题的牛顿步，其复杂度量级相同。

</div>

<!-- pdf-page: 570 -->

## 文献说明

在不可行初始点牛顿法的分析中，两个关键假设（导数 $Dr$ 的逆有界且满足 Lipschitz 条件），也是大多数牛顿法收敛性证明的核心；见 Ortega 和 Rheinboldt [OR00] 以及 Dennis 和 Schnabel [DS96]。

直接分解完整方程组与通过消元求解 KKT 方程组，这两种方法各自的优劣，已在线性规划和二次规划的内点法研究中得到广泛探讨；例如，见 Wright [Wri97, 第 11 章] 以及 Nocedal 和 Wright [NW99, §16.1-2]。最优控制中的 Riccati 递推，可以解释为利用第 552 页算例中 Schur 补 $S$ 的分块三对角结构的一种方法。Rao、Wright 和 Rawlings [RWR98, §3.3] 指出了这一点。

<!-- pdf-page: 571 -->

## 习题

### 等式约束最小化

**10.1 KKT 矩阵的非奇异性。** 考虑 KKT 矩阵

$$
\begin{bmatrix}P&A^T\\A&0\end{bmatrix},
$$

其中 $P\in\mathbf{S}_+^n$，$A\in\mathbf{R}^{p\times n}$，且 $\mathbf{rank}\,A=p<n$。

- (a) 证明，下列各项陈述都与 KKT 矩阵非奇异等价。

    - $\mathcal{N}(P)\cap\mathcal{N}(A)=\{0\}$。

    - $Ax=0,\ x\neq0\implies x^TPx>0$。

    - $F^TPF\succ0$，其中 $F\in\mathbf{R}^{n\times(n-p)}$ 满足 $\mathcal{R}(F)=\mathcal{N}(A)$。

    - 存在某个 $Q\succeq0$，使 $P+A^TQA\succ0$。

- (b) 证明，若 KKT 矩阵非奇异，则它恰有 $n$ 个正特征值和 $p$ 个负特征值。

**10.2 投影梯度法。** 本题探讨如何把梯度法扩展到等式约束最小化问题。假设 $f$ 凸且可微，$x\in\mathbf{dom}\,f$ 满足 $Ax=b$，其中 $A\in\mathbf{R}^{p\times n}$，且 $\mathbf{rank}\,A=p<n$。负梯度 $-\nabla f(x)$ 在 $\mathcal{N}(A)$ 上的 Euclidean 投影为

$$
\Delta x_{\mathrm{pg}}=\mathop{\operatorname{argmin}}_{Au=0}\|-\nabla f(x)-u\|_2.
$$

- (a) 设 $(v,w)$ 是方程组

    $$
    \begin{bmatrix}I&A^T\\A&0\end{bmatrix}
    \begin{bmatrix}v\\w\end{bmatrix}
    =\begin{bmatrix}-\nabla f(x)\\0\end{bmatrix}
    $$

    的唯一解。证明 $v=\Delta x_{\mathrm{pg}}$，且 $w=\operatorname{argmin}_y\|\nabla f(x)+A^Ty\|_2$。

- (b) 假设 $F^TF=I$，投影后的负梯度 $\Delta x_{\mathrm{pg}}$ 与约化问题 (10.5) 的负梯度之间有什么关系？

- (c) 求解等式约束最小化问题的*投影梯度法*采用步 $\Delta x_{\mathrm{pg}}$，并对 $f$ 作回溯直线搜索。利用 (b) 的结果，给出一些条件，使得投影梯度法从满足 $Ax^{(0)}=b$ 的点 $x^{(0)}\in\mathbf{dom}\,f$ 出发时，能够收敛到最优解。

### 含等式约束的牛顿法

**10.3 对偶牛顿法。** 本题探讨用牛顿法求解等式约束最小化问题 (10.1) 的对偶问题。假设 $f$ 二阶可微，对所有 $x\in\mathbf{dom}\,f$ 都有 $\nabla^2f(x)\succ0$，并且对每个 $\nu\in\mathbf{R}^p$，拉格朗日函数 $L(x,\nu)=f(x)+\nu^T(Ax-b)$ 都有唯一的最小点，记为 $x(\nu)$。

- (a) 证明，对偶函数 $g$ 二阶可微。用 $f$、$\nabla f$ 和 $\nabla^2f$ 在 $x=x(\nu)$ 处的值，给出对偶函数 $g$ 在 $\nu$ 处的牛顿步表达式。可以使用习题 3.40 的结果。

    <!-- pdf-page: 572 -->

- (b) 假设存在一个 $K$，使得对所有 $x\in\mathbf{dom}\,f$，都有

    $$
    \left\|\begin{bmatrix}\nabla^2f(x)&A^T\\A&0\end{bmatrix}^{-1}\right\|_2\leq K.
    $$

    证明，$g$ 强凹，且 $\nabla^2g(\nu)\preceq-(1/K)I$。

**10.4 约化问题的强凸性与 Lipschitz 常数。** 假设 $f$ 满足第 529 页给出的假设。证明，约化后的目标函数 $\tilde f(z)=f(Fz+\hat x)$ 强凸，并且它的 Hessian 矩阵（在对应的下水平集 $\tilde S$ 上）Lipschitz 连续。用 $K$、$M$、$L$ 以及 $F$ 的最大、最小奇异值，表示 $\tilde f$ 的强凸性常数和 Lipschitz 常数。

**10.5 给目标函数加上二次项。** 假设 $Q\succeq0$。问题

$$
\begin{array}{ll}
\text{最小化} & f(x)+(Ax-b)^TQ(Ax-b)\\
\text{约束条件} & Ax=b
\end{array}
$$

与原等式约束优化问题 (10.1) 等价。这个问题的牛顿步与原问题的牛顿步相同吗？

**10.6 牛顿减量。** 证明 (10.13) 成立，即

$$
f(x)-\inf\{\hat f(x+v)\mid A(x+v)=b\}=\lambda(x)^2/2.
$$


### 不可行初始点牛顿法

**10.7 不可行初始点牛顿法的假设。** 考虑第 536 页给出的那组假设。

- (a) 假设函数 $f$ 是闭函数。证明，这意味着残差的范数 $\|r(x,\nu)\|_2$ 也是闭函数。

- (b) 证明，$Dr$ 满足 Lipschitz 条件，当且仅当 $\nabla^2f$ 满足 Lipschitz 条件。

**10.8 不可行初始点牛顿法与初始时已满足的等式约束。** 假设我们使用不可行初始点牛顿法，在约束 $a_i^Tx=b_i$，$i=1,\ldots,p$ 下最小化 $f(x)$。

- (a) 假设初始点 $x^{(0)}$ 满足线性等式 $a_i^Tx=b_i$。证明，以后的迭代点也始终满足这个线性等式，即对所有 $k$ 都有 $a_i^Tx^{(k)}=b_i$。

- (b) 假设其中一个等式约束在第 $k$ 次迭代时变为满足，即 $a_i^Tx^{(k-1)}\neq b_i$，而 $a_i^Tx^{(k)}=b_i$。证明，在第 $k$ 次迭代时，所有等式约束都已满足。

**10.9 带等式约束的熵最大化问题。** 考虑带等式约束的熵最大化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Ax=b,
\end{array}
\tag{10.42}
$$

其中 $\mathbf{dom}\,f=\mathbf{R}_{++}^n$，$A\in\mathbf{R}^{p\times n}$。我们假设问题可行，并且 $\mathbf{rank}\,A=p<n$。

- (a) 证明，该问题有唯一的最优解 $x^\star$。

- (b) 找出 $A$、$b$ 以及可行点 $x^{(0)}$，使下水平集

    $$
    \{x\in\mathbf{R}_{++}^n\mid Ax=b,\ f(x)\leq f(x^{(0)})\}
    $$

    不是闭集。因此，对于某些可行初始点，§10.2.4（第 529 页）列出的假设并不成立。

    <!-- pdf-page: 573 -->

- (c) 证明，对于任意可行初始点，问题 (10.42) 都满足 §10.3.3（第 536 页）列出的不可行初始点牛顿法的假设。

- (d) 推导 (10.42) 的拉格朗日对偶问题，并说明如何从对偶问题的最优解求出 (10.42) 的最优解。证明，对于任意初始点，对偶问题都满足 §10.2.4（第 529 页）列出的假设。

(b)、(c) 和 (d) 的结果并不意味着标准牛顿法会失败，也不意味着不可行初始点牛顿法或对偶方法在实际中表现更好。这些结果仅表明，我们对标准牛顿法的收敛分析不适用，而对不可行初始点牛顿法和对偶方法的收敛分析适用。（见习题 10.15。）

**10.10 强凸–凹博弈的导数逆矩阵有界条件。** 考虑支付函数为 $f$ 的凸–凹博弈（见第 541 页）。假设对所有 $(u,v)\in\mathbf{dom}\,f$，都有 $\nabla_{uu}^2f(u,v)\succeq mI$ 和 $\nabla_{vv}^2f(u,v)\preceq-mI$。证明

$$
\|Dr(u,v)^{-1}\|_2=\|\nabla^2f(u,v)^{-1}\|_2\leq1/m.
$$


### 实现

**10.11** 考虑例 10.1 中的资源分配问题。可以假设 $f_i$ 强凸，即对所有 $z$ 都有 $f_i''(z)\geq m>0$。

- (a) 求出计算约化问题的一个牛顿步所需的计算量。务必利用牛顿方程组的特殊结构。

- (b) 说明如何通过对偶问题求解原问题。可以假设共轭函数 $f_i^\star$ 及其导数容易计算，并且给定 $\nu$ 后，容易从方程 $f_i'(x)=\nu$ 中解出 $x$。求对偶问题的一个牛顿步，其计算复杂度是多少？

- (c) 计算资源分配问题的一个牛顿步，其计算复杂度是多少？务必利用 KKT 方程组的特殊结构。

**10.12** 说明一种高效计算下列问题的牛顿步的方法：

$$
\begin{array}{ll}
\text{最小化} & \mathbf{tr}(X^{-1})\\
\text{约束条件} & \mathbf{tr}(A_iX)=b_i,\quad i=1,\ldots,p,
\end{array}
$$

其定义域为 $\mathbf{S}_{++}^n$，假设 $p$ 与 $n$ 属于同一数量级。还要推导其拉格朗日对偶问题，并给出求对偶问题的牛顿步的计算复杂度。

**10.13 用消元法计算凸–凹博弈的牛顿步。** 考虑支付函数为 $f:\mathbf{R}^p\times\mathbf{R}^q\to\mathbf{R}$ 的凸–凹博弈（见第 541 页）。假设 $f$ 强凸–凹，即存在某个 $m>0$，使得对所有 $(u,v)\in\mathbf{dom}\,f$，都有 $\nabla_{uu}^2f(u,v)\succeq mI$ 和 $\nabla_{vv}^2f(u,v)\preceq-mI$。

- (a) 说明如何利用 $\nabla_{uu}^2f(u,v)$ 和 $-\nabla^2f_{vv}(u,v)$ 的 Cholesky 分解计算牛顿步。假设 $\nabla^2f(u,v)$ 稠密，将此方法的计算量与利用 $\nabla f(u,v)$ 的 $LDL^T$ 分解所需的计算量作比较。

- (b) 说明如何利用 $\nabla_{uu}^2f(u,v)$ 和／或 $\nabla_{vv}^2f(u,v)$ 的对角或分块对角结构。假设 $\nabla_{uv}^2f(u,v)$ 稠密，能够节省多少计算量？

<div class="translator-note" markdown="1">

**译注：习题 10.13 的导数记号。** 本题 (a) 中的 $-\nabla^2f_{vv}(u,v)$ 应理解为 $-\nabla_{vv}^2f(u,v)$，即关于 $v$ 的 Hessian 分块的相反数；$LDL^T$ 分解的对象应为整体 Hessian 矩阵 $\nabla^2f(u,v)$，原文此处漏写上标 $2$。

</div>

### 数值实验

**10.14 对数最优投资。** 考虑习题 4.60 中的对数最优投资问题，但去掉约束 $x\succeq0$。用牛顿法求解，<!-- pdf-page: 574 -->问题数据如下：有 $n=3$ 种资产和 $m=4$ 个情景，收益向量为

$$
p_1=\begin{bmatrix}2\\1.3\\1\end{bmatrix},\qquad
p_2=\begin{bmatrix}2\\0.5\\1\end{bmatrix},\qquad
p_3=\begin{bmatrix}0.5\\1.3\\1\end{bmatrix},\qquad
p_4=\begin{bmatrix}0.5\\0.5\\1\end{bmatrix}.
$$

四个情景的概率为 $\pi=(1/3,1/6,1/3,1/6)$。

**10.15 等式约束熵最大化。** 考虑等式约束熵最大化问题

$$
\begin{array}{ll}
\text{最小化} & f(x)=\displaystyle\sum_{i=1}^nx_i\log x_i\\
\text{约束条件} & Ax=b,
\end{array}
$$

其中 $\mathbf{dom}\,f=\mathbf{R}_{++}^n$，$A\in\mathbf{R}^{p\times n}$，且 $p<n$。（相关分析见习题 10.9。）

生成一个 $n=100$、$p=30$ 的问题实例：随机选取 $A$（检查它是否满秩），再随机选取正向量 $\hat x$（例如，各分量在 $[0,1]$ 上均匀分布），然后令 $b=A\hat x$。（这样，$\hat x$ 就是可行点。）

用以下方法求解这个问题。

- (a) *标准牛顿法。* 可以采用初始点 $x^{(0)}=\hat x$。

- (b) *不可行初始点牛顿法。* 可以采用初始点 $x^{(0)}=\hat x$（以便与标准牛顿法比较），也可以采用初始点 $x^{(0)}=\mathbf{1}$。

- (c) *对偶牛顿法*，即对偶问题上的标准牛顿法。

验证这三种方法求得相同的最优点（和拉格朗日乘子）。假设利用了相关结构，比较三种方法每一步所需的计算量。（不过，你的实现不必利用结构来计算牛顿步。）

**10.16 凸–凹博弈。** 随机生成数据，用不可行初始点牛顿法求解具有 (10.32) 形式的凸–凹博弈。画出残差范数和步长随迭代次数变化的曲线。试验不同的直线搜索参数和初始点（但初始点必须满足 $\|u\|_2<1$、$\|v\|_2<1$）。
