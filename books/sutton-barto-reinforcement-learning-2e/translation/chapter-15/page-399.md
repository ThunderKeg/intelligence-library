\[
\begin{aligned}
\delta_t &= R_{t+1}+\gamma\hat v(S_{t+1},\mathbf w)-\hat v(S_t,\mathbf w),\\
\mathbf z_t^{\mathbf w} &= \gamma\lambda^{\mathbf w}\mathbf z_{t-1}^{\mathbf w}+\nabla\hat v(S_t,\mathbf w),\\
\mathbf z_t^{\boldsymbol\theta} &= \gamma\lambda^{\boldsymbol\theta}\mathbf z_{t-1}^{\boldsymbol\theta}+\nabla\ln\pi(A_t\mid S_t,\boldsymbol\theta),\\
\mathbf w &\leftarrow \mathbf w+\alpha^{\mathbf w}\delta_t\mathbf z_t^{\mathbf w},\\
\boldsymbol\theta &\leftarrow \boldsymbol\theta+\alpha^{\boldsymbol\theta}\delta_t\mathbf z_t^{\boldsymbol\theta}.
\end{aligned}
\]

其中 \(\gamma\in[0,1)\) 是折扣率参数，\(\lambda^{\mathbf w}\in[0,1]\) 和 \(\lambda^{\boldsymbol\theta}\in[0,1]\) 分别是评论家与行动者的自举参数；\(\alpha^{\mathbf w}>0\) 和 \(\alpha^{\boldsymbol\theta}>0\) 是相应的步长参数。

把近似价值函数 \(\hat v\) 看作单个线性类神经元单元的输出。这个单元称为评论家单元，在图 15.5a 中标为 \(V\)。这样，价值函数就是状态 \(s\) 的特征向量表征 \(\mathbf x(s)=(x_1(s),\ldots,x_n(s))^\top\) 的线性函数，由权重向量 \(\mathbf w=(w_1,\ldots,w_n)^\top\) 参数化：

\[
\hat v(s,\mathbf w)=\mathbf w^\top\mathbf x(s). \tag{15.1}
\]

每个 \(x_i(s)\) 都类似于送往神经元某个突触的突触前信号，该突触的效能为 \(w_i\)。按照上述规则，评论家的权重增加量为 \(\alpha^{\mathbf w}\delta_t\mathbf z_t^{\mathbf w}\)；其中，强化信号 \(\delta_t\) 对应于广播到评论家单元所有突触的多巴胺信号。评论家单元的资格迹向量 \(\mathbf z_t^{\mathbf w}\)，是 \(\nabla\hat v(S_t,\mathbf w)\) 近期取值的迹（一种平均）。由于 \(\hat v(s,\mathbf w)\) 对权重是线性的，\(\nabla\hat v(S_t,\mathbf w)=\mathbf x(S_t)\)。

从神经元角度看，这意味着每个突触都有自己的资格迹，对应向量 \(\mathbf z_t^{\mathbf w}\) 的一个分量。突触资格迹按照到达该突触的活动水平累积，也就是按照突触前活动的水平累积；这里它由抵达该突触的特征向量 \(\mathbf x(S_t)\) 的相应分量表示。除此之外，资格迹以由 \(\lambda^{\mathbf w}\) 控制的速率向零衰减。只要资格迹非零，突触就有资格被修改。突触效能实际上如何改变，则取决于它保持可修改期间收到的强化信号。我们把评论家单元突触上的这种资格迹称为**非条件性资格迹**（non-contingent eligibility traces），因为它们只依赖突触前活动，丝毫不以突触后活动为条件。

评论家单元突触的非条件性资格迹，意味着评论家的学习规则实质上就是 §14.2 所述的经典条件作用 TD 模型。按这里对评论家单元及其学习规则的定义，图 15.5a 中的评论家与 Barto 等人（1983）的 ANN 行动者—评论家中的评论家相同。显然，仅由一个线性类神经元单元组成的评论家，是最简单的起点；这个单元代表一个更复杂、能够学习更复杂价值函数的神经网络。

图 15.5a 中的行动者，是由 \(k\) 个类神经元行动者单元组成的单层网络。每个单元在时刻 \(t\) 都收到与评论家单元相同的特征向量 \(\mathbf x(S_t)\)。每个行动者单元 \(j\)，\(j=1,\ldots,k\)，都有自己的权重向量 \(\boldsymbol\theta_j\)；但由于各单元相同，我们只描述其中一个，省略下标。这些单元遵循上述行动者—评论家算法的一种方式，是让每个单元成为**伯努利—logistic 单元**（Bernoulli-logistic unit）。这意味着每个时刻行动者单元的输出都是一个随机变量 \(A_t\)，取值为 0 或 1。可以把 1 理解为该神经元放电，即发出动作电位。单元输入向量的加权和 \(\boldsymbol\theta^\top\mathbf x(S_t)\)，通过指数 soft-max 分布（13.2）决定它的行动概率；对于两个行动，这就是 logistic 函数：
