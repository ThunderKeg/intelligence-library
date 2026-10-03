图 15.5a 展示了以 ANN 实现的行动者—评论家算法，其中有分别实现行动者和评论家的网络。评论家包含一个类似神经元的单元 \(V\)，其输出活动表示状态价值；还有一个标记为 TD 的菱形模块，它把 \(V\) 的输出、奖励信号以及先前的状态价值结合起来，计算 TD 误差（从 TD 菱形回到自身的回路表示后者）。行动者网络由单层 \(k\) 个行动者单元 \(A_i\) 组成，\(i=1,\ldots,k\)。每个行动者单元的输出，是一个 \(k\) 维行动向量的一个分量。另一种理解是，这 \(k\) 个单元分别发出一个行动指令，彼此竞争以决定执行哪一个；但这里我们把整个 \(\mathbf A\) 向量视为一次行动。

![图15.5：行动者—评论家人工神经网络及假设的神经实现](assets/fig-15-5.png)

图 15.5：行动者—评论家 ANN 及一种假设的神经实现。(a) 行动者—评论家算法的 ANN 实现。行动者根据从评论家收到的 TD 误差 \(\delta\) 调整策略；评论家使用同一个 \(\delta\) 调整状态价值参数。评论家根据奖励信号 \(R\) 和当前估计状态价值的变化产生 TD 误差。行动者不能直接取得奖励信号，评论家也不能直接取得行动。(b) 行动者—评论家算法的一种假设神经实现：行动者和评论家中学习价值的部分，分别位于纹状体背侧部和腹侧部。位于 VTA 和 SNpc 的多巴胺神经元传递 TD 误差，调节来自各皮质区、投向纹状体腹侧部和背侧部的输入突触效能的变化。改编自 Y. Takahashi、G. Schoenbaum 和 Y. Niv，〈Silencing the critics: Understanding the effects of cocaine sensitization on dorsolateral and ventral striatum in the context of an Actor/Critic model〉，《Frontiers in Neuroscience》，第 2 卷第 1 期，2008 年。

图内文字译注：(a) Environment：环境；Reward：奖励；States/Stimuli：状态／刺激；Critic：评论家；Actor：行动者；Actions：行动；TD error \(\delta\)：TD 误差 \(\delta\)。(b) Cortex (multiple areas)：大脑皮质（多个区域）；Ventral striatum：纹状体腹侧部；Dorsal striatum：纹状体背侧部；VTA：腹侧被盖区；SNc（图内标记）：黑质致密部；Dopamine：多巴胺；其余相同的英文标记沿用 (a) 的译法。图中的 \(x_1,\ldots,x_n\) 是状态或刺激特征，\(V\) 是价值输出，\(A_1,\ldots,A_k\) 是行动者单元的输出。
