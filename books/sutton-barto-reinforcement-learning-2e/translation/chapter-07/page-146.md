主要思想是把状态换成行动（状态—行动对），再使用 ε-贪心策略。n 步 Sarsa 的备份图（图 7.3）与 n 步 TD 的备份图（图 7.1）一样，由交替出现的状态和行动串成；区别在于 Sarsa 的图都以行动开始，也以行动结束，而不是以状态开始和结束。我们根据估计的动作价值，重新定义 n 步回报（更新目标）：

公式（7.4）：\(G_{t:t+n}\doteq R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{n-1}R_{t+n}+\gamma^nQ_{t+n-1}(S_{t+n},A_{t+n}),\qquad n\geq1,\ 0\leq t<T-n\)。

若 \(t+n\geq T\)，则 \(G_{t:t+n}\doteq G_t\)。自然得到的算法为：

公式（7.5）：\(Q_{t+n}(S_t,A_t)\doteq Q_{t+n-1}(S_t,A_t)+\alpha\bigl[G_{t:t+n}-Q_{t+n-1}(S_t,A_t)\bigr],\qquad 0\leq t<T\)。

所有其他状态—行动对的价值保持不变：只要 \(s\ne S_t\) 或 \(a\ne A_t\)，就有 \(Q_{t+n}(s,a)=Q_{t+n-1}(s,a)\)。这就是 n 步 Sarsa 算法。下一页的方框给出伪代码，图 7.4 则举例说明它为何能比一步方法学得更快。

![图 7.3](assets/fig-7-3.png)

图 7.3：用于状态—行动价值的 n 步方法谱系的备份图。从 Sarsa(0) 的一步更新，一直到延伸至终止时刻的蒙特卡洛更新。中间的 n 步更新依据 n 步真实奖励，以及第 n 个后继状态—行动对的估计价值，并对它们作适当折扣。最右侧是 n 步期望 Sarsa 的备份图。

图内文字译注：1-step Sarsa aka Sarsa(0)＝一步 Sarsa，即 Sarsa(0)；2-step Sarsa＝两步 Sarsa；3-step Sarsa＝三步 Sarsa；n-step Sarsa＝n 步 Sarsa；∞-step Sarsa aka Monte Carlo＝无穷步 Sarsa，即蒙特卡洛；n-step Expected Sarsa＝n 步期望 Sarsa。空心圆表示状态，实心圆表示行动，灰色方块表示终止状态；最右侧的末端分支表示按策略对所有可能行动求期望。
