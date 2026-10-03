## 5.9 *逐决策重要性采样

在异策略重要性采样中，还可以用另一种方式利用“回报是奖励之和”这一结构：即使没有折扣（也就是 \(\gamma=1\)），它也可能降低方差。在异策略估计量（5.5）和（5.6）中，分子的求和项本身也是一个和：

\[
\rho_{t:T-1}G_t
=\rho_{t:T-1}\left(R_{t+1}+\gamma R_{t+2}+\cdots+\gamma^{T-t-1}R_T\right)
=\rho_{t:T-1}R_{t+1}+\gamma\rho_{t:T-1}R_{t+2}+\cdots+\gamma^{T-t-1}\rho_{t:T-1}R_T.
\tag{5.11}
\]

异策略估计量依赖这些项的期望值，而它们可以写得更简单。注意，式（5.11）的每一项都是一个随机奖励与一个随机重要性采样比率的乘积。例如，按式（5.3），第一项可以写成

\[
\rho_{t:T-1}R_{t+1}
=\frac{\pi(A_t\mid S_t)}{b(A_t\mid S_t)}
\frac{\pi(A_{t+1}\mid S_{t+1})}{b(A_{t+1}\mid S_{t+1})}
\frac{\pi(A_{t+2}\mid S_{t+2})}{b(A_{t+2}\mid S_{t+2})}
\cdots
\frac{\pi(A_{T-1}\mid S_{T-1})}{b(A_{T-1}\mid S_{T-1})}R_{t+1}.
\tag{5.12}
\]

在这些因子中，可能只有第一个和最后一个（奖励）相互关联；其余因子都对应奖励之后才发生的事件。而且，这些其余因子每个的期望都是 1：

\[
\mathbb E\left[\frac{\pi(A_k\mid S_k)}{b(A_k\mid S_k)}\right]
=\sum_a b(a\mid S_k)\frac{\pi(a\mid S_k)}{b(a\mid S_k)}
=\sum_a\pi(a\mid S_k)=1.
\tag{5.13}
\]

再经过几步可以证明，正如所猜想的，其余因子在期望意义下都没有影响。换句话说，

\[
\mathbb E\left[\rho_{t:T-1}R_{t+1}\right]
=\mathbb E\left[\rho_{t:t}R_{t+1}\right].
\tag{5.14}
\]

若对式（5.11）的第 \(k\) 项重复这个过程，就得到

\[
\mathbb E\left[\rho_{t:T-1}R_{t+k}\right]
=\mathbb E\left[\rho_{t:t+k-1}R_{t+k}\right].
\]

因此，原式（5.11）的期望可以写成

\[
\mathbb E\left[\rho_{t:T-1}G_t\right]
=\mathbb E\left[\tilde G_t\right],
\]

其中

\[
\tilde G_t
=\rho_{t:t}R_{t+1}
+\gamma\rho_{t:t+1}R_{t+2}
+\gamma^2\rho_{t:t+2}R_{t+3}
+\cdots
+\gamma^{T-t-1}\rho_{t:T-1}R_T.
\]

我们称这种思路为逐决策重要性采样（per-decision importance sampling）。
