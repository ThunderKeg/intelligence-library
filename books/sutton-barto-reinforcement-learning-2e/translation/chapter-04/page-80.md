这说明发生了策略改进。这个例子里的新策略 \(\pi'\) 恰好最优，但一般只能保证它有所改进。

## 4.3 策略迭代

用 \(v_\pi\) 改进策略 \(\pi\) 得到更好的 \(\pi'\) 后，我们还可以计算 \(v_{\pi'}\)，再改进一次，得到更好的 \(\pi''\)。这样便得到单调改进的策略和值函数序列：

\[
\pi_0\xrightarrow{\mathrm E}v_{\pi_0}\xrightarrow{\mathrm I}\pi_1
\xrightarrow{\mathrm E}v_{\pi_1}\xrightarrow{\mathrm I}\pi_2
\xrightarrow{\mathrm E}\cdots\xrightarrow{\mathrm I}\pi_*
\xrightarrow{\mathrm E}v_*.
\]

这里，标记 \(\mathrm E\) 的箭头表示**策略评估**，标记 \(\mathrm I\) 的箭头表示**策略改进**。除非某个策略已经最优，否则下一个策略一定严格优于它。有限 MDP 只有有限多个确定性策略，因此该过程必定在有限次迭代后收敛到最优策略及最优价值函数。

这种求最优策略的方法称为**策略迭代**（policy iteration）。完整算法如下。注意，每次策略评估本身都是一个迭代计算，而且从前一个策略的价值函数开始。这通常会使策略评估收敛得快得多，推测原因是相邻策略的价值函数变化不大。

**策略迭代：使用迭代式策略评估，估计 \(\pi\approx\pi_*\)**

1. **初始化**：对每个 \(s\in\mathcal S\)，任意选择 \(V(s)\in\mathbb R\) 与 \(\pi(s)\in\mathcal A(s)\)；令 \(V(\text{terminal})=0\)。
2. **策略评估**：重复执行以下扫描，直到 \(\Delta<\theta\)；其中 \(\theta>0\) 是控制估计精度的小正数。
   1. \(\Delta\leftarrow0\)；
   2. 对每个 \(s\in\mathcal S\)：
      1. \(v\leftarrow V(s)\)；
      2. \(V(s)\leftarrow\sum_{s',r}p(s',r\mid s,\pi(s))[r+\gamma V(s')]\)；
      3. \(\Delta\leftarrow\max(\Delta,|v-V(s)|)\)。
3. **策略改进**：
   1. \(\text{policy-stable}\leftarrow\text{true}\)；
   2. 对每个 \(s\in\mathcal S\)：
      1. \(\text{old-action}\leftarrow\pi(s)\)；
      2. \(\pi(s)\leftarrow\arg\max_a\sum_{s',r}p(s',r\mid s,a)[r+\gamma V(s')]\)；
      3. 如果 \(\text{old-action}\ne\pi(s)\)，令 \(\text{policy-stable}\leftarrow\text{false}\)。
   3. 若 \(\text{policy-stable}\) 为真，则停止并返回 \(V\approx v_*\)、\(\pi\approx\pi_*\)；否则返回第 2 步。
