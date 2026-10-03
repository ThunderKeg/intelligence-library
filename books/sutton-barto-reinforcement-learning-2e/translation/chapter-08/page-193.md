实时 A*”（LRTA*）算法是一种异步 DP 算法：它既适用于 Korf 关注的确定性问题，也适用于随机问题。与 LRTA* 相比，RTDP 还允许在执行行动的间隔中更新许多状态的价值。Barto 等人（1995）把 Korf（1990）对 LRTA* 的收敛证明，与 Bertsekas（1982；另见 Bertsekas 和 Tsitsiklis，1989）关于无折扣随机最短路径问题中异步 DP 收敛的结果结合，证明了本章所述的收敛结论。把模型学习与 RTDP 结合称为**自适应 RTDP**（Adaptive RTDP），也由 Barto 等人（1995）提出，并在 Barto（2011）中讨论。

**8.9** 关于启发式搜索，推荐参阅 Russell 和 Norvig（2009）及 Korf（1988）等人的教材和综述。Peng 和 Williams（1993）研究了本节建议的更新向前聚焦方法。

**8.10** Abramson（1990）的期望结果模型，是一种用于双人游戏的 rollout 算法，模拟的双方都随机走棋。他认为即使采用随机走法，它也是一种“强有力的启发式方法”，兼具精确、准确、容易估计、高效计算和不依赖领域的特点。Tesauro 和 Galperin（1997）证明 rollout 算法能有效提高双陆棋程序的水平；他们借用双陆棋局面评价中的“rollout”一词：以不同的随机掷骰序列，把局面反复走到底。Bertsekas、Tsitsiklis 和 Wu（1997）研究用于组合优化问题的 rollout 算法；Bertsekas（2013）综述它们在离散确定性优化中的应用，指出它们的效果“常常出人意料地好”。

**8.11** MCTS 的核心思想由 Coulom（2006）以及 Kocsis 和 Szepesvári（2006）提出。他们建立在先前的蒙特卡洛规划算法研究之上；两篇文献也回顾了这些研究。Browne、Powley、Whitehouse、Lucas、Cowling、Rohlfshagen、Tavener、Perez、Samothrakis 和 Colton（2012）对 MCTS 方法及其应用作了出色的综述。David Silver 对本节的思路和表述作出了贡献。
