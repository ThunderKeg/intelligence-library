利用这一更新目标，我们构造 \(\mathbf w_1\)。接着，把数据视界推进到第 2 步，该怎么办？此时除了新的 \(\mathbf w_1\)，我们还得到了 \(R_2\) 和 \(S_2\)，因此可以为从 \(S_0\) 开始的第一次更新构造更好的目标 \(G_{0:2}^{\lambda}\)，也可以为从 \(S_1\) 开始的第二次更新构造更好的目标 \(G_{1:2}^{\lambda}\)。利用这些改进的目标，我们再次从 \(\mathbf w_0\) 出发，重做在 \(S_1\) 和 \(S_2\) 上的更新，得到 \(\mathbf w_2\)。随后把视界推进到第 3 步，照此重复：一直回到起点，构造三个新目标，再从原来的 \(\mathbf w_0\) 出发重做所有更新，得到 \(\mathbf w_3\)，依此类推。每次视界前移，都从 \(\mathbf w_0\) 开始、使用前一视界的权重向量重做全部更新。

这个概念性算法对同一回合要作多遍处理，每个视界作一遍，每遍产生不同的权重向量序列。要清楚描述它，必须区分不同视界下算出的权重向量。用 \(\mathbf w_t^h\) 表示截至视界 \(h\) 的序列中、在时刻 \(t\) 产生价值估计所用的权重。每个序列中的第一个权重向量 \(\mathbf w_0^h\) 都继承自上一回合（所以对所有 \(h\) 都相同）；每个序列中的最后一个权重向量 \(\mathbf w_h^h\) 则确定算法最终的权重向量序列。在最终视界 \(h=T\)，我们得到最终权重 \(\mathbf w_T^T\)，它将成为下一回合的初始权重。按这些约定，上段所述前三个序列可明确写成：

$$
\begin{aligned}
h=1:\quad
\mathbf w_1^1&\doteq\mathbf w_0^1+\alpha\bigl[G_{0:1}^{\lambda}-\hat v(S_0,\mathbf w_0^1)\bigr]\nabla\hat v(S_0,\mathbf w_0^1),\\[1em]
h=2:\quad
\mathbf w_1^2&\doteq\mathbf w_0^2+\alpha\bigl[G_{0:2}^{\lambda}-\hat v(S_0,\mathbf w_0^2)\bigr]\nabla\hat v(S_0,\mathbf w_0^2),\\
\mathbf w_2^2&\doteq\mathbf w_1^2+\alpha\bigl[G_{1:2}^{\lambda}-\hat v(S_1,\mathbf w_1^2)\bigr]\nabla\hat v(S_1,\mathbf w_1^2),\\[1em]
h=3:\quad
\mathbf w_1^3&\doteq\mathbf w_0^3+\alpha\bigl[G_{0:3}^{\lambda}-\hat v(S_0,\mathbf w_0^3)\bigr]\nabla\hat v(S_0,\mathbf w_0^3),\\
\mathbf w_2^3&\doteq\mathbf w_1^3+\alpha\bigl[G_{1:3}^{\lambda}-\hat v(S_1,\mathbf w_1^3)\bigr]\nabla\hat v(S_1,\mathbf w_1^3),\\
\mathbf w_3^3&\doteq\mathbf w_2^3+\alpha\bigl[G_{2:3}^{\lambda}-\hat v(S_2,\mathbf w_2^3)\bigr]\nabla\hat v(S_2,\mathbf w_2^3).
\end{aligned}
$$

更新的一般形式为

$$
\mathbf w_{t+1}^h\doteq\mathbf w_t^h+
\alpha\bigl[G_{t:h}^{\lambda}-\hat v(S_t,\mathbf w_t^h)\bigr]
\nabla\hat v(S_t,\mathbf w_t^h),\qquad 0\le t<h\le T.
$$

这一更新连同 \(\mathbf w_t\doteq\mathbf w_t^t\)，定义了**在线 \(\lambda\)-回报算法**。

在线 \(\lambda\)-回报算法确实完全在线：在一个回合内，它每走一步 \(t\)，就只利用时刻 \(t\) 已获得的信息确定新的权重向量 \(\mathbf w_t\)。主要缺点是计算复杂：每一步都要重新处理截至当前已经历的整个回合部分。注意，它严格说来比离线 \(\lambda\)-回报算法更复杂；后者在终止时遍历全部时间步，但在回合进行期间不作任何更新。作为回报，可以预期在线算法比离线算法表现更好：回合进行期间，在线算法更新而离线算法不更新；到回合结束时也可能更好，因为用于自举的权重向量（在 \(G_{t:h}^{\lambda}\) 中）已经经历更多有用信息的更新。仔细查看图 12.8，就能看到这种效果：它比较了两种算法在 19 状态随机游走任务上的表现。
