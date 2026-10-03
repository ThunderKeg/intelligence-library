## 书目与历史注释

讨论学习与决策神经科学同本书所述强化学习方法之间联系的文献数量极多，这里只能选引其中一小部分。Niv（2009）、Dayan 和 Niv（2008）、Gimcher（2011）、Ludvig、Bellemare 和 Pearson（2011），以及 Shah（2012），都是很好的入门文献。

强化学习理论正与经济学、进化生物学和数学心理学一道，帮助建立人类及非人灵长类动物选择行为神经机制的定量模型。本章侧重学习，因此只略微涉及决策神经科学。Glimcher（2003）介绍了“神经经济学”领域；在其中，强化学习从经济学视角帮助研究决策的神经基础。另见 Glimcher 和 Fehr（2013）。Dayan 和 Abbott（2001）的神经科学计算与数学建模教科书，也讨论了强化学习在这些方法中的作用。Sterling 和 Laughlin（2015）从使适应行为得以高效运行的一般设计原则出发，研究学习的神经基础。

**15.1**　基础神经科学有许多优秀的介绍。Kandel、Schwartz、Jessell、Siegelbaum 和 Hudspeth（2013）是权威且非常全面的资料。

**15.2**　Berridge 和 Kringelbach（2008）综述了奖励和愉悦的神经基础，指出奖励处理有许多维度，涉及许多神经系统。篇幅所限，我们无法讨论 Berridge 和 Robinson（1998）颇具影响力的研究；他们区分刺激的享乐效应，即所谓“喜欢”（liking），与动机效应，即所谓“想要”（wanting）。Hare、O’Doherty、Camerer、Schultz 和 Rangel（2008）从经济学视角研究价值相关信号的神经基础，区分目标价值、决策价值和预测误差。决策价值等于目标价值减去行动成本。另见 Rangel、Camerer 和 Montague（2008）、Rangel 和 Hare（2010），以及 Peters 和 Büchel（2010）。

**15.3**　Schultz、Dayan 和 Montague（1997）对多巴胺神经元活动的奖励预测误差假说作了最有影响力的论述。Montague、Dayan 和 Sejnowski（1996）最早明确提出这个假说。他们的表述指的是奖励预测误差（reward prediction error，RPE），并没有具体称之为 TD 误差；不过，从他们对假说的展开可以清楚看出，所指的就是 TD 误差。据我们所知，最早认识到 TD 误差与多巴胺的联系的是 Montague、Dayan、Nowlan、Pouget 和 Sejnowski（1993）；受 Schultz 团队关于多巴胺信号的研究结果启发，他们提出一种由 TD 误差调节的 Hebb 式学习规则。Quartz、Dayan、Montague 和 Sejnowski（1992）的一篇摘要也指出了这一联系。Montague 和 Sejnowski（1994）强调预测在脑中的重要性，并概述了怎样通过多巴胺系统这类广泛分布的神经调节系统，实现由 TD 误差调节的预测性 Hebb 式学习。
