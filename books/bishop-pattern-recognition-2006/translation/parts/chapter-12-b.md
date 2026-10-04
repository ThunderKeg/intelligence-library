<!-- pdf-page: 603 -->

由于这一积分难以计算，我们使用拉普拉斯近似（第 4.4 节）。假设后验分布具有尖锐的峰，这在数据集足够大时会出现，那么关于 $\alpha_i$ 最大化边缘似然所得到的重估方程，就具有如下简单形式（第 3.5.3 节）：

$$
\alpha_i^{\mathrm{new}}=\frac{D}{\mathbf{w}_i^{\mathrm{T}}\mathbf{w}_i}
\tag{12.62}
$$

注意到 $\mathbf{w}_i$ 的维数为 $D$，这个结果即可由（3.98）得到。这些重估步骤与用于确定 $\mathbf{W}$ 和 $\sigma^2$ 的 EM 算法更新交替进行。E 步的方程仍由（12.54）和（12.55）给出。类似地，$\sigma^2$ 的 M 步方程仍由（12.57）给出。唯一的变化是 $\mathbf{W}$ 的 M 步方程，它修改为

$$
\mathbf{W}_{\mathrm{new}}=\left[\sum_{n=1}^N(\mathbf{x}_n-\overline{\mathbf{x}})\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\right]\left[\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]+\sigma^2\mathbf{A}\right]^{-1}
\tag{12.63}
$$

其中 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。与前面一样，$\boldsymbol{\mu}$ 的值由样本均值给出。

如果选择 $M=D-1$，那么，当所有 $\alpha_i$ 都是有限值时，模型表示一个具有完整协方差的高斯分布；当所有 $\alpha_i$ 都趋于无穷大时，模型等价于各向同性高斯分布。因此，模型能够涵盖主子空间有效维数的所有允许值。也可以考虑较小的 $M$，这样会节省计算成本，但会限制子空间的最大维数。图 12.14 比较了这一算法与标准概率 PCA 的结果。

贝叶斯 PCA 提供了一个展示第 11.3 节所讨论的 Gibbs 采样算法的机会。图 12.15 给出了超参数 $\ln\alpha_i$ 的采样示例：数据集位于 $D=4$ 维空间，潜空间的维数为 $M=3$，但数据集是由一个概率 PCA 模型生成的，该模型只有一个方向具有较高方差，其余方向都是低方差噪声。这个结果清楚地显示，后验分布存在三个不同的模态。在每一步迭代中，一个超参数较小，其余两个较大，因此三个潜变量中的两个受到抑制。在 Gibbs 采样过程中，解会在这三个模态之间突然切换。

这里描述的模型只对矩阵 $\mathbf{W}$ 引入了先验。Bishop（1999b）介绍了一种完全贝叶斯的 PCA 处理方式，其中还对 $\boldsymbol{\mu}$、$\sigma^2$ 和 $\boldsymbol{\alpha}$ 引入先验，并使用变分方法求解。关于确定 PCA 模型合适维数的各种贝叶斯方法，参见 Minka（2001c）。

### 12.2.4 因子分析

因子分析是一种线性高斯潜变量模型，与概率 PCA 密切相关。它的定义与概率 PCA 只有一点不同：给定潜变量 $\mathbf{z}$ 时，观测变量 $\mathbf{x}$ 的条件分布

<!-- pdf-page: 604 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-14.png" alt="矩阵 W 的两个 Hinton 图，用面积不同的黑白方块表现各矩阵元素及部分列被抑制的结果"><figcaption>图 12.14：矩阵 $\mathbf{W}$ 的“Hinton 图”，其中每个矩阵元素都表示为一个正方形（白色表示正值，黑色表示负值），其面积与该元素的绝对值成正比。合成数据集包含 $D=10$ 维空间中的 300 个数据点，它们采样自一个高斯分布，该分布在 3 个方向上的标准差为 1.0，在其余 7 个方向上的标准差为 0.5；这是一个 $D=10$ 维数据集，其中 $M=3$ 个方向的方差大于其余 7 个方向。左图显示最大似然概率 PCA 的结果，左图显示贝叶斯 PCA 的相应结果。可以看到，贝叶斯模型能够通过抑制 6 个多余的自由度，发现合适的维数。</figcaption><p class="figure-translation">白色方块：正的矩阵元素；黑色方块：负的矩阵元素；方块面积：相应矩阵元素的绝对值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
采用对角协方差，而不是各向同性协方差，即

$$
p(\mathbf{x}\mid\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{W}\mathbf{z}+\boldsymbol{\mu},\boldsymbol{\Psi})
\tag{12.64}
$$

其中，$\boldsymbol{\Psi}$ 是一个 $D\times D$ 对角矩阵。注意，因子分析模型与概率 PCA 一样，假设给定潜变量 $\mathbf{z}$ 后，观测变量 $x_1,\ldots,x_D$ 相互独立。实质上，因子分析模型将与每个坐标相关的独立方差表示在矩阵 $\boldsymbol{\Psi}$ 中，将变量之间的协方差表示在矩阵 $\mathbf{W}$ 中，从而解释数据中观察到的协方差结构。在因子分析文献中，$\mathbf{W}$ 的各列捕捉观测变量之间的相关性，称为 *因子载荷*（factor loadings）；$\boldsymbol{\Psi}$ 的对角元素表示各变量的独立噪声方差，称为 *独特性*（uniquenesses）。

因子分析的起源与 PCA 同样久远，Everitt（1984）、Bartholomew（1987）和 Basilevsky（1994）的著作中都有关于因子分析的讨论。Lawley（1953）和 Anderson（1963）研究了因子分析与 PCA 之间的联系。他们证明，对于满足 $\boldsymbol{\Psi}=\sigma^2\mathbf{I}$ 的因子分析模型，在似然函数的驻点处，$\mathbf{W}$ 的各列是样本协方差矩阵经过缩放的特征向量，而 $\sigma^2$ 是被舍弃的特征值的平均值。随后，Tipping and Bishop（1999b）证明，当构成 $\mathbf{W}$ 的特征向量选为主特征向量时，对数似然函数达到最大值。

利用（2.115）可知，观测

<!-- pdf-page: 605 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-15.png" alt="贝叶斯 PCA 的三个对数超参数 Gibbs 采样轨迹，分别用红绿蓝曲线显示三个后验模态间的切换"><figcaption>图 12.15：贝叶斯 PCA 的 Gibbs 采样，展示三个 $\alpha$ 值各自的 $\ln\alpha_i$ 随迭代次数变化的曲线，可以看到后验分布三个模态之间的切换。</figcaption><p class="figure-translation">横向：迭代次数；纵向：$\ln\alpha_i$。上、中、下三条轨迹分别对应三个超参数，以红色、绿色、蓝色表示。</p></figure>

<!-- join-previous-paragraph-across-figures -->
变量的边缘分布为 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\mathbf{C})$，其中现在有

$$
\mathbf{C}=\mathbf{W}\mathbf{W}^{\mathrm{T}}+\boldsymbol{\Psi}.
\tag{12.65}
$$

与概率 PCA 一样，这个模型在潜空间旋转下保持不变（习题 12.19）。

历史上，当人们尝试解释各个因子（即 $\mathbf{z}$ 空间中的坐标）时，因子分析曾引发争议。由于这个空间中的旋转造成因子分析不可辨识，这种解释被证明存在问题。不过，从我们的角度看，因子分析是一种潜变量密度模型，我们关心的是潜空间的形式，而不是用来描述它的具体坐标选择。如果希望消除潜空间旋转带来的退化，就必须考虑非高斯的潜变量分布，这会得到独立成分分析（ICA）模型（第 12.4 节）。

可以通过最大似然确定因子分析模型中的参数 $\boldsymbol{\mu}$、$\mathbf{W}$ 和 $\boldsymbol{\Psi}$。$\boldsymbol{\mu}$ 的解仍由样本均值给出。不过，与概率 PCA 不同，$\mathbf{W}$ 不再具有闭式的最大似然解，因此必须通过迭代求得。由于因子分析是一种潜变量模型，可以使用类似于概率 PCA 的 EM 算法（Rubin and Thayer，1982）完成这一点（习题 12.21）。具体来说，E 步方程为

$$
\mathbb{E}[\mathbf{z}_n]=\mathbf{G}\mathbf{W}^{\mathrm{T}}\boldsymbol{\Psi}^{-1}(\mathbf{x}_n-\overline{\mathbf{x}})
\tag{12.66}
$$

$$
\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]=\mathbf{G}+\mathbb{E}[\mathbf{z}_n]\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}
\tag{12.67}
$$

其中定义了

$$
\mathbf{G}=(\mathbf{I}+\mathbf{W}^{\mathrm{T}}\boldsymbol{\Psi}^{-1}\mathbf{W})^{-1}.
\tag{12.68}
$$

注意，这种表达形式只涉及对 $M\times M$ 矩阵求逆，而不是对 $D\times D$ 矩阵求逆（$D\times D$ 对角矩阵 $\boldsymbol{\Psi}$ 除外，它的逆很容易

<!-- pdf-page: 606 -->
<!-- join-previous-paragraph -->
在 $O(D)$ 步内算出），这很方便，因为通常 $M\ll D$。类似地，M 步方程为（习题 12.22）

$$
\mathbf{W}^{\mathrm{new}}=\left[\sum_{n=1}^N(\mathbf{x}_n-\overline{\mathbf{x}})\mathbb{E}[\mathbf{z}_n]^{\mathrm{T}}\right]\left[\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n\mathbf{z}_n^{\mathrm{T}}]\right]^{-1}
\tag{12.69}
$$

$$
\boldsymbol{\Psi}^{\mathrm{new}}=\operatorname{diag}\left\{\mathbf{S}-\mathbf{W}_{\mathrm{new}}\frac{1}{N}\sum_{n=1}^N\mathbb{E}[\mathbf{z}_n](\mathbf{x}_n-\overline{\mathbf{x}})^{\mathrm{T}}\right\}
\tag{12.70}
$$

其中，“diag”算子将矩阵的所有非对角元素设为零。直接应用本书讨论的技术，就可以得到因子分析模型的贝叶斯处理方式。

概率 PCA 与因子分析的另一个区别，是它们在数据集变换下的行为不同（习题 12.25）。对于 PCA 和概率 PCA，如果旋转数据空间中的坐标系，就会得到完全相同的数据拟合，但 $\mathbf{W}$ 矩阵要由相应的旋转矩阵进行变换。对于因子分析，相应的性质则是：如果对数据向量的各个分量分别重新缩放，那么这种变换就会被吸收到 $\boldsymbol{\Psi}$ 各元素相应的重新缩放中。

## 12.3 核 PCA

第 6 章已经介绍，核替换技术允许我们将一个以 $\mathbf{x}^{\mathrm{T}}\mathbf{x}'$ 形式的标量积表达的算法，通过把这些标量积替换为非线性核，推广为更一般的算法。这里将核替换技术应用于主成分分析，从而得到一种称为 *核 PCA*（kernel PCA）的非线性推广（Schölkopf et al.，1998）。

考虑一个由观测 $\{\mathbf{x}_n\}$ 组成的数据集，其中 $n=1,\ldots,N$，每个观测位于 $D$ 维空间中。为了使记号简洁，假设已经从每个向量 $\mathbf{x}_n$ 中减去了样本均值，因此 $\sum_n\mathbf{x}_n=\mathbf{0}$。第一步是将传统 PCA 写成一种形式，使数据向量 $\{\mathbf{x}_n\}$ 仅以标量积 $\mathbf{x}_n^{\mathrm{T}}\mathbf{x}_m$ 的形式出现。回顾主成分由协方差矩阵的特征向量 $\mathbf{u}_i$ 定义：

$$
\mathbf{S}\mathbf{u}_i=\lambda_i\mathbf{u}_i
\tag{12.71}
$$

其中 $i=1,\ldots,D$。这里，$D\times D$ 样本协方差矩阵 $\mathbf{S}$ 定义为

$$
\mathbf{S}=\frac{1}{N}\sum_{n=1}^N\mathbf{x}_n\mathbf{x}_n^{\mathrm{T}},
\tag{12.72}
$$

并且对特征向量归一化，使 $\mathbf{u}_i^{\mathrm{T}}\mathbf{u}_i=1$。

现在考虑将数据映射到一个 $M$ 维特征空间的非线性变换 $\boldsymbol{\phi}(\mathbf{x})$，从而将每个数据点 $\mathbf{x}_n$ 投影为一个点 $\boldsymbol{\phi}(\mathbf{x}_n)$。这样，就可以

<!-- pdf-page: 607 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-16.png" alt="原数据空间中的非线性投影曲线与特征空间中的线性主轴及投影线"><figcaption>图 12.16：核 PCA 的示意图。原数据空间中的数据集（左图），通过非线性变换 $\boldsymbol{\phi}(\mathbf{x})$ 投影到特征空间（右图）。在特征空间中进行 PCA，就得到主成分，其中第一个以蓝色表示，并用向量 $\mathbf{v}_1$ 标记。特征空间中的绿色线表示到第一主成分的线性投影，它们对应于原数据空间中的非线性投影。注意，一般无法用 $\mathbf{x}$ 空间中的一个向量来表示非线性主成分。</figcaption><p class="figure-translation">$x_1$、$x_2$：原数据空间的坐标；$\phi_1$、$\phi_2$：特征空间的坐标；$\mathbf{v}_1$：特征空间中的第一主成分方向。红点表示数据，蓝线表示第一主轴，绿线表示相应投影。</p></figure>

<!-- join-previous-paragraph-across-figures -->
在特征空间中进行标准 PCA，它隐式地在原数据空间中定义了一个非线性主成分模型，如图 12.16 所示。

暂时假设投影后的数据集也具有零均值，即 $\sum_n\boldsymbol{\phi}(\mathbf{x}_n)=\mathbf{0}$。稍后会回到这一点。特征空间中的 $M\times M$ 样本协方差矩阵为

$$
\mathbf{C}=\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}
\tag{12.73}
$$

其特征向量展开由下式定义：

$$
\mathbf{C}\mathbf{v}_i=\lambda_i\mathbf{v}_i
\tag{12.74}
$$

其中 $i=1,\ldots,M$。我们的目标是在不显式进入特征空间运算的情况下，求解这个特征值问题。由 $\mathbf{C}$ 的定义，特征向量方程表明 $\mathbf{v}_i$ 满足

$$
\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\left\{\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\mathbf{v}_i\right\}=\lambda_i\mathbf{v}_i
\tag{12.75}
$$

因此，只要 $\lambda_i>0$，向量 $\mathbf{v}_i$ 就是各 $\boldsymbol{\phi}(\mathbf{x}_n)$ 的线性组合，可以写成

$$
\mathbf{v}_i=\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x}_n).
\tag{12.76}
$$

<!-- pdf-page: 608 -->

将这个展开式代回特征向量方程，得到

$$
\frac{1}{N}\sum_{n=1}^N\boldsymbol{\phi}(\mathbf{x}_n)\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\sum_{m=1}^N a_{im}\boldsymbol{\phi}(\mathbf{x}_m)=\lambda_i\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x}_n).
\tag{12.77}
$$

关键的一步，是用核函数 $k(\mathbf{x}_n,\mathbf{x}_m)=\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)$ 表达这一结果。为此，在两边乘以 $\boldsymbol{\phi}(\mathbf{x}_l)^{\mathrm{T}}$，得到

$$
\frac{1}{N}\sum_{n=1}^N k(\mathbf{x}_l,\mathbf{x}_n)\sum_{m=1}^{m}a_{im}k(\mathbf{x}_n,\mathbf{x}_m)=\lambda_i\sum_{n=1}^N a_{in}k(\mathbf{x}_l,\mathbf{x}_n).
\tag{12.78}
$$

写成矩阵形式为

$$
\mathbf{K}^2\mathbf{a}_i=\lambda_i N\mathbf{K}\mathbf{a}_i
\tag{12.79}
$$

其中，$\mathbf{a}_i$ 是一个 $N$ 维列向量，其元素为 $a_{ni}$，$n=1,\ldots,N$。通过求解下面的特征值问题，就可以找到 $\mathbf{a}_i$ 的解：

$$
\mathbf{K}\mathbf{a}_i=\lambda_i N\mathbf{a}_i
\tag{12.80}
$$

这里从（12.79）两边各消去了一个因子 $\mathbf{K}$。注意，（12.79）与（12.80）的解，只在 $\mathbf{K}$ 的零特征值所对应的特征向量上存在差异，而这些特征向量不会影响主成分投影（习题 12.26）。

系数 $\mathbf{a}_i$ 的归一化条件，通过要求特征空间中的特征向量归一化来得到。利用（12.76）和（12.80），有

$$
1=\mathbf{v}_i^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N\sum_{m=1}^N a_{in}a_{im}\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)=\mathbf{a}_i^{\mathrm{T}}\mathbf{K}\mathbf{a}_i=\lambda_i N\mathbf{a}_i^{\mathrm{T}}\mathbf{a}_i.
\tag{12.81}
$$

求解特征向量问题后，所得的主成分投影也可以用核函数表达。利用（12.76），点 $\mathbf{x}$ 在第 $i$ 个特征向量上的投影为

$$
y_i(\mathbf{x})=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N a_{in}\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)=\sum_{n=1}^N a_{in}k(\mathbf{x},\mathbf{x}_n)
\tag{12.82}
$$

因此，它同样由核函数表达。

在原来的 $D$ 维 $\mathbf{x}$ 空间中，有 $D$ 个正交特征向量，因此最多只能找到 $D$ 个线性主成分。不过，特征空间的维数 $M$ 可以远大于 $D$（甚至为无穷），所以非线性主成分的数量可以超过 $D$。但要注意，非零特征值的数量不能超过数据点的数量 $N$，因为即使 $M>N$，特征空间中的协方差矩阵的秩也至多为 $N$。这一点也体现在，核 PCA 所涉及的是 $N\times N$ 矩阵 $\mathbf{K}$ 的特征向量展开。

<!-- pdf-page: 609 -->

到目前为止，我们假设由 $\boldsymbol{\phi}(\mathbf{x}_n)$ 给出的投影数据集具有零均值，但一般并非如此。由于希望避免直接在特征空间中运算，不能简单地计算均值并将它减去。因此，再次完全用核函数来表述算法。中心化后的投影数据点记为 $\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)$，由下式给出：

$$
\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)=\boldsymbol{\phi}(\mathbf{x}_n)-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_l)
\tag{12.83}
$$

相应的 Gram 矩阵元素为

$$
\begin{aligned}
\widetilde{K}_{nm}&=\widetilde{\boldsymbol{\phi}}(\mathbf{x}_n)^{\mathrm{T}}\widetilde{\boldsymbol{\phi}}(\mathbf{x}_m)\\
&=\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_n)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_l)\\
&\quad-\frac{1}{N}\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_l)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_m)+\frac{1}{N^2}\sum_{j=1}^N\sum_{l=1}^N\boldsymbol{\phi}(\mathbf{x}_j)^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_l)\\
&=k(\mathbf{x}_n,\mathbf{x}_m)-\frac{1}{N}\sum_{l=1}^N k(\mathbf{x}_l,\mathbf{x}_m)\\
&\quad-\frac{1}{N}\sum_{l=1}^N k(\mathbf{x}_n,\mathbf{x}_l)+\frac{1}{N^2}\sum_{j=1}^N\sum_{l=1}^N k(\mathbf{x}_j,\mathbf{x}_l).
\end{aligned}
\tag{12.84}
$$

写成矩阵形式为

$$
\widetilde{\mathbf{K}}=\mathbf{K}-\mathbf{1}_N\mathbf{K}-\mathbf{K}\mathbf{1}_N+\mathbf{1}_N\mathbf{K}\mathbf{1}_N
\tag{12.85}
$$

其中，$\mathbf{1}_N$ 表示每个元素都等于 $1/N$ 的 $N\times N$ 矩阵。因此，仅利用核函数就能计算 $\widetilde{\mathbf{K}}$，再用 $\widetilde{\mathbf{K}}$ 确定特征值和特征向量。注意，如果使用线性核 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$，就会恢复标准 PCA 算法这一特殊情形（习题 12.27）。图 12.17 给出了将核 PCA 应用于合成数据集的示例（Schölkopf et al.，1998）。这里，将如下形式的“高斯”核

$$
k(\mathbf{x},\mathbf{x}')=\exp(-\|\mathbf{x}-\mathbf{x}'\|^2/0.1)
\tag{12.86}
$$

应用于合成数据集。图中的线是等高线，沿这些线，在相应主成分上的投影保持不变；这一投影定义为

$$
\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\mathbf{v}_i=\sum_{n=1}^N a_{in}k(\mathbf{x},\mathbf{x}_n).
\tag{12.87}
$$

<!-- pdf-page: 610 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-17.png" alt="高斯核 PCA 的八个特征函数与特征值，按两行四列展示三个红色点簇及投影等高线"><figcaption>图 12.17：核 PCA 的示例，将高斯核应用于二维合成数据集，展示前八个特征函数及其特征值。等高线表示在相应主成分上的投影保持不变的线。注意，前两个特征向量将三个簇分开；接下来的三个特征向量把各个簇分为两半；再接下来的三个特征向量，则沿与前面划分正交的方向，再次将各簇分为两半。</figcaption><p class="figure-translation">Eigenvalue → 特征值。上排从左到右：21.72、21.65、4.11、3.93；下排从左到右：3.66、3.09、2.60、2.53。红色圆点表示数据，曲线表示相应主成分投影的等高线。</p></figure>

核 PCA 的一个明显缺点，是需要求 $N\times N$ 矩阵 $\widetilde{\mathbf{K}}$ 的特征向量，而不是传统线性 PCA 中 $D\times D$ 矩阵 $\mathbf{S}$ 的特征向量。因此，在实际处理大型数据集时，往往使用近似方法。

最后注意，在标准线性 PCA 中，常常只保留较少的 $L<D$ 个特征向量，然后用数据向量 $\mathbf{x}_n$ 在 $L$ 维主子空间上的投影 $\widehat{\mathbf{x}}_n$ 来近似它，这个投影定义为

$$
\widehat{\mathbf{x}}_n=\sum_{i=1}^L(\mathbf{x}_n^{\mathrm{T}}\mathbf{u}_i)\mathbf{u}_i.
\tag{12.88}
$$

在核 PCA 中，一般无法这样做。要理解这一点，注意映射 $\boldsymbol{\phi}(\mathbf{x})$ 将 $D$ 维 $\mathbf{x}$ 空间，映射为 $M$ 维特征空间 $\boldsymbol{\phi}$ 中的一个 $D$ 维 *流形*。向量 $\mathbf{x}$ 称为对应点 $\boldsymbol{\phi}(\mathbf{x})$ 的 *原像*（pre-image）。不过，将特征空间中的点投影到该空间的线性 PCA 子空间后，所得点通常不会落在这个非线性的 $D$ 维流形上，因此在数据空间中没有对应的原像。为此，人们提出了寻找近似原像的方法（Bakir et al.，2004）。

<!-- pdf-page: 611 -->

## 12.4 非线性潜变量模型

本章主要讨论了具有连续潜变量的最简单的一类模型，即基于线性高斯分布的模型。除了具有重要的实际用途，这些模型也相对容易分析、容易拟合数据，还可以作为更复杂模型的组成部分。这里简要考虑这个框架的一些推广，它们是非线性模型、非高斯模型，或同时具有这两种性质的模型。

事实上，非线性与非高斯性是相关的：通过非线性的变量变换，可以从一个简单而固定的参考密度（例如高斯密度）得到一般的概率密度（习题 12.28）。稍后会看到，这个思想是若干实用潜变量模型的基础。

### 12.4.1 独立成分分析

首先考虑这样一类模型：观测变量与潜变量之间是线性关系，但潜变量分布是非高斯的。其中重要的一类称为 *独立成分分析*（independent component analysis，ICA）；当潜变量上的分布可以因子化时，就得到这类模型，即

$$
p(\mathbf{z})=\prod_{j=1}^M p(z_j).
\tag{12.89}
$$

为了理解这类模型的作用，考虑两个人同时说话，并用两个麦克风录下他们声音的情形。如果忽略时间延迟和回声等影响，那么在任意时刻，各麦克风接收到的信号，都是两个人声音振幅的线性组合。这个线性组合的系数是常数；如果能从样本数据推断出这些系数，就可以逆转混合过程（假定它是非奇异的），从而得到两个干净的信号，每个信号只包含一个人的声音。这是一类称为 *盲源分离*（blind source separation）的问题的例子，其中“盲”是指只有混合后的数据，既观测不到原始信号源，也观测不到混合系数（Cardoso，1998）。

有时可以用下面的方法处理这类问题（MacKay，2003）：忽略信号的时间性质，将相继样本视为独立同分布。考虑一个生成式模型，其中有两个潜变量，对应于未观测到的语音信号振幅；有两个观测变量，对应于两个麦克风处的信号值。潜变量的联合分布如上所示进行因子化，观测变量则由潜变量的线性组合给出。不需要引入噪声分布，因为潜变量的数量等于观测变量的数量，观测变量的边缘分布一般不会是奇异的。因此，观测变量就是潜变量的确定性线性组合。给定一个观测数据集，

<!-- pdf-page: 612 -->
<!-- join-previous-paragraph -->
这个模型的似然函数就是线性组合系数的函数。使用基于梯度的优化方法最大化对数似然，就得到独立成分分析的一个具体版本。

这种方法要取得成功，要求潜变量具有非高斯分布。要理解这一点，回顾概率 PCA（以及因子分析）中，潜空间的分布是零均值、各向同性高斯分布。因此，如果两种潜变量选择仅相差潜空间中的一次旋转，模型就无法区分它们。可以直接验证这一点：进行变换 $\mathbf{W}\to\mathbf{W}\mathbf{R}$，其中 $\mathbf{R}$ 是满足 $\mathbf{R}\mathbf{R}^{\mathrm{T}}=\mathbf{I}$ 的正交矩阵，边缘密度（12.35）以及似然函数都保持不变，因为（12.36）给出的矩阵 $\mathbf{C}$ 本身就是不变的。将模型推广为允许更一般的高斯潜变量分布，并不会改变这一结论，因为前面已经看到，这样的模型与零均值、各向同性的高斯潜变量模型等价。

还可以从另一个角度理解，为什么线性模型中的高斯潜变量分布不足以找到独立成分：主成分对应于数据空间中坐标系的一次旋转，使协方差矩阵对角化，从而使数据分布在新坐标下不相关。零相关虽然是独立性的必要条件，却不是充分条件（习题 12.29）。在实践中，潜变量分布的一种常见选择是

$$
p(z_j)=\frac{1}{\pi\cosh(z_j)}=\frac{1}{\pi(e^{z_j}+e^{-z_j})}
\tag{12.90}
$$

它比高斯分布具有更重的尾部，反映了许多现实世界中的分布也具有这一性质的观察结果。

最初的 ICA 模型（Bell and Sejnowski，1995），基于对一个由信息最大化定义的目标函数进行优化。概率潜变量表述的一个优点，是有助于提出并构建基本 ICA 的推广。例如，*独立因子分析*（independent factor analysis）（Attias，1999a）考虑这样一种模型：潜变量和观测变量的数量可以不同，观测变量包含噪声，各个潜变量的分布由高斯混合建模，因而具有较大的灵活性。这个模型的对数似然使用 EM 最大化，潜变量的重建则用变分方法近似。人们还研究了许多其他类型的模型，目前已经有大量关于 ICA 及其应用的文献（Jutten and Herault，1991；Comon et al.，1991；Amari et al.，1996；Pearlmutter and Parra，1997；Hyvärinen and Oja，1997；Hinton et al.，2001；Miskin and MacKay，2001；Hojen-Sorensen et al.，2002；Choudrey and Roberts，2003；Chan et al.，2003；Stone，2004）。

### 12.4.2 自联想神经网络

第 5 章在监督学习的背景下讨论了神经网络，网络的作用是根据

<!-- pdf-page: 613 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-18.png" alt="具有输入层、较窄隐藏层和输出层的自联想多层感知机"><figcaption>图 12.18：具有两层权重的自联想多层感知机。通过最小化平方和误差，训练这样的网络将输入向量映射到自身。即使隐藏层使用非线性单元，这样的网络仍然等价于线性主成分分析。为清晰起见，图中省略了表示偏置参数的连线。</figcaption><p class="figure-translation">inputs → 输入；outputs → 输出。$x_1,\ldots,x_D$：输入和输出变量；$z_1,\ldots,z_M$：隐藏单元；上方箭头表示从输入到输出的映射方向。</p></figure>

<!-- join-previous-paragraph-across-figures -->
给定的输入变量值，预测输出变量。不过，神经网络也被应用于无监督学习，用来进行降维。实现方式是使用一个输出数量与输入数量相同的网络，并对一组训练数据优化权重，使输入与输出之间的某种重建误差度量最小。

首先考虑图 12.18 所示的多层感知机，它具有 $D$ 个输入、$D$ 个输出单元和 $M$ 个隐藏单元，其中 $M<D$。用于训练网络的目标就是输入向量本身，因此网络试图将每个输入向量映射到自身。这种网络形成的映射称为 *自联想*（autoassociative）映射。由于隐藏单元的数量少于输入的数量，一般不可能完美重建所有输入向量。因此，通过最小化一个误差函数，来确定网络参数 $\mathbf{w}$；这个函数衡量输入向量与重建结果之间的不匹配程度。具体而言，选择如下形式的平方和误差：

$$
E(\mathbf{w})=\frac{1}{2}\sum_{n=1}^N\|\mathbf{y}(\mathbf{x}_n,\mathbf{w})-\mathbf{x}_n\|^2.
\tag{12.91}
$$

如果隐藏单元的激活函数是线性的，可以证明，误差函数具有唯一的全局最小值，并且在这个最小值处，网络将输入投影到由数据的前 $M$ 个主成分张成的 $M$ 维子空间上（Bourlard and Kamp，1988；Baldi and Hornik，1989）。因此，图 12.18 中通向各隐藏单元的权重向量，构成一组张成主子空间的基。不过要注意，这些向量不必正交，也不必归一化。这个结果并不令人意外，因为主成分分析和该神经网络都在进行线性降维，并最小化同一个平方和误差函数。

人们可能认为，在图 12.18 的网络中，为隐藏单元使用非线性的 sigmoid 激活函数，就能克服线性降维的限制。不过，即使隐藏单元是非线性的，最小误差解仍然是向主成分子空间的投影（Bourlard and Kamp，1988）。因此，用两层神经网络进行降维并没有优势。主成分分析的标准方法（基于奇异值分解）保证能在有限时间内得到正确解，还能生成一组按顺序排列的特征值及相应的标准正交特征向量。

<!-- pdf-page: 614 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-19.png" alt="增加两层非线性隐藏单元的自联想网络，显示从输入到低维中间层的 F1 与从中间层到输出的 F2"><figcaption>图 12.19：增加由非线性单元构成的隐藏层，就得到能够进行非线性降维的自联想网络。</figcaption><p class="figure-translation">inputs → 输入；outputs → 输出；non-linear → 非线性。$x_1,\ldots,x_D$：输入和输出变量；$\mathbf{F}_1$、$\mathbf{F}_2$：网络前半部分和后半部分的映射。两支向上箭头指出具有非线性单元的隐藏层。</p></figure>

不过，如果允许网络增加隐藏层，情况就不同了。考虑图 12.19 所示的四层自联想网络。输出单元仍然是线性的，第二隐藏层中的 $M$ 个单元也可以是线性的，但第一和第三隐藏层使用非线性的 sigmoid 激活函数。网络仍通过最小化误差函数（12.91）来训练。可以将这个网络看成两个依次进行的函数映射 $\mathbf{F}_1$ 和 $\mathbf{F}_2$，如图 12.19 所示。第一个映射 $\mathbf{F}_1$ 将原始的 $D$ 维数据投影到一个 $M$ 维子空间 $\mathcal{S}$，该子空间由第二隐藏层各单元的激活值定义。由于第一隐藏层包含非线性单元，这个映射十分一般，尤其不局限于线性映射。类似地，网络的后半部分定义了一个任意的函数映射，将 $M$ 维空间映射回原来的 $D$ 维输入空间。这有一个简单的几何解释，图 12.20 展示了 $D=3$、$M=2$ 时的情形。

这样的网络实际上进行了非线性主成分分析。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-20.png" alt="三维数据经 F1 映射到二维空间 S，再经 F2 映射为原三维空间中的非平面曲面"><figcaption>图 12.20：当输入数 $D=3$、中间隐藏层单元数 $M=2$ 时，图 12.19 的网络所实现映射的几何解释。函数 $\mathbf{F}_2$ 从 $M$ 维空间 $\mathcal{S}$ 映射到 $D$ 维空间，因此定义了空间 $\mathcal{S}$ 嵌入原始 $\mathbf{x}$ 空间的方式。由于映射 $\mathbf{F}_2$ 可以是非线性的，$\mathcal{S}$ 的嵌入也可以不是平面，如图所示。映射 $\mathbf{F}_1$ 则定义了从原始 $D$ 维空间中的点到 $M$ 维子空间 $\mathcal{S}$ 的投影。</figcaption><p class="figure-translation">$x_1,x_2,x_3$：原数据空间的坐标；$z_1,z_2$：中间空间的坐标；$\mathcal{S}$：二维中间空间；$\mathbf{F}_1$：到中间空间的映射；$\mathbf{F}_2$：回到原数据空间的映射。</p></figure>

<!-- pdf-page: 615 -->
<!-- join-previous-paragraph-across-figures -->
它的优点是不局限于线性变换，同时又包含标准主成分分析这一特殊情形。不过，训练网络现在涉及一个非线性优化问题，因为误差函数（12.91）不再是网络参数的二次函数。必须使用计算量较大的非线性优化方法，并且可能找到误差函数的一个次优局部最小值。此外，必须在训练网络之前指定子空间的维数。

### 12.4.3 非线性流形建模

前面已经指出，许多自然数据源对应于嵌入较高维观测数据空间中的低维非线性流形，并且可能带有噪声。与更一般的方法相比，显式地刻画这一性质，可以改进密度建模。这里简要介绍一些尝试实现这一目标的技术。

建模非线性结构的一种方式，是组合多个线性模型，从而对流形作分段线性近似。例如，可以使用基于欧氏距离的 K 均值等聚类技术，将数据集划分为若干局部组，再对每一组应用标准 PCA。更好的方法是使用重建误差来决定簇归属（Kambhatla and Leen，1997；Hinton et al.，1997），因为这样每个阶段都在优化同一个代价函数。不过，由于缺乏整体的密度模型，这些方法仍然存在局限。使用概率 PCA 时，只要考虑一个各分量都是概率 PCA 模型的混合分布，就能直接定义一个完全概率化的模型（Tipping and Bishop，1999a）。这样的模型既有对应于离散混合的离散潜变量，也有连续潜变量，并且可以使用 EM 算法最大化似然函数。基于变分推断的完全贝叶斯处理（Bishop and Winn，2000），能够从数据推断混合分量的数量，以及各个模型的有效维数。这个模型还有许多变体，例如让不同混合分量共享 $\mathbf{W}$ 矩阵或噪声方差等参数，或者将各向同性噪声分布替换为对角协方差的分布，从而得到因子分析器的混合（Ghahramani and Hinton，1996a；Ghahramani and Beal，2000）。还可以对概率 PCA 混合模型进行层次扩展，得到一种交互式数据可视化算法（Bishop and Tipping，1998）。

除了考虑线性模型的混合，也可以考虑单个非线性模型。回顾传统 PCA，它寻找一个在最小二乘意义下接近数据的线性子空间。这个概念可以通过 *主曲线*（principal curves）的形式，推广到一维非线性曲面（Hastie and Stuetzle，1989）。可以用向量值函数 $\mathbf{f}(\lambda)$，描述 $D$ 维数据空间中的一条曲线；这个向量的每个元素都是标量 $\lambda$ 的函数。曲线有许多可能的参数化方式，其中一个自然的选择是沿曲线的弧长。对于数据空间中任意给定的点 $\widehat{\mathbf{x}}$，可以找到曲线上与它的欧氏距离最近的点。将这个点记为

<!-- pdf-page: 616 -->
<!-- join-previous-paragraph -->
$\lambda=g_{\mathbf{f}}(\mathbf{x})$，因为它依赖于具体的曲线 $\mathbf{f}(\lambda)$。对于连续的数据密度 $p(\mathbf{x})$，主曲线定义为满足如下性质的曲线：曲线上的每一个点，都是数据空间中所有投影到该点的数据点的均值，即

$$
\mathbb{E}[\mathbf{x}\mid g_{\mathbf{f}}(\mathbf{x})=\lambda]=\mathbf{f}(\lambda).
\tag{12.92}
$$

对于给定的连续密度，可以存在多条主曲线。在实践中，我们关心的是有限数据集，并且也希望将注意力限制在光滑曲线上。Hastie and Stuetzle（1989）提出了一个寻找这类主曲线的两阶段迭代过程，有些类似于 PCA 的 EM 算法。先用第一主成分初始化曲线，然后交替执行数据投影步骤和曲线重估步骤。在投影步骤中，将每个数据点分配到一个 $\lambda$ 值，它对应于曲线上最近的点。随后在重估步骤中，曲线上的每个点由一个加权平均给出：对投影到曲线上邻近位置的数据点进行加权，其中在曲线上距离最近的点具有最大权重。当子空间被限制为线性时，这个过程收敛到第一主成分，并等价于求协方差矩阵最大特征值所对应特征向量的幂法。主曲线可以推广为称作 *主曲面*（principal surfaces）的多维流形，但由于高维数据平滑很困难，即使对二维流形也是如此，这种推广的应用一直有限。

PCA 经常用于将数据集投影到低维空间（例如二维空间），以实现可视化。另一种具有类似目标的线性技术是 *多维尺度分析*（multidimensional scaling，MDS）（Cox and Cox，2000）。它寻找数据的低维投影，使数据点之间的两两距离尽可能保持不变，这涉及求距离矩阵的特征向量。当使用欧氏距离时，它得到的结果与 PCA 等价。MDS 的概念可以推广到以相似度矩阵指定的多种数据类型，从而得到非度量 MDS。

另有两种用于降维和数据可视化的非概率方法值得介绍。*局部线性嵌入*（locally linear embedding，LLE）（Roweis and Saul，2000）首先计算一组系数，使每个数据点都能最好地由其邻居重建。这些系数被设定为对该数据点及其邻居的旋转、平移和缩放不变，因此刻画了邻域的局部几何性质。随后，LLE 在保持这些邻域系数不变的条件下，将高维数据点映射到低维空间。如果某个数据点的局部邻域可以视为线性，就可以通过平移、旋转和缩放的组合来实现这一变换，保持数据点与其邻居形成的夹角不变。由于权重对这些变换不变，我们期望同样的权重值，能够像在高维数据空间中一样，在低维空间中重建数据点。尽管这是非线性方法，LLE 的优化过程并不存在局部最小值。

在 *等距特征映射*（isometric feature mapping，isomap）（Tenenbaum et al.，2000）中，目标是使用 MDS 将数据投影到低维空间，但这里的不相似度，是由沿流形

<!-- pdf-page: 617 -->
<!-- join-previous-paragraph -->
测得的测地距离定义的。例如，如果两个点位于一个圆上，那么测地距离是沿圆周测得的弧长，而不是沿连接两点的弦测得的直线距离。算法首先为每个数据点定义邻域，可以寻找 $K$ 个最近邻，也可以寻找半径为 $\epsilon$ 的球内的所有点。然后通过连接所有相邻点来构造一个图，并用欧氏距离标记这些连接。任意一对点之间的测地距离，就由连接它们的最短路径上各弧段长度之和近似（最短路径本身用标准算法求得）。最后，将度量 MDS 应用于测地距离矩阵，得到低维投影。

本章主要关注观测变量为连续变量的模型。也可以考虑连续潜变量与离散观测变量相结合的模型，从而得到 *潜在特质模型*（latent trait models）（Bartholomew，1987）。在这种情况下，即使潜变量与观测变量之间是线性关系，也无法解析地对连续潜变量进行边缘化，因此需要更复杂的技术。Tipping（1999）在一个具有二维潜空间的模型中使用变分推断，使二元数据集能够像使用 PCA 可视化连续数据那样进行可视化。注意，这个模型是第 4.5 节讨论的贝叶斯逻辑回归问题的对偶。在逻辑回归中，特征向量 $\boldsymbol{\phi}_n$ 有 $N$ 个观测，它们由单个参数向量 $\mathbf{w}$ 参数化；而在潜空间可视化模型中，只有一个潜空间变量 $\mathbf{x}$（对应于 $\boldsymbol{\phi}$），以及潜变量的 $N$ 个副本 $\mathbf{w}_n$。Collins et al.（2002）介绍了将概率潜变量模型推广到一般指数族分布的方法。

前面已经指出，对高斯随机变量施加适当的非线性变换，可以构造任意分布。一个称为 *密度网络*（density network）的通用潜变量模型（MacKay，1995；MacKay and Gibbs，1999）利用了这一点，其中非线性函数由多层神经网络控制。如果网络具有足够多的隐藏单元，就能以任意要求的精度近似给定的非线性函数（第 5 章）。这种灵活模型的代价是，为得到似然函数而必须进行的潜变量边缘化，不再能解析求解。于是，改用蒙特卡洛技术，从高斯先验中抽取样本来近似似然（第 11 章）。对潜变量的边缘化就变成了一个简单求和，每个样本对应其中一项。不过，为了准确表示边缘分布，可能需要大量采样点，因此这一过程的计算成本可能很高。

如果对非线性函数的形式加以限制，并适当选择潜变量分布，就可以构造一种既非线性又能高效训练的潜变量模型。*生成拓扑映射*（generative topographic mapping，GTM）（Bishop et al.，1996；Bishop et al.，1997a；Bishop et al.，1998b）所用的潜变量分布，由潜空间（通常是二维空间）中规则排列的有限个 $\delta$ 函数网格定义。这样，对潜空间的边缘化只需将各个网格位置的贡献相加。

<!-- pdf-page: 618 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-12/b-fig-12-21.png" alt="油流数据的 PCA 与 GTM 二维可视化，左侧点簇重叠较多，右侧各组更清楚地分开"><figcaption>图 12.21：油流数据集的可视化，左图使用 PCA，右图使用 GTM。对于 GTM 模型，每个数据点画在其潜空间后验分布的均值位置。GTM 模型的非线性，使各组数据点之间的分离更加清楚。</figcaption><p class="figure-translation">左图：PCA；右图：GTM。红色叉号、蓝色加号和绿色圆圈表示数据的三个类别。</p></figure>

非线性映射由一个线性回归模型给出，它允许一般的非线性，同时仍是可调参数的线性函数（第 3 章）。注意，线性回归模型通常受到维数灾难的限制（第 1.4 节），但这个限制不会在 GTM 中出现，因为无论数据空间的维数是多少，流形通常只有二维。这两个选择带来的结果是，似然函数可以解析地写成闭式，并使用 EM 算法高效优化。所得 GTM 模型为数据集拟合一个二维非线性流形；通过计算各数据点在潜空间上的后验分布，就可以将它们投影回潜空间，以实现可视化。图 12.21 比较了使用线性 PCA 与非线性 GTM 对油流数据集进行可视化的结果。

GTM 可以看作更早的一种模型——*自组织映射*（self organizing map，SOM）（Kohonen，1982；Kohonen，1995）——的概率版本。SOM 也用规则排列的离散点表示二维非线性流形。它有些类似于 K 均值算法：先将数据点分配给附近的原型向量，再更新这些原型。最初，原型随机分布；训练过程中，它们“自组织”起来，以近似一个光滑流形。不过，与 K 均值不同，SOM 并不优化任何定义明确的代价函数（Erwin et al.，1992），因此难以设置模型参数和判断收敛。此外，也不能保证一定会发生“自组织”，因为这取决于是否为具体数据集选择了合适的参数值。

相比之下，GTM 优化的是对数似然函数，所得模型在数据空间中定义了一个概率密度。事实上，它对应于一个受约束的高斯混合模型：所有分量共享同一个方差，均值则被限制在一个光滑的二维流形上。这种概率

<!-- pdf-page: 619 -->
<!-- join-previous-paragraph -->
基础也使 GTM 的推广十分直接（Bishop et al.，1998a），例如贝叶斯处理、缺失值处理、依据明确原理推广到离散变量、使用高斯过程定义流形（第 6.4 节），或者构造层次 GTM 模型（Tino and Nabney，2002）。

由于 GTM 中的流形被定义为一个连续曲面，而不像 SOM 那样只在原型向量处定义，因此可以计算 *放大因子*（magnification factors），它对应于为拟合数据集所需的流形局部伸展和压缩（Bishop et al.，1997b）；还可以计算流形的 *方向曲率*（directional curvatures）（Tino et al.，2001）。将这些量与投影后的数据一起可视化，可以更深入地了解模型。

## 习题

**12.1（⋆⋆）www** 本题使用数学归纳法证明：使投影数据方差最大的、到 $M$ 维子空间的线性投影，由数据协方差矩阵 $\mathbf{S}$ 的最大 $M$ 个特征值所对应的 $M$ 个特征向量定义，其中 $\mathbf{S}$ 由（12.3）给出。第 12.1 节已经证明了 $M=1$ 时的结果。现在假设这一结果对某个一般的 $M$ 值成立，证明它因此也对维数 $M+1$ 成立。为此，首先令投影数据的方差关于向量 $\mathbf{u}_{M+1}$ 的导数为零，这个向量定义数据空间中的新方向。同时要求 $\mathbf{u}_{M+1}$ 与已有向量 $\mathbf{u}_1,\ldots,\mathbf{u}_M$ 正交，并归一化为单位长度。使用拉格朗日乘子施加这些约束（附录 E）。然后，利用向量 $\mathbf{u}_1,\ldots,\mathbf{u}_M$ 的标准正交性质，证明新向量 $\mathbf{u}_{M+1}$ 是 $\mathbf{S}$ 的特征向量。最后，证明当选择与特征向量 $\lambda_{M+1}$ 对应的那个特征向量时，方差达到最大；这里特征值已按从大到小排列。

**12.2（⋆⋆）** 证明，在标准正交约束（12.7）下，关于 $\mathbf{u}_i$ 最小化（12.15）给出的 PCA 畸变度量 $J$，会在 $\mathbf{u}_i$ 是数据协方差矩阵 $\mathbf{S}$ 的特征向量时取得最小值。为此，引入一个拉格朗日乘子矩阵 $\mathbf{H}$，每个约束对应一个乘子，使修改后的畸变度量写成如下矩阵形式：

$$
\widetilde{J}=\operatorname{Tr}\left\{\widehat{\mathbf{U}}^{\mathrm{T}}\mathbf{S}\widehat{\mathbf{U}}\right\}+\operatorname{Tr}\left\{\mathbf{H}(\mathbf{I}-\widehat{\mathbf{U}}^{\mathrm{T}}\widehat{\mathbf{U}})\right\}
\tag{12.93}
$$

其中，$\widehat{\mathbf{U}}$ 是一个 $D\times(D-M)$ 矩阵，其各列由 $\mathbf{u}_i$ 给出。现在关于 $\widehat{\mathbf{U}}$ 最小化 $\widetilde{J}$，证明解满足 $\mathbf{S}\widehat{\mathbf{U}}=\widehat{\mathbf{U}}\mathbf{H}$。显然，一个可能的解是 $\widehat{\mathbf{U}}$ 的各列为 $\mathbf{S}$ 的特征向量，此时 $\mathbf{H}$ 是包含相应特征值的对角矩阵。为了得到一般解，证明可以假设 $\mathbf{H}$ 是对称矩阵，并利用它的特征向量展开，证明 $\mathbf{S}\widehat{\mathbf{U}}=\widehat{\mathbf{U}}\mathbf{H}$ 的一般解给出的 $\widetilde{J}$ 值，与 $\widehat{\mathbf{U}}$ 的各列为

<!-- pdf-page: 620 -->
<!-- join-previous-paragraph -->
$\mathbf{S}$ 的特征向量时的特殊解相同。由于这些解全部等价，选择特征向量解会比较方便。

**12.3（⋆）** 假设特征向量 $\mathbf{v}_i$ 的长度为一，验证（12.30）定义的特征向量也归一化为单位长度。

**12.4（⋆）www** 假设将概率 PCA 模型中零均值、单位协方差的潜空间分布（12.31），替换为形式为 $\mathcal{N}(\mathbf{z}\mid\mathbf{m},\boldsymbol{\Sigma})$ 的一般高斯分布。通过重新定义模型参数，证明对于任意有效的 $\mathbf{m}$ 和 $\boldsymbol{\Sigma}$ 选择，这都会使观测变量的边缘分布 $p(\mathbf{x})$ 得到相同的模型。

**12.5（⋆⋆）** 设 $\mathbf{x}$ 是一个 $D$ 维随机变量，服从高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$。考虑 $M$ 维随机变量 $\mathbf{y}=\mathbf{A}\mathbf{x}+\mathbf{b}$，其中 $\mathbf{A}$ 是 $M\times D$ 矩阵。证明 $\mathbf{y}$ 也服从高斯分布，并求其均值和协方差的表达式。分别讨论 $M<D$、$M=D$ 和 $M>D$ 时这个高斯分布的形式。

**12.6（⋆）www** 为第 12.2 节描述的概率 PCA 模型画出有向概率图，将观测变量 $\mathbf{x}$ 的各分量明确地分别表示为不同节点。由此验证，概率 PCA 模型具有与第 8.2.2 节讨论的朴素贝叶斯模型相同的独立性结构。

**12.7（⋆⋆）** 利用一般分布的均值和协方差结果（2.270）和（2.271），推导概率 PCA 模型中边缘分布 $p(\mathbf{x})$ 的结果（12.35）。

**12.8（⋆⋆）www** 利用结果（2.116），证明概率 PCA 模型的后验分布 $p(\mathbf{z}\mid\mathbf{x})$ 由（12.42）给出。

**12.9（⋆）** 验证，对于概率 PCA 模型，关于参数 $\boldsymbol{\mu}$ 最大化对数似然（12.43），会得到 $\boldsymbol{\mu}_{\mathrm{ML}}=\overline{\mathbf{x}}$，其中 $\overline{\mathbf{x}}$ 是数据向量的均值。

**12.10（⋆⋆）** 通过计算概率 PCA 模型的对数似然函数（12.43）关于参数 $\boldsymbol{\mu}$ 的二阶导数，证明驻点 $\boldsymbol{\mu}_{\mathrm{ML}}=\overline{\mathbf{x}}$ 是唯一的最大值点。

**12.11（⋆⋆）www** 证明，当 $\sigma^2\to0$ 时，概率 PCA 模型的后验均值变成到主子空间的正交投影，与传统 PCA 一样。

**12.12（⋆⋆）** 对于 $\sigma^2>0$，证明相对于正交投影，概率 PCA 模型的后验均值向原点偏移。

**12.13（⋆⋆）** 证明，按照传统 PCA 的最小二乘投影代价，概率 PCA 下对数据点的最优重建为

$$
\widetilde{\mathbf{x}}=\mathbf{W}_{\mathrm{ML}}(\mathbf{W}_{\mathrm{ML}}^{\mathrm{T}}\mathbf{W}_{\mathrm{ML}})^{-1}\mathbf{M}\mathbb{E}[\mathbf{z}\mid\mathbf{x}].
\tag{12.94}
$$

<!-- pdf-page: 621 -->

**12.14（⋆）** 对于具有 $M$ 维潜空间和 $D$ 维数据空间的概率 PCA 模型，协方差矩阵中独立参数的数量由（12.51）给出。验证，当 $M=D-1$ 时，独立参数的数量与一般协方差高斯分布相同；当 $M=0$ 时，则与各向同性协方差的高斯分布相同。

**12.15（⋆⋆）www** 通过最大化（12.53）给出的完整数据对数似然的期望，推导概率 PCA 模型的 M 步方程（12.56）和（12.57）。

**12.16（⋆⋆⋆）** 图 12.11 展示了将概率 PCA 应用于部分数据值随机缺失的数据集。推导在这种情况下最大化概率 PCA 模型似然函数的 EM 算法。注意，现在 $\{\mathbf{z}_n\}$ 以及向量 $\{\mathbf{x}_n\}$ 中缺失的数据分量，都是潜变量。证明，在所有数据值均被观测到的特殊情况下，这一算法退化为第 12.2.2 节推导的概率 PCA 的 EM 算法。

**12.17（⋆⋆）www** 设 $\mathbf{W}$ 是一个 $D\times M$ 矩阵，其各列定义了嵌入 $D$ 维数据空间中的 $M$ 维线性子空间；$\boldsymbol{\mu}$ 是一个 $D$ 维向量。给定数据集 $\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，可以通过一组 $M$ 维向量 $\{\mathbf{z}_n\}$ 的线性映射来近似数据点，即用 $\mathbf{W}\mathbf{z}_n+\boldsymbol{\mu}$ 近似 $\mathbf{x}_n$。相应的平方和重建代价为

$$
J=\sum_{n=1}^N\|\mathbf{x}_n-\boldsymbol{\mu}-\mathbf{W}\mathbf{z}_n\|^2.
\tag{12.95}
$$

首先证明，关于 $\boldsymbol{\mu}$ 最小化 $J$，会得到一个类似的表达式，其中 $\mathbf{x}_n$ 和 $\mathbf{z}_n$ 分别替换为零均值变量 $\mathbf{x}_n-\overline{\mathbf{x}}$ 和 $\mathbf{z}_n-\overline{\mathbf{z}}$，这里 $\overline{\mathbf{x}}$ 和 $\overline{\mathbf{z}}$ 表示样本均值。然后证明，在固定 $\mathbf{W}$ 时，关于 $\mathbf{z}_n$ 最小化 $J$ 会得到 PCA 的 E 步（12.58）；而在固定 $\{\mathbf{z}_n\}$ 时，关于 $\mathbf{W}$ 最小化 $J$ 会得到 PCA 的 M 步（12.59）。

**12.18（⋆）** 推导第 12.2.4 节描述的因子分析模型中，独立参数数量的表达式。

**12.19（⋆⋆）www** 证明，第 12.2.4 节描述的因子分析模型在潜空间坐标的旋转下保持不变。

**12.20（⋆⋆）** 通过考虑二阶导数，证明第 12.2.4 节讨论的因子分析模型的对数似然函数，关于参数 $\boldsymbol{\mu}$ 的唯一驻点，由（12.1）定义的样本均值给出。进一步证明，这个驻点是最大值点。

**12.21（⋆⋆）** 推导因子分析的 EM 算法中 E 步的公式（12.66）和（12.67）。注意，根据习题 12.20 的结果，参数 $\boldsymbol{\mu}$ 可以替换为样本均值 $\overline{\mathbf{x}}$。

<!-- pdf-page: 622 -->

**12.22（⋆⋆）** 写出因子分析模型的完整数据对数似然期望的表达式，并由此推导相应的 M 步方程（12.69）和（12.70）。

**12.23（⋆）www** 画一个有向概率图模型，表示概率 PCA 模型的离散混合，其中每个 PCA 模型都有自己的 $\mathbf{W}$、$\boldsymbol{\mu}$ 和 $\sigma^2$ 值。然后修改这个图，使这些参数值在混合的各分量之间共享。

**12.24（⋆⋆⋆）** 第 2.3.7 节已经看到，Student t 分布可以看作高斯分布的无限混合，其中对一个连续潜变量进行边缘化。利用这一表示，为给定观测数据点集的多元 Student t 分布，构造最大化其对数似然函数的 EM 算法，并推导 E 步和 M 步方程的形式。

**12.25（⋆⋆）www** 考虑一个线性高斯潜变量模型，它的潜空间分布为 $p(\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{0},\mathbf{I})$，观测变量的条件分布为 $p(\mathbf{x}\mid\mathbf{z})=\mathcal{N}(\mathbf{x}\mid\mathbf{W}\mathbf{z}+\boldsymbol{\mu},\boldsymbol{\Phi})$，其中 $\boldsymbol{\Phi}$ 是任意对称正定的噪声协方差矩阵。现在假设对数据变量进行非奇异线性变换 $\mathbf{x}\to\mathbf{A}\mathbf{x}$，其中 $\mathbf{A}$ 是 $D\times D$ 矩阵。如果 $\boldsymbol{\mu}_{\mathrm{ML}}$、$\mathbf{W}_{\mathrm{ML}}$ 和 $\boldsymbol{\Phi}_{\mathrm{ML}}$ 表示对应于原始未变换数据的最大似然解，证明 $\mathbf{A}\boldsymbol{\mu}_{\mathrm{ML}}$、$\mathbf{A}\mathbf{W}_{\mathrm{ML}}$ 和 $\mathbf{A}\boldsymbol{\Phi}_{\mathrm{ML}}\mathbf{A}^{\mathrm{T}}$ 表示对应于变换后数据集的最大似然解。最后，证明在以下两种情况下，模型的形式保持不变：（i）$\mathbf{A}$ 和 $\boldsymbol{\Phi}$ 都是对角矩阵。这对应于因子分析的情形。变换后的 $\boldsymbol{\Phi}$ 仍然是对角矩阵，因此因子分析对数据变量按分量重新缩放具有协变性；（ii）$\mathbf{A}$ 是正交矩阵，$\boldsymbol{\Phi}$ 与单位矩阵成比例，即 $\boldsymbol{\Phi}=\sigma^2\mathbf{I}$。这对应于概率 PCA。变换后的 $\boldsymbol{\Phi}$ 矩阵仍然与单位矩阵成比例，因此与传统 PCA 一样，概率 PCA 对数据空间坐标轴的旋转具有协变性。

**12.26（⋆⋆）** 证明，满足（12.80）的任意向量 $\mathbf{a}_i$ 也满足（12.79）。再证明，对于（12.80）的任意一个特征值为 $\lambda$ 的解，加上 $\mathbf{K}$ 的一个零特征值所对应的特征向量的任意倍数，仍会得到（12.79）的一个特征值为 $\lambda$ 的解。最后，证明这样的修改不会影响（12.82）给出的主成分投影。

**12.27（⋆⋆）** 证明，如果选择线性核函数 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm{T}}\mathbf{x}'$，传统线性 PCA 算法就是核 PCA 的一个特殊情形。

**12.28（⋆⋆）www** 利用概率密度在变量变换下的变换性质（1.27），证明任意密度 $p(y)$ 都可以由一个处处非零的固定密度 $q(x)$，通过非线性变量变换 $y=f(x)$ 得到；其中 $f(x)$ 是单调函数，满足 $0\leqslant f'(x)<\infty$。写出 $f(x)$ 满足的微分方程，并画图说明密度的变换。

<!-- pdf-page: 623 -->

**12.29（⋆⋆）www** 假设两个变量 $z_1$ 和 $z_2$ 相互独立，即 $p(z_1,z_2)=p(z_1)p(z_2)$。证明，这两个变量之间的协方差矩阵是对角矩阵。这说明，独立是两个变量不相关的充分条件。现在考虑两个变量 $y_1$ 和 $y_2$，其中 $-1\leqslant y_1\leqslant1$，且 $y_2=y_2^2$。写出条件分布 $p(y_2\mid y_1)$，并观察到它依赖于 $y_1$，从而说明这两个变量不独立。然后证明，这两个变量之间的协方差矩阵仍然是对角矩阵。为此，利用关系 $p(y_1,y_2)=p(y_1)p(y_2\mid y_1)$，证明非对角项为零。这个反例说明，零相关不是独立性的充分条件。

<!-- pdf-page: 624 -->
