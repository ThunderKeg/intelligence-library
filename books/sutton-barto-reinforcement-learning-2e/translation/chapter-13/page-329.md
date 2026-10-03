作为随机梯度方法，REINFORCE 具有良好的理论收敛性质。依构造，每个回合的期望更新方向与性能梯度的方向相同。因此，当 \(\alpha\) 足够小时，期望性能能够提高；在步长递减且满足标准随机近似条件时，它会收敛到局部最优。不过，REINFORCE 是蒙特卡洛方法，方差可能很大，从而学习缓慢。

**习题 13.3**　在第 13.1 节，我们考虑了以行动偏好的 softmax（13.2）参数化策略，并使用线性行动偏好（13.3）。利用定义和初等微积分，证明对于这种参数化方式，资格向量为

$$
\nabla\ln\pi(a\mid s,\boldsymbol\theta)
=\mathbf x(s,a)-\sum_b\pi(b\mid s,\boldsymbol\theta)\mathbf x(s,b). \tag{13.9}
$$

□

## 13.4　带基线的 REINFORCE

策略梯度定理（13.5）可以推广为：把行动价值与任意基线 \(b(s)\) 比较：

$$
\nabla J(\boldsymbol\theta)\propto
\sum_s\mu(s)\sum_a
\bigl(q_\pi(s,a)-b(s)\bigr)\nabla\pi(a\mid s,\boldsymbol\theta). \tag{13.10}
$$

只要基线不随 \(a\) 变化，它就可以是任何函数，甚至可以是随机变量；方程仍然成立，因为被减去的部分为零：

$$
\sum_a b(s)\nabla\pi(a\mid s,\boldsymbol\theta)
=b(s)\nabla\sum_a\pi(a\mid s,\boldsymbol\theta)
=b(s)\nabla 1=0.
$$

与上一节类似，利用带基线的策略梯度定理（13.10）可以推导更新规则。所得的是含一般基线的新版 REINFORCE：

$$
\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+
\alpha\bigl(G_t-b(S_t)\bigr)
\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)}
{\pi(A_t\mid S_t,\boldsymbol\theta_t)}. \tag{13.11}
$$

基线可以恒为零，因此这个更新严格推广了 REINFORCE。一般来说，基线不改变更新的期望值，但会对更新的方差产生很大影响。例如，第 2.8 节表明，类似的基线能显著降低梯度赌博机算法的方差，进而加快学习。在赌博机算法中，基线只是一个数，即迄今所见奖励的平均值；但在马尔可夫决策过程中，基线应随状态而变。有些状态下所有行动的价值都高，需要较高的基线来区分价值更高与较低的行动；另一些状态下所有行动的价值都低，低基线才合适。

一种自然的基线选择是状态价值的估计 \(\hat v(S_t,\mathbf w)\)，其中 \(\mathbf w\in\mathbb R^d\) 是用前几章介绍的方法之一学得的权重向量。
