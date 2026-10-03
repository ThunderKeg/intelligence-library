可以把三步树备份更新看成六个半步：从行动到后继状态的采样半步，与从该状态考虑策略下所有可能行动及其发生概率的期望半步，交替出现。

下面推导 n 步树备份算法的详细公式。一步回报（目标）与期望 Sarsa 相同：

公式（7.15）：\(G_{t:t+1}\doteq R_{t+1}+\gamma\sum_a\pi(a\mid S_{t+1})Q_t(S_{t+1},a)\)。

式（7.15）适用于 \(t<T-1\)。两步树备份回报为：

公式：\(\begin{aligned}G_{t:t+2}&\doteq R_{t+1}+\gamma\sum_{a\ne A_{t+1}}\pi(a\mid S_{t+1})Q_{t+1}(S_{t+1},a)\\&\quad+\gamma\pi(A_{t+1}\mid S_{t+1})\left(R_{t+2}+\gamma\sum_a\pi(a\mid S_{t+2})Q_{t+1}(S_{t+2},a)\right)\\&=R_{t+1}+\gamma\sum_{a\ne A_{t+1}}\pi(a\mid S_{t+1})Q_{t+1}(S_{t+1},a)+\gamma\pi(A_{t+1}\mid S_{t+1})G_{t+1:t+2}.\end{aligned}\)

上述两步回报适用于 \(t<T-2\)。它的后一种形式提示了树备份 n 步回报的一般递归定义：

公式（7.16）：\(G_{t:t+n}\doteq R_{t+1}+\gamma\sum_{a\ne A_{t+1}}\pi(a\mid S_{t+1})Q_{t+n-1}(S_{t+1},a)+\gamma\pi(A_{t+1}\mid S_{t+1})G_{t+1:t+n}\)。

这里 \(t<T-1\)、\(n\geq2\)。\(n=1\) 的情形用式（7.15）处理，只有终止前最后一步满足 \(G_{T-1:t+n}\doteq R_T\)。随后，按 n 步 Sarsa 的通常动作价值更新规则使用该目标：

公式：\(Q_{t+n}(S_t,A_t)\doteq Q_{t+n-1}(S_t,A_t)+\alpha\bigl[G_{t:t+n}-Q_{t+n-1}(S_t,A_t)\bigr]\)。

其中 \(0\leq t<T\)；所有其他状态—行动对的价值不变：只要 \(s\ne S_t\) 或 \(a\ne A_t\)，就有 \(Q_{t+n}(s,a)=Q_{t+n-1}(s,a)\)。算法伪代码见下一页方框。

**习题 7.11：**证明，如果近似动作价值不变，树备份回报（7.16）可写成基于期望的 TD 误差之和：

公式：\(G_{t:t+n}=Q(S_t,A_t)+\sum_{k=t}^{\min(t+n-1,T-1)}\delta_k\prod_{i=t+1}^{k}\gamma\pi(A_i\mid S_i)\)。

其中 \(\delta_t\doteq R_{t+1}+\gamma\bar V_t(S_{t+1})-Q(S_t,A_t)\)，\(\bar V_t\) 由式（7.8）给出。
