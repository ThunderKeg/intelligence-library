自然地，在持续性情形中，我们用差分回报定义价值：\(v_\pi(s)\doteq\mathbb E_\pi[G_t\mid S_t=s]\)，\(q_\pi(s,a)\doteq\mathbb E_\pi[G_t\mid S_t=s,A_t=a]\)。差分回报为

\[
G_t\doteq R_{t+1}-r(\pi)+R_{t+2}-r(\pi)+R_{t+3}-r(\pi)+\cdots. \tag{13.17}
\]

采用这些定义后，回合式情形的策略梯度定理（式（13.5））在持续性情形中仍成立。证明见下面的方框。前向视角和后向视角的方程也保持不变。

:::source-box

### 策略梯度定理的证明（持续性情形）

持续性情形的策略梯度定理，其证明开头与回合式情形相似。仍默认 \(\pi\) 是 \(\boldsymbol\theta\) 的函数，所有梯度都是对 \(\boldsymbol\theta\) 求的。回想在持续性情形中，\(J(\boldsymbol\theta)=r(\pi)\)（式（13.15）），而 \(v_\pi\) 和 \(q_\pi\) 是相对于差分回报（式（13.17））定义的价值。对于任何 \(s\in\mathcal S\)，状态价值函数的梯度可写为

\[
\begin{aligned}
\nabla v_\pi(s)
&=\nabla\Bigl[\sum_a\pi(a\mid s)q_\pi(s,a)\Bigr],&&\text{对所有 }s\in\mathcal S\quad\text{（习题 3.18）}\\
&=\sum_a\bigl[\nabla\pi(a\mid s)q_\pi(s,a)+\pi(a\mid s)\nabla q_\pi(s,a)\bigr],&&\text{（求导的乘积法则）}\\
&=\sum_a\Bigl[\nabla\pi(a\mid s)q_\pi(s,a)+\pi(a\mid s)\nabla\sum_{s',r}p(s',r\mid s,a)\bigl(r-r(\boldsymbol\theta)+v_\pi(s')\bigr)\Bigr]\\
&=\sum_a\Bigl[\nabla\pi(a\mid s)q_\pi(s,a)+\pi(a\mid s)\Bigl(-\nabla r(\boldsymbol\theta)+\sum_{s'}p(s'\mid s,a)\nabla v_\pi(s')\Bigr)\Bigr].
\end{aligned}
\]

整理各项，得到

\[
\nabla r(\boldsymbol\theta)=\sum_a\Bigl[\nabla\pi(a\mid s)q_\pi(s,a)+\pi(a\mid s)\sum_{s'}p(s'\mid s,a)\nabla v_\pi(s')\Bigr]-\nabla v_\pi(s).
\]

注意，左边也可写成 \(\nabla J(\boldsymbol\theta)\)，它不依赖于 \(s\)。因此，右边也不依赖于 \(s\)；可以安全地对所有 \(s\in\mathcal S\) 用 \(\mu(s)\) 加权求和而不改变结果（因为 \(\sum_s\mu(s)=1\)）：

\[
\begin{aligned}
\nabla J(\boldsymbol\theta)
&=\sum_s\mu(s)\Bigl(\sum_a\bigl[\nabla\pi(a\mid s)q_\pi(s,a)+\pi(a\mid s)\sum_{s'}p(s'\mid s,a)\nabla v_\pi(s')\bigr]-\nabla v_\pi(s)\Bigr)\\
&=\sum_s\mu(s)\sum_a\nabla\pi(a\mid s)q_\pi(s,a)\\
&\quad+\sum_s\mu(s)\sum_a\pi(a\mid s)\sum_{s'}p(s'\mid s,a)\nabla v_\pi(s')-\sum_s\mu(s)\nabla v_\pi(s).
\end{aligned}
\]
