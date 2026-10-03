**9.5** 本章对线性函数近似各种可能做法的介绍，以 Barto（1990）的论述为基础。

**9.5.2** Konidaris、Osentoski 和 Thomas（2011）以一种简单形式引入傅里叶基，适用于状态空间为多维连续空间、待近似函数不要求周期性的强化学习任务。

**9.5.3** “粗编码（coarse coding）”一词出自 Hinton（1984），本书图 9.6 基于他的一幅图。Waltz 和 Fu（1965）给出了这类函数近似在强化学习系统中的早期例子。

**9.5.4** 包括散列在内的瓦片编码由 Albus（1971，1981）引入。他以“**小脑模型关节控制器**”（cerebellar model articulator controller，CMAC）描述这种方法；文献有时也用 CMAC 称呼瓦片编码。“瓦片编码”这一名称始见于本书第一版，不过以瓦片来描述 CMAC 的思路取自 Watkins（1989）。许多强化学习系统使用过瓦片编码（例如 Shewchuk 和 Dean，1990；Lin 和 Kim，1991；Miller、Scalera 和 Kim，1994；Sofge 和 White，1992；Tham，1994；Sutton，1996；Watkins，1989），其他学习控制系统也使用过（例如 Kraft 和 Campagna，1990；Kraft、Miller 和 Dietz，1992）。本节很大程度上借鉴 Miller 和 Glanz（1996）的工作。多种语言都有通用的瓦片编码软件，例如 http://incompleteideas.net/tiles/tiles3.html。

**9.5.5** 自 Broomhead 和 Lowe（1988）把径向基函数与人工神经网络联系起来以后，使用径向基函数进行函数近似受到广泛关注。Powell（1987）回顾了 RBF 更早的用法；Poggio 和 Girosi（1989，1990）深入发展并应用了这一方法。

**9.6** 自动调整步长参数的方法包括 RMSprop（Tieleman 和 Hinton，2012）、Adam（Kingma 和 Ba，2015）、Delta-Bar-Delta（Jacobs，1988）等随机元下降方法、Delta-Bar-Delta 的增量式推广（Sutton，1992b，c；Mahmood 等，2012），以及非线性推广（Schraudolph，1999，2002）。专为强化学习设计的方法包括 AlphaBound（Dabney 和 Barto，2012）、SID 和 NOSID（Dabney，2014）、TIDBD（Kearney 等，撰写中），以及随机元下降在策略梯度学习中的应用（Schraudolph、Yu 和 Aberdeen，2006）。

**9.7** McCulloch 和 Pitts（1943）提出把阈值逻辑单元作为抽象神经元模型，开启了人工神经网络（ANN）的发展史。作为分类或回归的学习方法，ANN 大致经历了几个阶段：用单层 ANN 学习的感知机（Rosenblatt，1962）和 ADALINE（自适应线性单元，Widrow 和 Hoff，1960）阶段；用多层 ANN 学习的误差反向传播阶段（LeCun，1985；Rumelhart、Hinton 和 Williams，1986）；以及当下强调表示学习的深度学习阶段（例如 Bengio、Courville 和 Vincent，2012；Goodfellow、Bengio 和 Courville，2016）。关于 ANN 的著作很多，例如 Haykin（1994）、Bishop（1995）和 Ripley（2007）。
