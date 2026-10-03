:::source-box

### 策略梯度定理的证明（回合式问题）

只需初等微积分和项的重新排列，就可以从第一原理证明策略梯度定理。为简化记号，以下均默认 \(\pi\) 是 \(\boldsymbol\theta\) 的函数，所有梯度也都对 \(\boldsymbol\theta\) 求取。首先，状态价值函数的梯度可用行动价值函数写成

$$
\nabla v_\pi(s)
=\nabla\!\left[\sum_a\pi(a\mid s)q_\pi(s,a)\right],
\qquad \text{对所有 }s\in\mathcal S
\quad\text{（习题 3.18）}.
$$

由微积分中的乘积法则，

$$
=\sum_a\left[
\nabla\pi(a\mid s)q_\pi(s,a)
+\pi(a\mid s)\nabla q_\pi(s,a)
\right].
$$

根据习题 3.19 和式（3.2），进一步得到

$$
=\sum_a\left[
\nabla\pi(a\mid s)q_\pi(s,a)
+\pi(a\mid s)\nabla
\sum_{s',r}p(s',r\mid s,a)\bigl(r+v_\pi(s')\bigr)
\right].
$$

根据式（3.4），

$$
=\sum_a\left[
\nabla\pi(a\mid s)q_\pi(s,a)
+\pi(a\mid s)\sum_{s'}p(s'\mid s,a)\nabla v_\pi(s')
\right].
$$

继续展开（unrolling），

$$
\begin{aligned}
=\sum_a\Biggl[
&\nabla\pi(a\mid s)q_\pi(s,a)
+\pi(a\mid s)\sum_{s'}p(s'\mid s,a)\\
&\quad\sum_{a'}\left[
\nabla\pi(a'\mid s')q_\pi(s',a')
+\pi(a'\mid s')\sum_{s''}p(s''\mid s',a')\nabla v_\pi(s'')
\right]\Biggr].
\end{aligned}
$$

反复展开后，

$$
=\sum_{x\in\mathcal S}\sum_{k=0}^{\infty}
\Pr(s\to x,k,\pi)\sum_a\nabla\pi(a\mid x)q_\pi(x,a).
$$

其中，\(\Pr(s\to x,k,\pi)\) 是遵循策略 \(\pi\) 从状态 \(s\) 经 \(k\) 步转移到状态 \(x\) 的概率。于是立即有

$$
\nabla J(\boldsymbol\theta)=\nabla v_\pi(s_0)
$$

$$
=\sum_s\left(\sum_{k=0}^{\infty}\Pr(s_0\to s,k,\pi)\right)
\sum_a\nabla\pi(a\mid s)q_\pi(s,a)
$$

$$
=\sum_s\eta(s)\sum_a\nabla\pi(a\mid s)q_\pi(s,a)
\qquad\text{（第 199 页方框）}
$$

$$
=\sum_{s'}\eta(s')\sum_s
\frac{\eta(s)}{\sum_{s'}\eta(s')}
\sum_a\nabla\pi(a\mid s)q_\pi(s,a)
$$

$$
=\sum_{s'}\eta(s')\sum_s\mu(s)
\sum_a\nabla\pi(a\mid s)q_\pi(s,a)
\qquad\text{（式 9.3）}
$$

$$
\propto\sum_s\mu(s)\sum_a\nabla\pi(a\mid s)q_\pi(s,a).
\qquad\text{（证毕）}
$$

:::end-source-box
