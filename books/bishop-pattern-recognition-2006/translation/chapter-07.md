# 第 7 章 稀疏核机器

<aside class="chapter-guide"><strong>本章导读</strong><p>本章介绍只依赖少量训练数据点进行预测的核模型。先从最大间隔出发推导支持向量机，说明如何处理类别重叠、多类别分类和回归，再介绍相关向量机及其贝叶斯解释，比较两种方法的稀疏性、预测方式与训练过程。</p></aside>

<!-- pdf-page: 345 -->

<figure class="chapter-art"><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-chapter-opening.png" alt="水面纹理上的第 7 章标题"><p class="figure-translation">Sparse Kernel Machines → 稀疏核机器。</p></figure>

上一章中，我们考察了多种基于非线性核的学习算法。许多这类算法有一个显著限制：必须对训练点 $\mathbf{x}_n$ 和 $\mathbf{x}_m$ 的所有可能配对计算核函数 $k(\mathbf{x}_n,\mathbf{x}_m)$。这可能使训练在计算上难以实现，也可能导致新数据点的预测耗时过长。本章将考察具有稀疏解的核算法，使新输入的预测只依赖于在训练数据点的一个子集处求值的核函数。

我们首先较详细地考察支持向量机（support vector machine，SVM）。几年前，它开始广泛用于解决分类、回归和新颖性检测问题。支持向量机的一个重要性质是，确定模型参数对应于一个凸优化问题，因此任何局部解也都是全局最优解。由于支持向量机的讨论会大量使用拉格朗日乘子，建议读者

<!-- pdf-page: 346 -->
<!-- join-previous-paragraph -->
复习附录 E 中介绍的关键概念。关于支持向量机的更多资料，可参见 Vapnik（1995）、Burges（1998）、Cristianini and Shawe-Taylor（2000）、Müller et al.（2001）、Schölkopf and Smola（2002）以及 Herbrich（2002）。

SVM 是一种决策机，因此不提供后验概率。第 1.5.4 节已经讨论过确定概率所带来的一些好处。另一种稀疏核方法称为相关向量机（relevance vector machine，RVM），它建立在贝叶斯表述之上，既能提供后验概率输出，又通常具有比 SVM 稀疏得多的解。<span class="margin-reference">第 7.2 节</span>

## 7.1 最大间隔分类器

我们从使用如下形式线性模型的二分类问题入手，开始讨论支持向量机：

$$
y(\mathbf{x})=\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x})+b
\tag{7.1}
$$

其中 $\boldsymbol{\phi}(\mathbf{x})$ 表示一个固定的特征空间变换，偏置参数 $b$ 已显式写出。注意，我们很快将引入用核函数表示的对偶形式，从而避免显式在特征空间中计算。训练数据集由 $N$ 个输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 及相应的目标值 $t_1,\ldots,t_N$ 组成，其中 $t_n\in\{-1,1\}$；根据 $y(\mathbf{x})$ 的符号，对新数据点 $\mathbf{x}$ 进行分类。

暂时假设训练数据集在特征空间中线性可分。因此，根据定义，至少存在一组参数 $\mathbf{w}$ 和 $b$，使式（7.1）形式的函数满足：对于 $t_n=+1$ 的点，$y(\mathbf{x}_n)>0$；对于 $t_n=-1$ 的点，$y(\mathbf{x}_n)<0$。也就是说，对所有训练数据点都有 $t_ny(\mathbf{x}_n)>0$。

当然，可能存在很多能将类别完全分开的解。在第 4.1.7 节，我们介绍了感知机算法，它保证能在有限步内找到一个解。不过，它找到的解取决于为 $\mathbf{w}$ 和 $b$ 任意选择的初始值，也取决于输入数据点的呈现顺序。如果存在多个都能完全正确分类训练数据集的解，那么应当尝试寻找泛化误差最小的那个解。支持向量机通过间隔（margin）的概念来处理这个问题；间隔定义为决策边界与任意样本之间的最小距离，如图 7.1 所示。

在支持向量机中，选择使间隔最大的决策边界。最大间隔解可以通过计算学习理论，也称为统计学习理论，来说明其依据。<span class="margin-reference">第 7.1.5 节</span>不过，Tong and Koller（2000）对最大间隔的由来给出了一个简单解释。他们考察一种结合生成式与判别式方法的分类框架。首先，对每个类别的输入向量 $\mathbf{x}$ 的分布，使用高斯核的 Parzen 密度估计器进行建模，所有核

<!-- pdf-page: 347 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-1.png" alt="决策边界的间隔及由三个支持向量确定的最大间隔边界"><figcaption>图 7.1：间隔定义为决策边界与最近数据点之间的垂直距离，如左图所示。最大化间隔会得到一个特定的决策边界，如右图所示。该边界的位置由称为支持向量的一部分数据点决定，图中用圆圈标出了这些点。</figcaption><p class="figure-translation">margin → 间隔。</p></figure>

<!-- join-previous-paragraph-across-figures -->
共享参数 $\sigma^2$。结合类别先验，就能定义使误分类率最小的决策边界。不过，他们并不使用这个最优边界，而是相对于学得的密度模型，最小化错误概率，从而确定最佳超平面。可以证明，在 $\sigma^2\to0$ 的极限下，最优超平面就是具有最大间隔的超平面。直观上，随着 $\sigma^2$ 减小，相对于较远的数据点，附近的数据点对超平面的影响越来越大。在极限情况下，超平面不再依赖于不是支持向量的数据点。

在图 10.13 中，我们将看到，对于一个简单的线性可分数据集，贝叶斯方法对参数先验分布进行边缘化，会得到位于数据点分隔区域中间的决策边界。大间隔解具有类似的行为。

回顾图 4.1，若 $y(\mathbf{x})$ 具有式（7.1）的形式，那么点 $\mathbf{x}$ 到由 $y(\mathbf{x})=0$ 定义的超平面的垂直距离为 $|y(\mathbf{x})|/\|\mathbf{w}\|$。此外，我们只关心所有数据点都被正确分类的解，因此对所有 $n$ 都有 $t_ny(\mathbf{x}_n)>0$。于是，点 $\mathbf{x}_n$ 到决策面的距离为

$$
\frac{t_ny(\mathbf{x}_n)}{\|\mathbf{w}\|}=\frac{t_n(\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)+b)}{\|\mathbf{w}\|}.
\tag{7.2}
$$

间隔由数据集中距离决策面最近的点 $\mathbf{x}_n$ 的垂直距离给出，我们希望优化参数 $\mathbf{w}$ 和 $b$，使这个距离最大。因此，通过求解以下问题得到最大间隔解：

$$
\operatorname*{arg\,max}_{\mathbf{w},b}\left\{\frac{1}{\|\mathbf{w}\|}\min_n\left[t_n\left(\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)+b\right)\right]\right\}
\tag{7.3}
$$

其中将因子 $1/\|\mathbf{w}\|$ 移到了对 $n$ 的优化之外，因为 $\mathbf{w}$

<!-- pdf-page: 348 -->
<!-- join-previous-paragraph -->
不依赖于 $n$。直接求解这个优化问题会很复杂，因此我们将它转换为一个容易得多的等价问题。为此，注意到如果进行缩放 $\mathbf{w}\to\kappa\mathbf{w}$ 和 $b\to\kappa b$，任意点 $\mathbf{x}_n$ 到决策面的距离 $t_ny(\mathbf{x}_n)/\|\mathbf{w}\|$ 都保持不变。可以利用这一自由度，对距离决策面最近的点设定

$$
t_n\left(\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)+b\right)=1
\tag{7.4}
$$

此时，所有数据点都会满足约束

$$
t_n\left(\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)+b\right)\geqslant1,\qquad n=1,\ldots,N.
\tag{7.5}
$$

这称为决策超平面的典范表示（canonical representation）。对于等式成立的数据点，相应约束称为起作用的（active）；其余约束则称为不起作用的（inactive）。根据定义，总会至少存在一个起作用的约束，因为总会有一个最近的点；一旦间隔最大化，就会至少存在两个起作用的约束。于是，优化问题只要求最大化 $\|\mathbf{w}\|^{-1}$，这等价于最小化 $\|\mathbf{w}\|^2$。因此，需要求解优化问题

$$
\operatorname*{arg\,min}_{\mathbf{w},b}\frac{1}{2}\|\mathbf{w}\|^2
\tag{7.6}
$$

并满足式（7.5）给出的约束。式（7.6）中的因子 $1/2$ 是为了后面的推导方便而加入的。这是二次规划（quadratic programming）问题的一个例子：在一组线性不等式约束下，最小化一个二次函数。偏置参数 $b$ 似乎从优化中消失了。不过，它仍由约束隐式确定，因为这些约束要求对 $\|\mathbf{w}\|$ 的改变必须由 $b$ 的改变来补偿。稍后将说明具体过程。

为求解这一约束优化问题，我们引入拉格朗日乘子 $a_n\geqslant0$，式（7.5）中的每个约束对应一个乘子 $a_n$，得到拉格朗日函数<span class="margin-reference">附录 E</span>

$$
L(\mathbf{w},b,\mathbf{a})=\frac{1}{2}\|\mathbf{w}\|^2-\sum_{n=1}^{N}a_n\{t_n(\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)+b)-1\}
\tag{7.7}
$$

其中 $\mathbf{a}=(a_1,\ldots,a_N)^{\mathrm{T}}$。注意拉格朗日乘子项前的负号，因为我们对 $\mathbf{w}$ 和 $b$ 作最小化，对 $\mathbf{a}$ 作最大化。令 $L(\mathbf{w},b,\mathbf{a})$ 对 $\mathbf{w}$ 和 $b$ 的导数为零，得到以下两个条件：

$$
\mathbf{w}=\sum_{n=1}^{N}a_nt_n\boldsymbol{\phi}(\mathbf{x}_n)
\tag{7.8}
$$

$$
0=\sum_{n=1}^{N}a_nt_n.
\tag{7.9}
$$

<!-- pdf-page: 349 -->

利用这些条件，从 $L(\mathbf{w},b,\mathbf{a})$ 中消去 $\mathbf{w}$ 和 $b$，就得到最大间隔问题的对偶表示。在该表示中，对 $\mathbf{a}$ 最大化

$$
\widetilde{L}(\mathbf{a})=\sum_{n=1}^{N}a_n-\frac{1}{2}\sum_{n=1}^{N}\sum_{m=1}^{N}a_na_mt_nt_mk(\mathbf{x}_n,\mathbf{x}_m)
\tag{7.10}
$$

并满足约束

$$
a_n\geqslant0,\qquad n=1,\ldots,N,
\tag{7.11}
$$

$$
\sum_{n=1}^{N}a_nt_n=0.
\tag{7.12}
$$

这里，核函数定义为 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}')$。这仍是一个二次规划问题，即在一组不等式约束下优化 $\mathbf{a}$ 的二次函数。第 7.1.1 节将讨论这类二次规划问题的求解方法。

求解一个具有 $M$ 个变量的二次规划问题，其计算复杂度一般为 $O(M^3)$。转到对偶形式后，我们把原来对 $M$ 个变量最小化式（7.6）的优化问题，变成了具有 $N$ 个变量的对偶问题（7.10）。如果固定基函数的数量 $M$ 少于数据点数量 $N$，转到对偶问题似乎不利。不过，这样可以用核来重新表述模型，因此最大间隔分类器能够高效地用于维数超过数据点数量的特征空间，包括无限维特征空间。核形式也明确说明了要求核函数 $k(\mathbf{x},\mathbf{x}')$ 正定这一约束的作用，因为它保证拉格朗日函数 $\widetilde{L}(\mathbf{a})$ 有下界，从而得到一个定义良好的优化问题。

要用训练好的模型对新数据点分类，需要求出式（7.1）定义的 $y(\mathbf{x})$ 的符号。利用式（7.8）代入 $\mathbf{w}$，可以用参数 $\{a_n\}$ 和核函数将其表示为

$$
y(\mathbf{x})=\sum_{n=1}^{N}a_nt_nk(\mathbf{x},\mathbf{x}_n)+b.
\tag{7.13}
$$

<aside class="biography"><p><strong>约瑟夫-路易·拉格朗日（Joseph-Louis Lagrange）</strong><br>1736–1813</p><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-lagrange.png" alt="拉格朗日肖像"><p>虽然拉格朗日通常被认为是法国数学家，但他出生于意大利都灵。十九岁时，他就已经对数学作出了重要贡献，并被任命为都灵皇家炮兵学校的教授。多年来，Euler 一直努力劝说拉格朗日移居柏林，后者终于在 1766 年前往柏林，接替 Euler 担任柏林科学院数学部主任。后来，他移居巴黎。在法国大革命期间，由于发现氧气的法国化学家 Lavoisier 亲自出面干预，他才勉强保住性命；而 Lavoisier 本人后来却被送上了断头台。拉格朗日对变分法和动力学基础作出了关键贡献。</p></aside>

<!-- pdf-page: 350 -->

在附录 E 中，我们说明这种形式的约束优化满足 Karush–Kuhn–Tucker（KKT）条件。在这里，这些条件要求以下三个性质成立：

$$
a_n\geqslant0
\tag{7.14}
$$

$$
t_ny(\mathbf{x}_n)-1\geqslant0
\tag{7.15}
$$

$$
a_n\{t_ny(\mathbf{x}_n)-1\}=0.
\tag{7.16}
$$

因此，对于每个数据点，要么 $a_n=0$，要么 $t_ny(\mathbf{x}_n)=1$。任何满足 $a_n=0$ 的数据点都不会出现在式（7.13）的求和中，因此对新数据点的预测不起作用。其余数据点称为支持向量（support vectors）；由于它们满足 $t_ny(\mathbf{x}_n)=1$，因此对应于特征空间中位于最大间隔超平面上的点，如图 7.1 所示。这一性质是支持向量机能够实用化的核心。模型训练完成后，可以丢弃相当大一部分数据点，只保留支持向量。

求解二次规划问题并得到 $\mathbf{a}$ 后，可以利用任意支持向量 $\mathbf{x}_n$ 都满足 $t_ny(\mathbf{x}_n)=1$ 这一事实，确定阈值参数 $b$。由式（7.13），有

$$
t_n\left(\sum_{m\in\mathcal{S}}a_mt_mk(\mathbf{x}_n,\mathbf{x}_m)+b\right)=1
\tag{7.17}
$$

其中 $\mathcal{S}$ 表示支持向量的下标集合。虽然可以任意选取一个支持向量 $\mathbf{x}_n$，用这个方程求出 $b$，但数值上更稳定的做法是：先将方程两边乘以 $t_n$，利用 $t_n^2=1$，然后对所有支持向量对应的这些方程取平均，再解出 $b$，得到

$$
b=\frac{1}{N_{\mathcal{S}}}\sum_{n\in\mathcal{S}}\left(t_n-\sum_{m\in\mathcal{S}}a_mt_mk(\mathbf{x}_n,\mathbf{x}_m)\right)
\tag{7.18}
$$

其中 $N_{\mathcal{S}}$ 是支持向量的总数。

为了便于后面与其他模型比较，可以把最大间隔分类器表示为最小化一个带简单二次正则化项的误差函数，其形式为

$$
\sum_{n=1}^{N}E_{\infty}(y(\mathbf{x}_n)t_n-1)+\lambda\|\mathbf{w}\|^2
\tag{7.19}
$$

其中函数 $E_{\infty}(z)$ 在 $z\geqslant0$ 时为零，否则为 $\infty$，从而保证约束（7.5）成立。注意，只要正则化参数满足 $\lambda>0$，它的具体值就不起作用。

图 7.2 展示了一个分类例子：在简单合成数据集上，使用

<!-- pdf-page: 351 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-2.png" alt="二维两类合成数据上使用高斯核的支持向量机边界、等高线及支持向量"><figcaption>图 7.2：二维空间中两个类别的合成数据示例，展示了使用高斯核函数的支持向量机所得的 $y(\mathbf{x})$ 等高线。图中还画出了决策边界、间隔边界以及支持向量。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
式（6.23）形式的高斯核训练支持向量机，得到分类结果。虽然该数据集在二维数据空间 $\mathbf{x}$ 中并非线性可分，但在非线性核函数隐式定义的非线性特征空间中，它是线性可分的。因此，训练数据点在原始数据空间中被完全分开。

这个例子还从几何上说明了 SVM 稀疏性的来源。最大间隔超平面由支持向量的位置决定。其他数据点可以自由移动，只要仍处于间隔区域之外，就不会改变决策边界，因此解与这些数据点无关。

### 7.1.1 类别分布重叠

到目前为止，我们假设训练数据点在特征空间 $\boldsymbol{\phi}(\mathbf{x})$ 中线性可分。所得支持向量机会在原始输入空间 $\mathbf{x}$ 中将训练数据完全分开，尽管相应的决策边界是非线性的。不过，在实践中，类条件分布可能重叠，此时将训练数据完全分开可能导致较差的泛化性能。

因此，需要修改支持向量机，允许一部分训练点被错误分类。从式（7.19）可以看到，对于类别可分的情形，我们隐含地使用了这样一个误差函数：若数据点被误分类，则误差为无穷大；若分类正确，则误差为零，然后优化模型参数以最大化间隔。现在修改这一方法，允许数据点位于间隔边界的“错误一侧”，但施加随该点到边界的距离增大而增大的惩罚。为便于后续优化，将惩罚取为这一距离的线性函数。为此，引入松弛变量（slack variables）$\xi_n\geqslant0$，其中 $n=1,\ldots,N$，每个训练数据点对应一个松弛变量（Bennett, 1992；Cortes and Vapnik, 1995）。对于位于正确间隔边界上或该边界类别内侧的数据点，定义 $\xi_n=0$；对其他点，定义 $\xi_n=|t_n-y(\mathbf{x}_n)|$。因此，位于决策边界 $y(\mathbf{x}_n)=0$ 上的数据点满足 $\xi_n=1$，而

<!-- pdf-page: 352 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-3.png" alt="不同松弛变量取值对应的间隔内外数据点及支持向量"><figcaption>图 7.3：松弛变量 $\xi_n\geqslant0$ 的示意图。带圆圈的数据点是支持向量。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
$\xi_n>1$ 的点会被误分类。于是，精确分类约束（7.5）被替换为

$$
t_ny(\mathbf{x}_n)\geqslant1-\xi_n,\qquad n=1,\ldots,N
\tag{7.20}
$$

其中松弛变量须满足 $\xi_n\geqslant0$。满足 $\xi_n=0$ 的数据点分类正确，并位于间隔边界上或间隔边界的正确一侧。满足 $0<\xi_n\leqslant1$ 的点位于间隔内部，但仍在决策边界的正确一侧；满足 $\xi_n>1$ 的数据点位于决策边界的错误一侧，被误分类，如图 7.3 所示。这有时被描述为放松硬间隔（hard margin）约束，得到软间隔（soft margin），从而允许一部分训练数据点被误分类。注意，虽然松弛变量允许类别分布重叠，但这一框架仍对离群点敏感，因为误分类惩罚随 $\xi$ 线性增加。

现在的目标是最大化间隔，同时对位于间隔边界错误一侧的点施加软惩罚。因此，我们最小化

$$
C\sum_{n=1}^{N}\xi_n+\frac{1}{2}\|\mathbf{w}\|^2
\tag{7.21}
$$

其中参数 $C>0$ 控制松弛变量惩罚与间隔之间的权衡。由于任何被误分类的点都满足 $\xi_n>1$，所以 $\sum_n\xi_n$ 是误分类点数量的上界。因此，参数 $C$ 类似于正则化系数的倒数，因为它控制着最小化训练误差与控制模型复杂度之间的权衡。在 $C\to\infty$ 的极限下，将恢复前面针对可分数据的支持向量机。

现在，希望在约束（7.20）以及 $\xi_n\geqslant0$ 下最小化式（7.21）。相应的拉格朗日函数为

$$
L(\mathbf{w},b,\mathbf{a})=\frac{1}{2}\|\mathbf{w}\|^2+C\sum_{n=1}^{N}\xi_n-\sum_{n=1}^{N}a_n\{t_ny(\mathbf{x}_n)-1+\xi_n\}-\sum_{n=1}^{N}\mu_n\xi_n
\tag{7.22}
$$

<!-- pdf-page: 353 -->

其中 $\{a_n\geqslant0\}$ 和 $\{\mu_n\geqslant0\}$ 是拉格朗日乘子。相应的一组 KKT 条件为<span class="margin-reference">附录 E</span>

$$
a_n\geqslant0
\tag{7.23}
$$

$$
t_ny(\mathbf{x}_n)-1+\xi_n\geqslant0
\tag{7.24}
$$

$$
a_n(t_ny(\mathbf{x}_n)-1+\xi_n)=0
\tag{7.25}
$$

$$
\mu_n\geqslant0
\tag{7.26}
$$

$$
\xi_n\geqslant0
\tag{7.27}
$$

$$
\mu_n\xi_n=0
\tag{7.28}
$$

其中 $n=1,\ldots,N$。

现在，利用 $y(\mathbf{x})$ 的定义（7.1），对 $\mathbf{w}$、$b$ 和 $\{\xi_n\}$ 进行优化并将它们消去，得到

$$
\frac{\partial L}{\partial\mathbf{w}}=0\quad\Rightarrow\quad\mathbf{w}=\sum_{n=1}^{N}a_nt_n\boldsymbol{\phi}(\mathbf{x}_n)
\tag{7.29}
$$

$$
\frac{\partial L}{\partial b}=0\quad\Rightarrow\quad\sum_{n=1}^{N}a_nt_n=0
\tag{7.30}
$$

$$
\frac{\partial L}{\partial\xi_n}=0\quad\Rightarrow\quad a_n=C-\mu_n.
\tag{7.31}
$$

利用这些结果，从拉格朗日函数中消去 $\mathbf{w}$、$b$ 和 $\{\xi_n\}$，得到对偶拉格朗日函数

$$
\widetilde{L}(\mathbf{a})=\sum_{n=1}^{N}a_n-\frac{1}{2}\sum_{n=1}^{N}\sum_{m=1}^{N}a_na_mt_nt_mk(\mathbf{x}_n,\mathbf{x}_m)
\tag{7.32}
$$

它与可分情形相同，只是约束略有不同。为了看清这些约束，注意，由于 $a_n$ 是拉格朗日乘子，因此要求 $a_n\geqslant0$。此外，式（7.31）结合 $\mu_n\geqslant0$，意味着 $a_n\leqslant C$。因此，需要对对偶变量 $\{a_n\}$ 最小化式（7.32），并满足

$$
0\leqslant a_n\leqslant C
\tag{7.33}
$$

$$
\sum_{n=1}^{N}a_nt_n=0
\tag{7.34}
$$

其中 $n=1,\ldots,N$，式（7.33）称为盒约束（box constraints）。这仍然是一个二次规划问题。将式（7.29）代入式（7.1），可以看到，对新数据点的预测仍然使用式（7.13）。

现在可以解释所得解。与前面一样，一部分数据点可能满足 $a_n=0$，这时它们不对预测

<!-- pdf-page: 354 -->
<!-- join-previous-paragraph -->
模型（7.13）作出贡献。其余数据点构成支持向量。它们满足 $a_n>0$，因此由式（7.25），必须满足

$$
t_ny(\mathbf{x}_n)=1-\xi_n.
\tag{7.35}
$$

如果 $a_n<C$，式（7.31）意味着 $\mu_n>0$，由式（7.28）又要求 $\xi_n=0$，因此这样的点位于间隔边界上。满足 $a_n=C$ 的点可以位于间隔内部：若 $\xi_n\leqslant1$，则分类正确；若 $\xi_n>1$，则被误分类。

为了确定式（7.1）中的参数 $b$，注意到满足 $0<a_n<C$ 的支持向量具有 $\xi_n=0$，因此 $t_ny(\mathbf{x}_n)=1$，从而满足

$$
t_n\left(\sum_{m\in\mathcal{S}}a_mt_mk(\mathbf{x}_n,\mathbf{x}_m)+b\right)=1.
\tag{7.36}
$$

同样，通过取平均可以得到数值稳定的解：

$$
b=\frac{1}{N_{\mathcal{M}}}\sum_{n\in\mathcal{M}}\left(t_n-\sum_{m\in\mathcal{S}}a_mt_mk(\mathbf{x}_n,\mathbf{x}_m)\right)
\tag{7.37}
$$

其中 $\mathcal{M}$ 表示满足 $0<a_n<C$ 的数据点的下标集合。

Schölkopf et al.（2000）提出了支持向量机的另一种等价形式，称为 $\nu$-SVM。它要求最大化

$$
\widetilde{L}(\mathbf{a})=-\frac{1}{2}\sum_{n=1}^{N}\sum_{m=1}^{N}a_na_mt_nt_mk(\mathbf{x}_n,\mathbf{x}_m)
\tag{7.38}
$$

并满足约束

$$
0\leqslant a_n\leqslant1/N
\tag{7.39}
$$

$$
\sum_{n=1}^{N}a_nt_n=0
\tag{7.40}
$$

$$
\sum_{n=1}^{N}a_n\geqslant\nu.
\tag{7.41}
$$

这种方法的优点是，替代 $C$ 的参数 $\nu$ 既可解释为间隔错误比例的上界，又可解释为支持向量比例的下界。间隔错误是指满足 $\xi_n>0$ 的点，它们位于间隔边界的错误一侧，但可能被正确分类，也可能被误分类。图 7.4 展示了将 $\nu$-SVM 用于一个合成数据集的例子。这里使用形式为 $\exp(-\gamma\|\mathbf{x}-\mathbf{x}'\|^2)$ 的高斯核，取 $\gamma=0.45$。

虽然对新输入的预测只使用支持向量，但训练阶段，即确定参数 $\mathbf{a}$ 和 $b$，会使用整个数据集。因此，高效求解

<!-- pdf-page: 355 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-4.png" alt="二维不可分数据集上的 ν-SVM 分类与支持向量"><figcaption>图 7.4：将 $\nu$-SVM 应用于二维不可分数据集的示例。圆圈表示支持向量。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
二次规划问题的算法很重要。首先注意，式（7.10）或式（7.32）给出的目标函数 $\widetilde{L}(\mathbf{a})$ 是二次函数，因此只要约束定义了一个凸区域，任何局部最优解也都是全局最优解；这里的约束是线性的，因而确实定义了凸区域。由于计算量和内存要求很高，使用传统技术直接求解二次规划问题往往不可行，所以需要寻找更实用的方法。分块法（chunking）（Vapnik, 1982）利用了以下事实：如果删除核矩阵中对应于零值拉格朗日乘子的行与列，拉格朗日函数的值不会改变。这样可以把完整的二次规划问题分解为一系列较小的问题，最终目标是识别全部非零拉格朗日乘子，并丢弃其余乘子。分块法可以使用 protected conjugate gradients 实现（Burges, 1998）。虽然分块法把二次函数中矩阵的规模从数据点数量的平方，缩减到大约非零拉格朗日乘子数量的平方，但对大规模应用而言，这个矩阵仍可能大到无法放入内存。分解方法（decomposition methods）（Osuna et al., 1996）同样求解一系列较小的二次规划问题，但设计时让每个问题的规模固定，因此可以用于任意大的数据集。不过，它仍然需要对二次规划子问题进行数值求解，而这些子问题可能难以处理且代价高昂。最常用的支持向量机训练方法之一称为序贯最小优化（sequential minimal optimization，SMO）（Platt, 1999）。它把分块的概念推到极限，每次只考虑两个拉格朗日乘子。在这种情况下，子问题可以解析求解，从而完全避免数值二次规划。该方法给出了启发式规则，用来选择每一步要考虑的拉格朗日乘子对。实践中发现，SMO 的计算量随数据点数量的增长速度介于线性与二次之间，具体取决于应用。

我们已经看到，核函数对应于特征空间中的内积，而特征空间可以是高维的，甚至无限维的。因此，直接用核函数计算而不显式引入特征空间，似乎使支持向量机能够以某种方式避免维数

<!-- pdf-page: 356 -->
<!-- join-previous-paragraph -->
灾难。然而，事实并非如此，因为各特征的取值之间存在约束，限制了特征空间的有效维数。<span class="margin-reference">第 1.4 节</span>为说明这一点，考虑一个简单的二次多项式核，将其按分量展开：

$$
\begin{aligned}
k(\mathbf{x},\mathbf{z})&=(1+\mathbf{x}^{\mathrm{T}}\mathbf{z})^2=(1+x_1z_1+x_2z_2)^2\\
&=1+2x_1z_1+2x_2z_2+x_1^2z_1^2+2x_1z_1x_2z_2+x_2^2z_2^2\\
&=(1,\sqrt{2}x_1,\sqrt{2}x_2,x_1^2,\sqrt{2}x_1x_2,x_2^2)(1,\sqrt{2}z_1,\sqrt{2}z_2,z_1^2,\sqrt{2}z_1z_2,z_2^2)^{\mathrm{T}}\\
&=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{z}).
\end{aligned}
\tag{7.42}
$$

因此，这个核函数表示六维特征空间中的内积，从输入空间到特征空间的映射由向量函数 $\boldsymbol{\phi}(\mathbf{x})$ 描述。不过，对这些不同特征加权的系数被约束为特定形式。因此，原来二维空间 $\mathbf{x}$ 中的任意一组点，在六维特征空间中都被约束为恰好位于嵌入其中的一个二维非线性流形上。

我们已经强调，支持向量机不提供概率输出，而是对新的输入向量作出分类决策。Veropoulos et al.（1999）讨论了如何修改 SVM，使假阳性错误与假阴性错误之间的权衡可控。不过，如果希望把 SVM 用作一个更大概率系统中的模块，就需要对新输入 $\mathbf{x}$ 的类别标记 $t$ 作概率预测。

为解决这个问题，Platt（2000）提出对已经训练好的支持向量机的输出拟合一个 logistic sigmoid 函数。具体来说，假设所需条件概率具有如下形式：

$$
p(t=1\mid\mathbf{x})=\sigma(Ay(\mathbf{x})+B)
\tag{7.43}
$$

其中 $y(\mathbf{x})$ 由式（7.1）定义。用成对的 $y(\mathbf{x}_n)$ 与 $t_n$ 值构成训练集，最小化该训练集定义的交叉熵误差函数，从而确定参数 $A$ 和 $B$。用于拟合 sigmoid 的数据必须独立于训练原 SVM 的数据，以避免严重过拟合。这种两阶段方法，等价于假设支持向量机的输出 $y(\mathbf{x})$ 表示 $\mathbf{x}$ 属于类别 $t=1$ 的对数几率。由于 SVM 的训练过程并非专门为促成这一性质而设计，SVM 对后验概率的近似可能很差（Tipping, 2001）。

### 7.1.2 与逻辑回归的关系

与可分情形一样，可以把针对不可分分布的 SVM 重新表述为最小化一个正则化误差函数。这样也便于突出它与逻辑回归模型之间的相似和不同之处。<span class="margin-reference">第 4.3.2 节</span>

我们已经看到，对于位于间隔边界正确一侧、因而满足 $y_nt_n\geqslant1$ 的数据点，有 $\xi_n=0$；而对于

<!-- pdf-page: 357 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-5.png" alt="铰链误差、逻辑回归误差、误分类误差与平方误差的比较"><figcaption>图 7.5：支持向量机所用的“铰链”误差函数以蓝色绘出；逻辑回归的误差函数以红色绘出，并乘以 $1/\ln(2)$ 进行缩放，使其经过点 $(0,1)$。图中还以黑色绘出了误分类误差，以绿色绘出了平方误差。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
其余数据点，有 $\xi_n=1-y_nt_n$。因此，忽略一个整体乘法常数，目标函数（7.21）可以写成

$$
\sum_{n=1}^{N}E_{\mathrm{SV}}(y_nt_n)+\lambda\|\mathbf{w}\|^2
\tag{7.44}
$$

其中 $\lambda=(2C)^{-1}$，而 $E_{\mathrm{SV}}(\cdot)$ 是铰链误差函数（hinge error function），其定义为

$$
E_{\mathrm{SV}}(y_nt_n)=[1-y_nt_n]_+
\tag{7.45}
$$

其中 $[\,\cdot\,]_+$ 表示正值部分。铰链误差函数因其形状而得名，如图 7.5 所示。它可以看成对误分类误差的近似；误分类误差才是我们理想中希望最小化的误差函数，也绘于图 7.5 中。

在第 4.3.2 节讨论逻辑回归模型时，我们发现使用目标变量 $t\in\{0,1\}$ 很方便。为了与支持向量机比较，首先用目标变量 $t\in\{-1,1\}$ 重新表述最大似然逻辑回归。为此，注意到 $p(t=1\mid y)=\sigma(y)$，其中 $y(\mathbf{x})$ 由式（7.1）给出，$\sigma(y)$ 是式（4.59）定义的 logistic sigmoid 函数。利用 logistic sigmoid 函数的性质，有 $p(t=-1\mid y)=1-\sigma(y)=\sigma(-y)$，因此可以写成

$$
p(t\mid y)=\sigma(yt).
\tag{7.46}
$$

由此，对似然函数取负对数即可构造误差函数；加入二次正则化项后，其形式为<span class="margin-reference">习题 7.6</span>

$$
\sum_{n=1}^{N}E_{\mathrm{LR}}(y_nt_n)+\lambda\|\mathbf{w}\|^2.
\tag{7.47}
$$

其中

$$
E_{\mathrm{LR}}(yt)=\ln\left(1+\exp(-yt)\right).
\tag{7.48}
$$

<!-- pdf-page: 358 -->

为了与其他误差函数比较，可以将该函数除以 $\ln(2)$，使它经过点 $(0,1)$。图 7.5 也绘出了这个经过缩放的误差函数，可以看到，其形式与支持向量误差函数相似。关键区别在于，$E_{\mathrm{SV}}(yt)$ 中的平坦区域会产生稀疏解。

逻辑回归误差和铰链损失都可以看成对误分类误差的连续近似。另一个有时用于解决分类问题的连续误差函数是平方误差，图 7.5 中也绘出了它。然而，平方误差有这样一个性质：对于分类正确、却在决策边界正确一侧远离边界的数据点，它会给予越来越大的重视。这类点会获得很大的权重，从而削弱对误分类点的重视。因此，如果目标是最小化误分类率，那么单调递减的误差函数是更好的选择。

### 7.1.3 多类 SVM

支持向量机本质上是一种二类分类器。然而在实践中，我们经常需要处理涉及 $K>2$ 个类别的问题。因此，人们提出了多种方法，将多个二类 SVM 组合起来，构成多类分类器。

一种常用方法（Vapnik, 1998）是构造 $K$ 个独立的 SVM，其中第 $k$ 个模型 $y_k(\mathbf{x})$ 以类别 $\mathcal{C}_k$ 的数据为正例，其余 $K-1$ 个类别的数据为负例来训练。这称为一对其余（one-versus-the-rest）方法。不过，在图 4.2 中我们已经看到，采用各个分类器的决策可能产生不一致的结果，使一个输入同时被分到多个类别。解决这一问题时，有时会使用下式预测新输入 $\mathbf{x}$：

$$
y(\mathbf{x})=\max_k y_k(\mathbf{x}).
\tag{7.49}
$$

遗憾的是，这种启发式方法存在一个问题：不同分类器针对不同任务训练，无法保证不同分类器的实值量 $y_k(\mathbf{x})$ 具有适当的尺度。

一对其余方法的另一个问题是训练集不均衡。例如，若有十个类别，每类的训练数据点数量相同，那么各个分类器所用的数据集会包含 $90\%$ 的负例和仅 $10\%$ 的正例，原问题的对称性便丢失了。Lee et al.（2001）提出了一对其余方案的一种变体：修改目标值，使正类的目标值为 $+1$，负类的目标值为 $-1/(K-1)$。

Weston and Watkins（1999）定义了一个单一目标函数，通过最大化每个类别与其余类别之间的间隔，同时训练全部 $K$ 个 SVM。然而，这可能使训练慢得多：原来只需分别求解 $K$ 个各含 $N$ 个数据点的优化问题，总代价为 $O(KN^2)$；现在则必须求解一个规模为 $(K-1)N$ 的优化问题，总代价为 $O(K^2N^2)$。

<!-- pdf-page: 359 -->

另一种方法是对所有可能的类别对，训练 $K(K-1)/2$ 个不同的二类 SVM，然后根据哪个类别获得最多“票数”来对测试点分类。这种方法有时称为一对一（one-versus-one）。同样，我们在图 4.2 中已经看到，这可能使最终分类产生歧义。而且，当 $K$ 很大时，该方法所需的训练时间远多于一对其余方法。类似地，对测试点求值也需要更多计算。

可以将这些成对分类器组织成一个有向无环图（不要与概率图模型混淆），从而缓解后一个问题；所得方法称为 DAGSVM（Platt et al., 2000）。对于 $K$ 个类别，DAGSVM 共有 $K(K-1)/2$ 个分类器；对一个新的测试点分类时，只需对 $K-1$ 个成对分类器求值。具体使用哪些分类器，取决于沿图遍历的路径。

Dietterich and Bakiri（1995）提出了另一种基于纠错输出编码（error-correcting output codes）的多类分类方法，Allwein et al.（2000）将其应用于支持向量机。它可以看成一对一方法中投票方案的推广，使用更一般的类别划分来训练各个分类器。每个类别都用所选二类分类器的一组特定响应来表示；再结合适当的解码方案，就能对各个分类器输出中的错误和歧义具有鲁棒性。尽管 SVM 如何用于多类分类问题仍是一个开放问题，但在实践中，一对其余方法仍然最为常用，即使它的构造具有临时拼凑的性质，也有实际局限。

还有单类支持向量机（single-class support vector machine），用于解决一个与概率密度估计有关的无监督学习问题。不过，这些方法不对数据密度建模，而是试图找到一条光滑边界，将高密度区域围起来。选择该边界，使它表示密度的一个分位数；也就是说，从该分布中抽取的数据点落入这个区域的概率，是预先指定的一个介于 $0$ 和 $1$ 之间的固定数值。这个问题的范围比估计完整密度更受限，但可能足以满足特定应用的需要。针对这一问题，已有两种使用支持向量机的方法。Schölkopf et al.（2001）的算法试图找到一个超平面，将除固定比例 $\nu$ 以外的所有训练数据与原点分开，同时最大化超平面到原点的距离（间隔）。Tax and Duin（1999）则寻找特征空间中最小的球，使它包含除比例 $\nu$ 以外的所有数据点。对于仅是 $\mathbf{x}-\mathbf{x}'$ 的函数的核 $k(\mathbf{x},\mathbf{x}')$，这两种算法等价。

### 7.1.4 用于回归的 SVM

现在把支持向量机扩展到回归问题，同时保留其稀疏性。<span class="margin-reference">第 3.1.4 节</span>在简单线性回归中，我们

<!-- pdf-page: 360 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-6.png" alt="ε 不敏感误差函数与二次误差函数的比较"><figcaption>图 7.6：$\epsilon$ 不敏感误差函数以红色绘出。在不敏感区域之外，误差随距离线性增长。图中还以绿色绘出了二次误差函数，以便比较。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
最小化如下正则化误差函数：

$$
\frac{1}{2}\sum_{n=1}^{N}\{y_n-t_n\}^2+\frac{\lambda}{2}\|\mathbf{w}\|^2.
\tag{7.50}
$$

为了得到稀疏解，将二次误差函数替换为 $\epsilon$ 不敏感误差函数（$\epsilon$-insensitive error function）（Vapnik, 1995）。当预测值 $y(\mathbf{x})$ 与目标值 $t$ 之差的绝对值小于 $\epsilon$ 时，该误差函数取零，其中 $\epsilon>0$。一种简单的 $\epsilon$ 不敏感误差函数，对不敏感区域之外的误差赋予线性代价，其表达式为

$$
E_{\epsilon}(y(\mathbf{x})-t)=
\begin{cases}
0,&\text{若 }|y(\mathbf{x})-t|<\epsilon;\\
|y(\mathbf{x})-t|-\epsilon,&\text{其他情况}
\end{cases}
\tag{7.51}
$$

如图 7.6 所示。

因此，我们最小化如下正则化误差函数：

$$
C\sum_{n=1}^{N}E_{\epsilon}(y(\mathbf{x}_n)-t_n)+\frac{1}{2}\|\mathbf{w}\|^2
\tag{7.52}
$$

其中 $y(\mathbf{x})$ 由式（7.1）给出。按照惯例，以 $C$ 表示的正则化参数的倒数置于误差项之前。

与前面一样，可以通过引入松弛变量，重新表述这个优化问题。对于每个数据点 $\mathbf{x}_n$，现在需要两个松弛变量 $\xi_n\geqslant0$ 和 $\widehat{\xi}_n\geqslant0$，其中 $\xi_n>0$ 对应于满足 $t_n>y(\mathbf{x}_n)+\epsilon$ 的点，而 $\widehat{\xi}_n>0$ 对应于满足 $t_n<y(\mathbf{x}_n)-\epsilon$ 的点，如图 7.7 所示。

目标点位于 $\epsilon$ 管内的条件是 $y_n-\epsilon\leqslant t_n\leqslant y_n+\epsilon$，其中 $y_n=y(\mathbf{x}_n)$。引入松弛变量后，只要松弛变量不为零，就允许点落在管外，相应的条件为

$$
t_n\leqslant y(\mathbf{x}_n)+\epsilon+\xi_n
\tag{7.53}
$$

$$
t_n\geqslant y(\mathbf{x}_n)-\epsilon-\widehat{\xi}_n.
\tag{7.54}
$$

<!-- pdf-page: 361 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/a-fig-7-7.png" alt="支持向量回归曲线、ε 不敏感管及管外点的松弛变量"><figcaption>图 7.7：SVM 回归示意图，显示了回归曲线及其 $\epsilon$ 不敏感“管”，并给出了松弛变量 $\xi$ 和 $\widehat{\xi}$ 的示例。$\epsilon$ 管上方的点满足 $\xi>0$ 且 $\widehat{\xi}=0$；$\epsilon$ 管下方的点满足 $\xi=0$ 且 $\widehat{\xi}>0$；$\epsilon$ 管内的点满足 $\xi=\widehat{\xi}=0$。</figcaption></figure>

于是，支持向量回归的误差函数可以写成

$$
C\sum_{n=1}^{N}(\xi_n+\widehat{\xi}_n)+\frac{1}{2}\|\mathbf{w}\|^2
\tag{7.55}
$$

需要在满足 $\xi_n\geqslant0$、$\widehat{\xi}_n\geqslant0$ 以及式（7.53）和式（7.54）的约束下，将其最小化。为此，引入拉格朗日乘子 $a_n\geqslant0$、$\widehat{a}_n\geqslant0$、$\mu_n\geqslant0$ 和 $\widehat{\mu}_n\geqslant0$，然后优化拉格朗日函数

$$
\begin{aligned}
L={}&C\sum_{n=1}^{N}(\xi_n+\widehat{\xi}_n)+\frac{1}{2}\|\mathbf{w}\|^2-\sum_{n=1}^{N}(\mu_n\xi_n+\widehat{\mu}_n\widehat{\xi}_n)\\
&-\sum_{n=1}^{N}a_n(\epsilon+\xi_n+y_n-t_n)-\sum_{n=1}^{N}\widehat{a}_n(\epsilon+\widehat{\xi}_n-y_n+t_n).
\end{aligned}
\tag{7.56}
$$

现在用式（7.1）代入 $y(\mathbf{x})$，然后令拉格朗日函数关于 $\mathbf{w}$、$b$、$\xi_n$ 和 $\widehat{\xi}_n$ 的导数为零，得到

$$
\frac{\partial L}{\partial\mathbf{w}}=0\quad\Rightarrow\quad\mathbf{w}=\sum_{n=1}^{N}(a_n-\widehat{a}_n)\boldsymbol{\phi}(\mathbf{x}_n)
\tag{7.57}
$$

$$
\frac{\partial L}{\partial b}=0\quad\Rightarrow\quad\sum_{n=1}^{N}(a_n-\widehat{a}_n)=0
\tag{7.58}
$$

$$
\frac{\partial L}{\partial\xi_n}=0\quad\Rightarrow\quad a_n+\mu_n=C
\tag{7.59}
$$

$$
\frac{\partial L}{\partial\widehat{\xi}_n}=0\quad\Rightarrow\quad\widehat{a}_n+\widehat{\mu}_n=C.
\tag{7.60}
$$

利用这些结果，从拉格朗日函数中消去相应变量，可以看到，对偶问题要求最大化<span class="margin-reference">习题 7.7</span>

<!-- pdf-page: 362 -->

$$
\begin{aligned}
\widetilde{L}(\mathbf{a},\widehat{\mathbf{a}})={}&-\frac{1}{2}\sum_{n=1}^{N}\sum_{m=1}^{N}(a_n-\widehat{a}_n)(a_m-\widehat{a}_m)k(\mathbf{x}_n,\mathbf{x}_m)\\
&-\epsilon\sum_{n=1}^{N}(a_n+\widehat{a}_n)+\sum_{n=1}^{N}(a_n-\widehat{a}_n)t_n
\end{aligned}
\tag{7.61}
$$

最大化是关于 $\{a_n\}$ 和 $\{\widehat{a}_n\}$ 进行的，这里引入了核 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}')$。这同样是一个受约束的最大化问题。为找出这些约束，注意到 $a_n\geqslant0$ 和 $\widehat{a}_n\geqslant0$ 都是必需的，因为它们是拉格朗日乘子。此外，$\mu_n\geqslant0$ 和 $\widehat{\mu}_n\geqslant0$ 与式（7.59）、式（7.60）一起，要求 $a_n\leqslant C$ 和 $\widehat{a}_n\leqslant C$，因此再次得到盒约束

$$
0\leqslant a_n\leqslant C
\tag{7.62}
$$

$$
0\leqslant\widehat{a}_n\leqslant C
\tag{7.63}
$$

以及条件（7.58）。

将式（7.57）代入式（7.1），可知对新输入的预测可以使用

$$
y(\mathbf{x})=\sum_{n=1}^{N}(a_n-\widehat{a}_n)k(\mathbf{x},\mathbf{x}_n)+b
\tag{7.64}
$$

它同样用核函数表示。

相应的 Karush-Kuhn-Tucker（KKT）条件要求，在解处，对偶变量与约束的乘积必须为零，其表达式为

$$
a_n(\epsilon+\xi_n+y_n-t_n)=0
\tag{7.65}
$$

$$
\widehat{a}_n(\epsilon+\widehat{\xi}_n-y_n+t_n)=0
\tag{7.66}
$$

$$
(C-a_n)\xi_n=0
\tag{7.67}
$$

$$
(C-\widehat{a}_n)\widehat{\xi}_n=0.
\tag{7.68}
$$

由此可以得到几个有用的结果。首先，注意到只有当 $\epsilon+\xi_n+y_n-t_n=0$ 时，系数 $a_n$ 才可能非零。这意味着该数据点要么位于 $\epsilon$ 管的上边界上（$\xi_n=0$），要么位于上边界上方（$\xi_n>0$）。类似地，$\widehat{a}_n$ 非零意味着 $\epsilon+\widehat{\xi}_n-y_n+t_n=0$，这样的点必须位于 $\epsilon$ 管的下边界上或下边界下方。

此外，$\epsilon+\xi_n+y_n-t_n=0$ 与 $\epsilon+\widehat{\xi}_n-y_n+t_n=0$ 这两个约束不相容。将它们相加，并注意到 $\xi_n$ 和 $\widehat{\xi}_n$ 非负、$\epsilon$ 严格为正，就很容易看出这一点。因此，对每个数据点 $\mathbf{x}_n$，$a_n$ 或 $\widehat{a}_n$ 中至少有一个必须为零。

支持向量是对式（7.64）给出的预测有贡献的数据点，也就是 $a_n\ne0$ 或 $\widehat{a}_n\ne0$ 的点。这些点位于 $\epsilon$ 管的边界上或管外。管内的所有点都满足

<!-- pdf-page: 363 -->
<!-- join-previous-paragraph -->
$a_n=\widehat{a}_n=0$。我们再次得到了稀疏解，预测模型（7.64）中需要求值的项，仅限于涉及支持向量的那些项。

可以考虑一个满足 $0<a_n<C$ 的数据点来求得参数 $b$。根据式（7.67），该点必须满足 $\xi_n=0$，因此由式（7.65）可知，它必须满足 $\epsilon+y_n-t_n=0$。使用式（7.1）并解出 $b$，得到

$$
\begin{aligned}
b&=t_n-\epsilon-\mathbf{w}^{\mathrm{T}}\boldsymbol{\phi}(\mathbf{x}_n)\\
&=t_n-\epsilon-\sum_{m=1}^{N}(a_m-\widehat{a}_m)k(\mathbf{x}_n,\mathbf{x}_m)
\end{aligned}
\tag{7.69}
$$

其中使用了式（7.57）。考虑一个满足 $0<\widehat{a}_n<C$ 的点，可以得到类似结果。在实践中，最好对 $b$ 的所有这类估计取平均。

与分类情形一样，用于回归的 SVM 也有另一种形式，其中控制复杂度的参数具有更直观的解释（Schölkopf et al., 2000）。具体来说，不固定不敏感区域的宽度 $\epsilon$，而是固定参数 $\nu$，用它约束落在管外的点所占比例。这要求最大化

$$
\begin{aligned}
\widetilde{L}(\mathbf{a},\widehat{\mathbf{a}})={}&-\frac{1}{2}\sum_{n=1}^{N}\sum_{m=1}^{N}(a_n-\widehat{a}_n)(a_m-\widehat{a}_m)k(\mathbf{x}_n,\mathbf{x}_m)\\
&+\sum_{n=1}^{N}(a_n-\widehat{a}_n)t_n
\end{aligned}
\tag{7.70}
$$

并满足约束

$$
0\leqslant a_n\leqslant C/N
\tag{7.71}
$$

$$
0\leqslant\widehat{a}_n\leqslant C/N
\tag{7.72}
$$

$$
\sum_{n=1}^{N}(a_n-\widehat{a}_n)=0
\tag{7.73}
$$

$$
\sum_{n=1}^{N}(a_n+\widehat{a}_n)\leqslant\nu C.
\tag{7.74}
$$

可以证明，落在不敏感管之外的数据点至多有 $\nu N$ 个，而支持向量至少有 $\nu N$ 个，它们位于管的边界上或管外。

图 7.8 通过正弦数据集，展示了使用支持向量机解决回归问题的例子。<span class="margin-reference">附录 A</span>这里的参数 $\nu$ 和 $C$ 是手工选择的。在实践中，通常通过交叉验证来确定它们的值。

<!-- pdf-page: 364 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-8.png" alt="采用高斯核的ν-SVM对正弦数据的回归预测与支持向量"><figcaption>图 7.8：将用于回归的 $\nu$-SVM 应用于正弦合成数据集的示例，采用高斯核。红色线为预测的回归曲线，阴影区域对应于 $\epsilon$ 不敏感管道。数据点以绿色表示，其中对应支持向量的数据点用蓝色圆圈标出。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

### 7.1.5 计算学习理论

从历史上看，支持向量机的提出和分析在很大程度上基于一种称为*计算学习理论*（computational learning theory）的理论框架，它有时也称为*统计学习理论*（statistical learning theory）（Anthony and Biggs, 1992; Kearns and Vazirani, 1994; Vapnik, 1995; Vapnik, 1998）。它起源于 Valiant（1984）提出的*概率近似正确*（probably approximately correct，PAC）学习框架。PAC 框架的目标是理解：要获得良好的泛化能力，需要多大的数据集。它还给出学习所需计算成本的界，不过这里不讨论这一点。

假设大小为 $N$ 的数据集 $\mathcal{D}$ 从某个联合分布 $p(\mathbf{x},t)$ 中抽取，其中 $\mathbf{x}$ 是输入变量，$t$ 表示类别标记。我们将注意力限制在“无噪声”的情况，即类别标记由某个未知的确定性函数 $t=g(\mathbf{x})$ 决定。在 PAC 学习中，根据训练集 $\mathcal{D}$，从函数空间 $\mathcal{F}$ 中选择函数 $f(\mathbf{x};\mathcal{D})$。如果它的期望错误率低于某个预先指定的阈值 $\epsilon$，即

$$
\mathbb{E}_{\mathbf{x},t}\left[I\left(f(\mathbf{x};\mathcal{D})\ne t\right)\right]<\epsilon
\tag{7.75}
$$

就说它具有良好的泛化能力。这里 $I(\cdot)$ 是指示函数，期望关于分布 $p(\mathbf{x},t)$ 计算。左端的量是随机变量，因为它依赖于训练集 $\mathcal{D}$；PAC 框架要求，对于从 $p(\mathbf{x},t)$ 随机抽取的数据集 $\mathcal{D}$，（7.75）以大于 $1-\delta$ 的概率成立。这里 $\delta$ 是另一个预先指定的参数。“概率近似正确”这一名称，来自这样的要求：以很高的概率，大于 $1-\delta$，使错误率很小，小于 $\epsilon$。对于给定的模型空间 $\mathcal{F}$，以及给定的参数 $\epsilon$ 和 $\delta$，PAC 学习旨在为满足这一准则所需的最小数据集大小 $N$ 提供界。PAC 学习中的一个关键量是 *Vapnik–Chervonenkis 维数*，简称 *VC 维*；它衡量函数空间的复杂度，并使 PAC 框架能够扩展到包含无穷多个函数的空间。

PAC 框架中推导出的界通常被称为最坏

<!-- pdf-page: 365 -->

<!-- join-previous-paragraph -->
情况下的界，因为它们适用于分布 $p(\mathbf{x},t)$ 的任意选择，只要训练样本和测试样本都从同一分布中独立抽取；它们也适用于函数 $f(\mathbf{x})$ 的任意选择，只要该函数属于 $\mathcal{F}$。在现实世界的机器学习应用中，所处理的分布通常具有明显的规律，例如，输入空间的大片区域具有相同的类别标记。由于不对分布形式作任何假设，PAC 界非常保守；换言之，它们会严重高估达到给定泛化性能所需的数据集大小。因此，PAC 界在实际应用中即使有所使用，也很少见。

一种使 PAC 界更紧的尝试是 PAC–Bayesian 框架（McAllester, 2003）。它考虑函数空间 $\mathcal{F}$ 上的一个分布，这与贝叶斯处理中的先验有些类似。它仍然考虑 $p(\mathbf{x},t)$ 的任意可能选择，因此，虽然所得的界更紧，但仍然非常保守。

## 7.2 相关向量机

支持向量机已被用于多种分类和回归应用。不过，它有若干局限，本章已经强调了其中几项。特别是，SVM 的输出表示决策，而不是后验概率。另外，SVM 最初是针对二类问题提出的，扩展到 $K>2$ 个类别时会遇到困难。复杂度参数 $C$ 或 $\nu$，以及回归中的参数 $\epsilon$，必须通过交叉验证等留出方法来确定。最后，预测表示为核函数的线性组合，这些核函数以训练数据点为中心，而且必须是正定的。

*相关向量机*（relevance vector machine，RVM）（Tipping, 2001）是一种用于回归和分类的贝叶斯稀疏核技术。它具有 SVM 的许多特征，同时避免了 SVM 的主要局限。此外，它通常能得到稀疏得多的模型，因此在测试数据上的计算速度相应更快，同时保持相近的泛化误差。

与介绍 SVM 时不同，先介绍 RVM 的回归形式，再考虑如何扩展到分类任务，会更加方便。

### 7.2.1 用于回归的 RVM

用于回归的相关向量机，是第 3 章研究过的那种线性模型，但使用了经过修改的先验，从而得到稀疏解。给定输入向量 $\mathbf{x}$，模型为实值目标变量 $t$ 定义如下条件分布：

$$
p(t\mid\mathbf{x},\mathbf{w},\beta)=\mathcal{N}(t\mid y(\mathbf{x}),\beta^{-1})
\tag{7.76}
$$

<!-- pdf-page: 366 -->

其中 $\beta=\sigma^{-2}$ 是噪声精度，即噪声方差的倒数，均值由如下形式的线性模型给出：

$$
y(\mathbf{x})=\sum_{i=1}^{M}w_i\phi_i(\mathbf{x})=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{7.77}
$$

其中非线性基函数 $\phi_i(\mathbf{x})$ 固定不变，通常还包含一个常数项，使相应的权重参数表示“偏置”。

相关向量机是这个模型的一个具体实例，其结构意在与支持向量机相对应。具体来说，基函数由核给出，训练集中的每个数据点都关联一个核。于是，一般表达式（7.77）具有类似 SVM 的形式：

$$
y(\mathbf{x})=\sum_{n=1}^{N}w_n k(\mathbf{x},\mathbf{x}_n)+b
\tag{7.78}
$$

其中 $b$ 是偏置参数。此时参数数目为 $M=N+1$，$y(\mathbf{x})$ 与 SVM 的预测模型（7.64）形式相同，只是这里将系数 $a_n$ 记为 $w_n$。应强调的是，后续分析对任意基函数选择都成立；为保持一般性，我们将使用（7.77）的形式。与 SVM 不同，这里不局限于正定核，基函数的数目和位置也不必与训练数据点绑定。

假设给定输入向量 $\mathbf{x}$ 的 $N$ 个观测，将它们统记为数据矩阵 $\mathbf{X}$，其第 $n$ 行为 $\mathbf{x}_n^{\mathrm T}$，其中 $n=1,\ldots,N$。相应的目标值为 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。于是，似然函数为

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)=\prod_{n=1}^{N}p(t_n\mid\mathbf{x}_n,\mathbf{w},\beta^{-1}).
\tag{7.79}
$$

接下来为参数向量 $\mathbf{w}$ 引入先验分布。与第 3 章一样，考虑零均值的高斯先验。不过，RVM 的关键区别在于：为每个权重参数 $w_i$ 分别引入超参数 $\alpha_i$，而不是共享单个超参数。因此，权重先验具有如下形式：

$$
p(\mathbf{w}\mid\boldsymbol{\alpha})=\prod_{i=1}^{M}\mathcal{N}(w_i\mid0,\alpha_i^{-1})
\tag{7.80}
$$

其中 $\alpha_i$ 表示相应参数 $w_i$ 的精度，$\boldsymbol{\alpha}$ 表示 $(\alpha_1,\ldots,\alpha_M)^{\mathrm T}$。我们将看到，当关于这些超参数最大化证据时，其中相当大一部分会趋于无穷大，相应权重参数的后验分布则集中于零。因此，与这些参数关联的基函数在

<!-- pdf-page: 367 -->

<!-- join-previous-paragraph -->
模型作出的预测中不起作用，实际上就被剪除，从而得到稀疏模型。

利用线性回归模型的结果（3.49），可知权重的后验分布仍然是高斯分布，形式为

$$
p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\mathbf{X},\boldsymbol{\alpha},\beta)=\mathcal{N}(\mathbf{w}\mid\mathbf{m},\boldsymbol{\Sigma})
\tag{7.81}
$$

其中均值和协方差分别为

$$
\mathbf{m}=\beta\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{7.82}
$$

$$
\boldsymbol{\Sigma}=(\mathbf{A}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}
\tag{7.83}
$$

这里 $\boldsymbol{\Phi}$ 是一个 $N\times M$ 设计矩阵，元素为 $\Phi_{ni}=\phi_i(\mathbf{x}_n)$，而 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。注意，对于模型（7.78）这一特殊情况，有 $\boldsymbol{\Phi}=\mathbf{K}$，其中 $\mathbf{K}$ 是元素为 $k(\mathbf{x}_n,\mathbf{x}_m)$ 的对称 $(N+1)\times(N+1)$ 核矩阵。

$\boldsymbol{\alpha}$ 和 $\beta$ 的值通过第二类最大似然确定，也称为证据近似（3.5 节）。在这一方法中，通过对权重参数积分消元得到边缘似然函数，再将其最大化：

$$
p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\boldsymbol{\alpha},\beta)=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\alpha})\,d\mathbf{w}.
\tag{7.84}
$$

由于这表示两个高斯分布的卷积，很容易计算（习题 7.10），得到如下形式的对数边缘似然：

$$
\begin{aligned}
\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\boldsymbol{\alpha},\beta)&=\ln\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\mathbf{0},\mathbf{C})\\
&=-\frac{1}{2}\{N\ln(2\pi)+\ln|\mathbf{C}|+\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\mathsf{t}}\}
\end{aligned}
\tag{7.85}
$$

其中 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$，并定义了如下 $N\times N$ 矩阵 $\mathbf{C}$：

$$
\mathbf{C}=\beta^{-1}\mathbf{I}+\boldsymbol{\Phi}\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}.
\tag{7.86}
$$

现在的目标是关于超参数 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化（7.85）。这只需对 3.5 节中线性回归模型的证据近似结果稍作修改。同样可以采用两种方法。第一种方法是直接令边缘似然的相应导数为零，得到以下重估方程（习题 7.12）：

$$
\alpha_i^{\mathrm{new}}=\frac{\gamma_i}{m_i^2}
\tag{7.87}
$$

$$
(\beta^{\mathrm{new}})^{-1}=\frac{\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}\|^2}{N-\sum_i\gamma_i}
\tag{7.88}
$$

其中 $m_i$ 是（7.82）定义的后验均值 $\mathbf{m}$ 的第 $i$ 个分量。量 $\gamma_i$ 衡量相应参数 $w_i$ 被数据确定的程度（3.5.3 节），其定义为

<!-- pdf-page: 368 -->

$$
\gamma_i=1-\alpha_i\Sigma_{ii}
\tag{7.89}
$$

其中 $\Sigma_{ii}$ 是（7.83）给出的后验协方差 $\boldsymbol{\Sigma}$ 的第 $i$ 个对角元素。因此，学习过程如下：先选择 $\boldsymbol{\alpha}$ 和 $\beta$ 的初始值，分别利用（7.82）和（7.83）计算后验分布的均值与协方差，再交替执行超参数重估和后验均值、协方差的重估；前者使用（7.87）和（7.88），后者使用（7.82）和（7.83），直到满足适当的收敛准则。

第二种方法使用 EM 算法，将在 9.3.4 节讨论。这两种寻找使证据最大的超参数值的方法在形式上等价（习题 9.23）。不过，从数值计算看，与（7.87）和（7.88）对应的直接优化方法收敛稍快（Tipping, 2001）。

优化的结果是，一部分超参数 $\{\alpha_i\}$ 被推向很大的值，原则上为无穷大（7.2.2 节），因此对应权重参数 $w_i$ 的后验分布，其均值和方差都为零。于是，这些参数和相应基函数 $\phi_i(\mathbf{x})$ 被从模型中删除，在对新输入作预测时不起作用。对于（7.78）形式的模型，剩余非零权重对应的输入 $\mathbf{x}_n$ 称为*相关向量*（relevance vectors），因为它们通过自动相关性确定机制识别出来，与 SVM 的支持向量类似。不过，需要强调的是，这种通过自动相关性确定在概率模型中实现稀疏性的机制相当一般，可用于任何表示为基函数可调线性组合的模型。

找到使边缘似然最大的超参数值 $\boldsymbol{\alpha}^{\star}$ 和 $\beta^{\star}$ 后，就可以计算新输入 $\mathbf{x}$ 对应的 $t$ 的预测分布。利用（7.76）和（7.81），得到（习题 7.14）

$$
\begin{aligned}
p(t\mid\mathbf{x},\mathbf{X},\boldsymbol{\mathsf{t}},\boldsymbol{\alpha}^{\star},\beta^{\star})&=\int p(t\mid\mathbf{x},\mathbf{w},\beta^{\star})p(\mathbf{w}\mid\mathbf{X},\boldsymbol{\mathsf{t}},\boldsymbol{\alpha}^{\star},\beta^{\star})\,d\mathbf{w}\\
&=\mathcal{N}\left(t\mid\mathbf{m}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}),\sigma^2(\mathbf{x})\right).
\end{aligned}
\tag{7.90}
$$

因此，预测均值由（7.76）给出，其中将 $\mathbf{w}$ 设为后验均值 $\mathbf{m}$；预测分布的方差为

$$
\sigma^2(\mathbf{x})=(\beta^{\star})^{-1}+\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\Sigma}\boldsymbol{\phi}(\mathbf{x})
\tag{7.91}
$$

其中 $\boldsymbol{\Sigma}$ 由（7.83）给出，并将其中的 $\boldsymbol{\alpha}$ 和 $\beta$ 设为优化后的值 $\boldsymbol{\alpha}^{\star}$ 和 $\beta^{\star}$。这就是在线性回归背景下得到的熟悉结果（3.59）。回顾一下，对于局部化基函数，线性回归模型的预测方差会在输入空间中没有基函数的区域变小。对于基函数以数据点为中心的 RVM，在数据范围之外进行外推时，模型会对自己的预测越来越确信（Rasmussen and Quiñonero-Candela, 2005），这当然是不希望发生的。高斯过程回归中的预测分布（6.4.2 节）没有

<!-- pdf-page: 369 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-9.png" alt="相关向量机回归的预测均值、一个标准差区间及三个相关向量"><figcaption>图 7.9：RVM 回归示例，使用与图 7.8 中 $\nu$-SVM 回归模型相同的数据集和高斯核函数。红色线表示 RVM 预测分布的均值，阴影区域表示预测分布的一个标准差范围。数据点以绿色表示，相关向量用蓝色圆圈标出。注意，这里只有 3 个相关向量，而图 7.8 中的 $\nu$-SVM 有 7 个支持向量。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
这一问题。不过，高斯过程作预测的计算成本通常比 RVM 高得多。

图 7.9 给出了将 RVM 应用于正弦回归数据集的一个例子。这里，噪声精度参数 $\beta$ 也通过证据最大化来确定。可以看到，RVM 中的相关向量数目明显少于 SVM 使用的支持向量数目。在广泛的回归和分类任务中，RVM 所得模型的规模通常比相应支持向量机小一个数量级，从而显著提高处理测试数据的速度。引人注意的是，与相应的 SVM 相比，泛化误差几乎没有降低或完全未降低，却实现了这种更强的稀疏性。

与 SVM 相比，RVM 的主要缺点是训练涉及非凸函数的优化，而且训练时间可能比相当的 SVM 更长。对于具有 $M$ 个基函数的模型，RVM 需要求一个 $M\times M$ 矩阵的逆，通常需要 $O(M^3)$ 的计算量。在类似 SVM 的模型（7.78）这一特殊情况下，有 $M=N+1$。前面已经指出，一些 SVM 训练技术的计算成本大致随 $N$ 的平方增长。当然，对于 RVM，始终可以选择从少于 $N+1$ 个基函数开始。更重要的是，在相关向量机中，控制复杂度和噪声方差的参数通过一次训练就能自动确定；而在支持向量机中，参数 $C$ 和 $\epsilon$（或 $\nu$）一般通过交叉验证来确定，这涉及多次训练。此外，下一节将推导相关向量机的另一种训练过程，它能显著提高训练速度。

### 7.2.2 稀疏性分析

前面已经指出，自动相关性确定机制使一部分参数被推向零。现在更详细地研究

<!-- pdf-page: 370 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-10.png" alt="与目标向量方向不一致的基向量如何使贝叶斯线性回归选择稀疏解"><figcaption>图 7.10：贝叶斯线性回归模型中稀疏性机制的示意图。叉号表示训练集目标值向量 $\boldsymbol{\mathsf{t}}=(t_1,t_2)^{\mathrm T}$；模型只有一个基向量 $\boldsymbol{\varphi}=(\phi(\mathbf{x}_1),\phi(\mathbf{x}_2))^{\mathrm T}$，其方向与目标数据向量 $\boldsymbol{\mathsf{t}}$ 的方向相差较大。左图的模型只有各向同性噪声，因此 $\mathbf{C}=\beta^{-1}\mathbf{I}$，对应于 $\alpha=\infty$，并将 $\beta$ 设为其最可能的值。右图是相同的模型，但 $\alpha$ 取有限值。两幅图中的红色椭圆都对应于单位马氏距离（Mahalanobis distance），并且 $|\mathbf{C}|$ 的值相同；绿色虚线圆表示噪声项 $\beta^{-1}$ 的贡献。可以看到，$\alpha$ 的任何有限取值都会降低观测数据的概率，因此，在最可能的解中，这个基向量被移除。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
相关向量机中的稀疏性机制。在这一过程中，将得到一个优化超参数的过程，其速度比前面给出的直接方法快得多。

在进行数学分析之前，先对贝叶斯线性模型中稀疏性的来源作一些直观说明。考虑一个包含 $N=2$ 个观测 $t_1$、$t_2$ 的数据集，模型具有单个基函数 $\phi(\mathbf{x})$、超参数 $\alpha$，以及精度为 $\beta$ 的各向同性噪声。由（7.85），边缘似然为 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\mathcal{N}(\boldsymbol{\mathsf{t}}\mid\mathbf{0},\mathbf{C})$，其中协方差矩阵的形式为

$$
\mathbf{C}=\frac{1}{\beta}\mathbf{I}+\frac{1}{\alpha}\boldsymbol{\varphi}\boldsymbol{\varphi}^{\mathrm T}
\tag{7.92}
$$

这里 $\boldsymbol{\varphi}$ 表示 $N$ 维向量 $(\phi(\mathbf{x}_1),\phi(\mathbf{x}_2))^{\mathrm T}$，类似地，$\boldsymbol{\mathsf{t}}=(t_1,t_2)^{\mathrm T}$。注意，这就是 $\mathbf{t}$ 上均值为零、协方差为 $\mathbf{C}$ 的高斯过程模型。给定 $\mathbf{t}$ 的某个观测，目标是通过最大化边缘似然，求得 $\alpha^{\star}$ 和 $\beta^{\star}$。由图 7.10 可以看到，如果 $\boldsymbol{\varphi}$ 的方向与训练数据向量 $\mathbf{t}$ 的方向相差较大，那么相应超参数 $\alpha$ 就会被推向 $\infty$，该基向量将从模型中被剪除。这是因为，只要 $\beta$ 设为其最优值，$\alpha$ 的任何有限取值都会给数据分配更低的概率，从而降低 $\boldsymbol{\mathsf{t}}$ 处的密度值。可以看到，$\alpha$ 取任何有限值都会使分布沿着偏离数据的方向拉长，从而增加远离观测数据区域的概率质量，降低目标数据向量本身所在位置的密度值。对于具有 $M$ 个

<!-- pdf-page: 371 -->

<!-- join-previous-paragraph -->
基向量 $\boldsymbol{\varphi}_1,\ldots,\boldsymbol{\varphi}_M$ 的更一般情况，也有类似的直观解释：如果某个基向量与数据向量 $\mathbf{t}$ 的方向相差较大，它就很可能从模型中被剪除。

现在，对于包含 $M$ 个基函数的一般情况，从更严格的数学角度研究稀疏性机制。为引出这一分析，先注意，在重估参数 $\alpha_i$ 的结果（7.87）中，右端各项本身也是 $\alpha_i$ 的函数。因此，这些结果给出的是隐式解；即使固定所有其他 $\alpha_j$（$j\ne i$），只确定单个 $\alpha_i$，也需要迭代。

这提示了求解 RVM 优化问题的另一种方法：显式写出边缘似然（7.85）对某个 $\alpha_i$ 的全部依赖，再显式求出其驻点（Faul and Tipping, 2002; Tipping and Faul, 2003）。为此，先从（7.86）定义的矩阵 $\mathbf{C}$ 中分离出 $\alpha_i$ 的贡献，得到

$$
\begin{aligned}
\mathbf{C}&=\beta^{-1}\mathbf{I}+\sum_{j\ne i}\alpha_j^{-1}\boldsymbol{\varphi}_j\boldsymbol{\varphi}_j^{\mathrm T}+\alpha_i^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}\\
&=\mathbf{C}_{-i}+\alpha_i^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}
\end{aligned}
\tag{7.93}
$$

其中 $\boldsymbol{\varphi}_i$ 表示 $\boldsymbol{\Phi}$ 的第 $i$ 列，即元素为 $(\phi_i(\mathbf{x}_1),\ldots,\phi_i(\mathbf{x}_N))$ 的 $N$ 维向量；它不同于表示 $\boldsymbol{\Phi}$ 第 $n$ 行的 $\boldsymbol{\phi}_n$。矩阵 $\mathbf{C}_{-i}$ 表示从矩阵 $\mathbf{C}$ 中去掉基函数 $i$ 的贡献所得的矩阵。利用矩阵恒等式（C.7）和（C.15），可以将 $\mathbf{C}$ 的行列式和逆矩阵写为

$$
|\mathbf{C}|=|\mathbf{C}_{-i}|\,|1+\alpha_i^{-1}\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i|
\tag{7.94}
$$

$$
\mathbf{C}^{-1}=\mathbf{C}_{-i}^{-1}-\frac{\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}}{\alpha_i+\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i}.
\tag{7.95}
$$

利用这些结果，就可以将对数边缘似然函数（7.85）写成如下形式（习题 7.15）：

$$
L(\boldsymbol{\alpha})=L(\boldsymbol{\alpha}_{-i})+\lambda(\alpha_i)
\tag{7.96}
$$

其中 $L(\boldsymbol{\alpha}_{-i})$ 就是去掉基函数 $\boldsymbol{\varphi}_i$ 后的对数边缘似然，而量 $\lambda(\alpha_i)$ 定义为

$$
\lambda(\alpha_i)=\frac{1}{2}\left[\ln\alpha_i-\ln(\alpha_i+s_i)+\frac{q_i^2}{\alpha_i+s_i}\right]
\tag{7.97}
$$

它包含对 $\alpha_i$ 的全部依赖。这里引入了两个量

$$
s_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\varphi}_i
\tag{7.98}
$$

$$
q_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}_{-i}^{-1}\boldsymbol{\mathsf{t}}.
\tag{7.99}
$$

其中 $s_i$ 称为 $\boldsymbol{\varphi}_i$ 的*稀疏度*（sparsity），$q_i$ 称为其*质量*（quality）。我们将看到，相对于 $q_i$ 的值，$s_i$ 越大，就意味着基函数 $\boldsymbol{\varphi}_i$

<!-- pdf-page: 372 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-11.png" alt="质量与稀疏度两种相对大小下，对数边缘似然的有限及无穷大最优超参数"><figcaption>图 7.11：对数边缘似然 $\lambda(\alpha_i)$ 随 $\ln\alpha_i$ 变化的曲线。左图中，$q_i^2=4$、$s_i=1$，因此 $q_i^2>s_i$，在有限的 $\alpha_i$ 处有唯一极大值；右图中，$q_i^2=1$、$s_i=2$，因此 $q_i^2<s_i$，极大值在 $\alpha_i=\infty$ 处取得。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
越有可能从模型中被剪除。“稀疏度”衡量基函数 $\boldsymbol{\varphi}_i$ 与模型中其他基向量的重叠程度；“质量”则衡量基向量 $\boldsymbol{\varphi}_n$ 的方向与一种误差方向的一致程度，这种误差是训练集目标值 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$ 与去掉向量 $\boldsymbol{\varphi}_i$ 后模型所给预测向量 $\boldsymbol{\mathsf{y}}_{-i}$ 之间的差（Tipping and Faul, 2003）。

边缘似然关于 $\alpha_i$ 的驻点，出现在导数

$$
\frac{d\lambda(\alpha_i)}{d\alpha_i}=\frac{\alpha_i^{-1}s_i^2-(q_i^2-s_i)}{2(\alpha_i+s_i)^2}
\tag{7.100}
$$

等于零的位置。解有两种可能的形式。回顾 $\alpha_i\geqslant0$，可以看到，如果 $q_i^2<s_i$，那么 $\alpha_i\to\infty$ 给出一个解。反之，如果 $q_i^2>s_i$，就可以解出 $\alpha_i$：

$$
\alpha_i=\frac{s_i^2}{q_i^2-s_i}.
\tag{7.101}
$$

图 7.11 展示了这两种解。可以看到，质量项与稀疏度项的相对大小，决定某个基向量是否会从模型中被剪除。基于边缘似然二阶导数的更完整分析（Faul and Tipping, 2002），确认这些解确实是 $\lambda(\alpha_i)$ 的唯一极大值（习题 7.16）。

注意，对于给定的其他超参数值，这种方法给出了 $\alpha_i$ 的闭式解。除了帮助理解 RVM 中稀疏性的来源，这一分析还导出一种优化超参数的实用算法，具有显著的速度优势。它使用一组固定的候选基向量，依次循环考察它们，决定是否将每个向量纳入模型。所得的顺序稀疏贝叶斯学习算法如下。

<aside class="procedure">
<h3>顺序稀疏贝叶斯学习算法</h3>
<ol>
<li>如果求解的是回归问题，初始化 $\beta$。</li>
<li>使用一个基函数 $\boldsymbol{\varphi}_1$ 初始化，并利用（7.101）设置超参数 $\alpha_1$；其余超参数 $\alpha_j$（$j\ne i$）初始化为无穷大，使模型中仅包含 $\boldsymbol{\varphi}_1$。</li>
</ol>
</aside>

<!-- pdf-page: 373 -->

<!-- join-previous-procedure -->
<aside class="procedure">
<ol start="3">
<li>计算 $\boldsymbol{\Sigma}$ 和 $\mathbf{m}$，以及所有基函数的 $q_i$ 和 $s_i$。</li>
<li>选择一个候选基函数 $\boldsymbol{\varphi}_i$。</li>
<li>如果 $q_i^2>s_i$ 且 $\alpha_i<\infty$，即基向量 $\boldsymbol{\varphi}_i$ 已经包含在模型中，则利用（7.101）更新 $\alpha_i$。</li>
<li>如果 $q_i^2>s_i$ 且 $\alpha_i=\infty$，则将 $\boldsymbol{\varphi}_i$ 加入模型，并利用（7.101）计算超参数 $\alpha_i$。</li>
<li>如果 $q_i^2\leqslant s_i$ 且 $\alpha_i<\infty$，则将基函数 $\boldsymbol{\varphi}_i$ 从模型中移除，并令 $\alpha_i=\infty$。</li>
<li>如果求解的是回归问题，更新 $\beta$。</li>
<li>如果已经收敛，则终止；否则返回第 3 步。</li>
</ol>
</aside>

注意，如果 $q_i^2\leqslant s_i$ 且 $\alpha_i=\infty$，那么基函数 $\boldsymbol{\varphi}_i$ 本来就没有包含在模型中，无需采取任何操作。

在实际计算中，先计算下列量比较方便：

$$
Q_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\mathsf{t}}
\tag{7.102}
$$

$$
S_i=\boldsymbol{\varphi}_i^{\mathrm T}\mathbf{C}^{-1}\boldsymbol{\varphi}_i.
\tag{7.103}
$$

随后，可以将质量和稀疏度变量表示为

$$
q_i=\frac{\alpha_i Q_i}{\alpha_i-S_i}
\tag{7.104}
$$

$$
s_i=\frac{\alpha_i S_i}{\alpha_i-S_i}.
\tag{7.105}
$$

注意，当 $\alpha_i=\infty$ 时，有 $q_i=Q_i$ 且 $s_i=S_i$。利用（C.7），可以写出（习题 7.17）

$$
Q_i=\beta\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\mathsf{t}}-\beta^2\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\Phi}\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}
\tag{7.106}
$$

$$
S_i=\beta\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\varphi}_i-\beta^2\boldsymbol{\varphi}_i^{\mathrm T}\boldsymbol{\Phi}\boldsymbol{\Sigma}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\varphi}_i
\tag{7.107}
$$

其中 $\boldsymbol{\Phi}$ 和 $\boldsymbol{\Sigma}$ 只涉及与有限超参数 $\alpha_i$ 对应的基向量。因此，每个阶段所需计算量为 $O(M^3)$，其中 $M$ 为模型中活跃基向量的数目，通常远小于训练模式的数目 $N$。

### 7.2.3 用于分类的 RVM

将权重的 ARD 先验用于第 4 章研究过的概率线性分类模型，就可以将相关向量机框架扩展到分类问题。首先考虑目标变量为二元变量 $t\in\{0,1\}$ 的二类问题。现在，模型采用基函数的线性组合，再通过 logistic sigmoid 函数变换的形式：

$$
y(\mathbf{x},\mathbf{w})=\sigma\left(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})\right)
\tag{7.108}
$$

<!-- pdf-page: 374 -->

其中 $\sigma(\cdot)$ 是（4.59）定义的 logistic sigmoid 函数。如果为权重向量 $\mathbf{w}$ 引入高斯先验，就得到第 4 章已经考虑过的模型。这里的区别在于，RVM 使用 ARD 先验（7.80），每个权重参数都关联一个独立的精度超参数。

与回归模型不同，现在无法再对参数向量 $\mathbf{w}$ 进行解析积分。这里遵循 Tipping（2001）的方法，使用拉普拉斯近似（4.4 节）；4.5.1 节已将它用于密切相关的贝叶斯逻辑回归问题。

首先初始化超参数向量 $\boldsymbol{\alpha}$。对于给定的 $\boldsymbol{\alpha}$，构建后验分布的高斯近似，进而得到边缘似然的近似。最大化这个近似边缘似然，就得到重估后的 $\boldsymbol{\alpha}$，重复这一过程直到收敛。

更详细地考察这个模型的拉普拉斯近似。对于固定的 $\boldsymbol{\alpha}$，通过最大化下式，求得 $\mathbf{w}$ 的后验分布的众数：

$$
\begin{aligned}
\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})&=\ln\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\alpha})\}-\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha})\\
&=\sum_{n=1}^{N}\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}-\frac{1}{2}\mathbf{w}^{\mathrm T}\mathbf{A}\mathbf{w}+\mathrm{const}
\end{aligned}
\tag{7.109}
$$

其中 $\mathbf{A}=\operatorname{diag}(\alpha_i)$。这可以通过 4.3.3 节讨论的迭代重加权最小二乘（IRLS）完成。为此，需要对数后验分布的梯度向量和 Hessian 矩阵，由（7.109）可得（习题 7.18）

$$
\nabla\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})=\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{t}}-\boldsymbol{\mathsf{y}})-\mathbf{A}\mathbf{w}
\tag{7.110}
$$

$$
\nabla\nabla\ln p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\boldsymbol{\alpha})=-(\boldsymbol{\Phi}^{\mathrm T}\mathbf{B}\boldsymbol{\Phi}+\mathbf{A})
\tag{7.111}
$$

其中 $\mathbf{B}$ 是 $N\times N$ 对角矩阵，对角元素为 $b_n=y_n(1-y_n)$，向量 $\boldsymbol{\mathsf{y}}=(y_1,\ldots,y_N)^{\mathrm T}$，$\boldsymbol{\Phi}$ 是元素为 $\Phi_{ni}=\phi_i(\mathbf{x}_n)$ 的设计矩阵。这里使用了 logistic sigmoid 函数导数的性质（4.88）。当 IRLS 算法收敛时，Hessian 矩阵的负值就是后验分布高斯近似的协方差矩阵的逆。

所得后验近似的众数，对应于高斯近似的均值，通过令（7.110）为零来求得。由此得到拉普拉斯近似的均值和协方差：

$$
\mathbf{w}^{\star}=\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}(\boldsymbol{\mathsf{t}}-\boldsymbol{\mathsf{y}})
\tag{7.112}
$$

$$
\boldsymbol{\Sigma}=(\boldsymbol{\Phi}^{\mathrm T}\mathbf{B}\boldsymbol{\Phi}+\mathbf{A})^{-1}.
\tag{7.113}
$$

现在可以用这个拉普拉斯近似计算边缘似然。利用通过拉普拉斯近似计算积分的一般结果（4.135），

<!-- pdf-page: 375 -->

<!-- join-previous-paragraph -->
得到

$$
\begin{aligned}
p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha})&=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\boldsymbol{\alpha})\,d\mathbf{w}\\
&\simeq p(\boldsymbol{\mathsf{t}}\mid\mathbf{w}^{\star})p(\mathbf{w}^{\star}\mid\boldsymbol{\alpha})(2\pi)^{M/2}|\boldsymbol{\Sigma}|^{1/2}.
\end{aligned}
\tag{7.114}
$$

代入 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w}^{\star})$ 和 $p(\mathbf{w}^{\star}\mid\boldsymbol{\alpha})$，再令边缘似然关于 $\alpha_i$ 的导数等于零，得到（习题 7.19）

$$
-\frac{1}{2}(w_i^{\star})^2+\frac{1}{2\alpha_i}-\frac{1}{2}\Sigma_{ii}=0.
\tag{7.115}
$$

定义 $\gamma_i=1-\alpha_i\Sigma_{ii}$ 并整理，得到

$$
\alpha_i^{\mathrm{new}}=\frac{\gamma_i}{(w_i^{\star})^2}
\tag{7.116}
$$

这与用于回归的 RVM 所得到的重估公式（7.87）相同。

如果定义

$$
\widehat{\boldsymbol{\mathsf{t}}}=\boldsymbol{\Phi}\mathbf{w}^{\star}+\mathbf{B}^{-1}(\boldsymbol{\mathsf{t}}-\mathbf{y})
\tag{7.117}
$$

就可以将近似对数边缘似然写成

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\alpha},\beta)=-\frac{1}{2}\left\{N\ln(2\pi)+\ln|\mathbf{C}|+(\widehat{\boldsymbol{\mathsf{t}}})^{\mathrm T}\mathbf{C}^{-1}\widehat{\boldsymbol{\mathsf{t}}}\right\}
\tag{7.118}
$$

其中

$$
\mathbf{C}=\mathbf{B}+\boldsymbol{\Phi}\mathbf{A}\boldsymbol{\Phi}^{\mathrm T}.
\tag{7.119}
$$

它与回归情况下的（7.85）具有相同形式，因此可以应用相同的稀疏性分析，得到相同的快速学习算法：每一步都充分优化一个超参数 $\alpha_i$。

图 7.12 给出了将相关向量机应用于合成分类数据集的结果（附录 A）。与支持向量机不同，相关向量往往不位于决策边界附近。这与前面对 RVM 稀疏性的讨论一致，因为以边界附近数据点为中心的基函数 $\phi_i(\mathbf{x})$，其向量 $\boldsymbol{\varphi}_i$ 的方向与训练数据向量 $\boldsymbol{\mathsf{t}}$ 的方向相差较大。

与 SVM 相比，相关向量机的一项潜在优点是它能给出概率预测。例如，这使得 RVM 可以辅助构建发射密度，用于线性动态系统的一种非线性扩展，从而在视频序列中跟踪人脸（Williams et al., 2005；13.3 节）。

到目前为止，考虑的都是用于二类分类问题的 RVM。对于 $K>2$ 个类别，再次利用 4.3.4 节的概率方法，其中有 $K$ 个如下形式的线性模型：

$$
a_k=\mathbf{w}_k^{\mathrm T}\mathbf{x}
\tag{7.120}
$$

<!-- pdf-page: 376 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-07/b-fig-7-12.png" alt="相关向量机的分类边界、相关向量及类别后验概率"><figcaption>图 7.12：相关向量机应用于一个合成数据集的示例。左图给出决策边界和数据点，相关向量用圆圈标出。与图 7.4 中相应支持向量机的结果相比，可以看到 RVM 给出的模型要稀疏得多。右图给出 RVM 输出的后验概率，其中红色（蓝色）颜料所占的比例，表示该点属于红色（蓝色）类别的概率。</figcaption><p class="figure-translation">左图中的红色与蓝色叉号表示两个类别的数据点，绿色圆圈标出相关向量，黑线表示决策边界；右图中红色与蓝色的比例表示相应类别的后验概率。</p></figure>

这些模型通过 softmax 函数组合起来，得到输出

$$
y_k(\mathbf{x})=\frac{\exp(a_k)}{\sum_j\exp(a_j)}.
\tag{7.121}
$$

相应的对数似然函数为

$$
\ln p(\mathbf{T}\mid\mathbf{w}_1,\ldots,\mathbf{w}_K)=\prod_{n=1}^{N}\prod_{k=1}^{K}y_{nk}^{t_{nk}}
\tag{7.122}
$$

其中，每个数据点 $n$ 的目标值 $t_{nk}$ 采用 1-of-$K$ 编码，$\mathbf{T}$ 是元素为 $t_{nk}$ 的矩阵。同样，可以使用拉普拉斯近似优化超参数（Tipping, 2001），其中模型及其 Hessian 矩阵通过 IRLS 求得。与支持向量机采用的两两配对方法相比，这为多类分类提供了理论依据更充分的方法，也能为新数据点给出概率预测。它的主要缺点是 Hessian 矩阵的大小为 $MK\times MK$，其中 $M$ 为有效基函数的数量；因此，与二类 RVM 相比，训练计算量多出一个 $K^3$ 的因子。

相关向量机的主要缺点是，与 SVM 相比，训练时间较长。不过，它无需通过交叉验证运行来设定模型复杂度参数，这在一定程度上抵消了上述缺点。此外，由于它得到的模型更稀疏，测试点上的计算时间通常短得多，而在实践中，这往往是更重要的考虑因素。

<!-- pdf-page: 377 -->

## 习题

**7.1（⋆⋆）www** 假设有一个由输入向量 $\{\mathbf{x}_n\}$ 构成的数据集，相应的目标值为 $t_n\in\{-1,1\}$；再假设使用核为 $k(\mathbf{x},\mathbf{x}')$ 的 Parzen 核密度估计器（见 2.5.1 节），分别对每个类别中的输入向量密度建模。假定两个类别的先验概率相等，写出使误分类率最小的决策规则。进一步证明，如果选择核 $k(\mathbf{x},\mathbf{x}')=\mathbf{x}^{\mathrm T}\mathbf{x}'$，那么分类规则就简化为：把新的输入向量分配给均值与它最近的类别。最后证明，如果核的形式为 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')$，分类就依据特征空间 $\boldsymbol{\phi}(\mathbf{x})$ 中最近的均值进行。

**7.2（⋆）** 证明，如果将约束（7.5）右侧的 $1$ 替换为任意常数 $\gamma>0$，最大间隔超平面的解保持不变。

**7.3（⋆⋆）** 证明，无论数据空间的维数是多少，一个仅含两个数据点、每个类别各有一个点的数据集，就足以确定最大间隔超平面的位置。

**7.4（⋆⋆）www** 证明，最大间隔超平面的间隔值 $\rho$ 满足

$$
\frac{1}{\rho^2}=\sum_{n=1}^{N}a_n
\tag{7.123}
$$

其中，$\{a_n\}$ 是在约束（7.11）和（7.12）下最大化（7.10）得到的。

**7.5（⋆⋆）** 证明，上一题中的 $\rho$ 和 $\{a_n\}$ 还满足

$$
\frac{1}{\rho^2}=2\widetilde{L}(\mathbf{a})
\tag{7.124}
$$

其中，$\widetilde{L}(\mathbf{a})$ 由（7.10）定义。类似地，证明

$$
\frac{1}{\rho^2}=\|\mathbf{w}\|^2.
\tag{7.125}
$$

**7.6（⋆）** 考虑目标变量为 $t\in\{-1,1\}$ 的逻辑回归模型。若定义 $p(t=1\mid y)=\sigma(y)$，其中 $y(\mathbf{x})$ 由（7.1）给出，证明在负对数似然中加入二次正则化项后，所得表达式具有（7.47）的形式。

**7.7（⋆）** 考虑用于回归的支持向量机的拉格朗日函数（7.56）。将拉格朗日函数关于 $\mathbf{w}$、$b$、$\xi_n$ 和 $\widehat{\xi}_n$ 的导数设为零，再回代消去相应变量，证明对偶拉格朗日函数由（7.61）给出。

<!-- pdf-page: 378 -->

**7.8（⋆）www** 对于 7.1.4 节讨论的回归支持向量机，证明所有满足 $\xi_n>0$ 的训练数据点都有 $a_n=C$；类似地，所有满足 $\widehat{\xi}_n>0$ 的点都有 $\widehat{a}_n=C$。

**7.9（⋆）** 验证回归 RVM 中权重后验分布的均值和协方差满足（7.82）和（7.83）。

**7.10（⋆⋆）www** 在（7.84）的指数项中运用配方法，完成关于 $\mathbf{w}$ 的高斯积分，推导回归 RVM 的边缘似然函数的结果（7.85）。

**7.11（⋆⋆）** 重做上一题，但这次使用一般结果（2.115）。

**7.12（⋆⋆）www** 证明，直接最大化回归相关向量机的对数边缘似然（7.85），会得到重估方程（7.87）和（7.88），其中 $\gamma_i$ 由（7.89）定义。

**7.13（⋆⋆）** 在 RVM 回归的证据框架中，我们通过最大化（7.85）给出的边缘似然，得到了重估公式（7.87）和（7.88）。加入形如（B.26）的伽马分布（gamma distribution）作为超先验，扩展这一方法；关于 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化相应的后验概率 $p(\boldsymbol{\mathsf{t}},\boldsymbol{\alpha},\beta\mid\mathbf{X})$，求出 $\boldsymbol{\alpha}$ 和 $\beta$ 的相应重估公式。

**7.14（⋆⋆）** 推导用于回归的相关向量机的预测分布的结果（7.90）。证明其预测方差由（7.91）给出。

**7.15（⋆⋆）www** 利用（7.94）和（7.95），证明边缘似然（7.85）可以写成（7.96）的形式，其中 $\lambda(\alpha_n)$ 由（7.97）定义，稀疏度因子和质量因子分别由（7.98）和（7.99）定义。

**7.16（⋆）** 对回归 RVM 的对数边缘似然（7.97）求关于超参数 $\alpha_i$ 的二阶导数，证明（7.101）给出的驻点是边缘似然的极大值点。

**7.17（⋆⋆）** 利用（7.83）和（7.86），以及矩阵恒等式（C.7），证明（7.102）和（7.103）定义的量 $S_n$ 和 $Q_n$ 可以写成（7.106）和（7.107）的形式。

**7.18（⋆）www** 证明，用于分类的相关向量机的对数后验分布（7.109）的梯度向量和 Hessian 矩阵分别由（7.110）和（7.111）给出。

**7.19（⋆⋆）** 验证，最大化用于分类的相关向量机的近似对数边缘似然函数（7.114），会得到用于重估超参数的结果（7.116）。
