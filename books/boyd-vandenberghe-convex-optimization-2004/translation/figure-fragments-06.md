<!-- Chapter 6 figure fragments for the chapter owner to integrate at their original locations. Each original PDF page and existing crop is checked by the caption translator; independent chapter review is still required. This is not a reader chapter. -->

<!-- Figure 6.1; original PDF page 309, printed page 295; crop 159,121,440,307. -->
<figure id="fig-6-1" data-figure="6.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-1.png" alt="二次罚函数、死区线性罚函数和对数障碍罚函数的曲线比较；三条曲线关于纵轴对称，在原点附近的形状及远离原点时的增长速度不同" data-source-page="309" data-source-rect="159,121,440,307">
<figcaption>图 6.1 几种常见的罚函数：二次罚函数 $\phi(u)=u^2$、死区宽度为 $a=1/4$ 的死区线性罚函数，以及界限为 $a=1$ 的对数障碍罚函数。</figcaption>
<p class="figure-translation">图内文字：log barrier——对数障碍；quadratic——二次；deadzone-linear——死区线性。</p>
</figure>

<!-- Figure 6.2; original PDF page 311, printed page 297; crop 116,248,445,512. -->
<figure id="fig-6-2" data-figure="6.2">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-2.png" alt="四幅上下排列的残差直方图，分别对应 p=1、p=2、死区和对数障碍罚函数；各图叠加罚函数曲线，最下图另以虚线表示二次罚函数" data-source-page="311" data-source-rect="116,248,445,512">
<figcaption>图 6.2 采用四种罚函数时，残差取值的直方图。图中还画出了经缩放的罚函数，供对照。在对数障碍罚函数对应的图中，还用虚线画出了二次罚函数。</figcaption>
<p class="figure-translation">图内文字：Deadzone——死区；Log barrier——对数障碍。</p>
</figure>

<!-- Figure 6.3; original PDF page 312, printed page 298; crop 229,120,434,277. -->
<figure id="fig-6-3" data-figure="6.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-3.png" alt="在负一到一之间为二次曲线、两侧保持为一的非凸罚函数，横轴为 u，纵轴为罚函数值" data-source-page="312" data-source-rect="229,120,434,277">
<figcaption>图 6.3 一种（非凸）罚函数，对幅值超过某个阈值（本例中为 1）的残差施加固定惩罚：当 $|u|\leq1$ 时，$\phi(u)=u^2$；当 $|u|>1$ 时，$\phi(u)=1$。因此，采用这个函数进行罚函数逼近时，对离群点相对不敏感。</figcaption>
</figure>

<!-- Figure 6.4; original PDF page 313, printed page 299; crop 177,120,380,277. -->
<figure id="fig-6-4" data-figure="6.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-4.png" alt="Huber 罚函数的实线曲线，在中心区域为二次函数，两侧线性增长；两侧的直线段向中央以虚线延伸" data-source-page="313" data-source-rect="177,120,380,277">
<figcaption>图 6.4 实线表示 $M=1$ 时的鲁棒最小二乘罚函数，也称 Huber 罚函数 $\phi_{\mathrm{hub}}$。当 $|u|\leq M$ 时，它是二次函数；当 $|u|>M$ 时，它线性增长。</figcaption>
</figure>

<!-- Figure 6.5; original PDF page 314, printed page 300; crop 216,121,448,306. -->
<figure id="fig-6-5" data-figure="6.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-5.png" alt="四十二个圆圈表示数据点，左上和右下各有一个离群点；最小二乘拟合虚线偏向离群点，鲁棒最小二乘拟合实线更贴近其余数据点" data-source-page="314" data-source-rect="216,121,448,306">
<figcaption>图 6.5 42 个圆圈表示数据点；除了左上方和右下方的两个离群点外，这些点都可以用一个仿射函数很好地逼近。虚线是用直线 $f(t)=\alpha+\beta t$ 对这些点进行最小二乘拟合的结果，它偏离了大多数数据点所在的位置，转向了离群点。实线表示通过最小化 $M=1$ 时的 Huber 罚函数得到的鲁棒最小二乘拟合。这种拟合对非离群数据的效果好得多。</figcaption>
</figure>

<!-- Figure 6.6; original PDF page 323, printed page 309; crop 90,141,470,596. -->
<figure id="fig-6-6" data-figure="6.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-6.png" alt="三行两列的曲线图：左列为最优输入，右列为相应输出；每行对应一组正则化参数，右列的虚线为期望输出" data-source-page="323" data-source-rect="90,141,470,596">
<figcaption>图 6.6 正则化参数 $\delta$（对应输入变化）和 $\eta$（对应输入幅值）取三组值时的最优输入（左）及相应输出（右）。右侧各图中的虚线表示期望输出 $y_{\mathrm{des}}$。最上行为 $\delta=0,\ \eta=0.005$；中间行为 $\delta=0,\ \eta=0.05$；最下行为 $\delta=0.3,\ \eta=0.05$。</figcaption>
</figure>

<!-- Figure 6.7; original PDF page 325, printed page 311; crop 164,122,395,306.5. -->
<figure id="fig-6-7" data-figure="6.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-7.png" alt="稀疏回归变量选择中，非零元素个数随残差范数变化的两条阶梯曲线；虚线上的圆圈为 Pareto 最优值，实线上的圆圈为正则化启发式方法得到的点" data-source-page="325" data-source-rect="164,122,395,306.5">
<figcaption>图 6.7 矩阵 $A\in\mathbf{R}^{10\times20}$ 时的稀疏回归变量选择。虚线上的圆圈表示残差 $\|Ax-b\|_2$ 与非零元素个数 $\operatorname{card}(x)$ 之间权衡的 Pareto 最优值。实线上用圆圈标出的点由 $\ell_1$ 范数正则化启发式方法得到。</figcaption>
</figure>

<!-- Figure 6.8; original PDF page 327, printed page 313; crop 134,138,436,372. -->
<figure id="fig-6-8" data-figure="6.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-8.png" alt="上下两幅信号图：上图为包含四千个分量的平滑原始信号，下图为受噪声污染的信号，横轴均为分量索引 i" data-source-page="327" data-source-rect="134,138,436,372">
<figcaption>图 6.8 上图：原始信号 $x\in\mathbf{R}^{4000}$。下图：受噪声污染的信号 $x_{\mathrm{cor}}$。</figcaption>
</figure>

<!-- Figure 6.9; original PDF page 327, printed page 313; crop 164,452,397,635.5. The final norm in the source caption has no subscript. -->
<figure id="fig-6-9" data-figure="6.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-9.png" alt="平滑程度与重构误差之间的最优权衡曲线：曲线先陡降，在横坐标约为三时明显转折，此后逐渐趋平" data-source-page="327" data-source-rect="164,452,397,635.5">
<figcaption>图 6.9 $\|D\widehat{x}\|_2$ 与 $\|\widehat{x}-x_{\mathrm{cor}}\|_2$ 之间的最优权衡曲线。曲线在 $\|\widehat{x}-x_{\mathrm{cor}}\|\approx3$ 附近有一个明显的转折。</figcaption>
</figure>

<!-- Figure 6.10; original PDF page 328, printed page 314; crop 185,122,487,352. -->
<figure id="fig-6-10" data-figure="6.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-10.png" alt="上下排列的三个平滑或重构信号，重构误差范数从上到下为八、三、一；最上图最平滑，最下图保留较多噪声" data-source-page="328" data-source-rect="185,122,487,352">
<figcaption>图 6.10 三个经过平滑或重构的信号 $\widehat{x}$。最上图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=8$，中间图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=3$，最下图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=1$。</figcaption>
</figure>

<!-- Figure 6.11; original PDF page 329, printed page 315; crop 134,260,436,499. -->
<figure id="fig-6-11" data-figure="6.11" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-11.png" alt="上下两幅信号图：上图为主要部分平滑、在三个位置发生跳变的原始信号，下图为叠加快速变化噪声后的信号；横轴为分量索引 i" data-source-page="329" data-source-rect="134,260,436,499">
<figcaption>图 6.11 信号 $x\in\mathbf{R}^{2000}$ 及受噪声污染的信号 $x_{\mathrm{cor}}\in\mathbf{R}^{2000}$。噪声变化很快，而信号总体平滑，只有少数位置变化很快。</figcaption>
</figure>

<!-- Figure 6.12; original PDF page 330, printed page 316; crop 185,128,489,365. -->
<figure id="fig-6-12" data-figure="6.12" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-12.png" alt="采用二次平滑得到的三个信号：最上图噪声较小但跳变被明显抹平，最下图仍有较多噪声，中间图介于两者之间" data-source-page="330" data-source-rect="185,128,489,365">
<figcaption>图 6.12 三个经过二次平滑的信号 $\widehat{x}$。最上图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=10$，中间图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=7$，最下图对应 $\|\widehat{x}-x_{\mathrm{cor}}\|_2=4$。最上图大幅减小了噪声，但也过度平滑了信号中快速变化的部分。最下图中的平滑信号降噪不足，却仍然抹平了原信号中快速变化的部分。中间图中的平滑信号给出了最好的折中，但仍然抹平了快速变化的部分。</figcaption>
</figure>

<!-- Figure 6.13; original PDF page 330, printed page 316; crop 216,476,452,664.5. -->
<figure id="fig-6-13" data-figure="6.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-13.png" alt="信号总变差与重构误差之间的最优权衡曲线；曲线从左上方快速下降，随后逐渐趋近横轴" data-source-page="330" data-source-rect="216,476,452,664.5">
<figcaption>图 6.13 $\|D\widehat{x}\|_1$ 与 $\|\widehat{x}-x_{\mathrm{cor}}\|_2$ 之间的最优权衡曲线。</figcaption>
</figure>

<!-- Figure 6.14; original PDF page 331, printed page 317; crop 134,250,436,477. -->
<figure id="fig-6-14" data-figure="6.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-14.png" alt="采用总变差重构得到的三个信号，均保留原信号的三处跳变；最上图消除了部分缓慢变化，最下图仍有残留噪声" data-source-page="331" data-source-rect="134,250,436,477">
<figcaption>图 6.14 采用总变差重构得到的三个重构信号 $\widehat{x}$。最上图对应 $\|D\widehat{x}\|_1=5$，中间图对应 $\|D\widehat{x}\|_1=8$，最下图对应 $\|D\widehat{x}\|_1=10$。最下图的降噪还不够充分，而最上图消除了信号中一部分缓慢变化的成分。注意，与二次平滑不同，总变差重构保留了信号中的突变。</figcaption>
</figure>

<!-- Figure 6.15; original PDF page 334, printed page 320; crop 215,121,448,307. -->
<figure id="fig-6-15" data-figure="6.15" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-15.png" alt="标称、随机鲁棒和最坏情形鲁棒三种解的残差随参数 u 变化的曲线；标称解在零附近残差最小，最坏情形鲁棒解在负一至一区间内的残差变化最小" data-source-page="334" data-source-rect="215,121,448,307">
<figcaption>图 6.15 三个近似解 $x$ 的残差 $r(u)=\|A(u)x-b\|_2$ 随不确定参数 $u$ 变化的曲线。这三个解分别是：（1）标称最小二乘解 $x_{\mathrm{nom}}$；（2）随机鲁棒逼近问题的解 $x_{\mathrm{stoch}}$（假设 $u$ 在 $[-1,1]$ 上均匀分布）；（3）最坏情形鲁棒逼近问题的解 $x_{\mathrm{wc}}$，假设参数 $u$ 位于区间 $[-1,1]$ 内。标称解在 $u=0$ 时取得最小残差，但当 $u$ 接近 $-1$ 或 $1$ 时，其残差会大得多。最坏情形解在 $u=0$ 时的残差较大，但当参数 $u$ 在区间 $[-1,1]$ 内变化时，其残差不会增加很多。</figcaption>
</figure>

<!-- Figure 6.16; original PDF page 339, printed page 325; crop 140,259,413,474.5. -->
<figure id="fig-6-16" data-figure="6.16">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-16.png" alt="叠加的三组残差直方图，比较普通最小二乘、Tikhonov 正则化和鲁棒最小二乘的解；横轴为残差范数，纵轴为频率，鲁棒解的残差集中在较窄区间内" data-source-page="339" data-source-rect="140,259,413,474.5">
<figcaption>图 6.16 最小二乘问题（6.16）的三个解所对应的残差分布：$x_{\mathrm{ls}}$ 是假设 $u=0$ 时的最小二乘解；$x_{\mathrm{tik}}$ 是 $\delta=1$ 时的 Tikhonov 正则化解；$x_{\mathrm{rls}}$ 是鲁棒最小二乘解。这些直方图通过从 $\mathbf{R}^2$ 中单位圆盘上的均匀分布生成不确定参数向量 $u$ 的 $10^5$ 个取值得到。直方图各分组区间的宽度为 $0.1$。</figcaption>
<p class="figure-translation">图内文字：frequency——频率。</p>
</figure>

<!-- Figure 6.17; original PDF page 341, printed page 327; crop 166,121,399,299. -->
<figure id="fig-6-17" data-figure="6.17" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-17.png" alt="单位正方形上的二元分段线性函数三维图，曲面由三角形平面片拼接而成，坐标轴为 u₁、u₂ 和函数值" data-source-page="341" data-source-rect="166,121,399,299">
<figcaption>图 6.17 单位正方形上的一个二元分段线性函数。该三角剖分包含 98 个单纯形，所用的均匀网格由单位正方形内的 64 个点组成。</figcaption>
</figure>

<!-- Figure 6.18; original PDF page 342, printed page 328; crop 223,259,451,443. -->
<figure id="fig-6-18" data-figure="6.18" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-18.png" alt="由三个三次多项式拼接成的三次样条曲线；两个内部区间边界以竖直虚线表示，三个多项式在边界处平滑衔接" data-source-page="342" data-source-rect="223,259,451,443">
<figcaption>图 6.18 <em>三次样条。</em>三次样条是一阶、二阶导数均连续的分段多项式。本例中的三次样条 $f$ 由三个三次多项式组成：$p_1$ 定义在 $[u_0,u_1]$ 上，$p_2$ 定义在 $[u_1,u_2]$ 上，$p_3$ 定义在 $[u_2,u_3]$ 上。相邻多项式在边界点 $u_1$ 和 $u_2$ 处的函数值相同，一阶、二阶导数也分别相等。本例中，该函数族的维数为 $n=6$，因为共有 12 个多项式系数（每个三次多项式有 4 个）和 6 个等式约束（在 $u_1$ 和 $u_2$ 处各有 3 个）。</figcaption>
</figure>

<!-- Figure 6.19; original PDF page 346, printed page 332; crop 212,138,449,321. -->
<figure id="fig-6-19" data-figure="6.19" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-19.png" alt="对四十个圆圈数据点进行逼近的两条五次多项式曲线；实线使误差的二范数最小，虚线使误差的无穷范数最小" data-source-page="346" data-source-rect="212,138,449,321">
<figcaption>图 6.19 逼近图中 40 个圆圈所示数据点的两个五次多项式。实线所示的多项式最小化误差的 $\ell_2$ 范数；虚线所示的多项式最小化误差的 $\ell_\infty$ 范数。</figcaption>
</figure>

<!-- Figure 6.20; original PDF page 346, printed page 332; crop 212,420,449,603.5. -->
<figure id="fig-6-20" data-figure="6.20" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-20.png" alt="对四十个圆圈数据点进行逼近的两条三次样条曲线；实线使误差的二范数最小，虚线使误差的无穷范数最小，竖直虚线标示区间边界" data-source-page="346" data-source-rect="212,420,449,603.5">
<figcaption>图 6.20 逼近图中 40 个圆圈所示数据点的两条三次样条（数据点与图 6.19 相同）。实线所示的样条最小化误差的 $\ell_2$ 范数；虚线所示的样条最小化误差的 $\ell_\infty$ 范数。与图 6.19 所示的多项式逼近一样，拟合函数所在子空间的维数为 6。</figcaption>
</figure>

<!-- Figure 6.21; original PDF page 349, printed page 335; crop 129,123,431,361. -->
<figure id="fig-6-21" data-figure="6.21" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-21.png" alt="三个以时刻零点五为中心的字典基函数，按频率零、七十五、一百五十从上到下排列；频率越高，局部振荡越密集" data-source-page="349" data-source-rect="129,123,431,361">
<figcaption>图 6.21 字典中的三个基元素，中心时刻均为 $\tau=0.5$，相位均为余弦相位。最上方信号的频率为 $\omega=0$，中间信号的频率为 $\omega=75$，最下方信号的频率为 $\omega=150$。</figcaption>
</figure>

<!-- Figure 6.22; original PDF page 350, printed page 336; crop 174,123,483,361. -->
<figure id="fig-6-22" data-figure="6.22" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-22.png" alt="上图为几乎重合的原始信号和基追踪逼近信号，下图采用较小的纵轴刻度范围显示两者之间的逼近误差" data-source-page="350" data-source-rect="174,123,483,361">
<figcaption>图 6.22 上图：原始信号（实线）与通过基追踪得到的逼近信号 $\widehat{y}$（虚线）几乎无法区分。下图：逼近误差 $y(t)-\widehat{y}(t)$，纵轴采用了不同的刻度比例。</figcaption>
</figure>

<!-- Figure 6.23; original PDF page 351, printed page 337; crop 120,123,430,361. -->
<figure id="fig-6-23" data-figure="6.23" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-23.png" alt="上图为频率随时间变化的原始信号；下图为时频图，所选基元素对应的圆圈紧邻表示原始信号瞬时频率的虚线曲线" data-source-page="351" data-source-rect="120,123,430,361">
<figcaption>图 6.23 上图：原始信号。下图：时频图。虚线曲线表示原始信号的瞬时频率 $\omega(t)=150|\cos(5t)|$。每个圆圈对应通过基追踪得到的逼近中选用的一个基元素。横轴表示该基元素的时间索引 $\tau$，纵轴表示其频率索引 $\omega$。</figcaption>
</figure>

<!-- Figure 6.24; original PDF page 353, printed page 339; crop 175,123,394,279. -->
<figure id="fig-6-24" data-figure="6.24" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-24.png" alt="用凸的分段线性函数拟合圆圈数据点，折线在左侧下降，中部缓慢上升，右侧快速上升" data-source-page="353" data-source-rect="175,123,394,279">
<figcaption>图 6.24 用凸函数对圆圈所示的数据进行最小二乘拟合。图中所示的（分段线性）函数在所有凸函数中使拟合误差的平方和最小。</figcaption>
</figure>

<!-- Figure 6.25; original PDF page 356, printed page 342; crop 216,121,448,307. -->
<figure id="fig-6-25" data-figure="6.25" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-25.png" alt="单位正方形中的四十个圆圈表示两种商品的不同数量组合，九条虚线表示真实效用函数从零点一至零点九的等高线" data-source-page="356" data-source-rect="216,121,448,307">
<figcaption>图 6.25 40 个商品组合 $a_1,\ldots,a_{40}$，以圆圈表示。真实效用函数 $u$ 取值为 $0.1,\ 0.2,\ldots,0.9$ 的等高线以虚线表示。利用这个效用函数可以得到这 40 个商品组合之间的消费者偏好数据 $\mathcal{P}$。</figcaption>
</figure>

<!-- Figure 6.26; original PDF page 356, printed page 342; crop 216,374,448,560. -->
<figure id="fig-6-26" data-figure="6.26" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-06/fig-6-26.png" alt="相对于新商品组合零点五、零点五的偏好分析；空心圆表示确定不如新组合的点，黑色实心圆表示确定优于新组合的点，方框表示无法判定的点，虚线为通过新组合的真实效用等高线" data-source-page="356" data-source-rect="216,374,448,560">
<figcaption>图 6.26 针对新商品组合 $a_0=(0.5,0.5)$，利用 LP（6.25）进行消费者偏好分析的结果。对于原有商品组合，若能确定它不如新组合（$u(a_k)<u(a_0)$），则以空心圆表示；若能确定它优于新组合（$u(a_k)>u(a_0)$），则以黑色实心圆表示；若无法作出判断，则以方框表示。真实效用函数通过 $(0.5,0.5)$ 的等高线以虚线曲线表示。通过 $(0.5,0.5)$ 的竖直线和水平线把 $[0,1]^2$ 分成四个象限。根据对 $u$ 的单调性假设，右上象限中的点一定优于 $(0.5,0.5)$。同样，$(0.5,0.5)$ 一定优于左下象限中的点。对于另外两个象限中的点，结果并不显然。</figcaption>
</figure>
