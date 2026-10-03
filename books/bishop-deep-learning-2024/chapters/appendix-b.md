<!-- pdf-page: 625 -->

# 附录 B 变分法

<aside class="chapter-guide"><strong>本附录导读</strong><p>本附录从普通导数类比引出泛函导数，并推导一维变分问题的欧拉—拉格朗日方程。</p></aside>

可以把函数 $y(x)$ 看成一种算子：输入任意 $x$，输出 $y$。类似地，可以定义**泛函**（functional）$F[y]$：它以函数 $y(x)$ 为输入，返回数值 $F$。例如，二维平面中由函数确定的一条曲线的长度就是泛函。在机器学习中，一个广泛使用的泛函是连续变量 $x$ 的熵 $\mathrm H[x]$：选择任意概率密度函数 $p(x)$ 后，它返回表示 $x$ 在该密度下的熵的标量。因此，$p(x)$ 的熵同样可以写作 $\mathrm H[p]$。

常规微积分中的一个常见问题，是找出使函数 $y(x)$ 取得最大值或最小值的 $x$。类似地，在变分法中，我们寻找使泛函 $F[y]$ 最大或最小的函数 $y(x)$。也就是说，在所有可能的函数 $y(x)$ 中，找出使 $F[y]$ 取极值的特定函数。例如，可以用变分法证明，两点之间最短的路径是直线，以及最大熵分布是高斯分布。

即使不熟悉普通微积分的规则，也可以通过使变量 $x$ 发生微小变化 $\epsilon$、再按 $\epsilon$ 的幂展开，求得普通导数 $\mathrm dy/\mathrm dx$，即

$$
y(x+\epsilon)=y(x)+\frac{\mathrm dy}{\mathrm dx}\epsilon+\mathcal O(\epsilon^2). \tag{B.1}
$$

最后再取极限 $\epsilon\to0$。类似地，对于多变量函数 $y(x_1,\ldots,x_D)$，相应的偏导数由

$$
y(x_1+\epsilon_1,\ldots,x_D+\epsilon_D)
=y(x_1,\ldots,x_D)
+\sum_{i=1}^{D}\frac{\partial y}{\partial x_i}\epsilon_i
+\mathcal O(\epsilon^2) \tag{B.2}
$$

定义。泛函导数可以类比地定义：考察把函数

<!-- pdf-page: 626 -->
<!-- join-previous-paragraph -->

$y(x)$ 改变一小部分 $\epsilon\eta(x)$ 时，泛函 $F[y]$ 会变化多少；这里 $\eta(x)$ 是任意关于 $x$ 的函数，如图 B.1 所示。用 $\delta F/\delta y(x)$ 表示 $F[y]$ 对 $y(x)$ 的泛函导数，并由以下关系定义：

<figure id="fig-b-1">
  <img src="books/bishop-deep-learning-2024/assets/appendix-b/fig-b-1.png" alt="红色函数曲线 y(x) 在扰动后变为蓝色曲线 y(x) 加 εη(x)">
  <figcaption>图 B.1：考察把函数 $y(x)$ 改为 $y(x)+\epsilon\eta(x)$ 时，泛函 $F[y]$ 的值如何变化，由此可定义泛函导数；$\eta(x)$ 是任意关于 $x$ 的函数。</figcaption>
  <p class="figure-translation">图内符号：$y(x)$ 为原函数；$y(x)+\epsilon\eta(x)$ 为扰动后的函数；$x$ 为横轴变量。</p>
</figure>

$$
F[y(x)+\epsilon\eta(x)]
=F[y(x)]+\epsilon\int\frac{\delta F}{\delta y(x)}\eta(x)\,\mathrm dx
+\mathcal O(\epsilon^2). \tag{B.3}
$$

这可以看成式 (B.2) 的自然扩展：$F[y]$ 现在依赖于连续的一组变量，也就是函数 $y$ 在所有 $x$ 处的取值。要求泛函对于 $y(x)$ 的微小变化处于驻点，便有

$$
\int\frac{\delta F}{\delta y(x)}\eta(x)\,\mathrm dx=0. \tag{B.4}
$$

因为任意选择 $\eta(x)$ 时此式都必须成立，所以泛函导数必为零。设想选择一个扰动 $\eta(x)$，它仅在某个点 $\widehat x$ 的邻域内非零，其他地方均为零；此时泛函导数在 $x=\widehat x$ 处必须为零。由于任意 $\widehat x$ 都如此，所以泛函导数对所有 $x$ 都必须为零。

考虑一个由函数 $G(y,y',x)$ 的积分定义的泛函；$G$ 同时依赖于 $y(x)$、它的导数 $y'(x)$，并直接依赖于 $x$：

$$
F[y]=\int G(y(x),y'(x),x)\,\mathrm dx. \tag{B.5}
$$

假定在积分区域的边界处，$y(x)$ 的值固定；边界也可能位于无穷远处。若现在让函数 $y(x)$ 发生变化，就得到

$$
F[y(x)+\epsilon\eta(x)]
=F[y(x)]
+\epsilon\int\left\{
\frac{\partial G}{\partial y}\eta(x)
+\frac{\partial G}{\partial y'}\eta'(x)
\right\}\mathrm dx+\mathcal O(\epsilon^2). \tag{B.6}
$$

需要把它写成式 (B.3) 的形式。为此，对第二项分部积分，并注意积分边界处 $\eta(x)$ 必须为零，因为 $y(x)$ 在边界上固定。于是

$$
F[y(x)+\epsilon\eta(x)]
=F[y(x)]
+\epsilon\int\left\{
\frac{\partial G}{\partial y}
-\frac{\mathrm d}{\mathrm dx}\left(\frac{\partial G}{\partial y'}\right)
\right\}\eta(x)\,\mathrm dx
+\mathcal O(\epsilon^2). \tag{B.7}
$$

<!-- pdf-page: 627 -->

与式 (B.3) 比较，即可读出泛函导数。要求泛函导数为零，就有

$$
\frac{\partial G}{\partial y}
-\frac{\mathrm d}{\mathrm dx}\left(\frac{\partial G}{\partial y'}\right)=0, \tag{B.8}
$$

称为**欧拉—拉格朗日方程**。例如，若

$$
G=y(x)^2+\bigl(y'(x)\bigr)^2, \tag{B.9}
$$

则欧拉—拉格朗日方程为

$$
y(x)-\frac{\mathrm d^2y}{\mathrm dx^2}=0. \tag{B.10}
$$

这个二阶微分方程可结合 $y(x)$ 的边界条件求解。

我们常考虑另一类泛函：其被积函数形如 $G(y,x)$，不依赖于 $y(x)$ 的导数。这时，驻点条件只要求所有 $x$ 上均有 $\partial G/\partial y(x)=0$。

如果优化对象是概率分布的泛函，就需要保持概率归一化约束。通常最方便的做法是使用拉格朗日乘子（见附录 C），将问题化为无约束优化。

上述结果很容易推广到多维变量 $\mathbf x$。有关变分法的更全面讨论，见 Sagan（1969）。
