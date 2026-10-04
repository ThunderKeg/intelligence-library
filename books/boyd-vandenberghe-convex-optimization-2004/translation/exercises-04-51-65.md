**4.51 向量优化中目标函数的单调变换。** 考虑向量优化问题 (4.56)。假设把目标函数 $f_0$ 替换为 $\phi\circ f_0$，得到一个新的向量优化问题，其中 $\phi:\mathbf{R}^q\to\mathbf{R}^q$ 满足

$$
u\preceq_K v,\quad u\ne v
\quad\Longrightarrow\quad
\phi(u)\preceq_K\phi(v),\quad\phi(u)\ne\phi(v).
$$

证明：点 $x$ 是其中一个问题的 Pareto 最优点（或最优点），当且仅当它是另一个问题的 Pareto 最优点（或最优点），因此这两个问题等价。特别地，将多准则问题的每个目标分别与一个递增函数复合，不会改变 Pareto 最优点。

**4.52 Pareto 最优点与可达值集合的边界。** 考虑一个锥为 $K$ 的向量优化问题。用 $\mathcal{P}$ 表示 Pareto 最优值的集合，用 $\mathcal{O}$ 表示可达目标值的集合。证明 $\mathcal{P}\subseteq\mathcal{O}\cap\operatorname{bd}\mathcal{O}$，即每个 Pareto 最优值都是一个可达目标值，而且位于可达目标值集合的边界上。

**4.53** 假设向量优化问题 (4.56) 是凸的。证明集合

$$
\mathcal{A}=\mathcal{O}+K
=\{t\in\mathbf{R}^q\mid f_0(x)\preceq_K t\text{ 对某个可行点 }x\text{ 成立}\},
$$

是凸集。再证明：$\mathcal{A}$ 的极小元素与 $\mathcal{O}$ 的极小点相同。

**4.54 标量化与最优点。** 假设一个向量优化问题（不一定是凸问题）有最优点 $x^\star$。证明：无论如何选择 $\lambda\succ_{K^*}0$，$x^\star$ 都是相应标量化问题的一个解。再证明其逆命题：如果一个点 $x$ 对任意选择的 $\lambda\succ_{K^*}0$ 都是标量化问题的解，那么它就是这个向量优化问题（不一定是凸问题）的最优点。

**4.55 加权和标量化的推广。** 在 §4.7.4 中，我们说明了如何把向量目标 $f_0:\mathbf{R}^n\to\mathbf{R}^q$ 替换为标量目标 $\lambda^Tf_0$（其中 $\lambda\succ_{K^*}0$），从而得到向量优化问题的 Pareto 最优解。设 $\psi:\mathbf{R}^q\to\mathbf{R}$ 是一个 $K$-递增函数，即满足

$$
u\preceq_K v,\quad u\ne v
\quad\Longrightarrow\quad\psi(u)<\psi(v).
$$

证明，问题

$$
\begin{array}{ll}
\text{最小化} & \psi(f_0(x))\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p
\end{array}
$$

<!-- pdf-page: 221 -->

的任意解，都是向量优化问题

$$
\begin{array}{ll}
\text{最小化（相对于 }K\text{）} & f_0(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p
\end{array}
$$

的 Pareto 最优点。注意，$\psi(u)=\lambda^Tu$（其中 $\lambda\succ_{K^*}0$）是一个特例。

作为一个相关的例子，证明：在多准则优化问题中（即 $f_0=F:\mathbf{R}^n\to\mathbf{R}^q$、$K=\mathbf{R}_+^q$ 的向量优化问题），标量优化问题

$$
\begin{array}{ll}
\text{最小化} & \max_{i=1,\ldots,q}F_i(x)\\
\text{约束条件} & f_i(x)\leq0,\quad i=1,\ldots,m\\
& h_i(x)=0,\quad i=1,\ldots,p,
\end{array}
$$

的唯一解是 Pareto 最优点。

### 其他问题

**4.56** [P. Parrilo] 考虑在一些凸集之并的凸包 $\operatorname{conv}\left(\bigcup_{i=1}^q C_i\right)$ 上，最小化凸函数 $f_0:\mathbf{R}^n\to\mathbf{R}$ 的问题。这些集合由凸不等式描述：

$$
C_i=\{x\mid f_{ij}(x)\leq0,\ j=1,\ldots,k_i\},
$$

其中 $f_{ij}:\mathbf{R}^n\to\mathbf{R}$ 是凸函数。我们的目标是把这个问题表述为凸优化问题。

一个直观的办法是引入变量 $x_1,\ldots,x_q\in\mathbf{R}^n$，并要求 $x_i\in C_i$；引入 $\theta\in\mathbf{R}^q$，并要求 $\theta\succeq0$、$\mathbf{1}^T\theta=1$；再引入变量 $x\in\mathbf{R}^n$，并要求 $x=\theta_1x_1+\cdots+\theta_qx_q$。这个等式约束不是变量的仿射函数，因此这种办法不能得到凸问题。

一种更巧妙的表述是

$$
\begin{array}{ll}
\text{最小化} & f_0(x)\\
\text{约束条件} & s_if_{ij}(z_i/s_i)\leq0,\quad i=1,\ldots,q,\quad j=1,\ldots,k_i\\
& \mathbf{1}^Ts=1,\quad s\succeq0\\
& x=z_1+\cdots+z_q,
\end{array}
$$

变量为 $z_1,\ldots,z_q\in\mathbf{R}^n$、$x\in\mathbf{R}^n$ 和 $s_1,\ldots,s_q\in\mathbf{R}$。（当 $s_i=0$ 时，若 $z_i=0$，则把 $s_if_{ij}(z_i/s_i)$ 取为 $0$；若 $z_i\ne0$，则取为 $\infty$。）解释为什么这个问题是凸的，并且与原问题等价。

**4.57 通信信道的容量。** 考虑一个通信信道，在 $t=1,2,\ldots$（例如以秒为单位）时，输入为 $X(t)\in\{1,\ldots,n\}$，输出为 $Y(t)\in\{1,\ldots,m\}$。输入与输出之间的关系由统计规律给出：

$$
p_{ij}=\operatorname{prob}(Y(t)=i\mid X(t)=j),
\quad i=1,\ldots,m,\quad j=1,\ldots,n.
$$

矩阵 $P\in\mathbf{R}^{m\times n}$ 称为**信道转移矩阵**（channel transition matrix），这种信道称为**离散无记忆信道**（discrete memoryless channel）。

Shannon 的一个著名结果指出：只要信息传输速率小于某个数 $C$，就能通过该通信信道传递信息，并使出错概率任意小。$C$ 称为**信道容量**（channel capacity），单位为比特／秒。Shannon 还证明，离散无记忆信道的容量可以通过求解一个优化问题得到。假设 $X$ 的概率分布记作 $x\in\mathbf{R}^n$，即

$$
x_j=\operatorname{prob}(X=j),\quad j=1,\ldots,n.
$$

<!-- pdf-page: 222 -->

$X$ 与 $Y$ 之间的**互信息**（mutual information）为

$$
I(X;Y)=\sum_{i=1}^m\sum_{j=1}^n x_jp_{ij}\log_2\frac{p_{ij}}{\sum_{k=1}^n x_kp_{ik}}.
$$

于是信道容量 $C$ 为

$$
C=\sup_x I(X;Y),
$$

其中上确界取遍输入 $X$ 的所有可能概率分布，也就是所有满足 $x\succeq0$、$\mathbf{1}^Tx=1$ 的 $x$。

说明如何用凸优化计算信道容量。

**提示：** 引入变量 $y=Px$，它给出输出 $Y$ 的概率分布；证明互信息可以写成

$$
I(X;Y)=c^Tx-\sum_{i=1}^m y_i\log_2 y_i,
$$

其中 $c_j=\sum_{i=1}^m p_{ij}\log_2 p_{ij}$，$j=1,\ldots,n$。

**4.58 最优消费。** 本题考虑如何在一段时间内，以最优方式消费（或花掉）一笔初始金额（或其他资产）$k_0$。变量为 $c_0,\ldots,c_T$，其中 $c_t\geq0$ 表示第 $t$ 期的消费量。消费量为 $c$ 时获得的效用为 $u(c)$，其中 $u:\mathbf{R}\to\mathbf{R}$ 是一个递增凹函数。消费带来的效用的现值为

$$
U=\sum_{t=0}^T\beta^t u(c_t),
$$

其中 $0<\beta<1$ 是折现因子。

用 $k_t$ 表示第 $t$ 期可用于投资的金额。假设这笔投资获得的收益为 $f(k_t)$，其中 $f:\mathbf{R}\to\mathbf{R}$ 是一个递增的凹投资收益函数，满足 $f(0)=0$。例如，如果资金每期按 $R\%$ 的利率获取单利，则 $f(a)=(R/100)a$。要消费的金额 $c_t$ 在期末取出，因此有递推关系

$$
k_{t+1}=k_t+f(k_t)-c_t,\quad t=0,\ldots,T.
$$

初始金额 $k_0>0$ 是给定的。我们要求 $k_t\geq0$，$t=1,\ldots,T+1$（不过，也可以考虑允许 $k_t<0$ 的更复杂模型）。

说明如何把最大化 $U$ 的问题表述为凸优化问题。解释你所建立的问题如何与本问题等价，以及二者之间的确切关系。

**提示：** 证明，可以把上述关于 $k_t$ 的递推关系替换为不等式

$$
k_{t+1}\leq k_t+f(k_t)-c_t,\quad t=0,\ldots,T.
$$

（解释：这些不等式允许你在每期扔掉一部分钱。）这种技巧的更一般形式见习题 4.6。

**4.59 鲁棒优化。** 在一些优化问题中，由于某些参数或因素无法控制或尚不清楚，目标函数和约束函数存在不确定性或变化。可以把目标函数和约束函数 $f_0,\ldots,f_m$ 写成优化变量 $x\in\mathbf{R}^n$ 与参数向量 $u\in\mathbf{R}^k$ 的函数，以此建立模型，其中 $u$ 的值未知，或者会发生变化。在随机优化<!-- pdf-page: 223 -->方法中，将参数向量 $u$ 建模为具有已知分布的随机变量，并使用期望值 $\mathbf{E}_u f_i(x,u)$。在最坏情况分析方法中，给定一个集合 $\mathcal{U}$，并且知道 $u$ 属于这个集合；此时使用最大值或最坏情况值 $\sup_{u\in\mathcal{U}}f_i(x,u)$。为简化讨论，假设没有等式约束。

- (a) **随机优化。** 考虑问题

    $$
    \begin{array}{ll}
    \text{最小化} & \mathbf{E}f_0(x,u)\\
    \text{约束条件} & \mathbf{E}f_i(x,u)\leq0,\quad i=1,\ldots,m,
    \end{array}
    $$

    其中期望是对 $u$ 取的。证明：如果对每个 $u$，$f_i$ 都是关于 $x$ 的凸函数，那么这个随机优化问题是凸的。

- (b) **最坏情况优化。** 考虑问题

    $$
    \begin{array}{ll}
    \text{最小化} & \sup_{u\in\mathcal{U}}f_0(x,u)\\
    \text{约束条件} & \sup_{u\in\mathcal{U}}f_i(x,u)\leq0,\quad i=1,\ldots,m.
    \end{array}
    $$

    证明：如果对每个 $u$，$f_i$ 都是关于 $x$ 的凸函数，那么这个最坏情况优化问题是凸的。

- (c) **参数可能取值构成有限集合。** 当期望值 $\mathbf{E}f_i(x,u)$ 或最坏情况值 $\sup_{u\in\mathcal{U}}f_i(x,u)$ 有解析表达式，或有容易求值的表达式时，(a) 与 (b) 的结论最有用。

    假设参数的可能取值构成有限集合，即 $u\in\{u_1,\ldots,u_N\}$。对于随机情形，还给定了每个取值的概率：$\operatorname{prob}(u=u_i)=p_i$，其中 $p\in\mathbf{R}^N$、$p\succeq0$、$\mathbf{1}^Tp=1$。在最坏情况表述中，只需取 $\mathcal{U}\in\{u_1,\ldots,u_N\}$。

    说明如何显式建立最坏情况优化问题和随机优化问题（即给出 $\sup_{u\in\mathcal{U}}f_i$ 与 $\mathbf{E}_u f_i$ 的显式表达式）。

**4.60 对数最优投资策略。** 考虑一个在 $N$ 个期间内持有 $n$ 种资产的投资组合问题。在每期期初，我们把全部财富重新投资，按照一个固定不变的配置策略 $x\in\mathbf{R}^n$，将其重新分配到这 $n$ 种资产上，其中 $x\succeq0$、$\mathbf{1}^Tx=1$。换句话说，如果 $W(t-1)$ 是第 $t$ 期期初的财富，那么在第 $t$ 期，投入资产 $i$ 的金额为 $x_iW(t-1)$。用 $\lambda(t)$ 表示第 $t$ 期的总回报，即 $\lambda(t)=W(t)/W(t-1)$。经过 $N$ 期后，财富变为原来的 $\prod_{t=1}^N\lambda(t)$ 倍。我们把

$$
\frac{1}{N}\sum_{t=1}^N\log\lambda(t)
$$

称为这 $N$ 期内投资的**增长率**。我们希望确定一个配置策略 $x$，使 $N$ 很大时的总财富增长最大。

用一个离散随机模型来描述回报的不确定性。假设每期有 $m$ 种可能的情景，其概率为 $\pi_j$，$j=1,\ldots,m$。在情景 $j$ 下，资产 $i$ 一期的回报为 $p_{ij}$。因此，投资组合在第 $t$ 期的回报 $\lambda(t)$ 是一个随机变量，有 $m$ 个可能取值 $p_1^Tx,\ldots,p_m^Tx$，其分布为

$$
\pi_j=\operatorname{prob}(\lambda(t)=p_j^Tx),\quad j=1,\ldots,m.
$$

假设每期的可能情景相同，各期的情景取值相互独立且服从相同分布。根据大数定律，有

$$
\lim_{N\to\infty}\frac{1}{N}\log\left(\frac{W(N)}{W(0)}\right)
=\lim_{N\to\infty}\frac{1}{N}\sum_{t=1}^N\log\lambda(t)
=\mathbf{E}\log\lambda(t)
=\sum_{j=1}^m\pi_j\log(p_j^Tx).
$$

<!-- pdf-page: 224 -->

换句话说，采用投资策略 $x$ 时，长期增长率为

$$
R_{\mathrm{lt}}=\sum_{j=1}^m\pi_j\log(p_j^Tx).
$$

使这个量最大的投资策略 $x$，称为**对数最优投资策略**（log-optimal investment strategy）。它可以通过求解优化问题

$$
\begin{array}{ll}
\text{最大化} & \sum_{j=1}^m\pi_j\log(p_j^Tx)\\
\text{约束条件} & x\succeq0,\quad\mathbf{1}^Tx=1,
\end{array}
$$

得到，其中变量为 $x\in\mathbf{R}^n$。

证明这是一个凸优化问题。

**4.61 使用 logistic 模型的优化。** 随机变量 $X\in\{0,1\}$ 满足

$$
\operatorname{prob}(X=1)=p=\frac{\exp(a^Tx+b)}{1+\exp(a^Tx+b)},
$$

其中 $x\in\mathbf{R}^n$ 是影响该概率的变量向量，$a$ 和 $b$ 是已知参数。可以把 $X=1$ 理解为消费者购买某件产品这一事件，把 $x$ 理解为影响购买概率的变量向量，例如广告投入、零售价格、折扣价格、包装费用以及其他因素。需要优化的变量 $x$ 受到一组线性约束 $Fx\preceq g$ 的限制。

把下列问题表述为凸优化问题。

- (a) **最大化购买概率。** 目标是选择 $x$，使 $p$ 最大。
- (b) **最大化期望利润。** 设 $c^Tx+d$ 为售出该产品所得的利润，并假设它对所有可行的 $x$ 都为正。目标是最大化期望利润 $p(c^Tx+d)$。

**4.62 高斯广播信道中的最优功率与带宽分配。** 考虑一个由中心节点向 $n$ 个接收端发送消息的通信系统。（“高斯”指干扰传输的噪声类型。）每个接收端的信道由其（发射）功率 $P_i\geq0$ 和带宽 $W_i\geq0$ 描述。接收端信道的功率与带宽，按下式决定其比特率 $R_i$（即信息可以传送的速率）：

$$
R_i=\alpha_iW_i\log(1+\beta_iP_i/W_i),
$$

其中 $\alpha_i$ 和 $\beta_i$ 是已知的正常数。当 $W_i=0$ 时，取 $R_i=0$（这也就是令 $W_i\to0$ 时得到的极限）。

各功率必须满足总功率约束，其形式为

$$
P_1+\cdots+P_n=P_{\mathrm{tot}},
$$

其中 $P_{\mathrm{tot}}>0$ 是给定的、可分配给各信道的总功率。类似地，各带宽必须满足

$$
W_1+\cdots+W_n=W_{\mathrm{tot}},
$$

其中 $W_{\mathrm{tot}}>0$ 是给定的可用总带宽。本题中的优化变量为各功率与带宽，即 $P_1,\ldots,P_n,W_1,\ldots,W_n$。

目标是最大化总效用

$$
\sum_{i=1}^n u_i(R_i),
$$

<!-- pdf-page: 225 -->

其中 $u_i:\mathbf{R}\to\mathbf{R}$ 是第 $i$ 个接收端对应的效用函数。（可以把 $u_i(R_i)$ 理解为向接收端 $i$ 提供比特率 $R_i$ 所获得的收入，因此目标就是最大化总收入。）可以假设效用函数 $u_i$ 非递减且为凹函数。

将这个问题表述为凸优化问题。

**4.63 制造成本与成品率的最优权衡。** 向量 $x\in\mathbf{R}^n$ 表示制造过程中的标称参数。过程的成品率，即制成品中合格产品所占的比例，为 $Y(x)$。假设 $Y$ 是对数凹函数（实际中经常如此；见例 3.43）。生产单位产品的成本为 $c^Tx$，其中 $c\in\mathbf{R}^n$。每件合格产品的成本为 $c^Tx/Y(x)$。我们希望在 $x$ 满足某些凸约束（例如线性不等式 $Ax\preceq b$）的条件下，最小化 $c^Tx/Y(x)$。（可以假设在可行集上有 $c^Tx>0$ 且 $Y(x)>0$。）

这个问题既不是凸优化问题，也不是拟凸优化问题，但可以结合凸优化和一维搜索来求解。下面给出基本思路，你需要补全所有细节和论证。

- (a) 证明函数 $f:\mathbf{R}\to\mathbf{R}$

    $$
    f(a)=\sup\{Y(x)\mid Ax\preceq b,\ c^Tx=a\},
    $$

    是对数凹函数；它给出成本为 $a$ 时能够达到的最大成品率。这意味着，通过求解一个以 $x$ 为变量的凸优化问题，就可以计算函数 $f$ 的值。

- (b) 假设在足够多个 $a$ 值处计算了 $f$，从而在所关心的范围内得到了较好的近似。说明如何用这些数据，近似求解使每件合格产品的成本最小的问题。

**4.64 带补救决策的优化。** 在带补救决策的优化问题（optimization with recourse）中，也称为**两阶段优化**（two-stage optimization），代价函数和约束不仅取决于所选择的变量，还取决于一个离散随机变量 $s\in\{1,\ldots,S\}$；它表示 $S$ 种情景中发生了哪一种。情景随机变量 $s$ 的概率分布 $\pi$ 已知，其中 $\pi_i=\operatorname{prob}(s=i)$，$i=1,\ldots,S$。

在两阶段优化中，需要选择两个变量 $x\in\mathbf{R}^n$ 和 $z\in\mathbf{R}^q$ 的值。变量 $x$ 必须在得知具体情景 $s$ 之前选定；变量 $z$ 则在得知情景随机变量的值之后选择。换句话说，$z$ 是情景随机变量 $s$ 的函数。为了描述对 $z$ 的选择，我们列出在各个情景下会选择的值，即列出向量

$$
z_1,\ldots,z_S\in\mathbf{R}^q.
$$

这里，$z_3$ 是 $s=3$ 发生时所选择的 $z$，其余类似。这组值

$$
x\in\mathbf{R}^n,\quad z_1,\ldots,z_S\in\mathbf{R}^q
$$

称为**策略**（policy），因为它规定了如何选择 $x$（与发生哪一种情景无关），以及在每种可能情景下如何选择 $z$。

变量 $z$ 称为**补救变量**（recourse variable，或**第二阶段变量**），因为它允许我们在知道哪种情景已经发生后，再采取行动或作出选择。相对而言，对 $x$（称为**第一阶段变量**）的选择，必须在对具体情景一无所知时作出。

为简便起见，只考虑没有约束的情形。代价函数为

$$
f:\mathbf{R}^n\times\mathbf{R}^q\times\{1,\ldots,S\}\to\mathbf{R},
$$

其中 $f(x,z,i)$ 给出第一阶段选择为 $x$、第二阶段选择为 $z$，且情景 $i$ 发生时的代价。我们把期望代价

$$
\mathbf{E}f(x,z_s,s)=\sum_{i=1}^S\pi_i f(x,z_i,i)
$$

作为总目标，在所有策略中使其最小。

<!-- pdf-page: 226 -->

假设对每个情景 $i=1,\ldots,S$，$f$ 都是关于 $(x,z)$ 的凸函数。说明如何用凸优化找到一个最优策略，即在所有可能策略中使期望代价最小的策略。

**4.65 混合动力汽车的最优运行。** 混合动力汽车具有内燃机、与蓄电池连接的电动机／发电机，以及常规的摩擦制动器。本题考虑一个并联式混合动力汽车的高度简化模型，其中电动机／发电机和发动机都直接与驱动车轮连接。发动机可以向车轮提供功率，制动器则可以从车轮吸收功率，并将其转化为热。电动机／发电机既可以作为电动机，利用蓄电池中储存的能量向车轮输出功率，也可以作为发电机，从车轮或发动机获取功率，用来给蓄电池充电。当发电机从车轮获取功率并给蓄电池充电时，称为**再生制动**（regenerative braking）；与普通的摩擦制动不同，从车轮获取的能量被储存起来，可以在以后使用。通过让车辆驶过一条已知、固定的测试路线，评估其燃油效率。

下图展示混合动力汽车中的功率流向。箭头表示功率流被规定为正的方向。例如，发动机输出功率时，发动机功率 $p_{\mathrm{eng}}$ 为正；制动器从车轮吸收功率时，制动功率 $p_{\mathrm{br}}$ 为正。$p_{\mathrm{req}}$ 是车轮所需的功率。当车轮需要输入功率时（例如车辆加速、爬坡或在水平路面匀速行驶时），它为正。当车辆必须快速减速或下坡时，车轮所需的功率为负。

<figure id="exercise-4-65" data-uncaptioned="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/exercise-4-65.png" alt="混合动力汽车的功率流向图，包含发动机、制动器、电动机／发电机、蓄电池和车轮，以及各功率的正方向箭头" data-source-page="226" data-source-rect="229,358,462,459">
<p class="figure-translation">图内文字：Engine：发动机；Brake：制动器；wheels：车轮；Motor/generator：电动机／发电机；Battery：蓄电池。</p>
</figure>

所有这些功率都是时间的函数。我们将时间离散为一秒一个间隔，记作 $t=1,2,\ldots,T$。车轮所需的功率 $p_{\mathrm{req}}(1),\ldots,p_{\mathrm{req}}(T)$ 是给定的。（车辆在测试路线上的速度已指定，因此结合已知的道路坡度信息，以及已知的空气动力学损耗和其他损耗，可以计算出车轮所需的功率。）

功率守恒意味着

$$
p_{\mathrm{req}}(t)=p_{\mathrm{eng}}(t)+p_{\mathrm{mg}}(t)-p_{\mathrm{br}}(t),\quad t=1,\ldots,T.
$$

制动器只能耗散功率，因此每个 $t$ 都有 $p_{\mathrm{br}}(t)\geq0$。发动机只能提供功率，而且不能超过给定上限 $P_{\mathrm{eng}}^{\max}$，即

$$
0\leq p_{\mathrm{eng}}(t)\leq P_{\mathrm{eng}}^{\max},\quad t=1,\ldots,T.
$$

电动机／发电机的功率也有限制：$p_{\mathrm{mg}}$ 必须满足

$$
P_{\mathrm{mg}}^{\min}\leq p_{\mathrm{mg}}(t)\leq P_{\mathrm{mg}}^{\max},\quad t=1,\ldots,T.
$$

这里，$P_{\mathrm{mg}}^{\max}>0$ 是最大电动机功率，而 $-P_{\mathrm{mg}}^{\min}>0$ 是最大发电机功率。

时刻 $t$ 的蓄电池电量或能量记作 $E(t)$，$t=1,\ldots,T+1$。蓄电池能量满足

$$
E(t+1)=E(t)-p_{\mathrm{mg}}(t)-\eta|p_{\mathrm{mg}}(t)|,\quad t=1,\ldots,T,
$$

<!-- pdf-page: 227 -->

其中 $\eta>0$ 是已知参数。（$-p_{\mathrm{mg}}(t)$ 一项表示在忽略损耗时，电动机／发电机从蓄电池取出的能量，或向其中加入的能量。$-\eta|p_{\mathrm{mg}}(t)|$ 一项表示蓄电池或电动机／发电机效率不足所造成的能量损耗。）

蓄电池电量在所有时刻都必须介于 $0$（空电）与上限 $E_{\mathrm{batt}}^{\max}$（满电）之间。（当 $E(t)=0$ 时，蓄电池已完全放电，不能再从中取出能量；当 $E(t)=E_{\mathrm{batt}}^{\max}$ 时，蓄电池已满，不能再充电。）为了与非混合动力汽车公平比较，规定蓄电池的初始电量等于最终电量，使车辆驶过整条测试路线后的净能量变化为零：$E(1)=E(T+1)$。初始（也就是最终）能量的具体值不作指定。

本题要最小化的目标是发动机消耗的总燃油量，即

$$
F_{\mathrm{total}}=\sum_{t=1}^T F(p_{\mathrm{eng}}(t)),
$$

其中 $F:\mathbf{R}\to\mathbf{R}$ 是发动机的**燃油消耗特性**。假设 $F$ 为正、递增且为凸函数。

将此问题表述为凸优化问题，变量为 $p_{\mathrm{eng}}(t)$、$p_{\mathrm{mg}}(t)$ 和 $p_{\mathrm{br}}(t)$（$t=1,\ldots,T$），以及 $E(t)$（$t=1,\ldots,T+1$）。解释为什么你的表述与上述问题等价。

<!-- pdf-page: 228 -->
