本章的论述主要依据 Sutton、McAllester、Singh 和 Mansour（2000）的工作；他们提出了“策略梯度方法”这一名称。Bhatnagar 等（2009）提供了一篇有用的综述。更早的相关工作之一出自 Aleksandrov、Sysoyev 和 Shemeneva（1968）。Thomas（2014）首先意识到：对于带折扣的回合式问题，本章方框中的算法需要包含 \(\gamma^t\) 因子。

**13.1** 示例 13.1 及本章与之相关的结果，是与 Eric Graves 合作完成的。

**13.2** 本书这里及第 334 页所述的策略梯度定理，首先由 Marbach 和 Tsitsiklis（1998，2001）得到，随后 Sutton 等（2000）独立得到。Cao 和 Chen（1997）得到了类似表达式。其他早期结果来自 Konda 和 Tsitsiklis（2000，2003）、Baxter 和 Bartlett（2001），以及 Baxter、Bartlett 和 Weaver（2001）。Sutton、Singh 和 McAllester（2000）还提出了一些后续结果。

**13.3** REINFORCE 出自 Williams（1987，1992）。Phansalkar 和 Thathachar（1995）证明了改进版 REINFORCE 算法的局部和全局收敛定理。

全行动算法最早见于一篇未出版、未完成但广为流传的论文（Sutton、Singh 和 McAllester，2000），后来由 Ciosek 和 Whiteson（2017，2018）进一步发展；他们称其为“期望策略梯度”（expected policy gradients）。Asadi、Allen、Roderick、Mohamed、Konidaris 和 Littman（2017）也进一步发展了它，并称之为“均值行动者—评论家”（mean actor critic）。

**13.4** Williams（1987，1992）在最初的工作中引入基线。Greensmith、Bartlett 和 Baxter（2004）分析了一种可能更好的基线（见 Dick，2015）。Thomas 和 Brunskill（2017）主张，可以使用依赖行动的基线而不引入偏差。

**13.5–6** 行动者—评论家方法是强化学习中最早得到研究的方法之一（Witten，1977；Barto、Sutton 和 Anderson，1983；Sutton，1984）。这里给出的算法基于 Degris、White 和 Sutton（2012）的工作。文献中，行动者—评论家方法有时称为优势行动者—评论家（advantage actor–critic，A2C）方法。

**13.7** 最早说明如何以这种方式处理连续行动的，似乎是 Williams（1987，1992）。第 335 页的图改绘自维基百科。
