## 13.6 持续性问题的策略梯度

如 §10.3 所述，对没有回合边界的持续性问题，需要用每个时间步的平均奖励率定义表现：

\[
\begin{aligned}
J(\boldsymbol\theta)\doteq r(\pi)
&\doteq\lim_{h\to\infty}\frac1h\sum_{t=1}^{h}\mathbb E[R_t\mid S_0,A_{0:t-1}\sim\pi]\\
&=\lim_{t\to\infty}\mathbb E[R_t\mid S_0,A_{0:t-1}\sim\pi]\\
&=\sum_s\mu(s)\sum_a\pi(a\mid s)\sum_{s',r}p(s',r\mid s,a)r.
\end{aligned} \tag{13.15}
\]

其中 \(\mu\) 是策略 \(\pi\) 下的稳态分布：\(\mu(s)\doteq\lim_{t\to\infty}\Pr\{S_t=s\mid A_{0:t}\sim\pi\}\)。这里假设它存在且不依赖 \(S_0\)（遍历性假设）。回想这一分布有个特殊性质：若从它出发并按 \(\pi\) 选择行动，状态分布会保持不变：

\[
\sum_s\mu(s)\sum_a\pi(a\mid s,\boldsymbol\theta)p(s'\mid s,a)=\mu(s'),\qquad\text{对所有 }s'\in\mathcal S. \tag{13.16}
\]

持续性情形下行动者—评论家算法（后向视角）的完整伪代码见下方方框。

:::algorithm

### 带资格迹的行动者—评论家（持续性）：估计 \(\pi_{\boldsymbol\theta}\approx\pi_*\)

输入：可微的策略参数化 \(\pi(a\mid s,\boldsymbol\theta)\)。

输入：可微的状态价值函数参数化 \(\hat v(s,\mathbf w)\)。

算法参数：\(\lambda^w\in[0,1]\)、\(\lambda^\theta\in[0,1]\)；\(\alpha^w>0\)、\(\alpha^\theta>0\)、\(\alpha^{\bar R}>0\)。

初始化 \(\bar R\in\mathbb R\)（例如为 \(0\)）。

初始化状态价值权重 \(\mathbf w\in\mathbb R^d\) 和策略参数 \(\boldsymbol\theta\in\mathbb R^{d'}\)（例如都设为 \(0\)）。

初始化 \(S\in\mathcal S\)（例如 \(s_0\)）。

$$
\mathbf z^w\leftarrow\mathbf0\quad(d\text{ 维资格迹向量})
$$

$$
\mathbf z^\theta\leftarrow\mathbf0\quad(d'\text{ 维资格迹向量})
$$

无限循环（每个时间步一次）：

$$
A\sim\pi(\cdot\mid S,\boldsymbol\theta)
$$

　执行行动 \(A\)，观察 \(S',R\)。

$$
\delta\leftarrow R-\bar R+\hat v(S',\mathbf w)-\hat v(S,\mathbf w)
$$

$$
\bar R\leftarrow\bar R+\alpha^{\bar R}\delta
$$

$$
\mathbf z^w\leftarrow\lambda^w\mathbf z^w+\nabla\hat v(S,\mathbf w)
$$

$$
\mathbf z^\theta\leftarrow\lambda^\theta\mathbf z^\theta+\nabla\ln\pi(A\mid S,\boldsymbol\theta)
$$

$$
\mathbf w\leftarrow\mathbf w+\alpha^w\delta\mathbf z^w
$$

$$
\boldsymbol\theta\leftarrow\boldsymbol\theta+\alpha^\theta\delta\mathbf z^\theta
$$

$$
S\leftarrow S'
$$

:::end-algorithm
