<!-- pdf-page: 628 -->

# 附录 C 拉格朗日乘子

<aside class="chapter-guide"><strong>本附录导读</strong><p>本附录用几何图像解释拉格朗日乘子，随后给出等式约束、不等式约束和多个约束下的驻点条件。</p></aside>

**拉格朗日乘子**（Lagrange multiplier）有时也称为**待定乘子**（undetermined multiplier），用于寻找多变量函数在一个或多个约束条件下的驻点。

考虑求函数 $f(x_1,x_2)$ 的最大值，同时要求 $x_1$ 和 $x_2$ 满足一个约束，写为

$$
g(x_1,x_2)=0. \tag{C.1}
$$

一种办法是求解约束方程 (C.1)，把 $x_2$ 表示为 $x_1$ 的函数 $x_2=h(x_1)$。再代入 $f(x_1,x_2)$，得到只依赖于 $x_1$ 的函数 $f(x_1,h(x_1))$。随后按通常的方法求导，找到关于 $x_1$ 的最大值所对应的驻点 $x_1^\star$；相应的 $x_2$ 为 $x_2^\star=h(x_1^\star)$。

这一办法的一个困难是，未必容易解析地求解约束方程，把 $x_2$ 显式地写成 $x_1$ 的函数。此外，它对 $x_1$ 和 $x_2$ 采取不同处理方式，破坏了两个变量之间自然的对称性。

一种更优雅、通常也更简单的办法，是引入一个称为拉格朗日乘子的参数 $\lambda$。下面从几何角度说明这种方法。考虑一个 $D$ 维变量 $\mathbf x$，它的分量为 $x_1,\ldots,x_D$。如图 C.1 所示，约束方程 $g(\mathbf x)=0$ 在 $\mathbf x$ 空间中表示一个 $D-1$ 维曲面。

首先，约束曲面上任意一点处，约束函数的梯度 $\nabla g(\mathbf x)$ 都与该曲面正交。为理解这一点，考虑曲面上的一个点 $\mathbf x$，以及同样位于曲面上的邻近点 $\mathbf x+\boldsymbol\epsilon$。在 $\mathbf x$ 附近作 Taylor 展开，得到

$$
g(\mathbf x+\boldsymbol\epsilon)\simeq g(\mathbf x)+\boldsymbol\epsilon^{\mathsf T}\nabla g(\mathbf x). \tag{C.2}
$$

因为 $\mathbf x$ 和 $\mathbf x+\boldsymbol\epsilon$ 都位于约束曲面上，$g(\mathbf x)=g(\mathbf x+\boldsymbol\epsilon)$，所以 $\boldsymbol\epsilon^{\mathsf T}\nabla g(\mathbf x)\simeq0$。在 $\lVert\boldsymbol\epsilon\rVert\to0$ 的极限下，$\boldsymbol\epsilon^{\mathsf T}\nabla g(\mathbf x)=0$。又因为 $\boldsymbol\epsilon$

<!-- pdf-page: 629 -->
<!-- join-previous-paragraph -->

与约束曲面 $g(\mathbf x)=0$ 平行，所以向量 $\nabla g$ 是曲面的法向量。

<figure id="fig-c-1">
  <img src="books/bishop-deep-learning-2024/assets/appendix-c/fig-c-1.png" alt="红色约束曲面 g(x)=0 上的点 x_A，梯度 ∇g 垂直曲面，∇f 与其反向平行">
  <figcaption>图 C.1：拉格朗日乘子法的几何图像：在约束 $g(\mathbf x)=0$ 下使函数 $f(\mathbf x)$ 最大。如果 $\mathbf x$ 为 $D$ 维，约束 $g(\mathbf x)=0$ 对应一个 $D-1$ 维子空间，图中的红色曲线表示它。这个问题可以通过优化拉格朗日函数 $L(\mathbf x,\lambda)=f(\mathbf x)+\lambda g(\mathbf x)$ 来求解。</figcaption>
  <p class="figure-translation">图内符号：$\nabla f(\mathbf x)$ 为目标函数的梯度；$\nabla g(\mathbf x)$ 为约束函数的梯度；$\mathbf x_A$ 为约束曲面上的点；红色边界表示 $g(\mathbf x)=0$。</p>
</figure>

现在要在约束曲面上找到一个点 $\mathbf x^\star$，使 $f(\mathbf x)$ 最大。如图 C.1 所示，在该点，向量 $\nabla f(\mathbf x)$ 也必须与约束曲面正交；否则，沿曲面移动一小段距离就可以增大 $f(\mathbf x)$。因此，$\nabla f$ 与 $\nabla g$ 平行或反向平行，所以必存在一个参数 $\lambda$，使得

$$
\nabla f+\lambda\nabla g=0, \tag{C.3}
$$

其中 $\lambda\ne0$ 称为拉格朗日乘子。注意，$\lambda$ 可以为正，也可以为负。

现在定义**拉格朗日函数**（Lagrangian）

$$
L(\mathbf x,\lambda)\equiv f(\mathbf x)+\lambda g(\mathbf x). \tag{C.4}
$$

令 $\nabla_{\mathbf x}L=0$，就得到约束下的驻点条件 (C.3)。此外，条件 $\partial L/\partial\lambda=0$ 给出约束方程 $g(\mathbf x)=0$。

因此，若要在约束 $g(\mathbf x)=0$ 下求 $f(\mathbf x)$ 的最大值，可先按式 (C.4) 定义拉格朗日函数，再同时对 $\mathbf x$ 和 $\lambda$ 求 $L(\mathbf x,\lambda)$ 的驻点。对于 $D$ 维向量 $\mathbf x$，这给出 $D+1$ 个方程，用来确定驻点 $\mathbf x^\star$ 和 $\lambda$ 的值。如果只关心 $\mathbf x^\star$，就可以从驻点方程中消去 $\lambda$，无需求出它的值；“待定乘子”一名也由此而来。

举一个简单例子：在约束 $g(x_1,x_2)=x_1+x_2-1=0$ 下，求函数 $f(x_1,x_2)=1-x_1^2-x_2^2$ 的驻点，如图 C.2 所示。相应的拉格朗日函数是

$$
L(\mathbf x,\lambda)=1-x_1^2-x_2^2+\lambda(x_1+x_2-1). \tag{C.5}
$$

分别对 $x_1$、$x_2$ 和 $\lambda$ 令该函数处于驻点，得到以下联立方程：

$$
-2x_1+\lambda=0, \tag{C.6}
$$

$$
-2x_2+\lambda=0, \tag{C.7}
$$

$$
x_1+x_2-1=0. \tag{C.8}
$$

<!-- pdf-page: 630 -->

<figure id="fig-c-2">
  <img src="books/bishop-deep-learning-2024/assets/appendix-c/fig-c-2.png" alt="函数 f 的同心圆等值线与约束直线 g(x1,x2)=0 在最优点相切">
  <figcaption>图 C.2：拉格朗日乘子的一个简单应用：在约束 $g(x_1,x_2)=0$ 下最大化 $f(x_1,x_2)=1-x_1^2-x_2^2$，其中 $g(x_1,x_2)=x_1+x_2-1$。圆表示函数 $f(x_1,x_2)$ 的等值线，对角线表示约束曲面 $g(x_1,x_2)=0$。</figcaption>
  <p class="figure-translation">图内符号：$x_1$、$x_2$ 为坐标轴；$(x_1^\star,x_2^\star)$ 为约束下的驻点；红色直线表示 $g(x_1,x_2)=0$。</p>
</figure>

解这些方程，得到驻点 $(x_1^\star,x_2^\star)=(1/2,1/2)$，对应的拉格朗日乘子为 $\lambda=1$。

到目前为止，讨论的都是在等式约束 $g(\mathbf x)=0$ 下最大化函数的问题。现在考虑在不等式约束 $g(\mathbf x)\geqslant0$ 下最大化 $f(\mathbf x)$，如图 C.3 所示。

此时可能有两类解：约束下的驻点位于 $g(\mathbf x)>0$ 的区域内，约束因而是**非活跃的**（inactive）；或者驻点位于边界 $g(\mathbf x)=0$ 上，约束因而是**活跃的**（active）。前一种情况下，函数 $g(\mathbf x)$ 不起作用，驻点条件只是 $\nabla f(\mathbf x)=0$。它仍然是拉格朗日函数 (C.4) 的驻点，不过此时 $\lambda=0$。后一种情况下，解位于边界上，情形类似前面讨论的等式约束，对应 $\lambda\ne0$ 时拉格朗日函数 (C.4) 的驻点。但现在乘子的符号至关重要：只有当 $f(\mathbf x)$ 的梯度指向远离 $g(\mathbf x)>0$ 区域的方向时，$f(\mathbf x)$ 才取最大值，如图 C.3 所示。因此，对某个 $\lambda>0$，有 $\nabla f(\mathbf x)=-\lambda\nabla g(\mathbf x)$。

<figure id="fig-c-3">
  <img src="books/bishop-deep-learning-2024/assets/appendix-c/fig-c-3.png" alt="红色边界 g(x)=0 内为满足 g(x)>0 的区域，图示边界点 x_A 与内部点 x_B 的不等式约束极值情形">
  <figcaption>图 C.3：在不等式约束 $g(\mathbf x)\geqslant0$ 下最大化 $f(\mathbf x)$ 的问题示意图。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf x_A$ 为边界上的点；$\mathbf x_B$ 为区域内的点；$\nabla f(\mathbf x)$ 和 $\nabla g(\mathbf x)$ 分别为目标函数与约束函数的梯度；红色边界为 $g(\mathbf x)=0$；着色区域满足 $g(\mathbf x)>0$。</p>
</figure>

对于这两类解，都有 $\lambda g(\mathbf x)=0$。因此，在约束 $g(\mathbf x)\geqslant0$ 下最大化 $f(\mathbf x)$ 的解，可以通过

<!-- pdf-page: 631 -->
<!-- join-previous-paragraph -->

对 $\mathbf x$ 和 $\lambda$ 优化式 (C.4) 的拉格朗日函数求得，同时满足以下条件：

$$
g(\mathbf x)\geqslant0, \tag{C.9}
$$

$$
\lambda\geqslant0, \tag{C.10}
$$

$$
\lambda g(\mathbf x)=0. \tag{C.11}
$$

这些条件称为 **Karush–Kuhn–Tucker 条件**（KKT 条件；Karush，1939；Kuhn 和 Tucker，1951）。

注意，如果要在不等式约束 $g(\mathbf x)\geqslant0$ 下**最小化**而不是最大化 $f(\mathbf x)$，则应对 $\mathbf x$ 最小化拉格朗日函数 $L(\mathbf x,\lambda)=f(\mathbf x)-\lambda g(\mathbf x)$，并且仍要求 $\lambda\geqslant0$。

最后，拉格朗日乘子法很容易推广到有多个等式约束和不等式约束的情形。设在 $j=1,\ldots,J$ 时有 $g_j(\mathbf x)=0$，在 $k=1,\ldots,K$ 时有 $h_k(\mathbf x)\geqslant0$，我们希望最大化 $f(\mathbf x)$。引入乘子 $\{\lambda_j\}$ 和 $\{\mu_k\}$，然后优化拉格朗日函数

$$
L(\mathbf x,\{\lambda_j\},\{\mu_k\})
=f(\mathbf x)+\sum_{j=1}^{J}\lambda_j g_j(\mathbf x)
+\sum_{k=1}^{K}\mu_k h_k(\mathbf x), \tag{C.12}
$$

并对 $k=1,\ldots,K$ 满足 $\mu_k\geqslant0$ 和 $\mu_k h_k(\mathbf x)=0$。受约束的泛函导数也可作类似推广（见附录 B）。关于拉格朗日乘子法的更详细讨论，见 Nocedal 和 Wright（1999）。
