<!-- pdf-page: 365 -->

# 第 7 章 统计估计

<aside class="chapter-guide"><p>导读（编者）：本章把参数估计、分布估计和检测规则的选择写成优化问题，说明哪些模型可以用凸优化求解，随后讨论概率界和实验设计。阅读时需分清待估参数、观测数据和先验约束各自的角色，并留意概率模型的哪些性质保证了问题的凸性。</p></aside>

## 7.1 参数化分布估计

### 7.1.1 最大似然估计

考虑 $\mathbf{R}^m$ 上的一族概率分布，用向量 $x\in\mathbf{R}^n$ 标识，密度为 $p_x(\cdot)$。对固定的 $y\in\mathbf{R}^m$，将 $p_x(y)$ 看作 $x$ 的函数时，称其为**似然函数（likelihood function）**。使用它的对数更方便，称为**对数似然函数（log-likelihood function）**，记作 $l$：

$$
l(x)=\log p_x(y).
$$

参数 $x$ 的取值通常受到约束，这些约束可以表示关于 $x$ 的先验知识，也可以表示似然函数的定义域。可以显式给出这些约束，也可以将其纳入似然函数：只要 $x$ 不满足先验信息约束，就令 $p_x(y)=0$（对所有 $y$）。（因此，对于违反先验信息约束的参数 $x$，可将对数似然函数的值设为 $-\infty$。）

现在考虑如下问题：根据从该分布中观测到的一个样本 $y$，估计参数 $x$ 的值。一种广泛使用的方法称为**最大似然估计（maximum likelihood estimation，ML 估计）**，将 $x$ 估计为

$$
\widehat x_{\mathrm{ml}}=\operatorname{argmax}_x p_x(y)=\operatorname{argmax}_x l(x),
$$

即选择一个使观测值 $y$ 的似然函数（或对数似然函数）达到最大的参数值，作为估计值。如果有关于 $x$ 的先验信息，例如 $x\in C\subseteq\mathbf{R}^n$，可以显式加入约束 $x\in C$，也可以通过将 $x\notin C$ 时的 $p_x(y)$ 重新定义为零，隐式施加这一约束。

求参数向量 $x$ 的最大似然估计，可以表述为

$$
\begin{array}{ll}
\text{最大化} & l(x)=\log p_x(y)\\
\text{约束条件} & x\in C,
\end{array}
\tag{7.1}
$$

其中 $x\in C$ 表示参数向量 $x$ 的先验信息或其他约束。在这个优化问题中，向量 $x\in\mathbf{R}^n$（它是概率密度中的<!-- pdf-page: 366 -->参数）是变量，而向量 $y\in\mathbf{R}^m$（它是观测到的样本）是问题参数。

如果对于每个 $y$，对数似然函数 $l$ 都是凹函数，并且集合 $C$ 可以用一组线性等式约束和凸不等式约束描述，那么最大似然估计问题 (7.1) 就是凸优化问题。许多估计问题都满足这些条件。对于这类问题，可以用凸优化计算 ML 估计。

#### 带独立同分布噪声的线性测量

考虑线性测量模型

$$
y_i=a_i^Tx+v_i,\qquad i=1,\ldots,m,
$$

其中 $x\in\mathbf{R}^n$ 是待估参数向量，$y_i\in\mathbf{R}$ 是测量或观测到的量，$v_i$ 是测量误差或噪声。假设 $v_i$ 独立同分布（independent, identically distributed，IID），其在 $\mathbf{R}$ 上的密度为 $p$。于是似然函数为

$$
p_x(y)=\prod_{i=1}^m p(y_i-a_i^Tx),
$$

因此对数似然函数为

$$
l(x)=\log p_x(y)=\sum_{i=1}^m\log p(y_i-a_i^Tx).
$$

ML 估计就是问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum_{i=1}^m\log p(y_i-a_i^Tx),
\end{array}
\tag{7.2}
$$

的任意最优点，变量为 $x$。如果密度 $p$ 是对数凹的，那么这个问题是凸问题，并且具有罚函数逼近问题的形式（第 294 页的 (6.2)），罚函数为 $-\log p$。

<div class="example" markdown="1">

**例 7.1 几种常见噪声密度下的 ML 估计。**

- **高斯噪声。** 当 $v_i$ 服从均值为零、方差为 $\sigma^2$ 的高斯分布时，密度为 $p(z)=(2\pi\sigma^2)^{-1/2}e^{-z^2/2\sigma^2}$，对数似然函数为

    $$
    l(x)=-(m/2)\log(2\pi\sigma^2)-\frac{1}{2\sigma^2}\|Ax-y\|_2^2,
    $$

    其中矩阵 $A$ 的各行为 $a_1^T,\ldots,a_m^T$。因此，$x$ 的 ML 估计为 $x_{\mathrm{ml}}=\operatorname{argmin}_x\|Ax-y\|_2^2$，即一个最小二乘逼近问题的解。

- **Laplace 噪声。** 当 $v_i$ 服从 Laplace 分布，即密度为 $p(z)=(1/2a)e^{-|z|/a}$（其中 $a>0$）时，ML 估计为 $\widehat x=\operatorname{argmin}_x\|Ax-y\|_1$，即 $\ell_1$ 范数逼近问题的解。

- **均匀噪声。** 当 $v_i$ 在 $[-a,a]$ 上均匀分布时，在 $[-a,a]$ 上有 $p(z)=1/(2a)$，任意满足 $\|Ax-y\|_\infty\leq a$ 的 $x$ 都是一个 ML 估计。

</div>

<!-- pdf-page: 367 -->

#### 罚函数逼近的 ML 解释

反过来，任意罚函数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m\phi(b_i-a_i^Tx)
\end{array}
$$

都可以解释为一个最大似然估计问题，其噪声密度为

$$
p(z)=\frac{e^{-\phi(z)}}{\int e^{-\phi(u)}\,du},
$$

测量值为 $b$。这为罚函数逼近问题提供了统计解释。例如，假设罚函数 $\phi$ 在取值很大时增长得非常快，这意味着对较大的残差赋予很大的代价或惩罚。对应的噪声密度函数 $p$ 的尾部会很小，而 ML 估计量会尽可能避免产生任何较大残差的估计，因为这些残差对应于极不可能发生的事件。

也可以从最大似然估计的角度，理解 $\ell_1$ 范数逼近对大误差的鲁棒性。将 $\ell_1$ 范数逼近解释为噪声密度为 Laplace 密度的最大似然估计；$\ell_2$ 范数逼近则是噪声密度为高斯密度的最大似然估计。Laplace 密度的尾部比高斯密度更大，也就是说，$v_i$ 取很大值的概率，在 Laplace 密度下远高于高斯密度。因此，相应的最大似然方法预期会出现更多较大的残差。

#### 服从 Poisson 分布的计数问题

在许多不同的问题中，随机变量 $y$ 取非负整数值，服从均值为 $\mu>0$ 的 Poisson 分布：

$$
\mathbf{prob}(y=k)=\frac{e^{-\mu}\mu^k}{k!}.
$$

$y$ 通常表示一个 Poisson 过程在某段时间内发生的事件次数或数量，例如光子到达次数、交通事故数等。

在一个简单的统计模型中，将均值 $\mu$ 建模为向量 $u\in\mathbf{R}^n$ 的仿射函数：

$$
\mu=a^Tu+b.
$$

这里，$u$ 称为**解释变量（explanatory variables）**向量，向量 $a\in\mathbf{R}^n$ 和数 $b\in\mathbf{R}$ 称为**模型参数**。例如，如果 $y$ 是某地区在某段时间内发生的交通事故数，那么 $u_1$ 可以是该时段通过该地区的总交通流量，$u_2$ 可以是该地区在该时段的降雨量，等等。

给定若干观测，它们由数对 $(u_i,y_i)$，$i=1,\ldots,m$ 组成，其中 $y_i$ 是解释变量取值为 $u_i\in\mathbf{R}^n$ 时观测到的 $y$ 值。我们的任务是根据这些数据，求模型参数 $a\in\mathbf{R}^n$ 和 $b\in\mathbf{R}$ 的最大似然估计。

<!-- pdf-page: 368 -->

似然函数具有如下形式：

$$
\prod_{i=1}^m\frac{(a^Tu_i+b)^{y_i}\exp(-(a^Tu_i+b))}{y_i!},
$$

因此，对数似然函数为

$$
l(a,b)=\sum_{i=1}^m\bigl(y_i\log(a^Tu_i+b)-(a^Tu_i+b)-\log(y_i!)\bigr).
$$

求解凸优化问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum_{i=1}^m\bigl(y_i\log(a^Tu_i+b)-(a^Tu_i+b)\bigr),
\end{array}
$$

就可以得到 $a$ 和 $b$ 的 ML 估计，其中变量为 $a$ 和 $b$。

#### logistic 回归

考虑随机变量 $y\in\{0,1\}$，满足

$$
\mathbf{prob}(y=1)=p,\qquad\mathbf{prob}(y=0)=1-p,
$$

其中 $p\in[0,1]$，并假设它依赖于解释变量向量 $u\in\mathbf{R}^n$。例如，$y=1$ 可以表示某个人群中的个体患上某种疾病。患病概率为 $p$，将其建模为若干解释变量 $u$ 的函数；这些变量可以表示体重、年龄、身高、血压及其他医学相关变量。

**logistic 模型**具有如下形式：

$$
p=\frac{\exp(a^Tu+b)}{1+\exp(a^Tu+b)},
\tag{7.3}
$$

其中 $a\in\mathbf{R}^n$ 和 $b\in\mathbf{R}$ 是模型参数，它们决定了概率 $p$ 如何随解释变量 $u$ 变化。

现在假设给定一组数据，由解释变量的取值 $u_1,\ldots,u_m\in\mathbf{R}^n$ 及相应的结果 $y_1,\ldots,y_m\in\{0,1\}$ 组成。我们的任务是求模型参数 $a\in\mathbf{R}^n$ 和 $b\in\mathbf{R}$ 的最大似然估计。求 $a$ 和 $b$ 的 ML 估计，有时称为 **logistic 回归**。

可以重新排列数据，使得 $u_1,\ldots,u_q$ 对应的结果为 $y=1$，而 $u_{q+1},\ldots,u_m$ 对应的结果为 $y=0$。于是似然函数具有如下形式：

$$
\prod_{i=1}^q p_i\prod_{i=q+1}^m(1-p_i),
$$

其中 $p_i$ 由解释变量取值为 $u_i$ 时的 logistic 模型给出。对数似然函数为

$$
l(a,b)=\sum_{i=1}^q\log p_i+\sum_{i=q+1}^m\log(1-p_i)
$$

<!-- pdf-page: 369 -->

<figure id="fig-7-1" data-figure="7.1" data-no-english-text="true" data-reader-after="logistic-likelihood-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-1.png" alt="logistic 回归示意图：圆圈分布在结果为零和一的两排，实线概率曲线随解释变量 u 增大而从接近零上升到接近一" data-source-page="369" data-source-rect="160,122,395,303.5">
<figcaption>图 7.1 <em>logistic 回归。</em>圆圈表示 50 个点 $(u_i,y_i)$，其中 $u_i\in\mathbf{R}$ 是解释变量，$y_i\in\{0,1\}$ 是结果。数据表明，当 $u$ 大致小于 5 时，结果更可能是 $y=0$；当 $u$ 大致大于 5 时，结果更可能是 $y=1$。数据还表明，当 $u$ 大致小于 2 时，结果以很高的概率为 $y=0$；当 $u$ 大致大于 8 时，结果以很高的概率为 $y=1$。实线曲线表示取最大似然参数 $a,b$ 时的 $\mathbf{prob}(y=1)=\exp(au+b)/(1+\exp(au+b))$。这个最大似然模型与我们对数据集的直观观察一致。</figcaption>
</figure>

$$
\begin{aligned}
&=\sum_{i=1}^q\log\frac{\exp(a^Tu_i+b)}{1+\exp(a^Tu_i+b)}+\sum_{i=q+1}^m\log\frac{1}{1+\exp(a^Tu_i+b)}\\
&=\sum_{i=1}^q(a^Tu_i+b)-\sum_{i=1}^m\log(1+\exp(a^Tu_i+b)).
\end{aligned}
$$

<p id="logistic-likelihood-end" markdown="1">由于 $l$ 是 $a$ 和 $b$ 的凹函数，logistic 回归问题可以作为凸优化问题求解。图 7.1 给出了 $u\in\mathbf{R}$ 时的一个例子。</p>

#### 高斯变量的协方差估计

假设 $y\in\mathbf{R}^n$ 是均值为零、协方差矩阵为 $R=\mathbf{E}\,yy^T$ 的高斯随机变量，其密度为

$$
p_R(y)=(2\pi)^{-n/2}\det(R)^{-1/2}\exp(-y^TR^{-1}y/2),
$$

其中 $R\in\mathbf{S}_{++}^n$。我们希望根据从该分布中抽取的 $N$ 个独立样本 $y_1,\ldots,y_N\in\mathbf{R}^n$，并利用关于 $R$ 的先验知识，估计协方差矩阵 $R$。

对数似然函数具有如下形式：

$$
l(R)=\log p_R(y_1,\ldots,y_N)
$$

<!-- pdf-page: 370 -->

$$
\begin{aligned}
&=-(Nn/2)\log(2\pi)-(N/2)\log\det R-(1/2)\sum_{k=1}^N y_k^TR^{-1}y_k\\
&=-(Nn/2)\log(2\pi)-(N/2)\log\det R-(N/2)\operatorname{\mathbf{tr}}(R^{-1}Y),
\end{aligned}
$$

其中

$$
Y=\frac{1}{N}\sum_{k=1}^N y_ky_k^T
$$

是 $y_1,\ldots,y_N$ 的**样本协方差**。这个对数似然函数不是 $R$ 的凹函数（不过，它在定义域 $\mathbf{S}_{++}^n$ 的某个子集上是凹的；见习题 7.4），但通过变量替换可以得到凹的对数似然函数。用 $S$ 表示协方差矩阵的逆，即 $S=R^{-1}$（称为**信息矩阵**）。用 $S$ 代替 $R$ 作为新参数，对数似然函数成为

$$
l(S)=-(Nn/2)\log(2\pi)+(N/2)\log\det S-(N/2)\operatorname{\mathbf{tr}}(SY),
$$

它是 $S$ 的凹函数。

因此，求解问题

$$
\begin{array}{ll}
\text{最大化} & \log\det S-\operatorname{\mathbf{tr}}(SY)\\
\text{约束条件} & S\in\mathcal{S}
\end{array}
\tag{7.4}
$$

就可以得到 $S$（进而得到 $R$）的 ML 估计，其中 $\mathcal{S}$ 表示我们关于 $S=R^{-1}$ 的先验知识。（还有隐式约束 $S\in\mathbf{S}_{++}^n$。）由于目标函数是凹函数，如果集合 $\mathcal{S}$ 可以用一组线性等式约束和凸不等式约束描述，那么这个问题就是凸问题。

先考察除了 $R\succ0$ 以外，不对 $R$（因而也不对 $S$）作任何先验假设的情形。这时，问题 (7.4) 可以解析求解。目标函数的梯度为 $S^{-1}-Y$，所以如果 $Y\in\mathbf{S}_{++}^n$，最优的 $S$ 满足 $S^{-1}=Y$。（如果 $Y\notin\mathbf{S}_{++}^n$，对数似然函数无上界。）因此，当没有关于 $R$ 的先验假设时，协方差的最大似然估计就是样本协方差：$\widehat R_{\mathrm{ml}}=Y$。

现在考虑一些关于 $R$ 的约束，它们可以表述为信息矩阵 $S$ 的凸约束。对于形如

$$
L\preceq R\preceq U,
$$

的 $R$ 的矩阵下界和上界，其中 $L$ 和 $U$ 是对称正定矩阵，可以写成

$$
U^{-1}\preceq R^{-1}\preceq L^{-1}.
$$

$R$ 的条件数约束

$$
\lambda_{\max}(R)\leq\kappa_{\max}\lambda_{\min}(R),
$$

可以写成

$$
\lambda_{\max}(S)\leq\kappa_{\max}\lambda_{\min}(S).
$$

<!-- pdf-page: 371 -->

这等价于存在 $u>0$，使得 $uI\preceq S\preceq\kappa_{\max}uI$。因此，求解凸问题

$$
\begin{array}{ll}
\text{最大化} & \log\det S-\operatorname{\mathbf{tr}}(SY)\\
\text{约束条件} & uI\preceq S\preceq\kappa_{\max}uI
\end{array}
\tag{7.5}
$$

就可以求解带有 $R$ 的条件数约束的 ML 问题，其中变量为 $S\in\mathbf{S}^n$ 和 $u\in\mathbf{R}$。

再举一个例子。假设给定随机向量 $y$ 的若干线性函数的方差界：

$$
\mathbf{E}(c_i^Ty)^2\leq\alpha_i,\qquad i=1,\ldots,K.
$$

这些先验假设可以写成

$$
\mathbf{E}(c_i^Ty)^2=c_i^TRc_i=c_i^TS^{-1}c_i\leq\alpha_i,\qquad i=1,\ldots,K.
$$

由于 $c_i^TS^{-1}c_i$ 是 $S$ 的凸函数（条件是 $S\succ0$，这里满足该条件），这些界可以作为约束加入 ML 问题。

### 7.1.2 最大后验概率估计

**最大后验概率估计（maximum a posteriori probability estimation，MAP 估计）**可以看作最大似然估计的贝叶斯形式，为待估参数 $x$ 指定一个先验概率密度。假设 $x$（待估向量）和 $y$（观测量）都是随机变量，具有联合概率密度 $p(x,y)$。这与前面的统计估计设定不同，在前面的设定中，$x$ 是参数而不是随机变量。

$x$ 的**先验密度**为

$$
p_x(x)=\int p(x,y)\,dy.
$$

这个密度表示在观测向量 $y$ 之前，关于向量 $x$ 可能取哪些值的先验信息。类似地，$y$ 的先验密度为

$$
p_y(y)=\int p(x,y)\,dx.
$$

这个密度表示关于测量或观测向量 $y$ 将会取哪些值的先验信息。

给定 $x$ 时，$y$ 的条件密度为

$$
p_{y\mid x}(x,y)=\frac{p(x,y)}{p_x(x)}.
$$

在 MAP 估计方法中，$p_{y\mid x}$ 所起的作用，与最大似然估计设定中依赖参数的密度 $p_x$ 相同。给定 $y$ 时，$x$ 的条件密度为

$$
p_{x\mid y}(x,y)=\frac{p(x,y)}{p_y(y)}=p_{y\mid x}(x,y)\frac{p_x(x)}{p_y(y)}.
$$

<!-- pdf-page: 372 -->

将观测值 $y$ 代入 $p_{x\mid y}$，就得到 $x$ 的**后验密度**。它表示观测之后我们对 $x$ 的了解。

在 MAP 估计方法中，给定观测 $y$，对 $x$ 的估计为

$$
\begin{aligned}
\widehat x_{\mathrm{map}}&=\operatorname{argmax}_x p_{x\mid y}(x,y)\\
&=\operatorname{argmax}_x p_{y\mid x}(x,y)p_x(x)\\
&=\operatorname{argmax}_x p(x,y).
\end{aligned}
$$

换言之，给定观测值 $y$ 后，我们取使 $x$ 的条件密度最大的值作为 $x$ 的估计。这个估计与最大似然估计的唯一区别，是这里出现的第二个因子 $p_x(x)$。可以将这个因子解释为对 $x$ 的先验知识的考虑。注意，如果 $x$ 的先验密度在集合 $C$ 上均匀分布，那么求 MAP 估计就等同于在约束 $x\in C$ 下最大化似然函数，也就是 ML 估计问题 (7.1)。

取对数后，MAP 估计可以写成

$$
\widehat x_{\mathrm{map}}=\operatorname{argmax}_x\bigl(\log p_{y\mid x}(x,y)+\log p_x(x)\bigr).
\tag{7.6}
$$

第一项实质上与对数似然函数相同；第二项则惩罚那些根据先验密度不太可能出现的 $x$ 值（即 $p_x(x)$ 很小的 $x$）。

暂且不讨论两种设定在哲学观点上的差异，通过 (7.6) 求 MAP 估计与通过 (7.1) 求 ML 估计，唯一区别在于优化问题中多了一项，它与 $x$ 的先验密度有关。因此，对于任何对数似然函数为凹函数的最大似然估计问题，都可以为 $x$ 加入一个对数凹的先验密度，得到的 MAP 估计问题仍然是凸问题。

#### 带独立同分布噪声的线性测量

假设 $x\in\mathbf{R}^n$ 和 $y\in\mathbf{R}^m$ 满足关系

$$
y_i=a_i^Tx+v_i,\qquad i=1,\ldots,m,
$$

其中 $v_i$ 独立同分布，在 $\mathbf{R}$ 上的密度为 $p_v$，而 $x$ 在 $\mathbf{R}^n$ 上的先验密度为 $p_x$。于是 $x$ 和 $y$ 的联合密度为

$$
p(x,y)=p_x(x)\prod_{i=1}^m p_v(y_i-a_i^Tx),
$$

求解优化问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\log p_x(x)+\sum_{i=1}^m\log p_v(y_i-a_i^Tx).
\end{array}
\tag{7.7}
$$

就可以得到 MAP 估计。

如果 $p_x$ 和 $p_v$ 都是对数凹的，这个问题就是凸问题。MAP 估计问题 (7.7) 与相应的 ML 估计问题 (7.2) 之间，唯一区别是多了一项 $\log p_x(x)$。

<!-- pdf-page: 373 -->

例如，如果 $v_i$ 在 $[-a,a]$ 上均匀分布，而 $x$ 的先验分布是均值为 $\bar x$、协方差为 $\Sigma$ 的高斯分布，那么求解二次规划

$$
\begin{array}{ll}
\text{最小化} & (x-\bar x)^T\Sigma^{-1}(x-\bar x)\\
\text{约束条件} & \|Ax-y\|_\infty\leq a,
\end{array}
$$

就可以得到 MAP 估计，其中变量为 $x$。

#### 精确线性测量下的 MAP 估计

假设 $x\in\mathbf{R}^n$ 是待估参数向量，先验密度为 $p_x$。有 $m$ 个精确的（无噪声、确定性的）线性测量，由 $y=Ax$ 给出。换言之，给定 $x$ 时，$y$ 的条件分布是集中在点 $Ax$ 上、质量为一的点质量分布。求解问题

$$
\begin{array}{ll}
\text{最大化} & \log p_x(x)\\
\text{约束条件} & Ax=y.
\end{array}
$$

就可以得到 MAP 估计。如果 $p_x$ 是对数凹的，这个问题就是凸问题。

如果在先验分布下，参数 $x_i$ 独立同分布，在 $\mathbf{R}$ 上的密度为 $p$，那么 MAP 估计问题具有如下形式：

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum_{i=1}^n\log p(x_i)\\
\text{约束条件} & Ax=y,
\end{array}
$$

这是一个最小惩罚问题（第 304 页的 (6.6)），罚函数为 $\phi(u)=-\log p(u)$。

反过来，任意最小惩罚问题

$$
\begin{array}{ll}
\text{最小化} & \phi(x_1)+\cdots+\phi(x_n)\\
\text{约束条件} & Ax=b
\end{array}
$$

都可以解释为 MAP 估计问题，其中有 $m$ 个精确线性测量（即 $Ax=b$），且 $x_i$ 独立同分布，密度为

$$
p(z)=\frac{e^{-\phi(z)}}{\int e^{-\phi(u)}\,du}.
$$

## 7.2 非参数分布估计

考虑随机变量 $X$，其取值属于有限集合 $\{\alpha_1,\ldots,\alpha_n\}\subseteq\mathbf{R}$。（为简单起见，假设取值位于 $\mathbf{R}$ 中；同样的思路也适用于取值位于例如 $\mathbf{R}^k$ 中的情形。）$X$ 的分布由 $p\in\mathbf{R}^n$ 刻画，其中 $\mathbf{prob}(X=\alpha_k)=p_k$。显然，$p$ 满足 $p\succeq0$、$\mathbf{1}^Tp=1$。反过来，如果 $p\in\mathbf{R}^n$ 满足 $p\succeq0$、$\mathbf{1}^Tp=1$，那么它就通过 $\mathbf{prob}(X=\alpha_k)=p_k$ 定义了随机变量 $X$ 的一个概率分布。因此，概率单纯形

$$
\{p\in\mathbf{R}^n\mid p\succeq0,\ \mathbf{1}^Tp=1\}
$$

<!-- pdf-page: 374 -->

与取值属于 $\{\alpha_1,\ldots,\alpha_n\}$ 的随机变量 $X$ 的所有可能概率分布一一对应。

本节讨论如何结合先验信息以及可能获得的观测和测量，估计分布 $p$。

### 先验信息

关于 $p$ 的许多类先验信息，都可以用线性等式约束或不等式约束表示。若 $f:\mathbf{R}\to\mathbf{R}$ 是任意函数，则

$$
\mathbf{E}\,f(X)=\sum_{i=1}^n p_if(\alpha_i)
$$

是 $p$ 的线性函数。作为一个特例，若 $C\subseteq\mathbf{R}$，则 $\mathbf{prob}(X\in C)$ 是 $p$ 的线性函数：

$$
\mathbf{prob}(X\in C)=c^Tp,\qquad
c_i=\begin{cases}1&\alpha_i\in C\\0&\alpha_i\notin C.\end{cases}
$$

因此，某些函数的已知期望值（例如矩），或某些集合的已知概率，可以作为关于 $p\in\mathbf{R}^n$ 的线性等式约束加入问题。期望值或概率所满足的不等式，可以表示为关于 $p\in\mathbf{R}^n$ 的线性不等式。

例如，假设已知 $X$ 的均值为 $\mathbf{E}\,X=\alpha$，二阶矩为 $\mathbf{E}\,X^2=\beta$，且 $\mathbf{prob}(X\geq0)\leq0.3$。这些先验信息可以写成

$$
\mathbf{E}\,X=\sum_{i=1}^n\alpha_ip_i=\alpha,\qquad
\mathbf{E}\,X^2=\sum_{i=1}^n\alpha_i^2p_i=\beta,\qquad
\sum_{\alpha_i\geq0}p_i\leq0.3,
$$

即关于 $p$ 的两个线性等式和一个线性不等式。

还可以加入一些涉及 $p$ 的非线性函数的先验约束。例如，$X$ 的方差为

$$
\mathbf{var}(X)=\mathbf{E}\,X^2-(\mathbf{E}\,X)^2
=\sum_{i=1}^n\alpha_i^2p_i-\left(\sum_{i=1}^n\alpha_ip_i\right)^2.
$$

第一项是 $p$ 的线性函数，第二项是 $p$ 的凹二次函数，所以 $X$ 的方差是 $p$ 的凹函数。因此，$X$ 的方差下界可以表示为关于 $p$ 的凸二次不等式。

再举一个例子。假设 $A$ 和 $B$ 是 $\mathbf{R}$ 的子集，考虑给定 $B$ 时 $A$ 的条件概率：

$$
\mathbf{prob}(X\in A\mid X\in B)
=\frac{\mathbf{prob}(X\in A\cap B)}{\mathbf{prob}(X\in B)}.
$$

这个函数是 $p\in\mathbf{R}^n$ 的线性分式函数，可以写为

$$
\mathbf{prob}(X\in A\mid X\in B)=c^Tp/d^Tp,
$$

其中

$$
c_i=\begin{cases}1&\alpha_i\in A\cap B\\0&\alpha_i\notin A\cap B,\end{cases}
\qquad
d_i=\begin{cases}1&\alpha_i\in B\\0&\alpha_i\notin B.\end{cases}
$$

<!-- pdf-page: 375 -->

因此，可以将先验约束

$$
l\leq\mathbf{prob}(X\in A\mid X\in B)\leq u
$$

写成关于 $p$ 的线性不等式约束

$$
ld^Tp\leq c^Tp\leq ud^Tp.
$$

其他几类先验信息可以用非线性凸不等式表示。例如，$X$ 的熵为

$$
-\sum_{i=1}^n p_i\log p_i,
$$

它是 $p$ 的凹函数，因此可以通过关于 $p$ 的凸不等式，规定熵的最小值。如果 $q$ 表示另一个分布，即 $q\succeq0$、$\mathbf{1}^Tq=1$，那么分布 $q$ 与分布 $p$ 之间的 Kullback–Leibler 散度为

$$
\sum_{i=1}^n p_i\log(p_i/q_i),
$$

它关于 $p$ 是凸的（关于 $q$ 也凸；见第 90 页的例 3.19）。因此，可以通过关于 $p$ 的凸不等式，规定 $p$ 与一个给定分布 $q$ 之间 Kullback–Leibler 散度的最大值。

在接下来的几段中，将关于分布 $p$ 的先验信息写作 $p\in\mathcal{P}$。假设 $\mathcal{P}$ 可以用一组线性等式和凸不等式描述。在先验信息 $\mathcal{P}$ 中，也包含基本约束 $p\succeq0$、$\mathbf{1}^Tp=1$。

### 概率和期望值的界

给定关于分布的先验信息，例如 $p\in\mathcal{P}$，可以计算函数期望值或集合概率的上界、下界。例如，要在所有满足先验信息 $p\in\mathcal{P}$ 的分布中，确定 $\mathbf{E}\,f(X)$ 的下界，可求解凸问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n f(\alpha_i)p_i\\
\text{约束条件} & p\in\mathcal{P}.
\end{array}
$$

### 最大似然估计

可以根据从该分布获得的观测，使用最大似然估计来估计 $p$。假设从该分布中观测到 $N$ 个独立样本 $x_1,\ldots,x_N$。用 $k_i$ 表示这些样本中取值为 $\alpha_i$ 的个数，因此 $k_1+\cdots+k_n=N$，即观测样本的总数。于是，对数似然函数为

$$
l(p)=\sum_{i=1}^n k_i\log p_i,
$$

<!-- pdf-page: 376 -->

它是 $p$ 的凹函数。求解凸问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle l(p)=\sum_{i=1}^n k_i\log p_i\\
\text{约束条件} & p\in\mathcal{P},
\end{array}
$$

就可以得到 $p$ 的最大似然估计，其中变量为 $p$。

### 最大熵

求解凸问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n p_i\log p_i\\
\text{约束条件} & p\in\mathcal{P}.
\end{array}
$$

就可以得到与先验假设一致的最大熵分布。这种方法的支持者将最大熵分布描述为：在与先验信息一致的所有分布中，不确定性最大或随机性最强的分布。

### 最小 Kullback–Leibler 散度

求解凸问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n p_i\log(p_i/q_i)\\
\text{约束条件} & p\in\mathcal{P},
\end{array}
$$

就可以在所有与先验信息一致的分布中，找到与给定先验分布 $q$ 的 Kullback–Leibler 散度最小的分布 $p$。

注意，当先验分布为均匀分布，即 $q=(1/n)\mathbf{1}$ 时，这个问题就化为最大熵问题。

<div class="example" id="example-7-2" markdown="1">

**例 7.2** 考虑区间 $[-1,1]$ 内 $100$ 个等距点 $\alpha_i$ 上的概率分布。施加如下先验假设：

$$
\begin{aligned}
\mathbf{E}\,X&\in[-0.1,0.1]\\
\mathbf{E}\,X^2&\in[0.5,0.6]\\
\mathbf{E}(3X^3-2X)&\in[-0.3,-0.2]\\
\mathbf{prob}(X<0)&\in[0.3,0.4].
\end{aligned}
\tag{7.8}
$$

这些约束与 $\mathbf{1}^Tp=1$、$p\succeq0$ 一起，描述了一个由概率分布组成的多面体。

图 7.2 给出了满足这些约束的最大熵分布。该最大熵分布满足

$$
\begin{aligned}
\mathbf{E}\,X&=0.056\\
\mathbf{E}\,X^2&=0.5\\
\mathbf{E}(3X^3-2X)&=-0.2\\
\mathbf{prob}(X<0)&=0.4.
\end{aligned}
$$

<p id="cdf-bound-start" markdown="1">为了说明如何求概率界，计算累积分布 $\mathbf{prob}(X\leq\alpha_i)$，$i=1,\ldots,100$ 的上界和下界。对于每个 $i$，</p>

<!-- pdf-page: 377 -->

<figure id="fig-7-2" data-figure="7.2" data-no-english-text="true" data-reader-after="cdf-bound-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-2.png" alt="满足给定约束的最大熵离散分布，横轴为各取值 αᵢ，纵轴为相应概率 pᵢ；阶梯曲线先下降，再上升后略微回落" data-source-page="377" data-source-rect="154,122,394,303">
<figcaption>图 7.2 满足约束 (7.8) 的最大熵分布。</figcaption>
</figure>

<p id="cdf-bound-end" markdown="1" data-reader-continue="cdf-bound-start">求解两个线性规划：在所有满足先验假设 (7.8) 的分布中，一个最大化 $\mathbf{prob}(X\leq\alpha_i)$，另一个最小化 $\mathbf{prob}(X\leq\alpha_i)$。结果如图 7.3 所示。上、下两条曲线分别表示上界和下界；中间的曲线表示最大熵分布的累积分布。</p>

</div>

<div class="example" markdown="1">

**例 7.3 已知边缘分布时求风险概率的界。** 假设 $X$ 和 $Y$ 是两个随机变量，分别表示两项投资的收益。假设 $X$ 的取值属于 $\{\alpha_1,\ldots,\alpha_n\}\subseteq\mathbf{R}$，$Y$ 的取值属于 $\{\beta_1,\ldots,\beta_m\}\subseteq\mathbf{R}$，且 $p_{ij}=\mathbf{prob}(X=\alpha_i,Y=\beta_j)$。两项收益 $X$ 和 $Y$ 的边缘分布已知，即

$$
\sum_{j=1}^m p_{ij}=r_i,\quad i=1,\ldots,n,\qquad
\sum_{i=1}^n p_{ij}=q_j,\quad j=1,\ldots,m,
\tag{7.9}
$$

但除此之外，对联合分布 $p$ 一无所知。这就定义了一个由所有与给定边缘分布一致的联合分布组成的多面体。

现在假设同时进行这两项投资，因此总收益为随机变量 $X+Y$。我们希望计算损失达到某种程度或收益偏低的概率上界，即 $\mathbf{prob}(X+Y<\gamma)$ 的上界。求解线性规划

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum\{p_{ij}\mid\alpha_i+\beta_j<\gamma\}\\
\text{约束条件} & (7.9),\quad p_{ij}\geq0,\quad i=1,\ldots,n,\quad j=1,\ldots,m.
\end{array}
$$

就可以计算这个概率的紧上界。这个线性规划的最优值是损失概率的最大值。最优解 $p^\star$ 是与给定边缘分布一致、并使损失概率最大的联合分布。

<p id="derivative-risk-start" markdown="1">同样的方法也可以用于这两项投资的衍生产品。设 $R(X,Y)$ 为该衍生产品的收益，其中 $R:\mathbf{R}^2\to\mathbf{R}$。我们可以计算 $\mathbf{prob}(R<\gamma)$ 的紧下界</p>

<!-- pdf-page: 378 -->

<figure id="fig-7-3" data-figure="7.3" data-no-english-text="true" data-reader-owner="example-7-2">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-3.png" alt="三条累积分布阶梯曲线：上、下两条为给定约束下累积概率的最大值和最小值，中间一条为最大熵分布的累积分布函数" data-source-page="378" data-source-rect="211,122,448,304">
<figcaption>图 7.3 在所有满足 (7.8) 的分布中，最上方和最下方的曲线分别给出累积分布函数 $\mathbf{prob}(X\leq\alpha_i)$ 的最大可能值和最小可能值。中间的曲线是满足 (7.8) 的最大熵分布的累积分布函数。</figcaption>
</figure>

<p id="derivative-risk-end" markdown="1" data-reader-continue="derivative-risk-start">和上界，为此只需求解一个类似的线性规划，其目标函数为</p>

$$
\sum\{p_{ij}\mid R(\alpha_i,\beta_j)<\gamma\},
$$

分别最小化和最大化这个目标函数即可。

</div>

## 7.3 最优检测器设计与假设检验

假设 $X$ 是取值属于 $\{1,\ldots,n\}$ 的随机变量，其分布依赖于参数 $\theta\in\{1,\ldots,m\}$。对应于 $\theta$ 的 $m$ 个可能取值，$X$ 的各个分布可以用矩阵 $P\in\mathbf{R}^{n\times m}$ 表示，其元素为

$$
p_{kj}=\mathbf{prob}(X=k\mid\theta=j).
$$

$P$ 的第 $j$ 列给出与参数值 $\theta=j$ 对应的概率分布。

考虑根据观测到的 $X$ 的一个样本，估计 $\theta$ 的问题。换言之，样本 $X$ 是从 $m$ 个可能分布之一生成的，我们要猜测是哪个分布。$\theta$ 的 $m$ 个取值称为**假设**，猜测哪个假设正确（即哪个分布生成了观测样本 $X$）称为**假设检验**。在许多情况下，一个假设对应于某种正常情况，而其他各个假设分别对应于某种异常事件。这时，假设检验可以解释为观测<!-- pdf-page: 379 -->$X$ 的一个取值，然后猜测是否发生了异常事件；若发生了，则猜测是哪一种。因此，假设检验也称为**检测**。

大多数情况下，假设的顺序没有意义；它们只是 $m$ 个不同的假设，任意标记为 $\theta=1,\ldots,m$。用 $\widehat\theta$ 表示 $\theta$ 的估计，若 $\widehat\theta=\theta$，就正确猜中了参数值 $\theta$。若 $\widehat\theta\ne\theta$，就猜错了参数值 $\theta$，把它误判成了 $\widehat\theta$。在另一些情况下，假设的顺序有意义。这时，像 $\widehat\theta>\theta$ 这样的事件，即高估 $\theta$ 的事件，就有具体含义。

也可以用 $\{1,\ldots,m\}$ 以外的取值来表示参数 $\theta$，例如 $\theta\in\{\theta_1,\ldots,\theta_m\}$，其中 $\theta_i$ 是互不相同的值。这些值可以是实数，也可以是向量，例如用于指定第 $k$ 个分布的均值和方差。这时，像 $\|\widehat\theta-\theta\|$ 这样的量，也就是参数估计误差的范数，就有意义。

### 7.3.1 确定性检测器与随机化检测器

一个（确定性）**估计器**或**检测器**，是从 $\{1,\ldots,n\}$（可能观测值的集合）到 $\{1,\ldots,m\}$（假设的集合）的函数 $\psi$。如果观测到 $X$ 的值为 $k$，则我们对 $\theta$ 的猜测为 $\widehat\theta=\psi(k)$。一种显而易见的确定性检测器是**最大似然检测器**，定义为

$$
\widehat\theta=\psi_{\mathrm{ml}}(k)=\operatorname{argmax}_j p_{kj}.
\tag{7.10}
$$

当观测到 $X=k$ 时，$\theta$ 的最大似然估计是在所有可能分布中，使观测到 $X=k$ 的概率最大的那个参数值。

下面考虑确定性检测器的一种推广：给定 $X$ 的观测值，对 $\theta$ 的估计仍是随机的。$\theta$ 的**随机化检测器**是一个随机变量 $\widehat\theta\in\{1,\ldots,m\}$，其分布依赖于 $X$ 的观测值。随机化检测器可以用矩阵 $T\in\mathbf{R}^{m\times n}$ 定义，其元素为

$$
t_{ik}=\mathbf{prob}(\widehat\theta=i\mid X=k).
$$

其含义如下：如果观测到 $X=k$，检测器就以概率 $t_{ik}$ 给出 $\widehat\theta=i$。将 $T$ 的第 $k$ 列记作 $t_k$，它给出观测到 $X=k$ 时 $\widehat\theta$ 的概率分布。如果 $T$ 的每一列都是一个单位向量，那么这个随机化检测器就是确定性检测器，也就是说，$\widehat\theta$ 是 $X$ 的观测值的一个确定性函数。

乍看起来，在估计或检测过程中有意加入额外的随机化，似乎只会使估计器的性能变差。但下面会看到，在某些例子中，随机化检测器的性能优于所有确定性估计器。

我们要设计定义随机化检测器的矩阵 $T$。显然，$T$ 的各列 $t_k$ 必须满足以下线性等式和不等式约束：

$$
t_k\succeq0,\qquad\mathbf{1}^Tt_k=1.
\tag{7.11}
$$

<!-- pdf-page: 380 -->

### 7.3.2 检测概率矩阵

对于由矩阵 $T$ 定义的随机化检测器，定义**检测概率矩阵**为 $D=TP$。有

$$
D_{ij}=(TP)_{ij}=\mathbf{prob}(\widehat\theta=i\mid\theta=j),
$$

因此，$D_{ij}$ 是实际为 $\theta=j$ 时猜测 $\widehat\theta=i$ 的概率。$m\times m$ 检测概率矩阵 $D$ 刻画了由 $T$ 定义的随机化检测器的性能。对角元素 $D_{ii}$ 是 $\theta=i$ 时猜测 $\widehat\theta=i$ 的概率，即正确检测出 $\theta=i$ 的概率。非对角元素 $D_{ij}$（$i\ne j$）是将实际的 $\theta=j$ 误判为 $\theta=i$ 的概率，也就是实际为 $\theta=j$ 时，我们猜测 $\widehat\theta=i$ 的概率。如果 $D=I$，检测器就是完美的：无论参数 $\theta$ 是什么，都能正确猜出 $\widehat\theta=\theta$。

将 $D$ 的对角元素排列成向量，称为**检测概率**，记作 $P^{\mathrm{d}}$：

$$
P_i^{\mathrm{d}}=D_{ii}=\mathbf{prob}(\widehat\theta=i\mid\theta=i).
$$

**错误概率**是它们的补，记作 $P^{\mathrm{e}}$：

$$
P_i^{\mathrm{e}}=1-D_{ii}=\mathbf{prob}(\widehat\theta\ne i\mid\theta=i).
$$

由于检测概率矩阵 $D$ 每一列的元素之和为一，错误概率可以写成

$$
P_i^{\mathrm{e}}=\sum_{j\ne i}D_{ji}.
$$

### 7.3.3 最优检测器设计

本节说明，检测器设计中的许多目标，都是 $D$ 的线性函数、仿射函数或分段线性凸函数，因此也是 $T$（优化变量）的这类函数。同样，检测器设计中的多种约束，都可以用关于 $D$ 的线性不等式表示。因此，许多不同的最优检测器设计问题都可以表述为线性规划。在 §7.3.4 中会看到，这些线性规划中的某些问题有简单的解；本节只讨论如何表述这些问题。

#### 错误概率和检测概率的限制

可以规定正确检测出第 $j$ 个假设的概率下界：

$$
P_j^{\mathrm{d}}=D_{jj}\geq L_j,
$$

这是关于 $D$（因而也是关于 $T$）的线性不等式。类似地，也可以规定将实际的 $\theta=j$ 误判为 $\theta=i$ 的最大允许概率：

$$
D_{ij}\leq U_{ij},
$$

<!-- pdf-page: 381 -->

这同样是关于 $T$ 的线性约束。可以将任意一个检测概率作为要最大化的目标，也可以将任意一个错误概率作为要最小化的目标。

#### 极小极大检测器设计

可以将极小极大错误概率 $\max_jP_j^{\mathrm{e}}$ 作为要最小化的目标，它是 $D$（因而也是 $T$）的分段线性凸函数。以此作为唯一目标，就得到最小化最大检测错误概率的问题：

$$
\begin{array}{ll}
\text{最小化} & \max_jP_j^{\mathrm{e}}\\
\text{约束条件} & t_k\succeq0,\quad\mathbf{1}^Tt_k=1,\quad k=1,\ldots,n,
\end{array}
$$

其中变量为 $t_1,\ldots,t_n\in\mathbf{R}^m$。这个问题可以重写为线性规划。极小极大检测器使全部 $m$ 个假设中最坏情形的（最大的）错误概率最小。

当然，也可以在极小极大检测器设计问题中加入其他约束。

#### Bayes 检测器设计

在 Bayes 检测器设计中，各个假设有一个先验分布，由 $q\in\mathbf{R}^m$ 给出，其中

$$
q_i=\mathbf{prob}(\theta=i).
$$

这时，概率 $p_{ij}$ 被解释为给定 $\theta$ 时 $X$ 的条件概率。检测器的错误概率为 $q^TP^{\mathrm{e}}$，它是 $T$ 的仿射函数。Bayes 最优检测器是线性规划

$$
\begin{array}{ll}
\text{最小化} & q^TP^{\mathrm{e}}\\
\text{约束条件} & t_k\succeq0,\quad\mathbf{1}^Tt_k=1,\quad k=1,\ldots,n.
\end{array}
$$

的解。§7.3.4 将说明，这个问题有简单的解析解。

一个特例是 $q=(1/m)\mathbf{1}$。这时，Bayes 最优检测器最小化平均错误概率，其中平均是对所有假设取不加权平均。在 §7.3.4 中会看到，最大似然检测器 (7.10) 对这个问题是最优的。

#### 偏差、均方误差及其他量

本节假设 $\theta$ 各个取值的顺序有某种意义，即当 $i>j$ 时，$\theta=i$ 可以解释为比 $\theta=j$ 更大的参数值。例如，当 $\theta=i$ 对应于发生了 $i$ 次事件这一假设时，就可能属于这种情况。此时，我们可能关心这样的量：

$$
\mathbf{prob}(\widehat\theta>\theta\mid\theta=i),
$$

它是 $\theta=i$ 时高估 $\theta$ 的概率。这是 $D$ 的仿射函数：

$$
\mathbf{prob}(\widehat\theta>\theta\mid\theta=i)=\sum_{j>i}D_{ji},
$$

<!-- pdf-page: 382 -->

因此，这个概率的最大允许值可以表示为关于 $D$（因而也是关于 $T$）的线性不等式。再举一个例子，$\theta=i$ 时对 $\theta$ 的分类误差大于一的概率为

$$
\mathbf{prob}(|\widehat\theta-\theta|>1\mid\theta=i)=\sum_{|j-i|>1}D_{ji},
$$

它也是 $D$ 的线性函数。

现在假设参数的取值属于 $\{\theta_1,\ldots,\theta_m\}\subseteq\mathbf{R}$。于是，估计或检测的参数误差为 $\widehat\theta-\theta$，许多关心的量都是 $D$ 的线性函数。例如：

- **偏差（bias）。** 当 $\theta=\theta_i$ 时，检测器的偏差由以下线性函数给出：

    $$
    \mathop{\mathbf{E}}_i(\widehat\theta-\theta)=\sum_{j=1}^m(\theta_j-\theta_i)D_{ji},
    $$

    其中 $\mathbf{E}$ 的下标表示，期望是针对假设 $\theta=\theta_i$ 所对应的分布求取的。

- **均方误差。** 当 $\theta=\theta_i$ 时，检测器的均方误差由以下线性函数给出：

    $$
    \mathop{\mathbf{E}}_i(\widehat\theta-\theta)^2=\sum_{j=1}^m(\theta_j-\theta_i)^2D_{ji}.
    $$

- **平均绝对误差。** 当 $\theta=\theta_i$ 时，检测器的平均绝对误差由以下线性函数给出：

    $$
    \mathop{\mathbf{E}}_i|\widehat\theta-\theta|=\sum_{j=1}^m|\theta_j-\theta_i|D_{ji}.
    $$

### 7.3.4 多准则表述与标量化

最优检测器设计问题可以看成一个多准则问题，约束为 (7.11)，而 $m(m-1)$ 个目标由 $D$ 的非对角元素给出，它们是不同类型检测错误的概率：

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{R}_+^{m(m-1)}\text{）} & D_{ij},\quad i,j=1,\ldots,m,\quad i\ne j\\
\text{约束条件} & t_k\succeq0,\quad\mathbf{1}^Tt_k=1,\quad k=1,\ldots,n,
\end{array}
\tag{7.12}
$$

其中变量为 $t_1,\ldots,t_n\in\mathbf{R}^m$。由于每个目标 $D_{ij}$ 都是变量的线性函数，这是一个多准则线性规划。

可以构造加权和目标

$$
\sum_{i,j=1}^m W_{ij}D_{ij}=\operatorname{\mathbf{tr}}(W^TD)
$$

<!-- pdf-page: 383 -->

来对这个多准则问题进行标量化，其中权重矩阵 $W\in\mathbf{R}^{m\times m}$ 满足

$$
W_{ii}=0,\quad i=1,\ldots,m,\qquad W_{ij}>0,\quad i,j=1,\ldots,m,\quad i\ne j.
$$

这个目标是 $m(m-1)$ 个错误概率的加权和，权重 $W_{ij}$ 对应于实际为 $\theta=j$ 时猜测 $\widehat\theta=i$ 的错误。权重矩阵有时称为**损失矩阵**。

为了求多准则问题 (7.12) 的一个 Pareto 最优点，构造标量优化问题

$$
\begin{array}{ll}
\text{最小化} & \operatorname{\mathbf{tr}}(W^TD)\\
\text{约束条件} & t_k\succeq0,\quad\mathbf{1}^Tt_k=1,\quad k=1,\ldots,n,
\end{array}
\tag{7.13}
$$

这是一个线性规划。该线性规划关于变量 $t_1,\ldots,t_n$ 是可分的。目标可以写成各个 $t_k$ 的线性函数之和：

$$
\operatorname{\mathbf{tr}}(W^TD)=\operatorname{\mathbf{tr}}(W^TTP)=\operatorname{\mathbf{tr}}(PW^TT)=\sum_{k=1}^n c_k^Tt_k,
$$

其中 $c_k$ 是 $WP^T$ 的第 $k$ 列。约束也是可分的，即每个 $t_i$ 都有各自独立的约束。因此，可以对 $k=1,\ldots,n$ 分别求解

$$
\begin{array}{ll}
\text{最小化} & c_k^Tt_k\\
\text{约束条件} & t_k\succeq0,\quad\mathbf{1}^Tt_k=1,
\end{array}
$$

从而求解线性规划 (7.13)。这些线性规划都有简单的解析解（见习题 4.8）。先找出一个下标 $q$，使得 $c_{kq}=\min_jc_{kj}$，再取 $t_k^\star=e_q$。这个最优点对应于一个确定性检测器：当观测到 $X=k$ 时，估计为

$$
\widehat\theta=\operatorname{argmin}_j(WP^T)_{jk}.
\tag{7.14}
$$

因此，对于每个非对角元素均为正的权重矩阵 $W$，都可以找到使加权和目标最小的确定性检测器。这似乎表明不需要随机化检测器，但下面会看到并非如此。多准则线性规划 (7.12) 的 Pareto 最优权衡曲面是分段线性的；形如 (7.14) 的确定性检测器对应于 Pareto 最优曲面上的顶点。

#### MAP 与 ML 检测器

考虑先验分布为 $q$ 的 Bayes 检测器设计。平均错误概率为

$$
q^TP^{\mathrm{e}}=\sum_{j=1}^m q_j\sum_{i\ne j}D_{ij}=\sum_{i,j=1}^m W_{ij}D_{ij},
$$

其中将权重矩阵 $W$ 定义为

$$
W_{ij}=q_j,\quad i,j=1,\ldots,m,\quad i\ne j,\qquad
W_{ii}=0,\quad i=1,\ldots,m.
$$

<!-- pdf-page: 384 -->

因此，Bayes 最优检测器由确定性检测器 (7.14) 给出，其中

$$
(WP^T)_{jk}=\sum_{i\ne j}q_ip_{ki}=\sum_{i=1}^m q_ip_{ki}-q_jp_{kj}.
$$

第一项与 $j$ 无关，所以当观测到 $X=k$ 时，最优检测器就是

$$
\widehat\theta=\operatorname{argmax}_j(p_{kj}q_j).
$$

这个解有一个简单的解释：由于 $p_{kj}q_j$ 给出 $\theta=j$ 且 $X=k$ 的概率，因此这个检测器是**最大后验概率（MAP）检测器**。

在特例 $q=(1/m)\mathbf{1}$ 中，即 $\theta$ 的先验分布为均匀分布时，这个 MAP 检测器化为**最大似然（ML）检测器**：

$$
\widehat\theta=\operatorname{argmax}_j p_{kj}.
$$

因此，最大似然检测器使不加权的平均错误概率最小。

### 7.3.5 二元假设检验

作为说明，考虑特例 $m=2$，称为**二元假设检验**。随机变量 $X$ 从两个分布之一生成；为简化记号，将这两个分布记作 $p\in\mathbf{R}^n$ 和 $q\in\mathbf{R}^n$。通常，假设 $\theta=1$ 对应于某种正常情况，而假设 $\theta=2$ 对应于试图检测的某种异常事件。如果 $\widehat\theta=1$，称检验结果为**阴性**（即猜测事件没有发生）；如果 $\widehat\theta=2$，称检验结果为**阳性**（即猜测事件已经发生）。

检测概率矩阵 $D\in\mathbf{R}^{2\times2}$ 通常写成

$$
D=\begin{bmatrix}1-P_{\mathrm{fp}}&P_{\mathrm{fn}}\\P_{\mathrm{fp}}&1-P_{\mathrm{fn}}\end{bmatrix}.
$$

这里，$P_{\mathrm{fn}}$ 是**假阴性**的概率，即事件实际已经发生，但检验结果为阴性；$P_{\mathrm{fp}}$ 是**假阳性**的概率，即事件实际没有发生，但检验结果为阳性，也称为**虚警概率**。最优检测器设计问题是一个双准则问题，目标为 $P_{\mathrm{fn}}$ 和 $P_{\mathrm{fp}}$。

$P_{\mathrm{fn}}$ 和 $P_{\mathrm{fp}}$ 之间的最优权衡曲线称为**接收者操作特征（receiver operating characteristic，ROC）**，由分布 $p$ 和 $q$ 决定。按照 §7.3.4 中的方法对双准则问题进行标量化，就可以求出 ROC。对于权重矩阵 $W$，一个最优检测器 (7.14) 为

$$
\widehat\theta=\begin{cases}1&W_{21}p_k>W_{12}q_k\\2&W_{21}p_k\leq W_{12}q_k\end{cases}
$$

<!-- pdf-page: 385 -->

<figure id="fig-7-4" data-figure="7.4" data-no-english-text="true" data-reader-after="example-7-4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-4.png" alt="假阴性概率与假阳性概率之间的最优权衡折线；三个顶点标为一至三，折线与两种错误概率相等的斜虚线相交于标为四的点" data-source-page="385" data-source-rect="160,121,391,303.5">
<figcaption>图 7.4 对于 (7.15) 给出的矩阵 $P$，假阴性概率与检验结果为假阳性的概率之间的最优权衡曲线。曲线上标为 1–3 的顶点对应确定性检测器；标为 4 的点对应极小极大检测器，这是一个随机化检测器。虚线表示 $P_{\mathrm{fn}}=P_{\mathrm{fp}}$，即两种错误概率相等的点。</figcaption>
</figure>

其中观测值为 $X=k$。这称为**似然比阈值检验**：若比值 $p_k/q_k$ 大于阈值 $W_{12}/W_{21}$，则检验结果为阴性（即 $\widehat\theta=1$）；否则为阳性。选择不同的阈值，就得到具有不同假阳性与假阴性错误概率组合的确定性 Pareto 最优检测器。这个结论称为 **Neyman–Pearson 引理**。

似然比检测器并不能给出所有 Pareto 最优检测器；它们是分段线性最优权衡曲线的顶点。

<div class="example" id="example-7-4" markdown="1">

**例 7.4** 考虑一个二元假设检验例子，取 $n=4$，并令

$$
P=\begin{bmatrix}
0.70&0.10\\
0.20&0.10\\
0.05&0.70\\
0.05&0.10
\end{bmatrix}.
\tag{7.15}
$$

$P_{\mathrm{fn}}$ 和 $P_{\mathrm{fp}}$ 之间的最优权衡曲线，也就是接收者操作特征曲线，如图 7.4 所示。左端点对应于无论观测到什么 $X$ 值，总是给出阴性结果的检测器；右端点对应于总是给出阳性结果的检测器。标为 $1$、$2$、$3$ 的顶点分别对应于以下确定性检测器：

$$
T^{(1)}=\begin{bmatrix}1&1&0&1\\0&0&1&0\end{bmatrix},
$$

$$
T^{(2)}=\begin{bmatrix}1&1&0&0\\0&0&1&1\end{bmatrix},
$$

<!-- pdf-page: 386 -->

$$
T^{(3)}=\begin{bmatrix}1&0&0&0\\0&1&1&1\end{bmatrix}.
$$

标为 $4$ 的点对应于非确定性检测器

$$
T^{(4)}=\begin{bmatrix}1&2/3&0&0\\0&1/3&1&1\end{bmatrix},
$$

它是极小极大检测器。这个极小极大检测器的假阳性概率与假阴性概率相等，在本例中都是 $1/6$。每个确定性检测器的假阳性概率或假阴性概率，至少有一个超过 $1/6$，因此本例展示了随机化检测器优于所有确定性检测器的情形。

</div>

### 7.3.6 鲁棒检测器

到目前为止，一直假设 $P$ 已知，它给出参数 $\theta$ 取各个值时，观测变量 $X$ 的分布。本节考虑这些分布未知、但给定了关于它们的某些先验信息的情形。假设 $P\in\mathcal{P}$，其中 $\mathcal{P}$ 是可能分布的集合。对于由 $T$ 刻画的随机化检测器，检测概率矩阵 $D$ 现在依赖于 $P$ 的具体取值。我们将根据 $P\in\mathcal{P}$ 时的最坏情形值，评价错误概率。定义**最坏情形检测概率矩阵** $D^{\mathrm{wc}}$ 为

$$
D_{ij}^{\mathrm{wc}}=\sup_{P\in\mathcal{P}}D_{ij},\qquad i,j=1,\ldots,m,\quad i\ne j
$$

以及

$$
D_{ii}^{\mathrm{wc}}=\inf_{P\in\mathcal{P}}D_{ii},\qquad i=1,\ldots,m.
$$

非对角元素给出在 $P\in\mathcal{P}$ 中可能出现的最大错误概率，而对角元素给出可能出现的最小检测概率。注意，一般有 $\sum_{i=1}^nD_{ij}^{\mathrm{wc}}\ne1$，也就是说，最坏情形检测概率矩阵每一列的元素之和不一定为一。

定义最坏情形错误概率为

$$
P_i^{\mathrm{wce}}=1-D_{ii}^{\mathrm{wc}}.
$$

因此，$P_i^{\mathrm{wce}}$ 是当 $\theta=i$ 时，在 $\mathcal{P}$ 中所有可能分布上最大的错误概率。

利用最坏情形检测概率矩阵，或最坏情形错误概率向量，可以建立检测器设计问题的各种鲁棒形式。本节余下部分集中讨论鲁棒极小极大检测器设计问题，以此作为说明思路的典型例子。

将**鲁棒极小极大检测器**定义为使所有假设下最坏情形错误概率最小的检测器，即最小化目标

$$
\max_iP_i^{\mathrm{wce}}=\max_{i=1,\ldots,m}\sup_{P\in\mathcal{P}}(1-(TP)_{ii})
=1-\min_{i=1,\ldots,m}\inf_{P\in\mathcal{P}}(TP)_{ii}.
$$

鲁棒极小极大检测器使全部 $m$ 个假设及全部 $P\in\mathcal{P}$ 中可能出现的最大错误概率最小。

<!-- pdf-page: 387 -->

#### 有限集合 $\mathcal{P}$ 的鲁棒极小极大检测器

当可能分布的集合有限时，鲁棒极小极大检测器设计问题很容易表述为线性规划。设 $\mathcal{P}=\{P_1,\ldots,P_k\}$，求解

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\min_{i=1,\ldots,m}\inf_{P\in\mathcal{P}}(TP)_{ii}=\min_{i=1,\ldots,m}\min_{j=1,\ldots,k}(TP_j)_{ii}\\
\text{约束条件} & t_i\succeq0,\quad\mathbf{1}^Tt_i=1,\quad i=1,\ldots,n,
\end{array}
$$

就可以得到鲁棒极小极大检测器。目标是分段线性的凹函数，因此这个问题可以表示为线性规划。注意，也可以将 $\mathcal{P}$ 换成多面体 $\operatorname{\mathbf{conv}}\mathcal{P}$；对应的最坏情形检测矩阵和鲁棒极小极大检测器都相同。

#### 多面体 $\mathcal{P}$ 的鲁棒极小极大检测器

当 $\mathcal{P}$ 是由线性等式和不等式约束描述的多面体时，也可以将鲁棒极小极大检测器问题有效地表述为线性规划。这种表述没有那么显然，需要借助 $\mathcal{P}$ 的对偶表示。

为简化讨论，假设 $\mathcal{P}$ 具有如下形式：

$$
\mathcal{P}=\{P=[p_1\ \cdots\ p_m]\mid A_kp_k=b_k,\ \mathbf{1}^Tp_k=1,\ p_k\succeq0\}.
\tag{7.16}
$$

换言之，对于每个分布 $p_k$，给定若干期望值 $A_kp_k=b_k$。（它们可以表示已知的矩、概率等。）推广到给定期望值不等式的情形也很直接。

鲁棒极小极大设计问题为

$$
\begin{array}{ll}
\text{最大化} & \gamma\\
\text{约束条件} & \inf\{\widetilde t_i^Tp\mid A_ip=b_i,\ \mathbf{1}^Tp=1,\ p\succeq0\}\geq\gamma,\quad i=1,\ldots,m\\
& t_i\succeq0,\quad\mathbf{1}^Tt_i=1,\quad i=1,\ldots,n,
\end{array}
$$

其中 $\widetilde t_i^T$ 表示 $T$ 的第 $i$ 行（因此 $(TP)_{ii}=\widetilde t_i^Tp_i$）。根据线性规划对偶性，

$$
\inf\{\widetilde t_i^Tp\mid A_ip=b_i,\ \mathbf{1}^Tp=1,\ p\succeq0\}
=\sup\{\nu^Tb_i+\mu\mid A_i^T\nu+\mu\mathbf{1}\preceq\widetilde t_i\}.
$$

利用这一点，鲁棒极小极大检测器设计问题可以表述为线性规划

$$
\begin{array}{ll}
\text{最大化} & \gamma\\
\text{约束条件} & \nu_i^Tb_i+\mu_i\geq\gamma,\quad i=1,\ldots,m\\
& A_i^T\nu_i+\mu_i\mathbf{1}\preceq\widetilde t_i,\quad i=1,\ldots,m\\
& t_i\succeq0,\quad\mathbf{1}^Tt_i=1,\quad i=1,\ldots,n,
\end{array}
$$

变量为 $\nu_1,\ldots,\nu_m$、$\mu_1,\ldots,\mu_n$ 和 $T$（其各列为 $t_i$，各行为 $\widetilde t_i^T$）。

<div class="example" markdown="1">

**例 7.5 鲁棒二元假设检验。** 假设 $m=2$，且 (7.16) 中的集合 $\mathcal{P}$ 由下式定义：

$$
A_1=A_2=A=\begin{bmatrix}a_1&a_2&\cdots&a_n\\a_1^2&a_2^2&\cdots&a_n^2\end{bmatrix},
\qquad b_1=\begin{bmatrix}\alpha_1\\\alpha_2\end{bmatrix},
\qquad b_2=\begin{bmatrix}\beta_1\\\beta_2\end{bmatrix}.
$$

为这个集合 $\mathcal{P}$ 设计鲁棒极小极大检测器，可以解释为一个二元假设检验问题：根据对随机变量 $X\in\{a_1,\ldots,a_n\}$ 的一次观测，在下面两个假设之间作出选择：

<!-- pdf-page: 388 -->

1. $\mathbf{E}\,X=\alpha_1$、$\mathbf{E}\,X^2=\alpha_2$。
2. $\mathbf{E}\,X=\beta_1$、$\mathbf{E}\,X^2=\beta_2$。

用 $\widetilde t^T$ 表示 $T$ 的第一行，因此第二行为 $(\mathbf{1}-\widetilde t)^T$。给定 $\widetilde t$，正确检测的最坏情形概率为

$$
\begin{aligned}
D_{11}^{\mathrm{wc}}&=\inf\left\{\widetilde t^Tp\ \middle|\ \sum_{i=1}^n a_ip_i=\alpha_1,\ \sum_{i=1}^n a_i^2p_i=\alpha_2,\ \mathbf{1}^Tp=1,\ p\succeq0\right\}\\
D_{22}^{\mathrm{wc}}&=\inf\left\{(\mathbf{1}-\widetilde t)^Tp\ \middle|\ \sum_{i=1}^n a_ip_i=\beta_1,\ \sum_{i=1}^n a_i^2p_i=\beta_2,\ \mathbf{1}^Tp=1,\ p\succeq0\right\}.
\end{aligned}
$$

利用线性规划对偶性，可以将 $D_{11}^{\mathrm{wc}}$ 表示为线性规划

$$
\begin{array}{ll}
\text{最大化} & z_0+z_1\alpha_1+z_2\alpha_2\\
\text{约束条件} & z_0+a_iz_1+a_i^2z_2\leq\widetilde t_i,\quad i=1,\ldots,n,
\end{array}
$$

的最优值，其中变量为 $z_0,z_1,z_2\in\mathbf{R}$。类似地，$D_{22}^{\mathrm{wc}}$ 是线性规划

$$
\begin{array}{ll}
\text{最大化} & w_0+w_1\beta_1+w_2\beta_2\\
\text{约束条件} & w_0+a_iw_1+a_i^2w_2\leq1-\widetilde t_i,\quad i=1,\ldots,n,
\end{array}
$$

的最优值，其中变量为 $w_0,w_1,w_2\in\mathbf{R}$。为了得到极小极大检测器，需要最大化 $D_{11}^{\mathrm{wc}}$ 和 $D_{22}^{\mathrm{wc}}$ 中的较小者，即求解线性规划

$$
\begin{array}{ll}
\text{最大化} & \gamma\\
\text{约束条件} & z_0+z_1\alpha_2+z_2\alpha_2\geq\gamma\\
& w_0+\beta_1w_1+\beta_2w_2\geq\gamma\\
& z_0+z_1a_i+z_2a_i^2\leq\widetilde t_i,\quad i=1,\ldots,n\\
& w_0+w_1a_i+w_2a_i^2\leq1-\widetilde t_i,\quad i=1,\ldots,n\\
& 0\preceq\widetilde t\preceq\mathbf{1}.
\end{array}
$$

变量为 $z_0,z_1,z_2,w_0,w_1,w_2$ 和 $\widetilde t$。

</div>

<div class="translator-note" markdown="1">

**译注（矩的下标）：** 由本例上面的 $D_{11}^{\mathrm{wc}}$ 对偶表达式，$z_1$ 对应一阶矩 $\alpha_1$；最后一个线性规划第一条约束中的 $z_1\alpha_2$ 应为 $z_1\alpha_1$。

</div>

## 7.4 Chebyshev 界与 Chernoff 界

本节考虑集合概率的两类经典界，并说明它们各自的推广都可以表述为凸优化问题。最初的经典界对应于具有解析解的简单凸优化问题；把一般情形表述为凸优化问题，就可以计算更好的界，或计算更复杂情况下的界。

### 7.4.1 Chebyshev 界

Chebyshev 界根据某些函数的已知期望值（例如均值和方差），给出集合概率的上界。最简单的例子是 **Markov 不等式**：如果 $X$ 是 $\mathbf{R}_+$ 上的随机变量，且 $\mathbf{E}\,X=\mu$，<!-- pdf-page: 389 -->那么无论 $X$ 的分布如何，都有 $\mathbf{prob}(X\geq1)\leq\mu$。另一个简单例子是 **Chebyshev 界**：如果 $X$ 是 $\mathbf{R}$ 上的随机变量，满足 $\mathbf{E}\,X=\mu$、$\mathbf{E}(X-\mu)^2=\sigma^2$，那么同样无论 $X$ 的分布如何，都有 $\mathbf{prob}(|X-\mu|\geq1)\leq\sigma^2$。这些简单界背后的思路，可以推广到用凸优化计算概率界的情形。

设 $X$ 是 $S\subseteq\mathbf{R}^m$ 上的随机变量，$C\subseteq S$ 是我们希望求其概率 $\mathbf{prob}(X\in C)$ 的界的集合。用 $1_C$ 表示集合 $C$ 的 $0$–$1$ 指示函数，即当 $z\in C$ 时 $1_C(z)=1$，当 $z\notin C$ 时 $1_C(z)=0$。

关于分布的先验知识由某些函数的已知期望值组成：

$$
\mathbf{E}\,f_i(X)=a_i,\qquad i=1,\ldots,n,
$$

其中 $f_i:\mathbf{R}^m\to\mathbf{R}$。取 $f_0$ 为值恒为一的常函数，始终有 $\mathbf{E}\,f_0(X)=a_0=1$。考虑函数 $f_i$ 的线性组合

$$
f(z)=\sum_{i=0}^n x_if_i(z),
$$

其中 $x_i\in\mathbf{R}$，$i=0,\ldots,n$。根据已知的 $\mathbf{E}\,f_i(X)$，有 $\mathbf{E}\,f(X)=a^Tx$。

现在假设 $f$ 对所有 $z\in S$ 都满足条件 $f(z)\geq1_C(z)$，即 $f$ 在 $S$ 上逐点大于或等于集合 $C$ 的指示函数。于是有

$$
\mathbf{E}\,f(X)=a^Tx\geq\mathbf{E}\,1_C(X)=\mathbf{prob}(X\in C).
$$

换言之，$a^Tx$ 是 $\mathbf{prob}(X\in C)$ 的一个上界，对所有取值位于 $S$ 且满足 $\mathbf{E}\,f_i(X)=a_i$ 的分布都成立。

可以通过求解问题

$$
\begin{array}{ll}
\text{最小化} & x_0+a_1x_1+\cdots+a_nx_n\\
\text{约束条件} & \displaystyle f(z)=\sum_{i=0}^n x_if_i(z)\geq1\quad\text{对于 }z\in C\\
& \displaystyle f(z)=\sum_{i=0}^n x_if_i(z)\geq0\quad\text{对于 }z\in S,\ z\notin C,
\end{array}
\tag{7.17}
$$

寻找 $\mathbf{prob}(X\in C)$ 的最佳此类上界，其中变量为 $x\in\mathbf{R}^{n+1}$。这个问题总是凸问题，因为约束可以写成

$$
g_1(x)=1-\inf_{z\in C}f(z)\leq0,\qquad
g_2(x)=-\inf_{z\in S\setminus C}f(z)\leq0
$$

（$g_1$ 和 $g_2$ 都是凸函数）。问题 (7.17) 也可以看作一个**半无限线性规划**，即目标为线性函数、包含无穷多个线性不等式的优化问题，每个 $z\in S$ 对应一个不等式。

在简单情况下，可以解析求解问题 (7.17)。例如，取 $S=\mathbf{R}_+$、$C=[1,\infty)$、$f_0(z)=1$ 和 $f_1(z)=z$，先验信息为 $\mathbf{E}\,f_1(X)=\mathbf{E}\,X=\mu\leq1$。对 $z\in S$ 要求 $f(z)\geq0$，可化为 $x_0\geq0$、$x_1\geq0$。对 $z\in C$ 要求 $f(z)\geq1$，即对所有 $z\geq1$ 都有 $x_0+x_1z\geq1$，可化为 $x_0+x_1\geq1$。于是问题 (7.17) 成为

$$
\begin{array}{ll}
\text{最小化} & x_0+\mu x_1\\
\text{约束条件} & x_0\geq0,\quad x_1\geq0\\
& x_0+x_1\geq1.
\end{array}
$$

<!-- pdf-page: 390 -->

由于 $0\leq\mu\leq1$，这个简单线性规划的最优点为 $x_0=0$、$x_1=1$。这就给出了经典的 Markov 界 $\mathbf{prob}(X\geq1)\leq\mu$。

在其他情况下，可以用凸优化求解问题 (7.17)。

<div class="remark" markdown="1">

**注 7.1 对偶性与 Chebyshev 界问题。** Chebyshev 界问题 (7.17) 为所有满足给定期望值约束的概率测度，确定 $\mathbf{prob}(X\in C)$ 的一个界。因此，可以认为 Chebyshev 界问题 (7.17) 给出了无限维问题

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\int_C\pi(dz)\\
\text{约束条件} & \displaystyle\int_S f_i(z)\pi(dz)=a_i,\quad i=1,\ldots,n\\
& \displaystyle\int_S\pi(dz)=1\\
& \pi\geq0,
\end{array}
\tag{7.18}
$$

最优值的一个界，其中变量是测度 $\pi$，$\pi\geq0$ 表示该测度非负。

由于 Chebyshev 问题 (7.17) 为问题 (7.18) 给出了一个界，两者通过对偶性联系在一起也就并不意外。虽然半无限问题和无限维问题超出了本书的范围，仍可以形式上构造问题 (7.17) 的一个对偶：引入拉格朗日乘子函数 $p:S\to\mathbf{R}$，其中 $p(z)$ 是与不等式 $f(z)\geq1$（当 $z\in C$ 时）或 $f(z)\geq0$（当 $z\in S\setminus C$ 时）对应的拉格朗日乘子。用关于 $z$ 的积分，代替有限维情形中的求和，就得到形式上的对偶

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\int_C p(z)\,dz\\
\text{约束条件} & \displaystyle\int_S f_i(z)p(z)\,dz=a_i,\quad i=1,\ldots,n\\
& \displaystyle\int_S p(z)\,dz=1\\
& p(z)\geq0\quad\text{对所有 }z\in S,
\end{array}
$$

其中优化变量是函数 $p$。这实质上与 (7.18) 相同。

</div>

#### 已知一阶和二阶矩时的概率界

例如，假设 $S=\mathbf{R}^m$，且给定随机变量 $X$ 的一阶和二阶矩：

$$
\mathbf{E}\,X=a\in\mathbf{R}^m,\qquad\mathbf{E}\,XX^T=\Sigma\in\mathbf{S}^m.
$$

换言之，给定了 $m$ 个函数 $z_i$，$i=1,\ldots,m$，以及 $m(m+1)/2$ 个函数 $z_iz_j$，$i,j=1,\ldots,m$ 的期望值，但没有关于分布的其他信息。

这时，可以将 $f$ 写成一般的二次函数

$$
f(z)=z^TPz+2q^Tz+r,
$$

其中变量（即上面讨论中的向量 $x$）为 $P\in\mathbf{S}^m$、$q\in\mathbf{R}^m$ 和 $r\in\mathbf{R}$。根据已知的一阶和二阶矩，可以得到

$$
\begin{aligned}
\mathbf{E}\,f(X)&=\mathbf{E}(X^TPX+2q^TX+r)\\
&=\mathbf{E}\,\operatorname{\mathbf{tr}}(PXX^T)+2\mathbf{E}\,q^TX+r\\
&=\operatorname{\mathbf{tr}}(\Sigma P)+2q^Ta+r.
\end{aligned}
$$

<!-- pdf-page: 391 -->

要求对所有 $z$ 都有 $f(z)\geq0$，可以表示为线性矩阵不等式

$$
\begin{bmatrix}P&q\\q^T&r\end{bmatrix}\succeq0.
$$

特别地，有 $P\succeq0$。

现在假设集合 $C$ 是一个开多面体的补集：

$$
C=\mathbf{R}^m\setminus\mathcal{P},\qquad
\mathcal{P}=\{z\mid a_i^Tz<b_i,\ i=1,\ldots,k\}.
$$

对所有 $z\in C$ 要求 $f(z)\geq1$，等同于对 $i=1,\ldots,k$ 要求

$$
a_i^Tz\geq b_i\quad\Longrightarrow\quad z^TPz+2q^Tz+r\geq1.
$$

这又可以表示为：存在 $\tau_1,\ldots,\tau_k\geq0$，使得

$$
\begin{bmatrix}P&q\\q^T&r-1\end{bmatrix}
\succeq\tau_i\begin{bmatrix}0&a_i/2\\a_i^T/2&-b_i\end{bmatrix},\qquad i=1,\ldots,k.
$$

（见 §B.2。）

将这些条件合在一起，Chebyshev 界问题 (7.17) 可以写成

$$
\begin{array}{ll}
\text{最小化} & \operatorname{\mathbf{tr}}(\Sigma P)+2q^Ta+r\\
\text{约束条件} & \begin{bmatrix}P&q\\q^T&r-1\end{bmatrix}\succeq\tau_i\begin{bmatrix}0&a_i/2\\a_i^T/2&-b_i\end{bmatrix},\quad i=1,\ldots,k\\[3pt]
& \tau_i\geq0,\quad i=1,\ldots,k\\[3pt]
& \begin{bmatrix}P&q\\q^T&r\end{bmatrix}\succeq0,
\end{array}
\tag{7.19}
$$

这是关于变量 $P,q,r$ 和 $\tau_1,\ldots,\tau_k$ 的半定规划。设最优值为 $\alpha$，它是所有均值为 $a$、二阶矩为 $\Sigma$ 的分布下 $\mathbf{prob}(X\in C)$ 的上界。换一种说法，$1-\alpha$ 是 $\mathbf{prob}(X\in\mathcal{P})$ 的下界。

<div class="remark" markdown="1">

**注 7.2 对偶性与 Chebyshev 界问题。** 与 (7.19) 对应的对偶半定规划可以写成

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\sum_{i=1}^k\lambda_i\\
\text{约束条件} & a_i^Tz_i\geq b\lambda_i,\quad i=1,\ldots,k\\
& \displaystyle\sum_{i=1}^k\begin{bmatrix}Z_i&z_i\\z_i^T&\lambda_i\end{bmatrix}\preceq\begin{bmatrix}\Sigma&a\\a^T&1\end{bmatrix}\\[3pt]
& \begin{bmatrix}Z_i&z_i\\z_i^T&\lambda_i\end{bmatrix}\succeq0,\quad i=1,\ldots,k.
\end{array}
$$

变量为 $Z_i\in\mathbf{S}^m$、$z_i\in\mathbf{R}^m$ 和 $\lambda_i\in\mathbf{R}$，$i=1,\ldots,k$。由于半定规划 (7.19) 严格可行，强对偶性成立，且对偶最优值能够达到。

可以对这个对偶问题给出一个有趣的概率解释。假设 $Z_i,z_i,\lambda_i$ 对偶可行，且 $\lambda$ 的前 $r$ 个分量为正，其<!-- pdf-page: 392 -->余分量为零。为简单起见，还假设 $\sum_{i=1}^k\lambda_i<1$。定义

$$
\begin{aligned}
x_i&=(1/\lambda_i)z_i,\qquad i=1,\ldots,r,\\
w_0&=\frac{1}{\mu}\left(a-\sum_{i=1}^r\lambda_ix_i\right),\\
W&=\frac{1}{\mu}\left(\Sigma-\sum_{i=1}^r\lambda_ix_ix_i^T\right),
\end{aligned}
$$

其中 $\mu=1-\sum_{i=1}^k\lambda_i$。按照这些定义，对偶可行性约束可以写成

$$
a_i^Tx_i\geq b_i,\qquad i=1,\ldots,r
$$

以及

$$
\sum_{i=1}^r\lambda_i\begin{bmatrix}x_ix_i^T&x_i\\x_i^T&1\end{bmatrix}
+\mu\begin{bmatrix}W&w_0\\w_0^T&1\end{bmatrix}
=\begin{bmatrix}\Sigma&a\\a^T&1\end{bmatrix}.
$$

此外，由对偶可行性可得

$$
\begin{aligned}
\mu\begin{bmatrix}W&w_0\\w_0^T&1\end{bmatrix}
&=\begin{bmatrix}\Sigma&a\\a^T&1\end{bmatrix}-\sum_{i=1}^r\lambda_i\begin{bmatrix}x_ix_i^T&x_i\\x_i^T&1\end{bmatrix}\\
&=\begin{bmatrix}\Sigma&a\\a^T&1\end{bmatrix}-\sum_{i=1}^r\begin{bmatrix}(1/\lambda_i)z_iz_i^T&z_i\\z_i^T&\lambda_i\end{bmatrix}\\
&\succeq\begin{bmatrix}\Sigma&a\\a^T&1\end{bmatrix}-\sum_{i=1}^r\begin{bmatrix}Z_i&z_i\\z_i^T&\lambda_i\end{bmatrix}\\
&\succeq0.
\end{aligned}
$$

因此，$W\succeq w_0w_0^T$，所以可以作分解 $W-w_0w_0^T=\sum_{i=1}^s w_iw_i^T$。现在考虑具有以下分布的离散随机变量 $X$。如果 $s\geq1$，取

$$
\begin{array}{lll}
X=x_i & \text{以概率 }\lambda_i, & i=1,\ldots,r\\
X=w_0+\sqrt{s}\,w_i & \text{以概率 }\mu/(2s), & i=1,\ldots,s\\
X=w_0-\sqrt{s}\,w_i & \text{以概率 }\mu/(2s), & i=1,\ldots,s.
\end{array}
$$

如果 $s=0$，取

$$
\begin{array}{lll}
X=x_i & \text{以概率 }\lambda_i, & i=1,\ldots,r\\
X=w_0 & \text{以概率 }\mu.
\end{array}
$$

容易验证 $\mathbf{E}\,X=a$ 且 $\mathbf{E}\,XX^T=\Sigma$，即这个分布与给定的矩相符。此外，由于 $x_i\in C$，

$$
\mathbf{prob}(X\in C)\geq\sum_{i=1}^r\lambda_i.
$$

特别地，将这种解释用于对偶最优解，就能构造出一个分布，使 (7.19) 给出的 Chebyshev 界取等号，说明这一情形下的 Chebyshev 界是紧的。

</div>

<div class="translator-note" markdown="1">

**译注（约束的下标）：** 对应 (7.19) 中第 $i$ 个半空间，上面对偶问题第一条约束中的 $b$ 应为 $b_i$，即 $a_i^Tz_i\geq b_i\lambda_i$。这也与化简后的 $a_i^Tx_i\geq b_i$ 一致。

</div>

<!-- pdf-page: 393 -->

### 7.4.2 Chernoff 界

设 $X$ 是 $\mathbf{R}$ 上的随机变量。Chernoff 界指出

$$
\mathbf{prob}(X\geq u)\leq\inf_{\lambda\geq0}\mathbf{E}\,e^{\lambda(X-u)},
$$

可以写成

$$
\log\mathbf{prob}(X\geq u)\leq\inf_{\lambda\geq0}\{-\lambda u+\log\mathbf{E}\,e^{\lambda X}\}.
\tag{7.20}
$$

回忆第 106 页的例 3.41，右侧的 $\log\mathbf{E}\,e^{\lambda X}$ 称为该分布的累积量生成函数，它总是凸函数，因此要最小化的函数是凸的。当累积量生成函数具有解析表达式，而且可以解析求出关于 $\lambda$ 的最小值时，界 (7.20) 最有用。

例如，如果 $X$ 服从均值为零、方差为一的高斯分布，其累积量生成函数为

$$
\log\mathbf{E}\,e^{\lambda X}=\lambda^2/2,
$$

且 $-\lambda u+\lambda^2/2$ 在 $\lambda\geq0$ 上的下确界在 $\lambda=u$ 处取得（若 $u\geq0$），所以 Chernoff 界为（对 $u\geq0$）

$$
\mathbf{prob}(X\geq u)\leq e^{-u^2/2}.
$$

Chernoff 界背后的思路可以推广到更一般的情形，用凸优化来计算 $\mathbf{R}^m$ 中集合的概率界。设 $C\subseteq\mathbf{R}^m$，与上面对 Chebyshev 界的讨论一样，用 $1_C$ 表示 $C$ 的 $0$–$1$ 指示函数。下面推导 $\mathbf{prob}(X\in C)$ 的上界。（原则上，可以通过例如 Monte Carlo 模拟或数值积分来计算 $\mathbf{prob}(X\in C)$，但两种方法的计算任务都可能十分繁重，而且都不能给出有保证的界。）

设 $\lambda\in\mathbf{R}^m$、$\mu\in\mathbf{R}$，考虑函数 $f:\mathbf{R}^m\to\mathbf{R}$，定义为

$$
f(z)=e^{\lambda^Tz+\mu}.
$$

与推导 Chebyshev 界时一样，如果 $f$ 对所有 $z$ 都满足 $f(z)\geq1_C(z)$，就可以得出

$$
\mathbf{prob}(X\in C)=\mathbf{E}\,1_C(X)\leq\mathbf{E}\,f(X).
$$

显然，对所有 $z$ 都有 $f(z)\geq0$；要求对 $z\in C$ 有 $f(z)\geq1$，等同于对所有 $z\in C$ 有 $\lambda^Tz+\mu\geq0$，即对所有 $z\in C$ 有 $-\lambda^Tz\leq\mu$。因此，如果对所有 $z\in C$ 都有 $-\lambda^Tz\leq\mu$，就得到界

$$
\mathbf{prob}(X\in C)\leq\mathbf{E}\,\exp(\lambda^TX+\mu),
$$

或者取对数后写成

$$
\log\mathbf{prob}(X\in C)\leq\mu+\log\mathbf{E}\,\exp(\lambda^TX).
$$

<!-- pdf-page: 394 -->

由此得到 Chernoff 界的一般形式：

$$
\begin{aligned}
\log\mathbf{prob}(X\in C)
&\leq\inf\{\mu+\log\mathbf{E}\,\exp(\lambda^TX)\mid-\lambda^Tz\leq\mu\ \text{对所有 }z\in C\}\\
&=\inf_\lambda\left(\sup_{z\in C}(-\lambda^Tz)+\log\mathbf{E}\,\exp(\lambda^TX)\right)\\
&=\inf\bigl(S_C(-\lambda)+\log\mathbf{E}\,\exp(\lambda^TX)\bigr),
\end{aligned}
$$

其中 $S_C$ 是 $C$ 的支撑函数。注意，第二项 $\log\mathbf{E}\,\exp(\lambda^TX)$ 是该分布的累积量生成函数，总是凸的（见第 106 页的例 3.41）。一般来说，计算这个界是一个凸优化问题。

#### 高斯变量落在多面体中的 Chernoff 界

作为一个具体例子，假设 $X$ 是 $\mathbf{R}^m$ 上均值为零、协方差为 $I$ 的高斯随机向量，因此其累积量生成函数为

$$
\log\mathbf{E}\,\exp(\lambda^TX)=\lambda^T\lambda/2.
$$

取 $C$ 为由不等式描述的多面体：

$$
C=\{x\mid Ax\preceq b\},
$$

并假设它非空。

为了用于 Chernoff 界，采用支撑函数 $S_C$ 的对偶表示：

$$
\begin{aligned}
S_C(y)&=\sup\{y^Tx\mid Ax\preceq b\}\\
&=-\inf\{-y^Tx\mid Ax\preceq b\}\\
&=-\sup\{-b^Tu\mid A^Tu=y,\ u\succeq0\}\\
&=\inf\{b^Tu\mid A^Tu=y,\ u\succeq0\},
\end{aligned}
$$

其中第三行用了线性规划对偶性：

$$
\inf\{c^Tx\mid Ax\preceq b\}=\sup\{-b^Tu\mid A^Tu+c=0,\ u\succeq0\},
$$

并取 $c=-y$。在 Chernoff 界中使用这个 $S_C$ 的表达式，就得到

$$
\begin{aligned}
\log\mathbf{prob}(X\in C)&\leq\inf_\lambda\bigl(S_C(-\lambda)+\log\mathbf{E}\,\exp(\lambda^TX)\bigr)\\
&=\inf_\lambda\inf_u\{b^Tu+\lambda^T\lambda/2\mid u\succeq0,\ A^Tu+\lambda=0\}.
\end{aligned}
$$

因此，$\mathbf{prob}(X\in C)$ 的 Chernoff 界，是以下二次规划最优值的指数：

$$
\begin{array}{ll}
\text{最小化} & b^Tu+\lambda^T\lambda/2\\
\text{约束条件} & u\succeq0,\quad A^Tu+\lambda=0,
\end{array}
\tag{7.21}
$$

其中变量为 $u$ 和 $\lambda$。

<!-- pdf-page: 395 -->

这个问题有一个有趣的几何解释。它等价于

$$
\begin{array}{ll}
\text{最小化} & b^Tu+(1/2)\|A^Tu\|_2^2\\
\text{约束条件} & u\succeq0,
\end{array}
$$

而这个问题是

$$
\begin{array}{ll}
\text{最大化} & -(1/2)\|x\|_2^2\\
\text{约束条件} & Ax\preceq b.
\end{array}
$$

的对偶。换言之，Chernoff 界为

$$
\mathbf{prob}(X\in C)\leq\exp(-\mathbf{dist}(0,C)^2/2),
\tag{7.22}
$$

其中 $\mathbf{dist}(0,C)$ 是原点到 $C$ 的欧几里得距离。

<div class="remark" markdown="1">

**注 7.3** 也可以不使用 Chernoff 不等式推导界 (7.22)。如果 $0$ 与 $C$ 之间的距离为 $d$，那么存在包含 $C$ 的半空间 $\mathcal{H}=\{z\mid a^Tz\geq d\}$，其中 $\|a\|_2=1$。随机变量 $a^TX$ 服从 $\mathcal{N}(0,1)$ 分布，因此

$$
\mathbf{prob}(X\in C)\leq\mathbf{prob}(X\in\mathcal{H})=\Phi(-d),
$$

其中 $\Phi$ 是均值为零、方差为一的高斯分布的累积分布函数。由于当 $d\geq0$ 时有 $\Phi(-d)\leq e^{-d^2/2}$，这个界至少与 Chernoff 界 (7.22) 一样紧。

</div>

<div class="translator-note" markdown="1">

**译注（半空间论证的条件）：** 对于上述非空多面体 $C$，这里的半空间论证需要原点不在 $C$ 的内部。若 $0\in\operatorname{\mathbf{int}}C$，则 $d=0$，(7.22) 仍给出上界 $1$，但不能由此推出更强的 $\Phi(-d)=1/2$ 上界。

</div>

### 7.4.3 例子

本节用一个检测例子说明 Chebyshev 和 Chernoff 概率界方法。有一个包含 $m$ 个可能符号或信号的集合 $s\in\{s_1,s_2,\ldots,s_m\}\subseteq\mathbf{R}^n$，称为**信号星座**。其中一个信号通过带噪声的信道传输。接收信号为 $x=s+v$，其中 $v$ 是噪声，将其建模为随机变量。假设 $\mathbf{E}\,v=0$ 且 $\mathbf{E}\,vv^T=\sigma^2I$，即噪声分量 $v_1,\ldots,v_n$ 的均值为零、互不相关，方差为 $\sigma^2$。接收端必须根据收到的信号 $x=s+v$，估计发送了哪个信号。**最小距离检测器**选择与 $x$ 的欧几里得距离最近的符号 $s_k$ 作为估计。（如果噪声 $v$ 为高斯噪声，最小距离译码就与最大似然译码相同。）

如果发送的是信号 $s_k$，给定 $x$ 后将 $s_k$ 作为估计就属于正确检测。当信号 $s_k$ 比其他信号更接近 $x$ 时，就会出现这种情况，即

$$
\|x-s_k\|_2<\|x-s_j\|_2,\qquad j\ne k.
$$

因此，当随机变量 $v$ 满足线性不等式

$$
2(s_j-s_k)^T(s_k+v)<\|s_j\|_2^2-\|s_k\|_2^2,\qquad j\ne k,
$$

时，就能正确检测符号 $s_k$。这些不等式定义了信号星座中 $s_k$ 的 **Voronoi 区域** $V_k$，即与 $s_k$ 的距离比与星座中其他任何信号的距离都近的点所组成的集合。正确检测 $s_k$ 的概率为 $\mathbf{prob}(s_k+v\in V_k)$。

图 7.5 给出了一个简单例子，信号数为 $m=7$，维数为 $n=2$。

<!-- pdf-page: 396 -->

<figure id="fig-7-5" data-figure="7.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-5.png" alt="由七个信号点组成的二维星座；小空心圆表示各信号，实线表示 Voronoi 区域边界，每个信号周围还有一个表示尺度的点状圆" data-source-page="396" data-source-rect="246,121,430,307">
<figcaption>图 7.5 由 7 个信号 $s_1,\ldots,s_7\in\mathbf{R}^2$ 组成的星座，信号以小圆圈表示。线段表示相应 Voronoi 区域的边界。当接收信号比起其他任何点都更接近 $s_k$ 时，即接收信号位于符号 $s_k$ 周围的 Voronoi 区域内部时，最小距离检测器选择符号 $s_k$。各点周围的圆的半径为 1，用于表示尺度。</figcaption>
</figure>

#### Chebyshev 界

半定规划界 (7.19) 给出了正确检测概率的下界。对于三个符号 $s_1$、$s_2$ 和 $s_3$，图 7.6 将这些下界画成噪声标准差 $\sigma$ 的函数。这些界对任何均值为零、协方差为 $\sigma^2I$ 的噪声分布都成立。它们是紧的，意思是存在均值为零、协方差为 $\Sigma=\sigma^2I$ 的噪声分布，使错误概率等于这个下界。图 7.7 针对第一个 Voronoi 集合，在 $\sigma=1$ 时说明了这一点。

<div class="translator-note" markdown="1">

**译注（达到下界的概率）：** 这一段讨论的是正确检测概率的下界，因此“使错误概率等于这个下界”中的“错误概率”应理解为“正确检测概率”。图 7.7 给出的正确检测概率为 $0.2048$，相应错误概率为 $0.7952$。

</div>

#### Chernoff 界

用同一个例子说明 Chernoff 界。这里假设噪声是高斯噪声，即 $v\sim\mathcal{N}(0,\sigma^2I)$。如果发送符号 $s_k$，正确检测的概率就是 $s_k+v\in V_k$ 的概率。为了求这个概率的下界，利用二次规划 (7.21) 计算 ML 检测器选择符号 $i$，$i=1,\ldots,m$、$i\ne k$ 的概率上界。（每个上界都与 $s_k$ 到 Voronoi 集合 $V_i$ 的距离有关。）把这些将 $s_k$ 误判为 $s_i$ 的概率上界相加，就得到错误概率的上界，进而得到正确检测符号 $s_k$ 的概率下界。对于 $s_1$，得到的下界如图 7.8 所示，图中还给出了通过 Monte Carlo 分析得到的正确检测概率估计。

<!-- pdf-page: 397 -->

<figure id="fig-7-6" data-figure="7.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-6.png" alt="符号一、二、三的正确检测概率的三条 Chebyshev 下界曲线，均随噪声标准差 σ 增大而下降到零" data-source-page="397" data-source-rect="160,134,397,315">
<figcaption>图 7.6 符号 $s_1$、$s_2$ 和 $s_3$ 的正确检测概率的 Chebyshev 下界。这些界对任何均值为零、协方差为 $\sigma^2I$ 的噪声分布都有效。</figcaption>
<p class="figure-translation">图内文字：probability of correct detection——正确检测的概率。</p>
</figure>

<figure id="fig-7-7" data-figure="7.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-7.png" alt="七个信号点的 Voronoi 图中加入一个椭圆及六个实心点；五点位于椭圆边界，一点位于椭圆中心，中心实心点与符号 s₁ 的空心圆不同" data-source-page="397" data-source-rect="193,396,376,580">
<figcaption>图 7.7 当 $\sigma=1$ 时，正确检测符号 1 的概率的 Chebyshev 下界等于 0.2048。图中所示的离散分布达到了这个界。实心圆表示接收信号 $s_1+v$ 的可能取值。椭圆中心的点具有概率 0.2048，边界上五个点的概率之和为 0.7952。椭圆由 $x^TPx+2q^Tx+r=1$ 定义，其中 $P$、$q$ 和 $r$ 是 SDP (7.19) 的最优解。</figcaption>
</figure>

<!-- pdf-page: 398 -->

<figure id="fig-7-8" data-figure="7.8">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-8.png" alt="正确检测符号 s₁ 的概率随噪声标准差 σ 变化；Chernoff 下界为实线，Monte Carlo 估计为虚线，虚线始终位于实线上方或与其接近重合" data-source-page="398" data-source-rect="209,122,452,306">
<figcaption>图 7.8 正确检测符号 $s_1$ 的概率的 Chernoff 下界（实线）和 Monte Carlo 估计（虚线），作为 $\sigma$ 的函数。本例中，噪声服从均值为零、协方差为 $\sigma^2I$ 的高斯分布。</figcaption>
<p class="figure-translation">图内文字：probability of correct detection——正确检测的概率。</p>
</figure>

## 7.5 实验设计

考虑根据测量或实验

$$
y_i=a_i^Tx+w_i,\qquad i=1,\ldots,m,
$$

估计向量 $x\in\mathbf{R}^n$ 的问题，其中 $w_i$ 是测量噪声。假设 $w_i$ 是相互独立、均值为零、方差为一的高斯随机变量，并且测量向量 $a_1,\ldots,a_m$ 张成 $\mathbf{R}^n$。$x$ 的最大似然估计与最小方差估计相同，由最小二乘解给出：

$$
\widehat x=\left(\sum_{i=1}^m a_ia_i^T\right)^{-1}\sum_{i=1}^m y_ia_i.
$$

对应的估计误差 $e=\widehat x-x$ 的均值为零，协方差矩阵为

$$
E=\mathbf{E}\,ee^T=\left(\sum_{i=1}^m a_ia_i^T\right)^{-1}.
$$

矩阵 $E$ 刻画了估计的准确程度，或实验所提供的信息量。例如，$x$ 的 $\alpha$ 置信水平椭球为

$$
\mathcal{E}=\{z\mid(z-\widehat x)^TE^{-1}(z-\widehat x)\leq\beta\},
$$

其中 $\beta$ 是依赖于 $n$ 和 $\alpha$ 的常数。

假设用于描述测量的向量 $a_1,\ldots,a_m$，可以从 $p$ 个可能的测试向量 $v_1,\ldots,v_p\in\mathbf{R}^n$ 中选择，即每个 $a_i$ 都是某个<!-- pdf-page: 399 -->$v_j$。**实验设计**的目标，是从这些可能的选择中选出向量 $a_i$，使误差协方差 $E$ 在某种意义下尽可能小。换言之，$m$ 次实验或测量中的每一次，都可以从固定的 $p$ 种实验中选择；我们的任务是找到一组测量，使它们合在一起提供最多的信息。

用 $m_j$ 表示选择 $a_i=v_j$ 的实验次数，于是有

$$
m_1+\cdots+m_p=m.
$$

误差协方差矩阵可以写成

$$
E=\left(\sum_{i=1}^m a_ia_i^T\right)^{-1}
=\left(\sum_{j=1}^p m_jv_jv_j^T\right)^{-1}.
$$

这说明误差协方差只依赖于选择各类实验的次数，即 $m_1,\ldots,m_p$。

基本实验设计问题如下：给定实验的可能选择 $v_1,\ldots,v_p$，以及要进行的实验总次数 $m$，选择各类实验的次数 $m_1,\ldots,m_p$，使误差协方差 $E$ 在某种意义下尽可能小。当然，变量 $m_1,\ldots,m_p$ 必须为整数，而且它们之和必须等于给定的实验总次数 $m$。由此得到优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{S}_+^n\text{）} & \displaystyle E=\left(\sum_{j=1}^p m_jv_jv_j^T\right)^{-1}\\
\text{约束条件} & m_i\geq0,\quad m_1+\cdots+m_p=m\\
& m_i\in\mathbf{Z},
\end{array}
\tag{7.23}
$$

其中变量为整数 $m_1,\ldots,m_p$。

基本实验设计问题 (7.23) 是相对于半正定锥的向量优化问题。如果一个实验设计产生 $E$，另一个产生 $\widetilde E$，且 $E\preceq\widetilde E$，那么第一个实验设计肯定至少与第二个一样好。例如，第一个实验设计的置信椭球（为便于比较，将其平移到原点）包含于第二个实验设计的置信椭球中。还可以说，对任意向量 $q$，第一个实验设计都能比第二个更好地估计 $q^Tx$，即估计方差更小，因为对 $q^Tx$ 的估计方差，在第一个实验设计下为 $q^TEq$，在第二个实验设计下为 $q^T\widetilde Eq$。下面会介绍这个问题的几种常见标量化形式。

### 7.5.1 松弛后的实验设计问题

当实验总次数 $m$ 与 $p$ 相近时，基本实验设计问题 (7.23) 可能是一个困难的组合问题，因为这时各个 $m_i$ 都是小整数。不过，当 $m$ 远大于 $p$ 时，可以忽略或松弛 $m_i$ 必须为整数的约束，从而找到 (7.23) 的一个较好的近似解。令 $\lambda_i=m_i/m$，它是<!-- pdf-page: 400 -->满足 $a_j=v_i$ 的实验次数占实验总次数的比例，也就是实验 $i$ 的相对频率。用 $\lambda_i$ 可以将误差协方差写成

$$
E=\frac{1}{m}\left(\sum_{i=1}^p\lambda_iv_iv_i^T\right)^{-1}.
\tag{7.24}
$$

向量 $\lambda\in\mathbf{R}^p$ 满足 $\lambda\succeq0$、$\mathbf{1}^T\lambda=1$，而且每个 $\lambda_i$ 都是 $1/m$ 的整数倍。忽略最后这个约束，就得到问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{S}_+^n\text{）} & \displaystyle E=(1/m)\left(\sum_{i=1}^p\lambda_iv_iv_i^T\right)^{-1}\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1,
\end{array}
\tag{7.25}
$$

其中变量为 $\lambda\in\mathbf{R}^p$。为了与原来的组合实验设计问题 (7.23) 区分，称它为**松弛后的实验设计问题**。松弛后的实验设计问题 (7.25) 是凸优化问题，因为目标 $E$ 是 $\lambda$ 的 $\mathbf{S}_+^n$ 凸函数。

关于组合实验设计问题 (7.23) 与松弛问题 (7.25) 之间的关系，可以作出几个判断。显然，松弛问题的最优值为组合问题的最优值提供了下界，因为组合问题多了一个约束。根据松弛问题 (7.25) 的解，可以按如下方式构造组合问题 (7.23) 的一个次优解。首先，简单地四舍五入，得到

$$
m_i=\mathbf{round}(m\lambda_i),\qquad i=1,\ldots,p.
$$

与这组 $m_1,\ldots,m_p$ 对应的向量为 $\widetilde\lambda$，其中

$$
\widetilde\lambda_i=(1/m)\mathbf{round}(m\lambda_i),\qquad i=1,\ldots,p.
$$

向量 $\widetilde\lambda$ 满足每个分量都是 $1/m$ 的整数倍这一约束。显然，有 $|\lambda_i-\widetilde\lambda_i|\leq1/(2m)$，所以当 $m$ 很大时，$\lambda\approx\widetilde\lambda$。这意味着，当 $m$ 很大时，约束 $\mathbf{1}^T\widetilde\lambda=1$ 近似满足，而且与 $\widetilde\lambda$ 和 $\lambda$ 对应的误差协方差矩阵很接近。

<div class="translator-note" markdown="1">

**译注（取整后的总次数）：** 逐项取整后的总次数未必等于 $m$；若需严格满足总次数约束，还应调整取整结果，使各 $m_i$ 的和为 $m$。

</div>

还可以对松弛后的实验设计问题 (7.25) 给出另一种解释。可以将向量 $\lambda\in\mathbf{R}^p$ 看作定义了实验 $v_1,\ldots,v_p$ 上的一个概率分布。选择 $\lambda$ 对应于一个随机实验：每次实验 $a_i$ 以概率 $\lambda_j$ 取形式 $v_j$。

本节余下部分只考虑松弛后的实验设计问题，因此在讨论中省略“松弛后的”这一限定词。

### 7.5.2 标量化

实验设计问题 (7.25) 是相对于半正定锥的向量优化问题，人们为它提出了多种标量化形式。

<!-- pdf-page: 401 -->

#### $D$ 最优设计

使用最广泛的标量化形式称为 **$D$ 最优设计**，它最小化误差协方差矩阵 $E$ 的行列式。这相当于设计实验，使得到的置信椭球体积最小，置信水平保持固定。忽略 $E$ 中的常数因子 $1/m$，并对目标取对数，就可以将问题写成

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\log\det\left(\sum_{i=1}^p\lambda_iv_iv_i^T\right)^{-1}\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1,
\end{array}
\tag{7.26}
$$

这是一个凸优化问题。

#### $E$ 最优设计

在 **$E$ 最优设计**中，最小化误差协方差矩阵的范数，也就是 $E$ 的最大特征值。由于置信椭球 $\mathcal{E}$ 的直径（最长半轴的两倍）正比于 $\|E\|_2^{1/2}$，最小化 $\|E\|_2$ 可以在几何上解释为最小化置信椭球的直径。$E$ 最优设计也可以解释为：在所有满足 $\|q\|_2=1$ 的 $q$ 中，最小化 $q^Te$ 的最大方差。

$E$ 最优实验设计问题为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\left\|\left(\sum_{i=1}^p\lambda_iv_iv_i^T\right)^{-1}\right\|_2\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1.
\end{array}
$$

目标是 $\lambda$ 的凸函数，所以这是凸问题。

$E$ 最优实验设计问题可以表述为半定规划

$$
\begin{array}{ll}
\text{最大化} & t\\
\text{约束条件} & \displaystyle\sum_{i=1}^p\lambda_iv_iv_i^T\succeq tI\\
& \lambda\succeq0,\quad\mathbf{1}^T\lambda=1,
\end{array}
\tag{7.27}
$$

其中变量为 $\lambda\in\mathbf{R}^p$ 和 $t\in\mathbf{R}$。

#### $A$ 最优设计

在 **$A$ 最优实验设计**中，最小化协方差矩阵的迹 $\operatorname{\mathbf{tr}}E$。这个目标就是误差范数平方的期望：

$$
\mathbf{E}\,\|e\|_2^2=\mathbf{E}\,\operatorname{\mathbf{tr}}(ee^T)=\operatorname{\mathbf{tr}}E.
$$

$A$ 最优实验设计问题为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\operatorname{\mathbf{tr}}\left(\sum_{i=1}^p\lambda_iv_iv_i^T\right)^{-1}\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1.
\end{array}
\tag{7.28}
$$

这同样是凸问题。与 $E$ 最优实验设计问题一样，它也可以表述为半定规划：

$$
\begin{array}{ll}
\text{最小化} & \mathbf{1}^Tu\\
\text{约束条件} & \begin{bmatrix}\displaystyle\sum_{i=1}^p\lambda_iv_iv_i^T&e_k\\e_k^T&u_k\end{bmatrix}\succeq0,\quad k=1,\ldots,n\\[3pt]
& \lambda\succeq0,\quad\mathbf{1}^T\lambda=1,
\end{array}
$$

<!-- pdf-page: 402 -->

其中变量为 $u\in\mathbf{R}^n$ 和 $\lambda\in\mathbf{R}^p$，这里 $e_k$ 是第 $k$ 个单位向量。

#### 最优实验设计与对偶性

这三种标量化形式的拉格朗日对偶具有有趣的几何意义。

$D$ 最优实验设计问题 (7.26) 的对偶可以写成

$$
\begin{array}{ll}
\text{最大化} & \log\det W+n\log n\\
\text{约束条件} & v_i^TWv_i\leq1,\quad i=1,\ldots,p,
\end{array}
$$

其中变量为 $W\in\mathbf{S}^n$，定义域为 $\mathbf{S}_{++}^n$（见习题 5.10）。这个对偶问题有一个简单的解释：最优解 $W^\star$ 确定了以原点为中心、包含点 $v_1,\ldots,v_p$ 的最小体积椭球，其表达式为 $\{x\mid x^TW^\star x\leq1\}$。（另见第 222 页对问题 (5.14) 的讨论。）由互补松弛性，

$$
\lambda_i^\star(1-v_i^TW^\star v_i)=0,\qquad i=1,\ldots,p,
\tag{7.29}
$$

也就是说，最优实验设计只使用位于最小体积椭球表面上的实验 $v_i$。

$E$ 最优和 $A$ 最优设计问题的对偶也可以作类似解释。问题 (7.27) 和 (7.28) 的对偶分别可以写成

$$
\begin{array}{ll}
\text{最大化} & \operatorname{\mathbf{tr}}W\\
\text{约束条件} & v_i^TWv_i\leq1,\quad i=1,\ldots,p\\
& W\succeq0,
\end{array}
\tag{7.30}
$$

以及

$$
\begin{array}{ll}
\text{最大化} & (\operatorname{\mathbf{tr}}W^{1/2})^2\\
\text{约束条件} & v_i^TWv_i\leq1,\quad i=1,\ldots,p.
\end{array}
\tag{7.31}
$$

两个问题的变量都是 $W\in\mathbf{S}^n$。第二个问题中有隐式约束 $W\in\mathbf{S}_+^n$。（见习题 5.40 和 5.10。）

与 $D$ 最优设计一样，最优解 $W^\star$ 确定了一个包含点 $v_1,\ldots,v_p$ 的极小椭球 $\{x\mid x^TW^\star x\leq1\}$。此外，$W^\star$ 与 $\lambda^\star$ 满足互补松弛性条件 (7.29)，也就是说，最优设计只使用位于 $W^\star$ 所定义椭球表面上的实验 $v_i$。

<div class="translator-note" markdown="1">

**译注（对偶目标的归一化）：** (7.30) 使用了倒数归一化，其最优值与 (7.27) 的最优值互为倒数，等于前页逆矩阵谱范数最小化问题的最优值。

</div>

#### 实验设计例子

考虑 $x\in\mathbf{R}^2$、$p=20$ 的问题。$20$ 个候选测量向量 $a_i$ 用图 7.9 中的圆圈表示，原点用十字标出。$D$ 最优实验只有两个非零 $\lambda_i$，对应点在图 7.9 中用实心圆表示。$E$ 最优实验有两个非零 $\lambda_i$，对应点在图 7.10 中用实心圆表示。$A$ 最优实验有三个非零 $\lambda_i$，对应点在图 7.11 中用实心圆表示。图中还画出了与对偶最优解 $W^\star$ 对应的三个椭球 $\{x\mid x^TW^\star x\leq1\}$。相应的 $90\%$ 置信椭球如图 7.12 所示，图中也画出了“均匀”设计的置信椭球，即对所有实验赋予相等权重 $\lambda_i=1/p$ 的设计。

<!-- pdf-page: 403 -->

<figure id="fig-7-9" data-figure="7.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-9.png" alt="D 最优实验设计在二十个候选测量向量中选择两个，以实心圆标出且权重均为零点五；虚线椭圆以十字标出的原点为中心，并包含全部候选点" data-source-page="403" data-source-rect="159,120,394,235">
<figcaption>图 7.9 实验设计示例。20 个候选测量向量以圆圈表示。$D$ 最优设计使用实心圆所示的两个测量向量，并给它们分别赋予相同的权重 $\lambda_i=0.5$。图中的椭球是以原点为中心、包含所有点 $v_i$ 的最小体积椭球。</figcaption>
</figure>

<figure id="fig-7-10" data-figure="7.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-10.png" alt="E 最优实验设计选用两个实心圆所示的测量向量，权重分别为零点二和零点八；两条斜虚线表示相应椭球边界的一部分，十字标示原点" data-source-page="403" data-source-rect="175,329,394,461">
<figcaption>图 7.10 $E$ 最优设计使用两个测量向量。虚线是椭球 $\{x\mid x^TW^\star x\leq1\}$ 边界的一部分，其中 $W^\star$ 是对偶问题 (7.30) 的解。</figcaption>
</figure>

<figure id="fig-7-11" data-figure="7.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-11.png" alt="A 最优实验设计选用三个实心圆所示的测量向量，权重分别为零点三零、零点三八和零点三二；虚线椭圆表示与对偶解相关的椭球，十字标示原点" data-source-page="403" data-source-rect="171,529,394,628">
<figcaption>图 7.11 $A$ 最优设计使用三个测量向量。虚线表示与对偶问题 (7.31) 的解对应的椭球 $\{x\mid x^TW^\star x\leq1\}$。</figcaption>
</figure>

<!-- pdf-page: 404 -->

<figure id="fig-7-12" data-figure="7.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-12.png" alt="D、A、E 最优设计与均匀设计的四个置信椭球；三个实线椭圆较窄，均匀设计对应一个方向不同、范围较大的虚线椭圆" data-source-page="404" data-source-rect="247,122,442,291">
<figcaption>图 7.12 $D$ 最优、$A$ 最优、$E$ 最优设计和均匀设计对应的 90% 置信椭球的形状。</figcaption>
<p class="figure-translation">图内文字：uniform——均匀设计。</p>
</figure>

### 7.5.3 扩展

#### 资源限制

假设每种实验都有对应的成本 $c_i$，它可以表示采用 $v_i$ 进行一次实验所需的经济成本或时间。那么，总成本或所需总时间（若实验按顺序进行）为

$$
m_1c_1+\cdots+m_pc_p=mc^T\lambda.
$$

在基本实验设计问题中加入线性不等式 $mc^T\lambda\leq B$，就可以限制总成本，其中 $B$ 是预算。还可以加入多个线性不等式，表示多种资源的限制。

#### 每次实验进行多项测量

也可以考虑一种推广：每次实验得到多项测量。换言之，采用某个可能的实验选项进行一次实验时，会得到若干测量值。为这种情况建模，可以沿用前面的记号，但令 $v_i$ 为 $\mathbf{R}^{n\times k_i}$ 中的矩阵：

$$
v_i=\begin{bmatrix}u_{i1}&\cdots&u_{ik_i}\end{bmatrix},
$$

其中 $k_i$ 是进行实验 $v_i$ 时获得的标量测量数。在这个更复杂的设定中，误差协方差矩阵的形式完全相同。

结合表示成本或时间限制的额外线性不等式，可以为同时进行一组测量所带来的折扣或时间节省建模。例如，假设同时进行标量测量 $v_1$ 和 $v_2$ 的成本，低于分别<!-- pdf-page: 405 -->进行这两项测量的成本之和。可以取 $v_3$ 为矩阵

$$
v_3=\begin{bmatrix}v_1&v_2\end{bmatrix},
$$

并分别为单独进行第一项测量、单独进行第二项测量，以及同时进行两项测量指定成本 $c_1,c_2,c_3$。

求解实验设计问题后，$\lambda_1$ 给出应该单独进行第一种实验的次数比例，$\lambda_2$ 给出应该单独进行第二种实验的次数比例，$\lambda_3$ 给出应该同时进行这两种实验的次数比例。（通常会在这些方式之间作出取舍，不会预期 $\lambda_1>0$、$\lambda_2>0$ 和 $\lambda_3>0$ 同时成立。）

<!-- pdf-page: 406 -->

## 文献说明

统计学、模式识别、统计信号处理或通信方面的书籍，都介绍了 ML 与 MAP 估计、假设检验和检测；例如，参见 Bickel 和 Doksum [BD77]、Duda、Hart 和 Stork [DHS99]、Scharf [Sch91] 或 Proakis [Pro01]。

Hastie、Tibshirani 和 Friedman [HTF01，§4.4] 讨论了 logistic 回归。关于第 355 页的协方差估计问题，参见 Anderson [And70]。

20 世纪 60 年代，Isii [Isi64]、Marshall 和 Olkin [MO60]、Karlin 和 Studden [KS66，第 12 章] 等人广泛研究了 Chebyshev 不等式的推广。较近时期，Bertsimas 和 Sethuraman [BS00] 以及 Lasserre [Las02] 建立了它与半定规划的联系。

§7.5 中的术语（$A$、$D$ 和 $E$ 最优性）是最优实验设计文献中的标准用语，例如参见 Pukelsheim [Puk93]。Titterington [Tit75] 讨论了 $D$ 最优设计对偶问题的几何解释。

<!-- pdf-page: 407 -->

## 习题

### 估计

**7.1 带指数分布噪声的线性测量。** 当噪声服从指数分布，密度为

$$
p(z)=\begin{cases}(1/a)e^{-z/a}&z\geq0\\0&z<0,\end{cases}
$$

其中 $a>0$ 时，说明如何求解 ML 估计问题 (7.2)。

**7.2 ML 估计与 $\ell_\infty$ 范数逼近。** 考虑第 352 页的线性测量模型 $y=Ax+v$，噪声服从如下形式的均匀分布：

$$
p(z)=\begin{cases}1/(2\alpha)&|z|\leq\alpha\\0&|z|>\alpha.\end{cases}
$$

如第 352 页的例 7.1 所述，任意满足 $\|Ax-y\|_\infty\leq\alpha$ 的 $x$ 都是一个 ML 估计。

现在假设参数 $\alpha$ 未知，希望同时估计 $\alpha$ 和参数 $x$。证明：求解 $\ell_\infty$ 范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-y\|_\infty,
\end{array}
$$

就可以得到 $x$ 和 $\alpha$ 的 ML 估计，其中 $a_i^T$ 是 $A$ 的各行。

**7.3 Probit 模型。** 假设随机变量 $y\in\{0,1\}$ 由下式给出：

$$
y=\begin{cases}1&a^Tu+b+v\leq0\\0&a^Tu+b+v>0,\end{cases}
$$

其中向量 $u\in\mathbf{R}^n$ 是解释变量向量（与第 354 页介绍的 logistic 模型一样），$v$ 是均值为零、方差为一的高斯变量。

给定由数对 $(u_i,y_i)$，$i=1,\ldots,N$ 组成的数据，将估计 $a$ 和 $b$ 的 ML 估计问题表述为凸优化问题。

**7.4 多元正态分布的协方差与均值估计。** 考虑根据 $N$ 个独立样本 $y_1,y_2,\ldots,y_N\in\mathbf{R}^n$，估计高斯概率密度函数

$$
p_{R,a}(y)=(2\pi)^{-n/2}\det(R)^{-1/2}\exp(-(y-a)^TR^{-1}(y-a)/2)
$$

的协方差矩阵 $R$ 和均值 $a$ 的问题。

- (a) 先考虑对 $R$ 和 $a$ 没有额外约束时的估计问题。设 $\mu$ 和 $Y$ 分别为样本均值与样本协方差，定义为

    $$
    \mu=\frac{1}{N}\sum_{k=1}^N y_k,\qquad
    Y=\frac{1}{N}\sum_{k=1}^N(y_k-\mu)(y_k-\mu)^T.
    $$

    证明对数似然函数

    $$
    l(R,a)=-(Nn/2)\log(2\pi)-(N/2)\log\det R-(1/2)\sum_{k=1}^N(y_k-a)^TR^{-1}(y_k-a)
    $$

    <!-- pdf-page: 408 -->

    可以写成

    $$
    l(R,a)=\frac{N}{2}\bigl(-n\log(2\pi)-\log\det R-\operatorname{\mathbf{tr}}(R^{-1}Y)-(a-\mu)^TR^{-1}(a-\mu)\bigr).
    $$

    利用这个表达式证明：若 $Y\succ0$，$R$ 和 $a$ 的 ML 估计唯一，并且为

    $$
    a_{\mathrm{ml}}=\mu,\qquad R_{\mathrm{ml}}=Y.
    $$

- (b) 对数似然函数中包含一个凸项 $-\log\det R$，所以不能直接看出它是凹函数。证明：在由

    $$
    R\preceq2Y
    $$

    定义的区域内，$l$ 关于 $R$ 和 $a$ 联合为凹函数。

    这意味着，只要约束中包含 $R\preceq2Y$，就可以用凸优化同时计算满足凸约束的 $R$ 和 $a$ 的 ML 估计；也就是说，估计值 $R$ 不能超过无约束 ML 估计值的两倍。

**7.5 Markov 链估计。** 考虑一个有 $n$ 个状态的 Markov 链，其转移概率矩阵 $P\in\mathbf{R}^{n\times n}$ 定义为

$$
P_{ij}=\mathbf{prob}(y(t+1)=i\mid y(t)=j).
$$

转移概率必须满足 $P_{ij}\geq0$ 以及 $\sum_{i=1}^nP_{ij}=1$，$j=1,\ldots,n$。我们考虑根据观测到的样本序列 $y(1)=k_1$、$y(2)=k_2$、$\ldots$、$y(N)=k_n$，估计转移概率的问题。

- (a) 证明：如果对 $P_{ij}$ 没有其他先验约束，那么 ML 估计就是经验转移频率：$\widehat P_{ij}$ 等于观测样本中状态从 $j$ 转移到 $i$ 的次数，除以状态为 $j$ 的次数。

- (b) 假设已知这个 Markov 链的一个平衡分布 $p$，即一个满足 $\mathbf{1}^Tq=1$ 和 $Pq=q$ 的向量 $q\in\mathbf{R}_+^n$。证明：在给定观测序列和已知 $q$ 的条件下，计算 $P$ 的 ML 估计可以表述为一个凸优化问题。

**7.6 均值与方差的估计。** 考虑密度为 $p$ 的随机变量 $x\in\mathbf{R}$，它已经标准化，即均值为零、方差为一。对 $x$ 作仿射变换，得到随机变量 $y=(x+b)/a$，其中 $a>0$。随机变量 $y$ 的均值为 $b/a$，方差为 $1/a^2$。当 $a$ 和 $b$ 分别在 $\mathbf{R}_+$ 和 $\mathbf{R}$ 中取值时，就得到由 $p$ 经缩放和平移而生成的一族密度，其中每个密度都由其均值和方差唯一确定。

证明：如果 $p$ 是对数凹的，那么根据 $y$ 的样本 $y_1,\ldots,y_n$ 求 $a$ 和 $b$ 的 ML 估计是一个凸问题。

作为例子，假设 $p$ 是标准化的 Laplace 密度 $p(x)=e^{-2|x|}$，求出 $a$ 和 $b$ 的 ML 估计的解析解。

<div class="translator-note" markdown="1">

**译注（Laplace 密度的方差）：** 本题给出的 Laplace 密度 $p(x)=e^{-2|x|}$ 的方差为 $1/2$，与题首单位方差的标准化假设不同。采用这个密度时，$y$ 的方差为 $1/(2a^2)$。

</div>

**7.7 Poisson 分布的 ML 估计。** 设 $x_i$，$i=1,\ldots,n$，是相互独立的随机变量，服从 Poisson 分布

$$
\mathbf{prob}(x_i=k)=\frac{e^{-\mu_i}\mu_i^k}{k!},
$$

其均值 $\mu_i$ 未知。变量 $x_i$ 表示 $n$ 种可能发生的独立事件中，第 $i$ 种事件在某段时间内发生的次数。例如，在发射断层成像中，它们可以表示 $n$ 个源发射的光子数。

我们考虑一个旨在确定均值 $\mu_i$ 的实验。实验使用 $m$ 个检测器。如果事件 $i$ 发生，它被检测器 $j$ 检测到的概率为 $p_{ji}$。假设<!-- pdf-page: 409 -->概率 $p_{ji}$ 已知，并满足 $p_{ji}\geq0$、$\sum_{j=1}^m p_{ji}\leq1$。检测器 $j$ 记录的事件总数记为 $y_j$，

$$
y_j=\sum_{i=1}^n y_{ji},\qquad j=1,\ldots,m.
$$

将根据 $y_j$，$j=1,\ldots,m$，的观测值估计均值 $\mu_i$ 的 ML 估计问题，表述为一个凸优化问题。

**提示。** 变量 $y_{ji}$ 服从均值为 $p_{ji}\mu_i$ 的 Poisson 分布，即

$$
\mathbf{prob}(y_{ji}=k)=\frac{e^{-p_{ji}\mu_i}(p_{ji}\mu_i)^k}{k!}.
$$

$n$ 个相互独立、均值分别为 $\lambda_1,\ldots,\lambda_n$ 的 Poisson 随机变量之和，服从均值为 $\lambda_1+\cdots+\lambda_n$ 的 Poisson 分布。

**7.8 利用符号测量进行估计。** 考虑如下测量模型：

$$
y_i=\mathbf{sign}(a_i^Tx+b_i+v_i),\qquad i=1,\ldots,m,
$$

其中 $x\in\mathbf{R}^n$ 是待估向量，$y_i\in\{-1,1\}$ 是测量值。向量 $a_i\in\mathbf{R}^n$ 和标量 $b_i\in\mathbf{R}$ 已知，$v_i$ 是独立同分布的噪声，其概率密度为对数凹函数。（可以假设 $a_i^Tx+b_i+v_i=0$ 的情况不会发生。）证明：$x$ 的最大似然估计是一个凸优化问题。

**7.9 传感器非线性未知时的估计。** 考虑如下测量模型：

$$
y_i=f(a_i^Tx+b_i+v_i),\qquad i=1,\ldots,m,
$$

其中 $x\in\mathbf{R}^n$ 是待估向量，$y_i\in\mathbf{R}$ 是测量值，$a_i\in\mathbf{R}^n$、$b_i\in\mathbf{R}$ 已知，$v_i$ 是独立同分布的噪声，其概率密度为对数凹函数。函数 $f:\mathbf{R}\to\mathbf{R}$ 表示测量中的非线性关系，其具体形式未知。不过，已知对所有 $t$ 都有 $f'(t)\in[l,u]$，其中 $0<l<u$ 已给定。

说明如何利用凸优化求出 $x$ 以及函数 $f$ 的最大似然估计。（这是一个无限维的 ML 估计问题，但求解思路和说明可以不作严格的形式化。）

**7.10 $\mathbf{R}^k$ 上的非参数分布。** 考虑随机变量 $x\in\mathbf{R}^k$，其取值位于有限集合 $\{\alpha_1,\ldots,\alpha_n\}$ 中，分布为

$$
p_i=\mathbf{prob}(x=\alpha_i),\qquad i=1,\ldots,n.
$$

证明：对 $X$ 的协方差施加下界

$$
S\preceq\mathbf{E}(X-\mathbf{E}\,X)(X-\mathbf{E}\,X)^T,
$$

是关于 $p$ 的凸约束。

### 最优检测器设计

**7.11 随机化检测器。** 证明：每个随机化检测器都可以表示为一组确定性检测器的凸组合。也就是说，如果

$$
T=\begin{bmatrix}t_1&t_2&\cdots&t_n\end{bmatrix}\in\mathbf{R}^{m\times n}
$$

满足 $t_k\succeq0$ 和 $\mathbf{1}^Tt_k=1$，那么 $T$ 可以表示为

$$
T=\theta_1T_1+\cdots+\theta_NT_N,
$$

<!-- pdf-page: 410 -->

其中 $T_i$ 是每列恰有一个元素等于一的零一矩阵，且 $\theta_i\geq0$、$\sum_{i=1}^N\theta_i=1$。我们最多可能需要多少个确定性检测器，即 $N$ 最大需要取多大？

可以如下解释这一凸分解。随机化检测器可以由一组 $N$ 个确定性检测器实现。当观测到 $X=k$ 时，估计器从集合 $\{1,\ldots,N\}$ 中随机选择一个下标，选择概率为 $\mathbf{prob}(j=i)=\theta_i$，然后使用确定性检测器 $T_j$。

**7.12 最优行动。** 在检测器设计中，给定矩阵 $P\in\mathbf{R}^{n\times m}$（其各列为概率分布），然后设计矩阵 $T\in\mathbf{R}^{m\times n}$（其各列为概率分布），使 $D=TP$ 的对角元素较大，而非对角元素较小。本题研究对偶问题：给定 $P$，求矩阵 $S\in\mathbf{R}^{m\times n}$（其各列为概率分布），使 $\widetilde D=PS\in\mathbf{R}^{n\times n}$ 的对角元素较大，而非对角元素较小。为使问题明确，将目标取为最大化 $\widetilde D$ 的最小对角元素。

可以如下解释这个问题。共有 $n$ 种可能的结果，其发生概率取决于我们选择 $m$ 种输入或行动中的哪一种：$P_{ij}$ 是采取行动 $j$ 时出现结果 $i$ 的概率。我们的目标是找到一种随机化策略，使任意指定的结果尽可能发生。策略由矩阵 $S$ 给出：$S_{ji}$ 是希望结果 $i$ 发生时采取行动 $j$ 的概率。矩阵 $\widetilde D$ 给出行动错误概率矩阵：$\widetilde D_{ij}$ 是希望结果 $j$ 发生时，实际出现结果 $i$ 的概率。特别地，$\widetilde D_{ii}$ 是希望结果 $i$ 发生时，它确实发生的概率。

证明：这个问题有简单的解析解。证明：与对应的检测器问题不同，总存在一个确定性的最优解。

*提示。* 证明问题关于 $S$ 的各列可分。

### Chebyshev 与 Chernoff 界

**7.13 有限集合上的 Chebyshev 型不等式。** 假设随机变量 $X$ 在集合 $\{\alpha_1,\alpha_2,\ldots,\alpha_m\}$ 中取值，令 $S$ 为 $\{\alpha_1,\ldots,\alpha_m\}$ 的一个子集。$X$ 的分布未知，但已给定 $n$ 个函数 $f_i$ 的期望值：

$$
\mathbf{E}\,f_i(X)=b_i,\qquad i=1,\ldots,n.
\tag{7.32}
$$

证明：变量为 $x_0,\ldots,x_n$ 的线性规划

$$
\begin{array}{ll}
\text{最小化} & \displaystyle x_0+\sum_{i=1}^n b_ix_i\\
\text{约束条件} & \displaystyle x_0+\sum_{i=1}^n f_i(\alpha)x_i\geq1,\quad\alpha\in S\\
& \displaystyle x_0+\sum_{i=1}^n f_i(\alpha)x_i\geq0,\quad\alpha\notin S,
\end{array}
$$

的最优值是 $\mathbf{prob}(X\in S)$ 的上界，且这个界对所有满足 (7.32) 的分布都成立。证明总存在一个分布达到这个上界。
