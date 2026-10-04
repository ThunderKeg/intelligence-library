# 附录 E 拉格朗日乘子

<aside class="chapter-guide"><strong>附录导读</strong><p>拉格朗日乘子把约束条件并入目标函数，使原问题可以通过一组驻点方程求解。本附录先用几何关系解释等式约束，再讨论不等式约束及 KKT 条件；阅读时可留意乘子的符号，以及约束是否在解处取等号。</p></aside>

<!-- pdf-page: 727 -->

拉格朗日乘子（Lagrange multipliers）有时也称为未定乘子（undetermined multipliers），用于寻找多元函数在一个或多个约束条件下的驻点。

考虑在一个联系 $x_1$ 与 $x_2$ 的约束下，求函数 $f(x_1,x_2)$ 的最大值。将约束写成

$$
g(x_1,x_2)=0.
\tag{E.1}
$$

一种方法是求解约束方程（E.1），从而将 $x_2$ 表示为 $x_1$ 的函数，即 $x_2=h(x_1)$。然后把它代入 $f(x_1,x_2)$，得到只依赖于 $x_1$ 的函数 $f(x_1,h(x_1))$。接着用通常的求导方法，求它关于 $x_1$ 的最大值，得到驻点处的取值 $x_1^\star$，对应的 $x_2$ 值则由 $x_2^\star=h(x_1^\star)$ 给出。

这种方法的一个问题是，为了将 $x_2$ 写成 $x_1$ 的显式函数，需要求出约束方程的解析解，而这可能很难做到。另外，它对 $x_1$ 与 $x_2$ 作了不同的处理，破坏了这些变量之间原有的对称性。

一个更巧妙、而且通常更简单的方法，是引入一个称为拉格朗日乘子的参数 $\lambda$。下面从几何角度说明这种方法的由来。考虑一个 $D$ 维变量 $\mathbf{x}$，其分量为 $x_1,\ldots,x_D$。约束方程 $g(\mathbf{x})=0$ 表示 $\mathbf{x}$ 空间中的一个 $(D-1)$ 维曲面，如图 E.1 所示。

首先注意，在约束面上的任意一点，约束函数的梯度 $\nabla g(\mathbf{x})$ 都与曲面垂直。为说明这一点，考虑约束面上的一点 $\mathbf{x}$，以及其附近同样位于曲面上的一点 $\mathbf{x}+\boldsymbol{\epsilon}$。在 $\mathbf{x}$ 附近作泰勒展开，有

$$
g(\mathbf{x}+\boldsymbol{\epsilon})\simeq g(\mathbf{x})+\boldsymbol{\epsilon}^{\mathrm{T}}\nabla g(\mathbf{x}).
\tag{E.2}
$$

由于 $\mathbf{x}$ 与 $\mathbf{x}+\boldsymbol{\epsilon}$ 都位于约束面上，所以 $g(\mathbf{x})=g(\mathbf{x}+\boldsymbol{\epsilon})$，从而 $\boldsymbol{\epsilon}^{\mathrm{T}}\nabla g(\mathbf{x})\simeq0$。在极限 $\lVert\boldsymbol{\epsilon}\rVert\to0$ 下，有 $\boldsymbol{\epsilon}^{\mathrm{T}}\nabla g(\mathbf{x})=0$，而此时扰动向量 $\boldsymbol{\epsilon}$

<!-- pdf-page: 728 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/appendix-e/a-fig-E-1.png" alt="红色约束曲线上的点xA与方向相反的目标函数梯度、约束函数梯度"><figcaption>图 E.1：拉格朗日乘子法的几何解释：在约束 $g(\mathbf{x})=0$ 下，使函数 $f(\mathbf{x})$ 最大。如果 $\mathbf{x}$ 是 $D$ 维的，那么约束 $g(\mathbf{x})=0$ 就对应于一个 $D-1$ 维子空间，图中用红色曲线表示。通过优化拉格朗日函数 $L(\mathbf{x},\lambda)=f(\mathbf{x})+\lambda g(\mathbf{x})$，即可求解这个问题。</figcaption><p class="figure-translation">$\nabla f(\mathbf{x})$ → 目标函数的梯度；$\nabla g(\mathbf{x})$ → 约束函数的梯度；$\mathbf{x}_A$ → 约束面上的点；$g(\mathbf{x})=0$ → 约束面。</p></figure>

<!-- join-previous-paragraph-across-figures -->

与约束面 $g(\mathbf{x})=0$ 平行，因此向量 $\nabla g$ 是这个曲面的法向量。

接下来，我们要在约束面上寻找使 $f(\mathbf{x})$ 最大的点 $\mathbf{x}^\star$。在这样的点上，向量 $\nabla f(\mathbf{x})$ 也必须与约束面垂直，如图 E.1 所示；否则，只要沿约束面移动一小段距离，就可以增大 $f(\mathbf{x})$ 的值。因此，$\nabla f$ 与 $\nabla g$ 是同向或反向平行的向量，所以必定存在一个参数 $\lambda$，使得

$$
\nabla f+\lambda\nabla g=0
\tag{E.3}
$$

其中 $\lambda\neq0$ 称为拉格朗日乘子。注意，$\lambda$ 可以为正，也可以为负。

此时，引入如下定义的拉格朗日函数会很方便：

$$
L(\mathbf{x},\lambda)\equiv f(\mathbf{x})+\lambda g(\mathbf{x}).
\tag{E.4}
$$

令 $\nabla_{\mathbf{x}}L=0$，就得到有约束的驻点条件（E.3）。此外，条件 $\partial L/\partial\lambda=0$ 给出约束方程 $g(\mathbf{x})=0$。

因此，为了求函数 $f(\mathbf{x})$ 在约束 $g(\mathbf{x})=0$ 下的最大值，我们先定义式（E.4）给出的拉格朗日函数，然后同时对 $\mathbf{x}$ 和 $\lambda$ 求 $L(\mathbf{x},\lambda)$ 的驻点。对于 $D$ 维向量 $\mathbf{x}$，这会给出 $D+1$ 个方程，用来同时确定驻点 $\mathbf{x}^\star$ 以及 $\lambda$ 的值。如果只关心 $\mathbf{x}^\star$，就可以从驻点方程中消去 $\lambda$，而无须求出它的值，“未定乘子”一词也由此而来。

举一个简单例子：假设要在约束 $g(x_1,x_2)=x_1+x_2-1=0$ 下，求函数 $f(x_1,x_2)=1-x_1^2-x_2^2$ 的驻点，如图 E.2 所示。相应的拉格朗日函数为

$$
L(\mathbf{x},\lambda)=1-x_1^2-x_2^2+\lambda(x_1+x_2-1).
\tag{E.5}
$$

令这个拉格朗日函数对 $x_1$、$x_2$ 和 $\lambda$ 取驻值，就得到以下联立方程：

$$
-2x_1+\lambda=0
\tag{E.6}
$$

$$
-2x_2+\lambda=0
\tag{E.7}
$$

$$
x_1+x_2-1=0.
\tag{E.8}
$$

<!-- pdf-page: 729 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/appendix-e/b-fig-e-2.png" alt="蓝色圆形等高线与红色线性约束相切于最优点"><figcaption>图 E.2：使用拉格朗日乘子的一个简单例子，目标是在约束 $g(x_1,x_2)=0$ 下最大化 $f(x_1,x_2)=1-x_1^2-x_2^2$，其中 $g(x_1,x_2)=x_1+x_2-1$。圆表示函数 $f(x_1,x_2)$ 的等高线，斜线表示约束面 $g(x_1,x_2)=0$。</figcaption><p class="figure-translation">$x_1$、$x_2$：两个坐标分量；$(x_1^\star,x_2^\star)$：最优点；$g(x_1,x_2)=0$：红色约束线；蓝色圆：目标函数的等高线。</p></figure>

求解这些方程，得到驻点 $(x_1^\star,x_2^\star)=\left(\frac{1}{2},\frac{1}{2}\right)$，对应的拉格朗日乘子为 $\lambda=1$。

到目前为止，我们考虑的是在形如 $g(\mathbf{x})=0$ 的*等式约束*下最大化函数的问题。现在考虑在形如 $g(\mathbf{x})\geqslant0$ 的*不等式约束*下最大化 $f(\mathbf{x})$ 的问题，如图 E.3 所示。

现在可能出现两类解，取决于约束下的驻点是位于 $g(\mathbf{x})>0$ 的区域内，此时约束称为*不起作用的*（inactive）；还是位于边界 $g(\mathbf{x})=0$ 上，此时约束称为*起作用的*（active）。在前一种情形中，函数 $g(\mathbf{x})$ 不起作用，驻定条件就是 $\nabla f(\mathbf{x})=0$。这同样对应于拉格朗日函数（E.4）的一个驻点，但此时 $\lambda=0$。在后一种情形中，解位于边界上，这与前面讨论的等式约束类似，对应于拉格朗日函数（E.4）在 $\lambda\neq0$ 时的一个驻点。不过，此时拉格朗日乘子的符号至关重要，因为只有当函数 $f(\mathbf{x})$ 的梯度指向远离区域 $g(\mathbf{x})>0$ 的方向时，函数才处于极大值，如图 E.3 所示。因此，对于某个 $\lambda>0$，有 $\nabla f(\mathbf{x})=-\lambda\nabla g(\mathbf{x})$。

无论上述哪一种情形，都有乘积 $\lambda g(\mathbf{x})=0$。因此，要解决

<figure><img src="books/bishop-pattern-recognition-2006/assets/appendix-e/b-fig-e-3.png" alt="不等式约束区域及其边界驻点，目标函数与约束函数的梯度方向相反"><figcaption>图 E.3：在不等式约束 $g(\mathbf{x})\geqslant0$ 下最大化 $f(\mathbf{x})$ 的问题示意图。</figcaption><p class="figure-translation">$g(\mathbf{x})=0$：红色边界；$g(\mathbf{x})>0$：浅黄色内部区域；$\mathbf{x}_A$：边界上的点；$\mathbf{x}_B$：区域内的点；$\nabla f(\mathbf{x})$、$\nabla g(\mathbf{x})$：目标函数和约束函数的梯度。</p></figure>

<!-- pdf-page: 730 -->
<!-- join-previous-paragraph-across-figures -->
在约束 $g(\mathbf{x})\geqslant0$ 下最大化 $f(\mathbf{x})$ 的问题，可以在下列条件下，关于 $\mathbf{x}$ 和 $\lambda$ 优化拉格朗日函数（E.4）：

$$
g(\mathbf{x})\geqslant0
\tag{E.9}
$$

$$
\lambda\geqslant0
\tag{E.10}
$$

$$
\lambda g(\mathbf{x})=0
\tag{E.11}
$$

这些条件称为 *Karush–Kuhn–Tucker（KKT）条件*（Karush，1939；Kuhn and Tucker，1951）。

注意，如果我们希望在不等式约束 $g(\mathbf{x})\geqslant0$ 下最小化（而不是最大化）函数 $f(\mathbf{x})$，那么就要关于 $\mathbf{x}$ 最小化拉格朗日函数 $L(\mathbf{x},\lambda)=f(\mathbf{x})-\lambda g(\mathbf{x})$，同样要求 $\lambda\geqslant0$。

最后，拉格朗日乘子方法可以直接推广到多个等式约束和不等式约束的情形。假设我们希望最大化 $f(\mathbf{x})$，约束为 $g_j(\mathbf{x})=0$，其中 $j=1,\ldots,J$，以及 $h_k(\mathbf{x})\geqslant0$，其中 $k=1,\ldots,K$。于是引入拉格朗日乘子 $\{\lambda_j\}$ 和 $\{\mu_k\}$，再优化如下拉格朗日函数

$$
L(\mathbf{x},\{\lambda_j\},\{\mu_k\})=f(\mathbf{x})+\sum_{j=1}^{J}\lambda_jg_j(\mathbf{x})+\sum_{k=1}^{K}\mu_kh_k(\mathbf{x})
\tag{E.12}
$$

所满足的约束为 $\mu_k\geqslant0$ 以及 $\mu_kh_k(\mathbf{x})=0$，其中 $k=1,\ldots,K$。推广到带约束的泛函导数也同样直接。<span class="margin-reference">附录 D</span>关于拉格朗日乘子方法更详细的讨论，参见 Nocedal and Wright（1999）。
