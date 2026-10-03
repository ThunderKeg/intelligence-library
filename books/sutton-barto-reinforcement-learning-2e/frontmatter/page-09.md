# 目录（续）

## 7 n 步自举（n-step Bootstrapping）—— 141

- 7.1 n 步 TD 预测（n-step TD Prediction）—— 142
- 7.2 n 步 Sarsa（n-step Sarsa）—— 145
- 7.3 n 步异策略学习（n-step Off-policy Learning）—— 148
- 7.4 *采用控制变量的逐决策方法（Per-decision Methods with Control Variates）—— 150
- 7.5 不使用重要性采样的异策略学习：n 步树备份算法（Off-policy Learning Without Importance Sampling: The n-step Tree Backup Algorithm）—— 152
- 7.6 *统一的算法：n 步 Q(σ)（A Unifying Algorithm: n-step Q(σ)）—— 154
- 7.7 小结（Summary）—— 157

## 8 用表格型方法进行规划与学习（Planning and Learning with Tabular Methods）—— 159

- 8.1 模型与规划（Models and Planning）—— 159
- 8.2 Dyna：整合规划、行动与学习（Dyna: Integrated Planning, Acting, and Learning）—— 161
- 8.3 模型出错时（When the Model Is Wrong）—— 166
- 8.4 优先级扫描（Prioritized Sweeping）—— 168
- 8.5 期望更新与采样更新（Expected vs. Sample Updates）—— 172
- 8.6 轨迹采样（Trajectory Sampling）—— 174
- 8.7 实时动态规划（Real-time Dynamic Programming）—— 177
- 8.8 决策时规划（Planning at Decision Time）—— 180
- 8.9 启发式搜索（Heuristic Search）—— 181
- 8.10 Rollout 算法（Rollout Algorithms）—— 183
- 8.11 蒙特卡洛树搜索（Monte Carlo Tree Search）—— 185
- 8.12 本章小结（Summary of the Chapter）—— 188
- 8.13 第一部分总结：各个维度（Summary of Part I: Dimensions）—— 189

## 第二部分 近似解法（Approximate Solution Methods） —— 195

## 9 使用函数近似的同策略预测（On-policy Prediction with Approximation）—— 197

- 9.1 价值函数近似（Value-function Approximation）—— 198
- 9.2 预测目标（\(\overline{\mathrm{VE}}\)）（The Prediction Objective (\(\overline{\mathrm{VE}}\))）—— 199
- 9.3 随机梯度法与半梯度法（Stochastic-gradient and Semi-gradient Methods）—— 200
- 9.4 线性方法（Linear Methods）—— 204
- 9.5 为线性方法构造特征（Feature Construction for Linear Methods）—— 210
  - 9.5.1 多项式（Polynomials）—— 210
  - 9.5.2 傅里叶基（Fourier Basis）—— 211
  - 9.5.3 粗编码（Coarse Coding）—— 215
  - 9.5.4 瓦片编码（Tile Coding）—— 217
  - 9.5.5 径向基函数（Radial Basis Functions）—— 221
- 9.6 手动选择步长参数（Selecting Step-Size Parameters Manually）—— 222
- 9.7 非线性函数近似：人工神经网络（Nonlinear Function Approximation: Artificial Neural Networks）—— 223
- 9.8 最小二乘 TD（Least-Squares TD）—— 228
