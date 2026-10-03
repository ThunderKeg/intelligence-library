## 书目与历史评注

Ludvig、Bellemare 和 Pearson（2011），以及 Shah（2012），分别在心理学和神经科学的语境中综述强化学习。这些文献可与本章以及下一章关于强化学习与神经科学的内容配合阅读。

**14.1**　Dayan、Niv、Seymour 和 Daw（2006）关注经典条件作用与操作性条件作用之间的交互，特别是经经典条件作用形成的反应与操作性反应发生冲突的情境。他们提出一个 Q-learning 框架，对这种交互的某些方面建模。Modayil 和 Sutton（2014）用移动机器人展示了一种结合固定反应与在线预测学习的控制方法的有效性。他们称之为**巴甫洛夫式控制**，并强调它不同于常见的强化学习控制方法：它基于预测来执行固定反应，而不是最大化奖励。Ross（1933）的机电机器，尤其是 Walter 的“乌龟”的学习型版本（Walter，1951），都是巴甫洛夫式控制的很早期实例。

**14.2.1**　Kamin（1968）最先报告经典条件作用中的阻断现象，如今通常称为 Kamin 阻断。Moore 和 Schmajuk（2008）出色地总结了阻断现象、由此激发的研究，以及它对动物学习理论的持久影响。Gibbs、Cool、Land、Kehoe 和 Gormezano（1991）描述了兔瞬膜反应的二阶条件作用及其与串联复合刺激条件作用的关系。Finch 和 Culler（1934）报告，在“通过各阶次维持动物动机”的条件下，获得了狗前腿撤回反应的五阶条件作用。

**14.2.2**　Rescorla–Wagner 模型所包含的“动物感到意外时才发生学习”这一思想，来自 Kamin（1969）。除 Rescorla 和 Wagner 的模型外，经典条件作用模型还有 Klopf（1988）、Grossberg（1975）、Mackintosh（1975）、Moore 和 Stickney（1980）、Pearce 和 Hall（1980），以及 Courville、Daw 和 Touretzky（2006）的模型。Schmajuk（2008）综述了经典条件作用模型。Wagner（2008）从现代心理学角度评述了 Rescorla–Wagner 模型及类似的基础元素学习理论。

**14.2.3**　经典条件作用 TD 模型的早期版本见 Sutton 和 Barto（1981a）。那篇工作还预测：时间上先出现的刺激会压过阻断；Kehoe、Schreurs 和 Graham（1987）后来在兔瞬膜实验中证实了这一点。Sutton 和 Barto（1981a）也最早认识到 Rescorla–Wagner 模型与最小均方（LMS）学习规则，即 Widrow–Hoff 规则（Widrow 和 Hoff，1960），几乎相同。Sutton 开发 TD 算法（Sutton，1984、1988）后，对这一早期模型作了修订；它首次作为 TD 模型发表在 Sutton 和 Barto（1987）中，并在 Sutton 和 Barto（1990）中得到更完整的阐述，本节主要依据后者。Moore 及同事进一步探索了 TD 模型及其可能的神经实现（Moore、Desmond、Berthier、Blazis、Sutton 和 Barto，1986；Moore 和 Blazis，1989；Moore、Choi 和 Brunzell，1998；Moore、Marks、Castagna 和 Polewan，2001）。Klopf（1988）的经典条件作用驱力—强化理论扩展了 TD 模型，用于解释更多实验细节，例如习得曲线的 S 形。在其中一些文献中，TD 指的是“时间导数”（Time Derivative），而非“时序差分”（Temporal Difference）。
