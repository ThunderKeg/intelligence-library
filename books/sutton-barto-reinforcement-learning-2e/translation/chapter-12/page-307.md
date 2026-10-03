:::algorithm

### 真在线 Sarsa(\(\lambda\))：估计 \(\mathbf w^\top\mathbf x\approx q_\pi\) 或 \(q_*\)

输入：特征函数 \(\mathbf x:\mathcal S^+\times\mathcal A\to\mathbb R^d\)，并令 \(\mathbf x(\text{终止状态},\cdot)=\mathbf0\)。

输入：策略 \(\pi\)（若估计 \(q_\pi\)）。

算法参数：步长 \(\alpha>0\)、迹衰减率 \(\lambda\in[0,1]\)、很小的 \(\varepsilon>0\)。

初始化：\(\mathbf w\in\mathbb R^d\)（例如 \(\mathbf w=\mathbf0\)）。

对每个回合循环：

　初始化 \(S\)。

　按 \(\pi(\cdot\mid S)\) 选择 \(A\)，或按 \(\hat q(S,\cdot,\mathbf w)\) 作 \(\varepsilon\)-贪心选择。

　\(\mathbf x\leftarrow\mathbf x(S,A)\)。

　\(\mathbf z\leftarrow\mathbf0\)。

　\(Q_{\mathrm{old}}\leftarrow0\)。

　对该回合的每一步循环：

　　执行行动 \(A\)，观察 \(R,S'\)。

　　按 \(\pi(\cdot\mid S')\) 选择 \(A'\)，或按 \(\hat q(S',\cdot,\mathbf w)\) 作 \(\varepsilon\)-贪心选择。

　　\(\mathbf x'\leftarrow\mathbf x(S',A')\)。

　　\(Q\leftarrow\mathbf w^\top\mathbf x\)。

　　\(Q'\leftarrow\mathbf w^\top\mathbf x'\)。

　　\(\delta\leftarrow R+\gamma Q'-Q\)。

　　\(\mathbf z\leftarrow\gamma\lambda\mathbf z+
(1-\alpha\gamma\lambda\mathbf z^\top\mathbf x)\mathbf x\)。

　　\(\mathbf w\leftarrow\mathbf w+\alpha(\delta+Q-Q_{\mathrm{old}})\mathbf z
-\alpha(Q-Q_{\mathrm{old}})\mathbf x\)。

　　\(Q_{\mathrm{old}}\leftarrow Q'\)。

　　\(\mathbf x\leftarrow\mathbf x'\)。

　　\(A\leftarrow A'\)。

　直到 \(S'\) 是终止状态。

:::end-algorithm

最后，还有一种 Sarsa(\(\lambda\)) 的截断版本，称为前向 Sarsa(\(\lambda\))（van Seijen，2016）；它看来是一种特别适合与多层人工神经网络配合使用的高效无模型控制方法。

## 12.8　可变的 \(\lambda\) 与 \(\gamma\)

本书对基本 TD 学习算法的介绍即将结束。为了以最一般的形式给出最后几种算法，把自举与折扣的程度从常数参数推广为可能依赖状态和行动的函数，会很有用。也就是说，每个时间步都有不同的 \(\lambda\) 和 \(\gamma\)，分别记为 \(\lambda_t\) 和 \(\gamma_t\)。现在调整记号：令 \(\lambda:\mathcal S\times\mathcal A\to[0,1]\) 为从状态与行动到单位区间的函数，使 \(\lambda_t\doteq\lambda(S_t,A_t)\)；类似地，令 \(\gamma:\mathcal S\to[0,1]\) 为从状态到单位区间的函数，使 \(\gamma_t\doteq\gamma(S_t)\)。

引入函数 \(\gamma\)——**终止函数（termination function）**——尤其重要，因为它改变了回报这一基本随机变量，而我们要估计的正是它的期望。现在，把回报更一般地定义为
