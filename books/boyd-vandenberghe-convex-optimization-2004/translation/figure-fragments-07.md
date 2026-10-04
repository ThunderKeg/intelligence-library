<!-- Chapter 7 figure fragments for the chapter owner to integrate at their original locations. Each original PDF page and existing crop is checked by the caption translator; independent chapter review is still required. This is not a reader chapter. -->

<!-- Figure 7.1; original PDF page 369, printed page 355; crop 160,122,395,303.5. -->
<figure id="fig-7-1" data-figure="7.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-1.png" alt="logistic 回归示意图：圆圈分布在结果为零和一的两排，实线概率曲线随解释变量 u 增大而从接近零上升到接近一" data-source-page="369" data-source-rect="160,122,395,303.5">
<figcaption>图 7.1 <em>logistic 回归。</em>圆圈表示 50 个点 $(u_i,y_i)$，其中 $u_i\in\mathbf{R}$ 是解释变量，$y_i\in\{0,1\}$ 是结果。数据表明，当 $u$ 大致小于 5 时，结果更可能是 $y=0$；当 $u$ 大致大于 5 时，结果更可能是 $y=1$。数据还表明，当 $u$ 大致小于 2 时，结果以很高的概率为 $y=0$；当 $u$ 大致大于 8 时，结果以很高的概率为 $y=1$。实线曲线表示取最大似然参数 $a,b$ 时的 $\mathbf{prob}(y=1)=\exp(au+b)/(1+\exp(au+b))$。这个最大似然模型与我们对数据集的直观观察一致。</figcaption>
</figure>

<!-- Figure 7.2; original PDF page 377, printed page 363; crop 154,122,394,303. -->
<figure id="fig-7-2" data-figure="7.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-2.png" alt="满足给定约束的最大熵离散分布，横轴为各取值 αᵢ，纵轴为相应概率 pᵢ；阶梯曲线先下降，再上升后略微回落" data-source-page="377" data-source-rect="154,122,394,303">
<figcaption>图 7.2 满足约束 (7.8) 的最大熵分布。</figcaption>
</figure>

<!-- Figure 7.3; original PDF page 378, printed page 364; crop 211,122,448,304. -->
<figure id="fig-7-3" data-figure="7.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-3.png" alt="三条累积分布阶梯曲线：上、下两条为给定约束下累积概率的最大值和最小值，中间一条为最大熵分布的累积分布函数" data-source-page="378" data-source-rect="211,122,448,304">
<figcaption>图 7.3 在所有满足 (7.8) 的分布中，最上方和最下方的曲线分别给出累积分布函数 $\mathbf{prob}(X\leq\alpha_i)$ 的最大可能值和最小可能值。中间的曲线是满足 (7.8) 的最大熵分布的累积分布函数。</figcaption>
</figure>

<!-- Figure 7.4; original PDF page 385, printed page 371; crop 160,121,391,303.5. -->
<figure id="fig-7-4" data-figure="7.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-4.png" alt="假阴性概率与假阳性概率之间的最优权衡折线；三个顶点标为一至三，折线与两种错误概率相等的斜虚线相交于标为四的点" data-source-page="385" data-source-rect="160,121,391,303.5">
<figcaption>图 7.4 对于 (7.15) 给出的矩阵 $P$，假阴性概率与检验结果为假阳性的概率之间的最优权衡曲线。曲线上标为 1–3 的顶点对应确定性检测器；标为 4 的点对应极小极大检测器，这是一个随机化检测器。虚线表示 $P_{\mathrm{fn}}=P_{\mathrm{fp}}$，即两种错误概率相等的点。</figcaption>
</figure>

<!-- Figure 7.5; original PDF page 396, printed page 382; crop 246,121,430,307. -->
<figure id="fig-7-5" data-figure="7.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-5.png" alt="由七个信号点组成的二维星座；小空心圆表示各信号，实线表示 Voronoi 区域边界，每个信号周围还有一个表示尺度的点状圆" data-source-page="396" data-source-rect="246,121,430,307">
<figcaption>图 7.5 由 7 个信号 $s_1,\ldots,s_7\in\mathbf{R}^2$ 组成的星座，信号以小圆圈表示。线段表示相应 Voronoi 区域的边界。当接收信号比起其他任何点都更接近 $s_k$ 时，即接收信号位于符号 $s_k$ 周围的 Voronoi 区域内部时，最小距离检测器选择符号 $s_k$。各点周围的圆的半径为 1，用于表示尺度。</figcaption>
</figure>

<!-- Figure 7.6; original PDF page 397, printed page 383; crop 160,134,397,315. -->
<figure id="fig-7-6" data-figure="7.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-6.png" alt="符号一、二、三的正确检测概率的三条 Chebyshev 下界曲线，均随噪声标准差 σ 增大而下降到零" data-source-page="397" data-source-rect="160,134,397,315">
<figcaption>图 7.6 符号 $s_1$、$s_2$ 和 $s_3$ 的正确检测概率的 Chebyshev 下界。这些界对任何均值为零、协方差为 $\sigma^2I$ 的噪声分布都有效。</figcaption>
<p class="figure-translation">图内文字：probability of correct detection——正确检测的概率。</p>
</figure>

<!-- Figure 7.7; original PDF page 397, printed page 383; crop 193,396,376,580. -->
<figure id="fig-7-7" data-figure="7.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-7.png" alt="七个信号点的 Voronoi 图中加入一个椭圆及六个实心点；五点位于椭圆边界，一点位于椭圆中心，中心实心点与符号 s₁ 的空心圆不同" data-source-page="397" data-source-rect="193,396,376,580">
<figcaption>图 7.7 当 $\sigma=1$ 时，正确检测符号 1 的概率的 Chebyshev 下界等于 0.2048。图中所示的离散分布达到了这个界。实心圆表示接收信号 $s_1+v$ 的可能取值。椭圆中心的点具有概率 0.2048，边界上五个点的概率之和为 0.7952。椭圆由 $x^TPx+2q^Tx+r=1$ 定义，其中 $P$、$q$ 和 $r$ 是 SDP (7.19) 的最优解。</figcaption>
</figure>

<!-- Figure 7.8; original PDF page 398, printed page 384; crop 209,122,452,306. -->
<figure id="fig-7-8" data-figure="7.8">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-8.png" alt="正确检测符号 s₁ 的概率随噪声标准差 σ 变化；Chernoff 下界为实线，Monte Carlo 估计为虚线，虚线始终位于实线上方或与其接近重合" data-source-page="398" data-source-rect="209,122,452,306">
<figcaption>图 7.8 正确检测符号 $s_1$ 的概率的 Chernoff 下界（实线）和 Monte Carlo 估计（虚线），作为 $\sigma$ 的函数。本例中，噪声服从均值为零、协方差为 $\sigma^2I$ 的高斯分布。</figcaption>
<p class="figure-translation">图内文字：probability of correct detection——正确检测的概率。</p>
</figure>

<!-- Figure 7.9; original PDF page 403, printed page 389; crop 159,120,394,235. -->
<figure id="fig-7-9" data-figure="7.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-9.png" alt="D 最优实验设计在二十个候选测量向量中选择两个，以实心圆标出且权重均为零点五；虚线椭圆以十字标出的原点为中心，并包含全部候选点" data-source-page="403" data-source-rect="159,120,394,235">
<figcaption>图 7.9 实验设计示例。20 个候选测量向量以圆圈表示。$D$ 最优设计使用实心圆所示的两个测量向量，并给它们分别赋予相同的权重 $\lambda_i=0.5$。图中的椭球是以原点为中心、包含所有点 $v_i$ 的最小体积椭球。</figcaption>
</figure>

<!-- Figure 7.10; original PDF page 403, printed page 389; crop 175,329,394,461. -->
<figure id="fig-7-10" data-figure="7.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-10.png" alt="E 最优实验设计选用两个实心圆所示的测量向量，权重分别为零点二和零点八；两条斜虚线表示相应椭球边界的一部分，十字标示原点" data-source-page="403" data-source-rect="175,329,394,461">
<figcaption>图 7.10 $E$ 最优设计使用两个测量向量。虚线是椭球 $\{x\mid x^TW^\star x\leq1\}$ 边界的一部分，其中 $W^\star$ 是对偶问题 (7.30) 的解。</figcaption>
</figure>

<!-- Figure 7.11; original PDF page 403, printed page 389; crop 171,529,394,628. -->
<figure id="fig-7-11" data-figure="7.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-11.png" alt="A 最优实验设计选用三个实心圆所示的测量向量，权重分别为零点三零、零点三八和零点三二；虚线椭圆表示与对偶解相关的椭球，十字标示原点" data-source-page="403" data-source-rect="171,529,394,628">
<figcaption>图 7.11 $A$ 最优设计使用三个测量向量。虚线表示与对偶问题 (7.31) 的解对应的椭球 $\{x\mid x^TW^\star x\leq1\}$。</figcaption>
</figure>

<!-- Figure 7.12; original PDF page 404, printed page 390; crop 247,122,442,291. -->
<figure id="fig-7-12" data-figure="7.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-07/fig-7-12.png" alt="D、A、E 最优设计与均匀设计的四个置信椭球；三个实线椭圆较窄，均匀设计对应一个方向不同、范围较大的虚线椭圆" data-source-page="404" data-source-rect="247,122,442,291">
<figcaption>图 7.12 $D$ 最优、$A$ 最优、$E$ 最优设计和均匀设计对应的 90% 置信椭球的形状。</figcaption>
<p class="figure-translation">图内文字：uniform——均匀设计。</p>
</figure>
