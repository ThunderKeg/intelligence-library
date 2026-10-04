<!-- Chapter 10 figure fragments for integration at their original source locations. Original PDF pages and existing crops checked by the caption translator; independent chapter review remains required. -->

<!-- Figure 10.1; original PDF page 557, printed page 543; crop 145,155,418,354.6. -->
<figure id="fig-10-1" data-figure="10.1">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-1.png" alt="不可行初始点牛顿法的原残差和对偶残差范数随迭代次数变化；实线在第 8 次迭代陡降，虚线随后陡降，纵轴为对数刻度。" data-source-page="557" data-source-rect="145,155,418,354.6">
<figcaption>图 10.1 不可行初始点牛顿法求解一个带等式约束的解析中心问题时的迭代过程，该问题有 $100$ 个变量和 $50$ 个约束。图中给出了 $\|r_{\mathrm{pri}}\|_2$（实线）和 $\|r_{\mathrm{dual}}\|_2$（虚线）。注意，经过 $8$ 次迭代后便达到并保持可行，约从第 $9$ 次迭代开始呈二次收敛。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数；$\|r_{\mathrm{pri}}\|_2$ and $\|r_{\mathrm{dual}}\|_2$——$\|r_{\mathrm{pri}}\|_2$ 与 $\|r_{\mathrm{dual}}\|_2$。</p>
</figure>

<!-- Figure 10.2; original PDF page 557, printed page 543; crop 158,412,398,597.4. -->
<figure id="fig-10-2" data-figure="10.2">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-2.png" alt="步长 t 随迭代次数变化；第 1 至第 7 次迭代的步长为 0.5，第 8 次起步长为 1，空心圆标出各次迭代的取值。" data-source-page="557" data-source-rect="158,412,398,597.4">
<figcaption>图 10.2 同一个算例中，步长随迭代次数的变化。第 $8$ 次迭代取完整步长，因而从该次迭代起保持可行。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<!-- Figure 10.3; original PDF page 558, printed page 544; crop 207,158,471,357.4. -->
<figure id="fig-10-3" data-figure="10.3">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-3.png" alt="不可行算例中，原残差范数的实线下降后逐渐变平，对偶残差范数的虚线经过起伏后也逐渐变平；两者均未趋于零，纵轴为对数刻度。" data-source-page="558" data-source-rect="207,158,471,357.4">
<figcaption>图 10.3 不可行初始点牛顿法求解一个带等式约束的解析中心问题时的迭代过程，该问题有 $100$ 个变量和 $50$ 个约束，且 $\mathbf{dom}\,f=\mathbf{R}_{++}^{100}$ 与 $\{z\mid Az=b\}$ 不相交。图中给出了 $\|r_{\mathrm{pri}}\|_2$（实线）和 $\|r_{\mathrm{dual}}\|_2$（虚线）。在这种情况下，残差不收敛到零。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数；$\|r_{\mathrm{pri}}\|_2$ and $\|r_{\mathrm{dual}}\|_2$——$\|r_{\mathrm{pri}}\|_2$ 与 $\|r_{\mathrm{dual}}\|_2$。</p>
</figure>

<!-- Figure 10.4; original PDF page 558, printed page 544; crop 212,413,452,602.5. -->
<figure id="fig-10-4" data-figure="10.4">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-4.png" alt="不可行算例的步长 t 随迭代次数变化；最初几次为 0.25，随后逐级下降并趋近零，所有步长都小于 1。" data-source-page="558" data-source-rect="212,413,452,602.5">
<figcaption>图 10.4 不可行算例中，步长随迭代次数的变化。从未取完整步长，且步长收敛到零。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<!-- Figure 10.5; original PDF page 559, printed page 545; crop 147,112,417,308.5. -->
<figure id="fig-10-5" data-figure="10.5">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-5.png" alt="凸–凹博弈中，梯度范数 ‖∇f(u,v)‖₂ 随迭代次数下降，约从第 5 次迭代之后下降明显加快；纵轴为对数刻度。" data-source-page="559" data-source-rect="147,112,417,308.5">
<figcaption>图 10.5 将牛顿法（从不可行初始点出发）用于凸–凹博弈时的迭代过程。约在 $5$ 次迭代之后，可以明显看出二次收敛。</figcaption>
<p class="figure-translation">图内文字：iteration number——迭代次数。</p>
</figure>

<!-- Figure 10.6; original PDF page 563, printed page 549; crop 144,132,417,329.6. -->
<figure id="fig-10-6" data-figure="10.6" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-6.png" alt="四个不同起始点对应的牛顿法误差曲线；横轴为迭代次数 k，纵轴为 f(x⁽ᵏ⁾)−p⋆ 的对数刻度，各曲线在最后几次迭代中迅速下降。" data-source-page="563" data-source-rect="144,132,417,329.6">
<figcaption>图 10.6 将牛顿法用于规模为 $p=100$、$n=500$ 的带等式约束的解析中心问题时，误差 $f(x^{(k)})-p^\star$ 的变化。不同曲线对应四个不同的起始点。最终阶段的二次收敛十分明显。</figcaption>
</figure>

<!-- Figure 10.7; original PDF page 563, printed page 549; crop 144,429,418,627.2. -->
<figure id="fig-10-7" data-figure="10.7" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-7.png" alt="对偶问题中四条牛顿法曲线随迭代次数 k 下降；纵轴标为 p⋆−g(ν⁽ᵏ⁾)，采用对数刻度，各曲线在后几次迭代中迅速下降。" data-source-page="563" data-source-rect="144,429,418,627.2">
<figcaption>图 10.7 将牛顿法用于带等式约束的解析中心问题的对偶问题时，误差 $|g(\nu^{(k)})-p^\star|$ 的变化。</figcaption>
</figure>

<!-- Figure 10.8; original PDF page 564, printed page 550; crop 198,112,471,307.3. -->
<figure id="fig-10-8" data-figure="10.8" data-no-english-text="true">
<img src="books/boyd-vandenberghe-convex-optimization-2004/assets/chapter-10/fig-10-8.png" alt="不可行初始点牛顿法的四条残差范数曲线；横轴为迭代次数 k，纵轴为 ‖r(x⁽ᵏ⁾,ν⁽ᵏ⁾)‖₂ 的对数刻度，各曲线先逐渐下降，随后迅速降至很小。" data-source-page="564" data-source-rect="198,112,471,307.3">
<figcaption>图 10.8 将不可行初始点牛顿法用于带等式约束的解析中心问题时，残差 $\|r(x^{(k)},\nu^{(k)})\|_2$ 的变化。</figcaption>
</figure>
