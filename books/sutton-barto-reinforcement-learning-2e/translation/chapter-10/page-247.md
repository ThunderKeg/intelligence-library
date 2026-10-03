## 10.2　半梯度 \(n\) 步 Sarsa

在半梯度 Sarsa 的更新式（10.1）中，用 \(n\) 步回报作为更新目标，就得到回合式半梯度 Sarsa 的 \(n\) 步版本。\(n\) 步回报可以直接从表格型形式（式（7.4））推广为函数近似形式：

$$
\begin{aligned}
G_{t:t+n}\doteq{}&
R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{n-1}R_{t+n}\\
&+\gamma^n\hat q(S_{t+n},A_{t+n},\mathbf w_{t+n-1}),
\qquad t+n<T.
\end{aligned}
\tag{10.4}
$$

同往常一样，当 \(t+n\ge T\) 时，令 \(G_{t:t+n}\doteq G_t\)。\(n\) 步更新式为

$$
\begin{aligned}
\mathbf w_{t+n}\doteq{}&
\mathbf w_{t+n-1}
+\alpha\bigl[G_{t:t+n}-\hat q(S_t,A_t,\mathbf w_{t+n-1})\bigr]\\
&\quad\cdot\nabla\hat q(S_t,A_t,\mathbf w_{t+n-1}),
\qquad 0\le t<T.
\end{aligned}
\tag{10.5}
$$

完整伪代码如下。

:::source-box

### 回合式半梯度 \(n\) 步 Sarsa：估计 \(\hat q\approx q_*\) 或 \(q_\pi\)

输入：可微的动作价值函数参数化形式 \(\hat q:\mathcal S\times\mathcal A\times\mathbb R^d\to\mathbb R\)。

输入：策略 \(\pi\)（如果要估计 \(q_\pi\)）。

算法参数：步长 \(\alpha>0\)、很小的 \(\epsilon>0\)、正整数 \(n\)。

任意初始化价值函数权重 \(\mathbf w\in\mathbb R^d\)（例如令 \(\mathbf w=\mathbf 0\)）。

所有保存和读取操作（涉及 \(S_t,A_t,R_t\)）的索引都可以模 \(n+1\) 取值。

对每个回合循环：

　初始化并存储非终止状态 \(S_0\)。

　选择并存储行动 \(A_0\sim\pi(\cdot\mid S_0)\)，或根据 \(\hat q(S_0,\cdot,\mathbf w)\) 按 \(\epsilon\)-贪心方式选择。

　令 \(T\leftarrow\infty\)。

　对 \(t=0,1,2,\ldots\) 循环：

　　如果 \(t<T\)：

　　　执行行动 \(A_t\)。

　　　观察并保存下一奖励为 \(R_{t+1}\)，下一状态为 \(S_{t+1}\)。

　　　如果 \(S_{t+1}\) 是终止状态，令 \(T\leftarrow t+1\)。

　　　否则，选择并存储 \(A_{t+1}\sim\pi(\cdot\mid S_{t+1})\)，或根据 \(\hat q(S_{t+1},\cdot,\mathbf w)\) 按 \(\epsilon\)-贪心方式选择。

　　令 \(\tau\leftarrow t-n+1\)（\(\tau\) 是其估计值正在更新的时间）。

　　如果 \(\tau\ge0\)：

$$
G\leftarrow\sum_{i=\tau+1}^{\min(\tau+n,T)}
\gamma^{i-\tau-1}R_i
$$

　　　如果 \(\tau+n<T\)，则令 \(G\leftarrow G+\gamma^n\hat q(S_{\tau+n},A_{\tau+n},\mathbf w)\)；此时 \(G=G_{\tau:\tau+n}\)。

$$
\mathbf w\leftarrow\mathbf w+
\alpha\bigl[G-\hat q(S_\tau,A_\tau,\mathbf w)\bigr]
\nabla\hat q(S_\tau,A_\tau,\mathbf w)
$$

　　直到 \(\tau=T-1\) 时结束循环。

:::end-source-box

如前所见，采用中等程度的自举，即令 \(n>1\)，往往表现最好。图 10.3 显示，在山地车任务上，当 \(n=8\) 时，这个算法通常比 \(n=1\) 学得更快，最终表现也更好。图 10.4 则更细致地研究了参数 \(\alpha\) 与 \(n\) 对这一任务学习速度的影响。
