<!-- pdf-page: 513 -->

## 10.5 局部变分方法

10.1 节和 10.2 节讨论的变分框架可以看作一种“全局”方法，因为它直接寻找所有随机变量的完整后验分布的近似。另一种“局部”方法，则为模型中单个变量或变量组上的函数寻找界。例如，我们可以为条件分布 $p(y\mid x)$ 寻找一个界，而这个条件分布本身只是在有向图所描述的更大概率模型中的一个因子。引入这个界的目的，当然是简化所得的分布。可以依次对多个变量应用这种局部近似，直到得到一个可处理的近似；在 10.6.1 节中，我们将以逻辑回归为背景，给出这种方法的实际例子。这里先着重讨论如何构造这些界。

在讨论 Kullback–Leibler 散度时，我们已经看到，对数函数的凸性在构造全局变分方法的下界时起了关键作用。此前，我们把（严格）凸函数定义为每条弦都位于函数图像上方的函数（1.6.1 节）。凸性在局部变分框架中同样起着核心作用。注意，只要互换“min”和“max”，并将下界换为上界，以下讨论也同样适用于凹函数。

先考虑一个简单例子，即函数 $f(x)=\exp(-x)$。它是关于 $x$ 的凸函数，如图 10.10 左图所示。我们的目标是用一个更简单的函数来近似 $f(x)$，具体而言，用 $x$ 的线性函数。由图 10.10 可以看到，如果这个线性函数对应于一条切线，它就是 $f(x)$ 的下界。对某个特定的 $x$ 值，例如 $x=\xi$，作一阶泰勒展开，就能得到切线 $y(x)$：

$$
y(x)=f(\xi)+f'(\xi)(x-\xi)
\tag{10.125}
$$

因此 $y(x)\leqslant f(x)$，在 $x=\xi$ 时取等号。对于我们的示例函数 $f(x)=$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-10.png" alt="左图以红色指数曲线及蓝绿切线示意下界，右图显示对偶目标关于斜率的最大值"><figcaption>图 10.10：左图中的红色曲线表示函数 $\exp(-x)$，蓝色直线表示由（10.125）定义的、在 $x=\xi$ 处的切线，其中 $\xi=1$。这条直线的斜率为 $\lambda=f'(\xi)=-\exp(-\xi)$。注意，任何其他切线，例如图中的绿色直线，在 $x=\xi$ 处都会有更小的 $y$ 值。右图给出了相应的函数 $\lambda\xi-g(\lambda)$ 关于 $\lambda$ 的图像，其中 $g(\lambda)$ 由（10.131）给出，$\xi=1$；最大值对应于 $\lambda=-\exp(-\xi)=-1/e$。</figcaption><p class="figure-translation">$x$：自变量；$\xi$：切点的横坐标；$\lambda$：切线斜率；$\lambda\xi-g(\lambda)$：在给定 $\xi$ 处的对偶表达式。</p></figure>

<!-- pdf-page: 514 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-11.png" alt="凸函数与给定斜率直线之间的最短竖直距离决定切线截距，左右两图展示上移前后"><figcaption>图 10.11：左图中的红色曲线表示凸函数 $f(x)$，蓝色直线表示线性函数 $\lambda x$。它是 $f(x)$ 的下界，因为对所有 $x$ 都有 $f(x)>\lambda x$。对于给定的斜率 $\lambda$，关于 $x$ 最小化差值 $f(x)-\lambda x$（以绿色虚线表示），就能找到具有相同斜率的切线的切点。由此定义对偶函数 $g(\lambda)$，它对应于斜率为 $\lambda$ 的切线的截距的负值。</figcaption><p class="figure-translation">$x$、$y$：横轴和纵轴变量；$f(x)$：凸函数；$\lambda x$：上移前的直线；$\lambda x-g(\lambda)$：切线；$-g(\lambda)$：切线在纵轴上的截距。</p></figure>

<!-- join-previous-paragraph-across-figures -->
$\exp(-x)$，因此得到如下形式的切线：

$$
y(x)=\exp(-\xi)-\exp(-\xi)(x-\xi)
\tag{10.126}
$$

这是一个由 $\xi$ 参数化的线性函数。为与后面的讨论一致，定义 $\lambda=-\exp(-\xi)$，于是

$$
y(x,\lambda)=\lambda x-\lambda+\lambda\ln(-\lambda).
\tag{10.127}
$$

不同的 $\lambda$ 值对应不同的切线；由于所有这些直线都是函数的下界，有 $f(x)\geqslant y(x,\lambda)$。因此，可以将该函数写为

$$
f(x)=\max_{\lambda}\{\lambda x-\lambda+\lambda\ln(-\lambda)\}.
\tag{10.128}
$$

我们已经成功地用一个更简单的线性函数 $y(x,\lambda)$ 来近似凸函数 $f(x)$。付出的代价是引入了一个变分参数 $\lambda$；为得到最紧的界，必须关于 $\lambda$ 进行优化。

利用*凸对偶性*（convex duality）的框架，可以更一般地表述这种方法（Rockafellar, 1972; Jordan et al., 1999）。考虑图 10.11 左图所示的凸函数 $f(x)$。在这个例子中，函数 $\lambda x$ 是 $f(x)$ 的下界，但它不是斜率为 $\lambda$ 的线性函数所能达到的最佳下界，因为最紧的界由切线给出。将斜率为 $\lambda$ 的切线方程写成 $\lambda x-g(\lambda)$，其中截距的负值 $g(\lambda)$ 显然依赖于切线斜率 $\lambda$。为了确定截距，注意，直线必须竖直移动一段距离，其大小等于直线与函数之间的最小竖直距离，如图 10.11 所示。因此

$$
\begin{aligned}
g(\lambda)&=-\min_x\{f(x)-\lambda x\}\\
&=\max_x\{\lambda x-f(x)\}.
\end{aligned}
\tag{10.129}
$$

<!-- pdf-page: 515 -->

现在，可以不固定 $\lambda$ 并改变 $x$，而是考虑一个特定的 $x$，然后调整 $\lambda$，直到切平面恰好在这个 $x$ 处相切。因为对于某个特定的 $x$，当它恰好对应于切点时，切线的 $y$ 值达到最大，所以有

$$
f(x)=\max_{\lambda}\{\lambda x-g(\lambda)\}.
\tag{10.130}
$$

可以看到，函数 $f(x)$ 和 $g(\lambda)$ 具有对偶的作用，并通过（10.129）和（10.130）相联系。

将这些对偶关系应用于简单例子 $f(x)=\exp(-x)$。由（10.129）可知，使其达到最大值的 $x$ 由 $\xi=-\ln(-\lambda)$ 给出，回代后得到共轭函数 $g(\lambda)$：

$$
g(\lambda)=\lambda-\lambda\ln(-\lambda)
\tag{10.131}
$$

这与前面得到的结果相同。图 10.10 右图显示了 $\xi=1$ 时的函数 $\lambda\xi-g(\lambda)$。为了验证，将（10.131）代入（10.130），得到使其达到最大值的 $\lambda=-\exp(-x)$，再回代就恢复了原函数 $f(x)=\exp(-x)$。

对于凹函数，可以通过类似论证得到上界，只需把“max”换成“min”，于是

$$
f(x)=\min_{\lambda}\{\lambda x-g(\lambda)\}
\tag{10.132}
$$

$$
g(\lambda)=\min_x\{\lambda x-f(x)\}.
\tag{10.133}
$$

如果所关注的函数不是凸函数（或凹函数），就不能直接应用上述方法来得到界。不过，可以先对函数或其自变量寻找可逆变换，将其变为凸形式。然后计算共轭函数，再变换回原来的变量。

一个在模式识别中经常出现的重要例子，是如下定义的 logistic sigmoid 函数：

$$
\sigma(x)=\frac{1}{1+e^{-x}}.
\tag{10.134}
$$

这个函数本身既不是凸函数，也不是凹函数。不过，对它取对数后得到的是凹函数，这很容易通过求二阶导数来验证（习题 10.30）。根据（10.133），相应的共轭函数具有如下形式：

$$
g(\lambda)=\min_x\{\lambda x-f(x)\}=-\lambda\ln\lambda-(1-\lambda)\ln(1-\lambda)
\tag{10.135}
$$

可以看出，这正是一个取值为 $1$ 的概率为 $\lambda$ 的变量的二元熵函数（附录 B）。利用（10.132），得到对数 sigmoid 的上界：

$$
\ln\sigma(x)\leqslant\lambda x-g(\lambda)
\tag{10.136}
$$

<!-- pdf-page: 516 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-12.png" alt="左图以指数函数给出logistic sigmoid的两个上界，右图以高斯形函数给出在正负ξ处相切的下界"><figcaption>图 10.12：左图以红色显示（10.134）定义的 logistic sigmoid 函数 $\sigma(x)$，并以蓝色显示指数上界（10.137）的两个例子。右图同样以红色显示 logistic sigmoid，以蓝色显示高斯下界（10.144）。这里参数 $\xi=2.5$，在绿色虚线标出的 $x=\xi$ 和 $x=-\xi$ 处，这个界是精确的。</figcaption><p class="figure-translation">左图的 $\lambda=0.2$ 和 $\lambda=0.7$ 为两个上界的参数值；右图的 $\xi=2.5$ 为下界参数，$-\xi$ 与 $\xi$ 标出下界与原函数相等的两个位置。</p></figure>

对两边取指数，就得到 logistic sigmoid 本身的上界：

$$
\sigma(x)\leqslant\exp(\lambda x-g(\lambda))
\tag{10.137}
$$

图 10.12 左图绘出了两个不同 $\lambda$ 值对应的上界。

我们还可以得到一个具有高斯函数形式的 sigmoid 下界。为此，按照 Jaakkola and Jordan（2000）的方法，同时对输入变量和函数本身作变换。首先对 logistic 函数取对数，再分解为

$$
\begin{aligned}
\ln\sigma(x)&=-\ln(1+e^{-x})=-\ln\left\{e^{-x/2}(e^{x/2}+e^{-x/2})\right\}\\
&=x/2-\ln(e^{x/2}+e^{-x/2}).
\end{aligned}
\tag{10.138}
$$

注意，函数 $f(x)=-\ln(e^{x/2}+e^{-x/2})$ 是变量 $x^2$ 的凸函数，这同样可以通过求二阶导数来验证（习题 10.31）。由此得到 $f(x)$ 的下界，它是 $x^2$ 的线性函数，其共轭函数为

$$
g(\lambda)=\max_{x^2}\left\{\lambda x^2-f\left(\sqrt{x^2}\right)\right\}.
\tag{10.139}
$$

驻点条件给出

$$
0=\lambda-\frac{dx}{dx^2}\frac{d}{dx}f(x)=\lambda+\frac{1}{4x}\tanh\left(\frac{x}{2}\right).
\tag{10.140}
$$

将这个 $x$ 值记为 $\xi$，它对应于给定 $\lambda$ 值时切线的切点，于是

$$
\lambda(\xi)=-\frac{1}{4\xi}\tanh\left(\frac{\xi}{2}\right)=-\frac{1}{2\xi}\left[\sigma(\xi)-\frac{1}{2}\right].
\tag{10.141}
$$

<!-- pdf-page: 517 -->

可以让 $\xi$ 而不是 $\lambda$ 充当变分参数，因为这样能得到更简单的共轭函数表达式：

$$
g(\lambda)=\lambda(\xi)\xi^2-f(\xi)=\lambda(\xi)\xi^2+\ln(e^{\xi/2}+e^{-\xi/2}).
\tag{10.142}
$$

因此，$f(x)$ 的界可以写成

$$
f(x)\geqslant\lambda x^2-g(\lambda)=\lambda x^2-\lambda\xi^2-\ln(e^{\xi/2}+e^{-\xi/2}).
\tag{10.143}
$$

于是，sigmoid 的界变为

$$
\sigma(x)\geqslant\sigma(\xi)\exp\left\{(x-\xi)/2-\lambda(\xi)(x^2-\xi^2)\right\}
\tag{10.144}
$$

其中 $\lambda(\xi)$ 由（10.141）定义。图 10.12 右图展示了这个界。可以看到，它具有对 $x$ 的二次函数取指数的形式；当我们希望用高斯分布表示通过 logistic sigmoid 函数定义的后验分布时，这种形式将很有用（4.5 节）。

logistic sigmoid 经常出现在二元变量的概率模型中，因为它能把对数几率转换为后验概率。对于多类别分布，相应的变换由 softmax 函数给出（4.3 节）。遗憾的是，这里为 logistic sigmoid 推导的下界不能直接推广到 softmax。Gibbs（1997）提出了一种构造高斯分布的方法，并推测该分布是一个界（虽然没有给出严格证明）；这种方法可以将局部变分方法应用于多类别问题。

我们将在 10.6.1 节看到局部变分界的应用示例。不过，现在先从一般角度考察如何使用这些界，会有助于理解。假设要计算如下形式的积分：

$$
I=\int\sigma(a)p(a)\,da
\tag{10.145}
$$

其中 $\sigma(a)$ 是 logistic sigmoid，$p(a)$ 是高斯概率密度。例如，在贝叶斯模型中计算预测分布时，就会出现这样的积分，此时 $p(a)$ 表示参数的后验分布。由于这个积分难以求解，我们采用变分界（10.144），并将其写成 $\sigma(a)\geqslant f(a,\xi)$，其中 $\xi$ 是变分参数。积分中的函数现在成为两个二次指数函数的乘积，因此可以解析积分，得到 $I$ 的界：

$$
I\geqslant\int f(a,\xi)p(a)\,da=F(\xi).
\tag{10.146}
$$

现在可以自由选择变分参数 $\xi$；具体做法是寻找使函数 $F(\xi)$ 最大的值 $\xi^{\star}$。所得的 $F(\xi^{\star})$ 表示这一族界中最紧的界，可以用来近似 $I$。不过，这个优化后的界通常并不精确。

<!-- pdf-page: 518 -->
<!-- join-previous-paragraph -->
虽然 logistic sigmoid 的界 $\sigma(a)\geqslant f(a,\xi)$ 可以精确优化，但所需的 $\xi$ 取值依赖于 $a$，所以这个界只在一个 $a$ 值处精确。由于 $F(\xi)$ 是对 $a$ 的所有取值积分得到的，$\xi^{\star}$ 就代表一种由分布 $p(a)$ 加权的折中。

## 10.6 变分逻辑回归

现在回到 4.5 节研究的贝叶斯逻辑回归模型，以此说明局部变分方法的使用。此前我们着重使用拉普拉斯近似，这里则考虑基于 Jaakkola and Jordan（2000）方法的变分处理。与拉普拉斯方法一样，这种处理也得到后验分布的高斯近似。不过，变分近似具有更大的灵活性，因此比拉普拉斯方法更精确。此外，与拉普拉斯方法不同，变分方法优化的是一个定义明确的目标函数，它由模型证据的严格界给出。Dybowski and Roberts（2005）还使用蒙特卡洛采样技术，从贝叶斯角度研究了逻辑回归。

### 10.6.1 变分后验分布

这里将使用基于 10.5 节所介绍的局部界的变分近似。这样，由 logistic sigmoid 决定的逻辑回归似然函数，就能用一个二次型的指数来近似。因此，再次选用（4.140）形式的共轭高斯先验会很方便。暂时把超参数 $\mathbf{m}_0$ 和 $\mathbf{S}_0$ 视为固定常数。10.6.3 节将说明，如何把变分方法推广到存在未知超参数、需要从数据推断这些超参数取值的情况。

在变分框架中，我们希望最大化边缘似然的下界。对于贝叶斯逻辑回归模型，边缘似然具有如下形式：

$$
p(\boldsymbol{\mathsf{t}})=\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\,d\mathbf{w}=\int\left[\prod_{n=1}^{N}p(t_n\mid\mathbf{w})\right]p(\mathbf{w})\,d\mathbf{w}.
\tag{10.147}
$$

首先注意，$t$ 的条件分布可以写成

$$
\begin{aligned}
p(t\mid\mathbf{w})&=\sigma(a)^t\{1-\sigma(a)\}^{1-t}\\
&=\left(\frac{1}{1+e^{-a}}\right)^t\left(1-\frac{1}{1+e^{-a}}\right)^{1-t}\\
&=e^{at}\frac{e^{-a}}{1+e^{-a}}=e^{at}\sigma(-a)
\end{aligned}
\tag{10.148}
$$

其中 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$。为了得到 $p(\boldsymbol{\mathsf{t}})$ 的下界，我们利用（10.144）给出的 logistic sigmoid 函数的变分下界。为方便起见，

<!-- pdf-page: 519 -->
<!-- join-previous-paragraph -->
在这里将它重列如下：

$$
\sigma(z)\geqslant\sigma(\xi)\exp\left\{(z-\xi)/2-\lambda(\xi)(z^2-\xi^2)\right\}
\tag{10.149}
$$

其中

$$
\lambda(\xi)=\frac{1}{2\xi}\left[\sigma(\xi)-\frac{1}{2}\right].
\tag{10.150}
$$

因此，可以写成

$$
p(t\mid\mathbf{w})=e^{at}\sigma(-a)\geqslant e^{at}\sigma(\xi)\exp\left\{-(a+\xi)/2-\lambda(\xi)(a^2-\xi^2)\right\}.
\tag{10.151}
$$

注意，由于这个界分别应用于似然函数中的每一项，每个训练集观测 $(\boldsymbol{\phi}_n,t_n)$ 都对应一个变分参数 $\xi_n$。使用 $a=\mathbf{w}^{\mathrm T}\boldsymbol{\phi}$，再乘以先验分布，得到 $\boldsymbol{\mathsf{t}}$ 和 $\mathbf{w}$ 的联合分布的如下界：

$$
p(\boldsymbol{\mathsf{t}},\mathbf{w})=p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\geqslant h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})
\tag{10.152}
$$

其中 $\boldsymbol{\xi}$ 表示变分参数的集合 $\{\xi_n\}$，并且

$$
\begin{aligned}
h(\mathbf{w},\boldsymbol{\xi})={}&\prod_{n=1}^{N}\sigma(\xi_n)\exp\Bigl\{\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n t_n-(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n+\xi_n)/2\\
&-\lambda(\xi_n)([\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n]^2-\xi_n^2)\Bigr\}.
\end{aligned}
\tag{10.153}
$$

计算精确后验分布，需要将这个不等式的左侧归一化。由于这难以处理，我们改为处理右侧。注意，右侧函数尚未归一化，因此不能解释为概率密度。不过，一旦将它归一化，得到变分后验分布 $q(\mathbf{w})$，它就不再表示一个界。

由于对数函数单调递增，不等式 $A\geqslant B$ 意味着 $\ln A\geqslant\ln B$。由此得到 $\boldsymbol{\mathsf{t}}$ 和 $\mathbf{w}$ 的联合分布的对数下界：

$$
\begin{aligned}
\ln\{p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\}\geqslant{}&\ln p(\mathbf{w})+\sum_{n=1}^{N}\Bigl\{\ln\sigma(\xi_n)+\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n t_n\\
&-(\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n+\xi_n)/2-\lambda(\xi_n)([\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n]^2-\xi_n^2)\Bigr\}.
\end{aligned}
\tag{10.154}
$$

代入先验 $p(\mathbf{w})$，这个不等式的右侧作为 $\mathbf{w}$ 的函数，变为

$$
\begin{aligned}
&-\frac{1}{2}(\mathbf{w}-\mathbf{m}_0)^{\mathrm T}\mathbf{S}_0^{-1}(\mathbf{w}-\mathbf{m}_0)\\
&+\sum_{n=1}^{N}\left\{\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n(t_n-1/2)-\lambda(\xi_n)\mathbf{w}^{\mathrm T}(\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T})\mathbf{w}\right\}+\mathrm{const}.
\end{aligned}
\tag{10.155}
$$

<!-- pdf-page: 520 -->

这是 $\mathbf{w}$ 的二次函数，因此可以通过识别 $\mathbf{w}$ 的一次项和二次项，得到相应的后验分布变分近似，从而得到如下形式的高斯变分后验：

$$
q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_N,\mathbf{S}_N)
\tag{10.156}
$$

其中

$$
\mathbf{m}_N=\mathbf{S}_N\left(\mathbf{S}_0^{-1}\mathbf{m}_0+\sum_{n=1}^{N}(t_n-1/2)\boldsymbol{\phi}_n\right)
\tag{10.157}
$$

$$
\mathbf{S}_N^{-1}=\mathbf{S}_0^{-1}+2\sum_{n=1}^{N}\lambda(\xi_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{10.158}
$$

与拉普拉斯框架一样，我们再次得到了后验分布的高斯近似。不过，变分参数 $\{\xi_n\}$ 提供了额外的灵活性，提高了近似的精度（Jaakkola and Jordan，2000）。

这里考虑的是一次性获得全部训练数据的批量学习情形。不过，贝叶斯方法本来就很适合序贯学习：每次处理一个数据点，处理后就将它丢弃。将这个变分方法写成序贯形式很直接（习题 10.32）。

注意，（10.149）给出的界只适用于两类问题，因此这种方法不能直接推广到具有 $K>2$ 个类别的分类问题。Gibbs（1997）研究了适用于多类别情形的另一种界。

### 10.6.2 优化变分参数

现在已经得到了后验分布的归一化高斯近似，稍后将用它计算新数据点的预测分布。不过，首先需要通过最大化边缘似然的下界，来确定变分参数 $\{\xi_n\}$。

为此，将不等式（10.152）代回边缘似然，得到

$$
\ln p(\boldsymbol{\mathsf{t}})=\ln\int p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w})\,d\mathbf{w}\geqslant\ln\int h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})\,d\mathbf{w}=\mathcal{L}(\boldsymbol{\xi}).
\tag{10.159}
$$

与 3.5 节线性回归模型中超参数 $\alpha$ 的优化一样，确定 $\xi_n$ 有两种方法。第一种方法注意到，函数 $\mathcal{L}(\boldsymbol{\xi})$ 是通过对 $\mathbf{w}$ 积分定义的，因此可以把 $\mathbf{w}$ 视为潜变量，并使用 EM 算法。第二种方法先对 $\mathbf{w}$ 作解析积分，再直接关于 $\boldsymbol{\xi}$ 最大化。先考虑 EM 方法。

EM 算法首先为参数 $\{\xi_n\}$ 选择初始值，将它们合记为 $\boldsymbol{\xi}^{\mathrm{old}}$。在 EM 算法的 E 步中，

<!-- pdf-page: 521 -->
<!-- join-previous-paragraph -->
用这些参数值求出（10.156）给出的 $\mathbf{w}$ 的后验分布。在 M 步中，最大化完整数据对数似然的期望：

$$
\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})=\mathbb{E}\left[\ln\{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w})\}\right]
\tag{10.160}
$$

其中，期望是关于使用 $\boldsymbol{\xi}^{\mathrm{old}}$ 计算出的后验分布 $q(\mathbf{w})$ 取的。注意到 $p(\mathbf{w})$ 不依赖于 $\boldsymbol{\xi}$，再代入 $h(\mathbf{w},\boldsymbol{\xi})$，得到

$$
\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})=\sum_{n=1}^{N}\left\{\ln\sigma(\xi_n)-\xi_n/2-\lambda(\xi_n)\left(\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n-\xi_n^2\right)\right\}+\mathrm{const}
\tag{10.161}
$$

其中“const”表示与 $\boldsymbol{\xi}$ 无关的项。现在令关于 $\xi_n$ 的导数等于零。利用 $\sigma(\xi)$ 和 $\lambda(\xi)$ 的定义，经过几步代数运算，得到

$$
0=\lambda'(\xi_n)\left(\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n-\xi_n^2\right).
\tag{10.162}
$$

注意，对于 $\xi\geqslant0$，$\lambda'(\xi)$ 是 $\xi$ 的单调函数；而且由于这个界关于 $\xi=0$ 对称，可以不失一般性地只考虑 $\xi$ 的非负值。因此 $\lambda'(\xi)\neq0$，从而得到如下重估方程（习题 10.33）：

$$
(\xi_n^{\mathrm{new}})^2=\boldsymbol{\phi}_n^{\mathrm T}\mathbb{E}[\mathbf{w}\mathbf{w}^{\mathrm T}]\boldsymbol{\phi}_n=\boldsymbol{\phi}_n^{\mathrm T}\left(\mathbf{S}_N+\mathbf{m}_N\mathbf{m}_N^{\mathrm T}\right)\boldsymbol{\phi}_n
\tag{10.163}
$$

这里使用了（10.156）。

下面归纳求变分后验分布的 EM 算法。首先初始化变分参数 $\boldsymbol{\xi}^{\mathrm{old}}$。在 E 步中，计算（10.156）给出的 $\mathbf{w}$ 的后验分布，其中均值和协方差由（10.157）和（10.158）定义。在 M 步中，利用这个变分后验，通过（10.163）计算新的 $\boldsymbol{\xi}$ 值。反复执行 E 步和 M 步，直到满足合适的收敛判据；在实践中，通常只需少量迭代。

另一种获得 $\boldsymbol{\xi}$ 的重估方程的方法，是注意到下界 $\mathcal{L}(\boldsymbol{\xi})$ 的定义（10.159）中，对 $\mathbf{w}$ 的积分具有类高斯的被积函数，因此可以解析求出该积分。求出积分后，再对 $\xi_n$ 求导。结果表明，这得到的重估方程与 EM 方法的（10.163）完全相同（习题 10.34）。

正如前面已经强调的，在应用变分方法时，能够计算（10.159）给出的下界 $\mathcal{L}(\boldsymbol{\xi})$ 很有用。注意到 $p(\mathbf{w})$ 是高斯分布，而 $h(\mathbf{w},\boldsymbol{\xi})$ 是 $\mathbf{w}$ 的二次函数的指数，就可以对 $\mathbf{w}$ 作解析积分。因此，通过配方并使用高斯分布归一化系数的标准结果，可以得到如下形式的闭式解（习题 10.35）：

<!-- pdf-page: 522 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-13.png" alt="线性可分的两类数据，左图显示变分预测等高线，右图显示后验抽样的五条决策边界"><figcaption>图 10.13：对一个简单的线性可分数据集应用贝叶斯逻辑回归的示例。左图显示用变分推断得到的预测分布。可以看到，决策边界大致位于两簇数据点的中间；预测分布的等高线在远离数据的地方向外展开，反映出这些区域的分类具有更大的不确定性。右图显示从后验分布 $p(\mathbf{w}\mid\boldsymbol{\mathsf{t}})$ 中抽取的五个参数向量 $\mathbf{w}$ 样本所对应的决策边界。</figcaption><p class="figure-translation">左图标出的 $0.01$、$0.25$、$0.75$、$0.99$ 为预测概率等高线的值；红色叉号与圆圈表示两个类别；右图的五条直线对应五次后验抽样。</p></figure>

$$
\begin{aligned}
\mathcal{L}(\boldsymbol{\xi})={}&\frac{1}{2}\ln\frac{|\mathbf{S}_N|}{|\mathbf{S}_0|}-\frac{1}{2}\mathbf{m}_N^{\mathrm T}\mathbf{S}_N^{-1}\mathbf{m}_N+\frac{1}{2}\mathbf{m}_0^{\mathrm T}\mathbf{S}_0^{-1}\mathbf{m}_0\\
&+\sum_{n=1}^{N}\left\{\ln\sigma(\xi_n)-\frac{1}{2}\xi_n-\lambda(\xi_n)\xi_n^2\right\}.
\end{aligned}
\tag{10.164}
$$

这种变分框架也可以应用于数据依次到达的情况（Jaakkola and Jordan，2000）。此时，维护一个关于 $\mathbf{w}$ 的高斯后验分布，并用先验 $p(\mathbf{w})$ 来初始化它。每到达一个数据点，就利用界（10.151）更新后验，然后归一化，得到更新后的后验分布。

预测分布通过对后验分布边缘化得到，其形式与 4.5.2 节讨论的拉普拉斯近似相同。图 10.13 显示了一个合成数据集的变分预测分布。这个例子有助于理解 7.1 节讨论的“大间隔”概念；它的行为与贝叶斯解在定性上相似。

### 10.6.3 超参数推断

到目前为止，我们一直把先验分布中的超参数 $\alpha$ 视为已知常数。现在扩展贝叶斯逻辑回归模型，使这个参数的值可以从数据集中推断出来。将全局和局部变分近似结合在同一个框架中，就能做到这一点，同时在每个阶段都保持边缘似然的下界。Bishop and Svensén（2003）在对层次专家混合模型进行贝叶斯处理时，采用过这种结合的方法。

<!-- pdf-page: 523 -->

具体而言，再次考虑一个简单的各向同性高斯先验分布：

$$
p(\mathbf{w}\mid\alpha)=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I}).
\tag{10.165}
$$

这种分析很容易推广到更一般的高斯先验，例如，希望对参数 $w_j$ 的不同子集关联不同的超参数时。与通常的做法一样，为 $\alpha$ 选择伽马分布形式的共轭超先验：

$$
p(\alpha)=\operatorname{Gam}(\alpha\mid a_0,b_0)
\tag{10.166}
$$

它由常数 $a_0$ 和 $b_0$ 控制。

这个模型的边缘似然现在具有如下形式：

$$
p(\boldsymbol{\mathsf{t}})=\iint p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})\,d\mathbf{w}\,d\alpha
\tag{10.167}
$$

其中联合分布为

$$
p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})=p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})p(\mathbf{w}\mid\alpha)p(\alpha).
\tag{10.168}
$$

现在面对的是一个难以解析求解的、关于 $\mathbf{w}$ 和 $\alpha$ 的积分。我们将在同一个模型中同时使用局部和全局变分方法来处理它。

首先引入变分分布 $q(\mathbf{w},\alpha)$，再应用分解（10.2），在这里它的形式为

$$
\ln p(\boldsymbol{\mathsf{t}})=\mathcal{L}(q)+\operatorname{KL}(q\|p)
\tag{10.169}
$$

其中，下界 $\mathcal{L}(q)$ 和 Kullback–Leibler 散度 $\operatorname{KL}(q\|p)$ 定义为

$$
\mathcal{L}(q)=\iint q(\mathbf{w},\alpha)\ln\left\{\frac{p(\mathbf{w},\alpha,\boldsymbol{\mathsf{t}})}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha
\tag{10.170}
$$

$$
\operatorname{KL}(q\|p)=-\iint q(\mathbf{w},\alpha)\ln\left\{\frac{p(\mathbf{w},\alpha\mid\boldsymbol{\mathsf{t}}))}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha.
\tag{10.171}
$$

此时，由于似然因子 $p(\boldsymbol{\mathsf{t}}\mid\mathbf{w})$ 的形式，下界 $\mathcal{L}(q)$ 仍然难以处理。因此，像前面一样，对每个 logistic sigmoid 因子应用局部变分界。这样就能利用不等式（10.152），为 $\mathcal{L}(q)$ 再给出一个下界，它也因此是对数边缘似然的下界：

$$
\begin{aligned}
\ln p(\boldsymbol{\mathsf{t}})&\geqslant\mathcal{L}(q)\geqslant\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})\\
&=\iint q(\mathbf{w},\alpha)\ln\left\{\frac{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w}\mid\alpha)p(\alpha)}{q(\mathbf{w},\alpha)}\right\}\,d\mathbf{w}\,d\alpha.
\end{aligned}
\tag{10.172}
$$

接着，假设变分分布可以在参数和超参数之间分解，即

$$
q(\mathbf{w},\alpha)=q(\mathbf{w})q(\alpha).
\tag{10.173}
$$

<!-- pdf-page: 524 -->

有了这种因子化，就可以利用一般结果（10.9）求出最优因子的表达式。先考虑分布 $q(\mathbf{w})$。去掉与 $\mathbf{w}$ 无关的项，得到

$$
\begin{aligned}
\ln q(\mathbf{w})&=\mathbb{E}_{\alpha}\left[\ln\{h(\mathbf{w},\boldsymbol{\xi})p(\mathbf{w}\mid\alpha)p(\alpha)\}\right]+\mathrm{const}\\
&=\ln h(\mathbf{w},\boldsymbol{\xi})+\mathbb{E}_{\alpha}[\ln p(\mathbf{w}\mid\alpha)]+\mathrm{const}.
\end{aligned}
$$

现在使用（10.153）代入 $\ln h(\mathbf{w},\boldsymbol{\xi})$，并使用（10.165）代入 $\ln p(\mathbf{w}\mid\alpha)$，得到

$$
\ln q(\mathbf{w})=-\frac{\mathbb{E}[\alpha]}{2}\mathbf{w}^{\mathrm T}\mathbf{w}+\sum_{n=1}^{N}\left\{(t_n-1/2)\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n-\lambda(\xi_n)\mathbf{w}^{\mathrm T}\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}\mathbf{w}\right\}+\mathrm{const}.
$$

可以看到，这是 $\mathbf{w}$ 的二次函数，因此 $q(\mathbf{w})$ 的解将是高斯分布。按通常的方法配方，得到

$$
q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\boldsymbol{\mu}_N,\boldsymbol{\Sigma}_N)
\tag{10.174}
$$

其中定义

$$
\boldsymbol{\Sigma}_N^{-1}\boldsymbol{\mu}_N=\sum_{n=1}^{N}(t_n-1/2)\boldsymbol{\phi}_n
\tag{10.175}
$$

$$
\boldsymbol{\Sigma}_N^{-1}=\mathbb{E}[\alpha]\mathbf{I}+2\sum_{n=1}^{N}\lambda(\xi_n)\boldsymbol{\phi}_n\boldsymbol{\phi}_n^{\mathrm T}.
\tag{10.176}
$$

类似地，因子 $q(\alpha)$ 的最优解由下式得到：

$$
\ln q(\alpha)=\mathbb{E}_{\mathbf{w}}[\ln p(\mathbf{w}\mid\alpha)]+\ln p(\alpha)+\mathrm{const}.
$$

使用（10.165）代入 $\ln p(\mathbf{w}\mid\alpha)$，并使用（10.166）代入 $\ln p(\alpha)$，得到

$$
\ln q(\alpha)=\frac{M}{2}\ln\alpha-\frac{\alpha}{2}\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]+(a_0-1)\ln\alpha-b_0\alpha+\mathrm{const}.
$$

可以看出，这是伽马分布的对数，因此得到

$$
q(\alpha)=\operatorname{Gam}(\alpha\mid a_N,b_N)=\frac{1}{\Gamma(a_0)}a_0^{b_0}\alpha^{a_0-1}e^{-b_0\alpha}
\tag{10.177}
$$

其中

$$
a_N=a_0+\frac{M}{2}
\tag{10.178}
$$

$$
b_N=b_0+\frac{1}{2}\mathbb{E}_{\mathbf{w}}[\mathbf{w}^{\mathrm T}\mathbf{w}].
\tag{10.179}
$$

<!-- pdf-page: 525 -->

还需要优化变分参数 $\xi_n$，这同样通过最大化下界 $\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})$ 来实现。省略与 $\boldsymbol{\xi}$ 无关的项，并对 $\alpha$ 积分，得到

$$
\widetilde{\mathcal{L}}(q,\boldsymbol{\xi})=\int q(\mathbf{w})\ln h(\mathbf{w},\boldsymbol{\xi})\,d\mathbf{w}+\mathrm{const}.
\tag{10.180}
$$

注意，它的形式与（10.159）完全相同，因此可以再次利用之前的结果（10.163）。该结果可以通过直接优化边缘似然函数得到，从而产生如下形式的重估方程：

$$
(\xi_n^{\mathrm{new}})^2=\boldsymbol{\phi}_n^{\mathrm T}\left(\boldsymbol{\Sigma}_N+\boldsymbol{\mu}_N\boldsymbol{\mu}_N^{\mathrm T}\right)\boldsymbol{\phi}_n.
\tag{10.181}
$$

我们已经得到了 $q(\mathbf{w})$、$q(\alpha)$ 和 $\boldsymbol{\xi}$ 这三个量的重估方程，因此，在适当初始化之后，就可以循环地依次更新它们。所需的矩为（附录 B）

$$
\mathbb{E}[\alpha]=\frac{a_N}{b_N}
\tag{10.182}
$$

$$
\mathbb{E}[\mathbf{w}^{\mathrm T}\mathbf{w}]=\boldsymbol{\Sigma}_N+\boldsymbol{\mu}_N^{\mathrm T}\boldsymbol{\mu}_N.
\tag{10.183}
$$

## 10.7 期望传播

本章最后讨论另一种确定性近似推断，称为*期望传播*（expectation propagation，EP）（Minka, 2001a; Minka, 2001b）。与前面讨论的变分贝叶斯方法一样，它也基于最小化 Kullback–Leibler 散度，但使用相反方向的形式，因此得到的近似具有很不相同的性质。

先考虑关于 $q(\mathbf{z})$ 最小化 $\operatorname{KL}(p\|q)$ 的问题，其中 $p(\mathbf{z})$ 是固定分布，而 $q(\mathbf{z})$ 属于指数族，因此由（2.194）可写成

$$
q(\mathbf{z})=h(\mathbf{z})g(\boldsymbol{\eta})\exp\{\boldsymbol{\eta}^{\mathrm T}\mathbf{u}(\mathbf{z})\}.
\tag{10.184}
$$

作为 $\boldsymbol{\eta}$ 的函数，Kullback–Leibler 散度变为

$$
\operatorname{KL}(p\|q)=-\ln g(\boldsymbol{\eta})-\boldsymbol{\eta}^{\mathrm T}\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})]+\mathrm{const}
\tag{10.185}
$$

其中常数项与自然参数 $\boldsymbol{\eta}$ 无关。令关于 $\boldsymbol{\eta}$ 的梯度为零，就能在这族分布中最小化 $\operatorname{KL}(p\|q)$，得到

$$
-\nabla\ln g(\boldsymbol{\eta})=\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})].
\tag{10.186}
$$

不过，由（2.226）已经知道，$\ln g(\boldsymbol{\eta})$ 的负梯度等于 $\mathbf{u}(\mathbf{z})$ 在分布 $q(\mathbf{z})$ 下的期望。令这两个结果相等，得到

$$
\mathbb{E}_{q(\mathbf{z})}[\mathbf{u}(\mathbf{z})]=\mathbb{E}_{p(\mathbf{z})}[\mathbf{u}(\mathbf{z})].
\tag{10.187}
$$

<!-- pdf-page: 526 -->

可以看到，最优解就对应于匹配充分统计量的期望。例如，如果 $q(\mathbf{z})$ 是高斯分布 $\mathcal{N}(\mathbf{z}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，那么令 $q(\mathbf{z})$ 的均值 $\boldsymbol{\mu}$ 等于分布 $p(\mathbf{z})$ 的均值，协方差 $\boldsymbol{\Sigma}$ 等于 $p(\mathbf{z})$ 的协方差，就能最小化 Kullback–Leibler 散度。这有时称为*矩匹配*（moment matching）。图 10.3(a) 已展示过一个例子。

现在利用这个结果，得到一种实用的近似推断算法。对于许多概率模型，数据 $\mathcal{D}$ 和隐藏变量（包括参数）$\boldsymbol{\theta}$ 的联合分布由若干因子的乘积组成，其形式为

$$
p(\mathcal{D},\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta}).
\tag{10.188}
$$

例如，在独立同分布数据的模型中，每个数据点 $\mathbf{x}_n$ 对应一个因子 $f_n(\boldsymbol{\theta})=p(\mathbf{x}_n\mid\boldsymbol{\theta})$，再加上与先验对应的因子 $f_0(\boldsymbol{\theta})=p(\boldsymbol{\theta})$，就会出现这种形式。更一般地，它也适用于任何由有向概率图定义的模型，其中每个因子是对应某个节点的条件分布；或者适用于无向图模型，其中每个因子是一个团势函数。我们希望计算后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$ 来进行预测，同时计算模型证据 $p(\mathcal{D})$ 来比较模型。由（10.188），后验分布为

$$
p(\boldsymbol{\theta}\mid\mathcal{D})=\frac{1}{p(\mathcal{D})}\prod_i f_i(\boldsymbol{\theta})
\tag{10.189}
$$

模型证据为

$$
p(\mathcal{D})=\int\prod_i f_i(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.190}
$$

这里考虑的是连续变量，不过，将积分换成求和后，以下讨论同样适用于离散变量。假设对 $\boldsymbol{\theta}$ 的边缘化，以及为了预测而需要对后验分布进行的边缘化，都难以求解，因此需要某种近似。

期望传播基于一个后验分布的近似，这个近似同样由因子的乘积给出：

$$
q(\boldsymbol{\theta})=\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.191}
$$

其中，近似中的每个因子 $\widetilde{f}_i(\boldsymbol{\theta})$ 都对应于真实后验（10.189）中的一个因子 $f_i(\boldsymbol{\theta})$，而因子 $1/Z$ 是归一化常数，用来保证（10.191）左侧积分为 $1$。为了得到实用的算法，需要以某种方式约束因子 $\widetilde{f}_i(\boldsymbol{\theta})$；具体而言，假设这些因子属于指数族。因此，因子的乘积也属于指数族，从而可以

<!-- pdf-page: 527 -->
<!-- join-previous-paragraph -->
用有限个充分统计量来描述。例如，如果每个 $\widetilde{f}_i(\boldsymbol{\theta})$ 都是高斯函数，那么整体近似 $q(\boldsymbol{\theta})$ 也将是高斯分布。

理想情况下，我们希望通过最小化真实后验与近似之间的 Kullback–Leibler 散度来确定 $\widetilde{f}_i(\boldsymbol{\theta})$，即

$$
\operatorname{KL}(p\|q)=\operatorname{KL}\left(\frac{1}{p(\mathcal{D})}\prod_i f_i(\boldsymbol{\theta})\,\middle\|\,\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta})\right).
\tag{10.192}
$$

注意，与变分推断所使用的 KL 散度相比，这里的方向相反。一般来说，这个最小化问题难以处理，因为 KL 散度涉及关于真实分布求平均。一种粗略近似，是改为最小化各对对应因子 $f_i(\boldsymbol{\theta})$ 和 $\widetilde{f}_i(\boldsymbol{\theta})$ 之间的 KL 散度。这个问题容易求解得多，而且算法不需要迭代。不过，由于每个因子都是单独近似的，因子乘积所得到的近似很可能很差。

期望传播在所有其他因子所给定的环境中，依次优化每个因子，因而得到好得多的近似。它先初始化因子 $\widetilde{f}_i(\boldsymbol{\theta})$，然后循环遍历这些因子，每次改进其中一个。这与前面变分贝叶斯框架中更新因子的思路相近。假设要改进因子 $\widetilde{f}_j(\boldsymbol{\theta})$。首先从乘积中移除这个因子，得到 $\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})$。从概念上说，现在要确定因子 $\widetilde{f}_j(\boldsymbol{\theta})$ 的新形式，使乘积

$$
q^{\mathrm{new}}(\boldsymbol{\theta})\propto\widetilde{f}_j(\boldsymbol{\theta})\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.193}
$$

尽可能接近

$$
f_j(\boldsymbol{\theta})\prod_{i\neq j}\widetilde{f}_i(\boldsymbol{\theta})
\tag{10.194}
$$

同时保持所有 $i\neq j$ 的因子 $\widetilde{f}_i(\boldsymbol{\theta})$ 不变。这样可以保证，在其余因子所确定的后验概率较高的区域中，近似最为精确。把 EP 应用于“杂波问题”时，将看到这一效果的例子（10.7.1 节）。为此，先定义未归一化分布，从当前后验近似中移除因子 $\widetilde{f}_j(\boldsymbol{\theta})$：

$$
q^{\backslash j}(\boldsymbol{\theta})=\frac{q(\boldsymbol{\theta})}{\widetilde{f}_j(\boldsymbol{\theta})}.
\tag{10.195}
$$

注意，也可以通过所有 $i\neq j$ 的因子乘积来求 $q^{\backslash j}(\boldsymbol{\theta})$，不过实践中做除法通常更容易。现在将它与因子 $f_j(\boldsymbol{\theta})$ 结合，得到分布

$$
\frac{1}{Z_j}f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})
\tag{10.196}
$$

<!-- pdf-page: 528 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-14.png" alt="左图比较真实分布及拉普拉斯、全局变分、期望传播的高斯近似，右图比较对应的负对数"><figcaption>图 10.14：对之前图 4.14 和图 10.1 中的例子，使用高斯分布进行期望传播近似。左图显示原分布（黄色）、拉普拉斯近似（红色）、全局变分近似（绿色）和 EP 近似（蓝色），右图显示这些分布相应的负对数。注意，由于 KL 散度形式不同，EP 分布比变分推断得到的分布更宽。</figcaption><p class="figure-translation">黄色：原分布；红色：拉普拉斯近似；绿色：全局变分近似；蓝色：期望传播近似。左图为分布，右图为负对数。</p></figure>

其中 $Z_j$ 是归一化常数，给定为

$$
Z_j=\int f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.197}
$$

现在通过最小化 Kullback–Leibler 散度来确定更新后的因子 $\widetilde{f}_j(\boldsymbol{\theta})$：

$$
\operatorname{KL}\left(\frac{f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})}{Z_j}\,\middle\|\,q^{\mathrm{new}}(\boldsymbol{\theta})\right).
\tag{10.198}
$$

这很容易求解，因为近似分布 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 属于指数族，所以可以利用结果（10.187）：将它的充分统计量的期望与（10.196）的对应矩匹配，就能得到 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的参数。这里假设这项操作是可处理的。例如，如果选择 $q(\boldsymbol{\theta})$ 为高斯分布 $\mathcal{N}(\boldsymbol{\theta}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$，那么将 $\boldsymbol{\mu}$ 设为（未归一化）分布 $f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})$ 的均值，将 $\boldsymbol{\Sigma}$ 设为它的协方差。更一般地，只要能对指数族中的分布归一化，就很容易得到所需的期望，因为充分统计量的期望可以与归一化系数的导数联系起来，如（2.226）所示。图 10.14 展示了 EP 近似。

由（10.193）可以看到，将 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 除以其余因子，就能得到更新后的因子 $\widetilde{f}_j(\boldsymbol{\theta})$，即

$$
\widetilde{f}_j(\boldsymbol{\theta})=K\frac{q^{\mathrm{new}}(\boldsymbol{\theta})}{q^{\backslash j}(\boldsymbol{\theta})}
\tag{10.199}
$$

这里使用了（10.195）。为确定系数 $K$，将等式两边

<!-- pdf-page: 529 -->
<!-- join-previous-paragraph -->
乘以 $q^{\backslash i}(\boldsymbol{\theta})$，再对（10.199）积分，得到

$$
K=\int\widetilde{f}_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}
\tag{10.200}
$$

这里使用了 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 已归一化这一事实。因此，可以通过匹配零阶矩来确定 $K$ 的值：

$$
\int\widetilde{f}_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}=\int f_j(\boldsymbol{\theta})q^{\backslash j}(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.201}
$$

将它与（10.197）结合，可知 $K=Z_j$，因此可以通过计算（10.197）中的积分来求出它。

实践中，会对因子集合遍历多轮，每次依次更新各个因子。随后用（10.191）近似后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$，并在（10.190）中将因子 $f_i(\boldsymbol{\theta})$ 替换为其近似 $\widetilde{f}_i(\boldsymbol{\theta})$，以近似模型证据 $p(\mathcal{D})$。

<aside class="procedure">
<h3>期望传播</h3>
<p>给定观测数据 $\mathcal{D}$ 和随机变量 $\boldsymbol{\theta}$ 的联合分布，它具有因子乘积的形式</p>
<p>$$
p(\mathcal{D},\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta})
\tag{10.202}
$$</p>
<p>我们希望用如下形式的分布近似后验分布 $p(\boldsymbol{\theta}\mid\mathcal{D})$：</p>
<p>$$
q(\boldsymbol{\theta})=\frac{1}{Z}\prod_i\widetilde{f}_i(\boldsymbol{\theta}).
\tag{10.203}
$$</p>
<p>还希望近似模型证据 $p(\mathcal{D})$。</p>
<ol>
<li>初始化所有近似因子 $\widetilde{f}_i(\boldsymbol{\theta})$。</li>
<li>通过如下设置，初始化后验近似：</li>
</ol>
<p>$$
q(\boldsymbol{\theta})\propto\prod_i\widetilde{f}_i(\boldsymbol{\theta}).
\tag{10.204}
$$</p>
<ol start="3">
<li>反复执行以下操作，直到收敛：</li>
</ol>
<p>（a）选择一个因子 $\widetilde{f}_j(\boldsymbol{\theta})$ 进行改进。</p>
<p>（b）通过除法，从后验中移除 $\widetilde{f}_j(\boldsymbol{\theta})$：</p>
<p>$$
q^{\backslash j}(\boldsymbol{\theta})=\frac{q(\boldsymbol{\theta})}{\widetilde{f}_j(\boldsymbol{\theta})}.
\tag{10.205}
$$</p>
</aside>

<!-- pdf-page: 530 -->
<!-- join-previous-procedure -->

<aside class="procedure">
<p>（c）将 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的充分统计量（矩）设为与 $q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta})$ 的相同，从而计算新的后验；这包括计算归一化常数</p>
<p>$$
Z_j=\int q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.206}
$$</p>
<p>（d）计算并存储新的因子</p>
<p>$$
\widetilde{f}_j(\boldsymbol{\theta})=Z_j\frac{q^{\mathrm{new}}(\boldsymbol{\theta})}{q^{\backslash j}(\boldsymbol{\theta})}.
\tag{10.207}
$$</p>
<ol start="4">
<li>计算模型证据的近似：</li>
</ol>
<p>$$
p(\mathcal{D})\simeq\int\prod_i\widetilde{f}_i(\boldsymbol{\theta})\,d\boldsymbol{\theta}.
\tag{10.208}
$$</p>
</aside>

EP 的一个特殊情形称为*假定密度滤波*（assumed density filtering，ADF），也称为*矩匹配*（Maybeck, 1982; Lauritzen, 1992; Boyen and Koller, 1998; Opper and Winther, 1999）。其做法是：除第一个因子外，将所有近似因子都初始化为 $1$，然后只遍历一轮因子，每个因子更新一次。假定密度滤波适用于在线学习：数据点依次到达，需要从每个数据点学习，然后在处理下一个点之前丢弃它。不过，在批量情形中，可以多次使用数据点来提高精度，期望传播正是利用了这一思路。此外，如果将 ADF 应用于批量数据，结果会依赖于处理数据点的（任意）顺序；这种依赖并不理想，而 EP 同样能够克服这一问题。

期望传播的一个缺点是，不能保证迭代收敛。不过，对于指数族中的近似 $q(\boldsymbol{\theta})$，如果迭代确实收敛，所得的解将是某个特定能量函数的驻点（Minka，2001a），尽管每次 EP 迭代不一定降低这个能量函数的值。这与变分贝叶斯不同：后者迭代地最大化对数边缘似然的一个下界，并保证每次迭代都不会减小这个下界。也可以直接优化 EP 的代价函数，这时能够保证收敛，不过所得算法可能较慢，而且实现更复杂。

变分贝叶斯与 EP 的另一个区别，来自这两种算法所最小化的 KL 散度形式：前者最小化 $\operatorname{KL}(q\|p)$，后者最小化 $\operatorname{KL}(p\|q)$。如图 10.3 所示，对于多峰分布 $p(\boldsymbol{\theta})$，最小化 $\operatorname{KL}(p\|q)$ 可能得到较差的近似。特别是，将 EP 应用于混合模型时，结果并不合理，因为近似试图涵盖后验分布的所有峰。相反，在 logistic 类型的模型中，EP 往往优于局部变分方法和拉普拉斯近似（Kuss and Rasmussen，2006）。

<!-- pdf-page: 531 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-15.png" alt="一维杂波问题，绿色目标高斯与红色背景高斯的混合生成由叉号表示的数据点"><figcaption>图 10.15：数据空间维数为 $D=1$ 时的杂波问题示例。叉号表示的训练数据点来自两个高斯分布的混合，两个分量分别用红色和绿色显示。目标是从观测数据推断绿色高斯分布的均值。</figcaption><p class="figure-translation">$x$：观测变量；$\theta$：绿色高斯分布的均值；红色曲线：背景杂波分布；绿色曲线：目标分布；叉号：训练数据点。</p></figure>

### 10.7.1 示例：杂波问题

按照 Minka（2001b），使用一个简单例子说明 EP 算法。给定从变量 $\mathbf{x}$ 的多元高斯分布中抽取的一组观测，目标是推断该分布的均值 $\boldsymbol{\theta}$。为使问题更有趣，观测混杂在背景杂波中，而背景杂波本身也服从高斯分布，如图 10.15 所示。因此，观测值 $\mathbf{x}$ 的分布是高斯混合，采用如下形式：

$$
p(\mathbf{x}\mid\boldsymbol{\theta})=(1-w)\mathcal{N}(\mathbf{x}\mid\boldsymbol{\theta},\mathbf{I})+w\mathcal{N}(\mathbf{x}\mid\mathbf{0},a\mathbf{I})
\tag{10.209}
$$

其中 $w$ 是背景杂波的比例，假设它已知。$\boldsymbol{\theta}$ 的先验取为高斯分布：

$$
p(\boldsymbol{\theta})=\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{0},b\mathbf{I})
\tag{10.210}
$$

Minka（2001a）选择的参数值为 $a=10$、$b=100$ 和 $w=0.5$。$N$ 个观测 $\mathcal{D}=\{\mathbf{x}_1,\ldots,\mathbf{x}_N\}$ 与 $\boldsymbol{\theta}$ 的联合分布为

$$
p(\mathcal{D},\boldsymbol{\theta})=p(\boldsymbol{\theta})\prod_{n=1}^{N}p(\mathbf{x}_n\mid\boldsymbol{\theta})
\tag{10.211}
$$

因此，后验分布由 $2^N$ 个高斯分布的混合组成。精确求解这个问题的计算成本会随数据集大小指数增长，所以当 $N$ 达到中等规模时，精确解就难以求得。

为了将 EP 应用于杂波问题，首先确定因子 $f_0(\boldsymbol{\theta})=p(\boldsymbol{\theta})$ 和 $f_n(\boldsymbol{\theta})=p(\mathbf{x}_n\mid\boldsymbol{\theta})$。接着从指数族中选择一个近似分布；在这个例子中，选用球形高斯分布较为方便：

$$
q(\boldsymbol{\theta})=\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{m},v\mathbf{I}).
\tag{10.212}
$$

<!-- pdf-page: 532 -->

因此，因子的近似将是如下形式的二次指数函数：

$$
\widetilde{f}_n(\boldsymbol{\theta})=s_n\mathcal{N}(\boldsymbol{\theta}\mid\mathbf{m}_n,v_n\mathbf{I})
\tag{10.213}
$$

其中 $n=1,\ldots,N$，并令 $\widetilde{f}_0(\boldsymbol{\theta})$ 等于先验 $p(\boldsymbol{\theta})$。注意，使用 $\mathcal{N}(\boldsymbol{\theta}\mid\cdot,\cdot)$ 并不意味着右侧是一个合法的高斯密度（事实上，稍后会看到，方差参数 $v_n$ 可以为负），它只是一个方便的简写记号。对于 $n=1,\ldots,N$，可以将近似 $\widetilde{f}_n(\boldsymbol{\theta})$ 初始化为 $1$，对应于 $s_n=(2\pi v_n)^{D/2}$、$v_n\to\infty$ 和 $\mathbf{m}_n=\mathbf{0}$，其中 $D$ 是 $\mathbf{x}$ 的维数，也就是 $\boldsymbol{\theta}$ 的维数。因此，由（10.191）定义的初始 $q(\boldsymbol{\theta})$ 等于先验。

然后，每次选取一个因子 $f_n(\boldsymbol{\theta})$，应用（10.205）、（10.206）和（10.207），迭代地改进这些因子。注意，不需要更新项 $f_0(\boldsymbol{\theta})$，因为 EP 更新会使这一项保持不变（习题 10.37）。这里给出结果，具体细节留给读者完成。

首先，利用（10.205），通过除法从 $q(\boldsymbol{\theta})$ 中移除当前估计 $\widetilde{f}_n(\boldsymbol{\theta})$，得到 $q^{\backslash n}(\boldsymbol{\theta})$；其均值和逆方差为（习题 10.38）

$$
\mathbf{m}^{\backslash n}=\mathbf{m}+v^{\backslash n}v_n^{-1}(\mathbf{m}-\mathbf{m}_n)
\tag{10.214}
$$

$$
(v^{\backslash n})^{-1}=v^{-1}-v_n^{-1}.
\tag{10.215}
$$

接着，利用（10.206）计算归一化常数 $Z_n$，得到

$$
Z_n=(1-w)\mathcal{N}(\mathbf{x}_n\mid\mathbf{m}^{\backslash n},(v^{\backslash n}+1)\mathbf{I})+w\mathcal{N}(\mathbf{x}_n\mid\mathbf{0},a\mathbf{I}).
\tag{10.216}
$$

类似地，通过求 $q^{\backslash n}(\boldsymbol{\theta})f_n(\boldsymbol{\theta})$ 的均值和方差，来计算 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 的均值和方差，得到（习题 10.39）

$$
\mathbf{m}=\mathbf{m}^{\backslash n}+\rho_n\frac{v^{\backslash n}}{v^{\backslash n}+1}(\mathbf{x}_n-\mathbf{m}^{\backslash n})
\tag{10.217}
$$

$$
v=v^{\backslash n}-\rho_n\frac{(v^{\backslash n})^2}{v^{\backslash n}+1}+\rho_n(1-\rho_n)\frac{(v^{\backslash n})^2\|\mathbf{x}_n-\mathbf{m}^{\backslash n}\|^2}{D(v^{\backslash n}+1)^2}
\tag{10.218}
$$

其中

$$
\rho_n=1-\frac{w}{Z_n}\mathcal{N}(\mathbf{x}_n\mid\mathbf{0},a\mathbf{I})
\tag{10.219}
$$

具有简单的解释：它是数据点 $\mathbf{x}_n$ 不属于杂波的概率。然后，利用（10.207）计算改进后的因子 $\widetilde{f}_n(\boldsymbol{\theta})$，其参数为

$$
v_n^{-1}=(v^{\mathrm{new}})^{-1}-(v^{\backslash n})^{-1}
\tag{10.220}
$$

$$
\mathbf{m}_n=\mathbf{m}^{\backslash n}+(v_n+v^{\backslash n})(v^{\backslash n})^{-1}(\mathbf{m}^{\mathrm{new}}-\mathbf{m}^{\backslash n})
\tag{10.221}
$$

$$
s_n=\frac{Z_n}{(2\pi v_n)^{D/2}\mathcal{N}(\mathbf{m}_n\mid\mathbf{m}^{\backslash n},(v_n+v^{\backslash n})\mathbf{I})}.
\tag{10.222}
$$

反复执行这个改进过程，直到满足适当的终止条件，例如，完整

<!-- pdf-page: 533 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-16.png" alt="一维杂波模型两个局部因子近似，蓝色为真实因子、红色为近似因子、绿色为移除该因子后的分布"><figcaption>图 10.16：一维杂波问题中特定因子的近似示例，其中 $f_n(\theta)$ 用蓝色显示，$\widetilde{f}_n(\theta)$ 用红色显示，$q^{\backslash n}(\theta)$ 用绿色显示。注意，$q^{\backslash n}(\theta)$ 的当前形式决定了 $\widetilde{f}_n(\theta)$ 能够很好地近似 $f_n(\theta)$ 的 $\theta$ 取值范围。</figcaption><p class="figure-translation">$\theta$：一维参数；蓝色：真实因子 $f_n(\theta)$；红色：近似因子 $\widetilde{f}_n(\theta)$；绿色：移除该近似因子后的 $q^{\backslash n}(\theta)$。</p></figure>

<!-- join-previous-paragraph-across-figures -->
遍历所有因子一轮后，参数值的最大变化小于某个阈值。最后，使用（10.208）计算模型证据的近似，得到

$$
p(\mathcal{D})\simeq(2\pi v^{\mathrm{new}})^{D/2}\exp(B/2)\prod_{n=1}^{N}\left\{s_n(2\pi v_n)^{-D/2}\right\}
\tag{10.223}
$$

其中

$$
B=\frac{(\mathbf{m}^{\mathrm{new}})^{\mathrm T}\mathbf{m}^{\mathrm{new}}}{v}-\sum_{n=1}^{N}\frac{\mathbf{m}_n^{\mathrm T}\mathbf{m}_n}{v_n}.
\tag{10.224}
$$

图 10.16 给出了一维参数空间 $\theta$ 下杂波问题的因子近似示例。注意，近似因子的“方差”参数 $v_n$ 可以取无穷大，甚至取负值。这只意味着近似曲线向上弯而不是向下弯；只要整体近似后验 $q(\boldsymbol{\theta})$ 具有正方差，就不一定有问题。图 10.17 比较了 EP、变分贝叶斯（平均场理论）和拉普拉斯近似在杂波问题上的表现。

### 10.7.2 图上的期望传播

在此前对 EP 的一般讨论中，我们允许分布 $p(\boldsymbol{\theta})$ 中的因子 $f_i(\boldsymbol{\theta})$ 依赖于 $\boldsymbol{\theta}$ 的所有分量，近似分布 $q(\boldsymbol{\theta})$ 中的近似因子 $\widetilde{f}(\boldsymbol{\theta})$ 也一样。现在考虑因子只依赖于变量子集的情况。这种限制可以方便地用第 8 章讨论的概率图模型框架表示。这里使用因子图表示，因为它同时涵盖有向图和无向图。

<!-- pdf-page: 534 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-17.png" alt="杂波问题中三种近似算法的误差与浮点运算次数比较，左图为后验均值，右图为模型证据"><figcaption>图 10.17：期望传播、变分推断和拉普拉斯近似在杂波问题上的比较。左图显示预测后验均值的误差与浮点运算次数的关系，右图显示模型证据的相应结果。</figcaption><p class="figure-translation">Posterior mean → 后验均值；Evidence → 模型证据；Error → 误差；FLOPS → 浮点运算次数；laplace → 拉普拉斯近似（蓝色）；vb → 变分贝叶斯（红色）；ep → 期望传播（绿色）。</p></figure>

我们将着重讨论近似分布完全因子化的情况，并证明，此时期望传播会化为有环信念传播（Minka，2001a）。先通过一个简单例子说明这一点，再研究一般情形。

首先，回顾（10.17）：如果关于因子化分布 $q$ 最小化 Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$，那么每个因子的最优解就是 $p$ 的对应边缘分布。

现在考虑图 10.18 左侧的因子图，它在前面讨论和积算法时已经出现过（8.4.4 节）。联合分布为

$$
p(\mathbf{x})=f_a(x_1,x_2)f_b(x_2,x_3)f_c(x_2,x_4).
\tag{10.225}
$$

我们寻找具有相同因子分解的近似 $q(\mathbf{x})$，即

$$
q(\mathbf{x})\propto\widetilde{f}_a(x_1,x_2)\widetilde{f}_b(x_2,x_3)\widetilde{f}_c(x_2,x_4).
\tag{10.226}
$$

注意，这里省略了归一化常数；可以在最后通过局部归一化重新加入这些常数，这也是信念传播通常的做法。现在进一步限制近似形式，令因子本身也按各个变量分解，使得

$$
q(\mathbf{x})\propto\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)
\tag{10.227}
$$

这对应于图 10.18 右侧的因子图。由于各个因子都已分解，整体分布 $q(\mathbf{x})$ 本身也完全因子化。

现在使用这个完全因子化的近似来应用 EP 算法。假设已经初始化了所有因子，并选择改进因子

<!-- pdf-page: 535 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-10/b-fig-10-18.png" alt="左侧为四变量三因子的原始因子图，右侧为各因子进一步分解后的完全因子化近似"><figcaption>图 10.18：左侧是图 8.51 中的一个简单因子图，为方便起见在此再次给出。右侧是相应的因子化近似。</figcaption><p class="figure-translation">$x_1$、$x_2$、$x_3$、$x_4$：变量节点；$f_a$、$f_b$、$f_c$：原因子；$\widetilde{f}_{a1}$、$\widetilde{f}_{a2}$、$\widetilde{f}_{b2}$、$\widetilde{f}_{b3}$、$\widetilde{f}_{c2}$、$\widetilde{f}_{c4}$：按单个变量分解后的近似因子。圆圈表示变量，方块表示因子。</p></figure>

<!-- join-previous-paragraph-across-figures -->
$\widetilde{f}_b(x_2,x_3)=\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)$。首先从近似分布中移除这个因子，得到

$$
q^{\backslash b}(\mathbf{x})=\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)
\tag{10.228}
$$

然后乘以精确因子 $f_b(x_2,x_3)$，得到

$$
\widehat{p}(\mathbf{x})=q^{\backslash b}(\mathbf{x})f_b(x_2,x_3)=\widetilde{f}_{a1}(x_1)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\widetilde{f}_{c4}(x_4)f_b(x_2,x_3).
\tag{10.229}
$$

现在通过最小化 Kullback–Leibler 散度 $\operatorname{KL}(\widehat{p}\|q^{\mathrm{new}})$ 来求 $q^{\mathrm{new}}(\mathbf{x})$。如前所述，结果是 $q^{\mathrm{new}}(\mathbf{z})$ 由因子的乘积组成，每个变量 $x_i$ 对应一个因子，并且每个因子由 $\widehat{p}(\mathbf{x})$ 的相应边缘分布给出。这四个边缘分布为

$$
\widehat{p}(x_1)\propto\widetilde{f}_{a1}(x_1)
\tag{10.230}
$$

$$
\widehat{p}(x_2)\propto\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\sum_{x_3}f_b(x_2,x_3)
\tag{10.231}
$$

$$
\widehat{p}(x_3)\propto\sum_{x_2}\left\{f_b(x_2,x_3)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\right\}
\tag{10.232}
$$

$$
\widehat{p}(x_4)\propto\widetilde{f}_{c4}(x_4)
\tag{10.233}
$$

将这些边缘分布相乘，就得到 $q^{\mathrm{new}}(\mathbf{x})$。可以看到，当更新 $\widetilde{f}_b(x_2,x_3)$ 时，$q(\mathbf{x})$ 中只有涉及 $f_b$ 中变量的因子会发生变化，也就是涉及 $x_2$ 和 $x_3$ 的因子。要得到改进后的因子 $\widetilde{f}_b(x_2,x_3)=\widetilde{f}_{b2}(x_2)\widetilde{f}_{b3}(x_3)$，只需将 $q^{\mathrm{new}}(\mathbf{x})$ 除以 $q^{\backslash b}(\mathbf{x})$，得到

$$
\widetilde{f}_{b2}(x_2)\propto\sum_{x_3}f_b(x_2,x_3)
\tag{10.234}
$$

$$
\widetilde{f}_{b3}(x_3)\propto\sum_{x_2}\left\{f_b(x_2,x_3)\widetilde{f}_{a2}(x_2)\widetilde{f}_{c2}(x_2)\right\}.
\tag{10.235}
$$

<!-- pdf-page: 536 -->

这些正是信念传播得到的消息，其中从变量节点到因子节点的消息已经并入从因子节点到变量节点的消息（8.4.4 节）。具体来说，$\widetilde{f}_{b2}(x_2)$ 对应于因子节点 $f_b$ 发送给变量节点 $x_2$ 的消息 $\mu_{f_b\to x_2}(x_2)$，由（8.81）给出。类似地，将（8.78）代入（8.79），就得到（10.235）；其中 $\widetilde{f}_{a2}(x_2)$ 对应于 $\mu_{f_a\to x_2}(x_2)$，$\widetilde{f}_{c2}(x_2)$ 对应于 $\mu_{f_c\to x_2}(x_2)$，由此得到的消息 $\widetilde{f}_{b3}(x_3)$ 对应于 $\mu_{f_b\to x_3}(x_3)$。

这个结果与标准信念传播略有不同，因为消息同时沿两个方向传递。只需每次更新一个因子，就能很容易地把 EP 过程改为标准形式的和积算法。例如，如果只改进 $\widetilde{f}_{b3}(x_3)$，那么按定义，$\widetilde{f}_{b2}(x_2)$ 保持不变，而 $\widetilde{f}_{b3}(x_3)$ 的改进形式仍由（10.235）给出。如果每次只改进一项，就可以按需要选择改进顺序。特别是，对于树结构图，可以采用与标准信念传播调度相对应的两轮更新方案，从而对变量边缘和因子边缘进行精确推断。在这种情况下，近似因子的初始化并不重要。

现在考虑与如下分布对应的一般因子图：

$$
p(\boldsymbol{\theta})=\prod_i f_i(\boldsymbol{\theta}_i)
\tag{10.236}
$$

其中 $\boldsymbol{\theta}_i$ 表示与因子 $f_i$ 关联的变量子集。使用如下形式的完全因子化分布来近似它：

$$
q(\boldsymbol{\theta})\propto\prod_i\prod_k\widetilde{f}_{ik}(\theta_k)
\tag{10.237}
$$

其中 $\theta_k$ 对应于单个变量节点。假设希望改进某一项 $\widetilde{f}_{jl}(\theta_l)$，同时保持所有其他项不变。首先从 $q(\boldsymbol{\theta})$ 中移除项 $\widetilde{f}_j(\boldsymbol{\theta}_j)$，得到

$$
q^{\backslash j}(\boldsymbol{\theta})\propto\prod_{i\neq j}\prod_k\widetilde{f}_{ik}(\theta_k)
\tag{10.238}
$$

然后乘以精确因子 $f_j(\boldsymbol{\theta}_j)$。为确定改进后的项 $\widetilde{f}_{jl}(\theta_l)$，只需考虑对 $\theta_l$ 的函数依赖，因此只需找出下式相应的边缘分布：

$$
q^{\backslash j}(\boldsymbol{\theta})f_j(\boldsymbol{\theta}_j).
\tag{10.239}
$$

忽略一个乘法常数，这意味着先将 $f_j(\boldsymbol{\theta}_j)$ 与 $q^{\backslash j}(\boldsymbol{\theta})$ 中所有依赖于 $\boldsymbol{\theta}_j$ 内任意变量的项相乘，再取边缘分布。随后除以 $q^{\backslash j}(\boldsymbol{\theta})$ 时，对应于其他因子 $\widetilde{f}_i(\boldsymbol{\theta}_i)$（$i\neq j$）的项会在分子和分母之间消去。因此得到

$$
\widetilde{f}_{jl}(\theta_l)\propto\sum_{\theta_{m\neq l}\in\boldsymbol{\theta}_j}f_j(\boldsymbol{\theta}_j)\prod_k\prod_{m\neq l}\widetilde{f}_{km}(\theta_m).
\tag{10.240}
$$

<!-- pdf-page: 537 -->

可以看出，这就是消去了变量节点到因子节点消息之后的和积规则，图 8.50 中的例子展示了这种形式。$\widetilde{f}_{jm}(\theta_m)$ 对应于因子节点 $j$ 发送给变量节点 $m$ 的消息 $\mu_{f_j\to\theta_m}(\theta_m)$；（10.240）中关于 $k$ 的乘积，遍历所有依赖于变量 $\theta_m$、且与因子 $f_j(\boldsymbol{\theta}_j)$ 具有共同变量（变量 $\theta_l$ 除外）的因子。换言之，要计算一个因子节点的输出消息，先将来自其他因子节点的全部输入消息相乘，再乘以局部因子，最后进行边缘化。

因此，使用完全因子化的近似分布时，和积算法就是期望传播的一个特殊情形。这表明，可以用对应于部分断开连接图的、更灵活的近似分布来提高精度。另一种推广方式，是将因子 $f_i(\boldsymbol{\theta}_i)$ 分组为若干集合，在每次迭代中同时改进一个集合内的全部因子。这两种方法都可能提高精度（Minka，2001b）。一般而言，如何选择最佳的分组与断开连接组合，仍是一个开放的研究问题。

我们已经看到，变分消息传递和期望传播优化的是两种不同形式的 Kullback–Leibler 散度。Minka（2005）证明，许多消息传递算法都可以从一个共同框架中推导出来，即最小化（10.19）给出的 alpha 散度族中的某个散度。其中包括变分消息传递、有环信念传播和期望传播，也包括这里没有篇幅讨论的其他一系列算法，例如*树重加权消息传递*（tree-reweighted message passing）（Wainwright et al.，2005）、*分数信念传播*（fractional belief propagation）（Wiegerinck and Heskes，2003）和*幂 EP*（power EP）（Minka，2004）。

## 习题

**10.1（⋆）www** 验证：观测数据的对数边缘分布 $\ln p(\mathbf{X})$ 可以分解为（10.2）形式的两项，其中 $\mathcal{L}(q)$ 由（10.3）给出，$\operatorname{KL}(q\|p)$ 由（10.4）给出。

**10.2（⋆）** 利用性质 $\mathbb{E}[z_1]=m_1$ 和 $\mathbb{E}[z_2]=m_2$，求解联立方程（10.13）和（10.15），由此证明：只要原分布 $p(\mathbf{z})$ 非奇异，近似分布中各因子均值的唯一解就是 $\mathbb{E}[z_1]=\mu_1$ 和 $\mathbb{E}[z_2]=\mu_2$。

**10.3（⋆⋆）www** 考虑（10.5）形式的因子化变分分布 $q(\mathbf{Z})$。利用拉格朗日乘子法，验证：保持其他所有因子不变，关于某个因子 $q_i(\mathbf{Z}_i)$ 最小化 Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$，会得到解（10.17）。

**10.4（⋆⋆）** 假设 $p(\mathbf{x})$ 是某个固定分布，希望使用高斯分布 $q(\mathbf{x})=\mathcal{N}(\mathbf{x}\mid\boldsymbol{\mu},\boldsymbol{\Sigma})$ 来近似它。写出 $q(\mathbf{x})$ 为高斯分布时 KL 散度 $\operatorname{KL}(p\|q)$ 的形式，再通过求导，证明

<!-- pdf-page: 538 -->
<!-- join-previous-paragraph -->
关于 $\boldsymbol{\mu}$ 和 $\boldsymbol{\Sigma}$ 最小化 $\operatorname{KL}(p\|q)$，会使 $\boldsymbol{\mu}$ 等于 $\mathbf{x}$ 在 $p(\mathbf{x})$ 下的期望，$\boldsymbol{\Sigma}$ 等于其协方差。

**10.5（⋆⋆）www** 考虑一个模型，其中全部隐藏随机变量的集合统记为 $\mathbf{Z}$，它由一些潜变量 $\mathbf{z}$ 和一些模型参数 $\boldsymbol{\theta}$ 组成。假设使用一个在潜变量与参数之间因子化的变分分布，即 $q(\mathbf{z},\boldsymbol{\theta})=q_{\mathbf{z}}(\mathbf{z})q_{\boldsymbol{\theta}}(\boldsymbol{\theta})$，其中分布 $q_{\boldsymbol{\theta}}(\boldsymbol{\theta})$ 用点估计近似，其形式为 $q_{\boldsymbol{\theta}}(\boldsymbol{\theta})=\delta(\boldsymbol{\theta}-\boldsymbol{\theta}_0)$，$\boldsymbol{\theta}_0$ 是自由参数向量。证明，对这个因子化分布进行变分优化，等价于一个 EM 算法：E 步优化 $q_{\mathbf{z}}(\mathbf{z})$，M 步则关于 $\boldsymbol{\theta}_0$，最大化 $\boldsymbol{\theta}$ 的完整数据对数后验分布的期望。

**10.6（⋆⋆）** alpha 散度族由（10.19）定义。证明，Kullback–Leibler 散度 $\operatorname{KL}(p\|q)$ 对应于 $\alpha\to1$。可以通过写出 $p^{\epsilon}=\exp(\epsilon\ln p)=1+\epsilon\ln p+O(\epsilon^2)$，再取 $\epsilon\to0$ 来完成。类似地，证明 $\operatorname{KL}(q\|p)$ 对应于 $\alpha\to-1$。

**10.7（⋆⋆）** 考虑 10.1.3 节研究的问题：用因子化变分近似推断一元高斯分布的均值和精度。证明，因子 $q_{\mu}(\mu)$ 是 $\mathcal{N}(\mu\mid\mu_N,\lambda_N^{-1})$ 形式的高斯分布，其均值和精度分别由（10.26）和（10.27）给出。类似地，证明因子 $q_{\tau}(\tau)$ 是 $\operatorname{Gam}(\tau\mid a_N,b_N)$ 形式的伽马分布，其参数由（10.29）和（10.30）给出。

**10.8（⋆）** 考虑一元高斯分布精度的变分后验分布，其参数由（10.29）和（10.30）给出。利用（B.27）和（B.28）给出的伽马分布均值与方差的标准结果，证明：当 $N\to\infty$ 时，这个变分后验分布的均值等于数据方差的最大似然估计量的倒数，而其方差趋于零。

**10.9（⋆⋆）** 利用伽马分布均值的标准结果 $\mathbb{E}[\tau]=a_N/b_N$，结合（10.26）、（10.27）、（10.29）和（10.30），推导一元高斯分布的因子化变分处理中精度期望值的倒数结果（10.33）。

**10.10（⋆）www** 推导（10.34）给出的分解，它用于通过变分推断求模型的近似后验分布。

**10.11（⋆⋆）www** 使用拉格朗日乘子对分布 $q(m)$ 施加归一化约束，证明下界（10.35）的最大值由（10.36）给出。

**10.12（⋆⋆）** 从联合分布（10.41）出发，应用一般结果（10.9），验证正文中的各个步骤，证明贝叶斯高斯混合模型中潜变量的最优变分分布 $q^{\star}(\mathbf{Z})$ 由（10.48）给出。

<!-- pdf-page: 539 -->

**10.13（⋆⋆）www** 从（10.54）出发，推导贝叶斯高斯混合模型中 $\boldsymbol{\mu}_k$ 和 $\boldsymbol{\Lambda}_k$ 的最优变分后验分布结果（10.59），由此验证（10.60）—（10.63）给出的这个分布的参数表达式。

**10.14（⋆⋆）** 使用分布（10.59），验证结果（10.64）。

**10.15（⋆）** 使用结果（B.17），证明变分高斯混合模型中混合系数的期望值由（10.69）给出。

**10.16（⋆⋆）www** 对于（10.70）给出的变分高斯混合模型下界，验证其前两项的结果（10.71）和（10.72）。

**10.17（⋆⋆⋆）** 对于（10.70）给出的变分高斯混合模型下界，验证其余各项的结果（10.73）—（10.77）。

**10.18（⋆⋆⋆）** 本题通过直接对下界求导，推导高斯混合模型的变分重估方程。为此，假设变分分布具有（10.42）和（10.55）定义的因子分解，其中各因子由（10.48）、（10.57）和（10.59）给出。将它们代入（10.70），得到下界作为变分分布参数的函数。然后，关于这些参数最大化下界，推导变分分布各因子的重估方程，并证明它们与 10.2.1 节得到的方程相同。

**10.19（⋆⋆）** 推导贝叶斯高斯混合模型的变分处理中预测分布的结果（10.81）。

**10.20（⋆⋆）www** 本题研究数据集大小 $N$ 很大时高斯混合模型的变分贝叶斯解，并证明它会化为第 9 章基于 EM 推导的最大似然解，这与我们的预期一致。注意，可以借助附录 B 的结果来解答本题。首先证明，精度的后验分布 $q^{\star}(\boldsymbol{\Lambda}_k)$ 会在最大似然解附近形成尖锐的峰。对均值的后验分布 $q^{\star}(\boldsymbol{\mu}_k\mid\boldsymbol{\Lambda}_k)$ 证明同样的结论。接着考虑混合系数的后验分布 $q^{\star}(\boldsymbol{\pi})$，证明它也会在最大似然解附近形成尖锐的峰。类似地，利用 digamma 函数在 $x$ 很大时的如下渐近结果，证明当 $N$ 很大时，责任度等于相应的最大似然值：

$$
\psi(x)=\ln x+O(1/x).
\tag{10.241}
$$

最后，利用（10.80），证明当 $N$ 很大时，预测分布变为高斯混合。

**10.21（⋆）** 证明：具有 $K$ 个分量的混合模型中，由交换对称性产生的等价参数配置共有 $K!$ 种。

<!-- pdf-page: 540 -->

**10.22（⋆⋆）** 我们已经看到，高斯混合模型后验分布的每一个峰，都属于由 $K!$ 个等价峰构成的一族。假设运行变分推断算法得到的近似后验分布 $q$ 集中在其中一个峰的邻域。于是，可以用 $K!$ 个这样的 $q$ 分布的混合来近似完整后验分布，每个峰上各放一个，并取相等的混合系数。证明：若假设这个 $q$ 混合的各分量之间的重叠可忽略不计，那么所得下界与单个分量 $q$ 分布对应的下界相比，多出一项 $\ln K!$。

**10.23（⋆⋆）www** 考虑一个变分高斯混合模型，其中没有为混合系数 $\{\pi_k\}$ 设置先验分布，而是将混合系数视为参数，通过最大化对数边缘似然的变分下界来确定其值。证明：关于混合系数最大化这个下界，并使用拉格朗日乘子施加混合系数之和为 $1$ 的约束，会得到重估结果（10.83）。注意，不必考虑下界的所有项，只需考虑下界对 $\{\pi_k\}$ 的依赖。

**10.24（⋆⋆）www** 在 10.2 节中已经看到，对高斯混合模型进行最大似然处理时出现的奇异性，在贝叶斯处理中不会出现。讨论：如果使用最大后验（MAP）估计来求解贝叶斯模型，是否还会出现这种奇异性？

**10.25（⋆⋆）** 10.2 节讨论的贝叶斯高斯混合模型的变分处理，对后验分布采用了因子化近似（10.5）。如图 10.2 所示，因子化假设会导致参数空间中某些方向上的后验分布方差被低估。定性讨论这对模型证据的变分近似有什么影响，以及这种影响如何随混合分量数变化。由此说明，变分高斯混合模型倾向于低估还是高估最优分量数。

**10.26（⋆⋆⋆）** 扩展贝叶斯线性回归的变分处理，为 $\beta$ 加入伽马超先验 $\operatorname{Gam}(\beta\mid c_0,d_0)$，并假设变分分布具有 $q(\mathbf{w})q(\alpha)q(\beta)$ 的因子化形式，以变分方法求解。推导变分分布中三个因子的变分更新方程，并求出下界和预测分布的表达式。

**10.27（⋆⋆）** 利用附录 B 给出的公式，证明：（10.107）定义的线性基函数回归模型的变分下界可以写成（10.107）的形式，其中各项由（10.108）—（10.112）定义。

**10.28（⋆⋆⋆）** 将 10.2 节介绍的贝叶斯高斯混合模型，改写成 10.4 节讨论的指数族共轭模型。然后利用一般结果（10.115）和（10.119），推导具体结果（10.48）、（10.57）和（10.59）。

<!-- pdf-page: 541 -->

**10.29（⋆）www** 通过计算二阶导数，证明函数 $f(x)=\ln(x)$ 在 $0<x<\infty$ 上是凹函数。确定（10.133）定义的对偶函数 $g(\lambda)$ 的形式，并验证：根据（10.132），关于 $\lambda$ 最小化 $\lambda x-g(\lambda)$，确实能恢复函数 $\ln(x)$。

**10.30（⋆）** 通过求二阶导数，证明对数 logistic 函数 $f(x)=-\ln(1+e^{-x})$ 是凹函数。对这个对数 logistic 函数在点 $x=\xi$ 附近作二阶泰勒展开，直接推导变分上界（10.137）。

**10.31（⋆⋆）** 通过求关于 $x$ 的二阶导数，证明函数 $f(x)=-\ln(e^{x/2}+e^{-x/2})$ 是 $x$ 的凹函数。再考虑关于变量 $x^2$ 的二阶导数，由此证明它是 $x^2$ 的凸函数。分别画出 $f(x)$ 关于 $x$ 和关于 $x^2$ 的图像。把 $f(x)$ 视为变量 $x^2$ 的函数，在 $\xi^2$ 处作一阶泰勒级数展开，直接推导 logistic sigmoid 函数的下界（10.144）。

**10.32（⋆⋆）www** 考虑序贯学习中的逻辑回归变分处理：数据点逐个到达，每个数据点都必须在下一个数据点到达之前处理完毕并丢弃。证明，利用下界（10.151），可以维护一个后验分布的高斯近似；该分布用先验初始化，每吸收一个数据点，就优化其对应的变分参数 $\xi_n$。

**10.33（⋆）** 对（10.161）定义的量 $\mathcal{Q}(\boldsymbol{\xi},\boldsymbol{\xi}^{\mathrm{old}})$ 关于变分参数 $\xi_n$ 求导，证明贝叶斯逻辑回归模型中 $\xi_n$ 的更新方程由（10.163）给出。

**10.34（⋆⋆）** 本题通过直接最大化（10.164）给出的下界，推导 4.5 节贝叶斯逻辑回归模型中变分参数 $\boldsymbol{\xi}$ 的重估方程。为此，令 $\mathcal{L}(\boldsymbol{\xi})$ 关于 $\xi_n$ 的导数等于零，并利用行列式对数求导的结果（3.117），以及定义变分后验分布 $q(\mathbf{w})$ 的均值和协方差的表达式（10.157）和（10.158）。

**10.35（⋆⋆）** 推导变分逻辑回归模型中下界 $\mathcal{L}(\boldsymbol{\xi})$ 的结果（10.164）。最简单的做法，是把高斯先验 $q(\mathbf{w})=\mathcal{N}(\mathbf{w}\mid\mathbf{m}_0,\mathbf{S}_0)$ 的表达式，以及似然函数的下界 $h(\mathbf{w},\boldsymbol{\xi})$，代入定义 $\mathcal{L}(\boldsymbol{\xi})$ 的积分（10.159）。然后，将指数中依赖于 $\mathbf{w}$ 的项归并并配方，得到高斯积分，再利用多元高斯分布归一化系数的标准结果来计算它。最后取对数，得到（10.164）。

**10.36（⋆⋆）** 考虑 10.7 节讨论的 ADF 近似方案，证明加入因子 $f_j(\boldsymbol{\theta})$ 后，模型证据会按如下形式更新：

$$
p_j(\mathcal{D})\simeq p_{j-1}(\mathcal{D})Z_j
\tag{10.242}
$$

<!-- pdf-page: 542 -->

其中 $Z_j$ 是（10.197）定义的归一化常数。递归应用这个结果，并以 $p_0(\mathcal{D})=1$ 初始化，推导

$$
p(\mathcal{D})\simeq\prod_j Z_j.
\tag{10.243}
$$

**10.37（⋆）www** 考虑 10.7 节的期望传播算法，假设定义（10.188）中的一个因子 $f_0(\boldsymbol{\theta})$，与近似分布 $q(\boldsymbol{\theta})$ 具有相同的指数族函数形式。证明：若将因子 $\widetilde{f}_0(\boldsymbol{\theta})$ 初始化为 $f_0(\boldsymbol{\theta})$，那么用于改进 $\widetilde{f}_0(\boldsymbol{\theta})$ 的 EP 更新会使 $\widetilde{f}_0(\boldsymbol{\theta})$ 保持不变。这通常出现在某个因子为先验 $p(\boldsymbol{\theta})$ 的情况下，因此可知，先验因子可以一次性精确地并入，无需再改进。

**10.38（⋆⋆⋆）** 本题和下一题将验证期望传播算法应用于杂波问题时的结果（10.214）—（10.224）。先使用除法公式（10.205），在指数中配方以识别均值和方差，从而推导表达式（10.214）和（10.215）。另外，证明（10.206）定义的归一化常数 $Z_n$ 在杂波问题中由（10.216）给出。可以利用一般结果（2.115）完成证明。

**10.39（⋆⋆⋆）** 证明：EP 应用于杂波问题时，$q^{\mathrm{new}}(\boldsymbol{\theta})$ 的均值和方差由（10.217）和（10.218）给出。为此，先证明 $\boldsymbol{\theta}$ 和 $\boldsymbol{\theta}\boldsymbol{\theta}^{\mathrm T}$ 在 $q^{\mathrm{new}}(\boldsymbol{\theta})$ 下的期望满足如下结果：

$$
\mathbb{E}[\boldsymbol{\theta}]=\mathbf{m}^{\backslash n}+v^{\backslash n}\nabla_{\mathbf{m}^{\backslash n}}\ln Z_n
\tag{10.244}
$$

$$
\mathbb{E}[\boldsymbol{\theta}^{\mathrm T}\boldsymbol{\theta}]=2(v^{\backslash n})^2\nabla_{v^{\backslash n}}\ln Z_n+2\mathbb{E}[\boldsymbol{\theta}]^{\mathrm T}\mathbf{m}^{\backslash n}-\|\mathbf{m}^{\backslash n}\|^2
\tag{10.245}
$$

然后利用 $Z_n$ 的结果（10.216）。接着，使用（10.207）并在指数中配方，证明结果（10.220）—（10.222）。最后，使用（10.208）推导结果（10.223）。
