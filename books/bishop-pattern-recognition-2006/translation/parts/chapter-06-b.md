<!-- pdf-page: 328 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-5.png" alt="六组不同核参数下从高斯过程先验抽取的函数样本"><figcaption>图 6.5：从协方差函数（6.63）定义的高斯过程先验中抽取的样本。每张图上方的标题表示 $(\theta_0,\theta_1,\theta_2,\theta_3)$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
$c=k(\mathbf{x}_{N+1},\mathbf{x}_{N+1})+\beta^{-1}$。利用结果（2.81）和（2.82），可知条件分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}})$ 是高斯分布，其均值和协方差分别为

$$
m(\mathbf{x}_{N+1})=\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}
\tag{6.66}
$$

$$
\sigma^2(\mathbf{x}_{N+1})=c-\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{k}.
\tag{6.67}
$$

这两个关键结果定义了高斯过程回归。由于向量 $\mathbf{k}$ 是测试点输入值 $\mathbf{x}_{N+1}$ 的函数，预测分布是一个均值和方差都依赖于 $\mathbf{x}_{N+1}$ 的高斯分布。图 6.8 给出了高斯过程回归的一个例子。

对核函数唯一的限制是，（6.62）给出的协方差矩阵必须正定。如果 $\lambda_i$ 是 $\mathbf{K}$ 的一个特征值，那么 $\mathbf{C}$ 的相应特征值为 $\lambda_i+\beta^{-1}$。因此，只需核矩阵 $k(\mathbf{x}_n,\mathbf{x}_m)$ 对任意一对点 $\mathbf{x}_n$、$\mathbf{x}_m$ 都是半正定的，从而有 $\lambda_i\geqslant0$；因为 $\beta>0$，即使某个特征值 $\lambda_i$ 为零，$\mathbf{C}$ 的相应特征值仍然为正。这与前面对核函数讨论过的限制相同，因此可以再次利用 6.2 节中的所有技术来构造

<!-- pdf-page: 329 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-6.png" alt="高斯过程函数样本、在输入点的函数值及加入高斯噪声后的观测值"><figcaption>图 6.6：从高斯过程中采样数据点 $\{t_n\}$ 的示意图。蓝色曲线是从函数的高斯过程先验中抽取的一个函数样本，红色点是在一组输入值 $\{x_n\}$ 处计算该函数而得到的 $y_n$ 值。绿色表示相应的 $\{t_n\}$，它们通过向每个 $\{y_n\}$ 加入独立高斯噪声而得到。</figcaption><p class="figure-translation">$x$：输入；$t$：目标值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
合适的核。

注意，将预测分布的均值（6.66）看作 $\mathbf{x}_{N+1}$ 的函数时，可以写成

$$
m(\mathbf{x}_{N+1})=\sum_{n=1}^{N}a_n k(\mathbf{x}_n,\mathbf{x}_{N+1})
\tag{6.68}
$$

其中 $a_n$ 是 $\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}$ 的第 $n$ 个分量。因此，如果核函数 $k(\mathbf{x}_n,\mathbf{x}_m)$ 仅依赖于距离 $\|\mathbf{x}_n-\mathbf{x}_m\|$，就得到了径向基函数展开。

结果（6.66）和（6.67）定义了任意核函数 $k(\mathbf{x}_n,\mathbf{x}_m)$ 下高斯过程回归的预测分布。在一个特殊情况下，核函数 $k(\mathbf{x},\mathbf{x}')$ 由有限个基函数定义，这时可以从高斯过程的观点出发，推导出此前在 3.3.2 节中得到的线性回归结果（习题 6.21）。

因此，对于这样的模型，既可以采用参数空间的观点，利用线性回归的结果来得到预测分布，也可以采用函数空间的观点，利用高斯过程的结果来得到预测分布。

使用高斯过程时，核心计算操作涉及一个 $N\times N$ 矩阵的求逆，标准方法需要 $O(N^3)$ 的计算量。相比之下，在基函数模型中，需要求一个 $M\times M$ 矩阵 $\mathbf{S}_N$ 的逆，计算复杂度为 $O(M^3)$。注意，对两种观点而言，对于给定训练集都只需进行一次矩阵求逆。对于每个新的测试点，两种方法都需要进行向量与矩阵的乘法；高斯过程的代价为 $O(N^2)$，线性基函数模型的代价为 $O(M^2)$。如果基函数数目 $M$ 小于数据点数目 $N$，那么采用基函数

<!-- pdf-page: 330 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-7.png" alt="由一个训练点的条件值从联合高斯分布得到测试点的条件分布"><figcaption>图 6.7：只有一个训练点和一个测试点时，高斯过程回归机制的示意图。红色椭圆为联合分布 $p(t_1,t_2)$ 的等高线。这里 $t_1$ 是训练数据点，以 $t_1$ 的值为条件，对应于蓝色竖线，就得到 $p(t_2\mid t_1)$，绿色曲线表示它作为 $t_2$ 的函数。</figcaption><p class="figure-translation">$t_1$：训练点目标值；$t_2$：测试点目标值；$m(\mathbf{x}_2)$：条件均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
框架在计算上会更高效。不过，高斯过程观点的一个优点是，可以考虑那些只能用无穷多个基函数来表示的协方差函数。

然而，对于大型训练数据集，直接应用高斯过程方法可能不可行，因此已经发展出一系列近似方案。与精确方法相比，这些方案的计算量随训练集规模增长得更慢（Gibbs, 1997; Tresp, 2001; Smola and Bartlett, 2001; Williams and Seeger, 2001; Csató and Opper, 2002; Seeger et al., 2003）。Bishop and Nabney（2008）讨论了高斯过程应用中的实际问题。

我们已经介绍了单个目标变量情况下的高斯过程回归。将这一形式扩展到多个目标变量很直接，这称为*协同克里金*（co-kriging）（Cressie, 1993；习题 6.23）。高斯

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-8.png" alt="高斯过程回归的预测均值与两标准差区间，右侧缺少观测时不确定性增大"><figcaption>图 6.8：将高斯过程回归应用于图 A.6 中正弦数据集的示例，其中省略了最右边的三个数据点。绿色曲线是正弦函数；蓝色数据点通过对该函数采样并加入高斯噪声得到。红色线表示高斯过程预测分布的均值，阴影区域对应于均值上下各两个标准差的范围。注意，在数据点右侧的区域，不确定性如何增大。</figcaption></figure>

<!-- pdf-page: 331 -->

<!-- join-previous-paragraph-across-figures -->
过程回归的其他扩展也已有研究，例如，为无监督学习对低维流形上的分布建模（Bishop et al., 1998a），以及求解随机微分方程（Graepel, 2003）。

### 6.4.3 学习超参数

高斯过程模型的预测，部分取决于协方差函数的选择。在实际应用中，我们可能更愿意使用一个参数化的函数族，再从数据中推断参数值，而不是固定协方差函数。这些参数控制相关性的长度尺度、噪声精度等性质，对应于标准参数模型中的超参数。

学习超参数的技术以计算似然函数 $p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 为基础，其中 $\boldsymbol{\theta}$ 表示高斯过程模型的超参数。最简单的方法是通过最大化对数似然函数，得到 $\boldsymbol{\theta}$ 的点估计。由于 $\boldsymbol{\theta}$ 表示这个回归问题的一组超参数，这可以看作与线性回归模型的第二类最大似然过程类似（3.5 节）。可以使用共轭梯度等高效的基于梯度的优化算法，来最大化对数似然（Fletcher, 1987; Nocedal and Wright, 1999; Bishop and Nabney, 2008）。

利用多元高斯分布的标准形式，很容易计算高斯过程回归模型的对数似然函数，得到

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=-\frac{1}{2}\ln|\mathbf{C}_N|-\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}-\frac{N}{2}\ln(2\pi).
\tag{6.69}
$$

对于非线性优化，还需要对数似然函数关于参数向量 $\boldsymbol{\theta}$ 的梯度。假设 $\mathbf{C}_N$ 的导数很容易计算，本章所考虑的协方差函数都满足这一点。利用 $\mathbf{C}_N^{-1}$ 的导数结果（C.21）和 $\ln|\mathbf{C}_N|$ 的导数结果（C.22），得到

$$
\frac{\partial}{\partial\theta_i}\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})=-\frac{1}{2}\operatorname{Tr}\left(\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_i}\right)+\frac{1}{2}\boldsymbol{\mathsf{t}}^{\mathrm T}\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_i}\mathbf{C}_N^{-1}\boldsymbol{\mathsf{t}}.
\tag{6.70}
$$

由于 $\ln p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 一般是非凸函数，它可能具有多个极大值。

很容易为 $\boldsymbol{\theta}$ 引入先验，再使用基于梯度的方法最大化对数后验。在完全贝叶斯处理中，需要对 $\boldsymbol{\theta}$ 进行边缘化，权重为先验 $p(\boldsymbol{\theta})$ 与似然函数 $p(\boldsymbol{\mathsf{t}}\mid\boldsymbol{\theta})$ 的乘积。不过，一般情况下，精确边缘化难以完成，必须借助近似。

高斯过程回归模型给出的预测分布，其均值和方差都是输入向量 $\mathbf{x}$ 的函数。不过，我们假设预测方差中来自加性噪声、由参数 $\beta$ 控制的那部分贡献是一个常数。对于某些称为*异方差*（heteroscedastic）的问题，噪声方差本身也依赖于 $\mathbf{x}$。为此，可以扩展

<!-- pdf-page: 332 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-9.png" alt="两个高斯过程ARD先验曲面样本，比较不同输入方向精度参数的影响"><figcaption>图 6.9：从高斯过程的 ARD 先验中抽取的样本，其中核函数由（6.71）给出。左图对应于 $\eta_1=\eta_2=1$，右图对应于 $\eta_1=1,\eta_2=0.01$。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
高斯过程框架，引入第二个高斯过程，表示 $\beta$ 对输入 $\mathbf{x}$ 的依赖关系（Goldberg et al., 1998）。由于 $\beta$ 是方差，因此非负，所以使用高斯过程对 $\ln\beta(\mathbf{x})$ 建模。

### 6.4.4 自动相关性确定

在上一节中，我们看到，可以利用最大似然来确定高斯过程中的相关长度尺度参数。为每个输入变量分别引入一个参数，可以有效地扩展这一技术（Rasmussen and Williams, 2006）。我们将看到，通过最大似然优化这些参数，就能够从数据中推断不同输入的相对重要性。这是高斯过程背景下*自动相关性确定*（automatic relevance determination，ARD）的一个例子；ARD 最初是在神经网络框架中提出的（MacKay, 1994; Neal, 1996）。7.2.2 节将讨论偏好适当输入的机制。

考虑一个输入空间为二维 $\mathbf{x}=(x_1,x_2)$ 的高斯过程，其核函数具有如下形式：

$$
k(\mathbf{x},\mathbf{x}')=\theta_0\exp\left\{-\frac{1}{2}\sum_{i=1}^{2}\eta_i(x_i-x_i')^2\right\}.
\tag{6.71}
$$

图 6.9 给出了精度参数 $\eta_i$ 取两组不同值时，从所得到的函数 $y(\mathbf{x})$ 的先验中抽取的样本。可以看到，随着某个参数 $\eta_i$ 变小，函数对相应输入变量 $x_i$ 的变化变得相对不敏感。利用最大似然，根据数据集调整这些参数，就可以检测出对预测分布几乎没有影响的输入变量，因为相应的 $\eta_i$ 值会很小。这在实际应用中很有用，因为可以据此舍弃这样的输入。图 6.10 使用一个具有三个输入 $x_1$、$x_2$ 和 $x_3$ 的简单合成数据集说明 ARD（Nabney, 2002）。目标变量 $t$ 的生成方法是：从高斯分布中采样 100 个 $x_1$ 值，计算函数 $\sin(2\pi x_1)$，然后加入

<!-- pdf-page: 333 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-10.png" alt="三个输入对应的自动相关性超参数在边缘似然优化过程中的变化"><figcaption>图 6.10：在一个具有三个输入 $x_1$、$x_2$ 和 $x_3$ 的合成问题中，高斯过程自动相关性确定的示例。曲线表示优化边缘似然时，相应超参数 $\eta_1$（红色）、$\eta_2$（绿色）和 $\eta_3$（蓝色）随迭代次数的变化。详情见正文。注意，纵轴采用对数刻度。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
高斯噪声。$x_2$ 的值由相应的 $x_1$ 值加上噪声得到，$x_3$ 的值则从一个独立的高斯分布中采样。因此，$x_1$ 能很好地预测 $t$，$x_2$ 也能预测 $t$，但噪声更大，而 $x_3$ 与 $t$ 之间只有偶然的相关性。使用缩放共轭梯度算法，优化具有 ARD 参数 $\eta_1,\eta_2,\eta_3$ 的高斯过程的边缘似然。由图 6.10 可见，$\eta_1$ 收敛到一个相对较大的值，$\eta_2$ 收敛到一个小得多的值，而 $\eta_3$ 变得非常小，表明 $x_3$ 与预测 $t$ 无关。

很容易将 ARD 框架纳入指数二次核（6.63），得到如下形式的核函数。在将高斯过程用于多种回归问题时，这种核函数已被证明很有用：

$$
k(\mathbf{x}_n,\mathbf{x}_m)=\theta_0\exp\left\{-\frac{1}{2}\sum_{i=1}^{D}\eta_i(x_{ni}-x_{mi})^2\right\}+\theta_2+\theta_3\sum_{i=1}^{D}x_{ni}x_{mi}
\tag{6.72}
$$

其中 $D$ 是输入空间的维数。

### 6.4.5 用于分类的高斯过程

在分类的概率方法中，目标是在给定训练数据集后，为一个新的输入向量建立目标变量的后验概率模型。这些概率必须位于区间 $(0,1)$ 内，而高斯过程模型的预测值可以位于整个实轴。不过，利用适当的非线性激活函数变换高斯过程的输出，就很容易将高斯过程用于分类问题。

首先考虑目标变量为 $t\in\{0,1\}$ 的二类问题。如果为函数 $a(\mathbf{x})$ 定义一个高斯过程，再利用（4.59）给出的 logistic sigmoid 函数 $y=\sigma(a)$ 进行变换，就得到函数 $y(\mathbf{x})$ 上的非高斯随机过程，其中 $y\in(0,1)$。图 6.11 展示了一维输入空间的情况，此时目标变量 $t$ 的概率分布

<!-- pdf-page: 334 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-11.png" alt="高斯过程潜在函数样本及其经过logistic sigmoid变换后的结果"><figcaption>图 6.11：左图是从函数 $a(\mathbf{x})$ 的高斯过程先验中抽取的一个样本，右图是将这个样本通过 logistic sigmoid 函数变换后的结果。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
由伯努利分布给出：

$$
p(t\mid a)=\sigma(a)^t(1-\sigma(a))^{1-t}.
\tag{6.73}
$$

像通常一样，将训练集的输入记为 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，对应的观测目标变量为 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$。还考虑一个测试点 $\mathbf{x}_{N+1}$，其目标值为 $t_{N+1}$。目标是确定预测分布 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}})$，其中对输入变量的条件依赖隐含在表达式中。为此，对向量 $\mathbf{a}_{N+1}$ 引入一个高斯过程先验，其分量为 $a(\mathbf{x}_1),\ldots,a(\mathbf{x}_{N+1})$。这又定义了 $\mathbf{t}_{N+1}$ 上的一个非高斯过程；以训练数据 $\mathbf{t}_N$ 为条件，就得到所需的预测分布。$\mathbf{a}_{N+1}$ 的高斯过程先验具有如下形式：

$$
p(\mathbf{a}_{N+1})=\mathcal{N}(\mathbf{a}_{N+1}\mid\mathbf{0},\mathbf{C}_{N+1}).
\tag{6.74}
$$

与回归情况不同，协方差矩阵不再包含噪声项，因为假设所有训练数据点的标记都是正确的。不过，出于数值计算的原因，引入一个由参数 $\nu$ 控制的类噪声项会更方便，它可以确保协方差矩阵正定。因此，协方差矩阵 $\mathbf{C}_{N+1}$ 的元素为

$$
C(\mathbf{x}_n,\mathbf{x}_m)=k(\mathbf{x}_n,\mathbf{x}_m)+\nu\delta_{nm}
\tag{6.75}
$$

其中 $k(\mathbf{x}_n,\mathbf{x}_m)$ 可以是 6.2 节所考虑的任意半正定核函数，而 $\nu$ 的值通常预先固定。假设核函数 $k(\mathbf{x},\mathbf{x}')$ 由参数向量 $\boldsymbol{\theta}$ 控制，稍后将讨论如何从训练数据中学习 $\boldsymbol{\theta}$。

对于二类问题，只需预测 $p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)$，因为 $p(t_{N+1}=0\mid\boldsymbol{\mathsf{t}}_N)$ 的值为 $1-p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)$。所需的

<!-- pdf-page: 335 -->

<!-- join-previous-paragraph -->
预测分布为

$$
p(t_{N+1}=1\mid\boldsymbol{\mathsf{t}}_N)=\int p(t_{N+1}=1\mid a_{N+1})p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)\,da_{N+1}
\tag{6.76}
$$

其中 $p(t_{N+1}=1\mid a_{N+1})=\sigma(a_{N+1})$。

这个积分无法解析求出，因此可以用采样方法近似（Neal, 1997）。另一种选择是考虑基于解析近似的技术。在 4.5.2 节中，我们推导了 logistic sigmoid 函数与高斯分布的卷积的近似公式（4.153）。只要有后验分布 $p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 的高斯近似，就可以利用这个结果计算（6.76）中的积分。通常，用高斯分布近似后验分布的依据是：由中心极限定理，真实后验分布会随着数据点数目的增加而趋于高斯分布（2.3 节）。对于高斯过程，变量数目随数据点数目一起增长，因此不能直接应用这一论证。不过，如果考虑增加 $\mathbf{x}$ 空间某个固定区域内的数据点数目，那么函数 $a(\mathbf{x})$ 的相应不确定性就会减小，同样会渐近地得到高斯分布（Williams and Barber, 1998）。

已有研究考虑了三种不同的高斯近似方法。第一种技术基于变分推断（Gibbs and MacKay, 2000；10.1 节），并利用 logistic sigmoid 函数的局部变分界（10.144）。这样可以将 sigmoid 函数的乘积近似为高斯函数的乘积，从而对 $\mathbf{a}_N$ 进行解析边缘化。该方法还给出了似然函数 $p(\mathbf{t}_N\mid\boldsymbol{\theta})$ 的一个下界。通过对 softmax 函数作高斯近似，高斯过程分类的变分框架还可以扩展到多类（$K>2$）问题（Gibbs, 1997）。

第二种方法使用期望传播（Opper and Winther, 2000b; Minka, 2001b; Seeger, 2003；10.7 节）。正如马上将会看到的，真实后验分布是单峰的，因此期望传播方法可以取得较好的结果。

### 6.4.6 拉普拉斯近似

高斯过程分类的第三种方法基于拉普拉斯近似（4.4 节），现在对它作详细讨论。为了计算预测分布（6.76），我们寻找 $a_{N+1}$ 的后验分布的高斯近似。根据贝叶斯定理，该后验分布为

$$
\begin{aligned}
p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)&=\int p(a_{N+1},\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)\,d\mathbf{a}_N\\
&=\frac{1}{p(\boldsymbol{\mathsf{t}}_N)}\int p(a_{N+1},\mathbf{a}_N)p(\boldsymbol{\mathsf{t}}_N\mid a_{N+1},\mathbf{a}_N)\,d\mathbf{a}_N\\
&=\frac{1}{p(\boldsymbol{\mathsf{t}}_N)}\int p(a_{N+1}\mid\mathbf{a}_N)p(\mathbf{a}_N)p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)\,d\mathbf{a}_N\\
&=\int p(a_{N+1}\mid\mathbf{a}_N)p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)\,d\mathbf{a}_N
\end{aligned}
\tag{6.77}
$$

<!-- pdf-page: 336 -->

这里使用了 $p(\boldsymbol{\mathsf{t}}_N\mid a_{N+1},\mathbf{a}_N)=p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)$。利用高斯过程回归的结果（6.66）和（6.67），得到条件分布 $p(a_{N+1}\mid\mathbf{a}_N)$：

$$
p(a_{N+1}\mid\mathbf{a}_N)=\mathcal{N}(a_{N+1}\mid\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{a}_N,c-\mathbf{k}^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{k}).
\tag{6.78}
$$

因此，可以先求出后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的拉普拉斯近似，再使用两个高斯分布卷积的标准结果，来计算（6.77）中的积分。

先验 $p(\mathbf{a}_N)$ 由均值为零、协方差矩阵为 $\mathbf{C}_N$ 的高斯过程给出，而在假设数据点相互独立时，数据项为

$$
p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)=\prod_{n=1}^{N}\sigma(a_n)^{t_n}(1-\sigma(a_n))^{1-t_n}=\prod_{n=1}^{N}e^{a_nt_n}\sigma(-a_n).
\tag{6.79}
$$

随后，对 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的对数作 Taylor 展开，得到拉普拉斯近似。除了一个加性的归一化常数外，这个对数由下列量给出：

$$
\begin{aligned}
\Psi(\mathbf{a}_N)&=\ln p(\mathbf{a}_N)+\ln p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)\\
&=-\frac{1}{2}\mathbf{a}_N^{\mathrm T}\mathbf{C}_N^{-1}\mathbf{a}_N-\frac{N}{2}\ln(2\pi)-\frac{1}{2}\ln|\mathbf{C}_N|+\boldsymbol{\mathsf{t}}_N^{\mathrm T}\mathbf{a}_N\\
&\quad-\sum_{n=1}^{N}\ln(1+e^{a_n})+\mathrm{const}.
\end{aligned}
\tag{6.80}
$$

首先，需要找到后验分布的众数，这要求计算 $\Psi(\mathbf{a}_N)$ 的梯度，它为

$$
\nabla\Psi(\mathbf{a}_N)=\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N-\mathbf{C}_N^{-1}\mathbf{a}_N
\tag{6.81}
$$

其中 $\boldsymbol{\sigma}_N$ 是元素为 $\sigma(a_n)$ 的向量。不能简单地令这个梯度为零来求众数，因为 $\boldsymbol{\sigma}_N$ 非线性地依赖于 $\mathbf{a}_N$；因此，采用基于 Newton–Raphson 方法的迭代方案，由此得到迭代重加权最小二乘（IRLS）算法（4.3.3 节）。这需要 $\Psi(\mathbf{a}_N)$ 的二阶导数，而拉普拉斯近似本来也需要这些导数，它们为

$$
\nabla\nabla\Psi(\mathbf{a}_N)=-\mathbf{W}_N-\mathbf{C}_N^{-1}
\tag{6.82}
$$

其中 $\mathbf{W}_N$ 是对角矩阵，对角元素为 $\sigma(a_n)(1-\sigma(a_n))$，这里使用了 logistic sigmoid 函数的导数结果（4.88）。注意，这些对角元素位于区间 $(0,1/4)$ 内，因此 $\mathbf{W}_N$ 是正定矩阵。由于按构造 $\mathbf{C}_N$ 及其逆矩阵都是正定的，而且两个正定矩阵之和仍为正定矩阵（习题 6.24），可知 Hessian 矩阵 $\mathbf{A}=-\nabla\nabla\Psi(\mathbf{a}_N)$ 正定，因此后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 是对数凸的，只有一个众数，并且它是全局

<!-- pdf-page: 337 -->

<!-- join-previous-paragraph -->
最大值。不过，后验分布并不是高斯分布，因为 Hessian 矩阵是 $\mathbf{a}_N$ 的函数。

使用 Newton–Raphson 公式（4.92），$\mathbf{a}_N$ 的迭代更新方程为（习题 6.25）

$$
\mathbf{a}_N^{\mathrm{new}}=\mathbf{C}_N(\mathbf{I}+\mathbf{W}_N\mathbf{C}_N)^{-1}\{\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N+\mathbf{W}_N\mathbf{a}_N\}.
\tag{6.83}
$$

反复应用这些方程，直到收敛到众数，将它记为 $\mathbf{a}_N^{\star}$。在众数处，梯度 $\nabla\Psi(\mathbf{a}_N)$ 为零，因此 $\mathbf{a}_N^{\star}$ 满足

$$
\mathbf{a}_N^{\star}=\mathbf{C}_N(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N).
\tag{6.84}
$$

一旦找到后验分布的众数 $\mathbf{a}_N^{\star}$，就可以计算 Hessian 矩阵

$$
\mathbf{H}=-\nabla\nabla\Psi(\mathbf{a}_N)=\mathbf{W}_N+\mathbf{C}_N^{-1}
\tag{6.85}
$$

其中 $\mathbf{W}_N$ 的元素利用 $\mathbf{a}_N^{\star}$ 计算。这就定义了后验分布 $p(\mathbf{a}_N\mid\boldsymbol{\mathsf{t}}_N)$ 的高斯近似：

$$
q(\mathbf{a}_N)=\mathcal{N}(\mathbf{a}_N\mid\mathbf{a}_N^{\star},\mathbf{H}^{-1}).
\tag{6.86}
$$

现在可以将它与（6.78）结合，计算积分（6.77）。由于这对应于线性高斯模型，可以使用一般结果（2.115），得到（习题 6.26）

$$
\mathbb{E}[a_{N+1}\mid\boldsymbol{\mathsf{t}}_N]=\mathbf{k}^{\mathrm T}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N)
\tag{6.87}
$$

$$
\operatorname{var}[a_{N+1}\mid\boldsymbol{\mathsf{t}}_N]=c-\mathbf{k}^{\mathrm T}(\mathbf{W}_N^{-1}+\mathbf{C}_N)^{-1}\mathbf{k}.
\tag{6.88}
$$

现在，$p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 已经是高斯分布，就可以利用结果（4.153）来近似积分（6.76）。与 4.5 节的贝叶斯逻辑回归模型一样，如果只关心对应于 $p(t_{N+1}\mid\boldsymbol{\mathsf{t}}_N)=0.5$ 的决策边界，那么只需考虑均值，可以忽略方差的影响。

还需要确定协方差函数的参数 $\boldsymbol{\theta}$。一种方法是最大化似然函数 $p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})$，这需要对数似然及其梯度的表达式。如有需要，还可以加入合适的正则化项，得到带惩罚的最大似然解。似然函数定义为

$$
p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})=\int p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N)p(\mathbf{a}_N\mid\boldsymbol{\theta})\,d\mathbf{a}_N.
\tag{6.89}
$$

这个积分无法解析求出，因此再次使用拉普拉斯近似。利用结果（4.135），得到似然函数对数的如下近似：

$$
\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})=\Psi(\mathbf{a}_N^{\star})-\frac{1}{2}\ln|\mathbf{W}_N+\mathbf{C}_N^{-1}|+\frac{N}{2}\ln(2\pi)
\tag{6.90}
$$

<!-- pdf-page: 338 -->

其中 $\Psi(\mathbf{a}_N^{\star})=\ln p(\mathbf{a}_N^{\star}\mid\boldsymbol{\theta})+\ln p(\boldsymbol{\mathsf{t}}_N\mid\mathbf{a}_N^{\star})$。还需要计算 $\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})$ 关于参数向量 $\boldsymbol{\theta}$ 的梯度。注意，$\boldsymbol{\theta}$ 的变化会引起 $\mathbf{a}_N^{\star}$ 的变化，从而在梯度中产生额外的项。因此，对（6.90）关于 $\boldsymbol{\theta}$ 求导时，会得到两组项：第一组来自协方差矩阵 $\mathbf{C}_N$ 对 $\boldsymbol{\theta}$ 的依赖，其余项来自 $\mathbf{a}_N^{\star}$ 对 $\boldsymbol{\theta}$ 的依赖。

利用（6.80）以及结果（C.21）、（C.22），可以求出由对 $\boldsymbol{\theta}$ 的显式依赖产生的项：

$$
\begin{aligned}
\frac{\partial\ln p(\boldsymbol{\mathsf{t}}_N\mid\boldsymbol{\theta})}{\partial\theta_j}
&=\frac{1}{2}(\mathbf{a}_N^{\star})^{\mathrm T}\mathbf{C}_N^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_j}\mathbf{C}_N^{-1}\mathbf{a}_N^{\star}\\
&\quad-\frac{1}{2}\operatorname{Tr}\left[(\mathbf{I}+\mathbf{C}_N\mathbf{W}_N)^{-1}\mathbf{W}_N\frac{\partial\mathbf{C}_N}{\partial\theta_j}\right].
\end{aligned}
\tag{6.91}
$$

为了计算由 $\mathbf{a}_N^{\star}$ 对 $\boldsymbol{\theta}$ 的依赖所产生的项，注意拉普拉斯近似的构造保证 $\Psi(\mathbf{a}_N)$ 在 $\mathbf{a}_N=\mathbf{a}_N^{\star}$ 处的梯度为零。因此，$\Psi(\mathbf{a}_N^{\star})$ 对 $\mathbf{a}_N^{\star}$ 的依赖不会对梯度产生贡献。剩下关于 $\boldsymbol{\theta}$ 的分量 $\theta_j$ 的导数贡献为

$$
\begin{aligned}
&-\frac{1}{2}\sum_{n=1}^{N}\frac{\partial\ln|\mathbf{W}_N+\mathbf{C}_N^{-1}|}{\partial a_n^{\star}}\frac{\partial a_n^{\star}}{\partial\theta_j}\\
&\quad=-\frac{1}{2}\sum_{n=1}^{N}\left[(\mathbf{I}+\mathbf{C}_N\mathbf{W}_N)^{-1}\mathbf{C}_N\right]_{nn}\sigma_n^{\star}(1-\sigma_n^{\star})(1-2\sigma_n^{\star})\frac{\partial a_n^{\star}}{\partial\theta_j}
\end{aligned}
\tag{6.92}
$$

其中 $\sigma_n^{\star}=\sigma(a_n^{\star})$，这里再次使用了结果（C.22）和 $\mathbf{W}_N$ 的定义。对关系式（6.84）关于 $\theta_j$ 求导，就可以计算 $\mathbf{a}_N^{\star}$ 关于 $\theta_j$ 的导数，得到

$$
\frac{\partial a_n^{\star}}{\partial\theta_j}=\frac{\partial\mathbf{C}_N}{\partial\theta_j}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N)-\mathbf{C}_N\mathbf{W}_N\frac{\partial a_n^{\star}}{\partial\theta_j}.
\tag{6.93}
$$

整理得到

$$
\frac{\partial a_n^{\star}}{\partial\theta_j}=(\mathbf{I}+\mathbf{W}_N\mathbf{C}_N)^{-1}\frac{\partial\mathbf{C}_N}{\partial\theta_j}(\boldsymbol{\mathsf{t}}_N-\boldsymbol{\sigma}_N).
\tag{6.94}
$$

结合（6.91）、（6.92）和（6.94），就可以计算对数似然函数的梯度，并将它与标准非线性优化算法结合，用来确定 $\boldsymbol{\theta}$ 的值。

可以使用图 6.12 所示的合成二类数据集（附录 A），说明拉普拉斯近似在高斯过程中的应用。利用 softmax 激活函数，很容易将拉普拉斯近似扩展到涉及 $K>2$ 个类别的高斯过程（Williams and Barber, 1998）。

<!-- pdf-page: 339 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-06/b-fig-6-12.png" alt="高斯过程分类的训练数据、决策边界及两个类别的预测后验概率"><figcaption>图 6.12：使用高斯过程进行分类的示例。左图给出数据，以及真实分布的最优决策边界（绿色）和高斯过程分类器的决策边界（黑色）。右图给出蓝色、红色两个类别的预测后验概率，以及高斯过程的决策边界。</figcaption></figure>

### 6.4.7 与神经网络的联系

我们已经看到，神经网络能够表示的函数范围由隐藏单元数目 $M$ 决定；当 $M$ 足够大时，两层网络可以以任意精度近似任何给定函数。在最大似然框架中，为避免过拟合，需要将隐藏单元的数目限制在一个取决于训练集大小的水平。不过，从贝叶斯观点看，根据训练集的大小来限制网络中的参数数目并没有多少意义。

在贝叶斯神经网络中，参数向量 $\mathbf{w}$ 的先验分布与网络函数 $f(\mathbf{x},\mathbf{w})$ 相结合，会产生函数 $\mathbf{y}(\mathbf{x})$ 上的先验分布，其中 $\mathbf{y}$ 是网络输出向量。Neal（1996）证明，对于一大类 $\mathbf{w}$ 的先验分布，在 $M\to\infty$ 的极限下，神经网络生成的函数分布将趋于一个高斯过程。不过，应该注意，在这一极限下，神经网络的输出变量变得相互独立。神经网络的一项重要优点是，各输出共享隐藏单元，因此能够彼此“借用统计信息”；也就是说，与每个隐藏单元关联的权重都受到所有输出变量的影响，而不仅受到其中一个输出变量的影响。因此，在高斯过程极限下，这一性质就丢失了。

我们已经看到，高斯过程由它的协方差函数，也就是核函数确定。对于隐藏单元激活函数的两种具体选择——probit 函数和高斯函数，Williams（1998）给出了协方差的显式形式。这些核函数 $k(\mathbf{x},\mathbf{x}')$ 是非平稳的，即不能表示成差值 $\mathbf{x}-\mathbf{x}'$ 的函数。这是因为高斯权重先验以零为中心，破坏了权重空间中的平移不变性。

<!-- pdf-page: 340 -->

直接使用协方差函数，相当于隐式地对权重分布进行了边缘化。如果权重先验由超参数控制，那么这些超参数的值将决定函数分布的长度尺度；通过研究图 5.11 中隐藏单元数目有限时的例子，可以理解这一点。注意，无法解析地将超参数边缘化掉，必须借助 6.4 节讨论的那类技术。

## 习题

**6.1（⋆⋆）www** 考虑 6.1 节给出的最小二乘线性回归问题的对偶形式。证明，向量 $\mathbf{a}$ 的分量 $a_n$ 的解可以表示为向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 各元素的线性组合。将这些系数记为向量 $\mathbf{w}$，证明对偶形式的对偶，就是原先用参数向量 $\mathbf{w}$ 表示的形式。

**6.2（⋆⋆）** 本题推导感知机学习算法的对偶形式。利用感知机学习规则（4.55），证明学到的权重向量 $\mathbf{w}$ 可以写成向量 $t_n\boldsymbol{\phi}(\mathbf{x}_n)$ 的线性组合，其中 $t_n\in\{-1,+1\}$。将这个线性组合的系数记为 $\alpha_n$，推导用 $\alpha_n$ 表示的感知机学习算法和感知机预测函数。证明，特征向量 $\boldsymbol{\phi}(\mathbf{x})$ 仅以核函数 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')$ 的形式出现。

**6.3（⋆）** 最近邻分类器（2.5.2 节）将新输入向量 $\mathbf{x}$ 分到训练集中距它最近的输入向量 $\mathbf{x}_n$ 所属的类别；在最简单的情况下，距离由欧氏度量 $\|\mathbf{x}-\mathbf{x}_n\|^2$ 定义。用标量积表示这一规则，再利用核替换，给出一般非线性核下的最近邻分类器。

**6.4（⋆）** 在附录 C 中，我们给出了一个矩阵的例子，它的元素均为正，却具有负特征值，因此不是正定矩阵。找出一个具有相反性质的例子，即一个特征值均为正、但至少有一个负元素的 $2\times2$ 矩阵。

**6.5（⋆）www** 验证构造有效核的结果（6.13）和（6.14）。

**6.6（⋆）** 验证构造有效核的结果（6.15）和（6.16）。

**6.7（⋆）www** 验证构造有效核的结果（6.17）和（6.18）。

**6.8（⋆）** 验证构造有效核的结果（6.19）和（6.20）。

**6.9（⋆）** 验证构造有效核的结果（6.21）和（6.22）。

**6.10（⋆）** 证明，对于学习函数 $f(\mathbf{x})$，一个很好的核选择是 $k(\mathbf{x},\mathbf{x}')=f(\mathbf{x})f(\mathbf{x}')$；为此，证明基于这个核的线性学习机器总会找到一个与 $f(\mathbf{x})$ 成正比的解。

<!-- pdf-page: 341 -->

**6.11（⋆）** 利用展开式（6.25），再将中间的因子展开为幂级数，证明高斯核（6.23）可以表示为无穷维特征向量的内积。

**6.12（⋆⋆）www** 考虑一个给定固定集合 $D$ 的所有可能子集 $A$ 所构成的空间。证明，核函数（6.27）对应于由映射 $\boldsymbol{\phi}(A)$ 定义的 $2^{|D|}$ 维特征空间中的内积，其中 $A$ 是 $D$ 的一个子集，而以子集 $U$ 为索引的元素 $\phi_U(A)$ 为

$$
\phi_U(A)=\begin{cases}
1,&\text{若 }U\subseteq A;\\
0,&\text{否则。}
\end{cases}
\tag{6.95}
$$

这里 $U\subseteq A$ 表示 $U$ 是 $A$ 的子集，或者等于 $A$。

**6.13（⋆）** 证明，在对参数向量进行非线性变换 $\boldsymbol{\theta}\to\boldsymbol{\psi}(\boldsymbol{\theta})$ 后，由（6.33）定义的 Fisher 核保持不变，其中函数 $\boldsymbol{\psi}(\cdot)$ 可逆且可微。

**6.14（⋆）www** 对于均值为 $\boldsymbol{\mu}$、协方差 $\mathbf{S}$ 固定的高斯分布 $p(\mathbf{x}\mid\boldsymbol{\mu})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\mathbf{S})$，写出（6.33）定义的 Fisher 核的形式。

**6.15（⋆）** 考虑一个 $2\times2$ Gram 矩阵的行列式，证明正定核函数 $k(x,x')$ 满足 Cauchy–Schwartz 不等式

$$
k(x_1,x_2)^2\leqslant k(x_1,x_1)k(x_2,x_2).
\tag{6.96}
$$

**6.16（⋆⋆）** 考虑一个由参数向量 $\mathbf{w}$ 控制的参数模型，以及由输入值 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 构成的数据集和非线性特征映射 $\boldsymbol{\phi}(\mathbf{x})$。假设误差函数对 $\mathbf{w}$ 的依赖具有如下形式：

$$
J(\mathbf{w})=f(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_1),\ldots,\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_N))+g(\mathbf{w}^{\mathrm T}\mathbf{w})
\tag{6.97}
$$

其中 $g(\cdot)$ 是单调递增函数。将 $\mathbf{w}$ 写成

$$
\mathbf{w}=\sum_{n=1}^{N}\alpha_n\boldsymbol{\phi}(\mathbf{x}_n)+\mathbf{w}_{\perp}
\tag{6.98}
$$

证明，使 $J(\mathbf{w})$ 最小的 $\mathbf{w}$，是基函数 $\boldsymbol{\phi}(\mathbf{x}_n)$（$n=1,\ldots,N$）的线性组合。

**6.17（⋆⋆）www** 考虑针对输入含噪声的数据的平方和误差函数（6.39），其中 $\nu(\boldsymbol{\xi})$ 是噪声分布。利用变分法，关于函数 $y(\mathbf{x})$ 最小化这个误差函数，从而证明最优解由（6.40）形式的展开给出，其中基函数由（6.41）给出。

<!-- pdf-page: 342 -->

**6.18（⋆）** 考虑一个具有单个输入变量 $x$ 和单个目标变量 $t$ 的 Nadaraya–Watson 模型，其高斯分量具有各向同性协方差，因此协方差矩阵为 $\sigma^2\mathbf{I}$，其中 $\mathbf{I}$ 为单位矩阵。用核函数 $k(x,x_n)$ 写出条件密度 $p(t\mid x)$、条件均值 $\mathbb{E}[t\mid x]$ 和方差 $\operatorname{var}[t\mid x]$ 的表达式。

**6.19（⋆⋆）** 核回归的另一种观点，来自输入变量和目标变量都受到加性噪声污染的回归问题。假设每个目标值 $t_n$ 都像通常一样生成：在点 $\mathbf{z}_n$ 处计算函数 $y(\mathbf{z}_n)$，再加入高斯噪声。不过，无法直接观测到 $\mathbf{z}_n$ 的值，只能观测到受噪声污染的版本 $\mathbf{x}_n=\mathbf{z}_n+\boldsymbol{\xi}_n$，其中随机变量 $\boldsymbol{\xi}$ 服从某个分布 $g(\boldsymbol{\xi})$。考虑一组观测 $\{\mathbf{x}_n,t_n\}$，其中 $n=1,\ldots,N$，以及通过对输入噪声分布取平均而定义的相应平方和误差函数：

$$
E=\frac{1}{2}\sum_{n=1}^{N}\int\{y(\mathbf{x}_n-\boldsymbol{\xi}_n)-t_n\}^2g(\boldsymbol{\xi}_n)\,d\boldsymbol{\xi}_n.
\tag{6.99}
$$

利用变分法（附录 D），关于函数 $y(\mathbf{z})$ 最小化 $E$，证明 $y(\mathbf{x})$ 的最优解由（6.45）形式的 Nadaraya–Watson 核回归解给出，其核具有（6.46）的形式。

**6.20（⋆⋆）www** 验证结果（6.66）和（6.67）。

**6.21（⋆⋆）www** 考虑一个高斯过程回归模型，其核函数由一组固定的非线性基函数定义。证明，它的预测分布与 3.3.2 节针对贝叶斯线性回归模型得到的结果（3.58）相同。为此，注意两个模型的预测分布都是高斯分布，因此只需证明条件均值和方差相同。对于均值，使用矩阵恒等式（C.6）；对于方差，使用矩阵恒等式（C.7）。

**6.22（⋆⋆）** 考虑一个回归问题，具有 $N$ 个训练集输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 和 $L$ 个测试集输入向量 $\mathbf{x}_{N+1},\ldots,\mathbf{x}_{N+L}$，并假设为函数 $t(\mathbf{x})$ 定义了一个高斯过程先验。给定 $t(\mathbf{x}_1),\ldots,t(\mathbf{x}_N)$ 的值，推导 $t(\mathbf{x}_{N+1}),\ldots,t(\mathbf{x}_{N+L})$ 的联合预测分布的表达式。证明，对于其中一个测试观测 $t_j$，其中 $N+1\leqslant j\leqslant N+L$，该分布的边缘分布由通常的高斯过程回归结果（6.66）和（6.67）给出。

**6.23（⋆⋆）www** 考虑一个高斯过程回归模型，其中目标变量 $\mathbf{t}$ 的维数为 $D$。给定由输入向量 $\mathbf{x}_1,\ldots,\mathbf{x}_{N+1}$ 和相应目标观测 $\mathbf{t}_1,\ldots,\mathbf{t}_N$ 构成的训练集，写出测试输入向量 $\mathbf{x}_{N+1}$ 对应的 $\mathbf{t}_{N+1}$ 的条件分布。

**6.24（⋆）** 证明，一个对角元素满足 $0<W_{ii}<1$ 的对角矩阵 $\mathbf{W}$ 是正定矩阵。证明，两个正定矩阵之和本身也是正定矩阵。

<!-- pdf-page: 343 -->

**6.25（⋆）www** 利用 Newton–Raphson 公式（4.92），推导用于寻找高斯过程分类模型中后验分布众数 $\mathbf{a}_N^{\star}$ 的迭代更新公式（6.83）。

**6.26（⋆）** 利用结果（2.115），推导高斯过程分类模型中后验分布 $p(a_{N+1}\mid\boldsymbol{\mathsf{t}}_N)$ 的均值和方差的表达式（6.87）和（6.88）。

**6.27（⋆⋆⋆）** 推导高斯过程分类的拉普拉斯近似框架中，对数似然函数的结果（6.90）。类似地，推导对数似然梯度各项的结果（6.91）、（6.92）和（6.94）。

<!-- pdf-page: 344 -->
