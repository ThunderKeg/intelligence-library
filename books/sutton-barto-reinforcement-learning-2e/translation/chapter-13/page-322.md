## 13.1　策略近似及其优势

在策略梯度方法中，策略可以用任何方式参数化，只要 \(\pi(a\mid s,\boldsymbol\theta)\) 对参数可微。也就是说，对于所有 \(s\in\mathcal S\)、\(a\in\mathcal A(s)\) 和 \(\boldsymbol\theta\in\mathbb R^{d'}\)，\(\nabla\pi(a\mid s,\boldsymbol\theta)\) 都存在且有限；它是由 \(\pi(a\mid s,\boldsymbol\theta)\) 对 \(\boldsymbol\theta\) 各分量的偏导数组成的列向量。实践中，为保证探索，我们通常要求策略永远不会变成确定性策略，即对所有 \(s,a,\boldsymbol\theta\)，都有 \(\pi(a\mid s,\boldsymbol\theta)\in(0,1)\)。本节介绍离散行动空间最常用的参数化方式，并指出它相对于行动价值方法的优势。基于策略的方法也为处理连续行动空间提供了有用的途径，见第 13.7 节。

如果行动空间离散且规模不太大，一种自然且常见的参数化方式是，为每个状态—行动对构造参数化的数值型**行动偏好** \(h(s,a,\boldsymbol\theta)\in\mathbb R\)。在每个状态下，偏好最高的行动获得最高的选择概率。例如，可使用指数 softmax 分布：

$$
\pi(a\mid s,\boldsymbol\theta)\doteq
\frac{e^{h(s,a,\boldsymbol\theta)}}{\sum_b e^{h(s,b,\boldsymbol\theta)}}. \tag{13.2}
$$

其中，\(e\approx2.71828\) 是自然对数的底。分母恰好使每个状态下的行动概率之和为一。我们把这种策略参数化称为**对行动偏好做 softmax**。

行动偏好本身可以任意参数化。例如，可以由深度人工神经网络（ANN）计算，\(\boldsymbol\theta\) 则是网络所有连接权重组成的向量，第 16.6 节所述的 AlphaGo 系统即采用这种方式。偏好也可以只是特征的线性函数：

$$
h(s,a,\boldsymbol\theta)=\boldsymbol\theta^\top\mathbf x(s,a), \tag{13.3}
$$

其中，特征向量 \(\mathbf x(s,a)\in\mathbb R^{d'}\) 可用第 9.5 节介绍的任一方法构造。

按行动偏好做 softmax 来参数化策略，一个优势是近似策略可以趋近确定性策略；而对行动价值使用 \(\varepsilon\)-贪心选择时，总有 \(\varepsilon\) 的概率随机选择行动。当然，也可以根据行动价值使用 softmax 分布，但仅此仍不足以使策略趋近确定性策略。行动价值估计会收敛到相应的真实价值，而这些价值之间的差距是有限的，因此得到的选择概率会是某些既非 0 也非 1 的值。如果 softmax 分布包含温度参数，可以随时间降低温度以趋近确定性；但在实践中，要选定降温计划，甚至初始温度，都需要比我们愿意假定的更多关于真实行动价值的先验知识。行动偏好则不同：它们并不趋近某些特定数值，而是被推动着产生最优随机策略。如果最优策略是确定性的，那么只要参数化方式允许，最优行动的偏好就会被推得无限高于所有次优行动。
