# 附录 C 矩阵的性质

<aside class="chapter-guide"><strong>附录导读</strong><p>本附录供线性代数公式查阅，重点是矩阵运算顺序、维度与转置。遇到涉及矩阵求导或特征分解的推导时，可在这里核对所用恒等式及其条件。</p></aside>

<!-- pdf-page: 715 -->

本附录汇集了一些涉及矩阵和行列式的有用性质与恒等式。这里并不是入门教程，假定读者已经熟悉基本线性代数。对于一些结果，我们会说明如何证明；对于较复杂的情况，则请感兴趣的读者查阅相关标准教材。在所有情况下，我们都假设逆矩阵存在，而且矩阵的维度使公式中的各项都有定义。关于线性代数的全面讨论，可参阅 Golub 和 Van Loan（1996）；Lütkepohl（1996）汇集了大量矩阵性质。关于矩阵导数的讨论，可参阅 Magnus 和 Neudecker（1999）。

## 基本矩阵恒等式

矩阵 $\mathbf{A}$ 的元素记作 $A_{ij}$，其中 $i$ 是行下标，$j$ 是列下标。我们用 $\mathbf{I}_N$ 表示 $N\times N$ 的单位矩阵（identity matrix，也称 unit matrix）；在维度不会产生歧义时，简记为 $\mathbf{I}$。转置矩阵 $\mathbf{A}^{\mathrm{T}}$ 的元素为 $(\mathbf{A}^{\mathrm{T}})_{ij}=A_{ji}$。由转置的定义，有

$$
(\mathbf{A}\mathbf{B})^{\mathrm{T}}=\mathbf{B}^{\mathrm{T}}\mathbf{A}^{\mathrm{T}}
\tag{C.1}
$$

用带下标的分量写出两边，即可验证这个等式。$\mathbf{A}$ 的逆记作 $\mathbf{A}^{-1}$，满足

$$
\mathbf{A}\mathbf{A}^{-1}=\mathbf{A}^{-1}\mathbf{A}=\mathbf{I}.
\tag{C.2}
$$

由于 $\mathbf{A}\mathbf{B}\mathbf{B}^{-1}\mathbf{A}^{-1}=\mathbf{I}$，所以有

$$
(\mathbf{A}\mathbf{B})^{-1}=\mathbf{B}^{-1}\mathbf{A}^{-1}.
\tag{C.3}
$$

另外，还有

$$
\left(\mathbf{A}^{\mathrm{T}}\right)^{-1}=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
\tag{C.4}
$$

<!-- pdf-page: 716 -->

对式（C.2）取转置，再应用式（C.1），就很容易证明这个等式。

下面是一条关于矩阵逆的有用恒等式：

$$
(\mathbf{P}^{-1}+\mathbf{B}^{\mathrm{T}}\mathbf{R}^{-1}\mathbf{B})^{-1}\mathbf{B}^{\mathrm{T}}\mathbf{R}^{-1}=\mathbf{P}\mathbf{B}^{\mathrm{T}}(\mathbf{B}\mathbf{P}\mathbf{B}^{\mathrm{T}}+\mathbf{R})^{-1}.
\tag{C.5}
$$

在两边右乘 $(\mathbf{B}\mathbf{P}\mathbf{B}^{\mathrm{T}}+\mathbf{R})$，即可很容易地验证它。假设 $\mathbf{P}$ 的维度是 $N\times N$，而 $\mathbf{R}$ 的维度是 $M\times M$，那么 $\mathbf{B}$ 就是 $M\times N$ 矩阵。当 $M\ll N$ 时，计算式（C.5）右边的代价会远低于计算左边。有时会遇到如下特例：

$$
(\mathbf{I}+\mathbf{A}\mathbf{B})^{-1}\mathbf{A}=\mathbf{A}(\mathbf{I}+\mathbf{B}\mathbf{A})^{-1}.
\tag{C.6}
$$

另一条关于矩阵逆的有用恒等式是

$$
(\mathbf{A}+\mathbf{B}\mathbf{D}^{-1}\mathbf{C})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{B}(\mathbf{D}+\mathbf{C}\mathbf{A}^{-1}\mathbf{B})^{-1}\mathbf{C}\mathbf{A}^{-1}
\tag{C.7}
$$

它称为 Woodbury 恒等式，在两边乘以 $(\mathbf{A}+\mathbf{B}\mathbf{D}^{-1}\mathbf{C})$ 就可以验证。例如，当 $\mathbf{A}$ 是一个大型对角矩阵、因而容易求逆，而 $\mathbf{B}$ 的行数很多但列数很少，$\mathbf{C}$ 则相反时，这个恒等式就很有用，因为此时计算右边的代价远低于计算左边。

对于一组向量 $\{\mathbf{a}_1,\ldots,\mathbf{a}_N\}$，如果关系 $\sum_n\alpha_n\mathbf{a}_n=0$ 只有在所有 $\alpha_n=0$ 时才成立，就称这组向量线性无关。这意味着其中没有任何向量能够表示为其余向量的线性组合。矩阵的秩是其线性无关行的最大数目，等价地，也是其线性无关列的最大数目。

## 迹与行列式

迹和行列式适用于方阵。矩阵 $\mathbf{A}$ 的迹 $\operatorname{Tr}(\mathbf{A})$ 定义为主对角线上元素的和。写出各分量的下标，可以得到

$$
\operatorname{Tr}(\mathbf{A}\mathbf{B})=\operatorname{Tr}(\mathbf{B}\mathbf{A}).
\tag{C.8}
$$

对三个矩阵的乘积多次应用这个公式，可得

$$
\operatorname{Tr}(\mathbf{A}\mathbf{B}\mathbf{C})=\operatorname{Tr}(\mathbf{C}\mathbf{A}\mathbf{B})=\operatorname{Tr}(\mathbf{B}\mathbf{C}\mathbf{A})
\tag{C.9}
$$

这称为迹运算的循环性质，显然也适用于任意多个矩阵的乘积。$N\times N$ 矩阵 $\mathbf{A}$ 的行列式 $|\mathbf{A}|$ 定义为

$$
|\mathbf{A}|=\sum(\pm1)A_{1i_1}A_{2i_2}\cdots A_{Ni_N}
\tag{C.10}
$$

其中的求和遍历所有乘积，每个乘积恰好从每一行、每一列各取一个元素；其系数为 $+1$ 或 $-1$，分别对应于

<!-- pdf-page: 717 -->
<!-- join-previous-paragraph -->

排列 $i_1i_2\ldots i_N$ 为偶排列或奇排列。注意，$|\mathbf{I}|=1$。因此，对于 $2\times2$ 矩阵，行列式为

$$
|\mathbf{A}|=\begin{vmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{vmatrix}=a_{11}a_{22}-a_{12}a_{21}.
\tag{C.11}
$$

两个矩阵乘积的行列式为

$$
|\mathbf{A}\mathbf{B}|=|\mathbf{A}||\mathbf{B}|
\tag{C.12}
$$

这可以由式（C.10）证明。另外，逆矩阵的行列式为

$$
\left|\mathbf{A}^{-1}\right|=\frac{1}{|\mathbf{A}|}
\tag{C.13}
$$

对式（C.2）两边取行列式，再应用式（C.12），就能证明这个等式。

如果 $\mathbf{A}$ 和 $\mathbf{B}$ 都是 $N\times M$ 矩阵，那么

$$
\left|\mathbf{I}_N+\mathbf{A}\mathbf{B}^{\mathrm{T}}\right|=\left|\mathbf{I}_M+\mathbf{A}^{\mathrm{T}}\mathbf{B}\right|.
\tag{C.14}
$$

一个有用的特例是

$$
\left|\mathbf{I}_N+\mathbf{a}\mathbf{b}^{\mathrm{T}}\right|=1+\mathbf{a}^{\mathrm{T}}\mathbf{b}
\tag{C.15}
$$

其中 $\mathbf{a}$ 和 $\mathbf{b}$ 是 $N$ 维列向量。

## 矩阵导数

有时需要考虑向量和矩阵对标量的导数。向量 $\mathbf{a}$ 对标量 $x$ 的导数本身是一个向量，其分量为

$$
\left(\frac{\partial\mathbf{a}}{\partial x}\right)_i=\frac{\partial a_i}{\partial x}
\tag{C.16}
$$

矩阵的导数也有类似定义。还可以定义对向量和矩阵的导数，例如

$$
\left(\frac{\partial x}{\partial\mathbf{a}}\right)_i=\frac{\partial x}{\partial a_i}
\tag{C.17}
$$

类似地，有

$$
\left(\frac{\partial\mathbf{a}}{\partial\mathbf{b}}\right)_{ij}=\frac{\partial a_i}{\partial b_j}.
\tag{C.18}
$$

写出各个分量，就很容易证明下面的关系：

$$
\frac{\partial}{\partial\mathbf{x}}(\mathbf{x}^{\mathrm{T}}\mathbf{a})=\frac{\partial}{\partial\mathbf{x}}(\mathbf{a}^{\mathrm{T}}\mathbf{x})=\mathbf{a}.
\tag{C.19}
$$

<!-- pdf-page: 718 -->

类似地，

$$
\frac{\partial}{\partial\mathbf{x}}(\mathbf{A}\mathbf{B})=\frac{\partial\mathbf{A}}{\partial\mathbf{x}}\mathbf{B}+\mathbf{A}\frac{\partial\mathbf{B}}{\partial\mathbf{x}}.
\tag{C.20}
$$

矩阵逆的导数可以表示为

$$
\frac{\partial}{\partial x}(\mathbf{A}^{-1})=-\mathbf{A}^{-1}\frac{\partial\mathbf{A}}{\partial x}\mathbf{A}^{-1}
\tag{C.21}
$$

利用式（C.20）对等式 $\mathbf{A}^{-1}\mathbf{A}=\mathbf{I}$ 求导，然后在等式两边右乘 $\mathbf{A}^{-1}$，即可证明这个结果。另外，还有

$$
\frac{\partial}{\partial x}\ln|\mathbf{A}|=\operatorname{Tr}\left(\mathbf{A}^{-1}\frac{\partial\mathbf{A}}{\partial x}\right)
\tag{C.22}
$$

我们稍后会证明它。如果选择 $x$ 为 $\mathbf{A}$ 中的某个元素，那么

$$
\frac{\partial}{\partial A_{ij}}\operatorname{Tr}(\mathbf{A}\mathbf{B})=B_{ji}
\tag{C.23}
$$

用带下标的分量写出矩阵，即可看出这个结果。它可以更紧凑地写成

$$
\frac{\partial}{\partial\mathbf{A}}\operatorname{Tr}(\mathbf{A}\mathbf{B})=\mathbf{B}^{\mathrm{T}}.
\tag{C.24}
$$

采用这种记法，有如下性质：

$$
\frac{\partial}{\partial\mathbf{A}}\operatorname{Tr}(\mathbf{A}^{\mathrm{T}}\mathbf{B})=\mathbf{B}
\tag{C.25}
$$

$$
\frac{\partial}{\partial\mathbf{A}}\operatorname{Tr}(\mathbf{A})=\mathbf{I}
\tag{C.26}
$$

$$
\frac{\partial}{\partial\mathbf{A}}\operatorname{Tr}(\mathbf{A}\mathbf{B}\mathbf{A}^{\mathrm{T}})=\mathbf{A}(\mathbf{B}+\mathbf{B}^{\mathrm{T}})
\tag{C.27}
$$

同样，写出矩阵的分量下标就能证明这些关系。我们还有

$$
\frac{\partial}{\partial\mathbf{A}}\ln|\mathbf{A}|=\left(\mathbf{A}^{-1}\right)^{\mathrm{T}}
\tag{C.28}
$$

这由式（C.22）和式（C.26）得到。

## 特征向量方程

对于一个 $M\times M$ 的方阵 $\mathbf{A}$，特征向量方程定义为

$$
\mathbf{A}\mathbf{u}_i=\lambda_i\mathbf{u}_i
\tag{C.29}
$$

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
