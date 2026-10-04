<!-- pdf-page: 463 -->

将（9.10）、（9.11）与贝叶斯定理结合，可知这个后验分布具有如下形式：

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})\propto\prod_{n=1}^{N}\prod_{k=1}^{K}\left[\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right]^{z_{nk}}.
\tag{9.38}
$$

因此，它可以按 $n$ 分解，于是在后验分布下，各个 $\{\mathbf{z}_n\}$ 相互独立。查看图 9.6 的有向图，并使用 d 分离判据，就很容易验证这一点（习题 9.5；8.2 节）。指示变量 $z_{nk}$ 在这个后验分布下的期望为

$$
\begin{aligned}
\mathbb{E}[z_{nk}]&=\frac{\sum_{z_{nk}}z_{nk}\left[\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right]^{z_{nk}}}{\sum_{z_{nj}}\left[\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)\right]^{z_{nj}}}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_{j=1}^{K}\pi_j\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_j,\boldsymbol{\Sigma}_j)}=\gamma(z_{nk})
\end{aligned}
\tag{9.39}
$$

这正是分量 $k$ 对数据点 $\mathbf{x}_n$ 的责任度。因此，完整数据对数似然函数的期望为

$$
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})]=\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\left\{\ln\pi_k+\ln\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{9.40}
$$

现在可以按以下步骤进行。首先为参数 $\boldsymbol{\mu}^{\mathrm{old}}$、$\boldsymbol{\Sigma}^{\mathrm{old}}$ 和 $\boldsymbol{\pi}^{\mathrm{old}}$ 选择初始值，用它们计算责任度，即 E 步。随后固定责任度，关于 $\boldsymbol{\mu}_k$、$\boldsymbol{\Sigma}_k$ 和 $\pi_k$ 最大化（9.40），即 M 步。这与前面一样，得到由（9.17）、（9.19）和（9.22）给出的 $\boldsymbol{\mu}^{\mathrm{new}}$、$\boldsymbol{\Sigma}^{\mathrm{new}}$ 和 $\boldsymbol{\pi}^{\mathrm{new}}$ 的闭式解（习题 9.8）。这正是此前推导的高斯混合 EM 算法。在 9.4 节给出 EM 算法收敛性的证明时，我们将更深入地理解完整数据对数似然期望的作用。

### 9.3.2 与 K 均值的关系

比较 K 均值算法与高斯混合的 EM 算法，可以看到两者非常相似。K 均值算法将数据点*硬分配*给各个簇，每个数据点唯一地对应一个簇；EM 算法则根据后验概率进行*软分配*。事实上，可以按以下方式，把 K 均值算法推导为高斯混合 EM 算法的一个特定极限。

考虑一个高斯混合模型，各混合分量的协方差矩阵为 $\epsilon\mathbf{I}$，其中 $\epsilon$ 是

<!-- pdf-page: 464 -->

<!-- join-previous-paragraph -->
所有分量共享的方差参数，$\mathbf{I}$ 是单位矩阵，因此

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)=\frac{1}{(2\pi\epsilon)^{1/2}}\exp\left\{-\frac{1}{2\epsilon}\|\mathbf{x}-\boldsymbol{\mu}_k\|^2\right\}.
\tag{9.41}
$$

现在考虑由 $K$ 个这种高斯分布组成的混合模型的 EM 算法，将 $\epsilon$ 视为固定常数，而不是需要重估的参数。由（9.13），对于某个数据点 $\mathbf{x}_n$，后验概率，即责任度，为

$$
\gamma(z_{nk})=\frac{\pi_k\exp\{-\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2/2\epsilon\}}{\sum_j\pi_j\exp\{-\|\mathbf{x}_n-\boldsymbol{\mu}_j\|^2/2\epsilon\}}.
\tag{9.42}
$$

考虑极限 $\epsilon\to0$。在分母中，使 $\|\mathbf{x}_n-\boldsymbol{\mu}_j\|^2$ 最小的那一项趋于零的速度最慢。因此，对于数据点 $\mathbf{x}_n$，除第 $j$ 项的责任度 $\gamma(z_{nj})$ 趋于 $1$ 以外，其余责任度 $\gamma(z_{nk})$ 都趋于零。注意，只要没有任何 $\pi_k$ 等于零，这个结论就与 $\pi_k$ 的取值无关。因此，在这一极限下，就像 K 均值算法一样，得到数据点到簇的硬分配，即 $\gamma(z_{nk})\to r_{nk}$，其中 $r_{nk}$ 由（9.2）定义。每个数据点由此被分配给均值与其最近的簇。

此时，（9.17）给出的 $\boldsymbol{\mu}_k$ 的 EM 重估方程，简化为 K 均值的结果（9.4）。注意，混合系数的重估公式（9.22）只是把 $\pi_k$ 重新设为分配到簇 $k$ 的数据点所占的比例，不过这些参数此时已不再对算法起实际作用。

最后，在极限 $\epsilon\to0$ 下，由（9.40）给出的完整数据对数似然的期望变为（习题 9.11）

$$
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})]\to-\frac{1}{2}\sum_{n=1}^{N}\sum_{k=1}^{K}r_{nk}\|\mathbf{x}_n-\boldsymbol{\mu}_k\|^2+\mathrm{const}.
\tag{9.43}
$$

因此，在这一极限下，最大化完整数据对数似然的期望，等价于最小化 K 均值算法中由（9.1）给出的失真度量 $J$。

注意，K 均值算法只估计簇均值，并不估计簇的协方差。Sung and Poggio（1994）研究过一种具有一般协方差矩阵的高斯混合模型的硬分配版本，称为*椭圆 K 均值算法*（elliptical K-means algorithm）。

### 9.3.3 伯努利分布的混合

本章到目前为止，着重讨论了用高斯混合描述的连续变量分布。作为混合建模的另一个例子，也为了在不同背景下说明 EM 算法，现在讨论用伯努利分布描述的离散二元变量的混合。这一模型也称为*潜在类别分析*（latent class analysis）（Lazarsfeld and Henry, 1968; McLachlan and Peel, 2000）。除本身具有实际价值外，对伯努利混合的讨论也将为研究离散变量的隐马尔可夫模型打下基础（13.2 节）。

<!-- pdf-page: 465 -->

考虑 $D$ 个二元变量 $x_i$，其中 $i=1,\ldots,D$，每个变量都服从参数为 $\mu_i$ 的伯努利分布，因此

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{i=1}^{D}\mu_i^{x_i}(1-\mu_i)^{(1-x_i)}
\tag{9.44}
$$

其中 $\mathbf{x}=(x_1,\ldots,x_D)^{\mathrm T}$，$\boldsymbol{\mu}=(\mu_1,\ldots,\mu_D)^{\mathrm T}$。可以看到，给定 $\boldsymbol{\mu}$ 后，各个变量 $x_i$ 相互独立。容易看出，这个分布的均值和协方差为

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu}
\tag{9.45}
$$

$$
\operatorname{cov}[\mathbf{x}]=\operatorname{diag}\{\mu_i(1-\mu_i)\}.
\tag{9.46}
$$

现在考虑这些分布的有限混合：

$$
p(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\pi})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid\boldsymbol{\mu}_k)
\tag{9.47}
$$

其中 $\boldsymbol{\mu}=\{\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K\}$、$\boldsymbol{\pi}=\{\pi_1,\ldots,\pi_K\}$，并且

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k)=\prod_{i=1}^{D}\mu_{ki}^{x_i}(1-\mu_{ki})^{(1-x_i)}.
\tag{9.48}
$$

这个混合分布的均值和协方差为（习题 9.12）

$$
\mathbb{E}[\mathbf{x}]=\sum_{k=1}^{K}\pi_k\boldsymbol{\mu}_k
\tag{9.49}
$$

$$
\operatorname{cov}[\mathbf{x}]=\sum_{k=1}^{K}\pi_k\left\{\boldsymbol{\Sigma}_k+\boldsymbol{\mu}_k\boldsymbol{\mu}_k^{\mathrm T}\right\}-\mathbb{E}[\mathbf{x}]\mathbb{E}[\mathbf{x}]^{\mathrm T}
\tag{9.50}
$$

其中 $\boldsymbol{\Sigma}_k=\operatorname{diag}\{\mu_{ki}(1-\mu_{ki})\}$。由于协方差矩阵 $\operatorname{cov}[\mathbf{x}]$ 不再是对角矩阵，这个混合分布能够描述变量之间的相关性，而单个伯努利分布不能。

若给定数据集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$，这个模型的对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\mu},\boldsymbol{\pi})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\right\}.
\tag{9.51}
$$

这里又出现了对数内部的求和，因此最大似然解不再具有闭式形式。

现在推导最大化伯努利混合分布似然函数的 EM 算法。为此，首先显式引入一个潜

<!-- pdf-page: 466 -->

<!-- join-previous-paragraph -->
变量 $\mathbf{z}$，使其与 $\mathbf{x}$ 的每个实例关联。与高斯混合一样，$\mathbf{z}=(z_1,\ldots,z_K)^{\mathrm T}$ 是一个 $K$ 维二元变量，只有一个分量为 $1$，其余分量全为 $0$。于是，给定潜变量后，$\mathbf{x}$ 的条件分布可以写为

$$
p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})=\prod_{k=1}^{K}p(\mathbf{x}\mid\boldsymbol{\mu}_k)^{z_k}
\tag{9.52}
$$

而潜变量的先验分布与高斯混合模型相同，因此

$$
p(\mathbf{z}\mid\boldsymbol{\pi})=\prod_{k=1}^{K}\pi_k^{z_k}.
\tag{9.53}
$$

将 $p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})$ 与 $p(\mathbf{z}\mid\boldsymbol{\pi})$ 相乘，再对 $\mathbf{z}$ 进行边缘化，就能重新得到（9.47）（习题 9.14）。

为了推导 EM 算法，先写出完整数据对数似然函数：

$$
\begin{aligned}
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\pi})={}&\sum_{n=1}^{N}\sum_{k=1}^{K}z_{nk}\Biggl\{\ln\pi_k\\
&+\sum_{i=1}^{D}\left[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\right]\Biggr\}
\end{aligned}
\tag{9.54}
$$

其中 $\mathbf{X}=\{\mathbf{x}_n\}$，$\mathbf{Z}=\{\mathbf{z}_n\}$。接着，关于潜变量的后验分布，对完整数据对数似然取期望，得到

$$
\begin{aligned}
\mathbb{E}_{\mathbf{Z}}[\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\mu},\boldsymbol{\pi})]={}&\sum_{n=1}^{N}\sum_{k=1}^{K}\gamma(z_{nk})\Biggl\{\ln\pi_k\\
&+\sum_{i=1}^{D}\left[x_{ni}\ln\mu_{ki}+(1-x_{ni})\ln(1-\mu_{ki})\right]\Biggr\}
\end{aligned}
\tag{9.55}
$$

其中，$\gamma(z_{nk})=\mathbb{E}[z_{nk}]$ 是给定数据点 $\mathbf{x}_n$ 后分量 $k$ 的后验概率，即责任度。在 E 步中，利用贝叶斯定理计算这些责任度，其形式为

$$
\begin{aligned}
\gamma(z_{nk})=\mathbb{E}[z_{nk}]&=\frac{\sum_{z_{nk}}z_{nk}\left[\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\right]^{z_{nk}}}{\sum_{z_{nj}}\left[\pi_j p(\mathbf{x}_n\mid\boldsymbol{\mu}_j)\right]^{z_{nj}}}\\
&=\frac{\pi_k p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)}{\sum_{j=1}^{K}\pi_j p(\mathbf{x}_n\mid\boldsymbol{\mu}_j)}.
\end{aligned}
\tag{9.56}
$$

<!-- pdf-page: 467 -->

考察（9.55）中关于 $n$ 的求和，可以看到，责任度只通过以下两项起作用：

$$
N_k=\sum_{n=1}^{N}\gamma(z_{nk})
\tag{9.57}
$$

$$
\overline{\mathbf{x}}_k=\frac{1}{N_k}\sum_{n=1}^{N}\gamma(z_{nk})\mathbf{x}_n
\tag{9.58}
$$

其中 $N_k$ 是与分量 $k$ 关联的有效数据点数。在 M 步中，关于参数 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\pi}$ 最大化完整数据对数似然的期望。将（9.55）关于 $\boldsymbol{\mu}_k$ 的导数设为零，并整理各项，得到（习题 9.15）

$$
\boldsymbol{\mu}_k=\overline{\mathbf{x}}_k.
\tag{9.59}
$$

这使分量 $k$ 的均值等于数据的加权均值，权重为该分量对各数据点的责任度。要关于 $\pi_k$ 最大化，需要引入拉格朗日乘子来实施约束 $\sum_k\pi_k=1$。按照与高斯混合类似的步骤，得到（习题 9.16）

$$
\pi_k=\frac{N_k}{N}
\tag{9.60}
$$

这一结果在直观上很合理：分量 $k$ 的混合系数，就是数据集中由该分量解释的点所占的有效比例。

注意，与高斯混合不同，这里不存在似然函数趋于无穷大的奇异点。这可以从似然函数有上界看出，因为 $0\leqslant p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\leqslant1$（习题 9.17）。虽然存在使似然函数趋于零的奇异点，但只要不把 EM 初始化在病态的起点上，算法就不会到达这些点，因为 EM 算法始终提高似然函数的值，直到找到一个局部最大值（9.4 节）。图 9.10 用手写数字建模展示了伯努利混合模型。这里将数字图像转换为二元向量：把所有大于 $0.5$ 的元素设为 $1$，其余元素设为 $0$。现在对由数字“2”“3”和“4”组成的 $N=600$ 个数字样本，运行 10 轮 EM 迭代，用 $K=3$ 个伯努利分布的混合进行拟合。混合系数初始化为 $\pi_k=1/K$；参数 $\mu_{kj}$ 则在区间 $(0.25,0.75)$ 内均匀随机选取，再归一化以满足约束 $\sum_j\mu_{kj}=1$。可以看到，3 个伯努利分布的混合能够找出数据集中与不同数字对应的三个簇。

伯努利分布参数的共轭先验是 Beta 分布；我们已经看到，Beta 先验等价于引入

<!-- pdf-page: 468 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-10.png" alt="二值数字样本与伯努利混合三个分量及单个伯努利分布的均值图像"><figcaption>图 9.10：伯努利混合模型示例。上排为数字数据集中的样本，像素值已用 $0.5$ 的阈值从灰度转换为二值。下排前三幅图显示混合模型中三个分量各自的参数 $\mu_{ki}$。作为比较，我们也再次使用最大似然，用单个多元伯努利分布拟合同一数据集。这相当于直接对每个像素的计数取平均，结果如最右下方的图像所示。</figcaption><p class="figure-translation">上排五幅图为二值样本；下排左侧三幅图为混合分量的均值，最右侧图为单个多元伯努利分布的均值。</p></figure>

<!-- join-previous-paragraph-across-figures -->
额外的 $\mathbf{x}$ 的有效观测（2.1.1 节）。同样，可以为伯努利混合模型引入先验，并用 EM 最大化后验概率分布（习题 9.18）。

利用离散分布（2.26），很容易把伯努利混合的分析扩展到具有 $M>2$ 个状态的多项二元变量（multinomial binary variables）的情况（习题 9.19）。如果需要，同样可以为模型参数引入狄利克雷先验。

### 9.3.4 用于贝叶斯线性回归的 EM

作为 EM 应用的第三个例子，回到贝叶斯线性回归的证据近似。在 3.5.2 节中，我们先计算证据，再令所得表达式的导数为零，得到了超参数 $\alpha$ 和 $\beta$ 的重估方程。现在考虑另一种基于 EM 算法求 $\alpha$ 和 $\beta$ 的方法。回顾一下，目标是关于 $\alpha$ 和 $\beta$ 最大化（3.77）给出的证据函数 $p(\boldsymbol{\mathsf{t}}\mid\alpha,\beta)$。由于参数向量 $\mathbf{w}$ 被边缘化消去了，可以把它视为潜变量，从而用 EM 优化这个边缘似然函数。在 E 步中，给定当前参数 $\alpha$ 和 $\beta$，计算 $\mathbf{w}$ 的后验分布，再利用它求完整数据对数似然的期望。在 M 步中，关于 $\alpha$ 和 $\beta$ 最大化这个量。我们已经推导过 $\mathbf{w}$ 的后验分布，它由（3.49）给出。完整数据对数似然函数于是为

$$
\ln p(\boldsymbol{\mathsf{t}},\mathbf{w}\mid\alpha,\beta)=\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)+\ln p(\mathbf{w}\mid\alpha)
\tag{9.61}
$$

<!-- pdf-page: 469 -->

其中，似然 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w},\beta)$ 和先验 $p(\mathbf{w}\mid\alpha)$ 分别由（3.10）和（3.52）给出，$y(\mathbf{x},\mathbf{w})$ 由（3.3）给出。关于 $\mathbf{w}$ 的后验分布取期望，得到

$$
\begin{aligned}
\mathbb{E}[\ln p(\boldsymbol{\mathsf{t}},\mathbf{w}\mid\alpha,\beta)]={}&\frac{M}{2}\ln\left(\frac{\alpha}{2\pi}\right)-\frac{\alpha}{2}\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]+\frac{N}{2}\ln\left(\frac{\beta}{2\pi}\right)\\
&-\frac{\beta}{2}\sum_{n=1}^{N}\mathbb{E}\left[(t_n-\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n)^2\right].
\end{aligned}
\tag{9.62}
$$

将关于 $\alpha$ 的导数设为零，得到 M 步的重估方程（习题 9.20）

$$
\alpha=\frac{M}{\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]}=\frac{M}{\mathbf{m}_N^{\mathrm T}\mathbf{m}_N+\operatorname{Tr}(\mathbf{S}_N)}.
\tag{9.63}
$$

对于 $\beta$，也有类似结果（习题 9.21）。

注意，这个重估方程与直接计算证据函数得到的相应结果（3.92），形式略有不同。不过，两者都涉及一个 $M\times M$ 矩阵的计算及求逆，或特征分解，因此每次迭代的计算成本相近。

当然，这两种确定 $\alpha$ 的方法应当收敛到相同的结果，前提是它们找到证据函数的同一个局部最大值。要验证这一点，先注意量 $\gamma$ 的定义为

$$
\gamma=M-\alpha\sum_{i=1}^{M}\frac{1}{\lambda_i+\alpha}=M-\alpha\operatorname{Tr}(\mathbf{S}_N).
\tag{9.64}
$$

在证据函数的驻点，重估方程（3.92）会自洽地成立，因此可以代入 $\gamma$，得到

$$
\alpha\mathbf{m}_N^{\mathrm T}\mathbf{m}_N=\gamma=M-\alpha\operatorname{Tr}(\mathbf{S}_N)
\tag{9.65}
$$

解出 $\alpha$，就得到（9.63），恰好就是 EM 重估方程。

最后一个例子考虑一个密切相关的模型，即 7.2.1 节讨论的回归相关向量机。那里通过直接最大化边缘似然，推导了超参数 $\alpha$ 和 $\beta$ 的重估方程。这里考虑另一种方法，把权重向量 $\mathbf{w}$ 视为潜变量，应用 EM 算法。E 步求权重的后验分布，它由（7.81）给出。M 步则最大化完整数据对数似然的期望，其定义为

$$
\mathbb{E}_{\mathbf{w}}\left[\ln\left\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\beta)p(\mathbf{w}\mid\boldsymbol{\alpha})\right\}\right]
\tag{9.66}
$$

其中，期望是关于使用“旧”参数值计算出的后验分布取的。为求新参数值，关于 $\boldsymbol{\alpha}$ 和 $\beta$ 最大化，得到（习题 9.22）

<!-- pdf-page: 470 -->

$$
\alpha_i^{\mathrm{new}}=\frac{1}{m_i^2+\Sigma_{ii}}
\tag{9.67}
$$

$$
(\beta^{\mathrm{new}})^{-1}=\frac{\|\boldsymbol{\mathsf{t}}-\boldsymbol{\Phi}\mathbf{m}_N\|^2+\beta^{-1}\sum_i\gamma_i}{N}.
\tag{9.68}
$$

这些重估方程与直接最大化得到的方程在形式上等价（习题 9.23）。

## 9.4 一般的 EM 算法

*期望最大化算法*（expectation maximization algorithm），简称 EM 算法，是为含潜变量的概率模型寻找最大似然解的一般方法（Dempster et al., 1977; McLachlan and Krishnan, 1997）。这里将对 EM 算法作一般性的讨论，并在此过程中证明：9.2 节和 9.3 节中为高斯混合启发式推导的 EM 算法，确实能够最大化似然函数（Csiszàr and Tusnàdy, 1984; Hathaway, 1986; Neal and Hinton, 1999）。这里的讨论也将为推导变分推断框架打下基础（10.1 节）。

考虑一个概率模型，用 $\mathbf{X}$ 统称所有观测变量，用 $\mathbf{Z}$ 统称所有隐藏变量。联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 由一组记为 $\boldsymbol{\theta}$ 的参数控制。目标是最大化如下似然函数：

$$
p(\mathbf{X}\mid\boldsymbol{\theta})=\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta}).
\tag{9.69}
$$

这里假设 $\mathbf{Z}$ 是离散的；如果 $\mathbf{Z}$ 包含连续变量，或同时包含离散变量和连续变量，只需在相应位置将求和替换为积分，讨论完全相同。

假设直接优化 $p(\mathbf{X}\mid\boldsymbol{\theta})$ 很困难，而优化完整数据似然函数 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 则容易得多。接着，在潜变量上引入一个分布 $q(\mathbf{Z})$。可以看到，无论如何选择 $q(\mathbf{Z})$，以下分解都成立：

$$
\ln p(\mathbf{X}\mid\boldsymbol{\theta})=\mathcal{L}(q,\boldsymbol{\theta})+\operatorname{KL}(q\|p)
\tag{9.70}
$$

其中定义了

$$
\mathcal{L}(q,\boldsymbol{\theta})=\sum_{\mathbf{Z}}q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}{q(\mathbf{Z})}\right\}
\tag{9.71}
$$

$$
\operatorname{KL}(q\|p)=-\sum_{\mathbf{Z}}q(\mathbf{Z})\ln\left\{\frac{p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})}{q(\mathbf{Z})}\right\}.
\tag{9.72}
$$

注意，$\mathcal{L}(q,\boldsymbol{\theta})$ 是分布 $q(\mathbf{Z})$ 的泛函，关于泛函的讨论见附录 D；同时，它是参数 $\boldsymbol{\theta}$ 的函数。值得仔细研究

<!-- pdf-page: 471 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-11.png" alt="对数似然分解为下界与KL散度之和"><figcaption>图 9.11：（9.70）所给分解的示意图；该分解对分布 $q(\mathbf{Z})$ 的任意选择都成立。由于 Kullback–Leibler 散度满足 $\operatorname{KL}(q\|p)\geqslant0$，量 $\mathcal{L}(q,\boldsymbol{\theta})$ 是对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的一个下界。</figcaption><p class="figure-translation">红线表示对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$，蓝线表示下界 $\mathcal{L}(q,\boldsymbol{\theta})$，两者之差为 $\operatorname{KL}(q\|p)$。</p></figure>

<!-- join-previous-paragraph-across-figures -->
表达式（9.71）和（9.72）的形式，尤其要注意：它们的符号相反；此外，$\mathcal{L}(q,\boldsymbol{\theta})$ 包含 $\mathbf{X}$ 和 $\mathbf{Z}$ 的联合分布，而 $\operatorname{KL}(q\|p)$ 包含给定 $\mathbf{X}$ 后 $\mathbf{Z}$ 的条件分布。为验证分解（9.70），先利用概率的乘积规则，得到（习题 9.24）

$$
\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})=\ln p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})+\ln p(\mathbf{X}\mid\boldsymbol{\theta})
\tag{9.73}
$$

将它代入 $\mathcal{L}(q,\boldsymbol{\theta})$ 的表达式，会得到两项。其中一项抵消 $\operatorname{KL}(q\|p)$；对于另一项，利用 $q(\mathbf{Z})$ 是求和为 $1$ 的归一化分布，就得到所需的对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。

由（9.72）可知，$\operatorname{KL}(q\|p)$ 是 $q(\mathbf{Z})$ 与后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$ 之间的 Kullback–Leibler 散度。回顾一下，Kullback–Leibler 散度满足 $\operatorname{KL}(q\|p)\geqslant0$，当且仅当 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$ 时取等号（1.6.1 节）。因此，由（9.70）可得 $\mathcal{L}(q,\boldsymbol{\theta})\leqslant\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。换言之，$\mathcal{L}(q,\boldsymbol{\theta})$ 是 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的下界。图 9.11 展示了分解（9.70）。

EM 算法是一种寻找最大似然解的两阶段迭代优化方法。可以用分解（9.70）定义 EM 算法，并证明它确实能够最大化对数似然。假设参数向量的当前值为 $\boldsymbol{\theta}^{\mathrm{old}}$。在 E 步中，保持 $\boldsymbol{\theta}^{\mathrm{old}}$ 不变，关于 $q(\mathbf{Z})$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$。这个最大化问题的解很容易看出：$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{old}})$ 的值不依赖于 $q(\mathbf{Z})$，因此，当 Kullback–Leibler 散度为零时，$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$ 达到最大值；也就是说，此时 $q(\mathbf{Z})$ 等于后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$。在这种情况下，下界等于对数似然，如图 9.12 所示。

在随后的 M 步中，保持分布 $q(\mathbf{Z})$ 不变，关于 $\boldsymbol{\theta}$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta})$，得到新值 $\boldsymbol{\theta}^{\mathrm{new}}$。这会使下界 $\mathcal{L}$ 增大，除非它已经达到最大值；相应的对数似然函数也必然增大。由于分布 $q$ 是由旧参数值而不是新参数值确定的，并且在 M 步中保持不变，它不会等于新的后验分布 $p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{new}})$，因此 KL 散度不为零。所以，对数似然函数的增加量大于下界的增加量，正如

<!-- pdf-page: 472 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-12.png" alt="E步将分布q设为当前参数下的后验分布，使蓝色下界升到红色对数似然，KL散度降为零"><figcaption>图 9.12：EM 算法的 E 步示意图。将分布 $q$ 设为当前参数值 $\boldsymbol{\theta}^{\mathrm{old}}$ 下的后验分布，使下界上移到与对数似然函数相同的值，此时 KL 散度为零。</figcaption><p class="figure-translation">$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{old}})$：当前参数下的对数似然；$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{old}})$：下界；$\operatorname{KL}(q\|p)=0$：KL 散度为零。</p></figure>

<!-- join-previous-paragraph-across-figures -->
图 9.13 所示。将 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})$ 代入（9.71），可知在 E 步之后，下界具有如下形式：

$$
\begin{aligned}
\mathcal{L}(q,\boldsymbol{\theta})
&=\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})-\sum_{\mathbf{Z}}p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\ln p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{\mathrm{old}})\\
&=\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})+\mathrm{const}
\end{aligned}
\tag{9.74}
$$

这里的常数就是分布 $q$ 的负熵，因此与 $\boldsymbol{\theta}$ 无关。由此可见，在 M 步中最大化的量是完整数据对数似然的期望，这与前面讨论高斯混合时的结论一致。注意，要优化的变量 $\boldsymbol{\theta}$ 只出现在对数内部。如果联合分布 $p(\mathbf{Z},\mathbf{X}\mid\boldsymbol{\theta})$ 属于指数族，或者是若干指数族分布的乘积，那么对数会消去指数运算，得到的 M 步通常会比最大化相应的不完整数据对数似然函数 $p(\mathbf{X}\mid\boldsymbol{\theta})$ 简单得多。

也可以在参数空间中观察 EM 算法的运行过程，如图 9.14 的示意图所示。图中的红色曲线表示我们希望最大化的（不完

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-13.png" alt="M步固定q并提升蓝色下界，对数似然的增加量至少与下界的增加量相同"><figcaption>图 9.13：EM 算法的 M 步示意图。保持分布 $q(\mathbf{Z})$ 不变，关于参数向量 $\boldsymbol{\theta}$ 最大化下界 $\mathcal{L}(q,\boldsymbol{\theta})$，得到更新后的值 $\boldsymbol{\theta}^{\mathrm{new}}$。由于 KL 散度非负，对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的增加量至少与下界的增加量相同。</figcaption><p class="figure-translation">$\ln p(\mathbf{X}\mid\boldsymbol{\theta}^{\mathrm{new}})$：新参数下的对数似然；$\mathcal{L}(q,\boldsymbol{\theta}^{\mathrm{new}})$：新参数下的下界；$\operatorname{KL}(q\|p)$：KL 散度。</p></figure>

<!-- pdf-page: 473 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-09/b-fig-9-14.png" alt="EM参数空间示意图，红色对数似然曲线与蓝色和绿色下界分别在旧参数和新参数处相切"><figcaption>图 9.14：EM 算法交替执行两个操作：根据当前参数值计算对数似然的下界，再最大化这个下界以获得新的参数值。完整讨论见正文。</figcaption><p class="figure-translation">$\boldsymbol{\theta}^{\mathrm{old}}$、$\boldsymbol{\theta}^{\mathrm{new}}$：旧参数、新参数；$\ln p(\mathbf{X}\mid\boldsymbol{\theta})$：对数似然；$\mathcal{L}(q,\boldsymbol{\theta})$：下界。蓝色曲线是在旧参数处构造的下界，绿色曲线是在新参数处构造的下界。</p></figure>

<!-- join-previous-paragraph-across-figures -->
整数据）对数似然函数。首先选取初始参数值 $\boldsymbol{\theta}^{\mathrm{old}}$；在第一个 E 步中，计算潜变量的后验分布，由此得到下界 $\mathcal{L}(\boldsymbol{\theta},\boldsymbol{\theta}^{(\mathrm{old})})$，它在 $\boldsymbol{\theta}^{(\mathrm{old})}$ 处的值等于对数似然，如蓝色曲线所示。注意，这个下界在 $\boldsymbol{\theta}^{(\mathrm{old})}$ 处与对数似然相切，因此两条曲线具有相同的梯度（习题 9.25）。这个下界是一个具有唯一最大值的凸函数（对于属于指数族的混合分量而言）。在 M 步中，最大化这个下界，得到参数值 $\boldsymbol{\theta}^{(\mathrm{new})}$，它所对应的对数似然值大于 $\boldsymbol{\theta}^{(\mathrm{old})}$ 对应的值。随后的 E 步再构造一个在 $\boldsymbol{\theta}^{(\mathrm{new})}$ 处相切的下界，如绿色曲线所示。

对于独立同分布数据集这一特殊情况，$\mathbf{X}$ 包含 $N$ 个数据点 $\{\mathbf{x}_n\}$，而 $\mathbf{Z}$ 包含 $N$ 个对应的潜变量 $\{\mathbf{z}_n\}$，其中 $n=1,\ldots,N$。由独立性假设，有 $p(\mathbf{X},\mathbf{Z})=\prod_n p(\mathbf{x}_n,\mathbf{z}_n)$；对 $\{\mathbf{z}_n\}$ 边缘化，得到 $p(\mathbf{X})=\prod_n p(\mathbf{x}_n)$。利用求和规则和乘积规则，可知在 E 步中计算的后验概率具有如下形式：

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})=\frac{p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}{\displaystyle\sum_{\mathbf{Z}}p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})}=\frac{\displaystyle\prod_{n=1}^{N}p(\mathbf{x}_n,\mathbf{z}_n\mid\boldsymbol{\theta})}{\displaystyle\sum_{\mathbf{Z}}\prod_{n=1}^{N}p(\mathbf{x}_n,\mathbf{z}_n\mid\boldsymbol{\theta})}=\prod_{n=1}^{N}p(\mathbf{z}_n\mid\mathbf{x}_n,\boldsymbol{\theta})
\tag{9.75}
$$

因此，后验分布也可以按 $n$ 分解。对于高斯混合模型，这只是说：各混合分量对某个数据点 $\mathbf{x}_n$ 的责任度，只依赖于 $\mathbf{x}_n$ 的值和混合分量的参数 $\boldsymbol{\theta}$，而不依赖于其他数据点的值。

我们已经看到，EM 算法的 E 步和 M 步都会增大对数似然函数的一个定义明确的下界，并且

<!-- pdf-page: 474 -->
<!-- join-previous-paragraph -->
一个完整的 EM 迭代周期会改变模型参数，使对数似然增大（除非它已经达到最大值，此时参数保持不变）。

对于引入了参数先验 $p(\boldsymbol{\theta})$ 的模型，我们也可以用 EM 算法最大化后验分布 $p(\boldsymbol{\theta}\mid\mathbf{X})$。为说明这一点，注意，作为 $\boldsymbol{\theta}$ 的函数，有 $p(\boldsymbol{\theta}\mid\mathbf{X})=p(\boldsymbol{\theta},\mathbf{X})/p(\mathbf{X})$，因此

$$
\ln p(\boldsymbol{\theta}\mid\mathbf{X})=\ln p(\boldsymbol{\theta},\mathbf{X})-\ln p(\mathbf{X}).
\tag{9.76}
$$

利用分解（9.70），得到

$$
\begin{aligned}
\ln p(\boldsymbol{\theta}\mid\mathbf{X})&=\mathcal{L}(q,\boldsymbol{\theta})+\operatorname{KL}(q\|p)+\ln p(\boldsymbol{\theta})-\ln p(\mathbf{X})\\
&\geqslant\mathcal{L}(q,\boldsymbol{\theta})+\ln p(\boldsymbol{\theta})-\ln p(\mathbf{X}).
\end{aligned}
\tag{9.77}
$$

其中 $\ln p(\mathbf{X})$ 是常数。我们可以再次交替关于 $q$ 和 $\boldsymbol{\theta}$ 优化右侧表达式。由于 $q$ 只出现在 $\mathcal{L}(q,\boldsymbol{\theta})$ 中，关于 $q$ 的优化会得到与标准 EM 算法相同的 E 步方程。先验项 $\ln p(\boldsymbol{\theta})$ 的引入会改变 M 步方程，通常只需对标准最大似然 M 步方程作少量修改。

EM 算法把可能很难求解的似然函数最大化问题分成 E 步和 M 步这两个阶段，每个阶段通常都更容易实现。不过，对于复杂模型，E 步或 M 步，甚至两者，仍有可能难以处理。这就引出了 EM 算法的以下两种扩展。

*广义 EM*（generalized EM，GEM）算法处理 M 步难以求解的问题。它的目标不是关于 $\boldsymbol{\theta}$ 最大化 $\mathcal{L}(q,\boldsymbol{\theta})$，而是改变参数，使这个函数的值增大。同样，由于 $\mathcal{L}(q,\boldsymbol{\theta})$ 是对数似然函数的下界，GEM 算法的每个完整 EM 迭代周期都保证对数似然的值增大（除非当前参数已经对应一个局部最大值）。使用 GEM 方法的一种方式，是在 M 步中采用某种非线性优化策略，例如共轭梯度算法。GEM 算法的另一种形式称为*期望条件最大化*（expectation conditional maximization，ECM）算法，它在每个 M 步中执行多次有约束的优化（Meng and Rubin，1993）。例如，可以把参数划分为若干组，再将 M 步分成多个子步骤；每个子步骤只优化其中一个参数子集，而其余参数保持不变。

类似地，我们可以通过关于 $q(\mathbf{Z})$ 对 $\mathcal{L}(q,\boldsymbol{\theta})$ 执行部分优化而不是完全优化，来推广 EM 算法的 E 步（Neal and Hinton，1999）。正如前面所见，对于任意给定的 $\boldsymbol{\theta}$，$\mathcal{L}(q,\boldsymbol{\theta})$ 关于 $q(\mathbf{Z})$ 有唯一的最大值，对应于后验分布 $q_{\boldsymbol{\theta}}(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta})$；选择这个 $q(\mathbf{Z})$ 时，下界 $\mathcal{L}(q,\boldsymbol{\theta})$ 等于对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$。因此，任何收敛到 $\mathcal{L}(q,\boldsymbol{\theta})$ 的全局最大值的算法，都会找到一个同时使对数似然 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 达到全局最大值的 $\boldsymbol{\theta}$。只要 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 是 $\boldsymbol{\theta}$ 的连续函数，

<!-- pdf-page: 475 -->
<!-- join-previous-paragraph -->
那么根据连续性，$\mathcal{L}(q,\boldsymbol{\theta})$ 的任何局部最大值也都是 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的局部最大值。

考虑 $N$ 个独立的数据点 $\mathbf{x}_1,\ldots,\mathbf{x}_N$，以及相应的潜变量 $\mathbf{z}_1,\ldots,\mathbf{z}_N$。联合分布 $p(\mathbf{X},\mathbf{Z}\mid\boldsymbol{\theta})$ 可以按数据点分解；利用这种结构，可以得到一种增量形式的 EM 算法，每个 EM 迭代周期只处理一个数据点。在 E 步中，我们只重新计算一个数据点的责任度，而不重新计算所有数据点的责任度。乍看之下，随后的 M 步似乎仍然需要涉及所有数据点责任度的计算。然而，如果混合分量属于指数族，那么责任度只通过简单的充分统计量参与计算，而这些统计量可以高效地更新。例如，考虑高斯混合的情形，假设对数据点 $m$ 执行一次更新，将其责任度的旧值和新值分别记为 $\gamma^{\mathrm{old}}(z_{mk})$ 和 $\gamma^{\mathrm{new}}(z_{mk})$。在 M 步中，可以增量更新所需的充分统计量。例如，均值所需的充分统计量由（9.17）和（9.18）定义，由此可得（习题 9.26）

$$
\boldsymbol{\mu}_k^{\mathrm{new}}=\boldsymbol{\mu}_k^{\mathrm{old}}+\left(\frac{\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk})}{N_k^{\mathrm{new}}}\right)\left(\mathbf{x}_m-\boldsymbol{\mu}_k^{\mathrm{old}}\right)
\tag{9.78}
$$

以及

$$
N_k^{\mathrm{new}}=N_k^{\mathrm{old}}+\gamma^{\mathrm{new}}(z_{mk})-\gamma^{\mathrm{old}}(z_{mk}).
\tag{9.79}
$$

协方差和混合系数的相应结果与此类似。

因此，E 步和 M 步所需的时间都是固定的，与数据点总数无关。由于每处理一个数据点就更新参数，而不必等到整个数据集处理完毕，这种增量版本可能比批量版本收敛得更快。这个增量算法中的每个 E 步或 M 步都会增大 $\mathcal{L}(q,\boldsymbol{\theta})$ 的值；正如前面已经证明的，如果算法收敛到 $\mathcal{L}(q,\boldsymbol{\theta})$ 的一个局部（或全局）最大值，那么它也对应于对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 的一个局部（或全局）最大值。

## 习题

**9.1（⋆）www** 考虑 9.1 节讨论的 K 均值算法。证明：由于这组离散指示变量 $r_{nk}$ 的可能赋值只有有限种，而且每一种赋值都对应于 $\{\boldsymbol{\mu}_k\}$ 的唯一最优值，K 均值算法一定会在有限次迭代后收敛。

**9.2（⋆）** 将 2.3.5 节介绍的 Robbins–Monro 序贯估计过程应用于如下问题：求解一个回归函数的根，该回归函数由（9.1）中的 $J$ 对 $\boldsymbol{\mu}_k$ 的导数给出。证明，这会得到一种随机 K 均值算法；对于每个数据点 $\mathbf{x}_n$，它使用（9.5）更新最近的原型 $\boldsymbol{\mu}_k$。

<!-- pdf-page: 476 -->

**9.3（⋆）www** 考虑一个高斯混合模型，其中潜变量的边缘分布 $p(\mathbf{z})$ 由（9.10）给出，观测变量的条件分布 $p(\mathbf{x}\mid\mathbf{z})$ 由（9.11）给出。证明：对 $\mathbf{z}$ 的所有可能取值求和 $p(\mathbf{z})p(\mathbf{x}\mid\mathbf{z})$，得到的边缘分布 $p(\mathbf{x})$ 是（9.7）形式的高斯混合。

**9.4（⋆）** 假设我们希望用 EM 算法最大化一个含潜变量模型的参数后验分布 $p(\boldsymbol{\theta}\mid\mathbf{X})$，其中 $\mathbf{X}$ 是观测数据集。证明：E 步与最大似然情形相同，而在 M 步中需要最大化的量是 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})+\ln p(\boldsymbol{\theta})$，其中 $\mathcal{Q}(\boldsymbol{\theta},\boldsymbol{\theta}^{\mathrm{old}})$ 由（9.30）定义。

**9.5（⋆）** 考虑图 9.6 所示的高斯混合模型的有向图。利用 8.2 节讨论的 d 分离准则，证明潜变量的后验分布可按不同数据点分解，即

$$
p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi})=\prod_{n=1}^{N}p(\mathbf{z}_n\mid\mathbf{x}_n,\boldsymbol{\mu},\boldsymbol{\Sigma},\boldsymbol{\pi}).
\tag{9.80}
$$

**9.6（⋆⋆）** 考虑高斯混合模型的一种特殊情况，其中各分量的协方差矩阵 $\boldsymbol{\Sigma}_k$ 都被约束为相同的值 $\boldsymbol{\Sigma}$。推导在这种模型下最大化似然函数的 EM 方程。

**9.7（⋆）www** 验证：最大化高斯混合模型的完整数据对数似然（9.36），会使各分量的均值和协方差分别独立地拟合对应的数据点组，且混合系数等于各组数据点占总数的比例。

**9.8（⋆）www** 证明：保持责任度 $\gamma(z_{nk})$ 不变，关于 $\boldsymbol{\mu}_k$ 最大化（9.40），会得到（9.17）给出的闭式解。

**9.9（⋆）** 证明：保持责任度 $\gamma(z_{nk})$ 不变，关于 $\boldsymbol{\Sigma}_k$ 和 $\pi_k$ 最大化（9.40），会得到（9.19）和（9.22）给出的闭式解。

**9.10（⋆⋆）** 考虑由混合分布给出的密度模型

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid k)
\tag{9.81}
$$

并假设将向量 $\mathbf{x}$ 分成两部分，使得 $\mathbf{x}=(\mathbf{x}_a,\mathbf{x}_b)$。证明，条件密度 $p(\mathbf{x}_b\mid\mathbf{x}_a)$ 本身也是一个混合分布，并求出混合系数和分量密度的表达式。

<!-- pdf-page: 477 -->

**9.11（⋆）** 在 9.3.2 节中，我们考虑了所有分量的协方差都为 $\epsilon\mathbf{I}$ 的混合模型，从而得到了 K 均值与高斯混合 EM 算法之间的关系。证明：在 $\epsilon\to0$ 的极限下，最大化（9.40）给出的该模型完整数据对数似然的期望，等价于最小化（9.1）给出的 K 均值算法的失真度量 $J$。

**9.12（⋆）www** 考虑如下形式的混合分布

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid k)
\tag{9.82}
$$

其中，$\mathbf{x}$ 的元素可以是离散的、连续的，也可以同时包含这两类。将 $p(\mathbf{x}\mid k)$ 的均值和协方差分别记为 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Sigma}_k$。证明，该混合分布的均值和协方差由（9.49）和（9.50）给出。

**9.13（⋆⋆）** 利用 EM 算法的重估方程，证明：当伯努利混合分布的参数设为对应于似然函数最大值的取值时，它具有如下性质：

$$
\mathbb{E}[\mathbf{x}]=\frac{1}{N}\sum_{n=1}^{N}\mathbf{x}_n\equiv\overline{\mathbf{x}}.
\tag{9.83}
$$

由此证明：如果将这个模型的参数初始化为所有分量都具有相同的均值 $\boldsymbol{\mu}_k=\widehat{\boldsymbol{\mu}}$，其中 $k=1,\ldots,K$，那么无论初始混合系数如何选择，EM 算法都会在一次迭代后收敛，而且这个解具有 $\boldsymbol{\mu}_k=\overline{\mathbf{x}}$ 的性质。注意，这表示混合模型的一种退化情形，其中所有分量都完全相同；实践中，我们会通过恰当的初始化来尽量避免这种解。

**9.14（⋆）** 考虑将（9.52）给出的 $p(\mathbf{x}\mid\mathbf{z},\boldsymbol{\mu})$ 与（9.53）给出的 $p(\mathbf{z}\mid\boldsymbol{\pi})$ 相乘，得到的伯努利分布潜变量与观测变量的联合分布。证明，对这个联合分布关于 $\mathbf{z}$ 边缘化，会得到（9.47）。

**9.15（⋆）www** 证明：关于 $\boldsymbol{\mu}_k$ 最大化伯努利混合分布的完整数据对数似然期望（9.55），会得到 M 步方程（9.59）。

**9.16（⋆）** 证明：关于混合系数 $\pi_k$ 最大化伯努利混合分布的完整数据对数似然期望（9.55），并使用一个拉格朗日乘子来施加求和约束，会得到 M 步方程（9.60）。

**9.17（⋆）www** 证明：由于离散变量 $\mathbf{x}_n$ 满足约束 $0\leqslant p(\mathbf{x}_n\mid\boldsymbol{\mu}_k)\leqslant1$，伯努利混合分布的不完整数据对数似然函数具有上界，因此不存在使似然趋于无穷大的奇异点。

<!-- pdf-page: 478 -->

**9.18（⋆⋆）** 考虑 9.3.3 节讨论的伯努利混合模型，并为每个参数向量 $\boldsymbol{\mu}_k$ 引入由 Beta 分布（2.13）给出的先验分布 $p(\boldsymbol{\mu}_k\mid a_k,b_k)$，同时引入（2.38）给出的狄利克雷先验 $p(\boldsymbol{\pi}\mid\boldsymbol{\alpha})$。推导最大化后验概率 $p(\boldsymbol{\mu},\boldsymbol{\pi}\mid\mathbf{X})$ 的 EM 算法。

**9.19（⋆⋆）** 考虑一个 $D$ 维变量 $\mathbf{x}$，它的每个分量 $i$ 本身都是一个 $M$ 阶多项变量，因此 $\mathbf{x}$ 是一个二元向量，其分量为 $x_{ij}$，其中 $i=1,\ldots,D$，$j=1,\ldots,M$，并且对所有 $i$ 都满足约束 $\sum_j x_{ij}=1$。假设这些变量的分布由 2.2 节所讨论的离散多项分布的混合来描述，即

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k p(\mathbf{x}\mid\boldsymbol{\mu}_k)
\tag{9.84}
$$

其中

$$
p(\mathbf{x}\mid\boldsymbol{\mu}_k)=\prod_{i=1}^{D}\prod_{j=1}^{M}\mu_{kij}^{x_{ij}}.
\tag{9.85}
$$

参数 $\mu_{kij}$ 表示概率 $p(x_{ij}=1\mid\boldsymbol{\mu}_k)$，必须满足 $0\leqslant\mu_{kij}\leqslant1$，且对所有 $k$ 和 $i$ 都满足约束 $\sum_j\mu_{kij}=1$。给定观测数据集 $\{\mathbf{x}_n\}$，其中 $n=1,\ldots,N$，推导 EM 算法的 E 步和 M 步方程，以最大似然方法优化该分布的混合系数 $\pi_k$ 和分量参数 $\mu_{kij}$。

**9.20（⋆）www** 证明：最大化贝叶斯线性回归模型的完整数据对数似然期望（9.62），会得到 $\alpha$ 的 M 步重估结果（9.63）。

**9.21（⋆⋆）** 利用 3.5 节的证据框架，推导贝叶斯线性回归模型中参数 $\beta$ 的 M 步重估方程，与 $\alpha$ 的结果（9.63）相对应。

**9.22（⋆⋆）** 通过最大化（9.66）定义的完整数据对数似然期望，推导用于重估回归相关向量机超参数的 M 步方程（9.67）和（9.68）。

**9.23（⋆⋆）www** 在 7.2.1 节中，我们直接最大化边缘似然，推导出了重估方程（7.87）和（7.88），用于求回归 RVM 的超参数 $\boldsymbol{\alpha}$ 和 $\beta$ 的值。类似地，在 9.3.4 节中，我们用 EM 算法最大化同一个边缘似然，得到了重估方程（9.67）和（9.68）。证明，这两组重估方程在形式上等价。

**9.24（⋆）** 验证关系式（9.70），其中 $\mathcal{L}(q,\boldsymbol{\theta})$ 和 $\operatorname{KL}(q\|p)$ 分别由（9.71）和（9.72）定义。

<!-- pdf-page: 479 -->

**9.25（⋆）www** 证明：当 $q(\mathbf{Z})=p(\mathbf{Z}\mid\mathbf{X},\boldsymbol{\theta}^{(\mathrm{old})})$ 时，（9.71）给出的下界 $\mathcal{L}(q,\boldsymbol{\theta})$ 与对数似然函数 $\ln p(\mathbf{X}\mid\boldsymbol{\theta})$ 在 $\boldsymbol{\theta}=\boldsymbol{\theta}^{(\mathrm{old})}$ 处关于 $\boldsymbol{\theta}$ 的梯度相同。

**9.26（⋆）www** 考虑高斯混合 EM 算法的增量形式，其中只重新计算某个特定数据点 $\mathbf{x}_m$ 的责任度。从 M 步公式（9.17）和（9.18）出发，推导用于更新分量均值的结果（9.78）和（9.79）。

**9.27（⋆⋆）** 当责任度以增量方式更新时，推导高斯混合模型中更新协方差矩阵和混合系数的 M 步公式，与更新均值的结果（9.78）相对应。

<!-- pdf-page: 480 -->
