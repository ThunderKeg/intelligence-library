<!-- Chapter 4 figure fragments for the chapter owner to integrate at their original locations. Author checked each original PDF page and existing source crop; independent chapter review is still required. This file is not a reader chapter. -->

<!-- Figure 4.1; original PDF page 149, printed page 135; crop 193,119,381,282. -->
<figure id="fig-4-1" data-figure="4.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-1.png" alt="目标函数的上图与其中最低的点，横轴为 x，纵轴为 t" data-source-page="149" data-source-rect="193,119,381,282">
<figcaption>图 4.1 无约束问题改写为上图形式后的几何解释。问题是在上图（阴影区域）中找出使 $t$ 最小的点，也就是上图中“最低”的点。最优点为 $(x^\star,t^\star)$。</figcaption>
<p class="figure-translation">图内文字：$\operatorname{epi}f_0$ 表示 $f_0$ 的上图。</p>
</figure>

<!-- Figure 4.2; original PDF page 153, printed page 139; crop 200,121,379,251. -->
<figure id="fig-4-2" data-figure="4.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-2.png" alt="阴影可行集、目标函数的虚线等值线，以及最优点处的支撑超平面和负梯度箭头" data-source-page="153" data-source-rect="200,121,379,251">
<figcaption>图 4.2 最优性条件 (4.21) 的几何解释。可行集 $X$ 用阴影表示，$f_0$ 的若干条等值线用虚线表示。点 $x$ 是最优点：$-\nabla f_0(x)$ 确定了 $X$ 在 $x$ 处的一条支撑超平面（图中的实线）。</figcaption>
</figure>

<!-- Figure 4.3; original PDF page 159, printed page 145; crop 193,122,377,250. -->
<figure id="fig-4-3" data-figure="4.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-3.png" alt="一维拟凸函数的曲线，在高于全局最低点的水平段上标出一个局部最优点" data-source-page="159" data-source-rect="193,122,377,250">
<figcaption>图 4.3 $\mathbf{R}$ 上的一个拟凸函数 $f$，其中 $x$ 是局部最优点，却不是全局最优点。这个例子说明，对凸函数成立的简单最优性条件 $f'(x)=0$ 并不适用于拟凸函数。</figcaption>
</figure>

<!-- Figure 4.4; original PDF page 161, printed page 147; crop 193,121,379,253. -->
<figure id="fig-4-4" data-figure="4.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-4.png" alt="多面体可行集与线性目标函数的平行等值线，最优点位于负 c 方向最远的顶点" data-source-page="161" data-source-rect="193,121,379,253">
<figcaption>图 4.4 线性规划（LP）的几何解释。可行集 $\mathcal{P}$ 是一个多面体，用阴影表示。目标函数 $c^Tx$ 是线性的，因此它的等值线是与 $c$ 正交的超平面（图中的虚线）。点 $x^\star$ 是最优点；它是 $\mathcal{P}$ 中沿 $-c$ 方向最远的点。</figcaption>
</figure>

<!-- Figure 4.5; original PDF page 167, printed page 153; crop 192,122,380,288. -->
<figure id="fig-4-5" data-figure="4.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-5.png" alt="多面体可行集与凸二次目标函数的等值线，最优点位于多面体边界上" data-source-page="167" data-source-rect="192,122,380,288">
<figcaption>图 4.5 二次规划（QP）的几何示意。可行集 $\mathcal{P}$ 是一个多面体，用阴影表示。目标函数是凸二次函数，其等值线用虚线表示。点 $x^\star$ 是最优点。</figcaption>
</figure>

<!-- Figure 4.6; original PDF page 178, printed page 164; crop 211,116,463,208. All four segment labels and the force arrow remain in the source image. -->
<figure id="fig-4-6" data-figure="4.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-6.png" alt="由四段组成的悬臂梁，左端固定，右端受到竖直向下的力 F" data-source-page="178" data-source-rect="211,116,463,208">
<figcaption>图 4.6 由 4 段组成的分段悬臂梁。每段的长度均为 1，截面为矩形。梁的右端施加竖直力 $F$。</figcaption>
<p class="figure-translation">图内文字：从左到右，segment 4：第 4 段；segment 3：第 3 段；segment 2：第 2 段；segment 1：第 1 段。</p>
</figure>

<!-- Figure 4.7; original PDF page 190, printed page 176; crop 238,121,401,267. -->
<figure id="fig-4-7" data-figure="4.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-7.png" alt="可达目标值集合及其左下端的最优值，浅色区域表示劣于或等于该最优值的目标值" data-source-page="190" data-source-rect="238,121,401,267">
<figcaption>图 4.7 阴影区域表示一个向量优化问题的可达目标值集合 $\mathcal{O}$；该问题的目标值属于 $\mathbf{R}^2$，所用的锥为 $K=\mathbf{R}_+^2$。在这个例子中，标为 $f_0(x^\star)$ 的点是问题的最优值，而 $x^\star$ 是最优点。目标值 $f_0(x^\star)$ 可以与每个其他可达目标值 $f_0(y)$ 比较，并且优于或等于 $f_0(y)$。（这里，“优于或等于”是指“位于其左下方，允许落在边界上”。）浅色阴影区域是 $f_0(x^\star)+K$，即所有劣于或等于 $f_0(x^\star)$ 的目标值 $z\in\mathbf{R}^2$ 构成的集合。</figcaption>
</figure>

<!-- Figure 4.8; original PDF page 192, printed page 178; crop 238,123,439,267. The superscript po is the original mathematical label for Pareto optimal. -->
<figure id="fig-4-8" data-figure="4.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-8.png" alt="可达目标值集合的 Pareto 最优边界，以及一个 Pareto 最优值左下方的浅色区域" data-source-page="192" data-source-rect="238,123,439,267">
<figcaption>图 4.8 阴影区域表示一个向量优化问题的可达目标值集合 $\mathcal{O}$；该问题的目标值属于 $\mathbf{R}^2$，所用的锥为 $K=\mathbf{R}_+^2$。这个问题没有最优点或最优值，但存在一组 Pareto 最优点，它们对应的目标值用 $\mathcal{O}$ 左下边界上加粗的曲线表示。标为 $f_0(x^{\mathrm{po}})$ 的点是一个 Pareto 最优值，而 $x^{\mathrm{po}}$ 是一个 Pareto 最优点。浅色阴影区域是 $f_0(x^{\mathrm{po}})-K$，即所有优于或等于 $f_0(x^{\mathrm{po}})$ 的目标值 $z\in\mathbf{R}^2$ 构成的集合。</figcaption>
</figure>

<!-- Figure 4.9; original PDF page 193, printed page 179; crop 184,121,393,282. -->
<figure id="fig-4-9" data-figure="4.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-9.png" alt="可达目标值集合上的三个 Pareto 最优值，其中两个可通过图示权重的标量化得到" data-source-page="193" data-source-rect="184,121,393,282">
<figcaption>图 4.9 标量化。图中显示了锥为 $K=\mathbf{R}_+^2$ 的向量优化问题的可达目标值集合 $\mathcal{O}$，以及三个 Pareto 最优值 $f_0(x_1)$、$f_0(x_2)$、$f_0(x_3)$。前两个值可以通过标量化得到：$f_0(x_1)$ 使 $\lambda_1^Tu$ 在所有 $u\in\mathcal{O}$ 上达到最小值，$f_0(x_2)$ 使 $\lambda_2^Tu$ 达到最小值，其中 $\lambda_1,\lambda_2\succ0$。值 $f_0(x_3)$ 是 Pareto 最优的，但无法通过标量化求得。</figcaption>
</figure>

<!-- Figure 4.10; original PDF page 195, printed page 181; crop 193,115,383,265. Minimal means minimal in the set-inclusion order, not minimum volume. -->
<figure id="fig-4-10" data-figure="4.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-10.png" alt="三个阴影椭球，以及两个分别以 X₁、X₂ 标记边界、包含这三个椭球的极小椭球" data-source-page="195" data-source-rect="193,115,383,265">
<figcaption>图 4.10 问题 (4.63) 的几何解释。三个阴影椭球对应于数据 $A_1,A_2,A_3\in\mathbf{S}_{++}^2$；Pareto 最优点对应于包含它们的极小椭球。边界分别标为 $X_1$ 和 $X_2$ 的两个椭球，是用两个不同的权重矩阵 $W_1$ 和 $W_2$ 求解半正定规划（SDP）(4.64) 得到的两个极小椭球。</figcaption>
</figure>

<!-- Figure 4.11; original PDF page 199, printed page 185; crop 161,121,397,309.5. The close bottom boundary preserves the complete horizontal-axis formula and excludes the source caption. -->
<figure id="fig-4-11" data-figure="4.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-11.png" alt="正则化最小二乘问题的可达目标值集合，其左下边界的粗线为最优权衡曲线" data-source-page="199" data-source-rect="161,121,397,309.5">
<figcaption>图 4.11 正则化最小二乘问题的最优权衡曲线。阴影集合是可达目标值 $(\|Ax-b\|_2^2,\|x\|_2^2)$ 的集合。最优权衡曲线是边界的左下部分，用较深的线条表示。</figcaption>
</figure>

<!-- Figure 4.12; original PDF page 201, printed page 187; crop 162,189,395,548. Both original subfigures remain in one image. The labels x(1), ..., x(4) use parentheses in the original, not subscripts. -->
<figure id="fig-4-12" data-figure="4.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/fig-4-12.png" alt="上图为投资组合的风险与收益率权衡曲线，下图为四种资产随风险变化的最优配置比例" data-source-page="201" data-source-rect="162,189,395,548">
<figcaption>图 4.12 上：一个简单投资组合优化问题中，风险与收益率的最优权衡曲线。左端点对应于将全部资金投入无风险资产，因此收益率的标准差为零。右端点对应于将全部资金投入平均收益率最高的资产 1。下：相应的最优资产配置。</figcaption>
<p class="figure-translation">图内文字：上图纵轴 mean return：平均收益率；下图纵轴 allocation：配置比例；下图横轴 standard deviation of return：收益率的标准差。下图中的 $x(4)$、$x(3)$、$x(2)$、$x(1)$ 分别表示资产 4、3、2、1 的配置比例。</p>
</figure>

<!-- Exercise 4.65, unnumbered power-flow diagram; original PDF page 226, printed page 212; crop 229,358,462,459. Place after the paragraph defining positive engine/brake/required wheel power and negative required wheel power during deceleration or descent. The source has no standalone caption; the surrounding explanatory paragraph belongs to the exercise body. -->
<figure id="exercise-4-65" data-uncaptioned="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-04/exercise-4-65.png" alt="混合动力汽车的功率流向图，包含发动机、制动器、电动机／发电机、蓄电池和车轮，以及各功率的正方向箭头" data-source-page="226" data-source-rect="229,358,462,459">
<p class="figure-translation">图内文字：Engine：发动机；Brake：制动器；wheels：车轮；Motor/generator：电动机／发电机；Battery：蓄电池。</p>
</figure>
