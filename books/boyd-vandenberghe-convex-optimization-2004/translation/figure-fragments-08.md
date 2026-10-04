<!-- Chapter 8 figure fragments for integration at their original source locations. Original PDF pages and existing crops checked by the caption translator; independent chapter review remains required. -->

<!-- Figure 8.1; original PDF page 414, printed page 400; crop 246,120,432,259. -->
<figure id="fig-8-1" data-figure="8.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-1.png" alt="点 x₀ 位于灰色凸集 C 外，虚线将它连接到集合边界上的欧几里得投影 P_C(x₀)，两点之间的斜直线垂直平分这条线段并将点与集合分开" data-source-page="414" data-source-rect="246,120,432,259">
<figcaption>图 8.1 点 $x_0$ 及其在凸集 $C$ 上的欧几里得投影 $P_C(x_0)$。位于这两点中间、法向量为 $P_C(x_0)-x_0$ 的超平面，将这个点与该集合严格分离。这一性质对一般范数并不成立；见习题 8.4。</figcaption>
</figure>

<!-- Figure 8.2; original PDF page 417, printed page 403; crop 192,120,379,229. -->
<figure id="fig-8-2" data-figure="8.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-2.png" alt="两个分离的灰色多边形 C 和 D，虚线连接各自边界上彼此最接近的两个点，表示两个集合的欧几里得距离" data-source-page="417" data-source-rect="192,120,379,229">
<figcaption>图 8.2 多面体 $C$ 与 $D$ 之间的欧几里得距离。虚线连接分别位于 $C$ 和 $D$ 中、按欧几里得范数衡量时彼此最接近的两个点。这两个点可以通过求解一个 QP 找到。</figcaption>
</figure>

<!-- Figure 8.3; original PDF page 426, printed page 412; crop 246,122,430,273. -->
<figure id="fig-8-3" data-figure="8.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-3.png" alt="六个实心点构成的多边形包含在外侧椭圆内；内侧灰色椭圆与外侧椭圆同心，缩小后完全位于多边形中" data-source-page="426" data-source-rect="246,122,430,273">
<figcaption>图 8.3 外侧椭圆是 Löwner-John 椭球的边界，即包含点 $x_1,\ldots,x_6$（以实心点表示）、从而也包含多面体 $\mathcal{P}=\mathbf{conv}\{x_1,\ldots,x_6\}$ 的最小体积椭球的边界。较小的椭圆是将 Löwner-John 椭球以其中心为基准缩小至原来的 $1/n$ 后的边界，这里 $n=2$。可以保证这个椭球位于 $\mathcal{P}$ 内。</figcaption>
</figure>

<!-- Figure 8.4; original PDF page 430, printed page 416; crop 246,121,431,273. -->
<figure id="fig-8-4" data-figure="8.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-4.png" alt="多边形中有一个灰色最大体积内接椭圆，将它以中心为基准放大两倍得到外侧椭圆，覆盖整个多边形" data-source-page="430" data-source-rect="246,121,431,273">
<figcaption>图 8.4 多面体 $\mathcal{P}$ 的最大体积内接椭球，以阴影表示。外侧椭圆是将内侧椭球以其中心为基准放大 $n=2$ 倍后的边界。可以保证放大后的椭球覆盖 $\mathcal{P}$。</figcaption>
</figure>

<!-- Figure 8.5; original PDF page 431, printed page 417; crop 192,121,378,276. -->
<figure id="fig-8-5" data-figure="8.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-5.png" alt="多边形中的最大内接欧几里得球以浅灰圆表示，圆心以小空心圆标出并标为 x_cheb" data-source-page="431" data-source-rect="192,121,378,276">
<figcaption>图 8.5 欧几里得范数下，多面体 $C$ 的 Chebyshev 中心。中心 $x_{\mathrm{cheb}}$ 是 $C$ 内部最深的点，意思是它到 $C$ 的外部（即补集）的距离最远。中心 $x_{\mathrm{cheb}}$ 也是包含在 $C$ 内的最大欧几里得球（浅色阴影区域）的球心。</figcaption>
</figure>

<!-- Figure 8.6; original PDF page 433, printed page 419; crop 192,121,378,276. -->
<figure id="fig-8-6" data-figure="8.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-6.png" alt="多边形内的最大体积椭球以浅灰椭圆表示，椭圆中心用小空心圆标出并标为 x_mve" data-source-page="433" data-source-rect="192,121,378,276">
<figcaption>图 8.6 浅色阴影椭球表示包含在集合 $C$ 内的最大体积椭球，$C$ 是图 8.5 中的同一个多面体。它的中心 $x_{\mathrm{mve}}$ 就是 $C$ 的最大体积椭球中心。</figcaption>
</figure>

<!-- Figure 8.7; original PDF page 435, printed page 421; crop 192,121,378,276. -->
<figure id="fig-8-7" data-figure="8.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-7.png" alt="同一多边形内部有五条虚线等值曲线，中央的灰色椭圆包围标为 x_ac 的解析中心" data-source-page="435" data-source-rect="192,121,378,276">
<figcaption>图 8.7 虚线表示定义图 8.5 中多面体 $C$ 的不等式所对应的对数障碍函数的五条等值曲线。标为 $x_{\mathrm{ac}}$ 的点是对数障碍函数的极小点，也就是这些不等式的解析中心。内侧椭球 $\mathcal{E}_{\mathrm{inner}}=\{x\mid(x-x_{\mathrm{ac}})H(x-x_{\mathrm{ac}})\leq1\}$ 以阴影表示，其中 $H$ 是对数障碍函数在 $x_{\mathrm{ac}}$ 处的 Hessian 矩阵。</figcaption>
</figure>

<!-- Figure 8.8; original PDF page 437, printed page 423; crop 201,120,370,303. -->
<figure id="fig-8-8" data-figure="8.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-8.png" alt="一条斜直线将左上方的实心点与右下方的空心点完全分开，表示仿射分类函数的零水平集" data-source-page="437" data-source-rect="201,120,370,303">
<figcaption>图 8.8 点 $x_1,\ldots,x_N$ 以空心圆表示，点 $y_1,\ldots,y_M$ 以实心圆表示。用一个仿射函数 $f$ 对这两个点集进行分类，其零水平集（一条直线）将两者分离。</figcaption>
</figure>

<!-- Figure 8.9; original PDF page 439, printed page 425; crop 200,119,370,308. -->
<figure id="fig-8-9" data-figure="8.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-9.png" alt="两条平行虚线之间的浅灰条带分离实心点与空心点，部分点恰位于条带边界，中央实线是分类边界" data-source-page="439" data-source-rect="200,119,370,308">
<figcaption>图 8.9 通过求解鲁棒线性判别问题 (8.23)，我们找到一个使两个点集的函数值间隔最大的仿射函数，同时对函数的线性部分施加归一化界限。从几何上看，我们在寻找能将这两个点集分开的最宽条带。</figcaption>
</figure>

<!-- Figure 8.10; original PDF page 440, printed page 426; crop 237,121,438,312. -->
<figure id="fig-8-10" data-figure="8.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-10.png" alt="空心点与实心点的散点图中画出一条实线分类边界及其两侧距离很近的平行虚线；存在被误分类的点和位于条带内的点" data-source-page="440" data-source-rect="237,121,438,312">
<figcaption>图 8.10 通过线性规划进行近似线性判别。以空心圆表示的点 $x_1,\ldots,x_{50}$，无法与以实心圆表示的点 $y_1,\ldots,y_{50}$ 线性分离。实线所示的分类器通过求解 LP (8.25) 得到。这个分类器将一个点分错了类。虚线表示超平面 $a^Tz-b=\pm1$。有四个点被正确分类，但落在两条虚线定义的条带内。</figcaption>
</figure>

<!-- Figure 8.11; original PDF page 441, printed page 427; crop 183,121,385,311. -->
<figure id="fig-8-11" data-figure="8.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-11.png" alt="支持向量分类器的实线边界位于两条平行虚线之间；空心点和实心点分布在其两侧，若干点位于较宽的条带内" data-source-page="441" data-source-rect="183,121,385,311">
<figcaption>图 8.11 通过支持向量分类器进行近似线性判别，其中 $\gamma=0.1$。实线所示的支持向量分类器将三个点分错了类。有十五个点被正确分类，但位于由 $-1<a^Tz-b<1$ 定义、以两条虚线为边界的条带内。</figcaption>
</figure>

<!-- Figure 8.12; original PDF page 443, printed page 429; crop 183,133,385,312. -->
<figure id="fig-8-12" data-figure="8.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-12.png" alt="logistic 模型给出的实线分类边界与两条平行虚线穿过两组散点之间，实心点与空心点并非完全线性可分" data-source-page="443" data-source-rect="183,133,385,312">
<figcaption>图 8.12 通过 logistic 建模进行近似线性判别。以空心圆表示的点 $x_1,\ldots,x_{50}$，无法与以实心圆表示的点 $y_1,\ldots,y_{50}$ 线性分离。最大似然 logistic 模型给出了图中以深色直线表示的超平面，它只将两个点分错了类。两条虚线表示 $a^Tu-b=\pm1$；根据 logistic 模型，两种结果在各自对应的线上具有 73% 的概率。有三个点被正确分类，但位于两条虚线之间。</figcaption>
</figure>

<!-- Figure 8.13; original PDF page 445, printed page 431; crop 184,146,385,312. -->
<figure id="fig-8-13" data-figure="8.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-13.png" alt="一个倾斜椭圆包围全部空心点，并将周围全部实心点排除在外，表示具有负定二次项的分类边界" data-source-page="445" data-source-rect="184,146,385,312">
<figcaption>图 8.13 带有条件 $P\prec0$ 的二次判别。这意味着要寻找一个包含所有 $x_i$（以空心圆表示）、却不包含任何 $y_i$（以实心圆表示）的椭球。这个问题可以作为一个 SDP 可行性问题来求解。</figcaption>
</figure>

<!-- Figure 8.14; original PDF page 445, printed page 431; crop 193,424,376,600. -->
<figure id="fig-8-14" data-figure="8.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-14.png" alt="一条右侧向内凹的闭合曲线将中央空心点与周围实心点分离，曲线是四次多项式的零水平集" data-source-page="445" data-source-rect="193,424,376,600">
<figcaption>图 8.14 $\mathbf{R}^2$ 中的最低次数多项式判别。本例中，不存在能将点 $x_1,\ldots,x_N$（以空心圆表示）与点 $y_1,\ldots,y_M$（以实心圆表示）分离的三次多项式，但可以用一个四次多项式将它们分离，图中画出了这个多项式的零水平集。</figcaption>
</figure>

<!-- Figure 8.15; original PDF page 449, printed page 435; crop 92,154,473,309.7. -->
<figure id="fig-8-15" data-figure="8.15" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-15.png" alt="左图用实心点表示六个自由点、方框表示八个固定点，虚点线表示连线；右图给出连线长度的直方图和一条上升的线性罚函数虚线" data-source-page="449" data-source-rect="92,154,473,309.7">
<figcaption>图 8.15 <em>线性布置。</em>一个包含 6 个自由点（以实心点表示）、8 个固定点（以方框表示）和 27 条连线的布置问题。自由点的坐标使各连线的欧几里得长度之和最小。右图给出了这 27 条连线长度的分布。虚线表示经缩放的罚函数 $h(z)=z$。</figcaption>
</figure>

<!-- Figure 8.16; original PDF page 449, printed page 435; crop 92,451,473,607.1. -->
<figure id="fig-8-16" data-figure="8.16" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-16.png" alt="左图给出自由点较为分散的二次布置及其与固定点之间的连线，右图给出连线长度直方图和二次罚函数虚线" data-source-page="449" data-source-rect="92,451,473,607.1">
<figcaption>图 8.16 <em>二次布置。</em>采用与图 8.15 相同的数据，使各连线的欧几里得长度平方和最小的布置。虚线表示经缩放的罚函数 $h(z)=z^2$。</figcaption>
</figure>

<!-- Figure 8.17; original PDF page 450, printed page 436; crop 146,112,527,265.5. -->
<figure id="fig-8-17" data-figure="8.17" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-17.png" alt="左图给出四次布置中的自由点、固定点和连线，右图给出连线长度直方图以及随长度增大而快速上升的四次罚函数虚线" data-source-page="450" data-source-rect="146,112,527,265.5">
<figcaption>图 8.17 <em>四次布置。</em>使各连线的欧几里得长度四次方之和最小的布置。虚线表示经缩放的罚函数 $h(z)=z^4$。</figcaption>
</figure>

<!-- Figure 8.18; original PDF page 453, printed page 439; crop 201,120,375,296.4. -->
<figure id="fig-8-18" data-figure="8.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-18.png" alt="宽 W、高 H 的大矩形中放置三个互不重叠的小矩形，单元 Cᵢ 标有宽 wᵢ、高 hᵢ 和左下角坐标 (xᵢ,yᵢ)" data-source-page="453" data-source-rect="201,120,375,296.4">
<figcaption>图 8.18 平面布局问题。在一个宽为 $W$、高为 $H$、左下角位于 $(0,0)$ 的矩形中，放置互不重叠的矩形单元。第 $i$ 个单元由其宽度 $w_i$、高度 $h_i$ 以及左下角坐标 $(x_i,y_i)$ 确定。</figcaption>
</figure>

<!-- Figure 8.19; original PDF page 455, printed page 441; crop 152,120,415,266. -->
<figure id="fig-8-19" data-figure="8.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-19.png" alt="左侧两个有向图 H 和 V 分别规定五个矩形单元的左右与上下关系，右侧给出满足这些关系的平面布局，单元以一至五编号" data-source-page="455" data-source-rect="152,120,415,266">
<figcaption>图 8.19 用水平图 $\mathcal{H}$ 和竖直图 $\mathcal{V}$ 规定各单元相对位置的示例。如果 $\mathcal{H}$ 中存在从节点 $i$ 到节点 $j$ 的路径，那么单元 $i$ 必须放在单元 $j$ 的左侧。如果 $\mathcal{V}$ 中存在从节点 $i$ 到节点 $j$ 的路径，那么单元 $i$ 必须放在单元 $j$ 的下方。右侧所示的平面布局满足这两个图规定的相对位置关系。</figcaption>
</figure>

<!-- Figure 8.20; original PDF page 458, printed page 444; crop 174,122,501,398. -->
<figure id="fig-8-20" data-figure="8.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/fig-8-20.png" alt="四个子图分别展示五个编号矩形单元的最优平面布局；相对位置相同，各单元的面积与形状随最小面积要求改变" data-source-page="458" data-source-rect="174,122,501,398">
<figcaption>图 8.20 采用图 8.19 所示相对位置约束的四个最优平面布局实例。每种情况下，目标都是最小化周长，并施加相同的单元间最小间距约束。还要求宽高比介于 $1/5$ 和 $5$ 之间。四种情况的区别在于对各单元最小面积的要求不同，但各单元最小面积之和在四种情况下都相同。</figcaption>
</figure>

<!-- Exercise 8.30 first unnumbered diagram; original PDF page 467, printed page 453; crop 221,321,350,436. No original independent caption or lettered subpart. -->
<figure id="fig-exercise-8-30-a" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/exercise-8-30-a.png" alt="相同端点 aᵢ 与 aᵢ₊₁ 之间的四条圆弧或线段，分别标注 θᵢ 等于零、π/4、π/2 和 3π/4，虚线表示端点处的切线方向" data-source-page="467" data-source-rect="221,321,350,436">
</figure>

<!-- Exercise 8.30 second unnumbered diagram; original PDF page 467, printed page 453; crop 155,532,408,607. No original independent caption or lettered subpart. -->
<figure id="fig-exercise-8-30-b" data-uncaptioned="true" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-08/exercise-8-30-b.png" alt="相邻两段圆弧在 aᵢ 处连接，图中标出端点 aᵢ₋₁、aᵢ、aᵢ₊₁、切线方向以及角 θᵢ₋₁、θᵢ、ψᵢ，虚线画出两段弦及其延长线" data-source-page="467" data-source-rect="155,532,408,607">
</figure>
