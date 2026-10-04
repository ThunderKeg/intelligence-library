<!-- pdf-page: 305 -->

# 第 6 章 逼近与拟合

<aside class="chapter-guide"><p>导读（编者）：本章把凸优化用于逼近与拟合：先用范数和罚函数衡量误差，再通过正则化控制解的性质，并处理数据中的不确定性。随后讨论如何选择函数来拟合数据，以及如何利用凸性、单调性等已知条件限制拟合结果。阅读时可留意：不同的误差度量和约束，分别保留了什么信息，又允许了什么偏差。</p></aside>

## 6.1 范数逼近

### 6.1.1 基本范数逼近问题

最简单的**范数逼近问题**是如下形式的无约束问题：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|,
\end{array}
\tag{6.1}
$$

其中 $A\in\mathbf{R}^{m\times n}$ 和 $b\in\mathbf{R}^m$ 是问题数据，$x\in\mathbf{R}^n$ 是变量，$\|\cdot\|$ 是 $\mathbf{R}^m$ 上的一个范数。范数逼近问题的解有时称为在范数 $\|\cdot\|$ 意义下 $Ax\approx b$ 的一个**近似解**。向量

$$
r=Ax-b
$$

称为这个问题的**残差**（residual）；其各个分量有时称为与 $x$ 对应的各个残差。

范数逼近问题 (6.1) 是凸问题，而且可解，即总存在至少一个最优解。其最优值为零，当且仅当 $b\in\mathcal{R}(A)$；不过，当 $b\notin\mathcal{R}(A)$ 时，这个问题更有意思，也更有用。不失一般性，可以假设 $A$ 的各列线性无关；特别地，有 $m\geq n$。当 $m=n$ 时，最优点就是 $A^{-1}b$，因此可以假设 $m>n$。

#### 逼近的解释

把 $Ax$ 写成

$$
Ax=x_1a_1+\cdots+x_na_n,
$$

其中 $a_1,\ldots,a_n\in\mathbf{R}^m$ 是 $A$ 的各列，就可以看出：范数逼近问题的目标是用 $A$ 各列的线性组合尽可能贴近地拟合或逼近向量 $b$，偏差则用范数 $\|\cdot\|$ 衡量。

逼近问题也称为**回归问题**（regression problem）。在这种语境中，向量 $a_1,\ldots,a_n$ 称为**回归变量**（regressors），而向量 $x_1a_1+\cdots+x_na_n$，<!-- pdf-page: 306 -->其中 $x$ 是问题的一个最优解，称为 $b$（在这些回归变量上）的**回归**。

#### 估计的解释

根据不完全准确的线性向量测量来估计参数向量时，也会得到范数逼近问题的一种密切相关的解释。考虑线性测量模型

$$
y=Ax+v,
$$

其中 $y\in\mathbf{R}^m$ 是测量向量，$x\in\mathbf{R}^n$ 是待估计的参数向量，$v\in\mathbf{R}^m$ 是未知的测量误差，但假定它（按范数 $\|\cdot\|$ 衡量）很小。估计问题就是在给定 $y$ 的情况下，对 $x$ 作出合理的猜测。

如果猜测 $x$ 的值为 $\widehat x$，就隐含地猜测 $v$ 的值为 $y-A\widehat x$。假设较小的 $v$（按 $\|\cdot\|$ 衡量）比较大的 $v$ 更可信，那么对 $x$ 最可信的猜测就是

$$
\widehat x=\operatorname{argmin}_z\|Az-y\|.
$$

（这些想法可以在统计框架下更正式地表述；见第 7 章。）

#### 几何解释

考虑子空间 $\mathcal{A}=\mathcal{R}(A)\subseteq\mathbf{R}^m$ 和点 $b\in\mathbf{R}^m$。在范数 $\|\cdot\|$ 意义下，点 $b$ 在子空间 $\mathcal{A}$ 上的一个**投影**，是 $\mathcal{A}$ 中距离 $b$ 最近的任意一点，也就是问题

$$
\begin{array}{ll}
\text{最小化} & \|u-b\|\\
\text{约束条件} & u\in\mathcal{A}
\end{array}
$$

的任意最优点。把 $\mathcal{R}(A)$ 的任意元素参数化为 $u=Ax$，就可以看出，求解范数逼近问题 (6.1) 等价于计算 $b$ 在 $\mathcal{A}$ 上的一个投影。

#### 设计的解释

范数逼近问题 (6.1) 可以解释为一个最优设计问题。$n$ 个变量 $x_1,\ldots,x_n$ 是待确定取值的**设计变量**。向量 $y=Ax$ 给出 $m$ 个**结果**组成的向量，假设这些结果都是设计变量 $x$ 的线性函数。向量 $b$ 由各个**目标结果**或**期望结果**组成。目标是选择设计变量向量，使实际结果尽可能接近期望结果，即 $Ax\approx b$。残差向量 $r$ 可以解释为实际结果（即 $Ax$）与期望结果或目标结果（即 $b$）之间的偏差。如果用实际结果与期望结果之间的偏差范数来衡量设计的好坏，那么范数逼近问题 (6.1) 就是寻找最佳设计的问题。

<!-- pdf-page: 307 -->

#### 加权范数逼近问题

范数逼近问题的一种扩展是**加权范数逼近问题**：

$$
\begin{array}{ll}
\text{最小化} & \|W(Ax-b)\|,
\end{array}
$$

其中问题数据 $W\in\mathbf{R}^{m\times m}$ 称为**加权矩阵**。加权矩阵通常是对角矩阵，这时它对残差向量 $r=Ax-b$ 的不同分量赋予不同的相对重要性。

加权范数问题可以看成范数为 $\|\cdot\|$、数据为 $\widetilde A=WA$、$\widetilde b=Wb$ 的范数逼近问题，因此可以作为标准范数逼近问题 (6.1) 处理。另一种看法是，把它视为数据为 $A$ 和 $b$、使用 **$W$ 加权范数**的范数逼近问题，这个范数定义为

$$
\|z\|_W=\|Wz\|
$$

（这里假设 $W$ 非奇异）。

#### 最小二乘逼近

最常见的范数逼近问题使用欧几里得范数，即 $\ell_2$ 范数。把目标函数平方，就得到一个等价问题，称为**最小二乘逼近问题**：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2=r_1^2+r_2^2+\cdots+r_m^2,
\end{array}
$$

其中目标函数是各残差的平方和。把目标函数写成凸二次函数

$$
f(x)=x^TA^TAx-2b^TAx+b^Tb,
$$

就能解析地求解这个问题。点 $x$ 使 $f$ 最小，当且仅当

$$
\nabla f(x)=2A^TAx-2A^Tb=0,
$$

也就是当且仅当 $x$ 满足所谓的**正规方程**（normal equations）

$$
A^TAx=A^Tb,
$$

这个方程总有解。由于假设 $A$ 的各列线性无关，最小二乘逼近问题有唯一解 $x=(A^TA)^{-1}A^Tb$。

#### Chebyshev 逼近或极小极大逼近

使用 $\ell_\infty$ 范数时，范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_\infty=\max\{|r_1|,\ldots,|r_m|\}
\end{array}
$$

称为 **Chebyshev 逼近问题**，或**极小极大逼近问题**（minimax approximation problem），因为我们要最小化残差的最大绝对值。Chebyshev 逼近问题可以写成 LP

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & -t\mathbf{1}\preceq Ax-b\preceq t\mathbf{1},
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}$。

<!-- pdf-page: 308 -->

#### 残差绝对值之和逼近

使用 $\ell_1$ 范数时，范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_1=|r_1|+\cdots+|r_m|
\end{array}
$$

称为**残差（绝对值）之和逼近问题**；在估计的语境中，它也称为一种**鲁棒估计器**（原因稍后就会说明）。与 Chebyshev 逼近问题一样，$\ell_1$ 范数逼近问题可以写成 LP

$$
\begin{array}{ll}
\text{最小化} & \mathbf{1}^Tt\\
\text{约束条件} & -t\preceq Ax-b\preceq t,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}^m$。

### 6.1.2 罚函数逼近

在 $\ell_p$ 范数逼近中，对于 $1\leq p<\infty$，目标函数是

$$
\left(|r_1|^p+\cdots+|r_m|^p\right)^{1/p}.
$$

与最小二乘问题一样，可以考虑目标函数为

$$
|r_1|^p+\cdots+|r_m|^p
$$

的等价问题。这个目标函数是残差的可分离对称函数。特别地，目标函数只取决于残差的**取值分布**（amplitude distribution），也就是按顺序排列后的残差。

下面考虑 $\ell_p$ 范数逼近问题的一种有用推广，其目标函数同样只取决于残差的取值分布。**罚函数逼近问题**具有如下形式：

$$
\begin{array}{ll}
\text{最小化} & \phi(r_1)+\cdots+\phi(r_m)\\
\text{约束条件} & r=Ax-b,
\end{array}
\tag{6.2}
$$

其中 $\phi:\mathbf{R}\to\mathbf{R}$ 称为（残差）**罚函数**。假设 $\phi$ 为凸函数，因此罚函数逼近问题是凸优化问题。在许多情形下，罚函数 $\phi$ 是对称、非负的，并满足 $\phi(0)=0$，但下面的分析不会用到这些性质。

#### 解释

罚函数逼近问题 (6.2) 可以作如下解释。选定 $x$ 后，就得到了用来逼近 $b$ 的 $Ax$，以及相应的残差向量 $r$。罚函数对残差的每个分量给出一个代价或惩罚 $\phi(r_i)$；总惩罚是各残差所受惩罚的总和，即 $\phi(r_1)+\cdots+\phi(r_m)$。不同的 $x$ 会产生不同的残差，因而产生不同的总惩罚。在罚函数逼近问题中，我们最小化残差带来的总惩罚。

<!-- pdf-page: 309 -->

<figure id="fig-6-1" data-figure="6.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-1.png" alt="二次罚函数、死区线性罚函数和对数障碍罚函数的曲线比较；三条曲线关于纵轴对称，在原点附近的形状及远离原点时的增长速度不同" data-source-page="309" data-source-rect="159,121,440,307">
<figcaption>图 6.1 几种常见的罚函数：二次罚函数 $\phi(u)=u^2$、死区宽度为 $a=1/4$ 的死区线性罚函数，以及界限为 $a=1$ 的对数障碍罚函数。</figcaption>
<p class="figure-translation">图内文字：log barrier——对数障碍；quadratic——二次；deadzone-linear——死区线性。</p>
</figure>

<div class="example" markdown="1">

**例 6.1 几种常见的罚函数及相应的逼近问题。**

- 取 $\phi(u)=|u|^p$，其中 $p\geq1$，罚函数逼近问题就等价于 $\ell_p$ 范数逼近问题。特别地，二次罚函数 $\phi(u)=u^2$ 给出最小二乘逼近，即欧几里得范数逼近；绝对值罚函数 $\phi(u)=|u|$ 则给出 $\ell_1$ 范数逼近。

- **死区线性罚函数**（deadzone-linear penalty function，死区宽度为 $a>0$）定义为

    $$
    \phi(u)=\begin{cases}
    0 & |u|\leq a,\\
    |u|-a & |u|>a.
    \end{cases}
    $$

    死区线性函数不惩罚幅值小于 $a$ 的残差。

- **对数障碍罚函数**（log barrier penalty function，界限为 $a>0$）具有如下形式：

    $$
    \phi(u)=\begin{cases}
    -a^2\log(1-(u/a)^2) & |u|<a,\\
    \infty & |u|\geq a.
    \end{cases}
    $$

    对数障碍罚函数对幅值大于 $a$ 的残差施加无穷大的惩罚。

图 6.1 画出了一个死区线性罚函数、一个对数障碍罚函数和一个二次罚函数。注意，当 $|u/a|\leq0.25$ 时，对数障碍函数与二次罚函数非常接近（见习题 6.1）。

</div>

将罚函数乘以一个正数不会影响罚函数逼近问题的解，因为这只是把目标<!-- pdf-page: 310 -->函数作了相同倍数的缩放。但是，罚函数的形状对罚函数逼近问题的解有很大影响。粗略地说，$\phi(u)$ 衡量我们对取值为 $u$ 的残差有多么不满意。如果在 $u$ 较小时，$\phi$ 非常小（甚至为零），就表示我们很少在意（或者完全不在意）残差取这些值。如果 $u$ 变大时 $\phi(u)$ 迅速增长，就表示我们很不希望出现大残差；如果 $\phi$ 在某个区间之外变成无穷大，就表示不能接受区间之外的残差。这种简单的解释既有助于理解罚函数逼近问题的解，也能指导我们选择罚函数。

例如，比较 $\ell_1$ 范数逼近与 $\ell_2$ 范数逼近，它们分别对应罚函数 $\phi_1(u)=|u|$ 和 $\phi_2(u)=u^2$。当 $|u|=1$ 时，两个罚函数施加相同的惩罚。当 $u$ 较小时，有 $\phi_1(u)\gg\phi_2(u)$，因此与 $\ell_2$ 范数逼近相比，$\ell_1$ 范数逼近相对更重视小残差。当 $u$ 较大时，有 $\phi_2(u)\gg\phi_1(u)$，因此与 $\ell_2$ 范数逼近相比，$\ell_1$ 范数逼近赋予大残差较小的权重。这种对大小残差赋予不同相对权重的差异，会反映在相应逼近问题的解中。与 $\ell_2$ 范数逼近的解相比，$\ell_1$ 范数逼近问题的最优残差取值分布往往包含更多零残差和非常小的残差。相反，$\ell_2$ 范数逼近的解往往包含相对较少的大残差（因为大残差在 $\ell_2$ 范数逼近中受到的惩罚远大于在 $\ell_1$ 范数逼近中受到的惩罚）。

#### 例子

下面用一个例子说明这些想法。取矩阵 $A\in\mathbf{R}^{100\times30}$ 和向量 $b\in\mathbf{R}^{100}$（随机选取，但结果具有代表性），计算 $Ax\approx b$ 的 $\ell_1$ 范数与 $\ell_2$ 范数近似解，以及采用死区线性罚函数（$a=0.5$）和对数障碍罚函数（$a=1$）的罚函数逼近。图 6.2 给出了这四种罚函数，以及这四种罚函数逼近所得最优残差的取值分布。观察罚函数的图像，可以注意到：

- $\ell_1$ 范数罚函数赋予小残差的权重最大，赋予大残差的权重最小。

- $\ell_2$ 范数罚函数赋予小残差很小的权重，却赋予大残差很大的权重。

- 死区线性罚函数对幅值小于 $0.5$ 的残差不赋予权重，对大残差也只赋予相对较小的权重。

- 对于小残差，对数障碍罚函数的权重与 $\ell_2$ 范数罚函数非常接近；但对于幅值超过约 $0.8$ 的残差，它赋予很大的权重，对于幅值超过 $1$ 的残差，则赋予无穷大的权重。

从取值分布可以清楚地看出几个特点：

<ul id="penalty-observations-start">
<li>对于 $\ell_1$ 最优解，许多残差为零或非常小。$\ell_1$ 最优解也有相对更多的大残差。</li>
</ul>

<!-- pdf-page: 311 -->

<figure id="fig-6-2" data-figure="6.2" data-reader-after="penalty-observations-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-2.png" alt="四幅上下排列的残差直方图，分别对应 p=1、p=2、死区和对数障碍罚函数；各图叠加罚函数曲线，最下图另以虚线表示二次罚函数" data-source-page="311" data-source-rect="116,248,445,512">
<figcaption>图 6.2 采用四种罚函数时，残差取值的直方图。图中还画出了经缩放的罚函数，供对照。在对数障碍罚函数对应的图中，还用虚线画出了二次罚函数。</figcaption>
<p class="figure-translation">图内文字：Deadzone——死区；Log barrier——对数障碍。</p>
</figure>

<!-- pdf-page: 312 -->

<figure id="fig-6-3" data-figure="6.3" data-no-english-text="true" data-reader-after="penalty-observations-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-3.png" alt="在负一到一之间为二次曲线、两侧保持为一的非凸罚函数，横轴为 u，纵轴为罚函数值" data-source-page="312" data-source-rect="229,120,434,277">
<figcaption>图 6.3 一种（非凸）罚函数，对幅值超过某个阈值（本例中为 1）的残差施加固定惩罚：当 $|u|\leq1$ 时，$\phi(u)=u^2$；当 $|u|>1$ 时，$\phi(u)=1$。因此，采用这个函数进行罚函数逼近时，对离群点相对不敏感。</figcaption>
</figure>

<ul id="penalty-observations-end" data-reader-continue="penalty-observations-start">
<li>$\ell_2$ 范数逼近有许多大小适中的残差，较大的残差相对较少。</li>
<li>对于死区线性罚函数，可以看到许多残差的取值为 $\pm0.5$，恰好位于不受惩罚的“免费”区域的边缘。</li>
<li>对于对数障碍罚函数，可以看到没有残差的幅值大于 $1$，但除此之外，残差分布与 $\ell_2$ 范数逼近的残差分布相似。</li>
</ul>

#### 对离群点或大误差的敏感性

在估计或回归的语境中，**离群点**（outlier）是噪声 $v_i$ 相对较大的测量值 $y_i=a_i^Tx+v_i$。它通常与错误的数据或有缺陷的测量有关。出现离群点时，$x$ 的任意估计都会对应一个含有某些大分量的残差向量。理想情况下，我们希望猜出哪些测量值是离群点，并将其从估计过程中去掉，或者在构造估计时大幅降低其权重。（不过，不能对非常大的残差施加零惩罚，因为这样最优点很可能会使所有残差都变得很大，从而让总惩罚为零。）可以采用罚函数逼近来实现这种想法，例如使用图 6.3 所示的罚函数

$$
\phi(u)=\begin{cases}
u^2 & |u|\leq M,\\
M^2 & |u|>M.
\end{cases}
\tag{6.3}
$$

<p id="outlier-penalty-start">对于幅值小于 $M$ 的残差，这个罚函数与最小二乘的罚函数相同；对于幅值大于 $M$ 的残差，不论大出多少，它都赋予固定的权重。换言之，幅值大于 $M$ 的残差被忽略了；它们被认为对应离群点或错误数据。遗憾的是，罚函数</p>

<!-- pdf-page: 313 -->

<figure id="fig-6-4" data-figure="6.4" data-no-english-text="true" data-reader-after="outlier-penalty-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-4.png" alt="Huber 罚函数的实线曲线，在中心区域为二次函数，两侧线性增长；两侧的直线段向中央以虚线延伸" data-source-page="313" data-source-rect="177,120,380,277">
<figcaption>图 6.4 实线表示 $M=1$ 时的鲁棒最小二乘罚函数，也称 Huber 罚函数 $\phi_{\mathrm{hub}}$。当 $|u|\leq M$ 时，它是二次函数；当 $|u|>M$ 时，它线性增长。</figcaption>
</figure>

<p id="outlier-penalty-end" data-reader-continue="outlier-penalty-start">(6.3) 不是凸函数，相应的罚函数逼近问题就成了一个难解的组合优化问题。</p>

基于罚函数的估计方法对离群点有多敏感，取决于罚函数在大残差处的（相对）取值。如果限定使用凸罚函数（这样得到的是凸优化问题），那么敏感性最低的函数，是那些在 $u$ 很大时 $\phi(u)$ 线性增长，即像 $|u|$ 一样增长的函数。具有这种性质的罚函数有时称为**鲁棒**罚函数，因为与最小二乘等方法相比，相应的罚函数逼近方法对离群点或大误差的敏感性低得多。

鲁棒罚函数的一个明显例子是 $\phi(u)=|u|$，它对应 $\ell_1$ 范数逼近。另一个例子是**鲁棒最小二乘罚函数**，也称 **Huber 罚函数**，定义为

$$
\phi_{\mathrm{hub}}(u)=\begin{cases}
u^2 & |u|\leq M,\\
M(2|u|-M) & |u|>M,
\end{cases}
\tag{6.4}
$$

如图 6.4 所示。这个罚函数对幅值小于 $M$ 的残差采用与最小二乘罚函数相同的惩罚，对更大的残差则转为类似 $\ell_1$ 的线性增长。Huber 罚函数可以在如下意义下看成离群点罚函数 (6.3) 的凸逼近：两者在 $|u|\leq M$ 时相同；在 $|u|>M$ 时，Huber 罚函数是最接近离群点罚函数 (6.3) 的凸函数。

<div class="example" markdown="1">

**例 6.2 鲁棒回归。** 图 6.5 给出了平面中的 $42$ 个点 $(t_i,y_i)$，其中有两个明显的离群点（一个在左上方，另一个在右下方）。虚线表示用直线 $f(t)=\alpha+\beta t$ 对这些点进行最小二乘逼近的结果。系数 $\alpha$ 和 $\beta$ 通过求解最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^{42}(y_i-\alpha-\beta t_i)^2
\end{array}
$$

<!-- pdf-page: 314 -->

<figure id="fig-6-5" data-figure="6.5" data-no-english-text="true" data-reader-after="robust-regression-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-5.png" alt="四十二个圆圈表示数据点，左上和右下各有一个离群点；最小二乘拟合虚线偏向离群点，鲁棒最小二乘拟合实线更贴近其余数据点" data-source-page="314" data-source-rect="216,121,448,306">
<figcaption>图 6.5 42 个圆圈表示数据点；除了左上方和右下方的两个离群点外，这些点都可以用一个仿射函数很好地逼近。虚线是用直线 $f(t)=\alpha+\beta t$ 对这些点进行最小二乘拟合的结果，它偏离了大多数数据点所在的位置，转向了离群点。实线表示通过最小化 $M=1$ 时的 Huber 罚函数得到的鲁棒最小二乘拟合。这种拟合对非离群数据的效果好得多。</figcaption>
</figure>

得到，其中变量为 $\alpha$ 和 $\beta$。最小二乘逼近显然偏离了大多数数据点所在的位置，转向了两个离群点。

实线表示通过最小化 Huber 罚函数得到的鲁棒最小二乘逼近：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^{42}\phi_{\mathrm{hub}}(y_i-\alpha-\beta t_i),
\end{array}
$$

<p id="robust-regression-end">其中 $M=1$。这种逼近受离群点的影响小得多。</p>

</div>

由于 $\ell_1$ 范数逼近是对离群点最具鲁棒性的（凸）罚函数逼近方法之一，因此有时也称为**鲁棒估计**或**鲁棒回归**。$\ell_1$ 范数估计的鲁棒性也可以在统计框架下理解；见第 353 页。

#### 小残差与 $\ell_1$ 范数逼近

也可以把注意力放在小残差上。最小二乘逼近赋予小残差很小的权重，因为当 $u$ 很小时，$\phi(u)=u^2$ 非常小。死区线性罚函数等函数对小残差赋予零权重。如果一个罚函数在残差较小时非常小，那么可以预期，最优残差会较小，但不会非常小。粗略地说，这时几乎没有动力，甚至完全没有动力，去让已经较小的残差进一步变小。

相反，对小残差赋予相对较大权重的罚函数，例如与 $\ell_1$ 范数逼近对应的 $\phi(u)=|u|$，往往会产生<!-- pdf-page: 315 -->许多非常小、甚至恰好为零的最优残差。这意味着，在 $\ell_1$ 范数逼近中，通常会发现许多方程被精确满足，即对于许多 $i$，都有 $a_i^Tx=b_i$。图 6.2 中可以看到这种现象。

### 6.1.3 带约束的逼近

可以在基本范数逼近问题 (6.1) 中加入约束。如果这些约束是凸的，得到的问题就是凸问题。约束的来源有很多。

- 在逼近问题中，约束可以用来排除向量 $b$ 的某些不可接受的逼近，或者确保逼近向量 $Ax$ 满足某些性质。

- 在估计问题中，约束来自关于待估计向量 $x$ 的先验知识，或者来自关于估计误差 $v$ 的先验知识。

- 在几何问题中，当要确定点 $b$ 在比子空间更复杂的集合（例如锥或多面体）上的投影时，也会出现约束。

下面用几个例子说明。

#### 变量的非负约束

可以在基本范数逼近问题中加入约束 $x\succeq0$：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|\\
\text{约束条件} & x\succeq0.
\end{array}
$$

在估计问题中，如果已知待估计的参数向量 $x$ 非负，例如它表示功率、强度或速率，就会出现非负约束。其几何解释是：确定向量 $b$ 在由 $A$ 的各列生成的锥上的投影。也可以把这个问题解释为：用 $A$ 各列的非负线性组合（即锥组合）来逼近 $b$。

#### 变量的上下界

这里加入约束 $l\preceq x\preceq u$，其中 $l,u\in\mathbf{R}^n$ 是问题参数：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|\\
\text{约束条件} & l\preceq x\preceq u.
\end{array}
$$

在估计问题中，变量的上下界来自关于各变量所在区间的先验知识。其几何解释是：求向量 $b$ 在一个盒经过 $A$ 所定义的线性映射后所得像集上的投影。

<!-- pdf-page: 316 -->

#### 概率分布

可以要求 $x$ 满足约束 $x\succeq0$、$\mathbf{1}^Tx=1$：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|\\
\text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1.
\end{array}
$$

估计比例或相对频率时就会出现这种约束，因为它们非负且总和为一。也可以把它解释为用 $A$ 各列的凸组合来逼近 $b$。（§7.2 将更详细地讨论概率估计。）

#### 范数球约束

可以在基本范数逼近问题中加入约束，要求 $x$ 位于一个范数球内：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|\\
\text{约束条件} & \|x-x_0\|\leq d,
\end{array}
$$

其中 $x_0$ 和 $d$ 是问题参数。加入这种约束可以有多种原因。

- 在估计问题中，$x_0$ 是对参数 $x$ 的先验猜测，$d$ 则是我们认为估计值偏离先验猜测的最大合理幅度。对参数 $x$ 的估计值 $\widehat x$，是在所有合理候选值（即满足 $\|z-x_0\|\leq d$ 的 $z$）中，与测量数据最吻合的值（即使 $\|Az-b\|$ 最小的值）。

- 约束 $\|x-x_0\|\leq d$ 可以表示一个**信赖域**（trust region）。这里，线性关系 $y=Ax$ 只是某个非线性关系 $y=f(x)$ 的近似，并且只有在 $x$ 接近某点 $x_0$，具体地说，满足 $\|x-x_0\|\leq d$ 时才有效。问题是最小化 $\|Ax-b\|$，但只在模型 $y=Ax$ 可以信赖的那些 $x$ 上进行。

这些想法也会出现在正则化中；见 §6.3.2。

## 6.2 最小范数问题

基本的**最小范数问题**具有如下形式：

$$
\begin{array}{ll}
\text{最小化} & \|x\|\\
\text{约束条件} & Ax=b,
\end{array}
\tag{6.5}
$$

其中数据为 $A\in\mathbf{R}^{m\times n}$ 和 $b\in\mathbf{R}^m$，变量为 $x\in\mathbf{R}^n$，$\|\cdot\|$ 是 $\mathbf{R}^n$ 上的一个范数。只要线性方程 $Ax=b$ 有解，这个问题就总有解；其解称为 $Ax=b$ 的一个**最小范数解**。最小范数问题当然是一个凸优化问题。

不失一般性，可以假设 $A$ 的各行线性无关，因此 $m\leq n$。当 $m=n$ 时，唯一的可行点是 $x=A^{-1}b$；只有在 $m<n$ 时，即方程 $Ax=b$ 欠定时，最小范数问题才有研究意义。

<!-- pdf-page: 317 -->

### 改写为范数逼近问题

通过消去等式约束，可以把最小范数问题 (6.5) 写成范数逼近问题。设 $x_0$ 是 $Ax=b$ 的任意一个解，矩阵 $Z\in\mathbf{R}^{n\times k}$ 的各列构成 $A$ 的零空间的一组基。于是 $Ax=b$ 的通解可以表示为 $x_0+Zu$，其中 $u\in\mathbf{R}^k$。最小范数问题 (6.5) 可以写成

$$
\begin{array}{ll}
\text{最小化} & \|x_0+Zu\|,
\end{array}
$$

其中变量为 $u\in\mathbf{R}^k$；这就是一个范数逼近问题。特别地，对范数逼近问题的分析和讨论，在作出适当解释后，也适用于最小范数问题。

### 控制或设计的解释

最小范数问题 (6.5) 可以解释为一个最优设计或最优控制问题。$n$ 个变量 $x_1,\ldots,x_n$ 是待确定取值的**设计变量**。在控制问题中，变量 $x_1,\ldots,x_n$ 表示**输入**，其取值由我们选择。向量 $y=Ax$ 给出设计 $x$ 的 $m$ 个属性或结果，假设它们都是设计变量 $x$ 的线性函数。$m<n$ 个方程 $Ax=b$ 表示对设计的 $m$ 项指标或要求。由于 $m<n$，这些要求不足以完全确定设计；设计中还有 $n-m$ 个自由度（假设 $A$ 的秩为 $m$）。

在所有满足指标的设计中，最小范数问题选择按范数 $\|\cdot\|$ 衡量最小的设计。这可以看成效率最高的设计，因为它用尽可能小的 $x$ 达到了指标 $Ax=b$。

### 估计的解释

假设 $x$ 是待估计的参数向量。我们拥有 $m<n$ 个完全准确（无噪声）的线性测量，由 $Ax=b$ 给出。由于测量数量少于待估计参数的数量，这些测量不能完全确定 $x$。任何满足 $Ax=b$ 的参数向量 $x$ 都与测量相符。

要在不增加测量的情况下对 $x$ 作出好的猜测，就必须利用先验信息。假设先验信息或先验假设是：$x$（按 $\|\cdot\|$ 衡量）较小比它较大更有可能。最小范数问题从所有与测量 $Ax=b$ 相符的参数向量中，选择最小的向量（因此也就是最可信的向量），作为参数向量 $x$ 的估计。（关于最小范数问题的统计解释，见第 359 页。）

### 几何解释

最小范数问题 (6.5) 也有一个简单的几何解释。可行集 $\{x\mid Ax=b\}$ 是仿射集，目标函数是 $x$ 与点 $0$ 之间的距离（用范数 $\|\cdot\|$ 衡量）。最小范数问题寻找<!-- pdf-page: 318 -->仿射集中距离 $0$ 最近的点，即确定点 $0$ 在仿射集 $\{x\mid Ax=b\}$ 上的投影。

### 线性方程的最小二乘解

最常见的最小范数问题使用欧几里得范数，即 $\ell_2$ 范数。将目标函数平方，得到等价问题

$$
\begin{array}{ll}
\text{最小化} & \|x\|_2^2\\
\text{约束条件} & Ax=b,
\end{array}
$$

其唯一解称为方程 $Ax=b$ 的**最小二乘解**。与最小二乘逼近问题一样，这个问题可以解析求解。引入对偶变量 $\nu\in\mathbf{R}^m$，最优性条件为

$$
2x^\star+A^T\nu^\star=0,\qquad Ax^\star=b,
$$

这是一对线性方程，很容易求解。由第一个方程得到 $x^\star=-(1/2)A^T\nu^\star$；代入第二个方程，得到 $-(1/2)AA^T\nu^\star=b$，从而有

$$
\nu^\star=-2(AA^T)^{-1}b,\qquad x^\star=A^T(AA^T)^{-1}b.
$$

（由于 $\operatorname{\mathbf{rank}}A=m<n$，矩阵 $AA^T$ 可逆。）

### 最小惩罚问题

最小范数问题 (6.5) 的一种有用变体是**最小惩罚问题**：

$$
\begin{array}{ll}
\text{最小化} & \phi(x_1)+\cdots+\phi(x_n)\\
\text{约束条件} & Ax=b,
\end{array}
\tag{6.6}
$$

其中 $\phi:\mathbf{R}\to\mathbf{R}$ 是凸的、非负的，并满足 $\phi(0)=0$。罚函数值 $\phi(u)$ 量化了我们对 $x$ 的某个分量取值为 $u$ 有多么不满意；最小惩罚问题在约束 $Ax=b$ 下，寻找总惩罚最小的 $x$。

把（罚函数逼近问题中的）残差 $r$ 的取值分布，替换为（最小惩罚问题中的）$x$ 的取值分布，就可以将罚函数逼近中关于罚函数的所有讨论和解释转用于最小惩罚问题。

### 通过最小 $\ell_1$ 范数求稀疏解

回顾第 300 页的讨论：$\ell_1$ 范数逼近赋予小残差相对较大的权重，因此会使许多最优残差很小，甚至为零。最小范数问题中也会出现类似的效果。最小 $\ell_1$ 范数问题

$$
\begin{array}{ll}
\text{最小化} & \|x\|_1\\
\text{约束条件} & Ax=b
\end{array}
$$

往往会产生含有大量零分量的解 $x$。换言之，最小 $\ell_1$ 范数问题往往会产生 $Ax=b$ 的**稀疏解**，通常含有 $m$ 个非零分量。

<!-- pdf-page: 319 -->

找到只有 $m$ 个非零分量的 $Ax=b$ 的解并不难。从 $1,\ldots,n$ 中任选 $m$ 个指标，作为 $x$ 的非零分量的位置。方程 $Ax=b$ 就简化为 $\widetilde A\widetilde x=b$，其中 $\widetilde A$ 是从 $A$ 中只选取这些列得到的 $m\times m$ 子矩阵，$\widetilde x\in\mathbf{R}^m$ 是由 $x$ 中选定的 $m$ 个分量构成的子向量。如果 $\widetilde A$ 非奇异，就可以取 $\widetilde x=\widetilde A^{-1}b$，由此得到一个含有不超过 $m$ 个非零分量的可行解 $x$。如果 $\widetilde A$ 奇异且 $b\notin\mathcal{R}(\widetilde A)$，则方程 $\widetilde A\widetilde x=b$ 无解，意味着不存在具有所选非零分量位置的可行 $x$。如果 $\widetilde A$ 奇异且 $b\in\mathcal{R}(\widetilde A)$，则存在一个非零分量少于 $m$ 个的可行解。

这种方法可以用来寻找具有 $m$ 个（或更少）非零分量的最小 $x$，但一般需要考察并比较从 $x$ 的 $n$ 个系数中选取 $m$ 个非零系数的全部 $n!/(m!(n-m)!)$ 种选择。另一方面，求解最小 $\ell_1$ 范数问题，则为寻找 $Ax=b$ 的一个既稀疏又较小的解提供了一种有效的启发式方法。

## 6.3 正则化逼近

### 6.3.1 双准则表述

正则化逼近的基本形式，是寻找一个向量 $x$，既让它本身较小（如果可能），又让残差 $Ax-b$ 较小。这很自然地可以描述为一个具有两个目标 $\|Ax-b\|$ 和 $\|x\|$ 的（凸）向量优化问题：

$$
\begin{array}{ll}
\text{最小化（关于 }\mathbf{R}_+^2\text{）} & (\|Ax-b\|,\|x\|).
\end{array}
\tag{6.7}
$$

这里的两个范数可以不同：第一个是 $\mathbf{R}^m$ 上的范数，用来衡量残差的大小；第二个是 $\mathbf{R}^n$ 上的范数，用来衡量 $x$ 的大小。

两个目标之间的最优权衡可以用多种方法求得。随后可以画出 $\|Ax-b\|$ 与 $\|x\|$ 之间的最优权衡曲线，它表示为了使一个目标较小，另一个目标必须增大到什么程度。$\|Ax-b\|$ 与 $\|x\|$ 之间的最优权衡曲线有一个端点很容易描述。$\|x\|$ 的最小值为零，并且仅当 $x=0$ 时达到。对于这个 $x$，残差范数的值为 $\|b\|$。

权衡曲线的另一个端点描述起来较复杂。用 $C$ 表示使 $\|Ax-b\|$ 最小的点所构成的集合（不对 $\|x\|$ 施加约束）。那么，$C$ 中任意一个范数最小的点都是 Pareto 最优点，对应权衡曲线的另一个端点。换言之，这个端点所对应的 Pareto 最优点，是在所有使 $\|Ax-b\|$ 最小的点中，范数最小的那些点。如果两个范数都是欧几里得范数，这个 Pareto 最优点是唯一的，由 $x=A^\dagger b$ 给出，其中 $A^\dagger$ 是 $A$ 的伪逆。（见第 184 页的 §4.7.6，以及 §A.5.4。）

<!-- pdf-page: 320 -->

### 6.3.2 正则化

**正则化**（regularization）是求解双准则问题 (6.7) 的一种常用标量化方法。正则化的一种形式是最小化两个目标的加权和：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|+\gamma\|x\|,
\end{array}
\tag{6.8}
$$

其中 $\gamma>0$ 是问题参数。当 $\gamma$ 在 $(0,\infty)$ 上变化时，(6.8) 的解描出最优权衡曲线。

另一种常见的正则化方法，尤其是在采用欧几里得范数时，是对不同的 $\delta>0$，最小化范数平方的加权和，即

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|^2+\delta\|x\|^2.
\end{array}
\tag{6.9}
$$

这些正则化逼近问题都通过添加一个与 $x$ 的范数有关的附加项或惩罚项，来解决同时使 $\|Ax-b\|$ 和 $\|x\|$ 较小的双准则问题。

#### 解释

正则化应用于多种场合。在估计问题中，惩罚较大 $\|x\|$ 的附加项，可以解释为我们事先知道 $\|x\|$ 不会太大。在最优设计问题中，附加项把使用较大设计变量的代价，加到未达到目标指标的代价上。

要求 $\|x\|$ 较小也可能是出于建模方面的考虑。例如，$y=Ax$ 可能只是 $x$ 与 $y$ 之间真实关系 $y=f(x)$ 的一个较好近似。为了使 $f(x)\approx b$，我们希望 $Ax\approx b$，同时也需要 $x$ 较小，以保证 $f(x)\approx Ax$。

在 §6.4.1 和 §6.4.2 中将会看到，正则化可以用来考虑矩阵 $A$ 的变化。粗略地说，当 $x$ 较大时，$A$ 的变化会导致 $Ax$ 发生较大变化，因此应当避免这样的 $x$。

当矩阵 $A$ 是方阵、目标是求解线性方程 $Ax=b$ 时，也会使用正则化。如果 $A$ 的条件很差，甚至是奇异的，正则化就会在求解方程（即使 $\|Ax-b\|$ 为零）与将 $x$ 的大小保持在合理范围内之间作出折中。

正则化也出现在统计问题中；见 §7.1.2。

#### Tikhonov 正则化

最常见的正则化形式以 (6.9) 为基础，并使用欧几里得范数，从而得到一个（凸）二次优化问题：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2+\delta\|x\|_2^2=x^T(A^TA+\delta I)x-2b^TAx+b^Tb.
\end{array}
\tag{6.10}
$$

这个 **Tikhonov 正则化**问题的解析解为

$$
x=(A^TA+\delta I)^{-1}A^Tb.
$$

由于对任意 $\delta>0$ 都有 $A^TA+\delta I\succ0$，Tikhonov 正则化最小二乘解不要求对矩阵 $A$ 的秩（或维度）作任何假设。

<!-- pdf-page: 321 -->

#### 平滑正则化

正则化的想法，即在目标函数中加入惩罚较大 $x$ 的一项，可以向多个方向扩展。一种有用的扩展是加入形如 $\|Dx\|$ 的正则化项，来代替 $\|x\|$。在许多应用中，矩阵 $D$ 表示一个近似微分算子或近似二阶微分算子，因此 $\|Dx\|$ 衡量的是 $x$ 的变化程度或平滑程度。

例如，假设向量 $x\in\mathbf{R}^n$ 表示某个连续物理参数（例如温度）在区间 $[0,1]$ 上的取值：$x_i$ 是点 $i/n$ 处的温度。这个参数在 $i/n$ 附近的梯度或一阶导数，可以简单地用 $n(x_{i+1}-x_i)$ 近似；其二阶导数可以简单地用二阶差分

$$
n\bigl(n(x_{i+1}-x_i)-n(x_i-x_{i-1})\bigr)=n^2(x_{i+1}-2x_i+x_{i-1})
$$

近似。如果 $\Delta$ 是（三对角 Toeplitz）矩阵

$$
\Delta=n^2\begin{bmatrix}
1&-2&1&0&\cdots&0&0&0&0\\
0&1&-2&1&\cdots&0&0&0&0\\
0&0&1&-2&\cdots&0&0&0&0\\
\vdots&\vdots&\vdots&\vdots&&\vdots&\vdots&\vdots&\vdots\\
0&0&0&0&\cdots&-2&1&0&0\\
0&0&0&0&\cdots&1&-2&1&0\\
0&0&0&0&\cdots&0&1&-2&1
\end{bmatrix}\in\mathbf{R}^{(n-2)\times n},
$$

那么 $\Delta x$ 就表示该参数二阶导数的近似，因此 $\|\Delta x\|_2^2$ 可以衡量这个参数在区间 $[0,1]$ 上的均方曲率。

Tikhonov 正则化问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2+\delta\|\Delta x\|_2^2
\end{array}
$$

可以用来在两个目标之间作权衡：$\|Ax-b\|_2^2$ 可能衡量拟合程度或与实验数据的一致程度；$\|\Delta x\|_2^2$ 则（近似地）表示所研究物理参数的均方曲率。参数 $\delta$ 用于控制所需的正则化程度，或者用于画出拟合程度与平滑程度之间的最优权衡曲线。

也可以加入多个正则化项。例如，可以同时加入与平滑程度及大小有关的项：

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2^2+\delta\|\Delta x\|_2^2+\eta\|x\|_2^2.
\end{array}
$$

这里，参数 $\delta\geq0$ 用于控制近似解的平滑程度，参数 $\eta\geq0$ 用于控制近似解的大小。

<div class="example" markdown="1">

**例 6.3 最优输入设计。** 考虑一个动态系统，其标量输入序列为 $u(0),u(1),\ldots,u(N)$，标量输出序列为 $y(0),y(1),\ldots,y(N)$，两者由卷积关系联系：

$$
y(t)=\sum_{\tau=0}^t h(\tau)u(t-\tau),\qquad t=0,1,\ldots,N.
$$

<!-- pdf-page: 322 -->

序列 $h(0),h(1),\ldots,h(N)$ 称为系统的**卷积核**或**脉冲响应**。

我们的目标是选择输入序列 $u$，实现以下几个目标。

- **输出跟踪。** 首要目标是让输出 $y$ 跟踪或跟随期望的目标信号或参考信号 $y_{\mathrm{des}}$。用二次函数

    $$
    J_{\mathrm{track}}=\frac{1}{N+1}\sum_{t=0}^N(y(t)-y_{\mathrm{des}}(t))^2
    $$

    衡量输出跟踪误差。

- **输入较小。** 输入不应过大。用二次函数

    $$
    J_{\mathrm{mag}}=\frac{1}{N+1}\sum_{t=0}^N u(t)^2
    $$

    衡量输入的大小。

- **输入变化较小。** 输入不应快速变化。用二次函数

    $$
    J_{\mathrm{der}}=\frac{1}{N}\sum_{t=0}^{N-1}(u(t+1)-u(t))^2
    $$

    衡量输入变化的大小。

通过最小化加权和

$$
J_{\mathrm{track}}+\delta J_{\mathrm{der}}+\eta J_{\mathrm{mag}},
$$

其中 $\delta>0$、$\eta>0$，就可以在这三个目标之间作权衡。

现在考虑一个具体例子，其中 $N=200$，脉冲响应为

$$
h(t)=\frac{1}{9}(0.9)^t(1-0.4\cos(2t)).
$$

图 6.6 给出了正则化参数 $\delta$ 和 $\eta$ 取三组值时的最优输入及相应输出（并画出期望轨迹 $y_{\mathrm{des}}$）。第一行表示 $\delta=0$、$\eta=0.005$ 时的最优输入及相应输出。这时对输入大小作了一定正则化，但没有对输入变化作正则化。虽然跟踪效果很好（即 $J_{\mathrm{track}}$ 很小），所需输入却很大，而且变化很快。第二行对应 $\delta=0$、$\eta=0.05$。这时对输入大小施加了更强的正则化，但仍未对 $u$ 的变化作正则化。相应输入确实变小了，代价是跟踪误差增大。最后一行表示 $\delta=0.3$、$\eta=0.05$ 时的结果。这时加入了一定程度的变化正则化。输入变化显著减小，而输出跟踪误差增加不多。

</div>

#### $\ell_1$ 范数正则化

采用 $\ell_1$ 范数进行正则化，可以作为寻找稀疏解的启发式方法。例如，考虑问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2+\gamma\|x\|_1,
\end{array}
\tag{6.11}
$$

<!-- pdf-page: 323 -->

<figure id="fig-6-6" data-figure="6.6" data-no-english-text="true" data-reader-after="sparse-regression-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-6.png" alt="三行两列的曲线图：左列为最优输入，右列为相应输出；每行对应一组正则化参数，右列的虚线为期望输出" data-source-page="323" data-source-rect="90,141,470,596">
<figcaption>图 6.6 正则化参数 $\delta$（对应输入变化）和 $\eta$（对应输入幅值）取三组值时的最优输入（左）及相应输出（右）。右侧各图中的虚线表示期望输出 $y_{\mathrm{des}}$。最上行为 $\delta=0,\ \eta=0.005$；中间行为 $\delta=0,\ \eta=0.05$；最下行为 $\delta=0.3,\ \eta=0.05$。</figcaption>
</figure>

<!-- pdf-page: 324 -->

<p id="sparse-regression-explanation" markdown="1">其中用欧几里得范数衡量残差，用 $\ell_1$ 范数进行正则化。改变参数 $\gamma$，可以描出 $\|Ax-b\|_2$ 与 $\|x\|_1$ 之间的最优权衡曲线，用它近似 $\|Ax-b\|_2$ 与向量 $x$ 的稀疏程度或基数 $\operatorname{\mathbf{card}}(x)$（即非零元素的个数）之间的最优权衡曲线。问题 (6.11) 可以改写为 SOCP 并求解。</p>

<div class="example" markdown="1">

**例 6.4 回归变量选择问题。** 给定矩阵 $A\in\mathbf{R}^{m\times n}$，其各列是候选回归变量；还给定向量 $b\in\mathbf{R}^m$，希望用 $A$ 的 $k<n$ 列的线性组合来拟合它。问题是选择要使用的 $k$ 个回归变量，以及相应的系数。这个问题可以写成

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_2\\
\text{约束条件} & \operatorname{\mathbf{card}}(x)\leq k.
\end{array}
$$

一般来说，这是一个难解的组合优化问题。

一种直接的方法是检查 $x$ 中具有 $k$ 个非零元素的所有可能稀疏模式。固定稀疏模式后，可以通过求解最小二乘问题来找到最优 $x$，即最小化 $\|\widetilde A\widetilde x-b\|_2$，其中 $\widetilde A$ 是从 $A$ 中保留与该稀疏模式对应的列得到的子矩阵，$\widetilde x$ 是由 $x$ 的非零分量组成的子向量。对具有 $k$ 个非零元素的全部 $n!/(k!(n-k)!)$ 种稀疏模式，都要这样做一次。

一种有效的启发式方法是对不同的 $\gamma$ 求解问题 (6.11)，寻找能产生满足 $\operatorname{\mathbf{card}}(x)=k$ 的解的最小 $\gamma$。随后固定这个稀疏模式，求使 $\|Ax-b\|_2$ 最小的 $x$。

图 6.7 给出了一个数值例子，其中 $A\in\mathbf{R}^{10\times20}$、$x\in\mathbf{R}^{20}$、$b\in\mathbf{R}^{10}$。虚线上的圆圈表示 $\operatorname{\mathbf{card}}(x)$（纵轴）与残差 $\|Ax-b\|_2$（横轴）之间权衡的（全局）Pareto 最优值。对每个 $k$，采用上述方法枚举所有具有 $k$ 个非零元素的稀疏模式，得到 Pareto 最优点。实线上的圆圈则用启发式方法得到：对不同的 $\gamma$，采用问题 (6.11) 的解所给出的稀疏模式。注意，当 $\operatorname{\mathbf{card}}(x)=1$ 时，启发式方法确实找到了全局最优解。

这一想法会在**基追踪**（basis pursuit，§6.5.4）中再次出现。

</div>

### 6.3.3 重构、平滑与去噪

本节介绍上述双准则逼近问题的一个重要特例，并通过几个例子说明不同正则化方法的表现。在**重构问题**中，首先有一个由向量 $x\in\mathbf{R}^n$ 表示的**信号**。系数 $x_i$ 对应某个时间函数在等间隔点处的取值（用信号处理的术语说，就是采样值）。通常假设信号不会变化得太快，也就是说，通常有 $x_i\approx x_{i+1}$。（本节考虑一维信号，例如音频信号，但同样的想法也适用于二维或更高维信号，例如图像或视频。）

<!-- pdf-page: 325 -->

<figure id="fig-6-7" data-figure="6.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-7.png" alt="稀疏回归变量选择中，非零元素个数随残差范数变化的两条阶梯曲线；虚线上的圆圈为 Pareto 最优值，实线上的圆圈为正则化启发式方法得到的点" data-source-page="325" data-source-rect="164,122,395,306.5">
<figcaption>图 6.7 矩阵 $A\in\mathbf{R}^{10\times20}$ 时的稀疏回归变量选择。虚线上的圆圈表示残差 $\|Ax-b\|_2$ 与非零元素个数 $\operatorname{\mathbf{card}}(x)$ 之间权衡的 Pareto 最优值。实线上用圆圈标出的点由 $\ell_1$ 范数正则化启发式方法得到。</figcaption>
</figure>

信号 $x$ 受到加性噪声 $v$ 的污染：

$$
x_{\mathrm{cor}}=x+v.
$$

噪声可以用许多不同方式建模，但这里仅假设噪声未知、较小，并且与信号不同，它变化很快。目标是在给定受噪声污染的信号 $x_{\mathrm{cor}}$ 的情况下，形成原信号 $x$ 的估计 $\widehat x$。这个过程称为**信号重构**（因为我们试图从受污染的信号重建原信号），或**去噪**（因为我们试图去除受污染信号中的噪声）。大多数重构方法最终都会对 $x_{\mathrm{cor}}$ 进行某种平滑操作，得到 $\widehat x$，所以这个过程也称为**平滑**。

重构问题的一种简单表述是双准则问题

$$
\begin{array}{ll}
\text{最小化（关于 }\mathbf{R}_+^2\text{）} & (\|\widehat x-x_{\mathrm{cor}}\|_2,\phi(\widehat x)),
\end{array}
\tag{6.12}
$$

其中 $\widehat x$ 是变量，$x_{\mathrm{cor}}$ 是问题参数。函数 $\phi:\mathbf{R}^n\to\mathbf{R}$ 是凸函数，称为**正则化函数**或**平滑目标函数**。它用于衡量估计 $\widehat x$ 的粗糙程度，即不平滑的程度。重构问题 (6.12) 寻找既接近受污染信号（按 $\ell_2$ 范数衡量），又平滑（即 $\phi(\widehat x)$ 较小）的信号。重构问题 (6.12) 是一个凸双准则问题。通过标量化并求解一个（标量）凸优化问题，可以找到 Pareto 最优点。

<!-- pdf-page: 326 -->

#### 二次平滑

最简单的重构方法使用**二次平滑函数**

$$
\phi_{\mathrm{quad}}(x)=\sum_{i=1}^{n-1}(x_{i+1}-x_i)^2=\|Dx\|_2^2,
$$

其中 $D\in\mathbf{R}^{(n-1)\times n}$ 是双对角矩阵

$$
D=\begin{bmatrix}
-1&1&0&\cdots&0&0&0\\
0&-1&1&\cdots&0&0&0\\
\vdots&\vdots&\vdots&&\vdots&\vdots&\vdots\\
0&0&0&\cdots&-1&1&0\\
0&0&0&\cdots&0&-1&1
\end{bmatrix}.
$$

通过最小化

$$
\|\widehat x-x_{\mathrm{cor}}\|_2^2+\delta\|D\widehat x\|_2^2,
$$

可以得到 $\|\widehat x-x_{\mathrm{cor}}\|_2$ 与 $\|D\widehat x\|_2$ 之间的最优权衡，其中 $\delta>0$ 对最优权衡曲线作参数化。这个二次问题的解为

$$
\widehat x=(I+\delta D^TD)^{-1}x_{\mathrm{cor}}.
$$

由于 $I+\delta D^TD$ 是三对角矩阵，计算这个解非常高效；见附录 C。

#### 二次平滑的例子

图 6.8 给出了一个信号 $x\in\mathbf{R}^{4000}$（上图）及受噪声污染的信号 $x_{\mathrm{cor}}$（下图）。目标 $\|\widehat x-x_{\mathrm{cor}}\|_2$ 与 $\|D\widehat x\|_2$ 之间的最优权衡曲线见图 6.9。权衡曲线最左端的点对应 $\widehat x=x_{\mathrm{cor}}$，其目标值为 $\|Dx_{\mathrm{cor}}\|_2=4.4$。最右端的点对应 $\widehat x=0$，此时 $\|\widehat x-x_{\mathrm{cor}}\|_2=\|x_{\mathrm{cor}}\|_2=16.2$。注意，权衡曲线在 $\|\widehat x-x_{\mathrm{cor}}\|_2\approx3$ 附近有一个明显的拐折。

图 6.10 给出了最优权衡曲线上的三个平滑信号，分别对应 $\|\widehat x-x_{\mathrm{cor}}\|_2=8$（上图）、$3$（中图）和 $1$（下图）。把重构信号与原信号 $x$ 比较，可以看到当 $\|\widehat x-x_{\mathrm{cor}}\|_2=3$ 时，重构效果最好，这对应权衡曲线的拐折处。$\|\widehat x-x_{\mathrm{cor}}\|_2$ 更大时，平滑过度；更小时，平滑不足。

#### 总变差重构

当原信号非常平滑、噪声变化很快时，简单的二次平滑是一种效果很好的重构方法。但是显然，原信号中的任何快速变化也会被二次平滑削弱或消除。下面介绍一种重构方法，它能去除大部分噪声，同时保留原信号中偶尔出现的快速变化。该方法基于平滑函数

$$
\phi_{\mathrm{tv}}(\widehat x)=\sum_{i=1}^{n-1}|\widehat x_{i+1}-\widehat x_i|=\|D\widehat x\|_1,
$$

<!-- pdf-page: 327 -->

<figure id="fig-6-8" data-figure="6.8" data-no-english-text="true" data-reader-after="total-variation-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-8.png" alt="上下两幅信号图：上图为包含四千个分量的平滑原始信号，下图为受噪声污染的信号，横轴均为分量索引 i" data-source-page="327" data-source-rect="134,138,436,372">
<figcaption>图 6.8 上图：原始信号 $x\in\mathbf{R}^{4000}$。下图：受噪声污染的信号 $x_{\mathrm{cor}}$。</figcaption>
</figure>

<figure id="fig-6-9" data-figure="6.9" data-no-english-text="true" data-reader-after="total-variation-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-9.png" alt="平滑程度与重构误差之间的最优权衡曲线：曲线先陡降，在横坐标约为三时明显转折，此后逐渐趋平" data-source-page="327" data-source-rect="164,452,397,635.5">
<figcaption>图 6.9 $\|D\widehat{x}\|_2$ 与 $\|\widehat{x}-x_{\mathrm{cor}}\|_2$ 之间的最优权衡曲线。曲线在 $\|\widehat{x}-x_{\mathrm{cor}}\|\approx3$ 附近有一个明显的转折。</figcaption>
</figure>

<!-- pdf-page: 328 -->

<figure id="fig-6-10" data-figure="6.10" data-no-english-text="true" data-reader-after="total-variation-explanation">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-10.png" alt="上下排列的三个平滑或重构信号，重构误差范数从上到下为八、三、一；最上图最平滑，最下图保留较多噪声" data-source-page="328" data-source-rect="185,122,487,352">
<figcaption>图 6.10 三个经过平滑或重构的信号 $\widehat{x}$。最上图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=8$，中间图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=3$，最下图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=1$。</figcaption>
</figure>

<p id="total-variation-explanation" markdown="1">它称为 $x\in\mathbf{R}^n$ 的**总变差**（total variation）。与二次平滑度量 $\phi_{\mathrm{quad}}$ 一样，总变差函数对快速变化的 $\widehat x$ 赋予较大的值。不过，总变差度量对较大的 $|x_{i+1}-x_i|$ 所施加的惩罚相对较小。</p>

#### 总变差重构的例子

图 6.11 给出了一个信号 $x\in\mathbf{R}^{2000}$（上图）及受噪声污染的信号 $x_{\mathrm{cor}}$。原信号大部分是平滑的，但有几处快速变化或数值跳变；噪声则变化很快。

先采用二次平滑。图 6.12 给出了 $\|D\widehat x\|_2$ 与 $\|\widehat x-x_{\mathrm{cor}}\|_2$ 之间最优权衡曲线上的三个平滑信号。在前两个信号中，原信号的快速变化也被平滑掉了。第三个信号较好地保留了信号中的陡峭边缘，但仍残留大量噪声。

现在展示总变差重构。图 6.13 给出了 $\|D\widehat x\|_1$ 与 $\|\widehat x-x_{\mathrm{cor}}\|_2$ 之间的最优权衡曲线。图 6.14 给出了最优权衡曲线上的重构信号，分别对应 $\|D\widehat x\|_1=5$（上图）、$\|D\widehat x\|_1=8$（中图）和 $\|D\widehat x\|_1=10$（下图）。可以看到，与二次平滑不同，总变差重构保留了信号中的突变。

<!-- pdf-page: 329 -->

<figure id="fig-6-11" data-figure="6.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-11.png" alt="上下两幅信号图：上图为主要部分平滑、在三个位置发生跳变的原始信号，下图为叠加快速变化噪声后的信号；横轴为分量索引 i" data-source-page="329" data-source-rect="134,260,436,499">
<figcaption>图 6.11 信号 $x\in\mathbf{R}^{2000}$ 及受噪声污染的信号 $x_{\mathrm{cor}}\in\mathbf{R}^{2000}$。噪声变化很快，而信号总体平滑，只有少数位置变化很快。</figcaption>
</figure>

<!-- pdf-page: 330 -->

<figure id="fig-6-12" data-figure="6.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-12.png" alt="采用二次平滑得到的三个信号：最上图噪声较小但跳变被明显抹平，最下图仍有较多噪声，中间图介于两者之间" data-source-page="330" data-source-rect="185,128,489,365">
<figcaption>图 6.12 三个经过二次平滑的信号 $\widehat{x}$。最上图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=10$，中间图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=7$，最下图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=4$。最上图大幅减小了噪声，但也过度平滑了信号中快速变化的部分。最下图中的平滑信号降噪不足，却仍然抹平了原信号中快速变化的部分。中间图中的平滑信号给出了最好的折中，但仍然抹平了快速变化的部分。</figcaption>
</figure>

<figure id="fig-6-13" data-figure="6.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-13.png" alt="信号总变差与重构误差之间的最优权衡曲线；曲线从左上方快速下降，随后逐渐趋近横轴" data-source-page="330" data-source-rect="216,476,452,664.5">
<figcaption>图 6.13 $\|D\widehat{x}\|_1$ 与 $\|\widehat{x}-x_{\mathrm{cor}}\|_2$ 之间的最优权衡曲线。</figcaption>
</figure>

<!-- pdf-page: 331 -->

<figure id="fig-6-14" data-figure="6.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-14.png" alt="采用总变差重构得到的三个信号，均保留原信号的三处跳变；最上图消除了部分缓慢变化，最下图仍有残留噪声" data-source-page="331" data-source-rect="134,250,436,477">
<figcaption>图 6.14 采用总变差重构得到的三个重构信号 $\widehat{x}$。最上图对应 $\|D\widehat{x}\|_1=5$，中间图对应 $\|D\widehat{x}\|_1=8$，最下图对应 $\|D\widehat{x}\|_1=10$。最下图的降噪还不够充分，而最上图消除了信号中一部分缓慢变化的成分。注意，与二次平滑不同，总变差重构保留了信号中的突变。</figcaption>
</figure>

<!-- pdf-page: 332 -->

## 6.4 鲁棒逼近

### 6.4.1 随机鲁棒逼近

考虑基本目标为 $\|Ax-b\|$ 的逼近问题，但还希望计入数据矩阵 $A$ 的某些不确定性或可能发生的变化。（同样的想法也可以扩展到 $A$ 和 $b$ 都有不确定性的情形。）本节考虑描述 $A$ 变化的几种统计模型。

假设 $A$ 是取值于 $\mathbf{R}^{m\times n}$ 的随机变量，均值为 $\bar A$，因此可以写成

$$
A=\bar A+U,
$$

其中 $U$ 是均值为零的随机矩阵。这里，常矩阵 $\bar A$ 给出 $A$ 的平均值，$U$ 描述其统计变化。

很自然地，可以用 $\|Ax-b\|$ 的期望作为目标函数：

$$
\begin{array}{ll}
\text{最小化} & \mathbf{E}\,\|Ax-b\|.
\end{array}
\tag{6.13}
$$

我们把这个问题称为**随机鲁棒逼近问题**。它总是一个凸优化问题，但通常难以有效求解，因为在大多数情形下，目标函数或其导数都很难计算。

随机鲁棒逼近问题 (6.13) 的一种容易求解的简单情形，是 $A$ 只取有限多个值，即

$$
\operatorname{\mathbf{prob}}(A=A_i)=p_i,\qquad i=1,\ldots,k,
$$

其中 $A_i\in\mathbf{R}^{m\times n}$、$\mathbf{1}^Tp=1$、$p\succeq0$。此时问题 (6.13) 具有如下形式：

$$
\begin{array}{ll}
\text{最小化} & p_1\|A_1x-b\|+\cdots+p_k\|A_kx-b\|,
\end{array}
$$

它通常称为**范数和问题**。这个问题可以写成

$$
\begin{array}{ll}
\text{最小化} & p^Tt\\
\text{约束条件} & \|A_ix-b\|\leq t_i,\quad i=1,\ldots,k,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}^k$。如果采用欧几里得范数，这个范数和问题就是 SOCP。如果采用 $\ell_1$ 或 $\ell_\infty$ 范数，范数和问题可以写成 LP；见习题 6.8。

随机鲁棒逼近问题 (6.13) 的一些变体可以有效求解。例如，考虑随机鲁棒最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \mathbf{E}\,\|Ax-b\|_2^2,
\end{array}
$$

其中采用欧几里得范数。目标函数可以写成

$$
\begin{aligned}
\mathbf{E}\,\|Ax-b\|_2^2
&=\mathbf{E}\,(\bar Ax-b+Ux)^T(\bar Ax-b+Ux)\\
&=(\bar Ax-b)^T(\bar Ax-b)+\mathbf{E}\,x^TU^TUx\\
&=\|\bar Ax-b\|_2^2+x^TPx,
\end{aligned}
$$

<!-- pdf-page: 333 -->

其中 $P=\mathbf{E}\,U^TU$。因此，随机鲁棒逼近问题具有正则化最小二乘问题的形式：

$$
\begin{array}{ll}
\text{最小化} & \|\bar Ax-b\|_2^2+\|P^{1/2}x\|_2^2,
\end{array}
$$

其解为

$$
x=(\bar A^T\bar A+P)^{-1}\bar A^Tb.
$$

这完全合乎道理：当矩阵 $A$ 发生变化时，$x$ 越大，向量 $Ax$ 的变化就越大；而 Jensen 不等式告诉我们，$Ax$ 的变化会增大 $\|Ax-b\|_2$ 的平均值。因此，需要在使 $\bar Ax-b$ 较小与希望 $x$ 较小（以使 $Ax$ 的变化较小）之间作权衡，这正是正则化的基本思想。

这一观察为 Tikhonov 正则化最小二乘问题 (6.10) 提供了另一种解释：它是一个考虑矩阵 $A$ 可能变化的鲁棒最小二乘问题。Tikhonov 正则化最小二乘问题 (6.10) 的解最小化 $\mathbf{E}\,\|(A+U)x-b\|^2$，其中 $U_{ij}$ 是均值为零、互不相关的随机变量，方差为 $\delta/m$（这里 $A$ 是确定的）。

### 6.4.2 最坏情形鲁棒逼近

也可以用基于集合的最坏情形方法来描述矩阵 $A$ 的变化。用 $A$ 的可能取值组成的集合来描述不确定性：

$$
A\in\mathcal{A}\subseteq\mathbf{R}^{m\times n},
$$

假设该集合非空且有界。对于候选近似解 $x\in\mathbf{R}^n$，将相应的**最坏情形误差**定义为

$$
e_{\mathrm{wc}}(x)=\sup\{\|Ax-b\|\mid A\in\mathcal{A}\},
$$

它总是 $x$ 的凸函数。（最坏情形）**鲁棒逼近问题**就是最小化最坏情形误差：

$$
\begin{array}{ll}
\text{最小化} & e_{\mathrm{wc}}(x)=\sup\{\|Ax-b\|\mid A\in\mathcal{A}\},
\end{array}
\tag{6.14}
$$

其中变量为 $x$，问题数据为 $b$ 和集合 $\mathcal{A}$。当 $\mathcal{A}$ 是单点集 $\mathcal{A}=\{A\}$ 时，鲁棒逼近问题 (6.14) 就退化为基本范数逼近问题 (6.1)。鲁棒逼近问题总是凸优化问题，但能否有效求解取决于使用的范数，以及不确定集 $\mathcal{A}$ 的描述方式。

<div class="example" markdown="1">

**例 6.5 随机鲁棒逼近与最坏情形鲁棒逼近的比较。** 为了说明鲁棒逼近问题的随机表述与最坏情形表述之间的区别，考虑最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \|A(u)x-b\|_2^2,
\end{array}
$$

<p id="robust-uncertainty-start" markdown="1">其中 $u\in\mathbf{R}$ 是不确定参数，$A(u)=A_0+uA_1$。考虑这个问题的一个具体实例，其中 $A(u)\in\mathbf{R}^{20\times10}$、$\|A_0\|=10$、$\|A_1\|=1$，而 $u$</p>

<!-- pdf-page: 334 -->

<figure id="fig-6-15" data-figure="6.15" data-no-english-text="true" data-reader-after="robust-comparison-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-15.png" alt="标称、随机鲁棒和最坏情形鲁棒三种解的残差随参数 u 变化的曲线；标称解在零附近残差最小，最坏情形鲁棒解在负一至一区间内的残差变化最小" data-source-page="334" data-source-rect="215,121,448,307">
<figcaption>图 6.15 三个近似解 $x$ 的残差 $r(u)=\|A(u)x-b\|_2$ 随不确定参数 $u$ 变化的曲线。这三个解分别是：（1）标称最小二乘解 $x_{\mathrm{nom}}$；（2）随机鲁棒逼近问题的解 $x_{\mathrm{stoch}}$（假设 $u$ 在 $[-1,1]$ 上均匀分布）；（3）最坏情形鲁棒逼近问题的解 $x_{\mathrm{wc}}$，假设参数 $u$ 位于区间 $[-1,1]$ 内。标称解在 $u=0$ 时取得最小残差，但当 $u$ 接近 $-1$ 或 $1$ 时，其残差会大得多。最坏情形解在 $u=0$ 时的残差较大，但当参数 $u$ 在区间 $[-1,1]$ 内变化时，其残差不会增加很多。</figcaption>
</figure>

<p id="robust-uncertainty-end" markdown="1" data-reader-continue="robust-uncertainty-start">位于区间 $[-1,1]$ 中。（因此粗略地说，矩阵 $A$ 的变化约为 $\pm10\%$。）</p>

求取三个近似解：

- **标称最优。** 假设 $A(u)$ 取标称值 $A_0$，求得最优解 $x_{\mathrm{nom}}$。

- **随机鲁棒逼近。** 假设参数 $u$ 在 $[-1,1]$ 上均匀分布，求使 $\mathbf{E}\,\|A(u)x-b\|_2^2$ 最小的 $x_{\mathrm{stoch}}$。

- **最坏情形鲁棒逼近。** 求使下式最小的 $x_{\mathrm{wc}}$：

    $$
    \sup_{-1\leq u\leq1}\|A(u)x-b\|_2
    =\max\{\|(A_0-A_1)x-b\|_2,\|(A_0+A_1)x-b\|_2\}.
    $$

<p id="robust-comparison-end" markdown="1">对这三个 $x$，图 6.15 分别画出了残差 $r(u)=\|A(u)x-b\|_2$ 随不确定参数 $u$ 变化的曲线。这些曲线表明，近似解对参数 $u$ 的变化可能相当敏感。标称解在 $u=0$ 时取得最小残差，但对参数变化十分敏感：当 $u$ 偏离 $0$、接近 $-1$ 或 $1$ 时，它产生的残差会大得多。最坏情形解在 $u=0$ 时残差较大，但当 $u$ 在区间 $[-1,1]$ 上变化时，其残差增加不多。随机鲁棒近似解的表现介于两者之间。</p>

</div>

<!-- pdf-page: 335 -->

鲁棒逼近问题 (6.14) 出现在许多场景和应用中。在估计问题中，集合 $\mathcal{A}$ 给出待估计向量与测量向量之间线性关系的不确定性。模型 $y=Ax+v$ 中的噪声项 $v$ 有时称为**加性噪声**或**加性误差**，因为它加在“理想”测量值 $Ax$ 上。相应地，$A$ 的变化称为**乘性误差**，因为它与变量 $x$ 相乘。

在最优设计问题中，这种变化可以表示联系设计变量 $x$ 与结果向量 $Ax$ 的线性方程所具有的不确定性（例如制造过程引起的不确定性）。于是，鲁棒逼近问题 (6.14) 可以解释为鲁棒设计问题：寻找设计变量 $x$，使得在 $A$ 的所有可能取值中，$Ax$ 与 $b$ 之间最坏的偏差尽可能小。

#### 有限集

这里 $\mathcal{A}=\{A_1,\ldots,A_k\}$，鲁棒逼近问题为

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\max_{i=1,\ldots,k}\|A_ix-b\|.
\end{array}
$$

它等价于不确定集为多面体集 $\mathcal{A}=\operatorname{\mathbf{conv}}\{A_1,\ldots,A_k\}$ 的鲁棒逼近问题：

$$
\begin{array}{ll}
\text{最小化} & \sup\{\|Ax-b\|\mid A\in\operatorname{\mathbf{conv}}\{A_1,\ldots,A_k\}\}.
\end{array}
$$

可以把问题写成上图形式：

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & \|A_ix-b\|\leq t,\quad i=1,\ldots,k.
\end{array}
$$

根据使用的范数，可以采用多种方法求解。如果使用欧几里得范数，这就是 SOCP。如果使用 $\ell_1$ 或 $\ell_\infty$ 范数，则可以写成 LP。

#### 范数有界的误差

这里不确定集 $\mathcal{A}$ 是一个范数球，$\mathcal{A}=\{\bar A+U\mid\|U\|\leq a\}$，其中 $\|\cdot\|$ 是 $\mathbf{R}^{m\times n}$ 上的范数。此时有

$$
e_{\mathrm{wc}}(x)=\sup\{\|\bar Ax-b+Ux\|\mid\|U\|\leq a\}.
$$

解释这个式子时需要注意，第一次出现的范数定义在 $\mathbf{R}^m$ 上（用来衡量残差大小），第二次出现的范数则定义在 $\mathbf{R}^{m\times n}$ 上（用来定义范数球 $\mathcal{A}$）。

在若干情形下，$e_{\mathrm{wc}}(x)$ 的这个表达式可以简化。例如，采用 $\mathbf{R}^n$ 上的欧几里得范数，以及它在 $\mathbf{R}^{m\times n}$ 上对应的诱导范数，即最大奇异值。如果 $\bar Ax-b\neq0$ 且 $x\neq0$，则 $e_{\mathrm{wc}}(x)$ 表达式中的上确界在 $U=auv^T$ 时达到，其中

$$
u=\frac{\bar Ax-b}{\|\bar Ax-b\|_2},\qquad v=\frac{x}{\|x\|_2},
$$

得到的最坏情形误差为

$$
e_{\mathrm{wc}}(x)=\|\bar Ax-b\|_2+a\|x\|_2.
$$

<!-- pdf-page: 336 -->

（容易验证，当 $x$ 或 $\bar Ax-b$ 为零时，这个表达式也成立。）于是鲁棒逼近问题 (6.14) 变为

$$
\begin{array}{ll}
\text{最小化} & \|\bar Ax-b\|_2+a\|x\|_2,
\end{array}
$$

这是一个正则化范数问题，可以写成如下 SOCP 求解：

$$
\begin{array}{ll}
\text{最小化} & t_1+at_2\\
\text{约束条件} & \|\bar Ax-b\|_2\leq t_1,\quad\|x\|_2\leq t_2.
\end{array}
$$

由于这个问题的解与正则化参数 $\delta$ 取某个值时的正则化最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \|\bar Ax-b\|_2^2+\delta\|x\|_2^2
\end{array}
$$

的解相同，我们就得到了正则化最小二乘问题的另一种解释：它是一个最坏情形鲁棒逼近问题。

<div class="translator-note" markdown="1">

**译注（正则化参数的端点）：** 范数和问题的零解有时只能由平方范数问题在 $\delta\to\infty$ 时趋近，而不能在有限参数下得到。例如，标量情形 $\bar A=b=1$、$a=2$ 时，$|x-1|+2|x|$ 的唯一最优解为 $x=0$；但对任何有限的 $\delta\geq0$，$(x-1)^2+\delta x^2$ 的最优解都是 $x=1/(1+\delta)>0$。因此，上述对应关系在零解端点需要包含参数趋于无穷的极限。

</div>

#### 不确定性椭球

也可以为每一行给出一个可能取值的椭球，以此描述 $A$ 的变化：

$$
\mathcal{A}=\{[a_1\ \cdots\ a_m]^T\mid a_i\in\mathcal{E}_i,\ i=1,\ldots,m\},
$$

其中

$$
\mathcal{E}_i=\{\bar a_i+P_i u\mid\|u\|_2\leq1\}.
$$

矩阵 $P_i\in\mathbf{R}^{n\times n}$ 描述 $a_i$ 的变化。允许 $P_i$ 具有非平凡零空间，以便描述 $a_i$ 的变化被限制在某个子空间内的情形。作为一种极端情形，如果 $a_i$ 没有不确定性，就取 $P_i=0$。

在这种椭球不确定性描述下，可以给出每个残差最坏情形幅值的显式表达式：

$$
\begin{aligned}
\sup_{a_i\in\mathcal{E}_i}|a_i^Tx-b_i|
&=\sup\{|\bar a_i^Tx-b_i+(P_i u)^Tx|\mid\|u\|_2\leq1\}\\
&=|\bar a_i^Tx-b_i|+\|P_i^Tx\|_2.
\end{aligned}
$$

利用这个结果，可以求解几种鲁棒逼近问题。例如，鲁棒 $\ell_2$ 范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & e_{\mathrm{wc}}(x)=\sup\{\|Ax-b\|_2\mid a_i\in\mathcal{E}_i,\ i=1,\ldots,m\}
\end{array}
$$

可以按如下方式转化为 SOCP。最坏情形误差的显式表达式为

$$
e_{\mathrm{wc}}(x)
=\left(\sum_{i=1}^m\left(\sup_{a_i\in\mathcal{E}_i}|a_i^Tx-b_i|\right)^2\right)^{1/2}
=\left(\sum_{i=1}^m\bigl(|\bar a_i^Tx-b_i|+\|P_i^Tx\|_2\bigr)^2\right)^{1/2}.
$$

为了最小化 $e_{\mathrm{wc}}(x)$，可以求解

$$
\begin{array}{ll}
\text{最小化} & \|t\|_2\\
\text{约束条件} & |\bar a_i^Tx-b_i|+\|P_i^Tx\|_2\leq t_i,\quad i=1,\ldots,m,
\end{array}
$$

<!-- pdf-page: 337 -->

其中引入了新变量 $t_1,\ldots,t_m$。这个问题可以写成

$$
\begin{array}{ll}
\text{最小化} & \|t\|_2\\
\text{约束条件} & \bar a_i^Tx-b_i+\|P_i^Tx\|_2\leq t_i,\quad i=1,\ldots,m\\
& -\bar a_i^Tx+b_i+\|P_i^Tx\|_2\leq t_i,\quad i=1,\ldots,m.
\end{array}
$$

改写为上图形式后，它就是 SOCP。

#### 具有线性结构的范数有界误差

作为范数界描述 $\mathcal{A}=\{\bar A+U\mid\|U\|\leq a\}$ 的推广，可以将 $\mathcal{A}$ 定义为范数球在仿射变换下的像：

$$
\mathcal{A}=\{\bar A+u_1A_1+u_2A_2+\cdots+u_pA_p\mid\|u\|\leq1\},
$$

其中 $\|\cdot\|$ 是 $\mathbf{R}^p$ 上的范数，$p+1$ 个矩阵 $\bar A,A_1,\ldots,A_p\in\mathbf{R}^{m\times n}$ 已给定。最坏情形误差可以写成

$$
\begin{aligned}
e_{\mathrm{wc}}(x)
&=\sup_{\|u\|\leq1}\|(\bar A+u_1A_1+\cdots+u_pA_p)x-b\|\\
&=\sup_{\|u\|\leq1}\|P(x)u+q(x)\|,
\end{aligned}
$$

其中 $P$ 和 $q$ 定义为

$$
P(x)=\begin{bmatrix}A_1x&A_2x&\cdots&A_px\end{bmatrix}\in\mathbf{R}^{m\times p},
\qquad q(x)=\bar Ax-b\in\mathbf{R}^m.
$$

先考虑鲁棒 Chebyshev 逼近问题

$$
\begin{array}{ll}
\text{最小化} & e_{\mathrm{wc}}(x)=\displaystyle\sup_{\|u\|_\infty\leq1}\|(\bar A+u_1A_1+\cdots+u_pA_p)x-b\|_\infty.
\end{array}
$$

这时可以推导出最坏情形误差的显式表达式。用 $p_i(x)^T$ 表示 $P(x)$ 的第 $i$ 行。有

$$
\begin{aligned}
e_{\mathrm{wc}}(x)
&=\sup_{\|u\|_\infty\leq1}\|P(x)u+q(x)\|_\infty\\
&=\max_{i=1,\ldots,m}\sup_{\|u\|_\infty\leq1}|p_i(x)^Tu+q_i(x)|\\
&=\max_{i=1,\ldots,m}(\|p_i(x)\|_1+|q_i(x)|).
\end{aligned}
$$

因此，鲁棒 Chebyshev 逼近问题可以写成 LP

$$
\begin{array}{ll}
\text{最小化} & t\\
\text{约束条件} & -y_0\preceq\bar Ax-b\preceq y_0\\
& -y_k\preceq A_kx\preceq y_k,\quad k=1,\ldots,p\\
& \displaystyle y_0+\sum_{k=1}^p y_k\preceq t\mathbf{1},
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$、$y_k\in\mathbf{R}^m$、$t\in\mathbf{R}$。

再考虑鲁棒最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & e_{\mathrm{wc}}(x)=\displaystyle\sup_{\|u\|_2\leq1}\|(\bar A+u_1A_1+\cdots+u_pA_p)x-b\|_2.
\end{array}
$$

<!-- pdf-page: 338 -->

这里用拉格朗日对偶性来计算 $e_{\mathrm{wc}}$。最坏情形误差 $e_{\mathrm{wc}}(x)$ 是以下（非凸）二次优化问题最优值的平方根：

$$
\begin{array}{ll}
\text{最大化} & \|P(x)u+q(x)\|_2^2\\
\text{约束条件} & u^Tu\leq1,
\end{array}
$$

其中变量为 $u$。这个问题的拉格朗日对偶可以写成 SDP

$$
\begin{array}{ll}
\text{最小化} & t+\lambda\\
\text{约束条件} &
\begin{bmatrix}
I&P(x)&q(x)\\
P(x)^T&\lambda I&0\\
q(x)^T&0&t
\end{bmatrix}\succeq0,
\end{array}
\tag{6.15}
$$

其中变量为 $t,\lambda\in\mathbf{R}$。而且，正如 §5.2 和 §B.1 中所述（证明见 §B.4），这一对原问题与对偶问题满足强对偶性。换言之，固定 $x$ 后，通过求解变量为 $t$ 和 $\lambda$ 的 SDP (6.15)，就可以计算 $e_{\mathrm{wc}}(x)^2$。对 $t$、$\lambda$ 和 $x$ 联合优化，等价于最小化 $e_{\mathrm{wc}}(x)^2$。由此可知，鲁棒最小二乘问题等价于以 $x,\lambda,t$ 为变量的 SDP (6.15)。

<div class="example" markdown="1">

**例 6.6 最坏情形鲁棒解、Tikhonov 正则化解与标称最小二乘解的比较。** 考虑鲁棒逼近问题的一个实例：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sup_{\|u\|_2\leq1}\|(\bar A+u_1A_1+u_2A_2)x-b\|_2,
\end{array}
\tag{6.16}
$$

其中维度为 $m=50$、$n=20$。矩阵 $\bar A$ 的范数为 $10$，矩阵 $A_1$ 和 $A_2$ 的范数均为 $1$，因此粗略地说，矩阵 $A$ 的变化约为 $10\%$。不确定参数 $u_1$ 和 $u_2$ 位于 $\mathbf{R}^2$ 中的单位圆盘内。

计算鲁棒最小二乘问题 (6.16) 的最优解 $x_{\mathrm{rls}}$，以及标称最小二乘问题的解 $x_{\mathrm{ls}}$（即假设 $u=0$），还计算 $\delta=1$ 时的 Tikhonov 正则化解 $x_{\mathrm{tik}}$。

为了说明这些近似解对参数 $u$ 的敏感性，生成 $10^5$ 个在单位圆盘上均匀分布的参数向量，并对每个参数值计算残差

$$
\|(A_0+u_1A_1+u_2A_2)x-b\|_2.
$$

残差的分布见图 6.16。

可以观察到几点。首先，标称最小二乘解的残差分布范围很宽，从约 $0.52$ 的最小值到约 $4.9$ 的最大值。特别地，最小二乘解对参数变化非常敏感。相比之下，当不确定参数在单位圆盘内变化时，鲁棒最小二乘解和 Tikhonov 正则化解的残差变化都小得多。例如，对于单位圆盘内的所有参数，鲁棒最小二乘解取得的残差都在 $2.0$ 到 $2.6$ 之间。

</div>

## 6.5 函数拟合与插值

<p id="function-fitting-intro-start" markdown="1">在函数拟合问题中，我们从一个有限维函数子空间中选择一个函数，使它最符合给定的数据或要求。为简单起见，下面</p>

<!-- pdf-page: 339 -->

<figure id="fig-6-16" data-figure="6.16" data-reader-after="function-fitting-intro-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-16.png" alt="叠加的三组残差直方图，比较普通最小二乘、Tikhonov 正则化和鲁棒最小二乘的解；横轴为残差范数，纵轴为频率，鲁棒解的残差集中在较窄区间内" data-source-page="339" data-source-rect="140,259,413,474.5">
<figcaption>图 6.16 最小二乘问题（6.16）的三个解所对应的残差分布：$x_{\mathrm{ls}}$ 是假设 $u=0$ 时的最小二乘解；$x_{\mathrm{tik}}$ 是 $\delta=1$ 时的 Tikhonov 正则化解；$x_{\mathrm{rls}}$ 是鲁棒最小二乘解。这些直方图通过从 $\mathbf{R}^2$ 中单位圆盘上的均匀分布生成不确定参数向量 $u$ 的 $10^5$ 个取值得到。直方图各分组区间的宽度为 $0.1$。</figcaption>
<p class="figure-translation">图内文字：frequency——频率。</p>
</figure>

<!-- pdf-page: 340 -->

<p id="function-fitting-intro-end" markdown="1" data-reader-continue="function-fitting-intro-start">考虑实值函数；这些想法也很容易扩展到向量值函数。</p>

### 6.5.1 函数族

考虑具有公共定义域 $\operatorname{\mathbf{dom}}f_i=D$ 的函数族 $f_1,\ldots,f_n:\mathbf{R}^k\to\mathbf{R}$。对每个 $x\in\mathbf{R}^n$，定义相应的函数 $f:\mathbf{R}^k\to\mathbf{R}$ 为

$$
f(u)=x_1f_1(u)+\cdots+x_nf_n(u),
\tag{6.17}
$$

且 $\operatorname{\mathbf{dom}}f=D$。函数族 $\{f_1,\ldots,f_n\}$ 有时称为（拟合问题的）**基函数集**，即使这些函数并不线性无关，也沿用这一称呼。向量 $x\in\mathbf{R}^n$ 对函数子空间作参数化，是我们的优化变量，有时称为**系数向量**。这些基函数生成了 $D$ 上的函数子空间 $\mathcal{F}$。

在许多应用中，基函数是利用先验知识或经验特意选取的，使有限维函数子空间能够合理地描述所关心的函数。另一些情形下，则使用更通用的函数族。下面介绍其中几种。

#### 多项式

$\mathbf{R}$ 上的一个常见函数子空间由次数小于 $n$ 的多项式组成。最简单的一组基由各个幂函数构成，即 $f_i(t)=t^{i-1}$，$i=1,\ldots,n$。在许多应用中，会用另一组基来描述同一个子空间，例如次数小于 $n$、关于某个正函数（或测度）$\phi:\mathbf{R}^n\to\mathbf{R}_+$ 标准正交的一组多项式 $f_1,\ldots,f_n$，即

$$
\int f_i(t)f_j(t)\phi(t)\,dt=
\begin{cases}
1 & i=j,\\
0 & i\neq j.
\end{cases}
$$

另一组常见的多项式基，是与互不相同的点 $t_1,\ldots,t_n$ 对应的 **Lagrange 基** $f_1,\ldots,f_n$，它们满足

$$
f_i(t_j)=\begin{cases}
1 & i=j,\\
0 & i\neq j.
\end{cases}
$$

也可以考虑 $\mathbf{R}^k$ 上的多项式，并限制其最高总次数，或者每个变量的最高次数。

一个相关的例子是次数小于 $n$ 的**三角多项式**，其基为

$$
\sin kt,\quad k=1,\ldots,n-1,\qquad
\cos kt,\quad k=0,\ldots,n-1.
$$

#### 分段线性函数

首先对定义域 $D$ 进行**三角剖分**（triangularization），其含义如下。给定一组网格点 $g_1,\ldots,g_n\in\mathbf{R}^k$，把 $D$ 划分成一组单纯形：

$$
D=S_1\cup\cdots\cup S_m,\qquad
\operatorname{\mathbf{int}}(S_i\cap S_j)=\emptyset\quad\text{当 }i\neq j.
$$

<!-- pdf-page: 341 -->

<figure id="fig-6-17" data-figure="6.17" data-no-english-text="true" data-reader-after="piecewise-linear-explanation-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-17.png" alt="单位正方形上的二元分段线性函数三维图，曲面由三角形平面片拼接而成，坐标轴为 u₁、u₂ 和函数值" data-source-page="341" data-source-rect="166,121,399,299">
<figcaption>图 6.17 单位正方形上的一个二元分段线性函数。该三角剖分包含 98 个单纯形，所用的均匀网格由单位正方形内的 64 个点组成。</figcaption>
</figure>

每个单纯形都是 $k+1$ 个网格点的凸包，而且要求每个网格点都是包含它的任意单纯形的一个顶点。

给定三角剖分后，可以先给网格点指定函数值 $f(g_i)=x_i$，再在每个单纯形上作仿射延拓，从而构造一个分段线性（更准确地说，分段仿射）函数 $f$。函数 $f$ 可以表示为 (6.17)，其中基函数 $f_i$ 在每个单纯形上都是仿射函数，并由条件

$$
f_i(g_j)=\begin{cases}
1 & i=j,\\
0 & i\neq j
\end{cases}
$$

确定。由构造可知，这样的函数是连续的。

<p id="piecewise-linear-explanation-end" markdown="1">图 6.17 给出了 $k=2$ 时的一个例子。</p>

#### 分段多项式与样条

在经过三角剖分的定义域上构造分段仿射函数的想法，很容易扩展到分段多项式及其他函数。

分段多项式是在三角剖分的每个单纯形上定义一个多项式（限制其最高次数），并要求整个函数连续，即相邻单纯形上的多项式在共同边界处取值相同。进一步要求分段多项式直到某一阶的导数都连续，就可以定义各类**样条函数**（spline functions）。图 6.18 给出了一个三次样条的例子，即 $\mathbf{R}$ 上具有连续一阶和二阶导数的三次分段多项式。

<!-- pdf-page: 342 -->

<figure id="fig-6-18" data-figure="6.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-18.png" alt="由三个三次多项式拼接成的三次样条曲线；两个内部区间边界以竖直虚线表示，三个多项式在边界处平滑衔接" data-source-page="342" data-source-rect="223,259,451,443">
<figcaption>图 6.18 <em>三次样条。</em>三次样条是一阶、二阶导数均连续的分段多项式。本例中的三次样条 $f$ 由三个三次多项式组成：$p_1$ 定义在 $[u_0,u_1]$ 上，$p_2$ 定义在 $[u_1,u_2]$ 上，$p_3$ 定义在 $[u_2,u_3]$ 上。相邻多项式在边界点 $u_1$ 和 $u_2$ 处的函数值相同，一阶、二阶导数也分别相等。本例中，该函数族的维数为 $n=6$，因为共有 12 个多项式系数（每个三次多项式有 4 个）和 6 个等式约束（在 $u_1$ 和 $u_2$ 处各有 3 个）。</figcaption>
</figure>

<!-- pdf-page: 343 -->

### 6.5.2 约束

本节介绍可以施加在函数 $f$ 上，因而也就是施加在变量 $x\in\mathbf{R}^n$ 上的一些约束。

#### 函数值插值条件与不等式

设 $v$ 是 $D$ 中的一点。$f$ 在 $v$ 处的值

$$
f(v)=\sum_{i=1}^n x_i f_i(v)
$$

是 $x$ 的线性函数。因此，要求函数 $f$ 在指定点 $v_j\in D$ 处取值 $z_j\in\mathbf{R}$ 的**插值条件**

$$
f(v_j)=z_j,\qquad j=1,\ldots,m,
$$

构成关于 $x$ 的一组线性等式。更一般地，对给定点处的函数值施加不等式，例如 $l\leq f(v)\leq u$，就是对变量 $x$ 施加线性不等式。还有许多有用的关于 $f$（因而也是关于 $x$）的凸约束，涉及有限个点 $v_1,\ldots,v_N$ 处的函数值。例如，Lipschitz 约束

$$
|f(v_j)-f(v_k)|\leq L\|v_j-v_k\|,\qquad j,k=1,\ldots,m,
$$

构成关于 $x$ 的一组线性不等式。

也可以在无穷多个点处对函数值施加不等式。例如，考虑非负约束

$$
f(u)\geq0\quad\text{对所有 }u\in D.
$$

这是关于 $x$ 的凸约束（因为它是无穷多个半空间的交），但除了能够利用函数特定结构的特殊情形外，未必能得到容易求解的问题。一个简单的例子是分段线性函数：如果函数在网格点处的取值非负，那么处处非负，因此只需一组简单的（有限个）线性不等式。

一个稍复杂的例子是 $\mathbf{R}$ 上的多项式，其最高次数为偶数 $2k$（即 $n=2k+1$），且 $D=\mathbf{R}$。正如第 65 页习题 2.37 所示，非负约束

$$
p(u)=x_1+x_2u+\cdots+x_{2k+1}u^{2k}\geq0\quad\text{对所有 }u\in\mathbf{R}
$$

等价于

$$
x_i=\sum_{m+n=i+1}Y_{mn},\qquad i=1,\ldots,2k+1,\qquad Y\succeq0,
$$

其中 $Y\in\mathbf{S}^{k+1}$ 是辅助变量。

<!-- pdf-page: 344 -->

#### 导数约束

假设基函数 $f_i$ 在某点 $v\in D$ 处可微。梯度

$$
\nabla f(v)=\sum_{i=1}^n x_i\nabla f_i(v)
$$

是 $x$ 的线性函数，因此，对 $f$ 在 $v$ 处导数的插值条件，可归结为关于 $x$ 的线性等式约束。要求 $v$ 处梯度的范数不超过给定界限，即

$$
\|\nabla f(v)\|=\left\|\sum_{i=1}^n x_i\nabla f_i(v)\right\|\leq M,
$$

是关于 $x$ 的凸约束。同样的想法也可以推广到高阶导数。例如，如果 $f$ 在 $v$ 处二阶可微，那么要求

$$
lI\preceq\nabla^2f(v)\preceq uI
$$

就是关于 $x$ 的线性矩阵不等式，因此是凸约束。

也可以在无穷多个点处对导数施加约束。例如，可以要求 $f$ 单调：

$$
f(u)\geq f(v)\quad\text{对所有 }u,v\in D,\ u\succeq v.
$$

这是关于 $x$ 的凸约束，但除特殊情形外，未必能得到容易求解的问题。例如，当 $f$ 是分段仿射函数时，单调性约束等价于在每个单纯形内部都有 $\nabla f(v)\succeq0$。由于梯度是网格点函数值的线性函数，因此可得到一组简单的（有限个）线性不等式。

再例如，可以要求函数为凸函数，即满足

$$
f((u+v)/2)\leq(f(u)+f(v))/2\quad\text{对所有 }u,v\in D
$$

（当 $f$ 连续时，这就足以保证凸性）。这是一个凸约束，在某些情形下具有便于求解的表示。一个明显的例子是 $f$ 为二次函数，这时凸性约束归结为要求 $f$ 的二次部分非负，这是一个 LMI。§6.5.5 将更详细地介绍另一个凸性约束能带来易解问题的例子。

#### 积分约束

函数子空间上的任意线性泛函 $\mathcal{L}$，都可以表示为 $x$ 的线性函数，即 $\mathcal{L}(f)=c^Tx$。计算 $f$（或某阶导数）在一点处的值，只是其中的一个特例。另一个例子是线性泛函

$$
\mathcal{L}(f)=\int_D\phi(u)f(u)\,du,
$$

<!-- pdf-page: 345 -->

其中 $\phi:\mathbf{R}^k\to\mathbf{R}$，它可以写成 $\mathcal{L}(f)=c^Tx$，其中

$$
c_i=\int_D\phi(u)f_i(u)\,du.
$$

因此，形如 $\mathcal{L}(f)=a$ 的约束是关于 $x$ 的线性等式约束。这种约束的一个例子是**矩约束**

$$
\int_D t^m f(t)\,dt=a
$$

（其中 $f:\mathbf{R}\to\mathbf{R}$）。

### 6.5.3 拟合与插值问题

#### 最小范数函数拟合

在拟合问题中，给定数据

$$
(u_1,y_1),\quad\ldots,\quad(u_m,y_m),
$$

其中 $u_i\in D$、$y_i\in\mathbf{R}$，希望找到函数 $f\in\mathcal{F}$，使它尽可能贴近这些数据。例如，在最小二乘拟合中，考虑问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m(f(u_i)-y_i)^2,
\end{array}
$$

这就是一个以 $x$ 为变量的简单最小二乘问题。可以加入各种约束，例如要求 $f$ 在各点满足的线性不等式、对 $f$ 导数的约束、单调性约束或矩约束。

<div class="example" markdown="1">

**例 6.7 多项式拟合。** 给定数据 $u_1,\ldots,u_m\in\mathbf{R}$ 和 $v_1,\ldots,v_m\in\mathbf{R}$，希望用形如

$$
p(u)=x_1+x_2u+\cdots+x_nu^{n-1}
$$

的多项式近似拟合这些数据。对每个 $x$，构造误差向量

$$
e=(p(u_1)-v_1,\ldots,p(u_m)-v_m).
$$

为了找到使误差范数最小的多项式，求解范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|e\|=\|Ax-v\|,
\end{array}
$$

其中变量为 $x\in\mathbf{R}^n$，$A_{ij}=u_i^{j-1}$，$i=1,\ldots,m$，$j=1,\ldots,n$。

图 6.19 给出了一个采用 $\ell_2$ 范数和 $\ell_\infty$ 范数的例子，其中有 $m=40$ 个数据点，$n=6$（即多项式最高次数为 $5$）。

</div>

<!-- pdf-page: 346 -->

<figure id="fig-6-19" data-figure="6.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-19.png" alt="对四十个圆圈数据点进行逼近的两条五次多项式曲线；实线使误差的二范数最小，虚线使误差的无穷范数最小" data-source-page="346" data-source-rect="212,138,449,321">
<figcaption>图 6.19 逼近图中 40 个圆圈所示数据点的两个五次多项式。实线所示的多项式最小化误差的 $\ell_2$ 范数；虚线所示的多项式最小化误差的 $\ell_\infty$ 范数。</figcaption>
</figure>

<figure id="fig-6-20" data-figure="6.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-20.png" alt="对四十个圆圈数据点进行逼近的两条三次样条曲线；实线使误差的二范数最小，虚线使误差的无穷范数最小，竖直虚线标示区间边界" data-source-page="346" data-source-rect="212,420,449,603.5">
<figcaption>图 6.20 逼近图中 40 个圆圈所示数据点的两条三次样条（数据点与图 6.19 相同）。实线所示的样条最小化误差的 $\ell_2$ 范数；虚线所示的样条最小化误差的 $\ell_\infty$ 范数。与图 6.19 所示的多项式逼近一样，拟合函数所在子空间的维数为 6。</figcaption>
</figure>

<!-- pdf-page: 347 -->

<div class="example" markdown="1">

**例 6.8 样条拟合。** 图 6.20 给出了与例 6.7 相同的数据，以及用三次样条得到的两个最优拟合。将区间 $[-1,1]$ 分为三个等长区间，考虑最高次数为 $3$、具有连续一阶和二阶导数的分段多项式。这个函数子空间的维度为 $6$，与例 6.7 中最高次数为 $5$ 的多项式空间维度相同。

</div>

在最简单的函数拟合形式中，有 $m\gg n$，即数据点的数量远大于函数子空间的维度。由于子空间中的所有函数都是平滑的，因此拟合会自动实现平滑。

#### 最小范数插值

在函数拟合的另一种变体中，数据点的数量少于函数子空间的维度。最简单的情形是要求所选函数满足插值条件

$$
f(u_i)=y_i,\qquad i=1,\ldots,m,
$$

这就是关于 $x$ 的线性等式约束。在满足这些插值条件的函数中，可以寻找最平滑的函数，或者最小的函数。这些要求会产生最小范数问题。

在最一般的函数拟合问题中，可以在各种凸约束下优化某个目标（例如误差 $e$ 的某种度量），这些约束表示关于实际函数的先验知识。

#### 插值、外推与确定界限

在原始数据集之外的一点 $v$ 处计算最优拟合函数 $\widehat f$ 的值，就得到实际函数在 $v$ 处取值的一个猜测。当 $v$ 位于给定数据点之间或附近时（例如 $v\in\operatorname{\mathbf{conv}}\{v_1,\ldots,v_m\}$），这称为**插值**；否则称为**外推**。

也可以在约束下最大化和最小化（线性函数）$f(v)$，从而得到 $f(v)$ 可能取值的区间。拟合函数还可以用来辅助识别错误数据或离群点。例如，可以采用 $\ell_1$ 范数拟合，然后寻找误差较大的数据点。

### 6.5.4 稀疏描述与基追踪

在**基追踪**中，基函数的数量非常大，目标是用少量基函数的线性组合很好地拟合给定数据。（在这种语境中，函数族线性相关，有时称为**过完备基**（over-complete basis）或**字典**（dictionary）。）之所以称为基追踪，是因为我们从给定的过完备基中选取一组小得多的基来描述数据。

<!-- pdf-page: 348 -->

因此，要寻找一个能很好地拟合数据的函数 $f\in\mathcal{F}$，即

$$
f(u_i)\approx y_i,\qquad i=1,\ldots,m,
$$

并且其系数向量 $x$ 稀疏，即 $\operatorname{\mathbf{card}}(x)$ 较小。这时，将

$$
f=x_1f_1+\cdots+x_nf_n=\sum_{i\in\mathcal{B}}x_if_i,
$$

称为数据的**稀疏描述**，其中 $\mathcal{B}=\{i\mid x_i\neq0\}$ 是所选基元素的指标集。从数学上说，基追踪与回归变量选择问题相同（见 §6.4），但优化问题的解释（及规模）不同。

<div class="translator-note" markdown="1">

**译注（回归变量选择的交叉引用）：** 本页两处指向 §6.4 的引用，所述内容实际位于 §6.3.2 的例 6.4，阅读时请参见该例。

</div>

稀疏描述和基追踪有许多用途。它们可以用于去噪或平滑，也可以用于数据压缩，以便高效传输或存储信号。在数据压缩中，发送方和接收方都知道字典，即各个基元素。为了向接收方发送一个信号，发送方先找到该信号的稀疏表示，然后只把非零系数（保留一定精度）发送给接收方。接收方利用这些系数，就能重构原信号的一个近似。

一种常见的基追踪方法，与 §6.4 中描述的回归变量选择方法相同，都是把 $\ell_1$ 范数正则化作为寻找稀疏描述的启发式方法。先求解凸问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m(f(u_i)-y_i)^2+\gamma\|x\|_1,
\end{array}
\tag{6.18}
$$

其中参数 $\gamma>0$ 用于在数据拟合质量与系数向量的稀疏程度之间作权衡。这个问题的解可以直接使用，也可以再作一步细化：固定 (6.18) 的解所给出的稀疏模式，寻找最佳拟合。换言之，先求解 (6.18)，得到 $\widehat x$。然后令 $\mathcal{B}=\{i\mid\widehat x_i\neq0\}$，即非零系数对应的指标集。再求解最小二乘问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m(f(u_i)-y_i)^2,
\end{array}
$$

其中变量为 $x_i$，$i\in\mathcal{B}$，而对 $i\notin\mathcal{B}$，令 $x_i=0$。

在基追踪和稀疏描述的应用中，字典规模很大并不少见，$n$ 可以达到 $10^4$ 量级，甚至更大。要高效求解 (6.18)，算法必须利用问题结构，而这些结构来自字典中各个信号的结构。

#### 通过基追踪进行时频分析

下面用一个简单例子说明基追踪和稀疏表示。考虑 $\mathbf{R}$ 上的函数（或信号），关注的区间为 $[0,1]$。把自变量看成时间，因此用 $t$（而非 $u$）表示。

先描述字典中的基函数。每个基函数都是一个**高斯正弦脉冲**，也称 **Gabor 函数**，具有如下形式：

$$
e^{-(t-\tau)^2/\sigma^2}\cos(\omega t+\phi),
$$

<!-- pdf-page: 349 -->

<figure id="fig-6-21" data-figure="6.21" data-no-english-text="true" data-reader-after="gabor-dictionary-explanation-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-21.png" alt="三个以时刻零点五为中心的字典基函数，按频率零、七十五、一百五十从上到下排列；频率越高，局部振荡越密集" data-source-page="349" data-source-rect="129,123,431,361">
<figcaption>图 6.21 字典中的三个基元素，中心时刻均为 $\tau=0.5$，相位均为余弦相位。最上方信号的频率为 $\omega=0$，中间信号的频率为 $\omega=75$，最下方信号的频率为 $\omega=150$。</figcaption>
</figure>

其中 $\sigma>0$ 给出脉冲宽度，$\tau$ 是脉冲（中心）所在的时刻，$\omega\geq0$ 是频率，$\phi$ 是相位角。所有基函数的宽度都为 $\sigma=0.05$。脉冲的时刻和频率为

$$
\tau=0.002k,\quad k=0,\ldots,500,\qquad
\omega=5k,\quad k=0,\ldots,30.
$$

对于每个时刻 $\tau$，有一个频率为零（相位为 $\phi=0$）的基元素；其余 $30$ 个频率各有 $2$ 个基元素（余弦和正弦，即相位分别为 $\phi=0$ 和 $\phi=\pi/2$），因此一共有 $501\times61=30561$ 个基元素。很自然地，可以用时刻、频率和相位（余弦或正弦）为基元素编号，因此将它们记作

$$
\begin{aligned}
f_{\tau,\omega,c},\quad &\tau=0,0.002,\ldots,1,\quad\omega=0,5,\ldots,150,\\
f_{\tau,\omega,s},\quad &\tau=0,0.002,\ldots,1,\quad\omega=5,\ldots,150.
\end{aligned}
$$

<p id="gabor-dictionary-explanation-end" markdown="1">图 6.21 给出了其中三个基函数（时刻均为 $\tau=0.5$）。</p>

使用这个字典进行基追踪，可以看成对数据进行**时频分析**。如果基元素 $f_{\tau,\omega,c}$ 或 $f_{\tau,\omega,s}$ 出现在信号的稀疏表示中（即其系数非零），就可以解释为数据在时刻 $\tau$ 包含频率 $\omega$。

我们将用基追踪寻找信号

$$
y(t)=a(t)\sin\theta(t)
$$

<!-- pdf-page: 350 -->

<figure id="fig-6-22" data-figure="6.22" data-no-english-text="true" data-reader-after="signal-parameters-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-22.png" alt="上图为几乎重合的原始信号和基追踪逼近信号，下图采用较小的纵轴刻度范围显示两者之间的逼近误差" data-source-page="350" data-source-rect="174,123,483,361">
<figcaption>图 6.22 上图：原始信号（实线）与通过基追踪得到的逼近信号 $\widehat{y}$（虚线）几乎无法区分。下图：逼近误差 $y(t)-\widehat{y}(t)$，纵轴采用了不同的刻度比例。</figcaption>
</figure>

的稀疏近似，其中

<div id="signal-parameters-end" markdown="1">

$$
a(t)=1+0.5\sin(11t),\qquad\theta(t)=30\sin(5t).
$$

</div>

（选择这个信号只是因为它容易描述，而且其频谱成分随时间有明显变化。）可以把 $a(t)$ 解释为信号幅度，把 $\theta(t)$ 解释为其总相位。还可以把

$$
\omega(t)=\left|\frac{d\theta}{dt}\right|=150|\cos(5t)|
$$

解释为信号在时刻 $t$ 的**瞬时频率**。数据是在区间 $[0,1]$ 上等间隔采得的 $501$ 个值，即给定 $501$ 对 $(t_k,y_k)$，其中

$$
t_k=0.005k,\qquad y_k=y(t_k),\qquad k=0,\ldots,500.
$$

<div class="translator-note" markdown="1">

**译注（采样间距）：** 原式的 $0.005\times500=2.5$，与上文“区间 $[0,1]$ 上的 $501$ 个等间隔采样值”不一致。若按上文所述包含区间两端点，间距应为 $1/500=0.002$，即 $t_k=0.002k$，$k=0,\ldots,500$。后面的相对误差公式使用 $1,\ldots,501$ 编号，计算时须与这里的 $0,\ldots,500$ 对齐到同一组样本。

</div>

<p id="basis-pursuit-fit-start" markdown="1">先求解 $\gamma=1$ 时的 $\ell_1$ 范数正则化最小二乘问题 (6.18)。所得最优系数向量非常稀疏，$30561$ 个系数中只有 $42$ 个非零。然后用这 $42$ 个基向量对原信号作最小二乘拟合。图 6.22 比较了所得结果 $\widehat y$ 与原信号 $y$。上图画出了近似信号（虚线），以及与它几乎无法区分的原信号 $y(t)$（实线）。下图画出了误差 $y(t)-\widehat y(t)$。从图中可以清楚地看出，我们得到了一个</p>

<!-- pdf-page: 351 -->

<figure id="fig-6-23" data-figure="6.23" data-no-english-text="true" data-reader-after="basis-pursuit-relative-error">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-23.png" alt="上图为频率随时间变化的原始信号；下图为时频图，所选基元素对应的圆圈紧邻表示原始信号瞬时频率的虚线曲线" data-source-page="351" data-source-rect="120,123,430,361">
<figcaption>图 6.23 上图：原始信号。下图：时频图。虚线曲线表示原始信号的瞬时频率 $\omega(t)=150|\cos(5t)|$。每个圆圈对应通过基追踪得到的逼近中选用的一个基元素。横轴表示该基元素的时间索引 $\tau$，纵轴表示其频率索引 $\omega$。</figcaption>
</figure>

<p id="basis-pursuit-fit-end" markdown="1" data-reader-continue="basis-pursuit-fit-start">相对误差很小的近似 $\widehat y$。相对误差为</p>

<div id="basis-pursuit-relative-error" markdown="1">

$$
\frac{(1/501)\sum_{i=1}^{501}(y(t_i)-\widehat y(t_i))^2}
{(1/501)\sum_{i=1}^{501}y(t_i)^2}=2.6\cdot10^{-4}.
$$

</div>

把非零系数的位置按时间和频率画出来，就得到对原始数据的时频分析。图 6.23 给出了这样的图，同时画出了瞬时频率。可以看到，非零分量紧密地跟随瞬时频率。

### 6.5.5 用凸函数插值

在某些特殊情形下，可以用有限维凸优化来求解涉及无穷维函数集合的插值问题。本节介绍一个例子。

先考虑如下问题：在什么条件下，存在一个凸函数 $f:\mathbf{R}^k\to\mathbf{R}$，$\operatorname{\mathbf{dom}}f=\mathbf{R}^k$，使它在给定点处满足插值条件

$$
f(u_i)=y_i,\qquad i=1,\ldots,m,
$$

<!-- pdf-page: 352 -->

其中 $u_i\in\mathbf{R}^k$？（这里不要求 $f$ 属于任何有限维函数子空间。）答案是：当且仅当存在 $g_1,\ldots,g_m$，使得

$$
y_j\geq y_i+g_i^T(u_j-u_i),\qquad i,j=1,\ldots,m.
\tag{6.19}
$$

为说明这一点，先假设 $f$ 是凸函数，$\operatorname{\mathbf{dom}}f=\mathbf{R}^k$，且 $f(u_i)=y_i$，$i=1,\ldots,m$。在每个 $u_i$ 处，都可以找到一个向量 $g_i$，使得对所有 $z$ 有

$$
f(z)\geq f(u_i)+g_i^T(z-u_i).
\tag{6.20}
$$

如果 $f$ 可微，可以取 $g_i=\nabla f(u_i)$；在更一般的情形下，可以通过寻找 $\operatorname{\mathbf{epi}}f$ 在 $(u_i,y_i)$ 处的一个支撑超平面来构造 $g_i$。（向量 $g_i$ 称为**次梯度**（subgradients）。）在 (6.20) 中取 $z=u_j$，就得到 (6.19)。

反过来，假设 $g_1,\ldots,g_m$ 满足 (6.19)。对所有 $z\in\mathbf{R}^k$，定义 $f$ 为

$$
f(z)=\max_{i=1,\ldots,m}(y_i+g_i^T(z-u_i)).
$$

显然，$f$ 是一个（分段线性）凸函数。不等式 (6.19) 蕴含 $f(u_i)=y_i$，$i=1,\ldots,m$。

利用这个结果，可以求解若干涉及凸函数插值、逼近或求界的问题。

#### 用凸函数拟合给定数据

最简单的应用也许是计算凸函数对给定数据 $(u_i,y_i)$，$i=1,\ldots,m$ 的最小二乘拟合：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m(y_i-f(u_i))^2\\
\text{约束条件} & f:\mathbf{R}^k\to\mathbf{R}\text{ 为凸函数},\quad\operatorname{\mathbf{dom}}f=\mathbf{R}^k.
\end{array}
$$

这是一个无穷维问题，因为变量是 $f$，它属于 $\mathbf{R}^k$ 上的连续实值函数空间。利用上述结果，可以将这个问题写成

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m(y_i-\widehat y_i)^2\\
\text{约束条件} & \widehat y_j\geq\widehat y_i+g_i^T(u_j-u_i),\quad i,j=1,\ldots,m,
\end{array}
$$

这是一个 QP，变量为 $\widehat y\in\mathbf{R}^m$ 和 $g_1,\ldots,g_m\in\mathbf{R}^k$。这个问题的最优值为零，当且仅当给定数据可以由某个凸函数插值，即存在满足 $f(u_i)=y_i$ 的凸函数。图 6.24 给出了一个例子。

#### 确定插值凸函数的取值界限

再看一个简单例子。假设给定数据 $(u_i,y_i)$，$i=1,\ldots,m$，且这些数据可以由凸函数插值。希望确定 $f(u_0)$ 的可能取值范围，其中 $u_0$ 是 $\mathbf{R}^k$ 中的另一个点，$f$ 是对给定数据进行插值的任意凸函数。为了找到 $f(u_0)$ 的最小可能值，求解 LP

$$
\begin{array}{ll}
\text{最小化} & y_0\\
\text{约束条件} & y_j\geq y_i+g_i^T(u_j-u_i),\quad i,j=0,\ldots,m,
\end{array}
$$

<!-- pdf-page: 353 -->

<figure id="fig-6-24" data-figure="6.24" data-no-english-text="true" data-reader-after="convex-interpolation-bound-end">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-24.png" alt="用凸的分段线性函数拟合圆圈数据点，折线在左侧下降，中部缓慢上升，右侧快速上升" data-source-page="353" data-source-rect="175,123,394,279">
<figcaption>图 6.24 用凸函数对圆圈所示的数据进行最小二乘拟合。图中所示的（分段线性）函数在所有凸函数中使拟合误差的平方和最小。</figcaption>
</figure>

<p id="convex-interpolation-bound-end" markdown="1">其中变量为 $y_0\in\mathbf{R}$、$g_0,\ldots,g_m\in\mathbf{R}^k$。通过最大化 $y_0$（这同样是一个 LP），就能找到对给定数据进行插值的凸函数在 $u_0$ 处的最大可能值。</p>

#### 用单调凸函数插值

作为凸插值的扩展，可以考虑用单调非减的凸函数进行插值。可以证明，存在凸函数 $f:\mathbf{R}^k\to\mathbf{R}$，$\operatorname{\mathbf{dom}}f=\mathbf{R}^k$，满足插值条件

$$
f(u_i)=y_i,\qquad i=1,\ldots,m,
$$

并且单调非减（即只要 $u\succeq v$，就有 $f(u)\geq f(v)$），当且仅当存在 $g_1,\ldots,g_m\in\mathbf{R}^k$，使得

$$
g_i\succeq0,\quad i=1,\ldots,m,\qquad
y_j\geq y_i+g_i^T(u_j-u_i),\quad i,j=1,\ldots,m.
\tag{6.21}
$$

换言之，就是在凸插值条件 (6.19) 中加入所有次梯度 $g_i$ 非负的条件。（见习题 6.12。）

#### 确定消费者偏好的范围

作为应用，考虑预测消费者偏好的问题。不同的**商品组合**（baskets of goods）由 $n$ 种消费品的不同数量组成。一个商品组合用向量 $x\in[0,1]^n$ 表示，其中 $x_i$ 表示第 $i$ 种消费品的数量。假设这些数量已经归一化，使得 $0\leq x_i\leq1$，即 $x_i=0$ 是第 $i$ 种商品的最小可能数量，$x_i=1$ 是最大可能数量。给定两个商品组合 $x$ 和 $\widetilde x$，消费者可能更偏好 $x$，也可能更偏好 $\widetilde x$，或者认为两者同样有吸引力。考虑一个选择具有可重复性的模型消费者。

<!-- pdf-page: 354 -->

用如下方式建立消费者偏好模型。假设存在一个潜在的**效用函数** $u:\mathbf{R}^n\to\mathbf{R}$，定义域为 $[0,1]^n$；$u(x)$ 衡量消费者从商品组合 $x$ 获得的效用。在两个商品组合之间选择时，消费者会选择效用较大的一个；若两者效用相同，则没有偏向。假设 $u$ 单调非减是合理的。这意味着，在其他商品数量保持不变时，消费者总是更愿意拥有更多的某一种商品。假设 $u$ 为凹函数也合理。这描述了**饱和效应**：随着商品数量增加，边际效用递减。

现在假设给定一些消费者偏好数据，但不知道潜在的效用函数 $u$。具体来说，有一组商品组合 $a_1,\ldots,a_m\in[0,1]^n$，以及它们之间的部分偏好信息：

$$
u(a_i)>u(a_j)\quad\text{对 }(i,j)\in\mathcal{P},\qquad
u(a_i)\geq u(a_j)\quad\text{对 }(i,j)\in\mathcal{P}_{\mathrm{weak}},
\tag{6.22}
$$

其中给定 $\mathcal{P},\mathcal{P}_{\mathrm{weak}}\subseteq\{1,\ldots,m\}\times\{1,\ldots,m\}$。$\mathcal{P}$ 表示已知偏好的集合：$(i,j)\in\mathcal{P}$ 意味着已知消费者更偏好商品组合 $a_i$ 而非 $a_j$。集合 $\mathcal{P}_{\mathrm{weak}}$ 表示已知弱偏好的集合：$(i,j)\in\mathcal{P}_{\mathrm{weak}}$ 意味着消费者更偏好 $a_i$，或者认为 $a_i$ 与 $a_j$ 同样有吸引力。

先考虑如下问题：如何确定给定数据是否一致，也就是是否存在一个凹且非减的效用函数 $u$，使 (6.22) 成立？这等价于求解可行性问题

$$
\begin{array}{ll}
\text{求} & u\\
\text{约束条件} & u:\mathbf{R}^n\to\mathbf{R}\text{ 为凹且非减的函数}\\
& u(a_i)>u(a_j),\quad(i,j)\in\mathcal{P}\\
& u(a_i)\geq u(a_j),\quad(i,j)\in\mathcal{P}_{\mathrm{weak}},
\end{array}
\tag{6.23}
$$

其中函数 $u$ 是（无穷维）优化变量。由于 (6.23) 中的约束都是齐次的，可以将问题写成等价形式

$$
\begin{array}{ll}
\text{求} & u\\
\text{约束条件} & u:\mathbf{R}^n\to\mathbf{R}\text{ 为凹且非减的函数}\\
& u(a_i)\geq u(a_j)+1,\quad(i,j)\in\mathcal{P}\\
& u(a_i)\geq u(a_j),\quad(i,j)\in\mathcal{P}_{\mathrm{weak}},
\end{array}
\tag{6.24}
$$

其中只使用非严格不等式。（显然，若 $u$ 满足 (6.24)，就一定满足 (6.23)；反过来，若 $u$ 满足 (6.23)，则可以将它缩放，使其满足 (6.24)。）利用第 339 页的插值结果，这个问题又可以写成一个（有限维）线性规划可行性问题：

$$
\begin{array}{ll}
\text{求} & u_1,\ldots,u_m,g_1,\ldots,g_m\\
\text{约束条件} & g_i\succeq0,\quad i=1,\ldots,m\\
& u_j\leq u_i+g_i^T(a_j-a_i),\quad i,j=1,\ldots,m\\
& u_i\geq u_j+1,\quad(i,j)\in\mathcal{P}\\
& u_i\geq u_j,\quad(i,j)\in\mathcal{P}_{\mathrm{weak}}.
\end{array}
\tag{6.25}
$$

通过求解这个线性规划可行性问题，可以确定是否存在一个凹且非减的效用函数，与给定的<!-- pdf-page: 355 -->严格偏好和非严格偏好集合一致。如果 (6.25) 可行，就至少存在一个这样的效用函数（实际上，可以由可行的 $u_1,\ldots,u_m,g_1,\ldots,g_m$ 构造一个分段线性效用函数）。如果 (6.25) 不可行，就可以断定，不存在与给定严格偏好和非严格偏好集合一致的凹且递增的效用函数。

例如，假设已知消费者偏好 $\mathcal{P}$ 和 $\mathcal{P}_{\mathrm{weak}}$ 至少与一个凹且递增的效用函数一致。考虑既不属于 $\mathcal{P}$ 也不属于 $\mathcal{P}_{\mathrm{weak}}$ 的一对 $(k,l)$，即消费者对商品组合 $k$ 和 $l$ 的偏好未知。在某些情形下，即使不知道潜在的偏好函数，也能确定商品组合 $k$ 和 $l$ 之间存在某种偏好。为此，在已知偏好 (6.22) 中加入不等式 $u(a_k)\leq u(a_l)$，它表示消费者更偏好商品组合 $l$ 而非 $k$，或者认为两者同样有吸引力。然后求解包含这个额外弱偏好 $u(a_k)\leq u(a_l)$ 的可行性线性规划 (6.25)。如果扩充后的偏好集合不可行，就说明任何与原始给定消费者偏好数据一致的凹非减效用函数，都必须满足 $u(a_k)>u(a_l)$。换言之，无须知道潜在的效用函数，就能断定消费者更偏好商品组合 $k$ 而非 $l$。

<div class="example" markdown="1">

**例 6.9** 下面给出一个简单的数值例子来说明上述讨论。考虑由两种商品组成的商品组合（这样就很容易画出各个组合）。为了生成消费者偏好数据 $\mathcal{P}$，在 $[0,1]^2$ 中生成 $40$ 个随机点，再用效用函数

$$
u(x_1,x_2)=(1.1x_1^{1/2}+0.8x_2^{1/2})/1.9
$$

来比较它们。图 6.25 给出了这些商品组合，以及效用函数 $u$ 的几条等值曲线。

现在利用消费者偏好数据（当然，不使用真实效用函数 $u$），将这 $40$ 个商品组合逐一与商品组合 $a_0=(0.5,0.5)$ 比较。对每个原始组合 $a_i$，求解上述线性规划可行性问题，看能否断定消费者更偏好 $a_0$ 而非 $a_i$。同样，也检查能否断定消费者更偏好 $a_i$ 而非 $a_0$。对每个组合 $a_i$，有三种可能结果：可以断定 $a_0$ 一定优于 $a_i$，或者 $a_i$ 一定优于 $a_0$，或者（当两个 LP 可行性问题都可行时）无法得出结论。（这里，“一定优于”是指对于任何与原始给定数据一致的凹非减效用函数，该偏好都成立。）

结果发现，有 $21$ 个商品组合一定不如 $(0.5,0.5)$，有 $14$ 个一定优于它。对于剩下的 $5$ 个商品组合，无法仅由消费者偏好数据得出结论。图 6.26 给出了这些结果。注意，仅利用效用函数的单调性，就能确定 $(0.5,0.5)$ 左下方的商品组合一定不如 $(0.5,0.5)$；类似地，右上方的点一定优于它。因此，对于这 $17$ 个点，无须求解可行性 LP (6.25)。不过，要对另外两个象限中的 $23$ 个点进行分类，就需要凹性假设，并求解可行性 LP (6.25)。

</div>

<!-- pdf-page: 356 -->

<figure id="fig-6-25" data-figure="6.25" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-25.png" alt="单位正方形中的四十个圆圈表示两种商品的不同数量组合，九条虚线表示真实效用函数从零点一至零点九的等高线" data-source-page="356" data-source-rect="216,121,448,307">
<figcaption>图 6.25 40 个商品组合 $a_1,\ldots,a_{40}$，以圆圈表示。真实效用函数 $u$ 取值为 $0.1,\ 0.2,\ldots,0.9$ 的等高线以虚线表示。利用这个效用函数可以得到这 40 个商品组合之间的消费者偏好数据 $\mathcal{P}$。</figcaption>
</figure>

<figure id="fig-6-26" data-figure="6.26" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-26.png" alt="相对于新商品组合零点五、零点五的偏好分析；空心圆表示确定不如新组合的点，黑色实心圆表示确定优于新组合的点，方框表示无法判定的点，虚线为通过新组合的真实效用等高线" data-source-page="356" data-source-rect="216,374,448,560">
<figcaption>图 6.26 针对新商品组合 $a_0=(0.5,0.5)$，利用 LP（6.25）进行消费者偏好分析的结果。对于原有商品组合，若能确定它不如新组合（$u(a_k)<u(a_0)$），则以空心圆表示；若能确定它优于新组合（$u(a_k)>u(a_0)$），则以黑色实心圆表示；若无法作出判断，则以方框表示。真实效用函数通过 $(0.5,0.5)$ 的等高线以虚线曲线表示。通过 $(0.5,0.5)$ 的竖直线和水平线把 $[0,1]^2$ 分成四个象限。根据对 $u$ 的单调性假设，右上象限中的点一定优于 $(0.5,0.5)$。同样，$(0.5,0.5)$ 一定优于左下象限中的点。对于另外两个象限中的点，结果并不显然。</figcaption>
</figure>

<!-- pdf-page: 357 -->

## 文献说明

Huber [Hub64, Hub81] 分析了采用不同罚函数进行逼近时的鲁棒性，并提出了罚函数 (6.4)。对数障碍罚函数出现在控制理论中，用于系统的闭环频率响应，并有多个名称，例如中心 $H_\infty$（central $H_\infty$）控制或风险厌恶控制（risk-averse control）；见 Boyd 和 Barratt [BB91] 及其中的参考文献。

许多书都介绍了正则化逼近，包括 Tikhonov 和 Arsenin [TA77] 以及 Hansen [Han98]。Tikhonov 正则化有时称为**岭回归**（ridge regression；Golub 和 Van Loan [GL89，第 564 页]）。采用 $\ell_1$ 范数正则化的最小二乘逼近也称为 **lasso**（Tibshirani [Tib96]）。Hastie、Tibshirani 和 Friedman [HTF01, §3.4] 讨论并比较了其他最小二乘正则化与回归变量选择技术。

Rudin、Osher 和 Fatemi [ROF92] 在图像重构中引入了总变差去噪。

El Ghaoui 和 Lebret [EL97]，以及 Chandrasekaran、Golub、Gu 和 Sayed [CGGS98] 提出了具有范数有界不确定性的鲁棒最小二乘问题（第 321 页）。El Ghaoui 和 Lebret 还给出了具有结构化不确定性的鲁棒最小二乘问题（第 323 页）的 SDP 表述。

Chen、Donoho 和 Saunders [CDS01] 讨论了通过线性规划进行基追踪的方法。他们将 $\ell_1$ 范数正则化问题 (6.18) 称为**基追踪去噪**（basis pursuit denoising）。Meyer 和 Pratt [MP68] 是一篇研究效用函数界限问题的早期论文。

<!-- pdf-page: 358 -->

## 习题

### 范数逼近与最小范数问题

**6.1 对数障碍罚函数的二次界。** 设 $\phi:\mathbf{R}\to\mathbf{R}$ 是界限为 $a>0$ 的对数障碍罚函数：

$$
\phi(u)=\begin{cases}
-a^2\log(1-(u/a)^2) & |u|<a,\\
\infty & \text{其他情形}.
\end{cases}
$$

证明：如果 $u\in\mathbf{R}^m$ 满足 $\|u\|_\infty<a$，则

$$
\|u\|_2^2\leq\sum_{i=1}^m\phi(u_i)
\leq\frac{\phi(\|u\|_\infty)}{\|u\|_\infty^2}\|u\|_2^2.
$$

这意味着，当 $\|u\|_\infty$ 与 $a$ 相比很小时，$\|u\|_2^2$ 能很好地近似 $\sum_{i=1}^m\phi(u_i)$。例如，如果 $\|u\|_\infty/a=0.25$，则

$$
\|u\|_2^2\leq\sum_{i=1}^m\phi(u_i)\leq1.033\cdot\|u\|_2^2.
$$

**6.2 用常向量作 $\ell_1$、$\ell_2$ 和 $\ell_\infty$ 范数逼近。** 对于只有一个标量变量 $x\in\mathbf{R}$ 的范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|x\mathbf{1}-b\|,
\end{array}
$$

采用 $\ell_1$、$\ell_2$ 和 $\ell_\infty$ 范数时，解分别是什么？

**6.3** 将下列逼近问题写成 LP、QP、SOCP 或 SDP。问题数据为 $A\in\mathbf{R}^{m\times n}$ 和 $b\in\mathbf{R}^m$。$A$ 的各行记作 $a_i^T$。

- (a) **死区线性罚函数逼近：** 最小化 $\sum_{i=1}^m\phi(a_i^Tx-b_i)$，其中

    $$
    \phi(u)=\begin{cases}
    0 & |u|\leq a,\\
    |u|-a & |u|>a,
    \end{cases}
    $$

    且 $a>0$。

- (b) **对数障碍罚函数逼近：** 最小化 $\sum_{i=1}^m\phi(a_i^Tx-b_i)$，其中

    $$
    \phi(u)=\begin{cases}
    -a^2\log(1-(u/a)^2) & |u|<a,\\
    \infty & |u|\geq a,
    \end{cases}
    $$

    且 $a>0$。

- (c) **Huber 罚函数逼近：** 最小化 $\sum_{i=1}^m\phi(a_i^Tx-b_i)$，其中

    $$
    \phi(u)=\begin{cases}
    u^2 & |u|\leq M,\\
    M(2|u|-M) & |u|>M,
    \end{cases}
    $$

    且 $M>0$。

- (d) **对数 Chebyshev 逼近：** 最小化 $\max_{i=1,\ldots,m}|\log(a_i^Tx)-\log b_i|$。假设 $b\succ0$。一个等价的凸形式为

    $$
    \begin{array}{ll}
    \text{最小化} & t\\
    \text{约束条件} & 1/t\leq a_i^Tx/b_i\leq t,\quad i=1,\ldots,m,
    \end{array}
    $$

    其中变量为 $x\in\mathbf{R}^n$ 和 $t\in\mathbf{R}$，定义域为 $\mathbf{R}^n\times\mathbf{R}_{++}$。

    <!-- pdf-page: 359 -->

- (e) **最小化最大的 $k$ 个残差之和：**

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{i=1}^k|r|_{[i]}\\
    \text{约束条件} & r=Ax-b,
    \end{array}
    $$

    其中 $|r|_{[1]}\geq|r|_{[2]}\geq\cdots\geq|r|_{[m]}$ 是将 $|r_1|,|r_2|,\ldots,|r_m|$ 按降序排列后的结果。（当 $k=1$ 时，这退化为 $\ell_\infty$ 范数逼近；当 $k=m$ 时，则退化为 $\ell_1$ 范数逼近。）*提示：* 见习题 5.19。

**6.4 $\ell_1$ 范数逼近的可微近似。** 带参数 $\epsilon>0$ 的函数 $\phi(u)=(u^2+\epsilon)^{1/2}$，有时用作绝对值函数 $|u|$ 的可微近似。为了近似求解 $\ell_1$ 范数逼近问题

$$
\begin{array}{ll}
\text{最小化} & \|Ax-b\|_1,
\end{array}
\tag{6.26}
$$

其中 $A\in\mathbf{R}^{m\times n}$，转而求解问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m\phi(a_i^Tx-b_i),
\end{array}
\tag{6.27}
$$

其中 $a_i^T$ 是 $A$ 的第 $i$ 行。假设 $\operatorname{\mathbf{rank}}A=n$。

用 $p^\star$ 表示 $\ell_1$ 范数逼近问题 (6.26) 的最优值。用 $\widehat x$ 表示近似问题 (6.27) 的最优解，用 $\widehat r$ 表示相应残差，$\widehat r=A\widehat x-b$。

- (a) 证明 $p^\star\geq\sum_{i=1}^m\widehat r_i^2/(\widehat r_i^2+\epsilon)^{1/2}$。

- (b) 证明

    $$
    \|A\widehat x-b\|_1\leq p^\star+
    \sum_{i=1}^m|\widehat r_i|\left(1-\frac{|\widehat r_i|}{(\widehat r_i^2+\epsilon)^{1/2}}\right).
    $$

（计算出 $\widehat x$ 后，再计算右端，就能得到 $\widehat x$ 对 $\ell_1$ 范数逼近问题的次优程度的一个界。）

**6.5 最小长度逼近。** 考虑问题

$$
\begin{array}{ll}
\text{最小化} & \operatorname{length}(x)\\
\text{约束条件} & \|Ax-b\|\leq\epsilon,
\end{array}
$$

其中 $\operatorname{length}(x)=\min\{k\mid x_i=0\text{ 对 }i>k\}$。问题变量为 $x\in\mathbf{R}^n$；问题参数为 $A\in\mathbf{R}^{m\times n}$、$b\in\mathbf{R}^m$ 和 $\epsilon>0$。在回归语境中，要求按原顺序选取 $A$ 的前若干列，使它们能以不超过 $\epsilon$ 的误差逼近向量 $b$，并使所取列数最少。

证明这是一个拟凸优化问题。

**6.6 一些罚函数逼近问题的对偶。** 对于下面各个罚函数 $\phi:\mathbf{R}\to\mathbf{R}$，推导问题

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\sum_{i=1}^m\phi(r_i)\\
\text{约束条件} & r=Ax-b,
\end{array}
$$

的一个拉格朗日对偶。变量为 $x\in\mathbf{R}^n$、$r\in\mathbf{R}^m$。

- (a) **死区线性罚函数**（死区宽度为 $a=1$）：

    $$
    \phi(u)=\begin{cases}
    0 & |u|\leq1\\
    |u|-1 & |u|>1.
    \end{cases}
    $$

- (b) **Huber 罚函数**（$M=1$）：

    $$
    \phi(u)=\begin{cases}
    u^2 & |u|\leq1\\
    2|u|-1 & |u|>1.
    \end{cases}
    $$

    <!-- pdf-page: 360 -->

- (c) **对数障碍罚函数**（界限为 $a=1$）：

    $$
    \phi(u)=-\log(1-u^2),\qquad\operatorname{\mathbf{dom}}\phi=(-1,1).
    $$

- (d) **相对 1 的偏差**：

    $$
    \phi(u)=\max\{u,1/u\}=\begin{cases}
    u & u\geq1\\
    1/u & u\leq1,
    \end{cases}
    $$

    其中 $\operatorname{\mathbf{dom}}\phi=\mathbf{R}_{++}$。

### 正则化与鲁棒逼近

**6.7 采用欧几里得范数的双准则优化。** 考虑双准则优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }\mathbf{R}_+^2\text{）} & (\|Ax-b\|_2^2,\ \|x\|_2^2),
\end{array}
$$

其中 $A\in\mathbf{R}^{m\times n}$ 的秩为 $r$，$b\in\mathbf{R}^m$。说明如何利用 $A$ 的奇异值分解

$$
A=U\operatorname{\mathbf{diag}}(\sigma)V^T=\sum_{i=1}^r\sigma_i u_i v_i^T
$$

（见 §A.5.4），求出下面各个问题的解。

- (a) **Tikhonov 正则化：** 最小化 $\|Ax-b\|_2^2+\delta\|x\|_2^2$。

- (b) 在约束 $\|x\|_2^2=\gamma$ 下，最小化 $\|Ax-b\|_2^2$。

- (c) 在约束 $\|x\|_2^2=\gamma$ 下，最大化 $\|Ax-b\|_2^2$。

这里 $\delta$ 和 $\gamma$ 是正参数。

你的结果将为计算这个双准则问题的最优权衡曲线和可达值集合提供高效方法。

**6.8** 将下面的鲁棒逼近问题表述为 LP、QP、SOCP 或 SDP。对每个小问，分别考虑 $\ell_1$、$\ell_2$ 和 $\ell_\infty$ 范数。

- (a) **参数取值只有有限个的随机鲁棒逼近**，即范数和问题

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{i=1}^k p_i\|A_i x-b\|
    \end{array}
    $$

    其中 $p\succeq0$ 且 $\mathbf{1}^Tp=1$。（见 §6.4.1。）

- (b) **系数有上下界的最坏情形鲁棒逼近：**

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sup_{A\in\mathcal{A}}\|Ax-b\|
    \end{array}
    $$

    其中

    $$
    \mathcal{A}=\{A\in\mathbf{R}^{m\times n}\mid l_{ij}\leq a_{ij}\leq u_{ij},\ i=1,\ldots,m,\ j=1,\ldots,n\}.
    $$

    这里通过给出 $A$ 各个元素的上下界来描述不确定性集合。假设 $l_{ij}<u_{ij}$。

- (c) **具有多面体不确定性的最坏情形鲁棒逼近：**

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sup_{A\in\mathcal{A}}\|Ax-b\|
    \end{array}
    $$

    其中

    $$
    \mathcal{A}=\{[a_1\ \cdots\ a_m]^T\mid C_i a_i\preceq d_i,\ i=1,\ldots,m\}.
    $$

    不确定性通过给出每一行的可能取值所构成的多面体 $\mathcal{P}_i=\{a_i\mid C_i a_i\preceq d_i\}$ 来描述。参数 $C_i\in\mathbf{R}^{p_i\times n}$、$d_i\in\mathbf{R}^{p_i}$，$i=1,\ldots,m$，均已给定。假设多面体 $\mathcal{P}_i$ 非空且有界。

<!-- pdf-page: 361 -->

### 函数拟合与插值

**6.9 极小极大有理函数拟合。** 证明下面的问题是拟凸的：

$$
\begin{array}{ll}
\text{最小化} & \displaystyle\max_{i=1,\ldots,k}\left|\frac{p(t_i)}{q(t_i)}-y_i\right|
\end{array}
$$

其中

$$
p(t)=a_0+a_1t+a_2t^2+\cdots+a_m t^m,\qquad
q(t)=1+b_1t+\cdots+b_n t^n,
$$

目标函数的定义域定义为

$$
D=\{(a,b)\in\mathbf{R}^{m+1}\times\mathbf{R}^n\mid q(t)>0,\ \alpha\leq t\leq\beta\}.
$$

在这个问题中，我们用有理函数 $p(t)/q(t)$ 拟合给定数据，同时约束分母多项式在区间 $[\alpha,\beta]$ 上为正。优化变量为分子和分母的系数 $a_i$、$b_i$。插值点 $t_i\in[\alpha,\beta]$ 以及期望函数值 $y_i$，$i=1,\ldots,k$，均已给定。

**6.10 用凹、非负且非减的二次函数拟合数据。** 给定数据

$$
x_1,\ldots,x_N\in\mathbf{R}^n,\qquad y_1,\ldots,y_N\in\mathbf{R},
$$

我们希望拟合一个形如

$$
f(x)=(1/2)x^TPx+q^Tx+r,
$$

的二次函数，其中 $P\in\mathbf{S}^n$、$q\in\mathbf{R}^n$ 和 $r\in\mathbf{R}$ 是模型中的参数（因此也是拟合问题中的变量）。

这个模型只在盒 $\mathcal{B}=\{x\in\mathbf{R}^n\mid l\preceq x\preceq u\}$ 上使用。可以假设 $l\prec u$，并且给定的数据点 $x_i$ 都位于这个盒内。

我们使用简单的误差平方和目标

$$
\sum_{i=1}^N(f(x_i)-y_i)^2,
$$

作为拟合的准则。此外，还对函数 $f$ 施加若干约束。首先，它必须是凹函数。其次，它在 $\mathcal{B}$ 上必须非负，即对于所有 $z\in\mathcal{B}$，都有 $f(z)\geq0$。第三，$f$ 在 $\mathcal{B}$ 上必须非减，即只要 $z,\widetilde{z}\in\mathcal{B}$ 满足 $z\preceq\widetilde{z}$，就有 $f(z)\leq f(\widetilde{z})$。

说明如何将这个拟合问题表述为一个凸问题。尽量简化你的表述。

**6.11 最小二乘方向插值。** 设 $F_1,\ldots,F_n:\mathbf{R}^k\to\mathbf{R}^p$，将它们作线性组合，得到 $F:\mathbf{R}^k\to\mathbf{R}^p$，

$$
F(u)=x_1F_1(u)+\cdots+x_nF_n(u),
$$

其中 $x$ 是插值问题的变量。

在这个问题中，我们要求 $\angle(F(v_j),q_j)=0$，$j=1,\ldots,m$，其中 $q_j$ 是给定的 $\mathbf{R}^p$ 中的向量，并假设满足 $\|q_j\|_2=1$。换言之，要求 $F$ 在各点 $v_j$ 处的方向取指定的值。为了确保 $F(v_j)$ 不为零（否则夹角没有定义），还施加最小长度约束 $\|F(v_j)\|_2\geq\epsilon$，$j=1,\ldots,m$，其中 $\epsilon>0$ 是给定的。

说明如何用凸优化求出使 $\|x\|^2$ 最小、并满足上述方向条件（及最小长度条件）的 $x$。

**6.12 用单调函数插值。** 如果只要 $u\succeq v$ 就有 $f(u)\geq f(v)$，就称函数 $f:\mathbf{R}^k\to\mathbf{R}$（关于 $\mathbf{R}_+^k$）单调非减。

<!-- pdf-page: 362 -->

- (a) 证明：存在单调非减函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当

    $$
    y_i\geq y_j\quad\text{只要 }u_i\succeq u_j,\qquad i,j=1,\ldots,m.
    $$

- (b) 证明：存在定义域为 $\operatorname{\mathbf{dom}}f=\mathbf{R}^k$ 的凸且单调非减的函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当存在 $g_i\in\mathbf{R}^k$，$i=1,\ldots,m$，使得

    $$
    g_i\succeq0,\quad i=1,\ldots,m,\qquad
    y_j\geq y_i+g_i^T(u_j-u_i),\quad i,j=1,\ldots,m.
    $$

**6.13 用拟凸函数插值。** 证明：存在拟凸函数 $f:\mathbf{R}^k\to\mathbf{R}$，满足 $f(u_i)=y_i$，$i=1,\ldots,m$，当且仅当存在 $g_i\in\mathbf{R}^k$，$i=1,\ldots,m$，使得

$$
g_i^T(u_j-u_i)\leq-1\quad\text{只要 }y_j<y_i,\qquad i,j=1,\ldots,m.
$$

**6.14 [Nes00] 用正实函数插值。** 设 $z_1,\ldots,z_n\in\mathbf{C}$ 是 $n$ 个互不相同的点，且 $|z_i|>1$。将 $K_{\mathrm{np}}$ 定义为所有满足如下条件的向量 $y\in\mathbf{C}^n$ 构成的集合：存在函数 $f:\mathbf{C}\to\mathbf{C}$，使得以下条件成立。

- $f$ 是**正实函数（positive-real function）**，也就是说，它在单位圆外（即 $|z|>1$）解析，且在单位圆外实部非负（$|z|>1$ 时 $\Re f(z)\geq0$）。

- $f$ 满足插值条件

    $$
    f(z_1)=y_1,\qquad f(z_2)=y_2,\qquad\ldots,\qquad f(z_n)=y_n.
    $$

若用 $\mathcal{F}$ 表示正实函数的集合，就可以将 $K_{\mathrm{np}}$ 写为

$$
K_{\mathrm{np}}=\{y\in\mathbf{C}^n\mid\exists f\in\mathcal{F},\ y_k=f(z_k),\ k=1,\ldots,n\}.
$$

- (a) 可以证明，$f$ 为正实函数，当且仅当存在一个非减函数 $\rho$，使得对所有满足 $|z|>1$ 的 $z$，都有

    $$
    f(z)=i\Im f(\infty)+\int_0^{2\pi}\frac{e^{i\theta}+z^{-1}}{e^{i\theta}-z^{-1}}\,d\rho(\theta),
    $$

    其中 $i=\sqrt{-1}$（见 [KN77，第 389 页]）。利用这种表示证明 $K_{\mathrm{np}}$ 是闭凸锥。

- (b) 对于向量 $x,y\in\mathbf{C}^n$，我们使用内积 $\Re(x^Hy)$，其中 $x^H$ 表示 $x$ 的共轭转置。证明 $K_{\mathrm{np}}$ 的对偶锥为

    $$
    K_{\mathrm{np}}^*=\left\{x\in\mathbf{C}^n\ \middle|\ \Im(\mathbf{1}^Tx)=0,\ \Re\left(\sum_{l=1}^nx_l\frac{e^{-i\theta}+\bar z_l^{-1}}{e^{-i\theta}-\bar z_l^{-1}}\right)\geq0\ \forall\theta\in[0,2\pi]\right\}.
    $$

- (c) 证明

    $$
    K_{\mathrm{np}}^*=\left\{x\in\mathbf{C}^n\ \middle|\ \exists Q\in\mathbf{H}_+^n,\ x_l=\sum_{k=1}^n\frac{Q_{kl}}{1-z_k^{-1}\bar z_l^{-1}},\ l=1,\ldots,n\right\},
    $$

    其中 $\mathbf{H}_+^n$ 表示所有 $n\times n$ 半正定 Hermitian 矩阵构成的集合。

    使用下面的结论（称为 Riesz–Fejér 定理，见 [KN77，第 60 页]）：形如

    $$
    \sum_{k=0}^n(y_ke^{-ik\theta}+\bar y_ke^{ik\theta})
    $$

    的函数对所有 $\theta$ 均非负，当且仅当存在 $a_0,\ldots,a_n\in\mathbf{C}$，使得

    $$
    \sum_{k=0}^n(y_ke^{-ik\theta}+\bar y_ke^{ik\theta})=\left|\sum_{k=0}^na_ke^{ik\theta}\right|^2.
    $$

    <!-- pdf-page: 363 -->

- (d) 证明 $K_{\mathrm{np}}=\{y\in\mathbf{C}^n\mid P(y)\succeq0\}$，其中 $P(y)\in\mathbf{H}^n$ 定义为

    $$
    P(y)_{kl}=\frac{y_k+\bar y_l}{1-z_k^{-1}\bar z_l^{-1}},\qquad l,k=1,\ldots,n.
    $$

    矩阵 $P(y)$ 称为与各点 $z_k,y_k$ 对应的 **Nevanlinna–Pick 矩阵**。

    *提示：* 如 (a) 中所述，$K_{\mathrm{np}}$ 是闭凸锥，因此 $K_{\mathrm{np}}=K_{\mathrm{np}}^{**}$。

- (e) 作为一个应用，将下面的问题表述为凸优化问题：

    $$
    \begin{array}{ll}
    \text{最小化} & \displaystyle\sum_{k=1}^n|f(z_k)-w_k|^2\\
    \text{约束条件} & f\in\mathcal{F}.
    \end{array}
    $$

    问题数据为满足 $|z_k|>1$ 的 $n$ 个点 $z_k$，以及 $n$ 个复数 $w_1,\ldots,w_n$。我们在所有正实函数 $f$ 中进行优化。

<!-- pdf-page: 364 -->
