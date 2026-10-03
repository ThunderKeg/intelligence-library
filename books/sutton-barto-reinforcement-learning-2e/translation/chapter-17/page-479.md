此前尚未有人描述过使用 GVF 实现选项模型。我们的表述使用了 Modayil、White 和 Sutton（2014）为预测策略终止时的信号而提出的技巧。

在少数几项使用函数近似来学习选项模型的工作中，有 Sorg 和 Singh（2010）以及 Bacon、Harb 和 Precup（2017）的研究。

选项及选项模型向平均奖励情形的扩展，在文献中尚未得到发展。

**17.3**　Monahan（1982）很好地介绍了 POMDP 方法。Littman、Sutton 和 Singh（2002）提出 PSR 和测试。Jaeger（1997、1998、2000）提出 OOM。Michael Thon 在其博士论文（2017；Thon 和 Jaeger，2015）中提出序列系统，统一了 PSR、OOM 和许多其他工作。Tanner（2006；Sutton 和 Tanner，2005）发展了时间关系网络，后来又扩展到选项（Sutton、Rafols 和 Koop，2006）。

使用非马尔可夫状态表示进行强化学习的理论，由 Singh、Jaakkola 和 Jordan（1994；Jaakkola、Singh 和 Jordan，1995）明确提出。早期针对部分可观测性的强化学习方法由 Chrisman（1992）、McCallum（1993、1995）、Parr 和 Russell（1995）、Littman、Cassandra 和 Kaelbling（1995），以及 Lin 和 Mitchell（1992）提出。

**17.4**　在强化学习中加入建议与教学的早期尝试，包括 Lin（1992）、Maclin 和 Shavlik（1994）、Clouse（1996），以及 Clouse 和 Utgoff（1992）的工作。

不要把 Skinner 的塑造技术与 Ng、Harada 和 Russell（1999）提出的“基于势函数的塑造”（potential-based shaping）混淆。Wiewiora（2003）证明，后者等价于更简单的想法：如式 17.11 那样，提供一个价值函数的初始近似。

**17.5**　关于当今深度学习技术，我们推荐 Goodfellow、Bengio 和 Courville（2016）的著作。ANN 中的灾难性干扰问题由 McCloskey 和 Cohen（1989）、Ratcliff（1990），以及 French（1999）提出。经验回放缓冲区的想法由 Lin（1992）提出，并在 Atari 游戏系统的深度学习中得到广泛使用（第 16.5 节；Mnih 等，2013、2015）。
