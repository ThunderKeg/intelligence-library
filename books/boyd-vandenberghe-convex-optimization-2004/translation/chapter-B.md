<!-- pdf-page: 667 -->

# 附录 B 涉及两个二次函数的问题

<aside class="chapter-guide"><p>导读（编者）：本附录研究一个目标函数和一个约束函数均为二次函数时的特殊结论，包括强对偶性、半定松弛和 S-程序。阅读时注意严格可行性假设的作用，并对照最后的证明，理解二次函数与矩阵半定条件之间的联系。</p></aside>

本附录考察一些涉及两个二次函数的优化问题；这两个函数不一定是凸函数。对于这些问题，即使它们非凸，也有若干很强的结论成立。

## B.1 单约束二次优化

考虑只有一个约束的问题

$$
\begin{aligned}
\text{最小化}\quad &x^TA_0x+2b_0^Tx+c_0\\
\text{约束为}\quad &x^TA_1x+2b_1^Tx+c_1\leq0,
\end{aligned}
\tag{B.1}
$$

其中变量为 $x\in\mathbf{R}^n$，问题参数为 $A_i\in\mathbf{S}^n$、$b_i\in\mathbf{R}^n$、$c_i\in\mathbf{R}$。我们不假设 $A_i\succeq0$，因此问题 (B.1) 不是凸优化问题。

(B.1) 的拉格朗日函数为

$$
L(x,\lambda)=x^T(A_0+\lambda A_1)x+2(b_0+\lambda b_1)^Tx+c_0+\lambda c_1,
$$

对偶函数为

$$
\begin{aligned}
g(\lambda)&=\inf_x L(x,\lambda)\\
&=
\begin{cases}
c_0+\lambda c_1-(b_0+\lambda b_1)^T(A_0+\lambda A_1)^\dagger(b_0+\lambda b_1)
&
\begin{gathered}
A_0+\lambda A_1\succeq0,\\
b_0+\lambda b_1\in\mathcal{R}(A_0+\lambda A_1)
\end{gathered}\\
-\infty&\text{其他情形}
\end{cases}
\end{aligned}
$$

（见 §A.5.4）。利用 Schur 补，可将对偶问题写为

$$
\begin{aligned}
\text{最大化}\quad &\gamma\\
\text{约束为}\quad &\lambda\geq0\\
&\begin{bmatrix}
A_0+\lambda A_1&b_0+\lambda b_1\\
(b_0+\lambda b_1)^T&c_0+\lambda c_1-\gamma
\end{bmatrix}\succeq0,
\end{aligned}
\tag{B.2}
$$

<!-- pdf-page: 668 -->

这是一个以 $\gamma,\lambda\in\mathbf{R}$ 为两个变量的 SDP。

第一个结论是，只要满足 Slater 约束资格条件，即存在 $x$ 使 $x^TA_1x+2b_1^Tx+c_1<0$，问题 (B.1) 与其拉格朗日对偶 (B.2) 之间就有强对偶性。换言之，若 (B.1) 严格可行，则 (B.1) 与 (B.2) 的最优值相等。（证明见 §B.4。）

### 松弛解释

SDP (B.2) 的对偶为

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(A_0X)+2b_0^Tx+c_0\\
\text{约束为}\quad &\mathbf{tr}(A_1X)+2b_1^Tx+c_1\leq0\\
&\begin{bmatrix}X&x\\x^T&1\end{bmatrix}\succeq0,
\end{aligned}
\tag{B.3}
$$

这是一个以 $X\in\mathbf{S}^n$、$x\in\mathbf{R}^n$ 为变量的 SDP。相对于原问题 (B.1)，这个对偶 SDP 有一种有意思的解释。

首先注意，(B.1) 等价于

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(A_0X)+2b_0^Tx+c_0\\
\text{约束为}\quad &\mathbf{tr}(A_1X)+2b_1^Tx+c_1\leq0\\
&X=xx^T.
\end{aligned}
\tag{B.4}
$$

在这个表述中，我们将二次项 $x^TA_ix$ 写成 $\mathbf{tr}(A_ixx^T)$，再引入新变量 $X=xx^T$。问题 (B.4) 的目标函数为线性函数，有一个线性不等式约束，以及一个非线性等式约束 $X=xx^T$。下一步是将这个等式约束替换为不等式 $X\succeq xx^T$：

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(A_0X)+b_0^Tx+c_0\\
\text{约束为}\quad &\mathbf{tr}(A_1X)+b_1^Tx+c_1\leq0\\
&X\succeq xx^T.
\end{aligned}
\tag{B.5}
$$

这个问题称为 (B.4) 的一个松弛，因为其中一个约束被替换成了更宽松的约束。最后注意，利用 Schur 补，可以把 (B.5) 中的不等式写成线性矩阵不等式，从而得到 (B.3)。

<div class="translator-note" markdown="1">

**译注（松弛模型中的线性项）：** 式 (B.5) 沿用 (B.4) 时，目标和约束中的线性项应分别是 $2b_0^Tx$ 和 $2b_1^Tx$。原式在这两处省略了系数 2；这一步只放松 $X=xx^T$ 约束，不改变原目标和其他项。

</div>

将 (B.3) 解释为 (B.1) 的松弛，可以立即得到若干有意思的事实。首先，(B.3) 的最优值显然小于或等于 (B.1) 的最优值，因为我们是在一个更大的集合上最小化同一个目标函数。其次，可以断定，如果 (B.3) 的最优解满足 $X=xx^T$，那么 $x$ 必定也是 (B.1) 的最优解。

将前面得到的结论——若 (B.1) 严格可行，则 (B.1) 与 (B.2) 之间有强对偶性——与互为对偶的 SDP (B.2) 和 (B.3) 之间的强对偶性结合起来，可知：只要 (B.1) 严格可行，原来的非凸二次问题 (B.1) 与 SDP 松弛 (B.3) 之间就有强对偶性。

<!-- pdf-page: 669 -->

## B.2 S-程序

下面的结论是一对（非凸）二次不等式的择一定理。设 $A_1,A_2\in\mathbf{S}^n$、$b_1,b_2\in\mathbf{R}^n$、$c_1,c_2\in\mathbf{R}$，并假设存在 $\hat x$，使

$$
\hat x^TA_2\hat x+2b_2^T\hat x+c_2<0.
$$

那么，存在 $x\in\mathbf{R}^n$ 满足

$$
x^TA_1x+2b_1^Tx+c_1<0,\qquad x^TA_2x+2b_2^Tx+c_2\leq0,
\tag{B.6}
$$

当且仅当不存在 $\lambda$ 使

$$
\lambda\geq0,\qquad
\begin{bmatrix}A_1&b_1\\b_1^T&c_1\end{bmatrix}
+\lambda\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}\succeq0.
\tag{B.7}
$$

换言之，(B.6) 与 (B.7) 是强择一系统。

容易证明，这个结论与 §B.1 的结论等价，证明见 §B.4。这里指出，这两个不等式系统显然是弱择一系统，因为 (B.6) 与 (B.7) 同时成立会导致矛盾：

$$
\begin{aligned}
0
&\leq
\begin{bmatrix}x\\1\end{bmatrix}^T
\left(
\begin{bmatrix}A_1&b_1\\b_1^T&c_1\end{bmatrix}
+\lambda\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}
\right)
\begin{bmatrix}x\\1\end{bmatrix}\\
&=x^TA_1x+2b_1^Tx+c_1+\lambda(x^TA_2x+2b_2^Tx+c_2)\\
&<0.
\end{aligned}
$$

这个择一定理有时称为 S-程序（S-procedure），通常表述成以下形式：蕴含关系

$$
x^TF_1x+2g_1^Tx+h_1\leq0
\quad\Longrightarrow\quad
x^TF_2x+2g_2^Tx+h_2\leq0,
$$

其中 $F_i\in\mathbf{S}^n$、$g_i\in\mathbf{R}^n$、$h_i\in\mathbf{R}$，成立当且仅当存在 $\lambda$ 使

$$
\lambda\geq0,\qquad
\begin{bmatrix}F_2&g_2\\g_2^T&h_2\end{bmatrix}
\preceq
\lambda\begin{bmatrix}F_1&g_1\\g_1^T&h_1\end{bmatrix},
$$

前提是存在点 $\hat x$ 满足 $\hat x^TF_1\hat x+2g_1^T\hat x+h_1<0$。（注意，充分性是显然的。）

<div class="example" id="example-B-1" markdown="1">

**例 B.1 椭球的包含关系。** 内部非空的椭球 $\mathcal{E}\subseteq\mathbf{R}^n$ 可以表示为一个二次函数的下水平集：

$$
\mathcal{E}=\{x\mid x^TFx+2g^Tx+h\leq0\},
$$

其中 $F\in\mathbf{S}_{++}$，且 $h-g^TF^{-1}g<0$。设 $\tilde{\mathcal{E}}$ 是另一个椭球，具有类似的表示：

$$
\tilde{\mathcal{E}}=\{x\mid x^T\tilde F x+2\tilde g^Tx+\tilde h\leq0\},
$$

其中 $\tilde F\in\mathbf{S}_{++}$，且 $\tilde h-\tilde g^T\tilde F^{-1}\tilde g<0$。由 S-程序可知，$\mathcal{E}\subseteq\tilde{\mathcal{E}}$ 当且仅当存在 $\lambda>0$，使

$$
\begin{bmatrix}\tilde F&\tilde g\\\tilde g^T&\tilde h\end{bmatrix}
\preceq
\lambda\begin{bmatrix}F&g\\g^T&h\end{bmatrix}.
$$

</div>

<!-- pdf-page: 670 -->

## B.3 两个对称矩阵的值域

下面的结论是证明 §B.1 强对偶性结论和 §B.2 S-程序的基础。若 $A,B\in\mathbf{S}^n$，则对于所有 $X\in\mathbf{S}_+^n$，都存在 $x\in\mathbf{R}^n$，使

$$
x^TAx=\mathbf{tr}(AX),\qquad x^TBx=\mathbf{tr}(BX).
\tag{B.8}
$$

<div class="remark" id="remark-B-1" markdown="1">

**注 B.1 几何解释。** 借助集合

$$
W(A,B)=\{(x^TAx,x^TBx)\mid x\in\mathbf{R}^n\},
$$

可以对这个结论作出一种有意思的解释。$W(A,B)$ 是 $\mathbf{R}^2$ 中的一个锥，由集合

$$
F(A,B)=\{(x^TAx,x^TBx)\mid\|x\|_2=1\}
$$

生成；$F(A,B)$ 称为矩阵对 $(A,B)$ 的二维值域（field of values）。从几何上看，$W(A,B)$ 是所有秩为一的半正定矩阵组成的集合，在线性变换 $f:\mathbf{S}^n\to\mathbf{R}^2$

$$
f(X)=(\mathbf{tr}(AX),\mathbf{tr}(BX))
$$

下的像。

对于每个 $X\in\mathbf{S}_+^n$，都存在 $x$ 满足 (B.8)，这一结论意味着

$$
W(A,B)=f(\mathbf{S}_+^n).
$$

换言之，$W(A,B)$ 是一个凸锥。

</div>

这个证明是构造性的，使用关于 $X$ 的秩的归纳法。设 $k\geq2$，并假设对于所有满足 $1\leq\mathbf{rank}\,X\leq k$ 的 $X\in\mathbf{S}_+^n$，都存在 $x$ 使 (B.8) 成立。那么，当 $\mathbf{rank}\,X=k+1$ 时，这个结论也成立，理由如下。秩为 $k+1$ 的矩阵 $X\in\mathbf{S}_+^n$ 可以表示成 $X=yy^T+Z$，其中 $y\ne0$，$Z\in\mathbf{S}_+^n$，且 $\mathbf{rank}\,Z=k$。由归纳假设，存在 $z$ 使 $\mathbf{tr}(AZ)=z^TAz$、$\mathbf{tr}(BZ)=z^TBz$。因此，

$$
\mathbf{tr}(AX)=\mathbf{tr}\bigl(A(yy^T+zz^T)\bigr),
\qquad
\mathbf{tr}(BX)=\mathbf{tr}\bigl(B(yy^T+zz^T)\bigr).
$$

$yy^T+zz^T$ 的秩为一或二，因此由假设，存在 $x$ 使 (B.8) 成立。

所以，只需证明 $\mathbf{rank}\,X\leq2$ 时的结论。对于 $\mathbf{rank}\,X=0$ 和 $\mathbf{rank}\,X=1$，无需证明。若 $\mathbf{rank}\,X=2$，则可以将 $X$ 分解为 $X=VV^T$，其中 $V\in\mathbf{R}^{n\times2}$ 的两列 $v_1$、$v_2$ 线性无关。不失一般性，可以假设 $V^TAV$ 为对角矩阵。（如果 $V^TAV$ 不是对角矩阵，就用 $VP$ 替换 $V$，其中 $V^TAV=P\mathbf{diag}(\lambda)P^T$ 是 $V^TAV$ 的特征值分解。）将 $V^TAV$ 和 $V^TBV$ 写为

$$
V^TAV=\begin{bmatrix}\lambda_1&0\\0&\lambda_2\end{bmatrix},
\qquad
V^TBV=\begin{bmatrix}\sigma_1&\gamma\\\gamma&\sigma_2\end{bmatrix},
$$

并定义

$$
w=\begin{bmatrix}\mathbf{tr}(AX)\\\mathbf{tr}(BX)\end{bmatrix}
=\begin{bmatrix}\lambda_1+\lambda_2\\\sigma_1+\sigma_2\end{bmatrix}.
$$

<!-- pdf-page: 671 -->

需要证明，对于某个 $x$，有 $w=(x^TAx,x^TBx)$。

分两种情况讨论。首先，假设 $(0,\gamma)$ 是向量 $(\lambda_1,\sigma_1)$ 和 $(\lambda_2,\sigma_2)$ 的线性组合：

$$
0=z_1\lambda_1+z_2\lambda_2,\qquad
\gamma=z_1\sigma_1+z_2\sigma_2,
$$

其中 $z_1,z_2$ 为某两个数。这时取 $x=\alpha v_1+\beta v_2$，其中 $\alpha$ 和 $\beta$ 通过求解下面两个二元二次方程确定：

$$
\alpha^2+2\alpha\beta z_1=1,\qquad
\beta^2+2\alpha\beta z_2=1.
\tag{B.9}
$$

这会给出所需的结果，因为

$$
\begin{aligned}
&\begin{bmatrix}
(\alpha v_1+\beta v_2)^TA(\alpha v_1+\beta v_2)\\
(\alpha v_1+\beta v_2)^TB(\alpha v_1+\beta v_2)
\end{bmatrix}\\
&\quad=\alpha^2\begin{bmatrix}\lambda_1\\\sigma_1\end{bmatrix}
+2\alpha\beta\begin{bmatrix}0\\\gamma\end{bmatrix}
+\beta^2\begin{bmatrix}\lambda_2\\\sigma_2\end{bmatrix}\\
&\quad=(\alpha^2+2\alpha\beta z_1)\begin{bmatrix}\lambda_1\\\sigma_1\end{bmatrix}
+(\beta^2+2\alpha\beta z_2)\begin{bmatrix}\lambda_2\\\sigma_2\end{bmatrix}\\
&\quad=\begin{bmatrix}\lambda_1+\lambda_2\\\sigma_1+\sigma_2\end{bmatrix}.
\end{aligned}
$$

还需证明方程组 (B.9) 有解。为此，首先注意到 $\alpha$ 和 $\beta$ 必须都非零，因此可以将方程组等价地写为

$$
\alpha^2\bigl(1+2(\beta/\alpha)z_1\bigr)=1,\qquad
(\beta/\alpha)^2+2(\beta/\alpha)(z_2-z_1)=1.
$$

方程 $t^2+2t(z_2-z_1)=1$ 有一个正根和一个负根。其中至少有一个根（与 $z_1$ 同号的那个根）满足 $1+2tz_1>0$，因此可以取

$$
\alpha=\pm1/\sqrt{1+2tz_1},\qquad\beta=t\alpha.
$$

这样就得到两个满足 (B.9) 的解 $(\alpha,\beta)$。（如果 $t^2+2t(z_2-z_1)=1$ 的两个根都满足 $1+2tz_1>0$，则会得到四个解。）

接着，假设 $(0,\gamma)$ 不是 $(\lambda_1,\sigma_1)$ 和 $(\lambda_2,\sigma_2)$ 的线性组合。特别地，这意味着 $(\lambda_1,\sigma_1)$ 与 $(\lambda_2,\sigma_2)$ 线性相关。因此，它们的和 $w=(\lambda_1+\lambda_2,\sigma_1+\sigma_2)$ 是 $(\lambda_1,\sigma_1)$ 或 $(\lambda_2,\sigma_2)$ 的非负倍数，也可能同时是两者的非负倍数。如果对某个 $\alpha$，有 $w=\alpha^2(\lambda_1,\sigma_1)$，则可以取 $x=\alpha v_1$。如果对某个 $\beta$，有 $w=\beta^2(\lambda_2,\sigma_2)$，则可以取 $x=\beta v_2$。

## B.4 强对偶性结论的证明

首先证明 §B.2 给出的 S-程序结论。$\hat x$ 严格可行的假设意味着矩阵

$$
\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}
$$

<!-- pdf-page: 672 -->

至少有一个负特征值。因此，

$$
\tau\geq0,\qquad
\tau\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}\succeq0
\quad\Longrightarrow\quad\tau=0.
$$

可以应用例 5.14 中非严格线性矩阵不等式的择一定理。该定理指出，(B.7) 不可行，当且仅当

$$
X\succeq0,\qquad
\mathbf{tr}\left(X\begin{bmatrix}A_1&b_1\\b_1^T&c_1\end{bmatrix}\right)<0,\qquad
\mathbf{tr}\left(X\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}\right)\leq0
$$

可行。由 §B.3，这又等价于下面的系统可行：

$$
\begin{bmatrix}v\\w\end{bmatrix}^T
\begin{bmatrix}A_1&b_1\\b_1^T&c_1\end{bmatrix}
\begin{bmatrix}v\\w\end{bmatrix}<0,\qquad
\begin{bmatrix}v\\w\end{bmatrix}^T
\begin{bmatrix}A_2&b_2\\b_2^T&c_2\end{bmatrix}
\begin{bmatrix}v\\w\end{bmatrix}\leq0.
$$

若 $w\ne0$，则 $x=v/w$ 在 (B.6) 中可行。若 $w=0$，则有 $v^TA_1v<0$、$v^TA_2v\leq0$，因此 $x=\hat x+tv$ 满足

$$
\begin{aligned}
x^TA_1x+2b_1^Tx+c_1
&=\hat x^TA_1\hat x+2b_1^T\hat x+c_1+t^2v^TA_1v+2t(A_1\hat x+b_1)^Tv\\
x^TA_2x+2b_2^Tx+c_2
&=\hat x^TA_2\hat x+2b_2^T\hat x+c_2+t^2v^TA_2v+2t(A_2\hat x+b_2)^Tv\\
&<2t(A_2\hat x+b_2)^Tv,
\end{aligned}
$$

也就是说，根据 $(A_2\hat x+b_2)^Tv$ 的符号，在 $t\to+\infty$ 或 $t\to-\infty$ 时，$x$ 会变得可行。

最后证明 §B.1 中的结论，即若 (B.1) 严格可行，则 (B.1) 与 (B.2) 的最优值相等。为此，注意到如果

$$
x^TA_1x+b_1^Tx+c_1\leq0
\quad\Longrightarrow\quad
x^TA_0x+b_0^Tx+c_0\geq\gamma,
$$

那么 $\gamma$ 就是 (B.1) 最优值的一个下界。根据 S-程序，这个蕴含关系成立，当且仅当存在 $\lambda\geq0$，使

$$
\begin{bmatrix}A_0&b_0\\b_0^T&c_0-\gamma\end{bmatrix}
+\lambda\begin{bmatrix}A_1&b_1\\b_1^T&c_1\end{bmatrix}\succeq0,
$$

即 $\gamma,\lambda$ 在 (B.2) 中可行。

<div class="translator-note" markdown="1">

**译注（证明中二次函数的系数）：** 上面的蕴含式与 (B.1) 采用同一组 $A_i,b_i,c_i$，所以两侧的线性项应分别为 $2b_1^Tx$ 和 $2b_0^Tx$；这也与紧随其后的对称分块矩阵一致。原文两处未写系数 2。

</div>

<!-- pdf-page: 673 -->

## 文献说明

本附录中的结论在不同学科中有不同的名称。S-程序这一术语来自控制领域；综述及参考文献可见 Boyd、El Ghaoui、Feron 与 Balakrishnan [BEFB94，第 23、33 页]。在线性代数中，一对对称矩阵的同时对角化问题也涉及 S-程序的变体，例如 Calabi [Cal64] 和 Uhlig [Uhl79]。关于信赖域方法的非线性规划文献研究了强对偶性结论的若干特例（Stern 与 Wolkowicz [SW95]，Nocedal 与 Wright [NW99，第 78 页]）。

Brickman [Bri61] 证明，当 $n>2$ 时，一对矩阵 $A,B\in\mathbf{S}^n$ 的值域（即注 B.1 中定义的集合 $F(A,B)$）是凸集，而集合 $W(A,B)$ 对任意 $n$ 都是凸锥。§B.3 中的证明基于 Hestenes [Hes68]。许多相关结论及其他参考文献可见 Horn 与 Johnson [HJ91, §1.8]，以及 Ben-Tal 与 Nemirovski [BTN01, §4.10.5]。

<!-- pdf-page: 674 -->
