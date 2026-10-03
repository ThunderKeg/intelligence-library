\[
\hat v(s,\mathbf w)=\mathbf w^\top\mathbf x(s)=\sum_{i=1}^{d}w_i x_i(s). \tag{9.8}
\]

在这种情况下，近似价值函数对权重是**线性的**，简称线性价值函数。

向量 \(\mathbf x(s)\) 称为表示状态 \(s\) 的**特征向量（feature vector）**。它的每个分量 \(x_i(s)\) 都是函数 \(x_i:\mathcal S\to\mathbb R\) 在状态 \(s\) 上的值。这里把整个函数称为一个**特征（feature）**，把它对某一状态的函数值称为该状态的一个特征值。在线性方法中，这些特征也是**基函数（basis functions）**，因为它们构成近似函数集合的一组线性基。为状态构造 \(d\) 维特征向量，等价于选取 \(d\) 个基函数。特征可以有多种定义方式；后续各节会介绍一些做法。

将 SGD 更新用于线性函数近似很自然。此时近似价值函数对 \(\mathbf w\) 的梯度为

\[
\nabla\hat v(s,\mathbf w)=\mathbf x(s).
\]

所以，在线性情况下，一般的 SGD 更新式（9.7）化为十分简单的形式：

\[
\mathbf w_{t+1}=\mathbf w_t+\alpha\big[U_t-\hat v(S_t,\mathbf w_t)\big]\mathbf x(S_t).
\]

因为形式简单，线性 SGD 是最适合做数学分析的情况之一。各类学习系统几乎所有有用的收敛结果，都是针对线性或更简单的函数近似方法得到的。

尤其是，在线性情况下，最优解只有一个；退化情况下，也只有一组同样好的最优解。因此，凡是保证收敛到局部最优解或其附近的方法，也就保证收敛到全局最优解或其附近。例如，上一节给出的梯度蒙特卡洛算法，在使用线性函数近似、并按通常条件逐渐减小 \(\alpha\) 时，会收敛到均方价值误差 \(\overline{\mathrm{VE}}\) 的全局最优解。

上一节的半梯度 TD(0) 算法在线性函数近似下也会收敛，但这不能由 SGD 的一般结果推出，而需要单独的定理。它收敛到的权重向量也不是全局最优解，而是局部最优解附近的一点。这个重要情况值得进一步考察，下面具体讨论持续性任务。每个时刻 \(t\) 的更新是

\[
\begin{aligned}
\mathbf w_{t+1}
&=\mathbf w_t+\alpha\big(R_{t+1}+\gamma\mathbf w_t^\top\mathbf x_{t+1}-\mathbf w_t^\top\mathbf x_t\big)\mathbf x_t\\
&=\mathbf w_t+\alpha\big(R_{t+1}\mathbf x_t-\mathbf x_t(\mathbf x_t-\gamma\mathbf x_{t+1})^\top\mathbf w_t\big),
\end{aligned} \tag{9.9}
\]

其中以 \(\mathbf x_t=\mathbf x(S_t)\) 作简写。系统进入稳态后，对任一给定的 \(\mathbf w_t\)，下一权重向量的期望可写为

\[
\mathbb E[\mathbf w_{t+1}\mid\mathbf w_t]=\mathbf w_t+\alpha(\mathbf b-\mathbf A\mathbf w_t), \tag{9.10}
\]
