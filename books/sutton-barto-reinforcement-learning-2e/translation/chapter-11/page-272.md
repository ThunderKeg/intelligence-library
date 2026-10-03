A 分叉示例使用表格型表示，真实状态价值本来可以精确表示；但朴素残差梯度算法找到的价值不同，而且其 \(\overline{\mathrm{TDE}}\) 比真实价值更低。最小化 \(\overline{\mathrm{TDE}}\) 的想法很朴素：它惩罚所有 TD 误差，得到的效果更像是时间上的平滑，而不是准确预测。

看起来，更好的主意是最小化均方贝尔曼误差 \(\overline{\mathrm{BE}}\)。如果学到了精确价值，每个状态的贝尔曼误差都为零。因此，最小化贝尔曼误差的算法应该能够轻松解决 A 分叉示例。一般情形下，我们不能指望贝尔曼误差为零，因为那需要找到真实价值函数，而我们假定真实价值函数不在可表示函数空间中。不过，尽量接近这一理想仍似乎是自然的目标。如前所见，贝尔曼误差也与 TD 误差密切相关：一个状态的贝尔曼误差，就是该状态中 TD 误差的期望。因此，我们把上面的推导改用期望 TD 误差再做一次（以下各期望都隐含以 \(S_t\) 为条件）：

$$
\begin{aligned}
\mathbf w_{t+1}
&=\mathbf w_t-\tfrac12\alpha\nabla\bigl(\mathbb E_\pi[\delta_t]^2\bigr)\\
&=\mathbf w_t-\tfrac12\alpha\nabla\bigl(\mathbb E_b[\rho_t\delta_t]^2\bigr)\\
&=\mathbf w_t-\alpha\mathbb E_b[\rho_t\delta_t]\,
\nabla\mathbb E_b[\rho_t\delta_t]\\
&=\mathbf w_t-\alpha\mathbb E_b\!\left[
\rho_t\bigl(R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w)
-\hat v(S_t,\mathbf w)\bigr)\right]
\mathbb E_b[\rho_t\nabla\delta_t]\\
&=\mathbf w_t+\alpha\Bigl[
\mathbb E_b\!\left[\rho_t\bigl(R_{t+1}
+\gamma\hat v(S_{t+1},\mathbf w)\bigr)\right]
-\hat v(S_t,\mathbf w)\Bigr]\\
&\qquad\cdot\Bigl[\nabla\hat v(S_t,\mathbf w)
-\gamma\mathbb E_b\!\left[
\rho_t\nabla\hat v(S_{t+1},\mathbf w)\right]\Bigr].
\end{aligned}
$$

这一更新及其各种抽样方式称为*残差梯度算法*。如果在所有期望中直接使用样本值，上式几乎恰好退化为朴素残差梯度算法（式（11.23））。¹ 但这样做很朴素，因为上式中的下一个状态 \(S_{t+1}\) 出现在相乘的两个期望里。要取得这个乘积的无偏样本，需要对下一个状态独立抽样两次；但在与外部环境的正常交互中，只能得到一次样本。两个期望可以择一抽样，却不能同时抽样。

有两种方式能使残差梯度算法可行。第一种是在确定性环境中。如果到下一状态的转移是确定性的，两次样本必然相同，朴素算法便有效。第二种是从 \(S_t\) 独立抽取两个下一状态 \(S_{t+1}\) 的样本，分别用于第一个和第二个期望。与真实环境交互时，这似乎无法做到；但与模拟环境交互时可以。只需回退到前一个状态，在从第一次抽到的下一状态继续前进之前，再取得一个不同的下一状态样本。在这两种情形下，只要步长参数满足常规条件，残差梯度算法就保证收敛到 \(\overline{\mathrm{BE}}\) 的一个最小点。作为真正的 SGD 方法，这种收敛具有稳健性，适用于线性和非线性函数近似器。在线性情形中，它总收敛到唯一一个使 \(\overline{\mathrm{BE}}\) 最小的 \(\mathbf w\)。

脚注 1：对于状态价值，重要性采样比率 \(\rho_t\) 的处理仍有细微差别。在对应的动作价值情形（也是控制算法最重要的情形）中，残差梯度算法会与朴素版本完全相同。
