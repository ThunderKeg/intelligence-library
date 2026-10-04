<!-- pdf-page: 719 -->

其中 $i=1,\ldots,M$，$\mathbf{u}_i$ 是一个*特征向量*，$\lambda_i$ 是对应的*特征值*。这可以看作由 $M$ 个齐次线性方程组成的方程组，其有解的条件是

$$
|\mathbf{A}-\lambda_i\mathbf{I}|=0
\tag{C.30}
$$

这称为*特征方程*。由于它是关于 $\lambda_i$ 的 $M$ 次多项式，所以必定有 $M$ 个解（尽管这些解不一定各不相同）。$\mathbf{A}$ 的秩等于非零特征值的个数。

我们特别关心对称矩阵，协方差矩阵、核矩阵和 Hessian 矩阵都是其例子。对称矩阵具有性质 $A_{ij}=A_{ji}$，等价地，$\mathbf{A}^{\mathrm{T}}=\mathbf{A}$。对称矩阵的逆也对称：对 $\mathbf{A}^{-1}\mathbf{A}=\mathbf{I}$ 取转置，再利用 $\mathbf{A}\mathbf{A}^{-1}=\mathbf{I}$ 和 $\mathbf{I}$ 的对称性，就可以看出这一点。

一般来说，矩阵的特征值是复数，但对称矩阵的特征值 $\lambda_i$ 是实数。为说明这一点，首先将式（C.29）左乘 $(\mathbf{u}_i^\star)^{\mathrm{T}}$，其中 $\star$ 表示复共轭，得到

$$
(\mathbf{u}_i^\star)^{\mathrm{T}}\mathbf{A}\mathbf{u}_i=\lambda_i(\mathbf{u}_i^\star)^{\mathrm{T}}\mathbf{u}_i.
\tag{C.31}
$$

接下来，对式（C.29）取复共轭，再左乘 $\mathbf{u}_i^{\mathrm{T}}$，得到

$$
\mathbf{u}_i^{\mathrm{T}}\mathbf{A}\mathbf{u}_i^\star=\lambda_i^\star\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_i^\star.
\tag{C.32}
$$

这里使用了 $\mathbf{A}^\star=\mathbf{A}$，因为我们只考虑实矩阵 $\mathbf{A}$。对这两个方程中的第二个取转置，再利用 $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$，可见两式左侧相等，因此 $\lambda_i^\star=\lambda_i$，所以 $\lambda_i$ 必须为实数。

实对称矩阵的特征向量 $\mathbf{u}_i$ 可以选为标准正交的（即相互正交且长度为一），使得

$$
\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_j=I_{ij}
\tag{C.33}
$$

其中，$I_{ij}$ 是单位矩阵 $\mathbf{I}$ 的元素。为证明这一点，首先将式（C.29）左乘 $\mathbf{u}_j^{\mathrm{T}}$，得到

$$
\mathbf{u}_j^{\mathrm{T}}\mathbf{A}\mathbf{u}_i=\lambda_i\mathbf{u}_j^{\mathrm{T}}\mathbf{u}_i
\tag{C.34}
$$

于是，交换下标便得到

$$
\mathbf{u}_i^{\mathrm{T}}\mathbf{A}\mathbf{u}_j=\lambda_j\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_j.
\tag{C.35}
$$

现在，对第二个方程取转置，利用对称性 $\mathbf{A}^{\mathrm{T}}=\mathbf{A}$，再将两个方程相减，得到

$$
(\lambda_i-\lambda_j)\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_j=0.
\tag{C.36}
$$

因此，当 $\lambda_i\neq\lambda_j$ 时，有 $\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_j=0$，所以 $\mathbf{u}_i$ 和 $\mathbf{u}_j$ 正交。如果两个特征值相等，那么任意线性组合 $\alpha\mathbf{u}_i+\beta\mathbf{u}_j$ 也都是对应于同一特征值的特征向量，因此我们可以任意选取一个线性组合，

<!-- pdf-page: 720 -->
<!-- join-previous-paragraph -->
再选择第二个，使其与第一个正交（可以证明，简并特征向量不会线性相关）。因此，可以选取相互正交的特征向量，再通过归一化使其长度为一。由于有 $M$ 个特征值，对应的 $M$ 个正交特征向量便构成一个完备集，所以任意 $M$ 维向量都可以表示为这些特征向量的线性组合。

我们可以用特征向量 $\mathbf{u}_i$ 作为一个 $M\times M$ 矩阵 $\mathbf{U}$ 的各列。由标准正交性，它满足

$$
\mathbf{U}^{\mathrm{T}}\mathbf{U}=\mathbf{I}.
\tag{C.37}
$$

这样的矩阵称为*正交矩阵*。有趣的是，该矩阵的各行也相互正交，所以 $\mathbf{U}\mathbf{U}^{\mathrm{T}}=\mathbf{I}$。为证明这一点，注意式（C.37）意味着 $\mathbf{U}^{\mathrm{T}}\mathbf{U}\mathbf{U}^{-1}=\mathbf{U}^{-1}=\mathbf{U}^{\mathrm{T}}$，所以 $\mathbf{U}\mathbf{U}^{-1}=\mathbf{U}\mathbf{U}^{\mathrm{T}}=\mathbf{I}$。利用式（C.12），还可得 $|\mathbf{U}|=1$。

特征向量方程（C.29）可以用 $\mathbf{U}$ 表示为

$$
\mathbf{A}\mathbf{U}=\mathbf{U}\boldsymbol{\Lambda}
\tag{C.38}
$$

其中，$\boldsymbol{\Lambda}$ 是一个 $M\times M$ 对角矩阵，对角元素由特征值 $\lambda_i$ 给出。

考虑列向量 $\mathbf{x}$，用正交矩阵 $\mathbf{U}$ 对它作变换，得到新的向量

$$
\widetilde{\mathbf{x}}=\mathbf{U}\mathbf{x}
\tag{C.39}
$$

则向量的长度保持不变，因为

$$
\widetilde{\mathbf{x}}^{\mathrm{T}}\widetilde{\mathbf{x}}=\mathbf{x}^{\mathrm{T}}\mathbf{U}^{\mathrm{T}}\mathbf{U}\mathbf{x}=\mathbf{x}^{\mathrm{T}}\mathbf{x}
\tag{C.40}
$$

类似地，任意两个这样变换后的向量之间的夹角也保持不变，因为

$$
\widetilde{\mathbf{x}}^{\mathrm{T}}\widetilde{\mathbf{y}}=\mathbf{x}^{\mathrm{T}}\mathbf{U}^{\mathrm{T}}\mathbf{U}\mathbf{y}=\mathbf{x}^{\mathrm{T}}\mathbf{y}.
\tag{C.41}
$$

因此，乘以 $\mathbf{U}$ 可以解释为对坐标系作刚性旋转。

由式（C.38）可得

$$
\mathbf{U}^{\mathrm{T}}\mathbf{A}\mathbf{U}=\boldsymbol{\Lambda}
\tag{C.42}
$$

由于 $\boldsymbol{\Lambda}$ 是对角矩阵，我们就说矩阵 $\mathbf{A}$ 被矩阵 $\mathbf{U}$ *对角化*了。如果左乘 $\mathbf{U}$，再右乘 $\mathbf{U}^{\mathrm{T}}$，就得到

$$
\mathbf{A}=\mathbf{U}\boldsymbol{\Lambda}\mathbf{U}^{\mathrm{T}}
\tag{C.43}
$$

对这个方程取逆，再利用式（C.3）以及 $\mathbf{U}^{-1}=\mathbf{U}^{\mathrm{T}}$，有

$$
\mathbf{A}^{-1}=\mathbf{U}\boldsymbol{\Lambda}^{-1}\mathbf{U}^{\mathrm{T}}.
\tag{C.44}
$$

<!-- pdf-page: 721 -->

最后这两个方程也可以写成

$$
\mathbf{A}=\sum_{i=1}^{M}\lambda_i\mathbf{u}_i\mathbf{u}_i^{\mathrm{T}}
\tag{C.45}
$$

$$
\mathbf{A}^{-1}=\sum_{i=1}^{M}\frac{1}{\lambda_i}\mathbf{u}_i\mathbf{u}_i^{\mathrm{T}}.
\tag{C.46}
$$

对式（C.43）取行列式，并利用式（C.12），得到

$$
|\mathbf{A}|=\prod_{i=1}^{M}\lambda_i.
\tag{C.47}
$$

类似地，对式（C.43）取迹，并利用迹运算的循环性质（C.8）以及 $\mathbf{U}^{\mathrm{T}}\mathbf{U}=\mathbf{I}$，有

$$
\operatorname{Tr}(\mathbf{A})=\sum_{i=1}^{M}\lambda_i.
\tag{C.48}
$$

利用式（C.33）、（C.45）、（C.46）和（C.47）的结果来验证式（C.22），留作读者的练习。

如果对向量 $\mathbf{w}$ 的所有取值都有 $\mathbf{w}^{\mathrm{T}}\mathbf{A}\mathbf{w}>0$，就称矩阵 $\mathbf{A}$ 为*正定矩阵*，记为 $\mathbf{A}\succ0$。等价地，正定矩阵的所有特征值都满足 $\lambda_i>0$（依次令 $\mathbf{w}$ 取各个特征向量，并注意任意向量都可以展开为这些特征向量的线性组合，即可看出这一点）。注意，正定与所有元素均为正并不是一回事。例如，矩阵

$$
\begin{pmatrix}
1 & 2\\
3 & 4
\end{pmatrix}
\tag{C.49}
$$

的特征值为 $\lambda_1\simeq5.37$ 和 $\lambda_2\simeq-0.37$。如果对 $\mathbf{w}$ 的所有取值都有 $\mathbf{w}^{\mathrm{T}}\mathbf{A}\mathbf{w}\geqslant0$，就称矩阵为*半正定矩阵*，记为 $\mathbf{A}\succeq0$，这等价于 $\lambda_i\geqslant0$。

<!-- pdf-page: 722 -->
