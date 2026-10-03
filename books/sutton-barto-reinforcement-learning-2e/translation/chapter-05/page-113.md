这个思路的核心，是把折扣理解为一种终止概率，或等价地，部分终止的程度。对任何 \(\gamma\in[0,1)\)，可以把回报 \(G_0\) 看成以 \(1-\gamma\) 的程度在一步后部分终止，得到仅含第一个奖励 \(R_1\) 的回报；又以 \((1-\gamma)\gamma\) 的程度在两步后部分终止，得到 \(R_1+R_2\)，依此类推。后一个程度对应于第二步终止的程度 \(1-\gamma\)，乘以第一步尚未终止的程度 \(\gamma\)。因此，第三步终止的程度是 \((1-\gamma)\gamma^2\)，其中 \(\gamma^2\) 表示前两步都未终止。这里的部分回报称为无折扣部分回报（flat partial returns）：

\[
\bar G_{t:h}\doteq R_{t+1}+R_{t+2}+\cdots+R_h,
\qquad 0\le t<h\le T,
\]

其中“无折扣”表示没有折扣，“部分”表示这些回报并未一直延伸到终止，而是在称为视界（horizon）的 \(h\) 处停止（\(T\) 为该回合的终止时刻）。据此，常规完整回报 \(G_t\) 可以表示为无折扣部分回报之和：

\[
\begin{aligned}
G_t
&\doteq R_{t+1}+\gamma R_{t+2}
+\gamma^2R_{t+3}+\cdots+\gamma^{T-t-1}R_T\\
&=(1-\gamma)R_{t+1}\\
&\quad+(1-\gamma)\gamma(R_{t+1}+R_{t+2})\\
&\quad+(1-\gamma)\gamma^2(R_{t+1}+R_{t+2}+R_{t+3})\\
&\quad+\vdots\\
&\quad+(1-\gamma)\gamma^{T-t-2}
(R_{t+1}+\cdots+R_{T-1})\\
&\quad+\gamma^{T-t-1}(R_{t+1}+\cdots+R_T)\\
&=(1-\gamma)\sum_{h=t+1}^{T-1}
\gamma^{h-t-1}\bar G_{t:h}
+\gamma^{T-t-1}\bar G_{t:T}.
\end{aligned}
\]

现在需要用同样截短的重要性采样比率来缩放无折扣部分回报。由于 \(\bar G_{t:h}\) 只涉及截至视界 \(h\) 的奖励，我们只需要截至 \(h-1\) 的概率比率。类似于式（5.5），定义普通重要性采样估计量：

\[
V(s)\doteq
\frac{\displaystyle\sum_{t\in\mathcal T(s)}
\left(
(1-\gamma)\sum_{h=t+1}^{T(t)-1}
\gamma^{h-t-1}\rho_{t:h-1}\bar G_{t:h}
+\gamma^{T(t)-t-1}\rho_{t:T(t)-1}\bar G_{t:T(t)}
\right)}
{|\mathcal T(s)|}.\tag{5.9}
\]

类似于式（5.6），定义加权重要性采样估计量：

\[
V(s)\doteq
\frac{\displaystyle\sum_{t\in\mathcal T(s)}
\left(
(1-\gamma)\sum_{h=t+1}^{T(t)-1}
\gamma^{h-t-1}\rho_{t:h-1}\bar G_{t:h}
+\gamma^{T(t)-t-1}\rho_{t:T(t)-1}\bar G_{t:T(t)}
\right)}
{\displaystyle\sum_{t\in\mathcal T(s)}
\left(
(1-\gamma)\sum_{h=t+1}^{T(t)-1}
\gamma^{h-t-1}\rho_{t:h-1}
+\gamma^{T(t)-t-1}\rho_{t:T(t)-1}
\right)}.\tag{5.10}
\]

我们称这两种估计量为考虑折扣的重要性采样估计量（discounting-aware importance sampling estimators）。它们考虑折扣率；但若 \(\gamma=1\)，它们不起额外作用，与第 5.5 节的异策略估计量相同。
