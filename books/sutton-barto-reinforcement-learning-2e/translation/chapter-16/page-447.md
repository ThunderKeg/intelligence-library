总的来说，AlphaGo 惊人的成功重新激发了人们对人工智能前景的热情，尤其是对结合强化学习与深度 ANN、解决其他领域难题的系统的期待。

### 16.6.2　AlphaGo Zero

DeepMind 团队借鉴 AlphaGo 的经验，开发了 AlphaGo Zero（Silver 等，2017a）。与 AlphaGo 不同，它不使用围棋基本规则之外的任何人类数据或指导，名称中的 Zero 即由此而来。它完全通过自我对弈强化学习来学习，输入只是棋盘上棋子位置的“原始”描述。AlphaGo Zero 实现了一种策略迭代（§4.3）：策略评估与策略改进交替进行。图 16.7 概览了算法。AlphaGo Zero 与 AlphaGo 的一个显著差别是：AlphaGo Zero 在整个自我对弈强化学习期间都用 MCTS 选择着法，而 AlphaGo 是在学习结束后、正式对局期间才使用 MCTS。除了不使用人类数据和人工设计的特征，另一些区别是：AlphaGo Zero 只用一个深度卷积 ANN，且采用更简单的 MCTS。

AlphaGo Zero 的 MCTS 比 AlphaGo 的版本简单：它不包含完整对局的 rollout，因此也不需要 rollout 策略。每次 MCTS 迭代执行一次模拟，终点是当前搜索树的叶节点，而不是一盘完整模拟对局的终局。不过，如同 AlphaGo，AlphaGo Zero 每次 MCTS 迭代仍由深度卷积网络的输出引导。图 16.7 把这个网络记为 \(f_{\boldsymbol\theta}\)，其中 \(\boldsymbol\theta\) 是网络权重向量。网络的输入由棋盘局面的原始表征组成；输出有两部分：标量 \(v\)，估计当前棋手从当前局面获胜的概率；向量 \(\mathbf p\)，给出每种可能落点以及停一手或认输的着法概率。

不过，AlphaGo Zero 不直接按 \(\mathbf p\) 的概率选择自我对弈行动，而是用这些概率连同网络输出的价值，引导每次 MCTS 运行。MCTS 返回新的着法概率，图 16.7 中记为策略 \(\pi_i\)。这些策略得益于 MCTS 每次运行中进行的大量模拟。因此，AlphaGo Zero 实际遵循的策略，优于直接由网络输出 \(\mathbf p\) 给出的策略。Silver 等人（2017a）认为，MCTS 因而可视为一种强有力的策略改进算子。
