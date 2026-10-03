前向视角的更新随时间求和为

\[
\begin{aligned}
\sum_{t=0}^{\infty}(\mathbf w_{t+1}-\mathbf w_t)
&\approx\sum_{t=0}^{\infty}\sum_{k=t}^{\infty}\alpha\rho_t\delta_k^s\nabla\hat v(S_t,\mathbf w_t)\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i\\
&=\sum_{k=0}^{\infty}\sum_{t=0}^{k}\alpha\rho_t\nabla\hat v(S_t,\mathbf w_t)\delta_k^s\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i\\
&=\sum_{k=0}^{\infty}\alpha\delta_k^s\sum_{t=0}^{k}\rho_t\nabla\hat v(S_t,\mathbf w_t)\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i.
\end{aligned}
\]

第二行交换了求和顺序，使用规则 \(\sum_{t=x}^{y}\sum_{k=t}^{y}=\sum_{k=x}^{y}\sum_{t=x}^{k}\)。如果从第二次求和开始的整个表达式能够写成资格迹，并能增量更新，上式就具有后向视角 TD 更新求和的形式。现在证明这确实可以做到：若把该表达式记为时刻 \(k\) 的迹，就能根据时刻 \(k-1\) 的值更新它：

\[
\begin{aligned}
\mathbf z_k
&=\sum_{t=0}^{k}\rho_t\nabla\hat v(S_t,\mathbf w_t)\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i\\
&=\sum_{t=0}^{k-1}\rho_t\nabla\hat v(S_t,\mathbf w_t)\prod_{i=t+1}^{k}\gamma_i\lambda_i\rho_i+\rho_k\nabla\hat v(S_k,\mathbf w_k)\\
&=\gamma_k\lambda_k\rho_k\underbrace{\sum_{t=0}^{k-1}\rho_t\nabla\hat v(S_t,\mathbf w_t)\prod_{i=t+1}^{k-1}\gamma_i\lambda_i\rho_i}_{\mathbf z_{k-1}}+\rho_k\nabla\hat v(S_k,\mathbf w_k)\\
&=\rho_k\bigl(\gamma_k\lambda_k\mathbf z_{k-1}+\nabla\hat v(S_k,\mathbf w_k)\bigr).
\end{aligned}
\]

把下标 \(k\) 改为 \(t\)，便得到状态价值的一般**累积迹**更新式：

\[
\mathbf z_t\doteq\rho_t\bigl(\gamma_t\lambda_t\mathbf z_{t-1}+\nabla\hat v(S_t,\mathbf w_t)\bigr). \tag{12.25}
\]

该资格迹与 TD(\(\lambda\)) 通常的半梯度参数更新规则（12.7）相结合，构成可用于同策略或异策略数据的一般 TD(\(\lambda\)) 算法。在同策略情形，它恰好就是 TD(\(\lambda\))：因为 \(\rho_t\) 恒为 \(1\)，式（12.25）退化为通常的累积迹式（12.5）（扩展到可变 \(\lambda\) 与 \(\gamma\)）。在异策略情形，这个算法通常表现不错；但它是半梯度方法，因而不能保证稳定。接下来的几节会考虑使其稳定的扩展。

用非常相似的一系列步骤，可以推导出动作价值方法的异策略资格迹，以及相应的一般 Sarsa(\(\lambda\)) 算法。可以从一般基于行动的 \(\lambda\)-回报的两种递归形式（12.19）或（12.20）中的任一种开始，但后一种（预期 Sarsa 形式）得到的结果更简洁。我们依照式（7.14）的形式，把式（12.20）扩展到异策略情形，得到
