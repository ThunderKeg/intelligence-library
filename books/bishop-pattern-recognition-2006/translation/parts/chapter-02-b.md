<!-- pdf-page: 122 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-14.png" alt="正态-伽马分布的等高线图"><figcaption>图 2.14：正态-伽马分布（2.154）的等高线图，参数取值为 $\mu_0=0$、$\beta=2$、$a=5$、$b=6$。</figcaption><p class="figure-translation">$\mu$ 为均值参数，$\lambda$ 为精度参数。</p></figure>

对于 $D$ 维变量 $\mathbf{x}$ 的多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda}^{-1})$，假设精度已知，则均值 $\boldsymbol{\mu}$ 的共轭先验仍然是高斯分布。对于均值已知、精度矩阵 $\boldsymbol{\Lambda}$ 未知的情况，共轭先验是 *Wishart 分布*（习题 2.45）：

$$
\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu)=B|\boldsymbol{\Lambda}|^{(\nu-D-1)/2}\exp\left(-\frac12\operatorname{Tr}(\mathbf{W}^{-1}\boldsymbol{\Lambda})\right),
\tag{2.155}
$$

其中 $\nu$ 称为分布的*自由度*（degrees of freedom），$\mathbf{W}$ 为 $D\times D$ 的尺度矩阵，$\operatorname{Tr}(\cdot)$ 表示迹。归一化常数 $B$ 为

$$
B(\mathbf{W},\nu)=|\mathbf{W}|^{-\nu/2}\left(2^{\nu D/2}\pi^{D(D-1)/4}\prod_{i=1}^{D}\Gamma\left(\frac{\nu+1-i}{2}\right)\right)^{-1}.
\tag{2.156}
$$

同样，也可以直接在协方差矩阵上定义共轭先验，而不在精度矩阵上定义，这就得到*逆 Wishart 分布*，不过这里不再深入讨论。如果均值和精度均未知，那么沿用与一元情形相似的推理，共轭先验为

$$
p(\boldsymbol{\mu},\boldsymbol{\Lambda}\mid\boldsymbol{\mu}_0,\beta,\mathbf{W},\nu)=\mathcal{N}(\boldsymbol{\mu}\mid\boldsymbol{\mu}_0,(\beta\boldsymbol{\Lambda})^{-1})\,\mathcal{W}(\boldsymbol{\Lambda}\mid\mathbf{W},\nu),
\tag{2.157}
$$

称为*正态 Wishart 分布*（normal-Wishart distribution），也称*高斯 Wishart 分布*（Gaussian-Wishart distribution）。

### 2.3.7 Student t 分布

我们已经看到，高斯分布精度的共轭先验是伽马分布（第 2.3.6 节）。如果有一元高斯分布 $\mathcal{N}(x\mid\mu,\tau^{-1})$ 及伽马先验 $\operatorname{Gam}(\tau\mid a,b)$，并将精度积分消去，就得到如下形式的 $x$ 的边缘分布（习题 2.46）：

<!-- pdf-page: 123 -->

$$
\begin{aligned}
p(x\mid\mu,a,b)
&=\int_0^{\infty}\mathcal{N}(x\mid\mu,\tau^{-1})\operatorname{Gam}(\tau\mid a,b)\,\mathrm{d}\tau\\
&=\int_0^{\infty}\frac{b^a e^{-b\tau}\tau^{a-1}}{\Gamma(a)}\left(\frac{\tau}{2\pi}\right)^{1/2}\exp\left\{-\frac{\tau}{2}(x-\mu)^2\right\}\,\mathrm{d}\tau\\
&=\frac{b^a}{\Gamma(a)}\left(\frac1{2\pi}\right)^{1/2}\left[b+\frac{(x-\mu)^2}{2}\right]^{-a-1/2}\Gamma(a+1/2),
\end{aligned}
\tag{2.158}
$$

其中作了变量代换 $z=\tau[b+(x-\mu)^2/2]$。按照惯例，定义新参数 $\nu=2a$ 和 $\lambda=a/b$，则分布 $p(x\mid\mu,a,b)$ 可以写成

$$
\operatorname{St}(x\mid\mu,\lambda,\nu)=\frac{\Gamma(\nu/2+1/2)}{\Gamma(\nu/2)}\left(\frac{\lambda}{\pi\nu}\right)^{1/2}\left[1+\frac{\lambda(x-\mu)^2}{\nu}\right]^{-\nu/2-1/2},
\tag{2.159}
$$

称为 *Student t 分布*。参数 $\lambda$ 有时称为 t 分布的*精度*，尽管一般而言，它并不等于方差的倒数。参数 $\nu$ 称为*自由度*，其作用如图 2.15 所示。在 $\nu=1$ 的特殊情况下，t 分布退化为*柯西分布*（Cauchy distribution）；在 $\nu\to\infty$ 的极限下，t 分布 $\operatorname{St}(x\mid\mu,\lambda,\nu)$ 变为均值 $\mu$、精度 $\lambda$ 的高斯分布 $\mathcal{N}(x\mid\mu,\lambda^{-1})$（习题 2.47）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-15.png" alt="不同自由度的Student t分布曲线及高斯极限"><figcaption>图 2.15：$\mu=0$、$\lambda=1$ 时，不同 $\nu$ 值下的 Student t 分布（2.159）。极限 $\nu\to\infty$ 对应均值为 $\mu$、精度为 $\lambda$ 的高斯分布。</figcaption><p class="figure-translation">$\nu\to\infty$、$\nu=1.0$、$\nu=0.1$ 分别标示绿色、蓝色与红色曲线。</p></figure>

由式（2.158）可见，Student t 分布是将无穷多个均值相同、精度不同的高斯分布相加而得到的。这可以解释为高斯分布的无穷混合（第 2.3.9 节将详细讨论高斯混合）。得到的分布通常比高斯分布有更长的“尾部”，如图 2.15 所示。这使 t 分布具有一个重要性质，称为*鲁棒性*（robustness）：与高斯分布相比，它对少量离群数据点的存在不那么敏感。图 2.16 比较了高斯分布和 t 分布的最大似然解，以说明 t 分布的鲁棒性。注意，t 分布的最大似然解可以用期望最大化（EM）算法求得（习题 12.24）。这里可以看到，少量

<!-- pdf-page: 124 -->
<!-- join-previous-paragraph -->
离群点对 t 分布的影响，远小于对高斯分布的影响。在实际应用中，离群点的产生可能是因为数据生成过程对应一个重尾分布，也可能仅仅是因为数据标注错误。鲁棒性对于回归问题同样重要。最小二乘回归不具备鲁棒性，这并不意外，因为它对应于（条件）高斯分布下的最大似然。如果以 t 分布这类重尾分布为基础建立回归模型，就能得到更鲁棒的模型。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-16.png" alt="加入三个离群点前后高斯分布和Student t分布最大似然拟合对比"><figcaption>图 2.16：Student t 分布相对于高斯分布的鲁棒性。（a）从高斯分布中抽取的 30 个数据点的直方图，以及 t 分布（红线）和高斯分布（绿线，大部分被红线遮住）的最大似然拟合。由于 t 分布包含高斯分布这一特例，它给出的解与高斯分布几乎相同。（b）在同一数据集中额外加入三个离群点。高斯分布（绿线）受到离群点的强烈影响而变形，t 分布（红线）则基本不受影响。</figcaption><p class="figure-translation">（a）原数据集；（b）增加三个离群点的数据集。</p></figure>

回到式（2.158），代入另一组参数 $\nu=2a$、$\lambda=a/b$、$\eta=\tau b/a$，可以将 t 分布写成

$$
\operatorname{St}(x\mid\mu,\lambda,\nu)=\int_0^{\infty}\mathcal{N}(x\mid\mu,(\eta\lambda)^{-1})\operatorname{Gam}(\eta\mid\nu/2,\nu/2)\,\mathrm{d}\eta.
\tag{2.160}
$$

然后将其推广到多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda})$，得到相应的多元 Student t 分布：

$$
\operatorname{St}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda},\nu)=\int_0^{\infty}\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},(\eta\boldsymbol{\Lambda})^{-1})\operatorname{Gam}(\eta\mid\nu/2,\nu/2)\,\mathrm{d}\eta.
\tag{2.161}
$$

采用与一元情形相同的方法，可以算出这一积分（习题 2.48）：

<!-- pdf-page: 125 -->

$$
\operatorname{St}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Lambda},\nu)=\frac{\Gamma(D/2+\nu/2)}{\Gamma(\nu/2)}\frac{|\boldsymbol{\Lambda}|^{1/2}}{(\pi\nu)^{D/2}}\left[1+\frac{\Delta^2}{\nu}\right]^{-D/2-\nu/2},
\tag{2.162}
$$

其中 $D$ 为 $\mathbf{x}$ 的维数，$\Delta^2$ 为马氏距离的平方，定义为

$$
\Delta^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\boldsymbol{\Lambda}(\mathbf{x}-\boldsymbol{\mu}).
\tag{2.163}
$$

这是 Student t 分布的多元形式，满足以下性质（习题 2.49）：

$$
\mathbb{E}[\mathbf{x}]=\boldsymbol{\mu},\qquad\text{若 }\nu>1,
\tag{2.164}
$$

$$
\operatorname{cov}[\mathbf{x}]=\frac{\nu}{\nu-2}\boldsymbol{\Lambda}^{-1},\qquad\text{若 }\nu>2,
\tag{2.165}
$$

$$
\operatorname{mode}[\mathbf{x}]=\boldsymbol{\mu}.
\tag{2.166}
$$

一元情形也有相应的结果。

### 2.3.8 周期变量

无论直接使用高斯分布，还是将它作为更复杂概率模型的组成部分，它都具有很大的实际意义。但在某些情形下，高斯分布并不适合用作连续变量的密度模型。实际应用中的一个重要情形就是*周期变量*（periodic variable）。

某个地理位置的风向就是周期变量的一个例子。例如，可以在多个日子里测量风向，然后希望用参数分布来描述这些测量值。另一个例子是日历时间：我们可能希望对某些量建模，并认为这些量具有 24 小时或一年的周期。这类量可以方便地用角坐标（极坐标）$0\leqslant\theta<2\pi$ 表示。

我们可能会尝试选定某个方向作为原点，再应用高斯分布等常规分布来处理周期变量。然而，这种方法的结果会强烈依赖于任意选定的原点。例如，假设有两个观测 $\theta_1=1^{\circ}$ 和 $\theta_2=359^{\circ}$，并用标准的一元高斯分布建模。如果选择 $0^{\circ}$ 为原点，那么该数据集的样本均值为 $180^{\circ}$，标准差为 $179^{\circ}$；如果选择 $180^{\circ}$ 为原点，则均值为 $0^{\circ}$，标准差为 $1^{\circ}$。显然，我们需要专门的方法来处理周期变量。

考虑如何计算周期变量的一组观测 $\mathcal{D}=\{\theta_1,\ldots,\theta_N\}$ 的均值。从现在起，假设 $\theta$ 以弧度为单位。前面已经看到，简单平均值 $(\theta_1+\cdots+\theta_N)/N$ 强烈依赖于坐标。为了找到不随坐标原点改变的均值度量，可以将这些观测看作单位圆上的点，从而用二维单位向量 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 表示，其中对 $n=1,\ldots,N$ 有 $\|\mathbf{x}_n\|=1$，如图 2.17 所示。改为对向量 $\{\mathbf{x}_n\}$ 求平均，

<!-- pdf-page: 126 -->
<!-- join-previous-paragraph -->
得到

$$
\overline{\mathbf{x}}=\frac1N\sum_{n=1}^{N}\mathbf{x}_n,
\tag{2.167}
$$

再求出这个平均向量对应的角度 $\overline{\theta}$。显然，这一定义保证均值的位置不依赖于角坐标原点。注意，$\overline{\mathbf{x}}$ 通常位于单位圆内部。观测的笛卡尔坐标为 $\mathbf{x}_n=(\cos\theta_n,\sin\theta_n)$，样本均值的笛卡尔坐标则可以写为 $\overline{\mathbf{x}}=(\overline{r}\cos\overline{\theta},\overline{r}\sin\overline{\theta})$。代入式（2.167），分别令 $x_1$ 与 $x_2$ 分量相等，得到

$$
\overline{r}\cos\overline{\theta}=\frac1N\sum_{n=1}^{N}\cos\theta_n,\qquad\overline{r}\sin\overline{\theta}=\frac1N\sum_{n=1}^{N}\sin\theta_n.
\tag{2.168}
$$

两式相除，并利用恒等式 $\tan\theta=\sin\theta/\cos\theta$，可以解出

$$
\overline{\theta}=\tan^{-1}\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.
\tag{2.169}
$$

稍后会看到，对周期变量恰当地定义一个分布之后，这个结果会自然地作为其最大似然估计出现。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-17.png" alt="单位圆上表示周期变量的二维向量及平均向量"><figcaption>图 2.17：将周期变量的取值 $\theta_n$ 表示为单位圆上的二维向量 $\mathbf{x}_n$。图中还画出了这些向量的平均值 $\overline{\mathbf{x}}$。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为坐标轴；$\mathbf{x}_1$ 至 $\mathbf{x}_4$ 为观测向量；$\overline{\mathbf{x}}$、$\overline{r}$、$\overline{\theta}$ 分别为平均向量及其极坐标。</p></figure>

现在考虑高斯分布的一种周期性推广，称为 *von Mises 分布*。这里只讨论一元分布，不过任意维数的超球面上也可以定义周期分布。关于周期分布的详细讨论，参见 Mardia and Jupp（2000）。

按照惯例，我们考虑周期为 $2\pi$ 的分布 $p(\theta)$。定义在 $\theta$ 上的概率密度 $p(\theta)$，不仅必须非负、积分

<!-- pdf-page: 127 -->
<!-- join-previous-paragraph -->
为 1，而且还必须具有周期性。因此，$p(\theta)$ 必须满足三个条件：

$$
p(\theta)\geqslant0,
\tag{2.170}
$$

$$
\int_0^{2\pi}p(\theta)\,\mathrm{d}\theta=1,
\tag{2.171}
$$

$$
p(\theta+2\pi)=p(\theta).
\tag{2.172}
$$

由式（2.172）可知，对于任意整数 $M$，有 $p(\theta+M2\pi)=p(\theta)$。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-18.png" alt="在二维高斯分布上以单位圆为条件得到von Mises分布"><figcaption>图 2.18：考虑形式为（2.173）的二维高斯分布，其密度等高线为蓝色，再以红色单位圆为条件，就可以导出 von Mises 分布。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为坐标轴；$p(\mathbf{x})$ 标示高斯密度；$r=1$ 标示单位圆。</p></figure>

可以很容易地构造一个满足这三个性质、类似高斯的分布。考虑两个变量 $\mathbf{x}=(x_1,x_2)$ 的高斯分布，其均值为 $\boldsymbol{\mu}=(\mu_1,\mu_2)$，协方差矩阵为 $\boldsymbol{\Sigma}=\sigma^2\mathbf{I}$，其中 $\mathbf{I}$ 是 $2\times2$ 单位矩阵，于是

$$
p(x_1,x_2)=\frac1{2\pi\sigma^2}\exp\left\{-\frac{(x_1-\mu_1)^2+(x_2-\mu_2)^2}{2\sigma^2}\right\}.
\tag{2.173}
$$

$p(\mathbf{x})$ 的等值线是圆，如图 2.18 所示。现在考虑这个分布沿某个固定半径圆周的取值。这样构造的分布自然具有周期性，但尚未归一化。通过从笛卡尔坐标 $(x_1,x_2)$ 变换为极坐标 $(r,\theta)$，可以确定其形式，其中

$$
x_1=r\cos\theta,\qquad x_2=r\sin\theta.
\tag{2.174}
$$

均值 $\boldsymbol{\mu}$ 也映射到极坐标，写为

$$
\mu_1=r_0\cos\theta_0,\qquad\mu_2=r_0\sin\theta_0.
\tag{2.175}
$$

接着，将这些变换代入二维高斯分布（2.173），并以单位圆 $r=1$ 为条件。注意，我们只关心对 $\theta$ 的依赖。只看高斯分布的指数部分，有

$$
\begin{aligned}
&-\frac1{2\sigma^2}\{(r\cos\theta-r_0\cos\theta_0)^2+(r\sin\theta-r_0\sin\theta_0)^2\}\\
&=-\frac1{2\sigma^2}\{1+r_0^2-2r_0\cos\theta\cos\theta_0-2r_0\sin\theta\sin\theta_0\}\\
&=\frac{r_0}{\sigma^2}\cos(\theta-\theta_0)+\mathrm{const}.
\end{aligned}
\tag{2.176}
$$

<!-- pdf-page: 128 -->

其中 “const” 表示不依赖于 $\theta$ 的项，并使用了以下三角恒等式（习题 2.51）：

$$
\cos^2A+\sin^2A=1,
\tag{2.177}
$$

$$
\cos A\cos B+\sin A\sin B=\cos(A-B).
\tag{2.178}
$$

定义 $m=r_0/\sigma^2$，最终得到沿单位圆 $r=1$ 的分布 $p(\theta)$：

$$
p(\theta\mid\theta_0,m)=\frac1{2\pi I_0(m)}\exp\{m\cos(\theta-\theta_0)\},
\tag{2.179}
$$

这称为 *von Mises 分布*，也称*圆周正态分布*（circular normal）。参数 $\theta_0$ 对应分布的均值，而 $m$ 称为*集中参数*（concentration parameter），类似于高斯分布的方差倒数（精度）。式（2.179）的归一化系数通过 $I_0(m)$ 表示；$I_0(m)$ 是第一类零阶贝塞尔函数（Abramowitz and Stegun，1965），定义为

$$
I_0(m)=\frac1{2\pi}\int_0^{2\pi}\exp\{m\cos\theta\}\,\mathrm{d}\theta.
\tag{2.180}
$$

当 $m$ 很大时，该分布近似为高斯分布（习题 2.52）。图 2.19 画出了 von Mises 分布，图 2.20 画出了函数 $I_0(m)$。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-19.png" alt="两组参数的von Mises分布，左为笛卡尔坐标图，右为极坐标图"><figcaption>图 2.19：两组不同参数下的 von Mises 分布。左侧为笛卡尔坐标图，右侧为对应的极坐标图。</figcaption><p class="figure-translation">红线：$m=5,\theta_0=\pi/4$；蓝线：$m=1,\theta_0=3\pi/4$；$0$、$2\pi$、$\pi/4$、$3\pi/4$ 为角度标记。</p></figure>

现在考虑 von Mises 分布参数 $\theta_0$ 与 $m$ 的最大似然估计。对数似然函数为

$$
\ln p(\mathcal{D}\mid\theta_0,m)=-N\ln(2\pi)-N\ln I_0(m)+m\sum_{n=1}^{N}\cos(\theta_n-\theta_0).
\tag{2.181}
$$

<!-- pdf-page: 129 -->

令对 $\theta_0$ 的导数为零，得到

$$
\sum_{n=1}^{N}\sin(\theta_n-\theta_0)=0.
\tag{2.182}
$$

为解出 $\theta_0$，使用三角恒等式

$$
\sin(A-B)=\cos B\sin A-\cos A\sin B,
\tag{2.183}
$$

由此得到（习题 2.53）

$$
\theta_0^{\mathrm{ML}}=\tan^{-1}\left\{\frac{\sum_n\sin\theta_n}{\sum_n\cos\theta_n}\right\}.
\tag{2.184}
$$

这正是前面将观测看作二维笛卡尔空间中的点时，得到的均值公式（2.169）。

类似地，关于 $m$ 最大化式（2.181），并利用 $I_0'(m)=I_1(m)$（Abramowitz and Stegun，1965），得到

$$
A(m)=\frac1N\sum_{n=1}^{N}\cos(\theta_n-\theta_0^{\mathrm{ML}}),
\tag{2.185}
$$

其中已经代入 $\theta_0^{\mathrm{ML}}$ 的最大似然解（记住，我们在对 $\theta$ 与 $m$ 做联合优化），并定义

$$
A(m)=\frac{I_1(m)}{I_0(m)}.
\tag{2.186}
$$

函数 $A(m)$ 如图 2.20 所示。利用三角恒等式（2.178），式（2.185）可写成

$$
A(m_{\mathrm{ML}})=\left(\frac1N\sum_{n=1}^{N}\cos\theta_n\right)\cos\theta_0^{\mathrm{ML}}-\left(\frac1N\sum_{n=1}^{N}\sin\theta_n\right)\sin\theta_0^{\mathrm{ML}}.
\tag{2.187}
$$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-20.png" alt="贝塞尔函数I0和函数A随集中参数m变化的曲线"><figcaption>图 2.20：式（2.180）定义的贝塞尔函数 $I_0(m)$，以及式（2.186）定义的函数 $A(m)$。</figcaption><p class="figure-translation">两图横轴均为 $m$，左图纵轴为 $I_0(m)$，右图纵轴为 $A(m)$。</p></figure>

<!-- pdf-page: 130 -->

式（2.187）的右侧容易计算，而函数 $A(m)$ 可以数值求逆。

为求完整，简要提及构造周期分布的其他方法。最简单的方法是将角坐标划分为固定区间，使用观测值的直方图。这种方法简单、灵活，但也有明显局限；第 2.5 节详细讨论直方图方法时会看到这一点。另一种方法与 von Mises 分布一样，从欧氏空间中的高斯分布出发，但这次对单位圆进行边缘化，而不是条件化（Mardia and Jupp，2000）。不过，由此得到的分布形式较复杂，这里不再讨论。最后，实轴上的任何有效分布（例如高斯分布），都可以通过将宽度为 $2\pi$ 的连续区间映射到周期变量 $(0,2\pi)$ 上，变成周期分布。这相当于把实轴“缠绕”在单位圆周上。同样，所得分布比 von Mises 分布更难处理。

von Mises 分布的一个局限是它只有单个众数。通过构造 von Mises 分布的混合，可以得到一个能处理多峰情况的灵活框架，用于周期变量建模。使用 von Mises 分布的机器学习应用示例可参见 Lawrence et al.（2002）；将其推广到回归问题的条件密度建模，可参见 Bishop and Nabney（1996）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-21.png" alt="Old Faithful数据集的单高斯拟合与双高斯混合拟合对比"><figcaption>图 2.21：“Old Faithful”数据的散点图，蓝色曲线为概率密度等高线。左图是用最大似然拟合得到的单个高斯分布。注意，这个分布无法刻画数据的两个簇，反而将大量概率质量放在两簇之间数据相对稀疏的中央区域。右图的分布是两个高斯分布的线性组合，用第 9 章介绍的方法进行最大似然拟合，更好地表示了数据。</figcaption><p class="figure-translation">两图横轴表示喷发持续时间（分钟），纵轴表示距离下一次喷发的时间（分钟）。</p></figure>

### 2.3.9 高斯混合

尽管高斯分布具有一些重要的解析性质，但对真实数据集建模时仍有明显局限。考虑图 2.21 的例子。这是“Old Faithful”（老忠实泉）数据集，包含美国黄石国家公园老忠实间歇泉的 272 次喷发测量（附录 A）。每次测量记录

<!-- pdf-page: 131 -->
<!-- join-previous-paragraph -->
喷发持续时间，单位为分钟（横轴），以及距离下一次喷发的时间，单位同样为分钟（纵轴）。可以看到，数据形成了两个明显的簇，简单的高斯分布无法刻画这种结构，而两个高斯分布的线性叠加能更好地描述这个数据集。

通过对高斯分布等较基本的分布作线性组合，可以将这种叠加构造成称为*混合分布*（mixture distribution）的概率模型（McLachlan and Basford，1988；McLachlan and Peel，2000）。图 2.22 表明，高斯分布的线性组合能够产生非常复杂的密度。只要使用足够多的高斯分布，调整它们的均值、协方差以及线性组合的系数，就可以用任意精度近似几乎任何连续密度。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-22.png" alt="三个一维高斯分量相加得到多峰混合密度"><figcaption>图 2.22：一维高斯混合分布的例子。蓝色为三个高斯分布（每个都乘以相应系数），红色为它们的和。</figcaption><p class="figure-translation">横轴为 $x$，纵轴为概率密度 $p(x)$。</p></figure>

因此，考虑如下形式的 $K$ 个高斯密度的叠加：

$$
p(\mathbf{x})=\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k),
\tag{2.188}
$$

称为*高斯混合*（mixture of Gaussians）。每个高斯密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)$ 称为混合的一个*分量*（component），具有自己的均值 $\boldsymbol{\mu}_k$ 和协方差 $\boldsymbol{\Sigma}_k$。含有 3 个分量的高斯混合的等高线图和曲面图见图 2.23。

本节以高斯分量为例说明混合模型的框架。更一般地，混合模型也可以由其他分布的线性组合构成。例如，第 9.3.3 节将讨论伯努利分布的混合，作为离散变量混合模型的一个例子。

式（2.188）中的参数 $\pi_k$ 称为*混合系数*（mixing coefficient）。将式（2.188）两边对 $\mathbf{x}$ 积分，并注意 $p(\mathbf{x})$ 和每个高斯分量都已归一化，得到

$$
\sum_{k=1}^{K}\pi_k=1.
\tag{2.189}
$$

此外，要求 $p(\mathbf{x})\geqslant0$，并结合 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\geqslant0$，意味着所有 $k$ 都满足 $\pi_k\geqslant0$。结合条件（2.189），得到

$$
0\leqslant\pi_k\leqslant1.
\tag{2.190}
$$

<!-- pdf-page: 132 -->

因此，混合系数满足作为概率所需的条件。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-23.png" alt="二维空间中三个高斯分量、混合密度等高线及三维曲面"><figcaption>图 2.23：二维空间中由 3 个高斯分布构成的混合。（a）各混合分量的密度等高线，三个分量分别用红色、蓝色和绿色表示，每个分量下方标出了混合系数。（b）混合分布的边缘概率密度 $p(\mathbf{x})$ 的等高线。（c）分布 $p(\mathbf{x})$ 的曲面图。</figcaption><p class="figure-translation">（a）分量等高线，红、蓝、绿分量的混合系数分别为 $0.5$、$0.2$、$0.3$；（b）混合密度等高线；（c）混合密度曲面。</p></figure>

根据求和法则和乘积法则，边缘密度为

$$
p(\mathbf{x})=\sum_{k=1}^{K}p(k)p(\mathbf{x}\mid k),
\tag{2.191}
$$

它与式（2.188）等价，其中可以将 $\pi_k=p(k)$ 看作选择第 $k$ 个分量的先验概率，将密度 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)=p(\mathbf{x}\mid k)$ 看作给定 $k$ 时 $\mathbf{x}$ 的概率。后续章节将看到，后验概率 $p(k\mid\mathbf{x})$ 起着重要作用，它们也称为*责任度*（responsibility）。由贝叶斯定理，

$$
\begin{aligned}
\gamma_k(\mathbf{x})&\equiv p(k\mid\mathbf{x})\\
&=\frac{p(k)p(\mathbf{x}\mid k)}{\sum_l p(l)p(\mathbf{x}\mid l)}\\
&=\frac{\pi_k\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)}{\sum_l\pi_l\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_l,\boldsymbol{\Sigma}_l)}.
\end{aligned}
\tag{2.192}
$$

第 9 章将更详细地讨论混合分布的概率解释。

高斯混合分布的形式由参数 $\boldsymbol{\pi}$、$\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 决定，这里使用记号 $\boldsymbol{\pi}\equiv\{\pi_1,\ldots,\pi_K\}$、$\boldsymbol{\mu}\equiv\{\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K\}$ 和 $\boldsymbol{\Sigma}\equiv\{\boldsymbol{\Sigma}_1,\ldots,\boldsymbol{\Sigma}_K\}$。设置这些参数的一种方法是最大似然。根据式（2.188），对数似然函数为

$$
\ln p(\mathbf{X}\mid\boldsymbol{\pi},\boldsymbol{\mu},\boldsymbol{\Sigma})=\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{K}\pi_k\mathcal{N}(\mathbf{x}_n\mid\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k)\right\}.
\tag{2.193}
$$

<!-- pdf-page: 133 -->

其中 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$。立刻可以看到，由于对 $k$ 的求和出现在对数内部，情况比单个高斯分布复杂得多。因此，参数的最大似然解不再具有闭式解析表达式。最大化似然函数的一种方法是使用迭代数值优化技术（Fletcher，1987；Nocedal and Wright，1999；Bishop and Nabney，2008）。也可以采用一个强有力的框架，称为*期望最大化*（expectation maximization），第 9 章将详细讨论它。

## 2.4 指数族

本章目前研究的概率分布（高斯混合除外），都是一大类称为*指数族*（exponential family）的分布的具体例子（Duda and Hart，1973；Bernardo and Smith，1994）。指数族成员具有许多重要的共同性质，以较一般的形式讨论这些性质很有启发意义。

给定参数 $\boldsymbol{\eta}$，定义在 $\mathbf{x}$ 上的指数族，是具有如下形式的分布集合：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=h(\mathbf{x})g(\boldsymbol{\eta})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\},
\tag{2.194}
$$

其中 $\mathbf{x}$ 可以是标量或向量，也可以是离散或连续的。$\boldsymbol{\eta}$ 称为分布的*自然参数*（natural parameter），$\mathbf{u}(\mathbf{x})$ 是 $\mathbf{x}$ 的某个函数。函数 $g(\boldsymbol{\eta})$ 可以看作确保分布归一化的系数，因此满足

$$
g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\,\mathrm{d}\mathbf{x}=1.
\tag{2.195}
$$

如果 $\mathbf{x}$ 是离散变量，则将积分换成求和。

先以本章前面介绍的一些分布为例，说明它们确实属于指数族。首先考虑伯努利分布

$$
p(x\mid\mu)=\operatorname{Bern}(x\mid\mu)=\mu^x(1-\mu)^{1-x}.
\tag{2.196}
$$

将右侧写成其对数的指数，得到

$$
\begin{aligned}
p(x\mid\mu)&=\exp\{x\ln\mu+(1-x)\ln(1-\mu)\}\\
&=(1-\mu)\exp\left\{\ln\left(\frac{\mu}{1-\mu}\right)x\right\}.
\end{aligned}
\tag{2.197}
$$

与式（2.194）比较，可知

$$
\eta=\ln\left(\frac{\mu}{1-\mu}\right).
\tag{2.198}
$$

<!-- pdf-page: 134 -->

由此可以解出 $\mu=\sigma(\eta)$，其中

$$
\sigma(\eta)=\frac1{1+\exp(-\eta)}
\tag{2.199}
$$

称为 *logistic sigmoid 函数*。因此，可以用标准表示（2.194）将伯努利分布写为

$$
p(x\mid\eta)=\sigma(-\eta)\exp(\eta x),
\tag{2.200}
$$

其中使用了 $1-\sigma(\eta)=\sigma(-\eta)$，这一恒等式很容易由式（2.199）证明。与式（2.194）比较可知

$$
u(x)=x,
\tag{2.201}
$$

$$
h(x)=1,
\tag{2.202}
$$

$$
g(\eta)=\sigma(-\eta).
\tag{2.203}
$$

接着考虑多项分布。对于单个观测 $\mathbf{x}$，其形式为

$$
p(\mathbf{x}\mid\boldsymbol{\mu})=\prod_{k=1}^{M}\mu_k^{x_k}=\exp\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\},
\tag{2.204}
$$

其中 $\mathbf{x}=(x_1,\ldots,x_N)^{\mathrm T}$。同样，可以将其写成标准表示（2.194）：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=\exp(\boldsymbol{\eta}^{\mathrm T}\mathbf{x}),
\tag{2.205}
$$

其中 $\eta_k=\ln\mu_k$，并定义 $\boldsymbol{\eta}=(\eta_1,\ldots,\eta_M)^{\mathrm T}$。再次与式（2.194）比较，有

$$
\mathbf{u}(\mathbf{x})=\mathbf{x},
\tag{2.206}
$$

$$
h(\mathbf{x})=1,
\tag{2.207}
$$

$$
g(\boldsymbol{\eta})=1.
\tag{2.208}
$$

注意，参数 $\eta_k$ 并非彼此独立，因为参数 $\mu_k$ 受到约束

$$
\sum_{k=1}^{M}\mu_k=1.
\tag{2.209}
$$

因此，只要给定任意 $M-1$ 个参数 $\mu_k$，剩下一个参数的值就确定了。在某些情况下，只用 $M-1$ 个参数表示分布、消去这个约束，会更方便。可以利用关系（2.209），用其余 $\{\mu_k\}$（$k=1,\ldots,M-1$）表示 $\mu_M$ 并将其消去，从而只留下 $M-1$ 个参数。注意，剩余参数仍然受到如下约束：

$$
0\leqslant\mu_k\leqslant1,\qquad\sum_{k=1}^{M-1}\mu_k\leqslant1.
\tag{2.210}
$$

<!-- pdf-page: 135 -->

利用约束（2.209），在这种表示下，多项分布变为

$$
\begin{aligned}
&\exp\left\{\sum_{k=1}^{M}x_k\ln\mu_k\right\}\\
&=\exp\left\{\sum_{k=1}^{M-1}x_k\ln\mu_k+\left(1-\sum_{k=1}^{M-1}x_k\right)\ln\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}\\
&=\exp\left\{\sum_{k=1}^{M-1}x_k\ln\left(\frac{\mu_k}{1-\sum_{j=1}^{M-1}\mu_j}\right)+\ln\left(1-\sum_{k=1}^{M-1}\mu_k\right)\right\}.
\end{aligned}
\tag{2.211}
$$

于是取

$$
\ln\left(\frac{\mu_k}{1-\sum_j\mu_j}\right)=\eta_k.
\tag{2.212}
$$

先将两边对 $k$ 求和，再整理并代回，就可以解出 $\mu_k$：

$$
\mu_k=\frac{\exp(\eta_k)}{1+\sum_j\exp(\eta_j)}.
\tag{2.213}
$$

这称为 *softmax 函数*，也称*归一化指数函数*（normalized exponential）。因此，在这种表示下，多项分布具有如下形式：

$$
p(\mathbf{x}\mid\boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}\exp(\boldsymbol{\eta}^{\mathrm T}\mathbf{x}).
\tag{2.214}
$$

这就是指数族的标准形式，参数向量为 $\boldsymbol{\eta}=(\eta_1,\ldots,\eta_{M-1})^{\mathrm T}$，其中

$$
\mathbf{u}(\mathbf{x})=\mathbf{x},
\tag{2.215}
$$

$$
h(\mathbf{x})=1,
\tag{2.216}
$$

$$
g(\boldsymbol{\eta})=\left(1+\sum_{k=1}^{M-1}\exp(\eta_k)\right)^{-1}.
\tag{2.217}
$$

最后考虑高斯分布。对于一元高斯分布，有

$$
p(x\mid\mu,\sigma^2)=\frac1{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac1{2\sigma^2}(x-\mu)^2\right\},
\tag{2.218}
$$

$$
\phantom{p(x\mid\mu,\sigma^2)}=\frac1{(2\pi\sigma^2)^{1/2}}\exp\left\{-\frac1{2\sigma^2}x^2+\frac{\mu}{\sigma^2}x-\frac1{2\sigma^2}\mu^2\right\}.
\tag{2.219}
$$

<!-- pdf-page: 136 -->

经过简单整理，可以将其写成指数族的标准形式（2.194），其中（习题 2.57）

$$
\boldsymbol{\eta}=\begin{pmatrix}\mu/\sigma^2\\-1/2\sigma^2\end{pmatrix},
\tag{2.220}
$$

$$
\mathbf{u}(x)=\begin{pmatrix}x\\x^2\end{pmatrix},
\tag{2.221}
$$

$$
h(x)=(2\pi)^{-1/2},
\tag{2.222}
$$

$$
g(\boldsymbol{\eta})=(-2\eta_2)^{1/2}\exp\left(\frac{\eta_1^2}{4\eta_2}\right).
\tag{2.223}
$$

### 2.4.1 最大似然与充分统计量

现在考虑如何用最大似然估计一般指数族分布（2.194）的参数向量 $\boldsymbol{\eta}$。对式（2.195）两边关于 $\boldsymbol{\eta}$ 取梯度，有

$$
\begin{aligned}
&\nabla g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\,\mathrm{d}\mathbf{x}\\
&\quad+g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=0.
\end{aligned}
\tag{2.224}
$$

整理，并再次利用式（2.195），得到

$$
-\frac1{g(\boldsymbol{\eta})}\nabla g(\boldsymbol{\eta})=g(\boldsymbol{\eta})\int h(\mathbf{x})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{x})\}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}[\mathbf{u}(\mathbf{x})],
\tag{2.225}
$$

其中使用了式（2.194）。因此得到

$$
-\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})].
\tag{2.226}
$$

注意，$\mathbf{u}(\mathbf{x})$ 的协方差可以用 $g(\boldsymbol{\eta})$ 的二阶导数表示，更高阶矩也类似（习题 2.58）。因此，只要能够将指数族中的分布归一化，就总能通过简单求导得到它的各阶矩。

现在考虑一组独立同分布的数据，记为 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_n\}$，其似然函数为

$$
p(\mathbf{X}\mid\boldsymbol{\eta})=\left(\prod_{n=1}^{N}h(\mathbf{x}_n)\right)g(\boldsymbol{\eta})^N\exp\left\{\boldsymbol{\eta}^{\mathrm T}\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n)\right\}.
\tag{2.227}
$$

令 $\ln p(\mathbf{X}\mid\boldsymbol{\eta})$ 关于 $\boldsymbol{\eta}$ 的梯度为零，得到最大似然估计 $\boldsymbol{\eta}_{\mathrm{ML}}$ 必须满足的条件：

$$
-\nabla\ln g(\boldsymbol{\eta}_{\mathrm{ML}})=\frac1N\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n).
\tag{2.228}
$$

<!-- pdf-page: 137 -->

原则上，解这个方程就可以得到 $\boldsymbol{\eta}_{\mathrm{ML}}$。可以看到，最大似然估计的解只通过 $\sum_n\mathbf{u}(\mathbf{x}_n)$ 依赖于数据，所以这个量称为分布（2.194）的*充分统计量*（sufficient statistic）。不必存储整个数据集，只需存储充分统计量的值。例如，伯努利分布中的函数 $u(x)$ 就是 $x$，因此只需保留数据点 $\{x_n\}$ 的和；对于高斯分布，$\mathbf{u}(x)=(x,x^2)^{\mathrm T}$，因此必须同时保留 $\{x_n\}$ 的和与 $\{x_n^2\}$ 的和。

在 $N\to\infty$ 的极限下，式（2.228）的右侧变为 $\mathbb{E}[\mathbf{u}(\mathbf{x})]$。与式（2.226）比较可知，在这个极限下，$\boldsymbol{\eta}_{\mathrm{ML}}$ 等于真实参数值 $\boldsymbol{\eta}$。

事实上，这种充分性也适用于贝叶斯推断，不过我们把讨论推迟到第 8 章。在那里，我们已经掌握图模型的工具，从而能够更深入地理解这些重要概念。

### 2.4.2 共轭先验

我们已经多次遇到共轭先验的概念，例如伯努利分布的共轭先验是Beta 分布；高斯分布中，均值的共轭先验是高斯分布，精度的共轭先验是 Wishart 分布。一般地，对于给定概率分布 $p(\mathbf{x}\mid\boldsymbol{\eta})$，可以寻找与似然函数共轭的先验 $p(\boldsymbol{\eta})$，使后验分布与先验具有相同的函数形式。指数族（2.194）的任意成员，都存在如下形式的共轭先验：

$$
p(\boldsymbol{\eta}\mid\boldsymbol{\chi},\nu)=f(\boldsymbol{\chi},\nu)g(\boldsymbol{\eta})^{\nu}\exp\{\nu\boldsymbol{\eta}^{\mathrm T}\boldsymbol{\chi}\},
\tag{2.229}
$$

其中 $f(\boldsymbol{\chi},\nu)$ 为归一化系数，$g(\boldsymbol{\eta})$ 与式（2.194）中的函数相同。要确认它确实共轭，将先验（2.229）乘以似然函数（2.227），忽略归一化系数，得到后验分布

$$
p(\boldsymbol{\eta}\mid\mathbf{X},\boldsymbol{\chi},\nu)\propto g(\boldsymbol{\eta})^{\nu+N}\exp\left\{\boldsymbol{\eta}^{\mathrm T}\left(\sum_{n=1}^{N}\mathbf{u}(\mathbf{x}_n)+\nu\boldsymbol{\chi}\right)\right\}.
\tag{2.230}
$$

它与先验（2.229）的函数形式相同，因而确认了共轭性。还可以看到，参数 $\nu$ 可以解释为先验中的有效伪观测数，每个伪观测的充分统计量 $\mathbf{u}(\mathbf{x})$ 都取值为 $\boldsymbol{\chi}$。

### 2.4.3 无信息先验

在概率推断的一些应用中，我们可能具有便于用先验分布表达的先验知识。例如，如果先验对变量的某个值赋予零概率，那么无论

<!-- pdf-page: 138 -->
<!-- join-previous-paragraph -->
随后观测到什么数据，后验分布也必然给这个值零概率。然而，很多时候，我们对先验分布应具有什么形式所知甚少。这时可以寻找一种称为*无信息先验*（noninformative prior）的先验分布，希望它对后验分布的影响尽可能小（Jeffries，1946；Box and Tao，1973；Bernardo and Smith，1994）。这有时被称为“让数据自己说话”。

如果分布 $p(x\mid\lambda)$ 由参数 $\lambda$ 决定，我们可能会认为常数先验 $p(\lambda)=\mathrm{const}$ 很合适。如果 $\lambda$ 是具有 $K$ 个状态的离散变量，这相当于令各状态的先验概率均为 $1/K$。但对于连续参数，这种方法有两个潜在困难。首先，如果 $\lambda$ 的定义域无界，那么对 $\lambda$ 的积分发散，该先验分布无法正确归一化。这种先验称为*非正常先验*（improper prior）。在实践中，只要相应的后验分布是正常的（proper），即能够正确归一化，往往仍然可以使用非正常先验。例如，在高斯分布的均值上采用均匀先验后，只要观测到至少一个数据点，均值的后验分布就是正常的。

第二个困难来自非线性变量变换下概率密度的变换规律，即式（1.27）。如果函数 $h(\lambda)$ 是常数，进行变量代换 $\lambda=\eta^2$ 后，$\widehat{h}(\eta)=h(\eta^2)$ 仍是常数。但如果选择密度 $p_{\lambda}(\lambda)$ 为常数，根据式（1.27），$\eta$ 的密度为

$$
p_{\eta}(\eta)=p_{\lambda}(\lambda)\left|\frac{\mathrm{d}\lambda}{\mathrm{d}\eta}\right|=p_{\lambda}(\eta^2)2\eta\propto\eta,
\tag{2.231}
$$

所以 $\eta$ 的密度不是常数。最大似然方法不会遇到这个问题，因为似然函数 $p(x\mid\lambda)$ 只是 $\lambda$ 的普通函数，可以自由选择任何方便的参数化方式。但是，如果要选择常数先验分布，就必须谨慎地选择参数的合适表示。

这里考察两个简单的无信息先验例子（Berger，1985）。首先，如果密度具有形式

$$
p(x\mid\mu)=f(x-\mu),
\tag{2.232}
$$

则参数 $\mu$ 称为*位置参数*（location parameter）。这个密度族具有*平移不变性*（translation invariance），因为将 $x$ 平移一个常数，得到 $\widehat{x}=x+c$ 后，有

$$
p(\widehat{x}\mid\widehat{\mu})=f(\widehat{x}-\widehat{\mu}),
\tag{2.233}
$$

其中定义了 $\widehat{\mu}=\mu+c$。因此，密度在新变量下与原变量下具有相同形式，也就是说，密度不依赖原点的选择。我们希望选取的先验反映这种平移不变性，因此令先验对

<!-- pdf-page: 139 -->
<!-- join-previous-paragraph -->
区间 $A\leqslant\mu\leqslant B$ 及平移后的区间 $A-c\leqslant\mu\leqslant B-c$ 赋予相同的概率质量。这意味着

$$
\int_A^B p(\mu)\,\mathrm{d}\mu=\int_{A-c}^{B-c}p(\mu)\,\mathrm{d}\mu=\int_A^B p(\mu-c)\,\mathrm{d}\mu.
\tag{2.234}
$$

由于对任意 $A$ 和 $B$ 都必须成立，所以

$$
p(\mu-c)=p(\mu),
\tag{2.235}
$$

即 $p(\mu)$ 是常数。高斯分布的均值 $\mu$ 就是位置参数的一个例子。前面看到，$\mu$ 的共轭先验是高斯分布 $p(\mu\mid\mu_0,\sigma_0^2)=\mathcal{N}(\mu\mid\mu_0,\sigma_0^2)$。取极限 $\sigma_0^2\to\infty$，就得到无信息先验。事实上，由式（2.141）和（2.142）可见，此时 $\mu$ 的后验分布中，先验的贡献消失了。

第二个例子是如下形式的密度：

$$
p(x\mid\sigma)=\frac1{\sigma}f\left(\frac{x}{\sigma}\right),
\tag{2.236}
$$

其中 $\sigma>0$。注意，只要 $f(x)$ 正确归一化，这也是归一化的密度（习题 2.59）。参数 $\sigma$ 称为*尺度参数*（scale parameter），密度具有*尺度不变性*（scale invariance）：将 $x$ 乘以常数，得到 $\widehat{x}=cx$ 后，有

$$
p(\widehat{x}\mid\widehat{\sigma})=\frac1{\widehat{\sigma}}f\left(\frac{\widehat{x}}{\widehat{\sigma}}\right),
\tag{2.237}
$$

其中定义 $\widehat{\sigma}=c\sigma$。这种变换对应于尺度的改变，例如当 $x$ 表示长度时，从米换为千米。我们希望所选先验反映这种尺度不变性。如果考虑区间 $A\leqslant\sigma\leqslant B$ 和缩放后的区间 $A/c\leqslant\sigma\leqslant B/c$，先验应对这两个区间赋予相同的概率质量。因此

$$
\int_A^B p(\sigma)\,\mathrm{d}\sigma=\int_{A/c}^{B/c}p(\sigma)\,\mathrm{d}\sigma=\int_A^B p\left(\frac1c\sigma\right)\frac1c\,\mathrm{d}\sigma.
\tag{2.238}
$$

由于对任意 $A$ 和 $B$ 都必须成立，所以

$$
p(\sigma)=p\left(\frac1c\sigma\right)\frac1c,
\tag{2.239}
$$

从而 $p(\sigma)\propto1/\sigma$。注意，这又是一个非正常先验，因为分布在 $0\leqslant\sigma\leqslant\infty$ 上的积分发散。有时，从参数对数的密度来看尺度参数的先验也很方便。利用密度变换规则（1.27），可知 $p(\ln\sigma)=\mathrm{const}$。因此，在这个先验下，区间 $1\leqslant\sigma\leqslant10$、$10\leqslant\sigma\leqslant100$ 和 $100\leqslant\sigma\leqslant1000$ 的概率质量相同。

<!-- pdf-page: 140 -->

在考虑了位置参数 $\mu$ 之后，高斯分布的标准差 $\sigma$ 就是尺度参数的一个例子，因为

$$
\mathcal{N}(x\mid\mu,\sigma^2)\propto\sigma^{-1}\exp\{-(\widetilde{x}/\sigma)^2\},
\tag{2.240}
$$

其中 $\widetilde{x}=x-\mu$。如前所述，使用精度 $\lambda=1/\sigma^2$ 往往比直接使用 $\sigma$ 更方便。根据密度变换规则，分布 $p(\sigma)\propto1/\sigma$ 对应于形式为 $p(\lambda)\propto1/\lambda$ 的分布。我们已经看到，$\lambda$ 的共轭先验是式（2.146）给出的伽马分布 $\operatorname{Gam}(\lambda\mid a_0,b_0)$（第 2.3 节）。无信息先验是 $a_0=b_0=0$ 的特例。再看 $\lambda$ 的后验分布结果（2.150）和（2.151），当 $a_0=b_0=0$ 时，后验只依赖于来自数据的项，而不依赖先验。

## 2.5 非参数方法

本章一直关注具有特定函数形式的概率分布，这些分布由少量参数决定，参数值则根据数据集确定。这称为密度建模的*参数化方法*（parametric approach）。这种方法的一个重要局限是，所选密度可能无法很好地描述生成数据的分布，导致预测性能较差。例如，如果数据生成过程具有多个众数，那么高斯分布永远无法刻画这一特征，因为它必定是单峰的。

在最后这一节，我们考察一些对分布形式作很少假设的*非参数*（nonparametric）密度估计方法。这里主要关注简单的频率学派方法。不过，读者也应知道，非参数贝叶斯方法正受到越来越多的关注（Walker et al.，1999；Neal，2000；Müller and Quintana，2004；Teh et al.，2006）。

先讨论密度估计的直方图方法。前面在图 1.11 的边缘分布与条件分布，以及图 2.6 的中心极限定理中，已经见过这种方法。这里进一步考察直方图密度模型的性质，重点是单个连续变量 $x$。标准直方图把 $x$ 划分为宽度为 $\Delta_i$ 的互不重叠的区间，再统计落入第 $i$ 个区间的观测数 $n_i$。要将计数变为归一化概率密度，只需除以观测总数 $N$ 和区间宽度 $\Delta_i$，得到每个区间的概率值

$$
p_i=\frac{n_i}{N\Delta_i}.
\tag{2.241}
$$

容易看出，此时 $\int p(x)\,\mathrm{d}x=1$。得到的密度模型 $p(x)$ 在每个区间内都是常数，通常选择各区间具有相同宽度 $\Delta_i=\Delta$。

<!-- pdf-page: 141 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-24.png" alt="三种区间宽度下的直方图密度估计"><figcaption>图 2.24：直方图密度估计示意图。从绿色曲线所表示的分布中生成包含 50 个数据点的数据集。根据式（2.241）进行直方图密度估计，所有区间宽度相同，为 $\Delta$；图中展示了不同 $\Delta$ 值下的结果。</figcaption><p class="figure-translation">从上到下，区间宽度分别为 $\Delta=0.04$、$\Delta=0.08$、$\Delta=0.25$。</p></figure>

图 2.24 展示了直方图密度估计的例子。数据来自绿色曲线对应的分布，它由两个高斯分布混合而成。图中同时给出了三种区间宽度 $\Delta$ 对应的直方图密度估计。当 $\Delta$ 很小（上图）时，得到的密度模型有很多尖峰，其中许多结构并不存在于实际生成数据的分布中。相反，当 $\Delta$ 过大（下图）时，模型过于平滑，无法刻画绿色曲线的双峰特征。某个适中的 $\Delta$ 值（中图）给出了最佳结果。原则上，直方图密度模型也依赖于区间边界位置的选择，不过其影响通常远小于 $\Delta$ 的影响。

注意，直方图方法具有一个特点（稍后介绍的方法没有这一特点）：一旦计算完直方图，就可以丢弃原数据集。数据集很大时，这可能是一个优势。此外，当数据点逐个到达时，直方图方法也容易使用。

实际中，直方图适合快速查看一维或二维数据的分布，但不适合大多数密度估计应用。一个明显问题是，估计密度的不连续性来自区间边界，而不是来自真实数据生成分布的任何性质。另一个重要局限是它随维数的增长情况。如果将 $D$ 维空间中每个变量都划分为 $M$ 个区间，则总单元数为 $M^D$。这种随 $D$ 的指数增长，就是维数灾难的一个例子（第 1.4 节）。在高维空间中，要对局部概率密度作出有意义的估计，所需数据量大得难以承受。

不过，直方图密度估计给出了两点重要启示。第一，为了估计某个位置的概率密度，应考察该点某个局部邻域内的数据点。注意，局部性的概念要求我们假定某种距离度量，这里一直采用欧氏距离。对于直方图，

<!-- pdf-page: 142 -->
<!-- join-previous-paragraph -->
邻域由区间定义，并且自然存在一个描述局部区域空间范围的“平滑”参数，此处就是区间宽度。第二，要获得好的结果，平滑参数既不能太大，也不能太小。这使人想到第 1 章多项式曲线拟合中的模型复杂度选择：多项式阶数 $M$，或者正则化参数 $\alpha$，都在某个不大不小的中间值处最优。带着这些认识，我们转而讨论两种广泛使用的非参数密度估计技术：核估计和近邻方法。它们随维数增长的表现，比简单直方图模型更好。

### 2.5.1 核密度估计

假设在某个 $D$ 维空间中，从未知概率密度 $p(\mathbf{x})$ 抽取观测；这里假定该空间是欧氏空间。我们希望估计 $p(\mathbf{x})$ 的值。根据前面对局部性的讨论，考虑包含 $\mathbf{x}$ 的一个小区域 $\mathcal{R}$。这个区域的概率质量为

$$
P=\int_{\mathcal{R}}p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{2.242}
$$

现在假设已经收集到由 $p(\mathbf{x})$ 抽取的 $N$ 个观测组成的数据集。每个数据点落入 $\mathcal{R}$ 的概率都是 $P$，因此区域内的数据点总数 $K$ 服从二项分布（第 2.1 节）：

$$
\operatorname{Bin}(K\mid N,P)=\frac{N!}{K!(N-K)!}P^K(1-P)^{1-K}.
\tag{2.243}
$$

根据式（2.11），落入该区域的数据点比例的均值为 $\mathbb{E}[K/N]=P$；类似地，根据式（2.12），围绕此均值的方差为 $\operatorname{var}[K/N]=P(1-P)/N$。当 $N$ 很大时，这个分布在均值附近形成尖峰，因此

$$
K\simeq NP.
\tag{2.244}
$$

如果再假设区域 $\mathcal{R}$ 足够小，使概率密度 $p(\mathbf{x})$ 在整个区域内近似不变，则有

$$
P\simeq p(\mathbf{x})V,
\tag{2.245}
$$

其中 $V$ 是 $\mathcal{R}$ 的体积。结合式（2.244）与（2.245），得到密度估计

$$
p(\mathbf{x})=\frac{K}{NV}.
\tag{2.246}
$$

注意，式（2.246）的有效性依赖两个相互矛盾的假设：区域 $\mathcal{R}$ 必须足够小，使区域内密度近似不变；同时，相对于密度的大小，它又必须足够大，使落入区域的数据点数 $K$ 足以让二项分布形成尖峰。

<!-- pdf-page: 143 -->

结果（2.246）有两种用法。可以固定 $K$，根据数据确定 $V$，得到稍后讨论的 $K$ 近邻方法；也可以固定 $V$，根据数据确定 $K$，得到核方法。可以证明，只要 $V$ 随 $N$ 适当缩小，而 $K$ 随 $N$ 增长，$K$ 近邻密度估计和核密度估计在 $N\to\infty$ 的极限下都会收敛于真实概率密度（Duda and Hart，1973）。

先详细讨论核方法。首先，将区域 $\mathcal{R}$ 取为以待估计概率密度的位置 $\mathbf{x}$ 为中心的小超立方体。为了统计落入其中的数据点数 $K$，定义以下函数很方便：

$$
k(\mathbf{u})=\begin{cases}1,&|u_i|\leqslant1/2,\quad i=1,\ldots,D,\\0,&\text{其他情况},\end{cases}
\tag{2.247}
$$

它表示以原点为中心的单位立方体。函数 $k(\mathbf{u})$ 是*核函数*（kernel function）的一个例子，在此也称为 *Parzen 窗*（Parzen window）。由式（2.247），如果数据点 $\mathbf{x}_n$ 位于以 $\mathbf{x}$ 为中心、边长为 $h$ 的立方体内，$k((\mathbf{x}-\mathbf{x}_n)/h)$ 等于 1，否则等于 0。因此，立方体内的数据点总数为

$$
K=\sum_{n=1}^{N}k\left(\frac{\mathbf{x}-\mathbf{x}_n}{h}\right).
\tag{2.248}
$$

将其代入式（2.246），得到 $\mathbf{x}$ 处的密度估计

$$
p(\mathbf{x})=\frac1N\sum_{n=1}^{N}\frac1{h^D}k\left(\frac{\mathbf{x}-\mathbf{x}_n}{h}\right),
\tag{2.249}
$$

这里使用了 $D$ 维空间中边长为 $h$ 的超立方体体积 $V=h^D$。利用 $k(\mathbf{u})$ 的对称性，可以重新解释这个等式：不再看作以 $\mathbf{x}$ 为中心的单个立方体，而是看作分别以 $N$ 个数据点 $\mathbf{x}_n$ 为中心的 $N$ 个立方体的求和。

当前形式的核密度估计（2.249）仍然存在直方图方法的一个问题：人为产生的不连续性，此处出现在立方体边界。如果选择更平滑的核函数，就可以得到更平滑的密度模型。常见选择是高斯函数，对应如下核密度模型：

$$
p(\mathbf{x})=\frac1N\sum_{n=1}^{N}\frac1{(2\pi h^2)^{1/2}}\exp\left\{-\frac{\|\mathbf{x}-\mathbf{x}_n\|^2}{2h^2}\right\},
\tag{2.250}
$$

其中 $h$ 表示高斯分量的标准差。因此，密度模型的构造方法是：在每个数据点上放置一个高斯分布，将整个数据集中各点的贡献相加，再除以 $N$，使密度正确归一化。图 2.25 将模型（2.250）应用于前面用于

<!-- pdf-page: 144 -->
<!-- join-previous-paragraph -->
说明直方图方法的数据集。正如预期，参数 $h$ 起着平滑参数的作用：较小的 $h$ 对噪声敏感，较大的 $h$ 又会过度平滑，需要在两者之间权衡。同样，优化 $h$ 是模型复杂度问题，类似于直方图密度估计中选择区间宽度，或者曲线拟合中选择多项式阶数。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-25.png" alt="三种核宽度的核密度估计，与真实双峰密度比较"><figcaption>图 2.25：将核密度模型（2.250）应用于图 2.24 中说明直方图方法的同一数据集。$h$ 起平滑参数的作用。如果太小（上图），得到的密度模型噪声很大；如果太大（下图），实际生成数据的分布（绿色曲线）的双峰结构会被抹平。某个适中的 $h$ 值（中图）给出最佳密度模型。</figcaption><p class="figure-translation">从上到下分别为 $h=0.005$、$h=0.07$、$h=0.2$；绿色为真实分布，蓝色为核密度估计。</p></figure>

式（2.249）也可以选择任何其他核函数 $k(\mathbf{u})$，只要满足

$$
k(\mathbf{u})\geqslant0,
\tag{2.251}
$$

$$
\int k(\mathbf{u})\,\mathrm{d}\mathbf{u}=1.
\tag{2.252}
$$

这两个条件保证最终的概率分布处处非负，并且积分为 1。式（2.249）给出的这类密度模型称为*核密度估计*（kernel density estimator），也称 *Parzen 估计*。它的一个很大优点是“训练”阶段无需计算，只需存储训练集。不过，这也是它的一个主要弱点，因为计算密度的代价随数据集大小线性增长。

### 2.5.2 近邻方法

核密度估计的一个困难是，控制核宽度的参数 $h$ 对所有核都相同。在数据密集的区域，较大的 $h$ 可能过度平滑，抹去本可从数据中提取的结构；但缩小 $h$，又可能在密度较低的其他区域产生噪声较大的估计。因此，$h$ 的最优选择可能依赖于数据空间中的位置。近邻密度估计方法解决了这一问题。

因此，回到局部密度估计的一般结果（2.246）。这次不固定 $V$ 后根据数据确定 $K$，而是固定 $K$ 后根据数据寻找合适的 $V$。为此，以需要估计

<!-- pdf-page: 145 -->
<!-- join-previous-paragraph -->
密度 $p(\mathbf{x})$ 的点 $\mathbf{x}$ 为中心，画一个小球，并逐渐增大半径，直到球内恰好包含 $K$ 个数据点。然后用式（2.246）估计密度 $p(\mathbf{x})$，其中 $V$ 取最终球体的体积。这称为 *$K$ 近邻*（$K$ nearest neighbours）方法。图 2.26 使用与图 2.24、图 2.25 相同的数据集，展示不同参数 $K$ 下的结果。可以看到，此时由 $K$ 控制平滑程度，同样存在一个既不过大也不过小的最优选择。注意，$K$ 近邻得到的模型不是真正的密度模型，因为它在整个空间上的积分发散（习题 2.61）。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-26.png" alt="不同近邻数的K近邻密度估计"><figcaption>图 2.26：$K$ 近邻密度估计示意图，数据集与图 2.25 和图 2.24 相同。参数 $K$ 控制平滑程度：较小的 $K$（上图）得到噪声很大的密度模型；较大的 $K$（下图）会将生成数据的真实分布（绿色曲线）的双峰结构抹平。</figcaption><p class="figure-translation">从上到下分别为 $K=1$、$K=5$、$K=30$；绿色为真实分布，蓝色为近邻密度估计。</p></figure>

作为本章的结尾，下面说明如何将 $K$ 近邻密度估计推广到分类问题。做法是对各类别分别应用 $K$ 近邻密度估计，再使用贝叶斯定理。假设数据集中类别 $\mathcal{C}_k$ 有 $N_k$ 个点，总数为 $N$，因此 $\sum_kN_k=N$。如果要对新点 $\mathbf{x}$ 分类，就以 $\mathbf{x}$ 为中心画一个球，使其恰好包含 $K$ 个点，而不考虑它们的类别。假设球的体积为 $V$，其中有 $K_k$ 个点来自类别 $\mathcal{C}_k$。于是，由式（2.246），各类密度的估计为

$$
p(\mathbf{x}\mid\mathcal{C}_k)=\frac{K_k}{N_kV}.
\tag{2.253}
$$

类似地，无条件密度为

$$
p(\mathbf{x})=\frac{K}{NV},
\tag{2.254}
$$

而类别先验为

$$
p(\mathcal{C}_k)=\frac{N_k}{N}.
\tag{2.255}
$$

利用贝叶斯定理将式（2.253）、（2.254）和（2.255）结合，得到类别归属的后验概率

$$
p(\mathcal{C}_k\mid\mathbf{x})=\frac{p(\mathbf{x}\mid\mathcal{C}_k)p(\mathcal{C}_k)}{p(\mathbf{x})}=\frac{K_k}{K}.
\tag{2.256}
$$

<!-- pdf-page: 146 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-27.png" alt="K近邻分类器以及最近邻分类边界示意图"><figcaption>图 2.27：（a）在 $K$ 近邻分类器中，新点（黑色菱形）的类别，由距离最近的 $K$ 个训练点中的多数类别决定，这里 $K=3$。（b）最近邻（$K=1$）分类方法得到的决策边界，由不同类别成对数据点的垂直平分超平面组成。</figcaption><p class="figure-translation">$x_1$、$x_2$ 为输入坐标；（a）$K$ 近邻多数类别判定；（b）最近邻决策边界。</p></figure>

若希望最小化误分类概率，应将测试点 $\mathbf{x}$ 归入后验概率最大的类别，也就是 $K_k/K$ 最大的类别。因此，对新点分类时，先找出训练集中最近的 $K$ 个点，再把新点归入这些点中数量最多的类别。出现并列时可以随机决定。$K=1$ 的特殊情形称为*最近邻规则*（nearest-neighbour rule）：测试点直接归入训练集中与它最近的点所属的类别。图 2.27 说明了这些概念。

图 2.28 展示了在第 1 章介绍的油流数据上，不同 $K$ 值下的 $K$ 近邻算法结果。正如预期，$K$ 控制平滑程度：较小的 $K$ 使每个类别形成许多小区域，较大的 $K$ 则产生更少、更大的区域。

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-02/b-fig-2-28.png" alt="油流数据在三种近邻数下的分类区域"><figcaption>图 2.28：油流数据集中的 200 个数据点，图中画出了 $x_6$ 与 $x_7$ 的关系。红色、绿色和蓝色点分别对应“层状流”（laminar）、“环状流”（annular）和“均匀流”（homogeneous）类别。图中还展示了不同 $K$ 值下，$K$ 近邻算法对输入空间给出的分类。</figcaption><p class="figure-translation">从左至右为 $K=1$、$K=3$、$K=31$；横轴 $x_6$、纵轴 $x_7$ 为输入变量；背景颜色表示预测类别。</p></figure>

<!-- pdf-page: 147 -->

最近邻（$K=1$）分类器有一个有趣的性质：在 $N\to\infty$ 的极限下，它的错误率绝不会超过最优分类器可达最小错误率的两倍；这里的最优分类器指使用真实类别分布的分类器（Cover and Hart，1967）。

按照目前的讨论，$K$ 近邻方法和核密度估计都必须存储整个训练集；数据集很大时，计算代价很高。可以通过构造树形搜索结构，在不遍历整个数据集的情况下高效找到（近似）近邻，以一次性的额外计算抵消这种代价。尽管如此，这些非参数方法仍然有很大局限。另一方面，我们已经看到，简单参数模型所能表示的分布形式也非常有限。因此，需要寻找足够灵活、同时其复杂度又能独立于训练集大小加以控制的密度模型。后续章节将介绍如何做到这一点。

## 习题

**2.1（⋆）www** 验证伯努利分布（2.2）满足以下性质：

$$
\sum_{x=0}^{1}p(x\mid\mu)=1,
\tag{2.257}
$$

$$
\mathbb{E}[x]=\mu,
\tag{2.258}
$$

$$
\operatorname{var}[x]=\mu(1-\mu).
\tag{2.259}
$$

证明服从伯努利分布的二元随机变量 $x$ 的熵为

$$
\mathrm{H}[x]=-\mu\ln\mu-(1-\mu)\ln(1-\mu).
\tag{2.260}
$$

**2.2（⋆⋆）** 式（2.2）给出的伯努利分布形式，对 $x$ 的两个取值并不对称。在一些情形下，使用 $x\in\{-1,1\}$ 的等价形式会更方便，此时分布可以写为

$$
p(x\mid\mu)=\left(\frac{1-\mu}{2}\right)^{(1-x)/2}\left(\frac{1+\mu}{2}\right)^{(1+x)/2},
\tag{2.261}
$$

其中 $\mu\in[-1,1]$。证明分布（2.261）已归一化，并求它的均值、方差和熵。

**2.3（⋆⋆）www** 本题证明二项分布（2.9）已归一化。先利用从总共 $N$ 个相同物体中选取 $m$ 个的组合数定义（2.10），证明

$$
\binom{N}{m}+\binom{N}{m-1}=\binom{N+1}{m}.
\tag{2.262}
$$

<!-- pdf-page: 148 -->

利用这个结果，通过归纳法证明

$$
(1+x)^N=\sum_{m=0}^{N}\binom{N}{m}x^m,
\tag{2.263}
$$

这称为*二项式定理*（binomial theorem），对任意实数 $x$ 都成立。最后，证明二项分布已归一化，即

$$
\sum_{m=0}^{N}\binom{N}{m}\mu^m(1-\mu)^{N-m}=1.
\tag{2.264}
$$

可以先从求和中提取因子 $(1-\mu)^N$，再使用二项式定理。

**2.4（⋆⋆）** 证明二项分布的均值由式（2.11）给出。为此，将归一化条件（2.264）两边对 $\mu$ 求导，再整理得到 $n$ 的均值表达式。类似地，将式（2.264）对 $\mu$ 求两次导数，并利用二项分布均值的结果（2.11），证明方差的结果（2.12）。

**2.5（⋆⋆）www** 本题证明式（2.13）给出的Beta 分布已正确归一化，即式（2.14）成立。这等价于证明

$$
\int_0^1\mu^{a-1}(1-\mu)^{b-1}\,\mathrm{d}\mu=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}.
\tag{2.265}
$$

由伽马函数定义（1.141），有

$$
\Gamma(a)\Gamma(b)=\int_0^{\infty}\exp(-x)x^{a-1}\,\mathrm{d}x\int_0^{\infty}\exp(-y)y^{b-1}\,\mathrm{d}y.
\tag{2.266}
$$

按以下步骤利用这个表达式证明式（2.265）：先将对 $y$ 的积分移入对 $x$ 积分的被积函数中；再固定 $x$，作变量代换 $t=y+x$；然后交换 $x$ 和 $t$ 的积分顺序；最后固定 $t$，作变量代换 $x=t\mu$。

**2.6（⋆）** 利用结果（2.265），证明Beta 分布（2.13）的均值、方差和众数分别为

$$
\mathbb{E}[\mu]=\frac{a}{a+b},
\tag{2.267}
$$

$$
\operatorname{var}[\mu]=\frac{ab}{(a+b)^2(a+b+1)},
\tag{2.268}
$$

$$
\operatorname{mode}[\mu]=\frac{a-1}{a+b-2}.
\tag{2.269}
$$

<!-- pdf-page: 149 -->

**2.7（⋆⋆）** 考虑式（2.9）给出的二项随机变量 $x$，$\mu$ 的先验为Beta 分布（2.13）。假设观测到 $m$ 次 $x=1$ 和 $l$ 次 $x=0$。证明，$x$ 的后验均值位于先验均值与 $\mu$ 的最大似然估计之间。为此，证明后验均值可以写为先验均值乘以 $\lambda$，加上最大似然估计乘以 $1-\lambda$，其中 $0\leqslant\lambda\leqslant1$。这说明后验分布在先验分布与最大似然解之间作出了折中。

**2.8（⋆）** 考虑具有联合分布 $p(x,y)$ 的两个变量 $x$ 和 $y$。证明以下两个结果：

$$
\mathbb{E}[x]=\mathbb{E}_y\bigl[\mathbb{E}_x[x\mid y]\bigr],
\tag{2.270}
$$

$$
\operatorname{var}[x]=\mathbb{E}_y\bigl[\operatorname{var}_x[x\mid y]\bigr]+\operatorname{var}_y\bigl[\mathbb{E}_x[x\mid y]\bigr].
\tag{2.271}
$$

这里，$\mathbb{E}_x[x\mid y]$ 表示条件分布 $p(x\mid y)$ 下 $x$ 的期望，条件方差的记号含义类似。

**2.9（⋆⋆⋆）www** 本题利用归纳法证明狄利克雷分布（2.38）的归一化。习题 2.5 已经证明，Beta 分布是归一化的，它是 $M=2$ 时狄利克雷分布的特例。现在假设 $M-1$ 个变量的狄利克雷分布已归一化，证明 $M$ 个变量时也归一化。为此，考虑 $M$ 个变量的狄利克雷分布，利用约束 $\sum_{k=1}^{M}\mu_k=1$ 消去 $\mu_M$，将分布写为

$$
p_M(\mu_1,\ldots,\mu_{M-1})=C_M\prod_{k=1}^{M-1}\mu_k^{\alpha_k-1}\left(1-\sum_{j=1}^{M-1}\mu_j\right)^{\alpha_M-1}.
\tag{2.272}
$$

目标是求出 $C_M$ 的表达式。先对 $\mu_{M-1}$ 积分，注意积分限，再作变量代换，使积分限成为 0 和 1。假设 $C_{M-1}$ 的正确结果成立，并利用式（2.265），推导 $C_M$ 的表达式。

**2.10（⋆⋆）** 利用伽马函数性质 $\Gamma(x+1)=x\Gamma(x)$，推导狄利克雷分布（2.38）的均值、方差和协方差的以下结果：

$$
\mathbb{E}[\mu_j]=\frac{\alpha_j}{\alpha_0},
\tag{2.273}
$$

$$
\operatorname{var}[\mu_j]=\frac{\alpha_j(\alpha_0-\alpha_j)}{\alpha_0^2(\alpha_0+1)},
\tag{2.274}
$$

$$
\operatorname{cov}[\mu_j\mu_l]=-\frac{\alpha_j\alpha_l}{\alpha_0^2(\alpha_0+1)},\qquad j\ne l,
\tag{2.275}
$$

其中 $\alpha_0$ 由式（2.39）定义。

<!-- pdf-page: 150 -->

**2.11（⋆）www** 将狄利克雷分布（2.38）下 $\ln\mu_j$ 的期望表示为对 $\alpha_j$ 的导数，证明

$$
\mathbb{E}[\ln\mu_j]=\psi(\alpha_j)-\psi(\alpha_0),
\tag{2.276}
$$

其中 $\alpha_0$ 由式（2.39）给出，而

$$
\psi(a)\equiv\frac{\mathrm{d}}{\mathrm{d}a}\ln\Gamma(a)
\tag{2.277}
$$

是 *digamma 函数*。

**2.12（⋆）** 连续变量 $x$ 的均匀分布定义为

$$
\mathrm{U}(x\mid a,b)=\frac1{b-a},\qquad a\leqslant x\leqslant b.
\tag{2.278}
$$

验证该分布已归一化，并求出其均值和方差的表达式。

**2.13（⋆⋆）** 计算两个高斯分布 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 和 $q(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\mathbf{m},\mathbf{L})$ 之间的 Kullback–Leibler 散度（1.113）。

**2.14（⋆⋆）www** 本题说明，给定协方差时，熵最大的多元分布是高斯分布。分布 $p(\mathbf{x})$ 的熵为

$$
\mathrm{H}[\mathbf{x}]=-\int p(\mathbf{x})\ln p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{2.279}
$$

我们希望在所有 $p(\mathbf{x})$ 中最大化 $\mathrm{H}[\mathbf{x}]$，约束条件是 $p(\mathbf{x})$ 归一化，并且具有指定的均值和协方差，即

$$
\int p(\mathbf{x})\,\mathrm{d}\mathbf{x}=1,
\tag{2.280}
$$

$$
\int p(\mathbf{x})\mathbf{x}\,\mathrm{d}\mathbf{x}=\boldsymbol{\mu},
\tag{2.281}
$$

$$
\int p(\mathbf{x})(\mathbf{x}-\boldsymbol{\mu})(\mathbf{x}-\boldsymbol{\mu})^{\mathrm T}\,\mathrm{d}\mathbf{x}=\boldsymbol{\Sigma}.
\tag{2.282}
$$

对式（2.279）作变分最大化，并用拉格朗日乘子施加约束（2.280）、（2.281）、（2.282），证明最大似然分布由高斯分布（2.43）给出。

**2.15（⋆⋆）** 证明多元高斯分布 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 的熵为

$$
\mathrm{H}[\mathbf{x}]=\frac12\ln|\boldsymbol{\Sigma}|+\frac D2(1+\ln(2\pi)),
\tag{2.283}
$$

其中 $D$ 为 $\mathbf{x}$ 的维数。

<!-- pdf-page: 151 -->

**2.16（⋆⋆⋆）www** 考虑两个随机变量 $x_1$ 和 $x_2$，它们分别服从均值为 $\mu_1$、$\mu_2$，精度为 $\tau_1$、$\tau_2$ 的高斯分布。推导变量 $x=x_1+x_2$ 的微分熵表达式。为此，先利用关系

$$
p(x)=\int_{-\infty}^{\infty}p(x\mid x_2)p(x_2)\,\mathrm{d}x_2
\tag{2.284}
$$

并在指数中配方，求出 $x$ 的分布。然后注意，这表示两个高斯分布的卷积，其结果本身也是高斯分布；最后利用一元高斯熵的结果（1.110）。

**2.17（⋆）www** 考虑式（2.43）给出的多元高斯分布。将精度矩阵（协方差逆矩阵）$\boldsymbol{\Sigma}^{-1}$ 写为对称矩阵与反对称矩阵之和，证明反对称项不出现在高斯分布的指数中，因此不失一般性，可以令精度矩阵对称。由于对称矩阵的逆矩阵也对称（见习题 2.22），所以不失一般性，也可以令协方差矩阵对称。

**2.18（⋆⋆⋆）** 考虑实对称矩阵 $\boldsymbol{\Sigma}$，其特征值方程由式（2.45）给出。对方程取复共轭并减去原方程，再与特征向量 $\mathbf{u}_i$ 作内积，证明特征值 $\lambda_i$ 为实数。类似地，利用 $\boldsymbol{\Sigma}$ 的对称性，证明只要 $\lambda_j\ne\lambda_i$，特征向量 $\mathbf{u}_i$ 与 $\mathbf{u}_j$ 就正交。最后证明，不失一般性，即使某些特征值为零，也可以选择一组标准正交的特征向量，使它们满足式（2.46）。

**2.19（⋆⋆）** 证明：具有特征向量方程（2.45）的实对称矩阵 $\boldsymbol{\Sigma}$，可以展开为以特征向量为基、特征值为系数的形式，即式（2.48）。类似地，证明逆矩阵 $\boldsymbol{\Sigma}^{-1}$ 具有式（2.49）的表示。

**2.20（⋆⋆）www** 正定矩阵 $\boldsymbol{\Sigma}$ 可以定义为：对向量 $\mathbf{a}$ 的任意实数取值，二次型

$$
\mathbf{a}^{\mathrm T}\boldsymbol{\Sigma}\mathbf{a}
\tag{2.285}
$$

都为正。证明：$\boldsymbol{\Sigma}$ 正定的充要条件，是式（2.45）定义的所有特征值 $\lambda_i$ 均为正。

**2.21（⋆）** 证明，一个 $D\times D$ 的实对称矩阵具有 $D(D+1)/2$ 个独立参数。

**2.22（⋆）www** 证明对称矩阵的逆矩阵本身也是对称矩阵。

**2.23（⋆⋆）** 利用特征向量展开（2.45）将坐标系对角化，证明对应于马氏距离

<!-- pdf-page: 152 -->
<!-- join-previous-paragraph -->
恒为 $\Delta$ 的超椭球，其内部体积为

$$
V_D|\boldsymbol{\Sigma}|^{1/2}\Delta^D,
\tag{2.286}
$$

其中 $V_D$ 是 $D$ 维单位球的体积，马氏距离由式（2.44）定义。

**2.24（⋆⋆）www** 在恒等式（2.76）的两边乘以矩阵

$$
\begin{pmatrix}\mathbf{A}&\mathbf{B}\\\mathbf{C}&\mathbf{D}\end{pmatrix},
\tag{2.287}
$$

并利用定义（2.77），证明该恒等式。

**2.25（⋆⋆）** 第 2.3.1 节和第 2.3.2 节讨论了多元高斯分布的条件分布与边缘分布。更一般地，可以将 $\mathbf{x}$ 的分量划分为三组 $\mathbf{x}_a$、$\mathbf{x}_b$ 和 $\mathbf{x}_c$，相应地将均值向量 $\boldsymbol{\mu}$ 与协方差矩阵 $\boldsymbol{\Sigma}$ 划分为

$$
\boldsymbol{\mu}=\begin{pmatrix}\boldsymbol{\mu}_a\\\boldsymbol{\mu}_b\\\boldsymbol{\mu}_c\end{pmatrix},\qquad
\boldsymbol{\Sigma}=\begin{pmatrix}\boldsymbol{\Sigma}_{aa}&\boldsymbol{\Sigma}_{ab}&\boldsymbol{\Sigma}_{ac}\\\boldsymbol{\Sigma}_{ba}&\boldsymbol{\Sigma}_{bb}&\boldsymbol{\Sigma}_{bc}\\\boldsymbol{\Sigma}_{ca}&\boldsymbol{\Sigma}_{cb}&\boldsymbol{\Sigma}_{cc}\end{pmatrix}.
\tag{2.288}
$$

利用第 2.3 节的结果，求出将 $\mathbf{x}_c$ 边缘化后，条件分布 $p(\mathbf{x}_a\mid\mathbf{x}_b)$ 的表达式。

**2.26（⋆⋆）** 线性代数中一个很有用的结果是 *Woodbury 矩阵求逆公式*：

$$
(\mathbf{A}+\mathbf{B}\mathbf{C}\mathbf{D})^{-1}=\mathbf{A}^{-1}-\mathbf{A}^{-1}\mathbf{B}(\mathbf{C}^{-1}+\mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1}\mathbf{D}\mathbf{A}^{-1}.
\tag{2.289}
$$

将两边乘以 $(\mathbf{A}+\mathbf{B}\mathbf{C}\mathbf{D})$，证明这个结果正确。

**2.27（⋆）** 设 $\mathbf{x}$ 与 $\mathbf{z}$ 为两个独立随机向量，即 $p(\mathbf{x},\mathbf{z})=p(\mathbf{x})p(\mathbf{z})$。证明，它们之和 $\mathbf{y}=\mathbf{x}+\mathbf{z}$ 的均值等于两个变量各自均值之和。类似地，证明 $\mathbf{y}$ 的协方差矩阵等于 $\mathbf{x}$ 与 $\mathbf{z}$ 的协方差矩阵之和。确认这个结果与习题 1.10 一致。

**2.28（⋆⋆⋆）www** 考虑变量

$$
\mathbf{z}=\begin{pmatrix}\mathbf{x}\\\mathbf{y}\end{pmatrix}
\tag{2.290}
$$

的联合分布，其均值和协方差分别由式（2.108）与（2.105）给出。利用结果（2.92）和（2.93），证明边缘分布 $p(\mathbf{x})$ 由式（2.99）给出。类似地，利用结果（2.81）和（2.82），证明条件分布 $p(\mathbf{y}\mid\mathbf{x})$ 由式（2.100）给出。

<!-- pdf-page: 153 -->

**2.29（⋆⋆）** 利用分块矩阵求逆公式（2.76），证明精度矩阵（2.104）的逆矩阵就是协方差矩阵（2.105）。

**2.30（⋆）** 从式（2.107）出发，并利用结果（2.105），验证结果（2.108）。

**2.31（⋆⋆）** 考虑两个多维随机向量 $\mathbf{x}$ 和 $\mathbf{z}$，分别服从高斯分布 $p(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu}_x,\boldsymbol{\Sigma}_x)$ 和 $p(\mathbf{z})=\mathcal{N}(\mathbf{z}\mid\boldsymbol{\mu}_z,\boldsymbol{\Sigma}_z)$，以及它们的和 $\mathbf{y}=\mathbf{x}+\mathbf{z}$。考虑由边缘分布 $p(\mathbf{x})$ 与条件分布 $p(\mathbf{y}\mid\mathbf{x})$ 的乘积构成的线性高斯模型，利用结果（2.109）和（2.110），求出边缘分布 $p(\mathbf{y})$ 的表达式。

**2.32（⋆⋆⋆）www** 本题和下一题用于练习处理线性高斯模型中的二次型，同时独立核对正文推导的结果。考虑由边缘分布（2.99）和条件分布（2.100）定义的联合分布 $p(\mathbf{x},\mathbf{y})$。考察联合分布指数中的二次型，使用第 2.3 节讨论的“配方”方法，求出将变量 $\mathbf{x}$ 积分消去后，边缘分布 $p(\mathbf{y})$ 的均值和协方差表达式。为此，使用 Woodbury 矩阵求逆公式（2.289）。验证这些结果与利用第 2 章结果所得的式（2.109）、（2.110）一致。

**2.33（⋆⋆⋆）** 考虑与习题 2.32 相同的联合分布，这次用配方方法求出条件分布 $p(\mathbf{x}\mid\mathbf{y})$ 的均值和协方差。再次验证，它们与相应的式（2.111）、（2.112）一致。

**2.34（⋆⋆）www** 为求多元高斯分布协方差矩阵的最大似然解，需要关于 $\boldsymbol{\Sigma}$ 最大化对数似然函数（2.118），同时注意协方差矩阵必须对称且正定。这里先忽略这些约束，直接最大化。利用附录 C 的结果（C.21）、（C.26）和（C.28），证明使对数似然函数（2.118）最大的协方差矩阵 $\boldsymbol{\Sigma}$，由样本协方差（2.122）给出。注意，最终结果必然对称且正定（只要样本协方差非奇异）。

**2.35（⋆⋆）** 利用结果（2.59）证明式（2.62）。然后结合结果（2.59）和（2.62），证明

$$
\mathbb{E}[\mathbf{x}_n\mathbf{x}_m]=\boldsymbol{\mu}\boldsymbol{\mu}^{\mathrm T}+I_{nm}\boldsymbol{\Sigma},
\tag{2.291}
$$

其中 $\mathbf{x}_n$ 表示从均值为 $\boldsymbol{\mu}$、协方差为 $\boldsymbol{\Sigma}$ 的高斯分布抽取的数据点，$I_{nm}$ 为单位矩阵的第 $(n,m)$ 个元素。由此证明结果（2.124）。

**2.36（⋆⋆）www** 采用与推导式（2.126）类似的步骤，推导一元高斯

<!-- pdf-page: 154 -->
<!-- join-previous-paragraph -->
分布方差的序贯估计表达式，从以下最大似然表达式出发：

$$
\sigma_{\mathrm{ML}}^2=\frac1N\sum_{n=1}^{N}(x_n-\mu)^2.
\tag{2.292}
$$

验证，将高斯分布的表达式代入 Robbins–Monro 序贯估计公式（2.135），会得到相同形式的结果，并由此求出相应系数 $a_N$ 的表达式。

**2.37（⋆⋆）** 采用与推导式（2.126）类似的步骤，从最大似然表达式（2.122）出发，推导多元高斯分布协方差的序贯估计表达式。验证，将高斯分布的表达式代入 Robbins–Monro 序贯估计公式（2.135），会得到相同形式的结果，并由此求出相应系数 $a_N$ 的表达式。

**2.38（⋆）** 对指数中的二次型使用配方方法，推导结果（2.141）和（2.142）。

**2.39（⋆⋆）** 从高斯随机变量均值的后验分布结果（2.141）和（2.142）出发，分离前 $N-1$ 个数据点的贡献，由此求出 $\mu_N$ 和 $\sigma_N^2$ 的序贯更新表达式。再从后验分布 $p(\mu\mid x_1,\ldots,x_{N-1})=\mathcal{N}(\mu\mid\mu_{N-1},\sigma_{N-1}^2)$ 出发，乘以似然函数 $p(x_N\mid\mu)=\mathcal{N}(x_N\mid\mu,\sigma^2)$，通过配方并归一化得到 $N$ 次观测后的后验分布，从而推导相同的结果。

**2.40（⋆⋆）www** 考虑 $D$ 维高斯随机变量 $\mathbf{x}$，其分布为 $\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，协方差 $\boldsymbol{\Sigma}$ 已知。我们希望根据观测集 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 推断均值 $\boldsymbol{\mu}$。给定先验分布 $p(\boldsymbol{\mu})=\mathcal{N}(\boldsymbol{\mu}\mid\boldsymbol{\mu}_0,\boldsymbol{\Sigma}_0)$，求相应的后验分布 $p(\boldsymbol{\mu}\mid\mathbf{X})$。

**2.41（⋆）** 利用伽马函数定义（1.141），证明伽马分布（2.146）已归一化。

**2.42（⋆⋆）** 求伽马分布（2.146）的均值、方差和众数。

**2.43（⋆）** 以下分布是一元高斯分布的推广：

$$
p(x\mid\sigma^2,q)=\frac{q}{2(2\sigma^2)^{1/q}\Gamma(1/q)}\exp\left(-\frac{|x|^q}{2\sigma^2}\right).
\tag{2.293}
$$

证明它已归一化，即

$$
\int_{-\infty}^{\infty}p(x\mid\sigma^2,q)\,\mathrm{d}x=1,
\tag{2.294}
$$

并且在 $q=2$ 时退化为高斯分布。考虑一个回归模型，目标变量为 $t=y(\mathbf{x},\mathbf{w})+\epsilon$，其中 $\epsilon$ 是从分布（2.293）抽取的随机噪声

<!-- pdf-page: 155 -->
<!-- join-previous-paragraph -->
变量。证明，对于由输入向量 $\mathbf{X}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 和相应目标变量 $\boldsymbol{\mathsf{t}}=(t_1,\ldots,t_N)^{\mathrm T}$ 组成的观测数据集，关于 $\mathbf{w}$ 和 $\sigma^2$ 的对数似然函数为

$$
\ln p(\boldsymbol{\mathsf{t}}\mid\mathbf{X},\mathbf{w},\sigma^2)=-\frac1{2\sigma^2}\sum_{n=1}^{N}|y(\mathbf{x}_n,\mathbf{w})-t_n|^q-\frac Nq\ln(2\sigma^2)+\mathrm{const},
\tag{2.295}
$$

其中 “const” 表示与 $\mathbf{w}$ 及 $\sigma^2$ 都无关的项。注意，将其看作 $\mathbf{w}$ 的函数，它就是第 1.5.5 节讨论的 $L_q$ 误差函数。

**2.44（⋆⋆）** 考虑一元高斯分布 $\mathcal{N}(x\mid\mu,\tau^{-1})$，其共轭高斯-伽马先验由式（2.154）给出。给定独立同分布观测构成的数据集 $\boldsymbol{\mathsf{x}}=\{x_1,\ldots,x_N\}$，证明后验分布仍为与先验具有相同函数形式的高斯-伽马分布，并写出后验分布各参数的表达式。

**2.45（⋆）** 验证式（2.155）定义的 Wishart 分布，确实是多元高斯分布精度矩阵的共轭先验。

**2.46（⋆）www** 验证，计算式（2.158）中的积分会得到结果（2.159）。

**2.47（⋆）www** 证明，在 $\nu\to\infty$ 的极限下，t 分布（2.159）变为高斯分布。提示：忽略归一化系数，只考察对 $x$ 的依赖。

**2.48（⋆）** 按照与推导一元 Student t 分布（2.159）类似的步骤，对式（2.161）中的变量 $\eta$ 进行边缘化，验证多元 Student t 分布的结果（2.162）。利用定义（2.161），通过交换积分变量，证明多元 t 分布正确归一化。

**2.49（⋆⋆）** 利用式（2.161）把多元 Student t 分布定义为高斯分布与伽马分布的卷积，验证式（2.162）定义的多元 t 分布的性质（2.164）、（2.165）和（2.166）。

**2.50（⋆）** 证明，在 $\nu\to\infty$ 的极限下，多元 Student t 分布（2.162）退化为均值 $\boldsymbol{\mu}$、精度 $\boldsymbol{\Lambda}$ 的高斯分布。

**2.51（⋆）www** 本章讨论周期变量时使用的各种三角恒等式，都可以容易地由以下关系证明：

$$
\exp(\mathrm{i}A)=\cos A+\mathrm{i}\sin A,
\tag{2.296}
$$

其中 $\mathrm{i}$ 是负一的平方根。考虑恒等式

$$
\exp(\mathrm{i}A)\exp(-\mathrm{i}A)=1,
\tag{2.297}
$$

证明结果（2.177）。类似地，利用恒等式

$$
\cos(A-B)=\Re\exp\{\mathrm{i}(A-B)\},
\tag{2.298}
$$

<!-- pdf-page: 156 -->

其中 $\Re$ 表示实部，证明式（2.178）。最后，利用 $\sin(A-B)=\Im\exp\{\mathrm{i}(A-B)\}$（$\Im$ 表示虚部），证明结果（2.183）。

**2.52（⋆⋆）** 当 $m$ 很大时，von Mises 分布（2.179）在众数 $\theta_0$ 附近形成尖峰。定义 $\xi=m^{1/2}(\theta-\theta_0)$，并使用余弦函数的泰勒展开

$$
\cos\alpha=1-\frac{\alpha^2}{2}+O(\alpha^4),
\tag{2.299}
$$

证明当 $m\to\infty$ 时，von Mises 分布趋于高斯分布。

**2.53（⋆）** 利用三角恒等式（2.183），证明式（2.182）关于 $\theta_0$ 的解由式（2.184）给出。

**2.54（⋆）** 计算 von Mises 分布（2.179）的一阶和二阶导数，并利用 $m>0$ 时 $I_0(m)>0$，证明分布在 $\theta=\theta_0$ 时取最大值，在 $\theta=\theta_0+\pi\pmod{2\pi}$ 时取最小值。

**2.55（⋆）** 结合结果（2.168）、（2.184）与三角恒等式（2.178），证明 von Mises 分布集中参数的最大似然解 $m_{\mathrm{ML}}$ 满足 $A(m_{\mathrm{ML}})=\overline{r}$，其中 $\overline{r}$ 是将观测看作二维欧氏平面上的单位向量后，其平均向量的长度，如图 2.17 所示。

**2.56（⋆⋆）www** 将Beta 分布（2.13）、伽马分布（2.146）和 von Mises 分布（2.179）写成指数族（2.194）的成员，并确定它们的自然参数。

**2.57（⋆）** 验证多元高斯分布可以写成指数族形式（2.194），并推导与式（2.220）至（2.223）类似的 $\boldsymbol{\eta}$、$\mathbf{u}(\mathbf{x})$、$h(\mathbf{x})$ 和 $g(\boldsymbol{\eta})$ 的表达式。

**2.58（⋆）** 结果（2.226）表明，指数族中 $\ln g(\boldsymbol{\eta})$ 的负梯度由 $\mathbf{u}(\mathbf{x})$ 的期望给出。对式（2.195）求二阶导数，证明

$$
-\nabla\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}[\mathbf{u}(\mathbf{x})\mathbf{u}(\mathbf{x})^{\mathrm T}]-\mathbb{E}[\mathbf{u}(\mathbf{x})]\mathbb{E}[\mathbf{u}(\mathbf{x})^{\mathrm T}]=\operatorname{cov}[\mathbf{u}(\mathbf{x})].
\tag{2.300}
$$

**2.59（⋆）** 作变量代换 $y=x/\sigma$，证明只要 $f(x)$ 正确归一化，密度（2.236）也会正确归一化。

**2.60（⋆⋆）www** 考虑类似直方图的密度模型：将空间 $\mathbf{x}$ 划分为固定区域，第 $i$ 个区域内密度 $p(\mathbf{x})$ 取常数 $h_i$，区域体积记为 $\Delta_i$。假设有 $N$ 个关于 $\mathbf{x}$ 的观测，其中 $n_i$ 个落在第 $i$ 个区域。利用拉格朗日乘子施加密度归一化约束，推导 $\{h_i\}$ 的最大似然估计表达式。

**2.61（⋆）** 证明，$K$ 近邻密度模型定义了一个非正常分布，它在整个空间上的积分发散。
