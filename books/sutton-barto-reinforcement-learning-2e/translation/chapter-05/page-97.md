**习题 5.3** 蒙特卡洛估计 \(q_\pi\) 的备份图是什么样的？ □

## 5.3 蒙特卡洛控制

现在我们可以考虑怎样用蒙特卡洛估计进行控制，即近似求得最优策略。总体思路沿用 DP 一章的模式，也就是广义策略迭代（generalized policy iteration，GPI）。GPI 同时维护一个近似策略和一个近似价值函数。价值函数不断调整，以便更接近当前策略的价值函数；策略则不断依据当前价值函数得到改进，如右图所示。这两类调整在一定程度上相互牵制，因为一类调整会让另一类调整追逐的目标发生变化；但它们共同推动策略和价值函数接近最优。

![广义策略迭代示意图](assets/fig-5-gpi.png)

图内文字译注：evaluation 为“评估”，表示 Q 向 \(q_\pi\) 靠近；improvement 为“改进”，表示 π 向相对于 Q 的贪心策略靠近。

先考虑经典策略迭代的蒙特卡洛版本。这个方法交替执行完整的策略评估和策略改进：从任意策略 π₀ 开始，以最优策略和最优动作价值函数结束：

\[
\pi_0\xrightarrow{\mathrm E}q_{\pi_0}\xrightarrow{\mathrm I}\pi_1
\xrightarrow{\mathrm E}q_{\pi_1}\xrightarrow{\mathrm I}\pi_2
\xrightarrow{\mathrm E}\cdots\xrightarrow{\mathrm I}\pi_*
\xrightarrow{\mathrm E}q_*.
\]

这里的 E 箭头表示一次完整的策略评估，I 箭头表示一次完整的策略改进。策略评估完全按照上一节介绍的方法进行。经历许多个回合后，近似动作价值函数渐近地趋向真实函数。暂且假设我们确实观察到无穷多个回合，而且这些回合由探索性起点生成。在这些假设下，对任意 \(\pi_k\)，蒙特卡洛方法都能精确求出 \(q_{\pi_k}\)。

策略改进通过使策略相对于当前价值函数变为贪心策略来完成。这里我们已有动作价值函数，因此构造贪心策略不需要模型。对于任意动作价值函数 q，相应的贪心策略在每个 s ∈ S 都确定性地选择动作价值最大的一个行动：

\[
\pi(s)\doteq\operatorname*{arg\,max}_{a}q(s,a).\tag{5.1}
\]

接下来，令每个 \(\pi_{k+1}\) 成为相对于 \(q_{\pi_k}\) 的贪心策略，就完成了策略改进。此时，策略改进定理（第 4.2 节）适用于 \(\pi_k\) 和 \(\pi_{k+1}\)，因为对所有 s ∈ S，都有

\[
\begin{aligned}
q_{\pi_k}\bigl(s,\pi_{k+1}(s)\bigr)
&=q_{\pi_k}\bigl(s,\operatorname*{arg\,max}_{a}q_{\pi_k}(s,a)\bigr)\\
&=\max_a q_{\pi_k}(s,a)\\
&\ge q_{\pi_k}\bigl(s,\pi_k(s)\bigr)\\
&=v_{\pi_k}(s).
\end{aligned}
\]
