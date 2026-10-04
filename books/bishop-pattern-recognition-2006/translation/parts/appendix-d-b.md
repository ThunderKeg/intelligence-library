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
