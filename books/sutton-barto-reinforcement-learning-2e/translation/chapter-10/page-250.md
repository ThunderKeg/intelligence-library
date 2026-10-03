在平均奖励设定中，回报用各次奖励与平均奖励的差来定义：

\[
G_t\doteq R_{t+1}-r(\pi)+R_{t+2}-r(\pi)+R_{t+3}-r(\pi)+\cdots. \tag{10.9}
\]

这称为**差分回报**（differential return），相应的价值函数称为**差分价值函数**。差分价值函数与传统价值函数一样，都是相应回报的期望；只是这里用新的回报取代折扣回报。因此，差分价值函数仍使用相同记号：\(v_\pi(s)\doteq\mathbb E_\pi[G_t\mid S_t=s]\) 和 \(q_\pi(s,a)\doteq\mathbb E_\pi[G_t\mid S_t=s,A_t=a]\)；\(v_*\) 和 \(q_*\) 同理。差分价值函数也满足贝尔曼方程，与前面见过的方程仅有少许差别：去掉所有 \(\gamma\)，并把每个奖励替换成该奖励与真实平均奖励之差：

\[
v_\pi(s)=\sum_a\pi(a\mid s)\sum_{r,s'}p(s',r\mid s,a)\bigl[r-r(\pi)+v_\pi(s')\bigr],
\]

\[
q_\pi(s,a)=\sum_{r,s'}p(s',r\mid s,a)\biggl[r-r(\pi)+\sum_{a'}\pi(a'\mid s')q_\pi(s',a')\biggr],
\]

\[
v_*(s)=\max_a\sum_{r,s'}p(s',r\mid s,a)\bigl[r-\max_\pi r(\pi)+v_*(s')\bigr],
\]

以及

\[
q_*(s,a)=\sum_{r,s'}p(s',r\mid s,a)\bigl[r-\max_\pi r(\pi)+\max_{a'}q_*(s',a')\bigr].
\]

可对照式（3.14）、习题 3.17、式（3.19）和式（3.20）。

两种 TD 误差也各有一个差分形式：

\[
\delta_t\doteq R_{t+1}-\bar R_t+\hat v(S_{t+1},\mathbf w_t)-\hat v(S_t,\mathbf w_t), \tag{10.10}
\]

以及

\[
\delta_t\doteq R_{t+1}-\bar R_t+\hat q(S_{t+1},A_{t+1},\mathbf w_t)-\hat q(S_t,A_t,\mathbf w_t), \tag{10.11}
\]

其中 \(\bar R_t\) 是在时刻 \(t\) 对平均奖励 \(r(\pi)\) 的估计。采用这些替代定义后，我们的大多数算法和许多理论结果都可以原样用于平均奖励设定。

例如，平均奖励版半梯度 Sarsa 可以沿用式（10.2），只把 TD 误差换成差分形式。即

\[
\mathbf w_{t+1}\doteq\mathbf w_t+\alpha\delta_t\nabla\hat q(S_t,A_t,\mathbf w_t), \tag{10.12}
\]

其中 \(\delta_t\) 由式（10.11）给出。完整算法的伪代码见下一页方框。该算法的一个局限是：它不会收敛到差分价值本身，而是收敛到与差分价值相差某个任意常数的数值。注意，把所有价值都平移同一个量，不会影响上述贝尔曼方程和 TD 误差。因此，这个偏移在实践中可能并不重要。如何修改算法来消除偏移，是值得未来研究的问题。

**习题 10.4** 给出半梯度 Q-learning 的差分版本伪代码。 □

**习题 10.5** 除式（10.10）以外，还需要哪些方程才能完整规定 TD(0) 的差分版本？ □
