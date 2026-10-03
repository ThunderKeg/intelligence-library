## 10.5 差分半梯度 n 步 Sarsa

为了推广到 \(n\) 步自举，需要 TD 误差的 \(n\) 步版本。先把式（7.4）的 \(n\) 步回报推广到采用函数近似的差分形式：

\[
G_{t:t+n}\doteq R_{t+1}-\bar R_{t+n-1}+\cdots+R_{t+n}-\bar R_{t+n-1}+\hat q(S_{t+n},A_{t+n},\mathbf w_{t+n-1}), \tag{10.14}
\]

其中 \(\bar R\) 是 \(r(\pi)\) 的估计，\(n\geq1\)，且 \(t+n<T\)。如果 \(t+n\geq T\)，则照常定义 \(G_{t:t+n}\doteq G_t\)。于是 \(n\) 步 TD 误差为

\[
\delta_t\doteq G_{t:t+n}-\hat q(S_t,A_t,\mathbf w), \tag{10.15}
\]

然后就可以应用通常的半梯度 Sarsa 更新式（10.12）。完整算法的伪代码见下方方框。

:::source-box

### 差分半梯度 n 步 Sarsa：估计 \(\hat q\approx q_\pi\) 或 \(q_*\)

输入：可微函数 \(\hat q:\mathcal S\times\mathcal A\times\mathbb R^d\to\mathbb R\)，策略 \(\pi\)。

任意初始化价值函数权重 \(\mathbf w\in\mathbb R^d\)（例如 \(\mathbf w=\mathbf0\)）。

任意初始化平均奖励估计 \(\bar R\in\mathbb R\)（例如 \(\bar R=0\)）。

算法参数：步长 \(\alpha,\beta>0\)，较小的 \(\epsilon>0\)，正整数 \(n\)。

所有存储和访问操作（\(S_t,A_t,R_t\)）都可以把下标对 \(n+1\) 取模。

初始化并存储 \(S_0\) 和 \(A_0\)。

对每个时间步 \(t=0,1,2,\ldots\) 循环：

　执行行动 \(A_t\)。

　观察并存储下一奖励 \(R_{t+1}\) 和下一状态 \(S_{t+1}\)。

　选择并存储行动 \(A_{t+1}\sim\pi(\cdot\mid S_{t+1})\)，或者相对于 \(\hat q(S_{t+1},\cdot,\mathbf w)\) 采用 \(\epsilon\)-贪心选择。

$$
\tau\leftarrow t-n+1\qquad(\tau\text{ 是正在更新其估计的时刻})
$$

　如果 \(\tau\geq0\)：

$$
\delta\leftarrow\sum_{i=\tau+1}^{\tau+n}(R_i-\bar R)+\hat q(S_{\tau+n},A_{\tau+n},\mathbf w)-\hat q(S_\tau,A_\tau,\mathbf w)
$$

$$
\bar R\leftarrow\bar R+\beta\delta
$$

$$
\mathbf w\leftarrow\mathbf w+\alpha\delta\nabla\hat q(S_\tau,A_\tau,\mathbf w)
$$

:::end-source-box

**习题 10.9** 在差分半梯度 \(n\) 步 Sarsa 算法中，平均奖励的步长参数 \(\beta\) 必须很小，才能使 \(\bar R\) 成为平均奖励的良好长期估计。遗憾的是，这样一来，\(\bar R\) 会在许多步内受到其初始值的偏置影响，学习可能因此效率低下。另一种办法是用已观察奖励的样本均值作为 \(\bar R\)。它最初能快速适应，但长期来看也会变得适应缓慢。随着策略缓慢变化，\(\bar R\) 也会变化；这种长期非平稳性的可能性，使样本均值方法并不合适。实际上，平均奖励的步长参数正适合使用习题 2.7 的无偏恒定步长技巧。请说明要在上述差分半梯度 \(n\) 步 Sarsa 方框算法中使用这一技巧，需要作哪些具体修改。 □
