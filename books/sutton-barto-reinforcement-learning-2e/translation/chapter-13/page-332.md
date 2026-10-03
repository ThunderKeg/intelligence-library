:::algorithm

### 单步行动者—评论家（回合式）：估计 \(\pi_{\boldsymbol\theta}\approx\pi_*\)

输入：可微的策略参数化 \(\pi(a\mid s,\boldsymbol\theta)\)。

输入：可微的状态价值函数参数化 \(\hat v(s,\mathbf w)\)。

参数：步长 \(\alpha^\theta>0\)、\(\alpha^w>0\)。

初始化策略参数 \(\boldsymbol\theta\in\mathbb R^{d'}\) 和状态价值权重 \(\mathbf w\in\mathbb R^d\)（例如都设为 \(0\)）。

无限循环（每个回合一次）：

　初始化 \(S\)（本回合的第一个状态）。

$$
I\leftarrow1
$$

　当 \(S\) 不是终止状态时，对每个时间步循环：

$$
A\sim\pi(\cdot\mid S,\boldsymbol\theta)
$$

　执行行动 \(A\)，观察 \(S',R\)。

$$
\delta\leftarrow R+\gamma\hat v(S',\mathbf w)-\hat v(S,\mathbf w)
$$

　若 \(S'\) 是终止状态，则 \(\hat v(S',\mathbf w)\doteq0\)。

$$
\mathbf w\leftarrow\mathbf w+\alpha^w\delta\nabla\hat v(S,\mathbf w)
$$

$$
\boldsymbol\theta\leftarrow\boldsymbol\theta+\alpha^\theta I\delta\nabla\ln\pi(A\mid S,\boldsymbol\theta)
$$

$$
I\leftarrow\gamma I
$$

$$
S\leftarrow S'
$$

:::end-algorithm

推广到 \(n\) 步方法的前向视角，再推广到 \(\lambda\)-回报算法，都很直接：只须把式（13.12）中的单步回报分别换成 \(G_{t:t+n}\) 或 \(G_t^\lambda\)。\(\lambda\)-回报算法的后向视角也很直接：按照第 12 章的模式，给行动者和评论家各用一组独立资格迹。完整算法的伪代码如下。

:::algorithm

### 带资格迹的行动者—评论家（回合式）：估计 \(\pi_{\boldsymbol\theta}\approx\pi_*\)

输入：可微的策略参数化 \(\pi(a\mid s,\boldsymbol\theta)\)。

输入：可微的状态价值函数参数化 \(\hat v(s,\mathbf w)\)。

参数：迹衰减率 \(\lambda^\theta\in[0,1]\)、\(\lambda^w\in[0,1]\)；步长 \(\alpha^\theta>0\)、\(\alpha^w>0\)。

初始化策略参数 \(\boldsymbol\theta\in\mathbb R^{d'}\) 和状态价值权重 \(\mathbf w\in\mathbb R^d\)（例如都设为 \(0\)）。

无限循环（每个回合一次）：

　初始化 \(S\)（本回合的第一个状态）。

$$
\mathbf z^\theta\leftarrow\mathbf0\quad(d'\text{ 维资格迹向量})
$$

$$
\mathbf z^w\leftarrow\mathbf0\quad(d\text{ 维资格迹向量})
$$

$$
I\leftarrow1
$$

　当 \(S\) 不是终止状态时，对每个时间步循环：

$$
A\sim\pi(\cdot\mid S,\boldsymbol\theta)
$$

　执行行动 \(A\)，观察 \(S',R\)。

$$
\delta\leftarrow R+\gamma\hat v(S',\mathbf w)-\hat v(S,\mathbf w)
$$

　若 \(S'\) 是终止状态，则 \(\hat v(S',\mathbf w)\doteq0\)。

$$
\mathbf z^w\leftarrow\gamma\lambda^w\mathbf z^w+\nabla\hat v(S,\mathbf w)
$$

$$
\mathbf z^\theta\leftarrow\gamma\lambda^\theta\mathbf z^\theta+I\nabla\ln\pi(A\mid S,\boldsymbol\theta)
$$

$$
\mathbf w\leftarrow\mathbf w+\alpha^w\delta\mathbf z^w
$$

$$
\boldsymbol\theta\leftarrow\boldsymbol\theta+\alpha^\theta\delta\mathbf z^\theta
$$

$$
I\leftarrow\gamma I
$$

$$
S\leftarrow S'
$$

:::end-algorithm
