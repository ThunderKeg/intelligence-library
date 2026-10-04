<!-- pdf-page: 52 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-17.png" alt="九阶多项式的贝叶斯预测分布，红线为均值，红色区域为均值上下一个标准差"><figcaption>图 1.17：对多项式曲线拟合进行贝叶斯处理所得到的预测分布。这里使用 $M=9$ 的多项式，固定参数为 $\alpha=5\times10^{-3}$、$\beta=11.1$（对应于已知的噪声方差）。红色曲线表示预测分布的均值，红色区域表示均值上下 $\pm1$ 个标准差的范围。</figcaption><p class="figure-translation">图中 $x$、$t$ 为变量符号。</p></figure>

## 1.3 模型选择

在用最小二乘法进行多项式曲线拟合的例子中，我们看到，存在一个能带来最佳泛化性能的最优多项式阶数。多项式阶数控制着模型中自由参数的数目，因而决定了模型的复杂度。对于带正则化的最小二乘法，正则化系数 $\lambda$ 也控制着模型的有效复杂度；而对于混合分布、神经网络等更复杂的模型，可能有多个参数共同决定复杂度。在实际应用中，我们需要确定这些参数的取值，而这样做的主要目的通常是在新数据上获得最佳预测性能。此外，除了为某个给定模型寻找合适的复杂度参数值，我们还可能希望考虑多种不同类型的模型，从中找出最适合特定应用的一个。

我们已经看到，在最大似然方法中，由于存在过拟合问题，训练集上的表现并不能很好地反映模型对未见数据的预测性能。如果数据充足，一种做法是用现有数据的一部分来训练一系列模型，或者以一系列复杂度参数值来训练某个给定模型，然后在独立的数据上比较它们，选择预测性能最好的一个。这些独立数据有时称为*验证集*（validation set）。如果在一个大小有限的数据集上反复调整模型设计，也可能对验证数据产生一定程度的过拟合，因此可能还需要另外保留第三个数据集，即*测试集*（test set），用于最终评估选定模型的性能。

然而，在许多应用中，可用于训练和测试的数据有限。为了建立好的模型，我们希望尽可能多地使用现有数据进行训练。但是，验证集如果很小，对预测性能的估计就会有较大的随机波动。解决这一矛盾的一种方法是*交叉验证*（cross-validation），如图 1.18 所示。它允许使用现有数据中 $(S-1)/S$ 的部分进行训练，同时利用全部

<!-- pdf-page: 53 -->
<!-- join-previous-paragraph -->
数据来评估性能。当数据特别稀缺时，可以考虑 $S=N$ 的情形，其中 $N$ 为数据点总数，这就得到了*留一法*（leave-one-out）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-18.png" alt="四折交叉验证中依次保留四组数据作为验证组的示意图"><figcaption>图 1.18：$S$ 折交叉验证方法，这里以 $S=4$ 为例。将现有数据划分为 $S$ 组（最简单的情况是各组大小相等），然后用其中的 $S-1$ 组训练一组模型，并在剩下的一组上评估这些模型。对保留组的全部 $S$ 种可能选择重复这一过程，图中以红色方块表示保留组，最后将这 $S$ 次运行的性能得分取平均。</figcaption><p class="figure-translation">run 1 → 第 1 次运行；run 2 → 第 2 次运行；run 3 → 第 3 次运行；run 4 → 第 4 次运行。</p></figure>

交叉验证的一个主要缺点是，所需的训练次数增加到原来的 $S$ 倍；对于训练本身计算代价就很高的模型，这可能成为问题。交叉验证这类使用独立数据评估性能的方法还有一个问题：单个模型可能有多个复杂度参数（例如，可能有多个正则化参数）。在最坏情况下，考察这些参数的取值组合，所需的训练次数可能随参数个数呈指数增长。显然，我们需要更好的方法。理想的方法应当只依赖训练数据，并能在一次训练中比较多个超参数以及不同的模型类型。因此，我们需要找到一种只依赖训练数据、同时不会因过拟合而产生偏差的性能度量。

历史上，人们提出过各种“信息准则”，试图通过加入惩罚项来弥补复杂模型的过拟合，从而纠正最大似然的偏差。例如，*赤池信息准则*（Akaike information criterion，AIC；Akaike，1974）选择使下式最大的模型：

$$
\ln p(\mathcal{D}\mid\mathbf{w}_{\mathrm{ML}})-M.
\tag{1.73}
$$

这里，$p(\mathcal{D}\mid\mathbf{w}_{\mathrm{ML}})$ 是最佳拟合时的对数似然，$M$ 为模型中可调参数的数目。这个量的一个变体称为*贝叶斯信息准则*（Bayesian information criterion，BIC），将在第 4.4.1 节讨论。不过，这类准则没有考虑模型参数的不确定性，在实践中往往倾向于选择过于简单的模型。因此，第 3.4 节将转向完全贝叶斯的方法，在那里我们会看到，复杂度惩罚如何以自然且有理论依据的方式产生。

## 1.4 维数灾难

在多项式曲线拟合的例子中，我们只有一个输入变量 $x$。然而，在模式识别的实际应用中，我们必须处理由许多输入变量构成的

<!-- pdf-page: 54 -->
<!-- join-previous-paragraph -->
高维空间。正如下文将讨论的，这会带来一些严峻的挑战，也是影响模式识别技术设计的一个重要因素。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-19.png" alt="油流数据的两个输入变量散点图，红绿蓝分别表示三种流型，叉号表示待分类测试点"><figcaption>图 1.19：油流数据在输入变量 $x_6$ 和 $x_7$ 上的散点图。红色表示“均匀流”（homogenous）类，绿色表示“环状流”（annular）类，蓝色表示“层状流”（laminar）类。我们的目标是对“$\times$”标记的新测试点进行分类。</figcaption><p class="figure-translation">$x_6$、$x_7$ 为输入变量符号；“$\times$”表示新测试点。</p></figure>

为了说明这一问题，我们考虑一个合成数据集，它模拟了对含有油、水和气体混合物的管道所做的测量（Bishop and James，1993）。这三种物质在管内可以形成三种不同的几何分布，分别称为“均匀流”（homogenous）、“环状流”（annular）和“层状流”（laminar）；三种物质所占的比例也可以变化。每个数据点都是一个 12 维输入向量，其分量来自伽马射线密度计的测量。这些仪器测量以窄束穿过管道的伽马射线的衰减。附录 A 详细介绍了这个数据集。图 1.19 展示了其中的 100 个点，只画出了 $x_6$ 和 $x_7$ 这两个测量值（为了便于说明，忽略其余十个输入值）。每个数据点都标有它所属的三种几何流型类别之一。我们的目标是用这些数据作为训练集，以便对新的观测 $(x_6,x_7)$ 进行分类，例如图 1.19 中以叉号标出的观测。我们看到，叉号周围有许多红点，因此可能认为它属于红色类别。但是，附近也有不少绿点，所以也可能认为它属于绿色类别。它似乎不大可能属于蓝色类别。这里的直觉是：与距离较远的点相比，训练集中附近的点应当对叉号的类别判断产生更强的影响。事实上，这一直觉是合理的，后续章节将更详细地讨论它。

如何把这一直觉转化为学习算法呢？一种非常简单的办法是把输入空间划分成规则的单元格，如图 1.20 所示。当给定一个测试点并希望预测其类别时，先确定它落在哪个单元格中，然后找出落在

<!-- pdf-page: 55 -->
<!-- join-previous-paragraph -->
同一单元格内的全部训练数据点。将测试点预测为该单元格中训练点数量最多的那个类别（如果并列，则随机打破平局）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-20.png" alt="将油流数据输入空间划为规则单元格并按格中多数类别分类"><figcaption>图 1.20：一种简单的分类方法：把输入空间划分为单元格，并把任何新的测试点归入与它同格且样本数量占多数的类别。我们很快就会看到，这种过于简单的办法存在一些严重的缺点。</figcaption><p class="figure-translation">$x_6$、$x_7$ 为输入变量符号。</p></figure>

这种朴素方法存在很多问题，其中一个最严重的问题，在将它推广到输入变量更多、也就是输入空间维数更高的情形时就会显现出来。图 1.21 说明了问题的根源：如果将空间中的一个区域划分为规则的单元格，那么单元格数量将随空间维数呈指数增长。单元格数量呈指数级增加的困难在于：为了确保这些单元格不是空的，我们也需要指数级增加的训练数据量。显然，当变量数目超过少数几个时，这种方法就不可能适用了，因此需要寻找更精细的方法。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-21.png" alt="一维、二维、三维规则网格的单元格数量随维数增长的示意图"><figcaption>图 1.21：维数灾难示意图。规则网格中的区域数量随空间维数 $D$ 呈指数增长。为使图示清楚，$D=3$ 时只画出了部分立方体区域。</figcaption><p class="figure-translation">$D=1$、$D=2$、$D=3$ 分别表示一维、二维和三维；$x_1$、$x_2$、$x_3$ 为坐标变量。</p></figure>

我们还可以回到多项式曲线拟合的例子（第 1.1 节），考虑如何将该方法

<!-- pdf-page: 56 -->
<!-- join-previous-paragraph -->
推广到包含多个变量的输入空间，从而进一步理解高维空间的问题。如果有 $D$ 个输入变量，那么最高三阶的一般多项式具有如下形式：

$$
y(\mathbf{x},\mathbf{w})=w_0+\sum_{i=1}^{D}w_i x_i+\sum_{i=1}^{D}\sum_{j=1}^{D}w_{ij}x_i x_j+\sum_{i=1}^{D}\sum_{j=1}^{D}\sum_{k=1}^{D}w_{ijk}x_i x_j x_k.
\tag{1.74}
$$

随着 $D$ 增加，独立系数的数目将按 $D^3$ 的比例增长（由于各个 $x$ 变量之间存在交换对称性，并不是所有系数都独立）。实际中，为了刻画数据中复杂的依赖关系，我们可能需要使用更高阶的多项式。对于 $M$ 阶多项式，系数数目的增长量级为 $D^M$（习题 1.16）。虽然这时是幂律增长而不是指数增长，但仍然意味着，这种方法很快就会变得难以处理，实际用途也很有限。

我们一生都生活在三维空间中，由此形成的几何直觉在更高维的空间里可能会严重失效。一个简单的例子是：考虑 $D$ 维空间中半径 $r=1$ 的球，问球内半径介于 $r=1-\epsilon$ 与 $r=1$ 之间的部分占整个球体积的多少。注意到 $D$ 维空间中半径为 $r$ 的球的体积必定按 $r^D$ 缩放，就可以计算这个比例。于是写成

$$
V_D(r)=K_Dr^D
\tag{1.75}
$$

其中常数 $K_D$ 只依赖于 $D$（习题 1.18）。因此，所求比例为

$$
\frac{V_D(1)-V_D(1-\epsilon)}{V_D(1)}=1-(1-\epsilon)^D.
\tag{1.76}
$$

图 1.22 对不同的 $D$ 值画出了这个比例随 $\epsilon$ 的变化。可以看到，当 $D$ 很大时，即使 $\epsilon$ 很小，这个比例也趋近于 1。因此，在高维空间中，球的大部分体积集中在靠近表面的一个薄壳里！

再举一个与模式识别直接相关的例子：考虑高维空间中高斯分布的表现。如果从笛卡尔坐标变换到极坐标，再将方向变量积分消去，就能得到以距原点的半径 $r$ 为自变量的密度 $p(r)$（习题 1.20）。因此，$p(r)\delta r$ 就是位于半径 $r$ 处、厚度为 $\delta r$ 的薄壳内的概率质量。图 1.23 对不同的 $D$ 值画出了这一分布。可以看到，当 $D$ 很大时，高斯分布的概率质量也集中在一个薄壳中。

在多维空间中可能出现的这些严重困难，有时被称为*维数灾难*（curse of dimensionality；Bellman，1961）。本书会大量使用一维或二维输入空间的例子，因为这样特别容易用图形说明各种方法。不过，读者需要留意：在低维空间中形成的直觉，并不都能推广到多维空间。

<!-- pdf-page: 57 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-22.png" alt="不同维数下单位球在表面薄壳中的体积占比"><figcaption>图 1.22：对于不同的维数 $D$，球内从 $r=1-\epsilon$ 到 $r=1$ 范围所占的体积比例。</figcaption><p class="figure-translation">volume fraction → 体积比例；$\epsilon$ 为壳层厚度；曲线标签 $D=1,2,5,20$ 表示维数。</p></figure>

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-23.png" alt="不同维数的高斯分布关于半径的概率密度"><figcaption>图 1.23：对于不同的维数 $D$，高斯分布关于半径 $r$ 的概率密度。在高维空间中，高斯分布的大部分概率质量位于某一特定半径处的薄壳内。</figcaption><p class="figure-translation">$r$ 为半径，$p(r)$ 为关于半径的概率密度；$D=1,2,20$ 表示维数。</p></figure>

尽管维数灾难确实给模式识别应用带来了重要问题，但它并不妨碍我们找到适用于高维空间的有效技术。这有两方面原因。首先，真实数据通常局限于空间中有效维数较低的某个区域，特别是，目标变量发生重要变化的方向也可能受限于这样的区域。其次，真实数据通常具有某种平滑性（至少在局部如此），也就是说，在大多数情况下，输入变量的小变化会引起目标变量的小变化，因此可以利用类似局部插值的方法，预测新输入值所对应的目标变量。成功的模式识别技术利用了其中一种或两种性质。例如，考虑制造业中的一个应用：对传送带上相同的平面物体拍摄图像，目标是确定物体的朝向。每幅图像都是

<!-- pdf-page: 58 -->
<!-- join-previous-paragraph -->
高维空间中的一个点，空间的维数由像素数目决定。由于物体在图像中的位置和朝向都可能不同，图像之间的变化具有三个自由度，因此，这组图像位于嵌入高维空间的一个三维*流形*（manifold）上。物体的位置或朝向与像素强度之间的关系很复杂，所以这个流形具有很强的非线性。如果目标是学习一个模型，输入图像后输出物体的朝向，而不受位置影响，那么流形内的变化只有一个自由度是有意义的。

## 1.5 决策论

第 1.2 节介绍了概率论如何为不确定性的量化与处理提供一致的数学框架。现在转向讨论决策论。决策论与概率论结合，使我们能够在包含不确定性的情形下作出最优决策，模式识别中遇到的情况正是如此。

设有输入向量 $\mathbf{x}$ 及其对应的目标变量向量 $\mathbf{t}$，我们的目标是：给定一个新的 $\mathbf{x}$ 值，预测 $\mathbf{t}$。对于回归问题，$\mathbf{t}$ 由连续变量组成；对于分类问题，$\mathbf{t}$ 表示类别标签。联合概率分布 $p(\mathbf{x},\mathbf{t})$ 完整地描述了这些变量的不确定性。根据一组训练数据确定 $p(\mathbf{x},\mathbf{t})$，是*推断*（inference）的一个例子。它通常是一个非常困难的问题，本书相当大一部分内容都围绕其求解展开。但在实际应用中，我们往往必须对 $\mathbf{t}$ 的值作出具体预测，或者更一般地，根据对 $\mathbf{t}$ 可能取值的认识采取某个具体行动。这一方面的问题就是决策论的研究内容。

例如，考虑一个医学诊断问题：我们已经拍摄了一名患者的 X 射线图像，希望判断患者是否患有癌症。这里，输入向量 $\mathbf{x}$ 是图像中各像素的强度集合，输出变量 $t$ 则表示患有癌症（记为类别 $\mathcal{C}_1$）或未患癌症（记为类别 $\mathcal{C}_2$）。例如，可以让 $t$ 是二元变量，令 $t=0$ 对应类别 $\mathcal{C}_1$，$t=1$ 对应类别 $\mathcal{C}_2$。后面将会看到，这样选择标签值，对概率模型特别方便。一般的推断问题就是确定联合分布 $p(\mathbf{x},\mathcal{C}_k)$，或者等价地确定 $p(\mathbf{x},t)$；这给出了关于当前情形最完整的概率描述。虽然这个量非常有用，也包含丰富的信息，但最终我们仍必须决定是否对患者进行治疗，并且希望这一选择在某种合适的意义下是最优的（Duda and Hart，1973）。这就是*决策*步骤。决策论要回答的是：在已知相关概率的条件下，如何作出最优决策。我们将会看到，一旦解决推断问题，决策阶段通常非常简单，甚至不费什么力气。

这里介绍本书后续内容所需的决策论核心概念。

<!-- pdf-page: 59 -->
<!-- join-previous-paragraph -->
更多背景知识以及更详细的论述，可参见 Berger（1985）和 Bather（2000）。

在详细分析之前，先直观地考虑一下，概率可能怎样参与决策。当得到一名新患者的 X 射线图像 $\mathbf{x}$ 时，我们要决定将图像归入哪一类。我们关心的是给定图像后两个类别的概率，即 $p(\mathcal{C}_k\mid\mathbf{x})$。根据贝叶斯定理，这些概率可以写为

$$
p(\mathcal{C}_k\mid\mathbf{x})=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{p(\mathbf{x})}.
\tag{1.77}
$$

注意，贝叶斯定理中的任何一个量，都可以从联合分布 $p(\mathbf{x},\mathcal{C}_k)$ 出发，对适当的变量进行边缘化或条件化而得到。现在可以把 $p(\mathcal{C}_k)$ 解释为类别 $\mathcal{C}_k$ 的先验概率，把 $p(\mathcal{C}_k\mid\mathbf{x})$ 解释为相应的后验概率。因此，$p(\mathcal{C}_1)$ 表示在拍摄 X 射线图像之前，一个人患癌症的概率；类似地，$p(\mathcal{C}_1\mid\mathbf{x})$ 则是在获得 X 射线图像所含信息之后，用贝叶斯定理修正后的相应概率。如果目标是尽量降低把 $\mathbf{x}$ 分错类别的可能性，那么直觉上应当选择后验概率较大的类别。下面将证明这一直觉是正确的，并讨论更一般的决策准则。

### 1.5.1 最小化误分类率

假设我们的目标仅仅是尽可能少地分错类别。我们需要一个规则，把每个 $\mathbf{x}$ 值分配给现有类别中的一个。这样的规则将输入空间划分成称为*决策区域*（decision region）的区域 $\mathcal{R}_k$，每个类别对应一个区域，$\mathcal{R}_k$ 中的所有点都被归入类别 $\mathcal{C}_k$。决策区域之间的边界称为*决策边界*（decision boundary），也称*决策面*（decision surface）。注意，每个决策区域不一定连通，也可以由若干互不相连的区域组成。后续章节会给出决策边界和决策区域的例子。为了找出最优决策规则，先考虑只有两个类别的情形，例如上述癌症诊断问题。当属于类别 $\mathcal{C}_1$ 的输入向量被归入类别 $\mathcal{C}_2$，或反过来时，就发生了错误。发生这种错误的概率为

$$
\begin{aligned}
p(\mathrm{mistake})
&=p(\mathbf{x}\in\mathcal{R}_1,\mathcal{C}_2)+p(\mathbf{x}\in\mathcal{R}_2,\mathcal{C}_1)\\
&=\int_{\mathcal{R}_1}p(\mathbf{x},\mathcal{C}_2)\,\mathrm{d}\mathbf{x}+\int_{\mathcal{R}_2}p(\mathbf{x},\mathcal{C}_1)\,\mathrm{d}\mathbf{x}.
\end{aligned}
\tag{1.78}
$$

我们可以自由选择决策规则，将每个点 $\mathbf{x}$ 归入两个类别之一。显然，为了最小化 $p(\mathrm{mistake})$，应当选择使式（1.78）中相应被积函数较小的类别。因此，如果对于给定的 $\mathbf{x}$ 有 $p(\mathbf{x},\mathcal{C}_1)>p(\mathbf{x},\mathcal{C}_2)$，就应当把该 $\mathbf{x}$ 归入类别 $\mathcal{C}_1$。根据概率的乘积法则，有 $p(\mathbf{x},\mathcal{C}_k)=p(\mathcal{C}_k\mid\mathbf{x})p(\mathbf{x})$。因子 $p(\mathbf{x})$ 对两项都相同，所以这个结果还可以表述为：

<!-- pdf-page: 60 -->
<!-- join-previous-paragraph -->
将每个 $\mathbf{x}$ 归入后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 最大的类别，就能使犯错概率最小。图 1.24 用两个类别、一个输入变量 $x$ 的情形说明了这一结果。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-24.png" alt="两个类别联合概率曲线和决策边界，彩色面积表示误分类概率"><figcaption>图 1.24：两个类别的联合概率 $p(x,\mathcal{C}_k)$ 随 $x$ 变化的示意图，以及决策边界 $x=\widehat{x}$。$x\geqslant\widehat{x}$ 的点被归入类别 $\mathcal{C}_2$，因而属于决策区域 $\mathcal{R}_2$；$x<\widehat{x}$ 的点被归入 $\mathcal{C}_1$，属于 $\mathcal{R}_1$。错误来自蓝色、绿色和红色区域：对于 $x<\widehat{x}$，错误是将类别 $\mathcal{C}_2$ 的点误判为 $\mathcal{C}_1$（由红色与绿色区域之和表示）；反过来，对于 $x\geqslant\widehat{x}$，错误是将类别 $\mathcal{C}_1$ 的点误判为 $\mathcal{C}_2$（由蓝色区域表示）。改变决策边界的位置 $\widehat{x}$ 时，蓝色与绿色区域的面积之和保持不变，而红色区域的大小会变化。$\widehat{x}$ 的最优位置是曲线 $p(x,\mathcal{C}_1)$ 与 $p(x,\mathcal{C}_2)$ 的交点，即 $\widehat{x}=x_0$，因为此时红色区域消失。这等价于最小误分类率决策规则：将每个 $x$ 归入后验概率 $p(\mathcal{C}_k\mid x)$ 较大的类别。</figcaption><p class="figure-translation">$p(x,\mathcal{C}_1)$、$p(x,\mathcal{C}_2)$ 为两类联合概率；$\mathcal{R}_1$、$\mathcal{R}_2$ 为决策区域；$\widehat{x}$ 为当前边界，$x_0$ 为两条曲线的交点位置。</p></figure>

对于有 $K$ 个类别的更一般情形，转而最大化分类正确的概率会稍微方便一些。该概率为

$$
\begin{aligned}
p(\mathrm{correct})
&=\sum_{k=1}^{K}p(\mathbf{x}\in\mathcal{R}_k,\mathcal{C}_k)\\
&=\sum_{k=1}^{K}\int_{\mathcal{R}_k}p(\mathbf{x},\mathcal{C}_k)\,\mathrm{d}\mathbf{x}.
\end{aligned}
\tag{1.79}
$$

如果选择区域 $\mathcal{R}_k$，使每个 $\mathbf{x}$ 都被归入 $p(\mathbf{x},\mathcal{C}_k)$ 最大的类别，那么这个概率就达到最大。再次使用乘积法则 $p(\mathbf{x},\mathcal{C}_k)=p(\mathcal{C}_k\mid\mathbf{x})p(\mathbf{x})$，并注意各项都具有共同因子 $p(\mathbf{x})$，就知道每个 $\mathbf{x}$ 都应当被归入后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 最大的类别。

<!-- pdf-page: 61 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-25.png" alt="癌症治疗问题的损失矩阵，漏诊损失为1000、误报损失为1、正确判断损失为0"><figcaption>图 1.25：癌症治疗问题的一个损失矩阵示例，其元素为 $L_{kj}$。行对应真实类别，列对应决策准则所分配的类别。</figcaption><p class="figure-translation">cancer → 癌症；normal → 正常。各单元格的中文对应如下。</p></figure>

| 真实类别／判定类别 | 癌症 | 正常 |
| --- | ---: | ---: |
| 癌症 | 0 | 1000 |
| 正常 | 1 | 0 |

### 1.5.2 最小化期望损失

在许多应用中，我们的目标比单纯减少误分类次数更复杂。再次考虑医学诊断问题。对于没有癌症的患者，如果错误地诊断为患有癌症，后果可能是给患者带来一些痛苦，并需要进一步检查。相反，如果把癌症患者诊断为健康，可能因未得到治疗而使其过早死亡。因此，这两种错误的后果可能截然不同。显然，即使要以增加第一类错误为代价，也应尽量减少第二类错误。

可以通过引入*损失函数*（loss function），也称*代价函数*（cost function），来形式化地处理这些问题。损失函数用一个统一的量，衡量采取各个可选决策或行动时造成的损失。我们的目标于是变成最小化总损失。注意，有些作者使用*效用函数*（utility function），并希望将其最大化。如果把效用定义为损失的相反数，这两个概念就是等价的。本书统一采用损失函数的说法。设对于新的 $\mathbf{x}$，其真实类别为 $\mathcal{C}_k$，而我们把它归入类别 $\mathcal{C}_j$（$j$ 可能等于 $k$，也可能不等于）。这样做产生一定的损失，记为 $L_{kj}$，可以把它看作*损失矩阵*的第 $k,j$ 个元素。例如，在癌症诊断例子中，损失矩阵可以采用图 1.25 所示形式。这个具体的损失矩阵表示：决策正确时没有损失；将健康患者诊断为患癌症时，损失为 1；将癌症患者诊断为健康时，损失为 1000。

最优解应使损失函数最小。但是，损失函数依赖于真实类别，而真实类别是未知的。对于给定的输入向量 $\mathbf{x}$，真实类别的不确定性由联合概率分布 $p(\mathbf{x},\mathcal{C}_k)$ 表示，因此，我们转而最小化相对于这个分布计算的平均损失，即

$$
\mathbb{E}[L]=\sum_k\sum_j\int_{\mathcal{R}_j}L_{kj}p(\mathbf{x},\mathcal{C}_k)\,\mathrm{d}\mathbf{x}.
\tag{1.80}
$$

每个 $\mathbf{x}$ 都可以独立地分配到某个决策区域 $\mathcal{R}_j$。我们的目标是选择这些区域，使期望损失（1.80）最小。这意味着，对每个 $\mathbf{x}$，应当最小化 $\sum_k L_{kj}p(\mathbf{x},\mathcal{C}_k)$。与前面一样，可以用乘积法则 $p(\mathbf{x},\mathcal{C}_k)=p(\mathcal{C}_k\mid\mathbf{x})p(\mathbf{x})$ 消去共同因子 $p(\mathbf{x})$。因此，使期望损失最小的决策规则，是将每个

<!-- pdf-page: 62 -->
<!-- join-previous-paragraph -->
新的 $\mathbf{x}$ 归入使下式最小的类别 $j$：

$$
\sum_k L_{kj}p(\mathcal{C}_k\mid\mathbf{x}).
\tag{1.81}
$$

显然，一旦知道类别后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$，这件事就十分简单。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-26.png" alt="两个类别的后验概率曲线，以及两者最大值不超过阈值时的拒绝区域"><figcaption>图 1.26：拒绝选项示意图。如果输入 $x$ 对应的两个后验概率中较大的一个小于或等于阈值 $\theta$，就拒绝对它分类。</figcaption><p class="figure-translation">reject region → 拒绝区域；$p(\mathcal{C}_1\mid x)$、$p(\mathcal{C}_2\mid x)$ 为两个类别的后验概率；$\theta$ 为阈值。</p></figure>

### 1.5.3 拒绝选项

我们已经看到，分类错误来自输入空间中的这样一些区域：最大的后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 显著小于 1，或者等价地，各联合分布 $p(\mathbf{x},\mathcal{C}_k)$ 的值相差不大。在这些区域，我们对类别归属相对不确定。对于一些应用，可以不对难以判断的样本作出决策，以期降低那些已经作出分类决策的样本的错误率。这称为*拒绝选项*（reject option）。例如，在上述假想的医学应用中，对于正确类别几乎没有疑问的 X 射线图像，可以由自动系统分类，而将较模糊的情况交给人类专家。为此，可以引入阈值 $\theta$，当输入 $\mathbf{x}$ 对应的最大后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$ 小于或等于 $\theta$ 时，就拒绝分类。图 1.26 用两个类别、一个连续输入变量 $x$ 的情形说明了这一点。注意，取 $\theta=1$ 能保证拒绝所有样本；如果有 $K$ 个类别，取 $\theta<1/K$ 则能保证不拒绝任何样本。因此，被拒绝样本的比例由 $\theta$ 的值控制。

当给定损失矩阵时，只要把作出拒绝决定所造成的损失也考虑进来，就可以很容易地扩展拒绝准则，使期望损失最小（习题 1.24）。

### 1.5.4 推断与决策

我们已经把分类问题分成两个独立阶段：在*推断阶段*，利用训练数据学习 $p(\mathcal{C}_k\mid\mathbf{x})$ 的模型；在随后的

<!-- pdf-page: 63 -->
<!-- join-previous-paragraph -->
*决策阶段*，利用这些后验概率作出最优的类别分配。另一种可能是把这两个问题一起解决，直接学习一个从输入 $\mathbf{x}$ 映射到决策的函数。这种函数称为*判别函数*（discriminant function）。

事实上，求解决策问题可以区分为三种方法，它们都在实际应用中使用过。按复杂程度由高到低排列如下：

**（a）** 先解决推断问题，分别确定每个类别 $\mathcal{C}_k$ 的类条件密度 $p(\mathbf{x}\mid\mathcal{C}_k)$，并单独推断类别先验概率 $p(\mathcal{C}_k)$。然后利用如下形式的贝叶斯定理

$$
p(\mathcal{C}_k\mid\mathbf{x})=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{p(\mathbf{x})}
\tag{1.82}
$$

求出类别后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$。与往常一样，贝叶斯定理的分母可以根据分子中的量求出，因为

$$
p(\mathbf{x})=\sum_k p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k).
\tag{1.83}
$$

等价地，也可以直接建立联合分布 $p(\mathbf{x},\mathcal{C}_k)$ 的模型，再归一化得到后验概率。得到后验概率之后，利用决策论确定每个新输入 $\mathbf{x}$ 的类别归属。显式或隐式地同时对输入和输出分布建模的方法称为*生成式模型*（generative model），因为可以从模型中抽样，在输入空间内生成合成的数据点。

**（b）** 先解决推断问题，确定类别后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$，然后用决策论将每个新的 $\mathbf{x}$ 归入某一类别。直接对后验概率建模的方法称为*判别式模型*（discriminative model）。

**（c）** 找到一个称为判别函数的函数 $f(\mathbf{x})$，将每个输入 $\mathbf{x}$ 直接映射到类别标签。例如，对于二分类问题，$f(\cdot)$ 可以取二元值，其中 $f=0$ 表示类别 $\mathcal{C}_1$，$f=1$ 表示类别 $\mathcal{C}_2$。在这种情况下，概率不起作用。

下面比较这三种方案的优缺点。方法（a）要求最高，因为需要确定 $\mathbf{x}$ 与 $\mathcal{C}_k$ 的联合分布。在许多应用中，$\mathbf{x}$ 的维数很高，因此可能需要很大的训练集，才能以合理的精度确定类条件密度。注意，类别先验 $p(\mathcal{C}_k)$ 往往只需根据训练集中各类别的数据点所占比例就能估计出来。不过，方法（a）的一个优点是：还能根据式（1.83）确定数据的边缘密度 $p(\mathbf{x})$。这有助于发现那些在模型下概率很低、预测结果可能

<!-- pdf-page: 64 -->
<!-- join-previous-paragraph -->
不太准确的新数据点。这称为*离群点检测*（outlier detection）或*新颖性检测*（novelty detection；Bishop，1994；Tarassenko，1995）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-27.png" alt="两个类别的类条件密度与相应后验概率，绿线标出最小误分类率边界"><figcaption>图 1.27：只有一个输入变量 $x$ 时，两个类别的类条件密度示例（左图）及相应的后验概率（右图）。注意，左图蓝色类条件密度 $p(x\mid\mathcal{C}_1)$ 左侧的众数对后验概率没有影响。右图的绿色竖线表示使误分类率最小的 $x$ 方向决策边界。</figcaption><p class="figure-translation">class densities → 类条件密度；$p(x\mid\mathcal{C}_1)$、$p(x\mid\mathcal{C}_2)$ 为类条件密度；$p(\mathcal{C}_1\mid x)$、$p(\mathcal{C}_2\mid x)$ 为后验概率；横轴为 $x$。</p></figure>

但是，如果我们只想进行分类决策，求联合分布 $p(\mathbf{x},\mathcal{C}_k)$ 可能浪费计算资源，对数据量的要求也可能过高，因为真正需要的只是后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$，而它可以通过方法（b）直接求得。事实上，类条件密度可能包含许多对后验概率影响甚微的结构，如图 1.27 所示。研究机器学习中生成式方法与判别式方法的相对优缺点，以及寻找将两者结合的方法，一直受到广泛关注（Jebara，2004；Lasserre et al.，2006）。

更简单的是方法（c）：利用训练数据找出判别函数 $f(\mathbf{x})$，把每个 $\mathbf{x}$ 直接映射到类别标签，从而将推断和决策阶段合并为一个学习问题。在图 1.27 的例子中，这相当于寻找绿色竖线所对应的 $x$ 值，因为它给出了使误分类概率最小的决策边界。

然而，采用方法（c）就无法再得到后验概率 $p(\mathcal{C}_k\mid\mathbf{x})$。即使最终仍要用后验概率作出决策，我们也有许多充分理由先计算它们，包括：

**最小化风险。** 考虑损失矩阵元素需要不时修订的情形（例如金融

<!-- pdf-page: 65 -->
<!-- join-previous-paragraph -->
应用中就可能如此）。如果知道后验概率，只需适当地修改式（1.81），就能很容易地调整最小风险决策准则。如果只有判别函数，损失矩阵的任何改动都会要求我们回到训练数据，重新求解整个分类问题。

**拒绝选项。** 当拒绝的数据点比例给定时，后验概率使我们能够确定一个拒绝准则，让误分类率，或更一般地，让期望损失达到最小。

**校正类别先验。** 再次考虑医学 X 射线图像问题，假设为了建立自动筛查系统，我们从一般人群中收集了大量 X 射线图像作为训练数据。由于癌症在一般人群中较少见，可能每 1000 个样本中只有 1 个属于癌症。如果用这种数据集训练自适应模型，癌症类别所占比例太小可能带来严重困难。例如，一个把所有点都判定为正常的分类器，已经能达到 99.9% 的准确率，因此很难避免得到这种没有实际价值的解。此外，即使数据集很大，其中的癌症 X 射线图像仍然很少，学习算法无法接触到这类图像的多种不同样本，因而不大可能具有良好的泛化性能。如果从各类别中选取相同数量的样本，组成一个平衡的数据集，就能找到更准确的模型。不过，此时必须校正我们修改训练数据所产生的影响。假设已经用这种修改后的数据集建立了后验概率模型。根据贝叶斯定理（1.82），后验概率与先验概率成正比，而先验概率可以解释为各类别中数据点的比例。因此，只需把人为平衡的数据集上得到的后验概率，先除以该数据集中相应类别的比例，再乘以模型实际应用人群中相应类别的比例。最后还需要归一化，确保新的后验概率之和为 1。注意，如果直接学习判别函数而没有确定后验概率，就无法使用这个过程。

**组合模型。** 对于复杂应用，我们可能希望把问题拆分成若干较小的子问题，每个子问题交给独立模块处理。例如，在假想的医学诊断问题中，除了 X 射线图像，还可能有血液检查等信息。与其将这些不同类型的信息合并到一个巨大的输入空间，不如分别建立一个系统解释 X 射线图像，另一个系统解释血液数据，这样可能更有效。只要两个模型都给出类别后验概率，就可以运用概率规则有系统地组合它们的输出。一种简单的做法是：对每个类别分别假设，X 射线图像输入（记为 $\mathbf{x}_{\mathrm I}$）和血液数据输入（记为 $\mathbf{x}_{\mathrm B}$）的分布

<!-- pdf-page: 66 -->
<!-- join-previous-paragraph -->
相互独立，于是有

$$
p(\mathbf{x}_{\mathrm I},\mathbf{x}_{\mathrm B}\mid\mathcal{C}_k)=p(\mathbf{x}_{\mathrm I}\mid\mathcal{C}_k)p(\mathbf{x}_{\mathrm B}\mid\mathcal{C}_k).
\tag{1.84}
$$

这是*条件独立*（conditional independence）性质的一个例子（第 8.2 节），因为独立性是在以类别 $\mathcal{C}_k$ 为条件时成立的。同时给定 X 射线图像与血液数据时，后验概率为

$$
\begin{aligned}
p(\mathcal{C}_k\mid\mathbf{x}_{\mathrm I},\mathbf{x}_{\mathrm B})
&\propto p(\mathbf{x}_{\mathrm I},\mathbf{x}_{\mathrm B}\mid\mathcal{C}_k)p(\mathcal{C}_k)\\
&\propto p(\mathbf{x}_{\mathrm I}\mid\mathcal{C}_k)p(\mathbf{x}_{\mathrm B}\mid\mathcal{C}_k)p(\mathcal{C}_k)\\
&\propto\frac{p(\mathcal{C}_k\mid\mathbf{x}_{\mathrm I})p(\mathcal{C}_k\mid\mathbf{x}_{\mathrm B})}{p(\mathcal{C}_k)}.
\end{aligned}
\tag{1.85}
$$

因此，我们需要类别先验概率 $p(\mathcal{C}_k)$；它可以容易地由各类别数据点所占的比例估计。然后，需要将得到的后验概率归一化，使其和为 1。式（1.84）中这个特定的条件独立假设，是*朴素贝叶斯模型*（naive Bayes model）的一个例子（第 8.2.2 节）。注意，在该模型中，联合边缘分布 $p(\mathbf{x}_{\mathrm I},\mathbf{x}_{\mathrm B})$ 通常不能分解为因子的乘积。后续章节将介绍如何构建无需条件独立假设（1.84）的数据组合模型。

### 1.5.5 回归的损失函数

到目前为止，我们一直在分类问题的背景下讨论决策论。现在转向回归问题，例如前面讨论过的曲线拟合（第 1.1 节）。决策阶段要为每个输入 $\mathbf{x}$ 选出一个对 $t$ 的具体估计值 $y(\mathbf{x})$。假设这样做造成的损失为 $L(t,y(\mathbf{x}))$，则平均损失，也就是期望损失，为

$$
\mathbb{E}[L]=\iint L(t,y(\mathbf{x}))p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t.
\tag{1.86}
$$

回归问题中常用的一个损失函数是*平方损失*，即 $L(t,y(\mathbf{x}))=\{y(\mathbf{x})-t\}^2$。此时期望损失可以写为

$$
\mathbb{E}[L]=\iint\{y(\mathbf{x})-t\}^2p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t.
\tag{1.87}
$$

我们的目标是选择 $y(\mathbf{x})$，使 $\mathbb{E}[L]$ 最小。如果假设函数 $y(\mathbf{x})$ 可以完全自由地选择，就可以形式上利用变分法（附录 D）得到

$$
\frac{\delta\mathbb{E}[L]}{\delta y(\mathbf{x})}=2\int\{y(\mathbf{x})-t\}p(\mathbf{x},t)\,\mathrm{d}t=0.
\tag{1.88}
$$

解出 $y(\mathbf{x})$，并利用概率的求和法则和乘积法则，得到

$$
y(\mathbf{x})=\frac{\int t p(\mathbf{x},t)\,\mathrm{d}t}{p(\mathbf{x})}=\int t p(t\mid\mathbf{x})\,\mathrm{d}t=\mathbb{E}_t[t\mid\mathbf{x}].
\tag{1.89}
$$

<!-- pdf-page: 67 -->

这就是给定 $\mathbf{x}$ 时 $t$ 的条件平均值，称为*回归函数*（regression function）。图 1.28 说明了这一结果。它可以很容易地推广到以向量 $\mathbf{t}$ 表示的多个目标变量；此时，最优解是条件平均值 $\mathbf{y}(\mathbf{x})=\mathbb{E}_{\mathbf{t}}[\mathbf{t}\mid\mathbf{x}]$（习题 1.25）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-28.png" alt="回归函数等于各输入处目标变量条件分布的均值"><figcaption>图 1.28：使期望平方损失最小的回归函数 $y(x)$，由条件分布 $p(t\mid x)$ 的均值给出。</figcaption><p class="figure-translation">$x$ 为输入，$t$ 为目标；$x_0$ 为给定输入，$p(t\mid x_0)$ 为该输入处的条件分布，$y(x_0)$ 为其均值；$y(x)$ 为回归函数。</p></figure>

还可以用稍有不同的方法推导这个结果，它也能帮助我们理解回归问题的性质。既然已经知道最优解是条件期望，就可以将平方项展开为

$$
\begin{aligned}
\{y(\mathbf{x})-t\}^2
&=\{y(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]+\mathbb{E}[t\mid\mathbf{x}]-t\}^2\\
&=\{y(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}^2\\
&\quad+2\{y(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}\{\mathbb{E}[t\mid\mathbf{x}]-t\}\\
&\quad+\{\mathbb{E}[t\mid\mathbf{x}]-t\}^2,
\end{aligned}
$$

其中，为了简化记号，用 $\mathbb{E}[t\mid\mathbf{x}]$ 表示 $\mathbb{E}_t[t\mid\mathbf{x}]$。代入损失函数，并对 $t$ 积分，可以看到交叉项消失，得到如下形式的损失函数表达式：

$$
\mathbb{E}[L]=\int\{y(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}+\int\{\mathbb{E}[t\mid\mathbf{x}]-t\}^2p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{1.90}
$$

我们要确定的函数 $y(\mathbf{x})$ 只出现在第一项中。当 $y(\mathbf{x})$ 等于 $\mathbb{E}[t\mid\mathbf{x}]$ 时，这一项最小，并且等于零。这就是前面推导出的结果，说明最优的最小二乘预测器由条件均值给出。第二项是 $t$ 的分布的方差再对 $\mathbf{x}$ 取平均。它表示目标数据固有的变动，可以看作噪声。由于它不依赖于 $y(\mathbf{x})$，所以代表损失函数无法进一步降低的最小值。

与分类问题一样，我们既可以先确定合适的概率，再用它们作出最优决策，也可以建立直接作出决策的模型。事实上，回归问题同样可以区分出三种求解方法，按复杂程度由高到低排列如下：

**（a）** 先解决推断问题，确定联合密度 $p(\mathbf{x},t)$；然后归一化，求出条件密度 $p(t\mid\mathbf{x})$；最后进行边缘化，求得式（1.89）给出的条件均值。

<!-- pdf-page: 68 -->

**（b）** 先解决推断问题，确定条件密度 $p(t\mid\mathbf{x})$；然后进行边缘化，求得式（1.89）给出的条件均值。

**（c）** 直接从训练数据中求出回归函数 $y(\mathbf{x})$。

这三种方法的相对优缺点，与前述分类问题中的情况相同。

平方损失并不是回归问题唯一可选的损失函数。事实上，在某些情形下，平方损失会产生很差的结果，需要发展更精细的方法。一个重要例子是条件分布 $p(t\mid\mathbf{x})$ 具有多个众数的情况，求解逆问题时就经常如此（第 5.6 节）。这里简要介绍平方损失的一种简单推广，称为*闵可夫斯基损失*（Minkowski loss），其期望为

$$
\mathbb{E}[L_q]=\iint|y(\mathbf{x})-t|^q p(\mathbf{x},t)\,\mathrm{d}\mathbf{x}\,\mathrm{d}t.
\tag{1.91}
$$

当 $q=2$ 时，它退化为期望平方损失。图 1.29 对不同的 $q$ 值画出了函数 $|y-t|^q$ 随 $y-t$ 的变化。使 $\mathbb{E}[L_q]$ 最小的解，在 $q=2$ 时为条件均值，在 $q=1$ 时为条件中位数，在 $q\to0$ 时为条件众数（习题 1.27）。

## 1.6 信息论

本章讨论了概率论和决策论中的各种概念，它们构成本书后续大部分讨论的基础。作为本章的结尾，我们再介绍信息论中的一些概念；在发展模式识别与机器学习方法时，它们同样有用。这里仍然只关注核心概念，详细论述请参见其他文献（Viterbi and Omura，1979；Cover and Thomas，1991；MacKay，2003）。

先考虑一个离散随机变量 $x$：当观测到它的某个具体取值时，我们获得了多少信息？信息量可以看作得知 $x$ 的取值时的“惊讶程度”。如果有人告诉我们一个极不可能的事件刚刚发生了，那么相比于得知一个很可能的事件刚刚发生，我们获得的信息更多；如果事先就知道事件必然发生，那么就不会获得任何信息。因此，信息量的度量应依赖概率分布 $p(x)$。我们要寻找一个量 $h(x)$，它是概率 $p(x)$ 的单调函数，并表达信息量。要确定 $h(\cdot)$ 的形式，可以注意到：如果事件 $x$ 和 $y$ 互不相关，那么同时观测到两个事件所得到的信息，应当等于分别观测每个事件所得到的信息之和，即 $h(x,y)=h(x)+h(y)$。两个互不相关的事件在统计上独立，所以 $p(x,y)=p(x)p(y)$。根据这两个关系，很容易证明 $h(x)$ 必须由 $p(x)$ 的对数给出（习题 1.28），因此有

<!-- pdf-page: 69 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-29.png" alt="闵可夫斯基损失在q等于0.3、1、2、10时的曲线"><figcaption>图 1.29：不同 $q$ 值下，量 $L_q=|y-t|^q$ 的曲线。</figcaption><p class="figure-translation">横轴 $y-t$ 为预测值与目标值之差，纵轴为 $|y-t|^q$；四幅图分别对应 $q=0.3$、$q=1$、$q=2$、$q=10$。</p></figure>

$$
h(x)=-\log_2 p(x)
\tag{1.92}
$$

其中负号确保信息量非负。注意，概率较小的事件 $x$ 对应较大的信息量。对数底数可以任意选择，目前先采用信息论中常见的约定，以 2 为底。很快就会看到，在这种情况下，$h(x)$ 的单位是*比特*（bit，即“二进制数位”）。

现在假设发送者希望把一个随机变量的值传给接收者。在这个过程中传输的平均信息量，可以通过对式（1.92）按照分布 $p(x)$ 取期望得到，即

$$
\mathrm{H}[x]=-\sum_x p(x)\log_2 p(x).
\tag{1.93}
$$

这个重要的量称为随机变量 $x$ 的*熵*（entropy）。注意，$\lim_{p\to0}p\ln p=0$，因此，每当某个 $x$ 满足 $p(x)=0$ 时，就取 $p(x)\ln p(x)=0$。

到目前为止，我们只是通过较为直观的启发式论证来引出信息量

<!-- pdf-page: 70 -->
<!-- join-previous-paragraph -->
（1.92）及相应的熵（1.93）的定义。现在说明，这些定义确实具有有用的性质。考虑随机变量 $x$，它有 8 个可能状态，且每个状态等可能。要把 $x$ 的值传给接收者，就需要发送一个长度为 3 比特的消息。注意，这个变量的熵为

$$
\mathrm{H}[x]=-8\times\frac18\log_2\frac18=3\text{ 比特}.
$$

再考虑一个例子（Cover and Thomas，1991）：一个变量有 8 个可能状态 $\{a,b,c,d,e,f,g,h\}$，相应概率为 $\left(\frac12,\frac14,\frac18,\frac1{16},\frac1{64},\frac1{64},\frac1{64},\frac1{64}\right)$。此时的熵为

$$
\mathrm{H}[x]=-\frac12\log_2\frac12-\frac14\log_2\frac14-\frac18\log_2\frac18-\frac1{16}\log_2\frac1{16}-\frac4{64}\log_2\frac1{64}=2\text{ 比特}.
$$

可以看到，非均匀分布的熵小于均匀分布的熵。稍后从无序程度的角度解释熵时，我们会进一步理解这一点。现在先考虑，如何把变量所处的状态传给接收者。和前面一样，可以使用一个 3 比特的数。但也可以利用分布的不均匀性：对较可能的事件使用较短的码字，代价是对较不可能的事件使用较长的码字，以求缩短平均码长。例如，可以依次用下面的码字表示状态 $\{a,b,c,d,e,f,g,h\}$：`0`、`10`、`110`、`1110`、`111100`、`111101`、`111110`、`111111`。此时需要传输的平均码长为

$$
\text{平均码长}=\frac12\times1+\frac14\times2+\frac18\times3+\frac1{16}\times4+4\times\frac1{64}\times6=2\text{ 比特},
$$

再次等于随机变量的熵。注意，不能使用更短的码字，因为这些码字连接起来之后，必须能够无歧义地拆分成各个组成部分。例如，`11001110` 可以唯一地解码为状态序列 $c,a,d$。

熵与最短编码长度之间的关系具有普遍性。*无噪声编码定理*（noiseless coding theorem；Shannon，1948）指出，熵是传输随机变量状态所需比特数的下界。

从现在开始，定义熵时改用自然对数，这样能更方便地与本书其他部分的概念联系起来。此时熵的单位为 *nat*，而不是比特；两者只相差一个 $\ln2$ 的因子。

我们从指定随机变量状态所需的平均信息量出发，介绍了熵的概念。事实上，熵在物理学中的起源要早得多：它最初在平衡热力学中被引入，后来随着统计力学的发展，获得了作为无序程度度量的更深入解释。要理解熵的这种解释，可以考虑将 $N$ 个相同的物体分配到一组箱子中，使第 $i$ 个箱子有 $n_i$ 个物体。考虑

<!-- pdf-page: 71 -->
<!-- join-previous-paragraph -->
把这些物体分配到箱子中的不同方式有多少种。选择第一个物体有 $N$ 种方式，选择第二个有 $N-1$ 种，以此类推，因此将全部 $N$ 个物体分配到箱子中，总共有 $N!$ 种方式。其中 $N!$ 读作“$N$ 的阶乘”，表示乘积 $N\times(N-1)\times\cdots\times2\times1$。不过，我们不想区分同一箱子内物体的不同排列。第 $i$ 个箱子内的物体有 $n_i!$ 种排列方式，所以将 $N$ 个物体分配到箱子中的不同方式总数为

$$
W=\frac{N!}{\prod_i n_i!},
\tag{1.94}
$$

称为*多重度*（multiplicity）。于是把熵定义为多重度的对数，再乘以合适的常数：

$$
\mathrm{H}=\frac1N\ln W=\frac1N\ln N!-\frac1N\sum_i\ln n_i!.
\tag{1.95}
$$

现在考虑 $N\to\infty$ 的极限，同时保持各比例 $n_i/N$ 不变，并使用 Stirling 近似

$$
\ln N!\simeq N\ln N-N,
\tag{1.96}
$$

得到

$$
\mathrm{H}=-\lim_{N\to\infty}\sum_i\left(\frac{n_i}{N}\right)\ln\left(\frac{n_i}{N}\right)=-\sum_i p_i\ln p_i,
\tag{1.97}
$$

其中使用了 $\sum_i n_i=N$。这里，$p_i=\lim_{N\to\infty}(n_i/N)$ 是物体被分配到第 $i$ 个箱子的概率。用物理学的术语说，物体在箱子中的具体排列称为*微观态*（microstate）；由比例 $n_i/N$ 表示的整体占据数分布称为*宏观态*（macrostate）。多重度 $W$ 也称为宏观态的*权重*（weight）。

可以把箱子解释为离散随机变量 $X$ 的状态 $x_i$，其中 $p(X=x_i)=p_i$。随机变量 $X$ 的熵于是为

$$
\mathrm{H}[p]=-\sum_i p(x_i)\ln p(x_i).
\tag{1.98}
$$

在少数取值附近形成尖峰的分布 $p(x_i)$，熵相对较低；而在许多取值上分布得较均匀的分布，熵较高，如图 1.30 所示。由于 $0\leqslant p_i\leqslant1$，熵非负；当某个 $p_i=1$、其余所有 $p_{j\ne i}=0$ 时，熵取最小值 0。要找出熵最大的分布，可以使用拉格朗日乘子施加概率归一化约束，再最大化 $\mathrm{H}$（附录 E）。也就是最大化

$$
\widetilde{\mathrm{H}}=-\sum_i p(x_i)\ln p(x_i)+\lambda\left(\sum_i p(x_i)-1\right).
\tag{1.99}
$$

<!-- pdf-page: 72 -->

由此可得，所有 $p(x_i)$ 都相等，且 $p(x_i)=1/M$，其中 $M$ 是状态 $x_i$ 的总数。对应的熵为 $\mathrm{H}=\ln M$。这个结果也可以由稍后将讨论的 Jensen 不等式导出（习题 1.29）。为了验证该驻点确实是最大值，可以计算熵的二阶导数，得到

$$
\frac{\partial\widetilde{\mathrm{H}}}{\partial p(x_i)\partial p(x_j)}=-I_{ij}\frac1{p_i},
\tag{1.100}
$$

其中 $I_{ij}$ 是单位矩阵的元素。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-30.png" alt="30个箱子上的两个概率分布直方图，分布越宽熵越高"><figcaption>图 1.30：30 个箱子上的两个概率分布的直方图，说明较宽的分布具有较大的熵 $\mathrm{H}$。均匀分布的熵最大，其值为 $\mathrm{H}=-\ln(1/30)=3.40$。</figcaption><p class="figure-translation">probabilities → 概率；左图 $\mathrm{H}=1.77$，右图 $\mathrm{H}=3.09$。</p></figure>

还可以按如下方式将熵的定义推广到连续变量 $x$ 的分布 $p(x)$。先把 $x$ 划分为宽度为 $\Delta$ 的区间。假设 $p(x)$ 连续，根据中值定理（Weisstein，1999），每个区间内必定存在某个值 $x_i$，使得

$$
\int_{i\Delta}^{(i+1)\Delta}p(x)\,\mathrm{d}x=p(x_i)\Delta.
\tag{1.101}
$$

现在对连续变量 $x$ 进行量化：只要 $x$ 落在第 $i$ 个区间，就将其取值映射到 $x_i$。于是观测到 $x_i$ 的概率为 $p(x_i)\Delta$。这样得到了一个离散分布，其熵为

$$
\mathrm{H}_{\Delta}=-\sum_i p(x_i)\Delta\ln\bigl(p(x_i)\Delta\bigr)=-\sum_i p(x_i)\Delta\ln p(x_i)-\ln\Delta,
\tag{1.102}
$$

这里使用了由式（1.101）得到的 $\sum_i p(x_i)\Delta=1$。现在去掉式（1.102）右侧的第二项 $-\ln\Delta$，再考虑

<!-- pdf-page: 73 -->
<!-- join-previous-paragraph -->
$\Delta\to0$ 的极限。在此极限下，式（1.102）右侧第一项趋近于 $p(x)\ln p(x)$ 的积分，因此

$$
\lim_{\Delta\to0}\left\{\sum_i p(x_i)\Delta\ln p(x_i)\right\}=-\int p(x)\ln p(x)\,\mathrm{d}x.
\tag{1.103}
$$

右侧的量称为*微分熵*（differential entropy）。可以看到，熵的离散形式与连续形式相差一个 $\ln\Delta$，它在 $\Delta\to0$ 时发散。这反映了这样一个事实：要非常精确地指定连续变量，需要大量比特。对于多个连续变量的密度，若将这些变量统记为向量 $\mathbf{x}$，其微分熵为

$$
\mathrm{H}[\mathbf{x}]=-\int p(\mathbf{x})\ln p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{1.104}
$$

<aside class="biography"><p><strong>路德维希·玻尔兹曼（Ludwig Boltzmann）</strong><br>1844–1906</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-boltzmann.png" alt="路德维希·玻尔兹曼肖像"><p>路德维希·爱德华·玻尔兹曼是奥地利物理学家，创立了统计力学。在玻尔兹曼之前，经典热力学中已经有熵的概念，用来量化这样一个事实：从系统中取出的能量，通常不能全部用于做有用功。玻尔兹曼证明，宏观量热力学熵 $S$ 可以与微观层面的统计性质联系起来。这就是著名的公式 $S=k\ln W$，其中 $W$ 表示某个宏观态所对应的可能微观态数目，$k\simeq1.38\times10^{-23}$（单位为焦耳每开尔文）称为玻尔兹曼常数。玻尔兹曼的思想受到当时许多科学家的质疑。他们认为，其中一个困难来自热力学第二定律：封闭系统的熵倾向于随时间增加。相比之下，微观层面的经典牛顿物理方程是可逆的，因此他们很难理解，后者如何解释前者。他们没有充分理解玻尔兹曼的统计性论证：这一论证并不是说熵绝不可能随时间减少，而只是说，熵以压倒性的概率总体上会增加。玻尔兹曼甚至曾与德国一本主要物理学期刊的编辑长期争论；该编辑坚持认为，原子与分子只能被称为方便的理论构造。对其工作的持续攻击使他反复陷入抑郁，最终自杀。玻尔兹曼去世后不久，Perrin 对胶体悬浮液所做的新实验证实了他的理论，也确认了玻尔兹曼常数的数值。公式 $S=k\ln W$ 刻在玻尔兹曼的墓碑上。</p></aside>

对于离散分布，我们看到，变量各个可能状态的概率相等时，熵最大。现在考虑连续变量的最大熵分布。为了使这个最大值有明确的定义，除了保持归一化约束，还必须约束 $p(x)$ 的一阶矩和二阶矩。因此，我们在以下

<!-- pdf-page: 74 -->
<!-- join-previous-paragraph -->
三个约束下最大化微分熵：

$$
\int_{-\infty}^{\infty}p(x)\,\mathrm{d}x=1,
\tag{1.105}
$$

$$
\int_{-\infty}^{\infty}xp(x)\,\mathrm{d}x=\mu,
\tag{1.106}
$$

$$
\int_{-\infty}^{\infty}(x-\mu)^2p(x)\,\mathrm{d}x=\sigma^2.
\tag{1.107}
$$

可以利用拉格朗日乘子完成有约束的最大化（附录 E），也就是对 $p(x)$ 最大化以下泛函：

$$
\begin{aligned}
&-\int_{-\infty}^{\infty}p(x)\ln p(x)\,\mathrm{d}x
+\lambda_1\left(\int_{-\infty}^{\infty}p(x)\,\mathrm{d}x-1\right)\\
&\quad+\lambda_2\left(\int_{-\infty}^{\infty}xp(x)\,\mathrm{d}x-\mu\right)
+\lambda_3\left(\int_{-\infty}^{\infty}(x-\mu)^2p(x)\,\mathrm{d}x-\sigma^2\right).
\end{aligned}
$$

利用变分法（附录 D），令这个泛函的导数为零，得到

$$
p(x)=\exp\{-1+\lambda_1+\lambda_2x+\lambda_3(x-\mu)^2\}.
\tag{1.108}
$$

将这个结果代回三个约束方程，即可求得拉格朗日乘子，最终得到（习题 1.34）

$$
p(x)=\frac1{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac{(x-\mu)^2}{2\sigma^2}\right\}.
\tag{1.109}
$$

因此，使微分熵最大的分布是高斯分布。注意，最大化熵时，我们并未约束分布非负。不过，求出的分布确实非负，因此事后看来，没有必要另加这个约束。

计算高斯分布的微分熵，得到（习题 1.35）

$$
\mathrm{H}[x]=\frac12\{1+\ln(2\pi\sigma^2)\}.
\tag{1.110}
$$

因此我们再次看到，分布越宽，也就是 $\sigma^2$ 越大，熵就越大。这个结果还说明，与离散熵不同，微分熵可以为负，因为当 $\sigma^2<1/(2\pi e)$ 时，式（1.110）中的 $\mathrm{H}(x)<0$。

假设有联合分布 $p(\mathbf{x},\mathbf{y})$，从中抽取成对的 $\mathbf{x}$ 和 $\mathbf{y}$。如果已经知道 $\mathbf{x}$ 的值，那么指定相应的 $\mathbf{y}$ 所需的额外信息为 $-\ln p(\mathbf{y}\mid\mathbf{x})$。因此，指定 $\mathbf{y}$ 所需的平均额外信息可以写为

$$
\mathrm{H}[\mathbf{y}\mid\mathbf{x}]=-\iint p(\mathbf{y},\mathbf{x})\ln p(\mathbf{y}\mid\mathbf{x})\,\mathrm{d}\mathbf{y}\,\mathrm{d}\mathbf{x}.
\tag{1.111}
$$

<!-- pdf-page: 75 -->

这称为给定 $\mathbf{x}$ 时 $\mathbf{y}$ 的*条件熵*（conditional entropy）。利用乘积法则，很容易看出条件熵满足以下关系（习题 1.37）：

$$
\mathrm{H}[\mathbf{x},\mathbf{y}]=\mathrm{H}[\mathbf{y}\mid\mathbf{x}]+\mathrm{H}[\mathbf{x}],
\tag{1.112}
$$

其中 $\mathrm{H}[\mathbf{x},\mathbf{y}]$ 是 $p(\mathbf{x},\mathbf{y})$ 的微分熵，$\mathrm{H}[\mathbf{x}]$ 是边缘分布 $p(\mathbf{x})$ 的微分熵。因此，描述 $\mathbf{x}$ 和 $\mathbf{y}$ 所需的信息，等于单独描述 $\mathbf{x}$ 所需的信息，加上给定 $\mathbf{x}$ 后指定 $\mathbf{y}$ 所需的额外信息。

### 1.6.1 相对熵与互信息

本节到目前为止介绍了一些信息论概念，包括熵这一核心概念。现在开始将这些思想与模式识别联系起来。考虑某个未知分布 $p(\mathbf{x})$，假设用近似分布 $q(\mathbf{x})$ 对其建模。如果根据 $q(\mathbf{x})$ 构造编码方案，把 $\mathbf{x}$ 的值传给接收者，那么由于使用了 $q(\mathbf{x})$ 而不是真实分布 $p(\mathbf{x})$，指定 $\mathbf{x}$ 的值所需的平均额外信息量（单位为 nat，并假设选择了高效的编码方案）为

$$
\begin{aligned}
\mathrm{KL}(p\Vert q)
&=-\int p(\mathbf{x})\ln q(\mathbf{x})\,\mathrm{d}\mathbf{x}-\left(-\int p(\mathbf{x})\ln p(\mathbf{x})\,\mathrm{d}\mathbf{x}\right)\\
&=-\int p(\mathbf{x})\ln\left\{\frac{q(\mathbf{x})}{p(\mathbf{x})}\right\}\,\mathrm{d}\mathbf{x}.
\end{aligned}
\tag{1.113}
$$

这称为分布 $p(\mathbf{x})$ 与 $q(\mathbf{x})$ 之间的*相对熵*（relative entropy），或 *Kullback–Leibler 散度*，简称 *KL 散度*（Kullback and Leibler，1951）。注意，它不是对称的量，即 $\mathrm{KL}(p\Vert q)\not\equiv\mathrm{KL}(q\Vert p)$。

<aside class="biography"><p><strong>克劳德·香农（Claude Shannon）</strong><br>1916–2001</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-shannon.png" alt="克劳德·香农肖像"><p>香农从密歇根大学和麻省理工学院毕业后，于 1941 年加入 AT&amp;T 贝尔电话实验室。他于 1948 年在《贝尔系统技术杂志》（Bell System Technical Journal）发表的论文《通信的数学理论》（A Mathematical Theory of Communication），奠定了现代信息论的基础。这篇论文引入了“bit”一词；他提出信息可以作为 1 和 0 的序列发送，这一观念为通信革命铺平了道路。据说，冯·诺伊曼建议香农使用“熵”这个术语，不仅因为它与物理学中使用的量相似，还因为“没有人真正知道熵是什么，所以无论在什么讨论中，你总会占据优势”。</p></aside>

现在证明，Kullback–Leibler 散度满足 $\mathrm{KL}(p\Vert q)\geqslant0$，且当且仅当 $p(\mathbf{x})=q(\mathbf{x})$ 时取等号。为此，先介绍*凸函数*（convex function）的概念。如果函数 $f(x)$ 的任意弦都位于函数曲线之上或与之重合，就称它为凸函数，如图 1.31 所示。区间 $x=a$ 到 $x=b$ 中的任意 $x$，都可以写成 $\lambda a+(1-\lambda)b$，其中 $0\leqslant\lambda\leqslant1$。弦上对应的点由 $\lambda f(a)+(1-\lambda)f(b)$ 给出，

<!-- pdf-page: 76 -->
<!-- join-previous-paragraph -->
而相应的函数值为 $f(\lambda a+(1-\lambda)b)$。于是凸性意味着

$$
f(\lambda a+(1-\lambda)b)\leqslant\lambda f(a)+(1-\lambda)f(b).
\tag{1.114}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-01/b-fig-1-31.png" alt="凸函数的任意弦位于函数曲线上方"><figcaption>图 1.31：对于凸函数 $f(x)$，每条弦（蓝色）都位于函数曲线（红色）上方或与之重合。</figcaption><p class="figure-translation">chord → 弦；$a$、$b$ 为弦两端对应的横坐标，$x_{\lambda}$ 为两者之间的横坐标；$f(x)$ 为函数。</p></figure>

这等价于要求函数的二阶导数处处为正（习题 1.36）。凸函数的例子有 $x\ln x$（$x>0$ 时）和 $x^2$。如果等号仅在 $\lambda=0$ 和 $\lambda=1$ 时成立，则称函数为*严格凸*（strictly convex）。如果函数具有相反的性质，即每条弦都位于函数曲线下方或与之重合，则称为*凹函数*（concave function），严格凹也有相应的定义。如果 $f(x)$ 为凸函数，那么 $-f(x)$ 就是凹函数。

利用数学归纳法，可以由式（1.114）证明，对于任意一组点 $\{x_i\}$，凸函数 $f(x)$ 满足（习题 1.38）

$$
f\left(\sum_{i=1}^{M}\lambda_i x_i\right)\leqslant\sum_{i=1}^{M}\lambda_i f(x_i),
\tag{1.115}
$$

其中 $\lambda_i\geqslant0$，且 $\sum_i\lambda_i=1$。式（1.115）称为 *Jensen 不等式*。如果把 $\lambda_i$ 解释为取值为 $\{x_i\}$ 的离散变量 $x$ 的概率分布，那么式（1.115）可以写为

$$
f\bigl(\mathbb{E}[x]\bigr)\leqslant\mathbb{E}[f(x)],
\tag{1.116}
$$

其中 $\mathbb{E}[\cdot]$ 表示期望。对于连续变量，Jensen 不等式的形式为

$$
f\left(\int xp(x)\,\mathrm{d}x\right)\leqslant\int f(x)p(x)\,\mathrm{d}x.
\tag{1.117}
$$

将形式（1.117）的 Jensen 不等式应用于 Kullback–Leibler 散度（1.113），得到

$$
\mathrm{KL}(p\Vert q)=-\int p(\mathbf{x})\ln\left\{\frac{q(\mathbf{x})}{p(\mathbf{x})}\right\}\,\mathrm{d}\mathbf{x}\geqslant-\ln\int q(\mathbf{x})\,\mathrm{d}\mathbf{x}=0.
\tag{1.118}
$$

<!-- pdf-page: 77 -->

这里利用了 $-\ln x$ 为凸函数这一事实，以及归一化条件 $\int q(\mathbf{x})\,\mathrm{d}\mathbf{x}=1$。事实上，$-\ln x$ 是严格凸函数，所以当且仅当对所有 $\mathbf{x}$ 都有 $q(\mathbf{x})=p(\mathbf{x})$ 时，等号成立。因此，可以将 Kullback–Leibler 散度解释为两个分布 $p(\mathbf{x})$ 与 $q(\mathbf{x})$ 的差异程度。

可以看到，数据压缩与密度估计（即为未知概率分布建模的问题）之间有密切联系，因为知道真实分布时，才能实现最高效的压缩。如果使用不同于真实分布的分布，编码效率必然较低，平均需要额外传输的信息量至少等于两个分布之间的 Kullback–Leibler 散度。

假设数据由未知分布 $p(\mathbf{x})$ 生成，而我们希望对它建模。可以用某个参数分布 $q(\mathbf{x}\mid\boldsymbol{\theta})$ 来近似它，例如多元高斯分布；该分布由一组可调参数 $\boldsymbol{\theta}$ 控制。确定 $\boldsymbol{\theta}$ 的一种方法，是关于 $\boldsymbol{\theta}$ 最小化 $p(\mathbf{x})$ 与 $q(\mathbf{x}\mid\boldsymbol{\theta})$ 之间的 Kullback–Leibler 散度。由于不知道 $p(\mathbf{x})$，无法直接这样做。但假设我们已观测到从 $p(\mathbf{x})$ 中抽取的有限个训练点 $\mathbf{x}_n$，$n=1,\ldots,N$，就可以根据式（1.35），用这些点上的有限求和来近似关于 $p(\mathbf{x})$ 的期望，于是

$$
\mathrm{KL}(p\Vert q)\simeq\sum_{n=1}^{N}\{-\ln q(\mathbf{x}_n\mid\boldsymbol{\theta})+\ln p(\mathbf{x}_n)\}.
\tag{1.119}
$$

式（1.119）右侧第二项与 $\boldsymbol{\theta}$ 无关，第一项则是在分布 $q(\mathbf{x}\mid\boldsymbol{\theta})$ 下，用训练集计算得到的关于 $\boldsymbol{\theta}$ 的负对数似然函数。因此，最小化这个 Kullback–Leibler 散度，等价于最大化似然函数。

现在考虑两组变量 $\mathbf{x}$ 和 $\mathbf{y}$ 的联合分布 $p(\mathbf{x},\mathbf{y})$。如果这两组变量独立，联合分布就可以分解为边缘分布的乘积，即 $p(\mathbf{x},\mathbf{y})=p(\mathbf{x})p(\mathbf{y})$。如果变量并不独立，那么通过考察联合分布与边缘分布乘积之间的 Kullback–Leibler 散度，可以了解它们是否“接近”独立。该散度为

$$
\begin{aligned}
\mathrm{I}[\mathbf{x},\mathbf{y}]
&\equiv\mathrm{KL}\bigl(p(\mathbf{x},\mathbf{y})\Vert p(\mathbf{x})p(\mathbf{y})\bigr)\\
&=-\iint p(\mathbf{x},\mathbf{y})\ln\left(\frac{p(\mathbf{x})p(\mathbf{y})}{p(\mathbf{x},\mathbf{y})}\right)\,\mathrm{d}\mathbf{x}\,\mathrm{d}\mathbf{y},
\end{aligned}
\tag{1.120}
$$

称为变量 $\mathbf{x}$ 与 $\mathbf{y}$ 之间的*互信息*（mutual information）。根据 Kullback–Leibler 散度的性质，有 $\mathrm{I}(\mathbf{x},\mathbf{y})\geqslant0$，且当且仅当 $\mathbf{x}$ 与 $\mathbf{y}$ 独立时取等号。利用概率的求和法则和乘积法则，可知互信息与条件熵之间有如下关系（习题 1.41）：

$$
\mathrm{I}[\mathbf{x},\mathbf{y}]=\mathrm{H}[\mathbf{x}]-\mathrm{H}[\mathbf{x}\mid\mathbf{y}]=\mathrm{H}[\mathbf{y}]-\mathrm{H}[\mathbf{y}\mid\mathbf{x}].
\tag{1.121}
$$

<!-- pdf-page: 78 -->

因此，可以将互信息看作：得知 $\mathbf{y}$ 的值之后，关于 $\mathbf{x}$ 的不确定性减少了多少（反过来也一样）。从贝叶斯观点看，可以把 $p(\mathbf{x})$ 看作 $\mathbf{x}$ 的先验分布，把 $p(\mathbf{x}\mid\mathbf{y})$ 看作观测到新数据 $\mathbf{y}$ 后的后验分布。因此，互信息表示新观测 $\mathbf{y}$ 所带来的关于 $\mathbf{x}$ 的不确定性减少量。

## 习题

**1.1（⋆）www** 考虑式（1.2）给出的平方和误差函数，其中函数 $y(x,\mathbf{w})$ 由多项式（1.1）给出。证明，使这一误差函数最小的系数 $\mathbf{w}=\{w_i\}$，由下列线性方程组的解给出：

$$
\sum_{j=0}^{M}A_{ij}w_j=T_i,
\tag{1.122}
$$

其中

$$
A_{ij}=\sum_{n=1}^{N}(x_n)^{i+j},\qquad T_i=\sum_{n=1}^{N}(x_n)^i t_n.
\tag{1.123}
$$

这里，下标 $i$ 或 $j$ 表示分量的索引，而 $(x)^i$ 表示 $x$ 的 $i$ 次幂。

**1.2（⋆）** 写出与式（1.122）类似的联立线性方程组，使式（1.4）所给正则化平方和误差函数最小的系数 $w_i$ 应满足该方程组。

**1.3（⋆⋆）** 假设有三个有颜色的盒子：$r$（红色）、$b$（蓝色）和 $g$（绿色）。盒子 $r$ 中有 3 个苹果、4 个橙子和 3 个青柠；盒子 $b$ 中有 1 个苹果、1 个橙子、没有青柠；盒子 $g$ 中有 3 个苹果、3 个橙子和 4 个青柠。以概率 $p(r)=0.2$、$p(b)=0.2$、$p(g)=0.6$ 随机选择一个盒子，再从盒中取出一个水果（盒中每个水果被选中的概率相同）。选到苹果的概率是多少？如果观察到所选水果实际上是橙子，那么它来自绿色盒子的概率是多少？

**1.4（⋆⋆）www** 考虑定义在连续变量 $x$ 上的概率密度 $p_x(x)$。假设通过 $x=g(y)$ 进行非线性变量变换，使密度按式（1.27）变换。对式（1.27）求导，证明：由于雅可比因子的存在，$y$ 的密度达到最大值的位置 $\widehat{y}$，通常并不与 $x$ 的密度达到最大值的位置 $\widehat{x}$ 满足简单的函数关系 $\widehat{x}=g(\widehat{y})$。这说明，与普通函数不同，概率密度的最大值位置依赖变量的选择。验证：在线性变换的情况下，最大值位置的变换方式与变量本身相同。

**1.5（⋆）** 利用定义（1.38），证明 $\operatorname{var}[f(x)]$ 满足式（1.39）。

<!-- pdf-page: 79 -->

**1.6（⋆）** 证明：如果两个变量 $x$ 和 $y$ 独立，它们的协方差为零。

**1.7（⋆⋆）www** 本题证明一元高斯分布的归一化条件（1.48）。为此，考虑积分

$$
I=\int_{-\infty}^{\infty}\exp\left(-\frac1{2\sigma^2}x^2\right)\,\mathrm{d}x.
\tag{1.124}
$$

计算时，先将它的平方写成

$$
I^2=\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}\exp\left(-\frac1{2\sigma^2}x^2-\frac1{2\sigma^2}y^2\right)\,\mathrm{d}x\,\mathrm{d}y.
\tag{1.125}
$$

现在从笛卡尔坐标 $(x,y)$ 变换到极坐标 $(r,\theta)$，然后代入 $u=r^2$。证明：对 $\theta$ 和 $u$ 积分，再将两边开平方，得到

$$
I=(2\pi\sigma^2)^{1/2}.
\tag{1.126}
$$

最后，利用这个结果证明高斯分布 $\mathcal{N}(x\mid\mu,\sigma^2)$ 已归一化。

**1.8（⋆⋆）www** 通过变量变换，验证式（1.46）给出的一元高斯分布满足式（1.49）。接着，对归一化条件

$$
\int_{-\infty}^{\infty}\mathcal{N}(x\mid\mu,\sigma^2)\,\mathrm{d}x=1
\tag{1.127}
$$

的两边关于 $\sigma^2$ 求导，验证高斯分布满足式（1.50）。最后证明式（1.51）成立。

**1.9（⋆）www** 证明：高斯分布（1.46）的众数（即最大值所在位置）为 $\mu$。类似地，证明多元高斯分布（1.52）的众数为 $\boldsymbol{\mu}$。

**1.10（⋆）www** 假设两个变量 $x$ 与 $z$ 在统计上独立。证明它们之和的均值和方差满足

$$
\mathbb{E}[x+z]=\mathbb{E}[x]+\mathbb{E}[z],
\tag{1.128}
$$

$$
\operatorname{var}[x+z]=\operatorname{var}[x]+\operatorname{var}[z].
\tag{1.129}
$$

**1.11（⋆）** 将对数似然函数（1.54）对 $\mu$ 和 $\sigma^2$ 的导数置为零，验证结果（1.55）和（1.56）。

<!-- pdf-page: 80 -->

**1.12（⋆⋆）www** 利用结果（1.49）和（1.50），证明

$$
\mathbb{E}[x_nx_m]=\mu^2+I_{nm}\sigma^2,
\tag{1.130}
$$

其中，$x_n$ 和 $x_m$ 表示从均值为 $\mu$、方差为 $\sigma^2$ 的高斯分布抽取的数据点；当 $n=m$ 时，$I_{nm}=1$，否则 $I_{nm}=0$。由此证明结果（1.57）和（1.58）。

**1.13（⋆）** 假设使用式（1.56）估计高斯分布的方差，但把最大似然估计 $\mu_{\mathrm{ML}}$ 换成均值的真实值 $\mu$。证明，这个估计量的期望等于真实方差 $\sigma^2$。

**1.14（⋆⋆）** 证明：任意元素为 $w_{ij}$ 的方阵，都可以写成 $w_{ij}=w_{ij}^{\mathrm S}+w_{ij}^{\mathrm A}$，其中 $w_{ij}^{\mathrm S}$ 和 $w_{ij}^{\mathrm A}$ 分别为对称矩阵与反对称矩阵，对所有 $i$、$j$ 满足 $w_{ij}^{\mathrm S}=w_{ji}^{\mathrm S}$ 和 $w_{ij}^{\mathrm A}=-w_{ji}^{\mathrm A}$。现在考虑 $D$ 维高阶多项式中的二阶项：

$$
\sum_{i=1}^{D}\sum_{j=1}^{D}w_{ij}x_ix_j.
\tag{1.131}
$$

证明

$$
\sum_{i=1}^{D}\sum_{j=1}^{D}w_{ij}x_ix_j=\sum_{i=1}^{D}\sum_{j=1}^{D}w_{ij}^{\mathrm S}x_ix_j,
\tag{1.132}
$$

即反对称矩阵的贡献为零。因此，不失一般性，可以选择系数矩阵 $w_{ij}$ 为对称矩阵，也就是说，这个矩阵的 $D^2$ 个元素不能全部独立选择。证明，矩阵 $w_{ij}^{\mathrm S}$ 中独立参数的数目为 $D(D+1)/2$。

**1.15（⋆⋆⋆）www** 本题和下一题考察多项式中独立参数的数目如何随多项式阶数 $M$ 和输入空间维数 $D$ 增长。首先将 $D$ 维多项式的第 $M$ 阶项写成

$$
\sum_{i_1=1}^{D}\sum_{i_2=1}^{D}\cdots\sum_{i_M=1}^{D}w_{i_1i_2\cdots i_M}x_{i_1}x_{i_2}\cdots x_{i_M}.
\tag{1.133}
$$

系数 $w_{i_1i_2\cdots i_M}$ 一共有 $D^M$ 个元素，但因子 $x_{i_1}x_{i_2}\cdots x_{i_M}$ 具有许多交换对称性，所以独立参数的数目远少于这个数。先证明，将第 $M$ 阶项改写为以下形式，就能消除系数的冗余：

$$
\sum_{i_1=1}^{D}\sum_{i_2=1}^{i_1}\cdots\sum_{i_M=1}^{i_{M-1}}\widetilde{w}_{i_1i_2\cdots i_M}x_{i_1}x_{i_2}\cdots x_{i_M}.
\tag{1.134}
$$

<!-- pdf-page: 81 -->

注意，不必明确写出系数 $\widetilde{w}$ 与系数 $w$ 之间的精确关系。利用这一结果，证明第 $M$ 阶项中独立参数的数目 $n(D,M)$ 满足以下递推关系：

$$
n(D,M)=\sum_{i=1}^{D}n(i,M-1).
\tag{1.135}
$$

接着用数学归纳法证明

$$
\sum_{i=1}^{D}\frac{(i+M-2)!}{(i-1)!\,(M-1)!}=\frac{(D+M-1)!}{(D-1)!\,M!}.
\tag{1.136}
$$

可以先利用 $0!=1$，证明 $D=1$、$M$ 任意时成立；再假设维数为 $D$ 时成立，验证维数为 $D+1$ 时也成立。最后，利用前两个结果和数学归纳法，证明

$$
n(D,M)=\frac{(D+M-1)!}{(D-1)!\,M!}.
\tag{1.137}
$$

为此，先与习题 1.14 的结果比较，证明 $M=2$、任意 $D\geqslant1$ 时该结果成立。然后结合式（1.135）和（1.136），证明如果它对阶数 $M-1$ 成立，那么对阶数 $M$ 也成立。

**1.16（⋆⋆⋆）** 在习题 1.15 中，我们证明了 $D$ 维多项式第 $M$ 阶项中独立参数数目的结果（1.135）。现在求从零阶直到第 $M$ 阶（包括第 $M$ 阶）所有项中独立参数总数 $N(D,M)$ 的表达式。首先证明 $N(D,M)$ 满足

$$
N(D,M)=\sum_{m=0}^{M}n(D,m),
\tag{1.138}
$$

其中 $n(D,m)$ 是第 $m$ 阶项中独立参数的数目。然后利用式（1.137）和数学归纳法，证明

$$
N(d,M)=\frac{(D+M)!}{D!\,M!}.
\tag{1.139}
$$

可以先证明 $M=0$、任意 $D\geqslant1$ 时成立；再假设阶数为 $M$ 时成立，进而证明阶数为 $M+1$ 时也成立。最后，利用大 $n$ 下如下形式的 Stirling 近似

$$
n!\simeq n^n e^{-n},
\tag{1.140}
$$

证明：当 $D\gg M$ 时，量 $N(D,M)$ 按 $D^M$ 增长；当 $M\gg D$ 时，它按 $M^D$ 增长。考虑 $D$ 维三次（$M=3$）多项式，分别数值计算（i）$D=10$ 和（ii）$D=100$ 时独立参数的总数，它们分别对应典型的小规模和中等规模机器学习应用。

<!-- pdf-page: 82 -->

**1.17（⋆⋆）www** 伽马函数（gamma function）定义为

$$
\Gamma(x)\equiv\int_0^{\infty}u^{x-1}e^{-u}\,\mathrm{d}u.
\tag{1.141}
$$

利用分部积分，证明关系 $\Gamma(x+1)=x\Gamma(x)$。再证明 $\Gamma(1)=1$，从而说明当 $x$ 为整数时，$\Gamma(x+1)=x!$。

**1.18（⋆⋆）www** 可以利用式（1.126），推导 $D$ 维空间中单位半径球的表面积 $S_D$ 与体积 $V_D$ 的表达式。为此，考虑通过从笛卡尔坐标变换到极坐标而得到的如下结果：

$$
\prod_{i=1}^{D}\int_{-\infty}^{\infty}e^{-x_i^2}\,\mathrm{d}x_i=S_D\int_0^{\infty}e^{-r^2}r^{D-1}\,\mathrm{d}r.
\tag{1.142}
$$

利用伽马函数定义（1.141）以及式（1.126），计算等式两边，从而证明

$$
S_D=\frac{2\pi^{D/2}}{\Gamma(D/2)}.
\tag{1.143}
$$

接着，将半径从 0 积分到 1，证明 $D$ 维单位球的体积为

$$
V_D=\frac{S_D}{D}.
\tag{1.144}
$$

最后，利用 $\Gamma(1)=1$ 和 $\Gamma(3/2)=\sqrt{\pi}/2$，证明式（1.143）与（1.144）在 $D=2$ 和 $D=3$ 时化为通常的表达式。

**1.19（⋆⋆）** 考虑 $D$ 维空间中半径为 $a$ 的球，以及与它同心、边长为 $2a$ 的超立方体，使球在超立方体各个面的中心处与其相切。利用习题 1.18 的结果，证明球体积与立方体体积之比为

$$
\frac{\text{球的体积}}{\text{立方体的体积}}=\frac{\pi^{D/2}}{D2^{D-1}\Gamma(D/2)}.
\tag{1.145}
$$

再利用在 $x\gg1$ 时成立的如下形式的 Stirling 公式

$$
\Gamma(x+1)\simeq(2\pi)^{1/2}e^{-x}x^{x+1/2},
\tag{1.146}
$$

证明当 $D\to\infty$ 时，比值（1.145）趋于零。再证明：从超立方体中心到某个顶点的距离，除以从中心到某个面的垂直距离，所得比值为 $\sqrt{D}$，因此当 $D\to\infty$ 时，它趋于无穷大。由这些结果可见，在高维空间中，立方体的大部分体积集中于数量众多的角部，而这些角部本身变成了很长的“尖刺”！

<!-- pdf-page: 83 -->

**1.20（⋆⋆）www** 本题考察高维空间中高斯分布的表现。考虑以下 $D$ 维高斯分布：

$$
p(\mathbf{x})=\frac1{(2\pi\sigma^2)^{D/2}}\exp\left(-\frac{\|\mathbf{x}\|^2}{2\sigma^2}\right).
\tag{1.147}
$$

我们希望求出极坐标下将方向变量积分消去后，关于半径的密度。为此，证明：在半径为 $r$、厚度为 $\epsilon$（$\epsilon\ll1$）的薄壳上积分概率密度，所得结果为 $p(r)\epsilon$，其中

$$
p(r)=\frac{S_Dr^{D-1}}{(2\pi\sigma^2)^{D/2}}\exp\left(-\frac{r^2}{2\sigma^2}\right),
\tag{1.148}
$$

这里 $S_D$ 为 $D$ 维单位球的表面积。证明函数 $p(r)$ 只有一个驻点，在 $D$ 很大时，其位置为 $\widehat{r}\simeq\sqrt{D}\sigma$。考察 $p(\widehat{r}+\epsilon)$，其中 $\epsilon\ll\widehat{r}$，证明当 $D$ 很大时，

$$
p(\widehat{r}+\epsilon)=p(\widehat{r})\exp\left(-\frac{3\epsilon^2}{2\sigma^2}\right).
\tag{1.149}
$$

这说明，$\widehat{r}$ 是径向概率密度的最大值位置，并且 $p(r)$ 离开 $\widehat{r}$ 处的最大值后，以 $\sigma$ 为长度尺度按指数衰减。前面已经看到，$D$ 很大时有 $\sigma\ll\widehat{r}$，因此大部分概率质量集中在半径很大的薄壳中。最后证明：概率密度 $p(\mathbf{x})$ 在原点处的值，是在半径 $\widehat{r}$ 处的值的 $\exp(D/2)$ 倍。因此，高维高斯分布中，大部分概率质量所在的半径，与高概率密度区域所在的半径不同。在后续章节考虑模型参数的贝叶斯推断时，高维空间分布的这一性质会带来重要影响。

**1.21（⋆⋆）** 考虑两个非负数 $a$、$b$。证明：如果 $a\leqslant b$，则 $a\leqslant(ab)^{1/2}$。利用这一结果，证明如果选择二分类问题的决策区域，使误分类概率最小，那么这一概率满足

$$
p(\mathrm{mistake})\leqslant\int\{p(\mathbf{x},\mathcal{C}_1)p(\mathbf{x},\mathcal{C}_2)\}^{1/2}\,\mathrm{d}\mathbf{x}.
\tag{1.150}
$$

**1.22（⋆）www** 给定元素为 $L_{kj}$ 的损失矩阵，如果对每个 $\mathbf{x}$ 选择使式（1.81）最小的类别，期望风险便达到最小。验证：当损失矩阵为 $L_{kj}=1-I_{kj}$，其中 $I_{kj}$ 为单位矩阵的元素时，这个准则就化为选择后验概率最大的类别。这种形式的损失矩阵有什么含义？

**1.23（⋆）** 在损失矩阵与各类别先验概率均为一般形式时，推导使期望损失最小的准则。

<!-- pdf-page: 84 -->

**1.24（⋆⋆）www** 考虑一个分类问题：当来自类别 $\mathcal{C}_k$ 的输入向量被判为类别 $\mathcal{C}_j$ 时，造成的损失由损失矩阵 $L_{kj}$ 给出；选择拒绝选项时造成的损失为 $\lambda$。求使期望损失最小的决策准则。验证：当损失矩阵为 $L_{kj}=1-I_{kj}$ 时，它化为第 1.5.3 节讨论的拒绝准则。$\lambda$ 与拒绝阈值 $\theta$ 有什么关系？

**1.25（⋆）www** 考虑将单一目标变量 $t$ 的平方损失函数（1.87），推广到由向量 $\mathbf{t}$ 描述的多个目标变量的情形：

$$
\mathbb{E}[L(\mathbf{t},\mathbf{y}(\mathbf{x}))]=\iint\|\mathbf{y}(\mathbf{x})-\mathbf{t}\|^2p(\mathbf{x},\mathbf{t})\,\mathrm{d}\mathbf{x}\,\mathrm{d}\mathbf{t}.
\tag{1.151}
$$

利用变分法，证明使这个期望损失最小的函数 $\mathbf{y}(\mathbf{x})$ 为 $\mathbf{y}(\mathbf{x})=\mathbb{E}_{\mathbf{t}}[\mathbf{t}\mid\mathbf{x}]$。证明：对于单一目标变量 $t$，这一结果化为式（1.89）。

**1.26（⋆）** 展开式（1.151）中的平方项，推导与式（1.90）类似的结果，从而证明：当目标变量为向量 $\mathbf{t}$ 时，使期望平方损失最小的函数 $\mathbf{y}(\mathbf{x})$，仍然由 $\mathbf{t}$ 的条件期望给出。

**1.27（⋆⋆）www** 考虑回归问题中由式（1.91）给出的 $L_q$ 损失函数的期望损失。写出使 $\mathbb{E}[L_q]$ 最小的 $y(\mathbf{x})$ 必须满足的条件。证明：当 $q=1$ 时，这个解表示条件中位数，即满足 $t<y(\mathbf{x})$ 的概率质量与 $t\geqslant y(\mathbf{x})$ 的概率质量相等的函数 $y(\mathbf{x})$。再证明：当 $q\to0$ 时，使期望 $L_q$ 损失最小的解由条件众数给出，即对于每个 $\mathbf{x}$，函数 $y(\mathbf{x})$ 都等于使 $p(t\mid\mathbf{x})$ 最大的 $t$ 值。

**1.28（⋆）** 第 1.6 节引入了熵 $h(x)$ 的概念，将它解释为观测到分布为 $p(x)$ 的随机变量 $x$ 的值时所获得的信息。我们看到，对于满足 $p(x,y)=p(x)p(y)$ 的独立变量 $x$ 与 $y$，熵函数具有可加性，即 $h(x,y)=h(x)+h(y)$。本题以函数 $h(p)$ 的形式推导 $h$ 与 $p$ 的关系。先证明 $h(p^2)=2h(p)$，再用归纳法证明 $h(p^n)=nh(p)$，其中 $n$ 为正整数。由此证明 $h(p^{n/m})=(n/m)h(p)$，其中 $m$ 也是正整数。这意味着，当 $x$ 为正有理数时，$h(p^x)=xh(p)$；再由连续性可知，当 $x$ 为正实数时也成立。最后证明，这意味着 $h(p)$ 必须具有 $h(p)\propto\ln p$ 的形式。

**1.29（⋆）www** 考虑具有 $M$ 个状态的离散随机变量 $x$，利用形式（1.115）的 Jensen 不等式，证明其分布 $p(x)$ 的熵满足 $\mathrm{H}[x]\leqslant\ln M$。

**1.30（⋆⋆）** 计算两个高斯分布 $p(x)=\mathcal{N}(x\mid\mu,\sigma^2)$ 和 $q(x)=\mathcal{N}(x\mid m,s^2)$ 之间的 Kullback–Leibler 散度（1.113）。

<!-- pdf-page: 85 -->

**表 1.3：** 习题 1.39 使用的两个二元变量 $x$ 与 $y$ 的联合分布 $p(x,y)$。

| $x\backslash y$ | $0$ | $1$ |
| --- | ---: | ---: |
| $0$ | $1/3$ | $1/3$ |
| $1$ | $0$ | $1/3$ |

**1.31（⋆⋆）www** 考虑具有联合分布 $p(\mathbf{x},\mathbf{y})$ 的两个变量 $\mathbf{x}$ 与 $\mathbf{y}$。证明它们的微分熵满足

$$
\mathrm{H}[\mathbf{x},\mathbf{y}]\leqslant\mathrm{H}[\mathbf{x}]+\mathrm{H}[\mathbf{y}],
\tag{1.152}
$$

且当且仅当 $\mathbf{x}$ 与 $\mathbf{y}$ 在统计上独立时取等号。

**1.32（⋆）** 考虑连续变量向量 $\mathbf{x}$，其分布为 $p(\mathbf{x})$，相应的熵为 $\mathrm{H}[\mathbf{x}]$。假设对 $\mathbf{x}$ 进行非奇异线性变换，得到新变量 $\mathbf{y}=\mathbf{A}\mathbf{x}$。证明相应的熵为 $\mathrm{H}[\mathbf{y}]=\mathrm{H}[\mathbf{x}]+\ln|\mathbf{A}|$，其中 $|\mathbf{A}|$ 表示 $\mathbf{A}$ 的行列式。

**1.33（⋆⋆）** 假设两个离散随机变量 $x$ 与 $y$ 之间的条件熵 $\mathrm{H}[y\mid x]$ 为零。证明：对于所有满足 $p(x)>0$ 的 $x$，变量 $y$ 必须是 $x$ 的函数；换言之，对于每个 $x$，只有一个 $y$ 值满足 $p(y\mid x)\ne0$。

**1.34（⋆⋆）www** 利用变分法，证明泛函（1.108）的驻点由式（1.108）给出。然后利用约束（1.105）、（1.106）和（1.107）消去拉格朗日乘子，从而证明最大熵解由高斯分布（1.109）给出。

**1.35（⋆）www** 利用结果（1.106）和（1.107），证明一元高斯分布（1.109）的熵由式（1.110）给出。

**1.36（⋆）** 严格凸函数定义为每条弦都位于函数曲线上方的函数。证明，这等价于函数的二阶导数为正。

**1.37（⋆）** 利用定义（1.111）和概率的乘积法则，证明结果（1.112）。

**1.38（⋆⋆）www** 利用数学归纳法，证明凸函数的不等式（1.114）蕴含结果（1.115）。

**1.39（⋆⋆⋆）** 考虑两个二元变量 $x$ 和 $y$，其联合分布如表 1.3 所示。

计算下列各量：

| | | |
| --- | --- | --- |
| （a）$\mathrm{H}[x]$ | （c）$\mathrm{H}[y\mid x]$ | （e）$\mathrm{H}[x,y]$ |
| （b）$\mathrm{H}[y]$ | （d）$\mathrm{H}[x\mid y]$ | （f）$\mathrm{I}[x,y]$ |

画图说明这些量之间的关系。

<!-- pdf-page: 86 -->

**1.40（⋆）** 令 $f(x)=\ln x$，应用 Jensen 不等式（1.115），证明一组实数的算术平均数不会小于其几何平均数。

**1.41（⋆）www** 利用概率的求和法则和乘积法则，证明互信息 $\mathrm{I}(\mathbf{x},\mathbf{y})$ 满足关系（1.121）。
