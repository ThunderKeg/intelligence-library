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
