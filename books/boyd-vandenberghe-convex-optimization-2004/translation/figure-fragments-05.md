<!-- Chapter 5 figure fragments for the chapter owner to integrate at their original locations. Author checked each original PDF page and existing source crop; independent chapter review is still required. This file is not a reader chapter. -->

<!-- Figure 5.1; original PDF page 231, printed page 217; crop 181,172,386,343. -->
<figure id="fig-5-1" data-figure="5.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-1.png" alt="目标函数、约束函数和多条拉格朗日函数曲线，两条竖向点线界定可行区间，圆点标出原问题的最优点及最优值" data-source-page="231" data-source-rect="181,172,386,343">
<figcaption>图 5.1 由对偶可行点得到的下界。实线表示目标函数 $f_0$，虚线表示约束函数 $f_1$。可行集是区间 $[-0.46,0.46]$，由两条竖向点线标出。最优点和最优值分别为 $x^\star=-0.46$、$p^\star=1.54$（用圆点表示）。点线曲线表示 $\lambda=0.1,0.2,\ldots,1.0$ 时的 $L(x,\lambda)$。每条曲线的最小值都小于 $p^\star$，因为在可行集上，当 $\lambda\geq0$ 时，有 $L(x,\lambda)\leq f_0(x)$。</figcaption>
</figure>

<!-- Figure 5.2; original PDF page 231, printed page 217; crop 168,424,386,595. -->
<figure id="fig-5-2" data-figure="5.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-2.png" alt="凹的对偶函数曲线和表示原问题最优值的水平虚线" data-source-page="231" data-source-rect="168,424,386,595">
<figcaption>图 5.2 图 5.1 中问题的对偶函数 $g$。$f_0$ 和 $f_1$ 都不是凸函数，但对偶函数是凹函数。水平虚线表示该问题的最优值 $p^\star$。</figcaption>
</figure>

<!-- Figure 5.3; original PDF page 247, printed page 233; crop 136,183,381,341. -->
<figure id="fig-5-3" data-figure="5.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-3.png" alt="阴影集合 G 与一条支撑直线，直线与纵轴的交点给出低于原问题最优值的对偶函数值" data-source-page="247" data-source-rect="136,183,381,341">
<figcaption>图 5.3 只有一个（不等式）约束的问题中，对偶函数及下界 $g(\lambda)\leq p^\star$ 的几何解释。给定 $\lambda$，在 $\mathcal{G}=\{(f_1(x),f_0(x))\mid x\in\mathcal{D}\}$ 上最小化 $(\lambda,1)^T(u,t)$。这样得到一条斜率为 $-\lambda$ 的支撑超平面。该超平面与 $u=0$ 轴的交点给出 $g(\lambda)$。</figcaption>
</figure>

<!-- Figure 5.4; original PDF page 247, printed page 233; crop 127,405,381,564. -->
<figure id="fig-5-4" data-figure="5.4" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-4.png" alt="三个对偶可行乘子对应的支撑直线，最优对偶值低于原问题的最优值" data-source-page="247" data-source-rect="127,405,381,564">
<figcaption>图 5.4 $\lambda$ 的三个对偶可行取值所对应的支撑超平面，其中包括最优取值 $\lambda^\star$。强对偶性不成立；最优对偶间隙 $p^\star-d^\star$ 为正。</figcaption>
</figure>

<!-- Figure 5.5; original PDF page 248, printed page 234; crop 181,118,444,274. -->
<figure id="fig-5-5" data-figure="5.5" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-5.png" alt="阴影集合 A 与一条支撑直线，纵轴上标出原问题的最优值和对偶函数值" data-source-page="248" data-source-rect="181,118,444,274">
<figcaption>图 5.5 只有一个（不等式）约束的问题中，对偶函数及下界 $g(\lambda)\leq p^\star$ 的几何解释。给定 $\lambda$，在 $\mathcal{A}=\{(u,t)\mid\exists x\in\mathcal{D},\ f_0(x)\leq t,\ f_1(x)\leq u\}$ 上最小化 $(\lambda,1)^T(u,t)$。这样得到一条斜率为 $-\lambda$ 的支撑超平面。该超平面与 $u=0$ 轴的交点给出 $g(\lambda)$。</figcaption>
</figure>

<!-- Figure 5.6; original PDF page 250, printed page 236; crop 246,118,435,306. -->
<figure id="fig-5-6" data-figure="5.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-6.png" alt="凸集 A、竖直线段 B 和一条分离直线，A 中标出严格可行点对应的位置，B 的上端为空心圆点" data-source-page="250" data-source-rect="246,118,435,306">
<figcaption>图 5.6 满足 Slater 约束资格条件的凸问题中，强对偶性证明的示意图。集合 $\mathcal{A}$ 用阴影表示，集合 $\mathcal{B}$ 是粗竖直线段，不包括用小空心圆表示的点 $(0,p^\star)$。这两个集合都是凸集且互不相交，因此可以用一个超平面将它们分离。Slater 约束资格条件保证，任何分离超平面都不能是竖直的，因为它必须从点 $(\widetilde u,\widetilde t)=(f_1(\widetilde x),f_0(\widetilde x))$ 的左侧经过，其中 $\widetilde x$ 是严格可行点。</figcaption>
</figure>

<!-- Figure 5.7; original PDF page 260, printed page 246; crop 227,121,433,236. The image label is x_i without a star; the source caption uses x_i^star. -->
<figure id="fig-5-7" data-figure="5.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-7.png" alt="高低不等的阶梯状地面与统一水位，阴影表示水，右侧箭头分别标出水深和地面高度" data-source-page="260" data-source-rect="227,121,433,236">
<figcaption>图 5.7 注水算法的示意图。每块地面的高度为 $\alpha_i$。向这片区域注水至水位 $1/\nu^\star$，总用水量为 1。每块地面上方的水深（用阴影表示）就是最优值 $x_i^\star$。</figcaption>
</figure>

<!-- Figure 5.8; original PDF page 260, printed page 246; crop 229,305,450,415. -->
<figure id="fig-5-8" data-figure="5.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-8.png" alt="两个宽度均为 w 的物块通过三个弹簧彼此相连并连接两端墙壁，下方标出物块中心位置和墙间距离" data-source-page="260" data-source-rect="229,305,450,415">
<figcaption>图 5.8 两个物块通过弹簧彼此相连，并与左右两侧的墙壁相连。物块的宽度为 $w>0$，不能相互穿透，也不能穿过墙壁。</figcaption>
</figure>

<!-- Figure 5.9; original PDF page 261, printed page 247; crop 128,120,463,152. Both original force diagrams remain in one image; signs are represented by the original arrow directions. -->
<figure id="fig-5-9" data-figure="5.9" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-9.png" alt="两个物块的受力图，上方箭头表示接触力，下方箭头表示弹簧力" data-source-page="261" data-source-rect="128,120,463,152">
<figcaption>图 5.9 物块与弹簧系统的受力分析。每个物块受到的弹簧力与接触力的合力必须为零。上方标出的拉格朗日乘子，是墙壁和物块之间的接触力。弹簧力标在下方。</figcaption>
</figure>

<!-- Figure 5.10; original PDF page 265, printed page 251; crop 176,121,415,290. -->
<figure id="fig-5-10" data-figure="5.10" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-05/fig-5-10.png" alt="凸问题的最优值曲线与仿射下界直线，竖向点线标出没有扰动的位置 u=0" data-source-page="265" data-source-rect="176,121,415,290">
<figcaption>图 5.10 具有单个约束 $f_1(x)\leq u$ 的凸问题的最优值 $p^\star(u)$ 随 $u$ 的变化。当 $u=0$ 时，得到原来的未扰动问题；当 $u<0$ 时，约束收紧；当 $u>0$ 时，约束放宽。仿射函数 $p^\star(0)-\lambda^\star u$ 是 $p^\star$ 的一个下界。</figcaption>
</figure>
