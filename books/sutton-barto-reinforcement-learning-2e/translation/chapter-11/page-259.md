对于动作价值，一步算法是半梯度期望 Sarsa：

$$
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\nabla\hat q(S_t,A_t,\mathbf w_t),\quad\text{其中} \tag{11.5}
$$

$$
\delta_t\doteq R_{t+1}+\gamma\sum_a\pi(a\mid S_{t+1})\hat q(S_{t+1},a,\mathbf w_t)-\hat q(S_t,A_t,\mathbf w_t),\quad\text{（回合式）或}
$$

$$
\delta_t\doteq R_{t+1}-\bar R_t+\sum_a\pi(a\mid S_{t+1})\hat q(S_{t+1},a,\mathbf w_t)-\hat q(S_t,A_t,\mathbf w_t).\quad\text{（持续式）}
$$

注意，这个算法不使用重要性采样。在表格型情形下，这样做显然恰当，因为被采样的唯一行动是 \(A_t\)；学习它的价值时，不必考虑其他行动。采用函数近似后，情况就不那么明确了：不同状态—行动对都参与同一个总体近似，我们可能希望赋予它们不同权重。要妥善解决这一问题，还需要更透彻地理解强化学习中函数近似的理论。

在这些算法的多步推广中，状态价值与动作价值算法都涉及重要性采样。半梯度 Sarsa 的 \(n\) 步版本为

$$
\mathbf w_{t+n}\doteq\mathbf w_{t+n-1}+\alpha\rho_{t+1}\cdots\rho_{t+n}\bigl[G_{t:t+n}-\hat q(S_t,A_t,\mathbf w_{t+n-1})\bigr]\nabla\hat q(S_t,A_t,\mathbf w_{t+n-1}), \tag{11.6}
$$

其中，

$$
G_{t:t+n}\doteq R_{t+1}+\cdots+\gamma^{n-1}R_{t+n}+\gamma^n\hat q(S_{t+n},A_{t+n},\mathbf w_{t+n-1}),\quad\text{（回合式）或}
$$

$$
G_{t:t+n}\doteq R_{t+1}-\bar R_t+\cdots+R_{t+n}-\bar R_{t+n-1}+\hat q(S_{t+n},A_{t+n},\mathbf w_{t+n-1}).\quad\text{（持续式）}
$$

这里对回合终点的处理略显简略。在第一种情形下，\(k\ge T\)（\(T\) 是该回合最后一个时间步）时，\(\rho_k\) 应取 1；如果 \(t+n\ge T\)，\(G_{t:t+n}\) 应取 \(G_t\)。

回想一下，第 7 章还介绍了一种完全不涉及重要性采样的异策略算法：\(n\) 步树备份算法。其半梯度版本为

$$
\mathbf w_{t+n}\doteq\mathbf w_{t+n-1}+\alpha\bigl[G_{t:t+n}-\hat q(S_t,A_t,\mathbf w_{t+n-1})\bigr]\nabla\hat q(S_t,A_t,\mathbf w_{t+n-1}), \tag{11.7}
$$

$$
G_{t:t+n}\doteq\hat q(S_t,A_t,\mathbf w_{t+n-1})+\sum_{k=t}^{t+n-1}\delta_k\prod_{i=t+1}^{k}\gamma\pi(A_i\mid S_i), \tag{11.8}
$$

其中 \(\delta_t\) 按本页开头为期望 Sarsa 给出的定义。第 7 章还定义了一种统一所有动作价值算法的算法：\(n\) 步 \(Q(\sigma)\)。该算法以及 \(n\) 步状态价值算法的半梯度形式，留给读者作为习题。

**习题 11.1**　把 \(n\) 步异策略 TD 的式（7.9）转换为半梯度形式，并分别给出回合式与持续式情形下回报的相应定义。□

**∗习题 11.2**　把 \(n\) 步 \(Q(\sigma)\) 的式（7.11）和（7.17）转换为半梯度形式，并给出同时覆盖回合式与持续式情形的定义。□
