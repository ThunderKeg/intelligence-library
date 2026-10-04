<!-- pdf-page: 229 -->

# 第 5 章 对偶性

<aside class="chapter-guide"><p>导读（编者）：本章从拉格朗日函数出发，说明如何用对偶函数为原问题的最优值提供下界，再寻找其中最好的下界。阅读时应区分原问题与对偶问题的可行性，并留意弱对偶性、强对偶性各自需要的条件。后续的最优性条件与灵敏度分析，将进一步说明最优解如何与约束及其乘子联系起来。</p></aside>

## 5.1 拉格朗日对偶函数

### 5.1.1 拉格朗日函数

考虑标准形式 (4.1) 的优化问题：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
\tag{5.1}
$$

其中变量为 $x\in\mathbf{R}^n$。假设其定义域 $\mathcal{D}=\bigcap_{i=0}^m\operatorname{\mathbf{dom}}f_i\cap\bigcap_{i=1}^p\operatorname{\mathbf{dom}}h_i$ 非空，并将 (5.1) 的最优值记为 $p^\star$。我们不假设问题 (5.1) 是凸的。

拉格朗日对偶性的基本思想是：在目标函数中加入各个约束函数的加权和，以此考虑 (5.1) 中的约束。将与问题 (5.1) 对应的**拉格朗日函数**（Lagrangian）$L:\mathbf{R}^n\times\mathbf{R}^m\times\mathbf{R}^p\to\mathbf{R}$ 定义为

$$
L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\nu_i h_i(x),
$$

其定义域为 $\operatorname{\mathbf{dom}}L=\mathcal{D}\times\mathbf{R}^m\times\mathbf{R}^p$。称 $\lambda_i$ 为第 $i$ 个不等式约束 $f_i(x)\leq0$ 对应的**拉格朗日乘子**；类似地，称 $\nu_i$ 为第 $i$ 个等式约束 $h_i(x)=0$ 对应的拉格朗日乘子。向量 $\lambda$ 和 $\nu$ 称为问题 (5.1) 对应的**对偶变量**，或**拉格朗日乘子向量**。

<!-- pdf-page: 230 -->

### 5.1.2 拉格朗日对偶函数

将**拉格朗日对偶函数**（或简称**对偶函数**）$g:\mathbf{R}^m\times\mathbf{R}^p\to\mathbf{R}$ 定义为拉格朗日函数关于 $x$ 的最小值：对于 $\lambda\in\mathbf{R}^m$、$\nu\in\mathbf{R}^p$，

$$
g(\lambda,\nu)=\inf_{x\in\mathcal{D}}L(x,\lambda,\nu)=\inf_{x\in\mathcal{D}}\left(f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\nu_i h_i(x)\right).
$$

当拉格朗日函数关于 $x$ 无下界时，对偶函数取值为 $-\infty$。对偶函数是一族关于 $(\lambda,\nu)$ 的仿射函数的逐点下确界，因此它是凹函数，即使问题 (5.1) 不是凸的，也依然如此。

### 5.1.3 最优值的下界

对偶函数给出了问题 (5.1) 的最优值 $p^\star$ 的下界：对于任意 $\lambda\succeq0$ 和任意 $\nu$，都有

$$
g(\lambda,\nu)\leq p^\star.
\tag{5.2}
$$

这个重要性质很容易验证。设 $\widetilde{x}$ 是问题 (5.1) 的一个可行点，即 $f_i(\widetilde{x})\leq0$、$h_i(\widetilde{x})=0$，并且 $\lambda\succeq0$。于是

$$
\sum_{i=1}^m\lambda_i f_i(\widetilde{x})+\sum_{i=1}^p\nu_i h_i(\widetilde{x})\leq0,
$$

因为第一个和式中的每一项都非正，第二个和式中的每一项都为零。因此，

$$
L(\widetilde{x},\lambda,\nu)=f_0(\widetilde{x})+\sum_{i=1}^m\lambda_i f_i(\widetilde{x})+\sum_{i=1}^p\nu_i h_i(\widetilde{x})\leq f_0(\widetilde{x}).
$$

从而

$$
g(\lambda,\nu)=\inf_{x\in\mathcal{D}}L(x,\lambda,\nu)\leq L(\widetilde{x},\lambda,\nu)\leq f_0(\widetilde{x}).
$$

由于 $g(\lambda,\nu)\leq f_0(\widetilde{x})$ 对每个可行点 $\widetilde{x}$ 都成立，所以得到不等式 (5.2)。图 5.1 用一个变量 $x\in\mathbf{R}$、只有一个不等式约束的简单问题，展示了下界 (5.2)。

当 $g(\lambda,\nu)=-\infty$ 时，不等式 (5.2) 仍成立，但不能提供有用的信息。只有当 $\lambda\succeq0$ 且 $(\lambda,\nu)\in\operatorname{\mathbf{dom}}g$，即 $g(\lambda,\nu)>-\infty$ 时，对偶函数才给出 $p^\star$ 的一个非平凡下界。对于满足 $\lambda\succeq0$ 且 $(\lambda,\nu)\in\operatorname{\mathbf{dom}}g$ 的一对 $(\lambda,\nu)$，称其为**对偶可行的**；采用这个名称的原因将在后面说明。

### 5.1.4 线性逼近的解释

利用集合 $\{0\}$ 和 $-\mathbf{R}_+$ 的指示函数的线性逼近，可以对拉格朗日函数及其下界性质给出一个简单解释。

<!-- pdf-page: 231 -->

<figure id="fig-5-1" data-figure="5.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-1.png" alt="目标函数、约束函数和多条拉格朗日函数曲线，两条竖向点线界定可行区间，圆点标出原问题的最优点及最优值" data-source-page="231" data-source-rect="181,172,386,343">
<figcaption>图 5.1 由对偶可行点得到的下界。实线表示目标函数 $f_0$，虚线表示约束函数 $f_1$。可行集是区间 $[-0.46,0.46]$，由两条竖向点线标出。最优点和最优值分别为 $x^\star=-0.46$、$p^\star=1.54$（用圆点表示）。点线曲线表示 $\lambda=0.1,0.2,\ldots,1.0$ 时的 $L(x,\lambda)$。每条曲线的最小值都小于 $p^\star$，因为在可行集上，当 $\lambda\geq0$ 时，有 $L(x,\lambda)\leq f_0(x)$。</figcaption>
</figure>

<figure id="fig-5-2" data-figure="5.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-2.png" alt="凹的对偶函数曲线和表示原问题最优值的水平虚线" data-source-page="231" data-source-rect="168,424,386,595">
<figcaption>图 5.2 图 5.1 中问题的对偶函数 $g$。$f_0$ 和 $f_1$ 都不是凸函数，但对偶函数是凹函数。水平虚线表示该问题的最优值 $p^\star$。</figcaption>
</figure>

<!-- pdf-page: 232 -->

先将原问题 (5.1) 改写为无约束问题

$$
\text{最小化}\quad f_0(x)+\sum_{i=1}^m I_-(f_i(x))+\sum_{i=1}^p I_0(h_i(x)),
\tag{5.3}
$$

其中 $I_-:\mathbf{R}\to\mathbf{R}$ 是非正实数集合的指示函数，

$$
I_-(u)=\begin{cases}0&u\leq0\\\infty&u>0,\end{cases}
$$

类似地，$I_0$ 是集合 $\{0\}$ 的指示函数。在形式 (5.3) 中，可以把 $I_-(u)$ 解释为约束函数取值 $u=f_i(x)$ 所引起的烦恼或不满程度：当 $f_i(x)\leq0$ 时，它为零；当 $f_i(x)>0$ 时，它为无穷大。类似地，$I_0(u)$ 表示我们对等式约束取值 $u=h_i(x)$ 的不满程度。可以将 $I_-$ 看作“砖墙”式或“无限刚硬”的不满函数：当 $f_i(x)$ 从非正变为正时，不满程度从零跳到无穷大。

现在，假设在形式 (5.3) 中，用线性函数 $\lambda_i u$ 替换函数 $I_-(u)$，其中 $\lambda_i\geq0$，并用 $\nu_i u$ 替换函数 $I_0(u)$。目标函数就变成拉格朗日函数 $L(x,\lambda,\nu)$，而对偶函数值 $g(\lambda,\nu)$ 就是下列问题的最优值：

$$
\text{最小化}\quad L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\nu_i h_i(x).
\tag{5.4}
$$

在这个形式中，用线性或“软”的不满函数替换了 $I_-$ 和 $I_0$。对于不等式约束，当 $f_i(x)=0$ 时，不满程度为零；当 $f_i(x)>0$ 时，若 $\lambda_i>0$，不满程度为正，而且随着约束违反程度的加深而增大。在原形式中，只要 $f_i(x)$ 非正，就都可以接受；而在这种软化的形式中，约束具有裕量，即 $f_i(x)<0$ 时，实际上还会带来“满意”。

显然，用线性函数 $\lambda_i u$ 逼近指示函数 $I_-(u)$，逼近效果相当差。不过，这个线性函数至少是指示函数的下界函数。由于对所有 $u$ 都有 $\lambda_i u\leq I_-(u)$ 和 $\nu_i u\leq I_0(u)$，立即可知，对偶函数给出了原问题最优值的一个下界。

将“硬”约束替换为“软”约束的思想，还会在讨论内点法时再次出现（§11.2.1）。

### 5.1.5 例子

本节给出一些能够推导出拉格朗日对偶函数解析表达式的例子。

#### 线性方程的最小二乘解

考虑问题

$$
\begin{array}{ll}
\text{最小化} & x^Tx\\
\text{约束条件} & Ax=b,
\end{array}
\tag{5.5}
$$

其中 $A\in\mathbf{R}^{p\times n}$。这个问题没有不等式约束，有 $p$ 个线性等式约束。其拉格朗日函数为 $L(x,\nu)=x^Tx+\nu^T(Ax-b)$，定义域为 $\mathbf{R}^n\times\mathbf{R}^p$。<!-- pdf-page: 233 -->对偶函数为 $g(\nu)=\inf_x L(x,\nu)$。由于 $L(x,\nu)$ 是关于 $x$ 的凸二次函数，可以根据最优性条件

$$
\nabla_xL(x,\nu)=2x+A^T\nu=0,
$$

求得使其最小的 $x=-(1/2)A^T\nu$。因此，对偶函数为

$$
g(\nu)=L(-(1/2)A^T\nu,\nu)=-(1/4)\nu^TAA^T\nu-b^T\nu,
$$

这是一个凹二次函数，定义域为 $\mathbf{R}^p$。下界性质 (5.2) 表明，对于任意 $\nu\in\mathbf{R}^p$，都有

$$
-(1/4)\nu^TAA^T\nu-b^T\nu\leq\inf\{x^Tx\mid Ax=b\}.
$$

#### 标准形式 LP

考虑标准形式的 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax=b\\
& x\succeq0,
\end{array}
\tag{5.6}
$$

其不等式约束函数为 $f_i(x)=-x_i$，$i=1,\ldots,n$。为构造拉格朗日函数，给这 $n$ 个不等式约束引入乘子 $\lambda_i$，给各个等式约束引入乘子 $\nu_i$，得到

$$
L(x,\lambda,\nu)=c^Tx-\sum_{i=1}^n\lambda_i x_i+\nu^T(Ax-b)=-b^T\nu+(c+A^T\nu-\lambda)^Tx.
$$

对偶函数为

$$
g(\lambda,\nu)=\inf_x L(x,\lambda,\nu)=-b^T\nu+\inf_x(c+A^T\nu-\lambda)^Tx,
$$

很容易写出其解析表达式，因为线性函数只有在恒等于零时才有下界。因此，除非 $c+A^T\nu-\lambda=0$，否则 $g(\lambda,\nu)=-\infty$；当这个等式成立时，对偶函数值为 $-b^T\nu$：

$$
g(\lambda,\nu)=\begin{cases}-b^T\nu&A^T\nu-\lambda+c=0\\-\infty&\text{其他情形。}\end{cases}
$$

注意，对偶函数 $g$ 只在 $\mathbf{R}^m\times\mathbf{R}^p$ 的一个真仿射子集上取有限值。我们将会看到，这种情况经常出现。

只有当 $\lambda$ 和 $\nu$ 满足 $\lambda\succeq0$ 及 $A^T\nu-\lambda+c=0$ 时，下界性质 (5.2) 才能给出非平凡下界。在这种情况下，$-b^T\nu$ 就是 LP (5.6) 最优值的一个下界。

#### 两路划分问题

考虑非凸问题

$$
\begin{array}{ll}
\text{最小化} & x^TWx\\
\text{约束条件} & x_i^2=1,\quad i=1,\ldots,n,
\end{array}
\tag{5.7}
$$

<!-- pdf-page: 234 -->

其中 $W\in\mathbf{S}^n$。约束将 $x_i$ 的取值限制为 $1$ 或 $-1$，所以这个问题等价于：在各分量均为 $\pm1$ 的向量中，寻找使 $x^TWx$ 最小的向量。这里的可行集是有限的，包含 $2^n$ 个点，因此原则上只需逐个检查可行点的目标值，就能求解这个问题。不过，可行点的数量呈指数增长，所以这种方法只适用于小问题，例如 $n\leq30$。一般来说，当 $n$ 大于 50 左右时，问题 (5.7) 就很难求解。

问题 (5.7) 可以解释为对含有 $n$ 个元素的集合，例如 $\{1,\ldots,n\}$，进行**两路划分**（two-way partitioning）的问题。一个可行向量 $x$ 对应于划分

$$
\{1,\ldots,n\}=\{i\mid x_i=-1\}\cup\{i\mid x_i=1\}.
$$

矩阵元素 $W_{ij}$ 可以解释为把元素 $i$ 和 $j$ 分到同一组的代价，而 $-W_{ij}$ 是把 $i$ 和 $j$ 分到不同组的代价。问题 (5.7) 的目标函数是所有元素对的总代价；问题本身就是寻找总代价最小的划分。

现在推导这个问题的对偶函数。其拉格朗日函数为

$$
\begin{aligned}
L(x,\nu)&=x^TWx+\sum_{i=1}^n\nu_i(x_i^2-1)\\
&=x^T(W+\operatorname{\mathbf{diag}}(\nu))x-\mathbf{1}^T\nu.
\end{aligned}
$$

对 $x$ 取最小值，得到拉格朗日对偶函数：

$$
\begin{aligned}
g(\nu)&=\inf_x x^T(W+\operatorname{\mathbf{diag}}(\nu))x-\mathbf{1}^T\nu\\
&=\begin{cases}-\mathbf{1}^T\nu&W+\operatorname{\mathbf{diag}}(\nu)\succeq0\\-\infty&\text{其他情形，}\end{cases}
\end{aligned}
$$

这里用到了如下事实：二次型的下确界要么为零（当二次型半正定时），要么为 $-\infty$（当二次型不是半正定时）。

这个对偶函数为难以求解的问题 (5.7) 的最优值提供了下界。例如，可以为对偶变量选取具体值

$$
\nu=-\lambda_{\min}(W)\mathbf{1},
$$

它是对偶可行的，因为

$$
W+\operatorname{\mathbf{diag}}(\nu)=W-\lambda_{\min}(W)I\succeq0.
$$

由此得到最优值 $p^\star$ 的下界

$$
p^\star\geq-\mathbf{1}^T\nu=n\lambda_{\min}(W).
\tag{5.8}
$$

<div class="remark" markdown="1">

**注 5.1** 不使用拉格朗日对偶函数，也可以得到 $p^\star$ 的这个下界。先将约束 $x_1^2=1,\ldots,x_n^2=1$ 替换为 $\sum_{i=1}^n x_i^2=n$，得到修改后的问题

$$
\begin{array}{ll}
\text{最小化} & x^TWx\\
\text{约束条件} & \displaystyle\sum_{i=1}^n x_i^2=n.
\end{array}
\tag{5.9}
$$

<!-- pdf-page: 235 -->

原问题 (5.7) 的约束蕴含这里的约束，因此问题 (5.9) 的最优值是 (5.7) 的最优值 $p^\star$ 的下界。而修改后的问题 (5.9) 很容易作为特征值问题求解，其最优值为 $n\lambda_{\min}(W)$。

</div>

### 5.1.6 拉格朗日对偶函数与共轭函数

回顾 §3.3，函数 $f:\mathbf{R}^n\to\mathbf{R}$ 的共轭函数 $f^*$ 为

$$
f^*(y)=\sup_{x\in\operatorname{\mathbf{dom}}f}\left(y^Tx-f(x)\right).
$$

共轭函数与拉格朗日对偶函数密切相关。为说明一个简单的联系，考虑问题

$$
\begin{array}{ll}
\text{最小化} & f(x)\\
\text{约束条件} & x=0.
\end{array}
$$

这个问题本身并没有什么特别之处，观察即可求解。其拉格朗日函数为 $L(x,\nu)=f(x)+\nu^Tx$，对偶函数为

$$
g(\nu)=\inf_x\left(f(x)+\nu^Tx\right)=-\sup_x\left((-\nu)^Tx-f(x)\right)=-f^*(-\nu).
$$

更一般地，也更有用地，考虑带有线性不等式约束和线性等式约束的优化问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & Ax\preceq b\\
& Cx=d.
\end{array}
\tag{5.10}
$$

利用 $f_0$ 的共轭函数，可以将问题 (5.10) 的对偶函数写成

$$
\begin{aligned}
g(\lambda,\nu)&=\inf_x\left(f_0(x)+\lambda^T(Ax-b)+\nu^T(Cx-d)\right)\\
&=-b^T\lambda-d^T\nu+\inf_x\left(f_0(x)+(A^T\lambda+C^T\nu)^Tx\right)\\
&=-b^T\lambda-d^T\nu-f_0^*(-A^T\lambda-C^T\nu).
\end{aligned}
\tag{5.11}
$$

$g$ 的定义域由 $f_0^*$ 的定义域得到：

$$
\operatorname{\mathbf{dom}}g=\{(\lambda,\nu)\mid-A^T\lambda-C^T\nu\in\operatorname{\mathbf{dom}}f_0^*\}.
$$

下面用几个例子说明。

#### 带等式约束的范数最小化

考虑问题

$$
\begin{array}{ll}
\text{最小化} & \|x\|\\
\text{约束条件} & Ax=b,
\end{array}
\tag{5.12}
$$

<!-- pdf-page: 236 -->

其中 $\|\cdot\|$ 是任意范数。回顾原书第 93 页例 3.26，$f_0=\|\cdot\|$ 的共轭函数为

$$
f_0^*(y)=\begin{cases}0&\|y\|_*\leq1\\\infty&\text{其他情形，}\end{cases}
$$

即对偶范数单位球的指示函数。

利用上面的结果 (5.11)，问题 (5.12) 的对偶函数为

$$
g(\nu)=-b^T\nu-f_0^*(-A^T\nu)=\begin{cases}-b^T\nu&\|A^T\nu\|_*\leq1\\-\infty&\text{其他情形。}\end{cases}
$$

#### 熵最大化

考虑熵最大化问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle f_0(x)=\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Ax\preceq b\\
& \mathbf{1}^Tx=1,
\end{array}
\tag{5.13}
$$

其中 $\operatorname{\mathbf{dom}}f_0=\mathbf{R}_{++}^n$。标量变量 $u$ 的负熵函数 $u\log u$ 的共轭函数为 $e^{v-1}$（见原书第 91 页例 3.21）。由于 $f_0$ 是不同变量的负熵函数之和，其共轭函数为

$$
f_0^*(y)=\sum_{i=1}^n e^{y_i-1},
$$

定义域为 $\operatorname{\mathbf{dom}}f_0^*=\mathbf{R}^n$。利用上面的结果 (5.11)，(5.13) 的对偶函数为

$$
g(\lambda,\nu)=-b^T\lambda-\nu-\sum_{i=1}^n e^{-a_i^T\lambda-\nu-1}=-b^T\lambda-\nu-e^{-\nu-1}\sum_{i=1}^n e^{-a_i^T\lambda},
$$

其中 $a_i$ 是 $A$ 的第 $i$ 列。

#### 最小体积覆盖椭球

考虑变量为 $X\in\mathbf{S}^n$ 的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(X)=\log\det X^{-1}\\
\text{约束条件} & a_i^TXa_i\leq1,\quad i=1,\ldots,m,
\end{array}
\tag{5.14}
$$

其中 $\operatorname{\mathbf{dom}}f_0=\mathbf{S}_{++}^n$。问题 (5.14) 有一个简单的几何解释。为每个 $X\in\mathbf{S}_{++}^n$ 对应一个以原点为中心的椭球

$$
\mathcal{E}_X=\{z\mid z^TXz\leq1\}.
$$

这个椭球的体积与 $(\det X^{-1})^{1/2}$ 成正比，因此，除了一个常数和一个因子 2，(5.14) 的目标函数就是椭球 $\mathcal{E}_X$ 体积<!-- pdf-page: 237 -->的对数。问题 (5.14) 的约束表示 $a_i\in\mathcal{E}_X$。所以，问题 (5.14) 是要确定一个以原点为中心、包含所有点 $a_1,\ldots,a_m$ 的最小体积椭球。

问题 (5.14) 的不等式约束是仿射的，可以写成

$$
\operatorname{\mathbf{tr}}\left((a_i a_i^T)X\right)\leq1.
$$

在原书第 92 页例 3.23 中，已经求得 $f_0$ 的共轭函数为

$$
f_0^*(Y)=\log\det(-Y)^{-1}-n,
$$

定义域为 $\operatorname{\mathbf{dom}}f_0^*=-\mathbf{S}_{++}^n$。应用上面的结果 (5.11)，问题 (5.14) 的对偶函数为

$$
g(\lambda)=\begin{cases}\displaystyle\log\det\left(\sum_{i=1}^m\lambda_i a_i a_i^T\right)-\mathbf{1}^T\lambda+n&\displaystyle\sum_{i=1}^m\lambda_i a_i a_i^T\succ0\\-\infty&\text{其他情形。}\end{cases}
\tag{5.15}
$$

因此，对于满足 $\sum_{i=1}^m\lambda_i a_i a_i^T\succ0$ 的任意 $\lambda\succeq0$，数值

$$
\log\det\left(\sum_{i=1}^m\lambda_i a_i a_i^T\right)-\mathbf{1}^T\lambda+n
$$

都是问题 (5.14) 最优值的一个下界。

## 5.2 拉格朗日对偶问题

对于每一对满足 $\lambda\succeq0$ 的 $(\lambda,\nu)$，拉格朗日对偶函数都为优化问题 (5.1) 的最优值 $p^\star$ 提供一个下界。因此，我们得到了一个依赖于参数 $\lambda,\nu$ 的下界。自然会问：从拉格朗日对偶函数能够得到的最好下界是什么？

这就引出优化问题

$$
\begin{array}{ll}
\text{最大化} & g(\lambda,\nu)\\
\text{约束条件} & \lambda\succeq0.
\end{array}
\tag{5.16}
$$

这个问题称为与问题 (5.1) 对应的**拉格朗日对偶问题**。在这种语境下，原来的问题 (5.1) 有时称为**原问题**（primal problem）。现在，对于满足 $\lambda\succeq0$ 且 $g(\lambda,\nu)>-\infty$ 的一对 $(\lambda,\nu)$，称其为对偶可行，就有了明确的含义：正如名称所示，$(\lambda,\nu)$ 对于对偶问题 (5.16) 是可行的。如果 $(\lambda^\star,\nu^\star)$ 是问题 (5.16) 的最优解，就称其为**对偶最优解**或**最优拉格朗日乘子**。

拉格朗日对偶问题 (5.16) 是一个凸优化问题，因为要最大化的目标函数是凹函数，约束也是凸的。无论原问题 (5.1) 是否为凸问题，这一点都成立。

<!-- pdf-page: 238 -->

### 5.2.1 显式写出对偶约束

前面的例子表明，对偶函数的定义域

$$
\operatorname{\mathbf{dom}}g=\{(\lambda,\nu)\mid g(\lambda,\nu)>-\infty\}
$$

的维数小于 $m+p$，并不少见。在许多情形下，可以确定 $\operatorname{\mathbf{dom}}g$ 的仿射包，并用一组线性等式约束来描述。粗略地说，这意味着能够找出“隐藏”或“隐含”在对偶问题 (5.16) 的目标函数 $g$ 中的等式约束。此时，可以构造一个等价问题，将这些等式作为约束显式给出。下面的例子说明这种思路。

#### 标准形式 LP 的拉格朗日对偶

在原书第 219 页，我们求得标准形式 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax=b\\
& x\succeq0
\end{array}
\tag{5.17}
$$

的拉格朗日对偶函数为

$$
g(\lambda,\nu)=\begin{cases}-b^T\nu&A^T\nu-\lambda+c=0\\-\infty&\text{其他情形。}\end{cases}
$$

严格地说，标准形式 LP 的拉格朗日对偶问题，是在 $\lambda\succeq0$ 的约束下最大化这个对偶函数 $g$，即

$$
\begin{array}{ll}
\text{最大化} & g(\lambda,\nu)=\begin{cases}-b^T\nu&A^T\nu-\lambda+c=0\\-\infty&\text{其他情形}\end{cases}\\
\text{约束条件} & \lambda\succeq0.
\end{array}
\tag{5.18}
$$

这里，只有当 $A^T\nu-\lambda+c=0$ 时，$g$ 才取有限值。将这些等式约束显式写出，就得到一个等价问题：

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu\\
\text{约束条件} & A^T\nu-\lambda+c=0\\
& \lambda\succeq0.
\end{array}
\tag{5.19}
$$

这个问题又可以表示为

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu\\
\text{约束条件} & A^T\nu+c\succeq0,
\end{array}
\tag{5.20}
$$

它是不等式形式的 LP。

注意这三个问题之间的细微区别。标准形式 LP (5.17) 的拉格朗日对偶是问题 (5.18)，它与问题 (5.19)、(5.20) 等价，但并不是同一个问题。在术语使用上略作放宽，我们也把问题 (5.19) 或 (5.20) 称为标准形式 LP (5.17) 的拉格朗日对偶。

<!-- pdf-page: 239 -->

#### 不等式形式 LP 的拉格朗日对偶

用类似的方法，可以求出不等式形式线性规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b.
\end{array}
\tag{5.21}
$$

的拉格朗日对偶问题。其拉格朗日函数为

$$
L(x,\lambda)=c^Tx+\lambda^T(Ax-b)=-b^T\lambda+(A^T\lambda+c)^Tx,
$$

所以对偶函数为

$$
g(\lambda)=\inf_x L(x,\lambda)=-b^T\lambda+\inf_x(A^T\lambda+c)^Tx.
$$

线性函数的下确界为 $-\infty$，除非它恒等于零。因此，对偶函数为

$$
g(\lambda)=\begin{cases}-b^T\lambda&A^T\lambda+c=0\\-\infty&\text{其他情形。}\end{cases}
$$

当 $\lambda\succeq0$ 且 $A^T\lambda+c=0$ 时，对偶变量 $\lambda$ 是对偶可行的。

LP (5.21) 的拉格朗日对偶，是在所有 $\lambda\succeq0$ 上最大化 $g$。同样，可以将对偶可行性条件显式列为约束，改写为

$$
\begin{array}{ll}
\text{最大化} & -b^T\lambda\\
\text{约束条件} & A^T\lambda+c=0\\
& \lambda\succeq0,
\end{array}
\tag{5.22}
$$

这是标准形式的 LP。

注意标准形式和不等式形式的 LP 与各自的对偶之间有一种有趣的对称性：标准形式 LP 的对偶是只含不等式约束的 LP，反之亦然。还可以验证，(5.22) 的拉格朗日对偶等价于原问题 (5.21)。

### 5.2.2 弱对偶性

将拉格朗日对偶问题的最优值记为 $d^\star$。按照定义，它是由拉格朗日对偶函数能够得到的、关于 $p^\star$ 的最好下界。特别地，有如下简单而重要的不等式：

$$
d^\star\leq p^\star,
\tag{5.23}
$$

即使原问题不是凸的，这个不等式也成立。这个性质称为**弱对偶性**（weak duality）。

当 $d^\star$ 和 $p^\star$ 取无穷值时，弱对偶不等式 (5.23) 仍成立。例如，如果原问题无下界，即 $p^\star=-\infty$，那么必有 $d^\star=-\infty$，也就是说，拉格朗日对偶问题不可行。反过来，如果对偶问题无上界，即 $d^\star=\infty$，那么必有 $p^\star=\infty$，也就是说，原问题不可行。

<!-- pdf-page: 240 -->

差值 $p^\star-d^\star$ 称为原问题的**最优对偶间隙**，因为它给出了原问题最优值与拉格朗日对偶函数所能提供的最好、也就是最大的下界之间的差距。最优对偶间隙总是非负的。

有时，可以利用界 (5.23)，为某个难以求解的问题找到最优值的下界。这是因为对偶问题总是凸的，而且在许多情形下可以高效求解，从而得到 $d^\star$。例如，考虑原书第 219 页介绍的两路划分问题 (5.7)。其对偶问题是 SDP

$$
\begin{array}{ll}
\text{最大化} & -\mathbf{1}^T\nu\\
\text{约束条件} & W+\operatorname{\mathbf{diag}}(\nu)\succeq0,
\end{array}
$$

其中变量为 $\nu\in\mathbf{R}^n$。即使 $n$ 较大，例如 $n=1000$，这个问题也能高效求解。它的最优值是两路划分问题最优值的下界，并且总是至少与基于 $\lambda_{\min}(W)$ 的下界 (5.8) 一样好。

### 5.2.3 强对偶性与 Slater 约束资格条件

如果等式

$$
d^\star=p^\star
\tag{5.24}
$$

成立，即最优对偶间隙为零，就称**强对偶性**（strong duality）成立。这意味着，拉格朗日对偶函数所能给出的最好下界是紧的。

一般来说，强对偶性不一定成立。不过，如果原问题 (5.1) 是凸的，即具有形式

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,\\
& Ax=b,
\end{array}
\tag{5.25}
$$

其中 $f_0,\ldots,f_m$ 为凸函数，那么通常具有强对偶性，但并非总是如此。许多结果给出了凸性以外的附加条件，使问题满足强对偶性。这些条件称为**约束资格条件**（constraint qualifications）。

一个简单的约束资格条件是 **Slater 条件**：存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$，使得

$$
f_i(x)<0,\quad i=1,\ldots,m,\qquad Ax=b.
\tag{5.26}
$$

由于各个不等式约束都以严格不等式成立，这样的点有时称为**严格可行点**。Slater 定理指出：如果 Slater 条件成立，并且问题是凸的，那么强对偶性成立。

当某些不等式约束函数 $f_i$ 是仿射函数时，可以进一步放宽 Slater 条件。如果前 $k$ 个约束函数 $f_1,\ldots,f_k$ 是仿射函数，那么只要满足下面这个更弱的条件，强对偶性就成立：存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$，使得

$$
f_i(x)\leq0,\quad i=1,\ldots,k,\qquad f_i(x)<0,\quad i=k+1,\ldots,m,\qquad Ax=b.
\tag{5.27}
$$

<!-- pdf-page: 241 -->

换言之，仿射不等式不需要严格成立。注意，当所有约束都是线性等式和不等式，而且 $\operatorname{\mathbf{dom}}f_0$ 是开集时，改进后的 Slater 条件 (5.27) 就退化为可行性条件。

对于凸问题，Slater 条件及其改进形式 (5.27) 不仅蕴含强对偶性，还意味着：当 $d^\star>-\infty$ 时，对偶最优值能够达到，即存在对偶可行的 $(\lambda^\star,\nu^\star)$，使得 $g(\lambda^\star,\nu^\star)=d^\star=p^\star$。§5.3.2 将证明：当原问题是凸的且 Slater 条件成立时，强对偶性成立。

### 5.2.4 例子

#### 线性方程的最小二乘解

回顾问题 (5.5)：

$$
\begin{array}{ll}
\text{最小化} & x^Tx\\
\text{约束条件} & Ax=b.
\end{array}
$$

相应的对偶问题为

$$
\text{最大化}\quad-(1/4)\nu^TAA^T\nu-b^T\nu,
$$

这是一个无约束的凹二次函数最大化问题。

Slater 条件在这里仅仅要求原问题可行，因此只要 $b\in\mathcal{R}(A)$，即 $p^\star<\infty$，就有 $p^\star=d^\star$。事实上，这个问题总是具有强对偶性，即使 $p^\star=\infty$ 也成立。这种情形发生在 $b\notin\mathcal{R}(A)$ 时，此时存在 $z$，使得 $A^Tz=0$ 而 $b^Tz\ne0$。于是，对偶函数沿直线 $\{tz\mid t\in\mathbf{R}\}$ 无上界，所以同样有 $d^\star=\infty$。

#### LP 的拉格朗日对偶

由 Slater 条件的较弱形式可知，对于任意 LP，无论是标准形式还是不等式形式，只要原问题可行，就具有强对偶性。将这个结果应用于对偶问题，又可得知，只要对偶问题可行，LP 就具有强对偶性。因此，LP 的强对偶性只有在一种情形下可能不成立：原问题和对偶问题都不可行。这种病态情形确实可能出现；见习题 5.23。

#### QCQP 的拉格朗日对偶

考虑 QCQP

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TP_0x+q_0^Tx+r_0\\
\text{约束条件} & (1/2)x^TP_ix+q_i^Tx+r_i\leq0,\quad i=1,\ldots,m,
\end{array}
\tag{5.28}
$$

其中 $P_0\in\mathbf{S}_{++}^n$，$P_i\in\mathbf{S}_+^n$，$i=1,\ldots,m$。拉格朗日函数为

$$
L(x,\lambda)=(1/2)x^TP(\lambda)x+q(\lambda)^Tx+r(\lambda),
$$

其中

$$
P(\lambda)=P_0+\sum_{i=1}^m\lambda_i P_i,\qquad q(\lambda)=q_0+\sum_{i=1}^m\lambda_i q_i,\qquad r(\lambda)=r_0+\sum_{i=1}^m\lambda_i r_i.
$$

<!-- pdf-page: 242 -->

可以推导一般 $\lambda$ 下 $g(\lambda)$ 的表达式，但相当复杂。不过，当 $\lambda\succeq0$ 时，有 $P(\lambda)\succ0$，而且

$$
g(\lambda)=\inf_x L(x,\lambda)=-(1/2)q(\lambda)^TP(\lambda)^{-1}q(\lambda)+r(\lambda).
$$

因此，对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & -(1/2)q(\lambda)^TP(\lambda)^{-1}q(\lambda)+r(\lambda)\\
\text{约束条件} & \lambda\succeq0.
\end{array}
\tag{5.29}
$$

Slater 条件表明：如果这些二次不等式约束严格可行，即存在 $x$，使得

$$
(1/2)x^TP_ix+q_i^Tx+r_i<0,\quad i=1,\ldots,m,
$$

那么 (5.29) 与 (5.28) 之间成立强对偶性。

#### 熵最大化

下一个例子是熵最大化问题 (5.13)：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Ax\preceq b\\
& \mathbf{1}^Tx=1,
\end{array}
$$

定义域为 $\mathcal{D}=\mathbf{R}_+^n$。其拉格朗日对偶函数已在原书第 222 页推导；对偶问题为

$$
\begin{array}{ll}
\text{最大化} & \displaystyle-b^T\lambda-\nu-e^{-\nu-1}\sum_{i=1}^n e^{-a_i^T\lambda}\\
\text{约束条件} & \lambda\succeq0,
\end{array}
\tag{5.30}
$$

其中变量为 $\lambda\in\mathbf{R}^m$、$\nu\in\mathbf{R}$。问题 (5.13) 的较弱 Slater 条件告诉我们：如果存在 $x\succ0$，满足 $Ax\preceq b$ 和 $\mathbf{1}^Tx=1$，那么最优对偶间隙为零。

可以对对偶变量 $\nu$ 进行解析最大化，从而简化对偶问题 (5.30)。固定 $\lambda$ 时，目标函数在其关于 $\nu$ 的导数为零时达到最大值，即

$$
\nu=\log\sum_{i=1}^n e^{-a_i^T\lambda}-1.
$$

将这个 $\nu$ 的最优值代入对偶问题，得到

$$
\begin{array}{ll}
\text{最大化} & \displaystyle-b^T\lambda-\log\left(\sum_{i=1}^n e^{-a_i^T\lambda}\right)\\
\text{约束条件} & \lambda\succeq0,
\end{array}
$$

这是一个带非负约束的、采用凸形式的几何规划。

#### 最小体积覆盖椭球

考虑问题 (5.14)：

$$
\begin{array}{ll}
\text{最小化} & \log\det X^{-1}\\
\text{约束条件} & a_i^TXa_i\leq1,\quad i=1,\ldots,m,
\end{array}
$$

<!-- pdf-page: 243 -->

定义域为 $\mathcal{D}=\mathbf{S}_{++}^n$。拉格朗日对偶函数由 (5.15) 给出，因此对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & \displaystyle\log\det\left(\sum_{i=1}^m\lambda_i a_i a_i^T\right)-\mathbf{1}^T\lambda+n\\
\text{约束条件} & \lambda\succeq0,
\end{array}
\tag{5.31}
$$

其中，当 $X\not\succ0$ 时，取 $\log\det X=-\infty$。

问题 (5.14) 的较弱 Slater 条件要求存在 $X\in\mathbf{S}_{++}^n$，使得 $a_i^TXa_i\leq1$，$i=1,\ldots,m$。这个条件总能满足，因此 (5.14) 与对偶问题 (5.31) 之间总是成立强对偶性。

#### 一个具有强对偶性的非凸二次问题

少数情况下，非凸问题也具有强对偶性。一个重要的例子是在单位球上最小化非凸二次函数的问题：

$$
\begin{array}{ll}
\text{最小化} & x^TAx+2b^Tx\\
\text{约束条件} & x^Tx\leq1,
\end{array}
\tag{5.32}
$$

其中 $A\in\mathbf{S}^n$、$A\not\succeq0$、$b\in\mathbf{R}^n$。由于 $A\not\succeq0$，这不是凸问题。这个问题有时称为**信赖域问题**（trust region problem）：在单位球上最小化某个函数的二阶近似时，就会遇到它；这里假设该近似在这个单位球内大致有效。

拉格朗日函数为

$$
L(x,\lambda)=x^TAx+2b^Tx+\lambda(x^Tx-1)=x^T(A+\lambda I)x+2b^Tx-\lambda,
$$

因此，对偶函数为

$$
g(\lambda)=\begin{cases}-b^T(A+\lambda I)^\dagger b-\lambda&A+\lambda I\succeq0,\quad b\in\mathcal{R}(A+\lambda I)\\-\infty&\text{其他情形，}\end{cases}
$$

其中 $(A+\lambda I)^\dagger$ 是 $A+\lambda I$ 的伪逆。于是，拉格朗日对偶问题为

$$
\begin{array}{ll}
\text{最大化} & -b^T(A+\lambda I)^\dagger b-\lambda\\
\text{约束条件} & A+\lambda I\succeq0,\quad b\in\mathcal{R}(A+\lambda I),
\end{array}
\tag{5.33}
$$

其中变量为 $\lambda\in\mathbf{R}$。虽然从这个表达式中并不容易看出，但它确实是一个凸优化问题。事实上，这个问题很容易求解，因为可以写成

$$
\begin{array}{ll}
\text{最大化} & \displaystyle-\sum_{i=1}^n(q_i^Tb)^2/(\lambda_i+\lambda)-\lambda\\
\text{约束条件} & \lambda\geq-\lambda_{\min}(A),
\end{array}
$$

其中 $\lambda_i$ 和 $q_i$ 是 $A$ 的特征值及对应的标准正交特征向量；当 $q_i^Tb=0$ 时，将 $(q_i^Tb)^2/0$ 解释为 0，否则解释为 $\infty$。

尽管原问题 (5.32) 不是凸的，这个问题的最优对偶间隙却总是为零：(5.32) 与 (5.33) 的最优值总是相同。事实上，还有一个更一般的结果：对于任意一个具有二次目标函数和一个二次不等式约束的优化问题，只要 Slater 条件成立，就具有强对偶性；见 §B.1。

<!-- pdf-page: 244 -->

### 5.2.5 矩阵博弈中的混合策略

本节利用强对偶性推导零和矩阵博弈的一个基本结果。考虑一个有两名玩家的博弈。玩家 1 作出选择或行动 $k\in\{1,\ldots,n\}$，玩家 2 作出选择 $l\in\{1,\ldots,m\}$。随后，玩家 1 向玩家 2 支付 $P_{kl}$，其中 $P\in\mathbf{R}^{n\times m}$ 是这个博弈的**支付矩阵**（payoff matrix）。玩家 1 的目标是使支付额尽可能小，玩家 2 的目标则是使它尽可能大。

两名玩家采用**随机策略**或**混合策略**，即各自按照某个概率分布随机作出选择，而且两人的选择相互独立：

$$
\operatorname{\mathbf{prob}}(k=i)=u_i,\quad i=1,\ldots,n,\qquad\operatorname{\mathbf{prob}}(l=i)=v_i,\quad i=1,\ldots,m.
$$

这里，$u$ 和 $v$ 给出了两名玩家选择的概率分布，也就是各自的策略。于是，玩家 1 向玩家 2 支付的期望金额为

$$
\sum_{k=1}^n\sum_{l=1}^m u_kv_lP_{kl}=u^TPv.
$$

玩家 1 希望选择 $u$ 使 $u^TPv$ 最小，玩家 2 则希望选择 $v$ 使 $u^TPv$ 最大。

先从玩家 1 的角度分析，假设玩家 2 知道玩家 1 的策略 $u$，这显然给了玩家 2 优势。玩家 2 会选择 $v$ 来最大化 $u^TPv$，得到期望支付额

$$
\sup\{u^TPv\mid v\succeq0,\ \mathbf{1}^Tv=1\}=\max_{i=1,\ldots,m}(P^Tu)_i.
$$

玩家 1 所能做的最好选择，是选择 $u$ 来最小化这个在最坏情况下向玩家 2 支付的金额，即选择一个能够求解下列问题的策略 $u$：

$$
\begin{array}{ll}
\text{最小化} & \max_{i=1,\ldots,m}(P^Tu)_i\\
\text{约束条件} & u\succeq0,\quad\mathbf{1}^Tu=1,
\end{array}
\tag{5.34}
$$

这是一个分段线性凸优化问题。将其最优值记为 $p_1^\star$。假设玩家 2 知道玩家 1 的策略，并采取对自己最有利的行动，那么 $p_1^\star$ 就是玩家 1 能够安排的最小期望支付额。

类似地，可以考虑玩家 1 知道玩家 2 的策略 $v$ 的情形，这给了玩家 1 优势。此时，玩家 1 选择 $u$ 使 $u^TPv$ 最小，得到期望支付额

$$
\inf\{u^TPv\mid u\succeq0,\ \mathbf{1}^Tu=1\}=\min_{i=1,\ldots,n}(Pv)_i.
$$

玩家 2 选择 $v$ 使这个值最大，即选择一个能够求解下列问题的策略 $v$：

$$
\begin{array}{ll}
\text{最大化} & \min_{i=1,\ldots,n}(Pv)_i\\
\text{约束条件} & v\succeq0,\quad\mathbf{1}^Tv=1,
\end{array}
\tag{5.35}
$$

<!-- pdf-page: 245 -->

这是另一个凸优化问题，目标函数是分段线性凹函数。将这个问题的最优值记为 $p_2^\star$。假设玩家 1 知道玩家 2 的策略，那么 $p_2^\star$ 就是玩家 2 能够保证获得的最大期望支付额。

直观上，知道对手的策略显然会带来优势，至少不会有害；事实上，也很容易证明总有 $p_1^\star\geq p_2^\star$。可以将非负的差值 $p_1^\star-p_2^\star$ 解释为知道对手策略所带给玩家的优势。

利用对偶性，可以证明一个乍看令人意外的结果：$p_1^\star=p_2^\star$。换言之，在采用混合策略的矩阵博弈中，知道对手的策略并不会带来优势。下面通过证明 (5.34) 和 (5.35) 互为拉格朗日对偶问题，而且强对偶性成立，来建立这个结果。

首先，将 (5.34) 写成 LP：

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & u\succeq0,\quad\mathbf{1}^Tu=1\\
& P^Tu\preceq t\mathbf{1},
\end{array}
$$

其中增加了变量 $t\in\mathbf{R}$。为 $P^Tu\preceq t\mathbf{1}$ 引入乘子 $\lambda$，为 $u\succeq0$ 引入乘子 $\mu$，为 $\mathbf{1}^Tu=1$ 引入乘子 $\nu$，得到拉格朗日函数

$$
t+\lambda^T(P^Tu-t\mathbf{1})-\mu^Tu+\nu(1-\mathbf{1}^Tu)=\nu+(1-\mathbf{1}^T\lambda)t+(P\lambda-\nu\mathbf{1}-\mu)^Tu,
$$

所以对偶函数为

$$
g(\lambda,\mu,\nu)=\begin{cases}\nu&\mathbf{1}^T\lambda=1,\quad P\lambda-\nu\mathbf{1}=\mu\\-\infty&\text{其他情形。}\end{cases}
$$

于是，对偶问题为

$$
\begin{array}{ll}
\text{最大化} & \nu\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1,\quad\mu\succeq0\\
& P\lambda-\nu\mathbf{1}=\mu.
\end{array}
$$

消去 $\mu$，得到 (5.34) 的如下拉格朗日对偶：

$$
\begin{array}{ll}
\text{最大化} & \nu\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1\\
& P\lambda\succeq\nu\mathbf{1},
\end{array}
$$

其中变量为 $\lambda,\nu$。这显然等价于 (5.35)。由于这些 LP 都可行，强对偶性成立，所以 (5.34) 与 (5.35) 的最优值相等。

<!-- pdf-page: 246 -->

## 5.3 几何解释

### 5.3.1 用取值集合解释弱对偶性与强对偶性

利用集合

$$
\mathcal{G}=\{(f_1(x),\ldots,f_m(x),h_1(x),\ldots,h_p(x),f_0(x))\in\mathbf{R}^m\times\mathbf{R}^p\times\mathbf{R}\mid x\in\mathcal{D}\},\tag{5.36}
$$

可以给出对偶函数的一个简单几何解释。这个集合由约束函数与目标函数的取值组成。(5.1) 的最优值 $p^\star$ 很容易用 $\mathcal{G}$ 表示为

$$
p^\star=\inf\{t\mid(u,v,t)\in\mathcal{G},\ u\preceq0,\ v=0\}.
$$

为了求对偶函数在 $(\lambda,\nu)$ 处的值，我们在 $(u,v,t)\in\mathcal{G}$ 上最小化仿射函数

$$
(\lambda,\nu,1)^T(u,v,t)=\sum_{i=1}^m\lambda_i u_i+\sum_{i=1}^p\nu_i v_i+t,
$$

即

$$
g(\lambda,\nu)=\inf\{(\lambda,\nu,1)^T(u,v,t)\mid(u,v,t)\in\mathcal{G}\}.
$$

特别地，如果这个下确界有限，那么不等式

$$
(\lambda,\nu,1)^T(u,v,t)\geq g(\lambda,\nu)
$$

定义了 $\mathcal{G}$ 的一个支撑超平面。由于法向量的最后一个分量非零，这种超平面有时称为*非竖直支撑超平面*。

现在设 $\lambda\succeq0$。显然，当 $u\preceq0$ 且 $v=0$ 时，有 $t\geq(\lambda,\nu,1)^T(u,v,t)$。因此

$$
\begin{aligned}
p^\star&=\inf\{t\mid(u,v,t)\in\mathcal{G},\ u\preceq0,\ v=0\}\\
&\geq\inf\{(\lambda,\nu,1)^T(u,v,t)\mid(u,v,t)\in\mathcal{G},\ u\preceq0,\ v=0\}\\
&\geq\inf\{(\lambda,\nu,1)^T(u,v,t)\mid(u,v,t)\in\mathcal{G}\}\\
&=g(\lambda,\nu),
\end{aligned}
$$

即弱对偶性成立。图 5.3 和图 5.4 以一个只有单个不等式约束的简单问题说明了这种解释。

#### 上图形式的变体

本节介绍利用 $\mathcal{G}$ 对对偶性作几何解释的一种变体，它说明了为什么（大多数）凸问题具有强对偶性。定义集合 $\mathcal{A}\subseteq\mathbf{R}^m\times\mathbf{R}^p\times\mathbf{R}$ 为

$$
\mathcal{A}=\mathcal{G}+(\mathbf{R}_+^m\times\{0\}\times\mathbf{R}_+),\tag{5.37}
$$

更明确地写为

$$
\begin{aligned}
\mathcal{A}=\{(u,v,t)\mid{}&\exists x\in\mathcal{D},\ f_i(x)\leq u_i,\ i=1,\ldots,m,\\
&h_i(x)=v_i,\ i=1,\ldots,p,\ f_0(x)\leq t\}.
\end{aligned}
$$

<!-- pdf-page: 247 -->

<figure id="fig-5-3" data-figure="5.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-3.png" alt="阴影集合 G 与一条支撑直线，直线与纵轴的交点给出低于原问题最优值的对偶函数值" data-source-page="247" data-source-rect="136,183,381,341">
<figcaption>图 5.3 只有一个（不等式）约束的问题中，对偶函数及下界 $g(\lambda)\leq p^\star$ 的几何解释。给定 $\lambda$，在 $\mathcal{G}=\{(f_1(x),f_0(x))\mid x\in\mathcal{D}\}$ 上最小化 $(\lambda,1)^T(u,t)$。这样得到一条斜率为 $-\lambda$ 的支撑超平面。该超平面与 $u=0$ 轴的交点给出 $g(\lambda)$。</figcaption>
</figure>

<figure id="fig-5-4" data-figure="5.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-4.png" alt="三个对偶可行乘子对应的支撑直线，最优对偶值低于原问题的最优值" data-source-page="247" data-source-rect="127,405,381,564">
<figcaption>图 5.4 $\lambda$ 的三个对偶可行取值所对应的支撑超平面，其中包括最优取值 $\lambda^\star$。强对偶性不成立；最优对偶间隙 $p^\star-d^\star$ 为正。</figcaption>
</figure>

<!-- pdf-page: 248 -->

<figure id="fig-5-5" data-figure="5.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-5.png" alt="阴影集合 A 与一条支撑直线，纵轴上标出原问题的最优值和对偶函数值" data-source-page="248" data-source-rect="181,118,444,274">
<figcaption>图 5.5 只有一个（不等式）约束的问题中，对偶函数及下界 $g(\lambda)\leq p^\star$ 的几何解释。给定 $\lambda$，在 $\mathcal{A}=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)\leq t,\ f_1(x)\leq u\}$ 上最小化 $(\lambda,1)^T(u,t)$。这样得到一条斜率为 $-\lambda$ 的支撑超平面。该超平面与 $u=0$ 轴的交点给出 $g(\lambda)$。</figcaption>
</figure>

可以把 $\mathcal{A}$ 看成 $\mathcal{G}$ 的一种上图形式，因为 $\mathcal{A}$ 既包含 $\mathcal{G}$ 中的所有点，也包含那些“更差”的点，即目标函数或不等式约束函数的值更大的点。

最优值可以用 $\mathcal{A}$ 表示为

$$
p^\star=\inf\{t\mid(0,0,t)\in\mathcal{A}\}.
$$

为了求对偶函数在满足 $\lambda\succeq0$ 的点 $(\lambda,\nu)$ 处的值，可以在 $\mathcal{A}$ 上最小化仿射函数 $(\lambda,\nu,1)^T(u,v,t)$：如果 $\lambda\succeq0$，则

$$
g(\lambda,\nu)=\inf\{(\lambda,\nu,1)^T(u,v,t)\mid(u,v,t)\in\mathcal{A}\}.
$$

如果这个下确界有限，则

$$
(\lambda,\nu,1)^T(u,v,t)\geq g(\lambda,\nu)
$$

定义了 $\mathcal{A}$ 的一个非竖直支撑超平面。

特别地，由于 $(0,0,p^\star)\in\operatorname{\mathbf{bd}}\mathcal{A}$，有

$$
p^\star=(\lambda,\nu,1)^T(0,0,p^\star)\geq g(\lambda,\nu),\tag{5.38}
$$

这就是弱对偶性给出的下界。强对偶性成立，当且仅当存在某个对偶可行的 $(\lambda,\nu)$，使 (5.38) 中等号成立；也就是说，$\mathcal{A}$ 在边界点 $(0,0,p^\star)$ 处存在一个非竖直支撑超平面。

<div class="translator-note" markdown="1">

**译注（强对偶性与最优值的达到）：** 强对偶性只要求 $d^\star=p^\star$，并不保证某个对偶可行点能达到这一值。这里的“当且仅当”还需要对偶最优值能够达到。例如，最小化 $x$、约束为 $x^2\leq0$ 时，$p^\star=d^\star=0$，但 $g(\lambda)=-1/(4\lambda)<0$（$\lambda>0$），且 $g(0)=-\infty$；没有有限乘子达到对偶最优值。

</div>

图 5.5 说明了这第二种解释。

### 5.3.2 约束资格条件下强对偶性的证明

本节证明，对于凸问题，Slater 约束资格条件能够保证强对偶性成立（并保证对偶最优值能够达到）。我们考虑<!-- pdf-page: 249 -->原问题 (5.25)，其中 $f_0,\ldots,f_m$ 为凸函数，并假设 Slater 条件成立：存在 $\widetilde x\in\operatorname{\mathbf{relint}}\mathcal{D}$，使得 $f_i(\widetilde x)<0$，$i=1,\ldots,m$，且 $A\widetilde x=b$。为了简化证明，再增加两个假设：第一，$\mathcal{D}$ 的内部非空（因此 $\operatorname{\mathbf{relint}}\mathcal{D}=\operatorname{\mathbf{int}}\mathcal{D}$）；第二，$\operatorname{\mathbf{rank}}A=p$。我们假设 $p^\star$ 有限。（由于存在可行点，只可能有 $p^\star=-\infty$ 或 $p^\star$ 有限；如果 $p^\star=-\infty$，则由弱对偶性可知 $d^\star=-\infty$。）

如果原问题是凸问题，很容易证明 (5.37) 定义的集合 $\mathcal{A}$ 是凸集。再定义一个凸集 $\mathcal{B}$：

$$
\mathcal{B}=\{(0,0,s)\in\mathbf{R}^m\times\mathbf{R}^p\times\mathbf{R}\mid s<p^\star\}.
$$

集合 $\mathcal{A}$ 和 $\mathcal{B}$ 不相交。为说明这一点，假设 $(u,v,t)\in\mathcal{A}\cap\mathcal{B}$。由于 $(u,v,t)\in\mathcal{B}$，有 $u=0$、$v=0$ 且 $t<p^\star$。由于 $(u,v,t)\in\mathcal{A}$，存在 $x$ 使得 $f_i(x)\leq0$，$i=1,\ldots,m$，$Ax-b=0$，且 $f_0(x)\leq t<p^\star$；但 $p^\star$ 是原问题的最优值，因此这是不可能的。

由 §2.5.1 的分离超平面定理，存在 $(\widetilde\lambda,\widetilde\nu,\mu)\neq0$ 和 $\alpha$，使得

$$
(u,v,t)\in\mathcal{A}\quad\Longrightarrow\quad\widetilde\lambda^Tu+\widetilde\nu^Tv+\mu t\geq\alpha,\tag{5.39}
$$

以及

$$
(u,v,t)\in\mathcal{B}\quad\Longrightarrow\quad\widetilde\lambda^Tu+\widetilde\nu^Tv+\mu t\leq\alpha.\tag{5.40}
$$

由 (5.39) 可知 $\widetilde\lambda\succeq0$ 且 $\mu\geq0$。（否则，$\widetilde\lambda^Tu+\mu t$ 在 $\mathcal{A}$ 上无下界，与 (5.39) 矛盾。）条件 (5.40) 只是说，对所有 $t<p^\star$，都有 $\mu t\leq\alpha$，从而 $\mu p^\star\leq\alpha$。结合 (5.39)，可知对于任意 $x\in\mathcal{D}$，

$$
\sum_{i=1}^m\widetilde\lambda_i f_i(x)+\widetilde\nu^T(Ax-b)+\mu f_0(x)\geq\alpha\geq\mu p^\star.\tag{5.41}
$$

假设 $\mu>0$。此时将 (5.41) 除以 $\mu$，得到

$$
L(x,\widetilde\lambda/\mu,\widetilde\nu/\mu)\geq p^\star
$$

对所有 $x\in\mathcal{D}$ 成立。因此，对 $x$ 取最小值可知 $g(\lambda,\nu)\geq p^\star$，这里定义

$$
\lambda=\widetilde\lambda/\mu,\qquad\nu=\widetilde\nu/\mu.
$$

由弱对偶性，有 $g(\lambda,\nu)\leq p^\star$，所以实际上 $g(\lambda,\nu)=p^\star$。这说明，至少在 $\mu>0$ 的情形下，强对偶性成立，而且对偶最优值能够达到。

现在考虑 $\mu=0$ 的情形。由 (5.41) 可知，对于所有 $x\in\mathcal{D}$，

$$
\sum_{i=1}^m\widetilde\lambda_i f_i(x)+\widetilde\nu^T(Ax-b)\geq0.\tag{5.42}
$$

将这一不等式用于满足 Slater 条件的点 $\widetilde x$，得到

$$
\sum_{i=1}^m\widetilde\lambda_i f_i(\widetilde x)\geq0.
$$

<!-- pdf-page: 250 -->

<figure id="fig-5-6" data-figure="5.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-6.png" alt="凸集 A、竖直线段 B 和一条分离直线，A 中标出严格可行点对应的位置，B 的上端为空心圆点" data-source-page="250" data-source-rect="246,118,435,306">
<figcaption>图 5.6 满足 Slater 约束资格条件的凸问题中，强对偶性证明的示意图。集合 $\mathcal{A}$ 用阴影表示，集合 $\mathcal{B}$ 是粗竖直线段，不包括用小空心圆表示的点 $(0,p^\star)$。这两个集合都是凸集且互不相交，因此可以用一个超平面将它们分离。Slater 约束资格条件保证，任何分离超平面都不能是竖直的，因为它必须从点 $(\widetilde u,\widetilde t)=(f_1(\widetilde x),f_0(\widetilde x))$ 的左侧经过，其中 $\widetilde x$ 是严格可行点。</figcaption>
</figure>

由于 $f_i(\widetilde x)<0$ 且 $\widetilde\lambda_i\geq0$，可知 $\widetilde\lambda=0$。由 $(\widetilde\lambda,\widetilde\nu,\mu)\neq0$ 以及 $\widetilde\lambda=0$、$\mu=0$，可知 $\widetilde\nu\neq0$。于是 (5.42) 表明，对于所有 $x\in\mathcal{D}$，都有 $\widetilde\nu^T(Ax-b)\geq0$。但是，$\widetilde x$ 满足 $\widetilde\nu^T(A\widetilde x-b)=0$，而且由于 $\widetilde x\in\operatorname{\mathbf{int}}\mathcal{D}$，除非 $A^T\widetilde\nu=0$，否则 $\mathcal{D}$ 中就存在满足 $\widetilde\nu^T(Ax-b)<0$ 的点。这当然与假设 $\operatorname{\mathbf{rank}}A=p$ 矛盾。

图 5.6 以一个只有单个不等式约束的简单问题，说明了这个证明背后的几何思路。分离 $\mathcal{A}$ 和 $\mathcal{B}$ 的超平面定义了 $\mathcal{A}$ 在 $(0,p^\star)$ 处的一个支撑超平面。Slater 约束资格条件用于证明这个超平面必定不是竖直的（即其法向量具有 $(\lambda^\star,1)$ 的形式）。（关于只有单个不等式约束、但强对偶性不成立的凸问题的简单例子，见习题 5.21。）

### 5.3.3 多准则解释

没有等式约束的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m
\end{array}\tag{5.43}
$$

<!-- pdf-page: 251 -->

的拉格朗日对偶性，与（无约束）多准则问题

$$
\begin{array}{ll}
\text{最小化（关于 }\mathbf{R}_+^{m+1}\text{）} & F(x)=(f_1(x),\ldots,f_m(x),f_0(x))
\end{array}\tag{5.44}
$$

的标量化方法之间存在自然的联系（见 §4.7.4）。在标量化方法中，我们选取一个正向量 $\widetilde\lambda$，然后最小化标量函数 $\widetilde\lambda^TF(x)$；它的任何最小值点都保证是 Pareto 最优点。将 $\widetilde\lambda$ 乘以正常数不会改变最小值点，因此不失一般性，可以取 $\widetilde\lambda=(\lambda,1)$。所以，在标量化方法中，我们最小化的函数为

$$
\widetilde\lambda^TF(x)=f_0(x)+\sum_{i=1}^m\lambda_i f_i(x),
$$

它恰好就是问题 (5.43) 的拉格朗日函数。

为了证明凸多准则问题的每一个 Pareto 最优点，都能使某个非负权重向量 $\widetilde\lambda$ 所对应的函数 $\widetilde\lambda^TF(x)$ 取得最小值，我们曾考虑 (4.62) 定义的集合 $\mathcal{A}$，

$$
\mathcal{A}=\{t\in\mathbf{R}^{m+1}\mid\exists x\in\mathcal{D},\ f_i(x)\leq t_i,\ i=0,\ldots,m\},
$$

它与拉格朗日对偶性中出现的、由 (5.37) 定义的集合 $\mathcal{A}$ 完全相同。在那里，我们也是通过该集合在任意一个 Pareto 最优点处的支撑超平面，构造出所需的权重向量。在多准则优化中，权重向量的各分量表示各个目标函数之间的相对权重。当我们把权重向量的最后一个分量（与 $f_0$ 对应的分量）固定为 1 时，其余权重就可以解释为相对于 $f_0$ 的代价，即相对于目标函数的代价。

## 5.4 鞍点解释

本节给出拉格朗日对偶性的几种解释。后文不会用到本节的内容。

### 5.4.1 弱对偶性与强对偶性的极大极小刻画

我们可以把原优化问题与对偶优化问题写成更加对称的形式。为简化讨论，假设没有等式约束；这些结果很容易推广到包含等式约束的情形。

首先注意到

$$
\begin{aligned}
\sup_{\lambda\succeq0}L(x,\lambda)&=\sup_{\lambda\succeq0}\left(f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)\right)\\
&=\begin{cases}f_0(x)&f_i(x)\leq0,\quad i=1,\ldots,m\\\infty&\text{其他情形。}\end{cases}
\end{aligned}
$$

<!-- pdf-page: 252 -->

事实上，假设 $x$ 不可行，且某个 $i$ 满足 $f_i(x)>0$。令 $\lambda_j=0$，$j\neq i$，并令 $\lambda_i\to\infty$，就可看出 $\sup_{\lambda\succeq0}L(x,\lambda)=\infty$。另一方面，如果 $f_i(x)\leq0$，$i=1,\ldots,m$，那么 $\lambda$ 的最优选择为 $\lambda=0$，且 $\sup_{\lambda\succeq0}L(x,\lambda)=f_0(x)$。这意味着原问题的最优值可以表示为

$$
p^\star=\inf_x\sup_{\lambda\succeq0}L(x,\lambda).
$$

由对偶函数的定义，还有

$$
d^\star=\sup_{\lambda\succeq0}\inf_x L(x,\lambda).
$$

因此，弱对偶性可以表示为不等式

$$
\sup_{\lambda\succeq0}\inf_x L(x,\lambda)\leq\inf_x\sup_{\lambda\succeq0}L(x,\lambda),\tag{5.45}
$$

而强对偶性可以表示为等式

$$
\sup_{\lambda\succeq0}\inf_x L(x,\lambda)=\inf_x\sup_{\lambda\succeq0}L(x,\lambda).
$$

强对偶性意味着，可以交换对 $x$ 最小化与对 $\lambda\succeq0$ 最大化的次序，而不影响结果。

事实上，不等式 (5.45) 不依赖于 $L$ 的任何性质：对于任意 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$（以及任意 $W\subseteq\mathbf{R}^n$ 和 $Z\subseteq\mathbf{R}^m$），都有

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)\leq\inf_{w\in W}\sup_{z\in Z}f(w,z).\tag{5.46}
$$

这个一般性不等式称为**极大极小不等式**（max-min inequality）。当等号成立，即

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)=\inf_{w\in W}\sup_{z\in Z}f(w,z)\tag{5.47}
$$

时，我们说 $f$（以及 $W$ 和 $Z$）满足**强极大极小性质**或**鞍点性质**。当然，强极大极小性质只在特殊情形下成立。例如，$f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$ 是某个具有强对偶性的问题的拉格朗日函数，而 $W=\mathbf{R}^n$、$Z=\mathbf{R}_+^m$ 时，这一性质就成立。

### 5.4.2 鞍点解释

如果一对 $\widetilde w\in W$、$\widetilde z\in Z$ 满足

$$
f(\widetilde w,z)\leq f(\widetilde w,\widetilde z)\leq f(w,\widetilde z)
$$

对所有 $w\in W$ 和 $z\in Z$ 成立，就称它为 $f$（以及 $W$ 和 $Z$）的一个**鞍点**（saddle-point）。换言之，$\widetilde w$ 使 $f(w,\widetilde z)$（在 $w\in W$ 上）最小，而 $\widetilde z$ 使 $f(\widetilde w,z)$（在 $z\in Z$ 上）最大：

$$
f(\widetilde w,\widetilde z)=\inf_{w\in W}f(w,\widetilde z),\qquad f(\widetilde w,\widetilde z)=\sup_{z\in Z}f(\widetilde w,z).
$$

<!-- pdf-page: 253 -->

这意味着强极大极小性质 (5.47) 成立，且两边的共同值为 $f(\widetilde w,\widetilde z)$。

回到拉格朗日对偶性的讨论。如果 $x^\star$ 和 $\lambda^\star$ 分别是某个具有强对偶性的问题的原最优点与对偶最优点，那么它们就构成拉格朗日函数的一个鞍点。反之也成立：如果 $(x,\lambda)$ 是拉格朗日函数的一个鞍点，那么 $x$ 是原最优点，$\lambda$ 是对偶最优点，且最优对偶间隙为零。

### 5.4.3 博弈解释

我们可以用一个连续的**零和博弈**来解释极大极小不等式 (5.46)、极大极小等式 (5.47) 和鞍点性质。如果玩家 1 选择 $w\in W$，玩家 2 选择 $z\in Z$，那么玩家 1 向玩家 2 支付金额 $f(w,z)$。因此，玩家 1 希望使 $f$ 最小，而玩家 2 希望使 $f$ 最大。（这个博弈称为连续博弈，因为选择是向量，而不是离散的。）

假设玩家 1 先作出选择，然后玩家 2 得知玩家 1 的选择，再作出自己的选择。玩家 2 希望使支付额 $f(w,z)$ 最大，因此会选取使 $f(w,z)$ 最大的 $z\in Z$。由此得到的支付额为 $\sup_{z\in Z}f(w,z)$，它取决于玩家 1 的选择 $w$。（这里假设上确界能够取到；如果不能，最优支付额可以任意接近 $\sup_{z\in Z}f(w,z)$。）玩家 1 知道（或假设）玩家 2 会采取这一策略，因此会选择 $w\in W$，使这种最坏情形下支付给玩家 2 的金额尽可能小。所以，玩家 1 选择

$$
\mathop{\operatorname{argmin}}_{w\in W}\sup_{z\in Z}f(w,z),
$$

从而向玩家 2 支付

$$
\inf_{w\in W}\sup_{z\in Z}f(w,z).
$$

现在假设行动次序颠倒：玩家 2 必须先选择 $z\in Z$，然后玩家 1（在知道 $z$ 的情况下）选择 $w\in W$。类似地，如果双方都采取最优策略，玩家 2 就应选择 $z\in Z$，使 $\inf_{w\in W}f(w,z)$ 最大，由此玩家 1 向玩家 2 支付

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z).
$$

极大极小不等式 (5.46) 表达了一个（直觉上显然的）事实：后行动对玩家更有利；更准确地说，在作出自己的选择前知道对手的选择更有利。换言之，如果玩家 1 必须先作出选择，玩家 2 得到的支付额就会更大。当鞍点性质 (5.47) 成立时，后行动就没有优势。

如果 $(\widetilde w,\widetilde z)$ 是 $f$（以及 $W$ 和 $Z$）的一个鞍点，就称它为博弈的一个*解*；$\widetilde w$ 称为玩家 1 的最优选择或最优策略，而 $\widetilde z$ 称为<!-- pdf-page: 254 -->玩家 2 的最优选择或最优策略。此时，后行动没有优势。

现在考虑支付函数为拉格朗日函数、$W=\mathbf{R}^n$ 且 $Z=\mathbf{R}_+^m$ 的特殊情形。这里，玩家 1 选择原变量 $x$，玩家 2 选择对偶变量 $\lambda\succeq0$。由上述论证可知，如果玩家 2 必须先行动，那么其最优选择是任意一个对偶最优的 $\lambda^\star$，由此玩家 2 得到的支付额为 $d^\star$。反过来，如果玩家 1 必须先行动，那么其最优选择是任意一个原最优的 $x^\star$，由此产生的支付额为 $p^\star$。

问题的最优对偶间隙，恰好等于后行动的玩家所获得的优势，即在作出自己的选择前知道对手选择的优势。如果强对偶性成立，那么知道对手的选择对双方都不再有利。

### 5.4.4 价格或税费解释

拉格朗日对偶性有一个有趣的经济学解释。假设变量 $x$ 表示企业的经营方式，$f_0(x)$ 表示在 $x$ 下经营的成本，即 $-f_0(x)$ 是在经营状况 $x$ 下获得的利润（例如以美元计）。每个约束 $f_i(x)\leq0$ 都表示某种限制，例如资源限制（如仓储空间、劳动力），或法规限制（如环境方面的规定）。通过求解问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}
$$

可以找到在满足这些限制的同时使利润最大的经营状况。由此得到的最优利润为 $-p^\star$。

现在设想第二种情形：允许违反这些限制，但必须支付额外成本，且成本与违反程度（由 $f_i$ 度量）成线性关系。因此，企业为第 $i$ 项限制或约束支付的金额为 $\lambda_i f_i(x)$。对于没有取紧的约束，企业也会收到款项；如果 $f_i(x)<0$，那么 $\lambda_i f_i(x)$ 就表示一笔支付给企业的金额。系数 $\lambda_i$ 可以解释为违反 $f_i(x)\leq0$ 的价格，其单位是每单位违反程度（由 $f_i$ 度量）所需支付的美元数。企业也可以按同样的价格出售第 $i$ 个约束中任何“未使用”的部分。我们假设 $\lambda_i\geq0$，即企业违反限制时必须支付费用（而约束没有取紧时会获得收入）。

例如，假设原问题的第一个约束 $f_1(x)\leq0$ 表示仓储空间的限制（例如以平方米计）。在这种新安排下，企业可以按每平方米 $\lambda_1$ 美元的价格租入额外的仓储空间，也可以按相同的价格出租未使用的空间。

在经营状况为 $x$、约束价格为 $\lambda_i$ 时，企业的总成本为 $L(x,\lambda)=f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)$。显然，企业会选择使总成本 $L(x,\lambda)$ 最小的经营方式，得到的成本为 $g(\lambda)$。因此，对偶函数表示企业的最优成本随约束价格向量 $\lambda$ 的变化。对偶最优值 $d^\star$ 是在最不利的一组价格下，企业能够达到的最优成本。

<!-- pdf-page: 255 -->

利用这一解释，可以把弱对偶性表述如下：即使价格最不利，企业在第二种情形（可以买卖约束的违反量）下的最优成本，也不会超过原来情形（约束不能违反）下的成本。这是显然的：如果 $x^\star$ 在第一种情形下最优，那么在第二种情形下，采用 $x^\star$ 的经营成本会低于 $f_0(x^\star)$，因为那些没有取紧的约束可以带来一些收入。因此，最优对偶间隙就是允许企业付费违反约束（并因约束没有取紧而收到款项）所能带来的最小优势。

现在假设强对偶性成立，且对偶最优值能够达到。对偶最优的 $\lambda^\star$ 可以解释为这样一组价格：按这组价格，允许企业付费违反约束（或因约束没有取紧而收到款项）不会给企业带来任何优势。因此，对偶最优的 $\lambda^\star$ 有时称为原问题的一组**影子价格**（shadow prices）。

## 5.5 最优性条件

提醒读者，除非明确说明，否则我们不假设问题 (5.1) 是凸问题。

### 5.5.1 次优性证书与停止准则

如果能找到一个对偶可行的 $(\lambda,\nu)$，就得到了原问题最优值的一个下界：$p^\star\geq g(\lambda,\nu)$。因此，对偶可行点 $(\lambda,\nu)$ 提供了 $p^\star\geq g(\lambda,\nu)$ 的一个证明或*证书*（certificate）。强对偶性意味着存在任意好的证书。

有了对偶可行点，无需知道 $p^\star$ 的精确值，就可以给出某个可行点距离最优值有多远的界。事实上，如果 $x$ 原可行，且 $(\lambda,\nu)$ 对偶可行，那么

$$
f_0(x)-p^\star\leq f_0(x)-g(\lambda,\nu).
$$

特别地，这说明 $x$ 是 $\epsilon$-次优点，其中 $\epsilon=f_0(x)-g(\lambda,\nu)$。（这也说明 $(\lambda,\nu)$ 是对偶问题的 $\epsilon$-次优点。）

我们把原目标与对偶目标之间的间隙

$$
f_0(x)-g(\lambda,\nu),
$$

称为与原可行点 $x$ 和对偶可行点 $(\lambda,\nu)$ 对应的**对偶间隙**。一对原、对偶可行点 $x$、$(\lambda,\nu)$ 将原问题（和对偶问题）的最优值限定在一个区间内：

$$
p^\star\in[g(\lambda,\nu),f_0(x)],\qquad d^\star\in[g(\lambda,\nu),f_0(x)],
$$

这个区间的宽度就是对偶间隙。

如果原、对偶可行点对 $x$、$(\lambda,\nu)$ 的对偶间隙为零，即 $f_0(x)=g(\lambda,\nu)$，那么 $x$ 原最优，$(\lambda,\nu)$ 对偶最优。我们可以把 $(\lambda,\nu)$ 看成<!-- pdf-page: 256 -->证明 $x$ 最优的证书（类似地，也可以把 $x$ 看成证明 $(\lambda,\nu)$ 对偶最优的证书）。

这些结论可以为优化算法提供有严格依据的停止准则。假设某个算法生成原可行点 $x^{(k)}$ 和对偶可行点 $(\lambda^{(k)},\nu^{(k)})$ 的序列，$k=1,2,\ldots$，并给定要求的绝对精度 $\epsilon_{\mathrm{abs}}>0$。那么停止准则（即终止算法的条件）

$$
f_0(x^{(k)})-g(\lambda^{(k)},\nu^{(k)})\leq\epsilon_{\mathrm{abs}}
$$

保证算法终止时，$x^{(k)}$ 是 $\epsilon_{\mathrm{abs}}$-次优点。事实上，$(\lambda^{(k)},\nu^{(k)})$ 就是证明这一点的证书。（当然，如果要让这种方法对任意小的容差 $\epsilon_{\mathrm{abs}}$ 都有效，强对偶性就必须成立。）

类似的条件也可以保证给定的相对精度 $\epsilon_{\mathrm{rel}}>0$。如果

$$
g(\lambda^{(k)},\nu^{(k)})>0,\qquad\frac{f_0(x^{(k)})-g(\lambda^{(k)},\nu^{(k)})}{g(\lambda^{(k)},\nu^{(k)})}\leq\epsilon_{\mathrm{rel}}
$$

成立，或者

$$
f_0(x^{(k)})<0,\qquad\frac{f_0(x^{(k)})-g(\lambda^{(k)},\nu^{(k)})}{-f_0(x^{(k)})}\leq\epsilon_{\mathrm{rel}}
$$

成立，那么 $p^\star\neq0$，并且可以保证相对误差

$$
\frac{f_0(x^{(k)})-p^\star}{|p^\star|}
$$

不超过 $\epsilon_{\mathrm{rel}}$。

### 5.5.2 互补松弛性

假设原最优值和对偶最优值都能达到，且两者相等（所以，特别地，强对偶性成立）。设 $x^\star$ 为原最优点，$(\lambda^\star,\nu^\star)$ 为对偶最优点。这意味着

$$
\begin{aligned}
f_0(x^\star)&=g(\lambda^\star,\nu^\star)\\
&=\inf_x\left(f_0(x)+\sum_{i=1}^m\lambda_i^\star f_i(x)+\sum_{i=1}^p\nu_i^\star h_i(x)\right)\\
&\leq f_0(x^\star)+\sum_{i=1}^m\lambda_i^\star f_i(x^\star)+\sum_{i=1}^p\nu_i^\star h_i(x^\star)\\
&\leq f_0(x^\star).
\end{aligned}
$$

第一行表示最优对偶间隙为零，第二行是对偶函数的定义。第三行来自这样一个事实：拉格朗日函数对 $x$ 的下确界，不大于它在 $x=x^\star$ 处的值。最后一个不等式来自 $\lambda_i^\star\geq0$、$f_i(x^\star)\leq0$，$i=1,\ldots,m$，以及 $h_i(x^\star)=0$，$i=1,\ldots,p$。由此可知，这一连串关系中的两个不等式都取等号。

<!-- pdf-page: 257 -->

从中可以得到几个有趣的结论。例如，由于第三行的不等式取等号，可知 $x^\star$ 使 $L(x,\lambda^\star,\nu^\star)$ 对 $x$ 取得最小值。（拉格朗日函数 $L(x,\lambda^\star,\nu^\star)$ 可以还有其他最小值点；$x^\star$ 只是其中一个。）

另一个重要结论是

$$
\sum_{i=1}^m\lambda_i^\star f_i(x^\star)=0.
$$

由于这个和式中的每一项都非正，可知

$$
\lambda_i^\star f_i(x^\star)=0,\qquad i=1,\ldots,m.\tag{5.48}
$$

这个条件称为**互补松弛性**（complementary slackness）；当强对偶性成立时，它对任意原最优点 $x^\star$ 和任意对偶最优点 $(\lambda^\star,\nu^\star)$ 都成立。互补松弛条件可以写成

$$
\lambda_i^\star>0\quad\Longrightarrow\quad f_i(x^\star)=0,
$$

或者等价地写成

$$
f_i(x^\star)<0\quad\Longrightarrow\quad\lambda_i^\star=0.
$$

大致地说，这意味着，除非第 $i$ 个约束在最优点处有效，否则第 $i$ 个最优拉格朗日乘子为零。

### 5.5.3 KKT 最优性条件

现在假设函数 $f_0,\ldots,f_m,h_1,\ldots,h_p$ 可微（因而具有开定义域），但暂时不对凸性作任何假设。

#### 非凸问题的 KKT 条件

与前面一样，设 $x^\star$ 和 $(\lambda^\star,\nu^\star)$ 是任意一对对偶间隙为零的原、对偶最优点。由于 $x^\star$ 使 $L(x,\lambda^\star,\nu^\star)$ 对 $x$ 取得最小值，其梯度在 $x^\star$ 处必定为零，即

$$
\nabla f_0(x^\star)+\sum_{i=1}^m\lambda_i^\star\nabla f_i(x^\star)+\sum_{i=1}^p\nu_i^\star\nabla h_i(x^\star)=0.
$$

因此，有

$$
\begin{aligned}
f_i(x^\star)&\leq0,\quad i=1,\ldots,m\\
h_i(x^\star)&=0,\quad i=1,\ldots,p\\
\lambda_i^\star&\geq0,\quad i=1,\ldots,m\\
\lambda_i^\star f_i(x^\star)&=0,\quad i=1,\ldots,m\\
\nabla f_0(x^\star)+\sum_{i=1}^m\lambda_i^\star\nabla f_i(x^\star)+\sum_{i=1}^p\nu_i^\star\nabla h_i(x^\star)&=0,
\end{aligned}\tag{5.49}
$$

这些条件称为 **Karush–Kuhn–Tucker（KKT）条件**。

综上，对于任意一个目标函数和约束函数都可微、并且具有强对偶性的优化问题，任意一对原、对偶最优点都必须满足 KKT 条件 (5.49)。

<!-- pdf-page: 258 -->

#### 凸问题的 KKT 条件

当原问题为凸问题时，KKT 条件也是原、对偶点最优的充分条件。换言之，如果 $f_i$ 是凸函数，$h_i$ 是仿射函数，而 $\widetilde x,\widetilde\lambda,\widetilde\nu$ 是任意满足 KKT 条件

$$
\begin{aligned}
f_i(\widetilde x)&\leq0,\quad i=1,\ldots,m\\
h_i(\widetilde x)&=0,\quad i=1,\ldots,p\\
\widetilde\lambda_i&\geq0,\quad i=1,\ldots,m\\
\widetilde\lambda_i f_i(\widetilde x)&=0,\quad i=1,\ldots,m\\
\nabla f_0(\widetilde x)+\sum_{i=1}^m\widetilde\lambda_i\nabla f_i(\widetilde x)+\sum_{i=1}^p\widetilde\nu_i\nabla h_i(\widetilde x)&=0
\end{aligned}
$$

的点，那么 $\widetilde x$ 和 $(\widetilde\lambda,\widetilde\nu)$ 分别原最优和对偶最优，且对偶间隙为零。

为说明这一点，注意前两个条件表明 $\widetilde x$ 原可行。由于 $\widetilde\lambda_i\geq0$，$L(x,\widetilde\lambda,\widetilde\nu)$ 关于 $x$ 是凸函数；最后一个 KKT 条件表明，它关于 $x$ 的梯度在 $x=\widetilde x$ 处为零，因此 $\widetilde x$ 使 $L(x,\widetilde\lambda,\widetilde\nu)$ 对 $x$ 取得最小值。由此可知

$$
\begin{aligned}
g(\widetilde\lambda,\widetilde\nu)&=L(\widetilde x,\widetilde\lambda,\widetilde\nu)\\
&=f_0(\widetilde x)+\sum_{i=1}^m\widetilde\lambda_i f_i(\widetilde x)+\sum_{i=1}^p\widetilde\nu_i h_i(\widetilde x)\\
&=f_0(\widetilde x),
\end{aligned}
$$

其中最后一行用到了 $h_i(\widetilde x)=0$ 和 $\widetilde\lambda_i f_i(\widetilde x)=0$。这说明 $\widetilde x$ 和 $(\widetilde\lambda,\widetilde\nu)$ 的对偶间隙为零，因此分别原最优和对偶最优。综上，对于任意目标函数和约束函数都可微的凸优化问题，满足 KKT 条件的任意一组点，都分别原最优和对偶最优，并且对偶间隙为零。

如果目标函数和约束函数都可微的凸优化问题满足 Slater 条件，那么 KKT 条件就是最优性的充要条件：Slater 条件意味着最优对偶间隙为零，且对偶最优值能够达到，因此 $x$ 最优，当且仅当存在 $(\lambda,\nu)$ 与 $x$ 一起满足 KKT 条件。

KKT 条件在优化中起着重要作用。在少数特殊情形下，可以解析地求解 KKT 条件（从而求解优化问题）。更一般地，许多凸优化算法就是为求解 KKT 条件而设计的，或者可以解释为求解 KKT 条件的方法。

<div class="example" markdown="1">

**例 5.1 带等式约束的凸二次最小化。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & (1/2)x^TPx+q^Tx+r\\
\text{约束条件} & Ax=b,
\end{array}\tag{5.50}
$$

其中 $P\in\mathbf{S}_+^n$。这个问题的 KKT 条件为

$$
Ax^\star=b,\qquad Px^\star+q+A^T\nu^\star=0,
$$

可以写成

$$
\begin{bmatrix}P&A^T\\A&0\end{bmatrix}\begin{bmatrix}x^\star\\\nu^\star\end{bmatrix}=\begin{bmatrix}-q\\b\end{bmatrix}.
$$

<!-- pdf-page: 259 -->

求解这个关于 $m+n$ 个变量 $x^\star,\nu^\star$ 的 $m+n$ 个方程所组成的方程组，就得到了 (5.50) 的最优原变量和最优对偶变量。

</div>

<div class="example" markdown="1">

**例 5.2 注水。** 考虑凸优化问题

$$
\begin{array}{ll}
\text{最小化} & -\sum_{i=1}^n\log(\alpha_i+x_i)\\
\text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

其中 $\alpha_i>0$。这个问题出现在信息论中，要为 $n$ 个通信信道分配功率。变量 $x_i$ 表示分配给第 $i$ 个信道的发射功率，$\log(\alpha_i+x_i)$ 给出该信道的容量或通信速率。因此，问题是把总量为 1 的功率分配给这些信道，使总通信速率最大。

为不等式约束 $x^\star\succeq0$ 引入拉格朗日乘子 $\lambda^\star\in\mathbf{R}^n$，为等式约束 $\mathbf{1}^Tx=1$ 引入乘子 $\nu^\star\in\mathbf{R}$，得到 KKT 条件

$$
\begin{gathered}
x^\star\succeq0,\quad\mathbf{1}^Tx^\star=1,\quad\lambda^\star\succeq0,\quad\lambda_i^\star x_i^\star=0,\quad i=1,\ldots,n,\\
-1/(\alpha_i+x_i^\star)-\lambda_i^\star+\nu^\star=0,\quad i=1,\ldots,n.
\end{gathered}
$$

直接求解这些方程，就能求出 $x^\star,\lambda^\star,\nu^\star$。首先注意，$\lambda^\star$ 在最后一个方程中起松弛变量的作用，因此可以将它消去，剩下

$$
\begin{gathered}
x^\star\succeq0,\quad\mathbf{1}^Tx^\star=1,\quad x_i^\star(\nu^\star-1/(\alpha_i+x_i^\star))=0,\quad i=1,\ldots,n,\\
\nu^\star\geq1/(\alpha_i+x_i^\star),\quad i=1,\ldots,n.
\end{gathered}
$$

如果 $\nu^\star<1/\alpha_i$，那么最后一个条件只有在 $x_i^\star>0$ 时才可能成立，再由第三个条件可知 $\nu^\star=1/(\alpha_i+x_i^\star)$。解出 $x_i^\star$，可知当 $\nu^\star<1/\alpha_i$ 时，$x_i^\star=1/\nu^\star-\alpha_i$。如果 $\nu^\star\geq1/\alpha_i$，那么 $x_i^\star>0$ 不可能成立，因为这将意味着 $\nu^\star\geq1/\alpha_i>1/(\alpha_i+x_i^\star)$，违反互补松弛条件。因此，当 $\nu^\star\geq1/\alpha_i$ 时，$x_i^\star=0$。于是有

$$
x_i^\star=\begin{cases}1/\nu^\star-\alpha_i&\nu^\star<1/\alpha_i\\0&\nu^\star\geq1/\alpha_i,\end{cases}
$$

或者更简洁地写成 $x_i^\star=\max\{0,1/\nu^\star-\alpha_i\}$。将 $x_i^\star$ 的这个表达式代入条件 $\mathbf{1}^Tx^\star=1$，得到

$$
\sum_{i=1}^n\max\{0,1/\nu^\star-\alpha_i\}=1.
$$

左边是 $1/\nu^\star$ 的分段线性递增函数，转折点为 $\alpha_i$，因此这个方程有唯一解，而且很容易求出。

这种求解方法称为**注水算法**（water-filling），原因如下。把 $\alpha_i$ 看作第 $i$ 块地面的高度，然后向这片区域注水至水位 $1/\nu$，如图 5.7 所示。此时总用水量为 $\sum_{i=1}^n\max\{0,1/\nu^\star-\alpha_i\}$。不断提高水位，直到总用水量等于 1。第 $i$ 块地面上方的水深就是最优值 $x_i^\star$。

</div>

<!-- pdf-page: 260 -->

<figure id="fig-5-7" data-figure="5.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-7.png" alt="高低不等的阶梯状地面与统一水位，阴影表示水，右侧箭头分别标出水深和地面高度" data-source-page="260" data-source-rect="227,121,433,236">
<figcaption>图 5.7 注水算法的示意图。每块地面的高度为 $\alpha_i$。向这片区域注水至水位 $1/\nu^\star$，总用水量为 1。每块地面上方的水深（用阴影表示）就是最优值 $x_i^\star$。</figcaption>
</figure>

<figure id="fig-5-8" data-figure="5.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-8.png" alt="两个宽度均为 w 的物块通过三个弹簧彼此相连并连接两端墙壁，下方标出物块中心位置和墙间距离" data-source-page="260" data-source-rect="229,305,450,415">
<figcaption>图 5.8 两个物块通过弹簧彼此相连，并与左右两侧的墙壁相连。物块的宽度为 $w>0$，不能相互穿透，也不能穿过墙壁。</figcaption>
</figure>

### 5.5.4 KKT 条件的力学解释

KKT 条件在力学中有一个很好的解释（事实上，这也是 Lagrange 最初研究它的主要动机之一）。我们用一个简单例子说明这个想法。图 5.8 中的系统由两个物块组成，它们通过三根弹簧彼此相连，并与左右两侧的墙壁相连。物块的位置由 $x\in\mathbf{R}^2$ 给出，其中 $x_1$ 为左侧物块（中心）的位移，$x_2$ 为右侧物块的位移。左墙的位置为 0，右墙的位置为 $l$。

弹簧的势能是物块位置的函数，表达式为

$$
f_0(x_1,x_2)=\frac12 k_1x_1^2+\frac12 k_2(x_2-x_1)^2+\frac12 k_3(l-x_2)^2,
$$

其中 $k_i>0$ 是三根弹簧的刚度系数。平衡位置 $x^\star$ 是在满足不等式

$$
w/2-x_1\leq0,\qquad w+x_1-x_2\leq0,\qquad w/2-l+x_2\leq0\tag{5.51}
$$

的条件下，使势能最小的位置。

<!-- pdf-page: 261 -->

<figure id="fig-5-9" data-figure="5.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-9.png" alt="两个物块的受力图，上方箭头表示接触力，下方箭头表示弹簧力" data-source-page="261" data-source-rect="128,120,463,152">
<figcaption>图 5.9 物块与弹簧系统的受力分析。每个物块受到的弹簧力与接触力的合力必须为零。上方标出的拉格朗日乘子，是墙壁和物块之间的接触力。弹簧力标在下方。</figcaption>
</figure>

这些约束称为**运动学约束**（kinematic constraints），表示物块的宽度为 $w>0$，并且不能相互穿透，也不能穿过墙壁。因此，平衡位置由优化问题

$$
\begin{array}{ll}
\text{最小化} & (1/2)\bigl(k_1x_1^2+k_2(x_2-x_1)^2+k_3(l-x_2)^2\bigr)\\
\text{约束条件} & w/2-x_1\leq0\\
& w+x_1-x_2\leq0\\
& w/2-l+x_2\leq0
\end{array}\tag{5.52}
$$

的解给出，这是一个 QP。

以 $\lambda_1,\lambda_2,\lambda_3$ 为拉格朗日乘子，这个问题的 KKT 条件包括运动学约束 (5.51)、非负性约束 $\lambda_i\geq0$、互补松弛条件

$$
\lambda_1(w/2-x_1)=0,\quad\lambda_2(w-x_2+x_1)=0,\quad\lambda_3(w/2-l+x_2)=0,\tag{5.53}
$$

以及梯度为零的条件

$$
\begin{bmatrix}k_1x_1-k_2(x_2-x_1)\\k_2(x_2-x_1)-k_3(l-x_2)\end{bmatrix}+\lambda_1\begin{bmatrix}-1\\0\end{bmatrix}+\lambda_2\begin{bmatrix}1\\-1\end{bmatrix}+\lambda_3\begin{bmatrix}0\\1\end{bmatrix}=0.\tag{5.54}
$$

只要把拉格朗日乘子解释为墙壁与物块之间的*接触力*，方程 (5.54) 就可以解释为两个物块的力平衡方程，如图 5.9 所示。第一个方程表示第一个物块所受各力之和为零：$-k_1x_1$ 是左侧弹簧对左侧物块的作用力，$k_2(x_2-x_1)$ 是中间弹簧的作用力，$\lambda_1$ 是左墙的作用力，而 $-\lambda_2$ 是右侧物块的作用力。接触力必须指向离开接触面的方向（由约束 $\lambda_1\geq0$ 和 $-\lambda_2\leq0$ 表示），而且只有发生接触时才可能非零（由 (5.53) 中前两个互补松弛条件表示）。类似地，(5.54) 中第二个方程表示第二个物块的力平衡，而 (5.53) 中最后一个条件表明，除非右侧物块接触墙壁，否则 $\lambda_3$ 为零。

在这个例子中，势能和运动学约束函数都是凸函数；只要 $2w\leq l$，即两墙之间有足够空间容纳两个物块，Slater 约束资格条件（的细化形式）就成立。因此，(5.52) 给出的平衡位置的能量表述，与 KKT 条件给出的力平衡表述，会得到相同结果。

<!-- pdf-page: 262 -->

### 5.5.5 通过对偶问题求解原问题

在 §5.5.3 开头我们提到，如果强对偶性成立，且存在对偶最优解 $(\lambda^\star,\nu^\star)$，那么任意原最优点也是 $L(x,\lambda^\star,\nu^\star)$ 的最小值点。利用这个事实，有时可以根据一个对偶最优解，求出一个原最优解。

更准确地说，假设强对偶性成立，并且已知最优的 $(\lambda^\star,\nu^\star)$。假设 $L(x,\lambda^\star,\nu^\star)$ 的最小值点，即问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)+\sum_{i=1}^m\lambda_i^\star f_i(x)+\sum_{i=1}^p\nu_i^\star h_i(x),
\end{array}\tag{5.55}
$$

的解，是唯一的。（对于凸问题，例如当 $L(x,\lambda^\star,\nu^\star)$ 关于 $x$ 严格凸时，就会如此。）那么，如果 (5.55) 的解原可行，它就必定原最优；如果它原不可行，那么就不存在原最优点，即可以断定原最优值不能达到。当对偶问题比原问题更容易求解时，例如对偶问题可以解析求解，或者具有某种可以利用的特殊结构时，这一结论很有意义。

<div class="example" markdown="1">

**例 5.3 熵最大化。** 考虑定义域为 $\mathbf{R}_{++}^n$ 的熵最大化问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)=\sum_{i=1}^n x_i\log x_i\\
\text{约束条件} & Ax\preceq b\\
& \mathbf{1}^Tx=1
\end{array}
$$

及其对偶问题

$$
\begin{array}{ll}
\text{最大化} & -b^T\lambda-\nu-e^{-\nu-1}\sum_{i=1}^n e^{-a_i^T\lambda}\\
\text{约束条件} & \lambda\succeq0,
\end{array}
$$

其中 $a_i$ 为 $A$ 的各列（见原书第 222 页和第 228 页）。我们假设较弱形式的 Slater 条件成立，即存在 $x\succ0$ 满足 $Ax\preceq b$ 和 $\mathbf{1}^Tx=1$，因此强对偶性成立，且存在最优解 $(\lambda^\star,\nu^\star)$。

假设已经求解了对偶问题。拉格朗日函数在 $(\lambda^\star,\nu^\star)$ 处为

$$
L(x,\lambda^\star,\nu^\star)=\sum_{i=1}^n x_i\log x_i+(\lambda^\star)^T(Ax-b)+\nu^\star(\mathbf{1}^Tx-1),
$$

它在 $\mathcal{D}$ 上严格凸且有下界，因此有唯一解 $x^\star$，其表达式为

$$
x_i^\star=1/\exp(a_i^T\lambda^\star+\nu^\star+1),\qquad i=1,\ldots,n.
$$

如果 $x^\star$ 原可行，它就必定是原问题 (5.13) 的最优解。如果 $x^\star$ 原不可行，就可以断定原最优值不能达到。

</div>

<div class="example" markdown="1">

**例 5.4 在等式约束下最小化可分函数。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)=\sum_{i=1}^n f_i(x_i)\\
\text{约束条件} & a^Tx=b,
\end{array}
$$

<!-- pdf-page: 263 -->

其中 $a\in\mathbf{R}^n$，$b\in\mathbf{R}$，$f_i:\mathbf{R}\to\mathbf{R}$ 可微且严格凸。目标函数称为**可分函数**（separable function），因为它是各个变量 $x_1,\ldots,x_n$ 的函数之和。假设 $f_0$ 的定义域与约束集合相交，即存在点 $x_0\in\operatorname{\mathbf{dom}}f_0$，使得 $a^Tx_0=b$。这意味着问题存在唯一最优点 $x^\star$。

拉格朗日函数为

$$
L(x,\nu)=\sum_{i=1}^n f_i(x_i)+\nu(a^Tx-b)=-b\nu+\sum_{i=1}^n(f_i(x_i)+\nu a_i x_i),
$$

它也是可分的，因此对偶函数为

$$
\begin{aligned}
g(\nu)&=-b\nu+\inf_x\left(\sum_{i=1}^n(f_i(x_i)+\nu a_i x_i)\right)\\
&=-b\nu+\sum_{i=1}^n\inf_{x_i}(f_i(x_i)+\nu a_i x_i)\\
&=-b\nu-\sum_{i=1}^n f_i^*(-\nu a_i).
\end{aligned}
$$

所以对偶问题为

$$
\begin{array}{ll}
\text{最大化} & -b\nu-\sum_{i=1}^n f_i^*(-\nu a_i),
\end{array}
$$

其中（标量）变量为 $\nu\in\mathbf{R}$。

现在假设已经找到一个最优对偶变量 $\nu^\star$。（对于只有一个标量变量的凸问题，有若干简单的求解方法，例如二分法。）由于每个 $f_i$ 都严格凸，函数 $L(x,\nu^\star)$ 关于 $x$ 严格凸，因而有唯一最小值点 $\widetilde x$。但我们也知道，$x^\star$ 使 $L(x,\nu^\star)$ 取得最小值，所以必定有 $\widetilde x=x^\star$。可以利用 $\nabla_x L(x,\nu^\star)=0$ 恢复 $x^\star$，即求解方程 $f_i'(x_i^\star)=-\nu^\star a_i$。

</div>

<div class="translator-note" markdown="1">

**译注（例 5.4）：** 严格凸性只保证最优点如果存在就唯一，不能保证最优值能够达到。例如，取 $f_1(t)=f_2(t)=e^t$、$a=(1,-1)$、$b=0$，则可行点为 $(t,t)$，目标值为 $2e^t$；下确界为 $0$，但不存在最优点。此例后续使用 $x^\star$ 时，还需假设最优值能够达到。

</div>

## 5.6 扰动与灵敏度分析

当强对偶性成立时，最优对偶变量能够提供很有用的信息，说明最优值对约束扰动的敏感程度。

### 5.6.1 扰动问题

考虑原优化问题 (5.1) 的如下扰动形式：

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq u_i,\quad i=1,\ldots,m\\
& h_i(x)=v_i,\quad i=1,\ldots,p,
\end{array}\tag{5.56}
$$

<!-- pdf-page: 264 -->

其中变量为 $x\in\mathbf{R}^n$。当 $u=0$、$v=0$ 时，这个问题与原问题 (5.1) 相同。$u_i$ 为正意味着放宽第 $i$ 个不等式约束；$u_i$ 为负意味着收紧该约束。因此，将原问题 (5.1) 的各个不等式约束按照 $u_i$ 收紧或放宽，并将等式约束的右端改动 $v_i$，就得到了扰动问题 (5.56)。

定义 $p^\star(u,v)$ 为扰动问题 (5.56) 的最优值：

$$
\begin{aligned}
p^\star(u,v)=\inf\{f_0(x)\mid{}&\exists x\in\mathcal{D},\ f_i(x)\leq u_i,\ i=1,\ldots,m,\\
&h_i(x)=v_i,\ i=1,\ldots,p\}.
\end{aligned}
$$

可能出现 $p^\star(u,v)=\infty$，这对应于约束扰动导致问题不可行的情形。注意，$p^\star(0,0)=p^\star$，即未扰动问题 (5.1) 的最优值。（希望这种略微混用记号的做法不会造成混淆。）大致地说，函数 $p^\star:\mathbf{R}^m\times\mathbf{R}^p\to\mathbf{R}$ 描述了问题最优值如何随约束右端的扰动而变化。

当原问题是凸问题时，函数 $p^\star$ 关于 $u$ 和 $v$ 是凸函数；事实上，其上图恰好是 (5.37) 定义的集合 $\mathcal{A}$ 的闭包（见习题 5.32）。

<div class="translator-note" markdown="1">

**译注（扰动值函数的上图）：** 凸函数的上图不一定是闭集；原句还需要 $p^\star$ 为闭函数。例如，考虑最小化 $0$、约束为 $e^{-x}-1\leq u$ 的扰动问题：$p^\star(u)=0$ 当 $u>-1$，而 $p^\star(u)=+\infty$ 当 $u\leq-1$。此时 $\mathcal{A}=\operatorname{\mathbf{epi}}p^\star=\{(u,t)\mid u>-1,\ t\geq0\}$，其闭包还包含 $u=-1$ 的边界点。

</div>

### 5.6.2 一个全局不等式

现在假设强对偶性成立，且对偶最优值能够达到。（如果原问题为凸问题，且满足 Slater 条件，就属于这种情形。）设 $(\lambda^\star,\nu^\star)$ 是未扰动问题的对偶问题 (5.16) 的最优点。那么，对于所有 $u$ 和 $v$，都有

$$
p^\star(u,v)\geq p^\star(0,0)-(\lambda^\star)^Tu-(\nu^\star)^Tv.\tag{5.57}
$$

为证明这个不等式，设 $x$ 是扰动问题的任意可行点，即 $f_i(x)\leq u_i$，$i=1,\ldots,m$，且 $h_i(x)=v_i$，$i=1,\ldots,p$。由强对偶性可得

$$
\begin{aligned}
p^\star(0,0)=g(\lambda^\star,\nu^\star)&\leq f_0(x)+\sum_{i=1}^m\lambda_i^\star f_i(x)+\sum_{i=1}^p\nu_i^\star h_i(x)\\
&\leq f_0(x)+(\lambda^\star)^Tu+(\nu^\star)^Tv.
\end{aligned}
$$

（第一个不等式来自 $g(\lambda^\star,\nu^\star)$ 的定义；第二个不等式来自 $\lambda^\star\succeq0$。）因此，对于扰动问题的任意可行点 $x$，都有

$$
f_0(x)\geq p^\star(0,0)-(\lambda^\star)^Tu-(\nu^\star)^Tv,
$$

从而得到 (5.57)。

#### 灵敏度解释

当强对偶性成立时，不等式 (5.57) 直接给出了最优拉格朗日变量的多种灵敏度解释。其中一些结论如下：

<!-- pdf-page: 265 -->

<figure id="fig-5-10" data-figure="5.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-10.png" alt="凸问题的最优值曲线与仿射下界直线，竖向点线标出没有扰动的位置 u=0" data-source-page="265" data-source-rect="176,121,415,290">
<figcaption>图 5.10 具有单个约束 $f_1(x)\leq u$ 的凸问题的最优值 $p^\star(u)$ 随 $u$ 的变化。当 $u=0$ 时，得到原来的未扰动问题；当 $u<0$ 时，约束收紧；当 $u>0$ 时，约束放宽。仿射函数 $p^\star(0)-\lambda^\star u$ 是 $p^\star$ 的一个下界。</figcaption>
</figure>

- 如果 $\lambda_i^\star$ 很大，并且收紧第 $i$ 个约束（即选择 $u_i<0$），那么最优值 $p^\star(u,v)$ 必定大幅增大。

- 如果 $\nu_i^\star$ 为正且很大，并取 $v_i<0$；或者 $\nu_i^\star$ 为负且绝对值很大，并取 $v_i>0$，那么最优值 $p^\star(u,v)$ 必定大幅增大。

- 如果 $\lambda_i^\star$ 很小，并且放宽第 $i$ 个约束（$u_i>0$），那么最优值 $p^\star(u,v)$ 不会下降太多。

- 如果 $\nu_i^\star$ 为正且很小，并取 $v_i>0$；或者 $\nu_i^\star$ 为负且绝对值很小，并取 $v_i<0$，那么最优值 $p^\star(u,v)$ 不会下降太多。

不等式 (5.57) 和上面列出的结论给出了扰动后最优值的下界，却没有给出上界。因此，这些结论对于放宽和收紧约束并不对称。例如，假设 $\lambda_i^\star$ 很大，而我们稍微放宽第 $i$ 个约束（即取很小的正数 $u_i$）。此时不等式 (5.57) 并没有什么用处；例如，它并不意味着最优值会显著下降。

图 5.10 用一个只有单个不等式约束的凸问题说明了不等式 (5.57)。这个不等式表明，仿射函数 $p^\star(0)-\lambda^\star u$ 是凸函数 $p^\star$ 的一个下界。

### 5.6.3 局部灵敏度分析

现在假设 $p^\star(u,v)$ 在 $u=0$、$v=0$ 处可微。那么，只要强对偶性成立，最优对偶变量 $\lambda^\star,\nu^\star$ 就与 $p^\star$ 在<!-- pdf-page: 266 -->$u=0$、$v=0$ 处的梯度具有如下关系：

$$
\lambda_i^\star=-\frac{\partial p^\star(0,0)}{\partial u_i},\qquad\nu_i^\star=-\frac{\partial p^\star(0,0)}{\partial v_i}.\tag{5.58}
$$

从图 5.10 的例子中可以看出这一性质，其中 $-\lambda^\star$ 就是 $p^\star$ 在 $u=0$ 附近的斜率。

因此，当 $p^\star(u,v)$ 在 $u=0$、$v=0$ 处可微，且强对偶性成立时，最优拉格朗日乘子恰好就是最优值对约束扰动的局部灵敏度。与不可微情形不同，这种解释是对称的：将第 $i$ 个不等式约束稍微收紧（即取绝对值很小的负数 $u_i$），会使 $p^\star$ 增加约 $-\lambda_i^\star u_i$；将第 $i$ 个约束稍微放宽（即取很小的正数 $u_i$），会使 $p^\star$ 减少约 $\lambda_i^\star u_i$。

为证明 (5.58)，假设 $p^\star(u,v)$ 可微，且强对偶性成立。对于扰动 $u=te_i$、$v=0$，其中 $e_i$ 是第 $i$ 个单位向量，有

$$
\lim_{t\to0}\frac{p^\star(te_i,0)-p^\star}{t}=\frac{\partial p^\star(0,0)}{\partial u_i}.
$$

不等式 (5.57) 表明，当 $t>0$ 时，

$$
\frac{p^\star(te_i,0)-p^\star}{t}\geq-\lambda_i^\star,
$$

而当 $t<0$ 时，不等号方向相反。令 $t>0$ 并取极限 $t\to0$，得到

$$
\frac{\partial p^\star(0,0)}{\partial u_i}\geq-\lambda_i^\star,
$$

而令 $t<0$ 取极限时，得到方向相反的不等式，因此可知

$$
\frac{\partial p^\star(0,0)}{\partial u_i}=-\lambda_i^\star.
$$

用同样的方法可以证明

$$
\frac{\partial p^\star(0,0)}{\partial v_i}=-\nu_i^\star.
$$

局部灵敏度结果 (5.58) 为约束在最优点 $x^\star$ 处的有效程度提供了定量度量。如果 $f_i(x^\star)<0$，那么这个约束是非有效的，因此将它稍微收紧或放宽，不会影响最优值。由互补松弛性，对应的最优拉格朗日乘子必定为零。现在假设 $f_i(x^\star)=0$，即第 $i$ 个约束在最优点处有效。第 $i$ 个最优拉格朗日乘子告诉我们这个约束有多有效：如果 $\lambda_i^\star$ 很小，说明将约束稍微放宽或收紧，对最优值影响不大；如果 $\lambda_i^\star$ 很大，说明将约束稍微放宽或收紧，都会对最优值产生很大影响。

<!-- pdf-page: 267 -->

#### 影子价格解释

我们也可以从经济学角度，对结果 (5.58) 给出一个简单的几何解释。为简便起见，考虑一个没有等式约束、满足 Slater 条件的凸问题。变量 $x\in\mathbf{R}^m$ 决定企业如何经营，目标函数 $f_0$ 是成本，即 $-f_0$ 是利润。每个约束 $f_i(x)\leq0$ 都表示某种资源的限制，例如劳动力、钢材或仓储空间。扰动后最优成本的负值函数 $-p^\star(u)$，表示如果企业可以使用的各项资源增加或减少，其利润会增加或减少多少。如果这个函数在 $u=0$ 附近可微，则有

$$
\lambda_i^\star=-\frac{\partial p^\star(0)}{\partial u_i}.
$$

换言之，$\lambda_i^\star$ 告诉我们，当资源 $i$ 的可用量少量增加时，企业的利润大约能够增加多少。

因此，如果企业能够买卖资源 $i$，$\lambda_i^\star$ 就是该资源的自然价格或**均衡价格**。例如，假设企业能够以低于 $\lambda_i^\star$ 的价格买卖资源 $i$。此时企业一定会购买一些该资源，因为这会使企业能够采用新的经营方式，增加的利润超过购买资源的成本。反过来，如果价格超过 $\lambda_i^\star$，企业就会卖出一部分分配给自己的资源 $i$，从而获得净收益，因为出售资源的收入会超过资源可用量减少所导致的利润下降。

## 5.7 例子

本节通过例子说明，对一个问题作简单的等价改写，可能得到很不相同的对偶问题。我们考虑以下几类改写：

- 引入新变量及相应的等式约束。

- 用原目标函数的一个递增函数替换目标函数。

- 将显式约束变成隐式约束，即把它们并入目标函数的定义域。

### 5.7.1 引入新变量和等式约束

考虑如下形式的无约束问题：

$$
\begin{array}{ll}\text{最小化} & f_0(Ax+b).\end{array}\tag{5.59}
$$

它的拉格朗日对偶函数是常数 $p^\star$。因此，虽然强对偶性确实成立，即 $p^\star=d^\star$，但这个拉格朗日对偶既没有用处，也没有什么值得研究的内容。

<!-- pdf-page: 268 -->

现在把问题 (5.59) 改写为

$$
\begin{array}{ll}
\text{最小化} & f_0(y)\\
\text{约束条件} & Ax+b=y.
\end{array}\tag{5.60}
$$

这里引入了新变量 $y$ 和新的等式约束 $Ax+b=y$。问题 (5.59) 和 (5.60) 显然等价。

改写后问题的拉格朗日函数为

$$
L(x,y,\nu)=f_0(y)+\nu^T(Ax+b-y).
$$

为求对偶函数，我们对 $x$ 和 $y$ 最小化 $L$。对 $x$ 最小化可知，除非 $A^T\nu=0$，否则 $g(\nu)=-\infty$；当 $A^T\nu=0$ 时，剩下

$$
g(\nu)=b^T\nu+\inf_y(f_0(y)-\nu^Ty)=b^T\nu-f_0^*(\nu),
$$

其中 $f_0^*$ 是 $f_0$ 的共轭函数。因此，(5.60) 的对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & b^T\nu-f_0^*(\nu)\\
\text{约束条件} & A^T\nu=0.
\end{array}\tag{5.61}
$$

这样，改写后问题 (5.60) 的对偶，就比原问题 (5.59) 的对偶有用得多。

<div class="example" markdown="1">

**例 5.5 无约束几何规划。** 考虑无约束几何规划

$$
\begin{array}{ll}\text{最小化} & \log\left(\sum_{i=1}^m\exp(a_i^Tx+b_i)\right).\end{array}
$$

首先引入新变量和等式约束，将它改写为

$$
\begin{array}{ll}
\text{最小化} & f_0(y)=\log\left(\sum_{i=1}^m\exp y_i\right)\\
\text{约束条件} & Ax+b=y,
\end{array}
$$

其中 $a_i^T$ 为 $A$ 的各行。指数和的对数（log-sum-exp）函数的共轭函数为

$$
f_0^*(\nu)=\begin{cases}\sum_{i=1}^m\nu_i\log\nu_i&\nu\succeq0,\quad\mathbf{1}^T\nu=1\\\infty&\text{其他情形}\end{cases}
$$

（例 3.25，原书第 93 页），因此改写后问题的对偶可以表示为

$$
\begin{array}{ll}
\text{最大化} & b^T\nu-\sum_{i=1}^m\nu_i\log\nu_i\\
\text{约束条件} & \mathbf{1}^T\nu=1\\
& A^T\nu=0\\
& \nu\succeq0,
\end{array}\tag{5.62}
$$

这是一个熵最大化问题。

</div>

<div class="example" markdown="1">

**例 5.6 范数逼近问题。** 考虑无约束范数逼近问题

$$
\begin{array}{ll}\text{最小化} & \|Ax-b\|,\end{array}\tag{5.63}
$$

其中 $\|\cdot\|$ 为任意范数。这里的拉格朗日对偶函数同样是常数，等于 (5.63) 的最优值，因此没有用处。

<!-- pdf-page: 269 -->

我们再次把问题改写为

$$
\begin{array}{ll}
\text{最小化} & \|y\|\\
\text{约束条件} & Ax-b=y.
\end{array}
$$

由 (5.61)，拉格朗日对偶问题为

$$
\begin{array}{ll}
\text{最大化} & b^T\nu\\
\text{约束条件} & \|\nu\|_*\leq1\\
& A^T\nu=0,
\end{array}\tag{5.64}
$$

其中用到了这样一个事实：范数的共轭函数是对偶范数单位球的指示函数（例 3.26，原书第 93 页）。

</div>

引入新等式约束的思路同样可以用于约束函数。例如，考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(A_0x+b_0)\\
\text{约束条件} & f_i(A_ix+b_i)\leq0,\quad i=1,\ldots,m,
\end{array}\tag{5.65}
$$

其中 $A_i\in\mathbf{R}^{k_i\times n}$，$f_i:\mathbf{R}^{k_i}\to\mathbf{R}$ 为凸函数。（为简便起见，这里不包含等式约束。）引入新变量 $y_i\in\mathbf{R}^{k_i}$，$i=0,\ldots,m$，将问题改写为

$$
\begin{array}{ll}
\text{最小化} & f_0(y_0)\\
\text{约束条件} & f_i(y_i)\leq0,\quad i=1,\ldots,m\\
& A_ix+b_i=y_i,\quad i=0,\ldots,m.
\end{array}\tag{5.66}
$$

这个问题的拉格朗日函数为

$$
L(x,y_0,\ldots,y_m,\lambda,\nu_0,\ldots,\nu_m)=f_0(y_0)+\sum_{i=1}^m\lambda_i f_i(y_i)+\sum_{i=0}^m\nu_i^T(A_ix+b_i-y_i).
$$

为求对偶函数，对 $x$ 和 $y_i$ 最小化。除非

$$
\sum_{i=0}^m A_i^T\nu_i=0,
$$

否则对 $x$ 的最小值为 $-\infty$；在上述等式成立时，对于 $\lambda\succ0$，有

$$
\begin{aligned}
&g(\lambda,\nu_0,\ldots,\nu_m)\\
&=\sum_{i=0}^m\nu_i^Tb_i+\inf_{y_0,\ldots,y_m}\left(f_0(y_0)+\sum_{i=1}^m\lambda_i f_i(y_i)-\sum_{i=0}^m\nu_i^Ty_i\right)\\
&=\sum_{i=0}^m\nu_i^Tb_i+\inf_{y_0}(f_0(y_0)-\nu_0^Ty_0)+\sum_{i=1}^m\lambda_i\inf_{y_i}(f_i(y_i)-(\nu_i/\lambda_i)^Ty_i)\\
&=\sum_{i=0}^m\nu_i^Tb_i-f_0^*(\nu_0)-\sum_{i=1}^m\lambda_i f_i^*(\nu_i/\lambda_i).
\end{aligned}
$$

<!-- pdf-page: 270 -->

最后一个表达式涉及共轭函数的透视函数，因此关于对偶变量是凹的。最后，考虑 $\lambda\succeq0$ 但某些 $\lambda_i$ 为零时的情况。如果 $\lambda_i=0$ 且 $\nu_i\neq0$，那么对偶函数为 $-\infty$。但是，如果 $\lambda_i=0$ 且 $\nu_i=0$，那么涉及 $y_i,\nu_i,\lambda_i$ 的各项都为零。因此，只要约定：当 $\lambda_i=0$ 且 $\nu_i=0$ 时，$\lambda_i f_i^*(\nu_i/\lambda_i)=0$；当 $\lambda_i=0$ 且 $\nu_i\neq0$ 时，$\lambda_i f_i^*(\nu_i/\lambda_i)=\infty$，上面给出的 $g$ 的表达式就对所有 $\lambda\succeq0$ 有效。

所以，问题 (5.66) 的对偶可以表示为

$$
\begin{array}{ll}
\text{最大化} & \sum_{i=0}^m\nu_i^Tb_i-f_0^*(\nu_0)-\sum_{i=1}^m\lambda_i f_i^*(\nu_i/\lambda_i)\\
\text{约束条件} & \lambda\succeq0\\
& \sum_{i=0}^m A_i^T\nu_i=0.
\end{array}\tag{5.67}
$$

<div class="example" markdown="1">

**例 5.7 带不等式约束的几何规划。** 带不等式约束的几何规划

$$
\begin{array}{ll}
\text{最小化} & \log\left(\sum_{k=1}^{K_0}e^{a_{0k}^Tx+b_{0k}}\right)\\
\text{约束条件} & \log\left(\sum_{k=1}^{K_i}e^{a_{ik}^Tx+b_{ik}}\right)\leq0,\quad i=1,\ldots,m,
\end{array}
$$

具有 (5.65) 的形式，其中 $f_i:\mathbf{R}^{K_i}\to\mathbf{R}$ 由 $f_i(y)=\log\left(\sum_{k=1}^{K_i}e^{y_k}\right)$ 给出。这个函数的共轭函数为

$$
f_i^*(\nu)=\begin{cases}\sum_{k=1}^{K_i}\nu_k\log\nu_k&\nu\succeq0,\quad\mathbf{1}^T\nu=1\\\infty&\text{其他情形。}\end{cases}
$$

利用 (5.67)，可以立即写出对偶问题：

$$
\begin{array}{ll}
\text{最大化} & b_0^T\nu_0-\sum_{k=1}^{K_0}\nu_{0k}\log\nu_{0k}+\sum_{i=1}^m\left(b_i^T\nu_i-\sum_{k=1}^{K_i}\nu_{ik}\log(\nu_{ik}/\lambda_i)\right)\\
\text{约束条件} & \nu_0\succeq0,\quad\mathbf{1}^T\nu_0=1\\
& \nu_i\succeq0,\quad\mathbf{1}^T\nu_i=\lambda_i,\quad i=1,\ldots,m\\
& \lambda_i\geq0,\quad i=1,\ldots,m\\
& \sum_{i=0}^m A_i^T\nu_i=0,
\end{array}
$$

还可以进一步简化为

$$
\begin{array}{ll}
\text{最大化} & b_0^T\nu_0-\sum_{k=1}^{K_0}\nu_{0k}\log\nu_{0k}+\sum_{i=1}^m\left(b_i^T\nu_i-\sum_{k=1}^{K_i}\nu_{ik}\log(\nu_{ik}/\mathbf{1}^T\nu_i)\right)\\
\text{约束条件} & \nu_i\succeq0,\quad i=0,\ldots,m\\
& \mathbf{1}^T\nu_0=1\\
& \sum_{i=0}^m A_i^T\nu_i=0.
\end{array}
$$

</div>

### 5.7.2 变换目标函数

如果用 $f_0$ 的一个递增函数替换目标函数 $f_0$，所得问题显然与原问题等价（见 §4.1.3）。但是，这个等价问题的对偶可能与原问题的对偶很不相同。

<div class="example" markdown="1">

**例 5.8** 再次考虑最小范数问题

$$
\begin{array}{ll}\text{最小化} & \|Ax-b\|,\end{array}
$$

<!-- pdf-page: 271 -->

其中 $\|\cdot\|$ 为某个范数。将这个问题改写为

$$
\begin{array}{ll}
\text{最小化} & (1/2)\|y\|^2\\
\text{约束条件} & Ax-b=y.
\end{array}
$$

这里引入了新变量，并用原目标函数平方的一半替换目标函数。显然，它与原问题等价。

改写后问题的对偶为

$$
\begin{array}{ll}
\text{最大化} & -(1/2)\|\nu\|_*^2+b^T\nu\\
\text{约束条件} & A^T\nu=0,
\end{array}
$$

其中用到了 $(1/2)\|\cdot\|^2$ 的共轭函数为 $(1/2)\|\cdot\|_*^2$ 这一事实（见例 3.27，原书第 93 页）。

注意，这个对偶问题与先前推导出的对偶问题 (5.64) 不同。

</div>

### 5.7.3 隐式约束

接下来研究另一种简单改写：将某些约束并入目标函数，具体做法是把目标函数修改为在违反约束时取无穷大。

<div class="example" markdown="1">

**例 5.9 带盒约束的线性规划。** 考虑线性规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax=b\\
& l\preceq x\preceq u,
\end{array}\tag{5.68}
$$

其中 $A\in\mathbf{R}^{p\times n}$，$l\prec u$。约束 $l\preceq x\preceq u$ 有时称为**盒约束**或**变量界**。

当然，可以推导这个线性规划的对偶。对偶中，拉格朗日乘子 $\nu$ 对应于等式约束，$\lambda_1$ 对应于不等式约束 $x\preceq u$，$\lambda_2$ 对应于不等式约束 $l\preceq x$。对偶为

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu-\lambda_1^Tu+\lambda_2^Tl\\
\text{约束条件} & A^T\nu+\lambda_1-\lambda_2+c=0\\
& \lambda_1\succeq0,\quad\lambda_2\succeq0.
\end{array}\tag{5.69}
$$

现在换一种做法，先把问题 (5.68) 改写为

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & Ax=b,
\end{array}\tag{5.70}
$$

其中定义

$$
f_0(x)=\begin{cases}c^Tx&l\preceq x\preceq u\\\infty&\text{其他情形。}\end{cases}
$$

问题 (5.70) 显然与 (5.68) 等价；我们只是把显式的盒约束变成了隐式约束。

<!-- pdf-page: 272 -->

问题 (5.70) 的对偶函数为

$$
\begin{aligned}
g(\nu)&=\inf_{l\preceq x\preceq u}\bigl(c^Tx+\nu^T(Ax-b)\bigr)\\
&=-b^T\nu-u^T(A^T\nu+c)^-+l^T(A^T\nu+c)^+,
\end{aligned}
$$

其中 $y_i^+=\max\{y_i,0\}$，$y_i^-=\max\{-y_i,0\}$。因此，在这里可以推导出 $g$ 的解析表达式；它是一个凹的分段线性函数。

对偶问题为无约束问题

$$
\begin{array}{ll}\text{最大化} & -b^T\nu-u^T(A^T\nu+c)^-+l^T(A^T\nu+c)^+,\end{array}\tag{5.71}
$$

其形式与原问题的对偶很不相同。

（问题 (5.69) 和 (5.71) 有紧密联系，实际上两者等价；见习题 5.8。）

</div>

## 5.8 择一定理

### 5.8.1 利用对偶函数构造弱择一系统

本节将拉格朗日对偶理论用于判断不等式和等式系统

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad h_i(x)=0,\quad i=1,\ldots,p\tag{5.72}
$$

是否可行。假设不等式系统 (5.72) 的定义域 $\mathcal{D}=\bigcap_{i=1}^m\operatorname{\mathbf{dom}}f_i\cap\bigcap_{i=1}^p\operatorname{\mathbf{dom}}h_i$ 非空。可以把 (5.72) 看成目标函数为 $f_0=0$ 的标准问题 (5.1)，即

$$
\begin{array}{ll}
\text{最小化} & 0\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p.
\end{array}\tag{5.73}
$$

这个问题的最优值为

$$
p^\star=\begin{cases}0&\text{(5.72) 可行}\\\infty&\text{(5.72) 不可行，}\end{cases}\tag{5.74}
$$

因此，求解优化问题 (5.73) 与求解不等式系统 (5.72) 是一回事。

#### 对偶函数

为不等式系统 (5.72) 定义对应的对偶函数

$$
g(\lambda,\nu)=\inf_{x\in\mathcal{D}}\left(\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\nu_i h_i(x)\right),
$$

<!-- pdf-page: 273 -->

它与优化问题 (5.73) 的对偶函数相同。由于 $f_0=0$，对偶函数关于 $(\lambda,\nu)$ 正齐次：对于 $\alpha>0$，$g(\alpha\lambda,\alpha\nu)=\alpha g(\lambda,\nu)$。与 (5.73) 对应的对偶问题是在 $\lambda\succeq0$ 的约束下最大化 $g(\lambda,\nu)$。由于 $g$ 是齐次的，这个对偶问题的最优值为

$$
d^\star=\begin{cases}\infty&\lambda\succeq0,\ g(\lambda,\nu)>0\text{ 可行}\\0&\lambda\succeq0,\ g(\lambda,\nu)>0\text{ 不可行。}\end{cases}\tag{5.75}
$$

弱对偶性告诉我们 $d^\star\leq p^\star$。将这个事实与 (5.74)、(5.75) 结合，得到如下结论：如果不等式系统

$$
\lambda\succeq0,\qquad g(\lambda,\nu)>0\tag{5.76}
$$

可行（这意味着 $d^\star=\infty$），那么不等式系统 (5.72) 不可行（因为此时 $p^\star=\infty$）。事实上，可以把不等式 (5.76) 的任意解 $(\lambda,\nu)$ 解释为系统 (5.72) 不可行的一个证明或证书。

也可以从原系统可行性的角度重述这个蕴含关系：如果原不等式系统 (5.72) 可行，那么不等式系统 (5.76) 必定不可行。可以把满足 (5.72) 的 $x$ 解释为证明不等式系统 (5.76) 不可行的证书。

如果两个不等式（和等式）系统中至多有一个可行，就称它们为**弱择一系统**（weak alternatives）。因此，系统 (5.72) 和 (5.76) 是弱择一系统。无论不等式 (5.72) 是否为凸的（即 $f_i$ 为凸函数、$h_i$ 为仿射函数），这一点都成立；而且，其择一不等式系统 (5.76) 总是凸的（即 $g$ 为凹函数，约束 $\lambda_i\geq0$ 为凸约束）。

#### 严格不等式

也可以研究严格不等式系统

$$
f_i(x)<0,\quad i=1,\ldots,m,\qquad h_i(x)=0,\quad i=1,\ldots,p\tag{5.77}
$$

的可行性。沿用非严格不等式系统中 $g$ 的定义，得到择一不等式系统

$$
\lambda\succeq0,\qquad\lambda\neq0,\qquad g(\lambda,\nu)\geq0.\tag{5.78}
$$

可以直接证明 (5.77) 和 (5.78) 是弱择一系统。假设存在 $\widetilde x$ 满足 $f_i(\widetilde x)<0$、$h_i(\widetilde x)=0$。那么，对于任意 $\lambda\succeq0$、$\lambda\neq0$ 和任意 $\nu$，都有

$$
\lambda_1 f_1(\widetilde x)+\cdots+\lambda_m f_m(\widetilde x)+\nu_1h_1(\widetilde x)+\cdots+\nu_p h_p(\widetilde x)<0.
$$

因此

$$
\begin{aligned}
g(\lambda,\nu)&=\inf_{x\in\mathcal{D}}\left(\sum_{i=1}^m\lambda_i f_i(x)+\sum_{i=1}^p\nu_i h_i(x)\right)\\
&\leq\sum_{i=1}^m\lambda_i f_i(\widetilde x)+\sum_{i=1}^p\nu_i h_i(\widetilde x)\\
&<0.
\end{aligned}
$$

<!-- pdf-page: 274 -->

所以，(5.77) 可行意味着不存在满足 (5.78) 的 $(\lambda,\nu)$。

因此，给出系统 (5.78) 的一个解，就能证明 (5.77) 不可行；给出系统 (5.77) 的一个解，就能证明 (5.78) 不可行。

### 5.8.2 强择一系统

当原不等式系统是凸的，即 $f_i$ 为凸函数、$h_i$ 为仿射函数，并且某种约束资格条件成立时，上面描述的各对弱择一系统就是**强择一系统**（strong alternatives），这意味着两者中恰好有一个成立。换言之，每一个不等式系统可行，当且仅当另一个不可行。

本节假设 $f_i$ 为凸函数，$h_i$ 为仿射函数，因此不等式系统 (5.72) 可以表示为

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad Ax=b,
$$

其中 $A\in\mathbf{R}^{p\times n}$。

#### 严格不等式

首先研究严格不等式系统

$$
f_i(x)<0,\quad i=1,\ldots,m,\qquad Ax=b,\tag{5.79}
$$

以及它的择一系统

$$
\lambda\succeq0,\qquad\lambda\neq0,\qquad g(\lambda,\nu)\geq0.\tag{5.80}
$$

需要一个技术条件：存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$ 满足 $Ax=b$。也就是说，不仅假设线性等式约束相容，还要求它们在 $\operatorname{\mathbf{relint}}\mathcal{D}$ 中有解。（通常 $\mathcal{D}=\mathbf{R}^n$，此时只要等式约束相容，这个条件就成立。）在此条件下，不等式系统 (5.79) 和 (5.80) 中恰好有一个可行。换言之，(5.79) 和 (5.80) 是强择一系统。

通过考虑相关的优化问题

$$
\begin{array}{ll}
\text{最小化} & s\\
\text{约束条件} & f_i(x)-s\leq0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}\tag{5.81}
$$

来证明这个结果。这个问题的变量为 $x,s$，定义域为 $\mathcal{D}\times\mathbf{R}$。其最优值 $p^\star$ 为负，当且仅当严格不等式系统 (5.79) 存在解。

问题 (5.81) 的拉格朗日对偶函数为

$$
\inf_{x\in\mathcal{D},\ s}\left(s+\sum_{i=1}^m\lambda_i(f_i(x)-s)+\nu^T(Ax-b)\right)=\begin{cases}g(\lambda,\nu)&\mathbf{1}^T\lambda=1\\-\infty&\text{其他情形。}\end{cases}
$$

<!-- pdf-page: 275 -->

因此，(5.81) 的对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & g(\lambda,\nu)\\
\text{约束条件} & \lambda\succeq0,\quad\mathbf{1}^T\lambda=1.
\end{array}
$$

现在注意，问题 (5.81) 满足 Slater 条件。根据假设，存在 $\widetilde x\in\operatorname{\mathbf{relint}}\mathcal{D}$ 满足 $A\widetilde x=b$。任取 $\widetilde s>\max_i f_i(\widetilde x)$，就得到 (5.81) 的一个严格可行点 $(\widetilde x,\widetilde s)$。因此，$d^\star=p^\star$，并且对偶最优值 $d^\star$ 能够达到。换言之，存在 $(\lambda^\star,\nu^\star)$ 使得

$$
g(\lambda^\star,\nu^\star)=p^\star,\qquad\lambda^\star\succeq0,\qquad\mathbf{1}^T\lambda^\star=1.\tag{5.82}
$$

现在假设严格不等式系统 (5.79) 不可行，这意味着 $p^\star\geq0$。那么 (5.82) 中的 $(\lambda^\star,\nu^\star)$ 就满足择一不等式系统 (5.80)。类似地，如果择一不等式系统 (5.80) 可行，那么 $d^\star=p^\star\geq0$，这说明严格不等式系统 (5.79) 不可行。因此，不等式系统 (5.79) 和 (5.80) 是强择一系统；每一个可行，当且仅当另一个不可行。

#### 非严格不等式

现在考虑非严格不等式系统

$$
f_i(x)\leq0,\quad i=1,\ldots,m,\qquad Ax=b,\tag{5.83}
$$

及其择一系统

$$
\lambda\succeq0,\qquad g(\lambda,\nu)>0.\tag{5.84}
$$

我们将证明，只要以下条件成立，它们就是强择一系统：存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$ 满足 $Ax=b$，且 (5.81) 的最优值 $p^\star$ 能够达到。例如，如果 $\mathcal{D}=\mathbf{R}^n$，且当 $x\to\infty$ 时有 $\max_i f_i(x)\to\infty$，这些条件就成立。在这些假设下，与严格不等式情形一样，有 $p^\star=d^\star$，且原、对偶最优值都能够达到。现在假设非严格不等式系统 (5.83) 不可行，这意味着 $p^\star>0$。（这里用到了原最优值能够达到的假设。）那么，(5.82) 中的 $(\lambda^\star,\nu^\star)$ 就满足择一不等式系统 (5.84)。所以，不等式系统 (5.83) 和 (5.84) 是强择一系统；每一个可行，当且仅当另一个不可行。

### 5.8.3 例子

#### 线性不等式

考虑线性不等式系统 $Ax\preceq b$。对偶函数为

$$
g(\lambda)=\inf_x\lambda^T(Ax-b)=\begin{cases}-b^T\lambda&A^T\lambda=0\\-\infty&\text{其他情形。}\end{cases}
$$

因此，择一不等式系统为

$$
\lambda\succeq0,\qquad A^T\lambda=0,\qquad b^T\lambda<0.
$$

<!-- pdf-page: 276 -->

事实上，它们是强择一系统，因为相关问题 (5.81) 的最优值只要不是下方无界，就能够达到。

现在考虑严格线性不等式系统 $Ax\prec b$，它的强择一系统为

$$
\lambda\succeq0,\qquad\lambda\neq0,\qquad A^T\lambda=0,\qquad b^T\lambda\leq0.
$$

事实上，我们已经在 §2.5.1 遇到并证明过这个结果；见 (2.17) 和 (2.18)（原书第 50 页）。

#### 椭球的交集

考虑 $m$ 个椭球，表示为

$$
\mathcal{E}_i=\{x\mid f_i(x)\leq0\},
$$

其中 $f_i(x)=x^TA_ix+2b_i^Tx+c_i$，$i=1,\ldots,m$，$A_i\in\mathbf{S}_{++}^n$。我们想知道，这些椭球的交集在什么条件下内部非空。这等价于判断下面这组严格二次不等式是否可行：

$$
f_i(x)=x^TA_ix+2b_i^Tx+c_i<0,\qquad i=1,\ldots,m.\tag{5.85}
$$

对偶函数 $g$ 为

$$
\begin{aligned}
g(\lambda)&=\inf_x\bigl(x^TA(\lambda)x+2b(\lambda)^Tx+c(\lambda)\bigr)\\
&=\begin{cases}-b(\lambda)^TA(\lambda)^\dagger b(\lambda)+c(\lambda)&A(\lambda)\succeq0,\quad b(\lambda)\in\mathcal{R}(A(\lambda))\\-\infty&\text{其他情形，}\end{cases}
\end{aligned}
$$

其中

$$
A(\lambda)=\sum_{i=1}^m\lambda_i A_i,\qquad b(\lambda)=\sum_{i=1}^m\lambda_i b_i,\qquad c(\lambda)=\sum_{i=1}^m\lambda_i c_i.
$$

注意，当 $\lambda\succeq0$ 且 $\lambda\neq0$ 时，有 $A(\lambda)\succ0$，所以对偶函数的表达式可以简化为

$$
g(\lambda)=-b(\lambda)^TA(\lambda)^{-1}b(\lambda)+c(\lambda).
$$

因此，系统 (5.85) 的强择一系统为

$$
\lambda\succeq0,\qquad\lambda\neq0,\qquad-b(\lambda)^TA(\lambda)^{-1}b(\lambda)+c(\lambda)\geq0.\tag{5.86}
$$

这对强择一系统有一个简单的几何解释。对于任意非零的 $\lambda\succeq0$，椭球（也可能为空）

$$
\mathcal{E}_\lambda=\{x\mid x^TA(\lambda)x+2b(\lambda)^Tx+c(\lambda)\leq0\}
$$

包含 $\mathcal{E}_1\cap\cdots\cap\mathcal{E}_m$，因为 $f_i(x)\leq0$ 蕴含 $\sum_{i=1}^m\lambda_i f_i(x)\leq0$。而 $\mathcal{E}_\lambda$ 的内部为空，当且仅当

$$
\inf_x\bigl(x^TA(\lambda)x+2b(\lambda)^Tx+c(\lambda)\bigr)=-b(\lambda)^TA(\lambda)^{-1}b(\lambda)+c(\lambda)\geq0.
$$

因此，择一系统 (5.86) 意味着 $\mathcal{E}_\lambda$ 的内部为空。

弱对偶性显然成立：如果 (5.86) 成立，那么 $\mathcal{E}_\lambda$ 包含交集 $\mathcal{E}_1\cap\cdots\cap\mathcal{E}_m$，并且内部为空，所以该交集自然也内部为空。它们是强择一系统这一事实，表达了下面这个并不显然的结论：如果交集 $\mathcal{E}_1\cap\cdots\cap\mathcal{E}_m$ 的内部为空，那么就能构造一个包含该交集、且内部为空的椭球 $\mathcal{E}_\lambda$。

<!-- pdf-page: 277 -->

#### Farkas 引理

本节介绍一对涉及严格与非严格线性不等式混合系统的强择一系统，这一结论称为 **Farkas 引理**：不等式系统

$$
Ax\preceq0,\qquad c^Tx<0,\tag{5.87}
$$

其中 $A\in\mathbf{R}^{m\times n}$、$c\in\mathbf{R}^n$，与等式和不等式系统

$$
A^Ty+c=0,\qquad y\succeq0,\tag{5.88}
$$

是强择一系统。

利用 LP 对偶性，可以直接证明 Farkas 引理。考虑 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq0,
\end{array}\tag{5.89}
$$

及其对偶

$$
\begin{array}{ll}
\text{最大化} & 0\\
\text{约束条件} & A^Ty+c=0\\
& y\succeq0.
\end{array}\tag{5.90}
$$

原 LP (5.89) 是齐次的，因此，当 (5.87) 不可行时，其最优值为 0；当 (5.87) 可行时，其最优值为 $-\infty$。对偶 LP (5.90) 在 (5.88) 可行时最优值为 0，在 (5.88) 不可行时最优值为 $-\infty$。

由于 $x=0$ 是 (5.89) 的可行点，可以排除 LP 中强对偶性可能不成立的唯一一种情形，因此必定有 $p^\star=d^\star$。结合上述分析，就证明了 (5.87) 和 (5.88) 是强择一系统。

<div class="example" markdown="1">

**例 5.10 价格的无套利界。** 考虑 $n$ 项资产，它们在投资期开始时的价格分别为 $p_1,\ldots,p_n$，在投资期结束时的价值为 $v_1,\ldots,v_n$。如果 $x_1,\ldots,x_n$ 表示各项资产的初始投资头寸（其中 $x_j<0$ 表示对资产 $j$ 持有空头头寸），那么初始投资的成本为 $p^Tx$，投资的最终价值为 $v^Tx$。

资产在投资期结束时的价值 $v$ 是不确定的。我们假设只有 $m$ 种可能情景或结果。如果结果 $i$ 发生，资产的最终价值为 $v^{(i)}$，因此投资的总价值为 $(v^{(i)})^Tx$。

如果存在投资向量 $x$ 满足 $p^Tx<0$，并且在所有可能情景下最终价值都非负，即 $(v^{(i)})^Tx\geq0$，$i=1,\ldots,m$，就称存在**套利**（arbitrage）。条件 $p^Tx<0$ 表示，接受这一投资组合时你会收到一笔钱；条件 $(v^{(i)})^Tx\geq0$，$i=1,\ldots,m$，表示无论出现哪一种结果，最终价值都非负，因此套利对应于一种保证赚钱的投资策略。通常假设价格和价值满足无套利条件。这意味着不等式系统

$$
Vx\succeq0,\qquad p^Tx<0
$$

不可行，其中 $V_{ij}=v_j^{(i)}$。

利用 Farkas 引理可知，不存在套利，当且仅当存在 $y$ 使得

$$
-V^Ty+p=0,\qquad y\succeq0.
$$

<!-- pdf-page: 278 -->

利用这种对无套利价格和价值的刻画，可以求解几个有趣的问题。

例如，假设价值 $V$ 已知，除最后一个价格 $p_n$ 外，其余价格也都已知。与无套利假设一致的价格 $p_n$ 构成一个区间，可以通过求解两个 LP 找到这个区间。LP

$$
\begin{array}{ll}
\text{最小化} & p_n\\
\text{约束条件} & V^Ty=p,\quad y\succeq0,
\end{array}
$$

的变量为 $p_n$ 和 $y$，其最优值给出资产 $n$ 可能的最低无套利价格。将最小化改为最大化，求解同一个 LP，就得到资产 $n$ 可能的最高价格。如果这两个值相等，即无套利假设唯一确定了资产 $n$ 的价格，就称市场是**完备的**（complete）。例子见习题 5.38。

这种方法可以用于求取衍生品或期权价格的界：它们基于其他标的资产的最终价值，也就是说，资产 $n$ 的价值或支付额是其他资产价值的函数。

</div>

## 5.9 广义不等式

本节考察如何将拉格朗日对偶性推广到含有广义不等式约束的问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}\tag{5.91}
$$

其中 $K_i\subseteq\mathbf{R}^{k_i}$ 是正常锥。暂时不假设问题 (5.91) 是凸问题。我们假设 (5.91) 的定义域 $\mathcal{D}=\bigcap_{i=0}^m\operatorname{\mathbf{dom}}f_i\cap\bigcap_{i=1}^p\operatorname{\mathbf{dom}}h_i$ 非空。

### 5.9.1 拉格朗日对偶

为 (5.91) 中的每个广义不等式 $f_i(x)\preceq_{K_i}0$ 配置一个拉格朗日乘子向量 $\lambda_i\in\mathbf{R}^{k_i}$，并将相应的拉格朗日函数定义为

$$
L(x,\lambda,\nu)=f_0(x)+\lambda_1^Tf_1(x)+\cdots+\lambda_m^Tf_m(x)+\nu_1h_1(x)+\cdots+\nu_p h_p(x),
$$

其中 $\lambda=(\lambda_1,\ldots,\lambda_m)$，$\nu=(\nu_1,\ldots,\nu_p)$。对偶函数的定义与标量不等式问题中的定义完全相同：

$$
g(\lambda,\nu)=\inf_{x\in\mathcal{D}}L(x,\lambda,\nu)=\inf_{x\in\mathcal{D}}\left(f_0(x)+\sum_{i=1}^m\lambda_i^Tf_i(x)+\sum_{i=1}^p\nu_i h_i(x)\right).
$$

由于拉格朗日函数关于对偶变量 $(\lambda,\nu)$ 是仿射的，而对偶函数是拉格朗日函数的逐点下确界，所以对偶函数是凹函数。

<!-- pdf-page: 279 -->

与标量不等式问题一样，对偶函数给出原问题 (5.91) 最优值 $p^\star$ 的下界。对于标量不等式问题，我们要求 $\lambda_i\geq0$。这里，对偶变量的非负性要求由条件

$$
\lambda_i\succeq_{K_i^*}0,\qquad i=1,\ldots,m,
$$

替代，其中 $K_i^*$ 表示 $K_i$ 的对偶锥。换言之，与不等式对应的拉格朗日乘子必须在对偶意义下非负。

由对偶锥的定义可以立即得到弱对偶性。如果 $\lambda_i\succeq_{K_i^*}0$ 且 $f_i(\widetilde x)\preceq_{K_i}0$，那么 $\lambda_i^Tf_i(\widetilde x)\leq0$。因此，对于任意原可行点 $\widetilde x$ 以及任意 $\lambda_i\succeq_{K_i^*}0$，都有

$$
f_0(\widetilde x)+\sum_{i=1}^m\lambda_i^Tf_i(\widetilde x)+\sum_{i=1}^p\nu_i h_i(\widetilde x)\leq f_0(\widetilde x).
$$

对 $\widetilde x$ 取下确界，得到 $g(\lambda,\nu)\leq p^\star$。

拉格朗日对偶优化问题为

$$
\begin{array}{ll}
\text{最大化} & g(\lambda,\nu)\\
\text{约束条件} & \lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m.
\end{array}\tag{5.92}
$$

无论原问题 (5.91) 是否为凸问题，弱对偶性总是成立，即 $d^\star\leq p^\star$，其中 $d^\star$ 表示对偶问题 (5.92) 的最优值。

#### Slater 条件与强对偶性

正如可以预料的，当原问题为凸问题，且满足适当的约束资格条件时，强对偶性（$d^\star=p^\star$）成立。例如，对于问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}
$$

其中 $f_0$ 为凸函数，$f_i$ 为 $K_i$-凸函数，Slater 条件的推广形式为：存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$，使得 $Ax=b$ 且 $f_i(x)\prec_{K_i}0$，$i=1,\ldots,m$。这个条件保证强对偶性成立（并保证对偶最优值能够达到）。

<div class="example" markdown="1">

**例 5.11 半定规划的拉格朗日对偶。** 考虑不等式形式的半定规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & x_1F_1+\cdots+x_nF_n+G\preceq0,
\end{array}\tag{5.93}
$$

其中 $F_1,\ldots,F_n,G\in\mathbf{S}^k$。（这里 $f_1$ 是仿射函数，$K_1$ 是半正定锥 $\mathbf{S}_+^k$。）

为这个约束配置对偶变量或乘子 $Z\in\mathbf{S}^k$，则拉格朗日函数为

$$
\begin{aligned}
L(x,Z)&=c^Tx+\operatorname{\mathbf{tr}}\bigl((x_1F_1+\cdots+x_nF_n+G)Z\bigr)\\
&=x_1(c_1+\operatorname{\mathbf{tr}}(F_1Z))+\cdots+x_n(c_n+\operatorname{\mathbf{tr}}(F_nZ))+\operatorname{\mathbf{tr}}(GZ),
\end{aligned}
$$

<!-- pdf-page: 280 -->

它关于 $x$ 是仿射的。对偶函数为

$$
g(Z)=\inf_x L(x,Z)=\begin{cases}\operatorname{\mathbf{tr}}(GZ)&\operatorname{\mathbf{tr}}(F_iZ)+c_i=0,\quad i=1,\ldots,n\\-\infty&\text{其他情形。}\end{cases}
$$

因此，对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & \operatorname{\mathbf{tr}}(GZ)\\
\text{约束条件} & \operatorname{\mathbf{tr}}(F_iZ)+c_i=0,\quad i=1,\ldots,n\\
& Z\succeq0.
\end{array}
$$

（这里用到了 $\mathbf{S}_+^k$ 是自对偶锥这一事实，即 $(\mathbf{S}_+^k)^*=\mathbf{S}_+^k$；见 §2.6。）

如果半定规划 (5.93) 严格可行，即存在 $x$ 满足

$$
x_1F_1+\cdots+x_nF_n+G\prec0,
$$

那么强对偶性成立。

</div>

<div class="example" markdown="1">

**例 5.12 标准形式锥规划的拉格朗日对偶。** 考虑锥规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax=b\\
& x\succeq_K0,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$，$b\in\mathbf{R}^m$，$K\subseteq\mathbf{R}^n$ 是正常锥。为等式约束配置乘子 $\nu\in\mathbf{R}^m$，为非负性约束配置乘子 $\lambda\in\mathbf{R}^n$。拉格朗日函数为

$$
L(x,\lambda,\nu)=c^Tx-\lambda^Tx+\nu^T(Ax-b),
$$

因此，对偶函数为

$$
g(\lambda,\nu)=\inf_x L(x,\lambda,\nu)=\begin{cases}-b^T\nu&A^T\nu-\lambda+c=0\\-\infty&\text{其他情形。}\end{cases}
$$

对偶问题可以表示为

$$
\begin{array}{ll}
\text{最大化} & -b^T\nu\\
\text{约束条件} & A^T\nu+c=\lambda\\
& \lambda\succeq_{K^*}0.
\end{array}
$$

消去 $\lambda$，并定义 $y=-\nu$，可以将这个问题简化为

$$
\begin{array}{ll}
\text{最大化} & b^Ty\\
\text{约束条件} & A^Ty\preceq_{K^*}c,
\end{array}
$$

这是一个不等式形式的锥规划，涉及对偶广义不等式。如果 Slater 条件成立，即存在 $x\succ_K0$ 满足 $Ax=b$，那么强对偶性成立。

</div>

### 5.9.2 最优性条件

§5.5 中的最优性条件很容易推广到含广义不等式的问题。首先推导互补松弛条件。

<!-- pdf-page: 281 -->

#### 互补松弛性

假设原最优值和对偶最优值相等，并且在最优点 $x^\star,\lambda^\star,\nu^\star$ 处达到。与 §5.5.2 一样，由等式 $f_0(x^\star)=g(\lambda^\star,\nu^\star)$ 和 $g$ 的定义，可以直接得到互补松弛条件。我们有

$$
\begin{aligned}
f_0(x^\star)&=g(\lambda^\star,\nu^\star)\\
&\leq f_0(x^\star)+\sum_{i=1}^m(\lambda_i^\star)^Tf_i(x^\star)+\sum_{i=1}^p\nu_i^\star h_i(x^\star)\\
&\leq f_0(x^\star),
\end{aligned}
$$

因此可知，$x^\star$ 使 $L(x,\lambda^\star,\nu^\star)$ 取得最小值，而且第二行的两个和式都为零。由于第二个和式为零（因为 $x^\star$ 满足等式约束），有 $\sum_{i=1}^m(\lambda_i^\star)^Tf_i(x^\star)=0$。又因为该和式中的每一项都非正，可知

$$
(\lambda_i^\star)^Tf_i(x^\star)=0,\qquad i=1,\ldots,m,\tag{5.94}
$$

这是互补松弛条件 (5.48) 的推广。由 (5.94) 可得

$$
\lambda_i^\star\succ_{K_i^*}0\quad\Longrightarrow\quad f_i(x^\star)=0,\qquad f_i(x^\star)\prec_{K_i}0\quad\Longrightarrow\quad\lambda_i^\star=0.
$$

但是，与标量不等式问题不同，$\lambda_i^\star\neq0$ 且 $f_i(x^\star)\neq0$ 时，仍有可能满足 (5.94)。

#### KKT 条件

现在增加假设：函数 $f_i,h_i$ 可微，并将 §5.5.3 的 KKT 条件推广到含广义不等式的问题。由于 $x^\star$ 使 $L(x,\lambda^\star,\nu^\star)$ 取得最小值，它关于 $x$ 的梯度在 $x^\star$ 处为零：

$$
\nabla f_0(x^\star)+\sum_{i=1}^m Df_i(x^\star)^T\lambda_i^\star+\sum_{i=1}^p\nu_i^\star\nabla h_i(x^\star)=0,
$$

其中 $Df_i(x^\star)\in\mathbf{R}^{k_i\times n}$ 是 $f_i$ 在 $x^\star$ 处的导数（见 §A.4.1）。因此，如果强对偶性成立，那么任意原最优点 $x^\star$ 和任意对偶最优点 $(\lambda^\star,\nu^\star)$ 必须满足最优性条件（或 KKT 条件）

$$
\begin{aligned}
f_i(x^\star)&\preceq_{K_i}0,\quad i=1,\ldots,m\\
h_i(x^\star)&=0,\quad i=1,\ldots,p\\
\lambda_i^\star&\succeq_{K_i^*}0,\quad i=1,\ldots,m\\
(\lambda_i^\star)^Tf_i(x^\star)&=0,\quad i=1,\ldots,m\\
\nabla f_0(x^\star)+\sum_{i=1}^m Df_i(x^\star)^T\lambda_i^\star+\sum_{i=1}^p\nu_i^\star\nabla h_i(x^\star)&=0.
\end{aligned}\tag{5.95}
$$

如果原问题为凸问题，反过来也成立，即条件 (5.95) 是 $x^\star$、$(\lambda^\star,\nu^\star)$ 最优的充分条件。

<!-- pdf-page: 282 -->

### 5.9.3 扰动与灵敏度分析

§5.6 的结果可以推广到含广义不等式的问题。考虑相应的扰动问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\preceq_{K_i}u_i,\quad i=1,\ldots,m\\
& h_i(x)=v_i,\quad i=1,\ldots,p,
\end{array}
$$

其中 $u_i\in\mathbf{R}^{k_i}$，$v\in\mathbf{R}^p$。定义 $p^\star(u,v)$ 为扰动问题的最优值。与标量不等式情形一样，当原问题为凸问题时，$p^\star$ 是凸函数。

现在设 $(\lambda^\star,\nu^\star)$ 是原来未扰动问题的对偶最优点，并假设该问题的对偶间隙为零。那么，对于所有 $u$ 和 $v$，都有

$$
p^\star(u,v)\geq p^\star-\sum_{i=1}^m(\lambda_i^\star)^Tu_i-(\nu^\star)^Tv,
$$

这是全局灵敏度不等式 (5.57) 的对应形式。局部灵敏度结果也成立：如果 $p^\star(u,v)$ 在 $u=0$、$v=0$ 处可微，那么最优对偶变量 $\lambda_i^\star$ 满足

$$
\lambda_i^\star=-\nabla_{u_i}p^\star(0,0),
$$

这是 (5.58) 的对应形式。

<div class="example" markdown="1">

**例 5.13 不等式形式的半定规划。** 与例 5.11 一样，考虑不等式形式的半定规划。原问题为

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & F(x)=x_1F_1+\cdots+x_nF_n+G\preceq0,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$（且 $F_1,\ldots,F_n,G\in\mathbf{S}^k$）；对偶问题为

$$
\begin{array}{ll}
\text{最大化} & \operatorname{\mathbf{tr}}(GZ)\\
\text{约束条件} & \operatorname{\mathbf{tr}}(F_iZ)+c_i=0,\quad i=1,\ldots,n\\
& Z\succeq0,
\end{array}
$$

其中变量为 $Z\in\mathbf{S}^k$。

假设 $x^\star$ 和 $Z^\star$ 分别原最优和对偶最优，且对偶间隙为零。互补松弛条件为 $\operatorname{\mathbf{tr}}(F(x^\star)Z^\star)=0$。由于 $F(x^\star)\preceq0$ 且 $Z^\star\succeq0$，可知 $F(x^\star)Z^\star=0$。因此，互补松弛条件可以表示为

$$
\mathcal{R}(F(x^\star))\perp\mathcal{R}(Z^\star),
$$

即原矩阵与对偶矩阵的值域相互正交。

用 $p^\star(U)$ 表示扰动后的 SDP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & F(x)=x_1F_1+\cdots+x_nF_n+G\preceq U
\end{array}
$$

的最优值。

<!-- pdf-page: 283 -->

那么，对于所有 $U$，都有 $p^\star(U)\geq p^\star-\operatorname{\mathbf{tr}}(Z^\star U)$。如果 $p^\star(U)$ 在 $U=0$ 处可微，则有

$$
\nabla p^\star(0)=-Z^\star.
$$

这意味着，当 $U$ 很小时，扰动后 SDP 的最优值非常接近（下界）$p^\star-\operatorname{\mathbf{tr}}(Z^\star U)$。

</div>

### 5.9.4 择一定理

对于广义不等式和等式系统

$$
f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m,\qquad h_i(x)=0,\quad i=1,\ldots,p,\tag{5.96}
$$

其中 $K_i\subseteq\mathbf{R}^{k_i}$ 为正常锥，也可以推导择一定理。我们还将考虑含严格不等式的系统

$$
f_i(x)\prec_{K_i}0,\quad i=1,\ldots,m,\qquad h_i(x)=0,\quad i=1,\ldots,p.\tag{5.97}
$$

假设 $\mathcal{D}=\bigcap_{i=0}^m\operatorname{\mathbf{dom}}f_i\cap\bigcap_{i=1}^p\operatorname{\mathbf{dom}}h_i$ 非空。

#### 弱择一系统

为系统 (5.96) 和 (5.97) 定义对应的对偶函数

$$
g(\lambda,\nu)=\inf_{x\in\mathcal{D}}\left(\sum_{i=1}^m\lambda_i^Tf_i(x)+\sum_{i=1}^p\nu_i h_i(x)\right),
$$

其中 $\lambda=(\lambda_1,\ldots,\lambda_m)$，$\lambda_i\in\mathbf{R}^{k_i}$，且 $\nu\in\mathbf{R}^p$。与 (5.76) 类似，我们断言

$$
\lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m,\qquad g(\lambda,\nu)>0\tag{5.98}
$$

与系统 (5.96) 构成弱择一系统。为验证这一点，假设存在 $x$ 满足 (5.96)，同时存在 $(\lambda,\nu)$ 满足 (5.98)。那么就会得到矛盾：

$$
0<g(\lambda,\nu)\leq\lambda_1^Tf_1(x)+\cdots+\lambda_m^Tf_m(x)+\nu_1h_1(x)+\cdots+\nu_p h_p(x)\leq0.
$$

因此，(5.96) 和 (5.98) 两个系统中至少有一个不可行，即它们是弱择一系统。

类似地，可以证明 (5.97) 与系统

$$
\lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m,\qquad\lambda\neq0,\qquad g(\lambda,\nu)\geq0
$$

构成一对弱择一系统。

#### 强择一系统

现在假设函数 $f_i$ 为 $K_i$-凸函数，而函数 $h_i$ 为仿射函数。首先考虑含严格不等式的系统

$$
f_i(x)\prec_{K_i}0,\quad i=1,\ldots,m,\qquad Ax=b,\tag{5.99}
$$

<!-- pdf-page: 284 -->

及其择一系统

$$
\lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m,\qquad\lambda\neq0,\qquad g(\lambda,\nu)\geq0.\tag{5.100}
$$

我们已经看到，(5.99) 和 (5.100) 是弱择一系统。只要下面的约束资格条件成立，它们也是强择一系统：存在 $\widetilde x\in\operatorname{\mathbf{relint}}\mathcal{D}$ 满足 $A\widetilde x=b$。为证明这一点，选取一组向量 $e_i\succ_{K_i}0$，并考虑问题

$$
\begin{array}{ll}
\text{最小化} & s\\
\text{约束条件} & f_i(x)\preceq_{K_i}se_i,\quad i=1,\ldots,m\\
& Ax=b,
\end{array}\tag{5.101}
$$

其中变量为 $x$ 和 $s\in\mathbf{R}$。Slater 条件成立，因为只要 $\widetilde s$ 足够大，$(\widetilde x,\widetilde s)$ 就满足严格不等式 $f_i(\widetilde x)\prec_{K_i}\widetilde s e_i$。

(5.101) 的对偶为

$$
\begin{array}{ll}
\text{最大化} & g(\lambda,\nu)\\
\text{约束条件} & \lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m\\
& \sum_{i=1}^m e_i^T\lambda_i=1,
\end{array}\tag{5.102}
$$

其中变量为 $\lambda=(\lambda_1,\ldots,\lambda_m)$ 和 $\nu$。

现在假设系统 (5.99) 不可行。那么 (5.101) 的最优值非负。由于满足 Slater 条件，强对偶性成立，且对偶最优值能够达到。因此，存在 $(\widetilde\lambda,\widetilde\nu)$ 满足 (5.102) 的约束，并满足 $g(\widetilde\lambda,\widetilde\nu)\geq0$，即系统 (5.100) 有解。

正如在标量不等式情形中指出的，存在 $x\in\operatorname{\mathbf{relint}}\mathcal{D}$ 满足 $Ax=b$，并不足以保证非严格不等式系统

$$
f_i(x)\preceq_{K_i}0,\quad i=1,\ldots,m,\qquad Ax=b
$$

及其择一系统

$$
\lambda_i\succeq_{K_i^*}0,\quad i=1,\ldots,m,\qquad g(\lambda,\nu)>0
$$

是强择一系统。还需要一个附加条件，例如 (5.101) 的最优值能够达到。

<div class="example" markdown="1">

**例 5.14 线性矩阵不等式的可行性。** 下面两个系统是强择一系统：

$$
F(x)=x_1F_1+\cdots+x_nF_n+G\prec0,
$$

其中 $F_i,G\in\mathbf{S}^k$；以及

$$
Z\succeq0,\qquad Z\neq0,\qquad\operatorname{\mathbf{tr}}(GZ)\geq0,\qquad\operatorname{\mathbf{tr}}(F_iZ)=0,\quad i=1,\ldots,n,
$$

其中 $Z\in\mathbf{S}^k$。取 $K$ 为半正定锥 $\mathbf{S}_+^k$，并令

$$
g(Z)=\inf_x\bigl(\operatorname{\mathbf{tr}}(F(x)Z)\bigr)=\begin{cases}\operatorname{\mathbf{tr}}(GZ)&\operatorname{\mathbf{tr}}(F_iZ)=0,\quad i=1,\ldots,n\\-\infty&\text{其他情形，}\end{cases}
$$

就能由一般结果得到这个结论。

<!-- pdf-page: 285 -->

非严格不等式的情形稍微复杂一些；要得到强择一系统，需要对矩阵 $F_i$ 增加一个假设。其中一个这样的条件是

$$
\sum_{i=1}^n v_iF_i\succeq0\quad\Longrightarrow\quad\sum_{i=1}^n v_iF_i=0.
$$

如果这个条件成立，那么以下两个系统是强择一系统：

$$
F(x)=x_1F_1+\cdots+x_nF_n+G\preceq0
$$

和

$$
Z\succeq0,\qquad\operatorname{\mathbf{tr}}(GZ)>0,\qquad\operatorname{\mathbf{tr}}(F_iZ)=0,\quad i=1,\ldots,n
$$

（见习题 5.44）。

</div>

<!-- pdf-page: 286 -->

## 文献说明

Luenberger [Lue69，第 8 章]、Rockafellar [Roc70，第 VI 部分]、Whittle [Whi71]、Hiriart-Urruty 和 Lemaréchal [HUL93]，以及 Bertsekas、Nedić 和 Ozdaglar [Ber03] 详细介绍了拉格朗日对偶性。这一名称源于 Lagrange 为求解带等式约束的优化问题提出的乘子法；见 Courant 和 Hilbert [CH53，第 IV 章]。

§5.2.5 中矩阵博弈的极大极小结果，早于线性规划对偶性出现。von Neuman 和 Morgenstern [vNM53，第 153 页] 利用一个择一定理证明了这一结果。原书第 227 页的线性规划强对偶性结果，来自 von Neumann [vN63] 以及 Gale、Kuhn 和 Tucker [GKT51]。非凸二次问题 (5.32) 的强对偶性，是非线性优化的信赖域方法文献中的一个基本结果（Nocedal 和 Wright [NW99，第 78 页]）。它还与控制理论中的 S-procedure 有关，后者在附录 §B.1 中讨论。关于如何把 §5.3.2 的强对偶性证明推广到细化的 Slater 条件 (5.27)，见 Rockafellar [Roc70，第 277 页]。

保证鞍点性质 (5.47) 成立的条件，可见 Rockafellar [Roc70，第 VII 部分] 和 Bertsekas、Nedić、Ozdaglar [Ber03，第 2 章]；另见习题 5.25。

KKT 条件以 Karush（其未发表的 1939 年硕士论文在 Kuhn [Kuh76] 中有概述）、Kuhn 和 Tucker [KT51] 的名字命名。John [Joh85] 也推导了相关的最优性条件。例 5.2 中的注水算法在信息论和通信中有应用（Cover 和 Thomas [CT91，第 252 页]）。

Farkas 引理由 Farkas [Far02] 发表。它是线性不等式与等式系统中最著名的择一定理，但还存在许多变体；见 Mangasarian [Man94，§2.4]。Bertsimas 和 Tsitsiklis [BT97，第 167 页] 以及 Ross [Ros99] 讨论了 Farkas 引理在资产定价中的应用（例 5.10）。

将拉格朗日对偶性推广到广义不等式问题的结果，见 Isii [Isi64]、Luenberger [Lue69，第 8 章]、Berman [Ber73] 和 Rockafellar [Roc89，第 47 页]。Nesterov 和 Nemirovski [NN94，§4.2] 以及 Ben-Tal 和 Nemirovski [BTN01，第 2 讲] 在锥规划的背景下讨论了这一推广。Ben-Israel [BI69]、Berman 和 Ben-Israel [BBI71]，以及 Craven 和 Kohila [CK77] 研究了广义不等式的择一定理。Bellman 和 Fan [BF63]、Wolkowicz [Wol81] 以及 Lasserre [Las95] 给出了 Farkas 引理在线性矩阵不等式上的推广。

<!-- pdf-page: 287 -->

## 习题

### 基本定义

**5.1 一个简单例子。** 考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & x^2+1\\
\text{约束条件} & (x-2)(x-4)\leq0,
\end{array}
$$

其中变量为 $x\in\mathbf{R}$。

- (a) *分析原问题。* 给出可行集、最优值和最优解。

- (b) *拉格朗日函数与对偶函数。* 绘制目标函数 $x^2+1$ 随 $x$ 变化的图像。在同一幅图上标出可行集、最优点和最优值，并对几个正的 $\lambda$ 值，绘制拉格朗日函数 $L(x,\lambda)$ 随 $x$ 变化的图像。验证下界性质（当 $\lambda\geq0$ 时，$p^\star\geq\inf_x L(x,\lambda)$）。推导拉格朗日对偶函数 $g$，并画出其示意图。

- (c) *拉格朗日对偶问题。* 写出对偶问题，验证它是凹函数最大化问题。求对偶最优值和对偶最优解 $\lambda^\star$。强对偶性是否成立？

- (d) *灵敏度分析。* 用 $p^\star(u)$ 表示问题

    $$
    \begin{array}{ll}
    \text{最小化} & x^2+1\\
    \text{约束条件} & (x-2)(x-4)\leq u
    \end{array}
    $$

    的最优值，并把它看作参数 $u$ 的函数。绘制 $p^\star(u)$ 的图像。验证 $dp^\star(0)/du=-\lambda^\star$。

**5.2 无界问题与不可行问题的弱对偶性。** 当 $d^\star=-\infty$ 或 $p^\star=\infty$ 时，弱对偶不等式 $d^\star\leq p^\star$ 显然成立。证明，在另外两种情形下它也成立：如果 $p^\star=-\infty$，那么必定有 $d^\star=-\infty$；如果 $d^\star=\infty$，那么必定有 $p^\star=\infty$。

**5.3 只有一个不等式约束的问题。** 利用共轭函数 $f^*$，表示问题

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & f(x)\leq0
\end{array}
$$

的对偶问题，其中 $c\neq0$。解释为什么你给出的问题是凸问题。这里不假设 $f$ 是凸函数。

### 例子与应用

**5.4 利用松弛问题解释 LP 对偶。** 考虑不等式形式的 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$，$b\in\mathbf{R}^m$。本题给出对偶 LP (5.22) 的一个简单几何解释。

设 $w\in\mathbf{R}_+^m$。如果 $x$ 是 LP 的可行点，即满足 $Ax\preceq b$，那么它也满足不等式

$$
w^TAx\leq w^Tb.
$$

从几何上看，对于任意 $w\succeq0$，半空间 $H_w=\{x\mid w^TAx\leq w^Tb\}$ 都包含 LP 的可行集。因此，在半空间 $H_w$ 上最小化目标函数 $c^Tx$，就得到 $p^\star$ 的一个下界。

<!-- pdf-page: 288 -->

- (a) 推导 $c^Tx$ 在半空间 $H_w$ 上最小值的表达式（它将取决于 $w\succeq0$ 的选择）。

- (b) 将寻找这类最优下界的问题表述为：在 $w\succeq0$ 上最大化所得下界。

- (c) 说明 (a)、(b) 的结果与 (5.22) 给出的 LP 拉格朗日对偶之间的关系。

**5.5 一般 LP 的对偶。** 求 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Gx\preceq h\\
& Ax=b
\end{array}
$$

的对偶函数。给出对偶问题，并将隐式等式约束显式写出。

**5.6 由最小二乘得到 Chebyshev 逼近的下界。** 考虑 Chebyshev 逼近问题，即 $\ell_\infty$ 范数逼近问题

$$
\begin{array}{ll}\text{最小化} & \|Ax-b\|_\infty,\end{array}\tag{5.103}
$$

其中 $A\in\mathbf{R}^{m\times n}$，$\operatorname{\mathbf{rank}}A=n$。用 $x_{\mathrm{ch}}$ 表示一个最优解（可能有多个最优解；$x_{\mathrm{ch}}$ 表示其中一个）。

Chebyshev 问题没有闭式解，但相应的最小二乘问题有闭式解。定义

$$
x_{\mathrm{ls}}=\operatorname{argmin}\|Ax-b\|_2=(A^TA)^{-1}A^Tb.
$$

我们要回答以下问题。假设对于给定的 $A$ 和 $b$，已经算出最小二乘解 $x_{\mathrm{ls}}$（但没有算出 $x_{\mathrm{ch}}$）。对于 Chebyshev 问题，$x_{\mathrm{ls}}$ 距离最优有多远？换言之，$\|Ax_{\mathrm{ls}}-b\|_\infty$ 比 $\|Ax_{\mathrm{ch}}-b\|_\infty$ 大多少？

- (a) 证明下界

    $$
    \|Ax_{\mathrm{ls}}-b\|_\infty\leq\sqrt{m}\,\|Ax_{\mathrm{ch}}-b\|_\infty,
    $$

    利用的事实是：对于所有 $z\in\mathbf{R}^m$，都有

    $$
    \frac1{\sqrt m}\|z\|_2\leq\|z\|_\infty\leq\|z\|_2.
    $$

- (b) 在例 5.6（原书第 254 页）中，我们推导了一般范数逼近问题的一个对偶。将这些结果用于 $\ell_\infty$ 范数（及其对偶范数 $\ell_1$ 范数），可以写出 Chebyshev 逼近问题的如下对偶：

    $$
    \begin{array}{ll}
    \text{最大化} & b^T\nu\\
    \text{约束条件} & \|\nu\|_1\leq1\\
    & A^T\nu=0.
    \end{array}\tag{5.104}
    $$

    任意可行的 $\nu$ 都对应于 $\|Ax_{\mathrm{ch}}-b\|_\infty$ 的一个下界 $b^T\nu$。

    将最小二乘残差记为 $r_{\mathrm{ls}}=b-Ax_{\mathrm{ls}}$。假设 $r_{\mathrm{ls}}\neq0$，证明

    $$
    \widehat\nu=-r_{\mathrm{ls}}/\|r_{\mathrm{ls}}\|_1,\qquad\widetilde\nu=r_{\mathrm{ls}}/\|r_{\mathrm{ls}}\|_1
    $$

    都是 (5.104) 的可行点。由对偶性，$b^T\widehat\nu$ 和 $b^T\widetilde\nu$ 都是 $\|Ax_{\mathrm{ch}}-b\|_\infty$ 的下界。哪个下界更好？这些下界与 (a) 中推导的下界相比如何？

**5.7 分段线性最小化。** 考虑凸分段线性最小化问题

$$
\begin{array}{ll}\text{最小化} & \max_{i=1,\ldots,m}(a_i^Tx+b_i),\end{array}\tag{5.105}
$$

其中变量为 $x\in\mathbf{R}^n$。

<!-- pdf-page: 289 -->

- (a) 根据等价问题

    $$
    \begin{array}{ll}
    \text{最小化} & \max_{i=1,\ldots,m}y_i\\
    \text{约束条件} & a_i^Tx+b_i=y_i,\quad i=1,\ldots,m
    \end{array}
    $$

    的拉格朗日对偶，推导一个对偶问题。这里，等价问题的变量为 $x\in\mathbf{R}^n$、$y\in\mathbf{R}^m$。

- (b) 将分段线性最小化问题 (5.105) 表述为 LP，并构造该 LP 的对偶。说明这个 LP 对偶与 (a) 中得到的对偶之间的关系。

- (c) 假设用光滑函数

    $$
    f_0(x)=\log\left(\sum_{i=1}^m\exp(a_i^Tx+b_i)\right)
    $$

    逼近 (5.105) 的目标函数，并求解无约束几何规划

    $$
    \begin{array}{ll}\text{最小化} & \log\left(\sum_{i=1}^m\exp(a_i^Tx+b_i)\right).\end{array}\tag{5.106}
    $$

    这个问题的一个对偶由 (5.62) 给出。用 $p_{\mathrm{pwl}}^\star$ 和 $p_{\mathrm{gp}}^\star$ 分别表示 (5.105) 和 (5.106) 的最优值。证明

    $$
    0\leq p_{\mathrm{gp}}^\star-p_{\mathrm{pwl}}^\star\leq\log m.
    $$

- (d) 对 $p_{\mathrm{pwl}}^\star$ 与问题

    $$
    \begin{array}{ll}\text{最小化} & (1/\gamma)\log\left(\sum_{i=1}^m\exp(\gamma(a_i^Tx+b_i))\right)\end{array}
    $$

    最优值之差，推导类似的界，其中 $\gamma>0$ 是参数。增大 $\gamma$ 时会发生什么？

**5.8** 说明例 5.9（原书第 257 页）中推导出的两个对偶问题之间的关系。

**5.9 一个简单覆盖椭球的次优程度。** 回顾以原点为中心、包含各点 $a_1,\ldots,a_m\in\mathbf{R}^n$ 的最小体积椭球问题（问题 (5.14)，原书第 222 页）：

$$
\begin{array}{ll}
\text{最小化} & f_0(X)=\log\det(X^{-1})\\
\text{约束条件} & a_i^TXa_i\leq1,\quad i=1,\ldots,m,
\end{array}
$$

其中 $\operatorname{\mathbf{dom}}f_0=\mathbf{S}_{++}^n$。假设向量 $a_1,\ldots,a_m$ 张成 $\mathbf{R}^n$（这意味着问题有下界）。

- (a) 证明矩阵

    $$
    X_{\mathrm{sim}}=\left(\sum_{k=1}^m a_ka_k^T\right)^{-1}
    $$

    是可行的。*提示：* 证明

    $$
    \begin{bmatrix}\sum_{k=1}^m a_ka_k^T&a_i\\a_i^T&1\end{bmatrix}\succeq0,
    $$

    并利用 Schur 补（§A.5.5）证明 $a_i^TXa_i\leq1$，$i=1,\ldots,m$。

- (b) 现在利用对偶问题

    $$
    \begin{array}{ll}
    \text{最大化} & \log\det\left(\sum_{i=1}^m\lambda_i a_i a_i^T\right)-\mathbf{1}^T\lambda+n\\
    \text{约束条件} & \lambda\succeq0,
    \end{array}
    $$

    来给出可行点 $X_{\mathrm{sim}}$ 次优程度的界，其中还包含隐式约束 $\sum_{i=1}^m\lambda_i a_i a_i^T\succ0$。（这个对偶在原书第 222 页推导。）为求出一个界，只考虑形如 $\lambda=t\mathbf{1}$ 的对偶变量，其中 $t>0$。解析地求出 $t$ 的最优值，并计算这个 $\lambda$ 处的对偶目标值。利用这一结果证明，椭球 $\{u\mid u^TX_{\mathrm{sim}}u\leq1\}$ 的体积，不超过最小体积椭球体积的 $(m/n)^{n/2}$ 倍。

<!-- pdf-page: 290 -->

**5.10 最优实验设计。** 以下问题出现在实验设计中（见 §7.5）。

- (a) *D-最优设计。*

    $$
    \begin{array}{ll}
    \text{最小化} & \log\det\left(\sum_{i=1}^p x_i v_i v_i^T\right)^{-1}\\
    \text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1.
    \end{array}
    $$

- (b) *A-最优设计。*

    $$
    \begin{array}{ll}
    \text{最小化} & \operatorname{\mathbf{tr}}\left(\sum_{i=1}^p x_i v_i v_i^T\right)^{-1}\\
    \text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1.
    \end{array}
    $$

两个问题的定义域都是 $\{x\mid\sum_{i=1}^p x_i v_i v_i^T\succ0\}$。变量为 $x\in\mathbf{R}^p$；向量 $v_1,\ldots,v_p\in\mathbf{R}^n$ 已知。

先引入新变量 $X\in\mathbf{S}^n$ 以及等式约束 $X=\sum_{i=1}^p x_i v_i v_i^T$，然后利用拉格朗日对偶性，推导两个问题的对偶。尽可能简化对偶问题。

**5.11** 推导问题

$$
\begin{array}{ll}\text{最小化} & \sum_{i=1}^N\|A_ix+b_i\|_2+(1/2)\|x-x_0\|_2^2\end{array}
$$

的一个对偶问题。问题数据为 $A_i\in\mathbf{R}^{m_i\times n}$、$b_i\in\mathbf{R}^{m_i}$ 和 $x_0\in\mathbf{R}^n$。先引入新变量 $y_i\in\mathbf{R}^{m_i}$ 以及等式约束 $y_i=A_ix+b_i$。

**5.12 求解析中心。** 推导问题

$$
\begin{array}{ll}\text{最小化} & -\sum_{i=1}^m\log(b_i-a_i^Tx)\end{array}
$$

的一个对偶问题，其定义域为 $\{x\mid a_i^Tx<b_i,\ i=1,\ldots,m\}$。先引入新变量 $y_i$ 以及等式约束 $y_i=b_i-a_i^Tx$。

（这个问题的解称为线性不等式 $a_i^Tx\leq b_i$，$i=1,\ldots,m$，的**解析中心**。解析中心具有几何应用（见 §8.5.3），并在障碍法中起着重要作用（见第 11 章）。）

**5.13 布尔 LP 的拉格朗日松弛。** **布尔线性规划**是形如下式的优化问题：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b\\
& x_i\in\{0,1\},\quad i=1,\ldots,n,
\end{array}
$$

通常很难求解。在习题 4.15 中，我们研究了这个问题的 LP 松弛：

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b\\
& 0\leq x_i\leq1,\quad i=1,\ldots,n,
\end{array}\tag{5.107}
$$

它容易求解得多，并给出布尔 LP 最优值的一个下界。本题推导布尔 LP 的另一个下界，并弄清这两个下界之间的关系。

- (a) *拉格朗日松弛。* 布尔 LP 可以改写为问题

    $$
    \begin{array}{ll}
    \text{最小化} & c^Tx\\
    \text{约束条件} & Ax\preceq b\\
    & x_i(1-x_i)=0,\quad i=1,\ldots,n,
    \end{array}
    $$

    其中包含二次等式约束。求这个问题的拉格朗日对偶。对偶问题是凸问题，其最优值给出布尔 LP 最优值的一个下界。这种求取最优值下界的方法称为**拉格朗日松弛**（Lagrangian relaxation）。

    <!-- pdf-page: 291 -->

- (b) 证明，由拉格朗日松弛得到的下界，与由 LP 松弛 (5.107) 得到的下界相同。*提示：* 推导 LP 松弛 (5.107) 的对偶。

**5.14 等式约束的罚函数法。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & Ax=b,
\end{array}\tag{5.108}
$$

其中 $f_0:\mathbf{R}^n\to\mathbf{R}$ 为可微凸函数，$A\in\mathbf{R}^{m\times n}$，且 $\operatorname{\mathbf{rank}}A=m$。

在**二次罚函数法**（quadratic penalty method）中，构造辅助函数

$$
\phi(x)=f_0(x)+\alpha\|Ax-b\|_2^2,
$$

其中 $\alpha>0$ 为参数。这个辅助函数由目标函数加上*罚项* $\alpha\|Ax-b\|_2^2$ 组成。其思路是，辅助函数的最小值点 $\widetilde x$ 应当是原问题的一个近似解。直觉上，惩罚权重 $\alpha$ 越大，$\widetilde x$ 对原问题解的逼近就越好。

假设 $\widetilde x$ 是 $\phi$ 的一个最小值点。说明如何由 $\widetilde x$ 求出 (5.108) 的一个对偶可行点。求相应的 (5.108) 最优值的下界。

**5.15** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}\tag{5.109}
$$

其中函数 $f_i:\mathbf{R}^n\to\mathbf{R}$ 可微且凸。设 $h_1,\ldots,h_m:\mathbf{R}\to\mathbf{R}$ 为递增、可微的凸函数。证明

$$
\phi(x)=f_0(x)+\sum_{i=1}^m h_i(f_i(x))
$$

是凸函数。假设 $\widetilde x$ 使 $\phi$ 取得最小值。说明如何由 $\widetilde x$ 求出 (5.109) 对偶问题的一个可行点。求相应的 (5.109) 最优值的下界。

**5.16 不等式约束的精确罚函数法。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m,
\end{array}
\tag{5.110}
$$

其中函数 $f_i:\mathbf{R}^n\to\mathbf{R}$ 可微且凸。在**精确罚函数法**（exact penalty method）中，我们求解辅助问题

$$
\begin{array}{ll}
\text{最小化} & \phi(x)=f_0(x)+\alpha\max_{i=1,\ldots,m}\max\{0,f_i(x)\},
\end{array}
\tag{5.111}
$$

其中 $\alpha>0$ 为参数。$\phi$ 中的第二项用于惩罚 $x$ 违反约束的程度。如果 $\alpha$ 充分大时，辅助问题 (5.111) 的解也都是原问题 (5.110) 的解，就称这种方法为精确罚函数法。

- (a) 证明 $\phi$ 是凸函数。

- (b) 辅助问题可以表示为

    $$
    \begin{array}{ll}
    \text{最小化} & f_0(x)+\alpha y\\
    \text{约束条件} & f_i(x)\leq y,\quad i=1,\ldots,m\\
    & 0\leq y,
    \end{array}
    $$

    其中变量为 $x$ 和 $y\in\mathbf{R}$。求这个问题的拉格朗日对偶，并用 (5.110) 的拉格朗日对偶函数 $g$ 表示它。

    <!-- pdf-page: 292 -->

- (c) 利用 (b) 中的结果证明下面的性质。设 $\lambda^\star$ 是 (5.110) 的拉格朗日对偶的一个最优解，并且强对偶性成立。如果 $\alpha>\mathbf{1}^T\lambda^\star$，则辅助问题 (5.111) 的任意解也是 (5.110) 的最优解。

**5.17 具有多面体不确定性的鲁棒线性规划。** 考虑鲁棒 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & \displaystyle\sup_{a\in\mathcal{P}_i}a^Tx\leq b_i,\quad i=1,\ldots,m,
\end{array}
$$

变量为 $x\in\mathbf{R}^n$，其中 $\mathcal{P}_i=\{a\mid C_i a\preceq d_i\}$。问题数据为 $c\in\mathbf{R}^n$、$C_i\in\mathbf{R}^{m_i\times n}$、$d_i\in\mathbf{R}^{m_i}$ 和 $b\in\mathbf{R}^m$。我们假设各多面体 $\mathcal{P}_i$ 非空。

证明这个问题等价于 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & d_i^Tz_i\leq b_i,\quad i=1,\ldots,m\\
& C_i^Tz_i=x,\quad i=1,\ldots,m\\
& z_i\succeq0,\quad i=1,\ldots,m,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $z_i\in\mathbf{R}^{m_i}$，$i=1,\ldots,m$。*提示：* 求在 $a_i\in\mathcal{P}_i$ 上最大化 $a_i^Tx$ 的问题的对偶，其中变量为 $a_i$。

**5.18 两个多面体之间的分离超平面。** 将下面的问题表示为一个 LP 或 LP 可行性问题。求一个分离超平面，严格分离两个多面体

$$
\mathcal{P}_1=\{x\mid Ax\preceq b\},\qquad
\mathcal{P}_2=\{x\mid Cx\preceq d\},
$$

即求向量 $a\in\mathbf{R}^n$ 和标量 $\gamma$，使得

$$
a^Tx>\gamma\quad\text{对 }x\in\mathcal{P}_1,\qquad
a^Tx<\gamma\quad\text{对 }x\in\mathcal{P}_2.
$$

可以假设 $\mathcal{P}_1$ 与 $\mathcal{P}_2$ 不相交。

*提示：* 向量 $a$ 和标量 $\gamma$ 必须满足

$$
\inf_{x\in\mathcal{P}_1}a^Tx>\gamma>\sup_{x\in\mathcal{P}_2}a^Tx.
$$

利用 LP 对偶性简化这些条件中的下确界和上确界。

**5.19 向量中最大的若干个元素之和。** 定义 $f:\mathbf{R}^n\to\mathbf{R}$ 为

$$
f(x)=\sum_{i=1}^r x_{[i]},
$$

其中 $r$ 是 $1$ 到 $n$ 之间的整数，$x_{[1]}\geq x_{[2]}\geq\cdots\geq x_{[r]}$ 是 $x$ 的分量按降序排列后的结果。换言之，$f(x)$ 是 $x$ 中最大的 $r$ 个元素之和。本题研究约束

$$
f(x)\leq\alpha.
$$

正如第 3 章第 80 页中所述，这是一个凸约束，等价于下面这组含 $n!/(r!(n-r)!)$ 个线性不等式的约束：

$$
x_{i_1}+\cdots+x_{i_r}\leq\alpha,\qquad
1\leq i_1<i_2<\cdots<i_r\leq n.
$$

本题的目的是推导一种更紧凑的表示。

<!-- pdf-page: 293 -->

- (a) 给定向量 $x\in\mathbf{R}^n$，证明 $f(x)$ 等于 LP

    $$
    \begin{array}{ll}
    \text{最大化} & x^Ty\\
    \text{约束条件} & 0\preceq y\preceq\mathbf{1}\\
    & \mathbf{1}^Ty=r
    \end{array}
    $$

    的最优值，其中变量为 $y\in\mathbf{R}^n$。

- (b) 推导 (a) 中 LP 的对偶。证明它可以写成

    $$
    \begin{array}{ll}
    \text{最小化} & rt+\mathbf{1}^Tu\\
    \text{约束条件} & t\mathbf{1}+u\succeq x\\
    & u\succeq0,
    \end{array}
    $$

    其中变量为 $t\in\mathbf{R}$、$u\in\mathbf{R}^n$。由对偶性，这个 LP 与 (a) 中的 LP 有相同的最优值，即 $f(x)$。因此得到如下结果：$x$ 满足 $f(x)\leq\alpha$，当且仅当存在 $t\in\mathbf{R}$、$u\in\mathbf{R}^n$，使得

    $$
    rt+\mathbf{1}^Tu\leq\alpha,\qquad
    t\mathbf{1}+u\succeq x,\qquad
    u\succeq0.
    $$

    这些条件构成关于 $x,u,t$ 这 $2n+1$ 个变量的一组 $2n+1$ 个线性不等式。

- (c) 作为一个应用，我们考虑第 4 章第 155 页讨论过的经典 Markowitz 投资组合优化问题

    $$
    \begin{array}{ll}
    \text{最小化} & x^T\Sigma x\\
    \text{约束条件} & \bar p^Tx\geq r_{\min}\\
    & \mathbf{1}^Tx=1,\quad x\succeq0
    \end{array}
    $$

    的一个扩展。变量为投资组合 $x\in\mathbf{R}^n$；$\bar p$ 和 $\Sigma$ 分别是价格变化向量 $p$ 的均值和协方差矩阵。

    假设增加一个*分散化约束*，要求投向任意 $10\%$ 的资产的资金不得超过总预算的 $80\%$。这个约束可以表示为

    $$
    \sum_{i=1}^{\lfloor0.1n\rfloor}x_{[i]}\leq0.8.
    $$

    将带有分散化约束的投资组合优化问题表示为一个 QP。

**5.20 信道容量问题的对偶。** 推导问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle-c^Tx+\sum_{i=1}^m y_i\log y_i\\
\text{约束条件} & Px=y\\
& x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

的一个对偶问题，其中 $P\in\mathbf{R}^{m\times n}$ 的元素非负，且各列元素之和为一（即 $P^T\mathbf{1}=\mathbf{1}$）。变量为 $x\in\mathbf{R}^n$、$y\in\mathbf{R}^m$。（当 $c_j=\sum_{i=1}^m p_{ij}\log p_{ij}$ 时，最优值与信道转移概率矩阵为 $P$ 的离散无记忆信道容量的负值只相差一个 $\log2$ 因子；见习题 4.57。）

尽可能简化对偶问题。

<!-- pdf-page: 294 -->

### 强对偶性与 Slater 条件

**5.21 强对偶性不成立的凸问题。** 考虑优化问题

$$
\begin{array}{ll}
\text{最小化} & e^{-x}\\
\text{约束条件} & x^2/y\leq0,
\end{array}
$$

变量为 $x$ 和 $y$，定义域为 $\mathcal{D}=\{(x,y)\mid y>0\}$。

- (a) 验证这是一个凸优化问题。求其最优值。

- (b) 给出拉格朗日对偶问题，并求对偶问题的最优解 $\lambda^\star$ 和最优值 $d^\star$。最优对偶间隙是多少？

- (c) 这个问题满足 Slater 条件吗？

- (d) 扰动问题

    $$
    \begin{array}{ll}
    \text{最小化} & e^{-x}\\
    \text{约束条件} & x^2/y\leq u
    \end{array}
    $$

    的最优值 $p^\star(u)$ 作为 $u$ 的函数是什么？验证全局灵敏度不等式

    $$
    p^\star(u)\geq p^\star(0)-\lambda^\star u
    $$

    不成立。

**5.22 对偶性的几何解释。** 对下面每个优化问题，画出集合

$$
\begin{aligned}
\mathcal{G}&=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)=t,\ f_1(x)=u\},\\
\mathcal{A}&=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)\leq t,\ f_1(x)\leq u\}
\end{aligned}
$$

的示意图，给出对偶问题，并求解原问题和对偶问题。问题是凸的吗？是否满足 Slater 条件？强对偶性是否成立？

除非另有说明，问题的定义域为 $\mathbf{R}$。

- (a) 在 $x^2\leq1$ 的约束下最小化 $x$。

- (b) 在 $x^2\leq0$ 的约束下最小化 $x$。

- (c) 在 $|x|\leq0$ 的约束下最小化 $x$。

- (d) 在 $f_1(x)\leq0$ 的约束下最小化 $x$，其中

    $$
    f_1(x)=
    \begin{cases}
    -x+2 & x\geq1,\\
    x & -1\leq x\leq1,\\
    -x-2 & x\leq-1.
    \end{cases}
    $$

- (e) 在 $-x+1\leq0$ 的约束下最小化 $x^3$。

- (f) 在 $-x+1\leq0$ 的约束下最小化 $x^3$，定义域为 $\mathcal{D}=\mathbf{R}_+$。

**5.23 线性规划中的强对偶性。** 我们证明，只要 LP

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq b
\end{array}
$$

及其对偶

$$
\begin{array}{ll}
\text{最大化} & -b^Tz\\
\text{约束条件} & A^Tz+c=0,\quad z\succeq0
\end{array}
$$

中至少一个问题可行，强对偶性就成立。换言之，强对偶性唯一可能不成立的情形是 $p^\star=\infty$ 且 $d^\star=-\infty$。

<!-- pdf-page: 295 -->

- (a) 假设 $p^\star$ 有限，且 $x^\star$ 是一个最优解。（LP 的最优值若有限，就一定能达到。）设 $I\subseteq\{1,2,\ldots,m\}$ 为在 $x^\star$ 处的有效约束的指标集：

    $$
    a_i^Tx^\star=b_i,\quad i\in I,\qquad
    a_i^Tx^\star<b_i,\quad i\notin I.
    $$

    证明存在 $z\in\mathbf{R}^m$，满足

    $$
    z_i\geq0,\quad i\in I,\qquad
    z_i=0,\quad i\notin I,\qquad
    \sum_{i\in I}z_i a_i+c=0.
    $$

    证明 $z$ 是对偶最优解，其目标值为 $c^Tx^\star$。

    *提示：* 假设不存在这样的 $z$，即 $-c\notin\{\sum_{i\in I}z_i a_i\mid z_i\geq0\}$。利用第 49 页例 2.20 中的严格分离超平面定理导出矛盾。也可以使用 Farkas 引理（见 §5.8.3）。

- (b) 假设 $p^\star=\infty$ 且对偶问题可行。证明 $d^\star=\infty$。*提示：* 证明存在非零的 $v\in\mathbf{R}^m$，使得 $A^Tv=0$、$v\succeq0$、$b^Tv<0$。如果对偶问题可行，它就沿方向 $v$ 无界。

- (c) 考虑例子

    $$
    \begin{array}{ll}
    \text{最小化} & x\\
    \text{约束条件} &
    \begin{bmatrix}0\\1\end{bmatrix}x
    \preceq
    \begin{bmatrix}-1\\1\end{bmatrix}.
    \end{array}
    $$

    写出对偶 LP，并求解原问题和对偶问题。证明 $p^\star=\infty$ 且 $d^\star=-\infty$。

**5.24 弱极大极小不等式。** 证明弱极大极小不等式

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)
\leq
\inf_{w\in W}\sup_{z\in Z}f(w,z)
$$

*总是*成立，无须对 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$、$W\subseteq\mathbf{R}^n$ 或 $Z\subseteq\mathbf{R}^m$ 作任何假设。

**5.25** [BL00，第 95 页] **凸凹函数与鞍点性质。** 我们推导鞍点性质

$$
\sup_{z\in Z}\inf_{w\in W}f(w,z)
=
\inf_{w\in W}\sup_{z\in Z}f(w,z)
\tag{5.112}
$$

成立的条件，其中 $f:\mathbf{R}^n\times\mathbf{R}^m\to\mathbf{R}$、$W\times Z\subseteq\operatorname{\mathbf{dom}}f$，且 $W$ 和 $Z$ 非空。我们假设，对每个 $z\in Z$，函数

$$
g_z(w)=
\begin{cases}
f(w,z) & w\in W,\\
\infty & \text{其他情形}
\end{cases}
$$

都是闭凸函数；对每个 $w\in W$，函数

$$
h_w(z)=
\begin{cases}
-f(w,z) & z\in Z,\\
\infty & \text{其他情形}
\end{cases}
$$

也都是闭凸函数。

- (a) (5.112) 的右端可以表示为 $p(0)$，其中

    $$
    p(u)=\inf_{w\in W}\sup_{z\in Z}\bigl(f(w,z)+u^Tz\bigr).
    $$

    证明 $p$ 是凸函数。

    <!-- pdf-page: 296 -->

- (b) 证明 $p$ 的共轭函数为

    $$
    p^*(v)=
    \begin{cases}
    -\inf_{w\in W}f(w,v) & v\in Z,\\
    \infty & \text{其他情形}.
    \end{cases}
    $$

- (c) 证明 $p^*$ 的共轭函数为

    $$
    p^{**}(u)=\sup_{z\in Z}\inf_{w\in W}\bigl(f(w,z)+u^Tz\bigr).
    $$

    将此式与 (a) 结合，就可以把极大极小等式 (5.112) 表示为 $p^{**}(0)=p(0)$。

- (d) 由习题 3.28 和 3.39(d) 可知，若 $0\in\operatorname{\mathbf{int}}\operatorname{\mathbf{dom}}p$，则 $p^{**}(0)=p(0)$。由此得出，若 $W$ 和 $Z$ 有界，这一等式成立。

- (e) 习题 3.28 和 3.39 还有一个推论：若 $0\in\operatorname{\mathbf{dom}}p$ 且 $p$ 是闭函数，则 $p^{**}(0)=p(0)$。证明，如果 $g_z$ 的下水平集有界，则 $p$ 是闭函数。

### 最优性条件

**5.26** 考虑 QCQP

$$
\begin{array}{ll}
\text{最小化} & x_1^2+x_2^2\\
\text{约束条件} & (x_1-1)^2+(x_2-1)^2\leq1\\
& (x_1-1)^2+(x_2+1)^2\leq1,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^2$。

- (a) 画出可行集和目标函数等值线的示意图。求最优点 $x^\star$ 和最优值 $p^\star$。

- (b) 给出 KKT 条件。是否存在拉格朗日乘子 $\lambda_1^\star$ 和 $\lambda_2^\star$，能够证明 $x^\star$ 最优？

- (c) 推导并求解拉格朗日对偶问题。强对偶性成立吗？

**5.27 带等式约束的最小二乘。** 考虑带等式约束的最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2\\
\text{约束条件} & Gx=h,
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$ 且 $\operatorname{\mathbf{rank}}A=n$，$G\in\mathbf{R}^{p\times n}$ 且 $\operatorname{\mathbf{rank}}G=p$。

给出 KKT 条件，并推导原问题解 $x^\star$ 和对偶问题解 $\nu^\star$ 的表达式。

**5.28** 证明（不使用任何线性规划代码），LP

$$
\begin{array}{ll}
\text{最小化} & 47x_1+93x_2+17x_3-93x_4\\
\text{约束条件} &
\begin{bmatrix}
-1&-6&1&3\\
-1&-2&7&1\\
0&3&-10&-1\\
-6&-11&-2&12\\
1&6&-1&-3
\end{bmatrix}
\begin{bmatrix}x_1\\x_2\\x_3\\x_4\end{bmatrix}
\preceq
\begin{bmatrix}-3\\5\\-8\\-7\\4\end{bmatrix}
\end{array}
$$

的最优解唯一，且为 $x^\star=(1,1,1,1)$。

**5.29** 问题

$$
\begin{array}{ll}
\text{最小化} & -3x_1^2+x_2^2+2x_3^2+2(x_1+x_2+x_3)\\
\text{约束条件} & x_1^2+x_2^2+x_3^2=1,
\end{array}
$$

是 (5.32) 的一个特例，所以即使该问题不是凸问题，强对偶性仍然成立。推导 KKT 条件。求所有满足 KKT 条件的解 $x,\nu$。其中哪一对对应最优解？

<!-- pdf-page: 297 -->

**5.30** 推导问题

$$
\begin{array}{ll}
\text{最小化} & \operatorname{\mathbf{tr}}X-\log\det X\\
\text{约束条件} & Xs=y,
\end{array}
$$

的 KKT 条件，其中变量为 $X\in\mathbf{S}^n$，定义域为 $\mathbf{S}_{++}^n$。给定 $y\in\mathbf{R}^n$ 和 $s\in\mathbf{R}^n$，且 $s^Ty=1$。验证最优解为

$$
X^\star=I+yy^T-\frac{1}{s^Ts}ss^T.
$$

**5.31 KKT 条件的支撑超平面解释。** 考虑不含等式约束的凸问题

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m.
\end{array}
$$

假设 $x^\star\in\mathbf{R}^n$ 和 $\lambda^\star\in\mathbf{R}^m$ 满足 KKT 条件

$$
\begin{aligned}
f_i(x^\star)&\leq0,\quad i=1,\ldots,m\\
\lambda_i^\star&\geq0,\quad i=1,\ldots,m\\
\lambda_i^\star f_i(x^\star)&=0,\quad i=1,\ldots,m\\
\nabla f_0(x^\star)+\sum_{i=1}^m\lambda_i^\star\nabla f_i(x^\star)&=0.
\end{aligned}
$$

证明：对所有可行的 $x$，都有

$$
\nabla f_0(x^\star)^T(x-x^\star)\geq0.
$$

换言之，KKT 条件蕴含 §4.2.3 中的简单最优性判据。

### 扰动与灵敏度分析

**5.32 扰动问题的最优值。** 设 $f_0,f_1,\ldots,f_m:\mathbf{R}^n\to\mathbf{R}$ 为凸函数。证明函数

$$
p^\star(u,v)=\inf\{f_0(x)\mid\exists x\in\mathcal{D},\ f_i(x)\leq u_i,\ i=1,\ldots,m,\ Ax-b=v\}
$$

是凸函数。这个函数把扰动问题的最优代价表示为扰动量 $u$ 和 $v$ 的函数（见 §5.6.1）。

**5.33 参数化的 $\ell_1$ 范数逼近。** 考虑 $\ell_1$ 范数最小化问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax+b+\epsilon d\|_1
\end{array}
$$

变量为 $x\in\mathbf{R}^3$，其中

$$
A=\begin{bmatrix}
-2&7&1\\
-5&-1&3\\
-7&3&-5\\
-1&4&-4\\
1&5&5\\
2&-5&-1
\end{bmatrix},\qquad
b=\begin{bmatrix}-4\\3\\9\\0\\-11\\5\end{bmatrix},\qquad
d=\begin{bmatrix}-10\\-13\\-27\\-10\\-7\\14\end{bmatrix}.
$$

用 $p^\star(\epsilon)$ 表示作为 $\epsilon$ 的函数的最优值。

- (a) 假设 $\epsilon=0$。证明 $x^\star=\mathbf{1}$ 是最优点。是否还有其他最优点？

- (b) 证明：在一个包含 $\epsilon=0$ 的区间上，$p^\star(\epsilon)$ 是仿射函数。

<!-- pdf-page: 298 -->

**5.34** 考虑下列一对原线性规划和对偶线性规划：

$$
\begin{array}{ll}
\text{最小化} & (c+\epsilon d)^Tx\\
\text{约束条件} & Ax\preceq b+\epsilon f
\end{array}
$$

和

$$
\begin{array}{ll}
\text{最大化} & -(b+\epsilon f)^Tz\\
\text{约束条件} & A^Tz+c+\epsilon d=0\\
& z\succeq0,
\end{array}
$$

其中

$$
A=\begin{bmatrix}
-4&12&-2&1\\
-17&12&7&11\\
1&0&-6&1\\
3&3&22&-1\\
-11&2&-1&-8
\end{bmatrix},\qquad
b=\begin{bmatrix}8\\13\\-4\\27\\-18\end{bmatrix},\qquad
f=\begin{bmatrix}6\\15\\-13\\48\\8\end{bmatrix},
$$

$c=(49,-34,-50,-5)$、$d=(3,8,21,25)$，而 $\epsilon$ 是参数。

- (a) 通过构造一个与 $x^\star$ 具有相同目标值的对偶最优点 $z^\star$，证明 $\epsilon=0$ 时 $x^\star=(1,1,1,1)$ 是最优点。原问题或对偶问题是否还有其他最优解？

- (b) 在一个包含 $\epsilon=0$ 的区间上，给出最优值 $p^\star(\epsilon)$ 关于 $\epsilon$ 的显式表达式。指出该表达式成立的区间。还要在同一区间上，给出原问题解 $x^\star(\epsilon)$ 和对偶问题解 $z^\star(\epsilon)$ 关于 $\epsilon$ 的显式表达式。

    **提示。** 先假定：在 $\epsilon=0$ 的最优点处有效的原问题约束和对偶问题约束，对于 $0$ 附近的 $\epsilon$，在最优点处仍然有效。在这个假定下计算 $x^\star(\epsilon)$ 和 $z^\star(\epsilon)$，然后验证假定成立。

**5.35 几何规划的灵敏度分析。** 考虑几何规划

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq1,\quad i=1,\ldots,m\\
& h_i(x)=1,\quad i=1,\ldots,p,
\end{array}
$$

其中 $f_0,\ldots,f_m$ 为正项式，$h_1,\ldots,h_p$ 为单项式，问题的定义域为 $\mathbf{R}_{++}^n$。将扰动后的几何规划定义为

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & f_i(x)\leq e^{u_i},\quad i=1,\ldots,m\\
& h_i(x)=e^{v_i},\quad i=1,\ldots,p,
\end{array}
$$

并用 $p^\star(u,v)$ 表示扰动后的几何规划的最优值。可以把 $u_i$ 和 $v_i$ 看作约束的相对扰动，即按比例施加的扰动。例如，$u_1=-0.01$ 相当于将第一个不等式约束收紧约 $1\%$。

设 $\lambda^\star$ 和 $\nu^\star$ 是凸形式几何规划

$$
\begin{array}{ll}
\text{最小化} & \log f_0(y)\\
\text{约束条件} & \log f_i(y)\leq0,\quad i=1,\ldots,m\\
& \log h_i(y)=0,\quad i=1,\ldots,p,
\end{array}
$$

的最优对偶变量，其中变量为 $y_i=\log x_i$。假设 $p^\star(u,v)$ 在 $u=0$、$v=0$ 处可微，求 $\lambda^\star$、$\nu^\star$ 与 $p^\star(u,v)$ 在 $u=0$、$v=0$ 处的导数之间的关系。说明下列说法成立的理由：“当 $\alpha$ 较小时，将第 $i$ 个约束放宽 $\alpha\%$，会使目标值改善约 $\alpha\lambda_i^\star\%$。”

<div class="translator-note" markdown="1">

**译注（习题 5.35）：** 按题首对 $f_i$ 和 $h_i$ 的定义，代换 $y_i=\log x_i$ 后，凸形式中的目标与约束应写为 $\log f_0(e^y)$、$\log f_i(e^y)\leq0$、$\log h_i(e^y)=0$，其中 $e^y$ 表示逐分量取指数。原式省略了自变量中的指数变换。

</div>

<!-- pdf-page: 299 -->

### 择一定理

**5.36 线性等式的择一系统。** 考虑线性方程组 $Ax=b$，其中 $A\in\mathbf{R}^{m\times n}$。由线性代数可知，这个方程组有解当且仅当 $b\in\mathcal{R}(A)$，而后者等价于 $b\perp\mathcal{N}(A^T)$。换言之，$Ax=b$ 有解当且仅当不存在满足 $A^Ty=0$ 且 $b^Ty\ne0$ 的 $y\in\mathbf{R}^m$。

由 §5.8.2 的择一定理推导这一结果。

**5.37** [BT97] **有限状态马尔可夫链中平衡分布的存在性。** 设 $P\in\mathbf{R}^{n\times n}$ 是满足

$$
p_{ij}\geq0,\quad i,j=1,\ldots,n,\qquad P^T\mathbf{1}=\mathbf{1}
$$

的矩阵，即各元素非负且各列之和为一。用 Farkas 引理证明，存在 $y\in\mathbf{R}^n$ 使得

$$
Py=y,\qquad y\succeq0,\qquad\mathbf{1}^Ty=1.
$$

（可以把 $y$ 解释为一个具有 $n$ 个状态、转移概率矩阵为 $P$ 的马尔可夫链的平衡分布。）

**5.38** [BT97] **期权定价。** 将第 263 页例 5.10 的结果应用于一个含有三种资产的简单问题：一种在所考察的投资期内具有固定回报 $r>1$ 的无风险资产（例如债券）、一只股票，以及该股票的一份期权。这份期权使我们有权在期末以预先确定的价格 $K$ 买入股票。

考虑两种情景。在第一种情景中，股票价格从期初的 $S$ 上涨至期末的 $Su$，其中 $u>r$。在这种情景下，仅当 $Su>K$ 时才行使期权，此时获得的利润为 $Su-K$；否则不行使期权，利润为零。因此，第一种情景下期权在期末的价值为 $\max\{0,Su-K\}$。

在第二种情景中，股票价格从 $S$ 下跌至 $Sd$，其中 $d<1$。期末价值为 $\max\{0,Sd-K\}$。

使用例 5.10 中的记号，

$$
V=\begin{bmatrix}
r&uS&\max\{0,Su-K\}\\
r&dS&\max\{0,Sd-K\}
\end{bmatrix},\qquad
p_1=1,\quad p_2=S,\quad p_3=C,
$$

其中 $C$ 为期权价格。

证明：给定 $r$、$S$、$K$、$u$、$d$ 后，无套利条件唯一确定期权价格 $C$。换言之，这份期权的市场是完备的。

### 广义不等式

**5.39 两路划分问题的半定规划松弛。** 考虑第 219 页介绍的两路划分问题 (5.7)：

$$
\begin{array}{ll}
\text{最小化} & x^TWx\\
\text{约束条件} & x_i^2=1,\quad i=1,\ldots,n,
\end{array}
\tag{5.113}
$$

变量为 $x\in\mathbf{R}^n$。这个（非凸）问题的拉格朗日对偶问题是半定规划

$$
\begin{array}{ll}
\text{最大化} & -\mathbf{1}^T\nu\\
\text{约束条件} & W+\operatorname{\mathbf{diag}}(\nu)\succeq0,
\end{array}
\tag{5.114}
$$

变量为 $\nu\in\mathbf{R}^n$。这个半定规划的最优值给出了划分问题 (5.113) 最优值的一个下界。在本题中，我们将推导另一个半定规划，它也给出两路划分问题最优值的一个下界，并探讨这两个半定规划之间的联系。

<!-- pdf-page: 300 -->

- (a) **矩阵形式的两路划分问题。** 证明，两路划分问题可以写成

    $$
    \begin{array}{ll}
    \text{最小化} & \operatorname{\mathbf{tr}}(WX)\\
    \text{约束条件} & X\succeq0,\quad\operatorname{\mathbf{rank}}X=1\\
    & X_{ii}=1,\quad i=1,\ldots,n,
    \end{array}
    $$

    变量为 $X\in\mathbf{S}^n$。**提示。** 证明：若 $X$ 可行，则它具有 $X=xx^T$ 的形式，其中 $x\in\mathbf{R}^n$ 满足 $x_i\in\{-1,1\}$，反之亦然。

- (b) **两路划分问题的半定规划松弛。** 利用 (a) 中的表述，可以构造松弛问题

    $$
    \begin{array}{ll}
    \text{最小化} & \operatorname{\mathbf{tr}}(WX)\\
    \text{约束条件} & X\succeq0\\
    & X_{ii}=1,\quad i=1,\ldots,n,
    \end{array}
    \tag{5.115}
    $$

    变量为 $X\in\mathbf{S}^n$。这个问题是半定规划，因此可以高效求解。解释为什么它的最优值给出了两路划分问题 (5.113) 最优值的一个下界。如果这个半定规划的某个最优点 $X^\star$ 的秩为一，你能得出什么结论？

- (c) 现在有两个半定规划能给出两路划分问题 (5.113) 最优值的下界：一是 (b) 中得到的半定规划松弛 (5.115)，二是 (5.114) 给出的两路划分问题的拉格朗日对偶。这两个半定规划之间是什么关系？它们给出的下界之间有什么关系？**提示。** 通过对偶性建立两个半定规划之间的联系。

**5.40 E-最优实验设计。** 习题 5.10 中两个最优实验设计问题的一个变式是 E-最优设计问题

$$
\begin{array}{ll}
\text{最小化} & \lambda_{\max}\left(\sum_{i=1}^p x_iv_iv_i^T\right)^{-1}\\
\text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1.
\end{array}
$$

（另见 §7.5。）先把它改写为

$$
\begin{array}{ll}
\text{最小化} & 1/t\\
\text{约束条件} & \sum_{i=1}^p x_iv_iv_i^T\succeq tI\\
& x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

变量为 $t\in\mathbf{R}$、$x\in\mathbf{R}^p$，定义域为 $\mathbf{R}_{++}\times\mathbf{R}^p$；然后应用拉格朗日对偶性，推导这个问题的一个对偶问题。尽可能简化所得的对偶问题。

**5.41 最快混合马尔可夫链问题的对偶。** 在第 174 页，我们遇到了半定规划

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & -tI\preceq P-(1/n)\mathbf{1}\mathbf{1}^T\preceq tI\\
& P\mathbf{1}=\mathbf{1}\\
& P_{ij}\geq0,\quad i,j=1,\ldots,n\\
& P_{ij}=0,\quad (i,j)\notin\mathcal{E},
\end{array}
$$

变量为 $t\in\mathbf{R}$、$P\in\mathbf{S}^n$。

证明，这个问题的对偶可以表示为

$$
\begin{array}{ll}
\text{最大化} & \mathbf{1}^Tz-(1/n)\mathbf{1}^TY\mathbf{1}\\
\text{约束条件} & \|Y\|_{2*}\leq1\\
& (z_i+z_j)\leq Y_{ij},\quad(i,j)\in\mathcal{E},
\end{array}
$$

变量为 $z\in\mathbf{R}^n$ 和 $Y\in\mathbf{S}^n$。范数 $\|\cdot\|_{2*}$ 是 $\mathbf{S}^n$ 上谱范数的对偶范数：$\|Y\|_{2*}=\sum_{i=1}^n|\lambda_i(Y)|$，即 $Y$ 的特征值绝对值之和。（见第 637 页 §A.1.6。）

<div class="translator-note" markdown="1">

**译注（习题 5.41）：** 原对偶目标与约束的系数不匹配。若保留约束 $z_i+z_j\leq Y_{ij}$，目标的第一项应为 $2\mathbf{1}^Tz$；若保留目标中的 $\mathbf{1}^Tz$，则约束应为 $(z_i+z_j)/2\leq Y_{ij}$。例如，当 $\mathcal{E}$ 包含所有 $(i,j)$ 时，原问题取 $P=\mathbf{1}\mathbf{1}^T/n$ 可得最优值 $0$；但原印刷对偶式中的可行点 $Y=-\mathbf{1}\mathbf{1}^T/n$、$z=-\mathbf{1}/(2n)$ 给出目标值 $1/2$，与弱对偶性矛盾。

</div>

<!-- pdf-page: 301 -->

**5.42 不等式形式锥规划的拉格朗日对偶。** 求不等式形式的锥规划

$$
\begin{array}{ll}
\text{最小化} & c^Tx\\
\text{约束条件} & Ax\preceq_K b
\end{array}
$$

的拉格朗日对偶问题，其中 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$，$K$ 是 $\mathbf{R}^m$ 中的正常锥。把所有隐含的等式约束显式写出。

**5.43 二阶锥规划的对偶。** 证明，二阶锥规划

$$
\begin{array}{ll}
\text{最小化} & f^Tx\\
\text{约束条件} & \|A_ix+b_i\|_2\leq c_i^Tx+d_i,\quad i=1,\ldots,m,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$，其对偶可以表示为

$$
\begin{array}{ll}
\text{最大化} & \sum_{i=1}^m(b_i^Tu_i-d_iv_i)\\
\text{约束条件} & \sum_{i=1}^m(A_i^Tu_i-c_iv_i)+f=0\\
& \|u_i\|_2\leq v_i,\quad i=1,\ldots,m,
\end{array}
$$

变量为 $u_i\in\mathbf{R}^{n_i}$、$v_i\in\mathbf{R}$，$i=1,\ldots,m$。问题数据为 $f\in\mathbf{R}^n$、$A_i\in\mathbf{R}^{n_i\times n}$、$b_i\in\mathbf{R}^{n_i}$、$c_i\in\mathbf{R}$ 和 $d_i\in\mathbf{R}$，$i=1,\ldots,m$。

用下列两种方法推导对偶问题。

- (a) 引入新变量 $y_i\in\mathbf{R}^{n_i}$ 和 $t_i\in\mathbf{R}$，以及等式 $y_i=A_ix+b_i$、$t_i=c_i^Tx+d_i$，然后推导拉格朗日对偶。

- (b) 从二阶锥规划的锥形式出发，利用锥对偶。使用二阶锥是自对偶锥这一事实。

<div class="translator-note" markdown="1">

**译注（习题 5.43）：** 数据行中的 $c_i\in\mathbf{R}$ 应为 $c_i\in\mathbf{R}^n$，才能与约束中的 $c_i^Tx$ 以及对偶等式中的 $c_iv_i$ 保持维数一致。

</div>

**5.44 非严格线性矩阵不等式的强择一系统。** 在第 270 页例 5.14 中，我们提到，系统

$$
Z\succeq0,\qquad\operatorname{\mathbf{tr}}(GZ)>0,\qquad\operatorname{\mathbf{tr}}(F_iZ)=0,\quad i=1,\ldots,n,
\tag{5.116}
$$

是非严格线性矩阵不等式

$$
F(x)=x_1F_1+\cdots+x_nF_n+G\preceq0
\tag{5.117}
$$

的强择一系统，只要矩阵 $F_i$ 满足

$$
\sum_{i=1}^n v_iF_i\succeq0\quad\Longrightarrow\quad\sum_{i=1}^n v_iF_i=0.
\tag{5.118}
$$

在本题中，我们将证明这一结果，并给出一个例子，说明这两个系统并非总是强择一系统。

- (a) 假设 (5.118) 成立，并且辅助半定规划

    $$
    \begin{array}{ll}
    \text{最小化} & s\\
    \text{约束条件} & F(x)\preceq sI
    \end{array}
    $$

    的最优值为正。证明这个最优值能够达到。由 §5.9.4 的讨论可知，系统 (5.117) 与 (5.116) 是强择一系统。

    **提示。** 不失一般性地假设矩阵 $F_1,\ldots,F_n$ 线性无关，可以简化证明。这样一来，就可以用 $\sum_{i=1}^n v_iF_i\succeq0\Rightarrow v=0$ 代替 (5.118)。

- (b) 取 $n=1$，并取

    $$
    G=\begin{bmatrix}0&1\\1&0\end{bmatrix},\qquad
    F_1=\begin{bmatrix}0&0\\0&1\end{bmatrix}.
    $$

    证明 (5.117) 与 (5.116) 均不可行。

<!-- pdf-page: 302 -->
