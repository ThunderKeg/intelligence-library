:::algorithm

### Sarsa(\(\lambda\))：采用二元特征与线性函数近似，估计 \(\mathbf w^\top\mathbf x\approx q_\pi\) 或 \(q_*\)

输入：函数 \(\mathcal F(s,a)\)，返回状态—行动对 \((s,a)\) 的活跃特征（索引）集合。

输入：策略 \(\pi\)。

算法参数：步长 \(\alpha>0\)、迹衰减率 \(\lambda\in[0,1]\)、很小的 \(\varepsilon>0\)。

初始化：\(\mathbf w=(w_1,\ldots,w_d)^\top\in\mathbb R^d\)（例如 \(\mathbf w=\mathbf0\)），\(\mathbf z=(z_1,\ldots,z_d)^\top\in\mathbb R^d\)。

对每个回合循环：

　初始化 \(S\)。

　按 \(\pi(\cdot\mid S)\) 选择 \(A\)，或按 \(\hat q(S,\cdot,\mathbf w)\) 作 \(\varepsilon\)-贪心选择。

　\(\mathbf z\leftarrow\mathbf0\)。

　对该回合的每一步循环：

　　执行行动 \(A\)，观察 \(R,S'\)。

　　\(\delta\leftarrow R\)。

　　对每个 \(i\in\mathcal F(S,A)\) 循环：

　　　\(\delta\leftarrow\delta-w_i\)。

　　　\(z_i\leftarrow z_i+1\)（累积迹）；

　　　或 \(z_i\leftarrow1\)（替换迹）。

　　如果 \(S'\) 是终止状态：

　　　\(\mathbf w\leftarrow\mathbf w+\alpha\delta\mathbf z\)。

　　　转入下一回合。

　　按 \(\pi(\cdot\mid S')\) 选择 \(A'\)，或按 \(\hat q(S',\cdot,\mathbf w)\) 作 \(\varepsilon\)-贪心选择。

　　对每个 \(i\in\mathcal F(S',A')\)：\(\delta\leftarrow\delta+\gamma w_i\)。

　　\(\mathbf w\leftarrow\mathbf w+\alpha\delta\mathbf z\)。

　　\(\mathbf z\leftarrow\gamma\lambda\mathbf z\)。

　　\(S\leftarrow S'\)；\(A\leftarrow A'\)。

:::end-algorithm

**习题 12.6**　修改 Sarsa(\(\lambda\)) 的伪代码，改用式（12.11）的 Dutch 迹，但不采用真在线算法的其他独有特性。假定使用线性函数近似和二元特征。□

**例 12.2：山地车上的 Sarsa(\(\lambda\))。**　下一页的图 12.10 左侧给出例 10.1 中山地车任务采用 Sarsa(\(\lambda\)) 的结果。函数近似、行动选择和环境细节与第 10 章完全相同，因此适合把这里的结果与第 10 章 \(n\) 步 Sarsa 的结果（该图右侧）作数值比较。此前的结果改变更新长度 \(n\)；这里的 Sarsa(\(\lambda\)) 则改变作用类似的迹参数 \(\lambda\)。在这一问题上，Sarsa(\(\lambda\)) 中逐渐衰减的迹自举策略似乎带来了更高效的学习。■

我们理想化 TD 方法的动作价值版本——在线 \(\lambda\)-回报算法（第 12.4 节）——及其高效实现——真在线 TD(\(\lambda\))（第 12.5 节）——也都存在。第 12.4 节除使用本节开头给出的动作价值形式 \(n\) 步回报外，其他内容都不需改动。第 12.5、12.6 节的分析同样适用于动作价值，唯一的改动是使用状态—行动特征向量 \(\mathbf x_t=\mathbf x(S_t,A_t)\)，而不是状态特征向量 \(\mathbf x_t=\mathbf x(S_t)\)。由此得到的高效算法称为**真在线 Sarsa(\(\lambda\))**，其伪代码见下一页的方框。下方图表则比较了山地车例子中各种 Sarsa(\(\lambda\)) 版本的表现。
