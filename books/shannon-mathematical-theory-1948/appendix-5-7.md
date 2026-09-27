<!-- pdf-page: 52 -->
# 附录 5—7

<aside class="chapter-guide"><strong>本组导读</strong><p>附录 5 证明时间平移下不变的运算保留系综的平稳性和遍历性；附录 6 推导两个系综相加时熵功率的界；附录 7 用概率测度与划分，给出更一般的传输速率和维数率定义。</p></aside>

## 致谢

作者感谢他在实验室的同事，尤其感谢 H. W. Bode 博士、J. R. Pierce 博士、B. McMillan 博士和 B. M. Oliver 博士；他们在这项工作期间提出了许多有益的建议和批评。还应感谢 N. Wiener 教授：他对平稳系综的滤波和预测问题给出的精妙解法，深刻影响了作者在这一领域的思考。

## 附录 5

设 $S_1$ 是 $g$ 系综中的任意可测子集，$S_2$ 是 $f$ 系综中经运算 $T$ 后产生 $S_1$ 的那个子集。那么

$$S_1=TS_2.$$

设 $H^\lambda$ 是把一个集合中的所有函数沿时间轴平移 $\lambda$ 的算子。于是

$$H^\lambda S_1=H^\lambda TS_2=TH^\lambda S_2,$$

因为 $T$ 不变，所以它与 $H^\lambda$ 可交换。若 $m[S]$ 是集合 $S$ 的概率测度，则

$$\begin{aligned}
m[H^\lambda S_1]&=m[TH^\lambda S_2]=m[H^\lambda S_2]\\
&=m[S_2]=m[S_1].
\end{aligned}$$

第二个等号来自 $g$ 空间中测度的定义；第三个等号来自 $f$ 系综的平稳性；最后一个等号再次来自 $g$ 空间中测度的定义。

为证明不变运算也保留遍历性，设 $S_1$ 是 $g$ 系综中在 $H^\lambda$ 下保持不变的子集，$S_2$ 是所有变换后落入 $S_1$ 的函数 $f$ 的集合。则

$$H^\lambda S_1=H^\lambda TS_2=TH^\lambda S_2=S_1,$$

因此对所有 $\lambda$，$H^\lambda S_2$ 都包含于 $S_2$。现在，由于

$$m[H^\lambda S_2]=m[S_1],$$

这就意味着，只要 $m[S_2]\ne0,1$，对所有 $\lambda$ 都有

$$H^\lambda S_2=S_2.$$

这一矛盾说明这样的 $S_1$ 不存在。

## 附录 6

上界 $\bar N_3\leq N_1+N_2$ 来自这样一个事实：功率为 $N_1+N_2$ 时，最大可能的熵出现在同等功率的白噪声情形。此时熵功率为 $N_1+N_2$。

为得到下界，设 $n$ 维空间中有两个分布 $p(x_i)$ 和 $q(x_i)$，熵功率分别为 $\bar N_1$ 和 $\bar N_2$。要使它们的卷积 $r(x_i)$ 的熵功率 $\bar N_3$ 最小，$p$ 和 $q$ 应具有什么形式？

$$r(x_i)=\int p(y_i)q(x_i-y_i)\,dy_i.$$

$r$ 的熵 $H_3$ 为

$$H_3=-\int r(x_i)\log r(x_i)\,dx_i.$$

我们希望在下列约束下使它最小：

$$H_1=-\int p(x_i)\log p(x_i)\,dx_i,$$

$$H_2=-\int q(x_i)\log q(x_i)\,dx_i.$$

<!-- pdf-page: 53 -->
因此考虑

$$U=-\int\left[r(x)\log r(x)+\lambda p(x)\log p(x)+\mu q(x)\log q(x)\right]dx,$$

$$\delta U=-\int\left\{[1+\log r(x)]\delta r(x)+\lambda[1+\log p(x)]\delta p(x)+\mu[1+\log q(x)]\delta q(x)\right\}dx.$$

如果在特定自变量 $x_i=s_i$ 处改变 $p(x)$，则 $r(x)$ 的变分为

$$\delta r(x)=q(x_i-s_i),$$

并且

$$\delta U=-\int q(x_i-s_i)\log r(x_i)\,dx_i-\lambda\log p(s_i)=0.$$

对 $q$ 作变分时也一样。因此，极小值的条件是

$$\int q(x_i-s_i)\log r(x_i)\,dx_i=-\lambda\log p(s_i),$$

$$\int p(x_i-s_i)\log r(x_i)\,dx_i=-\mu\log q(s_i).$$

第一式乘以 $p(s_i)$，第二式乘以 $q(s_i)$，再对 $s_i$ 积分，得到

$$H_3=-\lambda H_1,\qquad H_3=-\mu H_2.$$

解出 $\lambda$ 和 $\mu$ 并代回原式，得到

$$H_1\int q(x_i-s_i)\log r(x_i)\,dx_i=-H_3\log p(s_i),$$

$$H_2\int p(x_i-s_i)\log r(x_i)\,dx_i=-H_3\log q(s_i).$$

现在设 $p(x_i)$ 和 $q(x_i)$ 都是正态分布：

$$p(x_i)=\frac{|A_{ij}|^{n/2}}{(2\pi)^{n/2}}\exp\!\left(-\frac12\sum_{i,j}A_{ij}x_i x_j\right),$$

$$q(x_i)=\frac{|B_{ij}|^{n/2}}{(2\pi)^{n/2}}\exp\!\left(-\frac12\sum_{i,j}B_{ij}x_i x_j\right).$$

那么 $r(x_i)$ 也服从正态分布，其二次型为 $C_{ij}$。若这些二次型的逆分别为 $a_{ij}$、$b_{ij}$、$c_{ij}$，则

$$c_{ij}=a_{ij}+b_{ij}.$$

我们要说明，这些函数满足上述极小值条件，当且仅当 $a_{ij}=Kb_{ij}$；于是它们在约束下给出最小的 $H_3$。首先有

$$\log r(x_i)=\frac n2\log\frac1{2\pi}|C_{ij}|-\frac12\sum_{i,j}C_{ij}x_i x_j,$$

$$\int q(x_i-s_i)\log r(x_i)\,dx_i=\frac n2\log\frac1{2\pi}|C_{ij}|-\frac12\sum_{i,j}C_{ij}s_i s_j-\frac12\sum_{i,j}C_{ij}b_{ij}.$$

这应当等于

$$\frac{H_3}{H_1}\left[\frac n2\log\frac1{2\pi}|A_{ij}|-\frac12\sum_{i,j}A_{ij}s_i s_j\right],$$

因而要求 $A_{ij}=\frac{H_1}{H_3}C_{ij}$。此时 $A_{ij}=\frac{H_1}{H_2}B_{ij}$，两个方程便都化为恒等式。

<!-- pdf-page: 54 -->
## 附录 7

下面说明如何以更一般、更严格的方式处理通信理论的核心定义。考虑一个概率测度空间，其元素是有序对 $(x,y)$。把变量 $x,y$ 分别看作某个长时段 $T$ 内可能的发射信号和接收信号。所有满足 $x$ 属于 $x$ 空间子集 $S_1$ 的点所构成的集合，称为 $S_1$ 上的“条带”；同理定义 $y$ 空间子集 $S_2$ 上的条带。把 $x$ 和 $y$ 分别划分为一组互不重叠的可测子集 $X_i$ 和 $Y_i$，则传输速率 $R$ 可近似为

$$R_1=\frac1T\sum_i P(X_i,Y_i)\log\frac{P(X_i,Y_i)}{P(X_i)P(Y_i)},$$

其中：

$$\begin{aligned}
P(X_i)&\quad\text{是 }X_i\text{ 上条带的概率测度},\\
P(Y_i)&\quad\text{是 }Y_i\text{ 上条带的概率测度},\\
P(X_i,Y_i)&\quad\text{是两个条带交集的概率测度}.
\end{aligned}$$

进一步细分绝不会使 $R_1$ 减小。设 $X_1$ 被分为 $X_1=X'_1+X''_1$，并令

$$\begin{alignedat}{2}
P(Y_1)&=a,\qquad &P(X_1)&=b+c,\\
P(X'_1)&=b, &P(X'_1,Y_1)&=d,\\
P(X''_1)&=c, &P(X''_1,Y_1)&=e,\\
&&P(X_1,Y_1)&=d+e.
\end{alignedat}$$

那么，对于 $X_1$ 与 $Y_1$ 的交集，求和式中的

$$ (d+e)\log\frac{d+e}{a(b+c)} $$

被替换为

$$d\log\frac d{ab}+e\log\frac e{ac}.$$

在 $b,c,d,e$ 所受的限制下，很容易证明

$$\left(\frac{d+e}{b+c}\right)^{d+e}\leq\frac{d^d e^e}{b^d c^e},$$

因此求和式增大。各种可能的细分构成一个有向集，而 $R$ 随划分的加细单调增加。我们可把 $R$ 明确定义为 $R_1$ 的最小上界，并写成

$$R=\frac1T\iint P(x,y)\log\frac{P(x,y)}{P(x)P(y)}\,dx\,dy.$$

按上述意义理解，这个积分既包括连续情形，也包括离散情形，当然还包括许多无法用这两种形式表示的其他情形。在这种表述中，如果 $x$ 与 $u$ 一一对应，那么从 $u$ 到 $y$ 的速率等于从 $x$ 到 $y$ 的速率，这是显然的。如果 $v$ 是 $y$ 的任何函数（不要求有逆函数），那么从 $x$ 到 $y$ 的速率大于或等于从 $x$ 到 $v$ 的速率，因为在计算近似值时，对 $y$ 的划分实际上比对 $v$ 的划分更细。更一般地，如果 $y$ 与 $v$ 之间的关系不是函数关系而是统计关系，即存在概率测度空间 $(y,v)$，则 $R(x,v)\leq R(x,y)$。这意味着，对接收信号施加任何运算，即使其中包含随机因素，也不会增加 $R$。

在理论的抽象表述中，还应精确定义另一个概念，即“维数率”（dimension rate）：为了表示系综中的一个成员，平均每秒需要多少个维度。在带限情形下，每秒用 $2W$ 个数就足够了。更一般的定义可以如下给出。设 $f_\alpha(t)$ 是一个函数系综，$\rho_T[f_\alpha(t),f_\beta(t)]$ 是一个度量，用来测量在时段 $T$ 内从 $f_\alpha$ 到 $f_\beta$ 的“距离”（例如这个区间内的均方根差异）。设 $N(\epsilon,\delta,T)$ 为可以选出的最少的函数 $f$ 的数量，使得除去一个测度为 $\delta$ 的集合外，系综中的每个函数都在所选函数至少一个的距离 $\epsilon$ 之内。因此，我们在忽略测度很小的集合 $\delta$ 的条件下，以精度 $\epsilon$ 覆盖了这个空间。系综的维数率 $\lambda$ 定义为三重极限

<!-- pdf-page: 55 -->
$$\lambda=\lim_{\delta\to0}\lim_{\epsilon\to0}\lim_{T\to\infty}\frac{\log N(\epsilon,\delta,T)}{T\log\epsilon}.$$

这是拓扑学中测度式维数定义的一种推广；对于结果一目了然的简单系综，它与直观的维数率一致。
