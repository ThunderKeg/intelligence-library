**习题 12.7** 把上文的三个递归方程推广到各自的截断版本，定义 \(G_{t:h}^{\lambda s}\) 和 \(G_{t:h}^{\lambda a}\)。 □

## 12.9 带控制变量的异策略资格迹

最后一步是纳入重要性采样。对于使用未截断 \(\lambda\)-回报的方法，没有一种实用的选择，可以像 §7.3 所述的 \(n\) 步方法那样，对目标回报施加重要性采样权重。因此，我们直接采用带控制变量的逐决策重要性采样的自举推广（§7.4）。

在状态价值的情形，\(\lambda\)-回报的最终定义依照式（7.13）的形式推广式（12.18），得到

\[
G_t^{\lambda s}\doteq\rho_t\Bigl(R_{t+1}+\gamma_{t+1}\bigl((1-\lambda_{t+1})\hat v(S_{t+1},\mathbf w_t)+\lambda_{t+1}G_{t+1}^{\lambda s}\bigr)\Bigr)+(1-\rho_t)\hat v(S_t,\mathbf w_t). \tag{12.22}
\]

其中 \(\rho_t=\frac{\pi(A_t\mid S_t)}{b(A_t\mid S_t)}\) 是通常的单步重要性采样比。与本书介绍过的许多其他回报类似，这个最终的 \(\lambda\)-回报也可以简单地近似写成基于状态的 TD 误差之和。先定义

\[
\delta_t^s\doteq R_{t+1}+\gamma_{t+1}\hat v(S_{t+1},\mathbf w_t)-\hat v(S_t,\mathbf w_t), \tag{12.23}
\]

则有

\[
G_t^{\lambda s}\approx\hat v(S_t,\mathbf w_t)+\rho_t\sum_{k=t}^{\infty}\delta_k^s\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i. \tag{12.24}
\]

如果近似价值函数不随时间变化，这一近似就成为精确等式。

**习题 12.8** 证明：如果价值函数不变，式（12.24）是精确的。为少写一些符号，考虑 \(t=0\) 的情形，并记 \(V_k\doteq\hat v(S_k,\mathbf w)\)。 □

**习题 12.9** 一般异策略回报的截断版本记为 \(G_{t:h}^{\lambda s}\)。根据式（12.24），猜测正确的方程。 □

式（12.24）给出的 \(\lambda\)-回报形式便于用于前向视角的更新：

\[
\begin{aligned}
\mathbf w_{t+1}
&=\mathbf w_t+\alpha\bigl(G_t^{\lambda s}-\hat v(S_t,\mathbf w_t)\bigr)\nabla\hat v(S_t,\mathbf w_t)\\
&\approx\mathbf w_t+\alpha\rho_t\left(\sum_{k=t}^{\infty}\delta_k^s\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i\right)\nabla\hat v(S_t,\mathbf w_t).
\end{aligned}
\]

对熟悉资格迹的读者来说，这看起来很像基于资格迹的 TD 更新：括号中的乘积类似资格迹，随后乘以 TD 误差。但这只是前向视角中一个时间步的更新。我们真正要建立的关系是：把前向视角的更新随时间求和，得到的量近似等于把后向视角的更新随时间求和（这里仍是近似关系，因为我们再次忽略了价值函数的变化）。
