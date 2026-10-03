![图 12.8：在线与离线 λ-回报算法](assets/fig-12-8.png)

**图 12.8**　19 状态随机游走结果（例 7.1）：在线与离线 \(\lambda\)-回报算法的表现。这里的指标是回合结束时的均方价值误差 \(\overline{\mathrm{VE}}\)，这本应最有利于离线算法。尽管如此，在线算法的表现仍略微更好。作为对照，\(\lambda=0\) 的曲线对两种方法相同。

图内文字译注：左图标题 On-line \(\lambda\)-return algorithm = true online TD(\(\lambda\))＝“在线 \(\lambda\)-回报算法＝真在线 TD(\(\lambda\))”；右图标题 Off-line \(\lambda\)-return algorithm (from Section 12.1)＝“离线 \(\lambda\)-回报算法（见 12.1 节）”；纵轴 RMS error at the end of the episode over the first 10 episodes＝“前 10 个回合在回合结束时的均方根误差”；横轴 \(\alpha\)＝“步长 \(\alpha\)”；各曲线旁的 \(\lambda=0,0.4,0.8,0.9,0.95,0.975,0.99,1\) 为对应的迹衰减参数值。

## 12.5　真在线 TD(\(\lambda\))

刚介绍的在线 \(\lambda\)-回报算法，目前是表现最好的时序差分算法。它是一个理想算法，在线 TD(\(\lambda\)) 只能近似它。然而，按前述方式实现的在线 \(\lambda\)-回报算法十分复杂。能否把这个前向视角算法转换成采用资格迹、计算高效的后向视角算法？在线性函数近似情形下，确实存在一种与在线 \(\lambda\)-回报算法完全等价、而且便于计算的实现。它称为**真在线 TD(\(\lambda\))**，因为它比 TD(\(\lambda\)) 算法更忠实于在线 \(\lambda\)-回报算法这一理想形式。

真在线 TD(\(\lambda\)) 的推导略显复杂，这里不展开（见下一节，以及 van Seijen 等，2016 年论文的附录），但思路很简单。在线 \(\lambda\)-回报算法生成的权重向量序列可排列成一个三角形：

$$
\begin{array}{ccccc}
\mathbf w_0^0\\
\mathbf w_0^1&\mathbf w_1^1\\
\mathbf w_0^2&\mathbf w_1^2&\mathbf w_2^2\\
\mathbf w_0^3&\mathbf w_1^3&\mathbf w_2^3&\mathbf w_3^3\\
\vdots&\vdots&\vdots&\vdots&\ddots\\
\mathbf w_0^T&\mathbf w_1^T&\mathbf w_2^T&\mathbf w_3^T&\cdots\quad\mathbf w_T^T
\end{array}
$$

每个时间步产生三角形的一行。实际上，真正需要的只是对角线上的权重向量 \(\mathbf w_t^t\)。其中第一个 \(\mathbf w_0^0\) 是本回合的初始权重向量，最后一个 \(\mathbf w_T^T\) 是最终权重向量；中间每个权重向量 \(\mathbf w_t^t\)，都参与了各次更新中 \(n\) 步回报的自举。在最终算法中，为去掉上标，将对角线上的权重向量重新记为 \(\mathbf w_t\doteq\mathbf w_t^t\)。于是，策略是找到一种紧凑、高效的方式，根据前一个向量计算每个 \(\mathbf w_t^t\)。若能做到，在线性情形 \(\hat v(s,\mathbf w)=\mathbf w^\top\mathbf x(s)\) 下，就得到真在线 TD(\(\lambda\)) 算法：
