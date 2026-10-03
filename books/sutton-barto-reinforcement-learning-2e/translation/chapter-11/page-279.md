把这三个因子的期望代入 \(\overline{\mathrm{PBE}}\) 梯度的表达式，得到

\[
\nabla\overline{\mathrm{PBE}}(\mathbf w)
=2\mathbb E[\rho_t(\gamma\mathbf x_{t+1}-\mathbf x_t)\mathbf x_t^\top]
\mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}
\mathbb E[\rho_t\delta_t\mathbf x_t]. \tag{11.27}
\]

这样写出梯度之后，进展或许并不明显。它是三个表达式的乘积，而第一个和最后一个并不独立。两者都取决于下一个特征向量 \(\mathbf x_{t+1}\)；不能简单地分别抽样这两个期望，再把样本相乘。那样会像残差梯度算法一样，得到有偏的梯度估计。

另一种办法是分别估计三个期望，再把它们组合成梯度的无偏估计。这可行，但会消耗大量计算资源，尤其是要存储前两个 \(d\times d\) 矩阵的期望，并计算第二个矩阵的逆。可以改进这种办法：如果先估计并保存三个期望中的两个，就能对第三个采样，并与保存的两个量一起使用。例如，保存后两个量的估计（使用 §9.8 的增量式逆矩阵更新技术），再对第一个表达式采样。遗憾的是，整个算法仍具有二次复杂度（\(O(d^2)\)）。

分别保存某些估计、再与样本组合，是个好思路，梯度 TD 方法也采用这一思路。梯度 TD 方法估计并保存式（11.27）后两个因子的**乘积**。这两个因子分别是一个 \(d\times d\) 矩阵和一个 \(d\) 维向量，因此其乘积只是一个 \(d\) 维向量，与 \(\mathbf w\) 一样。把这个新学习到的向量记为 \(\mathbf v\)：

\[
\mathbf v\approx\mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}\mathbb E[\rho_t\delta_t\mathbf x_t]. \tag{11.28}
\]

熟悉线性监督学习的读者会认出这一形式：它是一个线性最小二乘问题的解，试图用特征近似 \(\rho_t\delta_t\)。增量式求取使预期平方误差 \((\mathbf v^\top\mathbf x_t-\rho_t\delta_t)^2\) 最小的向量 \(\mathbf v\) 时，标准 SGD 方法称为**最小均方**（Least Mean Square，LMS）规则；这里还加入了重要性采样比：

\[
\mathbf v_{t+1}\doteq\mathbf v_t+\beta\rho_t(\delta_t-\mathbf v_t^\top\mathbf x_t)\mathbf x_t,
\]

其中 \(\beta>0\) 是另一个步长参数。这个方法能以 \(O(d)\) 的存储量和每步计算量有效近似式（11.28）。

有了近似式（11.28）的已存估计 \(\mathbf v_t\)，就可以根据式（11.27），用 SGD 更新主参数向量 \(\mathbf w_t\)。其中最简单的规则是

\[
\begin{aligned}
\mathbf w_{t+1}
&=\mathbf w_t-\tfrac12\alpha\nabla\overline{\mathrm{PBE}}(\mathbf w_t)\\
&=\mathbf w_t-\tfrac12\alpha 2\mathbb E[\rho_t(\gamma\mathbf x_{t+1}-\mathbf x_t)\mathbf x_t^\top]\mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}\mathbb E[\rho_t\delta_t\mathbf x_t]\\
&=\mathbf w_t+\alpha\mathbb E[\rho_t(\mathbf x_t-\gamma\mathbf x_{t+1})\mathbf x_t^\top]\mathbb E[\mathbf x_t\mathbf x_t^\top]^{-1}\mathbb E[\rho_t\delta_t\mathbf x_t] \tag{11.29}\\
&\approx\mathbf w_t+\alpha\mathbb E[\rho_t(\mathbf x_t-\gamma\mathbf x_{t+1})\mathbf x_t^\top]\mathbf v_t\\
&\approx\mathbf w_t+\alpha\rho_t(\mathbf x_t-\gamma\mathbf x_{t+1})\mathbf x_t^\top\mathbf v_t.
\end{aligned}
\]

第一行是一般 SGD 规则，第二行来自式（11.27），倒数第二行使用式（11.28），最后一行进行采样。
