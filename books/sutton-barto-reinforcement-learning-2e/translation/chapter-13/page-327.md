我们继续推导 REINFORCE，按照在式（13.6）中引入 \(S_t\) 的方式引入 \(A_t\)：将对随机变量可能取值的求和，改写为策略 \(\pi\) 下的期望，再对该期望采样。式（13.6）已包含适当的行动求和，但其中各项并未乘上形成 \(\pi\) 下期望所需的权重 \(\pi(a\mid S_t,\boldsymbol\theta)\)。因此，我们把每个求和项乘以、再除以该权重，在不改变等式的情况下引入它。从式（13.6）继续，有

$$
\begin{aligned}
\nabla J(\boldsymbol\theta)
&\propto\mathbb E_\pi\!\left[
\sum_a\pi(a\mid S_t,\boldsymbol\theta)q_\pi(S_t,a)
\frac{\nabla\pi(a\mid S_t,\boldsymbol\theta)}
{\pi(a\mid S_t,\boldsymbol\theta)}
\right]\\
&=\mathbb E_\pi\!\left[
q_\pi(S_t,A_t)
\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta)}
{\pi(A_t\mid S_t,\boldsymbol\theta)}
\right]
\quad\text{（用样本 }A_t\sim\pi\text{ 替换 }a\text{）}\\
&=\mathbb E_\pi\!\left[
G_t\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta)}
{\pi(A_t\mid S_t,\boldsymbol\theta)}
\right],
\quad\text{（因为 }\mathbb E_\pi[G_t\mid S_t,A_t]=q_\pi(S_t,A_t)\text{）}.
\end{aligned}
$$

其中，\(G_t\) 像往常一样是回报。最后一个方括号内的量正是我们所需的：每个时间步都可以从中取得样本，其期望与梯度成正比。用这个样本来实例化式（13.1）的通用随机梯度上升算法，得到 REINFORCE 更新：

$$
\boldsymbol\theta_{t+1}\doteq\boldsymbol\theta_t+
\alpha G_t\frac{\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)}
{\pi(A_t\mid S_t,\boldsymbol\theta_t)}. \tag{13.8}
$$

这个更新具有直观含义。每次增量与两个量的乘积成正比：回报 \(G_t\)，以及一个向量，即实际所选行动的概率的梯度除以该行动的概率。这个向量指向参数空间中最能提高将来再次访问 \(S_t\) 时重复选择 \(A_t\) 的概率的方向。更新沿此方向改变参数向量，幅度与回报成正比、与行动概率成反比。前者合理，因为它让参数朝着偏好高回报行动的方向移动得最多。后者也合理，否则经常被选中的行动会占优势——更新会更频繁地朝它们的方向进行——即使它们并不能带来最高回报，也可能胜出。

注意，REINFORCE 使用从时刻 \(t\) 直至回合结束的完整回报，包含此后的全部奖励。因此，REINFORCE 是蒙特卡洛算法，只在回合式问题上有明确的定义；所有更新都要在回合结束后回顾性地进行，这与第 5 章的蒙特卡洛算法一样。下一页方框中的算法明确展示了这一点。

注意，伪代码最后一行的更新看起来与式（13.8）很不一样。一个区别是：伪代码用简洁的表达式 \(\nabla\ln\pi(A_t\mid S_t,\boldsymbol\theta_t)\) 表示式（13.8）中的分式向量 \(\nabla\pi(A_t\mid S_t,\boldsymbol\theta_t)/\pi(A_t\mid S_t,\boldsymbol\theta_t)\)。由恒等式 \(\nabla\ln x=(\nabla x)/x\) 可知，这两种表达式等价。文献给这个向量起过多种名称，并采用过多种记号；这里我们简单地称它为**资格向量**（eligibility vector）。注意，算法中只有这一处出现了策略的参数化形式。
