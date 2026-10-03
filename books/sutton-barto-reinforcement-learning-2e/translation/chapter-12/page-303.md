每个时间步 \(t<T\) 都更新辅助向量 \(\mathbf a_t\) 和 \(\mathbf z_t\)；到了时刻 \(T\)，观察到 \(G\) 后，便按式（12.14）用它们计算 \(\mathbf w_T\)。这样得到的最终结果，与计算特性欠佳的蒙特卡洛／LMS 算法（12.13）完全相同，但现在是每步时间和存储复杂度均为 \(O(d)\) 的增量算法。令人意外且颇有启发的是，资格迹这一概念（尤其是 Dutch 迹）竟出现在没有时序差分（TD）学习的场景中（对比 van Seijen 和 Sutton，2014）。看来资格迹根本不是 TD 学习所特有的，而是比它更基本的工具：只要想高效学习长期预测，就似乎需要资格迹。

## 12.7　Sarsa(\(\lambda\))

要把资格迹扩展到动作价值方法，本章已有的思想几乎不必改变。要学习近似动作价值 \(\hat q(s,a,\mathbf w)\)，而非近似状态价值 \(\hat v(s,\mathbf w)\)，就需要使用第 10 章给出的动作价值形式的 \(n\) 步回报：

$$
G_{t:t+n}\doteq R_{t+1}+\cdots+\gamma^{n-1}R_{t+n}
+\gamma^n\hat q(S_{t+n},A_{t+n},\mathbf w_{t+n-1}),
\qquad t+n<T,
$$

若 \(t+n\ge T\)，则 \(G_{t:t+n}\doteq G_t\)。据此可以构造动作价值形式的 \(\lambda\)-回报；除此之外，它与状态价值形式（12.3）完全相同。离线 \(\lambda\)-回报算法（12.4）的动作价值形式，只须用 \(\hat q\) 代替 \(\hat v\)：

$$
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha
\bigl[G_t^\lambda-\hat q(S_t,A_t,\mathbf w_t)\bigr]
\nabla\hat q(S_t,A_t,\mathbf w_t),\qquad t=0,\ldots,T-1. \tag{12.15}
$$

这里 \(G_t^\lambda\doteq G_{t:\infty}^\lambda\)。这个前向视角的复合备份图见图 12.9。注意它与 TD(\(\lambda\)) 算法的图（图 12.1）很相似。第一次更新向前看完整的一步，直到下一状态—行动对；第二次向前看两步，直到第二个状态—行动对；依此类推。最后一次更新以完整回报为依据。\(\lambda\)-回报中各个 \(n\) 步更新的权重，与 TD(\(\lambda\)) 和 \(\lambda\)-回报算法（12.3）中的权重相同。

称为 Sarsa(\(\lambda\)) 的动作价值时序差分方法，近似这一前向视角。它使用与前述 TD(\(\lambda\)) 相同的更新规则：

$$
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\mathbf z_t,
$$

自然地，TD 误差改用动作价值形式：

$$
\delta_t\doteq R_{t+1}+\gamma\hat q(S_{t+1},A_{t+1},\mathbf w_t)
-\hat q(S_t,A_t,\mathbf w_t), \tag{12.16}
$$

资格迹也改用动作价值形式：

$$
\begin{aligned}
\mathbf z_{-1}&\doteq\mathbf0,\\
\mathbf z_t&\doteq\gamma\lambda\mathbf z_{t-1}
+\nabla\hat q(S_t,A_t,\mathbf w_t),\qquad 0\le t\le T.
\end{aligned}
$$
