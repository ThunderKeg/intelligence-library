<!-- pdf-page: 141 -->

# 第 4 章 凸优化问题

<aside class="chapter-guide"><p>导读（编者）：本章把凸集与凸函数用于建立优化问题。先明确可行性、最优解和等价变换，再给出凸优化的判别条件，并介绍线性规划、二次规划、几何规划和半定规划等常见形式。阅读时要留意：同一个问题可以有不同的表达形式，合适的变量与约束形式往往能使它的凸性显现出来。本章最后还讨论多个目标之间的权衡。</p></aside>

## 4.1 优化问题

### 4.1.1 基本术语

我们用记号

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p
\end{array}
\tag{4.1}
$$

描述这样的问题：在所有满足条件 $f_i(x)\leq0$，$i=1,\ldots,m$，以及 $h_i(x)=0$，$i=1,\ldots,p$ 的 $x$ 中，寻找使 $f_0(x)$ 最小的 $x$。我们称 $x\in\mathbf{R}^n$ 为**优化变量**，称函数 $f_0:\mathbf{R}^n\to\mathbf{R}$ 为**目标函数**或**代价函数**。不等式 $f_i(x)\leq0$ 称为**不等式约束**，相应的函数 $f_i:\mathbf{R}^n\to\mathbf{R}$ 称为**不等式约束函数**。等式 $h_i(x)=0$ 称为**等式约束**，函数 $h_i:\mathbf{R}^n\to\mathbf{R}$ 称为**等式约束函数**。如果没有约束（即 $m=p=0$），就称问题 (4.1) 为**无约束**问题。

目标函数和所有约束函数都有定义的点所构成的集合

$$
\mathcal{D}=\bigcap_{i=0}^m\operatorname{\mathbf{dom}}f_i\;\cap\;\bigcap_{i=1}^p\operatorname{\mathbf{dom}}h_i,
$$

称为优化问题 (4.1) 的**定义域**。如果点 $x\in\mathcal{D}$ 满足约束 $f_i(x)\leq0$，$i=1,\ldots,m$，以及 $h_i(x)=0$，$i=1,\ldots,p$，就称它是**可行的**。如果至少存在一个可行点，就称问题 (4.1) **可行**；否则称它**不可行**。所有可行点组成的集合称为**可行集**或**约束集**。

问题 (4.1) 的**最优值** $p^\star$ 定义为

$$
p^\star=\inf\{f_0(x)\mid f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p\}.
$$

我们允许 $p^\star$ 取扩展值 $\pm\infty$。如果问题不可行，就有 $p^\star=\infty$（按照通常约定，空集的下确界<!-- pdf-page: 142 -->是 $\infty$）。如果存在可行点 $x_k$，使得当 $k\to\infty$ 时，$f_0(x_k)\to-\infty$，那么 $p^\star=-\infty$，此时称问题 (4.1) **下方无界**。

#### 最优点与局部最优点

如果 $x^\star$ 可行且 $f_0(x^\star)=p^\star$，就称 $x^\star$ 是一个**最优点**，或者说它**求解了**问题 (4.1)。所有最优点组成的集合称为**最优解集**，记为

$$
X_{\mathrm{opt}}=\{x\mid f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p,\ f_0(x)=p^\star\}.
$$

如果问题 (4.1) 存在最优点，就说最优值**能够取到**，并称该问题**可解**。如果 $X_{\mathrm{opt}}$ 为空，就说最优值**不能取到**。（当问题下方无界时，总是如此。）满足 $f_0(x)\leq p^\star+\epsilon$（其中 $\epsilon>0$）的可行点 $x$ 称为 **$\epsilon$-次优点**，所有 $\epsilon$-次优点组成的集合称为问题 (4.1) 的 **$\epsilon$-次优解集**。

如果存在 $R>0$，使得

$$
\begin{aligned}
f_0(x)=\inf\{f_0(z)\mid{}&f_i(z)\leq0,\ i=1,\ldots,m,\\
&h_i(z)=0,\ i=1,\ldots,p,\ \|z-x\|_2\leq R\},
\end{aligned}
$$

就称可行点 $x$ 是**局部最优的**。换句话说，$x$ 是以下以 $z$ 为变量的优化问题的解：

$$
\begin{array}{ll}
\text{最小化} & f_0(z)\\
\text{约束条件} & f_i(z)\leq0,\quad i=1,\ldots,m\\
& h_i(z)=0,\quad i=1,\ldots,p\\
& \|z-x\|_2\leq R.
\end{array}
$$

粗略地说，这意味着在可行集中与 $x$ 邻近的点上，$x$ 使 $f_0$ 最小。有时也用“全局最优”代替“最优”，以区分“局部最优”和“最优”。不过，在本书中，“最优”始终指全局最优。

如果 $x$ 可行且 $f_i(x)=0$，就说第 $i$ 个不等式约束 $f_i(x)\leq0$ 在 $x$ 处是**有效的**（active）。如果 $f_i(x)<0$，就说约束 $f_i(x)\leq0$ 是**非有效的**（inactive）。（等式约束在所有可行点处都是有效的。）如果删除一个约束不会改变可行集，就称这个约束是**冗余的**。

<div class="example" markdown="1">

**例 4.1** 我们用几个简单的无约束优化问题来说明这些定义。它们的变量为 $x\in\mathbf{R}$，并且 $\operatorname{\mathbf{dom}}f_0=\mathbf{R}_{++}$。

- $f_0(x)=1/x$：$p^\star=0$，但最优值不能取到。
- $f_0(x)=-\log x$：$p^\star=-\infty$，因此这个问题下方无界。
- $f_0(x)=x\log x$：$p^\star=-1/e$，在唯一的最优点 $x^\star=1/e$ 处取到。

</div>

#### 可行性问题

如果目标函数恒为零，最优值就只能是零（可行集非空时）或 $\infty$（可行集为空时）。我们称这类问题为<!-- pdf-page: 143 -->**可行性问题**，有时将它写为

$$
\begin{array}{ll}
\text{寻找} & x\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p.
\end{array}
$$

因此，可行性问题就是判断这些约束能否同时满足；如果能，就找出一个满足它们的点。

### 4.1.2 将问题写成标准形式

我们将 (4.1) 称为**标准形式**的优化问题。对于标准形式的问题，我们约定不等式约束和等式约束的右端都是零。把非零的右端移到左端，总能得到这种形式。例如，对于等式约束 $g_i(x)=\widetilde g_i(x)$，我们将它表示为 $h_i(x)=0$，其中 $h_i(x)=g_i(x)-\widetilde g_i(x)$。类似地，我们将形如 $f_i(x)\geq0$ 的不等式写成 $-f_i(x)\leq0$。

<div class="example" markdown="1">

**例 4.2 盒约束。** 考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & l_i\leq x_i\leq u_i,\quad i=1,\ldots,n,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$。这些约束称为**变量界约束**（因为它们给出了每个 $x_i$ 的下界和上界），也称为**盒约束**（因为可行集是一个盒）。

我们可以把这个问题写成标准形式：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & l_i-x_i\leq0,\quad i=1,\ldots,n\\
& x_i-u_i\leq0,\quad i=1,\ldots,n.
\end{array}
$$

这里有 $2n$ 个不等式约束函数：

$$
f_i(x)=l_i-x_i,\quad i=1,\ldots,n,
$$

以及

$$
f_i(x)=x_{i-n}-u_{i-n},\quad i=n+1,\ldots,2n.
$$

</div>

#### 最大化问题

按照惯例，我们主要讨论最小化问题。对于最大化问题

$$
\begin{array}{ll}
\text{最大化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{4.2}
$$

<!-- pdf-page: 144 -->

我们可以在相同约束下最小化函数 $-f_0$，从而求解它。通过这种对应关系，可以把上面的所有术语定义推广到最大化问题 (4.2)。例如，(4.2) 的最优值定义为

$$
p^\star=\sup\{f_0(x)\mid f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p\},
$$

如果可行点 $x$ 满足 $f_0(x)\geq p^\star-\epsilon$，就称它是 $\epsilon$-次优点。在讨论最大化问题时，目标有时称为**效用**或**满意度**，而不是代价。

### 4.1.3 等价问题

本书以一种非形式化的方式使用优化问题之间的等价概念。如果从一个问题的解能够容易地找到另一个问题的解，反过来也一样，就称这两个问题**等价**。（可以给出等价的形式化定义，但会比较复杂。）

作为一个简单例子，考虑问题

$$
\begin{array}{ll}
\text{最小化} & \widetilde f(x)=\alpha_0f_0(x)\\
\text{约束条件} & \widetilde f_i(x)=\alpha_i f_i(x)\leq0,\quad i=1,\ldots,m\\
& \widetilde h_i(x)=\beta_i h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{4.3}
$$

其中 $\alpha_i>0$，$i=0,\ldots,m$，且 $\beta_i\ne0$，$i=1,\ldots,p$。这个问题由标准形式问题 (4.1) 得到：将目标函数和不等式约束函数分别乘以正常数，将等式约束函数分别乘以非零常数。因此，问题 (4.3) 与原问题 (4.1) 的可行集相同。点 $x$ 对原问题 (4.1) 最优，当且仅当它对缩放后的问题 (4.3) 最优，所以我们说这两个问题等价。不过，问题 (4.1) 与 (4.3) 并不是同一个问题（除非所有 $\alpha_i$ 和 $\beta_i$ 都等于 1），因为它们的目标函数和约束函数不同。下面介绍几种能够产生等价问题的一般变换。

#### 变量变换

设 $\phi:\mathbf{R}^n\to\mathbf{R}^n$ 是一一映射，且它的像覆盖了问题的定义域 $\mathcal{D}$，即 $\phi(\operatorname{\mathbf{dom}}\phi)\supseteq\mathcal{D}$。定义函数 $\widetilde f_i$ 和 $\widetilde h_i$ 为

$$
\widetilde f_i(z)=f_i(\phi(z)),\quad i=0,\ldots,m,\qquad
\widetilde h_i(z)=h_i(\phi(z)),\quad i=1,\ldots,p.
$$

现在考虑以 $z$ 为变量的问题

$$
\begin{array}{ll}
\text{最小化} & \widetilde f_0(z)\\
\text{约束条件} & \widetilde f_i(z)\leq0,\quad i=1,\ldots,m\\
& \widetilde h_i(z)=0,\quad i=1,\ldots,p.
\end{array}
\tag{4.4}
$$

我们说标准形式问题 (4.1) 与问题 (4.4) 通过**变量变换**或**变量代换** $x=\phi(z)$ 联系起来。

这两个问题显然等价：如果 $x$ 是问题 (4.1) 的解，那么 $z=\phi^{-1}(x)$ 就是问题 (4.4) 的解；如果 $z$ 是问题 (4.4) 的解，那么 $x=\phi(z)$ 就是问题 (4.1) 的解。

<!-- pdf-page: 145 -->

#### 目标函数和约束函数的变换

设 $\psi_0:\mathbf{R}\to\mathbf{R}$ 单调递增，$\psi_1,\ldots,\psi_m:\mathbf{R}\to\mathbf{R}$ 满足 $\psi_i(u)\leq0$ 当且仅当 $u\leq0$，而 $\psi_{m+1},\ldots,\psi_{m+p}:\mathbf{R}\to\mathbf{R}$ 满足 $\psi_i(u)=0$ 当且仅当 $u=0$。通过复合定义函数 $\widetilde f_i$ 和 $\widetilde h_i$：

$$
\widetilde f_i(x)=\psi_i(f_i(x)),\quad i=0,\ldots,m,\qquad
\widetilde h_i(x)=\psi_{m+i}(h_i(x)),\quad i=1,\ldots,p.
$$

显然，相应的问题

$$
\begin{array}{ll}
\text{最小化} & \widetilde f_0(x)\\
\text{约束条件} & \widetilde f_i(x)\leq0,\quad i=1,\ldots,m\\
& \widetilde h_i(x)=0,\quad i=1,\ldots,p
\end{array}
$$

与标准形式问题 (4.1) 等价；事实上，它们的可行集相同，最优点也相同。（上面将目标函数和约束函数乘以适当常数的例子 (4.3)，就是所有 $\psi_i$ 都为线性函数的特殊情形。）

<div class="example" markdown="1">

**例 4.3 最小范数与最小范数平方问题。** 作为一个简单例子，考虑无约束的欧几里得范数最小化问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2,
\end{array}
\tag{4.5}
$$

其中变量为 $x\in\mathbf{R}^n$。由于范数总是非负的，我们也可以求解问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2=(Ax-b)^T(Ax-b),
\end{array}
\tag{4.6}
$$

即最小化欧几里得范数的平方。问题 (4.5) 与 (4.6) 显然等价；它们的最优点相同。不过，这两个问题并不是同一个问题。例如，(4.5) 的目标函数在任何满足 $Ax-b=0$ 的 $x$ 处都不可微，而 (4.6) 的目标函数在所有 $x$ 处都可微（事实上，它是二次函数）。

</div>

#### 松弛变量

一种简单的变换基于以下事实：$f_i(x)\leq0$ 当且仅当存在 $s_i\geq0$，使得 $f_i(x)+s_i=0$。利用这个变换，可以得到问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & s_i\geq0,\quad i=1,\ldots,m\\
& f_i(x)+s_i=0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{4.7}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $s\in\mathbf{R}^m$。这个问题有 $n+m$ 个变量、$m$ 个不等式约束（$s_i$ 的非负约束）以及 $m+p$ 个等式约束。新变量 $s_i$ 称为原不等式约束 $f_i(x)\leq0$ 对应的**松弛变量**。引入松弛变量后，每个不等式约束都被替换为一个等式约束和一个非负约束。

问题 (4.7) 与原来的标准形式问题 (4.1) 等价。确实，如果 $(x,s)$ 对问题 (4.7) 可行，那么 $x$ 对原<!-- pdf-page: 146 -->问题可行，因为 $s_i=-f_i(x)\geq0$。反过来，如果 $x$ 对原问题可行，那么取 $s_i=-f_i(x)$ 后，$(x,s)$ 就对问题 (4.7) 可行。类似地，$x$ 对原问题 (4.1) 最优，当且仅当 $(x,s)$ 对问题 (4.7) 最优，其中 $s_i=-f_i(x)$。

#### 消去等式约束

如果能够用参数 $z\in\mathbf{R}^k$ 将等式约束

$$
h_i(x)=0,\quad i=1,\ldots,p,
\tag{4.8}
$$

的所有解显式参数化，就可以从问题中**消去**这些等式约束，具体如下。设函数 $\phi:\mathbf{R}^k\to\mathbf{R}^n$ 满足：$x$ 满足 (4.8)，当且仅当存在某个 $z\in\mathbf{R}^k$，使得 $x=\phi(z)$。那么优化问题

$$
\begin{array}{ll}
\text{最小化} & \widetilde f_0(z)=f_0(\phi(z))\\
\text{约束条件} & \widetilde f_i(z)=f_i(\phi(z))\leq0,\quad i=1,\ldots,m
\end{array}
$$

就与原问题 (4.1) 等价。变换后的问题以 $z\in\mathbf{R}^k$ 为变量，有 $m$ 个不等式约束，没有等式约束。如果 $z$ 对变换后的问题最优，那么 $x=\phi(z)$ 对原问题最优。反过来，如果 $x$ 对原问题最优，那么由于 $x$ 可行，至少存在一个 $z$，使得 $x=\phi(z)$。任何这样的 $z$ 都对变换后的问题最优。

#### 消去线性等式约束

当所有等式约束都是线性的，即具有形式 $Ax=b$ 时，消去变量的过程可以更明确地描述，也容易通过数值计算实现。如果 $Ax=b$ 无解，即 $b\notin\mathcal{R}(A)$，那么原问题不可行。假设没有出现这种情况，用 $x_0$ 表示等式约束的任意一个解。取任意满足 $\mathcal{R}(F)=\mathcal{N}(A)$ 的矩阵 $F\in\mathbf{R}^{n\times k}$，则线性方程组 $Ax=b$ 的通解为 $Fz+x_0$，其中 $z\in\mathbf{R}^k$。（可以选择满秩的 $F$，此时有 $k=n-\operatorname{\mathbf{rank}}A$。）

将 $x=Fz+x_0$ 代入原问题，得到问题

$$
\begin{array}{ll}
\text{最小化} & f_0(Fz+x_0)\\
\text{约束条件} & f_i(Fz+x_0)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

它以 $z$ 为变量，与原问题等价，没有等式约束，变量个数也减少了 $\operatorname{\mathbf{rank}}A$。

#### 引入等式约束

我们也可以向问题中引入等式约束和新变量。一般情形的描述比较复杂，也不能提供多少直观帮助，因此我们给出一个后面会用到的典型例子。考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(A_0x+b_0)\\
\text{约束条件} & f_i(A_ix+b_i)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
$$

<!-- pdf-page: 147 -->

其中 $x\in\mathbf{R}^n$、$A_i\in\mathbf{R}^{k_i\times n}$、$f_i:\mathbf{R}^{k_i}\to\mathbf{R}$。在这个问题中，目标函数和约束函数由函数 $f_i$ 与 $A_ix+b_i$ 所定义的仿射变换复合而成。

对于 $i=0,\ldots,m$，我们引入新变量 $y_i\in\mathbf{R}^{k_i}$ 以及新的等式约束 $y_i=A_ix+b_i$，得到等价问题

$$
\begin{array}{ll}
\text{最小化} & f_0(y_0)\\
\text{约束条件} & f_i(y_i)\leq0,\quad i=1,\ldots,m\\
& y_i=A_ix+b_i,\quad i=0,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p.
\end{array}
$$

这个问题有 $k_0+\cdots+k_m$ 个新变量，

$$
y_0\in\mathbf{R}^{k_0},\quad\ldots,\quad y_m\in\mathbf{R}^{k_m},
$$

以及 $k_0+\cdots+k_m$ 个新的等式约束，

$$
y_0=A_0x+b_0,\quad\ldots,\quad y_m=A_mx+b_m.
$$

这个问题中的目标函数和各个不等式约束是**相互独立的**，也就是说，它们涉及不同的优化变量。

#### 对部分变量进行优化

我们总有

$$
\inf_{x,y}f(x,y)=\inf_x\widetilde f(x),
$$

其中 $\widetilde f(x)=\inf_y f(x,y)$。换句话说，要使一个函数最小，总可以先对部分变量最小化，再对其余变量最小化。这个简单而普遍的原理可以用来把问题变换为等价形式。一般情形的描述比较繁琐，也不能提供多少直观帮助，因此我们用一个例子来说明。

设变量 $x\in\mathbf{R}^n$ 分块为 $x=(x_1,x_2)$，其中 $x_1\in\mathbf{R}^{n_1}$、$x_2\in\mathbf{R}^{n_2}$，且 $n_1+n_2=n$。考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x_1,x_2)\\
\text{约束条件} & f_i(x_1)\leq0,\quad i=1,\ldots,m_1\\
& \widetilde f_i(x_2)\leq0,\quad i=1,\ldots,m_2,
\end{array}
\tag{4.9}
$$

其中各个约束相互独立，意思是每个约束函数只依赖于 $x_1$ 或 $x_2$。我们先对 $x_2$ 最小化。将关于 $x_1$ 的函数 $\widetilde f_0$ 定义为

$$
\widetilde f_0(x_1)=\inf\{f_0(x_1,z)\mid\widetilde f_i(z)\leq0,\ i=1,\ldots,m_2\}.
$$

于是，问题 (4.9) 等价于

$$
\begin{array}{ll}
\text{最小化} & \widetilde f_0(x_1)\\
\text{约束条件} & f_i(x_1)\leq0,\quad i=1,\ldots,m_1.
\end{array}
\tag{4.10}
$$

<!-- pdf-page: 148 -->

<div class="example" markdown="1">

**例 4.4 对部分变量有约束的二次函数最小化。** 考虑一个目标函数为严格凸二次函数、部分变量不受约束的问题：

$$
\begin{array}{ll}
\text{最小化} & x_1^TP_{11}x_1+2x_1^TP_{12}x_2+x_2^TP_{22}x_2\\
\text{约束条件} & f_i(x_1)\leq0,\quad i=1,\ldots,m,
\end{array}
$$

其中 $P_{11}$ 和 $P_{22}$ 为对称矩阵。这里，对 $x_2$ 的最小化可以通过解析计算完成：

$$
\inf_{x_2}\left(x_1^TP_{11}x_1+2x_1^TP_{12}x_2+x_2^TP_{22}x_2\right)
=x_1^T\left(P_{11}-P_{12}P_{22}^{-1}P_{12}^T\right)x_1
$$

（见第 A.5.5 节）。因此，原问题等价于

$$
\begin{array}{ll}
\text{最小化} & x_1^T\left(P_{11}-P_{12}P_{22}^{-1}P_{12}^T\right)x_1\\
\text{约束条件} & f_i(x_1)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

</div>

#### 问题的上图形式

标准形式问题 (4.1) 的**上图形式**为问题

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & f_0(x)-t\leq0\\
& f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{4.11}
$$

其变量为 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}$。容易看出它与原问题等价：$(x,t)$ 对 (4.11) 最优，当且仅当 $x$ 对 (4.1) 最优且 $t=f_0(x)$。注意，上图形式问题的目标函数是变量 $x,t$ 的线性函数。

上图形式问题 (4.11) 可以在几何上解释为“函数图像所在空间” $(x,t)$ 中的一个优化问题：在 $x$ 满足约束的条件下，在 $f_0$ 的上图中最小化 $t$。图 4.1 给出了示意。

#### 隐式约束与显式约束

利用第 3.1.2 节中已经提过的一个简单技巧，我们可以通过重新定义目标函数的定义域，将任何约束隐含到目标函数之中。作为一个极端例子，标准形式问题可以表示成无约束问题

$$
\begin{array}{ll}
\text{最小化} & F(x),
\end{array}
\tag{4.12}
$$

其中我们将函数 $F$ 定义为 $f_0$，但把其定义域限制为可行集：

$$
\operatorname{\mathbf{dom}}F=\{x\in\operatorname{\mathbf{dom}}f_0\mid f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p\},
$$

并且当 $x\in\operatorname{\mathbf{dom}}F$ 时，$F(x)=f_0(x)$。（等价地，也可以将不可行的 $x$ 处的 $F(x)$ 定义为 $\infty$。）问题 (4.1) 与 (4.12) 显然等价：它们有相同的可行集、最优点和最优值。

当然，这种变换只是一种记号上的技巧。将约束隐含起来，并没有使问题更容易分析或求解，<!-- pdf-page: 149 -->尽管问题 (4.12) 至少在名义上是无约束的。在某些方面，这种变换反而使问题更困难。例如，假设原问题的目标函数 $f_0$ 可微，这特别意味着它的定义域是开集。限制定义域后的目标函数 $F$ 很可能不可微，因为它的定义域很可能不是开集。

<figure id="fig-4-1" data-figure="4.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-1.png" alt="目标函数的上图与其中最低的点，横轴为 x，纵轴为 t" data-source-page="149" data-source-rect="193,119,381,282">
<figcaption>图 4.1 无约束问题改写为上图形式后的几何解释。问题是在上图（阴影区域）中找出使 $t$ 最小的点，也就是上图中“最低”的点。最优点为 $(x^\star,t^\star)$。</figcaption>
<p class="figure-translation">图内文字：$\operatorname{\mathbf{epi}}f_0$ 表示 $f_0$ 的上图。</p>
</figure>

反过来，我们也会遇到带有隐式约束的问题，此时可以将这些约束显式写出。作为一个简单例子，考虑无约束问题

$$
\begin{array}{ll}
\text{最小化} & f(x),
\end{array}
\tag{4.13}
$$

其中函数 $f$ 为

$$
f(x)=\begin{cases}
x^Tx & Ax=b,\\
\infty & \text{其他情况}.
\end{cases}
$$

因此，在 $Ax=b$ 定义的仿射集上，目标函数等于二次型 $x^Tx$；在这个仿射集之外，它等于 $\infty$。显然，我们只需考虑满足 $Ax=b$ 的点，所以说问题 (4.13) 的目标函数中隐含了一个等式约束 $Ax=b$。通过构造等价问题

$$
\begin{array}{ll}
\text{最小化} & x^Tx\\
\text{约束条件} & Ax=b,
\end{array}
\tag{4.14}
$$

就可以将这个隐式等式约束显式写出。

问题 (4.13) 与 (4.14) 显然等价，但它们并不是同一个问题。问题 (4.13) 无约束，但它的目标函数不可微。问题 (4.14) 则有一个等式约束，不过它的目标函数和约束函数都可微。

<!-- pdf-page: 150 -->

### 4.1.4 问题的参数描述与 oracle 描述

对于标准形式 (4.1) 的问题，还需要说明如何给出目标函数和约束函数。在许多情况下，这些函数有解析形式或闭式表达，也就是说，可以用包含变量 $x$ 及一些参数的公式或表达式给出。例如，假设目标函数是二次函数，那么它具有形式 $f_0(x)=(1/2)x^TPx+q^Tx+r$。要给出这个目标函数，我们只需给出系数 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$ 和 $r\in\mathbf{R}$（它们也称为**问题参数**或**问题数据**）。我们称这种方式为问题的**参数描述**，因为给出目标函数和约束函数表达式中各参数的值，就确定了待求解的具体问题，也就是问题实例。

在另一些情况下，目标函数和约束函数通过 **oracle 模型**描述（也称为**黑箱模型**或**子程序模型**）。在 oracle 模型中，我们并不知道 $f$ 的显式表达式，但可以在任意 $x\in\operatorname{\mathbf{dom}}f$ 处计算 $f(x)$（通常还可以计算一些导数）。这种操作称为**查询 oracle**，通常需要付出一定代价，例如时间。我们还已知关于函数的一些先验信息，例如它的凸性及其函数值的界。作为 oracle 模型的一个具体例子，考虑一个最小化函数 $f$ 的无约束问题。函数值 $f(x)$ 及其梯度 $\nabla f(x)$ 由一个子程序计算。我们可以在任意 $x\in\operatorname{\mathbf{dom}}f$ 处调用这个子程序，但无法访问它的源代码。以 $x$ 为参数调用该子程序，在它返回时就能得到 $f(x)$ 和 $\nabla f(x)$。注意，在 oracle 模型中，我们始终没有真正掌握这个函数；我们只知道已经查询过 oracle 的那些点处的函数值及一些导数。（我们还知道关于该函数的一些给定的先验信息，例如可微性与凸性。）

在实际应用中，参数描述与 oracle 描述之间的区别并没有那么鲜明。如果给定了一个问题的参数描述，就可以为它构造一个 oracle；被查询时，它只需计算所需的函数值和导数即可。本书第三部分研究的大多数算法都适用于 oracle 模型；但如果把求解对象限制为某个特定的参数化问题族，往往可以提高这些算法的效率。

## 4.2 凸优化

### 4.2.1 标准形式的凸优化问题

**凸优化问题**具有形式

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& a_i^Tx=b_i,\quad i=1,\ldots,p,
\end{array}
\tag{4.15}
$$

其中 $f_0,\ldots,f_m$ 都是凸函数。与一般的标准形式问题 (4.1) 相比，凸问题 (4.15) 有三个额外要求：

<!-- pdf-page: 151 -->

- 目标函数必须是凸函数；
- 不等式约束函数必须是凸函数；
- 等式约束函数 $h_i(x)=a_i^Tx-b_i$ 必须是仿射函数。

我们立即得到一个重要性质：凸优化问题的可行集是凸集，因为它是问题的定义域

$$
\mathcal{D}=\bigcap_{i=0}^m\operatorname{\mathbf{dom}}f_i
$$

这个凸集与 $m$ 个凸下水平集 $\{x\mid f_i(x)\leq0\}$ 以及 $p$ 个超平面 $\{x\mid a_i^Tx=b_i\}$ 的交。（不失一般性，可以假设 $a_i\ne0$：如果某个 $i$ 满足 $a_i=0$ 且 $b_i=0$，就可以删除第 $i$ 个等式约束；如果 $a_i=0$ 且 $b_i\ne0$，那么第 $i$ 个等式约束无解，问题不可行。）因此，在凸优化问题中，我们是在一个凸集上最小化凸目标函数。

如果 $f_0$ 是拟凸函数，而不是凸函数，就称问题 (4.15) 为标准形式的**拟凸优化问题**。由于凸函数或拟凸函数的下水平集都是凸集，可以得出：凸优化问题或拟凸优化问题的 $\epsilon$-次优解集是凸集。特别地，最优解集是凸集。如果目标函数严格凸，那么最优解集至多包含一个点。

#### 凹函数最大化问题

稍微放宽上述术语的用法，如果目标函数 $f_0$ 是凹函数，不等式约束函数 $f_1,\ldots,f_m$ 是凸函数，我们也将

$$
\begin{array}{ll}
\text{最大化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& a_i^Tx=b_i,\quad i=1,\ldots,p
\end{array}
\tag{4.16}
$$

称为凸优化问题。这个凹函数最大化问题可以通过最小化凸目标函数 $-f_0$ 来求解。我们对最小化问题给出的所有结果、结论和算法，都容易转换到最大化情形。类似地，如果 $f_0$ 是拟凹函数，就称最大化问题 (4.16) 为拟凸优化问题。

#### 抽象形式的凸优化问题

需要留意凸优化问题定义中的一个细节。考虑下面这个以 $x\in\mathbf{R}^2$ 为变量的例子：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)=x_1^2+x_2^2\\
\text{约束条件} & f_1(x)=x_1/(1+x_2^2)\leq0\\
& h_1(x)=(x_1+x_2)^2=0.
\end{array}
\tag{4.17}
$$

它具有标准形式 (4.1)。这个问题并不是标准形式的凸优化问题，因为等式约束函数 $h_1$ 不是仿射函数，<!-- pdf-page: 152 -->不等式约束函数 $f_1$ 也不是凸函数。不过，它的可行集 $\{x\mid x_1\leq0,\ x_1+x_2=0\}$ 却是凸集。因此，虽然这个问题是在凸集上最小化凸函数 $f_0$，按照我们的定义，它仍然不是凸优化问题。

当然，这个问题很容易改写为

$$
\begin{array}{ll}
\text{最小化} & f_0(x)=x_1^2+x_2^2\\
\text{约束条件} & \widetilde f_1(x)=x_1\leq0\\
& \widetilde h_1(x)=x_1+x_2=0,
\end{array}
\tag{4.18}
$$

它具有凸优化的标准形式，因为 $f_0$ 和 $\widetilde f_1$ 为凸函数，$\widetilde h_1$ 为仿射函数。

一些作者用**抽象凸优化问题**这个术语，描述在凸集上最小化凸函数的抽象问题。按照这种术语，问题 (4.17) 就是抽象凸优化问题。**本书不采用这种术语。** 对我们来说，凸优化问题不仅要求在凸集上最小化凸函数，还要求可行集明确地用一组涉及凸函数的不等式和一组线性等式约束来描述。问题 (4.17) 不是凸优化问题，而问题 (4.18) 是凸优化问题。（不过，这两个问题是等价的。）

我们采用较严格的凸优化问题定义，在实际应用中影响不大。为了求解在凸集上最小化凸函数这一抽象问题，我们需要找到用凸不等式和线性等式约束描述该集合的方法。正如上面的例子所示，这通常并不困难。

### 4.2.2 局部最优解与全局最优解

凸优化问题的一个基本性质是：任何局部最优点也是全局最优点。为说明这一点，假设 $x$ 是某个凸优化问题的局部最优点，即 $x$ 可行，并且存在 $R>0$，使得

$$
f_0(x)=\inf\{f_0(z)\mid z\text{ 可行},\ \|z-x\|_2\leq R\}.
\tag{4.19}
$$

现在假设 $x$ 不是全局最优点，也就是说，存在一个可行的 $y$，满足 $f_0(y)<f_0(x)$。显然 $\|y-x\|_2>R$，否则就会有 $f_0(x)\leq f_0(y)$。考虑点

$$
z=(1-\theta)x+\theta y,\qquad\theta=\frac{R}{2\|y-x\|_2}.
$$

于是 $\|z-x\|_2=R/2<R$，而且由可行集的凸性可知 $z$ 可行。由 $f_0$ 的凸性，得到

$$
f_0(z)\leq(1-\theta)f_0(x)+\theta f_0(y)<f_0(x),
$$

这与 (4.19) 矛盾。因此，不存在满足 $f_0(y)<f_0(x)$ 的可行点 $y$，即 $x$ 是全局最优点。

<!-- pdf-page: 153 -->

<figure id="fig-4-2" data-figure="4.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-2.png" alt="阴影可行集、目标函数的虚线等值线，以及最优点处的支撑超平面和负梯度箭头" data-source-page="153" data-source-rect="200,121,379,251">
<figcaption>图 4.2 最优性条件 (4.21) 的几何解释。可行集 $X$ 用阴影表示，$f_0$ 的若干条等值线用虚线表示。点 $x$ 是最优点：$-\nabla f_0(x)$ 确定了 $X$ 在 $x$ 处的一条支撑超平面（图中的实线）。</figcaption>
</figure>

拟凸优化问题的局部最优点并不一定是全局最优点，见第 4.2.5 节。

### 4.2.3 $f_0$ 可微时的最优性判据

假设凸优化问题中的目标函数 $f_0$ 可微，因此对于所有 $x,y\in\operatorname{\mathbf{dom}}f_0$，都有

$$
f_0(y)\geq f_0(x)+\nabla f_0(x)^T(y-x)
\tag{4.20}
$$

（见第 3.1.3 节）。用 $X$ 表示可行集，即

$$
X=\{x\mid f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p\}.
$$

那么，$x$ 最优当且仅当 $x\in X$，并且

$$
\nabla f_0(x)^T(y-x)\geq0\quad\text{对所有 }y\in X.
\tag{4.21}
$$

这个最优性判据可以从几何上理解：如果 $\nabla f_0(x)\ne0$，它就意味着 $-\nabla f_0(x)$ 确定了可行集在 $x$ 处的一条支撑超平面（见图 4.2）。

#### 最优性条件的证明

首先，假设 $x\in X$ 且满足 (4.21)。那么，如果 $y\in X$，由 (4.20) 可得 $f_0(y)\geq f_0(x)$。这说明 $x$ 是 (4.1) 的最优点。

反过来，假设 $x$ 最优，但条件 (4.21) 不成立，即对于某个 $y\in X$，有

$$
\nabla f_0(x)^T(y-x)<0.
$$

<!-- pdf-page: 154 -->

考虑点 $z(t)=ty+(1-t)x$，其中 $t\in[0,1]$ 是参数。由于 $z(t)$ 位于 $x$ 与 $y$ 之间的线段上，而且可行集是凸集，所以 $z(t)$ 可行。我们断言：对于足够小的正数 $t$，有 $f_0(z(t))<f_0(x)$，这就证明了 $x$ 不是最优点。为此，注意到

$$
\left.\frac{d}{dt}f_0(z(t))\right|_{t=0}=\nabla f_0(x)^T(y-x)<0,
$$

因此，对于足够小的正数 $t$，有 $f_0(z(t))<f_0(x)$。

我们将在第 5 章更深入地讨论最优性条件，这里先看几个简单例子。

#### 无约束问题

对于无约束问题（即 $m=p=0$），条件 (4.21) 化为熟知的 $x$ 最优的充要条件

$$
\nabla f_0(x)=0.
\tag{4.22}
$$

虽然前面已经见过这个最优性条件，但看看如何从 (4.21) 推出它仍然很有帮助。假设 $x$ 最优，这里意味着 $x\in\operatorname{\mathbf{dom}}f_0$，而且对于所有可行的 $y$，都有 $\nabla f_0(x)^T(y-x)\geq0$。由于 $f_0$ 可微，按照定义，它的定义域是开集，所以与 $x$ 足够接近的所有 $y$ 都可行。取 $y=x-t\nabla f_0(x)$，其中 $t\in\mathbf{R}$ 是参数。当 $t$ 是足够小的正数时，$y$ 可行，因此

$$
\nabla f_0(x)^T(y-x)=-t\|\nabla f_0(x)\|_2^2\geq0,
$$

由此得出 $\nabla f_0(x)=0$。

根据 (4.22) 的解的个数，可能出现几种情况。如果 (4.22) 无解，就不存在最优点；问题的最优值不能取到。这里又可以区分两种情形：问题下方无界；或者最优值有限，但不能取到。另一方面，方程 (4.22) 也可能有多个解，此时每个解都是 $f_0$ 的一个最小点。

<div class="example" markdown="1">

**例 4.5 无约束二次优化。** 考虑最小化二次函数

$$
f_0(x)=(1/2)x^TPx+q^Tx+r
$$

的问题，其中 $P\in\mathbf{S}_+^n$（这保证了 $f_0$ 的凸性）。$x$ 是 $f_0$ 的最小点的充要条件为

$$
\nabla f_0(x)=Px+q=0.
$$

根据这个线性方程无解、有唯一解还是有多个解，可能出现几种情况。

- 如果 $q\notin\mathcal{R}(P)$，那么方程无解。此时 $f_0$ 下方无界。
- 如果 $P\succ0$（这正是 $f_0$ 严格凸的条件），那么存在唯一的最小点 $x^\star=-P^{-1}q$。
- <!-- pdf-page: 155 -->如果 $P$ 奇异，但 $q\in\mathcal{R}(P)$，那么最优点构成仿射集 $X_{\mathrm{opt}}=-P^\dagger q+\mathcal{N}(P)$，其中 $P^\dagger$ 表示 $P$ 的伪逆（见第 A.5.4 节）。

</div>

<div class="example" markdown="1">

**例 4.6 求解析中心。** 考虑最小化凸函数 $f_0:\mathbf{R}^n\to\mathbf{R}$ 的无约束问题，其中

$$
f_0(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx),\qquad\operatorname{\mathbf{dom}}f_0=\{x\mid Ax\prec b\},
$$

而 $a_1^T,\ldots,a_m^T$ 是 $A$ 的各行。函数 $f_0$ 可微，因此 $x$ 最优的充要条件为

$$
Ax\prec b,\qquad\nabla f_0(x)=\sum_{i=1}^m\frac{1}{b_i-a_i^Tx}a_i=0.
\tag{4.23}
$$

（条件 $Ax\prec b$ 就是 $x\in\operatorname{\mathbf{dom}}f_0$。）如果 $Ax\prec b$ 不可行，那么 $f_0$ 的定义域为空。假设 $Ax\prec b$ 可行，仍可能出现几种情况（见习题 4.2）：

- (4.23) 无解，因此问题没有最优点。这种情况发生当且仅当 $f_0$ 下方无界。
- (4.23) 有多个解。此时可以证明，这些解构成一个仿射集。
- (4.23) 有唯一解，即 $f_0$ 有唯一的最小点。这种情况发生当且仅当开多面体 $\{x\mid Ax\prec b\}$ 非空且有界。

</div>

#### 只有等式约束的问题

考虑有等式约束而没有不等式约束的情形，即

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & Ax=b.
\end{array}
$$

这里，可行集是仿射集。我们假设它非空，否则问题不可行。可行点 $x$ 的最优性条件是：对所有满足 $Ay=b$ 的 $y$，必须有

$$
\nabla f_0(x)^T(y-x)\geq0.
$$

由于 $x$ 可行，每个可行的 $y$ 都可以写成 $y=x+v$，其中 $v\in\mathcal{N}(A)$。因此，最优性条件可以表示为

$$
\nabla f_0(x)^Tv\geq0\quad\text{对所有 }v\in\mathcal{N}(A).
$$

如果一个线性函数在某个子空间上非负，那么它必定在这个子空间上恒为零。因此，对所有 $v\in\mathcal{N}(A)$，都有 $\nabla f_0(x)^Tv=0$。换句话说，

$$
\nabla f_0(x)\perp\mathcal{N}(A).
$$

<!-- pdf-page: 156 -->

利用 $\mathcal{N}(A)^\perp=\mathcal{R}(A^T)$，这个最优性条件可以表示为 $\nabla f_0(x)\in\mathcal{R}(A^T)$，即存在 $\nu\in\mathbf{R}^p$，使得

$$
\nabla f_0(x)+A^T\nu=0.
$$

加上要求 $Ax=b$（即 $x$ 可行），就得到了经典的**拉格朗日乘子最优性条件**。我们将在第 5 章更详细地研究它。

#### 在非负正交象限上最小化

作为另一个例子，考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & x\succeq0,
\end{array}
$$

其中唯一的不等式约束是变量的非负约束。此时，最优性条件 (4.21) 为

$$
x\succeq0,\qquad\nabla f_0(x)^T(y-x)\geq0\quad\text{对所有 }y\succeq0.
$$

其中 $\nabla f_0(x)^Ty$ 是 $y$ 的线性函数；除非 $\nabla f_0(x)\succeq0$，否则它在 $y\succeq0$ 上下方无界。于是，这个条件化为 $-\nabla f_0(x)^Tx\geq0$。但 $x\succeq0$ 且 $\nabla f_0(x)\succeq0$，所以必须有 $\nabla f_0(x)^Tx=0$，即

$$
\sum_{i=1}^n(\nabla f_0(x))_i x_i=0.
$$

这个和中的每一项都是两个非负数的乘积，因此每一项都必须为零，即 $(\nabla f_0(x))_i x_i=0$，$i=1,\ldots,n$。所以，最优性条件可以表示为

$$
x\succeq0,\qquad\nabla f_0(x)\succeq0,\qquad x_i(\nabla f_0(x))_i=0,\quad i=1,\ldots,n.
$$

最后一个条件称为**互补性**，因为它意味着向量 $x$ 和 $\nabla f_0(x)$ 的稀疏模式（即非零分量对应的下标集合）相互互补，也就是说，它们的交集为空。我们将在第 5 章再次遇到互补性条件。

### 4.2.4 等价的凸问题

看看第 4.1.3 节介绍的哪些变换能够保持凸性，会很有帮助。

#### 消去等式约束

对于凸问题，等式约束必须是线性的，即具有形式 $Ax=b$。此时，可以通过找到<!-- pdf-page: 157 -->$Ax=b$ 的一个特解 $x_0$，以及一个值域等于 $A$ 的零空间的矩阵 $F$，消去这些约束，得到以 $z$ 为变量的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(Fz+x_0)\\
\text{约束条件} & f_i(Fz+x_0)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

由于凸函数与仿射函数的复合仍为凸函数，消去等式约束能够保持问题的凸性。而且，消去等式约束，以及从变换后问题的解重构原问题的解，都只涉及标准的线性代数运算。

至少从原理上说，这意味着我们可以只考虑没有等式约束的凸优化问题。不过，在许多情况下，保留等式约束更好，因为消去它们可能使问题更难理解和分析，或者破坏求解算法的效率。例如，当变量 $x$ 的维数很大，而消去等式约束会破坏问题的稀疏性或其他有用结构时，就是如此。

#### 引入等式约束

我们可以向凸优化问题中引入新变量和等式约束；只要这些等式约束是线性的，得到的问题仍是凸问题。例如，如果一个目标函数或约束函数具有形式 $f_i(A_ix+b_i)$，其中 $A_i\in\mathbf{R}^{k_i\times n}$，那么可以引入新变量 $y_i\in\mathbf{R}^{k_i}$，用 $f_i(y_i)$ 替换 $f_i(A_ix+b_i)$，并增加线性等式约束 $y_i=A_ix+b_i$。

#### 松弛变量

引入松弛变量后，我们得到新约束 $f_i(x)+s_i=0$。由于凸问题的等式约束函数必须是仿射函数，$f_i$ 也必须是仿射函数。换句话说，为**线性**不等式引入松弛变量能够保持问题的凸性。

#### 问题的上图形式

凸优化问题 (4.15) 的上图形式为

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & f_0(x)-t\leq0\\
& f_i(x)\leq0,\quad i=1,\ldots,m\\
& a_i^Tx=b_i,\quad i=1,\ldots,p.
\end{array}
$$

目标函数是线性的，因而是凸函数；新的约束函数 $f_0(x)-t$ 关于 $(x,t)$ 也是凸函数，所以这个上图形式问题同样是凸问题。

有时，人们说线性目标函数对于凸优化具有普遍性，因为任何凸优化问题都容易变换成目标函数为线性函数的问题。凸问题的上图形式有几个实际用途。假设凸优化问题的目标函数为线性函数，可以简化理论分析。它也能简化算法设计，因为一个能够求解线性目标凸优化问题的算法，可以借助<!-- pdf-page: 158 -->上述变换求解任何凸优化问题，只要它能够处理约束 $f_0(x)-t\leq0$。

#### 对部分变量最小化

对凸函数的部分变量最小化能够保持凸性。因此，如果 (4.9) 中的 $f_0$ 关于 $x_1$ 和 $x_2$ 联合凸，且 $f_i$，$i=1,\ldots,m_1$，以及 $\widetilde f_i$，$i=1,\ldots,m_2$，都是凸函数，那么等价问题 (4.10) 是凸问题。

### 4.2.5 拟凸优化

回顾一下，拟凸优化问题的标准形式为

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
\tag{4.24}
$$

其中不等式约束函数 $f_1,\ldots,f_m$ 是凸函数，而目标函数 $f_0$ 是拟凸函数，不必像凸优化问题那样要求为凸函数。（拟凸约束函数可以替换为等价的凸约束函数，即具有相同的 0-下水平集的凸函数，见第 3.4.5 节。）

本节指出凸优化问题与拟凸优化问题之间的一些基本区别，并说明如何将拟凸优化问题的求解归结为一系列凸优化问题的求解。

#### 局部最优解与最优性条件

凸优化与拟凸优化之间最重要的区别是：拟凸优化问题可能存在局部最优、却不是全局最优的解。即使在对 $\mathbf{R}$ 上的拟凸函数作无约束最小化这样简单的情形中，也会出现这种现象，例如图 4.3 所示的函数。

不过，对于目标函数可微的拟凸优化问题，第 4.2.3 节最优性条件 (4.21) 的一种变体仍然成立。用 $X$ 表示拟凸优化问题 (4.24) 的可行集。由拟凸性的一阶条件 (3.20) 可得，如果

$$
x\in X,\qquad\nabla f_0(x)^T(y-x)>0\quad\text{对所有 }y\in X\setminus\{x\},
\tag{4.25}
$$

那么 $x$ 最优。这个判据与凸优化中对应的判据 (4.21) 有两个重要区别：

- 条件 (4.25) 只是最优性的**充分条件**；简单的例子就能说明，最优点不一定满足它。相比之下，条件 (4.21) 是 $x$ 求解凸问题的充要条件。
- 条件 (4.25) 要求 $f_0$ 的梯度非零，而条件 (4.21) 没有这个要求。事实上，在凸情形中，当 $\nabla f_0(x)=0$ 时，条件 (4.21) 成立，$x$ 就是最优点。

<!-- pdf-page: 159 -->

<figure id="fig-4-3" data-figure="4.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-3.png" alt="一维拟凸函数的曲线，在高于全局最低点的水平段上标出一个局部最优点" data-source-page="159" data-source-rect="193,122,377,250">
<figcaption>图 4.3 $\mathbf{R}$ 上的一个拟凸函数 $f$，其中 $x$ 是局部最优点，却不是全局最优点。这个例子说明，对凸函数成立的简单最优性条件 $f'(x)=0$ 并不适用于拟凸函数。</figcaption>
</figure>

#### 通过凸可行性问题进行拟凸优化

拟凸优化的一种一般方法，依赖于第 3.4.5 节介绍的表示：用一族凸不等式表示拟凸函数的下水平集。设 $\phi_t:\mathbf{R}^n\to\mathbf{R}$，$t\in\mathbf{R}$，是一族凸函数，满足

$$
f_0(x)\leq t\quad\Longleftrightarrow\quad\phi_t(x)\leq0,
$$

而且对于每个 $x$，$\phi_t(x)$ 都是 $t$ 的非增函数，即只要 $s\geq t$，就有 $\phi_s(x)\leq\phi_t(x)$。

用 $p^\star$ 表示拟凸优化问题 (4.24) 的最优值。如果可行性问题

$$
\begin{array}{ll}
\text{寻找} & x\\
\text{约束条件} & \phi_t(x)\leq0\\
& f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b
\end{array}
\tag{4.26}
$$

可行，那么 $p^\star\leq t$。反过来，如果问题 (4.26) 不可行，就可以断定 $p^\star\geq t$。问题 (4.26) 是一个凸可行性问题，因为不等式约束函数都是凸函数，等式约束也都是线性的。因此，通过求解凸可行性问题 (4.26)，可以检验拟凸优化问题的最优值 $p^\star$ 位于给定值 $t$ 的哪一侧。如果这个凸可行性问题可行，就有 $p^\star\leq t$，而且它的任何可行点 $x$ 都对拟凸问题可行，并满足 $f_0(x)\leq t$。如果凸可行性问题不可行，就知道 $p^\star\geq t$。

基于这一观察，可以得到一个用**二分法**求解拟凸优化问题 (4.24) 的简单算法：每一步求解一个凸可行性问题。假设问题可行，从一个已知包含最优值 $p^\star$ 的区间 $[l,u]$ 开始。然后在区间中点 $t=(l+u)/2$ 处求解凸可行性问题，以判断<!-- pdf-page: 160 -->最优值位于区间的下半部分还是上半部分，并相应地更新区间。得到的新区间仍包含最优值，但宽度只有原区间的一半。重复这个过程，直到区间宽度足够小：

<div class="algorithm" id="algorithm-4-1" data-algorithm="4.1" markdown="1">

**算法 4.1 用于拟凸优化的二分法。**

**给定** $l\leq p^\star$、$u\geq p^\star$，容差 $\epsilon>0$。

**重复执行**

1. $t:=(l+u)/2$。
2. 求解凸可行性问题 (4.26)。
3. **如果** (4.26) 可行，令 $u:=t$；**否则**令 $l:=t$。

**直到** $u-l\leq\epsilon$。

</div>

区间 $[l,u]$ 保证包含 $p^\star$，也就是说，每一步都有 $l\leq p^\star\leq u$。每次迭代都把区间一分为二，即二等分；因此，经过 $k$ 次迭代后，区间长度为 $2^{-k}(u-l)$，其中 $u-l$ 是初始区间的长度。由此可知，算法恰好需要 $\lceil\log_2((u-l)/\epsilon)\rceil$ 次迭代便会终止。每一步都要求解凸可行性问题 (4.26)。

## 4.3 线性优化问题

当目标函数和所有约束函数都是仿射函数时，该问题称为**线性规划**（linear program，LP）。一般的线性规划具有形式

$$
\begin{array}{ll}
\text{最小化} & c^Tx+d\\
\text{约束条件} & Gx\preceq h\\
& Ax=b,
\end{array}
\tag{4.27}
$$

其中 $G\in\mathbf{R}^{m\times n}$、$A\in\mathbf{R}^{p\times n}$。线性规划当然是凸优化问题。

通常会省去目标函数中的常数 $d$，因为它不影响最优解集或可行集。由于最大化仿射目标函数 $c^Tx+d$ 可以通过最小化 $-c^Tx-d$ 来实现，而且后者仍为凸函数，因此目标函数和约束函数均为仿射函数的最大化问题也称为 LP。

图 4.4 展示了 LP 的几何解释。LP (4.27) 的可行集是一个多面体 $\mathcal{P}$；这个问题就是在 $\mathcal{P}$ 上最小化仿射函数 $c^Tx+d$，或者等价地，最小化线性函数 $c^Tx$。

#### 标准形式与不等式形式的线性规划

LP (4.27) 的两个特殊情形十分常见，因此有各自的名称。在**标准形式 LP** 中，唯一的不等式是逐分量<!-- pdf-page: 161 -->非负约束 $x\succeq0$：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax=b\\
& x\succeq0.
\end{array}
\tag{4.28}
$$

<figure id="fig-4-4" data-figure="4.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-4.png" alt="多面体可行集与线性目标函数的平行等值线，最优点位于负 c 方向最远的顶点" data-source-page="161" data-source-rect="193,121,379,253">
<figcaption>图 4.4 线性规划（LP）的几何解释。可行集 $\mathcal{P}$ 是一个多面体，用阴影表示。目标函数 $c^Tx$ 是线性的，因此它的等值线是与 $c$ 正交的超平面（图中的虚线）。点 $x^\star$ 是最优点；它是 $\mathcal{P}$ 中沿 $-c$ 方向最远的点。</figcaption>
</figure>

如果 LP 没有等式约束，就称它为**不等式形式 LP**，通常写为

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b.
\end{array}
\tag{4.29}
$$

#### 将 LP 转换为标准形式

有时，将一般的 LP (4.27) 转换为标准形式 (4.28) 很有用，例如为了使用求解标准形式 LP 的算法。第一步是为不等式引入松弛变量 $s_i$，得到

$$
\begin{array}{ll}
\text{最小化} & c^Tx+d\\
\text{约束条件} & Gx+s=h\\
& Ax=b\\
& s\succeq0.
\end{array}
$$

第二步是将变量 $x$ 表示为两个非负变量 $x^+$ 和 $x^-$ 的差，即 $x=x^+-x^-$，$x^+,x^-\succeq0$。由此得到问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx^+-c^Tx^-+d\\
\text{约束条件} & Gx^+-Gx^-+s=h\\
& Ax^+-Ax^-=b\\
& x^+\succeq0,\quad x^-\succeq0,\quad s\succeq0,
\end{array}
$$

<!-- pdf-page: 162 -->

这是以 $x^+$、$x^-$ 和 $s$ 为变量的标准形式 LP。（它与原问题 (4.27) 的等价性见习题 4.10。）

利用这些变换问题的技巧，以及后面的例子和习题中将出现的许多其他技巧，可以把很多问题写成线性规划。人们常常略微放宽术语的用法，把能够写成 LP 的问题也称为 LP，即使它本身不具有形式 (4.27)。

### 4.3.1 例子

LP 出现在大量领域和应用中；这里给出几个典型例子。

#### 饮食问题

健康的饮食需要包含 $m$ 种营养成分，其含量分别至少为 $b_1,\ldots,b_m$。我们可以从 $n$ 种食物中选择非负的数量 $x_1,\ldots,x_n$，组成这样的饮食。每单位第 $j$ 种食物含有数量为 $a_{ij}$ 的第 $i$ 种营养成分，成本为 $c_j$。我们希望找出满足营养要求的最便宜饮食。这个问题可以写成 LP：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\succeq b\\
& x\succeq0.
\end{array}
$$

这个问题的几种变体也可以写成 LP。例如，可以要求饮食中某种营养成分的含量恰好等于给定值，从而得到一个线性等式约束；也可以在上述下界之外，再对某种营养成分的含量施加上界。

#### 多面体的 Chebyshev 中心

考虑寻找包含在线性不等式所描述的多面体

$$
\mathcal{P}=\{x\in\mathbf{R}^n\mid a_i^Tx\leq b_i,\ i=1,\ldots,m\}
$$

中的最大欧几里得球的问题。（最优球的球心称为多面体的 **Chebyshev 中心**；它是多面体内部最深处的点，也就是离边界最远的点，见第 8.5.1 节。）将球表示为

$$
\mathcal{B}=\{x_c+u\mid\|u\|_2\leq r\}.
$$

问题的变量是球心 $x_c\in\mathbf{R}^n$ 和半径 $r$；我们希望在约束 $\mathcal{B}\subseteq\mathcal{P}$ 下最大化 $r$。

先考虑一个更简单的约束：$\mathcal{B}$ 包含在半空间 $a_i^Tx\leq b_i$ 中，即

$$
\|u\|_2\leq r\quad\Longrightarrow\quad a_i^T(x_c+u)\leq b_i.
\tag{4.30}
$$

由于

$$
\sup\{a_i^Tu\mid\|u\|_2\leq r\}=r\|a_i\|_2,
$$

<!-- pdf-page: 163 -->

可以将 (4.30) 写成

$$
a_i^Tx_c+r\|a_i\|_2\leq b_i,
\tag{4.31}
$$

这是关于 $x_c$ 和 $r$ 的线性不等式。换句话说，球包含在不等式 $a_i^Tx\leq b_i$ 所确定的半空间中，这个约束可以写成一个线性不等式。

因此，$\mathcal{B}\subseteq\mathcal{P}$ 当且仅当 (4.31) 对所有 $i=1,\ldots,m$ 都成立。于是，可以通过求解以下以 $r$ 和 $x_c$ 为变量的 LP，确定 Chebyshev 中心：

$$
\begin{array}{ll}
\text{最大化} & r\\
\text{约束条件} & a_i^Tx_c+r\|a_i\|_2\leq b_i,\quad i=1,\ldots,m.
\end{array}
$$

（关于 Chebyshev 中心的更多内容，见第 8.5.1 节。）

#### 动态活动规划

考虑为 $n$ 种活动或经济部门选择、规划 $N$ 个时期内的活动水平的问题。用 $x_j(t)\geq0$，$t=1,\ldots,N$，表示第 $j$ 个部门在第 $t$ 期的活动水平。每种活动都按照与其活动水平成比例的数量消耗并生产产品。每单位第 $j$ 种活动生产的第 $i$ 种产品数量为 $a_{ij}$。类似地，每单位第 $j$ 种活动消耗的第 $i$ 种产品数量为 $b_{ij}$。第 $t$ 期生产的产品总量为 $Ax(t)\in\mathbf{R}^m$，消耗的产品总量为 $Bx(t)\in\mathbf{R}^m$。（虽然我们把这些产出称为“产品”，但它们也可以包含污染物等不希望产生的产物。）

一个时期内消耗的产品不能超过上一期生产的产品：必须有 $Bx(t+1)\preceq Ax(t)$，$t=1,\ldots,N$。给定初始产品数量向量 $g_0\in\mathbf{R}^m$，它对第一期的活动水平施加约束：$Bx(1)\preceq g_0$。没有被各项活动消耗掉的剩余产品数量向量为

$$
\begin{aligned}
s(0)&=g_0-Bx(1),\\
s(t)&=Ax(t)-Bx(t+1),\quad t=1,\ldots,N-1,\\
s(N)&=Ax(N).
\end{aligned}
$$

目标是最大化剩余产品的折现总价值：

$$
c^Ts(0)+\gamma c^Ts(1)+\cdots+\gamma^Nc^Ts(N),
$$

其中 $c\in\mathbf{R}^m$ 给出各产品的价值，$\gamma>0$ 是折现因子。（如果第 $i$ 种产品是不希望产生的产物，例如污染物，那么 $c_i$ 为负数；此时 $|c_i|$ 是每单位的处置成本。）

将这些条件合在一起，得到 LP

$$
\begin{array}{ll}
\text{最大化} & c^Ts(0)+\gamma c^Ts(1)+\cdots+\gamma^Nc^Ts(N)\\
\text{约束条件} & x(t)\succeq0,\quad t=1,\ldots,N\\
& s(t)\succeq0,\quad t=0,\ldots,N\\
& s(0)=g_0-Bx(1)\\
& s(t)=Ax(t)-Bx(t+1),\quad t=1,\ldots,N-1\\
& s(N)=Ax(N),
\end{array}
$$

其变量为 $x(1),\ldots,x(N),s(0),\ldots,s(N)$。这是一个标准形式 LP；变量 $s(t)$ 是与约束 $Bx(t+1)\preceq Ax(t)$ 对应的松弛变量。

<div class="translator-note" markdown="1">

**译注（动态活动规划）：** 跨期约束 $Bx(t+1)\preceq Ax(t)$ 的下标范围应为 $t=1,\ldots,N-1$，与本节的完整模型一致；末期产出单独用 $s(N)=Ax(N)$ 表示。

</div>

<!-- pdf-page: 164 -->

#### Chebyshev 不等式

考虑离散随机变量 $x$ 在含有 $n$ 个元素的集合 $\{u_1,\ldots,u_n\}\subseteq\mathbf{R}$ 上的概率分布。用向量 $p\in\mathbf{R}^n$ 描述 $x$ 的分布，其中

$$
p_i=\operatorname{\mathbf{prob}}(x=u_i),
$$

因此 $p$ 满足 $p\succeq0$ 和 $\mathbf{1}^Tp=1$。反过来，如果 $p$ 满足 $p\succeq0$ 和 $\mathbf{1}^Tp=1$，那么它就确定了 $x$ 的一个概率分布。假设各个 $u_i$ 已知且固定，但分布 $p$ 未知。

如果 $f$ 是 $x$ 的任意函数，那么

$$
\mathbf{E}f=\sum_{i=1}^n p_i f(u_i)
$$

是 $p$ 的线性函数。如果 $S$ 是 $\mathbf{R}$ 的任意子集，那么

$$
\operatorname{\mathbf{prob}}(x\in S)=\sum_{u_i\in S}p_i
$$

也是 $p$ 的线性函数。

虽然不知道 $p$，但我们拥有如下形式的先验知识：已知 $x$ 的某些函数的期望值，以及 $\mathbf{R}$ 的某些子集的概率的上下界。这些先验知识可以表示成关于 $p$ 的线性不等式约束，

$$
\alpha_i\leq a_i^Tp\leq\beta_i,\quad i=1,\ldots,m.
$$

问题是给出 $\mathbf{E}f_0(x)=a_0^Tp$ 的下界和上界，其中 $f_0$ 是 $x$ 的某个函数。

为求得下界，求解以下以 $p$ 为变量的 LP：

$$
\begin{array}{ll}
\text{最小化} & a_0^Tp\\
\text{约束条件} & p\succeq0,\quad\mathbf{1}^Tp=1\\
& \alpha_i\leq a_i^Tp\leq\beta_i,\quad i=1,\ldots,m.
\end{array}
$$

这个 LP 的最优值，就是所有符合先验信息的分布中 $\mathbf{E}f_0(X)$ 能达到的最低值。而且，这个界是紧的：最优解给出了一个既符合先验信息、又达到该下界的分布。类似地，在相同约束下最大化 $a_0^Tp$，可以找到最好的上界。（我们将在第 7.4.1 节更详细地讨论 Chebyshev 不等式。）

#### 分段线性函数最小化

考虑对分段线性凸函数

$$
f(x)=\max_{i=1,\ldots,m}(a_i^Tx+b_i)
$$

进行无约束最小化的问题。这个问题可以转换为等价的 LP：先写成上图形式，

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & \max_{i=1,\ldots,m}(a_i^Tx+b_i)\leq t,
\end{array}
$$

<!-- pdf-page: 165 -->

然后将这个不等式表示为 $m$ 个独立的不等式：

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & a_i^Tx+b_i\leq t,\quad i=1,\ldots,m.
\end{array}
$$

这是以 $x$ 和 $t$ 为变量的不等式形式 LP。

### 4.3.2 线性分式规划

在多面体上最小化两个仿射函数之比的问题称为**线性分式规划**：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & Gx\preceq h\\
& Ax=b,
\end{array}
\tag{4.32}
$$

其中目标函数为

$$
f_0(x)=\frac{c^Tx+d}{e^Tx+f},\qquad\operatorname{\mathbf{dom}}f_0=\{x\mid e^Tx+f>0\}.
$$

目标函数是拟凸的（事实上是拟线性的），所以线性分式规划是拟凸优化问题。

#### 转换为线性规划

如果可行集

$$
\{x\mid Gx\preceq h,\ Ax=b,\ e^Tx+f>0\}
$$

非空，那么线性分式规划 (4.32) 可以转换为等价的线性规划

$$
\begin{array}{ll}
\text{最小化} & c^Ty+dz\\
\text{约束条件} & Gy-hz\preceq0\\
& Ay-bz=0\\
& e^Ty+fz=1\\
& z\geq0,
\end{array}
\tag{4.33}
$$

其中变量为 $y,z$。

为说明等价性，首先注意到：如果 $x$ 对 (4.32) 可行，那么

$$
y=\frac{x}{e^Tx+f},\qquad z=\frac{1}{e^Tx+f}
$$

这一对变量对 (4.33) 可行，而且有相同的目标值 $c^Ty+dz=f_0(x)$。由此可知，(4.32) 的最优值大于或等于 (4.33) 的最优值。

反过来，如果 $(y,z)$ 对 (4.33) 可行且 $z\ne0$，那么 $x=y/z$ 对 (4.32) 可行，而且有相同的目标值 $f_0(x)=c^Ty+dz$。如果 $(y,z)$ 对 (4.33) 可行且 $z=0$，并且 $x_0$ 对 (4.32) 可行，那么对所有 $t\geq0$，$x=x_0+ty$ 都对 (4.32) 可行。而且，$\lim_{t\to\infty}f_0(x_0+ty)=c^Ty+dz$，因此可以在 (4.32) 中找到可行点，使其目标值任意接近 $(y,z)$ 的目标值。由此得出，(4.32) 的最优值小于或等于 (4.33) 的最优值。

<!-- pdf-page: 166 -->

#### 广义线性分式规划

线性分式规划 (4.32) 的一种推广是**广义线性分式规划**，其中

$$
f_0(x)=\max_{i=1,\ldots,r}\frac{c_i^Tx+d_i}{e_i^Tx+f_i},\qquad
\operatorname{\mathbf{dom}}f_0=\{x\mid e_i^Tx+f_i>0,\ i=1,\ldots,r\}.
$$

目标函数是 $r$ 个拟凸函数的逐点最大值，因此也是拟凸函数，所以这个问题是拟凸问题。当 $r=1$ 时，它就退化为标准的线性分式规划。

<div class="example" markdown="1">

**例 4.7 Von Neumann 增长问题。** 考虑一个有 $n$ 个部门的经济体，当前时期的活动水平为 $x_i>0$，下一时期的活动水平为 $x_i^+>0$。（这个问题只考虑一个时期。）这些活动既消耗也生产 $m$ 种产品：活动水平 $x$ 消耗的产品数量为 $Bx\in\mathbf{R}^m$，生产的产品数量为 $Ax$。下一期消耗的产品数量不能超过当前时期生产的产品数量，即 $Bx^+\preceq Ax$。第 $i$ 个部门在这一时期的增长率为 $x_i^+/x_i$。

Von Neumann 增长问题是寻找一个活动水平向量 $x$，使整个经济体各部门中的最小增长率最大。这个问题可以表示为广义线性分式问题

$$
\begin{array}{ll}
\text{最大化} & \min_{i=1,\ldots,n}x_i^+/x_i\\
\text{约束条件} & x^+\succeq0\\
& Bx^+\preceq Ax,
\end{array}
$$

定义域为 $\{(x,x^+)\mid x\succ0\}$。注意，这个问题关于 $x$ 和 $x^+$ 是齐次的，因此可以将隐式约束 $x\succ0$ 替换为显式约束 $x\succeq\mathbf{1}$。

</div>

## 4.4 二次优化问题

如果目标函数是凸二次函数，约束函数都是仿射函数，就称凸优化问题 (4.15) 为**二次规划**（quadratic program，QP）。二次规划可以表示为

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r\\
\text{约束条件} & Gx\preceq h\\
& Ax=b,
\end{array}
\tag{4.34}
$$

其中 $P\in\mathbf{S}_+^n$、$G\in\mathbf{R}^{m\times n}$、$A\in\mathbf{R}^{p\times n}$。在二次规划中，我们是在多面体上最小化一个凸二次函数，如图 4.5 所示。

如果 (4.15) 中的目标函数和不等式约束函数都是凸二次函数，例如

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TP_0x+q_0^Tx+r_0\\
\text{约束条件} & (1/2)x^TP_ix+q_i^Tx+r_i\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
\tag{4.35}
$$

<!-- pdf-page: 167 -->

其中 $P_i\in\mathbf{S}_+^n$，$i=0,1,\ldots,m$，就称这个问题为**二次约束二次规划**（quadratically constrained quadratic program，QCQP）。在 QCQP 中，我们是在一个可行区域上最小化凸二次函数；当 $P_i\succ0$ 时，这个可行区域是若干椭球的交。

<figure id="fig-4-5" data-figure="4.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-5.png" alt="多面体可行集与凸二次目标函数的等值线，最优点位于多面体边界上" data-source-page="167" data-source-rect="192,122,380,288">
<figcaption>图 4.5 二次规划（QP）的几何示意。可行集 $\mathcal{P}$ 是一个多面体，用阴影表示。目标函数是凸二次函数，其等值线用虚线表示。点 $x^\star$ 是最优点。</figcaption>
</figure>

二次规划以线性规划为特殊情形，只需在 (4.34) 中取 $P=0$。二次约束二次规划则以二次规划为特殊情形，因而也包含线性规划；只需在 (4.35) 中，对 $i=1,\ldots,m$ 取 $P_i=0$。

### 4.4.1 例子

#### 最小二乘与回归

最小化凸二次函数

$$
\|Ax-b\|_2^2=x^TA^TAx-2b^TAx+b^Tb
$$

的问题是一个无约束 QP。它出现在许多领域，也有许多名称，例如**回归分析**或**最小二乘逼近**。这个问题足够简单，具有熟知的解析解 $x=A^\dagger b$，其中 $A^\dagger$ 是 $A$ 的伪逆（见第 A.5.4 节）。

加入线性不等式约束后，这个问题称为**约束回归**或**约束最小二乘**，此时不再有简单的解析解。例如，可以考虑变量带有下界和上界的回归问题，即

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2\\
\text{约束条件} & l_i\leq x_i\leq u_i,\quad i=1,\ldots,n,
\end{array}
$$

<!-- pdf-page: 168 -->

这是一个 QP。（我们将在第 6 章和第 7 章更深入地研究最小二乘与回归问题。）

#### 多面体之间的距离

$\mathbf{R}^n$ 中的多面体 $\mathcal{P}_1=\{x\mid A_1x\preceq b_1\}$ 和 $\mathcal{P}_2=\{x\mid A_2x\preceq b_2\}$ 之间的欧几里得距离定义为

$$
\operatorname{\mathbf{dist}}(\mathcal{P}_1,\mathcal{P}_2)=\inf\{\|x_1-x_2\|_2\mid x_1\in\mathcal{P}_1,\ x_2\in\mathcal{P}_2\}.
$$

如果两个多面体相交，距离就是零。

为求出 $\mathcal{P}_1$ 和 $\mathcal{P}_2$ 之间的距离，可以求解以下以 $x_1,x_2\in\mathbf{R}^n$ 为变量的 QP：

$$
\begin{array}{ll}
\text{最小化} & \|x_1-x_2\|_2^2\\
\text{约束条件} & A_1x_1\preceq b_1,\quad A_2x_2\preceq b_2.
\end{array}
$$

这个问题不可行，当且仅当至少一个多面体为空。最优值为零，当且仅当两个多面体相交；此时最优的 $x_1$ 与 $x_2$ 相同，是交集 $\mathcal{P}_1\cap\mathcal{P}_2$ 中的一个点。否则，最优的 $x_1$ 和 $x_2$ 分别是 $\mathcal{P}_1$ 和 $\mathcal{P}_2$ 中彼此最近的两个点。（我们将在第 8 章更详细地研究涉及距离的几何问题。）

#### 求方差的界

再次考虑第 150 页的 Chebyshev 不等式例子，其中变量是向量 $p\in\mathbf{R}^n$ 给出的未知概率分布，而我们已知关于它的一些先验信息。随机变量 $f(x)$ 的方差为

$$
\mathbf{E}f^2-(\mathbf{E}f)^2=\sum_{i=1}^n f_i^2p_i-\left(\sum_{i=1}^n f_ip_i\right)^2,
$$

其中 $f_i=f(u_i)$。这是关于 $p$ 的凹二次函数。

因此，在给定先验信息的约束下，可以通过求解以下 QP 来最大化 $f(x)$ 的方差：

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum_{i=1}^n f_i^2p_i-\left(\sum_{i=1}^n f_ip_i\right)^2\\
\text{约束条件} & p\succeq0,\quad\mathbf{1}^Tp=1\\
& \alpha_i\leq a_i^Tp\leq\beta_i,\quad i=1,\ldots,m.
\end{array}
$$

最优值给出了所有符合先验信息的分布中，$f(x)$ 可能具有的最大方差；最优的 $p$ 则给出了达到这个最大方差的分布。

#### 代价随机的线性规划

考虑 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Gx\preceq h\\
& Ax=b,
\end{array}
$$

<!-- pdf-page: 169 -->

其中变量为 $x\in\mathbf{R}^n$。假设代价函数的系数向量 $c\in\mathbf{R}^n$ 是随机的，其均值为 $\bar c$，协方差为 $\mathbf{E}(c-\bar c)(c-\bar c)^T=\Sigma$。（为简单起见，假设问题的其他参数是确定的。）对于给定的 $x\in\mathbf{R}^n$，代价 $c^Tx$ 是一个标量随机变量，其均值为 $\mathbf{E}c^Tx=\bar c^Tx$，方差为

$$
\operatorname{\mathbf{var}}(c^Tx)=\mathbf{E}(c^Tx-\mathbf{E}c^Tx)^2=x^T\Sigma x.
$$

一般来说，较小的期望代价与较小的代价方差之间存在权衡。将方差纳入考虑的一种方法，是最小化代价期望与方差的线性组合，即

$$
\mathbf{E}c^Tx+\gamma\operatorname{\mathbf{var}}(c^Tx),
$$

它称为**风险敏感代价**。参数 $\gamma\geq0$ 称为**风险厌恶参数**，因为它设定了代价方差与期望值之间的相对权重。（当 $\gamma>0$ 时，我们愿意接受期望代价增加，以换取代价方差足够大的下降。）

为最小化风险敏感代价，求解 QP

$$
\begin{array}{ll}
\text{最小化} & \bar c^Tx+\gamma x^T\Sigma x\\
\text{约束条件} & Gx\preceq h\\
& Ax=b.
\end{array}
$$

#### Markowitz 投资组合优化

考虑一个经典的投资组合问题：在一段时间内持有 $n$ 种资产或股票。用 $x_i$ 表示在整个时期内持有的第 $i$ 种资产的数量，按照期初价格折算，以美元计量。第 $i$ 种资产的普通多头头寸对应 $x_i>0$；空头头寸，即在期末买入该资产的义务，对应 $x_i<0$。用 $p_i$ 表示第 $i$ 种资产在这一时期内的相对价格变动，即这段时间内的价格变化除以期初价格。投资组合的总收益为 $r=p^Tx$，以美元计量。优化变量是投资组合向量 $x\in\mathbf{R}^n$。

可以对投资组合考虑多种约束。最简单的一组约束为 $x_i\geq0$，即不允许空头头寸，以及 $\mathbf{1}^Tx=B$，即投入的总预算为 $B$，通常取 $B=1$。

我们对价格变化采用随机模型：$p\in\mathbf{R}^n$ 是随机向量，其均值 $\bar p$ 和协方差 $\Sigma$ 已知。因此，对于投资组合 $x\in\mathbf{R}^n$，收益 $r$ 是一个标量随机变量，其均值为 $\bar p^Tx$，方差为 $x^T\Sigma x$。选择投资组合 $x$ 时，需要在收益的均值与方差之间进行权衡。

由 Markowitz 提出的经典投资组合优化问题为以下 QP：

$$
\begin{array}{ll}
\text{最小化} & x^T\Sigma x\\
\text{约束条件} & \bar p^Tx\geq r_{\min}\\
& \mathbf{1}^Tx=1,\quad x\succeq0,
\end{array}
$$

其中变量 $x$ 是投资组合。这里要找出使收益方差最小的投资组合，收益方差与投资组合的风险相关；同时要求<!-- pdf-page: 170 -->达到最低可接受的平均收益 $r_{\min}$，并满足投资组合的预算约束和禁止做空约束。

这个问题可以有许多扩展。例如，一种常见扩展是允许空头头寸，即允许 $x_i<0$。为此，引入变量 $x_{\mathrm{long}}$ 和 $x_{\mathrm{short}}$，满足

$$
x_{\mathrm{long}}\succeq0,\qquad x_{\mathrm{short}}\succeq0,\qquad
x=x_{\mathrm{long}}-x_{\mathrm{short}},\qquad
\mathbf{1}^Tx_{\mathrm{short}}\leq\eta\mathbf{1}^Tx_{\mathrm{long}}.
$$

最后一个约束将期初的空头总头寸限制为期初多头总头寸的一定比例 $\eta$。

另一种扩展是在投资组合优化问题中加入线性交易成本。从给定的初始投资组合 $x_{\mathrm{init}}$ 出发，通过买卖资产得到投资组合 $x$，随后在上述时期内持有它。买入和卖出资产时，需要支付与买卖金额成比例的交易费用。为处理这一点，引入变量 $u_{\mathrm{buy}}$ 和 $u_{\mathrm{sell}}$，分别确定持有期开始前买入和卖出各种资产的金额。它们满足约束

$$
x=x_{\mathrm{init}}+u_{\mathrm{buy}}-u_{\mathrm{sell}},\qquad
u_{\mathrm{buy}}\succeq0,\qquad u_{\mathrm{sell}}\succeq0.
$$

将简单的预算约束 $\mathbf{1}^Tx=1$ 替换为以下条件：初始买卖交易连同交易费用在内，净现金流为零，

$$
(1-f_{\mathrm{sell}})\mathbf{1}^Tu_{\mathrm{sell}}=(1+f_{\mathrm{buy}})\mathbf{1}^Tu_{\mathrm{buy}}.
$$

左端是卖出资产所得的总收入减去卖出交易费用，右端是买入资产的总成本，包括交易费用。常数 $f_{\mathrm{buy}}\geq0$ 和 $f_{\mathrm{sell}}\geq0$ 分别为买入和卖出的交易费率；为简单起见，假设它们对所有资产都相同。

在满足最低平均收益、预算及交易约束的条件下，最小化收益方差的问题，是一个以 $x,u_{\mathrm{buy}},u_{\mathrm{sell}}$ 为变量的 QP。

### 4.4.2 二阶锥规划

与二次规划密切相关的一类问题是**二阶锥规划**（second-order cone program，SOCP）：

$$
\begin{array}{ll}
\text{最小化} & f^Tx\\
\text{约束条件} & \|A_ix+b_i\|_2\leq c_i^Tx+d_i,\quad i=1,\ldots,m\\
& Fx=g,
\end{array}
\tag{4.36}
$$

其中 $x\in\mathbf{R}^n$ 是优化变量，$A_i\in\mathbf{R}^{n_i\times n}$，$F\in\mathbf{R}^{p\times n}$。我们将形如

$$
\|Ax+b\|_2\leq c^Tx+d,
$$

其中 $A\in\mathbf{R}^{k\times n}$，的约束称为**二阶锥约束**，因为它等价于要求仿射函数 $(Ax+b,c^Tx+d)$ 的值落在 $\mathbf{R}^{k+1}$ 中的二阶锥内。

当 $c_i=0$，$i=1,\ldots,m$ 时，SOCP (4.36) 等价于一个 QCQP，对各个约束两边平方即可得到它。类似地，如果 $A_i=0$，$i=1,\ldots,m$，那么 SOCP (4.36) 就退化为一般的 LP。不过，二阶锥规划比 QCQP 更一般，当然也比 LP 更一般。

<!-- pdf-page: 171 -->

#### 鲁棒线性规划

考虑不等式形式的线性规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & a_i^Tx\leq b_i,\quad i=1,\ldots,m,
\end{array}
$$

其中参数 $c,a_i,b_i$ 存在一定的不确定性或变化。为简化叙述，假设 $c$ 和 $b_i$ 固定，而已知 $a_i$ 位于给定的椭球中：

$$
a_i\in\mathcal{E}_i=\{\bar a_i+P_iu\mid\|u\|_2\leq1\},
$$

其中 $P_i\in\mathbf{R}^{n\times n}$。（如果 $P_i$ 奇异，得到的就是维数为 $\operatorname{\mathbf{rank}}P_i$ 的“扁平”椭球；$P_i=0$ 则表示 $a_i$ 完全已知。）

我们要求约束对于参数 $a_i$ 的所有可能取值都成立，从而得到**鲁棒线性规划**

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & a_i^Tx\leq b_i\quad\text{对所有 }a_i\in\mathcal{E}_i,\quad i=1,\ldots,m.
\end{array}
\tag{4.37}
$$

鲁棒线性约束“对所有 $a_i\in\mathcal{E}_i$，都有 $a_i^Tx\leq b_i$”可以表示为

$$
\sup\{a_i^Tx\mid a_i\in\mathcal{E}_i\}\leq b_i,
$$

其左端可以写为

$$
\begin{aligned}
\sup\{a_i^Tx\mid a_i\in\mathcal{E}_i\}
&=\bar a_i^Tx+\sup\{u^TP_i^Tx\mid\|u\|_2\leq1\}\\
&=\bar a_i^Tx+\|P_i^Tx\|_2.
\end{aligned}
$$

因此，鲁棒线性约束可以表示为

$$
\bar a_i^Tx+\|P_i^Tx\|_2\leq b_i,
$$

它显然是一个二阶锥约束。所以鲁棒 LP (4.37) 可以写成 SOCP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \bar a_i^Tx+\|P_i^Tx\|_2\leq b_i,\quad i=1,\ldots,m.
\end{array}
$$

注意，新增的范数项起到了正则化项的作用；它们防止 $x$ 在参数 $a_i$ 不确定性较大的方向上取过大的值。

#### 约束随机的线性规划

上面描述的鲁棒 LP 也可以放在统计框架下考虑。这里假设参数 $a_i$ 是相互独立的高斯随机向量，其均值为 $\bar a_i$，协方差为 $\Sigma_i$。我们要求每个约束 $a_i^Tx\leq b_i$ 成立的概率或置信度达到 $\eta$ 以上，其中 $\eta\geq0.5$，即

$$
\operatorname{\mathbf{prob}}(a_i^Tx\leq b_i)\geq\eta.
\tag{4.38}
$$

<!-- pdf-page: 172 -->

下面将说明，这个概率约束可以表示为二阶锥约束。

令 $u=a_i^Tx$，用 $\sigma^2$ 表示其方差，则这个约束可以写成

$$
\operatorname{\mathbf{prob}}\left(\frac{u-\bar u}{\sigma}\leq\frac{b_i-\bar u}{\sigma}\right)\geq\eta.
$$

由于 $(u-\bar u)/\sigma$ 是均值为零、方差为一的高斯随机变量，上面的概率就是 $\Phi((b_i-\bar u)/\sigma)$，其中

$$
\Phi(z)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^z e^{-t^2/2}\,dt
$$

是均值为零、方差为一的高斯随机变量的累积分布函数。因此，概率约束 (4.38) 可以表示为

$$
\frac{b_i-\bar u}{\sigma}\geq\Phi^{-1}(\eta),
$$

或者等价地，

$$
\bar u+\Phi^{-1}(\eta)\sigma\leq b_i.
$$

由 $\bar u=\bar a_i^Tx$ 和 $\sigma=(x^T\Sigma_i x)^{1/2}$，得到

$$
\bar a_i^Tx+\Phi^{-1}(\eta)\|\Sigma_i^{1/2}x\|_2\leq b_i.
$$

根据假设 $\eta\geq1/2$，有 $\Phi^{-1}(\eta)\geq0$，所以这个约束是二阶锥约束。

总之，问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \operatorname{\mathbf{prob}}(a_i^Tx\leq b_i)\geq\eta,\quad i=1,\ldots,m
\end{array}
$$

可以表示为 SOCP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \bar a_i^Tx+\Phi^{-1}(\eta)\|\Sigma_i^{1/2}x\|_2\leq b_i,\quad i=1,\ldots,m.
\end{array}
$$

（我们将在第 6 章更深入地讨论鲁棒凸优化问题。另见习题 4.13、4.28 和 4.59。）

<div class="example" markdown="1">

**例 4.8 带有损失风险约束的投资组合优化。** 再次考虑前面第 155 页介绍的经典 Markowitz 投资组合问题。这里假设价格变化向量 $p\in\mathbf{R}^n$ 是高斯随机变量，其均值为 $\bar p$，协方差为 $\Sigma$。因此，收益 $r$ 是高斯随机变量，其均值为 $\bar r=\bar p^Tx$，方差为 $\sigma_r^2=x^T\Sigma x$。

考虑形如

$$
\operatorname{\mathbf{prob}}(r\leq\alpha)\leq\beta
\tag{4.39}
$$

的损失风险约束，其中 $\alpha$ 是一个给定的不希望出现的收益水平，例如较大的亏损，$\beta$ 是给定的最大概率。

<!-- pdf-page: 173 -->

与上面对鲁棒 LP 的随机解释一样，可以利用标准高斯随机变量的累积分布函数 $\Phi$ 来表示这个约束。不等式 (4.39) 等价于

$$
\bar p^Tx+\Phi^{-1}(\beta)\|\Sigma^{1/2}x\|_2\geq\alpha.
$$

只要 $\beta\leq1/2$，即 $\Phi^{-1}(\beta)\leq0$，这个损失风险约束就是二阶锥约束。（如果 $\beta>1/2$，那么损失风险约束关于 $x$ 就不再是凸的。）

因此，在损失风险受到限制且 $\beta\leq1/2$ 的条件下，最大化期望收益的问题，可以写成只有一个二阶锥约束的 SOCP：

$$
\begin{array}{ll}
\text{最大化} & \bar p^Tx\\
\text{约束条件} & \bar p^Tx+\Phi^{-1}(\beta)\|\Sigma^{1/2}x\|_2\geq\alpha\\
& x\succeq0,\quad\mathbf{1}^Tx=1.
\end{array}
$$

这个问题有许多扩展。例如，可以施加多个损失风险约束，即

$$
\operatorname{\mathbf{prob}}(r\leq\alpha_i)\leq\beta_i,\quad i=1,\ldots,k,
$$

其中 $\beta_i\leq1/2$；它们表示对于不同的损失水平 $\alpha_i$，我们愿意接受的风险 $\beta_i$。

</div>

#### 极小曲面

考虑可微函数 $f:\mathbf{R}^2\to\mathbf{R}$，$\operatorname{\mathbf{dom}}f=C$。其图像的曲面面积为

$$
A=\int_C\sqrt{1+\|\nabla f(x)\|_2^2}\,dx
=\int_C\|(\nabla f(x),1)\|_2\,dx,
$$

这是关于 $f$ 的凸泛函。**极小曲面问题**是寻找使 $A$ 最小的函数 $f$，同时满足某些约束，例如给定 $f$ 在 $C$ 的边界上的某些值。

我们通过将函数 $f$ 离散化来近似这个问题。令 $C=[0,1]\times[0,1]$，并用 $f_{ij}$ 表示 $f$ 在点 $(i/K,j/K)$ 处的值，其中 $i,j=0,\ldots,K$。利用前向差分，可以得到 $f$ 在点 $x=(i/K,j/K)$ 处梯度的近似表达式：

$$
\nabla f(x)\approx K\begin{bmatrix}f_{i+1,j}-f_{i,j}\\f_{i,j+1}-f_{i,j}\end{bmatrix}.
$$

将它代入图像面积的表达式，并用求和近似积分，得到曲面面积的近似值：

$$
A\approx A_{\mathrm{disc}}=\frac{1}{K^2}\sum_{i,j=0}^{K-1}
\left\|\begin{bmatrix}K(f_{i+1,j}-f_{i,j})\\K(f_{i,j+1}-f_{i,j})\\1\end{bmatrix}\right\|_2.
$$

离散化后的面积近似值 $A_{\mathrm{disc}}$ 是 $f_{ij}$ 的凸函数。

我们可以对 $f_{ij}$ 考虑多种约束，例如对其中任意元素施加等式或不等式约束，特别是对边界值施加约束；也可以<!-- pdf-page: 174 -->对其矩施加约束。作为一个例子，考虑正方形左右两条边上的边界值固定时，寻找面积最小曲面的问题：

$$
\begin{array}{ll}
\text{最小化} & A_{\mathrm{disc}}\\
\text{约束条件} & f_{0j}=l_j,\quad j=0,\ldots,K\\
& f_{Kj}=r_j,\quad j=0,\ldots,K,
\end{array}
\tag{4.40}
$$

其中 $f_{ij}$，$i,j=0,\ldots,K$，是变量，$l_j,r_j$ 分别为正方形左边和右边给定的边界值。

引入新变量 $t_{ij}$，$i,j=0,\ldots,K-1$，就可以将问题 (4.40) 转换为 SOCP：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle(1/K^2)\sum_{i,j=0}^{K-1}t_{ij}\\
\text{约束条件} & \left\|\begin{bmatrix}K(f_{i+1,j}-f_{i,j})\\K(f_{i,j+1}-f_{i,j})\\1\end{bmatrix}\right\|_2\leq t_{ij},\quad i,j=0,\ldots,K-1\\
& f_{0j}=l_j,\quad j=0,\ldots,K\\
& f_{Kj}=r_j,\quad j=0,\ldots,K.
\end{array}
$$

## 4.5 几何规划

本节介绍一族优化问题，它们在自然的表达形式下并不是凸问题。不过，通过变量变换以及目标函数和约束函数的变换，可以将它们转化为凸优化问题。

### 4.5.1 单项式与正项式

定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n$、形式为

$$
f(x)=cx_1^{a_1}x_2^{a_2}\cdots x_n^{a_n},
\tag{4.41}
$$

其中 $c>0$、$a_i\in\mathbf{R}$ 的函数 $f:\mathbf{R}^n\to\mathbf{R}$，称为**单项式函数**，简称**单项式**（monomial）。单项式的指数 $a_i$ 可以是任意实数，包括分数或负数，但系数 $c$ 只能是正数。（“单项式”这一术语与代数中的标准定义有所不同；代数中的指数必须是非负整数，不过这里应当不会造成混淆。）单项式的和，即形如

$$
f(x)=\sum_{k=1}^K c_kx_1^{a_{1k}}x_2^{a_{2k}}\cdots x_n^{a_{nk}},
\tag{4.42}
$$

其中 $c_k>0$ 的函数，称为具有 $K$ 项的**正项式函数**，简称**正项式**（posynomial）。

<!-- pdf-page: 175 -->

正项式对加法、乘法及非负数乘封闭。单项式对乘法和除法封闭。正项式乘以单项式，结果仍是正项式；类似地，正项式也可以除以单项式，结果仍是正项式。

### 4.5.2 几何规划

形如

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq1,\quad i=1,\ldots,m\\
& h_i(x)=1,\quad i=1,\ldots,p,
\end{array}
\tag{4.43}
$$

其中 $f_0,\ldots,f_m$ 是正项式，$h_1,\ldots,h_p$ 是单项式的优化问题，称为**几何规划**（geometric program，GP）。这个问题的定义域为 $\mathcal{D}=\mathbf{R}_{++}^n$；约束 $x\succ0$ 是隐含的。

#### 几何规划的扩展

几种扩展形式也容易处理。如果 $f$ 是正项式，$h$ 是单项式，那么可以将约束 $f(x)\leq h(x)$ 写成 $f(x)/h(x)\leq1$ 来处理，因为 $f/h$ 是正项式。这包含了形如 $f(x)\leq a$ 的约束这一特殊情况，其中 $f$ 为正项式，$a>0$。类似地，如果 $h_1$ 和 $h_2$ 都是非零单项式函数，那么可以将等式约束 $h_1(x)=h_2(x)$ 写成 $h_1(x)/h_2(x)=1$ 来处理，因为 $h_1/h_2$ 是单项式。我们可以通过最小化非零单项式目标函数的倒数，来最大化这个目标函数；它的倒数仍是单项式。

例如，考虑问题

$$
\begin{array}{ll}
\text{最大化} & x/y\\
\text{约束条件} & 2\leq x\leq3\\
& x^2+3y/z\leq\sqrt y\\
& x/y=z^2,
\end{array}
$$

其中变量为 $x,y,z\in\mathbf{R}$，并隐含约束 $x,y,z>0$。利用上述简单变换，得到等价的标准形式 GP

$$
\begin{array}{ll}
\text{最小化} & x^{-1}y\\
\text{约束条件} & 2x^{-1}\leq1,\quad(1/3)x\leq1\\
& x^2y^{-1/2}+3y^{1/2}z^{-1}\leq1\\
& xy^{-1}z^{-2}=1.
\end{array}
$$

像这样的、容易转换为等价标准形式 (4.43) 的问题，我们也称为 GP。这与把容易转换为 LP 的问题也称为 LP 的做法相同。

<!-- pdf-page: 176 -->

### 4.5.3 几何规划的凸形式

几何规划一般并不是凸优化问题，但通过变量变换以及目标函数和约束函数的变换，可以将它们转换为凸问题。

采用新变量 $y_i=\log x_i$，因此 $x_i=e^{y_i}$。如果 $f$ 是 (4.41) 给出的关于 $x$ 的单项式函数，即

$$
f(x)=cx_1^{a_1}x_2^{a_2}\cdots x_n^{a_n},
$$

那么

$$
\begin{aligned}
f(x)&=f(e^{y_1},\ldots,e^{y_n})\\
&=c(e^{y_1})^{a_1}\cdots(e^{y_n})^{a_n}\\
&=e^{a^Ty+b},
\end{aligned}
$$

其中 $b=\log c$。变量变换 $y_i=\log x_i$ 将单项式函数变成了仿射函数的指数。

类似地，如果 $f$ 是 (4.42) 给出的正项式，即

$$
f(x)=\sum_{k=1}^K c_kx_1^{a_{1k}}x_2^{a_{2k}}\cdots x_n^{a_{nk}},
$$

那么

$$
f(x)=\sum_{k=1}^K e^{a_k^Ty+b_k},
$$

其中 $a_k=(a_{1k},\ldots,a_{nk})$，$b_k=\log c_k$。变量变换后，正项式变成了若干仿射函数的指数之和。

几何规划 (4.43) 用新变量 $y$ 可以表示为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{k=1}^{K_0}e^{a_{0k}^Ty+b_{0k}}\\
\text{约束条件} & \displaystyle\sum_{k=1}^{K_i}e^{a_{ik}^Ty+b_{ik}}\leq1,\quad i=1,\ldots,m\\
& e^{g_i^Ty+h_i}=1,\quad i=1,\ldots,p,
\end{array}
$$

其中 $a_{ik}\in\mathbf{R}^n$，$i=0,\ldots,m$，包含原几何规划中正项式不等式约束的指数，而 $g_i\in\mathbf{R}^n$，$i=1,\ldots,p$，包含单项式等式约束的指数。

现在通过取对数来变换目标函数和约束函数，得到问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\widetilde f_0(y)=\log\left(\sum_{k=1}^{K_0}e^{a_{0k}^Ty+b_{0k}}\right)\\
\text{约束条件} & \displaystyle\widetilde f_i(y)=\log\left(\sum_{k=1}^{K_i}e^{a_{ik}^Ty+b_{ik}}\right)\leq0,\quad i=1,\ldots,m\\
& \widetilde h_i(y)=g_i^Ty+h_i=0,\quad i=1,\ldots,p.
\end{array}
\tag{4.44}
$$

由于函数 $\widetilde f_i$ 都是凸函数，$\widetilde h_i$ 都是仿射函数，这个问题是凸优化问题。我们称它为**凸形式的几何规划**。为<!-- pdf-page: 177 -->与原来的几何规划区分，我们将 (4.43) 称为**正项式形式的几何规划**。

注意，正项式形式的几何规划 (4.43) 与凸形式的几何规划 (4.44) 之间的转换不涉及任何计算；这两个问题的数据相同。转换只是改变了目标函数和约束函数的形式。

如果正项式目标函数和约束函数都只有一项，即都是单项式，那么凸形式的几何规划 (4.44) 就退化为一般的线性规划。因此，可以把几何规划看作线性规划的一种推广或扩展。

### 4.5.4 例子

#### Frobenius 范数的对角缩放

考虑矩阵 $M\in\mathbf{R}^{n\times n}$，以及相应的将 $u$ 映射为 $y=Mu$ 的线性函数。假设我们缩放坐标，即作变量变换 $\widetilde u=Du$、$\widetilde y=Dy$，其中 $D$ 是对角矩阵，且 $D_{ii}>0$。在新坐标下，这个线性函数为 $\widetilde y=DMD^{-1}\widetilde u$。

现在希望选择一种缩放，使得到的矩阵 $DMD^{-1}$ 较小。用 Frobenius 范数的平方来衡量矩阵的大小：

$$
\begin{aligned}
\|DMD^{-1}\|_F^2
&=\operatorname{\mathbf{tr}}\left((DMD^{-1})^T(DMD^{-1})\right)\\
&=\sum_{i,j=1}^n(DMD^{-1})_{ij}^2\\
&=\sum_{i,j=1}^n M_{ij}^2d_i^2/d_j^2,
\end{aligned}
$$

其中 $D=\operatorname{\mathbf{diag}}(d)$。由于这是关于 $d$ 的正项式，选择缩放 $d$ 以最小化 Frobenius 范数的问题，就是一个无约束几何规划：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i,j=1}^n M_{ij}^2d_i^2/d_j^2,
\end{array}
$$

其中变量为 $d$。这个几何规划中出现的指数只有 $0$、$2$ 和 $-2$。

#### 悬臂梁设计

考虑一根由 $N$ 段组成的悬臂梁的设计问题，这些分段从右到左编号为 $1,\ldots,N$，如图 4.6 所示。每段长度均为 1，横截面为均匀的矩形，宽度为 $w_i$、高度为 $h_i$。梁的右端承受一个竖直载荷，即力 $F$。这个载荷使梁向下挠曲，并在梁的每一段中产生应力。假设挠度很小，材料具有线性弹性，杨氏模量为 $E$。

<!-- pdf-page: 178 -->

<figure id="fig-4-6" data-figure="4.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-6.png" alt="由四段组成的悬臂梁，左端固定，右端受到竖直向下的力 F" data-source-page="178" data-source-rect="211,116,463,208">
<figcaption>图 4.6 由 4 段组成的分段悬臂梁。每段的长度均为 1，截面为矩形。梁的右端施加竖直力 $F$。</figcaption>
<p class="figure-translation">图内文字：从左到右，segment 4：第 4 段；segment 3：第 3 段；segment 2：第 2 段；segment 1：第 1 段。</p>
</figure>

这个问题中的设计变量是 $N$ 段梁各自的宽度 $w_i$ 和高度 $h_i$。我们希望在一些设计约束下，最小化与梁的重量成比例的总体积，

$$
w_1h_1+\cdots+w_Nh_N.
$$

对各段的宽度和高度施加上下界约束，

$$
w_{\min}\leq w_i\leq w_{\max},\qquad h_{\min}\leq h_i\leq h_{\max},\quad i=1,\ldots,N,
$$

并对高宽比施加约束，

$$
S_{\min}\leq h_i/w_i\leq S_{\max}.
$$

此外，还要限制材料中的最大容许应力，以及梁末端的竖直挠度。

先考虑最大应力约束。用 $\sigma_i$ 表示第 $i$ 段中的最大应力，它由 $\sigma_i=6iF/(w_i h_i^2)$ 给出。施加约束

$$
\frac{6iF}{w_i h_i^2}\leq\sigma_{\max},\quad i=1,\ldots,N,
$$

就能保证梁上任何位置的应力都不超过最大容许值 $\sigma_{\max}$。

最后一个约束限制梁末端的竖直挠度，用 $y_1$ 表示这个挠度：

$$
y_1\leq y_{\max}.
$$

挠度 $y_1$ 可以通过一个涉及各段梁的挠度和斜率的递推来求得：

$$
v_i=12(i-1/2)\frac{F}{Ew_i h_i^3}+v_{i+1},\qquad
y_i=6(i-1/3)\frac{F}{Ew_i h_i^3}+v_{i+1}+y_{i+1},
\tag{4.45}
$$

其中 $i=N,N-1,\ldots,1$，初始值为 $v_{N+1}=y_{N+1}=0$。在这个递推中，$y_i$ 是第 $i$ 段右端的挠度，$v_i$ 是该点的斜率。利用递推式 (4.45)，可以证明这些挠度和斜率<!-- pdf-page: 179 -->实际上都是变量 $w$ 和 $h$ 的正项式函数。首先，$v_{N+1}$ 和 $y_{N+1}$ 都为零，因此是正项式。现在假设 $v_{i+1}$ 和 $y_{i+1}$ 是 $w$ 和 $h$ 的正项式函数。(4.45) 左边的等式说明，$v_i$ 是一个单项式与一个正项式 $v_{i+1}$ 的和，因此也是正项式。由 (4.45) 右边的等式可知，挠度 $y_i$ 是一个单项式与两个正项式 $v_{i+1}$、$y_{i+1}$ 的和，所以也是正项式。特别地，梁末端的挠度 $y_1$ 是正项式。

于是，问题为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^N w_i h_i\\
\text{约束条件} & w_{\min}\leq w_i\leq w_{\max},\quad i=1,\ldots,N\\
& h_{\min}\leq h_i\leq h_{\max},\quad i=1,\ldots,N\\
& S_{\min}\leq h_i/w_i\leq S_{\max},\quad i=1,\ldots,N\\
& 6iF/(w_i h_i^2)\leq\sigma_{\max},\quad i=1,\ldots,N\\
& y_1\leq y_{\max},
\end{array}
\tag{4.46}
$$

其中变量为 $w$ 和 $h$。这是一个 GP，因为目标函数是正项式，所有约束都可以表示为正项式不等式。（事实上，除挠度限制是一个复杂的正项式不等式之外，其余约束都可以表示为单项式不等式。）

当分段数 $N$ 很大时，正项式 $y_1$ 中出现的单项式项数大致按 $N^2$ 增长。习题 4.31 讨论了这个问题的另一种表达方式：将 $v_1,\ldots,v_N$ 和 $y_1,\ldots,y_N$ 引入为变量，并把递推式的一个修改版本作为一组约束。这种表达方式避免了单项式项数的上述增长。

#### 利用 Perron–Frobenius 理论最小化谱半径

设矩阵 $A\in\mathbf{R}^{n\times n}$ 逐元素非负，即对于 $i,j=1,\ldots,n$，都有 $A_{ij}\geq0$；并且它**不可约**，意思是矩阵 $(I+A)^{n-1}$ 的每个元素都为正。Perron–Frobenius 定理指出，$A$ 有一个正实特征值 $\lambda_{\mathrm{pf}}$，等于它的谱半径，即它的所有特征值的模的最大值。Perron–Frobenius 特征值 $\lambda_{\mathrm{pf}}$ 确定了当 $k\to\infty$ 时，$A^k$ 的渐近增长率或衰减率；事实上，矩阵 $((1/\lambda_{\mathrm{pf}})A)^k$ 收敛。粗略地说，这意味着当 $k\to\infty$ 时，如果 $\lambda_{\mathrm{pf}}>1$，$A^k$ 按 $\lambda_{\mathrm{pf}}^k$ 的量级增长；如果 $\lambda_{\mathrm{pf}}<1$，则按 $\lambda_{\mathrm{pf}}^k$ 的量级衰减。

<div class="translator-note" markdown="1">

**译注（矩阵幂的收敛）：** 仅有非负和不可约条件，还不足以保证这里的归一化矩阵幂收敛；还需排除周期性。例如，要求 $A$ 为本原矩阵（primitive matrix，即存在正整数 $k$ 使 $A^k$ 逐项为正）即可。

</div>

非负矩阵理论中的一个基本结果是，Perron–Frobenius 特征值可表示为

$$
\lambda_{\mathrm{pf}}=\inf\{\lambda\mid Av\preceq\lambda v\text{ 对某个 }v\succ0\text{ 成立}\},
$$

而且这个下确界能够取到。不等式 $Av\preceq\lambda v$ 可以表示为

$$
\sum_{j=1}^n A_{ij}v_j/(\lambda v_i)\leq1,\quad i=1,\ldots,n,
\tag{4.47}
$$

这是一组关于变量 $A_{ij},v_i,\lambda$ 的正项式不等式。因此，条件 $\lambda_{\mathrm{pf}}\leq\lambda$ 可以表示为一组<!-- pdf-page: 180 -->关于 $A,v,\lambda$ 的正项式不等式。这使我们能够用几何规划求解一些涉及 Perron–Frobenius 特征值的优化问题。

假设矩阵 $A$ 的元素是某个底层变量 $x\in\mathbf{R}^k$ 的正项式函数。此时，不等式 (4.47) 就是关于变量 $x\in\mathbf{R}^k$、$v\in\mathbf{R}^n$ 和 $\lambda\in\mathbf{R}$ 的正项式不等式。考虑选择 $x$，使 $A$ 的 Perron–Frobenius 特征值或谱半径最小的问题，并允许对 $x$ 施加正项式不等式约束：

$$
\begin{array}{ll}
\text{最小化} & \lambda_{\mathrm{pf}}(A(x))\\
\text{约束条件} & f_i(x)\leq1,\quad i=1,\ldots,p,
\end{array}
$$

其中 $f_i$ 是正项式。利用上述刻画，可以将这个问题表示为 GP

$$
\begin{array}{ll}
\text{最小化} & \lambda\\
\text{约束条件} & \displaystyle\sum_{j=1}^n A_{ij}v_j/(\lambda v_i)\leq1,\quad i=1,\ldots,n\\
& f_i(x)\leq1,\quad i=1,\ldots,p,
\end{array}
$$

其中变量为 $x,v,\lambda$。

作为一个具体例子，考虑一个简单的细菌种群动态模型，用 $t=0,1,2,\ldots$ 表示时间或时期，单位为小时。向量 $p(t)\in\mathbf{R}_+^4$ 描述第 $t$ 期的种群年龄分布：$p_1(t)$ 是年龄在 0 到 1 小时之间的细菌总数，$p_2(t)$ 是年龄在 1 到 2 小时之间的细菌总数，其余类推。我们任意地假设没有细菌能够存活超过 4 小时。种群随时间按 $p(t+1)=Ap(t)$ 演化，其中

$$
A=\begin{bmatrix}
b_1&b_2&b_3&b_4\\
s_1&0&0&0\\
0&s_2&0&0\\
0&0&s_3&0
\end{bmatrix}.
$$

这里，$b_i$ 是第 $i$ 个年龄组的细菌出生率，$s_i$ 是从第 $i$ 个年龄组存活到第 $i+1$ 个年龄组的存活率。假设 $b_i>0$、$0<s_i<1$，这意味着矩阵 $A$ 不可约。

$A$ 的 Perron–Frobenius 特征值决定种群的渐近增长率或衰减率。如果 $\lambda_{\mathrm{pf}}<1$，种群数量按 $\lambda_{\mathrm{pf}}^t$ 的量级趋于零，因此半衰期为 $-1/\log_2\lambda_{\mathrm{pf}}$ 小时。如果 $\lambda_{\mathrm{pf}}>1$，种群数量按 $\lambda_{\mathrm{pf}}^t$ 成几何级数增长，倍增时间为 $1/\log_2\lambda_{\mathrm{pf}}$ 小时。最小化 $A$ 的谱半径，对应于寻找种群最快的衰减率，或者最慢的增长率。

我们取 $c_1$ 和 $c_2$ 作为矩阵 $A$ 所依赖的底层变量，它们是环境中两种化学物质的浓度，这两种物质会影响细菌的出生率和存活率。将出生率和存活率建模为这两个浓度的单项式函数：

$$
\begin{aligned}
b_i&=b_i^{\mathrm{nom}}(c_1/c_1^{\mathrm{nom}})^{\alpha_i}(c_2/c_2^{\mathrm{nom}})^{\beta_i},\quad i=1,\ldots,4,\\
s_i&=s_i^{\mathrm{nom}}(c_1/c_1^{\mathrm{nom}})^{\gamma_i}(c_2/c_2^{\mathrm{nom}})^{\delta_i},\quad i=1,\ldots,3.
\end{aligned}
$$

这里，$b_i^{\mathrm{nom}}$ 是标称出生率，$s_i^{\mathrm{nom}}$ 是标称存活率，$c_i^{\mathrm{nom}}$ 是第 $i$ 种化学物质的标称浓度。常数 $\alpha_i,\beta_i,\gamma_i,\delta_i$ 给出了化学物质浓度偏离标称值时，<!-- pdf-page: 181 -->出生率和存活率受到的影响。例如，$\alpha_2=-0.3$ 和 $\gamma_1=0.5$ 表示：第 1 种化学物质的浓度高于标称浓度时，年龄在 1 到 2 小时之间的细菌的出生率会下降，而细菌从 0 小时存活到 1 小时的存活率会上升。

假设可以通过施用药物，独立地提高或降低浓度 $c_1$ 和 $c_2$，例如控制在标称值的 $1/2$ 到 2 倍之间。我们要找出使种群衰减率最大的药物配比，即使 $\lambda_{\mathrm{pf}}(A)$ 最小的配比。利用上述方法，可以将这个问题写成 GP

$$
\begin{array}{ll}
\text{最小化} & \lambda\\
\text{约束条件} & b_1v_1+b_2v_2+b_3v_3+b_4v_4\leq\lambda v_1\\
& s_1v_1\leq\lambda v_2\\
& s_2v_2\leq\lambda v_3\\
& s_3v_3\leq\lambda v_4\\
& 1/2\leq c_i/c_i^{\mathrm{nom}}\leq2,\quad i=1,2\\
& b_i=b_i^{\mathrm{nom}}(c_1/c_1^{\mathrm{nom}})^{\alpha_i}(c_2/c_2^{\mathrm{nom}})^{\beta_i},\quad i=1,\ldots,4\\
& s_i=s_i^{\mathrm{nom}}(c_1/c_1^{\mathrm{nom}})^{\gamma_i}(c_2/c_2^{\mathrm{nom}})^{\delta_i},\quad i=1,\ldots,3,
\end{array}
$$

其中变量为 $b_i,s_i,c_i,v_i,\lambda$。

## 4.6 广义不等式约束

允许不等式约束函数取向量值，并在约束中使用广义不等式，就能得到标准形式凸优化问题 (4.15) 的一种非常有用的推广：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
\tag{4.48}
$$

其中 $f_0:\mathbf{R}^n\to\mathbf{R}$，$K_i\subseteq\mathbf{R}^{k_i}$ 是正常锥，$f_i:\mathbf{R}^n\to\mathbf{R}^{k_i}$ 是 $K_i$-凸函数。我们称它为带有广义不等式约束的标准形式凸优化问题。问题 (4.15) 就是 $K_i=\mathbf{R}_+$，$i=1,\ldots,m$，时的特殊情形。

普通凸优化问题的许多结果也适用于带有广义不等式的问题。例如：

- 可行集、任何下水平集以及最优解集都是凸集。
- 问题 (4.48) 的任何局部最优点都是全局最优点。
- 第 4.2.3 节给出的 $f_0$ 可微时的最优性条件，无须修改便仍然成立。

我们还将在第 11 章看到，带有广义不等式约束的凸优化问题，通常可以和普通凸优化问题一样容易地求解。

<!-- pdf-page: 182 -->

### 4.6.1 锥形式问题

带有广义不等式的凸优化问题中，最简单的一类是**锥形式问题**，也称为**锥规划**。它们具有线性目标函数，以及一个仿射不等式约束函数，后者因而也是 $K$-凸函数：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Fx+g\preceq_K0\\
& Ax=b.
\end{array}
\tag{4.49}
$$

当 $K$ 是非负正交象限时，锥形式问题就退化为线性规划。可以把锥形式问题看作线性规划的推广，用广义线性不等式替换其中的逐分量不等式。

继续类比线性规划，我们将锥形式问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & x\succeq_K0\\
& Ax=b
\end{array}
$$

称为**标准形式的锥形式问题**。类似地，问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Fx+g\preceq_K0
\end{array}
$$

称为**不等式形式的锥形式问题**。

### 4.6.2 半定规划

当 $K$ 为 $k\times k$ 半正定矩阵组成的锥 $\mathbf{S}_+^k$ 时，相应的锥形式问题称为**半定规划**（semidefinite program，SDP），具有形式

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & x_1F_1+\cdots+x_nF_n+G\preceq0\\
& Ax=b,
\end{array}
\tag{4.50}
$$

其中 $G,F_1,\ldots,F_n\in\mathbf{S}^k$、$A\in\mathbf{R}^{p\times n}$。这里的不等式是一个线性矩阵不等式，见例 2.10。

如果矩阵 $G,F_1,\ldots,F_n$ 都是对角矩阵，那么 (4.50) 中的 LMI 等价于一组 $n$ 个线性不等式，SDP (4.50) 就退化为线性规划。

<div class="translator-note" markdown="1">

**译注（对角 LMI）：** 按矩阵阶数 $k$ 逐个对角元展开，应得到 $k$ 条线性不等式；$n$ 是优化变量的个数。

</div>

#### 标准形式与不等式形式的半定规划

继续类比 LP，**标准形式 SDP** 包含线性等式约束，以及对变量 $X\in\mathbf{S}^n$ 施加的矩阵非负性约束：

$$
\begin{array}{ll}
\text{最小化} & \operatorname{\mathbf{tr}}(CX)\\
\text{约束条件} & \operatorname{\mathbf{tr}}(A_iX)=b_i,\quad i=1,\ldots,p\\
& X\succeq0,
\end{array}
\tag{4.51}
$$

<!-- pdf-page: 183 -->

其中 $C,A_1,\ldots,A_p\in\mathbf{S}^n$。（回顾 $\operatorname{\mathbf{tr}}(CX)=\sum_{i,j=1}^n C_{ij}X_{ij}$，这是 $\mathbf{S}^n$ 上一般实值线性函数的形式。）可以将它与标准形式线性规划 (4.28) 作比较。在 LP 和 SDP 的标准形式中，我们都在变量满足 $p$ 个线性等式约束及一个非负性约束的条件下，最小化变量的线性函数。

与不等式形式 LP (4.29) 类似，**不等式形式 SDP** 没有等式约束，只有一个 LMI：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & x_1A_1+\cdots+x_nA_n\preceq B,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$，参数为 $B,A_1,\ldots,A_n\in\mathbf{S}^k$ 和 $c\in\mathbf{R}^n$。

#### 多个 LMI 和线性不等式

具有线性目标函数、线性等式与不等式约束，以及多个 LMI 约束的问题，即

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & F^{(i)}(x)=x_1F_1^{(i)}+\cdots+x_nF_n^{(i)}+G^{(i)}\preceq0,\quad i=1,\ldots,K\\
& Gx\preceq h,\quad Ax=b,
\end{array}
$$

通常也称为 SDP。将各个 LMI 和线性不等式组合成一个大的分块对角 LMI，就容易将这类问题转换为 SDP：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \operatorname{\mathbf{diag}}(Gx-h,F^{(1)}(x),\ldots,F^{(K)}(x))\preceq0\\
& Ax=b.
\end{array}
$$

### 4.6.3 例子

#### 二阶锥规划

SOCP (4.36) 可以表示为锥形式问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & -(A_ix+b_i,c_i^Tx+d_i)\preceq_{K_i}0,\quad i=1,\ldots,m\\
& Fx=g,
\end{array}
$$

其中

$$
K_i=\{(y,t)\in\mathbf{R}^{n_i+1}\mid\|y\|_2\leq t\},
$$

即 $\mathbf{R}^{n_i+1}$ 中的二阶锥。这说明了为什么将优化问题 (4.36) 称为二阶锥规划。

#### 矩阵范数最小化

设 $A(x)=A_0+x_1A_1+\cdots+x_nA_n$，其中 $A_i\in\mathbf{R}^{p\times q}$。考虑无约束问题

$$
\begin{array}{ll}
\text{最小化} & \|A(x)\|_2,
\end{array}
$$

<!-- pdf-page: 184 -->

其中 $\|\cdot\|_2$ 表示谱范数，即最大奇异值，变量为 $x\in\mathbf{R}^n$。这是一个凸问题，因为 $\|A(x)\|_2$ 是 $x$ 的凸函数。

利用 $\|A\|_2\leq s$ 当且仅当 $A^TA\preceq s^2I$ 且 $s\geq0$ 这一事实，可以将问题表示为

$$
\begin{array}{ll}
\text{最小化} & s\\
\text{约束条件} & A(x)^TA(x)\preceq sI,
\end{array}
$$

其中变量为 $x$ 和 $s$。由于函数 $A(x)^TA(x)-sI$ 关于 $(x,s)$ 是矩阵凸的，这就是一个只有一个 $q\times q$ 矩阵不等式约束的凸优化问题。

也可以利用一个大小为 $(p+q)\times(p+q)$ 的线性矩阵不等式来表示这个问题，所用的事实为

$$
A^TA\preceq t^2I\text{ 且 }t\geq0
\quad\Longleftrightarrow\quad
\begin{bmatrix}tI&A\\A^T&tI\end{bmatrix}\succeq0
$$

（见第 A.5.5 节）。这样得到以 $x$ 和 $t$ 为变量的 SDP

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & \begin{bmatrix}tI&A(x)\\A(x)^T&tI\end{bmatrix}\succeq0.
\end{array}
$$

#### 矩问题

设 $t$ 是 $\mathbf{R}$ 中的随机变量。期望值 $\mathbf{E}t^k$，在它们存在的前提下，称为 $t$ 的分布的**幂矩**，简称**矩**。下面的经典结果给出了矩序列的刻画。

如果 $\mathbf{R}$ 上存在一个概率分布，使得 $x_k=\mathbf{E}t^k$，$k=0,\ldots,2n$，那么 $x_0=1$，并且

$$
H(x_0,\ldots,x_{2n})=
\begin{bmatrix}
x_0&x_1&x_2&\cdots&x_{n-1}&x_n\\
x_1&x_2&x_3&\cdots&x_n&x_{n+1}\\
x_2&x_3&x_4&\cdots&x_{n+1}&x_{n+2}\\
\vdots&\vdots&\vdots&&\vdots&\vdots\\
x_{n-1}&x_n&x_{n+1}&\cdots&x_{2n-2}&x_{2n-1}\\
x_n&x_{n+1}&x_{n+2}&\cdots&x_{2n-1}&x_{2n}
\end{bmatrix}\succeq0.
\tag{4.52}
$$

矩阵 $H$ 称为与 $x_0,\ldots,x_{2n}$ 对应的 Hankel 矩阵。这个结论容易看出：设 $x_i=\mathbf{E}t^i$，$i=0,\ldots,2n$，是某个分布的矩，并令 $y=(y_0,y_1,\ldots,y_n)\in\mathbf{R}^{n+1}$，那么

$$
y^TH(x_0,\ldots,x_{2n})y=\sum_{i,j=0}^n y_i y_j\mathbf{E}t^{i+j}
=\mathbf{E}(y_0+y_1t^1+\cdots+y_nt^n)^2\geq0.
$$

下面这个部分逆命题则没有那么显然：如果 $x_0=1$ 且 $H(x)\succ0$，那么 $\mathbf{R}$ 上存在一个概率分布，使得 $x_i=\mathbf{E}t^i$，$i=0,\ldots,2n$。（证明<!-- pdf-page: 185 -->见习题 2.37。）现在假设 $x_0=1$，$H(x)\succeq0$，但可能有 $H(x)\not\succ0$，也就是说，线性矩阵不等式 (4.52) 成立，但可能不是严格不等式。在这种情况下，存在 $\mathbf{R}$ 上的一列分布，它们的矩收敛到 $x$。总之，$x_0,\ldots,x_{2n}$ 是 $\mathbf{R}$ 上某个分布的矩，或者是一列分布的矩的极限，这个条件可以表示为变量 $x$ 的线性矩阵不等式 (4.52) 加上线性等式 $x_0=1$。利用这一事实，可以将一些有意思的矩问题写成 SDP。

设 $t$ 是 $\mathbf{R}$ 上的随机变量。我们不知道它的分布，但知道它的矩的一些界，即

$$
\underline\mu_k\leq\mathbf{E}t^k\leq\bar\mu_k,\quad k=1,\ldots,2n,
$$

这也包含了某些矩的精确值已知的特殊情形。设 $p(t)=c_0+c_1t+\cdots+c_{2n}t^{2n}$ 是给定的关于 $t$ 的多项式。$p(t)$ 的期望值关于矩 $\mathbf{E}t^i$ 是线性的：

$$
\mathbf{E}p(t)=\sum_{i=0}^{2n}c_i\mathbf{E}t^i=\sum_{i=0}^{2n}c_ix_i.
$$

我们可以在所有满足给定矩界限的概率分布中，计算 $\mathbf{E}p(t)$ 的上界和下界，

$$
\begin{array}{ll}
\text{最小化（最大化）} & \mathbf{E}p(t)\\
\text{约束条件} & \underline\mu_k\leq\mathbf{E}t^k\leq\bar\mu_k,\quad k=1,\ldots,2n,
\end{array}
$$

具体做法是求解以下以 $x_1,\ldots,x_{2n}$ 为变量的 SDP：

$$
\begin{array}{ll}
\text{最小化（最大化）} & c_1x_1+\cdots+c_{2n}x_{2n}\\
\text{约束条件} & \underline\mu_k\leq x_k\leq\bar\mu_k,\quad k=1,\ldots,2n\\
& H(1,x_1,\ldots,x_{2n})\succeq0.
\end{array}
$$

这样就得到了所有满足已知矩约束的概率分布上 $\mathbf{E}p(t)$ 的界。这些界是紧的，意思是存在一列分布，它们的矩满足给定的矩界限，而且相应的 $\mathbf{E}p(t)$ 收敛到这些 SDP 所找到的上界和下界。

<div class="translator-note" markdown="1">

**译注（矩问题中的常数项）：** 由于 $x_0=1$，所列目标与 $\mathbf{E}p(t)$ 相差常数 $c_0$。省去这一常数不改变最优变量，但将半定规划的最优值用作 $\mathbf{E}p(t)$ 的数值上下界时，需要加回 $c_0$。

</div>

#### 协方差信息不完整时投资组合风险的界

再次考虑经典 Markowitz 投资组合问题的设定，见第 155 页。投资组合由 $n$ 种资产或股票组成，$x_i$ 表示在某个投资期间持有的第 $i$ 种资产的金额，$p_i$ 表示该资产在这一时期内的相对价格变动。投资组合总价值的变化为 $p^Tx$。将价格变化向量 $p$ 建模为随机向量，其均值和协方差为

$$
\bar p=\mathbf{E}p,\qquad\Sigma=\mathbf{E}(p-\bar p)(p-\bar p)^T.
$$

因此，投资组合价值的变化是一个随机变量，其均值为 $\bar p^Tx$，标准差为 $\sigma=(x^T\Sigma x)^{1/2}$。发生较大损失的风险，也就是投资组合价值变化明显低于期望值的风险，与<!-- pdf-page: 186 -->标准差 $\sigma$ 直接相关，并随之增大。因此，标准差 $\sigma$ 或方差 $\sigma^2$ 被用来衡量投资组合的风险。

在经典的投资组合优化问题中，投资组合 $x$ 是优化变量，我们在最低平均收益及其他约束下最小化风险。价格变化的统计量 $\bar p$ 和 $\Sigma$ 是已知的问题参数。这里考虑的风险界限问题则反过来：假设投资组合 $x$ 已知，但只有协方差矩阵 $\Sigma$ 的部分信息。例如，可能已知它的每个元素的上下界：

$$
L_{ij}\leq\Sigma_{ij}\leq U_{ij},\quad i,j=1,\ldots,n,
$$

其中 $L$ 和 $U$ 已知。现在要问：在所有符合给定界限的协方差矩阵中，这个投资组合的最大风险是多少？将投资组合的**最坏情形方差**定义为

$$
\sigma_{\mathrm{wc}}^2=\sup\{x^T\Sigma x\mid L_{ij}\leq\Sigma_{ij}\leq U_{ij},\ i,j=1,\ldots,n,\ \Sigma\succeq0\}.
$$

这里加上了条件 $\Sigma\succeq0$；协方差矩阵当然必须满足这个条件。

可以通过求解以下 SDP 来找到 $\sigma_{\mathrm{wc}}$：

$$
\begin{array}{ll}
\text{最大化} & x^T\Sigma x\\
\text{约束条件} & L_{ij}\leq\Sigma_{ij}\leq U_{ij},\quad i,j=1,\ldots,n\\
& \Sigma\succeq0,
\end{array}
$$

其中变量为 $\Sigma\in\mathbf{S}^n$，问题参数为 $x,L,U$。最优的 $\Sigma$ 是符合给定元素界限的最坏协方差矩阵；这里“最坏”是指对于给定的投资组合 $x$ 产生最大的风险。由 SDP 的一个最优 $\Sigma$，容易构造出一个既符合给定界限、又达到最坏情形方差的 $p$ 的分布。例如，可以取 $p=\bar p+\Sigma^{1/2}v$，其中 $v$ 是任何满足 $\mathbf{E}v=0$ 和 $\mathbf{E}vv^T=I$ 的随机向量。

显然，只要关于 $\Sigma$ 的先验信息构成凸约束，就可以用同样的方法确定 $\sigma_{\mathrm{wc}}$。下面列出一些例子。

- **某些投资组合的方差已知。** 可能存在如下等式约束：

    $$
    u_k^T\Sigma u_k=\sigma_k^2,
    $$

    其中 $u_k$ 和 $\sigma_k$ 已知。这对应于这样的先验知识：由 $u_k$ 给出的某些已知投资组合，其方差也已知，或者已经得到非常准确的估计。

- **纳入估计误差的影响。** 如果协方差 $\Sigma$ 是从观测数据中估计得到的，那么估计方法会给出估计值 $\widehat\Sigma$，以及关于估计可靠性的一些信息，例如一个置信椭球。这可以表示为

    $$
    C(\Sigma-\widehat\Sigma)\leq\alpha,
    $$

    其中 $C$ 是 $\mathbf{S}^n$ 上的正定二次型，常数 $\alpha$ 决定置信水平。

- <!-- pdf-page: 187 -->**因子模型。** 协方差可能具有形式

    $$
    \Sigma=F\Sigma_{\mathrm{factor}}F^T+D,
    $$

    其中 $F\in\mathbf{R}^{n\times k}$、$\Sigma_{\mathrm{factor}}\in\mathbf{S}^k$，$D$ 为对角矩阵。这对应于形如

    $$
    p=Fz+d
    $$

    的价格变化模型，其中 $z$ 是随机变量，表示影响价格变化的底层因子，各个 $d_i$ 相互独立，表示每种资产价格的额外波动。假设这些因子已知。由于 $\Sigma$ 与 $\Sigma_{\mathrm{factor}}$ 和 $D$ 具有线性关系，可以对它们施加任何表示先验信息的凸约束，并且仍能用凸优化计算 $\sigma_{\mathrm{wc}}$。

- **关于相关系数的信息。** 在最简单的情形中，$\Sigma$ 的对角元素，即每种资产价格的波动程度，已知；同时，价格变化之间的相关系数的界也已知：

    $$
    l_{ij}\leq\rho_{ij}=\frac{\Sigma_{ij}}{\Sigma_{ii}^{1/2}\Sigma_{jj}^{1/2}}\leq u_{ij},\quad i,j=1,\ldots,n.
    $$

    由于 $\Sigma_{ii}$ 已知，而 $i\ne j$ 时的 $\Sigma_{ij}$ 未知，所以这些都是线性不等式。

#### 图上混合最快的 Markov 链

考虑一个无向图，其节点为 $1,\ldots,n$，边集为

$$
\mathcal{E}\subseteq\{1,\ldots,n\}\times\{1,\ldots,n\}.
$$

这里，$(i,j)\in\mathcal{E}$ 表示节点 $i$ 与 $j$ 之间有一条边相连。由于图是无向的，$\mathcal{E}$ 对称：$(i,j)\in\mathcal{E}$ 当且仅当 $(j,i)\in\mathcal{E}$。我们允许自环，也就是说，可以有 $(i,i)\in\mathcal{E}$。

下面定义一个 Markov 链，它在 $t\in\mathbf{Z}_+$，即非负整数时刻的状态为 $X(t)\in\{1,\ldots,n\}$。为每条边 $(i,j)\in\mathcal{E}$ 指定一个概率 $P_{ij}$，表示 $X$ 在节点 $i$ 与 $j$ 之间转移的概率。状态只能沿边转移；当 $(i,j)\notin\mathcal{E}$ 时，有 $P_{ij}=0$。各条边对应的概率必须非负，而且对于每个节点，与该节点相连的边的概率之和必须为 1；如果存在自环，也包括该自环。

这个 Markov 链的转移概率矩阵为

$$
P_{ij}=\operatorname{\mathbf{prob}}(X(t+1)=i\mid X(t)=j),\quad i,j=1,\ldots,n.
$$

这个矩阵必须满足

$$
P_{ij}\geq0,\quad i,j=1,\ldots,n,\qquad\mathbf{1}^TP=\mathbf{1}^T,\qquad P=P^T,
\tag{4.53}
$$

以及

$$
P_{ij}=0\quad\text{当 }(i,j)\notin\mathcal{E}.
\tag{4.54}
$$

<!-- pdf-page: 188 -->

由于 $P$ 对称，且 $\mathbf{1}^TP=\mathbf{1}^T$，可知 $P\mathbf{1}=\mathbf{1}$，所以均匀分布 $(1/n)\mathbf{1}$ 是这个 Markov 链的一个平衡分布。$X(t)$ 的分布向 $(1/n)\mathbf{1}$ 的收敛，由 $P$ 的模第二大的特征值决定，即由 $r=\max\{\lambda_2,-\lambda_n\}$ 决定，其中

$$
1=\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_n
$$

是 $P$ 的特征值。我们称 $r$ 为这个 Markov 链的**混合率**。

如果 $r=1$，那么 $X(t)$ 的分布不一定收敛到 $(1/n)\mathbf{1}$，也就是说，这个 Markov 链不发生混合。当 $r<1$ 时，随着 $t\to\infty$，$X(t)$ 的分布按 $r^t$ 的渐近速率接近 $(1/n)\mathbf{1}$。因此，$r$ 越小，Markov 链的混合越快。

**最快混合 Markov 链问题**是在约束 (4.53) 和 (4.54) 下，寻找使 $r$ 最小的 $P$。问题数据是这个图，即 $\mathcal{E}$。下面将说明，这个问题可以写成 SDP。

由于特征值 $\lambda_1=1$ 对应特征向量 $\mathbf{1}$，可以将混合率表示为矩阵 $P$ 限制在子空间 $\mathbf{1}^\perp$ 上的范数：$r=\|QPQ\|_2$，其中 $Q=I-(1/n)\mathbf{1}\mathbf{1}^T$ 是向 $\mathbf{1}^\perp$ 作正交投影的矩阵。利用性质 $P\mathbf{1}=\mathbf{1}$，有

$$
\begin{aligned}
r&=\|QPQ\|_2\\
&=\|(I-(1/n)\mathbf{1}\mathbf{1}^T)P(I-(1/n)\mathbf{1}\mathbf{1}^T)\|_2\\
&=\|P-(1/n)\mathbf{1}\mathbf{1}^T\|_2.
\end{aligned}
$$

这说明混合率 $r$ 是 $P$ 的凸函数，因此最快混合 Markov 链问题可以写成凸优化问题

$$
\begin{array}{ll}
\text{最小化} & \|P-(1/n)\mathbf{1}\mathbf{1}^T\|_2\\
\text{约束条件} & P\mathbf{1}=\mathbf{1}\\
& P_{ij}\geq0,\quad i,j=1,\ldots,n\\
& P_{ij}=0\quad\text{当 }(i,j)\notin\mathcal{E},
\end{array}
$$

其中变量为 $P\in\mathbf{S}^n$。引入一个标量变量 $t$，作为 $P-(1/n)\mathbf{1}\mathbf{1}^T$ 的范数上界，就可以将问题表示为 SDP：

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & -tI\preceq P-(1/n)\mathbf{1}\mathbf{1}^T\preceq tI\\
& P\mathbf{1}=\mathbf{1}\\
& P_{ij}\geq0,\quad i,j=1,\ldots,n\\
& P_{ij}=0\quad\text{当 }(i,j)\notin\mathcal{E}.
\end{array}
\tag{4.55}
$$

## 4.7 向量优化

### 4.7.1 一般向量优化问题与凸向量优化问题

在 §4.6 中，我们扩展了标准形式问题 (4.1)，允许约束函数取向量值。本节研究目标函数取向量值<!-- pdf-page: 189 -->的含义。一般的**向量优化问题**记为

$$
\begin{array}{ll}
\text{最小化（相对于 }K\text{）} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p.
\end{array}
\tag{4.56}
$$

这里，$x\in\mathbf{R}^n$ 是优化变量，$K\subseteq\mathbf{R}^q$ 是正常锥，$f_0:\mathbf{R}^n\to\mathbf{R}^q$ 是目标函数，$f_i:\mathbf{R}^n\to\mathbf{R}$ 是不等式约束函数，$h_i:\mathbf{R}^n\to\mathbf{R}$ 是等式约束函数。这个问题与标准优化问题 (4.1) 的唯一区别是：这里的目标函数取值于 $\mathbf{R}^q$，而且问题描述中包含一个正常锥 $K$，用于比较目标值。在讨论向量优化时，标准优化问题 (4.1) 有时称为**标量优化问题**。

如果目标函数 $f_0$ 是 $K$-凸函数，不等式约束函数 $f_1,\ldots,f_m$ 是凸函数，等式约束函数 $h_1,\ldots,h_p$ 是仿射函数，就称向量优化问题 (4.56) 为**凸向量优化问题**。（与标量情形一样，等式约束通常写成 $Ax=b$，其中 $A\in\mathbf{R}^{p\times n}$。）

应该怎样理解向量优化问题 (4.56)？设 $x$ 和 $y$ 是两个可行点，即都满足约束。它们对应的目标值 $f_0(x)$ 和 $f_0(y)$ 要用广义不等式 $\preceq_K$ 来比较。我们将 $f_0(x)\preceq_K f_0(y)$ 解释为：按照目标函数 $f_0$、相对于锥 $K$ 来判断，$x$ 的目标值“优于或等于”$y$ 的目标值。向量优化中容易令人困惑的一点是，两个目标值 $f_0(x)$ 和 $f_0(y)$ 不一定能够比较：可能既没有 $f_0(x)\preceq_K f_0(y)$，也没有 $f_0(y)\preceq_K f_0(x)$，即双方都不优于另一方。在目标函数为标量的优化问题中，不会出现这种情况。

### 4.7.2 最优点与最优值

先考虑一种特殊情形，在这种情形下，向量优化问题的含义是明确的。考虑所有可行点的目标值构成的集合

$$
\mathcal{O}=\{f_0(x)\mid\exists x\in\mathcal{D},\ f_i(x)\leq0,\ i=1,\ldots,m,\ h_i(x)=0,\ i=1,\ldots,p\}\subseteq\mathbf{R}^q,
$$

称为**可达目标值集合**。如果这个集合有最小元素（见 §2.4.2），即存在一个可行点 $x$，使所有可行点 $y$ 都满足 $f_0(x)\preceq_K f_0(y)$，就称 $x$ 是问题 (4.56) 的**最优点**，并称 $f_0(x)$ 为问题的**最优值**。（如果向量优化问题存在最优值，那么最优值是唯一的。）如果 $x^\star$ 是最优点，那么它的目标值 $f_0(x^\star)$ 能够与其他每个可行点的目标值比较，而且优于或等于后者。粗略地说，在所有可行点中，$x^\star$ 是一个毫无歧义的最佳选择。

点 $x^\star$ 为最优点，当且仅当它可行，并且

$$
\mathcal{O}\subseteq f_0(x^\star)+K
\tag{4.57}
$$

<!-- pdf-page: 190 -->

（见 §2.4.2）。集合 $f_0(x^\star)+K$ 可以解释为所有劣于或等于 $f_0(x^\star)$ 的值构成的集合，因此条件 (4.57) 表示每个可达目标值都落在这个集合中。图 4.7 展示了这一点。大多数向量优化问题没有最优点和最优值，但在某些特殊情形下，它们确实存在。

<figure id="fig-4-7" data-figure="4.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-7.png" alt="可达目标值集合及其左下端的最优值，浅色区域表示劣于或等于该最优值的目标值" data-source-page="190" data-source-rect="238,121,401,267">
<figcaption>图 4.7 阴影区域表示一个向量优化问题的可达目标值集合 $\mathcal{O}$；该问题的目标值属于 $\mathbf{R}^2$，所用的锥为 $K=\mathbf{R}_+^2$。在这个例子中，标为 $f_0(x^\star)$ 的点是问题的最优值，而 $x^\star$ 是最优点。目标值 $f_0(x^\star)$ 可以与每个其他可达目标值 $f_0(y)$ 比较，并且优于或等于 $f_0(y)$。（这里，“优于或等于”是指“位于其左下方，允许落在边界上”。）浅色阴影区域是 $f_0(x^\star)+K$，即所有劣于或等于 $f_0(x^\star)$ 的目标值 $z\in\mathbf{R}^2$ 构成的集合。</figcaption>
</figure>

<div class="example" markdown="1">

**例 4.9 最佳线性无偏估计器。** 设 $y=Ax+v$，其中 $v\in\mathbf{R}^m$ 是测量噪声，$y\in\mathbf{R}^m$ 是测量值组成的向量，$x\in\mathbf{R}^n$ 是需要根据测量值 $y$ 估计的向量。假设 $A$ 的秩为 $n$，并且测量噪声满足 $\mathbf{E}v=0$、$\mathbf{E}vv^T=I$，即各个分量的均值为零，彼此不相关。

$x$ 的线性估计器具有形式 $\widehat{x}=Fy$。如果对所有 $x$ 都有 $\mathbf{E}\widehat{x}=x$，即 $FA=I$，就称这个估计器为**无偏估计器**。无偏估计器的误差协方差为

$$
\mathbf{E}(\widehat{x}-x)(\widehat{x}-x)^T=\mathbf{E}Fvv^TF^T=FF^T.
$$

我们的目标是找到一个误差协方差矩阵“较小”的无偏估计器。可以用矩阵不等式，即相对于 $\mathbf{S}_+^n$ 的不等式来比较误差协方差。这种比较具有如下含义：设 $\widehat{x}_1=F_1y$ 和 $\widehat{x}_2=F_2y$ 是两个无偏估计器。第一个估计器至少与第二个一样好，即 $F_1F_1^T\preceq F_2F_2^T$，当且仅当对所有 $c$ 都有

$$
\mathbf{E}(c^T\widehat{x}_1-c^Tx)^2\leq\mathbf{E}(c^T\widehat{x}_2-c^Tx)^2.
$$

换言之，对于 $x$ 的任意线性函数，估计器 $F_1$ 给出的估计至少与 $F_2$ 给出的估计一样好。

<!-- pdf-page: 191 -->

寻找 $x$ 的无偏估计器这一问题，可以表示为向量优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{S}_+^n\text{）} & FF^T\\
\text{约束条件} & FA=I,
\end{array}
\tag{4.58}
$$

其中变量为 $F\in\mathbf{R}^{n\times m}$。目标函数 $FF^T$ 相对于 $\mathbf{S}_+^n$ 是凸的，因此问题 (4.58) 是凸向量优化问题。要看出这一点，只需注意到：对于任意固定的 $v$，$v^TFF^Tv=\|F^Tv\|_2^2$ 都是 $F$ 的凸函数。

一个著名的结果表明，问题 (4.58) 有最优解，即最小二乘估计器，或称伪逆：

$$
F^\star=A^\dagger=(A^TA)^{-1}A^T.
$$

对于任意满足 $FA=I$ 的 $F$，都有 $FF^T\succeq F^\star F^{\star T}$。矩阵

$$
F^\star F^{\star T}=A^\dagger A^{\dagger T}=(A^TA)^{-1}
$$

就是问题 (4.58) 的最优值。

</div>

### 4.7.3 Pareto 最优点与 Pareto 最优值

现在考虑可达目标值集合没有最小元素的情形；在大多数值得研究的向量优化问题中，都是这种情形。此时，问题没有最优点或最优值，而可达目标值集合的极小元素起着重要作用。如果可行点 $x$ 的目标值 $f_0(x)$ 是可达目标值集合 $\mathcal{O}$ 的极小元素，就称 $x$ 为 **Pareto 最优点**（或称**有效点**，efficient）。此时，称 $f_0(x)$ 为向量优化问题 (4.56) 的 **Pareto 最优值**。因此，如果 $x$ 可行，并且对于任意可行点 $y$，$f_0(y)\preceq_K f_0(x)$ 都能推出 $f_0(y)=f_0(x)$，那么 $x$ 就是 Pareto 最优点。换言之，任意优于或等于 $x$ 的可行点 $y$（即满足 $f_0(y)\preceq_K f_0(x)$ 的点），其目标值都与 $x$ 完全相同。

点 $x$ 为 Pareto 最优点，当且仅当它可行，并且

$$
(f_0(x)-K)\cap\mathcal{O}=\{f_0(x)\}
\tag{4.59}
$$

（见 §2.4.2）。集合 $f_0(x)-K$ 可以解释为所有优于或等于 $f_0(x)$ 的值构成的集合，因此条件 (4.59) 表示：优于或等于 $f_0(x)$ 的可达目标值只有 $f_0(x)$ 本身。图 4.8 展示了这一点。

一个向量优化问题可以有许多 Pareto 最优值（以及 Pareto 最优点）。将 Pareto 最优值集合记为 $\mathcal{P}$，则有

$$
\mathcal{P}\subseteq\mathcal{O}\cap\operatorname{\mathbf{bd}}\mathcal{O},
$$

即每个 Pareto 最优值都是可达目标值，并且位于可达目标值集合的边界上（见习题 4.52）。

<!-- pdf-page: 192 -->

<figure id="fig-4-8" data-figure="4.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-8.png" alt="可达目标值集合的 Pareto 最优边界，以及一个 Pareto 最优值左下方的浅色区域" data-source-page="192" data-source-rect="238,123,439,267">
<figcaption>图 4.8 阴影区域表示一个向量优化问题的可达目标值集合 $\mathcal{O}$；该问题的目标值属于 $\mathbf{R}^2$，所用的锥为 $K=\mathbf{R}_+^2$。这个问题没有最优点或最优值，但存在一组 Pareto 最优点，它们对应的目标值用 $\mathcal{O}$ 左下边界上加粗的曲线表示。标为 $f_0(x^{\mathrm{po}})$ 的点是一个 Pareto 最优值，而 $x^{\mathrm{po}}$ 是一个 Pareto 最优点。浅色阴影区域是 $f_0(x^{\mathrm{po}})-K$，即所有优于或等于 $f_0(x^{\mathrm{po}})$ 的目标值 $z\in\mathbf{R}^2$ 构成的集合。</figcaption>
</figure>

### 4.7.4 标量化

**标量化**（scalarization）是寻找向量优化问题的 Pareto 最优点（或最优点）的一种标准方法，其依据是 §2.6.3 中用对偶广义不等式刻画最小点和极小点的结果。任选 $\lambda\succ_{K^*}0$，即在对偶广义不等式意义下为正的任意向量。考虑标量优化问题

$$
\begin{array}{ll}
\text{最小化} & \lambda^Tf_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{4.60}
$$

并设 $x$ 是其最优点。那么，$x$ 就是向量优化问题 (4.56) 的 Pareto 最优点。这个结论可由 §2.6.3 中利用对偶不等式对极小点的刻画得到，也容易直接证明。如果 $x$ 不是 Pareto 最优点，那么就存在可行点 $y$，满足 $f_0(y)\preceq_K f_0(x)$ 且 $f_0(x)\ne f_0(y)$。由于 $f_0(x)-f_0(y)\succeq_K0$ 且不为零，有 $\lambda^T(f_0(x)-f_0(y))>0$，即 $\lambda^Tf_0(x)>\lambda^Tf_0(y)$。这与 $x$ 是标量问题 (4.60) 的最优点这一假设矛盾。

借助标量化，可以通过求解普通的标量优化问题 (4.60)，寻找任意向量优化问题的 Pareto 最优点。向量 $\lambda$ 有时称为**权重向量**，必须满足 $\lambda\succ_{K^*}0$。权重向量是一个自由参数；改变它，就可能得到向量优化问题 (4.56) 的不同 Pareto 最优解。图 4.9 展示了这一点。图中还展示了一个无法通过标量化得到的 Pareto 最优点：无论权重向量 $\lambda\succ_{K^*}0$<!-- pdf-page: 193 -->取何值，都无法得到该点。

<figure id="fig-4-9" data-figure="4.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-9.png" alt="可达目标值集合上的三个 Pareto 最优值，其中两个可通过图示权重的标量化得到" data-source-page="193" data-source-rect="184,121,393,282">
<figcaption>图 4.9 标量化。图中显示了锥为 $K=\mathbf{R}_+^2$ 的向量优化问题的可达目标值集合 $\mathcal{O}$，以及三个 Pareto 最优值 $f_0(x_1)$、$f_0(x_2)$、$f_0(x_3)$。前两个值可以通过标量化得到：$f_0(x_1)$ 使 $\lambda_1^Tu$ 在所有 $u\in\mathcal{O}$ 上达到最小值，$f_0(x_2)$ 使 $\lambda_2^Tu$ 达到最小值，其中 $\lambda_1,\lambda_2\succ0$。值 $f_0(x_3)$ 是 Pareto 最优的，但无法通过标量化求得。</figcaption>
</figure>

标量化方法也有几何解释。点 $x$ 是标量化问题的最优点，即在可行集上使 $\lambda^Tf_0$ 最小，当且仅当所有可行点 $y$ 都满足 $\lambda^T(f_0(y)-f_0(x))\geq0$。这等价于说，$\{u\mid-\lambda^T(u-f_0(x))=0\}$ 是可达目标值集合 $\mathcal{O}$ 在点 $f_0(x)$ 处的支撑超平面；特别地，

$$
\{u\mid\lambda^T(u-f_0(x))<0\}\cap\mathcal{O}=\emptyset.
\tag{4.61}
$$

（见图 4.9。）因此，找到标量化问题的最优点时，既找到了原向量优化问题的一个 Pareto 最优点，也找到了 $\mathbf{R}^q$ 中由 (4.61) 给出的整个半空间，其中的目标值都无法达到。

#### 凸向量优化问题的标量化

现在假设向量优化问题 (4.56) 是凸的。由于 $\lambda^Tf_0$ 是标量值凸函数（由 §3.6 的结果可知），标量化问题 (4.60) 也是凸的。这意味着，可以通过求解凸标量优化问题，寻找凸向量优化问题的 Pareto 最优点。对于权重向量 $\lambda\succ_{K^*}0$ 的每种选择，都能得到一个 Pareto 最优点，而且通常会得到不同的点。

对于凸向量优化问题，还成立一个部分逆命题：对于每个 Pareto 最优点 $x^{\mathrm{po}}$，都存在某个非零的 $\lambda\succeq_{K^*}0$，使得 $x^{\mathrm{po}}$ 是标量化问题 (4.60) 的解。因此，粗略地说，对于凸问题，让权重向量 $\lambda$<!-- pdf-page: 194 -->遍历所有在 $K^*$ 意义下非负且非零的取值，标量化方法就能给出全部 Pareto 最优点。这里需要谨慎：当 $\lambda\succeq_{K^*}0$ 且 $\lambda\ne0$ 时，标量化问题的每个解并不一定都是向量问题的 Pareto 最优点。（而当 $\lambda\succ_{K^*}0$ 时，标量化问题的每个解都是 Pareto 最优点。）

在某些情形下，可以利用这个部分逆命题找到凸向量优化问题的全部 Pareto 最优点。取 $\lambda\succ_{K^*}0$ 进行标量化，可得到一组 Pareto 最优点；对于非凸向量优化问题，这一点也成立。要寻找剩余的 Pareto 最优解，必须考虑满足 $\lambda\succeq_{K^*}0$ 的非零权重向量 $\lambda$。对于每个这样的权重向量，先找出标量化问题的全部解，再从中检查哪些确实是向量优化问题的 Pareto 最优点。这些“极端”的 Pareto 最优点也可以作为正权重向量所产生的 Pareto 最优点的极限来求得。

为证明这个部分逆命题，考虑集合

$$
\mathcal{A}=\mathcal{O}+K=\{t\in\mathbf{R}^q\mid\text{存在可行点 }x\text{，使 }f_0(x)\preceq_K t\},
\tag{4.62}
$$

它包含所有在 $\preceq_K$ 意义下劣于或等于某个可达目标值的值。可达目标值集合 $\mathcal{O}$ 不一定是凸集，但如果问题是凸的，集合 $\mathcal{A}$ 就是凸集。而且，$\mathcal{A}$ 的极小元素与可达目标值集合 $\mathcal{O}$ 的极小元素完全相同，也就是 Pareto 最优值。（见习题 4.53。）现在利用 §2.6.3 的结果可知：对于 $\mathcal{A}$ 的任意极小元素，都存在某个非零的 $\lambda\succeq_{K^*}0$，使这个元素在 $\mathcal{A}$ 上使 $\lambda^Tz$ 达到最小值。这意味着，对于向量优化问题的每个 Pareto 最优点，都存在某个非零权重 $\lambda\succeq_{K^*}0$，使该点是标量化问题的最优点。

<div class="example" markdown="1">

**例 4.10 一组矩阵的极小上界。** 考虑相对于半正定锥的凸向量优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{S}_+^n\text{）} & X\\
\text{约束条件} & X\succeq A_i,\quad i=1,\ldots,m,
\end{array}
\tag{4.63}
$$

其中 $A_i\in\mathbf{S}^n$，$i=1,\ldots,m$，是给定矩阵。约束表示 $X$ 是给定矩阵 $A_1,\ldots,A_m$ 的一个上界；问题 (4.63) 的 Pareto 最优解就是这些矩阵的一个极小上界。

为寻找 Pareto 最优点，采用标量化方法：任选 $W\in\mathbf{S}_{++}^n$，构造问题

$$
\begin{array}{ll}
\text{最小化} & \operatorname{\mathbf{tr}}(WX)\\
\text{约束条件} & X\succeq A_i,\quad i=1,\ldots,m,
\end{array}
\tag{4.64}
$$

这是一个 SDP。一般来说，不同的 $W$ 会给出不同的极小解。

部分逆命题告诉我们：如果 $X$ 是向量问题 (4.63) 的 Pareto 最优点，那么存在某个非零权重矩阵 $W\succeq0$，使 $X$ 是 SDP (4.64) 的最优点。（不过在这种情形下，(4.64) 的每个解并不一定都是向量优化问题的 Pareto 最优点。）

这个问题有一个简单的几何解释。为每个 $A\in\mathbf{S}_{++}^n$ 对应一个以原点为中心的椭球

$$
\mathcal{E}_A=\{u\mid u^TA^{-1}u\leq1\},
$$

<!-- pdf-page: 195 -->

于是 $A\preceq B$ 当且仅当 $\mathcal{E}_A\subseteq\mathcal{E}_B$。问题 (4.63) 的 Pareto 最优点 $X$ 对应一个极小椭球，它包含 $A_1,\ldots,A_m$ 对应的所有椭球。图 4.10 给出了一个例子。

<figure id="fig-4-10" data-figure="4.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-10.png" alt="三个阴影椭球，以及两个分别以 X₁、X₂ 标记边界、包含这三个椭球的极小椭球" data-source-page="195" data-source-rect="193,115,383,265">
<figcaption>图 4.10 问题 (4.63) 的几何解释。三个阴影椭球对应于数据 $A_1,A_2,A_3\in\mathbf{S}_{++}^2$；Pareto 最优点对应于包含它们的极小椭球。边界分别标为 $X_1$ 和 $X_2$ 的两个椭球，是用两个不同的权重矩阵 $W_1$ 和 $W_2$ 求解半定规划（SDP）(4.64) 得到的两个极小椭球。</figcaption>
</figure>

</div>

### 4.7.5 多准则优化

当向量优化问题使用锥 $K=\mathbf{R}_+^q$ 时，称为**多准则优化问题**（multicriterion optimization problem）或**多目标优化问题**（multi-objective optimization problem）。将 $f_0$ 的各个分量记为 $F_1,\ldots,F_q$，就可以把它们解释为 $q$ 个不同的标量目标，而我们希望每个目标都尽可能小。称 $F_i$ 为问题的第 $i$ 个目标。如果 $f_1,\ldots,f_m$ 是凸函数，$h_1,\ldots,h_p$ 是仿射函数，而且各个目标 $F_1,\ldots,F_q$ 都是凸函数，那么这个多准则优化问题就是凸的。

多准则问题是向量优化问题，因此 §4.7.1–§4.7.4 的全部内容都适用。不过，对于多准则问题，可以给出更具体的解释。如果 $x$ 可行，可以把 $F_i(x)$ 看作按照第 $i$ 个目标评定的得分或取值。如果 $x$ 和 $y$ 都可行，那么 $F_i(x)\leq F_i(y)$ 表示按照第 $i$ 个目标衡量，$x$ 至少与 $y$ 一样好；$F_i(x)<F_i(y)$ 则表示按照第 $i$ 个目标衡量，$x$ 优于 $y$，或者说 $x$ 胜过 $y$。对于两个可行点 $x$ 和 $y$，如果 $F_i(x)\leq F_i(y)$，$i=1,\ldots,q$，并且至少有一个 $j$ 满足 $F_j(x)<F_j(y)$，就说 $x$ 优于 $y$，或 $x$ **支配**（dominates）$y$。粗略地说，如果 $x$ 在所有目标上都至少与 $y$ 一样好，并且在至少一个目标上胜过 $y$，那么 $x$ 就优于 $y$。

在多准则问题中，最优点 $x^\star$ 满足

$$
F_i(x^\star)\leq F_i(y),\quad i=1,\ldots,q,
$$

<!-- pdf-page: 196 -->

对每个可行点 $y$ 都成立。换言之，$x^\star$ 同时是所有标量问题

$$
\begin{array}{ll}
\text{最小化} & F_j(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
$$

的最优点，其中 $j=1,\ldots,q$。存在最优点时，称这些目标**互不竞争**，因为目标之间不需要作任何妥协：即使不考虑其他目标，每个目标也已经达到所能达到的最小值。

Pareto 最优点 $x^{\mathrm{po}}$ 满足如下性质：如果 $y$ 可行，且 $F_i(y)\leq F_i(x^{\mathrm{po}})$，$i=1,\ldots,q$，那么 $F_i(x^{\mathrm{po}})=F_i(y)$，$i=1,\ldots,q$。也就是说，一个点是 Pareto 最优点，当且仅当它可行，并且不存在更好的可行点。特别地，如果一个可行点不是 Pareto 最优点，就至少存在另一个比它更好的可行点。因此，在寻找好的点时，显然可以将搜索范围限制为 Pareto 最优点。

#### 权衡分析

设 $x$ 和 $y$ 是两个 Pareto 最优点，并且

$$
\begin{array}{ll}
F_i(x)<F_i(y), & i\in A\\
F_i(x)=F_i(y), & i\in B\\
F_i(x)>F_i(y), & i\in C,
\end{array}
$$

其中 $A\cup B\cup C=\{1,\ldots,q\}$。换言之，$A$ 是 $x$ 胜过 $y$ 的目标的下标集合，$B$ 是 $x$ 与 $y$ 持平的目标集合，$C$ 是 $y$ 胜过 $x$ 的目标集合。如果 $A$ 和 $C$ 都为空，那么 $x$ 和 $y$ 的各个目标值完全相同。否则，$A$ 和 $C$ 都必须非空。也就是说，比较两个 Pareto 最优点时，它们或者具有相同的表现（即所有目标值都相等），或者各自在至少一个目标上胜过对方。

比较点 $x$ 和 $y$ 时，可以说，$i\in A$ 的目标值较好，是以 $i\in C$ 的目标值较差为代价换来的；这就是目标之间的**权衡**。**最优权衡分析**（或简称**权衡分析**）研究的是：为了改善某些目标，必须在其他一个或多个目标上作出多大的让步；更一般地说，它研究哪些目标值组合是可以达到的。

例如，考虑一个双准则（即两个准则）问题。设 $x$ 是 Pareto 最优点，目标值为 $F_1(x)$ 和 $F_2(x)$。我们可以问：要得到一个满足 $F_1(z)\leq F_1(x)-a$ 的可行点 $z$，$F_2(z)$ 至少必须增大多少，其中 $a>0$ 是某个常数。粗略地说，这就是问：为了使第一个目标改善 $a$，必须在第二个目标上付出多大的代价。如果为了使 $F_1$ 略微减小，就必须接受 $F_2$ 大幅增加，那么就说在 Pareto 最优值 $(F_1(x),F_2(x))$ 附近，两个目标之间存在**强权衡**。反过来，如果只需使 $F_2$ 略微增加，就能使 $F_1$ 大幅减小，就说在 Pareto 最优值 $(F_1(x),F_2(x))$ 附近，两个目标之间的权衡较弱。

也可以考虑牺牲第一个目标的表现，以换取第二个目标改善的情形。此时，我们要问：对于满足 $F_1(z)\leq F_1(x)+a$ 的可行点 $z$，其中 $a>0$ 是某个常数，$F_2(z)$<!-- pdf-page: 197 -->最多能够减小多少。在这种情形下，第二个目标得到好处，即 $F_2$ 相对于 $F_2(x)$ 有所减小。如果这种好处很大，也就是说，使 $F_1$ 略微增加就能使 $F_2$ 大幅减小，就说两个目标之间存在强权衡。如果这种好处很小，就说在 Pareto 最优值 $(F_1(x),F_2(x))$ 附近，两个目标之间的权衡较弱。

#### 最优权衡曲面

多准则问题的 Pareto 最优值集合称为**最优权衡曲面**（通常指 $q>2$ 时），或**最优权衡曲线**（$q=2$ 时）。（接受一个非 Pareto 最优点显然不明智，因此可以只对 Pareto 最优点进行权衡分析。）权衡分析有时也称为**探索最优权衡曲面**。（最优权衡曲面通常是一般意义上的曲面，但并非总是如此。例如，如果问题存在最优点，那么最优权衡曲面只包含一个点，即最优值。）

最优权衡曲线很容易解释。原书第 185 页的图 4.11 给出了一个凸双准则问题的例子。从这条曲线，可以直观地看出并理解两个目标之间的权衡关系。

- 右端点表示完全不考虑 $F_1$ 时，$F_2$ 所能达到的最小值。
- 左端点表示完全不考虑 $F_2$ 时，$F_1$ 所能达到的最小值。
- 找到曲线与竖直直线 $F_1=\alpha$ 的交点，就能看出为了达到 $F_1\leq\alpha$，$F_2$ 至少必须多大。
- 找到曲线与水平直线 $F_2=\beta$ 的交点，就能看出为了达到 $F_2\leq\beta$，$F_1$ 至少必须多大。
- 最优权衡曲线在某点（即某个 Pareto 最优值）处的斜率，反映了两个目标之间的局部最优权衡关系。在斜率较陡的地方，$F_1$ 的微小变化伴随着 $F_2$ 的较大变化。
- 在曲率较大的点处，一个目标的小幅减小只能以另一个目标的大幅增加为代价实现。这就是通常所说的权衡曲线的**膝点**（knee），在许多应用中，它代表一个不错的折中解。

这些解释都容易推广到权衡曲面，不过，当目标超过三个时，曲面就很难直观展示了。

#### 多准则问题的标量化

通过构造加权和目标函数

$$
\lambda^Tf_0(x)=\sum_{i=1}^q\lambda_iF_i(x),
$$

<!-- pdf-page: 198 -->

其中 $\lambda\succ0$，来对多准则问题进行标量化时，可以把 $\lambda_i$ 解释为赋予第 $i$ 个目标的权重。权重 $\lambda_i$ 可以看作我们希望 $F_i$ 较小的程度，或不愿让 $F_i$ 较大的程度。特别地，如果希望 $F_i$ 小，就应该将 $\lambda_i$ 取大；如果不太在意 $F_i$，就可以将 $\lambda_i$ 取小。比值 $\lambda_i/\lambda_j$ 可以解释为第 $i$ 个目标相对于第 $j$ 个目标的**相对权重**或相对重要性。也可以把 $\lambda_i/\lambda_j$ 看作两个目标之间的**交换比率**，因为在加权和目标中，例如，$F_i$ 减少 $\alpha$ 所带来的变化，正好可以抵消 $F_j$ 增加 $(\lambda_i/\lambda_j)\alpha$ 所带来的变化。

这些解释使我们能够直观地判断，在探索最优权衡曲面时应该如何设置或改变权重。例如，设权重向量 $\lambda\succ0$ 给出 Pareto 最优点 $x^{\mathrm{po}}$，其目标值为 $F_1(x^{\mathrm{po}}),\ldots,F_q(x^{\mathrm{po}})$。为了寻找一个可能不同的 Pareto 最优点，使第 $k$ 个目标值改善，而其他目标值可能变差，构造新的权重向量 $\widetilde{\lambda}$，满足

$$
\widetilde{\lambda}_k>\lambda_k,\qquad\widetilde{\lambda}_j=\lambda_j,\quad j\ne k,\quad j=1,\ldots,q,
$$

即增加第 $k$ 个目标的权重。这样得到新的 Pareto 最优点 $\widetilde{x}^{\mathrm{po}}$，满足 $F_k(\widetilde{x}^{\mathrm{po}})\leq F_k(x^{\mathrm{po}})$，并且通常有 $F_k(\widetilde{x}^{\mathrm{po}})<F_k(x^{\mathrm{po}})$；也就是说，得到一个第 $k$ 个目标有所改善的 Pareto 最优点。

还可以看出，在最优权衡曲面的任意光滑点处，$\lambda$ 给出了曲面在对应 Pareto 最优值处指向内部的法向量。特别地，选定权重向量 $\lambda$ 并进行标量化后，所得到的 Pareto 最优点处，各目标之间的局部权衡关系由 $\lambda$ 给出。

实际中，人们根据上述直观认识，因地制宜地调整权重，来探索最优权衡曲面。后面第 5 章将会看到，标量化的基本思想，即先最小化各个目标的加权和，再调整权重以获得合适的解，正是对偶性的核心。

### 4.7.6 例子

#### 正则化最小二乘

给定 $A\in\mathbf{R}^{m\times n}$ 和 $b\in\mathbf{R}^m$，希望在考虑下列两个二次目标的情况下选择 $x\in\mathbf{R}^n$：

- $F_1(x)=\|Ax-b\|_2^2=x^TA^TAx-2b^TAx+b^Tb$ 衡量 $Ax$ 与 $b$ 之间的不匹配程度；
- $F_2(x)=\|x\|_2^2=x^Tx$ 衡量 $x$ 的大小。

我们的目标是找到一个既能较好拟合（即 $F_1$ 较小），自身又不太大（即 $F_2$ 较小）的 $x$。可以将其写成相对于锥 $\mathbf{R}_+^2$ 的向量优化问题，即无约束的双准则问题：

$$
\text{最小化（相对于 }\mathbf{R}_+^2\text{）}\quad f_0(x)=(F_1(x),F_2(x)).
$$

<!-- pdf-page: 199 -->

<figure id="fig-4-11" data-figure="4.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-11.png" alt="正则化最小二乘问题的可达目标值集合，其左下边界的粗线为最优权衡曲线" data-source-page="199" data-source-rect="161,121,397,309.5">
<figcaption>图 4.11 正则化最小二乘问题的最优权衡曲线。阴影集合是可达目标值 $(\|Ax-b\|_2^2,\|x\|_2^2)$ 的集合。最优权衡曲线是边界的左下部分，用较深的线条表示。</figcaption>
</figure>

取 $\lambda_1>0$ 和 $\lambda_2>0$，并最小化标量加权和目标函数，就可以对这个问题进行标量化：

$$
\begin{aligned}
\lambda^Tf_0(x)&=\lambda_1F_1(x)+\lambda_2F_2(x)\\
&=x^T(\lambda_1A^TA+\lambda_2I)x-2\lambda_1b^TAx+\lambda_1b^Tb,
\end{aligned}
$$

得到

$$
x(\mu)=(\lambda_1A^TA+\lambda_2I)^{-1}\lambda_1A^Tb=(A^TA+\mu I)^{-1}A^Tb,
$$

其中 $\mu=\lambda_2/\lambda_1$。对于任意 $\mu>0$，这个点都是双准则问题的 Pareto 最优点。可以将 $\mu=\lambda_2/\lambda_1$ 解释为赋予 $F_2$ 相对于 $F_1$ 的权重。

这个方法给出了除两个端点以外的全部 Pareto 最优点；这两个端点分别对应于 $\mu\to\infty$ 和 $\mu\to0$ 的极限。第一种情形给出 Pareto 最优解 $x=0$，也可通过取 $\lambda=(0,1)$ 进行标量化得到。另一个端点处的 Pareto 最优解是 $A^\dagger b$，其中 $A^\dagger$ 是 $A$ 的伪逆。当 $\mu\to0$，即 $\lambda\to(1,0)$ 时，标量化问题的最优解趋于这个 Pareto 最优解。（在 §6.3.2 中还会遇到正则化最小二乘问题。）

图 4.11 展示了一个正则化最小二乘问题的最优权衡曲线与可达目标值集合，其问题数据为 $A\in\mathbf{R}^{100\times10}$、$b\in\mathbf{R}^{100}$。（更多讨论见习题 4.50。）

#### 投资组合优化中的风险与收益权衡

原书第 155 页介绍的经典 Markowitz 投资组合优化问题，很自然地可以表示为双准则问题，其两个目标是平均<!-- pdf-page: 200 -->收益率的负值（因为我们希望最大化平均收益率）和收益率的方差：

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{R}_+^2\text{）} & (F_1(x),F_2(x))=(-\bar{p}^Tx,x^T\Sigma x)\\
\text{约束条件} & \mathbf{1}^Tx=1,\quad x\succeq0.
\end{array}
$$

构造相应的标量化问题时，不失一般性，可以取 $\lambda_1=1$ 和 $\lambda_2=\mu>0$：

$$
\begin{array}{ll}
\text{最小化} & -\bar{p}^Tx+\mu x^T\Sigma x\\
\text{约束条件} & \mathbf{1}^Tx=1,\quad x\succeq0,
\end{array}
$$

这是一个 QP。在这个例子中，同样能得到除 $\mu\to0$ 和 $\mu\to\infty$ 两种极限情形以外的全部 Pareto 最优投资组合。粗略地说，在第一种情形下，我们不考虑收益率的方差，而只追求最大的平均收益率；在第二种情形下，则不考虑平均收益率，而只追求最小的收益率方差。假设对 $i\ne k$ 都有 $\bar{p}_k>\bar{p}_i$，即资产 $k$ 是唯一具有最大平均收益率的资产，那么 $\mu\to0$ 时对应的投资组合配置只有 $x=e_k$。（也就是说，将整个投资组合全部投入平均收益率最高的资产。）在许多投资组合问题中，资产 $n$ 对应于一项无风险投资，其确定的收益率为 $r_{\mathrm{rf}}$。假设将 $\Sigma$ 的最后一行和最后一列（它们都为零）去掉后，得到的矩阵满秩，那么另一个端点处的 Pareto 最优投资组合就是 $x=e_n$，即将整个投资组合全部投入无风险资产。

作为具体例子，考虑一个包含 4 种资产的简单投资组合优化问题，其价格变化的均值与标准差如下表所示。

<table style="min-width:0;width:100%">
<thead><tr><th>资产</th><th>$\bar{p}_i$</th><th>$\Sigma_{ii}^{1/2}$</th></tr></thead>
<tbody>
<tr><td>1</td><td>12%</td><td>20%</td></tr>
<tr><td>2</td><td>10%</td><td>10%</td></tr>
<tr><td>3</td><td>7%</td><td>5%</td></tr>
<tr><td>4</td><td>3%</td><td>0%</td></tr>
</tbody>
</table>

资产 4 是无风险资产，具有确定的 3% 收益率。资产 3、2、1 的平均收益率依次增大，从 7% 增加到 12%；标准差也依次增大，从 5% 增加到 20%。资产之间的相关系数为 $\rho_{12}=30\%$、$\rho_{13}=-40\%$ 和 $\rho_{23}=0\%$。

图 4.12 展示了这个投资组合优化问题的最优权衡曲线。图中采用通常的画法，横轴表示标准差，即方差的平方根，纵轴表示期望收益率。下图给出了每个 Pareto 最优点对应的最优资产配置向量 $x$。

这个简单例子的结果符合我们的直觉。风险较小时，最优配置主要由无风险资产组成，再混入少量其他资产。注意，资产 3 与资产 1 负相关，将它们混合可以起到一定的对冲作用，即在给定平均收益率水平下减小方差。在权衡曲线的另一端，追求积极增长的投资组合，即平均收益率较高的投资组合，主要配置于资产 1 和资产 2；它们具有最高的平均收益率和方差。

<!-- pdf-page: 201 -->

<figure id="fig-4-12" data-figure="4.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-12.png" alt="上图为投资组合的风险与收益率权衡曲线，下图为四种资产随风险变化的最优配置比例" data-source-page="201" data-source-rect="162,189,395,548">
<figcaption>图 4.12 上：一个简单投资组合优化问题中，风险与收益率的最优权衡曲线。左端点对应于将全部资金投入无风险资产，因此收益率的标准差为零。右端点对应于将全部资金投入平均收益率最高的资产 1。下：相应的最优资产配置。</figcaption>
<p class="figure-translation">图内文字：上图纵轴 mean return：平均收益率；下图纵轴 allocation：配置比例；下图横轴 standard deviation of return：收益率的标准差。下图中的 $x(4)$、$x(3)$、$x(2)$、$x(1)$ 分别表示资产 4、3、2、1 的配置比例。</p>
</figure>

<!-- pdf-page: 202 -->

## 文献说明

自 20 世纪 40 年代以来，线性规划得到了广泛研究，许多优秀著作以它为主题，包括 Dantzig [Dan63]、Luenberger [Lue84]、Schrijver [Sch86]、Papadimitriou 和 Steiglitz [PS98]、Bertsimas 和 Tsitsiklis [BT97]、Vanderbei [Van96]，以及 Roos、Terlaky 和 Vial [RTV97] 的著作。Dantzig 和 Schrijver 还详细介绍了线性规划的历史。较近的综述可参见 Todd [Tod02]。

Schaible [Sch82, Sch83] 综述了分式规划，其中包括线性分式问题，以及凸凹分式问题等推广形式（见习题 4.7）。例 4.7 中的经济增长模型见 von Neumann [vN46]。

二次规划的研究始于 20 世纪 50 年代，例如可参见 Frank 和 Wolfe [FW56]、Markowitz [Mar56]、Hildreth [Hil57]。其部分研究动机来自原书第 155 页讨论的投资组合优化问题（Markowitz [Mar52]），以及原书第 154 页讨论的具有随机代价的 LP（见 Freund [Fre56]）。

对二阶锥规划的关注出现得较晚，始于 Nesterov 和 Nemirovski [NN94, §6.2.3]。关于 SOCP 的理论与应用的综述，可参见 Alizadeh 和 Goldfarb [AG03]、Ben-Tal 和 Nemirovski [BTN01, 第 3 讲]（其中将这类问题称为**锥二次规划**），以及 Lobo、Vandenberghe、Boyd 和 Lebret [LVBL98]。

鲁棒线性规划，以及更一般的鲁棒凸优化，起源于 Ben-Tal 和 Nemirovski [BTN98, BTN99] 及 El Ghaoui 和 Lebret [EL97] 的工作。Goldfarb 和 Iyengar [GI03a, GI03b] 讨论了鲁棒 QCQP 及其在投资组合优化中的应用。El Ghaoui、Oustry 和 Lebret [EOL98] 着重研究鲁棒半定规划。

几何规划自 20 世纪 60 年代就已为人所知。Duffin、Peterson 和 Zener [DPZ67] 以及 Zener [Zen71] 最早倡导将它用于工程设计。Peterson [Pet76] 和 Ecker [Eck80] 介绍了 20 世纪 70 年代取得的进展。这些文章和著作也包含工程应用的例子，特别是化学工程和土木工程方面的应用。Fishburn 和 Dunlop [FD85]，Sapatnekar、Rao、Vaidya 和 Kang [SRVK93]，以及 Hershenson、Boyd 和 Lee [HBL01] 将几何规划应用于集成电路设计。悬臂梁设计的例子（原书第 163 页）来自 Vanderplaats [Van84, 第 147 页]。Perron–Frobenius 特征值的变分刻画（原书第 165 页）的证明见 Berman 和 Plemmons [BP94, 第 31 页]。

Nesterov 和 Nemirovski [NN94, 第 4 章] 将锥形式问题 (4.49) 引入为非线性凸优化的一种标准问题形式。Ben-Tal 和 Nemirovski [BTN01] 进一步发展了锥规划方法，并介绍了大量应用。

Alizadeh [Ali91] 以及 Nesterov 和 Nemirovski [NN94, §6.4] 最早系统地研究半定规划，并指出它在凸优化中的广泛应用。20 世纪 90 年代后续的半定规划研究，受到组合优化（Goemans 和 Williamson [GW95]）、控制（Boyd、El Ghaoui、Feron 和 Balakrishnan [BEFB94]，Scherer、Gahinet 和 Chilali [SGC97]，Dullerud 和 Paganini [DP00]）、通信与信号处理（Luo [Luo03]，Davidson、Luo、Wong 和 Ma [DLW00, MDW+02]），以及其他工程领域应用的推动。Wolkowicz、Saigal 和 Vandenberghe 编著的书 [WSV00]，以及 Todd [Tod01]、Lewis 和 Overton [LO96]、Vandenberghe 和 Boyd [VB95] 的文章，提供了综述与广泛的参考文献。我们在原书第 170 页给出了 SDP 与矩问题之间联系的一个简单例子；Bertsimas 和 Sethuraman [BS00]、Nesterov [Nes00] 和 Lasserre [Las02] 对这种联系进行了详细研究。最快混合 Markov 链问题来自 Boyd、Diaconis 和 Xiao [BDX04]。

多准则优化与 Pareto 最优性是经济学中的基本工具；可参见 Pareto [Par71]、Debreu [Deb59] 和 Luenberger [Lue95]。例 4.9 中的结果称为 Gauss–Markov 定理（Kailath、Sayed 和 Hassibi [KSH00, 第 97 页]）。

<!-- pdf-page: 203 -->

## 习题

### 基本术语与最优性条件

**4.1** 考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x_1,x_2)\\
\text{约束条件} & 2x_1+x_2\geq1\\
& x_1+3x_2\geq1\\
& x_1\geq0,\quad x_2\geq0.
\end{array}
$$

画出可行集的示意图。对于下面每个目标函数，给出最优解集和最优值。

- (a) $f_0(x_1,x_2)=x_1+x_2$。

- (b) $f_0(x_1,x_2)=-x_1-x_2$。

- (c) $f_0(x_1,x_2)=x_1$。

- (d) $f_0(x_1,x_2)=\max\{x_1,x_2\}$。

- (e) $f_0(x_1,x_2)=x_1^2+9x_2^2$。

**4.2** 考虑优化问题

$$
\text{最小化}\quad f_0(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx),
$$

其定义域为 $\operatorname{\mathbf{dom}}f_0=\{x\mid Ax\prec b\}$，其中 $A\in\mathbf{R}^{m\times n}$，各行为 $a_i^T$。假设 $\operatorname{\mathbf{dom}}f_0$ 非空。

证明下列结论，其中包括原书第 141 页引用但未证明的结果。

- (a) $\operatorname{\mathbf{dom}}f_0$ 无界，当且仅当存在满足 $Av\preceq0$ 的非零向量 $v$。

- (b) $f_0$ 无下界，当且仅当存在 $v$，使得 $Av\preceq0$ 且 $Av\ne0$。**提示：** 存在满足 $Av\preceq0$、$Av\ne0$ 的 $v$，当且仅当不存在满足 $A^Tz=0$ 的 $z\succ0$。这可以由原书第 50 页例 2.21 中的择一定理得到。

- (c) 如果 $f_0$ 有下界，那么它的最小值可以达到，即存在满足最优性条件 (4.23) 的 $x$。

- (d) 最优解集是仿射集：$X_{\mathrm{opt}}=\{x^\star+v\mid Av=0\}$，其中 $x^\star$ 是任意一个最优点。

**4.3** 证明 $x^\star=(1,1/2,-1)$ 是优化问题

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r\\
\text{约束条件} & -1\leq x_i\leq1,\quad i=1,2,3,
\end{array}
$$

的最优点，其中

$$
P=\begin{bmatrix}13&12&-2\\12&17&6\\-2&6&12\end{bmatrix},\qquad
q=\begin{bmatrix}-22.0\\-14.5\\13.0\end{bmatrix},\qquad r=1.
$$

**4.4** [P. Parrilo] **对称性与凸优化。** 设 $\mathcal{G}=\{Q_1,\ldots,Q_k\}\subseteq\mathbf{R}^{n\times n}$ 是一个群，即对乘法和求逆封闭。如果对所有 $x$ 及 $i=1,\ldots,k$ 都有 $f(Q_ix)=f(x)$，就称函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是 **$\mathcal{G}$-不变的**，或**关于 $\mathcal{G}$ 对称**。定义 $\bar{x}=(1/k)\sum_{i=1}^kQ_ix$，即 $x$ 在其 $\mathcal{G}$-轨道上的平均值。将 $\mathcal{G}$ 的**不动子空间**定义为

$$
\mathcal{F}=\{x\mid Q_ix=x,\ i=1,\ldots,k\}.
$$

- (a) 证明：对任意 $x\in\mathbf{R}^n$，都有 $\bar{x}\in\mathcal{F}$。

- (b) <!-- pdf-page: 204 -->证明：如果 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，且是 $\mathcal{G}$-不变的，那么 $f(\bar{x})\leq f(x)$。

- (c) 对于优化问题

    $$
    \begin{array}{ll}
    \text{最小化} & f_0(x)\\
    \text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
    \end{array}
    $$

    如果目标函数 $f_0$ 是 $\mathcal{G}$-不变的，并且可行集也是 $\mathcal{G}$-不变的，就称这个问题是 $\mathcal{G}$-不变的。可行集的 $\mathcal{G}$-不变性是指

    $$
    f_1(x)\leq0,\ldots,f_m(x)\leq0\quad\Longrightarrow\quad f_1(Q_ix)\leq0,\ldots,f_m(Q_ix)\leq0,
    $$

    对 $i=1,\ldots,k$ 都成立。证明：如果问题是凸的、$\mathcal{G}$-不变的，而且存在最优点，那么在 $\mathcal{F}$ 中也存在最优点。换言之，可以不失一般性地给问题加入等式约束 $x\in\mathcal{F}$。

- (d) 作为例子，设 $f$ 是凸的且对称，即对每个置换矩阵 $P$ 都有 $f(Px)=f(x)$。证明：如果 $f$ 存在使其达到最小值的点，那么也存在形如 $\alpha\mathbf{1}$ 的点使其达到最小值。（这意味着，在 $x\in\mathbf{R}^n$ 上最小化 $f$，完全可以改为在 $t\in\mathbf{R}$ 上最小化 $f(t\mathbf{1})$。）

**4.5 等价的凸问题。** 证明下面三个凸问题等价。仔细说明如何由每个问题的解得到其他问题的解。问题数据为矩阵 $A\in\mathbf{R}^{m\times n}$（各行为 $a_i^T$）、向量 $b\in\mathbf{R}^m$ 和常数 $M>0$。

- (a) 鲁棒最小二乘问题

    $$
    \text{最小化}\quad\sum_{i=1}^m\phi(a_i^Tx-b_i),
    $$

    其中变量为 $x\in\mathbf{R}^n$，$\phi:\mathbf{R}\to\mathbf{R}$ 定义为

    $$
    \phi(u)=\begin{cases}u^2&|u|\leq M\\M(2|u|-M)&|u|>M.\end{cases}
    $$

    （这个函数称为 Huber 惩罚函数；见 §6.1.2。）

- (b) 权重可变的最小二乘问题

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{i=1}^m(a_i^Tx-b_i)^2/(w_i+1)+M^2\mathbf{1}^Tw\\
    \text{约束条件} & w\succeq0,
    \end{array}
    $$

    其中变量为 $x\in\mathbf{R}^n$ 和 $w\in\mathbf{R}^m$，定义域为 $\mathcal{D}=\{(x,w)\in\mathbf{R}^n\times\mathbf{R}^m\mid w\succ-\mathbf{1}\}$。

    **提示：** 固定 $x$，对 $w$ 进行优化，从而建立它与 (a) 中问题的关系。

    （这个问题可以解释为一个允许调整第 $i$ 个残差权重的加权最小二乘问题。当 $w_i=0$ 时，权重为 1；增大 $w_i$ 时，权重减小。目标函数的第二项惩罚较大的 $w$，即惩罚对权重进行较大的调整。）

- (c) 二次规划问题

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{i=1}^m(u_i^2+2Mv_i)\\
    \text{约束条件} & -u-v\preceq Ax-b\preceq u+v\\
    & 0\preceq u\preceq M\mathbf{1}\\
    & v\succeq0.
    \end{array}
    $$

<!-- pdf-page: 205 -->

**4.6 处理凸等式约束。** 凸优化问题只允许线性的等式约束函数。但在某些特殊情形下，也可以处理凸等式约束函数，即形如 $h(x)=0$、其中 $h$ 为凸函数的约束。本题探讨这种思路。

考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h(x)=0,
\end{array}
\tag{4.65}
$$

其中 $f_i$ 和 $h$ 都是定义域为 $\mathbf{R}^n$ 的凸函数。除非 $h$ 是仿射函数，否则这不是凸优化问题。考虑与之相关的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,\\
& h(x)\leq0,
\end{array}
\tag{4.66}
$$

其中将凸等式约束松弛为凸不等式约束。这个问题当然是凸的。

现在假设能够保证：在凸问题 (4.66) 的任意最优解 $x^\star$ 处，都有 $h(x^\star)=0$，即不等式 $h(x)\leq0$ 在解处总是有效约束。那么，就可以通过求解凸问题 (4.66) 来求解非凸问题 (4.65)。

证明：如果存在下标 $r$，使得

- $f_0$ 关于 $x_r$ 单调递增；
- $f_1,\ldots,f_m$ 关于 $x_r$ 非减；
- $h$ 关于 $x_r$ 单调递减，

上述保证就成立。

习题 4.31 和 4.58 将给出具体例子。

**4.7 凸凹分式问题。** 考虑如下形式的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)/(c^Tx+d)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
$$

其中 $f_0,f_1,\ldots,f_m$ 是凸函数，目标函数的定义域为 $\{x\in\operatorname{\mathbf{dom}}f_0\mid c^Tx+d>0\}$。

- (a) 证明这是一个拟凸优化问题。

- (b) 证明这个问题等价于

    $$
    \begin{array}{ll}
    \text{最小化} & g_0(y,t)\\
    \text{约束条件} & g_i(y,t)\leq0,\quad i=1,\ldots,m\\
    & Ay=bt\\
    & c^Ty+dt=1,
    \end{array}
    $$

    其中 $g_i$ 是 $f_i$ 的透视函数（见 §3.2.6），变量为 $y\in\mathbf{R}^n$ 和 $t\in\mathbf{R}$。证明这个问题是凸的。

- (c) 沿用类似的论证，为凸凹分式问题

    $$
    \begin{array}{ll}
    \text{最小化} & f_0(x)/h(x)\\
    \text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
    & Ax=b
    \end{array}
    $$

    <!-- pdf-page: 206 -->

    推导一个凸优化形式，其中 $f_0,f_1,\ldots,f_m$ 是凸函数，$h$ 是凹函数，目标函数的定义域为 $\{x\in\operatorname{\mathbf{dom}}f_0\cap\operatorname{\mathbf{dom}}h\mid h(x)>0\}$，并且处处有 $f_0(x)\geq0$。

    作为例子，将你的方法应用于如下无约束问题：

    $$
    f_0(x)=(\operatorname{\mathbf{tr}}F(x))/m,\qquad h(x)=(\det(F(x)))^{1/m},
    $$

    其中 $\operatorname{\mathbf{dom}}(f_0/h)=\{x\mid F(x)\succ0\}$，$F(x)=F_0+x_1F_1+\cdots+x_nF_n$，给定 $F_i\in\mathbf{S}^m$。这个问题最小化仿射矩阵函数 $F(x)$ 的特征值的算术平均与几何平均之比。

### 线性优化问题

**4.8 一些简单的 LP。** 给出下列每个 LP 的显式解。

- (a) 在仿射集上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & Ax=b.
    \end{array}
    $$

- (b) 在半空间上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & a^Tx\leq b,
    \end{array}
    $$

    其中 $a\ne0$。

- (c) 在矩形上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & l\preceq x\preceq u,
    \end{array}
    $$

    其中 $l$ 和 $u$ 满足 $l\preceq u$。

- (d) 在概率单纯形上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & \mathbf{1}^Tx=1,\quad x\succeq0.
    \end{array}
    $$

    如果将等式约束替换为不等式 $\mathbf{1}^Tx\leq1$，会怎样？

    这个 LP 可以解释为一个简单的投资组合优化问题。向量 $x$ 表示总预算在各项资产之间的配置，$x_i$ 是投入资产 $i$ 的比例。每项投资的收益率固定，等于 $-c_i$，因此希望最大化的总收益率为 $-c^Tx$。如果将预算约束 $\mathbf{1}^Tx=1$ 替换为不等式 $\mathbf{1}^Tx\leq1$，就可以选择不将一部分预算用于投资。

- (e) 在带有总预算约束的单位盒上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & \mathbf{1}^Tx=\alpha,\quad0\preceq x\preceq\mathbf{1},
    \end{array}
    $$

    其中 $\alpha$ 是 0 到 $n$ 之间的整数。如果 $\alpha$ 不是整数，但仍满足 $0\leq\alpha\leq n$，会怎样？如果将等式改为不等式 $\mathbf{1}^Tx\leq\alpha$，又会怎样？

- (f) 在带有加权预算约束的单位盒上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & d^Tx=\alpha,\quad0\preceq x\preceq\mathbf{1},
    \end{array}
    $$

    其中 $d\succ0$，且 $0\leq\alpha\leq\mathbf{1}^Td$。

<!-- pdf-page: 207 -->

**4.9 方阵 LP。** 考虑 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b,
\end{array}
$$

其中 $A$ 是非奇异方阵。证明其最优值为

$$
p^\star=\begin{cases}c^TA^{-1}b&A^{-T}c\preceq0\\-\infty&\text{其他情形。}\end{cases}
$$

**4.10 将一般 LP 转换为标准形式。** 补全 §4.3 原书第 147 页中的推导细节。详细说明标准形式 LP 与原 LP 的可行集、最优解和最优值之间的关系。

**4.11 涉及 $\ell_1$ 范数和 $\ell_\infty$ 范数的问题。** 将下列问题写成 LP。详细说明每个问题的最优解与其等价 LP 的解之间的关系。

- (a) 最小化 $\|Ax-b\|_\infty$（$\ell_\infty$ 范数逼近）。

- (b) 最小化 $\|Ax-b\|_1$（$\ell_1$ 范数逼近）。

- (c) 在 $\|x\|_\infty\leq1$ 的约束下最小化 $\|Ax-b\|_1$。

- (d) 在 $\|Ax-b\|_\infty\leq1$ 的约束下最小化 $\|x\|_1$。

- (e) 最小化 $\|Ax-b\|_1+\|x\|_\infty$。

每个问题中，$A\in\mathbf{R}^{m\times n}$ 和 $b\in\mathbf{R}^m$ 都是给定的。（更多涉及逼近和约束逼近的问题见 §6.1。）

**4.12 网络流问题。** 考虑一个包含 $n$ 个节点的网络，每对节点之间都有有向链路。问题的变量是各条链路上的流量：$x_{ij}$ 表示从节点 $i$ 到节点 $j$ 的流量。从节点 $i$ 到节点 $j$ 的链路上，流动的代价为 $c_{ij}x_{ij}$，其中 $c_{ij}$ 是给定常数。整个网络的总代价为

$$
C=\sum_{i,j=1}^n c_{ij}x_{ij}.
$$

每条链路的流量 $x_{ij}$ 还受到给定下界 $l_{ij}$（通常假设非负）和上界 $u_{ij}$ 的约束。

节点 $i$ 的外部供给为 $b_i$：$b_i>0$ 表示外部流量从节点 $i$ 进入网络，$b_i<0$ 表示有 $|b_i|$ 的流量从节点 $i$ 流出网络。假设 $\mathbf{1}^Tb=0$，即外部总供给等于外部总需求。每个节点都满足流量守恒：沿链路流入节点 $i$ 的总流量，加上外部供给，再减去沿链路流出的总流量，等于零。

问题是在上述约束下，最小化流经网络的总代价。将这个问题写成 LP。

**4.13 具有区间系数的鲁棒 LP。** 考虑变量为 $x\in\mathbf{R}^n$ 的问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b\quad\text{对所有 }A\in\mathcal{A},
\end{array}
$$

其中 $\mathcal{A}\subseteq\mathbf{R}^{m\times n}$ 为集合

$$
\mathcal{A}=\{A\in\mathbf{R}^{m\times n}\mid\bar{A}_{ij}-V_{ij}\leq A_{ij}\leq\bar{A}_{ij}+V_{ij},\ i=1,\ldots,m,\ j=1,\ldots,n\}.
$$

矩阵 $\bar{A}$ 和 $V$ 已给定。这个问题可以解释为一个 LP，其中只知道 $A$ 的每个系数位于某个区间内，并且要求 $x$ 对系数的所有可能取值都满足约束。

将这个问题表示为 LP。所构造的 LP 应该能高效求解，即其维数不应随 $n$ 或 $m$ 呈指数增长。

<!-- pdf-page: 208 -->

**4.14 在无穷范数下逼近矩阵。** 矩阵 $A\in\mathbf{R}^{m\times n}$ 由 $\ell_\infty$ 范数诱导的范数记为 $\|A\|_\infty$，定义为

$$
\|A\|_\infty=\sup_{x\ne0}\frac{\|Ax\|_\infty}{\|x\|_\infty}=\max_{i=1,\ldots,m}\sum_{j=1}^n|a_{ij}|.
$$

这个范数有时称为最大行和范数，原因显而易见（见 §A.1.5）。

考虑用其他矩阵的线性组合，在最大行和范数下逼近一个矩阵的问题。也就是说，给定 $k+1$ 个矩阵 $A_0,\ldots,A_k\in\mathbf{R}^{m\times n}$，需要寻找 $x\in\mathbf{R}^k$，使

$$
\|A_0+x_1A_1+\cdots+x_kA_k\|_\infty
$$

最小。

将这个问题表示为线性规划。解释你的 LP 中所有额外变量的含义。仔细说明这个 LP 形式如何求解原问题，例如，你的 LP 的可行集与原问题有什么关系？

**4.15 布尔 LP 的松弛。** 在布尔线性规划中，变量 $x$ 的每个分量被限制为 0 或 1：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b\\
& x_i\in\{0,1\},\quad i=1,\ldots,n.
\end{array}
\tag{4.67}
$$

一般来说，即使可行集是有限的，最多只有 $2^n$ 个点，这类问题仍然很难求解。

在称为**松弛**的一般方法中，将 $x_i$ 必须为 0 或 1 的约束替换为线性不等式 $0\leq x_i\leq1$：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b\\
& 0\leq x_i\leq1,\quad i=1,\ldots,n.
\end{array}
\tag{4.68}
$$

称这个问题为布尔 LP (4.67) 的 **LP 松弛**。LP 松弛远比原布尔 LP 容易求解。

- (a) 证明：LP 松弛 (4.68) 的最优值是布尔 LP (4.67) 最优值的下界。如果 LP 松弛不可行，可以对布尔 LP 得出什么结论？

- (b) 有时，LP 松弛恰好存在一个满足 $x_i\in\{0,1\}$ 的解。在这种情况下，可以得出什么结论？

**4.16 最少燃料最优控制。** 考虑一个线性动态系统，其状态为 $x(t)\in\mathbf{R}^n$，$t=0,\ldots,N$，执行器信号或输入信号为 $u(t)\in\mathbf{R}$，$t=0,\ldots,N-1$。系统动态由线性递推式

$$
x(t+1)=Ax(t)+bu(t),\quad t=0,\ldots,N-1,
$$

给出，其中 $A\in\mathbf{R}^{n\times n}$ 和 $b\in\mathbf{R}^n$ 已给定。假设初始状态为零，即 $x(0)=0$。

**最少燃料最优控制问题**是选择输入 $u(0),\ldots,u(N-1)$，使总燃料消耗

$$
F=\sum_{t=0}^{N-1}f(u(t)),
$$

<!-- pdf-page: 209 -->

在约束 $x(N)=x_{\mathrm{des}}$ 下最小。其中，$N$ 是给定的时间范围，$x_{\mathrm{des}}\in\mathbf{R}^n$ 是给定的期望终态或目标状态。函数 $f:\mathbf{R}\to\mathbf{R}$ 是执行器的燃料消耗映射，给出燃料用量随执行器信号幅值的变化。本题采用

$$
f(a)=\begin{cases}|a|&|a|\leq1\\2|a|-1&|a|>1.\end{cases}
$$

这意味着，当执行器信号位于 $-1$ 与 $1$ 之间时，燃料消耗与信号的绝对值成正比；对于幅值更大的执行器信号，边际燃料效率减半。

将这个最少燃料最优控制问题写成 LP。

**4.17 最优活动水平。** 考虑选择 $n$ 个非负活动水平，记为 $x_1,\ldots,x_n$。这些活动消耗 $m$ 种有限的资源。活动 $j$ 消耗资源 $i$ 的数量为 $A_{ij}x_j$，其中 $A_{ij}$ 已给定。资源消耗量可以相加，所以资源 $i$ 的总消耗为 $c_i=\sum_{j=1}^nA_{ij}x_j$。（通常有 $A_{ij}\geq0$，即活动 $j$ 消耗资源 $i$。但这里允许 $A_{ij}<0$，这意味着活动 $j$ 实际上会附带产生资源 $i$。）每种资源的消耗量都有上限：必须满足 $c_i\leq c_i^{\mathrm{max}}$，其中 $c_i^{\mathrm{max}}$ 已给定。每项活动都产生收入，收入是活动水平的分段线性凹函数：

$$
r_j(x_j)=\begin{cases}p_jx_j&0\leq x_j\leq q_j\\p_jq_j+p_j^{\mathrm{disc}}(x_j-q_j)&x_j\geq q_j.\end{cases}
$$

这里，$p_j>0$ 是活动 $j$ 所产产品的基本价格，$q_j>0$ 是数量折扣的门槛，$p_j^{\mathrm{disc}}$ 是数量折扣价格，并且 $0<p_j^{\mathrm{disc}}<p_j$。总收入是各项活动收入之和，即 $\sum_{j=1}^n r_j(x_j)$。

目标是选择活动水平，在满足资源限制的同时使总收入最大。说明如何将这个问题写成 LP。

**4.18 分离超平面与分离球面。** 给定 $\mathbf{R}^n$ 中的两个点集 $\{v^1,v^2,\ldots,v^K\}$ 和 $\{w^1,w^2,\ldots,w^L\}$。将下列两个问题写成 LP 可行性问题。

- (a) 确定一个分离这两个点集的超平面，即寻找 $a\in\mathbf{R}^n$ 和 $b\in\mathbf{R}$，满足 $a\ne0$，使得

    $$
    a^Tv^i\leq b,\quad i=1,\ldots,K,\qquad a^Tw^i\geq b,\quad i=1,\ldots,L.
    $$

    注意，这里要求 $a\ne0$，所以必须确保你的问题形式排除了平凡解 $a=0$、$b=0$。可以假设

    $$
    \operatorname{\mathbf{rank}}\begin{bmatrix}v^1&v^2&\cdots&v^K&w^1&w^2&\cdots&w^L\\1&1&\cdots&1&1&1&\cdots&1\end{bmatrix}=n+1
    $$

    （即这 $K+L$ 个点的仿射包维数为 $n$）。

- (b) 确定一个分离这两个点集的球面，即寻找 $x_c\in\mathbf{R}^n$ 和 $R\geq0$，使得

    $$
    \|v^i-x_c\|_2\leq R,\quad i=1,\ldots,K,\qquad\|w^i-x_c\|_2\geq R,\quad i=1,\ldots,L.
    $$

    （这里 $x_c$ 是球心，$R$ 是半径。）

关于分离超平面、分离球面及相关主题的更多内容，见第 8 章。

<!-- pdf-page: 210 -->

**4.19** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_1/(c^Tx+d)\\
\text{约束条件} & \|x\|_\infty\leq1,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$c\in\mathbf{R}^n$、$d\in\mathbf{R}$。假设 $d>\|c\|_1$，这保证了对所有可行点 $x$，都有 $c^Tx+d>0$。

- (a) 证明这是一个拟凸优化问题。

- (b) 证明它等价于凸优化问题

    $$
    \begin{array}{ll}
    \text{最小化} & \|Ay-bt\|_1\\
    \text{约束条件} & \|y\|_\infty\leq t\\
    & c^Ty+dt=1,
    \end{array}
    $$

    其中变量为 $y\in\mathbf{R}^n$、$t\in\mathbf{R}$。

**4.20 无线通信系统中的功率分配。** 考虑 $n$ 个发射机，功率为 $p_1,\ldots,p_n\geq0$，向 $n$ 个接收机发送信号。这些功率就是问题的优化变量。用 $G\in\mathbf{R}^{n\times n}$ 表示从发射机到接收机的路径增益矩阵；$G_{ij}\geq0$ 是发射机 $j$ 到接收机 $i$ 的路径增益。于是，接收机 $i$ 的信号功率为 $S_i=G_{ii}p_i$，干扰功率为 $I_i=\sum_{k\ne i}G_{ik}p_k$。接收机 $i$ 的**信干噪比**（signal to interference plus noise ratio，SINR），为 $S_i/(I_i+\sigma_i)$，其中 $\sigma_i>0$ 是接收机 $i$ 自身的噪声功率。问题的目标是最大化所有接收机中最小的 SINR，即最大化

$$
\min_{i=1,\ldots,n}\frac{S_i}{I_i+\sigma_i}.
$$

除了显然需要满足的 $p_i\geq0$ 以外，功率还必须满足若干约束。首先，每个发射机都有最大允许功率，即 $p_i\leq P_i^{\mathrm{max}}$，其中 $P_i^{\mathrm{max}}>0$ 已给定。此外，发射机被分成若干组，同组发射机共用一个电源，因此每组发射机的功率之和都有一个约束。更具体地说，给定 $\{1,\ldots,n\}$ 的子集 $K_1,\ldots,K_m$，满足 $K_1\cup\cdots\cup K_m=\{1,\ldots,n\}$，且当 $j\ne l$ 时，$K_j\cap K_l=0$。对于每组 $K_l$，对应发射机的总功率不能超过 $P_l^{\mathrm{gp}}>0$：

$$
\sum_{k\in K_l}p_k\leq P_l^{\mathrm{gp}},\quad l=1,\ldots,m.
$$

最后，每个接收机接收的总功率都有上限 $P_k^{\mathrm{rc}}>0$：

$$
\sum_{k=1}^nG_{ik}p_k\leq P_i^{\mathrm{rc}},\quad i=1,\ldots,n.
$$

这个约束反映了接收总功率过大会使接收机饱和的事实。

将这个 SINR 最大化问题写成广义线性分式规划。

### 二次优化问题

**4.21 一些简单的 QCQP。** 给出下列每个 QCQP 的显式解。

- (a) 在以原点为中心的椭球上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & x^TAx\leq1,
    \end{array}
    $$

    其中 $A\in\mathbf{S}_{++}^n$ 且 $c\ne0$。如果问题不是凸的，即 $A\notin\mathbf{S}_+^n$，解是什么？

- (b) <!-- pdf-page: 211 -->在椭球上最小化线性函数。

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & (x-x_c)^TA(x-x_c)\leq1,
    \end{array}
    $$

    其中 $A\in\mathbf{S}_{++}^n$ 且 $c\ne0$。

- (c) 在以原点为中心的椭球上最小化二次型。

    $$
    \begin{array}{ll}
    \text{最小化} & x^TBx\\
    \text{约束条件} & x^TAx\leq1,
    \end{array}
    $$

    其中 $A\in\mathbf{S}_{++}^n$，$B\in\mathbf{S}_+^n$。再考虑 $B\notin\mathbf{S}_+^n$ 的非凸推广。（见 §B.1。）

**4.22** 考虑 QCQP

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r\\
\text{约束条件} & x^Tx\leq1,
\end{array}
$$

其中 $P\in\mathbf{S}_{++}^n$。证明 $x^\star=-(P+\lambda I)^{-1}q$，其中 $\lambda=\max\{0,\bar{\lambda}\}$，$\bar{\lambda}$ 是非线性方程

$$
q^T(P+\lambda I)^{-2}q=1
$$

的最大解。

<div class="translator-note" markdown="1">

**译注（习题 4.22）：** 当 $q=0$ 时，用于定义 $\bar\lambda$ 的方程没有解。这一退化情形应单独处理：取 $\lambda=0$，最优点为 $x^\star=0$。

</div>

**4.23 用 QCQP 求解 $\ell_4$ 范数逼近。** 将 $\ell_4$ 范数逼近问题

$$
\text{最小化}\quad\|Ax-b\|_4=\left(\sum_{i=1}^m(a_i^Tx-b_i)^4\right)^{1/4}
$$

写成 QCQP。矩阵 $A\in\mathbf{R}^{m\times n}$（各行为 $a_i^T$）和向量 $b\in\mathbf{R}^m$ 已给定。

**4.24 复数 $\ell_1$、$\ell_2$ 和 $\ell_\infty$ 范数逼近。** 考虑问题

$$
\text{最小化}\quad\|Ax-b\|_p,
$$

其中 $A\in\mathbf{C}^{m\times n}$、$b\in\mathbf{C}^m$，变量为 $x\in\mathbf{C}^n$。当 $p\geq1$ 时，复数 $\ell_p$ 范数定义为

$$
\|y\|_p=\left(\sum_{i=1}^m|y_i|^p\right)^{1/p},
$$

而 $\|y\|_\infty=\max_{i=1,\ldots,m}|y_i|$。对于 $p=1,2,\infty$，将复数 $\ell_p$ 范数逼近问题表示为变量和数据均为实数的 QCQP 或 SOCP。

**4.25 两组椭球的线性分离。** 给定 $K+L$ 个椭球

$$
\mathcal{E}_i=\{P_iu+q_i\mid\|u\|_2\leq1\},\quad i=1,\ldots,K+L,
$$

其中 $P_i\in\mathbf{S}^n$。希望找到一个将 $\mathcal{E}_1,\ldots,\mathcal{E}_K$ 与 $\mathcal{E}_{K+1},\ldots,\mathcal{E}_{K+L}$ 严格分离的超平面，即计算 $a\in\mathbf{R}^n$、$b\in\mathbf{R}$，使得

$$
a^Tx+b>0\quad\text{对 }x\in\mathcal{E}_1\cup\cdots\cup\mathcal{E}_K,\qquad
a^Tx+b<0\quad\text{对 }x\in\mathcal{E}_{K+1}\cup\cdots\cup\mathcal{E}_{K+L},
$$

或者证明这样的超平面不存在。将这个问题表示为 SOCP 可行性问题。

**4.26 将双曲约束表示为二阶锥约束。** 验证：$x\in\mathbf{R}^n$、$y,z\in\mathbf{R}$ 满足

$$
x^Tx\leq yz,\qquad y\geq0,\qquad z\geq0
$$

当且仅当

$$
\left\|\begin{bmatrix}2x\\y-z\end{bmatrix}\right\|_2\leq y+z,\qquad y\geq0,\qquad z\geq0.
$$

利用这一观察，将下列问题写成 SOCP。

- (a) <!-- pdf-page: 212 -->最大化调和平均。

    $$
    \text{最大化}\quad\left(\sum_{i=1}^m1/(a_i^Tx-b_i)\right)^{-1},
    $$

    定义域为 $\{x\mid Ax\succ b\}$，其中 $a_i^T$ 是 $A$ 的第 $i$ 行。

- (b) 最大化几何平均。

    $$
    \text{最大化}\quad\left(\prod_{i=1}^m(a_i^Tx-b_i)\right)^{1/m},
    $$

    定义域为 $\{x\mid Ax\succeq b\}$，其中 $a_i^T$ 是 $A$ 的第 $i$ 行。

**4.27 用 SOCP 求解矩阵分式最小化问题。** 将下面的问题表示为一个 SOCP：

$$
\begin{array}{ll}
\text{最小化} & (Ax+b)^T(I+B\operatorname{\mathbf{diag}}(x)B^T)^{-1}(Ax+b)\\
\text{约束条件} & x\succeq0,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$B\in\mathbf{R}^{m\times n}$。变量为 $x\in\mathbf{R}^n$。

**提示：** 先证明该问题等价于

$$
\begin{array}{ll}
\text{最小化} & v^Tv+w^T\operatorname{\mathbf{diag}}(x)^{-1}w\\
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

- (b) 由标称值 $P_0\in\mathbf{S}_+^n$ 和偏差 $P-P_0$ 的特征值界给出的集合：

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
\text{最大化} & \operatorname{\mathbf{prob}}(c^Tx\geq\alpha)\\
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

<div class="translator-note" markdown="1">

**译注（习题 4.37）：** 按前面给定的 $\phi$ 展开复合函数，$h$ 的末项应为 $3f_2^3$。

</div>

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

### 半定规划与锥形式问题

**4.38 只有一个变量的 LMI 与 SDP。** 矩阵对 $(A,B)$（其中 $A,B\in\mathbf{S}^n$）的**广义特征值**定义为多项式 $\det(\lambda B-A)$ 的根（见 §A.5.3）。假设 $B$ 非奇异，而且 $A$、$B$ 可以通过合同变换同时对角化，即存在非奇异矩阵 $R\in\mathbf{R}^{n\times n}$，使得

$$
R^TAR=\operatorname{\mathbf{diag}}(a),\qquad R^TBR=\operatorname{\mathbf{diag}}(b),
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

**4.41 共正矩阵与 $P_0$ 矩阵的 LMI 检验。** 如果矩阵 $A\in\mathbf{S}^n$ 对所有 $x\succeq0$ 都满足 $x^TAx\geq0$，就称 $A$ 是共正矩阵（见习题 2.35）。如果矩阵 $A\in\mathbf{R}^{n\times n}$ 对所有 $x$ 都满足 $\max_{i=1,\ldots,n}x_i(Ax)_i\geq0$，就称 $A$ 是 $P_0$ 矩阵。一般来说，检验一个矩阵是否为共正矩阵或 $P_0$ 矩阵非常困难。不过，存在一些有用的充分条件，可以通过半定规划加以检验。

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
\operatorname{\mathbf{dom}}f_0=\{x\mid Fx+g\succ_K0\},
$$

定义的函数 $f_0:\mathbf{R}^n\to\mathbf{R}^m$ 是拟凸的，其中 $C,F\in\mathbf{R}^{m\times n}$，$d,g\in\mathbf{R}^m$。

以这种形式的函数为目标的拟凸优化问题称为**广义分式规划**（generalized fractional program）。将第 152 页的广义线性分式规划，以及广义特征值最小化问题 (4.73)，表示为广义分式规划。

<div class="translator-note" markdown="1">

**译注（习题 4.49）：** $K$ 是 $\mathbf{R}^m$ 中的集合，应写作 $K\subseteq\mathbf{R}^m$。这里的 $f_0$ 是关于标量 $t$ 的下确界，取标量值；相应的映射应写作 $f_0:\mathbf{R}^n\to\mathbf{R}$。

</div>

### 向量优化与多准则优化

**4.50 双准则优化。** 图 4.11 给出了双准则优化问题

$$
\text{最小化（关于 }\mathbf{R}_+^2\text{）}\quad
\bigl(\|Ax-b\|^2,\|x\|_2^2\bigr),
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

**4.51 向量优化中目标函数的单调变换。** 考虑向量优化问题 (4.56)。假设把目标函数 $f_0$ 替换为 $\phi\circ f_0$，得到一个新的向量优化问题，其中 $\phi:\mathbf{R}^q\to\mathbf{R}^q$ 满足

$$
u\preceq_K v,\quad u\ne v
\quad\Longrightarrow\quad
\phi(u)\preceq_K\phi(v),\quad\phi(u)\ne\phi(v).
$$

证明：点 $x$ 是其中一个问题的 Pareto 最优点（或最优点），当且仅当它是另一个问题的 Pareto 最优点（或最优点），因此这两个问题等价。特别地，将多准则问题的每个目标分别与一个递增函数复合，不会改变 Pareto 最优点。

<div class="translator-note" markdown="1">

**译注（习题 4.51）：** 对于一般向量映射，题设的保序条件不足以保证双向等价；可补充条件 $\phi(u)\preceq_K\phi(v)\Longrightarrow u\preceq_K v$。逐个目标分别复合严格递增函数的特例满足这一要求。

</div>

**4.52 Pareto 最优点与可达值集合的边界。** 考虑一个锥为 $K$ 的向量优化问题。用 $\mathcal{P}$ 表示 Pareto 最优值的集合，用 $\mathcal{O}$ 表示可达目标值的集合。证明 $\mathcal{P}\subseteq\mathcal{O}\cap\operatorname{\mathbf{bd}}\mathcal{O}$，即每个 Pareto 最优值都是一个可达目标值，而且位于可达目标值集合的边界上。

**4.53** 假设向量优化问题 (4.56) 是凸的。证明集合

$$
\mathcal{A}=\mathcal{O}+K
=\{t\in\mathbf{R}^q\mid f_0(x)\preceq_K t\text{ 对某个可行点 }x\text{ 成立}\},
$$

是凸集。再证明：$\mathcal{A}$ 的极小元素与 $\mathcal{O}$ 的极小点相同。

**4.54 标量化与最优点。** 假设一个向量优化问题（不一定是凸问题）有最优点 $x^\star$。证明：无论如何选择 $\lambda\succ_{K^*}0$，$x^\star$ 都是相应标量化问题的一个解。再证明其逆命题：如果一个点 $x$ 对任意选择的 $\lambda\succ_{K^*}0$ 都是标量化问题的解，那么它就是这个向量优化问题（不一定是凸问题）的最优点。

**4.55 加权和标量化的推广。** 在 §4.7.4 中，我们说明了如何把向量目标 $f_0:\mathbf{R}^n\to\mathbf{R}^q$ 替换为标量目标 $\lambda^Tf_0$（其中 $\lambda\succ_{K^*}0$），从而得到向量优化问题的 Pareto 最优解。设 $\psi:\mathbf{R}^q\to\mathbf{R}$ 是一个 $K$-递增函数，即满足

$$
u\preceq_K v,\quad u\ne v
\quad\Longrightarrow\quad\psi(u)<\psi(v).
$$

证明，问题

$$
\begin{array}{ll}
\text{最小化} & \psi(f_0(x))\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p
\end{array}
$$

<!-- pdf-page: 221 -->

的任意解，都是向量优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }K\text{）} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p
\end{array}
$$

的 Pareto 最优点。注意，$\psi(u)=\lambda^Tu$（其中 $\lambda\succ_{K^*}0$）是一个特例。

作为一个相关的例子，证明：在多准则优化问题中（即 $f_0=F:\mathbf{R}^n\to\mathbf{R}^q$、$K=\mathbf{R}_+^q$ 的向量优化问题），标量优化问题

$$
\begin{array}{ll}
\text{最小化} & \max_{i=1,\ldots,q}F_i(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
$$

的唯一解是 Pareto 最优点。

### 其他问题

**4.56** [P. Parrilo] 考虑在一些凸集之并的凸包 $\operatorname{\mathbf{conv}}\left(\bigcup_{i=1}^q C_i\right)$ 上，最小化凸函数 $f_0:\mathbf{R}^n\to\mathbf{R}$ 的问题。这些集合由凸不等式描述：

$$
C_i=\{x\mid f_{ij}(x)\leq0,\ j=1,\ldots,k_i\},
$$

其中 $f_{ij}:\mathbf{R}^n\to\mathbf{R}$ 是凸函数。我们的目标是把这个问题表述为凸优化问题。

一个直观的办法是引入变量 $x_1,\ldots,x_q\in\mathbf{R}^n$，并要求 $x_i\in C_i$；引入 $\theta\in\mathbf{R}^q$，并要求 $\theta\succeq0$、$\mathbf{1}^T\theta=1$；再引入变量 $x\in\mathbf{R}^n$，并要求 $x=\theta_1x_1+\cdots+\theta_qx_q$。这个等式约束不是变量的仿射函数，因此这种办法不能得到凸问题。

一种更巧妙的表述是

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & s_if_{ij}(z_i/s_i)\leq0,\quad i=1,\ldots,q,\quad j=1,\ldots,k_i\\
& \mathbf{1}^Ts=1,\quad s\succeq0\\
& x=z_1+\cdots+z_q,
\end{array}
$$

变量为 $z_1,\ldots,z_q\in\mathbf{R}^n$、$x\in\mathbf{R}^n$ 和 $s_1,\ldots,s_q\in\mathbf{R}$。（当 $s_i=0$ 时，若 $z_i=0$，则把 $s_if_{ij}(z_i/s_i)$ 取为 $0$；若 $z_i\ne0$，则取为 $\infty$。）解释为什么这个问题是凸的，并且与原问题等价。

**4.57 通信信道的容量。** 考虑一个通信信道，在 $t=1,2,\ldots$（例如以秒为单位）时，输入为 $X(t)\in\{1,\ldots,n\}$，输出为 $Y(t)\in\{1,\ldots,m\}$。输入与输出之间的关系由统计规律给出：

$$
p_{ij}=\operatorname{\mathbf{prob}}(Y(t)=i\mid X(t)=j),
\quad i=1,\ldots,m,\quad j=1,\ldots,n.
$$

矩阵 $P\in\mathbf{R}^{m\times n}$ 称为**信道转移矩阵**（channel transition matrix），这种信道称为**离散无记忆信道**（discrete memoryless channel）。

Shannon 的一个著名结果指出：只要信息传输速率小于某个数 $C$，就能通过该通信信道传递信息，并使出错概率任意小。$C$ 称为**信道容量**（channel capacity），单位为比特／秒。Shannon 还证明，离散无记忆信道的容量可以通过求解一个优化问题得到。假设 $X$ 的概率分布记作 $x\in\mathbf{R}^n$，即

$$
x_j=\operatorname{\mathbf{prob}}(X=j),\quad j=1,\ldots,n.
$$

<!-- pdf-page: 222 -->

$X$ 与 $Y$ 之间的**互信息**（mutual information）为

$$
I(X;Y)=\sum_{i=1}^m\sum_{j=1}^n x_jp_{ij}\log_2\frac{p_{ij}}{\sum_{k=1}^n x_kp_{ik}}.
$$

于是信道容量 $C$ 为

$$
C=\sup_x I(X;Y),
$$

其中上确界取遍输入 $X$ 的所有可能概率分布，也就是所有满足 $x\succeq0$、$\mathbf{1}^Tx=1$ 的 $x$。

说明如何用凸优化计算信道容量。

**提示：** 引入变量 $y=Px$，它给出输出 $Y$ 的概率分布；证明互信息可以写成

$$
I(X;Y)=c^Tx-\sum_{i=1}^m y_i\log_2 y_i,
$$

其中 $c_j=\sum_{i=1}^m p_{ij}\log_2 p_{ij}$，$j=1,\ldots,n$。

**4.58 最优消费。** 本题考虑如何在一段时间内，以最优方式消费（或花掉）一笔初始金额（或其他资产）$k_0$。变量为 $c_0,\ldots,c_T$，其中 $c_t\geq0$ 表示第 $t$ 期的消费量。消费量为 $c$ 时获得的效用为 $u(c)$，其中 $u:\mathbf{R}\to\mathbf{R}$ 是一个递增凹函数。消费带来的效用的现值为

$$
U=\sum_{t=0}^T\beta^t u(c_t),
$$

其中 $0<\beta<1$ 是折现因子。

用 $k_t$ 表示第 $t$ 期可用于投资的金额。假设这笔投资获得的收益为 $f(k_t)$，其中 $f:\mathbf{R}\to\mathbf{R}$ 是一个递增的凹投资收益函数，满足 $f(0)=0$。例如，如果资金每期按 $R\%$ 的利率获取单利，则 $f(a)=(R/100)a$。要消费的金额 $c_t$ 在期末取出，因此有递推关系

$$
k_{t+1}=k_t+f(k_t)-c_t,\quad t=0,\ldots,T.
$$

初始金额 $k_0>0$ 是给定的。我们要求 $k_t\geq0$，$t=1,\ldots,T+1$（不过，也可以考虑允许 $k_t<0$ 的更复杂模型）。

说明如何把最大化 $U$ 的问题表述为凸优化问题。解释你所建立的问题如何与本问题等价，以及二者之间的确切关系。

**提示：** 证明，可以把上述关于 $k_t$ 的递推关系替换为不等式

$$
k_{t+1}\leq k_t+f(k_t)-c_t,\quad t=0,\ldots,T.
$$

（解释：这些不等式允许你在每期扔掉一部分钱。）这种技巧的更一般形式见习题 4.6。

**4.59 鲁棒优化。** 在一些优化问题中，由于某些参数或因素无法控制或尚不清楚，目标函数和约束函数存在不确定性或变化。可以把目标函数和约束函数 $f_0,\ldots,f_m$ 写成优化变量 $x\in\mathbf{R}^n$ 与参数向量 $u\in\mathbf{R}^k$ 的函数，以此建立模型，其中 $u$ 的值未知，或者会发生变化。在随机优化<!-- pdf-page: 223 -->方法中，将参数向量 $u$ 建模为具有已知分布的随机变量，并使用期望值 $\mathbf{E}_u f_i(x,u)$。在最坏情况分析方法中，给定一个集合 $\mathcal{U}$，并且知道 $u$ 属于这个集合；此时使用最大值或最坏情况值 $\sup_{u\in\mathcal{U}}f_i(x,u)$。为简化讨论，假设没有等式约束。

- (a) **随机优化。** 考虑问题

    $$
    \begin{array}{ll}
    \text{最小化} & \mathbf{E}f_0(x,u)\\
    \text{约束条件} & \mathbf{E}f_i(x,u)\leq0,\quad i=1,\ldots,m,
    \end{array}
    $$

    其中期望是对 $u$ 取的。证明：如果对每个 $u$，$f_i$ 都是关于 $x$ 的凸函数，那么这个随机优化问题是凸的。

- (b) **最坏情况优化。** 考虑问题

    $$
    \begin{array}{ll}
    \text{最小化} & \sup_{u\in\mathcal{U}}f_0(x,u)\\
    \text{约束条件} & \sup_{u\in\mathcal{U}}f_i(x,u)\leq0,\quad i=1,\ldots,m.
    \end{array}
    $$

    证明：如果对每个 $u$，$f_i$ 都是关于 $x$ 的凸函数，那么这个最坏情况优化问题是凸的。

- (c) **参数可能取值构成有限集合。** 当期望值 $\mathbf{E}f_i(x,u)$ 或最坏情况值 $\sup_{u\in\mathcal{U}}f_i(x,u)$ 有解析表达式，或有容易求值的表达式时，(a) 与 (b) 的结论最有用。

    假设参数的可能取值构成有限集合，即 $u\in\{u_1,\ldots,u_N\}$。对于随机情形，还给定了每个取值的概率：$\operatorname{\mathbf{prob}}(u=u_i)=p_i$，其中 $p\in\mathbf{R}^N$、$p\succeq0$、$\mathbf{1}^Tp=1$。在最坏情况表述中，只需取 $\mathcal{U}\in\{u_1,\ldots,u_N\}$。

    说明如何显式建立最坏情况优化问题和随机优化问题（即给出 $\sup_{u\in\mathcal{U}}f_i$ 与 $\mathbf{E}_u f_i$ 的显式表达式）。

<div class="translator-note" markdown="1">

**译注（习题 4.59(c)）：** $\mathcal{U}$ 是参数的不确定集合。按本题上下文，这里应取 $\mathcal{U}=\{u_1,\ldots,u_N\}$；原式的 $\in$ 应为 $=$。

</div>

**4.60 对数最优投资策略。** 考虑一个在 $N$ 个期间内持有 $n$ 种资产的投资组合问题。在每期期初，我们把全部财富重新投资，按照一个固定不变的配置策略 $x\in\mathbf{R}^n$，将其重新分配到这 $n$ 种资产上，其中 $x\succeq0$、$\mathbf{1}^Tx=1$。换句话说，如果 $W(t-1)$ 是第 $t$ 期期初的财富，那么在第 $t$ 期，投入资产 $i$ 的金额为 $x_iW(t-1)$。用 $\lambda(t)$ 表示第 $t$ 期的总回报，即 $\lambda(t)=W(t)/W(t-1)$。经过 $N$ 期后，财富变为原来的 $\prod_{t=1}^N\lambda(t)$ 倍。我们把

$$
\frac{1}{N}\sum_{t=1}^N\log\lambda(t)
$$

称为这 $N$ 期内投资的**增长率**。我们希望确定一个配置策略 $x$，使 $N$ 很大时的总财富增长最大。

用一个离散随机模型来描述回报的不确定性。假设每期有 $m$ 种可能的情景，其概率为 $\pi_j$，$j=1,\ldots,m$。在情景 $j$ 下，资产 $i$ 一期的回报为 $p_{ij}$。因此，投资组合在第 $t$ 期的回报 $\lambda(t)$ 是一个随机变量，有 $m$ 个可能取值 $p_1^Tx,\ldots,p_m^Tx$，其分布为

$$
\pi_j=\operatorname{\mathbf{prob}}(\lambda(t)=p_j^Tx),\quad j=1,\ldots,m.
$$

假设每期的可能情景相同，各期的情景取值相互独立且服从相同分布。根据大数定律，有

$$
\lim_{N\to\infty}\frac{1}{N}\log\left(\frac{W(N)}{W(0)}\right)
=\lim_{N\to\infty}\frac{1}{N}\sum_{t=1}^N\log\lambda(t)
=\mathbf{E}\log\lambda(t)
=\sum_{j=1}^m\pi_j\log(p_j^Tx).
$$

<!-- pdf-page: 224 -->

换句话说，采用投资策略 $x$ 时，长期增长率为

$$
R_{\mathrm{lt}}=\sum_{j=1}^m\pi_j\log(p_j^Tx).
$$

使这个量最大的投资策略 $x$，称为**对数最优投资策略**（log-optimal investment strategy）。它可以通过求解优化问题

$$
\begin{array}{ll}
\text{最大化} & \sum_{j=1}^m\pi_j\log(p_j^Tx)\\
\text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

得到，其中变量为 $x\in\mathbf{R}^n$。

证明这是一个凸优化问题。

**4.61 使用 logistic 模型的优化。** 随机变量 $X\in\{0,1\}$ 满足

$$
\operatorname{\mathbf{prob}}(X=1)=p=\frac{\exp(a^Tx+b)}{1+\exp(a^Tx+b)},
$$

其中 $x\in\mathbf{R}^n$ 是影响该概率的变量向量，$a$ 和 $b$ 是已知参数。可以把 $X=1$ 理解为消费者购买某件产品这一事件，把 $x$ 理解为影响购买概率的变量向量，例如广告投入、零售价格、折扣价格、包装费用以及其他因素。需要优化的变量 $x$ 受到一组线性约束 $Fx\preceq g$ 的限制。

把下列问题表述为凸优化问题。

- (a) **最大化购买概率。** 目标是选择 $x$，使 $p$ 最大。
- (b) **最大化期望利润。** 设 $c^Tx+d$ 为售出该产品所得的利润，并假设它对所有可行的 $x$ 都为正。目标是最大化期望利润 $p(c^Tx+d)$。

**4.62 高斯广播信道中的最优功率与带宽分配。** 考虑一个由中心节点向 $n$ 个接收端发送消息的通信系统。（“高斯”指干扰传输的噪声类型。）每个接收端的信道由其（发射）功率 $P_i\geq0$ 和带宽 $W_i\geq0$ 描述。接收端信道的功率与带宽，按下式决定其比特率 $R_i$（即信息可以传送的速率）：

$$
R_i=\alpha_iW_i\log(1+\beta_iP_i/W_i),
$$

其中 $\alpha_i$ 和 $\beta_i$ 是已知的正常数。当 $W_i=0$ 时，取 $R_i=0$（这也就是令 $W_i\to0$ 时得到的极限）。

各功率必须满足总功率约束，其形式为

$$
P_1+\cdots+P_n=P_{\mathrm{tot}},
$$

其中 $P_{\mathrm{tot}}>0$ 是给定的、可分配给各信道的总功率。类似地，各带宽必须满足

$$
W_1+\cdots+W_n=W_{\mathrm{tot}},
$$

其中 $W_{\mathrm{tot}}>0$ 是给定的可用总带宽。本题中的优化变量为各功率与带宽，即 $P_1,\ldots,P_n,W_1,\ldots,W_n$。

目标是最大化总效用

$$
\sum_{i=1}^n u_i(R_i),
$$

<!-- pdf-page: 225 -->

其中 $u_i:\mathbf{R}\to\mathbf{R}$ 是第 $i$ 个接收端对应的效用函数。（可以把 $u_i(R_i)$ 理解为向接收端 $i$ 提供比特率 $R_i$ 所获得的收入，因此目标就是最大化总收入。）可以假设效用函数 $u_i$ 非递减且为凹函数。

将这个问题表述为凸优化问题。

**4.63 制造成本与成品率的最优权衡。** 向量 $x\in\mathbf{R}^n$ 表示制造过程中的标称参数。过程的成品率，即制成品中合格产品所占的比例，为 $Y(x)$。假设 $Y$ 是对数凹函数（实际中经常如此；见例 3.43）。生产单位产品的成本为 $c^Tx$，其中 $c\in\mathbf{R}^n$。每件合格产品的成本为 $c^Tx/Y(x)$。我们希望在 $x$ 满足某些凸约束（例如线性不等式 $Ax\preceq b$）的条件下，最小化 $c^Tx/Y(x)$。（可以假设在可行集上有 $c^Tx>0$ 且 $Y(x)>0$。）

这个问题既不是凸优化问题，也不是拟凸优化问题，但可以结合凸优化和一维搜索来求解。下面给出基本思路，你需要补全所有细节和论证。

- (a) 证明函数 $f:\mathbf{R}\to\mathbf{R}$

    $$
    f(a)=\sup\{Y(x)\mid Ax\preceq b,\ c^Tx=a\},
    $$

    是对数凹函数；它给出成本为 $a$ 时能够达到的最大成品率。这意味着，通过求解一个以 $x$ 为变量的凸优化问题，就可以计算函数 $f$ 的值。

- (b) 假设在足够多个 $a$ 值处计算了 $f$，从而在所关心的范围内得到了较好的近似。说明如何用这些数据，近似求解使每件合格产品的成本最小的问题。

**4.64 带补救决策的优化。** 在带补救决策的优化问题（optimization with recourse）中，也称为**两阶段优化**（two-stage optimization），代价函数和约束不仅取决于所选择的变量，还取决于一个离散随机变量 $s\in\{1,\ldots,S\}$；它表示 $S$ 种情景中发生了哪一种。情景随机变量 $s$ 的概率分布 $\pi$ 已知，其中 $\pi_i=\operatorname{\mathbf{prob}}(s=i)$，$i=1,\ldots,S$。

在两阶段优化中，需要选择两个变量 $x\in\mathbf{R}^n$ 和 $z\in\mathbf{R}^q$ 的值。变量 $x$ 必须在得知具体情景 $s$ 之前选定；变量 $z$ 则在得知情景随机变量的值之后选择。换句话说，$z$ 是情景随机变量 $s$ 的函数。为了描述对 $z$ 的选择，我们列出在各个情景下会选择的值，即列出向量

$$
z_1,\ldots,z_S\in\mathbf{R}^q.
$$

这里，$z_3$ 是 $s=3$ 发生时所选择的 $z$，其余类似。这组值

$$
x\in\mathbf{R}^n,\quad z_1,\ldots,z_S\in\mathbf{R}^q
$$

称为**策略**（policy），因为它规定了如何选择 $x$（与发生哪一种情景无关），以及在每种可能情景下如何选择 $z$。

变量 $z$ 称为**补救变量**（recourse variable，或**第二阶段变量**），因为它允许我们在知道哪种情景已经发生后，再采取行动或作出选择。相对而言，对 $x$（称为**第一阶段变量**）的选择，必须在对具体情景一无所知时作出。

为简便起见，只考虑没有约束的情形。代价函数为

$$
f:\mathbf{R}^n\times\mathbf{R}^q\times\{1,\ldots,S\}\to\mathbf{R},
$$

其中 $f(x,z,i)$ 给出第一阶段选择为 $x$、第二阶段选择为 $z$，且情景 $i$ 发生时的代价。我们把期望代价

$$
\mathbf{E}f(x,z_s,s)=\sum_{i=1}^S\pi_i f(x,z_i,i)
$$

作为总目标，在所有策略中使其最小。

<!-- pdf-page: 226 -->

假设对每个情景 $i=1,\ldots,S$，$f$ 都是关于 $(x,z)$ 的凸函数。说明如何用凸优化找到一个最优策略，即在所有可能策略中使期望代价最小的策略。

**4.65 混合动力汽车的最优运行。** 混合动力汽车具有内燃机、与蓄电池连接的电动机／发电机，以及常规的摩擦制动器。本题考虑一个并联式混合动力汽车的高度简化模型，其中电动机／发电机和发动机都直接与驱动车轮连接。发动机可以向车轮提供功率，制动器则可以从车轮吸收功率，并将其转化为热。电动机／发电机既可以作为电动机，利用蓄电池中储存的能量向车轮输出功率，也可以作为发电机，从车轮或发动机获取功率，用来给蓄电池充电。当发电机从车轮获取功率并给蓄电池充电时，称为**再生制动**（regenerative braking）；与普通的摩擦制动不同，从车轮获取的能量被储存起来，可以在以后使用。通过让车辆驶过一条已知、固定的测试路线，评估其燃油效率。

下图展示混合动力汽车中的功率流向。箭头表示功率流被规定为正的方向。例如，发动机输出功率时，发动机功率 $p_{\mathrm{eng}}$ 为正；制动器从车轮吸收功率时，制动功率 $p_{\mathrm{br}}$ 为正。$p_{\mathrm{req}}$ 是车轮所需的功率。当车轮需要输入功率时（例如车辆加速、爬坡或在水平路面匀速行驶时），它为正。当车辆必须快速减速或下坡时，车轮所需的功率为负。

<figure id="exercise-4-65" data-uncaptioned="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/exercise-4-65.png" alt="混合动力汽车的功率流向图，包含发动机、制动器、电动机／发电机、蓄电池和车轮，以及各功率的正方向箭头" data-source-page="226" data-source-rect="229,358,462,459">
<p class="figure-translation">图内文字：Engine：发动机；Brake：制动器；wheels：车轮；Motor/generator：电动机／发电机；Battery：蓄电池。</p>
</figure>

所有这些功率都是时间的函数。我们将时间离散为一秒一个间隔，记作 $t=1,2,\ldots,T$。车轮所需的功率 $p_{\mathrm{req}}(1),\ldots,p_{\mathrm{req}}(T)$ 是给定的。（车辆在测试路线上的速度已指定，因此结合已知的道路坡度信息，以及已知的空气动力学损耗和其他损耗，可以计算出车轮所需的功率。）

功率守恒意味着

$$
p_{\mathrm{req}}(t)=p_{\mathrm{eng}}(t)+p_{\mathrm{mg}}(t)-p_{\mathrm{br}}(t),\quad t=1,\ldots,T.
$$

制动器只能耗散功率，因此每个 $t$ 都有 $p_{\mathrm{br}}(t)\geq0$。发动机只能提供功率，而且不能超过给定上限 $P_{\mathrm{eng}}^{\max}$，即

$$
0\leq p_{\mathrm{eng}}(t)\leq P_{\mathrm{eng}}^{\max},\quad t=1,\ldots,T.
$$

电动机／发电机的功率也有限制：$p_{\mathrm{mg}}$ 必须满足

$$
P_{\mathrm{mg}}^{\min}\leq p_{\mathrm{mg}}(t)\leq P_{\mathrm{mg}}^{\max},\quad t=1,\ldots,T.
$$

这里，$P_{\mathrm{mg}}^{\max}>0$ 是最大电动机功率，而 $-P_{\mathrm{mg}}^{\min}>0$ 是最大发电机功率。

时刻 $t$ 的蓄电池电量或能量记作 $E(t)$，$t=1,\ldots,T+1$。蓄电池能量满足

$$
E(t+1)=E(t)-p_{\mathrm{mg}}(t)-\eta|p_{\mathrm{mg}}(t)|,\quad t=1,\ldots,T,
$$

<!-- pdf-page: 227 -->

其中 $\eta>0$ 是已知参数。（$-p_{\mathrm{mg}}(t)$ 一项表示在忽略损耗时，电动机／发电机从蓄电池取出的能量，或向其中加入的能量。$-\eta|p_{\mathrm{mg}}(t)|$ 一项表示蓄电池或电动机／发电机效率不足所造成的能量损耗。）

蓄电池电量在所有时刻都必须介于 $0$（空电）与上限 $E_{\mathrm{batt}}^{\max}$（满电）之间。（当 $E(t)=0$ 时，蓄电池已完全放电，不能再从中取出能量；当 $E(t)=E_{\mathrm{batt}}^{\max}$ 时，蓄电池已满，不能再充电。）为了与非混合动力汽车公平比较，规定蓄电池的初始电量等于最终电量，使车辆驶过整条测试路线后的净能量变化为零：$E(1)=E(T+1)$。初始（也就是最终）能量的具体值不作指定。

本题要最小化的目标是发动机消耗的总燃油量，即

$$
F_{\mathrm{total}}=\sum_{t=1}^T F(p_{\mathrm{eng}}(t)),
$$

其中 $F:\mathbf{R}\to\mathbf{R}$ 是发动机的**燃油消耗特性**。假设 $F$ 为正、递增且为凸函数。

将此问题表述为凸优化问题，变量为 $p_{\mathrm{eng}}(t)$、$p_{\mathrm{mg}}(t)$ 和 $p_{\mathrm{br}}(t)$（$t=1,\ldots,T$），以及 $E(t)$（$t=1,\ldots,T+1$）。解释为什么你的表述与上述问题等价。

<!-- pdf-page: 228 -->
