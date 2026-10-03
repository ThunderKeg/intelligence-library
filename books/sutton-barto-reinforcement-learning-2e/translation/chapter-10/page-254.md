:::source-box

### 持续性问题中折扣的徒劳

也许可以尝试挽救折扣式设定：选取一个目标，把折扣价值按策略下各状态的出现分布加总：

$$
J(\pi)=\sum_s\mu_\pi(s)v_\pi^\gamma(s)
$$

这里 \(v_\pi^\gamma\) 是折扣价值函数。由贝尔曼方程，

$$
=\sum_s\mu_\pi(s)\sum_a\pi(a\mid s)\sum_{s'}\sum_r p(s',r\mid s,a)\bigl[r+\gamma v_\pi^\gamma(s')\bigr]
$$

再由式（10.7），

$$
=r(\pi)+\gamma\sum_s\mu_\pi(s)\sum_a\pi(a\mid s)\sum_{s'}\sum_r p(s',r\mid s,a)v_\pi^\gamma(s')
$$

由式（3.4），

$$
=r(\pi)+\gamma\sum_{s'}v_\pi^\gamma(s')\sum_s\mu_\pi(s)\sum_a\pi(a\mid s)p(s'\mid s,a)
$$

由式（10.8），

$$
=r(\pi)+\gamma\sum_{s'}v_\pi^\gamma(s')\mu_\pi(s')
$$

$$
=r(\pi)+\gamma J(\pi)
$$

$$
=r(\pi)+\gamma r(\pi)+\gamma^2J(\pi)
$$

$$
=r(\pi)+\gamma r(\pi)+\gamma^2r(\pi)+\gamma^3r(\pi)+\cdots
$$

$$
=\frac{1}{1-\gamma}r(\pi).
$$

这个提出的折扣目标与无折扣（平均奖励）目标对策略的排序完全相同。折扣率 \(\gamma\) 不影响排序！

:::end-source-box

我们就失去了这一保证！

事实上，缺少策略改进定理也是总回报式回合任务和平均奖励设定在理论上的一处缺口。一旦引入函数近似，就无法在任何设定中保证改进。第 13 章将介绍另一类基于参数化策略的强化学习算法；在那里，有一个称为“策略梯度定理”的理论保证，发挥着与策略改进定理相似的作用。但对于学习动作价值的方法，目前似乎缺少局部改进保证（Perkins 和 Precup，2003 年，采用的方法可能提供部分答案）。我们知道，\(\epsilon\)-贪心化有时会得到较差的策略：策略可能在若干较好的策略之间反复跳变，而不是收敛（Gordon，1996a）。这里仍有多个尚待解决的理论问题。
