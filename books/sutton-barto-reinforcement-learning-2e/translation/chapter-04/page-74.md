以上方程对所有 \(s\in\mathcal S\)、\(a\in\mathcal A(s)\) 和 \(s'\in\mathcal S^+\) 成立。我们将看到，DP 算法是把这样的贝尔曼方程变成赋值语句，也就是不断改进所需价值函数近似值的更新规则。

## 4.1 策略评估（预测）

先考虑怎样计算任意策略 \(\pi\) 的状态价值函数 \(v_\pi\)。DP 文献把这称为**策略评估**（policy evaluation）；我们也称其为**预测问题**。回顾第 3 章，对所有 \(s\in\mathcal S\)，有

\[
\begin{aligned}
v_\pi(s)&\doteq\mathbb E_\pi[G_t\mid S_t=s]\\
&=\mathbb E_\pi[R_{t+1}+\gamma G_{t+1}\mid S_t=s]\qquad\text{（由式 3.9）}\\
&=\mathbb E_\pi[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s].
\end{aligned}\tag{4.3}
\]

\[
v_\pi(s)=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_\pi(s')\bigr].\tag{4.4}
\]

其中，\(\pi(a\mid s)\) 是依照策略 \(\pi\) 在状态 \(s\) 选择动作 \(a\) 的概率；期望算子下标的 \(\pi\) 表示：这些期望以遵循策略 \(\pi\) 为条件。只要 \(\gamma<1\)，或者按照 \(\pi\) 从所有状态出发最终都保证终止，\(v_\pi\) 的存在性和唯一性就有保证。

如果完全知道环境的动力学，那么式（4.4）就是关于 \(|\mathcal S|\) 个未知数 \(v_\pi(s)\)（\(s\in\mathcal S\)）的 \(|\mathcal S|\) 个联立线性方程。原则上，求解它虽繁琐却很直接。不过，对我们的目的而言，迭代求解更合适。考虑一列近似价值函数 \(v_0,v_1,v_2,\ldots\)，每个函数都把 \(\mathcal S^+\) 映射到实数集 \(\mathbb R\)。初始近似 \(v_0\) 可以任意选择，但终止状态（若有）的价值必须是 0。此后，把 \(v_\pi\) 的贝尔曼方程（4.4）当作更新规则，得到下一次近似：

\[
\begin{aligned}
v_{k+1}(s)&\doteq\mathbb E_\pi[R_{t+1}+\gamma v_k(S_{t+1})\mid S_t=s]\\
&=\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_k(s')\bigr].
\end{aligned}\tag{4.5}
\]

这对所有 \(s\in\mathcal S\) 成立。显然，\(v_k=v_\pi\) 是该更新规则的不动点，因为此时 \(v_\pi\) 的贝尔曼方程保证等号成立。事实上，在保证 \(v_\pi\) 存在的同样条件下，可以证明当 \(k\to\infty\) 时，序列 \(\{v_k\}\) 一般会收敛到 \(v_\pi\)。这个算法叫作**迭代式策略评估**（iterative policy evaluation）。

为了从 \(v_k\) 得到下一次近似 \(v_{k+1}\)，迭代式策略评估会对每个状态 \(s\) 应用同一种操作：根据策略下从 \(s\) 出发的所有可能一步转移、后继状态的旧价值，以及这些转移的期望即时奖励，算出一个新价值，替换 \(s\) 的旧价值。我们把这种操作称为**期望更新**（expected update）。每轮迭代都把所有状态的价值各更新一次，得到新的近似价值函数。
