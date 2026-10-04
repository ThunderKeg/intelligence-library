**11.17 对偶广义对数。** 设 $\psi$ 是正常锥 $K$ 的广义对数，次数为 $\theta$。证明，式 (11.49) 定义的对偶广义对数 $\bar\psi$ 满足

$$
\bar\psi(sv)=\psi(v)+\theta\log s,
$$

其中 $v\succ_{K^*}0$、$s>0$。

**11.18** 函数

$$
\psi(y)=\log\left(y_{n+1}-\frac{\sum_{i=1}^n y_i^2}{y_{n+1}}\right),
$$

其定义域为 $\mathbf{dom}\,\psi=\{y\in\mathbf{R}^{n+1}\mid y_{n+1}>\sum_{i=1}^n y_i^2\}$，是否是 $\mathbf{R}^{n+1}$ 中二阶锥的广义对数？

### 实现

**11.19 计算牛顿步的又一种方法。** 障碍法的牛顿步由线性方程组 (11.14) 的解给出。证明，也可以通过求解一个更大的线性方程组来得到这个牛顿步，其系数矩阵为

$$
\begin{bmatrix}
t\nabla^2 f_0(x)+\sum_i\dfrac{1}{-f_i(x)}\nabla^2 f_i(x) & Df(x)^T & A^T\\
Df(x) & -\mathbf{diag}(f(x))^2 & 0\\
A & 0 & 0
\end{bmatrix},
$$

其中 $f(x)=(f_1(x),\ldots,f_m(x))$。

对于哪些类型的问题结构，求解这个更大的方程组可能值得考虑？

**11.20 通过对偶问题进行网络速率优化。** 本题考察求解 §11.8.4 网络速率优化问题的一种对偶方法。为简化叙述，假设效用函数 $U_i$ 严格凹，定义域为 $\mathbf{dom}\,U_i=\mathbf{R}_{++}$，并且满足：当 $x_i\to0$ 时，$U_i'(x_i)\to\infty$；当 $x_i\to\infty$ 时，$U_i'(x_i)\to0$。

- (a) 用共轭效用函数 $V_i=(-U_i)^*$ 表示问题 (11.62) 的对偶问题，其中

    $$
    V_i(\lambda)=\sup_{x>0}(\lambda x+U_i(x)).
    $$

    证明，$\mathbf{dom}\,V_i=-\mathbf{R}_{++}$，并且对每个 $\lambda<0$，都存在唯一的 $x$ 满足 $U_i'(x)=-\lambda$。

- (b) 描述求解对偶问题的障碍法。将每次迭代的复杂度与 §11.8.4 中方法的复杂度作比较。像 §11.8.4 那样，分别讨论 $A^TA$ 稀疏和 $AA^T$ 稀疏这两种情况。

<!-- pdf-page: 643 -->

### 数值实验

**11.21 带界约束的对数 Chebyshev 逼近。** 考虑如下逼近问题：求 $x\in\mathbf{R}^n$，使它满足变量的界约束 $l\preceq x\preceq u$，并使 $Ax\approx b$，其中 $b\in\mathbf{R}^m$。可以假设 $l\prec u$ 且 $b\succ0$（原因将在下面说明）。用 $a_i^T$ 表示矩阵 $A$ 的第 $i$ 行。

我们用最大比例偏差（maximum fractional deviation）来衡量逼近 $Ax\approx b$ 的好坏。当 $Ax\succ0$ 时，这个量为

$$
\max_{i=1,\ldots,n}\max\{(a_i^Tx)/b_i,\ b_i/(a_i^Tx)\}
=\max_{i=1,\ldots,n}\frac{\max\{a_i^Tx,b_i\}}{\min\{a_i^Tx,b_i\}};
$$

当 $Ax\not\succ0$ 时，将最大比例偏差定义为 $\infty$。

最小化最大比例偏差的问题称为比例 Chebyshev 逼近问题（fractional Chebyshev approximation problem），也称为对数 Chebyshev 逼近问题，因为它等价于最小化目标

$$
\max_{i=1,\ldots,n}|\log a_i^Tx-\log b_i|.
$$

（另见习题 6.3 的 (c)。）

- (a) 将带变量界约束的比例 Chebyshev 逼近问题，表述为目标函数和约束函数均二阶可微的凸优化问题。

- (b) 实现求解比例 Chebyshev 逼近问题的障碍法。可以假设已知一个满足 $l\prec x^{(0)}\prec u$、$Ax^{(0)}\succ0$ 的初始点 $x^{(0)}$。

**11.22 多面体内的最大体积矩形。** 考虑习题 8.16 中的问题，即求一个体积最大的矩形 $\mathcal{R}=\{x\mid l\preceq x\preceq u\}$，使它位于由一组线性不等式描述的多面体 $\mathcal{P}=\{x\mid Ax\preceq b\}$ 内。实现求解这个问题的障碍法。可以假设 $b\succ0$，这意味着：当 $l\prec0$ 和 $u\succ0$ 都足够接近零时，矩形 $\mathcal{R}$ 位于 $\mathcal{P}$ 内。

在几个简单例子上测试你的实现。求下列数据所定义的多面体内的最大体积矩形：

$$
A=\begin{bmatrix}
0&-1\\
2&-4\\
2&1\\
-4&4\\
-4&0
\end{bmatrix},\qquad b=\mathbf{1}.
$$

画出这个多面体，以及位于其中的最大体积矩形。

**11.23 两路划分问题的 SDP 界与启发式方法。** 本题考虑第 219 页介绍、习题 5.39 也讨论过的两路划分问题 (5.7)：

$$
\begin{aligned}
\text{最小化}\quad &x^TWx\\
\text{约束为}\quad &x_i^2=1,\quad i=1,\ldots,n,
\end{aligned}
\tag{11.65}
$$

其中变量为 $x\in\mathbf{R}^n$。不失一般性，假设 $W\in\mathbf{S}^n$ 满足 $W_{ii}=0$。将划分问题的最优值记为 $p^\star$，用 $x^\star$ 表示一个最优划分。（注意，$-x^\star$ 也是一个最优划分。）

两路划分问题 (11.65) 的拉格朗日对偶是 SDP

$$
\begin{aligned}
\text{最大化}\quad &-\mathbf{1}^T\nu\\
\text{约束为}\quad &W+\mathbf{diag}(\nu)\succeq0,
\end{aligned}
\tag{11.66}
$$

<!-- pdf-page: 644 -->

其中变量为 $\nu\in\mathbf{R}^n$。这个 SDP 的对偶为

$$
\begin{aligned}
\text{最小化}\quad &\mathbf{tr}(WX)\\
\text{约束为}\quad &X\succeq0\\
&X_{ii}=1,\quad i=1,\ldots,n,
\end{aligned}
\tag{11.67}
$$

其中变量为 $X\in\mathbf{S}^n$。（这个 SDP 可以解释为两路划分问题 (11.65) 的一个松弛；见习题 5.39。）这两个 SDP 的最优值相等，并给出最优值 $p^\star$ 的一个下界，将这个下界记为 $d^\star$。用 $\nu^\star$ 和 $X^\star$ 表示两个 SDP 的最优点。

- (a) 给定权重矩阵 $W$，实现求解 SDP (11.66) 及其对偶 (11.67) 的障碍法。说明如何得到近似最优的 $\nu$ 和 $X$，给出方法中所需的各个 Hessian 矩阵与梯度的公式，并说明如何计算牛顿步。在一些小规模问题实例上测试你的实现，将求得的界与最优值比较（检查全部 $2^n$ 种划分的目标值，就能求得最优值）。再随机选取一个规模足够大的问题实例，使得无法通过穷举搜索求得最优划分（例如 $n=100$），测试你的实现。

- (b) *一种划分启发式方法。* 在习题 5.39 中，你已经发现：如果 $X^\star$ 的秩为一，它必定具有 $X^\star=x^\star(x^\star)^T$ 的形式，其中 $x^\star$ 是两路划分问题的最优解。这启发了一种简单的方法，用来寻找一个好的划分，即使它未必是最优的：求解上面的 SDP，得到 $X^\star$ 及下界 $d^\star$。用 $v$ 表示 $X^\star$ 的最大特征值所对应的一个特征向量，并令 $\hat x=\mathbf{sign}(v)$。向量 $\hat x$ 就是我们对一个好划分的估计。

    在一些小规模问题实例，以及 (a) 中使用的大规模实例上试验这个启发式方法。将所得划分的目标值 $\hat x^TW\hat x$ 与下界 $d^\star$ 比较。

- (c) *随机化方法。* 已知 SDP (11.67) 的解 $X^\star$ 后，还可以用随机化技术寻找一个好的划分。方法很简单：从 $\mathbf{R}^n$ 上均值为零、协方差为 $X^\star$ 的正态分布中，生成独立样本 $x^{(1)},\ldots,x^{(K)}$。对每个样本，构造启发式近似解 $\hat x^{(k)}=\mathbf{sign}(x^{(k)})$。然后从这些解中选出最好的一个，即代价最小的一个。在一些小规模问题实例，以及 (a) 中考虑的大规模实例上试验这个过程。

- (d) *一种贪心启发式改进方法。* 假设已给定一个划分 $x$，即 $x_i\in\{-1,1\}$，$i=1,\ldots,n$。如果将元素 $i$ 从一个集合移到另一个集合，也就是把 $x_i$ 改为 $-x_i$，目标值会如何变化？现在考虑下面这个简单的贪心算法：给定初始划分 $x$，移动能使目标值下降最多的那个元素。反复执行这个过程，直到再也无法通过将一个元素从一个集合移到另一个集合来降低目标值。

    在一些问题实例上试验这个启发式方法，包括那个大规模实例。采用不同的初始划分，包括 $x=\mathbf{1}$、(b) 中得到的启发式近似解，以及 (c) 中随机生成的近似解。这种贪心改进能将 (b) 和 (c) 中的近似解改善多少？

**11.24 二次规划的障碍法与原始–对偶内点法。** 实现障碍法和原始–对偶法，求解下面的 QP（为简单起见，不含等式约束）：

$$
\begin{aligned}
\text{最小化}\quad &(1/2)x^TPx+q^Tx\\
\text{约束为}\quad &Ax\preceq b,
\end{aligned}
$$

其中 $A\in\mathbf{R}^{m\times n}$。可以假设已给定一个严格可行的初始点。在几个例子上测试你的代码。对于障碍法，画出对偶间隙随牛顿步数的变化。对于原始–对偶内点法，画出替代对偶间隙和对偶残差范数随迭代次数的变化。
