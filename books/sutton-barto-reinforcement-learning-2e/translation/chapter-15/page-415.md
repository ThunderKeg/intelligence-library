**15.5**　Schultz（1998）的综述文章，是进入多巴胺神经元奖励预测信号这一庞大文献领域的良好起点。Berns、McClure、Pagnoni 和 Montague（2001），Breiter、Aharon、Kahneman、Dale 和 Shizgal（2001），Pagnoni、Zink、Montague 和 Berns（2002），以及 O’Doherty、Dayan、Friston、Critchley 和 Dolan（2003），介绍了支持人脑中存在类似 TD 误差信号的功能性脑影像研究。

**15.6**　本节解释 TD 误差如何再现 Schultz 团队关于多巴胺神经元时相响应的主要结果，大体遵循 Barto（1995a）的论述。

**15.7**　本节主要依据 Takahashi、Schoenbaum 和 Niv（2008），以及 Niv（2009）。据我们所知，Barto（1995a）以及 Houk、Adams 和 Barto（1995）最早推测，行动者—评论家算法可能在基底神经节中实现。根据受试者参加工具性条件作用任务时的功能性磁共振成像结果，O’Doherty、Dayan、Schultz、Deichmann、Friston 和 Dolan（2004）提出，行动者和评论家最可能分别位于纹状体背侧部和腹侧部。Gershman、Moustafa 和 Ludvig（2014）关注基底神经节强化学习模型如何表征时间，讨论各种计算时间表征方法的证据及其含义。

本节描述的行动者—评论家架构的假设神经实现，几乎没有涉及已知的基底神经节解剖与生理细节。除 Houk、Adams 和 Barto（1995）更详细的假说外，许多其他假说都与解剖和生理结构建立了更具体的联系，并声称能够解释更多数据。其中包括 Suri 和 Schultz（1998，1999），Brown、Bullock 和 Grossberg（1999），Contreras-Vidal 和 Schultz（1999），Suri、Bargas 和 Arbib（2001），O’Reilly 和 Frank（2006），以及 O’Reilly、Frank、Hazy 和 Watz（2007）的假说。Joel、Niv 和 Ruppin（2002）批判性地评估其中几个模型在解剖学上的合理性，并提出一种替代方案，试图纳入基底神经节回路中此前被忽略的一些特征。

**15.8**　这里讨论的行动者学习规则，比 Barto 等人（1983）早期行动者—评论家网络中的规则更复杂。那个网络中，行动者单元的资格迹只是 \(A_t\times\mathbf x(S_t)\) 的迹，而非完整的 \(\bigl(A_t-\pi(1\mid S_t,\boldsymbol\theta)\bigr)\mathbf x(S_t)\)。当年的工作尚未得益于第 13 章的策略梯度理论，也没有利用 Williams（1986，1992）的成果；后者说明了由伯努利—logistic 单元组成的 ANN 如何实现策略梯度方法。
