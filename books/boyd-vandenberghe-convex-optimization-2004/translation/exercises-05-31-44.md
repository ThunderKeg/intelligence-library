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
\text{约束条件} & W+\operatorname{diag}(\nu)\succeq0,
\end{array}
\tag{5.114}
$$

变量为 $\nu\in\mathbf{R}^n$。这个半定规划的最优值给出了划分问题 (5.113) 最优值的一个下界。在本题中，我们将推导另一个半定规划，它也给出两路划分问题最优值的一个下界，并探讨这两个半定规划之间的联系。

<!-- pdf-page: 300 -->

- (a) **矩阵形式的两路划分问题。** 证明，两路划分问题可以写成

    $$
    \begin{array}{ll}
    \text{最小化} & \operatorname{tr}(WX)\\
    \text{约束条件} & X\succeq0,\quad\operatorname{rank}X=1\\
    & X_{ii}=1,\quad i=1,\ldots,n,
    \end{array}
    $$

    变量为 $X\in\mathbf{S}^n$。**提示。** 证明：若 $X$ 可行，则它具有 $X=xx^T$ 的形式，其中 $x\in\mathbf{R}^n$ 满足 $x_i\in\{-1,1\}$，反之亦然。

- (b) **两路划分问题的半定规划松弛。** 利用 (a) 中的表述，可以构造松弛问题

    $$
    \begin{array}{ll}
    \text{最小化} & \operatorname{tr}(WX)\\
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

**5.44 非严格线性矩阵不等式的强择一系统。** 在第 270 页例 5.14 中，我们提到，系统

$$
Z\succeq0,\qquad\operatorname{tr}(GZ)>0,\qquad\operatorname{tr}(F_iZ)=0,\quad i=1,\ldots,n,
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
