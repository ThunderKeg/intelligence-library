# 术语与记号工作表

本表记录已核对章节采用的译法。后续章节出现不同语境时，对照原书 PDF 判断，再在全书审查时统一。

| 原词 | 当前译法 | 使用说明 |
| --- | --- | --- |
| agent | 智能体 | 与 environment（环境）成对。 |
| action | 行动 | 正文叙述用“行动”；在 action value 等复合术语中用“动作”。 |
| reward | 奖励 | 数值形式的奖励信号。 |
| return | 回报 | 与单步奖励区分。 |
| episode / episodic task | 回合 / 回合式任务 | 与持续式任务相对；全书保持统一。 |
| policy | 策略 | 将情境或状态映射到行动。 |
| value function | 价值函数 | 与单步奖励区分。 |
| action value | 动作价值 | 第 2 章方法名为“动作价值方法”。 |
| exploration / exploitation | 探索 / 利用 | 保留两者的权衡含义。 |
| greedy / ε-greedy | 贪心 / ε-贪心 | 用于行动选择方法。 |
| bandit | 赌博机 | 第 2 章用“多臂赌博机”；关联问题用“情境赌博机”。 |
| stationary / nonstationary | 平稳 / 非平稳 | 指奖励分布或问题随时间变化与否。 |
| temporal-difference learning | 时序差分学习 | 缩写 TD 可保留。 |
| on-policy / off-policy | 同策略 / 异策略 | 与行为策略和目标策略的关系相对应。 |
| bootstrapping | 自举 | 第 7 章标题“n 步自举”。 |
| tile coding / tiling / tile | 瓦片编码 / 铺砌 / 瓦片 | 第 9–10 章：方法称“瓦片编码”，一个错位的覆盖层称“铺砌”。 |
| eligibility trace | 资格迹 | 第 12 章的方法机制；与 TD(λ) 等算法中的迹相对应。 |
| policy gradient | 策略梯度 | 第 13 章直接对参数化策略的表现求梯度。 |
| option | 选项 | 第 17 章的时间抽象行动过程；首次出现时保留英文。 |
| general value function (GVF) / cumulant | 一般价值函数 / 累积信号 | 第 17 章将预测信号从奖励推广到任意累积信号。 |
| afterstate / afterstate value function | 后继状态 / 后继状态价值函数 | 指智能体行动已产生直接效果、环境其余动态尚未发生时的状态。 |
| maximization bias / double learning | 最大化偏差 / 双重学习 | 第 6 章术语。 |
| tree-backup | 树备份 | 与“回溯”区分，卷首与目录用词一致。 |
| exploring starts | 探索性起始 | 不限定为初始状态，包含起始动作。 |
| average reward / reward rate | 平均奖励 / 奖励率 | 持续性任务按策略的长期每步奖励。 |
| differential return / value function | 差分回报 / 差分价值函数 | 每步奖励减去平均奖励后的回报及相应价值。 |
| ergodic | 遍历的 | 本书第 10 章指稳态分布存在且与初始状态无关。 |
| molar stimulus traces | 整体刺激迹 | 第 14 章 Hull 的术语；“molar”强调行为整体层次，不译为“摩尔”。 |
| reward prediction error (RPE) | 奖励预测误差 | 第 15 章多巴胺神经元时相反应假说的核心概念。 |
| phasic response | 时相反应 | 与持续的基线活动区分。 |
| medium spiny neuron | 中型多棘神经元 | 第 15 章纹状体的主要输入／输出神经元。 |
| corticostriatal synapse | 皮层—纹状体突触 | 皮层至纹状体通路上的突触。 |
| deep Q-network (DQN) | 深度 Q 网络 | 第 16 章 Atari 游戏应用。 |
| experience replay | 经验回放 | 第 16 章 DQN 的回放记忆和随机小批量更新。 |
| First-Ready, First-Come-First-Serve (FR-FCFS) | 先就绪、先到先服务 | 第 16 章内存控制调度策略。 |

数学变量遵守原书第二版的大小写、上下标和加横线记号；不要用字面下划线或逐字组合附加横线替代整组数学排版。网页所需的复杂记号在逐页源稿中用 `\(...\)` 写成 TeX，并在生成 JSON 时转为 MathML。
