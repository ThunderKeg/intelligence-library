其中

\[
\mathbf b\doteq\mathbb E[R_{t+1}\mathbf x_t]\in\mathbb R^d,
\qquad
\mathbf A\doteq\mathbb E\big[\mathbf x_t(\mathbf x_t-\gamma\mathbf x_{t+1})^\top\big]\in\mathbb R^{d\times d}. \tag{9.11}
\]

由（9.10）可知，如果系统收敛，就必定收敛到满足以下条件的权重向量 \(\mathbf w_{\mathrm{TD}}\)：

\[
\begin{aligned}
\mathbf b-\mathbf A\mathbf w_{\mathrm{TD}}&=0\\
\Longrightarrow\quad \mathbf b&=\mathbf A\mathbf w_{\mathrm{TD}}\\
\Longrightarrow\quad \mathbf w_{\mathrm{TD}}&\doteq\mathbf A^{-1}\mathbf b.
\end{aligned} \tag{9.12}
\]

这个量称为 **TD 不动点（TD fixed point）**。实际上，线性半梯度 TD(0) 会收敛到这一点。证明其收敛以及上述逆矩阵存在性的部分理论，见下面的方框。

:::source-box

### 线性 TD(0) 的收敛性证明

什么性质能保证线性 TD(0) 算法（9.9）收敛？把（9.10）改写为下式，可以得到一些直观认识：

\[
\mathbb E[\mathbf w_{t+1}\mid\mathbf w_t]=(\mathbf I-\alpha\mathbf A)\mathbf w_t+\alpha\mathbf b. \tag{9.13}
\]

注意，乘在权重向量 \(\mathbf w_t\) 上的是矩阵 \(\mathbf A\)，而不是 \(\mathbf b\)；对收敛性起决定作用的只有 \(\mathbf A\)。先考虑 \(\mathbf A\) 是对角矩阵的特殊情况。如果某个对角元素为负，那么 \(\mathbf I-\alpha\mathbf A\) 中对应的对角元素就大于 1，\(\mathbf w_t\) 的对应分量会被放大；如果这种情况持续，就会发散。反过来，若 \(\mathbf A\) 的对角元素全为正，就可以选取小于其中最大值倒数的 \(\alpha\)，使 \(\mathbf I-\alpha\mathbf A\) 的对角元素全在 0 和 1 之间。此时，更新式的第一项会使 \(\mathbf w_t\) 趋于缩小，稳定性就有了保证。一般地，只要 \(\mathbf A\) **正定（positive definite）**，即任意非零实向量 \(\mathbf y\) 都满足 \(\mathbf y^\top\mathbf A\mathbf y>0\)，\(\mathbf w_t\) 就会趋向零方向缩小。正定性还保证逆矩阵 \(\mathbf A^{-1}\) 存在。

对于折扣因子 \(\gamma<1\) 的持续性任务，线性 TD(0) 的矩阵 \(\mathbf A\)（9.11）可写成

\[
\begin{aligned}
\mathbf A
&=\sum_s\mu(s)\sum_a\pi(a\mid s)\sum_{r,s'}p(r,s'\mid s,a)\,\mathbf x(s)\big(\mathbf x(s)-\gamma\mathbf x(s')\big)^\top\\
&=\sum_s\mu(s)\sum_{s'}p(s'\mid s)\,\mathbf x(s)\big(\mathbf x(s)-\gamma\mathbf x(s')\big)^\top\\
&=\sum_s\mu(s)\mathbf x(s)\left(\mathbf x(s)-\gamma\sum_{s'}p(s'\mid s)\mathbf x(s')\right)^\top\\
&=\mathbf X^\top\mathbf D(\mathbf I-\gamma\mathbf P)\mathbf X,
\end{aligned}
\]

其中 \(\mu(s)\) 是策略 \(\pi\) 下的平稳分布，\(p(s'\mid s)\) 是该策略下从 \(s\) 转移到 \(s'\) 的概率；\(\mathbf P\) 是由这些概率组成的 \(|\mathcal S|\times|\mathcal S|\) 矩阵，
