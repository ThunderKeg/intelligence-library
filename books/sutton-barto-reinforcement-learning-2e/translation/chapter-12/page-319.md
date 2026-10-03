## 参考文献与历史评注

资格迹进入强化学习领域，源于 Klopf（1972）富有成果的思想。我们对资格迹的使用基于 Klopf 的工作（Sutton，1978a、1978b、1978c；Barto 和 Sutton，1981a、1981b；Sutton 和 Barto，1981a；Barto、Sutton 和 Anderson，1983；Sutton，1984）。我们可能是最早使用“资格迹”这一术语的人（Sutton 和 Barto，1981a）。刺激会在神经系统中产生对学习重要的后续效应，这一思想由来已久（见第 14 章）。资格迹最早的一些用法见第 13 章讨论的行动者—评论家方法（Barto、Sutton 和 Anderson，1983；Sutton，1984）。

**12.1** 复合更新在本书第一版中称为“复杂备份”（complex backups）。

\(\lambda\)-回报及其降低误差的性质由 Watkins（1989）提出，随后由 Jaakkola、Jordan 和 Singh（1994）进一步发展。本节及后续章节的随机游走结果是本书新增的，“前向视角”和“后向视角”这两个术语也是如此。\(\lambda\)-回报算法这一概念最早在本书第一版中引入。这里较细致的处理方式是与 Harm van Seijen 共同发展出来的（例如 van Seijen 和 Sutton，2014）。

**12.2** 带累积迹的 TD(\(\lambda\)) 由 Sutton（1988，1984）提出。Dayan（1992）证明了均值意义下的收敛性，随后许多研究者证明了高概率收敛性，包括 Peng（1993）、Dayan 和 Sejnowski（1994）、Tsitsiklis（1994），以及 Gurvits、Lin 和 Hanson（1994）。线性 TD(\(\lambda\)) 渐近 \(\lambda\) 依赖解的误差上界由 Tsitsiklis 和 Van Roy（1997）给出。

**12.3** 截断 TD 方法由 Cichosz（1995）和 van Seijen（2016）发展。

**12.4** 重做更新的思路由 van Seijen 广泛发展，最初称为“最佳匹配学习”（best-match learning）（van Seijen，2011；van Seijen、Whiteson、van Hasselt 和 Wiering，2011）。

**12.5** 真正在线 TD(\(\lambda\)) 主要归功于 Harm van Seijen（van Seijen 和 Sutton，2014；van Seijen 等，2016）；不过，其中一些关键想法也由 Hado van Hasselt 独立发现（私人交流）。“Dutch 迹”这一名称是为了认可两位研究者的贡献。替换迹出自 Singh 和 Sutton（1996）。

**12.6** 本节材料来自 van Hasselt 和 Sutton（2015）。

**12.7** 带累积迹的 Sarsa(\(\lambda\)) 最早由 Rummery 和 Niranjan（1994；Rummery，1995）作为控制方法探索。真正在线 Sarsa(\(\lambda\)) 由 van Seijen 和 Sutton（2014）提出。第 307 页的算法改编自 van Seijen 等（2016）。山地车结果为本书新作，但图 12.11 改编自 van Seijen 和 Sutton（2014）。
