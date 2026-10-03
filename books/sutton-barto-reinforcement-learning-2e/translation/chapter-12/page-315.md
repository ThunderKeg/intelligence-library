其中，\(\delta_t^s\)、\(\mathbf z_t\) 和 \(\rho_t\) 分别按状态价值情形的通常方式定义（式（12.23）、（12.25）、（11.1））；此外，

\[
\mathbf v_{t+1}\doteq\mathbf v_t+\beta\delta_t^s\mathbf z_t-\beta(\mathbf v_t^\top\mathbf x_t)\mathbf x_t, \tag{12.30}
\]

与 §11.7 一样，\(\mathbf v\in\mathbb R^d\) 的维数与 \(\mathbf w\) 相同，初始值为 \(\mathbf v_0=\mathbf 0\)；\(\beta>0\) 是第二个步长参数。

**GQ(\(\lambda\))** 是用于动作价值、带资格迹的梯度 TD 算法。它的目标是从异策略数据中学得参数 \(\mathbf w_t\)，使 \(\hat q(s,a,\mathbf w_t)\doteq\mathbf w_t^\top\mathbf x(s,a)\approx q_\pi(s,a)\)。如果目标策略是 \(\epsilon\)-贪心的，或者以其他方式偏向 \(\hat q\) 的贪心策略，GQ(\(\lambda\)) 也可以用作控制算法。其更新式为

\[
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t^a\mathbf z_t
-\alpha\gamma_{t+1}(1-\lambda_{t+1})(\mathbf z_t^\top\mathbf v_t)\bar{\mathbf x}_{t+1},
\]

其中 \(\bar{\mathbf x}_t\) 是目标策略在状态 \(S_t\) 下的平均特征向量：

\[
\bar{\mathbf x}_t\doteq\sum_a\pi(a\mid S_t)\mathbf x(S_t,a).
\]

\(\delta_t^a\) 是 TD 误差的期望形式，可写成

\[
\delta_t^a\doteq R_{t+1}+\gamma_{t+1}\mathbf w_t^\top\bar{\mathbf x}_{t+1}-\mathbf w_t^\top\mathbf x_t.
\]

\(\mathbf z_t\) 按动作价值的通常方式定义（式（12.29））；其余部分与 GTD(\(\lambda\)) 相同，包括 \(\mathbf v_t\) 的更新式（12.30）。

**HTD(\(\lambda\))** 是一种混合状态价值算法，结合了 GTD(\(\lambda\)) 和 TD(\(\lambda\)) 的特点。它最吸引人的性质是：它真正把 TD(\(\lambda\)) 推广到异策略学习。也就是说，若行为策略恰好与目标策略相同，HTD(\(\lambda\)) 就退化为 TD(\(\lambda\))；GTD(\(\lambda\)) 并不具备这一性质。这很有吸引力，因为两个算法都收敛时，TD(\(\lambda\)) 往往比 GTD(\(\lambda\)) 更快，而且 TD(\(\lambda\)) 只须设置一个步长。HTD(\(\lambda\)) 定义为

\[
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t^s\mathbf z_t
+\alpha\bigl((\mathbf z_t-\mathbf z_t^b)^\top\mathbf v_t\bigr)(\mathbf x_t-\gamma_{t+1}\mathbf x_{t+1}),
\]

\[
\mathbf v_{t+1}\doteq\mathbf v_t+\beta\delta_t^s\mathbf z_t
-\beta\bigl((\mathbf z_t^b)^\top\mathbf v_t\bigr)(\mathbf x_t-\gamma_{t+1}\mathbf x_{t+1}),\qquad\mathbf v_0\doteq\mathbf 0,
\]

\[
\mathbf z_t\doteq\rho_t(\gamma_t\lambda_t\mathbf z_{t-1}+\mathbf x_t),\qquad\mathbf z_{-1}\doteq\mathbf 0,
\]

\[
\mathbf z_t^b\doteq\gamma_t\lambda_t\mathbf z_{t-1}^b+\mathbf x_t,\qquad\mathbf z_{-1}^b\doteq\mathbf 0,
\]

其中 \(\beta>0\) 同样是第二个步长参数。除了第二组权重 \(\mathbf v_t\)，HTD(\(\lambda\)) 还有第二组资格迹 \(\mathbf z_t^b\)。它们是行为策略下的传统累积资格迹；如果所有 \(\rho_t\) 都为 \(1\)，它们就等于 \(\mathbf z_t\)，使 \(\mathbf w_t\) 更新式的最后一项为零，整个更新退化为 TD(\(\lambda\))。

**强调 TD(\(\lambda\))** 把单步强调 TD 算法（§9.11、§11.8）扩展到资格迹。得到的算法允许任意程度的自举，并保留很强的异策略收敛保证，代价是方差较高且收敛可能缓慢。
