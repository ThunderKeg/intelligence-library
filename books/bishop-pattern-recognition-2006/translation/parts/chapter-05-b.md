<!-- pdf-page: 277 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-9.png" alt="分别含一个、三个和十个隐藏单元的两层网络对正弦数据的拟合"><figcaption>图 5.9：用从正弦数据集中抽取的 10 个数据点训练两层网络的例子。三张图分别给出具有 $M=1$、3 和 10 个隐藏单元的网络的拟合结果，训练使用缩放共轭梯度算法来最小化平方和误差函数。</figcaption><p class="figure-translation">$M$：隐藏单元数目。</p></figure>

<!-- join-previous-paragraph-across-figures -->
函数具有如下形式：

$$
\widetilde{E}(\mathbf{w})=E(\mathbf{w})+\frac{\lambda}{2}\mathbf{w}^{\mathrm T}\mathbf{w}.
\tag{5.112}
$$

这个正则化项也称为*权重衰减*（weight decay），第 3 章已作过详细讨论。此时，模型的有效复杂度由正则化系数 $\lambda$ 的选择决定。正如前面所见，这个正则化项可以解释为权重向量 $\mathbf{w}$ 上零均值高斯先验分布的负对数。

### 5.5.1 一致的高斯先验

形式为（5.112）的简单权重衰减有一个局限：它与网络映射的某些缩放性质不一致。为说明这一点，考虑一个具有两层权重、输出单元为线性单元的多层感知机网络，它将一组输入变量 $\{x_i\}$ 映射到一组输出变量 $\{y_k\}$。第一隐藏层中隐藏单元的激活值

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-10.png" alt="不同隐藏单元数与三十次随机初始化下的测试集平方和误差"><figcaption>图 5.10：多项式数据集上的测试集平方和误差随网络隐藏单元数目的变化。每种网络大小均使用 30 个随机初始点，展示了局部极小值的影响。每次重新开始时，权重向量都通过从均值为零、方差为 10 的各向同性高斯分布中采样来初始化。</figcaption></figure>

<!-- pdf-page: 278 -->
<!-- join-previous-paragraph-across-figures -->
具有如下形式：

$$
z_j=h\left(\sum_i w_{ji}x_i+w_{j0}\right)
\tag{5.113}
$$

输出单元的激活值则为

$$
y_k=\sum_j w_{kj}z_j+w_{k0}.
\tag{5.114}
$$

假设对输入数据进行如下形式的线性变换：

$$
x_i\to\widetilde{x}_i=ax_i+b.
\tag{5.115}
$$

那么，通过对从输入到隐藏层单元的权重与偏置作相应的线性变换，就可以使网络实现的映射保持不变。这些变换为（习题 5.24）

$$
w_{ji}\to\widetilde{w}_{ji}=\frac{1}{a}w_{ji}
\tag{5.116}
$$

$$
w_{j0}\to\widetilde{w}_{j0}=w_{j0}-\frac{b}{a}\sum_i w_{ji}.
\tag{5.117}
$$

同样，网络输出变量的线性变换

$$
y_k\to\widetilde{y}_k=cy_k+d
\tag{5.118}
$$

可以通过对第二层权重与偏置作如下变换来实现：

$$
w_{kj}\to\widetilde{w}_{kj}=cw_{kj}
\tag{5.119}
$$

$$
w_{k0}\to\widetilde{w}_{k0}=cw_{k0}+d.
\tag{5.120}
$$

如果用原始数据训练一个网络，再用经过上述某个线性变换处理输入和／或目标变量的数据训练另一个网络，那么一致性就要求得到的两个网络彼此等价，只在权重上存在上述线性变换的差别。任何正则化项都应与这一性质一致，否则它就会任意偏好某个解，而不偏好与它等价的另一个解。显然，简单权重衰减（5.112）对所有权重和偏置一视同仁，不满足这一性质。

因此，我们要寻找一个在线性变换（5.116）、（5.117）、（5.119）和（5.120）下保持不变的正则化项。这要求正则化项在权重重新缩放和偏置平移下保持不变。这样的正则化项为

$$
\frac{\lambda_1}{2}\sum_{w\in\mathcal{W}_1}w^2+\frac{\lambda_2}{2}\sum_{w\in\mathcal{W}_2}w^2
\tag{5.121}
$$

其中 $\mathcal{W}_1$ 表示第一层的权重集合，$\mathcal{W}_2$ 表示第二层的权重集合，求和中不包含偏置。这个正则化项

<!-- pdf-page: 279 -->
<!-- join-previous-paragraph -->
在权重变换下会保持不变，只要将正则化参数按照 $\lambda_1\to a^{1/2}\lambda_1$ 和 $\lambda_2\to c^{-1/2}\lambda_2$ 重新缩放。

正则化项（5.121）对应于如下形式的先验：

$$
p(\mathbf{w}\mid\alpha_1,\alpha_2)\propto\exp\left(-\frac{\alpha_1}{2}\sum_{w\in\mathcal{W}_1}w^2-\frac{\alpha_2}{2}\sum_{w\in\mathcal{W}_2}w^2\right).
\tag{5.122}
$$

注意，这种形式的先验是非正常先验（无法归一化），因为偏置参数不受约束。使用非正常先验，可能使贝叶斯框架下的正则化系数选择和模型比较遇到困难，因为相应的证据为零。因此，通常会为偏置另外设置先验，使其具有各自的超参数（这样会破坏平移不变性）。从先验中抽取样本，并绘制相应的网络函数，就可以展示由此得到的四个超参数的作用，如图 5.11 所示。

更一般地，可以将权重划分为任意多个组 $\mathcal{W}_k$，并考虑如下先验：

$$
p(\mathbf{w})\propto\exp\left(-\frac{1}{2}\sum_k\alpha_k\|\mathbf{w}\|_k^2\right)
\tag{5.123}
$$

其中

$$
\|\mathbf{w}\|_k^2=\sum_{j\in\mathcal{W}_k}w_j^2.
\tag{5.124}
$$

作为这种先验的一种特殊情况，如果将每组选择为与一个输入单元相连的权重集合，并对相应的参数 $\alpha_k$ 优化边缘似然，就得到 7.2.2 节讨论的*自动相关性确定*（automatic relevance determination）。

### 5.5.2 提前停止

除了正则化，还可以采用*提前停止*（early stopping）来控制网络的有效复杂度。训练非线性网络模型，就是迭代地减小根据一组训练数据定义的误差函数。对于共轭梯度等许多用于网络训练的优化算法，误差都是迭代次数的非增函数。不过，在独立数据（通常称为验证集）上测得的误差，往往先减小，随后在网络开始过拟合时增大。因此，可以在验证集误差最小的位置停止训练，如图 5.12 所示，从而得到泛化性能良好的网络。

有时可以用网络的有效自由度数目来定性解释这种行为：该数目开始时较小，在训练过程中逐渐增加，对应于模型有效复杂度的稳步增加。在

<!-- pdf-page: 280 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-11.png" alt="四组先验超参数下，从两层网络先验中采样所得的函数"><figcaption>图 5.11：两层网络中控制权重与偏置先验分布的超参数的作用。网络具有一个输入、一个线性输出，以及 12 个使用 $\tanh$ 激活函数的隐藏单元。先验由四个超参数 $\alpha_1^b$、$\alpha_1^w$、$\alpha_2^b$ 和 $\alpha_2^w$ 控制，它们分别表示第一层偏置、第一层权重、第二层偏置和第二层权重的高斯分布精度。可见，参数 $\alpha_2^w$ 控制函数的竖直尺度（注意上面两幅图的纵轴范围不同），$\alpha_1^w$ 控制函数值变化的水平尺度，而 $\alpha_1^b$ 控制发生变化的水平范围。参数 $\alpha_2^b$ 的作用未在图中展示，它控制函数竖直偏移的范围。</figcaption><p class="figure-translation">上标 $w$：权重；上标 $b$：偏置；下标 1、2：第一层、第二层。左上：$\alpha_1^w=1,\alpha_1^b=1,\alpha_2^w=1,\alpha_2^b=1$；右上：$\alpha_1^w=1,\alpha_1^b=1,\alpha_2^w=10,\alpha_2^b=1$；左下：$\alpha_1^w=1000,\alpha_1^b=100,\alpha_2^w=1,\alpha_2^b=1$；右下：$\alpha_1^w=1000,\alpha_1^b=1000,\alpha_2^w=1,\alpha_2^b=1$。</p></figure>

<!-- join-previous-paragraph-across-figures -->
训练误差达到极小值之前停止训练，就成为限制网络有效复杂度的一种方式。

对于二次误差函数，可以验证这一解释，并证明提前停止应当表现出与使用简单权重衰减项进行正则化相似的行为。图 5.13 有助于理解这一点，其中权重空间中的坐标轴经过旋转，与 Hessian 矩阵的特征向量平行。如果在不使用权重衰减的情况下，权重向量从原点出发，沿着局部负梯度方向前进，那么它一开始会沿平行于 $w_2$ 轴的方向移动，经过大致对应于 $\widetilde{\mathbf{w}}$ 的位置，再移向误差函数的极小值点 $\mathbf{w}_{\mathrm{ML}}$。这是由误差曲面的形状以及 Hessian 矩阵差别很大的特征值决定的。因此，在 $\widetilde{\mathbf{w}}$ 附近停止，与权重衰减有相似效果。提前停止与权重衰减之间的关系还可以定量化，由此可证明（习题 5.25），$\tau\eta$（其中 $\tau$ 是迭代次数，$\eta$ 是学习率参数）起到正则化

<!-- pdf-page: 281 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-12.png" alt="训练集误差持续下降，验证集误差先降后升，并以虚线标出提前停止位置"><figcaption>图 5.12：对于正弦数据集，一次典型训练过程中训练集误差（左）与验证集误差（右）随迭代步数变化的示意图。为了得到最佳泛化性能，应在竖直虚线所示位置停止训练，该位置对应于验证集误差的最小值。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
参数 $\lambda$ 的倒数的作用。因此，网络的有效参数数目会在训练过程中增加。

### 5.5.3 不变性

在模式识别的许多应用中，我们知道，输入变量经过一种或多种变换后，预测结果应保持不变，即具有*不变性*。例如，对二维图像中的对象（如手写数字）进行分类时，无论某个对象在图像中的位置如何（平移不变性）、大小如何（尺度不变性），都应被分到同一个类别。这些变换会显著改变由图像各像素强度表示的原始数据，却应使分类系统给出相同的输出。类似地，在语音识别中，沿时间轴作小幅度非线性扭曲，只要保持时间先后顺序，就不应改变对信号的解释。

如果有足够多的训练模式，神经网络这样的自适应模型就可以学到这种不变性，至少可以近似学到。这需要训练集中包含足够多的例子，体现各种变换的影响。因此，要学习图像的平移不变性，训练集就应包含对象位于许多不同位置的例子。然而，当训练样本有限，或者需要满足多种不变性时，这种方法可能不切实际，因为变换组合的数目会随变换种类的增加而呈指数增长。因此，需要寻找其他方法，促使自适应模型具备所要求的不变性。这些方法大致可分为四类：

1. 按照所需的不变性对训练模式的副本作变换，再用这些副本扩充训练集。例如，在数字识别的例子中，可以为每个样本生成多个副本，使

<!-- pdf-page: 282 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-13.png" alt="二次误差下，提前停止的梯度路径和权重衰减解的关系"><figcaption>图 5.13：说明在二次误差函数下，提前停止为什么会产生与权重衰减相似结果的示意图。椭圆表示一条等误差线，$\mathbf{w}_{\mathrm{ML}}$ 表示误差函数的极小值点。如果权重向量从原点开始，沿局部负梯度方向移动，就会沿图中曲线所示的路径前进。提前停止训练，得到的权重向量 $\widetilde{\mathbf{w}}$，在定性上与采用简单权重衰减正则化项、一直训练到正则化误差最小值所得到的结果相似；与图 3.15 比较即可看出这一点。</figcaption><p class="figure-translation">$w_1$、$w_2$：权重坐标；$\widetilde{\mathbf{w}}$：提前停止时的权重向量；$\mathbf{w}_{\mathrm{ML}}$：最大似然权重向量。</p></figure>

<!-- join-previous-list-item-across-figures -->
数字在每张图像中平移到不同的位置。

<ol start="2">
<li>在误差函数中加入正则化项，惩罚输入经过变换时模型输出发生的变化。这就引出了 5.5.4 节讨论的切向传播方法。</li>
<li>在预处理中提取对所需变换具有不变性的特征，从而将不变性引入预处理。此后，任何将这些特征作为输入的回归或分类系统，也必然满足相同的不变性。</li>
<li>最后一种选择是将不变性纳入神经网络的结构，或者对于相关向量机等方法，将其纳入核函数的定义。一种实现方式是使用局部感受野和共享权重，我们将在 5.5.6 节讨论卷积神经网络时介绍。</li>
</ol>

方法 1 往往比较容易实现，而且可以用来促使模型具备图 5.14 所示的复杂不变性。对于序贯训练算法，可以在每个输入模式送入模型之前对其作变换：如果反复使用这些模式，每次就加入一个从适当分布中抽取的不同变换。对于批量方法，可以将每个数据点复制若干份，并独立地变换各个副本，达到类似效果。使用这类扩充数据可以显著改善泛化性能（Simard et al., 2003），但计算代价也可能很高。

方法 2 保持数据集不变，通过添加正则化项来修改误差函数。在 5.5.5 节中，我们将证明，这种方法与方法 2 密切相关。

<!-- pdf-page: 283 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-14.png" alt="手写数字六的原图、三种人工扭曲结果及对应的位移场"><figcaption>图 5.14：对手写数字作人工扭曲的示意图。左侧是原图。右侧上排给出三个扭曲后的数字例子，下排给出相应的位移场。这些位移场通过在每个像素处采样随机位移 $\Delta x,\Delta y\in(0,1)$，再分别与宽度为 0.01、30 和 60 的高斯函数卷积平滑得到。</figcaption></figure>

方法 3 的一个优点是，即使变换幅度远远超出训练集所包含的范围，也能正确外推。不过，要手工设计既具有所需不变性、又不丢弃有助于判别的信息的特征，可能很困难。

### 5.5.4 切向传播

利用*切向传播*（tangent propagation）方法，可以通过正则化促使模型对输入变换保持不变（Simard et al., 1992）。考虑变换对某个特定输入向量 $\mathbf{x}_n$ 的作用。只要变换是连续的，例如平移或旋转，而不是镜像反射，变换后的模式就会在 $D$ 维输入空间中扫出一个流形 $\mathcal{M}$。图 5.15 展示了这一点，为了简单起见，图中采用 $D=2$ 的情况。假设变换由单个参数 $\xi$ 控制，例如旋转角度，那么 $\mathbf{x}_n$ 扫出的子空间 $\mathcal{M}$

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-15.png" alt="输入空间中的连续变换流形、变换参数与数据点处的切向量"><figcaption>图 5.15：二维输入空间示意图，展示连续变换对某个输入向量 $\mathbf{x}_n$ 的作用。由连续变量 $\xi$ 参数化的一维变换作用于 $\mathbf{x}_n$ 时，会扫出一维流形 $\mathcal{M}$。在局部，变换的影响可以用切向量 $\boldsymbol{\tau}_n$ 近似。</figcaption><p class="figure-translation">$x_1$、$x_2$：输入坐标；$\mathbf{x}_n$：输入向量；$\boldsymbol{\tau}_n$：切向量；$\xi$：连续变换参数；$\mathcal{M}$：变换扫出的流形。</p></figure>

<!-- pdf-page: 284 -->
<!-- join-previous-paragraph-across-figures -->
就是一维的，并由 $\xi$ 参数化。将这个变换作用于 $\mathbf{x}_n$ 后得到的向量记为 $\mathbf{s}(\mathbf{x}_n,\xi)$，并定义 $\mathbf{s}(\mathbf{x},0)=\mathbf{x}$。于是，曲线 $\mathcal{M}$ 的切向量由方向导数 $\boldsymbol{\tau}=\partial\mathbf{s}/\partial\xi$ 给出，点 $\mathbf{x}_n$ 处的切向量为

$$
\boldsymbol{\tau}_n=\left.\frac{\partial\mathbf{s}(\mathbf{x}_n,\xi)}{\partial\xi}\right|_{\xi=0}.
\tag{5.125}
$$

输入向量发生变换时，网络输出向量通常也会变化。第 $k$ 个输出对 $\xi$ 的导数为

$$
\left.\frac{\partial y_k}{\partial\xi}\right|_{\xi=0}=\left.\sum_{i=1}^{D}\frac{\partial y_k}{\partial x_i}\frac{\partial x_i}{\partial\xi}\right|_{\xi=0}=\sum_{i=1}^{D}J_{ki}\tau_i
\tag{5.126}
$$

其中 $J_{ki}$ 是雅可比矩阵 $\mathbf{J}$ 的第 $(k,i)$ 个元素，见 5.3.4 节。利用结果（5.126），可以修改标准误差函数，促使模型在数据点附近具有局部不变性：在原误差函数 $E$ 中加入正则化函数 $\Omega$，得到如下形式的总误差函数：

$$
\widetilde{E}=E+\lambda\Omega
\tag{5.127}
$$

其中 $\lambda$ 为正则化系数，并且

$$
\Omega=\frac{1}{2}\sum_n\sum_k\left(\left.\frac{\partial y_{nk}}{\partial\xi}\right|_{\xi=0}\right)^2=\frac{1}{2}\sum_n\sum_k\left(\sum_{i=1}^{D}J_{nki}\tau_{ni}\right)^2.
\tag{5.128}
$$

当网络映射函数在每个模式向量附近对该变换保持不变时，正则化函数为零。参数 $\lambda$ 的值决定了拟合训练数据与学习不变性之间的平衡。

实际实现中，可以用有限差分来近似切向量 $\boldsymbol{\tau}_n$：取一个较小的 $\xi$ 值，用变换后的对应向量减去原向量 $\mathbf{x}_n$，再除以 $\xi$。图 5.16 展示了这一点。

正则化函数通过雅可比矩阵 $\mathbf{J}$ 依赖于网络权重。扩展 5.3 节介绍的方法，就可以容易地得到一个反向传播形式，用于计算正则化项关于网络权重的导数（习题 5.26）。

如果变换由 $L$ 个参数控制，例如二维图像的平移与平面内旋转组合对应于 $L=3$，那么流形 $\mathcal{M}$ 的维数就是 $L$，相应的正则化项由若干个（5.128）形式的项相加得到，每个变换对应一项。如果同时考虑若干种变换，并使网络映射分别对每种变换保持不变，那么它对这些变换的组合也将具有局部不变性（Simard et al., 1992）。

<!-- pdf-page: 285 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-16.png" alt="原始手写数字、旋转切向量、线性近似结果与真实旋转图像四幅对照图"><figcaption>图 5.16：（a）手写数字的原始图像 $\mathbf{x}$；（b）与无穷小顺时针旋转相对应的切向量 $\boldsymbol{\tau}$；（c）在原图中加入少量切向量分量所得的结果 $\mathbf{x}+\epsilon\boldsymbol{\tau}$，其中 $\epsilon=15$ 度；（d）用于比较的真实旋转图像。</figcaption><p class="figure-translation">（a）原图；（b）切向量；（c）线性近似；（d）真实旋转图像。</p></figure>

一种相关方法称为*切向距离*（tangent distance），可以将不变性引入最近邻分类器等基于实例（instance-based）的方法中（Simard et al., 1993）。

### 5.5.5 使用变换后的数据训练

我们已经看到，要促使模型对一组变换保持不变，一种方法是使用原始输入模式的变换版本来扩充训练集。这里将证明，这种方法与切向传播密切相关（Bishop, 1995b; Leen, 1995）。

与 5.5.4 节一样，考虑由单个参数 $\xi$ 控制、用函数 $\mathbf{s}(\mathbf{x},\xi)$ 描述的变换，其中 $\mathbf{s}(\mathbf{x},0)=\mathbf{x}$。同时考虑平方和误差函数。对于未经变换的输入，误差函数可以在无限数据集的极限下写为

$$
E=\frac{1}{2}\iint\{y(\mathbf{x})-t\}^2p(t\mid\mathbf{x})p(\mathbf{x})\,d\mathbf{x}\,dt
\tag{5.129}
$$

如 1.5.5 节所述。为了简化记号，这里考虑只有一个输出的网络。现在，假设对每个数据点生成无穷多个副本，并用变换对每个副本作扰动，

<!-- pdf-page: 286 -->
<!-- join-previous-paragraph -->
其中参数 $\xi$ 从分布 $p(\xi)$ 中抽取，那么在这个扩充数据集上定义的误差函数可以写为

$$
\widetilde{E}=\frac{1}{2}\iiint\{y(\mathbf{s}(\mathbf{x},\xi))-t\}^2p(t\mid\mathbf{x})p(\mathbf{x})p(\xi)\,d\mathbf{x}\,dt\,d\xi.
\tag{5.130}
$$

现在假设分布 $p(\xi)$ 的均值为零、方差较小，因此只考虑对原始输入向量的小幅变换。于是，可以将变换函数按 $\xi$ 的幂作泰勒展开，得到

$$
\begin{aligned}
\mathbf{s}(\mathbf{x},\xi)&=\mathbf{s}(\mathbf{x},0)+\left.\xi\frac{\partial}{\partial\xi}\mathbf{s}(\mathbf{x},\xi)\right|_{\xi=0}+\left.\frac{\xi^2}{2}\frac{\partial^2}{\partial\xi^2}\mathbf{s}(\mathbf{x},\xi)\right|_{\xi=0}+O(\xi^3)\\
&=\mathbf{x}+\xi\boldsymbol{\tau}+\frac{1}{2}\xi^2\boldsymbol{\tau}'+O(\xi^3)
\end{aligned}
$$

其中 $\boldsymbol{\tau}'$ 表示 $\mathbf{s}(\mathbf{x},\xi)$ 关于 $\xi$ 的二阶导数在 $\xi=0$ 处的值。由此可以将模型函数展开为

$$
y(\mathbf{s}(\mathbf{x},\xi))=y(\mathbf{x})+\xi\boldsymbol{\tau}^{\mathrm T}\nabla y(\mathbf{x})+\frac{\xi^2}{2}\left[(\boldsymbol{\tau}')^{\mathrm T}\nabla y(\mathbf{x})+\boldsymbol{\tau}^{\mathrm T}\nabla\nabla y(\mathbf{x})\boldsymbol{\tau}\right]+O(\xi^3).
$$

代入平均误差函数（5.130）并展开，得到

$$
\begin{aligned}
\widetilde{E}&=\frac{1}{2}\iint\{y(\mathbf{x})-t\}^2p(t\mid\mathbf{x})p(\mathbf{x})\,d\mathbf{x}\,dt\\
&\quad+\mathbb{E}[\xi]\iint\{y(\mathbf{x})-t\}\boldsymbol{\tau}^{\mathrm T}\nabla y(\mathbf{x})p(t\mid\mathbf{x})p(\mathbf{x})\,d\mathbf{x}\,dt\\
&\quad+\mathbb{E}[\xi^2]\iint\left[\{y(\mathbf{x})-t\}\frac{1}{2}\left\{(\boldsymbol{\tau}')^{\mathrm T}\nabla y(\mathbf{x})+\boldsymbol{\tau}^{\mathrm T}\nabla\nabla y(\mathbf{x})\boldsymbol{\tau}\right\}\right.\\
&\hspace{7em}\left.+\left(\boldsymbol{\tau}^{\mathrm T}\nabla y(\mathbf{x})\right)^2\right]p(t\mid\mathbf{x})p(\mathbf{x})\,d\mathbf{x}\,dt+O(\xi^3).
\end{aligned}
$$

由于变换分布的均值为零，有 $\mathbb{E}[\xi]=0$。再将 $\mathbb{E}[\xi^2]$ 记为 $\lambda$。忽略 $O(\xi^3)$ 项后，平均误差函数变为

$$
\widetilde{E}=E+\lambda\Omega
\tag{5.131}
$$

其中 $E$ 是原始平方和误差，而正则化项 $\Omega$ 具有如下形式：

$$
\begin{aligned}
\Omega&=\int\left[\{y(\mathbf{x})-\mathbb{E}[t\mid\mathbf{x}]\}\frac{1}{2}\left\{(\boldsymbol{\tau}')^{\mathrm T}\nabla y(\mathbf{x})+\boldsymbol{\tau}^{\mathrm T}\nabla\nabla y(\mathbf{x})\boldsymbol{\tau}\right\}\right.\\
&\qquad\left.+\left(\boldsymbol{\tau}^{\mathrm T}\nabla y(\mathbf{x})\right)^2\right]p(\mathbf{x})\,d\mathbf{x}
\end{aligned}
\tag{5.132}
$$

这里已经对 $t$ 完成积分。

<!-- pdf-page: 287 -->

这个正则化项还可以进一步简化。在 1.5.5 节中，我们看到，使平方和误差最小的函数是目标值 $t$ 的条件均值 $\mathbb{E}[t\mid\mathbf{x}]$。由（5.131）可知，正则化误差等于未正则化的平方和误差加上 $O(\xi)$ 阶的项，因此，使总误差最小的网络函数具有如下形式：

$$
y(\mathbf{x})=\mathbb{E}[t\mid\mathbf{x}]+O(\xi).
\tag{5.133}
$$

所以，在 $\xi$ 的最低阶近似下，正则化项中的第一项消失，只剩下

$$
\Omega=\frac{1}{2}\int\left(\boldsymbol{\tau}^{\mathrm T}\nabla y(\mathbf{x})\right)^2p(\mathbf{x})\,d\mathbf{x}
\tag{5.134}
$$

它与切向传播正则化项（5.128）等价。

如果考虑一种特殊情况，即输入变换仅仅是在输入上加上随机噪声，从而有 $\mathbf{x}\to\mathbf{x}+\boldsymbol{\xi}$，那么正则化项具有如下形式（习题 5.27）：

$$
\Omega=\frac{1}{2}\int\|\nabla y(\mathbf{x})\|^2p(\mathbf{x})\,d\mathbf{x}
\tag{5.135}
$$

这称为 *Tikhonov 正则化*（Tikhonov and Arsenin, 1977; Bishop, 1995b）。可以利用扩展的反向传播算法求出这个正则化项关于网络权重的导数（Bishop, 1993）。我们看到，当噪声幅度很小时，Tikhonov 正则化与向输入加入随机噪声有关；已有研究表明，在适当条件下，加入这样的噪声可以改善泛化能力（Sietsma and Dow, 1991）。

### 5.5.6 卷积网络

要使模型对输入的某些变换保持不变，另一种做法是将这些不变性纳入神经网络的结构。这是卷积神经网络（convolutional neural network）的基础（Le Cun et al., 1989; LeCun et al., 1998），这种网络已广泛用于图像数据。

考虑识别手写数字这一具体任务。每幅输入图像由一组像素强度值组成，希望得到的输出是十个数字类别上的后验概率分布。我们知道，平移、缩放以及小幅旋转都不会改变数字的类别。此外，网络还必须对更细微的变换保持不变，例如图 5.14 所示的弹性形变。一种简单做法是将图像作为图 5.1 那样的全连接网络的输入。只要训练集足够大，这种网络原则上就能很好地解决这个问题，并从示例中学到相应的不变性。

不过，这种做法忽略了图像的一项关键性质：相邻像素之间的相关性比相距较远的像素更强。许多现代计算机视觉方法利用了这一性质，提取仅依赖于图像小块区域的局部特征。随后，在后续处理阶段合并这些特征提供的信息，以检测更高阶的特征，

<!-- pdf-page: 288 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-17.png" alt="卷积神经网络的输入图像、卷积层和子采样层之间的局部连接"><figcaption>图 5.17：卷积神经网络的部分结构示意图，其中一层卷积单元之后连接一层子采样单元。可以连续使用若干对这样的层。</figcaption><p class="figure-translation">Input image → 输入图像；Convolutional layer → 卷积层；Sub-sampling layer → 子采样层。</p></figure>

<!-- join-previous-paragraph-across-figures -->
最终获得关于整幅图像的信息。另外，在图像某个区域中有用的局部特征，在其他区域中也很可能有用，例如在关注的物体发生平移时。

卷积神经网络通过三种机制融入这些思想：（i）局部感受野；（ii）权重共享；（iii）子采样。卷积网络的结构如图 5.17 所示。在卷积层中，单元组织成若干平面，每个平面称为一个*特征图*（feature map）。特征图中的每个单元仅接收来自图像某个小区域的输入，而且同一特征图中的所有单元都被约束为共享相同的权重值。例如，一个特征图可以由排列成 $10\times10$ 网格的 100 个单元组成，每个单元接收图像中一个 $5\times5$ 像素块的输入。因此，整个特征图共有 25 个可调权重参数，以及一个可调偏置参数。利用这些权重和偏置，将像素块的输入值作线性组合，再按照（5.1）通过 sigmoid 非线性变换得到结果。如果把这些单元看作特征检测器，那么同一特征图中的所有单元检测的都是同一种模式，只是它们在输入图像中的位置不同。由于采用了权重共享，计算这些单元的激活值，等价于将图像像素强度与由权重参数组成的“核”作卷积。如果输入图像发生平移，特征图中的激活值也会平移相同的距离，除此之外不发生变化。这为网络输出对输入图像的平移和畸变保持近似不变

<!-- pdf-page: 289 -->

<!-- join-previous-paragraph -->
奠定了基础。由于构建有效模型通常需要检测多种特征，卷积层一般会有多个特征图，每个特征图都有自己的一组权重和偏置参数。

卷积单元的输出构成网络中子采样层的输入。卷积层的每个特征图，在子采样层中都有一个对应的单元平面，其中每个单元都从卷积层相应特征图的一个小感受野接收输入。这些单元执行子采样。例如，每个子采样单元可以接收相应特征图中一个 $2\times2$ 单元区域的输入，计算这些输入的平均值，乘以一个可调权重，再加上一个可调偏置参数，最后通过 sigmoid 非线性激活函数变换。所选感受野彼此相邻而不重叠，因此，子采样层的行数和列数都只有卷积层的一半。这样，输入空间中相应区域的图像发生小幅平移时，子采样层单元的响应会相对不敏感。

在实际的网络结构中，可以包含多对卷积层和子采样层。与前一层相比，每个阶段对输入变换的不变性都会增强。前一个子采样层的每个单元平面，在给定的卷积层中可以对应多个特征图；这样，就通过不断增加特征的数量来补偿空间分辨率的逐步降低。网络的最后一层通常是所有参数均可调的全连接层，在多类分类的情况下，其输出非线性函数为 softmax。

整个网络可以通过误差最小化来训练，并用反向传播计算误差函数的梯度。为此，需要对通常的反向传播算法稍作修改，以保证满足共享权重的约束（习题 5.28）。由于采用了局部感受野，网络中的权重数量少于全连接网络。又由于权重受到大量约束，需要从数据中学习的独立参数数量还会少得多。

### 5.5.7 软权重共享

对于具有大量权重的网络，一种降低其有效复杂度的方法，是将某些组内的权重约束为相等。这就是 5.5.6 节讨论的权重共享技术，该节用它将平移不变性纳入用于图像解释的网络。不过，这种技术只适用于能够预先指定约束形式的特定问题。这里，我们考虑一种*软权重共享*（soft weight sharing）方法（Nowlan and Hinton, 1992）：用一种正则化形式替代权重相等的硬约束，使同组权重倾向于取相近的值。此外，如何将权重分组、每组的权重均值，以及组内取值的分散程度，都作为学习过程的一部分来确定。

<!-- pdf-page: 290 -->

回顾（5.112）给出的简单权重衰减正则化项，它可以看作权重的高斯先验分布的负对数。如果改用高斯混合概率分布，就可以促使权重值形成多个组，而不是只有一个组（2.3.9 节）。高斯分量的中心、方差以及混合系数，都将视为可调参数，在学习过程中确定。因此，概率密度具有如下形式：

$$
p(\mathbf{w})=\prod_i p(w_i)
\tag{5.136}
$$

其中

$$
p(w_i)=\sum_{j=1}^{M}\pi_j\mathcal{N}(w_i\mid\mu_j,\sigma_j^2)
\tag{5.137}
$$

而 $\pi_j$ 是混合系数。取负对数，就得到如下形式的正则化函数：

$$
\Omega(\mathbf{w})=-\sum_i\ln\left(\sum_{j=1}^{M}\pi_j\mathcal{N}(w_i\mid\mu_j,\sigma_j^2)\right).
\tag{5.138}
$$

于是，总误差函数为

$$
\widetilde{E}(\mathbf{w})=E(\mathbf{w})+\lambda\Omega(\mathbf{w})
\tag{5.139}
$$

其中 $\lambda$ 是正则化系数。需要同时关于权重 $w_i$ 和混合模型的参数 $\{\pi_j,\mu_j,\sigma_j\}$ 最小化这个误差。如果权重固定，那么可以用第 9 章讨论的 EM 算法确定混合模型的参数。然而，在学习过程中，权重分布本身也在不断变化，因此，为避免数值不稳定，要同时对权重和混合模型参数进行联合优化。这可以通过共轭梯度法或拟牛顿法等标准优化算法来完成。

为了最小化总误差函数，需要能够计算它关于各个可调参数的导数。为此，可以方便地将 $\{\pi_j\}$ 看作先验概率，并引入相应的后验概率。由（2.192），根据贝叶斯定理，这些后验概率为

$$
\gamma_j(w)=\frac{\pi_j\mathcal{N}(w\mid\mu_j,\sigma_j^2)}{\sum_k\pi_k\mathcal{N}(w\mid\mu_k,\sigma_k^2)}.
\tag{5.140}
$$

于是，总误差函数关于权重的导数为（习题 5.29）

$$
\frac{\partial\widetilde{E}}{\partial w_i}=\frac{\partial E}{\partial w_i}+\lambda\sum_j\gamma_j(w_i)\frac{(w_i-\mu_j)}{\sigma_j^2}.
\tag{5.141}
$$

<!-- pdf-page: 291 -->

因此，正则化项会将每个权重拉向第 $j$ 个高斯分布的中心，拉力大小与给定该权重时这个高斯分布的后验概率成正比。这正是我们希望得到的效果。

误差关于各高斯分布中心的导数也很容易计算，结果为（习题 5.30）

$$
\frac{\partial\widetilde{E}}{\partial\mu_j}=\lambda\sum_i\gamma_j(w_i)\frac{(\mu_i-w_j)}{\sigma_j^2}
\tag{5.142}
$$

这个式子有简单直观的解释：它将 $\mu_j$ 推向权重值的加权平均值，而加权系数为相应权重参数由分量 $j$ 生成的后验概率。类似地，关于方差的导数为（习题 5.31）

$$
\frac{\partial\widetilde{E}}{\partial\sigma_j}=\lambda\sum_i\gamma_j(w_i)\left(\frac{1}{\sigma_j}-\frac{(w_i-\mu_j)^2}{\sigma_j^3}\right)
\tag{5.143}
$$

它将 $\sigma_j$ 推向各权重相对于相应中心 $\mu_j$ 的偏差平方的加权平均值；这里，加权系数仍然是每个权重由分量 $j$ 生成的后验概率。注意，在实际实现中，要引入新变量 $\eta_j$，定义为

$$
\sigma_j^2=\exp(\eta_j)
\tag{5.144}
$$

并关于 $\eta_j$ 进行最小化。这保证了参数 $\sigma_j$ 始终为正。它还会抑制一种病态解：一个或多个 $\sigma_j$ 趋于零，这相当于某个高斯分量坍缩到一个权重参数值上。9.2.1 节讨论高斯混合模型时，将更详细地介绍这类解。

对于关于混合系数 $\pi_j$ 的导数，我们需要考虑约束

$$
\sum_j\pi_j=1,\qquad 0\leqslant\pi_i\leqslant1
\tag{5.145}
$$

这些约束来自将 $\pi_j$ 解释为先验概率。可以利用 softmax 函数，将混合系数表示为一组辅助变量 $\{\eta_j\}$ 的函数，从而满足这些约束：

$$
\pi_j=\frac{\exp(\eta_j)}{\sum_{k=1}^{M}\exp(\eta_k)}.
\tag{5.146}
$$

于是，正则化误差函数关于 $\{\eta_j\}$ 的导数具有如下形式（习题 5.32）：

<!-- pdf-page: 292 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-18.png" alt="双连杆机械臂的正运动学及肘部向上和向下两种逆运动学解"><figcaption>图 5.18：左图为一个双连杆机械臂，末端执行器的笛卡尔坐标 $(x_1,x_2)$ 由两个关节角 $\theta_1$、$\theta_2$ 和连杆的固定长度 $L_1$、$L_2$ 唯一确定。这称为机械臂的正运动学。在实际应用中，我们必须求出能够使末端执行器到达所需位置的关节角。如右图所示，这个逆运动学问题有两个解，分别对应“肘部向上”和“肘部向下”。</figcaption><p class="figure-translation">elbow up → 肘部向上；elbow down → 肘部向下；$L_1,L_2$：连杆长度；$\theta_1,\theta_2$：关节角；$(x_1,x_2)$：末端执行器坐标。</p></figure>

$$
\frac{\partial\widetilde{E}}{\partial\eta_j}=\sum_i\{\pi_j-\gamma_j(w_i)\}.
\tag{5.147}
$$

由此可见，$\pi_j$ 会被推向分量 $j$ 的平均后验概率。

## 5.6 混合密度网络

监督学习的目标是对条件分布 $p(\mathbf{t}\mid\mathbf{x})$ 建模。对于许多简单回归问题，这个分布被选为高斯分布。然而，实际机器学习问题中的分布常常明显偏离高斯分布。例如，在*逆问题*（inverse problem）中，分布可能具有多个峰，此时，高斯假设可能导致很差的预测。

作为逆问题的一个简单例子，考虑图 5.18 所示机械臂的运动学（习题 5.33）。*正问题*（forward problem）是给定关节角求末端执行器的位置，它有唯一解。不过，在实际应用中，我们希望将机器人的末端执行器移动到指定位置，为此必须设置适当的关节角。因此，我们需要求解逆问题；如图 5.18 所示，它有两个解。

正问题往往对应于物理系统中的因果关系，并且通常具有唯一解。例如，人体出现某种特定的症状模式，可能是由某种特定疾病引起的。然而，在模式识别中，我们通常必须求解逆问题，例如根据一组症状尝试预测是否患有某种疾病。如果正问题涉及多对一映射，那么逆问题就会有多个解。例如，多种不同疾病可能造成相同的症状。

在机械臂的例子中，运动学由几何方程定义，多峰性十分明显。不过，在许多机器学习问题中，尤其是涉及高维空间的问题中，多峰性的存在可能并不那么容易看出来。为了便于说明，我们将考虑一个简单的玩具问题，其多峰性很容易可视化。这个问题的数据通过在区间 $(0,1)$ 上均匀采样变量 $x$ 来生成，得到一组取值 $\{x_n\}$，对应的目标值 $t_n$ 则通过

<!-- pdf-page: 293 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-19.png" alt="简单正问题和交换输入目标后的逆问题，以及平方和误差训练的网络拟合曲线"><figcaption>图 5.19：左图是一个简单“正问题”的数据集，红色曲线表示通过最小化平方和误差函数来拟合两层神经网络所得的结果。右图是交换 $x$ 和 $t$ 的角色后得到的相应逆问题。由于数据集具有多峰性，再次通过最小化平方和误差函数训练的同一网络，对这些数据的拟合效果很差。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
计算函数 $x_n+0.3\sin(2\pi x_n)$，再加上区间 $(-0.1,0.1)$ 上的均匀噪声来得到。保持数据点不变，交换 $x$ 和 $t$ 的角色，就得到逆问题。图 5.19 给出了正问题和逆问题的数据集，以及通过最小化平方和误差函数，使用具有 6 个隐藏单元和一个线性输出单元的两层神经网络进行拟合的结果。最小二乘对应于高斯假设下的最大似然。我们看到，对于明显偏离高斯分布的逆问题，这种做法得到的模型很差。

因此，我们希望找到一个对条件概率分布建模的通用框架。可以使用 $p(\mathbf{t}\mid\mathbf{x})$ 的混合模型来实现这一点，其中混合系数和各分量密度都是输入向量 $\mathbf{x}$ 的灵活函数，这就得到*混合密度网络*（mixture density network）。对于任意给定的 $\mathbf{x}$，混合模型提供了一种对任意条件密度函数 $p(\mathbf{t}\mid\mathbf{x})$ 建模的通用形式。只要所考虑的网络足够灵活，就得到了一个能够近似任意条件分布的框架。

这里，我们针对高斯分量具体构建这个模型，从而有

$$
p(\mathbf{t}\mid\mathbf{x})=\sum_{k=1}^{K}\pi_k(\mathbf{x})\mathcal{N}\left(\mathbf{t}\mid\boldsymbol{\mu}_k(\mathbf{x}),\sigma_k^2(\mathbf{x})\right).
\tag{5.148}
$$

这是一个*异方差*（heteroscedastic）模型的例子，因为数据上的噪声方差是输入向量 $\mathbf{x}$ 的函数。各分量也可以使用高斯分布之外的其他分布；例如，目标变量是二元变量而非连续变量时，可以使用伯努利分布。这里还将讨论限定在各分量具有各向同性协方差的情况，不过，通过 Cholesky 分解来表示协方差，很容易将混合密度网络扩展到一般协方差矩阵的情况（Williams, 1996）。即使各分量都是各向同性的，由于采用了混合分布，条件分布 $p(\mathbf{t}\mid\mathbf{x})$ 也不要求按 $\mathbf{t}$ 的各个分量进行因子分解，这与标准的平方和回归模型不同。

现在，我们令混合模型的各个参数，即混合系数 $\pi_k(\mathbf{x})$、均值 $\boldsymbol{\mu}_k(\mathbf{x})$ 和方差 $\sigma_k^2(\mathbf{x})$，由

<!-- pdf-page: 294 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-20.png" alt="神经网络根据输入向量给出混合模型参数，再由混合模型形成条件概率密度"><figcaption>图 5.20：混合密度网络能够表示一般的条件概率密度 $p(\mathbf{t}\mid\mathbf{x})$：对 $\mathbf{t}$ 的分布采用参数化混合模型，其参数由一个以 $\mathbf{x}$ 为输入向量的神经网络的输出确定。</figcaption><p class="figure-translation">$x_1,\ldots,x_D$：输入分量；$\theta_1,\ldots,\theta_M$：混合模型参数；$\boldsymbol{\theta}$：参数向量；$p(t\mid\mathbf{x})$：条件概率密度。</p></figure>

<!-- join-previous-paragraph-across-figures -->
一个以 $\mathbf{x}$ 为输入的常规神经网络的输出决定。这个混合密度网络的结构如图 5.20 所示。混合密度网络与 14.5.3 节讨论的专家混合密切相关。主要区别在于，混合密度网络使用同一个函数来预测所有分量密度的参数以及混合系数，因此，这些依赖于输入的函数共享非线性隐藏单元。

例如，图 5.20 中的神经网络可以是一个隐藏单元采用 sigmoid（“tanh”）函数的两层网络。如果混合模型（5.148）中有 $L$ 个分量，而 $\mathbf{t}$ 有 $K$ 个分量，那么网络将具有 $L$ 个输出单元激活值，记为 $a_k^{\pi}$，用于确定混合系数 $\pi_k(\mathbf{x})$；$K$ 个输出，记为 $a_k^{\sigma}$，用于确定核宽度 $\sigma_k(\mathbf{x})$；以及 $L\times K$ 个输出，记为 $a_{kj}^{\mu}$，用于确定核中心 $\boldsymbol{\mu}_k(\mathbf{x})$ 的各个分量 $\mu_{kj}(\mathbf{x})$。网络输出的总数为 $(K+2)L$；相比之下，仅预测目标变量条件均值的通常网络只有 $K$ 个输出。

混合系数必须满足约束

$$
\sum_{k=1}^{K}\pi_k(\mathbf{x})=1,\qquad0\leqslant\pi_k(\mathbf{x})\leqslant1
\tag{5.149}
$$

这可以用一组 softmax 输出来实现：

$$
\pi_k(\mathbf{x})=\frac{\exp(a_k^{\pi})}{\sum_{l=1}^{K}\exp(a_l^{\pi})}.
\tag{5.150}
$$

类似地，方差必须满足 $\sigma_k^2(\mathbf{x})\geqslant0$，因此，可以用相应网络激活值的指数来表示：

$$
\sigma_k(\mathbf{x})=\exp(a_k^{\sigma}).
\tag{5.151}
$$

最后，由于均值 $\boldsymbol{\mu}_k(\mathbf{x})$ 的各分量为实数，可以

<!-- pdf-page: 295 -->

<!-- join-previous-paragraph -->
直接用网络输出激活值表示：

$$
\mu_{kj}(\mathbf{x})=a_{kj}^{\mu}.
\tag{5.152}
$$

混合密度网络的可调参数由神经网络中权重和偏置构成的向量 $\mathbf{w}$ 组成，可以通过最大似然来确定；等价地，也可以最小化定义为似然负对数的误差函数。对于相互独立的数据，这个误差函数具有如下形式：

$$
E(\mathbf{w})=-\sum_{n=1}^{N}\ln\left\{\sum_{k=1}^{k}\pi_k(\mathbf{x}_n,\mathbf{w})\mathcal{N}\left(\mathbf{t}_n\mid\boldsymbol{\mu}_k(\mathbf{x}_n,\mathbf{w}),\sigma_k^2(\mathbf{x}_n,\mathbf{w})\right)\right\}
\tag{5.153}
$$

这里显式写出了对 $\mathbf{w}$ 的依赖。

为了最小化误差函数，需要计算误差 $E(\mathbf{w})$ 关于 $\mathbf{w}$ 各分量的导数。只要得到误差关于输出单元激活值的合适导数表达式，就可以用标准的反向传播过程来计算这些导数。这些导数代表每个模式、每个输出单元的误差信号 $\delta$，可以将它们反向传播到隐藏单元，再按通常的方法计算误差函数的导数。由于误差函数（5.153）由若干项求和组成，每个训练数据点对应一项，因此，可以先考虑某个特定模式 $n$ 的导数，再对所有模式求和，得到 $E$ 的导数。

由于处理的是混合分布，可以方便地将混合系数 $\pi_k(\mathbf{x})$ 看作依赖于 $\mathbf{x}$ 的先验概率，并引入相应的后验概率：

$$
\gamma_k(\mathbf{t}\mid\mathbf{x})=\frac{\pi_k\mathcal{N}_{nk}}{\sum_{l=1}^{K}\pi_l\mathcal{N}_{nl}}
\tag{5.154}
$$

其中 $\mathcal{N}_{nk}$ 表示 $\mathcal{N}(\mathbf{t}_n\mid\boldsymbol{\mu}_k(\mathbf{x}_n),\sigma_k^2(\mathbf{x}_n))$。

关于控制混合系数的网络输出激活值的导数为（习题 5.34）

$$
\frac{\partial E_n}{\partial a_k^{\pi}}=\pi_k-\gamma_k.
\tag{5.155}
$$

类似地，关于控制分量均值的输出激活值的导数为（习题 5.35）

$$
\frac{\partial E_n}{\partial a_{kl}^{\mu}}=\gamma_k\left\{\frac{\mu_{kl}-t_l}{\sigma_k^2}\right\}.
\tag{5.156}
$$

最后，关于控制分量方差的输出激活值的导数为（习题 5.36）

$$
\frac{\partial E_n}{\partial a_k^{\sigma}}=-\gamma_k\left\{\frac{\|\mathbf{t}-\boldsymbol{\mu}_k\|^2}{\sigma_k^3}-\frac{1}{\sigma_k}\right\}.
\tag{5.157}
$$

<!-- pdf-page: 296 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-21.png" alt="混合密度网络的混合系数、分量均值、条件密度等高线与条件众数"><figcaption>图 5.21：（a）用图 5.19 所示数据训练的混合密度网络中，三个核函数的混合系数 $\pi_k(x)$ 随 $x$ 变化的曲线。该模型具有三个高斯分量，采用一个两层多层感知机，其隐藏层有五个“tanh” sigmoid 单元，输出有九个，分别对应高斯分量的 3 个均值、3 个方差和 3 个混合系数。在 $x$ 较小和较大时，目标数据的条件概率密度是单峰的，此时只有一个核的先验概率较高；在 $x$ 取中间值时，条件密度具有三个峰，此时三个混合系数的大小相近。（b）均值 $\mu_k(x)$ 的曲线，颜色与混合系数图中的对应分量一致。（c）同一个混合密度网络给出的目标数据条件概率密度的等高线。（d）条件密度的近似条件众数，以红色点表示。</figcaption></figure>

回到图 5.19 所示的逆问题玩具例子，来说明混合密度网络的用法。图 5.21 给出了混合系数 $\pi_k(x)$、均值 $\mu_k(x)$ 以及 $p(t\mid x)$ 对应的条件密度等高线。神经网络的输出，以及由它们决定的混合模型参数，必然是输入变量的连续单值函数。不过，从图 5.21（c）可以看到，通过调节各混合分量的幅度 $\pi_k(x)$，该模型能够得到一种条件密度：对于某些 $x$ 值，它是单峰的；对于其他 $x$ 值，它则具有三个峰。

混合密度网络训练完成后，就可以为任意给定的输入向量值，预测目标数据的条件密度函数。就预测输出向量的值这一问题而言，这个条件密度完整描述了数据的生成过程。根据这个密度函数，可以计算不同应用中可能感兴趣的更具体的量。其中最简单的一种是均值，它对应于目标数据的条件平均值，由下式给出：

$$
\mathbb{E}[\mathbf{t}\mid\mathbf{x}]=\int\mathbf{t}p(\mathbf{t}\mid\mathbf{x})\,d\mathbf{t}=\sum_{k=1}^{K}\pi_k(\mathbf{x})\boldsymbol{\mu}_k(\mathbf{x})
\tag{5.158}
$$

<!-- pdf-page: 297 -->

这里使用了（5.148）。由于用最小二乘训练的标准网络是在近似条件均值，我们看到，常规的最小二乘结果可以作为混合密度网络的一种特殊情况。当然，正如已经指出的，对于多峰分布，条件均值的价值有限。

类似地，可以计算密度函数相对于条件均值的方差，得到（习题 5.37）

$$
s^2(\mathbf{x})=\mathbb{E}\left[\|\mathbf{t}-\mathbb{E}[\mathbf{t}\mid\mathbf{x}]\|^2\mid\mathbf{x}\right]
\tag{5.159}
$$

$$
=\sum_{k=1}^{K}\pi_k(\mathbf{x})\left\{\sigma_k^2(\mathbf{x})+\left\|\boldsymbol{\mu}_k(\mathbf{x})-\sum_{l=1}^{K}\pi_l(\mathbf{x})\boldsymbol{\mu}_l(\mathbf{x})\right\|^2\right\}
\tag{5.160}
$$

这里使用了（5.148）和（5.158）。这比相应的最小二乘结果更一般，因为方差是 $\mathbf{x}$ 的函数。

我们已经看到，对于多峰分布，条件均值可能无法很好地代表数据。例如，在控制图 5.18 所示的简单机械臂时，为了达到所需的末端执行器位置，需要从两种可能的关节角设置中选择一种；而两个解的平均值本身并不是一个解。在这种情况下，条件众数可能更有价值。由于混合密度网络的条件众数没有简单的解析解，求解它需要进行数值迭代。一种简单的替代方法是：对于每个 $\mathbf{x}$ 值，取最有可能的分量，即混合系数最大的分量的均值。图 5.21（d）给出了玩具数据集上的这一结果。

## 5.7 贝叶斯神经网络

到目前为止，对神经网络的讨论集中于使用最大似然来确定网络参数，即权重和偏置。正则化最大似然可以解释为 MAP（最大后验）方法，其中正则化项可以看作参数先验分布的对数。不过，在贝叶斯处理中，需要对参数分布进行边缘化，才能作出预测。

在 3.3 节中，我们在高斯噪声假设下，推导了简单线性回归模型的贝叶斯解。我们看到，可以精确求出高斯形式的后验分布，也可以得到预测分布的闭式表达。对于多层网络，网络函数对参数值具有高度非线性的依赖，这意味着无法再得到精确的贝叶斯处理结果。事实上，后验分布的对数将是非凸的，对应于误差函数中的多个局部极小值。

第 10 章将讨论的变分推断技术已经被用于贝叶斯神经网络，其中既有用因子分解形式的高斯分布来近似

<!-- pdf-page: 298 -->

<!-- join-previous-paragraph -->
后验分布的方法（Hinton and van Camp, 1993），也有采用具有完整协方差的高斯分布的方法（Barber and Bishop, 1998a; Barber and Bishop, 1998b）。不过，最完整的处理是基于拉普拉斯近似的方法（MacKay, 1992c; MacKay, 1992b），这里的讨论将以它为基础。我们将用一个以真实后验分布的某个众数为中心的高斯分布，来近似后验分布。此外，假设这个高斯分布的协方差很小，从而在参数空间中后验概率明显非零的区域内，网络函数关于参数近似为线性函数。在这两个近似下，得到的模型将类似于前面各章讨论过的线性回归和分类模型，因此可以利用那里得到的结果。随后，可以利用证据框架对超参数进行点估计，并比较不同的模型，例如隐藏单元数量不同的网络。我们先讨论回归情况，再考虑解决分类任务所需的修改。

### 5.7.1 参数的后验分布

考虑根据输入向量 $\mathbf{x}$ 预测单个连续目标变量 $t$ 的问题，扩展到多个目标变量很直接。假设条件分布 $p(t\mid\mathbf{x})$ 是高斯分布，它的均值依赖于 $\mathbf{x}$，由神经网络模型的输出 $y(\mathbf{x},\mathbf{w})$ 给出，精度即方差的倒数为 $\beta$：

$$
p(t\mid\mathbf{x},\mathbf{w},\beta)=\mathcal{N}(t\mid y(\mathbf{x},\mathbf{w}),\beta^{-1}).
\tag{5.161}
$$

类似地，选择权重 $\mathbf{w}$ 的先验分布为如下形式的高斯分布：

$$
p(\mathbf{w}\mid\alpha)=\mathcal{N}(\mathbf{w}\mid\mathbf{0},\alpha^{-1}\mathbf{I}).
\tag{5.162}
$$

对于由 $N$ 个独立同分布的观测 $\mathbf{x}_1,\ldots,\mathbf{x}_N$ 构成的数据集，以及相应的目标值集合 $\mathcal{D}=\{t_1,\ldots,t_N\}$，似然函数为

$$
p(\mathcal{D}\mid\mathbf{w},\beta)=\prod_{n=1}^{N}\mathcal{N}(t_n\mid y(\mathbf{x}_n,\mathbf{w}),\beta^{-1})
\tag{5.163}
$$

从而得到后验分布

$$
p(\mathbf{w}\mid\mathcal{D},\alpha,\beta)\propto p(\mathbf{w}\mid\alpha)p(\mathcal{D}\mid\mathbf{w},\beta).
\tag{5.164}
$$

由于 $y(\mathbf{x},\mathbf{w})$ 对 $\mathbf{w}$ 的依赖是非线性的，这个分布将不是高斯分布。

可以利用拉普拉斯近似，找到后验分布的高斯近似。为此，首先必须找到后验分布的一个局部极大值，这必须通过迭代数值优化来完成。像通常一样，最大化后验分布的对数比较方便，它可以写成如下

<!-- pdf-page: 299 -->

<!-- join-previous-paragraph -->
形式：

$$
\ln p(\mathbf{w}\mid\mathcal{D})=-\frac{\alpha}{2}\mathbf{w}^{\mathrm T}\mathbf{w}-\frac{\beta}{2}\sum_{n=1}^{N}\{y(\mathbf{x}_n,\mathbf{w})-t_n\}^2+\mathrm{const}
\tag{5.165}
$$

这对应于正则化的平方和误差函数。暂时假设 $\alpha$ 和 $\beta$ 固定，就可以使用共轭梯度法等标准非线性优化算法，找到后验分布的一个极大值，记为 $\mathbf{w}_{\mathrm{MAP}}$，并通过误差反向传播计算所需的导数。

找到一个众数 $\mathbf{w}_{\mathrm{MAP}}$ 后，就可以计算后验分布负对数的二阶导数矩阵，从而构建局部高斯近似。由（5.165），该矩阵为

$$
\mathbf{A}=-\nabla\nabla\ln p(\mathbf{w}\mid\mathcal{D},\alpha,\beta)=\alpha\mathbf{I}+\beta\mathbf{H}
\tag{5.166}
$$

其中 $\mathbf{H}$ 是由平方和误差函数关于 $\mathbf{w}$ 各分量的二阶导数组成的 Hessian 矩阵。5.4 节讨论了计算和近似 Hessian 矩阵的算法。于是，由（4.134），后验分布的相应高斯近似为

$$
q(\mathbf{w}\mid\mathcal{D})=\mathcal{N}(\mathbf{w}\mid\mathbf{w}_{\mathrm{MAP}},\mathbf{A}^{-1}).
\tag{5.167}
$$

类似地，通过关于这个后验分布进行边缘化，得到预测分布

$$
p(t\mid\mathbf{x},\mathcal{D})=\int p(t\mid\mathbf{x},\mathbf{w})q(\mathbf{w}\mid\mathcal{D})\,d\mathbf{w}.
\tag{5.168}
$$

不过，即使采用了后验分布的高斯近似，由于网络函数 $y(\mathbf{x},\mathbf{w})$ 关于 $\mathbf{w}$ 是非线性函数，这个积分仍然无法解析求出。为了继续推导，现在假设：与 $y(\mathbf{x},\mathbf{w})$ 发生变化时 $\mathbf{w}$ 的特征尺度相比，后验分布的方差很小。这样，就可以在 $\mathbf{w}_{\mathrm{MAP}}$ 附近对网络函数作泰勒级数展开，并仅保留线性项：

$$
y(\mathbf{x},\mathbf{w})\simeq y(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})+\mathbf{g}^{\mathrm T}(\mathbf{w}-\mathbf{w}_{\mathrm{MAP}})
\tag{5.169}
$$

其中定义了

$$
\mathbf{g}=\left.\nabla_{\mathbf{w}}y(\mathbf{x},\mathbf{w})\right|_{\mathbf{w}=\mathbf{w}_{\mathrm{MAP}}}.
\tag{5.170}
$$

在这个近似下，我们得到一个线性高斯模型：$p(\mathbf{w})$ 是高斯分布，$p(t\mid\mathbf{w})$ 也是高斯分布，而后者的均值是 $\mathbf{w}$ 的线性函数，具有如下形式：

$$
p(t\mid\mathbf{x},\mathbf{w},\beta)\simeq\mathcal{N}\left(t\mid y(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})+\mathbf{g}^{\mathrm T}(\mathbf{w}-\mathbf{w}_{\mathrm{MAP}}),\beta^{-1}\right).
\tag{5.171}
$$

因此，可以利用边缘分布 $p(t)$ 的一般结果（2.115），得到（习题 5.38）

$$
p(t\mid\mathbf{x},\mathcal{D},\alpha,\beta)=\mathcal{N}\left(t\mid y(\mathbf{x},\mathbf{w}_{\mathrm{MAP}}),\sigma^2(\mathbf{x})\right)
\tag{5.172}
$$

<!-- pdf-page: 300 -->

其中，依赖于输入的方差为

$$
\sigma^2(\mathbf{x})=\beta^{-1}+\mathbf{g}^{\mathrm T}\mathbf{A}^{-1}\mathbf{g}.
\tag{5.173}
$$

我们看到，预测分布 $p(t\mid\mathbf{x},\mathcal{D})$ 是高斯分布，其均值由参数取 MAP 值时的网络函数 $y(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})$ 给出。方差包含两项：第一项来自目标变量的内在噪声；第二项依赖于 $\mathbf{x}$，表示模型参数 $\mathbf{w}$ 的不确定性所导致的插值函数的不确定性。可以将它与（3.58）和（3.59）给出的线性回归模型的相应预测分布进行比较。

### 5.7.2 超参数优化

到目前为止，假设超参数 $\alpha$ 和 $\beta$ 固定且已知。可以结合 3.5 节讨论的证据框架，以及通过拉普拉斯近似得到的后验高斯近似，获得一种选择这些超参数值的实用过程。

通过对网络权重积分，得到超参数的边缘似然，也就是证据：

$$
p(\mathcal{D}\mid\alpha,\beta)=\int p(\mathcal{D}\mid\mathbf{w},\beta)p(\mathbf{w}\mid\alpha)\,d\mathbf{w}.
\tag{5.174}
$$

利用拉普拉斯近似的结果（4.135），很容易计算这个积分（习题 5.39）。然后取对数，得到

$$
\ln p(\mathcal{D}\mid\alpha,\beta)\simeq-E(\mathbf{w}_{\mathrm{MAP}})-\frac{1}{2}\ln|\mathbf{A}|+\frac{W}{2}\ln\alpha+\frac{N}{2}\ln\beta-\frac{N}{2}\ln(2\pi)
\tag{5.175}
$$

其中 $W$ 是 $\mathbf{w}$ 中参数的总数，正则化误差函数定义为

$$
E(\mathbf{w}_{\mathrm{MAP}})=\frac{\beta}{2}\sum_{n=1}^{N}\{y(\mathbf{x}_n,\mathbf{w}_{\mathrm{MAP}})-t_n\}^2+\frac{\alpha}{2}\mathbf{w}_{\mathrm{MAP}}^{\mathrm T}\mathbf{w}_{\mathrm{MAP}}.
\tag{5.176}
$$

可以看到，它与线性回归模型的相应结果（3.86）具有相同的形式。

在证据框架中，通过最大化 $\ln p(\mathcal{D}\mid\alpha,\beta)$，得到 $\alpha$ 和 $\beta$ 的点估计。首先考虑关于 $\alpha$ 的最大化，这可以参照 3.5.2 节讨论的线性回归情况来完成。先定义特征值方程

$$
\beta\mathbf{H}\mathbf{u}_i=\lambda_i\mathbf{u}_i
\tag{5.177}
$$

其中 $\mathbf{H}$ 是由平方和误差函数的二阶导数组成的 Hessian 矩阵，在 $\mathbf{w}=\mathbf{w}_{\mathrm{MAP}}$ 处取值。类比（3.92），得到

$$
\alpha=\frac{\gamma}{\mathbf{w}_{\mathrm{MAP}}^{\mathrm T}\mathbf{w}_{\mathrm{MAP}}}
\tag{5.178}
$$

<!-- pdf-page: 301 -->

其中 $\gamma$ 表示参数的有效数目（3.5.3 节），定义为

$$
\gamma=\sum_{i=1}^{W}\frac{\lambda_i}{\alpha+\lambda_i}.
\tag{5.179}
$$

注意，对于线性回归，这个结果是精确的。但对于非线性神经网络，它忽略了这样一个事实：$\alpha$ 的变化会使 Hessian 矩阵 $\mathbf{H}$ 改变，进而改变特征值。因此，这里隐含地忽略了包含 $\lambda_i$ 关于 $\alpha$ 的导数的项。

类似地，由（3.95）可以看到，关于 $\beta$ 最大化证据，得到重估公式

$$
\frac{1}{\beta}=\frac{1}{N-\gamma}\sum_{n=1}^{N}\{y(\mathbf{x}_n,\mathbf{w}_{\mathrm{MAP}})-t_n\}^2.
\tag{5.180}
$$

与线性模型一样，需要交替进行超参数 $\alpha$、$\beta$ 的重估和后验分布的更新。不过，由于后验分布具有多个峰，神经网络模型的情况更复杂。因此，通过最大化对数后验得到的解 $\mathbf{w}_{\mathrm{MAP}}$，将依赖于 $\mathbf{w}$ 的初始化。如果两个解的区别仅来自隐藏单元的交换对称性和符号反转对称性（5.1.1 节），那么就预测而言，它们完全相同；找到其中哪一个等价解并不重要。不过，也可能存在不等价的解，这些解通常会给出不同的最优超参数值。

为了比较不同的模型，例如隐藏单元数量不同的神经网络，需要计算模型证据 $p(\mathcal{D})$。可以将迭代优化超参数得到的 $\alpha$ 和 $\beta$ 值代入（5.175），从而近似这个证据。更细致的计算是再次作高斯近似，并对 $\alpha$ 和 $\beta$ 进行边缘化（MacKay, 1992c; Bishop, 1995a）。无论哪种情况，都需要计算 Hessian 矩阵的行列式 $|\mathbf{A}|$。这在实际应用中可能会带来问题，因为与迹不同，行列式对小特征值很敏感，而这些小特征值往往难以精确确定。

拉普拉斯近似基于权重后验分布某个众数附近的局部二次展开。在 5.1.1 节中，我们已经看到，两层网络中任意给定的众数，都属于一个包含 $M!2^M$ 个等价众数的集合；这些众数之间的区别来自交换和符号变换对称性，其中 $M$ 为隐藏单元的数量。在比较隐藏单元数量不同的网络时，可以将证据乘以因子 $M!2^M$，把这一点考虑进去。

### 5.7.3 用于分类的贝叶斯神经网络

到目前为止，我们利用拉普拉斯近似，对神经网络回归模型进行了贝叶斯处理。现在讨论

<!-- pdf-page: 302 -->

<!-- join-previous-paragraph -->
将这个框架用于分类时需要作出的修改。这里，考虑一个具有单个 logistic sigmoid 输出的网络，对应于二类分类问题。扩展到具有多类 softmax 输出的网络很直接（习题 5.40）。我们将大量利用 4.5 节讨论线性分类模型时得到的类似结果，因此建议读者在学习本节前先熟悉那些内容。

这个模型的对数似然函数为

$$
\ln p(\mathcal{D}\mid\mathbf{w})=\sum_n=1^N\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}
\tag{5.181}
$$

其中 $t_n\in\{0,1\}$ 是目标值，$y_n\equiv y(\mathbf{x}_n,\mathbf{w})$。注意，这里没有超参数 $\beta$，因为假设数据点的标记是正确的。与前面一样，先验取（5.162）形式的各向同性高斯分布。

将拉普拉斯框架应用于这个模型时，第一阶段是初始化超参数 $\alpha$，然后通过最大化对数后验分布来确定参数向量 $\mathbf{w}$。这等价于最小化正则化误差函数

$$
E(\mathbf{w})=-\ln p(\mathcal{D}\mid\mathbf{w})+\frac{\alpha}{2}\mathbf{w}^{\mathrm T}\mathbf{w}
\tag{5.182}
$$

可以按照 5.3 节的讨论，将误差反向传播与标准优化算法结合来完成这一过程。

找到权重向量的一个解 $\mathbf{w}_{\mathrm{MAP}}$ 后，下一步是计算由负对数似然函数的二阶导数组成的 Hessian 矩阵 $\mathbf{H}$。例如，可以使用 5.4.5 节的精确方法，或者使用（5.85）给出的外积近似。负对数后验的二阶导数仍然可以写成（5.166）的形式，相应的后验高斯近似由（5.167）给出。

为了优化超参数 $\alpha$，再次最大化边缘似然；很容易证明，它具有如下形式（习题 5.41）：

$$
\ln p(\mathcal{D}\mid\alpha)\simeq-E(\mathbf{w}_{\mathrm{MAP}})-\frac{1}{2}\ln|\mathbf{A}|+\frac{W}{2}\ln\alpha+\mathrm{const}
\tag{5.183}
$$

其中正则化误差函数定义为

$$
E(\mathbf{w}_{\mathrm{MAP}})=-\sum_{n=1}^{N}\{t_n\ln y_n+(1-t_n)\ln(1-y_n)\}+\frac{\alpha}{2}\mathbf{w}_{\mathrm{MAP}}^{\mathrm T}\mathbf{w}_{\mathrm{MAP}}
\tag{5.184}
$$

其中 $y_n\equiv y(\mathbf{x}_n,\mathbf{w}_{\mathrm{MAP}})$。关于 $\alpha$ 最大化这个证据函数，再次得到（5.178）给出的重估方程。

图 5.22 以附录 A 讨论的二维合成数据为例，说明如何使用证据过程来确定 $\alpha$。

最后，还需要（5.168）定义的预测分布。由于网络函数的非线性，这个积分同样难以求解。

<!-- pdf-page: 303 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-22.png" alt="合成二类数据上的最优决策边界、最大似然网络边界和证据正则化网络边界"><figcaption>图 5.22：将证据框架应用于一个合成二类数据集的示例。绿色曲线为最优决策边界，黑色曲线是用最大似然拟合一个具有 8 个隐藏单元的两层网络所得的结果，红色曲线是加入正则化项后的结果，其中 $\alpha$ 通过证据过程优化，初始值为 $\alpha=0$。注意，证据过程大幅减轻了网络的过拟合。</figcaption></figure>

<!-- join-previous-paragraph-across-figures -->
最简单的近似是假设后验分布非常窄，从而作出近似

$$
p(t\mid\mathbf{x},\mathcal{D})\simeq p(t\mid\mathbf{x},\mathbf{w}_{\mathrm{MAP}}).
\tag{5.185}
$$

不过，通过考虑后验分布的方差，可以改进这一近似。此时，像回归情况那样对网络输出作线性近似并不合适，因为输出单元的 logistic sigmoid 激活函数将输出限制在 $(0,1)$ 范围内。因此，改为对输出单元的激活值作如下线性近似：

$$
a(\mathbf{x},\mathbf{w})\simeq a_{\mathrm{MAP}}(\mathbf{x})+\mathbf{b}^{\mathrm T}(\mathbf{w}-\mathbf{w}_{\mathrm{MAP}})
\tag{5.186}
$$

其中 $a_{\mathrm{MAP}}(\mathbf{x})=a(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})$，向量 $\mathbf{b}\equiv\nabla a(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})$ 可以通过反向传播求得。

现在，$\mathbf{w}$ 的后验分布具有高斯近似，而且 $a$ 的模型是 $\mathbf{w}$ 的线性函数，因此可以利用 4.5.2 节的结果。由网络权重分布诱导的输出单元激活值分布为

$$
p(a\mid\mathbf{x},\mathcal{D})=\int\delta\left(a-a_{\mathrm{MAP}}(\mathbf{x})-\mathbf{b}^{\mathrm T}(\mathbf{x})(\mathbf{w}-\mathbf{w}_{\mathrm{MAP}})\right)q(\mathbf{w}\mid\mathcal{D})\,d\mathbf{w}
\tag{5.187}
$$

其中 $q(\mathbf{w}\mid\mathcal{D})$ 是（5.167）给出的后验分布的高斯近似。由 4.5.2 节可知，这个分布是高斯分布，均值为 $a_{\mathrm{MAP}}\equiv a(\mathbf{x},\mathbf{w}_{\mathrm{MAP}})$，方差为

$$
\sigma_a^2(\mathbf{x})=\mathbf{b}^{\mathrm T}(\mathbf{x})\mathbf{A}^{-1}\mathbf{b}(\mathbf{x}).
\tag{5.188}
$$

最后，为得到预测分布，必须对 $a$ 进行边缘化：

$$
p(t=1\mid\mathbf{x},\mathcal{D})=\int\sigma(a)p(a\mid\mathbf{x},\mathcal{D})\,da.
\tag{5.189}
$$

<!-- pdf-page: 304 -->

<figure><img src="books/bishop-pattern-recognition-2006/assets/chapter-05/b-fig-5-23.png" alt="贝叶斯神经网络中参数点估计与边缘化后的分类概率等高线比较"><figcaption>图 5.23：贝叶斯神经网络的拉普拉斯近似示例。网络包含 8 个采用“tanh”激活函数的隐藏单元，以及一个 logistic sigmoid 输出单元。权重参数通过缩放共轭梯度法求得，超参数 $\alpha$ 利用证据框架优化。左图是采用简单近似（5.185）的结果，该近似基于参数的点估计 $\mathbf{w}_{\mathrm{MAP}}$；其中绿色曲线表示 $y=0.5$ 的决策边界，其余等高线对应于 $y=0.1,0.3,0.7,0.9$ 的输出概率。右图是使用（5.190）得到的相应结果。注意，边缘化使等高线变得更分散，并使预测的置信程度降低，因此在每个输入点 $\mathbf{x}$ 处，后验概率都会向 0.5 移动，而 $y=0.5$ 等高线本身不受影响。</figcaption></figure>

高斯函数与 logistic sigmoid 函数的卷积无法解析求出。因此，对（5.189）应用近似（4.153），得到

$$
p(t=1\mid\mathbf{x},\mathcal{D})=\sigma\left(\kappa(\sigma_a^2)\mathbf{b}^{\mathrm T}\mathbf{w}_{\mathrm{MAP}}\right)
\tag{5.190}
$$

其中 $\kappa(\cdot)$ 由（4.154）定义。回顾一下，$\sigma_a^2$ 和 $\mathbf{b}$ 都是 $\mathbf{x}$ 的函数。

图 5.23 给出了将这个框架应用于附录 A 所述合成分类数据集的一个例子。

## 习题

**5.1（⋆⋆）** 考虑一个形式为（5.7）的两层网络函数，其中隐藏单元的非线性激活函数 $g(\cdot)$ 采用如下形式的 logistic sigmoid 函数：

$$
\sigma(a)=\{1+\exp(-a)\}^{-1}.
\tag{5.191}
$$

证明存在一个等价网络，它计算完全相同的函数，但隐藏单元的激活函数为 $\tanh(a)$，其中 $\tanh$ 函数由（5.59）定义。提示：先求出 $\sigma(a)$ 与 $\tanh(a)$ 的关系，再证明两个网络的参数之间相差线性变换。

**5.2（⋆）www** 证明，对于多输出神经网络，最大化条件分布（5.16）下的似然函数，等价于最小化平方和误差函数（5.11）。

<!-- pdf-page: 305 -->

**5.3（⋆⋆）** 考虑一个涉及多个目标变量的回归问题，假设给定输入向量 $\mathbf{x}$ 后，目标变量的分布为如下形式的高斯分布：

$$
p(\mathbf{t}\mid\mathbf{x},\mathbf{w})=\mathcal{N}(\mathbf{t}\mid\mathbf{y}(\mathbf{x},\mathbf{w}),\boldsymbol{\Sigma})
\tag{5.192}
$$

其中 $\mathbf{y}(\mathbf{x},\mathbf{w})$ 是输入向量为 $\mathbf{x}$、权重向量为 $\mathbf{w}$ 的神经网络的输出，$\boldsymbol{\Sigma}$ 是假设加在目标变量上的高斯噪声的协方差。给定一组 $\mathbf{x}$ 和 $\mathbf{t}$ 的独立观测，假设 $\boldsymbol{\Sigma}$ 固定且已知，写出为求得 $\mathbf{w}$ 的最大似然解而必须最小化的误差函数。现在假设 $\boldsymbol{\Sigma}$ 也需要从数据中确定，写出 $\boldsymbol{\Sigma}$ 的最大似然解的表达式。注意，此时 $\mathbf{w}$ 与 $\boldsymbol{\Sigma}$ 的优化相互耦合，这不同于 5.2 节讨论的目标变量相互独立的情况。

**5.4（⋆⋆）** 考虑一个二类分类问题，目标值为 $t\in\{0,1\}$，网络输出 $y(\mathbf{x},\mathbf{w})$ 表示 $p(t=1\mid\mathbf{x})$。假设训练数据点的类别标记有概率 $\epsilon$ 被错误地设置。在数据独立同分布的假设下，写出对应于负对数似然的误差函数。验证 $\epsilon=0$ 时得到误差函数（5.21）。注意，与通常的误差函数相比，这个误差函数使模型对错误标记的数据具有鲁棒性。

**5.5（⋆）www** 证明，对于一个多类神经网络模型，如果网络输出具有解释 $y_k(\mathbf{x},\mathbf{w})=p(t_k=1\mid\mathbf{x})$，那么最大化似然等价于最小化交叉熵误差函数（5.24）。

**5.6（⋆）www** 证明，对于采用 logistic sigmoid 激活函数的输出单元，误差函数（5.21）关于激活值 $a_k$ 的导数满足（5.18）。

**5.7（⋆）** 证明，对于采用 softmax 激活函数的输出单元，误差函数（5.24）关于激活值 $a_k$ 的导数满足（5.18）。

**5.8（⋆）** 我们在（4.88）中看到，logistic sigmoid 激活函数的导数可以用函数值本身表示。对（5.59）定义的“tanh”激活函数，推导相应的结果。

**5.9（⋆）www** 二类分类问题的误差函数（5.21）是在以下条件下推导的：网络采用 logistic sigmoid 输出激活函数，因此 $0\leqslant y(\mathbf{x},\mathbf{w})\leqslant1$，数据的目标值为 $t\in\{0,1\}$。如果考虑一个输出满足 $-1\leqslant y(\mathbf{x},\mathbf{w})\leqslant1$ 的网络，而且类别 $\mathcal{C}_1$ 的目标值为 $t=1$，类别 $\mathcal{C}_2$ 的目标值为 $t=-1$，推导相应的误差函数。应该选择什么样的输出单元激活函数？

**5.10（⋆）www** 考虑一个特征向量方程为（5.33）的 Hessian 矩阵 $\mathbf{H}$。依次将（5.39）中的向量 $\mathbf{v}$ 取为各个特征向量 $\mathbf{u}_i$，证明 $\mathbf{H}$ 正定当且仅当它的所有特征值均为正。

<!-- pdf-page: 306 -->

**5.11（⋆⋆）www** 考虑（5.32）定义的二次误差函数，其中 Hessian 矩阵 $\mathbf{H}$ 的特征值方程由（5.33）给出。证明等误差轮廓是椭圆，其轴与特征向量 $\mathbf{u}_i$ 的方向一致，轴长与对应特征值 $\lambda_i$ 的平方根成反比。

**5.12（⋆⋆）www** 考虑误差函数在驻点 $\mathbf{w}^{\star}$ 附近的局部泰勒展开（5.32），证明该驻点成为误差函数局部极小值点的充要条件是：在（5.30）中取 $\widehat{\mathbf{w}}=\mathbf{w}^{\star}$ 所定义的 Hessian 矩阵 $\mathbf{H}$ 为正定矩阵。

**5.13（⋆）** 证明，由于 Hessian 矩阵 $\mathbf{H}$ 的对称性，二次误差函数（5.28）中独立元素的数目为 $W(W+3)/2$。

**5.14（⋆）** 通过泰勒展开，验证（5.69）右端的 $O(\epsilon)$ 阶项相互抵消。

**5.15（⋆⋆）** 在 5.3.4 节中，我们推导了利用反向传播过程计算神经网络雅可比矩阵的方法。推导一种基于前向传播方程来求雅可比矩阵的替代方法。

**5.16（⋆）** 对于使用平方和误差函数的神经网络，Hessian 矩阵的外积近似由（5.84）给出。将这个结果扩展到多个输出的情况。

**5.17（⋆）** 考虑如下形式的平方损失函数：

$$
E=\frac{1}{2}\iint\{y(\mathbf{x},\mathbf{w})-t\}^2p(\mathbf{x},t)\,d\mathbf{x}\,dt
\tag{5.193}
$$

其中 $y(\mathbf{x},\mathbf{w})$ 是神经网络等参数化函数。结果（1.89）表明，使这个误差最小的函数 $y(\mathbf{x},\mathbf{w})$，由给定 $\mathbf{x}$ 时 $t$ 的条件期望给出。利用这个结果，证明 $E$ 关于向量 $\mathbf{w}$ 的两个元素 $w_r$ 和 $w_s$ 的二阶导数为

$$
\frac{\partial^2 E}{\partial w_r\partial w_s}=\int\frac{\partial y}{\partial w_r}\frac{\partial y}{\partial w_s}p(\mathbf{x})\,d\mathbf{x}.
\tag{5.194}
$$

注意，对于从 $p(\mathbf{x})$ 中抽取的有限样本，会得到（5.84）。

**5.18（⋆）** 考虑一个形式如图 5.1 所示的两层网络，并额外加入从输入直接连到输出的跳层连接所对应的参数。扩展 5.3.2 节的讨论，写出误差函数关于这些新增参数的导数方程。

**5.19（⋆）www** 对于只有一个输出、输出单元采用 logistic sigmoid 激活函数并使用交叉熵误差函数的网络，推导 Hessian 矩阵外积近似的表达式（5.85）；它对应于平方和误差函数的结果（5.84）。

<!-- pdf-page: 307 -->

**5.20（⋆）** 对于具有 $K$ 个输出、输出单元采用 softmax 激活函数并使用交叉熵误差函数的网络，推导 Hessian 矩阵外积近似的表达式；它对应于平方和误差函数的结果（5.84）。

**5.21（⋆⋆⋆）** 将 Hessian 矩阵外积近似的表达式（5.86）扩展到具有 $K>1$ 个输出单元的情况。由此，推导一个类似于（5.87）的递推表达式，用于增加模式数 $N$，再推导一个类似表达式，用于增加输出数 $K$。结合这些结果和恒等式（5.88），求出类似于（5.89）的顺序更新表达式，以便通过逐步加入新的模式和新的输出，求得 Hessian 矩阵的逆。

**5.22（⋆⋆）** 应用微分的链式法则，推导两层前馈网络的 Hessian 矩阵元素的结果（5.93）、（5.94）和（5.95）。

**5.23（⋆⋆）** 扩展 5.4.5 节中两层网络的精确 Hessian 矩阵的结果，使其包含从输入直接连到输出的跳层连接。

**5.24（⋆）** 验证：只要同时按照（5.116）和（5.117）变换权重和偏置，由（5.113）和（5.114）定义的网络函数，在输入受到变换（5.115）后就保持不变。类似地，证明：对第二层的权重和偏置应用变换（5.119）和（5.120），可以使网络输出按照（5.118）变换。

**5.25（⋆⋆⋆）www** 考虑如下形式的二次误差函数：

$$
E=E_0+\frac{1}{2}(\mathbf{w}-\mathbf{w}^{\star})^{\mathrm T}\mathbf{H}(\mathbf{w}-\mathbf{w}^{\star})
\tag{5.195}
$$

其中 $\mathbf{w}^{\star}$ 表示极小值点，Hessian 矩阵 $\mathbf{H}$ 正定且保持不变。假设初始权重向量 $\mathbf{w}^{(0)}$ 选在原点，并通过简单梯度下降更新：

$$
\mathbf{w}^{(\tau)}=\mathbf{w}^{(\tau-1)}-\rho\nabla E
\tag{5.196}
$$

其中 $\tau$ 表示步数，$\rho$ 是学习率，假设它很小。证明，经过 $\tau$ 步后，权重向量沿 $\mathbf{H}$ 的各特征向量方向的分量可以写为

$$
w_j^{(\tau)}=\{1-(1-\rho\eta_j)^{\tau}\}w_j^{\star}
\tag{5.197}
$$

其中 $w_j=\mathbf{w}^{\mathrm T}\mathbf{u}_j$，$\mathbf{u}_j$ 和 $\eta_j$ 分别是 $\mathbf{H}$ 的特征向量和特征值，即

$$
\mathbf{H}\mathbf{u}_j=\eta_j\mathbf{u}_j.
\tag{5.198}
$$

证明，只要 $|1-\rho\eta_j|<1$，当 $\tau\to\infty$ 时，就会如预期一样得到 $\mathbf{w}^{(\tau)}\to\mathbf{w}^{\star}$。现在假设训练在有限步数 $\tau$ 后停止。证明

<!-- pdf-page: 308 -->

<!-- join-previous-paragraph -->
权重向量沿 Hessian 矩阵各特征向量方向的分量满足

$$
w_j^{(\tau)}\simeq w_j^{\star}\qquad\text{当}\quad\eta_j\gg(\rho\tau)^{-1}
\tag{5.199}
$$

$$
|w_j^{(\tau)}|\ll|w_j^{\star}|\qquad\text{当}\quad\eta_j\ll(\rho\tau)^{-1}.
\tag{5.200}
$$

将这个结果与 3.5.3 节关于简单权重衰减正则化的讨论进行比较，从而说明 $(\rho\tau)^{-1}$ 类似于正则化参数 $\lambda$。上述结果还表明，由（3.91）定义的网络有效参数数目会随训练过程推进而增加。

**5.26（⋆⋆）** 考虑一个具有任意前馈拓扑结构的多层感知机，通过最小化切向传播误差函数（5.127）来训练，其中正则化函数由（5.128）给出。证明，正则化项 $\Omega$ 可以写成对各个模式的如下形式的项求和：

$$
\Omega_n=\frac{1}{2}\sum_k(\mathcal{G}y_k)^2
\tag{5.201}
$$

其中 $\mathcal{G}$ 是一个微分算子，定义为

$$
\mathcal{G}\equiv\sum_i\tau_i\frac{\partial}{\partial x_i}.
\tag{5.202}
$$

将算子 $\mathcal{G}$ 作用于前向传播方程

$$
z_j=h(a_j),\qquad a_j=\sum_i w_{ji}z_i
\tag{5.203}
$$

证明，可以利用下列方程，通过前向传播来计算 $\Omega_n$：

$$
\alpha_j=h'(a_j)\beta_j,\qquad\beta_j=\sum_i w_{ji}\alpha_i.
\tag{5.204}
$$

其中定义了新变量

$$
\alpha_j\equiv\mathcal{G}z_j,\qquad\beta_j\equiv\mathcal{G}a_j.
\tag{5.205}
$$

现在证明，$\Omega_n$ 关于网络中权重 $w_{rs}$ 的导数可以写成如下形式：

$$
\frac{\partial\Omega_n}{\partial w_{rs}}=\sum_k\alpha_k\{\phi_{kr}z_s+\delta_{kr}\alpha_s\}
\tag{5.206}
$$

其中定义了

$$
\delta_{kr}\equiv\frac{\partial y_k}{\partial a_r},\qquad\phi_{kr}\equiv\mathcal{G}\delta_{kr}.
\tag{5.207}
$$

写出 $\delta_{kr}$ 的反向传播方程，并由此推导一组用于计算 $\phi_{kr}$ 的反向传播方程。

<!-- pdf-page: 309 -->

**5.27（⋆⋆）www** 考虑使用变换后的数据进行训练的框架中的一个特殊情况：变换仅仅是加入随机噪声 $\mathbf{x}\to\mathbf{x}+\boldsymbol{\xi}$，其中 $\boldsymbol{\xi}$ 服从均值为零、协方差为单位矩阵的高斯分布。按照与 5.5.5 节类似的论证，证明所得的正则化项会化为 Tikhonov 形式（5.135）。

**5.28（⋆）www** 考虑一个神经网络，其中多个权重被约束为具有相同的值，例如 5.5.6 节讨论的卷积网络。讨论如何修改标准反向传播算法，以保证在计算误差函数关于网络可调参数的导数时满足这些约束。

**5.29（⋆）www** 验证结果（5.141）。

**5.30（⋆）** 验证结果（5.142）。

**5.31（⋆）** 验证结果（5.143）。

**5.32（⋆⋆）** 证明，由（5.146）定义的混合系数 $\{\pi_k\}$ 关于辅助参数 $\{\eta_j\}$ 的导数为

$$
\frac{\partial\pi_k}{\partial\eta_j}=\delta_{jk}\pi_j-\pi_j\pi_k.
\tag{5.208}
$$

由此，利用约束 $\sum_k\pi_k=1$，推导结果（5.147）。

**5.33（⋆）** 对于图 5.18 所示的机械臂，写出两个方程，用关节角 $\theta_1$、$\theta_2$ 和连杆长度 $L_1$、$L_2$ 表示笛卡尔坐标 $(x_1,x_2)$。假设坐标系原点位于下部连杆的固定连接点。这些方程定义了该机械臂的“正运动学”。

**5.34（⋆）www** 对于混合密度网络，推导误差函数关于控制混合系数的网络输出激活值的导数结果（5.155）。

**5.35（⋆）** 对于混合密度网络，推导误差函数关于控制分量均值的网络输出激活值的导数结果（5.156）。

**5.36（⋆）** 对于混合密度网络，推导误差函数关于控制分量方差的网络输出激活值的导数结果（5.157）。

**5.37（⋆）** 验证混合密度网络模型的条件均值和方差的结果（5.158）和（5.160）。

**5.38（⋆）** 利用一般结果（2.115），推导贝叶斯神经网络模型采用拉普拉斯近似时的预测分布（5.172）。

<!-- pdf-page: 310 -->

**5.39（⋆）www** 利用拉普拉斯近似的结果（4.135），证明贝叶斯神经网络模型中超参数 $\alpha$ 和 $\beta$ 的证据函数可以用（5.175）近似。

**5.40（⋆）www** 概述需要如何修改 5.7.3 节讨论的贝叶斯神经网络框架，才能使用输出单元具有 softmax 激活函数的网络来处理多类问题。

**5.41（⋆⋆）** 按照与 5.7.1 节针对回归网络所给出步骤类似的过程，对于采用交叉熵误差函数和 logistic sigmoid 输出单元激活函数的网络，推导边缘似然的结果（5.183）。
