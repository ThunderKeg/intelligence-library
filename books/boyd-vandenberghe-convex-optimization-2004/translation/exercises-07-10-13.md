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
