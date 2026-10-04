<!-- pdf-page: 81 -->

# 第 3 章 凸函数

<aside class="chapter-guide">导读（编者）：本章从定义、导数条件和上图出发，说明怎样判断一个函数是否为凸函数，再介绍保持凸性的运算以及共轭函数。后半章讨论拟凸函数、对数凹函数和对数凸函数，并把凸性推广到取值为向量的函数。这些工具将用于识别和构造凸优化问题。</aside>

## 3.1 基本性质与例子

### 3.1.1 定义

如果函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的定义域 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对所有 $x,y\in\operatorname{\mathbf{dom}}f$ 及满足 $0\leq\theta\leq1$ 的 $\theta$，都有

$$
f(\theta x+(1-\theta)y)\leq\theta f(x)+(1-\theta)f(y),
\tag{3.1}
$$

就称 $f$ 是**凸函数**。从几何上看，这个不等式表示，连接 $(x,f(x))$ 和 $(y,f(y))$ 的线段，也就是从 $x$ 到 $y$ 的弦，位于 $f$ 的图像上方，见图 3.1。如果只要 $x\ne y$ 且 $0<\theta<1$，(3.1) 中就严格取不等号，则称 $f$ 是**严格凸函数**。如果 $-f$ 是凸函数，就称 $f$ 是**凹函数**；如果 $-f$ 是严格凸函数，就称 $f$ 是**严格凹函数**。

对于仿射函数，(3.1) 中总是取等号，因此所有仿射函数（从而也包括线性函数）既是凸函数，又是凹函数。反过来，任何既凸又凹的函数都是仿射函数。

<figure id="fig-3-1" data-figure="3.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-1.png" alt="凸函数的图像，以及连接图像上两点的弦" data-source-page="81" data-source-rect="183,551,407,643">
<figcaption>图 3.1 凸函数的图像。连接图像上任意两点的弦（即线段）位于图像上方。</figcaption>
</figure>

一个函数是凸函数，当且仅当将它限制在与其定义域相交的任意一条直线上时，得到的函数都是凸函数。换句话说，$f$ 是凸函数，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$<!-- pdf-page: 82 -->及所有 $v$，函数 $g(t)=f(x+tv)$ 都是凸函数（其定义域为 $\{t\mid x+tv\in\operatorname{\mathbf{dom}}f\}$）。这个性质很有用，因为它使我们可以通过把函数限制到直线上，来检验函数是否为凸函数。

凸函数的分析已经发展成一个成熟领域，本书不作深入讨论。例如，一个简单的结论是：凸函数在其定义域的相对内部连续；它只能在定义域的相对边界上出现不连续点。

### 3.1.2 扩展值延拓

把凸函数在定义域之外的值定义为 $\infty$，就可以将它延拓到整个 $\mathbf{R}^n$，这样做往往很方便。如果 $f$ 是凸函数，我们把它的**扩展值延拓**（extended-value extension）$\widetilde f:\mathbf{R}^n\to\mathbf{R}\cup\{\infty\}$ 定义为

$$
\widetilde f(x)=\begin{cases}
f(x)&x\in\operatorname{\mathbf{dom}}f\\
\infty&x\notin\operatorname{\mathbf{dom}}f.
\end{cases}
$$

延拓后的函数 $\widetilde f$ 定义在整个 $\mathbf{R}^n$ 上，取值属于 $\mathbf{R}\cup\{\infty\}$。由延拓 $\widetilde f$ 可以恢复原函数 $f$ 的定义域，即 $\operatorname{\mathbf{dom}}f=\{x\mid\widetilde f(x)<\infty\}$。

这种延拓可以简化记号，因为不必显式描述定义域，也不必每次提到 $f(x)$ 都补上“对所有 $x\in\operatorname{\mathbf{dom}}f$”这一限定。例如，考虑定义凸性的基本不等式 (3.1)。使用延拓 $\widetilde f$，可以将它写成：当 $0<\theta<1$ 时，对任意 $x$ 和 $y$，都有

$$
\widetilde f(\theta x+(1-\theta)y)\leq\theta\widetilde f(x)+(1-\theta)\widetilde f(y).
$$

（当 $\theta=0$ 或 $\theta=1$ 时，不等式总是成立。）当然，这里必须使用扩展的算术运算与序关系来理解不等式。如果 $x$ 和 $y$ 都属于 $\operatorname{\mathbf{dom}}f$，这个不等式就是 (3.1)；如果其中任意一点不属于 $\operatorname{\mathbf{dom}}f$，右端就是 $\infty$，所以不等式成立。再举一个运用这种记号的例子。设 $f_1$ 和 $f_2$ 是 $\mathbf{R}^n$ 上的两个凸函数。逐点和 $f=f_1+f_2$ 的定义域为 $\operatorname{\mathbf{dom}}f=\operatorname{\mathbf{dom}}f_1\cap\operatorname{\mathbf{dom}}f_2$，并且对任意 $x\in\operatorname{\mathbf{dom}}f$，都有 $f(x)=f_1(x)+f_2(x)$。使用扩展值延拓，只需说：对任意 $x$，都有 $\widetilde f(x)=\widetilde f_1(x)+\widetilde f_2(x)$。这个等式已经自动把 $f$ 的定义域确定为 $\operatorname{\mathbf{dom}}f=\operatorname{\mathbf{dom}}f_1\cap\operatorname{\mathbf{dom}}f_2$，因为只要 $x\notin\operatorname{\mathbf{dom}}f_1$ 或 $x\notin\operatorname{\mathbf{dom}}f_2$，就有 $\widetilde f(x)=\infty$。在这个例子中，我们利用扩展算术自动确定了定义域。

本书在这种歧义不影响理解时，会用同一个符号表示凸函数及其延拓。这相当于默认所有凸函数都已延拓，即在定义域之外的值都定义为 $\infty$。

<div class="example" markdown="1">

**例 3.1 凸集的指示函数。** 设 $C\subseteq\mathbf{R}^n$ 是凸集，考虑定义域为 $C$、对所有 $x\in C$ 都满足 $I_C(x)=0$ 的（凸）函数 $I_C$。换句话说，这个函数在集合 $C$ 上恒为零。它的扩展值延拓<!-- pdf-page: 83 -->为

$$
\widetilde I_C(x)=\begin{cases}
0&x\in C\\
\infty&x\notin C.
\end{cases}
$$

凸函数 $\widetilde I_C$ 称为集合 $C$ 的**指示函数**（indicator function）。

借助指示函数 $\widetilde I_C$，可以对记号作一些方便的处理。例如，在集合 $C$ 上最小化函数 $f$（不妨设它定义在整个 $\mathbf{R}^n$ 上），等价于在整个 $\mathbf{R}^n$ 上最小化函数 $f+\widetilde I_C$。实际上，按照我们的约定，函数 $f+\widetilde I_C$ 就是把 $f$ 限制在集合 $C$ 上得到的函数。

</div>

<figure id="fig-3-2" data-figure="3.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-2.png" alt="凸函数的图像与一点处的切线，切线位于函数图像下方" data-source-page="83" data-source-rect="193,119,471,220">
<figcaption>图 3.2 如果 $f$ 是可微凸函数，那么对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有 $f(x)+\nabla f(x)^T(y-x)\leq f(y)$。</figcaption>
</figure>

类似地，可以把凹函数在定义域之外的值定义为 $-\infty$，从而对它作延拓。

### 3.1.3 一阶条件

假设 $f$ 可微，即它的定义域 $\operatorname{\mathbf{dom}}f$ 是开集，而且在定义域的每一点处，梯度 $\nabla f$ 都存在。那么 $f$ 是凸函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对所有 $x,y\in\operatorname{\mathbf{dom}}f$ 都有

$$
f(y)\geq f(x)+\nabla f(x)^T(y-x).
\tag{3.2}
$$

图 3.2 展示了这个不等式。

关于 $y$ 的仿射函数 $f(x)+\nabla f(x)^T(y-x)$，当然就是 $f$ 在 $x$ 附近的一阶 Taylor 近似。不等式 (3.2) 表明：对于凸函数，一阶 Taylor 近似实际上是该函数的全局下界。反过来，如果一个函数的一阶 Taylor 近似总是它的全局下界，那么这个函数就是凸函数。

不等式 (3.2) 表明，由凸函数的局部信息（即它在某一点处的值和导数），可以推导出全局信息（即它的一个全局下界）。这可能是凸函数最重要的性质，也解释了凸函数和凸优化问题的一些突出性质。举一个简单例子：不等式 (3.2) 表明，如果 $\nabla f(x)=0$，那么对所有 $y\in\operatorname{\mathbf{dom}}f$，都有 $f(y)\geq f(x)$，也就是说，$x$ 是函数 $f$ 的一个全局最小点。

<!-- pdf-page: 84 -->

严格凸性也可以用一阶条件来刻画：$f$ 是严格凸函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对 $x,y\in\operatorname{\mathbf{dom}}f$、$x\ne y$，都有

$$
f(y)>f(x)+\nabla f(x)^T(y-x).
\tag{3.3}
$$

对于凹函数，有相应的刻画：$f$ 是凹函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
f(y)\leq f(x)+\nabla f(x)^T(y-x).
$$

#### 凸性一阶条件的证明

为证明 (3.2)，先考虑 $n=1$ 的情形：我们要说明，可微函数 $f:\mathbf{R}\to\mathbf{R}$ 是凸函数，当且仅当对 $\operatorname{\mathbf{dom}}f$ 中的所有 $x$ 和 $y$，都有

$$
f(y)\geq f(x)+f'(x)(y-x).
\tag{3.4}
$$

先假设 $f$ 是凸函数，且 $x,y\in\operatorname{\mathbf{dom}}f$。由于 $\operatorname{\mathbf{dom}}f$ 是凸集（即一个区间），因此对所有 $0<t\leq1$，都有 $x+t(y-x)\in\operatorname{\mathbf{dom}}f$。由 $f$ 的凸性可得

$$
f(x+t(y-x))\leq(1-t)f(x)+tf(y).
$$

两边除以 $t$，得到

$$
f(y)\geq f(x)+\frac{f(x+t(y-x))-f(x)}{t},
$$

再令 $t\to0$ 取极限，就得到 (3.4)。

为证明充分性，假设函数对 $\operatorname{\mathbf{dom}}f$（它是一个区间）中的所有 $x$ 和 $y$ 都满足 (3.4)。任取 $x\ne y$ 及 $0\leq\theta\leq1$，令 $z=\theta x+(1-\theta)y$。两次运用 (3.4)，得到

$$
f(x)\geq f(z)+f'(z)(x-z),\qquad f(y)\geq f(z)+f'(z)(y-z).
$$

将第一个不等式乘以 $\theta$，第二个乘以 $1-\theta$，再相加，得到

$$
\theta f(x)+(1-\theta)f(y)\geq f(z),
$$

这就证明了 $f$ 是凸函数。

现在可以证明 $f:\mathbf{R}^n\to\mathbf{R}$ 的一般情形。设 $x,y\in\mathbf{R}^n$，考虑将 $f$ 限制在通过这两点的直线上，即定义函数 $g(t)=f(ty+(1-t)x)$，于是 $g'(t)=\nabla f(ty+(1-t)x)^T(y-x)$。

先假设 $f$ 是凸函数，这意味着 $g$ 是凸函数。由上面的论证，有 $g(1)\geq g(0)+g'(0)$，也就是

$$
f(y)\geq f(x)+\nabla f(x)^T(y-x).
$$

现在假设这个不等式对任意 $x$ 和 $y$ 都成立。那么，如果 $ty+(1-t)x\in\operatorname{\mathbf{dom}}f$ 且 $\widetilde t y+(1-\widetilde t)x\in\operatorname{\mathbf{dom}}f$，就有

$$
f(ty+(1-t)x)\geq f(\widetilde t y+(1-\widetilde t)x)+\nabla f(\widetilde t y+(1-\widetilde t)x)^T(y-x)(t-\widetilde t),
$$

即 $g(t)\geq g(\widetilde t)+g'(\widetilde t)(t-\widetilde t)$。前面已经说明，这意味着 $g$ 是凸函数。

<!-- pdf-page: 85 -->

### 3.1.4 二阶条件

现在假设 $f$ 二阶可微，即它的定义域 $\operatorname{\mathbf{dom}}f$ 是开集，而且在定义域的每一点处，Hessian 矩阵，也就是二阶导数 $\nabla^2f$，都存在。那么 $f$ 是凸函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，而且它的 Hessian 矩阵半正定：对所有 $x\in\operatorname{\mathbf{dom}}f$，都有

$$
\nabla^2f(x)\succeq0.
$$

对于 $\mathbf{R}$ 上的函数，这就化为简单的条件 $f''(x)\geq0$（并且 $\operatorname{\mathbf{dom}}f$ 是凸集，即一个区间），意思是导数单调不减。从几何上看，条件 $\nabla^2f(x)\succeq0$ 要求函数图像在 $x$ 处具有正的、朝上的曲率。二阶条件的证明留作习题，见习题 3.8。

类似地，$f$ 是凹函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对所有 $x\in\operatorname{\mathbf{dom}}f$，都有 $\nabla^2f(x)\preceq0$。二阶条件可以部分刻画严格凸性。如果对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $\nabla^2f(x)\succ0$，那么 $f$ 是严格凸函数。但是反过来不成立：例如，函数 $f:\mathbf{R}\to\mathbf{R}$，$f(x)=x^4$ 是严格凸函数，但在 $x=0$ 处的二阶导数为零。

<div class="example" markdown="1">

**例 3.2 二次函数。** 考虑定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$ 的二次函数 $f:\mathbf{R}^n\to\mathbf{R}$，

$$
f(x)=(1/2)x^TPx+q^Tx+r,
$$

其中 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$、$r\in\mathbf{R}$。由于对所有 $x$ 都有 $\nabla^2f(x)=P$，所以 $f$ 是凸函数当且仅当 $P\succeq0$（是凹函数当且仅当 $P\preceq0$）。

二次函数的严格凸性也容易刻画：$f$ 是严格凸函数当且仅当 $P\succ0$（是严格凹函数当且仅当 $P\prec0$）。

</div>

<div class="remark" markdown="1">

**注 3.1** 在刻画凸性和凹性的一阶条件或二阶条件中，不能省略 $\operatorname{\mathbf{dom}}f$ 必须为凸集这一独立要求。例如，函数 $f(x)=1/x^2$，$\operatorname{\mathbf{dom}}f=\{x\in\mathbf{R}\mid x\ne0\}$，对所有 $x\in\operatorname{\mathbf{dom}}f$ 都满足 $f''(x)>0$，却不是凸函数。

</div>

### 3.1.5 例子

我们已经提到，所有线性函数和仿射函数都是凸函数（也是凹函数），也已经说明了哪些二次函数是凸函数或凹函数。本节再给出几个凸函数和凹函数的例子。先从变量为 $x$ 的一些 $\mathbf{R}$ 上的函数开始。

- **指数函数。** 对任意 $a\in\mathbf{R}$，$e^{ax}$ 在 $\mathbf{R}$ 上为凸函数。
- **幂函数。** 当 $a\geq1$ 或 $a\leq0$ 时，$x^a$ 在 $\mathbf{R}_{++}$ 上为凸函数；当 $0\leq a\leq1$ 时，它为凹函数。
- **绝对值的幂。** 当 $p\geq1$ 时，$|x|^p$ 在 $\mathbf{R}$ 上为凸函数。
- **对数函数。** $\log x$ 在 $\mathbf{R}_{++}$ 上为凹函数。
- <!-- pdf-page: 86 -->**负熵。** $x\log x$ 是凸函数，定义域可以取 $\mathbf{R}_{++}$，也可以取 $\mathbf{R}_+$，此时把 $x=0$ 处的值定义为 0。

<figure id="fig-3-3" data-figure="3.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-3.png" alt="函数 x²/y 的三维网格曲面，保留三个坐标轴及刻度" data-source-page="86" data-source-rect="225,116,448,296">
<figcaption>图 3.3 函数 $f(x,y)=x^2/y$ 的图像。</figcaption>
</figure>

对于这些例子，可以通过验证基本不等式 (3.1)，或者检查二阶导数是非负还是非正，来证明凸性或凹性。例如，对 $f(x)=x\log x$，有

$$
f'(x)=\log x+1,\qquad f''(x)=1/x,
$$

因此，当 $x>0$ 时，$f''(x)>0$。这说明负熵函数是（严格）凸函数。

下面给出 $\mathbf{R}^n$ 上的几个有意思的函数例子。

- **范数。** $\mathbf{R}^n$ 上的每个范数都是凸函数。
- **最大值函数。** $f(x)=\max\{x_1,\ldots,x_n\}$ 在 $\mathbf{R}^n$ 上为凸函数。
- **二次除以线性函数。** 函数 $f(x,y)=x^2/y$，其定义域为

    $$
    \operatorname{\mathbf{dom}}f=\mathbf{R}\times\mathbf{R}_{++}=\{(x,y)\in\mathbf{R}^2\mid y>0\},
    $$

    是凸函数，见图 3.3。

- **指数和的对数（log-sum-exp）。** 函数 $f(x)=\log(e^{x_1}+\cdots+e^{x_n})$ 在 $\mathbf{R}^n$ 上为凸函数。它可以看作最大值函数的可微（实际上是解析）近似，因为对所有 $x$，都有

    $$
    \max\{x_1,\ldots,x_n\}\leq f(x)\leq\max\{x_1,\ldots,x_n\}+\log n.
    $$

    （当 $x$ 的所有分量都相等时，第二个不等式取等号。）图 3.4 展示了 $n=2$ 时的函数 $f$。

- <!-- pdf-page: 87 -->**几何平均。** 几何平均 $f(x)=(\prod_{i=1}^n x_i)^{1/n}$ 在 $\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n$ 上为凹函数。
- **对数行列式。** 函数 $f(X)=\log\det X$ 在 $\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n$ 上为凹函数。

<figure id="fig-3-4" data-figure="3.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-4.png" alt="函数 log(e^x+e^y) 的三维网格曲面，保留三个坐标轴及刻度" data-source-page="87" data-source-rect="172,140,396,305">
<figcaption>图 3.4 函数 $f(x,y)=\log(e^x+e^y)$ 的图像。</figcaption>
</figure>

这些例子的凸性（或凹性）有多种验证方法，例如直接验证不等式 (3.1)、验证 Hessian 矩阵半正定，或者把函数限制在任意一条直线上，再验证得到的一元函数具有凸性。

**范数。** 如果 $f:\mathbf{R}^n\to\mathbf{R}$ 是范数，且 $0\leq\theta\leq1$，那么

$$
f(\theta x+(1-\theta)y)\leq f(\theta x)+f((1-\theta)y)=\theta f(x)+(1-\theta)f(y).
$$

这里的不等式来自三角不等式，等式来自范数的齐次性。

**最大值函数。** 当 $0\leq\theta\leq1$ 时，函数 $f(x)=\max_i x_i$ 满足

$$
\begin{aligned}
f(\theta x+(1-\theta)y)&=\max_i(\theta x_i+(1-\theta)y_i)\\
&\leq\theta\max_i x_i+(1-\theta)\max_i y_i\\
&=\theta f(x)+(1-\theta)f(y).
\end{aligned}
$$

**二次除以线性函数。** 为证明二次除以线性函数 $f(x,y)=x^2/y$ 是凸函数，注意到当 $y>0$ 时，

$$
\nabla^2f(x,y)=\frac{2}{y^3}\begin{bmatrix}y^2&-xy\\-xy&x^2\end{bmatrix}
=\frac{2}{y^3}\begin{bmatrix}y\\-x\end{bmatrix}\begin{bmatrix}y\\-x\end{bmatrix}^{T}\succeq0.
$$

<!-- pdf-page: 88 -->

**指数和的对数。** 指数和的对数函数的 Hessian 矩阵为

$$
\nabla^2f(x)=\frac{1}{(\mathbf{1}^Tz)^2}\left((\mathbf{1}^Tz)\operatorname{\mathbf{diag}}(z)-zz^T\right),
$$

其中 $z=(e^{x_1},\ldots,e^{x_n})$。为验证 $\nabla^2f(x)\succeq0$，必须证明：对所有 $v$，都有 $v^T\nabla^2f(x)v\geq0$，即

$$
v^T\nabla^2f(x)v=\frac{1}{(\mathbf{1}^Tz)^2}\left(\left(\sum_{i=1}^n z_i\right)\left(\sum_{i=1}^n v_i^2z_i\right)-\left(\sum_{i=1}^n v_i z_i\right)^2\right)\geq0.
$$

对分量为 $a_i=v_i\sqrt{z_i}$、$b_i=\sqrt{z_i}$ 的两个向量应用 Cauchy–Schwarz 不等式 $(a^Ta)(b^Tb)\geq(a^Tb)^2$，就得到这个结果。

**几何平均。** 用类似的方法可以说明，几何平均 $f(x)=(\prod_{i=1}^n x_i)^{1/n}$ 在 $\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n$ 上为凹函数。它的 Hessian 矩阵 $\nabla^2f(x)$ 的各元素为

$$
\frac{\partial^2f(x)}{\partial x_k^2}=-(n-1)\frac{(\prod_{i=1}^n x_i)^{1/n}}{n^2x_k^2},\qquad
\frac{\partial^2f(x)}{\partial x_k\partial x_l}=\frac{(\prod_{i=1}^n x_i)^{1/n}}{n^2x_kx_l}\quad\text{当 }k\ne l,
$$

并可写为

$$
\nabla^2f(x)=-\frac{\prod_{i=1}^n x_i^{1/n}}{n^2}\left(n\operatorname{\mathbf{diag}}(1/x_1^2,\ldots,1/x_n^2)-qq^T\right),
$$

其中 $q_i=1/x_i$。我们必须证明 $\nabla^2f(x)\preceq0$，即对所有 $v$，都有

$$
v^T\nabla^2f(x)v=-\frac{\prod_{i=1}^n x_i^{1/n}}{n^2}\left(n\sum_{i=1}^n v_i^2/x_i^2-\left(\sum_{i=1}^n v_i/x_i\right)^2\right)\leq0.
$$

同样，对向量 $a=\mathbf{1}$ 和分量为 $b_i=v_i/x_i$ 的向量 $b$ 应用 Cauchy–Schwarz 不等式 $(a^Ta)(b^Tb)\geq(a^Tb)^2$，就得到这个结果。

**对数行列式。** 对于函数 $f(X)=\log\det X$，可以通过考察任意一条直线 $X=Z+tV$ 来验证凹性，其中 $Z,V\in\mathbf{S}^n$。定义 $g(t)=f(Z+tV)$，并把 $g$ 限制在使 $Z+tV\succ0$ 成立的 $t$ 值所构成的区间上。不失一般性，可以假设 $t=0$ 位于这个区间内，即 $Z\succ0$。于是

$$
\begin{aligned}
g(t)&=\log\det(Z+tV)\\
&=\log\det\left(Z^{1/2}(I+tZ^{-1/2}VZ^{-1/2})Z^{1/2}\right)\\
&=\sum_{i=1}^n\log(1+t\lambda_i)+\log\det Z,
\end{aligned}
$$

其中 $\lambda_1,\ldots,\lambda_n$ 是 $Z^{-1/2}VZ^{-1/2}$ 的特征值。因此

$$
g'(t)=\sum_{i=1}^n\frac{\lambda_i}{1+t\lambda_i},\qquad
g''(t)=-\sum_{i=1}^n\frac{\lambda_i^2}{(1+t\lambda_i)^2}.
$$

由于 $g''(t)\leq0$，可知 $f$ 是凹函数。

<!-- pdf-page: 89 -->

### 3.1.6 下水平集

函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的 **$\alpha$ 下水平集**（$\alpha$-sublevel set）定义为

$$
C_\alpha=\{x\in\operatorname{\mathbf{dom}}f\mid f(x)\leq\alpha\}.
$$

对于任意 $\alpha$，凸函数的下水平集都是凸集。由凸性的定义立即可以证明：如果 $x,y\in C_\alpha$，那么 $f(x)\leq\alpha$ 且 $f(y)\leq\alpha$，所以当 $0\leq\theta\leq1$ 时，$f(\theta x+(1-\theta)y)\leq\alpha$，从而 $\theta x+(1-\theta)y\in C_\alpha$。

反过来不成立：一个函数的所有下水平集都可能是凸集，但它本身却不是凸函数。例如，$f(x)=-e^x$ 在 $\mathbf{R}$ 上不是凸函数（实际上，它是严格凹函数），但它的所有下水平集都是凸集。

如果 $f$ 是凹函数，那么它的 **$\alpha$ 上水平集**（$\alpha$-superlevel set）$\{x\in\operatorname{\mathbf{dom}}f\mid f(x)\geq\alpha\}$ 是凸集。下水平集的性质常常为证明集合的凸性提供方便的方法：把集合表示成凸函数的下水平集，或者凹函数的上水平集即可。

<div class="example" markdown="1">

**例 3.3** $x\in\mathbf{R}_+^n$ 的几何平均与算术平均分别为

$$
G(x)=\left(\prod_{i=1}^n x_i\right)^{1/n},\qquad A(x)=\frac{1}{n}\sum_{i=1}^n x_i,
$$

其中在 $G$ 的定义中取 $0^{1/n}=0$。算术平均–几何平均不等式指出，$G(x)\leq A(x)$。

设 $0\leq\alpha\leq1$，考虑集合

$$
\{x\in\mathbf{R}_+^n\mid G(x)\geq\alpha A(x)\},
$$

即几何平均不小于算术平均的 $\alpha$ 倍的所有向量所组成的集合。这个集合是凸集，因为它是凹函数 $G(x)-\alpha A(x)$ 的 0 上水平集。实际上，该集合还具有正齐次性，因此是一个凸锥。

</div>

### 3.1.7 上图

函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的**图像**定义为

$$
\{(x,f(x))\mid x\in\operatorname{\mathbf{dom}}f\},
$$

它是 $\mathbf{R}^{n+1}$ 的子集。函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的**上图**（epigraph）定义为

$$
\operatorname{\mathbf{epi}}f=\{(x,t)\mid x\in\operatorname{\mathbf{dom}}f,\ f(x)\leq t\},
$$

它也是 $\mathbf{R}^{n+1}$ 的子集。（“Epi”表示“在上方”，所以 epigraph 的意思就是“图像上方”。）图 3.5 展示了这个定义。

上图把凸集与凸函数联系起来：一个函数是凸函数，当且仅当它的上图是凸集。一个函数是凹函数，当且仅当它的**下图**（hypograph）是凸集，下图定义为

$$
\operatorname{\mathbf{hypo}}f=\{(x,t)\mid t\leq f(x)\}.
$$

<!-- pdf-page: 90 -->

<figure id="fig-3-5" data-figure="3.5">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-5.png" alt="函数曲线及其上方的阴影区域，阴影区域表示函数的上图" data-source-page="90" data-source-rect="246,121,431,246">
<figcaption>图 3.5 函数 $f$ 的上图，用阴影表示。下边界用较深的线条表示，它就是 $f$ 的图像。</figcaption>
<p class="figure-translation">图内文字：$\operatorname{\mathbf{epi}}f$ 表示 $f$ 的上图。</p>
</figure>

<div class="example" markdown="1">

**例 3.4 矩阵分式函数。** 函数 $f:\mathbf{R}^n\times\mathbf{S}^n\to\mathbf{R}$ 定义为

$$
f(x,Y)=x^TY^{-1}x,
$$

它在 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n\times\mathbf{S}_{++}^n$ 上为凸函数。（它推广了二次除以线性函数 $f(x,y)=x^2/y$，后者的定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}\times\mathbf{R}_{++}$。）

证明 $f$ 凸性的一个简单方法是考察它的上图：

$$
\begin{aligned}
\operatorname{\mathbf{epi}}f&=\{(x,Y,t)\mid Y\succ0,\ x^TY^{-1}x\leq t\}\\
&=\left\{(x,Y,t)\ \middle|\ \begin{bmatrix}Y&x\\x^T&t\end{bmatrix}\succeq0,\ Y\succ0\right\},
\end{aligned}
$$

这里使用了分块矩阵半正定的 Schur 补条件，见第 A.5.5 节。最后一个条件是关于 $(x,Y,t)$ 的线性矩阵不等式，因此 $\operatorname{\mathbf{epi}}f$ 是凸集。

在 $n=1$ 这一特殊情形下，矩阵分式函数化为二次除以线性函数 $x^2/y$，对应的线性矩阵不等式（LMI）表示为

$$
\begin{bmatrix}y&x\\x&t\end{bmatrix}\succeq0,\qquad y>0
$$

（它的图像见图 3.3）。

</div>

关于凸函数的许多结论，都可以借助上图并应用凸集的结论，从几何上加以证明或解释。例如，考虑凸性的一阶条件：

$$
f(y)\geq f(x)+\nabla f(x)^T(y-x),
$$

其中 $f$ 是凸函数，且 $x,y\in\operatorname{\mathbf{dom}}f$。可以利用 $\operatorname{\mathbf{epi}}f$，从几何上解释这个基本不等式。如果 $(y,t)\in\operatorname{\mathbf{epi}}f$，那么

$$
t\geq f(y)\geq f(x)+\nabla f(x)^T(y-x).
$$

<!-- pdf-page: 91 -->

<figure id="fig-3-6" data-figure="3.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-6.png" alt="凸函数的上图、在函数图像上一点处的支撑超平面，以及指向右下方的法向量" data-source-page="91" data-source-rect="193,121,402,248">
<figcaption>图 3.6 对于可微凸函数 $f$，向量 $(\nabla f(x),-1)$ 确定了 $f$ 的上图在 $x$ 处的一条支撑超平面。</figcaption>
<p class="figure-translation">图内文字：$\operatorname{\mathbf{epi}}f$ 表示 $f$ 的上图。</p>
</figure>

这可以写成

$$
(y,t)\in\operatorname{\mathbf{epi}}f\quad\Longrightarrow\quad
\begin{bmatrix}\nabla f(x)\\-1\end{bmatrix}^{T}
\left(\begin{bmatrix}y\\t\end{bmatrix}-\begin{bmatrix}x\\f(x)\end{bmatrix}\right)\leq0.
$$

这意味着，由 $(\nabla f(x),-1)$ 确定的超平面，在边界点 $(x,f(x))$ 处支撑 $\operatorname{\mathbf{epi}}f$，见图 3.6。

### 3.1.8 Jensen 不等式及其推广

基本不等式 (3.1)，即

$$
f(\theta x+(1-\theta)y)\leq\theta f(x)+(1-\theta)f(y),
$$

有时称为 **Jensen 不等式**。它容易推广到两个以上点的凸组合：如果 $f$ 是凸函数，$x_1,\ldots,x_k\in\operatorname{\mathbf{dom}}f$，并且 $\theta_1,\ldots,\theta_k\geq0$、$\theta_1+\cdots+\theta_k=1$，那么

$$
f(\theta_1x_1+\cdots+\theta_kx_k)\leq\theta_1f(x_1)+\cdots+\theta_kf(x_k).
$$

与凸集的情形相同，这个不等式还可以推广到无穷和、积分以及期望。例如，如果在 $S\subseteq\operatorname{\mathbf{dom}}f$ 上有 $p(x)\geq0$，且 $\int_Sp(x)\,dx=1$，那么，只要积分存在，就有

$$
f\left(\int_Sp(x)x\,dx\right)\leq\int_Sf(x)p(x)\,dx.
$$

在最一般的情形下，可以取支集位于 $\operatorname{\mathbf{dom}}f$ 内的任意概率测度。如果 $x$ 是随机变量，以概率 1 满足 $x\in\operatorname{\mathbf{dom}}f$，并且 $f$ 是凸函数，那么，只要期望存在，就有

$$
f(\mathbf{E}x)\leq\mathbf{E}f(x).
\tag{3.5}
$$

取随机变量 $x$ 的支集为 $\{x_1,x_2\}$，并令<!-- pdf-page: 92 -->$\operatorname{\mathbf{prob}}(x=x_1)=\theta$、$\operatorname{\mathbf{prob}}(x=x_2)=1-\theta$，就可以从这一一般形式恢复基本不等式 (3.1)。因此，不等式 (3.5) 刻画了凸性：如果 $f$ 不是凸函数，就存在一个以概率 1 满足 $x\in\operatorname{\mathbf{dom}}f$ 的随机变量 $x$，使得 $f(\mathbf{E}x)>\mathbf{E}f(x)$。

现在，这些不等式都称为 Jensen 不等式，尽管 Jensen 当初研究的只是下面这个非常简单的不等式：

$$
f\left(\frac{x+y}{2}\right)\leq\frac{f(x)+f(y)}{2}.
$$

<div class="remark" markdown="1">

**注 3.2** 可以这样解释 (3.5)。设 $x\in\operatorname{\mathbf{dom}}f\subseteq\mathbf{R}^n$，$z$ 是 $\mathbf{R}^n$ 中任意零均值随机向量。那么

$$
\mathbf{E}f(x+z)\geq f(x).
$$

因此，随机化或抖动（dithering，即给自变量加上一个零均值随机向量）不能使凸函数的值在平均意义上减小。

</div>

### 3.1.9 不等式

对适当的凸函数应用 Jensen 不等式，可以推导出许多著名的不等式。（事实上，凸性和 Jensen 不等式可以作为一套不等式理论的基础。）作为一个简单例子，考虑算术平均–几何平均不等式：对于 $a,b\geq0$，有

$$
\sqrt{ab}\leq(a+b)/2.
\tag{3.6}
$$

函数 $-\log x$ 是凸函数；取 $\theta=1/2$，由 Jensen 不等式得到

$$
-\log\left(\frac{a+b}{2}\right)\leq\frac{-\log a-\log b}{2}.
$$

两边取指数，就得到 (3.6)。

再看一个稍复杂的例子，我们来证明 Hölder 不等式：当 $p>1$、$1/p+1/q=1$ 且 $x,y\in\mathbf{R}^n$ 时，

$$
\sum_{i=1}^n x_i y_i\leq\left(\sum_{i=1}^n|x_i|^p\right)^{1/p}\left(\sum_{i=1}^n|y_i|^q\right)^{1/q}.
$$

由 $-\log x$ 的凸性，并对一般的 $\theta$ 应用 Jensen 不等式，得到更一般的算术平均–几何平均不等式

$$
a^\theta b^{1-\theta}\leq\theta a+(1-\theta)b,
$$

它对 $a,b\geq0$、$0\leq\theta\leq1$ 成立。取

$$
a=\frac{|x_i|^p}{\sum_{j=1}^n|x_j|^p},\qquad
b=\frac{|y_i|^q}{\sum_{j=1}^n|y_j|^q},\qquad\theta=1/p,
$$

代入上述不等式，得到

$$
\left(\frac{|x_i|^p}{\sum_{j=1}^n|x_j|^p}\right)^{1/p}
\left(\frac{|y_i|^q}{\sum_{j=1}^n|y_j|^q}\right)^{1/q}
\leq\frac{|x_i|^p}{p\sum_{j=1}^n|x_j|^p}+\frac{|y_i|^q}{q\sum_{j=1}^n|y_j|^q}.
$$

再对 $i$ 求和，就得到 Hölder 不等式。

<!-- pdf-page: 93 -->

## 3.2 保持凸性的运算

本节介绍一些能够保持函数凸性或凹性、或者用来构造新的凸函数和凹函数的运算。先从加法、缩放和逐点上确界等简单运算开始，再介绍一些更复杂的运算，其中有些以这些简单运算为特殊情况。

### 3.2.1 非负加权和

显然，如果 $f$ 是凸函数且 $\alpha\geq0$，那么函数 $\alpha f$ 也是凸函数。如果 $f_1$ 和 $f_2$ 都是凸函数，那么它们的和 $f_1+f_2$ 也是凸函数。把非负缩放与加法结合起来，可以看出，凸函数组成的集合本身就是一个凸锥：凸函数的非负加权和

$$
f=w_1f_1+\cdots+w_mf_m
$$

是凸函数。类似地，凹函数的非负加权和是凹函数。严格凸（凹）函数的非负且不全为零的加权和，是严格凸（凹）函数。

这些性质可以推广到无穷和与积分。例如，如果对每个 $y\in A$，$f(x,y)$ 关于 $x$ 是凸函数，且对每个 $y\in A$ 都有 $w(y)\geq0$，那么由

$$
g(x)=\int_Aw(y)f(x,y)\,dy
$$

定义的函数 $g$ 关于 $x$ 是凸函数，只要该积分存在。

非负缩放和加法保持凸性这一事实，既容易直接验证，也可以从相应的上图看出来。例如，如果 $w\geq0$ 且 $f$ 是凸函数，那么

$$
\operatorname{\mathbf{epi}}(wf)=\begin{bmatrix}I&0\\0&w\end{bmatrix}\operatorname{\mathbf{epi}}f,
$$

它是凸集，因为凸集在线性映射下的像是凸集。

<div class="translator-note" markdown="1">

**译注（第 3.2.1 节）：** 这里的上图等式一般要求 $w>0$。例如，取定义在整个 $\mathbf{R}^n$ 上的零函数并令 $w=0$，右侧只含末坐标为 $0$ 的点，而左侧的上图还包含末坐标为正的点。非负缩放保持凸性的结论仍然成立。

</div>

### 3.2.2 与仿射映射复合

设 $f:\mathbf{R}^n\to\mathbf{R}$、$A\in\mathbf{R}^{n\times m}$、$b\in\mathbf{R}^n$。定义 $g:\mathbf{R}^m\to\mathbf{R}$ 为

$$
g(x)=f(Ax+b),
$$

其定义域为 $\operatorname{\mathbf{dom}}g=\{x\mid Ax+b\in\operatorname{\mathbf{dom}}f\}$。那么，如果 $f$ 是凸函数，$g$ 也是凸函数；如果 $f$ 是凹函数，$g$ 也是凹函数。

<!-- pdf-page: 94 -->

### 3.2.3 逐点最大值与上确界

如果 $f_1$ 和 $f_2$ 是凸函数，那么由

$$
f(x)=\max\{f_1(x),f_2(x)\}
$$

定义、定义域为 $\operatorname{\mathbf{dom}}f=\operatorname{\mathbf{dom}}f_1\cap\operatorname{\mathbf{dom}}f_2$ 的**逐点最大值**函数 $f$ 也是凸函数。这个性质容易验证：如果 $0\leq\theta\leq1$ 且 $x,y\in\operatorname{\mathbf{dom}}f$，那么

$$
\begin{aligned}
f(\theta x+(1-\theta)y)&=\max\{f_1(\theta x+(1-\theta)y),f_2(\theta x+(1-\theta)y)\}\\
&\leq\max\{\theta f_1(x)+(1-\theta)f_1(y),\theta f_2(x)+(1-\theta)f_2(y)\}\\
&\leq\theta\max\{f_1(x),f_2(x)\}+(1-\theta)\max\{f_1(y),f_2(y)\}\\
&=\theta f(x)+(1-\theta)f(y),
\end{aligned}
$$

这就证明了 $f$ 的凸性。也容易证明，如果 $f_1,\ldots,f_m$ 都是凸函数，那么它们的逐点最大值

$$
f(x)=\max\{f_1(x),\ldots,f_m(x)\}
$$

也是凸函数。

<div class="example" markdown="1">

**例 3.5 分段线性函数。** 函数

$$
f(x)=\max\{a_1^Tx+b_1,\ldots,a_L^Tx+b_L\}
$$

定义了一个分段线性函数（准确地说，是分段仿射函数），它具有 $L$ 个或更少的分区。它是凸函数，因为它是仿射函数的逐点最大值。

也可以证明其逆命题：任何具有 $L$ 个或更少分区的分段线性凸函数，都可以表示成这种形式，见习题 3.29。

</div>

<div class="example" markdown="1">

**例 3.6 最大的 $r$ 个分量之和。** 对于 $x\in\mathbf{R}^n$，用 $x_{[i]}$ 表示 $x$ 的第 $i$ 大分量，也就是说，

$$
x_{[1]}\geq x_{[2]}\geq\cdots\geq x_{[n]}
$$

是按非增次序排列的 $x$ 的各分量。那么函数

$$
f(x)=\sum_{i=1}^r x_{[i]},
$$

也就是 $x$ 中最大的 $r$ 个元素之和，是凸函数。把它写成

$$
f(x)=\sum_{i=1}^r x_{[i]}=\max\{x_{i_1}+\cdots+x_{i_r}\mid1\leq i_1<i_2<\cdots<i_r\leq n\},
$$

即可看出这一点：它是从 $x$ 中选取 $r$ 个不同分量后，所有可能的和的最大值。由于它是 $n!/(r!(n-r)!)$ 个线性函数的逐点最大值，因此是凸函数。

进一步可以证明，只要 $w_1\geq w_2\geq\cdots\geq w_r\geq0$，函数 $\sum_{i=1}^r w_i x_{[i]}$ 就是凸函数，见习题 3.19。

</div>

<!-- pdf-page: 95 -->

逐点最大值的性质可以推广到无穷多个凸函数的逐点上确界。如果对每个 $y\in A$，$f(x,y)$ 关于 $x$ 是凸函数，那么由

$$
g(x)=\sup_{y\in A}f(x,y)
\tag{3.7}
$$

定义的函数 $g$ 关于 $x$ 是凸函数。这里 $g$ 的定义域是

$$
\operatorname{\mathbf{dom}}g=\left\{x\ \middle|\ (x,y)\in\operatorname{\mathbf{dom}}f\text{ 对所有 }y\in A\text{ 成立},\ \sup_{y\in A}f(x,y)<\infty\right\}.
$$

类似地，一族凹函数的逐点下确界是凹函数。

从上图来看，函数的逐点上确界对应于上图的交集：对于 (3.7) 中的 $f$、$g$ 和 $A$，有

$$
\operatorname{\mathbf{epi}}g=\bigcap_{y\in A}\operatorname{\mathbf{epi}}f(\cdot,y).
$$

因此，上述结论来自一族凸集的交集仍为凸集这一事实。

<div class="example" markdown="1">

**例 3.7 集合的支撑函数。** 设 $C\subseteq\mathbf{R}^n$ 且 $C\ne\varnothing$。集合 $C$ 的**支撑函数**（support function）$S_C$ 定义为

$$
S_C(x)=\sup\{x^Ty\mid y\in C\}
$$

（自然，其定义域为 $\operatorname{\mathbf{dom}}S_C=\{x\mid\sup_{y\in C}x^Ty<\infty\}$）。

对于每个 $y\in C$，$x^Ty$ 都是 $x$ 的线性函数，所以 $S_C$ 是一族线性函数的逐点上确界，因此是凸函数。

</div>

<div class="example" markdown="1">

**例 3.8 到集合中最远点的距离。** 设 $C\subseteq\mathbf{R}^n$。到 $C$ 中最远点的距离（可以采用任意范数）

$$
f(x)=\sup_{y\in C}\|x-y\|
$$

是凸函数。为说明这一点，注意到对任意 $y$，函数 $\|x-y\|$ 关于 $x$ 是凸函数。由于 $f$ 是一族凸函数（由 $y\in C$ 索引）的逐点上确界，所以它是 $x$ 的凸函数。

</div>

<div class="example" markdown="1">

**例 3.9 最小二乘代价作为权重的函数。** 设 $a_1,\ldots,a_n\in\mathbf{R}^m$。在加权最小二乘问题中，我们对 $x\in\mathbf{R}^m$ 最小化目标函数 $\sum_{i=1}^n w_i(a_i^Tx-b_i)^2$。我们把 $w_i$ 称为权重，并允许 $w_i$ 取负值，这使得目标函数有可能无下界。

定义（最优的）加权最小二乘代价为

$$
g(w)=\inf_x\sum_{i=1}^n w_i(a_i^Tx-b_i)^2,
$$

其定义域为

$$
\operatorname{\mathbf{dom}}g=\left\{w\ \middle|\ \inf_x\sum_{i=1}^n w_i(a_i^Tx-b_i)^2>-\infty\right\}.
$$

<!-- pdf-page: 96 -->

由于 $g$ 是一族关于 $w$ 的线性函数（由 $x\in\mathbf{R}^m$ 索引）的下确界，因此它是 $w$ 的凹函数。

至少在 $g$ 的一部分定义域上，可以推导出它的显式表达式。令 $W=\operatorname{\mathbf{diag}}(w)$，即对角元素为 $w_1,\ldots,w_n$ 的对角矩阵，并令 $A\in\mathbf{R}^{n\times m}$ 的各行为 $a_i^T$，则有

$$
g(w)=\inf_x(Ax-b)^TW(Ax-b)=\inf_x(x^TA^TWAx-2b^TWAx+b^TWb).
$$

由此可见，如果 $A^TWA\not\succeq0$，这个二次函数关于 $x$ 无下界，因此 $g(w)=-\infty$，即 $w\notin\operatorname{\mathbf{dom}}g$。当 $A^TWA\succ0$ 时（这是一个严格线性矩阵不等式），通过解析地最小化这个二次函数，可以给出 $g$ 的一个简单表达式：

$$
\begin{aligned}
g(w)&=b^TWb-b^TWA(A^TWA)^{-1}A^TWb\\
&=\sum_{i=1}^n w_i b_i^2-\sum_{i=1}^n w_i^2b_i^2a_i^T\left(\sum_{j=1}^n w_j a_j a_j^T\right)^{-1}a_i.
\end{aligned}
$$

从这个表达式不能立即看出 $g$ 的凹性，不过仍然可以证明，例如可以利用矩阵分式函数的凸性，见例 3.4。

</div>

<div class="translator-note" markdown="1">

**译注（例 3.9）：** 第二行的展开漏掉了不同下标之间的交叉项，一般不等于第一行。应使用第一行的矩阵二次型，或把所减的项展开为对两组下标的双重求和。

</div>

<div class="example" markdown="1">

**例 3.10 对称矩阵的最大特征值。** 函数 $f(X)=\lambda_{\max}(X)$，$\operatorname{\mathbf{dom}}f=\mathbf{S}^m$，是凸函数。为说明这一点，把 $f$ 表示为

$$
f(X)=\sup\{y^TXy\mid\|y\|_2=1\},
$$

也就是一族关于 $X$ 的线性函数（即 $y^TXy$）的逐点上确界，这一族函数由 $y\in\mathbf{R}^m$ 索引。

</div>

<div class="example" markdown="1">

**例 3.11 矩阵的范数。** 考虑 $f(X)=\|X\|_2$，$\operatorname{\mathbf{dom}}f=\mathbf{R}^{p\times q}$，其中 $\|\cdot\|_2$ 表示谱范数，也就是最大奇异值。$f$ 的凸性来自

$$
f(X)=\sup\{u^TXv\mid\|u\|_2=1,\ \|v\|_2=1\},
$$

这个表达式说明，它是一族关于 $X$ 的线性函数的逐点上确界。

作为推广，设 $\|\cdot\|_a$ 和 $\|\cdot\|_b$ 分别是 $\mathbf{R}^p$ 和 $\mathbf{R}^q$ 上的范数。矩阵 $X\in\mathbf{R}^{p\times q}$ 的**诱导范数**定义为

$$
\|X\|_{a,b}=\sup_{v\ne0}\frac{\|Xv\|_a}{\|v\|_b}.
$$

（当两个范数都是欧几里得范数时，它就化为谱范数。）诱导范数可以写成

$$
\begin{aligned}
\|X\|_{a,b}&=\sup\{\|Xv\|_a\mid\|v\|_b=1\}\\
&=\sup\{u^TXv\mid\|u\|_{a*}=1,\ \|v\|_b=1\},
\end{aligned}
$$

其中 $\|\cdot\|_{a*}$ 是 $\|\cdot\|_a$ 的对偶范数，并且我们使用了以下事实：

$$
\|z\|_a=\sup\{u^Tz\mid\|u\|_{a*}=1\}.
$$

由于已把 $\|X\|_{a,b}$ 表示成关于 $X$ 的线性函数的上确界，所以它是凸函数。

</div>

<!-- pdf-page: 97 -->

#### 表示为仿射函数的逐点上确界

前面的例子说明了证明函数凸性的一个有效方法：把它表示成一族仿射函数的逐点上确界。除去一个技术条件，逆命题也成立：几乎每个凸函数都可以表示成一族仿射函数的逐点上确界。例如，如果 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，且 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$，那么

$$
f(x)=\sup\{g(x)\mid g\text{ 为仿射函数，且对所有 }z\text{ 有 }g(z)\leq f(z)\}.
$$

换句话说，$f$ 是它的所有仿射全局下界函数的逐点上确界。下面证明这个结论，而 $\operatorname{\mathbf{dom}}f\ne\mathbf{R}^n$ 的情形留作习题，见习题 3.28。

设 $f$ 是凸函数，且 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$。不等式

$$
f(x)\geq\sup\{g(x)\mid g\text{ 为仿射函数，且对所有 }z\text{ 有 }g(z)\leq f(z)\}
$$

显然成立，因为只要 $g$ 是 $f$ 的一个仿射下界函数，就有 $g(x)\leq f(x)$。为证明等式成立，我们将说明：对于每个 $x\in\mathbf{R}^n$，都存在一个作为 $f$ 全局下界的仿射函数 $g$，并且满足 $g(x)=f(x)$。

$f$ 的上图当然是凸集。因此，可以找到它在 $(x,f(x))$ 处的一个支撑超平面，也就是存在 $a\in\mathbf{R}^n$ 和 $b\in\mathbf{R}$，满足 $(a,b)\ne0$，并且对所有 $(z,t)\in\operatorname{\mathbf{epi}}f$，都有

$$
\begin{bmatrix}a\\b\end{bmatrix}^{T}\begin{bmatrix}x-z\\f(x)-t\end{bmatrix}\leq0.
$$

这意味着，对所有 $z\in\operatorname{\mathbf{dom}}f=\mathbf{R}^n$ 和所有 $s\geq0$，都有

$$
a^T(x-z)+b(f(x)-f(z)-s)\leq0,
\tag{3.8}
$$

因为 $(z,t)\in\operatorname{\mathbf{epi}}f$ 意味着存在某个 $s\geq0$，使 $t=f(z)+s$。要使不等式 (3.8) 对所有 $s\geq0$ 成立，必须有 $b\geq0$。如果 $b=0$，则不等式 (3.8) 化为对所有 $z\in\mathbf{R}^n$ 都有 $a^T(x-z)\leq0$，这意味着 $a=0$，与 $(a,b)\ne0$ 矛盾。所以 $b>0$，也就是说，这个支撑超平面不是竖直的。

利用 $b>0$，把 $s=0$ 时的 (3.8) 改写为：对所有 $z$，都有

$$
g(z)=f(x)+(a/b)^T(x-z)\leq f(z).
$$

函数 $g$ 是 $f$ 的一个仿射下界函数，并且满足 $g(x)=f(x)$。

### 3.2.4 复合

本节考察 $h:\mathbf{R}^k\to\mathbf{R}$ 和 $g:\mathbf{R}^n\to\mathbf{R}^k$ 应满足什么条件，才能保证它们的复合 $f=h\circ g:\mathbf{R}^n\to\mathbf{R}$ 为凸函数或凹函数。复合函数定义为

$$
f(x)=h(g(x)),\qquad\operatorname{\mathbf{dom}}f=\{x\in\operatorname{\mathbf{dom}}g\mid g(x)\in\operatorname{\mathbf{dom}}h\}.
$$

<!-- pdf-page: 98 -->

#### 标量复合

先考虑 $k=1$ 的情形，此时 $h:\mathbf{R}\to\mathbf{R}$，$g:\mathbf{R}^n\to\mathbf{R}$。只需考察 $n=1$ 的情形，因为函数的凸性取决于它在与定义域相交的任意直线上的表现。

为了找出复合规则，先假设 $h$ 和 $g$ 都二阶可微，且 $\operatorname{\mathbf{dom}}g=\operatorname{\mathbf{dom}}h=\mathbf{R}$。此时，$f$ 的凸性等价于 $f''\geq0$，即对所有 $x\in\mathbf{R}$ 都有 $f''(x)\geq0$。

复合函数 $f=h\circ g$ 的二阶导数为

$$
f''(x)=h''(g(x))g'(x)^2+h'(g(x))g''(x).
\tag{3.9}
$$

例如，假设 $g$ 为凸函数（所以 $g''\geq0$），而 $h$ 为凸函数且非减（所以 $h''\geq0$ 且 $h'\geq0$）。由 (3.9) 可得 $f''\geq0$，即 $f$ 为凸函数。用类似的方法，由表达式 (3.9) 可以得到以下结论：

$$
\begin{aligned}
&f\text{ 为凸函数，若 }h\text{ 为凸函数且非减，}g\text{ 为凸函数；}\\
&f\text{ 为凸函数，若 }h\text{ 为凸函数且非增，}g\text{ 为凹函数；}\\
&f\text{ 为凹函数，若 }h\text{ 为凹函数且非减，}g\text{ 为凹函数；}\\
&f\text{ 为凹函数，若 }h\text{ 为凹函数且非增，}g\text{ 为凸函数。}
\end{aligned}
\tag{3.10}
$$

这些结论在 $g$ 和 $h$ 都二阶可微、定义域都是整个 $\mathbf{R}$ 时成立。事实上，在一般的 $n>1$ 情形下，即使不假设 $h$ 和 $g$ 可微，也不假设 $\operatorname{\mathbf{dom}}g=\mathbf{R}^n$、$\operatorname{\mathbf{dom}}h=\mathbf{R}$，仍有非常相似的复合规则：

$$
\begin{aligned}
&f\text{ 为凸函数，若 }h\text{ 为凸函数，}\widetilde h\text{ 非减，}g\text{ 为凸函数；}\\
&f\text{ 为凸函数，若 }h\text{ 为凸函数，}\widetilde h\text{ 非增，}g\text{ 为凹函数；}\\
&f\text{ 为凹函数，若 }h\text{ 为凹函数，}\widetilde h\text{ 非减，}g\text{ 为凹函数；}\\
&f\text{ 为凹函数，若 }h\text{ 为凹函数，}\widetilde h\text{ 非增，}g\text{ 为凸函数。}
\end{aligned}
\tag{3.11}
$$

这里 $\widetilde h$ 表示函数 $h$ 的扩展值延拓：当 $h$ 为凸（凹）函数时，它把不属于 $\operatorname{\mathbf{dom}}h$ 的点的函数值设为 $\infty$（$-\infty$）。这些结论与 (3.10) 的唯一区别在于，我们要求扩展值延拓函数 $\widetilde h$ 在整个 $\mathbf{R}$ 上非增或非减。

为理解这意味着什么，假设 $h$ 是凸函数，所以 $\widetilde h$ 在 $\operatorname{\mathbf{dom}}h$ 之外取值为 $\infty$。$\widetilde h$ 非减，是指对于任意满足 $x<y$ 的 $x,y\in\mathbf{R}$，都有 $\widetilde h(x)\leq\widetilde h(y)$。特别地，这意味着如果 $y\in\operatorname{\mathbf{dom}}h$，那么 $x\in\operatorname{\mathbf{dom}}h$。换句话说，$h$ 的定义域沿负方向无限延伸；它要么是 $\mathbf{R}$，要么是形如 $(-\infty,a)$ 或 $(-\infty,a]$ 的区间。类似地，$h$ 为凸函数且 $\widetilde h$ 非增，意味着 $h$ 非增，而且 $\operatorname{\mathbf{dom}}h$ 沿正方向无限延伸。图 3.7 说明了这一点。

<div class="example" markdown="1">

**例 3.12** 下面几个简单例子说明复合定理中对 $h$ 的要求。

- 函数 $h(x)=\log x$，$\operatorname{\mathbf{dom}}h=\mathbf{R}_{++}$，是凹函数，而且满足 $\widetilde h$ 非减。
- <!-- pdf-page: 99 -->函数 $h(x)=x^{1/2}$，$\operatorname{\mathbf{dom}}h=\mathbf{R}_+$，是凹函数，而且满足 $\widetilde h$ 非减这一条件。
- 函数 $h(x)=x^{3/2}$，$\operatorname{\mathbf{dom}}h=\mathbf{R}_+$，是凸函数，但不满足 $\widetilde h$ 非减这一条件。例如，$\widetilde h(-1)=\infty$，而 $\widetilde h(1)=1$。
- 函数 $h$ 在 $x\geq0$ 时定义为 $h(x)=x^{3/2}$，在 $x<0$ 时定义为 $h(x)=0$，其定义域为 $\operatorname{\mathbf{dom}}h=\mathbf{R}$。它是凸函数，并且满足 $\widetilde h$ 非减这一条件。

</div>

<figure id="fig-3-7" data-figure="3.7">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-7.png" alt="左右两幅图比较定义域限于非负半轴的平方函数，与负半轴上取零的函数的上图" data-source-page="99" data-source-rect="120,121,454,260">
<figcaption>图 3.7 左：定义域为 $\mathbf{R}_+$ 的函数 $x^2$ 在其定义域上是凸且非减的，但它的扩展值延拓不是非减的。右：定义域为 $\mathbf{R}$ 的函数 $\max\{x,0\}^2$ 是凸函数，其扩展值延拓是非减的。</figcaption>
<p class="figure-translation">图内文字：两幅图中的 $\operatorname{\mathbf{epi}}f$ 均表示各自函数 $f$ 的上图。</p>
</figure>

复合结论 (3.11) 可以直接证明，无须假设可微性，也无须使用公式 (3.9)。作为例子，我们证明以下复合定理：如果 $g$ 是凸函数，$h$ 是凸函数，且 $\widetilde h$ 非减，那么 $f=h\circ g$ 是凸函数。设 $x,y\in\operatorname{\mathbf{dom}}f$，且 $0\leq\theta\leq1$。由于 $x,y\in\operatorname{\mathbf{dom}}f$，所以 $x,y\in\operatorname{\mathbf{dom}}g$，并且 $g(x),g(y)\in\operatorname{\mathbf{dom}}h$。由于 $\operatorname{\mathbf{dom}}g$ 是凸集，可得 $\theta x+(1-\theta)y\in\operatorname{\mathbf{dom}}g$；再由 $g$ 的凸性得到

$$
g(\theta x+(1-\theta)y)\leq\theta g(x)+(1-\theta)g(y).
\tag{3.12}
$$

由于 $g(x),g(y)\in\operatorname{\mathbf{dom}}h$，所以 $\theta g(x)+(1-\theta)g(y)\in\operatorname{\mathbf{dom}}h$，即 (3.12) 的右端属于 $\operatorname{\mathbf{dom}}h$。现在使用 $\widetilde h$ 非减这一假设，它意味着 $h$ 的定义域沿负方向无限延伸。由于 (3.12) 的右端属于 $\operatorname{\mathbf{dom}}h$，可知左端，即 $g(\theta x+(1-\theta)y)$，也属于 $\operatorname{\mathbf{dom}}h$。这意味着 $\theta x+(1-\theta)y\in\operatorname{\mathbf{dom}}f$。到这里，已经证明 $\operatorname{\mathbf{dom}}f$ 是凸集。

现在利用 $\widetilde h$ 非减及不等式 (3.12)，得到

$$
h(g(\theta x+(1-\theta)y))\leq h(\theta g(x)+(1-\theta)g(y)).
\tag{3.13}
$$

由 $h$ 的凸性，得到

$$
h(\theta g(x)+(1-\theta)g(y))\leq\theta h(g(x))+(1-\theta)h(g(y)).
\tag{3.14}
$$

<!-- pdf-page: 100 -->

把 (3.13) 和 (3.14) 合起来，得到

$$
h(g(\theta x+(1-\theta)y))\leq\theta h(g(x))+(1-\theta)h(g(y)),
$$

这就证明了复合定理。

<div class="example" markdown="1">

**例 3.13 简单的复合结论。**

- 如果 $g$ 是凸函数，那么 $\exp g(x)$ 是凸函数。
- 如果 $g$ 是凹函数且取正值，那么 $\log g(x)$ 是凹函数。
- 如果 $g$ 是凹函数且取正值，那么 $1/g(x)$ 是凸函数。
- 如果 $g$ 是非负凸函数且 $p\geq1$，那么 $g(x)^p$ 是凸函数。
- 如果 $g$ 是凸函数，那么 $-\log(-g(x))$ 在 $\{x\mid g(x)<0\}$ 上为凸函数。

</div>

<div class="remark" markdown="1">

**注 3.3** 单调性必须对扩展值延拓 $\widetilde h$ 成立，仅对函数 $h$ 成立还不够，这一要求不能省去。例如，考虑函数 $g(x)=x^2$，$\operatorname{\mathbf{dom}}g=\mathbf{R}$，以及 $h(x)=0$，$\operatorname{\mathbf{dom}}h=[1,2]$。这里 $g$ 是凸函数，$h$ 是凸函数且非减。但是函数 $f=h\circ g$，即

$$
f(x)=0,\qquad\operatorname{\mathbf{dom}}f=[-\sqrt2,-1]\cup[1,\sqrt2],
$$

不是凸函数，因为它的定义域不是凸集。当然，这里的函数 $\widetilde h$ 并非非减。

</div>

#### 向量复合

下面转向更复杂的 $k\geq1$ 情形。设

$$
f(x)=h(g(x))=h(g_1(x),\ldots,g_k(x)),
$$

其中 $h:\mathbf{R}^k\to\mathbf{R}$、$g_i:\mathbf{R}^n\to\mathbf{R}$。同样，不失一般性，可以假设 $n=1$。和 $k=1$ 的情形一样，为了找出复合规则，先假设这些函数二阶可微，并且 $\operatorname{\mathbf{dom}}g=\mathbf{R}$、$\operatorname{\mathbf{dom}}h=\mathbf{R}^k$。有

$$
f''(x)=g'(x)^T\nabla^2h(g(x))g'(x)+\nabla h(g(x))^Tg''(x),
\tag{3.15}
$$

这是 (3.9) 的向量形式。同样，问题在于确定什么条件能保证对所有 $x$ 都有 $f''(x)\geq0$，或者在考察凹性时，对所有 $x$ 都有 $f''(x)\leq0$。从 (3.15) 可以推导出许多规则，例如：

- 如果 $h$ 是凸函数，并且对每个自变量都非减，且各个 $g_i$ 都是凸函数，那么 $f$ 是凸函数。
- 如果 $h$ 是凸函数，并且对每个自变量都非增，且各个 $g_i$ 都是凹函数，那么 $f$ 是凸函数。
- 如果 $h$ 是凹函数，并且对每个自变量都非减，且各个 $g_i$ 都是凹函数，那么 $f$ 是凹函数。

<!-- pdf-page: 101 -->

和标量情形一样，在一般情形下，即 $n>1$、不假设 $h$ 或 $g$ 可微、且定义域可以是一般集合时，也有类似的复合结论。对于这些一般结论，$h$ 的单调性条件必须对扩展值延拓 $\widetilde h$ 成立。

为理解扩展值延拓 $\widetilde h$ 满足单调性这一条件的含义，考虑 $h:\mathbf{R}^k\to\mathbf{R}$ 为凸函数、$\widetilde h$ 非减的情形，即只要 $u\preceq v$，就有 $\widetilde h(u)\leq\widetilde h(v)$。这意味着，如果 $v\in\operatorname{\mathbf{dom}}h$，那么 $u$ 也属于 $\operatorname{\mathbf{dom}}h$：$h$ 的定义域必须沿 $-\mathbf{R}_+^k$ 中的方向无限延伸。可以简洁地写为 $\operatorname{\mathbf{dom}}h-\mathbf{R}_+^k=\operatorname{\mathbf{dom}}h$。

<div class="example" markdown="1">

**例 3.14 向量复合的例子。**

- 令 $h(z)=z_{[1]}+\cdots+z_{[r]}$，即 $z\in\mathbf{R}^k$ 中最大的 $r$ 个分量之和。那么 $h$ 是凸函数，并且对每个自变量都非减。设 $g_1,\ldots,g_k$ 是 $\mathbf{R}^n$ 上的凸函数。那么复合函数 $f=h\circ g$，也就是逐点取最大的 $r$ 个 $g_i$ 再求和所得的函数，是凸函数。
- 函数 $h(z)=\log(\sum_{i=1}^k e^{z_i})$ 是凸函数，并且对每个自变量都非减，所以只要各个 $g_i$ 都是凸函数，$\log(\sum_{i=1}^k e^{g_i})$ 就是凸函数。
- 当 $0<p\leq1$ 时，$\mathbf{R}_+^k$ 上的函数 $h(z)=(\sum_{i=1}^k z_i^p)^{1/p}$ 是凹函数，而且它的延拓（在 $z\not\succeq0$ 时取值为 $-\infty$）对每个分量都非减。因此，如果各个 $g_i$ 都是非负凹函数，就可以得出 $f(x)=(\sum_{i=1}^k g_i(x)^p)^{1/p}$ 是凹函数。
- 设 $p\geq1$，且 $g_1,\ldots,g_k$ 都是非负凸函数。那么函数 $(\sum_{i=1}^k g_i(x)^p)^{1/p}$ 是凸函数。

    为说明这一点，考虑函数 $h:\mathbf{R}^k\to\mathbf{R}$，定义为

    $$
    h(z)=\left(\sum_{i=1}^k\max\{z_i,0\}^p\right)^{1/p},
    $$

    其定义域为 $\operatorname{\mathbf{dom}}h=\mathbf{R}^k$，因此 $h=\widetilde h$。这个函数是凸函数且非减，所以 $h(g(x))$ 是 $x$ 的凸函数。当 $z\succeq0$ 时，有 $h(z)=(\sum_{i=1}^k z_i^p)^{1/p}$，因此可以得出 $(\sum_{i=1}^k g_i(x)^p)^{1/p}$ 是凸函数。

- $\mathbf{R}_+^k$ 上的几何平均 $h(z)=(\prod_{i=1}^k z_i)^{1/k}$ 是凹函数，而且它的延拓对每个自变量都非减。因此，如果 $g_1,\ldots,g_k$ 都是非负凹函数，那么它们的几何平均 $(\prod_{i=1}^k g_i)^{1/k}$ 也是非负凹函数。

</div>

### 3.2.5 最小化

前面已经看到，任意一族凸函数的最大值或上确界仍为凸函数。事实上，某些特殊形式的最小化也会得到凸函数。如果 $f$ 关于 $(x,y)$ 是凸函数，且 $C$ 是非空凸集，那么函数

$$
g(x)=\inf_{y\in C}f(x,y)
\tag{3.16}
$$

<!-- pdf-page: 102 -->

关于 $x$ 是凸函数，只要对所有 $x$ 都有 $g(x)>-\infty$。$g$ 的定义域是 $\operatorname{\mathbf{dom}}f$ 在 $x$ 坐标上的投影，即

$$
\operatorname{\mathbf{dom}}g=\{x\mid\text{存在 }y\in C\text{ 使 }(x,y)\in\operatorname{\mathbf{dom}}f\}.
$$

我们通过对 $x_1,x_2\in\operatorname{\mathbf{dom}}g$ 验证 Jensen 不等式来证明这一点。设 $\epsilon>0$。那么存在 $y_1,y_2\in C$，使得对 $i=1,2$，都有 $f(x_i,y_i)\leq g(x_i)+\epsilon$。取 $\theta\in[0,1]$，则

$$
\begin{aligned}
g(\theta x_1+(1-\theta)x_2)&=\inf_{y\in C}f(\theta x_1+(1-\theta)x_2,y)\\
&\leq f(\theta x_1+(1-\theta)x_2,\theta y_1+(1-\theta)y_2)\\
&\leq\theta f(x_1,y_1)+(1-\theta)f(x_2,y_2)\\
&\leq\theta g(x_1)+(1-\theta)g(x_2)+\epsilon.
\end{aligned}
$$

由于这对任意 $\epsilon>0$ 都成立，所以

$$
g(\theta x_1+(1-\theta)x_2)\leq\theta g(x_1)+(1-\theta)g(x_2).
$$

也可以从上图来看这一结论。对于 (3.16) 中的 $f$、$g$ 和 $C$，假设对每个 $x$，在 $y\in C$ 上的下确界都能取到，则有

$$
\operatorname{\mathbf{epi}}g=\{(x,t)\mid\text{存在 }y\in C\text{ 使 }(x,y,t)\in\operatorname{\mathbf{epi}}f\}.
$$

所以 $\operatorname{\mathbf{epi}}g$ 是凸集，因为它是一个凸集在部分坐标上的投影。

<div class="example" markdown="1">

**例 3.15 Schur 补。** 假设二次函数

$$
f(x,y)=x^TAx+2x^TBy+y^TCy
$$

（其中 $A$ 和 $C$ 对称）关于 $(x,y)$ 是凸函数，这意味着

$$
\begin{bmatrix}A&B\\B^T&C\end{bmatrix}\succeq0.
$$

可以把 $g(x)=\inf_y f(x,y)$ 写成

$$
g(x)=x^T(A-BC^\dagger B^T)x,
$$

其中 $C^\dagger$ 是 $C$ 的伪逆，见第 A.5.4 节。由最小化规则，$g$ 是凸函数，因此可得 $A-BC^\dagger B^T\succeq0$。

如果 $C$ 可逆，即 $C\succ0$，那么矩阵 $A-BC^{-1}B^T$ 称为 $C$ 在矩阵

$$
\begin{bmatrix}A&B\\B^T&C\end{bmatrix}
$$

中的 **Schur 补**，见第 A.5.5 节。

</div>

<div class="example" markdown="1">

**例 3.16 到集合的距离。** 在范数 $\|\cdot\|$ 下，点 $x$ 到集合 $S\subseteq\mathbf{R}^n$ 的距离定义为

$$
\operatorname{\mathbf{dist}}(x,S)=\inf_{y\in S}\|x-y\|.
$$

函数 $\|x-y\|$ 关于 $(x,y)$ 是凸函数，所以如果集合 $S$ 是凸集，距离函数 $\operatorname{\mathbf{dist}}(x,S)$ 就是 $x$ 的凸函数。

</div>

<!-- pdf-page: 103 -->

<div class="example" markdown="1">

**例 3.17** 假设 $h$ 是凸函数。那么由

$$
g(x)=\inf\{h(y)\mid Ay=x\}
$$

定义的函数 $g$ 是凸函数。为说明这一点，定义 $f$ 为

$$
f(x,y)=\begin{cases}
h(y)&\text{若 }Ay=x\\
\infty&\text{否则},
\end{cases}
$$

它关于 $(x,y)$ 是凸函数。此时 $g$ 是 $f$ 关于 $y$ 的最小值，因此是凸函数。（直接证明 $g$ 的凸性也不难。）

</div>

### 3.2.6 函数的透视

如果 $f:\mathbf{R}^n\to\mathbf{R}$，那么 $f$ 的**透视函数**（perspective）是函数 $g:\mathbf{R}^{n+1}\to\mathbf{R}$，定义为

$$
g(x,t)=tf(x/t),
$$

其定义域为

$$
\operatorname{\mathbf{dom}}g=\{(x,t)\mid x/t\in\operatorname{\mathbf{dom}}f,\ t>0\}.
$$

透视运算保持凸性：如果 $f$ 是凸函数，那么它的透视函数 $g$ 也是凸函数。类似地，如果 $f$ 是凹函数，那么 $g$ 也是凹函数。

这一点有多种证明方法，例如直接验证定义凸性的不等式，见习题 3.33。这里利用上图及第 2.3.3 节介绍的 $\mathbf{R}^{n+1}$ 上的透视映射，给出一个简短证明，这也将解释“透视”这一名称。当 $t>0$ 时，有

$$
\begin{aligned}
(x,t,s)\in\operatorname{\mathbf{epi}}g&\quad\Longleftrightarrow\quad tf(x/t)\leq s\\
&\quad\Longleftrightarrow\quad f(x/t)\leq s/t\\
&\quad\Longleftrightarrow\quad(x/t,s/t)\in\operatorname{\mathbf{epi}}f.
\end{aligned}
$$

因此，$\operatorname{\mathbf{epi}}g$ 是 $\operatorname{\mathbf{epi}}f$ 在把 $(u,v,w)$ 映到 $(u,w)/v$ 的透视映射下的原像。于是由第 2.3.3 节可知，$\operatorname{\mathbf{epi}}g$ 是凸集，所以函数 $g$ 是凸函数。

<div class="example" markdown="1">

**例 3.18 欧几里得范数的平方。** $\mathbf{R}^n$ 上凸函数 $f(x)=x^Tx$ 的透视函数是

$$
g(x,t)=t(x/t)^T(x/t)=\frac{x^Tx}{t},
$$

当 $t>0$ 时，它关于 $(x,t)$ 是凸函数。

还可以用其他几种方法推导 $g$ 的凸性。首先，可以把 $g$ 表示成二次除以线性函数 $x_i^2/t$ 的和，这些函数的凸性已在第 3.1.5 节证明。也可以把 $g$ 写成 $x^T(tI)^{-1}x$，将它看作矩阵分式函数的特殊情况，见例 3.4。

</div>

<!-- pdf-page: 104 -->

<div class="example" markdown="1">

**例 3.19 负对数。** 考虑 $\mathbf{R}_{++}$ 上的凸函数 $f(x)=-\log x$。它的透视函数为

$$
g(x,t)=-t\log(x/t)=t\log(t/x)=t\log t-t\log x,
$$

在 $\mathbf{R}_{++}^2$ 上为凸函数。函数 $g$ 称为 $t$ 与 $x$ 的**相对熵**（relative entropy）。当 $x=1$ 时，$g$ 化为负熵函数。

由 $g$ 的凸性，可以证明几个有意思的相关函数的凸性或凹性。首先，两个向量 $u,v\in\mathbf{R}_{++}^n$ 的相对熵定义为

$$
\sum_{i=1}^n u_i\log(u_i/v_i),
$$

它关于 $(u,v)$ 是凸函数，因为它是各对 $u_i,v_i$ 的相对熵之和。

一个紧密相关的函数是 $u,v\in\mathbf{R}_{++}^n$ 之间的 **Kullback–Leibler 散度**，即

$$
D_{\mathrm{kl}}(u,v)=\sum_{i=1}^n\left(u_i\log(u_i/v_i)-u_i+v_i\right),
\tag{3.17}
$$

它是凸函数，因为它是在相对熵上加了一个关于 $(u,v)$ 的线性函数。Kullback–Leibler 散度满足 $D_{\mathrm{kl}}(u,v)\geq0$，并且 $D_{\mathrm{kl}}(u,v)=0$ 当且仅当 $u=v$，因此可以用来度量两个正向量之间的偏离程度，见习题 3.13。（注意，当 $u$ 和 $v$ 是概率向量，即满足 $\mathbf{1}^Tu=\mathbf{1}^Tv=1$ 时，相对熵与 Kullback–Leibler 散度相同。）

在相对熵函数中取 $v_i=\mathbf{1}^Tu$，可以得到关于 $u\in\mathbf{R}_{++}^n$ 的凹函数（同时也是齐次函数）

$$
\sum_{i=1}^n u_i\log(\mathbf{1}^Tu/u_i)=(\mathbf{1}^Tu)\sum_{i=1}^n z_i\log(1/z_i),
$$

其中 $z=u/(\mathbf{1}^Tu)$。它称为**归一化熵函数**（normalized entropy function）。向量 $z=u/\mathbf{1}^Tu$ 是一个归一化向量，也就是概率分布，因为它的各分量之和为 1；$u$ 的归一化熵等于这个归一化分布的熵乘以 $\mathbf{1}^Tu$。

</div>

<div class="example" markdown="1">

**例 3.20** 假设 $f:\mathbf{R}^m\to\mathbf{R}$ 是凸函数，$A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$c\in\mathbf{R}^n$、$d\in\mathbf{R}$。定义

$$
g(x)=(c^Tx+d)f\left((Ax+b)/(c^Tx+d)\right),
$$

其定义域为

$$
\operatorname{\mathbf{dom}}g=\{x\mid c^Tx+d>0,\ (Ax+b)/(c^Tx+d)\in\operatorname{\mathbf{dom}}f\}.
$$

那么 $g$ 是凸函数。

</div>

## 3.3 共轭函数

本节介绍一种将在后续章节中发挥重要作用的运算。

<!-- pdf-page: 105 -->

<figure id="fig-3-8" data-figure="3.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-8.png" alt="函数曲线与两条斜率相同的虚线，一条经过原点，另一条与曲线相切并标出纵轴截距" data-source-page="105" data-source-rect="194,121,385,266">
<figcaption>图 3.8 函数 $f:\mathbf{R}\to\mathbf{R}$，以及一个值 $y\in\mathbf{R}$。共轭函数 $f^*(y)$ 是线性函数 $yx$ 与 $f(x)$ 之间的最大差值，如图中的虚线所示。如果 $f$ 可微，这个最大差值在满足 $f'(x)=y$ 的点 $x$ 处取得。</figcaption>
</figure>

### 3.3.1 定义与例子

设 $f:\mathbf{R}^n\to\mathbf{R}$。由

$$
f^*(y)=\sup_{x\in\operatorname{\mathbf{dom}}f}\left(y^Tx-f(x)\right)
\tag{3.18}
$$

定义的函数 $f^*:\mathbf{R}^n\to\mathbf{R}$，称为函数 $f$ 的**共轭函数**（conjugate）。共轭函数的定义域，由使上确界有限的 $y\in\mathbf{R}^n$ 构成，也就是使差值 $y^Tx-f(x)$ 在 $\operatorname{\mathbf{dom}}f$ 上有上界的那些 $y$。图 3.8 展示了这个定义。

立即可以看出，$f^*$ 是凸函数，因为它是一族关于 $y$ 的凸函数（实际上是仿射函数）的逐点上确界。无论 $f$ 是否为凸函数，这一点都成立。（注意，当 $f$ 为凸函数时，下标 $x\in\operatorname{\mathbf{dom}}f$ 可以省去，因为按照约定，当 $x\notin\operatorname{\mathbf{dom}}f$ 时，$y^Tx-f(x)=-\infty$。）

我们先给出几个简单例子，再介绍求函数共轭的一些规则。借助这些规则，可以推导出许多常见凸函数的共轭函数的解析表达式。

<div class="example" markdown="1">

**例 3.21** 下面推导 $\mathbf{R}$ 上一些凸函数的共轭函数。

- **仿射函数。** $f(x)=ax+b$。作为 $x$ 的函数，$yx-ax-b$ 有界当且仅当 $y=a$，此时它为常数。因此，共轭函数 $f^*$ 的定义域是单点集 $\{a\}$，且 $f^*(a)=-b$。
- **负对数。** $f(x)=-\log x$，$\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}$。当 $y\geq0$ 时，函数 $xy+\log x$ 无上界；否则，它在 $x=-1/y$ 处取得最大值。因此，$\operatorname{\mathbf{dom}}f^*=\{y\mid y<0\}=-\mathbf{R}_{++}$，并且当 $y<0$ 时，$f^*(y)=-\log(-y)-1$。
- **指数函数。** $f(x)=e^x$。当 $y<0$ 时，$xy-e^x$ 无界。当 $y>0$ 时，$xy-e^x$ 在 $x=\log y$ 处取得最大值，所以 $f^*(y)=y\log y-y$。当 $y=0$ 时，<!-- pdf-page: 106 -->$f^*(y)=\sup_x(-e^x)=0$。总之，$\operatorname{\mathbf{dom}}f^*=\mathbf{R}_+$，$f^*(y)=y\log y-y$，其中把 $0\log0$ 理解为 0。
- **负熵。** $f(x)=x\log x$，$\operatorname{\mathbf{dom}}f=\mathbf{R}_+$，且 $f(0)=0$。对于所有 $y$，函数 $xy-x\log x$ 在 $\mathbf{R}_+$ 上都有上界，因此 $\operatorname{\mathbf{dom}}f^*=\mathbf{R}$。它在 $x=e^{y-1}$ 处取得最大值，代入可得 $f^*(y)=e^{y-1}$。
- **倒数。** $f(x)=1/x$，定义在 $\mathbf{R}_{++}$ 上。当 $y>0$ 时，$yx-1/x$ 无上界。当 $y=0$ 时，这个函数的上确界为 0；当 $y<0$ 时，上确界在 $x=(-y)^{-1/2}$ 处取得。因此，$f^*(y)=-2(-y)^{1/2}$，$\operatorname{\mathbf{dom}}f^*=-\mathbf{R}_+$。

</div>

<div class="example" markdown="1">

**例 3.22 严格凸二次函数。** 考虑 $f(x)=\tfrac12x^TQx$，其中 $Q\in\mathbf{S}_{++}^n$。对于所有 $y$，函数 $y^Tx-\tfrac12x^TQx$ 作为 $x$ 的函数都有上界。它在 $x=Q^{-1}y$ 处取得最大值，因此

$$
f^*(y)=\frac12y^TQ^{-1}y.
$$

</div>

<div class="example" markdown="1">

**例 3.23 对数行列式。** 考虑 $\mathbf{S}_{++}^n$ 上的函数 $f(X)=\log\det X^{-1}$。它的共轭函数定义为

$$
f^*(Y)=\sup_{X\succ0}\left(\operatorname{\mathbf{tr}}(YX)+\log\det X\right),
$$

因为 $\operatorname{\mathbf{tr}}(YX)$ 是 $\mathbf{S}^n$ 上的标准内积。先证明，除非 $Y\prec0$，否则 $\operatorname{\mathbf{tr}}(YX)+\log\det X$ 无上界。如果 $Y\not\prec0$，那么 $Y$ 有一个满足 $\|v\|_2=1$ 的特征向量 $v$，对应的特征值 $\lambda\geq0$。取 $X=I+tvv^T$，得到

$$
\operatorname{\mathbf{tr}}(YX)+\log\det X
=\operatorname{\mathbf{tr}}Y+t\lambda+\log\det(I+tvv^T)
=\operatorname{\mathbf{tr}}Y+t\lambda+\log(1+t),
$$

当 $t\to\infty$ 时，它无上界。

再考虑 $Y\prec0$ 的情形。令关于 $X$ 的梯度为零，就能找到使函数最大的 $X$：

$$
\nabla_X\left(\operatorname{\mathbf{tr}}(YX)+\log\det X\right)=Y+X^{-1}=0
$$

（见第 A.4.1 节），得到 $X=-Y^{-1}$，这个矩阵确实正定。因此

$$
f^*(Y)=\log\det(-Y)^{-1}-n,
$$

其中 $\operatorname{\mathbf{dom}}f^*=-\mathbf{S}_{++}^n$。

</div>

<div class="example" markdown="1">

**例 3.24 指示函数。** 设 $I_S$ 是集合 $S\subseteq\mathbf{R}^n$（不要求为凸集）的指示函数，即在 $\operatorname{\mathbf{dom}}I_S=S$ 上有 $I_S(x)=0$。它的共轭函数为

$$
I_S^*(y)=\sup_{x\in S}y^Tx,
$$

这正是集合 $S$ 的支撑函数。

</div>

<!-- pdf-page: 107 -->

<div class="example" markdown="1">

**例 3.25 指数和的对数函数。** 为推导指数和的对数函数 $f(x)=\log(\sum_{i=1}^n e^{x_i})$ 的共轭函数，先确定哪些 $y$ 能使 $y^Tx-f(x)$ 关于 $x$ 的最大值被取到。令关于 $x$ 的梯度为零，得到条件

$$
y_i=\frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}},\qquad i=1,\ldots,n.
$$

这些方程对于 $x$ 有解，当且仅当 $y\succ0$ 且 $\mathbf{1}^Ty=1$。把 $y_i$ 的表达式代入 $y^Tx-f(x)$，得到 $f^*(y)=\sum_{i=1}^n y_i\log y_i$。如果 $y$ 的某些分量为零，只要 $y\succeq0$、$\mathbf{1}^Ty=1$，并且把 $0\log0$ 理解为 0，这个 $f^*$ 的表达式仍然正确。

事实上，$f^*$ 的定义域恰好由 $\mathbf{1}^Ty=1$、$y\succeq0$ 给出。为说明这一点，假设 $y$ 的某个分量为负，例如 $y_k<0$。取 $x_k=-t$，对 $i\ne k$ 取 $x_i=0$，再令 $t$ 趋于无穷，就可以说明 $y^Tx-f(x)$ 无上界。

如果 $y\succeq0$ 但 $\mathbf{1}^Ty\ne1$，取 $x=t\mathbf{1}$，则

$$
y^Tx-f(x)=t\mathbf{1}^Ty-t-\log n.
$$

如果 $\mathbf{1}^Ty>1$，当 $t\to\infty$ 时它无限增大；如果 $\mathbf{1}^Ty<1$，当 $t\to-\infty$ 时它无限增大。

总之，

$$
f^*(y)=\begin{cases}
\displaystyle\sum_{i=1}^n y_i\log y_i&\text{若 }y\succeq0\text{ 且 }\mathbf{1}^Ty=1\\
\infty&\text{否则}.
\end{cases}
$$

换句话说，指数和的对数函数的共轭，是限制在概率单纯形上的负熵函数。

</div>

<div class="example" markdown="1">

**例 3.26 范数。** 设 $\|\cdot\|$ 是 $\mathbf{R}^n$ 上的范数，其对偶范数为 $\|\cdot\|_*$。下面说明，$f(x)=\|x\|$ 的共轭函数为

$$
f^*(y)=\begin{cases}
0&\|y\|_*\leq1\\
\infty&\text{否则},
\end{cases}
$$

即范数的共轭函数是对偶范数单位球的指示函数。

如果 $\|y\|_*>1$，那么由对偶范数的定义，存在 $z\in\mathbf{R}^n$，满足 $\|z\|\leq1$ 且 $y^Tz>1$。取 $x=tz$ 并令 $t\to\infty$，则有

$$
y^Tx-\|x\|=t(y^Tz-\|z\|)\to\infty,
$$

这表明 $f^*(y)=\infty$。反过来，如果 $\|y\|_*\leq1$，那么对所有 $x$ 都有 $y^Tx\leq\|x\|\|y\|_*$，这意味着对所有 $x$ 都有 $y^Tx-\|x\|\leq0$。因此，$x=0$ 使 $y^Tx-\|x\|$ 取得最大值，最大值为 0。

</div>

<div class="example" markdown="1">

**例 3.27 范数的平方。** 现在考虑函数 $f(x)=(1/2)\|x\|^2$，其中 $\|\cdot\|$ 是范数，对偶范数为 $\|\cdot\|_*$。下面说明，它的共轭函数为 $f^*(y)=(1/2)\|y\|_*^2$。

由 $y^Tx\leq\|y\|_*\|x\|$ 可知，对所有 $x$，都有

$$
y^Tx-(1/2)\|x\|^2\leq\|y\|_*\|x\|-(1/2)\|x\|^2.
$$

<!-- pdf-page: 108 -->

右端是 $\|x\|$ 的二次函数，最大值为 $(1/2)\|y\|_*^2$。因此，对所有 $x$，都有

$$
y^Tx-(1/2)\|x\|^2\leq(1/2)\|y\|_*^2,
$$

这说明 $f^*(y)\leq(1/2)\|y\|_*^2$。

为证明另一个方向的不等式，任取满足 $y^Tx=\|y\|_*\|x\|$ 的向量 $x$，并对它作缩放，使 $\|x\|=\|y\|_*$。对这个 $x$，有

$$
y^Tx-(1/2)\|x\|^2=(1/2)\|y\|_*^2,
$$

这说明 $f^*(y)\geq(1/2)\|y\|_*^2$。

</div>

<div class="example" markdown="1">

**例 3.28 收入函数与利润函数。** 考虑一家消耗 $n$ 种资源、生产可出售产品的企业。用 $r=(r_1,\ldots,r_n)$ 表示消耗的各类资源的数量向量，用 $S(r)$ 表示所生产产品带来的销售收入，它是所耗资源的函数。令 $p_i$ 表示第 $i$ 种资源的单位价格，那么企业为资源支付的总额为 $p^Tr$。企业获得的利润就是 $S(r)-p^Tr$。现在固定资源价格，考察通过合理选择各类资源的使用量，最多能获得多少利润。这个最大利润为

$$
M(p)=\sup_r\left(S(r)-p^Tr\right).
$$

函数 $M(p)$ 给出了可获得的最大利润，它是资源价格的函数。用共轭函数可以把 $M$ 表示为

$$
M(p)=(-S)^*(-p).
$$

因此，最大利润（作为资源价格的函数）与总销售收入（作为所耗资源的函数）的共轭密切相关。

</div>

### 3.3.2 基本性质

#### Fenchel 不等式

由共轭函数的定义，立即得到：对所有 $x,y$，都有

$$
f(x)+f^*(y)\geq x^Ty.
$$

这称为 **Fenchel 不等式**（当 $f$ 可微时，也称为 **Young 不等式**）。

例如，取 $f(x)=(1/2)x^TQx$，其中 $Q\in\mathbf{S}_{++}^n$，就得到不等式

$$
x^Ty\leq(1/2)x^TQx+(1/2)y^TQ^{-1}y.
$$

#### 共轭函数的共轭

前面的例子以及“共轭”这一名称，都暗示凸函数的共轭再取共轭后会回到原函数。只要满足一个技术条件，事实确实如此：如果 $f$ 是凸函数，并且 $f$ 是闭的（即 $\operatorname{\mathbf{epi}}f$ 是闭集，见第 A.3.3 节），那么 $f^{**}=f$。例如，如果 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$，那么 $f^{**}=f$，即 $f$ 的共轭函数再取共轭，仍为 $f$，见习题 3.39。

<!-- pdf-page: 109 -->

#### 可微函数

可微函数 $f$ 的共轭函数也称为 $f$ 的 **Legendre 变换**。（为了把一般定义与可微情形区分开，有时用“Fenchel 共轭”代替“共轭”。）

设 $f$ 是可微凸函数，且 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$。$y^Tx-f(x)$ 的任意最大点 $x^*$ 都满足 $y=\nabla f(x^*)$；反过来，如果 $x^*$ 满足 $y=\nabla f(x^*)$，那么 $x^*$ 就使 $y^Tx-f(x)$ 取得最大值。因此，如果 $y=\nabla f(x^*)$，就有

$$
f^*(y)=x^{*T}\nabla f(x^*)-f(x^*).
$$

所以，对于任何能从梯度方程 $y=\nabla f(z)$ 中求出 $z$ 的 $y$，都可以确定 $f^*(y)$。

还可以换一种方式表述。任取 $z\in\mathbf{R}^n$，并定义 $y=\nabla f(z)$，则有

$$
f^*(y)=z^T\nabla f(z)-f(z).
$$

#### 缩放及与仿射变换复合

当 $a>0$、$b\in\mathbf{R}$ 时，$g(x)=af(x)+b$ 的共轭函数为 $g^*(y)=af^*(y/a)-b$。

设 $A\in\mathbf{R}^{n\times n}$ 非奇异，且 $b\in\mathbf{R}^n$。那么 $g(x)=f(Ax+b)$ 的共轭函数为

$$
g^*(y)=f^*(A^{-T}y)-b^TA^{-T}y,
$$

其定义域为 $\operatorname{\mathbf{dom}}g^*=A^T\operatorname{\mathbf{dom}}f^*$。

#### 独立函数的和

如果 $f(u,v)=f_1(u)+f_2(v)$，其中 $f_1$ 和 $f_2$ 都是凸函数，共轭函数分别为 $f_1^*$ 和 $f_2^*$，那么

$$
f^*(w,z)=f_1^*(w)+f_2^*(z).
$$

换句话说，独立凸函数之和的共轭，等于它们各自共轭函数之和。（“独立”是指这些函数依赖不同的变量。）

## 3.4 拟凸函数

### 3.4.1 定义与例子

如果函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的定义域以及对所有 $\alpha\in\mathbf{R}$ 定义的下水平集

$$
S_\alpha=\{x\in\operatorname{\mathbf{dom}}f\mid f(x)\leq\alpha\}
$$

都是凸集，就称 $f$ 是**拟凸函数**（quasiconvex），也称**单峰函数**（unimodal）。如果 $-f$ 是拟凸函数，即每个上水平集 $\{x\mid f(x)\geq\alpha\}$ 都是凸集，就称 $f$ 是**拟凹函数**（quasiconcave）。既拟凸又拟凹的函数称为**拟线性函数**（quasilinear）。如果函数 $f$ 是拟线性的，那么它的定义域以及每个水平集 $\{x\mid f(x)=\alpha\}$ 都是凸集。

<!-- pdf-page: 110 -->

<figure id="fig-3-9" data-figure="3.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-9.png" alt="一维拟凸函数的曲线，两条水平虚线对应两个下水平集，横轴上标出三个端点" data-source-page="110" data-source-rect="222,121,449,269">
<figcaption>图 3.9 $\mathbf{R}$ 上的一个拟凸函数。对每个 $\alpha$，$\alpha$-下水平集 $S_\alpha$ 都是凸集，即一个区间。下水平集 $S_\alpha$ 是区间 $[a,b]$。下水平集 $S_\beta$ 是区间 $(-\infty,c]$。</figcaption>
</figure>

对于 $\mathbf{R}$ 上的函数，拟凸性要求每个下水平集都是一个区间，也可能是无穷区间。图 3.9 给出了 $\mathbf{R}$ 上拟凸函数的一个例子。

凸函数的下水平集是凸集，因此凸函数都是拟凸函数。但一些简单例子，例如图 3.9 中的例子，表明逆命题不成立。

<div class="example" markdown="1">

**例 3.29** $\mathbf{R}$ 上的几个例子：

- **对数函数。** $\mathbf{R}_{++}$ 上的 $\log x$ 是拟凸函数，也是拟凹函数，因而是拟线性函数。
- **向上取整函数。** $\operatorname{ceil}(x)=\inf\{z\in\mathbf{Z}\mid z\geq x\}$ 是拟凸函数，也是拟凹函数。

</div>

这些例子表明，拟凸函数可以是凹函数，也可以是不连续函数。下面给出 $\mathbf{R}^n$ 上的几个例子。

<div class="example" markdown="1">

**例 3.30 向量的长度。** 将 $x\in\mathbf{R}^n$ 的长度定义为非零分量的最大下标，即

$$
f(x)=\max\{i\mid x_i\ne0\}.
$$

（把零向量的长度定义为零。）这个函数在 $\mathbf{R}^n$ 上为拟凸函数，因为它的下水平集是子空间：

$$
f(x)\leq\alpha\quad\Longleftrightarrow\quad x_i=0\quad\text{对 }i=\lfloor\alpha\rfloor+1,\ldots,n.
$$

</div>

<div class="example" markdown="1">

**例 3.31** 考虑 $f:\mathbf{R}^2\to\mathbf{R}$，$\operatorname{\mathbf{dom}}f=\mathbf{R}_+^2$，$f(x_1,x_2)=x_1x_2$。这个函数既不是凸函数，也不是凹函数，因为它的 Hessian 矩阵

$$
\nabla^2f(x)=\begin{bmatrix}0&1\\1&0\end{bmatrix}
$$

<!-- pdf-page: 111 -->

是不定的，它有一个正特征值和一个负特征值。不过，函数 $f$ 是拟凹函数，因为对所有 $\alpha$，上水平集

$$
\{x\in\mathbf{R}_+^2\mid x_1x_2\geq\alpha\}
$$

都是凸集。（但注意，$f$ 在 $\mathbf{R}^2$ 上不是拟凹函数。）

</div>

<div class="example" markdown="1">

**例 3.32 线性分式函数。** 函数

$$
f(x)=\frac{a^Tx+b}{c^Tx+d},
$$

其定义域为 $\operatorname{\mathbf{dom}}f=\{x\mid c^Tx+d>0\}$，既是拟凸函数，也是拟凹函数，即拟线性函数。它的 $\alpha$ 下水平集为

$$
\begin{aligned}
S_\alpha&=\{x\mid c^Tx+d>0,\ (a^Tx+b)/(c^Tx+d)\leq\alpha\}\\
&=\{x\mid c^Tx+d>0,\ a^Tx+b\leq\alpha(c^Tx+d)\},
\end{aligned}
$$

这是凸集，因为它是一个开半空间与一个闭半空间的交集。（用同样的方法也可以证明它的上水平集是凸集。）

</div>

<div class="example" markdown="1">

**例 3.33 距离比函数。** 设 $a,b\in\mathbf{R}^n$，定义

$$
f(x)=\frac{\|x-a\|_2}{\|x-b\|_2},
$$

即到 $a$ 的欧几里得距离与到 $b$ 的欧几里得距离之比。那么，$f$ 在半空间 $\{x\mid\|x-a\|_2\leq\|x-b\|_2\}$ 上为拟凸函数。为说明这一点，考察 $f$ 的 $\alpha$ 下水平集，其中 $\alpha\leq1$，因为在半空间 $\{x\mid\|x-a\|_2\leq\|x-b\|_2\}$ 上有 $f(x)\leq1$。这个下水平集由满足

$$
\|x-a\|_2\leq\alpha\|x-b\|_2
$$

的点构成。两边平方并整理各项，可知它等价于

$$
(1-\alpha^2)x^Tx-2(a-\alpha^2b)^Tx+a^Ta-\alpha^2b^Tb\leq0.
$$

当 $\alpha\leq1$ 时，这描述了一个凸集，实际上是一个欧几里得球。

</div>

<div class="example" markdown="1">

**例 3.34 内部收益率。** 用 $x=(x_0,x_1,\ldots,x_n)$ 表示 $n$ 个期间上的现金流序列，其中 $x_i>0$ 表示第 $i$ 期收到一笔款项，$x_i<0$ 表示第 $i$ 期支付一笔款项。在利率 $r\geq0$ 下，现金流的**现值**定义为

$$
\operatorname{PV}(x,r)=\sum_{i=0}^n(1+r)^{-i}x_i.
$$

（因子 $(1+r)^{-i}$ 是第 $i$ 期支付或收到款项的贴现因子。）

现在考虑满足 $x_0<0$ 且 $x_0+x_1+\cdots+x_n>0$ 的现金流。这意味着第 0 期先投入 $|x_0|$，而<!-- pdf-page: 112 -->剩余现金流的总和 $x_1+\cdots+x_n$（不考虑任何贴现因子）超过初始投资。

对于这样的现金流，$\operatorname{PV}(x,0)>0$，并且当 $r\to\infty$ 时，$\operatorname{PV}(x,r)\to x_0<0$，所以至少存在一个 $r\geq0$，使 $\operatorname{PV}(x,r)=0$。将现金流的**内部收益率**（internal rate of return）定义为使现值等于零的最小利率 $r\geq0$：

$$
\operatorname{IRR}(x)=\inf\{r\geq0\mid\operatorname{PV}(x,r)=0\}.
$$

内部收益率是 $x$ 的拟凹函数，其中 $x$ 限制在 $x_0<0$、$x_1+\cdots+x_n>0$ 的范围内。为说明这一点，注意到

$$
\operatorname{IRR}(x)\geq R\quad\Longleftrightarrow\quad\operatorname{PV}(x,r)>0\quad\text{对 }0\leq r<R.
$$

左端定义了 $\operatorname{IRR}$ 的 $R$ 上水平集。右端是由 $r$ 索引的一族集合 $\{x\mid\operatorname{PV}(x,r)>0\}$ 在 $0\leq r<R$ 范围内的交集。对于每个 $r$，$\operatorname{PV}(x,r)>0$ 定义了一个开半空间，所以右端定义的是凸集。

</div>

### 3.4.2 基本性质

前面的例子表明，拟凸性大幅推广了凸性。尽管如此，凸函数的许多性质对拟凸函数仍然成立，或者有相应的类似结论。例如，Jensen 不等式有一个变形，可以刻画拟凸性：函数 $f$ 是拟凸函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对任意 $x,y\in\operatorname{\mathbf{dom}}f$ 及 $0\leq\theta\leq1$，都有

$$
f(\theta x+(1-\theta)y)\leq\max\{f(x),f(y)\},
\tag{3.19}
$$

即函数在线段上的值不超过它在两个端点处函数值的较大者。不等式 (3.19) 有时称为**拟凸函数的 Jensen 不等式**，图 3.10 展示了它的含义。

<div class="example" markdown="1">

**例 3.35 非负向量的基数。** 向量 $x\in\mathbf{R}^n$ 的**基数**（cardinality）或**大小**（size），是其非零分量的个数，记为 $\operatorname{\mathbf{card}}(x)$。函数 $\operatorname{\mathbf{card}}$ 在 $\mathbf{R}_+^n$ 上为拟凹函数，但在 $\mathbf{R}^n$ 上不是。由下面对 $x,y\succeq0$ 成立的修正 Jensen 不等式，立即可以得到这一点：

$$
\operatorname{\mathbf{card}}(x+y)\geq\min\{\operatorname{\mathbf{card}}(x),\operatorname{\mathbf{card}}(y)\}.
$$

</div>

<div class="example" markdown="1">

**例 3.36 半正定矩阵的秩。** 函数 $\operatorname{\mathbf{rank}}X$ 在 $\mathbf{S}_+^n$ 上为拟凹函数。这来自修正的 Jensen 不等式 (3.19)：

$$
\operatorname{\mathbf{rank}}(X+Y)\geq\min\{\operatorname{\mathbf{rank}}X,\operatorname{\mathbf{rank}}Y\},
$$

该不等式对 $X,Y\in\mathbf{S}_+^n$ 成立。（这可以看作前一例的推广，因为当 $x\succeq0$ 时，$\operatorname{\mathbf{rank}}(\operatorname{\mathbf{diag}}(x))=\operatorname{\mathbf{card}}(x)$。）

</div>

<!-- pdf-page: 113 -->

<figure id="fig-3-10" data-figure="3.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-10.png" alt="拟凸函数的曲线，两点之间的函数值不超过两端函数值中的较大者" data-source-page="113" data-source-rect="193,121,400,255">
<figcaption>图 3.10 $\mathbf{R}$ 上的一个拟凸函数。$f$ 在 $x$ 与 $y$ 之间的值不超过 $\max\{f(x),f(y)\}$。</figcaption>
</figure>

和凸性一样，拟凸性也可以由函数 $f$ 在直线上的表现来刻画：$f$ 是拟凸函数，当且仅当把它限制在与其定义域相交的任意一条直线上时，得到的函数都是拟凸函数。特别地，可以把函数限制在任意一条直线上，再检查所得 $\mathbf{R}$ 上函数的拟凸性，来验证原函数的拟凸性。

#### $\mathbf{R}$ 上的拟凸函数

对于 $\mathbf{R}$ 上的拟凸函数，可以给出一个简单刻画。我们只考虑连续函数，因为一般情形下的条件表述起来较为繁琐。连续函数 $f:\mathbf{R}\to\mathbf{R}$ 是拟凸函数，当且仅当以下条件至少有一个成立：

- $f$ 非减。
- $f$ 非增。
- 存在一点 $c\in\operatorname{\mathbf{dom}}f$，使得当 $t\leq c$（且 $t\in\operatorname{\mathbf{dom}}f$）时，$f$ 非增；当 $t\geq c$（且 $t\in\operatorname{\mathbf{dom}}f$）时，$f$ 非减。

点 $c$ 可以取为 $f$ 的任意一个全局最小点。图 3.11 展示了这种情况。

### 3.4.3 可微拟凸函数

#### 一阶条件

设 $f:\mathbf{R}^n\to\mathbf{R}$ 可微。那么 $f$ 是拟凸函数，当且仅当 $\operatorname{\mathbf{dom}}f$ 是凸集，并且对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
f(y)\leq f(x)\quad\Longrightarrow\quad\nabla f(x)^T(y-x)\leq0.
\tag{3.20}
$$

<!-- pdf-page: 114 -->

<figure id="fig-3-11" data-figure="3.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-11.png" alt="以 c 为分界，左侧非增、右侧非减的拟凸函数曲线" data-source-page="114" data-source-rect="247,121,433,230">
<figcaption>图 3.11 $\mathbf{R}$ 上的一个拟凸函数。该函数在 $t\leq c$ 时非增，在 $t\geq c$ 时非减。</figcaption>
</figure>

<figure id="fig-3-12" data-figure="3.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/fig-3-12.png" alt="拟凸函数的三条等值线，以及外侧等值线上一点处的支撑超平面和梯度箭头" data-source-page="114" data-source-rect="255,302,448,460">
<figcaption>图 3.12 图中显示了拟凸函数 $f$ 的三条等值线。向量 $\nabla f(x)$ 确定了下水平集 $\{z\mid f(z)\leq f(x)\}$ 在 $x$ 处的一条支撑超平面。</figcaption>
</figure>

这是不等式 (3.2) 在拟凸函数中的对应形式。证明留作习题，见习题 3.43。

当 $\nabla f(x)\ne0$ 时，条件 (3.20) 有一个简单的几何解释：$\nabla f(x)$ 确定了下水平集 $\{y\mid f(y)\leq f(x)\}$ 在点 $x$ 处的一个支撑超平面，如图 3.12 所示。

虽然凸性的一阶条件 (3.2) 与拟凸性的一阶条件 (3.20) 很相似，但二者有一些重要区别。例如，如果 $f$ 是凸函数且 $\nabla f(x)=0$，那么 $x$ 是 $f$ 的一个全局最小点。但这个结论对拟凸函数不成立：可能有 $\nabla f(x)=0$，而 $x$ 却不是 $f$ 的全局最小点。

<!-- pdf-page: 115 -->

#### 二阶条件

现在假设 $f$ 二阶可微。如果 $f$ 是拟凸函数，那么对所有 $x\in\operatorname{\mathbf{dom}}f$ 及所有 $y\in\mathbf{R}^n$，都有

$$
y^T\nabla f(x)=0\quad\Longrightarrow\quad y^T\nabla^2f(x)y\geq0.
\tag{3.21}
$$

对于 $\mathbf{R}$ 上的拟凸函数，这化为简单的条件

$$
f'(x)=0\quad\Longrightarrow\quad f''(x)\geq0,
$$

即在任意斜率为零的点处，二阶导数都非负。对于 $\mathbf{R}^n$ 上的拟凸函数，条件 (3.21) 的解释稍微复杂一些。与 $n=1$ 的情形一样，只要 $\nabla f(x)=0$，就必有 $\nabla^2f(x)\succeq0$。当 $\nabla f(x)\ne0$ 时，条件 (3.21) 表示 $\nabla^2f(x)$ 在 $(n-1)$ 维子空间 $\nabla f(x)^\perp$ 上半正定。这意味着 $\nabla^2f(x)$ 最多只能有一个负特征值。

作为一个部分逆命题，如果 $f$ 对所有 $x\in\operatorname{\mathbf{dom}}f$ 和所有非零 $y\in\mathbf{R}^n$ 都满足

$$
y^T\nabla f(x)=0\quad\Longrightarrow\quad y^T\nabla^2f(x)y>0,
\tag{3.22}
$$

那么 $f$ 是拟凸函数。这个条件等价于：在所有满足 $\nabla f(x)=0$ 的点处，要求 $\nabla^2f(x)$ 正定；在其余各点处，要求 $\nabla^2f(x)$ 在 $(n-1)$ 维子空间 $\nabla f(x)^\perp$ 上正定。

#### 拟凸性二阶条件的证明

把函数限制在任意一条直线上，就只需考虑 $f:\mathbf{R}\to\mathbf{R}$ 的情形。

先证明：如果 $f:\mathbf{R}\to\mathbf{R}$ 在区间 $(a,b)$ 上为拟凸函数，那么它必须满足 (3.21)，即若 $f'(c)=0$、$c\in(a,b)$，则必有 $f''(c)\geq0$。如果 $c\in(a,b)$、$f'(c)=0$ 而 $f''(c)<0$，那么对于充分小的正数 $\epsilon$，有 $f(c-\epsilon)<f(c)$ 且 $f(c+\epsilon)<f(c)$。所以当正数 $\epsilon$ 充分小时，下水平集 $\{x\mid f(x)\leq f(c)-\epsilon\}$ 不连通，因而不是凸集，这与 $f$ 为拟凸函数的假设矛盾。

再证明：如果条件 (3.22) 成立，那么 $f$ 是拟凸函数。假设 (3.22) 成立，即对于每个满足 $f'(c)=0$ 的 $c\in(a,b)$，都有 $f''(c)>0$。这意味着函数 $f'$ 每次穿过零值时，都严格递增。因此它最多只能穿过零值一次。如果 $f'$ 从不穿过零值，那么 $f$ 在 $(a,b)$ 上或者非增、或者非减，因此是拟凸函数。否则，它恰好穿过零值一次，设发生在 $c\in(a,b)$ 处。由于 $f''(c)>0$，可知当 $a<t\leq c$ 时，$f'(t)\leq0$；当 $c\leq t<b$ 时，$f'(t)\geq0$。这说明 $f$ 是拟凸函数。

### 3.4.4 保持拟凸性的运算

#### 非负加权最大值

拟凸函数的非负加权最大值，即

$$
f=\max\{w_1f_1,\ldots,w_mf_m\},
$$

<!-- pdf-page: 116 -->

其中 $w_i\geq0$、$f_i$ 为拟凸函数，仍是拟凸函数。这一性质可以推广到一般的逐点上确界

$$
f(x)=\sup_{y\in C}(w(y)g(x,y)),
$$

其中 $w(y)\geq0$，且对每个 $y$，$g(x,y)$ 关于 $x$ 是拟凸函数。这个事实容易验证：$f(x)\leq\alpha$ 当且仅当

$$
w(y)g(x,y)\leq\alpha\quad\text{对所有 }y\in C,
$$

即 $f$ 的 $\alpha$ 下水平集，是以 $x$ 为变量的各函数 $w(y)g(x,y)$ 的 $\alpha$ 下水平集的交集。

<div class="example" markdown="1">

**例 3.37 广义特征值。** 对称矩阵对 $(X,Y)$ 的**最大广义特征值**，其中 $Y\succ0$，定义为

$$
\lambda_{\max}(X,Y)=\sup_{u\ne0}\frac{u^TXu}{u^TYu}=\sup\{\lambda\mid\det(\lambda Y-X)=0\},
$$

见第 A.5.3 节。这个函数在 $\operatorname{\mathbf{dom}}f=\mathbf{S}^n\times\mathbf{S}_{++}^n$ 上为拟凸函数。

为说明这一点，考虑表达式

$$
\lambda_{\max}(X,Y)=\sup_{u\ne0}\frac{u^TXu}{u^TYu}.
$$

对于每个 $u\ne0$，函数 $u^TXu/u^TYu$ 关于 $(X,Y)$ 是线性分式函数，因此是 $(X,Y)$ 的拟凸函数。由于 $\lambda_{\max}$ 是一族拟凸函数的上确界，可知它是拟凸函数。

</div>

#### 复合

如果 $g:\mathbf{R}^n\to\mathbf{R}$ 是拟凸函数，而 $h:\mathbf{R}\to\mathbf{R}$ 非减，那么 $f=h\circ g$ 是拟凸函数。

拟凸函数与仿射变换或线性分式变换复合，得到的仍是拟凸函数。如果 $f$ 是拟凸函数，那么 $g(x)=f(Ax+b)$ 是拟凸函数，而 $\widetilde g(x)=f((Ax+b)/(c^Tx+d))$ 在集合

$$
\{x\mid c^Tx+d>0,\ (Ax+b)/(c^Tx+d)\in\operatorname{\mathbf{dom}}f\}
$$

上为拟凸函数。

#### 最小化

如果 $f(x,y)$ 关于 $x$ 和 $y$ 联合拟凸，且 $C$ 是凸集，那么函数

$$
g(x)=\inf_{y\in C}f(x,y)
$$

是拟凸函数。

为说明这一点，需要证明 $\{x\mid g(x)\leq\alpha\}$ 是凸集，其中 $\alpha\in\mathbf{R}$ 任意。根据 $g$ 的定义，$g(x)\leq\alpha$ 当且仅当对任意 $\epsilon>0$，都存在<!-- pdf-page: 117 -->$y\in C$，使 $f(x,y)\leq\alpha+\epsilon$。现在取 $g$ 的 $\alpha$ 下水平集中的两点 $x_1$ 和 $x_2$。那么，对于任意 $\epsilon>0$，都存在 $y_1,y_2\in C$，使得

$$
f(x_1,y_1)\leq\alpha+\epsilon,\qquad f(x_2,y_2)\leq\alpha+\epsilon.
$$

由于 $f$ 关于 $x$ 和 $y$ 是拟凸函数，当 $0\leq\theta\leq1$ 时，还有

$$
f(\theta x_1+(1-\theta)x_2,\theta y_1+(1-\theta)y_2)\leq\alpha+\epsilon.
$$

因此 $g(\theta x_1+(1-\theta)x_2)\leq\alpha$，这就证明了 $\{x\mid g(x)\leq\alpha\}$ 是凸集。

### 3.4.5 用一族凸函数表示

在后续讨论中，用凸函数的不等式来表示拟凸函数 $f$ 的下水平集（它们是凸集），会很方便。我们希望找到一族以 $t\in\mathbf{R}$ 为索引的凸函数 $\phi_t:\mathbf{R}^n\to\mathbf{R}$，满足

$$
f(x)\leq t\quad\Longleftrightarrow\quad\phi_t(x)\leq0,
\tag{3.23}
$$

即拟凸函数 $f$ 的 $t$ 下水平集，就是凸函数 $\phi_t$ 的 0 下水平集。显然，$\phi_t$ 必须满足以下性质：对所有 $x\in\mathbf{R}^n$，当 $s\geq t$ 时，有 $\phi_t(x)\leq0\Longrightarrow\phi_s(x)\leq0$。如果对每个 $x$，$\phi_t(x)$ 都是 $t$ 的非增函数，即只要 $s\geq t$ 就有 $\phi_s(x)\leq\phi_t(x)$，那么上述性质就成立。

要看出这种表示总是存在，只需取

$$
\phi_t(x)=\begin{cases}
0&f(x)\leq t\\
\infty&\text{否则},
\end{cases}
$$

即令 $\phi_t$ 为 $f$ 的 $t$ 下水平集的指示函数。显然，这种表示并不唯一；例如，如果 $f$ 的各下水平集都是闭集，可以取

$$
\phi_t(x)=\operatorname{\mathbf{dist}}\left(x,\{z\mid f(z)\leq t\}\right).
$$

通常，我们希望函数族 $\phi_t$ 具有可微性等良好性质。

<div class="example" markdown="1">

**例 3.38 凸函数除以凹函数。** 设 $p$ 是凸函数，$q$ 是凹函数，并且在凸集 $C$ 上有 $p(x)\geq0$、$q(x)>0$。那么，在 $C$ 上由 $f(x)=p(x)/q(x)$ 定义的函数 $f$ 是拟凸函数。

这里有

$$
f(x)\leq t\quad\Longleftrightarrow\quad p(x)-tq(x)\leq0,
$$

因此对于 $t\geq0$，可以取 $\phi_t(x)=p(x)-tq(x)$。对每个 $t$，$\phi_t$ 是凸函数；对每个 $x$，$\phi_t(x)$ 随 $t$ 递减。

</div>

<!-- pdf-page: 118 -->

## 3.5 对数凹函数与对数凸函数

### 3.5.1 定义

如果函数 $f:\mathbf{R}^n\to\mathbf{R}$ 对所有 $x\in\operatorname{\mathbf{dom}}f$ 都满足 $f(x)>0$，并且 $\log f$ 是凹函数，就称 $f$ 是**对数凹函数**（logarithmically concave 或 log-concave）。如果 $\log f$ 是凸函数，就称 $f$ 是**对数凸函数**（logarithmically convex 或 log-convex）。因此，$f$ 是对数凸函数，当且仅当 $1/f$ 是对数凹函数。允许 $f$ 取值为零会很方便，此时约定 $\log f(x)=-\infty$。在这种情况下，如果扩展值函数 $\log f$ 是凹函数，就称 $f$ 是对数凹函数。

不用对数，也可以直接表述对数凹性：函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的定义域为凸集，且对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $f(x)>0$，那么它是对数凹函数，当且仅当对所有 $x,y\in\operatorname{\mathbf{dom}}f$ 以及 $0\leq\theta\leq1$，都有

$$
f(\theta x+(1-\theta)y)\geq f(x)^\theta f(y)^{1-\theta}.
$$

特别地，对数凹函数在两点平均值处的函数值，不小于它在这两点处函数值的几何平均。

由复合规则可知，如果 $h$ 是凸函数，那么 $e^h$ 是凸函数，所以对数凸函数一定是凸函数。类似地，非负凹函数一定是对数凹函数。由于对数函数单调递增，也容易看出，对数凸函数是拟凸函数，而对数凹函数是拟凹函数。

<div class="example" markdown="1">

**例 3.39** 对数凹函数与对数凸函数的一些简单例子。

- **仿射函数。** $f(x)=a^Tx+b$ 在 $\{x\mid a^Tx+b>0\}$ 上为对数凹函数。
- **幂函数。** $\mathbf{R}_{++}$ 上的 $f(x)=x^a$，当 $a\leq0$ 时为对数凸函数，当 $a\geq0$ 时为对数凹函数。
- **指数函数。** $f(x)=e^{ax}$ 既是对数凸函数，也是对数凹函数。
- 高斯密度的累积分布函数

    $$
    \Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-u^2/2}\,du
    $$

    是对数凹函数，见习题 3.54。

- **Gamma 函数。** Gamma 函数

    $$
    \Gamma(x)=\int_0^\infty u^{x-1}e^{-u}\,du
    $$

    在 $x\geq1$ 时为对数凸函数，见习题 3.52。

- **行列式。** $\det X$ 在 $\mathbf{S}_{++}^n$ 上为对数凹函数。
- **行列式除以迹。** $\det X/\operatorname{\mathbf{tr}}X$ 在 $\mathbf{S}_{++}^n$ 上为对数凹函数，见习题 3.49。

</div>

<div class="example" markdown="1">

**例 3.40 对数凹密度函数。** 许多常见的概率密度函数都是对数凹的。其中两个例子是多元正态分布

$$
f(x)=\frac{1}{\sqrt{(2\pi)^n\det\Sigma}}e^{-\frac12(x-\bar x)^T\Sigma^{-1}(x-\bar x)}
$$

<!-- pdf-page: 119 -->

（其中 $\bar x\in\mathbf{R}^n$、$\Sigma\in\mathbf{S}_{++}^n$），以及 $\mathbf{R}_+^n$ 上的指数分布

$$
f(x)=\left(\prod_{i=1}^n\lambda_i\right)e^{-\lambda^Tx}
$$

（其中 $\lambda\succ0$）。另一个例子是凸集 $C$ 上的均匀分布，

$$
f(x)=\begin{cases}
1/\alpha&x\in C\\
0&x\notin C,
\end{cases}
$$

其中 $\alpha=\operatorname{\mathbf{vol}}(C)$ 是 $C$ 的体积，也就是 Lebesgue 测度。此时，$\log f$ 在 $C$ 外取值为 $-\infty$，在 $C$ 上取值为 $-\log\alpha$，因此是凹函数。

再考虑一个较少见的例子：Wishart 分布。它定义如下。设 $x_1,\ldots,x_p\in\mathbf{R}^n$ 是相互独立的高斯随机向量，均值为零，协方差为 $\Sigma\in\mathbf{S}^n$，且 $p>n$。随机矩阵 $X=\sum_{i=1}^p x_i x_i^T$ 具有 Wishart 密度

$$
f(X)=a(\det X)^{(p-n-1)/2}e^{-\frac12\operatorname{\mathbf{tr}}(\Sigma^{-1}X)},
$$

其中 $\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n$，$a$ 是正常数。Wishart 密度是对数凹的，因为

$$
\log f(X)=\log a+\frac{p-n-1}{2}\log\det X-\frac12\operatorname{\mathbf{tr}}(\Sigma^{-1}X),
$$

这是 $X$ 的凹函数。

</div>

### 3.5.2 性质

#### 二阶可微的对数凸函数与对数凹函数

设 $f$ 二阶可微，且 $\operatorname{\mathbf{dom}}f$ 是凸集。由于

$$
\nabla^2\log f(x)=\frac{1}{f(x)}\nabla^2f(x)-\frac{1}{f(x)^2}\nabla f(x)\nabla f(x)^T,
$$

可知 $f$ 是对数凸函数，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$，都有

$$
f(x)\nabla^2f(x)\succeq\nabla f(x)\nabla f(x)^T;
$$

$f$ 是对数凹函数，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$，都有

$$
f(x)\nabla^2f(x)\preceq\nabla f(x)\nabla f(x)^T.
$$

#### 乘法、加法与积分

对数凸性和对数凹性在乘法及正数缩放下保持不变。例如，如果 $f$ 和 $g$ 都是对数凹函数，那么逐点乘积 $h(x)=f(x)g(x)$ 也是对数凹函数，因为 $\log h(x)=\log f(x)+\log g(x)$，而 $\log f(x)$ 和 $\log g(x)$ 都是 $x$ 的凹函数。

简单例子表明，对数凹函数的和通常不是对数凹函数。但是，求和可以保持对数凸性。设 $f$ 和 $g$ 都是对数凸函数，即 $F=\log f$ 和 $G=\log g$ 都是凸函数。由凸函数的复合规则可知，

$$
\log(\exp F+\exp G)=\log(f+g)
$$

<!-- pdf-page: 120 -->

是凸函数。因此，两个对数凸函数之和仍为对数凸函数。

更一般地，如果对每个 $y\in C$，$f(x,y)$ 关于 $x$ 都是对数凸函数，那么

$$
g(x)=\int_Cf(x,y)\,dy
$$

是对数凸函数。

<div class="example" markdown="1">

**例 3.41 非负函数的 Laplace 变换，以及矩生成函数和累积量生成函数。** 设 $p:\mathbf{R}^n\to\mathbf{R}$ 对所有 $x$ 都满足 $p(x)\geq0$。$p$ 的 Laplace 变换

$$
P(z)=\int p(x)e^{-z^Tx}\,dx
$$

在 $\mathbf{R}^n$ 上为对数凸函数。（这里的定义域 $\operatorname{\mathbf{dom}}P$ 自然是 $\{z\mid P(z)<\infty\}$。）

现在假设 $p$ 是一个概率密度，即满足 $\int p(x)\,dx=1$。函数 $M(z)=P(-z)$ 称为该密度的**矩生成函数**（moment generating function）。这一名称来自以下事实：对矩生成函数求导并在 $z=0$ 处取值，就可以得到该密度的各阶矩。例如，

$$
\nabla M(0)=\mathbf{E}v,\qquad\nabla^2M(0)=\mathbf{E}vv^T,
$$

其中 $v$ 是密度为 $p$ 的随机变量。

凸函数 $\log M(z)$ 称为 $p$ 的**累积量生成函数**（cumulant generating function），因为它的导数给出该密度的累积量。例如，累积量生成函数的一阶和二阶导数在零点处的值，分别是相应随机变量的均值和协方差：

$$
\nabla\log M(0)=\mathbf{E}v,\qquad\nabla^2\log M(0)=\mathbf{E}(v-\mathbf{E}v)(v-\mathbf{E}v)^T.
$$

</div>

#### 对数凹函数的积分

在某些特殊情形下，积分保持对数凹性。如果 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$ 是对数凹函数，那么

$$
g(x)=\int f(x,y)\,dy
$$

是 $x$ 的对数凹函数，定义在 $\mathbf{R}^n$ 上。这里是在 $\mathbf{R}^m$ 上积分。这个结论的证明并不简单，可参阅相关文献。

这个结论有许多重要推论，本节余下部分将介绍其中一些。例如，它意味着对数凹概率密度的边缘分布也是对数凹的。它还意味着卷积保持对数凹性：如果 $f$ 和 $g$ 在 $\mathbf{R}^n$ 上都是对数凹函数，那么卷积

$$
(f*g)(x)=\int f(x-y)g(y)\,dy
$$

也是对数凹函数。（为说明这一点，只需注意 $g(y)$ 和 $f(x-y)$ 关于 $(x,y)$ 都是对数凹函数，因此乘积 $f(x-y)g(y)$ 也是；再应用上述积分结论即可。）

<!-- pdf-page: 121 -->

设 $C\subseteq\mathbf{R}^n$ 是凸集，$w$ 是 $\mathbf{R}^n$ 中的随机向量，具有对数凹概率密度 $p$。那么函数

$$
f(x)=\operatorname{\mathbf{prob}}(x+w\in C)
$$

关于 $x$ 是对数凹函数。为说明这一点，把 $f$ 写成

$$
f(x)=\int g(x+w)p(w)\,dw,
$$

其中 $g$ 定义为

$$
g(u)=\begin{cases}
1&u\in C\\
0&u\notin C,
\end{cases}
$$

它是对数凹函数，再应用积分结论即可。

<div class="example" markdown="1">

**例 3.42** 概率密度函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的**累积分布函数**（cumulative distribution function）定义为

$$
F(x)=\operatorname{\mathbf{prob}}(w\preceq x)=\int_{-\infty}^{x_n}\cdots\int_{-\infty}^{x_1}f(z)\,dz_1\cdots dz_n,
$$

其中 $w$ 是密度为 $f$ 的随机变量。如果 $f$ 是对数凹函数，那么 $F$ 也是对数凹函数。前面已经遇到过一个特殊情况：高斯随机变量的累积分布函数

$$
f(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt
$$

是对数凹函数，见例 3.39 和习题 3.54。

</div>

<div class="example" markdown="1">

**例 3.43 成品率函数。** 用 $x\in\mathbf{R}^n$ 表示某种制造产品的一组参数的标称值或目标值。制造过程中的波动，使实际制造出来的产品参数取值为 $x+w$，其中 $w\in\mathbf{R}^n$ 是表示制造波动的随机向量，通常假设其均值为零。制造过程的成品率作为标称参数值的函数，为

$$
Y(x)=\operatorname{\mathbf{prob}}(x+w\in S),
$$

其中 $S\subseteq\mathbf{R}^n$ 表示产品可接受的参数值集合，即产品规格。

如果制造误差 $w$ 的密度是对数凹的，例如高斯密度，并且产品规格集合 $S$ 是凸集，那么成品率函数 $Y$ 是对数凹函数。这意味着 **$\alpha$ 成品率区域**是凸集；该区域定义为使成品率超过 $\alpha$ 的标称参数所构成的集合。例如，95% 成品率区域

$$
\{x\mid Y(x)\geq0.95\}=\{x\mid\log Y(x)\geq\log0.95\}
$$

是凸集，因为它是凹函数 $\log Y$ 的上水平集。

</div>

<!-- pdf-page: 122 -->

<div class="example" markdown="1">

**例 3.44 多面体的体积。** 设 $A\in\mathbf{R}^{m\times n}$。定义

$$
P_u=\{x\in\mathbf{R}^n\mid Ax\preceq u\}.
$$

那么，它的体积 $\operatorname{\mathbf{vol}}P_u$ 是 $u$ 的对数凹函数。

为证明这一点，注意函数

$$
\Psi(x,u)=\begin{cases}
1&Ax\preceq u\\
0&\text{否则}
\end{cases}
$$

是对数凹函数。由积分结论可知，

$$
\int\Psi(x,u)\,dx=\operatorname{\mathbf{vol}}P_u
$$

是对数凹函数。

</div>

## 3.6 关于广义不等式的凸性

现在用广义不等式代替 $\mathbf{R}$ 上通常的序关系，来推广单调性和凸性的概念。

### 3.6.1 关于广义不等式的单调性

设 $K\subseteq\mathbf{R}^n$ 是正常锥，对应的广义不等式为 $\preceq_K$。如果函数 $f:\mathbf{R}^n\to\mathbf{R}$ 满足

$$
x\preceq_K y\quad\Longrightarrow\quad f(x)\leq f(y),
$$

就称它是 **$K$ 非减**的；如果满足

$$
x\preceq_K y,\ x\ne y\quad\Longrightarrow\quad f(x)<f(y),
$$

就称它是 **$K$ 递增**的。以类似方式可以定义 $K$ 非增函数和 $K$ 递减函数。

<div class="example" markdown="1">

**例 3.45 以向量为自变量的单调函数。** 函数 $f:\mathbf{R}^n\to\mathbf{R}$ 关于 $\mathbf{R}_+^n$ 非减，当且仅当对所有 $x,y$，都有

$$
x_1\leq y_1,\ldots,x_n\leq y_n\quad\Longrightarrow\quad f(x)\leq f(y).
$$

这等价于说，把 $f$ 限制在任意一个分量 $x_i$ 上时，即将 $x_i$ 视为变量、固定所有 $j\ne i$ 的 $x_j$ 时，所得函数非减。

</div>

<div class="example" markdown="1">

**例 3.46 矩阵单调函数。** 如果函数 $f:\mathbf{S}^n\to\mathbf{R}$ 关于半正定锥单调（递增、递减），就称它是**矩阵单调**（递增、递减）的。以下是变量 $X\in\mathbf{S}^n$ 的几个矩阵单调函数例子：

<!-- pdf-page: 123 -->

- 对于 $W\in\mathbf{S}^n$，当 $W\succeq0$ 时，$\operatorname{\mathbf{tr}}(WX)$ 矩阵非减；当 $W\succ0$ 时，它矩阵递增。当 $W\preceq0$ 时，它矩阵非增；当 $W\prec0$ 时，它矩阵递减。
- $\operatorname{\mathbf{tr}}(X^{-1})$ 在 $\mathbf{S}_{++}^n$ 上矩阵递减。
- $\det X$ 在 $\mathbf{S}_{++}^n$ 上矩阵递增，在 $\mathbf{S}_+^n$ 上矩阵非减。

</div>

#### 单调性的梯度条件

回顾定义域为凸集（即区间）的可微函数 $f:\mathbf{R}\to\mathbf{R}$：它非减，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $f'(x)\geq0$；如果对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $f'(x)>0$，那么它递增，但逆命题不成立。这些条件容易推广到关于广义不等式的单调性。定义域为凸集的可微函数 $f$ 是 $K$ 非减的，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$，都有

$$
\nabla f(x)\succeq_{K^*}0.
\tag{3.24}
$$

注意这里与简单标量情形的区别：梯度必须在**对偶不等式**的意义下非负。对于严格情形，有以下结论：如果对所有 $x\in\operatorname{\mathbf{dom}}f$，都有

$$
\nabla f(x)\succ_{K^*}0,
\tag{3.25}
$$

那么 $f$ 是 $K$ 递增的。与标量情形一样，逆命题不成立。

下面证明这些单调性的一阶条件。先假设 $f$ 对所有 $x$ 都满足 (3.24)，但它不是 $K$ 非减的，即存在 $x,y$，满足 $x\preceq_K y$ 且 $f(y)<f(x)$。由 $f$ 的可微性，存在 $t\in[0,1]$，使得

$$
\frac{d}{dt}f(x+t(y-x))=\nabla f(x+t(y-x))^T(y-x)<0.
$$

由于 $y-x\in K$，这意味着

$$
\nabla f(x+t(y-x))\notin K^*,
$$

与 (3.24) 处处成立的假设矛盾。类似地，可以证明 (3.25) 蕴含 $f$ 是 $K$ 递增的。

也容易看出，(3.24) 处处成立是必要的。假设 (3.24) 在 $x=z$ 处不成立。由对偶锥的定义，这意味着存在 $v\in K$，使得

$$
\nabla f(z)^Tv<0.
$$

现在把 $h(t)=f(z+tv)$ 看作 $t$ 的函数。有 $h'(0)=\nabla f(z)^Tv<0$，因此存在 $t>0$，使得 $h(t)=f(z+tv)<h(0)=f(z)$，这意味着 $f$ 不是 $K$ 非减的。

### 3.6.2 关于广义不等式的凸性

设 $K\subseteq\mathbf{R}^m$ 是正常锥，对应的广义不等式为 $\preceq_K$。如果函数 $f:\mathbf{R}^n\to\mathbf{R}^m$ 对所有 $x,y$ 以及 $0\leq\theta\leq1$ 都满足

$$
f(\theta x+(1-\theta)y)\preceq_K\theta f(x)+(1-\theta)f(y),
$$

就称 $f$ 是 **$K$ 凸**的。

<!-- pdf-page: 124 -->

如果对所有 $x\ne y$ 以及 $0<\theta<1$ 都有

$$
f(\theta x+(1-\theta)y)\prec_K\theta f(x)+(1-\theta)f(y),
$$

就称该函数是**严格 $K$ 凸**的。当 $m=1$ 且 $K=\mathbf{R}_+$ 时，这些定义就化为通常的凸性和严格凸性。

<div class="example" markdown="1">

**例 3.47 关于逐分量不等式的凸性。** 函数 $f:\mathbf{R}^n\to\mathbf{R}^m$ 关于逐分量不等式（即由 $\mathbf{R}_+^m$ 诱导的广义不等式）是凸的，当且仅当对所有 $x,y$ 以及 $0\leq\theta\leq1$，都有

$$
f(\theta x+(1-\theta)y)\preceq\theta f(x)+(1-\theta)f(y),
$$

即每个分量函数 $f_i$ 都是凸函数。函数 $f$ 关于逐分量不等式严格凸，当且仅当每个分量函数 $f_i$ 都严格凸。

</div>

<div class="example" markdown="1">

**例 3.48 矩阵凸性。** 设 $f$ 是一个取值为对称矩阵的函数，即 $f:\mathbf{R}^n\to\mathbf{S}^m$。如果对任意 $x,y$ 以及 $\theta\in[0,1]$，都有

$$
f(\theta x+(1-\theta)y)\preceq\theta f(x)+(1-\theta)f(y),
$$

就说函数 $f$ 关于矩阵不等式是凸的。这有时称为**矩阵凸性**。一个等价定义是：对所有向量 $z$，标量函数 $z^Tf(x)z$ 都是凸函数。（这常常是证明矩阵凸性的好方法。）如果当 $x\ne y$ 且 $0<\theta<1$ 时，有

$$
f(\theta x+(1-\theta)y)\prec\theta f(x)+(1-\theta)f(y),
$$

就称该矩阵函数严格矩阵凸；等价地，对每个 $z\ne0$，$z^Tfz$ 都严格凸。

一些例子如下：

- 函数 $f(X)=XX^T$，其中 $X\in\mathbf{R}^{n\times m}$，是矩阵凸函数，因为对于固定的 $z$，函数 $z^TXX^Tz=\|X^Tz\|_2^2$ 是关于 $X$ 的各分量的凸二次函数。出于同样的原因，$f(X)=X^2$ 在 $\mathbf{S}^n$ 上也是矩阵凸函数。
- 当 $1\leq p\leq2$ 或 $-1\leq p\leq0$ 时，函数 $X^p$ 在 $\mathbf{S}_{++}^n$ 上矩阵凸；当 $0\leq p\leq1$ 时，它矩阵凹。
- 当 $n\geq2$ 时，函数 $f(X)=e^X$ 在 $\mathbf{S}^n$ 上不是矩阵凸函数。

</div>

关于凸函数的许多结论都可以推广到 $K$ 凸函数。举一个简单例子：一个函数是 $K$ 凸的，当且仅当将它限制在定义域内任意一条直线上时，得到的函数都是 $K$ 凸的。本节余下部分列出几个以后将用到的 $K$ 凸性结论；更多结论将在习题中讨论。

#### $K$ 凸性的对偶刻画

函数 $f$ 是 $K$ 凸的，当且仅当对每个 $w\succeq_{K^*}0$，实值函数 $w^Tf$ 都是通常意义下的凸函数；$f$ 严格 $K$ 凸，当且仅当对每个非零 $w\succeq_{K^*}0$，函数 $w^Tf$ 都严格凸。这些结论直接来自对偶不等式的定义和性质。

<!-- pdf-page: 125 -->

#### 可微的 $K$ 凸函数

可微函数 $f$ 是 $K$ 凸的，当且仅当它的定义域是凸集，并且对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
f(y)\succeq_K f(x)+Df(x)(y-x).
$$

这里 $Df(x)\in\mathbf{R}^{m\times n}$ 是 $f$ 在 $x$ 处的导数，也就是 Jacobian 矩阵，见第 A.4.1 节。函数 $f$ 严格 $K$ 凸，当且仅当对所有满足 $x\ne y$ 的 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
f(y)\succ_K f(x)+Df(x)(y-x).
$$

#### 复合定理

关于复合的许多结论都可以推广到 $K$ 凸性。例如，如果 $g:\mathbf{R}^n\to\mathbf{R}^p$ 是 $K$ 凸的，$h:\mathbf{R}^p\to\mathbf{R}$ 是凸函数，并且 $\widetilde h$（$h$ 的扩展值延拓）是 $K$ 非减的，那么 $h\circ g$ 就是凸函数。这个结论推广了以下事实：对凸函数再施加一个非减凸函数，得到的仍是凸函数。$\widetilde h$ 为 $K$ 非减这一条件，意味着 $\operatorname{\mathbf{dom}}h-K=\operatorname{\mathbf{dom}}h$。

<div class="example" markdown="1">

**例 3.49** 二次矩阵函数 $g:\mathbf{R}^{m\times n}\to\mathbf{S}^n$ 定义为

$$
g(X)=X^TAX+B^TX+X^TB+C,
$$

其中 $A\in\mathbf{S}^m$、$B\in\mathbf{R}^{m\times n}$、$C\in\mathbf{S}^n$。当 $A\succeq0$ 时，它是凸的。

由 $h(Y)=-\log\det(-Y)$ 定义的函数 $h:\mathbf{S}^n\to\mathbf{R}$，在 $\operatorname{\mathbf{dom}}h=-\mathbf{S}_{++}^n$ 上凸且递增。

由复合定理可知，

$$
f(X)=-\log\det\left(-(X^TAX+B^TX+X^TB+C)\right)
$$

在

$$
\operatorname{\mathbf{dom}}f=\{X\in\mathbf{R}^{m\times n}\mid X^TAX+B^TX+X^TB+C\prec0\}
$$

上为凸函数。这推广了以下事实：只要 $a\geq0$，函数

$$
-\log(-(ax^2+bx+c))
$$

就在

$$
\{x\in\mathbf{R}\mid ax^2+bx+c<0\}
$$

上为凸函数。

</div>

<!-- pdf-page: 126 -->

## 文献说明

凸分析的标准参考书是 Rockafellar [Roc70]。其他关于凸函数的书包括 Stoer 与 Witzgall [SW70]、Roberts 与 Varberg [RV73]、Van Tiel [vT84]、Hiriart-Urruty 与 Lemaréchal [HUL93]、Ekeland 与 Témam [ET99]、Borwein 与 Lewis [BL00]、Florenzano 与 Le Van [FL01]、Barvinok [Bar02]，以及 Bertsekas、Nedić 与 Ozdaglar [Ber03] 的著作。大多数非线性规划教材也包含讨论凸函数的章节，例如 Mangasarian [Man94]、Bazaraa、Sherali 与 Shetty [BSS93]、Bertsekas [Ber99]、Polyak [Pol87]，以及 Peressini、Sullivan 与 Uhl [PSU88]。

Jensen 不等式见 [Jen06]。Hardy、Littlewood 与 Pólya [HLP52]，以及 Beckenbach 与 Bellman [BB65]，对不等式作了一般研究，其中 Jensen 不等式处于核心地位。

“透视函数”（perspective function）这一术语来自 Hiriart-Urruty 与 Lemaréchal [HUL93, 第 1 卷，第 100 页]。关于例 3.19 中的定义（相对熵与 Kullback–Leibler 散度）及相关的习题 3.13，可参阅 Cover 与 Thomas [CT91]。

关于拟凸函数以及凸性的其他推广，一些重要的早期文献包括 Nikaidô [Nik54]、Mangasarian [Man94, 第 9 章]、Arrow 与 Enthoven [AE61]、Ponstein [Pon67]，以及 Luenberger [Lue68]。更全面的参考文献列表可参阅 Bazaraa、Sherali 与 Shetty [BSS93, 第 126 页]。

Prékopa [Pré80] 对对数凹函数作了综述。Laplace 变换的对数凸性见 Barndorff-Nielsen [BN78, 第 7 节]。对数凹函数积分结论的证明见 Prékopa [Pré71, Pré73]。

从 Nesterov 与 Nemirovski [NN94, 第 156 页] 开始，广义不等式在近年的锥规划文献中得到广泛使用；另见 Ben-Tal 与 Nemirovski [BTN01] 以及第 4 章末的参考文献。关于广义不等式的凸性，也见于 Luenberger [Lue69, 第 8.2 节] 和 Isii [Isi64] 的工作。矩阵单调性与矩阵凸性通常归功于 Löwner [Löw34]，Davis [Dav63]、Roberts 与 Varberg [RV73, 第 216 页]，以及 Marshall 与 Olkin [MO79, 第 16E 节] 对它们作了详细讨论。例 3.48 中关于函数 $X^p$ 凸性和凹性的结论，见 Bondar [Bon94, 定理 16.1]。关于说明 $e^X$ 不是矩阵凸函数的简单例子，见 Marshall 与 Olkin [MO79, 第 474 页]。

<!-- pdf-page: 127 -->

## 习题

### 凸性的定义

**3.1** 设 $f:\mathbf{R}\to\mathbf{R}$ 是凸函数，$a,b\in\operatorname{\mathbf{dom}}f$，且 $a<b$。

- (a) 证明：对所有 $x\in[a,b]$，都有

    $$
    f(x)\leq\frac{b-x}{b-a}f(a)+\frac{x-a}{b-a}f(b).
    $$

- (b) 证明：对所有 $x\in(a,b)$，都有

    $$
    \frac{f(x)-f(a)}{x-a}\leq\frac{f(b)-f(a)}{b-a}\leq\frac{f(b)-f(x)}{b-x}.
    $$

    画一幅示意图说明这个不等式。

- (c) 假设 $f$ 可微。利用 (b) 的结论证明

    $$
    f'(a)\leq\frac{f(b)-f(a)}{b-a}\leq f'(b).
    $$

    注意，这些不等式也可以由 (3.2) 得到：

    $$
    f(b)\geq f(a)+f'(a)(b-a),\qquad f(a)\geq f(b)+f'(b)(a-b).
    $$

- (d) 假设 $f$ 二阶可微。利用 (c) 的结论证明 $f''(a)\geq0$ 且 $f''(b)\geq0$。

**3.2 凸函数、凹函数、拟凸函数和拟凹函数的水平集。** 下图给出了函数 $f$ 的一些水平集。标为 1 的曲线表示 $\{x\mid f(x)=1\}$，其余类推。

<figure id="exercise-3-2-a" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/exercise-3-2-a.png" alt="习题 3.2 第一组等值线：三条嵌套的闭合曲线，从内到外标为 1、2、3" data-source-page="127" data-source-rect="234,424,337,530">
</figure>

$f$ 是否可能是凸函数、凹函数、拟凸函数或拟凹函数？解释你的答案。对下面的等值线图作同样的分析。

<figure id="exercise-3-2-b" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-03/exercise-3-2-b.png" alt="习题 3.2 第二组等值线：六条从左到右标为 1 至 6 的曲线" data-source-page="127" data-source-rect="228,563,343,701">
</figure>

<!-- pdf-page: 128 -->

**3.3 递增凸函数的反函数。** 设 $f:\mathbf{R}\to\mathbf{R}$ 在其定义域 $(a,b)$ 上递增且凸。用 $g$ 表示其反函数，即定义域为 $(f(a),f(b))$、对 $a<x<b$ 满足 $g(f(x))=x$ 的函数。关于 $g$ 的凸性或凹性，可以得出什么结论？

**3.4** [RV73, 第 15 页] 证明：连续函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，当且仅当对于每条线段，它在线段上的平均值不大于它在两个端点处函数值的平均值。也就是说，对每个 $x,y\in\mathbf{R}^n$，都有

$$
\int_0^1f(x+\lambda(y-x))\,d\lambda\leq\frac{f(x)+f(y)}{2}.
$$

**3.5** [RV73, 第 22 页] **凸函数的累计平均。** 设 $f:\mathbf{R}\to\mathbf{R}$ 是凸函数，且 $\mathbf{R}_+\subseteq\operatorname{\mathbf{dom}}f$。证明它的**累计平均**（running average）$F$，定义为

$$
F(x)=\frac1x\int_0^x f(t)\,dt,\qquad\operatorname{\mathbf{dom}}F=\mathbf{R}_{++},
$$

是凸函数。**提示：** 对每个 $s$，$f(sx)$ 关于 $x$ 是凸函数，因此 $\int_0^1f(sx)\,ds$ 是凸函数。

**3.6 函数与上图。** 一个函数的上图在什么情况下是半空间？在什么情况下是凸锥？在什么情况下是多面体？

**3.7** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，$\operatorname{\mathbf{dom}}f=\mathbf{R}^n$，并且它在 $\mathbf{R}^n$ 上有上界。证明 $f$ 是常函数。

**3.8 凸性的二阶条件。** 证明：二阶可微函数 $f$ 是凸函数，当且仅当其定义域为凸集，而且对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $\nabla^2f(x)\succeq0$。**提示：** 先考虑 $f:\mathbf{R}\to\mathbf{R}$ 的情形。可以使用凸性的一阶条件，该条件已在第 70 页证明。

**3.9 仿射集上凸性的二阶条件。** 设 $F\in\mathbf{R}^{n\times m}$、$\widehat x\in\mathbf{R}^n$。将 $f:\mathbf{R}^n\to\mathbf{R}$ 限制在仿射集 $\{Fz+\widehat x\mid z\in\mathbf{R}^m\}$ 上，定义为函数 $\widetilde f:\mathbf{R}^m\to\mathbf{R}$，其中

$$
\widetilde f(z)=f(Fz+\widehat x),\qquad\operatorname{\mathbf{dom}}\widetilde f=\{z\mid Fz+\widehat x\in\operatorname{\mathbf{dom}}f\}.
$$

假设 $f$ 二阶可微，且定义域为凸集。

- (a) 证明：$\widetilde f$ 是凸函数，当且仅当对所有 $z\in\operatorname{\mathbf{dom}}\widetilde f$，都有

    $$
    F^T\nabla^2f(Fz+\widehat x)F\succeq0.
    $$

- (b) 设矩阵 $A\in\mathbf{R}^{p\times n}$ 的零空间等于 $F$ 的值域，即 $AF=0$ 且 $\operatorname{\mathbf{rank}}A=n-\operatorname{\mathbf{rank}}F$。证明：如果对所有 $z\in\operatorname{\mathbf{dom}}\widetilde f$，都存在 $\lambda\in\mathbf{R}$，使得

    $$
    \nabla^2f(Fz+\widehat x)+\lambda A^TA\succeq0,
    $$

    那么 $\widetilde f$ 是凸函数。

    **提示：** 使用以下结论：如果 $B\in\mathbf{S}^n$、$A\in\mathbf{R}^{p\times n}$，并且存在 $\lambda$ 使得 $B+\lambda A^TA\succeq0$，那么对所有 $x\in\mathcal{N}(A)$，都有 $x^TBx\geq0$。

**3.10 Jensen 不等式的一个推广。** Jensen 不等式的一种解释是，随机化或抖动会产生不利影响，即提高凸函数的平均值：对于凸函数 $f$ 和零均值随机变量 $v$，有 $\mathbf{E}f(x_0+v)\geq f(x_0)$。这引出以下猜想：如果 $f$ 是凸函数，那么 $v$ 的方差越大，$\mathbf{E}f(x_0+v)$ 就越大。

- (a) 给出一个反例，说明这一猜想不成立。找出零均值随机变量 $v$ 和 $w$，满足 $\operatorname{\mathbf{var}}(v)>\operatorname{\mathbf{var}}(w)$，以及一个凸函数 $f$ 和一点 $x_0$，使得 $\mathbf{E}f(x_0+v)<\mathbf{E}f(x_0+w)$。
- (b) <!-- pdf-page: 129 -->当 $v$ 和 $w$ 互为缩放版本时，猜想成立。证明：当 $f$ 为凸函数、$v$ 的均值为零时，$\mathbf{E}f(x_0+tv)$ 关于 $t\geq0$ 单调递增。

**3.11 单调映射。** 如果函数 $\psi:\mathbf{R}^n\to\mathbf{R}^n$ 对所有 $x,y\in\operatorname{\mathbf{dom}}\psi$ 都满足

$$
(\psi(x)-\psi(y))^T(x-y)\geq0,
$$

就称它是**单调的**。（注意，这里的“单调”与第 3.6.1 节的定义不同；这两种定义都被广泛使用。）设 $f:\mathbf{R}^n\to\mathbf{R}$ 是可微凸函数。证明它的梯度 $\nabla f$ 是单调的。逆命题是否成立，也就是说，每个单调映射都是某个凸函数的梯度吗？

**3.12** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，$g:\mathbf{R}^n\to\mathbf{R}$ 是凹函数，$\operatorname{\mathbf{dom}}f=\operatorname{\mathbf{dom}}g=\mathbf{R}^n$，并且对所有 $x$ 都有 $g(x)\leq f(x)$。证明存在仿射函数 $h$，使得对所有 $x$ 都有 $g(x)\leq h(x)\leq f(x)$。换句话说，如果凹函数 $g$ 是凸函数 $f$ 的下界函数，那么可以在 $f$ 和 $g$ 之间放入一个仿射函数。

**3.13 Kullback–Leibler 散度与信息不等式。** 设 $D_{\mathrm{kl}}$ 是 (3.17) 定义的 Kullback–Leibler 散度。证明**信息不等式**：对所有 $u,v\in\mathbf{R}_{++}^n$，都有 $D_{\mathrm{kl}}(u,v)\geq0$。再证明，$D_{\mathrm{kl}}(u,v)=0$ 当且仅当 $u=v$。

**提示：** Kullback–Leibler 散度可以写成

$$
D_{\mathrm{kl}}(u,v)=f(u)-f(v)-\nabla f(v)^T(u-v),
$$

其中 $f(v)=\sum_{i=1}^n v_i\log v_i$ 是 $v$ 的负熵。

**3.14 凸–凹函数与鞍点。** 如果对每个固定的 $x$，$f(x,z)$ 都是 $z$ 的凹函数，而对每个固定的 $z$，它都是 $x$ 的凸函数，就称函数 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$ 是**凸–凹函数**。还要求它的定义域具有乘积形式 $\operatorname{\mathbf{dom}}f=A\times B$，其中 $A\subseteq\mathbf{R}^n$ 和 $B\subseteq\mathbf{R}^m$ 都是凸集。

- (a) 对二阶可微函数 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$，用它的 Hessian 矩阵 $\nabla^2f(x,z)$ 给出其为凸–凹函数的二阶条件。
- (b) 设 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$ 是可微凸–凹函数，且 $\nabla f(\widetilde x,\widetilde z)=0$。证明**鞍点性质**成立：对所有 $x,z$，都有

    $$
    f(\widetilde x,z)\leq f(\widetilde x,\widetilde z)\leq f(x,\widetilde z).
    $$

    证明这意味着 $f$ 满足**强最大–最小性质**：

    $$
    \sup_z\inf_x f(x,z)=\inf_x\sup_z f(x,z)
    $$

    （两边的共同值为 $f(\widetilde x,\widetilde z)$）。

- (c) 现在假设 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$ 可微，但不一定是凸–凹函数，并且在 $\widetilde x,\widetilde z$ 处满足鞍点性质：对所有 $x,z$，都有

    $$
    f(\widetilde x,z)\leq f(\widetilde x,\widetilde z)\leq f(x,\widetilde z).
    $$

    证明 $\nabla f(\widetilde x,\widetilde z)=0$。

### 例子

**3.15 一族凹效用函数。** 当 $0<\alpha\leq1$ 时，令

$$
u_\alpha(x)=\frac{x^\alpha-1}{\alpha},
$$

其定义域为 $\operatorname{\mathbf{dom}}u_\alpha=\mathbf{R}_+$。另外定义 $u_0(x)=\log x$，其定义域为 $\operatorname{\mathbf{dom}}u_0=\mathbf{R}_{++}$。

- (a) 证明：当 $x>0$ 时，$u_0(x)=\lim_{\alpha\to0}u_\alpha(x)$。
- (b) <!-- pdf-page: 130 -->证明 $u_\alpha$ 都是凹函数、单调递增，并且都满足 $u_\alpha(1)=0$。

这些函数常用于经济学中，描述一定数量的商品或货币所带来的收益或效用。$u_\alpha$ 的凹性意味着：随着商品数量增加，边际效用（即商品增加固定数量时获得的效用增量）会减小。换句话说，凹性刻画了饱和效应。

**3.16** 对下面每个函数，判断它是否为凸函数、凹函数、拟凸函数或拟凹函数。

- (a) $\mathbf{R}$ 上的 $f(x)=e^x-1$。
- (b) $\mathbf{R}_{++}^2$ 上的 $f(x_1,x_2)=x_1x_2$。
- (c) $\mathbf{R}_{++}^2$ 上的 $f(x_1,x_2)=1/(x_1x_2)$。
- (d) $\mathbf{R}_{++}^2$ 上的 $f(x_1,x_2)=x_1/x_2$。
- (e) $\mathbf{R}\times\mathbf{R}_{++}$ 上的 $f(x_1,x_2)=x_1^2/x_2$。
- (f) $\mathbf{R}_{++}^2$ 上的 $f(x_1,x_2)=x_1^\alpha x_2^{1-\alpha}$，其中 $0\leq\alpha\leq1$。

**3.17** 设 $p<1$、$p\ne0$。证明函数

$$
f(x)=\left(\sum_{i=1}^n x_i^p\right)^{1/p},
$$

其定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n$，是凹函数。这包含特殊情况 $f(x)=(\sum_{i=1}^n x_i^{1/2})^2$，以及调和平均 $f(x)=(\sum_{i=1}^n1/x_i)^{-1}$。**提示：** 参照第 3.1.5 节中指数和的对数函数及几何平均的证明，作适当调整。

**3.18** 参照第 3.1.5 节中对数行列式函数凹性的证明，证明以下结论。

- (a) $f(X)=\operatorname{\mathbf{tr}}(X^{-1})$ 在 $\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n$ 上为凸函数。
- (b) $f(X)=(\det X)^{1/n}$ 在 $\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n$ 上为凹函数。

**3.19 非负加权和与积分。**

- (a) 证明 $f(x)=\sum_{i=1}^r\alpha_i x_{[i]}$ 是 $x$ 的凸函数，其中 $\alpha_1\geq\alpha_2\geq\cdots\geq\alpha_r\geq0$，$x_{[i]}$ 表示 $x$ 的第 $i$ 大分量。可以使用 $f(x)=\sum_{i=1}^k x_{[i]}$ 在 $\mathbf{R}^n$ 上为凸函数这一事实。
- (b) 用 $T(x,\omega)$ 表示三角多项式

    $$
    T(x,\omega)=x_1+x_2\cos\omega+x_3\cos2\omega+\cdots+x_n\cos(n-1)\omega.
    $$

    证明函数

    $$
    f(x)=-\int_0^{2\pi}\log T(x,\omega)\,d\omega
    $$

    在 $\{x\in\mathbf{R}^n\mid T(x,\omega)>0,\ 0\leq\omega\leq2\pi\}$ 上为凸函数。

**3.20 与仿射函数复合。** 证明下列函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数。

- (a) $f(x)=\|Ax-b\|$，其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，$\|\cdot\|$ 是 $\mathbf{R}^m$ 上的范数。
- (b) $f(x)=-(\det(A_0+x_1A_1+\cdots+x_nA_n))^{1/m}$，定义在 $\{x\mid A_0+x_1A_1+\cdots+x_nA_n\succ0\}$ 上，其中 $A_i\in\mathbf{S}^m$。
- (c) $f(X)=\operatorname{\mathbf{tr}}(A_0+x_1A_1+\cdots+x_nA_n)^{-1}$，定义在 $\{x\mid A_0+x_1A_1+\cdots+x_nA_n\succ0\}$ 上，其中 $A_i\in\mathbf{S}^m$。使用 $\operatorname{\mathbf{tr}}(X^{-1})$ 在 $\mathbf{S}_{++}^m$ 上为凸函数这一事实，见习题 3.18。

<div class="translator-note" markdown="1">

**译注（习题 3.20(c)）：** 本小问开头的 $f(X)$ 沿用了原书记号；根据题首的 $f:\mathbf{R}^n\to\mathbf{R}$、右侧的分量 $x_i$ 和定义域，自变量应读作向量 $x$。提示中 $\operatorname{\mathbf{tr}}(X^{-1})$ 的 $X$ 则是正定矩阵。

</div>

<!-- pdf-page: 131 -->

**3.21 逐点最大值与上确界。** 证明下列函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数。

- (a) $f(x)=\max_{i=1,\ldots,k}\|A^{(i)}x-b^{(i)}\|$，其中 $A^{(i)}\in\mathbf{R}^{m\times n}$、$b^{(i)}\in\mathbf{R}^m$，$\|\cdot\|$ 是 $\mathbf{R}^m$ 上的范数。
- (b) $\mathbf{R}^n$ 上的 $f(x)=\sum_{i=1}^r|x|_{[i]}$，其中 $|x|$ 表示分量为 $|x|_i=|x_i|$ 的向量，即逐分量取 $x$ 的绝对值；$|x|_{[i]}$ 是 $|x|$ 的第 $i$ 大分量。换句话说，$|x|_{[1]},|x|_{[2]},\ldots,|x|_{[n]}$ 是按非增次序排列的 $x$ 各分量的绝对值。

**3.22 复合规则。** 证明下列函数是凸函数。

- (a) $f(x)=-\log(-\log(\sum_{i=1}^m e^{a_i^Tx+b_i}))$，定义域为 $\operatorname{\mathbf{dom}}f=\{x\mid\sum_{i=1}^m e^{a_i^Tx+b_i}<1\}$。可以使用 $\log(\sum_{i=1}^n e^{y_i})$ 是凸函数这一事实。
- (b) $f(x,u,v)=-\sqrt{uv-x^Tx}$，定义域为 $\operatorname{\mathbf{dom}}f=\{(x,u,v)\mid uv>x^Tx,\ u,v>0\}$。使用以下事实：当 $u>0$ 时，$x^Tx/u$ 关于 $(x,u)$ 为凸函数；$-\sqrt{x_1x_2}$ 在 $\mathbf{R}_{++}^2$ 上为凸函数。
- (c) $f(x,u,v)=-\log(uv-x^Tx)$，定义域为 $\operatorname{\mathbf{dom}}f=\{(x,u,v)\mid uv>x^Tx,\ u,v>0\}$。
- (d) $f(x,t)=-(t^p-\|x\|_p^p)^{1/p}$，其中 $p>1$，定义域为 $\operatorname{\mathbf{dom}}f=\{(x,t)\mid t\geq\|x\|_p\}$。可以使用以下事实：当 $u>0$ 时，$\|x\|_p^p/u^{p-1}$ 关于 $(x,u)$ 为凸函数（见习题 3.23）；$-x^{1/p}y^{1-1/p}$ 在 $\mathbf{R}_+^2$ 上为凸函数（见习题 3.16）。
- (e) $f(x,t)=-\log(t^p-\|x\|_p^p)$，其中 $p>1$，定义域为 $\operatorname{\mathbf{dom}}f=\{(x,t)\mid t>\|x\|_p\}$。可以使用以下事实：当 $u>0$ 时，$\|x\|_p^p/u^{p-1}$ 关于 $(x,u)$ 为凸函数，见习题 3.23。

**3.23 函数的透视。**

- (a) 证明：当 $p>1$ 时，

    $$
    f(x,t)=\frac{|x_1|^p+\cdots+|x_n|^p}{t^{p-1}}=\frac{\|x\|_p^p}{t^{p-1}}
    $$

    在 $\{(x,t)\mid t>0\}$ 上为凸函数。

- (b) 证明

    $$
    f(x)=\frac{\|Ax+b\|_2^2}{c^Tx+d}
    $$

    在 $\{x\mid c^Tx+d>0\}$ 上为凸函数，其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$、$c\in\mathbf{R}^n$、$d\in\mathbf{R}$。

**3.24 概率单纯形上的一些函数。** 设实值随机变量 $x$ 取值于 $\{a_1,\ldots,a_n\}$，其中 $a_1<a_2<\cdots<a_n$，且 $\operatorname{\mathbf{prob}}(x=a_i)=p_i$，$i=1,\ldots,n$。对于下面每个关于 $p$ 的函数（定义在概率单纯形 $\{p\in\mathbf{R}_+^n\mid\mathbf{1}^Tp=1\}$ 上），判断它是否为凸函数、凹函数、拟凸函数或拟凹函数。

- (a) $\mathbf{E}x$。
- (b) $\operatorname{\mathbf{prob}}(x\geq\alpha)$。
- (c) $\operatorname{\mathbf{prob}}(\alpha\leq x\leq\beta)$。
- (d) $\sum_{i=1}^n p_i\log p_i$，即该分布的负熵。
- (e) $\operatorname{\mathbf{var}}x=\mathbf{E}(x-\mathbf{E}x)^2$。
- (f) $\operatorname{\mathbf{quartile}}(x)=\inf\{\beta\mid\operatorname{\mathbf{prob}}(x\leq\beta)\geq0.25\}$。
- (g) 概率不小于 90% 的最小集合 $A\subseteq\{a_1,\ldots,a_n\}$ 的基数。这里，基数是指 $A$ 中元素的个数。
- (h) 包含 90% 概率的区间的最小宽度，即

    $$
    \inf\{\beta-\alpha\mid\operatorname{\mathbf{prob}}(\alpha\leq x\leq\beta)\geq0.9\}.
    $$

<!-- pdf-page: 132 -->

**3.25 分布之间的最大概率距离。** 设 $p,q\in\mathbf{R}^n$ 表示 $\{1,\ldots,n\}$ 上的两个概率分布，因此 $p,q\succeq0$、$\mathbf{1}^Tp=\mathbf{1}^Tq=1$。定义 $p$ 与 $q$ 之间的**最大概率距离** $d_{\mathrm{mp}}(p,q)$ 为：遍历所有事件时，$p$ 与 $q$ 赋予该事件的概率之差的绝对值的最大值，

$$
d_{\mathrm{mp}}(p,q)=\max\{|\operatorname{\mathbf{prob}}(p,C)-\operatorname{\mathbf{prob}}(q,C)|\mid C\subseteq\{1,\ldots,n\}\}.
$$

这里，$\operatorname{\mathbf{prob}}(p,C)$ 是分布 $p$ 下事件 $C$ 的概率，即 $\operatorname{\mathbf{prob}}(p,C)=\sum_{i\in C}p_i$。

用 $\|p-q\|_1=\sum_{i=1}^n|p_i-q_i|$ 给出 $d_{\mathrm{mp}}$ 的简单表达式，并证明 $d_{\mathrm{mp}}$ 是 $\mathbf{R}^n\times\mathbf{R}^n$ 上的凸函数。它的定义域是 $\{(p,q)\mid p,q\succeq0,\ \mathbf{1}^Tp=\mathbf{1}^Tq=1\}$，但可以自然地延拓到整个 $\mathbf{R}^n\times\mathbf{R}^n$。

**3.26 更多特征值函数。** 用 $\lambda_1(X)\geq\lambda_2(X)\geq\cdots\geq\lambda_n(X)$ 表示矩阵 $X\in\mathbf{S}^n$ 的特征值。前面已经见过一些由特征值构成、关于 $X$ 为凸或凹的函数。

- 最大特征值 $\lambda_1(X)$ 是凸函数，见例 3.10。最小特征值 $\lambda_n(X)$ 是凹函数。
- 特征值之和，也就是迹，$\operatorname{\mathbf{tr}}X=\lambda_1(X)+\cdots+\lambda_n(X)$，是线性函数。
- 特征值倒数之和，也就是逆矩阵的迹，$\operatorname{\mathbf{tr}}(X^{-1})=\sum_{i=1}^n1/\lambda_i(X)$，在 $\mathbf{S}_{++}^n$ 上为凸函数，见习题 3.18。
- 特征值的几何平均 $(\det X)^{1/n}=(\prod_{i=1}^n\lambda_i(X))^{1/n}$，以及特征值乘积的对数 $\log\det X=\sum_{i=1}^n\log\lambda_i(X)$，关于 $X\in\mathbf{S}_{++}^n$ 都是凹函数，见习题 3.18 和第 74 页。

本题利用变分刻画，讨论更多特征值函数。

- (a) **最大的 $k$ 个特征值之和。** 证明 $\sum_{i=1}^k\lambda_i(X)$ 在 $\mathbf{S}^n$ 上为凸函数。**提示：** [HJ85, 第 191 页] 使用变分刻画

    $$
    \sum_{i=1}^k\lambda_i(X)=\sup\{\operatorname{\mathbf{tr}}(V^TXV)\mid V\in\mathbf{R}^{n\times k},\ V^TV=I\}.
    $$

- (b) **最小的 $k$ 个特征值的几何平均。** 证明 $(\prod_{i=n-k+1}^n\lambda_i(X))^{1/k}$ 在 $\mathbf{S}_{++}^n$ 上为凹函数。**提示：** [MO79, 第 513 页] 对于 $X\succ0$，有

    $$
    \left(\prod_{i=n-k+1}^n\lambda_i(X)\right)^{1/k}
    =\frac1k\inf\{\operatorname{\mathbf{tr}}(V^TXV)\mid V\in\mathbf{R}^{n\times k},\ \det V^TV=1\}.
    $$

- (c) **最小的 $k$ 个特征值乘积的对数。** 证明 $\sum_{i=n-k+1}^n\log\lambda_i(X)$ 在 $\mathbf{S}_{++}^n$ 上为凹函数。**提示：** [MO79, 第 513 页] 对于 $X\succ0$，有

    $$
    \prod_{i=n-k+1}^n\lambda_i(X)=\inf\left\{\prod_{i=1}^k(V^TXV)_{ii}\ \middle|\ V\in\mathbf{R}^{n\times k},\ V^TV=I\right\}.
    $$

**3.27 Cholesky 因子的对角元素。** 每个 $X\in\mathbf{S}_{++}^n$ 都有唯一的 Cholesky 分解 $X=LL^T$，其中 $L$ 是下三角矩阵，且 $L_{ii}>0$。证明 $L_{ii}$ 是 $X$ 的凹函数，定义域为 $\mathbf{S}_{++}^n$。

**提示：** $L_{ii}$ 可以表示为 $L_{ii}=(w-z^TY^{-1}z)^{1/2}$，其中

$$
\begin{bmatrix}Y&z\\z^T&w\end{bmatrix}
$$

是 $X$ 左上角的 $i\times i$ 子矩阵。

<!-- pdf-page: 133 -->

### 保持凸性的运算

**3.28 将凸函数表示为一族仿射函数的逐点上确界。** 本题把第 83 页证明的结论推广到 $\operatorname{\mathbf{dom}}f\ne\mathbf{R}^n$ 的情形。设 $f:\mathbf{R}^n\to\mathbf{R}$ 是凸函数。将 $\widetilde f:\mathbf{R}^n\to\mathbf{R}$ 定义为 $f$ 的所有仿射全局下界函数的逐点上确界：

$$
\widetilde f(x)=\sup\{g(x)\mid g\text{ 为仿射函数，且对所有 }z\text{ 有 }g(z)\leq f(z)\}.
$$

- (a) 证明：对于 $x\in\operatorname{\mathbf{int}}\operatorname{\mathbf{dom}}f$，有 $f(x)=\widetilde f(x)$。
- (b) 证明：如果 $f$ 是闭的，即 $\operatorname{\mathbf{epi}}f$ 是闭集（见第 A.3.3 节），那么 $f=\widetilde f$。

**3.29 分段线性凸函数的表示。** 设凸函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}^n$。如果存在 $\mathbf{R}^n$ 的一个划分

$$
\mathbf{R}^n=X_1\cup X_2\cup\cdots\cup X_L,
$$

其中 $\operatorname{\mathbf{int}}X_i\ne\varnothing$，且当 $i\ne j$ 时，$\operatorname{\mathbf{int}}X_i\cap\operatorname{\mathbf{int}}X_j=\varnothing$；同时存在一族仿射函数 $a_1^Tx+b_1,\ldots,a_L^Tx+b_L$，使得当 $x\in X_i$ 时有 $f(x)=a_i^Tx+b_i$，就称 $f$ 是**分段线性的**。

证明这样的函数具有形式 $f(x)=\max\{a_1^Tx+b_1,\ldots,a_L^Tx+b_L\}$。

**3.30 函数的凸包或凸包络。** 函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的**凸包**或**凸包络**定义为

$$
g(x)=\inf\{t\mid(x,t)\in\operatorname{\mathbf{conv}}\operatorname{\mathbf{epi}}f\}.
$$

从几何上看，$g$ 的上图是 $f$ 的上图的凸包。

证明 $g$ 是 $f$ 的最大凸下界函数。换句话说，证明：如果 $h$ 是凸函数，并且对所有 $x$ 都有 $h(x)\leq f(x)$，那么对所有 $x$ 都有 $h(x)\leq g(x)$。

**3.31** [Roc70, 第 35 页] **最大的齐次下界函数。** 设 $f$ 是凸函数。定义函数 $g$ 为

$$
g(x)=\inf_{\alpha>0}\frac{f(\alpha x)}{\alpha}.
$$

- (a) 证明 $g$ 是齐次的，即对所有 $t\geq0$，都有 $g(tx)=tg(x)$。
- (b) 证明 $g$ 是 $f$ 的最大齐次下界函数：如果 $h$ 是齐次的，且对所有 $x$ 都有 $h(x)\leq f(x)$，那么对所有 $x$ 都有 $h(x)\leq g(x)$。
- (c) 证明 $g$ 是凸函数。

**3.32 凸函数的乘积与比值。** 一般来说，两个凸函数的乘积或比值不一定为凸函数。不过，对于 $\mathbf{R}$ 上的函数，有一些适用的结论。证明以下各项。

- (a) 如果 $f$ 和 $g$ 是某一区间上的正值凸函数，并且二者都非减或都非增，那么 $fg$ 是凸函数。
- (b) 如果 $f$、$g$ 都是正值凹函数，其中一个非减、另一个非增，那么 $fg$ 是凹函数。
- (c) 如果 $f$ 是非减的正值凸函数，$g$ 是非增的正值凹函数，那么 $f/g$ 是凸函数。

**3.33 透视定理的直接证明。** 直接证明：凸函数 $f$ 的透视函数 $g$（定义见第 3.2.6 节）是凸函数。具体来说，证明 $\operatorname{\mathbf{dom}}g$ 是凸集，并且对 $(x,t),(y,s)\in\operatorname{\mathbf{dom}}g$ 及 $0\leq\theta\leq1$，有

$$
g(\theta x+(1-\theta)y,\theta t+(1-\theta)s)\leq\theta g(x,t)+(1-\theta)g(y,s).
$$

**3.34 Minkowski 函数。** 凸集 $C$ 的 Minkowski 函数定义为

$$
M_C(x)=\inf\{t>0\mid t^{-1}x\in C\}.
$$

<!-- pdf-page: 134 -->

- (a) 画图，从几何上解释如何求出 $M_C(x)$。
- (b) 证明 $M_C$ 是齐次的，即当 $\alpha\geq0$ 时，$M_C(\alpha x)=\alpha M_C(x)$。
- (c) $\operatorname{\mathbf{dom}}M_C$ 是什么？
- (d) 证明 $M_C$ 是凸函数。
- (e) 进一步假设 $C$ 是闭集、有界、对称（若 $x\in C$，则 $-x\in C$），并且内部非空。证明 $M_C$ 是范数。对应的单位球是什么？

**3.35 支撑函数的运算。** 回顾集合 $C\subseteq\mathbf{R}^n$ 的支撑函数定义为 $S_C(y)=\sup\{y^Tx\mid x\in C\}$。第 81 页已经证明 $S_C$ 是凸函数。

- (a) 证明 $S_B=S_{\operatorname{\mathbf{conv}}B}$。
- (b) 证明 $S_{A+B}=S_A+S_B$。
- (c) 证明 $S_{A\cup B}=\max\{S_A,S_B\}$。
- (d) 设 $B$ 是闭凸集。证明 $A\subseteq B$ 当且仅当对所有 $y$，都有 $S_A(y)\leq S_B(y)$。

### 共轭函数

**3.36** 推导下列函数的共轭函数。

- (a) **最大值函数。** $\mathbf{R}^n$ 上的 $f(x)=\max_{i=1,\ldots,n}x_i$。
- (b) **最大元素之和。** $\mathbf{R}^n$ 上的 $f(x)=\sum_{i=1}^r x_{[i]}$。
- (c) **$\mathbf{R}$ 上的分段线性函数。** $\mathbf{R}$ 上的 $f(x)=\max_{i=1,\ldots,m}(a_i x+b_i)$。可以假设各个 $a_i$ 已按递增次序排列，即 $a_1\leq\cdots\leq a_m$，并且没有任何一个函数 $a_i x+b_i$ 是冗余的，即对每个 $k$，都至少存在一个 $x$，使 $f(x)=a_kx+b_k$。
- (d) **幂函数。** $\mathbf{R}_{++}$ 上的 $f(x)=x^p$，其中 $p>1$。再对 $p<0$ 的情形求解。
- (e) **负几何平均。** $\mathbf{R}_{++}^n$ 上的 $f(x)=-(\prod_i x_i)^{1/n}$。
- (f) **二阶锥的负广义对数。** $\{(x,t)\in\mathbf{R}^n\times\mathbf{R}\mid\|x\|_2<t\}$ 上的 $f(x,t)=-\log(t^2-x^Tx)$。

**3.37** 证明 $f(X)=\operatorname{\mathbf{tr}}(X^{-1})$，$\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n$，的共轭函数为

$$
f^*(Y)=-2\operatorname{\mathbf{tr}}(-Y)^{1/2},\qquad\operatorname{\mathbf{dom}}f^*=-\mathbf{S}_+^n.
$$

**提示：** $f$ 的梯度为 $\nabla f(X)=-X^{-2}$。

**3.38 Young 不等式。** 设 $f:\mathbf{R}\to\mathbf{R}$ 是递增函数，$f(0)=0$，并令 $g$ 为其反函数。定义 $F$ 和 $G$ 为

$$
F(x)=\int_0^x f(a)\,da,\qquad G(y)=\int_0^y g(a)\,da.
$$

证明 $F$ 和 $G$ 互为共轭函数。给出 Young 不等式

$$
xy\leq F(x)+G(y)
$$

的简单图形解释。

**3.39 共轭函数的性质。**

- (a) **凸函数加仿射函数的共轭。** 定义 $g(x)=f(x)+c^Tx+d$，其中 $f$ 为凸函数。用 $f^*$ 以及 $c,d$ 表示 $g^*$。
- (b) **透视函数的共轭。** 用 $f^*$ 表示凸函数 $f$ 的透视函数的共轭。
- (c) <!-- pdf-page: 135 -->**共轭与最小化。** 设 $f(x,z)$ 关于 $(x,z)$ 是凸函数，定义 $g(x)=\inf_z f(x,z)$。用 $f^*$ 表示共轭函数 $g^*$。

    作为应用，对 $g(x)=\inf_z\{h(z)\mid Az+b=x\}$，其中 $h$ 是凸函数，用 $h^*$、$A$ 和 $b$ 表示它的共轭函数。

- (d) **共轭函数的共轭。** 证明闭凸函数的共轭再取共轭后得到它自身：如果 $f$ 是闭凸函数，那么 $f=f^{**}$。函数为闭的，是指它的上图为闭集，见第 A.3.3 节。**提示：** 证明 $f^{**}$ 是 $f$ 的所有仿射全局下界函数的逐点上确界，再应用习题 3.28 的结论。

**3.40 共轭函数的梯度与 Hessian 矩阵。** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 是二阶连续可微的凸函数。假设 $\bar y$ 和 $\bar x$ 满足关系 $\bar y=\nabla f(\bar x)$，且 $\nabla^2f(\bar x)\succ0$。

- (a) 证明 $\nabla f^*(\bar y)=\bar x$。
- (b) 证明 $\nabla^2f^*(\bar y)=\nabla^2f(\bar x)^{-1}$。

**3.41 负归一化熵的共轭。** 证明负归一化熵

$$
f(x)=\sum_{i=1}^n x_i\log(x_i/\mathbf{1}^Tx),
$$

其定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n$，的共轭函数为

$$
f^*(y)=\begin{cases}
0&\displaystyle\sum_{i=1}^n e^{y_i}\leq1\\
+\infty&\text{否则}.
\end{cases}
$$

### 拟凸函数

**3.42 逼近宽度。** 设 $f_0,\ldots,f_n:\mathbf{R}\to\mathbf{R}$ 是给定的连续函数。考虑用 $f_1,\ldots,f_n$ 的线性组合来逼近 $f_0$ 的问题。对于 $x\in\mathbf{R}^n$，如果当 $0\leq t\leq T$ 时，都有 $|f(t)-f_0(t)|\leq\epsilon$，就说 $f=x_1f_1+\cdots+x_nf_n$ 在区间 $[0,T]$ 上以容差 $\epsilon>0$ 逼近 $f_0$。现在固定容差 $\epsilon>0$，将**逼近宽度**定义为使 $f$ 在区间 $[0,T]$ 上逼近 $f_0$ 的最大 $T$：

$$
W(x)=\sup\{T\mid|x_1f_1(t)+\cdots+x_nf_n(t)-f_0(t)|\leq\epsilon\text{ 对 }0\leq t\leq T\text{ 成立}\}.
$$

证明 $W$ 是拟凹函数。

**3.43 拟凸性的一阶条件。** 证明第 3.4.3 节给出的拟凸性一阶条件：定义域 $\operatorname{\mathbf{dom}}f$ 为凸集的可微函数 $f:\mathbf{R}^n\to\mathbf{R}$ 是拟凸函数，当且仅当对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
f(y)\leq f(x)\quad\Longrightarrow\quad\nabla f(x)^T(y-x)\leq0.
$$

**提示：** 只需证明 $\mathbf{R}$ 上函数的情形；通过把函数限制在任意一条直线上，即可得到一般结论。

**3.44 拟凸性的二阶条件。** 本题推导第 3.4.3 节给出的拟凸性二阶条件的其他表示形式。证明以下各项。

- (a) 如果存在 $\sigma$，使得

    $$
    \nabla^2f(x)+\sigma\nabla f(x)\nabla f(x)^T\succeq0,
    \tag{3.26}
    $$

    那么点 $x\in\operatorname{\mathbf{dom}}f$ 满足 (3.21)。该点对所有 $y\ne0$ 满足 (3.22)，当且仅当存在 $\sigma$，使得

    $$
    \nabla^2f(x)+\sigma\nabla f(x)\nabla f(x)^T\succ0.
    \tag{3.27}
    $$

    **提示：** 不失一般性，可以假设 $\nabla^2f(x)$ 是对角矩阵。

- (b) <!-- pdf-page: 136 -->点 $x\in\operatorname{\mathbf{dom}}f$ 满足 (3.21)，当且仅当以下两种情况之一成立：$\nabla f(x)=0$ 且 $\nabla^2f(x)\succeq0$；或者 $\nabla f(x)\ne0$，且矩阵

    $$
    H(x)=\begin{bmatrix}\nabla^2f(x)&\nabla f(x)\\\nabla f(x)^T&0\end{bmatrix}
    $$

    恰好有一个负特征值。该点对所有 $y\ne0$ 满足 (3.22)，当且仅当 $H(x)$ 恰好有一个非正特征值。

    **提示：** 可以使用 (a) 的结论。下面这个来自线性代数中特征值交错定理的结论也可能有用：如果 $B\in\mathbf{S}^n$、$a\in\mathbf{R}^n$，那么

    $$
    \lambda_n\left(\begin{bmatrix}B&a\\a^T&0\end{bmatrix}\right)\geq\lambda_n(B).
    $$

**3.45** 利用第 3.4.3 节给出的拟凸性一阶与二阶条件，验证函数 $f(x)=-x_1x_2$，$\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^2$，的拟凸性。

**3.46 定义域为 $\mathbf{R}^n$ 的拟线性函数。** $\mathbf{R}$ 上的拟线性函数，即既拟凸又拟凹的函数，一定是单调的，也就是非减或非增。本题考虑把这个结论推广到 $\mathbf{R}^n$ 上的函数。

设函数 $f:\mathbf{R}^n\to\mathbf{R}$ 连续且拟线性，$\operatorname{\mathbf{dom}}f=\mathbf{R}^n$。证明它可以表示为 $f(x)=g(a^Tx)$，其中 $g:\mathbf{R}\to\mathbf{R}$ 单调，$a\in\mathbf{R}^n$。换句话说，定义域为 $\mathbf{R}^n$ 的拟线性函数，一定是对一个线性函数再施加一个单调函数得到的。逆命题也成立。

### 对数凹函数与对数凸函数

**3.47** 设 $f:\mathbf{R}^n\to\mathbf{R}$ 可微，$\operatorname{\mathbf{dom}}f$ 为凸集，且对所有 $x\in\operatorname{\mathbf{dom}}f$ 都有 $f(x)>0$。证明 $f$ 是对数凹函数，当且仅当对所有 $x,y\in\operatorname{\mathbf{dom}}f$，都有

$$
\frac{f(y)}{f(x)}\leq\exp\left(\frac{\nabla f(x)^T(y-x)}{f(x)}\right).
$$

**3.48** 证明：如果 $f:\mathbf{R}^n\to\mathbf{R}$ 是对数凹函数且 $a\geq0$，那么函数 $g=f-a$ 也是对数凹函数，其中 $\operatorname{\mathbf{dom}}g=\{x\in\operatorname{\mathbf{dom}}f\mid f(x)>a\}$。

**3.49** 证明下列函数具有对数凹性。

- (a) **Logistic 函数：** $f(x)=e^x/(1+e^x)$，$\operatorname{\mathbf{dom}}f=\mathbf{R}$。
- (b) **调和平均：**

    $$
    f(x)=\frac{1}{1/x_1+\cdots+1/x_n},\qquad\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n.
    $$

- (c) **乘积除以和：**

    $$
    f(x)=\frac{\prod_{i=1}^n x_i}{\sum_{i=1}^n x_i},\qquad\operatorname{\mathbf{dom}}f=\mathbf{R}_{++}^n.
    $$

- (d) **行列式除以迹：**

    $$
    f(X)=\frac{\det X}{\operatorname{\mathbf{tr}}X},\qquad\operatorname{\mathbf{dom}}f=\mathbf{S}_{++}^n.
    $$

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

其中 $\operatorname{\mathbf{dom}}S_k\in\mathbf{R}_+^n$、$1\leq k\leq n$，称为 $\mathbf{R}^n$ 上的第 $k$ 个初等对称函数。可以证明，$S_k^{1/k}$ 是凹函数（见 [ML57]）。

<div class="translator-note" markdown="1">

**译注（习题 3.50）：** 定义域是一个集合，原式中的 $\in$ 是记号笔误。按上下文，这里是在非负正交锥 $\mathbf{R}_+^n$ 上讨论函数 $S_k$。

</div>

**3.51** [BL00, 第 41 页] 设 $p$ 是 $\mathbf{R}$ 上的一个多项式，它的所有根都是实数。证明：在 $p$ 为正的任意区间上，$p$ 都是对数凹的。

**3.52** [MO79, 第 3.E.2 节] **矩函数的对数凸性。** 设 $f:\mathbf{R}\to\mathbf{R}$ 是一个非负函数，且 $\mathbf{R}_+\subseteq\operatorname{\mathbf{dom}}f$。对于 $x\geq0$，定义

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

    其中 $\operatorname{\mathbf{dom}}f=\mathbf{R}_+$，$\lambda\geq1$，$\alpha>0$。

- (b) [MO79, 第 306 页] Dirichlet 密度

    $$
    f(x)=\frac{\Gamma(\mathbf{1}^T\lambda)}{\Gamma(\lambda_1)\cdots\Gamma(\lambda_{n+1})}x_1^{\lambda_1-1}\cdots x_n^{\lambda_n-1}\left(1-\sum_{i=1}^n x_i\right)^{\lambda_{n+1}-1},
    $$

    其中 $\operatorname{\mathbf{dom}}f=\{x\in\mathbf{R}_{++}^n\mid\mathbf{1}^Tx<1\}$，参数为 $\lambda\succeq\mathbf{1}$。

### 关于广义不等式的凸性

**3.57** 证明：$f(X)=X^{-1}$ 在 $\mathbf{S}_{++}^n$ 上是矩阵凸的。

**3.58 Schur 补。** 设 $X\in\mathbf{S}^n$，并将其分块为

$$
X=\begin{bmatrix}A&B\\B^T&C\end{bmatrix},
$$

其中 $A\in\mathbf{S}^k$。$X$ 关于 $A$ 的 Schur 补为 $S=C-B^TA^{-1}B$（见第 A.5.5 节）。证明：把 Schur 补看作从 $\mathbf{S}^n$ 到 $\mathbf{S}^{n-k}$ 的函数时，它在 $\mathbf{S}_{++}^n$ 上是矩阵凹的。

**3.59 $K$-凸性的二阶条件。** 设 $K\subseteq\mathbf{R}^m$ 是正常凸锥，其对应的广义不等式为 $\preceq_K$。证明：对于定义域为凸集的二阶可微函数 $f:\mathbf{R}^n\to\mathbf{R}^m$，$f$ 是 $K$-凸函数，当且仅当对所有 $x\in\operatorname{\mathbf{dom}}f$ 和 $y\in\mathbf{R}^n$，都有

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
\operatorname{\mathbf{epi}}_K f=\{(x,t)\in\mathbf{R}^{n+m}\mid f(x)\preceq_K t\}.
$$

证明以下各项。

- (a) 如果 $f$ 是 $K$-凸函数，那么对所有 $\alpha\in\mathbf{R}^m$，$C_\alpha$ 都是凸集。
- (b) $f$ 是 $K$-凸函数，当且仅当 $\operatorname{\mathbf{epi}}_K f$ 是凸集。

<!-- pdf-page: 140 -->
