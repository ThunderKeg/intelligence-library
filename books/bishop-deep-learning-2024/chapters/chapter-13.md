<!-- pdf-page: 423 -->

# 第 13 章 图神经网络

<aside class="chapter-guide"><strong>本章导读</strong><p>图神经网络把节点及其连接关系作为输入，通过相邻节点之间传递信息来学习表示。本章先说明图上的预测任务和节点重排的对称性，再介绍消息传递、图卷积、注意力及图级表示。</p></aside>

<figure class="chapter-opener">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/chapter-opener.png" alt="第 13 章的彩色章首插图，标有 Graph Neural Networks">
  <p class="figure-translation">图中文字：Graph Neural Networks → 图神经网络。</p>
</figure>

前几章已经接触过序列和图像形式的结构化数据，分别对应一维和二维的变量数组。更一般地，许多结构化数据最适合用图来描述，如图 13.1 所示。一般而言，图由一组称为**节点**（node）的对象和连接节点的**边**（edge）构成。节点和边都可以附带数据。例如，在分子中，节点和边对应离散变量，分别表示原子种类（碳、氮、氢等）和化学键种类（单键、双键等）。对于铁路网，每条铁路线可以对应一个连续变量，例如两座城市间的平均旅程时间。这里假定边具有对称性，比如从伦敦到剑桥的旅程时间与从剑桥到伦敦相同。这样的边用节点之间的无向连接表示。而万维网中的边是有向的，

<!-- pdf-page: 424 -->

<!-- join-previous-paragraph -->
因为网页 A 有指向网页 B 的超链接，并不意味着网页 B 也有指回网页 A 的链接。

<figure id="fig-13-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/fig-13-1.png" alt="三种图结构数据：咖啡因分子、城市铁路网和有向网页链接网络">
  <figcaption>图 13.1：图结构数据的三个例子：（a）由原子和化学键构成的咖啡因分子；（b）由城市和铁路线构成的铁路网；（c）由网页和超链接构成的万维网。</figcaption>
  <p class="figure-translation">图内地名：Leeds → 利兹；Cambridge → 剑桥；Oxford → 牛津；Bristol → 布里斯托；London → 伦敦。其余字母为化学元素符号。</p>
</figure>

其他图结构数据还包括蛋白质相互作用网络，其中节点是蛋白质，边表示成对蛋白质之间相互作用的强度；电路，其中节点是元件，边是导线；以及社交网络，其中节点是人，边是“好友”关系。也可以有更复杂的图结构。例如，公司的知识图谱可能包含人、文档、会议等多种节点，以及表示不同属性的多种边，例如某人出席了某次会议，或某文档引用了另一份文档。

本章探讨如何把深度学习应用于图结构数据。讨论图像时，我们已经遇到结构化数据的一个例子：图像数据向量 $\mathbf{x}$ 的各元素对应规则网格上的像素。因此，图像是图结构数据的一种特殊情况：节点是像素，边表示像素之间的相邻关系。卷积神经网络（CNN）利用了这种结构，将像素相对位置的先验知识纳入模型，同时利用分割等任务的**等变性**（equivariance）和分类等任务的**不变性**（invariance；见第 10 章）。借鉴图像 CNN 的思路，我们将构造适用于一般图数据的深度学习方法，即**图神经网络**（graph neural network，GNN；Zhou et al., 2018；Wu et al., 2019；Hamilton, 2020；Veličković, 2023）。我们会看到，深度学习处理图结构数据时，一个关键问题是：对于图中节点顺序的重新排列，模型应保持等变或不变。

<!-- pdf-page: 425 -->

## 13.1 图上的机器学习

图结构数据有许多应用，可以按预测目标大致分为节点属性、边属性和整张图的属性。例如，节点预测任务可以利用文档之间的超链接和引用关系，把文档按主题分类。

对于边，我们可能已知蛋白质网络中的一部分相互作用，希望预测是否还有其他相互作用。这类任务称为**边预测**（edge prediction）或**图补全**（graph completion）。还有一些任务的边事先已知，目标是找出图内的簇或“社群”。

最后，预测目标也可能涉及整张图。例如，我们可能希望预测某个分子是否溶于水。此时给定的不再是单张图，而是由不同图组成的数据集；可以把这些图视为取自某个共同分布，也就是假定各张图本身独立同分布。这样的任务可以看作图回归或图分类。

以分子溶解度分类为例，我们可能有一个带标签的分子训练集，以及一个需要预测溶解度的新分子测试集。这是前几章多次见到的标准**归纳式**（inductive）任务。不过，有些图预测任务是**传导式**（transductive）的：我们已知整张图的结构，也知道其中部分节点的标签，目标是预测其余节点的标签。例如，在一个大型社交网络中，我们要判断每个节点是真人还是自动机器人。少量节点可以人工标注，但对于庞大而持续变化的社交网络，逐一调查所有节点不可行。因此，训练时可以访问整张图以及部分节点的标签，并希望预测剩余节点的标签。这可以看作一种半监督学习。

除了直接解决预测任务，还可以在图上用深度学习发现有用的内部表示，以帮助完成各种后续任务。这称为**图表示学习**（graph representation learning）。例如，我们可以用大量分子结构训练深度学习系统，尝试建立分子基础模型；期望模型训练完成后，只需少量带标签数据，就能针对具体任务进行微调。

图神经网络为每个节点定义一个嵌入向量，通常用观测到的节点属性初始化，再经过一系列可学习的层进行变换，形成学习得到的表示。这类似于 Transformer 中的词嵌入或 token：它们经过一系列层处理后，其表示更能体现词语在其余文本中的意义（见第 12 章）。图神经网络还可以使用与边及整张图相关联的可学习嵌入。

<!-- pdf-page: 426 -->

<figure id="fig-13-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/fig-13-2.png" alt="一个五节点图在两种节点顺序下对应的两个邻接矩阵，蓝色方格表示有边">
  <figcaption>图 13.2：邻接矩阵示例：（a）五个节点组成的图；（b）采用一种节点顺序得到的邻接矩阵；（c）采用另一种节点顺序得到的邻接矩阵。</figcaption>
</figure>

### 13.1.1 图的性质

本章主要考虑**简单图**：任意一对节点之间至多有一条边；边无方向；也没有把节点连接到自身的自环。这个范围足以介绍图神经网络的关键概念，同时也涵盖许多实际应用。这些概念随后还可以推广到更复杂的图结构。

先引入图的记号和一些重要性质。图 $G=(V,E)$ 由节点或顶点的集合 $V$ 与边或连接的集合 $E$ 构成。把节点编号为 $n=1,\ldots,N$，并将节点 $n$ 到节点 $m$ 的边记为 $(n,m)$。若两个节点之间有边相连，它们称为**邻居**；节点 $n$ 的全部邻居组成的集合记为 $\mathcal N(n)$。

除图结构外，通常还能观测到与节点相关的数据。对每个节点 $n$，可用一个 $D$ 维列向量 $\mathbf x_n$ 表示其节点变量，再将这些向量组合成 $N\times D$ 的数据矩阵 $\mathbf X$，其中第 $n$ 行为 $\mathbf x_n^{\mathrm T}$。图中的边也可能附带数据变量，不过我们先只讨论节点变量（边变量见 13.3.2 节）。

### 13.1.2 邻接矩阵

指定图中各条边的一种方便方法是使用**邻接矩阵**（adjacency matrix）$\mathbf A$。定义邻接矩阵前，必须先选定节点顺序。若图中有 $N$ 个节点，可以将它们编号为 $n=1,\ldots,N$。邻接矩阵是 $N\times N$ 矩阵：凡节点 $n$ 到节点 $m$ 有边的位置 $(n,m)$ 取 1，其余位置取 0。对于无向图，若 $n$ 到 $m$ 有边，$m$ 到 $n$ 也有边，因此所有 $n,m$ 都满足 $A_{mn}=A_{nm}$，邻接矩阵是对称的。图 13.2 给出了一个例子。

邻接矩阵既然定义了图的结构，我们可以考虑

<!-- pdf-page: 427 -->

<!-- join-previous-paragraph -->
直接将它作为神经网络的输入。具体做法可以是把矩阵“展平”，例如将各列首尾相接，构成一个长列向量。但这种做法有一个重要问题：如图 13.2 所示，邻接矩阵取决于任意选择的节点顺序。例如，预测分子的溶解度显然不应取决于编写邻接矩阵时给节点安排的顺序。节点排列数随节点数呈阶乘增长，因此靠大型数据集或数据增强来学习对排列的不变性并不现实。我们应当把这种不变性作为构造网络架构时的归纳偏置。

### 13.1.3 置换等变性

为从数学上描述节点标签的重新排列，引入**置换矩阵** $\mathbf P$。它与邻接矩阵同样大小，并指定一种节点顺序的置换。每行和每列恰好有一个 1，其余元素都是 0；位置 $(n,m)$ 的 1 表示置换后节点 $n$ 被重新标为节点 $m$。例如，图 13.2 中的两种节点顺序对应 $(A,B,C,D,E)\to(C,E,A,D,B)$，其置换矩阵为（习题 13.1）

$$
\mathbf P=\begin{pmatrix}
0&0&1&0&0\\
0&0&0&0&1\\
1&0&0&0&0\\
0&0&0&1&0\\
0&1&0&0&0
\end{pmatrix}. \tag{13.1}
$$

可以更形式化地定义置换矩阵。先引入 $n=1,\ldots,N$ 对应的标准单位列向量 $\mathbf u_n$：除了第 $n$ 个元素为 1，其余元素均为 0。用这个记号，单位矩阵为

$$
\mathbf I=\begin{pmatrix}
\mathbf u_1^{\mathrm T}\\
\mathbf u_2^{\mathrm T}\\
\vdots\\
\mathbf u_N^{\mathrm T}
\end{pmatrix}. \tag{13.2}
$$

再引入将 $n$ 映射到 $m=\pi(n)$ 的置换函数 $\pi(\cdot)$，相应的置换矩阵为

$$
\mathbf P=\begin{pmatrix}
\mathbf u_{\pi(1)}^{\mathrm T}\\
\mathbf u_{\pi(2)}^{\mathrm T}\\
\vdots\\
\mathbf u_{\pi(N)}^{\mathrm T}
\end{pmatrix}. \tag{13.3}
$$

重新排列图中节点的标签时，相应的节点数据矩阵 $\mathbf X$ 的各行也按照 $\pi(\cdot)$ 置换。这可以通过左乘 $\mathbf P$ 得到（习题 13.4）：

<!-- pdf-page: 428 -->

$$
\widetilde{\mathbf X}=\mathbf P\mathbf X. \tag{13.4}
$$

邻接矩阵的行和列都要置换。行仍可通过左乘 $\mathbf P$ 置换；列则通过右乘 $\mathbf P^{\mathrm T}$ 置换，从而得到新的邻接矩阵（习题 13.5）：

$$
\widetilde{\mathbf A}=\mathbf P\mathbf A\mathbf P^{\mathrm T}. \tag{13.5}
$$

把深度学习用于图结构数据时，必须以数值形式表示图结构，才能输入神经网络；这就要求给节点安排一个顺序。但具体选择哪个顺序是任意的，因此必须保证图的整体属性不依赖于这个顺序。换言之，网络预测应对节点标签重排保持不变：

$$
y(\widetilde{\mathbf X},\widetilde{\mathbf A})=y(\mathbf X,\mathbf A). \tag{13.6}
$$

这里 $y(\cdot,\cdot)$ 是网络输出；式 (13.6) 表示**不变性**（invariance）。

我们也可能需要预测单个节点的属性。这时若重新排列节点标签，相应预测也应按同样方式排列，使某项预测始终对应同一个节点，而不受节点顺序的选择影响。换言之，节点预测应对节点标签重排保持**等变**（equivariant）：

$$
y(\widetilde{\mathbf X},\widetilde{\mathbf A})=\mathbf P y(\mathbf X,\mathbf A). \tag{13.7}
$$

这里 $y(\cdot,\cdot)$ 是网络的输出向量，每个节点对应一个元素；式 (13.7) 表示**等变性**（equivariance）。

## 13.2 神经消息传递

把深层神经网络用于图结构数据时，一个关键设计要求是保证节点标签置换下的不变性或等变性。另一个要求是发挥深层网络的表示能力，因此保留“层”的概念：一层是可以反复应用的计算变换。如果每一层对节点重排都等变，那么连续应用多层仍具有等变性，同时每层的计算都能利用图结构。

对于输出为节点级预测的网络，整个网络将按要求保持等变。若网络用于预测图级属性，则可以在最后加入一层，使其对输入的置换保持不变。我们还希望每一层都是灵活的非线性函数，且对参数可微，从而能够利用自动微分得到的梯度，通过随机梯度下降训练。

图的大小各不相同。例如，不同分子的原子数可能不同，因此像标准神经网络那样使用固定长度表示，

<!-- pdf-page: 429 -->

<!-- join-previous-paragraph -->
并不合适。另一个要求是网络能够处理可变长度的输入，这一点与 Transformer 网络相同（见第 12 章）。有些图可能非常大，例如拥有数百万参与者的社交网络，因此还希望模型有良好的扩展能力。参数共享会发挥重要作用：它既能让网络架构内置不变性与等变性，也有助于模型扩展到大型图。

<figure id="fig-13-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/fig-13-3.png" alt="卷积滤波器与图消息传递的对应关系：左侧局部像素块向下一层像素汇聚，右侧邻居节点把消息传给中心节点">
  <figcaption>图 13.3：图像的卷积滤波器可以表示为图结构的计算。（a）深层卷积网络第 $l+1$ 层中，节点 $i$ 计算的滤波器取决于第 $l$ 层局部像素块的激活值。（b）把同一计算结构表示为图：邻居向节点 $i$ 传递“消息”。</figcaption>
</figure>

### 13.2.1 卷积滤波器

要建立满足上述要求的框架，可以借鉴卷积神经网络处理图像的方法。首先，图像是图结构数据的一种特殊情况：节点是像素，边连接图像中相邻的像素；这里的相邻既包括对角相邻，也包括水平或垂直相邻（见第 10 章）。

在卷积网络中，图像数据逐层变换。某一层的像素通过一个称为**滤波器**的局部函数，根据前一层附近像素的状态计算自身的值（见第 10.2 节）。以使用 $3\times3$ 滤波器的卷积层为例，如图 13.3(a) 所示。第 $l+1$ 层某个像素处的单个滤波器所做的计算可以写成

<!-- pdf-page: 430 -->

$$
z_i^{(l+1)}=f\!\left(\sum_j w_j z_j^{(l)}+b\right), \tag{13.8}
$$

其中 $f(\cdot)$ 是 ReLU 等可微的非线性激活函数；对 $j$ 的求和遍及第 $l$ 层一个小块中的全部九个像素。同一个函数应用于图像中的多个局部块，所以权重 $w_j$ 和偏置 $b$ 在这些块之间共享，也就没有下标 $i$。

就目前形式而言，式 (13.8) 对第 $l$ 层节点重排并不等变，因为由 $w_j$ 组成的权重向量并不对其元素的置换保持不变。不过，只需作简单修改就能得到等变性。先把滤波器看成图，如图 13.3(b) 所示，并将节点 $i$ 本身的贡献单独列出。其余八个节点是节点 $i$ 的邻居 $\mathcal N(i)$。再假定这些邻居共用一个权重参数 $w_{\mathrm{neigh}}$，得到

$$
z_i^{(l+1)}=f\!\left(w_{\mathrm{neigh}}\sum_{j\in\mathcal N(i)}z_j^{(l)}+w_{\mathrm{self}}z_i^{(l)}+b\right), \tag{13.9}
$$

其中节点 $i$ 自身有一个权重参数 $w_{\mathrm{self}}$。

式 (13.9) 可以理解为：邻居节点把消息传给节点 $i$，使它汇集邻居的信息并更新其局部表示 $z_i$。这里的消息只是其他节点的激活值。随后，来自邻居的消息与节点 $i$ 自身的信息结合，再经过非线性函数变换。式 (13.9) 以简单求和聚合邻居的信息，显然不受这些邻居标签的排列影响。而且，同一个操作同步应用于图中每个节点：若重排节点，计算本身不变，结果也随节点以同样方式重排，所以该计算对节点重排等变。这依赖于所有节点共享 $w_{\mathrm{neigh}}$、$w_{\mathrm{self}}$ 和 $b$。

### 13.2.2 图卷积网络

现在以卷积为模板，为图结构数据构造深层神经网络。目标是定义一个灵活的非线性节点嵌入变换：它对权重和偏置参数可微，并将第 $l$ 层的变量映射到第 $l+1$ 层对应的变量。对于图中每个节点 $n$ 和网络中的每一层 $l$，引入一个 $D$ 维节点嵌入列向量 $\mathbf h_n^{(l)}$，其中 $n=1,\ldots,N$，$l=1,\ldots,L$。

式 (13.9) 所示的变换先收集并合并邻居节点的信息，再根据

<!-- pdf-page: 431 -->

<!-- join-previous-paragraph -->
节点自身的当前嵌入和传入的消息更新该节点。因此，可以把每一层的处理视为连续的两个阶段：首先是**聚合**，每个节点接收邻居传来的消息，以不依赖节点排列的方式将它们合并成新向量 $\mathbf z_n^{(l)}$；随后是**更新**，把聚合后的邻居信息与该节点自己的局部信息结合，计算更新后的节点嵌入向量。

<figure id="algorithm-13-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/algorithm-13-1.png" alt="原书算法 13.1 的完整伪代码：对无向图逐层聚合邻居嵌入并更新节点嵌入">
  <figcaption>算法 13.1：简单的消息传递神经网络。下方给出图内伪代码的中文译文。</figcaption>
</figure>

**算法 13.1 的中文伪代码**

```text
输入：无向图 G=(V,E)
      初始节点嵌入
      {h_n^(0)=x_n}
      函数 Aggregate(·)
      函数 Update(·,·)
输出：最终节点嵌入 {h_n^(L)}
对 l=0,…,L−1，重复：
    z_n^(l) ← Aggregate(
        {h_m^(l): m∈N(n)})
    h_n^(l+1) ← Update(
        h_n^(l), z_n^(l))
返回 {h_n^(L)}
```

考虑图中的某个节点 $n$。先聚合其全部邻居的节点向量：

$$
\mathbf z_n^{(l)}=\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right). \tag{13.10}
$$

只要聚合函数能处理数量不定的邻居，而且不依赖这些邻居的顺序，其具体形式就可以很灵活。它也可以包含可学习参数，只要对这些参数可微，就能用梯度下降训练。

然后再通过另一个操作，更新节点 $n$ 的嵌入向量：

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l)}\right). \tag{13.11}
$$

这个操作同样可以是对一组可学习参数可微的函数。对图中每个节点并行执行聚合与更新，就构成网络的一层。节点嵌入通常用观测到的节点数据初始化，即 $\mathbf h_n^{(0)}=\mathbf x_n$。一般情况下，各层有各自独立的参数，也可以跨层共享参数。这一框架称为**消息传递神经网络**（message-passing neural network；Gilmer et al., 2017），算法 13.1 概括了它的流程。

<!-- pdf-page: 432 -->

### 13.2.3 聚合算子

$\operatorname{Aggregate}$ 函数可以有许多形式，但必须只依赖输入构成的集合，而不依赖输入顺序；若包含可学习参数，也必须对这些参数可微。根据式 (13.9)，最简单的聚合函数是求和：

$$
\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right)
=\sum_{m\in\mathcal N(n)}\mathbf h_m^{(l)}. \tag{13.12}
$$

简单求和显然不依赖邻居节点的顺序，而且无论邻居集合中有多少节点都有定义。它没有可学习参数。

求和使邻居较多的节点受到更强影响，而邻居较少的节点受到较弱影响；这可能引发数值问题，尤其是在社交网络等应用中，邻居集合大小可能相差几个数量级。一种变体是把聚合操作定义为邻居嵌入向量的平均值：

$$
\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right)
=\frac{1}{|\mathcal N(n)|}\sum_{m\in\mathcal N(n)}\mathbf h_m^{(l)}, \tag{13.13}
$$

其中 $|\mathcal N(n)|$ 是邻居集合 $\mathcal N(n)$ 中的节点数。不过，这种归一化也会丢弃网络结构的信息；可以证明，它的表达能力弱于简单求和（Hamilton, 2020）。因此，是否采用它，取决于节点特征与图结构各自有多重要。

另一种变体（Kipf and Welling, 2016）还考虑每个邻居节点自身的邻居数：

$$
\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right)
=\sum_{m\in\mathcal N(n)}\frac{\mathbf h_m^{(l)}}{\sqrt{|\mathcal N(n)|\,|\mathcal N(m)|}}. \tag{13.14}
$$

还可以逐元素取邻居嵌入向量的最大值或最小值。这种做法同样能处理数量不定的邻居，并且不依赖邻居顺序。

网络某一层中的每个节点都通过聚合前一层邻居的信息来更新，这定义了一个**感受野**，与 CNN 滤波器的感受野类似（见第 10 章）。随着信息经过连续的层，一个节点的更新会依赖于更早层中越来越多的其他节点；有效感受野最终可能覆盖整张图，如图 13.4 所示。不过，对于大型稀疏图，要让每个输出受到所有输入的影响，可能需要过多的层。因此，有些架构会额外引入一个直接连接原图所有节点的“超级节点”，

<!-- pdf-page: 433 -->

<!-- join-previous-paragraph -->
以确保信息能够快速传播。

<figure id="fig-13-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/fig-13-4.png" alt="图神经网络连续三层的节点与连边；红色节点显示第三层某个节点的有效感受野逐层扩张">
  <figcaption>图 13.4：信息在图神经网络连续各层之间流动的示意图。第三层有一个节点以红色突出显示；它接收前一层两个邻居的信息，而这两个邻居又接收第一层各自邻居的信息。与图像卷积网络一样，有效感受野对应的红色节点数随处理层数增加而增长。</figcaption>
</figure>

以上聚合算子都没有可学习参数。若先用一个多层神经网络 $\operatorname{MLP}_{\boldsymbol\phi}$ 分别变换各邻居的嵌入向量，再合并输出，就可以引入这样的参数；MLP 指“多层感知机”，$\boldsymbol\phi$ 表示其参数。只要该网络的结构和参数值在节点之间共享，这一聚合算子仍对置换保持不变。合并后的向量还可以用另一个参数为 $\boldsymbol\theta$ 的网络 $\operatorname{MLP}_{\boldsymbol\theta}$ 变换，得到整体聚合算子：

$$
\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right)
=\operatorname{MLP}_{\boldsymbol\theta}\!\left(\sum_{m\in\mathcal N(n)}\operatorname{MLP}_{\boldsymbol\phi}\!\left(\mathbf h_m^{(l)}\right)\right). \tag{13.15}
$$

其中 $\operatorname{MLP}_{\boldsymbol\phi}$ 和 $\operatorname{MLP}_{\boldsymbol\theta}$ 在第 $l$ 层的节点之间共享。由于 MLP 足够灵活，式 (13.15) 定义的变换可以作为从一组嵌入向量到单个嵌入向量的任意置换不变函数的通用逼近器（Zaheer et al., 2017）。求和也可以换成其他不变函数，例如平均值或逐元素最大值、最小值。

若图没有边，它就只是一个无结构的节点集合，构成图神经网络的一个特例。此时，对集合中每个向量 $\mathbf h_n^{(l)}$ 使用式 (13.15)，并对除 $\mathbf h_n^{(l)}$ 之外的全部其他向量求和，就得到一个学习无结构变量集合上的函数的通用框架，称为 **Deep Sets**。

<!-- pdf-page: 434 -->

### 13.2.4 更新算子

选定合适的聚合算子后，同样需要确定更新算子的形式。仿照 CNN 的式 (13.9)，一种简单形式为

$$
\operatorname{Update}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l)}\right)
=f\!\left(\mathbf W_{\mathrm{self}}\mathbf h_n^{(l)}+\mathbf W_{\mathrm{neigh}}\mathbf z_n^{(l)}+\mathbf b\right), \tag{13.16}
$$

其中 $f(\cdot)$ 是 ReLU 等非线性激活函数，逐元素作用于向量参数；$\mathbf W_{\mathrm{self}}$、$\mathbf W_{\mathrm{neigh}}$ 和 $\mathbf b$ 是可学习的权重与偏置，$\mathbf z_n^{(l)}$ 由聚合算子 (13.10) 定义。

若选用式 (13.12) 的简单求和作为聚合函数，并让节点自身与其邻居共享同一个权重矩阵，即 $\mathbf W_{\mathrm{self}}=\mathbf W_{\mathrm{neigh}}$，更新算子就有特别简单的形式：

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l)}\right)
=f\!\left(\mathbf W_{\mathrm{neigh}}\sum_{m\in\mathcal N(n),\,n}\mathbf h_m^{(l)}+\mathbf b\right). \tag{13.17}
$$

消息传递算法通常设 $\mathbf h_n^{(0)}=\mathbf x_n$ 作为初始化。但有时我们希望每个节点的内部表示向量维数高于或低于 $\mathbf x_n$。要提高维数，可以给节点向量 $\mathbf x_n$ 补零；也可以用可学习的线性变换，把节点向量映射到所需维数的空间。另一种初始化方式，特别适用于节点没有附带数据变量时，是使用独热向量表示每个节点的**度**，即邻居个数。

整体而言，图神经网络可表示为连续变换节点嵌入的一系列层。把节点嵌入组成矩阵 $\mathbf H$，其第 $n$ 行为 $\mathbf h_n^{\mathrm T}$，并用数据矩阵 $\mathbf X$ 初始化，就可以把逐层变换写为

$$
\begin{aligned}
\mathbf H^{(1)}&=\mathbf F\!\left(\mathbf X,\mathbf A,\mathbf W^{(1)}\right),\\
\mathbf H^{(2)}&=\mathbf F\!\left(\mathbf H^{(1)},\mathbf A,\mathbf W^{(2)}\right),\\
&\vdots\\
\mathbf H^{(L)}&=\mathbf F\!\left(\mathbf H^{(L-1)},\mathbf A,\mathbf W^{(L)}\right).
\end{aligned} \tag{13.18}
$$

其中 $\mathbf A$ 是邻接矩阵，$\mathbf W^{(l)}$ 表示网络第 $l$ 层的全部权重和偏置。对于置换矩阵 $\mathbf P$ 所定义的节点重排，第 $l$ 层计算的节点嵌入变换是等变的：

$$
\mathbf P\mathbf H^{(l)}=\mathbf F\!\left(\mathbf P\mathbf H^{(l-1)},\mathbf P\mathbf A\mathbf P^{\mathrm T},\mathbf W^{(l)}\right). \tag{13.19}
$$

因此，完整网络计算的变换也是等变的（习题 13.7）。

<!-- pdf-page: 435 -->

### 13.2.5 节点分类

图神经网络可以视为一系列层，每层把一组节点嵌入向量 $\{\mathbf h_n^{(l)}\}$ 变换为数量和维数相同的新向量组 $\{\mathbf h_n^{(l+1)}\}$。经过网络最后一个卷积层后，还须生成预测，才能定义训练用的代价函数，并用训练好的网络预测新数据。

先考虑图中节点的分类，这是图神经网络最常见的用途之一。可以定义一个输出层，有时称为**读出层**（readout layer），对每个节点计算 $C$ 类的 softmax：

$$
y_{ni}=\frac{\exp\!\left(\mathbf w_i^{\mathrm T}\mathbf h_n^{(L)}\right)}{\sum_j\exp\!\left(\mathbf w_j^{\mathrm T}\mathbf h_n^{(L)}\right)}, \tag{13.20}
$$

其中 $\{\mathbf w_i\}$ 是一组可学习的权重向量，$i=1,\ldots,C$。然后可将所有节点、所有类别的交叉熵损失相加，定义损失函数：

$$
\mathcal L=-\sum_{n\in V_{\mathrm{train}}}\sum_{i=1}^{C}y_{ni}^{t_{ni}}. \tag{13.21}
$$

**译注：** 原书式（13.21）将求和项印成 $y_{ni}^{t_{ni}}$，与前一句所称的交叉熵损失不符；按独热目标和式（13.20）的类别概率，训练节点上的常用交叉熵应为 $-\sum_{n\in V_{\mathrm{train}}}\sum_{i=1}^{C} t_{ni}\ln y_{ni}$。上式保留原书写法。

这里 $\{t_{ni}\}$ 是目标值，对每个 $n$ 采用独热编码。由于权重向量 $\{\mathbf w_i\}$ 在各输出节点间共享，输出 $y_{ni}$ 对节点顺序的置换等变，因此损失函数 (13.21) 不变。如果目标是预测连续输出值，可以用简单线性变换加平方和误差，定义适当的损失函数。

式 (13.21) 中对 $n$ 的求和只涉及训练用的节点子集 $V_{\mathrm{train}}$。可以区分以下三类节点：

1. **训练节点 $V_{\mathrm{train}}$** 有标签，参与图神经网络的消息传递，也用于计算训练损失函数。
2. **传导式节点 $V_{\mathrm{trans}}$** 可能存在，它们无标签，不参与训练损失的计算；但在训练与推理时仍参与消息传递，推理过程也可能预测其标签。
3. **归纳式节点 $V_{\mathrm{induct}}$** 是其余节点。它们不用于计算损失；在训练阶段，节点及其边都不参与消息传递。但在推理阶段，它们参与消息传递，其标签作为推理结果被预测。

<!-- pdf-page: 436 -->

如果没有传导式节点，测试节点及其边便无法在训练阶段使用；这种训练通常称为**归纳式学习**，可看作监督学习的一种形式。如果存在传导式节点，则称为**传导式学习**，可看作半监督学习的一种形式。

### 13.2.6 边分类

有些应用希望预测的是图的边，而非节点。边分类的一种常见任务是边补全，即判断两个节点之间是否应该有边。给定一组节点嵌入，可以对成对嵌入求点积，再通过 logistic sigmoid 函数定义节点 $n$ 与 $m$ 之间存在边的概率 $p(n,m)$：

$$
p(n,m)=\sigma\!\left(\mathbf h_n^{\mathrm T}\mathbf h_m\right). \tag{13.22}
$$

例如，可以预测社交网络中的两个人是否有共同兴趣，因而可能想要建立连接。

### 13.2.7 图分类

在一些图神经网络应用中，给定带标签图 $G_1,\ldots,G_N$ 的训练集，目标是预测新图的属性。这要求以不依赖节点任意顺序的方式合并最后一层的节点嵌入向量，保证输出预测对这一顺序不变。目标有点像聚合函数，只是这里要包括图中的全部节点，而非单个节点的邻居集合。最简单的做法是对节点嵌入向量求和：

$$
y=f\!\left(\sum_{n\in V}\mathbf h_n^{(L)}\right), \tag{13.23}
$$

其中 $f$ 可包含线性变换或神经网络等可学习参数。也可以使用其他不变的聚合函数，例如平均值或逐元素最小值、最大值。

分类问题通常使用交叉熵损失，例如判断候选药物分子有毒还是安全；回归问题通常使用平方误差损失，例如预测候选药物分子的溶解度。图级预测属于归纳式任务，因为训练和推理必须分别使用不同的图集合。

## 13.3 一般图网络

前述图网络有许多变体和扩展。这里概述几个关键概念及一些实践考量。

<!-- pdf-page: 437 -->

### 13.3.1 图注意力网络

注意力机制作为 Transformer 架构的基础时非常强大（见 12.1 节）；它也可用于图神经网络，构造聚合邻居消息的函数。传入的消息由注意力系数 $A_{nm}$ 加权：

$$
\mathbf z_n^{(l)}=\operatorname{Aggregate}\!\left(\left\{\mathbf h_m^{(l)}:m\in\mathcal N(n)\right\}\right)
=\sum_{m\in\mathcal N(n)}A_{nm}\mathbf h_m^{(l)}, \tag{13.24}
$$

其中注意力系数满足

$$
A_{nm}\geqslant0, \tag{13.25}
$$

$$
\sum_{m\in\mathcal N(n)}A_{nm}=1. \tag{13.26}
$$

这称为**图注意力网络**（graph attention network；Veličković et al., 2017）。它可以表达这样的归纳偏置：决定最佳更新时，有些邻居比另一些更重要，而且其重要性取决于数据本身。

注意力系数有多种构造方法，通常使用 softmax 函数。例如，可以采用双线性形式：

$$
A_{nm}=\frac{\exp\!\left(\mathbf h_n^{\mathrm T}\mathbf W\mathbf h_m\right)}{\sum_{m'\in\mathcal N(n)}\exp\!\left(\mathbf h_n^{\mathrm T}\mathbf W\mathbf h_{m'}\right)}, \tag{13.27}
$$

其中 $\mathbf W$ 是一个 $D\times D$ 的可学习参数矩阵。更一般的选择是使用神经网络，结合边两端节点的嵌入向量：

$$
A_{nm}=\frac{\exp\!\left\{\operatorname{MLP}(\mathbf h_n,\mathbf h_m)\right\}}{\sum_{m'\in\mathcal N(n)}\exp\!\left\{\operatorname{MLP}(\mathbf h_n,\mathbf h_{m'})\right\}}, \tag{13.28}
$$

其中 MLP 输出一个连续变量，且交换两个输入向量时其值不变。只要所有节点共享同一个 MLP，聚合函数就对节点重排等变（习题 13.8）。

图注意力网络还可以引入多个注意力头：对 $h=1,\ldots,H$，定义 $H$ 组不同的注意力权重 $A_{nm}^{(h)}$；每个头采用上述某种机制计算，并有自己的独立参数。聚合时，再把各头的结果连接起来并作线性投影（见 12.1.6 节）。注意，对全连接网络而言，多头图注意力网络就成为标准的 Transformer 编码器（习题 13.9）。

### 13.3.2 边嵌入

以上图神经网络使用与节点关联的嵌入向量。前面也看到，有些网络的边附带数据。即使边没有可观测值，

<!-- pdf-page: 438 -->

<!-- join-previous-paragraph -->
我们仍可以维护和更新基于边的隐藏变量，让它们参与图神经网络所学习的内部表示。

因此，除了节点嵌入 $\mathbf h_n^{(l)}$，再引入边嵌入 $\mathbf e_{nm}^{(l)}$，并定义一般的消息传递方程：

$$
\mathbf e_{nm}^{(l+1)}=\operatorname{Update}_{\mathrm{edge}}\!\left(\mathbf e_{nm}^{(l)},\mathbf h_n^{(l)},\mathbf h_m^{(l)}\right), \tag{13.29}
$$

$$
\mathbf z_n^{(l+1)}=\operatorname{Aggregate}_{\mathrm{node}}\!\left(\left\{\mathbf e_{nm}^{(l+1)}:m\in\mathcal N(n)\right\}\right), \tag{13.30}
$$

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}_{\mathrm{node}}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l+1)}\right). \tag{13.31}
$$

最后一层学习到的边嵌入 $\mathbf e_{nm}^{(L)}$ 可以直接用于边相关的预测。

### 13.3.3 图嵌入

除节点和边嵌入外，还可以维护并更新与整张图相关的嵌入向量 $\mathbf g^{(l)}$。把这些方面结合起来，就能为图结构应用定义更一般的消息传递函数，学习更丰富的表示。具体而言，可以定义以下一般消息传递方程（Battaglia et al., 2018）：

$$
\mathbf e_{nm}^{(l+1)}=\operatorname{Update}_{\mathrm{edge}}\!\left(\mathbf e_{nm}^{(l)},\mathbf h_n^{(l)},\mathbf h_m^{(l)},\mathbf g^{(l)}\right), \tag{13.32}
$$

$$
\mathbf z_n^{(l+1)}=\operatorname{Aggregate}_{\mathrm{node}}\!\left(\left\{\mathbf e_{nm}^{(l+1)}:m\in\mathcal N(n)\right\}\right), \tag{13.33}
$$

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}_{\mathrm{node}}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l+1)},\mathbf g^{(l)}\right), \tag{13.34}
$$

$$
\mathbf g^{(l+1)}=\operatorname{Update}_{\mathrm{graph}}\!\left(\mathbf g^{(l)},\left\{\mathbf h_n^{(l+1)}:n\in V\right\},\left\{\mathbf e_{nm}^{(l+1)}:(n,m)\in E\right\}\right). \tag{13.35}
$$

这些更新方程首先在式 (13.32) 中，根据边嵌入的上一层状态、边所连接的两个节点的嵌入，以及图级嵌入 $\mathbf g^{(l)}$，更新边嵌入 $\mathbf e_{nm}^{(l+1)}$。随后，式 (13.33) 聚合与每个节点相连的全部边的更新后嵌入，得到一组聚合向量。式 (13.34) 再根据节点原有嵌入、聚合向量和图级嵌入，更新节点嵌入 $\{\mathbf h_n^{(l+1)}\}$。最后，式 (13.35) 利用图中所有节点和边的信息，以及上一层的图级嵌入，更新图级嵌入。这些消息传递更新如图 13.5 所示，算法 13.2 给出总结。

### 13.3.4 过平滑

某些图神经网络有一个明显问题，称为**过平滑**（over-smoothing）：消息传递迭代若干次后，各节点的嵌入向量往往变得十分相似，实际上限制了网络深度。缓解这一问题的方法之一是加入残差连接，例如把更新算子 (13.34) 修改为（见 9.5 节）

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}_{\mathrm{node}}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l+1)},\mathbf g^{(l)}\right)+\mathbf h_n^{(l)}. \tag{13.36}
$$

<!-- pdf-page: 439 -->

<figure id="fig-13-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/fig-13-5.png" alt="一般图消息传递的三种更新：边更新、节点更新和全图更新；红色为当前更新变量，蓝色为参与该更新的变量">
  <figcaption>图 13.5：式 (13.32)–(13.35) 所定义的一般图消息传递更新：（a）边更新；（b）节点更新；（c）全局图更新。每幅图中，红色表示正在更新的变量，红色和蓝色变量共同参与该更新。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf h_n$、$\mathbf h_m$ 表示节点嵌入；$\mathbf e_{nm}$ 表示边嵌入；$\mathbf g$ 表示全图嵌入。</p>
</figure>

缓解过平滑影响的另一种做法，是让输出层从网络此前的所有层获取信息，而不只使用最后一个卷积层。例如，可以把此前各层的表示连接起来：

$$
\mathbf y_n=f\!\left(\mathbf h_n^{(1)}\oplus\mathbf h_n^{(2)}\oplus\cdots\oplus\mathbf h_n^{(L)}\right), \tag{13.37}
$$

其中 $\mathbf a\oplus\mathbf b$ 表示向量 $\mathbf a$ 与 $\mathbf b$ 的连接。另一种变体用最大池化代替连接，此时输出向量的每个元素，是此前各层嵌入向量对应元素的最大值。

### 13.3.5 正则化

图神经网络可以使用标准的正则化技术（见第 9 章），包括在损失函数中加入参数平方和等惩罚项。此外，还发展了一些专门针对图神经网络的正则化方法。

图神经网络已经通过权重共享实现置换等变性和不变性，但通常各层有独立的参数。权重和偏置也可以跨层共享，从而减少独立参数的数量。

图神经网络中的 dropout，是在训练时随机省略图中一部分节点，并在每次前向传递时重新随机选择。也可以将其用于图中的边：训练时随机选出邻接矩阵的一部分元素，删除或遮盖对应的边。

<!-- pdf-page: 440 -->

<figure id="algorithm-13-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-13/algorithm-13-2.png" alt="原书算法 13.2 的完整伪代码：联合更新边、节点与整张图的嵌入">
  <figcaption>算法 13.2：同时包含节点、边和图嵌入的图神经网络。下方给出图内伪代码的中文译文。</figcaption>
</figure>

**算法 13.2 的中文伪代码**

```text
输入：无向图 G=(V,E)
      初始节点嵌入
      {h_n^(0)}
      初始边嵌入
      {e_nm^(0)}
      初始图嵌入 g^(0)
输出：最终节点嵌入
      {h_n^(L)}
      最终边嵌入
      {e_nm^(L)}
      最终图嵌入
      g^(L)
对 l=0,…,L−1，重复：
    e_nm^(l+1) ← Update_edge(
        e_nm^(l), h_n^(l),
        h_m^(l), g^(l))
    z_n^(l+1) ←
        Aggregate_node(
        {e_nm^(l+1):
         m∈N(n)})
    h_n^(l+1) ← Update_node(
        h_n^(l),
        z_n^(l+1), g^(l))
    g^(l+1) ← Update_graph(
        g^(l), {h_n^(l+1)},
        {e_nm^(l+1)})
返回：
    {h_n^(L)}, {e_nm^(L)},
    g^(L)
```

### 13.3.6 几何深度学习

前面看到，设计图结构数据的深度学习模型时，置换对称性是一个关键考量。它提供一种归纳偏置，显著降低数据需求，同时提高预测性能。对图形网格、流体模拟、分子结构等涉及空间性质的图神经网络应用，还可以把其他等变性和不变性纳入网络架构。

以预测分子属性为例，例如探索候选药物空间。一个分子可以表示为一系列给定种类的原子（碳、氢、氮等），以及各原子的空间坐标；坐标写成三维列向量。可以为每个原子 $n$、每一层 $l$ 引入相应的嵌入向量 $\mathbf r_n^{(l)}$，并用已知原子坐标初始化。不过，这些向量的元素值取决于任意选取的坐标系，分子的属性却并非如此。例如，分子在空间中旋转、相对坐标原点平移到新位置，或者反射坐标系而得到分子的镜像版本，其溶解度都不改变。分子的

<!-- pdf-page: 441 -->

<!-- join-previous-paragraph -->
性质因此应对这些变换保持不变。

只要谨慎选择更新与聚合操作的函数形式（Satorras, Hoogeboom, and Welling, 2021），就能把新嵌入 $\mathbf r_n^{(l)}$ 纳入图神经网络的更新方程 (13.29)–(13.31)，实现所需的对称性质：

$$
\mathbf e_{nm}^{(l+1)}=\operatorname{Update}_{\mathrm{edge}}\!\left(\mathbf e_{nm}^{(l)},\mathbf h_n^{(l)},\mathbf h_m^{(l)},\left\|\mathbf r_n^{(l)}-\mathbf r_m^{(l)}\right\|^2\right), \tag{13.38}
$$

$$
\mathbf r_n^{(l+1)}=\mathbf r_n^{(l)}+C\sum_{(n,m)\in E}\left(\mathbf r_n^{(l)}-\mathbf r_m^{(l)}\right)\phi\!\left(\mathbf e_{nm}^{(l+1)}\right), \tag{13.39}
$$

$$
\mathbf z_n^{(l+1)}=\operatorname{Aggregate}_{\mathrm{node}}\!\left(\left\{\mathbf e_{nm}^{(l+1)}:m\in\mathcal N(n)\right\}\right), \tag{13.40}
$$

$$
\mathbf h_n^{(l+1)}=\operatorname{Update}_{\mathrm{node}}\!\left(\mathbf h_n^{(l)},\mathbf z_n^{(l+1)}\right). \tag{13.41}
$$

注意，$\|\mathbf r_n^{(l)}-\mathbf r_m^{(l)}\|^2$ 是坐标 $\mathbf r_n^{(l)}$ 和 $\mathbf r_m^{(l)}$ 之间距离的平方；它不依赖于平移、旋转或反射。坐标 $\mathbf r_n^{(l)}$ 也通过相对差 $\mathbf r_n^{(l)}-\mathbf r_m^{(l)}$ 的线性组合来更新。这里 $\phi(\mathbf e_{nm}^{(l+1)})$ 是边嵌入的一般标量函数，由神经网络表示；系数 $C$ 通常取求和项数的倒数。由此，这些变换下式 (13.38)、(13.40)、(13.41) 中的消息保持不变，而式 (13.39) 给出的坐标嵌入保持等变（习题 13.10）。

前面见到了结构化数据中的许多对称性：图像中物体的平移、图中节点顺序的置换，以及分子在三维空间中的旋转和平移。把这些对称性写进深层神经网络结构，是一种有力的归纳偏置，也是**几何深度学习**（geometric deep learning）这一丰富研究领域的基础（Bronstein et al., 2017；Bronstein et al., 2021）。

## 习题

### 13.1（★）

证明：图 13.2 两种节点顺序之间的置换 $(A,B,C,D,E)\to(C,E,A,D,B)$，可以写成式 (13.5) 的形式，其中置换矩阵由式 (13.1) 给出。

### 13.2（★★）

设 $\mathbf A$ 是图的邻接矩阵。证明：每个节点连接的边数由矩阵 $\mathbf A^2$ 对应的对角元素给出。

### 13.3（★）

画出邻接矩阵如下的图：

$$
\mathbf A=\begin{pmatrix}
0&1&1&0&1\\
1&0&1&1&1\\
1&1&0&1&0\\
0&1&1&0&0\\
1&1&0&0&0
\end{pmatrix}. \tag{13.42}
$$

<!-- pdf-page: 442 -->

### 13.4（★★）

证明：用式 (13.3) 定义的置换矩阵 $\mathbf P$ 左乘数据矩阵 $\mathbf X$，将得到式 (13.4) 的新数据矩阵 $\widetilde{\mathbf X}$，其各行按照置换函数 $\pi(\cdot)$ 重排。

### 13.5（★★）

证明：式 (13.5) 定义的变换后邻接矩阵 $\widetilde{\mathbf A}$，在 $\mathbf P$ 由式 (13.3) 定义时，相对于原邻接矩阵 $\mathbf A$，其行和列都按照置换函数 $\pi(\cdot)$ 重排。

### 13.6（★★）

本题把更新方程 (13.16) 写成图级矩阵方程。为使记号简洁，略去层下标 $l$。先把节点嵌入向量 $\{\mathbf h_n\}$ 合并为 $N\times D$ 矩阵 $\mathbf H$，其中第 $n$ 行为 $\mathbf h_n^{\mathrm T}$。然后证明，邻居聚合向量 $\mathbf z_n$ 满足

$$
\mathbf z_n=\sum_{m\in\mathcal N(n)}\mathbf h_m, \tag{13.43}
$$

并可写成矩阵形式 $\mathbf Z=\mathbf A\mathbf H$，其中 $\mathbf Z$ 为 $N\times D$ 矩阵，第 $n$ 行是 $\mathbf z_n^{\mathrm T}$，$\mathbf A$ 为邻接矩阵。最后证明，式 (13.16) 中非线性激活函数的参数可以写成矩阵形式

$$
\mathbf A\mathbf H\mathbf W_{\mathrm{neigh}}+\mathbf H\mathbf W_{\mathrm{self}}+\mathbf 1_D\mathbf b^{\mathrm T}, \tag{13.44}
$$

其中 $\mathbf 1_D$ 是各元素均为 1 的 $D$ 维列向量。

**译注：** 原书把 $\mathbf H$、$\mathbf Z$ 定义为 $N\times D$，却把式（13.44）的全 1 列向量写成 $D$ 维；要与该矩阵相加，其维数应为 $N$。此外，式（13.16）以列向量写 $\mathbf W\mathbf h_n$，改成以 $\mathbf h_n^{\mathrm T}$ 为行的矩阵形式时，权重矩阵通常还需要转置。上式保留原书记号。

### 13.7（★★）

利用深层图卷积网络第 $l$ 层的等变性质 (13.19)，以及节点变量的置换性质 (13.4)，证明式 (13.18) 定义的完整深层图卷积网络也等变。

### 13.8（★★）

说明：式 (13.24) 定义的聚合函数在注意力权重由式 (13.28) 给出时，为什么对图中节点的重排等变。

### 13.9（★）

证明：如果图为全连接，即任意两个节点之间都有边，图注意力网络就等价于标准 Transformer 架构。

### 13.10（★★）

坐标系平移时，由该坐标系定义的物体位置按下式变换：

$$
\widetilde{\mathbf r}=\mathbf r+\mathbf c, \tag{13.45}
$$

其中 $\mathbf c$ 是表示平移的固定向量。类似地，如果坐标系旋转和／或镜像反射，物体位置向量按下式变换：

$$
\widetilde{\mathbf r}=\mathbf R\mathbf r, \tag{13.46}
$$

其中 $\mathbf R$ 是正交矩阵，其逆为转置，因而

$$
\mathbf R\mathbf R^{\mathrm T}=\mathbf R^{\mathrm T}\mathbf R=\mathbf I. \tag{13.47}
$$

<!-- pdf-page: 443 -->

利用这些性质，证明在平移、旋转和反射下，式 (13.38)、(13.40)、(13.41) 中的消息保持不变，而式 (13.39) 的坐标嵌入保持等变。
