## 文献与历史评注

**8.1** 本章关于规划与学习的总体观点，是多年逐渐形成的；作者自身的工作贡献了一部分（Sutton，1990、1991a、1991b；Barto、Bradtke 和 Singh，1991、1995；Sutton 和 Pinette，1985；Sutton 和 Barto，1981b），也深受 Agre 和 Chapman（1990；Agre，1988）、Bertsekas 和 Tsitsiklis（1989）、Singh（1993）等人的影响。作者还深受潜伏学习的心理学研究（Tolman，1932），以及关于思维本质的心理学观点（例如 Galanter 和 Gerstenhaber，1956；Craik，1943；Campbell，1960；Dennett，1978）的影响。本书第三部分的 14.6 节把基于模型和无模型方法与学习及行为的心理学理论联系起来；15.11 节讨论大脑可能如何实现这两类方法。

**8.2** 我们用来描述不同强化学习方法的“直接”和“间接”两个术语，来自自适应控制文献（例如 Goodwin 和 Sin，1984），那里也用它们作同样区分。自适应控制所说的**系统辨识**（system identification），对应这里的模型学习（例如 Goodwin 和 Sin，1984；Ljung 和 Söderstrom，1983；Young，1984）。Dyna 架构由 Sutton（1990）提出，本节与下一节的结果基于该文报告的结果。Barto 和 Singh（1990）讨论了比较直接与间接强化学习方法的一些问题。将 Dyna 扩展到线性函数近似的早期工作，分别由 Sutton、Szepesvári、Geramifard 和 Bowling（2008），以及 Parr、Li、Taylor、Painter-Wakefield 和 Littman（2008）完成。

**8.3** 一些基于模型的强化学习研究，把探索奖励与乐观初始化推向了逻辑上的极端：对所有尚未充分探索的选择，都假定它们会产生最大奖励，再计算最优路径去检验。Kearns 和 Singh（2002）的 \(E^3\) 算法与 Brafman 和 Tennenholtz（2003）的 R-max 算法，保证在关于状态数和行动数的多项式时间内找到接近最优的解。这通常仍慢得不适于实际算法，但很可能是最坏情形下能做到的最好结果。

**8.4** Moore 和 Atkeson（1993）与 Peng 和 Williams（1993）同时、独立地发展出优先扫描。第 170 页框中的结果来自 Peng 和 Williams（1993）；第 171 页框中的结果来自 Moore 和 Atkeson。此领域后续的重要工作包括 McMahan 和 Gordon（2005）及 van Seijen 和 Sutton（2013）。

**8.5** 本节深受 Singh（1993）的实验影响。

**8.6–7** 轨迹采样从一开始便隐含于强化学习中，但在 Barto、Bradtke 和 Singh（1995）介绍 RTDP 时得到最明确的强调。他们认识到 Korf（1990）的“学习型
