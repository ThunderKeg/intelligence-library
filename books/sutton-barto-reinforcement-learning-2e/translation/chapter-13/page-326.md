幸运的是，**策略梯度定理**为这一难题提供了很好的理论答案。它给出性能对策略参数的梯度的解析表达式，也就是近似执行式（13.1）梯度上升所需要的量，而且该表达式不涉及状态分布的导数。回合式问题的策略梯度定理指出：

$$
\nabla J(\boldsymbol\theta)\propto
\sum_s\mu(s)\sum_a q_\pi(s,a)\nabla\pi(a\mid s,\boldsymbol\theta). \tag{13.5}
$$

其中，梯度是对 \(\boldsymbol\theta\) 各分量求偏导所得的列向量；\(\pi\) 表示参数向量 \(\boldsymbol\theta\) 对应的策略。符号 \(\propto\) 表示“正比于”。在回合式问题中，比例常数是回合的平均长度；在持续式问题中，比例常数为 1，因此关系实际上是等式。这里的分布 \(\mu\) 与第 9、10 章一样，是策略 \(\pi\) 下的同策略分布（见第 199 页）。前一页的方框给出了回合式问题策略梯度定理的证明。

## 13.3　REINFORCE：蒙特卡洛策略梯度

现在可以推导第一个策略梯度学习算法了。回顾式（13.1）中随机梯度上升的总体思路：我们需要取得样本，使样本梯度的期望正比于性能度量关于参数的真实梯度。样本梯度只需与该梯度成正比，因为任何比例常数都可以吸收到步长 \(\alpha\) 中，而步长本来就是任意选定的。策略梯度定理给出了一个与梯度成正比的精确表达式；剩下的问题是如何采样，使样本的期望等于或近似于这个表达式。注意，策略梯度定理右侧是对各状态求和，各项按状态在目标策略 \(\pi\) 下的出现频率加权；如果遵循 \(\pi\)，遇到各状态的比例就会符合这些权重。因此，

$$
\begin{aligned}
\nabla J(\boldsymbol\theta)
&\propto\sum_s\mu(s)\sum_a q_\pi(s,a)\nabla\pi(a\mid s,\boldsymbol\theta)\\
&=\mathbb E_\pi\!\left[
\sum_a q_\pi(S_t,a)\nabla\pi(a\mid S_t,\boldsymbol\theta)
\right].
\end{aligned}\tag{13.6}
$$

到这里，我们就可以停下，把式（13.1）的随机梯度上升算法具体写为

$$
\boldsymbol\theta_{t+1}\doteq
\boldsymbol\theta_t+\alpha\sum_a
\hat q(S_t,a,\mathbf w)\nabla\pi(a\mid S_t,\boldsymbol\theta). \tag{13.7}
$$

其中，\(\hat q\) 是学得的 \(q_\pi\) 近似。这一算法的更新涉及所有行动，因此称为**全行动方法**（all-actions method）。它很有前景，值得进一步研究，但这里我们关注经典的 REINFORCE 算法（Williams，1992）：其在时刻 \(t\) 的更新只涉及实际采取的那个行动 \(A_t\)。
