<!-- pdf-page: 618 -->

# 附录 A 线性代数

<aside class="chapter-guide"><strong>本附录导读</strong><p>本附录汇集矩阵恒等式、行列式、矩阵求导和特征向量的常用结果，供正文推导时查阅。</p></aside>

本附录汇集了关于矩阵和行列式的一些有用性质与恒等式。它并非线性代数入门教程，假定读者已经熟悉基本线性代数。对于部分结果，我们会说明如何证明；较复杂的情形则请有兴趣的读者参考标准教材。全文假定所用逆矩阵存在，且矩阵维度使各式均有定义。线性代数的全面讨论可见 Golub 和 Van Loan（1996），Lütkepohl（1996）汇集了大量矩阵性质，矩阵导数则见 Magnus 和 Neudecker（1999）。

## A.1 矩阵恒等式

矩阵 $\mathbf A$ 的元素为 $A_{ij}$，其中 $i$ 标记行，$j$ 标记列。用 $\mathbf I_N$ 表示 $N\times N$ 单位矩阵；如果维度没有歧义，就简写为 $\mathbf I$。转置矩阵 $\mathbf A^{\mathsf T}$ 的元素满足 $(\mathbf A^{\mathsf T})_{ij}=A_{ji}$。根据转置的定义，有

$$
(\mathbf A\mathbf B)^{\mathsf T}=\mathbf B^{\mathsf T}\mathbf A^{\mathsf T}. \tag{A.1}
$$

把指标展开即可验证。记 $\mathbf A$ 的逆为 $\mathbf A^{-1}$，它满足

$$
\mathbf A\mathbf A^{-1}=\mathbf A^{-1}\mathbf A=\mathbf I. \tag{A.2}
$$

因为 $\mathbf A\mathbf B\mathbf B^{-1}\mathbf A^{-1}=\mathbf I$，所以

$$
(\mathbf A\mathbf B)^{-1}=\mathbf B^{-1}\mathbf A^{-1}. \tag{A.3}
$$

此外还有

$$
(\mathbf A^{\mathsf T})^{-1}=(\mathbf A^{-1})^{\mathsf T}, \tag{A.4}
$$

<!-- pdf-page: 619 -->

对式 (A.2) 取转置，再应用式 (A.1)，便很容易证明。

关于矩阵求逆，有一个有用的恒等式：

$$
(\mathbf P^{-1}+\mathbf B^{\mathsf T}\mathbf R^{-1}\mathbf B)^{-1}
\mathbf B^{\mathsf T}\mathbf R^{-1}
=\mathbf P\mathbf B^{\mathsf T}(\mathbf B\mathbf P\mathbf B^{\mathsf T}+\mathbf R)^{-1}. \tag{A.5}
$$

两边右乘 $(\mathbf B\mathbf P\mathbf B^{\mathsf T}+\mathbf R)$，即可验证。设 $\mathbf P$ 的维度为 $N\times N$，$\mathbf R$ 的维度为 $M\times M$，那么 $\mathbf B$ 为 $M\times N$。如果 $M\ll N$，计算式 (A.5) 右边比计算左边便宜得多。有时出现的特殊情形是

$$
(\mathbf I+\mathbf A\mathbf B)^{-1}\mathbf A
=\mathbf A(\mathbf I+\mathbf B\mathbf A)^{-1}. \tag{A.6}
$$

另一个有用的求逆恒等式是

$$
(\mathbf A+\mathbf B\mathbf D^{-1}\mathbf C)^{-1}
=\mathbf A^{-1}-\mathbf A^{-1}\mathbf B
(\mathbf D+\mathbf C\mathbf A^{-1}\mathbf B)^{-1}
\mathbf C\mathbf A^{-1}, \tag{A.7}
$$

称为 **Woodbury 恒等式**。两边乘以 $(\mathbf A+\mathbf B\mathbf D^{-1}\mathbf C)$ 即可验证。例如，当 $\mathbf A$ 是大型对角矩阵、因而容易求逆，而 $\mathbf B$ 有很多行但只有少量列（$\mathbf C$ 的情形相反）时，右边的计算成本会远低于左边。

若一组向量 $\{\mathbf a_1,\ldots,\mathbf a_N\}$ 满足 $\sum_n\alpha_n\mathbf a_n=0$ 仅当所有 $\alpha_n=0$ 时才成立，就称这组向量**线性无关**。这意味着其中没有一个向量能表示成其余向量的线性组合。矩阵的秩是其线性无关行的最大数量，也等于线性无关列的最大数量。

## A.2 迹与行列式

方阵有迹和行列式。矩阵 $\mathbf A$ 的迹 $\operatorname{Tr}(\mathbf A)$ 定义为主对角线上元素的和。展开指标可见

$$
\operatorname{Tr}(\mathbf A\mathbf B)=\operatorname{Tr}(\mathbf B\mathbf A). \tag{A.8}
$$

对三个矩阵的乘积多次应用这个式子，得到

$$
\operatorname{Tr}(\mathbf A\mathbf B\mathbf C)
=\operatorname{Tr}(\mathbf C\mathbf A\mathbf B)
=\operatorname{Tr}(\mathbf B\mathbf C\mathbf A), \tag{A.9}
$$

这称为迹算子的**循环性质**，显然可以推广到任意多个矩阵的乘积。$N\times N$ 矩阵 $\mathbf A$ 的行列式 $|\mathbf A|$ 定义为

$$
|\mathbf A|=\sum_{i_1,\ldots,i_N}(\pm1)A_{1i_1}A_{2i_2}\cdots A_{Ni_N}, \tag{A.10}
$$

其中求和遍历从每一行、每一列都恰好选取一个元素所得到的全部乘积；排列 $i_1i_2\cdots i_N$ 为偶排列时系数是 $+1$，为奇排列时是 $-1$。注意 $|\mathbf I|=1$，

<!-- pdf-page: 620 -->
<!-- join-previous-paragraph -->

而对角矩阵的行列式等于主对角线上各元素的乘积。因此，对于 $2\times2$ 矩阵，行列式为

$$
|\mathbf A|
=\begin{vmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{vmatrix}
=a_{11}a_{22}-a_{12}a_{21}. \tag{A.11}
$$

两个矩阵乘积的行列式满足

$$
|\mathbf A\mathbf B|=|\mathbf A|\,|\mathbf B|, \tag{A.12}
$$

这可以由式 (A.10) 证明。此外，逆矩阵的行列式为

$$
|\mathbf A^{-1}|=\frac{1}{|\mathbf A|}, \tag{A.13}
$$

对式 (A.2) 取行列式，再应用式 (A.12)，即可证明。

如果 $\mathbf A$ 与 $\mathbf B$ 都是 $N\times M$ 矩阵，那么

$$
|\mathbf I_N+\mathbf A\mathbf B^{\mathsf T}|
=|\mathbf I_M+\mathbf A^{\mathsf T}\mathbf B|. \tag{A.14}
$$

一个有用的特殊情形是

$$
|\mathbf I_N+\mathbf a\mathbf b^{\mathsf T}|
=1+\mathbf a^{\mathsf T}\mathbf b, \tag{A.15}
$$

其中 $\mathbf a$ 和 $\mathbf b$ 是 $N$ 维列向量。

## A.3 矩阵导数

有时需要考虑向量和矩阵对标量的导数。向量 $\mathbf a$ 对标量 $x$ 的导数也是一个向量，其分量定义为

$$
\left(\frac{\partial\mathbf a}{\partial x}\right)_i
=\frac{\partial a_i}{\partial x}. \tag{A.16}
$$

矩阵的导数也有类似定义。还可以定义对向量和矩阵的导数，例如

$$
\left(\frac{\partial x}{\partial\mathbf a}\right)_i
=\frac{\partial x}{\partial a_i}, \tag{A.17}
$$

以及

$$
\left(\frac{\partial\mathbf a}{\partial\mathbf b}\right)_{ij}
=\frac{\partial a_i}{\partial b_j}. \tag{A.18}
$$

把分量写出后，很容易证明

$$
\frac{\partial}{\partial\mathbf x}(\mathbf x^{\mathsf T}\mathbf a)
=\frac{\partial}{\partial\mathbf x}(\mathbf a^{\mathsf T}\mathbf x)
=\mathbf a. \tag{A.19}
$$

<!-- pdf-page: 621 -->

类似地，

$$
\frac{\partial}{\partial x}(\mathbf A\mathbf B)
=\frac{\partial\mathbf A}{\partial x}\mathbf B
+\mathbf A\frac{\partial\mathbf B}{\partial x}. \tag{A.20}
$$

矩阵逆的导数可以表示为

$$
\frac{\partial}{\partial x}(\mathbf A^{-1})
=-\mathbf A^{-1}\frac{\partial\mathbf A}{\partial x}\mathbf A^{-1}, \tag{A.21}
$$

对此，可利用式 (A.20) 对 $\mathbf A^{-1}\mathbf A=\mathbf I$ 求导，再右乘 $\mathbf A^{-1}$。此外，

$$
\frac{\partial}{\partial x}\ln|\mathbf A|
=\operatorname{Tr}\left(\mathbf A^{-1}\frac{\partial\mathbf A}{\partial x}\right), \tag{A.22}
$$

这一结果稍后证明。如果选择 $x$ 为 $\mathbf A$ 的某个元素，就有

$$
\frac{\partial}{\partial A_{ij}}\operatorname{Tr}(\mathbf A\mathbf B)=B_{ji}, \tag{A.23}
$$

把矩阵写成指标形式便可看出。此结果也可以更紧凑地写成

$$
\frac{\partial}{\partial\mathbf A}\operatorname{Tr}(\mathbf A\mathbf B)
=\mathbf B^{\mathsf T}. \tag{A.24}
$$

采用这种记号，还有以下性质：

$$
\frac{\partial}{\partial\mathbf A}\operatorname{Tr}(\mathbf A^{\mathsf T}\mathbf B)
=\mathbf B, \tag{A.25}
$$

$$
\frac{\partial}{\partial\mathbf A}\operatorname{Tr}(\mathbf A)
=\mathbf I, \tag{A.26}
$$

$$
\frac{\partial}{\partial\mathbf A}\operatorname{Tr}(\mathbf A\mathbf B\mathbf A^{\mathsf T})
=\mathbf A(\mathbf B+\mathbf B^{\mathsf T}), \tag{A.27}
$$

同样可展开矩阵指标证明。还有

$$
\frac{\partial}{\partial\mathbf A}\ln|\mathbf A|
=(\mathbf A^{-1})^{\mathsf T}, \tag{A.28}
$$

由式 (A.22) 和 (A.24) 可得。

## A.4 特征向量

对于 $M\times M$ 方阵 $\mathbf A$，特征向量方程定义为

$$
\mathbf A\mathbf u_i=\lambda_i\mathbf u_i. \tag{A.29}
$$

<!-- pdf-page: 622 -->

其中 $i=1,\ldots,M$，$\mathbf u_i$ 为特征向量，$\lambda_i$ 为对应的特征值。它可以看成一组 $M$ 个联立的齐次线性方程，有解的条件是

$$
|\mathbf A-\lambda_i\mathbf I|=0, \tag{A.30}
$$

称为**特征方程**。由于这是关于 $\lambda_i$ 的 $M$ 次多项式，它必有 $M$ 个解，不过这些解不一定互不相同。$\mathbf A$ 的秩等于非零特征值的个数。

**译注：** 这里的“个数”需按重数计。秩与非零特征值个数相等，对可对角化矩阵成立，特别适用于下文的实对称矩阵；一般方阵未必如此，例如非零幂零矩阵有正秩，但特征值全为零。

对称矩阵尤其重要，它们出现在协方差矩阵、核矩阵和 Hessian 矩阵中。对称矩阵满足 $A_{ij}=A_{ji}$，也就是 $\mathbf A^{\mathsf T}=\mathbf A$。对称矩阵的逆也对称：对 $\mathbf A^{-1}\mathbf A=\mathbf I$ 取转置，并使用 $\mathbf A\mathbf A^{-1}=\mathbf I$ 与 $\mathbf I$ 的对称性，即可看出。

一般而言，矩阵的特征值可以是复数，但对称矩阵的特征值 $\lambda_i$ 为实数。为说明这一点，先在式 (A.29) 左侧乘以 $(\mathbf u_i^*)^{\mathsf T}$，其中 $*$ 表示复共轭，得到

$$
(\mathbf u_i^*)^{\mathsf T}\mathbf A\mathbf u_i
=\lambda_i(\mathbf u_i^*)^{\mathsf T}\mathbf u_i. \tag{A.31}
$$

接着对式 (A.29) 取复共轭，并在左侧乘以 $\mathbf u_i^{\mathsf T}$，得到

$$
\mathbf u_i^{\mathsf T}\mathbf A\mathbf u_i^*
=\lambda_i^*\mathbf u_i^{\mathsf T}\mathbf u_i^*. \tag{A.32}
$$

这里使用了 $\mathbf A^*=\mathbf A$，因为只考虑实矩阵 $\mathbf A$。对第二个方程取转置并使用 $\mathbf A^{\mathsf T}=\mathbf A$，可见两个方程左边相等，因此 $\lambda_i^*=\lambda_i$，所以 $\lambda_i$ 必为实数。

实对称矩阵的特征向量可以选为**标准正交**的，即相互正交且长度为 1，从而

$$
\mathbf u_i^{\mathsf T}\mathbf u_j=I_{ij}, \tag{A.33}
$$

其中 $I_{ij}$ 是单位矩阵 $\mathbf I$ 的元素。为证明这一点，先在式 (A.29) 左侧乘以 $\mathbf u_j^{\mathsf T}$，得到

$$
\mathbf u_j^{\mathsf T}\mathbf A\mathbf u_i
=\lambda_i\mathbf u_j^{\mathsf T}\mathbf u_i, \tag{A.34}
$$

交换指标可得

$$
\mathbf u_i^{\mathsf T}\mathbf A\mathbf u_j
=\lambda_j\mathbf u_i^{\mathsf T}\mathbf u_j. \tag{A.35}
$$

对第二个方程取转置并利用对称性 $\mathbf A^{\mathsf T}=\mathbf A$，再将两式相减，得到

$$
(\lambda_i-\lambda_j)\mathbf u_i^{\mathsf T}\mathbf u_j=0. \tag{A.36}
$$

因此，当 $\lambda_i\ne\lambda_j$ 时，$\mathbf u_i^{\mathsf T}\mathbf u_j=0$，即 $\mathbf u_i$ 与 $\mathbf u_j$ 正交。如果两个特征值相等，任意线性组合 $\alpha\mathbf u_i+\beta\mathbf u_j$ 也都是

<!-- pdf-page: 623 -->
<!-- join-previous-paragraph -->

同一特征值的特征向量，所以可以任取一个线性组合，再选第二个使其与第一个正交（可以证明，简并特征向量绝不会线性相关）。于是可把特征向量选为正交向量，再归一化为单位长度。由于有 $M$ 个特征值，对应的 $M$ 个正交特征向量构成完备集，任何 $M$ 维向量都可表示成它们的线性组合。

**译注：** 对实对称矩阵，同一特征值的特征空间中可以选出线性无关的特征向量，并使其正交；任意选取的两个特征向量仍可能线性相关。

将特征向量 $\mathbf u_i$ 作为 $M\times M$ 矩阵 $\mathbf U$ 的列，根据标准正交性可得

$$
\mathbf U^{\mathsf T}\mathbf U=\mathbf I. \tag{A.37}
$$

这样的矩阵称为**正交矩阵**。有意思的是，它的行也正交，因此 $\mathbf U\mathbf U^{\mathsf T}=\mathbf I$。为说明这一点，注意式 (A.37) 意味着 $\mathbf U^{\mathsf T}\mathbf U\mathbf U^{-1}=\mathbf U^{-1}$，即 $\mathbf U^{\mathsf T}=\mathbf U^{-1}$，于是 $\mathbf U\mathbf U^{-1}=\mathbf U\mathbf U^{\mathsf T}=\mathbf I$。用式 (A.12) 还可得 $|\mathbf U|=1$。

**译注：** 一般正交矩阵的行列式为 $+1$ 或 $-1$。行列式为 $+1$ 时可解释为旋转；为 $-1$ 时还包含反射。因此下文的“刚性旋转”只适用于前一种情况。

特征向量方程 (A.29) 可以用 $\mathbf U$ 表示为

$$
\mathbf A\mathbf U=\mathbf U\boldsymbol\Lambda, \tag{A.38}
$$

其中 $\boldsymbol\Lambda$ 是 $M\times M$ 对角矩阵，其对角元素为特征值 $\lambda_i$。

考虑列向量 $\mathbf x$ 经正交矩阵 $\mathbf U$ 变换后得到的新向量

$$
\widetilde{\mathbf x}=\mathbf U\mathbf x. \tag{A.39}
$$

向量的长度保持不变，因为

$$
\widetilde{\mathbf x}^{\mathsf T}\widetilde{\mathbf x}
=\mathbf x^{\mathsf T}\mathbf U^{\mathsf T}\mathbf U\mathbf x
=\mathbf x^{\mathsf T}\mathbf x, \tag{A.40}
$$

任意两个这种向量之间的夹角也保持不变，因为

$$
\widetilde{\mathbf x}^{\mathsf T}\widetilde{\mathbf y}
=\mathbf x^{\mathsf T}\mathbf U^{\mathsf T}\mathbf U\mathbf y
=\mathbf x^{\mathsf T}\mathbf y. \tag{A.41}
$$

因此，乘以 $\mathbf U$ 可解释为坐标系的一次刚性旋转。

由式 (A.38) 可得

$$
\mathbf U^{\mathsf T}\mathbf A\mathbf U=\boldsymbol\Lambda, \tag{A.42}
$$

由于 $\boldsymbol\Lambda$ 是对角矩阵，称 $\mathbf A$ 被矩阵 $\mathbf U$ **对角化**。在式 (A.42) 左侧乘以 $\mathbf U$，右侧乘以 $\mathbf U^{\mathsf T}$，得到

$$
\mathbf A=\mathbf U\boldsymbol\Lambda\mathbf U^{\mathsf T}. \tag{A.43}
$$

对其求逆，并结合式 (A.3) 与 $\mathbf U^{-1}=\mathbf U^{\mathsf T}$，可得

$$
\mathbf A^{-1}=\mathbf U\boldsymbol\Lambda^{-1}\mathbf U^{\mathsf T}. \tag{A.44}
$$

<!-- pdf-page: 624 -->

最后两个方程也可以写为

$$
\mathbf A=\sum_{i=1}^{M}\lambda_i\mathbf u_i\mathbf u_i^{\mathsf T}, \tag{A.45}
$$

$$
\mathbf A^{-1}=\sum_{i=1}^{M}\frac{1}{\lambda_i}\mathbf u_i\mathbf u_i^{\mathsf T}. \tag{A.46}
$$

对式 (A.43) 取行列式，并使用式 (A.12)，得到

$$
|\mathbf A|=\prod_{i=1}^{M}\lambda_i. \tag{A.47}
$$

类似地，对式 (A.43) 取迹，利用迹算子的循环性质 (A.8) 以及 $\mathbf U^{\mathsf T}\mathbf U=\mathbf I$，得到

$$
\operatorname{Tr}(\mathbf A)=\sum_{i=1}^{M}\lambda_i. \tag{A.48}
$$

留给读者一项练习：利用式 (A.33)、(A.45)、(A.46) 和 (A.47) 验证式 (A.22)。

若对任意非零向量 $\mathbf w$ 都有 $\mathbf w^{\mathsf T}\mathbf A\mathbf w>0$，则称矩阵 $\mathbf A$ **正定**，记为 $\mathbf A\succ0$。等价地，正定矩阵的所有特征值均满足 $\lambda_i>0$；要理解这一点，可依次令 $\mathbf w$ 等于各特征向量，并注意任意向量都能展开为特征向量的线性组合。矩阵的所有元素均为正，并不保证它正定。例如矩阵

$$
\begin{pmatrix}1&2\\3&4\end{pmatrix} \tag{A.49}
$$

的特征值为 $\lambda_1\simeq5.37$、$\lambda_2\simeq-0.37$。若对所有 $\mathbf w$ 都有 $\mathbf w^{\mathsf T}\mathbf A\mathbf w\geqslant0$，则称矩阵**半正定**，记为 $\mathbf A\succeq0$，这等价于 $\lambda_i\geqslant0$。

**译注：** “二次型正定／半正定当且仅当所有特征值为正／非负”及上文的正交特征分解，以实对称矩阵为前提。对非对称矩阵，$\mathbf w^{\mathsf T}\mathbf A\mathbf w$ 只取决于对称部分 $(\mathbf A+\mathbf A^{\mathsf T})/2$；式 (A.49) 的示例矩阵本身并不对称。

矩阵的条件数为

$$
\mathrm{CN}=\left(\frac{\lambda_{\max}}{\lambda_{\min}}\right)^{1/2}, \tag{A.50}
$$

其中 $\lambda_{\max}$ 是最大特征值，$\lambda_{\min}$ 是最小特征值。

**译注：** 式 (A.50) 按原书保留 $1/2$ 次方。若“条件数”指对称正定矩阵本身的常用 2 范数条件数，通常写作 $\lambda_{\max}/\lambda_{\min}$；此处可能采用了不同约定。
