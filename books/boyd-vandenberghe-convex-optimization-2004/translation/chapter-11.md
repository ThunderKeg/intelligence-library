<!-- pdf-page: 575 -->

# 第 11 章 内点法

<aside class="chapter-guide"><p>导读（编者）：本章进一步处理带不等式约束的问题。对数障碍函数把约束纳入目标函数，中心路径则把一系列较易求解的问题连接起来。阅读时重点理解障碍参数、对偶间隙和停止准则之间的关系，再看这些关系如何用于障碍法与原始–对偶内点法的设计和实现。</p></aside>

## 11.1 不等式约束最小化问题

本章讨论求解含不等式约束的凸优化问题的*内点法*：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
\tag{11.1}
$$

其中 $f_0,\ldots,f_m:\mathbf{R}^n\to\mathbf{R}$ 为凸函数且二阶连续可微，$A\in\mathbf{R}^{p\times n}$，并且 $\mathbf{rank}\,A=p<n$。假设问题可解，即存在最优解 $x^\star$。用 $p^\star$ 表示最优值 $f_0(x^\star)$。

还假设问题严格可行，即存在 $x\in\mathcal{D}$，满足 $Ax=b$，且对 $i=1,\ldots,m$ 都有 $f_i(x)<0$。这意味着 Slater 约束资格条件成立，所以存在对偶最优解 $\lambda^\star\in\mathbf{R}^m$、$\nu^\star\in\mathbf{R}^p$，它们与 $x^\star$ 一起满足 KKT 条件

$$
\begin{aligned}
Ax^\star=b,\qquad f_i(x^\star)&\leq0,\quad i=1,\ldots,m\\
\lambda^\star&\succeq0\\
\nabla f_0(x^\star)+\sum_{i=1}^m\lambda_i^\star\nabla f_i(x^\star)+A^T\nu^\star&=0\\
\lambda_i^\star f_i(x^\star)&=0,\quad i=1,\ldots,m.
\end{aligned}
\tag{11.2}
$$

内点法通过对一系列等式约束问题使用牛顿法，或者对一系列修改后的 KKT 条件使用牛顿法，来求解问题 (11.1)（或 KKT 条件 (11.2)）。我们主要介绍一种特定的内点算法——*障碍法*，并给出其收敛性证明和复杂度分析。还将在 §11.7 介绍一种简单的原始–对偶内点法，但不作分析。

可以把内点法看成凸优化算法层次中的更高一层。线性等式约束二次问题最简单，其 KKT 条件是一组线性方程，可以解析求解。牛顿法位于下一层。可以把牛顿法看成这样一种技术：将目标函数二阶可微的线性等式<!-- pdf-page: 576 -->约束优化问题，化为一系列线性等式约束二次问题来求解。内点法又进一步：它把同时含线性等式约束和不等式约束的优化问题，化为一系列线性等式约束问题来求解。

### 例子

许多问题已经具有 (11.1) 的形式，而且满足目标函数和约束函数二阶可微的假设。明显的例子包括 LP、QP、QCQP，以及凸形式的 GP；另一个例子是线性不等式约束熵最大化问题，

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Fx\preceq g\\
& Ax=b,
\end{array}
$$

其定义域为 $\mathcal{D}=\mathbf{R}_{++}^n$。

许多其他问题不具备要求的形式 (11.1)，即目标函数和约束函数不都是二阶可微的，但可以改写为所需形式。前面已经见过许多这样的例子，例如，将无约束凸分段线性最小化问题

$$
\begin{array}{ll}
\text{最小化} & \max_{i=1,\ldots,m}(a_i^Tx+b_i)
\end{array}
$$

（目标函数不可微）转换为 LP

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & a_i^Tx+b_i\leq t,\quad i=1,\ldots,m
\end{array}
$$

（其目标函数和约束函数都是二阶可微的）。

还有一些凸优化问题，例如 SOCP 和 SDP，不容易改写成所需形式，但可以通过将内点法扩展到含广义不等式的问题来处理；§11.6 将介绍这种扩展。

## 11.2 对数障碍函数与中心路径

我们的目标是将不等式约束问题 (11.1) 近似表示成可以应用牛顿法的等式约束问题。第一步是改写问题 (11.1)，把不等式约束隐含在目标函数中：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)+\displaystyle\sum_{i=1}^m I_-(f_i(x))\\
\text{约束条件} & Ax=b,
\end{array}
\tag{11.3}
$$

其中 $I_-:\mathbf{R}\to\mathbf{R}$ 是非正实数集的指示函数，

$$
I_-(u)=\begin{cases}0&u\leq0\\\infty&u>0.\end{cases}
$$

<!-- pdf-page: 577 -->

<figure id="fig-11-1" data-figure="11.1" data-no-english-text="true" data-reader-after="ch11-log-barrier-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-1.png" alt="横轴为 u；虚线沿负半轴的零值水平线和 u=0 的竖线延伸，三条对数障碍近似曲线都经过点 (−1,0)，并在 u 从左侧趋近零时上升。" data-source-page="577" data-source-rect="182,121,384,293">
<figcaption>图 11.1 虚线表示函数 $I_-(u)$，实线表示 $t=0.5,1,2$ 时的函数 $\widehat I_-(u)=-(1/t)\log(-u)$。其中，$t=2$ 的曲线给出了最好的近似。</figcaption>
</figure>

问题 (11.3) 没有不等式约束，但其目标函数（一般而言）不可微，所以不能应用牛顿法。

### 11.2.1 对数障碍

障碍法的基本思路，是用函数

$$
\hat I_-(u)=-(1/t)\log(-u),\qquad \mathbf{dom}\,\hat I_-=-\mathbf{R}_{++}
$$

<p id="ch11-log-barrier-explanation" markdown="1">来近似指示函数 $I_-$，其中参数 $t>0$ 决定近似的精度。与 $I_-$ 一样，函数 $\hat I_-$ 凸且非减，并且（按照我们的约定）在 $u>0$ 时取值为 $\infty$。不过，与 $I_-$ 不同的是，$\hat I_-$ 可微且为闭函数：当 $u$ 增大到 $0$ 时，它趋于 $\infty$。图 11.1 给出函数 $I_-$，以及 $t$ 取几个不同值时的近似 $\hat I_-$。随着 $t$ 增大，近似会更加准确。</p>

在 (11.3) 中用 $\hat I_-$ 替代 $I_-$，得到近似问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)+\displaystyle\sum_{i=1}^m-(1/t)\log(-f_i(x))\\
\text{约束条件} & Ax=b.
\end{array}
\tag{11.4}
$$

这里的目标函数凸且可微；凸性来自 $-(1/t)\log(-u)$ 关于 $u$ 凸且递增这一事实。假设适当的闭性条件成立，就可以用牛顿法求解。

函数

$$
\phi(x)=-\sum_{i=1}^m\log(-f_i(x)),
\tag{11.5}
$$

<!-- pdf-page: 578 -->

其定义域为 $\mathbf{dom}\,\phi=\{x\in\mathbf{R}^n\mid f_i(x)<0,\ i=1,\ldots,m\}$，称为问题 (11.1) 的*对数障碍函数*（logarithmic barrier，或 log barrier）。它的定义域由严格满足 (11.1) 中各不等式约束的点构成。无论正参数 $t$ 取什么值，只要任意一个 $i$ 对应的 $f_i(x)\to0$，对数障碍函数就会无限增大。

当然，问题 (11.4) 只是原问题 (11.3) 的近似，因此马上会产生一个问题：(11.4) 的解能在多大程度上近似原问题 (11.3) 的解？直觉告诉我们，随着参数 $t$ 增大，近似质量会提高；下面很快就会证实这一点。

另一方面，当参数 $t$ 很大时，很难用牛顿法最小化函数 $f_0+(1/t)\phi$，因为在可行集边界附近，它的 Hessian 矩阵变化很快。我们将看到，可以通过求解一系列形如 (11.4) 的问题来绕过这个困难：每一步都增大参数 $t$（从而提高近似精度），并以先前 $t$ 值对应问题的解，作为下一次牛顿最小化的初始点。

为便于后面使用，记下对数障碍函数 $\phi$ 的梯度和 Hessian 矩阵：

$$
\begin{aligned}
\nabla\phi(x)&=\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x),\\
\nabla^2\phi(x)&=\sum_{i=1}^m\frac{1}{f_i(x)^2}\nabla f_i(x)\nabla f_i(x)^T
+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla^2f_i(x)
\end{aligned}
$$

（见 §A.4.2 和 §A.4.4）。

### 11.2.2 中心路径

现在更详细地考察最小化问题 (11.4)。为了简化后面的记号，将目标函数乘以 $t$，考虑具有相同最小点的等价问题

$$
\begin{array}{ll}
\text{最小化} & tf_0(x)+\phi(x)\\
\text{约束条件} & Ax=b.
\end{array}
\tag{11.6}
$$

暂时假设问题 (11.6) 可以用牛顿法求解，特别地，假设对每个 $t>0$，它都有唯一解。（§11.3.3 将更详细地讨论这一假设。）

对 $t>0$，将 (11.6) 的解记为 $x^\star(t)$。与问题 (11.1) 对应的*中心路径*，定义为所有点 $x^\star(t)$（$t>0$）构成的集合，这些点称为*中心点*。中心路径上的点可由如下充要条件刻画：$x^\star(t)$ 严格可行，即满足

$$
Ax^\star(t)=b,\qquad f_i(x^\star(t))<0,\quad i=1,\ldots,m,
$$

并且存在 $\hat\nu\in\mathbf{R}^p$，使

$$
0=t\nabla f_0(x^\star(t))+\nabla\phi(x^\star(t))+A^T\hat\nu
$$

<!-- pdf-page: 579 -->

$$
\begin{aligned}
\quad=t\nabla f_0(x^\star(t))+\sum_{i=1}^m\frac{1}{-f_i(x^\star(t))}\nabla f_i(x^\star(t))+A^T\hat\nu
\end{aligned}
\tag{11.7}
$$

成立。

<div class="example" id="example-11-1" markdown="1">

**例 11.1 不等式形式的线性规划。** 对于不等式形式的 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b,
\end{array}
\tag{11.8}
$$

其对数障碍函数为

$$
\phi(x)=-\sum_{i=1}^m\log(b_i-a_i^Tx),\qquad
\mathbf{dom}\,\phi=\{x\mid Ax\prec b\},
$$

其中 $a_1^T,\ldots,a_m^T$ 是 $A$ 的各行。障碍函数的梯度和 Hessian 矩阵为

$$
\nabla\phi(x)=\sum_{i=1}^m\frac{1}{b_i-a_i^Tx}a_i,\qquad
\nabla^2\phi(x)=\sum_{i=1}^m\frac{1}{(b_i-a_i^Tx)^2}a_ia_i^T,
$$

也可以更简洁地写成

$$
\nabla\phi(x)=A^Td,\qquad \nabla^2\phi(x)=A^T\mathbf{diag}(d)^2A,
$$

其中 $d\in\mathbf{R}^m$ 的各分量为 $d_i=1/(b_i-a_i^Tx)$。由于 $x$ 严格可行，有 $d\succ0$，所以 $\phi$ 的 Hessian 矩阵非奇异，当且仅当 $A$ 的秩为 $n$。中心性条件 (11.7) 为

$$
tc+\sum_{i=1}^m\frac{1}{b_i-a_i^Tx}a_i=tc+A^Td=0.
\tag{11.9}
$$

可以给出中心性条件的一个简单几何解释。在中心路径上的点 $x^\star(t)$ 处，梯度 $\nabla\phi(x^\star(t))$ 垂直于经过 $x^\star(t)$ 的 $\phi$ 的水平集，它必须与 $-c$ 平行。换言之，超平面 $c^Tx=c^Tx^\star(t)$ 与经过 $x^\star(t)$ 的 $\phi$ 的水平集相切。图 11.2 给出了一个 $m=6$、$n=2$ 的例子。

</div>

#### 由中心路径得到对偶点

由 (11.7) 可以推导中心路径的一个重要性质：每个中心点都能给出一个对偶可行点，进而给出最优值 $p^\star$ 的一个下界。具体地，定义

$$
\lambda_i^\star(t)=-\frac{1}{tf_i(x^\star(t))},\quad i=1,\ldots,m,\qquad
\nu^\star(t)=\hat\nu/t.
\tag{11.10}
$$

我们断言，$\lambda^\star(t),\nu^\star(t)$ 这一对点对偶可行。

首先，由于 $f_i(x^\star(t))<0$，$i=1,\ldots,m$，显然有 $\lambda^\star(t)\succ0$。将最优性条件 (11.7) 写成

$$
\nabla f_0(x^\star(t))+\sum_{i=1}^m\lambda_i^\star(t)\nabla f_i(x^\star(t))+A^T\nu^\star(t)=0,
$$

<!-- pdf-page: 580 -->

<figure id="fig-11-2" data-figure="11.2" data-no-english-text="true" data-reader-return-to-example="example-11-1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-2.png" alt="二维线性规划的中心路径位于六条约束边界围成的区域内，趋向顶点 x⋆；图中还有三条虚线等高线、路径上的点 x⋆(10)、该点处的切线和目标方向 c。" data-source-page="580" data-source-rect="237,120,442,261">
<figcaption>图 11.2 一个 $n=2$、$m=6$ 的线性规划的中心路径。虚线表示对数障碍函数 $\phi$ 的三条等高线。当 $t\to\infty$ 时，中心路径收敛到最优点 $x^\star$。图中还标出了中心路径上对应于 $t=10$ 的点。该点处的最优性条件 (11.9) 可以从几何上验证：直线 $c^Tx=c^Tx^\star(10)$ 与经过 $x^\star(10)$ 的 $\phi$ 等高线相切。</figcaption>
</figure>

可见，当 $\lambda=\lambda^\star(t)$、$\nu=\nu^\star(t)$ 时，$x^\star(t)$ 最小化拉格朗日函数

$$
L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m\lambda_if_i(x)+\nu^T(Ax-b),
$$

这意味着 $\lambda^\star(t),\nu^\star(t)$ 是一对对偶可行点。因此，对偶函数 $g(\lambda^\star(t),\nu^\star(t))$ 的值有限，并且

$$
\begin{aligned}
g(\lambda^\star(t),\nu^\star(t))
&=f_0(x^\star(t))+\sum_{i=1}^m\lambda_i^\star(t)f_i(x^\star(t))
+\nu^\star(t)^T(Ax^\star(t)-b)\\
&=f_0(x^\star(t))-m/t.
\end{aligned}
$$

特别地，与 $x^\star(t)$ 和对偶可行点对 $\lambda^\star(t),\nu^\star(t)$ 对应的对偶间隙，恰好就是 $m/t$。由此得到一个重要结论：

$$
f_0(x^\star(t))-p^\star\leq m/t,
$$

即 $x^\star(t)$ 的次优程度不超过 $m/t$。这证实了前面的直觉：当 $t\to\infty$ 时，$x^\star(t)$ 收敛到一个最优点。

<div class="example" id="example-11-2" markdown="1">

**例 11.2 不等式形式的线性规划。** 不等式形式的 LP (11.8) 的对偶为

$$
\begin{array}{ll}
\text{最大化} & -b^T\lambda\\
\text{约束条件} & A^T\lambda+c=0\\
&\lambda\succeq0.
\end{array}
$$

由最优性条件 (11.9)，显然

$$
\lambda_i^\star(t)=\frac{1}{t(b_i-a_i^Tx^\star(t))},\quad i=1,\ldots,m,
$$

<!-- pdf-page: 581 -->

是对偶可行的，其对偶目标值为

$$
-b^T\lambda^\star(t)
=c^Tx^\star(t)+(Ax^\star(t)-b)^T\lambda^\star(t)
=c^Tx^\star(t)-m/t.
$$

</div>

#### 用 KKT 条件解释

也可以把中心路径条件 (11.7) 解释为 KKT 最优性条件 (11.2) 的连续变形。点 $x$ 等于 $x^\star(t)$，当且仅当存在 $\lambda,\nu$，使

$$
\begin{aligned}
Ax=b,\qquad f_i(x)&\leq0,\quad i=1,\ldots,m\\
\lambda&\succeq0\\
\nabla f_0(x)+\sum_{i=1}^m\lambda_i\nabla f_i(x)+A^T\nu&=0\\
-\lambda_if_i(x)&=1/t,\quad i=1,\ldots,m.
\end{aligned}
\tag{11.11}
$$

KKT 条件 (11.2) 与中心性条件 (11.11) 的唯一区别，是互补条件 $-\lambda_if_i(x)=0$ 被替换成了条件 $-\lambda_if_i(x)=1/t$。特别地，当 $t$ 很大时，$x^\star(t)$ 及其对应的对偶点 $\lambda^\star(t),\nu^\star(t)$ “几乎”满足 (11.1) 的 KKT 最优性条件。

#### 力场解释

将严格可行集 $C$ 中的点看作受到保守力作用的质点，就可以给出中心路径的一个简单力学解释。为简单起见，假设没有等式约束。

每个约束都对应一个力，质点处于位置 $x$ 时，这个力为

$$
F_i(x)=-\nabla(-\log(-f_i(x)))=\frac{1}{f_i(x)}\nabla f_i(x).
$$

所有约束产生的总力场，对应的势能就是对数障碍函数 $\phi$。当质点向可行集边界移动时，约束产生的力会强烈地排斥它。

现在再设想一个作用于质点的力，当质点位于 $x$ 时，这个力为

$$
F_0(x)=-t\nabla f_0(x).
$$

这个目标力场把质点拉向负梯度方向，即 $f_0$ 较小的方向。参数 $t$ 调节目标力相对于约束力的大小。

中心点 $x^\star(t)$ 就是质点所受约束力恰好与目标力平衡的位置。随着参数 $t$ 增大，质点会受到更强的力，拉向最优点；但它始终被障碍势能限制在 $C$ 中，因为质点接近边界时，这个势能会趋于无穷。

<div class="example" id="example-11-3" markdown="1">

**例 11.3 不等式形式 LP 的力场解释。** LP (11.8) 的第 $i$ 个约束对应的力场为

$$
F_i(x)=\frac{-a_i}{b_i-a_i^Tx}.
$$

<!-- pdf-page: 582 -->

<figure id="fig-11-3" data-figure="11.3" data-no-english-text="true" data-reader-after="ch11-force-example-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-3.png" alt="左右两图展示中心路径上两个平衡点的受力；粗箭头分别为目标力 −c 和 −3c，其余箭头为约束力，虚线为中心路径。右图的平衡点更靠近最优顶点。" data-source-page="582" data-source-rect="179,120,498,258">
<figcaption>图 11.3 <em>中心路径的力场解释。</em> 虚线表示中心路径。左、右图中的圆点分别表示 $x^\star(1)$ 和 $x^\star(3)$。目标力分别等于 $-c$ 和 $-3c$，用粗箭头表示。其余箭头表示约束力，其大小服从与距离成反比的规律。随着目标力的强度变化，质点的平衡位置就描出中心路径。</figcaption>
</figure>

这个力沿约束平面 $\mathcal{H}_i=\{x\mid a_i^Tx=b_i\}$ 指向内侧的法线方向，其大小与到 $\mathcal{H}_i$ 的距离成反比，即

$$
\|F_i(x)\|_2=\frac{\|a_i\|_2}{b_i-a_i^Tx}
=\frac{1}{\mathbf{dist}(x,\mathcal{H}_i)}.
$$

换言之，每个约束超平面都对应一个排斥力，大小为到该超平面距离的倒数。

项 $tc^Tx$ 是恒力 $-tc$ 作用于质点时对应的势能。这个“目标力”把质点推向代价较低的方向。因此，$x^\star(t)$ 是质点受到与距离成反比的约束力、以及目标力 $-tc$ 时的平衡位置。当 $t$ 很大时，质点几乎被推到最优点。强大的目标力由方向相反的约束力平衡；由于此时靠近可行集边界，这些约束力也很大。

<p id="ch11-force-example-end" markdown="1">图 11.3 用一个 $n=2$、$m=5$ 的小规模 LP 展示了这种解释。左图给出 $t=1$ 时的 $x^\star(t)$，以及作用于该点、与目标力平衡的约束力。右图给出 $t=3$ 时的 $x^\star(t)$ 及相应的力。目标力增大后，质点会移动到更靠近最优点的位置。</p>

</div>

## 11.3 障碍法

我们已经看到，点 $x^\star(t)$ 的次优程度不超过 $m/t$，而对偶可行点对 $\lambda^\star(t),\nu^\star(t)$ 给出了这一精度的证书。这启发了一种非常直接的方法，可以将原问题 (11.1) 求解到指定精度 $\epsilon$：只需取 $t=m/\epsilon$，并用牛顿法求解等式约束<!-- pdf-page: 583 -->问题

$$
\begin{aligned}
\text{最小化}\quad &(m/\epsilon)f_0(x)+\phi(x)\\
\text{约束为}\quad &Ax=b.
\end{aligned}
$$

这个方法可以称为无约束最小化方法，因为它通过求解一个无约束或线性约束问题，就能把不等式约束问题 (11.1) 求解到有保证的精度。当问题规模较小、初始点较好、精度要求适中（即 $\epsilon$ 不太小）时，这个方法可以表现良好；但在其他情况下，它的表现并不好。因此，这种方法很少使用，甚至几乎从不使用。

### 11.3.1 障碍法

对无约束最小化方法作一个简单扩展，就能得到表现良好的方法。其基本做法是求解一系列无约束（或线性约束）最小化问题，将上一个问题求得的点作为下一个无约束最小化问题的初始点。换言之，我们对一系列递增的 $t$ 值计算 $x^\star(t)$，直到 $t\geq m/\epsilon$；这保证得到了原问题的一个 $\epsilon$ 次优解。Fiacco 和 McCormick 在 20 世纪 60 年代首次提出这种方法时，将它称为序列无约束最小化技术（sequential unconstrained minimization technique，SUMT）。现在通常将它称为障碍法（barrier method）或路径跟随法（path-following method）。下面给出这种方法的一个简单版本。

<div class="algorithm" id="algorithm-11-1" data-algorithm="11.1" markdown="1">

**算法 11.1 障碍法。**

**给定** 严格可行点 $x$、$t:=t^{(0)}>0$、$\mu>1$、容差 $\epsilon>0$。

**重复**

1. **中心化步骤。** 从 $x$ 出发，在约束 $Ax=b$ 下最小化 $tf_0+\phi$，求出 $x^\star(t)$。
2. **更新。** $x:=x^\star(t)$。
3. **停止准则。** 如果 $m/t<\epsilon$，则退出。
4. **增大 $t$。** $t:=\mu t$。

</div>

在每次迭代中（第一次除外），我们从上一次求得的中心点出发，计算中心点 $x^\star(t)$，然后将 $t$ 增大为原来的 $\mu>1$ 倍。算法也可以返回 $\lambda=\lambda^\star(t)$ 和 $\nu=\nu^\star(t)$；这既是一个对偶 $\epsilon$ 次优点，也是 $x$ 的证书。

我们将步骤 1 的每次执行称为一个中心化步骤（centering step，因为该步骤要计算一个中心点），或一次外层迭代；将第一个中心化步骤（计算 $x^\star(t^{(0)})$）称为初始中心化步骤。（因此，取 $t^{(0)}=m/\epsilon$ 的简单算法只包含初始中心化步骤。）虽然步骤 1 可以使用任何线性约束最小化方法，这里仍假设使用牛顿法。中心化步骤中执行的牛顿迭代或牛顿步称为内层迭代。在每个内层步骤中，我们都有一个原可行点；不过，只有在每个外层（中心化）步骤结束时，才有一个对偶可行点。

<!-- pdf-page: 584 -->

#### 中心化精度

对于中心化问题的求解精度，需要作几点说明。没有必要精确地计算 $x^\star(t)$，因为中心路径的意义仅在于：当 $t\to\infty$ 时，它会通向原问题的解；不精确的中心化仍然能产生一个收敛到最优点的点列 $x^{(k)}$。不过，中心化不精确也意味着，用 (11.10) 计算得到的 $\lambda^\star(t),\nu^\star(t)$ 并非精确对偶可行。可以在公式 (11.10) 中加入修正项来弥补这一点：只要算出的 $x$ 接近中心路径上的点 $x^\star(t)$，修正后的公式就能给出对偶可行点（见习题 11.9）。

另一方面，与求出 $tf_0+\phi$ 的一个较好的极小点相比，求出一个精度极高的极小点，计算代价只会略微增加，即最多多做几个牛顿步。因此，假设中心化是精确的并非不合理。

#### $\mu$ 的选择

参数 $\mu$ 的选择涉及所需内层迭代次数和外层迭代次数之间的权衡。如果 $\mu$ 较小（即接近 $1$），则每次外层迭代只会将 $t$ 增大一个较小的倍数。因此，牛顿迭代的初始点，也就是上一次迭代点 $x$，是一个很好的起点，求出下一个迭代点所需的牛顿步数就较少。所以，当 $\mu$ 较小时，我们预期每次外层迭代只需少量牛顿步；但外层迭代次数当然会较多，因为每次外层迭代只使间隙减小一点。在这种情况下，迭代点（实际上也包括内层迭代点）紧贴着中心路径前进。这也解释了它的另一个名称：路径跟随法。

另一方面，如果 $\mu$ 较大，情况就相反。每次外层迭代之后，$t$ 都会大幅增大，所以当前迭代点可能不是下一个迭代点的良好近似。因此，我们预期需要更多的内层迭代。这种“激进”的 $t$ 更新方式会减少外层迭代次数，因为每次外层迭代都把对偶间隙缩小为原来的 $1/\mu$；但内层迭代次数会增多。$\mu$ 较大时，中心路径上相邻迭代点的距离较远，内层迭代点则会明显偏离中心路径。

这种对 $\mu$ 的权衡已经得到实践的证实，后面我们还将看到理论上的证实。在实际计算中，较小的 $\mu$ 值（即接近 $1$）会导致很多次外层迭代，而每次外层迭代只需几个牛顿步。在相当大的范围内，大约从 $3$ 到 $100$ 左右，两种效应几乎相互抵消，因此牛顿步的总数大致不变。这意味着 $\mu$ 的选择并不是特别关键；大约 $10$ 到 $20$ 的取值似乎都表现良好。如果选择参数 $\mu$ 的目的是使所需牛顿步总数的最坏情形界尽可能好，则要采用接近 $1$ 的 $\mu$ 值。

#### $t^{(0)}$ 的选择

另一个重要问题是 $t$ 的初值选择。这里的权衡很简单：如果 $t^{(0)}$ 取得过大，第一次外层迭代就会需要太多次迭代。如果 $t^{(0)}$ 取得过小，算法就会需要额外的外层迭代，而且第一次中心化步骤也可能需要过多的内层迭代。

由于 $m/t^{(0)}$ 是第一次中心化步骤结束后的对偶间隙，一种<!-- pdf-page: 585 -->合理的选择是让 $m/t^{(0)}$ 与 $f_0(x^{(0)})-p^\star$ 或其 $\mu$ 倍大致处于同一数量级。例如，如果已知一个对偶可行点 $\lambda,\nu$，其对偶间隙为 $\eta=f_0(x^{(0)})-g(\lambda,\nu)$，就可以取 $t^{(0)}=m/\eta$。这样，第一次外层迭代只需计算一对点，使它们的对偶间隙与初始原可行点、对偶可行点的间隙相同。

中心路径条件 (11.7) 还启发了另一种选择。我们可以将

$$
\inf_\nu\left\|t\nabla f_0(x^{(0)})+\nabla\phi(x^{(0)})+A^T\nu\right\|_2
\tag{11.12}
$$

看作 $x^{(0)}$ 偏离点 $x^\star(t)$ 程度的度量，并把使 (11.12) 最小的值选作 $t^{(0)}$。（这个 $t$ 值及相应的 $\nu$ 可以通过求解一个最小二乘问题得到。）

这种方法的一个变体，是使用仿射不变的度量代替欧几里得范数，来衡量 $x$ 与 $x^\star(t)$ 之间的偏离。我们选择使下式最小的 $t$ 和 $\nu$：

$$
\alpha(t,\nu)=\left(t\nabla f_0(x^{(0)})+\nabla\phi(x^{(0)})+A^T\nu\right)^T
H_0^{-1}\left(t\nabla f_0(x^{(0)})+\nabla\phi(x^{(0)})+A^T\nu\right),
$$

其中

$$
H_0=t\nabla^2f_0(x^{(0)})+\nabla^2\phi(x^{(0)}).
$$

（可以证明，$\inf_\nu\alpha(t,\nu)$ 是 $tf_0+\phi$ 在 $x^{(0)}$ 处的牛顿减量的平方。）由于 $\alpha$ 是关于 $\nu$ 和 $t$ 的二次除以线性函数，所以它是凸的。

#### 不可行初始点牛顿法

障碍法的一个变体在中心化步骤中使用不可行初始点牛顿法（见 §10.3）。因此，该障碍法的初始点 $x^{(0)}$ 满足 $x^{(0)}\in\mathbf{dom}\,f_0$ 以及 $f_i(x^{(0)})<0$，$i=1,\ldots,m$，但不一定满足 $Ax^{(0)}=b$。假设问题严格可行，则第一次中心化步骤中会在某一步采用完整牛顿步；此后的迭代点就都原可行，算法也就与（标准）障碍法一致。

### 11.3.2 示例

#### 不等式形式的线性规划

第一个例子是一个小规模的不等式形式 LP，

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &Ax\preceq b,
\end{aligned}
$$

其中 $A\in\mathbf{R}^{100\times50}$。数据随机生成，并保证问题原严格可行、对偶严格可行，最优值为 $p^\star=1$。

<p id="ch11-lp-parameters-start" markdown="1">初始点 $x^{(0)}$ 位于中心路径上，对偶间隙为 $100$。我们使用障碍法求解此问题，在对偶间隙小于 $10^{-6}$ 时终止。中心化问题用带回溯的牛顿法求解，参数取 $\alpha=0.01$、$\beta=0.5$。牛顿法的停止准则为</p>

<!-- pdf-page: 586 -->

<figure id="fig-11-4" data-figure="11.4" data-reader-after="ch11-lp-step-tradeoff">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-4.png" alt="小规模线性规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，三条曲线分别标为 μ=50、150、2。" data-source-page="586" data-source-rect="204,122,449,305">
<figcaption>图 11.4 障碍法求解一个小规模线性规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。三条曲线分别对应参数 $\mu$ 的三个取值：$2$、$50$ 和 $150$。每种情况下，对偶间隙都近似线性收敛。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<p id="ch11-lp-parameters-end" markdown="1" data-reader-continue="ch11-lp-parameters-start">$\lambda(x)^2/2\leq10^{-5}$，其中 $\lambda(x)$ 是函数 $tc^Tx+\phi(x)$ 的牛顿减量。</p>

图 11.4 给出了参数 $\mu$ 取三个不同值时障碍法的进展。纵轴用对数刻度表示对偶间隙。横轴表示内层迭代次数，也就是牛顿步数的累计总和，这是衡量计算工作量的自然指标。各条曲线均呈阶梯状，每一级台阶对应一次外层迭代。每级台阶的宽度（即水平部分的长度）是该次外层迭代所需的牛顿步数。每级台阶的高度（即竖直部分的长度）恰好对应 $\mu$ 这一倍数，因为每次外层迭代结束时，对偶间隙都会缩小为原来的 $1/\mu$。

这些曲线展示了障碍法的一些典型特点。首先，这种方法表现很好，对偶间隙近似线性收敛。原因在于，对每个 $\mu$ 值，重新中心化所需的牛顿步数都大致不变。$\mu=50$ 和 $\mu=150$ 时，障碍法只需总计 $35$ 到 $40$ 个牛顿步就能求解该问题。

<p id="ch11-lp-step-tradeoff" markdown="1">图 11.4 中的曲线清楚地展示了选择 $\mu$ 时的权衡。$\mu=2$ 时，台阶较窄；重新中心化大约需要 $2$ 或 $3$ 个牛顿步。但台阶也较矮，因为每次外层迭代只将对偶间隙减半。在另一端，$\mu=150$ 时，台阶较宽，通常约需 $7$ 个牛顿步；但台阶也高得多，因为每次外层迭代都把对偶间隙缩小为原来的 $1/150$。</p>

图 11.5 进一步考察了选择 $\mu$ 时的权衡。我们在 $1.2$ 到 $200$ 之间取 $25$ 个不同的 $\mu$ 值，分别用障碍法求解该 LP，并在对偶间隙小于 $10^{-3}$ 时终止。图中给出了求解问题所需的牛顿步总数随参数 $\mu$ 的变化。

<!-- pdf-page: 587 -->

<figure id="fig-11-5" data-figure="11.5">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-5.png" alt="小规模线性规划所需牛顿迭代总次数随 μ 变化的曲线；μ 接近 1 时次数很高，随后迅速下降，在较大的 μ 范围内仅小幅波动，圆圈标出各个试验值。" data-source-page="587" data-source-rect="159,122,399,304">
<figcaption>图 11.5 一个小规模线性规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。图中表明，当 $\mu$ 大于约 $3$ 时，障碍法表现良好，而在此范围内，其表现对 $\mu$ 的具体取值并不敏感。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

这张图表明，$\mu$ 在大约 $3$ 到 $200$ 的宽广范围内取值时，障碍法都表现很好。正如直觉所预期的那样，当 $\mu$ 太小时，由于需要更多次外层迭代，牛顿步总数会上升。一个有趣的观察是，当 $\mu$ 大于约 $3$ 时，牛顿步总数变化不大。因此，随着 $\mu$ 在这个范围内增大，外层迭代次数的减少，被每次外层迭代所需牛顿步数的增加抵消了。对于更大的 $\mu$ 值，障碍法的表现会更难预测（即更依赖具体的问题实例）。由于继续增大 $\mu$ 并不会改善表现，所以 $10$ 到 $100$ 是一个较好的取值范围。

#### 几何规划

考虑凸形式的几何规划，

$$
\begin{aligned}
\text{最小化}\quad &\log\left(\sum_{k=1}^{K_0}\exp(a_{0k}^Tx+b_{0k})\right)\\
\text{约束为}\quad &\log\left(\sum_{k=1}^{K_i}\exp(a_{ik}^Tx+b_{ik})\right)\leq0,\quad i=1,\ldots,m,
\end{aligned}
$$

变量为 $x\in\mathbf{R}^n$，相应的对数障碍函数为

$$
\phi(x)=-\sum_{i=1}^m\log\left(-\log\sum_{k=1}^{K_i}\exp(a_{ik}^Tx+b_{ik})\right).
$$

<p id="ch11-gp-terms-start" markdown="1">所考察的问题实例有 $n=50$ 个变量、$m=100$ 个不等式（与上面的小规模 LP 相同）。目标函数和约束函数都</p>

<!-- pdf-page: 588 -->

<figure id="fig-11-6" data-figure="11.6" data-reader-after="ch11-gp-step-tradeoff">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-6.png" alt="小规模几何规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=150、50、2。" data-source-page="588" data-source-rect="204,122,453,305">
<figcaption>图 11.6 障碍法求解一个小规模几何规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。这里，对偶间隙同样近似线性收敛。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<p id="ch11-gp-terms-end" markdown="1" data-reader-continue="ch11-gp-terms-start">包含 $K_i=5$ 项。这个问题实例随机生成，并保证其原严格可行、对偶严格可行，最优值为 $1$。</p>

我们从中心路径上的点 $x^{(0)}$ 出发，初始对偶间隙为 $100$。分别取参数 $\mu=2$、$\mu=50$ 和 $\mu=150$，使用障碍法求解问题，并在对偶间隙小于 $10^{-6}$ 时终止。中心化问题用牛顿法求解，参数与 LP 示例相同，即 $\alpha=0.01$、$\beta=0.5$，停止准则为 $\lambda(x)^2/2\leq10^{-5}$。

图 11.6 给出了对偶间隙随累计牛顿步数的变化。这张图与图 11.4 中的 LP 曲线非常相似。特别地，可以看到，每个中心化步骤所需的牛顿步数大致不变，因此对偶间隙近似线性收敛。

<p id="ch11-gp-step-tradeoff" markdown="1">求解问题所需的牛顿步总数随参数 $\mu$ 的变化，也与 LP 示例非常相似。对于这个 GP，当 $\mu$ 在 $10$ 到 $200$ 之间取值时，将对偶间隙降到 $10^{-3}$ 以下所需的牛顿步总数约为 $30$（大约在 $20$ 到 $40$ 之间）。所以在这里，$\mu$ 的一个较好取值范围同样是 $10$ 到 $100$。</p>

#### 一族标准形式 LP

在上面的例子中，我们针对一个随机生成的 LP 实例和一个维度相近的 GP 实例，用对偶间隙随累计牛顿步数的变化考察了障碍法的进展。这两个例子的结果非常相似：两者的对偶间隙都随着牛顿步数增加而近似线性收敛。我们也考察了算法表现随参数 $\mu$ 的变化，两个例子得到的结果基本相同。当 $\mu$ 大于约 $10$ 时，障碍法表现很好，约需 $30$ 个牛顿步就能将对偶间隙从 $10^2$ 降到 $10^{-6}$。在这两个例子中，<!-- pdf-page: 589 -->$\mu$ 的选择几乎不影响所需牛顿步的总数（只要 $\mu$ 大于约 $10$）。

本节考察障碍法的表现如何随问题维度变化。考虑标准形式的 LP，

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &Ax=b,\quad x\succeq0,
\end{aligned}
$$

其中 $A\in\mathbf{R}^{m\times n}$。对一族随机生成的问题实例，我们考察所需牛顿步总数如何随变量个数 $n$ 和等式约束个数 $m$ 变化。取 $n=2m$，即变量数是约束数的两倍。

问题按如下方式生成。$A$ 的元素独立同分布，服从均值为零、方差为一的正态分布 $\mathcal{N}(0,1)$。取 $b=Ax^{(0)}$，其中 $x^{(0)}$ 的各元素独立，并在 $[0,1]$ 上均匀分布。这保证了问题原严格可行，因为 $x^{(0)}\succ0$ 是一个可行点。为了构造代价向量 $c$，我们先生成向量 $z\in\mathbf{R}^m$，其元素服从 $\mathcal{N}(0,1)$ 分布；再生成向量 $s\in\mathbf{R}^n$，其元素服从 $[0,1]$ 上的均匀分布。然后取 $c=A^Tz+s$。这保证了问题对偶严格可行，因为 $A^Tz\prec c$。

算法参数取 $\mu=100$，中心化步骤的参数与前面的例子相同：回溯参数 $\alpha=0.01$、$\beta=0.5$，停止准则为 $\lambda(x)^2/2\leq10^{-5}$。初始点位于 $t^{(0)}=1$ 对应的中心路径点上（即间隙为 $n$）。当初始对偶间隙缩小为原来的 $10^{-4}$，即完成两次外层迭代之后，算法终止。

图 11.7 给出了维度分别为 $m=50$、$m=500$ 和 $m=1000$ 的三个问题实例中，对偶间隙随迭代次数的变化。这些曲线与前面的曲线非常相似，对偶间隙都近似线性收敛。可以看到，当问题规模从 $50$ 个约束（$100$ 个变量）增大到 $1000$ 个约束（$2000$ 个变量）时，所需的牛顿步数只是略有增加。

为了考察问题规模对所需牛顿步数的影响，我们从 $m=10$ 到 $m=1000$ 取 $20$ 个不同的 $m$ 值，对每个值生成 $100$ 个问题实例。用障碍法求解全部 $2000$ 个问题，并记录所需的牛顿步数。结果汇总在图 11.8 中，图中给出了每个 $m$ 值对应的牛顿步数均值和标准差。首先可以看到，标准差约为 $2$ 次迭代，而且似乎基本不受问题规模影响。由于所需步数的均值接近 $25$，这意味着牛顿步数的变化幅度仅约为 $\pm10\%$。

图中显示，问题维度增大到原来的 $100$ 倍时，所需的牛顿步数仅从大约 $21$ 略增到大约 $27$。这种表现一般也是障碍法的典型特点：所需牛顿步数随问题维度增长得非常缓慢，而且几乎总是几十步左右。当然，执行一个牛顿步的计算工作量会随问题维度增大。

<!-- pdf-page: 590 -->

<figure id="fig-11-7" data-figure="11.7">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-7.png" alt="三个标准形式线性规划的阶梯状对偶间隙曲线，分别标为 m=50、500、1000；横轴为累计牛顿迭代次数，问题较大时达到小对偶间隙所需的迭代次数略多。" data-source-page="590" data-source-rect="204,140,468,324">
<figcaption>图 11.7 障碍法求解三个随机生成、规模不同的标准形式线性规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。每个问题的变量个数均为 $n=2m$。这里也可以看到，对偶间隙近似线性收敛；对于较大的问题，所需的牛顿步数略有增加。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<figure id="fig-11-8" data-figure="11.8">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-8.png" alt="横轴 m 从 10 到 1000，采用对数刻度；平均牛顿迭代次数由约 21 次缓慢升至约 27 次，各个圆圈处的竖直误差条表示标准差。" data-source-page="590" data-source-rect="222,436,444,611">
<figcaption>图 11.8 在不同问题规模下，求解 $100$ 个随机生成的线性规划所需的平均牛顿步数，其中 $n=2m$。对于 $m$ 的每个取值，误差条表示平均值上下的标准差。尽管最大与最小问题规模之比为 $100:1$，所需牛顿步数的增长仍很小。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- pdf-page: 591 -->

### 11.3.3 收敛性分析

障碍法的收敛性分析很直接。假设对 $t=t^{(0)},\mu t^{(0)},\mu^2t^{(0)},\ldots$，都能用牛顿法最小化 $tf_0+\phi$，那么在完成初始中心化步骤以及另外 $k$ 个中心化步骤之后，对偶间隙为 $m/(\mu^kt^{(0)})$。因此，除了初始中心化步骤之外，恰好再做

$$
\left\lceil\frac{\log(m/(\epsilon t^{(0)}))}{\log\mu}\right\rceil
\tag{11.13}
$$

个中心化步骤，就能达到所需精度 $\epsilon$。

由此可见，只要在 $t\geq t^{(0)}$ 时都能用牛顿法求解中心化问题 (11.6)，障碍法就能奏效。对于标准牛顿法，一个充分条件是：当 $t\geq t^{(0)}$ 时，函数 $tf_0+\phi$ 满足 §10.2.4（第 529 页）给出的条件，即初始下水平集是闭集、对应的 KKT 矩阵的逆有界，而且 Hessian 矩阵满足 Lipschitz 条件。（另一组基于自协调性的充分条件将在 §11.5 中详细讨论。）如果中心化使用不可行初始点牛顿法，则 §10.3.3（第 536 页）中列出的条件足以保证收敛。

假设 $f_0,\ldots,f_m$ 都是闭函数，对原问题作一个简单修改，就能保证这些条件成立。在问题中加入一个形如 $\|x\|_2^2\leq R^2$ 的约束后，对于每个 $t\geq0$，$tf_0+\phi$ 都是强凸函数；特别地，中心化步骤中牛顿法的收敛性就有了保证。（见习题 11.4。）

虽然这个分析表明，在合理的假设下障碍法确实会收敛，但它没有回答一个基本问题：随着参数 $t$ 增大，中心化问题是否会变得更加困难（因此需要越来越多的迭代）？数值实验表明，对于很多类问题，情况并非如此；即使 $t$ 不断增大，求解中心化问题所需的牛顿步数似乎仍大致不变。我们将在 §11.5 中看到，对于满足某些自协调性条件的问题，这个问题可以得到解答。

### 11.3.4 修正 KKT 方程组的牛顿步

在障碍法中，牛顿步 $\Delta x_{\mathrm{nt}}$ 及相应的对偶变量由以下线性方程组给出：

$$
\begin{bmatrix}
t\nabla^2f_0(x)+\nabla^2\phi(x)&A^T\\
A&0
\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\nu_{\mathrm{nt}}\end{bmatrix}
=-\begin{bmatrix}t\nabla f_0(x)+\nabla\phi(x)\\0\end{bmatrix}.
\tag{11.14}
$$

本节说明，这些用于中心化问题的牛顿步，如何解释为按某种特定方式直接求解修正 KKT 方程组

$$
\begin{aligned}
\nabla f_0(x)+\textstyle\sum_{i=1}^m\lambda_i\nabla f_i(x)+A^T\nu&=0\\
-\lambda_if_i(x)&=1/t,\quad i=1,\ldots,m\\
Ax&=b
\end{aligned}
\tag{11.15}
$$

时的牛顿步。

<!-- pdf-page: 592 -->

修正 KKT 方程组 (11.15) 由关于 $n+p+m$ 个变量 $x,\nu,\lambda$ 的 $n+p+m$ 个非线性方程组成。为了求解它，我们先用 $\lambda_i=-1/(tf_i(x))$ 消去变量 $\lambda_i$，得到

$$
\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla f_i(x)+A^T\nu=0,\qquad Ax=b,
\tag{11.16}
$$

这是关于 $n+p$ 个变量 $x,\nu$ 的 $n+p$ 个方程。

为了求出解非线性方程组 (11.16) 的牛顿步，我们对第一个方程中的非线性项作 Taylor 近似。当 $v$ 较小时，有 Taylor 近似

$$
\begin{aligned}
&\nabla f_0(x+v)+\sum_{i=1}^m\frac{1}{-tf_i(x+v)}\nabla f_i(x+v)\\
&\quad\approx\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla f_i(x)+\nabla^2f_0(x)v\\
&\qquad+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla^2f_i(x)v
+\sum_{i=1}^m\frac{1}{tf_i(x)^2}\nabla f_i(x)\nabla f_i(x)^Tv.
\end{aligned}
$$

将 (11.16) 中的非线性项替换为这一 Taylor 近似，就得到牛顿步所满足的线性方程组

$$
Hv+A^T\nu=-g,\qquad Av=0,
\tag{11.17}
$$

其中

$$
\begin{aligned}
H&=\nabla^2f_0(x)+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla^2f_i(x)
+\sum_{i=1}^m\frac{1}{tf_i(x)^2}\nabla f_i(x)\nabla f_i(x)^T\\
g&=\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla f_i(x).
\end{aligned}
$$

现在注意到

$$
H=\nabla^2f_0(x)+(1/t)\nabla^2\phi(x),\qquad g=\nabla f_0(x)+(1/t)\nabla\phi(x),
$$

所以由 (11.14)，障碍法中心化步骤中的牛顿步 $\Delta x_{\mathrm{nt}}$ 和 $\nu_{\mathrm{nt}}$ 满足

$$
tH\Delta x_{\mathrm{nt}}+A^T\nu_{\mathrm{nt}}=-tg,\qquad A\Delta x_{\mathrm{nt}}=0.
$$

将其与 (11.17) 比较可得

$$
v=\Delta x_{\mathrm{nt}},\qquad \nu=(1/t)\nu_{\mathrm{nt}}.
$$

这说明，对对偶变量进行缩放之后，中心化问题 (11.6) 的牛顿步可以解释为求解修正 KKT 方程组 (11.16) 的牛顿步。

在这种做法中，我们先从修正 KKT 方程组中消去变量 $\lambda$，然后应用牛顿法求解所得方程组。另一种变体是不先消去 $\lambda$，而是直接对修正 KKT 方程组应用牛顿法。这样得到的就是所谓的原始–对偶搜索方向，将在 §11.7 中讨论。

<!-- pdf-page: 593 -->

## 11.4 可行性与第一阶段方法

障碍法需要一个严格可行的初始点 $x^{(0)}$。当这样的点未知时，要先执行一个称为第一阶段（phase I）的预备阶段，求出严格可行点（或判定约束不可行）。随后，将第一阶段找到的严格可行点作为障碍法的初始点，这时的障碍法称为第二阶段（phase II）。本节介绍几种第一阶段方法。

### 11.4.1 基本第一阶段方法

考虑关于变量 $x\in\mathbf{R}^n$ 的一组不等式和等式，

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad Ax=b,
\tag{11.18}
$$

其中 $f_i:\mathbf{R}^n\to\mathbf{R}$ 是具有连续二阶导数的凸函数。假设已给定一点 $x^{(0)}\in\mathbf{dom}\,f_1\cap\cdots\cap\mathbf{dom}\,f_m$，且 $Ax^{(0)}=b$。

我们的目标是找到这些不等式和等式的一个严格可行解，或判定这样的解不存在。为此，构造以下优化问题：

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m\\
&Ax=b,
\end{aligned}
\tag{11.19}
$$

变量为 $x\in\mathbf{R}^n$、$s\in\mathbf{R}$。变量 $s$ 可以解释为这些不等式的最大不可行度的上界；目标是将最大不可行度降到零以下。

这个问题总是严格可行的，因为可以将 $x^{(0)}$ 选为 $x$ 的初始点，并将任意大于 $\max_{i=1,\ldots,m}f_i(x^{(0)})$ 的数选为 $s$ 的初值。因此，可以应用障碍法求解问题 (11.19)，它称为与不等式和等式系统 (11.19) 对应的第一阶段优化问题。

根据 (11.19) 的最优值 $\bar p^\star$ 的符号，可以分为三种情况。

1. 如果 $\bar p^\star<0$，则 (11.18) 有严格可行解。而且，如果 $(x,s)$ 对 (11.19) 可行且 $s<0$，则 $x$ 满足 $f_i(x)<0$。这意味着不必将优化问题 (11.19) 求解到很高精度；当 $s<0$ 时就可以终止。

2. 如果 $\bar p^\star>0$，则 (11.18) 不可行。与第一种情况一样，不必将第一阶段优化问题 (11.19) 求解到很高精度；找到一个对偶目标值为正的对偶可行点时，就可以终止，因为这证明了 $\bar p^\star>0$。在这种情况下，可以利用这个对偶可行点构造择一系统的解，证明 (11.18) 不可行。

3. 如果 $\bar p^\star=0$，而且最小值在 $x^\star$ 和 $s^\star=0$ 处达到，那么这组不等式可行，但不严格可行。如果 $\bar p^\star=0$，但最小值不达到，则这些不等式不可行。

    <!-- pdf-page: 594 -->

    实际上，不可能精确判定 $\bar p^\star=0$。应用于 (11.19) 的优化算法会改为在得到 $|\bar p^\star|<\epsilon$ 时终止，其中 $\epsilon$ 是一个较小的正数。这允许我们得出结论：不等式 $f_i(x)\leq-\epsilon$ 不可行，而不等式 $f_i(x)\leq\epsilon$ 可行。

#### 不可行度之和

上述基本第一阶段方法有许多变体。其中一种方法最小化不可行度之和，而不是最大不可行度。构造问题

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{1}^Ts\\
\text{约束为}\quad &f_i(x)\leq s_i,\quad i=1,\ldots,m\\
&Ax=b\\
&s\succeq0.
\end{aligned}
\tag{11.20}
$$

对固定的 $x$，$s_i$ 的最优值是 $\max\{f_i(x),0\}$，所以这个问题最小化的是不可行度之和。问题 (11.20) 的最优值为零且能够达到，当且仅当原来这组等式和不等式可行。

当等式和不等式系统 (11.19) 不可行时，这种最小化不可行度之和的第一阶段方法具有一个很有意思的性质。此时，第一阶段问题 (11.20) 的最优点通常只违反少量不等式，设其数目为 $r$。因此，我们求得了一个满足很多个（$m-r$ 个）不等式的点，也就是说，找到了一个较大的可行不等式子集。在这种情况下，与严格满足的不等式对应的对偶变量为零，所以也证明了某个不等式子集不可行。相比于仅仅知道这 $m$ 个不等式合在一起无法同时满足，这个结果提供了更多信息。（这种现象与用于寻找稀疏近似解的 $\ell_1$ 范数正则化或基追踪密切相关；见 §6.1.2 和 §6.5.4。）

<div class="translator-note" markdown="1">

**译注：约束系统的编号。** 本节两处写作“系统 (11.19)”的等式和不等式系统，实际指 (11.18)。(11.19) 是为判断其可行性而构造的第一阶段优化问题。

</div>

<div class="example" id="example-11-4" markdown="1">

**例 11.4 第一阶段方法的比较。** 对一组不可行的不等式 $Ax\preceq b$ 应用两种第一阶段方法，问题维度为 $m=100$、$n=50$。第一种是基本第一阶段方法

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &Ax\preceq b+\mathbf{1}s,
\end{aligned}
$$

它最小化最大不可行度。第二种方法最小化不可行度之和，即求解 LP

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{1}^Ts\\
\text{约束为}\quad &Ax\preceq b+s\\
&s\succeq0.
\end{aligned}
$$

图 11.9 给出了这两个 $x$ 值所对应的不可行度 $b_i-a_i^Tx$ 的分布，两个点分别记为 $x_{\max}$ 和 $x_{\mathrm{sum}}$。$x_{\max}$ 满足 $100$ 个不等式中的 $39$ 个，而 $x_{\mathrm{sum}}$ 满足其中的 $79$ 个。

</div>

<!-- pdf-page: 595 -->

<figure id="fig-11-9" data-figure="11.9" data-reader-return-to-example="example-11-4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-9.png" alt="两个直方图比较不同方法所得向量对应的取值分布；左图横轴为 bᵢ−aᵢᵀx_max，右图为 bᵢ−aᵢᵀx_sum，纵轴均为不等式个数，最高的柱都位于零附近。" data-source-page="595" data-source-rect="90,121,472,274">
<figcaption>图 11.9 对于一组不可行的、含 $50$ 个变量的 $100$ 个不等式 $a_i^Tx\leq b_i$，图中给出了不可行度 $b_i-a_i^Tx$ 的分布。左图所用的向量 $x_{\mathrm{max}}$ 由基本的第一阶段算法得到，它满足 $100$ 个不等式中的 $39$ 个。右图所用的向量 $x_{\mathrm{sum}}$ 由最小化不可行度之和得到，它满足 $100$ 个不等式中的 $79$ 个。</figcaption>
<p class="figure-translation">图内文字：左右两图的 number——个数。</p>
</figure>

<div class="translator-note" markdown="1">

**译注：图中数量的符号。** 例 11.4 和图 11.9 将 $b_i-a_i^Tx$ 称为“不可行度”。对约束 $a_i^Tx\leq b_i$，这个量实际是松弛量：非负时约束满足，负值时约束被违反。前文用于度量违反程度的 $f_i(x)=a_i^Tx-b_i$ 与它符号相反。

</div>

#### 在第二阶段的中心路径附近终止

采用障碍法时，基本第一阶段方法的一个简单变体具有如下性质：当等式和不等式严格可行时，第一阶段问题的中心路径与原优化问题 (11.1) 的中心路径相交。

假设已给定一点 $x^{(0)}\in\mathcal{D}=\mathbf{dom}\,f_0\cap\mathbf{dom}\,f_1\cap\cdots\cap\mathbf{dom}\,f_m$，且 $Ax^{(0)}=b$。构造第一阶段优化问题

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m\\
&f_0(x)\leq M\\
&Ax=b,
\end{aligned}
\tag{11.21}
$$

其中常数 $M$ 选为大于 $\max\{f_0(x^{(0)}),p^\star\}$ 的数。

现在假设原问题 (11.1) 严格可行，因此 (11.21) 的最优值 $\bar p^\star$ 为负。问题 (11.21) 的中心路径由下式刻画：

$$
\sum_{i=1}^m\frac{1}{s-f_i(x)}=\bar t,\qquad
\frac{1}{M-f_0(x)}\nabla f_0(x)+\sum_{i=1}^m\frac{1}{s-f_i(x)}\nabla f_i(x)+A^T\nu=0,
$$

其中 $\bar t$ 是参数。如果 $(x,s)$ 位于中心路径上且 $s=0$，则 $x$ 和 $\nu$ 满足

$$
t\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x)+A^T\nu=0,
$$

这里 $t=1/(M-f_0(x))$。这意味着 $x$ 位于原<!-- pdf-page: 596 -->优化问题 (11.1) 的中心路径上，相应的对偶间隙为

$$
m(M-f_0(x))\leq m(M-p^\star).
\tag{11.22}
$$

### 11.4.2 用不可行初始点牛顿法执行第一阶段

也可以对原问题的一个修改版本应用不可行初始点牛顿法，来完成第一阶段。原问题为

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m\\
&Ax=b.
\end{aligned}
$$

首先，将问题写成如下显然等价的形式：

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m\\
&Ax=b,\quad s=0,
\end{aligned}
$$

其中增加了变量 $s\in\mathbf{R}$。为了启动障碍法，使用不可行初始点牛顿法求解

$$
\begin{aligned}
\text{最小化}\quad &t^{(0)}f_0(x)-\textstyle\sum_{i=1}^m\log(s-f_i(x))\\
\text{约束为}\quad &Ax=b,\quad s=0.
\end{aligned}
$$

初始点可以选为任意 $x\in\mathcal{D}$ 和任意 $s>\max_i f_i(x)$。只要问题严格可行，不可行初始点牛顿法最终就会采用一个无阻尼步，此后便有 $s=0$，即 $x$ 严格可行。

如果连这些函数的公共定义域 $\mathcal{D}$ 中的一个点都不知道，也可以使用同样的技巧。只需对以下问题应用不可行初始点牛顿法：

$$
\begin{aligned}
\text{最小化}\quad &t^{(0)}f_0(x+z_0)-\textstyle\sum_{i=1}^m\log(s-f_i(x+z_i))\\
\text{约束为}\quad &Ax=b,\quad s=0,\quad z_0=0,\quad\ldots,\quad z_m=0,
\end{aligned}
$$

变量为 $x,z_0,\ldots,z_m$ 以及 $s\in\mathbf{R}$。选择 $z_i$ 的初值，使 $x+z_i\in\mathbf{dom}\,f_i$。

用这种方法处理第一阶段问题的主要缺点是：当问题不可行时，没有好的停止准则；残差只是无法收敛到零。

### 11.4.3 示例

考虑一族线性可行性问题，

$$
Ax\preceq b(\gamma),
$$

其中 $A\in\mathbf{R}^{50\times20}$，$b(\gamma)=b+\gamma\Delta b$。问题数据的选取保证：当 $\gamma>0$ 时，这些不等式严格可行；当 $\gamma<0$ 时，不可行。$\gamma=0$ 时，问题可行但不严格可行。

<!-- pdf-page: 597 -->

<p id="ch11-phase-one-wide-reference" markdown="1">图 11.10 给出了 $\gamma$ 在 $[-1,1]$ 中取 $40$ 个不同值时，找到严格可行点或不可行性证书所需的牛顿步总数。我们使用 §11.4.1 的基本第一阶段方法，即对每个 $\gamma$ 值构造 LP</p>

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &Ax\preceq b(\gamma)+s\mathbf{1}.
\end{aligned}
$$

障碍法的参数取 $\mu=10$，初始点为 $x=0$、$s=-\min_i b_i(\gamma)+1$。当找到一个满足 $s<0$ 的点 $(x,s)$，或找到对偶问题

$$
\begin{aligned}
\text{最大化}\quad &-b(\gamma)^Tz\\
\text{约束为}\quad &A^Tz=0\\
&\mathbf{1}^Tz=1\\
&z\succeq0
\end{aligned}
$$

的可行解 $z$，且 $-b(\gamma)^Tz>0$ 时，方法终止。

<p id="ch11-phase-one-near-reference" markdown="1">图中显示，当这些不等式可行且有一定裕量时，约需 $25$ 个牛顿步就能得到一个严格可行点。反过来，当这些不等式不可行、而且同样有一定裕量时，约需 $35$ 步就能得到一个证明不可行性的证书。当这组不等式接近可行与不可行的分界，即 $\gamma$ 接近零时，第一阶段所需的工作量会增加。当 $\gamma$ 非常接近零、不等式非常接近可行与不可行的分界时，所需步数会显著增多。图 11.11 给出了 $\gamma$ 接近零时所需的牛顿步总数。这些曲线表明，对于非常接近可行与不可行分界的问题，确认可行性或证明不可行性所需的步数大致按对数规律增长。</p>

<p id="ch11-phase-one-results-end" markdown="1">这个例子具有典型性：只要问题不是非常接近可行与不可行的分界，用障碍法求解一组凸不等式和线性等式的代价就不高，而且大致不变。当问题非常接近这一分界时，找到严格可行点或给出不可行性证书所需的牛顿步数就会增加。当问题恰好位于严格可行与不可行的分界上，例如可行但不严格可行时，代价就变为无穷。</p>

#### 用不可行初始点牛顿法求可行点

我们还对以下问题应用不可行初始点牛顿法，求解同一组可行性问题：

$$
\begin{aligned}
\text{最小化}\quad &-\textstyle\sum_{i=1}^m\log s_i\\
\text{约束为}\quad &Ax+s=b(\gamma).
\end{aligned}
$$

回溯参数取 $\alpha=0.01$、$\beta=0.9$，初始值为 $x^{(0)}=0$、$s^{(0)}=\mathbf{1}$、$\nu^{(0)}=0$。这里只考虑可行问题（即 $\gamma>0$），一旦找到可行点就终止。（不考虑不可行问题，因为在那种情况下，残差只会收敛到一个正数。）图 11.12 给出了找到可行点所需的牛顿步数随 $\gamma$ 的变化。

<!-- pdf-page: 598 -->

<figure id="fig-11-10" data-figure="11.10" data-reader-after-previous="ch11-phase-one-results-end" data-reader-citation="ch11-phase-one-wide-reference">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-10.png" alt="判定线性不等式可行性所需的牛顿迭代次数随 γ 变化；γ=0 处的竖直虚线分开左侧不可行区与右侧可行区，迭代次数在接近零时明显增多。" data-source-page="598" data-source-rect="212,161,449,343">
<figcaption>图 11.10 判定由 $\gamma\in\mathbf{R}$ 参数化的一组线性不等式 $Ax\preceq b+\gamma\Delta b$ 可行或不可行所需的牛顿迭代次数。当 $\gamma>0$ 时，不等式严格可行；当 $\gamma<0$ 时，不等式不可行。当 $\gamma$ 大于约 $0.2$ 时，计算一个严格可行点约需 $30$ 步；当 $\gamma$ 小于约 $-0.5$ 时，得到一个证明不可行的证书约需 $35$ 步。对于介于两者之间、尤其是接近零的 $\gamma$ 值，需要更多牛顿步才能判定可行性。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；Infeasible——不可行；Feasible——可行。</p>
</figure>

<figure id="fig-11-11" data-figure="11.11" data-reader-after-previous="ch11-phase-one-results-end" data-reader-citation="ch11-phase-one-near-reference">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-11.png" alt="两图以对数刻度展开 γ 接近零时的结果：左图中 γ 从负侧趋近零，证明不可行所需的牛顿迭代次数上升；右图中正 γ 逐渐增大，求得严格可行点所需的次数下降。" data-source-page="598" data-source-rect="143,453,523,599">
<figcaption>图 11.11 <em>左图。</em> 当 $\gamma$ 为绝对值较小的负数时，找到不可行性证明所需的牛顿迭代次数随 $\gamma$ 的变化。<em>右图。</em> 当 $\gamma$ 为较小的正数时，找到严格可行点所需的牛顿迭代次数随 $\gamma$ 的变化。</figcaption>
<p class="figure-translation">图内文字：左右两图的 Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- pdf-page: 599 -->

<figure id="fig-11-12" data-figure="11.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-12.png" alt="不可行初始点牛顿法找到可行点所需的迭代次数随正参数 γ 增大而下降；横轴 γ 和纵轴牛顿迭代次数均采用对数刻度，圆圈表示各次试验的结果。" data-source-page="599" data-source-rect="160,121,397,305">
<figcaption>图 11.12 对于由 $\gamma\in\mathbf{R}$ 参数化的一组线性不等式 $Ax\preceq b+\gamma\Delta b$，找到可行点所需的迭代次数。这里使用不可行初始点牛顿法，并在找到可行点时终止。当 $\gamma=10$ 时，初始点 $x^{(0)}=0$ 恰好可行，因此迭代次数为 $0$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

图中显示，当 $\gamma$ 大于约 $0.3$ 时，少于 $20$ 个牛顿步就能找到一个可行点。在这些情况下，这种方法比第一阶段方法更高效，后者总共需要约 $30$ 个牛顿步。对于更小的 $\gamma$ 值，所需的牛顿步数会急剧增加，大致与 $1/\gamma$ 成正比。$\gamma=0.01$ 时，不可行初始点牛顿法需要几千次迭代才能得到可行点。在这个区域，第一阶段方法要高效得多，只需约 $40$ 次迭代。

这些结果很有代表性。只要不等式可行，而且不是非常接近可行与不可行的分界，不可行初始点牛顿法就表现很好。但当可行集只是勉强非空时（例如本例中 $\gamma$ 很小时），第一阶段方法要好得多。第一阶段方法的另一个优点是能妥善处理不可行的情况；而不可行初始点牛顿法在此时只会无法收敛。

## 11.5 基于自协调性的复杂度分析

利用针对自协调函数的牛顿法复杂度分析（§9.6.4，第 503 页，以及 §10.2.4，第 531 页），可以对障碍法作复杂度分析。这一分析适用于许多常见问题，并得出几个有意思的结论：它给出了用障碍法求解问题所需牛顿步总数的严格上界，也为我们观察到的现象提供了依据，即中心化问题不会随着 $t$ 增大而变得更困难。

<!-- pdf-page: 600 -->

### 11.5.1 自协调性假设

作以下两个假设。

- 对所有 $t\geq t^{(0)}$，函数 $tf_0+\phi$ 都是闭的、自协调的。
- 问题 (11.1) 的下水平集有界。

第二个假设意味着中心化问题的下水平集有界（见习题 11.3），因而中心化问题有解。下水平集有界的假设还意味着，$tf_0+\phi$ 的 Hessian 矩阵处处正定（见习题 11.14）。虽然自协调性假设使复杂度分析仅适用于某一类问题，但必须强调，无论自协调性假设是否成立，障碍法通常都表现良好。

自协调性假设对许多问题成立，包括所有线性和二次问题。如果函数 $f_i$ 是线性函数或二次函数，那么

$$
tf_0-\sum_{i=1}^m\log(-f_i)
$$

对所有 $t\geq0$ 都是自协调的（见 §9.6）。因此，下面给出的复杂度分析适用于 LP、QP 和 QCQP。

在其他情况下，可以重新表述问题，使其满足自协调性假设。例如，考虑带线性不等式约束的熵最大化问题

$$
\begin{aligned}
\text{最小化}\quad &\textstyle\sum_{i=1}^n x_i\log x_i\\
\text{约束为}\quad &Fx\preceq g\\
&Ax=b.
\end{aligned}
$$

函数

$$
tf_0(x)+\phi(x)=t\sum_{i=1}^n x_i\log x_i-\sum_{i=1}^m\log(g_i-f_i^Tx),
$$

其中 $f_1^T,\ldots,f_m^T$ 是 $F$ 的各行，既不是闭函数（除非 $Fx\preceq g$ 蕴含 $x\succeq0$），也不是自协调函数。不过，可以加入冗余不等式约束 $x\succeq0$，得到等价问题

$$
\begin{aligned}
\text{最小化}\quad &\textstyle\sum_{i=1}^n x_i\log x_i\\
\text{约束为}\quad &Fx\preceq g\\
&Ax=b\\
&x\succeq0.
\end{aligned}
\tag{11.23}
$$

对这个问题，有

$$
tf_0(x)+\phi(x)=t\sum_{i=1}^n x_i\log x_i-\sum_{i=1}^n\log x_i-\sum_{i=1}^m\log(g_i-f_i^Tx),
$$

<!-- pdf-page: 601 -->

它对任意 $t\geq0$ 都是自协调的、闭的。（对于所有 $t\geq0$，函数 $ty\log y-\log y$ 在 $\mathbf{R}_{++}$ 上自协调；见习题 11.13。）因此，复杂度分析适用于重新表述后的、带线性不等式约束的熵最大化问题 (11.23)。

再看一个稍微特殊的例子，考虑 GP

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)=\log\left(\textstyle\sum_{k=1}^{K_0}\exp(a_{0k}^Tx+b_{0k})\right)\\
\text{约束为}\quad &\log\left(\textstyle\sum_{k=1}^{K_i}\exp(a_{ik}^Tx+b_{ik})\right)\leq0,\quad i=1,\ldots,m.
\end{aligned}
$$

我们并不清楚函数

$$
tf_0(x)+\phi(x)=t\log\left(\sum_{k=1}^{K_0}\exp(a_{0k}^Tx+b_{0k})\right)
-\sum_{i=1}^m\log\left(-\log\sum_{k=1}^{K_i}\exp(a_{ik}^Tx+b_{ik})\right)
$$

是否自协调。因此，虽然障碍法可以使用，本节的复杂度分析却未必成立。

不过，可以将 GP 重新表述为一个确定满足自协调性假设的形式。对每个（单项式）项 $\exp(a_{ik}^Tx+b_{ik})$，引入一个作为其上界的新变量 $y_{ik}$，

$$
\exp(a_{ik}^Tx+b_{ik})\leq y_{ik}.
$$

利用这些新变量，可以将 GP 写成

$$
\begin{aligned}
\text{最小化}\quad &\textstyle\sum_{k=1}^{K_0}y_{0k}\\
\text{约束为}\quad &\textstyle\sum_{k=1}^{K_i}y_{ik}\leq1,\quad i=1,\ldots,m\\
&a_{ik}^Tx+b_{ik}-\log y_{ik}\leq0,\quad i=0,\ldots,m,\quad k=1,\ldots,K_i\\
&y_{ik}\geq0,\quad i=0,\ldots,m,\quad k=1,\ldots,K_i.
\end{aligned}
$$

相应的对数障碍函数为

$$
\sum_{i=0}^m\sum_{k=1}^{K_i}\left(-\log y_{ik}-\log(\log y_{ik}-a_{ik}^Tx-b_{ik})\right)
-\sum_{i=1}^m\log\left(1-\sum_{k=1}^{K_i}y_{ik}\right),
$$

它是闭的、自协调的（例 9.8，第 500 页）。由于目标函数是线性的，$tf_0+\phi$ 对任意 $t$ 都是闭的、自协调的。

### 11.5.2 每个中心化步骤中的牛顿迭代次数

§9.6.4（第 503 页）和 §10.2.4（第 531 页）建立的自协调函数牛顿法复杂度理论表明，最小化一个闭、严格凸、自协调函数 $f$ 所需的牛顿迭代次数，上界为

$$
\frac{f(x)-p^\star}{\gamma}+c.
\tag{11.24}
$$

<!-- pdf-page: 602 -->

这里，$x$ 是牛顿法的初始点，$p^\star=\inf_x f(x)$ 是最优值。常数 $\gamma$ 只依赖回溯参数 $\alpha$ 和 $\beta$，由下式给出：

$$
\frac{1}{\gamma}=\frac{20-8\alpha}{\alpha\beta(1-2\alpha)^2}.
$$

常数 $c$ 只依赖容差 $\epsilon_{\mathrm{nt}}$，

$$
c=\log_2\log_2(1/\epsilon_{\mathrm{nt}}),
$$

可以合理地近似取为 $c=6$。表达式 (11.24) 对所需牛顿步数给出了一个相当保守的上界，但本节只关心建立复杂度界，重点考察它如何随问题规模和算法参数增长。

本节利用这一结果，推导障碍法一次外层迭代所需牛顿步数的上界，即从 $x^\star(t)$ 出发计算 $x^\star(\mu t)$ 所需的步数。为简化记号，用 $x$ 表示当前迭代点 $x^\star(t)$，用 $x^+$ 表示下一迭代点 $x^\star(\mu t)$。分别用 $\lambda$ 和 $\nu$ 表示 $\lambda^\star(t)$ 和 $\nu^\star(t)$。

自协调性假设意味着

$$
\frac{\mu tf_0(x)+\phi(x)-\mu tf_0(x^+)-\phi(x^+)}{\gamma}+c
\tag{11.25}
$$

是从 $x=x^\star(t)$ 出发计算 $x^+=x^\star(\mu t)$ 所需牛顿步数的上界。遗憾的是，只有实际算出 $x^+$，也就是执行牛顿算法之后，才知道 $x^+$，进而知道上界 (11.25)。（但这时已经知道计算 $x^\star(\mu t)$ 所需的确切牛顿步数，求界也就失去了意义。）不过，可以按如下方式为 (11.25) 再求一个上界：

$$
\begin{aligned}
&\mu tf_0(x)+\phi(x)-\mu tf_0(x^+)-\phi(x^+)\\
&\quad=\mu tf_0(x)-\mu tf_0(x^+)+\sum_{i=1}^m\log(-\mu t\lambda_if_i(x^+))-m\log\mu\\
&\quad\leq\mu tf_0(x)-\mu tf_0(x^+)-\mu t\sum_{i=1}^m\lambda_if_i(x^+)-m-m\log\mu\\
&\quad=\mu tf_0(x)-\mu t\left(f_0(x^+)+\sum_{i=1}^m\lambda_if_i(x^+)+\nu^T(Ax^+-b)\right)-m-m\log\mu\\
&\quad\leq\mu tf_0(x)-\mu tg(\lambda,\nu)-m-m\log\mu\\
&\quad=m(\mu-1-\log\mu).
\end{aligned}
$$

<p id="ch11-complexity-proof-start" markdown="1">这一连串等式和不等式需要一些解释。从第一行得到第二行，利用了 $\lambda_i=-1/(tf_i(x))$。第一个不等式利用了：当 $a>0$ 时，$\log a\leq a-1$。从第三行得到第四行，利用了 $Ax^+=b$，因此增加的项 $\nu^T(Ax^+-b)$ 为零。第二个不等式来自</p>

<!-- pdf-page: 603 -->

<figure id="fig-11-13" data-figure="11.13" data-no-english-text="true" data-reader-after="ch11-complexity-bound-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-13.png" alt="函数 μ−1−log μ 在 μ 从 1 到 3 的区间上的曲线，从零开始上升，且斜率逐渐增大；横轴为 μ，纵轴为函数值。" data-source-page="603" data-source-rect="168,121,385,294">
<figcaption>图 11.13 函数 $\mu-1-\log\mu$ 随 $\mu$ 的变化。障碍法一次外层迭代所需的牛顿步数不超过 $(m/\gamma)(\mu-1-\log\mu)+c$。</figcaption>
</figure>

<p id="ch11-complexity-proof-end" markdown="1" data-reader-continue="ch11-complexity-proof-start">对偶函数的定义：</p>

$$
\begin{aligned}
 g(\lambda,\nu)&=\inf_z\left(f_0(z)+\sum_{i=1}^m\lambda_if_i(z)+\nu^T(Az-b)\right)\\
 &\leq f_0(x^+)+\sum_{i=1}^m\lambda_if_i(x^+)+\nu^T(Ax^+-b).
\end{aligned}
$$

最后一行则来自 $g(\lambda,\nu)=f_0(x)-m/t$。

因此，

$$
\frac{m(\mu-1-\log\mu)}{\gamma}+c
\tag{11.26}
$$

<p id="ch11-complexity-bound-explanation" markdown="1">是 (11.25) 的上界，从而也是障碍法一次外层迭代所需牛顿步数的上界。函数 $\mu-1-\log\mu$ 如图 11.13 所示。当 $\mu$ 较小时，它近似按二次规律增长；当 $\mu$ 较大时，它近似线性增长。这符合直觉：$\mu$ 接近 $1$ 时，中心化所需牛顿步数较少，而 $\mu$ 较大时，步数就可能增加。</p>

上界 (11.26) 表明，每个中心化步骤所需的牛顿步数有一个上界，该上界主要取决于 $\mu$ 和 $m$；前者是障碍法每个外层步骤中更新 $t$ 时所乘的倍数，后者是问题中不等式约束的个数。这个界也较弱地依赖于内层迭代直线搜索使用的参数 $\alpha$ 和 $\beta$，并且非常弱地依赖于终止内层迭代所用的容差。值得注意的是，该界不依赖变量维度 $n$、等式约束个数 $p$，也不依赖问题数据的具体取值，即目标函数和约束函数的具体形式（只要满足 §11.5.1 的自协调性假设）。最后，它也不依赖 $t$；特别地，当 $t\to\infty$ 时，每次外层迭代的牛顿步数仍有统一的上界。

<!-- pdf-page: 604 -->

### 11.5.3 牛顿迭代总次数

现在可以给出障碍法中牛顿步总数的上界，暂不计初始中心化步骤（稍后会将其作为第一阶段的一部分来分析）。将每次外层迭代所需牛顿步数的上界 (11.26)，乘以所需外层步骤数 (11.13)，得到

$$
N=\left\lceil\frac{\log(m/(t^{(0)}\epsilon))}{\log\mu}\right\rceil
\left(\frac{m(\mu-1-\log\mu)}{\gamma}+c\right),
\tag{11.27}
$$

这就是所需牛顿步总数的上界。该公式说明，只要自协调性假设成立，对于任意 $\mu>1$，都能为障碍法所需的牛顿步数给出上界。

如果固定 $\mu$ 和 $m$，则上界 $N$ 与 $\log(m/(t^{(0)}\epsilon))$ 成正比。这个量是初始对偶间隙 $m/t^{(0)}$ 与最终对偶间隙 $\epsilon$ 之比的对数，即所需对偶间隙缩减倍数的对数。因此，可以说障碍法至少线性收敛，因为达到给定精度所需的步数，随精度倒数按对数规律增长。

如果固定 $\mu$ 和所需的对偶间隙缩减倍数，则上界 $N$ 随不等式个数 $m$ 线性增长。上界 $N$ 与问题的其他维度 $n,p$ 无关，也与具体的问题数据或函数无关。下面将看到，对 $\mu$ 作一种依赖于 $m$ 的特定选择，可以得到仅按 $\sqrt m$ 而不是 $m$ 增长的牛顿步数上界。

最后，分析上界 $N$ 如何随算法参数 $\mu$ 变化。当 $\mu$ 趋近于 $1$ 时，$N$ 中的第一个因子会变得很大，因而 $N$ 也会很大。这与我们的直觉和观察一致：$\mu$ 接近 $1$ 时，外层迭代次数非常多。当 $\mu$ 很大时，上界 $N$ 大致按 $\mu/\log\mu$ 增长；这次是因为每次外层迭代所需牛顿迭代次数的上界增加了。这也与我们的观察一致。因此，上界 $N$ 作为 $\mu$ 的函数有一个最小值。

<p id="ch11-total-bound-reference" markdown="1">图 11.14 展示了上界随参数 $\mu$ 的变化，其中画出了以下取值下 (11.27) 随 $\mu$ 的变化：</p>

$$
c=6,\qquad\gamma=1/375,\qquad m/(t^{(0)}\epsilon)=10^5,\qquad m=100.
$$

<p id="ch11-total-bound-explanation" markdown="1">这个上界在定性上与直觉和观察一致：当 $\mu$ 趋近于 $1$ 时，它会变得非常大；当 $\mu$ 很大时，它也会增长，但速度较慢。上界 $N$ 在 $\mu\approx1.02$ 处取得最小值，对应的牛顿迭代总次数上界约为 $8000$。牛顿法的复杂度分析是保守的，但图中反映了选择 $\mu$ 时的基本权衡。（实际计算中，大得多的 $\mu$ 值，例如约 $2$ 到 $100$，都表现很好，所需牛顿迭代总次数只有几十次。）</p>

#### 根据 $m$ 选择 $\mu$

<p id="ch11-varying-mu-start" markdown="1">固定 $\mu$（以及所需的对偶间隙缩减倍数）时，上界 (11.27) 随不等式个数 $m$ 线性增长。事实上，将 $\mu$ 选成 $m$ 的函数，可以得到</p>

<!-- pdf-page: 605 -->

<figure id="fig-11-14" data-figure="11.14" data-no-english-text="true" data-reader-after-previous="ch11-total-bound-explanation" data-reader-citation="ch11-total-bound-reference">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-14.png" alt="牛顿迭代总次数的上界 N 随障碍法参数 μ 变化；μ 略大于 1 时曲线迅速下降到最低点，随后总体上升，右侧可见细小锯齿。" data-source-page="605" data-source-rect="156,125,400,313">
<figcaption>图 11.14 当 $c=6$、$\gamma=1/375$、$m=100$，且对偶间隙的缩减倍数为 $m/(t^{(0)}\epsilon)=10^5$ 时，由式 (11.27) 给出的牛顿迭代总次数上界 $N$ 随障碍算法参数 $\mu$ 的变化。</figcaption>
</figure>

<p id="ch11-varying-mu-end" markdown="1" data-reader-continue="ch11-varying-mu-start">一个关于 $m$ 的更低增长阶。假设选择</p>

$$
\mu=1+1/\sqrt m.
\tag{11.28}
$$

则可以对 (11.27) 的第二个因子作如下估计：

$$
\begin{aligned}
\mu-1-\log\mu&=1/\sqrt m-\log(1+1/\sqrt m)\\
&\leq1/\sqrt m-1/\sqrt m+1/(2m)\\
&=1/(2m)
\end{aligned}
$$

（这里使用了对 $a\geq0$ 成立的 $-\log(1+a)\leq-a+a^2/2$）。利用对数函数的凹性，还有

$$
\log\mu=\log(1+1/\sqrt m)\geq(\log2)/\sqrt m.
$$

由这些不等式，可以得到牛顿步总数的上界

$$
\begin{aligned}
N&\leq\left\lceil\frac{\log(m/(t^{(0)}\epsilon))}{\log\mu}\right\rceil
\left(\frac{m(\mu-1-\log\mu)}{\gamma}+c\right)\\
&\leq\left\lceil\sqrt m\,\frac{\log(m/(t^{(0)}\epsilon))}{\log2}\right\rceil
\left(\frac{1}{2\gamma}+c\right)\\
&=\left\lceil\sqrt m\log_2(m/(t^{(0)}\epsilon))\right\rceil\left(\frac{1}{2\gamma}+c\right)\\
&\leq c_1+c_2\sqrt m,
\end{aligned}
\tag{11.29}
$$

其中

$$
c_1=\frac{1}{2\gamma}+c,\qquad
c_2=\log_2(m/(t^{(0)}\epsilon))\left(\frac{1}{2\gamma}+c\right).
$$

<!-- pdf-page: 606 -->

这里，$c_1$ 依赖于中心化牛顿步的算法参数，而且依赖程度很弱；$c_2$ 则依赖这些参数以及所需的对偶间隙缩减倍数。注意，$\log_2(m/(t^{(0)}\epsilon))$ 恰好是所需对偶间隙缩减量的比特数。

固定对偶间隙缩减倍数时，上界 (11.29) 按 $\sqrt m$ 增长；而当参数 $\mu$ 保持不变时，(11.27) 中的上界 $N$ 则按 $m$ 增长。因此，参数取值为 (11.28) 的障碍法称为 $\sqrt m$ 阶方法。

实际计算中，我们不会采用 $\mu=1+1/\sqrt m$，因为这个值太小；甚至也不会让 $\mu$ 随 $m$ 增大而减小。这里只关注这个 $\mu$ 值，是因为它能（近似）最小化我们对牛顿步数给出的（非常保守的）上界，并得到按 $\sqrt m$ 而不是 $m$ 增长的总体估计。

### 11.5.4 可行性问题

本节分析 §11.4.1 所述基本第一阶段方法的一个小变体的复杂度，用它求解一组凸不等式，

$$
f_1(x)\leq0,\quad\ldots,\quad f_m(x)\leq0,
\tag{11.30}
$$

其中 $f_1,\ldots,f_m$ 是具有连续二阶导数的凸函数。（稍后再考虑等式约束。）假设第一阶段问题

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m
\end{aligned}
\tag{11.31}
$$

满足 §11.5.1 的条件。特别地，假设不等式 (11.30) 的可行集（当然也可能为空）包含于一个半径为 $R$ 的欧几里得球中：

$$
\{x\mid f_i(x)\leq0,\ i=1,\ldots,m\}\subseteq\{x\mid\|x\|_2\leq R\}.
$$

可以将 $R$ 解释为不等式可行集中任意点的范数的一个先验上界。这个假设意味着第一阶段问题的下水平集有界。不失一般性，从点 $x=0$ 开始第一阶段方法。定义 $F=\max_i f_i(0)$，它是最大的约束违反量，并假设其为正（否则 $x=0$ 就满足不等式 (11.30)）。

将第一阶段优化问题 (11.31) 的最优值记为 $\bar p^\star$。$\bar p^\star$ 的符号决定了不等式组 (11.30) 是否可行。$\bar p^\star$ 的大小也有含义。如果 $\bar p^\star$ 为正且很大（例如接近它可能取得的最大值 $F$），就意味着这组不等式明显不可行：对于每个 $x$，至少有一个不等式被大幅违反，违反量至少为 $\bar p^\star$。另一方面，如果 $\bar p^\star$ 为负且绝对值很大，就意味着这组不等式有很大的可行裕量：不仅存在一个使所有 $f_i(x)$ 非正的 $x$，而且存在一个使所有 $f_i(x)$ 都是绝对值很大的负数（不超过 $\bar p^\star$）的 $x$。因此，$|\bar p^\star|$ 衡量了这组不等式的可行性或不可行性有多明确，从而与判定<!-- pdf-page: 607 -->不等式组 (11.30) 可行性的难度有关。特别地，如果 $|\bar p^\star|$ 很小，就意味着问题接近可行与不可行的分界。

为了判定这些不等式是否可行，使用基本第一阶段问题 (11.31) 的一个变体。加入一个冗余线性不等式 $a^Tx\leq1$，得到

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m\\
&a^Tx\leq1.
\end{aligned}
\tag{11.32}
$$

稍后再指定 $a$。所选的 $a$ 将满足 $\|a\|_2\leq1/R$，因此 $\|x\|_2\leq R$ 蕴含 $a^Tx\leq1$，即增加的约束是冗余的。

我们将选择 $a$ 和 $s_0$，使 $x=0$、$s=s_0$ 位于问题 (11.32) 对应于参数值 $t^{(0)}$ 的中心路径上，即它们最小化

$$
t^{(0)}s-\sum_{i=1}^m\log(s-f_i(x))-\log(1-a^Tx).
$$

令关于 $s$ 的导数为零，得到

$$
t^{(0)}=\sum_{i=1}^m\frac{1}{s_0-f_i(0)}.
\tag{11.33}
$$

令关于 $x$ 的梯度为零，得到

$$
a=-\sum_{i=1}^m\frac{1}{s_0-f_i(0)}\nabla f_i(0).
\tag{11.34}
$$

所以只剩下参数 $s_0$ 需要选择；一旦选定 $s_0$，向量 $a$ 就由 (11.34) 给出，而参数 $t^{(0)}$ 由 (11.33) 给出。由于 $x=0$ 和 $s=s_0$ 必须对第一阶段问题 (11.32) 严格可行，所以必须选择 $s_0>F$。

选择 $s_0$ 时还必须保证 $\|a\|_2\leq1/R$。由 (11.34)，有

$$
\|a\|_2\leq\sum_{i=1}^m\frac{1}{s_0-f_i(0)}\|\nabla f_i(0)\|
\leq\frac{mG}{s_0-F},
$$

其中 $G=\max_i\|\nabla f_i(0)\|_2$。因此，可以取 $s_0=mGR+F$，这保证 $\|a\|_2\leq1/R$，从而新增的线性不等式是冗余的。

利用 (11.33)，有

$$
t^{(0)}=\sum_{i=1}^m\frac{1}{mGR+F-f_i(0)}\geq\frac{1}{mGR},
$$

因为 $F=\max_i f_i(0)$。因此，$x=0$、$s=s_0$ 位于第一阶段问题 (11.32) 的中心路径上，初始对偶间隙满足

$$
\frac{m+1}{t^{(0)}}\leq(m+1)mGR.
$$

<!-- pdf-page: 608 -->

为了求解原不等式组 (11.30)，需要确定 $\bar p^\star$ 的符号。当 (11.32) 的原目标值为负，或对偶目标值为正时，就可以停止。当 (11.32) 的对偶间隙小于 $|\bar p^\star|$ 时，这两种情况必有一种发生。

我们用障碍法求解 (11.32)，从一个对偶间隙不超过 $(m+1)mGR$ 的中心点出发，并在对偶间隙小于 $|\bar p^\star|$ 时或更早终止。由上一小节的结果，所需牛顿步数不超过

$$
\left\lceil\sqrt{m+1}\log_2\frac{m(m+1)GR}{|\bar p^\star|}\right\rceil
\left(\frac{1}{2\gamma}+c\right).
\tag{11.35}
$$

（这里取 $\mu=1+1/\sqrt{m+1}$，它给出的复杂度关于 $m$ 的增长阶优于固定 $\mu$ 时的结果。）

上界 (11.35) 的增长仅略快于 $\sqrt m$，而且对中心化步骤的算法参数只有很弱的依赖。它大致与 $\log_2((GR)/|\bar p^\star|)$ 成正比；这个量可以解释为衡量具体可行性问题有多困难，或者它有多接近可行与不可行分界的指标。

#### 带等式约束的可行性问题

通过消去等式约束，可以把同样的分析用于含等式约束的可行性问题。这不会影响问题的自协调性，但此时 $G$ 和 $R$ 指的是约化问题，也就是消元后的问题中的量。

### 11.5.5 第一阶段与第二阶段的合计复杂度

本节给出使用障碍法的一个变体求解以下问题时，全过程的复杂度分析：

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m\\
&Ax=b.
\end{aligned}
$$

首先求解第一阶段问题

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\leq s,\quad i=1,\ldots,m\\
&f_0(x)\leq M\\
&Ax=b\\
&a^Tx\leq1,
\end{aligned}
$$

并假设它满足 §11.5.1 的自协调性和下水平集有界假设。这里在基本第一阶段问题中增加了两个冗余不等式。加入约束 $f_0(x)\leq M$，是为了保证第一阶段的中心路径与第二阶段的中心路径相交，正如 §11.4.1 所述（见 (11.21)）。数值 $M$ 是问题最优值的一个先验上界。第二个新增约束是线性不等式 $a^Tx\leq1$，其中 $a$ 按<!-- pdf-page: 609 -->§11.5.4 所述方式选择。我们使用障碍法求解这个问题，取 $\mu=1+1/\sqrt{m+2}$，初始点 $x=0$、$s=s_0$ 按 §11.5.4 给出。

要找到一个严格可行点，或判定问题不可行，所需牛顿步数不超过

$$
N_{\mathrm{I}}=\left\lceil\sqrt{m+2}\log_2\frac{(m+1)(m+2)GR}{|\bar p^\star|}\right\rceil
\left(\frac{1}{2\gamma}+c\right),
\tag{11.36}
$$

其中 $G$ 和 $R$ 的定义同 §11.5.4。如果问题不可行，计算就结束了；如果问题可行，则在第一阶段中找到一个对应于 $s=0$ 的点，它位于第二阶段问题

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m\\
&Ax=b\\
&a^Tx\leq1
\end{aligned}
$$

的中心路径上。这个初始点对应的初始对偶间隙不超过 $(m+1)(M-p^\star)$（见 (11.22)）。假设第二阶段问题也满足 §11.5.1 的自协调性和下水平集有界假设。

接下来进入第二阶段，仍然使用障碍法。需要把对偶间隙从不超过 $(m+1)(M-p^\star)$ 的初始值，减小到给定容差 $\epsilon>0$。这至多需要

$$
N_{\mathrm{II}}=\left\lceil\sqrt{m+1}\log_2\frac{(m+1)(M-p^\star)}{\epsilon}\right\rceil
\left(\frac{1}{2\gamma}+c\right)
\tag{11.37}
$$

个牛顿步。

因此，牛顿步总数不超过 $N_{\mathrm{I}}+N_{\mathrm{II}}$。这个界随不等式个数 $m$ 大致按 $\sqrt m$ 增长，并包含两个依赖具体问题实例的项：

$$
\log_2\frac{GR}{|\bar p^\star|},\qquad\log_2\frac{M-p^\star}{\epsilon}.
$$

### 11.5.6 小结

本节的复杂度分析主要具有理论意义。特别提醒读者，本节讨论的 $\mu=1+1/\sqrt m$ 在实际计算中会是一个很差的选择；它唯一的优点是能得到按 $\sqrt m$ 而不是 $m$ 增长的上界。同样，我们也不建议在实际计算中加入冗余不等式 $a^Tx\leq1$。

这里分析得到的具体上界远高于实际观察到的迭代次数。甚至连上界的增长阶似乎也是保守的。最好的牛顿步数上界按 $\sqrt m$ 增长，而实际经验表明，牛顿步数几乎完全不随 $m$ 增长（事实上，对其他参数也基本如此）。

尽管如此，知道自协调性条件成立时，可以为障碍法每个<!-- pdf-page: 610 -->中心化步骤所需的牛顿步数给出统一上界，仍然令人安心。障碍法一个显而易见的潜在问题是：随着 $t$ 增大，相应的中心化问题可能变得更困难，需要更多的牛顿步。虽然实际经验表明这种情况不会发生，但这个统一上界进一步保证了它不会发生。

最后，是否将问题表述为满足自协调性条件的形式会在实际计算中带来好处，目前还不清楚。我们只能说，自协调性条件成立时，障碍法在实际计算中会表现良好，而且可以给出最坏情形复杂度界。

## 11.6 含广义不等式的问题

本节说明如何将障碍法扩展到含广义不等式的问题。考虑问题

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m\\
&Ax=b,
\end{aligned}
\tag{11.38}
$$

其中 $f_0:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，$f_i:\mathbf{R}^n\to\mathbf{R}^{k_i}$，$i=1,\ldots,k$，是 $K_i$ 凸函数，$K_i\subseteq\mathbf{R}^{k_i}$ 是正常锥。与 §11.1 一样，假设函数 $f_i$ 都二阶连续可微，$A\in\mathbf{R}^{p\times n}$ 且 $\mathbf{rank}\,A=p$，并且问题有解。

问题 (11.38) 的 KKT 条件为

$$
\begin{aligned}
Ax^\star&=b\\
f_i(x^\star)&\preceq_{K_i}0,\quad i=1,\ldots,m\\
\lambda_i^\star&\succeq_{K_i^*}0,\quad i=1,\ldots,m\\
\nabla f_0(x^\star)+\textstyle\sum_{i=1}^mDf_i(x^\star)^T\lambda_i^\star+A^T\nu^\star&=0\\
\lambda_i^{\star T}f_i(x^\star)&=0,\quad i=1,\ldots,m,
\end{aligned}
\tag{11.39}
$$

其中 $Df_i(x^\star)\in\mathbf{R}^{k_i\times n}$ 是 $f_i$ 在 $x^\star$ 处的导数。我们假设问题 (11.38) 严格可行，因此 KKT 条件是 $x^\star$ 最优的充要条件。

这种方法的推导与标量约束的情形相对应。一旦把对数函数推广到一般正常锥，就能为问题 (11.38) 定义对数障碍函数。此后的推导基本上与标量情形相同。特别地，中心路径、障碍法和复杂度分析都非常相似。

<!-- pdf-page: 611 -->

### 11.6.1 对数障碍函数与中心路径

#### 正常锥的广义对数

首先，对正常锥 $K\subseteq\mathbf{R}^q$ 定义一个类似于对数 $\log x$ 的函数。如果 $\psi:\mathbf{R}^q\to\mathbf{R}$ 满足以下条件，就称它是 $K$ 的广义对数（generalized logarithm）。

- $\psi$ 是凹的、闭的、二阶连续可微的，$\mathbf{dom}\,\psi=\mathbf{int}\,K$，且对 $y\in\mathbf{int}\,K$ 有 $\nabla^2\psi(y)\prec0$。
- 存在常数 $\theta>0$，使对所有 $y\succ_K0$ 和所有 $s>0$，都有

    $$
    \psi(sy)=\psi(y)+\theta\log s.
    $$

    换言之，沿锥 $K$ 中的任意射线，$\psi$ 都具有对数函数的变化规律。

常数 $\theta$ 称为 $\psi$ 的次数（degree，因为 $\exp\psi$ 是一个 $\theta$ 次齐次函数）。注意，广义对数在相差一个加法常数的意义下定义；如果 $\psi$ 是 $K$ 的广义对数，那么 $\psi+a$ 也是，其中 $a\in\mathbf{R}$。当然，普通对数就是 $\mathbf{R}_+$ 的广义对数。

我们将使用任意广义对数都满足的两个性质：如果 $y\succ_K0$，则

$$
\nabla\psi(y)\succ_{K^*}0,
\tag{11.40}
$$

这意味着 $\psi$ 是 $K$ 递增的（见 §3.6.1），并且

$$
y^T\nabla\psi(y)=\theta.
$$

第一个性质在习题 11.15 中证明。第二个性质对 $\psi(sy)=\psi(y)+\theta\log s$ 关于 $s$ 求导即可得到。

<div class="example" id="example-11-5" markdown="1">

**例 11.5 非负正交象限。** 函数 $\psi(x)=\sum_{i=1}^n\log x_i$ 是 $K=\mathbf{R}_+^n$ 的广义对数，次数为 $n$。对 $x\succ0$，

$$
\nabla\psi(x)=(1/x_1,\ldots,1/x_n),
$$

所以 $\nabla\psi(x)\succ0$，而且 $x^T\nabla\psi(x)=n$。

</div>

<div class="example" id="example-11-6" markdown="1">

**例 11.6 二阶锥。** 函数

$$
\psi(x)=\log\left(x_{n+1}^2-\sum_{i=1}^n x_i^2\right)
$$

是二阶锥

$$
K=\left\{x\in\mathbf{R}^{n+1}\;\middle|\;\left(\sum_{i=1}^n x_i^2\right)^{1/2}\leq x_{n+1}\right\}
$$

<!-- pdf-page: 612 -->

的广义对数，次数为 $2$。$\psi$ 在点 $x\in\mathbf{int}\,K$ 处的梯度由下式给出：

$$
\begin{aligned}
\frac{\partial\psi(x)}{\partial x_j}&=\frac{-2x_j}{x_{n+1}^2-\sum_{i=1}^n x_i^2},\quad j=1,\ldots,n\\
\frac{\partial\psi(x)}{\partial x_{n+1}}&=\frac{2x_{n+1}}{x_{n+1}^2-\sum_{i=1}^n x_i^2}.
\end{aligned}
$$

很容易验证 $\nabla\psi(x)\in\mathbf{int}\,K^*=\mathbf{int}\,K$ 和 $x^T\nabla\psi(x)=2$。

</div>

<div class="example" id="example-11-7" markdown="1">

**例 11.7 半正定锥。** 函数 $\psi(X)=\log\det X$ 是锥 $\mathbf{S}_+^p$ 的广义对数。其次数为 $p$，因为当 $s>0$ 时，

$$
\log\det(sX)=\log\det X+p\log s.
$$

$\psi$ 在点 $X\in\mathbf{S}_{++}^p$ 处的梯度等于

$$
\nabla\psi(X)=X^{-1}.
$$

因此，$\nabla\psi(X)=X^{-1}\succ0$，而 $X$ 与 $\nabla\psi(X)$ 的内积等于 $\mathbf{tr}(XX^{-1})=p$。

</div>

#### 广义不等式的对数障碍函数

回到问题 (11.38)。设 $\psi_1,\ldots,\psi_m$ 分别是锥 $K_1,\ldots,K_m$ 的广义对数，次数分别为 $\theta_1,\ldots,\theta_m$。将问题 (11.38) 的对数障碍函数定义为

$$
\phi(x)=-\sum_{i=1}^m\psi_i(-f_i(x)),\qquad
\mathbf{dom}\,\phi=\{x\mid f_i(x)\prec_{K_i}0,\ i=1,\ldots,m\}.
$$

由函数 $\psi_i$ 是 $K_i$ 递增的、函数 $f_i$ 是 $K_i$ 凸的，可知 $\phi$ 是凸函数（见 §3.6.2 的复合规则）。

#### 中心路径

下一步是定义问题 (11.38) 的中心路径。对于 $t\geq0$，将中心点 $x^\star(t)$ 定义为在 $Ax=b$ 约束下 $tf_0+\phi$ 的极小点，即问题

$$
\begin{aligned}
\text{最小化}\quad &tf_0(x)-\textstyle\sum_{i=1}^m\psi_i(-f_i(x))\\
\text{约束为}\quad &Ax=b
\end{aligned}
$$

的解（假设极小点存在且唯一）。中心点由以下最优性条件刻画：

$$
\begin{aligned}
&t\nabla f_0(x)+\nabla\phi(x)+A^T\nu\\
&\quad=t\nabla f_0(x)+\sum_{i=1}^mDf_i(x)^T\nabla\psi_i(-f_i(x))+A^T\nu=0,
\end{aligned}
\tag{11.41}
$$

其中某个 $\nu\in\mathbf{R}^p$ 使该条件成立，$Df_i(x)$ 是 $f_i$ 在 $x$ 处的导数。

<!-- pdf-page: 613 -->

#### 中心路径上的对偶点

与标量情形一样，中心路径上的点可以给出问题 (11.38) 的对偶可行点。对 $i=1,\ldots,m$，定义

$$
\lambda_i^\star(t)=\frac{1}{t}\nabla\psi_i(-f_i(x^\star(t))),
\tag{11.42}
$$

并令 $\nu^\star(t)=\nu/t$，其中 $\nu$ 是 (11.41) 中的最优对偶变量。下面证明，$\lambda_1^\star(t),\ldots,\lambda_m^\star(t)$ 与 $\nu^\star(t)$ 一起，构成原问题 (11.38) 的对偶可行点。

首先，由广义对数的单调性性质 (11.40)，有 $\lambda_i^\star(t)\succ_{K_i^*}0$。其次，由 (11.41) 可知，拉格朗日函数

$$
L(x,\lambda^\star(t),\nu^\star(t))=f_0(x)+\sum_{i=1}^m\lambda_i^\star(t)^Tf_i(x)+\nu^\star(t)^T(Ax-b)
$$

在 $x=x^\star(t)$ 处关于 $x$ 取得最小值。因此，对偶函数 $g$ 在 $(\lambda^\star(t),\nu^\star(t))$ 处的值等于

$$
\begin{aligned}
g(\lambda^\star(t),\nu^\star(t))
&=f_0(x^\star(t))+\sum_{i=1}^m\lambda_i^\star(t)^Tf_i(x^\star(t))+\nu^\star(t)^T(Ax^\star(t)-b)\\
&=f_0(x^\star(t))+(1/t)\sum_{i=1}^m\nabla\psi_i(-f_i(x^\star(t)))^Tf_i(x^\star(t))\\
&=f_0(x^\star(t))-(1/t)\sum_{i=1}^m\theta_i,
\end{aligned}
$$

其中 $\theta_i$ 是 $\psi_i$ 的次数。最后一行利用了当 $y\succ_{K_i}0$ 时 $y^T\nabla\psi_i(y)=\theta_i$，因此

$$
\lambda_i^\star(t)^Tf_i(x^\star(t))=-\theta_i/t,\quad i=1,\ldots,m.
\tag{11.43}
$$

于是，如果定义

$$
\bar\theta=\sum_{i=1}^m\theta_i,
$$

则原可行点 $x^\star(t)$ 与对偶可行点 $(\lambda^\star(t),\nu^\star(t))$ 的对偶间隙为 $\bar\theta/t$。这与标量情形完全类似，只是用各锥广义对数的次数之和 $\bar\theta$，替代了不等式个数 $m$。

<div class="example" id="example-11-8" markdown="1">

**例 11.8 二阶锥规划。** 考虑变量为 $x\in\mathbf{R}^n$ 的 SOCP：

$$
\begin{aligned}
\text{最小化}\quad &f^Tx\\
\text{约束为}\quad &\|A_ix+b_i\|_2\leq c_i^Tx+d_i,\quad i=1,\ldots,m,
\end{aligned}
\tag{11.44}
$$

其中 $A_i\in\mathbf{R}^{n_i\times n}$。例 11.6 已经说明，函数

$$
\psi(y)=\log\left(y_{p+1}^2-\sum_{i=1}^p y_i^2\right)
$$

<!-- pdf-page: 614 -->

是 $\mathbf{R}^{p+1}$ 中二阶锥的广义对数，次数为 $2$。问题 (11.44) 对应的对数障碍函数为

$$
\phi(x)=-\sum_{i=1}^m\log\left((c_i^Tx+d_i)^2-\|A_ix+b_i\|_2^2\right),
\tag{11.45}
$$

其中 $\mathbf{dom}\,\phi=\{x\mid\|A_ix+b_i\|_2<c_i^Tx+d_i,\ i=1,\ldots,m\}$。中心路径上的最优性条件是 $tf+\nabla\phi(x^\star(t))=0$，其中

$$
\nabla\phi(x)=-2\sum_{i=1}^m\frac{1}{(c_i^Tx+d_i)^2-\|A_ix+b_i\|_2^2}
\left((c_i^Tx+d_i)c_i-A_i^T(A_ix+b_i)\right).
$$

由此可知，点

$$
z_i^\star(t)=-\frac{2}{t\alpha_i}(A_ix^\star(t)+b_i),\qquad
w_i^\star(t)=\frac{2}{t\alpha_i}(c_i^Tx^\star(t)+d_i),\quad i=1,\ldots,m,
$$

其中 $\alpha_i=(c_i^Tx^\star(t)+d_i)^2-\|A_ix^\star(t)+b_i\|_2^2$，对以下对偶问题严格可行：

$$
\begin{aligned}
\text{最大化}\quad &-\textstyle\sum_{i=1}^m(b_i^Tz_i+d_iw_i)\\
\text{约束为}\quad &\textstyle\sum_{i=1}^m(A_i^Tz_i+c_iw_i)=f\\
&\|z_i\|_2\leq w_i,\quad i=1,\ldots,m.
\end{aligned}
$$

$x^\star(t)$ 与 $(z^\star(t),w^\star(t))$ 对应的对偶间隙为

$$
\sum_{i=1}^m\left((A_ix^\star(t)+b_i)^Tz_i^\star(t)+(c_i^Tx^\star(t)+d_i)w_i^\star(t)\right)=\frac{2m}{t},
$$

由于 $\theta_i=2$，这与一般公式 $\bar\theta/t$ 一致。

</div>

<div class="example" id="example-11-9" markdown="1">

**例 11.9 不等式形式的半定规划。** 考虑变量为 $x\in\mathbf{R}^n$ 的 SDP，

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &F(x)=x_1F_1+\cdots+x_nF_n+G\preceq0,
\end{aligned}
$$

其中 $G,F_1,\ldots,F_n\in\mathbf{S}^p$。对偶问题为

$$
\begin{aligned}
\text{最大化}\quad &\mathbf{tr}(GZ)\\
\text{约束为}\quad &\mathbf{tr}(F_iZ)+c_i=0,\quad i=1,\ldots,n\\
&Z\succeq0.
\end{aligned}
$$

使用半正定锥 $\mathbf{S}_+^p$ 的广义对数 $\log\det X$，得到原问题的障碍函数

$$
\phi(x)=\log\det(-F(x)^{-1}),
$$

其定义域为 $\mathbf{dom}\,\phi=\{x\mid F(x)\prec0\}$。对于严格可行的 $x$，$\phi$ 的梯度等于

$$
\frac{\partial\phi(x)}{\partial x_i}=\mathbf{tr}(-F(x)^{-1}F_i),\quad i=1,\ldots,n,
$$

由此得到刻画中心点的最优性条件：

$$
tc_i+\mathbf{tr}(-F(x^\star(t))^{-1}F_i)=0,\quad i=1,\ldots,n.
$$

因此，矩阵

$$
Z^\star(t)=\frac{1}{t}(-F(x^\star(t)))^{-1}
$$

是对偶严格可行的，而 $x^\star(t)$ 与 $Z^\star(t)$ 对应的对偶间隙为 $p/t$。

</div>

<!-- pdf-page: 615 -->

### 11.6.2 障碍法

我们已经看到，中心路径的关键性质可以推广到含广义不等式的问题。

- 计算中心路径上的一个点，需要在等式约束下最小化一个二阶可微凸函数，这可以用牛顿法完成。
- 每个中心点 $x^\star(t)$ 都对应一个对偶可行点 $(\lambda^\star(t),\nu^\star(t))$，两者的对偶间隙为 $\bar\theta/t$。特别地，$x^\star(t)$ 的次优程度不超过 $\bar\theta/t$。

这意味着，可以完全按照 §11.3 所述，将障碍法用于问题 (11.38)。从 $x^\star(t^{(0)})$ 出发，计算一个对偶间隙为 $\epsilon$ 的中心点，所需外层迭代次数，也就是中心化步骤数，等于

$$
\left\lceil\frac{\log(\bar\theta/(t^{(0)}\epsilon))}{\log\mu}\right\rceil,
$$

再加上一个初始中心化步骤。与标量情形的对应结果相比，唯一的区别就是 $\bar\theta$ 替代了 $m$。

#### 第一阶段与可行性问题

§11.4 所述的第一阶段方法很容易扩展到含广义不等式的问题。设 $e_i\succ_{K_i}0$，$i=1,\ldots,m$，是给定的 $K_i$ 正向量。为了判定等式与广义不等式

$$
f_1(x)\preceq_{K_1}0,\quad\ldots,\quad f_L(x)\preceq_{K_m}0,\qquad Ax=b
$$

是否可行，求解问题

$$
\begin{aligned}
\text{最小化}\quad &s\\
\text{约束为}\quad &f_i(x)\preceq_{K_i}se_i,\quad i=1,\ldots,m\\
&Ax=b,
\end{aligned}
$$

变量为 $x$ 和 $s\in\mathbf{R}$。与普通不等式的情况完全一样，最优值 $\bar p^\star$ 决定了这些等式和广义不等式是否可行。当 $\bar p^\star$ 为正时，任意目标值为正的对偶可行点都会给出一个择一系统的解，证明这组等式和广义不等式不可行（见第 270 页）。

### 11.6.3 示例

#### 一个小规模 SOCP

求解 SOCP

$$
\begin{aligned}
\text{最小化}\quad &f^Tx\\
\text{约束为}\quad &\|A_ix+b_i\|_2\leq c_i^Tx+d_i,\quad i=1,\ldots,m,
\end{aligned}
$$

<!-- pdf-page: 616 -->

<figure id="fig-11-15" data-figure="11.15" data-reader-after="ch11-small-socp-data-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-15.png" alt="二阶锥规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=50、200、2。" data-source-page="616" data-source-rect="204,122,449,305">
<figcaption>图 11.15 障碍法求解一个二阶锥规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<p id="ch11-small-socp-data-end" markdown="1">其中 $x\in\mathbf{R}^{50}$，$m=50$，$A_i\in\mathbf{R}^{5\times50}$。问题实例随机生成，并保证其原严格可行、对偶严格可行，最优值为 $p^\star=1$。我们从中心路径上的一点 $x^{(0)}$ 出发，对偶间隙为 $100$。</p>

使用障碍法求解该问题，障碍函数取为

$$
\phi(x)=-\sum_{i=1}^m\log\left((c_i^Tx+d_i)^2-\|A_ix+b_i\|_2^2\right).
$$

中心化问题用牛顿法求解，算法参数与 §11.3.2 的示例相同：回溯参数 $\alpha=0.01$、$\beta=0.5$，停止准则为 $\lambda(x)^2/2\leq10^{-5}$。

<p id="ch11-small-socp-results-end" markdown="1">图 11.15 给出了对偶间隙随累计牛顿步数的变化。这张图与线性规划和几何规划对应的图 11.4、图 11.6 非常相似。每个中心化步骤所需的牛顿步数大致不变，因此对偶间隙近似线性收敛。在这个例子中，只要 $\mu$ 至少在 $10$ 左右，它的选择也不会明显影响牛顿步总数。与线性规划和几何规划的例子一样，$\mu$ 的一个合理取值范围是 $10$ 到 $100$，此时牛顿步总数约为 $30$（见图 11.16）。</p>

#### 一个小规模 SDP

下一个例子是 SDP

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &\textstyle\sum_{i=1}^n x_iF_i+G\preceq0,
\end{aligned}
\tag{11.46}
$$

<!-- pdf-page: 617 -->

<figure id="fig-11-16" data-figure="11.16" data-reader-after-previous="ch11-small-socp-results-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-16.png" alt="小规模二阶锥规划所需牛顿迭代总次数随 μ 变化；μ 接近 1 时次数很高，随后迅速下降，在较大 μ 下只作小幅波动，圆圈标出试验值。" data-source-page="617" data-source-rect="159,122,399,304">
<figcaption>图 11.16 一个小规模二阶锥规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

变量为 $x\in\mathbf{R}^{100}$，并且 $F_i\in\mathbf{S}^{100}$、$G\in\mathbf{S}^{100}$。问题实例随机生成，并保证其原严格可行、对偶严格可行，$p^\star=1$。初始点位于中心路径上，对偶间隙为 $100$。

我们应用障碍法，对数障碍函数取为

$$
\phi(x)=-\log\det\left(-\sum_{i=1}^n x_iF_i-G\right).
$$

<p id="ch11-small-sdp-results-end" markdown="1">图 11.17 给出了三个不同 $\mu$ 值下障碍法的进展。注意，它与线性规划、几何规划和二阶锥规划的曲线非常相似，后者分别见图 11.4、图 11.6 和图 11.15。与其他例子一样，只要参数 $\mu$ 不太小，它对效率就只有较小影响。图 11.18 给出了将对偶间隙缩小为原来的 $10^{-5}$ 所需的牛顿步数随 $\mu$ 的变化。</p>

#### 一族 SDP

本节考察障碍法的表现如何随问题维度变化。考虑一族如下形式的 SDP：

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{1}^Tx\\
\text{约束为}\quad &A+\mathbf{diag}(x)\succeq0,
\end{aligned}
\tag{11.47}
$$

变量为 $x\in\mathbf{R}^n$，参数为 $A\in\mathbf{S}^n$。矩阵 $A$ 按如下方式生成：对 $i\geq j$，从相互独立的 $\mathcal{N}(0,1)$ 分布生成元素 $A_{ij}$；对 $i<j$，令 $A_{ij}=A_{ji}$，从而 $A\in\mathbf{S}^n$。然后缩放 $A$，使它的谱范数为 $1$。

<!-- pdf-page: 618 -->

<figure id="fig-11-17" data-figure="11.17" data-reader-after-previous="ch11-small-sdp-results-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-17.png" alt="小规模半定规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=150、50、2。" data-source-page="618" data-source-rect="204,150,453,333">
<figcaption>图 11.17 障碍法求解一个小规模半定规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。三条曲线分别对应参数 $\mu$ 的三个取值：$2$、$50$ 和 $150$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<figure id="fig-11-18" data-figure="11.18" data-reader-after-previous="ch11-small-sdp-results-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-18.png" alt="小规模半定规划所需牛顿迭代总次数随 μ 变化；较小 μ 处的曲线陡降，随后在较低的迭代次数附近波动，圆圈标出试验值。" data-source-page="618" data-source-rect="212,435,453,620">
<figcaption>图 11.18 一个小规模半定规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- pdf-page: 619 -->

<figure id="fig-11-19" data-figure="11.19" data-reader-after="ch11-sdp-family-three-results">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-19.png" alt="三个半定规划的阶梯状对偶间隙曲线，分别标为 n=50、500、1000；横轴为累计牛顿迭代次数，纵轴采用对数刻度，三条曲线的下降走势相似。" data-source-page="619" data-source-rect="153,120,429,306">
<figcaption>图 11.19 障碍法求解三个随机生成、规模不同且具有 (11.47) 形式的半定规划时的迭代过程。图中给出了对偶间隙随累计牛顿步数的变化。每个问题的变量个数为 $n$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

算法参数取 $\mu=20$，中心化步骤的参数与前面的例子相同：回溯参数 $\alpha=0.01$、$\beta=0.5$，停止准则为 $\lambda(x)^2/2\leq10^{-5}$。初始点位于 $t^{(0)}=1$ 对应的中心路径点上（即间隙为 $n$）。当初始对偶间隙缩小为原来的 $1/8000$，也就是完成三次外层迭代之后，算法终止。

<p id="ch11-sdp-family-three-results" markdown="1">图 11.19 给出了维度分别为 $n=50$、$n=500$ 和 $n=1000$ 的三个问题实例中，对偶间隙随迭代次数的变化。这些曲线与其他例子非常相似，也与 LP 的曲线非常相似。</p>

<p id="ch11-sdp-family-results-end" markdown="1">为了考察问题规模对所需牛顿步数的影响，我们从 $n=10$ 到 $n=1000$ 取 $20$ 个不同的 $n$ 值，对每个值生成 $100$ 个问题实例。用障碍法求解全部 $2000$ 个问题，并记录所需的牛顿步数。图 11.20 汇总了结果，给出了每个 $n$ 值对应的牛顿步数均值和标准差。这张图与图 11.8 中 LP 对应的结果非常相似。特别地，当问题维度增大到原来的 $100$ 倍时，所需的牛顿步数增长得非常缓慢，仅从约 $20$ 次增至 $26$ 次。</p>

### 11.6.4 基于自协调性的复杂度分析

本节将 §11.5 中针对普通不等式问题的障碍法复杂度分析，推广到含广义不等式的问题。我们已经看到，所需外层迭代次数为

$$
\left\lceil\frac{\log(\bar\theta/t^{(0)}\epsilon)}{\log\mu}\right\rceil,
$$

<!-- pdf-page: 620 -->

<figure id="fig-11-20" data-figure="11.20" data-reader-after-previous="ch11-sdp-family-results-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-20.png" alt="横轴为问题规模 n，采用从 10 到 1000 的对数刻度；平均牛顿迭代次数从约 20 次缓慢升至约 26 次，每个圆圈处的竖直误差条表示标准差。" data-source-page="620" data-source-rect="223,121,444,295">
<figcaption>图 11.20 对问题规模 $n$ 的 $20$ 个取值中的每一个，求解 $100$ 个随机生成的半定规划 (11.47) 所需的平均牛顿步数。对于 $n$ 的每个取值，误差条表示平均值上下的标准差。尽管最大与最小问题规模之比为 $100:1$，所需平均牛顿步数的增长仍很小。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

再加上一个初始中心化步骤。剩下的任务是为每个中心化步骤所需的牛顿步数求上界，这将利用针对自协调函数的牛顿法复杂度理论来完成。为简单起见，不计初始中心化的代价。

作与 §11.5 相同的假设：对所有 $t\geq t^{(0)}$，函数 $tf_0+\phi$ 都是闭的、自协调的，而且 (11.38) 的下水平集有界。

<div class="example" id="example-11-10" markdown="1">

**例 11.10 二阶锥规划。** 函数

$$
-\psi(x)=-\log\left(x_{p+1}^2-\sum_{i=1}^p x_i^2\right)
$$

是自协调的（见例 9.8），所以 SOCP (11.44) 的对数障碍函数 (11.45) 满足闭性和自协调性假设。

</div>

<div class="example" id="example-11-11" markdown="1">

**例 11.11 半定规划。** 对一般半定规划，使用 $\log\det X$ 作为半正定锥的广义对数时，自协调性假设成立。例如，对于变量为 $X\in\mathbf{S}^n$ 的标准形式 SDP

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(CX)\\
\text{约束为}\quad &\mathbf{tr}(A_iX)=b_i,\quad i=1,\ldots,p\\
&X\succeq0,
\end{aligned}
$$

函数 $t^{(0)}\mathbf{tr}(CX)-\log\det X$ 对任意 $t^{(0)}\geq0$ 都是自协调的，而且是闭的。

</div>

<!-- pdf-page: 621 -->

我们将看到，与标量情形完全一样，有

$$
\mu tf_0(x^\star(t))+\phi(x^\star(t))-\mu tf_0(x^\star(\mu t))-\phi(x^\star(\mu t))
\leq\bar\theta(\mu-1-\log\mu).
\tag{11.48}
$$

因此，当自协调性和下水平集有界条件成立时，每个中心化步骤中的牛顿步数不超过

$$
\frac{\bar\theta(\mu-1-\log\mu)}{\gamma}+c,
$$

这与普通不等式问题的障碍法完全相同。一旦建立了基本上界 (11.48)，广义不等式问题的复杂度分析就与普通不等式问题的分析一致，唯一区别是：$\bar\theta$ 是各锥对应的次数之和，而不是不等式个数。

#### 对偶锥的广义对数

我们将利用共轭来证明上界 (11.48)。设 $\psi$ 是正常锥 $K$ 的一个广义对数，次数为 $\theta$。凸函数 $-\psi$ 的共轭为

$$
(-\psi)^*(v)=\sup_u\left(v^Tu+\psi(u)\right).
$$

这个函数是凸的，其定义域为 $-K^*=\{v\mid v\prec_{K^*}0\}$。将 $\bar\psi$ 定义为

$$
\bar\psi(v)=-(-\psi)^*(-v)=\inf_u\left(v^Tu-\psi(u)\right),\qquad
\mathbf{dom}\,\bar\psi=\mathbf{int}\,K^*.
\tag{11.49}
$$

函数 $\bar\psi$ 是凹的，实际上它是对偶锥 $K^*$ 的广义对数，且具有相同的参数 $\theta$（见习题 11.17）。我们称 $\bar\psi$ 为与广义对数 $\psi$ 对应的对偶对数（dual logarithm）。

由 (11.49) 得到不等式

$$
\bar\psi(v)+\psi(u)\leq u^Tv,
\tag{11.50}
$$

它对任意 $u\succ_K0$、$v\succ_{K^*}0$ 成立，取等号当且仅当 $\nabla\psi(u)=v$，或等价地，$\nabla\bar\psi(v)=u$。（这个不等式是 Young 不等式针对凹函数的一个变体。）

<div class="example" id="example-11-12" markdown="1">

**例 11.12 二阶锥。** 二阶锥的广义对数为 $\psi(x)=\log(x_{p+1}^2-\sum_{i=1}^p x_i^2)$，其定义域是 $\mathbf{dom}\,\psi=\{x\in\mathbf{R}^{p+1}\mid x_{p+1}>(\sum_{i=1}^p x_i^2)^{1/2}\}$。对应的对偶对数为

$$
\bar\psi(y)=\log\left(y_{p+1}^2-\sum_{i=1}^p y_i^2\right)+2-\log4,
$$

其定义域为 $\mathbf{dom}\,\bar\psi=\{y\in\mathbf{R}^{p+1}\mid y_{p+1}>(\sum_{i=1}^p y_i^2)^{1/2}\}$（见习题 3.36）。除了相差一个常数，它与二阶锥原来的广义对数相同。

</div>

<!-- pdf-page: 622 -->

<div class="example" id="example-11-13" markdown="1">

**例 11.13 半正定锥。** 对于 $\psi(X)=\log\det X$，$\mathbf{dom}\,\psi=\mathbf{S}_{++}^p$，相应的对偶对数为

$$
\bar\psi(Y)=\log\det Y+p,
$$

定义域为 $\mathbf{dom}\,\psi^*=\mathbf{S}_{++}^p$（见例 3.23）。同样，除了相差一个常数，它是同一个广义对数。

</div>

<div class="translator-note" markdown="1">

**译注：对偶对数的定义域。** 上文用严格不等式描述的共轭函数 $(-\psi)^*$ 的定义域是 $-\mathbf{int}\,K^*$，而非包含边界的 $-K^*$。例 11.13 中的 $\mathbf{S}_{++}^p$ 则是对偶对数 $\bar\psi$ 的定义域，此处域记号应为 $\mathbf{dom}\,\bar\psi$。

</div>

#### 基本上界的推导

为简化记号，将 $x^\star(t)$ 记为 $x$，$x^\star(\mu t)$ 记为 $x^+$，$\lambda_i^\star(t)$ 记为 $\lambda_i$，$\nu^\star(t)$ 记为 $\nu$。由 (11.42) 中的 $t\lambda_i=\nabla\psi_i(-f_i(x))$ 以及性质 (11.43)，可得

$$
\psi_i(-f_i(x))+\bar\psi_i(t\lambda_i)=-t\lambda_i^Tf_i(x)=\theta_i,
\tag{11.51}
$$

即对于 $u=-f_i(x)$、$v=t\lambda_i$，不等式 (11.50) 取等号。对 $u=-f_i(x^+)$、$v=\mu t\lambda_i$ 使用同一个不等式，得到

$$
\psi_i(-f_i(x^+))+\bar\psi_i(\mu t\lambda_i)\leq-\mu t\lambda_i^Tf_i(x^+).
$$

利用 $\bar\psi_i$ 的对数齐次性，可将其写成

$$
\psi_i(-f_i(x^+))+\bar\psi_i(t\lambda_i)+\theta_i\log\mu\leq-\mu t\lambda_i^Tf_i(x^+).
$$

从这个不等式中减去等式 (11.51)，得到

$$
-\psi_i(-f_i(x))+\psi_i(-f_i(x^+))+\theta_i\log\mu\leq-\theta_i-\mu t\lambda_i^Tf_i(x^+).
$$

对 $i$ 求和得

$$
\phi(x)-\phi(x^+)+\bar\theta\log\mu
\leq-\bar\theta-\mu t\sum_{i=1}^m\lambda_i^Tf_i(x^+).
\tag{11.52}
$$

由对偶函数的定义，还有

$$
\begin{aligned}
f_0(x)-\bar\theta/t&=g(\lambda,\nu)\\
&\leq f_0(x^+)+\sum_{i=1}^m\lambda_i^Tf_i(x^+)+\nu^T(Ax^+-b)\\
&=f_0(x^+)+\sum_{i=1}^m\lambda_i^Tf_i(x^+).
\end{aligned}
$$

将这个不等式乘以 $\mu t$，再与不等式 (11.52) 相加，得到

$$
\phi(x)-\phi(x^+)+\bar\theta\log\mu+\mu tf_0(x)-\mu\bar\theta
\leq\mu tf_0(x^+)-\bar\theta.
$$

整理后得到

$$
\mu tf_0(x)+\phi(x)-\mu tf_0(x^+)-\phi(x^+)
\leq\bar\theta(\mu-1-\log\mu),
$$

这正是所需的不等式 (11.48)。

<!-- pdf-page: 623 -->

## 11.7 原始–对偶内点法

本节介绍一种基本的原始–对偶内点法。原始–对偶内点法与障碍法非常相似，但有一些区别。

- 只有一层循环或迭代，即不再像障碍法那样区分内层和外层迭代。每次迭代都同时更新原变量和对偶变量。
- 原始–对偶内点法的搜索方向，是对修正 KKT 方程组（即对数障碍函数中心化问题的最优性条件）应用牛顿法得到的。原始–对偶搜索方向与障碍法产生的搜索方向相似，但并不完全相同。
- 在原始–对偶内点法中，原迭代点和对偶迭代点不一定可行。

原始–对偶内点法通常比障碍法更高效，尤其是在要求高精度时，因为它可以具有快于线性的收敛速度。对于线性规划、二次规划、二阶锥规划、几何规划和半定规划等几类基本问题，专门设计的原始–对偶方法优于障碍法。对于一般非线性凸优化问题，原始–对偶内点法仍是一个活跃的研究课题，而且很有前景。相比障碍法，原始–对偶算法的另一个优点是：问题可行但不严格可行时，它仍可能奏效，不过这里不作进一步讨论。

本节给出求解 (11.1) 的一种基本原始–对偶方法，不作收敛性分析。关于原始–对偶方法及其收敛性分析的更全面讨论，请参阅参考文献。

### 11.7.1 原始–对偶搜索方向

与障碍法一样，从修正 KKT 条件 (11.15) 出发，将它们写成 $r_t(x,\lambda,\nu)=0$，其中定义

$$
r_t(x,\lambda,\nu)=
\begin{bmatrix}
\nabla f_0(x)+Df(x)^T\lambda+A^T\nu\\
-\mathbf{diag}(\lambda)f(x)-(1/t)\mathbf{1}\\
Ax-b
\end{bmatrix},
\tag{11.53}
$$

且 $t>0$。这里，$f:\mathbf{R}^n\to\mathbf{R}^m$ 及其导数矩阵 $Df$ 为

$$
f(x)=\begin{bmatrix}f_1(x)\\\vdots\\f_m(x)\end{bmatrix},\qquad
Df(x)=\begin{bmatrix}\nabla f_1(x)^T\\\vdots\\\nabla f_m(x)^T\end{bmatrix}.
$$

如果 $x,\lambda,\nu$ 满足 $r_t(x,\lambda,\nu)=0$，且 $f_i(x)<0$，则 $x=x^\star(t)$、$\lambda=\lambda^\star(t)$、$\nu=\nu^\star(t)$。特别地，$x$ 原可行，$\lambda,\nu$ 对偶可行，两者的<!-- pdf-page: 624 -->对偶间隙为 $m/t$。$r_t$ 的第一个分块分量

$$
r_{\mathrm{dual}}=\nabla f_0(x)+Df(x)^T\lambda+A^T\nu
$$

称为对偶残差，最后一个分块分量 $r_{\mathrm{pri}}=Ax-b$ 称为原残差。中间的分块

$$
r_{\mathrm{cent}}=-\mathbf{diag}(\lambda)f(x)-(1/t)\mathbf{1}
$$

是中心性残差，即修正互补条件的残差。

现在固定 $t$，考虑在满足 $f(x)\prec0$、$\lambda\succ0$ 的点 $(x,\lambda,\nu)$ 处，求解非线性方程组 $r_t(x,\lambda,\nu)=0$ 的牛顿步，这次不先像 §11.3.4 那样消去 $\lambda$。分别将当前点和牛顿步记为

$$
y=(x,\lambda,\nu),\qquad\Delta y=(\Delta x,\Delta\lambda,\Delta\nu).
$$

牛顿步由线性方程组

$$
r_t(y+\Delta y)\approx r_t(y)+Dr_t(y)\Delta y=0
$$

刻画，即 $\Delta y=-Dr_t(y)^{-1}r_t(y)$。用 $x,\lambda,\nu$ 表示，就有

$$
\begin{bmatrix}
\nabla^2f_0(x)+\sum_{i=1}^m\lambda_i\nabla^2f_i(x)&Df(x)^T&A^T\\
-\mathbf{diag}(\lambda)Df(x)&-\mathbf{diag}(f(x))&0\\
A&0&0
\end{bmatrix}
\begin{bmatrix}\Delta x\\\Delta\lambda\\\Delta\nu\end{bmatrix}
=-\begin{bmatrix}r_{\mathrm{dual}}\\r_{\mathrm{cent}}\\r_{\mathrm{pri}}\end{bmatrix}.
\tag{11.54}
$$

原始–对偶搜索方向 $\Delta y_{\mathrm{pd}}=(\Delta x_{\mathrm{pd}},\Delta\lambda_{\mathrm{pd}},\Delta\nu_{\mathrm{pd}})$ 定义为 (11.54) 的解。

原搜索方向和对偶搜索方向同时通过系数矩阵和残差相互耦合。例如，原搜索方向 $\Delta x_{\mathrm{pd}}$ 既依赖 $x$，也依赖对偶变量 $\lambda,\nu$ 的当前值。还可以注意到，如果 $x$ 满足 $Ax=b$，即原可行性残差 $r_{\mathrm{pri}}$ 为零，那么 $A\Delta x_{\mathrm{pd}}=0$，所以 $\Delta x_{\mathrm{pd}}$ 给出一个原可行方向：对任意 $s$，$x+s\Delta x_{\mathrm{pd}}$ 都满足 $A(x+s\Delta x_{\mathrm{pd}})=b$。

#### 与障碍法搜索方向的比较

原始–对偶搜索方向与障碍法使用的搜索方向密切相关，但并不完全相同。从定义原始–对偶搜索方向的线性方程组 (11.54) 出发，利用第二组分块方程给出的

$$
\Delta\lambda_{\mathrm{pd}}=-\mathbf{diag}(f(x))^{-1}\mathbf{diag}(\lambda)Df(x)\Delta x_{\mathrm{pd}}
+\mathbf{diag}(f(x))^{-1}r_{\mathrm{cent}}
$$

消去变量 $\Delta\lambda_{\mathrm{pd}}$。代入第一组分块方程，得到

$$
\begin{aligned}
&\begin{bmatrix}H_{\mathrm{pd}}&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{pd}}\\\Delta\nu_{\mathrm{pd}}\end{bmatrix}\\
&\quad=-\begin{bmatrix}
r_{\mathrm{dual}}+Df(x)^T\mathbf{diag}(f(x))^{-1}r_{\mathrm{cent}}\\r_{\mathrm{pri}}
\end{bmatrix}\\
&\quad=-\begin{bmatrix}
\nabla f_0(x)+(1/t)\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x)+A^T\nu\\r_{\mathrm{pri}}
\end{bmatrix},
\end{aligned}
\tag{11.55}
$$

<!-- pdf-page: 625 -->

其中

$$
H_{\mathrm{pd}}=\nabla^2f_0(x)+\sum_{i=1}^m\lambda_i\nabla^2f_i(x)
+\sum_{i=1}^m\frac{\lambda_i}{-f_i(x)}\nabla f_i(x)\nabla f_i(x)^T.
\tag{11.56}
$$

可以将 (11.55) 与方程 (11.14) 比较，后者定义了障碍法中参数为 $t$ 的中心化问题的牛顿步。该方程可以写为

$$
\begin{aligned}
&\begin{bmatrix}H_{\mathrm{bar}}&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{bar}}\\\nu_{\mathrm{bar}}\end{bmatrix}\\
&\quad=-\begin{bmatrix}t\nabla f_0(x)+\nabla\phi(x)\\r_{\mathrm{pri}}\end{bmatrix}\\
&\quad=-\begin{bmatrix}t\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x)\\r_{\mathrm{pri}}\end{bmatrix},
\end{aligned}
\tag{11.57}
$$

其中

$$
H_{\mathrm{bar}}=t\nabla^2f_0(x)+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla^2f_i(x)
+\sum_{i=1}^m\frac{1}{f_i(x)^2}\nabla f_i(x)\nabla f_i(x)^T.
\tag{11.58}
$$

（这里给出的是不可行牛顿步的一般表达式；如果当前的 $x$ 可行，即 $r_{\mathrm{pri}}=0$，则 $\Delta x_{\mathrm{bar}}$ 与 (11.14) 中定义的可行牛顿步 $\Delta x_{\mathrm{nt}}$ 相同。）

首先可以看到，方程组 (11.55) 和 (11.57) 非常相似。两者的系数矩阵具有相同的结构；事实上，矩阵 $H_{\mathrm{pd}}$ 和 $H_{\mathrm{bar}}$ 都是下列矩阵的正系数线性组合：

$$
\nabla^2f_0(x),\quad\nabla^2f_1(x),\ldots,\nabla^2f_m(x),\quad
\nabla f_1(x)\nabla f_1(x)^T,\ldots,\nabla f_m(x)\nabla f_m(x)^T.
$$

这意味着，可以使用同一种方法计算原始–对偶搜索方向和障碍法的牛顿步。

关于原始–对偶方程组 (11.55) 与障碍法方程组 (11.57) 的关系，还可以进一步说明。将 (11.57) 的第一组分块方程除以 $t$，并定义变量 $\Delta\nu_{\mathrm{bar}}=(1/t)\nu_{\mathrm{bar}}-\nu$，其中 $\nu$ 是任意的。于是得到

$$
\begin{bmatrix}(1/t)H_{\mathrm{bar}}&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{bar}}\\\Delta\nu_{\mathrm{bar}}\end{bmatrix}
=-\begin{bmatrix}
\nabla f_0(x)+(1/t)\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x)+A^T\nu\\r_{\mathrm{pri}}
\end{bmatrix}.
$$

在这种形式下，右端项与在相同 $x,\lambda,\nu$ 处计算的原始–对偶方程组右端项完全一致。系数矩阵只有第 $(1,1)$ 个分块不同：

$$
\begin{aligned}
H_{\mathrm{pd}}&=\nabla^2f_0(x)+\sum_{i=1}^m\lambda_i\nabla^2f_i(x)
+\sum_{i=1}^m\frac{\lambda_i}{-f_i(x)}\nabla f_i(x)\nabla f_i(x)^T,\\
(1/t)H_{\mathrm{bar}}&=\nabla^2f_0(x)+\sum_{i=1}^m\frac{1}{-tf_i(x)}\nabla^2f_i(x)
+\sum_{i=1}^m\frac{1}{tf_i(x)^2}\nabla f_i(x)\nabla f_i(x)^T.
\end{aligned}
$$

当 $x$ 和 $\lambda$ 满足 $-f_i(x)\lambda_i=1/t$ 时，两个系数矩阵一致，因而搜索方向也一致。

<!-- pdf-page: 626 -->

### 11.7.2 替代对偶间隙

在原始–对偶内点法中，迭代点 $x^{(k)},\lambda^{(k)},\nu^{(k)}$ 不一定可行，除非考虑算法收敛后的极限。这意味着，不能像障碍法的外层步骤那样，容易地计算算法第 $k$ 步对应的对偶间隙 $\eta^{(k)}$。因此，对于任意满足 $f(x)\prec0$ 的 $x$ 和 $\lambda\succeq0$，定义替代对偶间隙（surrogate duality gap）为

$$
\hat\eta(x,\lambda)=-f(x)^T\lambda.
\tag{11.59}
$$

如果 $x$ 原可行，$\lambda,\nu$ 对偶可行，即 $r_{\mathrm{pri}}=0$ 且 $r_{\mathrm{dual}}=0$，那么替代间隙 $\hat\eta$ 就是对偶间隙。注意，与替代对偶间隙 $\hat\eta$ 对应的参数 $t$ 值为 $m/\hat\eta$。

### 11.7.3 原始–对偶内点法

现在可以给出基本的原始–对偶内点算法。

<div class="algorithm" id="algorithm-11-2" data-algorithm="11.2" markdown="1">

**算法 11.2 原始–对偶内点法。**

**给定** 满足 $f_1(x)<0,\ldots,f_m(x)<0$ 的 $x$，以及 $\lambda\succ0$、$\mu>1$、$\epsilon_{\mathrm{feas}}>0$、$\epsilon>0$。

**重复**

1. **确定 $t$。** 令 $t:=\mu m/\hat\eta$。
2. **计算原始–对偶搜索方向 $\Delta y_{\mathrm{pd}}$。**
3. **直线搜索并更新。** 确定步长 $s>0$，并令 $y:=y+s\Delta y_{\mathrm{pd}}$。

**直到** $\|r_{\mathrm{pri}}\|_2\leq\epsilon_{\mathrm{feas}}$、$\|r_{\mathrm{dual}}\|_2\leq\epsilon_{\mathrm{feas}}$ 且 $\hat\eta\leq\epsilon$。

</div>

在步骤 1 中，参数 $t$ 被设为 $m/\hat\eta$ 的 $\mu$ 倍，而 $m/\hat\eta$ 是与当前替代对偶间隙 $\hat\eta$ 对应的 $t$ 值。如果 $x,\lambda,\nu$ 位于参数为 $t$ 的中心路径上，因而对偶间隙为 $m/t$，那么步骤 1 就会把 $t$ 增大为原来的 $\mu$ 倍，这恰好是障碍法使用的更新方式。参数 $\mu$ 取 $10$ 左右似乎表现良好。

当 $x$ 原可行、$\lambda,\nu$ 对偶可行（在容差 $\epsilon_{\mathrm{feas}}$ 范围内），且替代间隙小于容差 $\epsilon$ 时，原始–对偶内点算法终止。由于原始–对偶内点法通常具有快于线性的收敛速度，常将 $\epsilon_{\mathrm{feas}}$ 和 $\epsilon$ 选得较小。

#### 直线搜索

原始–对偶内点法中的直线搜索，是基于残差范数的标准回溯直线搜索，并经过修改以保证 $\lambda\succ0$ 和 $f(x)\prec0$。将当前迭代点记为 $x,\lambda,\nu$，下一迭代点记为 $x^+,\lambda^+,\nu^+$，即

$$
x^+=x+s\Delta x_{\mathrm{pd}},\qquad
\lambda^+=\lambda+s\Delta\lambda_{\mathrm{pd}},\qquad
\nu^+=\nu+s\Delta\nu_{\mathrm{pd}}.
$$

<!-- pdf-page: 627 -->

将 $y^+$ 处的残差记为 $r^+$。

首先计算不超过 $1$、且使 $\lambda^+\succeq0$ 的最大正步长，即

$$
\begin{aligned}
s^{\max}&=\sup\{s\in[0,1]\mid\lambda+s\Delta\lambda\succeq0\}\\
&=\min\{1,\ \min\{-\lambda_i/\Delta\lambda_i\mid\Delta\lambda_i<0\}\}.
\end{aligned}
$$

从 $s=0.99s^{\max}$ 开始回溯，不断将 $s$ 乘以 $\beta\in(0,1)$，直到 $f(x^+)\prec0$。再继续将 $s$ 乘以 $\beta$，直到

$$
\|r_t(x^+,\lambda^+,\nu^+)\|_2\leq(1-\alpha s)\|r_t(x,\lambda,\nu)\|_2.
$$

回溯参数 $\alpha,\beta$ 的常见选择与牛顿法相同：$\alpha$ 通常取在 $0.01$ 到 $0.1$ 之间，$\beta$ 通常取在 $0.3$ 到 $0.8$ 之间。

原始–对偶内点算法的一次迭代，相当于对方程组 $r_t(x,\lambda,\nu)=0$ 执行一步不可行牛顿法，但作了修改以保证 $\lambda\succ0$ 和 $f(x)\prec0$；等价地，也可以说把 $\mathbf{dom}\,r_t$ 限制在 $\lambda\succ0$ 和 $f(x)\prec0$ 的范围内。利用不可行初始点牛顿法收敛性证明中的相同论证，可以说明原始–对偶方法的直线搜索总会在有限步内终止。

### 11.7.4 示例

使用与 §11.3.2 相同的问题来展示原始–对偶内点法的表现。唯一的区别是：不再像 §11.3.2 那样从中心路径上的点出发，而是从随机生成的、满足 $f(x)\prec0$ 的 $x^{(0)}$ 出发，并取 $\lambda_i^{(0)}=-1/f_i(x^{(0)})$，因此初始替代间隙为 $\hat\eta=100$。原始–对偶内点法的参数取为

$$
\mu=10,\qquad\beta=0.5,\qquad\epsilon=10^{-8},\qquad\alpha=0.01.
$$

#### 小规模 LP 和 GP

首先考虑 §11.3.2 中使用的小规模 LP，它有 $m=100$ 个不等式和 $n=50$ 个变量。图 11.21 给出了原始–对偶内点法的进展。图中有两条曲线，分别表示替代间隙 $\hat\eta$，以及原残差和对偶残差的范数

$$
r_{\mathrm{feas}}=\left(\|r_{\mathrm{pri}}\|_2^2+\|r_{\mathrm{dual}}\|_2^2\right)^{1/2}
$$

随迭代次数的变化。（初始点原可行，因此图中给出的是对偶可行性残差的范数。）曲线表明，残差迅速收敛到零，并在 $24$ 次迭代后，在数值精度范围内变为零。替代间隙也快速收敛。与障碍法相比，原始–对偶内点法更快，尤其是在要求高精度时。

图 11.22 给出了原始–对偶内点法求解 §11.3.2 中 GP 的进展。其收敛情况与 LP 示例相似。

<!-- pdf-page: 628 -->

<figure id="fig-11-21" data-figure="11.21">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-21.png" alt="原始–对偶内点法求解线性规划的两条收敛曲线；左图为替代对偶间隙 η̂，右图为可行性残差范数 r_feas，纵轴均为对数刻度。右图约在第 24 次迭代骤降，左图约在第 28 次迭代达到很小值。" data-source-page="628" data-source-rect="130,159,524,307">
<figcaption>图 11.21 原始–对偶内点法求解一个线性规划时的迭代过程，图中给出了替代对偶间隙 $\widehat\eta$ 以及原残差与对偶残差的范数随迭代次数的变化。残差在 $24$ 次迭代内迅速收敛到零；替代对偶间隙也在约 $28$ 次迭代后收敛到很小的数值。原始–对偶内点法比障碍法收敛更快，尤其是在要求高精度时。</figcaption>
<p class="figure-translation">图内文字：左右两图的 iteration number——迭代次数。</p>
</figure>

<figure id="fig-11-22" data-figure="11.22">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-22.png" alt="原始–对偶内点法求解几何规划的两条收敛曲线；左图为替代对偶间隙 η̂，右图为可行性残差范数 r_feas，两者随迭代次数逐渐减小，并在后几次迭代中快速下降，纵轴均为对数刻度。" data-source-page="628" data-source-rect="130,463,524,611">
<figcaption>图 11.22 原始–对偶内点法求解一个几何规划时的迭代过程，图中给出了替代对偶间隙 $\widehat\eta$ 以及原残差与对偶残差的范数随迭代次数的变化。</figcaption>
<p class="figure-translation">图内文字：左右两图的 iteration number——迭代次数。</p>
</figure>

<!-- pdf-page: 629 -->

<figure id="fig-11-23" data-figure="11.23" data-reader-after="ch11-primal-dual-lp-family-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-23.png" alt="问题规模 m 从 10 增至 1000 时，平均迭代次数由约 16 次增至约 38 次；横轴为对数刻度，各圆圈处的竖直误差条表示标准差。" data-source-page="629" data-source-rect="168,121,388,295">
<figcaption>图 11.23 求解随机生成、规模不同的标准形式线性规划所需的迭代次数，其中 $n=2m$。对于每种规模的 $100$ 个实例，误差条表示平均值上下的标准差。当最大与最小问题规模之比达到 $100:1$ 时，所需迭代次数近似按对数增长。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>

#### 一族 LP

<p id="ch11-primal-dual-lp-family-end" markdown="1">这里使用 §11.3.2 考虑过的同一族标准形式 LP，考察原始–对偶方法的表现如何随问题维度变化。使用原始–对偶内点法求解相同的 $2000$ 个实例，其中每个 $m$ 值对应 $100$ 个实例。原始–对偶算法从 $x^{(0)}=\mathbf{1}$、$\lambda^{(0)}=\mathbf{1}$、$\nu^{(0)}=0$ 出发，终止容差取 $\epsilon=10^{-8}$。图 11.23 给出了所需迭代次数的均值和标准差随 $m$ 的变化。迭代次数在 $15$ 到 $35$ 之间，大致随 $m$ 的对数增长。与图 11.8 中障碍法的结果相比可以看到，尽管从不可行初始点出发，而且将问题求解到高得多的精度，原始–对偶方法的迭代次数仍然只略多一些。</p>

## 11.8 实现

障碍法的主要计算工作是求中心化问题的牛顿步，这需要求解如下形式的线性方程组：

$$
\begin{bmatrix}H&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\nu_{\mathrm{nt}}\end{bmatrix}
=-\begin{bmatrix}g\\0\end{bmatrix},
\tag{11.60}
$$

其中

$$
H=t\nabla^2f_0(x)+\sum_{i=1}^m\frac{1}{f_i(x)^2}\nabla f_i(x)\nabla f_i(x)^T
+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla^2f_i(x)
$$

<!-- pdf-page: 630 -->

$$
g=t\nabla f_0(x)+\sum_{i=1}^m\frac{1}{-f_i(x)}\nabla f_i(x).
$$

原始–对偶方法的牛顿方程组具有完全相同的结构，因此本节的讨论也适用于原始–对偶方法。

(11.60) 的系数矩阵具有 KKT 结构，所以 §9.7 和 §10.4 中的全部讨论都适用于这里。特别地，可以通过消元求解这些方程，并利用稀疏、对角加低秩等结构。下面给出几个一般性的例子，说明如何利用 KKT 方程组的特殊结构，更高效地计算牛顿步。

#### 稀疏问题

如果原问题是稀疏的，即目标函数和每个约束函数都只依赖少量变量，那么目标函数和约束函数的梯度、Hessian 矩阵以及系数矩阵 $A$ 都是稀疏的。只要 $m$ 不太大，矩阵 $H$ 就很可能也是稀疏的，因此可以使用稀疏矩阵方法计算牛顿步。即使 KKT 矩阵中有少量比较稠密的行和列，这种方法也很可能表现良好；例如，少数等式约束涉及大量变量时，就会出现这种情况。

#### 可分目标函数与少量线性不等式约束

假设目标函数可分，而且只有相对较少的线性等式和不等式约束。那么 $\nabla^2f_0(x)$ 是对角矩阵，各项 $\nabla^2f_i(x)$ 都为零，因此矩阵 $H$ 具有对角加低秩结构。由于 $H$ 容易求逆，所以可以高效地求解 KKT 方程组。只要 $\nabla^2f_0(x)$ 容易求逆，例如它是带状、稀疏或块对角矩阵，就可以采用同样的方法。

### 11.8.1 标准形式的线性规划

首先讨论标准形式 LP 的障碍法实现：

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &Ax=b,\quad x\succeq0,
\end{aligned}
$$

其中 $A\in\mathbf{R}^{m\times n}$。中心化问题

$$
\begin{aligned}
\text{最小化}\quad &tc^Tx-\textstyle\sum_{i=1}^n\log x_i\\
\text{约束为}\quad &Ax=b
\end{aligned}
$$

的牛顿方程组为

$$
\begin{bmatrix}\mathbf{diag}(x)^{-2}&A^T\\A&0\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\nu_{\mathrm{nt}}\end{bmatrix}
=\begin{bmatrix}-tc+\mathbf{diag}(x)^{-1}\mathbf{1}\\0\end{bmatrix}.
$$

<!-- pdf-page: 631 -->

通常通过分块消去 $\Delta x_{\mathrm{nt}}$ 来求解这些方程。由第一个方程，

$$
\begin{aligned}
\Delta x_{\mathrm{nt}}&=\mathbf{diag}(x)^2(-tc+\mathbf{diag}(x)^{-1}\mathbf{1}-A^T\nu_{\mathrm{nt}})\\
&=-t\mathbf{diag}(x)^2c+x-\mathbf{diag}(x)^2A^T\nu_{\mathrm{nt}}.
\end{aligned}
$$

代入第二个方程得到

$$
A\mathbf{diag}(x)^2A^T\nu_{\mathrm{nt}}=-tA\mathbf{diag}(x)^2c+b.
$$

由于假设 $\mathbf{rank}\,A=m$，系数矩阵是正定的。而且，如果 $A$ 稀疏，那么 $A\mathbf{diag}(x)^2A^T$ 通常也是稀疏的，因此可以使用稀疏 Cholesky 分解。

### 11.8.2 $\ell_1$ 范数逼近

考虑 $\ell_1$ 范数逼近问题

$$
\text{最小化}\quad\|Ax-b\|_1,
$$

其中 $A\in\mathbf{R}^{m\times n}$。在讨论实现时，假设 $m,n$ 很大，而且 $A$ 具有某种结构，例如稀疏结构；我们还会将它与对应最小二乘问题

$$
\text{最小化}\quad\|Ax-b\|_2^2
$$

的计算代价作比较。

首先引入辅助变量 $y\in\mathbf{R}^m$，将 $\ell_1$ 范数逼近问题表述为 LP：

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{1}^Ty\\
\text{约束为}\quad &\begin{bmatrix}A&-I\\-A&-I\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}\preceq\begin{bmatrix}b\\-b\end{bmatrix}.
\end{aligned}
$$

中心化问题的牛顿方程为

$$
\begin{bmatrix}A^T&-A^T\\-I&-I\end{bmatrix}
\begin{bmatrix}D_1&0\\0&D_2\end{bmatrix}
\begin{bmatrix}A&-I\\-A&-I\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\Delta y_{\mathrm{nt}}\end{bmatrix}
=-\begin{bmatrix}A^Tg_1\\g_2\end{bmatrix},
$$

其中

$$
D_1=\mathbf{diag}(b-Ax+y)^{-2},\qquad
D_2=\mathbf{diag}(-b+Ax+y)^{-2},
$$

且

$$
\begin{aligned}
g_1&=\mathbf{diag}(b-Ax+y)^{-1}\mathbf{1}-\mathbf{diag}(-b+Ax+y)^{-1}\mathbf{1}\\
g_2&=t\mathbf{1}-\mathbf{diag}(b-Ax+y)^{-1}\mathbf{1}-\mathbf{diag}(-b+Ax+y)^{-1}\mathbf{1}.
\end{aligned}
$$

将左端的乘积展开，可以简化为

$$
\begin{bmatrix}
A^T(D_1+D_2)A&-A^T(D_1-D_2)\\
-(D_1-D_2)A&D_1+D_2
\end{bmatrix}
\begin{bmatrix}\Delta x_{\mathrm{nt}}\\\Delta y_{\mathrm{nt}}\end{bmatrix}
=-\begin{bmatrix}A^Tg_1\\g_2\end{bmatrix}.
$$

<!-- pdf-page: 632 -->

分块消去 $\Delta y_{\mathrm{nt}}$，可以将其约化为

$$
A^TDA\Delta x_{\mathrm{nt}}=-A^Tg,
\tag{11.61}
$$

其中

$$
D=4D_1D_2(D_1+D_2)^{-1}=2\left(\mathbf{diag}(y)^2+\mathbf{diag}(b-Ax)^2\right)^{-1},
$$

且

$$
g=g_1+(D_1-D_2)(D_1+D_2)^{-1}g_2.
$$

求出 $\Delta x_{\mathrm{nt}}$ 之后，由下式得到 $\Delta y_{\mathrm{nt}}$：

$$
\Delta y_{\mathrm{nt}}=(D_1+D_2)^{-1}(-g_2+(D_1-D_2)A\Delta x_{\mathrm{nt}}).
$$

可以注意到，(11.61) 是加权最小二乘问题

$$
\text{最小化}\quad\|D^{1/2}(A\Delta x+D^{-1}g)\|_2
$$

的正规方程。换言之，求解 $\ell_1$ 范数逼近问题的代价，相当于求解少量加权最小二乘问题的代价；这些问题具有相同的矩阵 $A$，但权重在每次迭代中变化。如果 $A$ 的结构允许快速求解最小二乘问题，例如可以利用稀疏性，那么也可以快速求解 (11.61)。

### 11.8.3 不等式形式的半定规划

考虑 SDP

$$
\begin{aligned}
\text{最小化}\quad &c^Tx\\
\text{约束为}\quad &\textstyle\sum_{i=1}^n x_iF_i+G\preceq0,
\end{aligned}
$$

变量为 $x\in\mathbf{R}^n$，参数为 $F_1,\ldots,F_n,G\in\mathbf{S}^p$。使用对数行列式障碍函数时，对应的中心化问题为

$$
\text{最小化}\quad tc^Tx-\log\det\left(-\textstyle\sum_{i=1}^n x_iF_i-G\right).
$$

牛顿步 $\Delta x_{\mathrm{nt}}$ 由 $H\Delta x_{\mathrm{nt}}=-g$ 求得，其中 Hessian 矩阵和梯度为

$$
\begin{aligned}
H_{ij}&=\mathbf{tr}(S^{-1}F_iS^{-1}F_j),\quad i,j=1,\ldots,n\\
g_i&=tc_i+\mathbf{tr}(S^{-1}F_i),\quad i=1,\ldots,n,
\end{aligned}
$$

这里 $S=-\sum_{i=1}^n x_iF_i-G$。一种标准做法是先构造 $H$ 和 $g$，再通过 Cholesky 分解求解牛顿方程。

先考虑没有特殊结构的情况，即假设所有矩阵都是稠密的。这里只记录浮点运算次数相对于问题维度 $n,p$ 的增长阶。首先构造 $S$，需要 $np^2$ 阶浮点运算。然后，对每个 $i$，先对 $S$ 作 Cholesky 分解，再以 $F_i$ 的各列为右端项回代，计算矩阵 $S^{-1}F_i$；也可以先求出 $S^{-1}$，再与 $F_i$ 相乘。对每个 $i$，代价为 $p^3$ 阶，所以总代价为 $np^3$ 阶。最后，<!-- pdf-page: 633 -->将矩阵 $S^{-1}F_i$ 与 $S^{-1}F_j$ 的内积作为 $H_{ij}$，这需要 $p^2$ 阶浮点运算。由于要对 $n(n+1)/2$ 对矩阵执行这一操作，所以代价为 $n^2p^2$ 阶。求解牛顿方向的代价为 $n^3$ 阶。因此，主导项的阶为 $\max\{np^3,n^2p^2,n^3\}$。

<div class="translator-note" markdown="1">

**译注：这里的矩阵“内积”。** $S^{-1}F_i$ 和 $S^{-1}F_j$ 一般不对称。此处 $H_{ij}$ 应按前式的 $\mathbf{tr}(S^{-1}F_iS^{-1}F_j)$ 计算，不能直接把两个矩阵对应元素的乘积相加。

</div>

一般而言，无法利用矩阵 $F_i,G$ 的稀疏性，因为即使 $F_i,G$ 稀疏，$H$ 往往仍是稠密的。一个例外是 $F_i,G$ 具有共同的块对角结构；此时上述所有运算都可以逐块执行。

通常可以利用 $F_i,G$ 的共同稀疏性，更高效地构造稠密的 Hessian 矩阵 $H$。如果能找到一种排序，使 $S$ 的 Cholesky 因子相当稀疏，那么就可以高效地计算矩阵 $S^{-1}F_i$，并更高效地构造 $H_{ij}$。

一个经常出现的有趣例子，是含有矩阵不等式

$$
\mathbf{diag}(x)\preceq B
$$

的 SDP。这对应于 $F_i=E_{ii}$，其中 $E_{ii}$ 是第 $(i,i)$ 个元素为 $1$、其余元素均为零的矩阵。此时，可以非常高效地求得矩阵 $H$：

$$
H_{ij}=(S^{-1})_{ij}^2,
$$

其中 $S=B-\mathbf{diag}(x)$。因此，构造 $H$ 的代价就是求出 $S^{-1}$ 的代价，至多为 $n^3$ 阶，即不利用其他结构时的代价。

### 11.8.4 网络速率优化

考虑 §10.4.3（第 550 页）所述最优网络流问题的一个变体，它有时称为网络速率优化问题（network rate optimization problem）。网络用一个具有 $L$ 条弧或链路的有向图描述。货物或信息包在网络中传输，经过各条链路。网络承载 $n$ 条流，其非负速率 $x_1,\ldots,x_n$ 是优化变量。每条流沿网络中一条固定或预先确定的路径（或路由），从源节点移动到目的节点。每条链路可以承载多条流。链路上的总流量是经过该链路的所有流的速率之和。每条链路都有一个正的容量，即它能够承载的最大总流量。

这些链路容量限制可以用流–链路关联矩阵 $A\in\mathbf{R}^{L\times n}$ 描述，其定义为

$$
A_{ij}=\begin{cases}
1&\text{流 }j\text{ 经过链路 }i,\\
0&\text{其他情况。}
\end{cases}
$$

链路 $i$ 的总流量就是 $(Ax)_i$，所以链路容量约束可以写成 $Ax\preceq c$，其中 $c_i$ 是链路 $i$ 的容量。通常，每条路径只经过全部链路中的一小部分，因此矩阵 $A$ 是稀疏的。

在网络速率问题中，路径固定，并由作为问题参数的矩阵 $A$ 表示；变量是各流的速率 $x_i$。目标是<!-- pdf-page: 634 -->选择流速率，使可分效用函数 $U$ 最大，其表达式为

$$
U(x)=U_1(x_1)+\cdots+U_n(x_n).
$$

假设每个 $U_i$ 都是凹的、非减的，因而 $U$ 也是。可以将 $U_i(x_i)$ 看作以速率 $x_i$ 承载第 $i$ 条流所获得的收入；$U(x)$ 就是这些流对应的总收入。网络速率优化问题为

$$
\begin{aligned}
\text{最大化}\quad &U(x)\\
\text{约束为}\quad &Ax\preceq c,\quad x\succeq0,
\end{aligned}
\tag{11.62}
$$

这是一个凸优化问题。

用障碍法求解这个问题时，每一步都必须用牛顿法最小化一个如下形式的函数：

$$
-tU(x)-\sum_{i=1}^L\log(c-Ax)_i-\sum_{j=1}^n\log x_j.
$$

牛顿步 $\Delta x_{\mathrm{nt}}$ 通过求解线性方程组

$$
(D_0+A^TD_1A+D_2)\Delta x_{\mathrm{nt}}=-g
$$

得到，其中

$$
\begin{aligned}
D_0&=-t\mathbf{diag}(U_1''(x),\ldots,U_n''(x))\\
D_1&=\mathbf{diag}(1/(c-Ax)_1^2,\ldots,1/(c-Ax)_L^2)\\
D_2&=\mathbf{diag}(1/x_1^2,\ldots,1/x_n^2)
\end{aligned}
$$

是对角矩阵，$g\in\mathbf{R}^n$。可以精确描述这个 $n\times n$ 系数矩阵的稀疏结构：

$$
(D_0+A^TD_1A+D_2)_{ij}\neq0
$$

当且仅当流 $i$ 和流 $j$ 共用一条链路。如果路径较短，而且每条链路上经过的路径较少，这个矩阵就是稀疏的，因此可以使用稀疏 Cholesky 分解。当矩阵中只有少量行和列比较稠密时，也能高效地求解牛顿方程组。少数流与大量其他流相交时就会出现这种情况，例如，少数流的路径较长时可能如此。

还可以利用矩阵求逆引理，通过求解一个系数矩阵为 $L\times L$ 的方程组来计算牛顿步。该方程组为

$$
\left(D_1^{-1}+A(D_0+D_2)^{-1}A^T\right)y=-A(D_0+D_2)^{-1}g,
$$

然后计算

$$
\Delta x_{\mathrm{nt}}=-(D_0+D_2)^{-1}(g+A^Ty).
$$

这里同样可以精确描述稀疏结构：

$$
\left(D_1^{-1}+A(D_0+D_2)^{-1}A^T\right)_{ij}\neq0
$$

当且仅当存在一条同时经过链路 $i$ 和链路 $j$ 的路径。如果多数路径都很短，这个矩阵就是稀疏的。如果存在少数瓶颈，即少数有很多条流经过的链路，那么这个矩阵会是稀疏的，但带有少量稠密行和列。

<!-- pdf-page: 635 -->

## 文献说明

Fiacco 和 McCormick [FM90, §1.2] 详细介绍了障碍法的早期历史。20 世纪 60 年代，障碍法是一种流行的凸优化算法，与它密切相关的技术还包括中心法（Liêũ 和 Huard [LH66]；另见习题 11.11），以及罚函数法（或外点法）[FM90, §4]。到了 20 世纪 70 年代，人们担心当 $t$ 很大时，中心化问题 (11.6) 的牛顿方程组会严重病态，因此对这种方法的兴趣有所下降。

20 世纪 80 年代，Gill、Murray、Saunders、Tomlin 和 Wright [GMS+86] 指出，障碍法与 Karmarkar 的线性规划多项式时间投影算法 [Kar84] 密切相关，障碍法由此重新受到关注。整个 80 年代的研究仍主要集中在线性规划上，对二次规划的关注相对较少；这些研究产生了基本内点法的不同变体，并改进了最坏情形复杂度结果（见 Gonzaga [Gon92]）。原始–对偶方法逐渐成为实际实现中的首选算法（见 Mehrotra [Meh92]，Lustig、Marsten 和 Shanno [LMS94]，以及 Wright [Wri97]）。

Nesterov 和 Nemirovski 在 1994 年的专著中，利用自协调函数的牛顿法收敛理论，将线性规划内点法的复杂度理论扩展到了非线性凸优化问题。他们还为含广义不等式的问题提出了内点法，并讨论了通过重新表述问题来满足自协调性假设的方法。例如，第 587 页对几何规划的重新表述就来自 [NN94, §6.3.1]。

如第 585 页所述，复杂度分析表明，与人们可能预想的情况相反，障碍法的中心化问题不会随着 $t$ 增大而变得更困难，至少在精确算术下如此。实际经验及其理论支持（Forsgren、Gill 和 Wright [FGW02, §4.3.2]，Nocedal 和 Wright [NW99, 第 525 页]）也表明，病态性对牛顿方程组计算所得解的影响，比早先认为的要温和。

近期的内点法研究主要集中于将线性规划的原始–对偶方法推广到非线性凸问题；原始–对偶方法比基于原变量的障碍法收敛更快，并能达到更高精度。一种常用做法沿用 §11.7 中简单原始–对偶方法的思路，对标准形式凸优化问题，即问题 (11.1) 的修正 KKT 方程组进行线性化。同类的更复杂算法与算法 11.2 的区别，在于选择 $t$ 的策略和直线搜索；其中，$t$ 的选择对实现渐近超线性收敛至关重要。详细论述及参考文献可参见 Wright [Wri97, 第 8 章]、Ralph 和 Wright [RW97]、den Hertog [dH93]、Terlaky [Ter96]，以及 Forsgren、Gill 和 Wright 的综述 [FGW02, §5]。

另一些作者以锥规划框架为出发点，将线性规划的原始–对偶内点法扩展到凸优化，例如 Nesterov 和 Todd [NT98]。这种做法产生了高效而精确的半定规划和二阶锥规划原始–对偶方法（见 Todd [Tod01] 以及 Alizadeh 和 Goldfarb [AG03] 的综述）。

与线性规划一样，半定规划的原始–对偶方法通常也表述为对修正 KKT 方程组应用牛顿法的变体。但与线性规划不同，线性化可以用许多不同方式进行，产生不同的搜索方向和算法；见 Helmberg、Rendl、Vanderbei 和 Wolkowicz [HRVW96]，Kojima、Shindo 和 Harah [KSH97]，Monteiro [Mon97]，Nesterov 和 Todd [NT98]，Zhang [Zha98]，Alizadeh、Haeberly 和 Overton [AHO98]，以及 Todd、Toh 和 Tütüncü [TTT98]。

初始化和不可行性检测方面也取得了很大进展。齐次自对偶表述为 §11.4 中经典的两阶段方法提供了一种简洁而高效的替代方案；详见 Ye、Todd 和 Mizuno [YTM94]，Xu、Hung<!-- pdf-page: 636 -->和 Ye [XHY96]，Andersen 和 Ye [AY98]，以及 Luo、Sturm 和 Zhang [LSZ00]。

半定规划和二阶锥规划的原始–对偶内点法已在多个软件包中实现，包括 SeDuMi [Stu99]、SDPT3 [TTT02]、SDPA [FKN98]、CSDP [Bor02] 和 DSDP [BY02]。YALMIP [Löf04] 为其中若干程序提供了易用的接口。

以下专著更详细地记录了这一快速发展领域的近期进展：Vanderbei [Van96]，Wright [Wri97]，Roos、Terlaky 和 Vial [RTV97]，Ye [Ye97]，Wolkowicz、Saigal 和 Vandenberghe [WSV00]，Ben-Tal 和 Nemirovski [BTN01]，Renegar [Ren01]，以及 Peng、Roos 和 Terlaky [PRT02]。

<!-- pdf-page: 637 -->

## 习题

### 障碍法

**11.1 障碍法示例。** 考虑简单问题

$$
\begin{aligned}
\text{最小化}\quad &x^2+1\\
\text{约束为}\quad &2\leq x\leq4,
\end{aligned}
$$

其可行集为 $[2,4]$，最优点为 $x^\star=2$。对几个不同的 $t>0$ 值，画出 $f_0$ 和 $tf_0+\phi$ 随 $x$ 变化的曲线，并标出 $x^\star(t)$。

**11.2** 如果将障碍法用于变量为 $x\in\mathbf{R}^2$ 的 LP

$$
\begin{aligned}
\text{最小化}\quad &x_2\\
\text{约束为}\quad &x_1\leq x_2,\quad0\leq x_2,
\end{aligned}
$$

会发生什么？

**11.3 中心化问题的有界性。** 假设问题 (11.1)

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m\\
&Ax=b
\end{aligned}
$$

的下水平集有界。证明相应中心化问题

$$
\begin{aligned}
\text{最小化}\quad &tf_0(x)+\phi(x)\\
\text{约束为}\quad &Ax=b
\end{aligned}
$$

的下水平集也有界。

**11.4 加入范数界以保证中心化问题的强凸性。** 假设在问题 (11.1) 中加入约束 $x^Tx\leq R^2$：

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m\\
&Ax=b\\
&x^Tx\leq R^2.
\end{aligned}
$$

用 $\tilde\phi$ 表示修改后问题的对数障碍函数。求一个 $a>0$，使得对所有可行的 $x$ 都有 $\nabla^2(tf_0(x)+\tilde\phi(x))\succeq aI$。

**11.5 二阶锥规划的障碍法。** 考虑 SOCP（为简单起见，不含等式约束）

$$
\begin{aligned}
\text{最小化}\quad &f^Tx\\
\text{约束为}\quad &\|A_ix+b_i\|_2\leq c_i^Tx+d_i,\quad i=1,\ldots,m.
\end{aligned}
\tag{11.63}
$$

这个问题的约束函数不可微，因为欧几里得范数 $\|u\|_2$ 在 $u=0$ 处不可微，所以不能应用标准障碍法。在 §11.6 中，我们已经看到，可以使用能处理广义不等式的障碍法扩展来求解这个 SOCP（见第 599 页的例 11.8，以及第 601 页）。本题说明，如何用约束函数为标量值的标准障碍法求解该 SOCP。

首先将 SOCP 重新表述为

$$
\begin{aligned}
\text{最小化}\quad &f^Tx\\
\text{约束为}\quad &\|A_ix+b_i\|_2^2/(c_i^Tx+d_i)\leq c_i^Tx+d_i,\quad i=1,\ldots,m\\
&c_i^Tx+d_i\geq0,\quad i=1,\ldots,m.
\end{aligned}
\tag{11.64}
$$

<!-- pdf-page: 638 -->

约束函数

$$
f_i(x)=\frac{\|A_ix+b_i\|_2^2}{c_i^Tx+d_i}-c_i^Tx-d_i
$$

是二次除以线性函数与仿射函数的复合；只要将其定义域取为 $\mathbf{dom}\,f_i=\{x\mid c_i^Tx+d_i>0\}$，它就是二阶可微的，而且是凸的。注意，问题 (11.63) 与 (11.64) 并非完全等价。如果 SOCP (11.63) 的最优解 $x^\star$ 对某个 $i$ 满足 $c_i^Tx^\star+d_i=0$，那么重新表述的问题 (11.64) 没有最优解，因为 $x^\star$ 不在它的定义域中。不过，我们将看到，将障碍法用于 (11.64)，可以得到任意高精度的次优解，因而也能得到 (11.63) 的任意高精度次优解。

- (a) 构造问题 (11.64) 的对数障碍函数 $\phi$。将其与用广义不等式障碍法（§11.6）求解 SOCP (11.63) 时出现的对数障碍函数作比较。

- (b) 证明，如果 $tf^Tx+\phi(x)$ 已被最小化，则极小点 $x^\star(t)$ 对问题 (11.63) 的次优程度不超过 $2m/t$。因此，将标准障碍法用于重新表述的问题 (11.64)，就能在产生任意高精度次优解的意义下求解 SOCP (11.63)。即使最优点 $x^\star$ 不在重新表述的问题 (11.64) 的定义域内，这个结论仍然成立。

**11.6 一般障碍函数。** 对数障碍函数基于对指示函数 $\hat I_-(u)$ 的近似 $-(1/t)\log(-u)$（见 §11.2.1，第 563 页）。也可以用其他近似构造障碍函数，进而推广中心路径和障碍法。设 $h:\mathbf{R}\to\mathbf{R}$ 是二阶可微、闭、递增的凸函数，且 $\mathbf{dom}\,h=-\mathbf{R}_{++}$。（这意味着当 $u\to0$ 时，$h(u)\to\infty$。）$h(u)=-\log(-u)$ 就是这样的函数；另一个例子是 $h(u)=-1/u$，$u<0$。

现在考虑优化问题（为简单起见，不含等式约束）

$$
\begin{aligned}
\text{最小化}\quad &f_0(x)\\
\text{约束为}\quad &f_i(x)\leq0,\quad i=1,\ldots,m,
\end{aligned}
$$

其中 $f_i$ 二阶可微。将这个问题的 $h$ 障碍函数定义为

$$
\phi_h(x)=\sum_{i=1}^m h(f_i(x)),
$$

其定义域为 $\{x\mid f_i(x)<0,\ i=1,\ldots,m\}$。当 $h(u)=-\log(-u)$ 时，它就是通常的对数障碍函数；当 $h(u)=-1/u$ 时，$\phi_h$ 称为倒数障碍函数（inverse barrier）。将 $h$ 中心路径定义为

$$
x^\star(t)=\operatorname*{argmin}\,tf_0(x)+\phi_h(x),
$$

其中 $t>0$ 是参数。（假设对每个 $t$，极小点都存在且唯一。）

- (a) 解释为什么对每个 $t>0$，$tf_0(x)+\phi_h(x)$ 都是关于 $x$ 的凸函数。

- (b) 说明如何由 $x^\star(t)$ 构造一个对偶可行的 $\lambda$。求出相应的对偶间隙。

- (c) 对于哪些函数 $h$，(b) 中求出的对偶间隙只依赖 $t$ 和 $m$，而与其他问题数据无关？

**11.7 中心路径的切向量。** 本题研究 $dx^\star(t)/dt$，它给出了中心路径在点 $x^\star(t)$ 处的切向量。为简单起见，考虑不含等式约束的问题；结果很容易推广到含等式约束的问题。

- (a) 求 $dx^\star(t)/dt$ 的显式表达式。*提示：* 对中心性方程 (11.7) 关于 $t$ 求导。

    <!-- pdf-page: 639 -->

- (b) 证明 $f_0(x^\star(t))$ 随 $t$ 增大而减小。因此，障碍法中的目标值会随着参数 $t$ 增大而减小。（我们已经知道，对偶间隙 $m/t$ 会随着 $t$ 增大而减小。）

**11.8 中心化问题的预测–校正法。** 在标准障碍法中，从初始点 $x^\star(t)$ 出发，用牛顿法计算 $x^\star(\mu t)$。有人提出了一种替代做法：先求出 $x^\star(\mu t)$ 的一个近似值或预测值 $\hat x$，然后从 $\hat x$ 出发，用牛顿法计算 $x^\star(\mu t)$。其想法是，这样应该能减少牛顿步数，因为 $\hat x$ 据推测比 $x^\star(t)$ 是更好的初始点。这种中心化方法称为预测–校正法（predictor-corrector method），因为它先预测 $x^\star(\mu t)$ 的值，再用牛顿法校正这个预测。

最常用的是一阶预测器，它基于习题 11.7 中研究的中心路径切向量。该预测器为

$$
\hat x=x^\star(t)+\frac{dx^\star(t)}{dt}(\mu t-t).
$$

推导一阶预测器 $\hat x$ 的表达式。将它与牛顿更新得到的点 $x^\star(t)+\Delta x_{\mathrm{nt}}$ 作比较，其中 $\Delta x_{\mathrm{nt}}$ 是 $\mu tf_0(x)+\phi(x)$ 在 $x^\star(t)$ 处的牛顿步。当目标函数 $f_0$ 为线性函数时，可以得出什么结论？（为简单起见，可以考虑不含等式约束的问题。）


**11.9 中心路径附近的对偶可行点。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$。假设函数 $f_i$ 是凸函数且二阶可微。（为简单起见，假设没有等式约束。）回顾 §11.2.2（第 565 页），$\lambda_i=-1/(tf_i(x^\star(t)))$，$i=1,\ldots,m$，是对偶可行的，而且 $x^\star(t)$ 实际上使 $L(x,\lambda)$ 最小。由此可以算出 $\lambda$ 处的对偶函数值为 $g(\lambda)=f_0(x^\star(t))-m/t$。特别地，可以断定 $x^\star(t)$ 的次优程度不超过 $m/t$。

本题考察点 $x$ 接近 $x^\star(t)$、但尚未完全中心化时的情况。（如果中心化步骤提前停止，或者没有计算到足够高的精度，就会出现这种情况。）此时，当然不能断言 $\lambda_i=-1/(tf_i(x))$，$i=1,\ldots,m$，是对偶可行的，也不能断言 $x$ 的次优程度不超过 $m/t$。不过，只要 $x$ 足够接近中心点，一个稍复杂的公式就能给出对偶可行点。

设 $\Delta x_{\mathrm{nt}}$ 是中心化问题

$$
\begin{array}{ll}
\text{最小化} & tf_0(x)-\sum_{i=1}^m\log(-f_i(x))
\end{array}
$$

在 $x$ 处的牛顿步。当 $\Delta x_{\mathrm{nt}}$ 很小（即 $x$ 已接近中心点）时，下面的公式往往能给出一个对偶可行点：

$$
\lambda_i=\frac{1}{-tf_i(x)}\left(1+\frac{\nabla f_i(x)^T\Delta x_{\mathrm{nt}}}{-f_i(x)}\right),
\qquad i=1,\ldots,m.
$$

在这种情况下，向量 $x$ 并不使 $L(x,\lambda)$ 最小，因此没有适用于一般情形的公式来计算与 $\lambda$ 对应的对偶函数值 $g(\lambda)$。（不过，如果已知对偶目标的解析表达式，就可以直接计算 $g(\lambda)$。）

验证，对于 QCQP

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TP_0x+q_0^Tx+r_0\\
\text{约束条件} & (1/2)x^TP_ix+q_i^Tx+r_i\leq0,\quad i=1,\ldots,m,
\end{array}
$$

当 $\Delta x_{\mathrm{nt}}$ 足够小时，上述 $\lambda$ 的公式会给出一个对偶可行点（即 $\lambda\succeq0$，且 $L(x,\lambda)$ 下方有界）。

<!-- pdf-page: 640 -->

*提示。* 定义

$$
x_0=x+\Delta x_{\mathrm{nt}},\qquad
x_i=x-\frac{1}{t\lambda_if_i(x)}\Delta x_{\mathrm{nt}},\quad i=1,\ldots,m.
$$

证明

$$
\nabla f_0(x_0)+\sum_{i=1}^m\lambda_i\nabla f_i(x_i)=0.
$$

然后利用 $f_i(z)\geq f_i(x_i)+\nabla f_i(x_i)^T(z-x_i)$，$i=0,\ldots,m$，推导 $L(z,\lambda)$ 的一个下界。

**11.10 中心路径的另一种参数化。** 考虑问题 (11.1)。对于 $t>0$，其中心路径 $x^\star(t)$ 定义为下列问题的解：

$$
\begin{array}{ll}
\text{最小化} & tf_0(x)-\sum_{i=1}^m\log(-f_i(x))\\
\text{约束条件} & Ax=b.
\end{array}
$$

本题探讨中心路径的另一种参数化。

对于 $u>p^\star$，用 $z^\star(u)$ 表示下列问题的解：

$$
\begin{array}{ll}
\text{最小化} & -\log(u-f_0(x))-\sum_{i=1}^m\log(-f_i(x))\\
\text{约束条件} & Ax=b.
\end{array}
$$

证明，当 $u>p^\star$ 时，由 $z^\star(u)$ 定义的曲线就是中心路径。（换言之，对于每个 $u>p^\star$，都存在 $t>0$，使 $x^\star(t)=z^\star(u)$；反过来，对于每个 $t>0$，都存在 $u>p^\star$，使 $z^\star(u)=x^\star(t)$。）

**11.11 解析中心法。** 本题考虑障碍法的一种变体，它以习题 11.10 描述的中心路径参数化为基础。为简单起见，考虑没有等式约束的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

解析中心法从任意严格可行初始点 $x^{(0)}$ 和任意 $u^{(0)}>f_0(x^{(0)})$ 出发。先令

$$
u^{(1)}=\theta u^{(0)}+(1-\theta)f_0(x^{(0)}),
$$

其中 $\theta\in(0,1)$ 是算法参数（通常取较小的值），再计算下一个迭代点

$$
x^{(1)}=z^\star(u^{(1)})
$$

（使用牛顿法，以 $x^{(0)}$ 为初始点）。这里 $z^\star(s)$ 表示

$$
-\log(s-f_0(x))-\sum_{i=1}^m\log(-f_i(x))
$$

的极小点，假设它存在且唯一。然后重复上述过程。

点 $z^\star(s)$ 是不等式

$$
f_0(x)\leq s,\qquad f_1(x)\leq0,\ldots,f_m(x)\leq0
$$

的解析中心，算法由此得名。

证明，中心法是有效的，即 $x^{(k)}$ 收敛到一个最优点。找出一个停止准则，保证 $x$ 是 $\epsilon$ 次优点，其中 $\epsilon>0$。

*提示。* 点 $x^{(k)}$ 位于中心路径上，见习题 11.10。利用这一点证明

$$
u^+-p^\star\leq\frac{m+\theta}{m+1}(u-p^\star),
$$

其中 $u$ 和 $u^+$ 是相邻两次迭代中的 $u$ 值。

<!-- pdf-page: 641 -->

**11.12 凸–凹博弈的障碍法。** 考虑带不等式约束的凸–凹博弈

$$
\begin{array}{ll}
\text{最小化}_w\ \text{最大化}_z & f_0(w,z)\\
\text{约束条件} & f_i(w)\leq0,\quad i=1,\ldots,m\\
& \tilde f_i(z)\leq0,\quad i=1,\ldots,\tilde m.
\end{array}
$$

这里，$w\in\mathbf{R}^n$ 是用于最小化目标的变量，$z\in\mathbf{R}^{\tilde n}$ 是用于最大化目标的变量。约束函数 $f_i$ 和 $\tilde f_i$ 是凸函数且可微，目标函数 $f_0$ 可微且为凸–凹函数，即固定任意 $z$ 时关于 $w$ 是凸的，固定任意 $w$ 时关于 $z$ 是凹的。为简单起见，假设 $\mathbf{dom}\,f_0=\mathbf{R}^n\times\mathbf{R}^{\tilde n}$。

博弈的一个*解*或*鞍点*是一对 $w^\star,z^\star$，使

$$
f_0(w^\star,z)\leq f_0(w^\star,z^\star)\leq f_0(w,z^\star)
$$

对每个可行的 $w$ 和 $z$ 都成立。（凸–凹博弈和凸–凹函数的背景，见 §5.4.3、§10.3.4，以及习题 3.14、5.24、5.25、10.10 和 10.13。）本题将说明如何利用障碍法的一个扩展和不可行初始点牛顿法（见 §10.3）求解这个博弈。

- (a) 设 $t>0$。说明为什么函数

    $$
    tf_0(w,z)-\sum_{i=1}^m\log(-f_i(w))+\sum_{i=1}^{\tilde m}\log(-\tilde f_i(z))
    $$

    关于 $(w,z)$ 是凸–凹函数。假设它有唯一的鞍点 $(w^\star(t),z^\star(t))$，可以用不可行初始点牛顿法求出。

- (b) 与用于求解凸优化问题的障碍法一样，可以推导出 $(w^\star(t),z^\star(t))$ 次优程度的一个简单上界。该上界只依赖于问题维度，并随着 $t$ 增大而减小到零。用 $W$ 和 $Z$ 分别表示 $w$ 和 $z$ 的可行集：

    $$
    W=\{w\mid f_i(w)\leq0,\ i=1,\ldots,m\},\qquad
    Z=\{z\mid\tilde f_i(z)\leq0,\ i=1,\ldots,\tilde m\}.
    $$

    证明

    $$
    \begin{aligned}
    f_0(w^\star(t),z^\star(t))&\leq\inf_{w\in W}f_0(w,z^\star(t))+\frac{m}{t},\\
    f_0(w^\star(t),z^\star(t))&\geq\sup_{z\in Z}f_0(w^\star(t),z)-\frac{\tilde m}{t},
    \end{aligned}
    $$

    因而

    $$
    \sup_{z\in Z}f_0(w^\star(t),z)-\inf_{w\in W}f_0(w,z^\star(t))\leq\frac{m+\tilde m}{t}.
    $$

### 自协调性与复杂度分析

**11.13 自协调性与负熵。**

- (a) 证明，负熵函数 $x\log x$（定义在 $\mathbf{R}_{++}$ 上）不是自协调函数。

- (b) 证明，对于任意 $t>0$，$tx\log x-\log x$（定义在 $\mathbf{R}_{++}$ 上）都是自协调函数。

**11.14 自协调性与中心化问题。** 设 $\phi$ 是问题 (11.1) 的对数障碍函数。假设 (11.1) 的下水平集有界，并且 $tf_0+\phi$ 是闭函数且自协调。证明，对于所有 $x\in\mathbf{dom}\,\phi$，都有 $t\nabla^2f_0(x)+\nabla^2\phi(x)\succ0$。*提示。* 见习题 9.17 和 11.3。

<!-- pdf-page: 642 -->

### 广义不等式的障碍法

**11.15 广义对数是 $K$ 递增的。** 设 $\psi$ 是正常锥 $K$ 的一个广义对数，且 $y\succ_K0$。

- (a) 证明，$\nabla\psi(y)\succeq_{K^*}0$，即 $\psi$ 是 $K$ 非减的。*提示。* 如果 $\nabla\psi(y)\nsucceq_{K^*}0$，那么存在某个 $w\succ_K0$，使 $w^T\nabla\psi(y)\leq0$。利用不等式 $\psi(sw)\leq\psi(y)+\nabla\psi(y)^T(sw-y)$，其中 $s>0$。

- (b) 进一步证明，$\nabla\psi(y)\succ_{K^*}0$，即 $\psi$ 是 $K$ 递增的。*提示。* 证明，$\nabla^2\psi(y)\prec0$ 和 $\nabla\psi(y)\succeq_{K^*}0$ 蕴含 $\nabla\psi(y)\succ_{K^*}0$。

**11.16 [NN94，第 41 页] 广义对数的性质。** 设 $\psi$ 是正常锥 $K$ 的一个广义对数，次数为 $\theta$。证明，下列性质对任意 $y\succ_K0$ 都成立。

- (a) 对所有 $s>0$，都有 $\nabla\psi(sy)=\nabla\psi(y)/s$。

- (b) $\nabla\psi(y)=-\nabla^2\psi(y)y$。

- (c) $y^T\nabla\psi^2(y)y=-\theta$。

- (d) $\nabla\psi(y)^T\nabla^2\psi(y)^{-1}\nabla\psi(y)=-\theta$。


<div class="translator-note" markdown="1">

**译注：习题 11.16 的导数记号。** 本题 (c) 中的 $\nabla\psi^2(y)$ 应理解为 $\nabla^2\psi(y)$，即该函数的 Hessian 矩阵。

</div>

**11.17 对偶广义对数。** 设 $\psi$ 是正常锥 $K$ 的广义对数，次数为 $\theta$。证明，式 (11.49) 定义的对偶广义对数 $\bar\psi$ 满足

$$
\bar\psi(sv)=\psi(v)+\theta\log s,
$$

其中 $v\succ_{K^*}0$、$s>0$。

<div class="translator-note" markdown="1">

**译注：习题 11.17 的对偶对数记号。** 上式右侧应写 $\bar\psi(v)$，使两侧都指对偶广义对数。

</div>

**11.18** 函数

$$
\psi(y)=\log\left(y_{n+1}-\frac{\sum_{i=1}^n y_i^2}{y_{n+1}}\right),
$$

其定义域为 $\mathbf{dom}\,\psi=\{y\in\mathbf{R}^{n+1}\mid y_{n+1}>\sum_{i=1}^n y_i^2\}$，是否是 $\mathbf{R}^{n+1}$ 中二阶锥的广义对数？

### 实现

**11.19 计算牛顿步的又一种方法。** 障碍法的牛顿步由线性方程组 (11.14) 的解给出。证明，也可以通过求解一个更大的线性方程组来得到这个牛顿步，其系数矩阵为

$$
\begin{bmatrix}
t\nabla^2 f_0(x)+\sum_i\dfrac{1}{-f_i(x)}\nabla^2 f_i(x) & Df(x)^T & A^T\\
Df(x) & -\mathbf{diag}(f(x))^2 & 0\\
A & 0 & 0
\end{bmatrix},
$$

其中 $f(x)=(f_1(x),\ldots,f_m(x))$。

对于哪些类型的问题结构，求解这个更大的方程组可能值得考虑？

**11.20 通过对偶问题进行网络速率优化。** 本题考察求解 §11.8.4 网络速率优化问题的一种对偶方法。为简化叙述，假设效用函数 $U_i$ 严格凹，定义域为 $\mathbf{dom}\,U_i=\mathbf{R}_{++}$，并且满足：当 $x_i\to0$ 时，$U_i'(x_i)\to\infty$；当 $x_i\to\infty$ 时，$U_i'(x_i)\to0$。

- (a) 用共轭效用函数 $V_i=(-U_i)^*$ 表示问题 (11.62) 的对偶问题，其中

    $$
    V_i(\lambda)=\sup_{x>0}(\lambda x+U_i(x)).
    $$

    证明，$\mathbf{dom}\,V_i=-\mathbf{R}_{++}$，并且对每个 $\lambda<0$，都存在唯一的 $x$ 满足 $U_i'(x)=-\lambda$。

- (b) 描述求解对偶问题的障碍法。将每次迭代的复杂度与 §11.8.4 中方法的复杂度作比较。像 §11.8.4 那样，分别讨论 $A^TA$ 稀疏和 $AA^T$ 稀疏这两种情况。

<div class="translator-note" markdown="1">

**译注：习题 11.20 的定义域边界。** 当 $\lambda=0$ 时，$V_i(0)=\sup_{x>0}U_i(x)$。仅凭题设，这个值可能有限，因此零也可能属于定义域。要得到题中声称的定义域，还需假设 $U_i$ 上方无界。

</div>

<!-- pdf-page: 643 -->

### 数值实验

**11.21 带界约束的对数 Chebyshev 逼近。** 考虑如下逼近问题：求 $x\in\mathbf{R}^n$，使它满足变量的界约束 $l\preceq x\preceq u$，并使 $Ax\approx b$，其中 $b\in\mathbf{R}^m$。可以假设 $l\prec u$ 且 $b\succ0$（原因将在下面说明）。用 $a_i^T$ 表示矩阵 $A$ 的第 $i$ 行。

我们用最大比例偏差（maximum fractional deviation）来衡量逼近 $Ax\approx b$ 的好坏。当 $Ax\succ0$ 时，这个量为

$$
\max_{i=1,\ldots,n}\max\{(a_i^Tx)/b_i,\ b_i/(a_i^Tx)\}
=\max_{i=1,\ldots,n}\frac{\max\{a_i^Tx,b_i\}}{\min\{a_i^Tx,b_i\}};
$$

当 $Ax\not\succ0$ 时，将最大比例偏差定义为 $\infty$。

最小化最大比例偏差的问题称为比例 Chebyshev 逼近问题（fractional Chebyshev approximation problem），也称为对数 Chebyshev 逼近问题，因为它等价于最小化目标

$$
\max_{i=1,\ldots,n}|\log a_i^Tx-\log b_i|.
$$

（另见习题 6.3 的 (c)。）

- (a) 将带变量界约束的比例 Chebyshev 逼近问题，表述为目标函数和约束函数均二阶可微的凸优化问题。

- (b) 实现求解比例 Chebyshev 逼近问题的障碍法。可以假设已知一个满足 $l\prec x^{(0)}\prec u$、$Ax^{(0)}\succ0$ 的初始点 $x^{(0)}$。

<div class="translator-note" markdown="1">

**译注：习题 11.21 的指标与引用。** 本题三个最大值运算的指标上限写为 $n$；由于矩阵有 $m$ 行，均应取 $i=1,\ldots,m$。所引习题 6.3(c) 实际应为 6.3(d)。

</div>

**11.22 多面体内的最大体积矩形。** 考虑习题 8.16 中的问题，即求一个体积最大的矩形 $\mathcal{R}=\{x\mid l\preceq x\preceq u\}$，使它位于由一组线性不等式描述的多面体 $\mathcal{P}=\{x\mid Ax\preceq b\}$ 内。实现求解这个问题的障碍法。可以假设 $b\succ0$，这意味着：当 $l\prec0$ 和 $u\succ0$ 都足够接近零时，矩形 $\mathcal{R}$ 位于 $\mathcal{P}$ 内。

在几个简单例子上测试你的实现。求下列数据所定义的多面体内的最大体积矩形：

$$
A=\begin{bmatrix}
0&-1\\
2&-4\\
2&1\\
-4&4\\
-4&0
\end{bmatrix},\qquad b=\mathbf{1}.
$$

画出这个多面体，以及位于其中的最大体积矩形。

**11.23 两路划分问题的 SDP 界与启发式方法。** 本题考虑第 219 页介绍、习题 5.39 也讨论过的两路划分问题 (5.7)：

$$
\begin{aligned}
\text{最小化}\quad &x^TWx\\
\text{约束为}\quad &x_i^2=1,\quad i=1,\ldots,n,
\end{aligned}
\tag{11.65}
$$

其中变量为 $x\in\mathbf{R}^n$。不失一般性，假设 $W\in\mathbf{S}^n$ 满足 $W_{ii}=0$。将划分问题的最优值记为 $p^\star$，用 $x^\star$ 表示一个最优划分。（注意，$-x^\star$ 也是一个最优划分。）

两路划分问题 (11.65) 的拉格朗日对偶是 SDP

$$
\begin{aligned}
\text{最大化}\quad &-\mathbf{1}^T\nu\\
\text{约束为}\quad &W+\mathbf{diag}(\nu)\succeq0,
\end{aligned}
\tag{11.66}
$$

<!-- pdf-page: 644 -->

其中变量为 $\nu\in\mathbf{R}^n$。这个 SDP 的对偶为

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(WX)\\
\text{约束为}\quad &X\succeq0\\
&X_{ii}=1,\quad i=1,\ldots,n,
\end{aligned}
\tag{11.67}
$$

其中变量为 $X\in\mathbf{S}^n$。（这个 SDP 可以解释为两路划分问题 (11.65) 的一个松弛；见习题 5.39。）这两个 SDP 的最优值相等，并给出最优值 $p^\star$ 的一个下界，将这个下界记为 $d^\star$。用 $\nu^\star$ 和 $X^\star$ 表示两个 SDP 的最优点。

- (a) 给定权重矩阵 $W$，实现求解 SDP (11.66) 及其对偶 (11.67) 的障碍法。说明如何得到近似最优的 $\nu$ 和 $X$，给出方法中所需的各个 Hessian 矩阵与梯度的公式，并说明如何计算牛顿步。在一些小规模问题实例上测试你的实现，将求得的界与最优值比较（检查全部 $2^n$ 种划分的目标值，就能求得最优值）。再随机选取一个规模足够大的问题实例，使得无法通过穷举搜索求得最优划分（例如 $n=100$），测试你的实现。

- (b) *一种划分启发式方法。* 在习题 5.39 中，你已经发现：如果 $X^\star$ 的秩为一，它必定具有 $X^\star=x^\star(x^\star)^T$ 的形式，其中 $x^\star$ 是两路划分问题的最优解。这启发了一种简单的方法，用来寻找一个好的划分，即使它未必是最优的：求解上面的 SDP，得到 $X^\star$ 及下界 $d^\star$。用 $v$ 表示 $X^\star$ 的最大特征值所对应的一个特征向量，并令 $\hat x=\mathbf{sign}(v)$。向量 $\hat x$ 就是我们对一个好划分的估计。

    在一些小规模问题实例，以及 (a) 中使用的大规模实例上试验这个启发式方法。将所得划分的目标值 $\hat x^TW\hat x$ 与下界 $d^\star$ 比较。

- (c) *随机化方法。* 已知 SDP (11.67) 的解 $X^\star$ 后，还可以用随机化技术寻找一个好的划分。方法很简单：从 $\mathbf{R}^n$ 上均值为零、协方差为 $X^\star$ 的正态分布中，生成独立样本 $x^{(1)},\ldots,x^{(K)}$。对每个样本，构造启发式近似解 $\hat x^{(k)}=\mathbf{sign}(x^{(k)})$。然后从这些解中选出最好的一个，即代价最小的一个。在一些小规模问题实例，以及 (a) 中考虑的大规模实例上试验这个过程。

- (d) *一种贪心启发式改进方法。* 假设已给定一个划分 $x$，即 $x_i\in\{-1,1\}$，$i=1,\ldots,n$。如果将元素 $i$ 从一个集合移到另一个集合，也就是把 $x_i$ 改为 $-x_i$，目标值会如何变化？现在考虑下面这个简单的贪心算法：给定初始划分 $x$，移动能使目标值下降最多的那个元素。反复执行这个过程，直到再也无法通过将一个元素从一个集合移到另一个集合来降低目标值。

    在一些问题实例上试验这个启发式方法，包括那个大规模实例。采用不同的初始划分，包括 $x=\mathbf{1}$、(b) 中得到的启发式近似解，以及 (c) 中随机生成的近似解。这种贪心改进能将 (b) 和 (c) 中的近似解改善多少？

**11.24 二次规划的障碍法与原始–对偶内点法。** 实现障碍法和原始–对偶法，求解下面的 QP（为简单起见，不含等式约束）：

$$
\begin{aligned}
\text{最小化}\quad &(1/2)x^TPx+q^Tx\\
\text{约束为}\quad &Ax\preceq b,
\end{aligned}
$$

其中 $A\in\mathbf{R}^{m\times n}$。可以假设已给定一个严格可行的初始点。在几个例子上测试你的代码。对于障碍法，画出对偶间隙随牛顿步数的变化。对于原始–对偶内点法，画出替代对偶间隙和对偶残差范数随迭代次数的变化。
