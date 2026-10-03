这种做法的价值是

\[
\begin{aligned}
q_\pi(s,a)&\doteq\mathbb E[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s,A_t=a]\\
&=\sum_{s',r}p(s',r\mid s,a)\bigl[r+\gamma v_\pi(s')\bigr].
\end{aligned}\tag{4.6}
\]

关键是判断它比 \(v_\pi(s)\) 大还是小。如果它更大，也就是说，在状态 \(s\) 先选择一次 \(a\)、随后遵循 \(\pi\)，比始终遵循 \(\pi\) 更好，那么可以预期每次遇到 \(s\) 都选择 \(a\) 会更好，而新策略整体上也会更好。

这一判断成立，是一般性结果**策略改进定理**（policy improvement theorem）的一个特例。设 \(\pi\) 和 \(\pi'\) 是任意两个确定性策略，且对所有 \(s\in\mathcal S\) 都有

\[
q_\pi(s,\pi'(s))\ge v_\pi(s).\tag{4.7}
\]

那么 \(\pi'\) 至少与 \(\pi\) 一样好：从每个 \(s\in\mathcal S\) 出发，它得到的期望回报大于或等于 \(\pi\) 的，即

\[
v_{\pi'}(s)\ge v_\pi(s).\tag{4.8}
\]

此外，只要式（4.7）在某个状态是严格不等式，式（4.8）在同一状态也必为严格不等式。

本节开头考虑的两个策略正适用这一定理：原确定性策略 \(\pi\)，以及除 \(\pi'(s)=a\ne\pi(s)\) 之外与 \(\pi\) 完全相同的改变后策略 \(\pi'\)。在 \(s\) 以外的状态，式（4.7）两边相等。因此，如果 \(q_\pi(s,a)>v_\pi(s)\)，改变后的策略确实比 \(\pi\) 更好。

策略改进定理背后的证明思路并不难。由式（4.7）出发，反复用式（4.6）展开 \(q_\pi\) 一侧，再应用式（4.7），直到得到 \(v_{\pi'}(s)\)：

\[
\begin{aligned}
v_\pi(s)
&\le q_\pi(s,\pi'(s))\\
&=\mathbb E[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s,A_t=\pi'(s)]&&\text{（由式 4.6）}\\
&=\mathbb E_{\pi'}[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s]\\
&\le\mathbb E_{\pi'}[R_{t+1}+\gamma q_\pi(S_{t+1},\pi'(S_{t+1}))\mid S_t=s]&&\text{（由式 4.7）}\\
&=\mathbb E_{\pi'}[R_{t+1}+\gamma\mathbb E[R_{t+2}+\gamma v_\pi(S_{t+2})\mid S_{t+1},A_{t+1}=\pi'(S_{t+1})]\mid S_t=s]\\
&=\mathbb E_{\pi'}[R_{t+1}+\gamma R_{t+2}+\gamma^2v_\pi(S_{t+2})\mid S_t=s]\\
&\le\mathbb E_{\pi'}[R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\gamma^3v_\pi(S_{t+3})\mid S_t=s]\\
&\ \vdots\\
&\le\mathbb E_{\pi'}[R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\gamma^3R_{t+4}+\cdots\mid S_t=s]\\
&=v_{\pi'}(s).
\end{aligned}
\]

到目前为止，我们看到：给定一个策略及其价值函数，就能轻松评估只在一个状态改变策略的效果。自然可以进一步考虑在所有状态改变策略。
