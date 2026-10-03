## 11.7 梯度 TD 方法

现在考虑用随机梯度下降（SGD）最小化投影贝尔曼误差 \(\overline{\mathrm{PBE}}\) 的方法。作为真正的 SGD 方法，这些**梯度 TD**（Gradient-TD）方法即使采用异策略训练和非线性函数近似，也具有稳健的收敛性质。回想在线性情形中，TD 固定点 \(\mathbf w_{\mathrm{TD}}\) 始终是一个精确解，在该点 \(\overline{\mathrm{PBE}}\) 为零。这个解可以用最小二乘方法求得（§9.8），但在参数数量 \(d\) 上，只有复杂度为 \(O(d^2)\) 的方法可用。我们希望找到复杂度为 \(O(d)\)、同时具有稳健收敛性质的 SGD 方法。梯度 TD 方法接近这些目标，但计算复杂度大致增加了一倍。

为推导针对 \(\overline{\mathrm{PBE}}\) 的 SGD 方法（假设使用线性函数近似），首先把目标式（11.22）展开并改写成矩阵形式：

\[
\begin{aligned}
\overline{\mathrm{PBE}}(\mathbf w)
&=\lVert\boldsymbol\Pi\bar{\boldsymbol\delta}_{\mathbf w}\rVert_\mu^2\\
&=(\boldsymbol\Pi\bar{\boldsymbol\delta}_{\mathbf w})^\top\mathbf D\boldsymbol\Pi\bar{\boldsymbol\delta}_{\mathbf w}\\
&=\bar{\boldsymbol\delta}_{\mathbf w}^\top\boldsymbol\Pi^\top\mathbf D\boldsymbol\Pi\bar{\boldsymbol\delta}_{\mathbf w}\\
&=\bar{\boldsymbol\delta}_{\mathbf w}^\top\mathbf D\mathbf X(\mathbf X^\top\mathbf D\mathbf X)^{-1}\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w}.
\end{aligned} \tag{11.25}
\]

这里使用了式（11.13），以及恒等式 \(\boldsymbol\Pi^\top\mathbf D\boldsymbol\Pi=\mathbf D\mathbf X(\mathbf X^\top\mathbf D\mathbf X)^{-1}\mathbf X^\top\mathbf D\)。因此，

\[
\overline{\mathrm{PBE}}(\mathbf w)
=(\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w})^\top
(\mathbf X^\top\mathbf D\mathbf X)^{-1}
(\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w}). \tag{11.26}
\]

对 \(\mathbf w\) 求梯度，得到

\[
\nabla\overline{\mathrm{PBE}}(\mathbf w)
=2\nabla[\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w}]^\top
(\mathbf X^\top\mathbf D\mathbf X)^{-1}
(\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w}).
\]

要把它变成 SGD 方法，每个时间步都必须对某个量采样，且该量的期望值等于上述表达式。令 \(\mu\) 为行为策略下所访问状态的分布。上述三个因子都可以写成这一分布下的期望。例如，最后一个因子可以写成

\[
\mathbf X^\top\mathbf D\bar{\boldsymbol\delta}_{\mathbf w}
=\sum_s\mu(s)\mathbf x(s)\bar\delta_{\mathbf w}(s)
=\mathbb E[\rho_t\delta_t\mathbf x_t],
\]

这正是半梯度 TD(0) 更新（11.2）的期望。第一个因子是该更新的梯度的转置：

\[
\begin{aligned}
\nabla\mathbb E[\rho_t\delta_t\mathbf x_t]^\top
&=\mathbb E[\rho_t\nabla\delta_t^\top\mathbf x_t^\top]\\
&=\mathbb E\bigl[\rho_t\nabla(R_{t+1}+\gamma\mathbf w^\top\mathbf x_{t+1}-\mathbf w^\top\mathbf x_t)^\top\mathbf x_t^\top\bigr]\\
&=\mathbb E[\rho_t(\gamma\mathbf x_{t+1}-\mathbf x_t)\mathbf x_t^\top].
\end{aligned}
\]

第二行使用了回合式 \(\delta_t\)。最后，中间因子是特征向量外积矩阵的期望的逆：

\[
\mathbf X^\top\mathbf D\mathbf X
=\sum_s\mu(s)\mathbf x(s)\mathbf x(s)^\top
=\mathbb E[\mathbf x_t\mathbf x_t^\top].
\]
