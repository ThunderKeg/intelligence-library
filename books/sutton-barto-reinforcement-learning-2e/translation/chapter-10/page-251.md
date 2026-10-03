:::source-box

### 差分半梯度 Sarsa：估计 \(\hat q\approx q_*\)

输入：可微的动作价值函数参数化 \(\hat q:\mathcal S\times\mathcal A\times\mathbb R^d\to\mathbb R\)。

算法参数：步长 \(\alpha,\beta>0\)，较小的 \(\epsilon>0\)。

任意初始化价值函数权重 \(\mathbf w\in\mathbb R^d\)（例如 \(\mathbf w=\mathbf 0\)）。

任意初始化平均奖励估计 \(\bar R\in\mathbb R\)（例如 \(\bar R=0\)）。

初始化状态 \(S\) 与行动 \(A\)。

对每个时间步循环：

　执行行动 \(A\)，观察 \(R,S'\)。

　根据 \(\hat q(S',\cdot,\mathbf w)\) 选择 \(A'\)（例如采用 \(\epsilon\)-贪心）。

$$
\delta\leftarrow R-\bar R+\hat q(S',A',\mathbf w)-\hat q(S,A,\mathbf w)
$$

$$
\bar R\leftarrow\bar R+\beta\delta
$$

$$
\mathbf w\leftarrow\mathbf w+\alpha\delta\nabla\hat q(S,A,\mathbf w)
$$

$$
S\leftarrow S'
$$

$$
A\leftarrow A'
$$

:::end-source-box

**习题 10.6** 假设有一个 MDP，无论采取何种策略，都会无限地产生确定的奖励序列 \(+1,0,+1,0,+1,0,\ldots\)。严格说来，这不满足遍历性：不存在稳态极限分布 \(\mu_\pi\)，式（10.7）中的极限也不存在。尽管如此，式（10.6）所定义的平均奖励却存在。它是多少？现在考虑这个 MDP 中的两个状态。从状态 A 出发，奖励序列恰好如上所述，从 \(+1\) 开始；从状态 B 出发，奖励序列则从 \(0\) 开始，随后是 \(+1,0,+1,0,\ldots\)。我们希望计算 A 和 B 的差分价值。遗憾的是，从这两个状态出发时，差分回报（10.9）的隐含极限不存在，因而不能用它来定义差分价值。为补救这一点，可以改为把状态的差分价值定义为

\[
v_\pi(s)\doteq\lim_{\gamma\uparrow1}\lim_{h\to\infty}\sum_{t=0}^{h}\gamma^t\bigl(\mathbb E_\pi[R_{t+1}\mid S_0=s]-r(\pi)\bigr). \tag{10.13}
\]

按照这个定义，状态 A 和 B 的差分价值分别是多少？ □

**习题 10.7** 考虑一个马尔可夫奖励过程：三个状态 A、B、C 构成一个环，状态按环的顺序确定性地转移。进入 A 时获得 \(+1\) 的奖励，其他情况下奖励为 \(0\)。用式（10.13）求这三个状态的差分价值。 □

**习题 10.8** 第 251 页方框中的伪代码使用 \(\delta_t\) 作为误差来更新 \(\bar R_t\)，而不是直接使用 \(R_{t+1}-\bar R_t\)。两种误差都能起作用，但用 \(\delta_t\) 更好。为理解原因，考虑习题 10.7 中的三状态环形马尔可夫奖励过程。平均奖励估计应趋向其真实值 \(\frac13\)。假设这个估计已经等于 \(\frac13\)，并且保持不变，那么 \(R_{t+1}-\bar R_t\) 的误差序列是什么？按式（10.10）计算的 \(\delta_t\) 序列又是什么？如果允许平均奖励估计随误差变化，哪种误差序列会产生更稳定的估计？为什么？ □
