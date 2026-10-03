$$
\begin{aligned}
G_t
&\doteq R_{t+1}+\gamma_{t+1}G_{t+1}\\
&=R_{t+1}+\gamma_{t+1}R_{t+2}
+\gamma_{t+1}\gamma_{t+2}R_{t+3}
+\gamma_{t+1}\gamma_{t+2}\gamma_{t+3}R_{t+4}+\cdots\\
&=\sum_{k=t}^{\infty}\left(\prod_{i=t+1}^{k}\gamma_i\right)R_{k+1},
\end{aligned}\tag{12.17}
$$

为保证这些求和有限，要求对所有 \(t\)，\(\prod_{k=t}^{\infty}\gamma_k=0\) 以概率 1 成立。这样定义有一个方便之处：回合式问题及其算法可以表述为一条连续的经验流，不必特别引入终止状态、初始状态分布或终止时间。原来的终止状态变成一个满足 \(\gamma(s)=0\)、且随后转移到初始状态分布的状态。以这种方式（并在其他所有状态取常数 \(\gamma(\cdot)\)），就能把经典回合式问题作为特例。依状态而变的终止还包括其他预测情形，例如**伪终止（pseudo termination）**：我们希望预测某个量，却不改变马尔可夫过程本身的流动。折扣回报也可以看作这样的量；从这个角度看，依状态而变的终止统一了回合式与有折扣的持续式情形。（无折扣的持续式情形仍需要一些特殊处理。）

把自举程度推广为可变值，并不像折扣那样改变问题本身，而是改变求解策略。此推广会影响状态与行动的 \(\lambda\)-回报。新的状态型 \(\lambda\)-回报可递归地写为

$$
G_t^{\lambda s}\doteq R_{t+1}
+\gamma_{t+1}\left((1-\lambda_{t+1})\hat v(S_{t+1},\mathbf w_t)
+\lambda_{t+1}G_{t+1}^{\lambda s}\right), \tag{12.18}
$$

这里在上标 \(\lambda\) 后加上 “\(s\)”，提示这种回报从状态价值自举，以便与后面上标带 “\(a\)” 、从动作价值自举的回报区分。此式表明，\(\lambda\)-回报包含不折扣、也不受自举影响的第一笔奖励；若下一状态不发生终止，还可能包含第二项，其比例由下一状态的折扣程度决定（即由 \(\gamma_{t+1}\) 决定；若下一状态为终止状态，该值为零）。在不终止的程度上，第二项又依照该状态的自举程度分为两种情况：自举的部分取该状态的估计价值，不自举的部分取下一时间步的 \(\lambda\)-回报。基于行动的 \(\lambda\)-回报可以采用 Sarsa 形式：

$$
G_t^{\lambda a}\doteq R_{t+1}
+\gamma_{t+1}\left((1-\lambda_{t+1})\hat q(S_{t+1},A_{t+1},\mathbf w_t)
+\lambda_{t+1}G_{t+1}^{\lambda a}\right), \tag{12.19}
$$

也可以采用期望 Sarsa 形式：

$$
G_t^{\lambda a}\doteq R_{t+1}
+\gamma_{t+1}\left((1-\lambda_{t+1})\bar V_t(S_{t+1})
+\lambda_{t+1}G_{t+1}^{\lambda a}\right), \tag{12.20}
$$

其中，式（7.8）在函数近似下推广为

$$
\bar V_t(s)\doteq\sum_a\pi(a\mid s)\hat q(s,a,\mathbf w_t). \tag{12.21}
$$
