图 13.2 对比了短走廊网格世界（示例 13.1）中，带基线和不带基线的 REINFORCE 的表现。这里用作基线的近似状态价值函数是 \(\hat v(s,\mathbf w)=w\)，即 \(\mathbf w\) 只有一个分量 \(w\)。

## 13.5 行动者—评论家方法

在带基线的 REINFORCE 中，学到的状态价值函数估计每次状态转移的**第一个**状态的价值。这个估计构成后续回报的基线，但它是在该次转移采取行动之前作出的，因此不能用来评价该行动。在**行动者—评论家**（actor–critic）方法中，状态价值函数还用于转移的**第二个**状态。第二个状态的估计价值经过折扣再加上奖励，构成单步回报 \(G_{t:t+1}\)；它是实际回报的一个有用估计，从而提供了评价行动的办法。如本书讨论价值函数 TD 学习时所见，单步回报虽然引入偏差，却常因方差和计算便利性而优于实际回报。我们也知道如何用 \(n\) 步回报和资格迹灵活调整偏差大小（第 7、12 章）。如果以这种方式用状态价值函数评价行动，该函数就称为**评论家**（critic），整体策略梯度方法称为行动者—评论家方法。注意，梯度估计中的偏差并非自举本身所致：即使评论家是用蒙特卡洛方法学得，行动者的估计仍有偏差。

先看单步行动者—评论家方法，它类似于第 6 章介绍的 TD(0)、Sarsa(0) 和 Q-learning 等 TD 方法。单步方法的主要优点是完全在线、增量式更新，却避免了资格迹的复杂性。它们是资格迹方法的一个特例，但更易理解。单步行动者—评论家方法把 REINFORCE 式（13.11）中的完整回报替换为单步回报，并使用学到的状态价值函数作基线：

\[
\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+\alpha\bigl(G_{t:t+1}-\hat v(S_t,\mathbf w)\bigr)
\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)}{\pi(A_t\mid S_t,\boldsymbol\theta_t)}. \tag{13.12}
\]

\[
=\boldsymbol\theta_t+\alpha\bigl(R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w)-\hat v(S_t,\mathbf w)\bigr)
\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)}{\pi(A_t\mid S_t,\boldsymbol\theta_t)}. \tag{13.13}
\]

\[
=\boldsymbol\theta_t+\alpha\delta_t
\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)}{\pi(A_t\mid S_t,\boldsymbol\theta_t)}. \tag{13.14}
\]

与之配合学习状态价值函数的自然方法是半梯度 TD(0)。下一页顶部方框给出了完整算法的伪代码。注意，现在这是完全在线的增量式算法：状态、行动和奖励一出现就被处理，之后不再回访。
