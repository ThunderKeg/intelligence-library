# 附录 D 变分法

<aside class="chapter-guide"><strong>附录导读</strong><p>变分法把最优化的对象扩展到函数。本附录通过对函数施加小扰动，引出泛函导数和 Euler–Lagrange 方程，说明寻找极值函数的基本步骤。</p></aside>

<!-- pdf-page: 723 -->

我们可以把函数 $y(x)$ 看成一个算子：对于任意输入值 $x$，它返回一个输出值 $y$。同样，可以把泛函（functional）$F[y]$ 定义为一个以函数 $y(x)$ 为输入、返回输出值 $F$ 的算子。泛函的一个例子是二维平面中一条曲线的长度，其中曲线的路径由函数定义。在机器学习中，一个广泛使用的泛函是连续变量 $x$ 的熵 $\mathrm{H}[x]$：对于任意选定的概率密度函数 $p(x)$，它都返回一个标量，表示 $x$ 在该密度下的熵。因此，$p(x)$ 的熵也完全可以写成 $\mathrm{H}[p]$。

普通微积分中的一个常见问题是，寻找使函数 $y(x)$ 最大或最小的 $x$ 值。类似地，在变分法中，我们寻找使泛函 $F[y]$ 最大或最小的函数 $y(x)$。也就是说，在所有可能的函数 $y(x)$ 中，找出使泛函 $F[y]$ 取最大值或最小值的那个具体函数。例如，变分法可以用来证明两点之间的最短路径是直线，也可以证明最大熵分布是高斯分布。

即使不熟悉普通微积分的求导规则，我们也可以让变量 $x$ 发生微小变化 $\epsilon$，然后按 $\epsilon$ 的幂展开，来计算通常的导数 $\mathrm{d}y/\mathrm{d}x$，得到

$$
y(x+\epsilon)=y(x)+\frac{\mathrm{d}y}{\mathrm{d}x}\epsilon+O(\epsilon^2)
\tag{D.1}
$$

最后再取 $\epsilon\to0$ 的极限。类似地，对于多元函数 $y(x_1,\ldots,x_D)$，相应的偏导数由下式定义：

$$
y(x_1+\epsilon_1,\ldots,x_D+\epsilon_D)=y(x_1,\ldots,x_D)+\sum_{i=1}^{D}\frac{\partial y}{\partial x_i}\epsilon_i+O(\epsilon^2).
\tag{D.2}
$$

类似地，我们考虑在一个函数上加上微小变化 $\epsilon\eta(x)$ 时，泛函 $F[y]$ 会改变多少，由此便得到泛函导数（functional derivative）的定义。这里所考虑的函数是

<!-- pdf-page: 724 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/appendix-d/a-fig-D-1.png" alt="原函数y(x)与加入微小扰动后的函数曲线"><figcaption>图 D.1：当函数 $y(x)$ 变为 $y(x)+\epsilon\eta(x)$ 时，考察泛函 $F[y]$ 的值如何变化，就可以定义泛函导数，其中 $\eta(x)$ 是 $x$ 的任意函数。</figcaption><p class="figure-translation">$y(x)$ → 原函数；$y(x)+\epsilon\eta(x)$ → 加入扰动后的函数；$x$ → 自变量。</p></figure>

<!-- join-previous-paragraph-across-figures -->

$y(x)$，其中 $\eta(x)$ 是 $x$ 的任意函数，如图 D.1 所示。我们将 $E[f]$ 对 $f(x)$ 的泛函导数记为 $\delta F/\delta f(x)$，并通过下式定义它：

$$
F[y(x)+\epsilon\eta(x)]=F[y(x)]+\epsilon\int\frac{\delta F}{\delta y(x)}\eta(x)\,\mathrm{d}x+O(\epsilon^2).
\tag{D.3}
$$

这可以看成式（D.2）的自然推广：现在 $F[y]$ 依赖于连续的一组变量，即 $y$ 在所有点 $x$ 处的取值。要求泛函对函数 $y(x)$ 的微小变化是驻定的，就得到

$$
\int\frac{\delta E}{\delta y(x)}\eta(x)\,\mathrm{d}x=0.
\tag{D.4}
$$

由于对任意选择的 $\eta(x)$，这个等式都必须成立，所以泛函导数必须为零。为说明这一点，设想选择一个扰动 $\eta(x)$，它除了在某一点 $\widehat{x}$ 的邻域内以外，其他地方都为零；此时，泛函导数在 $x=\widehat{x}$ 处必须为零。然而，对任意选取的 $\widehat{x}$，这一点都必须成立，因此泛函导数必须在所有 $x$ 处为零。

考虑一个由函数 $G(y,y',x)$ 的积分定义的泛函，其中 $G$ 同时依赖于 $y(x)$ 及其导数 $y'(x)$，还直接依赖于 $x$：

$$
F[y]=\int G\bigl(y(x),y'(x),x\bigr)\,\mathrm{d}x
\tag{D.5}
$$

这里假定 $y(x)$ 在积分区域边界上的值固定，边界也可能位于无穷远处。现在考虑函数 $y(x)$ 的变分，得到

$$
F[y(x)+\epsilon\eta(x)]=F[y(x)]+\epsilon\int\left\{\frac{\partial G}{\partial y}\eta(x)+\frac{\partial G}{\partial y'}\eta'(x)\right\}\,\mathrm{d}x+O(\epsilon^2).
\tag{D.6}
$$

接下来要将它整理成式（D.3）的形式。为此，对第二项作分部积分，并利用 $\eta(x)$ 在积分边界上必须为零这一事实，因为 $y(x)$ 在边界上固定不变。这样就得到

$$
F[y(x)+\epsilon\eta(x)]=F[y(x)]+\epsilon\int\left\{\frac{\partial G}{\partial y}-\frac{\mathrm{d}}{\mathrm{d}x}\left(\frac{\partial G}{\partial y'}\right)\right\}\eta(x)\,\mathrm{d}x+O(\epsilon^2)
\tag{D.7}
$$

<!-- pdf-page: 725 -->

将其与式（D.3）比较，就可以读出泛函导数。令泛函导数为零，便得到

$$
\frac{\partial G}{\partial y}-\frac{\mathrm{d}}{\mathrm{d}x}\left(\frac{\partial G}{\partial y'}\right)=0
\tag{D.8}
$$

这称为 *Euler–Lagrange 方程*。例如，如果

$$
G=y(x)^2+\left(y'(x)\right)^2
\tag{D.9}
$$

那么 Euler–Lagrange 方程就具有如下形式

$$
y(x)-\frac{\mathrm{d}^2y}{\mathrm{d}x^2}=0.
\tag{D.10}
$$

利用 $y(x)$ 的边界条件，就可以由这个二阶微分方程求出 $y(x)$。

我们经常考虑由积分定义的泛函，其被积函数具有 $G(y,x)$ 的形式，不依赖于 $y(x)$ 的导数。在这种情况下，驻定性只要求对所有 $x$ 都有 $\partial G/\partial y(x)=0$。

如果我们要关于某个概率分布优化泛函，就需要保持概率的归一化约束。通常，最方便的方法是使用一个拉格朗日乘子，从而可以进行无约束优化。<span class="margin-reference">附录 E</span>

上述结果可以直接推广到多维变量 $\mathbf{x}$。关于变分法更全面的讨论，参见 Sagan（1969）。

<!-- pdf-page: 726 -->
