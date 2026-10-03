同策略蒙特卡洛控制的总体思路仍然是 GPI。与蒙特卡洛 ES 一样，我们用首次访问 MC 方法估计当前策略的动作价值函数。然而，如果没有探索性起点假设，就不能简单地把策略改成相对于当前价值函数的贪心策略，因为这样会阻止继续探索非贪心行动。幸运的是，GPI 并不要求将策略一直改到贪心策略，只要求它朝贪心策略的方向移动。在我们的同策略方法中，只把策略移动到一个 ε-贪心策略。对于任何 ε-软策略 π，相对于 \(q_\pi\) 的任意 ε-贪心策略都保证不差于 π。完整算法如下。

**同策略首次访问 MC 控制（用于 ε-软策略），估计 \(\pi\approx\pi_*\)**

```text
算法参数：小的 ε > 0
初始化：
    π ← 任意 ε-软策略
    对所有 s ∈ S、a ∈ A(s)，任意设定 Q(s,a) ∈ ℝ
    对所有 s ∈ S、a ∈ A(s)，令 Returns(s,a) 为空列表
无限重复（每回合一次）：
    按 π 生成一个回合：S₀,A₀,R₁,…,S_{T−1},A_{T−1},R_T
    G ← 0
    对回合中每一步，按 t = T−1,T−2,…,0 的顺序循环：
        G ← γG + R_{t+1}
        如果状态—动作对 (S_t,A_t) 未出现在此前的 S₀,A₀,S₁,A₁,…,S_{t−1},A_{t−1} 中：
            将 G 追加到 Returns(S_t,A_t)
            Q(S_t,A_t) ← average(Returns(S_t,A_t))
            A* ← arg max_a Q(S_t,a)    （并列时任意选一个）
            对所有 a ∈ A(S_t)：
                如果 a = A*，π(a|S_t) ← 1−ε+ε/|A(S_t)|
                否则，π(a|S_t) ← ε/|A(S_t)|
```

策略改进定理保证：相对于 \(q_\pi\) 的任意 ε-贪心策略，都不差于任意 ε-软策略 π。令 π′ 为这一 ε-贪心策略。对于任意 s ∈ S，策略改进定理的条件成立，因为：

\[
\begin{aligned}
q_\pi\bigl(s,\pi'(s)\bigr)
&=\sum_a\pi'(a\mid s)q_\pi(s,a)\\
&=\frac{\varepsilon}{|\mathcal A(s)|}\sum_a q_\pi(s,a)
 +(1-\varepsilon)\max_a q_\pi(s,a)\\
&\ge\frac{\varepsilon}{|\mathcal A(s)|}\sum_a q_\pi(s,a)
 +(1-\varepsilon)\sum_a
 \frac{\pi(a\mid s)-\varepsilon/|\mathcal A(s)|}{1-\varepsilon}q_\pi(s,a).
\end{aligned}\tag{5.2}
\]

这里的求和是以非负权重进行的加权平均，权重之和为 1，所以其结果必定不大于参与平均的最大值。

\[
\begin{aligned}
&=\frac{\varepsilon}{|\mathcal A(s)|}\sum_a q_\pi(s,a)
-\frac{\varepsilon}{|\mathcal A(s)|}\sum_a q_\pi(s,a)
+\sum_a\pi(a\mid s)q_\pi(s,a)\\
&=v_\pi(s).
\end{aligned}
\]
