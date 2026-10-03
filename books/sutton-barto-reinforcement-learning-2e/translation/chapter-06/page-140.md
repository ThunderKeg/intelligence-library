**6.5** Q-learning 由 Watkins（1989）提出。他给出的收敛证明纲要，经 Watkins 和 Dayan（1992）完善为严格证明。Jaakkola、Jordan 和 Singh（1994）以及 Tsitsiklis（1994）证明了更一般的收敛结果。

**6.6** 期望 Sarsa 算法由 George John（1994）提出；他称其为“Q-learning”，并强调它作为异策略算法相对于 Q-learning 的优势。本书第一版把期望 Sarsa 作为一道习题给出时，我们尚不知道 John 的工作；van Seijen、van Hasselt、Whiteson 和 Weiring（2009）确立期望 Sarsa 的收敛性质及其优于常规 Sarsa 和 Q-learning 的条件时，也不知道这项工作。本章图 6.3 改编自他们的结果。van Seijen 等人把“期望 Sarsa”专门定义为同策略方法（本书第一版也如此）；现在我们用这个名称指代目标策略和行为策略可以不同的一般算法。van Hasselt（2011）指出期望 Sarsa 的一般异策略视角，并称它为“广义 Q-learning”（General Q-learning）。

**6.7** 最大化偏差和双重学习由 van Hasselt（2010，2011）提出并深入研究。图 6.5 中的 MDP 示例改编自 van Hasselt（2011）的图 4.1。

**6.8** 后继状态（afterstate）与“决策后状态”（post-decision state）的概念相同（Van Roy、Bertsekas、Lee 和 Tsitsiklis，1997；Powell，2011）。
