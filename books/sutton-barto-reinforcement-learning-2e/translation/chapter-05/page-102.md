因此，根据策略改进定理，π′ ≥ π（即对所有 s ∈ S，\(v_{\pi'}(s)\) ≥ \(v_\pi(s)\)）。下面我们证明，只有当 π′ 和 π 都是 ε-软策略中的最优策略时，等号才可能成立；也就是说，它们都不差于任何其他 ε-软策略。

考虑一个与原环境基本相同的新环境，只是把“策略必须是 ε-软策略”这一要求“移到”环境内部。新环境与原环境有相同的状态集和行动集，行为方式如下：在状态 s 采取行动 a 时，新环境以概率 1−ε 表现得与原环境完全一样；以概率 ε，先等概率地重新随机选取一个行动，再按这个新行动在原环境中的方式运行。在这个新环境里使用一般策略所能取得的最优结果，与在原环境中使用 ε-软策略所能取得的最优结果相同。设 \(\tilde v_*\) 和 \(\tilde q_*\) 为新环境的最优价值函数。那么，策略 π 在 ε-软策略中最优，当且仅当 \(v_\pi\) = \(\tilde v_*\)。我们知道，\(\tilde v_*\) 是采用改变后转移概率的贝尔曼最优方程（3.19）的唯一解：

\[
\begin{aligned}
\tilde v_*(s)
&=\max_a\sum_{s',r}
\left[(1-\varepsilon)p(s',r\mid s,a)
+\sum_{a'}\frac{\varepsilon}{|\mathcal A(s)|}p(s',r\mid s,a')\right]
\left[r+\gamma\tilde v_*(s')\right]\\
&=(1-\varepsilon)\max_a\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma\tilde v_*(s')\right]\\
&\quad+\frac{\varepsilon}{|\mathcal A(s)|}
\sum_a\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma\tilde v_*(s')\right].
\end{aligned}
\]

当等号成立，ε-软策略 π 不再得到改进时，由式（5.2）还可得

\[
\begin{aligned}
v_\pi(s)
&=(1-\varepsilon)\max_a q_\pi(s,a)
+\frac{\varepsilon}{|\mathcal A(s)|}\sum_a q_\pi(s,a)\\
&=(1-\varepsilon)\max_a\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma v_\pi(s')\right]\\
&\quad+\frac{\varepsilon}{|\mathcal A(s)|}
\sum_a\sum_{s',r}p(s',r\mid s,a)
\left[r+\gamma v_\pi(s')\right].
\end{aligned}
\]

然而，除用 \(v_\pi\) 替换 \(\tilde v_*\) 外，这个方程与前一个方程完全相同。由于 \(\tilde v_*\) 是唯一的解，必有 \(v_\pi\) = \(\tilde v_*\)。

概括起来，前几页已经表明，策略迭代对 ε-软策略同样有效。只要采用适合 ε-软策略的贪心策略概念，每一步就都能得到改进，除非已经找到 ε-软策略中的最优策略。这个分析与每一步如何求出动作价值函数无关，但它假定这些函数都被精确求出。这使我们到达了与上一节大致相同的位置：现在只能求得 ε-软策略中最好的策略，但也去掉了探索性起点假设。
