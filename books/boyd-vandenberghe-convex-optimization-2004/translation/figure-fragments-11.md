<!-- Chapter 11 figure fragments for integration at their original source locations. Original PDF pages and existing crops checked by the caption translator; independent chapter review remains required. -->

<!-- Figure 11.1; original PDF page 577, printed page 563; crop 182,121,384,293. -->
<figure id="fig-11-1" data-figure="11.1" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-1.png" alt="横轴为 u；虚线沿负半轴的零值水平线和 u=0 的竖线延伸，三条对数障碍近似曲线都经过点 (−1,0)，并在 u 从左侧趋近零时上升。" data-source-page="577" data-source-rect="182,121,384,293">
<figcaption>图 11.1 虚线表示函数 $I_-(u)$，实线表示 $t=0.5,1,2$ 时的函数 $\widehat I_-(u)=-(1/t)\log(-u)$。其中，$t=2$ 的曲线给出了最好的近似。</figcaption>
</figure>

<!-- Figure 11.2; original PDF page 580, printed page 566; crop 237,120,442,261. -->
<figure id="fig-11-2" data-figure="11.2" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-2.png" alt="二维线性规划的中心路径位于六条约束边界围成的区域内，趋向顶点 x⋆；图中还有三条虚线等高线、路径上的点 x⋆(10)、该点处的切线和目标方向 c。" data-source-page="580" data-source-rect="237,120,442,261">
<figcaption>图 11.2 一个 $n=2$、$m=6$ 的线性规划的中心路径。虚线表示对数障碍函数 $\phi$ 的三条等高线。当 $t\to\infty$ 时，中心路径收敛到最优点 $x^\star$。图中还标出了中心路径上对应于 $t=10$ 的点。该点处的最优性条件 (11.9) 可以从几何上验证：直线 $c^Tx=c^Tx^\star(10)$ 与经过 $x^\star(10)$ 的 $\phi$ 等高线相切。</figcaption>
</figure>

<!-- Figure 11.3; original PDF page 582, printed page 568; crop 179,120,498,258. -->
<figure id="fig-11-3" data-figure="11.3" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-3.png" alt="左右两图展示中心路径上两个平衡点的受力；粗箭头分别为目标力 −c 和 −3c，其余箭头为约束力，虚线为中心路径。右图的平衡点更靠近最优顶点。" data-source-page="582" data-source-rect="179,120,498,258">
<figcaption>图 11.3 <em>中心路径的力场解释。</em> 虚线表示中心路径。左、右图中的圆点分别表示 $x^\star(1)$ 和 $x^\star(3)$。目标力分别等于 $-c$ 和 $-3c$，用粗箭头表示。其余箭头表示约束力，其大小服从与距离成反比的规律。随着目标力的强度变化，质点的平衡位置就描出中心路径。</figcaption>
</figure>

<!-- Figure 11.4; original PDF page 586, printed page 572; crop 204,122,449,305. -->
<figure id="fig-11-4" data-figure="11.4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-4.png" alt="小规模线性规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，三条曲线分别标为 μ=50、150、2。" data-source-page="586" data-source-rect="204,122,449,305">
<figcaption>图 11.4 障碍法求解一个小规模线性规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。三条曲线分别对应参数 $\mu$ 的三个取值：$2$、$50$ 和 $150$。每种情况下，对偶间隙都近似线性收敛。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.5; original PDF page 587, printed page 573; crop 159,122,399,304. -->
<figure id="fig-11-5" data-figure="11.5">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-5.png" alt="小规模线性规划所需牛顿迭代总次数随 μ 变化的曲线；μ 接近 1 时次数很高，随后迅速下降，在较大的 μ 范围内仅小幅波动，圆圈标出各个试验值。" data-source-page="587" data-source-rect="159,122,399,304">
<figcaption>图 11.5 一个小规模线性规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。图中表明，当 $\mu$ 大于约 $3$ 时，障碍法表现良好，而在此范围内，其表现对 $\mu$ 的具体取值并不敏感。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.6; original PDF page 588, printed page 574; crop 204,122,453,305. -->
<figure id="fig-11-6" data-figure="11.6">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-6.png" alt="小规模几何规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=150、50、2。" data-source-page="588" data-source-rect="204,122,453,305">
<figcaption>图 11.6 障碍法求解一个小规模几何规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。这里，对偶间隙同样近似线性收敛。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.7; original PDF page 590, printed page 576; crop 204,140,468,324. -->
<figure id="fig-11-7" data-figure="11.7">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-7.png" alt="三个标准形式线性规划的阶梯状对偶间隙曲线，分别标为 m=50、500、1000；横轴为累计牛顿迭代次数，问题较大时达到小对偶间隙所需的迭代次数略多。" data-source-page="590" data-source-rect="204,140,468,324">
<figcaption>图 11.7 障碍法求解三个随机生成、规模不同的标准形式线性规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。每个问题的变量个数均为 $n=2m$。这里也可以看到，对偶间隙近似线性收敛；对于较大的问题，所需的牛顿步数略有增加。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.8; original PDF page 590, printed page 576; crop 222,436,444,611. -->
<figure id="fig-11-8" data-figure="11.8">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-8.png" alt="横轴 m 从 10 到 1000，采用对数刻度；平均牛顿迭代次数由约 21 次缓慢升至约 27 次，各个圆圈处的竖直误差条表示标准差。" data-source-page="590" data-source-rect="222,436,444,611">
<figcaption>图 11.8 在不同问题规模下，求解 $100$ 个随机生成的线性规划所需的平均牛顿步数，其中 $n=2m$。对于 $m$ 的每个取值，误差条表示平均值上下的标准差。尽管最大与最小问题规模之比为 $100:1$，所需牛顿步数的增长仍很小。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.9; original PDF page 595, printed page 581; crop 90,121,472,274. -->
<figure id="fig-11-9" data-figure="11.9">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-9.png" alt="两个直方图比较不同方法所得向量对应的取值分布；左图横轴为 bᵢ−aᵢᵀx_max，右图为 bᵢ−aᵢᵀx_sum，纵轴均为不等式个数，最高的柱都位于零附近。" data-source-page="595" data-source-rect="90,121,472,274">
<figcaption>图 11.9 对于一组不可行的、含 $50$ 个变量的 $100$ 个不等式 $a_i^Tx\leq b_i$，图中给出了不可行度 $b_i-a_i^Tx$ 的分布。左图所用的向量 $x_{\mathrm{max}}$ 由基本的第一阶段算法得到，它满足 $100$ 个不等式中的 $39$ 个。右图所用的向量 $x_{\mathrm{sum}}$ 由最小化不可行度之和得到，它满足 $100$ 个不等式中的 $79$ 个。</figcaption>
<p class="figure-translation">图内文字：左右两图的 number——个数。</p>
</figure>

<!-- Figure 11.10; original PDF page 598, printed page 584; crop 212,161,449,343. -->
<figure id="fig-11-10" data-figure="11.10">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-10.png" alt="判定线性不等式可行性所需的牛顿迭代次数随 γ 变化；γ=0 处的竖直虚线分开左侧不可行区与右侧可行区，迭代次数在接近零时明显增多。" data-source-page="598" data-source-rect="212,161,449,343">
<figcaption>图 11.10 判定由 $\gamma\in\mathbf{R}$ 参数化的一组线性不等式 $Ax\preceq b+\gamma\Delta b$ 可行或不可行所需的牛顿迭代次数。当 $\gamma>0$ 时，不等式严格可行；当 $\gamma<0$ 时，不等式不可行。当 $\gamma$ 大于约 $0.2$ 时，计算一个严格可行点约需 $30$ 步；当 $\gamma$ 小于约 $-0.5$ 时，得到一个证明不可行的证书约需 $35$ 步。对于介于两者之间、尤其是接近零的 $\gamma$ 值，需要更多牛顿步才能判定可行性。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；Infeasible——不可行；Feasible——可行。</p>
</figure>

<!-- Figure 11.11; original PDF page 598, printed page 584; crop 143,453,523,599. -->
<figure id="fig-11-11" data-figure="11.11">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-11.png" alt="两图以对数刻度展开 γ 接近零时的结果：左图中 γ 从负侧趋近零，证明不可行所需的牛顿迭代次数上升；右图中正 γ 逐渐增大，求得严格可行点所需的次数下降。" data-source-page="598" data-source-rect="143,453,523,599">
<figcaption>图 11.11 <em>左图。</em> 当 $\gamma$ 为绝对值较小的负数时，找到不可行性证明所需的牛顿迭代次数随 $\gamma$ 的变化。<em>右图。</em> 当 $\gamma$ 为较小的正数时，找到严格可行点所需的牛顿迭代次数随 $\gamma$ 的变化。</figcaption>
<p class="figure-translation">图内文字：左右两图的 Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.12; original PDF page 599, printed page 585; crop 160,121,397,305. -->
<figure id="fig-11-12" data-figure="11.12">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-12.png" alt="不可行初始点牛顿法找到可行点所需的迭代次数随正参数 γ 增大而下降；横轴 γ 和纵轴牛顿迭代次数均采用对数刻度，圆圈表示各次试验的结果。" data-source-page="599" data-source-rect="160,121,397,305">
<figcaption>图 11.12 对于由 $\gamma\in\mathbf{R}$ 参数化的一组线性不等式 $Ax\preceq b+\gamma\Delta b$，找到可行点所需的迭代次数。这里使用不可行初始点牛顿法，并在找到可行点时终止。当 $\gamma=10$ 时，初始点 $x^{(0)}=0$ 恰好可行，因此迭代次数为 $0$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.13; original PDF page 603, printed page 589; crop 168,121,385,294. -->
<figure id="fig-11-13" data-figure="11.13" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-13.png" alt="函数 μ−1−log μ 在 μ 从 1 到 3 的区间上的曲线，从零开始上升，且斜率逐渐增大；横轴为 μ，纵轴为函数值。" data-source-page="603" data-source-rect="168,121,385,294">
<figcaption>图 11.13 函数 $\mu-1-\log\mu$ 随 $\mu$ 的变化。障碍法一次外层迭代所需的牛顿步数不超过 $(m/\gamma)(\mu-1-\log\mu)+c$。</figcaption>
</figure>

<!-- Figure 11.14; original PDF page 605, printed page 591; crop 156,125,400,313. -->
<figure id="fig-11-14" data-figure="11.14" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-14.png" alt="牛顿迭代总次数的上界 N 随障碍法参数 μ 变化；μ 略大于 1 时曲线迅速下降到最低点，随后总体上升，右侧可见细小锯齿。" data-source-page="605" data-source-rect="156,125,400,313">
<figcaption>图 11.14 当 $c=6$、$\gamma=1/375$、$m=100$，且对偶间隙的缩减倍数为 $m/(t^{(0)}\epsilon)=10^5$ 时，由式 (11.27) 给出的牛顿迭代总次数上界 $N$ 随障碍算法参数 $\mu$ 的变化。</figcaption>
</figure>

<!-- Figure 11.15; original PDF page 616, printed page 602; crop 204,122,449,305. -->
<figure id="fig-11-15" data-figure="11.15">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-15.png" alt="二阶锥规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=50、200、2。" data-source-page="616" data-source-rect="204,122,449,305">
<figcaption>图 11.15 障碍法求解一个二阶锥规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.16; original PDF page 617, printed page 603; crop 159,122,399,304. -->
<figure id="fig-11-16" data-figure="11.16">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-16.png" alt="小规模二阶锥规划所需牛顿迭代总次数随 μ 变化；μ 接近 1 时次数很高，随后迅速下降，在较大 μ 下只作小幅波动，圆圈标出试验值。" data-source-page="617" data-source-rect="159,122,399,304">
<figcaption>图 11.16 一个小规模二阶锥规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.17; original PDF page 618, printed page 604; crop 204,150,453,333. -->
<figure id="fig-11-17" data-figure="11.17">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-17.png" alt="小规模半定规划的三条阶梯状收敛曲线；横轴为累计牛顿迭代次数，纵轴为对偶间隙的对数刻度，曲线分别标为 μ=150、50、2。" data-source-page="618" data-source-rect="204,150,453,333">
<figcaption>图 11.17 障碍法求解一个小规模半定规划时的迭代过程，图中给出了对偶间隙随累计牛顿步数的变化。三条曲线分别对应参数 $\mu$ 的三个取值：$2$、$50$ 和 $150$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.18; original PDF page 618, printed page 604; crop 212,435,453,620. -->
<figure id="fig-11-18" data-figure="11.18">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-18.png" alt="小规模半定规划所需牛顿迭代总次数随 μ 变化；较小 μ 处的曲线陡降，随后在较低的迭代次数附近波动，圆圈标出试验值。" data-source-page="618" data-source-rect="212,435,453,620">
<figcaption>图 11.18 一个小规模半定规划中，参数 $\mu$ 的选择所涉及的权衡。纵轴表示将对偶间隙从 $100$ 降至 $10^{-3}$ 所需的牛顿步总数，横轴表示 $\mu$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.19; original PDF page 619, printed page 605; crop 153,120,429,306. -->
<figure id="fig-11-19" data-figure="11.19">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-19.png" alt="三个半定规划的阶梯状对偶间隙曲线，分别标为 n=50、500、1000；横轴为累计牛顿迭代次数，纵轴采用对数刻度，三条曲线的下降走势相似。" data-source-page="619" data-source-rect="153,120,429,306">
<figcaption>图 11.19 障碍法求解三个随机生成、规模不同且具有 (11.47) 形式的半定规划时的迭代过程。图中给出了对偶间隙随累计牛顿步数的变化。每个问题的变量个数为 $n$。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数；duality gap——对偶间隙。</p>
</figure>

<!-- Figure 11.20; original PDF page 620, printed page 606; crop 223,121,444,295. -->
<figure id="fig-11-20" data-figure="11.20">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-20.png" alt="横轴为问题规模 n，采用从 10 到 1000 的对数刻度；平均牛顿迭代次数从约 20 次缓慢升至约 26 次，每个圆圈处的竖直误差条表示标准差。" data-source-page="620" data-source-rect="223,121,444,295">
<figcaption>图 11.20 对问题规模 $n$ 的 $20$ 个取值中的每一个，求解 $100$ 个随机生成的半定规划 (11.47) 所需的平均牛顿步数。对于 $n$ 的每个取值，误差条表示平均值上下的标准差。尽管最大与最小问题规模之比为 $100:1$，所需平均牛顿步数的增长仍很小。</figcaption>
<p class="figure-translation">图内文字：Newton iterations——牛顿迭代次数。</p>
</figure>

<!-- Figure 11.21; original PDF page 628, printed page 614; crop 130,159,524,307. -->
<figure id="fig-11-21" data-figure="11.21">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-21.png" alt="原始–对偶内点法求解线性规划的两条收敛曲线；左图为替代对偶间隙 η̂，右图为可行性残差范数 r_feas，纵轴均为对数刻度。右图约在第 24 次迭代骤降，左图约在第 28 次迭代达到很小值。" data-source-page="628" data-source-rect="130,159,524,307">
<figcaption>图 11.21 原始–对偶内点法求解一个线性规划时的迭代过程，图中给出了替代对偶间隙 $\widehat\eta$ 以及原残差与对偶残差的范数随迭代次数的变化。残差在 $24$ 次迭代内迅速收敛到零；替代对偶间隙也在约 $28$ 次迭代后收敛到很小的数值。原始–对偶内点法比障碍法收敛更快，尤其是在要求高精度时。</figcaption>
<p class="figure-translation">图内文字：左右两图的 iteration number——迭代次数。</p>
</figure>

<!-- Figure 11.22; original PDF page 628, printed page 614; crop 130,463,524,611. -->
<figure id="fig-11-22" data-figure="11.22">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-22.png" alt="原始–对偶内点法求解几何规划的两条收敛曲线；左图为替代对偶间隙 η̂，右图为可行性残差范数 r_feas，两者随迭代次数逐渐减小，并在后几次迭代中快速下降，纵轴均为对数刻度。" data-source-page="628" data-source-rect="130,463,524,611">
<figcaption>图 11.22 原始–对偶内点法求解一个几何规划时的迭代过程，图中给出了替代对偶间隙 $\widehat\eta$ 以及原残差与对偶残差的范数随迭代次数的变化。</figcaption>
<p class="figure-translation">图内文字：左右两图的 iteration number——迭代次数。</p>
</figure>

<!-- Figure 11.23; original PDF page 629, printed page 615; crop 168,121,388,295. -->
<figure id="fig-11-23" data-figure="11.23">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-11/fig-11-23.png" alt="问题规模 m 从 10 增至 1000 时，平均迭代次数由约 16 次增至约 38 次；横轴为对数刻度，各圆圈处的竖直误差条表示标准差。" data-source-page="629" data-source-rect="168,121,388,295">
<figcaption>图 11.23 求解随机生成、规模不同的标准形式线性规划所需的迭代次数，其中 $n=2m$。对于每种规模的 $100$ 个实例，误差条表示平均值上下的标准差。当最大与最小问题规模之比达到 $100:1$ 时，所需迭代次数近似按对数增长。</figcaption>
<p class="figure-translation">图内文字：iterations——迭代次数。</p>
</figure>
