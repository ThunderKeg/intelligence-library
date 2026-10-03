\[
\begin{aligned}
G_t^{\lambda a}\doteq{}&R_{t+1}+\gamma_{t+1}\Bigl((1-\lambda_{t+1})\bar V_t(S_{t+1})\\
&\quad+\lambda_{t+1}\bigl[\rho_{t+1}G_{t+1}^{\lambda a}+\bar V_t(S_{t+1})-\rho_{t+1}\hat q(S_{t+1},A_{t+1},\mathbf w_t)\bigr]\Bigr)\\
={}&R_{t+1}+\gamma_{t+1}\Bigl(\bar V_t(S_{t+1})+\lambda_{t+1}\rho_{t+1}\bigl[G_{t+1}^{\lambda a}-\hat q(S_{t+1},A_{t+1},\mathbf w_t)\bigr]\Bigr).
\end{aligned} \tag{12.26}
\]

其中 \(\bar V_t(S_{t+1})\) 由式（12.21）给出。这个 \(\lambda\)-回报同样可以近似写成 TD 误差之和：

\[
G_t^{\lambda a}\approx\hat q(S_t,A_t,\mathbf w_t)+\sum_{k=t}^{\infty}\delta_k^a\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i, \tag{12.27}
\]

这里使用基于行动的 TD 误差的期望形式：

\[
\delta_t^a\doteq R_{t+1}+\gamma_{t+1}\bar V_t(S_{t+1})-\hat q(S_t,A_t,\mathbf w_t). \tag{12.28}
\]

与前文一样，如果近似价值函数不变，这一近似就成为精确等式。

**习题 12.10** 证明：如果价值函数不变，式（12.27）是精确的。为少写一些符号，考虑 \(t=0\) 的情形，记 \(Q_k\doteq\hat q(S_k,A_k,\mathbf w)\)。提示：先展开 \(\delta_0^a\) 和 \(G_0^{\lambda a}\)，再写出 \(G_0^{\lambda a}-Q_0\)。 □

**习题 12.11** 一般异策略回报的截断版本记为 \(G_{t:h}^{\lambda a}\)。根据式（12.27），猜测它的正确方程。 □

完全仿照状态价值情形的步骤，可以先写出基于式（12.27）的前向视角更新，再用求和规则变换更新之和，最终推导出动作价值的下列资格迹形式：

\[
\mathbf z_t\doteq\gamma_t\lambda_t\rho_t\mathbf z_{t-1}+\nabla\hat q(S_t,A_t,\mathbf w_t). \tag{12.29}
\]

该资格迹与基于期望的 TD 误差（12.28）以及通常的半梯度参数更新规则（12.7）相结合，构成一个简洁高效的预期 Sarsa(\(\lambda\)) 算法，可应用于同策略或异策略数据。它可能是目前同类算法中最好的，尽管与后面几节介绍的某种方法结合之前，尚不能保证稳定。在同策略、\(\lambda\) 和 \(\gamma\) 为常数，且采用通常的状态—行动 TD 误差（12.16）时，它与 §12.7 的 Sarsa(\(\lambda\)) 算法相同。

**习题 12.12** 详细写出上述从式（12.27）推导式（12.29）的步骤。从更新式（12.15）开始，用式（12.26）的 \(G_t^{\lambda a}\) 代入 \(G_t^\lambda\)，然后按推导式（12.25）时的相同步骤进行。 □

当 \(\lambda=1\) 时，这些算法与相应的蒙特卡洛算法联系紧密。有人可能会以为，对回合式问题和离线更新，两者会完全等价；但实际关系更微妙，也稍弱一些。即使在最有利的条件下，等价的也不是每个回合的更新，而仅是更新的期望。这并不奇怪：随着轨迹展开，这些方法会作出不可撤销的更新；而真正的蒙特卡洛方法不会对目标策略下发生概率为零的轨迹作任何更新。尤其是，即使 \(\lambda=1\)，所有这些方法在其目标取决于当前价值估计时仍会自举；只是这种依赖在期望值中抵消。实践中这是好事还是坏事，是另一个问题。近期有人提出真正精确等价的方法（Sutton、Mahmood、Precup 和 van Hasselt，2014）。这些方法需要额外一个“暂定权重”向量，记录已作出但随后可能需要撤销（或加强）的更新，具体取决于后续行动。它们的状态价值版和动作价值版分别称为 PTD(\(\lambda\)) 和 PQ(\(\lambda\))，其中 P 表示 Provisional（暂定）。
