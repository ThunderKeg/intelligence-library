:::source-box

### LSTD：估计 \(\hat v=\mathbf w^\top\mathbf x(\cdot)\approx v_\pi\)（\(O(d^2)\) 版本）

输入：特征表示 \(\mathbf x:\mathcal S^+\to\mathbb R^d\)，且 \(\mathbf x(\text{终止状态})=\mathbf 0\)。

算法参数：很小的 \(\epsilon>0\)。

初始化：

$$
\hat{\mathbf A}^{-1}\leftarrow\epsilon^{-1}\mathbf I
$$

上式为 \(d\times d\) 矩阵。

$$
\hat{\mathbf b}\leftarrow\mathbf 0
$$

上式为 \(d\) 维向量。

对每个回合循环：

　初始化 \(S\)；令 \(\mathbf x\leftarrow\mathbf x(S)\)。

　对该回合的每一步循环：

　　选择并执行行动 \(A\sim\pi(\cdot\mid S)\)，观察 \(R,S'\)；令 \(\mathbf x'\leftarrow\mathbf x(S')\)。

$$
\mathbf v\leftarrow\hat{\mathbf A}^{-1}(\mathbf x-\gamma\mathbf x')
$$

$$
\hat{\mathbf A}^{-1}\leftarrow
\hat{\mathbf A}^{-1}
-\frac{(\hat{\mathbf A}^{-1}\mathbf x)\mathbf v^\top}
{1+\mathbf v^\top\mathbf x}
$$

$$
\hat{\mathbf b}\leftarrow\hat{\mathbf b}+R\mathbf x
$$

$$
\mathbf w\leftarrow\hat{\mathbf A}^{-1}\hat{\mathbf b}
$$

$$
S\leftarrow S',\qquad \mathbf x\leftarrow\mathbf x'
$$

　直到 \(S'\) 是终止状态时结束本回合。

:::end-source-box

## 9.9　基于记忆的函数近似

到目前为止，我们讨论的是近似价值函数的*参数化方法*。在这种方法中，学习算法调整某种函数形式的参数，力求在问题的整个状态空间内近似价值函数。每次更新 \(s\mapsto g\) 都是一个训练样本；学习算法用它改变参数，以减小近似误差。更新之后，训练样本可以丢弃（当然也可以保存以便再次使用）。需要估计某个状态的价值时——下文称它为*查询状态*——只须使用学习算法得到的最新参数，在该状态上求函数值。

基于记忆的函数近似方法截然不同。训练样本到达时，它们只是把样本保存到存储器中（至少保存其中一部分），并不更新任何参数。此后，每当需要查询状态的价值估计时，就从存储器中取出一组样本，用它们计算查询状态的估计价值。这种方法有时称为*惰性学习*（lazy learning），因为训练样本的处理被推迟到系统收到输出查询时才进行。

基于记忆的函数近似是*非参数化方法*的典型例子。与参数化方法不同，近似函数的形式不局限于线性函数、多项式等某个固定的参数化函数类，而由训练样本本身以及把样本组合起来、输出查询状态估计价值的方法共同决定。随着存储器中积累更多训练样本，非参数化方法有望越来越精确地近似任意目标函数。
