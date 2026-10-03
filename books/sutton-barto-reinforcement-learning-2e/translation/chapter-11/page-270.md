SGD 很有吸引力，因此人们投入了大量精力，试图找到在强化学习中有效使用它的实用办法。所有这类尝试都从选择要优化的误差或目标函数开始。本节和下一节将探究其中最流行的一种目标函数——以上一节介绍的贝尔曼误差为基础的目标——从何而来、又有何局限。尽管这种思路很流行，也很有影响力，我们在这里得出的结论却是：它走错了方向，无法产生良好的学习算法。不过，它失败的方式很有启发性，有助于理解怎样的思路可能更好。

先不考虑贝尔曼误差，而看一个更直接、也更天真的目标。时序差分学习由 TD 误差驱动；为什么不以最小化 TD 误差平方的期望为目标呢？在一般的函数近似情形中，带折扣的一步 TD 误差是

$$
\delta_t=R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w_t)
-\hat v(S_t,\mathbf w_t).
$$

于是，一个可能的目标函数是所谓的*均方 TD 误差*：

$$
\begin{aligned}
\overline{\mathrm{TDE}}(\mathbf w)
&=\sum_{s\in\mathcal S}\mu(s)\,
\mathbb E\!\left[\delta_t^2\mid S_t=s,\ A_t\sim\pi\right]\\
&=\sum_{s\in\mathcal S}\mu(s)\,
\mathbb E\!\left[\rho_t\delta_t^2\mid S_t=s,\ A_t\sim b\right]\\
&=\mathbb E_b[\rho_t\delta_t^2].
\end{aligned}
$$

最后一个等式假定 \(\mu\) 是行为策略 \(b\) 下遇到的状态分布。它恰好具有 SGD 所需的形式：目标是一个可以从经验中抽样估计的期望（记住，经验由行为策略 \(b\) 产生）。因此，按标准 SGD 思路，可以基于该期望的样本，推导每一步的更新：

$$
\begin{aligned}
\mathbf w_{t+1}
&=\mathbf w_t-\tfrac12\alpha\nabla(\rho_t\delta_t^2)\\
&=\mathbf w_t-\alpha\rho_t\delta_t\nabla\delta_t\\
&=\mathbf w_t+\alpha\rho_t\delta_t
\bigl[\nabla\hat v(S_t,\mathbf w_t)
-\gamma\nabla\hat v(S_{t+1},\mathbf w_t)\bigr].
\end{aligned}
\tag{11.23}
$$

这与半梯度 TD 算法（式（11.2））只有最后多出的那一项不同。它补全了梯度，使该方法成为具有良好收敛保证的真正 SGD 算法。我们称它为*朴素残差梯度算法*（参见 Baird，1995）。虽然朴素残差梯度算法能够稳健收敛，却未必收敛到理想的位置。
