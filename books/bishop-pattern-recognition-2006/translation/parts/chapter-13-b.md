<!-- pdf-page: 649 -->

最后注意，前向—后向算法还有另一种表述（Jordan，2007）：后向过程的递推基于 $\gamma(\mathbf{z}_n)=\widehat{\alpha}(\mathbf{z}_n)\widehat{\beta}(\mathbf{z}_n)$，而不使用 $\widehat{\beta}(\mathbf{z}_n)$。这种 $\alpha$–$\gamma$ 递推要求先完成前向过程，使后向过程能够使用所有 $\widehat{\alpha}(\mathbf{z}_n)$；而 $\alpha$–$\beta$ 算法的前向过程和后向过程可以独立进行。这两种算法的计算成本相近，但在隐马尔可夫模型中，最常见的是 $\alpha$–$\beta$ 版本；在线性动力系统中，则更常使用类似 $\alpha$–$\gamma$ 形式的递推（第 13.3 节）。

### 13.2.5 Viterbi 算法

在隐马尔可夫模型的许多应用中，潜变量具有有意义的解释，因此，给定一个观测序列时，寻找最可能的隐藏状态序列通常很有用。例如，在语音识别中，可能希望根据一系列声学观测，找到最可能的音素序列。由于隐马尔可夫模型的图是一棵有向树，这个问题可以使用最大和算法精确求解。回顾第 8.4.5 节的讨论，寻找最可能的潜状态序列，与寻找每个位置上各自最可能的状态所构成的集合，并不是同一个问题。后一个问题可以先运行前向—后向（和积）算法，求出潜变量的边缘分布 $\gamma(\mathbf{z}_n)$，再分别最大化每个边缘分布来解决（Duda et al.，2001）。不过，这些状态组成的集合，一般并不对应于最可能的状态序列。事实上，这个状态集合甚至可能组成一个概率为零的序列：两个相邻状态单独来看各自最可能，但连接它们的转移矩阵元素却可能恰好为零。

在实践中，我们通常关心最可能的状态 *序列*。这个问题可以使用最大和算法高效求解，在隐马尔可夫模型中，该算法称为 *Viterbi 算法*（Viterbi，1967）。注意，最大和算法处理的是对数概率，因此不需要像前向—后向算法那样使用重新缩放的变量。图 13.16 展示了隐马尔可夫模型展开为格图后的一个片段。前面已经指出，穿过格图的可能路径数，随链的长度指数增长。Viterbi 算法能够高效搜索这个路径空间，以仅随链长线性增长的计算成本，找到最可能的路径。

与和积算法一样，首先将隐马尔可夫模型表示成因子图，如图 13.15 所示。同样，将变量节点 $\mathbf{z}_N$ 作为根，从叶节点开始向根传递消息。利用结果（8.93）和（8.94）可知，最大和算法中传递的消息为

$$
\mu_{\mathbf{z}_n\to f_{n+1}}(\mathbf{z}_n)=\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)
\tag{13.66}
$$

$$
\mu_{f_{n+1}\to\mathbf{z}_{n+1}}(\mathbf{z}_{n+1})=\max_{\mathbf{z}_n}\left\{\ln f_{n+1}(\mathbf{z}_n,\mathbf{z}_{n+1})+\mu_{\mathbf{z}_n\to f_{n+1}}(\mathbf{z}_n)\right\}.
\tag{13.67}
$$

<!-- pdf-page: 650 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-16.png" alt="HMM 格图中的两条候选路径，跨越四个时刻和三个彩色状态"><figcaption>图 13.16：HMM 格图的一个片段，显示两条可能的路径。Viterbi 算法从指数数量的可能路径中，高效地确定最可能的路径。对于任意给定路径，相应的概率由转移矩阵元素 $A_{jk}$ 的乘积，再乘以路径上各节点对应的发射密度 $p(\mathbf{x}_n\mid k)$ 给出；转移矩阵元素对应于路径各段的概率 $p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)$。</figcaption><p class="figure-translation">$k=1,2,3$：三个可能状态，分别用红、绿、蓝方框表示；$n-2,n-1,n,n+1$：相继时刻；上方箭头表示时间向前的方向。两条黑线表示两条候选状态路径。</p></figure>

从这两个方程中消去 $\mu_{\mathbf{z}_n\to f_{n+1}}(\mathbf{z}_n)$，并利用（13.46），得到 $f\to\mathbf{z}$ 消息的递推式

$$
\omega(\mathbf{z}_{n+1})=\ln p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})+\max_{\mathbf{z}_n}\left\{\ln p(\mathbf{x}_{+1}\mid\mathbf{z}_n)+\omega(\mathbf{z}_n)\right\}
\tag{13.68}
$$

其中引入了记号 $\omega(\mathbf{z}_n)\equiv\mu_{f_n\to\mathbf{z}_n}(\mathbf{z}_n)$。

由（8.95）和（8.96），这些消息使用下式初始化：

$$
\omega(\mathbf{z}_1)=\ln p(\mathbf{z}_1)+\ln p(\mathbf{x}_1\mid\mathbf{z}_1).
\tag{13.69}
$$

这里使用了（13.45）。注意，为保持记号简洁，省略了对模型参数 $\boldsymbol{\theta}$ 的依赖；寻找最可能序列时，这些参数保持固定。

Viterbi 算法也可以直接从联合分布的定义（13.6）推导出来：先取对数，再交换最大化与求和运算的顺序。很容易看出，$\omega(\mathbf{z}_n)$ 具有如下概率解释（习题 13.16）：

$$
\omega(\mathbf{z}_n)=\max_{\mathbf{z}_1,\ldots,\mathbf{z}_{n-1}}p(\mathbf{x}_1,\ldots,\mathbf{x}_n,\mathbf{z}_1,\ldots,\mathbf{z}_n).
\tag{13.70}
$$

一旦完成最后对 $\mathbf{z}_N$ 的最大化，就会得到最可能路径对应的联合分布 $p(\mathbf{X},\mathbf{Z})$ 的值。我们还希望找出这条路径对应的潜变量值序列。为此，只需使用第 8.4.5 节讨论的回溯过程。具体而言，对于 $\mathbf{z}_{n+1}$ 的每一个可能值，都必须对 $\mathbf{z}_n$ 进行最大化，总共有 $K$ 个这样的值。假设记录下 $\mathbf{z}_{n+1}$ 的每个可能值所对应的、使目标达到最大的 $\mathbf{z}_n$ 值。将这个函数记为 $\psi(k_n)$，其中 $k\in\{1,\ldots,K\}$。当消息已传到链的末端，并找到了 $\mathbf{z}_N$ 最可能的状态后，就可以递归地应用这个函数，沿链回溯：

$$
k_n^{\max}=\psi(k_{n+1}^{\max}).
\tag{13.71}
$$

<!-- pdf-page: 651 -->

可以直观地理解 Viterbi 算法。最直接的办法，是明确考虑穿过格图的全部路径——它们的数量呈指数增长——计算每条路径的概率，再选择概率最高的那一条。不过，可以用如下方法大幅减少计算成本。假设沿每条路径在格图中向前移动时，通过累加转移概率与发射概率的乘积，计算这条路径的概率。考虑某个时刻 $n$ 和该时刻的某个状态 $k$。许多可能的路径会汇聚到格图中的相应节点，但只需保留其中到目前为止概率最高的那一条。由于时刻 $n$ 有 $K$ 个状态，需要跟踪 $K$ 条这样的路径。在时刻 $n+1$，需要考虑 $K^2$ 条可能路径，即从当前 $K$ 个状态中的每个状态出发，都有 $K$ 条可能路径；但仍然只需保留 $K$ 条，它们分别是到达时刻 $n+1$ 各个状态的最佳路径。到达最后一个时刻 $N$ 时，就能确定哪个状态对应于整体上最可能的路径。由于进入这个状态的路径是唯一的，可以沿路径回溯到时刻 $N-1$，查看那时所处的状态，如此沿格图一直回溯到 $n=1$ 时的状态。

### 13.2.6 隐马尔可夫模型的扩展

为了满足特定应用的需求，人们对基本隐马尔可夫模型及其基于最大似然的标准训练算法进行了许多扩展。这里讨论其中几个较为重要的例子。

从图 13.11 的数字示例可以看出，隐马尔可夫模型作为数据的生成式模型，表现可能相当差，因为许多合成数字看起来并不能很好地代表训练数据。如果目标是序列分类，那么使用判别式方法而不是最大似然方法来确定隐马尔可夫模型的参数，可能带来显著收益。假设训练集包含 $R$ 个观测序列 $\mathbf{X}_r$，其中 $r=1,\ldots,R$，每个序列都有类别标记 $m$，其中 $m=1,\ldots,M$。每个类别都有一个单独的隐马尔可夫模型，具有自己的参数 $\boldsymbol{\theta}_m$。将确定参数值的问题视为一个标准分类问题，在其中优化交叉熵

$$
\sum_{r=1}^R\ln p(m_r\mid\mathbf{X}_r).
\tag{13.72}
$$

利用贝叶斯定理，可以用隐马尔可夫模型对应的序列概率来表达它：

$$
\sum_{r=1}^R\ln\left\{\frac{p(\mathbf{X}_r\mid\boldsymbol{\theta}_r)p(m_r)}{\sum_{l=1}^M p(\mathbf{X}_r\mid\boldsymbol{\theta}_l)p(l_r)}\right\}
\tag{13.73}
$$

其中，$p(m)$ 是类别 $m$ 的先验概率。优化这个代价函数，比最大似然优化更复杂（Kapadia，1998），尤其是

<!-- pdf-page: 652 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-17.png" alt="自回归隐马尔可夫模型局部图，当前观测依赖隐藏状态和前两个观测"><figcaption>图 13.17：自回归隐马尔可夫模型的一个片段，其中观测 $\mathbf{x}_n$ 的分布，既依赖于隐藏状态 $\mathbf{z}_n$，也依赖于之前观测的一个子集。在这个例子中，$\mathbf{x}_n$ 的分布依赖于前两个观测 $\mathbf{x}_{n-1}$ 和 $\mathbf{x}_{n-2}$。</figcaption><p class="figure-translation">上层 $\mathbf{z}_{n-1},\mathbf{z}_n,\mathbf{z}_{n+1}$：隐藏状态；下层 $\mathbf{x}_{n-1},\mathbf{x}_n,\mathbf{x}_{n+1}$：观测变量。填色表示已观测节点，下层的边包含相隔一个和两个时刻的依赖。</p></figure>

<!-- join-previous-paragraph-across-figures -->
为了计算（13.73）的分母，必须在每个模型下评估每一条训练序列。隐马尔可夫模型结合判别训练方法，被广泛应用于语音识别（Kapadia，1998）。

隐马尔可夫模型的一个显著弱点，在于它表示系统停留于给定状态的时长分布的方式。为了看清这个问题，注意：从给定隐马尔可夫模型采样的序列，恰好在状态 $k$ 停留 $T$ 步，然后转移到另一个状态的概率为

$$
p(T)=(A_{kk})^T(1-A_{kk})\propto\exp(-T\ln A_{kk})
\tag{13.74}
$$

因此是 $T$ 的指数衰减函数。对于许多应用，这种状态持续时间模型非常不符合实际。可以通过直接建模状态持续时间来解决这一问题：将所有对角系数 $A_{kk}$ 设为零，并为每个状态 $k$ 明确指定可能持续时间的概率分布 $p(T\mid k)$。从生成过程的角度看，当系统进入状态 $k$ 时，从 $p(T\mid k)$ 中抽取一个值 $T$，表示系统将在状态 $k$ 停留的时间步数。随后，模型发射观测变量 $\mathbf{x}_t$ 的 $T$ 个值；通常假设它们相互独立，因此相应的发射密度就是 $\prod_{t=1}^T p(\mathbf{x}_t\mid k)$。这种方法需要对 EM 优化过程作一些直接的修改（Rabiner，1989）。

标准 HMM 的另一个局限，是难以捕捉观测变量之间的长程相关性（即相隔许多时间步的变量之间的相关性），因为这些相关性必须通过隐藏状态的一阶马尔可夫链来传递。原则上，可以在图 13.5 的图模型中加入额外的边，纳入较长程的影响。一种方法是将 HMM 推广为 *自回归隐马尔可夫模型*（autoregressive hidden Markov model）（Ephraim et al.，1989），图 13.17 展示了一个例子。对于离散观测，这相当于扩大发射分布的条件概率表。对于高斯发射密度，可以使用线性高斯框架：给定先前观测值和 $\mathbf{z}_n$ 的值时，$\mathbf{x}_n$ 的条件分布是高斯分布，其均值是条件变量值的线性组合。显然，必须限制图中增加的边数，以免自由参数过多。在图 13.17 的例子中，每个观测都依赖于

<!-- pdf-page: 653 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-18.png" alt="输入输出隐马尔可夫模型，输入观测层同时影响隐藏状态层和输出观测层"><figcaption>图 13.18：输入输出隐马尔可夫模型的示例。在这个例子中，发射概率和转移概率都依赖于观测序列 $\mathbf{u}_1,\ldots,\mathbf{u}_N$ 的值。</figcaption><p class="figure-translation">上层 $\mathbf{u}_{n-1},\mathbf{u}_n,\mathbf{u}_{n+1}$：已观测的输入；中层 $\mathbf{z}_{n-1},\mathbf{z}_n,\mathbf{z}_{n+1}$：隐藏状态；下层 $\mathbf{x}_{n-1},\mathbf{x}_n,\mathbf{x}_{n+1}$：已观测的输出。填色表示已观测节点。</p></figure>

<!-- join-previous-paragraph-across-figures -->
前两个观测变量以及隐藏状态。虽然这个图看起来比较杂乱，但仍然可以借助 d 分离，发现它实际上具有简单的概率结构。具体而言，如果假设以 $\mathbf{z}_n$ 为条件，就会看到，与标准 HMM 一样，$\mathbf{z}_{n-1}$ 和 $\mathbf{z}_{n+1}$ 的值相互独立，对应于条件独立性质（13.5）。这一点很容易验证：从节点 $\mathbf{z}_{n-1}$ 到节点 $\mathbf{z}_{n+1}$ 的每条路径，都经过至少一个相对于该路径首尾相接的已观测节点。因此，在 EM 算法的 E 步中，仍然可以使用前向—后向递推，以随链长线性增长的计算时间，确定潜变量的后验分布。类似地，M 步只需对标准 M 步方程作少量修改。对于高斯发射密度，这涉及使用第 3 章讨论的标准线性回归方程估计参数。

我们已经看到，从图模型的角度看，自回归 HMM 是标准 HMM 的自然扩展。事实上，概率图建模的视角可以引出大量基于 HMM 的不同图结构。另一个例子是 *输入输出隐马尔可夫模型*（input-output hidden Markov model）（Bengio and Frasconi，1995）：除了输出变量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，还有一系列观测变量 $\mathbf{u}_1,\ldots,\mathbf{u}_N$，它们的值可以影响潜变量的分布、输出变量的分布，或同时影响两者。图 13.18 给出了一个例子。这将 HMM 框架扩展到了序列数据的监督学习领域。利用 d 分离判据，同样容易证明潜变量链的马尔可夫性质（13.5）仍然成立。为验证这一点，只需注意，从节点 $\mathbf{z}_{n-1}$ 到节点 $\mathbf{z}_{n+1}$ 只有一条路径，并且相对于已观测节点 $\mathbf{z}_n$，这条路径是首尾相接的。这个条件独立性质再次使我们能够构建计算高效的学习算法。具体来说，可以通过最大化似然函数 $L(\boldsymbol{\theta})=p(\mathbf{X}\mid\mathbf{U},\boldsymbol{\theta})$ 来确定模型参数 $\boldsymbol{\theta}$，其中 $\mathbf{U}$ 是各行由 $\mathbf{u}_n^{\mathrm{T}}$ 给出的矩阵。由于条件独立性质（13.5），这个似然函数可以用 EM 算法高效最大化，其中 E 步包含前向和后向递推（习题 13.18）。

另一种值得介绍的 HMM 变体是 *因子化隐马尔可夫模型*（factorial hidden Markov model）（Ghahramani and Jordan，1997），它包含多条相互独立的潜变量

<!-- pdf-page: 654 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-19.png" alt="由两条隐藏马尔可夫链共同生成同一观测序列的因子化 HMM"><figcaption>图 13.19：由两条潜变量马尔可夫链组成的因子化隐马尔可夫模型。对于连续观测变量 $\mathbf{x}$，一种可能的发射模型是线性高斯密度，其中高斯分布的均值是相应潜变量状态的线性组合。</figcaption><p class="figure-translation">$\mathbf{z}_{n-1}^{(1)},\mathbf{z}_n^{(1)},\mathbf{z}_{n+1}^{(1)}$ 与 $\mathbf{z}_{n-1}^{(2)},\mathbf{z}_n^{(2)},\mathbf{z}_{n+1}^{(2)}$：两条潜变量链；$\mathbf{x}_{n-1},\mathbf{x}_n,\mathbf{x}_{n+1}$：观测序列。每个观测节点接收同一时刻两条潜链的连接。</p></figure>

<!-- join-previous-paragraph-across-figures -->
马尔可夫链，某一时刻观测变量的分布，以同一时刻所有相应潜变量的状态为条件。图 13.19 显示了相应的图模型。考虑因子化 HMM 的动机可以从下面看出：例如，要在某个时刻表示 10 比特的信息，标准 HMM 需要 $K=2^{10}=1024$ 个潜状态，而因子化 HMM 可以使用 10 条二元潜变量链。不过，因子化 HMM 的主要缺点在于训练更复杂。模型的 M 步很直接，但观测到 $\mathbf{x}$ 变量后，会在各条潜链之间引入依赖，使 E 步变得困难。注意图 13.19 中的变量 $\mathbf{z}_n^{(1)}$ 与 $\mathbf{z}_n^{(2)}$：它们由一条在节点 $\mathbf{x}_n$ 处首首相接的路径连接，因此并未被 d 分离。这个模型的精确 E 步，并不等价于沿 $M$ 条马尔可夫链各自独立运行前向和后向递推。因子化 HMM 模型中的单条马尔可夫链不满足关键条件独立性质（13.5），这证实了上述结论；图 13.20 用 d 分离说明了这一点。现在假设有 $M$ 条隐藏节点链，为简单起见，假设所有潜变量的状态数都为 $K$。一种方法是注意到，在一个给定时刻，潜变量共有 $K^M$ 种组合，

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-20.png" alt="因子化 HMM 中未被阻断的绿色路径，通过另一条潜链连接两个时刻的状态"><figcaption>图 13.20：绿色高亮显示了一条路径，它在已观测节点 $\mathbf{x}_{n-1}$ 和 $\mathbf{x}_{n+1}$ 处首首相接，在未观测节点 $\mathbf{z}_{n-1}^{(2)}$、$\mathbf{z}_n^{(2)}$ 和 $\mathbf{z}_{n+1}^{(2)}$ 处首尾相接。因此，这条路径没有被阻断，条件独立性质（13.5）对因子化 HMM 模型中的单条潜链不成立。因此，这个模型没有高效的精确 E 步。</figcaption><p class="figure-translation">绿色曲线：未被阻断的路径；$\mathbf{z}^{(1)}$、$\mathbf{z}^{(2)}$：两条潜变量链；$\mathbf{x}$：观测变量。填色表示已观测或作为条件的节点，包括中间的 $\mathbf{z}_n^{(1)}$。</p></figure>

<!-- pdf-page: 655 -->
<!-- join-previous-paragraph-across-figures -->
因此可以将模型变换为一个等价的标准 HMM，它只有一条潜变量链，每个潜变量有 $K^M$ 个潜状态。然后，就可以在 E 步中运行标准的前向—后向递推。这需要 $O(NK^{2M})$ 的计算复杂度，随潜链数量 $M$ 指数增长，因此只有在 $M$ 较小时才可行。一种解决办法是使用第 11 章讨论的采样方法。作为一种简洁的确定性替代方法，Ghahramani and Jordan（1997）利用变分推断技术，得到了可计算的近似推断算法（第 10.1 节）。可以使用一个关于所有潜变量完全因子化的简单变分后验分布，也可以使用更有表达力的方法：用相互独立的马尔可夫链描述变分分布，这些链对应于原模型中的潜变量链。在后一种情况下，变分推断算法沿每条链独立运行前向和后向递推，既计算高效，又能捕捉同一条链中各变量之间的相关性。

显然，可以根据特定应用的需求构造许多不同的概率结构。图模型为提出、描述和分析这类结构提供了通用方法；对于无法精确求解的模型，变分方法则为推断提供了强大的框架。

## 13.3 线性动力系统

为了引出线性动力系统的概念，考虑下面这个在实际中经常出现的简单问题。假设希望测量一个未知量 $\mathbf{z}$，使用的传感器带有噪声，它返回观测 $\mathbf{x}$，等于 $\mathbf{z}$ 的值加上零均值高斯噪声。只有一次测量时，对 $\mathbf{z}$ 的最佳猜测是 $\mathbf{z}=\mathbf{x}$。不过，多次测量并取平均，可以改进对 $\mathbf{z}$ 的估计，因为随机噪声项会趋向于相互抵消。现在将情况变得更复杂一些：假设要测量的量 $\mathbf{z}$ 随时间变化。可以定期测量 $\mathbf{x}$，到某个时刻已经得到了 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，并希望找到对应的值 $\mathbf{z}_1,\ldots,\mathbf{x}_N$。如果简单地对测量取平均，随机噪声引起的误差会减小，但遗憾的是，我们只会得到一个平均估计值；因为也对 $\mathbf{z}$ 的变化进行了平均，所以又引入了新的误差来源。

直观地说，可以设想如下改进。为了估计 $\mathbf{z}_N$ 的值，只取最近几次测量，例如 $\mathbf{x}_{N-L},\ldots,\mathbf{x}_N$，并仅对它们取平均。如果 $\mathbf{z}$ 变化缓慢，而传感器中的随机噪声较强，选择一个较长的观测窗口来平均是合理的。反过来，如果信号变化很快而噪声较小，直接使用 $\mathbf{x}_N$ 估计 $\mathbf{z}_N$ 可能更好。也许采用加权平均还能进一步改进，其中越近的测量

<!-- pdf-page: 656 -->
<!-- join-previous-paragraph -->
比更早的测量贡献更大。

虽然这类直观论证似乎合理，但它并未告诉我们该如何构成加权平均，而任何人工设计的加权方式都很难是最优的。幸运的是，我们可以定义一个概率模型来描述随时间的演变过程和测量过程，再应用前面各章中建立的推断与学习方法，从而更系统地处理这类问题。这里将重点讨论一种广泛使用的模型，称为*线性动力系统*（linear dynamical system）。

正如前面所见，HMM 对应于图 13.5 所示的状态空间模型，其中潜变量是离散的，而发射概率分布可以是任意形式。当然，这个图还描述了范围广得多的一类概率分布，它们都按照（13.6）进行因子分解。现在考虑将潜变量推广到其他分布。具体来说，我们考虑连续潜变量，此时和积算法中的求和变成了积分。不过，推断算法的一般形式与隐马尔可夫模型相同。有趣的是，从历史上看，隐马尔可夫模型和线性动力系统是独立发展起来的。然而，一旦将二者都表示为图模型，它们之间的深刻联系就会立即显现出来。

一个关键要求是，我们仍然要有一个高效的推断算法，其计算量随链的长度线性增长。例如，这就要求：取表示给定观测 $\mathbf{x}_1,\ldots,\mathbf{x}_n$ 时 $\mathbf{z}_n$ 的后验概率的量 $\widehat{\alpha}(\mathbf{z}_{n-1})$，将它乘以转移概率 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 和发射概率 $p(\mathbf{x}_n\mid\mathbf{z}_n)$，再对 $\mathbf{z}_{n-1}$ 边缘化后，所得到的 $\mathbf{z}_n$ 上的分布，应当与 $\widehat{\alpha}(\mathbf{z}_{n-1})$ 具有相同的函数形式。也就是说，分布不能在每一步都变得更复杂，只能改变其参数值。不出所料，具有这种对乘法封闭的性质的分布，只有属于指数族的那些分布。

这里考虑从实际应用角度看最重要的例子，即高斯分布。具体来说，我们考虑线性高斯状态空间模型：潜变量 $\{\mathbf{z}_n\}$ 和观测变量 $\{\mathbf{x}_n\}$ 都服从多元高斯分布，其均值是图中父节点状态的线性函数。前面已经看到，由线性高斯单元构成的有向图，等价于所有变量上的一个联合高斯分布。此外，$\widehat{\alpha}(\mathbf{z}_n)$ 这样的边缘分布也为高斯分布，因此消息的函数形式得以保持，从而得到高效的推断算法。相反，假设发射密度 $p(\mathbf{x}_n\mid\mathbf{z}_n)$ 是由 $K$ 个高斯分布组成的混合，其中每个高斯分布的均值都是 $\mathbf{z}_n$ 的线性函数。那么，即使 $\widehat{\alpha}(\mathbf{z}_1)$ 是高斯分布，$\widehat{\alpha}(\mathbf{z}_2)$ 也将是 $K$ 个高斯分布的混合，$\widehat{\alpha}(\mathbf{z}_3)$ 将是 $K^2$ 个高斯分布的混合，依此类推，精确推断就不再具有实际价值。

我们已经看到，隐马尔可夫模型可以看作第 9 章混合模型的扩展，用来容纳数据中的序列相关性。同样，也可以将线性动力系统看作第 12 章连续潜变量模型的推广，例如概率 PCA 和因子分析。每一对节点 $\{\mathbf{z}_n,\mathbf{x}_n\}$ 都表示针对那个特定观测的一个线性高斯潜变量

<!-- pdf-page: 657 -->
<!-- join-previous-paragraph -->
模型。然而，潜变量 $\{\mathbf{z}_n\}$ 不再被视为相互独立，而是构成一条马尔可夫链。

由于该模型由树结构的有向图表示，因此可以使用和积算法高效地求解推断问题。与隐马尔可夫模型的 $\alpha$ 消息类似的前向递推，称为 *Kalman 滤波*方程（Kalman，1960；Zarchan and Musoff，2005）；与 $\beta$ 消息类似的后向递推，称为 *Kalman 平滑*方程，或 *Rauch-Tung-Striebel*（RTS）方程（Rauch et al.，1965）。Kalman 滤波广泛用于许多实时跟踪应用。

由于线性动力系统是线性高斯模型，所有变量上的联合分布，以及所有边缘分布和条件分布，都是高斯分布。因此，由各个潜变量各自最可能的值组成的序列，与最可能的潜状态序列相同（习题 13.19）。所以，对于线性动力系统，无须考虑 Viterbi 算法的对应形式。

由于模型具有线性高斯条件分布，转移分布与发射分布可以写成一般形式

$$
p(\mathbf{z}_n\mid\mathbf{z}_{n-1})=\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\mathbf{z}_{n-1},\boldsymbol{\Gamma})
\tag{13.75}
$$

$$
p(\mathbf{x}_n\mid\mathbf{z}_n)=\mathcal{N}(\mathbf{x}_n\mid\mathbf{C}\mathbf{z}_n,\boldsymbol{\Sigma}).
\tag{13.76}
$$

初始潜变量也服从高斯分布，写为

$$
p(\mathbf{z}_1)=\mathcal{N}(\mathbf{z}_1\mid\boldsymbol{\mu}_0,\mathbf{V}_0).
\tag{13.77}
$$

注意，为简化记号，我们省略了高斯分布均值中的加性常数项。实际上，如果需要，将它们纳入模型并不困难（习题 13.24）。传统上，这些分布更常用带噪声的线性方程表示为等价形式，即

$$
\mathbf{z}_n=\mathbf{A}\mathbf{z}_{n-1}+\mathbf{w}_n
\tag{13.78}
$$

$$
\mathbf{x}_n=\mathbf{C}\mathbf{z}_n+\mathbf{v}_n
\tag{13.79}
$$

$$
\mathbf{z}_1=\boldsymbol{\mu}_0+\mathbf{u}
\tag{13.80}
$$

其中，噪声项的分布为

$$
\mathbf{w}\sim\mathcal{N}(\mathbf{w}\mid\mathbf{0},\boldsymbol{\Gamma})
\tag{13.81}
$$

$$
\mathbf{v}\sim\mathcal{N}(\mathbf{v}\mid\mathbf{0},\boldsymbol{\Sigma})
\tag{13.82}
$$

$$
\mathbf{u}\sim\mathcal{N}(\mathbf{u}\mid\mathbf{0},\mathbf{V}_0).
\tag{13.83}
$$

模型参数记为 $\boldsymbol{\theta}=\{\mathbf{A},\boldsymbol{\Gamma},\mathbf{C},\boldsymbol{\Sigma},\boldsymbol{\mu}_0,\mathbf{V}_0\}$，可以通过 EM 算法按最大似然确定。在 E 步中，需要解决一个推断问题，即确定潜变量的局部后验边缘分布；这可以用和积算法高效求解，下一节将对此展开讨论。

<!-- pdf-page: 658 -->

### 13.3.1 LDS 中的推断

现在转向求解给定观测序列时潜变量的边缘分布。对于给定的参数设置，我们还希望以观测数据 $\mathbf{x}_1,\ldots,\mathbf{x}_{n-1}$ 为条件，预测下一个潜状态 $\mathbf{z}_n$ 和下一个观测 $\mathbf{x}_n$，以用于实时应用。这些推断问题可以用和积算法高效求解；在线性动力系统中，该算法导出 Kalman 滤波与 Kalman 平滑方程。

需要强调的是，由于线性动力系统是线性高斯模型，所有潜变量和观测变量上的联合分布就是一个高斯分布，所以原则上可以使用前面各章推导的多元高斯分布的边缘分布与条件分布的标准结果，来解决推断问题。和积算法的作用，是提供一种执行这些计算的更高效的方法。

线性动力系统与隐马尔可夫模型具有完全相同的因子分解形式，即（13.6），也由图 13.14 和图 13.15 中的因子图描述。因此，推断算法的形式完全相同，只需将对潜变量的求和替换为积分。首先考虑前向方程，将 $\mathbf{z}_N$ 作为根节点，并从叶节点 $h(\mathbf{z}_1)$ 向根节点传递消息。由（13.77）可知，初始消息是高斯分布；由于每个因子都是高斯分布，后续所有消息也都是高斯分布。按照惯例，我们传递的消息是对应于 $p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)$ 的归一化边缘分布，记为

$$
\widehat{\alpha}(\mathbf{z}_n)=\mathcal{N}(\mathbf{z}_n\mid\boldsymbol{\mu}_n,\mathbf{V}_n).
\tag{13.84}
$$

这与隐马尔可夫模型的离散情形中，传递（13.59）给出的缩放变量 $\widehat{\alpha}(\mathbf{z}_n)$ 完全类似，因此现在的递推方程为

$$
c_n\widehat{\alpha}(\mathbf{z}_n)=p(\mathbf{x}_n\mid\mathbf{z}_n)\int\widehat{\alpha}(\mathbf{z}_{n-1})p(\mathbf{z}_n\mid\mathbf{z}_{n-1})\,\mathrm{d}\mathbf{z}_{n-1}.
\tag{13.85}
$$

分别用（13.75）和（13.76）代入条件分布 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 和 $p(\mathbf{x}_n\mid\mathbf{z}_n)$，并使用（13.84），可见（13.85）变为

$$
\begin{aligned}
c_n\mathcal{N}(\mathbf{z}_n\mid\boldsymbol{\mu}_n,\mathbf{V}_n)
&=\mathcal{N}(\mathbf{x}_n\mid\mathbf{C}\mathbf{z}_n,\boldsymbol{\Sigma})\\
&\quad\int\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\mathbf{z}_{n-1},\boldsymbol{\Gamma})\mathcal{N}(\mathbf{z}_{n-1}\mid\boldsymbol{\mu}_{n-1},\mathbf{V}_{n-1})\,\mathrm{d}\mathbf{z}_{n-1}.
\end{aligned}
\tag{13.86}
$$

这里假设 $\boldsymbol{\mu}_{n-1}$ 和 $\mathbf{V}_{n-1}$ 已知，希望通过计算（13.86）中的积分来确定 $\boldsymbol{\mu}_n$ 和 $\mathbf{V}_n$。利用结果（2.115）很容易计算该积分，得到

$$
\begin{aligned}
&\int\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\mathbf{z}_{n-1},\boldsymbol{\Gamma})\mathcal{N}(\mathbf{z}_{n-1}\mid\boldsymbol{\mu}_{n-1},\mathbf{V}_{n-1})\,\mathrm{d}\mathbf{z}_{n-1}\\
&\qquad=\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\boldsymbol{\mu}_{n-1},\mathbf{P}_{n-1})
\end{aligned}
\tag{13.87}
$$

<!-- pdf-page: 659 -->

其中定义

$$
\mathbf{P}_{n-1}=\mathbf{A}\mathbf{V}_{n-1}\mathbf{A}^{\mathrm{T}}+\boldsymbol{\Gamma}.
\tag{13.88}
$$

现在可以利用（2.115）和（2.116），将这一结果与（13.86）右侧的第一个因子结合，得到

$$
\boldsymbol{\mu}_n=\mathbf{A}\boldsymbol{\mu}_{n-1}+\mathbf{K}_n(\mathbf{x}_n-\mathbf{C}\mathbf{A}\boldsymbol{\mu}_{n-1})
\tag{13.89}
$$

$$
\mathbf{V}_n=(\mathbf{I}-\mathbf{K}_n\mathbf{C})\mathbf{P}_{n-1}
\tag{13.90}
$$

$$
c_n=\mathcal{N}(\mathbf{x}_n\mid\mathbf{C}\mathbf{A}\boldsymbol{\mu}_{n-1},\mathbf{C}\mathbf{P}_{n-1}\mathbf{C}^{\mathrm{T}}+\boldsymbol{\Sigma}).
\tag{13.91}
$$

这里使用了矩阵求逆恒等式（C.5）和（C.7），还定义了 *Kalman 增益矩阵*

$$
\mathbf{K}_n=\mathbf{P}_{n-1}\mathbf{C}^{\mathrm{T}}\left(\mathbf{C}\mathbf{P}_{n-1}\mathbf{C}^{\mathrm{T}}+\boldsymbol{\Sigma}\right)^{-1}.
\tag{13.92}
$$

因此，给定 $\boldsymbol{\mu}_{n-1}$ 和 $\mathbf{V}_{n-1}$ 的值以及新的观测 $\mathbf{x}_n$，就可以计算 $\mathbf{z}_n$ 的高斯边缘分布，其均值为 $\boldsymbol{\mu}_n$，协方差为 $\mathbf{V}_n$，同时还可算出归一化系数 $c_n$。

这些递推方程的初始条件由下式得到

$$
c_1\widehat{\alpha}(\mathbf{z}_1)=p(\mathbf{z}_1)p(\mathbf{x}_1\mid\mathbf{z}_1).
\tag{13.93}
$$

由于 $p(\mathbf{z}_1)$ 由（13.77）给出，而 $p(\mathbf{x}_1\mid\mathbf{z}_1)$ 由（13.76）给出，因此可以再次用（2.115）计算 $c_1$，用（2.116）计算 $\boldsymbol{\mu}_1$ 和 $\mathbf{V}_1$，得到

$$
\boldsymbol{\mu}_1=\boldsymbol{\mu}_0+\mathbf{K}_1(\mathbf{x}_1-\mathbf{C}\boldsymbol{\mu}_0)
\tag{13.94}
$$

$$
\mathbf{V}_1=(\mathbf{I}-\mathbf{K}_1\mathbf{C})\mathbf{V}_0
\tag{13.95}
$$

$$
c_1=\mathcal{N}(\mathbf{x}_1\mid\mathbf{C}\boldsymbol{\mu}_0,\mathbf{C}\mathbf{V}_0\mathbf{C}^{\mathrm{T}}+\boldsymbol{\Sigma})
\tag{13.96}
$$

其中

$$
\mathbf{K}_1=\mathbf{V}_0\mathbf{C}^{\mathrm{T}}\left(\mathbf{C}\mathbf{V}_0\mathbf{C}^{\mathrm{T}}+\boldsymbol{\Sigma}\right)^{-1}.
\tag{13.97}
$$

同样，线性动力系统的似然函数由（13.63）给出，其中的因子 $c_n$ 可使用 Kalman 滤波方程求得。

从 $\mathbf{z}_{n-1}$ 上的后验边缘分布推进到 $\mathbf{z}_n$ 上的后验边缘分布，其各个步骤可以解释如下。在（13.89）中，可以将 $\mathbf{A}\boldsymbol{\mu}_{n-1}$ 看作对 $\mathbf{z}_n$ 均值的预测：只需取 $\mathbf{z}_{n-1}$ 的均值，并用转移概率矩阵 $\mathbf{A}$ 将其向前推进一步。将发射概率矩阵 $\mathbf{C}$ 作用于预测的隐状态均值，这个预测均值就会给出对 $\mathbf{x}_n$ 的预测观测 $\mathbf{C}\mathbf{A}\mathbf{z}_{n-1}$。潜变量分布均值的更新方程（13.89），可以看作先取预测均值 $\mathbf{A}\boldsymbol{\mu}_{n-1}$，再加上一个修正项；该修正项与预测观测和实际观测之间的误差 $\mathbf{x}_n-\mathbf{C}\mathbf{A}\mathbf{z}_{n-1}$ 成正比。这个修正项的系数由 Kalman 增益矩阵给出。因此，可以将 Kalman 滤波看作不断作出预测，再根据新观测修正这些预测的过程。图 13.21 对此给出了图示。

<!-- pdf-page: 660 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-21.png" alt="线性动力系统中扩散、观测似然和后验更新的三幅高斯曲线图"><figcaption>图 13.21：线性动力系统可以看作一系列步骤：扩散使状态变量的不确定性增加，而新数据的到来抵消了这种增加。左图中的蓝色曲线表示分布 $p(\mathbf{z}_{n-1}\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})$，它包含截至第 $n-1$ 步的所有数据。转移概率 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1})$ 的非零方差引起扩散，得到分布 $p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})$，如中图的红色曲线所示。注意，与蓝色曲线相比，该曲线更宽且发生了位移；中图用蓝色虚线给出原曲线以供比较。下一个数据观测 $\mathbf{x}_n$ 通过发射密度 $p(\mathbf{x}_n\mid\mathbf{z}_n)$ 起作用；右图用绿色将其画成 $\mathbf{z}_n$ 的函数。注意，这不是关于 $\mathbf{z}_n$ 的密度，因此没有归一化为 1。纳入这个新数据点后，得到修正后的状态密度分布 $p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_n)$，如蓝色曲线所示。可以看到，与 $p(\mathbf{z}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})$ 相比，观测数据使分布发生位移并变窄；右图用虚线画出后一个分布以供比较。</figcaption><p class="figure-translation">$z_{n-1}$、$z_n$：相邻时刻的潜状态；蓝色：状态分布；红色：经过状态转移得到的预测分布；绿色：观测的发射密度作为潜状态的函数。</p></figure>

如果测量噪声相对于潜变量的演变速率很小，那么会发现，$\mathbf{z}_n$ 的后验分布只依赖于当前测量 $\mathbf{x}_n$（习题 13.27），这与本节开头简单例子给出的直觉一致。同样，如果潜变量相对于观测噪声水平变化缓慢，那么 $\mathbf{z}_n$ 的后验均值就是对截至该时刻获得的全部测量取平均（习题 13.28）。

Kalman 滤波最重要的应用之一是跟踪。图 13.22 用一个物体在二维空间中运动的简单例子说明了这一点。

到目前为止，我们已经解决了给定从 $\mathbf{x}_1$ 到 $\mathbf{x}_n$ 的观测，求节点 $\mathbf{z}_n$ 的后验边缘分布这一推断问题。接下来考虑给定从 $\mathbf{x}_1$ 到 $\mathbf{x}_N$ 的全部观测，求节点 $\mathbf{z}_n$ 的边缘分布。对于时间数据，这相当于同时纳入未来与过去的观测。虽然这不能用于实时预测，但在学习模型参数时起着关键作用。与隐马尔可夫模型类似，可以将消息从节点 $\mathbf{x}_N$ 反向传递到节点 $\mathbf{x}_1$，再将这些信息与前向消息传递阶段为计算 $\widehat{\alpha}(\mathbf{z}_n)$ 而获得的信息结合起来，以解决这一问题。

在 LDS 文献中，通常用 $\gamma(\mathbf{z}_n)=\widehat{\alpha}(\mathbf{z}_n)\widehat{\beta}(\mathbf{z}_n)$ 来表述这一后向递推，而不是用 $\widehat{\beta}(\mathbf{z}_n)$。由于 $\gamma(\mathbf{z}_n)$ 也必然是高斯分布，因此将其写为

$$
\gamma(\mathbf{z}_n)=\widehat{\alpha}(\mathbf{z}_n)\widehat{\beta}(\mathbf{z}_n)=\mathcal{N}(\mathbf{z}_n\mid\widehat{\boldsymbol{\mu}}_n,\widehat{\mathbf{V}}_n).
\tag{13.98}
$$

为推导所需的递推式，我们从 $\widehat{\beta}(\mathbf{z}_n)$ 的后向递推（13.62）出发，

<!-- pdf-page: 661 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-22.png" alt="用线性动力系统跟踪二维运动物体，显示真实位置、含噪测量、后验均值和协方差椭圆"><figcaption>图 13.22：利用线性动力系统跟踪运动物体的示意图。蓝色点表示物体在连续时间步中于二维空间中的真实位置，绿色点表示带噪声的位置测量，红色叉号表示运行 Kalman 滤波方程后所推断的位置后验分布的均值。所推断位置的协方差由红色椭圆表示，它们对应于一个标准差的等高线。</figcaption><p class="figure-translation">蓝色点：真实位置；绿色点：含噪测量；红色叉号：后验均值；红色椭圆：一个标准差的等高线。</p></figure>

<!-- join-previous-paragraph-across-figures -->
对于连续潜变量，它可以写成

$$
c_{n+1}\widehat{\beta}(\mathbf{z}_n)=\int\widehat{\beta}(\mathbf{z}_{n+1})p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)\,\mathrm{d}\mathbf{z}_{n+1}.
\tag{13.99}
$$

现在将（13.99）的两边乘以 $\widehat{\alpha}(\mathbf{z}_n)$，并用（13.75）和（13.76）代入 $p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1})$ 和 $p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)$。然后使用（13.89）、（13.90）和（13.91），再结合（13.98），经过一些运算可得（习题 13.29）

$$
\widehat{\boldsymbol{\mu}}_n=\boldsymbol{\mu}_n+\mathbf{J}_n\left(\widehat{\boldsymbol{\mu}}_{n+1}-\mathbf{A}\boldsymbol{\mu}_N\right)
\tag{13.100}
$$

$$
\widehat{\mathbf{V}}_n=\mathbf{V}_n+\mathbf{J}_n\left(\widehat{\mathbf{V}}_{n+1}-\mathbf{P}_n\right)\mathbf{J}_n^{\mathrm{T}}
\tag{13.101}
$$

其中定义

$$
\mathbf{J}_n=\mathbf{V}_n\mathbf{A}^{\mathrm{T}}(\mathbf{P}_n)^{-1}
\tag{13.102}
$$

并使用了 $\mathbf{A}\mathbf{V}_n=\mathbf{P}_n\mathbf{J}_n^{\mathrm{T}}$。注意，这些递推要求先完成前向过程，以便在后向过程中使用 $\boldsymbol{\mu}_n$ 和 $\mathbf{V}_n$。

对于 EM 算法，还需要成对的后验边缘分布。由（13.65）可得

$$
\begin{aligned}
\xi(\mathbf{z}_{n-1},\mathbf{z}_n)
&=(c_n)^{-1}\widehat{\alpha}(\mathbf{z}_{n-1})p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{z}_{-1})\widehat{\beta}(\mathbf{z}_n)\\
&=\frac{\mathcal{N}(\mathbf{z}_{n-1}\mid\boldsymbol{\mu}_{n-1},\mathbf{V}_{n-1})\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\mathbf{z}_{n-1},\boldsymbol{\Gamma})\mathcal{N}(\mathbf{x}_n\mid\mathbf{C}\mathbf{z}_n,\boldsymbol{\Sigma})\mathcal{N}(\mathbf{z}_n\mid\widehat{\boldsymbol{\mu}}_n,\widehat{\mathbf{V}}_n)}{c_n\widehat{\alpha}(\mathbf{z}_n)}.
\end{aligned}
\tag{13.103}
$$

用（13.84）代入 $\widehat{\alpha}(\mathbf{z}_n)$ 并整理，可见 $\xi(\mathbf{z}_{n-1},\mathbf{z}_n)$ 为高斯分布，其均值由分量 $\gamma(\mathbf{z}_{n-1})$ 和 $\gamma(\mathbf{z}_n)$ 给出，且 $\mathbf{z}_n$ 与 $\mathbf{z}_{n-1}$ 之间的协方差为（习题 13.31）

$$
\operatorname{cov}[\mathbf{z}_n,\mathbf{z}_{n-1}]=\mathbf{J}_{n-1}\widehat{\mathbf{V}}_n.
\tag{13.104}
$$

<!-- pdf-page: 662 -->

### 13.3.2 LDS 中的学习

到目前为止，我们讨论的是线性动力系统的推断问题，假设模型参数 $\boldsymbol{\theta}=\{\mathbf{A},\boldsymbol{\Gamma},\mathbf{C},\boldsymbol{\Sigma},\boldsymbol{\mu}_0,\mathbf{V}_0\}$ 已知。接下来考虑用最大似然来确定这些参数（Ghahramani and Hinton，1996b）。由于模型具有潜变量，可以使用第 9 章从一般形式讨论过的 EM 算法来处理。

线性动力系统的 EM 算法可推导如下。将算法某一轮迭代中估计出的参数值记为 $\boldsymbol{\theta}^{\mathrm{old}}$。对于这些参数值，可以运行推断算法，确定潜变量的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$；更准确地说，是确定 M 步所需的那些局部后验边缘分布。具体来说，需要以下期望

$$
\mathbb{E}[\mathbf{z}_n]=\widehat{\boldsymbol{\mu}}_n
\tag{13.105}
$$

$$
\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_{n-1}^{\mathrm{T}}\right]=\mathbf{J}_{n-1}\widehat{\mathbf{V}}_n+\widehat{\boldsymbol{\mu}}_n\widehat{\boldsymbol{\mu}}_{n-1}^{\mathrm{T}}
\tag{13.106}
$$

$$
\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}\right]=\widehat{\mathbf{V}}_n+\widehat{\boldsymbol{\mu}}_n\widehat{\boldsymbol{\mu}}_n^{\mathrm{T}}
\tag{13.107}
$$

这里使用了（13.104）。

现在考虑完整数据对数似然函数。对（13.6）取对数，可得

$$
\begin{aligned}
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})
&=\ln p(\mathbf{z}_1\mid\boldsymbol{\mu}_0,\mathbf{V}_0)+\sum_{n=2}^{N}\ln p(\mathbf{z}_n\mid\mathbf{z}_{n-1},\mathbf{A},\boldsymbol{\Gamma})\\
&\quad+\sum_{n=1}^{N}\ln p(\mathbf{x}_n\mid\mathbf{z}_n,\mathbf{C},\boldsymbol{\Sigma})
\end{aligned}
\tag{13.108}
$$

其中已经显式写出了对参数的依赖关系。现在，关于后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$ 取完整数据对数似然的期望，从而定义函数

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=\mathbb{E}_{\mathbf{Z}\mid\boldsymbol{\theta}^{\mathrm{old}}}\left[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})\right].
\tag{13.109}
$$

在 M 步中，关于 $\boldsymbol{\theta}$ 的各个分量最大化这个函数。

先考虑参数 $\boldsymbol{\mu}_0$ 和 $\mathbf{V}_0$。如果用（13.77）代入（13.108）中的 $p(\mathbf{z}_1\mid\boldsymbol{\mu}_0,\mathbf{V}_0)$，再关于 $\mathbf{Z}$ 取期望，得到

$$
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})=-\frac{1}{2}\ln|\mathbf{V}_0|-\mathbb{E}_{\mathbf{Z}\mid\boldsymbol{\theta}^{\mathrm{old}}}\left[\frac{1}{2}(\mathbf{z}_1-\boldsymbol{\mu}_0)^{\mathrm{T}}\mathbf{V}_0^{-1}(\mathbf{z}_1-\boldsymbol{\mu}_0)\right]+\mathrm{const}
$$

这里所有不依赖于 $\boldsymbol{\mu}_0$ 或 $\mathbf{V}_0$ 的项都被吸收到加性常数中。利用第 2.3.4 节讨论的高斯分布的最大似然解，很容易完成关于 $\boldsymbol{\mu}_0$ 和 $\mathbf{V}_0$ 的最大化，得到（习题 13.32）

<!-- pdf-page: 663 -->

$$
\boldsymbol{\mu}_0^{\mathrm{new}}=\mathbb{E}[\mathbf{z}_1]
\tag{13.110}
$$

$$
\mathbf{V}_0^{\mathrm{new}}=\mathbb{E}[\mathbf{z}_1\mathbf{z}_1^{\mathrm{T}}]-\mathbb{E}[\mathbf{z}_1]\mathbb{E}[\mathbf{z}_1^{\mathrm{T}}].
\tag{13.111}
$$

同样，为优化 $\mathbf{A}$ 和 $\boldsymbol{\Gamma}$，用（13.75）代入（13.108）中的 $p(\mathbf{z}_n\mid\mathbf{z}_{n-1},\mathbf{A},\boldsymbol{\Gamma})$，得到

$$
\begin{aligned}
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})
&=-\frac{N-1}{2}\ln|\boldsymbol{\Gamma}|\\
&\quad-\mathbb{E}_{\mathbf{Z}\mid\boldsymbol{\theta}^{\mathrm{old}}}\left[\frac{1}{2}\sum_{n=2}^{N}(\mathbf{z}_n-\mathbf{A}\mathbf{z}_{n-1})^{\mathrm{T}}\boldsymbol{\Gamma}^{-1}(\mathbf{z}_n-\mathbf{A}\mathbf{z}_{n-1})\right]+\mathrm{const}
\end{aligned}
\tag{13.112}
$$

其中的常数由不依赖于 $\mathbf{A}$ 和 $\boldsymbol{\Gamma}$ 的项组成。关于这些参数最大化，得到（习题 13.33）

$$
\mathbf{A}^{\mathrm{new}}=\left(\sum_{n=2}^{N}\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_{n-1}^{\mathrm{T}}\right]\right)\left(\sum_{n=2}^{N}\mathbb{E}\left[\mathbf{z}_{n-1}\mathbf{z}_{n-1}^{\mathrm{T}}\right]\right)^{-1}
\tag{13.113}
$$

$$
\begin{aligned}
\boldsymbol{\Gamma}^{\mathrm{new}}
&=\frac{1}{N-1}\sum_{n=2}^{N}\Bigl\{\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}\right]-\mathbf{A}^{\mathrm{new}}\mathbb{E}\left[\mathbf{z}_{n-1}\mathbf{z}_n^{\mathrm{T}}\right]\\
&\qquad-\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_{n-1}^{\mathrm{T}}\right]\mathbf{A}^{\mathrm{new}}+\mathbf{A}^{\mathrm{new}}\mathbb{E}\left[\mathbf{z}_{n-1}\mathbf{z}_{n-1}^{\mathrm{T}}\right](\mathbf{A}^{\mathrm{new}})^{\mathrm{T}}\Bigr\}.
\end{aligned}
\tag{13.114}
$$

注意，必须先计算 $\mathbf{A}^{\mathrm{new}}$，然后才能利用该结果确定 $\boldsymbol{\Gamma}^{\mathrm{new}}$。

最后，为确定 $\mathbf{C}$ 和 $\boldsymbol{\Sigma}$ 的新值，用（13.76）代入（13.108）中的 $p(\mathbf{x}_n\mid\mathbf{z}_n,\mathbf{C},\boldsymbol{\Sigma})$，得到

$$
\begin{aligned}
Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})
&=-\frac{N}{2}\ln|\boldsymbol{\Sigma}|\\
&\quad-\mathbb{E}_{\mathbf{Z}\mid\boldsymbol{\theta}^{\mathrm{old}}}\left[\frac{1}{2}\sum_{n=1}^{N}(\mathbf{x}_n-\mathbf{C}\mathbf{z}_n)^{\mathrm{T}}\boldsymbol{\Sigma}^{-1}(\mathbf{x}_n-\mathbf{C}\mathbf{z}_n)\right]+\mathrm{const}.
\end{aligned}
$$

关于 $\mathbf{C}$ 和 $\boldsymbol{\Sigma}$ 最大化，得到（习题 13.34）

$$
\mathbf{C}^{\mathrm{new}}=\left(\sum_{n=1}^{N}\mathbf{x}_n\mathbb{E}\left[\mathbf{z}_n^{\mathrm{T}}\right]\right)\left(\sum_{n=1}^{N}\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}\right]\right)^{-1}
\tag{13.115}
$$

$$
\begin{aligned}
\boldsymbol{\Sigma}^{\mathrm{new}}
&=\frac{1}{N}\sum_{n=1}^{N}\Bigl\{\mathbf{x}_n\mathbf{x}_n^{\mathrm{T}}-\mathbf{C}^{\mathrm{new}}\mathbb{E}[\mathbf{z}_n]\mathbf{x}_n^{\mathrm{T}}\\
&\qquad-\mathbf{x}_n\mathbb{E}\left[\mathbf{z}_n^{\mathrm{T}}\right]\mathbf{C}^{\mathrm{new}}+\mathbf{C}^{\mathrm{new}}\mathbb{E}\left[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}\right]\mathbf{C}^{\mathrm{new}}\Bigr\}.
\end{aligned}
\tag{13.116}
$$

<!-- pdf-page: 664 -->

我们用最大似然来处理线性动力系统中的参数学习。纳入先验以得到 MAP 估计并不困难；应用第 10 章讨论的解析近似技术，还可以进行完全贝叶斯处理，不过限于篇幅，这里不作详细讨论。

### 13.3.3 LDS 的扩展

与隐马尔可夫模型一样，人们也十分关注如何扩展基本的线性动力系统，以增强其能力。虽然线性高斯模型的假设带来了高效的推断和学习算法，但也意味着观测变量的边缘分布只是一个高斯分布，这是一项很大的限制。线性动力系统的一种简单扩展，是用高斯混合作为 $\mathbf{z}_1$ 的初始分布。如果该混合有 $K$ 个分量，那么前向递推方程（13.85）会使每个隐变量 $\mathbf{z}_n$ 上的分布成为 $K$ 个高斯分布的混合，因此该模型仍然可以处理。

对于许多应用，高斯发射密度是一种很差的近似。如果尝试用 $K$ 个高斯分布的混合作为发射密度，那么后验 $\widehat{\alpha}(\mathbf{z}_1)$ 也将是 $K$ 个高斯分布的混合。然而，由（13.85）可知，后验 $\widehat{\alpha}(\mathbf{z}_2)$ 将由 $K^2$ 个高斯分布混合而成，依此类推，$\widehat{\alpha}(\mathbf{z}_n)$ 将是 $K^n$ 个高斯分布的混合。因此，分量的数量随链的长度指数增长，这个模型也就不切实际。

更一般地，引入不属于线性高斯模型（或其他指数族模型）的转移模型或发射模型，会使推断问题难以计算。可以使用假定密度滤波或期望传播等确定性近似（第 10 章），也可以使用第 13.3.4 节讨论的采样方法。一种广泛使用的方法是在预测分布的均值附近线性化，从而作出高斯近似，由此得到*扩展 Kalman 滤波*（extended Kalman filter）（Zarchan and Musoff，2005）。

与隐马尔可夫模型一样，可以通过扩展基本线性动力系统的图表示，构造一些有意义的推广。例如，*切换状态空间模型*（switching state space model）（Ghahramani and Hinton，1998）可以看作隐马尔可夫模型与一组线性动力系统的组合。该模型包含多条由连续线性高斯潜变量组成的马尔可夫链，每一条都类似于前面讨论的线性动力系统的潜变量链；此外，还有一条由离散变量组成的马尔可夫链，其形式与隐马尔可夫模型中使用的链相同。在每个时间步，以离散潜变量的状态作为开关，随机选择其中一条连续潜变量链，再从对应的条件输出分布发射一个观测，从而确定该时间步的输出。在这个模型中，精确推断难以计算，但变分方法可以得到高效的推断方案：分别沿每条连续和离散马尔可夫链独立执行前向—后向递推。注意，如果考虑多条离散潜变量链，并用其中一条作为开关，从其余各条链中作出选择，就得到一种仅含离散潜变量的类似模型，称为*切换隐马尔可夫模型*（switching hidden Markov model）。

<!-- pdf-page: 665 -->

### 13.3.4 粒子滤波器

对于不具有线性高斯形式的动力系统，例如采用非高斯发射密度的系统，可以转向采样方法（第 11 章），以找到计算上可行的推断算法。具体来说，可以应用第 11.1.5 节的采样—重要性—重采样方法，得到一种称为粒子滤波器（particle filter）的序贯蒙特卡洛算法。

考虑图 13.5 的图模型所表示的那类分布。假设给定观测值 $\mathbf{X}_n=(\mathbf{x}_1,\ldots,\mathbf{x}_n)$，希望从后验分布 $p(\mathbf{z}_n\mid\mathbf{X}_n)$ 中抽取 $L$ 个样本。利用贝叶斯定理，有

$$
\begin{aligned}
\mathbb{E}[f(\mathbf{z}_n)]
&=\int f(\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_n)\,\mathrm{d}\mathbf{z}_n\\
&=\int f(\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{x}_n,\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n\\
&=\frac{\int f(\mathbf{z}_n)p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n}{\int p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n}\\
&\simeq\sum_{l=1}^{L}w_n^{(l)}f(\mathbf{z}_n^{(l)})
\end{aligned}
\tag{13.117}
$$

其中，$\{\mathbf{z}_n^{(l)}\}$ 是从 $p(\mathbf{z}_n\mid\mathbf{X}_{n-1})$ 中抽取的一组样本，并且使用了由图 13.5 可知的条件独立性质 $p(\mathbf{x}_n\mid\mathbf{z}_n,\mathbf{X}_{n-1})=p(\mathbf{x}_n\mid\mathbf{z}_n)$。采样权重 $\{w_n^{(l)}\}$ 定义为

$$
w_n^{(l)}=\frac{p(\mathbf{x}_n\mid\mathbf{z}_n^{(l)})}{\sum_{m=1}^{L}p(\mathbf{x}_n\mid\mathbf{z}_n^{(m)})}
\tag{13.118}
$$

其中，分子和分母使用相同的样本。因此，后验分布 $p(\mathbf{z}_n\mid\mathbf{x}_n)$ 由样本集合 $\{\mathbf{z}_n^{(l)}\}$ 及其对应权重 $\{w_n^{(l)}\}$ 表示。注意，这些权重满足 $0\leqslant w_n^{(l)}1$ 和 $\sum_l w_n^{(l)}=1$。

由于希望得到一种序贯采样方案，假设已经在时间步 $n$ 得到一组样本和权重，随后又观测到了 $\mathbf{x}_{n+1}$ 的值，现在希望求出时间步 $n+1$ 的权重和样本。首先从分布 $p(\mathbf{z}_{n+1}\mid\mathbf{X}_n)$ 中采样。这

<!-- pdf-page: 666 -->
<!-- join-previous-paragraph -->
很容易做到，因为再次利用贝叶斯定理，有

$$
\begin{aligned}
p(\mathbf{z}_{n+1}\mid\mathbf{X}_n)
&=\int p(\mathbf{z}_{n+1}\mid\mathbf{z}_n,\mathbf{X}_n)p(\mathbf{z}_n\mid\mathbf{X}_n)\,\mathrm{d}\mathbf{z}_n\\
&=\int p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_n)\,\mathrm{d}\mathbf{z}_n\\
&=\int p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{x}_n,\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n\\
&=\frac{\int p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n}{\int p(\mathbf{x}_n\mid\mathbf{z}_n)p(\mathbf{z}_n\mid\mathbf{X}_{n-1})\,\mathrm{d}\mathbf{z}_n}\\
&=\sum_l w_n^{(l)}p(\mathbf{z}_{n+1}\mid\mathbf{z}_n^{(l)})
\end{aligned}
\tag{13.119}
$$

这里使用了条件独立性质

$$
p(\mathbf{z}_{n+1}\mid\mathbf{z}_n,\mathbf{X}_n)=p(\mathbf{z}_{n+1}\mid\mathbf{z}_n)
\tag{13.120}
$$

$$
p(\mathbf{x}_n\mid\mathbf{z}_n,\mathbf{X}_{n-1})=p(\mathbf{x}_n\mid\mathbf{z}_n)
\tag{13.121}
$$

它们可通过对图 13.5 应用 d 分离准则得到。（13.119）给出的分布是一个混合分布，可以先按混合系数 $w^{(l)}$ 给出的概率选择分量 $l$，再从对应的分量中抽取样本。

因此，粒子滤波算法的每一步可以看作包含两个阶段。在时间步 $n$，后验分布 $p(\mathbf{z}_n\mid\mathbf{X}_n)$ 由样本 $\{\mathbf{z}_n^{(l)}\}$ 及其对应的权重 $\{w_n^{(l)}\}$ 表示。这可以看作（13.119）形式的混合表示。为得到下一个时间步的相应表示，首先从混合分布（13.119）中抽取 $L$ 个样本，然后对每个样本，利用新的观测 $\mathbf{x}_{n+1}$ 计算对应的权重 $w_{n+1}^{(l)}\propto p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1}^{(l)})$。图 13.23 对单个变量 $z$ 的情形给出了示意图。

粒子滤波，也称序贯蒙特卡洛方法，在文献中以多种名称出现，包括*自助滤波器*（bootstrap filter）（Gordon et al.，1993）、*适者生存*（survival of the fittest）（Kanazawa et al.，1995）和*凝聚*（condensation）算法（Isard and Blake，1998）。

## 习题

**13.1（⋆） www** 使用第 8.2 节讨论的 d 分离技术，验证图 13.3 所示、总共具有 $N$ 个节点的马尔可夫模型，对 $n=2,\ldots,N$ 满足条件独立性质（13.3）。同样，证明由图 13.4 描述、总共具有 $N$ 个节点的模型

<!-- pdf-page: 667 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-13/b-fig-13-23.png" alt="粒子滤波在一维潜空间中的四层示意图，显示带权粒子、预测样本、发射密度和更新后的粒子权重"><figcaption>图 13.23：粒子滤波器在一维潜空间中的运行示意图。在时间步 $n$，后验 $p(z_n\mid\mathbf{x}_n)$ 表示为一个混合分布，图中用圆圈示意，圆圈的大小与权重 $w_n^{(l)}$ 成正比。随后从该分布中抽取一组 $L$ 个样本，并利用 $p(\mathbf{x}_{n+1}\mid\mathbf{z}_{n+1}^{(l)})$ 计算新的权重 $w_{n+1}^{(l)}$。</figcaption><p class="figure-translation">$p(z_n\mid\mathbf{X}_n)$：当前状态的后验分布；$p(z_{n+1}\mid\mathbf{X}_n)$：下一状态的预测分布；$p(\mathbf{x}_{n+1}\mid z_{n+1})$：新观测的发射密度；$p(z_{n+1}\mid\mathbf{X}_{n+1})$：纳入新观测后的后验分布；$z$：一维潜变量。圆圈大小表示粒子权重，红色曲线表示发射密度，蓝色箭头表示采样和权重更新过程。</p></figure>

<!-- join-previous-paragraph-across-figures -->
满足条件独立性质

$$
p(\mathbf{x}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})=p(\mathbf{x}_n\mid\mathbf{x}_{n-1},\mathbf{x}_{n-2})
\tag{13.122}
$$

其中 $n=3,\ldots,N$。

**13.2（⋆⋆）** 考虑与图 13.3 的有向图对应的联合概率分布（13.2）。利用概率的加法规则和乘法规则，验证该联合分布对 $n=2,\ldots,N$ 满足条件独立性质（13.3）。同样，证明由联合分布（13.4）描述的二阶马尔可夫模型满足条件独立性质

$$
p(\mathbf{x}_n\mid\mathbf{x}_1,\ldots,\mathbf{x}_{n-1})=p(\mathbf{x}_n\mid\mathbf{x}_{n-1},\mathbf{x}_{n-2})
\tag{13.123}
$$

其中 $n=3,\ldots,N$。

**13.3（⋆）** 利用 d 分离，证明图 13.5 中有向图所表示的状态空间模型，其观测数据的分布 $p(\mathbf{x}_1,\ldots,\mathbf{x}_N)$ 不满足任何条件独立性质，因此不具有任何有限阶的马尔可夫性质。

**13.4（⋆⋆） www** 考虑一个隐马尔可夫模型，其发射密度由参数模型 $p(\mathbf{x}\mid\mathbf{z},\mathbf{w})$ 表示，例如线性回归模型或神经网络，其中 $\mathbf{w}$ 是可调参数向量。描述如何用最大似然从数据中学习参数 $\mathbf{w}$。

<!-- pdf-page: 668 -->

**13.5（⋆⋆）** 通过最大化完整数据对数似然的期望（13.17），验证隐马尔可夫模型中初始状态概率和转移概率参数的 M 步方程（13.18）与（13.19）。使用适当的拉格朗日乘子，施加 $\boldsymbol{\pi}$ 和 $\mathbf{A}$ 各分量上的求和约束。

**13.6（⋆）** 证明，如果隐马尔可夫模型的参数 $\boldsymbol{\pi}$ 或 $\mathbf{A}$ 中的任意元素在初始化时被设为零，那么这些元素在 EM 算法后续所有更新中都将保持为零。

**13.7（⋆）** 考虑具有高斯发射密度的隐马尔可夫模型。证明，关于各高斯分布的均值与协方差参数最大化函数 $Q(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$，可得到 M 步方程（13.20）和（13.21）。

**13.8（⋆⋆） www** 对于离散观测由多项分布描述的隐马尔可夫模型，证明，给定隐变量时观测的条件分布由（13.22）给出，相应的 M 步方程由（13.23）给出。再考虑一个具有多个二元输出变量的隐马尔可夫模型，其中每个输出变量都由一个伯努利条件分布描述，写出这一情形下条件分布与 M 步方程的对应形式。提示：如有需要，可参考第 2.1 节和第 2.2 节中对独立同分布数据相应最大似然解的讨论。

**13.9（⋆⋆） www** 使用 d 分离准则，验证由（13.6）定义的隐马尔可夫模型的联合分布满足条件独立性质（13.24）—（13.31）。

**13.10（⋆⋆⋆）** 应用概率的加法规则和乘法规则，验证由（13.6）定义的隐马尔可夫模型的联合分布满足条件独立性质（13.24）—（13.31）。

**13.11（⋆⋆）** 从因子图中某个因子所涉及变量的边缘分布表达式（8.72）出发，结合第 13.2.3 节得到的和积算法消息的结果，推导隐马尔可夫模型中两个相邻潜变量的联合后验分布（13.43）。

**13.12（⋆⋆）** 假设希望通过最大似然训练隐马尔可夫模型，数据由 $R$ 条相互独立的观测序列组成，记为 $\mathbf{X}^{(r)}$，其中 $r=1,\ldots,R$。证明，在 EM 算法的 E 步中，只需对各条序列独立运行 $\alpha$ 和 $\beta$ 递推，就能计算潜变量的后验概率。还要证明，在 M 步中，初始概率和转移概率参数的重估

<!-- pdf-page: 669 -->
<!-- join-previous-paragraph -->
使用（13.18）与（13.19）的修正形式，即

$$
\pi_k=\frac{\displaystyle\sum_{r=1}^{R}\gamma(z_{1k}^{(r)})}{\displaystyle\sum_{r=1}^{R}\sum_{j=1}^{K}\gamma(z_{1j}^{(r)})}
\tag{13.124}
$$

$$
A_{jk}=\frac{\displaystyle\sum_{r=1}^{R}\sum_{n=2}^{N}\xi(z_{n-1,j}^{(r)},z_{n,k}^{(r)})}{\displaystyle\sum_{r=1}^{R}\sum_{l=1}^{K}\sum_{n=2}^{N}\xi(z_{n-1,j}^{(r)},z_{n,l}^{(r)})}
\tag{13.125}
$$

其中，为方便记号，假设各条序列具有相同的长度；推广到不同长度的序列并不困难。同样，证明高斯发射模型均值重估的 M 步方程为

$$
\boldsymbol{\mu}_k=\frac{\displaystyle\sum_{r=1}^{R}\sum_{n=1}^{N}\gamma(z_{nk}^{(r)})\mathbf{x}_n^{(r)}}{\displaystyle\sum_{r=1}^{R}\sum_{n=1}^{N}\gamma(z_{nk}^{(r)})}.
\tag{13.126}
$$

注意，其他发射模型参数和分布的 M 步方程也具有类似的形式。

**13.13（⋆⋆） www** 利用因子图中从因子节点传递到变量节点的消息的定义（8.64），结合隐马尔可夫模型联合分布的表达式（13.6），证明 alpha 消息的定义（13.50）与定义（13.34）相同。

**13.14（⋆⋆）** 利用因子图中从因子节点传递到变量节点的消息的定义（8.67），结合隐马尔可夫模型联合分布的表达式（13.6），证明 beta 消息的定义（13.52）与定义（13.35）相同。

**13.15（⋆⋆）** 利用隐马尔可夫模型中边缘分布的表达式（13.33）与（13.43），推导用重新缩放的变量表示的对应结果（13.64）与（13.65）。

**13.16（⋆⋆⋆）** 本题直接从联合分布的表达式（13.6）推导 Viterbi 算法的前向消息传递方程。这需要关于所有隐变量 $\mathbf{z}_1,\ldots,\mathbf{z}_N$ 最大化。通过取对数，再交换最大化与求和的顺序，推导递推

<!-- pdf-page: 670 -->
<!-- join-previous-paragraph -->
（13.68），其中 $\omega(\mathbf{z}_n)$ 由（13.70）定义。证明，这一递推的初始条件由（13.69）给出。

**13.17（⋆） www** 证明，图 13.18 给出的输入输出隐马尔可夫模型的有向图，可以表示为图 13.15 所示形式的树结构因子图，并写出初始因子 $h(\mathbf{z}_1)$ 和一般因子 $f_n(\mathbf{z}_{n-1},\mathbf{z}_n)$ 的表达式，其中 $2\leqslant n\leqslant N$。

**13.18（⋆⋆⋆）** 利用习题 13.17 的结果，推导图 13.18 所示输入输出隐马尔可夫模型的前向—后向算法的递推方程，包括初始条件。

**13.19（⋆） www** 对于线性动力系统，Kalman 滤波与平滑方程可以高效地求得给定所有观测变量时，各个潜变量的后验分布。证明，分别最大化每个后验分布所得到的潜变量值序列，与最可能的潜变量值序列相同。为此，只需注意到线性动力系统中所有潜变量和观测变量的联合分布是高斯分布，因此所有条件分布和边缘分布也都是高斯分布，然后利用结果（2.98）。

**13.20（⋆⋆） www** 利用结果（2.115）证明（13.87）。

**13.21（⋆⋆）** 利用结果（2.115）与（2.116），结合矩阵恒等式（C.5）与（C.7），推导结果（13.89）、（13.90）和（13.91），其中 Kalman 增益矩阵 $\mathbf{K}_n$ 由（13.92）定义。

**13.22（⋆⋆） www** 利用（13.93），结合定义（13.76）、（13.77）和结果（2.115），推导（13.96）。

**13.23（⋆⋆）** 利用（13.93），结合定义（13.76）、（13.77）和结果（2.116），推导（13.94）、（13.95）和（13.97）。

**13.24（⋆⋆） www** 考虑（13.75）和（13.76）的一种推广，在高斯均值中纳入常数项 $\mathbf{a}$ 和 $\mathbf{c}$，使得

$$
p(\mathbf{z}_n\mid\mathbf{z}_{n-1})=\mathcal{N}(\mathbf{z}_n\mid\mathbf{A}\mathbf{z}_{n-1}+\mathbf{a},\boldsymbol{\Gamma})
\tag{13.127}
$$

$$
p(\mathbf{x}_n\mid\mathbf{z}_n)=\mathcal{N}(\mathbf{x}_n\mid\mathbf{C}\mathbf{z}_n+\mathbf{c},\boldsymbol{\Sigma}).
\tag{13.128}
$$

证明，定义一个增加了固定为 1 的分量的状态向量 $\mathbf{z}$，再用对应于参数 $\mathbf{a}$ 和 $\mathbf{c}$ 的额外列扩充矩阵 $\mathbf{A}$ 与 $\mathbf{C}$，就可以将这一扩展重新表述为本章所讨论的框架。

**13.25（⋆⋆）** 本题证明，当 Kalman 滤波方程应用于独立观测时，会化为第 2.3 节给出的单个高斯分布的最大似然解。考虑求单个高斯随机变量 $x$ 的均值 $\mu$ 的问题，给定一组独立观测 $\{x_1,\ldots,x_N\}$。为对此建模，可以使用

<!-- pdf-page: 671 -->
<!-- join-previous-paragraph -->
由（13.75）和（13.76）描述的线性动力系统，其潜变量为 $\{z_1,\ldots,z_N\}$，其中 $\mathbf{C}$ 变为单位矩阵，并且由于各个观测相互独立，转移概率 $\mathbf{A}=\mathbf{0}$。将初始状态的参数 $\mathbf{m}_0$ 和 $\mathbf{V}_0$ 分别记为 $\mu_0$ 和 $\sigma_0^2$，并假设 $\boldsymbol{\Sigma}$ 变为 $\sigma^2$。从一般结果（13.89）和（13.90）出发，结合（13.94）和（13.95），写出相应的 Kalman 滤波方程。证明，它们等价于直接考虑独立数据时得到的结果（2.141）和（2.142）。

**13.26（⋆⋆⋆）** 考虑第 13.3 节线性动力系统中等价于概率 PCA 的一个特殊情形，此时转移矩阵 $\mathbf{A}=\mathbf{0}$，协方差 $\boldsymbol{\Gamma}=\mathbf{I}$，噪声协方差 $\boldsymbol{\Sigma}=\sigma^2\mathbf{I}$。利用矩阵求逆恒等式（C.7）证明，如果将发射密度矩阵 $\mathbf{C}$ 记为 $\mathbf{W}$，那么（13.89）与（13.90）定义的隐状态后验分布就化为概率 PCA 的结果（12.42）。

**13.27（⋆） www** 考虑第 13.3 节所讨论形式的线性动力系统，其中观测噪声的幅度趋于零，因此 $\boldsymbol{\Sigma}=\mathbf{0}$。证明，$\mathbf{z}_n$ 的后验分布的均值为 $\mathbf{x}_n$，方差为零。这符合我们的直觉：如果没有噪声，就应直接用当前观测 $\mathbf{x}_n$ 估计状态变量 $\mathbf{z}_n$，并忽略所有先前的观测。

**13.28（⋆⋆⋆）** 考虑第 13.3 节线性动力系统的一个特殊情形，状态变量 $\mathbf{z}_n$ 被约束为等于前一个状态变量，对应于 $\mathbf{A}=\mathbf{I}$ 和 $\boldsymbol{\Gamma}=\mathbf{0}$。为简单起见，再假设 $\mathbf{V}_0\to\infty$，使得 $\mathbf{z}$ 的初始条件不重要，预测完全由数据决定。用数学归纳法证明，状态 $\mathbf{z}_n$ 的后验均值由 $\mathbf{x}_1,\ldots,\mathbf{x}_n$ 的平均值确定。这对应于直观结果：如果状态变量是常数，那么对观测取平均就能得到最佳估计。

**13.29（⋆⋆⋆）** 从后向递推方程（13.99）出发，推导高斯线性动力系统的 RTS 平滑方程（13.100）与（13.101）。

**13.30（⋆⋆）** 从状态空间模型中成对后验边缘分布的结果（13.65）出发，推导高斯线性动力系统情形下的具体形式（13.103）。

**13.31（⋆⋆）** 从结果（13.103）出发，并用（13.84）代入 $\widehat{\alpha}(\mathbf{z}_n)$，验证 $\mathbf{z}_n$ 与 $\mathbf{z}_{n-1}$ 之间协方差的结果（13.104）。

**13.32（⋆⋆） www** 验证线性动力系统中 $\boldsymbol{\mu}_0$ 和 $\mathbf{V}_0$ 的 M 步方程（13.110）与（13.111）。

**13.33（⋆⋆）** 验证线性动力系统中 $\mathbf{A}$ 和 $\boldsymbol{\Gamma}$ 的 M 步方程（13.113）与（13.114）。

<!-- pdf-page: 672 -->

**13.34（⋆⋆）** 验证线性动力系统中 $\mathbf{C}$ 和 $\boldsymbol{\Sigma}$ 的 M 步方程（13.115）与（13.116）。
