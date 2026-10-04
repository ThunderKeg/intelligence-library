<!-- pdf-page: 179 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-10.png" alt="高斯基函数的等效核矩阵，以及对应三个不同输入位置的核切片"><figcaption>图 3.10：图 3.1 中高斯基函数的等效核 $k(x,x')$。右图以 $x$ 和 $x'$ 为坐标展示这个核，左边给出该矩阵在三个不同 $x$ 值处的切片。用于生成这个核的数据集包含 200 个 $x$ 值，它们在区间 $(-1,1)$ 上等间隔分布。</figcaption></figure>

### 3.3.3 等效核

线性基函数模型的后验均值解（3.53）有一种有趣的解释，它将为包括高斯过程在内的核方法奠定基础（第 6 章）。将（3.53）代入表达式（3.3），可以看到预测均值可写为

$$
y(\mathbf{x},\mathbf{m}_N)=\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})=\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}=\sum_{n=1}^{N}\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}_n)t_n
\tag{3.60}
$$

其中 $\mathbf{S}_N$ 由（3.51）定义。因此，点 $\mathbf{x}$ 处预测分布的均值是训练集目标变量 $t_n$ 的线性组合，所以可以写成

$$
y(\mathbf{x},\mathbf{m}_N)=\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)t_n
\tag{3.61}
$$

其中函数

$$
k(\mathbf{x},\mathbf{x}')=\beta\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}')
\tag{3.62}
$$

称为*平滑矩阵*（smoother matrix）或*等效核*（equivalent kernel）。像这样通过训练集目标值的线性组合来进行预测的回归函数，称为*线性平滑器*（linear smoother）。注意，等效核依赖于数据集中的输入值 $\mathbf{x}_n$，因为 $\mathbf{S}_N$ 的定义中包含这些输入值。图 3.10 展示了高斯基函数的等效核，图中对三个不同的 $x$ 值，将核函数 $k(x,x')$ 画成了 $x'$ 的函数。可以看到，这些函数都集中在 $x$ 附近，因此，$x$ 处预测分布的均值 $y(x,\mathbf{m}_N)$ 是目标值的加权组合，其中靠近 $x$ 的数据点得到的权重高于离 $x$ 较远的数据点。直观上，赋予局部证据比远处证据更大的权重是合理的。注意，这种局部性不仅适用于具有局部性的高斯基函数，也适用于非局部的多项式基函数和 sigmoid（S 形）基函数，如图 3.11 所示。

<!-- pdf-page: 180 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-11.png" alt="在 x 等于零处，多项式基函数和 sigmoid 基函数的等效核均表现出局部性"><figcaption>图 3.11：当 $x=0$ 时，将等效核 $k(x,x')$ 画成 $x'$ 的函数。左图对应图 3.1 中的多项式基函数，右图对应其中的 sigmoid 基函数。注意，虽然相应的基函数是非局部的，但这些核都是具有局部性的 $x'$ 的函数。</figcaption></figure>

考察 $y(\mathbf{x})$ 与 $y(\mathbf{x}')$ 之间的协方差，可以进一步理解等效核的作用。该协方差为

$$
\begin{aligned}
\operatorname{cov}[y(\mathbf{x}),y(\mathbf{x}')]&=\operatorname{cov}[\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{w},\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}')]\\
&=\boldsymbol{\phi}(\mathbf{x})^{\mathrm T}\mathbf{S}_N\boldsymbol{\phi}(\mathbf{x}')=\beta^{-1}k(\mathbf{x},\mathbf{x}')
\end{aligned}
\tag{3.63}
$$

这里使用了（3.49）和（3.62）。由等效核的形式可以看出，邻近位置的预测均值会高度相关，而相距较远的两个位置之间的相关性则较小。

图 3.8 所示的预测分布，使我们能够直观地看到各个位置处预测的不确定性，这种不确定性由（3.59）决定。但是，从 $\mathbf{w}$ 的后验分布中抽取样本，并像图 3.9 那样画出相应的模型函数 $y(\mathbf{x},\mathbf{w})$，则可以直观地展示后验分布中两个（或更多个）$x$ 值所对应的 $y$ 值之间的联合不确定性；这种不确定性由等效核决定。

用核函数来表述线性回归，启发了下面另一种回归方法。我们可以直接定义一个具有局部性的核，而不必先引入一组基函数来隐式地确定等效核；然后，给定观测到的训练集，就用这个核对新的输入向量 $\mathbf{x}$ 进行预测。这样就得到了一种称为*高斯过程*的实用回归（及分类）框架，我们将在 6.4 节详细讨论。

我们已经看到，有效核确定了组合训练集目标值所用的权重，从而对新的 $\mathbf{x}$ 值进行预测。可以证明，这些权重之和为 1，也就是说，对于所有 $\mathbf{x}$ 值，都有

$$
\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)=1.
\tag{3.64}
$$

这个符合直觉的结果可以用一种非严格的方式轻易证明（习题 3.14）：注意，上述求和等价于考虑这样一组目标数据的预测均值 $\widehat{y}(\mathbf{x})$，其中对所有 $n$ 都有 $t_n=1$。只要基函数线性无关、数据点的数目多于基函数的数目，并且其中一个基函数是常数（对应于偏置参数），显然就能精确拟合训练数据，因而预测均值

<!-- pdf-page: 181 -->
<!-- join-previous-paragraph -->
就是 $\widehat{y}(\mathbf{x})=1$，由此得到（3.64）。注意，核函数既可以为正，也可以为负，因此，虽然它满足一个求和约束，相应的预测却不一定是训练集目标变量的凸组合。

最后要指出，等效核（3.62）满足核函数普遍具有的一个重要性质（第 6 章），即它可以表示为非线性函数向量 $\boldsymbol{\psi}(\mathbf{x})$ 的内积形式：

$$
k(\mathbf{x},\mathbf{z})=\boldsymbol{\psi}(\mathbf{x})^{\mathrm T}\boldsymbol{\psi}(\mathbf{z})
\tag{3.65}
$$

其中 $\boldsymbol{\psi}(\mathbf{x})=\beta^{1/2}\mathbf{S}_N^{1/2}\boldsymbol{\phi}(\mathbf{x})$。

## 3.4 贝叶斯模型比较

在第 1 章中，我们着重介绍了过拟合问题，以及如何使用交叉验证来设定正则化参数的值，或在不同的候选模型之间作出选择。这里，我们从贝叶斯角度考察模型选择问题。本节将作一般性的讨论，随后在 3.5 节中，我们将看到如何将这些思想用于确定线性回归的正则化参数。

我们将会看到，对模型参数进行边缘化（求和或积分），而不是对它们的值进行点估计，就可以避免最大似然方法中的过拟合。这样，就能直接根据训练数据比较模型，而不需要验证集。这使得所有可用数据都可以用于训练，也免去了交叉验证要求对每个模型进行的多次训练。此外，这种方法还允许在训练过程中同时确定多个复杂度参数。例如，我们将在第 7 章介绍相关向量机，这是一种贝叶斯模型，每个训练数据点都有一个复杂度参数。

贝叶斯模型比较的做法，就是用概率表示模型选择的不确定性，并一致地运用概率的求和规则与乘积规则。假设要比较一组 $L$ 个模型 $\{\mathcal{M}_i\}$，其中 $i=1,\ldots,L$。这里，模型指的是观测数据 $\mathcal{D}$ 上的一个概率分布。在多项式曲线拟合问题中，该分布定义在目标值集合 $\boldsymbol{\mathsf{t}}$ 上，而输入值集合 $\mathbf{X}$ 则假定为已知。其他类型的模型会定义 $\mathbf{X}$ 与 $\boldsymbol{\mathsf{t}}$ 上的联合分布（1.5.4 节）。我们假设数据由这些模型中的某一个生成，但不确定具体是哪一个。这种不确定性通过先验概率分布 $p(\mathcal{M}_i)$ 来表示。给定训练集 $\mathcal{D}$，我们希望计算后验分布

$$
p(\mathcal{M}_i\mid\mathcal{D})\propto p(\mathcal{M}_i)p(\mathcal{D}\mid\mathcal{M}_i).
\tag{3.66}
$$

先验允许我们表达对不同模型的偏好。这里简单地假设所有模型具有相等的先验概率。值得关注的是模型证据 $p(\mathcal{D}\mid\mathcal{M}_i)$，它表示数据对

<!-- pdf-page: 182 -->
<!-- join-previous-paragraph -->
不同模型的偏好，我们马上就会更详细地考察这一项。模型证据有时也称为*边缘似然*（marginal likelihood），因为它可以看作模型空间上的似然函数，其中的参数已经被边缘化。两个模型的证据之比 $p(\mathcal{D}\mid\mathcal{M}_i)/p(\mathcal{D}\mid\mathcal{M}_j)$ 称为*贝叶斯因子*（Bayes factor；Kass and Raftery, 1995）。

一旦知道了模型的后验分布，根据求和规则与乘积规则，预测分布就为

$$
p(t\mid\mathbf{x},\mathcal{D})=\sum_{i=1}^{L}p(t\mid\mathbf{x},\mathcal{M}_i,\mathcal{D})p(\mathcal{M}_i\mid\mathcal{D}).
\tag{3.67}
$$

这是混合分布的一个例子：总体预测分布，是以各个模型的后验概率 $p(\mathcal{M}_i\mid\mathcal{D})$ 为权重，对它们各自的预测分布 $p(t\mid\mathbf{x},\mathcal{M}_i,\mathcal{D})$ 求平均得到的。例如，假设两个模型的后验概率相等，一个预测 $t=a$ 附近的窄分布，另一个预测 $t=b$ 附近的窄分布，那么总体预测分布将是一个双峰分布，峰分别位于 $t=a$ 和 $t=b$，而不是在 $t=(a+b)/2$ 处的单一模型。

对模型平均的一种简单近似，是只使用概率最大的那个模型进行预测。这称为*模型选择*。

对于由一组参数 $\mathbf{w}$ 控制的模型，依据概率的求和规则与乘积规则，模型证据为

$$
p(\mathcal{D}\mid\mathcal{M}_i)=\int p(\mathcal{D}\mid\mathbf{w},\mathcal{M}_i)p(\mathbf{w}\mid\mathcal{M}_i)\,d\mathbf{w}.
\tag{3.68}
$$

从采样的角度看（第 11 章），边缘似然可以理解为：先从先验中随机抽取模型参数，然后由该模型生成数据集 $\mathcal{D}$ 的概率。还有一点值得注意：在使用贝叶斯定理计算参数的后验分布时，证据恰好就是分母中的归一化项，因为

$$
p(\mathbf{w}\mid\mathcal{D},\mathcal{M}_i)=\frac{p(\mathcal{D}\mid\mathbf{w},\mathcal{M}_i)p(\mathbf{w}\mid\mathcal{M}_i)}{p(\mathcal{D}\mid\mathcal{M}_i)}.
\tag{3.69}
$$

对参数积分作一个简单近似，有助于理解模型证据。先考虑只有一个参数 $w$ 的模型。参数的后验分布正比于 $p(\mathcal{D}\mid w)p(w)$；为简化记号，这里略去了对模型 $\mathcal{M}_i$ 的依赖。假设后验分布在概率最大的值 $w_{\mathrm{MAP}}$ 附近有一个尖峰，宽度为 $\Delta w_{\mathrm{posterior}}$，那么就可以用被积函数的最大值乘以峰的宽度来近似积分。如果再假设先验是宽度为 $\Delta w_{\mathrm{prior}}$ 的平坦分布，即 $p(w)=1/\Delta w_{\mathrm{prior}}$，那么有

$$
p(\mathcal{D})=\int p(\mathcal{D}\mid w)p(w)\,dw\simeq p(\mathcal{D}\mid w_{\mathrm{MAP}})\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}
\tag{3.70}
$$

<!-- pdf-page: 183 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-12.png" alt="宽先验与窄后验分布示意，以及两者宽度和后验众数"><figcaption>图 3.12：如果假设参数的后验分布在其众数 $w_{\mathrm{MAP}}$ 附近具有尖峰，就可以得到模型证据的粗略近似。</figcaption><p class="figure-translation">$\Delta w_{\mathrm{posterior}}$：后验分布的宽度；$\Delta w_{\mathrm{prior}}$：先验分布的宽度；$w_{\mathrm{MAP}}$：最大后验参数值；$w$：参数。</p></figure>

于是取对数得到

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid w_{\mathrm{MAP}})+\ln\left(\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}\right).
\tag{3.71}
$$

图 3.12 展示了这一近似。第一项表示使用概率最大的参数值时对数据的拟合程度；对于平坦先验，它就对应于对数似然。第二项则根据模型的复杂度施加惩罚。由于 $\Delta w_{\mathrm{posterior}}<\Delta w_{\mathrm{prior}}$，这一项为负，而且随着比值 $\Delta w_{\mathrm{posterior}}/\Delta w_{\mathrm{prior}}$ 减小，其绝对值会增大。因此，如果后验分布中的参数需要针对数据作精细调节，惩罚项就会很大。

对于具有 $M$ 个参数的模型，可以依次对每个参数作类似近似。假设所有参数的 $\Delta w_{\mathrm{posterior}}/\Delta w_{\mathrm{prior}}$ 比值相同，则得到

$$
\ln p(\mathcal{D})\simeq\ln p(\mathcal{D}\mid\mathbf{w}_{\mathrm{MAP}})+M\ln\left(\frac{\Delta w_{\mathrm{posterior}}}{\Delta w_{\mathrm{prior}}}\right).
\tag{3.72}
$$

因此，在这个很简单的近似中，复杂度惩罚的大小随模型中可调参数的数目 $M$ 线性增长。当模型复杂度增加时，第一项通常会减小，因为更复杂的模型更能拟合数据；而第二项则由于依赖于 $M$ 而增大。由最大证据确定的最优模型复杂度，将取决于这两个相互竞争的项之间的权衡。我们将在后面基于后验分布的高斯近似，给出这一近似的更精细版本（4.4.1 节）。

考察图 3.13，可以进一步理解贝叶斯模型比较，并明白边缘似然为什么可能偏好复杂度适中的模型。这里，横轴是所有可能数据集所构成空间的一维表示，因此轴上的每一点都对应于一个特定的数据集。现在考虑复杂度依次增加的三个模型 $\mathcal{M}_1$、$\mathcal{M}_2$ 和 $\mathcal{M}_3$。设想用这些模型来生成一些示例数据集，然后考察所得数据集的分布。任意给定的

<!-- pdf-page: 184 -->
<!-- join-previous-paragraph -->
模型都可以生成多种不同的数据集，因为参数由先验概率分布决定，而且对于任何给定的参数值，目标变量都可能带有随机噪声。要从一个特定模型生成一个数据集，首先从参数的先验分布 $p(\mathbf{w})$ 中选取参数值，然后在这些参数值下从 $p(\mathcal{D}\mid\mathbf{w})$ 中对数据采样。简单模型（例如基于一次多项式的模型）的变化范围很小，因此生成的数据集彼此相当相似。于是，其分布 $p(\mathcal{D})$ 被限制在横轴上一个相对较小的区域内。相比之下，复杂模型（例如九次多项式）可以生成多种多样的数据集，所以其分布 $p(\mathcal{D})$ 分散在数据集空间的较大区域中。由于分布 $p(\mathcal{D}\mid\mathcal{M}_i)$ 都经过了归一化，可以看到，对于特定数据集 $\mathcal{D}_0$，复杂度适中的模型可能具有最大的证据。实质上，较简单的模型不能很好地拟合数据，而较复杂的模型则将预测概率分散到过于广泛的数据集上，从而只给每个数据集分配相对较小的概率。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-13.png" alt="不同复杂度模型生成数据集的分布，以及数据集 D0 对应的模型证据"><figcaption>图 3.13：三个不同复杂度模型的数据集分布示意图，其中 $\mathcal{M}_1$ 最简单，$\mathcal{M}_3$ 最复杂。注意，这些分布都经过了归一化。在这个例子中，对于观测到的特定数据集 $\mathcal{D}_0$，复杂度适中的模型 $\mathcal{M}_2$ 具有最大的证据。</figcaption><p class="figure-translation">$p(\mathcal{D})$：数据集的概率；$\mathcal{D}$：数据集；$\mathcal{D}_0$：观测到的数据集；$\mathcal{M}_1$、$\mathcal{M}_2$、$\mathcal{M}_3$：复杂度依次增加的三个模型。</p></figure>

贝叶斯模型比较框架隐含着一个假设：生成数据的真实分布包含在所考察的模型集合中。只要这一条件成立，就可以证明，贝叶斯模型比较平均而言会偏好正确模型。为此，考虑两个模型 $\mathcal{M}_1$ 和 $\mathcal{M}_2$，其中真实情况对应于 $\mathcal{M}_1$。对于一个给定的有限数据集，错误模型可能具有更大的贝叶斯因子。但是，如果按照数据集的分布对贝叶斯因子求平均，就得到如下形式的期望贝叶斯因子：

$$
\int p(\mathcal{D}\mid\mathcal{M}_1)\ln\frac{p(\mathcal{D}\mid\mathcal{M}_1)}{p(\mathcal{D}\mid\mathcal{M}_2)}\,d\mathcal{D}
\tag{3.73}
$$

这里按数据的真实分布求平均。这个量是 Kullback–Leibler 散度的一个例子（1.6.1 节），它总是为正，只有两个分布相等时才为零。因此，平均而言，贝叶斯因子总会偏好正确模型。

我们已经看到，贝叶斯框架可以避免过拟合问题，并允许仅根据训练数据来比较模型。不过，

<!-- pdf-page: 185 -->
<!-- join-previous-paragraph -->
贝叶斯方法与所有模式识别方法一样，都需要对模型的形式作出假设；如果这些假设不成立，结果就可能产生误导。特别是，从图 3.12 可以看出，模型证据可能对先验的许多方面都很敏感，例如其尾部的行为。事实上，如果先验是非正常先验，证据就没有定义。原因在于，非正常先验具有任意的缩放因子（换句话说，由于分布无法归一化，归一化系数也就没有定义）。如果先考虑一个正常先验，再取适当的极限得到非正常先验（例如，对高斯先验取方差趋于无穷大的极限），那么证据将趋于零，这可以从（3.70）和图 3.12 看出。不过，也许可以先考虑两个模型的证据之比，再取极限，从而得到有意义的答案。

因此，在实际应用中，明智的做法是留出一个独立的测试数据集，用它评估最终系统的总体性能。

## 3.5 证据近似

在线性基函数模型的完全贝叶斯处理中，我们会为超参数 $\alpha$ 和 $\beta$ 引入先验分布，并在预测时同时对这些超参数以及参数 $\mathbf{w}$ 进行边缘化。但是，虽然可以对 $\mathbf{w}$ 或超参数中的任一部分进行解析积分，要对所有这些变量完成全部边缘化，却无法解析求解。这里讨论一种近似方法：先对参数 $\mathbf{w}$ 积分，得到边缘似然函数，再通过最大化这个函数，将超参数设定为具体的值。在统计学文献中，这一框架称为*经验贝叶斯*（empirical Bayes；Bernardo and Smith, 1994; Gelman et al., 2004）、*第二类最大似然*（type 2 maximum likelihood；Berger, 1985）或*广义最大似然*（generalized maximum likelihood；Wahba, 1975）；在机器学习文献中，它也称为*证据近似*（evidence approximation；Gull, 1989; MacKay, 1992a）。

如果在 $\alpha$ 和 $\beta$ 上引入超先验，那么对 $\mathbf{w}$、$\alpha$ 和 $\beta$ 进行边缘化，就得到预测分布

$$
p(t\mid\boldsymbol{\mathsf{t}})=\iiint p(t\mid\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\alpha,\beta)p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})\,d\mathbf{w}\,d\alpha\,d\beta
\tag{3.74}
$$

其中 $p(t\mid\mathbf{w},\beta)$ 由（3.8）给出，$p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\alpha,\beta)$ 由（3.49）给出，$\mathbf{m}_N$ 和 $\mathbf{S}_N$ 则分别由（3.53）和（3.54）定义。为了简化记号，这里略去了对输入变量 $\mathbf{x}$ 的依赖。如果后验分布 $p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})$ 在 $\widehat{\alpha}$ 和 $\widehat{\beta}$ 附近有尖峰，那么只需将 $\alpha$ 和 $\beta$ 固定为 $\widehat{\alpha}$ 和 $\widehat{\beta}$，再对 $\mathbf{w}$ 进行边缘化，就可得到预测分布，即

$$
p(t\mid\boldsymbol{\mathsf{t}})\simeq p(t\mid\boldsymbol{\mathsf{t}},\widehat{\alpha},\widehat{\beta})=\int p(t\mid\mathbf{w},\widehat{\beta})p(\mathbf{w}\mid\boldsymbol{\mathsf{t}},\widehat{\alpha},\widehat{\beta})\,d\mathbf{w}.
\tag{3.75}
$$

<!-- pdf-page: 186 -->

根据贝叶斯定理，$\alpha$ 和 $\beta$ 的后验分布为

$$
p(\alpha,\beta\mid\boldsymbol{\mathsf{t}})\propto p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)p(\alpha,\beta).
\tag{3.76}
$$

如果先验比较平坦，那么在证据框架中，$\widehat{\alpha}$ 和 $\widehat{\beta}$ 的值就通过最大化边缘似然函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 来确定。下面先计算线性基函数模型的边缘似然，再寻找其最大值。这样，仅使用训练数据就能确定这些超参数，而不必借助交叉验证。回忆一下，比值 $\alpha/\beta$ 的作用类似于正则化参数。

顺便指出，如果为 $\alpha$ 和 $\beta$ 定义共轭的伽马先验分布，那么（3.74）中对这些超参数的边缘化就可以解析完成，并得到 $\mathbf{w}$ 上的 Student $t$ 分布（见 2.3.7 节）。虽然此后对 $\mathbf{w}$ 的积分已无法解析求解，但人们可能会想到，对这个积分作近似，例如使用 4.4 节讨论的拉普拉斯近似，或许能够得到证据框架的一种实用替代方法（Buntine and Weigend, 1991）。拉普拉斯近似是在后验分布的众数处构造局部高斯近似。不过，将被积函数看作 $\mathbf{w}$ 的函数时，其峰通常存在很强的偏斜，因此拉普拉斯近似无法覆盖大部分概率质量，所得结果也就差于最大化证据的方法（MacKay, 1999）。

回到证据框架，可以用两种方法最大化对数证据。一种是解析计算证据函数，再令其导数为零，从而得到 $\alpha$ 和 $\beta$ 的重新估计方程；我们将在 3.5.2 节采用这种方法。另一种则使用*期望最大化*（expectation maximization，EM）算法。我们将在 9.3.4 节讨论这一算法，并证明这两种方法会收敛到相同的解。

### 3.5.1 计算证据函数

边缘似然函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 是对权重参数 $\mathbf{w}$ 积分得到的，即

$$
p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)p(\mathbf{w}\mid\alpha)\,d\mathbf{w}.
\tag{3.77}
$$

计算这一积分的一种方法，是再次利用线性高斯模型中关于条件分布的结果（2.115）（习题 3.16）。这里改用另一种方法：对指数中的表达式配方，再利用高斯分布归一化系数的标准形式来计算积分。

由（3.11）、（3.12）和（3.52），可以将证据函数写为（习题 3.17）

$$
p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\left(\frac{\beta}{2\pi}\right)^{N/2}\left(\frac{\alpha}{2\pi}\right)^{M/2}\int\exp\{-E(\mathbf{w})\}\,d\mathbf{w}
\tag{3.78}
$$

<!-- pdf-page: 187 -->

其中 $M$ 是 $\mathbf{w}$ 的维数，并且定义

$$
\begin{aligned}
E(\mathbf{w})&=\beta E_D(\mathbf{w})+\alpha E_W(\mathbf{w})\\
&=\frac{\beta}{2}\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{w}\|^2+\frac{\alpha}{2}\mathbf{w}^{\mathrm T}\mathbf{w}.
\end{aligned}
\tag{3.79}
$$

可以看出，除了一个常数比例因子外，（3.79）就是正则化的平方和误差函数（3.27）。现在对 $\mathbf{w}$ 配方，得到（习题 3.18）

$$
E(\mathbf{w})=E(\mathbf{m}_N)+\frac{1}{2}(\mathbf{w}-\mathbf{m}_N)^{\mathrm T}\mathbf{A}(\mathbf{w}-\mathbf{m}_N)
\tag{3.80}
$$

其中引入了

$$
\mathbf{A}=\alpha\mathbf{I}+\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}
\tag{3.81}
$$

以及

$$
E(\mathbf{m}_N)=\frac{\beta}{2}\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}_N\|^2+\frac{\alpha}{2}\mathbf{m}_N^{\mathrm T}\mathbf{m}_N.
\tag{3.82}
$$

注意，$\mathbf{A}$ 对应于误差函数的二阶导数矩阵

$$
\mathbf{A}=\nabla\nabla E(\mathbf{w})
\tag{3.83}
$$

称为*Hessian 矩阵*。这里还定义了 $\mathbf{m}_N$：

$$
\mathbf{m}_N=\beta\mathbf{A}^{-1}\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\mathsf{t}}.
\tag{3.84}
$$

由（3.54）可知，$\mathbf{A}=\mathbf{S}_N^{-1}$，因此（3.84）与前面的定义（3.53）等价，所以它表示后验分布的均值。

现在，只需利用多元高斯分布归一化系数的标准结果，就可以计算对 $\mathbf{w}$ 的积分，得到（习题 3.19）

$$
\begin{aligned}
\int\exp\{-E(\mathbf{w})\}\,d\mathbf{w}
&=\exp\{-E(\mathbf{m}_N)\}\int\exp\left\{-\frac{1}{2}(\mathbf{w}-\mathbf{m}_N)^{\mathrm T}\mathbf{A}(\mathbf{w}-\mathbf{m}_N)\right\}\,d\mathbf{w}\\
&=\exp\{-E(\mathbf{m}_N)\}(2\pi)^{M/2}|\mathbf{A}|^{-1/2}.
\end{aligned}
\tag{3.85}
$$

利用（3.78），就可以将边缘似然的对数写为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)=\frac{M}{2}\ln\alpha+\frac{N}{2}\ln\beta-E(\mathbf{m}_N)-\frac{1}{2}\ln|\mathbf{A}|-\frac{N}{2}\ln(2\pi)
\tag{3.86}
$$

这就是所需的证据函数表达式。

回到多项式回归问题，可以将模型证据画成多项式次数的函数，如图 3.14 所示。这里假设先验具有（1.65）的形式，并将参数 $\alpha$ 固定为 $\alpha=5\times10^{-3}$。这张图的形状很有启发性。回顾图 1.4 可以看到，$M=0$ 的多项式对数据的拟合很差，因此证据的值也

<!-- pdf-page: 188 -->
<!-- join-previous-paragraph -->
相对较低。改用 $M=1$ 的多项式后，数据拟合有了很大改善，因而证据明显提高。不过，从 $M=1$ 增至 $M=2$ 时，数据拟合只得到很微小的改善，因为生成数据的底层正弦函数是奇函数，所以其多项式展开中没有偶数次项。事实上，图 1.5 表明，从 $M=1$ 增至 $M=2$ 时，残余的数据误差只略有下降。由于这个更丰富的模型受到更大的复杂度惩罚，从 $M=1$ 增至 $M=2$ 时，证据实际上反而降低。增至 $M=3$ 时，数据拟合又得到明显改善，如图 1.4 所示，因此证据再次增加，达到所有这些多项式中的最大值。继续增大 $M$，只能带来数据拟合上的小幅改善，却会受到越来越大的复杂度惩罚，综合结果就是证据值下降。再看图 1.5，可见泛化误差在 $M=3$ 到 $M=8$ 之间大致保持不变，仅根据这张图很难在这些模型之间作出选择。不过，证据值明确偏好 $M=3$，因为这是能够很好解释观测数据的最简单模型。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-14.png" alt="多项式回归的模型证据随次数变化，在三次时最大"><figcaption>图 3.14：多项式回归模型的模型证据随次数 $M$ 的变化。图中显示，证据偏好 $M=3$ 的模型。</figcaption><p class="figure-translation">$M$：多项式的次数。</p></figure>

### 3.5.2 最大化证据函数

先考虑如何关于 $\alpha$ 最大化 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$。为此，首先定义下列特征向量方程：

$$
\left(\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}\right)\mathbf{u}_i=\lambda_i\mathbf{u}_i.
\tag{3.87}
$$

由（3.81）可知，$\mathbf{A}$ 的特征值为 $\alpha+\lambda_i$。现在考虑（3.86）中含有 $\ln|\mathbf{A}|$ 的项对 $\alpha$ 的导数。有

$$
\frac{d}{d\alpha}\ln|\mathbf{A}|=\frac{d}{d\alpha}\ln\prod_i(\lambda_i+\alpha)=\frac{d}{d\alpha}\sum_i\ln(\lambda_i+\alpha)=\sum_i\frac{1}{\lambda_i+\alpha}.
\tag{3.88}
$$

因此，（3.86）关于 $\alpha$ 的驻点满足

$$
0=\frac{M}{2\alpha}-\frac{1}{2}\mathbf{m}_N^{\mathrm T}\mathbf{m}_N-\frac{1}{2}\sum_i\frac{1}{\lambda_i+\alpha}.
\tag{3.89}
$$

<!-- pdf-page: 189 -->

两边乘以 $2\alpha$ 并整理，得到

$$
\alpha\mathbf{m}_N^{\mathrm T}\mathbf{m}_N=M-\alpha\sum_i\frac{1}{\lambda_i+\alpha}=\gamma.
\tag{3.90}
$$

由于对 $i$ 的求和中有 $M$ 项，$\gamma$ 可以写为

$$
\gamma=\sum_i\frac{\lambda_i}{\alpha+\lambda_i}.
\tag{3.91}
$$

稍后将讨论 $\gamma$ 的含义。由（3.90）可见，使边缘似然最大的 $\alpha$ 值满足（习题 3.20）

$$
\alpha=\frac{\gamma}{\mathbf{m}_N^{\mathrm T}\mathbf{m}_N}.
\tag{3.92}
$$

注意，这是 $\alpha$ 的隐式解，不仅因为 $\gamma$ 依赖于 $\alpha$，还因为后验分布的众数 $\mathbf{m}_N$ 本身也依赖于 $\alpha$ 的选择。因此，我们采用迭代过程：首先选择 $\alpha$ 的初始值，用它求出（3.53）给出的 $\mathbf{m}_N$，并计算（3.91）给出的 $\gamma$。再将这些值代入（3.92），重新估计 $\alpha$，反复进行直至收敛。注意，由于矩阵 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 是固定的，可以在开始时只计算一次它的特征值，然后将这些特征值乘以 $\beta$，就得到 $\lambda_i$。

需要强调，$\alpha$ 的值完全是根据训练数据确定的。与最大似然方法不同，这里不需要独立的数据集来优化模型复杂度。

同样，也可以关于 $\beta$ 最大化对数边缘似然（3.86）。为此，注意（3.87）定义的特征值 $\lambda_i$ 正比于 $\beta$，因此 $d\lambda_i/d\beta=\lambda_i/\beta$，于是

$$
\frac{d}{d\beta}\ln|\mathbf{A}|=\frac{d}{d\beta}\sum_i\ln(\lambda_i+\alpha)=\frac{1}{\beta}\sum_i\frac{\lambda_i}{\lambda_i+\alpha}=\frac{\gamma}{\beta}.
\tag{3.93}
$$

因此，边缘似然的驻点满足

$$
0=\frac{N}{2\beta}-\frac{1}{2}\sum_{n=1}^{N}\left\{t_n-\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2-\frac{\gamma}{2\beta}
\tag{3.94}
$$

整理后得到（习题 3.22）

$$
\frac{1}{\beta}=\frac{1}{N-\gamma}\sum_{n=1}^{N}\left\{t_n-\mathbf{m}_N^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2.
\tag{3.95}
$$

这仍然是 $\beta$ 的隐式解。可以先选取 $\beta$ 的初值，用它计算 $\mathbf{m}_N$ 和 $\gamma$，再利用（3.95）重新估计 $\beta$，重复这一过程直至收敛。如果 $\alpha$ 和 $\beta$ 都要根据数据确定，则每次更新 $\gamma$ 后，可以一并重新估计它们的值。

<!-- pdf-page: 190 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-15.png" alt="似然与先验的等高线，两个特征方向上最大后验解所受约束不同"><figcaption>图 3.15：似然函数（红色）和先验（绿色）的等高线。参数空间中的坐标轴经过旋转，与 Hessian 矩阵的特征向量 $\mathbf{u}_i$ 对齐。当 $\alpha=0$ 时，后验的众数由最大似然解 $\mathbf{w}_{\mathrm{ML}}$ 给出；当 $\alpha$ 非零时，众数位于 $\mathbf{w}_{\mathrm{MAP}}=\mathbf{m}_N$。在 $w_1$ 方向上，（3.87）定义的特征值 $\lambda_1$ 与 $\alpha$ 相比较小，因此 $\lambda_1/(\lambda_1+\alpha)$ 接近于零，相应的 $w_1$ 的 MAP 值也接近于零。相比之下，在 $w_2$ 方向上，特征值 $\lambda_2$ 与 $\alpha$ 相比较大，因此 $\lambda_2/(\lambda_2+\alpha)$ 接近于 1，而 $w_2$ 的 MAP 值接近其最大似然值。</figcaption><p class="figure-translation">$w_1$、$w_2$：参数坐标；$\mathbf{u}_1$、$\mathbf{u}_2$：特征向量；$\mathbf{w}_{\mathrm{MAP}}$：最大后验解；$\mathbf{w}_{\mathrm{ML}}$：最大似然解。</p></figure>

### 3.5.3 参数的有效数目

结果（3.92）有一个很简洁的解释（MacKay, 1992a），有助于理解 $\alpha$ 的贝叶斯解。为此，考虑图 3.15 所示的似然函数和先验的等高线。这里隐式地将参数空间的坐标轴作了旋转，使它们与（3.87）定义的特征向量 $\mathbf{u}_i$ 对齐。这样，似然函数的等高线就成为与坐标轴对齐的椭圆。特征值 $\lambda_i$ 衡量似然函数的曲率，因此，在图 3.15 中，特征值 $\lambda_1$ 比 $\lambda_2$ 小（因为曲率较小，对应于似然函数的等高线沿该方向拉得更长）。由于 $\beta\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 是正定矩阵，其特征值为正，所以比值 $\lambda_i/(\lambda_i+\alpha)$ 位于 0 与 1 之间。因此，（3.91）定义的 $\gamma$ 位于 $0\leqslant\gamma\leqslant M$ 的范围内。对于 $\lambda_i\gg\alpha$ 的方向，相应的参数 $w_i$ 接近其最大似然值，而比值 $\lambda_i/(\lambda_i+\alpha)$ 接近 1。这些参数称为*充分确定的*（well determined）参数，因为它们的值受到数据的严格约束。相反，对于 $\lambda_i\ll\alpha$ 的方向，相应的参数 $w_i$ 接近于零，比值 $\lambda_i/(\lambda_i+\alpha)$ 也接近于零。在这些方向上，似然函数对参数值相对不敏感，因此先验将该参数设定为较小的值。所以，（3.91）定义的 $\gamma$ 衡量的是充分确定的参数的有效总数。

将重新估计 $\beta$ 的结果（3.95）与相应的最大似然结果（3.21）作比较，可以更深入地理解它。两个公式都将方差（即精度的倒数）表示为目标值与模型预测之差的平方的平均值。不过，两者的区别在于，最大似然结果分母中的数据点数 $N$，在贝叶斯结果中被替换为 $N-\gamma$。回忆（1.56），对于

<!-- pdf-page: 191 -->
<!-- join-previous-paragraph -->
单个变量 $x$ 上的高斯分布，方差的最大似然估计为

$$
\sigma_{\mathrm{ML}}^2=\frac{1}{N}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2
\tag{3.96}
$$

而且这一估计是有偏的，因为均值的最大似然解 $\mu_{\mathrm{ML}}$ 拟合了数据中的一部分噪声。这实际上消耗了模型中的一个自由度。相应的无偏估计由（1.59）给出，形式为

$$
\sigma_{\mathrm{MAP}}^2=\frac{1}{N-1}\sum_{n=1}^{N}(x_n-\mu_{\mathrm{ML}})^2.
\tag{3.97}
$$

我们将在 10.1.3 节看到，对未知均值进行边缘化的贝叶斯处理可以得到这一结果。贝叶斯结果分母中的因子 $N-1$ 考虑了拟合均值已使用一个自由度这一事实，从而消除了最大似然估计的偏差。现在考虑线性回归模型的相应结果。目标分布的均值由函数 $\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})$ 给出，其中包含 $M$ 个参数。不过，这些参数并非全都由数据调节。由数据确定的参数的有效数目为 $\gamma$，其余 $M-\gamma$ 个参数则由先验设为较小的值。这体现为方差的贝叶斯结果在分母中具有因子 $N-\gamma$，从而修正了最大似然结果的偏差。

我们可以用 1.1 节的正弦合成数据集，以及包含 9 个基函数的高斯基函数模型，来说明如何用证据框架设定超参数。计入偏置后，模型的参数总数为 $M=10$。这里，为了便于展示，将 $\beta$ 设为其真实值 11.1，再使用证据框架确定 $\alpha$，如图 3.16 所示。

将各个参数画成参数有效数目 $\gamma$ 的函数，还可以看到参数 $\alpha$ 如何控制参数 $\{w_i\}$ 的大小，如图 3.17 所示。

考虑 $N\gg M$ 的极限情形，此时数据点的数目远大于参数的数目。由（3.87）可知，所有参数都能由数据充分确定，因为 $\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi}$ 中隐含了对数据点的求和，所以特征值 $\lambda_i$ 会随数据集的增大而增大。在这种情况下，$\gamma=M$，而 $\alpha$ 和 $\beta$ 的重新估计方程变为

$$
\alpha=\frac{M}{2E_W(\mathbf{m}_N)}
\tag{3.98}
$$

$$
\beta=\frac{N}{2E_D(\mathbf{m}_N)}
\tag{3.99}
$$

其中 $E_W$ 和 $E_D$ 分别由（3.25）和（3.26）定义。这些结果可以作为完整证据重新估计公式的一种易于计算的近似，

<!-- pdf-page: 192 -->
<!-- join-previous-paragraph -->
因为它们不需要计算 Hessian 矩阵的特征值谱。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-16.png" alt="证据近似确定超参数的交点、对数证据的峰值与测试集误差的比较"><figcaption>图 3.16：左图针对正弦合成数据集，画出了 $\gamma$（红色曲线）和 $2\alpha E_W(\mathbf{m}_N)$（蓝色曲线）随 $\ln\alpha$ 的变化。两条曲线的交点确定了证据方法给出的最优 $\alpha$ 值。右图给出了相应的对数证据 $\ln p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 随 $\ln\alpha$ 的变化（红色曲线），可以看到其峰值与左图中两条曲线的交点相对应。图中还给出了测试集误差（蓝色曲线），表明证据的最大值位于最佳泛化性能的位置附近。</figcaption><p class="figure-translation">$\ln\alpha$：超参数 $\alpha$ 的自然对数。</p></figure>

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-03/b-fig-3-17.png" alt="高斯基函数模型的十个参数随参数有效数目变化的曲线"><figcaption>图 3.17：高斯基函数模型中的 10 个参数 $w_i$ 随参数有效数目 $\gamma$ 的变化。超参数 $\alpha$ 在 $0\leqslant\alpha\leqslant\infty$ 范围内变化，使 $\gamma$ 在 $0\leqslant\gamma\leqslant M$ 范围内变化。</figcaption><p class="figure-translation">$w_i$：第 $i$ 个权重参数；$\gamma$：参数的有效数目；曲线旁的 0 至 9 表示参数的下标。</p></figure>

## 3.6 固定基函数的局限性

本章始终关注由固定的非线性基函数的线性组合构成的模型。我们已经看到，对参数的线性假设带来了一系列有用的性质，包括最小二乘问题的闭式解，以及可以求解的贝叶斯处理。此外，只要适当地选择基函数，就可以对输入变量到目标值的映射中的任意非线性

<!-- pdf-page: 193 -->
<!-- join-previous-paragraph -->
进行建模。下一章中，我们将研究用于分类的一类类似模型。

因此，这些线性模型似乎构成了解决模式识别问题的通用框架。遗憾的是，线性模型存在一些明显的缺点，所以在后面的章节中，我们会转而讨论更复杂的模型，例如支持向量机和神经网络。

困难来源于这样一个假设：在观测训练数据集之前，基函数 $\phi_j(\mathbf{x})$ 已经固定。这是 1.4 节所讨论的维数灾难的一种表现。其结果是，基函数的数目需要随输入空间的维数 $D$ 快速增长，而且往往是指数增长。

好在真实数据集具有两个性质，可以用来缓解这一问题。首先，由于输入变量之间存在很强的相关性，数据向量 $\{\mathbf{x}_n\}$ 通常位于某个非线性流形附近，而该流形的内在维数低于输入空间的维数。第 12 章讨论手写数字图像时，我们将看到一个例子。如果使用具有局部性的基函数，可以让它们只分布在输入空间中有数据的区域。径向基函数网络，以及支持向量机和相关向量机，都采用了这种方法。神经网络模型使用具有 sigmoid 非线性的自适应基函数，可以调节参数，使基函数发生变化的输入空间区域与数据流形相对应。第二个性质是，目标变量可能仅对数据流形中少数几个可能方向有显著依赖。神经网络可以通过选择基函数所响应的输入空间方向来利用这一性质。

## 习题

**3.1（⋆）www** 证明，双曲正切函数 $\tanh$ 与 logistic sigmoid 函数（3.6）之间存在关系

$$
\tanh(a)=2\sigma(2a)-1.
\tag{3.100}
$$

由此证明，具有如下形式的 logistic sigmoid 函数的一般线性组合

$$
y(x,\mathbf{w})=w_0+\sum_{j=1}^{M}w_j\sigma\left(\frac{x-\mu_j}{s}\right)
\tag{3.101}
$$

等价于如下形式的 $\tanh$ 函数的线性组合

$$
y(x,\mathbf{u})=u_0+\sum_{j=1}^{M}u_j\tanh\left(\frac{x-\mu_j}{s}\right)
\tag{3.102}
$$

并求出新参数 $\{u_1,\ldots,u_M\}$ 与原参数 $\{w_1,\ldots,w_M\}$ 之间的关系式。

<!-- pdf-page: 194 -->

**3.2（⋆⋆）** 证明，矩阵

$$
\boldsymbol{\Phi}(\boldsymbol{\Phi}^{\mathrm T}\boldsymbol{\Phi})^{-1}\boldsymbol{\Phi}^{\mathrm T}
\tag{3.103}
$$

会将任意向量 $\mathbf{v}$ 投影到 $\boldsymbol{\Phi}$ 的列所张成的空间。利用这一结果，证明最小二乘解（3.15）对应于将向量 $\boldsymbol{\mathsf{t}}$ 正交投影到流形 $\mathcal{S}$ 上，如图 3.2 所示。

**3.3（⋆）** 考虑一个数据集，其中每个数据点 $t_n$ 都对应于一个权重因子 $r_n>0$，从而平方和误差函数变为

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}r_n\left\{t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right\}^2.
\tag{3.104}
$$

求出使该误差函数最小的解 $\mathbf{w}^{\star}$ 的表达式。从两个角度分别解释这个加权平方和误差函数：（i）依赖于数据的噪声方差；（ii）重复的数据点。

**3.4（⋆）www** 考虑如下形式的线性模型

$$
y(\mathbf{x},\mathbf{w})=w_0+\sum_{i=1}^{D}w_ix_i
\tag{3.105}
$$

以及如下形式的平方和误差函数

$$
E_D(\mathbf{w})=\frac{1}{2}\sum_{n=1}^{N}\{y(\mathbf{x}_n,\mathbf{w})-t_n\}^2.
\tag{3.106}
$$

现在假设，向每个输入变量 $x_i$ 独立地加入均值为零、方差为 $\sigma^2$ 的高斯噪声 $\epsilon_i$。利用 $\mathbb{E}[\epsilon_i]=0$ 和 $\mathbb{E}[\epsilon_i\epsilon_j]=\delta_{ij}\sigma^2$，证明：最小化对噪声分布取平均后的 $E_D$，等价于最小化无噪声输入变量对应的平方和误差，加上一个权重衰减正则化项，其中正则化项不包含偏置参数 $w_0$。

**3.5（⋆）www** 使用附录 E 中讨论的拉格朗日乘数法，证明：最小化正则化误差函数（3.29），等价于在约束（3.30）下最小化未正则化的平方和误差（3.12）。讨论参数 $\eta$ 与 $\lambda$ 之间的关系。

**3.6（⋆）www** 考虑以多维目标变量 $\mathbf{t}$ 为输出的线性基函数回归模型，目标变量具有如下形式的高斯分布：

$$
p(\mathbf{t}\mid\mathbf{W},\boldsymbol{\Sigma})=\mathcal{N}(\mathbf{t}\mid\mathbf{y}(\mathbf{x},\mathbf{W}),\boldsymbol{\Sigma})
\tag{3.107}
$$

其中

$$
\mathbf{y}(\mathbf{x},\mathbf{W})=\mathbf{W}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x})
\tag{3.108}
$$

<!-- pdf-page: 195 -->

此外，训练数据集由输入基向量 $\boldsymbol{\phi}(\mathbf{x}_n)$ 及其对应的目标向量 $\mathbf{t}_n$ 构成，其中 $n=1,\ldots,N$。证明，参数矩阵 $\mathbf{W}$ 的最大似然解 $\mathbf{W}_{\mathrm{ML}}$ 的每一列都由形如（3.15）的表达式给出，而（3.15）是各向同性噪声分布下的解。注意，这一结果与协方差矩阵 $\boldsymbol{\Sigma}$ 无关。证明，$\boldsymbol{\Sigma}$ 的最大似然解为

$$
\boldsymbol{\Sigma}=\frac{1}{N}\sum_{n=1}^{N}\left(\mathbf{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right)\left(\mathbf{t}_n-\mathbf{W}_{\mathrm{ML}}^{\mathrm T}\boldsymbol{\phi}(\mathbf{x}_n)\right)^{\mathrm T}.
\tag{3.109}
$$

**3.7（⋆）** 利用配方法，验证线性基函数模型中参数 $\mathbf{w}$ 的后验分布的结果（3.49），其中 $\mathbf{m}_N$ 和 $\mathbf{S}_N$ 分别由（3.50）和（3.51）定义。

**3.8（⋆⋆）www** 考虑 3.1 节的线性基函数模型，假设已经观测到 $N$ 个数据点，因此 $\mathbf{w}$ 的后验分布由（3.49）给出。这个后验可以看作下一次观测的先验。考虑额外的一个数据点 $(\mathbf{x}_{N+1},t_{N+1})$，通过对指数中的表达式配方，证明所得后验分布仍由（3.49）给出，只需将 $\mathbf{S}_N$ 替换为 $\mathbf{S}_{N+1}$，将 $\mathbf{m}_N$ 替换为 $\mathbf{m}_{N+1}$。

**3.9（⋆⋆）** 重做上一题，但不手动配方，而是利用（2.116）给出的线性高斯模型的一般结果。

**3.10（⋆⋆）www** 利用结果（2.115）计算（3.57）中的积分，验证贝叶斯线性回归模型的预测分布由（3.58）给出，其中依赖于输入的方差由（3.59）给出。

**3.11（⋆⋆）** 我们已经看到，随着数据集增大，模型参数的后验分布所具有的不确定性会减小。利用矩阵恒等式（附录 C）

$$
\left(\mathbf{M}+\mathbf{v}\mathbf{v}^{\mathrm T}\right)^{-1}=\mathbf{M}^{-1}-\frac{(\mathbf{M}^{-1}\mathbf{v})(\mathbf{v}^{\mathrm T}\mathbf{M}^{-1})}{1+\mathbf{v}^{\mathrm T}\mathbf{M}^{-1}\mathbf{v}}
\tag{3.110}
$$

证明，（3.59）给出的线性回归函数的不确定性 $\sigma_N^2(\mathbf{x})$ 满足

$$
\sigma_{N+1}^2(\mathbf{x})\leqslant\sigma_N^2(\mathbf{x}).
\tag{3.111}
$$

**3.12（⋆⋆）** 我们在 2.3.6 节看到，均值与精度（方差的倒数）均未知的高斯分布，其共轭先验是正态-伽马分布。对于线性回归模型的条件高斯分布 $p(t\mid\mathbf{x},\mathbf{w},\beta)$，这一性质同样成立。如果考虑似然函数（3.10），那么 $\mathbf{w}$ 和 $\beta$ 的共轭先验为

$$
p(\mathbf{w},\beta)=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\beta^{-1}\mathbf{S}_0)\operatorname{Gam}(\beta\mid a_0,b_0).
\tag{3.112}
$$

<!-- pdf-page: 196 -->

证明，相应的后验分布具有相同的函数形式，即

$$
p(\mathbf{w},\beta\mid\boldsymbol{\mathsf{t}})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\beta^{-1}\mathbf{S}_N)\operatorname{Gam}(\beta\mid a_N,b_N)
\tag{3.113}
$$

并求出后验参数 $\mathbf{m}_N$、$\mathbf{S}_N$、$a_N$ 和 $b_N$ 的表达式。

**3.13（⋆⋆）** 证明，习题 3.12 所讨论模型的预测分布 $p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}})$ 是如下形式的 Student $t$ 分布：

$$
p(t\mid\mathbf{x},\boldsymbol{\mathsf{t}})=\operatorname{St}(t\mid\mu,\lambda,\nu)
\tag{3.114}
$$

并求出 $\mu$、$\lambda$ 和 $\nu$ 的表达式。

**3.14（⋆⋆）** 本题更详细地考察（3.62）定义的等效核的性质，其中 $\mathbf{S}_N$ 由（3.54）定义。假设基函数 $\phi_j(\mathbf{x})$ 线性无关，而且数据点数目 $N$ 大于基函数数目 $M$。此外，设其中一个基函数为常数，例如 $\phi_0(\mathbf{x})=1$。通过对这些基函数取适当的线性组合，可以构造一组新的基函数 $\psi_j(\mathbf{x})$，它们张成同一空间，但满足标准正交条件，即

$$
\sum_{n=1}^{N}\psi_j(\mathbf{x}_n)\psi_k(\mathbf{x}_n)=I_{jk}
\tag{3.115}
$$

其中，$j=k$ 时 $I_{jk}$ 定义为 1，否则为 0，并且取 $\psi_0(\mathbf{x})=1$。证明，当 $\alpha=0$ 时，等效核可以写成 $k(\mathbf{x},\mathbf{x}')=\boldsymbol{\psi}(\mathbf{x})^{\mathrm T}\boldsymbol{\psi}(\mathbf{x}')$，其中 $\boldsymbol{\psi}=(\psi_1,\ldots,\psi_M)^{\mathrm T}$。利用这一结果，证明该核满足求和约束

$$
\sum_{n=1}^{N}k(\mathbf{x},\mathbf{x}_n)=1.
\tag{3.116}
$$

**3.15（⋆）www** 考虑一个用于回归的线性基函数模型，其中参数 $\alpha$ 和 $\beta$ 通过证据框架设定。证明，（3.82）定义的函数 $E(\mathbf{m}_N)$ 满足关系 $2E(\mathbf{m}_N)=N$。

**3.16（⋆⋆）** 利用（2.115）直接计算积分（3.77），推导线性回归模型的对数证据函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$ 的结果（3.86）。

**3.17（⋆）** 证明，贝叶斯线性回归模型的证据函数可以写成（3.78）的形式，其中 $E(\mathbf{w})$ 由（3.79）定义。

**3.18（⋆⋆）www** 对 $\mathbf{w}$ 配方，证明贝叶斯线性回归中的误差函数（3.79）可以写成（3.80）的形式。

**3.19（⋆⋆）** 证明，对贝叶斯线性回归模型中的 $\mathbf{w}$ 积分可得到结果（3.85）。由此证明，对数边缘似然由（3.86）给出。

<!-- pdf-page: 197 -->

**3.20（⋆⋆）www** 从（3.86）出发，逐步验证：关于 $\alpha$ 最大化对数边缘似然函数（3.86），会得到重新估计方程（3.92）。

**3.21（⋆⋆）** 在证据框架中推导 $\alpha$ 的最优值（3.92），还有一种方法，即利用恒等式

$$
\frac{d}{d\alpha}\ln|\mathbf{A}|=\operatorname{Tr}\left(\mathbf{A}^{-1}\frac{d}{d\alpha}\mathbf{A}\right).
\tag{3.117}
$$

考虑实对称矩阵 $\mathbf{A}$ 的特征值展开，并利用以特征值表示 $\mathbf{A}$ 的行列式与迹的标准结果（附录 C），证明这一恒等式。再利用（3.117），从（3.86）推导（3.92）。

**3.22（⋆⋆）** 从（3.86）出发，逐步验证：关于 $\beta$ 最大化对数边缘似然函数（3.86），会得到重新估计方程（3.95）。

**3.23（⋆⋆）www** 先对 $\mathbf{w}$ 边缘化，再对 $\beta$ 边缘化，证明习题 3.12 所描述模型的数据边缘概率，也就是模型证据，为

$$
p(\boldsymbol{\mathsf{t}})=\frac{1}{(2\pi)^{N/2}}\frac{b_0^{a_0}}{b_N^{a_N}}\frac{\Gamma(a_N)}{\Gamma(a_0)}\frac{|\mathbf{S}_N|^{1/2}}{|\mathbf{S}_0|^{1/2}}.
\tag{3.118}
$$

**3.24（⋆⋆）** 重做上一题，但这次使用如下形式的贝叶斯定理

$$
p(\boldsymbol{\mathsf{t}})=\frac{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)p(\mathbf{w},\beta)}{p(\mathbf{w},\beta\mid\boldsymbol{\mathsf{t}})}
\tag{3.119}
$$

然后代入先验分布、后验分布以及似然函数，推导结果（3.118）。

<!-- pdf-page: 198 -->
