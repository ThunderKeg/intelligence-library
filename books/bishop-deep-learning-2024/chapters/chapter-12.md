# 第 12 章 Transformer

<aside class="chapter-guide"><strong>本章导读</strong><p>本章从注意力机制出发，逐步构造 Transformer 层，再讨论它如何处理自然语言及多模态数据。阅读时可先把每个 token 看成一个向量，关注注意力权重怎样随输入改变。</p></aside>

<!-- pdf-page: 373 -->

<figure class="chapter-art">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/chapter-art.png" alt="第 12 章彩色抽象开篇图与英文标题 Transformers">
  <p class="figure-translation">图内文字：Transformers → Transformer。</p>
</figure>

Transformer 是深度学习中最重要的发展之一。它们基于一种称为**注意力**的处理概念，使网络能够为不同输入赋予不同权重，而这些权重系数本身又依赖于输入值，从而捕捉与序列数据及其他形式数据相关的强大归纳偏置。

这类模型之所以称为 Transformer，是因为它们将某个表示空间中的一组向量变换为另一个空间中维度相同的对应向量。变换的目标是让新空间具有更丰富的内部表示，从而更适合解决下游任务。Transformer 的输入可以是无结构的向量集合、有序序列或更一般的表示，因此适用范围广泛。

Transformer 最初是在自然语言处

<!-- pdf-page: 374 -->
<!-- join-previous-paragraph -->

理（natural language processing，NLP）的背景下提出的；这里的“自然”语言指英语、汉语等语言。它们的表现远远超过了此前基于循环神经网络（RNN）的最先进方法。后来，人们发现 Transformer 在许多其他领域也取得了优异结果。例如，视觉 Transformer 在图像处理任务中常常优于卷积神经网络（CNN），而结合文本、图像、音频、视频等多种数据的多模态 Transformer 则跻身最强大的深度学习模型之列。

Transformer 的一大优势是迁移学习非常有效：可以先用大量数据训练一个 Transformer 模型，再通过某种形式的微调，将训练后的模型用于许多下游任务。能够随后适配多种不同任务的大规模模型称为**基础模型**。此外，还可以用无标注数据以自监督方式训练 Transformer；这对语言模型尤其有效，因为 Transformer 能够利用互联网和其他来源的大量文本。**规模化假说**认为，只要增加模型的规模（以可学习参数数量衡量），并用规模相称的大型数据集训练，即便不改变架构，性能也能显著提高。Transformer 还特别适合图形处理器（GPU）等大规模并行处理硬件，使拥有约一万亿（$10^{12}$）个参数的超大型神经网络语言模型得以在合理时间内训练。这类模型具有非凡的能力，并明确展现出一些涌现性质的迹象，有人将其描述为通用人工智能的早期征兆（Bubeck 等，2023）。

对于初学者，Transformer 的架构可能显得复杂，甚至令人望而生畏，因为它涉及多个协同工作的组件，而各种设计选择看上去可能有些任意。因此，本章将逐步全面介绍 Transformer 背后的所有关键思想，并提供清晰的直觉来解释各个组成部分的设计动机。我们先描述 Transformer 架构，再重点讨论自然语言处理，最后考察其他应用领域。

## 12.1 注意力

Transformer 的根本基础是注意力。它最初被开发为机器翻译中循环神经网络的增强机制（Bahdanau、Cho 和 Bengio，2014；见第 12.2.5 节）。后来，Vaswani 等（2017）表明，去掉循环结构而只关注注意力机制，能够显著提高性能。如今，基于注意力的 Transformer 在几乎所有应用中都已取代循环神经网络。下面以自然语言为例说明注意力的用途，不过，它的适用范围要广得多。

<!-- pdf-page: 375 -->

<figure id="fig-12-1">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-1.png" alt="英语句子中的 bank 受到 swam 和 river 的注意力影响，线条粗细表示影响程度">
  <figcaption>图 12.1：注意力示意图。“bank”一词的解释受到“river”和“swam”的影响，连线粗细表示影响程度。</figcaption>
  <p class="figure-translation">图内句子：I swam across the river to get to the other bank → 我游过河，到达了对岸。图内单词：I → 我；swam → 游泳；across → 穿过；the → 这／那（定冠词）；river → 河流；to → 为了／到；get → 到达；other → 另一侧；bank → 河岸。绿色连线：从 swam、river 指向 bank，粗线表示更强的影响。</p>
</figure>

考虑下面两个句子：

> I swam across the river to get to the other bank.（我游过河，到达了对岸。）  
> I walked across the road to get cash from the bank.（我穿过马路，到银行取现金。）

“bank”在这两个句子中含义不同。然而，只有查看序列中其他词所提供的语境，才能判断其含义。我们还看到，在确定“bank”的解释时，有些词比其他词更重要。在第一句中，“swam”和“river”最有力地表明“bank”指河岸；在第二句中，“cash”则强烈表明“bank”指金融机构。由此可见，为了确定“bank”的恰当含义，处理句子的神经网络应当**关注**句子其余部分中的特定词，也就是说，更加依赖这些词。图 12.1 展示了注意力的概念。

此外，应当获得更多注意力的具体位置也依赖输入序列本身：第一句中重要的是第二个词和第五个词，第二句中则是第八个词。在标准神经网络中，不同输入对输出的影响程度取决于乘在这些输入上的权重值。然而，网络训练完毕后，这些权重及其关联的输入便固定不变。相比之下，注意力使用的加权因子，其值随具体输入数据而变化。图 12.2 显示了一个用自然语言训练的 Transformer 网络中的一部分注意力权重。

讨论自然语言处理时，我们会看到如何用词嵌入把词映射为嵌入空间中的向量。这些向量可用作后续神经网络处理的输入。词嵌入能够捕捉初步的语义性质，例如将含义相近的词映射到嵌入空间中相近的位置。这类嵌入的一个特点是，同一个词总会映射为同一个嵌入向量。

<!-- pdf-page: 376 -->

<figure id="fig-12-2">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-2.png" alt="英语句子两个词序列之间的多条绿色注意力连线，深浅表示习得的权重">
  <figcaption>图 12.2：习得的注意力权重示例。［经 Vaswani 等（2017）许可转载。］</figcaption>
  <p class="figure-translation">图内英文依序：The Law will never be perfect, but its application should be just. This is what we are missing in my opinion. &lt;EOS&gt; &lt;pad&gt; → 法律永远不会完美，但其执行应当公正。我认为，这正是我们所欠缺的。&lt;EOS&gt; 表示序列结束，&lt;pad&gt; 表示填充符。上下两行表示同一句中的词；绿色连线表示各词之间的注意力权重。</p>
</figure>

Transformer 可以看作一种更丰富的嵌入形式，其中某个向量映射到的位置取决于序列中的其他向量。因此，在上面的例子中，代表“bank”的向量在两个句子里可能映射到新嵌入空间中的不同位置。例如，在第一句中，变换后的表示可能让“bank”在嵌入空间中靠近“water”；在第二句中，则可能让它靠近“money”。

再以蛋白质建模为例。我们可以把蛋白质视为称为氨基酸的分子单元组成的一维序列。一个蛋白质可能包含数百乃至数千个这样的单元，每个单元属于 22 种可能类型中的一种。在活细胞中，蛋白质会折叠成三维结构，使一维序列中相隔很远的氨基酸在三维空间中变得非常接近，并因此发生相互作用。Transformer 模型允许这些相距较远的氨基酸相互“关注”，从而大大提高三维结构建模的准确性（Vig 等，2020；见图 1.2）。

### 12.1.1 Transformer 的处理过程

Transformer 的输入数据是一组维度为 $D$ 的向量 $\{\mathbf x_n\}$，其中 $n=1,\ldots,N$。我们将这些数据向量称为 **token**。例如，一个 token 可以对应句子中的一个词、图像中的一个图块，或蛋白质中的一个氨基酸。token 的元素 $x_{ni}$ 称为**特征**。稍后我们会看到如何为自然语言数据和图像构造这些 token 向量。Transformer 的一个强大性质是：处理不同类型数据的混合体时，无须设计新的神经网络架构，只需把数据变量合并为一组联合的 token。

在准确理解 Transformer 的运作方式之前，

<!-- pdf-page: 377 -->

<figure id="fig-12-3">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-3.png" alt="N 行 D 列的数据矩阵 X，第 n 行突出显示为转置向量 x_n^T">
  <figcaption>图 12.3：维度为 $N\times D$ 的数据矩阵 $\mathbf X$ 的结构，其中第 $n$ 行表示转置后的数据向量 $\mathbf x_n^\mathsf T$。</figcaption>
  <p class="figure-translation">图内文字：$N$ (tokens) → $N$ 个 token；$D$ (features) → $D$ 个特征；$\mathbf X$ → 数据矩阵；$\mathbf x_n^\mathsf T$ → 第 $n$ 个 token 的转置向量。</p>
</figure>

精确规定记号很重要。我们遵循标准惯例，把数据向量合并为一个 $N\times D$ 的矩阵 $\mathbf X$，其第 $n$ 行由 token 向量 $\mathbf x_n^\mathsf T$ 构成，$n=1,\ldots,N$ 是行标号，如图 12.3 所示。注意，此矩阵表示一组输入 token；在多数应用中，我们需要一个包含许多组 token 的数据集，例如多个相互独立的文本段落，每个词表示为一个 token。Transformer 的基本构件是一个以数据矩阵为输入、生成相同维度的变换后输出矩阵 $\widetilde{\mathbf X}$ 的函数。我们可以把这个函数写成

$$
\widetilde{\mathbf X}=\operatorname{TransformerLayer}[\mathbf X]. \tag{12.1}
$$

随后可以连续应用多个 Transformer 层，构建能够学习丰富内部表示的深层网络。每个 Transformer 层都包含自己的权重和偏置，它们可借助适当的代价函数，通过梯度下降学习；我们将在本章后面详细讨论（见第 12.3 节）。

单个 Transformer 层本身包含两个阶段。实现注意力机制的第一阶段在数据矩阵的列方向上混合不同 token 向量中对应的特征；第二阶段则独立作用于每一行，变换各个 token 向量内部的特征。我们先来看注意力机制。

### 12.1.2 注意力系数

设嵌入空间中有一组输入 token $\mathbf x_1,\ldots,\mathbf x_N$，我们想将其映射到同样包含 $N$ 个 token、但位于新嵌入空间中的另一组向量 $\mathbf y_1,\ldots,\mathbf y_N$，以捕捉更丰富的语义结构。考虑其中一个输出向量 $\mathbf y_n$。它的值不仅应取决于对应的输入向量 $\mathbf x_n$，还应取决于集合中的所有向量 $\mathbf x_1,\ldots,\mathbf x_N$。借助注意力，这种依赖对于那些在确定 $\mathbf y_n$ 的新表示时特别重要的输入 $\mathbf x_m$ 应更强。实现这一点的简单办法，是将每个输出向量 $\mathbf y_n$ 定义为输入向量

<!-- pdf-page: 378 -->
<!-- join-previous-paragraph -->

$\mathbf x_1,\ldots,\mathbf x_N$ 的线性组合，其加权系数为 $a_{nm}$：

$$
\mathbf y_n=\sum_{m=1}^{N}a_{nm}\mathbf x_m. \tag{12.2}
$$

其中，$a_{nm}$ 称为**注意力权重**。对输出 $\mathbf y_n$ 影响很小的输入 token，其系数应接近零；影响最大的输入应具有最大的系数。因此，我们要求系数非负，以避免一个系数变得很大且为正，而另一个系数变得很大且为负并与之抵消。我们还希望：如果某个输出更加关注某个特定输入，对其他输入的关注就应相应减少，所以要求系数之和为 1。于是加权系数须满足以下两个约束：

$$
a_{nm}\geqslant 0. \tag{12.3}
$$

$$
\sum_{m=1}^{N}a_{nm}=1. \tag{12.4}
$$

两者共同意味着每个系数都落在 $0\leqslant a_{nm}\leqslant 1$ 范围内，因此这些系数定义了一个“单位分解”（见习题 12.1）。在特殊情况 $a_{mm}=1$ 下，$n\ne m$ 时有 $a_{mn}=0$，因而 $\mathbf y_m=\mathbf x_m$，即输入向量在变换后保持不变。更一般地，输出 $\mathbf y_m$ 是输入向量的混合，其中某些输入得到更高权重。

**译注：** 原书在上述推论中写作 $a_{nm}=0$；式 (12.4) 对固定的第一下标按行归一化，因此从 $a_{mm}=1$ 得到的是同一行其余元素 $a_{mn}=0$，第二下标 $n\ne m$。

注意，每个输出向量 $\mathbf y_n$ 都有一组不同的系数，约束 (12.3) 和 (12.4) 对每个 $n$ 分别适用。这些系数 $a_{nm}$ 依赖输入数据，我们很快会看到如何计算它们。

### 12.1.3 自注意力

下一个问题是如何确定系数 $a_{nm}$。在详细讨论之前，先引入信息检索领域的一些术语。考虑在网上电影流媒体服务中选择一部影片的问题。一种方法是为每部影片附上一系列属性，描述其类型（喜剧、动作片等）、主演姓名、片长等。用户可在影片目录中搜索，找出符合自己偏好的影片。我们可以把每部影片的属性编码成一个称为**键**的向量，以实现自动搜索。相应的影片文件本身称为**值**。同样，用户可以给出自己对所需属性的取值构成的向量，我们称之为**查询**。影片服务可以将查询向量与所有键向量比较，找出最佳匹配，并以值文件的形式将相应影片发送给用户。我们可以认为用户“关注”其键与查询最为匹配的影片。这是一种**硬注意力**，只返回一个值向量。对于 Transformer，我们将其推广为**软注意力**：用连续变量衡量查询与键的匹配程度，再用这些变量对值向量影响输出的程度进行加权。这样也能保证 Transformer 函数可微，从而可用梯度下降训练。

<!-- pdf-page: 379 -->
<!-- join-previous-paragraph -->

沿用信息检索的类比，可以把每个输入向量 $\mathbf x_n$ 看作一个用于创建输出 token 的值向量。我们还直接将 $\mathbf x_n$ 用作输入 token $n$ 的键向量；这类似于用影片本身概括它的特征。最后，可用 $\mathbf x_m$ 作为输出 $\mathbf y_m$ 的查询向量，再将它与各个键向量比较。为判断 $\mathbf x_n$ 所表示的 token 应在多大程度上关注 $\mathbf x_m$ 所表示的 token，我们需要计算这些向量的相似程度。一种简单的相似性度量是它们的点积 $\mathbf x_n^\mathsf T\mathbf x_m$。为了施加约束 (12.3) 和 (12.4)，可用 softmax 函数变换点积，定义加权系数 $a_{nm}$（见第 5.3 节）：

$$
a_{nm}=\frac{\exp(\mathbf x_n^\mathsf T\mathbf x_m)}{\sum_{m'=1}^{N}\exp(\mathbf x_n^\mathsf T\mathbf x_{m'})}. \tag{12.5}
$$

注意，此处 softmax 函数没有概率解释，它只是用于恰当地归一化注意力权重。

综上，每个输入向量 $\mathbf x_n$ 都变换为相应的输出向量 $\mathbf y_n$。其方法是按式 (12.2) 对输入向量作线性组合，其中施加于输入向量 $\mathbf x_m$ 的权重 $a_{nm}$，由式 (12.5) 的 softmax 函数给出；该函数使用输入 $n$ 的查询 $\mathbf x_n$ 与输入 $m$ 的键 $\mathbf x_m$ 之间的点积 $\mathbf x_n^\mathsf T\mathbf x_m$。注意，如果所有输入向量相互正交，那么每个输出向量就等于相应的输入向量，即对 $m=1,\ldots,N$ 有 $\mathbf y_m=\mathbf x_m$（见习题 12.3）。

**译注：** 原书末句和习题 12.3 的结论与式 (12.5) 不一致。正交只使交叉点积为零，softmax 后的非对角权重仍为正。例如 $\mathbf x_1=(1,0)$、$\mathbf x_2=(0,1)$ 时，$a_{12}=1/(e+1)>0$，因此 $\mathbf y_1\ne\mathbf x_1$。

使用数据矩阵 $\mathbf X$，以及类似的 $N\times D$ 输出矩阵 $\mathbf Y$（其各行由 $\mathbf y_m$ 给出），可将式 (12.2) 写成矩阵形式：

$$
\mathbf Y=\operatorname{Softmax}[\mathbf X\mathbf X^\mathsf T]\mathbf X, \tag{12.6}
$$

其中，$\operatorname{Softmax}[\mathbf L]$ 是一个算子：它对矩阵 $\mathbf L$ 的每个元素取指数，然后独立归一化各行，使每行之和为 1。为清楚起见，下文将主要使用矩阵记法。

这一过程称为**自注意力**，因为我们用同一序列确定查询、键和值。本章后面还会遇到这一注意力机制的变体。此外，由于查询向量和键向量的相似性由点积给出，它又称为**点积自注意力**。

### 12.1.4 网络参数

到目前为止，从输入向量 $\{\mathbf x_n\}$ 到输出向量 $\{\mathbf y_n\}$ 的变换是固定的，没有可调参数，因此无法从数据中学习。此外，token 向量 $\mathbf x_n$ 中每个特征值在确定注意力系数时起同等作用；我们则希望网络在判断 token 相似性时能更灵活地侧重某些特征。

<!-- pdf-page: 380 -->
<!-- join-previous-paragraph -->

如果通过对原向量作线性变换，定义新的特征向量，就能解决这两个问题：

$$
\widetilde{\mathbf X}=\mathbf X\mathbf U, \tag{12.7}
$$

其中，$\mathbf U$ 是一个 $D\times D$ 的可学习权重参数矩阵，类似于标准神经网络中的一个“层”。这给出了如下改进后的变换形式：

$$
\mathbf Y=\operatorname{Softmax}[\mathbf X\mathbf U\mathbf U^\mathsf T\mathbf X^\mathsf T]\mathbf X\mathbf U. \tag{12.8}
$$

虽然这个形式灵活得多，但矩阵

$$
\mathbf X\mathbf U\mathbf U^\mathsf T\mathbf X^\mathsf T \tag{12.9}
$$

是对称的，而我们希望注意力机制能支持显著的不对称性。例如，我们可能预期“凿子”与“工具”之间应具有强关联，因为每把凿子都是工具；但“工具”与“凿子”之间的关联应较弱，因为凿子之外还有许多其他工具。尽管 softmax 函数使最终的注意力权重矩阵本身并不对称，我们仍可以让查询和键拥有独立参数，构造灵活得多的模型。此外，式 (12.8) 用同一个参数矩阵 $\mathbf U$ 定义值向量和注意力系数，这似乎也是一个不理想的限制。

我们可以为查询、键和值分别定义独立的线性变换，以克服这些限制：

$$
\mathbf Q=\mathbf X\mathbf W^{(q)}, \tag{12.10}
$$

$$
\mathbf K=\mathbf X\mathbf W^{(k)}, \tag{12.11}
$$

$$
\mathbf V=\mathbf X\mathbf W^{(v)}. \tag{12.12}
$$

权重矩阵 $\mathbf W^{(q)}$、$\mathbf W^{(k)}$ 和 $\mathbf W^{(v)}$ 都是最终 Transformer 架构训练时要学习的参数。这里，矩阵 $\mathbf W^{(k)}$ 的维度为 $D\times D_k$，$D_k$ 是键向量的长度。为了能在查询向量和键向量之间计算点积，矩阵 $\mathbf W^{(q)}$ 必须与 $\mathbf W^{(k)}$ 有相同的维度 $D\times D_k$。典型选择是 $D_k=D$。类似地，$\mathbf W^{(v)}$ 是一个 $D\times D_v$ 的矩阵，其中 $D_v$ 决定输出向量的维度。如果设 $D_v=D$，使输出表示与输入维度相同，就便于加入稍后讨论的残差连接（见第 12.1.7 节）。如果每层维度相同，也可以将多个 Transformer 层堆叠起来。于是可将式 (12.6) 推广为

$$
\mathbf Y=\operatorname{Softmax}[\mathbf Q\mathbf K^\mathsf T]\mathbf V, \tag{12.13}
$$

其中 $\mathbf Q\mathbf K^\mathsf T$ 的维度为 $N\times N$，矩阵 $\mathbf Y$ 的维度为 $N\times D_v$。图 12.4 展示 $\mathbf Q\mathbf K^\mathsf T$ 的计算，图 12.5 展示矩阵 $\mathbf Y$ 的计算。

<!-- pdf-page: 381 -->

<figure id="fig-12-4">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-4.png" alt="输入矩阵 X 分别变换为查询矩阵 Q 和键矩阵 K，再相乘得到 QK 转置">
  <figcaption>图 12.4：决定 Transformer 中注意力系数的矩阵 $\mathbf Q\mathbf K^\mathsf T$ 的计算过程。输入 $\mathbf X$ 分别通过式 (12.10) 和 (12.11) 变换，得到查询矩阵 $\mathbf Q$ 与键矩阵 $\mathbf K$，再将二者相乘。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf X$ → 输入矩阵；$\mathbf W^{(q)}$ → 查询权重；$\mathbf W^{(k)}$ → 键权重；$\mathbf Q$ → 查询矩阵；$\mathbf K$ → 键矩阵；$\mathbf Q\mathbf K^\mathsf T$ → 查询与转置键相乘；$N\times D$、$D\times D$、$N\times N$ → 各矩阵维度。</p>
</figure>

在实践中，我们还可在这些线性变换中加入偏置参数。不过，和处理标准神经网络的方法一样（见第 6.2.1 节），可通过在数据矩阵 $\mathbf X$ 中增加一列 1，并在权重矩阵中增加一行表示偏置的参数，将偏置参数吸收到权重矩阵中。此后，为避免记号繁杂，我们都将偏置参数视为隐含存在。

与传统神经网络相比，这里的信号路径在激活值之间存在乘法关系。标准网络把激活值乘以固定权重，而这里的激活值乘以依赖数据的注意力系数。这意味着，例如，对某个特定输入向量，如果某个注意力系数接近零，由此形成的信号路径便会忽略相应的传入信号，因此该信号不会影响网络输出。

<figure id="fig-12-5">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-5.png" alt="注意力权重矩阵乘以值矩阵 V，得到输出矩阵 Y 中突出显示的元素">
  <figcaption>图 12.5：给定查询、键和值矩阵 $\mathbf Q$、$\mathbf K$ 和 $\mathbf V$ 时，注意力层输出的计算过程。输出矩阵 $\mathbf Y$ 中突出显示的元素，由 $\operatorname{Softmax}[\mathbf Q\mathbf K^\mathsf T]$ 的突出显示行与 $\mathbf V$ 的突出显示列作点积得到。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf Y$ → 输出矩阵；$\operatorname{Softmax}[\mathbf Q\mathbf K^\mathsf T]$ → 归一化注意力权重矩阵；$\mathbf V$ → 值矩阵；$N\times D_v$、$N\times N$ → 矩阵维度。粉色行、列及方格表示参与点积的元素与所得输出位置。</p>
</figure>

<!-- pdf-page: 382 -->

<figure id="fig-12-6">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-6.png" alt="缩放点积自注意力层中从 X 到查询、键、值再到 Y 的计算流程">
  <figcaption>图 12.6：缩放点积自注意力神经网络层中的信息流。图中“mat mul”表示矩阵乘法，“scale”指用 $\sqrt{D_k}$ 归一化 softmax 的输入。这一结构构成一个注意力“头”。</figcaption>
  <p class="figure-translation">图内文字：mat mul → 矩阵乘法；scale → 缩放；softmax → softmax 归一化；$\mathbf X$ → 输入；$\mathbf Q$ → 查询；$\mathbf K$ → 键；$\mathbf V$ → 值；$\mathbf Y$ → 输出。</p>
</figure>

相比之下，如果标准神经网络学会忽略某个特定输入或隐藏单元变量，它就会对所有输入向量都忽略该变量。

### 12.1.5 缩放自注意力

我们还可以对自注意力层作最后一项改进。回想一下，softmax 函数在输入幅值较大时，其梯度会呈指数级减小，正如 tanh 或逻辑 sigmoid 激活函数一样。为了帮助防止这种情况，可在应用 softmax 函数之前重新缩放查询向量与键向量的乘积。为了推导合适的缩放因子，注意：如果查询向量和键向量的各元素都是均值为零、方差为 1 的独立随机数，那么点积的方差为 $D_k$（见习题 12.4）。因此，我们用 $D_k$ 的平方根所给出的标准差归一化 softmax 的输入，使注意力层的输出形式为

$$
\mathbf Y=\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)\equiv\operatorname{Softmax}\!\left[\frac{\mathbf Q\mathbf K^\mathsf T}{\sqrt{D_k}}\right]\mathbf V. \tag{12.14}
$$

这称为**缩放点积自注意力**，是我们的自注意力神经网络层的最终形式。图 12.6 和算法 12.1 总结了这一层的结构。

### 12.1.6 多头注意力

至此描述的注意力层使输出向量能够关注输入向量中依赖于数据的模式，称为一个**注意力头**。不过，

<!-- pdf-page: 383 -->

**算法 12.1：缩放点积自注意力**

```text
输入：一组 token X ∈ ℝ^(N×D)：{x₁, …, x_N}
      权重矩阵 {W^(q), W^(k)} ∈ ℝ^(D×D_k)，W^(v) ∈ ℝ^(D×D_v)
输出：Attention(Q, K, V) ∈ ℝ^(N×D_v)：{y₁, …, y_N}

Q = XW^(q)                 // 计算查询 Q ∈ ℝ^(N×D_k)
K = XW^(k)                 // 计算键 K ∈ ℝ^(N×D_k)
V = XW^(v)                 // 计算值 V ∈ ℝ^(N×D_v)
返回 Attention(Q, K, V) = Softmax[QKᵀ / √D_k] V
```

**译注：** 算法 12.1 的原书把 $\mathbf V$ 的维度误印为 $N\times D$；由输入矩阵 $\mathbf W^{(v)}\in\mathbb R^{D\times D_v}$ 可知它应为 $N\times D_v$。

可能同时存在多种相关的注意力模式。例如，在自然语言中，有些模式可能与时态有关，另一些则与词汇有关。只用一个注意力头可能会把这些效应平均掉。我们可以改用多个并行的注意力头。它们是结构相同的单头副本，但分别拥有独立的可学习参数来控制查询、键和值矩阵的计算。这类似于卷积网络的每一层使用多个不同的滤波器。

设有 $H$ 个头，以 $h=1,\ldots,H$ 为索引，形式为

$$
\mathbf H_h=\operatorname{Attention}(\mathbf Q_h,\mathbf K_h,\mathbf V_h), \tag{12.15}
$$

其中 $\operatorname{Attention}(\cdot,\cdot,\cdot)$ 由式 (12.14) 给出；我们还为每个头分别定义查询、键和值矩阵：

$$
\mathbf Q_h=\mathbf X\mathbf W_h^{(q)}, \tag{12.16}
$$

$$
\mathbf K_h=\mathbf X\mathbf W_h^{(k)}, \tag{12.17}
$$

$$
\mathbf V_h=\mathbf X\mathbf W_h^{(v)}. \tag{12.18}
$$

先将各个头拼接成一个矩阵，再用矩阵 $\mathbf W^{(o)}$ 对结果进行线性变换，得到组合输出：

$$
\mathbf Y(\mathbf X)=\operatorname{Concat}[\mathbf H_1,\ldots,\mathbf H_H]\mathbf W^{(o)}. \tag{12.19}
$$

图 12.7 展示了这一过程。

每个矩阵 $\mathbf H_h$ 的维度为 $N\times D_v$，因此拼接后的矩阵维度为 $N\times HD_v$。再用维度为 $HD_v\times D$ 的线性矩阵 $\mathbf W^{(o)}$ 变换，得到维度为 $N\times D$ 的最终输出矩阵 $\mathbf Y$，与原始输入矩阵 $\mathbf X$ 相同。训练时，矩阵 $\mathbf W^{(o)}$ 的元素与查询、键、值矩阵一同学习。通常选择 $D_v=D/H$，

<!-- pdf-page: 384 -->

<figure id="fig-12-7">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-7.png" alt="多个注意力头输出拼接后，通过输出权重矩阵投影为 N 乘 D 的矩阵 Y">
  <figcaption>图 12.7：多头注意力的网络架构。每个头都具有图 12.6 所示的结构，并有自己的键、查询和值参数。各个头的输出先拼接，再线性投影回输入数据的维度。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf H_1,\mathbf H_2,\ldots,\mathbf H_H$ → 各注意力头的输出；$\mathbf W^{(o)}$ → 输出投影矩阵；$\mathbf Y$ → 多头注意力输出；$N\times HD_v$、$HD_v\times D$、$N\times D$ → 矩阵维度。</p>
</figure>

使拼接后的矩阵维度为 $N\times D$。算法 12.2 总结了多头注意力，图 12.8 则展示了多头注意力层中的信息流。

注意，上述多头注意力的表述遵循研究文献中的写法，其中先对每个头乘以 $\mathbf W^{(v)}$，再乘以输出矩阵 $\mathbf W^{(o)}$，存在一定冗余。去除这种冗余后，多头自注意力层可写成各个头贡献之和（见习题 12.5）。

### 12.1.7 Transformer 层

多头自注意力是 Transformer 网络的核心架构元素。我们知道，神经网络能从深度中获益良多，因此希望将多个自注意力层堆叠起来。为了提高训练效率，可以引入绕过多头结构的残差连接（见第 9.5 节）。

**算法 12.2：多头注意力**

```text
输入：一组 token X ∈ ℝ^(N×D)：{x₁, …, x_N}
      查询权重矩阵 {W₁^(q), …, W_H^(q)} ∈ ℝ^(D×D)
      键权重矩阵 {W₁^(k), …, W_H^(k)} ∈ ℝ^(D×D)
      值权重矩阵 {W₁^(v), …, W_H^(v)} ∈ ℝ^(D×D_v)
      输出权重矩阵 W^(o) ∈ ℝ^(HD_v×D)
输出：Y ∈ ℝ^(N×D)：{y₁, …, y_N}

// 为每个头计算自注意力（算法 12.1）
for h = 1, …, H do
    Q_h = XW_h^(q)，K_h = XW_h^(k)，V_h = XW_h^(v)
    H_h = Attention(Q_h, K_h, V_h)  // H_h ∈ ℝ^(N×D_v)
end for
H = Concat[H₁, …, H_H]  // 拼接各头
返回 Y(X) = HW^(o)
```

**译注：** 算法 12.2 的原书把输出列表末项误写为 $\mathbf x_N$、拼接末项误写为 $\mathbf H_N$；此处按输出变量及头数 $H$ 更正。

<!-- pdf-page: 385 -->

<figure id="fig-12-8">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-8.png" alt="输入 X 并行经过多个自注意力模块，拼接、线性变换后输出 Y">
  <figcaption>图 12.8：多头注意力层中的信息流。算法 12.2 给出的相应计算见图 12.7。</figcaption>
  <p class="figure-translation">图内文字：self-attention → 自注意力；concat → 拼接；linear → 线性变换；$\mathbf X$ → 输入；$\mathbf Y$ → 输出。</p>
</figure>

为此，输出维度须与输入维度相同，即 $N\times D$。随后再应用层归一化（Ba、Kiros 和 Hinton，2016；见第 7.4.3 节），以提高训练效率。由此得到的变换可写为

$$
\mathbf Z=\operatorname{LayerNorm}[\mathbf Y(\mathbf X)+\mathbf X], \tag{12.20}
$$

其中 $\mathbf Y$ 由式 (12.19) 定义。有时会用**前置归一化**代替层归一化，即把归一化层放在多头自注意力之前而非之后；这可能使优化更有效，此时有

$$
\mathbf Z=\mathbf Y(\mathbf X')+\mathbf X,\qquad \text{其中}\quad \mathbf X'=\operatorname{LayerNorm}[\mathbf X]. \tag{12.21}
$$

在两种情况下，$\mathbf Z$ 的维度仍与输入矩阵 $\mathbf X$ 相同，都是 $N\times D$。

我们已经看到，注意力机制先对值向量作线性组合，再对所得结果作线性组合以生成输出向量。值向量也是输入向量的线性函数，因此注意力层的输出只能是输入的线性组合。非线性确实通过注意力权重引入，因此输出会通过 softmax 函数非线性地依赖于输入；不过，输出向量仍受限于输入向量张成的子空间，这限制了注意力层的表达能力。我们可以用一个标准的非线性神经网络后处理每层的输出，来增强 Transformer 的灵活性。这个网络具有 $D$ 个输入和 $D$ 个输出，记为 $\operatorname{MLP}[\cdot]$，即“多层感知机”。例如，它可以是一个隐藏单元使用 ReLU 的两层全连接网络。处理方式还须保留 Transformer 处理变长序列的能力。

<!-- pdf-page: 386 -->

<figure id="fig-12-9">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-9.png" alt="一个 Transformer 层：多头自注意力、残差连接与归一化、MLP、第二次残差连接与归一化">
  <figcaption>图 12.9：实现变换 (12.1) 的一个 Transformer 层。这里“MLP”表示多层感知机，“add and norm”表示残差连接后接层归一化。</figcaption>
  <p class="figure-translation">图内文字：multi-head self-attention → 多头自注意力；add &amp; norm → 相加并归一化；MLP → 多层感知机；$\mathbf X$ → 输入；$\mathbf Z$ → 中间表示；$\widetilde{\mathbf X}$ → 输出。</p>
</figure>

为此，要对 $\mathbf Z$ 的每一行所对应的输出向量应用同一个共享网络。同样，可使用残差连接改进这个神经网络层。它还包含层归一化，使 Transformer 层的最终输出为

$$
\widetilde{\mathbf X}=\operatorname{LayerNorm}[\operatorname{MLP}[\mathbf Z]+\mathbf Z]. \tag{12.22}
$$

由此得到的完整 Transformer 层架构见图 12.9，并总结于算法 12.3。这里也可以采用前置归一化，此时最终输出为

$$
\widetilde{\mathbf X}=\operatorname{MLP}(\mathbf Z')+\mathbf Z,\qquad \text{其中}\quad \mathbf Z'=\operatorname{LayerNorm}[\mathbf Z]. \tag{12.23}
$$

典型 Transformer 会把多个这样的层堆叠起来。各层一般结构相同，但不同层之间不共享权重和偏置。

### 12.1.8 计算复杂度

至此讨论的注意力层将一组长度为 $D$ 的 $N$ 个向量映射为另一组维度相同的 $N$ 个向量。因此，输入和输出的总体维度均为 $ND$。如果使用标准全连接神经网络来映射输入值和输出值，则需要 $O(N^2D^2)$ 个独立参数。类似地，该网络一次前向计算的成本也是 $O(N^2D^2)$。

在注意力层中，矩阵 $\mathbf W^{(q)}$、$\mathbf W^{(k)}$ 和 $\mathbf W^{(v)}$ 在输入 token 间共享。因此，假设 $D_k\simeq D_v\simeq D$，独立参数的数量为 $O(D^2)$。由于共有 $N$ 个输入 token，

<!-- pdf-page: 387 -->

**算法 12.3：Transformer 层**

```text
输入：一组 token X ∈ ℝ^(N×D)：{x₁, …, x_N}
      多头自注意力层参数
      前馈网络参数
输出：X̃ ∈ ℝ^(N×D)：{x̃₁, …, x̃_N}

Z = LayerNorm[Y(X) + X]    // Y(X) 来自算法 12.2
X̃ = LayerNorm[MLP[Z] + Z]  // 共享神经网络
返回 X̃
```

计算自注意力层中的点积需要 $O(N^2D)$ 次计算。可以把自注意力层视为一种稀疏矩阵，其中的参数在矩阵的特定块之间共享。后续神经网络层具有 $D$ 个输入和 $D$ 个输出，成本为 $O(D^2)$（见习题 12.6）。由于它在 token 间共享，其复杂度随 $N$ 线性增长，因此该层的总成本为 $O(ND^2)$。根据 $N$ 和 $D$ 的相对大小，Transformer 层或 MLP 层都可能主导计算成本。与全连接网络相比，Transformer 层的计算效率更高。Transformer 架构已有许多变体（Lin 等，2021；Phuong 和 Hutter，2022），其中包括旨在提高效率的改进（Tay 等，2020）。

### 12.1.9 位置编码

在 Transformer 架构中，矩阵 $\mathbf W_h^{(q)}$、$\mathbf W_h^{(k)}$ 和 $\mathbf W_h^{(v)}$ 在输入 token 间共享，后续神经网络也是如此。因此，若对输入 token 的顺序，即 $\mathbf X$ 的行顺序，进行置换，输出矩阵 $\widetilde{\mathbf X}$ 的行也会发生相同的置换（见习题 12.7）。换言之，Transformer 对输入置换具有**等变性**（见第 10.2 节）。网络架构中的参数共享有利于 Transformer 的大规模并行处理，也使网络能够像学习短距离依赖一样有效地学习长距离依赖。然而，当处理自然语言中的词等序列数据时，不依赖 token 顺序会成为一个重大局限，因为 Transformer 学到的表示与输入 token 的排列顺序无关。“The food was bad, not good at all.”（食物很差，一点也不好）与“The food was good, not bad at all.”（食物很好，一点也不差）包含相同的 token，但由于 token 顺序不同，含义大相径庭。显然，token 顺序对自然语言处理等大多数序列处理任务至关重要，因此我们需要设法把 token 顺序信息注入网络。

由于希望保留精心构造的注意力层所具有的强大性质，我们打算把 token 顺序编码到数据本身，

<!-- pdf-page: 388 -->
<!-- join-previous-paragraph -->

而不在网络架构中表示它。因此，我们为每个输入位置 $n$ 构造一个位置编码向量 $\mathbf r_n$，再把它与对应的输入 token 嵌入 $\mathbf x_n$ 结合。一个显而易见的结合方式是拼接两个向量，但这会增加输入空间乃至后续所有注意力空间的维度，从而显著增加计算成本。我们改为直接把位置向量加到 token 向量上：

$$
\widetilde{\mathbf x}_n=\mathbf x_n+\mathbf r_n. \tag{12.24}
$$

这要求位置编码向量与 token 嵌入向量具有相同的维度。

乍看之下，把位置信息加到 token 向量上似乎会破坏输入向量，使网络的任务更难。然而，一个直观理由是：在高维空间中，随机选取的两个不相关向量往往近乎正交；这表明网络可以相对独立地处理 token 身份信息和位置信息（见习题 12.8）。还要注意，由于每层都有跨层残差连接，位置信息从一个 Transformer 层传到下一层时不会丢失。此外，由于 Transformer 中存在的线性处理层，拼接表示与加法表示具有相似性质（见习题 12.9）。

接下来要构造嵌入向量 $\{\mathbf r_n\}$。一种简单方法是将整数 $1,2,3,\ldots$ 分别赋给各个位置。不过，这种方法的问题在于数值会无界增长，因此可能开始显著干扰嵌入向量。它也可能难以推广到比训练序列更长的新输入序列，因为这些序列需要用到训练时取值范围以外的编码值。另一种方法是给序列中的每个 token 分配一个 $(0,1)$ 区间内的数，使表示有界。不过，同一位置的表示并不唯一，而是取决于整个序列的长度。

理想的位置编码应为每个位置提供唯一表示，且有界、能推广到更长序列；它还应具有一致的方式，表达任意两个输入向量相隔多少步，而不依赖它们的绝对位置，因为 token 的相对位置往往比绝对位置更重要。

位置编码的方法有许多种（Dufter、Schmitt 和 Schütze，2021）。这里介绍 Vaswani 等（2017）提出的一种基于正弦函数的技术。对于给定位置 $n$，相应位置编码向量的分量 $r_{ni}$ 为

$$
r_{ni}=\begin{cases}
\sin\!\left(\dfrac{n}{L^{i/D}}\right),& i\text{ 为偶数},\\[4pt]
\cos\!\left(\dfrac{n}{L^{(i-1)/D}}\right),& i\text{ 为奇数}.
\end{cases} \tag{12.25}
$$

可见，嵌入向量 $\mathbf r_n$ 的各个元素由波长逐渐增大的一系列正弦与余弦函数给出，如图 12.10(a) 所示。

<!-- pdf-page: 389 -->

<figure id="fig-12-10">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-10.png" alt="位置编码的正弦余弦曲线及二维热图">
  <figcaption>图 12.10：式 (12.25) 所定义、用于构造位置编码向量的函数。(a) 横轴是嵌入向量 $\mathbf r$ 的不同分量，纵轴是序列位置；位置 $n$ 和 $m$ 的向量元素值由正弦、余弦曲线与水平灰线的交点表示。(b) 当维度 $D=100$、$L=30$ 时，前 $N=200$ 个位置由式 (12.25) 定义的位置编码向量的热图。</figcaption>
  <p class="figure-translation">图内文字：position → 位置；embedding dimension → 嵌入维度；$r_1,\ldots,r_6$ → 位置编码的各分量；$m,n$ → 两个位置；色标 $-1,0,1$ → 编码值。</p>
</figure>

<!-- pdf-page: 390 -->

这种编码使向量 $\mathbf r_n$ 的各元素都落在 $(-1,1)$ 范围内。它让人联想到二进制数的表示方式：最低位以最高频率交替变化，后续各位的交替频率逐渐降低：

```text
1: 0 0 0 1      2: 0 0 1 0      3: 0 0 1 1
4: 0 1 0 0      5: 0 1 0 1      6: 0 1 1 0
7: 0 1 1 1      8: 1 0 0 0      9: 1 0 0 1
```

不过，式 (12.25) 给出的编码中，向量元素是连续变量，而不是二进制数。图 12.10(b) 展示了位置编码向量。

式 (12.25) 的正弦表示有一个良好性质：对任意固定偏移量 $k$，位置 $n+k$ 处的编码可以表示为位置 $n$ 处编码的线性组合，而组合系数只依赖 $k$，不依赖绝对位置（见习题 12.10）。因此，网络应能够学习关注相对位置。注意，这一性质要求编码同时使用正弦函数和余弦函数。

另一种常见的位置表示方法是使用**可学习的位置编码**。其做法是在每个 token 位置设置一个权重向量，训练时将它与模型的其他参数一起学习，从而避免人工设计表示。由于不同 token 位置之间不共享参数，token 在置换下不再保持不变，而这正是位置编码的目的。不过，此方法不能满足前述推广到更长输入序列的要求，因为训练期间从未出现过的位置编码将未经过训练。因此，当输入长度在训练和推断时都相对固定，才通常最适合这种方法。

## 12.2 自然语言

了解 Transformer 的架构后，我们来探索如何用它处理由词、句子和段落组成的语言数据。虽然 Transformer 最初是为这种模态开发的，但事实证明它是一类非常通用的模型，对大多数输入数据类型都已达到最先进水平。本章后面会讨论它在其他领域中的用途（见第 12.4 节）。

包括英语在内的许多语言都由空白字符分隔的一系列词以及标点符号组成，因此属于序列数据的例子。

<!-- pdf-page: 391 -->

眼下我们先关注词，稍后再回到标点符号（见第 12.2.2 节；亦见第 11.3 节）。

第一个挑战是把词转换为适合用作深度神经网络输入的数值表示。一种简单方法是定义固定词典，并引入长度等于词典大小的向量；对每个词使用“独热”表示，即词典中的第 $k$ 个词对应的向量在位置 $k$ 上取 1，其余位置均取 0。例如，如果“aardwolf”（土狼）在词典中排第三，它的向量表示就是 $(0,0,1,0,\ldots,0)$。

独热表示的一个明显问题是：真实词典可能有几十万个词条，导致向量维度极高。此外，它也无法捕捉词与词之间可能存在的相似性或关系。通过**词嵌入**，把词映射到维度较低的空间，可以同时解决这两个问题；每个词在通常只有几百维的空间中表示为一个稠密向量。

### 12.2.1 词嵌入

嵌入过程可以由一个大小为 $D\times K$ 的矩阵 $\mathbf E$ 定义，其中 $D$ 是嵌入空间的维度，$K$ 是词典的维度。对于每个采用独热编码的输入向量 $\mathbf x_n$，可按下式计算相应的嵌入向量：

$$
\mathbf v_n=\mathbf E\mathbf x_n. \tag{12.26}
$$

由于 $\mathbf x_n$ 采用独热编码，向量 $\mathbf v_n$ 就是矩阵 $\mathbf E$ 的对应列。

我们可以从文本语料库（即大型数据集）中学习矩阵 $\mathbf E$，方法有很多。这里讨论一种常用技术 **word2vec**（Mikolov 等，2013），可以把它看成一个简单的两层神经网络。构造训练集时，文本中每个由 $M$ 个相邻词组成的“窗口”形成一个样本，$M$ 的典型值可以是 5。各样本视为独立，误差函数定义为所有样本误差函数之和。这种方法有两个变体。在**连续词袋**方法中，网络训练的目标变量是中间的词，其余上下文词构成输入，因而网络是在学习“填空”。一种密切相关的方法称为 **skip-gram**，它将输入与输出对调：把中心词作为输入，把上下文词作为目标值。图 12.11 展示了这两种模型。

这一训练过程可以看作一种自监督学习，因为数据只是一大批无标注文本，从中随机抽取许多短小的词序列窗口。标签来自文本本身：把网络试图预测的词“遮蔽”起来即可。

模型训练完毕后，对连续词袋方法，嵌入矩阵 $\mathbf E$ 由第二层权重矩阵的转置给出；对 skip-gram 方法，则由第一层权重矩阵给出。语义相关的词会被映射到嵌入空间中相近的位置。这种现象符合预期：

<!-- pdf-page: 392 -->

<figure id="fig-12-11">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-11.png" alt="连续词袋与 skip-gram 的两层神经网络结构对比">
  <figcaption>图 12.11：用于学习词嵌入的两层神经网络，(a) 为连续词袋方法，(b) 为 skip-gram 方法。</figcaption>
  <p class="figure-translation">图内标记：$\mathbf x_n$ → 中心词；$\mathbf x_{n-2},\mathbf x_{n-1},\mathbf x_{n+1},\mathbf x_{n+2}$ → 上下文词；$\mathbf v$ → 隐藏层中的嵌入向量。</p>
</figure>

与不相关的词相比，相关词更有可能和相似的上下文词一同出现。例如，“city”和“capital”可能更频繁地作为“Paris”或“London”等目标词的上下文，而较少作为“orange”或“polynomial”的上下文。如果“Paris”和“London”映射到相近的嵌入向量，网络就能更容易地预测缺失词的概率。

事实证明，学得的嵌入空间往往具有比相关词相互靠近更丰富的语义结构，还能进行简单的向量运算。例如，“巴黎之于法国，犹如罗马之于意大利”这一概念可以通过嵌入向量的运算表达。若用 $\mathbf v(\text{word})$ 表示词“word”的嵌入向量，则有

$$
\mathbf v(\text{Paris})-\mathbf v(\text{France})+\mathbf v(\text{Italy})\simeq\mathbf v(\text{Rome}). \tag{12.27}
$$

词嵌入最初本身就是作为自然语言处理工具开发的。如今，它们更可能被用作深度神经网络的预处理步骤。从这一角度看，它们可视为深度神经网络的第一层。可以用某个标准的预训练嵌入矩阵将其固定，也可以把它视为自适应层，作为整个系统端到端训练的一部分加以学习。若采用后一种方式，可用随机权重值或标准嵌入矩阵来初始化嵌入层。

<!-- pdf-page: 393 -->

<figure id="fig-12-12">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-12.png" alt="Peter Piper 英语绕口令依次合并 pe、ck 等字符对的分词过程">
  <figcaption>图 12.12：以字节对编码作类比，说明自然语言的 token 化过程。本例出现最频繁的字符对是“pe”，共出现四次，所以它们形成一个新 token，取代所有“pe”。注意，大写“P”与小写“p”是不同字符，因此“Pe”不包含在内。接着加入出现三次的“ck”。随后是“pi”“ed”“per”等各出现两次的 token，以此类推。</figcaption>
  <p class="figure-translation">图内句子各行均为 Peter Piper picked a peck of pickled peppers → 彼得·派珀摘了一配克腌辣椒；彩色下划线依次标示从字符合并成的 pe、ck、pi、ed、per 等 token。</p>
</figure>

### 12.2.2 Token 化

使用固定词典的一个问题是，无法处理词典中没有的词或拼错的词。它也没有考虑标点符号或计算机代码等其他字符序列。解决这些问题的另一种方法是处理字符而不是词，让词典包含大写和小写字母、数字、标点，以及空格和制表符等空白字符。不过，这种方法的缺点是丢弃了语言中有重要语义的词结构，后续神经网络就必须学会从基本字符重新组合出词。对于给定文本，它还需要多得多的序列步骤，从而增加序列处理的计算成本。

可以通过一个预处理步骤，兼取字符级表示与词级表示的优点：把由词和标点构成的字符串转换为 token 序列。这些 token 通常是较短的字符组，也可以包含完整的常见词、较长词的片段以及可组合成不常见词的单个字符（Schuster 和 Nakajima，2012）。这种 token 化还允许系统处理计算机代码等其他序列，甚至图像等其他模态（见第 12.4.1 节）。它也意味着同一词的不同变体可以具有相关表示。例如，“cook”“cooks”“cooked”“cooking”和“cooker”都有联系，共享“cook”这一部分，而“cook”本身也可以是一个 token。

token 化的方法有很多。举例来说，可将用于数据压缩的**字节对编码**改用于文本 token 化，方法是合并字符而不是字节（Sennrich、Haddow 和 Birch，2015）。这一过程从单个字符开始，迭代地把它们合并成更长的字符串。首先用单个字符列表初始化 token 列表，然后在一批文本中查找出现最频繁的相邻 token 对，并用一个新 token 取代它们。为了避免把词合并在一起，如果第二个 token 以空白字符开头，就不从这两个 token 构造新 token。图 12.12 展示了这个迭代重复的过程。

最初，token 数量等于字符数量，因此相对较少。随着新 token 的形成，token 总数增加，

<!-- pdf-page: 394 -->
<!-- join-previous-paragraph -->

如果继续足够长时间，token 最终就会对应文本中的词集合。token 总数一般事先固定，以在字符级和词级表示之间取得折中。达到这个 token 数量时，算法便停止。

在深度学习处理自然语言的实际应用中，通常先将输入文本映射为 token 化表示。不过，本章余下部分将使用词级表示，因为这样更容易说明关键概念及其动机。

### 12.2.3 词袋

现在转向有序向量序列的联合分布 $p(\mathbf x_1,\ldots,\mathbf x_N)$ 的建模，例如自然语言中的词（或 token）。最简单的方法是，假设各词独立地取自同一分布，因此联合分布完全分解为

$$
p(\mathbf x_1,\ldots,\mathbf x_N)=\prod_{n=1}^{N}p(\mathbf x_n). \tag{12.28}
$$

这可以表示成概率图模型，其中各节点相互孤立，没有连接边（见图 11.28）。

分布 $p(\mathbf x)$ 在所有变量间共享；不失一般性，可用一个简单的表表示，其中列出 $\mathbf x$ 各个可能状态（对应词或 token 的词典）的概率。此模型的极大似然解，只须将各个概率设为对应词在训练集中出现次数所占的比例即可（见习题 12.11）。这称为**词袋模型**，因为它完全忽略了词的顺序。

我们可以用词袋方法构造一个简单的文本分类器。例如，可将代表餐馆评论的文本段落分类为正面或负面，进行情感分析。朴素贝叶斯分类器假设每个类别 $C_k$ 内的词相互独立，但不同类别具有不同分布，因此

$$
p(\mathbf x_1,\ldots,\mathbf x_N\mid C_k)=\prod_{n=1}^{N}p(\mathbf x_n\mid C_k). \tag{12.29}
$$

给定类别的先验概率 $p(C_k)$，新序列的类别后验概率为

$$
p(C_k\mid\mathbf x_1,\ldots,\mathbf x_N)\propto p(C_k)\prod_{n=1}^{N}p(\mathbf x_n\mid C_k). \tag{12.30}
$$

类别条件分布 $p(\mathbf x\mid C_k)$ 和先验概率 $p(C_k)$ 都可由训练数据集中的频率估计。对于新序列，将表中的相应条目相乘，就得到所需的后验概率。注意，如果测试集中出现了训练集中没有的词，相应的概率估计将为零，

<!-- pdf-page: 395 -->
<!-- join-previous-paragraph -->

所以训练后通常会对这些估计作“平滑”：在所有条目上均匀重新分配少量概率，以避免零值。

### 12.2.4 自回归模型

词袋模型的一个明显重大局限是完全忽略词序。为解决这一问题，可以采用自回归方法。不失一般性，我们可将词序列的分布分解为条件分布的乘积：

$$
p(\mathbf x_1,\ldots,\mathbf x_N)=\prod_{n=1}^{N}p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1}). \tag{12.31}
$$

它可以表示为一个概率图模型：序列中的每个节点都接收来自此前所有节点的连线（见图 11.27）。我们也可以用一个表表示式 (12.31) 右侧的每一项，并再次从训练集的简单频数统计中估计表项。不过，这些表的大小随序列长度呈指数增长，因此这种方法的成本会高到无法接受（见习题 12.12）。

如果假设式 (12.31) 右侧的每个条件分布仅依赖最近的 $L$ 个词，与此前其他所有观察无关，就能大幅简化模型。例如，当 $L=2$ 时，模型中长度为 $N$ 的观察序列的联合分布为

$$
p(\mathbf x_1,\ldots,\mathbf x_N)=p(\mathbf x_1)p(\mathbf x_2\mid\mathbf x_1)\prod_{n=3}^{N}p(\mathbf x_n\mid\mathbf x_{n-1},\mathbf x_{n-2}). \tag{12.32}
$$

在相应的图模型中，每个节点都有来自前两个节点的连线。这里我们假设条件分布 $p(\mathbf x_n\mid\mathbf x_{n-1},\mathbf x_{n-2})$ 在所有变量间共享（见图 11.30）。同样，式 (12.32) 右侧的每个分布都可用表表示，其数值由训练语料库中连续三个词的统计量估计。

**译注：** 原书在“共享的条件分布”处漏印 $\mathbf x_{n-2}$；式 (12.32) 与随后对三元组的说明都包含前两个词。

$L=1$ 时称为**二元组模型**，因为它依赖相邻词对。类似地，$L=2$ 涉及相邻的三个词，称为**三元组模型**。一般地，它们统称为 **$n$ 元组模型**。

本节讨论的所有模型都可按生成方式运行，以合成新文本。例如，如果给出序列中的第一个和第二个词，就能从三元组统计量 $p(\mathbf x_n\mid\mathbf x_{n-1},\mathbf x_{n-2})$ 中采样生成第三个词，再用第二个和第三个词采样第四个词，依此类推。不过，生成的文本将不连贯，因为每个词只依据前两个词来预测。高质量的文本模型必须考虑语言中的长距离依赖。另一方面，也不能简单增大 $L$，因为概率表的大小会随 $L$ 呈指数增长，以至于远超三元组模型的代价难以承受。然而，自回归表示将在现代语言模型中发挥核心作用；

<!-- pdf-page: 396 -->

<figure id="fig-12-13">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-13.png" alt="三个连续的 RNN 网络单元，共享参数 w，隐状态 z 逐步传播">
  <figcaption>图 12.13：具有参数 $\mathbf w$ 的一般循环神经网络。它以序列 $\mathbf x_1,\ldots,\mathbf x_N$ 为输入，生成序列 $\mathbf y_1,\ldots,\mathbf y_N$ 作为输出。每个方框对应一个具有非线性隐藏单元的多层网络。</figcaption>
  <p class="figure-translation">图内标记：$\mathbf x_1,\mathbf x_2,\mathbf x_3$ → 连续输入；$\mathbf y_1,\mathbf y_2,\mathbf y_3$ → 连续输出；$\mathbf z_0,\mathbf z_1,\mathbf z_2$ → 隐状态；$\mathbf w$ → 各时刻共享的网络参数。</p>
</figure>

这类模型不再依赖概率表，而是采用 Transformer 形式的深度神经网络。

为了允许更长距离的依赖，同时避免 $n$ 元组模型的参数数量呈指数增长，一种方法是使用隐马尔可夫模型，其图结构见图 11.31（见第 11.3.1 节）。可学习参数的数量由潜变量的维度决定；而给定观察 $\mathbf x_n$ 的分布原则上依赖之前的所有观察。然而，较远观察的影响仍然很有限，因为它们的作用必须穿过一连串潜在状态，而这些状态本身又受到较近观察的更新。

### 12.2.5 循环神经网络

$n$ 元组之类的技术随序列长度扩展得很差，因为它们存储完全一般的条件分布表。利用基于神经网络的参数化模型，可以大幅改善扩展性。假设我们直接将标准前馈神经网络应用于自然语言词序列。一个问题是网络输入和输出的数量固定，而训练集和测试集中的序列长度可能变化。此外，如果序列中某个位置上的一个词或词组表示某个概念，那么同一个词或词组出现在另一个位置时，通常仍表示同一概念。这使人想到处理图像数据时遇到的等变性（见第 10 章）。如果能构造一种在序列中共享参数的网络架构，就不仅能捕捉这种等变性，还能大幅减少模型的自由参数数量，并处理不同长度的序列。

为此，可以借鉴隐马尔可夫模型，为序列中的每个步骤 $n$ 引入一个显式的隐藏变量 $\mathbf z_n$。神经网络将当前词 $\mathbf x_n$ 与当前隐藏状态 $\mathbf z_{n-1}$ 一同作为输入，并输出词 $\mathbf y_n$ 以及隐藏变量的下一状态 $\mathbf z_n$。然后可将该网络的多个副本串联起来，副本间共享权重值。所得架构称为**循环神经网络**（RNN），如图 12.13 所示。这里，隐藏状态的初值可以设为某个默认值。

<!-- pdf-page: 397 -->

<figure id="fig-12-14">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-14.png" alt="循环神经网络把英语 I am happy 编码后，逐词解码成荷兰语 Ik ben gelukkig">
  <figcaption>图 12.14：用于语言翻译的循环神经网络示例，详见正文。</figcaption>
  <p class="figure-translation">图内文字：encoder → 编码器；decoder → 解码器；I am happy → 我很高兴；Ik ben gelukkig → 荷兰语“我很高兴”；&lt;start&gt; → 开始标记；&lt;stop&gt; → 停止标记；$\mathbf z_0$ → 初始隐藏状态；$\mathbf z^*$ → 编码后的整句隐藏状态；$\mathbf w$ → 共享参数。虚线箭头表示已输出的词作为下一步输入。原图上方写作“gelukkig”，解码器下方却误拼为“gelukigg”。</p>
</figure>

例如，可以取 $\mathbf z_0=(0,0,\ldots,0)^\mathsf T$。

举一个 RNN 实际应用的例子：把英语句子翻译成荷兰语。句子长度可能不同，每个输出句子的长度也可能与相应的输入句子不同。此外，网络可能必须看到整个输入句子，才能开始生成输出句子。对此，可先向 RNN 输入完整的英语句子，然后接一个记作 $\langle\mathrm{start}\rangle$ 的特殊输入 token，触发翻译开始。训练时，网络学会将 $\langle\mathrm{start}\rangle$ 与输出句子的开头关联起来。我们还把每次生成的词输入到下一个时间步，如图 12.14 所示。网络可以被训练为生成一个特定的 $\langle\mathrm{stop}\rangle$ token，以表示翻译完成。网络的最初几个阶段用于吸收输入序列，相应的输出向量直接忽略。这部分网络可视为“编码器”，其中整个输入句子被压缩进隐藏变量的状态 $\mathbf z^*$。剩余阶段充当“解码器”，一次输出一个词，生成译文。注意，每个输出词都作为下一阶段的输入，因此这种方法具有与式 (12.31) 类似的自回归结构。

### 12.2.6 随时间反向传播

与常规神经网络一样，RNN 可以使用由反向传播计算、通过自动微分求值的梯度，以随机梯度下降训练。误差函数由各输出单元的误差求和而成；每个输出单元都使用 softmax 激活函数以及相应的交叉熵误差函数（见第 5.4.4 节）。在前向传播过程中，激活值从序列的第一个输入一路传播到序列中的所有输出节点，然后误差信号沿同样路径反向传播。这一过程称为**随时间反向传播**，

<!-- pdf-page: 398 -->
<!-- join-previous-paragraph -->

原则上并不复杂。然而，对于很长的序列，实践中会遇到深层网络架构常见的梯度消失或梯度爆炸问题，使训练变得困难（见第 7.4.2 节）。

标准 RNN 的另一个问题是难以处理长距离依赖，而这在自然语言中尤其棘手，因为此类依赖十分普遍。在一大段文本中，可能先引入某个概念，它会在预测许多词之后的内容时起重要作用。在图 12.14 的架构中，整个英语句子的概念必须被捕捉在一个长度固定的隐藏向量 $\mathbf z^*$ 中；序列越长，这一点越困难。这称为**瓶颈问题**，因为任意长度的序列必须概括为单个激活值隐藏向量，而且网络只有在完整处理输入序列后才能开始生成译文。

解决梯度消失与爆炸，以及长距离依赖受限问题的一种方法，是修改神经网络架构，增加能绕过每个网络阶段内部许多处理步骤的信号路径，使信息在更多时间步内得到保留。**长短期记忆**（LSTM）模型（Hochreiter 和 Schmidhuber，1997）与**门控循环单元**（GRU）模型（Cho 等，2014）是最著名的例子。虽然它们比标准 RNN 性能更好，但建模长距离依赖的能力仍有限。每个单元的额外复杂性也使 LSTM 比标准 RNN 训练得更慢。此外，所有循环网络的信号路径长度都随序列步数线性增长。又由于处理是顺序进行的，它们不支持在单个训练样本内部并行计算。特别是，这意味着 RNN 难以高效利用基于 GPU 的现代高度并行硬件。用 Transformer 取代 RNN 可以解决这些问题。

## 12.3 Transformer 语言模型

Transformer 处理层是一个高度灵活的组件，可用于构建适用范围广泛的强大神经网络模型。本节探讨 Transformer 在自然语言中的应用。它推动了称为**大语言模型**（LLM）的巨型神经网络的发展，这类模型展现出非凡的能力（Zhao 等，2023）。

Transformer 可用于许多不同类型的语言处理任务；根据输入和输出数据的形式，可分为三类。在情感分析等问题中，输入是词序列，输出是一个代表文本情感的变量，例如快乐或悲伤。此时 Transformer 充当序列的“编码器”。另一些问题可能以单个向量为输入，生成词序列作为输出，例如根据输入图像生成文字说明。这时 Transformer 充当“解码器”，生成

<!-- pdf-page: 399 -->
<!-- join-previous-paragraph -->

输出序列。最后，在序列到序列的处理任务中，输入与输出都由词序列组成，例如将一种语言翻译成另一种语言。此时 Transformer 同时扮演编码器和解码器。下面依次讨论这三类语言模型，并以模型架构实例加以说明。

### 12.3.1 解码器 Transformer

先来看仅含解码器的 Transformer 模型。它们可作为生成输出 token 序列的生成模型。作为示例，我们重点讨论称为 **GPT** 的一类模型，即“生成式预训练 Transformer”（Radford 等，2019；Brown 等，2020；OpenAI，2023）。目标是用 Transformer 架构构造式 (12.31) 定义的自回归模型，其中条件分布 $p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1})$ 由从数据中学习的 Transformer 神经网络表示。

模型以序列的前 $n-1$ 个 token 为输入，相应的输出表示第 $n$ 个 token 的条件分布。如果从此分布采样，就把序列扩展为 $n$ 个 token；再将新序列输入模型，便得到第 $n+1$ 个 token 的分布，依此类推。可以重复这一过程，直到生成的序列达到由 Transformer 输入数量决定的最大长度。稍后我们将讨论从条件分布中采样的策略（见第 12.3.2 节），眼下先关注如何构造并训练网络。

GPT 模型的架构由多层堆叠的 Transformer 层组成：输入是维度均为 $D$ 的 token 序列 $\mathbf x_1,\ldots,\mathbf x_N$，输出是维度同样为 $D$ 的 token 序列 $\widetilde{\mathbf x}_1,\ldots,\widetilde{\mathbf x}_N$。每个输出都须表示该时间步 token 词典上的概率分布；而词典维度为 $K$，token 的维度为 $D$。因此，用一个维度为 $D\times K$ 的矩阵 $\mathbf W^{(p)}$ 对每个输出 token 作线性变换，再接 softmax 激活函数：

$$
\mathbf Y=\operatorname{Softmax}\!\left(\widetilde{\mathbf X}\mathbf W^{(p)}\right). \tag{12.33}
$$

其中，$\mathbf Y$ 的第 $n$ 行是 $\mathbf y_n^\mathsf T$，$\widetilde{\mathbf X}$ 的第 $n$ 行是 $\widetilde{\mathbf x}_n^\mathsf T$。每个 softmax 输出单元都有相应的交叉熵误差函数（见第 5.4.4 节）。模型架构见图 12.15。

可用大量无标注自然语言语料，采用自监督方法训练这个模型。每个训练样本包含输入网络的 token 序列 $\mathbf x_1,\ldots,\mathbf x_n$，以及由序列下一个 token $\mathbf x_{n+1}$ 构成的目标值。各序列视为独立同分布，因此训练误差函数是在整个训练集上求和的交叉熵误差，并将样本划分为适当的小批量。最直接的办法是对每个训练样本分别进行一次前向计算。但如果一次处理整个序列，就能大幅提高效率：每个 token 既是此前 token 序列的目标值，也是后续 token 的输入值。

<!-- pdf-page: 400 -->

<figure id="fig-12-15">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-15.png" alt="GPT 解码器网络，词嵌入加位置编码后进入多层带掩码的 Transformer 层，再经线性 softmax 输出">
  <figcaption>图 12.15：GPT 解码器 Transformer 网络的架构。这里“LSM”表示“线性 softmax”，即参数在各 token 位置共享的线性变换，后接 softmax 激活函数。正文解释了掩码。</figcaption>
  <p class="figure-translation">图内文字：embedding → 嵌入；positional encoding → 位置编码；masked transformer layer → 带掩码的 Transformer 层；$L$ layers → $L$ 层；LSM → 线性变换加 softmax；&lt;start&gt; → 开始 token；$\mathbf x_1,\ldots,\mathbf x_N$ → 输入 token；$\mathbf y_1,\ldots,\mathbf y_{N+1}$ → 输出分布。</p>
</figure>

例如，考虑下面这个词序列：

> I swam across the river to get to the other bank.（我游过河，到达了对岸。）

可以把“I swam across”用作输入序列，把“the”作为对应目标；也可以把“I swam across the”作为输入序列，把“river”作为目标，依此类推。然而，若要并行处理这些样本，就必须确保网络无法通过查看序列的后续部分来“作弊”，否则它只会学会把下一个输入直接复制到输出。一旦如此，在测试时就无法生成新序列，因为按定义，后续 token 此时尚不存在。为解决这个问题，我们采取两项措施。第一，将输入序列向右移动一步，使输入 $\mathbf x_n$ 对应输出 $\mathbf y_{n+1}$，目标为 $\mathbf x_{n+1}$；并在输入序列的第一个位置前加上特殊 token $\langle\mathrm{start}\rangle$。第二，注意 Transformer 中的 token 是独立处理的，唯有计算注意力权重时，它们通过点积成对交互。因此，我们在每个注意力层中引入**掩码注意力**，有时也称为**因果注意力**，

<!-- pdf-page: 401 -->

<figure id="fig-12-16">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-16.png" alt="因果自注意力的三角形掩码矩阵，红色上三角元素被置零">
  <figcaption>图 12.16：带掩码自注意力的掩码矩阵示意。红色元素对应的注意力权重设为零。因此，在预测 token“across”时，输出只能依赖输入 token“$\langle\mathrm{start}\rangle$”“I”和“swam”。</figcaption>
  <p class="figure-translation">图内文字：inputs → 输入；outputs → 输出；I → 我；swam → 游过；across → 穿过；the → 这／那（定冠词）；river → 河流；&lt;start&gt; → 开始 token。红色方格表示被掩码阻止关注的未来输入。</p>
</figure>

即把某个 token 关注序列中任何后续 token 的全部注意力权重置为零。为此，只需把式 (12.14) 定义的注意力矩阵 $\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)$ 中相应的所有元素置零，再将其余元素归一化，使每一行再次加和为 1。实践中可把相应的激活前数值设为 $-\infty$，这样 softmax 在关联输出上取零，并同时完成非零输出之间的归一化。图 12.16 展示了掩码注意力矩阵的结构。

**译注：** 原书这里把 $\operatorname{Attention}(\mathbf Q,\mathbf K,\mathbf V)$ 称作“注意力矩阵”，但式 (12.14) 已将 softmax 权重乘上 $\mathbf V$。掩码与按行归一化作用于 $\operatorname{Softmax}(\mathbf Q\mathbf K^{\mathsf T}/\sqrt{D_k})$ 的权重；实际实现通常在 softmax 前把未来位置的得分设为 $-\infty$。

实际应用中，我们希望高效利用 GPU 的大规模并行能力，因此可以将多个序列堆叠成输入张量，在单个批次中并行处理。不过，这要求序列长度相同，而文本序列天然长度不一。可以引入一个记作 $\langle\mathrm{pad}\rangle$ 的特定 token，填入闲置位置，把所有序列补到相同长度，从而合并为单个张量。然后再对注意力权重使用一个额外的掩码，确保输出向量不关注由 $\langle\mathrm{pad}\rangle$ token 占据的任何输入。注意，此掩码的具体形式依赖特定的输入序列。

训练后的模型输出是由 softmax 输出激活函数给出的 token 空间上的概率分布，它表示在当前 token 序列已知时下一个 token 的概率。选出这个下一个词后，可将包含新 token 的序列再次送入模型，生成序列中的后续 token；过程可无限重复，或直到生成序列结束 token 为止。这看起来可能效率不高，因为每生成一个新 token 都须把数据送过整个模型。不过，由于使用掩码注意力，某个 token 学到的嵌入只依赖该 token 本身及此前的 token，

<!-- pdf-page: 402 -->
<!-- join-previous-paragraph -->

因此在生成一个新的、更靠后的 token 时不会改变。于是，处理新 token 时可以重复利用相当一部分计算结果。

### 12.3.2 采样策略

我们已经看到，解码器 Transformer 输出的是序列中下一个 token 取值的概率分布，必须从中选出这个 token 的一个具体取值，才能扩展序列。根据计算出的概率，选择 token 取值有几种方法（Holtzman 等，2019）。一种显而易见的方法叫**贪心搜索**，即直接选择概率最高的 token。这样一来模型成为确定性的：同一输入序列始终生成同一输出序列。注意，在每一步选择概率最高的 token，并不等于选择概率最高的 token 序列。要找到概率最高的序列，需要最大化所有 token 上的联合分布（见习题 12.15）：

$$
p(\mathbf y_1,\ldots,\mathbf y_N)=\prod_{n=1}^{N}p(\mathbf y_n\mid\mathbf y_1,\ldots,\mathbf y_{n-1}). \tag{12.34}
$$

若序列有 $N$ 步，词典中 token 的取值数为 $K$，则序列总数为 $O(K^N)$，随长度呈指数增长，因此找出单个概率最高的序列不可行。相比之下，贪心搜索的成本是 $O(KN)$，随序列长度线性增长。

一种可能生成比贪心搜索概率更高的序列的技术是**束搜索**。它并非在每一步只选一个概率最高的 token，而是保留 $B$ 个假设；$B$ 称为**束宽**，每个假设都包含截至第 $n$ 步的一个 token 取值序列。然后将所有这些序列送入网络，对每个序列找出概率最高的 $B$ 个 token 取值，从而为扩展后的序列产生 $B^2$ 个可能的假设。接着根据扩展序列的总概率，只保留概率最高的 $B$ 个假设。这样，束搜索算法始终维持 $B$ 个候选序列并追踪其概率，最后从考虑过的序列中选择概率最高的一个。由于序列概率是各步概率的乘积，且这些概率都不大于 1，长序列的概率一般会低于短序列，因而结果偏向短序列。为此，在比较之前通常会按序列长度对其概率作归一化。束搜索的成本是 $O(BKN)$，同样随序列长度线性增长。不过，生成序列的成本增加了 $B$ 倍，因此对于推断成本可能相当显著的超大型语言模型，束搜索的吸引力大大降低。

贪心搜索和束搜索等方法的一个问题是，它们限制了潜在输出的多样性，甚至可能使生成过程陷入循环，让同一词子序列反复出现。

<!-- pdf-page: 403 -->

<figure id="fig-12-17">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-17.png" alt="束搜索与人类文本各时间步的 token 概率曲线对比">
  <figcaption>图 12.17：对于给定的已训练 Transformer 语言模型和初始输入序列，束搜索与人类文本的 token 概率对比。人类序列的 token 概率低得多。［经 Holtzman 等（2019）许可转载。］</figcaption>
  <p class="figure-translation">图内文字：Probability → 概率；Timestep → 时间步；Beam Search → 束搜索；Human → 人类文本。蓝色曲线为束搜索，橙色曲线为人类文本。</p>
</figure>

如图 12.17 所示，相对于给定模型，人类生成的文本可能概率更低，因此比自动生成的文本更出乎意料。

我们也可以不去寻找概率最高的序列，而是每一步直接从 softmax 分布中采样，逐个生成 token。不过，这可能产生没有意义的序列。原因在于，token 词典通常很大，存在由大量 token 状态构成的长尾；其中每个状态的概率都很小，但加总起来却占总概率质量的相当一部分。因此，系统在选择下一个 token 时有不可忽略的概率作出糟糕的选择。

为了在这些极端情况之间取得平衡，可以只考虑概率最高的 $K$ 个状态，其中 $K$ 为选定值，然后按重新归一化后的概率从中采样。这种方法的一个变体称为 **top-p 采样**或**核采样**：它从概率最高的输出开始累加概率，直到达到某个阈值，再从所得受限 token 状态集合中采样。

top-$K$ 采样的一个更“柔和”的版本是在 softmax 函数的定义中引入称为**温度**的参数 $T$（Hinton、Vinyals 和 Dean，2015），使

$$
y_i=\frac{\exp(a_i/T)}{\sum_j\exp(a_j/T)}, \tag{12.35}
$$

再从这一修改后的分布中采样下一个 token。当 $T=0$ 时，概率质量集中在概率最高的状态，其他所有状态的概率均为零，因此变为贪心选择。当 $T=1$ 时，

<!-- pdf-page: 404 -->
<!-- join-previous-paragraph -->

恢复为未经修改的 softmax 分布；当 $T\to\infty$ 时，分布趋于所有状态上的均匀分布。选择 $0<T<1$ 范围内的值，会使概率向较高值集中。

**译注：** 式 (12.35) 在 $T=0$ 时无定义；原书的“当 $T=0$ 时”应理解为 $T\to0^+$ 的极限。若有多个状态并列取得最大激活值，该极限在它们之间分配概率，还需约定如何破除并列才能作出唯一的贪心选择。

序列生成的一个挑战是：学习阶段，模型是在人类生成的输入序列上训练的；但以生成模式运行时，输入序列本身由模型生成。这意味着模型可能逐渐偏离训练中见过的序列分布。

### 12.3.3 编码器 Transformer

接下来考虑基于编码器的 Transformer 语言模型，它以序列为输入、输出类别标签等固定长度向量。这类模型的一个例子是 **BERT**，其全称为“双向 Transformer 编码器表示”（Devlin 等，2018）。目标是先用大量文本语料预训练语言模型，再利用迁移学习为广泛的下游任务微调模型；每个下游任务只需要一个较小的特定应用训练集。图 12.18 展示了编码器 Transformer 的架构。它是前文讨论的 Transformer 层的一种直接应用（见第 12.1.7 节）。

每个输入字符串的第一个 token 都是特殊的 $\langle\mathrm{class}\rangle$ token；预训练期间，模型对应位置的输出会被忽略。讨论微调时，它的作用就会清楚。预训练时，向模型输入 token 序列。随机选出其中一部分 token，例如 15%，用一个记作 $\langle\mathrm{mask}\rangle$ 的特殊 token 替换。训练模型在相应的输出节点预测缺失的 token。这类似于用 word2vec 学习词嵌入时的遮蔽（见第 12.2.1 节）。例如，输入序列可能是

> I &lt;mask&gt; across the river to get to the &lt;mask&gt; bank.

网络应在输出节点 2 预测“swam”，在输出节点 10 预测“other”。在这种情况下，只有两个输出对误差函数有贡献，其余输出都被忽略。

“双向”一词指网络既能看到被遮蔽词之前的词，也能看到之后的词，并可同时利用这两方面的信息作出预测。因此，与解码器模型不同，这里无须将输入右移一位，也无须在每层遮蔽后续输入 token，使其输出无法看到这些 token。相比解码器模型，编码器的效率较低，因为只有一部分序列 token 用作训练标签。此外，编码器模型无法生成序列。

随机选出的 token 用 $\langle\mathrm{mask}\rangle$ 替换，会使训练集与后续的微调集不匹配，因为微调集不含任何 $\langle\mathrm{mask}\rangle$ token。为缓解由此可能产生的问题，Devlin 等（2018）略微修改了过程：在随机选出的 15% token 中，80% 替换为 $\langle\mathrm{mask}\rangle$，10% 替换为从词表中随机选择的词，另有 10% 保留原词作为输入，但输出端仍须正确预测它们。

<!-- pdf-page: 405 -->

<figure id="fig-12-18">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-18.png" alt="BERT 式编码器 Transformer，输入加位置编码后经多层 Transformer 和线性 softmax 输出">
  <figcaption>图 12.18：编码器 Transformer 模型架构。标记为“LSM”的方框表示一个参数在 token 位置间共享的线性变换，后接 softmax 激活函数。与解码器模型相比，主要区别是输入序列不右移，而且省略了“向前看”掩码矩阵；因此，在每个自注意力层中，每个输出 token 都可关注任意输入 token。</figcaption>
  <p class="figure-translation">图内文字：embedding → 嵌入；positional encoding → 位置编码；transformer layer → Transformer 层；$L$ layers → $L$ 层；LSM → 线性变换加 softmax；&lt;class&gt; → 分类 token；$\mathbf c$ → 类别向量；$\mathbf x_1,\ldots,\mathbf x_N$ → 输入 token；$\mathbf y_1,\ldots,\mathbf y_N$ → 输出。</p>
</figure>

编码器模型训练好以后，可针对多种不同任务进行微调。为此，构造一个形式针对具体任务的新输出层。对于文本分类任务，只使用第一个输出位置；它对应始终位于输入序列首位的 $\langle\mathrm{class}\rangle$ token。如果该输出的维度为 $D$，就在第一个输出节点后添加一个维度为 $D\times K$ 的参数矩阵，其中 $K$ 是类别数；矩阵的输出再送入 $K$ 维 softmax 函数。若 $K=2$，也可以使用一个 $D\times1$ 的向量后接逻辑 sigmoid。线性输出变换还可换成 MLP 等更复杂的可微模型。如果目标是对输入字符串的每个 token 进行分类，例如将每个 token 分到某个类别（人、地点、颜色等），就忽略第一个输出，让其余输出使用共享的线性变换加 softmax 层。微调期间，包括新输出矩阵在内的全部模型参数都使用

<!-- pdf-page: 406 -->
<!-- join-previous-paragraph -->

正确标签的对数概率，通过随机梯度下降学习。

也可以把预训练模型的输出送入复杂的生成式深度学习模型，用于文本生成图像等应用（见第 20 章）。

### 12.3.4 序列到序列 Transformer

为完整起见，简要讨论第三类 Transformer 模型：它结合了编码器与解码器，正如 Vaswani 等（2017）提出的原始 Transformer 论文所讨论的那样。考虑把英语句子翻译成荷兰语。可用前述解码器模型逐个 token 地生成对应荷兰语输出的 token 序列（见第 12.3.1 节）。主要区别是，该输出需要以完整的英语输入序列为条件。编码器 Transformer 可以将输入 token 序列映射为合适的内部表示，记为 $\mathbf Z$。为了把 $\mathbf Z$ 纳入输出序列的生成过程，我们使用一种改进的注意力机制，称为**交叉注意力**。它与自注意力相同，唯一区别是：查询向量来自正在生成的序列，这里是荷兰语输出序列；键向量和值向量则来自 $\mathbf Z$ 所表示的序列，如图 12.19 所示。回到视频流媒体服务的类比，这相当于用户把查询向量发给另一家流媒体公司，由该公司与自己的键向量集合比较，找出最佳匹配，然后以影片形式返回关联的值向量。

将编码器和解码器模块结合，就得到图 12.20 所示的模型架构。可以使用成对的输入与输出句子训练该模型。

### 12.3.5 大语言模型

机器学习领域近来最重要的发展，是为自然语言处理构建了基于 Transformer 的超大型神经网络，即**大语言模型**（LLM）。这里的“大”指网络中的权重与偏置参数数量；截至本书写作时，数量可达约一万亿（$10^{12}$）。训练这类模型成本高昂，之所以要构建它们，是因为其能力非凡。

除了大型数据集的可用性外，基于 GPU（图形处理器）和类似处理器的大规模并行训练硬件的出现，也推动了越来越大型的模型训练。这些处理器组成大型集群，配备高速互连及大量板载内存。Transformer 架构在此类模型的发展中发挥了关键作用，因为它能非常高效地利用这些硬件。很多时候，增加训练数据集的规模，同时相应增加模型参数数量，带来的性能提升会超过改进架构或纳入更多领域知识的其他方法（Sutton，2019；Kaplan 等，2020）。例如，GPT 系列模型在连续几代中令人印象深刻的性能提升，主要来自规模扩大（Radford 等，2019；Brown 等，2020；OpenAI，2023）。

<!-- pdf-page: 407 -->

<figure id="fig-12-19">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-19.png" alt="序列到序列 Transformer 解码器中的交叉注意力层，键和值来自编码器 Z，查询来自解码器">
  <figcaption>图 12.19：序列到序列 Transformer 解码器部分中一个交叉注意力层的示意图。$\mathbf Z$ 表示编码器部分的输出。$\mathbf Z$ 决定交叉注意力层的键向量和值向量，而查询向量由解码器部分决定。</figcaption>
  <p class="figure-translation">图内文字：masked multi-head self-attention → 带掩码的多头自注意力；multi-head cross-attention → 多头交叉注意力；add &amp; norm → 相加并归一化；MLP → 多层感知机；$\mathbf X$ → 解码器输入；$\mathbf Z$ → 编码器输出；K、V、Q → 键、值、查询；$\widetilde{\mathbf X}$ → 输出。</p>
</figure>

这类性能提升推动了一种新的“摩尔定律”：自大约 2012 年以来，训练最先进机器学习模型所需的计算操作数一直呈指数增长，倍增时间约为 3.4 个月（见图 1.16）。

早期语言模型通过监督学习训练。例如，为构建翻译系统，训练集由两种语言中相互匹配的句子对组成。然而，监督学习的一个主要局限是，数据通常必须经人工整理以提供有标签的样本，因而可用数据量受到严重限制；为了达到合理性能，就必须大量使用特征工程和架构约束等归纳偏置。

相反，大语言模型利用极大型文本数据集，以及可能存在的计算机代码等其他 token 序列，以自监督学习训练。我们已看到如何训练解码器 Transformer（见第 12.3.1 节）：在 token 序列中，每个 token 都作为一个有标签的目标样本，此前的序列作为输入，以学习条件概率分布。这种“自我标注”极大地扩大了可用训练数据的数量，因而能充分利用具有大量参数的深度神经网络。

<!-- pdf-page: 408 -->

<figure id="fig-12-20">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-20.png" alt="序列到序列 Transformer 中编码器输出 Z 输入解码器交叉注意力层，输出 Y_N 自回归反馈">
  <figcaption>图 12.20：序列到序列 Transformer 的示意图。为避免图示繁杂，输入 token 合并画作单个方框，输出 token 亦然。编码器和解码器部分都给输入 token 加上位置编码向量。编码器的每一层都对应图 12.9 所示结构，每个交叉注意力层的形式如图 12.19 所示。</figcaption>
  <p class="figure-translation">图内文字：encoder → 编码器；decoder → 解码器；embedding → 嵌入；positional encoding → 位置编码；self-attention transformer layer → 自注意力 Transformer 层；cross-attention transformer layer → 交叉注意力 Transformer 层；LSM → 线性变换加 softmax；$\mathbf X$ → 输入序列；$\mathbf Z$ → 编码器表示；$\{\langle\mathrm{start}\rangle,\mathbf Y_{1:N-1}\}$ → 解码器输入；$\mathbf Y_N$ → 当前输出。</p>
</figure>

自监督学习的使用带来了一次范式转变：先用无标注数据预训练一个大型模型，再用少量有标注数据通过监督学习微调。这实际上是一种迁移学习，而且同一个预训练模型可用于多个“下游”应用。具有广泛能力、随后可为特定任务微调的模型称为**基础模型**（Bommasani 等，2021）。

微调可以通过在网络输出端增加额外的层，或者将最后几层替换为新参数，再用有标注数据训练这些末端层来完成。微调期间，主模型中的权重和偏置既可以保持不变，也可以允许少量调整。一般来说，微调成本与预训练相比很低。

一种非常高效的微调方法称为**低秩适配**（LoRA；Hu 等，2021）。这种方法受到以下结果的启发：一个已训练的过参数化模型在微调方面具有较低的内在维度，即微调时模型参数的变化位于一个流形上，

<!-- pdf-page: 409 -->

<figure id="fig-12-21">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-21.png" alt="低秩适配的矩阵乘法示意，原权重 W0 与附加矩阵 A B 的乘积共同作用于 X">
  <figcaption>图 12.21：低秩适配的示意图，展示预训练 Transformer 某个注意力层中的权重矩阵 $\mathbf W_0$。附加的矩阵 $\mathbf A$ 和 $\mathbf B$ 在微调期间适配；后续推断时，将其乘积 $\mathbf A\mathbf B$ 加到原矩阵上。</figcaption>
  <p class="figure-translation">图内符号：$\mathbf X$ → 输入；$\mathbf W_0$ → 冻结的原权重；$\mathbf A$、$\mathbf B$ → 可学习低秩矩阵；$\mathbf X\mathbf W_0+\mathbf X\mathbf A\mathbf B$ → 合成输出；$N\times D$、$D\times D$、$D\times R$、$R\times D$ → 矩阵维度。</p>
</figure>

其维度远小于模型可学习参数的总数（Aghajanyan、Zettlemoyer 和 Gupta，2020）。LoRA 据此冻结原模型的权重，并在 Transformer 的每一层加入以低秩乘积形式表示的额外可学习权重。通常只修改注意力层的权重，MLP 层的权重则保持固定。考虑一个维度为 $D\times D$ 的权重矩阵 $\mathbf W_0$，它可以表示查询、键或值矩阵，其中多个注意力头的矩阵合并视为一个矩阵。我们引入一组并行权重，由两个矩阵 $\mathbf A$ 和 $\mathbf B$ 的乘积定义；它们的维度分别为 $D\times R$ 和 $R\times D$，如图 12.21 所示。该层的输出为 $\mathbf X\mathbf W_0+\mathbf X\mathbf A\mathbf B$。附加权重矩阵 $\mathbf A\mathbf B$ 的参数数量为 $2RD$，而原权重矩阵 $\mathbf W_0$ 的参数数量为 $D^2$；因此，如果 $R\ll D$，微调时需要适配的参数数量远小于原 Transformer 中的参数数量。实践中，需要训练的参数数量可减少至原来的约万分之一。微调完成后，可将附加权重加到原权重矩阵中，得到新权重矩阵

$$
\widehat{\mathbf W}=\mathbf W_0+\mathbf A\mathbf B. \tag{12.36}
$$

于是推断时，与运行原模型相比没有额外计算开销，因为更新后的模型大小与原模型相同。

随着语言模型变得更大、更强，微调的必要性已有所降低；现在，生成式语言模型只通过文本交互就能解决广泛的任务。例如，如果把下面的文本字符串作为输入序列：

> English: the cat sat on the mat. French:

自回归语言模型就能继续生成后续 token，直到生成 $\langle\mathrm{stop}\rangle$ token；新生成的

<!-- pdf-page: 410 -->
<!-- join-previous-paragraph -->

token 代表法语译文。注意，该模型并非专门针对翻译进行训练，而是在包含多种语言的大量数据上训练后学会了翻译。

用户可以通过自然语言对话与这类模型交互，因此广大受众也能方便地使用它们。为了改善用户体验和生成结果的质量，人们开发了通过人工评价生成结果来微调大语言模型的技术，例如**基于人类反馈的强化学习**（RLHF；Christiano 等，2017）。这些技术有助于造就对话界面格外易用的大语言模型，其中最著名的是 OpenAI 的 ChatGPT 系统。

用户给出的一串输入 token 称为**提示词**。例如，它可以是故事的开头几个词，要求模型将其续写；也可以是一个问题，要求模型回答。使用不同提示词，同一个经过训练的神经网络便可能完成广泛的任务，例如依据简单文本请求生成计算机代码，或者按要求写押韵诗。模型性能现在取决于提示词的形式，由此产生一个新领域，称为**提示词工程**（Liu 等，2021），旨在设计能为下游任务生成高质量输出的提示词形式。还可以先调整用户的提示词，再送入语言模型，以改变模型行为：在用户提示词前面添加一串额外的 token，称为**前缀提示词**，用于修改输出形式。例如，这段前置提示词可以是用标准英语表达的指令，要求网络在输出中不包含冒犯性语言。

这样一来，只要在提示词中提供几个示例，无须调整模型参数，就可以让模型解决新任务。这是**少样本学习**的一个例子。

诸如 GPT-4 等当时最先进的模型，能力已强大到展现出引人注目的性质，有人将其描述为通用人工智能的最初迹象（Bubeck 等，2023），并正在推动新一波技术创新。此外，这些模型的能力仍在以令人印象深刻的速度提高。

## 12.4 多模态 Transformer

虽然 Transformer 最初是作为处理序列语言数据的循环网络替代方案而开发的，但如今已在几乎所有深度学习领域得到广泛应用。它已被证明是一种通用模型，对输入数据只作很少的假设；相比之下，卷积网络对等变性和局部性有很强的假设（见第 10 章）。由于这种通用性，Transformer 在文本、图像、视频、点云和音频数据等许多不同模态上都已达到最先进水平，并用于各领域中的判别式和生成式应用。

<!-- pdf-page: 411 -->
<!-- join-previous-paragraph -->

Transformer 层的核心架构，随时间推移以及在不同应用中，都保持得相对稳定。因此，使 Transformer 能够用于自然语言以外领域的关键创新，主要集中在输入和输出的表示与编码上。

能够处理多种数据的单一架构有一大优势：多模态计算因而相对直接。这里的“多模态”指在输入或输出或两者中结合两种以上不同数据的应用。例如，我们可能希望从文本提示生成图像，或者设计一个结合摄像头、雷达、麦克风等多种传感器信息的机器人。要注意的关键点是：只要能把输入 token 化，并能解码输出 token，就很可能可以使用 Transformer。

### 12.4.1 视觉 Transformer

Transformer 已成功应用于计算机视觉，并在许多任务上达到最先进的性能。对于判别式任务，最常见的选择是标准 Transformer 编码器；视觉领域的这种方法称为**视觉 Transformer**，简称 **ViT**（Dosovitskiy 等，2020）。

使用 Transformer 时，需要决定如何把输入图像转换成 token。最简单的选择是先作线性投影，再把每个像素用作一个 token。不过，标准 Transformer 实现所需的内存随输入 token 数量的平方增长，因此一般不可行。最常见的 token 化方法是将图像分成一组大小相同的图块。假设图像维度为 $\mathbf x\in\mathbb R^{H\times W\times C}$，其中 $H$ 和 $W$ 是以像素为单位的高度和宽度，$C$ 是通道数（对红、绿、蓝三种颜色，通常 $C=3$）。将每幅图像分成大小为 $P\times P$ 的非重叠图块（常选 $P=16$），然后把每个图块“展平”为一维向量，得到表示 $\mathbf x_p\in\mathbb R^{N\times(P^2C)}$，其中 $N=HW/P^2$ 是一幅图像的图块总数。ViT 架构见图 12.22。

另一种 token 化方法是让图像先通过一个小型卷积神经网络（CNN）。这可以将图像降采样，得到数量可控的 token，每个 token 由一个网络输出表示。例如，典型的 ResNet18 编码器架构在高度和宽度方向上都将图像降采样 8 倍，因此 token 数量是像素数量的六十四分之一（见第 10 章）。

还需要一种方法，把位置信息编码到 token 中。可以构造明确的位置嵌入，编码图像图块的二维位置信息，但实践中这通常不能提高性能，因此最常用的是可学习的位置嵌入。与用于自然语言的 Transformer 不同，视觉 Transformer 一般接受固定数量的 token 作为输入，因而避免了可学习位置编码无法推广到不同尺寸输入的问题。

视觉 Transformer 与 CNN 的架构设计大不相同。CNN 模型内置了强归纳偏置，而视觉 Transformer 中唯一的二维归纳偏置来自对输入进行 token 化时所用的图块。

<!-- pdf-page: 412 -->

<figure id="fig-12-22">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-22.png" alt="小猫图像切成图块，展平并嵌入后加位置编码，送入 Transformer 编码器分类">
  <figcaption>图 12.22：用于分类任务的视觉 Transformer 架构。这里把一个可学习的 $\langle\mathrm{class}\rangle$ token 作为额外输入，与之关联的输出通过一个带 softmax 激活的线性层（记作 LSM）变换，得到最终的类别向量输出 $\mathbf c$。</figcaption>
  <p class="figure-translation">图内文字：flatten → 展平；embedding → 嵌入；learned positional encoding → 可学习的位置编码；transformer encoder → Transformer 编码器；LSM → 线性变换加 softmax；&lt;class&gt; → 分类 token；$\mathbf c$ → 类别输出。</p>
</figure>

因此，与类似的 CNN 相比，Transformer 通常需要更多训练数据，因为它必须从零学起图像的几何性质。不过，由于它对输入结构没有强假设，Transformer 往往能够收敛到更高的准确率。这再次说明了归纳偏置与训练数据规模之间的权衡（Sutton，2019）。

### 12.4.2 生成式图像 Transformer

在语言领域，当 Transformer 作为用于合成文本的自回归生成模型时，取得了最令人印象深刻的结果。因此，自然要问：是否也能用 Transformer 合成逼真的图像？自然语言本身具有序列性质，因而适合自回归框架；图像的像素却没有天然顺序，所以对像素作自回归解码的用处并不那么直观。然而，只要先为变量定义某种顺序，任何分布都能分解为条件分布的乘积（见第 11.1.2 节）。因此，我们可以对一组有序变量写出联合分布的分解。

<!-- pdf-page: 413 -->

<figure id="fig-12-23">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-23.png" alt="四乘四像素网格中的红色栅格扫描路径，从 x1 到 x16">
  <figcaption>图 12.23：栅格扫描示意图，定义了二维图像像素的一种特定线性顺序。</figcaption>
  <p class="figure-translation">图内标记：$x_1,\ldots,x_{16}$ → 按栅格扫描顺序编号的像素；红色箭头 → 逐行扫描方向。</p>
</figure>

对于有序变量 $\mathbf x_1,\ldots,\mathbf x_N$，联合分布可写为

$$
p(\mathbf x_1,\ldots,\mathbf x_N)=\prod_{n=1}^{N}p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1}). \tag{12.37}
$$

这一分解完全一般化，并未对各个条件分布 $p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1})$ 的形式施加限制。

对于图像，可令 $\mathbf x_n$ 表示由 RGB 值构成的第 $n$ 个像素三维向量。现在须决定像素的排列顺序，一个广泛使用的选择称为**栅格扫描**，如图 12.23 所示。图 12.24 示意了如何依据栅格扫描顺序，使用自回归模型生成图像。

注意，用于图像的自回归生成模型早于 Transformer 出现。例如，PixelCNN（Oord 等，2016）和 PixelRNN（Oord、Kalchbrenner 和 Kavukcuoglu，2016）使用特制的带掩码卷积层，保持式 (12.37) 右侧每个对应项为各像素定义的条件独立关系。

图像的连续值表示可很好地用于判别任务。但在图像生成中，使用离散表示的结果要好得多。通过极大似然学习的连续条件分布，例如其负对数似然函数是平方和误差函数的高斯分布，往往学到训练数据的平均值，导致图像模糊（见第 4.2 节）。相反，离散分布能轻松处理多模态。例如，式 (12.37) 中的某个条件分布 $p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1})$ 可能学到某个像素既可以为黑色也可以为白色，而回归模型则可能学到这个像素应为灰色。

<figure id="fig-12-24">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-24.png" alt="图像从空白开始，按像素栅格顺序逐步采样，最终形成小猫图像">
  <figcaption>图 12.24：从自回归模型采样图像的示意图。第一个像素从边缘分布 $p(\mathbf x_{11})$ 采样，第二个像素从条件分布 $p(\mathbf x_{12}\mid\mathbf x_{11})$ 采样，再依栅格扫描顺序继续，直至得到完整图像。</figcaption>
  <p class="figure-translation">图内箭头表示按栅格扫描顺序逐步生成；省略号表示中间采样步骤。</p>
</figure>

<!-- pdf-page: 414 -->

不过，处理离散空间也有挑战。图像像素的 R、G、B 值通常各以至少 8 位精度表示，因此每个像素有 $2^{24}\simeq 1600$ 万种可能取值。在如此高维的空间上学习条件 softmax 分布不可行。

解决高维问题的一种方法是使用**向量量化**技术，它可视为一种数据压缩形式（见第 15.1.1 节）。假设有一组维度均为 $D$ 的数据向量 $\mathbf x_1,\ldots,\mathbf x_N$，例如图像像素；然后引入一组维度同样为 $D$ 的 $K$ 个码本向量 $\mathcal C=\{\mathbf c_1,\ldots,\mathbf c_K\}$，其中通常 $K\ll D$。现在按某种相似性度量（通常为欧氏距离），用最近的码本向量近似每个数据向量：

$$
\mathbf x_n\longrightarrow\mathop{\arg\min}_{\mathbf c_k\in\mathcal C}\|\mathbf x_n-\mathbf c_k\|^2. \tag{12.38}
$$

由于共有 $K$ 个码本向量，可以用一个独热编码的 $K$ 维向量表示每个 $\mathbf x_n$。又由于可选择 $K$，便能控制两者的权衡：较大的 $K$ 能更准确地表示数据，较小的 $K$ 则能实现更高压缩率。

因此，可以把原始图像像素映射到维度较低的码本空间。随后训练自回归 Transformer 生成码本向量序列；再以对应的 $D$ 维码本向量 $\mathbf c_k$ 替换每个码本索引 $k$，把序列映射回原始图像空间。

自回归 Transformer 最早在 ImageGPT 中用于图像（Chen、Radford 等，2020）。这里每个像素都被视为离散的三维颜色码本向量集合中的一个，其每个向量对应颜色空间中 $K$ 均值聚类的一个簇（见第 15.1 节）。因此，独热编码产生了类似语言 token 的离散 token，使 Transformer 可像语言模型一样，以预测下一个 token 的分类目标来训练。这是用于学习表示、供后续微调使用的强大目标，与语言建模的情况相似（见第 6.3.3 节）。

不过，直接用单个像素作为 token 会导致高计算成本，因为每个像素都需要一次前向计算，训练和推断随图像分辨率的扩展性都很差。此外，若用单个像素作为输入，为在栅格扫描后段解码像素时保持合理的上下文长度，就不得不使用低分辨率图像。正如 ViT 模型所示，用图块而非像素作为 token 更合适，因为它能大幅减少 token 数量，从而便于处理更高分辨率的图像。和前面一样，由于条件分布可能具有多模态性，必须在离散的 token 取值空间中操作。这又带来维度方面的挑战，而且图块比单个像素严重得多，因为其维度随图块中像素的数量呈指数增长。例如，考虑每个像素 token 只有黑白两种可能取值的情形。

<!-- pdf-page: 415 -->

<figure id="fig-12-25">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-25.png" alt="座头鲸鸣声的梅尔频谱图，横轴为时间，纵轴为频率">
  <figcaption>图 12.25：座头鲸鸣声的梅尔频谱图示例。［源数据版权 ©2013–2023，librosa 开发团队。］</figcaption>
  <p class="figure-translation">图内文字：time → 时间；frequency → 频率。</p>
</figure>

若图块大小为 $16\times16$，图块 token 词典也需要 $2^{256}\simeq10^{77}$ 个条目。

为解决维度问题，我们再次使用向量量化。可通过 $K$ 均值等简单聚类算法，在图像图块数据集上学习码本向量；也可使用全卷积网络（Oord、Vinyals 和 Kavukcuoglu，2017；Esser、Rombach 和 Ommer，2020）乃至视觉 Transformer（Yu 等，2021）等更复杂的方法。学习把每个图块映射到一组离散码并再映射回来的一个问题是，向量量化是不可微的。幸运的是，可以使用**直通梯度估计**（Bengio、Léonard 和 Courville，2013）：这是一种简单近似，在反向传播期间直接把梯度复制穿过不可微函数。

通过把视频视为这类向量量化 token 的一个长序列，可将自回归 Transformer 生成图像的方法扩展到视频（Rakhimov 等，2020；Yan 等，2021；Hu 等，2023）。

### 12.4.3 音频数据

接下来考察 Transformer 在音频数据中的应用。声音通常存储为波形，由定期测量气压幅度得到。虽然这种波形可直接作为深度学习模型的输入，但实践中先把它预处理为**梅尔频谱图**更有效。它是一个矩阵，列表示时间步，行对应频率。频段遵循一项标准约定，该约定通过主观评估选择，使相邻频率之间具有相等的感知差异（“mel”一词来自 melody，即“旋律”）。图 12.25 给出了一个梅尔频谱图示例。

Transformer 在音频领域的一项应用是分类：将音频片段分到预定义类别之一。例如，AudioSet 数据集（Gemmeke 等，2017）是广泛使用的基准。

<!-- pdf-page: 416 -->
<!-- join-previous-paragraph -->

它包含“汽车”“动物”和“笑声”等类别。在 Transformer 出现之前，音频分类的最先进方法，是将梅尔频谱图视为图像，作为卷积神经网络（CNN）的输入。虽然 CNN 擅长理解局部关系，但它的一个缺点是难以处理长距离依赖，而这在音频处理中可能很重要（见第 10 章）。

正如 Transformer 在自然语言处理中取代 RNN 成为最先进方法一样，它也开始在音频分类等任务中取代 CNN。例如，可使用与语言和视觉领域结构相同的 Transformer 编码器模型（见图 12.18）来预测音频输入的类别（Gong、Chung 和 Glass，2021）。这里把梅尔频谱图视为一幅图像，再将它 token 化。做法与视觉 Transformer 相似：将图像分成图块，图块之间可能略有重叠，以免丢失重要的邻域关系。然后将每个图块展平，即转换为一个一维数组，此处长度为 256。再为每个 token 加入唯一的位置编码，附加一个特定的 $\langle\mathrm{class}\rangle$ token，随后将这些 token 送入 Transformer 编码器。最后一个 Transformer 层中与 $\langle\mathrm{class}\rangle$ 输入 token 对应的输出 token，可通过一个线性层及随后的 softmax 激活函数进行解码；整个模型可用交叉熵损失端到端训练。

### 12.4.4 文本转语音

分类并非深度学习，尤其是 Transformer 架构，在音频领域带来革命性变化的唯一任务。Transformer 成功合成了模仿给定说话人声音的语音，再次证明了其通用性；它在这一任务上的应用也是如何将 Transformer 用于新场景的一个有启发性的案例。

生成与给定文本段落对应的语音，称为**文本转语音合成**。一种更传统的方法是收集某个说话人的语音录音，训练监督式回归模型，从对应的转写文本预测语音输出，输出可能是梅尔频谱图的形式。在推断时，将希望合成为语音的文本作为输入，再把得到的梅尔频谱图输出解码回音频波形，因为这一映射是固定的。

然而，这种方法有几项重大缺点。首先，如果在较低层级预测语音，例如使用称为音素的亚词成分，则需要更大的上下文，才能让生成的句子听起来自然流畅。但如果预测更长的片段，可能输入的空间又会显著增大，为实现良好泛化可能需要数量无法承受的训练数据。其次，这种方法不能跨说话人迁移知识，因此对每个新说话人都需要大量数据。最后，这个问题实际上是生成式建模任务，因为给定说话人和文本，可以有多种正确的语音输出；回归倾向于对目标值取平均，因此可能并不合适（见第 4.2 节）。

如果改为像处理自然语言一样处理音频数据，把文本转语音视为条件语言建模任务，那么我们应能以与基于文本的大语言模型大体相同的方式训练模型。

<!-- pdf-page: 417 -->

<figure id="fig-12-26">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-26.png" alt="Vall-E 文本转语音架构：文本提示 token 与声学提示经 Transformer，音频解码器输出合成语音">
  <figcaption>图 12.26：Vall-E 高层架构图。Transformer 模型的输入包括标准文本 token，用于提示合成语音应包含哪些词；还包括决定说话人风格和语气信息的声学提示 token。采样得到的模型输出 token 经已学习的解码器转换回语音。为简洁起见，图中未显示位置编码和线性投影。</figcaption>
  <p class="figure-translation">图内文字：text prompt tokens → 文本提示 token；acoustic prompt → 声学提示；discrete tokenizer → 离散 token 化器；transformer → Transformer；audio decoder → 音频解码器；synthesized speech → 合成语音。</p>
</figure>

需要解决两个主要的实现问题：一是如何将训练数据 token 化并解码预测结果，二是如何以说话人的声音为条件来控制模型。

一种使用 Transformer 和语言建模技术的文本转语音方法是 Vall-E（Wang 等，2023）。只需提供某个新说话人几秒钟的样本语音，就能用这个人的声音将新文本转换为语音。语音数据通过向量量化，转换为从已学习的词典或码本中选取的离散 token 序列（见第 12.4.2 节）；可将这些 token 类比为自然语言领域的独热编码 token。输入由一段文本的文本 token 构成，而训练时的目标输出是对应的语音 token。此外，还将同一说话人的一小段无关语音所产生的语音 token

<!-- pdf-page: 418 -->
<!-- join-previous-paragraph -->

附加到输入文本 token 后面，如图 12.26 所示。通过纳入许多不同说话人的样本，系统能学会在朗读文本时模仿额外语音输入 token 所代表的声音。训练完成后，可向系统提供新文本，以及来自一位新说话人一小段语音的音频 token；再用训练时的同一码本解码所得输出 token，生成语音波形。于是系统能够用新说话人的声音，合成与输入文本对应的语音。

### 12.4.5 视觉与语言 Transformer

我们已经看到如何为文本、音频和图像生成离散 token，下一步自然会问：是否能训练一个模型，以一种模态的 token 为输入、另一种模态的 token 为输出？又或者，是否能在输入、输出或两者中混合不同模态？我们将重点讨论文本与视觉数据的结合，因为这是研究最广泛的例子；不过，原则上这里讨论的方法也可用于其他输入与输出模态组合。

首要条件是有大量训练数据。LAION-400M 数据集（Schuhmann 等，2021）极大地推动了文本生成图像与图像生成文字描述的研究，正如 ImageNet 对深度图像分类模型的发展至关重要。文本生成图像实际上与迄今讨论的无条件图像生成十分相似，只是我们还允许模型把文本信息作为输入，以生成过程的条件。在使用 Transformer 时，这很直接：解码每个图像 token 时，只需额外提供文本 token 作为输入。

这种方法也可看作把文本生成图像问题视为类似机器翻译的序列到序列语言建模问题，只是目标 token 变成离散图像 token，而不是语言 token。因此，采用图 12.20 所示的完整编码器—解码器 Transformer 模型是合理的，其中 $\mathbf X$ 对应输入文本 token，$\mathbf Y$ 对应输出图像 token。名为 Parti 的模型采用了这种方法（Yu 等，2022），将 Transformer 扩大到 200 亿个参数，并显示出随模型规模增加而持续提升的性能。

还有很多研究尝试使用预训练语言模型，通过修改或微调使其也能接受视觉数据作为输入（Alayrac 等，2022；Li 等，2022）。这些方法大多使用特制架构和连续值图像 token，因此不太适合同时生成视觉数据。而且，若想加入音频 token 等新模态，也不能直接使用它们。虽然这是朝多模态迈出的一步，但理想情况下，我们希望文本 token 和图像 token 都能同时充当输入和输出。最简单的办法是把所有内容都当作 token 序列来处理，仿佛处理自然语言，只是将语言 token 词典与图像 token 码本拼接成一个新词典。这样便可把任何音频和视觉数据流直接视为 token 序列。

<!-- pdf-page: 419 -->

<figure id="fig-12-27">
  <img src="books/bishop-deep-learning-2024/assets/chapter-12/fig-12-27.png" alt="CM3Leon 在图文混合文档、文本生成图像、图像生成文字等任务上的示例组合图">
  <figcaption>图 12.27：CM3Leon 模型在文本与图像的联合空间中完成多种不同任务的示例。［经 Yu 等（2023）许可转载。］</figcaption>
  <p class="figure-translation">图内标题：Interleaved texts and images → 图文交织；Text-Guided Editing → 文本引导编辑；Pix2pix: RDEdit → 图像编辑方法名（保留原名）；Image-to-Image Grounded Generation → 图像到图像的定位生成；Scribble → 涂鸦；Poses → 姿态；Generated images → 生成的图像；Text to image task → 文本生成图像任务；Image to text tasks → 图像生成文本任务；Generated text → 生成的文本；CM3Leon → 模型名称。各示例中的完整英文译文见紧随本图的译注。</p>
</figure>

<aside class="figure-translation">图 12.27 图内示例译注：上方第一行“Edit the image following the text instruction” → “按照文字指令编辑图像”；“Make her an alien” → “把她变成外星人”。第二行“Make high quality image from children's scribbles and text description” → “根据儿童涂鸦和文字描述制作高质量图像”；“The common kingfisher (Alcedo atthis) also known as the Eurasian kingfisher and river kingfisher sitting on branch” → “一只普通翠鸟（学名 Alcedo atthis，亦称欧亚翠鸟或河翠鸟）停在树枝上”。第三行“Make high quality image from pose features and text description” → “根据姿态特征和文字描述制作高质量图像”；“A woman practices yoga on a cross-legged sport mat” → “一名女子盘腿坐在运动垫上练习瑜伽”。左侧中部“Spatially Grounded: Fabricate an image of a contemporary kitchen with a refrigerator at the location (50, 50) → (100, 100), and stoves at the location (80, 80) → (200, 200)” → “空间定位：生成一幅现代厨房图像，将冰箱放在坐标 (50, 50) 至 (100, 100) 处、炉灶放在 (80, 80) 至 (200, 200) 处”；“How-to-write: A white sign that says ‘morning’” → “文字书写：一块写着‘morning’（早晨）的白色标牌”。左下“Caption: Describe the given image” → “图注：描述所给图像”；“Long Caption: Describe the given image in very detail” → “长图注：非常详细地描述所给图像”；“VQA: Question: what time of the day is the photo taken?” → “视觉问答：问题：照片拍摄于一天中的什么时段？”；“Reasoning: Question: Does this passage describe the weather or the climate? Context: Figure: Des Moines. The temperature recorded … Please explain your answer.” → “推理：问题：这段文字描述的是天气还是气候？背景：图：得梅因。记录的气温……请解释你的答案。”右下生成文字：“A beautiful view of a city from across a river.” → “隔河望去，一座城市的景色十分美丽。”；“A view of tall buildings in a city. The photo is taken from a park across a river. We can see a bridge over the river.” → “城市高楼的景色。这张照片从河对岸的公园拍摄，可以看到河上的一座桥。”；“Sunset time” → “日落时分”；“Weather. Because the atmosphere is the layer of air that surrounds Earth. Both weather and climate tell you about the atmosphere. …” → “天气。因为大气是环绕地球的空气层。天气和气候都涉及大气……”</aside>

在 CM3（Aghajanyan 等，2022）和 CM3Leon（Yu 等，2023）中，模型采用一种语言建模变体，在来自在线来源、同时包含图像和文本数据的 HTML 文档上训练。当大量训练数据与可扩展架构结合时，这些模型变得非常强大。此外，由于训练数据具有多模态性质，模型十分灵活。它们能够完成许多原本可能需要专门模型架构与训练方案的任务，例如文本生成图像、图像生成文字描述、图像编辑、文本补全等，也包括普通语言模型能完成的各种任务。图 12.27 展示了 CM3Leon 模型完成若干不同任务的例子。

## 习题

**12.1（★★）** 考虑一组系数 $a_{nm}$，其中 $m=1,\ldots,N$，满足

$$
a_{nm}\geqslant0 \tag{12.39}
$$

及

$$
\sum_m a_{nm}=1. \tag{12.40}
$$

<!-- pdf-page: 420 -->

使用拉格朗日乘子证明，这些系数还须满足（见附录 C）

$$
a_{nm}\leqslant1,\qquad n=1,\ldots,N. \tag{12.41}
$$

**12.2（★）** 验证：对于任意向量 $\mathbf x_1,\ldots,\mathbf x_N$，softmax 函数 (12.5) 都满足约束 (12.3) 和 (12.4)。

**12.3（★）** 考虑简单变换 (12.2) 中的输入向量 $\mathbf x_n$，其中加权系数 $a_{nm}$ 由式 (12.5) 定义。证明：如果所有输入向量相互正交，即当 $n\ne m$ 时 $\mathbf x_n^\mathsf T\mathbf x_m=0$，则输出向量直接等于相应的输入向量，即对 $n=1,\ldots,N$ 有 $\mathbf y_n=\mathbf x_n$。

**译注：** 原题按现有条件无法证明。正交不使 softmax 的非对角权重为零；正文式 (12.5) 后给出反例。

**12.4（★）** 考虑两个相互独立的 $D$ 维随机向量 $\mathbf a$ 与 $\mathbf b$，它们均取自均值为零、单位方差的高斯分布 $\mathcal N(\cdot\mid\mathbf0,\mathbf I)$。证明 $(\mathbf a^\mathsf T\mathbf b)^2$ 的期望为 $D$。

**12.5（★★★）** 证明：式 (12.19) 定义的多头注意力可重写为

$$
\mathbf Y=\sum_{h=1}^{H}\mathbf H_h\mathbf X\mathbf W^{(h)}, \tag{12.42}
$$

其中 $\mathbf H_h$ 由式 (12.15) 给出，且定义

$$
\mathbf W^{(h)}=\mathbf W_h^{(v)}\mathbf W_h^{(o)}. \tag{12.43}
$$

这里把矩阵 $\mathbf W^{(o)}$ 水平分成子矩阵 $\mathbf W_h^{(o)}$，每个维度为 $D_v\times D$，对应拼接后注意力矩阵的各个竖直片段。由于 $D_v$ 一般小于 $D$，例如常选 $D_v=D/H$（见图 12.7），所以这个组合矩阵秩亏。因此，如果用一个完全自由的矩阵替代 $\mathbf W_h^{(v)}\mathbf W_h^{(o)}$，就不再等价于正文给出的原始表述。

**译注：** 原书式 (12.42) 的 $\mathbf H_h$ 按式 (12.15) 是 $N\times D_v$ 的注意力输出，不能再左乘 $N\times D$ 的 $\mathbf X$。若令 $\mathbf A_h=\operatorname{Softmax}(\mathbf Q_h\mathbf K_h^{\mathsf T}/\sqrt{D_k})$ 为 $N\times N$ 的注意力权重矩阵，则维度一致的写法是 $\mathbf Y=\sum_h\mathbf A_h\mathbf X\mathbf W^{(h)}$；等价地，可写 $\mathbf Y=\sum_h\mathbf H_h\mathbf W_h^{(o)}$。原题公式和记号保留原书。

**12.6（★★）** 将自注意力函数 (12.14) 表示为全连接网络：写成一个矩阵，把由拼接后的词向量组成的完整输入序列映射到同维度的输出向量。注意，这样的矩阵将有 $O(N^2D^2)$ 个参数。证明自注意力网络对应其中一种具有参数共享的稀疏版本。画出该矩阵的结构草图，指出哪些参数块共享，哪些块的全部元素都为零。

**12.7（★）** 证明：如果省略输入向量的位置编码，式 (12.19) 定义的多头注意力层，其输出对输入序列的重新排序具有等变性。

**12.8（★★★）** 考虑从随机分布中抽取的两个 $D$ 维单位向量 $\mathbf a$ 与 $\mathbf b$，满足 $\|\mathbf a\|=1$ 和 $\|\mathbf b\|=1$。假设分布关于原点对称，即只依赖距原点的距离，不依赖方向。证明当 $D$ 较大时，两向量之间夹角余弦的绝对值接近零，因此这些随机向量在高维空间中近乎正交。为此，考虑正交归一基 $\{\mathbf u_i\}$，其中 $\mathbf u_i^\mathsf T\mathbf u_j=\delta_{ij}$，并在这组基下展开 $\mathbf a$ 与 $\mathbf b$。

<!-- pdf-page: 421 -->

**12.9（★★）** 考虑一种位置编码：将输入 token 向量 $\mathbf x$ 与位置编码向量 $\mathbf e$ 拼接。证明：当这一拼接后的向量乘以矩阵，进行一般线性变换时，结果可表示为线性变换后的输入向量与线性变换后的位置向量之和。

**12.10（★★）** 证明：式 (12.25) 定义的位置编码具有下述性质：对固定偏移量 $k$，位置 $n+k$ 的编码可表示为位置 $n$ 的编码的线性组合，而且其系数只依赖 $k$，不依赖 $n$。为此，使用以下三角恒等式：

$$
\cos(A+B)=\cos A\cos B-\sin A\sin B. \tag{12.44}
$$

$$
\sin(A+B)=\cos A\sin B+\sin A\cos B. \tag{12.45}
$$

证明：如果编码只使用正弦函数、不使用余弦函数，则这一性质不再成立。

**12.11（★）** 考虑词袋模型 (12.28)，其中每个分量分布 $p(\mathbf x_n)$ 都由一个在所有词间共享的一般概率表给出。证明：给定向量训练集时，极大似然解是一个概率表，其每个条目等于对应词在训练集中出现次数所占的比例。

**12.12（★）** 考虑式 (12.31) 给出的自回归语言模型，假设右侧各项 $p(\mathbf x_n\mid\mathbf x_1,\ldots,\mathbf x_{n-1})$ 都用一般概率表表示。证明这些表中的条目数量随 $n$ 呈指数增长。

**12.13（★）** 使用 $n$ 元组时，通常会同时训练 $n$ 元组和 $(n-1)$ 元组模型，再用概率乘法法则按下式计算条件概率：

$$
p(\mathbf x_n\mid\mathbf x_{n-L+1},\ldots,\mathbf x_{n-1})=\frac{p_L(\mathbf x_{n-L+1},\ldots,\mathbf x_n)}{p_{L-1}(\mathbf x_{n-L+1},\ldots,\mathbf x_{n-1})}. \tag{12.46}
$$

解释为什么这样比直接存储左侧更方便，并证明：为了获得正确的概率，计算 $p_{L-1}(\cdots)$ 时必须省略每个序列的最后一个 token。

**12.14（★★）** 为图 12.13 所示架构的已训练 RNN，写出推断过程的伪代码。

**12.15（★★）** 考虑由两个 token $y_1$ 和 $y_2$ 组成的序列，每个 token 都可取状态 $A$ 或 $B$。下表给出联合概率分布 $p(y_1,y_2)$：

<!-- pdf-page: 422 -->

|  | $y_1=A$ | $y_1=B$ |
|---|---:|---:|
| $y_2=A$ | 0.0 | 0.4 |
| $y_2=B$ | 0.1 | 0.25 |

可见，概率最高的序列是 $y_1=B,y_2=B$，概率为 $0.4$。利用概率的加法法则和乘法法则，写出边缘分布 $p(y_1)$ 与条件分布 $p(y_2\mid y_1)$ 的取值。证明：如果先最大化 $p(y_1)$ 得到 $y_1^*$，再最大化 $p(y_2\mid y_1^*)$，得到的序列不同于全局概率最高的序列。求出该序列的概率。

**译注：** 原书的四个表值相加为 $0.75$，不构成归一化的联合概率表；表中最大值 $0.4$ 对应 $(y_1=B,y_2=A)$，并非题干所称的 $(B,B)$。按现表先选边缘概率较高的 $y_1=B$，再选其条件概率较高的 $y_2=A$，也恰好落在表中全局最大格，无法得到题末要求的“不同”。在可核实的更正之前，本题不能按现表完成证明；表值与题干均保留原书。

**12.16（★）** BERT-Large 模型（Devlin 等，2018）的最大输入长度为 512 个 token，每个 token 的维度为 $D=1{,}024$，取自大小为 30,000 的词表。模型有 24 个 Transformer 层，每层有 16 个自注意力头，其中 $D_q=D_k=D_v=64$；各位置独立的 MLP 网络有两层，其中隐藏节点数为 4,096。证明这个 BERT 编码器 Transformer 语言模型的参数总数约为 3.4 亿。
