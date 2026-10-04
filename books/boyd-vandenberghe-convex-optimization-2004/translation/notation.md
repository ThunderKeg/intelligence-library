# 符号表

<aside class="chapter-guide"><p>导读（编者）：本表按集合、矩阵、范数、不等式等主题汇总全书记号，便于阅读时查阅。相似字母可能因字形、上下标不同而表示不同对象，查阅时应同时留意这些细节。</p></aside>

<!-- pdf-page: 711 -->

## 若干特定集合

<table class="notation-table" data-notation-group="sets" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="1"><td>$\mathbf{R}$</td><td>实数。</td></tr>
<tr data-notation-row="2"><td>$\mathbf{R}^n$</td><td>$n$ 维实向量（$n\times 1$ 矩阵）。</td></tr>
<tr data-notation-row="3"><td>$\mathbf{R}^{m\times n}$</td><td>$m\times n$ 实矩阵。</td></tr>
<tr data-notation-row="4"><td>$\mathbf{R}_{+},\ \mathbf{R}_{++}$</td><td>非负实数、正实数。</td></tr>
<tr data-notation-row="5"><td>$\mathbf{C}$</td><td>复数。</td></tr>
<tr data-notation-row="6"><td>$\mathbf{C}^n$</td><td>$n$ 维复向量。</td></tr>
<tr data-notation-row="7"><td>$\mathbf{C}^{m\times n}$</td><td>$m\times n$ 复矩阵。</td></tr>
<tr data-notation-row="8"><td>$\mathbf{Z}$</td><td>整数。</td></tr>
<tr data-notation-row="9"><td>$\mathbf{Z}_{+}$</td><td>非负整数。</td></tr>
<tr data-notation-row="10"><td>$\mathbf{S}^n$</td><td>$n\times n$ 对称矩阵。</td></tr>
<tr data-notation-row="11"><td>$\mathbf{S}_{+}^n,\ \mathbf{S}_{++}^n$</td><td>$n\times n$ 对称半正定矩阵、对称正定矩阵。</td></tr>
</tbody>
</table>

## 向量与矩阵

<table class="notation-table" data-notation-group="vectors_matrices" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="12"><td>$\mathbf{1}$</td><td>所有分量均为一的向量。</td></tr>
<tr data-notation-row="13"><td>$e_i$</td><td>第 $i$ 个标准基向量。</td></tr>
<tr data-notation-row="14"><td>$I$</td><td>单位矩阵。</td></tr>
<tr data-notation-row="15"><td>$X^T$</td><td>矩阵 $X$ 的转置。</td></tr>
<tr data-notation-row="16"><td>$X^H$</td><td>矩阵 $X$ 的 Hermitian（复共轭）转置。</td></tr>
<tr data-notation-row="17"><td>$\mathbf{tr}\,X$</td><td>矩阵 $X$ 的迹。</td></tr>
<tr data-notation-row="18"><td>$\lambda_i(X)$</td><td>对称矩阵 $X$ 的第 $i$ 大特征值。</td></tr>
<tr data-notation-row="19"><td>$\lambda_{\max}(X),\ \lambda_{\min}(X)$</td><td>对称矩阵 $X$ 的最大、最小特征值。</td></tr>
<tr data-notation-row="20"><td>$\sigma_i(X)$</td><td>矩阵 $X$ 的第 $i$ 大奇异值。</td></tr>
<tr data-notation-row="21"><td>$\sigma_{\max}(X),\ \sigma_{\min}(X)$</td><td>矩阵 $X$ 的最大、最小奇异值。</td></tr>
<tr data-notation-row="22"><td>$X^\dagger$</td><td>矩阵 $X$ 的 Moore–Penrose 逆或伪逆。</td></tr>
<tr data-notation-row="23"><td>$x\perp y$</td><td>向量 $x$ 与 $y$ 正交：$x^T y=0$。</td></tr>
<tr data-notation-row="24"><td>$V^\perp$</td><td>子空间 $V$ 的正交补。</td></tr>
<tr data-notation-row="25"><td>$\mathbf{diag}(x)$</td><td>对角元素为 $x_1,\ldots,x_n$ 的对角矩阵。</td></tr>
<tr data-notation-row="26"><td>$\mathbf{diag}(X,Y,\ldots)$</td><td>对角分块为 $X,Y,\ldots$ 的分块对角矩阵。</td></tr>
<tr data-notation-row="27"><td>$\mathbf{rank}\,A$</td><td>矩阵 $A$ 的秩。</td></tr>
<tr data-notation-row="28"><td>$\mathcal{R}(A)$</td><td>矩阵 $A$ 的值域。</td></tr>
<tr data-notation-row="29"><td>$\mathcal{N}(A)$</td><td>矩阵 $A$ 的零空间。</td></tr>
</tbody>
</table>

<!-- pdf-page: 712 -->

## 范数与距离

<table class="notation-table" data-notation-group="norms_distances" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="30"><td>$\|\cdot\|$</td><td>一个范数。</td></tr>
<tr data-notation-row="31"><td>$\|\cdot\|_*$</td><td>范数 $\|\cdot\|$ 的对偶范数。</td></tr>
<tr data-notation-row="32"><td>$\|x\|_2$</td><td>向量 $x$ 的欧几里得范数（或 $\ell_2$ 范数）。</td></tr>
<tr data-notation-row="33"><td>$\|x\|_1$</td><td>向量 $x$ 的 $\ell_1$ 范数。</td></tr>
<tr data-notation-row="34"><td>$\|x\|_\infty$</td><td>向量 $x$ 的 $\ell_\infty$ 范数。</td></tr>
<tr data-notation-row="35"><td>$\|X\|_2$</td><td>矩阵 $X$ 的谱范数（最大奇异值）。</td></tr>
<tr data-notation-row="36"><td>$B(c,r)$</td><td>以 $c$ 为中心、$r$ 为半径的球。</td></tr>
<tr data-notation-row="37"><td>$\mathbf{dist}(A,B)$</td><td>集合（或点）$A$ 与 $B$ 之间的距离。</td></tr>
</tbody>
</table>

## 广义不等式

<table class="notation-table" data-notation-group="inequalities" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="38"><td>$x\preceq y$</td><td>向量 $x$ 与 $y$ 之间的逐分量不等式。</td></tr>
<tr data-notation-row="39"><td>$x\prec y$</td><td>向量 $x$ 与 $y$ 之间的严格逐分量不等式</td></tr>
<tr data-notation-row="40"><td>$X\preceq Y$</td><td>对称矩阵 $X$ 与 $Y$ 之间的矩阵不等式。</td></tr>
<tr data-notation-row="41"><td>$X\prec Y$</td><td>对称矩阵 $X$ 与 $Y$ 之间的严格矩阵不等式。</td></tr>
<tr data-notation-row="42"><td>$x\preceq_K y$</td><td>由正常锥 $K$ 诱导的广义不等式。</td></tr>
<tr data-notation-row="43"><td>$x\prec_K y$</td><td>由正常锥 $K$ 诱导的严格广义不等式。</td></tr>
<tr data-notation-row="44"><td>$x\preceq_{K^*}y$</td><td>对偶广义不等式。</td></tr>
<tr data-notation-row="45"><td>$x\prec_{K^*}y$</td><td>对偶严格广义不等式。</td></tr>
</tbody>
</table>

## 拓扑与凸分析

<table class="notation-table" data-notation-group="topology_convex_analysis" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="46"><td>$\mathbf{card}\,C$</td><td>集合 $C$ 的基数。</td></tr>
<tr data-notation-row="47"><td>$\mathbf{int}\,C$</td><td>集合 $C$ 的内部。</td></tr>
<tr data-notation-row="48"><td>$\mathbf{relint}\,C$</td><td>集合 $C$ 的相对内部。</td></tr>
<tr data-notation-row="49"><td>$\mathbf{cl}\,C$</td><td>集合 $C$ 的闭包。</td></tr>
<tr data-notation-row="50"><td>$\mathbf{bd}\,C$</td><td>集合 $C$ 的边界：$\mathbf{bd}\,C=\mathbf{cl}\,C\setminus\mathbf{int}\,C$。</td></tr>
<tr data-notation-row="51"><td>$\mathbf{conv}\,C$</td><td>集合 $C$ 的凸包。</td></tr>
<tr data-notation-row="52"><td>$\mathbf{aff}\,C$</td><td>集合 $C$ 的仿射包。</td></tr>
<tr data-notation-row="53"><td>$K^*$</td><td>与 $K$ 对应的对偶锥。</td></tr>
<tr data-notation-row="54"><td>$I_C$</td><td>集合 $C$ 的指示函数。</td></tr>
<tr data-notation-row="55"><td>$S_C$</td><td>集合 $C$ 的支撑函数。</td></tr>
<tr data-notation-row="56"><td>$f^*$</td><td>$f$ 的共轭函数。</td></tr>
</tbody>
</table>

## 概率

<table class="notation-table" data-notation-group="probability" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="57"><td>$\mathbf{E}\,X$</td><td>随机向量 $X$ 的期望值。</td></tr>
<tr data-notation-row="58"><td>$\mathbf{prob}\,S$</td><td>事件 $S$ 的概率。</td></tr>
<tr data-notation-row="59"><td>$\mathbf{var}\,X$</td><td>标量随机变量 $X$ 的方差。</td></tr>
<tr data-notation-row="60"><td>$\mathcal{N}(c,\Sigma)$</td><td>均值为 $c$、协方差（矩阵）为 $\Sigma$ 的高斯分布。</td></tr>
<tr data-notation-row="61"><td>$\Phi$</td><td>$\mathcal{N}(0,1)$ 随机变量的累积分布函数。</td></tr>
</tbody>
</table>

<!-- pdf-page: 713 -->

## 函数与导数

<table class="notation-table" data-notation-group="functions_derivatives" style="min-width:0;width:100%">
<tbody>
<tr data-notation-row="62"><td>$f:A\to B$</td><td>$f$ 是定义在集合 $\mathbf{dom}\,f\subseteq A$ 上、取值于集合 $B$ 的函数。</td></tr>
<tr data-notation-row="63"><td>$\mathbf{dom}\,f$</td><td>函数 $f$ 的定义域。</td></tr>
<tr data-notation-row="64"><td>$\mathbf{epi}\,f$</td><td>函数 $f$ 的上图。</td></tr>
<tr data-notation-row="65"><td>$\nabla f$</td><td>函数 $f$ 的梯度。</td></tr>
<tr data-notation-row="66"><td>$\nabla^2 f$</td><td>函数 $f$ 的 Hessian 矩阵。</td></tr>
<tr data-notation-row="67"><td>$Df$</td><td>函数 $f$ 的导数（Jacobian）矩阵。</td></tr>
</tbody>
</table>

<!-- pdf-page: 714 -->
