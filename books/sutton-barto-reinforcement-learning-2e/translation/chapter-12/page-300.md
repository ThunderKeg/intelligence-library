$$
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\mathbf z_t+
\alpha\bigl(\mathbf w_t^\top\mathbf x_t-\mathbf w_{t-1}^\top\mathbf x_t\bigr)
(\mathbf z_t-\mathbf x_t).
$$

这里采用简写 \(\mathbf x_t\doteq\mathbf x(S_t)\)；\(\delta_t\) 与 TD(\(\lambda\)) 的式（12.6）定义相同；\(\mathbf z_t\) 定义为

$$
\mathbf z_t\doteq\gamma\lambda\mathbf z_{t-1}
+\bigl(1-\alpha\gamma\lambda\mathbf z_{t-1}^\top\mathbf x_t\bigr)\mathbf x_t. \tag{12.11}
$$

已有证明表明，这个算法生成的权重向量序列 \(\mathbf w_t\)（\(0\le t\le T\)）与在线 \(\lambda\)-回报算法完全相同（van Seijen 等，2016）。因此，图 12.8 左侧随机游走任务上的结果也是它在该任务上的结果。但现在算法的成本低得多。真在线 TD(\(\lambda\)) 所需内存与常规 TD(\(\lambda\)) 完全相同；每步计算量约增加 50%（资格迹更新中多了一次内积）。总体而言，每步计算复杂度仍为 \(O(d)\)，与 TD(\(\lambda\)) 相同。完整算法的伪代码见下框。

:::algorithm

### 真在线 TD(\(\lambda\))：估计 \(\mathbf w^\top\mathbf x\approx v_\pi\)

输入：待评估策略 \(\pi\)。

输入：特征函数 \(\mathbf x:\mathcal S^+\to\mathbb R^d\)，并令 \(\mathbf x(\text{终止状态},\cdot)=\mathbf0\)。

算法参数：步长 \(\alpha>0\)，迹衰减率 \(\lambda\in[0,1]\)。

初始化价值函数权重 \(\mathbf w\in\mathbb R^d\)（例如 \(\mathbf w=\mathbf0\)）。

对每个回合循环：

　初始化状态，并取得初始特征向量 \(\mathbf x\)。

　\(\mathbf z\leftarrow\mathbf0\)（\(d\) 维向量）。

　\(V_{\mathrm{old}}\leftarrow0\)（临时标量变量）。

　对该回合的每一步循环：

　　选择行动 \(A\sim\pi\)。

　　执行行动 \(A\)，观察奖励 \(R\) 和下一状态的特征向量 \(\mathbf x'\)。

　　\(V\leftarrow\mathbf w^\top\mathbf x\)。

　　\(V'\leftarrow\mathbf w^\top\mathbf x'\)。

　　\(\delta\leftarrow R+\gamma V'-V\)。

　　\(\mathbf z\leftarrow\gamma\lambda\mathbf z+
(1-\alpha\gamma\lambda\mathbf z^\top\mathbf x)\mathbf x\)。

　　\(\mathbf w\leftarrow\mathbf w+\alpha(\delta+V-V_{\mathrm{old}})\mathbf z
-\alpha(V-V_{\mathrm{old}})\mathbf x\)。

　　\(V_{\mathrm{old}}\leftarrow V'\)。

　　\(\mathbf x\leftarrow\mathbf x'\)。

　直到 \(\mathbf x'=\mathbf0\)（表示到达终止状态）。

:::end-algorithm

真在线 TD(\(\lambda\)) 中使用的资格迹（12.11）称为 **Dutch 迹（dutch trace）**，以区别 TD(\(\lambda\)) 中式（12.5）使用的**累积迹（accumulating trace）**。
