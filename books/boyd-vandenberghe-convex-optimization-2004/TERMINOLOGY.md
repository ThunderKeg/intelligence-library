# 全书术语表

译文以原书具体语境为准；本表由集成 Agent 维护。保留英文的人名与书目信息不强行音译。

| English | 中文 | 说明 |
| --- | --- | --- |
| convex / concave | 凸／凹 | 与函数或集合连用 |
| nondecreasing / nonincreasing | 非减／非增 | 需要时写“单调非减／单调非增”，不能误译为严格递增／严格递减 |
| affine | 仿射 | 不写成线性 |
| convex optimization | 凸优化 | |
| least squares | 最小二乘 | |
| linear programming | 线性规划 | |
| quadratic programming | 二次规划 | |
| semidefinite programming | 半定规划 | |
| second-order cone programming | 二阶锥规划 | |
| geometric programming | 几何规划 | |
| objective function | 目标函数 | |
| constraint | 约束 | |
| active / inactive constraint | 有效／非有效约束 | 首次保留英文；有效指在所讨论点取等号，不与可行／不可行混用 |
| slack variable | 松弛变量 | |
| box constraints | 盒约束 | 各分量分别受上下界约束 |
| oracle model | oracle 模型 | 保留英文，按原文说明为黑箱模型或子程序模型 |
| feasible / infeasible | 可行／不可行 | |
| optimal value / optimal point | 最优值／最优点 | 区别值与取值位置 |
| local / global optimum | 局部／全局最优解 | 根据所指区分最优值 |
| dual / primal | 对偶／原 | 原问题、对偶问题 |
| duality gap | 对偶间隙 | |
| weak / strong duality | 弱／强对偶性 | |
| Slater's constraint qualification | Slater 约束资格条件 | 首次保留 constraint qualification |
| two-way partitioning | 两路划分 | 第 5.1.5 节首次保留英文；与二分法区别 |
| water-filling algorithm | 注水算法 | |
| contact force | 接触力 | |
| Lagrange multiplier | 拉格朗日乘子 | |
| Lagrangian | 拉格朗日函数 | 不与拉格朗日对偶函数混用 |
| theorem of alternatives | 择一定理 | 沿用例 2.21、2.26；成对系统称“择一系统” |
| saddle point | 鞍点 | |
| max-min inequality | 极大极小不等式 | 具体上确界／下确界及顺序按原式保留 |
| shadow price | 影子价格 | 第 5 章价格解释与灵敏度分析 |
| complementary slackness | 互补松弛性 | |
| payoff matrix | 支付矩阵 | 第 5.2.5 节零和矩阵博弈语境 |
| positive semidefinite | 半正定 | |
| positive definite | 正定 | |
| quasiconvex / quasiconcave | 拟凸／拟凹 | 首次注明英文 |
| quasilinear | 拟线性 | 同时拟凸与拟凹 |
| log-concave / log-convex | 对数凹／对数凸 | 不与拟凹／拟凸混用 |
| conjugate function | 共轭函数 | |
| support function | 支撑函数 | 与支撑超平面区别 |
| pointwise maximum / supremum | 逐点最大值／逐点上确界 | 保留最大值与上确界的区别 |
| matrix convex / matrix concave | 矩阵凸／矩阵凹 | 关于半正定锥的广义不等式 |
| Hessian | Hessian 矩阵 | 保留原词，表示二阶导数矩阵 |
| indicator function | 指示函数 | 第 3 章与第 8.1.3 节取 0 或正无穷；第 7.4 节按原书另定义为 0/1，须在各自语境明确取值 |
| extended-value extension | 扩展值延拓 | 第 3 章按原定义在定义域外延拓为正无穷或负无穷 |
| log-sum-exp | 指数和的对数 | 首次保留英文 |
| geometric mean | 几何平均 | |
| log-determinant | 对数行列式 | log det X |
| quadratic-over-linear function | 二次除以线性函数 | 首次注明英文，并保留原式与定义域 |
| epigraph | 上图 | 首次注明英文并随原文定义 |
| sublevel set | 下水平集 | |
| supporting hyperplane | 支撑超平面 | |
| generalized inequality | 广义不等式 | |
| orthant / nonnegative orthant | 正交象限／非负正交象限 | 与第 2 章首次定义保持一致；不混用正交体 |
| proper cone | 正常锥 | 首次注明英文，闭、凸、实心、尖四项条件均按原文解释 |
| inverse image | 原像 | 与函数的逆区别 |
| perspective function | 透视函数 | |
| linear-fractional function | 线性分式函数 | |
| slab | 条带 | 首次注明英文 |
| minimum element / minimal element | 最小元素／极小元素 | 两个定义不可互换 |
| interior-point method | 内点法 | |
| barrier method / barrier function | 障碍法／障碍函数 | |
| self-concordance | 自协调性 | 首次注明英文 |
| descent method | 下降法 | |
| steepest descent | 最速下降 | |
| Newton's method | 牛顿法 | |
| Newton decrement | 牛顿减量 | 首次保留英文，按原书区分减量与减量的平方 |
| backtracking line search | 回溯直线搜索 | |
| norm / dual norm | 范数／对偶范数 | |
| approximation / fitting | 逼近／拟合 | |
| penalty function | 罚函数 | 第 6 章逼近问题语境 |
| deadzone-linear penalty function | 死区线性罚函数 | 死区内罚值为零；函数与范围按原式保留 |
| log barrier penalty function | 对数障碍罚函数 | 与“障碍函数”统一 |
| Huber penalty function | Huber 罚函数 | 保留人名 |
| outlier | 离群点 | |
| robust least-squares | 鲁棒最小二乘 | |
| residual | 残差 | 图 6.2 的 residual amplitudes 译为“残差取值”，保留横轴的正负号 |
| regularization | 正则化 | |
| sparse regressor selection | 稀疏回归变量选择 | |
| total variation reconstruction | 总变差重构 | |
| basis pursuit | 基追踪 | 首次保留英文 |
| positive-real function | 正实函数 | 习题 6.14 首次注明英文，按原文保留解析性及实部非负的条件 |
| Hermitian matrix | Hermitian 矩阵 | 与实对称矩阵区别，保留复共轭转置记号 |
| goods basket | 商品组合 | 第 6 章消费者偏好语境 |
| amplitude distribution | 取值分布 | 第 6 章保留有符号取值，不与绝对值幅值混用 |
| robust | 鲁棒 | 视名词写鲁棒性 |
| nominal value | 标称值 | 第 4 章工程参数语境；不与金融名义金额混用 |
| sensitivity analysis | 灵敏度分析 | |
| Schur complement | Schur 补 | |
| monomial | 单项式 | 第 4 章几何规划语境首次保留英文；指数可为任意实数，保留原文与通常多项式定义的区别 |
| posynomial | 正项式 | 第 4 章首次注明英文，系数为正的单项式之和 |
| Pareto optimal | Pareto 最优 | 与向量优化中更强的“最优”区别 |
| multicriterion / bicriterion optimization | 多准则／双准则优化 | 与第 4.7 节一致 |
| scalarization | 标量化 | |
| trade-off | 权衡 | |
| utility | 效用 | |
| likelihood / log-likelihood function | 似然函数／对数似然函数 | 第 7 章保留“将观测固定后视为参数的函数”的区分 |
| maximum likelihood estimation | 最大似然估计 | 首次注明英文和 ML，随后可写 ML 估计 |
| maximum a posteriori probability estimation | 最大后验概率估计 | 首次注明英文和 MAP，随后可写 MAP 估计 |
| prior / posterior density | 先验密度／后验密度 | |
| information matrix | 信息矩阵 | 第 7.1 节特指协方差矩阵的逆，不能改作 Fisher 信息矩阵 |
| logistic regression | logistic 回归 | 保留 logistic，避免与逻辑运算混淆 |
| randomized / deterministic detector | 随机化／确定性检测器 | 随机化指观测后按给定概率选择判断，不把“随机化”省作“随机” |
| detection probability matrix | 检测概率矩阵 | 第 7.3 节 D 的列对应实际假设，行对应检测结果 |
| minimax detector | 极小极大检测器 | 最小化各假设中最大的错误概率 |
| worst-case | 最坏情形 | 与已验收的第 4–6 章用语一致 |
| false positive / false negative | 假阳性／假阴性 | 二元假设检验；false alarm probability 为虚警概率 |
| receiver operating characteristic | 接收者操作特征 | 首次保留英文与 ROC，原书采用假阳性与假阴性概率的权衡曲线 |
| likelihood ratio threshold test | 似然比阈值检验 | 保留原式中的阈值方向和等号归属 |
| cumulant generating function | 累积量生成函数 | 与矩生成函数区别，按原书为其对数 |
| signal constellation | 信号星座 | 第 7.4.3 节候选信号点的集合 |
| minimum-distance detector | 最小距离检测器 | 此处使用欧几里得距离 |
| experiment design | 实验设计 | D／E／A 最优设计的字母保留原数学字体 |
| confidence ellipsoid | 置信椭球 | 不省去置信水平 |
| yield | 成品率 | 制成品中合格产品的比例；第 3.43 例与习题 4.63 一致 |
| total return | 总回报 | 习题 4.60 定义为 W(t)/W(t−1)，不擅自减去 1 |
| optimization with recourse | 带补救决策的优化 | 首次保留英文；在获知情景后选择第二阶段变量 |
| recourse variable | 补救变量 | 亦称第二阶段变量，首次保留英文 |
| two-stage optimization | 两阶段优化 | 习题 4.64 与后文 9.29 使用同一术语 |
| floor planning | 平面布局 | 第8章按设计语境使用 |
| projection | 投影 | 第 8 章按指定范数定义，不默认所有投影都是欧几里得投影 |
| placement | 布置 | 与平面布局区别，按原文保留节点与位置变量 |
| location | 选址 | 第 8.7 节设施与节点位置问题 |
| Gram matrix | Gram 矩阵 | 保留英文名称，不与距离矩阵混同 |
| Euclidean distance matrix | 欧几里得距离矩阵 | 第 8.3.3 节定义元素为距离的平方，须随原定义保留 |
| realizability | 可实现性 | 第 8.3 节指是否存在满足指定距离或角度条件的点集 |
| Löwner-John ellipsoid | Löwner-John 椭球 | 第 8.4 节采用最小体积覆盖椭球的定义 |
| maximum volume inscribed ellipsoid | 最大体积内接椭球 | “位于集合内”允许边界接触，不译成严格内部 |
| Chebyshev center | Chebyshev 中心 | 范数依具体问题给定 |
| analytic center | 解析中心 | 对应具体不等式／等式描述，通常不只是集合本身的函数 |
| linear discrimination | 线性判别 | 按原书使用仿射分类函数 |
| support vector classifier | 支持向量分类器 | 保留原目标函数中的范数，不按其他教材改成平方范数 |
| bounding box | 包围盒 | 第 8 章矩形外包区域 |
| aspect ratio | 高宽比／宽高比 | 按原式分子与分母区分：8.8.2 为 h_i/w_i，例 8.7 为 w_i/h_i |
| convex restriction | 凸限制 | 缩小可行集而得到凸问题，与凸松弛区别 |
| strongly convex | 强凸 | 不与严格凸混同；第 9.1.2 节按 Hessian 一致正定下界定义 |
| minimizing sequence | 最小化序列 | 函数值趋于最优值，未必存在有限的最优点 |
| normal equations | 正规方程 | 与第 1 章最小二乘用语一致 |
| gradient descent method / gradient method | 梯度下降法／梯度法 | 随原文保留全称和简称；不与最速下降法混同 |
| exact line search | 精确直线搜索 | 与回溯直线搜索区别，按搜索射线求最小值 |
| linear convergence | 线性收敛 | 第 9 章指误差按等比速度趋零，不是每次减少相同的数值 |
| twice differentiable / twice continuously differentiable | 二阶可微／二阶连续可微 | 与二次函数、二次模型和二次收敛区别；第 3／6 章 14 处旧译经原页核准后统一 |
| minimally self-concordant | 极小自协调 | 首次保留英文并保留本节完整缩放定义，不与函数值的极小点混同 |
| quadratic convergence | 二次收敛 | 按原书误差递推关系使用，与二阶可微区别 |
| stopping criterion | 停止准则 | 第 9 章梯度法、牛顿法和习题统一使用 |
| forward substitution / back substitution | 前代／回代 | 按下三角／上三角线性方程组的求解顺序使用 |
| Newton system | 牛顿方程组 | 保留所讨论问题的矩阵结构，不默认仅含 Hessian 矩阵 |
| symbolic factorization | 符号分解 | 利用非零元素的位置确定分解中的稀疏结构 |
| KKT system / KKT matrix | KKT 方程组／KKT 矩阵 | 按原书的分块矩阵及等式约束保留 |
| primal / dual feasibility equations | 原／对偶可行性方程 | 与第 5 章“原问题、原可行点”一致 |
| elimination matrix | 消元矩阵 | 消去等式约束时使用的零空间基矩阵 |
| reduced problem / reduced objective function | 约化问题／约化后的目标函数 | 第 10 章指消去等式约束后得到的无约束问题及其目标函数 |
| infeasible start Newton method | 不可行初始点牛顿法 | 初始点可以不满足等式约束，仍须属于目标函数的定义域 |
| convex-concave game / strongly convex-concave game | 凸–凹博弈／强凸–凹博弈 | 按第 10.3.4 节对两个变量分别凸、凹的条件使用 |
| payoff function | 支付函数 | 与第 5 章“支付矩阵”一致，保留参与者之间的支付方向 |
| primal-dual method | 原始–对偶方法 | 复合术语沿用第 9–10 章译法；单独 primal problem 仍为“原问题” |
| time horizon | 时间跨度 | 第 10.4.3 节最优控制算例中用 N 表示，不改变原离散时间指标 |
| central path / central point | 中心路径／中心点 | 第 11.2 节由正参数 t 对应的障碍子问题最优点定义 |
| centering step | 中心化步骤 | 障碍法的一次外层迭代；与该步骤内部的牛顿迭代区别 |
| path-following method | 路径跟随法 | 第 11.3 节中障碍法的另一名称 |
| surrogate duality gap | 替代对偶间隙 | 第 11.7 节沿用原始–对偶方法的定义，未满足可行性时不直接称为对偶间隙 |
| Euclidean norm / Euclidean distance | 欧几里得范数／欧几里得距离 | 与正文、附录 A 和符号表统一；non-Euclidean 为非欧几里得 |
| maximum entropy problem | 最大熵问题 | 第 7.2 节原题名及问题名；不强行改写为另一种名词结构 |
| operator norm | 算子范数 | 附录 A.1.5 按给定的两个向量范数诱导，不默认总是谱范数 |
| range / nullspace | 值域／零空间 | 附录 A.5.1 的线性映射语境，使用原花体记号 |
| field of values | 值域 | 附录 B.3 保留英文区分，是由两个对称矩阵的二次型共同定义的集合 |
| pseudoinverse | 伪逆 | 原书亦称 Moore–Penrose 逆，保留原定义 |
| condition number | 条件数 | 附录 A.5.4 的非奇异方阵语境，保留原比值定义 |
| factor-solve method | 分解–求解法 | 附录 C.2.2 区分矩阵分解与逐个求解已分解方程组的成本 |
| flop | 浮点运算 | 附录 C 按原书加／减／乘／除一次的计数约定使用 |
| underdetermined linear equations | 欠定线性方程组 | 附录 C.5 原矩阵满秩前提及解集参数化均保留 |

跨章变更须重新检查已验收章节，不把术语统一等同于正文完整性审查。
