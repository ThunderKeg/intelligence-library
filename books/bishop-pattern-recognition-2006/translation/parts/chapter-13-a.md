# 第 13 章 序列数据

<aside class="chapter-guide"><strong>本章导读</strong><p>序列中的相邻观测往往相互关联。本章先用马尔可夫模型描述这种依赖，再引入随序列演化的潜在状态，分别讨论隐马尔可夫模型和线性动力系统，说明如何估计状态、学习参数以及预测后续观测。</p></aside>

<!-- pdf-page: 625 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-chapter-opening.png" alt="水纹背景上的第 13 章标题"><p class="figure-translation">Sequential Data → 序列数据。</p></figure>

到目前为止，本书主要关注由独立同分布（independent and identically distributed，i.i.d.）的数据点组成的集合。这个假设使我们能够将似然函数写为：在各个数据点处计算概率分布，再对所有数据点取乘积。然而，对许多应用来说，独立同分布并不是一个合适的假设。这里考虑这类数据集中尤为重要的一类，即序列数据。这类数据往往来自时间序列测量，例如某个地点连续各天的降雨量、某种货币每天的汇率，或语音识别中连续时间帧的声学特征。图 13.1 给出了一个语音数据的例子。序列数据也可能出现在时间序列以外的情境中，例如 DNA 链上的核苷酸碱基对序列，或英文句子中的字符序列。为方便起见，我们有时会把序列中的观测称为“过去”和“未来”的观测。不过，本章研究的模型同样适用于所有

<!-- pdf-page: 626 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-1.png" alt="读出 Bayes’ theorem 时的声谱图、波形以及对应的单词和音素时间分段"><figcaption>图 13.1：读出“Bayes’ theorem”（贝叶斯定理）时的声谱图示例，展示频谱系数的强度随时间索引的变化。</figcaption><p class="figure-translation">Frequency (Hz) → 频率（Hz）；Amplitude → 振幅；Time (sec) → 时间（秒）；Bayes’ → 贝叶斯；Theorem → 定理。</p></figure>

<!-- join-previous-paragraph-across-figures -->
形式的序列数据，而不只是时间序列。

区分平稳与非平稳的序列分布是有用的。在平稳情形下，数据随时间演化，但生成数据的分布保持不变。在更复杂的非平稳情形下，生成分布本身也随时间演化。这里主要讨论平稳情形。

在金融预测等许多应用中，我们希望根据之前的观测值预测时间序列中的下一个值。直观上，在预测未来值时，近期观测很可能比更早的历史观测包含更多信息。图 13.1 的例子表明，语音频谱的连续观测确实高度相关。此外，考虑未来观测对全部历史观测的一般依赖关系并不切实际，因为随着观测数量增加，这样的模型的复杂度会无限增长。因此，我们考虑马尔可夫模型（Markov model），假设对未来的预测除最近的观测外，与其他观测都

<!-- pdf-page: 627 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-2.png" alt="四个彼此没有连边的观测节点及后续省略号"><figcaption>图 13.2：对观测序列建模的最简单方法，是把各个观测视为相互独立，对应于一个没有连边的图。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
独立。

尽管这类模型便于计算，它们也有很强的局限性。通过引入潜变量，可以在保持计算可行的同时，得到更一般的框架，也就是状态空间模型（state space model）。与第 9 章和第 12 章一样，我们将看到，复杂模型可以由较简单的组成部分构建，特别是由指数族分布构建，并且很容易用概率图模型框架加以描述。这里主要讨论状态空间模型中最重要的两个例子：潜变量为离散变量的隐马尔可夫模型，以及潜变量为高斯变量的线性动力系统。这两类模型都由具有树结构、没有环的有向图描述，因此可以用和积算法高效地进行推断。

## 13.1 马尔可夫模型

处理序列数据的最简单方法，是直接忽略序列性，将观测视为独立同分布，对应于图 13.2。然而，这种方法无法利用数据中的序列模式，例如序列中相邻观测之间的相关性。举例来说，假设我们观测一个二值变量，用它表示某一天是否下雨。给定这个变量近期观测组成的时间序列，希望预测下一天是否下雨。如果把数据视为独立同分布，那么从数据中能够获得的唯一信息，就是下雨天的相对频率。不过，根据实际经验，天气往往表现出持续几天的变化趋势。因此，观测今天是否下雨，对于预测明天是否下雨有很大帮助。

要在概率模型中表达这种效应，需要放宽独立同分布的假设；最简单的方法之一，就是考虑马尔可夫模型。首先注意到，不失一般性，可以利用乘积规则将观测序列的联合分布写成

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_N)=\prod_{n=1}^{N}p(\mathbf{x}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}).
\tag{13.1}
$$

现在假设右侧的每个条件分布，除最近一次观测外，都与更早的观测无关，就得到一阶马尔可夫链（first-order Markov chain），其图模型如图 13.3 所示。这个模型下，

<!-- pdf-page: 628 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-3.png" alt="观测 x_1 至 x_4 依次相连的一阶马尔可夫链"><figcaption>图 13.3：观测 $\{\mathbf{x}_n\}$ 的一阶马尔可夫链，其中某个观测 $\mathbf{x}_n$ 的分布 $p(\mathbf{x}_n\mid\mathbf{x}_{n-1})$ 以前一个观测 $\mathbf{x}_{n-1}$ 的值为条件。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
$N$ 个观测组成的序列的联合分布为

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_N)=p(\mathbf{x}_1)\prod_{n=2}^{N}p(\mathbf{x}_n\mid\mathbf{x}_{n-1}).
\tag{13.2}
$$

根据 d 分离性质，给定截至时刻 $n$ 的全部观测时，观测 $\mathbf{x}_n$ 的条件分布为<span class="margin-reference">第 8.2 节</span>

$$
p(\mathbf{x}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})=p(\mathbf{x}_n\mid\mathbf{x}_{n-1})
\tag{13.3}
$$

从式（13.2）出发，利用概率的乘积规则直接计算，很容易验证这个结果。<span class="margin-reference">习题 13.1</span>因此，如果用这种模型预测序列中的下一个观测，预测分布将只依赖于紧接在它之前的那个观测值，而与所有更早的观测无关。

在这类模型的大多数应用中，定义模型的条件分布 $p(\mathbf{x}_n\mid\mathbf{x}_{n-1})$ 被约束为相同的分布，对应于时间序列平稳的假设。这种模型称为齐次马尔可夫链（homogeneous Markov chain）。例如，如果条件分布依赖于可调参数，而这些参数值可能从一组训练数据中推断得到，那么链中的所有条件分布都共享相同的参数值。

虽然这比独立模型更一般，但限制仍然很强。对于许多序列观测，我们预期连续多个观测中的数据趋势，会为预测下一个值提供重要信息。让更早的观测发挥作用的一种方法，是使用高阶马尔可夫链。如果还允许预测依赖于倒数第二个观测值，就得到二阶马尔可夫链，其图模型如图 13.4 所示。此时，联合分布为

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_N)=p(\mathbf{x}_1)p(\mathbf{x}_2\mid\mathbf{x}_1)\prod_{n=3}^{N}p(\mathbf{x}_n\mid\mathbf{x}_{n-1},\mathbf{x}_{n-2}).
\tag{13.4}
$$

同样，利用 d 分离或直接计算，可见给定 $\mathbf{x}_{n-1}$ 和 $\mathbf{x}_{n-2}$ 时，$\mathbf{x}_n$ 的条件分布与所有观测 $\mathbf{x}_1,\ldots,\mathbf{x}_{n-3}$ 都无关。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-4.png" alt="二阶马尔可夫链中每个观测节点接收前两个观测节点的有向边"><figcaption>图 13.4：二阶马尔可夫链，其中某个观测 $\mathbf{x}_n$ 的条件分布依赖于前两个观测 $\mathbf{x}_{n-1}$ 和 $\mathbf{x}_{n-2}$ 的值。</figcaption></figure>

<!-- pdf-page: 629 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-5.png" alt="状态空间模型：潜变量构成马尔可夫链，每个潜变量指向对应的观测变量"><figcaption>图 13.5：可以用潜变量的马尔可夫链表示序列数据，每个观测都以对应潜变量的状态为条件。这个重要的图结构是隐马尔可夫模型和线性动力系统的共同基础。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
此时，每个观测都受到之前两个观测的影响。类似地，可以扩展到 $M$ 阶马尔可夫链，其中某个变量的条件分布依赖于之前的 $M$ 个变量。不过，提高灵活性也有代价，因为模型中的参数数量现在大得多。假设观测是具有 $K$ 个状态的离散变量。那么在一阶马尔可夫链中，对于 $\mathbf{x}_{n-1}$ 的每个状态，需要一组 $K-1$ 个参数来指定条件分布 $p(\mathbf{x}_n\mid\mathbf{x}_{n-1})$，共有 $K$ 个状态，因此总计 $K(K-1)$ 个参数。现在假设把模型扩展为 $M$ 阶马尔可夫链，联合分布由条件分布 $p(\mathbf{x}_n\mid\mathbf{x}_{n-M},\ldots,\mathbf{x}_{n-1})$ 构成。如果变量是离散的，而且条件分布用一般的条件概率表表示，那么这类模型的参数数量为 $K^{M-1}(K-1)$。由于这个数量随 $M$ 指数增长，$M$ 较大时，这种方法往往难以实际使用。

对于连续变量，可以采用线性高斯条件分布：每个节点都服从高斯分布，其均值是父节点的线性函数。这称为自回归（autoregressive，AR）模型（Box et al.，1994；Thiesson et al.，2004）。另一种方法是使用神经网络等参数模型来表示 $p(\mathbf{x}_n\mid\mathbf{x}_{n-M},\ldots,\mathbf{x}_{n-1})$。这种技术有时称为抽头延迟线（tapped delay line），因为它相当于存储，也就是延迟观测变量的前 $M$ 个值，以预测下一个值。这样，参数数量可以远少于完全一般的模型，例如可能只随 $M$ 线性增长，不过代价是条件分布被限制在某个分布族内。

假设我们希望为序列建立一个模型，它不受任何阶的马尔可夫假设限制，同时又只需有限数量的自由参数。可以通过引入额外的潜变量来实现这一点，使简单组成部分构成丰富的模型族，就像第 9 章的混合分布和第 12 章的连续潜变量模型那样。对于每个观测 $\mathbf{x}_n$，引入相应的潜变量 $\mathbf{z}_n$；潜变量与观测变量的类型或维数可以不同。现在假设潜变量构成马尔可夫链，就得到称为状态空间模型的图结构，如图 13.5 所示。它满足一个关键的条件独立性质：给定 $\mathbf{z}_n$ 时，$\mathbf{z}_{n-1}$ 与 $\mathbf{z}_{n+1}$ 相互独立，即

$$
\mathbf{z}_{n+1}\mathbin{\perp\!\!\!\perp}\mathbf{z}_{n-1}\mid\mathbf{z}_n.
\tag{13.5}
$$

<!-- pdf-page: 630 -->

这个模型的联合分布为

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_N,\mathbf{z}_1,\ldots,\mathbf{z}_N)=p(\mathbf{z}_1)\left[\prod_{n=2}^{N}p(\mathbf{z}_n\mid\mathbf{z}_{n-1})\right]\prod_{n=1}^{N}p(\mathbf{x}_n\mid\mathbf{z}_n).
\tag{13.6}
$$

利用 d 分离判据，可见任意两个观测变量 $\mathbf{x}_n$ 和 $\mathbf{x}_m$ 之间，总有一条经由潜变量相连的路径，而且这条路径永远不会被阻断。因此，给定此前全部观测时，观测 $\mathbf{x}_{n+1}$ 的预测分布 $p(\mathbf{x}_{n+1}\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)$ 不具有任何条件独立性质，所以对 $\mathbf{x}_{n+1}$ 的预测依赖于所有先前观测。而观测变量并不满足任何阶的马尔可夫性质。本章后续各节将讨论如何计算预测分布。

这个图描述了两种重要的序列数据模型。如果潜变量是离散的，就得到隐马尔可夫模型（hidden Markov model，HMM；Elliott et al.，1995）。<span class="margin-reference">第 13.2 节</span>注意，HMM 中的观测变量可以是离散的，也可以是连续的，并且可以用各种不同的条件分布来建模。如果潜变量和观测变量都是高斯变量，且条件分布对父节点的依赖为线性高斯形式，就得到线性动力系统（linear dynamical system）。<span class="margin-reference">第 13.3 节</span>

## 13.2 隐马尔可夫模型

隐马尔可夫模型可以看作图 13.5 中状态空间模型的一个特例，其中潜变量为离散变量。不过，如果只考察模型的一个时间片，就会发现它对应于一个混合分布，其分量密度为 $p(\mathbf{x}\mid\mathbf{z})$。因此，也可以把它解释为混合模型的一种扩展：每个观测所对应的混合分量并非独立选择，而是依赖于前一个观测所选择的分量。HMM 广泛用于语音识别（Jelinek，1997；Rabiner 和 Juang，1993）、自然语言建模（Manning 和 Schütze，1999）、在线手写识别（Nag et al.，1986），以及蛋白质和 DNA 等生物序列的分析（Krogh et al.，1994；Durbin et al.，1998；Baldi 和 Brunak，2001）。

与标准混合模型一样，潜变量是离散的多项变量 $\mathbf{z}_n$，描述混合中的哪个分量负责生成相应的观测 $\mathbf{x}_n$。同样，采用第 9 章混合模型中使用的 $1$-of-$K$ 编码很方便。现在，允许 $\mathbf{z}_n$ 的概率分布通过条件分布 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$，依赖于前一个潜变量 $\mathbf{z}_{n-1}$ 的状态。由于潜变量是 $K$ 维二值变量，这个条件分布对应于一个数值表，记为 $\mathbf{A}$，其元素称为转移概率（transition probability）。它们定义为 $A_{jk}\equiv p(z_{nk}=1\mid z_{n-1,j}=1)$；由于它们是概率，满足 $0\leqslant A_{jk}\leqslant1$ 以及 $\sum_k A_{jk}=1$，所以矩阵 $\mathbf{A}$

<!-- pdf-page: 631 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-6.png" alt="三个彩色状态方框之间的九种转移，每条线标有转移矩阵 A 的相应元素"><figcaption>图 13.6：一个模型的状态转移图，其潜变量有三个可能状态，分别对应三个方框。黑线表示转移矩阵的元素 $A_{jk}$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
具有 $K(K-1)$ 个独立参数。于是，可以将条件分布明确写成

$$
p(\mathbf{z}_n\mid\mathbf{z}_{n-1},\mathbf{A})=\prod_{k=1}^{K}\prod_{j=1}^{K}A_{jk}^{z_{n-1,j}z_{nk}}.
\tag{13.7}
$$

初始潜在节点 $\mathbf{z}_1$ 比较特殊，因为它没有父节点。因此，它有一个边缘分布 $p(\mathbf{z}_1)$，用概率向量 $\boldsymbol{\pi}$ 表示，其元素为 $\pi_k\equiv p(z_{1k}=1)$，从而

$$
p(\mathbf{z}_1\mid\boldsymbol{\pi})=\prod_{k=1}^{K}\pi_k^{z_{1k}}
\tag{13.8}
$$

其中 $\sum_k\pi_k=1$。

有时会将各个状态画成状态转移图中的节点，以图示方式表示转移矩阵，图 13.6 给出了 $K=3$ 时的例子。注意，这不是概率图模型，因为节点表示的不是不同的变量，而是同一个变量的不同状态，所以我们用方框而不是圆圈表示这些状态。

有时，将图 13.6 这样的状态转移图沿时间展开会很有用。这样就得到潜在状态间转移的另一种表示，称为格图（lattice 或 trellis diagram）；图 13.7 给出了隐马尔可夫模型的这种表示。<span class="margin-reference">第 8.4.5 节</span>

定义观测变量的条件分布 $p(\mathbf{x}_n\mid\mathbf{z}_n,\phi)$ 后，概率模型就完整了，其中 $\phi$ 是控制这个分布的一组参数。这些条件分布称为发射概率（emission probability）。例如，如果 $\mathbf{x}$ 的元素是连续变量，可以采用式（9.11）形式的高斯分布；如果 $\mathbf{x}$ 是离散的，则可以使用条件概率表。由于 $\mathbf{x}_n$ 已经被观测到，对于给定的 $\phi$ 值，分布 $p(\mathbf{x}_n\mid\mathbf{z}_n,\phi)$ 就是一个由 $K$ 个数构成的向量，分别对应二值向量 $\mathbf{z}_n$ 的 $K$ 个可能状态。

<!-- pdf-page: 632 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-7.png" alt="把三个潜在状态的转移沿时间展开形成格图，列对应时刻，每两个相邻时刻间都有九条转移线"><figcaption>图 13.7：将图 13.6 的状态转移图沿时间展开，就得到潜在状态的格图（lattice 或 trellis）表示。图中的每一列对应一个潜变量 $\mathbf{z}_n$。</figcaption></figure>

可以将发射概率写为

$$
p(\mathbf{x}_n\mid\mathbf{z}_n,\phi)=\prod_{k=1}^{K}p(\mathbf{x}_n\mid\phi_k)^{z_{nk}}.
\tag{13.9}
$$

我们主要考虑齐次模型，其中控制潜变量的所有条件分布共享相同的参数 $\mathbf{A}$，而所有发射分布也共享相同的参数 $\phi$；推广到更一般的情形很直接。注意，独立同分布数据集的混合模型对应于一种特殊情况：参数 $A_{jk}$ 对所有 $j$ 值都相同，因此条件分布 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 与 $\mathbf{z}_{n-1}$ 无关。这相当于删去图 13.5 中图模型的水平连边。

于是，潜变量与观测变量的联合概率分布为

$$
p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})=p(\mathbf{z}_1\mid\boldsymbol{\pi})\left[\prod_{n=2}^{N}p(\mathbf{z}_n\mid\mathbf{z}_{n-1},\mathbf{A})\right]\prod_{m=1}^{N}p(\mathbf{x}_m\mid\mathbf{z}_m,\phi)
\tag{13.10}
$$

其中，$\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，$\mathbf{Z}=\{\mathbf{z}_1,\ldots,\mathbf{z}_N\}$，$\boldsymbol{\theta}=\{\boldsymbol{\pi},\mathbf{A},\phi\}$ 表示控制模型的参数集合。我们关于隐马尔可夫模型的大部分讨论，都不依赖于发射概率的具体选择。事实上，对于离散概率表、高斯分布和高斯混合等多种发射分布，这个模型都便于计算。也可以利用神经网络等判别式模型。<span class="margin-reference">习题 13.4</span>这些模型可以直接对发射密度 $p(\mathbf{x}\mid\mathbf{z})$ 建模，也可以提供 $p(\mathbf{z}\mid\mathbf{x})$ 的表示，再利用贝叶斯定理将其转换为所需的发射密度 $p(\mathbf{x}\mid\mathbf{z})$（Bishop et al.，2004）。

从生成的角度考虑隐马尔可夫模型，可以更好地理解它。回顾一下，要从高斯

<!-- pdf-page: 633 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-8.png" alt="三状态高斯发射模型的等密度轮廓，以及从这个隐马尔可夫模型生成的五十个相连的二维观测点"><figcaption>图 13.8：从隐马尔可夫模型采样的示例。潜变量 $\mathbf{z}$ 有 3 个状态，发射模型 $p(\mathbf{x}\mid\mathbf{z})$ 为高斯分布，其中 $\mathbf{x}$ 为二维变量。（a）潜变量三个状态各自对应的发射分布的等概率密度轮廓。（b）从隐马尔可夫模型抽取的 50 个样本点，按生成它们的分量着色，并用线连接连续观测。这里固定转移矩阵，使任意状态转移到另外每个状态的概率均为 5%，因而停留在同一状态的概率为 90%。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
混合中生成样本，首先按混合系数 $\pi_k$ 给出的概率随机选择一个分量，再从相应的高斯分量生成样本向量 $\mathbf{x}$。重复这个过程 $N$ 次，就得到包含 $N$ 个独立样本的数据集。对于隐马尔可夫模型，这一过程作如下修改。首先，按照参数 $\pi_k$ 控制的概率，选择初始潜变量 $\mathbf{z}_1$，再对相应的观测 $\mathbf{x}_1$ 采样。然后利用已经实例化的 $\mathbf{z}_1$ 值，根据转移概率 $p(\mathbf{z}_2\mid\mathbf{z}_1)$ 选择变量 $\mathbf{z}_2$ 的状态。例如，假设 $\mathbf{z}_1$ 的样本对应状态 $j$，那么就以概率 $A_{jk}$ 选择 $\mathbf{z}_2$ 的状态 $k$，其中 $k=1,\ldots,K$。一旦知道 $\mathbf{z}_2$，就可以抽取 $\mathbf{x}_2$ 的样本，并对下一个潜变量 $\mathbf{z}_3$ 采样，依此类推。这是有向图模型的祖先采样的一个例子。<span class="margin-reference">第 8.1.2 节</span>例如，如果模型中的对角转移元素 $A_{kk}$ 远大于非对角元素，那么典型数据序列中会有很长一段连续的点由同一个分量生成，而从一个分量转移到另一个分量的情况较少。图 13.8 展示了从隐马尔可夫模型生成样本的过程。

标准 HMM 模型有许多变体，例如可以通过约束转移矩阵 $\mathbf{A}$ 的形式来得到这些变体（Rabiner，1989）。这里介绍一种在实践中特别重要的模型，称为从左到右的 HMM（left-to-right HMM）：当 $k<j$ 时，将 $\mathbf{A}$ 的元素 $A_{jk}$ 设为零，就得到这种模型，如图 13.9 的

<!-- pdf-page: 634 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-9.png" alt="三个状态按从左到右方向转移，也可停留在本状态，但没有向左返回的转移"><figcaption>图 13.9：一个三状态、从左到右的隐马尔可夫模型的状态转移图。注意，一旦离开某个状态，以后就无法再次进入该状态。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
三状态 HMM 状态转移图所示。对于这类模型，通常还会修改 $p(\mathbf{z}_1)$ 的初始状态概率，使 $p(z_{11})=1$，并且对 $j\neq1$ 有 $p(z_{1j})=0$；也就是说，每个序列都被约束为从状态 $j=1$ 开始。还可以进一步约束转移矩阵，以保证状态索引不会发生过大的变化：当 $k>j+\Delta$ 时，令 $A_{jk}=0$。图 13.10 用格图展示了这种模型。

隐马尔可夫模型的许多应用，例如语音识别和在线字符识别，都使用从左到右的结构。作为这种模型的例子，考虑手写数字的一个应用。这里使用在线数据，即每个数字由笔的轨迹随时间变化的函数表示，具体形式是一串笔坐标；这与附录 A 讨论的离线数字数据不同，后者由笔迹的静态二维像素图像组成。图 13.11 给出了在线数字的例子。这里用包含 45 个数字“2”的数据子集训练一个隐马尔可夫模型。模型有 $K=16$ 个状态，每个状态都能生成一条长度固定、角度取 16 个可能值之一的线段。因此，发射分布就是一个 $16\times16$ 的概率表，给出每个状态索引下各个允许角度值的概率。除了保持状态索引 $k$ 不变或将其增加 $1$ 的转移之外，所有转移概率都设为零；模型参数通过 25 轮 EM 迭代进行优化。按生成方式运行训练得到的模型，可以加深对它的理解，如图 13.11 所示。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-10.png" alt="三状态从左到右 HMM 的格图，每次转移只能留在同一行或向下一行前进"><figcaption>图 13.10：三状态、从左到右的 HMM 的格图，每次转移允许状态索引 $k$ 最多增加 $1$。</figcaption></figure>

<!-- pdf-page: 635 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-11.png" alt="上排三个真实在线手写数字 2，下排三个从训练后的隐马尔可夫模型生成的数字 2"><figcaption>图 13.11：上排：在线手写数字的例子。下排：从一个从左到右的隐马尔可夫模型按生成方式采样得到的合成数字，该模型在包含 45 个手写数字的数据集上训练。</figcaption></figure>

隐马尔可夫模型一个很强的性质，是能够对时间轴的局部扭曲，即压缩与拉伸，表现出一定程度的不变性。为理解这一点，考虑在线手写数字例子中数字“2”的书写方式。一个典型的数字由在尖点处相连的两个不同部分组成。第一部分从左上方开始，以一条大弧线向下延伸，到达左下方的尖点或环；随后第二部分以近似直线的笔画结束于右下方。书写风格的自然变化会使这两个部分的相对大小发生变化，从而使尖点或环在时间序列中的位置改变。从生成的角度看，隐马尔可夫模型可以通过改变转移到同一状态与转移到下一状态的次数来容纳这类变化。不过，如果以相反顺序书写数字“2”，即从右下方开始、在左上方结束，那么即使笔尖坐标与训练集中的某个例子完全相同，这些观测在模型下的概率也会极小。在语音识别中，时间轴的扭曲与语速的自然变化有关；隐马尔可夫模型同样能够容纳这种变形，而不会对它施加过重的惩罚。

### 13.2.1 HMM 的最大似然

如果已经观测到数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，就可以用最大似然方法确定 HMM 的参数。对联合分布（13.10）中的潜变量进行边缘化，就得到似然函数

$$
p(\mathbf{X}\mid\boldsymbol{\theta})=\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{13.11}
$$

与第 9 章讨论的混合分布不同，联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 不能按 $n$ 因子化，所以不能简单地独立处理对各个 $\mathbf{z}_n$ 的求和。也不能显式执行这些求和，因为共有 $N$ 个变量需要求和，每个变量有 $K$ 个状态，总计会产生 $K^N$ 项。因此，求和项的数量会

<!-- pdf-page: 636 -->

<!-- join-previous-paragraph -->
随链的长度指数增长。实际上，式（13.11）的求和相当于对图 13.7 格图中数量呈指数增长的所有路径求和。

在考虑图 8.32 中简单变量链的推断问题时，我们已经遇到过类似困难。当时利用图的条件独立性质，重新安排求和顺序，得到了一种计算代价随链长线性增长而非指数增长的算法。我们将对隐马尔可夫模型采用类似技术。

似然函数表达式（13.11）的另一个困难在于，它对应于混合分布的推广，是对潜变量不同取值下的发射模型求和。因此，直接极大化似然函数会产生没有闭式解的复杂表达式，简单混合模型也是如此；回顾一下，独立同分布数据的混合模型是 HMM 的一个特例。<span class="margin-reference">第 9.2 节</span>

因此，我们转向期望最大化算法，为极大化隐马尔可夫模型的似然函数寻找一个高效框架。EM 算法从某组初始模型参数出发，将它记为 $\boldsymbol{\theta}^{\mathrm{old}}$。在 E 步中，用这些参数值求潜变量的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$。然后用这个后验分布，计算完整数据似然函数的对数的期望，将其视为参数 $\boldsymbol{\theta}$ 的函数，得到函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$，定义为

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{13.12}
$$

此时，引入一些记号会比较方便。用 $\gamma(\mathbf{z}_n)$ 表示潜变量 $\mathbf{z}_n$ 的边缘后验分布，用 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$ 表示两个连续潜变量的联合后验分布，即

$$
\gamma(\mathbf{z}_n)=p(\mathbf{z}_n\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})
\tag{13.13}
$$

$$
\xi(\mathbf{z}_{n-1},\mathbf{z}_n)=p(\mathbf{z}_{n-1},\mathbf{z}_n\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}}).
\tag{13.14}
$$

对于每个 $n$ 值，可以用一组和为 $1$ 的 $K$ 个非负数来存储 $\gamma(\mathbf{z}_n)$；类似地，可以用一个元素非负、总和也为 $1$ 的 $K\times K$ 矩阵来存储 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$。还将用 $\gamma(z_{nk})$ 表示 $z_{nk}=1$ 的条件概率，对 $\xi(z_{n-1,j},z_{nk})$ 和后面引入的其他概率变量也采用类似记法。因为二值随机变量的期望就是它取值为 $1$ 的概率，所以有

$$
\gamma(z_{nk})=\mathbb{E}[z_{nk}]=\sum_{\mathbf{z}}\gamma(\mathbf{z})z_{nk}
\tag{13.15}
$$

$$
\xi(z_{n-1,j},z_{nk})=\mathbb{E}[z_{n-1,j}z_{nk}]=\sum_{\mathbf{z}}\gamma(\mathbf{z})z_{n-1,j}z_{nk}.
\tag{13.16}
$$

如果把式（13.10）给出的联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 代入式（13.12），

<!-- pdf-page: 637 -->

<!-- join-previous-paragraph -->
并利用 $\gamma$ 和 $\xi$ 的定义，就得到

$$
\begin{aligned}
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})&=\sum_{k=1}^{K}\gamma(z_{1k})\ln\pi_k+\sum_{n=2}^{N}\sum_{j=1}^{K}\sum_{k=1}^{K}\xi(z_{n-1,j},z_{nk})\ln A_{jk}\\
&\quad+\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\ln p(\mathbf{x}_n\mid\phi_k).
\end{aligned}
\tag{13.17}
$$

E 步的目标是高效地计算 $\gamma(\mathbf{z}_n)$ 和 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$，稍后将详细讨论。

在 M 步中，我们将 $\gamma(\mathbf{z}_n)$ 和 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$ 视为常数，对参数 $\boldsymbol{\theta}=\{\boldsymbol{\pi},\mathbf{A},\phi\}$ 极大化 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$。引入适当的拉格朗日乘子，很容易完成关于 $\boldsymbol{\pi}$ 和 $\mathbf{A}$ 的极大化，结果为<span class="margin-reference">习题 13.5</span>

$$
\pi_k=\frac{\gamma(z_{1k})}{\displaystyle\sum_{j=1}^{K}\gamma(z_{1j})}
\tag{13.18}
$$

$$
A_{jk}=\frac{\displaystyle\sum_{n=2}^{N}\xi(z_{n-1,j},z_{nk})}{\displaystyle\sum_{l=1}^{K}\sum_{n=2}^{N}\xi(z_{n-1,j},z_{nl})}.
\tag{13.19}
$$

EM 算法需要为 $\boldsymbol{\pi}$ 和 $\mathbf{A}$ 选择初始值；这些值当然必须满足其概率解释所要求的求和约束。注意，$\boldsymbol{\pi}$ 或 $\mathbf{A}$ 中任何初始时设为零的元素，在后续 EM 更新中都会保持为零。<span class="margin-reference">习题 13.6</span>一种典型的初始化方法，是在满足求和约束和非负约束的前提下，为这些参数随机选取起始值。注意，对于从左到右的模型，除了在选择 $A_{jk}$ 的初始值时将相应元素设为零，无须对 EM 的结果作任何特殊修改，因为这些元素会始终保持为零。

要对 $\phi_k$ 极大化 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$，注意到式（13.17）中只有最后一项依赖于 $\phi_k$。此外，这一项与独立同分布数据的标准混合分布中，相应函数的依赖于数据的那一项具有完全相同的形式；对于高斯混合，将它与式（9.40）比较即可看出。在这里，$\gamma(z_{nk})$ 起到责任度的作用。如果不同分量的参数 $\phi_k$ 相互独立，那么这一项就分解为一个和式，每个 $k$ 值对应一项，并且各项可以独立极大化。于是，只需极大化发射密度 $p(\mathbf{x}\mid\phi_k)$ 的加权对数似然函数，权重为 $\gamma(z_{nk})$。这里假定这种极大化能够高效完成。例如，对于

<!-- pdf-page: 638 -->

<!-- join-previous-paragraph -->
高斯发射密度，有 $p(\mathbf{x}\mid\phi_k)=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$，极大化函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 就得到

$$
\boldsymbol{\mu}_k=\frac{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})\mathbf{x}_n}{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})}
\tag{13.20}
$$

$$
\boldsymbol{\Sigma}_k=\frac{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})(\mathbf{x}_n-\boldsymbol{\mu}_k)(\mathbf{x}_n-\boldsymbol{\mu}_k)^{\mathrm{T}}}{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})}.
\tag{13.21}
$$

如果观测变量是离散的多项变量，观测的条件分布具有如下形式

$$
p(\mathbf{x}\mid\mathbf{z})=\prod_{i=1}^{D}\prod_{k=1}^{K}\mu_{ik}^{x_i z_k}
\tag{13.22}
$$

相应的 M 步方程为<span class="margin-reference">习题 13.8</span>

$$
\mu_{ik}=\frac{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})x_{ni}}{\displaystyle\sum_{n=1}^{N}\gamma(z_{nk})}.
\tag{13.23}
$$

对于伯努利观测变量，也有类似的结果。

EM 算法需要给定发射分布参数的初始值。一种设置方法是，先把数据视为独立同分布，用最大似然方法拟合发射密度，再用得到的值初始化 EM 的参数。

### 13.2.2 前向—后向算法

接下来寻找一种高效计算 $\gamma(z_{nk})$ 和 $\xi(z_{n-1,j},z_{nk})$ 的方法，这对应于 EM 算法的 E 步。图 13.5 中隐马尔可夫模型的图是一棵树，因此我们知道，可以利用两阶段的消息传递算法，高效地得到潜变量的后验分布。<span class="margin-reference">第 8.4 节</span>在隐马尔可夫模型的具体情境中，它称为前向—后向算法（forward-backward algorithm；Rabiner，1989），也称为 Baum–Welch 算法（Baum，1972）。事实上，根据沿链传递的消息的具体形式，

<!-- pdf-page: 639 -->

<!-- join-previous-paragraph -->
这个基本算法有几个变体，它们都能得到精确的边缘分布（Jordan，2007）。我们主要讨论其中使用最广泛的一种，称为 alpha-beta 算法。

前向—后向算法本身具有很高的实用价值，同时也很好地展示了前面各章介绍的许多概念。因此，本节先“按常规”推导前向—后向方程：利用概率的求和规则和乘积规则，以及从相应图模型中通过 d 分离得到的条件独立性质。然后，在第 13.2.3 节将看到，前向—后向算法可以作为第 8.4.4 节介绍的和积算法的一个具体例子，非常简单地推导出来。

需要强调的是，计算潜变量的后验分布并不依赖于发射密度 $p(\mathbf{x}\mid\mathbf{z})$ 的形式，也不依赖于观测变量是连续的还是离散的。我们只需要知道每个 $n$ 下，$\mathbf{z}_n$ 各个取值对应的 $p(\mathbf{x}_n\mid\mathbf{z}_n)$。另外，在本节和下一节中，将不再显式写出对模型参数 $\boldsymbol{\theta}^{\mathrm{old}}$ 的依赖，因为这些参数始终固定不变。

首先写出以下条件独立性质（Jordan，2007）：

$$
\begin{aligned}
p(\mathbf{X}\mid\mathbf{z}_n)&=p(\mathbf{x}_1,\ldots,\mathbf{x}_n\mid\mathbf{z}_n)\\
&\quad p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)
\end{aligned}
\tag{13.24}
$$

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{x}_n,\mathbf{z}_n)=p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_n)
\tag{13.25}
$$

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_{n-1},\mathbf{z}_n)=p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_{n-1})
\tag{13.26}
$$

$$
p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n,\mathbf{z}_{n+1})=p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_{n+1})
\tag{13.27}
$$

$$
p(\mathbf{x}_{n+2},\ldots,\mathbf{x}_N\mid\mathbf{z}_{n+1},\mathbf{x}_{n+1})=p(\mathbf{x}_{n+2},\ldots,\mathbf{x}_N\mid\mathbf{z}_{n+1})
\tag{13.28}
$$

$$
\begin{aligned}
p(\mathbf{X}\mid\mathbf{z}_{n-1},\mathbf{z}_n)&=p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_{n-1})\\
&\quad p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)
\end{aligned}
\tag{13.29}
$$

$$
p(\mathbf{x}_{N+1}\mid\mathbf{X},\mathbf{z}_{N+1})=p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})
\tag{13.30}
$$

$$
p(\mathbf{z}_{N+1}\mid\mathbf{z}_N,\mathbf{X})=p(\mathbf{z}_{N+1}\mid\mathbf{z}_N)
\tag{13.31}
$$

其中 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$。用 d 分离最容易证明这些关系。例如，对于第一个结果，注意到从节点 $\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}$ 中任何一个到节点 $\mathbf{x}_n$ 的每条路径，都经过已观测的节点 $\mathbf{z}_n$。由于这些路径在该处都是首尾相接的，条件独立性质必然成立。读者应花一点时间逐一验证这些性质，作为应用 d 分离的练习。也可以从隐马尔可夫模型的联合分布出发，利用概率的求和规则和乘积规则直接证明这些关系，不过需要更多推导。<span class="margin-reference">习题 13.10</span>

先来计算 $\gamma(z_{nk})$。回顾一下，对于离散多项随机变量，其中一个分量的期望值，就是该分量取值为 $1$ 的概率。因此，我们希望求出给定观测数据集 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 时，$\mathbf{z}_n$ 的后验分布 $p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_N)$。它

<!-- pdf-page: 640 -->

<!-- join-previous-paragraph -->
表示一个长度为 $K$ 的向量，各元素对应于 $z_{nk}$ 的期望值。利用贝叶斯定理，有

$$
\gamma(\mathbf{z}_n)=p(\mathbf{z}_n\mid\mathbf{X})=\frac{p(\mathbf{X}\mid\mathbf{z}_n)p(\mathbf{z}_n)}{p(\mathbf{X})}.
\tag{13.32}
$$

注意，分母 $p(\mathbf{X})$ 隐含地以 HMM 的参数 $\boldsymbol{\theta}^{\mathrm{old}}$ 为条件，因此它表示似然函数。利用条件独立性质（13.24）以及概率的乘积规则，得到

$$
\gamma(\mathbf{z}_n)=\frac{p(\mathbf{x}_1,\ldots,\mathbf{x}_n,\mathbf{z}_n)p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)}{p(\mathbf{X})}=\frac{\alpha(\mathbf{z}_n)\beta(\mathbf{z}_n)}{p(\mathbf{X})}
\tag{13.33}
$$

其中定义

$$
\alpha(\mathbf{z}_n)\equiv p(\mathbf{x}_1,\ldots,\mathbf{x}_n,\mathbf{z}_n)
\tag{13.34}
$$

$$
\beta(\mathbf{z}_n)\equiv p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n).
\tag{13.35}
$$

$\alpha(\mathbf{z}_n)$ 表示观测到截至时刻 $n$ 的所有给定数据以及 $\mathbf{z}_n$ 的值的联合概率；而 $\beta(\mathbf{z}_n)$ 表示给定 $\mathbf{z}_n$ 的值时，从时刻 $n+1$ 到 $N$ 的全部未来数据的条件概率。同样，$\alpha(\mathbf{z}_n)$ 和 $\beta(\mathbf{z}_n)$ 各表示一组 $K$ 个数，分别对应于采用 $1$-of-$K$ 编码的二值向量 $\mathbf{z}_n$ 的各个可能取值。用记号 $\alpha(z_{nk})$ 表示 $z_{nk}=1$ 时 $\alpha(\mathbf{z}_n)$ 的值，$\beta(z_{nk})$ 也有类似解释。

现在推导能够高效计算 $\alpha(\mathbf{z}_n)$ 和 $\beta(\mathbf{z}_n)$ 的递推关系。我们仍然利用条件独立性质，特别是式（13.25）和（13.26），再结合求和规则与乘积规则，将 $\alpha(\mathbf{z}_n)$ 用 $\alpha(\mathbf{z}_{n-1})$ 表示如下：

$$
\begin{aligned}
\alpha(\mathbf{z}_n)&=p(\mathbf{x}_1,\ldots,\mathbf{x}_n,\mathbf{z}_n)\\
&=p(\mathbf{x}_1,\ldots,\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n)\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_n)p(\mathbf{z}_n)\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1},\mathbf{z}_n)\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1},\mathbf{z}_{n-1},\mathbf{z}_n)\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1},\mathbf{z}_n\mid\mathbf{z}_{n-1})p(\mathbf{z}_{n-1})\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_{n-1})p(\mathbf{z}_n\mid\mathbf{z}_{n-1})p(\mathbf{z}_{n-1})\\
&=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1},\mathbf{z}_{n-1})p(\mathbf{z}_n\mid\mathbf{z}_{n-1})
\end{aligned}
$$

利用 $\alpha(\mathbf{z}_n)$ 的定义（13.34），就得到

$$
\alpha(\mathbf{z}_n)=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}\alpha(\mathbf{z}_{n-1})p(\mathbf{z}_n\mid\mathbf{z}_{n-1}).
\tag{13.36}
$$

<!-- pdf-page: 641 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-12.png" alt="前向递推的局部格图，前一时刻的三个 alpha 值通过转移权重汇入当前第一状态，再乘发射概率"><figcaption>图 13.12：计算 $\alpha$ 变量的前向递推（13.36）。在这段格图中，取第 $n-1$ 步 $\alpha(\mathbf{z}_{n-1})$ 的各元素 $\alpha(z_{n-1,j})$，以 $A_{j1}$ 为权重求和，再乘上数据贡献 $p(\mathbf{x}_n\mid z_{n1})$，就得到 $\alpha(z_{n1})$；权重 $A_{j1}$ 对应于 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 的值。</figcaption></figure>

值得仔细考察一下这个递推关系。注意，求和中有 $K$ 项，而对 $\mathbf{z}_n$ 的每个可能值都要计算右侧表达式，共 $K$ 次，所以 $\alpha$ 递推每一步的计算代价为 $O(K^2)$。图 13.12 用格图展示了 $\alpha(\mathbf{z}_n)$ 的前向递推方程。

要启动这个递推，需要以下初始条件：

$$
\alpha(\mathbf{z}_1)=p(\mathbf{x}_1,\mathbf{z}_1)=p(\mathbf{z}_1)p(\mathbf{x}_1\mid\mathbf{z}_1)=\prod_{k=1}^{K}\{\pi_k p(\mathbf{x}_1\mid\phi_k)\}^{z_{1k}}
\tag{13.37}
$$

它说明，对于 $k=1,\ldots,K$，$\alpha(z_{1k})$ 的值为 $\pi_k p(\mathbf{x}_1\mid\phi_k)$。从链的第一个节点出发，就可以沿链依次计算每个潜在节点的 $\alpha(\mathbf{z}_n)$。由于递推的每一步都涉及与一个 $K\times K$ 矩阵相乘，所以对整条链计算这些量的总代价为 $O(K^2N)$。

类似地，利用条件独立性质（13.27）和（13.28），可以求出 $\beta(\mathbf{z}_n)$ 的递推关系：

$$
\begin{aligned}
\beta(\mathbf{z}_n)&=p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)\\
&=\sum_{\mathbf{z}_{n+1}}p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N,\mathbf{z}_{n+1}\mid\mathbf{z}_n)\\
&=\sum_{\mathbf{z}_{n+1}}p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n,\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)\\
&=\sum_{\mathbf{z}_{n+1}}p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)\\
&=\sum_{\mathbf{z}_{n+1}}p(\mathbf{x}_{n+2},\ldots,\mathbf{x}_N\mid\mathbf{z}_{n+1})p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n).
\end{aligned}
$$

<!-- pdf-page: 642 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-13.png" alt="后向递推的局部格图，下一时刻的三个 beta 值分别结合转移权重与发射密度，汇入当前第一状态"><figcaption>图 13.13：计算 $\beta$ 变量的后向递推（13.38）。在这段格图中，取第 $n+1$ 步 $\beta(\mathbf{z}_{n+1})$ 的各分量 $\beta(z_{n+1,k})$，加权求和就得到 $\beta(z_{n1})$；权重是 $A_{1k}$ 与对应发射密度值 $p(\mathbf{x}_n\mid z_{n+1,k})$ 的乘积，其中 $A_{1k}$ 对应于 $p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)$ 的值。</figcaption></figure>

利用 $\beta(\mathbf{z}_n)$ 的定义（13.35），得到

$$
\beta(\mathbf{z}_n)=\sum_{\mathbf{z}_{n+1}}\beta(\mathbf{z}_{n+1})p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n).
\tag{13.38}
$$

注意，这里得到的是一个后向消息传递算法，用 $\beta(\mathbf{z}_{n+1})$ 计算 $\beta(\mathbf{z}_n)$。每一步都先通过发射概率 $p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})$ 纳入观测 $\mathbf{x}_{n+1}$ 的影响，再乘上转移矩阵 $p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)$，然后将 $\mathbf{z}_{n+1}$ 边缘化掉。图 13.13 展示了这一过程。

同样，需要递推的起始条件，即 $\beta(\mathbf{z}_N)$ 的值。在式（13.33）中令 $n=N$，再用定义（13.34）替换 $\alpha(\mathbf{z}_N)$，得到

$$
p(\mathbf{z}_N\mid\mathbf{X})=\frac{p(\mathbf{X},\mathbf{z}_N)\beta(\mathbf{z}_N)}{p(\mathbf{X})}
\tag{13.39}
$$

可见，只要对 $\mathbf{z}_N$ 的所有取值都令 $\beta(\mathbf{z}_N)=1$，这个式子就成立。

在 M 步方程中，$p(\mathbf{X})$ 会约掉。例如，式（13.20）给出的 $\boldsymbol{\mu}_k$ 的 M 步方程可以写成

$$
\boldsymbol{\mu}_k=\frac{\displaystyle\sum_{n=1}^{n}\gamma(z_{nk})\mathbf{x}_n}{\displaystyle\sum_{n=1}^{n}\gamma(z_{nk})}=\frac{\displaystyle\sum_{n=1}^{n}\alpha(z_{nk})\beta(z_{nk})\mathbf{x}_n}{\displaystyle\sum_{n=1}^{n}\alpha(z_{nk})\beta(z_{nk})}.
\tag{13.40}
$$

不过，$p(\mathbf{X})$ 表示似然函数，通常希望在 EM 优化过程中监测它的值，因此能够计算它仍然很有用。对式（13.33）两边关于 $\mathbf{z}_n$ 求和，并利用左侧是归一化分布这一事实，得到

$$
p(\mathbf{X})=\sum_{\mathbf{z}_n}\alpha(\mathbf{z}_n)\beta(\mathbf{z}_n).
\tag{13.41}
$$

<!-- pdf-page: 643 -->

因此，可以选择任意方便的 $n$ 值，通过计算这个和式来求似然函数。例如，如果只想计算似然函数，可以从链的起点到终点运行 $\alpha$ 递推，再令 $n=N$ 使用这个结果，并利用 $\beta(\mathbf{z}_N)$ 是全 $1$ 向量这一事实。此时不需要进行 $\beta$ 递推，只需

$$
p(\mathbf{X})=\sum_{\mathbf{z}_N}\alpha(\mathbf{z}_N).
\tag{13.42}
$$

下面解释一下 $p(\mathbf{X})$ 的这个结果。回顾一下，计算似然时，应取联合分布 $p(\mathbf{X},\mathbf{Z})$，对 $\mathbf{Z}$ 的所有可能值求和。每个这样的取值，都为每个时间步指定了一个隐状态；换言之，求和中的每一项都是穿过格图的一条路径，而这样的路径数量呈指数增长。把似然函数写成式（13.42），相当于交换求和与乘法的顺序，从而将计算代价从随链长指数增长降为线性增长。在每个时间步 $n$，对经过各状态 $z_{nk}$ 的所有路径的贡献求和，得到中间量 $\alpha(\mathbf{z}_n)$。

接下来考虑计算 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$，它对应于 $(\mathbf{z}_{n-1},\mathbf{z}_n)$ 的 $K\times K$ 种取值各自的条件概率 $p(\mathbf{z}_{n-1},\mathbf{z}_n\mid\mathbf{X})$。利用 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$ 的定义，并应用贝叶斯定理，有

$$
\begin{aligned}
\xi(\mathbf{z}_{n-1},\mathbf{z}_n)&=p(\mathbf{z}_{n-1},\mathbf{z}_n\mid\mathbf{X})\\
&=\frac{p(\mathbf{X}\mid\mathbf{z}_{n-1},\mathbf{z}_n)p(\mathbf{z}_{n-1},\mathbf{z}_n)}{p(\mathbf{X})}\\
&=\frac{p(\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}\mid\mathbf{z}_{n-1})p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{z}_{n-1})p(\mathbf{z}_{n-1})}{p(\mathbf{X})}\\
&=\frac{\alpha(\mathbf{z}_{n-1})p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{z}_{n-1})\beta(\mathbf{z}_n)}{p(\mathbf{X})}
\end{aligned}
\tag{13.43}
$$

其中利用了条件独立性质（13.29），以及式（13.34）和（13.35）中 $\alpha(\mathbf{z}_n)$ 与 $\beta(\mathbf{z}_n)$ 的定义。因此，可以直接利用 $\alpha$ 和 $\beta$ 递推的结果计算 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$。

下面归纳用 EM 算法训练隐马尔可夫模型所需的步骤。首先选择初始参数 $\boldsymbol{\theta}^{\mathrm{old}}$，其中 $\boldsymbol{\theta}\equiv(\boldsymbol{\pi},\mathbf{A},\phi)$。$\mathbf{A}$ 和 $\boldsymbol{\pi}$ 的参数通常初始化为均匀的值，或者从均匀分布中随机选取初始值，同时满足非负约束与求和约束。参数 $\phi$ 的初始化取决于分布形式。例如，对于高斯分布，可以对数据应用 K 均值算法来初始化 $\boldsymbol{\mu}_k$，并将 $\boldsymbol{\Sigma}_k$ 初始化为相应 K 均值簇的协方差矩阵。然后运行前向 $\alpha$ 递推和后向 $\beta$ 递推，利用结果计算 $\gamma(\mathbf{z}_n)$ 和 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$。此时，也可以计算似然函数。

<!-- pdf-page: 644 -->

<!-- join-previous-paragraph -->
这样就完成了 E 步，再利用这些结果以及第 13.2.1 节的 M 步方程，求出更新后的参数集 $\boldsymbol{\theta}^{\mathrm{new}}$。随后继续交替执行 E 步和 M 步，直到满足某个收敛判据，例如似然函数的变化小于某个阈值。

注意，在这些递推关系中，观测是通过 $p(\mathbf{x}_n\mid\mathbf{z}_n)$ 形式的条件分布进入的。因此，只要能够针对 $\mathbf{z}_n$ 的 $K$ 个可能状态分别计算这个条件分布的值，递推就与观测变量的类型、维数以及条件分布的形式无关。由于观测变量 $\{\mathbf{x}_n\}$ 固定不变，可以在 EM 算法开始时，将 $p(\mathbf{x}_n\mid\mathbf{z}_n)$ 作为 $\mathbf{z}_n$ 的函数预先计算出来，并在整个过程中保持不变。

前面各章已经看到，当数据点数量相对于参数数量足够大时，最大似然方法最有效。这里指出，只要训练序列足够长，就可以用最大似然方法有效地训练隐马尔可夫模型。另一种做法是使用多个较短的序列，这只需要对隐马尔可夫模型的 EM 算法作直接的修改。<span class="margin-reference">习题 13.12</span>对于从左到右的模型，这一点尤其重要，因为在给定的观测序列中，对应于 $\mathbf{A}$ 的非对角元素的某个状态转移，最多只能出现一次。

另一个值得关注的量是预测分布：已观测数据为 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，希望预测 $\mathbf{x}_{N+1}$；这对金融预测等实时应用很重要。再次利用求和规则、乘积规则以及条件独立性质（13.29）和（13.31），得到

$$
\begin{aligned}
p(\mathbf{x}_{N+1}\mid\mathbf{X})&=\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1},\mathbf{z}_{N+1}\mid\mathbf{X})\\
&=\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})p(\mathbf{z}_{N+1}\mid\mathbf{X})\\
&=\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})\sum_{\mathbf{z}_N}p(\mathbf{z}_{N+1},\mathbf{z}_N\mid\mathbf{X})\\
&=\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})\sum_{\mathbf{z}_N}p(\mathbf{z}_{N+1}\mid\mathbf{z}_N)p(\mathbf{z}_N\mid\mathbf{X})\\
&=\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})\sum_{\mathbf{z}_N}p(\mathbf{z}_{N+1}\mid\mathbf{z}_N)\frac{p(\mathbf{z}_N,\mathbf{X})}{p(\mathbf{X})}\\
&=\frac{1}{p(\mathbf{X})}\sum_{\mathbf{z}_{N+1}}p(\mathbf{x}_{N+1}\mid\mathbf{z}_{N+1})\sum_{\mathbf{z}_N}p(\mathbf{z}_{N+1}\mid\mathbf{z}_N)\alpha(\mathbf{z}_N)
\end{aligned}
\tag{13.44}
$$

计算时，可以先运行前向 $\alpha$ 递推，再完成最后对 $\mathbf{z}_N$ 和 $\mathbf{z}_{N+1}$ 的求和。第一次对 $\mathbf{z}_N$ 求和的结果可以存储起来；一旦观测到 $\mathbf{x}_{N+1}$ 的值，就可以利用它把 $\alpha$ 递推向前推进一步，从而预测后续值 $\mathbf{x}_{N+2}$。

<!-- pdf-page: 645 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-14.png" alt="隐马尔可夫模型的因子图局部，保留潜变量、观测变量以及转移与发射因子"><figcaption>图 13.14：隐马尔可夫模型的因子图表示的一个片段。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
注意，在式（13.44）中，从 $\mathbf{x}_1$ 到 $\mathbf{x}_N$ 的全部数据的影响，都汇总在 $\alpha(\mathbf{z}_N)$ 的 $K$ 个值中。因此，只需固定大小的存储空间，就可以无限地向前推进预测分布，这正是实时应用可能需要的能力。

这里讨论了用最大似然方法估计 HMM 参数。为模型参数 $\boldsymbol{\pi}$、$\mathbf{A}$ 和 $\phi$ 引入先验，再通过极大化参数的后验概率来估计其值，就很容易将这个框架扩展为正则化最大似然方法。这仍然可以用 EM 算法完成：E 步与前面的讨论相同；M 步则在极大化之前，将先验分布 $p(\boldsymbol{\theta})$ 的对数加入函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 中。这是本书多处讨论过的技术的直接应用。此外，还可以用变分方法对 HMM 进行完整的贝叶斯处理，将参数分布边缘化掉（MacKay，1997）。<span class="margin-reference">第 10.1 节</span>与最大似然一样，这会得到一次前向、一次后向的递推，用于计算后验概率。

### 13.2.3 HMM 的和积算法

图 13.5 中表示隐马尔可夫模型的有向图是一棵树，因此可以利用和积算法求隐变量的局部边缘分布。<span class="margin-reference">第 8.4.4 节</span>不出所料，它等价于上一节考虑的前向—后向算法，因此和积算法为推导 alpha-beta 递推公式提供了一种简单方法。

首先，将图 13.5 的有向图转换为因子图，图 13.14 展示了其中一个有代表性的片段。这种因子图显式显示所有变量，包括潜变量和观测变量。不过，为了解决推断问题，我们始终以变量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 为条件，因此可以将发射概率吸收到转移概率因子中，简化因子图。这样就得到图 13.15 中简化的因子图表示，其中各因子为

$$
h(\mathbf{z}_1)=p(\mathbf{z}_1)p(\mathbf{x}_1\mid\mathbf{z}_1)
\tag{13.45}
$$

$$
f_n(\mathbf{z}_{n-1},\mathbf{z}_n)=p(\mathbf{z}_n\mid\mathbf{z}_{n-1})p(\mathbf{x}_n\mid\mathbf{z}_n).
\tag{13.46}
$$

<!-- pdf-page: 646 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/a-fig-13-15.png" alt="隐马尔可夫模型简化后的因子链，h 因子与初始状态相连，转移发射合并因子 f_n 连接相邻潜变量"><figcaption>图 13.15：用于描述隐马尔可夫模型的简化因子图。</figcaption></figure>

为推导 alpha-beta 算法，将最后一个隐变量 $\mathbf{z}_N$ 指定为根节点，首先从叶节点 $h$ 向根节点传递消息。根据消息传播的一般结果（8.66）和（8.69），隐马尔可夫模型中传递的消息具有如下形式：

$$
\mu_{\mathbf{z}_{n-1}\to f_n}(\mathbf{z}_{n-1})=\mu_{f_{n-1}\to\mathbf{z}_{n-1}}(\mathbf{z}_{n-1})
\tag{13.47}
$$

$$
\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)=\sum_{\mathbf{z}_{n-1}}f_n(\mathbf{z}_{n-1},\mathbf{z}_n)\mu_{\mathbf{z}_{n-1}\to f_n}(\mathbf{z}_{n-1})
\tag{13.48}
$$

这些方程表示消息沿链向前传播，等价于上一节推导的 alpha 递推，下面就来说明这一点。注意，由于变量节点 $\mathbf{z}_n$ 只有两个邻居，它们不执行任何计算。

利用式（13.47），可以从式（13.48）中消去 $\mu_{\mathbf{z}_{n-1}\to f_n}(\mathbf{z}_{n-1})$，得到如下形式的 $f\to\mathbf{z}$ 消息递推：

$$
\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)=\sum_{\mathbf{z}_{n-1}}f_n(\mathbf{z}_{n-1},\mathbf{z}_n)\mu_{f_{n-1}\to\mathbf{z}_{n-1}}(\mathbf{z}_{n-1}).
\tag{13.49}
$$

现在回顾定义（13.46），并定义

$$
\alpha(\mathbf{z}_n)=\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)
\tag{13.50}
$$

就得到式（13.36）给出的 alpha 递推。还需要验证 $\alpha(\mathbf{z}_n)$ 本身也与之前定义的量等价。利用初始条件（8.71），并注意到 $\alpha(\mathbf{z}_1)$ 由 $h(\mathbf{z}_1)=p(\mathbf{z}_1)p(\mathbf{x}_1\mid\mathbf{z}_1)$ 给出，它与式（13.37）完全相同，就很容易完成验证。由于初始 $\alpha$ 相同，且它们使用相同方程迭代计算，所以之后所有的 $\alpha$ 也必然相同。

接下来考虑从根节点传回叶节点的消息，其形式为

$$
\mu_{f_{n+1}\to f_n}(\mathbf{z}_n)=\sum_{\mathbf{z}_{n+1}}f_{n+1}(\mathbf{z}_n,\mathbf{z}_{n+1})\mu_{f_{n+2}\to f_{n+1}}(\mathbf{z}_{n+1})
\tag{13.51}
$$

这里与之前一样，消去了 $\mathbf{z}\to f$ 类型的消息，因为变量节点不执行任何计算。利用定义（13.46）替换 $f_{n+1}(\mathbf{z}_n,\mathbf{z}_{n+1})$，并定义

$$
\beta(\mathbf{z}_n)=\mu_{f_{n+1}\to\mathbf{z}_n}(\mathbf{z}_n)
\tag{13.52}
$$

<!-- pdf-page: 647 -->

就得到式（13.38）给出的 beta 递推。同样，可以验证 beta 变量本身也是等价的：式（8.70）说明根变量节点发送的初始消息为 $\mu_{\mathbf{z}_N\to f_N}(\mathbf{z}_N)=1$，这与第 13.2.2 节给出的 $\beta(\mathbf{z}_N)$ 的初始化完全相同。

和积算法还规定了，在所有消息都计算完之后，如何计算边缘分布。具体来说，结果（8.63）表明，节点 $\mathbf{z}_n$ 处的局部边缘分布由所有传入消息的乘积给出。因为已经以变量 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 为条件，所以计算的是联合分布

$$
p(\mathbf{z}_n,\mathbf{X})=\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)\mu_{f_{n+1}\to\mathbf{z}_n}(\mathbf{z}_n)=\alpha(\mathbf{z}_n)\beta(\mathbf{z}_n).
\tag{13.53}
$$

两边除以 $p(\mathbf{X})$，就得到

$$
\gamma(\mathbf{z}_n)=\frac{p(\mathbf{z}_n,\mathbf{X})}{p(\mathbf{X})}=\frac{\alpha(\mathbf{z}_n)\beta(\mathbf{z}_n)}{p(\mathbf{X})}
\tag{13.54}
$$

与式（13.33）一致。类似地，结果（13.43）可以由式（8.72）推导出来。<span class="margin-reference">习题 13.11</span>

### 13.2.4 缩放因子

在实际使用前向—后向算法之前，必须解决一个重要问题。从递推关系（13.36）可见，每一步的新值 $\alpha(\mathbf{z}_n)$ 都是将前一个值 $\alpha(\mathbf{z}_{n-1})$ 乘以 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 和 $p(\mathbf{x}_n\mid\mathbf{z}_n)$ 得到的。由于这些概率往往远小于 $1$，随着沿链向前计算，$\alpha(\mathbf{z}_n)$ 的值可能以指数速度趋向零。对于中等长度的链，例如长度约为 $100$，即便使用双精度浮点数，$\alpha(\mathbf{z}_n)$ 的计算也很快会超出计算机能够表示的数值范围。

对于独立同分布数据，我们在计算似然函数时通过取对数，已经隐含地避开了这个问题。遗憾的是，这里取对数并不能解决问题，因为计算的是多个小数的乘积之和；事实上，我们隐含地对图 13.7 格图中的所有可能路径求和。因此，改用重新缩放后的 $\alpha(\mathbf{z}_n)$ 和 $\beta(\mathbf{z}_n)$，让它们的值保持在 $1$ 的数量级。我们将看到，在 EM 算法中使用这些重新缩放的量时，相应的缩放因子会约掉。

在式（13.34）中，定义了 $\alpha(\mathbf{z}_n)=p(\mathbf{x}_1,\ldots,\mathbf{x}_n,\mathbf{z}_n)$，它表示截至 $\mathbf{x}_n$ 的所有观测与潜变量 $\mathbf{z}_n$ 的联合分布。现在定义归一化后的 $\alpha$：

$$
\widehat{\alpha}(\mathbf{z}_n)=p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)=\frac{\alpha(\mathbf{z}_n)}{p(\mathbf{x}_1,\ldots,\mathbf{x}_n)}
\tag{13.55}
$$

对于任意 $n$，它都是 $K$ 个变量上的概率分布，因此预期它具有良好的数值性质。为联系缩放后的 alpha 变量和原变量，引入由观测变量的条件分布定义的缩放因子：

$$
c_n=p(\mathbf{x}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}).
\tag{13.56}
$$

<!-- pdf-page: 648 -->

根据乘积规则，有

$$
p(\mathbf{x}_1,\ldots,\mathbf{x}_n)=\prod_{m=1}^{n}c_m
\tag{13.57}
$$

因此

$$
\alpha(\mathbf{z}_n)=p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)p(\mathbf{x}_1,\ldots,\mathbf{x}_n)=\left(\prod_{m=1}^{n}c_m\right)\widehat{\alpha}(\mathbf{z}_n).
\tag{13.58}
$$

于是，可以将 $\alpha$ 的递推方程（13.36）改写为 $\widehat{\alpha}$ 的递推方程：

$$
c_n\widehat{\alpha}(\mathbf{z}_n)=p(\mathbf{x}_n\mid\mathbf{z}_n)\sum_{\mathbf{z}_{n-1}}\widehat{\alpha}(\mathbf{z}_{n-1})p(\mathbf{z}_n\mid\mathbf{z}_{n-1}).
\tag{13.59}
$$

注意，在用于计算 $\widehat{\alpha}(\mathbf{z}_n)$ 的前向消息传递阶段，每一步都必须计算并存储 $c_n$。这很容易做到，因为它就是使式（13.59）右侧归一化为 $\widehat{\alpha}(\mathbf{z}_n)$ 的系数。

类似地，可以用下式定义重新缩放的变量 $\widehat{\beta}(\mathbf{z}_n)$：

$$
\beta(\mathbf{z}_n)=\left(\prod_{m=n+1}^{N}c_m\right)\widehat{\beta}(\mathbf{z}_n)
\tag{13.60}
$$

它同样会保持在机器精度能够处理的范围内，因为根据式（13.35），$\widehat{\beta}(\mathbf{z}_n)$ 只是两个条件概率的比值：

$$
\widehat{\beta}(\mathbf{z}_n)=\frac{p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{z}_n)}{p(\mathbf{x}_{n+1},\ldots,\mathbf{x}_N\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)}.
\tag{13.61}
$$

$\beta$ 的递推结果（13.38）就给出重新缩放变量的以下递推：

$$
c_{n+1}\widehat{\beta}(\mathbf{z}_n)=\sum_{\mathbf{z}_{n+1}}\widehat{\beta}(\mathbf{z}_{n+1})p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n).
\tag{13.62}
$$

应用这个递推关系时，使用之前在 $\alpha$ 阶段计算出的缩放因子 $c_n$。

根据式（13.57），可见似然函数可以用下式求出：

$$
p(\mathbf{X})=\prod_{n=1}^{N}c_n.
\tag{13.63}
$$

类似地，利用式（13.33）、（13.43）和（13.63），可见所需的边缘分布为<span class="margin-reference">习题 13.15</span>

$$
\gamma(\mathbf{z}_n)=\widehat{\alpha}(\mathbf{z}_n)\widehat{\beta}(\mathbf{z}_n)
\tag{13.64}
$$

$$
\xi(\mathbf{z}_{n-1},\mathbf{z}_n)=c_n\widehat{\alpha}(\mathbf{z}_{n-1})p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{z}_{-1})\widehat{\beta}(\mathbf{z}_n).
\tag{13.65}
$$
