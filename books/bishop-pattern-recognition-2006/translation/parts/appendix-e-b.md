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
