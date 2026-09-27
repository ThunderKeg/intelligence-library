<!-- pdf-page: 28 -->
# 附录 1—4

<aside class="chapter-guide"><strong>本篇导读</strong><p>这四个附录依次推导有限状态约束下符号块的增长率、熵公式、遍历信源的几个定理，以及约束系统能达到的最大信息产生速率。</p></aside>

## 附录 1：有限状态条件下符号块数量的增长

设 $N_i(L)$ 是长度为 $L$、结束于状态 $i$ 的符号块数。于是

$$
N_j(L)=\sum_{i,s}N_i\!\left(L-b_{ij}^{(s)}\right),
$$

其中 $b_{ij}^{1},b_{ij}^{2},\ldots,b_{ij}^{m}$ 是在状态 $i$ 可以选取、并使系统转到状态 $j$ 的符号长度。这些是线性差分方程，因此当 $L\to\infty$ 时，其增长形式必定为

$$
N_j=A_jW^L.
$$

将其代入差分方程，得到

$$
A_jW^L=\sum_{i,s}A_iW^{L-b_{ij}^{(s)}}
$$

或

$$
\begin{aligned}
A_j&=\sum_{i,s}A_iW^{-b_{ij}^{(s)}},\\
\sum_i\left(\sum_sW^{-b_{ij}^{(s)}}-\delta_{ij}\right)A_i&=0.
\end{aligned}
$$

若要存在这样的解，行列式

$$
D(W)=|a_{ij}|=\left|\sum_sW^{-b_{ij}^{(s)}}-\delta_{ij}\right|
$$

必须为零。这就确定了 $W$；它当然是 $D=0$ 的最大实根。

量 $C$ 因而等于

$$
C=\lim_{L\to\infty}\frac{\log\sum A_jW^L}{L}=\log W.
$$

还可注意到：即使要求所有符号块都从同一个（任意选定的）状态出发，也会得到同样的增长性质。

## 附录 2：$H=-\sum p_i\log p_i$ 的推导

令 $H(\tfrac1n,\tfrac1n,\ldots,\tfrac1n)=A(n)$。根据条件 (3)，可以把从 $s^m$ 个等概率可能性中作一次选择，分解成连续作 $m$ 次、每次从 $s$ 个等概率可能性中选择，由此得到

$$
A(s^m)=mA(s).
$$

<!-- pdf-page: 29 -->
同样有

$$
A(t^n)=nA(t).
$$

可以任意增大 $n$，并找到一个 $m$，使

$$
s^m\le t^n<s^{m+1}.
$$

因此，取对数后除以 $n\log s$，得到

$$
\frac mn\le\frac{\log t}{\log s}<\frac mn+\frac1n,
\quad\text{或}\quad
\left|\frac mn-\frac{\log t}{\log s}\right|<\epsilon,
$$

其中 $\epsilon$ 可以任意小。由 $A(n)$ 的单调性又有

$$
\begin{aligned}
A(s^m)&\le A(t^n)\le A(s^{m+1}),\\
mA(s)&\le nA(t)\le(m+1)A(s).
\end{aligned}
$$

所以除以 $nA(s)$，得到

$$
\frac mn\le\frac{A(t)}{A(s)}\le\frac mn+\frac1n,
\quad\text{或}\quad
\left|\frac mn-\frac{A(t)}{A(s)}\right|<\epsilon.
$$

于是

$$
\left|\frac{A(t)}{A(s)}-\frac{\log t}{\log s}\right|<2\epsilon,
\qquad A(t)=K\log t,
$$

其中，为满足条件 (2)，$K$ 必须为正。

现在设从 $n$ 种可能性中选择，各项概率可通约（commeasurable），即 $p_i=n_i/\sum n_i$，其中 $n_i$ 为整数。可以把从 $\sum n_i$ 种可能性中选择分成两步：先按概率 $p_1,\ldots,p_n$ 从 $n$ 种可能性中选择；若选中第 $i$ 种，再从 $n_i$ 个等概率可能性中选择。再次利用条件 (3)，令两种方法算出的总选择量相等，得到

$$
K\log\sum n_i=H(p_1,\ldots,p_n)+K\sum p_i\log n_i.
$$

因此

$$
\begin{aligned}
H&=K\left[\sum p_i\log\sum n_i-\sum p_i\log n_i\right]\\
 &=-K\sum p_i\log\frac{n_i}{\sum n_i}
 =-K\sum p_i\log p_i.
\end{aligned}
$$

若 $p_i$ 不可通约，可以用有理数逼近；根据连续性假设，仍须得到同一表达式。因此该表达式一般成立。系数 $K$ 的选择只是为了方便，相当于选择计量单位。

## 附录 3：关于遍历信源的定理

如果从任一概率 $P>0$ 的状态，都能沿概率 $p>0$ 的路径到达其他任一状态，那么系统是遍历的，可以应用大数强定律。因此，在长度为 $N$ 的长序列中，网络中的某条给定路径 $p_{ij}$ 被经过的次数，约等于处于状态 $i$ 的概率（设为 $P_i$）乘以在该状态选取这条路径的概率，再乘以 $N$，即 $P_ip_{ij}N$。如果 $N$ 足够大，路径出现次数占 $N$ 的比例与 $P_ip_{ij}$ 之差超过 $\delta$ 的概率小于 $\epsilon$；因此，除一个总概率很小的集合外，实际次数落在

$$
(P_ip_{ij}\pm\delta)N
$$

所给的界限内。于是，几乎所有序列的概率 $p$ 可写作

$$
p=\prod p_{ij}^{(P_ip_{ij}\pm\delta)N}.
$$

<!-- pdf-page: 30 -->
而 $\log p/N$ 满足

$$
\frac{\log p}{N}=\sum(P_ip_{ij}\pm\delta)\log p_{ij},
\quad\text{或}\quad
\left|\frac{\log p}{N}-\sum P_ip_{ij}\log p_{ij}\right|<\eta.
$$

这就证明了定理 3。

根据定理 3 中 $p$ 可能取值的范围，计算 $n(q)$ 的上界和下界，即可直接得到定理 4。

在混合的（非遍历）情形中，若

$$
L=\sum p_iL_i,
$$

而各分量的熵满足 $H_1\ge H_2\ge\cdots\ge H_n$，则有如下定理：

*定理：* 极限

$$
\lim_{N\to\infty}\frac{\log n(q)}{N}=\varphi(q)
$$

是一个递减的阶梯函数；当

$$
\sum_{i=1}^{s-1}\alpha_i<q<\sum_{i=1}^{s}\alpha_i
$$

时，$\varphi(q)=H_s$。

<aside class="translator-note"><strong>译注</strong><p>原文前面用 $p_i$ 表示混合权重，此处改用 $\alpha_i$，没有说明两者的关系；译文保留原记号。</p></aside>

为证明定理 5 和定理 6，先注意 $F_N$ 单调递减，因为增大 $N$ 相当于给条件熵再增加一个下标。将 $p_{B_i}(S_j)$ 简单代入 $F_N$ 的定义可得

$$
F_N=NG_N-(N-1)G_{N-1}.
$$

再对所有 $N$ 求和，得到 $G_N=\tfrac1N\sum F_n$。因此 $G_N\ge F_N$，且 $G_N$ 单调递减。二者还必须趋于同一个极限。由定理 3 可知 $\lim_{N\to\infty}G_N=H$。

## 附录 4：约束系统的信息速率最大化

假设有一组针对符号序列的有限状态约束，因此可以用线性图表示。令 $\ell_{ij}^{(s)}$ 为从状态 $i$ 转到状态 $j$ 时可能出现的各个符号的长度。在这些约束下，应怎样分配各状态的概率 $P_i$，以及在状态 $i$ 选择符号 $s$ 并转到状态 $j$ 的概率 $p_{ij}^{(s)}$，才能使信息产生速率最大？这组约束定义了一个离散信道，而最大速率必不超过该信道的容量 $C$：如果所有足够长的符号块都等概率，那么得到的速率就是 $C$；如果做得到，这便是最优情形。下面证明，适当地选择 $P_i$ 和 $p_{ij}^{(s)}$，就能达到这个速率。

所讨论的速率是

$$
\frac{-\sum P_i p_{ij}^{(s)}\log p_{ij}^{(s)}}
{\sum P_i p_{ij}^{(s)}\ell_{ij}^{(s)}}=\frac NM.
$$

<aside class="translator-note"><strong>译注</strong><p>原文下文交替使用带上标 $(s)$ 与不带上标的 $p_{ij}$、$\ell_{ij}$，未交代两组记号如何转换；公式照原文排印。</p></aside>

令 $\ell_{ij}=\sum_s\ell_{ij}^{(s)}$。显然，在最大值处，$p_{ij}^{(s)}=k\exp\ell_{ij}^{(s)}$。最大化时的约束为 $\sum P_i=1$、$\sum_jp_{ij}=1$ 和 $\sum P_i(p_{ij}-\delta_{ij})=0$。因此要最大化

$$
U=\frac{-\sum P_i p_{ij}\log p_{ij}}{\sum P_i p_{ij}\ell_{ij}}
+\lambda\sum_iP_i+\sum\mu_i p_{ij}
+\sum\eta_jP_i(p_{ij}-\delta_{ij}),
$$

并有

$$
\frac{\partial U}{\partial p_{ij}}
=\frac{-MP_i(1+\log p_{ij})+NP_i\ell_{ij}}{M^2}
+\lambda+\mu_i+\eta_iP_i=0.
$$

<!-- pdf-page: 31 -->
解出 $p_{ij}$，得到

$$
p_{ij}=A_iB_jD^{-\ell_{ij}}.
$$

由于

$$
\sum_jp_{ij}=1,
\qquad A_i^{-1}=\sum_jB_jD^{-\ell_{ij}},
$$

所以

$$
p_{ij}=\frac{B_jD^{-\ell_{ij}}}{\sum_sB_sD^{-\ell_{is}}}.
$$

$D$ 的正确取值是容量 $C$，而 $B_j$ 是下式的解：

$$
B_i=\sum_jB_jC^{-\ell_{ij}}.
$$

<aside class="translator-note"><strong>译注</strong><p>此处把 $D$ 写成容量 $C$；本书第 1 节及附录 1 则写 $C=\log W$、特征根为 $W$。原文没有解释这两种写法的关系。</p></aside>

因为这时

$$
\begin{aligned}
p_{ij}&=\frac{B_j}{B_i}C^{-\ell_{ij}},\\
\sum_iP_i\frac{B_j}{B_i}C^{-\ell_{ij}}&=P_j,
\end{aligned}
$$

或者

$$
\sum_i\frac{P_i}{B_i}C^{-\ell_{ij}}=\frac{P_j}{B_j}.
$$

因此，如果 $\lambda_i$ 满足

$$
\sum_i\gamma_iC^{-\ell_{ij}}=\gamma_j,
\qquad P_i=B_i\gamma_i,
$$

<aside class="translator-note"><strong>译注</strong><p>原文上一句使用 $\lambda_i$，随后的公式改用 $\gamma_i$，没有说明两者的关系。</p></aside>

那么 $B_i$ 和 $\gamma_i$ 这两组方程都能成立，因为 $C$ 满足

$$
\left|C^{-\ell_{ij}}-\delta_{ij}\right|=0.
$$

此时信息速率为

$$
\frac{-\sum P_i p_{ij}\log\!\left(\frac{B_j}{B_i}C^{-\ell_{ij}}\right)}
{\sum P_i p_{ij}\ell_{ij}}
=C-\frac{\sum P_i p_{ij}\log\frac{B_j}{B_i}}
{\sum P_i p_{ij}\ell_{ij}},
$$

而

$$
\sum P_i p_{ij}(\log B_j-\log B_i)
=\sum_jP_j\log B_j-\sum_iP_i\log B_i=0.
$$

所以信息速率等于 $C$。由于它不可能超过 $C$，这就是最大值，也证实了前面假设的解。
