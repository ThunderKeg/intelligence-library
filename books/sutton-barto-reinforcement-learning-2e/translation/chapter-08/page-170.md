:::algorithm

**确定性环境中的优先扫描**

初始化所有 \(s,a\) 的 \(Q(s,a)\)、\(Model(s,a)\)，并将 \(PQueue\) 置空。

一直重复：

（a）\(S\leftarrow\) 当前（非终止）状态。

（b）\(A\leftarrow policy(S,Q)\)。

（c）执行行动 \(A\)，观察由此得到的奖励 \(R\) 和状态 \(S'\)。

（d）\(Model(S,A)\leftarrow R,S'\)。

（e）\(P\leftarrow\left|R+\gamma\max_aQ(S',a)-Q(S,A)\right|\)。

（f）若 \(P>\theta\)，以优先级 \(P\) 把 \(S,A\) 插入 \(PQueue\)。

（g）在 \(PQueue\) 非空时，最多重复 \(n\) 次：

　　\(S,A\leftarrow first(PQueue)\)；

　　\(R,S'\leftarrow Model(S,A)\)；

　　\(Q(S,A)\leftarrow Q(S,A)+\alpha\left[R+\gamma\max_aQ(S',a)-Q(S,A)\right]\)；

　　对所有预计会通往 \(S\) 的 \(\bar S,\bar A\)：

　　　　\(\bar R\leftarrow\) 从 \(\bar S,\bar A\) 到 \(S\) 的预测奖励；

　　　　\(P\leftarrow\left|\bar R+\gamma\max_aQ(S,a)-Q(\bar S,\bar A)\right|\)；

　　　　若 \(P>\theta\)，以优先级 \(P\) 把 \(\bar S,\bar A\) 插入 \(PQueue\)。

:::end-algorithm

**例 8.4：迷宫中的优先扫描** 已发现优先扫描能大幅提高在迷宫任务中找到最优解的速度，通常快 5 到 10 倍。右图是一个典型例子。数据来自一系列与图 8.2 迷宫结构完全相同、仅网格分辨率不同的任务。相对于未设优先级的 Dyna-Q，优先扫描始终具有明显优势。两种系统每次环境交互最多执行 \(n=5\) 次更新。改编自 Peng 和 Williams（1993）。

![例 8.4 不同网格规模下优先扫描与 Dyna-Q 的更新次数](assets/fig-8-prioritized-maze.png)

图内文字译注：Updates until optimal solution＝找到最优解前的更新次数（纵轴为对数刻度）；Gridworld size (#states)＝网格世界规模（状态数）；蓝线为 Dyna-Q，红线为优先扫描。

将优先扫描扩展到随机环境并不困难。维护模型时，记录每个状态—行动对经历的次数，以及随后进入各状态的次数。这时，更新每个状态—行动对时，自然可以不用迄今采用的样本更新，而用考虑全部可能下一状态及其出现概率的**期望更新**。

优先扫描只是分配计算、提高规划效率的一种方式，可能还不是最好的方式。它的一项局限是采用期望更新；在随机环境中，这可能在低概率转移上浪费许多计算。下一节将说明，样本更新
