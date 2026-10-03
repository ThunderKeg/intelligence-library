**12.8** 最早发表的关于可变 \(\lambda\) 的讨论也许来自 Watkins（1989）：他指出，在 Q(\(\lambda\)) 中，如果选择了非贪心行动，就可以暂时把 \(\lambda\) 设为 \(0\)，从而截断更新序列（图 12.12）。

可变 \(\lambda\) 在本书第一版中已有介绍。可变 \(\gamma\) 的源头是关于选项（options）的研究（Sutton、Precup 和 Singh，1999）及其先行工作（Sutton，1995a）；后来在 GQ(\(\lambda\)) 论文中被明确提出（Maei 和 Sutton，2010），该论文还给出了一些 \(\lambda\)-回报的递归形式。

Yu（2012）发展了另一种可变 \(\lambda\) 的概念。

**12.9** 异策略资格迹由 Precup 等（2000，2001）提出，随后由 Bertsekas 和 Yu（2009）、Maei（2011）、Maei 和 Sutton（2010）、Yu（2012）以及 Sutton、Mahmood、Precup 和 van Hasselt（2014）进一步发展。最后一篇文献尤其为带一般状态依赖 \(\lambda\) 和 \(\gamma\) 的异策略 TD 方法提供了有力的前向视角。本节的呈现方式似乎是新的。

本节以一个简洁的预期 Sarsa(\(\lambda\)) 算法结束。尽管它是自然的算法，但据我们所知，先前文献中没有对它作过描述或测试。

**12.10** Watkins 的 Q(\(\lambda\)) 来自 Watkins（1989）。Munos、Stepleton、Harutyunyan 和 Bellemare（2016）证明了表格型、回合式、离线版本的收敛性。Peng 和 Williams（1994，1996）以及 Sutton、Mahmood、Precup 和 van Hasselt（2014）提出了其他 Q(\(\lambda\)) 算法。树备份(\(\lambda\)) 来自 Precup、Sutton 和 Singh（2000）。

**12.11** GTD(\(\lambda\)) 来自 Maei（2011），GQ(\(\lambda\)) 来自 Maei 和 Sutton（2010）。HTD(\(\lambda\)) 由 White 和 White（2016）提出，基于 Hackman（2012）的单步 HTD 算法。Yu（2017）介绍了梯度 TD 方法理论的最新发展。强调 TD(\(\lambda\)) 由 Sutton、Mahmood 和 White（2016）提出，他们证明了其稳定性。Yu（2015，2016）证明了其收敛性，算法本身由 Hallak 等（2015，2016）发展。
