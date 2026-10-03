\(\mathbf D\) 是对角线上为 \(\mu(s)\) 的 \(|\mathcal S|\times|\mathcal S|\) 对角矩阵，而 \(\mathbf X\) 是以 \(\mathbf x(s)\) 为各行的 \(|\mathcal S|\times d\) 矩阵。由此可见，内部矩阵 \(\mathbf D(\mathbf I-\gamma\mathbf P)\) 是决定 \(\mathbf A\) 是否正定的关键。

对于这种形式的关键矩阵，只要它的每一列之和都非负，就能保证其正定性。Sutton（1988，第 27 页）根据两个先前建立的定理证明了这一点。第一个定理指出，矩阵 \(\mathbf M\) 正定，当且仅当对称矩阵 \(\mathbf S=\mathbf M+\mathbf M^\top\) 正定（Sutton 1988，附录）。第二个定理指出，若实对称矩阵 \(\mathbf S\) 的每个对角元素都为正，且大于同一行非对角元素绝对值之和，则 \(\mathbf S\) 正定（Varga 1962，第 23 页）。对这里的关键矩阵 \(\mathbf D(\mathbf I-\gamma\mathbf P)\) 而言，对角元素为正，非对角元素为负，因此只须证明每一行的行和加上对应列的列和为正。由于 \(\mathbf P\) 是随机矩阵，且 \(\gamma<1\)，各行之和都为正。所以剩下只需证明各列之和非负。注意，任意矩阵 \(\mathbf M\) 的各列列和所组成的行向量可写成 \(\mathbf 1^\top\mathbf M\)，其中 \(\mathbf 1\) 是各分量均为 1 的列向量。令 \(\boldsymbol\mu\) 表示由 \(\mu(s)\) 组成的 \(|\mathcal S|\) 维向量；由于它是平稳分布，\(\boldsymbol\mu=\mathbf P^\top\boldsymbol\mu\)。于是，关键矩阵的各列之和为：

\[
\begin{aligned}
\mathbf 1^\top\mathbf D(\mathbf I-\gamma\mathbf P)
&=\boldsymbol\mu^\top(\mathbf I-\gamma\mathbf P)\\
&=\boldsymbol\mu^\top-\gamma\boldsymbol\mu^\top\mathbf P\\
&=\boldsymbol\mu^\top-\gamma\boldsymbol\mu^\top
\quad\text{（因为 }\boldsymbol\mu\text{ 是平稳分布）}\\
&=(1-\gamma)\boldsymbol\mu^\top,
\end{aligned}
\]

其各分量均为正。因此，关键矩阵及其对应的 \(\mathbf A\) 正定，同策略 TD(0) 稳定。（若要证明以概率 1 收敛，还需要附加条件和一个随时间递减 \(\alpha\) 的安排。）

:::end-source-box

在 TD 不动点处，已有证明表明，对持续性任务，均方价值误差 \(\overline{\mathrm{VE}}\) 相对于可能达到的最小误差有一个上界：

\[
\overline{\mathrm{VE}}(\mathbf w_{\mathrm{TD}})
\le\frac{1}{1-\gamma}\min_{\mathbf w}\overline{\mathrm{VE}}(\mathbf w). \tag{9.14}
\]

也就是说，TD 方法的渐近误差，不超过最小可能误差的 \(1/(1-\gamma)\) 倍；这里的最小误差是蒙特卡洛方法在极限下达到的。由于 \(\gamma\) 往往接近 1，这个放大系数可能很大，所以 TD 方法的渐近表现可能损失不少。另一方面，如第 6、7 章所见，相比蒙特卡洛方法，TD 方法的方差通常低得多，因而学习更快。哪一种方法更好，取决于函数近似和任务的性质，以及学习会持续多久。
