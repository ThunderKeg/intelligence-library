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
