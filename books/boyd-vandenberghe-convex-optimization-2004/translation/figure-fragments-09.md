<!-- Chapter 9 figure fragments for integration at their original source locations. Original PDF pages and existing crops checked by the caption translator; independent chapter review remains required. -->

<!-- Figure 9.1; original PDF page 479, printed page 465; crop 181,126,478,292. -->
<figure id="fig-9-1" data-figure="9.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-1.png" alt="沿方向 Δx 搜索时，函数曲线随步长 t 先下降后上升；两条虚线从 t=0 处出发，上方虚线在 t₀ 处与曲线相交。" data-source-page="479" data-source-rect="181,126,478,292">
<figcaption>图 9.1 回溯直线搜索。曲线表示函数 $f$ 限制在搜索直线上时的取值。下方虚线表示 $f$ 的线性外推，上方虚线的斜率是下方虚线斜率的 $\alpha$ 倍。回溯条件要求 $f$ 不高于上方虚线，即 $0\leq t\leq t_0$。</figcaption>
</figure>

<!-- Figure 9.2; original PDF page 483, printed page 469; crop 148,122,413,246. -->
<figure id="fig-9-2" data-figure="9.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-2.png" alt="二次函数的虚线椭圆等值线中，梯度法的迭代点从 x⁽⁰⁾=(10,1) 出发，上下交替地向原点逼近；横轴为 x₁，纵轴为 x₂。" data-source-page="483" data-source-rect="148,122,413,246">
<figcaption>图 9.2 函数 $f(x)=(1/2)(x_1^2+10x_2^2)$ 的若干等值线。它的下水平集是椭球，条件数恰为 $10$。图中给出了采用精确直线搜索的梯度法从 $x^{(0)}=(10,1)$ 出发时的迭代点。</figcaption>
</figure>

<!-- Figure 9.3; original PDF page 485, printed page 471; crop 175,143,394,272. -->
<figure id="fig-9-3" data-figure="9.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-3.png" alt="虚线等值曲线内，梯度法从 x⁽⁰⁾ 出发，经过 x⁽¹⁾、x⁽²⁾ 等迭代点，沿往返折线逐渐逼近中心。" data-source-page="485" data-source-rect="175,143,394,272">
<figcaption>图 9.3 采用回溯直线搜索的梯度法的迭代点，所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。虚线是 $f$ 的等值线，小圆圈是梯度法的迭代点。连接相邻迭代点的实线表示缩放后的迭代步 $t^{(k)}\Delta x^{(k)}$。</figcaption>
</figure>

<!-- Figure 9.4; original PDF page 485, printed page 471; crop 148,400,394,586. -->
<figure id="fig-9-4" data-figure="9.4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-4.png" alt="梯度法的误差随迭代次数 k 下降，纵轴采用对数刻度；采用精确直线搜索的曲线比采用回溯直线搜索的曲线下降得更快。" data-source-page="485" data-source-rect="148,400,394,586">
<figcaption>图 9.4 采用回溯直线搜索和精确直线搜索的梯度法，其误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化；所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。图中表现出近似线性收敛：采用回溯直线搜索时，梯度法每次迭代后的误差约为前一次的 $0.4$ 倍；采用精确直线搜索时，每次迭代后的误差约为前一次的 $0.2$ 倍。</figcaption>
<p class="figure-translation">图内文字：backtracking l.s.——回溯直线搜索；exact l.s.——精确直线搜索。</p>
</figure>

<!-- Figure 9.5; original PDF page 486, printed page 472; crop 229,120,448,249. -->
<figure id="fig-9-5" data-figure="9.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-5.png" alt="采用精确直线搜索的梯度法从 x⁽⁰⁾ 到 x⁽¹⁾，再用几步到达虚线等值曲线的中心附近；空心圆表示迭代点，实线连接相邻点。" data-source-page="486" data-source-rect="229,120,448,249">
<figcaption>图 9.5 采用精确直线搜索的梯度法的迭代点，所求问题位于 $\mathbf{R}^2$ 中，目标函数 $f$ 由 (9.20) 给出。</figcaption>
</figure>

<!-- Figure 9.6; original PDF page 487, printed page 473; crop 148,122,416,306. -->
<figure id="fig-9-6" data-figure="9.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-6.png" alt="一百维问题中，采用回溯直线搜索和精确直线搜索的梯度法的误差随迭代次数 k 整体下降，两条曲线在后半段相交；纵轴为对数刻度。" data-source-page="487" data-source-rect="148,122,416,306">
<figcaption>图 9.6 对于 $\mathbf{R}^{100}$ 中的一个问题，采用回溯直线搜索和精确直线搜索的梯度法，其误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化。</figcaption>
<p class="figure-translation">图内文字：exact l.s.——精确直线搜索；backtracking l.s.——回溯直线搜索。</p>
</figure>

<!-- Figure 9.7; original PDF page 488, printed page 474; crop 213,164,448,348. -->
<figure id="fig-9-7" data-figure="9.7">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-7.png" alt="双对数坐标图中，梯度法所需迭代次数随对角缩放参数 γ 呈谷形变化，在 γ 接近 1 时较少，在两侧明显增加。" data-source-page="488" data-source-rect="213,164,448,348">
<figcaption>图 9.7 将梯度法用于问题 (9.22) 时的迭代次数。纵轴表示达到 $\bar f(\bar x^{(k)})-\bar p^\star<10^{-5}$ 所需的迭代次数。横轴表示控制对角缩放程度的参数 $\gamma$。这里使用回溯直线搜索，参数为 $\alpha=0.3$、$\beta=0.7$。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>

<!-- Figure 9.8; original PDF page 488, printed page 474; crop 211,412,448,596. -->
<figure id="fig-9-8" data-figure="9.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-8.png" alt="函数在最小值点处的 Hessian 矩阵条件数随 γ 变化，曲线在 γ 接近 1 时较低，在两侧升高；横纵轴都采用对数刻度。" data-source-page="488" data-source-rect="211,412,448,596">
<figcaption>图 9.8 函数在最小值点处的 Hessian 矩阵条件数随 $\gamma$ 的变化。将本图与图 9.7 比较，可以看出条件数对收敛速度有很强的影响。</figcaption>
</figure>

<!-- Figure 9.9; original PDF page 491, printed page 477; crop 211,121,393,276. -->
<figure id="fig-9-9" data-figure="9.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-9.png" alt="灰色椭圆表示平移后的二次范数单位球；从中心出发的负梯度箭头指向右上方，归一化最速下降箭头指向椭圆右下侧与支撑直线的接触点。" data-source-page="491" data-source-rect="211,121,393,276">
<figcaption>图 9.9 二次范数下的归一化最速下降方向。图中的椭球是该范数的单位球平移到点 $x$ 后得到的。点 $x$ 处的归一化最速下降方向 $\Delta x_{\mathrm{nsd}}$ 在保持端点位于椭球内的同时，使端点在 $-\nabla f(x)$ 方向上的投影尽可能远。图中画出了梯度方向和归一化最速下降方向。</figcaption>
</figure>

<!-- Figure 9.10; original PDF page 492, printed page 478; crop 265,121,447,281. -->
<figure id="fig-9-10" data-figure="9.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-10.png" alt="灰色菱形表示平移后的 ℓ₁ 范数单位球；负梯度箭头指向右上方，归一化最速下降箭头水平指向菱形最右侧的顶点。" data-source-page="492" data-source-rect="265,121,447,281">
<figcaption>图 9.10 $\ell_1$ 范数下的归一化最速下降方向。菱形是 $\ell_1$ 范数的单位球平移到点 $x$ 后得到的。归一化最速下降方向总可以选在某个标准基向量的方向上；本例中有 $\Delta x_{\mathrm{nsd}}=e_1$。</figcaption>
</figure>

<!-- Figure 9.11; original PDF page 495, printed page 481; crop 175,122,395,256. -->
<figure id="fig-9-11" data-figure="9.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-11.png" alt="采用 P₁ 二次范数的最速下降法迭代路径；x⁽⁰⁾ 和 x⁽¹⁾ 周围各有一个横向椭圆，虚线等值曲线内的迭代点经 x⁽²⁾ 向中心收敛。" data-source-page="495" data-source-rect="175,122,395,256">
<figcaption>图 9.11 采用二次范数 $\|\cdot\|_{P_1}$ 的最速下降法。图中的椭圆是分别以 $x^{(0)}$ 和 $x^{(1)}$ 为中心的范数球 $\{x\mid\|x-x^{(k)}\|_{P_1}\leq 1\}$ 的边界。</figcaption>
</figure>

<!-- Figure 9.12; original PDF page 496, printed page 482; crop 229,156,448,319. -->
<figure id="fig-9-12" data-figure="9.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-12.png" alt="采用 P₂ 二次范数的最速下降法迭代路径；x⁽⁰⁾ 和 x⁽¹⁾ 周围各有一个竖向椭圆，迭代点上下往返，逐渐靠近虚线等值曲线的中心。" data-source-page="496" data-source-rect="229,156,448,319">
<figcaption>图 9.12 采用二次范数 $\|\cdot\|_{P_2}$ 的最速下降法。</figcaption>
</figure>

<!-- Figure 9.13; original PDF page 496, printed page 482; crop 201,420,451,605. -->
<figure id="fig-9-13" data-figure="9.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-13.png" alt="最速下降法的误差随迭代次数 k 变化；纵轴采用对数刻度，P₁ 曲线在约 15 次迭代内降至 10⁻¹⁰，P₂ 曲线至 40 次迭代仍缓慢下降。" data-source-page="496" data-source-rect="201,420,451,605">
<figcaption>图 9.13 分别采用二次范数 $\|\cdot\|_{P_1}$ 和 $\|\cdot\|_{P_2}$ 时，最速下降法的误差 $f(x^{(k)})-p^\star$ 随迭代次数 $k$ 的变化。采用范数 $\|\cdot\|_{P_1}$ 时收敛很快，采用范数 $\|\cdot\|_{P_2}$ 时收敛则很慢。</figcaption>
</figure>

<!-- Figure 9.14; original PDF page 497, printed page 483; crop 211,222,359,400. -->
<figure id="fig-9-14" data-figure="9.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-14.png" alt="P₁ 范数最速下降法的迭代点经坐标变换后的图形；变换后的前两个迭代点旁画有圆形范数球，虚线等值曲线较为均匀，折线路径迅速接近中心。" data-source-page="497" data-source-rect="211,222,359,400">
<figcaption>图 9.14 采用范数 $\|\cdot\|_{P_1}$ 的最速下降法，其迭代点经坐标变换后的情形。这一坐标变换减小了下水平集的条件数，因此加快了收敛。</figcaption>
</figure>

<!-- Figure 9.15; original PDF page 497, printed page 483; crop 175,448,395,532. -->
<figure id="fig-9-15" data-figure="9.15" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-15.png" alt="P₂ 范数最速下降法的迭代点经坐标变换后的图形；前两个迭代点旁画有两个完整的圆，虚线等值曲线被横向拉长，迭代路径反复上下摆动。" data-source-page="497" data-source-rect="175,448,395,532">
<figcaption>图 9.15 采用范数 $\|\cdot\|_{P_2}$ 的最速下降法，其迭代点经坐标变换后的情形。这一坐标变换增大了下水平集的条件数，因此减慢了收敛。</figcaption>
</figure>

<!-- Figure 9.16; original PDF page 498, printed page 484; crop 227,121,431,249. -->
<figure id="fig-9-16" data-figure="9.16" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-16.png" alt="函数 f 的实线曲线与在 x 处相切的二阶近似虚线；虚线最低点和其正下方实际函数上的点具有相同横坐标 x+Δx_nt，两个点分别标出。" data-source-page="498" data-source-rect="227,121,431,249">
<figcaption>图 9.16 函数 $f$（实线）及其在点 $x$ 处的二阶近似 $\widehat f$（虚线）。将牛顿步 $\Delta x_{\mathrm{nt}}$ 加到 $x$ 上，就得到 $\widehat f$ 的最小值点。</figcaption>
</figure>

<!-- Figure 9.17; original PDF page 499, printed page 485; crop 229,122,342,300. -->
<figure id="fig-9-17" data-figure="9.17" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-17.png" alt="凸函数的虚线等值曲线和以 x 为中心的实线椭圆；负梯度箭头斜向右下方，归一化最速下降步的端点位于椭圆边界，牛顿步的端点位于椭圆外。" data-source-page="499" data-source-rect="229,122,342,300">
<figcaption>图 9.17 虚线是某个凸函数的等值线。实线所示的椭球为 $\{x+v\mid v^T\nabla^2 f(x)v\leq 1\}$。箭头表示 $-\nabla f(x)$，即梯度下降方向。牛顿步 $\Delta x_{\mathrm{nt}}$ 是范数 $\|\cdot\|_{\nabla^2 f(x)}$ 下的最速下降方向。图中还给出了 $\Delta x_{\mathrm{nsd}}$，即同一范数下的归一化最速下降方向。</figcaption>
</figure>

<!-- Figure 9.18; original PDF page 500, printed page 486; crop 247,122,449,253. -->
<figure id="fig-9-18" data-figure="9.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-18.png" alt="函数导数 f′ 的实线曲线与在 x 处的线性近似虚线；虚线在 x+Δx_nt 处穿过水平零线，该横坐标对应的实际导数值仍小于零。" data-source-page="500" data-source-rect="247,122,449,253">
<figcaption>图 9.18 实线曲线是图 9.16 中函数 $f$ 的导数 $f'$。$\widehat f'$ 是 $f'$ 在点 $x$ 处的线性近似。牛顿步 $\Delta x_{\mathrm{nt}}$ 等于 $\widehat f'$ 的根与点 $x$ 之差。</figcaption>
</figure>

<!-- Figure 9.19; original PDF page 506, printed page 492; crop 229,121,448,252. -->
<figure id="fig-9-19" data-figure="9.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-19.png" alt="二维问题中牛顿法的迭代路径；在 x⁽⁰⁾ 和 x⁽¹⁾ 处各画有一个倾斜椭圆，少量相连的迭代点迅速到达虚线等值曲线的中心附近。" data-source-page="506" data-source-rect="229,121,448,252">
<figcaption>图 9.19 将牛顿法用于 $\mathbf{R}^2$ 中的问题，目标函数 $f$ 由 (9.20) 给出，回溯直线搜索参数为 $\alpha=0.1$、$\beta=0.7$。图中还画出了前两个迭代点处的椭球 $\{x\mid\|x-x^{(k)}\|_{\nabla^2 f(x^{(k)})}\leq 1\}$。</figcaption>
</figure>

<!-- Figure 9.20; original PDF page 507, printed page 493; crop 148,142,394,326. -->
<figure id="fig-9-20" data-figure="9.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-20.png" alt="二维问题中牛顿法的误差随迭代次数 k 从 0 到 5 迅速下降；纵轴采用对数刻度，最后一次迭代后的误差低于 10⁻¹⁰。" data-source-page="507" data-source-rect="148,142,394,326">
<figcaption>图 9.20 对于 $\mathbf{R}^2$ 中的问题，牛顿法的误差随迭代次数 $k$ 的变化。经过 $5$ 次迭代就达到了很高的精度。</figcaption>
</figure>

<!-- Figure 9.21; original PDF page 507, printed page 493; crop 148,413,406,599. -->
<figure id="fig-9-21" data-figure="9.21">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-21.png" alt="一百维问题中牛顿法的两条误差曲线，纵轴采用对数刻度；菱形标记的精确直线搜索曲线在第 7 次迭代、圆圈标记的回溯直线搜索曲线在第 8 次迭代达到很小的误差。" data-source-page="507" data-source-rect="148,413,406,599">
<figcaption>图 9.21 对于 $\mathbf{R}^{100}$ 中的问题，牛顿法的误差随迭代次数的变化。回溯直线搜索参数为 $\alpha=0.01$、$\beta=0.5$。这里的收敛同样极快：仅需 $7$ 次或 $8$ 次迭代便达到了很高的精度。采用精确直线搜索时，牛顿法达到收敛所需的迭代次数仅比采用回溯直线搜索时少一次。</figcaption>
<p class="figure-translation">图内文字：backtracking l.s.——回溯直线搜索；exact l.s.——精确直线搜索。</p>
</figure>

<!-- Figure 9.22; original PDF page 508, printed page 494; crop 211,122,447,307. -->
<figure id="fig-9-22" data-figure="9.22">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-22.png" alt="牛顿法的步长随迭代次数 k 变化；回溯直线搜索前两次的步长为 0.5，此后为 1，精确直线搜索的步长先升至约 1.6，再逐渐接近 1。" data-source-page="508" data-source-rect="211,122,447,307">
<figcaption>图 9.22 将采用回溯直线搜索和精确直线搜索的牛顿法用于 $\mathbf{R}^{100}$ 中的问题时，步长 $t$ 随迭代次数的变化。回溯直线搜索在前两次迭代中各回溯一步。前两次迭代之后，它总是选择 $t=1$。</figcaption>
<p class="figure-translation">图内文字：step size $t^{(k)}$——步长 $t^{(k)}$；exact l.s.——精确直线搜索；backtracking l.s.——回溯直线搜索。</p>
</figure>

<!-- Figure 9.23; original PDF page 509, printed page 495; crop 150,122,398,306. -->
<figure id="fig-9-23" data-figure="9.23" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-23.png" alt="一万维问题中牛顿法的误差随迭代次数 k 下降，纵轴采用对数刻度；曲线在后几次迭代明显变陡，第 18 次迭代后的误差低于 10⁻⁵。" data-source-page="509" data-source-rect="150,122,398,306">
<figcaption>图 9.23 对于 $\mathbf{R}^{10000}$ 中的一个问题，牛顿法的误差随迭代次数的变化。这里使用回溯直线搜索，参数为 $\alpha=0.01$、$\beta=0.5$。即使对于这样的大规模问题，牛顿法也只需 $18$ 次迭代就能达到很高的精度。</figcaption>
</figure>

<!-- Figure 9.24; original PDF page 517, printed page 503; crop 185,121,375,274. -->
<figure id="fig-9-24" data-figure="9.24" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-24.png" alt="实线函数 −(λ+log(1−λ)) 与虚线 λ² 从原点出发；在 λ 不超过约 0.68 的区间，虚线位于实线上方，之后实线增长更快。" data-source-page="517" data-source-rect="185,121,375,274">
<figcaption>图 9.24 实线表示函数 $-(\lambda+\log(1-\lambda))$，当 $\lambda$ 较小时，它近似等于 $\lambda^2/2$。虚线表示 $\lambda^2$，在区间 $0\leq\lambda\leq 0.68$ 内，它是前者的上界。</figcaption>
</figure>

<!-- Figure 9.25; original PDF page 520, printed page 506; crop 225,122,440,291. -->
<figure id="fig-9-25" data-figure="9.25">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-09/fig-9-25.png" alt="散点图以初始目标值与最优值之差 f(x⁽⁰⁾)−p⋆ 为横轴，以牛顿迭代次数为纵轴；圆圈、方形和菱形分别表示三组不同维数的问题实例。" data-source-page="520" data-source-rect="225,122,440,291">
<figcaption>图 9.25 最小化自协调函数所需的牛顿迭代次数随 $f(x^{(0)})-p^\star$ 的变化。函数 $f$ 的形式为 $f(x)=-\sum_{i=1}^m\log(b_i-a_i^T x)$，其中问题数据 $a_i$ 和 $b$ 随机生成。圆圈表示 $m=100$、$n=50$ 的问题；方形表示 $m=1000$、$n=500$ 的问题；菱形表示 $m=1000$、$n=50$ 的问题。每组均给出了 $50$ 个实例。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>
