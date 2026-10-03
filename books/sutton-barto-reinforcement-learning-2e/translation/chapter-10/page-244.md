$$
\mathbf w_{t+1}\doteq\mathbf w_t+
\alpha\bigl[U_t-\hat q(S_t,A_t,\mathbf w_t)\bigr]
\nabla\hat q(S_t,A_t,\mathbf w_t).
\tag{10.1}
$$

例如，一步 Sarsa 方法的更新为

$$
\mathbf w_{t+1}\doteq\mathbf w_t+
\alpha\bigl[R_{t+1}+\gamma\hat q(S_{t+1},A_{t+1},\mathbf w_t)
-\hat q(S_t,A_t,\mathbf w_t)\bigr]
\nabla\hat q(S_t,A_t,\mathbf w_t).
\tag{10.2}
$$

我们称它为*回合式半梯度一步 Sarsa*。对于固定策略，这种方法的收敛方式与 TD(0) 相同，并具有同类误差界（式（9.14））。

要形成控制方法，需要把这种动作价值预测方法与策略改进、行动选择技术结合起来。适用于连续行动或大型离散行动集合的技术，仍是持续研究且尚无明确解决方案的课题。另一方面，如果行动集合是离散的，且规模不太大，就可以使用前面章节已建立的技术。也就是说，对下一状态 \(S_{t+1}\) 中每个可选行动 \(a\)，计算 \(\hat q(S_{t+1},a,\mathbf w_t)\)，然后找出贪心行动 \(A_{t+1}^*=\arg\max_a\hat q(S_{t+1},a,\mathbf w_t)\)。策略改进时，在本章讨论的同策略情形中，把估计策略调整为贪心策略的一种柔性近似，例如 \(\epsilon\)-贪心策略。行动也按照这一策略选择。完整算法的伪代码如下。

:::source-box

### 回合式半梯度 Sarsa：估计 \(\hat q\approx q_*\)

输入：可微的动作价值函数参数化形式 \(\hat q:\mathcal S\times\mathcal A\times\mathbb R^d\to\mathbb R\)。

算法参数：步长 \(\alpha>0\)，很小的 \(\epsilon>0\)。

任意初始化价值函数权重 \(\mathbf w\in\mathbb R^d\)（例如令 \(\mathbf w=\mathbf 0\)）。

对每个回合循环：

　令 \(S,A\) 为该回合的初始状态和行动（例如按 \(\epsilon\)-贪心策略选择）。

　对该回合的每一步循环：

　　执行行动 \(A\)，观察 \(R,S'\)。

　　如果 \(S'\) 是终止状态：

$$
\mathbf w\leftarrow\mathbf w+
\alpha\bigl[R-\hat q(S,A,\mathbf w)\bigr]\nabla\hat q(S,A,\mathbf w)
$$

　　　转入下一回合。

　　否则，根据 \(\hat q(S',\cdot,\mathbf w)\) 选择 \(A'\)（例如按 \(\epsilon\)-贪心策略）。

$$
\mathbf w\leftarrow\mathbf w+
\alpha\bigl[R+\gamma\hat q(S',A',\mathbf w)-\hat q(S,A,\mathbf w)\bigr]
\nabla\hat q(S,A,\mathbf w)
$$

　　令 \(S\leftarrow S'\)，\(A\leftarrow A'\)。

:::end-source-box

**示例 10.1：山地车任务。**考虑驾驶一辆动力不足的汽车驶上一条陡峭山路的任务，如图 10.1 左上角所示。难点在于，重力的作用强于汽车发动机；即使把油门踩到底，汽车也无法直接沿陡坡加速上行。唯一的办法是先远离目标，驶上左侧的相反斜坡。接着把油门踩到底，汽车就能获得足够的惯性，冲上陡坡，尽管它在整个上坡过程中一直减速。
