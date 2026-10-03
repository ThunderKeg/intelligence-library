为完成这个例子，只需指定这两个函数近似器的形式。把策略参数向量分为两部分：\(\boldsymbol\theta=[\boldsymbol\theta_\mu,\boldsymbol\theta_\sigma]^\top\)，一部分用于近似均值，另一部分用于近似标准差。均值可以近似为线性函数。标准差必须始终为正，用线性函数的指数来近似更合适。因此，

\[
\mu(s,\boldsymbol\theta)\doteq\boldsymbol\theta_\mu^\top\mathbf x_\mu(s)\quad\text{且}\quad\sigma(s,\boldsymbol\theta)\doteq\exp\!\bigl(\boldsymbol\theta_\sigma^\top\mathbf x_\sigma(s)\bigr), \tag{13.20}
\]

其中 \(\mathbf x_\mu(s)\) 和 \(\mathbf x_\sigma(s)\) 是状态特征向量，可以用 §9.5 介绍的某种方法构造。采用这些定义，本章其余部分介绍的所有算法都可用来学习选择实数行动。

**习题 13.4**　证明，对于高斯策略参数化（式（13.19）和（13.20）），资格向量分为以下两部分：

\[
\nabla\ln\pi(a\mid s,\boldsymbol\theta_\mu)=\frac{\nabla\pi(a\mid s,\boldsymbol\theta_\mu)}{\pi(a\mid s,\boldsymbol\theta)}=\frac{a-\mu(s,\boldsymbol\theta)}{\sigma(s,\boldsymbol\theta)^2}\mathbf x_\mu(s),\quad\text{以及}
\]

\[
\nabla\ln\pi(a\mid s,\boldsymbol\theta_\sigma)=\frac{\nabla\pi(a\mid s,\boldsymbol\theta_\sigma)}{\pi(a\mid s,\boldsymbol\theta)}=\left(\frac{\bigl(a-\mu(s,\boldsymbol\theta)\bigr)^2}{\sigma(s,\boldsymbol\theta)^2}-1\right)\mathbf x_\sigma(s).
\]

□

**习题 13.5**　伯努利逻辑单元（Bernoulli-logistic unit）是一些人工神经网络中使用的一种类似随机神经元的单元（§9.7）。在时间 \(t\)，它的输入是特征向量 \(\mathbf x(S_t)\)；输出 \(A_t\) 是取 0 或 1 的随机变量，满足 \(\Pr\{A_t=1\}=P_t\)、\(\Pr\{A_t=0\}=1-P_t\)（伯努利分布）。令 \(h(s,0,\boldsymbol\theta)\) 和 \(h(s,1,\boldsymbol\theta)\) 为策略参数 \(\boldsymbol\theta\) 下，该单元在状态 \(s\) 对两个行动的偏好。假定行动偏好之差由输入向量的加权和给出，即 \(h(s,1,\boldsymbol\theta)-h(s,0,\boldsymbol\theta)=\boldsymbol\theta^\top\mathbf x(s)\)，其中 \(\boldsymbol\theta\) 是单元的权重向量。

(a) 证明：若用指数 soft-max 分布（式（13.2））把行动偏好转为策略，则 \(P_t=\pi(1\mid S_t,\boldsymbol\theta_t)=1/\bigl(1+\exp(-\boldsymbol\theta_t^\top\mathbf x(S_t))\bigr)\)（逻辑函数）。

(b) 收到回报 \(G_t\) 时，蒙特卡洛 REINFORCE 从 \(\boldsymbol\theta_t\) 到 \(\boldsymbol\theta_{t+1}\) 的更新是什么？

(c) 通过计算梯度，用 \(a\)、\(\mathbf x(s)\) 和 \(\pi(a\mid s,\boldsymbol\theta)\) 表示伯努利逻辑单元的资格 \(\nabla\ln\pi(a\mid s,\boldsymbol\theta)\)。

对第 3 小题的提示：令 \(P=\pi(1\mid s,\boldsymbol\theta)\)，分别对两个行动，用链式法则计算其对数的导数。把两个结果合并成一个依赖于 \(a\) 和 \(P\) 的表达式；再对 \(\boldsymbol\theta^\top\mathbf x(s)\) 用一次链式法则，注意逻辑函数 \(f(x)=1/(1+e^{-x})\) 的导数是 \(f(x)(1-f(x))\)。 □
